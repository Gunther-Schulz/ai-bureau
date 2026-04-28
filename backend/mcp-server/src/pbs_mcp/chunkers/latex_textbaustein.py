"""Chunk a Begründung Textbaustein file. One chunk per file.

Pre-strips trivial LaTeX commands that aren't semantic content. Keeps
structural markers (\\section, \\textbf, \\glqq, \\cite).
"""
from __future__ import annotations

import re
from pathlib import Path

from pbs_mcp.chunkers.text_window import WORDS_PER_CHUNK


def _strip_latex(text: str) -> str:
    # Strip common comment lines
    text = re.sub(r"(?m)^%.*$", "", text)
    # Drop \input{...} (those become their own chunks)
    text = re.sub(r"\\input\{[^}]*\}", "", text)
    return text


def chunk_latex_textbaustein(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    cleaned = _strip_latex(content).strip()
    if not cleaned:
        return []

    section_name = Path(path).stem  # filename without extension as section name

    words = cleaned.split()
    if len(words) <= WORDS_PER_CHUNK:
        return [{
            "content": cleaned,
            "section": section_name,
            "chunk_index": 0,
            "chunk_total": 1,
            "tags": [],
        }]

    # Long Textbaustein — split at \section{} or paragraph break
    parts = re.split(r"(?m)(?=^\\section\{)|\n\n+", cleaned)
    parts = [p.strip() for p in parts if p.strip()]
    chunks = []
    for i, p in enumerate(parts):
        if len(p.split()) < 30 and chunks:
            chunks[-1]["content"] += "\n\n" + p
        else:
            chunks.append({
                "content": p,
                "section": section_name,
                "tags": [],
            })

    for i, ch in enumerate(chunks):
        ch["chunk_index"] = i
        ch["chunk_total"] = len(chunks)
    return chunks
