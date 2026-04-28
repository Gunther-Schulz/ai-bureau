"""Runtime configuration: paths to repo, references, hidrive projects.

Resolves the pbs-bureau repo root by walking upward from this module
until `.claude-plugin/marketplace.json` is found. All other paths are
derived from that root or from environment variables.

Environment overrides (used in tests + custom deployments):
- PBS_REPO_ROOT:       path to pbs-bureau repo (overrides auto-detect)
- PBS_HIDRIVE_PROJEKTE: path to hidrive Projekte/ folder
- PBS_LOCAL_REPOS:     path to ~/dev/Planungsbüro-Schulz/
- PBS_LANCEDB_PATH:    path to LanceDB data dir
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def repo_root() -> Path:
    """Locate the pbs-bureau repository root."""
    if env := os.getenv("PBS_REPO_ROOT"):
        return Path(env).resolve()

    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".claude-plugin" / "marketplace.json").is_file():
            return parent

    raise RuntimeError(
        "Could not locate pbs-bureau repo root. Set PBS_REPO_ROOT to override."
    )


def memory_dir() -> Path:
    return repo_root() / "memory"


def references_manifest() -> Path:
    return repo_root() / "references-manifest.yaml"


def hidrive_projekte() -> Path:
    if env := os.getenv("PBS_HIDRIVE_PROJEKTE"):
        return Path(env).resolve()
    return Path("/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte")


def hidrive_ai_references() -> Path:
    return hidrive_projekte() / "_ai-references"


def hidrive_ai_office_state() -> Path:
    return hidrive_projekte() / "_ai-office-state"


def local_planungsbuero_repos() -> Path:
    if env := os.getenv("PBS_LOCAL_REPOS"):
        return Path(env).resolve()
    return Path.home() / "dev" / "Planungsbüro-Schulz"


def lancedb_path() -> Path:
    if env := os.getenv("PBS_LANCEDB_PATH"):
        return Path(env).resolve()
    return repo_root() / "backend" / "data" / "lancedb"
