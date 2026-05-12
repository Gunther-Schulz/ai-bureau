# D28 — 2026-05-09 — Formal-schema notation: JSON Schema (Draft 2020-12)

**Decision**: Layer-3 formal schemas for the 8 kinds (D25) are written in **JSON Schema, Draft 2020-12**. This confirms D24's "in scope (layer-3 toolchain)" finding for JSON Schema.

**Rationale**:

- **Format-neutral per D11**: JSON Schema constrains structure, not wire format. Implementations may serialize instances as JSON, YAML, TOML, msgpack, etc. — all round-trip through the same schema.
- **Tooling maturity**: validators exist in every major language (ajv, jsonschema, opis/json-schema, etc.). No bootstrap problem.
- **Reference + composition**: `$ref`, `allOf`/`oneOf`/`anyOf`, `if/then/else`, `discriminator` (via OpenAPI extension) cover everything the kind contracts need (e.g., conditional metadata by `actor.subtype` per D9; `payload-subtype`-discriminated payloads per D10).
- **Draft 2020-12** is the latest stable; supersedes earlier drafts; broad validator support.

### What JSON Schema covers (sufficient)

- Per-kind structural validation: slot lists, required/optional, types, enums, cardinalities, format constraints (regex, ISO-8601 timestamps, etc.).
- Open-vocabulary slots (e.g., `payload-subtype`, `protocol-or-transport`, `kind`) modeled as strings with extension-registered values; the registry mechanism is layer-3 workstream 2 territory, not the schema itself.

### What JSON Schema does NOT cover (deferred to other layer-3 work)

- **Cross-kind referential integrity** — e.g., event's `actors[].id` must exist in workspace.actors[]; specialist's `supported-work-unit-kinds[]` must match an extension-registered work-unit-kind. Out of scope for JSON Schema; handled by the framework conformance validator (a layer above the schemas that applies cross-kind invariants). The schemas specify what conformance is *within* each kind; the validator specifies what conformance is *between* kinds.
- **Runtime invariants** — e.g., event-chain `prev-event` ordering, work-unit lifecycle transition validity. Schema-validates the slot's *type*; the validator-or-runtime enforces the *invariant*.

### What is NOT in this decision

- **Schema file layout / location** — deferred to per-kind workstream (workstream 3).
- **Validator implementation choice** (ajv vs jsonschema vs opis) — implementation level (below layer 3 per D11).
- **Other notations considered** — SHACL/RDF (overkill for kind contracts; may resurface in standards-mapping for PROV-O / VC / DID per D24); CUE / TypeSpec (less mature ecosystem). Not adopted; not ruled out for niche use later (e.g., a SHACL representation for PROV-O integration).
- **Schema versioning** (how schemas evolve over time) — deferred; will surface in promotion / demotion workstream (workstream 5).

**Cross-references**: D11 (formal schema = layer 3; format = implementation); D24 (JSON Schema named as in-scope toolchain candidate); D27 (workstream order).
