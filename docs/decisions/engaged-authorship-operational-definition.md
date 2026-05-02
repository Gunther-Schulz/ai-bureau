# DR: engaged-authorship-operational-definition (DERIVED axis-3 success mode; two-phase composite)

**Status**: ACCEPTED (Phase 3.1 lock; closes 3.1)
**Locked**: session 16 (2026-05-02)
**Sharpening**: 2-round pattern (Round 1 full monty + Round 2 user-triggered) under G + multi-axis + profile-anchored + D gate disciplines + GLOSSARY back-check
**Phase**: 3.1 (open architectural questions; FINAL 3.1 item)

## Decision

`engaged authorship` is locked as a **DERIVED axis-3 success mode** with two-phase composite operational definition:

1. **Production-phase engagement** (axis-2-anchored): per-claim sparring participation observed via sparring-event emissions (counter-argument engagement, alternative-consideration, position-defense, source-grounding decisions, judgment-call overrides)
2. **Attestation-phase engagement** (axis-3-anchored): per-claim attestation event emitted at finalization (NOT whole-output sign-off)

**Both phases independent + both must structurally complete** for engaged-authorship to hold per claim. Per locked `rubber-stamping` entry: axis-2 failures and rubber-stamping are INDEPENDENT dimensions; both must be defended-against.

**Granularity**: per-claim per-version (revised claim = new engagement test cycle; v1 engagement doesn't carry forward to v2).

**Two layers of operationalization**:
- **Framework-level: PRESENCE** — Y/N event-existence test (per-claim production-phase event ≥1 + per-claim attestation event)
- **Shape-policy-level: QUALITY** — depth-of-engagement signals; quality-gate (Pattern A protocol) enforces per shape policy

**Framework-level enforcement** (per `feedback_wrong_shapes_impossible.md`):
- Events emit per-claim per-phase via audit-emission mechanism
- `quality-gate` detects missing signals; emits drift signals at attestation moments
- Per-shape intervention: practitioner-shape = friction/block (defensibility-critical; fail-closed); autonomous-business-shape = programmatic block; personal-OS-shape = audit-only

**Elevation to standalone DERIVED entry**: engaged authorship is load-bearing across `defensibility` (Condition #1), `authorship preservation`, `rubber-stamping`, `quality-gate`, `claim` entries. Standalone entry preserves canonical operational definition without bloating defensibility entry.

## Context

`defensibility` entry (locked Phase 2) names three structural conditions: (1) engaged authorship, (2) reconstructible reasoning chain, (3) source-grounded content. The latter two are operationalized via specific framework mechanisms with clear observable signals. **Engaged authorship's operational meaning was historically loose** — described as "practitioner participated; not rubber-stamped" without structural signal definition.

Phase 3.1 closing item: sharpen engaged authorship to operational definition with structural signals enabling framework-level enforcement (per make-wrong-shapes-impossible discipline).

Critical insight from locked `rubber-stamping` entry: axis-2 failures (production phase) and rubber-stamping (attestation phase) are INDEPENDENT dimensions. Both can occur; both must be defended against. This locks the two-phase composite shape — engaged authorship cannot be single-phase.

## Adoption options considered

- **A**: Engagement-as-sparring-interaction — production-phase sparring participation only (singular phase)
- **B**: Engagement-as-per-claim-attestation — attestation-phase per-claim event only (singular phase)
- **C (CHOSEN)**: Two-phase composite — BOTH production-phase sparring + attestation-phase per-claim attestation; both phases necessary
- **D**: Single-phase practitioner-discipline — leave operational signals out of framework; trust practitioner discipline (rejected — violates make-wrong-shapes-impossible)

## Rationale for C (Two-phase composite)

**Locked rubber-stamping entry forces two-phase shape**: axis-2 failures (production) and rubber-stamping (attestation) are INDEPENDENT dimensions. Single-phase definition (Options A or B) misses one failure mode. Composite catches BOTH:
- Production-phase failure modes (answer-machine / oracle / validator AI) — caught by production-phase engagement test
- Attestation-phase failure mode (rubber-stamping) — caught by attestation-phase engagement test

**Per-claim granularity** matches locked defensibility's claim-granularity resolution. Per-claim engagement events fire DURING claim production + AT claim finalization, aligning with locked `claim` entry's "CREATED during workflow execution... FINALIZED at send/sign moment."

**Two layers (presence + quality)** preserves framework / shape-policy boundary: framework guarantees minimum (presence test); per-shape policy adds quality refinement. Quality-gate enforces at runtime. Maintains MAINTENANCE.md TOP-LEVEL ARCHITECTURE separation.

## Refinements applied (Round 2 expansions)

| ID | Refinement | Status |
|---|---|---|
| E1 | Vocabulary disambiguation: "engaged authorship" (locked) vs "engagement" (generic) vs "engaged" (adjective) | Applied to entry |
| E2 | Lens 6 reciprocal asymmetry with rubber-stamping: engaged authorship is two-phase success; rubber-stamping is attestation-phase failure only. NOT 1:1 reciprocal | Applied to entry's What-it-is-NOT + cross-ref structure |
| E3 | Claim revision per-version semantics: per-claim per-version test; v1 engagement doesn't carry forward to v2; append-only audit captures re-attestation events | Applied to entry's lifecycle |
| E4 | Quality-vs-presence two-layer distinction (Round 1 ST9 deepened): framework-PRESENCE (Y/N) + shape-policy-QUALITY (depth signals) | Applied to entry |
| E5 | Workflow_instance composition: engagement events fire at workflow phases when codified; ad-hoc events fire per claim regardless of workflow_instance | Applied to Composes-with `workflow` |
| E6 | Multi-claim batch attestation: PRESENCE holds per attestation event; QUALITY may flag rapid-batch as rubber-stamping risk; framework doesn't conflate | Applied to entry |
| E7 | Authority-binding orthogonal composition: authority-binding declares WHO can attest; engaged-authorship declares WHAT attestation captures | Applied to Composes-with `mechanism` |
| E8 | Pre-existing-claim ingestion: re-engagement event required OR template-with-attribution policy per shape | Note + flag for ARCH 3.5 schema |
| E9 | TOC placement: §8 Meta concepts (alongside DERIVED `deployment` / `pioneer instance` / `category collapse` / `defensibility`) | Applied to GLOSSARY TOC §8 |
| E10 | AI-runtime engagement events: practitioner's engagement is tested via human-actor events; AI-runtime is sparring substrate, not engagement subject | Applied to What-it-is-NOT |

## REVISION-grade stress-tests

| ID | Test | Verdict |
|---|---|---|
| **R1** | Should engaged authorship be PRIMITIVE not DERIVED? | **REJECTED** — DERIVED is correct: test/property applied to claims (parallel to defensibility), not entity-having primitive. Has structure (two-phase composite + signals) but no instances. |
| **R2** | Merge into `defensibility` entry as expanded Condition #1, no separate entry? | **REJECTED** — rubber-stamping has own entry (axis-3 failure mode); engaged authorship is its success contrast; parallel structure. Standalone entry preserves canonical operational definition without bloating defensibility. |
| **R3** | Unify both phases into single concept "engagement"? | **REJECTED** — composite catches BOTH failure modes (axis-2 production + axis-3 attestation); unifying loses asymmetry already-locked in rubber-stamping (attestation-only) vs axis-2 failures (production-only). |
| **R4** | Per-attestation-event granularity instead of per-claim? | **REJECTED** — locked defensibility says claim-granularity; per-claim is the right granularity; per-claim attestation is one signal at finalization phase. |

## Composition with existing architecture

| Existing primitive | Composition |
|---|---|
| `defensibility` (DERIVED) | Engaged authorship IS the operational definition of defensibility's engaged-authorship condition (Condition #1); per-claim defensibility composes from per-claim engaged-authorship + per-claim source-grounding + per-claim audit-trail-completeness |
| `authorship preservation (axis 3)` (DERIVED) | Engaged authorship IS the success mode this axis preserves; architectural commitment expresses, engaged authorship makes observable |
| `rubber-stamping` (DERIVED) | Attestation-phase failure mode contrast (asymmetric: rubber-stamping is attestation-only failure; engaged authorship is two-phase success) |
| `answer-machine AI / oracle AI / validator AI` (DERIVED) | Production-phase failure mode contrasts (each is axis-2 failure that bypasses production-phase engagement) |
| `claim` (PRIMITIVE) | Per-claim granularity; per-claim engagement events fire DURING claim production (production-phase) + AT claim finalization (attestation-phase) |
| `event` (PRIMITIVE) | Engagement events compose audit trail; per-claim per-phase event-existence is the framework-PRESENCE test |
| `sparring (axis 2)` (DERIVED) | Production-phase engagement is sparring-anchored; sparring events are the production-phase signal substrate |
| `actor` (PRIMITIVE) | Practitioner-engagement tested via human-actor events (`actor_kind: human`); AI-runtime is sparring substrate, not engagement subject |
| `mechanism` | Composes with audit-emission + authority-binding + source-grounding (orthogonal). Authority-binding: WHO. Engaged-authorship: WHAT attestation captures. |
| `quality-gate` (Pattern A) | Quality-gate's axis-3 intervention applies engaged-authorship test; engaged-authorship's quality signals are quality-gate's axis-3 observability source |
| `workflow_instance` (when codified) | Engagement events fire at workflow phases; ad-hoc events fire per claim regardless of workflow_instance (workflow primitive optional; engaged-authorship mandatory) |
| `category collapse` | Engaged-authorship-failure is category-collapse manifestation on axis 2 (production) and axis 3 (attestation) |
| `shape` | Shape policy declares quality thresholds + intervention semantics; framework declares presence test |

## Defers (D-gate-validated; Phase 3.5/3.6 schema territory)

| Defer | Awaited signal | Reason valid |
|---|---|---|
| Full event signal catalog per-phase (production-phase: counter-argument-emit / alternative-consider / position-defend / source-ground / judgment-override; attestation-phase: per-claim-attest / re-attest-on-revision) | Phase 3.5 engaged-authorship-mechanics ARCH topic + Phase 3.6 quality-gate signals | Schema-detail per signal |
| Per-claim-kind variation (interpretive vs citation vs procedural claims have different engagement requirements) | Phase 3.5 ARCH topic | Per-claim-kind schema |
| Quality threshold schema per shape (depth signals; substantiveness; review-time vs claim-complexity ratios) | Phase 3.6 quality-gate per-shape implementation | Per-shape policy |
| Multi-practitioner co-attestation mechanics (federation + multi-user shapes) | Phase 3.5 + per-shape policy | Per-shape policy variation |
| Pre-existing-claim ingestion semantics (template re-engagement policy) | Phase 3.5 ARCH topic | Implementation-specific |
| Authority-binding-vs-engaged-authorship interaction details | Phase 3.5 + Phase 3.3 (authority-binding mechanism detail) | Schema-detail |

D Gate verdict: all defers genuine schema-detail (HOW), not architectural-decision (WHAT). All defers valid.

## Constraints flowing

This decision flows constraints into:
- **Phase 3.3** per-mechanism detail (audit-emission events catalog must include engaged-authorship signals; authority-binding compose with engaged-authorship's WHAT-attestation-captures)
- **Phase 3.5** primitive-detail topics (engaged-authorship-mechanics ARCH topic: full event signal catalog per-phase; per-claim-kind variation; quality threshold schema per shape; multi-practitioner co-attestation; pre-existing-claim ingestion; claim-mechanics composes with per-claim engagement test)
- **Phase 3.6** quality-gate full ARCH topic (engaged-authorship's quality signals are quality-gate's axis-3 observability source; per-shape intervention mechanics)
- **Phase 6** workspace serialization spec (engagement events portability; per-claim attestation persistence)

## Files touched

- `GLOSSARY.md` engaged authorship entry (NEW; DERIVED entry with full anatomy)
- `GLOSSARY.md` TOC §8 Meta concepts (engaged authorship added)
- `GLOSSARY.md` defensibility Condition #1 (replaced inline description with reference to engaged-authorship entry; tightened cross-ref)
- `GLOSSARY.md` defensibility Composes-with (engaged authorship cross-ref added)
- `GLOSSARY.md` defensibility See section (engaged authorship cross-ref added)
- `GLOSSARY.md` authorship preservation (axis 3) Composes-with (engaged authorship cross-ref added)
- `GLOSSARY.md` rubber-stamping Composes-with (success-mode contrast cross-ref added)
- `GLOSSARY.md` quality-gate Composes-with (axis-3 observability source cross-ref added)
- `GLOSSARY.md` claim Composes-with (per-claim engagement events cross-ref added)
- `ARCHITECTURE.md` Locked architectural decisions section (engaged-authorship lock entry added; Phase 3.1 closed marker)
- `ARCHITECTURE.md` Phase 3 sub-phase status table (3.1 COMPLETE marker)
- `BACKLOG.md` Phase 3.1 (engaged-authorship → Resolved; **Phase 3.1 CLOSED**)
- `docs/decisions/engaged-authorship-operational-definition.md` (this file)

## Revisit triggers

This DR should be revisited if:
- Phase 3.5 engaged-authorship-mechanics ARCH detail surfaces operational concerns the two-phase composite can't accommodate
- Phase 3.6 quality-gate full design surfaces signal-catalog concerns the framework-PRESENCE test misses
- Second-shape productization (autonomous-business OR personal-OS) reveals engagement semantics differ structurally beyond per-shape quality-policy variation
- Federation / multi-practitioner work surfaces multi-author engagement structurally requiring framework-level (not just shape-policy) treatment
- Pioneer-deployment data shows two-phase composite is over- or under-specified

## Sharpening rounds metadata

- **Round 1**: AI full monty — 4 adoption options + 12 stress tests (ST1-ST12) + position committed (Option C: two-phase composite per-claim test + framework-PRESENCE / shape-policy-QUALITY layers + new DERIVED GLOSSARY entry parallel to rubber-stamping)
- **Round 2**: USER-TRIGGERED — 10 EXPANSIONS applied (E1-E10) + 4 REVISION-candidates rejected (R1-R4 manufactured criticism)
- **Self-check**: STABLE; 0 architectural REVISIONS; all findings EXPANSIONS or rejected manufactured criticism
- **Multi-axis validation discriminator** (per decision-design-sharpening v0.5.0): shape-specific surface present (practitioner-shape vs autonomous-business-shape vs personal-OS-shape) → profile-anchored validation fired (Cluster B deployers + Cluster C consumers + per-shape mental modeling — all confirm two-phase composite holds across shapes with per-shape quality variation)
- **GLOSSARY back-check** (per v0.5.0 + MAINTENANCE.md Bidirectional cascade): the decision IS itself glossary work; EXPANSIONS surfaced went directly into the new entry. Elevation from defensibility's Condition #1 inline to standalone DERIVED entry is the canonical example of bidirectional cascade — ARCH-territory work surfaced glossary-grade structural fact that retro-fitted (and elevated) to GLOSSARY before lock.

Total: 2 rounds. Per `feedback_pre_decision_sharpening.md` 2-round sweet spot empirical pattern. Narrow architectural surface (single DERIVED concept lock + condition extraction from existing entry) → 2 rounds sufficient.

## Phase 3.1 closure

This DR closes Phase 3.1 (open architectural questions: workflow / work-unit / deployment / engaged-authorship — all locked). Coherence-audit recommended before Phase 3.2 topic taxonomy work begins (4 architectural locks + new disciplines codified = phase boundary; corpus-set review warranted per `coherence-audit` skill phase-boundary trigger).
