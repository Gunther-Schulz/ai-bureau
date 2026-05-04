---
entry: authority-binding
class: PRIMITIVE
layer: framework-mechanism
axis: cross-axis (axis-3 lean per defensibility composition)
vision_usage: derived
---

# authority-binding

- **Class**: PRIMITIVE (atomic; the actor-attribution mechanism)
- **Layer**: framework-mechanism (interface contract requiring every accountability-bearing event to record emitting actor)
- **Axis**: cross-axis (axis-3 lean — actor-attribution chain is precondition for axis-3 defensibility test; also axis-1 trust — no anonymous-actor / silent-AI-action)
- **VISION usage**: derived (composes with axis 3 authorship preservation + axis 1 intertwined-AI-trust; not directly named in current VISION)

**Canonical**: A framework mechanism that records WHICH ACTOR (per `actor_kind` enum) emitted a given AuditEvent / authored a given claim / triggered a given action — load-bearing for axis-3 defensibility (reconstructible attribution chain) + axis-1 trust (no anonymous-actor-attribution invisible work). The mechanism enforces that every accountability-bearing event carries a binding to an identified actor; per-shape policy declares the trust model parameterizing how that binding satisfies shape-specific accountability requirements.

**What it is**: The atomic interface contract the framework provides for actor attribution. Every emission through audit Surface §A (emission API + actor declaration per `arch/audit.md` §2.A) MUST carry an actor binding (`actor_kind` + actor identity); the audit class Surface enforces actor declaration at emission. Authority-binding composes with substrate Surface §C (permission flow per `arch/substrate.md` §2.C) for runtime authorization moments where authority decisions require actor-binding evidence (e.g., HITL approval requires recorded human-actor identity for the binding).

**Three architectural sub-aspects**:

1. **Per-event actor declaration** — every AuditEvent carries `actor_kind` + actor identity; framework-level guarantee per locked `actor` GLOSSARY entry + locked `event` GLOSSARY entry
2. **Per-claim author attribution** — every claim_made event records the authoring actor; reconstructible via audit-trail query (per `arch/audit.md` §2.C); per-claim chain-of-defense per axis-3
3. **Authority-decision binding** — substrate permission flow (substrate Surface §C) integrates with authority-binding so that authority-bearing decisions (signature_applied; send_authorized; budget_consumed-with-approval) bind to identified actor

**What it is NOT**:
- Not a per-shape trust policy — trust-model variation lives at shape-policy layer (practitioner-judgment / budget-policy / individual per audit `arch/audit.md` §14 cross-shape policy variation); authority-binding mechanism is the framework-level binding, shape policy declares how the binding satisfies shape-specific accountability requirements
- Not a substrate-instance-internal hash-chain — audit-trail integrity (audit Surface §D per `arch/audit.md` §2.D) is a separate mechanism; integrity verifies the audit-trail hasn't been tampered, while authority-binding identifies WHO emitted each event in the trail
- Not an authentication mechanism for human operators — authentication (substrate Surface §C permission flow per `arch/substrate.md` §2.C native primitives) is the runtime authorization mechanism; authority-binding consumes the authenticated actor identity and records it on emission. Authentication answers "is this actor who they claim to be?"; authority-binding answers "which actor emitted this?"
- Not a `mechanism` instance only — the AuditEvent's `actor_kind` field is one mechanism; authority-binding is the broader framework primitive composing actor declaration + per-claim attribution + authority-decision binding

**Cross-archetype examples**:

- **Practitioner-shape**: every `claim_made` event records `actor_kind: skill` (or `ai_runtime` per actor.md naming-note) + skill identifier + emitting practitioner-record-id; every `signature_applied` event records `actor_kind: human` + practitioner identity for legal-bind moments (six-months-later test reconstructs WHO signed each claim); every `sparring_round_completed` event records `actor_kind: ai_runtime` for production-phase engagement attribution
- **Autonomous-business-shape**: every action records `actor_kind: ai_runtime` + autonomous-decision provenance; every `budget_consumed` event binds to autonomous-actor identity + (where shape policy declares budget threshold) records `approval_requested` + `actor_kind: human` for the approval-binding actor
- **Personal-OS-shape**: minimal binding (`workspace_booted` records `actor_kind: ai_runtime`); no human-author signature events (no professional-liability concern); per-session `actor_kind: human` recorded on individual-actor-driven moments

**Boundary tests** (would the primitive work for hypothetical workspaces?):

1. **Hypothetical legal-practice workspace**: every brief paragraph emits `claim_made` with `actor_kind: skill` + emitting lawyer-record; every `brief_signed` records `actor_kind: human` + lawyer identity → YES, mechanism applies
2. **Hypothetical research-paper workspace**: every methodology claim emits `claim_made` + emitting researcher-record; every `manuscript_finalized` records `actor_kind: human` + researcher identity for authorship attribution → YES, mechanism applies
3. **Hypothetical engineering-doc workspace**: every specification claim emits `claim_made` + emitting engineer-record; every `spec_approved` records `actor_kind: human` + engineer identity for engineering-liability attribution → YES, mechanism applies

Every accountability-bearing event needs actor binding regardless of domain — the mechanism is shape-neutral / archetype-neutral / pioneer-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2.

**Composes with**:
- [actor](actor.md) — provides `actor_kind` enum + identity sourcing (the entity being bound; authority-binding records WHICH actor)
- [event](event.md) — AuditEvent schema carries `actor_kind` field (the carrier; authority-binding ENFORCES the field's presence at emission)
- `audit` (mechanism class per `arch/audit.md`) — consumes authority-binding for per-event attribution + audit-trail integrity (audit class Surface §A enforces actor declaration at emission)
- [claim](claim.md) — per-claim author attribution (chain-of-defense per axis-3); claims emit `claim_made` events with actor binding
- [defensibility](defensibility.md) — reconstructible attribution chain is a precondition for axis-3 defensibility test (one of three structural conditions composing into per-claim defensibility)
- [quality-gate](quality-gate.md) — quality-gate may verify authority-binding completeness as a gate condition (e.g., refuse send if authority-binding chain incomplete per shape policy)
- [substrate](substrate.md) — substrate Surface §C permission flow integrates with authority-binding for authority-decision moments (HITL approval records human-actor identity for the binding)
- [practitioner](practitioner.md) — practitioner-record is a specific actor-kind that authority-binding records for human-actor accountability moments
- [skill](skill.md) — skill emissions record `actor_kind: ai_runtime` + skill identifier; authority-binding makes skill-side attribution observable
- [policy](policy.md) — per-shape trust-model policy parameterizes how authority-binding satisfies shape-specific accountability (practitioner-judgment / budget-policy / individual per audit class §14)
- [workflow](workflow.md) — workflow_instance phase transitions may require specific authority per workflow definition `phase_authority_requirements` per `glossary/workflow.md` composes-with authority-binding row; authority-binding mechanism enforces actor declaration on phase-transition events (per `arch/workflow-work-unit.md` SD-4 event-kind catalog)
- [work-unit](work-unit.md) — work-unit instance lifecycle transitions emit events bound to authority-decision actor per `glossary/work-unit.md` composes-with authority-binding row (practitioner-shape send/archive = practitioner-only per defensibility-critical; autonomous-business-shape transitions = operator-attestation programmatic); per-shape policy declares which transitions require which authority via authority-binding mechanism

**VISION-grounding chain**:
- Composes with VISION axis 3 (authorship preservation) — practitioner remains-the-author requires actor-attribution chain for every accountability-bearing claim. Without authority-binding, the defensibility test (`will the practitioner be able to defend this six months from now?`) cannot answer "who emitted each claim?" — defensibility's reconstructible-reasoning-chain condition fails
- Composes with VISION axis 1 (trust / intertwining) — no anonymous-actor / silent-AI-action; intertwined AI participates in real production with attributed-emission, distinct from tacked-on AI's invisible-feature pattern
- Cross-axis (axis-3 lean): the mechanism serves both, but defensibility composition (audit-trail attribution chain → axis-3 reconstructible reasoning) is the load-bearing axis-3 dependency

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Concept-by-concept" table "Authority binding" row: "`actor_kind` enum includes `human`; AuditEvent records emitting actor"
- `arch/sparring.md` §7 Composition with framework primitives "Authority binding mechanism" row: "Authority-binding mechanism is its own framework primitive (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table); per-shape policy declares trust model"
- `arch/audit.md` §2.A (Emission API + actor declaration), §7 Composition with framework primitives "Authority binding mechanism" row, §11 `AuditTrustError` category, §14 Cross-shape policy variation "Trust model" row — audit composes with authority-binding via AuditEvent's actor field
- `docs/decisions/audit-arch-topic.md` §7 Trust subsumption rationale: "Trust SUBSUMED-IN-AUTHORITY-BINDING-MECHANISM (per-shape variation was POLICY-level on the trust-model dimension, not IMPL-level alternative architectures); authority-binding mechanism is the framework primitive"
- `docs/decisions/greenfield-rederivation-pause.md` Step 3: Trust SUBSUMED-IN-AUTHORITY-BINDING-MECHANISM verdict (Trust as Pattern A protocol CANCELLED; per-shape trust policy lives at shape-policy declaring trust model on the authority-binding mechanism)
- Locked GLOSSARY entries: [actor](actor.md) (`actor_kind` enum); [event](event.md) (AuditEvent schema; `actor_kind` field); [claim](claim.md) (per-claim emission)

**See**:
- [actor](actor.md) (the entity being bound)
- [event](event.md) (the carrier of the binding; AuditEvent schema)
- [claim](claim.md) (per-claim author attribution; chain-of-defense)
- [defensibility](defensibility.md) (axis-3 success criterion authority-binding composes into)
- `arch/audit.md` (the mechanism class consuming authority-binding for per-event attribution)
- `arch/substrate.md` §2.C (permission flow integration for authority-decision moments)
- `arch/practitioner.md` §4 + §14 (practitioner-record as human authority bound to claim_made / signature_applied events; per-shape trust model parameterizes practitioner-record's accountability surface per `arch/audit.md` §14)
- `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster ARCH topic; workflow_instance phase transitions + work-unit instance lifecycle transitions are explicit composition relationships with authority-binding per per-event actor declaration sub-aspect; per-shape policy declares which transitions require which authority)
- `arch/claim-defensibility.md` (Phase 3.5 fourth primitive-cluster ARCH topic; per-claim author attribution chain composes through `claim_made` event-kind authority-binding sub-aspect — every claim emission records `actor_kind: ai_runtime` + skill identifier; per-claim attestation events at finalization record `actor_kind: human` + practitioner-RECORD identity; reconstructible attribution chain is precondition for defensibility Cond #2 reconstructible-reasoning-chain per `glossary/defensibility.md` composes-with authority-binding row)
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Concept-by-concept" Authority binding row (canonical concept reference)
- `docs/decisions/audit-arch-topic.md` (Trust subsumption rationale)
