# fresh-plan/schemas — layer-3 formal schemas

Layer-3 formal schemas for framework-core kinds + extension manifest + core event payload subtypes. Per **D11**: schemas constrain *structure*, not *wire format*; instances may be serialized as JSON / YAML / TOML / msgpack and round-trip through the same schema. Per **D28**: JSON Schema Draft 2020-12 is the notation. Per **D35**: this artifact set is the closure inventory of Phase A workstream 3.

## Inventory

**Kind-impl + manifest schemas** (validate templates / impls provided by extensions, or workspace per-deployment manifests):

| Schema | Kind | Source decisions |
|---|---|---|
| `extension-manifest.schema.json` | Extension manifest | D29, D31 (extends removed), D34 §A.7 (vocabulary-slot enum closure) |
| `workspace.schema.json` | Workspace manifest | D7, D34 §A.6 (substrate-binding mutual exclusivity) |
| `substrate.schema.json` | Substrate impl | D12, D17 (capability vocabulary) |
| `shape.schema.json` | Shape impl | D13, D31 (extends removed) |
| `adapter.schema.json` | Adapter impl | D16 |
| `specialist.schema.json` | Specialist impl | D19 |

**Runtime-instance schemas** (validate runtime entities; actor and work-unit are workspace-scoped at runtime):

| Schema | Kind | Source decisions |
|---|---|---|
| `actor.schema.json` | Actor | D9, D22 (substrate-binding resolution) |
| `event.schema.json` | Event (envelope + payload discrimination) | D10, D23 (work-unit-id slot) |
| `work-unit.schema.json` | Work-unit | D20 |

**Event payload schemas** (per-subtype payload validation; referenced from `event.schema.json` via `allOf`+`if/then`):

| Schema | Subtype | Source |
|---|---|---|
| `payload-claim.schema.json` | claim | D10, D34 §A.8 |
| `payload-action.schema.json` | action | D10, D34 §A.8 |
| `payload-state-change.schema.json` | state-change | D10, D34 §A.8 |
| `payload-composition-change.schema.json` | composition-change | D10, D34 §A.8 |
| `payload-lifecycle-transition.schema.json` | lifecycle-transition | D10, D34 §A.8 |

**Shared `$defs`**:

| Schema | Content |
|---|---|
| `_common.schema.json` | `vocabulary-identifier`, `instance-identifier`, `qualified-identifier`, `semver`, `version-range`, `capability-identifier`, `payload-subtype-identifier`, `actor-subtype-identifier`, `runtime-shape-identifier`. Extracted in D34 §B to eliminate `$defs` duplication. |

**Examples** in `examples/` — 10 worked-example instances; all validate against their schemas (verified at D34 + D35 commits).

## Cross-file `$ref` resolution

Schemas use relative `$ref`s into peer schemas (e.g., `workspace.schema.json` references `actor.schema.json` for its `composition.actors[]` items; every schema references `_common.schema.json` for shared `$defs`). Resolution per JSON Schema Draft 2020-12: a relative `$ref` resolves against the referencing schema's `$id` base URL.

The schemas declare canonical `$id` values rooted at `https://pbs-bureau.dev/fresh-plan/schemas/`. Validators must be configured to map this base URL to the local schemas directory.

## Loading the schemas with a validator

The validator must load **all** schema files in this directory before validation, because of cross-file `$ref`s. Loading only one schema in isolation will fail with reference-resolution errors.

### Python (jsonschema 4.x)

```python
import json, glob
from jsonschema import Draft202012Validator
from jsonschema.validators import RefResolver

# Load all schemas into a store keyed by filename
store = {}
for path in glob.glob("fresh-plan/schemas/*.schema.json"):
    with open(path) as f:
        store[path.split("/")[-1]] = json.load(f)

# To validate an instance against (say) workspace.schema.json:
schema = store["workspace.schema.json"]
resolver = RefResolver(base_uri="", referrer=schema, store=store)
validator = Draft202012Validator(schema, resolver=resolver)

instance = json.load(open("path/to/workspace-manifest.json"))
errors = list(validator.iter_errors(instance))
if errors:
    for e in errors:
        print(f"{list(e.absolute_path)}: {e.message}")
```

This is the loading pattern used during Phase A validation (jsonschema 4.26.0; all 10 examples validate via this pattern — see commits `412c14c`, `5ff46dd`).

### JavaScript / TypeScript (ajv)

Conceptual outline (untested in Phase A; framework reference for future TypeScript-impl pass per D36):

```javascript
import Ajv from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import * as fs from "fs";
import * as path from "path";

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const schemasDir = "fresh-plan/schemas";
for (const file of fs.readdirSync(schemasDir).filter(f => f.endsWith(".schema.json"))) {
  const schema = JSON.parse(fs.readFileSync(path.join(schemasDir, file), "utf8"));
  ajv.addSchema(schema);  // ajv indexes by $id
}

const validate = ajv.getSchema("https://pbs-bureau.dev/fresh-plan/schemas/workspace.schema.json");
const valid = validate(instance);
```

## What the schemas DO NOT validate

Per **D28** + **D30** + **D32**, schemas cover only intra-kind structural conformance. The framework conformance validator (Phase B workstream B1 per D36) handles:

- Cross-kind referential integrity (D30) — e.g., that `event.actors[].id` resolves in workspace state.
- Capability satisfaction (D30 §2) — that bound substrates collectively advertise every `required-capabilities` from shape / adapter / specialist.
- Vocabulary resolution (D30 §3) — that every fully-qualified identifier resolves to a registered extension.
- Workspace-internal identity (D30 §4) — that all binding-ids / actor-ids resolve.
- Boot-time resolution (D32) — multi-binding satisfiability, cycle detection, load order.
- Cross-extension version-conflict resolution (D33) — range intersection at boot.

These checks are *above* the per-kind schemas. The schemas tell the validator what's structurally a "valid event"; the validator tells the runtime whether a structurally-valid event is also referentially-consistent with the workspace's state.

## Versioning

Per **D33**:

- Schema `$id` URLs MAY include a version path segment; current schemas do not (deliberately deferred; will surface when first major bump happens).
- Kind contract versions are *advisory* per D34 §A.9 — not operationally consumed by the boot validator.
- Extension-manifest semver per D29 IS operationally consumed (drives cross-extension version-conflict resolution per D33).

## Authoring conventions

- **Use `unevaluatedProperties: false`, NOT `additionalProperties: false`, on object schemas that use `allOf` + `if/then` for conditional fields.** JSON Schema Draft 2020-12 evaluates `additionalProperties` against the immediate schema only — it rejects properties added by `if/then` branches and produces false-positive failures. `unevaluatedProperties` evaluates against the merged set of all applied branches. Acknowledged in D34 §A.6; applied across `event.schema.json`, `actor.schema.json`, etc. Easy to forget when writing a new schema; cross-check before locking.

## Identifier conventions (per D29 + D34 §A.1)

- **`vocabulary-identifier`** (kebab-strict, `^[a-z][a-z0-9-]*$`) — extension-id, kind-impl ids, role-tags, hook names, capability values, runtime-shape values, payload-subtype values, work-unit-kind bare forms.
- **`instance-identifier`** (broader, `^[a-zA-Z0-9][a-zA-Z0-9._-]*$`) — workspace-scoped runtime ids: workspace.id, actor.id, event.id, work-unit.id, all binding-ids. Admits dots and uppercase for domain-natural keys (e.g., `wu-b-plan-3.2-hennigsdorf-2024`).
- **`qualified-identifier`** (`<extension-id>:<vocabulary-identifier>`) — cross-extension references; the canonical form per D29 namespacing.

## See also

- `../decisions.md` — the append-only decision ledger (D1-D36).
- `../README.md` — fresh-plan working preferences + procedural conventions + session-start procedure.
- `examples/` — 10 worked-example instances exercising the schemas.
