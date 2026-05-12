# D33 — 2026-05-09 — Identifier graduation + versioning policy (workstream 5)

**Decision**: Two related concerns — graduation of identifiers between core and extension status, and versioning policy for framework artifacts — settled together as workstream 5.

### A. Identifier graduation (extension ↔ core)

Vocabulary values that live in framework-core's enums (capabilities per D17; payload-subtypes per D10; runtime-shapes per D12; actor-subtypes per D9) can move between core and extension status.

**Promotion (extension-registered → core)**

A value proves universal enough that core should own the name.

- **Process**: a supersedes entry on the relevant kind contract adds the value to core's enum.
- **Compatibility (non-breaking)**: existing extensions that already register the value continue to work. Per D29 namespacing, the qualified form `some-ext:mcp-client` and the bare core form `mcp-client` are *structurally distinct identifiers*; they don't collide. Existing extensions don't need to unregister; future extensions and impls naturally adopt the bare core form.

**Demotion (core → extension-registered)**

Already exemplified by D17 (`mcp-client`, `a2a` moved out of D12's core capability list).

- **Process**: a supersedes entry on the relevant kind contract removes the value from core's enum and names a canonical extension that now hosts the registration.
- **Compatibility (potentially breaking)**: instances using the bare form must update to the canonical extension's qualified form. Framework MAY ship a one-version-cycle deprecation alias resolving the bare form to the qualified form during transition; aliasing is implementation policy, not framework-core mandate.

**Source of truth**: a value is "core" iff it appears in a kind contract's enum at framework-core layer 2. The kind contract is the canonical record; supersedes entries on the contract are how graduation happens.

### B. Versioning policy

**Kind contract versioning**

Each kind contract (D7-D20) evolves via the decision ledger. Version bump rules:

- **Major** — breaking slot change (slot removed; type narrowed; semantic-breaking change). Existing impls must update to remain conformant. Migration path declared in the supersedes entry.
- **Minor** — non-breaking slot addition (new optional slot; enum value added — i.e., promotion per §A). Existing impls remain valid.
- **Patch** — clarification only, no slot change.

D23's `work-unit-id` addition to event is a **minor** bump (optional slot added). D17's capability demotion is a **major** bump on D12 (D12's enum narrowed; existing impls advertising `mcp-client` as core need to update).

**Schema versioning** (workstream-3 artifacts) tracks kind contract versioning: schema `$id` URLs MAY include a version path segment; specific scheme is implementation per D11.

**Extension versioning**: per D29, each extension manifest carries a semver-shaped version. Semver semantics apply: major = breaking; minor = additive; patch = clarification.

**Cross-extension version-conflict resolution** (the D32 deferral)

When a workspace's `composition.extensions[]` transitively pulls multiple version-ranges for the same extension dependency:

1. Compute the intersection of all declared ranges for each transitively-required extension.
2. If intersection is empty → boot fails with version-conflict report listing the conflicting ranges + their declarers.
3. If intersection is non-empty → pick the highest version within the intersection that is locally available.
4. If no locally-available version satisfies the intersection → boot fails with version-not-found report.

Algorithm specifics (range-intersection semantics, version-comparison details) are implementation per D11.

### Worked example: a version conflict

Workspace.composition.extensions:

- `pbs-schulz-ext` requires `mcp-protocol-ext` `>=1.0.0 <2.0.0`
- `regulator-shape-ext` requires `mcp-protocol-ext` `>=2.0.0`

Boot:

1. Per D32 §3, dependency graph constructed.
2. Per this D33 §B, range intersection for `mcp-protocol-ext`: `[1.0.0, 2.0.0)` ∩ `[2.0.0, ∞)` = ∅.
3. Validator returns failure: `{category: "version-conflict", extension: "mcp-protocol-ext", conflicts: [{range: ">=1.0.0 <2.0.0", declared-by: "pbs-schulz-ext"}, {range: ">=2.0.0", declared-by: "regulator-shape-ext"}]}`.
4. Boot does not proceed.

### What is NOT in this decision

- **Specific deprecation-alias mechanics** for demotion — implementation per D11.
- **Schema URL version-path scheme** — implementation; could be `/v1/`, `/v2/`, `/2026-05-09/`, etc.
- **Migration-tooling specifics** when major contract bumps require impl updates — implementation.
- **Forward compatibility** (newer instances / impls in older runtimes) — out of scope at framework-core; impl policy.
- **Adding / removing layer-2 kinds** — would re-open D25; out of scope for layer-3 promotion rules.

**Rationale**: per D2 (kinds are abstractions; instances are extensions), graduation is the mechanism by which the boundary between abstraction and instance can shift over time as the ecosystem matures. Per I2, version-conflict resolution must be machine-checkable; intersection-based resolution is mechanical. Per D11, formal-schema and implementation are separate concerns; versioning policy operates at the kind-contract layer (semantic), with schemas tracking (formal), with implementations free to choose URL / file conventions.

Locking these together (rather than splitting) reflects that they're one workstream: graduation is essentially a versioning event (a kind contract bumps when an identifier promotes / demotes); cross-extension version-conflict resolution is the runtime consequence of versioned dependencies. One workstream, one lock.

**Cross-references**: D2 (abstractions vs. instances); D9 + D10 + D12 + D17 (open-vocabulary slots); D11 (formal schema vs. implementation); D14 (decision-ledger discipline; supersedes pattern); D25 (layer 2 closure — kinds fixed); D29 (extension manifest versions); D32 (deferred version-conflict resolution to here).
