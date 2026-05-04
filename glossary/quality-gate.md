---
entry: quality-gate
class: PRIMITIVE
layer: framework-mechanism
axis: cross-axis
vision_usage: derived
---

# quality-gate

- **Class**: PRIMITIVE (named architectural Protocol; Pattern A pluggable subsystem with mechanism-shaped Surface)
- **Layer**: framework-mechanism (runtime mechanism)
- **Axis**: cross-axis (gate watches for category-collapse manifestations across all 3 axes)
- **VISION usage**: derived (composes with axes 1/2/3 + category collapse + axis-failure modes; not directly named in VISION)

**Naming disambiguation**: `quality-gate` (this entry) is distinct from `G Composability Gate` + `D Defer Gate` (in `profiles/INDEX.md`):
- G + D gates fire DURING architectural decisions (design-time; validate decisions)
- quality-gate fires DURING deployment work (run-time; validates engagement-quality at checkpoints)

Both involve "gate" but operate at different layers + lifecycle moments. Disambiguate by context.

**Canonical**: A Pattern A architectural Protocol that fires at runtime checkpoints (pre-send, pre-claim-finalization, pre-decision-lock, per-edit, drift-audit) to monitor for category-collapse manifestations across all three VISION axes, surface drift signals, and intervene with friction / re-engagement nudges / blocks per shape policy. Pattern A pluggability allows structural variation per shape; mechanism-shaped Surface ensures cross-implementation observability + emission compatibility.

**What it is**: A runtime mechanism converting category-collapse-resistance from ENABLED architecturally (sparring sub-mechanisms exist) to ENFORCED at gate-firing moments. Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: structural enforcement over conventional reliance on practitioner discipline. Quality-gate IS the structural counter to category-collapse drift at checkpoint moments.

**Per-shape implementations** (Pattern A pluggability):
- `practitioner-shape-gate`: full engagement procedure (sparring composition + friction + practitioner attestation + re-engagement nudges); fail-closed; stateful (cumulative engagement signals across session)
- `autonomous-business-shape-gate`: programmatic policy gate (threshold-based; no human-in-loop; audit-only intervention or programmatic block); fail-open with alert; stateless
- `personal-OS-shape-gate`: light gate (minimal friction; periodic drift-check report; audit-only); fail-open; stateful but lightweight
- Extensible: custom shapes implement own conforming to Surface

**What it is NOT**:
- Not a sparring sub-mechanism — sparring fires DURING work production (axis-2 runtime mode); gate fires AT CHECKPOINTS (event-triggered cross-axis)
- Not an audit emission — audit governs emission granularity per shape; gate is active intervention layer that emits to audit
- Not workflow-required — gate fires on ad-hoc work too (per claim emissions + session boundaries; workflow_instance is one observability source, not only)
- Not a single mechanism — Pattern A pluggability captures structural variation across shapes
- Not advisory — structural enforcement at gate-firing moments
- Not architectural-decision-time validation — runtime mechanism (G + D gates handle architectural-decision-time per `profiles/INDEX.md`)

**Cross-archetype illustration**:
- **Practitioner-shape (planner)**: gate fires at Begründung-finalization + per-claim attestation; engagement signals measured (sparring participation, counter-argument engagement, source-grounding completeness); intervention if rubber-stamping detected (axis-3 manifestation)
- **Practitioner-shape (lawyer)**: gate fires at brief-finalization + per-citation engagement check; intervention on legal-claim insufficient-engagement (axis-2 oracle/answer-machine manifestations)
- **Practitioner-shape (researcher)**: gate fires at manuscript-section-finalization + per-claim methodology-defensibility; intervention on rubber-stamping or oracle-mode acceptance
- **Autonomous-business-shape (operator)**: programmatic gate at decision-checkpoints; threshold-based policy evaluation; no human friction; audit-only or programmatic block
- **Personal-OS-shape (knowledge worker)**: light gate at session-end with drift-check report; audit-only

**Boundary test**: Three questions:
1. Is this a runtime mechanism that fires at deployment-work checkpoints (not architectural decisions)? → it's a quality-gate
2. Does it watch for category-collapse manifestations across axes? → it's a quality-gate
3. Is this a continuous runtime mode (not event-triggered checkpoint)? → it's `sparring (axis 2)` not quality-gate

**Composes with**:
- [protocol (architectural)](protocol-architectural.md) — Pattern A meta-primitive; quality-gate is one named Protocol
- [category collapse](category-collapse.md) — force quality-gate watches against
- [intertwining (axis 1)](intertwining.md) — state quality-gate guards against degradation toward tacked-on
- [sparring (axis 2)](sparring.md) — protocol whose runtime outputs feed quality-gate observability for axis-2 detection
- [authorship preservation (axis 3)](authorship-preservation.md) — axis quality-gate tests at attestation moments via defensibility check
- [defensibility](defensibility.md) — gate's axis-3 intervention applies defensibility test
- [engaged authorship](engaged-authorship.md) — gate's axis-3 observability source; engaged-authorship's structural signals (production-phase events + per-claim attestation events + quality signals) feed quality-gate's drift detection at attestation moments
- [tacked-on AI](tacked-on-ai.md) / [answer-machine AI](answer-machine-ai.md) / [oracle AI](oracle-ai.md) / [validator AI](validator-ai.md) / [rubber-stamping](rubber-stamping.md) — axis-failure mode manifestations gate detects per axis
- [co-worker](co-worker.md) — relational frame quality-gate guards against collapse
- [claim](claim.md) — gate fires per-claim at finalization (per shape policy granularity)
- `workflow_instance` (when codified) — gate fires at workflow phase transitions; observability source
- [session](session.md) — gate fires at session boundaries; cumulative engagement signal source
- [event](event.md) — gate emits gate-fired events to audit trail
- `audit` protocol — gate emissions follow audit protocol granularity per shape
- [authority-binding](authority-binding.md) — quality-gate may verify authority-binding completeness as a gate condition (e.g., refuse send if authority-binding chain incomplete per shape policy); intervention authority composes with the binding mechanism
- [mechanism](mechanism.md) (audit-emission, authority-binding) — composes for output emission + intervention authority
- [shape](shape.md) — shape declares which Pattern A gate implementation activates
- [specialist](specialist.md) — specialist may declare per-skill gate-firing requirements

**Cardinality + lifecycle**:

**Cardinality**: 1 active gate implementation per workspace (selected via shape policy declaration).

**Lifecycle**:
- **Boot**: gate becomes active at workspace deployment; shape declares which Pattern A implementation activates
- **Per-firing**: gate fires at checkpoint events (per shape policy); emits gate-fired event to audit trail; evaluates engagement signals; triggers intervention if threshold crossed
- **Stateful vs stateless**: per-implementation choice (practitioner-shape stateful with cumulative signals; autonomous-business-shape stateless per-checkpoint; personal-OS-shape stateful but lightweight)
- **Shutdown**: gate emits final drift report at workspace teardown; closes audit context
- **Error semantics**: per-implementation (fail-closed for defensibility-critical practitioner-shape; fail-open with alert for autonomous-business; fail-open for personal-OS)

**Source**:
- `docs/decisions/quality-gate-scope-lock.md` (decision rationale + sharpening rounds metadata; original exploratory draft removed on graduation per drafts discipline)
- VISION (`VISION.md`): not directly named; derives from category-collapse + axis-failure-mode framings + `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 structural-enforcement principle
- Locked GLOSSARY entries: [category collapse](category-collapse.md) / [protocol (architectural)](protocol-architectural.md) / [sparring (axis 2)](sparring.md) / axis-failure modes / [claim](claim.md) / `workflow_instance` / [session](session.md) / [event](event.md)
- Synthesis: Pattern A protocol with mechanism-shaped Surface (hybrid resolution from Round 1 + Round 2 sharpening; structural variation per shape; mechanism-shaped Surface for cross-implementation compatibility)

**See**:
- [arch/quality-gate.md](../arch/quality-gate.md) — Pattern A 12+7 third instance LOCKED Phase 3.6; FORMAL STABILITY achieved 3 of 3 Pattern A instances; single-layer mechanism-shaped Surface 6 capability categories + 3 concrete Implementations + shape-mediated selection + cross-axis category-collapse counter-mechanism per `arch/axis-interactions.md` §4.3
- [arch/axis-interactions.md](../arch/axis-interactions.md) — quality-gate Pattern A as architectural counter-mechanism for category-collapse per §4.3 (gate fires at runtime checkpoints to monitor for category-collapse manifestations across all 3 VISION axes); cross-axis observability hook signal-set integration per §7 + §14 W4 (per-axis signals quality-gate consumes for category-collapse drift detection across axis-1 / axis-2 / axis-3); quality-gate ARCH topic Phase 3.6 LOCKED resolves §7 E2 + §14 W4 forward-references per `arch/quality-gate.md`
- `profiles/G-composability-gate.md` (DISTINCT — G is architectural-decision-time validation gate)
- `profiles/INDEX.md` D Gate section (DISTINCT — D is architectural-decision-time validation gate)
- [category collapse](category-collapse.md) (force quality-gate exists to resist)
- [sparring (axis 2)](sparring.md) / `audit` protocols (composing protocols)
- [protocol (architectural)](protocol-architectural.md) (Pattern A meta-primitive)
