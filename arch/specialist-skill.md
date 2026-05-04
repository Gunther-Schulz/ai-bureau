---
title: Specialist + skill
topic-cluster: primitive-cluster (#1 of 4)
status: locked
---

# Specialist + skill

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the specialist + skill primitive cluster (the bundled-expertise unit + its atomic work-logic units). Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the SpecialistDescriptor + SkillDescriptor Pydantic schemas (Mode 3). Foundation-up dependency: specialist DEFINITION is the container for workflow + work-unit Pattern B nesting (per `glossary/specialist.md` composes-with rows); locking specialist-skill first means the future Phase 3.5 `arch/workflow-work-unit.md` topic locks against an already-validated container.

## 1. Topic scope + frontmatter

**Cluster identity**: specialist + skill — the codified-expertise primitive cluster. Specialist is the cohesion abstraction (bundle); skill is the atomic work-logic unit within. Both PRIMITIVES per locked GLOSSARY entries.

**Primitives covered**:
- `specialist` — bipartite Pattern B (DEFINITION at Framework C; INSTANCE-CONTENT at Owner B); the distributable expertise bundle
- `skill` — single-aspect cross-cutting; atomic work-logic unit within a specialist; loading semantics substrate-defined per substrate Pattern A Surface §G

**Cross-axis claim**: specialists support any axis through their bundled skills + entities + adapters (per `glossary/specialist.md`). Skills serve any axis depending on what work they encode (per `glossary/skill.md`). The cluster is cross-axis at primitive level; per-skill axis-membership is encoding-determined.

**Cardinality at cluster level** (per-primitive detail in §5):
- N specialists per workspace (activated via `workspace.md` `specialists_active` field)
- N skills per specialist (atomic work-logic units bundled within)

**Cluster boundary**: this topic locks the CONTAINMENT relationship between specialist + skill, the bundle structure, the atomicity tests, the activation + re-binding semantics, and the cross-specialist composition mechanics. It does NOT lock workflow or work-unit structural mechanics (Phase 3.5 `arch/workflow-work-unit.md` topic) or claim mechanics (Phase 3.5 `arch/claim-defensibility.md` topic) — those compose with this cluster's primitives but live in their own topics.

**Composition with framework**:
- Specialist DEFINITION lives at `Framework C scope` as distributable bundle; specialist INSTANCE-CONTENT lives at `Owner B scope`
- Skills live within specialist's bundle (cross-cutting layer; manifest at whatever scope the containing specialist manifests at)
- Pattern B classification per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern B row (specialist) + cross-cutting layer per locked GLOSSARY (skill)
- Substrate Surface §G translates substrate-neutral SpecialistDescriptor into substrate-native form at boot-time; skill loading semantics are substrate-defined per Pattern A
- Audit mechanism class records skill emissions with `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface

**Phase routing**: SpecialistDescriptor + SkillDescriptor Pydantic schemas → Phase 6 spec (Mode 3). Per-app-skill / per-specialist concrete authoring → workspace deployment (NOT this repo per `MAINTENANCE.md` TOP-LEVEL SCOPE app-skills-don't-live-here). This topic locks the architectural shape; Phase 6 locks typed contracts.

## 2. Per-primitive structural overview

### 2.1 Specialist (bipartite Pattern B)

Per locked GLOSSARY `specialist` entry: a composable bundle of codified expertise — skills + entities + memory + adapters — distributable as a unit. Bipartite: DEFINITION at Framework C (the distributable bundle); INSTANCE-CONTENT at Owner B (entities owned by the deployed specialist instance). NOT Pattern A — a specialist has no multiple interchangeable implementations; it IS its definition.

**DEFINITION aspect** (Framework C):
- Manifest (`specialist.md`) carrying frontmatter schema (per §2.3 below)
- Bundled skills (one or more skill files; per §2.2 atomicity)
- Bundled work-unit KIND DEFINITIONs (per `glossary/specialist.md` composes-with work-unit row; full mechanics → Phase 3.5 `arch/workflow-work-unit.md` topic)
- Bundled workflow DEFINITIONs (per `glossary/specialist.md` composes-with workflow row; full mechanics → same topic)
- Entity-kind DEFINITIONs (entities the deployed specialist instance owns at Owner B — e.g., bausteine kind / specialist-specific reference kinds)
- Memory namespace declaration (per-specialist memory partition at Owner B)
- Adapter implementation declarations (specialists may bundle adapters per `glossary/adapter.md` + `glossary/specialist.md` composes-with adapter row)

**INSTANCE-CONTENT aspect** (Owner B):
- Entities owned by the deployed specialist instance (bausteine instances; per-kind entity instances; specialist-scoped memory entries)
- Persists across activation/deactivation cycles per `glossary/specialist.md` (deactivating a specialist preserves accumulated content)
- Destruction semantics on workspace dissolution → §13 below

### 2.2 Skill (single-aspect cross-cutting)

Per locked GLOSSARY `skill` entry: an atomic unit of work logic within a specialist — a behavioral procedure invoked when its trigger conditions match. Loading semantics (auto-load / explicit-load / lazy-load) are substrate-defined per Pattern A; substrate Surface §G governs materialization. Skills are the smallest composable unit of codified expertise; specialists bundle multiple skills into a distributable expertise package.

**Skill atomic structure** (architectural-level):
- **Trigger frontmatter** — declares activation conditions (when this skill fires); substrate-defined keyword conventions (e.g., `name` / `description` / `when_to_use` / `version`)
- **Body content** — markdown procedural content the AI runtime reads at activation; Mode 1 production-runtime markdown per `ARCHITECTURE.md` §6 Logic placement modes
- **Optional output schema** — Pydantic schema (per `glossary/skill.md`) when skill produces structured output; composes with substrate Surface §D structured output validation

**Skill-loading-via-substrate Surface §G integration**: skills written against substrate-neutral SpecialistDescriptor work on any substrate impl; per-substrate materialization (Claude Agent SDK = Anthropic plugin manifest with auto-loaded SKILL.md; MS AF = module spec with Agent Skills SKILL.md format; hand-rolled = per-impl-decision) is impl-internal. Substrate-coupling impossible-by-construction per substrate §6 reconciliation.

**Skill emission attribution**: skill emissions record `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface (per `glossary/authority-binding.md` per-event actor declaration). The enum value is `ai_runtime` not `skill` — naming-collision prevention noted in `glossary/skill.md` (skill is the primitive; ai_runtime is the actor_kind value to avoid two distinct meanings of the same word).

**Specialist-skill structural boundary**: skill canNOT exist standalone outside specialist context (PBS architectural commitment per `glossary/skill.md` "specialist-as-skill-bundle constraint"; differs from Anthropic bare-skill plugin convention where skills can exist standalone in `plugin/skills/`). Phase 6 reconciles which convention applies to PBS app-skill rebuild — see W3 watch-list.

### 2.3 Specialist DEFINITION manifest schema (Framework C bundle structure)

Specialist DEFINITION = directory-bundle with this structure:

```
<specialist-name>/
  specialist.md          # manifest with frontmatter (schema below)
  skills/                # directory of skill files
    <skill-name>.md      # one skill per file
  entities/              # entity-md DEFINITIONs (kinds owned by deployed instance at Owner B)
  memory/                # memory namespace declaration
  adapters/              # adapter implementation declarations bundled with this specialist (if any)
  workflows/             # workflow DEFINITIONs (per Phase 3.5 workflow-work-unit topic)
  work-unit-kinds/       # work-unit KIND DEFINITIONs (per Phase 3.5 workflow-work-unit topic)
```

**Frontmatter manifest schema** (architectural-level enumeration; Phase 6 lands Pydantic shape):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | str | required | Specialist identifier; namespace root for KIND + workflow disambiguation per §10 specialist-namespace |
| `version` | semver | required | Specialist version (semver: major / minor / patch per §5 lifecycle) |
| `axis_claim` | enum | required | `axis-1` \| `axis-2` \| `axis-3` \| `cross-axis` — which axis this specialist primarily serves |
| `tier` | enum | required | `domain-anchored` \| `cross-archetype` per §9 two-tier classification |
| `activation_prereqs` | list | optional | Substrate-class-pinned (substrate impl id list) + adapter-bindings (required adapter classes + min-version) + other-specialists (specialist names + min-version) |
| `license` | str | optional | SPDX identifier (e.g., `Apache-2.0` / `MIT` / proprietary marker) — load-bearing for G Composability Gate consumption modes (OSS / marketplace) |
| `shape_compatibility` | list | required | `practitioner-shape` \| `autonomous-business-shape` \| `personal-OS-shape` \| `cross-shape` — per `profiles/G-composability-gate.md` cross-shape consumption framing |
| `capability_declarations` | object | required | Skills count + entity-kinds list + workflow-definitions list + work-unit-kinds list + shape-policy-conformance assertions (per-shape mandate-fulfilment claims, e.g., "satisfies practitioner-shape claim-level audit-emission") |

The manifest is the contract between the specialist DEFINITION (what the bundle PROVIDES) + the workspace (what the deployment NEEDS via `specialists_active`). Substrate Surface §G validates the manifest at workspace boot per substrate §10 boot step 6.

## 3. Cross-primitive composition within the cluster

Specialist + skill compose as container + atomic-unit (per §2). Composition mechanics:

**Specialist contains skills**: bundle structure per §2.3; skill files live under `skills/` subdirectory of specialist bundle; specialist DEFINITION manifest's `capability_declarations.skills` enumerates them.

**Skill identity within specialist**: skill identifier is `<specialist-name>:<skill-name>` (specialist-namespace per §10) — skill name within bundle is local; cross-specialist references use fully-qualified form.

**Skill activation context**: a skill's runtime context is provided by its containing specialist — dependencies (entity-kinds the skill writes to; adapters the skill invokes; memory namespace it reads from) resolve through the containing specialist's bundle. This is what makes the specialist-as-skill-bundle constraint structural (per §2.2): a skill outside specialist context has no resolved dependencies.

**Skill-to-skill composition within specialist**: skills within a specialist may invoke other skills within the same specialist by local name. Substrate-defined invocation mechanics per Pattern A; architectural commitment is the within-specialist invocation IS supported.

**Skill output composition**: skills with declared output schemas (Pydantic per substrate Surface §D) compose into specialist-level pipelines — one skill's structured output may be another skill's input. Per-pipeline mechanics → Phase 6.

## 4. Composition with framework primitives outside the cluster

| Primitive | Composition |
|---|---|
| `framework` | Specialist + skill are framework primitives (one PRIMITIVE / one PRIMITIVE) within `framework`'s primitive set |
| `mechanism` | Skills USE framework mechanisms (audit emission; source-grounding; sparring) at runtime via the substrate |
| `substrate` | Substrate Surface §G translates SpecialistDescriptor → substrate-native form at boot; substrate Surface §C permission flow consumed by skills before authority-bound operations; substrate Surface §D structured output validation consumed by skills with declared output schemas; substrate Surface §F session/context management persists skill-emitted state across sessions |
| `Framework C scope` | Specialist DEFINITIONs live there as distributable bundles |
| `Owner B scope` | Specialist INSTANCE-CONTENT (entities owned by the deployed specialist instance) lives there |
| `workspace` | Workspace activates specialists per `workspace.md` `specialists_active` field; `specialists_active` change triggers activation/deactivation per §5 lifecycle |
| `shape` | Per-shape policy may mandate certain specialists (e.g., practitioner-shape may mandate sparring-supporting specialists) or constrain what's permitted; `shape_compatibility` manifest field declares specialist-side shape applicability per per-shape G consumption |
| `adapter` | Specialists may bundle adapter implementations (per `glossary/specialist.md` composes-with adapter row); skills invoke adapters at runtime via per-class Surfaces (per `arch/adapter.md` §2) |
| `audit` (mechanism class) | Skills emit AuditEvents via skill-side MCP audit gate (per `arch/audit.md` §A emission API + `arch/substrate.md` §8 dual-emission); specialist activation emits audit events per §7 specialist-lifecycle event-kind catalog |
| `authority-binding` (mechanism) | Skill emissions record `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface; specialist activation events record activating actor (workspace-runtime activator) per same mechanism |
| `event` | Specialist + skill activation/deactivation/emission lifecycle generates events per §7 catalog; events flow through audit Surface |
| `claim` | Skills produce claims (claim_made events) during work execution; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain. Full claim mechanics → Phase 3.5 `arch/claim-defensibility.md` topic |
| `workflow` | Workflow DEFINITIONs live within specialist bundle (per `glossary/workflow.md` composes-with specialist row); workflow_instances reference skills by name (composition direction: workflow → skill). Full workflow mechanics → Phase 3.5 `arch/workflow-work-unit.md` topic |
| `work-unit` | Specialists DEFINE work-unit kinds at DEFINITION aspect (per `glossary/work-unit.md` composes-with specialist row); work-unit instances at Owner B owned by the deployed specialist instance per Pattern B nesting (§5 below). Full work-unit mechanics → Phase 3.5 `arch/workflow-work-unit.md` topic |
| `practitioner` | Practitioners author specialist DEFINITIONs (L1 producer profile); practitioner-shape workspaces activate specialists per shape policy. Full practitioner mechanics → Phase 3.5 `arch/practitioner.md` topic |

## 5. Cardinality + lifecycle (per primitive)

### Specialist cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Specialist DEFINITIONs per Framework C catalog | N | Multiple distributable definitions; immutable per version |
| Specialist instances per workspace | N | Bounded by `workspace.md` `specialists_active` list; per-shape policy may declare maximum (e.g., autonomous-business-shape may cap on capability surface) |
| Skills per specialist | N | Each specialist DEFINITION declares its skill set in `capability_declarations.skills` |
| Workflow DEFINITIONs per specialist | N | Each specialist DEFINITION declares its workflow definitions (Phase 3.5 detail) |
| Work-unit KIND DEFINITIONs per specialist | N | Each specialist DEFINITION declares its kinds (Phase 3.5 detail) |

### Specialist lifecycle

**DEFINITION lifecycle** (Framework C):
- **Creator**: L1 specialist creator (per `profiles/L1-specialist-creator.md`); domain expert who packages bundle
- **Owner**: Framework C catalog (distributable artifact)
- **Versioning**: semver — major (breaking changes to skill set / entity-kinds / workflow definitions / manifest schema), minor (new capabilities; backward-compatible), patch (content fixes; no API change)
- **Distributable forms**: consulting deliverable / internal firm reuse / OSS / future marketplace / backup-migration per `profiles/G-composability-gate.md` 5-mode framing
- **Immutability per version**: a specialist version is immutable once published; changes require version bump

**INSTANCE-CONTENT lifecycle** (Owner B):
- **Creator**: workspace runtime at specialist activation (entity-kinds become available; bausteine namespace opens)
- **Owner**: Owner B scope (workspace-bound)
- **Persistence across activation cycles**: deactivating a specialist preserves its accumulated INSTANCE-CONTENT (per `glossary/specialist.md` — practitioner work preserved across reactivation cycles)
- **Destructor**: workspace dissolution per §13 destruction semantics

**Mid-session re-binding (hot-activation)**: per `profiles/L5a-planner-pbs-schulz.md` lines 69-73 "Capability extension mid-flight" — practitioner activates specialist mid-project → new skills become available → resumes work. Architectural commitment:
1. `specialists_active` change is a workspace-scope event (orthogonal to active workflow_instance state)
2. New specialist activation invokes substrate Surface §G re-registration (substrate-native materialization mid-session)
3. In-flight workflow_instances NOT disrupted (workflow_instance state independent of specialist set changes; per `glossary/workflow.md` "workflow_instance doesn't gate capability changes")
4. New skills become available immediately to subsequent skill-firings within the workspace
5. Lifecycle event `specialist_activated` emitted per §7 catalog with activating actor binding

### Skill cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Skills per specialist | N | Each specialist DEFINITION declares its skill set |
| Skill INSTANCEs per workspace | N/A | Skills are stateless within a single firing; runtime context comes from containing specialist + workspace state |
| Skill firings per session | N | Each skill activation is one firing event; substrate Surface §G governs trigger evaluation |

### Skill lifecycle

- **Creator**: bundled within specialist DEFINITION (skills don't have independent author/version beyond their containing specialist)
- **Versioning**: skills inherit specialist version; no per-skill semver
- **Loading**: substrate-defined per Pattern A (auto-load / explicit-load / lazy-load); registered at substrate boot per substrate §10 step 6 specialist registration
- **Activation**: trigger condition match → substrate dispatches skill → skill body executes via AI runtime → optional structured output validated via substrate Surface §D
- **Emission**: skill firing emits skill-side events via MCP audit gate per `arch/substrate.md` §8 dual-emission (`actor_kind: ai_runtime` + skill identifier per authority-binding)
- **Termination**: skill firings are bounded (per substrate Surface §A run-with-max-turns); unbounded skills are an architectural anti-pattern

## 6. Logic placement mode

Per `ARCHITECTURE.md` §6 Logic placement modes:
- **Specialist DEFINITION manifest** (`specialist.md` frontmatter + capability declarations): Mode 1 production-runtime LLM-MD (workspace AI reads at activation time)
- **Skill body content** (`skills/<name>.md` markdown): Mode 1 production-runtime LLM-MD (AI runtime reads at activation; this is the canonical Mode 1 example per `ARCHITECTURE.md` §6 Mode 1 row)
- **Skill output schemas** (Pydantic): Mode 2 production-runtime Python (substrate Surface §D structured output validation)
- **SpecialistDescriptor + SkillDescriptor Pydantic shapes** (Phase 6 spec): Mode 3 hybrid spec layer
- **THIS topic + DR + GLOSSARY entries**: Mode 4 development-time documentation (NOT production-runtime)

Primitive-cluster topics are Mode 4 development-time documentation — articulating the architectural shape framework developers need to understand, not what production AI loads at runtime. Production AI in a deployed PBS workspace loads Mode 1 markdown (skill SKILL.md files; specialist manifests; workspace.md; shape policy bundles); this topic is for framework-developer orientation.

**LLM-instruction tightness asymmetry** (per `ARCHITECTURE.md` §6 cross-cutting principles): Mode 1 markdown (specialist manifests; skill bodies) requires the highest LLM-instruction tightness review effort because LLMs paper over imprecise markdown by inference. Phase 6 app-skill authoring + per-deployment specialist authoring inherit this discipline.

## 7. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns.

### Specialist-error categories (architectural-level)

Per-shape error escalation policy lives in §8 Cross-shape policy variation; the categories themselves are framework-level:

| Category | Architectural meaning |
|---|---|
| `SpecialistManifestValidation` | Manifest frontmatter fails schema validation (missing required fields; invalid enum values; semver malformed) |
| `SpecialistSkillLoadFailure` | Skill loading fails at substrate registration (substrate Surface §G error; skill file unparseable; substrate-defined trigger conventions violated) |
| `SpecialistEntityKindConflict` | Specialist's entity-kind DEFINITION collides with already-registered kind from another active specialist (resolved via specialist-namespace per §10) |
| `SpecialistCrossDependencyUnmet` | Specialist activation requires another specialist (per `activation_prereqs.other-specialists`) that isn't activated; workspace boot fails OR mid-session activation rejected |
| `SpecialistAdapterDependencyUnmet` | Specialist requires adapter binding (per `activation_prereqs.adapter-bindings`) that isn't in workspace.md adapter bindings list |
| `SpecialistSubstrateClassPinViolation` | Specialist declares substrate-impl pin (per `activation_prereqs.substrate-class-pinned`) incompatible with selected substrate |

### Specialist-lifecycle event-kind catalog (architectural-level)

Substrate emits AuditEvents at specialist lifecycle moments. Event kinds (architectural enumeration; per-event-shape Pydantic schema → Phase 6):

- `specialist_activated` — `specialists_active` set acquired this specialist; substrate Surface §G registered it; new skills available
- `specialist_deactivated` — `specialists_active` set released this specialist; INSTANCE-CONTENT preserved per persistence rule
- `specialist_skill_registered` — individual skill within specialist became substrate-registered (per substrate Surface §G materialization)
- `specialist_load_failed` — manifest validation OR skill load OR dependency check failed; specialist NOT activated; failure category per §7 error categories
- `specialist_version_bumped` — workspace observed specialist version change (e.g., re-deployment with newer specialist version); cross-version compatibility check fired

Specialist-lifecycle events compose with substrate §10 boot/shutdown sequence at substrate-phase 4 (specialist registration step) per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection — specialist registration ordering integrates with the canonical composite sequence.

### Other operational concerns (Phase 6)

- **Skill trigger evaluation mechanics**: per-substrate trigger-keyword convention; trigger-match disambiguation when multiple skills match
- **Skill output retry semantics**: substrate Surface §D auto-retry behavior on schema validation fail; max-retry per skill OR specialist
- **Specialist hot-deactivation mid-flight**: deactivating a specialist with active skill firings — drain-then-deactivate vs immediate-stop; per-shape policy
- **Cross-specialist namespace conflicts**: when same skill-name appears in multiple specialists, fully-qualified-reference is canonical; per-substrate dispatch mechanics for the resolution
- **Specialist activation ordering**: when `specialists_active` declares multiple specialists with cross-dependencies, activation ordering per dependency graph
- **Specialist update semantics during active workflow_instances**: workflow_instance defined against specialist v1.0; specialist updates to v1.1 mid-session — workflow_instance behavior (snapshot to v1.0 def vs adopt v1.1) per per-shape + per-specialist policy
- **Skill output streaming**: skills with long-running output; streaming vs buffered emission via substrate

## 8. Cross-shape policy variation (cluster-conditional; PARTIALLY APPLIES)

Per Pattern A template `MAINTENANCE.md` Layer 3 §14 conditional precedent + `arch/adapter.md` §14 cross-shape policy variation precedent: this section applies when primitive behavior is shape-policy-mediated. Specialist + skill primitives are PARTIALLY shape-policy-mediated.

**What is shape-uniform** (NOT shape-policy-mediated):
- Specialist DEFINITION manifest schema (Framework C; same across all shapes)
- Skill atomic structure (trigger frontmatter + body content + optional output schema; same across all shapes)
- Specialist-skill bundle structure (same directory layout)
- Specialist-namespace mechanics (same naming convention)
- Specialist-skill structural boundary (skill-as-bundled-within-specialist; same architectural commitment)

**What is shape-policy-mediated**:

| Dimension | practitioner-shape | autonomous-business-shape | personal-OS-shape |
|---|---|---|---|
| **Specialist activation policy** | Practitioner-judgment per session; specialist activation logged per audit | Programmatic activation per business policy; budget-aware capacity surface | User-preference per session; lightweight |
| **Per-skill-firing audit granularity** | Claim-level mandatory (per `arch/audit.md` §14 practitioner-shape granularity) | Action-level (per `arch/audit.md` §14 autonomous-business granularity) | Light (per `arch/audit.md` §14 personal-OS granularity) |
| **Specialist-error escalation** (per §7 categories) | Fail-closed (defensibility-critical; specialist load failures must surface to practitioner; no silent degradation) | Fail-open with alert (continuity prioritized; alert + fallback to remaining active specialists) | Fail-open (lightweight; degradation acceptable) |
| **Skill output validation strictness** | Strict (per axis-3 defensibility; structured output validation auto-retry exhaustion fails-closed) | Tolerant (per business-continuity; may fall through to unstructured emission) | Tolerant |
| **Specialist version-bump mid-session policy** | Snapshot to active version (preserves audit-trail integrity for active workflow_instances per defensibility); explicit re-deployment to adopt new version | May adopt new version mid-session per business policy | Adopt latest per user preference |
| **Cross-specialist write boundary** | Strict prohibition (entity ownership boundary structural per §10 cross-specialist composition rules) | Strict prohibition (same architectural commitment) | Strict prohibition (same architectural commitment) |

Specialist + skill DEFINITIONs themselves stay shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (framework primitives stay shape-neutral / archetype-neutral / pioneer-neutral). The `shape_compatibility` manifest field (per §2.3) declares specialist-side shape applicability; per-shape policy interprets specialist activation + per-skill emission semantics per shape's mandate. Shape policy declares per-shape specialist + skill enforcement at workspace boot.

## 9. Granularity tests (cluster-conditional; APPLIES)

Per primitive-cluster topic template, granularity tests apply when primitives have granularity discriminators. Both specialist + skill have load-bearing granularity discriminators per `glossary/specialist.md` boundary tests + Phase 3.5 BACKLOG specialist + skill granularity 3-tests.

### Specialist granularity 3-test

When considering "should this be ONE specialist or split into multiple?" / "should these capabilities be merged into existing specialist?" — apply all three:

1. **Cohesion** — do these skills + entities serve ONE defined competence area? (If competences are heterogeneous, candidate for split into multiple specialists.)
2. **Distributability** — could this bundle deploy to a workspace standalone (without other specialists) and still function? (If activation strictly requires another specialist's content, candidate for merge OR explicit `activation_prereqs.other-specialists` declaration.)
3. **Reusability** — could ≥2 distinct workspace archetypes activate this specialist productively? (If only one archetype could ever use it, that's `tier: domain-anchored`; if multiple, that's `tier: cross-archetype` per §9 two-tier classification below.)

A specialist passing all three is well-shaped. A specialist failing one is a candidate for restructure (split / merge / re-classify).

### Skill granularity 3-test

When considering "should this be ONE skill or split into multiple?" / "should these be merged into one skill?" — apply all three:

1. **Atomicity** — single trigger condition? (Multiple trigger conditions for genuinely distinct work logic = candidate for split. Per `glossary/skill.md` skills are atomic units.)
2. **Specialist-coherence** — does this skill belong to ONE specialist's competence area? (Skills serving multiple specialists' competences are mis-bundled; candidate for re-assignment OR cross-specialist invocation per §10.)
3. **Reusability-within-specialist** — invoked from ≥2 contexts within the specialist's workflows? (Single-use skills bundled separately may be over-decomposed; candidate for inline-into-workflow-step. Skills used across multiple workflows within the specialist = well-shaped atomic unit.)

A skill passing all three is well-shaped. A skill failing one is a candidate for restructure (merge / re-assign / inline).

### Two-tier specialist classification

Specialists classify into two tiers per `glossary/specialist.md` cross-archetype illustration. Tier declared in manifest `tier` field per §2.3:

| Tier | Definition | Example specialists |
|---|---|---|
| **`domain-anchored`** | Specialist serves one archetype's domain primarily; not naturally reusable across archetypes | `planning-document-work` (PBS-Schulz; B-Plan-Begründung); `legal-research` (legal practice); `naturschutz-specialist` (planning archetype FFH-VP) |
| **`cross-archetype`** | Specialist usable across ≥2 distinct workspace archetypes productively | `citation-verification` (legal + research + planning); `project-management` (cross-archetype business); `invoicing` (cross-archetype business with adapter); `brand-voice` (cross-archetype creative) |

Tier classification informs distribution + activation policy: `cross-archetype` specialists are higher-leverage (reusable across more deployments); `domain-anchored` specialists serve deeper specialization. Workspaces typically activate a mix (PBS-Schulz pioneer activates `planning-document-work + project-management + invoicing` per `profiles/L5a-planner-pbs-schulz.md` lines 76-83 — domain-anchored + 2 cross-archetype).

## 10. Bundle composition (cluster-conditional; APPLIES)

Specialist BUNDLES other artifacts (skills + entity-kind DEFINITIONs + workflow DEFINITIONs + work-unit KIND DEFINITIONs + adapter implementations + memory namespace declaration). This section locks the bundle composition mechanics + cross-specialist composition rules.

### Specialist-namespace (naming + collision prevention)

**Specialist-namespace** = specialist-name (per manifest `name` field). Prevents cross-specialist naming collision for KIND + workflow-name + skill-name + entity-kind:
- `legal-research:matter` (work-unit kind in legal-research specialist) is distinct from `planning-document-work:project` (work-unit kind in planning-document-work specialist)
- `planning-document-work:save-baustein` (skill in planning-document-work) is distinct from `legal-research:save-baustein` (hypothetical skill in legal-research)
- Cross-specialist references use fully-qualified `specialist-name:identifier` form

The specialist-namespace is anchored to the existing locked specialist primitive (specialist `name` field) rather than introducing kind-vs-specialist namespace ambiguity (e.g., a separate "kind-namespace" abstraction that would require its own primitive).

### Cross-specialist composition rules

When a workspace has multiple active specialists, cross-specialist composition is governed by:

| Composition direction | Permitted? | Mechanism |
|---|---|---|
| Skill in specialist-A invokes skill in specialist-B | YES | Fully-qualified reference: `specialist-B:skill-name`; substrate Surface §G dispatches across specialists |
| Specialist-A's skill READS specialist-B's entity instance | YES | Cross-specialist entity reads permitted at framework level (audit-trail records cross-specialist read with both specialist identifiers) |
| Specialist-A's skill WRITES specialist-B's entity instance | NO | Cross-specialist entity writes prohibited at framework level — entity ownership boundary structural per Pattern B (entities owned by deployed specialist instance live at Owner B per that specialist's namespace) |
| Specialist-A's workflow invokes specialist-B's workflow | YES (via skill composition) | Workflow → skill invocation; cross-specialist via fully-qualified skill reference (full mechanics → Phase 3.5 `arch/workflow-work-unit.md`) |
| Specialist-A's work-unit kind referenced from specialist-B | NO | Work-unit kinds are specialist-defined; cross-specialist work-unit creation is mis-shaped (each work-unit instance is owned by its defining specialist's namespace) |

Per-shape policy may further restrict cross-specialist composition (e.g., autonomous-business-shape may restrict to declared cross-specialist invocation lists for budget-control). Framework baseline = above table; per-shape tightening = additive.

### Bundle-level audit emission

Specialist bundle composition events flow through audit Surface:
- Bundle activation emits `specialist_activated` per §7
- Per-skill registration emits `specialist_skill_registered` per §7
- Cross-specialist invocation emits skill-firing events with both specialist identifiers per authority-binding chain

## 11. Marketplace + distribution mechanics (cluster-conditional; APPLIES — partially deferred)

Specialist is canonical distributable unit per `glossary/specialist.md` ("marketplace distribution per archived ROADMAP v3 treats specialists as the canonical distributable unit") + `profiles/L5a-planner-pbs-schulz.md` (pioneer activates `planning-document-work + project-management + invoicing` — multiple specialists per workspace illustrating distribution shape) + `profiles/G-composability-gate.md` (5-mode consumption framing: consulting / firm reuse / OSS / marketplace future-conditional / backup-migration). This section locks the SHAPE of specialist distribution; per-shape publication / versioning / dependency / supersession mechanics are D-Gate-deferred per §14 W1 watch-list (awaiting second-deployment OR shape-catalog-curator activity per L9 profile).

### Distribution shape (architectural-level)

**Specialist as distributable artifact**:
- Self-contained bundle per §2.3 directory structure
- License declared via manifest `license` field (SPDX identifier) per §2.3
- Provenance + signing → W4 watch-list (Phase 5/6+ tooling territory; specialist signing for OSS + marketplace anti-spoofing)
- Versioning per semver per §5 specialist lifecycle
- Self-containment validated per L1 producer profile packaging boundary (per `profiles/L1-specialist-creator.md` lines 18-23 specialist self-containment + DEFINITION boundary)
- Cross-substrate compatibility declared via manifest `activation_prereqs.substrate-class-pinned` per §2.3 (substrate-agnostic if list empty; substrate-pinned if listed)
- Cross-shape compatibility declared via manifest `shape_compatibility` per §2.3

**5-mode consumption (per `profiles/G-composability-gate.md`)**:
- **Consulting deliverable mode**: consultant builds specialist for client; signed handoff; license-bound use; update path
- **Internal firm reuse mode**: firm IT distributes shared specialist set across practitioners; per-office customization via Layer A; multi-tenant governance
- **OSS / community distribution mode**: domain expert publishes open-source specialist on community ecosystem; license-compatibility composes with framework license
- **Marketplace mode (FUTURE-CONDITIONAL per W1)**: paid specialist distribution; revenue tracking; quality / review / rating; signing / provenance per W4
- **Backup / migration / cloning mode**: workspace serialization includes activated specialist set + INSTANCE-CONTENT; cross-substrate restore preserves specialist semantics where substrate-agnostic; substrate-pinned specialists may require substrate match

### Per-shape distribution policy

| Shape | Distribution applicability |
|---|---|
| **practitioner-shape** | Heavy specialist activation typical (multiple domain-anchored + cross-archetype); strict version snapshot per defensibility |
| **autonomous-business-shape** | Capability-budgeted activation per business policy; specialist set may be smaller |
| **personal-OS-shape** | Light activation per user preference; cross-archetype specialists favored |

### Per-shape mechanics deferred to W1

Per `decision-design-sharpening` D Gate procedure (per `profiles/INDEX.md`): mental modeling can frame the SHAPE — specialist as canonical distributable unit per locked GLOSSARY + L5a + G profiles — but per-shape publication / versioning compatibility / dependency resolution / supersession mechanics need second-deployment surface friction signal before locking. Per-shape mechanics are `BACKLOG.md` Phase 5 ROADMAP entry per W1 watch-list.

## 12. Cross-references reservation

Cross-references for this topic are consolidated in §17 below per Pattern A template convention; this section number reserved for parity with substrate's §12 (Transport variation, N/A here per §13 below).

## 13. Per-primitive lifecycle ordering (cluster-conditional; APPLIES)

Specialist activation cycles via `workspace.md` mid-session re-binding (per §5 specialist lifecycle hot-activation) make this section load-bearing. Lifecycle ordering integrates with substrate boot/shutdown phases per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection.

### Boot-time specialist activation ordering

Per `ARCHITECTURE.md` §6 composite boot subsection substrate-phase 4 (specialist registration), within that step specialist activation orders as:

1. Per `workspace.md` `specialists_active` declaration order, iterate specialist set
2. For each specialist: parse manifest; validate frontmatter schema (`SpecialistManifestValidation` error if fail per §7)
3. Resolve `activation_prereqs`:
   - `substrate-class-pinned`: verify substrate impl in pin list (`SpecialistSubstrateClassPinViolation` if fail per §7)
   - `adapter-bindings`: verify adapter bindings present in `workspace.md` (`SpecialistAdapterDependencyUnmet` if fail per §7)
   - `other-specialists`: verify specialists in dependency list activated earlier in iteration (`SpecialistCrossDependencyUnmet` if fail per §7)
4. Substrate Surface §G translates SpecialistDescriptor → substrate-native form
5. Per-skill registration (`specialist_skill_registered` per §7)
6. Entity-kind registration (collision check; `SpecialistEntityKindConflict` if fail per §7; resolved via specialist-namespace per §10)
7. Memory namespace open
8. Adapter implementation declarations bind (if any)
9. Workflow + work-unit-kind DEFINITIONs registered (Phase 3.5 detail per `arch/workflow-work-unit.md`)
10. Emit `specialist_activated` event per §7
11. Per-shape policy applies activation policies (per §8 cross-shape policy variation)

### Mid-session activation ordering

Mid-session `specialists_active` change (hot-activation per §5) follows boot-time activation ordering steps 2-11 for newly-added specialists. Newly-deactivated specialists follow shutdown ordering below. In-flight workflow_instances NOT disrupted (per `glossary/workflow.md` capability changes orthogonal to workflow_instance state).

### Shutdown-time specialist deactivation ordering

Per `ARCHITECTURE.md` §6 composite shutdown subsection, specialist deactivation orders BEFORE adapter shutdown (specialists may use adapters; specialists release first):

1. Per `specialists_active` REVERSE declaration order, iterate specialist set
2. Per specialist: drain in-flight skill firings within this specialist
3. Stop accepting new skill activations for this specialist
4. Persist INSTANCE-CONTENT entities to Owner B per persistence rule (per §5 lifecycle persistence across activation cycles)
5. Substrate Surface §G de-registration (per-skill `specialist_skill_registered` reverse)
6. Adapter implementation releases (if specialist bundled adapters)
7. Emit `specialist_deactivated` event per §7

### Workspace dissolution (destruction semantics)

This topic LOCKS **archival as default** for specialist INSTANCE-CONTENT on workspace dissolution per `glossary/specialist.md` ("ARCH Layer 3 settles instance-content destruction semantics — deletion-with-audit vs archival; on workspace dissolution"):

- **Default**: archival preserves practitioner work + axis-3 authorship preservation + 6-months-later defensibility test favor
- **Opt-in**: deletion-with-audit policy declared at `workspace.md` level (workspace declares `instance_content_dissolution_policy: archive | delete-with-audit`)
- Per-shape policy may restrict the opt-in (practitioner-shape policy may prohibit deletion-with-audit per defensibility-critical concern)

Archival mechanics → Phase 6 (workspace serialization mechanics; archive format; restoration semantics).

## 14. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| **W1** | Marketplace publication mechanics | Second-deployment surface friction OR shape-catalog-curator activity (per `profiles/INDEX.md` L9 profile fleshing trigger) | Per-shape publication / versioning compatibility / dependency resolution / supersession mechanics design fires when concrete second-deployment evidence accumulates; `BACKLOG.md` Phase 5 ROADMAP entry |
| **W2** | Cross-substrate skill-portability | Second substrate deployment (MS AF or hand-rolled) with skills written against Claude Agent SDK substrate Surface §G mechanics | Re-validate skill loading semantics across substrates; surface per-substrate skill-portability discipline if friction emerges; per-substrate trigger-keyword convention reconciliation per `arch/substrate.md` §15 |
| **W3** | PBS specialist-as-skill-bundle constraint vs Anthropic bare-skill plugin convention reconciliation | Phase 6 app-skill rebuild begins (concrete authoring against substrate-native plugin format) | Reconciliation: PBS app-skill packaging convention adopts specialist-bundle constraint (per `glossary/skill.md` PBS architectural commitment) OR Anthropic bare-skill convention adopted with PBS-specific manifest layer; Phase 6 territory |
| **W4** | Specialist provenance + signing mechanism | OSS distribution friction surfaces (anti-spoofing concern with anonymous OSS specialists) OR marketplace mechanics design begins per W1 | Phase 5/6+ tooling design: specialist signing format; signature verification at install; chain-of-trust mechanics; integrates with manifest `license` field per §2.3 |

## 15. Decision-design provenance

Provenance for this topic lives in DR + HANDOFF + git log per `MAINTENANCE.md` Lens 5 v0.2.1 provenance hygiene + per `coherence-audit` Lens 5. See `docs/decisions/specialist-skill-arch-topic.md` for sharpening trajectory + Round 1 + Round 2 EXPANSIONS + manufactured-criticism rejections + GLOSSARY back-check verdict + profile-anchored validation cluster citations + Mode 2 composite decomposition rationale.

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: specialist + skill primitives stay shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz) reality (per `profiles/L5a-planner-pbs-schulz.md` lines 76-93 active specialists set + capability extension mid-flight) grounds the cluster primitives without leaking pioneer specifics into the framework definitions.

## 16. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.5 | LOCKED |
| SpecialistDescriptor + SkillDescriptor Pydantic schemas | 6 | Mode 3 spec; manifest schema typing per §2.3; SpecialistError class hierarchy per §7 |
| Per-app-skill / per-specialist concrete authoring | Workspace deployment (NOT this repo) | Per `MAINTENANCE.md` TOP-LEVEL SCOPE: app skills NEVER live in framework repo; build into deployed workspace (Phase 6 deployment) |
| Specialist signing + provenance mechanics | 5/6+ | Per W4 watch-list; tooling territory |
| Marketplace publication / versioning / supersession mechanics | 5+ | Per W1 watch-list; `BACKLOG.md` Phase 5 ROADMAP entry |
| Cross-specialist namespace dispatch implementation | 6 | Per-substrate dispatch mechanics; full-qualified-reference resolution |
| Specialist hot-activation in-flight semantics | 6 | Per §5 mid-session re-binding; pre-implementation sharpening at Phase 6 implementation-start |
| Workspace serialization / archival format | 6 | Per §13 workspace dissolution; archival mechanics |

## 17. Cross-references

- **GLOSSARY**: `specialist` (canonical entry); `skill` (canonical entry); `work-unit` (Pattern B nesting partner); `workflow` (Pattern B nesting partner); `authority-binding` (skill emission attribution); `actor` (`actor_kind: ai_runtime` for skill emissions); `framework`, `mechanism`, `Framework C scope`, `Owner B scope`, `workspace`, `shape`, `substrate`, `adapter`, `audit`, `event`, `claim`, `practitioner`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern B row (specialist) + Pattern A row (substrate composition); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (specialist-skill structural boundary; specialist-namespace prevents collision); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (pioneer-neutrality of specialist + skill); `MAINTENANCE.md` TOP-LEVEL SCOPE (app skills don't live in framework repo); `ARCHITECTURE.md` §6 cross-cutting principles "AI as runtime" + "LLM-instruction tightness for Mode 1 markdown layer" + "Workspace boot + shutdown composite sequence"; `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)
- **Profiles validated**: `G-composability-gate.md` (lines 22-34 consulting deliverable mode; lines 35-58 internal firm reuse mode; lines 60-92 OSS + marketplace modes; lines 94-104 backup/migration mode; lines 154-160 cross-substrate + cross-shape composition rules; lines 162-184 architectural concerns surfaced) + `L5a-planner-pbs-schulz.md` (lines 69-73 capability extension mid-flight; lines 76-83 active specialists set; lines 85-92 active substrate + adapters + Layer A scope; lines 119-129 stress-tests including capability extension mid-flight) + `L1-specialist-creator.md` (lines 18-29 specialist self-containment + DEFINITION boundary + skill granularity within specialist + workflow definition packaging + entity declarations + composability + versioning + license + cross-substrate + cross-shape compatibility — full intended-stress-test enumeration)
- **ARCH topics composing with specialist + skill**: `arch/substrate.md` (Surface §G specialist registration + §C permission flow + §D structured output + §F session/context management + §8 dual-emission); `arch/audit.md` (mechanism class; skill emissions via skill-side MCP gate per §A emission API; specialist-lifecycle event-kind catalog feeds audit-trail per §E event-kind catalog management); `arch/adapter.md` (specialists may bundle adapter implementations per `glossary/specialist.md` composes-with adapter row; specialist + adapter cross-composition per §3 framework-baseline-vs-shape-extension); `arch/sparring.md` (mechanism class peer; sub-mechanisms accessed by skills as framework mechanisms per §4 composition table); `arch/quality-gate.md` (Pattern A protocol Phase 3.6; consumes skill-firing observability + specialist-lifecycle events for cross-axis collapse-resistance); `arch/practitioner.md` (Phase 3.5 second primitive-cluster LOCKED; practitioner-record at Owner B; specialist DEFINITIONs authored by L1 practitioners; cross-specialist activation actor binding per `arch/practitioner.md` §4 composition table — when specialist activates mid-session per §5 mid-session re-binding above, the activating actor (workspace-runtime activator per §7 `specialist_activated` event-kind) is the practitioner-RECORD bound to current session per `arch/practitioner.md` §4 R-CC-9 cross-specialist activation actor binding row). `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster LOCKED; workflow + work-unit Pattern B nested within specialist DEFINITION at Framework C per cluster boundary; specialist DEFINES work-unit kinds + workflow definitions; cross-specialist composition rules per §10 + §3 apply to cross-specialist work-unit attachment per `arch/workflow-work-unit.md` §3 — cross-specialist work-unit READ permitted + ownership mutation PROHIBITED; workflow + work-unit kind DEFINITIONs registered at substrate-phase 4 step 9 per §13 boot integration). `arch/claim-defensibility.md` (Phase 3.5 fourth primitive-cluster LOCKED; skills produce claims (claim_made events) during work execution per §4 composition table claim row; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain — one of three architectural sub-aspects of authority-binding per `glossary/authority-binding.md`; specialist DEFINITIONs may declare per-specialist claim kinds per §18 composition table claim primitive row; per-skill claim-emission contract surfaces in skill DEFINITION authoring per L1 specialist creator profile validation). `arch/scope-model.md` (Phase 3.5 first cross-cutting integrator LOCKED — specialist DEFINITION as Framework C bundle nesting skill / workflow / work-unit-kind / adapter Implementations under specialist-namespace per §4 E2 nested-bundle pattern (specialist's Framework C bundle is the load-bearing nesting container; quad-closure across `glossary/specialist.md` + `glossary/skill.md` + `glossary/work-unit.md` + `glossary/workflow.md` per Note 56); specialist instance content at Owner B per §4 per-primitive composition table specialist row; skill atomic primitive nested in specialist's Framework C bundle per §4 E2 + per-skill events captured in audit-trail at workspace at Owner B per §18 composition table skill row)
- **Phase 6 spec target**: `docs/specs/specialist.md` (SpecialistDescriptor + manifest Pydantic schema); `docs/specs/skill.md` (SkillDescriptor Pydantic schema; trigger frontmatter conventions; output schema integration with substrate Surface §D)
- **Archived sources** (INPUT only per `disciplines/10-greenfield-evaluation.md` — archive citations name SOURCE where input came from, NOT TEMPLATE where structure transferred; each cited element greenfield-evaluated against current locked vocabulary): `archive/docs/decisions/terminology-and-specialist-primitive.md` (specialist-as-skill-bundle constraint origin); `archive/plugin/skills/` (per-specialist DEFINITION files reference patterns); `archive/docs/decisions/skill-expert-agent-and-domain-knowledge.md` (skill-frontmatter conventions reference)

## 18. Composition table

How specialist + skill compose with key framework primitives + Pattern A protocols + mechanism classes:

| Composing primitive | Specialist composition | Skill composition |
|---|---|---|
| **substrate Surface §G** (specialist registration) | SpecialistDescriptor materialized to substrate-native form at boot per substrate §10 step 6 + per §13 boot-time activation ordering above | Per-skill registration via substrate Surface §G; trigger-keyword convention per substrate; loading semantics (auto-load / explicit-load / lazy-load) substrate-defined per Pattern A |
| **substrate Surface §C** (permission flow) | Specialist activation may require permission per per-shape policy (e.g., practitioner-shape may prompt practitioner before activation in some workflows) | Skill firings request permission before authority-bound operations (write to entity / send via adapter / emit signed claim) |
| **substrate Surface §D** (structured output validation) | N/A at specialist level (specialist is a bundle, not an emission) | Skills with declared Pydantic output schemas have substrate auto-retry on validation fail |
| **audit mechanism class** | Specialist-lifecycle events per §7 (`specialist_activated` / `specialist_deactivated` / `specialist_skill_registered` / `specialist_load_failed` / `specialist_version_bumped`) flow through audit Surface §A emission | Skill firings emit events via skill-side MCP audit gate per `arch/substrate.md` §8 dual-emission; per-skill event catalog inherits from specialist's `capability_declarations` |
| **adapter** (Pattern A protocol) | Specialists may bundle adapter implementations per §2.1 DEFINITION aspect; specialist's `activation_prereqs.adapter-bindings` declares required adapter bindings | Skills invoke adapters at runtime via per-class Surfaces per `arch/adapter.md` §2 (e.g., draft-cover-mail invokes email-adapter; verify-citations invokes MCP-corpus-adapter) |
| **claim primitive** (Phase 3.5 `arch/claim-defensibility.md`) | Specialist DEFINITIONs may declare per-specialist claim kinds | Skills produce claims (claim_made events) during work execution; per-claim attribution composes through skill identifier → specialist → workspace per authority-binding chain |
| **authority-binding mechanism** | Specialist-lifecycle events record activating actor (workspace-runtime activator) | Skill emissions record `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface; chain of attribution composes into per-claim defensibility |
| **Pattern A protocols** (substrate / adapter / quality-gate) | Specialist composes with all Pattern A protocols via substrate Surface §G + adapter binding + quality-gate observability | Skills compose with Pattern A via runtime invocation through containing specialist |
| **Pattern B primitives** (workflow / work-unit) | Specialist DEFINITION CONTAINS workflow + work-unit-kind DEFINITIONs at Framework C; specialist instance OWNS workflow_instances + work-unit instances at Owner B per Pattern B nesting (Phase 3.5 `arch/workflow-work-unit.md` topic locks contained primitives' mechanics) | Skills are referenced BY workflow definitions (workflow → skill composition direction per `glossary/workflow.md`); skills participate in workflow_instance phase progression |
