---
entry: event
class: PRIMITIVE
layer: framework-mechanism
axis: cross-axis
vision_usage: implicit
---

# event

- **Class**: PRIMITIVE (atomic; the audit-emission unit)
- **Layer**: framework-mechanism (the AuditEvent schema is a framework-level interface contract; events are the structured units of audit emission)
- **Axis**: cross-axis (events serve all three axes — they're the substrate enabling axis-3 defensibility primarily, plus axis-1 trust + axis-2 sparring records)
- **VISION usage**: implicit (VISION mentions "audit trail" line 92, 172, 183; events are the structured units of that trail; not directly defined as glossary term)

**Canonical**: A structured unit emitted to the audit trail by an actor — captures decision provenance, actor kind, timestamp, and per-event-kind details. The AuditEvent schema is a framework-level mechanism (atomic interface contract per locked `mechanism` entry).

**What it is**: The smallest unit of audit-trail content. Each event records: which actor emitted it (per `actor_kind` enum), when, what kind of event (event_kind), and event-specific details (sources, causes, decision rationale, etc. per archived audit-trail-v2 schema). Events compose into the audit trail (specific mechanism instance, ARCH Layer 3 detail); the audit trail composes from events emitted over time. Per archived corpus, events are append-only — never rewritten — which is what makes them load-bearing for axis-3 defensibility.

**What it is NOT**:
- Not the audit trail (ARCH Layer 3 detail) — audit trail is the COMPOSITION (sequence) of events; event is the atomic unit
- Not an `actor` — actors EMIT events; event is what gets emitted
- Not a workspace-state mutation — events are append-only audit records; workspace state is mutable; per archived `audit-trail-v2.md` these were unified into single-write architecture (state rendered FROM events)
- Not a session log — sessions may contain events but the event is the architectural primitive

**Cross-archetype illustration**: events emitted across all workspace shapes share the same AuditEvent schema; differ in event_kind catalog per shape:
- Practitioner-shape: claim-level events (decision_made, source_grounded, sparring_fired, send_authorized, signature_applied)
- Autonomous-business-shape: action-level events (task_started, task_completed, budget_consumed, approval_requested)
- All shapes: framework-level events (workspace_booted, specialist_activated, substrate_initialized)

The framework provides the AuditEvent schema (mechanism); shapes determine which event kinds are MANDATORY emission per their policies.

**Boundary test**: Three questions:
1. Is this an atomic structured emission unit with declared actor + timestamp + kind? → it's an event
2. Is this the sequence/composition of events over time? → it's the audit trail (ARCH Layer 3)
3. Is this the entity emitting? → it's an `actor`

**Composes with**:
- [actor](actor.md) — every event declares its emitting actor (`actor_kind` field; framework-level guarantee)
- [authority-binding](authority-binding.md) — AuditEvent's `actor_kind` field is the carrier authority-binding enforces; authority-binding ENFORCES per-event actor declaration at emission
- `audit trail` — events compose into the audit trail; audit trail = sequence of events (specific mechanism instance; canonical detail in ARCH Layer 3)
- [mechanism](mechanism.md) — the AuditEvent schema IS a framework-mechanism (atomic interface contract)
- [substrate](substrate.md) — substrate emits substrate-internal architectural events (registration / permission decision / boot complete / shutdown initiated) directly to audit-trail per substrate Surface §8 dual-emission; substrate's running Instance IS `actor_kind: ai_runtime`
- [adapter](adapter.md) — adapter operations emit per-action events via MCP audit gate (skill-side; per-class event-kind catalog per `arch/adapter.md` §11) into audit-trail
- `sparring` (mechanism class per `arch/sparring.md`) — sparring sub-mechanisms emit per-sub-mechanism events (counter_argument_produced / confidence_calibrated / etc.) via MCP audit gate skill-side
- `audit` (mechanism class per `arch/audit.md`) — audit class consumes events via Surface §A emission API; audit-trail is the COMPOSITION of events the class manages
- [skill](skill.md) — skills emit events via the AI runtime that fires them (`actor_kind: ai_runtime`)
- [defensibility](defensibility.md) — events are the structural substrate enabling axis-3 defensibility (reconstructible reasoning chain)
- [work-unit](work-unit.md) — events are emitted scoped to work-units; each event records its work-unit attribution per archived audit-trail-v2 schema (every event traceable to the work-unit it concerns)
- [claim](claim.md) — claims emit `claim_made` events (the structured emission recording that an accountability-bearing assertion was made; claim is the content, event is the audit-trail emission)
- [rubber-stamping](rubber-stamping.md) — attestation events can fire performatively without engagement; events alone don't prevent rubber-stamping (events record sign-off, not the engagement that would make sign-off substantive); per-claim attestation requirements are the counter-mechanism
- [workflow](workflow.md) — workflow_instance lifecycle emits events (workflow_started, phase_transitioned, workflow_completed, suspended, abandoned, failed); events emitted during workflow_instance execution carry workflow_instance attribution; event_kind catalog includes workflow lifecycle events (Phase 3.5 schema)

**Source**:
- Locked GLOSSARY entries: [mechanism](mechanism.md) (lists "AuditEvent schema (Pydantic model contract for audit emission)" as canonical mechanism example); [actor](actor.md) (events are emitted by actors)
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table "Audit emission" row
- VISION `VISION.md` line 92 (falsification axis 3): "if defensibility ISN'T enhanced by structural authorship (regulators don't care about audit trails)"
- Archived `audit-trail-v2.md` for full schema detail (Phase 3 ARCH territory)

**See**:
- [actor](actor.md) — events are emitted by actors
- `audit trail` (ARCH Layer 3) — composition of events
- [mechanism](mechanism.md) — AuditEvent schema as framework-mechanism
- `arch/audit.md` (mechanism class consuming events; AuditEvent schema as Surface; per-shape event-kind catalog; append-only persistence; query primitives; integrity verification)
- `arch/substrate.md` (substrate emits substrate-internal architectural events; substrate Surface §8 dual-emission paths; Surface §F provides storage realization for audit class)
