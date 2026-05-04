---
title: Workflow + work-unit
topic-cluster: primitive-cluster (#3 of 4)
status: locked
---

# Workflow + work-unit

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the workflow + work-unit primitive cluster (the codified-pattern primitive + the always-present accountability-bearing-work container; both bipartite Pattern B per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern B row). Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the WorkflowDescriptor + WorkUnitKindDescriptor Pydantic schemas (Mode 3). Foundation-up dependency: workflow + work-unit DEFINITIONs nest within specialist's bundle (per `arch/specialist-skill.md` §10 + `glossary/specialist.md` composes-with workflow + work-unit rows); locking workflow-work-unit third after specialist-skill + practitioner means the future Phase 3.5 `arch/claim-defensibility.md` topic locks per-claim attestation chain against an already-validated workflow_instance + work-unit instance attribution surface.

## 1. Topic scope + frontmatter

**Cluster identity**: workflow + work-unit — the codified-pattern + accountability-bearing-work-container primitive cluster. Two-Pattern-B cluster. Workflow is the codified pattern of work (optional structural overlay per `glossary/workflow.md`); work-unit is the always-present container (every accountability-bearing piece of work IS a work-unit per `glossary/work-unit.md`). Both PRIMITIVES per locked GLOSSARY entries.

**Primitives covered**:
- `workflow` — bipartite Pattern B with optional applicability (DEFINITION at Framework C via specialist's bundle; INSTANCE at Owner B as workflow_instance entity)
- `work-unit` — bipartite Pattern B with always-present container (KIND DEFINITION at Framework C via specialist's bundle; INSTANCE at Owner B as work-unit instance entity)

**Cross-axis claim**: workflow is the axis-1 PRIMARY anchor — workflow is what intertwined AI intertwines WITH per `glossary/workflow.md` ("Workflow as precondition" implication per VISION). Work-unit is cross-axis — the artifact-container all axes operate against (axis-1 intertwined work happens IN work-units; axis-2 sparring fires DURING work-unit progression; axis-3 authorship attaches TO work-units per `glossary/work-unit.md`). The cluster is cross-axis at primitive level with axis-1 lean for workflow.

**Cardinality at cluster level** (per-primitive detail in §5):
- N workflow definitions per specialist; N workflow_instances per workspace per active specialist (instances created per work-unit when codified pattern applies; absent for ad-hoc work-units per `glossary/workflow.md` optional applicability)
- N work-unit kinds per specialist; N work-unit instances per workspace per active kind (always-present container; one per accountability-bearing work piece per `glossary/work-unit.md`)
- 1 work-unit instance per workflow_instance (workflow_instance has 1 work-unit attribution); N workflow_instances per work-unit instance (potentially across specialists per `glossary/work-unit.md`)

**Cluster boundary**: this topic locks the bipartite-pair structural articulation (4 sub-aspects: workflow DEFINITION + workflow_instance + work-unit KIND DEFINITION + work-unit instance), the always-present asymmetry, the cardinality asymmetry, the snapshot pattern as cross-primitive structural commitment, the workflow_instance + work-unit instance state machines, the cross-pattern destruction coherence + orphan-instance handling + boot integration, the granularity 3-tests per primitive, the cross-shape policy variation, and W1-W4 watch-list. It does NOT lock claim mechanics (Phase 3.5 `arch/claim-defensibility.md` topic) or specialist + skill mechanics (Phase 3.5 `arch/specialist-skill.md` topic; LOCKED) or practitioner mechanics (Phase 3.5 `arch/practitioner.md` topic; LOCKED) — those compose with this cluster's primitives but live in their own topics.

**Composition with framework**:
- Workflow DEFINITION lives at `Framework C scope` via specialist's bundle (per `glossary/workflow.md` "DEFINITION aspect inherits Framework C placement via specialist's bundle"); workflow_instance lives at `Owner B scope`
- Work-unit KIND DEFINITION lives at `Framework C scope` via specialist's bundle (per `glossary/work-unit.md`); work-unit instance lives at `Owner B scope`
- Pattern B classification per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern B row (both workflow + work-unit are Pattern B; the cluster pairs two Pattern B primitives)
- Authority-binding mechanism Surface (per `glossary/authority-binding.md`) consumes practitioner-RECORD + skill identifier for workflow_instance phase transitions + work-unit instance lifecycle transitions per per-event actor declaration sub-aspect
- Audit mechanism class records workflow_instance + work-unit instance lifecycle events per §SD-4 event-kind catalog

**Phase routing**: WorkflowDescriptor + WorkUnitKindDescriptor Pydantic schemas → Phase 6 spec (Mode 3). Per-deployment workflow_instance + work-unit instance entity-md authoring → workspace deployment (NOT this repo per `MAINTENANCE.md` TOP-LEVEL SCOPE instance-content lives at deployment-instance). This topic locks the architectural shape; Phase 6 locks typed contracts.

## 2. Per-primitive structural overview

### 2.1 Workflow DEFINITION (Framework C; in specialist's bundle)

Per locked GLOSSARY `workflow` entry: a workflow definition is the reusable pattern (specialist-bundled): "how does B-Plan-Begründung drafting actually proceed?" or "how does a legal brief get from intake to filing?" — sequence of activities + artifacts + decisions + handoffs + per-phase authority requirements. Workflow definitions live in specialist's distributable bundle at Framework C placement (workflow inherits Framework C placement via specialist composition, NOT as standalone framework primitive). Optional structural overlay per `glossary/workflow.md`: workflow primitive engages OPTIONALLY — only when work follows a codified pattern.

**Workflow DEFINITION manifest schema** (architectural-level enumeration; Phase 6 lands Pydantic shape):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | str | required | Workflow name local to specialist; specialist-namespace per `arch/specialist-skill.md` §10 R-N-1; fully-qualified `specialist-name:workflow-name` |
| `version` | semver | required | Inherits specialist version per `glossary/workflow.md` lifecycle (workflow definition immutable per specialist version; specialist version bump may include workflow definition changes) |
| `phases` | list (ordered) | required | Phase identifiers in sequence (e.g., `intake → research → draft → review → send → response_handling` per `profiles/L5a-planner-pbs-schulz.md` lines 22-29 B-Plan workflow) |
| `phase_authority_requirements` | object | optional | Per-phase authority binding per `glossary/workflow.md` composes-with authority-binding row (workflow definition declares per-phase authority requirements; per-shape policy declares trust model parameterizing authority-binding satisfaction) |
| `triggered_skills` | object | optional | Per-phase skill triggers; references skills in containing specialist by local name; cross-specialist via fully-qualified per `arch/specialist-skill.md` §3 + §10 (skill in specialist-A invokes skill in specialist-B via `specialist-B:skill-name`) |
| `optional_overlay_marker` | bool | default true | Always-true at framework level per `glossary/workflow.md` optional applicability (workflow primitive engages OPTIONALLY); documented for clarity (not configurable) |

### 2.2 workflow_instance (Owner B; OPTIONAL overlay)

Per locked GLOSSARY `workflow` entry: a workflow_instance is a specific execution against a work-unit (Owner B). The primitive engages OPTIONALLY — only when work follows a codified pattern; ad-hoc work without codified pattern engages session + work-unit + skill + claim + event WITHOUT workflow_instance.

**workflow_instance schema** (architectural-level; Phase 6 lands Pydantic):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | str | required | workflow_instance identifier; per-deployment uniqueness convention (deployment-side prose-rule pattern per archived `governance-and-identity-sourcing.md` decision 3 greenfield-evaluated per §15) |
| `definition_snapshot` | object | required | Snapshot of workflow definition at workflow-start (preserves defensibility per `glossary/workflow.md` lifecycle "preserves defensibility — execution reproducible per original definition"; cross-primitive snapshot pattern per §3 R-CC-10) |
| `definition_ref` | str | required | Fully-qualified `specialist-name:workflow-name@version` per `arch/specialist-skill.md` §10 specialist-namespace |
| `current_phase` | enum | required | References definition `phases` list |
| `lifecycle_state` | enum | required | `running` \| `suspended` \| `completed` \| `abandoned` \| `failed` per `glossary/workflow.md` lifecycle (R-CC-1 naming alignment with work-unit instance `lifecycle_state` + `arch/practitioner.md` §2.2 `lifecycle_state`) |
| `attached_work_unit_id` | str | required | work-unit instance attribution; cardinality asymmetry (1 work-unit per workflow_instance per §3) |
| `bound_practitioner_id` | str | required | practitioner-RECORD attribution per `arch/practitioner.md` §4 R-CC-10 (each session binds to ONE practitioner-record; workflow_instance attribution composes through session-bound practitioner) |
| `phase_history` | list | optional | Phase transitions with timestamps + actor + audit event references |

### 2.3 Work-unit KIND DEFINITION (Framework C; in specialist's bundle)

Per locked GLOSSARY `work-unit` entry: a work-unit kind is the specialist-defined discriminator + per-kind structural conventions (e.g., `project` for planning bureau, `matter` for legal practice, `case` for medical practice, `engagement` for consulting, `manuscript` for research lab, `audit` for accounting). KIND DEFINITION lives in specialist's distributable bundle at Framework C placement (work-unit inherits Framework C placement via specialist composition, NOT as standalone framework primitive). Always-present container per `glossary/work-unit.md`: every accountability-bearing piece of work IS a work-unit (regardless of workflow primitive engagement).

**Work-unit KIND DEFINITION manifest schema** (architectural-level; Phase 6 lands Pydantic):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | str | required | Kind discriminator (`project` / `matter` / `case` / `engagement` / `manuscript` / `audit` / `task` / `order` per `glossary/work-unit.md` cross-archetype illustration); specialist-namespace per `arch/specialist-skill.md` §10 R-N-1 |
| `version` | semver | required | Inherits specialist version per `glossary/work-unit.md` lifecycle (work-unit kind immutable per specialist version) |
| `lifecycle_states` | list | required | Kind-specific state machine; default: `initiated` → `in-progress` → `completed` \| `sent` \| `archived` per `glossary/work-unit.md` lifecycle |
| `artifact_attachment_shape` | object | optional | Per-kind structural conventions (drafts / references / sent versions); INPUT from archived `entity-md-scope-model-restructure.md` greenfield-evaluated per §15 (archive uses superseded vocabulary "office-level entities" → current "workspace-scope managed entities") |
| `audit_attribution_semantics` | object | optional | Per-kind event scoping rules (which events scope to this kind's instances; per `glossary/work-unit.md` "events scoped to work-unit per archived audit-trail-v2 schema" greenfield-evaluated per §15) |

### 2.4 work-unit instance (Owner B; ALWAYS-PRESENT container)

Per locked GLOSSARY `work-unit` entry: a work-unit instance is a specific deployment-bound artifact-container at Owner B. Always-present anchor per `glossary/work-unit.md`: every accountability-bearing work IS a work-unit (no optional-overlay discount; reciprocal to workflow's optional applicability). Carries lifecycle state (initiated → in-progress → completed / sent / archived), associated artifacts (drafts, references, sent versions), decisions made, sources cited, sparring outcomes, and audit-trail attribution (events emitted scoped to this instance).

**work-unit instance schema** (architectural-level; Phase 6 lands Pydantic):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | str | required | Per-deployment uniqueness convention (deployment-side prose-rule pattern per archived `governance-and-identity-sourcing.md` decision 3 greenfield-evaluated per §15) |
| `kind_snapshot` | object | required | CREATION snapshot per `glossary/work-unit.md` lifecycle "preserves audit-trail integrity if specialist version bumps mid-instance-lifetime; mirrors workflow_instance definition-snapshot pattern"; cross-primitive snapshot pattern per §3 R-CC-10 |
| `kind_ref` | str | required | Fully-qualified `specialist-name:kind-name@version` per `arch/specialist-skill.md` §10 specialist-namespace |
| `lifecycle_state` | enum | required | References kind `lifecycle_states` enum; FIXED kind at creation per `glossary/work-unit.md` ("kind is FIXED at creation; pivot creates new work-unit") |
| `attached_workflow_instances` | list | optional | N workflow_instances per cardinality asymmetry per §3 (potentially across specialists per `glossary/work-unit.md`) |
| `owning_specialist_id` | str | required | Per `glossary/work-unit.md` composes-with specialist row (work-unit instance is owned by deployed specialist instance) |
| `attribution` | object | required | practitioner-RECORD authorship per `glossary/work-unit.md` composes-with practitioner row (multi-practitioner-shape variants = shape-policy per `arch/practitioner.md` §3 + §8) |

## 3. Cross-primitive composition within the cluster

The workflow + work-unit cluster pairs two Pattern B primitives with deeply-coupled compositional semantics. Three load-bearing structural commitments + the snapshot pattern + cross-specialist composition mechanics.

### Always-present asymmetry (load-bearing)

Per `glossary/work-unit.md` always-present + `glossary/workflow.md` optional applicability: work-unit is ALWAYS-PRESENT container (every accountability-bearing piece of work IS a work-unit) vs workflow_instance is OPTIONAL overlay (engages only when codified pattern applies). This asymmetry is NOT cosmetic — it is load-bearing per the locked GLOSSARY entries.

The asymmetry enables ad-hoc work to be first-class supported via the always-present work-unit primitive without forcing workflow primitive engagement. The framework supports BOTH codified-pattern work (workflow_instance attached to work-unit) AND ad-hoc work (work-unit alone, carried by session + skill firings + claim emissions + events) as structurally legitimate.

### Cardinality asymmetry

Reciprocal but asymmetric:
- **1 work-unit per workflow_instance**: workflow_instance has exactly 1 work-unit attribution (the work-unit it progresses against); the `workflow_instance.attached_work_unit_id` field is a single reference per §2.2
- **N workflow_instances per work-unit**: a work-unit may have 0+ workflow_instances attached (potentially across specialists per `glossary/work-unit.md` "legal `matter` progressed by litigation-specialist's filing workflow + accounting-specialist's billing workflow"); the `work-unit-instance.attached_workflow_instances` field is a list per §2.4

The cardinality asymmetry composes with the always-present asymmetry: when N=0 attached workflow_instances on a work-unit, that's ad-hoc work; when N≥1, those are codified-pattern executions against the work-unit.

### Ad-hoc work first-class (via session + skill + claim + event; NOT via workflow primitive engagement)

When a work-unit has no workflow_instance attached, work proceeds via session(s) + skill firings + claim emissions + audit events alone — this is first-class supported, not a degenerate case. Per `profiles/L5a-planner-pbs-schulz.md` lines 60-73 hybrid moments: practitioner is mid-drafting (codified workflow_instance active) → notices unusual parcel feature → ad-hoc research detour (no workflow_instance for that exploration) → returns to drafting (workflow_instance resumes); same session, multiple workflow_instance ↔ ad-hoc transitions.

This composition is what distinguishes this cluster's two Pattern B primitives from a single bundled Pattern B primitive: workflow's optional overlay nature requires structural support for ad-hoc work; the always-present work-unit container provides that support without forcing workflow engagement. Per `glossary/workflow.md` evolution path: practitioner doing ad-hoc work repeatedly may notice patterns → pattern crystallizes into workflow definition → future similar work follows codified pattern.

### Snapshot pattern as cross-primitive structural commitment (R-CC-10)

Both workflow_instance (`definition_snapshot` per §2.2) and work-unit instance (`kind_snapshot` per §2.4) use snapshot-at-creation for defensibility-preservation across specialist version bumps. This is a CROSS-PRIMITIVE PATTERN — explicit cross-primitive commitment grounded in `glossary/workflow.md` definition snapshot + `glossary/work-unit.md` kind-creation snapshot mirror.

### Cross-specialist composition (within cluster but cross-specialist mechanics per `arch/specialist-skill.md` §10)

workflow_instance from specialist-A may attach to work-unit instance owned by specialist-B (cross-specialist work-unit attachment). This composes with `arch/specialist-skill.md` §10 cross-specialist composition rules:

- **Cross-specialist work-unit ATTACHMENT**: PERMITTED — workflow_instance from specialist-A attaches to work-unit from specialist-B (reflects `glossary/work-unit.md` "legal `matter` progressed by litigation-specialist's filing workflow + accounting-specialist's billing workflow" cross-archetype example)
- **Cross-specialist work-unit READS**: PERMITTED — workflow_instance from specialist-A reads work-unit content owned by specialist-B (per `arch/specialist-skill.md` §10 cross-specialist entity reads permitted)
- **Cross-specialist work-unit WRITES (ownership mutation)**: PROHIBITED — per `arch/specialist-skill.md` §10 cross-specialist composition rules, entity ownership boundary is structural (work-unit instance owned-by-deployed-specialist-instance per `glossary/work-unit.md` composes-with specialist row); workflow_instance can READ cross-specialist work-unit but cannot mutate ownership

Per-shape policy may further restrict cross-specialist composition (e.g., autonomous-business-shape may restrict to declared cross-specialist invocation lists for budget-control per `arch/specialist-skill.md` §10). Framework baseline = above rules; per-shape tightening = additive.

## 4. Composition with framework primitives outside the cluster

| Primitive | Composition |
|---|---|
| `framework` | Workflow + work-unit are framework primitives within `framework`'s primitive set; both bipartite Pattern B per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE |
| `mechanism` | Workflow_instance + work-unit instance lifecycle events flow through audit Surface; phase transitions + lifecycle transitions consume authority-binding mechanism for actor attribution |
| `Framework C scope` | Workflow DEFINITIONs + work-unit KIND DEFINITIONs live there via specialist's bundle (per `glossary/workflow.md` + `glossary/work-unit.md` DEFINITION aspect inherits Framework C placement via specialist composition) |
| `Owner B scope` | Workflow_instances + work-unit instances live there as workspace-scope managed entities (per `glossary/owner-b-scope.md` members list — work-unit instances explicitly named; workflow_instances inherit Owner B placement) |
| `workspace` | Workspace contains N work-unit instances + N workflow_instances per active specialist (per `glossary/work-unit.md` + `glossary/workflow.md` cardinality); workspace dissolution destruction per §13 archival-as-default cross-pattern coherence |
| `shape` | Shape policy declares per-shape multi-practitioner work-unit authorship + workflow_instance flexibility + work-unit lifecycle policy per §8 cross-shape policy variation matrix |
| `specialist` | Specialist DEFINITION CONTAINS workflow definitions + work-unit kind DEFINITIONs at Framework C per `arch/specialist-skill.md` §10 (bundle composition); specialist instance OWNS workflow_instances + work-unit instances at Owner B per Pattern B nesting |
| `skill` | Workflow definitions reference skills by name (composition direction: workflow → skill per `glossary/workflow.md` composes-with skill row); skills are consumed BY workflow definitions (skills fire within workflow phases when triggers match per `glossary/skill.md`) |
| `practitioner` | workflow_instance binds to ONE practitioner-record at session-open per `arch/practitioner.md` §4 R-CC-10 (`workflow_instance.bound_practitioner_id` references session-bound practitioner per §2.2); work-unit instance attribution composes through practitioner-RECORD per `glossary/work-unit.md` composes-with practitioner row (multi-practitioner-shape variants = shape-policy per `arch/practitioner.md` §3 + §8) |
| `session` | Sessions execute parts of workflow_instance executions (one workflow_instance can span many sessions per `glossary/workflow.md` composes-with session row); persistent-state mechanism carries workflow_instance state across session boundaries per substrate Surface §F |
| `substrate` (Pattern A) | Substrate Surface §F session/context management persists workflow_instance + work-unit instance state across sessions; substrate Surface §C permission flow integrates with workflow_instance phase transitions + work-unit instance lifecycle transitions for authority-binding moments (per substrate §10 boot/shutdown integration per §13) |
| `audit` (mechanism class) | All workflow_instance + work-unit instance lifecycle events flow through audit Surface §A emission per `arch/audit.md` §A; per-shape audit emission granularity composes per `arch/audit.md` §14 (claim-level / action-level / light per shape) |
| `authority-binding` (mechanism) | workflow_instance phase transitions may require specific authority per workflow definition `phase_authority_requirements` (per `glossary/workflow.md` composes-with authority-binding row); work-unit instance lifecycle transitions emit events bound to authority-decision actor per `glossary/work-unit.md` composes-with authority-binding row (practitioner-shape send/archive = practitioner-only per defensibility-critical) |
| `actor` | Actors emit events against workflow_instance + work-unit instance (practitioner authorizing send; AI runtime drafting; external client responding per `glossary/work-unit.md` composes-with actor row) |
| `event` | workflow_instance + work-unit instance lifecycle emit events per §SD-4 event-kind catalog; events flow through audit Surface |
| `adapter` (Pattern A) | Adapters invoked by skills firing within workflow_instance phases (e.g., draft-cover-mail invokes email-adapter; verify-citations invokes MCP-corpus-adapter per `arch/adapter.md` §2 per-class Surfaces) |
| `specialist-skill` (Phase 3.5 first primitive-cluster LOCKED) | Workflow + work-unit DEFINITIONs nest within specialist's bundle per `arch/specialist-skill.md` §10 (workflow definitions live in specialist's distributable bundle at Framework C; work-unit kind DEFINITIONs same); cross-specialist composition rules apply per `arch/specialist-skill.md` §10 + §3 cross-specialist composition |
| `practitioner` (Phase 3.5 second primitive-cluster LOCKED) | workflow_instance bound_practitioner_id + work-unit instance attribution compose through practitioner-RECORD per `arch/practitioner.md` §4 R-CC-10; cross-practitioner workflow handoff mechanics per `arch/practitioner.md` §14 W4 (composes with W2 cross-practitioner workflow handoff watch-list here) |
| `claim` (Phase 3.5 `arch/claim-defensibility.md` LOCKED) | Claims emitted during workflow_instance execution attribute to that workflow_instance (per `glossary/workflow.md` composes-with claim row); per-claim audit composes into workflow audit context; ad-hoc work claims attribute to work-unit + session without workflow_instance attribution; one work-unit instance contains N claims per `glossary/work-unit.md` |
| `engaged-authorship` (DERIVED axis-3) | Engagement events fire at workflow phases when codified workflow exists (drafting → review → signing); workflow's optional-overlay applicability is orthogonal to engaged-authorship's mandatory always-present status (engagement events fire per claim regardless of workflow_instance per `glossary/workflow.md` composes-with engaged-authorship row) |
| `quality-gate` (Pattern A; Phase 3.6 forthcoming) | workflow_instance execution + work-unit instance lifecycle events feed quality-gate's drift detection per `glossary/workflow.md` + `glossary/work-unit.md` composes-with quality-gate rows (e.g., practitioner approving phase transitions without engaging review content → axis-3 rubber-stamping signal; rapid sign-off cadence without sparring → axis-3 signal at attestation moment) |
| **axis-1 PRIMARY anchor** (workflow) | Workflow is what intertwined AI intertwines WITH per `glossary/workflow.md` axis-1 anchor + VISION "Workflow as precondition" implication; workflow primitive's optional-overlay design enables both codified-pattern intertwining AND ad-hoc intertwining (the latter via always-present work-unit container) |
| **axis-1 cross-axis** (work-unit) | Work-unit is the artifact-container axis-1 work happens IN per `glossary/work-unit.md` cross-axis claim |
| **axis-2** (sparring composition) | Sparring fires DURING workflow_instance phase progression AND ad-hoc work-unit progression; orthogonal to workflow primitive engagement; per `arch/sparring.md` §4 + `glossary/sparring.md` (sparring sub-mechanisms accessed by skills DURING workflow_instance phase progression per `arch/sparring.md` §4) |
| **axis-3** (defensibility composition) | work-unit instance is artifact-container authorship attaches TO; defensibility test resolves at work-unit + claim granularity per `arch/practitioner.md` §4 + `glossary/work-unit.md` composes-with practitioner row + `glossary/claim.md` defensibility-test-resolves-at-claim-granularity |

## 5. Cardinality + lifecycle (per primitive)

### Workflow cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Workflow DEFINITIONs per specialist | N | Each specialist DEFINITION declares its workflow patterns in `capability_declarations.workflow-definitions` per `arch/specialist-skill.md` §2.3 |
| Workflow_instances per workspace per active specialist | N | Instances created per work-unit when codified pattern applies; absent for ad-hoc work-units per `glossary/workflow.md` optional applicability |
| Workflow_instances per work-unit | 0..N | Cardinality asymmetry per §3 (work-unit may have 0+ workflow_instances attached, potentially across specialists) |
| Work-unit per workflow_instance | exactly 1 | Cardinality asymmetry per §3 (workflow_instance has exactly 1 work-unit attribution) |

### Workflow lifecycle (primary-summary; full state machine + event-kind catalog in §13)

**workflow definition lifecycle**:
- **Creator**: bundled within specialist DEFINITION (workflow definitions don't have independent author/version beyond their containing specialist per `glossary/workflow.md` lifecycle)
- **Versioning**: workflow definitions inherit specialist version; no per-workflow semver
- **Distribution**: distributed via specialist's Framework C placement per `arch/specialist-skill.md` §11
- **Immutability per version**: a workflow definition version is immutable once published; changes require specialist version bump

**workflow_instance lifecycle**:
- **Creator**: workspace runtime at workflow-start (when codified pattern applies; instance created per work-unit)
- **Owner**: Owner B scope (workspace-bound)
- **Mutability**: mutable-with-audit per `glossary/workflow.md` (state transitions, phase changes, artifact accumulation all audited)
- **Persistence**: persists across sessions via persistent-state mechanism per substrate Surface §F
- **Destructor**: workspace dissolution per §13 destruction semantics; orphan-instance handling per §13 orphan handling

### Work-unit cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Work-unit KINDs per specialist | N | Each specialist DEFINITION declares its kinds in `capability_declarations.work-unit-kinds` per `arch/specialist-skill.md` §2.3 |
| Work-unit instances per workspace per active kind | N | Instances created per accountability-bearing work piece; multiple concurrent typical for practitioner-shape per `glossary/work-unit.md` |
| Workflow_instances attached to work-unit | 0..N | Cardinality asymmetry per §3 |
| Claims contained in work-unit instance | N | One work-unit instance contains N claims per `glossary/work-unit.md` composes-with claim row (full claim mechanics → Phase 3.5 `arch/claim-defensibility.md`) |

### Work-unit lifecycle (primary-summary; full state machine + event-kind catalog in §13)

**work-unit kind lifecycle**:
- **Creator**: bundled within specialist DEFINITION
- **Versioning**: work-unit kinds inherit specialist version; no per-kind semver
- **Distribution**: distributed via specialist's Framework C placement
- **Immutability per version**: a work-unit kind version is immutable once published; changes require specialist version bump

**work-unit instance lifecycle**:
- **Creator**: workspace runtime when accountability-bearing work begins (instance created against active kind)
- **Owner**: Owner B scope (workspace-bound; owned by deployed specialist instance per `glossary/work-unit.md` composes-with specialist row)
- **Mutability**: mutable-with-audit per `glossary/work-unit.md` (state transitions, artifact accumulation, claim revisions all audited); kind FIXED at creation (no kind-switching mid-lifecycle; pivot creates new work-unit linked via predecessor_id per §13)
- **Persistence**: persists across sessions; retains for audit per workspace's audit-retention policy
- **Destructor**: workspace dissolution per §13 archival-as-default; orphan-instance handling per §13 orphan handling

## 6. Logic placement mode

Per `ARCHITECTURE.md` §6 Logic placement modes:
- **Workflow DEFINITION manifest** (frontmatter + capability declarations within specialist's bundle): Mode 1 production-runtime LLM-MD (workspace AI reads at activation + at workflow-start)
- **Work-unit KIND DEFINITION manifest** (frontmatter + per-kind structural conventions within specialist's bundle): Mode 1 production-runtime LLM-MD (workspace AI reads at activation + at instance creation)
- **workflow_instance entity-md** (per-deployment storage convention deferred to Phase 6): Mode 1 production-runtime LLM-MD (workspace AI reads at workflow_instance hydration + phase transitions) — though instance-content storage convention is deferred to Phase 6 deployment per §7 (per `MAINTENANCE.md` TOP-LEVEL SCOPE: instance-content storage is deployment-instance not framework)
- **work-unit instance entity-md** (per-deployment storage convention deferred to Phase 6): Mode 1 production-runtime LLM-MD
- **WorkflowDescriptor + WorkUnitKindDescriptor Pydantic shapes** (Phase 6 spec): Mode 3 hybrid spec layer
- **THIS topic + DR + GLOSSARY entries**: Mode 4 development-time documentation (NOT production-runtime)

Primitive-cluster topics are Mode 4 development-time documentation — articulating the architectural shape framework developers need to understand, not what production AI loads at runtime. Production AI in a deployed PBS workspace loads Mode 1 markdown (workflow + work-unit kind DEFINITIONs within active specialist bundles; workflow_instance + work-unit instance entity-md at workspace level; workspace.md; shape policy bundles); this topic is for framework-developer orientation.

**LLM-instruction tightness asymmetry** (per `ARCHITECTURE.md` §6 cross-cutting principles): Mode 1 markdown (workflow DEFINITION body content; work-unit KIND DEFINITION body content; per-deployment instance-md body content) requires the highest LLM-instruction tightness review effort because LLMs paper over imprecise markdown by inference. Phase 6 specialist-bundle authoring + per-deployment workflow_instance + work-unit instance authoring inherit this discipline.

## 7. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns.

### Error categories (architectural-level; per R-CC-11)

Per-shape error escalation policy lives in §8 Cross-shape policy variation; the categories themselves are framework-level:

| Category | Architectural meaning |
|---|---|
| `WorkflowDefinitionValidation` | Manifest frontmatter fails schema validation (missing required fields; invalid enum values; phases list malformed; phase_authority_requirements references undefined phase) |
| `WorkflowInstancePhaseTransitionViolation` | Illegal state transition (e.g., terminal state → running; phase out-of-sequence per workflow definition) |
| `WorkflowInstanceAuthorityBindingFailure` | Phase transition requires authority not present per `phase_authority_requirements` (e.g., review phase requires practitioner-only authority but session bound to under-supervision practitioner per `arch/practitioner.md` §2.2 signing_authority enum) |
| `WorkUnitKindValidation` | Manifest schema fail (missing required fields; lifecycle_states malformed; artifact_attachment_shape malformed) |
| `WorkUnitKindCollision` | Within-specialist kind name collision (cross-specialist disambiguated via specialist-namespace per `arch/specialist-skill.md` §10 R-N-1) |
| `WorkUnitInstanceLifecycleStateConflict` | State transition not in kind's `lifecycle_states` enum |
| `WorkUnitInstancePivotViolation` | Attempt to switch kind mid-lifecycle (per `glossary/work-unit.md` "kind is FIXED at creation; pivot creates new work-unit"); pivot must create new work-unit linked via `details.predecessor_work_unit_id` per §SD-4 event-kind catalog |
| `WorkflowInstanceOrphanReactivationFailure` | Specialist reactivated but workflow_instance state can't resume (version incompatibility between snapshot and current specialist version per §13 orphan handling) |

### Other operational concerns (Phase 6)

- **Per-deployment storage convention for workflow_instance + work-unit instance entity-md**: per `MAINTENANCE.md` TOP-LEVEL SCOPE instance-content storage is deployment-instance not framework; specific path schema lands Phase 6 deployment
- **Per-deployment ID uniqueness convention**: prose-rule pattern per archived `governance-and-identity-sourcing.md` decision 3 greenfield-evaluated per §15 (convention prose lives at deployment level, NOT framework level; AI applies at mint-time per Mode 1 markdown discipline)
- **Cross-practitioner workflow handoff implementation mechanics**: per W2 second-multi-practitioner-deployment-surface signal (composes with `arch/practitioner.md` §14 W4)
- **Per-kind structural conventions schema standardization**: per W3 ≥3-kinds-divergent-shapes signal (full schema design fires when concrete divergence accumulates; Phase 6 spec territory)
- **Multi-workflow_instance phase choreography implementation**: per W4 second-workspace-multi-workflow_instance-pattern signal (full mechanics → Phase 6 + cross-specialist phase ordering per `arch/specialist-skill.md` §10)
- **Workflow_instance suspension state implementation**: per-substrate suspension semantics; cross-session state preservation through suspended state
- **work-unit instance pivot mechanics implementation**: predecessor_work_unit_id link establishment; attribution chain preservation across pivot

## 8. Cross-shape policy variation (cluster-conditional; APPLIES)

Per primitive-cluster topic template `MAINTENANCE.md` Layer 3 §8 conditional applicability + Pattern A template §14 cross-shape policy variation precedent + `arch/adapter.md` §14 + `arch/audit.md` §14 + `arch/practitioner.md` §8: this section applies when primitive behavior is shape-policy-mediated. Workflow + work-unit cluster IS shape-policy-mediated (multi-practitioner work-unit authorship + workflow_instance flexibility + work-unit lifecycle policy + workflow_instance state-machine flexibility + work-unit kind required + authority-binding + audit emission granularity).

**What is shape-uniform** (NOT shape-policy-mediated):
- Bipartite Pattern B partition for both workflow + work-unit (DEFINITION at Framework C / INSTANCE at Owner B; same architectural commitment across all shapes)
- Workflow definition + work-unit kind manifest schemas (same fields per §2; per-shape policy declares which optional fields REQUIRED per shape)
- Always-present asymmetry (work-unit always present; workflow_instance optional per §3; same architectural commitment across all shapes)
- Cardinality asymmetry (1 work-unit per workflow_instance; N workflow_instances per work-unit; same per shape)
- Snapshot pattern (definition_snapshot + kind_snapshot at creation; same per shape)
- Specialist-namespace mechanics (per `arch/specialist-skill.md` §10 R-N-1; same per shape)

**What is shape-policy-mediated**:

| Dimension | practitioner-shape | autonomous-business-shape | personal-OS-shape |
|---|---|---|---|
| **Multi-practitioner authorship of work-unit** | Solo = 1; partnership/firm = N per `arch/practitioner.md` §3 cardinality matrix | N/A (no human-practitioner concept; operator/board are humans but not "practitioners" per `arch/practitioner.md` §8) | 1 user typically (single-user concept per `arch/practitioner.md` §8) |
| **work-unit lifecycle policy** | Defensibility-critical preservation (sent/archived states preserve attribution chain; rapid-archive prohibited under deadline per `glossary/category-collapse.md` axis-3 risk) | Archival OR delete-with-audit per business policy | Minimal lifecycle (deletion permitted per user preference; no professional-accountability concern) |
| **workflow_instance state-machine flexibility** | Strict (state transitions audit-emitted; rollback prohibited per defensibility — only re-start a new workflow_instance) | Tolerant (auto-rollback per business retry policy permitted) | Tolerant |
| **work-unit kind required** | Per shape policy may mandate (e.g., legal-practice mandates `matter` kind) | Per business policy (e.g., autonomous-business may mandate `task` + `order`) | Optional (kind discriminator per user preference) |
| **Authority-binding on workflow phase transition** | Per workflow definition `phase_authority_requirements` per phase (per §2.1; e.g., review → send transition requires practitioner-only authority per defensibility-critical) | Programmatic per business + budget policy (per `arch/audit.md` §14 trust model) | Optional |
| **Audit emission granularity per work-unit** (composes with `arch/audit.md` §14) | Claim-level mandatory (per `arch/audit.md` §14 practitioner-shape granularity) | Action-level (per `arch/audit.md` §14 autonomous-business granularity) | Light (per `arch/audit.md` §14 personal-OS granularity) |

Workflow + work-unit cluster primitives stay shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (both primitives' bipartite Pattern B structure is uniform across all shapes; per-shape variation lives in shape policy bundle declaring per-shape required-categories + per-shape lifecycle policy + per-shape audit emission granularity).

## 9. Granularity tests (cluster-conditional; APPLIES)

Per primitive-cluster topic template, granularity tests apply when primitives have granularity discriminators. Both workflow definition + work-unit kind have granularity discriminators per `glossary/workflow.md` boundary tests + `glossary/work-unit.md` boundary tests. This section contains TWO 3-tests (per-primitive granularity discriminators differ between workflow + work-unit per `arch/specialist-skill.md` §9 anchored 3-test pattern precedent).

### Workflow definition granularity 3-test

When considering "should this be ONE workflow OR split into multiple? / should ad-hoc be codified?" — apply all three:

1. **Phase-boundary clarity** — clearly separable phases? (Phases blurry/blending → ad-hoc instead of codification; codification of unclear phases produces brittle workflow definitions that don't capture the actual work pattern.)
2. **Reusability across work-units** — applies to ≥3 work-unit instances? (Single-use → ad-hoc better; per `glossary/workflow.md` evolution path "pattern crystallizes when noticed repeatedly". Codifying single-use patterns adds workflow surface without cross-work-unit reuse benefit.)
3. **Specialist-coherence** — belongs to ONE specialist's competence area? (Cross-specialist workflows = mis-bundled per `arch/specialist-skill.md` §9 specialist 3-test cohesion criterion; re-assign OR cross-specialist invocation via fully-qualified `specialist-name:workflow-name` per `arch/specialist-skill.md` §10 cross-specialist composition rules.)

A workflow definition passing all three is well-shaped. A workflow definition failing one is a candidate for restructure (split into smaller workflows / decode to ad-hoc / re-assign to different specialist).

### Work-unit kind granularity 3-test

When considering "should this be ONE kind OR split into multiple?" — apply all three:

1. **Boundedness** — bounded artifact-container with single accountability scope? (E.g., `project` for B-Plan = bounded; `general-work` = unbounded mis-shape — too generic to provide meaningful structural conventions per `glossary/work-unit.md` "specialist-defined discriminator + per-kind structural conventions".)
2. **Archetype-discriminator** — specialized for ONE archetype's domain (e.g., `matter` legal-practice; `case` medical-practice) OR cross-archetype generic (e.g., `task` autonomous-business + personal-OS)? (Both well-shaped at appropriate shape per `glossary/work-unit.md` cross-archetype illustration; the question is: is the kind specialized OR genuinely cross-archetype, NOT split-or-unify-at-tier-1.)
3. **Lifecycle-distinctiveness** — distinct lifecycle-states OR artifact-attachment shapes warrant separate kind vs reuse existing? (E.g., `audit` kind `under-review` state distinct from `manuscript` kind; if lifecycle + attachment shapes are identical to existing kind, candidate for merge OR reuse via existing kind.)

A work-unit kind passing all three is well-shaped. A work-unit kind failing one is a candidate for restructure (split into more-bounded kinds / re-classify archetype-tier / merge with existing kind sharing lifecycle).

### Composition with specialist 3-test (subordinate)

Workflow + work-unit kind 3-tests are SUBORDINATE to `arch/specialist-skill.md` §9 specialist 3-test:
- Specialist 3-test asks "should THIS specialist exist" (cohesion + distributability + reusability per `arch/specialist-skill.md` §9)
- Workflow + work-unit kind tests ask "should THIS workflow / kind exist within validated specialist"
- Foundation-up: specialist granularity validates first; workflow + work-unit kind granularity within validated specialist

This composition reflects the bundle hierarchy: specialist BUNDLES workflow + work-unit kind DEFINITIONs per `arch/specialist-skill.md` §10; the contained primitives' granularity is evaluated within the validated bundle's competence area.

### Two-tier classification N/A

Workflow + work-unit kinds INHERIT containing specialist's `tier: domain-anchored | cross-archetype` per `arch/specialist-skill.md` §9 manifest schema. Per-primitive tier classification for workflow + work-unit kinds adds vocabulary surface without genuine discrimination — REJECTED via Round 1 ST3 (per §15 manufactured-criticism rejections).

The reasoning: a workflow definition's tier is the containing specialist's tier (a workflow inside `planning-document-work` specialist inherits `domain-anchored`; a workflow inside `project-management` specialist inherits `cross-archetype`); per-workflow tier override would create ambiguity about which classification applies (containing specialist's vs workflow's own). Same applies to work-unit kinds.

## 10. Bundle composition (cluster-conditional; N/A)

**N/A** — workflow + work-unit are bundled IN specialist per `arch/specialist-skill.md` §10; they are NOT bundlers themselves. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §10 applies when a primitive in the cluster BUNDLES other artifacts (e.g., specialist BUNDLES skills + entity-kinds + workflows + work-unit-kinds + adapter implementations per `arch/specialist-skill.md` §10). Workflow definition + work-unit kind DEFINITION are themselves BUNDLED ARTIFACTS within specialist's bundle — they don't bundle other artifacts in a directory-structure sense.

The `triggered_skills` field on workflow definition (per §2.1 manifest schema) references skills by name — this is REFERENCE composition, not BUNDLE composition. Skills are bundled within specialist's `skills/` subdirectory (per `arch/specialist-skill.md` §2.3 directory structure); workflow definition references them by local name within the same specialist (or fully-qualified `specialist-name:skill-name` for cross-specialist invocation per `arch/specialist-skill.md` §10).

§10 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule (preserves template-anchoring stability for downstream primitive-cluster topics). Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template per-pattern conditional applicability rule: "Two Pattern B clusters (workflow-work-unit): granularity + per-primitive lifecycle ordering likely apply; bundle / marketplace likely N/A (workflow + work-unit are bundled IN specialist, not bundlers themselves)" — confirmed N/A per this analysis.

## 11. Marketplace + distribution mechanics (cluster-conditional; N/A)

**N/A** — workflow + work-unit kind DEFINITIONs are distributed THROUGH specialist DEFINITION per `arch/specialist-skill.md` §11; they are NOT independently distributable. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §11 applies when a primitive in the cluster is canonical distributable (e.g., specialist as canonical distributable per `glossary/specialist.md` + `arch/specialist-skill.md` §11). Workflow + work-unit kind DEFINITIONs inherit Framework C placement via specialist composition per `glossary/workflow.md` + `glossary/work-unit.md`; they ride along with specialist's distribution channels (consulting deliverable / internal firm reuse / OSS / marketplace future-conditional / backup-migration per `profiles/G-composability-gate.md` 5-mode framing) but don't have independent distribution mechanics.

A workflow definition or work-unit kind cannot be distributed standalone (no manifest of its own beyond the specialist's `capability_declarations.workflow-definitions` + `capability_declarations.work-unit-kinds` lists per `arch/specialist-skill.md` §2.3 manifest schema). Cross-deployment portability concerns (e.g., workflow definition consumed across multiple workspaces) are specialist-distribution mechanics per `arch/specialist-skill.md` §11, NOT workflow-or-work-unit-kind distribution mechanics.

§11 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template per-pattern conditional applicability rule: "Two Pattern B clusters (workflow-work-unit): granularity + per-primitive lifecycle ordering likely apply; bundle / marketplace likely N/A" — confirmed N/A per this analysis.

## 12. Cross-references reservation

Cross-references for this topic are consolidated in §17 below per primitive-cluster topic template convention; this section number reserved as **N/A-parity slot** preserving visual numbering parity with substrate's §12 Transport variation N/A + `arch/specialist-skill.md` §12 reservation + `arch/practitioner.md` §12 reservation. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template §-numbering convention: "**§12 reserved as N/A-parity slot** (parity with substrate's §12 Transport variation N/A — preserves visual numbering parity across topic-templates; downstream primitive-cluster topic Writers MUST keep §12 reserved as N/A-parity rather than omit-§12 or fill-§12-with-content; prevents template drift)."

## 13. Per-primitive lifecycle ordering (cluster-conditional; APPLIES)

Both workflow_instance + work-unit instance have load-bearing state machines + lifecycle ordering distinct from §5 cardinality + lifecycle treatment. Two state machines + cross-pattern destruction + orphan handling + boot integration. Lifecycle ordering integrates with substrate boot/shutdown phases per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection.

### workflow_instance state machine

**States** (per `glossary/workflow.md` lifecycle):
- `running` — workflow_instance actively progressing through phases
- `suspended` — workflow_instance paused (cross-session boundary suspension; explicit user-initiated suspension)
- `completed` — terminal state (workflow_instance successfully completed all phases)
- `abandoned` — terminal state (workflow_instance explicitly abandoned by practitioner; e.g., project cancelled mid-workflow)
- `failed` — terminal state (workflow_instance failed due to error; e.g., authority-binding failure that cannot be resolved)

**Transitions** (per R-CC-3):
- `running ↔ suspended` (bidirectional pause/resume)
- `running → completed | abandoned | failed`
- `suspended → completed | abandoned | failed` (non-terminal suspended state can transition to terminal)

**Event-kind catalog** (architectural enumeration; Phase 6 lands Pydantic per-event-shape schemas):
- `workflow_started` — workflow_instance created with definition snapshot per §2.2 (`details.definition_ref`; `details.attached_work_unit_id`; `details.bound_practitioner_id`)
- `workflow_phase_transitioned` — phase change with `details.from_phase` + `details.to_phase` per archived `audit-trail-v2.md` `details:` payload precedent (greenfield-evaluated per §15)
- `workflow_suspended` — running → suspended transition
- `workflow_resumed` — suspended → running transition
- `workflow_completed` — terminal completion event
- `workflow_abandoned` — terminal abandon event
- `workflow_failed` — terminal failure event with `details.failure_category` per §7 error categories

### work-unit instance state machine

**States** (per `glossary/work-unit.md` lifecycle; kind-default; per-kind extensible per `kind.lifecycle_states` field per §2.3 schema):
- `initiated` — work-unit instance created against active kind
- `in-progress` — work proceeds (with or without workflow_instance attached)
- `completed` — terminal state (work-unit instance work completed)
- `sent` — terminal state (work-unit instance output sent to recipient; practitioner-shape send-action terminal)
- `archived` — terminal state (work-unit instance archived; preserves audit-trail attribution per `arch/practitioner.md` §13 archival-as-default cross-pattern coherence)

**Per-kind extensibility**: kind-specific state machine via `kind.lifecycle_states` field per §2.3 schema (e.g., `audit` kind may add `under-review` state between `in-progress` and `completed`; `manuscript` kind may add `revision` state between `completed` and `sent`). Per `glossary/work-unit.md` "kind-specific state machine" — different specialists may declare different lifecycle state machines per their kind's structural conventions.

**Transitions** (kind-specific; default flow):
- `initiated → in-progress`
- `in-progress → completed | sent`
- `completed → sent | archived`
- `sent → archived`

**Event-kind catalog** (architectural enumeration):
- `work_unit_created` — work-unit instance created with kind snapshot per §2.4 (`details.kind_ref`; `details.owning_specialist_id`; `details.attribution`)
- `work_unit_state_transitioned` — state change with `details.from_state` + `details.to_state` per archived `audit-trail-v2.md` `details:` payload precedent (greenfield-evaluated per §15)
- `work_unit_completed` — terminal completion event
- `work_unit_sent` — terminal send event (practitioner-shape; signed-claim emission moment per `glossary/authority-binding.md` line 35)
- `work_unit_archived` — terminal archive event
- `work_unit_pivoted` — pivot event (per R-CC-4); kind-FIXED-at-creation enforcement; pivot creates new work-unit linked via `details.predecessor_work_unit_id` per `glossary/work-unit.md` "kind is FIXED at creation; pivot creates new work-unit"

### Cross-pattern destruction coherence

Per `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13: archival-as-default on workspace dissolution per `workspace.md` `instance_content_dissolution_policy: archive | delete-with-audit` (same field per cross-pattern coherence convention; this topic adopts the same field shape).

- **Default**: archival preserves practitioner work + axis-3 authorship preservation + 6-months-later defensibility test re-runable for both workflow_instance + work-unit instance
- **Opt-in**: deletion-with-audit policy declared at `workspace.md` level (workspace declares `instance_content_dissolution_policy: archive | delete-with-audit` per `arch/specialist-skill.md` §13 precedent + `arch/practitioner.md` §13 precedent; same field shape — cross-pattern coherence)
- Per-shape policy may restrict the opt-in (practitioner-shape policy may prohibit deletion-with-audit per defensibility-critical concern per `arch/practitioner.md` §8 deactivation policy row)

Archival mechanics → Phase 6 (workspace serialization mechanics; archive format; restoration semantics; per `profiles/G-composability-gate.md` backup-migration mode).

### Orphan-instance handling

Per `glossary/work-unit.md` line 39: owning specialist deactivated (workspace `specialists_active` change) → existing work-unit instances of that kind become orphan-state; PRESERVED per specialist persistence rule (per `arch/specialist-skill.md` §5 INSTANCE-CONTENT preservation cross-pattern coherence with `glossary/specialist.md` "deactivating a specialist doesn't delete its accumulated content; preserves practitioner work"); reactivation restores progression capability; NO auto-archive.

Same applies to attached workflow_instances of orphaned work-units — workflow_instance state preserved (lifecycle_state retained); resumes when specialist reactivated. If specialist version incompatible with workflow_instance's `definition_snapshot` at reactivation time → `WorkflowInstanceOrphanReactivationFailure` per §7 error category (version-incompatibility surfaces; per-shape escalation per §8).

### Boot integration

Per `ARCHITECTURE.md` §6 composite boot subsection + `arch/specialist-skill.md` §13 boot step 9: workflow + work-unit kind DEFINITIONs registered at substrate-phase 4 step 9 (already covered by specialist-skill boot ordering — workflow + work-unit kind DEFINITIONs ride along with specialist registration step). workflow_instance + work-unit instance entity hydration follows from Owner B INSTANCE-CONTENT load (per `glossary/owner-b-scope.md` work-unit instances are workspace-scope managed entities; loaded at substrate-phase 5+ post-specialist-registration when workspace state hydration occurs).

### Mid-session lifecycle ordering

Mid-session workflow_instance creation (when codified pattern applies to new work-unit instance) + work-unit instance creation (when accountability-bearing work begins) follow no special boot ordering — they are runtime events emitted via audit Surface §A per §SD-4 event-kind catalog. In-flight workflow_instances NOT disrupted by mid-session specialist activation per `glossary/workflow.md` "workflow_instance doesn't gate capability changes" + `arch/specialist-skill.md` §5 mid-session re-binding.

## 14. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| **W1** | Workflow_pattern primitive vs Layer A reusable templates | ≥2 specialists develop genuinely-cross-archetype workflow pattern that Layer A growth proves insufficient for | Examine then; primitive remains unwarranted by default per `glossary/workflow.md` See section explicit decision (mental modeling resolves SHAPED-AS-LAYER-A per D Gate procedure per `profiles/INDEX.md`); cross-link: `BACKLOG.md` Phase 5+ "Cross-specialist shared workflow patterns insufficient via Layer A" carryover |
| **W2** | Cross-practitioner workflow handoff mechanics | Second multi-practitioner deployment surface (pioneer is solo per `profiles/L5a-planner-pbs-schulz.md` lines 95-101) | `workflow_handoff` event-kind shape design + attribution chain preservation rules + per-shape required-handoff-recipient enforcement per shape policy; cross-link: `arch/practitioner.md` §14 W4 (composes with same awaited-signal — second multi-practitioner deployment surface) |
| **W3** | Per-kind structural conventions schema standardization | ≥3 kinds across specialists develop divergent artifact-attachment shapes warranting standardization | Per-kind structural conventions schema (work-unit kind manifest extension per §2.3 `artifact_attachment_shape` field); Phase 6 spec territory; awaits divergence accumulation across deployments |
| **W4** | Multi-workflow_instance phase choreography mechanics | Second workspace deploys multi-workflow_instance against single work-unit pattern (pioneer L5a documents single-workflow_instance + ad-hoc transitions, not concurrent multi-workflow_instance per lines 60-73) | Per-workflow phase coordination semantics + cross-specialist phase ordering; cross-link: `arch/specialist-skill.md` §10 cross-specialist composition rules (multi-workflow_instance per work-unit may surface cross-specialist phase choreography concerns) |

## 15. Decision-design provenance

Provenance for this topic lives in DR + HANDOFF + git log per `MAINTENANCE.md` Lens 5 v0.2.1 provenance hygiene + per `coherence-audit` Lens 5. See `docs/decisions/workflow-work-unit-arch-topic.md` for sharpening trajectory + Round 1 + Round 2 EXPANSIONS + manufactured-criticism rejections + GLOSSARY back-check verdict + profile-anchored validation cluster citations + Mode 2 composite decomposition rationale.

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: workflow + work-unit cluster primitives stay shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz) reality (per `profiles/L5a-planner-pbs-schulz.md` lines 22-29 B-Plan workflow phases + lines 60-73 hybrid moments + `project` work-unit kind) grounds the cluster primitives without leaking pioneer specifics into the framework definitions. Cross-archetype illustration in §2 + §5 + §9 anchors framework neutrality (legal `matter` / medical `case` / consulting `engagement` / research `manuscript` / accounting `audit` / autonomous-business `task`/`order` / personal-OS `task`/`goal` / federation `peering` per `glossary/work-unit.md` cross-archetype illustration).

## 16. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.5 | LOCKED |
| WorkflowDescriptor + WorkUnitKindDescriptor Pydantic schemas | 6 | Mode 3 spec; manifest schema typing per §2; WorkflowError + WorkUnitError class hierarchies per §7 |
| Per-deployment workflow_instance + work-unit instance entity-md authoring | Workspace deployment (NOT this repo) | Per `MAINTENANCE.md` TOP-LEVEL SCOPE: instance-content storage convention is deployment-instance; build into deployed workspace (Phase 6 deployment) |
| Per-deployment ID uniqueness convention prose | Workspace deployment (NOT this repo) | Prose-rule pattern per archived `governance-and-identity-sourcing.md` decision 3 (greenfield-evaluated per §15); deployment-side prose, AI applies at mint time per Mode 1 markdown discipline |
| Per-kind structural conventions schema standardization (W3) | 6 | Per W3 watch-list; awaits ≥3-kinds-divergent-shapes signal; work-unit kind manifest extension |
| Cross-practitioner workflow handoff (W2) | 5+ | Per W2 watch-list; awaits second multi-practitioner deployment; composes with `arch/practitioner.md` §14 W4 |
| Multi-workflow_instance phase choreography (W4) | 5+ | Per W4 watch-list; awaits second workspace multi-workflow_instance pattern; composes with `arch/specialist-skill.md` §10 cross-specialist composition |
| Workflow_pattern primitive vs Layer A reusable templates (W1) | 5+ | Per W1 watch-list; awaits ≥2-specialists-genuinely-cross-archetype-workflow-pattern signal; primitive remains unwarranted by default |
| Workspace serialization / archival format | 6 | Per §13 workspace dissolution; archival mechanics per cross-pattern coherence with `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 |

## 17. Cross-references

- **GLOSSARY**: `workflow` (canonical bipartite Pattern B with optional applicability entry); `work-unit` (canonical bipartite Pattern B with always-present container entry); `specialist` (containing primitive; workflow + work-unit DEFINITIONs nest within specialist's bundle); `skill` (composes-with workflow → skill direction); `practitioner` (multi-practitioner authorship per shape; bound_practitioner_id reference); `authority-binding` (per-event actor declaration; phase transitions may bind); `session` (sessions execute parts of workflow_instance); `claim` (work-unit instance contains N claims; forward-reference to claim-defensibility); `Owner B scope` (workflow_instance + work-unit instance placement); `Framework C scope` (workflow definition + work-unit kind placement via specialist's bundle); `framework`, `mechanism`, `workspace`, `shape`, `substrate`, `adapter`, `audit`, `event`, `actor`, `engaged-authorship`, `quality-gate`, `category-collapse`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern B row (workflow + work-unit; the cluster pairs two Pattern B primitives); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (work-unit kind FIXED at creation gate-enforced structural; cross-specialist work-unit WRITES prohibited structural per axis-3); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (workflow + work-unit cluster primitives stay shape-neutral; cross-archetype illustration anchors framework neutrality); `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment workflow_instance + work-unit instance instance-content lives at deployment-instance, not framework repo); `ARCHITECTURE.md` §6 cross-cutting principles "AI as runtime" + "LLM-instruction tightness for Mode 1 markdown layer" + "Workspace boot + shutdown composite sequence"; `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 10 (greenfield-evaluation of archived sources)
- **Profiles validated**: `L5a-planner-pbs-schulz.md` (lines 22-29 B-Plan workflow phases — validates SD-2 workflow definition manifest schema phases field; lines 60-73 hybrid moments — validates SD-3 ad-hoc work first-class commitment + cardinality asymmetry + always-present asymmetry; lines 76-83 active specialists set — validates SD-1 + SD-3 cross-specialist composition; lines 95-101 multi-user moments — validates W2 cross-practitioner workflow handoff awaiting second multi-practitioner deployment; lines 119-129 stress-tests — validates per-shape trust model parameterization per SD-6 §8 cross-shape policy variation matrix) + `G-composability-gate.md` (lines 14-22 multi-mode consumption framing — validates SD-1 12+5 template extension; lines 154-157 cross-shape consumption rules — validates SD-6 §8 cross-shape policy variation matrix shape-policy-mediated rows; lines 162-184 architectural concerns surfaced — backup-migration round-trip implicates work-unit instance + workflow_instance portability per W3 + W4) + `L1-specialist-creator.md` (lines 18-29 specialist creator stress-tests — validates SD-1 cluster boundary "workflow + work-unit DEFINITIONs nest within specialist's bundle"; workflow definition packaging row + work-unit kind packaging implicit per L1's intended-stress-test enumeration; specialist self-containment + cross-shape compatibility validate SD-2 manifest schema + SD-6 cross-shape policy variation; SKELETON profile fleshed-on-demand for this validation per `profiles/INDEX.md` skeleton-fleshing-on-demand strategy)
- **ARCH topics composing with workflow + work-unit**: `arch/substrate.md` (Surface §C permission flow integrates with workflow_instance phase transitions + work-unit instance lifecycle transitions for authority-binding moments per §13; Surface §F session/context management persists workflow_instance + work-unit instance state across sessions; §10 boot/shutdown integration per ARCHITECTURE.md §6 composite subsection); `arch/audit.md` (Surface §A emission API for §SD-4 event-kind catalog; Surface §C query API for cross-workflow_instance + cross-work-unit-instance audit-trail defensibility; §14 cross-shape policy variation per-shape audit emission granularity composes with work-unit attribution); `arch/sparring.md` (sparring sub-mechanisms accessed by skills DURING workflow_instance phase progression AND ad-hoc work-unit progression; orthogonal to workflow primitive engagement; per §4 per-shape activation matrix); `arch/adapter.md` (adapters invoked by skills firing within workflow_instance phases per `glossary/skill.md` composes-with adapter row); `arch/specialist-skill.md` (Phase 3.5 first primitive-cluster LOCKED — workflow + work-unit DEFINITIONs nest within specialist's bundle per §10; cross-specialist composition rules per §10 + §3 apply to cross-specialist work-unit attachment); `arch/practitioner.md` (Phase 3.5 second primitive-cluster LOCKED — workflow_instance bound_practitioner_id + work-unit instance attribution compose through practitioner-RECORD per §4 R-CC-10; cross-practitioner workflow handoff mechanics per §14 W4 composes with W2 here). `arch/claim-defensibility.md` (Phase 3.5 fourth primitive-cluster LOCKED — claims emitted during workflow_instance execution attribute to that workflow_instance per `glossary/workflow.md` composes-with claim row; work-unit instance contains N claims per `glossary/work-unit.md`; per-claim attestation chain composes through workflow_instance + work-unit instance attribution per `arch/claim-defensibility.md` §3 + §13; cross-pattern destruction inheritance for claims per `arch/claim-defensibility.md` §13 — claims inherit work-unit's `instance_content_dissolution_policy` per cross-pattern coherence with §13 archival-as-default; per-claim audit composes into work-unit attribution chain). `arch/scope-model.md` (Phase 3.5 first cross-cutting integrator LOCKED — workflow + work-unit two-Pattern-B bipartite cluster composes through scope-model per §4 E2 nested-bundle pattern: workflow DEFINITION + work-unit KIND DEFINITION nested in specialist's Framework C bundle under specialist-namespace (fully-qualified `specialist-name:workflow-name` + `specialist-name:kind-name`) + workflow_instance + work-unit instances at Owner B per §4 per-primitive composition narrative; always-present asymmetry preserved across scope placement (work-unit instance always-present at Owner B; workflow_instance optional overlay at Owner B); §18 per-primitive composition table workflow row + work-unit row). `arch/axis-interactions.md` (Phase 3.5 sixth + final ARCH topic LOCKED; second cross-cutting integrator extending scope-model anchor WITHOUT variation — workflow **axis-1 PRIMARY** per §4.1 per-primitive axis-anchoring catalog (workflow IS what intertwined AI intertwines WITH per `glossary/workflow.md` axis-1 PRIMARY anchor); cross-axis container for work-unit (work-unit is the artifact-container all axes operate against per `glossary/work-unit.md` cross-axis classification); work-unit is the cross-axis aggregation point — per-claim defensibility composes work-unit defensibility (axis-3); workflow_instance phase progression hosts axis-1 intertwined work; sparring fires DURING work-unit progression (axis-2); §18 per-primitive composition table workflow row + work-unit row — Phase 3.5 CLOSED with this lock). Forward-references to Phase 3.6 topics: `arch/quality-gate.md` (Pattern A Phase 3.6 — workflow_instance execution + work-unit instance lifecycle events feed quality-gate's drift detection per `glossary/workflow.md` + `glossary/work-unit.md` composes-with quality-gate rows)
- **Phase 6 spec target**: `docs/specs/workflow.md` (WorkflowDescriptor + workflow_instance Pydantic schemas; lifecycle state machine; WorkflowError class hierarchy); `docs/specs/work-unit.md` (WorkUnitKindDescriptor + work-unit instance Pydantic schemas; per-kind extensible state machine; WorkUnitError class hierarchy)
- **Archived sources** (INPUT only per `disciplines/10-greenfield-evaluation.md` — archive citations name SOURCE where input came from, NOT TEMPLATE where structure transferred; each cited element greenfield-evaluated against current locked vocabulary per Discipline 10): `archive/docs/decisions/entity-md-scope-model-restructure.md` (NAMING SUPERSEDED per archived header — "office-level entities" → "workspace-scope managed entities" per current locked vocabulary; Owner B placement of work-unit instances + per-kind structural conventions concept cited as INPUT for SD-2 work-unit kind manifest schema `artifact_attachment_shape` field but NOT transcribed verbatim — archive uses pre-rebuild scope model; current locked vocabulary uses A-B-C scope model per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; greenfield-derived schema per current Pattern B bipartite + locked GLOSSARY entries); `archive/docs/decisions/audit-trail-v2.md` (`details:` payload precedent for `details.changed_fields` + `details.predecessor_work_unit_id` + `details.from_phase`/`to_phase` event-kind shapes cited as INPUT for §SD-4 event-kind catalog but NOT transcribed verbatim — archive uses prior event_kind catalog; current locked vocabulary aligns event-kinds to current GLOSSARY primitives + minimal event-kind catalog growth per `details:` payload pattern; greenfield-derived event-kind catalog per current Pattern B + lifecycle states per locked GLOSSARY); `archive/plugin/skills/` (per-specialist DEFINITION files referencing workflow + work-unit kind patterns cited as INPUT for cross-archetype illustration but NOT transcribed verbatim — archive's per-specialist content is pre-rebuild; current locked GLOSSARY cross-archetype examples per `glossary/work-unit.md` adequately cover archetype illustration; greenfield-derived cluster boundary per current Pattern B nesting per `arch/specialist-skill.md` §10); `archive/docs/decisions/governance-and-identity-sourcing.md` (decision 3 = per-deployment uniqueness convention preserved as deployment-side commitment per §7 / §16; decision 4 = prose-rules pattern for ID minting cited as deployment-level discipline)

## 18. Composition table

How workflow + work-unit cluster primitives compose with key framework primitives + Pattern A protocols + mechanism classes (one column per cluster primitive — workflow + work-unit):

| Composing primitive | Workflow composition | Work-unit composition |
|---|---|---|
| **substrate Surface §C** (permission flow) | workflow_instance phase transitions request permission per `phase_authority_requirements` (per §2.1 + §13); HITL approval moments record practitioner identity per `glossary/authority-binding.md` "authority-decision binding" sub-aspect | work-unit instance lifecycle transitions (especially `sent` + `archived`) request permission per per-shape policy; practitioner-shape send-action requires practitioner-only authority per defensibility-critical |
| **substrate Surface §F** (session/context management) | workflow_instance state persists across sessions via persistent-state mechanism; one workflow_instance can span many sessions per `glossary/workflow.md` composes-with session row | work-unit instance state persists across sessions via persistent-state mechanism; multiple sessions over time per `glossary/work-unit.md` cardinality + lifecycle |
| **audit mechanism class** (Surface §A emission API) | workflow_instance lifecycle events per §SD-4 catalog (workflow_started / workflow_phase_transitioned / workflow_suspended / workflow_resumed / workflow_completed / workflow_abandoned / workflow_failed) flow through audit Surface §A | work-unit instance lifecycle events per §SD-4 catalog (work_unit_created / work_unit_state_transitioned / work_unit_completed / work_unit_sent / work_unit_archived / work_unit_pivoted) flow through audit Surface §A |
| **audit mechanism class** (Surface §C query API) | Cross-workflow_instance audit-trail query pattern for defensibility test mechanic; reconstruct historic phase progression through workflow_instance attribution chain | Cross-work-unit-instance audit-trail query pattern; reconstruct historic claim attribution chain through work-unit instance attribution |
| **authority-binding mechanism** | workflow_instance phase transitions may require specific authority per workflow definition `phase_authority_requirements` per `glossary/workflow.md` composes-with authority-binding row; per-phase authority binding parameterized by per-shape trust model | work-unit instance lifecycle transitions emit events bound to authority-decision actor per `glossary/work-unit.md` composes-with authority-binding row (practitioner-shape send/archive = practitioner-only; autonomous-business-shape transitions = operator-attestation programmatic) |
| **adapter** (Pattern A protocol) | Adapters invoked by skills firing within workflow_instance phases per `glossary/skill.md` composes-with adapter row (e.g., draft-cover-mail invokes email-adapter at workflow_instance send phase) | Adapter invocations attributed to work-unit instance via skill-side MCP audit gate per `arch/substrate.md` §8 dual-emission |
| **sparring** (mechanism class) | Sparring sub-mechanisms accessed by skills DURING workflow_instance phase progression per `arch/sparring.md` §4; sparring fires AT workflow_instance review phases (e.g., review-draft skill activates sparring sub-mechanisms per `profiles/L5a-planner-pbs-schulz.md` lines 43-48) | Sparring fires DURING ad-hoc work-unit progression too (orthogonal to workflow primitive engagement; per §4 cross-axis composition row); sparring outcomes attributed to work-unit instance per `glossary/work-unit.md` |
| **specialist-skill** (Phase 3.5 first primitive-cluster) | Workflow definitions nest within specialist's bundle per `arch/specialist-skill.md` §10 (workflow definitions live in specialist's distributable bundle at Framework C); workflow definition references skills by name (composition direction: workflow → skill); cross-specialist via fully-qualified `specialist-name:skill-name` per `arch/specialist-skill.md` §10 | Work-unit kind DEFINITIONs nest within specialist's bundle per `arch/specialist-skill.md` §10; work-unit instance owned by deployed specialist instance per `glossary/work-unit.md` composes-with specialist row + `arch/specialist-skill.md` §10 cross-specialist composition rules (cross-specialist work-unit attachment PERMITTED; ownership mutation PROHIBITED) |
| **practitioner** (Phase 3.5 second primitive-cluster) | workflow_instance binds to ONE practitioner-record at session-open per `arch/practitioner.md` §4 R-CC-10 (workflow_instance.bound_practitioner_id references session-bound practitioner per §2.2); cross-practitioner workflow handoff mechanics per W2 (composes with `arch/practitioner.md` §14 W4) | work-unit instance attribution composes through practitioner-RECORD per `glossary/work-unit.md` composes-with practitioner row; multi-practitioner-shape variants = shape-policy per `arch/practitioner.md` §3 + §8; defensibility test asks "will the practitioner defend THIS work-unit's outputs?" per `glossary/practitioner.md` |
| **claim primitive** (Phase 3.5 `arch/claim-defensibility.md` LOCKED) | Claims emitted during workflow_instance execution attribute to that workflow_instance per `glossary/workflow.md` composes-with claim row; per-claim audit composes into workflow audit context | Work-unit instance contains N claims per `glossary/work-unit.md` composes-with claim row; work-unit is artifact-container, claim is atomic content-unit within; ad-hoc work claims attribute to work-unit + session without workflow_instance attribution |
| **engaged-authorship** (DERIVED axis-3) | Engagement events fire at workflow phases when codified workflow exists (drafting → review → signing); workflow's optional-overlay applicability is orthogonal to engaged-authorship's mandatory always-present status | Engagement events fire per claim within work-unit regardless of workflow_instance attribution per `glossary/workflow.md` composes-with engaged-authorship row |
| **quality-gate** (Pattern A; Phase 3.6 forthcoming) | workflow_instance execution is observability source for quality-gate's drift detection (e.g., practitioner approving phase transitions without engaging review content → axis-3 rubber-stamping signal) per `glossary/workflow.md` composes-with quality-gate row | work-unit instance lifecycle events + per-claim emissions feed quality-gate's drift detection (e.g., rapid sign-off cadence without sparring → axis-3 rubber-stamping signal at attestation moment) per `glossary/work-unit.md` composes-with quality-gate row |
| **Pattern A protocols** (substrate / adapter / quality-gate) | Workflow composes with substrate Surface §C + §F (permission flow + session/context management); adapter invocation via skills firing within workflow phases; quality-gate Pattern A composes with workflow_instance observability per Phase 3.6 | Work-unit composes with substrate Surface §F (session/context management for state persistence); adapter invocation attributed to work-unit per skill-side audit emission; quality-gate Pattern A composes with work-unit instance observability per Phase 3.6 |
| **Pattern B primitives** (specialist) | Workflow is one of two Pattern B primitives in this cluster (the other being work-unit); specialist DEFINITION CONTAINS workflow definitions per `arch/specialist-skill.md` §10 | Work-unit is the other Pattern B primitive in this cluster; specialist DEFINITION CONTAINS work-unit kind DEFINITIONs per `arch/specialist-skill.md` §10; cross-primitive composition within cluster per §3 (always-present asymmetry + cardinality asymmetry + ad-hoc work first-class + snapshot pattern + cross-specialist composition) |
| **Pattern C primitives** (practitioner) | workflow_instance bound_practitioner_id references practitioner-RECORD per `arch/practitioner.md` §4 R-CC-10; per-shape multi-practitioner workflow_instance flexibility per `arch/practitioner.md` §8 | work-unit instance attribution composes through practitioner-RECORD per `glossary/work-unit.md` composes-with practitioner row; multi-practitioner work-unit authorship per `arch/practitioner.md` §8 |
