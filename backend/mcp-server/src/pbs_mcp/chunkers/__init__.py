"""Chunker registry — dispatches paths to per-source-type chunkers.

Strategy spec: backend/mcp-server/docs/chunking-strategy.md.

Each chunker is a callable: (path: str, content: str, manifest_entry:
dict | None) -> list[Chunk]. A `Chunk` is a dict with: content, plus
metadata fields populated for the source type (section, paragraph,
project, doctype, etc.).
"""
from __future__ import annotations

from typing import Callable, TypedDict

from pbs_mcp.chunkers.baustein_body import chunk_baustein_body
from pbs_mcp.chunkers.eml import chunk_eml
from pbs_mcp.chunkers.gesetz_paragraph import chunk_gesetz_paragraph
from pbs_mcp.chunkers.latex_enumerate import chunk_latex_enumerate
from pbs_mcp.chunkers.latex_kapitel import chunk_latex_kapitel
from pbs_mcp.chunkers.latex_textbaustein import chunk_latex_textbaustein
from pbs_mcp.chunkers.pdf_window import chunk_pdf_window
from pbs_mcp.chunkers.text_window import chunk_text_window
from pbs_mcp.chunkers.urteil_randnr import chunk_urteil_randnr


class Chunk(TypedDict, total=False):
    content: str
    section: str | None
    section_number: str | None
    paragraph: str | None
    paragraph_label: str | None
    chunk_index: int
    chunk_total: int
    tags: list[str]


Chunker = Callable[[str, str, dict | None], list[Chunk]]

CHUNKERS: dict[str, Chunker] = {
    "per-paragraph": chunk_gesetz_paragraph,
    "per-randnummer": chunk_urteil_randnr,
    "per-section": chunk_text_window,  # PDFs use text_window after PDF→text in v0.1; pdf_heading later
    "per-baustein": chunk_latex_textbaustein,
    "per-rule": chunk_latex_enumerate,
    "per-kapitel": chunk_latex_kapitel,
    "per-message": chunk_eml,
    "pdf-window": chunk_pdf_window,
    "text-window": chunk_text_window,
    "baustein-body": chunk_baustein_body,
}


def select_chunker(path: str, manifest_entry: dict | None = None) -> Chunker:
    """Path-based chunker dispatch with manifest override."""
    if manifest_entry and "chunking_strategy" in manifest_entry:
        strategy = manifest_entry["chunking_strategy"]
        if strategy in CHUNKERS:
            return CHUNKERS[strategy]

    p = path.lower()
    if "_ai-references/gesetze/" in p:
        return chunk_gesetz_paragraph
    if "_ai-references/urteile/" in p:
        return chunk_urteil_randnr
    if "_ai-references/leitfaeden/" in p and p.endswith(".pdf"):
        return chunk_pdf_window
    if "/textbausteine/" in p and p.endswith(".tex"):
        return chunk_latex_textbaustein
    if p.endswith("textteil-b-b-plan.tex") or "/festsetzungen/" in p:
        return chunk_latex_enumerate
    if "/kapitel_ub/" in p or "/umweltbericht/kapitel/" in p:
        return chunk_latex_kapitel
    if "/schriftverkehr/eml/" in p or p.endswith(".eml"):
        return chunk_eml
    if ("/bausteine/" in p or "/memory/" in p) and p.endswith(".md"):
        return chunk_baustein_body
    if p.endswith(".pdf"):
        return chunk_pdf_window
    return chunk_text_window
