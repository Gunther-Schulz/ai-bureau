"""Discovery tools — enumerate scope-aware system resources.

Tier 1 of the MCP discovery layer (per ROADMAP "Backend MCP discovery
layer"). Wraps the layered manifest API + skill discovery + skeleton
lookup as MCP tools so skills can call them deterministically rather
than falling back to filesystem Glob.

Per ARCHITECTURE.md meta-rule 5 (execution locality) + Backend
organization: these handlers are thin wrappers around plain-Python
functions in office_config / config; the logic lives there.
"""
from __future__ import annotations

import logging
from pathlib import Path

import yaml

from pbs_mcp import config, office_config
from pbs_mcp.schemas import (
    ListDoctypesManifestsInput,
    ListDoctypesManifestsOutput,
    ListReferenceManifestsInput,
    ListReferenceManifestsOutput,
    ListSkeletonsInput,
    ListSkeletonsOutput,
    ListSkillsInput,
    ListSkillsOutput,
    ManifestInfo,
    SkeletonInfo,
    SkillInfo,
)

logger = logging.getLogger(__name__)


# === Reference / Doctype manifests =========================================

def _count_entries(categories: dict) -> int:
    """Count entries in a references-manifest categories block."""
    total = 0
    for v in categories.values():
        if isinstance(v, list):
            total += len(v)
        elif isinstance(v, dict):
            for inner in v.values():
                if isinstance(inner, list):
                    total += len(inner)
    return total


def _manifest_info(path: Path, layer: str, scope_key: str | None) -> ManifestInfo:
    """Build a ManifestInfo from a path; populate entry_count + last_updated."""
    exists = path.is_file()
    entry_count: int | None = None
    last_updated: str | None = None
    if exists:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                lu = data.get("last_updated")
                last_updated = str(lu) if lu else None
                cats = data.get("categories")
                if isinstance(cats, dict):
                    entry_count = _count_entries(cats)
                doctypes = data.get("doctypes")
                if isinstance(doctypes, dict) and entry_count is None:
                    entry_count = len(doctypes)
        except Exception as e:
            logger.warning(f"failed to parse manifest at {path}: {e}")
    return ManifestInfo(
        path=str(path),
        layer=layer,  # type: ignore[arg-type]
        scope_key=scope_key,
        exists=exists,
        entry_count=entry_count,
        last_updated=last_updated,
    )


def _enumerate_manifests_full_union(kind: str) -> list[tuple[Path, str, str | None]]:
    """Return (path, layer, scope_key) for ALL manifests in the app extensions
    tree (and office_extensions if set), regardless of scope.

    Used when scope_filter=false — caller wants the full union, not the
    scope-filtered subset.
    """
    from pbs_mcp.office_config import Scope, StateCode

    # Synthesize a scope that covers every directory under domain/ and state/.
    cfg = office_config.load()
    app = config.app_extensions_dir()
    full_domains: list[str] = []
    if (app / "domain").is_dir():
        full_domains = sorted(p.name for p in (app / "domain").iterdir() if p.is_dir())
    full_states: list[str] = []
    if (app / "state").is_dir():
        full_states = [p.name for p in sorted((app / "state").iterdir()) if p.is_dir()]
    full_scope = Scope(
        domains=full_domains,
        states=[s for s in full_states if s in (
            "BB", "BW", "BY", "BE", "HB", "HH", "HE", "MV",
            "NI", "NW", "RP", "SH", "SL", "SN", "ST", "TH",
        )],
    )

    out = config._walk_extensions_tree(app, kind, full_scope)
    if cfg.roots.office_extensions is not None:
        out.extend(config._walk_extensions_tree(cfg.roots.office_extensions, kind, full_scope))
    return out


def list_reference_manifests(input: ListReferenceManifestsInput) -> ListReferenceManifestsOutput:
    if input.scope_filter:
        items = config.all_references_manifests()
    else:
        items = _enumerate_manifests_full_union("references")
    manifests = [_manifest_info(p, layer, key) for p, layer, key in items]
    return ListReferenceManifestsOutput(
        manifests=manifests,
        total=len(manifests),
        scope_filtered=input.scope_filter,
    )


def list_doctypes_manifests(input: ListDoctypesManifestsInput) -> ListDoctypesManifestsOutput:
    if input.scope_filter:
        items = config.all_doctypes_manifests()
    else:
        items = _enumerate_manifests_full_union("doctypes")
    manifests = [_manifest_info(p, layer, key) for p, layer, key in items]
    return ListDoctypesManifestsOutput(
        manifests=manifests,
        total=len(manifests),
        scope_filtered=input.scope_filter,
    )


# === Skills ===============================================================

def _parse_skill_frontmatter(path: Path) -> dict | None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        logger.warning(f"failed to parse skill frontmatter at {path}: {e}")
        return None


def list_skills(input: ListSkillsInput) -> ListSkillsOutput:
    skills_dir = config.repo_root() / "plugin" / "skills"
    skills: list[SkillInfo] = []
    if not skills_dir.is_dir():
        return ListSkillsOutput(skills=[], total=0)
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm = _parse_skill_frontmatter(skill_md)
        if not fm:
            continue
        version = fm.get("version")
        skills.append(SkillInfo(
            name=fm.get("name") or skill_dir.name,
            version=str(version) if version is not None else None,
            description=fm.get("description") or "",
            path=str(skill_md),
            mcp_tools_required=list(fm.get("mcp_tools_required") or []),
            mcp_tools_optional=list(fm.get("mcp_tools_optional") or []),
            fallback_when_mcp_absent=fm.get("fallback_when_mcp_absent"),
        ))
    return ListSkillsOutput(skills=skills, total=len(skills))


# === Skeletons ============================================================

def list_skeletons(input: ListSkeletonsInput) -> ListSkeletonsOutput:
    """Return layered skeleton dirs for a doctype: universal + per-domain overlays."""
    cfg = office_config.load()
    skeletons: list[SkeletonInfo] = []

    universal_skel = config.app_universal_skeleton_for(input.doctype)
    if universal_skel is not None:
        skeletons.append(SkeletonInfo(
            layer="universal",
            scope_key=None,
            path=str(universal_skel),
        ))

    for domain in cfg.scope.domains:
        domain_skel = config.app_domain_skeleton_for(domain, input.doctype)
        if domain_skel is not None:
            skeletons.append(SkeletonInfo(
                layer="domain",
                scope_key=domain,
                path=str(domain_skel),
            ))

    return ListSkeletonsOutput(
        doctype=input.doctype,
        skeletons=skeletons,
        total=len(skeletons),
    )
