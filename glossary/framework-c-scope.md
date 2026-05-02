---
entry: Framework C scope
class: SCOPE-CLASSIFICATION
layer: framework-meta
axis: cross-axis
vision_usage: implicit
---

# Framework C scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: framework-meta (placement category for framework primitive definitions)
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory; VISION doesn't directly use this term)

**Canonical**: The scope category for framework primitive DEFINITIONS — universal, immutable, distributable; the placement home for entity-md instances that define mechanisms, shapes, substrates, protocol-implementations, and specialist DEFINITIONS. Derived from `framework = mechanisms` (mechanism definitions live here) plus the framework's other distributable elements.

**What it is**: One of three scope classifications (Framework C / Owner B / Layer A) governing where entity-md instances live. Framework C is the "definitions" home — distributable, marketplace-listable (per ROADMAP v3), immutable at definition level. Identity is by `framework_kind` + `framework_key` in entity-md frontmatter.

**Members**:
- mechanism definitions (atomic interface contracts authored at framework level)
- shape definitions (policy bundles for an archetype)
- substrate definitions (runtime contracts: Claude Agent SDK, MS AF, future)
- protocol-implementation definitions (concrete impls: always-on-sparring, claim-level-audit, etc.)
- specialist DEFINITIONS (bipartite multi-aspect primitive: DEFINITION here, INSTANCE-CONTENT in Owner B)

**What it is NOT**:
- Not for instances (those go to Owner B)
- Not for layered content varying by domain/state (that's Layer A)
- Not for runtime state

**Boundary test**: ask "is this a distributable definition that any workspace shape could potentially use?" If yes → Framework C. "Is this an instance bound to a deployment?" → Owner B. "Is this content varying by domain/state?" → Layer A.

**Composes with**:
- [framework](framework.md) — Framework C IS where framework primitive definitions live
- [shape](shape.md) — shape definitions live in Framework C
- [mechanism](mechanism.md), [substrate](substrate.md), [protocol (architectural)](protocol-architectural.md), [specialist](specialist.md) (DEFINITION) — all live in Framework C
- [Owner B scope](owner-b-scope.md) — where INSTANCES of Framework C definitions get deployed

**Source**: derived from entity-md scope model under `framework = mechanisms` / `shape = policies` architectural framing.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)
