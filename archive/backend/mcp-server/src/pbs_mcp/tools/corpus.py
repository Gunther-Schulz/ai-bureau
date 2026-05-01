"""Corpus tools — search_corpus, read_corpus_file."""
from __future__ import annotations

import logging
from pathlib import Path

from pbs_mcp.db import get_db
from pbs_mcp.schemas import (
    ReadCorpusFileInput,
    ReadCorpusFileOutput,
    SearchCorpusInput,
    SearchCorpusOutput,
)

logger = logging.getLogger(__name__)


def search_corpus(input: SearchCorpusInput) -> SearchCorpusOutput:
    db = get_db()
    hits = db.search(
        query=input.query,
        k=input.k,
        filter=input.filter,
        rerank=input.rerank,
        hybrid=True,
    )
    return SearchCorpusOutput(
        hits=hits,
        query=input.query,
        k_returned=len(hits),
        used_reranker=input.rerank,
    )


def read_corpus_file(input: ReadCorpusFileInput) -> ReadCorpusFileOutput:
    p = Path(input.path)
    if not p.is_file():
        raise FileNotFoundError(f"file not found: {input.path}")

    if p.suffix.lower() == ".pdf":
        try:
            import pymupdf4llm
            content = pymupdf4llm.to_markdown(str(p))
        except ImportError:
            content = "(PDF — pymupdf4llm not installed; cannot extract)"
        except Exception as e:
            content = f"(PDF extraction failed: {e})"
    else:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="latin-1")

    truncated = False
    if input.offset is not None or input.limit is not None:
        offset = input.offset or 0
        limit = input.limit or len(content)
        if offset > 0 or limit < len(content):
            truncated = True
        content = content[offset:offset + limit]

    return ReadCorpusFileOutput(
        path=str(p),
        content=content,
        truncated=truncated,
    )
