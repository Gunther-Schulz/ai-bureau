# DR: deployment-derived-classification (workspace-as-bound-runtime)

**Status**: ACCEPTED (Phase 3.1 lock; resolves workspace Cardinality field hedge)
**Date**: 2026-05-02

## Decision

`deployment` is locked as **DERIVED concept** = workspace-as-bound-runtime (binding-act-aspect of workspace).

- **Class**: DERIVED (perspective on workspace; not standalone primitive)
- **Layer**: framework-meta (operates on workspace + framework without being one)
- **Cardinality**: 1:1 with workspace at framework primitive level
- **Vocabulary distinction**: `workspace` = entity (configuration view); `deployment` = binding-relation (runtime view); both describe same primitive object from different angles
- **Workspace identity** can persist across multiple deployments over time (backup→restore, substrate migration, re-activation) — workspace identity is workspace-portability concern (Phase 6 spec); deployment count is the runtime binding count

## Context

`workspace` GLOSSARY entry locked Phase 2 with Cardinality field carrying explicit hedge: "current preliminary lock is 'one git-cloned + activated workspace.md per deployment.'" The hedge was operational (mechanism-shaped) rather than concept-shaped, and "deployment" was used pervasively across locked entries (`pioneer instance`, `Layer A scope`, `Owner B scope`, `workspace`) without canonical definition.

The question: is `deployment` a separate primitive, a derived concept, or vocabulary to retire?

Pervasive usage across locked entries (always in sense of "workspace-as-bound-runtime") signaled DERIVED-class treatment. Round 1 + Round 2 sharpening confirmed.

## Adoption options considered

- **A (CHOSEN)**: `deployment` = DERIVED concept; binding-act-aspect of workspace; 1:1 cardinality at framework level
- **B**: `deployment` = separate PRIMITIVE distinct from workspace (would imply N workspaces per deployment OR N deployments per workspace; no structural content surfacing to motivate primitive-ness)
- **C**: Retire `deployment` vocabulary entirely; use `workspace` everywhere (rejected — pervasively load-bearing in existing entries; cascade rewrite cost without semantic gain)

## Rationale for A

**Pervasively used in locked entries always in same sense**: workspace-as-bound-runtime perspective. No surfacing usage motivates separate primitive.

**No independent structural content**: deployment introduces no separate cardinality, lifecycle, observability surface, or attributes beyond workspace's runtime aspect. Lifecycle = workspace runtime lifecycle; events emit at workspace level; no separate Surface to extract.

**Vocabulary utility preserved**: entity-vs-relation framing useful for discussing runtime concerns (deployment) vs configuration concerns (workspace). DERIVED entry captures this without inflating primitive count.

**Pattern matches `pioneer instance`**: pioneer instance is also DERIVED (role-aspect of workspace). Both are perspectives on workspace; orthogonal (one workspace can be both simultaneously).

## Refinements applied (Round 2 expansions)

| ID | Refinement | Status |
|---|---|---|
| E1 | Software-industry "deployment" (generic act of pushing code to environment) vs PBS-specific (workspace-as-bound-runtime) — disambiguation | Applied to What-it-is-NOT |
| E2 | Snapshot/restore semantics: backup→restore creates NEW deployment of SAME workspace (workspace identity preserved) | Applied to lifecycle |
| E3 | Substrate migration semantics: workspace migrating substrate-A → substrate-B = old deployment terminates + new deployment activates with same workspace identity | Applied to lifecycle |
| E4 | Orthogonality with `pioneer instance`: both DERIVED on workspace; orthogonal facets (deployment = runtime-binding aspect; pioneer instance = role aspect); one workspace can be BOTH simultaneously | Applied to Composes-with (both entries) |
| E5 | Lens 6 reciprocal: workspace's "exactly 1 workspace per deployment" needs cross-ref to deployment entry | Applied to workspace entry |
| E6 | Multi-environment / multi-instance taxonomy (dev/staging/prod; backup/recovery; CI/test) — all surface as N deployments in framework-primitive terms; workspace identity portability is Phase 6 concern | Applied to Cardinality |
| E7 | Quality-gate observability: deployment lifecycle events emit at workspace level (workspace_activated / workspace_decommissioned); no separate event stream | Applied to What-it-is-NOT |
| E8 | Entity-vs-relation framing: workspace = entity (container shape); deployment = binding-relation (act shape); both describe same primitive from different angles | Applied to Canonical (justifies keeping vocabulary vs Option C collapse) |

## REVISION-grade stress-tests

| ID | Test | Verdict |
|---|---|---|
| **R1** | Retire `deployment` entirely (Option C); use `workspace` everywhere | **REJECTED** — pervasively load-bearing in `pioneer instance`, `Layer A scope`, `Owner B scope`, `workspace`. Retiring forces wide cascade rewrite without semantic gain. DERIVED entry preserves utility + saves cascade work. |
| **R2** | Class deployment as SCOPE-CLASSIFICATION (parallel to Framework C / Owner B / Layer A) | **REJECTED** — scope-classification is for entity placement category; deployment is a binding-act perspective. Wrong shape. |
| **R3** | Class deployment as Pattern A protocol (variation per shape — practitioner-shape-deployment vs autonomous-business-deployment) | **REJECTED** — deployment-shape variation = workspace-shape variation (workspace selects shape; deployment inherits via 1:1). No independent Surface to extract. |

## Composition with existing architecture

| Existing primitive | Composition |
|---|---|
| `workspace` (PRIMITIVE) | 1:1 reciprocal at framework level; deployment IS workspace's runtime aspect |
| `substrate` (Pattern A protocol) | Deployment binds against exactly one substrate Instance (workspace selects substrate via `workspace.md`; deployment activates the binding) |
| `pioneer instance` (DERIVED) | Orthogonal DERIVED concept; deployment = runtime-binding aspect, pioneer instance = role aspect; one workspace can be BOTH simultaneously |
| `Layer A scope` | "deployment context" reads as workspace's bound runtime per workspace's `scope.{domains, states}` configuration |
| `Owner B scope` | "deployment-specific entities" = workspace-bound entities at Owner B (workspace-scope, specialist-instance-scope, work-unit-instance-scope) |
| `framework + shape` | Deployment is the act of binding `framework + shape → workspace deployment` (per `Owner B scope` derivation) |

## Defers (D-gate-validated; Phase 6 spec territory)

| Defer | Awaited signal | Reason valid |
|---|---|---|
| Workspace-identity invariants across deployments (what defines "same workspace" across backup→restore / substrate migration / re-activation) | Phase 6 spec (state serialization + identity invariants) | Schema-detail; conceptual decision (1:1 cardinality with persistent identity) settled at this DR |
| Substrate migration mechanics (live migration vs cold migration; state snapshot semantics) | Phase 6 + per-substrate Instance technical mechanics | Implementation-specific |
| Multi-tenant substrate-Instance patterns (one substrate hosting N workspace runtimes) | Per-substrate technical configuration; not framework-level | Substrate-Instance concern |
| Workspace-portability backup-restore protocols | Phase 6 spec (state serialization + portability) | Implementation-specific |

D Gate verdict: all defers genuine schema-detail (HOW), not architectural-decision (WHAT). All defers valid.

## Constraints flowing

This decision flows constraints into:
- **Phase 3.5** primitive-detail topics (workspace-mechanics ARCH topic includes deployment-runtime considerations; pioneer instance + deployment cross-cuts)
- **Phase 6** workspace serialization spec (workspace-identity invariants across deployments; backup→restore deployment cardinality; substrate migration semantics)
- **Phase 3.4** per-architectural-Protocol detail (substrate Pattern A composition with deployment binding)

## Files touched

- `GLOSSARY.md` deployment entry (NEW; DERIVED entry with full anatomy)
- `GLOSSARY.md` TOC §8 Meta concepts (deployment added before pioneer instance)
- `GLOSSARY.md` workspace Cardinality field (replaced operational hedge with reciprocal cross-ref to deployment entry)
- `GLOSSARY.md` workspace Composes-with (deployment cross-ref added)
- `GLOSSARY.md` pioneer instance Composes-with (orthogonal-DERIVED cross-ref added)
- `ARCHITECTURE.md` Locked architectural decisions section (deployment lock entry added)
- `ARCHITECTURE.md` Phase 3 sub-phase status table (3.1 deployment LOCKED)
- `BACKLOG.md` Phase 3.1 (deployment definition sharpening → Resolved)
- `docs/decisions/deployment-derived-classification.md` (this file)

## Revisit triggers

This DR should be revisited if:
- Phase 6 workspace serialization spec surfaces operational concerns the 1:1 cardinality can't accommodate
- Multi-tenant patterns require framework-level (not just substrate-Instance-level) treatment
- Federation second-deployment work surfaces deployment semantics differing structurally from current 1:1 framing
- New shape (cloud-shape; multi-org-shape) requires framework-level cardinality variation

## Sharpening rounds metadata

- **Round 1**: AI full monty — 3 adoption options + 10 stress tests + position committed (Option A: DERIVED concept = workspace-as-bound-runtime)
- **Round 2**: USER-TRIGGERED — 8 EXPANSIONS applied (E1-E8) + 3 REVISION-candidates rejected (R1-R3 manufactured criticism)
- **Self-check**: STABLE; 0 architectural REVISIONS; all findings EXPANSIONS
- **Multi-axis validation discriminator** (per decision-design-sharpening v0.5.0): shape-specific surface present (federation / multi-tenant / multi-environment) → profile-anchored validation fired (Cluster B deployers + Cluster A producers + Cluster C consumers + federation profile mental modeling — all confirm 1:1 cardinality at framework level)
- **GLOSSARY back-check** (per v0.5.0 + MAINTENANCE.md Bidirectional cascade): the decision IS itself glossary work; EXPANSIONS surfaced went directly into the new entry. No retro-fit gap.

Total: 2 rounds. Per `DISCIPLINES.md` Discipline 3 2-round sweet spot empirical pattern. Narrow architectural surface (single DERIVED concept lock + cardinality cleanup) → 2 rounds sufficient.
