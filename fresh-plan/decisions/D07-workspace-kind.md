# D7 — 2026-05-08 — Workspace kind

**Decision**: The workspace kind contract specifies four facets, derived from D5/I1's organizing-primitive role.

### 1. Identity

- Each workspace declares a stable, unique identifier.
- The identifier persists across the workspace's full lifecycle (boot → shutdown → resume across machines / sessions / years).
- Same identifier = same workspace (same composition lineage, same state lineage). Different identifier = independent composition.

### 2. Composition (declarative bindings)

The workspace declares which extensions it composes. Each binding references an extension that conforms to its respective kind contract. The framework validates conformance per I2.

**Cardinality:**
- **shape**: exactly 1 (the workspace is shape-typed; hybrid-shape mechanics deferred).
- **substrate-binding**: 1+ (binding can be specific, capability-based, or mixed — see §4 lifecycle).
- **adapter**: 0+.
- **specialist**: 0+.
- **actor**: 1+ (universal — workspaces require attributable actors per I3; actor = `human-actor` or `agent-actor` subtype). "Practitioner" is **not** a kind at this layer — it is a shape-level role-binding (e.g., practitioner-shape declares: "the human-actor who is the accountable principal of this workspace"). Other shapes may not use the term.

### 3. State (what accumulates)

A workspace accumulates state as composition runs. State survives between runtime sessions (workspace persists; sessions are runtime episodes within it).

**State contents:**
- **events**: timeline of attribution-bearing happenings. Single kind `event` with **payload subtypes** including `claim`, `action`, `state-change`, `composition-change`, `lifecycle-transition`, etc. Disciplines (later, in shapes) declare which payload subtypes they care about.
- **work-units**: active and historical units of work (work-unit kind defined separately).
- **scope**: current active domain / state within which composition is operating.

**Attribution closure (per I3)**: every state mutation is an event. Nothing escapes attribution. Even composition mutations (adding an adapter, retiring a specialist) flow through state as events.

### 4. Lifecycle

A workspace can boot, run, persist, and shut down.

- **boot**: read manifest → bind extensions → restore state → become operational.
- **run**: process events through composed extensions; accumulate state.
- **persist**: state survives between runtime episodes.
- **shut down**: clean exit; state persisted; bound substrate(s) released.

**Composition is mutable** during lifecycle (new bindings can be added; old bindings retired). Every composition mutation is itself an attribution-bearing event (per I3).

**Boot is triggered externally** (host process, user action, schedule, orchestrating agent, etc.); the workspace kind is agnostic to trigger mechanism. The **substrate hosts the agent loop**; the workspace is composed within the substrate's context. The workspace does not boot itself.

**Substrate-binding cardinality across lifecycle**:
- Manifest: 1+ substrate-binding declared (specific / capability-based / mixed).
- Runtime (running): 1+ substrate currently live and bound.
- Persisted, non-running: 0 substrates live; manifest declaration unchanged.

### Manifest vs runtime distinction

- **Manifest** = declarative — what this workspace IS (identity, bindings, intended composition). Persisted; survives between runs.
- **Runtime state** = accumulating — what's happening / has happened (events, claims, work-units, scope). Persisted between runs but grows during runs.
- **Together**: workspace = manifest + state. Both must conform to contract; framework validates manifest at boot and validates state-accumulation per event (per I2).

**Rationale**: each facet is load-bearing for at least one identity claim:
- Identity supports I1 (workspaces are distinguishable so compositions are independent).
- Composition supports I1 (it's what gets composed) + I2 (binding validation is structural conformance).
- State supports I3 (accumulation is attribution-bearing; event-recursive ensures nothing escapes attribution).
- Lifecycle supports I1 (boot/run/persist makes composition operationally real) + I3 (transitions are attribution-bearing).

**Open / deferred**:
- Concrete schema of the manifest (Pydantic, markdown, both, other) — implementation choice; layer-3 territory.
- Concrete persistence mechanism for state — implementation choice.
- Hybrid-shape mechanics (workspace with mixed shapes) — deferred; either becomes a separate kind or is handled as a shape-of-shapes.
- Multi-workspace federation (one actor across multiple workspaces) — deferred.

**Flagged for layer 2 follow-up kinds** (each becomes its own decision entry):
- `actor` (with subtypes `human-actor`, `agent-actor`).
- `event` (with payload-subtype machinery).
- `work-unit`.
- `substrate` (kind contract; capability declarations; binding semantics).
- `shape`, `adapter`, `specialist` — bound by workspace.
