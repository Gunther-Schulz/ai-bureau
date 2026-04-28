"""Chunk an Umweltbericht Kapitel module file. One chunk per file.

Each Schutzgut_<X>_UB.tex or Schutzgut_<X>_Mas_UB.tex becomes one chunk.
"""
from __future__ import annotations

from pathlib import Path

from pbs_mcp.chunkers.latex_textbaustein import _strip_latex
from pbs_mcp.chunkers.text_window import WORDS_PER_CHUNK


def chunk_latex_kapitel(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    cleaned = _strip_latex(content).strip()
    if not cleaned:
        return []

    fname = Path(path).stem

    section_name = fname.replace("_", " ")
    is_mas = "_Mas_" in fname or fname.endswith("_Mas_UB")
    suffix = " — Maßnahmen" if is_mas else " — Bestandsaufnahme" if "_UB" in fname else ""

    words = cleaned.split()
    if len(words) <= WORDS_PER_CHUNK:
        return [{
            "content": cleaned,
            "section": f"{section_name}{suffix}",
            "chunk_index": 0,
            "chunk_total": 1,
            "tags": ["umweltbericht", "schutzgut"] + (["maßnahmen"] if is_mas else ["bestand"]),
        }]

    # Fall back to text-window for very long Schutzgut sections
    from pbs_mcp.chunkers.text_window import chunk_text_window
    chunks = chunk_text_window(path, cleaned, manifest_entry)
    for ch in chunks:
        ch["section"] = f"{section_name}{suffix}"
        ch.setdefault("tags", []).extend(["umweltbericht", "schutzgut"])
        if is_mas:
            ch["tags"].append("maßnahmen")
        else:
            ch["tags"].append("bestand")
    return chunks
