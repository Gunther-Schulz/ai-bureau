# Decision record: unified audit trail v2 — JSONL canonical, single-write

**Status**: ACCEPTED (session 7, 2026-04-29; supersedes v1)
**Owner**: per-session HANDOFF; ARCHITECTURE.md Memory (record) sub-kind
**Supersedes**: `audit-trail-v1.md` (session 6)

## Context

Session-6's v1 commitment (`audit-trail-v1.md`) added a unified
JSONL log alongside the existing 6 prose audit sources, with
**dual-write discipline** — every event-producing skill writes to
both the prose source AND the unified log. Session-7's
audit-trail review surfaced the question: do we actually need the
prose sources, or is JSONL sufficient with render-time prose
synthesis?

The honest read: 5 of 6 prose sources are subsumable. Only
`snapshots/` (artifact bytes) and `decisions.md` (legal-defense
provenance) need persistent prose form. v2 retires the
dual-write discipline for a single-write architecture.

This is also a worked example for a more general pattern: **adding
a new mechanism without explicitly asking "what does this subsume?"
leaves load-bearing legacy in place by inertia.** Design-review
target 9 (Subsumption check) and audit slice 18 (Legacy retirement
scan), added in the same session, codify the question so future
mechanism-adds catch this at design time.

## Decision

**Single-write to the unified JSONL log, with `decisions.md` as
the only persistent prose source.** All other prose audit sources
become render-time views computed from JSONL queries.

**Storage layout** (after v2):

| Source | Status | Why |
|---|---|---|
| `<project>/_ai/audit-trail.jsonl` | Canonical machine-queryable log | Single source of truth for events |
| `<project>/_ai/decisions.md` | Persistent prose; user-approved | Legal-defense provenance — "I approved this on 2024-03-15" carries weight under UNB challenge |
| `<project>/_ai/snapshots/<date-recipient>/` | Persistent artifact bytes | Can't be in JSONL (PDFs, .tex source) |
| ~~`<project>/_ai/module-decisions.md`~~ | RETIRED | Render from `module_decision` events |
| ~~`<project>/_ai/correspondence-log.md`~~ | RETIRED | Render from `correspondence` events |
| ~~`<roots.references>/changelog.md`~~ | RETIRED | Render from `reference_update` events |
| ~~`state.md.phase_history`~~ | RETIRED (frontmatter field removed) | Render from `phase_transition` events |

**Write discipline**: skills call `record_audit_event` ONLY. The
gate-side `record_decision` MCP tool atomically writes BOTH the
unified log AND `decisions.md` — skills never see the dual-write,
it's hidden inside the gate. No more skill-side dual-write
discipline.

**Render discipline**: the `render_audit_trail` MCP tool produces
prose reports from queries. Adaptive — UNB asks about §45 → focused
report on `baustein_use` events citing §45 BNatSchG with chronology.
Replaces the static views that prose sources gave.

## Schema changes vs v1

`AuditEvent` Pydantic model unchanged in shape; one expanded field:

- `details: dict[str, Any]` — for `decision` and `module_decision`
  events, MUST contain `reasoning_full_text: str` (the complete
  reasoning prose, not a 100-char excerpt). Per-kind validators
  enforce. The v1 spec had `reasoning_excerpt: 100-char` — replaced
  with full text since JSONL is now canonical (length is no longer
  a cost since render synthesizes from this).

New event kind:

- `user_confirmation` — captures user's explicit approval of an
  AI-drafted decision/recommendation. `details: {confirmed_event_id:
  <id>, confirmed_at: <datetime>, confirmation_text: <user-typed
  free text or "approved" if button-click}`. Required for any
  `decision` event that was AI-drafted; chains via
  `causes: [user_confirmation_event_id]`. This is the
  legal-provenance anchor: when defending a decision, query for
  the corresponding `user_confirmation` event to show
  user-as-author.

## MCP tools

```python
# Unchanged from v1
record_audit_event(...)        # append + validate
query_audit_trail(...)         # filter + return events

# v2 additions
record_decision(input: RecordDecisionInput) -> RecordDecisionOutput
    """Atomically writes BOTH the decision event to JSONL AND
    appends the prose entry to decisions.md. Skills call this
    instead of the v1 dual-write idiom; the gate handles atomicity.
    Validates contract on event AND ensures decisions.md formatting
    matches the standard pattern."""

render_audit_trail(input: RenderAuditTrailInput) -> RenderAuditTrailOutput
    """Produces a prose report from a query. Input is a
    QueryAuditTrailInput plus output formatting preferences
    (chronological | by-kind | by-actor | per-baustein).
    Returns markdown text; suitable for direct UNB-defense use,
    inline display, or save-to-file. Render is deterministic
    (no LLM judgment); the wording is templated per event kind."""

# v1's backfill_audit_trail still applies for first-bind of
# pre-existing projects (walks legacy prose sources, emits events,
# then deletes the now-subsumed sources after user confirmation)
backfill_audit_trail(input: BackfillAuditTrailInput) -> BackfillAuditTrailOutput
    """v2 enhancement: dry_run shows what would be RETIRED (not just
    what would be added). Migration mode: walks legacy prose sources,
    emits events, optionally deletes the subsumed source files after
    successful round-trip render comparison."""
```

## Cross-reference invariants (simplified vs v1)

v1 had 3 invariants checking prose↔JSONL coherence. v2 has FEWER
because most prose sources are gone:

1. **Send events require snapshot existence** (unchanged): a `send`
   event's `snapshot_path` must point at an existing
   `<project>/_ai/snapshots/<date-recipient>/` directory.
2. **decisions.md ↔ decision events** (new): every paragraph in
   decisions.md corresponds to exactly one `decision` event in
   the JSONL log. The `record_decision` gate enforces this on
   write; slice 18 verifies on demand.
3. **state.md.phase ↔ latest phase_transition** (unchanged): the
   `details.to` of the latest `phase_transition` event for a
   project equals `state.md.phase`.

The v1 baustein-use invariant becomes part of slice 17 (deferred);
no behavior change.

## Why this shape (alternatives considered)

**Option A — keep dual-write (v1)**: rejected on simplification
grounds. 5 prose sources × N skills × every event = many places
where drift can sneak in. Slice 17 invariant audit was the v1
mitigation; v2 makes the invariants unnecessary by eliminating
the duplication.

**Option B — JSONL only, no decisions.md (full simplification)**:
rejected on legal-defense grounds. Under UNB challenge, the
question "did the AI synthesize this report or did you write it?"
matters — having a user-approved prose source the user can point
to is qualitatively different from "we render this from event
metadata." `user_confirmation` events partially address this, but
the persistent prose form is more legible to non-LLM readers.

**Option C (CHOSEN) — single-write to JSONL, gate-mediated mirror
to decisions.md**: skills call `record_decision` (one tool); gate
writes both. Provenance preserved; no skill-side dual-write
discipline; no drift risk for the 5 retired sources.

## Migration plan

**Pre-RAG (this session or next):**

- [x] Decision record (this file) — DONE
- [ ] `record_decision` MCP tool — atomic dual-write inside gate
- [ ] `render_audit_trail` MCP tool — deterministic prose synthesis
- [ ] AuditEvent schema: add `user_confirmation` event kind;
      enforce `reasoning_full_text` in `decision`/`module_decision`
      details
- [ ] Skill retrofits: orchestrator + save-baustein + record-feedback
      + draft-textteil-b/c + review-draft + research-references
      declare `record_audit_event` (and `record_decision` where
      applicable) in `mcp_tools_required`; bodies invoke at
      checkpoints. NO dual-write to prose sources from skills.
- [ ] state.md schema: drop `phase_history` field; ProjectState
      Pydantic updated; migration script for any existing state.md
- [ ] Update audit-trail-v1.md → mark superseded; add a
      "Superseded by audit-trail-v2.md" header note

**Migration of existing projects (when first bound)**:
- `backfill_audit_trail` reads legacy prose sources, emits events
- After successful round-trip render-vs-prose comparison, the
  retired sources can be deleted (user-confirmation gate)
- Today: zero projects bound, so backfill is academic until first
  bind. The migration code still ships pre-RAG so first-bind works.

## Why pre-RAG (timing)

Same as v1: define the schema before real events accumulate. v2
strengthens the case — by retiring 5 prose sources before any
projects bind, we avoid the painful migration of "5 prose source
files exist for project X; now we need to retire them and
reconstruct as JSONL events." Today the prose sources don't yet
exist for any project, so retirement is a schema change with no
data migration.

## Revisit triggers

- After first 5 real projects accumulate ~50+ events: validate
  the simplified schema captures what queries actually need.
- After first real Stellungnahme defense: did the trail support
  reconstruction? Was the JSONL-only render legible to the UNB
  Sachbearbeiter, or did they want the prose source form?
- If `render_audit_trail`'s deterministic-template output proves
  inadequate (queries need LLM-synthesis), revisit by adding
  `render_audit_trail_llm` as a separate tool — keeps the
  deterministic version available, adds judgment-mediated render
  on top.

## Files touched

- `docs/decisions/audit-trail-v1.md` — superseded note added
- `docs/decisions/audit-trail-v2.md` — this file
- `ARCHITECTURE.md` — Memory (record) sub-kind table updated
- `ROADMAP.md` — v1 commitment updated to v2 plan
- `plugin/skills/orchestrator/references/state-format.md` — drop
  prose-sources documentation; update to v2 layout
- 7 skill bodies (the dual-write retrofit list from v1) — single-
  write retrofit per v2
- `plugin/skills/audit/references/drift-surfaces-and-slices.md` —
  slice 17 invariants simplified per v2
