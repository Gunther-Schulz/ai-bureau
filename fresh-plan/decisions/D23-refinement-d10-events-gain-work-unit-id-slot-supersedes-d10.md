# D23 — 2026-05-08 — Refinement: D10 events gain `work-unit-id` slot (supersedes D10 slot list)

**Decision (supersedes D10's contract slots)**: The event kind contract (D10) gains an optional **`work-unit-id`** slot:

- **`work-unit-id`** *(optional)* — references the work-unit (per D20) the event is associated with, when applicable. `null` when the event is not work-unit-associated (e.g., workspace-level lifecycle events, composition-changes that don't belong to a specific work-unit).

**Revised D10 slot list** (full, with the addition):

- `id` — unique within workspace
- `prev-event` — reference to prior event in chain (`null` only for first ever)
- `timestamp` — when the event happened
- `actors[]` — at least one actor reference; each entry `{ id, role? }`
- `payload-subtype` — registered subtype identifier
- `payload` — subtype-specific structure
- **`work-unit-id`** *(optional)* — work-unit reference, when applicable

**Rationale**: per D10's single-chain principle, work-unit-events are a derived view by filtering. Filtering needs a structural slot, not payload-rummaging — payload-rummaging is brittle and breaks the kind contract's machine-checkability per I2. Making `work-unit-id` first-class enables clean per-work-unit views (per D20's lifecycle-history-derivable-from-events claim).

**Substantive impact**: this adds a slot to D10's contract, so it's a supersedes-class change. Implementations / formal schema / serialization adjust accordingly.

**Cross-references**: D20 work-unit kind; D7 §3 state contents.
