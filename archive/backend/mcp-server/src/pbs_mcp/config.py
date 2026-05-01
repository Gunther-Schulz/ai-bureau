"""Runtime path resolution.

App-internal paths (repo root, lancedb data dir, app-shipped extensions)
are resolved here. Office-specific paths come from `office_config.roots`.

Manifest discovery (v3+): the loader no longer stores manifest paths in
office-config. Instead, `all_references_manifests()` and
`all_doctypes_manifests()` walk `<repo>/extensions/` (and optionally the
office's `roots.office_extensions/` tree) filtered by the office's scope.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

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


# === Manifest discovery (v3 — walk extensions tree filtered by scope) ====

ManifestKind = Literal["references", "doctypes"]


def _filename_for(kind: ManifestKind) -> str:
    return "references-manifest.yaml" if kind == "references" else "doctypes.yaml"


def _walk_extensions_tree(
    root: Path, kind: ManifestKind, scope: office_config.Scope
) -> list[tuple[Path, str, str | None]]:
    """Return (path, layer, scope_key) triples for manifests in `root` matching scope.

    Layers walked: universal, then per-domain (in scope.domains order),
    then per-state (in scope.states order). Files that don't exist are
    silently skipped — non-existence in a given layer is normal (e.g.
    the universal layer doesn't ship every doctype).
    """
    filename = _filename_for(kind)
    out: list[tuple[Path, str, str | None]] = []

    universal = root / "universal" / filename
    if universal.is_file():
        out.append((universal, "universal", None))

    for domain in scope.domains:
        p = root / "domain" / domain / filename
        if p.is_file():
            out.append((p, "domain", domain))

    for state in scope.states:
        p = root / "state" / state / filename
        if p.is_file():
            out.append((p, "state", state))

    return out


def _all_manifests(kind: ManifestKind) -> list[tuple[Path, str, str | None]]:
    """All manifests of given kind selected by this office's scope.

    Walks `<repo>/extensions/` first (canonical app-shipped manifests),
    then `<roots.office_extensions>/` if set (office-local additions).
    Both trees use the same `<universal,domain/<X>,state/<X>>` layout.
    """
    cfg = office_config.load()
    out = _walk_extensions_tree(app_extensions_dir(), kind, cfg.scope)
    if cfg.roots.office_extensions is not None:
        out.extend(_walk_extensions_tree(cfg.roots.office_extensions, kind, cfg.scope))
    return out


def all_references_manifests() -> list[tuple[Path, str, str | None]]:
    """All reference manifests selected by this office's scope.

    Returns (path, layer, scope_key) triples. layer ∈ {universal, domain, state}.
    scope_key is None for universal, the domain key (e.g. 'PV-FFA') or
    state key (e.g. 'MV') otherwise. Walks app extensions tree first,
    then office_extensions if configured.
    """
    return _all_manifests("references")


def all_doctypes_manifests() -> list[tuple[Path, str, str | None]]:
    """All doctype manifests selected by this office's scope.

    Same return shape as all_references_manifests.
    """
    return _all_manifests("doctypes")


# === Office-config-derived paths =========================================

def projects_root() -> Path:
    return office_config.load().roots.projects


def references_root() -> Path:
    return office_config.load().roots.references


def office_state_root() -> Path:
    return office_config.load().roots.state


def local_repos_root() -> Path | None:
    return office_config.load().roots.local_repos


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
