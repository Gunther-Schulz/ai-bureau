"""Runtime path resolution.

App-internal paths (repo root, lancedb data dir) are resolved here.
Office-specific paths (state_root, references_root, projects_root,
local_repos_root) are read from `office_config`.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pbs_mcp import office_config


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


def federal_references_manifest() -> Path:
    """Path to the app's federal-core manifest (universal German law)."""
    return repo_root() / "references-manifest.yaml"


def office_extensions_manifest_for(bundesland: str) -> Path | None:
    """Path to the office's state-specific extension manifest, if any.

    Resolution: explicit `extensions.references_manifests.<bundesland>`
    in office-config wins; else conventional default at
    `<state_root>/extensions/<bundesland>/references-manifest.yaml`.
    """
    cfg = office_config.load()
    return cfg.references_manifest_for_state(bundesland)


def projects_root() -> Path:
    return office_config.load().paths.projects_root


def references_root() -> Path:
    return office_config.load().paths.references_root


def office_state_root() -> Path:
    return office_config.load().paths.state_root


def local_repos_root() -> Path | None:
    return office_config.load().paths.local_repos_root


def app_templates_root() -> Path:
    """Where the app ships LaTeX classes + skeletons."""
    return repo_root() / "plugin" / "templates"


def app_classes_dir() -> Path:
    return app_templates_root() / "classes"


def app_skeletons_dir() -> Path:
    return app_templates_root() / "skeletons"


def lancedb_path() -> Path:
    if env := os.getenv("PBS_LANCEDB_PATH"):
        return Path(env).resolve()
    return repo_root() / "backend" / "data" / "lancedb"
