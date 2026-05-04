---
title: Claim + defensibility
topic-cluster: primitive-cluster (#4 of 4)
status: locked
---

# Claim + defensibility

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the claim + defensibility primitive cluster (the atomic accountability-bearing-assertion PRIMITIVE + the operational test DERIVED for axis 3 per locked GLOSSARY entries). Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the claim-event Pydantic schema (Mode 3). Foundation-up dependency: claim-defensibility composes with already-locked specialist-skill + practitioner + workflow-work-unit primitive clusters (skills produce claims; practitioner-RECORD attests; work-unit instance contains claims; workflow_instance attribution scopes claims). Locking claim-defensibility fourth means the per-claim attestation chain mechanics lock against validated upstream attribution surfaces.

## 1. Topic scope + frontmatter

**Cluster identity**: claim + defensibility — the atomic-accountability-bearing-assertion + operational-axis-3-test primitive cluster. PRIMITIVE + DERIVED cluster. Claim is the atomic content-unit within work-unit output (the unit-of-defense per `glossary/claim.md`); defensibility is the operational test for axis 3 (`authorship preservation`) defined as a property/test applied AGAINST claims per `glossary/defensibility.md`.

**Primitives covered**:
- `claim` — PRIMITIVE atomic; the accountability-bearing-assertion content-unit within work-unit output (per locked GLOSSARY)
- `defensibility` — DERIVED property/test; operationalizes axis-3 success criterion against claim granularity (per locked GLOSSARY)

**Cross-axis claim**: claim is **axis-3 PRIMARY anchor** — claim is the unit-of-defense per the defensibility test (per `glossary/claim.md` axis classification "axis-3 primary anchor"); defensibility IS the axis-3 success criterion test (per `glossary/defensibility.md`). Cross-axis composition: axis-2 (claims are sparring targets — counter-arguments target individual claims; confidence calibration applies per claim per `glossary/sparring.md`); axis-1 (claims are content-units AI co-authors with practitioner per `glossary/intertwining.md` + `glossary/co-worker.md`). The cluster is axis-3 PRIMARY at primitive level with axis-2 + axis-1 cross-axis composition.

**Cardinality at cluster level** (per-primitive detail in §5):
- N claims per work-unit instance (typically dozens-to-hundreds per `glossary/claim.md` cardinality + lifecycle); claims emit `claim_made` events scoped to containing work-unit instance + workflow_instance attribution (when codified pattern applies)
- defensibility cardinality N/A — property/test, not entity-having; resolves at claim granularity per `glossary/defensibility.md`

**Cluster boundary**: this topic locks the PRIMITIVE+DERIVED structural articulation (4-property claim + 3-condition defensibility test), the cross-primitive composition commitments (reciprocal asymmetry + composability-of-defensibility-test + per-claim attestation chain mechanics + pre-existing-claim ingestion semantics), the per-claim lifecycle ordering + 6-event-kind catalog candidate, the granularity tests + claim 3-test, the cross-shape policy variation 6-row matrix, and W1-W4 watch-list. It does NOT lock specialist + skill mechanics (Phase 3.5 `arch/specialist-skill.md` topic; LOCKED) or practitioner mechanics (Phase 3.5 `arch/practitioner.md` topic; LOCKED) or workflow + work-unit mechanics (Phase 3.5 `arch/workflow-work-unit.md` topic; LOCKED) — those compose with this cluster's primitives but live in their own topics.

**Composition with framework**:
- Claim lives at cross-cutting layer (claims sit within work-unit output content per `glossary/claim.md` line 12; not framework-mechanism, not shape-policy, not Framework C definition)
- Defensibility lives at cross-cutting layer (property tested AGAINST claims + work-units per `glossary/defensibility.md` line 12)
- PRIMITIVE + DERIVED classification per locked GLOSSARY (claim PRIMITIVE; defensibility DERIVED); the cluster pairs a PRIMITIVE with its operational-test DERIVED partner — structurally distinct from Pattern B + atomic-primitive (specialist-skill cluster) + Pattern C bipartite (practitioner cluster) + two-Pattern-B (workflow-work-unit cluster)
- Authority-binding mechanism Surface (per `glossary/authority-binding.md`) consumes practitioner-RECORD + skill identifier for `claim_made` event attribution per per-event actor declaration sub-aspect; per-claim author attribution chain is one of three architectural sub-aspects of authority-binding
- Audit mechanism class records claim lifecycle events per §13 event-kind catalog candidate

**Phase routing**: claim-event Pydantic schema → Phase 6 spec (Mode 3). Per-claim-kind variation schema + cryptographic signing implementation + multi-practitioner co-attestation persistence + defensibility_test_run event reconstruction mechanics → Phase 6 (per W1 + W3 + W4 watch-list). Per-deployment claim production happens at workspace deployment (NOT this repo per `MAINTENANCE.md` TOP-LEVEL SCOPE instance-content lives at deployment-instance).

## 2. Per-primitive structural overview

### 2.1 Claim PRIMITIVE (atomic; cross-cutting)

Per locked GLOSSARY `claim` entry: an atomic accountability-bearing assertion within a work-unit's produced output — the smallest unit of content the practitioner-author can be challenged on, must defend, and bears regulatory/professional accountability for.

**Four distinguishing properties** (architectural-level enumeration; all four must hold for assertion to qualify as claim):

1. **Atomic** — semantic-unit of one assertion; typographical units (paragraph, sentence) may contain 0/1/N claims depending on content (per `glossary/claim.md` "Not a paragraph or sentence per se — claim is the SEMANTIC unit (one assertion)")
2. **Accountability-bearing** — practitioner can be professionally/regulatorily challenged on it (per `glossary/claim.md` What-it-is-NOT property #1)
3. **Judgment-bearing** — NOT lookup-shaped; fact-statements aren't claims even when sourced (e.g., "BauGB §35 was amended in 2024" = fact-statement, not a claim per `glossary/claim.md` What-it-is-NOT property #2)
4. **Source-grounded** — every claim traces to source per source-grounding mechanism; framework-level guarantee that no claim is unsourced (per `glossary/claim.md` What-it-is-NOT property #3)

**Claim-event composition**: claims emit `claim_made` events; the event records the claim's emission (structured emission to audit trail per `glossary/event.md`); the claim itself is the asserted content. Greenfield-evaluated against locked `event` + `actor` GLOSSARY entries: `claim_made` is the event-kind for emission moments; `actor_kind: ai_runtime` + skill identifier records authoring actor per authority-binding mechanism Surface (per `glossary/authority-binding.md` per-event actor declaration); per-claim author attribution chain composes through skill identifier → specialist → workspace per authority-binding chain (per `arch/specialist-skill.md` §4 composition table claim row).

**Claim revision per-version semantics**: claim revision = new `claim_made` event preserving prior claim state per append-only audit (per `glossary/claim.md` "REVISED during review (revision emits new event preserving prior claim state per append-only audit)"; per `arch/audit.md` §B append-only persistence). Engaged-authorship of claim v1 does NOT carry forward to v2 — re-attestation required on revision per `glossary/engaged-authorship.md` "claim revision = per-claim per-version engagement test. Engaged authorship of claim v1 doesn't carry forward to v2 if v2 wasn't engaged."

**Production / revision / finalization moments**: claims are CREATED during workflow execution (drafting fires `claim_made` events as claims are produced); REVISED during review (revision emits new event preserving prior claim state per append-only audit); FINALIZED at send/sign moment (signed-claim_made event; practitioner authorship binding per `glossary/authority-binding.md` line 35 "every signature_applied event records actor_kind: human + practitioner identity for legal-bind moments"). Mutability = append-only at audit level (claim revision = new event, not rewriting previous); content mutability lives at draft level until finalization.

### 2.2 Defensibility DERIVED (property/test; cross-cutting)

Per locked GLOSSARY `defensibility` entry: the operational test for `authorship preservation (axis 3)` — the property that the practitioner-author can defend the produced output under regulatory or professional challenge, having engaged with the judgment calls and being able to reconstruct the reasoning chain.

**Three-condition operational test** (architectural-level enumeration; all three structural conditions must hold for defensibility to pass):

1. **Engaged authorship (Cond #1)** — operational definition per `glossary/engaged-authorship.md` two-phase composite test: production-phase engagement (axis-2-anchored sparring events fire DURING claim production) + attestation-phase engagement (axis-3-anchored per-claim attestation event fires AT claim finalization). Both phases independent; both must structurally complete. Cross-cluster composition: engaged-authorship DERIVED entry's 2-phase test IS the operational definition of defensibility's Cond #1 — engaged-authorship lives at GLOSSARY but its operational mechanics compose INTO this cluster (cross-cluster DERIVED composition; documented explicitly).
2. **Reconstructible reasoning chain (Cond #2)** — every claim traces to source; events compose audit trail; reasoning recoverable post-hoc. Structurally enabled by audit emission mechanism (per `arch/audit.md` Surface §A emission API + §C query API) + authority-binding mechanism (per `glossary/authority-binding.md`; reconstructible attribution chain is precondition for defensibility's reconstructible-reasoning-chain condition).
3. **Source-grounded content (Cond #3)** — no unsourced claims at framework level. Structurally enabled by source-grounding mechanism (Phase 3.3 detail; mechanism instance per locked GLOSSARY `mechanism` entry; per `glossary/claim.md` "every claim must trace to source").

**Claim-granularity resolution + composability**: defensibility resolves at claim granularity per `glossary/defensibility.md` ("test resolves at claim granularity") + `glossary/claim.md` ("claim is the unit-of-defense per the defensibility test"). Composability: per-claim defensibility composes work-unit defensibility — if every claim passes the test, the work-unit's output passes; conversely, ONE indefensible claim taints the work-unit's output (per `glossary/defensibility.md` "Composability: if every claim passes the defensibility test, the work-unit's output passes. Conversely, ONE indefensible claim taints the output").

**Boundary tests** (architectural-level; per `glossary/defensibility.md` Boundary test 4-question structure):

| Q | Question | Test type |
|---|---|---|
| **Q1** | Will the practitioner be able to DEFEND this output six months from now under regulatory or professional challenge, having forgotten details? | practitioner-experiential |
| **Q2** | Is this output something the practitioner GENUINELY engaged with (not rubber-stamped)? | practitioner-experiential |
| **Q3** | Can the reasoning chain (sources, decisions, sparring outcomes) be RECONSTRUCTED from audit trail? | practitioner-experiential |
| **Q4** | Does the output have an audit trail showing per-claim sources, engagement events, and reasoning chain? | structural-observable (positive marker) |

Q1-Q3 are practitioner/experiential tests; Q4 is the structural-observable test for architects.

**Re-run-ability via audit-trail reconstruction**: defensibility test is **re-run-able** per `glossary/defensibility.md` cardinality + lifecycle: six-months-later (or years-later), when challenged, the reasoning chain is reconstructed via audit trail. Defensibility doesn't expire; the structural conditions, captured at production time, persist as audit records and remain testable indefinitely (subject to audit-trail retention policy per workspace + audit Surface §D integrity verification per `arch/audit.md`).

## 3. Cross-primitive composition within the cluster

The claim + defensibility cluster pairs a PRIMITIVE with its operational-test DERIVED partner. Four load-bearing structural commitments + cross-cluster engaged-authorship composition.

### Reciprocal asymmetry (load-bearing)

Claim is atomic content-unit (assertion within work-unit output); defensibility is property/test applied to claims (NOT entity-having; NOT 1:1 reciprocal). The cluster pairs primitive-with-its-test rather than two equal-status primitives.

This asymmetry parallels engaged-authorship's 2-phase asymmetry vs rubber-stamping (rubber-stamping is attestation-only failure; engaged-authorship is two-phase success per `glossary/engaged-authorship.md` "Asymmetry is load-bearing"; per Lens 6 reciprocal-asymmetry pattern). The asymmetry is NOT cosmetic — defensibility doesn't BUNDLE claims; defensibility is the test APPLIED TO claims. One-way directional composition (defensibility-tests-claims, never claims-bundle-defensibility).

### Composability-of-defensibility-test

Per-claim defensibility composes work-unit defensibility per `glossary/defensibility.md`: if every claim passes the test, the work-unit's output passes; ONE indefensible claim taints the whole output. This composability is structural — not cosmetic per-claim aggregation; the test resolves at claim granularity AND aggregates to work-unit level.

The composability commitment locks the granularity-resolution + aggregation discipline: validators (Cluster D) test per-claim individually under six-months-later challenge (NOT whole-output blob); architects evaluate work-unit-level defensibility AS the aggregation of per-claim test outcomes; one indefensible claim is sufficient signal of work-unit-output indefensibility regardless of other claims passing.

### Per-claim attestation chain (mechanics)

Per-claim attestation chain composes through ordered event emissions:

1. **`claim_made` emission** — claim production fires `claim_made` event with `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface
2. **Production-phase engaged-authorship sparring events** (axis-2 substrate) — sparring sub-mechanisms accessed by skills DURING claim production per `arch/sparring.md` §4 + `glossary/engaged-authorship.md` "production-phase engagement is sparring-anchored; sparring events are the production-phase signal substrate"
3. **Claim revision events** (append-only) — revision emits new `claim_made` event preserving prior state per `arch/audit.md` §B append-only persistence
4. **Finalization moment** — claim finalized at send/sign moment per `glossary/claim.md` lifecycle
5. **Per-claim attestation event** — fires AT finalization (axis-3-anchored per-claim attestation event per `glossary/engaged-authorship.md`); records `actor_kind: human` + practitioner-RECORD identity per `arch/practitioner.md` §4 R-CC-10 (session-bound practitioner) + `glossary/authority-binding.md` line 35
6. **Composition INTO work-unit attribution chain** — per-claim attestation chain composes into work-unit attribution per `arch/workflow-work-unit.md` §3 + `arch/practitioner.md` cross-axis composition; claims attribute to containing work-unit instance + workflow_instance (when codified pattern applies); ad-hoc work claims attribute to work-unit + session without workflow_instance (per `glossary/claim.md` composes-with workflow row)

The attestation chain is per-claim per-version (re-attestation required on revision per `glossary/engaged-authorship.md`); preserves reconstructible attribution chain for defensibility's Cond #2 across the claim's lifecycle.

### Pre-existing-claim ingestion semantics

When pre-existing claims (legacy claims; imported from external systems; carried forward from prior deployments) enter the workspace, framework-level handling preserves engaged-authorship per-claim per-version semantics:

- **Re-engagement event on import** — practitioner re-engages the claim at import-time; emits production-phase + attestation-phase engagement events for the imported claim's v1 (current state at import); from import forward, normal per-claim per-version semantics apply
- **Template-with-attribution policy per shape** — alternative framework-level handling: legacy claim treated as template; new claim_made event records the imported content with attribution chain noting the legacy origin; per-shape policy determines which path (re-engagement vs template-with-attribution) applies

Pre-existing-claim ingestion preserves engaged-authorship-presence guarantee at framework level (Cond #1 of defensibility) for legacy claims; specific handling per shape policy + per-deployment evidence (per W2 watch-list).

### Engaged-authorship cross-cluster composition (DERIVED entry composes IN this cluster)

Engaged-authorship is a DERIVED entry living at GLOSSARY (per `glossary/engaged-authorship.md`); its operational mechanics compose INTO claim-defensibility cluster as Cond #1 of defensibility's three-condition test. The 2-phase composite test (production-phase sparring + attestation-phase per-claim attestation) IS the operational definition of defensibility's Cond #1; without engaged-authorship's structural signals, defensibility's engaged-authorship condition fails.

This cross-cluster composition is documented explicitly to preserve the relationship between primitives clustered together (claim + defensibility in this topic) + DERIVED entries living at GLOSSARY whose operational mechanics compose INTO this cluster (engaged-authorship Cond #1; rubber-stamping axis-3 failure mode failing Cond #1 attestation-phase; answer-machine + oracle + validator AI axis-2 failure modes failing Cond #1 production-phase).

## 4. Composition with framework primitives outside the cluster

### Claim composes with

| Primitive | Composition |
|---|---|
| `framework` | Claim is a framework PRIMITIVE within `framework`'s primitive set; cross-cutting layer per locked GLOSSARY |
| `mechanism` | Claim composes with TWO framework-level mechanisms: audit-emission (captures claim emission via `claim_made` event-kind); source-grounding (requires every claim trace to source — no unsourced claims at framework level) per `glossary/claim.md` composes-with mechanism row |
| `work-unit` | Claims compose into work-unit instance output content; one work-unit instance contains N claims per `glossary/work-unit.md` composes-with claim row; work-unit is artifact-container, claim is atomic content-unit within |
| `workflow_instance` | Claims emitted during workflow_instance execution attribute to that workflow_instance per `glossary/workflow.md` composes-with claim row + `arch/workflow-work-unit.md` §4 composition table; ad-hoc work claims attribute to work-unit + session without workflow_instance attribution |
| `audit` (mechanism class) | Claim lifecycle events per §13 catalog flow through audit Surface §A emission API per `arch/audit.md` §A; per-claim reasoning chain reconstructed via audit Surface §C query API per `arch/audit.md` §C (defensibility test mechanic for Cond #2) |
| `sparring` (mechanism class) | Sparring fires AT claim granularity per `glossary/sparring.md` composes-with claim row: counter-arguments target individual claims; confidence calibration applies per claim; selective friction triggers per claim ambiguity; per-sub-mechanism sparring events compose into engaged-authorship's production-phase substrate per Cond #1 |
| `authority-binding` (mechanism) | Every `claim_made` event records authoring actor (`actor_kind: ai_runtime` + skill identifier); per-claim author attribution (chain-of-defense per axis-3) is one of three architectural sub-aspects of authority-binding per `glossary/authority-binding.md` |
| `practitioner` (Phase 3.5 second primitive-cluster) | Practitioners are accountable for individual claims per `glossary/practitioner.md` composes-with claim row; defensibility test resolves at claim granularity through practitioner-RECORD attribution; per-claim attestation event records practitioner-RECORD identity for attesting actor per `arch/practitioner.md` §4 |
| `specialist-skill` (Phase 3.5 first primitive-cluster) | Skills produce claims (claim_made events) during work execution per `arch/specialist-skill.md` §4 composition table claim row; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain |
| `session` | Claim emissions occur within sessions per `glossary/session.md`; cross-session per-claim attribution via session-bound practitioner per `arch/practitioner.md` §4 R-CC-10 |
| `event` | Claims emit `claim_made` events (specific event-kind); audit trail records claim emission per shape's audit-granularity policy per `glossary/event.md` composes-with claim row |
| `actor` | Claim emissions record `actor_kind` (typically `ai_runtime` for skill-side authoring; `human` for attestation-phase per-claim attestation events per `glossary/actor.md` |
| `shape` | Per-shape audit emission granularity (claim-level for practitioner-shape; action-level for autonomous-business; light for personal-OS) determines per-claim emission frequency per `arch/audit.md` §14 |
| `policy` | Audit granularity policy per shape determines emission frequency per `glossary/policy.md` composes-with claim row + `glossary/claim.md` composes-with policy row |

### Defensibility composes with

| Primitive | Composition |
|---|---|
| `authorship preservation (axis 3)` | Defensibility IS the operational test for axis 3 per `glossary/defensibility.md`; axis 3 expresses architectural commitment, defensibility expresses how to test whether commitment is met |
| `authority-binding` (mechanism) | Reconstructible attribution chain (per-event actor declaration + per-claim author attribution + authority-decision binding) is precondition for defensibility's Cond #2 reconstructible-reasoning-chain condition per `glossary/defensibility.md` composes-with authority-binding row; without authority-binding the test cannot answer "who emitted each claim?" — load-bearing axis-3 dependency |
| `audit` (mechanism class) | Audit Surface §A emission captures per-claim reasoning chain (Cond #2 substrate); audit Surface §B append-only persistence preserves attribution chain; audit Surface §C query API enables six-months-later reconstruction per `arch/audit.md` §A/§B/§C |
| `sparring` (mechanism class) | Sparring mechanisms structurally enable defensibility's engaged-authorship Cond #1 (sparring forces practitioner engagement; sparring events are production-phase substrate for engaged-authorship test per `arch/sparring.md` §4 + `glossary/engaged-authorship.md`) |
| `engaged-authorship` (DERIVED) | Operational definition of defensibility's Cond #1 (two-phase composite per-claim test); per-claim engaged-authorship + per-claim source-grounding + per-claim audit-trail-completeness compose into per-claim defensibility per `glossary/engaged-authorship.md` composes-with defensibility row |
| `source-grounding` (mechanism) | Defensibility's Cond #3 source-grounded content (every claim traces to source; framework-level guarantee); Phase 3.3 detail; mechanism instance per locked GLOSSARY `mechanism` entry; per `glossary/claim.md` "every claim must trace to source" |
| `rubber-stamping` (axis-3 failure mode) | Axis-3 failure mode that fails defensibility's Cond #1 engaged-authorship attestation-phase per `glossary/rubber-stamping.md` composes-with defensibility row; rubber-stamping at attestation moment makes output indefensible regardless of audit trail / source-grounding completeness |
| `answer-machine AI` / `oracle AI` / `validator AI` (axis-2 failure modes) | Axis-2 failure modes that fail defensibility's Cond #1 engaged-authorship production-phase via collapsed sparring (no engagement during reasoning → no engaged authorship at production-phase → defensibility fails) per `glossary/answer-machine-ai.md` + `glossary/oracle-ai.md` + `glossary/validator-ai.md` composes-with defensibility rows |
| `category-collapse` (general force) | Cross-axis force; manifestations on any axis (rubber-stamping axis-3 / axis-2 failure modes / tacked-on AI axis-1) cascade into defensibility failure per `glossary/category-collapse.md` composes-with defensibility row |
| `quality-gate` (Pattern A; Phase 3.6 forthcoming) | Quality-gate's axis-3 intervention applies engaged-authorship test at attestation moments per `glossary/engaged-authorship.md` composes-with quality-gate row + `glossary/defensibility.md`; quality-gate's drift detection consumes per-claim emission observability for axis-3 rubber-stamping signal at attestation moment |
| `claim` | Defensibility test resolves at claim granularity per `glossary/defensibility.md`; one indefensible claim taints the work-unit's output (composability per §3) |
| `work-unit` | Defensibility composes from per-claim tests across the work-unit's outputs per `glossary/defensibility.md` composes-with work-unit row |
| `practitioner` | Defensibility tests apply TO practitioner-authored output; the test asks "will THIS practitioner defend THIS output?" per `glossary/defensibility.md` composes-with practitioner row + `arch/practitioner.md` §4 defensibility composition |
| `event` | Events compose the audit trail that makes reasoning chains reconstructible (defensibility's Cond #2) per `glossary/defensibility.md` composes-with event row |

## 5. Cardinality + lifecycle (per primitive)

### Claim cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Claims per work-unit instance | N (typically dozens-to-hundreds) | Per `glossary/claim.md` cardinality + lifecycle; substantive accountability-bearing outputs typically hundreds of claims |
| Claims per workflow_instance | 0..N | Claims emitted during workflow_instance execution attribute via session-bound practitioner per workflow attribution chain; ad-hoc work claims attribute to work-unit alone |
| Claim INSTANCES per workspace | N | Bounded by total work-unit instances + per-work-unit claim density |

### Claim lifecycle

- **Creator**: AI-runtime via skills (skills produce claims per `arch/specialist-skill.md` §4 composition table claim row); claim emission records `actor_kind: ai_runtime` + skill identifier
- **Owner**: work-unit instance (claims bundled INTO work-unit output content per `glossary/work-unit.md` composes-with claim row + `glossary/claim.md` composes-with work-unit row); not a separate Owner B entity in itself
- **Destructor**: work-unit destruction policy per `arch/workflow-work-unit.md` §13 (NO separate per-claim destruction; claims inherit work-unit's `instance_content_dissolution_policy: archive | delete-with-audit` per cross-pattern coherence with `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 + `arch/workflow-work-unit.md` §13)
- **Mutability**: append-only at audit level (claim revision = new event preserving prior claim state per `arch/audit.md` §B); content mutability lives at draft level until finalization per `glossary/claim.md` lifecycle
- **Persistence**: persists as part of containing work-unit instance per Owner B placement; cross-session via persistent-state mechanism (substrate Surface §F per `arch/substrate.md` §F)

### Defensibility cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Defensibility instances | N/A — property/test, not entity-having | Per `glossary/defensibility.md` cardinality + lifecycle; defensibility resolves at claim granularity, not as separate entity-instance |

### Defensibility lifecycle

- **Test invocation**: applies whenever practitioner is challenged on produced output per `glossary/defensibility.md`; structural conditions (Cond #1 + Cond #2 + Cond #3) must be in place AT PRODUCTION TIME, not retrofitted
- **Re-run-ability**: six-months-later (or years-later) reconstruction via audit trail per `glossary/defensibility.md`; structural conditions captured at production time persist as audit records and remain testable indefinitely (subject to audit-trail retention policy)
- **Test re-applies on claim revision**: claim v2 = new engaged-authorship test cycle per `glossary/engaged-authorship.md`; per-claim per-version semantics preserved

## 6. Logic placement mode

Per `ARCHITECTURE.md` §6 Logic placement modes:
- **Claim production via skills** (claim_made event emission): Mode 1 production-runtime LLM-MD (skill bodies emit `claim_made` events at production moments per `arch/specialist-skill.md` §6); Mode 2 production-runtime Python (substrate audit emission impl per `arch/audit.md` §A)
- **Claim-event Pydantic schema** (Phase 6 spec): Mode 3 hybrid spec layer
- **Defensibility test as documentation**: Mode 4 development-time documentation (NOT production-runtime); test is documented for framework developers + L8 evaluator post-hoc engagement; no production-runtime impl needed beyond audit-trail Surface §C query API enabling reconstruction
- **THIS topic + DR + GLOSSARY entries**: Mode 4 development-time documentation (NOT production-runtime)

Primitive-cluster topics are Mode 4 development-time documentation — articulating the architectural shape framework developers need to understand, not what production AI loads at runtime. Production AI in a deployed PBS workspace loads Mode 1 markdown (skill SKILL.md files; specialist manifests; workspace.md; shape policy bundles); this topic is for framework-developer orientation.

**Per-primitive distribution**:
- Claim-event production: Mode 1 (skill-side emission) + Mode 2 (substrate audit emission impl) + Mode 3 (Phase 6 Pydantic schema spec)
- Defensibility test: Mode 4 (development-time documentation; no production-runtime impl needed; reconstruction via audit-trail Surface §C query is Mode 2 substrate-impl)

**LLM-instruction tightness asymmetry** (per `ARCHITECTURE.md` §6 cross-cutting principles): Mode 1 markdown (skill body content emitting `claim_made` events) requires the highest LLM-instruction tightness review effort because LLMs paper over imprecise markdown by inference. Phase 6 specialist-bundle authoring inherits this discipline.

## 7. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns.

- **Per-claim-kind variation schema** (per W1 watch-list): interpretive-claim vs citation-claim vs procedural-claim variation per per-claim-kind manifest extension; awaits Phase 3.5 schema work + per-archetype claim-kind evidence
- **Pre-existing-claim ingestion mechanics** (per W2 watch-list): re-engagement-event vs template-with-attribution choice per shape; awaits first legacy-claim import deployment evidence
- **Cryptographic signing per claim** (per W4 watch-list): cryptographic chain mechanism (parallel to `arch/practitioner.md` W3 practitioner-record signing + `arch/audit.md` §D integrity verification); awaits Phase 6 audit cryptographic chain implementation
- **Multi-practitioner co-attestation persistence** (per W3 watch-list): cross-practitioner co-attestation mechanics on claims requiring multiple practitioner attestations; awaits second multi-practitioner deployment evidence (cross-link to `arch/practitioner.md` W4 cross-practitioner workflow handoff + W1 multi-tenant federation)
- **`defensibility_test_run` event-kind reconstruction mechanics** (per §13 candidate event-kind catalog): post-hoc reconstruction event implementation; Phase 6 audit-emission catalog territory + Phase 6 spec
- **Per-deployment claim ID uniqueness convention**: prose-rule pattern per archived `governance-and-identity-sourcing.md` decision 3 + decision 4 (greenfield-evaluated per §15); deployment-side prose, AI applies at mint time per Mode 1 markdown discipline

## 8. Cross-shape policy variation (cluster-conditional; APPLIES)

Per primitive-cluster topic template `MAINTENANCE.md` Layer 3 §8 conditional applicability + Pattern A template §14 cross-shape policy variation precedent + `arch/adapter.md` §14 + `arch/audit.md` §14 + `arch/practitioner.md` §8 + `arch/workflow-work-unit.md` §8: this section applies when primitive behavior is shape-policy-mediated. Claim-defensibility cluster IS shape-policy-mediated (per-claim audit emission granularity + engaged-authorship enforcement + source-grounding strictness + attestation-event mandatoriness + quality-gate signal-set + cross-deployment portability all vary per shape).

**What is shape-uniform** (NOT shape-policy-mediated):
- Claim PRIMITIVE 4-property structure (atomic + accountability-bearing + judgment-bearing + source-grounded; same architectural commitment across all shapes)
- Defensibility 3-condition operational test (Cond #1 + Cond #2 + Cond #3; same architectural commitment across all shapes)
- Claim-granularity resolution + composability (per-claim defensibility composes work-unit defensibility; same per shape)
- Claim revision per-version semantics (append-only at audit level; same per shape)
- Reciprocal asymmetry + per-claim attestation chain mechanics (same architectural commitments across all shapes; per-shape tightening additive)

**What is shape-policy-mediated** (6-row matrix; per `arch/workflow-work-unit.md` §8 6-row precedent):

| Dimension | practitioner-shape | autonomous-business-shape | personal-OS-shape |
|---|---|---|---|
| **claim-emission audit granularity per shape** (composes with `arch/audit.md` §14) | Claim-level (one event per claim; finest granularity; mandates by axis-3 defensibility per `glossary/policy.md`) | Action-level (one event per workflow action; coarser; per `arch/audit.md` §14 autonomous-business granularity) | Light (minimal events for memory/replay only; no external accountability requirement) |
| **engaged-authorship enforcement per shape** (composes with `glossary/engaged-authorship.md` Framework-level enforcement) | Friction/block fail-closed (defensibility-critical; missing per-claim engagement events surface to practitioner; quality-gate intervention) | Programmatic block (operator-attestation programmatic; programmatic policy gate) | Audit-only (drift-check report; no friction; lightweight) |
| **per-claim source-grounding strictness per shape** | MANDATORY no-unsourced (every claim traces to source; framework-level guarantee + per-shape enforcement) | Per-action source aggregation OK (action-level audit aggregates source attribution; per-claim source not strictly required at action-level granularity) | Optional (no professional-accountability binding; user preference) |
| **attestation-event mandatoriness per shape** | MANDATORY per-claim (every claim attested at finalization; per-claim attestation event fires per `glossary/engaged-authorship.md`) | Programmatic (operator-attestation programmatic; per business policy) | Optional (no external accountability requirement; light audit) |
| **quality-gate signal-set per shape** (axis-3 observability source per shape policy) | Full engagement signals (sparring participation + counter-argument engagement + source-grounding completeness + per-claim attestation; quality-gate intervention if rubber-stamping detected per `glossary/engaged-authorship.md` quality-gate row) | Threshold-based programmatic signals (per business + budget policy) | Light drift signals (audit-only intervention) |
| **cross-deployment claim portability per shape** | MANDATORY cross-substrate (defensibility re-run-ability requires audit-trail integrity across substrate migrations per `arch/substrate.md` §F + `arch/audit.md` cross-deployment evidence) | Bounded by deployment (cross-substrate portability per business policy) | N/A (no cross-deployment requirement) |

Claim + defensibility cluster primitives stay shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (claim PRIMITIVE 4-property structure + defensibility DERIVED 3-condition test are uniform across all shapes; per-shape variation lives in shape policy bundle declaring per-shape audit-granularity + enforcement + strictness + mandatoriness + signal-set + portability requirements).

**Cross-axis composition** (per `arch/workflow-work-unit.md` §4 cross-axis composition precedent):
- **axis-3 PRIMARY anchor**: claim is unit-of-defense per `glossary/claim.md` axis classification "axis-3 primary anchor"; defensibility IS the axis-3 success criterion test per `glossary/defensibility.md`
- **axis-2 sparring orthogonal**: sparring fires AT claim granularity per `glossary/sparring.md` composes-with claim row; per-sub-mechanism sparring events compose into engaged-authorship's production-phase substrate per Cond #1
- **axis-1 cross-axis**: claims are content-units AI co-authors with practitioner per `glossary/intertwining.md` + `glossary/co-worker.md`; co-worker frame requires axis-1 mechanisms (persistent state, orchestration, source-grounding, audit emission, authority binding per `glossary/co-worker.md` composes-with mechanism row)

## 9. Granularity tests (cluster-conditional; APPLIES)

Per primitive-cluster topic template, granularity tests apply when primitives have granularity discriminators. Claim has load-bearing granularity discriminators per `glossary/claim.md` boundary tests (4-question structure); defensibility has resolution-granularity discriminator per `glossary/defensibility.md` (resolves at claim granularity).

### Claim 3-test (SUBORDINATE to work-unit kind 3-test per `arch/workflow-work-unit.md` §9)

When considering "is THIS assertion a claim or something else?" — apply all three (mirrors `glossary/claim.md` 3-property structure + boundary tests):

1. **Accountability-bearing** — practitioner can be professionally/regulatorily challenged on it. (If not — likely a fact-statement or other non-claim assertion.)
2. **Judgment-bearing** — NOT lookup-shaped. Fact-statements aren't claims even when sourced (e.g., "BauGB §35 was amended in 2024" = fact-statement, not a claim per `glossary/claim.md` What-it-is-NOT property #2).
3. **Source-grounded** — every claim traces to source per source-grounding mechanism (framework-level guarantee). (Generic statements / assertions need not have this property; claim does.)

An assertion passing all three is a claim. An assertion failing one is NOT a claim — it's a fact-statement (failing #2), an opinion-without-source (failing #3), or a non-accountability-bearing assertion (failing #1).

### Boundary tests (per `glossary/claim.md` Boundary test 4-question structure)

| Boundary | Test | Resolution |
|---|---|---|
| **Claim vs fact-statement** | Is this judgment-bearing OR lookup-shaped? | Judgment-bearing → claim; lookup-shaped → fact-statement |
| **Claim vs work-unit** | Is this atomic assertion OR bounded artifact-container holding many claims? | Atomic → claim; container → work-unit |
| **Claim vs event** | Is this asserted content OR structured emission unit recording that an assertion was made? | Content → claim; emission-record → event (`claim_made` event-kind) |

### Defensibility resolution-granularity test

Defensibility resolves at **claim granularity** per `glossary/defensibility.md` — practitioner doesn't defend a 50-page document as a single defensible blob; they defend each individual claim within. Composability: per-claim defensibility composes work-unit defensibility per §3.

**Validator-side (Cluster D L8 mental-modeling)**: six-months-later challenge tests per-claim individually, NOT whole-output blob. Regulators / opposing counsel / peer reviewers / audit committees challenge specific claims (e.g., specific legal-interpretation claim; specific finding-classification claim); the defensibility test resolves at THAT claim's granularity, not at whole-output granularity. Composability discipline: one indefensible claim taints the whole output regardless of other claims passing.

### Composition with work-unit kind 3-test (subordinate)

Claim 3-test is **SUBORDINATE** to `arch/workflow-work-unit.md` §9 work-unit kind 3-test (foundation-up granularity inheritance):
- Work-unit kind 3-test asks "should THIS work-unit kind exist" (boundedness + archetype-discriminator + lifecycle-distinctiveness per `arch/workflow-work-unit.md` §9)
- Claim 3-test asks "should THIS assertion be treated as a claim within validated work-unit kind"
- Foundation-up: work-unit kind granularity validates first; claim granularity within validated work-unit kind

This composition reflects the bundle hierarchy: work-unit kinds are specialist-defined per `arch/specialist-skill.md` §10; claims compose into work-unit instance output content per Owner B placement; the contained primitive's granularity is evaluated within the validated container's structural conventions.

### Two-tier classification N/A

Claim is content-level (not entity-level); defensibility is property/test (not primitive with instances). Per-primitive tier classification (e.g., domain-anchored vs cross-archetype per `arch/specialist-skill.md` §9 two-tier classification) doesn't apply: cross-archetype shape consistent — planner / lawyer / medical / researcher / auditor all share atomic-defensible-assertion shape per `glossary/claim.md` Cross-archetype illustration. Claim is the atomic-defensible-assertion shape uniformly across archetypes; no tier discriminator surfaces.

§9 two-tier classification N/A documented per template "document N/A explicitly when section is omitted" rule.

## 10. Bundle composition (cluster-conditional; N/A)

**N/A** — neither claim nor defensibility BUNDLES other artifacts. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §10 applies when a primitive in the cluster BUNDLES other artifacts (e.g., specialist BUNDLES skills + entity-kinds + workflows + work-unit-kinds + adapter implementations per `arch/specialist-skill.md` §10).

Claim is content-level atomic assertion within work-unit output content (per `glossary/claim.md`); claims are bundled INTO work-unit instance content, not bundlers themselves. Defensibility is property/test applied to claims (per `glossary/defensibility.md`); not entity-having; doesn't bundle artifacts.

§10 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule (preserves template-anchoring stability for downstream primitive-cluster topics). Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template per-pattern conditional applicability rule: "PRIMITIVE + DERIVED clusters (claim-defensibility): granularity + per-primitive lifecycle ordering likely apply; bundle / marketplace / cross-shape likely N/A" — confirmed N/A per this analysis.

## 11. Marketplace + distribution mechanics (cluster-conditional; N/A)

**N/A** — claim is content-unit IN work-unit; defensibility is property-test; neither independently distributable. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §11 applies when a primitive in the cluster is canonical distributable (e.g., specialist as canonical distributable per `glossary/specialist.md` + `arch/specialist-skill.md` §11).

Claims are workspace-bound deployment-specific content (per `glossary/claim.md` placement at cross-cutting layer within work-unit output content) — NOT distributable Framework C artifacts. Defensibility is property/test applied to claims — NOT a distributable artifact (no manifest of own; no packaging boundary). Cross-deployment portability concerns (claim + defensibility test re-runable across substrate migrations per `arch/substrate.md` §F) are workspace-migration mechanics + audit-trail integrity mechanics per `arch/audit.md` §D, NOT claim-or-defensibility distribution mechanics.

§11 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule.

## 12. Cross-references reservation

Cross-references for this topic are consolidated in §17 below per primitive-cluster topic template convention; this section number reserved as **N/A-parity slot** preserving visual numbering parity with substrate's §12 Transport variation N/A + `arch/specialist-skill.md` §12 reservation + `arch/practitioner.md` §12 reservation + `arch/workflow-work-unit.md` §12 reservation. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template §-numbering convention: "**§12 reserved as N/A-parity slot** (parity with substrate's §12 Transport variation N/A — preserves visual numbering parity across topic-templates; downstream primitive-cluster topic Writers MUST keep §12 reserved as N/A-parity rather than omit-§12 or fill-§12-with-content; prevents template drift)."

## 13. Per-primitive lifecycle ordering (cluster-conditional; APPLIES)

Claim has load-bearing lifecycle ordering distinct from §5 cardinality + lifecycle treatment: production → revision (append-only new event) → finalization → attestation → re-attestation-on-revision; defensibility re-run-able test mechanics. Lifecycle ordering integrates with substrate boot/shutdown phases per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection.

### Claim lifecycle ordering

1. **`claim_made` emission** — claim production fires `claim_made` event; production-phase moment per `glossary/claim.md` lifecycle (CREATED during workflow execution); `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface
2. **Production-phase engaged-authorship sparring events fire DURING production** — sparring sub-mechanisms accessed by skills DURING claim production per `arch/sparring.md` §4 + `glossary/engaged-authorship.md`; events accumulate across claim production (potentially across multiple sessions per `glossary/engaged-authorship.md` lifecycle)
3. **Revision = new `claim_made` event (append-only NOT rewrite)** — claim revision per-version semantics per `glossary/claim.md` "REVISED during review (revision emits new event preserving prior claim state per append-only audit)"; per `arch/audit.md` §B append-only persistence
4. **Finalization moment** — claim finalized at send/sign moment per `glossary/claim.md` lifecycle; signed-claim_made event; practitioner authorship binding per `glossary/authority-binding.md` line 35
5. **Per-claim attestation event fires AT finalization** — attestation-phase per-claim attestation event per `glossary/engaged-authorship.md`; records `actor_kind: human` + practitioner-RECORD identity per `arch/practitioner.md` §4 R-CC-10 (session-bound practitioner)
6. **Re-attest-on-revision** — claim v2 = new engaged-authorship test cycle per `glossary/engaged-authorship.md`; v1's engagement doesn't carry forward to v2 (per-claim per-version semantics)

Defensibility re-run-able test: post-hoc reconstruction event (per `glossary/defensibility.md` "test is re-run-able"; six-months-later or years-later reconstruction via audit-trail Surface §C query API per `arch/audit.md` §C); structural conditions captured at production time persist as audit records and remain testable indefinitely (subject to audit-trail retention policy).

### 6-event-kind catalog candidate (architectural enumeration; Phase 6 lands Pydantic per-event-shape schemas + per-shape event-kind catalog declarations)

| Event-kind | Architectural meaning |
|---|---|
| `claim_made` | Claim production fires; `actor_kind: ai_runtime` + skill identifier; carries claim content |
| `claim_revised` | New event preserving prior state per append-only; `details.previous_event_id` references prior `claim_made` event |
| `claim_finalized` | Finalization moment per `glossary/claim.md`; transition to send/sign-ready state |
| `claim_attested` | Per-claim attestation event per engaged-authorship presence; fires at finalization; `actor_kind: human` + practitioner-RECORD identity |
| `claim_re_attested` | Post-revision attestation event; v2 = new engaged-authorship test cycle per `glossary/engaged-authorship.md` |
| `defensibility_test_run` | Post-hoc reconstruction event per `glossary/defensibility.md` re-run-ability; records test invocation + outcome (passed / failed) + reconstructed reasoning chain reference |

The 6-event-kind catalog is candidate-level at this ARCH topic; per-event-shape Pydantic schemas + per-shape catalog declarations land in Phase 6 audit-emission catalog territory (per `arch/audit.md` §E event-kind catalog management) + Phase 6 spec.

### Cross-pattern destruction inheritance

Claims inherit work-unit's `instance_content_dissolution_policy: archive | delete-with-audit` per `arch/workflow-work-unit.md` §13 + `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 (same field; cross-pattern coherence preserved). NO separate per-claim destruction policy: claims are bundled INTO work-unit content per `glossary/claim.md`; destruction follows work-unit instance destruction.

- **Default**: archival preserves practitioner work + axis-3 authorship preservation + 6-months-later defensibility test re-runable for claims (cross-pattern coherence with `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 + `arch/workflow-work-unit.md` §13 archival-as-default)
- **Opt-in**: deletion-with-audit policy declared at `workspace.md` level (workspace declares `instance_content_dissolution_policy: archive | delete-with-audit` per cross-pattern coherence convention; same field shape across all 4 primitive-cluster ARCH topics)
- Per-shape policy may restrict the opt-in (practitioner-shape policy may prohibit deletion-with-audit per defensibility-critical concern)

### Boot integration

Per `ARCHITECTURE.md` §6 composite boot subsection + `arch/audit.md` §10 boot ordering: **`claim_made` event-kind catalog must register before substrate emits first audit event** per audit-phase 3 step (audit Surface available per `arch/audit.md` §10 boot step 4 — emission API ready BEFORE substrate emits first architectural event); claim event-kind catalog availability ordering integrates with `ARCHITECTURE.md` §6 composite boot subsection step 9 (audit-phase events catalog availability).

The 6-event-kind catalog (claim_made / claim_revised / claim_finalized / claim_attested / claim_re_attested / defensibility_test_run) registers at audit-phase 1 (AuditEvent schema validation per `ARCHITECTURE.md` §6 composite boot subsection); per-shape catalog extensions register at audit-phase 3 (audit Surface available); claim emissions begin flowing at substrate-phase 2+ (substrate emits architectural events via audit Surface).

### Mid-session lifecycle ordering

Mid-session claim production + revision + finalization + attestation are runtime events emitted via audit Surface §A per the 6-event-kind catalog candidate; no special boot ordering. In-flight claim production NOT disrupted by mid-session specialist activation per `glossary/workflow.md` "workflow_instance doesn't gate capability changes" + `arch/specialist-skill.md` §5 mid-session re-binding + `arch/practitioner.md` §5 multi-practitioner concurrent-session handling.

## 14. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| **W1** | Per-claim-kind variation schema (interpretive vs citation vs procedural) | Phase 3.5 schema work + per-archetype claim-kind evidence (per archetype claims surface distinct kind shapes warranting standardization) | Per-claim-kind manifest extension (claim schema additional `kind` field with per-kind structural conventions); cross-link: `arch/workflow-work-unit.md` W3 per-kind structural conventions schema standardization |
| **W2** | Pre-existing-claim ingestion semantics resolution | First legacy-claim import deployment evidence (concrete deployment surfaces re-engagement vs flag-conditional choice) | Per-shape policy declares re-engagement-event vs template-with-attribution mechanism; cross-link: `glossary/engaged-authorship.md` pre-existing-claim ingestion deferred-now-load-bearing (REVISION-flavored EXPANSION elevated from engaged-authorship DR §6 deferred to load-bearing within-cluster commitment) |
| **W3** | Multi-practitioner co-attestation mechanics | Second multi-practitioner deployment surfacing per-shape co-attestation friction | Per-shape co-attestation event-kind shape + attribution chain preservation rules + per-shape required-co-attestation-recipient enforcement; cross-link: `arch/practitioner.md` §14 W4 cross-practitioner workflow handoff + W1 multi-tenant federation |
| **W4** | Cryptographic signing per claim | Phase 6 audit cryptographic chain implementation (parallel to `arch/practitioner.md` W3 practitioner-record signing + `arch/audit.md` §D integrity verification) | Per-claim signing format design fires when Phase 6 audit-trail integrity implementation lands; integrates with `arch/practitioner.md` W3 signing format + `arch/audit.md` §D cryptographic-signature implementation |

## 15. Decision-design provenance

Provenance for this topic lives in DR + HANDOFF + git log per `MAINTENANCE.md` Lens 5 v0.2.1 provenance hygiene + per `coherence-audit` Lens 5. See `docs/decisions/claim-defensibility-arch-topic.md` for sharpening trajectory + Round 1 + Round 2 EXPANSIONS + manufactured-criticism rejections + GLOSSARY back-check verdict + profile-anchored validation cluster citations + Mode 2 composite decomposition rationale.

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: claim + defensibility cluster primitives stay shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz) reality (per `profiles/L5a-planner-pbs-schulz.md` lines 39-52 per-claim source-grounding + sparring + lines 105-115 defensibility under UNB-Stellungnahme challenge + lines 132-138 per-claim attestation cross-archetype generalization risk) grounds the cluster primitives without leaking pioneer specifics into the framework definitions. Cross-archetype illustration in §2 + §3 + §9 anchors framework neutrality (planner B-Plan-Begründung legal-interpretation claims / lawyer brief case-law-applicability claims / medical case-note diagnosis-attribution claims / research manuscript methodology claims / auditor audit-finding control-deficiency claims per `glossary/claim.md` Cross-archetype illustration).

## 16. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.5 | LOCKED |
| Claim-event Pydantic schema + per-shape event-kind catalog | 6 | Mode 3 spec; 6-event-kind catalog candidate per §13 (claim_made / claim_revised / claim_finalized / claim_attested / claim_re_attested / defensibility_test_run); per-shape declarations per `arch/audit.md` §E event-kind catalog management |
| Per-deployment claim production | Workspace deployment (NOT this repo) | Per `MAINTENANCE.md` TOP-LEVEL SCOPE: per-claim production happens at deployment-instance via skills (Mode 1 production-runtime LLM-MD); Phase 6 deployment |
| Per-claim-kind variation schema (W1) | 6 | Per W1 watch-list; awaits Phase 3.5 schema work + per-archetype claim-kind evidence; cross-link: `arch/workflow-work-unit.md` W3 |
| Pre-existing-claim ingestion mechanics (W2) | 5+ | Per W2 watch-list; awaits first legacy-claim import deployment evidence; cross-link: `glossary/engaged-authorship.md` deferred-now-load-bearing |
| Multi-practitioner co-attestation mechanics (W3) | 5+ | Per W3 watch-list; awaits second multi-practitioner deployment surface; cross-link: `arch/practitioner.md` §14 W4 + W1 |
| Cryptographic signing per claim (W4) | 6 | Per W4 watch-list; integrates with `arch/audit.md` §D integrity verification + cryptographic-signature implementation + `arch/practitioner.md` W3 practitioner-record signing |
| Defensibility_test_run reconstruction mechanics | 6 | Per §13 6-event-kind catalog candidate; post-hoc reconstruction event Phase 6 audit-emission catalog territory |
| Workspace serialization / archival format | 6 | Per §13 cross-pattern destruction inheritance from work-unit; archival mechanics per cross-pattern coherence with `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 + `arch/workflow-work-unit.md` §13 |

## 17. Cross-references

- **GLOSSARY**: `claim` (canonical PRIMITIVE atomic accountability-bearing-assertion entry); `defensibility` (canonical DERIVED operational-axis-3-test entry); `engaged-authorship` (cross-cluster DERIVED composing INTO this cluster as Cond #1 operational definition); `authorship-preservation` (axis 3 architectural commitment defensibility tests); `rubber-stamping` (axis-3 failure mode failing Cond #1 attestation-phase); `authority-binding` (per-event actor declaration; per-claim author attribution; one of three architectural sub-aspects); `event` (claims emit `claim_made` events); `actor` (`actor_kind: ai_runtime` for claim authoring + `actor_kind: human` for attestation); `policy` (per-shape audit emission granularity per `arch/audit.md` §14); `practitioner` (accountable for individual claims; defensibility resolves at claim granularity through practitioner attribution); `work-unit` (artifact-container holding N claims); `workflow` (workflow_instance attribution scopes claims; ad-hoc work-unit claims attribute without workflow_instance); `specialist` + `skill` (skills produce claims); `sparring` (sparring fires AT claim granularity; production-phase substrate); `quality-gate` (Pattern A; axis-3 intervention applies engaged-authorship test at attestation moments); `intertwining` + `co-worker` (axis-1 cross-axis; claims are content-units AI co-authors with practitioner); `category-collapse` (general force; cascades into defensibility failure); `answer-machine-ai` / `oracle-ai` / `validator-ai` (axis-2 failure modes failing Cond #1 production-phase); `framework`, `mechanism`, `shape`, `substrate`, `adapter`, `audit`, `session`, `Owner B scope`, `Framework C scope`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept "Audit emission" row (practitioner-shape "Audit granularity = claim-level" row anchors per-claim emission policy); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (source-grounding mechanism gate-enforced structural per `glossary/claim.md`; append-only enforced architecturally per `arch/audit.md` §B); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (claim + defensibility cluster primitives stay shape-neutral; cross-archetype illustration anchors framework neutrality; pioneer-neutrality); `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment claim production happens at deployment-instance via skills; not framework repo); `ARCHITECTURE.md` §6 cross-cutting principles "AI as runtime" + "LLM-instruction tightness for Mode 1 markdown layer" + "Workspace boot + shutdown composite sequence"; `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 3 (multi-axis sub-section + profile-anchored sub-sections); Discipline 4 (cascade-prevention; greenfield-draft + minimize-embedded + cascade-pass + foundation-first); Discipline 10 (greenfield-evaluation of archived sources)
- **Profiles validated**: `G-composability-gate.md` (lines 14-22 multi-mode consumption framing; lines 154-157 cross-shape consumption rules; lines 162-184 architectural concerns surfaced — backup-migration round-trip implicates per-claim portability per W4 cryptographic signing) + `L5a-planner-pbs-schulz.md` (lines 14-17 PBS-Schulz pioneer single-practitioner deployment; lines 39-52 per-claim source-grounding mandatory + sparring during drafting; lines 105-115 deadline-pressure rubber-stamping risk + defensibility under UNB-Stellungnahme challenge — six-months-later test concrete; lines 132-138 per-claim attestation cross-archetype generalization risk + axis-3 defensibility test mechanic) + `L1-specialist-creator.md` (lines 18-29 specialist creator stress-tests cited as Cluster A producer evidence — claim-emission contract surfaces per skill; specialist creator profile validates skills produce claims surface for cross-archetype claim production) + `INDEX.md` D Defer Gate procedure (per `profiles/INDEX.md` "D Gate procedure" — applied to W1-W4 deferrals; mental-modeling-resolves test passed for shape-uniform PRIMITIVE+DERIVED structural articulation; genuine awaited-evidence test passed for per-claim-kind variation + pre-existing-claim ingestion + multi-practitioner co-attestation + cryptographic signing per absence of pioneer evidence)
- **ARCH topics composing with claim + defensibility**: `arch/substrate.md` (Surface §C permission flow records practitioner identity at HITL approval moments for attestation events; Surface §F session/context management persists per-claim state across sessions; §10 boot ordering integration per ARCHITECTURE.md §6 composite subsection); `arch/audit.md` (§A emission API for §13 6-event-kind catalog candidate; §B append-only persistence preserves claim revision per-version semantics; §C query API for cross-claim audit-trail defensibility test reconstruction; §D integrity verification for cryptographic signing per W4; §E event-kind catalog management for per-shape catalog declarations; §10 boot ordering integration; §14 cross-shape policy variation per-shape audit emission granularity composes with claim attribution); `arch/sparring.md` (sparring sub-mechanisms accessed by skills DURING claim production per §4 per-shape activation matrix; sparring events ARE production-phase substrate for engaged-authorship per Cond #1); `arch/adapter.md` (adapters invoked by skills firing during claim production); `arch/specialist-skill.md` (Phase 3.5 first primitive-cluster LOCKED — skills produce claims per §4 composition table claim row; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain); `arch/practitioner.md` (Phase 3.5 second primitive-cluster LOCKED — practitioners accountable for individual claims per §4 composition table; defensibility resolves at claim granularity through practitioner-RECORD attribution; per-claim attestation event records practitioner-RECORD identity for attesting actor); `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster LOCKED — claims emitted during workflow_instance execution attribute to that workflow_instance per §4 composition table; work-unit instance contains N claims; per-claim attestation chain composes through workflow_instance + work-unit instance attribution; cross-pattern destruction inheritance for claims per §13). Forward-references to future Phase 3.5 + Phase 3.6 topics: `arch/quality-gate.md` (Pattern A Phase 3.6 — quality-gate's axis-3 intervention applies engaged-authorship test at attestation moments per `glossary/engaged-authorship.md` quality-gate row; consumes per-claim emission observability for axis-3 rubber-stamping signal at attestation moment); `arch/scope-model.md` (cross-cutting integrator; claims compose into work-unit instance content at Owner B scope); `arch/axis-interactions.md` (cross-cutting integrator; axis-3 PRIMARY anchor for claim + axis-2 cross-axis sparring composition + axis-1 cross-axis co-worker composition)
- **Phase 6 spec target**: `docs/specs/claim.md` (claim-event Pydantic schema; 6-event-kind catalog per §13; per-shape event-kind catalog declarations per `arch/audit.md` §E); `docs/specs/defensibility.md` (defensibility test reconstruction spec; `defensibility_test_run` event-kind shape; cross-deployment evidence preservation per `arch/audit.md` §G)
- **Archived sources** (INPUT only per `disciplines/10-greenfield-evaluation.md` — archive citations name SOURCE where input came from, NOT TEMPLATE where structure transferred; each cited element greenfield-evaluated against current locked vocabulary per Discipline 10): `archive/docs/decisions/audit-trail-v2.md` (`claim_made` event-kind catalog reference cited as INPUT for §13 6-event-kind catalog candidate but NOT transcribed verbatim — archive's prior event_kind catalog includes `decision` / `module_decision` / `user_confirmation` / `entity_minted` etc. with `details:` payload schema; current locked vocabulary aligns event-kinds to current GLOSSARY primitives + minimal event-kind catalog growth per `details:` payload pattern; greenfield-derived 6-event-kind catalog candidate per current PRIMITIVE+DERIVED + lifecycle states per locked GLOSSARY; archive's `convention_applied` field with `git_sha` precedent informs W4 cryptographic signing per claim direction); `archive/docs/decisions/governance-and-identity-sourcing.md` (decision 1 = role primitive at shape-policy per current vocabulary — composes with authority-binding mechanism per per-shape policy declaring trust model parameterizing how authority-binding satisfies shape-specific accountability; decision 2 = native vs adapter mode for practitioner-RECORD source — composes with `arch/practitioner.md` §2.2 mode field; decision 3 = per-deployment uniqueness convention preserved as deployment-side commitment per §7; decision 4 = prose-rules pattern for ID minting cited as deployment-level discipline; greenfield-evaluated against locked `authority-binding` GLOSSARY entry — authority-decision binding per `glossary/authority-binding.md` per-event actor declaration sub-aspect aligns with archive's gate-enforced role check pattern at decision 1)

## 18. Composition table

How claim + defensibility cluster primitives compose with key framework primitives + Pattern A protocols + mechanism classes (one column per cluster primitive — claim + defensibility):

| Composing primitive | Claim composition | Defensibility composition |
|---|---|---|
| **substrate Surface §C** (permission flow) | Substrate Surface §C records practitioner identity at HITL approval moments for attestation events; permission decisions bind to identified human actor per `glossary/authority-binding.md` "authority-decision binding" sub-aspect | Defensibility's Cond #2 reconstructible-reasoning-chain composes through substrate Surface §C permission-flow events (every HITL decision recorded with actor binding) |
| **substrate Surface §F** (session/context management) | Per-claim state persists across sessions via persistent-state mechanism per `glossary/claim.md` lifecycle | Defensibility's re-run-ability persists across sessions + substrate migrations per `arch/substrate.md` §F + cross-deployment evidence per `arch/audit.md` §G |
| **audit mechanism class** (Surface §A emission API) | Claim lifecycle events per §13 catalog (claim_made / claim_revised / claim_finalized / claim_attested / claim_re_attested / defensibility_test_run) flow through audit Surface §A | Defensibility's Cond #2 reconstructible-reasoning-chain composes through audit Surface §A emission (every claim event captured per audit-trail-as-canonical-source per `arch/audit.md` §6) |
| **audit mechanism class** (Surface §B append-only persistence) | Claim revision = new event preserving prior state per append-only audit per `arch/audit.md` §B | Defensibility's re-run-ability preserved via append-only persistence (six-months-later reconstruction reads same event stream as production-time) |
| **audit mechanism class** (Surface §C query API) | Cross-claim audit-trail query pattern for reasoning-chain reconstruction (per-claim reasoning chain via events filtered by claim_id, ordered by timestamp per `arch/audit.md` §C) | Defensibility test mechanic Cond #2: six-months-later reconstruction via audit Surface §C query API; reconstruct historic-claim attribution chain through claim_id + actor_kind + work-unit-id query filters |
| **audit mechanism class** (Surface §D integrity verification) | Per-claim cryptographic signing per W4 awaits Phase 6 audit cryptographic chain implementation | Defensibility's Cond #2 hash-chain integrity guarantees audit-trail unmodified for reconstruction; integrity verification per `arch/audit.md` §D |
| **authority-binding mechanism** | Every `claim_made` event records authoring actor (`actor_kind: ai_runtime` + skill identifier); per-claim author attribution chain composes through skill identifier → specialist → workspace per authority-binding chain (one of three architectural sub-aspects per `glossary/authority-binding.md`) | Reconstructible attribution chain (per-event actor declaration + per-claim author attribution + authority-decision binding) is precondition for defensibility's Cond #2 per `glossary/defensibility.md` composes-with authority-binding row |
| **adapter** (Pattern A protocol) | Adapters invoked by skills firing during claim production per `glossary/skill.md` composes-with adapter row; adapter invocations attributed to claim emission via skill-side MCP audit gate per `arch/substrate.md` §8 dual-emission | Defensibility's Cond #2 captures adapter invocation reasoning chain (every adapter call emitted to audit-trail per per-class event-kind catalog per `arch/adapter.md` §11) |
| **sparring** (mechanism class) | Sparring fires AT claim granularity per `glossary/sparring.md`; per-sub-mechanism sparring events compose into engaged-authorship's production-phase substrate per Cond #1 | Defensibility's Cond #1 engaged-authorship composes through sparring events (production-phase substrate per `glossary/engaged-authorship.md`); without sparring participation → no engaged authorship at production phase → Cond #1 fails per claim |
| **specialist-skill** (Phase 3.5 first primitive-cluster) | Skills produce claims (claim_made events) during work execution per `arch/specialist-skill.md` §4; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain | Defensibility's Cond #2 reconstructible-reasoning-chain composes through skill identifier in audit-trail; Cond #1 engaged-authorship requires skills' sparring sub-mechanism invocations during claim production |
| **practitioner** (Phase 3.5 second primitive-cluster) | Practitioners accountable for individual claims per `glossary/practitioner.md` composes-with claim row; per-claim attestation event records practitioner-RECORD identity for attesting actor per `arch/practitioner.md` §4 | Defensibility test resolves at practitioner-author granularity per `glossary/defensibility.md`; practitioner-RECORD persistence + dormant-not-deleted lifecycle (per `arch/practitioner.md` §13) preserves historic-claim attribution for re-runable defensibility tests |
| **workflow + work-unit** (Phase 3.5 third primitive-cluster) | Claims emitted during workflow_instance execution attribute to that workflow_instance per `arch/workflow-work-unit.md` §4 + `glossary/workflow.md` composes-with claim row; ad-hoc work claims attribute to work-unit + session without workflow_instance attribution; one work-unit instance contains N claims | Defensibility's claim-granularity resolution composes from per-claim tests across work-unit's outputs per `glossary/defensibility.md` composes-with work-unit row; one indefensible claim taints the work-unit's output |
| **engaged-authorship** (DERIVED axis-3) | Per-claim engagement events fire DURING claim production (production-phase) + AT claim finalization (attestation-phase) per `glossary/engaged-authorship.md`; per-claim per-version semantics | Operational definition of defensibility's Cond #1 (two-phase composite per-claim test); per-claim engaged-authorship + per-claim source-grounding + per-claim audit-trail-completeness compose into per-claim defensibility |
| **rubber-stamping** (axis-3 failure mode) | Claims rubber-stamped at attestation lack engaged-authorship; per-claim defensibility fails when rubber-stamping occurred at finalization per `glossary/rubber-stamping.md` composes-with claim row | Directly fails defensibility's Cond #1 engaged-authorship attestation-phase; axis-3 failure mode contrast to engaged-authorship 2-phase composite test |
| **answer-machine AI / oracle AI / validator AI** (axis-2 failure modes) | Claims produced under axis-2 collapse less defensible per claim per axis-2 failure-mode entries composes-with claim rows | Axis-2 failure modes fail defensibility's Cond #1 engaged-authorship production-phase via collapsed sparring (no engagement during reasoning → no engaged authorship at production phase → Cond #1 fails per claim) |
| **category-collapse** (general force) | General force; manifestations on any axis cascade into per-claim defensibility failure per `glossary/category-collapse.md` composes-with claim row | Cross-axis force quality-gate guards against; manifestations on any axis cascade into defensibility failure per `glossary/category-collapse.md` composes-with defensibility row |
| **quality-gate** (Pattern A; Phase 3.6 forthcoming) | Quality-gate fires per-claim at finalization (per shape policy granularity per `glossary/quality-gate.md` composes-with claim row); engaged-authorship's quality signals feed quality-gate's drift detection | Quality-gate's axis-3 intervention applies defensibility test at attestation moments per `glossary/defensibility.md` composes-with quality-gate row; quality-gate is structural counter to category-collapse drift at checkpoint moments |
| **Pattern A protocols** (substrate / adapter / quality-gate) | Claim composes with substrate Surface §C/§F (permission flow + session/context management); adapter invocation attributed via skill-side audit emission; quality-gate Pattern A composes with per-claim observability per Phase 3.6 | Defensibility composes with all Pattern A protocols via audit-trail Surface integration (substrate Surface §F session/context for cross-deployment; adapter Surface §C permission for HITL approval; quality-gate Pattern A composes with per-claim attestation observability per Phase 3.6) |
| **Pattern B primitives** (specialist + skill / workflow + work-unit) | Skills produce claims per Pattern B specialist-skill nesting (per `arch/specialist-skill.md` §10); claims compose into work-unit instance content per Pattern B work-unit (per `arch/workflow-work-unit.md` §3) | Defensibility test resolves at claim granularity within Pattern B work-unit container; per-claim defensibility composes work-unit defensibility per composability commitment per §3 |
| **Pattern C primitives** (practitioner) | Per-claim attestation event records practitioner-RECORD identity per Pattern C bipartite RECORD aspect per `arch/practitioner.md` §4 | Defensibility test asks "will THIS practitioner defend THIS output six months from now" per `glossary/defensibility.md`; practitioner is the role the test resolves against |
