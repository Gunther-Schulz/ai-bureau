---
entry: deployment
class: DERIVED
layer: framework-meta
axis: cross-axis
vision_usage: implicit
---

# deployment

- **Class**: DERIVED (perspective on `workspace`; not standalone primitive)
- **Layer**: framework-meta (operates on workspace + framework without being one)
- **Axis**: N/A — deployment is a binding-act perspective; axes operate within deployments, not on them
- **VISION usage**: implicit (VISION's cross-archetype practitioner workspaces all imply deployments; not directly named as separate term)

**Canonical**: The binding-act-aspect of `workspace` — workspace viewed as bound runtime (the active runtime instance produced when a workspace's configuration is activated against a substrate Instance). 1:1 with workspace at framework primitive level. Where `workspace` emphasizes the entity (container shape: selects shape, activates specialists, holds state), `deployment` emphasizes the binding-relation (act shape: workspace + substrate Instance + activated `workspace.md` configuration = one running deployment).

**What it is**: The runtime-binding view of a workspace. When a practitioner activates their workspace (substrate process running, `workspace.md` loaded, specialists initialized, state accessible), that bound runtime IS a deployment. The same workspace, decommissioned and re-activated later, becomes a new deployment of the same workspace identity. The same workspace, restored from backup onto fresh substrate, becomes a new deployment of the same workspace identity. The same workspace, migrated from substrate-A to substrate-B, terminates one deployment and activates a new one — workspace identity preserved across deployments.

**Entity-vs-relation framing**: `workspace` = entity (container shape — has attributes, lifecycle, contained instances). `deployment` = binding-relation (act shape — names the active runtime binding). Both describe the same primitive object from different angles; the vocabulary distinction is useful when discussing runtime concerns (deployment) vs configuration concerns (workspace).

**Cardinality**: 1:1 with workspace at framework primitive level — exactly 1 deployment per workspace at any moment of active runtime; sequence of deployments over a workspace's identity lifetime (each activation = one deployment; decommission ends it; re-activation begins a new one). Multi-environment scenarios (dev / staging / prod) are N workspaces (each its own deployment), not 1 workspace with N deployments. Multi-tenant scenarios are substrate-Instance-level concerns (one substrate hosting multiple workspace runtimes); each hosted workspace is its own deployment at framework level.

**Lifecycle**: deployment lifecycle ≈ workspace runtime lifecycle (activated → active → decommissioned). No independent lifecycle to motivate primitive-ness. Lifecycle events (activation, decommission) emit as workspace events (workspace_activated / workspace_decommissioned); deployment doesn't have separate event stream.

**Multi-deployment-of-same-workspace patterns** (workspace identity preserved across deployments):
- **Backup → restore**: workspace state restored onto fresh substrate = new deployment of same workspace identity
- **Substrate migration**: workspace migrating from substrate-A to substrate-B = old deployment terminates + new deployment activates with same workspace identity
- **Disaster recovery**: recovery deployment = restored workspace from backup; separate runtime = separate deployment; workspace identity preserved
- **Re-activation after decommission**: same workspace re-activated = new deployment, same identity

Workspace IDENTITY across deployments is workspace-portability concern (Phase 6 spec territory: state serialization + identity invariants). Deployment count is the runtime binding count.

**What it is NOT**:
- Not a standalone primitive — derived from workspace + substrate Instance binding; no independent structural content
- Not a separate scope category — Framework C / Owner B / Layer A are scope-classification primitives for entity placement; deployment is a binding-act perspective
- Not a Pattern A protocol — deployment-shape variation = workspace-shape variation (workspace selects shape; deployment inherits via 1:1); no independent Surface to extract
- Not the same as software-industry generic "deployment" (act of pushing code/config to environment) — PBS-specific usage means workspace-as-bound-runtime; tightened from generic usage
- Not a separate observability surface — lifecycle events emit at workspace level; quality-gate observability flows through workspace, not through deployment-as-separate-source

**Cross-archetype illustration**: every locked workspace illustration is also a deployment illustration. PBS-Schulz workspace = PBS-Schulz deployment. Müller Law workspace = Müller Law deployment. Federation node X workspace = Federation node X deployment. The vocabulary chosen depends on emphasis (configuration discussion → workspace; runtime discussion → deployment).

**Boundary test**: ask "are we discussing the active runtime binding or the entity-shaped container?"
- Runtime binding (active substrate + loaded config + initialized specialists + accessible state) → deployment
- Entity-shaped container (selects shape; activates specialists; contains work-units) → workspace
- Configuration document → `workspace.md` (the file)
- Static structural placement → check `Framework C` / `Owner B` / `Layer A` scope entries

**Composes with**:
- [workspace](workspace.md) — 1:1 at framework primitive level; deployment IS workspace's runtime aspect
- [substrate](substrate.md) — deployment binds against exactly one substrate Instance (workspace selects substrate via `workspace.md`; deployment activates that selection)
- [pioneer instance](pioneer-instance.md) — orthogonal DERIVED concept on workspace; deployment = runtime-binding aspect, pioneer instance = role aspect; one workspace can be BOTH simultaneously (PBS-Schulz workspace IS one deployment at any moment AND IS pioneer instance role)
- [Layer A scope](layer-a-scope.md) — Layer A content "applies in deployment" = applies in workspace's bound runtime per workspace's `scope.{domains, states}` configuration
- [Owner B scope](owner-b-scope.md) — "deployment-specific entities" = workspace-bound entities at Owner B (workspace-scope, specialist-instance-scope, work-unit-instance-scope)
- `framework + shape` — deployment is the act of binding `framework + shape → workspace deployment` (per `Owner B scope` derivation): framework provides mechanisms; shape provides policies; workspace selects shape; deployment is the runtime activation of that selection

**Source**:
- Locked GLOSSARY entries: [workspace](workspace.md) Cardinality field hedge ("current preliminary lock is 'one git-cloned + activated workspace.md per deployment'"); [pioneer instance](pioneer-instance.md) ("originating **deployment** of a framework"); [Layer A scope](layer-a-scope.md) ("**deployment** context"); [Owner B scope](owner-b-scope.md) ("**deployment**-specific entities")
- Synthesis: DERIVED-classification resolves the workspace Cardinality hedge; deployment is workspace-as-bound-runtime perspective with 1:1 cardinality at framework level; multi-environment / multi-tenant patterns resolve at workspace-count or substrate-Instance level, not at deployment-cardinality level

**See**:
- [workspace](workspace.md) (the entity primitive deployment is the runtime aspect of)
- [substrate](substrate.md) (Pattern A protocol whose Instance deployment binds against)
- [pioneer instance](pioneer-instance.md) (orthogonal DERIVED concept)
- [Owner B scope](owner-b-scope.md) (where deployment-specific entities live)
- [Layer A scope](layer-a-scope.md) (which scopes content per deployment context)
- `arch/scope-model.md` (Phase 3.5 first cross-cutting integrator LOCKED — §3 workspace integration "1:1 reciprocal cardinality with deployment" (1 workspace ↔ 1 active deployment at framework primitive level; multi-environment scenarios = N workspaces; multi-tenant scenarios = substrate-Instance-level concern); workspace identity persistence across multiple deployments over time per "Multi-deployment-of-same-workspace patterns"; §14 W3 workspace identity persistence schema watch (Phase 6 spec — workspace identity invariants across substrate migration / backup-restore / re-activation))
