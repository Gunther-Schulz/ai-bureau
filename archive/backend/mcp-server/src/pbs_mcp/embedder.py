"""Embedder + reranker.

Wraps sentence-transformers with bge-m3 (dense embeddings) and
bge-reranker-v2-m3 (cross-encoder reranker). Models load lazily on
first use; CUDA detected at load time, falls back to CPU.

bge-m3 produces dense embeddings of dim 1024. We use only dense in
v1 (sparse + ColBERT vectors deferred per chunking-strategy.md).

Usage:
    from pbs_mcp.embedder import get_embedder, get_reranker
    e = get_embedder()
    vec = e.encode_one("Was sagt §44 BNatSchG?")
    vecs = e.encode_batch(["text 1", "text 2"])
    r = get_reranker()
    scores = r.score("query", ["doc 1", "doc 2", "doc 3"])
"""
from __future__ import annotations

import logging
import threading
from functools import lru_cache

import torch

logger = logging.getLogger(__name__)

EMBEDDER_MODEL = "BAAI/bge-m3"
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
EMBEDDING_DIM = 1024


def _select_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class Embedder:
    """Singleton dense-embedding wrapper around sentence-transformers."""

    _instance: "Embedder | None" = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer

        device = _select_device()
        logger.info(f"Loading embedder {EMBEDDER_MODEL} on {device}")
        self.model = SentenceTransformer(EMBEDDER_MODEL, device=device)
        self.device = device

    @classmethod
    def get(cls) -> "Embedder":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def encode_one(self, text: str) -> list[float]:
        vec = self.model.encode(text, normalize_embeddings=True, convert_to_numpy=True)
        return vec.tolist()

    def encode_batch(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        if not texts:
            return []
        vecs = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 100,
        )
        return vecs.tolist()


class Reranker:
    """Cross-encoder reranker for top-k post-retrieval reordering."""

    _instance: "Reranker | None" = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        from sentence_transformers import CrossEncoder

        device = _select_device()
        logger.info(f"Loading reranker {RERANKER_MODEL} on {device}")
        self.model = CrossEncoder(RERANKER_MODEL, device=device)
        self.device = device

    @classmethod
    def get(cls) -> "Reranker":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def score(self, query: str, documents: list[str], batch_size: int = 32) -> list[float]:
        if not documents:
            return []
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs, batch_size=batch_size, show_progress_bar=False)
        return scores.tolist() if hasattr(scores, "tolist") else list(scores)


def get_embedder() -> Embedder:
    return Embedder.get()


def get_reranker() -> Reranker:
    return Reranker.get()


@lru_cache(maxsize=1)
def device_info() -> dict[str, str | bool]:
    """For diagnostics: which device the embedder uses."""
    return {
        "device": _select_device(),
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_name": (
            torch.cuda.get_device_name(0) if torch.cuda.is_available() else ""
        ),
        "embedding_dim": EMBEDDING_DIM,
        "embedder_model": EMBEDDER_MODEL,
        "reranker_model": RERANKER_MODEL,
    }
