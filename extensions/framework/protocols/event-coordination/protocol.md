---
id: event-coordination
label: Event-Shaped Coordination
type: protocol
status: active
last_updated: 2026-05-01

framework_kind: protocol
framework_key: event-coordination

display_name: Event-Shaped Coordination
protocol_kind: coordination
semver: "0.1.0"
pydantic_class: extensions.framework.protocols.event_coordination.EventCoordinationProtocol

shape_compat:
  - practitioner
  - knowledge-graph
  - federation
  - hybrid

substrate_compat:
  - claude-agent-sdk
  - ms-agent-framework

option_b_axiom: null

failure_modes:
  - mode: subscribed_specialist_unreachable
    recovery: emit_event_anyway_to_audit_trail; flag_subscriber_as_unhealthy; retry_on_next_workspace_boot
  - mode: event_subscription_circular
    recovery: gate_validation_at_workspace_boot_rejects_circular_subscriptions
  - mode: event_emission_during_critical_section
    recovery: queue_emission_until_section_releases; never_drop_events
---

# Event-Shaped Coordination Protocol

## What this implementation does

Cross-specialist coordination via AuditEvents + `event_subscriptions`. Specialists emit AuditEvents into the workspace's audit-trail; subscribed specialists react to events matching their declared subscriptions. No direct call between specialists.

Concrete pattern:
1. Specialist A completes work that affects domain X → emits AuditEvent (e.g., `phase_advanced` with details about which phase)
2. Specialist B has declared `event_subscriptions: ["phase_advanced"]` in its specialist.md — workspace's orchestrator routes the event to B
3. B reacts (perhaps generating a follow-up artifact, scheduling a deadline, querying related entities)

This is the canonical realization of `a2a-and-gemini-pattern-emulation.md` Row 4 — preserves transport-swap-to-A2A path for Tier 3 federation. Same event shape works in-process (single workspace) and over-network (federation).

## Configuration knobs

- **`subscription_strict_match: bool`** (default `false`) — if true, subscriptions must match event_kind exactly; if false, supports prefix matching (e.g., `subscriptions: ["phase_*"]` matches `phase_advanced`, `phase_started`)
- **`emit_self_loops: bool`** (default `false`) — whether a specialist's own emitted events route back to itself; default excludes self-emissions to prevent infinite loops
- **`max_event_queue_depth: int`** (default `1000`) — bounded queue per workspace; overflow triggers backpressure (events dropped into audit-trail with overflow flag rather than fully lost)

## Compat constraints

**Shapes**:
- ✅ practitioner (default coordination Protocol)
- ✅ knowledge-graph (events still useful for content-update propagation)
- ✅ federation (events are the natural cross-node coordination shape)
- ✅ hybrid (subset shapes may be event-coordinated; explicit per hybrid extension config)
- ❌ autonomous-business — uses `call-coordination` (tickets + atomic checkout; events are too loose for the transactional semantics autonomous-business needs)
- ⚠ personal-OS — overkill for single-human single-specialist deployments; may use `call-coordination` or skip coordination Protocol entirely

**Substrates**:
- ✅ Claude Agent SDK — events ride on RunHooks emit + audit-trail jsonl
- ✅ MS Agent Framework — events ride on lifecycle hooks + audit-trail jsonl
- Both substrates: `_emit_audit_event` is the substrate-level emission path; events flow through audit-trail uniformly

## Failure modes + recovery

| Mode | Detection | Recovery |
|---|---|---|
| Subscribed specialist unreachable | Event router cannot reach handler at workspace runtime | Event emitted to audit-trail anyway (immutable record); subscriber flagged as unhealthy; retry on next workspace boot |
| Event subscription circular (A subscribes to events emitted by B which subscribes to events emitted by A) | Gate validation at workspace boot detects subscription graph cycles | Boot rejects with diagnostic; deployment must resolve circular subscriptions before workspace operational |
| Event emission during critical section | Specialist mid-operation emits event that would disrupt its own work | Queue emission until section releases; never drop events (audit-trail integrity) |
| Event queue overflow | Queue depth > `max_event_queue_depth` | Events dropped into audit-trail with overflow flag (not fully lost); backpressure signal emitted; monitoring alert |

## Option B axiom binding

`option_b_axiom: null` — coordination Protocol is configurable per shape (event vs call); not one of the 3 non-overridable axioms. Different shapes legitimately need different coordination semantics.

## Migration / version evolution

v0.1.0 — initial implementation; event-shaped coordination via audit-trail + event_subscriptions field on specialist.md.

**Future versions**:
- v0.2.0 (W3 cross-shape watch-list resolution): may add per-event-kind delivery semantics (best-effort vs at-least-once vs exactly-once) when concrete cross-shape user surfaces specific reliability requirements
- v0.3.0 (W4 long-running runtime adapter): may add async event semantics for long-running workspace shapes when first autonomous-business shape extension built — though autonomous-business is more likely to use call-coordination Protocol

## Cross-references

- `docs/decisions/a2a-and-gemini-pattern-emulation.md` Row 4 — event-shaped coordination; transport-swap-to-A2A path
- `docs/decisions/audit-trail-v2.md` — AuditEvent schema; event emission contract
- `docs/decisions/terminology-and-specialist-primitive.md` (#22 Sub-DR A) — `event_subscriptions` field on SpecialistDescriptor
- `docs/decisions/entity-md-scope-model-restructure.md` — specialist's dual-nature (Framework C definition + Owner B scope)
