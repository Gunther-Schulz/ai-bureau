"""LanceDB connection + schema + hybrid search + reranker pipeline.

Single table `pbs_corpus` holds all chunks (corpus, references,
bausteine), distinguished by metadata. Schema follows
backend/mcp-server/docs/vector-metadata-schema.md.

Hybrid search flow:
1. Dense vector retrieval (bge-m3 embedding similarity)
2. FTS retrieval (Tantivy BM25 over content column)
3. Reciprocal rank fusion (LanceDB native) of top-K from each
4. Metadata filters applied
5. Reranker (bge-reranker-v2-m3) reorders top-K → top-k
6. Return CorpusHit objects
"""
from __future__ import annotations

import logging
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import lancedb
import pyarrow as pa

from pbs_mcp import config
from pbs_mcp.embedder import EMBEDDING_DIM, get_embedder, get_reranker
from pbs_mcp.schemas import CorpusHit

logger = logging.getLogger(__name__)

TABLE_NAME = "pbs_corpus"


def _build_schema() -> pa.Schema:
    """Arrow schema for the pbs_corpus table.

    Columns mirror backend/mcp-server/docs/vector-metadata-schema.md.
    All metadata fields are nullable to allow per-source-type
    population.
    """
    return pa.schema([
        # Identity
        pa.field("id", pa.string()),
        pa.field("content", pa.string()),
        # Vector
        pa.field("vector", pa.list_(pa.float32(), EMBEDDING_DIM)),
        # Source classification
        pa.field("source_type", pa.string()),
        pa.field("source_subtype", pa.string()),
        pa.field("source_path", pa.string()),
        pa.field("source_url", pa.string()),
        # Corpus-specific
        pa.field("project", pa.string()),
        pa.field("doctype", pa.string()),
        pa.field("section", pa.string()),
        pa.field("section_number", pa.string()),
        pa.field("artifact_kind", pa.string()),
        # References-specific
        pa.field("reference_id", pa.string()),
        pa.field("reference_category", pa.string()),
        pa.field("paragraph", pa.string()),
        pa.field("paragraph_label", pa.string()),
        pa.field("jurisdiction", pa.string()),
        pa.field("last_amendment", pa.string()),
        # Bausteine-specific
        pa.field("baustein_name", pa.string()),
        pa.field("baustein_scope", pa.string()),
        pa.field("baustein_status", pa.string()),
        # Timing
        pa.field("indexed_at", pa.timestamp("us")),
        pa.field("source_modified_at", pa.timestamp("us")),
        # Free-form
        pa.field("tags", pa.list_(pa.string())),
        pa.field("chunk_index", pa.int32()),
        pa.field("chunk_total", pa.int32()),
    ])


class CorpusDB:
    """Singleton wrapper around the LanceDB connection + corpus table."""

    _instance: "CorpusDB | None" = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        path = config.lancedb_path()
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Connecting to LanceDB at {path}")
        self.db = lancedb.connect(str(path))
        self._table_handle = None

    @classmethod
    def get(cls) -> "CorpusDB":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def table(self):
        """Lazy-create the table on first access. Creates FTS index too."""
        if self._table_handle is None:
            schema = _build_schema()
            if TABLE_NAME in self.db.table_names():
                self._table_handle = self.db.open_table(TABLE_NAME)
            else:
                logger.info(f"Creating LanceDB table {TABLE_NAME}")
                self._table_handle = self.db.create_table(
                    TABLE_NAME, schema=schema, mode="create"
                )
                # FTS index on content column for hybrid retrieval (BM25-ish via Tantivy)
                try:
                    self._table_handle.create_fts_index("content", replace=True)
                    logger.info("Created FTS index on content column")
                except Exception as e:
                    logger.warning(f"FTS index creation skipped: {e}")
        return self._table_handle

    def ensure_fts_index(self) -> None:
        """Idempotent: ensure FTS index exists on content column.

        Useful after bulk-ingest if FTS index lags behind row inserts
        (LanceDB FTS is not auto-updated; needs explicit re-index after
        large batch inserts).
        """
        try:
            self.table.create_fts_index("content", replace=True)
            logger.info("FTS index refreshed")
        except Exception as e:
            logger.warning(f"FTS index refresh failed: {e}")

    # === Write path ===

    def insert_chunks(self, chunks: list[dict[str, Any]]) -> int:
        """Insert chunks. Each chunk is a dict matching the schema columns.

        Caller must include `vector` (list[float], length EMBEDDING_DIM)
        and at minimum `id`, `content`, `source_type`, `source_path`.
        """
        if not chunks:
            return 0
        # Normalize: ensure all columns present (fill missing with None)
        schema_fields = [f.name for f in _build_schema()]
        normalized = []
        for ch in chunks:
            row = {f: ch.get(f) for f in schema_fields}
            if row.get("id") is None:
                row["id"] = str(uuid.uuid4())
            if row.get("indexed_at") is None:
                row["indexed_at"] = datetime.now()
            if row.get("tags") is None:
                row["tags"] = []
            normalized.append(row)
        self.table.add(normalized)
        return len(normalized)

    def delete_by_path(self, source_path: str) -> int:
        """Delete all chunks belonging to a given source file."""
        before = self.table.count_rows()
        self.table.delete(f"source_path = '{source_path}'")
        after = self.table.count_rows()
        return before - after

    def delete_by_filter(self, where: str) -> int:
        """Delete chunks matching a SQL-style filter expression."""
        before = self.table.count_rows()
        self.table.delete(where)
        after = self.table.count_rows()
        return before - after

    # === Read / search path ===

    def search(
        self,
        query: str,
        k: int = 10,
        filter: dict[str, Any] | None = None,
        rerank: bool = True,
        hybrid: bool = True,
    ) -> list[CorpusHit]:
        """Hybrid retrieval (dense + BM25 via LanceDB FTS) with reranker.

        Pipeline:
          1. Embed query (bge-m3 dense vector).
          2. Hybrid search on table (dense + FTS, RRF-merged) → top-K candidates.
          3. Apply metadata filters.
          4. Reranker (bge-reranker-v2-m3) reorders to top-k.

        Falls back to dense-only when hybrid=False or when FTS index
        is missing.
        """
        embedder = get_embedder()
        qvec = embedder.encode_one(query)

        candidates_k = max(k * 3, 30) if rerank else k

        # Hybrid search: pass both vector and text query.
        # LanceDB merges via reciprocal rank fusion automatically.
        try:
            if hybrid:
                q = (
                    self.table.search(query_type="hybrid")
                    .vector(qvec)
                    .text(query)
                    .limit(candidates_k)
                )
            else:
                q = self.table.search(qvec).limit(candidates_k)
        except (AttributeError, ValueError, NotImplementedError) as e:
            logger.warning(f"Hybrid search unavailable, falling back to dense: {e}")
            q = self.table.search(qvec).limit(candidates_k)

        if filter:
            where_expr = _build_where(filter)
            if where_expr:
                q = q.where(where_expr)

        rows = q.to_list()

        if not rows:
            return []

        if rerank and len(rows) > 1:
            rr = get_reranker()
            docs = [r["content"] for r in rows]
            scores = rr.score(query, docs)
            for r, s in zip(rows, scores):
                r["_rerank_score"] = float(s)
            rows.sort(key=lambda r: r["_rerank_score"], reverse=True)

        rows = rows[:k]

        return [_row_to_hit(r) for r in rows]

    def count(self) -> int:
        return self.table.count_rows()


def _build_where(filter: dict[str, Any]) -> str:
    """Build SQL-style WHERE expression from a filter dict.

    Supported operators per key:
    - scalar -> equality
    - list -> IN
    - dict with $contains -> array contains
    """
    parts: list[str] = []
    for key, value in filter.items():
        if isinstance(value, str):
            parts.append(f"{key} = '{_sql_escape(value)}'")
        elif isinstance(value, list):
            quoted = ", ".join(f"'{_sql_escape(str(v))}'" for v in value)
            parts.append(f"{key} IN ({quoted})")
        elif isinstance(value, dict):
            if "$contains" in value:
                v = value["$contains"]
                parts.append(f"array_has({key}, '{_sql_escape(str(v))}')")
            elif "$gt" in value:
                parts.append(f"{key} > '{_sql_escape(str(value['$gt']))}'")
            elif "$lt" in value:
                parts.append(f"{key} < '{_sql_escape(str(value['$lt']))}'")
        else:
            parts.append(f"{key} = '{_sql_escape(str(value))}'")
    return " AND ".join(parts)


def _sql_escape(s: str) -> str:
    return s.replace("'", "''")


def _row_to_hit(row: dict[str, Any]) -> CorpusHit:
    return CorpusHit(
        content=row.get("content", ""),
        score=float(row.get("_rerank_score", row.get("_distance", 0.0))),
        source_type=row.get("source_type", "corpus"),
        source_subtype=row.get("source_subtype"),
        source_path=row.get("source_path", ""),
        project=row.get("project"),
        doctype=row.get("doctype"),
        section=row.get("section"),
        paragraph=row.get("paragraph"),
        reference_id=row.get("reference_id"),
        tags=row.get("tags") or [],
        indexed_at=row.get("indexed_at"),
    )


def get_db() -> CorpusDB:
    return CorpusDB.get()
