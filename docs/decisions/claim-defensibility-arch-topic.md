# Decision record: Claim + defensibility ARCH topic (Phase 3.5 fourth primitive-cluster)

## 1. Status

**ACCEPTED** (session 30, 2026-05-04). 2-round decision-design-sharpening (Round 1 full monty + Round 2 user-triggered; USER-LOCKED en bloc per Note 58 cluster-execution pattern + user grant of autonomous authority through Wave-2.5 + HANDOFF Note 59). Mode 2 upfront-known composite decomposition per `decision-design-sharpening` v0.10.0 §Two decomposition modes — 6 sub-decisions tightly coupled; single composite DR (sub-decisions have no independent meaning outside the composite).

Sharpening rounds metadata:
- Round 1 (full monty): 6 sub-decisions inventoried + sharpened with foundation-up dependency ordering (sub-decision-batched: 4 + 6 + 5 + 5 + 4 + 6 = 30 EXPANSIONS)
- Round 2 (user-triggered): cross-cutting + schema-detail refinements (E1-E10 = 10 EXPANSIONS; 1 REVISION-flavored EXPANSION E4 pre-existing-claim ingestion elevation)
- STABLE-AT-ROUND-2 verdict per `decision-design-sharpening` §Lock + persist signals (Q3 DECAY CONFIRMED ~67%; Q5 specific termination signal named below; Q4 no unaddressed pass)
- LOCK-HARD target-type per skill §Step 4 target-type modifier (architectural decision; cascades hard if revised)

## 2. Owner

Phase 3.5 — fourth primitive-cluster ARCH topic (4 of 6 primitive-cluster + cross-cutting integrator topics). Anchors **PRIMITIVE + DERIVED topic-template-class** (parallel to `arch/substrate.md` anchoring Pattern A 12+7 template + `arch/specialist-skill.md` anchoring primitive-cluster Pattern B + atomic-primitive 12+5 template + `arch/practitioner.md` anchoring Pattern C topic-template-class + `arch/workflow-work-unit.md` anchoring two-Pattern-B topic-template-class). PRIMITIVE+DERIVED-specific conditional applicability rules surface here per per-pattern conditional applicability rules in `MAINTENANCE.md` Layer 3 Primitive-cluster topic template (granularity / per-primitive lifecycle ordering apply; bundle / marketplace likely N/A). Cited as precedent for downstream primitive-cluster topics where PRIMITIVE+DERIVED class conditional applicability surfaces.

## 3. Related

**Composes with**:
- `docs/decisions/workflow-work-unit-arch-topic.md` (just-locked attribution chain; per-claim attestation chain composes against validated workflow_instance + work-unit instance attribution surface per cluster-boundary commitment)
- `docs/decisions/practitioner-arch-topic.md` (cross-axis attribution chain; per-claim attestation event records practitioner-RECORD identity per `arch/practitioner.md` §4 R-CC-10)
- `docs/decisions/specialist-skill-arch-topic.md` (skills produce claims per `arch/specialist-skill.md` §4 composition table claim row; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain)
- `docs/decisions/engaged-authorship-operational-definition.md` (cross-cluster DERIVED composing INTO this cluster as Cond #1 operational definition; 2-phase composite per-claim test)
- `docs/decisions/audit-arch-topic.md` (Surface §A emission API for §13 6-event-kind catalog candidate per E2/E3; Surface §B append-only persistence preserves claim revision per-version semantics; Surface §C query API for cross-claim audit-trail defensibility test reconstruction; Surface §D integrity verification for cryptographic signing per W4; §10 boot ordering integration for `claim_made` event-kind catalog availability per E10; §14 cross-shape policy variation per-shape audit emission granularity composes with claim attribution per E5)
- `docs/decisions/sparring-arch-topic.md` (sparring fires AT claim granularity per `glossary/sparring.md` + §4 per-shape activation matrix; sparring events ARE production-phase substrate for engaged-authorship per Cond #1)
- `docs/decisions/substrate-arch-topic.md` (Surface §C permission flow records practitioner identity at HITL approval moments for attestation events; Surface §F session/context for cross-deployment per E6)
- `docs/decisions/greenfield-rederivation-pause.md` (Step 1.A Phase 2 GLOSSARY foundational vocabulary lock incl. claim + defensibility + engaged-authorship + rubber-stamping)
- `docs/decisions/quality-gate-scope-lock.md` (Pattern A; Phase 3.6 forthcoming — quality-gate's axis-3 intervention applies engaged-authorship test at attestation moments per `glossary/engaged-authorship.md` quality-gate row)

**GLOSSARY entries** (locked; cited extensively):
- `claim` (canonical PRIMITIVE atomic accountability-bearing-assertion entry; 4-property structure per E1)
- `defensibility` (canonical DERIVED operational-axis-3-test entry; 3-condition test)
- `engaged-authorship` (cross-cluster DERIVED composing INTO this cluster as Cond #1 operational definition per E7)
- `authorship-preservation` (axis 3 architectural commitment defensibility tests)
- `rubber-stamping` (axis-3 failure mode failing Cond #1 attestation-phase)
- `authority-binding` (per-event actor declaration; per-claim author attribution; one of three architectural sub-aspects)
- `event` (claims emit `claim_made` events)
- `actor` (`actor_kind: ai_runtime` for claim authoring + `actor_kind: human` for attestation)
- `policy` (per-shape audit emission granularity per `arch/audit.md` §14)
- `practitioner` + `work-unit` + `workflow` + `specialist` + `skill` + `sparring` + `quality-gate` + `intertwining` + `co-worker` + `category-collapse` + `answer-machine-ai` + `oracle-ai` + `validator-ai` + `session` + `workspace` (all composes-with rows cited)

**Forward-references** (future Phase 3.5 + Phase 3.6 topics):
- `arch/quality-gate.md` (Pattern A Phase 3.6 — quality-gate's axis-3 intervention applies engaged-authorship test at attestation moments; consumes per-claim emission observability for axis-3 rubber-stamping signal at attestation moment)
- `arch/scope-model.md` (cross-cutting integrator; claims compose into work-unit instance content at Owner B scope)
- `arch/axis-interactions.md` (cross-cutting integrator; axis-3 PRIMARY anchor for claim + axis-2 cross-axis sparring composition + axis-1 cross-axis co-worker composition)

**Disciplines applied**:
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (source-grounding mechanism gate-enforced structural per `glossary/claim.md`; append-only enforced architecturally per `arch/audit.md` §B)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (claim + defensibility cluster primitives stay shape-neutral; cross-archetype illustration anchors framework neutrality; pioneer-neutrality)
- `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment claim production happens at deployment-instance via skills; not framework repo)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 3 (multi-axis sub-section + profile-anchored sub-sections); Discipline 4 (cascade-prevention; greenfield-draft + minimize-embedded + cascade-pass + foundation-first); Discipline 8 (foundation-up ordering); Discipline 10 (greenfield-evaluation of archived sources)

**Archived sources** (INPUT only per Discipline 10 — greenfield-evaluated against current locked vocabulary; NOT transcribed as template):
- `archive/docs/decisions/audit-trail-v2.md` (`claim_made` event-kind catalog reference cited as INPUT for §13 6-event-kind catalog candidate but NOT transcribed verbatim — archive's prior event_kind catalog includes `decision` / `module_decision` / `user_confirmation` / `entity_minted` etc. with `details:` payload schema; current locked vocabulary aligns event-kinds to current GLOSSARY primitives + minimal event-kind catalog growth per `details:` payload pattern; greenfield-derived 6-event-kind catalog candidate per current PRIMITIVE+DERIVED + lifecycle states per locked GLOSSARY; archive's `convention_applied` field with `git_sha` precedent informs W4 cryptographic signing per claim direction)
- `archive/docs/decisions/governance-and-identity-sourcing.md` (decision 1 = role primitive at shape-policy per current vocabulary — composes with authority-binding mechanism per per-shape policy declaring trust model parameterizing how authority-binding satisfies shape-specific accountability; decision 2 = native vs adapter mode for practitioner-RECORD source — composes with `arch/practitioner.md` §2.2 mode field; decision 3 = per-deployment uniqueness convention preserved as deployment-side commitment per §7; decision 4 = prose-rules pattern for ID minting cited as deployment-level discipline; greenfield-evaluated against locked `authority-binding` GLOSSARY entry — authority-decision binding per `glossary/authority-binding.md` per-event actor declaration sub-aspect aligns with archive's gate-enforced role check pattern at decision 1)

## 4. Context

Phase 3.5 fourth primitive-cluster ARCH topic. Prior to this DR, Phase 3.5 first primitive-cluster topic (specialist-skill) LOCKED at commit `f6bab6e`; Phase 3.5 second primitive-cluster topic (practitioner) LOCKED at commit `7ffe93a`; Phase 3.5 third primitive-cluster topic (workflow-work-unit) LOCKED at commit `3b187ea` per `ARCHITECTURE.md` §7; Pattern A protocol topics + mechanism-class topics LOCKED in Phase 3.4.

**Why claim-defensibility chosen fourth** (foundation-up per Discipline 8): claim-defensibility cluster composes with already-locked specialist-skill (skills produce claims per `arch/specialist-skill.md` §4 composition table claim row) + practitioner (per-claim attestation event records practitioner-RECORD identity per `arch/practitioner.md` §4 R-CC-10) + workflow-work-unit (claims attribute to workflow_instance + work-unit instance per `arch/workflow-work-unit.md` §4 composition table claim row). Locking claim-defensibility fourth means per-claim attestation chain mechanics lock against already-validated upstream attribution surfaces. Reverse ordering would force claim-defensibility to forward-reference unlocked workflow_instance + work-unit instance + practitioner + specialist + skill primitives.

**Why PRIMITIVE+DERIVED topic-template-class anchored here**: claim is PRIMITIVE atomic content-unit (per locked GLOSSARY); defensibility is DERIVED property/test (per locked GLOSSARY). The cluster pairs a PRIMITIVE with its operational-test DERIVED partner — structurally distinct from Pattern B + atomic-primitive (specialist-skill cluster) + Pattern C bipartite (practitioner cluster) + two-Pattern-B (workflow-work-unit cluster). PRIMITIVE+DERIVED-specific conditional applicability surfaces here (granularity tests + per-primitive lifecycle ordering APPLY for PRIMITIVE+DERIVED clusters; bundle / marketplace N/A — neither claim nor defensibility BUNDLES other artifacts; cross-shape policy variation APPLIES per per-claim audit emission granularity + engaged-authorship enforcement + source-grounding strictness + attestation-event mandatoriness + quality-gate signal-set + cross-deployment portability all vary per shape). Future PRIMITIVE+DERIVED primitive-cluster topics inherit this DR's anchor for conditional applicability rules.

**What the decision-design phase needed to resolve**:
- PRIMITIVE+DERIVED topic-template-class confirmation (12+5 extends without variation; per-pattern conditional applicability rules)
- Per-primitive structural overview (claim PRIMITIVE 4-property structure + claim-event composition + revision per-version semantics; defensibility DERIVED 3-condition operational test + claim-granularity resolution + composability + Q1-Q4 boundary tests + re-run-ability)
- Cross-primitive composition WITHIN cluster (reciprocal asymmetry + composability-of-defensibility-test + per-claim attestation chain mechanics + pre-existing-claim ingestion semantics)
- Per-primitive lifecycle ordering (claim lifecycle 6-event-kind catalog candidate + cross-pattern destruction inheritance + boot integration)
- Granularity tests (claim 3-test SUBORDINATE to work-unit kind 3-test + defensibility resolution-granularity test + two-tier classification N/A)
- Cross-shape policy variation 6-row matrix + cross-axis composition + W1-W4 watch-list

## 5. Decision

Six sub-decisions per Mode 2 composite decomposition (sub-decisions have no independent meaning outside the composite; foundation-up dependency ordering applied within the composite).

### SD-1: Topic template applicability — anchors PRIMITIVE + DERIVED topic-template-class

**Decision**: 12+5 primitive-cluster template extends to PRIMITIVE+DERIVED clusters **without variation**. **PRIMITIVE+DERIVED topic-template-class anchored at this topic** (parallel to substrate Pattern A 12+7 anchor + specialist-skill primitive-cluster Pattern B + atomic-primitive 12+5 anchor + practitioner Pattern C 12+5 anchor + workflow-work-unit two-Pattern-B 12+5 anchor).

**PRIMITIVE+DERIVED-specific conditional applicability** (per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template per-pattern conditional applicability rules):
- §8 Cross-shape policy variation: APPLIES (per-claim audit emission granularity + engaged-authorship enforcement + source-grounding strictness + attestation-event mandatoriness + quality-gate signal-set + cross-deployment portability shape-policy-mediated)
- §9 Granularity tests: APPLIES (claim has 3-property granularity discriminator per `glossary/claim.md`; defensibility has resolution-granularity discriminator per `glossary/defensibility.md`)
- §10 Bundle composition: N/A (neither claim nor defensibility BUNDLES other artifacts; claim is content-level atomic assertion; defensibility is property/test)
- §11 Marketplace + distribution mechanics: N/A (claim is content-unit IN work-unit; defensibility is property-test; neither independently distributable)
- §12: N/A-parity (preserved per locked template convention)
- §13 Per-primitive lifecycle ordering: APPLIES (claim lifecycle ordering + 6-event-kind catalog candidate + cross-pattern destruction inheritance + boot integration)

**Why N/A documented explicitly**: per `MAINTENANCE.md` Layer 3 template "document N/A explicitly when section is omitted" rule. DO NOT skip section numbering — keep §10/§11/§12 as N/A sections preserving template-anchoring stability for downstream PRIMITIVE+DERIVED primitive-cluster topics.

**Total expected**: 18 sections (12 common + 3 conditional applies (§8 + §9 + §13) + 2 N/A documented (§10 + §11) + §12 N/A-parity). Target: ~400-450 lines.

### SD-2: Per-primitive structural overview (§2)

**Decision**: §2 = 2 sub-sections (no manifest schemas — claim isn't Framework C bundle; defensibility isn't entity).

**§2.1 Claim PRIMITIVE (atomic; cross-cutting)** — 4 distinguishing properties (atomic + accountability-bearing + judgment-bearing + source-grounded per E1 explicit "atomic" 4th property; vs `glossary/claim.md` 3-property listing where atomicity is implicit in What-it-is-NOT). Claim-event composition (`claim_made` event-kind from archived `audit-trail-v2.md`, greenfield-evaluated against locked `event` + `actor`); claim revision per-version semantics (append-only at audit level; v1 doesn't carry to v2 per `glossary/engaged-authorship.md`); production / revision / finalization moments per `glossary/claim.md` lifecycle.

**§2.2 Defensibility DERIVED (property/test; cross-cutting)** — 3-condition operational test (engaged-authorship Cond #1 / reconstructible-reasoning-chain Cond #2 / source-grounded Cond #3); claim-granularity resolution + composability per `glossary/defensibility.md` (one indefensible claim taints work-unit's output); 4 boundary questions (Q1-Q3 practitioner-experiential + Q4 structural-observable); re-run-ability via audit-trail reconstruction per `glossary/defensibility.md` cardinality + lifecycle.

### SD-3: Cross-primitive composition WITHIN cluster (§3) + Composition with framework primitives OUTSIDE cluster (§4) + per-claim attestation chain mechanics

**Decision**: §3 articulates **4 load-bearing structural commitments** (parallel-count to workflow-work-unit's 4):

1. **Reciprocal asymmetry** — claim atomic content-unit; defensibility property-applied-to-claim (NOT entity-having; NOT 1:1 reciprocal — parallel to engaged-authorship 2-phase asymmetry vs rubber-stamping attestation-only failure per Lens 6 reciprocal-asymmetry pattern). One-way directional composition (defensibility-tests-claims, never claims-bundle-defensibility).

2. **Composability-of-defensibility-test** — per-claim defensibility composes work-unit defensibility per `glossary/defensibility.md`; if every claim passes the test, the work-unit's output passes; ONE indefensible claim taints the whole output. Composability commitment locks granularity-resolution + aggregation discipline.

3. **Per-claim attestation chain (mechanics)** — claim_made emission → production-phase engaged-authorship sparring events (axis-2 substrate) → claim revision events (append-only) → finalization → per-claim attestation event (axis-3-anchored; `actor_kind: human` + practitioner-RECORD identity per `arch/practitioner.md` §4 R-CC-10) → composes INTO work-unit attribution chain per `arch/workflow-work-unit.md` §3 + `arch/practitioner.md` cross-axis composition. Per-claim per-version semantics.

4. **Pre-existing-claim ingestion semantics** (REVISION-flavored EXPANSION elevated from engaged-authorship DR §6 deferred-now-load-bearing per E4) — re-engagement event on import OR template-with-attribution policy per shape; preserves engaged-authorship per-claim per-version semantics for legacy claims at framework level. Awaits W2 first legacy-claim import deployment evidence for per-shape mechanics.

**Engaged-authorship cross-cluster composition** (per E7) — engaged-authorship is a DERIVED entry living at GLOSSARY (per `glossary/engaged-authorship.md`); its operational mechanics compose INTO claim-defensibility cluster as Cond #1 of defensibility's three-condition test. Documented explicitly to preserve relationship between primitives clustered together (claim + defensibility) + DERIVED entries living at GLOSSARY whose operational mechanics compose INTO this cluster (engaged-authorship Cond #1; rubber-stamping axis-3 failure mode failing Cond #1 attestation-phase; answer-machine + oracle + validator AI axis-2 failure modes failing Cond #1 production-phase).

**§4 Composition with framework primitives OUTSIDE cluster** — claim composes-with table (work-unit / workflow_instance / audit Surface §A/§C / sparring Surface §D / authority-binding mechanism / practitioner / specialist-skill / session / event PRIMITIVE / actor / shape / policy); defensibility composes-with table (authority-binding precondition for Cond #2 + audit Surface §A/§B Cond #2 + sparring Surface §D Cond #1 enabler + engaged-authorship DERIVED Cond #1 operational definition + source-grounding mechanism Cond #3 Phase 3.3 detail + rubber-stamping axis-3 failure mode failing Cond #1 attestation-phase + answer-machine/oracle/validator AI axis-2 failure modes failing Cond #1 production-phase + category-collapse general force + quality-gate Pattern A axis-3 intervention applies engaged-authorship test; Phase 3.6 forward).

### SD-4: §5 cardinality + lifecycle + §13 per-primitive lifecycle ordering + cross-pattern destruction inheritance + boot integration

**Decision**: §5 + §13 cluster-conditional treatment.

**§5 Claim cardinality**: N per work-unit (typically dozens-to-hundreds per `glossary/claim.md`); creator = AI-runtime via skills (skills produce claims per `arch/specialist-skill.md` §4); owner = work-unit (bundled INTO content); destructor = work-unit destruction policy (NO separate per-claim destruction); mutability = append-only at audit level + draft-mutable until finalization.

**§5 Defensibility cardinality**: N/A (property/test, not entity-having); resolves at claim granularity per `glossary/defensibility.md`.

**§13 Lifecycle ordering**: claim_made emission → production-phase engaged-authorship events fire DURING production → revision = new claim_made event (append-only NOT rewrite) → finalization moment → attestation-phase per-claim attestation event fires AT finalization → re-attest-on-revision (v2 = new engaged-authorship test cycle); defensibility re-run-able test (six-months-later via audit-trail reconstruction).

**§13 6-event-kind catalog candidate** (per E2/E3):
- `claim_made` (production fires; `actor_kind: ai_runtime` + skill identifier)
- `claim_revised` (new event preserving prior state)
- `claim_finalized` (finalization moment per E2)
- `claim_attested` (per-claim attestation per engaged-authorship presence per E2)
- `claim_re_attested` (post-revision per E2)
- `defensibility_test_run` (post-hoc reconstruction event per E3)

Catalog flagged as schema-detail Phase 3.3 audit-emission catalog territory + Phase 6 spec.

**Cross-pattern destruction coherence**: claims inherit work-unit's `instance_content_dissolution_policy: archive | delete-with-audit` per `arch/workflow-work-unit.md` §13 + `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 (same field; cross-pattern coherence preserved per E8 destruction inheritance — claims NOT destroyed independently). Per-shape policy may restrict opt-in per defensibility-critical concern.

**Boot integration** (per E10): `claim_made` + claim event-kind catalog must register before substrate emits first audit event per `arch/audit.md` §10 boot ordering + `ARCHITECTURE.md` §6 composite boot subsection step 9 audit-phase events catalog availability.

### SD-5: Granularity tests (§9)

**Decision**: §9 contains claim 3-test (SUBORDINATE to work-unit kind 3-test) + defensibility resolution-granularity test + two-tier classification N/A.

**Claim 3-test** (subordinate to work-unit kind 3-test per `arch/workflow-work-unit.md` §9; foundation-up granularity inheritance per E9):
1. **Accountability-bearing** (practitioner can be professionally/regulatorily challenged)
2. **Judgment-bearing** (NOT lookup-shaped — fact-statements aren't claims even when sourced)
3. **Source-grounded** (every claim traces to source — framework-level guarantee)

Boundary tests: vs fact-statement (judgment-bearing test) / vs work-unit (atomic vs container) / vs event (content vs emission-record).

**Defensibility resolution-granularity test**: defensibility resolves at claim granularity per `glossary/defensibility.md`; composability per-claim → per-work-unit; one indefensible claim taints output. Validator side (Cluster D L8 mental-modeling): six-months-later challenge tests per-claim individually, NOT whole-output blob.

**Two-tier classification N/A**: claim is content-level not entity-level; cross-archetype shape consistent — planner / lawyer / medical / researcher / auditor all share atomic-defensible-assertion shape per `glossary/claim.md` Cross-archetype illustration. No per-primitive tier discriminator surface.

**Composition with work-unit kind 3-test (subordinate)**: claim 3-test SUBORDINATE to `arch/workflow-work-unit.md` §9 work-unit kind 3-test (foundation-up): work-unit kind validates first; claim granularity within validated work-unit kind.

### SD-6: §8 cross-shape policy variation 6-row matrix + cross-axis composition + W1-W4 watch-list

**Decision**: §8 6-row matrix + cross-axis composition table in §4 + §7 operational concerns + W1-W4 watch-list.

**§8 Shape-uniform** (NOT shape-policy-mediated):
- Claim PRIMITIVE 4-property structure
- Defensibility 3-condition operational test
- Claim-granularity resolution + composability
- Claim revision per-version semantics
- Reciprocal asymmetry + per-claim attestation chain mechanics

**§8 Shape-policy-mediated** (6-row matrix; parallel to workflow-work-unit §8 6-row):

| Dimension | practitioner-shape | autonomous-business-shape | personal-OS-shape |
|---|---|---|---|
| **claim-emission audit granularity per shape** | Claim-level (per `arch/audit.md` §14 practitioner-shape) | Action-level (per `arch/audit.md` §14 autonomous-business) | Light (per `arch/audit.md` §14 personal-OS) |
| **engaged-authorship enforcement per shape** (per `glossary/engaged-authorship.md` Framework-level enforcement) | Friction/block fail-closed | Programmatic block | Audit-only |
| **per-claim source-grounding strictness per shape** (per E5) | MANDATORY no-unsourced | Per-action source aggregation OK | Optional |
| **attestation-event mandatoriness per shape** | MANDATORY per-claim | Programmatic | Optional |
| **quality-gate signal-set per shape** (axis-3 observability source per shape policy per `glossary/engaged-authorship.md` quality-gate row) | Full engagement signals | Threshold-based programmatic signals | Light drift signals |
| **cross-deployment claim portability per shape** (per E6 — defensibility re-run-ability requires cross-substrate portability per practitioner-shape) | MANDATORY cross-substrate (per `arch/substrate.md` §F + `arch/audit.md` cross-deployment evidence) | Bounded by deployment | N/A |

**Cross-axis composition** (in §4 composition table):
- **axis-3 PRIMARY anchor**: claim is unit-of-defense per `glossary/claim.md`; defensibility IS the axis-3 success criterion test
- **axis-2 sparring orthogonal**: sparring fires AT claim granularity per `glossary/sparring.md`
- **axis-1 cross-axis**: claims are content-units AI co-authors with practitioner per `glossary/intertwining.md` + `glossary/co-worker.md`

**§14 Watch-list** (4 items; each names specific external signal + resolution mechanism per `MAINTENANCE.md` no-defer principle):
- **W1**: Per-claim-kind variation schema (interpretive vs citation vs procedural per engaged-authorship DR §6 defer; awaited signal = Phase 3.5 schema work + per-archetype claim-kind evidence; resolution = per-claim-kind manifest extension; cross-link `arch/workflow-work-unit.md` W3)
- **W2**: Pre-existing-claim ingestion semantics resolution (re-engagement-event vs flag-conditional choice; awaited signal = first legacy-claim import deployment evidence; cross-link to `glossary/engaged-authorship.md` deferred-now-load-bearing per E4)
- **W3**: Multi-practitioner co-attestation mechanics (cross-link to `arch/practitioner.md` W4 cross-practitioner workflow handoff + W1 multi-tenant federation; awaited signal = second multi-practitioner deployment surfacing per-shape co-attestation friction)
- **W4**: Cryptographic signing per claim (parallel to `arch/practitioner.md` W3 practitioner-record signing + `arch/audit.md` §D integrity verification; awaited signal = Phase 6 audit cryptographic chain implementation)

**§7 Pre-implementation operational concerns** (architectural-level enumeration; Phase 6 territory):
- Per-claim-kind variation schema (W1)
- Pre-existing-claim ingestion mechanics (W2)
- Cryptographic signing per claim (W4)
- Multi-practitioner co-attestation persistence (W3)
- `defensibility_test_run` event-kind reconstruction mechanics (per §13 6-event-kind catalog candidate; per E3)
- Per-deployment claim ID uniqueness convention (prose-rule pattern per archived `governance-and-identity-sourcing.md` decision 3 + decision 4 greenfield-evaluated)

## 6. Sharpening provenance

### Round 1 (full monty)

EXPANSIONS surfaced (count: 30 = 4 + 6 + 5 + 5 + 4 + 6 — one EXPANSION-batch per sub-decision; Mode 2 upfront-known composite per `decision-design-sharpening` v0.10.0 §Two decomposition modes "Sub-decision inventory" step):

- **SD-1 EXPANSIONS** (4): PRIMITIVE+DERIVED topic-template-class confirmation; per-pattern conditional applicability rules (§8/§9/§13 APPLY; §10/§11 N/A; §12 N/A-parity); per-topic section count expectation 18; downstream PRIMITIVE+DERIVED precedent
- **SD-2 EXPANSIONS** (6): claim PRIMITIVE 4-property structure (atomic + accountability-bearing + judgment-bearing + source-grounded); claim-event composition (`claim_made` event-kind greenfield-evaluated against locked event + actor); claim revision per-version semantics (append-only; v1 doesn't carry to v2); production / revision / finalization moments; defensibility 3-condition operational test (Cond #1 engaged-authorship + Cond #2 reconstructible-reasoning-chain + Cond #3 source-grounded); claim-granularity resolution + composability + Q1-Q4 boundary tests + re-run-ability via audit-trail reconstruction
- **SD-3 EXPANSIONS** (5): reciprocal asymmetry load-bearing articulation (parallel to engaged-authorship 2-phase asymmetry vs rubber-stamping per Lens 6); composability-of-defensibility-test (per-claim composes work-unit; one indefensible claim taints output); per-claim attestation chain mechanics (6-step ordered emissions); pre-existing-claim ingestion semantics framework-level handling; engaged-authorship cross-cluster composition (DERIVED entry composes IN this cluster as Cond #1)
- **SD-4 EXPANSIONS** (5): claim cardinality (N per work-unit) + creator/owner/destructor + mutability append-only; defensibility cardinality N/A (property/test); claim lifecycle ordering (production → revision → finalization → attestation → re-attest-on-revision); 6-event-kind catalog candidate (claim_made / claim_revised / claim_finalized / claim_attested / claim_re_attested / defensibility_test_run); cross-pattern destruction inheritance from work-unit + boot integration step 9
- **SD-5 EXPANSIONS** (4): claim 3-test (3 properties + boundary tests vs fact-statement / vs work-unit / vs event); defensibility resolution-granularity test (validator side six-months-later); composition with work-unit kind 3-test (subordinate); two-tier classification N/A (cross-archetype shape consistent)
- **SD-6 EXPANSIONS** (6): §8 6-row shape-policy-mediated matrix; cross-axis composition (axis-3 PRIMARY anchor + axis-2 cross-axis + axis-1 cross-axis); §7 6-category operational concerns enumeration; W1 per-claim-kind variation; W2 pre-existing-claim ingestion semantics; W3 multi-practitioner co-attestation + W4 cryptographic signing per claim

### Round 2 (user-triggered)

Cross-cutting + schema-detail refinements (per `decision-design-sharpening` §Round 2 layered coverage observation: cross-cutting + schema details emphasized):

**Cross-cutting refinements (E1-E10)** — 10 items:
- **E1**: §2.1 claim 4-property structure — explicit "atomic" 4th property (vs `glossary/claim.md` 3-property listing; atomicity implicit in What-it-is-NOT)
- **E2**: claim_finalized + claim_attested + claim_re_attested event-kind candidates — schema-detail flag Phase 3.3 audit-emission catalog
- **E3**: defensibility_test_run as event-kind candidate — post-hoc reconstruction event flag Phase 3.3 + Phase 6 spec
- **E4** (REVISION-flavored): Pre-existing-claim ingestion elevated from engaged-authorship DR §6 defer to LOAD-BEARING within-cluster commitment SD-3 #4 — REVISION-flavored EXPANSION (5th cumulative cross-cluster)
- **E5**: Per-shape source-grounding-strictness as §8 row (autonomous-business per-action source aggregation insufficient for accountability-bearing claim-level)
- **E6**: Cross-deployment claim portability per shape as §8 row (defensibility re-run-ability requires cross-substrate portability per practitioner-shape)
- **E7**: Engaged-authorship cross-cluster composition (DERIVED entry's 2-phase test composes WITHIN claim-defensibility cluster as Cond #1 operational definition; document explicit cross-cluster relationship)
- **E8**: §13 destruction inheritance — claims NOT destroyed independently; inherit work-unit `instance_content_dissolution_policy` (preserves cross-pattern coherence with specialist-skill + practitioner + workflow-work-unit)
- **E9**: §9 SUBORDINATE-to-work-unit-3-test (foundation-up granularity inheritance per workflow-work-unit §9 precedent)
- **E10**: §13 boot integration — `claim_made` event-kind catalog must register before substrate emits first audit event per `arch/audit.md` §10 + `ARCHITECTURE.md` §6 composite boot

**Round 2 EXPANSIONS count**: 10 substantive findings (E1-E10). Per `decision-design-sharpening` §Empirical density check: Round 1 = 30 EXPANSIONS (sub-decision-batched); Round 2 = 10 EXPANSIONS — drops ~67% (DECAY CONFIRMED region per density-behavior table; ≥50% drop signals STABLE candidate per Q3).

### Manufactured-criticism rejections

Per `decision-design-sharpening` §Manufactured-comfort counter-test + §Pareto calibration: reject refinements that aren't Pareto-improving OR that surface manufactured-criticism territory.

Cumulative count: 5 (Round 1 + Round 2 ST):

- **R1 rejected**: defensibility as PRIMITIVE not DERIVED — REJECTED (parallel to engaged-authorship DR R1 rejection; defensibility is property/test not entity-having; locked GLOSSARY classification preserved per `glossary/defensibility.md` Class: DERIVED tag)
- **R2 rejected**: Merge claim + defensibility into single ARCH topic with engaged-authorship as third member — REJECTED (engaged-authorship is cross-cluster DERIVED; lives at GLOSSARY with operational mechanics composing INTO claim-defensibility per E7 cross-cluster composition; merging would violate primitive-cluster boundary discipline + engaged-authorship's cross-cluster nature)
- **R3 rejected**: Defensibility test resolution at work-unit granularity not claim — REJECTED (locked GLOSSARY `defensibility` "claim granularity"; revising would break locked vocabulary; per `glossary/defensibility.md` "test resolves at claim granularity")
- **R4 rejected**: Single-phase engaged-authorship within claim-defensibility (not 2-phase) — REJECTED (engaged-authorship DR R3 already rejected; locked 2-phase composite preserved per `glossary/engaged-authorship.md` Canonical body; revising would break locked vocabulary + engaged-authorship DR's locked 2-phase composite)
- **R5 rejected**: Per-claim-kind variation as §3 within-cluster commitment vs W1 watch-list — REJECTED (per-claim-kind variation genuinely awaited-evidence-dependent; surface as W1 not now-load-bearing per D Gate procedure; mental-modeling-resolves test passed for shape-uniform PRIMITIVE+DERIVED structural articulation; specific per-claim-kind shapes await per-archetype claim-kind evidence)

### GLOSSARY back-check verdict

Per `MAINTENANCE.md` Bidirectional cascade + `decision-design-sharpening` v0.5.0 GLOSSARY back-check at Round 2 termination.

**Verdict**: CLEAN — no retro-fits needed. 1 candidate evaluated and rejected as schema-detail-not-glossary-grade:

- **"Per-claim attestation chain" framing** evaluated for glossary-grade structural fact: result NOT glossary-grade per Bidirectional cascade rule (operational-mechanics ARCH territory per Lens 5 v0.2.1 placement; "Schema details / per-impl mechanics / operational procedures / per-shape variations are NOT glossary-grade — they stay in ARCH/DR/spec"); per-claim attestation chain mechanics live in ARCH topic §3 cross-primitive composition + §13 lifecycle ordering, NOT a glossary-grade structural fact deserving its own primitive entry. Unlike specialist-skill cluster which surfaced specialist-namespace mechanic R-N-1 (a vocabulary distinction load-bearing across entries; glossary-grade), per-claim attestation chain is operational-mechanics not vocabulary-distinction.

**Pattern observation**: PRIMITIVE+DERIVED narrower surface produces less GLOSSARY-grade material — parallel to practitioner cluster Note 57 verdict ("cleaner Round 2 GLOSSARY back-check than Note 56 specialist-skill which surfaced specialist-namespace mechanic R-N-1 (narrower Pattern C surface produces less GLOSSARY-grade material)"). PRIMITIVE+DERIVED surface narrower than Pattern B + atomic-primitive (specialist-skill cluster's bundle composition + namespace mechanics surfaced cross-cutting structural facts); claim + defensibility's relationship is property-test-applied-to-primitive (singular structural commitment already captured in locked GLOSSARY classification of defensibility as DERIVED).

### Profile-anchored validation

Per `decision-design-sharpening` v0.5.0+ profile-anchored validation + `profiles/INDEX.md` cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators).

**4 cluster representatives Read** (≥3 cluster coverage requirement; FULL DETAIL profile content cited NOT cluster letters):

**Cluster A Producers** — `profiles/L1-specialist-creator.md` (skills produce claim-emitting skills; SKELETON profile fleshed-on-demand for this validation):
- L1 lines 18-29 specialist creator stress-tests (intended-stress-test enumeration): "claim-emission contract surfaces per skill" — validates SD-3 per-claim attestation chain mechanics (skills produce claims; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain per `arch/specialist-skill.md` §4 composition table claim row)
- L1's specialist creator profile validates that skill-emitting `claim_made` events compose with per-claim attestation chain at deployment-instance integration time
- Verdict: covered (skeleton profile provides sufficient evidence for PRIMITIVE+DERIVED cluster validation per `profiles/INDEX.md` skeleton-fleshing-on-demand strategy; L1 mental-modeling: specialist creator authoring claim-emitting skills must declare claim_made emission contract per skill — handles cross-archetype claim production)

**Cluster B Deployers + Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` (pioneer; multi-cluster member):
- L5a lines 14-17 PBS-Schulz pioneer single-practitioner deployment: validates SD-3 per-claim attestation chain mechanics + SD-6 per-shape policy variation matrix (practitioner-shape claim-level audit granularity + MANDATORY no-unsourced source-grounding)
- L5a lines 39-52 per-claim source-grounding mandatory + sparring during drafting + claim_made events emitted per substantive claim: validates SD-2 claim-event composition + claim revision per-version semantics + SD-3 production-phase engaged-authorship sparring events
- L5a lines 105-115 deadline-pressure rubber-stamping risk + defensibility under UNB-Stellungnahme challenge — six-months-later test concrete: validates SD-2 defensibility 3-condition test + Q1-Q3 practitioner-experiential boundary tests + re-run-ability via audit-trail reconstruction; pioneer evidence anchors defensibility test mechanic concretely
- L5a lines 132-138 per-claim attestation cross-archetype generalization risk + axis-3 defensibility test mechanic: validates SD-1 cross-archetype-shape-consistency + SD-5 two-tier classification N/A (planner / lawyer / medical / researcher / auditor all share atomic-defensible-assertion shape per `glossary/claim.md` Cross-archetype illustration)
- Verdict: covered

**Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` + L5d auditor mental-modeling (per `profiles/INDEX.md` D Defer Gate procedure; L5d skeleton fleshed-on-demand):
- L5a planner B-Plan-Begründung claims (legal-interpretation / proportionality / nature-protection / mitigation per `glossary/claim.md` Cross-archetype illustration): validates SD-2 claim PRIMITIVE 4-property structure + cross-archetype shape consistency
- L5d auditor mental-modeling: audit-finding claims (control-deficiency / materiality-assessment / recommendation per `glossary/claim.md` Cross-archetype illustration); cross-archetype shape consistent — auditor archetype shares atomic-defensible-assertion shape with planner archetype per `glossary/claim.md`
- Verdict: covered (cross-archetype shape consistent per `glossary/claim.md` validates SD-2 cross-archetype generalization)

**Cluster D Validators** — `profiles/G-composability-gate.md` (cross-cutting validation gate; Cluster D member; transitively-satisfied via specialist's packaging boundary):
- G lines 14-22 multi-mode consumption framing: validates SD-1 12+5 template extension; claim is content-unit IN work-unit (NOT independently distributable per SD-1 §11 N/A); defensibility is property/test (NOT distributable artifact per SD-1 §11 N/A)
- G lines 154-157 cross-shape consumption rules: validates SD-6 §8 cross-shape policy variation matrix shape-policy-mediated rows; shape policy declares per-shape claim-emission audit granularity + engaged-authorship enforcement + source-grounding strictness + attestation-event mandatoriness + quality-gate signal-set + cross-deployment portability
- G lines 162-184 architectural concerns surfaced: backup-migration round-trip implicates per-claim portability per W4 cryptographic signing direction; cross-deployment evidence + audit-trail integrity per `arch/audit.md` §G validates SD-6 cross-deployment claim portability per shape (E6 row)
- Verdict: transitively-satisfied via specialist's packaging boundary (G's L1-L4 producer artifact concerns satisfied at specialist DEFINITION level per `arch/specialist-skill.md` §11 + §10; claims compose into work-unit instance content owned by deployed specialist instance — claim portability inherits via specialist's packaging boundary + work-unit instance attribution chain)

**Cluster D Validators (defensibility-test-from-evaluator-side L8 mental-modeling)** — defensibility primitive's three structural conditions tested against post-hoc validator perspective per `profiles/L8-auditor-reviewer-posthoc.md` (SKELETON; mental-modeling-resolved per D Gate):
- L8 evaluator side: regulators / opposing counsel / peer reviewers / audit committees challenge specific claims under six-months-later test; defensibility resolves at claim granularity per `glossary/defensibility.md` (Q1-Q3 practitioner-experiential tests + Q4 structural-observable test) — validates SD-5 defensibility resolution-granularity test (validator side tests per-claim individually, NOT whole-output blob)
- L8 mental-modeling: defensibility primitive's three structural conditions (engaged-authorship Cond #1 + reconstructible-reasoning-chain Cond #2 + source-grounded Cond #3) tested against post-hoc validator perspective; six-months-later reconstruction via audit-trail Surface §C query API per `arch/audit.md` §C
- Verdict: PASS (defensibility primitive's three structural conditions tested against post-hoc validator perspective via mental-modeling; D Gate satisfied per genuine awaited-evidence test for L8 skeleton fleshing — concrete L8 challenge-event evidence awaits second-deployment defensibility-challenge surface)

**Cluster D Validators (gate component)** — D Defer Gate per `profiles/INDEX.md` "D Gate procedure":
- W1 per-claim-kind variation: external-information test passes (specific signal = Phase 3.5 schema work + per-archetype claim-kind evidence); effort-asymmetry test passes (per-claim-kind variation genuinely awaited-evidence-dependent; specific per-claim-kind shapes await per-archetype claim-kind evidence); D Gate satisfied → W1 watch-list with resolution mechanism
- W2 pre-existing-claim ingestion semantics: external-information test passes (specific signal = first legacy-claim import deployment evidence); effort-asymmetry test passes (per-shape mechanics design before first-deployment friction risks wrong-design); D Gate satisfied → W2 watch-list with resolution mechanism
- W3 multi-practitioner co-attestation: external-information test passes (specific signal = second multi-practitioner deployment surface; pioneer is solo per L5a); effort-asymmetry test passes (per-shape co-attestation mechanics design before second-deployment friction risks wrong-design); D Gate satisfied → W3 watch-list with resolution mechanism
- W4 cryptographic signing per claim: external-information test passes (specific signal = Phase 6 audit cryptographic chain implementation); effort-asymmetry test passes (cryptographic signing format awaits Phase 6 audit cryptographic chain implementation); D Gate satisfied → W4 watch-list with resolution mechanism
- Verdict: D Gate satisfied per genuine awaited evidence (W1 + W2 + W3 + W4) + mental-modeling-resolves rejection (R5 — per-claim-kind variation genuinely awaited-evidence-dependent, surface as W1 not now-load-bearing)

### Decomposition mode

Per `decision-design-sharpening` v0.10.0 §Two decomposition modes Mode 2:
- **Trigger satisfied**: 6 sub-decisions visible at framing time (not emergent from drift); foundation-up dependencies identifiable (SD-1 template enables SD-2-6 to inherit shape; SD-2 2-sub-section structure enables SD-3 cross-primitive composition; SD-3 enables SD-4 lifecycle ordering composition; SD-5 granularity tests subordinate to work-unit kind 3-test from `arch/workflow-work-unit.md` §9; SD-6 cross-shape policy variation + cross-axis composition + W1-W4 layers on top of validated cluster shape)
- **Sub-decision inventory at start**: 6 sub-decisions listed before Round 1 (SD-1 → SD-6); composite decomposition mode declared upfront
- **Foundation-up dependency ordering**: SD-1 (template confirmation) locks first; SD-2 (2-sub-section structure) builds on SD-1; SD-3 (cross-primitive composition) builds on SD-2 articulation; SD-4 (lifecycle ordering) builds on SD-2 + SD-3; SD-5 (granularity tests) subordinate to work-unit kind 3-test; SD-6 (cross-shape + cross-axis + watch-list) layers on validated cluster shape
- **Per-sub-decision sharpening**: each got Round 1 + Round 2 sweep within the composite (no per-sub-decision split into separate rounds)
- **Synthesis pass at end**: this DR + ARCH §18 composition table is the cross-sub-decision coherence pass
- **Single composite DR**: chosen per Mode 2 §Single composite DR — sub-decisions have no independent meaning outside the composite; claim + defensibility cluster is the unit, not 6 independent decisions

### Layered coverage observation

Per `decision-design-sharpening` §Layered coverage observation: each round emphasizes different architectural concern layer.

- **Round 1**: emphasized template + structural overview + composition (architectural decisions per skill §Layered coverage Round 1 emphasis); 30 EXPANSIONS sub-decision-batched
- **Round 2**: emphasized cross-cutting (§8 cross-shape policy variation rows E5+E6 + §13 destruction inheritance E8 + §13 boot integration E10) + schema details (event-kind catalog candidates E2+E3 + boundary tests E1) — matches skill §Layered coverage Round 2 emphasis (cross-cutting + schema details)
- **No Round 3**: narrow architectural surface per skill §Empirical sweet-spot pattern (PRIMITIVE+DERIVED narrower than Pattern B + atomic-primitive specialist-skill cluster); operational concerns (per-claim-kind variation + pre-existing-claim ingestion mechanics + cryptographic signing implementation + multi-practitioner co-attestation persistence) belong to Phase 6 pre-implementation per skill §Phase 1 → Phase 2 transition

### Empirical density check

Per `decision-design-sharpening` §Empirical density check: count substantive findings (HIGH + MEDIUM impact; exclude cosmetic / NO-ACTION) for current round vs previous round.

- Round 1: 30 EXPANSIONS (sub-decision-batched: 4+6+5+5+4+6)
- Round 2: 10 EXPANSIONS (E1-E10)
- Density behavior: drops ~67% — DECAY CONFIRMED → STABLE candidate per Q3 (≥50% drop)

ARCHITECTURAL-DECISION surface per skill §Surface-type declaration. ~10 EXPANSIONS Round 2 within sweet-spot. 0 architectural REVISIONS (E4 is REVISION-flavored EXPANSION not pure architectural reversal — pre-existing-claim ingestion ELEVATED from defer to load-bearing within-cluster commitment; structural elevation of implicit-to-explicit per Note 56-58 R-CC-10 pattern). STABLE LOCK.

### REVISION/EXPANSION classification self-check

Per `decision-design-sharpening` v0.6.0 self-check at Round 2 termination + BACKLOG watch-list "3-tier discriminator codification".

**REVISION-flavored EXPANSIONS surfaced** (load-bearing structural elevations):
- **E4** (pre-existing-claim ingestion elevated from engaged-authorship DR §6 deferred to LOAD-BEARING within-cluster commitment SD-3 #4) — REVISION-flavored EXPANSION (structural elevation of implicit-to-explicit pattern; parallels `arch/practitioner.md` R-CC-1 boot ordering elevation + `arch/workflow-work-unit.md` R-CC-10 snapshot pattern elevation)

**Cumulative count for awaited 3-tier signal**: 1 REVISION-flavored EXPANSION in this composite. Combined with `arch/specialist-skill.md` DR's 2 REVISION-flavored EXPANSIONS + `arch/practitioner.md` DR's 1 REVISION-flavored EXPANSION + `arch/workflow-work-unit.md` DR's 1 REVISION-flavored EXPANSION = **5 cumulative cross-DR REVISION-flavored EXPANSIONS** across Phase 3.5 primitive-cluster decisions.

**Trip threshold for cumulative-count signal**: ≥3 trips per BACKLOG watch-list "3-tier REVISION/EXPANSION discriminator codification" entry. **Threshold continues** (5 ≥ 3 — increased from 4 at workflow-work-unit DR per Note 58); **flag continues for Coherence-audit C2** at Phase 3.5 close to evaluate whether 3-tier codification is now warranted across primitive-cluster topic class. USER pushback / cascade-work-lag signals NOT yet materialized per skill detection mechanisms; continue 2-tier within current composite.

**Pure REVISIONS** (architectural pivots changing existing decisions): 0. E4 is EXPANSION-with-load-bearing-implications, not pure architectural reversal.

### Termination signal (STABLE-AT-ROUND-2)

Per `decision-design-sharpening` §Round termination signals + §Honest termination test Q1-Q5:

- **Q1 (count)**: Round 1 = 30 EXPANSIONS (sub-decision-batched: 4+6+5+5+4+6); Round 2 = 10 EXPANSIONS (E1-E10)
- **Q2 (decay)**: Round 1 → Round 2 = 30 → 10 (drops ~67%; DECAY CONFIRMED region per density-behavior table; ≥50% drop signals STABLE candidate per Q3)
- **Q3 (density behavior)**: DECAY CONFIRMED per ≥67% drop; Round 2 surfaced cross-cutting + schema-detail refinements (per skill §Layered coverage observation Round 2 emphasis); no Round 3 architectural-pattern-surfacing pending
- **Q4 (specific unaddressed pass)**: NONE — all 4 profile clusters covered (A + B + C + D); G Gate transitively-satisfied via specialist's packaging boundary; D Gate fired (W1 + W2 + W3 + W4 satisfied); cross-cutting + schema details exhausted at decision-design-phase
- **Q5 (specific termination signal)**: NARROW ARCHITECTURAL SURFACE per `decision-design-sharpening` §Empirical sweet-spot pattern (PRIMITIVE+DERIVED narrower than Pattern B + atomic-primitive per fewer applicable conditional sections — 3 APPLY same as workflow-work-unit + practitioner; matches `arch/practitioner.md` DR Note 57 termination signal); operational concerns (per-claim-kind variation + pre-existing-claim ingestion mechanics + cryptographic signing implementation + multi-practitioner co-attestation persistence + defensibility_test_run reconstruction mechanics) belong to Phase 6 pre-implementation per §Phase 1 → Phase 2 transition
- **Lock + persist signal**: STABLE per Q3 DECAY CONFIRMED + Q5 specific termination signal + Q4 no-unaddressed-pass + manufactured-comfort counter-test passed (operational concerns explicitly deferred per §Layered coverage observation Round 4+ DEFER to Phase 2)

## 7. Composition with existing architecture

This decision composes with prior locked architecture:

- **Pattern A protocols** (substrate / adapter; sparring + audit mechanism classes per Phase 3.4 close): claim + defensibility composes with substrate Surface §C (permission flow records practitioner identity at HITL approval moments for attestation events) + §F (session/context management persists per-claim state across sessions per E6 cross-deployment portability); with audit Surface §A skill-side emission for §13 6-event-kind catalog candidate + §B append-only persistence preserves claim revision per-version semantics + §C query API for cross-claim audit-trail defensibility test reconstruction + §D integrity verification for cryptographic signing per W4 + §E event-kind catalog management for per-shape catalog declarations + §10 boot ordering integration per E10 + §14 cross-shape policy variation per-shape audit emission granularity composes with claim attribution per E5; with adapter §2 per-class Surfaces consumed by skills firing during claim production; with sparring §4 per-shape activation matrix (sparring fires AT claim granularity per `glossary/sparring.md`; production-phase substrate for engaged-authorship per Cond #1).

- **Pattern B specialist-skill primitive cluster** (per `arch/specialist-skill.md` Phase 3.5 first primitive-cluster lock): skills produce claims (claim_made events) during work execution per `arch/specialist-skill.md` §4 composition table claim row; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain.

- **Pattern C practitioner primitive cluster** (per `arch/practitioner.md` Phase 3.5 second primitive-cluster lock): practitioners are accountable for individual claims per `glossary/practitioner.md` composes-with claim row; per-claim attestation event records practitioner-RECORD identity for attesting actor per `arch/practitioner.md` §4 R-CC-10 (session-bound practitioner); defensibility test asks "will THIS practitioner defend THIS output six months from now" per `glossary/defensibility.md`.

- **Two-Pattern-B workflow-work-unit primitive cluster** (per `arch/workflow-work-unit.md` Phase 3.5 third primitive-cluster lock): claims emitted during workflow_instance execution attribute to that workflow_instance per `arch/workflow-work-unit.md` §4 composition table + `glossary/workflow.md` composes-with claim row; work-unit instance contains N claims per `glossary/work-unit.md`; per-claim attestation chain composes through workflow_instance + work-unit instance attribution; cross-pattern destruction inheritance for claims per E8 (claims inherit work-unit's `instance_content_dissolution_policy` per `arch/workflow-work-unit.md` §13).

- **engaged-authorship operational definition** (per `docs/decisions/engaged-authorship-operational-definition.md` Phase 3.1 lock): cross-cluster DERIVED entry's 2-phase composite test composes WITHIN claim-defensibility cluster as Cond #1 operational definition per E7; engaged-authorship lives at GLOSSARY but its operational mechanics compose INTO this cluster.

- **authority-binding mechanism** (per `glossary/authority-binding.md` from Phase 3.4 C1 cascade): every `claim_made` event records authoring actor (`actor_kind: ai_runtime` + skill identifier); per-claim author attribution chain composes through skill identifier → specialist → workspace per authority-binding chain (one of three architectural sub-aspects per `glossary/authority-binding.md`); reconstructible attribution chain is precondition for defensibility's Cond #2.

- **`ARCHITECTURE.md` §6 composite boot subsection**: `claim_made` event-kind catalog availability ordering integrates with composite boot subsection step 9 (audit-phase events catalog availability per E10).

- **`MAINTENANCE.md` Layer 3 Primitive-cluster topic template** (locked per `arch/specialist-skill.md` DR + `MAINTENANCE.md` Layer 3 §3 Primitive-cluster topic template subsection): PRIMITIVE+DERIVED topic-template-class anchored at this topic per per-pattern conditional applicability rules (granularity / per-primitive lifecycle ordering APPLY for PRIMITIVE+DERIVED clusters; bundle / marketplace N/A — neither claim nor defensibility BUNDLES other artifacts; cross-shape policy variation APPLIES). Future PRIMITIVE+DERIVED primitive-cluster topics inherit this DR's anchor for conditional applicability rules.

- **TOP-LEVEL DESIGN PRINCIPLES §1 (structural over conventional)**: source-grounding mechanism gate-enforced structural per `glossary/claim.md` (every claim traces to source — framework-level guarantee); append-only enforced architecturally per `arch/audit.md` §B (claim revision = new event, not rewriting previous) — both exemplify structural-over-conventional discipline.

- **TOP-LEVEL DESIGN PRINCIPLES §2 (pioneer-neutrality)**: claim + defensibility cluster primitives stay shape-neutral / archetype-neutral / pioneer-neutral; pioneer (PBS-Schulz) reality grounds the cluster primitives without leaking pioneer specifics (Bauleitplanung / B-Plan-Begründung / UNB / Stellungnahme do NOT appear in primitive definitions; cross-archetype illustration in §2 + §3 + §9 anchors framework neutrality per planner / lawyer / medical / researcher / auditor archetypes per `glossary/claim.md` Cross-archetype illustration).

## 8. Constraints flowing to downstream commitments

- **Phase 3.5 future primitive-cluster topics** (cross-cutting integrators last; `arch/scope-model.md` + `arch/axis-interactions.md`): inherit primitive-cluster 12+5 template per SD-1 + per-pattern conditional applicability pattern (document N/A explicitly per template rule; preserve §12 N/A-parity reservation); PRIMITIVE+DERIVED topic-template-class anchored here serves as precedent for conditional applicability when future PRIMITIVE+DERIVED primitive-cluster topics emerge
- **Phase 3.5 cross-cutting integrators** (`arch/scope-model.md` + `arch/axis-interactions.md`; LAST per `ARCHITECTURE.md` §5 reading order): scope-model topic locks Owner B scope category for claims composing into work-unit instance content; axis-interactions topic locks claim as axis-3 PRIMARY anchor + cross-axis composition table per SD-6
- **Phase 3.6 `arch/quality-gate.md`**: consumes per-claim emission observability for axis-3 rubber-stamping signal at attestation moment per `glossary/quality-gate.md` + `glossary/engaged-authorship.md` quality-gate row; quality-gate Pattern A composes with per-claim attestation event observability + per-claim source-grounding completeness (axis-3 intervention applies engaged-authorship test at attestation moments)
- **Phase 3.3 audit-emission catalog must include**: `claim_made` + `claim_revised` + `claim_finalized` + `claim_attested` + `claim_re_attested` + `defensibility_test_run` event-kinds per §13 6-event-kind catalog candidate (per E2/E3); per-shape catalog declarations per `arch/audit.md` §E event-kind catalog management
- **Phase 3.5 specialist-skill claim-emission contract per skill** (forward to L1 specialist creator profile fleshing): skills declare `claim_made` emission contract per skill (per `arch/specialist-skill.md` §4 composition table claim row); per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain
- **Phase 3.6 quality-gate axis-3 intervention applies engaged-authorship test at attestation moments**: quality-gate's drift detection consumes per-claim emission observability + per-claim attestation event presence
- **Phase 6 specs** (`docs/specs/claim.md` + `docs/specs/defensibility.md`): inherit claim-event Pydantic schema per §13 6-event-kind catalog candidate; defensibility test reconstruction spec per `defensibility_test_run` event-kind shape; per-claim-kind variation schema (per W1) + per-shape event-kind catalog declarations per `arch/audit.md` §E
- **Phase 6 deployment** (per `MAINTENANCE.md` TOP-LEVEL SCOPE: PBS-Schulz workspace deployment): per-deployment claim production happens at deployment-instance via skills (Mode 1 production-runtime LLM-MD); per-deployment claim ID uniqueness convention prose; cryptographic signing per claim implementation per W4
- **Wave-2 Cascade-Writer commit** (anticipated tight coupling): GLOSSARY downstream — claim + defensibility + engaged-authorship Composes-with rows + See sections + ARCH §17 references; ARCHITECTURE.md §7 NEW lock entry + §2 row 3.5 update (3 of 6 → 4 of 6) + §3 doc structure status table update (7 of 11 → 8 of 11); peer ARCH §17/§19 reciprocal back-mentions: substrate + audit + adapter + sparring + specialist-skill + practitioner + workflow-work-unit; MAINTENANCE.md Layer 3 PRIMITIVE+DERIVED topic-template-class ANCHOR codification + per-topic count expectation row update; BACKLOG.md cascade
- **BACKLOG.md cascade**: W1 (per-claim-kind variation schema) → Phase 6 spec territory per D Gate; W2 (pre-existing-claim ingestion semantics resolution) → Phase 5+ first-legacy-claim-import-deployment-evidence signal (cross-link to engaged-authorship DR §6 deferred-now-load-bearing); W3 (multi-practitioner co-attestation mechanics) → Phase 5+ second-multi-practitioner-deployment-surface signal (composes with `arch/practitioner.md` §14 W4 + W1); W4 (cryptographic signing per claim) → Phase 6 audit cryptographic chain implementation (parallel to `arch/practitioner.md` W3 practitioner-record signing + `arch/audit.md` §D); cross-DR cumulative REVISION-flavored count (1 here + 2 in `arch/specialist-skill.md` DR + 1 in `arch/practitioner.md` DR + 1 in `arch/workflow-work-unit.md` DR = 5) flagged for Coherence-audit C2 evaluation of 3-tier discriminator codification (trip threshold continues: 5 ≥ 3)

## 9. Files touched

Wave 1 (this DR commit + ARCH topic):
- `arch/claim-defensibility.md` (NEW; primitive-cluster 12+5 ARCH topic; PRIMITIVE+DERIVED topic-template-class anchor)
- `docs/decisions/claim-defensibility-arch-topic.md` (THIS file; composite DR; Mode 2 sub-decisions)

Cascade Wave 2 scope (deferred to Wave-2 Cascade-Writer per `arch/specialist-skill.md` DR §9 + `arch/practitioner.md` DR §9 + `arch/workflow-work-unit.md` DR §9 Wave-2 cascade pattern precedent; anticipated):

**A. GLOSSARY downstream cascade**:
- `glossary/claim.md` See section update (placeholder text replaced with anchored `arch/claim-defensibility.md` reference per Phase 3.5 fourth primitive-cluster lock; parallel to glossary/specialist + glossary/practitioner + glossary/workflow + glossary/work-unit Wave-2 cascades per Notes 56 + 57 + 58)
- `glossary/defensibility.md` See section update (parallel; placeholder text replaced with anchored `arch/claim-defensibility.md` reference)
- `glossary/engaged-authorship.md` See section reciprocal mention (cross-cluster DERIVED composing INTO claim-defensibility cluster as Cond #1; explicit cross-cluster relationship per E7)
- `glossary/authority-binding.md` See section reciprocal mention (per-claim author attribution chain composes through claim_made event; potentially — if cross-claim attribution warrants explicit back-link per Cascade-Writer scope determination)

**B. Peer ARCH §17/§19 reciprocal back-mentions** (Lens 6 reciprocal symmetry; per Note 56 + Note 57 + Note 58 cluster Wave-2 cascade precedent):
- `arch/substrate.md` §19 (added `arch/claim-defensibility.md` reference — substrate Surface §C permission flow records practitioner identity at HITL approval moments for attestation events; Surface §F session/context management persists per-claim state across sessions per E6)
- `arch/audit.md` §19 (added `arch/claim-defensibility.md` reference — Surface §A emission API for §13 6-event-kind catalog candidate per E2/E3; Surface §B append-only persistence preserves claim revision per-version semantics; Surface §C query API for cross-claim audit-trail defensibility test reconstruction; Surface §D integrity verification for cryptographic signing per W4; §10 boot ordering integration per E10; §14 cross-shape policy variation per-shape audit emission granularity composes with claim attribution per E5)
- `arch/adapter.md` §19 (added `arch/claim-defensibility.md` reference — adapters invoked by skills firing during claim production per `glossary/skill.md` composes-with adapter row)
- `arch/sparring.md` §19 (added `arch/claim-defensibility.md` reference — sparring sub-mechanisms accessed by skills DURING claim production per §4 per-shape activation matrix; sparring events ARE production-phase substrate for engaged-authorship per Cond #1)
- `arch/specialist-skill.md` §17 (forward-reference upgraded to backward-reference per Note 56 + Note 57 + Note 58 cleanup discipline — claim-defensibility-reference recasts from "Forward-references to future Phase 3.5 topics" to "Phase 3.5 fourth primitive-cluster LOCKED"; skills produce claims per §4 composition table claim row; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain)
- `arch/practitioner.md` §17 (forward-reference upgraded to backward-reference — claim-defensibility-reference recasts from "Forward-references to future Phase 3.5 topics" to "Phase 3.5 fourth primitive-cluster LOCKED"; per-claim attestation event records practitioner-RECORD identity for attesting actor per §4 R-CC-10; defensibility resolves at claim granularity through practitioner-RECORD attribution)
- `arch/workflow-work-unit.md` §17 (forward-reference upgraded to backward-reference — claim-defensibility-reference recasts from "Forward-references to future Phase 3.5 topics" to "Phase 3.5 fourth primitive-cluster LOCKED"; claims emitted during workflow_instance execution attribute to that workflow_instance per §4 composition table claim row; work-unit instance contains N claims; per-claim attestation chain composes through workflow_instance + work-unit instance attribution)

**C. ARCHITECTURE.md updates**:
- `ARCHITECTURE.md` §7 NEW lock entry: "Claim + defensibility ARCH topic (Phase 3.5 fourth primitive-cluster) — LOCKED" (positioned after workflow-work-unit entry, before Phase 3.1 closed entry; covers PRIMITIVE+DERIVED topic-template-class anchor + 2-sub-section per-primitive structural overview + 4 cross-primitive composition commitments + per-claim attestation chain mechanics + cross-pattern destruction inheritance + 6-event-kind catalog candidate + claim 3-test SUBORDINATE to work-unit kind 3-test + defensibility resolution-granularity test + per-shape policy variation 6-row matrix + W1-W4 watch-list + composes-with substrate §C/§F + audit §A/§B/§C/§D/§10/§14 + adapter + sparring + specialist-skill + practitioner + workflow-work-unit + authority-binding mechanism + engaged-authorship cross-cluster + cross-axis composition axis-3 PRIMARY + axis-2 + axis-1)
- `ARCHITECTURE.md` §2 Phase 3 sub-phase status table row 3.5 update (reflects fourth primitive-cluster LOCKED — claim-defensibility; PRIMITIVE+DERIVED topic-template-class anchor; 2 cross-cutting integrator topics remain)
- `ARCHITECTURE.md` §3 Doc structure status table update (7 of 11 → 8 of 11 drafted: substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility)

**D. MAINTENANCE.md Layer 3 Primitive-cluster topic template subsection**:
- Per-topic section count expectation row updated for claim-defensibility: marked as ANCHOR for PRIMITIVE+DERIVED topic-template-class; "12 common + 3 conditional applies (§8 + §9 + §13) + 2 N/A documented (§10 + §11) + §12 N/A-parity = 18 total"
- Per-pattern conditional applicability bullet updated: PRIMITIVE+DERIVED clusters marked as ANCHOR per `arch/claim-defensibility.md`; "granularity + per-primitive lifecycle ordering APPLIES; cross-shape policy variation APPLIES; bundle / marketplace N/A documented explicitly (claim is content-unit IN work-unit not bundler; defensibility is property/test not entity-having); 12+5 template extends WITHOUT variation"

**E. BACKLOG.md cascade**:
- Phase 3.5 row resolution: claim-defensibility topic marked RESOLVED with cluster commits `<Wave-1 commit hash>` (Wave-1) → `<Wave-2 cascade commit hash>` (Wave-2 cascade commit hash; resolved at Wave-2 commit landing) + execution-pattern signal + DR + profile-cluster validation citations + HANDOFF Note 59 forward-reference
- Phase 5 ROADMAP entries added: "Pre-existing-claim ingestion semantics resolution" (W2; cross-link to engaged-authorship DR §6 deferred-now-load-bearing) + "Multi-practitioner co-attestation mechanics" (W3; composes with `arch/practitioner.md` W4 + W1)
- Phase 6 watch-list entries added: "Per-claim-kind variation schema" (W1; cross-link to `arch/workflow-work-unit.md` W3) + "Cryptographic signing per claim" (W4; integrates with `arch/audit.md` §D + `arch/practitioner.md` W3) + "Defensibility_test_run reconstruction mechanics" (per §13 6-event-kind catalog candidate)
- Cross-cutting "3-tier REVISION/EXPANSION discriminator codification" watch-list cumulative count update (5 REVISION-flavored EXPANSIONS across 4 cluster-executions: specialist-skill = 2 + practitioner = 1 + workflow-work-unit = 1 + claim-defensibility = 1; **trip threshold continues: 5 ≥ 3** — increased from 4 at workflow-work-unit DR per Note 58; flag continues for Coherence-audit C2 evaluation post-Phase-3.5 close per `disciplines/09-coherence-audit-cadence.md`)

**Wave-2 cascade applied** (commit hash `<Wave-2 cascade commit hash>` placeholder; Wave-2.5 Cleanup-Writer resolves; cascade-bundle pattern per Note 56 + Note 57 + Note 58): A1-A5 GLOSSARY downstream cascade (claim.md + defensibility.md See sections anchored to `arch/claim-defensibility.md`; engaged-authorship.md See section cross-cluster reciprocal mention as Cond #1 operational definition per E7; authority-binding.md See section reciprocal back-link per per-claim author attribution chain sub-aspect; rubber-stamping.md See section reciprocal back-link per axis-3 failure mode failing Cond #1 attestation-phase); B1-B7 peer ARCH §17/§19 reciprocal back-mentions (substrate + audit + adapter + sparring §19 added `arch/claim-defensibility.md` references with composition specifics; specialist-skill + practitioner + workflow-work-unit §17 forward-references upgraded to backward-references — Phase 3.5 fourth primitive-cluster LOCKED); C1 `ARCHITECTURE.md` §7 NEW lock entry positioned after workflow-work-unit + C2 §2 row 3.5 update (third primitive-cluster → fourth primitive-cluster; remaining count phrasing "2 cross-cutting integrator topics remain") + C3 §3 doc structure status table update (7 of 11 → 8 of 11 drafted); D1+D2 MAINTENANCE.md Layer 3 Primitive-cluster topic template ANCHOR codification for PRIMITIVE+DERIVED topic-template-class + per-topic section count expectation row update (claim-defensibility ANCHOR row); E1-E5 BACKLOG cascade (Phase 3.5 row resolution + Phase 5 W2+W3 + Phase 6 W1+W4 + defensibility_test_run reconstruction watch-list entries + 3-tier discriminator cumulative-count update continuing trip threshold 5 ≥ 3); F THIS amendment per Section F below.

**F. DR §9 Files-touched Wave-2 cascade hash resolution** (THIS amendment per cascade discipline auditability; following Note 57 + Note 58 specialist-skill + practitioner + workflow-work-unit DR §9 Wave-2 cascade-scope pattern precedent): Wave-1 commit hash placeholder `<Wave-1 commit hash>` remains in Wave-1 enumeration above (Wave-1 hash known to be `a9fbbfa`; substitution deferred to Wave-2.5 Cleanup-Writer per brief); Wave-2 cascade hash placeholder `<Wave-2 cascade commit hash>` also remains for Wave-2.5 Cleanup-Writer to resolve at landing; Wave-2 cascade scope sub-sections A-E supplemented with applied-status note above. This DR amendment is part of the SAME Wave-2 cascade commit (cascade-bundle pattern per Note 56 + Note 57 + Note 58).

## 10. Revisit triggers

- **W1 signal arrives** (Phase 3.5 schema work + per-archetype claim-kind evidence — per archetype claims surface distinct kind shapes warranting standardization): per-claim-kind variation schema design fires; SD-2 claim manifest schema amendment for per-claim-kind structural conventions; Phase 6 spec territory; cross-link to `arch/workflow-work-unit.md` W3 per-kind structural conventions schema standardization
- **W2 signal arrives** (first legacy-claim import deployment evidence): pre-existing-claim ingestion semantics resolution mechanics design fires; SD-3 cross-primitive composition amendment for per-shape ingestion mechanism; integrates with `glossary/engaged-authorship.md` deferred-now-load-bearing per E4 elevation
- **W3 signal arrives** (second multi-practitioner deployment surface): multi-practitioner co-attestation mechanics design fires; SD-3 per-claim attestation chain mechanics amendment for cross-practitioner co-attestation; integrates with `arch/practitioner.md` §14 W4 cross-practitioner workflow handoff (composes with same awaited-signal) + W1 multi-tenant federation
- **W4 signal arrives** (Phase 6 audit cryptographic chain implementation): cryptographic signing per claim format design fires; integrates with `arch/audit.md` §D integrity verification + cryptographic-signature implementation + `arch/practitioner.md` W3 practitioner-record signing
- **Quality-gate full design signal** (Phase 3.6 quality-gate full design surfaces signal-catalog concerns): quality-gate Pattern A signal-catalog design surfaces per-claim emission observability concerns + per-claim attestation event observability concerns; integrates with SD-6 §8 quality-gate signal-set per shape row
- **Phase 3.3 audit-emission catalog spec creation** (Pydantic spec surfaces field-shape concerns): claim_made + claim_revised + claim_finalized + claim_attested + claim_re_attested + defensibility_test_run event-kind Pydantic shapes surface schema-detail amendments (~10-20% Phase 1 → Phase 2 architectural flow-back per `decision-design-sharpening` §Phase 1 → Phase 2 transition)
- **Second-shape productization signal** (autonomous-business OR personal-OS productization surfaces shape-specific claim-shape variation): SD-6 §8 cross-shape policy variation matrix amendment for per-shape claim-shape variation
- **Federation/multi-practitioner signal** (W3 cross-practitioner co-attestation framework-level treatment): SD-3 cross-primitive composition amendment for federation per-claim attribution chain semantics
- **Pioneer-deployment data shows two-phase composite gaps** (concrete deployment evidence surfaces engaged-authorship two-phase composite gaps): SD-3 engaged-authorship cross-cluster composition amendment for two-phase composite refinement; integrates with engaged-authorship DR amendment cycle
- **Coherence-audit C2 fires post-Phase-3.5 close** (per `disciplines/09-coherence-audit-cadence.md` cadence): primitive-cluster set audited at phase boundary; cross-primitive coherence verified across specialist-skill + practitioner + workflow-work-unit + claim-defensibility + cross-cutting integrators; cumulative REVISION-flavored count (5 across 4 cluster-executions; trip threshold reached) evaluated for 3-tier discriminator codification per BACKLOG watch-list
- **Future primitive-cluster topic creation** (Phase 3.5 cross-cutting integrators last; future PRIMITIVE+DERIVED primitive-cluster topics): validates 12+5 template extension per SD-1; if PRIMITIVE+DERIVED-specific 6th conditional candidate surfaces, MAINTENANCE.md Layer 3 §3 amendment per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern
