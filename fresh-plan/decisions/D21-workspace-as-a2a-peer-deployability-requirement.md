# D21 — 2026-05-08 — Workspace-as-A2A-peer deployability requirement

**Decision**: A deployed workspace must be exposable as an A2A peer when the deployment chooses A2A exposure. This is a load-bearing requirement on the framework's extensibility — framework-core kinds must support this composition pattern, even though the A2A protocol itself is extension territory (per D2 + D17).

### What this requires from framework-core

- Specialist `skills[]` declarations (per D19) carry enough metadata to map to A2A agent-card skill entries (name, description, input / output modalities). Verified at refinement pass via D15's standards-compatibility check.
- Workspace lifecycle (per D7 §4) supports A2A-peer-endpoint serving: boot binds the A2A peer adapter; adapter publishes agent-card; shutdown unpublishes.
- Shape authority-bindings (per D13) compose coherently with A2A peer authentication / authorization.
- Cross-process attribution flows through `agent-actor` (peer agents registered as actors per D9) + event chain (per D10), with peer interactions captured as events.

### What this requires from extensions

- **A2A peer adapter** (an instance of the adapter kind per D16): aggregates skills from loaded specialists into an agent-card; serves the agent-card at the well-known URL (e.g., `/.well-known/agent.json`); routes incoming A2A task requests to appropriate specialist skill invocations; translates results into A2A task responses.
- **A2A protocol extension** (extension-registered protocol identifier `a2a-peer`): defines the formal mapping between framework-core primitives (specialist skills, work-units, events, actors) and A2A protocol primitives (agent-card skills, tasks, messages, agents).
- **Per-skill exposure control**: specialist skills may need a publicly-exposed flag (or an explicit publish-list at adapter binding time) so internal-only skills don't leak into the agent-card. Specific mechanism = layer-3 formal schema; named here as a requirement.

### Generalization beyond A2A (MCP-server exposure parallel)

The parallel pattern for MCP — *workspace-as-MCP-server* (specialist skills exposed as MCP tools to external AI clients) — is similarly supported by the framework's extension architecture but is separate from this entry's scope. The refinement pass per D15 should verify the MCP-server-exposure mapping with the same rigor as A2A-peer mapping.

Both expose-patterns share the underlying requirement: *the workspace's specialists' skills are externally addressable via standards-conformant protocols*. The framework must enable this without baking either standard into core.

### Verification target for refinement pass (per D14 + D15)

The pass verifies:
- Specialist's skill declaration metadata is sufficient for clean agent-card mapping (no information loss).
- Workspace boot / shutdown lifecycle correctly binds / unbinds the A2A peer adapter.
- A2A peer auth integrates coherently with shape authority-bindings.
- Per-skill exposure control mechanism is well-defined.
- Cross-process actor attribution (peer agents in this workspace's actor registry) flows correctly.

### Why this matters (load-bearing rationale)

- **Cross-vendor interop**: PBS workspaces accessible to peer agents on Cowork, MS Agent Framework, Google ADK, LangGraph, CrewAI, LlamaIndex, Semantic Kernel, AutoGen — the universal A2A-adopting ecosystem in 2026.
- **Federation pathway**: workspaces can collaborate as peers without bespoke protocols. Multi-workspace federation (deferred per D7 + D9) gets a standards-based foundation.
- **Regulatory alignment**: A2A is converging with EU AI Act / governance frameworks for cross-vendor agent identity + collaboration audit (per D15 candidates including PROV-O, DID, VC).

### Caveat

The requirement applies to deployments that *choose* A2A exposure. Not every workspace must be A2A-exposed; this is deployment policy. The requirement is that the framework's design **supports it cleanly when chosen** — the framework neither forces A2A on every deployment nor makes A2A exposure a second-class extension.

**Rationale**: per D15's standards-compatibility criterion, specific compatibility targets need to be load-bearing requirements (not just verified at refinement). A2A-peer exposure is the most directly load-bearing because it's how a workspace participates in the cross-vendor agent ecosystem. Naming it as a requirement makes it a design constraint that informs the refinement pass + the layer-3 formal-schema work for specialist + workspace + adapter kinds.
