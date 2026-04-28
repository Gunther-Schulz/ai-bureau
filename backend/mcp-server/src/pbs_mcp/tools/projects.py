"""Project tools — list, bind, unbind, lightweight-survey, setup.

Heavy survey logic lives in the survey-project skill (markdown
orchestration); these tools are filesystem ops that the skill calls.
"""
from __future__ import annotations

import logging
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

from pbs_mcp import config, office_config
from pbs_mcp.db import get_db
from pbs_mcp.schemas import (
    BindProjectInput,
    BindProjectOutput,
    ListProjectsInput,
    ListProjectsOutput,
    ProjectSummary,
    SetupProjectInput,
    SetupProjectOutput,
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
    existing folder; fresh AI-owned projects come in via setup_project /
    scaffold_project which creates .ai/ explicitly.
    """
    if (root / ".ai").is_dir():
        return root / ".ai"
    if (root / "_ai").is_dir():
        return root / "_ai"
    return root / "_ai"


# === setup_project (single-entry create / initialize / bind) ===

def setup_project(input: SetupProjectInput) -> SetupProjectOutput:
    """Create / initialize / bind a project depending on target state.

    Mode detection:
      - target_root absent → create folder + scaffold layout + AI dir
      - target_root exists, empty (or only contains hidden files) →
        scaffold inside the existing folder
      - target_root exists, populated → fall back to bind flow (run
        survey-project skill to build file-map first, then bind here)
    """
    cfg = office_config.load()

    name = input.name or _generate_project_name(cfg, input)
    target = Path(input.target_root) if input.target_root else cfg.paths.projects_root / name
    practice = input.practice or cfg.default_practice().id

    mode = _detect_mode(target)
    if mode == "bound":
        # Existing populated folder — short-circuit to bind, expect that
        # the orchestrator's binding flow already ran survey-project.
        bind_out = bind_project(BindProjectInput(name=name, root_path=str(target)))
        return SetupProjectOutput(
            name=name,
            project_root=str(target),
            mode="bound",
            created_paths=[bind_out.state_path] if bind_out.created else [],
            doctypes_scaffolded=[],
            state_path=bind_out.state_path,
            index_entry_added=bind_out.created,
            next_steps=[
                "Project bound from existing content. Survey produced "
                "_ai/file-map.md if survey-project skill was run before "
                "this call. Continue with drafting / review per current "
                "lifecycle state.",
            ],
        )

    # Create or initialize: scaffold the canonical layout.
    target.mkdir(parents=True, exist_ok=True)
    created: list[str] = [str(target)]

    layout = cfg.conventions.project_folder_layout
    for sub in (layout.inputs, layout.sent_versions, layout.correspondence, layout.toeb):
        d = target / sub.strip("/")
        d.mkdir(parents=True, exist_ok=True)
        created.append(str(d))

    # Scaffold doctype subfolders + Apply skeleton per chosen doctype.
    doctypes_scaffolded: list[str] = []
    for doctype in input.doctypes:
        doctype_subfolder = _doctype_subfolder(doctype)
        doctype_dir = target / doctype_subfolder
        if doctype_dir.exists() and any(doctype_dir.iterdir()):
            # Don't clobber if user pre-populated something.
            continue
        doctype_dir.mkdir(parents=True, exist_ok=True)
        skeleton = _resolve_skeleton(cfg, doctype)
        if skeleton is None or not skeleton.is_dir():
            logger.warning("no skeleton found for doctype=%s; subfolder created empty", doctype)
            created.append(str(doctype_dir))
            doctypes_scaffolded.append(doctype)
            continue
        overlays = _resolve_domain_overlays(cfg, doctype)
        _copy_skeleton(skeleton, doctype_dir, input.project_data, overlays=overlays)
        if input.git_init_latex:
            _git_init(doctype_dir)
        created.append(str(doctype_dir))
        doctypes_scaffolded.append(doctype)

    # Seed AI dir (.ai/ for fresh creation).
    ai_dir = target / ".ai"
    ai_dir.mkdir(parents=True, exist_ok=True)
    state_path = ai_dir / "state.md"
    if not state_path.is_file():
        doctype_status = {dt: "active" for dt in input.doctypes}
        state_fm = {
            "project": name,
            "project_root": str(target),
            "client": input.client,
            "location": input.location,
            "lifecycle": "draft",
            "ownership_mode": "full",
            "practices": [practice],
            "doctype_focus": input.doctypes,
            "doctype_status": doctype_status,
            "phase": None,
            "phase_history": [],
            "deadlines": [],
            "linked_projects": [],
            "created": date.today().isoformat(),
            "last_session": date.today().isoformat(),
        }
        body = f"# History\n\n- {date.today().isoformat()} — Project scaffolded by setup_project ({mode}).\n"
        state_path.write_text(compose_baustein(state_fm, body), encoding="utf-8")
        created.append(str(state_path))

    # Empty companion files
    for fname in ("decisions.md", "module-decisions.md", "file-map.md", "correspondence-log.md"):
        p = ai_dir / fname
        if not p.exists():
            p.write_text(f"# {fname.replace('-', ' ').replace('.md', '').title()}\n\n", encoding="utf-8")
            created.append(str(p))

    # Append to projects-index
    entries = _read_projects_index()
    index_added = False
    if not any(e.get("name") == name for e in entries):
        entries.append({
            "name": name,
            "project_root": str(target),
            "client": input.client,
            "location": input.location,
            "lifecycle": "draft",
            "practices": [practice],
            "last_session": date.today().isoformat(),
        })
        _write_projects_index(entries)
        index_added = True

    next_steps = [
        f"Fill in Projektdaten.tex placeholders in {target}/<doctype>/.",
        "Drop client inputs into inputs/.",
        "Use draft-textteil-b / draft-textteil-c skills when ready to draft.",
    ]
    if input.doctypes and any(_resolve_skeleton(cfg, dt) is None for dt in input.doctypes):
        next_steps.append(
            "Some doctype skeletons were not available — register them via "
            "office_config.templates.doctype_overrides or add to "
            "plugin/templates/skeletons/."
        )

    return SetupProjectOutput(
        name=name,
        project_root=str(target),
        mode=mode,
        created_paths=created,
        doctypes_scaffolded=doctypes_scaffolded,
        state_path=str(state_path),
        index_entry_added=index_added,
        next_steps=next_steps,
    )


def _detect_mode(target: Path) -> str:
    if not target.exists():
        return "created"
    if not target.is_dir():
        raise NotADirectoryError(f"target_root exists but is not a directory: {target}")
    # Empty if no entries OR only hidden/git/_ai (re-entrant scaffold).
    visible = [p for p in target.iterdir() if not p.name.startswith(".")]
    if not visible:
        return "initialized"
    return "bound"


def _generate_project_name(cfg, input: SetupProjectInput) -> str:
    """Apply conventions.project_naming template with project metadata."""
    template = cfg.conventions.project_naming
    nr = input.project_number or _next_project_number(cfg)
    today = date.today()
    values = {
        "year_2": f"{today.year % 100:02d}",
        "year_4": str(today.year),
        "nr": nr,
        "client": input.client or "<client>",
        "location": input.location or "<location>",
    }
    # Support {nr_pad:N} placeholder
    def _pad(match: re.Match) -> str:
        n = int(match.group(1))
        return str(nr).zfill(n)
    name = re.sub(r"\{nr_pad:(\d+)\}", _pad, template)
    for k, v in values.items():
        name = name.replace("{" + k + "}", str(v))
    return name


def _next_project_number(cfg) -> str:
    """Suggest next project number per `auto_increment` policy.

    Scans projects-index AND projects_root folders for the highest
    matching number under the configured pattern.
    """
    pattern = cfg.conventions.project_numbering.pattern
    if not cfg.conventions.project_numbering.auto_increment:
        return "<NR>"

    today = date.today()
    yy = f"{today.year % 100:02d}"
    yyyy = str(today.year)

    if pattern == "YY-NN":
        regex = re.compile(rf"^{yy}-(\d+)")
    elif pattern == "YYYY-NN":
        regex = re.compile(rf"^{yyyy}-(\d+)")
    elif pattern == "YY/NN":
        regex = re.compile(rf"^{yy}/(\d+)")
    elif pattern == "NN":
        regex = re.compile(r"^(\d+)")
    else:
        return "<NR>"

    candidates: set[int] = set()
    for entry in _read_projects_index():
        m = regex.search(entry.get("name", ""))
        if m:
            try:
                candidates.add(int(m.group(1)))
            except ValueError:
                pass
    projekte = config.projects_root()
    if projekte.is_dir():
        for d in projekte.iterdir():
            if d.is_dir():
                m = regex.search(d.name)
                if m:
                    try:
                        candidates.add(int(m.group(1)))
                    except ValueError:
                        pass

    next_nr = (max(candidates) + 1) if candidates else 1
    return str(next_nr)


def _doctype_subfolder(doctype: str) -> str:
    """Default subfolder name for a doctype within the project root.

    Map known doctypes to their conventional subfolder; fall back to
    capitalized-doctype-id for unknowns.
    """
    mapping = {
        "b-plan-begruendung": "B-Plan/Begründung",
        "b-plan-festsetzungen": "B-Plan/Festsetzungen",
        "f-plan-begruendung": "F-Plan/Begründung",
        "umweltbericht": "Umweltbericht",
        "artenschutz": "Externe Gutachten/Artenschutz",
    }
    return mapping.get(doctype, doctype)


def _resolve_skeleton(cfg, doctype: str) -> Path | None:
    """Resolve the *base* skeleton path for a doctype (universal layer).

    Order: office override → universal app-shipped skeleton → None.
    Domain overlays are applied separately via `_resolve_domain_overlays`.
    """
    override = cfg.templates.doctype_overrides.get(doctype)
    if override:
        return override
    return config.app_universal_skeleton_for(doctype)


def _resolve_domain_overlays(cfg, doctype: str) -> list[Path]:
    """Domain overlay skeleton paths for the office's active scope.

    Walks `cfg.scope.domains` in declaration order; returns each domain's
    skeleton dir for this doctype if one exists. Empty list if no domain
    has a skeleton overlay for this doctype (the common case today).
    """
    overlays: list[Path] = []
    for domain in cfg.scope.domains:
        p = config.app_domain_skeleton_for(domain, doctype)
        if p is not None:
            overlays.append(p)
    return overlays


def _copy_skeleton(skeleton: Path, target: Path, project_data: dict[str, Any],
                    overlays: list[Path] | None = None) -> None:
    """Copy skeleton tree into target with optional domain overlays.

    Universal skeleton copied first; each overlay then layered on top
    (later-wins for files that exist in multiple layers). After all copies,
    Projektdaten.tex placeholders are patched with project_data values.
    """
    EXCLUDE_NAMES = {".git", ".gitignore"}

    def _ignore(d, names):
        return [n for n in names if n in EXCLUDE_NAMES]

    shutil.copytree(skeleton, target, ignore=_ignore, dirs_exist_ok=True)
    for overlay in overlays or []:
        shutil.copytree(overlay, target, ignore=_ignore, dirs_exist_ok=True)

    projektdaten = target / "Projektdaten.tex"
    if projektdaten.is_file() and project_data:
        text = projektdaten.read_text(encoding="utf-8")
        for key, value in project_data.items():
            pattern = rf"\\renewcommand\{{\\{re.escape(key)}\}}\{{[^}}]*\}}"
            replacement = f"\\renewcommand{{\\{key}}}{{{value}}}"
            text = re.sub(pattern, replacement, text)
        projektdaten.write_text(text, encoding="utf-8")


def _git_init(target: Path) -> None:
    """Initialize a git repo for Overleaf-style sync per doctype repo."""
    import subprocess
    if not shutil.which("git"):
        return
    try:
        subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=target, check=True, capture_output=True, timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        logger.warning("git init failed for %s: %s", target, e)
