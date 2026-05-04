# Decision record: Specialist + skill ARCH topic (Phase 3.5 first primitive-cluster)

## 1. Status

**ACCEPTED** 2026-05-03. Mode 2 upfront-known composite decomposition per `decision-design-sharpening` v0.10.0 §Two decomposition modes — 6 sub-decisions tightly coupled; single composite DR (sub-decisions have no independent meaning outside the composite). LOCK-HARD target-type (architectural decision; cascades hard if revised).

## 2. Owner

Phase 3.5 — first primitive-cluster ARCH topic. Anchors the primitive-cluster topic class (parallel to `arch/substrate.md` anchoring Pattern A 12+7 template). Cited as precedent for downstream Phase 3.5 topics: `arch/practitioner.md` / `arch/workflow-work-unit.md` / `arch/claim-defensibility.md`.

## 3. Related

**Composes with**:
- `arch/substrate.md` Surface §G (specialist registration) + §C (permission flow) + §D (structured output validation) + §F (session/context management) + §8 (dual-emission paths)
- `arch/audit.md` (mechanism class; skill emissions via skill-side MCP gate; specialist-lifecycle event-kind catalog)
- `arch/adapter.md` §14 (cross-shape policy variation precedent)
- `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` (Pattern A / mechanism-class template; primitive-cluster 12+5 derived parallel)
- `docs/decisions/audit-arch-topic.md` (mechanism-class precedent; skill-side emission)
- `docs/decisions/adapter-arch-topic.md` (Pattern A precedent + framework-baseline-vs-shape-extension partition)

**GLOSSARY entries** (locked; cited extensively):
- `specialist` (canonical Pattern B entry; bipartite DEFINITION + INSTANCE-CONTENT)
- `skill` (canonical single-aspect entry; specialist-as-skill-bundle constraint)
- `workflow` (Pattern B nesting partner; future Phase 3.5)
- `work-unit` (Pattern B nesting partner; future Phase 3.5)
- `authority-binding` (skill emission attribution `actor_kind: ai_runtime`)
- `actor` (`actor_kind: ai_runtime` enum value; naming-collision prevention)

**Forward-references** (future Phase 3.5 topics):
- `arch/practitioner.md` (practitioner-record at Owner B; L1 practitioners author specialist DEFINITIONs)
- `arch/workflow-work-unit.md` (workflow + work-unit Pattern B nested within specialist DEFINITION at Framework C)
- `arch/claim-defensibility.md` (claim primitive composes with skill emissions; per-claim attestation chain)

**Disciplines applied**:
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (specialist-skill structural boundary; specialist-namespace prevents collision)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (pioneer-neutrality)
- `MAINTENANCE.md` TOP-LEVEL SCOPE (app skills don't live in framework repo)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 8 (foundation-up ordering); Discipline 10 (greenfield-evaluation of archived sources)

**Archived sources** (INPUT only per Discipline 10):
- `archive/docs/decisions/terminology-and-specialist-primitive.md` (specialist-as-skill-bundle constraint origin; greenfield-evaluated)
- `archive/docs/decisions/skill-expert-agent-and-domain-knowledge.md` (skill-frontmatter conventions reference; greenfield-evaluated)
- `archive/plugin/skills/` (per-specialist DEFINITION files reference patterns)

## 4. Context

Phase 3.5 launches the first primitive-cluster ARCH topic. Prior to this DR, Phase 3.4 Pattern A protocol topics + mechanism-class topics LOCKED (substrate + adapter + sparring + audit per `ARCHITECTURE.md` §7); Phase 3.5 + 3.6 unblocked per coherence-audit C1 STABLE verdict (HANDOFF Note 55).

**Why specialist-skill chosen first** (foundation-up per Discipline 8): specialist DEFINITION is the container for workflow + work-unit Pattern B nesting (per `glossary/specialist.md` composes-with rows: specialist DEFINES work-unit kinds + workflow definitions in its bundle). Locking specialist-skill first means the future Phase 3.5 `arch/workflow-work-unit.md` topic locks against an already-validated container. Reverse ordering would force workflow-work-unit to forward-reference an unlocked specialist primitive.

**Why template-anchoring matters**: substrate's 12+7 template anchored Pattern A protocol topics (parallel established in `MAINTENANCE.md` Layer 3 §3 Pattern A / mechanism-class topic template). Primitive-cluster topics are a NEW topic class (per `ARCHITECTURE.md` §4 topic catalog) — no existing template. This DR establishes the **12+5 primitive-cluster template** anchored by specialist-skill; downstream Phase 3.5 primitive-cluster topics inherit this template (extended OR refined per emergent surfacing).

**What the decision-design phase needed to resolve**:
- Primitive-cluster topic structure (NEW template; what stays / drops / changes from Pattern A 12+7?)
- Specialist DEFINITION manifest schema (frontmatter required fields + types)
- Skill atomic structure + substrate Surface §G integration
- Specialist + workflow + work-unit Pattern B nesting (specialist contains workflow + work-unit-kind DEFINITIONs at Framework C; specialist instance owns instances at Owner B)
- Granularity tests (specialist + skill 3-tests; two-tier specialist classification)
- Marketplace + destruction semantics framing (D-Gate-deferred mechanics vs lockable shape)

## 5. Decision

Six sub-decisions per Mode 2 composite decomposition (sub-decisions have no independent meaning outside the composite; foundation-up dependency ordering applied within the composite).

### SD-1: Primitive-cluster ARCH topic template (12+5; template-anchoring)

**Decision**: Lock 12+5 primitive-cluster topic template parallel to substrate's Pattern A 12+7. 12 common-required sections + 5 cluster-conditional sections.

**12 common-required sections**:
1. Topic scope + frontmatter
2. Per-primitive structural overview
3. Cross-primitive composition within the cluster
4. Composition with framework primitives outside the cluster
5. Cardinality + lifecycle (per primitive)
6. Logic placement mode
7. Pre-implementation operational concerns (Phase 6 forward reference)
8. Watch-list (renumbered to §14 in this implementation per topic-flow)
9. Decision-design provenance (renumbered to §15)
10. Phase routing (renumbered to §16)
11. Cross-references (renumbered to §17)
12. Composition table (renumbered to §18)

**5 cluster-conditional sections** (apply OR document N/A per Pattern A precedent):
- §Granularity tests — when primitives have granularity discriminators (specialist + skill: APPLIES → §9)
- §Bundle composition — when primitive BUNDLES other artifacts (specialist: APPLIES → §10)
- §Cross-shape policy variation — when primitive behavior is shape-policy-mediated (specialist: PARTIALLY → §8)
- §Marketplace + distribution mechanics — when primitive is canonical distributable (specialist: APPLIES partially deferred → §11)
- §Per-primitive lifecycle ordering — when boot/shutdown/activation has load-bearing ordering (specialist activation cycles: APPLIES → §13)

**Why 12+5 not 12+7**: primitive-clusters lack Pattern A pluggability that justifies §3 multi-class boundaries / §10 substrate-specific lifecycle / §12 transport variation / §13 deployment-tier (Pattern A specifics). Conditional count drops to 5 reflecting genuine shape difference, not template-copy. Future primitive-cluster topics may surface 6th conditional candidates per cascade discipline (per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern).

### SD-2: Specialist DEFINITION shape (Framework C bundle structure)

**Decision**: Specialist DEFINITION = directory-bundle (greenfield-derived from archived `terminology-and-specialist-primitive.md` convention per Discipline 10; archived material is INPUT not template).

**Bundle directory structure**:
```
<specialist-name>/
  specialist.md          # manifest with frontmatter (schema below)
  skills/                # directory of skill files
  entities/              # entity-md DEFINITIONs (kinds owned by deployed instance at Owner B)
  memory/                # memory namespace declaration
  adapters/              # adapter implementation declarations bundled with this specialist (if any)
  workflows/             # workflow DEFINITIONs (Phase 3.5 detail)
  work-unit-kinds/       # work-unit KIND DEFINITIONs (Phase 3.5 detail)
```

**Frontmatter manifest schema** (architectural-level enumeration; Phase 6 lands Pydantic shape):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | str | required | Specialist identifier; namespace root |
| `version` | semver | required | Specialist version |
| `axis_claim` | enum | required | `axis-1` \| `axis-2` \| `axis-3` \| `cross-axis` |
| `tier` | enum | required | `domain-anchored` \| `cross-archetype` per SD-5 |
| `activation_prereqs` | list | optional | substrate-class-pinned + adapter-bindings + other-specialists |
| `license` | str | optional | SPDX identifier |
| `shape_compatibility` | list | required | `practitioner-shape` \| `autonomous-business-shape` \| `personal-OS-shape` \| `cross-shape` |
| `capability_declarations` | object | required | Skills count + entity-kinds + workflow-definitions + work-unit-kinds + shape-policy-conformance assertions |

### SD-3: Skill atomic structure + skill-loading-via-substrate Surface §G integration

**Decision**: Skill = trigger frontmatter + body content + optional output schema (Pydantic if structured-output gate composes per substrate Surface §D). Loading semantics declared per substrate Pattern A Surface §G (substrate-native materialization). Per `glossary/skill.md`: `auto-load / explicit-load / lazy-load` — substrate-defined per Implementation.

**Skill emissions**: `actor_kind: ai_runtime` + skill identifier (per authority-binding mechanism Surface; `actor_kind` is `ai_runtime` not `skill` per naming-collision prevention noted in `glossary/skill.md`).

**Specialist-skill structural boundary**: skill canNOT exist standalone outside specialist (PBS architectural commitment per `glossary/skill.md` "specialist-as-skill-bundle constraint"; differs from Anthropic bare-skill plugin convention; Phase 6 reconciles per W3 watch-list).

**Specialist re-binding (mid-session hot-activation)**: per L5a "Capability extension mid-flight" (load-bearing). Specialist activation mid-session must work; in-flight workflow_instances aren't disrupted; new skills become available immediately via substrate Surface §G re-registration. Architectural commitment: 5-step flow per `arch/specialist-skill.md` §5.

### SD-4: Specialist + workflow + work-unit Pattern B nesting

**Decision**: Specialist DEFINITION at Framework C contains: (a) workflow DEFINITIONs (per `glossary/specialist.md` composes-with workflow row); (b) work-unit KIND DEFINITIONs + per-kind structural conventions (per `glossary/specialist.md` composes-with work-unit row). At Owner B, deployed specialist instance owns: workflow_instance entities (when work follows codified pattern per workflow's optional-overlay nature) + work-unit instances of the kinds the specialist defined.

**Specialist-namespace**: per-specialist namespace = specialist-name; prevents cross-specialist KIND/workflow-name collision (e.g., `legal-research:matter` distinct from `planning-document-work:project`). Anchored to existing locked primitive (specialist) rather than introducing kind-vs-specialist ambiguity.

**Foundation-up note**: this DR locks the CONTAINMENT relationship. Future Phase 3.5 `arch/workflow-work-unit.md` topic locks the contained primitives' Pattern B mechanics.

**Cross-specialist composition rules**:
- Skill in specialist-A invokes skill in specialist-B: YES via fully-qualified `specialist-B:skill-name` reference
- Cross-specialist entity reads: YES (audit-trail records both specialist identifiers)
- Cross-specialist entity writes: NO (entity ownership boundary structural per Pattern B)
- Per-shape policy may further restrict

### SD-5: Granularity 3-tests + two-tier classification

**Specialist granularity 3-test** (greenfield-evaluated against `glossary/specialist.md` boundary tests):
1. **Cohesion** — do these skills + entities serve ONE defined competence area?
2. **Distributability** — could this bundle deploy to a workspace standalone (without other specialists) and still function?
3. **Reusability** — could ≥2 distinct workspace archetypes activate this specialist productively?

**Skill granularity 3-test**:
1. **Atomicity** — single trigger condition?
2. **Specialist-coherence** — does this skill belong to ONE specialist's competence area?
3. **Reusability-within-specialist** — invoked from ≥2 contexts within the specialist's workflows?

**Two-tier specialist classification**:
- `domain-anchored` — specialist serves one archetype's domain primarily (e.g., `planning-document-work` for PBS; `legal-research` for legal practice)
- `cross-archetype` — specialist usable across ≥2 archetypes per glossary illustration (e.g., `citation-verification` / `project-management` / `invoicing` / `brand-voice`)

Classification declared in specialist manifest frontmatter `tier` field per SD-2.

### SD-6: Marketplace + destruction semantics + watch-list framing

**Marketplace mechanics**: D-Gate-deferred to BACKLOG Phase 5 ROADMAP entry. Mental modeling can frame the SHAPE — specialist as canonical distributable unit per `glossary/specialist.md` — but per-shape publication / versioning / dependency / supersession mechanics need second-deployment surface friction signal. Per W1 watch-list.

**Destruction semantics on workspace dissolution**: this DR LOCKS **archival as default** (preserves practitioner work + axis-3 authorship preservation + 6-months-later defensibility test favor preservation) with deletion-with-audit as opt-in policy declared at workspace.md level.

**Watch-list (4 items)**:
- W1: Marketplace publication mechanics (awaits second-deployment OR L9 shape-catalog-curator activity)
- W2: Cross-substrate skill-portability (awaits 2nd substrate deployment)
- W3: PBS specialist-as-skill-bundle constraint vs Anthropic bare-skill plugin convention reconciliation (Phase 6)
- W4: Specialist provenance + signing mechanism (anti-spoofing for OSS + future marketplace; Phase 5/6+ tooling)

## 6. Sharpening provenance

### Round 1 (full monty)

EXPANSIONS surfaced (count: 6 — one per sub-decision; Mode 2 upfront-known composite per `decision-design-sharpening` v0.10.0 §Two decomposition modes "Sub-decision inventory" step):
- SD-1 EXPANSION: 12+5 primitive-cluster template (parallel to Pattern A 12+7; conditional count drops reflecting genuine shape difference)
- SD-2 EXPANSION: directory-bundle DEFINITION shape + initial frontmatter manifest schema (8 fields)
- SD-3 EXPANSION: skill atomic structure (trigger frontmatter + body + optional output schema) + skill-loading-via-substrate Surface §G + specialist-as-skill-bundle constraint articulated as PBS architectural commitment
- SD-4 EXPANSION: Pattern B nesting (specialist contains workflow + work-unit-kind DEFINITIONs at Framework C; specialist instance owns instances at Owner B)
- SD-5 EXPANSION: granularity 3-tests (specialist + skill) + two-tier classification (domain-anchored / cross-archetype)
- SD-6 EXPANSION: D-Gate-deferred marketplace + archival-as-default destruction semantics + initial 3-item watch-list (W1-W3)

### Round 2 (user-triggered)

Cross-cutting + schema-detail refinements (per `decision-design-sharpening` §Round 2 layered coverage observation: cross-cutting + schema details emphasized):

**G Composability Gate findings** (per `profiles/G-composability-gate.md`):
- **R-G1**: Manifest schema enrichment — `axis_claim` + `tier` + `license` fields surfaced as required for G consumption modes (consulting / firm reuse / OSS / marketplace)
- **R-G2**: Specialist provenance + signing mechanism added as W4 watch-list (anti-spoofing for OSS + marketplace) — REVISION-flavored EXPANSION (load-bearing for G consumer side)
- **R-G3**: `shape_compatibility` field surfaced as required (cross-shape consumption framing per G profile lines 154-157)
- **R-G4**: Backup-restore-migration round-trip cross-substrate concerns surfaced (per G profile line 159) → composes with SD-3 substrate-pinned vs substrate-agnostic declaration

**Pioneer profile findings** (per `profiles/L5a-planner-pbs-schulz.md` Cluster B/C):
- **R-L5a-1**: Specialist re-binding mid-session (hot-activation) elevated from implicit to load-bearing per L5a "Capability extension mid-flight" (lines 69-73, 119-129) — REVISION-flavored EXPANSION (in-flight workflow_instance preservation requirement)
- **R-L5a-2**: `capability_declarations` manifest field surfaced — pioneer reality (planning-document-work + project-management + invoicing concurrent activation per lines 76-83) requires bundle declares its capability surface explicitly

**Specialist creator profile findings** (per `profiles/L1-specialist-creator.md` Cluster A):
- **R-L1-1**: Manifest schema final form — 8 required/optional fields enumerated per `name` / `version` / `axis_claim` / `tier` / `activation_prereqs` / `license` / `shape_compatibility` / `capability_declarations` (per L1 lines 18-29 intended-stress-test enumeration)
- **R-L1-2**: Cross-specialist composition rules elevated from implicit to explicit (skill-to-skill via specialist boundary; entity-read vs entity-write boundary structural) — REVISION-flavored EXPANSION (structural elevation of implicit-to-explicit)
- **R-L1-3**: Specialist self-containment validated against L1 packaging boundary section (lines 30-32)

**Cross-cutting refinements**:
- **R-CC-1**: Specialist activation lifecycle ordering integrated with `ARCHITECTURE.md` §6 composite boot subsection at substrate-phase 4 (specialist registration step)
- **R-CC-2**: Specialist-error categories enumerated (6 categories: manifest validation / skill load failure / entity-kind conflict / cross-specialist-dependency unmet / adapter-dependency unmet / substrate-class-pin violation); per-shape error escalation policy via §8 cross-shape policy variation
- **R-CC-3**: Specialist-lifecycle event-kind catalog enumerated (5 kinds: activated / deactivated / skill_registered / load_failed / version_bumped)
- **R-CC-4**: Frontmatter schema enumeration formalized in SD-2

**Naming refinement**:
- **R-N-1**: Specialist-namespace mechanic anchored to existing locked specialist primitive (specialist `name` field) rather than introducing separate "kind-namespace" abstraction — REVISION-flavored EXPANSION (anchor to existing primitive vs new abstraction)

**Composition table**:
- **R-COMP-1**: Composition table cross-references substrate Surface §G + §C + §D + §F + §8 + audit Surface §A + adapter + claim primitive + authority-binding mechanism (per §18 of ARCH topic)

**Round 2 EXPANSIONS count**: 14 substantive EXPANSIONS + 1 GLOSSARY back-check verdict (= 15 total; per skill §Empirical density check Round 2 dense-but-bounded; load-bearing surfaces covered).

### Manufactured-criticism rejections

Per `decision-design-sharpening` §Manufactured-comfort counter-test + §Pareto calibration: reject refinements that aren't Pareto-improving OR that surface manufactured-criticism territory.

- **Rejected**: "Should specialist support sub-specialist nesting (specialist-of-specialists)?" — manufactured criticism territory; no profile evidence; flat specialist-set with cross-specialist composition (SD-4 R-L1-2) covers identified use cases; nesting adds complexity without Pareto improvement
- **Rejected**: "Should we introduce a separate kind-namespace primitive for work-unit kinds?" — manufactured criticism; specialist-namespace anchored to existing primitive (R-N-1) covers collision prevention; new primitive adds vocabulary surface without Pareto improvement
- **Rejected**: "Should marketplace mechanics be locked now (revenue tracking + dispute resolution)?" — fails D Gate per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (no genuine external evidence; mental modeling resolves to deferred-to-BACKLOG-with-W1-resolution-mechanism); per `decision-design-sharpening` §Decomposition trigger sub-decision granularity check
- **Rejected**: "Should cross-specialist write boundary have practitioner-shape exception (e.g., for cross-team handoffs)?" — manufactured criticism; entity ownership boundary structural per Pattern B is not shape-policy-mediated; per-shape tightening (autonomous-business restrictions) is additive, not relaxation

### GLOSSARY back-check verdict

Per `MAINTENANCE.md` Bidirectional cascade + `decision-design-sharpening` v0.5.0 GLOSSARY back-check at Round 2 termination.

**Verdict**: Lens 6 reciprocal closure PENDING for Wave-2 Cascade-Writer commit. Specialist-namespace mechanic (R-N-1) elevates to glossary-grade structural fact (load-bearing vocabulary distinction across `specialist` + `work-unit` + `workflow` + `skill` GLOSSARY entries). Cascade-Writer Wave-2 commit (separate tightly-coupled per `MAINTENANCE.md` cascade discipline) will:
- Update `glossary/specialist.md` to reference specialist-namespace anchor
- Update `glossary/work-unit.md` to reference specialist-namespace for cross-specialist KIND disambiguation (replace prior "kind-namespace" reference)
- Update `glossary/skill.md` to reference specialist-namespace for cross-specialist skill identification

This DR + ARCH topic commit covers `arch/specialist-skill.md` + `docs/decisions/specialist-skill-arch-topic.md`. Tightly-coupled GLOSSARY cascade follows in Wave-2 commit.

### Profile-anchored validation

Per `decision-design-sharpening` v0.5.0+ profile-anchored validation + `profiles/INDEX.md` cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators).

**3 cluster representatives Read** (≥3 cluster coverage requirement):

**Cluster A Producers** — `profiles/L1-specialist-creator.md` (specialist creator):
- L1 lines 18-29 intended-stress-test enumeration cited: specialist self-containment / DEFINITION boundary / skill granularity within specialist / workflow definition packaging / entity declarations / composability / versioning / license / cross-substrate / cross-shape compatibility — full coverage in SD-2 manifest schema + SD-4 cross-specialist rules + SD-5 granularity tests
- L1 lines 30-32 packaging boundary: validated against G profile in SD-6 W4 watch-list (signing); SD-2 license field
- Verdict: covered

**Cluster B Deployers** + **Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` (pioneer; multi-cluster member):
- L5a lines 69-73 Capability extension mid-flight: mid-session hot-activation locked in SD-3 + ARCH §5 + ARCH §13 mid-session activation ordering
- L5a lines 76-83 active specialists set (planning-document-work + project-management + invoicing): validates two-tier classification (1 domain-anchored + 2 cross-archetype) per SD-5
- L5a lines 119-129 stress-tests: capability extension mid-flight + per-claim attestation + sparring as load-bearing — covered via SD-3 re-binding + Pattern B composition with claim primitive (forward-reference)
- Verdict: covered

**Cluster D Validators** — `profiles/G-composability-gate.md` (cross-cutting validation gate; Cluster D member):
- G lines 22-92 5-mode consumption framing (consulting / firm reuse / OSS / marketplace / backup-migration): covered in SD-6 distribution shape + per-shape distribution policy
- G lines 154-157 cross-shape consumption rules: covered in SD-2 `shape_compatibility` field + §8 cross-shape policy variation
- G lines 162-184 architectural concerns surfaced: covered in SD-2 manifest schema + SD-6 W1/W4 watch-list + SD-3 substrate-pinned declaration
- Verdict: covered

**Cluster D Validators (gate component)** — D Defer Gate per `profiles/INDEX.md`:
- Marketplace mechanics genuine-defer test: external-information test passes (specific signal = second-deployment OR shape-catalog-curator activity); effort-asymmetry test passes (per-shape mechanics design before evidence accumulates risks wrong-design); D Gate satisfied → W1 watch-list with resolution mechanism
- Verdict: D Gate satisfied per genuine awaited evidence

### Mode 2 composite decomposition rationale

Per `decision-design-sharpening` v0.10.0 §Two decomposition modes Mode 2:
- **Trigger satisfied**: 6 sub-decisions visible at framing time (not emergent from drift); foundation-up dependencies identifiable (SD-1 template enables SD-2-6 to inherit shape; SD-2 + SD-3 enable SD-4 nesting; SD-5 + SD-6 layer on top)
- **Sub-decision inventory at start**: 6 sub-decisions listed before Round 1 (SD-1 → SD-6); composite decomposition mode declared upfront
- **Foundation-up dependency ordering**: SD-1 (template) locks first; SD-2 (specialist DEFINITION) + SD-3 (skill atomic) lock together (peer foundation); SD-4 (Pattern B nesting) builds on SD-2 + SD-3; SD-5 (granularity tests) layers on validated DEFINITIONs; SD-6 (marketplace + destruction) layers on validated bundle shape
- **Per-sub-decision sharpening**: each got Round 1 + Round 2 sweep within the composite (no per-sub-decision split into separate rounds)
- **Synthesis pass at end**: this DR + ARCH §18 composition table is the cross-sub-decision coherence pass
- **Single composite DR**: chosen per Mode 2 §Single composite DR — sub-decisions have no independent meaning outside the composite; specialist-skill cluster is the unit, not 6 independent decisions

### REVISION/EXPANSION classification self-check

Per `decision-design-sharpening` v0.6.0 self-check at Round 2 termination + BACKLOG watch-list "3-tier discriminator codification".

**REVISION-flavored EXPANSIONS surfaced** (load-bearing structural elevations):
- R-L5a-1 (specialist re-binding mid-session elevated from implicit to load-bearing per L5a evidence) — REVISION-flavored
- R-L1-2 (cross-specialist composition rules structural elevation of implicit-to-explicit) — REVISION-flavored

**Cumulative count for awaited 3-tier signal**: 2 REVISION-flavored EXPANSIONS in this composite. Below ≥3 threshold for 3-tier discriminator codification trigger per BACKLOG watch-list. **2-tier (REVISION/EXPANSION) holds**; signal hasn't materialized.

**Pure REVISIONS** (architectural pivots changing existing decisions): 0. Both REVISION-flavored items are EXPANSIONS-with-load-bearing-implications, not pure architectural reversals.

### Termination signal (STABLE-AT-ROUND-2)

Per `decision-design-sharpening` §Round termination signals + §Honest termination test Q1-Q5:

- **Q1 (count)**: Round 1 = 6 EXPANSIONS; Round 2 = 14 EXPANSIONS + 1 GLOSSARY back-check = 15
- **Q2 (decay)**: not applicable for Round 2 (Round 1 was foundation; Round 2 was first sharpening; expected density bump per §Layered coverage observation Round 2 cross-cutting + schema-detail layer)
- **Q3 (density behavior)**: Round 2 surfaced sub-decision-level refinements + cross-cutting (per skill §Layered coverage observation Round 2 emphasis); no Round 3 architectural-pattern-surfacing pending
- **Q4 (specific unaddressed pass)**: NONE — all 4 profile clusters covered (A + B + C + D); G Gate + D Gate fired; cross-cutting + schema details exhausted at decision-design-phase
- **Q5 (specific termination signal)**: NARROW ARCHITECTURAL SURFACE per `decision-design-sharpening` §Empirical sweet-spot pattern (single primitive cluster decomposed Mode-2; 2-round sweet spot fits); operational concerns (skill trigger evaluation mechanics; per-substrate dispatch implementation; schema-validation auto-retry) belong to Phase 6 pre-implementation per §Phase 1 → Phase 2 transition
- **Lock + persist signal**: STABLE per Q5 specific termination signal + Q4 no-unaddressed-pass + manufactured-comfort counter-test passed (operational concerns explicitly deferred per §Layered coverage observation Round 4+ DEFER to Phase 2)

## 7. Composition with existing architecture

This decision composes with prior locked architecture:

- **Pattern A protocols** (substrate / adapter; sparring + audit mechanism classes per Phase 3.4 close): specialist + skill compose with substrate Surface §G + §C + §D + §F + §8; with audit Surface §A skill-side emission; with adapter per-class Surfaces (§4 composition table). Specialist + skill primitives are NOT Pattern A (no multiple interchangeable implementations of one Surface) — specialist is Pattern B (DEFINITION + INSTANCE-CONTENT); skill is single-aspect cross-cutting.

- **Pattern B primitives** (workflow + work-unit per Phase 3.1 close): specialist DEFINITION CONTAINS workflow + work-unit-kind DEFINITIONs at Framework C; specialist instance OWNS workflow_instances + work-unit instances at Owner B per Pattern B nesting (SD-4). Future Phase 3.5 `arch/workflow-work-unit.md` topic locks the contained primitives' mechanics against this validated container.

- **authority-binding mechanism** (per `glossary/authority-binding.md` from Phase 3.4 C1 cascade): skill emissions record `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface; specialist activation events record activating actor.

- **`ARCHITECTURE.md` §6 composite boot subsection**: specialist registration ordering integrates at substrate-phase 4 per ARCH §13 boot-time activation ordering.

- **`MAINTENANCE.md` Pattern A / mechanism-class topic template** (`MAINTENANCE.md` Layer 3 §3): primitive-cluster 12+5 template establishes parallel topic class; future primitive-cluster topics (Phase 3.5 practitioner / workflow-work-unit / claim-defensibility) inherit this DR's template. MAINTENANCE.md Layer 3 §3 codifies the 12+5 template as canonical primitive-cluster pattern.

- **TOP-LEVEL DESIGN PRINCIPLES §1 (structural over conventional)**: specialist-skill structural boundary (skill-as-bundled-within-specialist) + specialist-namespace anchored to existing primitive — both exemplify structural-over-conventional discipline.

- **TOP-LEVEL DESIGN PRINCIPLES §2 (pioneer-neutrality)**: specialist + skill primitives stay shape-neutral / archetype-neutral / pioneer-neutral; pioneer reality grounds the cluster without leaking pioneer specifics.

## 8. Constraints flowing to downstream commitments

- **Phase 3.5 future primitive-cluster topics** (`arch/practitioner.md` / `arch/workflow-work-unit.md` / `arch/claim-defensibility.md`): inherit primitive-cluster 12+5 template per SD-1; apply 5 cluster-conditional sections per their primitive-set's discriminators
- **Phase 3.5 `arch/workflow-work-unit.md`**: specifically inherits SD-4 Pattern B nesting (workflow + work-unit-kind DEFINITIONs live in specialist bundle; workflow_instances + work-unit instances at Owner B owned by deployed specialist instance); locks contained primitives' mechanics against validated specialist container
- **Phase 3.6 `arch/quality-gate.md`**: consumes skill-firing observability + specialist-lifecycle event-kind catalog per §7 ARCH topic; quality-gate Pattern A composes with this cluster
- **Phase 6 specs** (`docs/specs/specialist.md` + `docs/specs/skill.md`): inherit manifest frontmatter schema per SD-2; skill output schema integration with substrate Surface §D per SD-3; specialist-error class hierarchy per §7 ARCH topic
- **Phase 6 deployment** (per `MAINTENANCE.md` TOP-LEVEL SCOPE: PBS-Schulz workspace deployment): app-skill rebuild inherits specialist-as-skill-bundle constraint per SD-3 + W3 reconciliation
- **GLOSSARY cascade**: `glossary/specialist.md` + `glossary/work-unit.md` + `glossary/skill.md` + MAINTENANCE.md primitive-cluster 12+5 template codification
- **BACKLOG.md**: W1 (marketplace publication mechanics) → Phase 5 ROADMAP entry per D Gate; W2 (cross-substrate skill-portability) → Phase 6 watch trigger; W3 (PBS specialist-as-skill-bundle vs Anthropic bare-skill reconciliation) → Phase 6 app-skill rebuild trigger; W4 (specialist provenance + signing) → Phase 5/6+ tooling territory

## 9. Files touched

- `arch/specialist-skill.md` — primitive-cluster 12+5 ARCH topic (~470 lines)
- `docs/decisions/specialist-skill-arch-topic.md` — this composite DR
- `glossary/specialist.md` — specialist-namespace anchor for work-unit kinds + workflow definitions; composes-with rows amended for reciprocal symmetry
- `glossary/work-unit.md` — composes-with specialist row: specialist-namespace mention; fully-qualified kind reference `specialist-name:kind-name`
- `glossary/workflow.md` — composes-with specialist row: specialist-namespace mention; fully-qualified workflow reference `specialist-name:workflow-name`
- `MAINTENANCE.md` Layer 3 — primitive-cluster topic template subsection (12 common-required + 5 cluster-conditional + per-pattern conditional applicability + §12-as-N/A-parity convention)
- `ARCHITECTURE.md` §7 — lock entry "Specialist-skill ARCH topic — Phase 3.5 first primitive-cluster"; §2 Phase 3 sub-phase status table row 3.5 updated (Pending → ACTIVE)
- `arch/substrate.md` §19 — added `arch/specialist-skill.md` reference (substrate Surface §G specialist registration integration point)
- `arch/audit.md` §19 — added `arch/specialist-skill.md` reference (specialist-lifecycle event-kind catalog emits via audit Surface)
- `arch/adapter.md` §19 — added `arch/specialist-skill.md` reference (specialists may bundle adapter implementations per `arch/specialist-skill.md` §10 bundle composition)
- `arch/sparring.md` §19 — added `arch/specialist-skill.md` reference (sparring sub-mechanisms invoked from skills within specialists composing with substrate Surface §D)

Initial commit `f6bab6e`; cascade + cleanup commits per git log.

## 10. Revisit triggers

- **W1 signal arrives** (second-deployment OR L9 shape-catalog-curator activity): marketplace publication / versioning / supersession mechanics design fires; per-shape distribution policy specifics lock; SD-6 amendment per cascade discipline
- **W2 signal arrives** (second substrate deployment): cross-substrate skill-portability validation; per-substrate trigger-keyword convention reconciliation; SD-3 amendment if friction surfaces
- **W3 signal arrives** (Phase 6 app-skill rebuild begins): PBS specialist-as-skill-bundle constraint vs Anthropic bare-skill plugin convention reconciliation; SD-3 amendment per chosen reconciliation path
- **W4 signal arrives** (OSS distribution friction OR marketplace mechanics design begins per W1): specialist signing format design; SD-2 manifest schema amendment to add signing field
- **Future primitive-cluster topic creation** (`arch/practitioner.md` / `arch/workflow-work-unit.md` / `arch/claim-defensibility.md`): validates 12+5 template extension or refinement; if cluster-specific discriminator surfaces 6th conditional candidate, MAINTENANCE.md Layer 3 §3 amendment per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern
- **Phase 6 spec creation**: SpecialistDescriptor + SkillDescriptor Pydantic schemas may surface architectural amendments (~10-20% Phase 1 → Phase 2 architectural flow-back per `decision-design-sharpening` §Phase 1 → Phase 2 transition)
- **Coherence-audit C2** (post-Phase-3.5 close): primitive-cluster set audited at phase boundary; cross-primitive coherence verified
