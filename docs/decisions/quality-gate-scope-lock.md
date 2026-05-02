# DR: quality-gate scope-lock (type + composition + per-shape variation + intervention shape)

**Status**: ACCEPTED (scope-lock; full mechanism design pending Phase 3.6)
**Locked**: session 16 (2026-05-02)
**Sharpening**: 2-round pattern (Round 1 full monty + Round 2 user-triggered) under G + multi-axis + D gate disciplines
**Phase**: pre-Phase-3.6 scope-lock (Phase 3.1 territory; brought forward to inform Phase 3.3-3.5 work)

## Decision

`quality-gate` is a **named architectural Protocol** (Pattern A pluggable subsystem) **with mechanism-shaped Surface**:
- **Surface**: common observability + emission contract; per-axis-failure-mode signal catalog
- **Implementations**: structural variation per shape (`practitioner-shape-gate` / `autonomous-business-shape-gate` / `personal-OS-shape-gate` / extensible)
- **Selection**: shape declares which Pattern A implementation activates
- **Lifecycle per implementation**: stateful vs stateless choice
- **Per-shape error semantics**: fail-closed (practitioner-shape; defensibility-critical) / fail-open with alert (autonomous-business) / fail-open (personal-OS)
- **Naming**: distinct from G/D validation gates (architectural-decision-time per `profiles/INDEX.md`); quality-gate is runtime

## Context

Earlier in session 16, quality-gate concept surfaced as exploratory draft (`drafts/quality-gate.md`) while building generic `sharpen` skill. Question: could sharpening discipline graduate to product-side runtime mechanism?

After locking category collapse + axis-2 failure mode trio + rubber-stamping in GLOSSARY (session 16 Phase 2 completion), quality-gate's architectural role became precise: monitor for category-collapse manifestations across all 3 axes; surface drift signals; intervene per shape policy.

User question (mid-session): scope-lock now (Phase 3.6 prerequisite) or wait for Phase 3.6 proper? Resolved: scope-lock NOW because Phase 3.3 (per-mechanism) and Phase 3.4 (per-protocol) need to know if quality-gate is mechanism or Pattern A protocol — placement decision affects 3.3-3.4 work.

## Adoption options considered

**Q1 type classification**:
- **A**: Mechanism (atomic interface contract; per-policy-only variation across shapes)
- **B**: Pattern A protocol (pluggable subsystem; Surface + implementations + selection)
- **C (CHOSEN)**: Hybrid — Pattern A protocol with mechanism-shaped Surface

## Rationale for C (Hybrid)

**Per-shape gate behavior is structurally different**, not just configurationally:
- practitioner-shape: full engagement procedure (sparring composition + friction + practitioner attestation + re-engagement nudges)
- autonomous-business-shape: programmatic policy-evaluation (threshold-based; no human-in-loop; audit-only intervention)
- personal-OS-shape: light gate (minimal friction; periodic drift-check; audit-only)

Different code paths, not just config knobs → Pattern A pluggability captures structural variation. Mechanism-with-config can't.

But pure Pattern A loses cross-implementation observability/emission compatibility. Hybrid: mechanism-shaped Surface ensures all implementations emit comparable signals + audit events; implementation variation per-shape.

## Why not other options

**Option A (pure mechanism)**: per-shape variation is structural; mechanism with config can't capture different code paths. Would force shape policies to encode structurally-different behaviors as configuration → smell.

**Option B (pure Pattern A protocol)**: without mechanism-shaped Surface, each implementation invents its own observability/emission contract → loses cross-implementation compatibility (e.g., L8 evaluator can't reason about gate outputs uniformly across deployments).

## Refinements applied (Round 2 expansions)

| ID | Refinement | Status |
|---|---|---|
| E1 | Naming-collision disambiguation (quality-gate vs G/D gates) | Applied to GLOSSARY canonical |
| E2 | Lifecycle per-implementation (stateful vs stateless choice) | Applied to GLOSSARY canonical |
| E3 | Composition expanded — intertwining (axis 1) + co-worker | Applied to composes-with table |
| E4 | Per-axis-failure-mode signals as Surface contract | Flag for 3.6 schema |
| E5 | Boot / shutdown / error semantics — fail-closed-vs-open per implementation | Applied to lifecycle section |
| E6 | Authority-binding for intervention reinforced | Applied (already in Round 1) |
| E7 | Tier-awareness per implementation | Flag for 3.6 schema |

## REVISION-grade stress-test

**R1 (REJECTED)**: rename quality-gate to avoid "gate" collision with G/D validation gates? Tested alternatives ("checkpoint-gate", "engagement-gate", "drift-gate") — none sharper than "quality-gate"; established in drafts + BACKLOG; renaming = cascade work without cleaner name. E1 disambiguation note suffices.

## Composition with existing architecture

| Existing primitive | Composition |
|---|---|
| `protocol (architectural)` | Pattern A meta-primitive; quality-gate is one named Protocol |
| `category collapse` | Force quality-gate watches against |
| `intertwining (axis 1)` | State quality-gate guards against degradation toward tacked-on |
| `sparring (axis 2)` | Protocol whose runtime outputs feed quality-gate observability for axis-2 detection |
| `authorship preservation (axis 3)` | Axis quality-gate tests at attestation moments via defensibility check |
| `defensibility` | Gate's axis-3 intervention applies defensibility test |
| Axis-failure modes (`tacked-on AI / answer-machine / oracle / validator AI / rubber-stamping`) | Manifestations gate detects per axis |
| `co-worker` | Relational frame quality-gate guards against collapse |
| `claim` | Gate fires per-claim at finalization (per shape policy) |
| `workflow_instance` (when codified) | Gate fires at workflow phase transitions; observability source |
| `session` | Gate fires at session boundaries; cumulative engagement signal source |
| `event` | Gate emits gate-fired events to audit trail |
| `audit` protocol | Gate emissions follow audit protocol granularity per shape |
| `mechanism` (audit-emission, authority-binding) | Composes for output emission + intervention authority |
| `shape` | Shape declares which Pattern A gate implementation activates |
| `specialist` | Specialist may declare per-skill gate-firing requirements |

## Defers (D-gate-validated; Phase 3.6 schema territory)

| Defer | Awaited signal | Reason valid |
|---|---|---|
| Surface specification specifics (method set; field types; emission schema) | Phase 3.6 ARCH topic | Schema-detail; mental modeling resolved WHAT (Pattern A protocol); HOW is 3.6 |
| Per-implementation detail (practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-shape-gate) | Phase 3.6 ARCH topic + per-shape policy work | Implementation specifics |
| Specific observability signals + thresholds | Phase 3.6 + Phase 3.5 workflow-mechanics + claim-mechanics outputs | Depends on per-primitive detail outputs |
| Specific intervention mechanics (friction patterns; nudge wording; block conditions) | Phase 3.6 ARCH topic | Implementation-specific |
| Error-semantics specifics (fail-closed vs fail-open thresholds) | Phase 3.6 ARCH topic | Per-implementation choice |
| Tier-awareness configuration | Phase 3.6 + per-shape policy work | Deployment-tier-specific |

D Gate verdict: all defers genuine schema-detail territory (HOW), not architectural-decision (WHAT). All defers valid.

## Constraints flowing

This decision flows constraints into:
- **Phase 3.4** per-architectural-Protocol detail (quality-gate joins Substrate / Adapter / Sparring / Audit / Coordination / Trust / Time as Pattern A protocols; Phase 3.4 may include quality-gate Surface + cross-protocol composition concerns)
- **Phase 3.6** quality-gate full ARCH topic (Surface specification + per-implementation detail + per-axis signal catalog + intervention mechanics + error semantics + tier-awareness)
- **Phase 3.5** workflow-mechanics + claim-mechanics + defensibility-mechanics (these primitives provide quality-gate's observability inputs; their schema influences gate's signal definitions)
- **Phase 3.3** per-mechanism detail (audit-emission + authority-binding mechanisms compose with quality-gate; their detail informs gate's emission + intervention)
- **Phase 6** workspace serialization spec (quality-gate state may be part of workspace state; gate-fired events part of audit-trail portability)

## Files touched

- `GLOSSARY.md` quality-gate entry (NEW; Pattern A primitive)
- `GLOSSARY.md` TOC §5 Pattern A primitives (quality-gate added)
- `GLOSSARY.md` framework entry's architectural-protocols list (quality-gate added)
- `ARCHITECTURE.md` Locked architectural decisions section (quality-gate scope-lock added; Phase 3.6 entry updated)
- `BACKLOG.md` Phase 3.6 entry (scope-lock complete; full design Phase 3.6)
- `drafts/quality-gate.md` (status updated to scope-locked)

## Revisit triggers

This DR should be revisited if:
- Phase 3.6 full design surfaces operational concerns not anticipated at scope-lock time
- Second-shape productization (autonomous-business OR personal-OS) reveals Surface needs adjustment
- Pioneer-deployment data shows Pattern A pluggability is over- or under-specified
- New named Protocol surfaces that subsumes quality-gate's role (unlikely)

## Sharpening rounds metadata

- **Round 1**: AI full monty — 3 adoption options + 11 stress tests + position committed (Option C: Pattern A protocol with mechanism-shaped Surface)
- **Round 2**: USER-TRIGGERED — 7 EXPANSIONS applied (E1-E7) + 1 REVISION-candidate rejected (R1 rename)
- **Self-check**: STABLE; 0 architectural REVISIONS; all findings EXPANSIONS or rejected manufactured criticism

Total: 2 rounds. Per `feedback_pre_decision_sharpening.md` 2-round sweet spot empirical pattern. Narrow architectural surface (single primitive scope-lock) → 2 rounds sufficient.
