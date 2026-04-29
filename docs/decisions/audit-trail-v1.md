# Decision record: unified audit trail (v1 commitment)

**Status**: ACCEPTED (pulled forward from ROADMAP defer per
target 8 first-run finding F2, 2026-04-29 session 6)
**Owner**: per-session HANDOFF; full build spans 1-2 sessions

## Context

VISION's defensibility test ("can the user defend this output six
months later under UNB challenge, having forgotten the details?")
is the load-bearing axis-3 (authorship preservation) requirement.
Today the audit-relevant evidence is scattered across 6 sources
with no query layer:

| Source | What it captures |
|---|---|
| `<project>/_ai/decisions.md` | Major project decisions (prose) |
| `<project>/_ai/module-decisions.md` | Per-doctype module include/exclude rationale |
| `<project>/_ai/state.md` (`phase_history`, `lifecycle`) | Lifecycle transitions |
| `<project>/_ai/snapshots/<date-recipient>/` | What was sent + when + to whom |
| `<project>/_ai/correspondence-log.md` | Mail/call/meeting index |
| Git history | Code/doc changes |
| `<roots.references>/changelog.md` | Reference-corpus updates |

User reconstructing "what happened with §45 BNatSchG argumentation
between Vorentwurf and Entwurf for project 24-12" today does manual
file-tour across these sources. Per VISION's defensibility test,
this should be a query, not detective work.

Design-review target 8 first run flagged this as the highest-
leverage axis-3 gap. User pulled it forward to v1 (no deferral)
in session 6.

## Decision

Build a unified write-through audit log per project as a new
Memory (record) sub-kind, alongside bausteine.

**Storage**: `<project>/_ai/audit-trail.jsonl` — JSON Lines,
append-only. One event per line. Why JSONL not YAML: append is O(1);
YAML requires re-serializing the whole file each write. Event logs
are the operational use case for JSONL.

**Authority**: the unified log is the canonical *machine-queryable*
view of the audit trail. The 6 existing sources are NOT removed —
they remain authoritative for *human-readable prose context*
(decisions.md keeps the full reasoning text, snapshots keep the
artifact bytes, etc.). The unified log captures *events* with
references back to the prose sources.

**Write discipline**: every skill/tool that produces an audit-
relevant event ALSO records to the unified log via
`record_audit_event` MCP tool. Dual-write discipline. Strict-
validation discipline applies — events fail loud on contract
violation.

## Schema

`AuditEvent` Pydantic model (StrictModel base, extra="forbid"):

```python
EventKind = Literal[
    "decision",               # decisions.md entry
    "module_decision",        # module-decisions.md entry
    "phase_transition",       # state.md.phase change
    "lifecycle_transition",   # state.md.lifecycle change
    "send",                   # snapshot created
    "correspondence",         # correspondence-log.md entry
    "doctype_status_change",  # state.md.doctype_status update
    "scope_change",           # bundesland/verfahren_type/ownership change
    "reference_update",       # research-references applied an update
    "baustein_use",           # baustein cited (successful_uses[]/rejected_uses[])
]

class SourceRef(StrictModel):
    """Pointer to the prose source where the event's content lives."""
    file: str           # path relative to project root
    line: int | None    # for line-addressable sources (decisions.md, etc.)
    section: str | None # for section-addressable sources

class AuditEvent(StrictModel):
    id: str              # UUID v4, generated server-side
    timestamp: datetime  # UTC, ISO-8601
    kind: EventKind
    project: str         # YY-NN-slug, must match projects-index entry
    actor: str           # office actor id (kind=internal); responsible signer
    summary: str         # one-line human description
    details: dict[str, Any]  # event-kind-specific payload (validated by kind below)
    sources: list[SourceRef]  # 1+ prose source references
    causes: list[str] = []   # other event IDs that caused this (chain reasoning)
```

**Per-kind details validation**: each `kind` value implies a
required-shape `details` payload. Initial spec captures the
shapes; richer validators land in next-session iteration:

- `phase_transition.details`: `{from: <phase>, to: <phase>}`
- `lifecycle_transition.details`: `{from: <lifecycle>, to: <lifecycle>}`
- `send.details`: `{recipient: <name>, recipient_email: <addr?>, snapshot_path: <relpath>, doctype: <slug>}`
- `decision.details`: `{title: <short>, reasoning_excerpt: <100-char>}`
- `module_decision.details`: `{doctype: <slug>, module: <module-name>, decision: included|excluded, reason: <100-char>}`
- `baustein_use.details`: `{baustein_name: <slug>, scope: universal|domain|state|project, scope_key: <key?>, kind: successful|rejected, feedback_id: <id?>}`
- `reference_update.details`: `{ref_id: <id>, prior_version: <str>, new_version: <str>, dependents_flagged: <int>}`
- (etc. for remaining kinds)

## MCP tools

```python
class RecordAuditEventInput(StrictModel):
    project: str
    event: AuditEvent  # client-supplied; id + timestamp filled server-side if absent

class RecordAuditEventOutput(StrictModel):
    event: AuditEvent  # post-validation, with id + timestamp

class QueryAuditTrailInput(StrictModel):
    project: str | None = None       # None = all bound projects
    kind: EventKind | list[EventKind] | None = None
    since: datetime | None = None
    until: datetime | None = None
    actor: str | None = None
    references_paragraph: str | None = None  # full-text match on summary/details
    references_baustein: str | None = None   # match against baustein_use events
    limit: int = 100

class QueryAuditTrailOutput(StrictModel):
    events: list[AuditEvent]
    total: int                  # before limit applied
    sources_referenced: dict[str, int]  # source-file → event count

class BackfillAuditTrailInput(StrictModel):
    project: str
    dry_run: bool = True  # show what would land; default no-write

class BackfillAuditTrailOutput(StrictModel):
    events_proposed: list[AuditEvent]   # if dry_run
    events_written: int                  # if not dry_run
    sources_walked: list[str]
    skipped: list[str]                   # files that couldn't be parsed
```

## Cross-reference invariants

The unified log must stay coherent with the 6 prose sources:

1. **Send events require snapshot existence**: a `send` event's
   `snapshot_path` must point at an existing
   `<project>/_ai/snapshots/<date-recipient>/` directory.
2. **Phase/lifecycle transitions match state.md**: when query_audit_trail
   returns the latest `phase_transition` for a project, its
   `details.to` must equal `<project>/_ai/state.md`'s current
   `phase` field.
3. **Baustein-use events match baustein frontmatter**: a
   `baustein_use` event with `kind: successful` corresponds to an
   entry in the baustein's `successful_uses[]`; `kind: rejected`
   corresponds to `rejected_uses[]`.

Slice 17 (future, deferred) checks these invariants on demand.

## Implementation plan

**Pre-RAG minimum (what ships before Phase 1 corpus download):**

- [x] Decision record (this file) — DONE this session
- [ ] AuditEvent Pydantic model in `pbs_mcp/audit_trail.py`
- [ ] `record_audit_event` MCP tool (append + validate)
- [ ] `query_audit_trail` MCP tool (read + filter)
- [ ] ARCHITECTURE.md addition: Memory (record) sub-kind "audit log"
- [ ] ROADMAP rewrite: this becomes a v1 commitment, not deferred

**Next-immediate-session-before-RAG:**

- [ ] `backfill_audit_trail` MCP tool — walk 6 existing sources;
      emit events
- [ ] Skill-side write integration — orchestrator + save-baustein
      + record-feedback + draft-textteil-b + draft-textteil-c +
      review-draft + research-references declare
      `record_audit_event` in `mcp_tools_required`; bodies invoke
      it at appropriate checkpoints
- [ ] Slice 17 — cross-reference invariant audit (deferred until
      first projects accumulate real audit events)

**Tool integration is on the read side; on the write side, every
event-generating skill is responsible for calling
`record_audit_event`.** This is the dual-write discipline. The
audit slice will catch missing dual-writes (skill produces an
event in a prose source but doesn't record to unified log).

## Why this shape (alternatives considered)

**Option A — virtual view, no new persistence**: query layer walks
the 6 sources at query time. Rejected: query latency scales with
project history depth; can't index for fast lookup; "what's
relevant for this query?" requires re-walking everything.

**Option B — write-through unified log (CHOSEN)**: events
canonicalized in unified log; prose sources stay for human
context. Dual-write risk mitigated by: unified log captures
events, not prose content; cross-reference invariants checkable
via slice 17.

**Option C — unified log as sole source, prose sources become
views**: rejected as too invasive pre-launch. Loses human-edit
ergonomics on decisions.md/module-decisions.md. Could revisit
post-launch if event coverage grows.

## Why pre-RAG (timing)

Per VISION axis 3: defensibility is load-bearing. Per session 6
target 8 finding F2: today's scattered trail is structurally
inadequate for the test. Pre-launch is the unique window to:
- Define the schema strictly before any real events accumulate
- Wire skill-side dual-write before the first real project session
- Avoid the migration cost of retroactive instrumentation

If we ship RAG before audit-trail, the first real project session
generates events that don't make it into the unified log. Each
such gap is a defense risk for that project's eventual UNB
challenge.

## Revisit triggers

- After first 5 real projects accumulate ~50+ events: validate
  the schema captures what queries actually need
- After first real Stellungnahme defense: did the trail support
  reconstruction? What was missing?
- Before any second deployment: the schema becomes load-bearing
  for that office's defensibility too
