# D32 — 2026-05-09 — Boot-time resolution: multi-binding, circular deps, load order (composition rules part 2)

**Decision**: Three boot-time resolution concerns settled together. The validator's behavior at workspace.composition resolution-time (per D29 + D30) is fully specified by these three principles plus D30's referential integrity checks.

### 1. Multi-binding ambiguity

When more than one binding could satisfy a requirement, the framework verifies satisfiability at boot but does not pick a specific binding for runtime use.

- **Specialist's `required-adapter-bindings[]`** — satisfied at boot if at least one workspace `adapter-bindings[]` entry references the named provision. If multiple bindings of the same provision exist, runtime / shape policy picks which one a given operation uses; framework does not specify.
- **Multiple specialists supporting the same `work-unit-kind`** — framework does not pick. Routing is shape policy or explicit at work-unit creation (work-unit.contributing-specialists[] declared per work-unit). Framework only verifies that at least one bound specialist supports the kind.
- **Shape's `required-capabilities[]` against multiple bound substrates** — already settled in D30 as union-based satisfiability (any substrate providing the capability satisfies). Restated here for completeness.

**Principle**: framework's boot-time job is *can the workspace run* (every requirement met by at least one provider); runtime concern is *which provider for this operation* (shape / runtime / impl decides).

### 2. Circular extension dependencies

Detected at boot via topological sort of the extension dependency graph.

- **Graph construction**: nodes = extensions referenced in workspace.composition.extensions[] (transitively closed via each extension's `dependencies.required-extensions[]`); edges = `A depends on B` becomes `B → A`.
- **Sort**: any standard topological-sort algorithm (Tarjan, Kahn). If sort fails, a cycle exists.
- **Failure semantics**: workspace cannot boot. Validator returns the cycle path (e.g., `A → B → C → A`). Per D30 timing modes: boot-time failure is all-or-nothing.

Algorithm specifics are implementation. The framework specifies *that* cycles are detected and *that* cycle-detection causes boot failure.

### 3. Extension load order + precedence

Once cycles are excluded, the dependency graph is a DAG. Load order is its topological order.

- **Predecessors before dependents**: if extension B depends on A, A's vocabulary registrations + provisions are available before B loads.
- **Independent extensions** (no dependency relationship, direct or transitive): framework loads them in **alphabetical order by extension id** for determinism. Avoids non-deterministic boot behavior across runs.
- **Precedence is not a question**: per D29's namespacing, two extensions cannot register the same fully-qualified identifier (`<ext-id>:<id>`). No "which registration wins" decision arises. The only ordering concern is *availability* (predecessor registrations available to dependents), which the topological order guarantees.

### Worked example: cycle detection

Workspace.composition.extensions includes `ext-a` and `ext-b`:

- `ext-a.dependencies.required-extensions[] = [{ id: "ext-b", version-range: ">=1.0.0" }]`
- `ext-b.dependencies.required-extensions[] = [{ id: "ext-a", version-range: ">=1.0.0" }]`

Boot:

1. Per D29 validation flow, extensions are resolved.
2. Per this D32 §2, dependency graph is built: edges `ext-a → ext-b → ext-a`.
3. Topological sort fails.
4. Validator returns failure: `{category: "circular-dependency", cycle: ["ext-a", "ext-b", "ext-a"]}`.
5. Boot does not proceed (per D30 all-or-nothing).

### What is NOT in this decision

- **Algorithm implementation** for cycle detection / topological sort — implementation per D11.
- **Runtime routing rules** for multi-binding cases (which adapter, which specialist) — shape policy / runtime / impl.
- **Hot-reload / partial-reload semantics** for extensions — implementation; D7 §4 composition mutability covers conceptually.
- **Extension version conflict resolution** when multiple workspace extensions transitively pull in different versions of the same dependency — surfaced here as a known gap; left to workstream 5 (promotion / demotion) or end-of-Phase-A refinement, since version-conflict resolution is interlinked with versioning policy more broadly.

**Rationale**: per I2, conformance must be machine-checkable; cycle detection + load order are mechanical. Per D29, validation runs at composition resolution-time. Multi-binding resolution settles to *satisfiability-only* at framework level because runtime routing is properly a shape / runtime concern (per D8: routing-by-context is not a framework-core kind). Alphabetical tiebreaking for independent extensions is the simplest deterministic rule; no real choice value lives here.

**Cross-references**: D8 (routing concerns are not framework-core); D11 (implementation level); D29 (validation flow + namespacing); D30 (referential integrity + boot-time failure semantics); D31 (extends removed; simpler workstream-4 scope).
