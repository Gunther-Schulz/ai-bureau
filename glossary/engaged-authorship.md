---
entry: engaged authorship
class: DERIVED
layer: cross-cutting
axis: axis-3
vision_usage: implicit
---

# engaged authorship

- **Class**: DERIVED (axis-3 success mode; operational definition for `defensibility`'s engaged-authorship condition; not a primitive with instances)
- **Layer**: cross-cutting (engaged authorship is a property tested AGAINST claims; structurally observable via events)
- **Axis**: axis-3 (the success mode `authorship preservation` requires); cross-axis composition with axis-2 (production-phase engagement is sparring-anchored)
- **VISION usage**: implicit (`VISION.md` axis-3 framing — "no signature without engagement" — names the success mode without using "engaged authorship" as locked term; engaged authorship is the operational sharpening)

**Vocabulary disambiguation**:
- **`engaged authorship`** — the locked operational concept (this entry; two-phase composite per-claim test)
- **`engagement`** — generic English term; NOT the locked concept; avoid in load-bearing contexts when engaged authorship is meant
- **`engaged`** — adjective; may modify other primitives (engaged co-worker, engaged sparring) without invoking this entry's full semantics

**Canonical**: The structurally observable practitioner participation in produced output, captured per-claim via composite signals across two phases — production-phase engagement (axis-2-anchored) AND attestation-phase engagement (axis-3-anchored). Both phases must structurally complete for engaged-authorship to hold per claim. Success contrast to `rubber-stamping` (attestation-phase failure) AND to `answer-machine AI / oracle AI / validator AI` (production-phase failures).

**What it is**: The operational definition of `defensibility`'s engaged-authorship condition. Where defensibility's three conditions are (1) engaged authorship, (2) reconstructible reasoning chain, (3) source-grounded content — the latter two are operationalized via `audit emission` + `source-grounding` mechanisms with clear observable signals. Engaged authorship's operational definition was historically loose; this entry sharpens to two-phase composite per-claim test:

1. **Production-phase engagement** (axis-2-anchored): per-claim sparring participation observed via sparring-event emissions — counter-argument engagement, alternative-consideration, position-defense, source-grounding decisions, judgment-call overrides (practitioner overrides AI suggestion). Without production-phase engagement, claim production was answer-machine / oracle / validator extraction (axis-2 failure modes); claim's engaged-authorship condition fails at production phase.

2. **Attestation-phase engagement** (axis-3-anchored): per-claim attestation event emitted at finalization (NOT whole-output sign-off). Without per-claim attestation, claim was rubber-stamped (axis-3 failure mode); claim's engaged-authorship condition fails at attestation phase.

**Both phases are independent and both must structurally complete** (per locked `rubber-stamping` entry: axis-2 failures and rubber-stamping are INDEPENDENT dimensions). One claim can have strong production-phase engagement but be rubber-stamped at attestation; another can have substantive attestation but had answer-machine extraction at production. Both failures bypass engaged authorship; both are independently observable.

**Granularity**: per-claim (consistent with `defensibility` claim-granularity resolution). Per-claim engagement events fire DURING claim production (production-phase) + AT claim finalization (attestation-phase). Aligns with `claim` entry's "CREATED during workflow execution... FINALIZED at send/sign moment."

**Two layers of operationalization** (presence vs quality):

- **Framework-level: PRESENCE** — Y/N structural test on event existence. Per-claim production-phase event (≥1 sparring/judgment event) + per-claim attestation event = PRESENCE holds. Framework-PRESENCE is the gate condition for defensibility's engaged-authorship condition.
- **Shape-policy-level: QUALITY** — depth-of-engagement signals (substantiveness; counter-argument depth; review-time vs claim-complexity ratio; etc.). Per-shape policy refines presence with quality thresholds. `quality-gate` (Pattern A protocol) detects quality-deficit signals; emits drift; per-shape intervention (practitioner-shape friction/block; autonomous-business programmatic block; personal-OS audit-only).

Two layers are intentional: framework guarantees minimum (presence) without dictating per-shape quality semantics. Per-shape policy extends framework with quality refinement.

**Framework-level enforcement** (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 make-wrong-shapes-impossible discipline):
- Events emit per-claim across both phases (audit-emission mechanism)
- `quality-gate` (Pattern A protocol) detects missing signals; emits drift signals at attestation moments
- Per-shape intervention policy: practitioner-shape = friction/block (defensibility-critical; fail-closed); autonomous-business-shape = programmatic block (operator-attestation programmatic); personal-OS-shape = audit-only

**Per-claim per-version semantics**: claim revision = per-claim per-version engagement test. Engaged authorship of claim v1 doesn't carry forward to v2 if v2 wasn't engaged. Append-only audit captures re-attestation events per revision; engagement events emit for revised content.

**Multi-claim batch attestation**: practitioner attests N claims in one sitting. Each emits per-claim attestation event (PRESENCE holds at framework level). QUALITY signals may flag rapid-batch as rubber-stamping risk (per-shape policy concern). Framework doesn't conflate batch with rubber-stamping; quality-gate's drift detection per shape policy may.

**What it is NOT**:
- Not 1:1 reciprocal of `rubber-stamping` — engaged authorship is two-phase (production + attestation); rubber-stamping is attestation-phase failure only. Asymmetry is load-bearing: engaged-authorship's failure modes include rubber-stamping (attestation) + axis-2 failure modes (production)
- Not a measure of AI-runtime engagement — practitioner's engagement is tested via human-actor events (per `actor` entry `actor_kind: human`); AI-runtime sparring events are the substrate, not the engagement subject
- Not engagement quality (framework operationalizes presence; quality is per-shape policy concern)
- Not a primitive with instances — DERIVED test/property applied to claims; no separate entity-having instances
- Not generic "human-in-the-loop" — HITL without per-claim engagement events still rubber-stamps (matches authorship preservation entry's What-it-is-NOT)
- Not capacity-building — capacity-building is a side effect of engaged-authorship-required architectures, not the test itself
- Not optional for accountability-bearing claims — wherever claim primitive is engaged, engaged-authorship test applies (mandatory; no opt-out at framework level for accountability-bearing output)

**Cross-archetype illustration** (engaged authorship per archetype):

- **Practitioner-shape (planner; PBS-Schulz pioneer)**: production-phase = sparring during Begründung argumentation construction (counter-arguments engaged, alternative legal-interpretations considered, source-grounding decisions emitted as events); attestation-phase = per-claim attestation at signing (each legal-interpretation claim, proportionality claim, mitigation claim attested individually before whole-Begründung sign-off)
- **Practitioner-shape (lawyer)**: production-phase = sparring during brief construction (case-law applicability defended, counter-arguments engaged); attestation-phase = per-citation + per-argument attestation at filing
- **Practitioner-shape (researcher)**: production-phase = sparring during methodology + finding-interpretation; attestation-phase = per-claim attestation at submission
- **Practitioner-shape (auditor)**: production-phase = sparring during materiality + finding-determination; attestation-phase = per-finding attestation at report-signing
- **Autonomous-business-shape (operator)**: production-phase = bounded AI checkpoints (operator-supervised); attestation-phase = programmatic attestation per shape policy; both phases observed via events even when non-human
- **Personal-OS-shape**: production-phase = light sparring per task; attestation-phase = per-claim attestation if accountability-bearing OR audit-only without intervention

**Boundary test**: Three questions — engaged authorship passes per claim only when ALL three resolve favorably:
1. Did production-phase engagement events emit for this claim (≥1 sparring / judgment / source-grounding event)? → if no, engaged-authorship fails at production phase
2. Did attestation-phase per-claim attestation event emit at finalization? → if no, engaged-authorship fails at attestation phase
3. Per shape policy: do quality signals exceed minimum thresholds? → if no, quality-gate may emit drift / intervene per shape policy

Q1 + Q2 are framework-PRESENCE tests. Q3 is shape-policy-QUALITY refinement.

**Composes with**:
- [defensibility](defensibility.md) — engaged authorship IS the operational definition of defensibility's engaged-authorship condition (defensibility condition #1); per-claim defensibility composes from per-claim engaged-authorship + per-claim source-grounding + per-claim audit-trail-completeness
- [authorship preservation (axis 3)](authorship-preservation.md) — engaged authorship IS the success mode authorship preservation requires (architectural commitment expresses; engaged authorship makes it observable)
- [rubber-stamping](rubber-stamping.md) — engaged authorship's attestation-phase failure mode contrast (asymmetric: rubber-stamping is attestation-only failure; engaged authorship is two-phase success requiring both phases)
- [answer-machine AI](answer-machine-ai.md) / [oracle AI](oracle-ai.md) / [validator AI](validator-ai.md) — engaged authorship's production-phase failure mode contrasts (each is axis-2 failure that bypasses production-phase engagement)
- [claim](claim.md) — per-claim granularity; per-claim engagement events fire DURING claim production (production-phase) + AT claim finalization (attestation-phase); aligns with claim lifecycle
- [event](event.md) — engagement events compose audit trail; per-claim per-phase event-existence is the framework-PRESENCE test
- [sparring (axis 2)](sparring.md) — production-phase engagement is sparring-anchored; sparring events are the production-phase signal substrate
- [actor](actor.md) — practitioner-engagement tested via human-actor events (`actor_kind: human`); AI-runtime is sparring substrate, not engagement subject
- [mechanism](mechanism.md) — composes with audit-emission (per-phase event capture) + authority-binding (WHO can attest per shape policy) + source-grounding (separate defensibility condition; orthogonal). Authority-binding declares WHO; engaged-authorship declares WHAT attestation captures
- [quality-gate](quality-gate.md) (Pattern A) — quality-gate's axis-3 intervention applies engaged-authorship test at attestation moments; engaged authorship's quality signals are quality-gate's axis-3 observability source
- `workflow_instance` (when codified) — engagement events fire at workflow phases (drafting → review → signing); ad-hoc work fires events per claim regardless of workflow_instance (workflow primitive is optional overlay; engaged-authorship is mandatory wherever accountability-bearing claims exist)
- [category collapse](category-collapse.md) — engaged-authorship-failure is category-collapse manifestation on axis 2 (production-phase) and axis 3 (attestation-phase)
- [shape](shape.md) — shape policy declares quality thresholds + intervention semantics; framework declares presence test
- [policy](policy.md) — practitioner-shape policy mandates engaged-authorship presence + quality intervention; autonomous-business-shape policy mandates programmatic attestation; personal-OS-shape policy mandates light-touch

**Cardinality + lifecycle**:

**Cardinality**: N/A — engaged authorship is a property/test applied per-claim per-version, not an instance-having entity.

**Lifecycle**: per-claim per-version test that resolves at finalization moment. Production-phase events accumulate across claim production (potentially across multiple sessions); attestation-phase event fires at claim finalization. Test re-runs at audit time (post-hoc reconstruction): claim's events reconstructed from audit trail; engaged-authorship test re-applied. Re-attestation required on claim revision (v2 of claim = new engaged-authorship test cycle; v1's engagement doesn't carry forward).

**Source**:
- VISION (`VISION.md`):
  - Line 154+ (axis-3 framing): "no rubber-stamping; no signature without engagement; no work the practitioner can't defend"
  - Line 92 (axis-3 falsification): defensibility framing implicitly requires engaged-authorship as condition
- Locked GLOSSARY entries: [defensibility](defensibility.md) (Condition #1: "engaged authorship"); [rubber-stamping](rubber-stamping.md) (failure mode at attestation phase only; axis-2 failures + rubber-stamping are INDEPENDENT dimensions); [claim](claim.md) (per-claim granularity; CREATED during workflow execution + FINALIZED at send/sign moment); [sparring (axis 2)](sparring.md) (production-phase engagement substrate); [quality-gate](quality-gate.md) (axis-3 intervention applies engaged-authorship test); [authorship preservation (axis 3)](authorship-preservation.md) (architectural commitment expressing engaged authorship); [actor](actor.md) (`actor_kind: human` distinguishes practitioner engagement from AI-runtime sparring substrate)
- Synthesis: two-phase composite operational definition resolves the historical looseness of "engaged authorship" condition inside defensibility entry; structural events at both phases enable framework-PRESENCE test; per-shape policy adds QUALITY refinement layer; quality-gate enforces

**See**:
- [defensibility](defensibility.md) (which engaged authorship is condition #1 of)
- [authorship preservation (axis 3)](authorship-preservation.md) (architectural commitment engaged authorship operationalizes)
- [rubber-stamping](rubber-stamping.md) (attestation-phase failure mode contrast)
- [answer-machine AI](answer-machine-ai.md) / [oracle AI](oracle-ai.md) / [validator AI](validator-ai.md) (production-phase failure mode contrasts)
- [claim](claim.md) (per-claim granularity)
- [sparring (axis 2)](sparring.md) (production-phase engagement substrate)
- [quality-gate](quality-gate.md) (Pattern A runtime protocol applying engaged-authorship test at attestation moments)
- [arch/claim-defensibility.md](../arch/claim-defensibility.md) — engaged-authorship cross-cluster composition WITHIN claim-defensibility cluster as defensibility Cond #1 operational definition + per-claim attestation chain mechanics + pre-existing-claim ingestion semantics (Phase 3.5 fourth primitive-cluster ARCH topic LOCKED; PRIMITIVE+DERIVED topic-template-class anchor; archived material to consult for Phase 6 engaged-authorship event signal catalog + per-claim-kind variation schema: `audit-trail-v2.md` for event schema)
