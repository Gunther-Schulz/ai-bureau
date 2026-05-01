"""Unified audit trail — Pydantic schema + read/write helpers.

Per VISION axis 3 (authorship preservation) defensibility test
("user defends six months later under UNB challenge"). The unified
log is the canonical machine-queryable view of the audit trail;
existing prose sources (decisions.md, snapshots/, etc.) remain
for human-readable context.

Design record: docs/decisions/audit-trail-v1.md.

Storage: `<project>/_ai/audit-trail.jsonl` — JSON Lines, append-
only. One AuditEvent per line. Append is O(1); query is filtered-
read.

Per the strict-validation discipline (ARCHITECTURE.md meta-rule 4):
all events validated by Pydantic on write; malformed events fail
loud with descriptive errors; never silently dropped.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from pbs_mcp._strict import StrictModel


# === Event taxonomy =====================================================

EventKind = Literal[
    "decision",                # entry in decisions.md
    "module_decision",         # entry in module-decisions.md
    "phase_transition",        # state.md.phase change
    "lifecycle_transition",    # state.md.lifecycle change
    "send",                    # snapshot created
    "correspondence",          # correspondence-log.md entry
    "doctype_status_change",   # state.md.doctype_status update
    "scope_change",            # bundesland/verfahren_type/ownership
    "reference_update",        # research-references applied an update
    "baustein_use",            # baustein cited (successful/rejected)
]


# Per docs/decisions/a2a-and-gemini-pattern-emulation.md — distinguishes
# the kind of agent that produced the event. "human" = a person (Gunther,
# colleague, user under multi-user deployment). "skill" = a PBS skill or
# plugin agent emitting an event during its execution. "external_agent" =
# an A2A peer producing events into our trail (today: none; reserved for
# future cross-office workflows). The discrimination is independently
# valuable for #11 (plugin agents as skill-kind) and #12 (per-department
# audit views via skill membership), and forward-compatible with A2A.
ActorKind = Literal["human", "skill", "external_agent"]


# === Source references ==================================================


class SourceRef(StrictModel):
    """Pointer to the prose source where the event's content lives.

    Lets a query consumer follow back from an event ID to the human-
    readable file (decisions.md, module-decisions.md, snapshot manifest,
    etc.). At least one source is required per event.
    """
    file: str = Field(..., min_length=1)  # path relative to project root
    line: int | None = None               # for line-addressable sources
    section: str | None = None            # for section-addressable sources


# === Audit event ========================================================


class AuditEvent(StrictModel):
    """One audit-relevant event.

    Strict-validation discipline: all required fields strictly required;
    `details` payload shape is `kind`-specific (richer per-kind validators
    land in next-session iteration). The minimum-viable model captures the
    common shape; per-kind invariants checked by slice 17 (future).
    """
    id: str = Field(..., min_length=1)               # UUID v4
    timestamp: datetime                              # UTC, ISO-8601
    kind: EventKind
    project: str = Field(..., min_length=1)          # YY-NN-slug
    actor: str = Field(..., min_length=1)            # office actor id, kind=internal
    actor_kind: ActorKind                            # human | skill | external_agent
    actor_card: str | None = None                    # reserved for agent-card URL (A2A)
    origin_agent_card: str | None = None             # source A2A peer (when external_agent)
    summary: str = Field(..., min_length=1)          # one-line description
    details: dict[str, Any] = Field(default_factory=dict)
    sources: list[SourceRef] = Field(..., min_length=1)
    causes: list[str] = Field(default_factory=list)  # other event IDs

    @field_validator("timestamp", mode="after")
    @classmethod
    def _ensure_tz(cls, v: datetime) -> datetime:
        """Naive datetimes treated as UTC; explicit-tz preserved."""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    @model_validator(mode="after")
    def _check_external_agent_origin(self) -> "AuditEvent":
        """external_agent events MUST name their source peer.

        Per docs/decisions/a2a-and-gemini-pattern-emulation.md row 5: the
        actor_kind discrimination is meaningful only if external_agent
        events can be traced back to their origin. Today no external
        events exist; this invariant guards future A2A-peer integration
        from emitting unattributable events into our trail.
        """
        if self.actor_kind == "external_agent" and not self.origin_agent_card:
            raise ValueError(
                f"actor_kind='external_agent' requires origin_agent_card to be set; "
                f"event {self.id} cannot be external without naming its source peer"
            )
        return self


# === Read/write helpers =================================================


def _audit_trail_path(project_root: Path) -> Path:
    """Resolve a project's audit-trail.jsonl path. Checks both _ai/ and
    .ai/ to match the per-project AI-state convention."""
    for ai_dir in ("_ai", ".ai"):
        candidate = project_root / ai_dir / "audit-trail.jsonl"
        # If the parent ai-dir exists, return that path (file may not yet).
        if (project_root / ai_dir).is_dir():
            return candidate
    # Default to _ai/ for new files (matches existing-project convention).
    return project_root / "_ai" / "audit-trail.jsonl"


def append_event(project_root: Path, event: AuditEvent) -> AuditEvent:
    """Append a validated AuditEvent to the project's audit-trail.jsonl.

    Server-side fills `id` (UUID v4) and `timestamp` (now-UTC) if the
    caller provides empty/sentinel values. Re-validates the resulting
    event before write per round-trip discipline.

    Returns the post-fill, post-validation event.
    """
    # Fill server-side fields if absent. Caller is allowed to provide
    # them (e.g., backfill from existing sources with historical dates),
    # but if absent we generate them. Pydantic Field(...) requires non-
    # empty strings, so callers omitting id pass `id=""` and we replace.
    data = event.model_dump(mode="python")
    if not data.get("id"):
        data["id"] = str(uuid.uuid4())
    if not data.get("timestamp"):
        data["timestamp"] = datetime.now(timezone.utc)

    final = AuditEvent.model_validate(data)
    line = final.model_dump_json()  # one JSON object per line
    trail_path = _audit_trail_path(project_root)
    trail_path.parent.mkdir(parents=True, exist_ok=True)
    with trail_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return final


def read_events(project_root: Path) -> list[AuditEvent]:
    """Read all events from the project's audit-trail.jsonl. Validates
    each line. Raises on malformed line per fail-loud discipline (a
    corrupted audit log is a defense risk; better to surface than to
    silently skip)."""
    trail_path = _audit_trail_path(project_root)
    if not trail_path.is_file():
        return []
    events: list[AuditEvent] = []
    for line_num, raw in enumerate(trail_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue  # skip blank lines (tolerated for human-edit aesthetics)
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"audit-trail.jsonl line {line_num} is malformed JSON: {e}"
            ) from e
        events.append(AuditEvent.model_validate(obj))
    return events
