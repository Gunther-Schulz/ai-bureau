---
title: Quality-gate
topic-cluster: Pattern A protocol topics (#3 of 3)
status: locked
---

# Quality-gate

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the quality-gate Pattern A protocol with mechanism-shaped Surface. Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the Pydantic Protocol contract + per-axis observability hook signal-set spec (Mode 3). Foundation-up dependency: quality-gate composes with substrate's Surface §B telemetry hooks + §C permission flow + §F session/context + §G specialist registration; audit Surface §A emission + §C query + §10 boot ordering; sparring Surface §D structured output validation diagnostics; per-axis observability infrastructure across all 9 prior Phase 3.4 + Phase 3.5 ARCH topics. Closes Phase 3.6 — third + final Pattern A protocol instance; Pattern A topic-template-class FORMAL STABILITY achieved with 3 of 3 Pattern A instances complete (substrate anchor + adapter second + quality-gate third).

## 1. Topic scope

**Quality-gate** is the runtime-checkpoint Pattern A protocol with mechanism-shaped Surface — a pluggable subsystem firing at runtime checkpoints (event-triggered + periodic/threshold-triggered) to monitor for category-collapse manifestations across all three VISION axes, surface drift signals, and intervene per shape policy. Per locked `glossary/quality-gate.md`: tri-aspect Pattern A (Protocol surface = mechanism-shaped; implementations = Framework C distributable definitions per shape; running instance = workspace-bound at Owner B). Per `docs/decisions/quality-gate-scope-lock.md` Hybrid Option C: structural variation per shape captured at Implementation aspect; mechanism-shaped Surface ensures cross-implementation observability + emission compatibility.

**Cross-axis**: quality-gate is the **architectural counter-mechanism for category-collapse** per `arch/axis-interactions.md` §4.3. Per-axis category-collapse manifestations (axis-1 tacked-on / axis-2 oracle-validator-answer-machine / axis-3 rubber-stamping) follow the cross-axis failure cascade pattern per `arch/axis-interactions.md` §3.4. Quality-gate watches for these manifestations across all three axes via per-axis-failure-mode signal-set ingested at Surface §B (per-axis signal ingestion). Cross-axis cumulative observability is the load-bearing structural requirement: per the cross-axis failure cascade pattern, axis-1 failure forecloses axes 2+3 + axis-2 failure cascades to axis-3 production-phase + axis-3 attestation-phase failure independently possible — single observation point ingesting per-axis signals into one cumulative state is required to detect cascades vs. independent failures.

**Cardinality**: 1 active gate Implementation per workspace per `glossary/quality-gate.md` Cardinality + lifecycle. Selection is shape-mediated (NOT direct workspace.md selection): workspace selects shape via `workspace.md` `shape:` field; transitive gate-impl selection through shape policy bundle declaration. N gate-firing events per workspace lifetime (per-checkpoint events; event-triggered + periodic/threshold-triggered classes per §2.A).

**Composition with framework**:
- One mechanism category within `framework`
- Surface IS a `mechanism` (framework-level interface contract; mechanism-shaped per `glossary/quality-gate.md` Canonical line)
- Implementations live at `Framework C scope` as distributable definitions per shape
- Running instance bound to `Owner B scope` per workspace deployment
- Pattern A protocol per `protocol (architectural)` GLOSSARY entry (parallel to substrate + adapter)

This topic articulates: the Surface contract (single-layer mechanism-shaped; 6 capability categories — checkpoint firing API + per-axis signal ingestion + signal evaluation + intervention dispatch + audit emission + state management); the Implementation aspect (Framework C distributable per-shape implementations + selection mechanics shape-mediated); tri-aspect reconciliation; composition with framework primitives; cardinality + lifecycle; boot + shutdown phase ordering integration with composite sequence; per-shape error categories; deployment-tier awareness; cross-shape policy variation as PRIMARY conditional (quality-gate IS shape-policy-mediated by definition); pre-implementation forward-references; and Pattern A topic-template-class FORMAL STABILITY achieved.

**Phase routing**: Pydantic Protocol contract + per-axis observability hook signal-set spec + cross-axis error catalog spec → Phase 6 spec (Mode 3). Per-impl concrete impls + specialist DEFINITION manifest schema `gate_firing_requirements` field → Phase 6. Per-shape threshold-set tuning → Phase 1+ pioneer deployment data per W2 watch-list. Second-shape productization concrete impls → W1. This topic locks the architectural shape; Phase 6 locks the typed contract + per-impl + spec.

## 2. Quality-gate Protocol Surface (architectural-level capability categories)

The Surface is the universal/shape-neutral interface any quality-gate impl must satisfy. **Single-layer mechanism-shaped** per `docs/decisions/quality-gate-scope-lock.md` Hybrid Option C — mechanism-shaped Surface ensures all implementations emit comparable signals + audit events; per-shape variation lives at Implementation aspect (NOT multi-class Surface per-axis). **Articulated here at architectural-conceptual level** — Pydantic Protocol typing + per-axis observability hook signal-set spec land at Phase 6.

Six capability categories define the Surface:

### A. Checkpoint firing API

The gate provides the entry point for firing at runtime checkpoints. `gate.fire(checkpoint_kind, context)` → `GateDecision`. Two-class checkpoint taxonomy:

- **Event-triggered checkpoints**: `pre_send` / `pre_claim_finalization` / `pre_decision_lock` / `per_edit` / `workflow_phase_transition` / `session_end` — fire AT specific runtime events; gate evaluates engagement-quality at the event moment per ingested signal-set up to that moment
- **Periodic/threshold-triggered checkpoints**: `drift_audit` — fire on time-period elapse or signal-threshold crossing; gate evaluates cumulative drift signals across session/work-unit lifetime

Per-shape policy declares which checkpoint-kinds active + threshold values + intervention mechanics (per §14 cross-shape policy variation 6-row matrix).

### B. Per-axis signal ingestion

The gate provides the entry point for ingesting per-axis-failure-mode signals. `gate.ingest_signal(axis_kind, signal_kind, value, source_event_ref)`. Per-axis-failure-mode signal catalog resolves `arch/axis-interactions.md` §7 per-axis observability hook signal-set forward-reference:

- **axis-1 signals**: tacked-on detection (workflow-bypass-rate; AI-output-on-side rate vs in-artifact rate); co-work-vs-transactional ratio (continuous-engagement signals vs invocation-driven signals)
- **axis-2 signals**: oracle / validator / answer-machine extraction patterns (query-pattern shape per `glossary/answer-machine-ai.md` boundary tests); sparring-bypass-rate (skill executions WITHOUT sparring sub-mechanism activation per `arch/sparring.md` §4); counter-argument acceptance ratio; engagement-depth signals (review-time vs claim-complexity ratio)
- **axis-3 signals**: rubber-stamping detection (per-claim attestation event timing per `glossary/engaged-authorship.md`; batch-attestation rapid-rate); engagement-depth signals at production-phase; reasoning-chain reconstructability gaps (audit-trail completeness checks per `arch/audit.md` §C query API)

Sources of signals: substrate Surface §B telemetry hooks (per `arch/substrate.md`); audit Surface §C query API (cross-claim audit-trail query per `arch/audit.md` §C); sparring sub-mechanism event-emissions per `arch/sparring.md` §4; per-claim attestation chain mechanics per `arch/claim-defensibility.md` §3.

### C. Signal evaluation

The gate provides signal evaluation against per-shape threshold-set. `gate.evaluate(checkpoint_kind, signal_set, threshold_set)` → engagement-quality verdict. Per-shape impl declares thresholds + evaluation logic per Implementation aspect (§4). Cumulative observability across axes — single evaluation point ingesting per-axis signals into one cumulative state per the cross-axis failure cascade pattern requirement.

### D. Intervention dispatch

The gate provides intervention dispatch when evaluation surfaces engagement-quality failure. `gate.intervene(decision, intervention_kind, context)`. `intervention_kind` ∈ {`friction` / `nudge` / `block` / `audit_only`}. When `intervention_kind = block` → authority-bound denial via substrate Surface §C `request_permission` per `arch/substrate.md` §C; `friction` + `nudge` are skill-side direct emission (no permission flow). Authority-binding records `actor_kind: ai_runtime` per `glossary/authority-binding.md` (gate is AI-runtime actor at intervention emission).

### E. Audit emission

The gate emits gate-fired events via audit Surface §A per `arch/audit.md` §A emission API + actor declaration. Event-kinds candidate (architectural-level enumeration; per-event-shape Pydantic schema → Phase 6):

- `gate_fired` — gate fired at checkpoint
- `gate_intervention_applied` — intervention dispatched (kind + reason captured)
- `gate_threshold_crossed` — signal threshold exceeded; pre-intervention signal
- `gate_state_persisted` — gate state persistence event (stateful impls)
- `gate_state_restored` — gate state restored from audit-trail at boot (stateful impls)
- `gate_active` — gate ready to fire (post-boot); composes with §10 boot phase ordering

Skill-side emission via MCP audit gate per `arch/audit.md` §8 dual-emission pattern (parallel to adapter §8 + sparring §8 — quality-gate emits skill-side ONLY; not substrate-internal direct emission).

### F. State management

The gate provides state management for stateful impls. `gate.get_state()` reads via audit Surface §C query API (filter by `gate_state_persisted` events for current session/work-unit context); `gate.set_state()` IS `gate_state_persisted` emission via Surface §A. Audit-trail IS state-store: NO separate gate-state-store. Avoids dual-store divergence; preserves single-write architecture per `arch/audit.md` §10 audit-trail-as-canonical-source. Stateless impls: no state read/write semantics on the Surface (operation absent).

Per `arch/audit.md` §F state-rendering-from-events: gate state IS rendered from `gate_state_persisted` event sequence per the same pattern as workspace state rendered from event-stream. Cross-deployment portability composes via audit-trail portability per `arch/audit.md` §G external-format export — gate state events are first-class in audit-trail; cross-deployment migration preserves gate state per audit-trail integrity invariants.

### Explicitly NOT in Surface

The following are NOT in Surface; they live at Implementation aspect (per-shape variation) or compose via prior framework primitives:

- Per-shape intervention mechanics specifics (friction patterns; nudge wording; block conditions specifics) — Implementation aspect per §4 + Phase 6 forward-reference per §15
- Multi-class Surface per-axis (rejected per scope-lock DR; per-axis variation belongs at signal-set level Surface §B + §C per-axis catalog + thresholds, NOT per-axis Surfaces — per the cross-axis failure cascade pattern requires single observation point ingesting cross-axis signals)
- Per-axis observability hook signal-set Pydantic Protocol typing — Phase 6 spec target (resolves `arch/axis-interactions.md` §7 per-axis observability hook signal-set forward-reference)
- Per-shape threshold values + tuning — Phase 1+ pioneer deployment data per W2 watch-list
- Authority-binding completeness verification logic — composes via `glossary/authority-binding.md` mechanism per §7

### Logic placement mode

The Surface contract is articulated here (Mode 4 conceptual; this topic) and encoded structurally in Phase 6 spec (Mode 3 Pydantic Protocol + per-axis observability hook signal-set spec + companion docs). Mode 1 production-runtime AI doesn't load this topic — production AI loads Mode 1 markdown (skills + specialists + workspace.md + shape policy bundle declaring per-shape gate-impl + threshold-set) above the Surface abstraction. Per `ARCHITECTURE.md` cross-cutting principles "AI as runtime": quality-gate Surface is Mode-2 Python-side runtime contract; the conceptual articulation here is for framework-developer orientation.

## 3. Common-surface boundary criteria

**N/A** — quality-gate has a single-layer mechanism-shaped Surface (per §2 six capability categories). The Pattern A protocol topic template's §3 (per `MAINTENANCE.md` Pattern A protocol topic template §3 applicability) applies when a protocol has multi-class Surface (e.g., adapter's per-integration-class Surfaces per `arch/adapter.md` §3). Quality-gate's Surface-vs-per-impl-variation boundary is covered in §4 Per-implementation aspect (per-shape impl + per-shape extension Protocols pattern). Parallel to substrate §3 N/A precedent (substrate has single unified Surface; per-impl extension Protocols pattern at §4).

Multi-class Surface per-axis rationale (one Surface per axis-1 / axis-2 / axis-3) was considered + not adopted per scope-lock DR Hybrid Option C verdict: per-axis variation belongs at signal-set level (Surface §B per-axis signal ingestion + Surface §C per-axis threshold-set), NOT per-axis Surfaces. Multi-class Surface would lose cross-axis cumulative observability (the cross-axis failure cascade pattern requires single observation point ingesting cross-axis signals into one cumulative state).

## 4. Per-implementation aspect

Implementations live at `Framework C scope` as distributable definitions. Each impl wraps per-shape engagement-quality enforcement to satisfy the Surface contract. Parallel to substrate §4 + adapter §4 per-implementation aspect pattern.

### Pattern level

Any per-shape engagement-quality impl that can satisfy the Surface qualifies. Pattern level is shape-policy-shape-neutral within Surface boundaries — gate-impl wraps per-shape enforcement variation while Surface contracts shape-uniform.

### Current Implementation set (CIRCA 2026)

Three concrete gate Implementations + extensible (per `glossary/quality-gate.md` Per-shape implementations row):

- **practitioner-shape-gate** — full engagement procedure (sparring composition + friction + practitioner attestation + re-engagement nudges); fail-closed (defensibility-critical); stateful (cumulative engagement signals across session via audit-trail per audit-trail-as-state-store reframe)
- **autonomous-business-shape-gate** — programmatic policy-evaluation gate (threshold-based; no human-in-loop; audit-only intervention or programmatic block); fail-open with alert (continuity prioritized); stateless (per-checkpoint policy evaluation)
- **personal-OS-shape-gate** — light gate (minimal friction; periodic drift-check report; audit-only); fail-open (lightweight); stateful but lightweight (drift-check accumulation via audit-trail)
- **research-lab-shape-gate** (preliminary; per W1 second-shape productization) — multi-author engagement procedure (co-attestation thresholds; sparring + co-attestation requests + block); fail-closed (research output accountability-bearing); stateful (multi-author engagement signals via audit-trail)

### Per-implementation declares

Each Implementation declares (parallel to substrate §4 + adapter §4 per-impl declarations):

- **Implementation identity** (id; e.g., `practitioner_shape_gate` / `autonomous_business_shape_gate` / `personal_os_shape_gate`)
- **Surface satisfaction** (claim + impl mapping each Surface capability category to per-shape native impl)
- **Per-axis signal threshold declarations** (per-axis signal-kind → threshold-value + evaluation-logic)
- **Per-shape intervention mechanics specifics** (friction patterns; nudge wording; block conditions; per `glossary/quality-gate.md` Per-shape implementations row + §14 cross-shape policy variation 6-row matrix)
- **Per-shape error semantics** (fail-closed / fail-open with alert / fail-open per shape per §11)
- **State-management mode** (stateful vs stateless per audit-trail-as-state-store reframe)
- **Deployment-tier compatibility** (Tier 1 local / Tier 2 cloud / Tier 3 federated per §13)

### Per-shape extension Protocols pattern

Per-shape gate-impl-specific value-adds accessed via typed extension Protocols (Phase 6 spec target per §15 forward-reference; pattern parallel to `arch/substrate.md` §4 per-substrate extension Protocols pattern):

- **practitioner-shape-gate extension** — exposes `practitioner-attestation-extension` (per-claim attestation engagement-quality verification; sparring composition rules per `arch/sparring.md` §4 architecturally-encoded sub-mechanisms)
- **autonomous-business-shape-gate extension** — exposes `budget-policy-extension` (programmatic threshold evaluation; per-action budget-policy substitution per `arch/audit.md` §14 action-level audit granularity)
- **personal-OS-shape-gate extension** — exposes drift-check reporting extension (periodic drift-audit summary emission)

This is structural: skill code using only Surface methods is gate-portable across shape impls by construction; skill code reaching extension Protocols is gate-impl-pinned by construction (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 — wrong shapes impossible; per `arch/substrate.md` §6 substrate-coupling-impossible-by-construction precedent).

## 5. Selection mechanics

**Shape-mediated, NOT direct workspace.md selection** — distinct architectural commitment from substrate's `workspace.md substrate:` direct field selection per `arch/substrate.md` §5. Per `glossary/quality-gate.md` Per-shape implementations row + scope-lock DR Hybrid Option C verdict: per-shape variation IS structural; shape-mediated selection preserves shape-policy semantics (workspace cannot bypass shape's per-shape-required gate impl).

### Shape-mediated selection mechanism

Workspace selects shape via `workspace.md` `shape:` field; transitive gate-impl selection through shape policy bundle declaration:

1. Workspace selects shape via `workspace.md shape:` field (per `glossary/workspace.md` shape selection)
2. Shape policy bundle declares per-shape gate-impl-id (e.g., practitioner-shape declares `gate_impl: practitioner_shape_gate`; autonomous-business-shape declares `gate_impl: autonomous_business_shape_gate`)
3. Workspace boot resolves shape policy bundle's gate-impl declaration to Implementation in Framework C catalog; workspace inherits per-shape gate-impl

### Cardinality

1:1 with workspace at framework level per `glossary/quality-gate.md` Cardinality (1 active gate Implementation per workspace; selected via shape policy declaration). Multi-tenant workspaces handled at gate-state isolation level per §13 (per-tenant gate state via session_id + actor_id discrimination).

### Validation at workspace boot

Gate selection validated at workspace boot:

- Shape policy bundle's gate-impl declaration resolves to known Implementation (per Framework C definition catalog)
- Gate-impl deployment-tier compatibility verified (per §13 per-tier compatibility declared per Implementation)
- Gate-impl compatible with active substrate (gate substrate-agnostic per `glossary/quality-gate.md`; should always pass; documented for completeness)
- Shape policy bundle's per-axis threshold-set declarations validate against gate-impl's per-axis signal-kind catalog

### Re-binding semantics

Gate-impl re-binding requires shape change (per shape-mediated selection mechanism); shape change is workspace-level architectural event (per `glossary/shape.md` shape selection lifecycle). Mid-session gate-impl swap NOT supported (would violate shape policy semantics). Gate state persisted across shape change is per-Implementation choice — Phase 6 spec territory per §15 forward-reference.

Direct `workspace.md gate:` selection (parallel to substrate's direct selection) considered + not adopted: would let workspace bypass shape's per-shape-required gate impl, violating per `glossary/quality-gate.md` Per-shape implementations + scope-lock DR Hybrid Option C structural variation per shape.

## 6. Tri-aspect reconciliation

Quality-gate as tri-aspect Pattern A primitive (per locked GLOSSARY entry + scope-lock DR Hybrid Option C):

| Aspect | Layer | What it is |
|---|---|---|
| **Surface** | mechanism (framework-level) | Single-layer mechanism-shaped contract; the six capability categories articulated in §2 (checkpoint firing API + per-axis signal ingestion + signal evaluation + intervention dispatch + audit emission + state management) |
| **Implementations** | Framework C scope | Distributable per-shape definitions wrapping per-shape engagement-quality enforcement to satisfy Surface — practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-shape-gate / extensible (research-lab-shape-gate at second-shape productization per W1) |
| **Running Instance** | Owner B scope | Bound to workspace deployment via shape-mediated selection at workspace boot; runs while workspace active; released at workspace shutdown |

### Gate-coupling impossible-by-construction

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: Surface-typed skill code structurally cannot reach impl-specific intervention mechanics without explicit isinstance check on per-shape Extension Protocol per Phase 6 spec target. Skill code calling `gate.fire / gate.ingest_signal / gate.evaluate / gate.intervene / gate.emit_event / gate.get_state` on Surface-typed reference is gate-portable across shape impls by construction; skill code reaching impl-specific intervention mechanics is gate-impl-pinned by construction. The architectural commitment makes gate-coupling-by-accident impossible.

This is one of three canonical examples of structural-over-conventional discipline applied at framework primitive design (parallel to substrate-coupling-impossible per `arch/substrate.md` §6 + adapter-impl-coupling-impossible per `arch/adapter.md` §6). Pattern A topic-template-class achieves FORMAL STABILITY with three instances complete — substrate anchor + adapter second + quality-gate third.

### Distinct from substrate's tri-aspect + adapter's tri-aspect

Substrate tri-aspect = singular per workspace; tier-aware; alternative whole-class architectural designs (Claude Agent SDK / MS AF) realize Surface differently per `arch/substrate.md` §6. Adapter tri-aspect = multi-instance + multi-class; per-class Surface variation; alternative impls per integration class realize Surface differently per `arch/adapter.md` §6. Quality-gate tri-aspect = singular per workspace per shape (1:1 cardinality); shape-policy-mediated selection (NOT direct workspace.md); alternative per-shape architectural designs (practitioner-shape-gate stateful procedure / autonomous-business-shape-gate programmatic threshold / personal-OS-shape-gate light reporting) realize single-layer mechanism-shaped Surface differently. Three Pattern A instances; three different selection mechanics + cardinality patterns; FORMAL STABILITY across three instances confirms 12+7 template extends per per-pattern instance-driven trigger.

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Quality-gate is one mechanism category within the framework (parallel to substrate + adapter; runtime-checkpoint mechanism) |
| `mechanism` | Quality-gate Protocol Surface IS a mechanism (framework-level interface contract; mechanism-shaped per `glossary/quality-gate.md` Canonical line) |
| `Framework C scope` | Quality-gate Implementations live there as distributable per-shape definitions |
| `Owner B scope` | Running gate Instance bound to workspace deployment (Owner B); 1 active gate per workspace |
| `protocol (architectural)` | Quality-gate is Pattern A protocol third instance per `glossary/protocol-architectural.md` Cross-archetype catalog; Pattern A topic-template-class FORMAL STABILITY achieved with this lock |
| `actor` | Gate Running Instance is `actor_kind: ai_runtime` at intervention dispatch emission per `glossary/actor.md` + `glossary/authority-binding.md` per-event actor declaration sub-aspect |
| **`category-collapse`** | **Cross-axis force quality-gate watches against per `arch/axis-interactions.md` §4.3 + `glossary/category-collapse.md` Composes-with quality-gate row. Quality-gate is the architectural counter-mechanism for category-collapse (gate fires at runtime checkpoints to monitor for category-collapse manifestations across all 3 axes per the cross-axis failure cascade pattern; surface drift signals; intervene per shape policy)** |
| **`intertwining (axis 1)`** | Axis-1 observability source (workflow-bypass-rate; AI-output-on-side rate vs in-artifact rate; co-work-vs-transactional ratio per Surface §B axis-1 signal catalog); state quality-gate guards against degradation toward tacked-on per `glossary/intertwining.md` |
| **`sparring (axis 2)`** | Protocol whose runtime outputs feed quality-gate observability for axis-2 detection per `arch/sparring.md` §4 sub-mechanism event-emission. Sparring sub-mechanism event-emissions are first-class signal source for Surface §B axis-2 signal catalog (oracle / validator / answer-machine extraction patterns; sparring-bypass-rate; counter-argument acceptance ratio; engagement-depth signals) |
| **`authorship preservation (axis 3)`** | Axis quality-gate tests at attestation moments via defensibility check; Surface §B axis-3 signal catalog (rubber-stamping detection; engagement-depth at production-phase; reasoning-chain reconstructability gaps) feeds gate's drift detection at attestation moments per `glossary/authorship-preservation.md` |
| **`engaged-authorship`** | Gate's axis-3 observability source per `glossary/engaged-authorship.md`. Production-phase events (sparring + per-claim source-grounding) + per-claim attestation events feed gate's drift detection at attestation moments per `arch/claim-defensibility.md` §3 attestation chain |
| **`defensibility`** | Gate's axis-3 intervention applies defensibility test at attestation checkpoints per `glossary/defensibility.md`. Per-claim defensibility composes work-unit defensibility per `arch/claim-defensibility.md` §3 — gate fires per-claim at finalization (per shape policy granularity) |
| `sparring (mechanism class)` | Protocol whose runtime outputs feed quality-gate observability for axis-2 detection per `arch/sparring.md` §4 sub-mechanism event-emission flowing through substrate event-bus per `arch/substrate.md` §E |
| **`audit (mechanism class)`** | **Gate emits via Surface §A per `arch/audit.md` §A emission API + actor declaration; gate state-restore reads via Surface §C query API per audit-trail-as-state-store reframe; per-shape audit emission granularity per `arch/audit.md` §14 composes with gate per-shape variation §14. Audit-trail-as-canonical-source per `arch/audit.md` §10 is the single-write architecture gate state preserves** |
| `claim` | Gate fires per-claim at finalization (per shape policy granularity per `glossary/claim.md` Composes-with quality-gate row); `pre_claim_finalization` checkpoint event-triggered per Surface §A two-class checkpoint taxonomy |
| `workflow_instance` / `work-unit` | Gate fires at workflow phase transitions + work-unit instance lifecycle transitions per `glossary/workflow.md` + `glossary/work-unit.md`. Observability sources for gate per `arch/workflow-work-unit.md` §4 — `workflow_phase_transition` checkpoint event-triggered per Surface §A |
| `session` | Gate fires at session boundaries; cumulative engagement signal source for stateful impls per `glossary/session.md`. `session_end` checkpoint event-triggered per Surface §A |
| `event` | Gate emits gate-fired events to audit-trail per `arch/audit.md` §A. Event-kind catalog per Surface §E (gate_fired / gate_intervention_applied / gate_threshold_crossed / gate_state_persisted / gate_state_restored / gate_active) |
| **`authority-binding`** | **Quality-gate verifies authority-binding completeness as gate condition per `glossary/authority-binding.md` Composes-with quality-gate row. Authority-binding completeness as gate condition: pre_send checkpoint evaluates "all claims in send batch have `claim_attested` event with `actor_kind: human`" per `glossary/engaged-authorship.md` attestation-phase test → if any claim lacks attestation → fail-closed block per shape semantics. Intervention authority composes with binding mechanism (gate intervention `actor_kind: ai_runtime` per `glossary/authority-binding.md` per-event actor declaration sub-aspect). Cross-axis: axis-3 attestation chain integrity IS gate's axis-3 detection mechanism per `arch/axis-interactions.md` §4.3** |
| **`shape`** | **Shape declares which Pattern A gate-impl activates (shape-mediated selection per §5; per `glossary/shape.md` shape policy bundle declaring gate-impl-id). Per-shape variation IS structural per scope-lock DR Hybrid Option C** |
| **`specialist`** | **Specialist DEFINITION may declare per-skill gate-firing requirements per `glossary/specialist.md` Composes-with quality-gate row. Manifest schema field `gate_firing_requirements: optional` Phase 6 spec target per §15 forward-reference. Reciprocal symmetry already locked between `glossary/specialist.md` Composes-with quality-gate + `glossary/quality-gate.md` Composes-with specialist** |
| **`skill`** | **Atomic work-logic unit per `glossary/skill.md`; specialist declares per-skill gate-firing requirements (manifest schema field per §15 forward-reference). Skills produce claims; gate fires at claim-finalization per shape policy granularity** |
| **`practitioner`** | **Practitioner-RECORD identity for gate intervention authority (HITL approval moments via substrate Surface §C per `arch/substrate.md` §C + `arch/practitioner.md` §4). Practitioner is engagement subject for axis-3 attestation events feeding gate's axis-3 signal catalog per Surface §B; gate's intervention may invoke HITL approval at `block` decision per Surface §D + substrate Surface §C** |
| **`substrate`** | **Gate substrate-agnostic per `glossary/quality-gate.md`; substrate provides observability infrastructure (Surface §B telemetry hooks per `arch/substrate.md` + audit Surface §C query API per `arch/audit.md` §C). Gate runs ABOVE substrate; substrate-phase 1-5 boot precondition for gate-phase 1-4 per §10 boot ordering integration** |
| **`adapter`** | **Orthogonal mechanism category — gate fires at adapter-bounded actions (e.g., `pre_send` fires before email-adapter dispatches Begründung per `arch/adapter.md` §11 email per-class event-kind catalog). Gate composes with adapter audit-event emissions for axis-3 send-class observability per `arch/adapter.md` §10 per-action audit emission** |
| `scope-model` | Cross-cutting integrator scope-categorization composition per `arch/scope-model.md` §4 authority-binding placement pattern parallel: gate Surface (mechanism) + Implementations (Framework C distributable definitions per shape) + Implementation Instance running per workspace at Owner B; §18 per-primitive composition table quality-gate row |
| **`axis-interactions`** | **Cross-axis category-collapse counter-mechanism per `arch/axis-interactions.md` §4.3. Resolves §7 per-axis observability hook signal-set forward-reference (Surface §B per-axis signal ingestion + §C per-axis threshold-set) + §14 W4 quality-gate cross-axis signal-set integration watch-list (this topic IS the W4 resolution mechanism). The cross-axis failure cascade pattern per `arch/axis-interactions.md` §3.4 is the structural reason quality-gate Surface is single-layer cumulative observability (multi-class Surface per-axis would lose cross-axis cumulative observability)** |

## 8. Substrate-internal vs skill-side audit emission

**N/A** — per Pattern A template `MAINTENANCE.md` §8 conditional applicability rule: §8 is substrate-specific (substrate registers MCP audit gate per `arch/substrate.md` §8; substrate has dual-emission paths — substrate-internal direct + skill-side via MCP gate — to resolve MCP-gate-circularity). Quality-gate does not register the MCP audit gate; quality-gate emits via audit Surface §A skill-side ONLY (parallel to adapter §8 N/A precedent + sparring §8 skill-side-only). Quality-gate has no circularity issue and no dual-emission framing to discuss — gate-fired events emit via MCP audit gate (skill-side) only per Surface §E (audit emission).

Audit-trail-as-state-store: gate state events (`gate_state_persisted` / `gate_state_restored`) are skill-side emissions via MCP gate per audit Surface §A; gate state-restore reads via audit Surface §C query API. NO separate gate-state-store dual-write — single-write architecture preserved per `arch/audit.md` §10 audit-trail-as-canonical-source.

## 9. Cardinality + lifecycle

Quality-gate follows singular-per-workspace cardinality with shape-mediated selection — distinct from substrate's singular-per-workspace + workspace-mediated selection per `arch/substrate.md` §9 + adapter's multi-instance + workspace-mediated bindings list per `arch/adapter.md` §9. Per Pattern A template `MAINTENANCE.md` §9 common-required section.

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Quality-gate Implementations per workspace | 1 | Shape-mediated selection per shape policy bundle declaration; framework-level 1:1 with workspace per `glossary/quality-gate.md` Cardinality |
| Running Instance per workspace | 1 | Bound at workspace boot; one active gate impl |
| Implementations per Framework C catalog | N (current 3 + extensible) | Multiple distributable definitions; current set: practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-shape-gate; research-lab-shape-gate preliminary at second-shape productization per W1 |
| gate-firing events per workspace lifetime | N | Per-checkpoint events (pre_send / pre_claim_finalization / etc.); event-triggered + periodic/threshold-triggered classes per Surface §A two-class checkpoint taxonomy |

### Lifecycle ownership

- **Creator**: framework-runtime (workspace activation orchestrator) — instantiates Implementation class per shape policy bundle's gate-impl declaration at workspace boot
- **Owner**: workspace deployment runtime (Owner B scope membership)
- **Destroyer**: framework-runtime at workspace shutdown (or process termination)

### Mutability

- **Configuration immutable across single workspace boot** (gate-impl loaded at boot per shape policy bundle declaration; immutable until next boot; gate-impl re-binding requires shape change per §5 re-binding semantics)
- **Runtime state evolves during gate lifetime** (signals ingested; thresholds evaluated; interventions dispatched; gate-fired events emitted) — for stateful impls, state persisted via `gate_state_persisted` events per Surface §F audit-trail-as-state-store reframe
- **Gate-active vs gate-firing distinction**: gate-active is workspace-lifetime state (post-boot-phase-4 per §10); gate-firing is per-checkpoint event lifecycle within gate-active. Distinct lifecycle states; gate-active enables gate-firing but they are not the same lifecycle moment.

### Cross-session persistence

Per Surface §F state management (audit-trail-as-state-store reframe): stateful impls persist state IN audit-trail via `gate_state_persisted` events (no separate store); stateless impls have no persistence. Cross-deployment portability composes via audit-trail portability per `arch/audit.md` §G external-format export — gate state events are first-class in audit-trail; cross-deployment migration preserves gate state per audit-trail integrity invariants. Resolves W3 watch-list cross-deployment gate-state portability mechanism per `arch/practitioner.md` W1 + `arch/scope-model.md` W1+W2 + `arch/substrate.md` §F + `arch/audit.md` §G.

## 10. Boot + shutdown phase ordering (architectural-level)

The quality-gate has explicit boot phase + shutdown phase with ordered stages (parallel to substrate §10 + audit §10 + sparring §10 mechanism-class shutdown ordering). Ordering is architectural commitment — deviations break gate-state integrity invariants. Canonical step-by-step composite ordering across audit + substrate + adapter + sparring + quality-gate lives in `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection (REQUIRES amendment per this topic lock — adds gate-phase 1-4 after substrate-phase 5 + corresponding shutdown ordering).

### Boot sequence (architectural ordering)

**Precondition**: audit-phase 1-3 ready (audit Surface available for gate emission per `arch/audit.md` §10 boot-before-substrate ordering); substrate-phase 1-5 complete (specialists registered → axis-1 mechanisms operational; sparring sub-mechanisms via skills → axis-2 observability per `arch/sparring.md` §4; per-claim attestation chain available → axis-3 observability per `arch/claim-defensibility.md` §3) so that gate has all 3 axes of observability ready before gate-phase 1.

1. **gate-phase 1**: Gate Implementation instantiates per shape policy bundle declaration (`gate = await ChosenGate.from_shape_policy(shape_policy)` per shape-mediated selection per §5)
2. **gate-phase 2**: Gate state-restore from audit-trail (stateful impls reads prior `gate_state_persisted` events via audit Surface §C query API per audit-trail-as-state-store reframe; reconstructs cumulative engagement signals across session/work-unit context; emits `gate_state_restored` event upon completion)
3. **gate-phase 3**: Gate registers checkpoint-firing handlers (subscribes to per-axis observability hooks per `arch/axis-interactions.md` §7 per-axis observability hook signal-set; checkpoint subscriptions for event-triggered + periodic/threshold-triggered classes per Surface §A two-class checkpoint taxonomy)
4. **gate-phase 4**: Gate emits `gate_active` event via audit Surface §A; gate ready to fire (per gate-firing-vs-gate-active lifecycle distinction: gate-active is workspace-lifetime state from this point until shutdown; gate-firing is per-checkpoint event lifecycle within gate-active)

### Shutdown sequence (architectural ordering)

Gate shuts down AFTER substrate but BEFORE audit storage realization (parallel to sparring §10 mechanism-class shutdown ordering — see `ARCHITECTURE.md` §6 composite shutdown step 7 mechanism-class shutdown). Gate releases its own runtime resources; gate state-persistence flushes via `gate_state_persisted` event emission to audit Surface §A; audit storage realization shutdown LAST flushes gate state events to disk per audit §10 shutdown.

1. **gate-shutdown 1**: Gate emits final drift report event (`gate_session_summary` or per-impl shape; e.g., personal-OS-shape-gate periodic drift-check report at session_end checkpoint)
2. **gate-shutdown 2**: Gate state persistence — stateful impls flush cumulative signals via `gate_state_persisted` event emission to audit Surface §A (preserves cross-deployment portability via audit-trail composition + W3 cross-deployment gate-state portability)
3. **gate-shutdown 3**: Gate unsubscribes from observability hooks (substrate Surface §B telemetry hooks; audit Surface §C query subscriptions; sparring sub-mechanism event-emission subscriptions per `arch/sparring.md` §4)
4. **gate-shutdown 4**: Gate shutdown returns; audit storage realization shutdown follows per `arch/audit.md` §10 shutdown steps 4-7 (drains pending events including gate state events; flushes audit-trail to storage; verifies hash-chain integrity; emits `audit_trail_integrity_verified` final event)

### Cross-axis dependency (cross-axis composite boot integration per axis-interactions §3.5)

Gate consumes per-axis observability — all 3 axes operational + AuditEvent schema + audit Surface ready before gate-phase 1. Per `arch/axis-interactions.md` §3.5 cross-axis composite boot integration: audit-phase 1-3 axis-3 evidence layer ready BEFORE substrate-phase 1-5 axes 1+2 activate; gate-phase 1-4 follows substrate-phase 5 `boot_complete` per cross-axis cumulative observability requirement (gate cannot evaluate cross-axis signals if any axis observability is not yet operational).

**Invariant preserved**: gate is operational AFTER all 3 axes have operational observability (substrate-phase 5 `boot_complete` per `arch/substrate.md` §10 boot step 8 → gate-phase 1) AND gate state events are persisted in audit-trail BEFORE workspace shutdown completes (gate-shutdown 2 `gate_state_persisted` flush → audit storage realization shutdown LAST per `arch/audit.md` §10 shutdown step 4-7).

Boot timing: gate-phase 1 fires AFTER substrate-phase 5 `boot_complete` (NOT substrate-phase 4 specialist registration) — gate consumes axis-1 observability (workflow_instance phase transitions emit events requiring specialists + adapter bindings); only complete at substrate-phase 5 per cross-axis cumulative observability requirement.

## 11. Quality-gate error categories (architectural-level)

Quality-gate operations may fail in named architectural categories (parallel to substrate §11 + adapter §11). Each Implementation maps native errors to common categories.

| Category | Architectural meaning |
|---|---|
| `GateUnreachable` | Gate impl unreachable; per-shape fail-closed/open semantics determines downstream behavior |
| `SignalIngestionFailure` | Per-axis signal ingestion failure (substrate Surface §B telemetry hook unreachable; audit Surface §C query API failure; sparring sub-mechanism event-emission unreachable) |
| `SignalEvaluationFailure` | Threshold evaluation failure (per-shape threshold-set declaration ill-formed; signal-set incomplete for evaluation) |
| `InterventionDispatchFailure` | Intervention mechanics failure (friction not displayed; nudge not delivered; block not enforced via substrate Surface §C); per-shape escalation semantics determines behavior |
| `GateStateRestoreFailure` | Boot-time state-restore failure for stateful impls (audit-trail integrity violation; missing prior `gate_state_persisted` event; per-shape continuation semantics — practitioner-shape fail-closed; autonomous-business fail-open with alert; personal-OS fail-open) |
| `EventEmissionFailure` | Gate-fired event emission failure; composes with audit Surface §11 error categories per `arch/audit.md` §11 |

### Per-shape error semantics

Per `glossary/quality-gate.md` Per-shape implementations row:

- **practitioner-shape-gate**: fail-closed (defensibility-critical; gate failures must surface to practitioner; no silent degradation; especially axis-3 attestation moments where rubber-stamping risk applies; parallel to practitioner-shape adapter fail-closed per `arch/adapter.md` §11 + practitioner-shape audit fail-closed per `arch/audit.md` §11)
- **autonomous-business-shape-gate**: fail-open with alert (continuity prioritized; alert on failure; gate may auto-recover after intervention dispatch failure)
- **personal-OS-shape-gate**: fail-open (lightweight; degradation acceptable; auto-retry with reduced verbosity)

Per-class Pydantic shape → Phase 6 spec (Mode 3) per §18 phase routing.

## 12. Transport variation + per-tier mapping

**N/A** — per Pattern A template `MAINTENANCE.md` §12 conditional applicability rule: §12 transport-variation is substrate-specific (MCP-transport-variation surfaces at substrate Surface §B per `arch/substrate.md` §12). Quality-gate is substrate-agnostic per `glossary/quality-gate.md` (gate runs ABOVE substrate per §10 boot ordering); gate Surface contracts themselves are transport-uniform — gate operates over substrate's telemetry hooks + audit Surface §C query API + sparring sub-mechanism event-emission flowing through substrate event-bus per `arch/substrate.md` §E. Transport choice is substrate-internal per substrate Surface §B per-impl support, not a quality-gate framework concern.

Per-impl tier-compatibility declared in §4 (Tier 1 / Tier 2 / Tier 3 compatibility per Implementation per §13), but Surface contracts themselves are transport-uniform. Parallel to adapter §12 N/A precedent (adapter operates over per-class transports declared per Implementation; transport choice is impl-internal per per-class Surface satisfaction).

## 13. Deployment-tier awareness

Quality-gate is aware of which deployment tier it runs at; per-Implementation `deployment_tier` compatibility is declared field (parallel to substrate §13 + adapter §4 deployment-tier compatibility per-impl declaration).

### Per-tier behavior in impl, NOT Surface

The Surface contract is tier-neutral — same Surface methods at all tiers (parallel to substrate §13 per-tier behavior in impl). Per-tier behavior variation lives in Implementation:

- **Tier 1 (local)**: solo practitioner / development; gate runs on practitioner's machine; full gate enforcement default; possible advisory-mode for development workflows (per-impl declares advisory-mode flag); single-tenant gate state
- **Tier 2 (cloud small-firm)**: small-firm hosted deployment; multi-user collaboration possible; full gate enforcement; multi-tenant gate state per tenant via session_id + actor_id discrimination (parallel to substrate §13 Tier 2 multi-tenant isolation)
- **Tier 3 (federated enterprise)**: enterprise multi-agent A2A platform; per-tenant isolation strict; gate state federation considerations (cross-link W3 cross-deployment portability per audit-trail composition)

### Multi-tenant gate state isolation (Tier 2+)

Per Tier 2+ multi-tenant deployment scenarios: gate state isolation via session_id + actor_id discrimination per `arch/substrate.md` §13 per-tier behavior. Per-tenant `gate_state_persisted` events scoped via session_id + actor_id; gate state-restore at boot reads tenant-scoped events via audit Surface §C query API. Per-tenant gate state federation considerations cross-link to W3 cross-deployment gate-state portability.

Gate-impl tier-compatibility declared per Implementation; workspace boot validates gate-impl tier-compatibility against deployment tier per §5 validation at workspace boot.

## 14. Cross-shape policy variation

Per Pattern A template `MAINTENANCE.md` §14 conditional applicability rule: §14 applies when protocol behavior is shape-policy-mediated. Quality-gate IS shape-policy-mediated by definition per `docs/decisions/quality-gate-scope-lock.md` Hybrid Option C — per-shape variation captured at Implementation aspect; mechanism-shaped Surface ensures cross-implementation observability + emission compatibility. **§14 is the PRIMARY conditional for quality-gate** (parallel to adapter §14 + sparring §14 mechanism-class precedents; quality-gate cross-shape policy variation IS the topic's shape-policy-mediation surface).

Resolves `arch/axis-interactions.md` §14 W4 quality-gate cross-axis signal-set integration watch-list (this section IS the W4 resolution mechanism); composes with `arch/axis-interactions.md` §8 6-row per-shape cross-axis activation matrix.

| Dimension | practitioner-shape | autonomous-business-shape | research-lab-shape (preliminary; per W1) | personal-OS-shape |
|---|---|---|---|---|
| **Gate firing checkpoints** | pre_send + pre_claim_finalization + per_edit + drift_audit (full enforcement) | autonomous-decision-checkpoints + budget-policy thresholds (drift_audit periodic) | pre_send + pre_claim_finalization + co-attestation checkpoints | session_end + drift_audit (light) |
| **Per-axis signal thresholds** | strict per-axis (axis-3 PRIMARY; rubber-stamping detection mandatory per `glossary/rubber-stamping.md`) | budget-policy substitutes per-claim (axis-2 PRIMARY; per `arch/audit.md` §14 action-level audit granularity) | strict + multi-author co-attestation thresholds (multi-practitioner per `arch/practitioner.md` §4 cardinality matrix research-lab N) | minimal advisory thresholds |
| **Intervention mechanics** | friction + nudge + block + practitioner attestation + re-engagement | programmatic-block + audit-only + budget-alert | friction + nudge + co-attestation requests + block | audit-only + drift-check report |
| **Error semantics** | fail-closed (defensibility-critical; parallel to practitioner-shape adapter §11 + audit §11) | fail-open with alert (continuity prioritized; parallel to autonomous-business adapter §11 + audit §11) | fail-closed (research output accountability-bearing; parallel to practitioner-shape pattern) | fail-open (lightweight; parallel to personal-OS adapter §11 + audit §11) |
| **State management** | stateful (cumulative engagement signals across session via audit-trail per audit-trail-as-state-store reframe) | stateless (per-checkpoint policy evaluation; no cumulative state) | stateful (multi-author engagement signals via audit-trail) | stateful but lightweight (drift-check accumulation via audit-trail) |
| **Per-shape failure-mode salience** | rubber-stamping CRITICAL deadline-pressure (axis-3 per `profiles/L5a-planner-pbs-schulz.md` lines 51-54 send-phase risk); answer-machine RISK regulatory transcription (axis-2 per `glossary/answer-machine-ai.md`); cross-link `arch/axis-interactions.md` §8 row 4 | category-collapse to feature-catalog (axis-1) when business automation overruns (per `arch/axis-interactions.md` §8 row 4 autonomous-business column) | answer-machine in literature review (axis-2 oracle-mode for consensus claims); rubber-stamping in collaborative attestation (multi-author signature drift) | tacked-on-AI default (axis-1 collapsed by default per `arch/axis-interactions.md` §8 row 4 personal-OS column) |

Per-shape salience cross-link: explicit cross-link at this row 6 between `arch/quality-gate.md` §14 + `arch/axis-interactions.md` §8 row 4+5 (per-shape failure-mode salience + per-shape category-collapse vulnerability) — gate's per-shape failure-mode salience IS the per-shape category-collapse vulnerability surface gate watches against.

Quality-gate primitives stay shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (Surface contracts + capability categories + checkpoint taxonomy + per-axis signal catalog structure + intervention dispatch are uniform across all shapes; per-shape variation lives at Implementation aspect declaring per-shape thresholds + intervention mechanics + error semantics + state mode + checkpoint activation).

## 15. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced here as forward-reference for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns; the ARCH topic deliberately stops at architectural-conceptual articulation per layered coverage observation in `decision-design-sharpening` v0.6.0+.

- **Per-impl extension Protocols pattern** (parallel to substrate §4 per-impl extension Protocols pattern): practitioner-shape-gate extension exposes practitioner-attestation-extension; autonomous-business-shape-gate extension exposes budget-policy-extension; personal-OS-shape-gate extension exposes drift-check reporting extension; research-lab-shape-gate extension at second-shape productization per W1
- **Specific observability signals + thresholds per axis**: Phase 6 spec lands per-axis signal-set + threshold semantics + diagnostic emission contract (resolves `arch/axis-interactions.md` §7 per-axis observability hook signal-set forward-reference)
- **Specific intervention mechanics**: friction patterns; nudge wording; block conditions specifics (per-shape variation specifics per §14 Implementation aspect)
- **Error-semantics specifics**: fail-closed vs fail-open thresholds; per-error-category recovery semantics per shape
- **Tier-awareness configuration specifics**: per-tier multi-tenant gate state isolation mechanics; per-tenant gate state federation (Tier 3) cross-link W3
- **Specialist DEFINITION manifest schema `gate_firing_requirements` field**: manifest schema field `gate_firing_requirements: optional` Phase 6 spec target; specialist DEFINITION may declare per-skill gate-firing requirements composing through specialist-skill primitive-cluster topic per `arch/specialist-skill.md`

These are per-implementation operational concerns — locked at Phase 6 implementation-start. ARCH topic explicitly does NOT lock these.

## 16. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| **W1** | Second-shape productization quality-gate variation (autonomous-business / personal-OS / research-lab concrete impls) | Second-shape design begins (autonomous-business OR personal-OS productization per BACKLOG shape-neutrality watch-list + `arch/scope-model.md` §14 W4 + `arch/axis-interactions.md` §14 W1) | Per-shape policy bundle declares gate-impl-id; concrete per-shape gate-impl satisfies Surface; per-shape extension Protocols pattern lands per Phase 6 spec; cross-link: BACKLOG "Shape-neutrality validation for second-shape productization" entry + `arch/axis-interactions.md` §14 W1 |
| **W2** | Per-axis observability hook signal-set + threshold-set evidence accumulation | Phase 1+ pioneer deployment data (per-axis signal capture mechanics + threshold tuning evidence) | Phase 6 spec lands per-axis observability hook signal-set + threshold semantics + diagnostic emission contract; resolves `arch/axis-interactions.md` §7 per-axis observability hook signal-set forward-reference Phase 6 spec target |
| **W3** | Cross-deployment gate-state portability via audit-trail composition | First cross-deployment claim ingestion deployment evidence (per `arch/practitioner.md` W1 + `arch/scope-model.md` W1+W2 + `arch/substrate.md` §F + `arch/audit.md` §G + `arch/axis-interactions.md` §14 W3) | Per-shape policy declares cross-deployment gate-state portability semantics; gate state events preserved across Owner B references per audit-trail integrity invariants per `arch/audit.md` §G external-format export; cross-link: `arch/practitioner.md` §14 W1 + `arch/scope-model.md` §14 W1+W2 + `arch/substrate.md` §F + `arch/audit.md` §G |
| **W4** | Quality-gate intervention efficacy empirical evidence (fail-closed vs fail-open per-shape thresholds; intervention mechanics efficacy by archetype) | Phase 1+ regulatory-challenge outcomes per `VISION.md` §Falsification criteria (axis-3 falsification: real defensibility events where audit-trail provided no benefit) | Per-shape threshold tuning + intervention mechanics tuning per Phase 1+ deployment data; falsification criteria signal feeds VISION update mechanism per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 anchored revision criteria; cross-link: `VISION.md` §Falsification criteria + `arch/axis-interactions.md` §14 W2 |

## 17. Decision-design provenance

This topic articulates quality-gate as Pattern A protocol with mechanism-shaped Surface per locked GLOSSARY entry + scope-lock DR Hybrid Option C verdict.

Provenance for this topic lives in DR + HANDOFF + git log per `MAINTENANCE.md` Lens 5 v0.2.2 provenance hygiene + per `coherence-audit` Lens 5. See `docs/decisions/quality-gate-arch-topic.md` §6 for sharpening provenance (canonical home).

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: quality-gate Surface stays shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz / planner-shape; per `profiles/L5a-planner-pbs-schulz.md` lines 51-71 axis engagement realities) reality grounds practitioner-shape-gate via cross-archetype illustration (planner / lawyer / researcher per `glossary/quality-gate.md` Cross-archetype illustration) NOT load-bearing pioneer specifics. Cross-archetype illustration in §2 + §14 anchors framework neutrality (planner / lawyer / researcher / autonomous-business operator / personal-OS knowledge worker).

**Pattern A topic-template-class FORMAL STABILITY achieved with three instances complete** (substrate anchor + adapter second + quality-gate third per per-pattern instance-driven trigger pattern per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`). Pattern A instances complete with Phase 3.6 close (3 of 3 — substrate anchor + adapter + quality-gate; this is the LAST Pattern A topic per Phase 3 ARCH catalog). 12+7 template extends WITHOUT variation across all three Pattern A instances; per-pattern conditional applicability differs per topic-instance discriminators (substrate 6 of 7 conditional applies; adapter 5 of 7 conditional applies; quality-gate 4 of 7 conditional applies — §10 + §11 + §13 + §14 apply per per-pattern conditional applicability rule).

## 18. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.6 | LOCKED; closes Phase 3.6 1 of 1 ARCH topic |
| Pydantic Protocol contract | 6 | Mode 3 spec; Surface category typing; GateError class hierarchy; supporting Pydantic types (CheckpointKind / InterventionKind / GateState / etc.) |
| Concrete quality-gate Implementations | 6 | practitioner-shape-gate full impl; autonomous-business-shape-gate full impl; personal-OS-shape-gate full impl; research-lab-shape-gate at second-shape productization per W1 |
| Per-axis observability hook signal-set spec | 6 | Phase 6 spec lands per-axis signal-set + threshold semantics + diagnostic emission contract (resolves `arch/axis-interactions.md` §7 per-axis observability hook signal-set forward-reference Phase 6 spec target per W2) |
| Cross-axis error catalog | 6 | Phase 6 spec lands cross-axis error catalog + recovery semantics + per-shape fail-closed vs fail-open declaration (resolves `arch/axis-interactions.md` §7 cross-axis error catalog forward-reference) |
| Per-shape threshold-set tuning | Phase 1+ | Pioneer deployment data per W2 + W4 watch-list |
| Specialist DEFINITION manifest schema `gate_firing_requirements` field | 6 | Phase 6 spec; specialist DEFINITION manifest schema field for per-skill gate-firing; composes through specialist-skill primitive-cluster topic per `arch/specialist-skill.md` |
| Pre-implementation operational concerns (per-impl extension Protocols / observability signals / intervention mechanics / error-semantics / tier-awareness / specialist manifest field) | 6 | Pre-implementation sharpening at Phase 6 implementation-start; per-implementation-sharpening skill applies |
| Per-shape extension Protocols (PractitionerShapeGateExtension / AutonomousBusinessShapeGateExtension / PersonalOSShapeGateExtension) | 6 | Designed alongside Quality-gate Protocol; each impl satisfies Surface + declares per-shape extension Protocols |
| Cross-deployment gate-state portability mechanics | 5+ | Per W3 watch-list; awaits first cross-deployment claim ingestion deployment evidence |
| Second-shape productization concrete impls | 3.5+ | Per W1 watch-list; awaits second-shape design begin signal; cross-link to BACKLOG shape-neutrality watch-list |

## 19. Cross-references

- **GLOSSARY** (20+ canonical entries): `quality-gate` (canonical PRIMITIVE Pattern A entry; primary anchor); `protocol (architectural)` (Pattern A meta-primitive); `category-collapse` (cross-axis force quality-gate watches against); `intertwining (axis 1)` / `sparring (axis 2)` / `authorship preservation (axis 3)` (3 VISION axes per-axis composition); `co-worker` (axis-1 relational frame); `intertwined-ai` / `tacked-on-ai` (axis-1 success / failure modes); `answer-machine-ai` / `oracle-ai` / `validator-ai` (axis-2 failure modes per Vivienne Ming research); `engaged-authorship` (axis-3 success mode; gate's axis-3 observability source); `rubber-stamping` (axis-3 failure mode at attestation phase; gate's axis-3 detection target); `defensibility` (axis-3 operational test; gate's axis-3 intervention applies); `authority-binding` (cross-axis attribution chain; gate verifies authority-binding completeness as gate condition); `claim` (gate fires per-claim at finalization); `workflow` / `work-unit` (workflow_instance + work-unit observability sources); `session` (session boundary checkpoint source); `event` (gate emits gate-fired events to audit-trail); `actor` (gate Running Instance is `actor_kind: ai_runtime` at intervention dispatch); `framework` / `mechanism` / `Framework C scope` / `Owner B scope` / `workspace` / `shape` / `specialist` / `skill` / `practitioner` / `substrate` / `adapter`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (make-wrong-shapes-impossible — gate-coupling impossible-by-construction at Surface level; structural enforcement via Pattern A pluggability); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (pattern-vs-instance — gate stays shape-neutral; per-shape variation at Implementation aspect; pioneer reality grounds practitioner-shape-gate via cross-archetype illustration NOT load-bearing pioneer specifics); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 (preliminary-lock — VISION axes anchored; gate primitives preliminary-locked); `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment workspace.md authoring happens at deployment-instance; not framework repo); `ARCHITECTURE.md` §6 cross-cutting principles "AI as runtime" + "LLM-instruction tightness for Mode 1 markdown layer" + "Workspace boot + shutdown composite sequence" subsection (gate-phase 1-4 amendment for cross-axis composite boot integration per §10); `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 4 (cascade-prevention; greenfield-draft + minimize-embedded + cascade-pass + foundation-first); Discipline 8 (foundation-up workflow ordering — quality-gate is third + final Pattern A instance + Phase 3.6 sole topic); Discipline 10 (greenfield-evaluation of archived material — NO archive territory per §17 archived sources NONE)
- **Profiles validated**: `G-composability-gate.md` (Cluster A multi-mode consumption — gate-impl distributable per Framework C catalog supports consulting / internal-firm-reuse / OSS / marketplace-future / backup-migration consumption modes; per-shape gate-impl distributable; cross-substrate compatibility — gate substrate-agnostic per `glossary/quality-gate.md` ensures gate-impl portable across substrates); `L5a-planner-pbs-schulz.md` (Cluster B+C deployer-of-self + practitioner-user — pioneer reality grounds practitioner-shape-gate via deadline-pressure rubber-stamping risk lines 51-54 send-phase + answer-machine extraction risk regulatory transcription axis-2; planner archetype hybrid moments line 67 "occasional rubber-stamp risk during deadline-pressure send (axis 3 risk)" validates gate fires at pre_send checkpoint per Surface §A); `L8-auditor-reviewer-posthoc.md` (Cluster D auditor — defensibility verification post-hoc engagement; gate's axis-3 intervention applies defensibility test at attestation moments per `glossary/defensibility.md`; per-claim attestation chain reconstructable via audit-trail per `arch/audit.md` §C query API); Cluster A producer transitively-satisfied via specialist-skill §4 (specialist DEFINITION may declare per-skill gate-firing requirements via manifest schema field) + shape policy bundle declaring gate-impl-id (per `glossary/shape.md`) + deployment template
- **ARCH topics composing with quality-gate**: `arch/substrate.md` (Pattern A; observability infrastructure — Surface §B telemetry hooks + §C permission flow at intervention `block` + §F session/context + §G specialist registration mediates skill-side gate emission; substrate-phase 1-5 boot precondition for gate-phase 1-4 per §10); `arch/adapter.md` (Pattern A; orthogonal mechanism category — gate fires at adapter-bounded actions e.g., pre_send fires before email-adapter dispatches); `arch/sparring.md` (Pattern D mechanism class; observability source axis-2 — sparring sub-mechanism event-emissions feed Surface §B axis-2 signal catalog); `arch/audit.md` (Pattern D mechanism class; gate emits via Surface §A; gate state-restore reads via Surface §C per audit-trail-as-state-store reframe; gate-phase boot/shutdown composes with audit §10 boot-before-substrate / shutdown-after-substrate ordering; per-shape audit emission granularity per §14 composes with gate per-shape variation); `arch/specialist-skill.md` (per-skill gate-firing requirements via manifest schema field; specialist DEFINITION manifest schema `gate_firing_requirements: optional` Phase 6 spec target; reciprocal symmetry already locked between `glossary/specialist.md` Composes-with quality-gate + `glossary/quality-gate.md` Composes-with specialist); `arch/practitioner.md` (HITL approval moments via substrate Surface §C — practitioner-RECORD identity for gate intervention authority at `block` decision per Surface §D; practitioner is engagement subject for axis-3 attestation events feeding gate's axis-3 signal catalog); `arch/workflow-work-unit.md` (workflow_instance + work-unit observability sources — workflow_phase_transition checkpoint event-triggered per Surface §A two-class checkpoint taxonomy); `arch/claim-defensibility.md` (per-claim attestation chain IS gate's axis-3 observability source per §3 + per-claim defensibility composes work-unit defensibility — gate fires per-claim at finalization per shape policy granularity); `arch/scope-model.md` (cross-cutting integrator scope-categorization composition — gate Implementation = Framework C distributable per shape; gate Running Instance = Owner B workspace-bound; per §4 authority-binding placement pattern parallel + §18 per-primitive composition table quality-gate row); `arch/axis-interactions.md` (cross-axis category-collapse counter-mechanism per §4.3; resolves §7 per-axis observability hook signal-set + §14 W4 quality-gate cross-axis signal-set integration forward-references; the cross-axis failure cascade pattern per §3.4 is structural reason gate Surface is single-layer cumulative observability)
- **Phase 6 spec target**: `docs/specs/quality-gate.md` (Pydantic Protocol + per-impl spec + per-axis observability hook signal-set spec + cross-axis error catalog spec + per-impl extension Protocols)
- **Archived sources**: NONE — per cross-cutting integrator + Pattern A precedent (substrate cited 3 archived sources; adapter cited none; quality-gate cited none — per topic-specific). Quality-gate foundations are `docs/decisions/quality-gate-scope-lock.md` (LOCKED Phase 2 NOT archive) + `glossary/quality-gate.md` (LOCKED Phase 2 GLOSSARY foundational vocabulary) + 9 prior locked Phase 3.4 + Phase 3.5 ARCH topics; not archive territory per `disciplines/10-greenfield-evaluation.md` greenfield-evaluation rule.
