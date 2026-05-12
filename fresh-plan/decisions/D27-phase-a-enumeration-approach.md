# D27 — 2026-05-09 — Phase A enumeration approach

**Decision**: Phase A (layer 3) is enumerated in five workstreams, in this order:

1. **Notation** — formal-schema toolchain choice.
2. **Extension mechanism** — how extensions declare themselves; how core validates conformance.
3. **Per-kind formal schemas** — the 8 kinds (D25), locked one-by-one.
4. **Composition rules** — cross-kind composition, conflict resolution, precedence.
5. **Promotion / demotion rules** — how things move between layers / extension ↔ core.

Each substantive decision = one ledger entry locked at the time of agreement (per D6 incremental discipline). After the five workstreams complete, a refinement pass per D14 sweeps the locked entries; a closure entry analog of D25 marks Phase A done.

**Rationale**: outside-in ordering. Notation comes first because the rest is written in it. Extension mechanism comes before per-kind schemas because every kind has extension-registered open vocabulary (event payload-subtypes, work-unit-kinds, protocol identifiers, capability identifiers) — schemas can't be precise without it. Composition + promotion build on top of locked schemas.

**Order is indicative, not rigid** (per D26 caveat): if a per-kind schema forces revisiting the extension mechanism, we revisit; if composition rules surface a schema gap, we sharpen. Strict sequence enforcement is not the point — the ordering is the default path.

**Procedural**: same disciplines as layer 2 — append-only, one question at a time, concrete examples before locking, rolling refinement (option C) for clear-now findings, named refinement pass at the end for cross-cutting findings.
