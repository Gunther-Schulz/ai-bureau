# D29 — 2026-05-09 — Extension manifest contract + validation flow

**Decision**: An extension is declared by a structural manifest. The manifest contract has four parts; core validates extensions at workspace.composition resolution-time.

### Manifest contract

**1. Identity**

- **`id`** — stable extension identifier.
- **`version`** — version designator (semver-shaped at layer-3 formal schema; range-comparable).
- **`extends`** *(optional)* — reference to a parent extension with version range. Inheritance conflict resolution = workstream 4.

**2. Vocabulary registrations** — list of `(slot, identifier, spec-ref)` tuples adding values to a core open-vocabulary slot.

The open-vocabulary slots in framework-core (per D7-D20):

- `event.payload-subtype` (D10)
- `work-unit.kind` (D20)
- `substrate.capabilities[]` items (D17 — beyond the three abstract core capabilities)
- `substrate.runtime-shapes[]` items (D12)
- `adapter.protocol-or-transport` (D16)
- `actor.subtype` (D9)

`spec-ref` references the value's specification (typically a JSON Schema per D28; for some slots, additionally a behavioral contract document).

Required slot; may be `[]` (per D13 required-with-explicit-empty pattern).

**3. Provisions** — list of `(kind, id, spec-ref)` tuples; actual instances of kinds the extension provides. Kinds that admit provisions: **substrate, shape, adapter, specialist**. (workspace, event, actor, work-unit are not extension-provided — workspace is per-deployment manifest; event / actor / work-unit are runtime instances.)

Each provision conforms to its kind's layer-3 formal schema (workstream 3).

Required slot; may be `[]`.

**4. Dependencies**

- **`required-core-capabilities[]`** — abstract core capabilities (`hooks`, `skills`, `event-streaming` per D17) the provisions need. Required, may be `[]`.
- **`required-extensions[]`** — list of `(extension-id, version-range)`. Required, may be `[]`. Circular-dep detection + resolution = workstream 4.

### Identifier namespacing

Identifiers registered by an extension are **implicitly namespaced by extension id**. Canonical fully-qualified form: `<extension-id>:<identifier>` (e.g., `a2a-protocol-ext:a2a-peer`).

Within an extension's own manifest, references to its own identifiers may be bare; cross-extension references must be fully-qualified. Workspace.composition references vocabulary by fully-qualified form. Two extensions registering the same bare identifier do not collide — they're distinct under qualification.

### Validation flow

Core validates at **workspace.composition resolution-time** (workspace boot, per D7 §4). No separate "install" step. The workspace's composition is the unit of trust.

1. Workspace manifest declares `composition`, referencing extensions by `(id, version-range)`.
2. Core resolves each reference to a specific extension version available locally.
3. Each resolved extension's manifest is validated against the extension formal schema (produced in workstream 3).
4. Vocabulary registrations are merged into the workspace's open-vocabulary tables (with namespacing per above).
5. Each provision is validated against its kind's formal schema.
6. Cross-kind composition checks run (workstream 4).
7. Any failure prevents workspace boot.

### Worked example: A2A protocol extension

```yaml
# Format: YAML for readability; on-disk format is implementation choice per D11.
id: a2a-protocol-ext
version: 1.0.0
extends: null

vocabulary-registrations:
  - slot: adapter.protocol-or-transport
    identifier: a2a-peer
    spec-ref: ./specs/a2a-peer-protocol.schema.json
  - slot: substrate.capabilities
    identifier: a2a
    spec-ref: ./specs/a2a-capability.schema.json

provisions:
  - kind: adapter
    id: a2a-peer-adapter-default
    spec-ref: ./adapters/a2a-peer-default.adapter.json

dependencies:
  required-core-capabilities: []
  required-extensions: []
```

A workspace using it:

```yaml
composition:
  extensions:
    - id: a2a-protocol-ext
      version: '>=1.0.0'
  adapter-bindings:
    - id: my-a2a-adapter
      provision: a2a-protocol-ext:a2a-peer-adapter-default
      protocol-or-transport: a2a-protocol-ext:a2a-peer
```

### Tensions / open questions surfaced (deferred)

- **Spec-ref resolution semantics** — within-package paths vs. URLs vs. registry references. Implementation per D11; manifest contract treats `spec-ref` as opaque-string-resolvable-by-the-loader.
- **Inheritance conflict resolution** for `extends` — child + parent register same identifier or provide same kind-id. → workstream 4.
- **Circular extension dependencies** — detection + handling. → workstream 4.
- **Mid-runtime extension reload** — workspace.composition mutability per D7 §4 covers conceptually; concrete validation flow for hot-reload = layer-3 detail / impl.
- **Extension signing / authenticity** — out of scope; impl / security concern.

### What is NOT in this decision

- The formal schema for the extension manifest itself (workstream 3 will produce).
- Discovery mechanism (how core finds available extensions) — implementation.
- File-system / packaging conventions — implementation.
- Inheritance + circular-dep + conflict resolution semantics — workstream 4.

**Rationale**: extensions connect the 8 layer-2 kinds' open vocabularies + impl-bearing kinds to the rest of the framework. Per I1, extensions compose; per I2, the manifest is machine-checkable; per I3, vocabulary registration is itself attribution-bearing (a `composition-change` event per D10).

The four-part shape reflects two distinct things extensions contribute — *vocabulary entries* (identifiers + specs) and *conforming things* (impls of kinds) — plus dependencies for composition validation. Each part is load-bearing.

**Cross-references**: D7, D10, D12, D13, D16, D17, D19, D20; D28 (notation); workstreams 3, 4, 5.
