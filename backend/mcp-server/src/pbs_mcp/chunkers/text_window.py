"""Generic sliding-window chunker. Fallback when no specific chunker matches.

Per chunking-strategy.md: 1024-token windows, no overlap (overlap is
harmful for structured cuts; for arbitrary cuts we accept some context loss).

Approximation: tokenize by whitespace, count words, treat ~750 words ≈
1024 tokens (German prose runs ~1.3 tokens/word). For accurate token
counting, would use the bge-m3 tokenizer — deferred until needed.
"""
from __future__ import annotations

WORDS_PER_CHUNK = 750
WORDS_MIN = 40
OVERLAP_WORDS = 0


def chunk_text_window(path: str, content: str, manifest_entry: dict | None = None) -> list[dict]:
    if not content or not content.strip():
        return []

    words = content.split()
    if len(words) < WORDS_MIN:
        return [{
            "content": content.strip(),
            "section": None,
            "chunk_index": 0,
            "chunk_total": 1,
            "tags": [],
        }]

    chunks = []
    step = WORDS_PER_CHUNK - OVERLAP_WORDS
    total = max(1, (len(words) + step - 1) // step)
    for idx, start in enumerate(range(0, len(words), step)):
        window = words[start:start + WORDS_PER_CHUNK]
        if len(window) < WORDS_MIN and chunks:
            chunks[-1]["content"] += " " + " ".join(window)
            continue
        chunks.append({
            "content": " ".join(window),
            "section": None,
            "chunk_index": idx,
            "chunk_total": total,
            "tags": [],
        })

    for i, ch in enumerate(chunks):
        ch["chunk_index"] = i
        ch["chunk_total"] = len(chunks)
    return chunks
