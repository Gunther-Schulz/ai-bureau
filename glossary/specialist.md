---
entry: specialist
class: PRIMITIVE
layer: multi-aspect
axis: cross-axis
vision_usage: directly-used
---

# specialist

- **Class**: PRIMITIVE (atomic; the bundled-expertise unit) — **bipartite multi-aspect Pattern B** (DEFINITION in Framework C; INSTANCE-CONTENT in Owner B)
- **Layer**: multi-aspect (Framework C for the distributable definition; Owner B for entities owned by the deployed specialist instance)
- **Axis**: cross-axis (specialists support any axis through their bundled skills + entities + adapters)
- **VISION usage**: directly used (`VISION.md` thesis line 7: "codified expertise bundled as specialists")

**Canonical**: A composable bundle of codified expertise — skills + entities + memory + adapters — distributable as a unit. Bipartite multi-aspect primitive: a specialist's DEFINITION lives at Framework C scope (the distributable bundle); when a workspace activates a specialist, the entities owned by the specialist's instance live at Owner B scope. NOT a Pattern A primitive — a specialist has no multiple interchangeable implementations; it IS its definition.

**What it is**: The cohesion abstraction for codified expertise. A specialist packages everything needed to address a defined competence area into a single distributable unit. Workspaces activate specialists via `workspace.md`'s `specialists_active` field; an activated specialist runs within the workspace's substrate, contributing its skills + entities + memory to the workspace's work output. Specialists are designed to be reusable across workspaces (e.g., `citation-verification` works in legal, research, and planning workspaces); marketplace distribution (per archived ROADMAP v3) treats specialists as the canonical distributable unit.

**Cardinality + lifecycle**: Specialist DEFINITIONS are immutable Framework C distributables. Specialist INSTANCES are activated/deactivated by `workspace.md` `specialists_active` changes; multiple specialists active per workspace simultaneously. Specialist instance content (entities owned by the deployed specialist instance — e.g., bausteine, work-units of the specialist's kind) lives at Owner B as workspace-scope managed entities; **persists across activation/deactivation cycles** (deactivating a specialist doesn't delete its accumulated content; preserves practitioner work). ARCH Layer 3 settles instance-content destruction semantics (deletion-with-audit vs archival; on workspace dissolution).

**What it is NOT**:
- Not a Pattern A primitive — specialist has NO multiple interchangeable implementations (the `planning-document-work` specialist is one specific bundle, not interchangeable with another impl)
- Not a `workspace` — workspaces activate specialists; specialist is one of many elements a workspace activates
- Not a `skill` — skill is the atomic unit of work logic WITHIN a specialist; specialist is the bundle that contains skills
- Not a `practitioner` — practitioner is the human author; specialist is the codified expertise that the practitioner-led workspace deploys
- Not the `framework` — framework provides universal mechanisms; specialist is one Framework C definition among many primitive kinds

**Cross-archetype illustration** (named, archived examples):
- **planning-document-work** — domain-anchored specialist; PBS pioneer reference; bundles skills for B-Plan-Begründung drafting + review
- **citation-verification** — cross-archetype specialist; usable in legal practice (case-law citations), research lab (paper citations), planning bureau (legal-text citations)
- **project-management** — cross-archetype business specialist
- **invoicing** — cross-archetype business specialist (with adapter for accounting integration)
- **brand-voice** — cross-archetype creative specialist
- **legal-research** — legal-practice-anchored specialist

A workspace activates a domain-relevant set: PBS-Schulz might activate `planning-document-work + project-management + invoicing`; Müller Law workspace might activate `legal-research + citation-verification + project-management + invoicing`.

**Boundary test**: Three questions:
1. Is this a unit of work logic that fires on a trigger? → it's a `skill` — within a specialist
2. Is this a deployment scope? → it's a `workspace`
3. Is this codified expertise bundled as a distributable unit? → it's a specialist
4. Disambiguator: is this multiple interchangeable implementations of one Protocol surface? → it's a Pattern A primitive (substrate / adapter / protocol), NOT specialist

**Composes with**:
- [workspace](workspace.md) — workspace activates specialists per `specialists_active` field in `workspace.md`
- [Framework C scope](framework-c-scope.md) — specialist DEFINITIONS live here as distributable bundles
- [Owner B scope](owner-b-scope.md) — specialist INSTANCE-CONTENT (entities owned by the deployed specialist instance) lives here
- [skill](skill.md) — skills are atomic work logic units within a specialist. Skill names scoped under specialist-namespace = specialist-name; fully-qualified skill reference is `specialist-name:skill-name`; prevents cross-specialist skill-name collision (e.g., `planning-document-work:save-baustein` distinct from a hypothetical `legal-research:save-baustein`); cross-specialist skill invocation uses fully-qualified reference
- [mechanism](mechanism.md) — specialists use framework mechanisms (audit emission, source-grounding, sparring) via the substrate at runtime
- [shape](shape.md) — shape policies may mandate certain specialists or constrain what's permitted (e.g., practitioner-shape may mandate sparring-relevant specialists)
- [adapter](adapter.md) — specialists may bundle adapter implementations as part of their package (per locked `adapter` entry)
- [work-unit](work-unit.md) — specialists DEFINE work-unit kinds at work-unit's DEFINITION aspect (kind discriminator + per-kind structural conventions live in specialist DEFINITION at Framework C); workspace's active specialists determine which work-unit kinds are available in that deployment. Two Pattern B primitives composing: specialist + work-unit (specialist DEFINITION holds work-unit kind; work-unit instance lives at Owner B). Work-unit kind names scoped under specialist-namespace = specialist-name; prevents cross-specialist KIND collision (e.g., `legal-research:matter` distinct from `planning-document-work:project`); fully-qualified kind reference is `specialist-name:kind-name`.
- [workflow](workflow.md) — specialists DEFINE workflow patterns (workflow definitions live in specialist's distributable bundle at Framework C; workflow inherits Framework C placement via specialist composition rather than as standalone framework primitive). Workflow definition names scoped under specialist-namespace = specialist-name; prevents cross-specialist workflow-name collision; fully-qualified workflow reference is `specialist-name:workflow-name`.

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "A workspace pools and leverages codified expertise (bundled as specialists)"
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)" — implies specialists deploy to multiple shapes
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Other multi-aspect primitives": specialist named as Pattern B (bipartite definition+instance-content)
- Locked GLOSSARY entries: [Framework C scope](framework-c-scope.md) (members include specialist DEFINITIONS); [Owner B scope](owner-b-scope.md) (members include specialist instance content)

**See**:
- [Framework C scope](framework-c-scope.md) (where specialist definitions live)
- [Owner B scope](owner-b-scope.md) (where specialist instance content lives)
- [workspace](workspace.md) (which activates specialists)
- ARCH Layer 3 specialist-detail topics (placeholder until Phase 3 — specialist granularity 3-test, composability axes, two-tier classification, marketplace mechanics; archived material to consult: `terminology-and-specialist-primitive.md`, `entity-md-scope-model-restructure.md`)
