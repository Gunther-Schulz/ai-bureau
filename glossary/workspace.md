---
entry: workspace
class: PRIMITIVE
layer: cross-cutting
axis: cross-axis
vision_usage: directly-used
---

# workspace

- **Class**: PRIMITIVE (atomic; the deployment-instance unit)
- **Layer**: cross-cutting (workspace integrates framework mechanisms + shape policies + practitioners; orthogonal to mechanism/policy split per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- **Axis**: cross-axis (workspace is the container in which all three VISION axes manifest)
- **VISION usage**: directly used (`VISION.md` thesis line 7 + cross-archetype examples throughout)

**Canonical**: The deployment-instance container that integrates framework mechanisms + shape policies + active specialists + practitioners + state into a coherent unit for accountability-bearing work; selects exactly one shape via its `workspace.md`; lives at Owner B scope.

**What it is**: The top-level deployment primitive — what gets bound when a practitioner deploys PBS for their work. A workspace is the central Owner B instance: its `workspace.md` selects shape + substrate + active specialists; its workspace-scope managed entities (practitioner-record, Actor, plus shape-policy-mandated engagement-target entities like `Client` in practitioner-shape, `Customer` in autonomous-business-shape, etc. — engagement-target entities are deliberately shape-policy-mandated rather than framework-level) live at Owner B; its layered content (references, doctypes, bausteine per Layer A) varies by domain/state context (configured via workspace's `scope.{domains, states}`).

**Cardinality**: exactly 1 workspace ↔ 1 active deployment at framework level (per `deployment` entry — deployment = workspace-as-bound-runtime; 1:1 reciprocal). Multi-environment scenarios (dev / staging / prod) = N workspaces (each its own deployment). Multi-tenant scenarios (one substrate hosting multiple workspace runtimes) = substrate-Instance-level concern, not framework-level cardinality concern. Workspace IDENTITY can persist across multiple deployments over time (backup→restore, substrate migration, re-activation) — workspace identity is workspace-portability concern (Phase 6 spec); deployment count is the runtime binding count.

**What it is NOT**:
- Not the `framework` — framework is the universal mechanism layer (what's POSSIBLE); workspace is one deployment instance built from framework + shape policies
- Not a `shape` — shape is the policy-bundle archetype (definition; lives in Framework C); workspace is an instance that SELECTS exactly one shape
- Not a `specialist` — specialist is composable expertise; workspace ACTIVATES specialists from the list in `workspace.md`
- Not a `session` — sessions are bounded interaction units WITHIN a workspace
- Not a single application running on a server — deployment-shape-agnostic (could be local, cloud, hybrid); not synonymous with "office" (prior naming, demoted; workspace is broader)

**Cross-archetype illustration**:
- Planning bureau: "PBS-Schulz workspace"
- Legal practice: "Müller Law workspace"
- Research lab: "Smith Lab workspace"
- Solo creative: "Anna's Writing workspace"
- Knowledge graph: "BNatSchG knowledge workspace"
- Federation node: "Federation X workspace"

All workspaces are built from the same framework; they differ in selected shape (which configures policies), active specialists, and Layer A content per their domain/state scope.

**Boundary test**: ask "what's the deployment scope of this work?" The answer names a workspace.
- If answer is "a single feature" → it's a skill or specialist, not a workspace
- If answer is "the open-source product" → it's the framework, not a workspace
- If answer is "a configuration archetype" → it's a shape, not a workspace
- If answer is "a particular bounded interaction" → it's a session, not a workspace

**Composes with**:
- [shape](shape.md) — workspace selects exactly one shape via `workspace.md` (the shape's policy bundle configures workspace's behavior over framework mechanisms)
- [framework](framework.md) — workspace inherits framework's mechanisms; the selected shape's policies determine which are active/mandatory and what defaults apply
- [Owner B scope](owner-b-scope.md) — workspace lives as the central instance + container for workspace-scope managed entities (practitioner-record, Actor, Client)
- [specialist](specialist.md) — workspace activates a list of specialists per `specialists_active` field in `workspace.md`
- [practitioner](practitioner.md) — workspace serves practitioner(s); records at Owner B (bipartite primitive: human cross-cutting, record at Owner B)
- [substrate](substrate.md) — workspace runs on exactly one substrate (selected via `workspace.md` `substrate` field)
- [session](session.md) — interaction units occur within a workspace
- [workflow](workflow.md) — workspaces SUPPORT workflows; workspace's deployed specialists + state + active substrate enable workflow progression (axis-1 intertwining requires workflow to embed in); workflow_instance entities live at Owner B as workspace-scope managed entities (when codified pattern applies; ad-hoc work-units have no workflow_instance). Capability addition (adding specialist / configuring adapter / activating skill mid-flight) is workspace-scope and orthogonal to running workflow_instance state — workflow_instance doesn't gate capability changes; workspace governance (authority binding) gates them in multi-user contexts.
- [authority-binding](authority-binding.md) — workspace governance (multi-user contexts; capability-change moments; workflow phase transitions) composes with authority-binding mechanism; per-shape policy declares trust model parameterizing how authority-binding satisfies workspace-level accountability requirements
- [work-unit](work-unit.md) — workspaces CONTAIN work-units as workspace-scope managed instances (cardinality multiple per workspace); kinds defined by active specialists
- [Layer A scope](layer-a-scope.md) — workspace's `scope.{domains, states}` configuration determines which Layer A content (references, doctypes, bausteine) applies
- [deployment](deployment.md) (DERIVED) — workspace's runtime-binding aspect; 1:1 reciprocal at framework level; workspace = entity (configuration view), deployment = relation (runtime view); workspace identity may persist across multiple deployments over time

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "A workspace pools and leverages codified expertise (bundled as specialists) to automate and support interactive practitioner workflows in a coherent manner"
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Multiple cross-archetype examples throughout
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Cross-cutting" classification (workspace listed as cross-cutting alongside practitioner, session, workflow)

**See**:
- [Owner B scope](owner-b-scope.md) (where workspace itself + workspace-scope managed entities live)
- [shape](shape.md) (what workspace selects)
- [Layer A scope](layer-a-scope.md) (content scoping per workspace's domain/state configuration)
- ARCH Layer 3 workspace-detail topics (placeholder until Phase 3 — `workspace.md` schema; multi-practitioner workspace; legal-entity workspace context; deployment configurations)
