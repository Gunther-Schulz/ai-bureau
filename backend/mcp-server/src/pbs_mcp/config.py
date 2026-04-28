"""Runtime path resolution.

App-internal paths (repo root, lancedb data dir, app-shipped extensions)
are resolved here. Office-specific paths (state_root, references_root,
projects_root, local_repos_root) and selected manifests come from
`office_config`.
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


# === App-shipped extensions (universal/domain/state templates) ===========

def app_extensions_dir() -> Path:
    """Where the app ships layered manifests + skeleton overlays."""
    return repo_root() / "extensions"


def app_universal_references_manifest() -> Path:
    """The app-shipped universal references manifest (every bureau)."""
    return app_extensions_dir() / "universal" / "references-manifest.yaml"


def app_universal_doctypes_manifest() -> Path:
    """The app-shipped universal doctypes manifest (every bureau)."""
    return app_extensions_dir() / "universal" / "doctypes.yaml"


def app_domain_references_manifest(domain: str) -> Path:
    """App-shipped per-domain references manifest path."""
    return app_extensions_dir() / "domain" / domain / "references-manifest.yaml"


def app_domain_doctypes_manifest(domain: str) -> Path:
    """App-shipped per-domain doctypes manifest path."""
    return app_extensions_dir() / "domain" / domain / "doctypes.yaml"


def app_state_references_manifest(state: str) -> Path:
    """App-shipped per-state references manifest path."""
    return app_extensions_dir() / "state" / state / "references-manifest.yaml"


def app_state_doctypes_manifest(state: str) -> Path:
    """App-shipped per-state doctypes manifest path."""
    return app_extensions_dir() / "state" / state / "doctypes.yaml"


# === Manifest resolution (delegates to office_config) ====================

def all_references_manifests() -> list[Path]:
    """All reference manifests selected by this office's scope."""
    return office_config.load().all_references_manifests()


def all_doctypes_manifests() -> list[Path]:
    """All doctype manifests selected by this office's scope."""
    return office_config.load().all_doctypes_manifests()


# === Office-config-derived paths =========================================

def projects_root() -> Path:
    return office_config.load().paths.projects_root


def references_root() -> Path:
    return office_config.load().paths.references_root


def office_state_root() -> Path:
    return office_config.load().paths.state_root


def local_repos_root() -> Path | None:
    return office_config.load().paths.local_repos_root


# === App-shipped templates ===============================================

def app_templates_root() -> Path:
    """Where the app ships LaTeX classes + skeletons."""
    return repo_root() / "plugin" / "templates"


def app_classes_dir() -> Path:
    return app_templates_root() / "classes"


def app_skeletons_dir() -> Path:
    """Root of the layered skeleton tree (universal/ + domain/<X>/)."""
    return app_templates_root() / "skeletons"


def app_universal_skeleton_for(doctype: str) -> Path | None:
    """Return the universal-layer skeleton dir for a doctype, if present."""
    p = app_skeletons_dir() / "universal" / doctype
    return p if p.is_dir() else None


def app_domain_skeleton_for(domain: str, doctype: str) -> Path | None:
    """Return a domain-overlay skeleton dir for a doctype, if present."""
    p = app_skeletons_dir() / "domain" / domain / doctype
    return p if p.is_dir() else None


# === LanceDB ==============================================================

def lancedb_path() -> Path:
    if env := os.getenv("PBS_LANCEDB_PATH"):
        return Path(env).resolve()
    return repo_root() / "backend" / "data" / "lancedb"
