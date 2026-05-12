# D12 — 2026-05-08 — Substrate kind

**Decision**: The substrate kind contract specifies what hosts the agent loop and exposes interfaces (capabilities) for other extensions to hook into. A workspace's manifest declares substrate-bindings (per D7) that resolve to substrate impls conforming to this contract.

### Contract slots

- **`id`** — stable identifier for this substrate (e.g., `claude-agent-sdk`).
- **`version`** — version designator (range-comparable for binding resolution; semver-shaped at layer-3 formal schema).
- **`capabilities[]`** — what interfaces the substrate exposes for other extensions to hook into. Hybrid vocabulary: framework-core declares a core set; extensions may register additional capabilities.
- **`runtime-shapes[]`** — which interaction modes the substrate supports: `interactive`, `programmatic`, `hosted-interactive`, `hosted-programmatic`. Open vocabulary; extensions may register additional shapes. A substrate may declare multiple shapes; each binding selects exactly one.

### Core capability vocabulary (framework-declared)

Framework-core declares only capabilities that *core kinds* depend on:

- **`mcp-client`** — substrate can be an MCP client (required by adapter kind for adapters that speak MCP).
- **`hooks`** — substrate exposes hook points for shape policies / discipline enforcement (required by shape kind for shapes that need pre/post-event policy hooks).
- **`skills`** — substrate can load specialist bundles as skills (required by specialist kind).
- **`event-streaming`** — substrate emits events the workspace state can capture (required by event kind per D10).
- **`a2a`** — substrate can speak A2A protocol (required by adapter kind for agent-to-agent adapters).

Other capabilities (`computer-use`, `cross-app-workflows`, `audit-via-purview`, `opentelemetry`, `parallel-tool-calls`, etc.) are extension-registered, not framework-required. The principle: framework-core declares a capability iff a core kind depends on it.

### Single kind; no subtypes

Substrate is a single kind. Variations sometimes imagined as subtypes (interactive vs programmatic vs hosted) are captured in `runtime-shapes[]` rather than kind subtypes — this avoids forced parallel hierarchies for what are really declarative facets.

### Binding resolution

A workspace's substrate-binding (per D7 §4 cardinality) may reference a substrate by:
- **specific identity**: `id` + `version-range` (e.g., `claude-agent-sdk @ ">=2.0"`)
- **capability requirements**: a list of required capabilities; runtime resolves any conforming substrate
- **mixed**: capability requirements + preferred substrate

Each binding selects exactly one runtime-shape. Multiple bindings of the same substrate (different runtime-shapes) are allowed — e.g., a workspace with `bind-primary: claude-agent-sdk@interactive` for daily work and `bind-scheduled: claude-agent-sdk@programmatic` for cron tasks.

### Capabilities as interfaces (boot semantics)

A substrate's capabilities are **interfaces other extensions hook into**, not just feature flags. When a workspace boots:

1. Host process loads the substrate (per the binding's id + version + runtime-shape).
2. Substrate provides runtime + exposes its declared capabilities as interfaces.
3. Workspace registers adapters into the substrate's `mcp-client` capability; specialists into `skills`; shape policies into `hooks`; events flow through `event-streaming` into the workspace event chain (per D10).
4. Agent loop runs; everything operates via substrate's exposed interfaces.

A substrate that lacks a capability required by another bound extension cannot host that composition. The framework validates this structurally per I2 at boot.

### D9 refinement (implicit but worth noting)

Per D9, an `agent-actor` declares `substrate-binding`. With a workspace possibly having multiple bindings of the same or different substrates, that reference resolves to a **specific binding-id within workspace.composition**, not just a substrate-id. This refinement is consistent with D9's wording; it just makes the resolution target precise.

### Concrete example (illustrative only; not part of core)

Three substrates with different capabilities and runtime-shapes — Claude Agent SDK supporting `[interactive, programmatic]`, Claude Cowork supporting `[hosted-interactive]`, MS Agent Framework supporting `[programmatic, hosted]` — and a workspace binding the same SDK twice with different runtime-shapes (interactive for daily work; programmatic for scheduled tasks). Worked through in discussion that produced this decision.

### What is NOT in the substrate kind contract

- Specific tool implementations → adapter kind.
- Specific skills / specialists loaded → specialist kind.
- Authentication configuration → implementation.
- Deployment / hosting target → implementation.
- Singletonness → a substrate may have multiple bindings within one workspace.
- **Formal protocol semantics** for each capability (e.g., the precise interface shape of `hooks`) → layer 3 / formal schema. At layer 2, we declare *that* the capability exists; layer 3 specifies its formal interface.

**Rationale**: substrate is the kind that hosts the agent loop and provides the runtime interfaces other extensions hook into. Per I1 (composition), the framework needs a defined kind for "where compositions execute"; per I2 (machine-checkable contracts), capability declarations let core validate that a substrate can host a given workspace's other bindings; per I3 (accountability), `event-streaming` connects substrate-level happenings to the workspace's event chain.
