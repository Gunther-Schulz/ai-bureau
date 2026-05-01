"""Chunk a PDF via PDF→markdown extraction + sliding-window fallback.

Uses pymupdf4llm (PyMuPDF) for text extraction. Per chunking-strategy.md
generic PDFs use 1024-token windows with 128-token overlap.

For leitfäden with detectable `##` headings, we could specialize via
chunk_pdf_heading; for v0.1 we use text_window after extraction.
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def chunk_pdf_window(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    """Note: `content` is ignored; we extract from `path` directly via PyMuPDF.

    The signature matches other chunkers but PDFs need binary read.
    """
    try:
        import pymupdf4llm
        md = pymupdf4llm.to_markdown(path)
    except ImportError:
        logger.warning("pymupdf4llm not installed; skipping PDF")
        return []
    except Exception as e:
        logger.warning(f"Failed to extract PDF {path}: {e}")
        return []

    if not md.strip():
        return []

    # For v0.1, treat extracted markdown as text and apply sliding window.
    # v0.2: detect ## headings and use per-section chunking (chunk_pdf_heading).
    from pbs_mcp.chunkers.text_window import chunk_text_window
    chunks = chunk_text_window(path, md, manifest_entry)

    for ch in chunks:
        ch.setdefault("tags", []).append("pdf-extracted")
    return chunks
