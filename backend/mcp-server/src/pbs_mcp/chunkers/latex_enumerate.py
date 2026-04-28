"""Chunk a Festsetzungen-style numbered-rule LaTeX file.

Cut points: each top-level `\\item` of the outer enumerate. Each chunk
includes the rule's text + nested sub-items.

Detects the master enumerate by finding the first `\\begin{enumerate}`
at depth 0. Verfahrensvermerke section is chunked separately per Vermerk.
"""
from __future__ import annotations

import re

ITEM_RE = re.compile(r"\\item\b")


def chunk_latex_enumerate(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    if not content.strip():
        return []

    chunks: list[dict] = []

    # Find the section between \section*{Teil B Text} and \section*{Verfahrensvermerke}
    teil_b_m = re.search(r"\\section\*\{Teil B Text\}", content)
    vv_m = re.search(r"\\section\*\{Verfahrensvermerke\}", content)
    rg_m = re.search(r"\\section\*\{Rechtsgrundlagen\}", content)

    if teil_b_m and vv_m:
        teil_b_text = content[teil_b_m.end():vv_m.start()]
        chunks.extend(_chunk_enumerate_block(teil_b_text, section_prefix="Teil B Text"))

    if vv_m:
        end = rg_m.start() if rg_m else len(content)
        vv_text = content[vv_m.start():end]
        chunks.extend(_chunk_enumerate_block(vv_text, section_prefix="Verfahrensvermerke"))

    if rg_m:
        rg_text = content[rg_m.start():]
        chunks.append({
            "content": rg_text.strip(),
            "section": "Rechtsgrundlagen",
            "tags": [],
        })

    if not chunks:
        # Fallback: one big chunk
        chunks.append({
            "content": content.strip(),
            "section": "(full document)",
            "tags": [],
        })

    for i, ch in enumerate(chunks):
        ch["chunk_index"] = i
        ch["chunk_total"] = len(chunks)
    return chunks


def _chunk_enumerate_block(text: str, section_prefix: str) -> list[dict]:
    """Split a numbered-rule block into one chunk per top-level \\item."""
    # Find positions of top-level \item (depth tracking is tricky in
    # nested enumerates; we approximate by splitting at \item that
    # follows an outer \begin{enumerate} or another top-level \item)
    items = re.split(r"(?m)^\s*\\item\b", text)
    if len(items) < 2:
        return [{
            "content": text.strip(),
            "section": section_prefix,
            "tags": [],
        }]

    chunks = []
    for i, item in enumerate(items[1:], start=1):
        item = item.strip()
        if not item:
            continue
        # Pull a short label from the first line
        first_line = item.split("\n", 1)[0].strip()
        label = re.sub(r"\\(textbf|emph|textit)\{([^}]*)\}", r"\2", first_line)[:80]
        chunks.append({
            "content": "\\item " + item,
            "section": f"{section_prefix} #{i}",
            "section_number": str(i),
            "tags": [],
        })
    return chunks
