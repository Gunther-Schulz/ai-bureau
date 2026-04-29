"""Ingest tools — ingest_paths, ingest_project_inputs, search_inputs.

Walks paths, applies the right chunker, embeds, writes to LanceDB.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from pbs_mcp import config
from pbs_mcp.chunkers import select_chunker
from pbs_mcp.db import get_db
from pbs_mcp.embedder import get_embedder
from pbs_mcp.schemas import (
    IngestPathsInput,
    IngestPathsOutput,
    IngestProjectInputsInput,
    IngestProjectInputsOutput,
    SearchInputsInput,
    SearchInputsOutput,
)
from pbs_mcp.tools.corpus import search_corpus
from pbs_mcp.schemas import SearchCorpusInput

logger = logging.getLogger(__name__)


def ingest_paths(input: IngestPathsInput) -> IngestPathsOutput:
    db = get_db()
    embedder = get_embedder()

    indexed: list[str] = []
    skipped: list[str] = []
    errors: list[dict[str, str]] = []
    total_chunks = 0

    for raw_path in input.paths:
        p = Path(raw_path)
        if not p.is_file():
            errors.append({"path": raw_path, "error": "not a file"})
            continue

        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
        except OSError as e:
            errors.append({"path": raw_path, "error": f"stat failed: {e}"})
            continue

        # Force-mode deletes existing chunks for this path before re-insert.
        # No-force mode is best-effort skip if mtime matches indexed_at.
        if input.force:
            db.delete_by_path(str(p))

        try:
            content = _read_file(p)
        except Exception as e:
            errors.append({"path": raw_path, "error": f"read failed: {e}"})
            continue

        chunker = select_chunker(str(p))
        try:
            raw_chunks = chunker(str(p), content, None)
        except Exception as e:
            errors.append({"path": raw_path, "error": f"chunker failed: {e}"})
            continue

        if not raw_chunks:
            skipped.append(raw_path)
            continue

        # Embed batch
        texts = [c["content"] for c in raw_chunks]
        try:
            vectors = embedder.encode_batch(texts)
        except Exception as e:
            errors.append({"path": raw_path, "error": f"embed failed: {e}"})
            continue

        # Compose rows for LanceDB
        rows = []
        source_subtype = _infer_source_subtype(str(p), input.source_type)
        extra = input.extra_metadata
        for chunk, vec in zip(raw_chunks, vectors):
            row = {
                "id": str(uuid.uuid4()),
                "content": chunk["content"],
                "vector": vec,
                "source_type": input.source_type,
                "source_subtype": source_subtype,
                "source_path": str(p),
                "indexed_at": datetime.now(),
                "source_modified_at": mtime,
                "tags": chunk.get("tags") or [],
                "chunk_index": chunk.get("chunk_index", 0),
                "chunk_total": chunk.get("chunk_total", 1),
                # Metadata from chunker
                "section": chunk.get("section"),
                "section_number": chunk.get("section_number"),
                "paragraph": chunk.get("paragraph"),
                "paragraph_label": chunk.get("paragraph_label"),
                # Metadata from caller
                "project": extra.get("project"),
                "doctype": extra.get("doctype"),
                "artifact_kind": extra.get("artifact_kind"),
                "reference_id": extra.get("reference_id"),
                "reference_category": extra.get("reference_category"),
                "jurisdiction": extra.get("jurisdiction"),
                "last_amendment": extra.get("last_amendment"),
                "baustein_name": extra.get("baustein_name"),
                "baustein_scope": extra.get("baustein_scope"),
                "baustein_status": extra.get("baustein_status"),
                "source_url": extra.get("source_url"),
            }
            rows.append(row)

        try:
            db.insert_chunks(rows)
            total_chunks += len(rows)
            indexed.append(raw_path)
        except Exception as e:
            errors.append({"path": raw_path, "error": f"insert failed: {e}"})

    # Refresh FTS index after bulk insert (LanceDB FTS is not auto-updated).
    if indexed:
        db.ensure_fts_index()

    return IngestPathsOutput(
        indexed=indexed,
        skipped_unchanged=skipped,
        errors=errors,
        total_chunks=total_chunks,
    )


def ingest_project_inputs(input: IngestProjectInputsInput) -> IngestProjectInputsOutput:
    """Project-namespaced ingestion. Wraps ingest_paths with project metadata."""
    out = ingest_paths(IngestPathsInput(
        paths=input.paths,
        source_type="corpus",
        force=False,
        extra_metadata={
            "project": input.project,
            "artifact_kind": "input",
        },
    ))
    return IngestProjectInputsOutput(
        project=input.project,
        indexed=out.indexed,
        total_chunks=out.total_chunks,
        errors=out.errors,
    )


def search_inputs(input: SearchInputsInput) -> SearchInputsOutput:
    """Search a single project's namespaced input documents."""
    out = search_corpus(SearchCorpusInput(
        query=input.query,
        k=input.k,
        filter={"project": input.project, "artifact_kind": "input"},
        rerank=input.rerank,
    ))
    return SearchInputsOutput(
        hits=out.hits,
        project=input.project,
        k_returned=out.k_returned,
    )


def _read_file(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        # PDFs are read by their chunker (chunk_pdf_window uses pymupdf4llm)
        return ""  # chunker reads from path directly
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="latin-1")


def _infer_source_subtype(path: str, source_type: str) -> str:
    """Classify a source path by which root + sub-area it falls under.

    Roots come from office-config; classification is by path containment
    rather than substring matching, so it works on any office layout.
    """
    p_resolved = Path(path).resolve()
    p_lower = path.lower()
    if source_type == "corpus":
        local_repos = config.local_repos_root()
        projects = config.projects_root()
        if local_repos and _is_relative_to(p_resolved, local_repos.resolve()):
            return "local-repo"
        if projects and _is_relative_to(p_resolved, projects.resolve()):
            if "/_ai/snapshots/" in p_lower:
                return "snapshot"
            if "/correspondence/" in p_lower or "schriftverkehr" in p_lower:
                return "correspondence"
            return "project-folder"
        return "external"
    if source_type == "reference":
        if "/gesetze/bund/" in p_lower:
            return "gesetz-bund"
        if "/gesetze/eu/" in p_lower:
            return "gesetz-eu"
        if "/gesetze/" in p_lower:
            return "gesetz-state"
        if "/leitfaeden/" in p_lower:
            return "leitfaden"
        if "/urteile/" in p_lower:
            return "urteil"
        if "/beispiele/" in p_lower:
            return "beispiel"
        return "reference"
    if source_type == "baustein":
        if "/bausteine/universal/" in p_lower:
            return "universal"
        if "/bausteine/domain/" in p_lower:
            return "domain"
        if "/bausteine/state/" in p_lower:
            return "state"
        if "/bausteine/projects/" in p_lower or "/_ai/bausteine/" in p_lower or "/.ai/bausteine/" in p_lower:
            return "project"
        return "baustein"
    return source_type


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False
