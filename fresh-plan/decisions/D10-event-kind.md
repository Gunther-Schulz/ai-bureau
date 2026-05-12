# D10 — 2026-05-08 — Event kind

**Decision**: The event kind is the workspace's attribution-bearing record of happenings. Single kind; no separate `claim` kind (claim is a payload subtype). Every state mutation in the workspace flows through events (audit closure per I3).

### Contract slots

- **`id`** — unique within the workspace.
- **`prev-event`** — reference to the prior event in the workspace's chain. `null` only for the workspace's first event ever.
- **`timestamp`** — when the event happened.
- **`actors`** — at least one actor reference per D9. Each entry: `{ id, role? }`. The role-tag (e.g., `drafter`, `attester`, `authorizer`) is **shape policy** vocabulary, not part of the event kind.
- **`payload-subtype`** — one of the registered subtypes (core set below or extension-declared).
- **`payload`** — subtype-specific structure.

### Single chain per workspace

A workspace has one ordered event chain. `prev-event` forms the chain. The chain is **integrity-checkable** (the implementation provides a mechanism — hash-of-prev, append-only log, database with sequence constraint, etc.); the kind contract states the property, not the mechanism.

Filtered views (per-actor, per-work-unit, per-domain) are **derived by query**, not stored as separate chains. This keeps audit reconstruction linear and makes cross-cutting events (composition changes, lifecycle transitions) live naturally in the same chain as everything else.

### Core payload subtypes (framework-declared)

- **`claim`** — attributable assertion. Payload shape: free-form assertional content + (optional) confidence + (optional) evidence references. Practitioner-shape and similar shapes operate disciplines (sparring, attestation) on this subtype.
- **`action`** — something an actor did. Tool call, message sent, file read, external API invoke. Payload shape: action-name + parameters + outcome reference.
- **`state-change`** — workspace state mutation other than composition or lifecycle (e.g., scope set, work-unit transition). Payload shape: `what` + before/after references.
- **`composition-change`** — workspace composition binding/unbinding (per D7 §4 composition mutability). Payload shape: change-type + binding reference.
- **`lifecycle-transition`** — workspace lifecycle phase change (boot, shutdown, persist, resume, per D7 §4). Payload shape: transition-type + trigger.

### Subtype machinery: hybrid (open via registration)

Extensions (shapes, specialists, adapters) **may register additional payload subtypes** via the extension protocol (layer 3). Per-subtype payload-shape is validated by whoever declared it:
- Framework-core validates the five core subtypes' payload shapes.
- Extension-declared subtypes are validated by the extension that declared them.

This keeps framework-core small while permitting domain-specific event vocabularies (e.g., a hypothetical practitioner-shape might add `attestation-revoked`; an adapter might add `external-event-received`).

### Concrete example

Per the discussion that produced this decision: a Monday-in-PBS-Schulz worked example showed a single chain across `lifecycle-transition` (boot) → `state-change` (scope set) → `action` (file read) → `claim` (B-Plan citation) → `composition-change` (adapter added) → `action` (email sent) → `lifecycle-transition` (shutdown). All linked via `prev-event`; multi-actor events with role-tags appeared on `claim` and `action` (send-email).

### What is NOT in the event kind contract

- **Role-tag vocabulary** (`drafter`, `attester`, `reviewer`, etc.) — shape policy.
- **Specific payload shape for non-core subtypes** — extension-declared.
- **Integrity-mechanism specifics** (hash algorithm, signing scheme, storage backend) — implementation choice / layer 3.
- **Per-event-kind chains** (per-actor chain, per-work-unit chain) — derived by query, not stored.
- **Cross-workspace event linkage** — out of scope; workspace-scoped chain.

**Rationale**: events are the substrate I3 demands ("nothing escapes attribution"). Single-chain ordering supports linear audit reconstruction (per I3); machine-checkable contract slots support I2; hybrid subtype machinery supports I1 (extensions can compose new event vocabularies without modifying core).
