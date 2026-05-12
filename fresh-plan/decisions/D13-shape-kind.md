# D13 — 2026-05-08 — Shape kind

**Decision**: The shape kind is the carrier of substantive identity (per D4) — policy bundles that give a workspace its disciplines, authority semantics, and role vocabulary. Per D7, exactly 1 shape per workspace.

### Contract slots

- **`id`** — stable identifier (e.g., `practitioner-shape`).
- **`version`** — version designator (range-comparable; semver-shaped at layer-3 formal schema).
- **`extends`** *(optional)* — reference to a parent shape with version range. When present, the parent's slots are inherited; the child shape adds / specializes. Inheritance conflict resolution rules → layer-3 formal schema.
- **`actor-requirements`** *(required slot, explicit `none` admissible)* — workspace-level cardinality constraints per actor-subtype that aren't expressible in authority-bindings (e.g., single-practitioner constraint; supervisor presence not appearing in any binding). When present as concrete requirements, framework validates eagerly at boot + at composition mutation. When `none`, no eager cardinality check; framework relies on per-event validation via authority-bindings.
- **`required-capabilities[]`** — substrate capabilities the shape needs (non-empty list; a shape that needs no capabilities cannot meaningfully impose policy).
- **`optional-capabilities[]`** — substrate capabilities the shape uses if present (may be empty list).
- **`authority-bindings[]`** — list of `(payload-subtype, qualifier?, required-role, required-actor-subtype, additional-constraints?)` tuples. Empty list (`[]`) is admissible (shape with no per-event authority requirements); the author still must declare the slot, signaling the question was considered.
- **`roles[]`** — role-tag vocabulary the shape introduces. Used by events (per D10) to tag actor participation. Empty list admissible.
- **`hooks[]`** — semantic declarations of policy hook points (`name`, `purpose`, optional `applies-to` qualifier). Formal hook interface = layer 3. Empty list admissible. Hook callable code = implementation.

### Required-with-explicit-none / required-with-empty-list pattern

Several slots above (`actor-requirements`, `authority-bindings`, `roles`, `hooks`) are **mandatory** even when their content is empty — to force shape authors to consider whether they need the slot rather than silently omit. `actor-requirements` admits an explicit `none` sentinel because it is not list-shaped; the others admit `[]` (empty list). In both cases, the explicit-empty form is a deliberate "considered and chose none" declaration, structurally distinct from omission.

### What this lets the shape kind do

- **Carry substantive identity** (per D4) without forcing axes / specific disciplines into framework-core.
- **Be machine-validatable** (per I2): authority-bindings + capability requirements + actor-requirements all let core check at boot whether a workspace + bound extensions satisfy the shape's contract.
- **Compose via extension** (`extends`): regulated-practitioner-shape extends practitioner-shape; autonomous-business-shape stands alone; hybrid-shape mechanics deferred per D7.

### Concrete example (illustrative; not part of core)

Per discussion that produced this decision: a `practitioner-shape` (human-actor required; sparring + attestation hooks; claim attestation requires human-actor in role=attester) and a contrasting `autonomous-business-shape` (no human required; budget gate on financial actions). Plus a `regulated-practitioner-shape` extending the practitioner-shape with defensibility-grade claim qualifier and a regulator role.

### What is NOT in the shape kind contract

- **The "three axes"** (intertwining / sparring / authorship-preservation / defensibility / engaged-authorship) — shape-internal organizing principles, not kind-level slots. Practitioner-shape adopts them; other shapes may not. Per D4.
- **Discipline implementations** (sparring algorithm, attestation flow, gate-firing logic) — shape-impl / extension territory. The kind declares hook *names* and *purposes*; impls supply behavior.
- **Specific role semantics** (what `attester` means in practice) — shape impl / prose.
- **Hook callable code** — implementation.
- **Inheritance conflict resolution rules** — layer 3 (formal schema for `extends`).
- **Hybrid / multi-shape composition mechanics** — deferred per D7.

**Rationale**: shape carries substantive identity per D4. Its slots are structural-declarative (what kinds of policies + roles + cardinality the shape imposes); the substantive semantics (what disciplines mean, what attester actually does) are pushed to shape impls and shape prose. Per I1, shape is the composable substantive layer; per I2, shape declarations are machine-validatable so the framework can check workspace conformance to its bound shape; per I3, shape's authority-bindings + hooks define how attribution-bearing events get policy treatment without baking specific disciplines into core.
