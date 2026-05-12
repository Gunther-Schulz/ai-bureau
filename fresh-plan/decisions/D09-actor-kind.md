# D9 — 2026-05-08 — Actor kind

**Decision**: The actor kind contract specifies an attribution-bearing participant in a workspace. Cardinality: 1+ per workspace (per D7); each actor has stable workspace-scoped identity and a subtype.

### Contract

- **`id`** — stable unique identifier within the workspace. Persists across substrate restarts, across runtime episodes, across the workspace's full lifecycle. Identity is workspace-scoped (not cross-workspace; cross-workspace coordination is out of scope for this kind).
- **`subtype`** — one of `human-actor`, `agent-actor`. Subtypes are open (other subtypes can be added as needed in future decisions).
- **Subtype-specific metadata** (kind-level structural slots; semantics not enforced by framework-core):
  - `agent-actor`: **`substrate-binding`** referencing a substrate declared in workspace.composition. The actor's runtime resolves through that substrate.
  - `human-actor`: **`declared-name`** (or equivalent free-form designation).

### Identity persistence (illustrative)

- Substrate restart → same actor (substrate session is not actor identity).
- Model version upgrade for an agent-actor → same actor (model version is metadata, captured in individual events; not actor identity).
- Same workspace running on a different substrate (per workspace.substrate-binding capability resolution) → same actors (actor identity is workspace-level, not substrate-level).
- Actor granularity is a workspace-level decision: one substrate may host multiple distinct agent-actors (e.g., interactive `claude-primary` vs cron-driven `claude-monthly-invoicing`); the workspace decides where actor boundaries fall, not the substrate.

### Linkage to events

Per D7 §3, every event has at least one actor. Per the actor kind: events reference actors by `id`, and the framework validates structurally (per I2) that referenced actor `id`s exist in the workspace manifest. Events may reference **multiple actors with role-tags** (e.g., `drafter`, `attester`, `reviewer`); role-tag vocabulary is **shape policy**, not part of the actor kind.

### Concrete example (PBS-Schulz workspace, illustrative only)

```
actors:
  - id: gunther-schulz
    subtype: human-actor
    declared-name: "Gunther Schulz"
  - id: claude-primary
    subtype: agent-actor
    substrate-binding: claude-agent-sdk
  - id: claude-monthly-invoicing
    subtype: agent-actor
    substrate-binding: claude-agent-sdk
```

A claim event might attribute to multiple actors with shape-declared roles (e.g., `claude-primary` as `drafter`, `gunther-schulz` as `attester`).

### What is NOT in the actor kind contract (deliberate omissions)

- **Authority** ("what events this actor may attest / authorize") → shape policy per D4. Framework-core's actor doesn't carry authority declarations.
- **Roles** (`drafter`, `attester`, `reviewer`, `practitioner`, etc.) → shape policy. Practitioner specifically is a shape role-binding on a `human-actor`, not a kind.
- **Cross-workspace identity** — out of scope. Whether two workspaces' `gunther-schulz` actors refer to the same human is a coordination-layer concern above the workspace kind.
- **Legal-personhood metadata** (Berufsrecht, professional licenses, etc.) → shape policy.
- **Capability declarations** (what tools an agent-actor can invoke) → substrate / specialist concern, not actor.

**Rationale**: actor is the minimal attribution-bearing participant kind. Per I3, every event needs an attributable subject; the actor kind provides exactly that, with subtype machinery to distinguish humans from agents (since their identity-resolution mechanics differ — humans persist via declared name + workspace-scope; agents persist via substrate-binding + workspace-scope). All substantive role/authority semantics push to shapes per D4.
