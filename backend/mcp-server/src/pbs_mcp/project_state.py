"""Pydantic schema + read/write gate for per-project state.md files.

State.md is YAML frontmatter (validated here) + free-form markdown body
(History section, append-only). The frontmatter is schema-bearing per
ARCHITECTURE.md meta-rule 4 refinement A: durable state with a typed
contract goes through MCP, never direct skill Read/Write.

This module owns:
- ProjectState Pydantic model (canonical contract for the frontmatter)
- read_project_state / write_project_state helpers (used by MCP tools
  in tools/projects.py)
- Cross-reference invariant validators (lifecycle/phase consistency,
  current phase appears in phase_history, doctype_status enum)

Per the strict-validation discipline (ARCHITECTURE.md meta-rule 4
maintenance corollary): all required fields are strictly required;
no silent defaults; fail loud with descriptive errors when contract
is violated.

The markdown body after the frontmatter (History section + free-form
prose) is preserved unchanged across read/write cycles. The body is
append-only by convention; no schema enforcement on it.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from pbs_mcp._strict import StrictModel


# === Enums + value types ================================================

Lifecycle = Literal[
    "draft",
    "internal-review",
    "sent-to-authority",
    "awaiting-response",
    "revision-requested",
    "finalized",
    "archived",
]

OwnershipMode = Literal["full", "migrate", "new-work-only", "quarantine"]

VerfahrenType = Literal[
    "regelverfahren",
    "vereinfachtes",     # §13 BauGB
    "beschleunigtes",    # §13a BauGB
    "vorhabensbezogen",  # §12 BauGB
]

DoctypeStatusValue = Literal[
    "tbd",
    "applicable",
    "active",
    "finalized",
    "not-applicable",
]

DeadlineKind = Literal[
    "behoerdliche-frist",
    "client-deadline",
    "internal",
    "stellungnahme-frist",
]

# Re-exported from office_config to avoid circular import; same Literal.
StateCode = Literal[
    "BB", "BW", "BY", "BE", "HB", "HH", "HE", "MV",
    "NI", "NW", "RP", "SH", "SL", "SN", "ST", "TH",
]


class PhaseEntry(StrictModel):
    """One Bauleitplanungs-phase transition."""
    phase: str = Field(..., min_length=1)
    entered: date


class Deadline(StrictModel):
    """One deadline tracked in state.md."""
    kind: DeadlineKind
    date: date
    description: str = Field(..., min_length=1)


# === ProjectState =======================================================


class ProjectState(StrictModel):
    """Canonical schema for state.md frontmatter.

    Required fields fail loud on parse if missing; no silent defaults.
    Optional fields default to None (semantic: not-yet-known) rather
    than to placeholder values.
    """

    # === Identity (required) ===
    project: str = Field(..., min_length=1)             # YY-NN-location-slug
    project_root: Path                                   # absolute path to project dir
    bundesland: StateCode                                # ISO state code

    # === Lifecycle (required) ===
    lifecycle: Lifecycle
    ownership_mode: OwnershipMode
    practices: list[str] = Field(..., min_length=1)     # actor ids, kind=internal
    verfahren_type: VerfahrenType
    phase: str = Field(..., min_length=1)               # current Bauleitplanungs-phase

    # === Dates (required) ===
    created: date
    last_session: date

    # === Identity details (optional — None means not-yet-known) ===
    client: str | None = None
    client_contact: str | None = None
    location: str | None = None
    gemeinde: str | None = None
    landkreis: str | None = None

    # === Scope tracking ===
    doctype_status: dict[str, DoctypeStatusValue] = Field(default_factory=dict)
    phase_history: list[PhaseEntry] = Field(default_factory=list)
    deadlines: list[Deadline] = Field(default_factory=list)
    linked_projects: list[str] = Field(default_factory=list)

    # === Department engagement ===
    # Per docs/decisions/office-vs-department.md (#12): departments that have
    # engaged with this project. Empty default = no department has engaged yet.
    # Gate-mediated update via record_audit_event (deferred to #6 retrofit):
    # when an event's actor_card is in skills_in_dept, gate atomically appends
    # the department to this list if not present.
    departments_active: list[str] = Field(default_factory=list)

    # === Plan content (optional) ===
    geltungsbereich_ha: float | None = None
    geltungsbereich_solar_ha: float | None = None
    b_plan_nr: str | None = None
    b_plan_name: str | None = None

    # === Notes (optional, free-form prose preserved as-is) ===
    notes: str | None = None

    # === Validators ===

    @field_validator("project_root", mode="before")
    @classmethod
    def _resolve_path(cls, v):
        if v is None:
            return v
        return Path(str(v)).expanduser()

    @model_validator(mode="after")
    def _check_phase_in_history(self) -> "ProjectState":
        """Current phase must appear in phase_history (when history exists)."""
        if self.phase_history:
            phases = {e.phase for e in self.phase_history}
            if self.phase not in phases:
                raise ValueError(
                    f"current phase '{self.phase}' must appear in phase_history; "
                    f"history phases: {sorted(phases)}"
                )
        return self

    @model_validator(mode="after")
    def _check_dates_ordered(self) -> "ProjectState":
        """last_session must be on/after created."""
        if self.last_session < self.created:
            raise ValueError(
                f"last_session ({self.last_session}) is before created "
                f"({self.created}); state.md dates are inconsistent"
            )
        return self


# === Read/write helpers =================================================

class ProjectStateFile(StrictModel):
    """The full state.md file: validated frontmatter + free-form body."""
    state: ProjectState
    body: str  # markdown body after the frontmatter delimiter


def parse_state_file(content: str) -> ProjectStateFile:
    """Parse a state.md file's text into validated frontmatter + raw body.

    Raises pydantic.ValidationError if frontmatter violates the contract.
    Raises ValueError if the file is missing the YAML frontmatter delimiter.
    """
    import yaml

    if not content.startswith("---"):
        raise ValueError(
            "state.md must start with YAML frontmatter delimiter `---`; "
            "got file beginning with: " + content[:50].replace("\n", "\\n")
        )

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(
            "state.md must have YAML frontmatter terminated by a closing `---` "
            "delimiter on its own line"
        )

    frontmatter_text = parts[1]
    body = parts[2].lstrip("\n")

    fm_dict = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(fm_dict, dict):
        raise ValueError(
            f"state.md frontmatter must be a YAML mapping; got {type(fm_dict).__name__}"
        )

    state = ProjectState.model_validate(fm_dict)
    return ProjectStateFile(state=state, body=body)


def serialize_state_file(file: ProjectStateFile) -> str:
    """Serialize a validated ProjectStateFile back to state.md text.

    Produces the same shape parse_state_file consumes: YAML frontmatter
    + markdown body, separated by `---` delimiters.
    """
    import yaml

    # Use mode="json" to coerce date/Path fields to strings for YAML.
    fm_dict = file.state.model_dump(mode="json", exclude_none=True)

    # Ordered output: identity, lifecycle, dates, scope, content, notes.
    # PyYAML preserves insertion order from Python dicts (3.7+).
    yaml_text = yaml.safe_dump(
        fm_dict,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )

    return f"---\n{yaml_text}---\n{file.body}"


def read_project_state(state_md_path: Path) -> ProjectStateFile:
    """Read + validate a state.md file. Raises on missing file or contract
    violation; never silently returns partial data."""
    if not state_md_path.is_file():
        raise FileNotFoundError(
            f"state.md not found at {state_md_path}; cannot read project state"
        )
    content = state_md_path.read_text(encoding="utf-8")
    return parse_state_file(content)


def write_project_state(state_md_path: Path, file: ProjectStateFile) -> None:
    """Write a validated ProjectStateFile to disk. Validates round-trip
    before writing; raises if serialization produces invalid output."""
    text = serialize_state_file(file)
    # Round-trip: re-parse to confirm we wrote valid frontmatter.
    parse_state_file(text)
    state_md_path.parent.mkdir(parents=True, exist_ok=True)
    state_md_path.write_text(text, encoding="utf-8")
