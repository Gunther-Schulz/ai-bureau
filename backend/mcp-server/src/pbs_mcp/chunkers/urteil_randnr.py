"""Chunk a court ruling per Randnummer.

Cut points: each `Rn. N` marker. Leitsatz / Tenor / Tatbestand /
Entscheidungsgründe sections at the start each become their own chunks.

Falls back to per-section chunking when no Randnummern found.
"""
from __future__ import annotations

import re

RANDNR_RE = re.compile(r"^Rn\.?\s*(\d+)\s*$|\b(\d+)\b\s*$", re.MULTILINE)
LEITSATZ_RE = re.compile(r"(?im)^(Leitsatz|Leitsätze|Tenor|Sachverhalt|Tatbestand|Entscheidungsgründe|Gründe)\s*[:.]?\s*$")


def chunk_urteil_randnr(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    if not content.strip():
        return []

    docket = manifest_entry.get("docket", "") if manifest_entry else ""

    # First, split by major sections (Leitsatz / Tenor / etc.)
    sections = LEITSATZ_RE.split(content)
    chunks: list[dict] = []
    current_section: str | None = None

    for piece in sections:
        if not piece.strip():
            continue
        if LEITSATZ_RE.fullmatch(piece.strip()):
            current_section = piece.strip()
            continue

        # Within a section, try to find Rn. markers
        rn_matches = list(re.finditer(r"(?m)^Rn\.?\s*(\d+)\s*$", piece))
        if rn_matches:
            for i, m in enumerate(rn_matches):
                start = m.start()
                end = rn_matches[i + 1].start() if i + 1 < len(rn_matches) else len(piece)
                block = piece[start:end].strip()
                rn = m.group(1)
                chunks.append({
                    "content": block,
                    "section": current_section or "Entscheidungsgründe",
                    "paragraph": f"Rn. {rn}",
                    "paragraph_label": f"{docket}-Rn-{rn}" if docket else f"Rn-{rn}",
                    "tags": [],
                })
        else:
            chunks.append({
                "content": piece.strip(),
                "section": current_section or "(unstructured)",
                "tags": [],
            })

    if not chunks:
        return [{
            "content": content.strip(),
            "section": "(full text)",
            "tags": [],
        }]

    for i, ch in enumerate(chunks):
        ch["chunk_index"] = i
        ch["chunk_total"] = len(chunks)
    return chunks
