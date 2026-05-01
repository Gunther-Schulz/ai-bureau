"""Chunk a Gesetz text per § paragraph.

Cut points: at each `§ N <Title>` header. Each chunk = full §, including
title and all Absätze (1), (2), ...

Skips repealed paragraphs ("§N — weggefallen") and heading-only sections.
"""
from __future__ import annotations

import re

# Pattern matches lines like "§ 44 Tötungsverbot" or "§ 45a Verstöße"
PARAGRAPH_RE = re.compile(r"^§\s*(\d+[a-z]?)\s+(.+?)$", re.MULTILINE)


def chunk_gesetz_paragraph(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    if not content.strip():
        return []

    chunks = []
    matches = list(PARAGRAPH_RE.finditer(content))
    if not matches:
        # No § structure — fall back to single chunk
        return [{
            "content": content.strip(),
            "section": "(no § structure)",
            "tags": [],
        }]

    law_id = manifest_entry.get("id", "") if manifest_entry else ""

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[start:end].strip()

        # Skip repealed paragraphs
        if "weggefallen" in block.lower() and len(block.split()) < 20:
            chunks.append({
                "content": block,
                "section": m.group(2).strip(),
                "paragraph": f"§ {m.group(1)}",
                "paragraph_label": f"{law_id}-§{m.group(1)}" if law_id else f"§{m.group(1)}",
                "tags": ["weggefallen"],
                "chunk_index": i,
            })
            continue

        title = m.group(2).strip()
        chunks.append({
            "content": block,
            "section": title,
            "paragraph": f"§ {m.group(1)}",
            "paragraph_label": f"{law_id}-§{m.group(1)}" if law_id else f"§{m.group(1)}",
            "tags": [],
            "chunk_index": i,
        })

    for i, ch in enumerate(chunks):
        ch["chunk_index"] = i
        ch["chunk_total"] = len(chunks)
    return chunks
