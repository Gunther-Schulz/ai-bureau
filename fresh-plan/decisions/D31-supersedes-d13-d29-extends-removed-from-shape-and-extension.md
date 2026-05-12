# D31 — 2026-05-09 — Supersedes D13 + D29: `extends` removed from shape and extension manifest

**Decision (supersedes the `extends` slot in D13 and D29)**: The `extends` slot is removed from both the shape kind contract (D13) and the extension manifest contract (D29). No composition / inheritance / mixin / overlay mechanism is introduced as a replacement. Shape variation patterns are deferred until concrete evidence forces a specific mechanism.

### Why this supersede

D13 introduced `extends` based on a hypothetical (regulated-practitioner-shape extending practitioner-shape); D29 introduced `extends` for extensions on parallel intent. No concrete deployment forces the slot today — we have neither a concrete second shape sharing with a first, nor an ecosystem-style variation pattern.

The cost of keeping `extends` (surfaced as workstream 4 began): conflict-resolution machinery per slot — additive vs. override vs. error rules; cascade through versioning; cognitive load of resolving extends-chains. Pure overhead until a concrete use case exists.

### Why no replacement mechanism

The mechanism shape changes; the cost remains:

- **Composition** (`composes: [...]`) — N-way conflict resolution; worse than 2-way inheritance.
- **Mixins** — same problem at finer granularity.
- **Configuration overlay** — pushes the conflict question into "what overlay slots exist."
- **Parameterization** — works for parameterizable values; doesn't address structural extension.
- **Delegation via reference** — runtime resolution semantics; same conflict question.

The mechanism that genuinely escapes the cost is **no mechanism — copy + modify when a deployment needs a variation**. Pay duplication; pay zero conflict-resolution complexity. Reversible later.

### What this changes

- **D13 (shape kind)** — the `extends` slot is removed. Shape is now standalone; no inheritance.
- **D29 (extension manifest contract)** — the `extends` slot is removed from the four-part manifest contract. Extensions are now standalone; no inheritance.
- **Workstream-3 schemas** — `shape.schema.json` and `extension-manifest.schema.json` are updated in the same commit as this entry to drop the `extends` slot (and the unused `version-range` `$def` in shape.schema.json that `extends` referenced). Worked examples updated where `extends: null` appeared (line removed).

### When to revisit

Per D14 late-emerging-pattern discipline + D26 Phase E (multi-deployment validation as evidence-gathering): when a concrete deployment surfaces a real cross-deployment variation pattern, the variation observed will tell us which mechanism (inheritance, composition, parameterization, overlay) is the right fit. Until then: nothing.

### What is NOT changed

- **D29 namespacing** — extension identifier scoping unchanged.
- **D29 vocabulary registrations + provisions + dependencies** — unchanged.
- **D13 other slots** — actor-requirements, required-capabilities, optional-capabilities, authority-bindings, roles, hooks all unchanged.
- **Workstream 4 remaining work** — multi-binding ambiguity (next entry); circular dependencies; extension load order + precedence. Inheritance conflict resolution removed from workstream 4 scope.

**Cross-references**: D4 (substantive identity = shape policy); D13 (shape kind contract; superseded on `extends`); D14 (late-emerging-pattern discipline); D26 (Phase E multi-deployment validation); D29 (extension manifest contract; superseded on `extends`); D30 (composition rules part 1).
