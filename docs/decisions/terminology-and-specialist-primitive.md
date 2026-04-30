# Decision record: Terminology + Specialist primitive

**Status**: ACCEPTED (session 13, 2026-04-30)
**Owner**: ARCHITECTURE.md "Pattern-vs-instance discipline" + "Substrate-pluggability discipline" + plugin-conventions §<TBD> + ROADMAP commitment #22
**Sharpening metadata**: 3-round decision-design-sharpening (full monty + 2 user-triggered). ~26 refinements surfaced; ~85% expansions, ~15% revisions. Per-sub-DR sharpening rounds skipped post-decomposition (Round 3 covered integration surface; per-sub-DR rounds would yield diminishing returns + risk manufactured criticism per `feedback_refine_pareto.md`).
**Related**:
- `office-vs-department.md` (#12 — predecessor; this DR demotes department to optional grouping shape)
- `office-level-managed-entities.md` (#15 — predecessor; renamed to `workspace-scope-managed-entities.md`)
- `ai-as-runtime-hybrid-shape.md` (#16 — specialist.md + workspace.md adopt hybrid-shape contract)
- `skill-expert-agent-and-domain-knowledge.md` (#11 topic 1 — display_label survives at skill level; specialist is NEW primitive ABOVE skill, not skill rename)
- `substrate-agentic-framework.md` (#18) + `substrate-protocol-design.md` (SpecialistDescriptor Pydantic Protocol added to common surface)
- `governance-and-identity-sourcing.md` (specialist registration prose conventions)
- `positioning-three-tier-framework.md` (Sub-DR B — strategic implications downstream of this DR)

## Context

Pre-RAG queue commitment #22 surfaced as near-blocking for #9 implementation phase. Question: are "office / department / expert-practitioner" the right primary abstractions, or do they leak PBS-instance shape (planning bureau IS literally an office)?

Cross-domain stress test of current vocabulary across 10 archetypes (planning bureau, legal practice, accounting firm, solo expert, research project, creative practice, educational deployment, personal knowledge management, open-source maintainer collective, knowledge graph deployment): "office" metaphor fights ≥6/10 archetypes. Strong PBS-instance-anchor signal.

Per session-11 framework-foundation framing: PBS is the framework foundation for the consulting business; framework's consumers include hypothetical legal-practice / research-lab / consulting-client deployments opening tomorrow. Pre-RAG is the chronological window where renaming is essentially free per ARCH "Maintenance discipline."

## Decision

Three changes, locked together (deeply coupled):

| # | Change |
|---|---|
| 1 | Replace "Office" pattern primitive with **Workspace** |
| 2 | Introduce **Specialist** as new pattern primitive between Skill and Workspace |
| 3 | Demote **Department** from pattern primitive to optional `groupings:` shape (deployment-instance) |

Composes architecturally — without all three, the cascade is incoherent.

## 1. Office → Workspace

Top-level deployment scope renames from `Office` to `Workspace` at pattern primitive level. PBS-instance shape "office for planning bureau" becomes ONE workspace shape among many.

### Naming alternatives evaluated

| Candidate | Verdict | Reasoning |
|---|---|---|
| Office (status quo) | ❌ | Org-shape baggage; fails ≥6 cross-archetype stress tests; PBS-instance-anchor |
| **Workspace** | ✅ **chosen** | Software-ecosystem-aligned (VS Code, Slack, GitHub, Notion); generic across solo→team→org→creative→research→KG; functional ("where work happens") with minimal metaphor |
| Practice | ⚠ | Aligns with VISION's expert-practitioner BUT German Planungsbüro ≠ Praxis; doesn't fit creative or knowledge-graph cleanly |
| Studio | ⚠ | Imposes creative connotation; doesn't fit legal/research |
| Hub | ⚠ | Vague; doesn't suggest persistence/identity |
| Deployment | ⚠ | Pure engineering; loses ergonomic clarity |
| Context | ❌ | Collides with LLM context window |
| (unnamed) | ❌ | Cross-specialist scope still needs a name |

### Cross-archetype fit

| Archetype | Workspace name |
|---|---|
| Planning bureau | "PBS-Schulz workspace" |
| Solo creative writer | "Anna's Writing workspace" |
| Research lab | "Smith Lab workspace" |
| Educational | "Course CS-101 workspace" |
| Knowledge graph | "BNatSchG knowledge workspace" |
| Federation node | "Federation X workspace" |
| Solo lawyer | "Müller Law workspace" |

Metaphor evaporates without losing structural clarity.

## 2. Specialist (NEW pattern primitive)

Introduce Specialist as a pattern-level architectural primitive. Specialist sits BETWEEN Skill (work logic unit) and Workspace (deployment scope). It is the framework's **cohesion abstraction for codified expertise**.

### Functional definition

A unit of codified expertise addressing a defined competence area. Composable, distributable, identity-bearing, standalone-capable.

### What Specialist IS

| Property | Meaning |
|---|---|
| Cohesive | Bounded competence area (citation-verification; planning-document-work; brand-voice) |
| Composable | 5 axes (FROM/IN/WITH/ACROSS/OVER) |
| Distributable | Versioned unit; installable, removable, marketplace-capable |
| Identity-bearing | Has `specialist_id`; references resolve through it |
| Standalone-capable | Can run without workspace wrapper for solo deployments |
| Cross-workspace | Employable by N workspaces simultaneously |
| Substrate-neutral | Materializes per substrate (plugin in CASDK; module in MS AF) |
| Persistent | State persists via bundled entities/memory |

### What Specialist IS NOT

| Confusion | Why it's not that |
|---|---|
| Not a person | Human is "expert-practitioner"; specialist is codified expertise the practitioner consults |
| Not a workflow | Workflows are skills WITHIN; specialist may bundle several |
| Not a plugin | Plugin is substrate-level form; specialist is architectural primitive that materializes as plugin |
| Not a department | Department is deployment-internal optional grouping convention |
| Not a microservice | No transport/network boundary; runs in-process via substrate |
| Not a knowledge graph alone | KG is passive data; specialist is active capability + state + workflow potential |

### Unique value (what only Specialist enables)

| Without Specialist | With Specialist |
|---|---|
| Skills locked to one workspace; no cross-workspace reuse | Cross-workspace expertise sharing native (citation-verification across planning + legal + research) |
| Marketplace impossible (skill too granular; workspace too coarse) | Marketplace unit naturally addressed |
| Solo deployment forces synthetic workspace wrapper | Solo specialist standalone — install one, no workspace required |
| Cohesion of expertise lives implicitly across files | Cohesion is first-class structured concept |
| Distribution of expertise has no natural unit | Distribution unit IS the specialist |
| Federation requires re-implementation per node | Each node assembles specialists from shared registry |

**Key claim**: Specialist is what makes the framework MORE than a collection of skills + entities + state. Cohesion abstraction for codified expertise.

### Composability — 5 axes

| Axis | How |
|---|---|
| Compose-FROM (downward) | Specialist BUNDLES smaller primitives (skills + entities + process entities + references + memory + adapters) |
| Compose-IN (upward) | Workspace EMPLOYS N specialists; multiple specialists cooperate via events + shared workspace-scope entities |
| Compose-WITH (lateral) | Specialists coordinate via AuditEvent + `event_subscriptions` (event-shaped, not call-shaped) |
| Compose-ACROSS (cross-workspace) | One specialist deployable to N workspaces; each workspace has independent state instance; code/structure shared |
| Compose-OVER (optional grouping) | Workspace MAY group employed specialists via optional `groupings: dict[group_name, list[specialist_id]]` |

### Specialist granularity 3-test

When does a competence area warrant its own specialist?

| Test | Question |
|---|---|
| Cohesive competence | Has clear what's-IN / what's-OUT? Internal cohesion + external decoupling? |
| Distributable as unit | Versionable; installable independently; clear distribution boundary? |
| Reusable across workspaces | Recurs across multiple workspaces? Cross-archetype OR within-archetype both qualify |

All three required.

### Two-tier classification

| Tier | Description | PBS examples |
|---|---|---|
| Cross-archetype specialist | Used across multiple workspace archetypes | citation-verification, layered-review-framework, brand-voice |
| Domain-anchored specialist | Used across multiple workspaces of one archetype | planning-document-work, project-management, invoicing |

Distinction matters for marketplace organization; doesn't affect architectural shape.

### Edge cases

| Edge case | Resolution |
|---|---|
| Empty specialist (skills=[]) | Allowed — entities + references + memory provide value (knowledge-graph deployments) |
| Workspace-instance content (e.g., Hendrik's signing convention) | NOT a specialist; lives at workspace-scope. Fails distribution test |
| Hyper-specific niche topic (e.g., §13a-Verfahren) | NOT a specialist; content distributed across existing specialist's process entities + references + skill body. Fails cohesion test |
| Composite specialist (legal-practice-package bundling intake + discovery + filing) | DEFER (D5) — could be recursive composition OR marketplace metadata; await concrete need |

### Decomposition trigger (parallel to skill-granularity)

| Signal | Action |
|---|---|
| Specialist's skills span unrelated competence areas | Split per cohesive competence |
| Specialist's bundle exceeds ~10-15 skills + entities | Likely two competences merged; investigate |
| Two halves are distributable separately | Split |
| Cross-specialist event subscriptions surface within single specialist | "Internal events" suggest decomposition |

## 3. Department → demoted to optional `groupings:` shape

Department is no longer a pattern primitive. Becomes deployment-instance optional grouping convention over employed specialists.

### Schema

`groupings: dict[str, list[specialist_id]] | None` in workspace.md Layer 2 frontmatter.

Single grouping convention per workspace. Multi-grouping (orthogonal classifications) deferred (D4) — covers all known cases with single grouping.

### Examples

```yaml
# PBS-Schulz uses "departments"
groupings:
  planning-document-work: [planning-document-work-specialist]
  administration: [project-management-specialist, invoicing-specialist]

# Hypothetical legal practice uses "practice-areas"
groupings:
  commercial-law: [contracts-specialist, IP-specialist]
  litigation: [litigation-specialist, discovery-specialist]

# Solo creative — no groupings
groupings: {}

# Knowledge-graph deployment — no groupings
groupings: null
```

### Validation

- Each grouping name unique within workspace
- Each specialist_id referenced must exist (gate-validated at workspace boot)
- Convention name ("departments" / "practice-areas" / etc.) is documentation-only; framework provides shape, deployment names

### Why demote

- Cross-archetype stress test: ≥3 archetypes don't use "department" naming naturally
- Pattern-vs-instance discipline: forcing "department" globally violates pattern level (parallel to session-11 "expert" vocabulary reasoning)
- All structural roles preserved on `specialist` axis (scope axis 4, audit filter, routing); department adds zero structural value at pattern layer

## Pydantic shape

### Workspace registration (`extensions/workspace/workspace.md`)

```python
class WorkspaceEntity(EntityBase):  # Layer 2
    workspace_id: str
    display_name: str
    specialists_employed: list[str]  # specialist_id refs
    groupings: dict[str, list[str]] | None
    workspace_scope_entities: dict[str, ManagedEntityRegistration]
    # Client + Actor live here per #15
```

### Specialist registration (`extensions/specialists/<id>/specialist.md`)

```python
class SpecialistEntity(EntityBase):  # Layer 2
    specialist_id: str
    competence_area: str
    skills: list[SkillRef]
    entities: dict[str, ManagedEntityRegistration]
    process_entities: list[ProcessEntityRef]
    references: list[ReferenceRef]
    memory_scope: MemoryScopeRef
    adapters: list[AdapterRef]
    event_subscriptions: list[str]
    substrate_compat: list[SubstrateId]
    classification: Literal["cross-archetype", "domain-anchored"]
```

### Skill frontmatter contract

```yaml
specialist: <specialist-id>  # REQUIRED, no silent default (per make-wrong-shapes-impossible)
display_label: "Begründungs-Schreiber"  # OPTIONAL per session-11 DR
```

### SpecialistDescriptor Pydantic Protocol

Added to `substrate-protocol-design.md` common Substrate Protocol surface:

```python
class SpecialistDescriptor(Protocol):
    specialist_id: str
    competence_area: str
    skills: list[SkillDescriptor]
    entities: dict[str, ManagedEntityDescriptor]
    process_entities: list[ProcessEntityDescriptor]
    references: list[ReferenceDescriptor]
    event_subscriptions: list[str]
    substrate_compat: list[SubstrateId]
```

Materialization: SpecialistDescriptor → Anthropic plugin manifest (CASDK) / MS AF module spec (MS AF). Substrate-coupling impossible-by-construction (per ARCH v0.21).

## Composition with disciplines

| Discipline | Connection |
|---|---|
| Pattern-vs-instance (v0.20) | Workspace + Specialist + Skill = pattern; Department/groupings = instance-level optional ✓ |
| Make-wrong-shapes-impossible (v0.21) | Specialist Pydantic gate; type-name namespacing impossible-by-construction; REQUIRED `specialist:` field ✓ |
| AI-as-runtime hybrid-shape (v0.16) | specialist.md + workspace.md = canonical hybrid-shape (Layer 1 + Layer 2 + body) ✓ |
| Substrate-pluggability (v0.30) | SpecialistDescriptor Protocol; per-substrate materialization ✓ |
| Glue-not-replacement (v0.15) | Specialist hosts adapter-mode entities (e.g., invoicing-specialist + Lexware adapter) ✓ |
| Entity-elevation 3-test | Unchanged — entities elevation-tested same; specialist-scope vs workspace-scope is placement choice ✓ |
| Skill-granularity 3-test | Unchanged — skills elevate within specialist by same criteria ✓ |
| Specialist-granularity 3-test (NEW) | Parallel to skill + entity granularity disciplines (this DR) ✓ |
| Sharp defer rule (v0.20) | All defers below chronological-valid (no manufactured restraint) ✓ |
| Validation-layering (v0.18) | L1 Pydantic; L2 conventions; L3 audit; L4 design-review; L5 marketplace (deferred to v3) ✓ |

## Cross-cutting integration

### Audit-trail (audit-trail-v2.md)

`AuditEvent` schema gains `specialist_id: str | None`:
- `None` = workspace-level operation (workspace bootstrap, settings change, cross-specialist coordination)
- non-None = specialist-scoped event

New event kinds: `specialist_installed`, `specialist_uninstalled`, `specialist_event_subscription_matched`.

Audit-trail filter: `query_audit_trail(specialist: str | None)`.

### Memory taxonomy

4th scope axis: `department` → `specialist`.

Specialist-scope memory bausteine live WITHIN specialist directory: `extensions/specialists/<id>/memory/<baustein>.md`. Aligns with bundling principle (specialist owns its memory; distribution unit self-contained). Cross-cutting memory (NOT specialist-scoped) lives at universal/domain/state axes (unchanged).

### Workspace-scope entities (Client, Actor)

Path: `extensions/workspace/entities/{clients,actors}/<id>.md`.
Pydantic class names: `ClientEntity`, `ActorEntity` (Layer 2 subclasses of `EntityBase`).
Cross-specialist references via `<entity>_id: str` Layer-2 fields, gate-validated at write time (per #15 + entity-md spec).

### Slash command namespacing (#11 Cowork integration)

`/<specialist-id>:<skill-name>` (was `/<dept>:<skill>`). Workspace-level skills: `/workspace:<skill>`.

### Validation gating (5 layers)

| Layer | Specialist enforcement |
|---|---|
| L1 runtime structural | Pydantic validates specialist.md (Layer 1+2); SpecialistDescriptor Protocol |
| L2 runtime conventional | Gate enforces REQUIRED `specialist:` skill frontmatter; event subscriptions parse-validated |
| L3 retrospective | Audit slice scans for over/under-elevated specialists per 3-test |
| L4 prospective | Design-review target enforces 3-test before persistence |
| L5 external boundary | Marketplace upload validation (deferred to ROADMAP v3) |

### Type-name namespacing (per Round 1 Bundle A lock + ARCH v0.21)

`type: <specialist-id>.<short-name>` (e.g., `planning-document-work.project`, `workspace.client`, `universal.reference`). Collisions impossible by construction.

## Pre-implementation surfacing

Per Round 3 of decision-design-sharpening: operational concerns surfaced for #9 implementation phase head-start.

| Concern | Position |
|---|---|
| Boot order | Workspace bootstraps specialists in dependency order (topological sort); event subscriptions resolved after all installed |
| Hot-add/remove specialist | DEFER (D6) — implementation simplifies if specialists settle at workspace boot |
| Specialist conflict (two declaring same entity type) | Impossible-by-construction per type-name namespacing; adapter id collisions caught at install |
| Shared specialist state (one specialist deployed to multiple workspaces) | Each workspace has independent state instance; code/structure shared. State NEVER shared across workspaces |
| Specialist version skew | Workspace.md declares specialist + version; install-time validation. Migration tooling deferred (D1) to ROADMAP v3 marketplace |

## Defers (chronological-valid)

| Defer | Home | Cost being avoided |
|---|---|---|
| D1: Specialist marketplace mechanics (registry, versioning, distribution, pricing, governance) | ROADMAP v3 | Substrate (#11 Cowork) defines plugin distribution; downstream of substrate decisions |
| D2: Cross-substrate specialist portability | Post-#11 first concrete cross-substrate need | No concrete cross-substrate user today |
| D3: Specialist-granularity discipline check (audit slice / design-review target) | Bundle with skill-granularity check (still pending) | No clear case of over-granularity today |
| D4: Multi-grouping (orthogonal classifications over specialists) | First concrete demand | Single-grouping covers all known cases |
| D5: Composite specialist (specialist employing other specialists) | First marketplace need | Could be recursive composition OR marketplace metadata; different shapes |
| D6: Specialist hot-reload (runtime add/remove) | First concrete need | Implementation simplifies if specialists settle at boot |

All chronological-valid: each names specific information that doesn't exist yet.

## Migration cascade

Pre-RAG, pre-launch, no projects bound. Per ARCH "Maintenance discipline" deprecation rules: pre-launch deprecation is essentially free.

| Layer | Change |
|---|---|
| File paths | `extensions/department/<dept>/` → `extensions/specialists/<id>/`; `extensions/office/` → `extensions/workspace/` |
| File names | `department.md` → `specialist.md`; `office.md` → `workspace.md`; `office-config.yaml` → `workspace.md` (adopts hybrid-shape) |
| Pydantic classes | `DepartmentEntity` → `SpecialistEntity`; `OfficeEntity` → `WorkspaceEntity` |
| Skill frontmatter | `department: <dept>` → `specialist: <specialist-id>` (REQUIRED) |
| Slash commands (#11) | `/<dept>:<skill>` → `/<specialist>:<skill>`; `/office:<skill>` → `/workspace:<skill>` |
| AuditEvent schema | `specialist:` filter + `specialist_id` field added |
| Memory taxonomy axis 4 | `department` → `specialist` |
| ARCH | "Office-vs-department" section → "Workspace-vs-specialist"; reference card; v0.30 → v0.31 |
| VISION | Minor edit (architectural primitive section); strategic rewrite in Sub-DR B |
| ROADMAP | #22 collapse; downstream constraint updates for #11 / #9 / #6 / #14 |
| ~12-15 DRs | s/department/specialist + s/office/workspace + logical re-reads |
| Skills (19) | `specialist:` frontmatter required; bundled with #11 single-touch refactor |
| entity-md-spec | namespacing examples + specialist-as-type |
| plugin-conventions.md | Specialist concept section |

## Pattern-vs-instance check

| Domain | Decisions hold? |
|---|---|
| Planning bureau (PBS) | ✅ Workspace shape: office-style; specialists: planning-document-work, project-management, invoicing; groupings: departments |
| Legal practice | ✅ Workspace shape: practice; specialists: contracts, IP, litigation, intake; groupings: practice-areas |
| Research lab | ✅ Workspace shape: lab; specialists: methodology, manuscript-prep, grant-writing; groupings: {} (flat) |
| Brand-voice solo | ✅ Workspace shape: solo; specialists: brand-voice; groupings: {} |
| Knowledge graph | ✅ Workspace shape: KB; specialists: bnatschg-knowledge (empty skills); groupings: null |

All hold cross-domain. Pattern-level. ✓

## Files touched

- `docs/decisions/terminology-and-specialist-primitive.md` (NEW — this file)
- `ARCHITECTURE.md` (v0.30 → v0.31)
- `VISION.md` (minor edit; strategic rewrite in Sub-DR B)
- `ROADMAP.md` (#22 collapse; downstream constraints)
- `docs/conventions/entity-md-spec.md` (namespacing + specialist type)
- `docs/decisions/office-vs-department.md` (header note: superseded scope)
- `docs/decisions/office-level-managed-entities.md` (rename → `workspace-scope-managed-entities.md`)
- `docs/decisions/ai-as-runtime-hybrid-shape.md` (s/department/specialist worked examples)
- `docs/decisions/governance-and-identity-sourcing.md` (s/department/specialist)
- `docs/decisions/skill-expert-agent-and-domain-knowledge.md` (clarification: specialist is NEW primitive ABOVE skill, not skill rename)
- `docs/decisions/substrate-agentic-framework.md` (s/department/specialist)
- `docs/decisions/substrate-protocol-design.md` (SpecialistDescriptor added)
- `docs/plugin-conventions.md` (specialist concept section)
- `HANDOFF.md` (session 13 entry)

## Revisit triggers

- Real second deployment chooses different vocabulary than "specialist" → vocabulary flexibility signal
- Composite specialist need emerges → D5 trigger
- Cross-substrate specialist portability becomes concrete need → D2 trigger
- Specialist marketplace launches → D1 trigger (likely revisits specialist-internal shape)
- Multi-grouping demand surfaces → D4 trigger
