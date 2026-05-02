---
entry: actor
class: PRIMITIVE
layer: cross-cutting
axis: cross-axis
vision_usage: implicit
---

# actor

- **Class**: PRIMITIVE (atomic; the event-emitter unit)
- **Layer**: cross-cutting (actor spans human + AI runtime + external systems; orthogonal to framework/shape split)
- **Axis**: cross-axis (actors emit events serving any axis; axis-3 lean — actors are the named-emitter primitive enabling axis-3 defensibility through audit attribution)
- **VISION usage**: implicit (VISION's "the user" + "the AI" map to actor kinds; not directly defined)

**Canonical**: An entity that emits events within the architecture — a human, an AI runtime, or an external system. Every AuditEvent declares its emitting actor (`actor_kind` enum; framework-level guarantee per locked `mechanism` entry). Actors are workspace-scope managed entities at Owner B (per `Owner B scope` members list).

**What it is**: The primitive that gives the architecture answer-to-the-question "who/what did this?" Every audit-emitted event has an actor; every action attributable in the audit trail traces to an actor. Actors are typed (`actor_kind`): typically `human`, `ai_runtime` (for substrate-running-instance-fired actions; named to disambiguate from the `skill` primitive — work-logic unit), or `external` (for events arriving from outside the workspace, e.g., A2A peers per archived corpus). The `actor_kind` enum lives at framework-mechanism level; specific actor records live as workspace-scope managed entities at Owner B.

**Naming note**: the `actor_kind: ai_runtime` enum value is deliberately NOT named `skill` — `skill` is locked vocabulary for the atomic work-logic unit within a specialist; using it as actor_kind would create naming collision. `ai_runtime` aligns with substrate's tri-aspect Instance nomenclature.

**Cardinality + lifecycle**: Actor cardinality per workspace = 1 ai_runtime (substrate's Instance is singular per workspace) + 1+ humans (practitioner-record(s); per shape — practitioner-shape mandates ≥1, multi-practitioner-shape allows N) + N external actors (peers, clients, external systems contacting the workspace; bounded by which adapters are activated). Lifecycle = practitioner-record created at workspace setup OR per-practitioner-addition; ai_runtime exists for duration of substrate activation; external actor records emerge when external entities first interact (lazy-creation per archived governance-and-identity-sourcing.md).

**What it is NOT**:
- Not a `practitioner` — practitioner is one specific actor kind (a human-practitioner-author); actor is the broader category that also includes AI runtimes and external systems
- Not the AI runtime — AI runtime is one actor kind (typically `actor_kind: ai_runtime` for substrate-running-instance-fired actions); actor is the abstraction
- Not an `event` — events are emitted BY actors; actor is the emitter, event is what gets emitted
- Not a workspace-config field — actors are managed entities (records); workspace.md may reference actors, not contain them inline

**Cross-archetype illustration**: actors recur across all workspace shapes:
- Practitioner-shape: human-practitioner-author actor + AI runtime actor + occasional external actors (clients sending email)
- Autonomous-business-shape: operator/board actor (humans) + AI runtime actors + customer-system actors (external)
- Personal-OS-shape: individual actor (human) + AI runtime actor
- Federation-shape: cross-node-peer actors (external A2A)

**Boundary test**: Three questions:
1. Does this entity emit audit events? → it's an actor
2. Is this the typed-kind of who emitted? → that's `actor_kind` (a property of actor + a framework mechanism)
3. Is this the structured emission unit? → that's an `event`, not an actor

**Composes with**:
- [event](event.md) — events are emitted by actors
- [mechanism](mechanism.md) — `actor_kind` enum is a framework-level mechanism (interface contract requiring every event to declare its actor)
- [Owner B scope](owner-b-scope.md) — actor records live as workspace-scope managed entities
- [practitioner](practitioner.md) — practitioner-record is one specific actor kind (human-practitioner-author)
- `audit trail` — actors' events compose into audit trail (specific mechanism instance; canonical detail in ARCH Layer 3, not a separate GLOSSARY entry)
- [skill](skill.md) — skills emit events via the AI runtime that fires them (`actor_kind: ai_runtime`)
- [work-unit](work-unit.md) — actors emit events scoped to work-units; actor attribution is per-work-unit in audit trail
- [engaged authorship](engaged-authorship.md) — practitioner's engagement is tested via human-actor events (`actor_kind: human`); AI-runtime sparring events serve as the production-phase substrate but are not the engagement subject; engaged-authorship test resolves on practitioner-actor attribution

**Source**:
- Locked GLOSSARY entries: [mechanism](mechanism.md) ("`actor_kind` enum (declared on every audit event; framework-level guarantee)"); [Owner B scope](owner-b-scope.md) ("Actor (event emitter — could be human-practitioner or AI runtime)"); [skill](skill.md) (composes-with: "skills emit AuditEvents via the AI runtime that fires them — `actor_kind: ai_runtime`")
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Authority binding" row in concept-by-concept table: "`actor_kind` enum includes `human`; AuditEvent records emitting actor"

**See**:
- [event](event.md) — what actors emit
- [practitioner](practitioner.md) — one actor kind (human)
- [mechanism](mechanism.md) — `actor_kind` is a framework-mechanism
- ARCH Layer 3 actor-detail topics (placeholder until Phase 3 — full actor_kind enum, A2A actor support per archived `a2a-and-gemini-pattern-emulation.md`, actor identity sourcing per archived `governance-and-identity-sourcing.md`)
