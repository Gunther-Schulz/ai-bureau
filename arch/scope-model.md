---
title: Scope model
topic-cluster: cross-cutting integrator (#1 of 2)
status: locked
---

# Scope model

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the Framework C / Owner B / Layer A scope-classification model + workspace-as-integration-point of all three scopes + per-primitive scope placement across already-locked primitives. Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands per-scope identity-uniqueness rules + schema versioning semantics + scope-categorization error catalog. Foundation-up dependency: scope-model composes with all 8 already-locked Phase 3.4 + Phase 3.5 ARCH topics (substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility) + 4 scope GLOSSARY entries (Framework C / Owner B / Layer A / workspace) + deployment + authority-binding mechanism. Locking scope-model fifth (first cross-cutting integrator) means per-primitive scope placement locks against validated upstream primitive surfaces; 5 of 6 Phase 3.5 ARCH topics close with this lock; only `arch/axis-interactions.md` remains per `ARCHITECTURE.md` §5 reading order.

## 1. Topic scope + frontmatter

**Topic identity**: scope-model — the cross-cutting integrator articulating the three scope-classification primitives (Framework C / Owner B / Layer A) + workspace as the integration point binding all three + per-primitive scope placement across already-locked framework primitives. **Cross-cutting integrator topic class** (NEW; first instance — anchors the cross-cutting integrator topic-template-class parallel to substrate Pattern A 12+7 anchor + specialist-skill primitive-cluster Pattern B + atomic-primitive 12+5 anchor + practitioner Pattern C 12+5 anchor + workflow-work-unit two-Pattern-B 12+5 anchor + claim-defensibility PRIMITIVE+DERIVED 12+5 anchor).

**Primitives covered**:
- `Framework C scope` — SCOPE-CLASSIFICATION (placement category for distributable definitions per locked GLOSSARY)
- `Owner B scope` — SCOPE-CLASSIFICATION (placement category for deployment-specific instances per locked GLOSSARY)
- `Layer A scope` — SCOPE-CLASSIFICATION (placement category for layered content varying by deployment context per locked GLOSSARY)
- `workspace` — PRIMITIVE cross-cutting (the deployment-instance container integrating Framework C selections + Owner B instances + Layer A scope configuration per locked GLOSSARY)

The 4 scope-related entries form an integrated articulation surface; per-primitive scope placement across already-locked primitives composes through this surface.

**Cross-axis claim**: scope-model is **cross-axis** — scope-classification is structurally orthogonal to the three VISION axes (intertwining / sparring / authorship preservation). All three axes operate WITHIN the scope categories (axis-1 intertwined AI participates in workspace-bound runtime at Owner B; axis-2 sparring fires at claim granularity within work-unit instance content at Owner B; axis-3 defensibility resolves at claim-granularity through per-claim attribution chain composing across Framework C definitions + Owner B instances). Scope-model is the cross-cutting structural surface across which per-axis primitives compose.

**Cluster identity (cross-cutting integrator)**: this topic articulates the structural surface across which per-primitive scope placement composes; distinct from primitive-cluster topics (specialist-skill / practitioner / workflow-work-unit / claim-defensibility) which articulate per-primitive structural detail. Cross-cutting integrator topics analyze composition ACROSS prior primitive-cluster topics + Pattern A protocols + mechanism classes; scope-model articulates the structural surface, axis-interactions (Phase 3.5 sixth) articulates the cross-axis composition surface.

**Cardinality at topic level** (per-scope detail in §5):
- Framework C scope: ONE category; N definitions across the framework's distributable artifacts (mechanism / shape / substrate / protocol-implementation / specialist DEFINITION + nested Framework C children per specialist's bundle)
- Owner B scope: ONE category; N instances per workspace deployment (workspace itself + workspace-scope managed entities universal {practitioner-record + Actor} + shape-policy-mandated engagement-target entities + specialist instance content + workflow_instance instances + work-unit instances)
- Layer A scope: ONE category; N content artifacts varying by domain/state context (references / doctypes / bausteine / memory prose / conventions / domain-specific knowledge)
- Workspace: 1:1 reciprocal with deployment per `glossary/deployment.md`; N workspaces per multi-environment or multi-tenant scenario; workspace identity may persist across multiple deployments over time

**Topic boundary**: this topic locks the cross-cutting integrator template anchor (12+5 extends WITHOUT variation; per-pattern conditional applicability rules surfaced — §8 cross-shape policy variation APPLIES; §9 granularity tests / §10 bundle composition / §11 marketplace + distribution / §13 per-element lifecycle ordering N/A documented; §12 N/A-parity preserved); per-scope structural overview (3 sub-sections — Framework C / Owner B / Layer A); workspace integration (workspace IS the binding-instance entity at Owner B); per-primitive composition with framework primitives outside cluster + 4 NEW patterns (E2 nested-bundle / E3 content-unit-IN-instance / E4 cross-cutting non-placed / E5 authority-binding placement); cardinality + lifecycle per scope; logic placement mode (Mode 4 ARCH-doc); operational concerns Phase 6 forward-reference (E6 schema evolution + E7 scope-categorization error categories); cross-shape policy variation 6-row matrix; W1-W4 watch-list; cross-references; per-primitive composition table. It does NOT lock individual primitive structural detail (those live in respective Pattern A / mechanism-class / primitive-cluster ARCH topics) or per-shape policy bundle content (Phase 3.5+ shape definition territory).

**Composition with framework**: scope-model composes with `framework` META-PRIMITIVE (Framework C derives from `framework = mechanisms`); `shape` META-PRIMITIVE (Owner B derives from `framework + shape → workspace deployment`); all 8 already-locked Phase 3.4 + Phase 3.5 ARCH topics (per-primitive scope placement composes through this topic); `authority-binding` mechanism (Framework C definition + Owner B event recording dual-aspect placement per E5).

**Phase routing**: per-scope identity-uniqueness rules + schema versioning semantics → Phase 6 spec (Mode 3 per E6). Scope-categorization error categories + recovery semantics → Phase 6 spec (Mode 3 per E7). Workspace identity persistence schema → Phase 6 spec (per W3 watch-list). Cross-deployment claim portability scope-model variation → Phase 5+ second-deployment evidence (per W2 watch-list).

## 2. Per-scope structural overview

Three sub-sections articulate each scope category structurally without duplicating `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE high-level summary (per Phase 3.2 Sub-decision 3 LOCK: NO content migration MAINTENANCE.md ↔ arch/scope-model.md; layer-distinction maintained — MAINTENANCE.md TOP-LEVEL ARCHITECTURE provides one-line summary + atom/container framing; this topic provides architectural-conceptual articulation).

### 2.1 Framework C scope

**Derivation**: Framework C derives from `framework = mechanisms` per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE — the scope category for framework primitive DEFINITIONS that are universal, immutable, distributable.

**Member catalog** (per locked `glossary/framework-c-scope.md`):
- `mechanism` definitions (atomic interface contracts authored at framework level — e.g., AuditEvent schema; `actor_kind` enum; source-grounding capability; visible reasoning capability per `glossary/mechanism.md` Examples)
- `shape` definitions (policy bundles for archetypes — practitioner-shape / autonomous-business-shape / personal-OS-shape / etc. per `glossary/shape.md` cross-archetype catalog)
- `substrate` definitions (runtime contract Implementations — Claude Agent SDK / MS Agent Framework / hand-rolled per `glossary/substrate.md`)
- `protocol-implementation` definitions (concrete realizations of Pattern A protocol Surfaces — substrate impls / adapter impls / quality-gate impls per `glossary/protocol-architectural.md`)
- `specialist DEFINITION` (bipartite Pattern B; the distributable specialist bundle per `glossary/specialist.md` + `arch/specialist-skill.md` §10)

**Identity convention**: `framework_kind` + `framework_key` in entity-md frontmatter per `glossary/framework-c-scope.md`. Every Framework C entry-md instance declares its kind + key for unique identification within the framework's distributable artifact set.

**Properties**:
- **Universal** — usable by any workspace shape; no shape-specific values embedded (per `glossary/mechanism.md` cross-archetype illustration)
- **Immutable at definition level** — distributable; consumers integrate against fixed definition (per `glossary/specialist.md` "Specialist DEFINITIONS are immutable Framework C distributables")
- **Distributable** — marketplace-listable per ROADMAP v3 forward-conditional; consulting deliverable / firm reuse / OSS / backup-migration consumption modes per `profiles/G-composability-gate.md`

**Boundary test** (per `glossary/framework-c-scope.md`): "is this a distributable definition that any workspace shape could potentially use?" If yes → Framework C. "Is this an instance bound to a deployment?" → Owner B. "Is this content varying by domain/state?" → Layer A.

### 2.2 Owner B scope

**Derivation**: Owner B derives from `framework + shape → workspace deployment` per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE — the scope category for INSTANCES owned at workspace, specialist-instance, or work-unit-instance level.

**Member catalog** (per locked `glossary/owner-b-scope.md` + per Phase 3.5 primitive-cluster ARCH topic locks):
- **workspace itself** — workspace.md selecting shape + substrate + active specialists per `glossary/workspace.md`; the central Owner B instance
- **workspace-scope managed entities universal** (across all shapes):
  - `practitioner-record` — system representation per `arch/practitioner.md` §2.2 RECORD aspect (11-field manifest schema; Pattern C bipartite primitive's Owner B aspect)
  - `Actor` — event emitter records per `glossary/actor.md` (`actor_kind: human / ai_runtime / external` enum)
- **workspace-scope managed entities shape-policy-mandated** (per `glossary/owner-b-scope.md` "additional managed entities per shape-policy mandate (NOT framework-level)"; engagement-target entity per shape policy):
  - practitioner-shape: `Client` (engagement target for accountability-bearing service)
  - autonomous-business-shape: `Customer`
  - research-lab-shape: `Funder` / `Co-author` / `Institution`
  - personal-OS-shape: NONE (engagement-target entity not universal per `glossary/owner-b-scope.md`)
- **specialist instance content** — entities owned within an active specialist instance per `glossary/specialist.md` (distinct from specialist DEFINITION at Framework C; bipartite Pattern B's INSTANCE aspect)
- **workflow_instance instances** — workflow_instance entities per `arch/workflow-work-unit.md` SD-2 4-sub-section structural overview (workflow_instance manifest schema; Pattern B INSTANCE aspect with optional applicability)
- **work-unit instances** — work-unit instance entities per `arch/workflow-work-unit.md` SD-2 (work-unit instance manifest schema; Pattern B INSTANCE aspect always-present container)

**Identity convention**: `owner_scope` + `owner_key` in entity-md frontmatter per `glossary/owner-b-scope.md`. Every Owner B entry-md instance declares its scope (workspace / specialist-instance / work-unit-instance) + key for unique identification within the deployment.

**Properties**:
- **Deployment-specific** — bound to workspace deployment context (per `glossary/owner-b-scope.md`)
- **Workspace-bound** — exists for workspace lifetime; persistence tied to workspace identity (per `glossary/workspace.md` Cardinality)

**Boundary test** (per `glossary/owner-b-scope.md`): "is this a deployment-specific instance bound to a workspace, specialist instance, or work-unit?" If yes → Owner B. "Is this a distributable definition?" → Framework C. "Is this content varying by deployment context (domain/state)?" → Layer A.

### 2.3 Layer A scope

**Derivation**: Layer A is **orthogonal axis** to the framework=mechanisms / shape=policies framing per `glossary/layer-a-scope.md` — independent classification axis for content layering by domain/state context. NOT derived from framework/shape (unlike Framework C + Owner B); content scoping is the orthogonal axis.

**Member catalog** (per locked `glossary/layer-a-scope.md`):
- references (e.g., legal texts varying by jurisdiction)
- doctypes (e.g., B-Plan-Begründung domain-specific)
- bausteine (saved text patterns; domain or state specific)
- memory prose (style-spec / korrektur-rules / verfahren docs; domain-specific)
- conventions (writing conventions per language / jurisdiction)
- domain-specific knowledge artifacts

**Identity convention**: `layer_scope` + `layer_key` in entity-md frontmatter per `glossary/layer-a-scope.md`. Effective content for a workspace = universal + active-domains + active-states (workspace declares which apply via `workspace.scope.{domains, states}` configuration per §3 workspace integration).

**Layer values**:
- `universal` — applies to every deployment regardless of domain or jurisdiction
- `domain` — applies to deployments in specific domains (e.g., PV-FFA / Wind / Naturschutz / Innenentwicklung); multiple domains can be active simultaneously
- `state` — applies to deployments in specific jurisdictions (e.g., DE-BB / DE-BY / DE-BW); multiple states can be active simultaneously

**Properties**:
- **Content varying by deployment context** — domain/state context determines applicability (per `glossary/layer-a-scope.md`)
- **Independent classification axis** — NOT about mechanism vs policy; about CONTENT applicability by deployment context (per `glossary/layer-a-scope.md` "Layer A is INDEPENDENT classification axis")
- **Composes with workspace.scope configuration** — workspace's `scope.{domains, states}` determines which Layer A content applies at runtime

**Boundary test** (per `glossary/layer-a-scope.md`): "does this content vary by deployment context (domain / state / universal)?" If yes → Layer A. "Is this a definition?" → Framework C. "Is this an instance bound to deployment?" → Owner B.

## 3. Cross-scope composition WITHIN cluster (workspace integration)

Workspace IS the integration point binding all three scopes — the architectural surface where Framework C selections + Owner B instances + Layer A content compose at workspace deployment time.

**Workspace as central Owner B instance + container**: per `glossary/workspace.md`, workspace.md is the binding-instance entity at Owner B; workspace itself is the central Owner B instance + container for workspace-scope managed entities (practitioner-record + Actor universal + engagement-target entities shape-policy-mandated). Workspace integration spans:

- **Framework C selections via workspace.md fields**:
  - `workspace.shape` — selects exactly one shape from Framework C shape catalog
  - `workspace.substrate` — selects exactly one substrate Implementation from Framework C substrate catalog
  - `workspace.specialists_active` — list referencing Framework C specialist DEFINITIONs
  - Per `glossary/workspace.md` line 16-18: workspace IS the deployment-instance container that integrates framework mechanisms + shape policies + active specialists + practitioners + state into a coherent unit

- **Owner B instance ownership at workspace level**:
  - workspace itself = central Owner B instance per `glossary/owner-b-scope.md`
  - workspace contains workspace-scope managed entities (practitioner-record + Actor + shape-policy-mandated engagement-target entities) per `glossary/owner-b-scope.md` Members list
  - workspace contains specialist instance content per active-specialists boot
  - workspace contains workflow_instance instances per `arch/workflow-work-unit.md` SD-2 + work-unit instance instances per `arch/workflow-work-unit.md` SD-2

- **Layer A scope-resolution via workspace.scope configuration**:
  - `workspace.scope.{domains, states}` configuration determines which Layer A content applies per `glossary/workspace.md` composes-with Layer A row
  - Effective content at runtime = universal + active-domains + active-states per `glossary/layer-a-scope.md`

**Workspace identity persistence across multiple deployments** (W3 watch-list trigger): workspace identity may persist across multiple deployments over time (backup→restore / substrate migration / re-activation per `glossary/deployment.md` "Multi-deployment-of-same-workspace patterns") — workspace identity invariants across deployments is workspace-portability concern (Phase 6 spec territory per W3).

**1:1 reciprocal cardinality with deployment**: per `glossary/deployment.md`, deployment = workspace-as-bound-runtime; 1:1 reciprocal at framework primitive level (exactly 1 deployment per workspace at any moment of active runtime; sequence of deployments over a workspace's identity lifetime). Multi-environment scenarios (dev / staging / prod) = N workspaces (each its own deployment); multi-tenant scenarios (one substrate hosting multiple workspace runtimes) = substrate-Instance-level concern, NOT framework-level cardinality concern (per `glossary/workspace.md` Cardinality).

**Workspace boot integration with composite boot sequence** (E1): workspace.md loading realizes scope-categories in ordered sequence per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection. Scope-categorization realization fires INSIDE substrate-phase 1-5 envelope, NOT as separate boot phase:

1. **substrate-phase 1** (substrate Implementation instantiates per workspace.md selection): Framework C substrate selection resolved (workspace.substrate field)
2. **substrate-phase 2** (substrate registers configured MCP servers): adapter-binding-list-loaded inherited from workspace-scope adapter bindings per Owner B placement
3. **substrate-phase 3** (Adapter bindings load): Framework C adapter Implementations resolved per workspace.md adapter bindings list
4. **substrate-phase 4** (Specialist registration): Framework C specialist DEFINITIONs resolved per workspace.specialists_active list; specialist instance content loaded at Owner B per active-specialists boot
5. **substrate-phase 5** (boot_complete event emitted): workspace-scope managed entities loaded (practitioner-record + Actor universal + engagement-target entity per shape policy); workflow_instance instances + work-unit instances loaded; Layer A content scope-resolved per workspace.scope.{domains, states} configuration

Composes with `arch/audit.md` §10 boot-before-substrate / shutdown-after-substrate ordering invariants + `arch/specialist-skill.md` §13 per-primitive lifecycle ordering for specialist registration.

## 4. Composition with framework primitives outside cluster

Per-primitive narrative articulating how each already-locked framework primitive's scope placement composes. 4 NEW load-bearing patterns surface here (E2 nested-bundle / E3 content-unit-IN-instance / E4 cross-cutting non-placed / E5 authority-binding placement).

### Pattern E2 — Nested-bundle pattern (Framework C children under specialist-namespace)

Specialist Framework C bundle NESTS other Framework C definitions under **specialist-namespace** per `glossary/specialist.md` locked mechanic (per `arch/specialist-skill.md` §10 specialist-namespace mechanic + `glossary/specialist.md` composes-with skill / work-unit / workflow rows):

- skill DEFINITIONs nested in specialist's Framework C bundle under specialist-namespace; fully-qualified reference `specialist-name:skill-name`
- workflow DEFINITIONs nested in specialist's Framework C bundle under specialist-namespace; fully-qualified reference `specialist-name:workflow-name`
- work-unit KIND DEFINITIONs nested in specialist's Framework C bundle under specialist-namespace; fully-qualified reference `specialist-name:kind-name`
- adapter Implementations may be bundled in specialist's Framework C bundle per `glossary/specialist.md` composes-with adapter row

Distinct from atomic Framework C primitives (substrate / shape / mechanism — no nested Framework C children). The nested-bundle pattern is load-bearing structurally: prevents cross-specialist KIND/skill/workflow-name collision; specialist-namespace mechanic is the discriminator. NEW pattern surfaced through scope-model articulation; documented for future Framework C primitive design.

### Pattern E3 — Content-unit-IN-instance (claim INHERITS work-unit's Owner B placement)

Claim is **content-unit IN work-unit** per `arch/claim-defensibility.md` §3 + `glossary/claim.md` — claim INHERITS work-unit's Owner B placement (NOT separately scoped). Claims compose into work-unit instance output content per `glossary/work-unit.md` composes-with claim row + `glossary/claim.md` composes-with work-unit row.

Distinct from instance-content-at-Owner-B placement (specialist instance content / work-unit instance):
- specialist instance content / work-unit instance = SEPARATELY-PLACED Owner B sub-entities (own `owner_scope` + `owner_key` per `glossary/owner-b-scope.md`)
- claim = INSIDE-the-instance-payload (NOT a separately-placed Owner B sub-entity; bundled INTO work-unit instance content per `arch/claim-defensibility.md` §5 "owner = work-unit (claims bundled INTO work-unit output content)")

Per `arch/claim-defensibility.md` §13 cross-pattern destruction inheritance: claims inherit work-unit's `instance_content_dissolution_policy: archive | delete-with-audit` (NO separate per-claim destruction policy). The content-unit-IN-instance pattern is load-bearing: distinguishes content-level atomic assertions (claims) from entity-level Owner B sub-instances (specialist instance content / work-unit instances). NEW pattern surfaced through scope-model articulation; documented for future content-level primitive design.

### Pattern E4 — Cross-cutting non-placed (DERIVED + cross-axis force + non-entity primitives)

Properties / tests / concepts that are NOT placed get explicit N/A documentation in §18 composition table. Load-bearing because cross-axis non-placed primitives compose ACROSS scope categories (test/property applies to placed entities; concept manifests through behavior of placed entities) without occupying any single scope category:

- **defensibility** (DERIVED property/test per `glossary/defensibility.md`): NOT placed; resolves at claim granularity through per-claim attribution chain composing across Framework C definitions (skill identifier → specialist-DEFINITION) + Owner B instances (workspace + work-unit instance + practitioner-RECORD)
- **engaged-authorship** (DERIVED axis-3 success mode per `glossary/engaged-authorship.md`): NOT placed; per-claim engagement events captured at Owner B in audit-trail
- **category-collapse** (DERIVED cross-axis force per `glossary/category-collapse.md`): NOT placed; manifests through behavior of placed practitioner-RECORD + AI-runtime
- **failure modes** (DERIVED per `glossary/rubber-stamping.md` + `glossary/answer-machine-ai.md` + `glossary/oracle-ai.md` + `glossary/validator-ai.md` + `glossary/tacked-on-ai.md` + `glossary/intertwined-ai.md`): NOT placed; manifest through behavior of placed entities at runtime
- **VISION axes** (intertwining / sparring / authorship-preservation per `glossary/intertwining.md` + `glossary/sparring.md` + `glossary/authorship-preservation.md`): NOT placed; cross-cutting concepts that placed primitives serve
- **co-worker** (DERIVED relational claim per `glossary/co-worker.md`): NOT placed; relational frame between practitioner-RECORD (Owner B) + AI-runtime substrate Instance (Owner B running instance of Framework C substrate Implementation)
- **HUMAN practitioner aspect** (cross-cutting per `glossary/practitioner.md` Pattern C bipartite): NOT placed (the natural person bearing legal/professional accountability in the world; framework records nothing about HUMAN directly per `arch/practitioner.md` §2.1); RECORD aspect = placed at Owner B per `arch/practitioner.md` §2.2

NEW pattern surfaced through scope-model articulation; documented for future cross-cutting non-placed primitive design + scope-model boundary test (per §1 Cluster boundary "this topic does NOT lock individual primitive structural detail").

### Pattern E5 — Authority-binding placement (mechanism dual-aspect)

Authority-binding mechanism per `glossary/authority-binding.md` PRIMITIVE / framework-mechanism placement = **Framework C** (mechanism definition home per `glossary/framework-c-scope.md` Members list — mechanism definitions live at Framework C). Authority-binding manifests at runtime as `actor_kind` + actor identity recorded ON events at Owner B (audit-trail) per `glossary/authority-binding.md` per-event actor declaration sub-aspect.

**Same dual-aspect placement as substrate**:
- Framework C: substrate Surface (mechanism definition) + substrate Implementations (Framework C distributable definitions per `glossary/substrate.md`)
- Owner B: substrate Implementation Instance running per workspace per `glossary/substrate.md` (workspace-bound at workspace deployment)

**Same shape as audit mechanism class**:
- Framework C: AuditEvent schema (Surface) + audit class definition per `arch/audit.md` §2
- Owner B: audit-trail (sequence of events) accumulating at workspace deployment per `arch/audit.md` §B

NEW pattern surfaced through scope-model articulation; load-bearing for authority-binding mechanism's dual-aspect documented explicitly.

### Per-primitive composition narrative (load-bearing primitives)

| Primitive | Pattern | Framework C aspect | Owner B aspect | Layer A aspect |
|---|---|---|---|---|
| **substrate** | Pattern A; tri-aspect | Surface (mechanism) + Implementations (distributable definitions) | Implementation Instance running per workspace | N/A |
| **adapter** | Pattern A; tri-aspect | Surface (META + per-class) + Implementations | Instance bindings per workspace (multiple typically) | N/A |
| **sparring** | Pattern D mechanism class | Surface (8 sub-mechanism contracts) + per-shape activation matrix definitions | Sparring events captured in audit-trail at workspace | N/A |
| **audit** | Pattern D mechanism class | Surface + AuditEvent schema | audit-trail at workspace (sequence of events; append-only) | N/A |
| **specialist** | Pattern B; bipartite | DEFINITION (distributable bundle nesting skill / workflow / work-unit-kind / adapter children per E2) | Instance content (entities owned within deployed specialist instance) | N/A |
| **skill** | atomic within specialist | Nested in specialist's Framework C bundle under specialist-namespace per E2 | Per-skill events captured in audit-trail at workspace | N/A |
| **practitioner** | Pattern C; bipartite | N/A (HUMAN aspect cross-cutting NOT placed per E4) | RECORD aspect (workspace-scope managed entity per `arch/practitioner.md` §2.2) | N/A |
| **workflow** | Pattern B; bipartite | DEFINITION nested in specialist's Framework C bundle per E2 | workflow_instance instance per workspace per `arch/workflow-work-unit.md` SD-2 | N/A |
| **work-unit** | Pattern B; bipartite | KIND DEFINITION nested in specialist's Framework C bundle per E2 | work-unit instance per workspace per `arch/workflow-work-unit.md` SD-2 | N/A |
| **claim** | PRIMITIVE; content-unit | N/A | Content-unit IN work-unit instance (INHERITS work-unit's Owner B placement per E3) | N/A |
| **defensibility** | DERIVED; property/test | N/A | NOT placed per E4 | N/A |
| **engaged-authorship** | DERIVED; axis-3 success mode | N/A | NOT placed per E4; events captured at Owner B per `glossary/engaged-authorship.md` | N/A |
| **authority-binding** | mechanism | Mechanism definition (Framework C per E5) | Event recording at Owner B per E5 | N/A |
| **mechanism** / **policy** / **shape** / **protocol-architectural** | meta | Definitions live at Framework C per `glossary/framework-c-scope.md` Members list | N/A | N/A |
| **session** | PRIMITIVE; bounded interaction | N/A | Bounded interaction unit within workspace (Owner B) per `glossary/session.md` | N/A |
| **event** | PRIMITIVE; framework-mechanism | AuditEvent schema definition (Framework C per `glossary/event.md` Class: framework-mechanism layer) | Event records at Owner B (audit-trail) | N/A |
| **actor** | PRIMITIVE; cross-cutting | `actor_kind` enum (framework-mechanism per `glossary/actor.md`) | Actor records at Owner B (workspace-scope managed entities per `glossary/actor.md`) | N/A |

Layer A primitives (references / doctypes / bausteine / memory prose / conventions / domain-specific knowledge per §2.3 Member catalog) live at Layer A per `glossary/layer-a-scope.md` Members list — content layering by domain/state context orthogonal to mechanism/policy split.

## 5. Cardinality + lifecycle (per scope)

### Framework C cardinality + lifecycle

| Concern | Value | Mechanism |
|---|---|---|
| Definitions per framework | N (across mechanism / shape / substrate / protocol-implementation / specialist DEFINITION + nested children per E2) | Per `glossary/framework-c-scope.md` Members list; definitions are universal/distributable |
| Definition lifecycle | Immutable per definition version | Per `glossary/specialist.md` "Specialist DEFINITIONS are immutable Framework C distributables"; specialist version bumps create new immutable definition versions |
| Definition versioning | Per-definition versioning (semver-like per ROADMAP v3) | Per `MAINTENANCE.md` Other maintenance disciplines §5 versioning per layer; Phase 6 spec lands per-scope identity-uniqueness rules + schema versioning semantics per E6 |
| Distributable lifecycle | Marketplace-listable per ROADMAP v3 forward-conditional | Per `profiles/G-composability-gate.md` multi-mode consumption framing |

### Owner B cardinality + lifecycle

| Concern | Value | Mechanism |
|---|---|---|
| workspace per active deployment | 1 | Per `glossary/workspace.md` Cardinality + `glossary/deployment.md` 1:1 reciprocal at framework primitive level |
| workspace-scope managed entities universal per workspace | 1+ practitioner-record (per shape — solo-1 / multi-N / legal-entity-firm-N) + 1 ai_runtime Actor (substrate's Instance singular per workspace) + N external Actors | Per `arch/practitioner.md` §5 multi-practitioner cardinality matrix + `glossary/actor.md` cardinality |
| workspace-scope managed entities shape-policy-mandated | Per shape policy (engagement-target entity per archetype OR none for personal-OS) | Per `glossary/owner-b-scope.md` shape-policy-mandated rule + per-shape policy bundle declaration |
| specialist instance content per workspace | N (per active-specialists list; persists across activation/deactivation cycles per `glossary/specialist.md`) | Per `arch/specialist-skill.md` §5 + §13 archival-as-default destruction |
| workflow_instance instances per workspace | 0..N per active specialist (instances created per work-unit when codified pattern applies per `glossary/workflow.md`; 0 for ad-hoc work-units) | Per `arch/workflow-work-unit.md` §5 |
| work-unit instances per workspace | N per active kind | Per `arch/workflow-work-unit.md` §5 + `glossary/work-unit.md` cardinality |
| Workspace identity persistence | Across multiple deployments over time (backup→restore / substrate migration / re-activation per `glossary/deployment.md`) | Workspace-portability concern (Phase 6 spec per W3) |

### Layer A cardinality + lifecycle

| Concern | Value | Mechanism |
|---|---|---|
| Layer A content artifacts | N across universal / domain / state Layer values | Per `glossary/layer-a-scope.md` Layer values |
| Effective content per workspace | universal + active-domains + active-states (per workspace.scope configuration) | Per `glossary/workspace.md` composes-with Layer A row + §3 workspace integration |
| Layer A lifecycle | Content-versioning per shape catalog curator (L9 perspective per `profiles/INDEX.md` L9 row) | Phase 6 spec lands schema versioning semantics per E6 |
| Cross-archetype applicability metadata | Per Layer value declaration (universal / domain / state) | Per `glossary/layer-a-scope.md` |

## 6. Logic placement mode

Per `ARCHITECTURE.md` §6 Logic placement modes (4-mode distribution Mode 1 production-runtime LLM-MD / Mode 2 production-runtime Python / Mode 3 hybrid Phase 6 specs / Mode 4 development-time LLM-MD):

**Per-element Mode distribution within scopes**:

- **Framework C Mode distribution**:
  - mechanism definitions: Mode 2 production-runtime Python (Pydantic schemas per `glossary/mechanism.md` Examples — AuditEvent schema; `actor_kind` enum)
  - shape definitions: Mode 1 production-runtime LLM-MD (shape policy bundles per `glossary/shape.md`; AI reads at runtime)
  - substrate definitions: Mode 2 production-runtime Python (substrate Implementations per `glossary/substrate.md`; per-impl realization)
  - specialist DEFINITIONs: Mode 1 production-runtime LLM-MD (specialist bundle content per `arch/specialist-skill.md` §6)

- **Owner B Mode distribution**:
  - workspace.md: Mode 1 production-runtime LLM-MD (AI reads at runtime per `ARCHITECTURE.md` §6 Mode 1 examples)
  - workspace-scope managed entities (practitioner-record + Actor + engagement-target): Mode 1 production-runtime LLM-MD (entity-md per Owner B convention)
  - specialist instance content: Mode 1 production-runtime LLM-MD per `arch/specialist-skill.md` §6
  - workflow_instance instances + work-unit instances: Mode 1 production-runtime LLM-MD per `arch/workflow-work-unit.md` §6 + Mode 2 substrate-impl Python (state machine validation per `arch/workflow-work-unit.md` SD-4)

- **Layer A Mode distribution**:
  - references / doctypes / bausteine / memory prose / conventions: Mode 1 production-runtime LLM-MD (content varying by domain/state context per `glossary/layer-a-scope.md` Members list)
  - domain-specific knowledge artifacts: Mode 1 production-runtime LLM-MD

- **THIS topic + DR + scope GLOSSARY entries**: Mode 4 development-time documentation (NOT production-runtime; framework-developer orientation per `ARCHITECTURE.md` §1 audience + scope)

Cross-cutting integrator topics are Mode 4 development-time documentation — articulating the architectural surface across which per-axis primitives compose, not what production AI loads at runtime. Production AI in a deployed PBS workspace loads Mode 1 markdown (workspace.md / active specialist DEFINITIONs / skill SKILL.md / shape policy bundles); this topic is for framework-developer orientation.

**LLM-instruction tightness asymmetry** (per `ARCHITECTURE.md` §6 cross-cutting principles): Mode 1 markdown (workspace.md content + specialist DEFINITION content + Layer A content) requires the highest LLM-instruction tightness review effort because LLMs paper over imprecise markdown by inference. Phase 6 specialist-bundle authoring inherits this discipline; Phase 6 Layer A content authoring inherits this discipline.

## 7. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns.

- **Per-scope identity-uniqueness rules + schema versioning semantics** (per E6 schema-evolution forward-reference): per-scope identity convention (`framework_kind` + `framework_key` for Framework C; `owner_scope` + `owner_key` for Owner B; `layer_scope` + `layer_key` for Layer A) may need `version` field for schema evolution. Framework C definitions distributable per G profile mode 4 marketplace future-conditional + mode 1 consulting versioning concerns; Owner B workspace serialization format per `glossary/deployment.md` workspace-portability concern Phase 6 spec; Layer A content versioning per shape catalog curator L9 perspective. Phase 6 spec: per-scope identity uniqueness rules + schema versioning semantics + breaking-change documentation discipline. NOT locked at ARCH level.

- **Scope-categorization error categories + recovery semantics** (per E7 forward-reference): scope-categorization errors that surface at runtime include:
  - **Invalid framework_kind reference** — workspace.specialists_active references non-existent specialist DEFINITION (Framework C resolution failure)
  - **Orphan owner_scope reference** — workspace-scope managed entity references non-existent workspace (Owner B integrity failure)
  - **Layer A content scope-mismatch** — workspace.scope.domains lists domain with no Layer A content available (Layer A applicability gap)
  - **Cross-deployment scope-resolution failure** — workspace identity persistence W3-related (cross-substrate migration scope-resolution gap)
  
  Phase 6 spec: error catalog + recovery semantics. NOT locked at ARCH level.

- **Workspace identity persistence schema** (per W3 watch-list): workspace identity invariants across multiple deployments (backup→restore / substrate migration / re-activation per `glossary/deployment.md` "Multi-deployment-of-same-workspace patterns"); awaits Phase 6 audit-trail integrity verification + cryptographic signing per `arch/practitioner.md` W3 + `arch/audit.md` §D + `arch/claim-defensibility.md` W4

- **Cross-deployment claim portability scope-model variation** (per W2 watch-list + cross-link to `arch/claim-defensibility.md` W2 + `arch/substrate.md` §F): cross-deployment claim portability variation per shape (practitioner-shape MANDATORY cross-substrate per `arch/claim-defensibility.md` §8; autonomous-business bounded-by-deployment; personal-OS N/A); awaits first cross-deployment claim ingestion deployment evidence

- **Engagement-target entity catalog per second-shape productization** (per W4 watch-list + cross-link to BACKLOG shape-neutrality watch-list): engagement-target entity for second shape (Customer for autonomous-business / Funder + Co-author + Institution for research-lab / etc.) fully realized when second-shape design begins

## 8. Cross-shape policy variation (cluster-conditional; APPLIES)

Per cross-cutting integrator topic template + per-pattern conditional applicability rules: §8 applies when scope-categorization is shape-policy-mediated. Engagement-target Owner B managed entities are shape-policy-mandated per `glossary/owner-b-scope.md` "additional managed entities per shape-policy mandate (NOT framework-level)"; per-shape variation in workspace-scope managed entity catalog + workspace.md required fields + Layer A scope configuration defaults + specialists_active recommended set + substrate selection constraints.

**What is shape-uniform** (NOT shape-policy-mediated):
- Three-scope structural articulation (Framework C / Owner B / Layer A; same architectural commitment across all shapes)
- Workspace as central Owner B instance + container (same per shape)
- 1:1 reciprocal cardinality with deployment (same per shape per `glossary/deployment.md`)
- Per-scope identity convention (`framework_kind` + `framework_key` / `owner_scope` + `owner_key` / `layer_scope` + `layer_key`; same per shape)
- Workspace boot integration with composite boot sequence per `ARCHITECTURE.md` §6 (same per shape)

**What is shape-policy-mediated** (6-row matrix; parallel to claim-defensibility §8 6-row precedent + workflow-work-unit §8 6-row precedent + practitioner §8 cross-shape variation precedent):

| Dimension | practitioner-shape | autonomous-business-shape | research-lab-shape | personal-OS-shape |
|---|---|---|---|---|
| **Engagement-target Owner B managed entity catalog per shape** (per `glossary/owner-b-scope.md` shape-policy-mandated rule) | Client (engagement target for accountability-bearing service) | Customer | Funder / Co-author / Institution | NONE (engagement-target entity not universal per `glossary/owner-b-scope.md`) |
| **workspace.md required fields per shape** (per `arch/practitioner.md` §4 multi-practitioner authorship requirements + legal-entity context) | Multi-practitioner cardinality matrix (solo-1 / multi-N / legal-entity-firm-N); legal_entity_context block per `arch/practitioner.md` §4 | Operator-supervised governance fields | Multi-author co-authorship attribution fields | Single-user fields |
| **Workspace-scope managed entity universals + shape-extensions per shape** (per `glossary/owner-b-scope.md` Members list) | Universals (practitioner-record + Actor) + Client | Universals + Customer | Universals + Funder / Co-author / Institution | Universals only (NO engagement-target extension) |
| **Layer A scope configuration defaults per shape** (per `glossary/workspace.md` composes-with Layer A row + `glossary/layer-a-scope.md` Layer values) | domains = {planning / naturschutz / environmental-law / baurecht}; states = {DE-BB / DE-BY / etc.} per archetype recommendation | domains = {business-domain-specific} + states = {business-state-specific per business archetype} | domains = {research-domain-specific} + states = {jurisdiction-specific per regulatory environment} | domains = minimal universal-only default |
| **Specialists_active recommended set per shape** (per `glossary/specialist.md` Cross-archetype illustration named-archived examples) | Practitioner-shape recommends sparring-relevant specialists (planning-document-work / citation-verification / legal-research / etc.) | Autonomous-business specialists (project-management / invoicing / customer-service / etc.) | Research-lab specialists (citation-verification / methodology-review / manuscript-drafting / etc.) | Personal-OS specialists (task-management / note-taking / calendar / etc.) |
| **Substrate selection constraints per shape** (per `arch/audit.md` §14 cross-shape policy variation precedent + `arch/sparring.md` §4 framework-baseline-vs-shape-extension partition) | Substrate must support claim-level audit granularity + sparring sub-mechanisms 1-4 architecturally-encoded per `arch/sparring.md` §4 | Substrate must support action-level audit granularity + budget-policy authority-binding | Substrate must support claim-level audit granularity (research output accountability-bearing) | Substrate may support light audit granularity + minimal sparring per shape policy |

scope-model primitives stay shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (three-scope structural articulation + workspace integration + per-scope identity convention are uniform across all shapes; per-shape variation lives in shape policy bundle declaring per-shape engagement-target catalog + workspace.md required fields + workspace-scope managed entity catalog + Layer A scope configuration defaults + specialists_active recommended set + substrate selection constraints).

**Cross-axis composition** (cross-cutting integrator surface across which per-axis primitives compose):

- **axis-1 (intertwining) cross-axis composition**: workspace IS the container for AI-co-worker intertwining per `glossary/workspace.md` cross-axis classification; intertwined AI participates in workspace-bound runtime at Owner B per `glossary/intertwined-ai.md` + `glossary/co-worker.md`; co-worker frame requires axis-1 mechanisms (persistent state via substrate Surface §F + orchestration + source-grounding + audit emission + authority binding) all composing across scope categories
- **axis-2 (sparring) cross-axis composition**: sparring events captured at Owner B in audit-trail per `arch/sparring.md` §4 + `arch/audit.md` §A; activation matrix per shape (Pattern D mechanism class) is workspace-policy-mediated through shape policy bundle at Framework C declaring per-shape activation per `arch/sparring.md` §14; per-sub-mechanism realization variation independent within fixed Surface
- **axis-3 (authorship preservation) cross-axis composition**: defensibility resolves at claim/work-unit granularity at Owner B per `arch/claim-defensibility.md` §3 + §13; workspace's accountability scope = scope of practitioner-author defensibility per `glossary/workspace.md` axis-3 framing; cross-deployment claim portability = cross-Owner-B reference per `arch/substrate.md` §F + `arch/claim-defensibility.md` §6 (per-shape policy variation matrix row 6 cross-deployment claim portability)

## 9. Granularity tests (cluster-conditional; N/A)

**N/A** — cross-cutting integrators have no granularity-test surface. Per cross-cutting integrator topic-template-class definition (this topic): scope-categorization is binary classification (Framework C / Owner B / Layer A — definitively one category per primitive per scope-classification convention), NOT granular. Granularity discriminators live in respective primitive-cluster topics:

- specialist + skill granularity 3-tests live at `arch/specialist-skill.md` §9
- workflow + work-unit granularity 3-tests live at `arch/workflow-work-unit.md` §9
- claim 3-test + defensibility resolution-granularity test live at `arch/claim-defensibility.md` §9

§9 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule (preserves template-anchoring stability for downstream cross-cutting integrator topics — `arch/axis-interactions.md` Phase 3.5 sixth + final ARCH topic).

## 10. Bundle composition (cluster-conditional; N/A)

**N/A** — scope-model doesn't bundle artifacts. Per cross-cutting integrator topic-template-class definition: scope-categorization is structural surface articulation, NOT a bundling primitive. Framework C bundling is specialist's domain per `arch/specialist-skill.md` §10 (specialist BUNDLES skills + entity-kinds + workflows + work-unit-kinds + adapter implementations); cross-cutting integrator topics analyze composition ACROSS prior topics, not packaging.

§10 documented N/A explicitly per template rule.

## 11. Marketplace + distribution mechanics (cluster-conditional; N/A)

**N/A** — scope-model is integrator topic, not independently distributable. Per cross-cutting integrator topic-template-class definition: scope-categorization is structural surface articulation, NOT a distributable artifact. Distributable artifacts (specialist DEFINITIONs / shape policy bundles / Layer A content) live at Framework C per their respective primitive-cluster topics + `glossary/framework-c-scope.md` Members list; per-distributable distribution mechanics live in respective primitive-cluster topics (`arch/specialist-skill.md` §11 specialist marketplace deferred per W1).

§11 documented N/A explicitly per template rule.

## 12. Cross-references reservation

Cross-references for this topic are consolidated in §17 below per cross-cutting integrator topic template convention; this section number reserved as **N/A-parity slot** preserving visual numbering parity with substrate's §12 Transport variation N/A + `arch/specialist-skill.md` §12 reservation + `arch/practitioner.md` §12 reservation + `arch/workflow-work-unit.md` §12 reservation + `arch/claim-defensibility.md` §12 reservation. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template §-numbering convention: "**§12 reserved as N/A-parity slot** (parity with substrate's §12 Transport variation N/A — preserves visual numbering parity across topic-templates; downstream primitive-cluster topic Writers MUST keep §12 reserved as N/A-parity rather than omit-§12 or fill-§12-with-content; prevents template drift)." Cross-cutting integrator topics inherit this convention.

## 13. Per-element lifecycle ordering (cluster-conditional; N/A)

**N/A** — scope categories are placement classifications, NOT entities with boot/shutdown/activation ordering distinct from §5 cardinality + lifecycle treatment. Per cross-cutting integrator topic-template-class definition: scope-categorization is structural surface articulation; per-primitive lifecycle ordering lives in respective primitive-cluster + Pattern A + mechanism-class topics (substrate §10 / audit §10 / specialist-skill §13 / practitioner §13 / workflow-work-unit §13 / claim-defensibility §13).

Workspace boot integration with composite boot sequence is articulated in §3 cross-scope composition WITHIN cluster (E1 — workspace.md loading realizes scope-categories in ordered sequence per `ARCHITECTURE.md` §6 composite boot subsection). NO separate scope-boot ordering distinct from substrate-phase 1-5 envelope.

§13 documented N/A explicitly per template rule.

## 14. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| **W1** | Multi-tenant federation scope-model variation | Workspace federation surfaces (per `arch/practitioner.md` W1 multi-tenant federation practitioner identity binding mechanism design) — when workspace federation surfaces, federated-Owner-B mechanism design | Per-shape policy declares federation-scope-model variation; cross-link: `arch/practitioner.md` §14 W1 multi-tenant federation |
| **W2** | Cross-deployment claim portability scope-model variation | First cross-deployment claim ingestion deployment evidence surfaces (per `arch/claim-defensibility.md` W2 + `arch/substrate.md` §F cross-substrate session/context management) — when first cross-deployment claim ingestion lands, scope-model addresses claim-as-portable-across-Owner-B | Per-shape policy declares cross-deployment claim portability semantics; cross-link: `arch/claim-defensibility.md` §14 W2 + `arch/substrate.md` §F |
| **W3** | Workspace identity persistence schema | Phase 6 spec (per `glossary/workspace.md` Cardinality + `glossary/deployment.md` "Multi-deployment-of-same-workspace patterns" — backup→restore / substrate migration / re-activation) — workspace identity invariants across deployments | Phase 6 spec: workspace identity persistence schema + schema versioning semantics (per E6); cross-link: `arch/practitioner.md` §14 W3 cryptographic signing + `arch/audit.md` §D integrity verification + `arch/claim-defensibility.md` §14 W4 cryptographic signing per claim |
| **W4** | Engagement-target entity catalog per second-shape productization | Second-shape design begins (autonomous-business OR personal-OS productization per BACKLOG shape-neutrality watch-list) — when second shape lands, engagement-target entity for that shape (Customer / Funder / etc.) fully realized | Per-shape policy declares engagement-target entity catalog (per `glossary/owner-b-scope.md` shape-policy-mandated rule); cross-link: BACKLOG "Shape-neutrality validation for second-shape productization" entry |

## 15. Decision-design provenance

Provenance for this topic lives in DR + HANDOFF + git log per `MAINTENANCE.md` Lens 5 v0.2.1 provenance hygiene + per `coherence-audit` Lens 5. See `docs/decisions/scope-model-arch-topic.md` for sharpening trajectory + Round 1 + Round 2 EXPANSIONS + manufactured-criticism rejections + GLOSSARY back-check verdict + profile-anchored validation cluster citations + Mode 2 composite decomposition rationale.

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: scope-model primitives stay shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz) reality (per `profiles/L5a-planner-pbs-schulz.md` lines 76-93 active specialists + active shape practitioner-shape + active substrate Claude Agent SDK + active adapters + Layer A scope domains/states configuration) grounds the workspace-as-integration-point articulation without leaking pioneer specifics into the framework primitive definitions. Cross-archetype illustration in §2 + §3 + §8 anchors framework neutrality (planning bureau / legal practice / research lab / solo creative / knowledge graph / federation node per `glossary/workspace.md` Cross-archetype illustration line 30-37 — 6 archetypes spanning shape-neutrality coverage).

## 16. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.5 | LOCKED |
| Per-scope identity-uniqueness rules + schema versioning semantics (per E6) | 6 | Phase 6 spec; per-scope identity convention may need `version` field for schema evolution |
| Scope-categorization error catalog + recovery semantics (per E7) | 6 | Phase 6 spec; error catalog (invalid framework_kind / orphan owner_scope / Layer A scope-mismatch / cross-deployment scope-resolution failure) |
| Workspace identity persistence schema (per W3) | 6 | Phase 6 spec; cross-link to `arch/practitioner.md` W3 + `arch/audit.md` §D + `arch/claim-defensibility.md` W4 |
| Cross-deployment claim portability scope-model variation (per W2) | 5+ | Per W2 watch-list; awaits first cross-deployment claim ingestion deployment evidence; cross-link to `arch/claim-defensibility.md` W2 + `arch/substrate.md` §F |
| Multi-tenant federation scope-model variation (per W1) | 5+ | Per W1 watch-list; awaits workspace federation surface; cross-link to `arch/practitioner.md` §14 W1 multi-tenant federation |
| Engagement-target entity catalog per second-shape productization (per W4) | 3.5+ | Per W4 watch-list; awaits second-shape design begin signal; cross-link to BACKLOG "Shape-neutrality validation for second-shape productization" entry |
| Per-deployment workspace.md authoring (Mode 1 production-runtime LLM-MD) | Workspace deployment (NOT this repo) | Per `MAINTENANCE.md` TOP-LEVEL SCOPE: per-deployment workspace.md authoring happens at deployment-instance via Mode 1 markdown discipline; Phase 6 deployment |

## 17. Cross-references

- **GLOSSARY**: `Framework C scope` (canonical SCOPE-CLASSIFICATION for distributable definitions); `Owner B scope` (canonical SCOPE-CLASSIFICATION for deployment-specific instances; engagement-target shape-policy-mandated per E4 cross-shape policy variation); `Layer A scope` (canonical SCOPE-CLASSIFICATION for layered content; orthogonal axis); `workspace` (PRIMITIVE cross-cutting; the deployment-instance container integrating all three scopes per §3); `deployment` (DERIVED concept; workspace-as-bound-runtime; 1:1 reciprocal at framework primitive level per W3); `framework` + `mechanism` + `policy` + `shape` (foundational meta-primitives; Framework C derives from `framework = mechanisms`); `protocol-architectural` + `substrate` + `adapter` (Pattern A primitives composing through scope-model per §4); `specialist` + `skill` + `practitioner` + `workflow` + `work-unit` (primitive-cluster primitives composing through scope-model per §4); `claim` (PRIMITIVE; content-unit IN work-unit per E3); `defensibility` + `engaged-authorship` + `category-collapse` + `intertwining` + `sparring` + `authorship-preservation` + `co-worker` + `intertwined-ai` + `tacked-on-ai` + `answer-machine-ai` + `oracle-ai` + `validator-ai` + `rubber-stamping` (DERIVED + axis primitives; cross-cutting non-placed per E4); `authority-binding` (mechanism dual-aspect placement per E5); `actor` + `event` + `session` + `pioneer-instance` (cross-cutting primitives composing through scope-model per §4)
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Framework = mechanisms; Shape = policies" (foundational architectural commitment); "A-B-C scope model" (preliminary-locked three-scope classification); "Atoms vs containers" (mechanism + policy atomic primitives; framework + shape META-PRIMITIVE containers); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (make-wrong-shapes-impossible — structural over conventional discipline applied to scope-categorization through Pydantic gate dispatch on `framework_kind` + `owner_scope` + `layer_scope`); §2 (pattern-vs-instance — scope-model primitives stay shape-neutral / archetype-neutral / pioneer-neutral; cross-archetype illustration anchors framework neutrality across 6 archetypes per `glossary/workspace.md`); §3 (preliminary-lock — A-B-C scope model preliminary-locked per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; revisable when concrete entity-md authoring exercises Phase 3+ reveal mismatches); `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment workspace.md authoring happens at deployment-instance; not framework repo); `ARCHITECTURE.md` §6 cross-cutting principles "AI as runtime" + "LLM-instruction tightness for Mode 1 markdown layer" + "Workspace boot + shutdown composite sequence" subsection (workspace boot integration realizes scope-categories in ordered sequence per E1); `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 4 (cascade-prevention; greenfield-draft + minimize-embedded + cascade-pass + foundation-first); Discipline 7 (cascade discipline structural consistency); Discipline 8 (foundation-up workflow ordering — scope-model is fifth Phase 3.5 ARCH topic + first cross-cutting integrator anchor; LAST per `ARCHITECTURE.md` §5 reading order with axis-interactions remaining); Discipline 10 (greenfield-evaluation of archived sources)
- **Profiles validated**: `G-composability-gate.md` (cross-shape consumption rules + per-shape variation in workspace serialization format + cross-substrate composition rules — validates SD-2 Owner B per-shape engagement-target catalog + SD-5 §8 cross-shape policy variation matrix + W3 workspace identity persistence schema); `L5a-planner-pbs-schulz.md` (PBS-Schulz pioneer concrete deployment surfaces SD-2 active substrate + active adapters + active specialists + Layer A scope domains/states configuration; validates SD-3 workspace integration + SD-4 §4 per-primitive composition narrative); Cluster A producer (L1 specialist creator skeleton fleshed-on-demand for cross-archetype claim production validation per `arch/claim-defensibility.md` SD-3); Cluster B deployer (L4a workspace deployer skeleton fleshed-on-demand for workspace.md integration validation); Cluster C consumer (L5a multi-cluster member; L5d auditor mental-modeling for cross-archetype shape consistency validation); Cluster D validator (G + D gates fired — G transitively-satisfied via specialist's packaging boundary per `arch/specialist-skill.md` §11; D Gate satisfied per W1 + W2 + W3 + W4 awaited evidence)
- **ARCH topics composing with scope-model**: `arch/substrate.md` (Surface tri-aspect Framework C + Owner B placement per E5 substrate parallel; substrate Surface §F session/context for cross-deployment claim portability per W2; substrate-phase 1 boot integration per E1); `arch/audit.md` (mechanism class Framework C Surface + Owner B audit-trail per E5; per-shape audit emission granularity per §14 composes with cross-shape policy variation per §8); `arch/sparring.md` (mechanism class Framework C Surface + Owner B sparring events per E5; per-shape activation matrix per §4 framework-baseline-vs-shape-extension partition composes with §8 cross-shape policy variation); `arch/adapter.md` (Pattern A tri-aspect Framework C + Owner B; multiple adapter Instance bindings per workspace; framework-baseline-vs-shape-extension partition per §3 composes with §8 cross-shape policy variation); `arch/specialist-skill.md` (Pattern B + atomic-primitive bipartite Framework C DEFINITION nests skill / workflow / work-unit-kind / adapter Implementations per E2 nested-bundle pattern + Owner B specialist instance content); `arch/practitioner.md` (Pattern C bipartite — HUMAN cross-cutting NOT placed per E4 + RECORD Owner B workspace-scope managed entity); `arch/workflow-work-unit.md` (two-Pattern-B bipartite — workflow DEFINITION + work-unit KIND DEFINITION nested in specialist's Framework C bundle per E2 + workflow_instance + work-unit instance Owner B); `arch/claim-defensibility.md` (PRIMITIVE+DERIVED — claim content-unit IN work-unit instance per E3 INHERITS work-unit's Owner B placement + defensibility cross-cutting non-placed per E4); `arch/quality-gate.md` (Pattern A 12+7 third instance LOCKED Phase 3.6; FORMAL STABILITY achieved 3 of 3 Pattern A instances — quality-gate Framework C Pattern A + Owner B observability source; gate Implementation Framework C distributable per shape policy bundle declaration; gate Running Instance Owner B 1 active per workspace); `arch/axis-interactions.md` (Phase 3.5 sixth + final ARCH topic LOCKED; second cross-cutting integrator extending scope-model anchor WITHOUT variation — cross-cutting integrator topic-template-class FORMAL STABILITY achieved with second instance lock; scope-model + axis-interactions are parallel cross-cutting integrators — scope-model articulates structural surface (Framework C / Owner B / Layer A scope-categorization across primitives), axis-interactions articulates cross-axis composition surface (axis-1 / axis-2 / axis-3 composition across primitives + their failure-mode dynamics + per-shape activation matrix per `arch/axis-interactions.md` §4.1); orthogonal but complementary articulation; closes Phase 3.5 6 of 6 ARCH topics LOCKED — Phase 3.5 CLOSED)
- **Phase 6 spec target**: `docs/specs/scope-model.md` (per-scope identity-uniqueness rules + schema versioning semantics per E6 + scope-categorization error catalog per E7 + workspace identity persistence schema per W3); `docs/specs/workspace.md` (workspace.md schema; cross-link to `arch/specialist-skill.md` §11 specialist marketplace deferred per W1 + `arch/practitioner.md` §4 multi-practitioner manifest schema)
- **Archived sources**: NONE expected for scope-model — foundations are `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE (preliminary-locked Phase 1.85 + cascade discipline) + `glossary/framework-c-scope.md` + `glossary/owner-b-scope.md` + `glossary/layer-a-scope.md` + `glossary/workspace.md` (locked Phase 2 GLOSSARY foundational vocabulary per `docs/decisions/greenfield-rederivation-pause.md` Step 1.A); not archive territory per `disciplines/10-greenfield-evaluation.md` greenfield-evaluation rule

## 18. Per-primitive composition table

How each already-locked framework primitive's scope placement composes (one row per primitive; columns per scope category):

| Composing primitive | Framework C placement | Owner B placement | Layer A placement | Pattern (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE) |
|---|---|---|---|---|
| **substrate** | Surface (mechanism) + Implementations (distributable definitions per `glossary/substrate.md`) | Implementation Instance running per workspace | N/A | Pattern A (tri-aspect) |
| **adapter** | Surface (META + per-class) + Implementations | Instance bindings per workspace (multiple typically) | N/A | Pattern A (tri-aspect) |
| **sparring** | Surface (8 sub-mechanism contracts) + per-shape activation matrix definitions per shape policy bundle | Sparring events captured in audit-trail at workspace | N/A | Pattern D (mechanism class) |
| **audit** | Surface + AuditEvent schema | audit-trail at workspace (sequence of events; append-only) | N/A | Pattern D (mechanism class) |
| **specialist** | DEFINITION (distributable bundle nesting skill / workflow / work-unit-kind / adapter children per E2 nested-bundle pattern) | Instance content (entities owned within deployed specialist instance) | N/A | Pattern B (bipartite) |
| **skill** | Nested in specialist's Framework C bundle under specialist-namespace per E2 (fully-qualified `specialist-name:skill-name`) | Per-skill events captured in audit-trail at workspace | N/A | atomic within specialist |
| **practitioner** | N/A (HUMAN aspect cross-cutting NOT placed per E4) | RECORD aspect (workspace-scope managed entity per `arch/practitioner.md` §2.2) | N/A | Pattern C (bipartite) |
| **workflow** | DEFINITION nested in specialist's Framework C bundle per E2 (fully-qualified `specialist-name:workflow-name`) | workflow_instance instance per workspace per `arch/workflow-work-unit.md` SD-2 | N/A | Pattern B (bipartite; optional applicability) |
| **work-unit** | KIND DEFINITION nested in specialist's Framework C bundle per E2 (fully-qualified `specialist-name:kind-name`) | work-unit instance per workspace per `arch/workflow-work-unit.md` SD-2 | N/A | Pattern B (bipartite; always-present container) |
| **claim** | N/A | Content-unit IN work-unit instance (INHERITS work-unit's Owner B placement per E3 content-unit-IN-instance pattern) | N/A | PRIMITIVE (atomic content-unit) |
| **defensibility** | N/A | NOT placed per E4 cross-cutting non-placed pattern (resolves at claim granularity through per-claim attribution chain) | N/A | DERIVED (property/test) |
| **engaged-authorship** | N/A | NOT placed per E4 (DERIVED axis-3 success mode; per-claim engagement events captured at Owner B in audit-trail) | N/A | DERIVED (axis-3 success mode) |
| **authority-binding** | Mechanism definition (Framework C per E5 authority-binding placement pattern) | Event recording at Owner B (`actor_kind` + actor identity recorded ON events per `glossary/authority-binding.md` per-event actor declaration sub-aspect) | N/A | PRIMITIVE (mechanism; framework-mechanism) |
| **mechanism** (META) | All mechanism definitions (e.g., AuditEvent schema; `actor_kind` enum; source-grounding capability) | N/A | N/A | PRIMITIVE (atomic interface contract) |
| **policy** (META) | N/A (policy as atom is a configured value within shape's bundle) | N/A | N/A (policies live in shape's policy bundle at Framework C) | PRIMITIVE (atomic configured value within shape) |
| **shape** (META) | Shape definitions (policy bundles) live at Framework C | N/A | N/A | META-PRIMITIVE (container) |
| **framework** (META) | The container of mechanisms + protocols + architectural disciplines per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE | N/A | N/A | META-PRIMITIVE (container) |
| **protocol-architectural** (META) | Pattern A meta-shape; substrate + adapter + quality-gate are PRIMITIVE instances | N/A | N/A | META-PRIMITIVE (Pattern A meta-shape) |
| **session** | N/A | Bounded interaction unit within workspace per `glossary/session.md` (Owner B; substrate-managed) | N/A | PRIMITIVE (bounded interaction unit) |
| **event** | AuditEvent schema definition per `glossary/event.md` (framework-mechanism Layer) | Event records at Owner B (audit-trail) | N/A | PRIMITIVE (audit-emission unit) |
| **actor** | `actor_kind` enum (framework-mechanism per `glossary/actor.md`) | Actor records at Owner B (workspace-scope managed entities per `glossary/actor.md`) | N/A | PRIMITIVE (event-emitter) |
| **workspace** | N/A (workspace is deployment-instance container, NOT distributable definition) | The central Owner B instance + container for workspace-scope managed entities per `glossary/workspace.md` + §3 workspace integration | N/A | PRIMITIVE (deployment-instance container) |
| **deployment** | N/A | DERIVED concept on workspace; 1:1 reciprocal at framework primitive level per `glossary/deployment.md` | N/A | DERIVED (workspace-as-bound-runtime) |
| **pioneer-instance** | N/A | DERIVED meta-concept on workspace; role aspect (orthogonal to deployment runtime-binding aspect per `glossary/pioneer-instance.md`) | N/A | DERIVED (originating deployment role) |
| **category-collapse** | N/A | NOT placed per E4 (cross-axis force; manifests through behavior of placed entities) | N/A | DERIVED (cross-axis force) |
| **intertwining (axis 1)** + **sparring (axis 2)** + **authorship-preservation (axis 3)** | N/A | NOT placed per E4 (cross-cutting concepts; placed primitives serve them) | N/A | DERIVED (VISION axes) |
| **co-worker** + **intertwined-ai** + **tacked-on-ai** + **answer-machine-ai** + **oracle-ai** + **validator-ai** + **rubber-stamping** | N/A | NOT placed per E4 (relational claim + modes + failure modes manifest through behavior of placed entities) | N/A | DERIVED (modes + failure modes) |
| **references / doctypes / bausteine / memory prose / conventions / domain-specific knowledge** | N/A | N/A | Layer A members per `glossary/layer-a-scope.md` Members list (universal / domain / state Layer values per workspace.scope configuration) | (content-class members of Layer A) |
