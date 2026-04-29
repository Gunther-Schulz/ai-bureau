"""MCP tool handlers for the unified audit trail.

Wraps the audit_trail module's AuditEvent + read/write helpers.
Tool I/O models in schemas.py; per-event Pydantic validation in
audit_trail.py.

Per docs/decisions/audit-trail-v1.md: unified write-through log
per project at `<project>/_ai/audit-trail.jsonl`. Skill-side
write integration (orchestrator, save-baustein, etc. calling
record_audit_event) is the next-immediate-session retrofit;
these handlers are the gate.
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from pbs_mcp import audit_trail
from pbs_mcp.schemas import (
    QueryAuditTrailInput,
    QueryAuditTrailOutput,
    RecordAuditEventInput,
    RecordAuditEventOutput,
)

logger = logging.getLogger(__name__)


def _resolve_project_root(project_name: str) -> Path:
    """Look up a project's root path from projects-index. Raises if
    project isn't bound."""
    # Imported here to avoid circular: tools.audit ← tools.projects ← schemas ← (no cycle)
    from pbs_mcp.tools.projects import _read_projects_index

    entries = _read_projects_index()
    for e in entries:
        if e.get("name") == project_name:
            pr = e.get("project_root")
            if pr:
                return Path(pr).expanduser()
    raise FileNotFoundError(
        f"project '{project_name}' not in projects-index; bind it first"
    )


def record_audit_event(input: RecordAuditEventInput) -> RecordAuditEventOutput:
    """Append a single event to a project's audit-trail.jsonl. Validates
    via AuditEvent contract; server-fills id + timestamp when absent."""
    project_root = _resolve_project_root(input.project)
    # Allow caller to omit id/timestamp; audit_trail.append_event server-fills.
    payload = dict(input.event)
    payload.setdefault("id", "")
    payload.setdefault("timestamp", "")
    payload.setdefault("project", input.project)
    candidate = audit_trail.AuditEvent.model_construct(**payload)
    final = audit_trail.append_event(project_root, candidate)
    trail_path = audit_trail._audit_trail_path(project_root)
    return RecordAuditEventOutput(
        event=final.model_dump(mode="json"),
        event_id=final.id,
        trail_path=str(trail_path),
    )


def _matches_filters(event: audit_trail.AuditEvent, input: QueryAuditTrailInput) -> bool:
    """Apply input's filters as AND-combined predicates."""
    if input.kind is not None:
        kinds = input.kind if isinstance(input.kind, list) else [input.kind]
        if event.kind not in kinds:
            return False
    if input.since and event.timestamp < input.since:
        return False
    if input.until and event.timestamp > input.until:
        return False
    if input.actor and event.actor != input.actor:
        return False
    if input.references_paragraph:
        needle = input.references_paragraph.lower()
        haystack = (event.summary + " " + str(event.details)).lower()
        if needle not in haystack:
            return False
    if input.references_baustein:
        if event.kind != "baustein_use":
            return False
        if event.details.get("baustein_name") != input.references_baustein:
            return False
    return True


def query_audit_trail(input: QueryAuditTrailInput) -> QueryAuditTrailOutput:
    """Filter the unified log across one or all projects. Strict-validation
    discipline: re-reads + re-validates each event line; malformed audit-
    trail.jsonl raises (defense risk if silently skipped)."""
    from pbs_mcp.tools.projects import _read_projects_index

    if input.project:
        project_roots = [(_resolve_project_root(input.project), input.project)]
    else:
        # Fan out across all bound projects.
        project_roots = []
        for e in _read_projects_index():
            pr = e.get("project_root")
            name = e.get("name")
            if pr and name:
                project_roots.append((Path(pr).expanduser(), name))

    matched: list[audit_trail.AuditEvent] = []
    sources_referenced: dict[str, int] = {}
    for root, _name in project_roots:
        for event in audit_trail.read_events(root):
            if not _matches_filters(event, input):
                continue
            matched.append(event)
            for src in event.sources:
                sources_referenced[src.file] = sources_referenced.get(src.file, 0) + 1

    matched.sort(key=lambda e: e.timestamp, reverse=True)
    total = len(matched)
    truncated = matched[: input.limit]

    return QueryAuditTrailOutput(
        events=[e.model_dump(mode="json") for e in truncated],
        total=total,
        sources_referenced=sources_referenced,
    )
