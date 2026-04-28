"""Project tools — list, bind, unbind, lightweight-survey.

Heavy survey logic lives in the survey-project skill (markdown
orchestration); these tools are filesystem ops that the skill calls.
"""
from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from pbs_mcp import config, office_config
from pbs_mcp.db import get_db
from pbs_mcp.schemas import (
    BindProjectInput,
    BindProjectOutput,
    ListProjectsInput,
    ListProjectsOutput,
    ProjectSummary,
    SurveyProjectInput,
    SurveyProjectOutput,
    UnbindProjectInput,
    UnbindProjectOutput,
)
from pbs_mcp.tools.memory import compose_baustein, parse_frontmatter

logger = logging.getLogger(__name__)


def _projects_index_path() -> Path:
    return config.office_state_root() / "projects-index.md"


def _default_practice_id() -> str:
    return office_config.load().default_practice().id


def _read_projects_index() -> list[dict]:
    p = _projects_index_path()
    if not p.is_file():
        return []
    content = p.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(content)
    return fm.get("projects") or []


def _write_projects_index(projects: list[dict]) -> None:
    p = _projects_index_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = {"version": 1, "last_updated": date.today().isoformat(), "projects": projects}
    body = "# Projects index\n\nMaintained by pbs-mcp. Do not edit manually.\n"
    p.write_text(compose_baustein(fm, body), encoding="utf-8")


def list_projects(input: ListProjectsInput) -> ListProjectsOutput:
    entries = _read_projects_index()
    summaries: list[ProjectSummary] = []
    for e in entries:
        if input.state and e.get("lifecycle") != input.state:
            continue
        if input.practice and input.practice not in (e.get("practices") or []):
            continue
        summaries.append(ProjectSummary(
            name=e.get("name", "?"),
            project_root=e.get("project_root", ""),
            client=e.get("client"),
            location=e.get("location"),
            lifecycle=e.get("lifecycle", "draft"),
            practices=e.get("practices") or [],
            last_session=e.get("last_session"),
            deadlines=e.get("deadlines") or [],
        ))
    return ListProjectsOutput(projects=summaries, total=len(summaries))


def bind_project(input: BindProjectInput) -> BindProjectOutput:
    """Register a project + path mapping. Creates _ai/state.md if needed."""
    root = Path(input.root_path) if input.root_path else _resolve_root_by_name(input.name)
    if not root.is_dir():
        raise FileNotFoundError(f"project root not a directory: {root}")

    ai_dir = _select_ai_dir(root)  # _ai/ for existing, .ai/ for new (heuristic)
    state_path = ai_dir / "state.md"
    created = not state_path.is_file()

    if created:
        ai_dir.mkdir(parents=True, exist_ok=True)
        state_fm = {
            "project": input.name,
            "project_root": str(root),
            "lifecycle": "draft",
            "ownership_mode": "new-work-only",
            "practices": [_default_practice_id()],
            "doctype_focus": [],
            "doctype_status": {},
            "phase": None,
            "phase_history": [],
            "deadlines": [],
            "linked_projects": [],
            "created": date.today().isoformat(),
            "last_session": date.today().isoformat(),
        }
        body = "# History\n\n- " + date.today().isoformat() + " — Project bound.\n"
        state_path.write_text(compose_baustein(state_fm, body), encoding="utf-8")

    # Append to projects-index
    entries = _read_projects_index()
    if not any(e.get("name") == input.name for e in entries):
        entries.append({
            "name": input.name,
            "project_root": str(root),
            "lifecycle": "draft",
            "practices": [_default_practice_id()],
            "last_session": date.today().isoformat(),
        })
        _write_projects_index(entries)

    return BindProjectOutput(
        name=input.name,
        project_root=str(root),
        state_path=str(state_path),
        created=created,
    )


def unbind_project(input: UnbindProjectInput) -> UnbindProjectOutput:
    """Delete project's namespaced chunks; optionally remove index entry."""
    db = get_db()
    chunks_deleted = db.delete_by_filter(
        f"project = '{input.name}' AND artifact_kind = 'input'"
    )

    if not input.keep_index_entry:
        entries = _read_projects_index()
        entries = [e for e in entries if e.get("name") != input.name]
        _write_projects_index(entries)

    return UnbindProjectOutput(
        name=input.name,
        chunks_deleted=chunks_deleted,
        index_entry_kept=input.keep_index_entry,
    )


def survey_project(input: SurveyProjectInput) -> SurveyProjectOutput:
    """Lightweight cluster proposal. Heavy survey logic is in the skill."""
    root = Path(input.project_root) if input.project_root else _resolve_root_by_name(input.project)
    if not root.is_dir():
        raise FileNotFoundError(f"project root not a directory: {root}")

    clusters: dict[str, list[str]] = {
        "doctype-artifacts": [],
        "inputs": [],
        "correspondence": [],
        "resources": [],
        "cruft": [],
        "unknown": [],
    }

    EXCLUDE_EXT = {".aux", ".fdb_latexmk", ".fls", ".log", ".lot", ".toc", ".synctex.gz"}
    layout = office_config.load().conventions.project_folder_layout
    inputs_seg = "/" + layout.inputs.strip("/").lower() + "/"
    sent_seg = "/" + layout.sent_versions.strip("/").lower() + "/"
    corr_seg = "/" + layout.correspondence.strip("/").lower() + "/"
    toeb_seg = "/" + layout.toeb.strip("/").lower() + "/"

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root))
        if any(rel.endswith(ext) for ext in EXCLUDE_EXT) or rel.startswith("~$") or "/.git/" in rel:
            clusters["cruft"].append(rel)
            continue

        rel_lower = "/" + rel.lower()
        if rel_lower.endswith((".tex", ".bib")) or "/textbausteine/" in rel_lower:
            clusters["doctype-artifacts"].append(rel)
        elif inputs_seg in rel_lower or sent_seg in rel_lower or toeb_seg in rel_lower:
            clusters["inputs"].append(rel)
        elif corr_seg in rel_lower or rel_lower.endswith(".eml"):
            clusters["correspondence"].append(rel)
        elif "/fotos/" in rel_lower or "/bilder/" in rel_lower or "/gis/" in rel_lower or "/karten/" in rel_lower:
            clusters["resources"].append(rel)
        else:
            clusters["unknown"].append(rel)

    proposed_state: dict[str, Any] = {
        "project": input.project,
        "project_root": str(root),
        "lifecycle": "draft",
        "ownership_mode": "new-work-only",
        "practices": [_default_practice_id()],
        "doctype_status": {},
    }

    proposed_file_map = "(generated by survey-project skill — confirm clusters)"

    return SurveyProjectOutput(
        project=input.project,
        clusters=clusters,
        proposed_state=proposed_state,
        proposed_file_map=proposed_file_map,
    )


# === Helpers ===

def _resolve_root_by_name(name: str) -> Path:
    """Resolve a project name to its root path via projects-index."""
    entries = _read_projects_index()
    for e in entries:
        if e.get("name") == name:
            return Path(e.get("project_root", ""))
    # Fallback: search projects_root for a folder matching the name
    projekte = config.projects_root()
    if projekte.is_dir():
        for d in projekte.iterdir():
            if d.is_dir() and name in d.name:
                return d
    raise FileNotFoundError(f"project not found in index or projects_root: {name}")


def _select_ai_dir(root: Path) -> Path:
    """Pick visible _ai/ for existing projects, hidden .ai/ for AI-owned ones.

    Detection: prefer whichever already exists. If neither does, fall back
    to _ai/ because bind_project is the entry point for *adopting* an
    existing folder; fresh AI-owned projects come in via scaffold_project
    which creates .ai/ explicitly.
    """
    if (root / ".ai").is_dir():
        return root / ".ai"
    if (root / "_ai").is_dir():
        return root / "_ai"
    return root / "_ai"
