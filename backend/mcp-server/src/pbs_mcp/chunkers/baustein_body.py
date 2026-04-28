"""Chunk a baustein markdown file: one chunk per body (post-frontmatter).

If body exceeds ~1000 tokens (rare), split at `##` headings. Frontmatter
NOT embedded — only body content goes into the vector.
"""
from __future__ import annotations

import re

from pbs_mcp.chunkers.text_window import WORDS_PER_CHUNK


def _strip_frontmatter(content: str) -> str:
    """Strip YAML frontmatter (lines between two `---` markers at top)."""
    if not content.startswith("---"):
        return content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    return parts[2].lstrip("\n")


def chunk_baustein_body(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    body = _strip_frontmatter(content)
    if not body.strip():
        return []

    words = body.split()
    if len(words) <= WORDS_PER_CHUNK:
        return [{
            "content": body.strip(),
            "section": "body",
            "chunk_index": 0,
            "chunk_total": 1,
            "tags": [],
        }]

    # Long body: split at top-level ## headings
    sections = re.split(r"(?m)^(##\s+.+)$", body)
    if len(sections) < 2:
        # No headings; fall back to single chunk (truncate is wrong; embedder handles long input)
        return [{
            "content": body.strip(),
            "section": "body",
            "chunk_index": 0,
            "chunk_total": 1,
            "tags": [],
        }]

    chunks = []
    current_heading: str | None = None
    current_text: list[str] = []
    if sections[0].strip():
        current_text.append(sections[0])

    for piece in sections[1:]:
        if piece.startswith("##"):
            if current_text:
                chunks.append({
                    "content": "\n".join(current_text).strip(),
                    "section": current_heading or "body",
                    "tags": [],
                })
            current_heading = piece.strip().lstrip("#").strip()
            current_text = [piece]
        else:
            current_text.append(piece)
    if current_text:
        chunks.append({
            "content": "\n".join(current_text).strip(),
            "section": current_heading or "body",
            "tags": [],
        })

    for i, ch in enumerate(chunks):
        ch["chunk_index"] = i
        ch["chunk_total"] = len(chunks)
    return chunks
