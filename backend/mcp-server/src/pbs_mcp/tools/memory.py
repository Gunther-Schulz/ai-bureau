"""Memory tools — bausteine: list, get, save, flag, archive, find-by-reference.

Bausteine are markdown files with YAML frontmatter, per
plugin/skills/save-baustein/references/format.md. Tools here parse +
manipulate them as filesystem operations. No LanceDB dependency for
v0.1 (bausteine are also indexed into LanceDB by ingest tools, but
read/write goes to filesystem directly to keep frontmatter authoritative).
"""
from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from pbs_mcp import config
from pbs_mcp.schemas import (
    ArchiveBausteinInput,
    ArchiveBausteinOutput,
    BausteinSummary,
    FindBausteineByReferenceInput,
    FindBausteineByReferenceOutput,
    FlagBausteinInput,
    FlagBausteinOutput,
    GetBausteinInput,
    GetBausteinOutput,
    ListBausteineInput,
    ListBausteineOutput,
    SaveBausteinInput,
    SaveBausteinOutput,
)

logger = logging.getLogger(__name__)


# === Frontmatter parsing ===

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Split a markdown file into (frontmatter dict, body)."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse frontmatter: {e}")
        return {}, content
    body = parts[2].lstrip("\n")
    return frontmatter, body


def compose_baustein(frontmatter: dict, body: str) -> str:
    """Compose frontmatter + body into a baustein markdown file."""
    yml = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return f"---\n{yml}---\n\n{body}"


# === Path resolution ===

def baustein_path(scope: str, name: str, domain: str | None = None,
                  project: str | None = None, project_root: str | None = None) -> Path:
    """Resolve baustein file path per scope rules."""
    if scope == "global":
        return config.memory_dir() / "global" / f"{name}.md"
    if scope == "domain":
        if not domain:
            raise ValueError("domain scope requires domain= argument")
        return config.memory_dir() / domain / f"{name}.md"
    if scope == "project":
        if project_root:
            return Path(project_root) / "_ai" / "bausteine" / f"{name}.md"
        if project:
            return config.memory_dir() / "projects" / project / f"{name}.md"
        raise ValueError("project scope requires project= or project_root= argument")
    raise ValueError(f"Unknown scope: {scope}")


def _enumerate_paths(scope: str | None, domain: str | None,
                     project: str | None) -> list[Path]:
    """Enumerate candidate baustein paths for a list query."""
    paths: list[Path] = []

    def _scan(d: Path) -> None:
        if not d.is_dir():
            return
        for p in d.rglob("*.md"):
            # Skip INDEX.md and other non-baustein meta files
            if p.name.lower() in ("index.md", "readme.md"):
                continue
            paths.append(p)

    base = config.memory_dir()
    if not base.is_dir():
        return paths

    if scope is None or scope == "global":
        _scan(base / "global")
    if scope is None or scope == "domain":
        if domain:
            _scan(base / domain)
        else:
            for d in base.iterdir():
                if d.is_dir() and d.name not in ("global", "office", "projects"):
                    # NOTE: domain folder is e.g. memory/artenschutz/, but
                    # currently memory/domain/ wraps domains. Adjust:
                    pass
            # Currently structure: memory/domain/<domain>/. Iterate.
            domain_root = base / "domain"
            if domain_root.is_dir():
                for d in domain_root.iterdir():
                    if d.is_dir():
                        _scan(d)
    if scope is None or scope == "project":
        if project:
            _scan(base / "projects" / project)

    return paths


# === Tools ===

def list_bausteine(input: ListBausteineInput) -> ListBausteineOutput:
    paths = _enumerate_paths(input.scope, input.domain, input.project)
    summaries: list[BausteinSummary] = []
    for p in paths:
        try:
            content = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, _ = parse_frontmatter(content)
        if not fm:
            continue
        if input.status and fm.get("status") != input.status:
            continue
        summaries.append(_summarize(fm, p))
    return ListBausteineOutput(bausteine=summaries, total=len(summaries))


def get_baustein(input: GetBausteinInput) -> GetBausteinOutput:
    if input.scope:
        p = baustein_path(input.scope, input.name, input.domain, input.project)
    else:
        # Search across all scopes by name
        candidates = [
            x for x in _enumerate_paths(None, None, None)
            if x.stem == input.name
        ]
        if not candidates:
            raise FileNotFoundError(f"baustein not found: {input.name}")
        p = candidates[0]

    if not p.is_file():
        raise FileNotFoundError(f"baustein not found at {p}")

    content = p.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    # Increment use_count + last_used
    fm["use_count"] = (fm.get("use_count") or 0) + 1
    fm["last_used"] = date.today().isoformat()
    p.write_text(compose_baustein(fm, body), encoding="utf-8")

    return GetBausteinOutput(name=input.name, path=str(p), frontmatter=fm, body=body)


def save_baustein(input: SaveBausteinInput) -> SaveBausteinOutput:
    p = baustein_path(input.scope, input.name, input.domain, input.project)
    if p.is_file() and not input.overwrite:
        raise FileExistsError(f"baustein already exists at {p}; use overwrite=true")

    today = date.today().isoformat()
    review_due = (date.today().replace(year=date.today().year + 1)).isoformat()

    frontmatter = {
        "name": input.name,
        "scope": input.scope,
        "domain": input.domain,
        "project": input.project,
        "type": input.type,
        "title": input.title,
        "language": "de",
        "source_project": input.source_project,
        "source_date": input.source_date or today,
        "captured_via": "save-baustein-tool",
        "status": "active",
        "last_validated": today,
        "review_due": review_due,
        "flagged_reason": None,
        "superseded_by": None,
        "use_count": 0,
        "last_used": None,
        "successful_uses": [],
        "rejected_uses": [],
        "references": input.references,
        "tags": input.tags,
    }
    # Drop None-valued optional fields for clarity
    frontmatter = {k: v for k, v in frontmatter.items() if v is not None or k in ("flagged_reason", "superseded_by", "last_used", "domain", "project", "source_project")}

    p.parent.mkdir(parents=True, exist_ok=True)
    created = not p.is_file()
    p.write_text(compose_baustein(frontmatter, input.body), encoding="utf-8")

    return SaveBausteinOutput(name=input.name, path=str(p), created=created)


def flag_baustein(input: FlagBausteinInput) -> FlagBausteinOutput:
    candidates = [x for x in _enumerate_paths(None, None, None) if x.stem == input.name]
    if not candidates:
        raise FileNotFoundError(f"baustein not found: {input.name}")
    p = candidates[0]
    content = p.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    previous = fm.get("status", "active")
    fm["status"] = "flagged"
    fm["flagged_reason"] = input.reason
    p.write_text(compose_baustein(fm, body), encoding="utf-8")
    return FlagBausteinOutput(name=input.name, path=str(p), previous_status=previous)


def archive_baustein(input: ArchiveBausteinInput) -> ArchiveBausteinOutput:
    candidates = [x for x in _enumerate_paths(None, None, None) if x.stem == input.name]
    if not candidates:
        raise FileNotFoundError(f"baustein not found: {input.name}")
    p = candidates[0]
    content = p.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    fm["status"] = "archived"
    if input.superseded_by:
        fm["superseded_by"] = input.superseded_by
    p.write_text(compose_baustein(fm, body), encoding="utf-8")
    return ArchiveBausteinOutput(name=input.name, path=str(p))


def find_bausteine_by_reference(input: FindBausteineByReferenceInput) -> FindBausteineByReferenceOutput:
    matches: list[BausteinSummary] = []
    paths = _enumerate_paths(None, None, None)
    for p in paths:
        try:
            content = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, _ = parse_frontmatter(content)
        refs = fm.get("references") or []
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            if input.law and ref.get("law") == input.law:
                if input.paragraph and ref.get("paragraph") != input.paragraph:
                    continue
                matches.append(_summarize(fm, p))
                break
            if input.ruling and ref.get("ruling") == input.ruling:
                matches.append(_summarize(fm, p))
                break
            if input.leitfaden and ref.get("leitfaden") == input.leitfaden:
                matches.append(_summarize(fm, p))
                break
    return FindBausteineByReferenceOutput(
        bausteine=matches,
        matched_filter={
            "law": input.law,
            "paragraph": input.paragraph,
            "ruling": input.ruling,
            "leitfaden": input.leitfaden,
        },
    )


def _summarize(fm: dict, path: Path) -> BausteinSummary:
    return BausteinSummary(
        name=fm.get("name", path.stem),
        scope=fm.get("scope", "unknown"),
        domain=fm.get("domain"),
        project=fm.get("project"),
        type=fm.get("type", "unknown"),
        title=fm.get("title", path.stem),
        status=fm.get("status", "active"),
        use_count=fm.get("use_count") or 0,
        last_used=fm.get("last_used"),
        last_validated=fm.get("last_validated"),
        review_due=fm.get("review_due"),
        flagged_reason=fm.get("flagged_reason"),
        superseded_by=fm.get("superseded_by"),
        tags=fm.get("tags") or [],
        path=str(path),
    )
