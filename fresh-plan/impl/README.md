# fresh-plan/impl — Phase B reference implementation

Per **D36** (Phase B planning lock), this directory hosts the Phase B reference impl. Shipping so far: **B1** conformance validator, **B2** in-process substrate runtime (+ B2-followon-1 D39 record emission + B2-followon-2 D40 §A `state_at(n)`), **B3** generic minimal shape impl. Pending: **B4** MCP-server adapter, **B5** direct-api adapter, **B6** specialist, **B7** RAG-via-MCP, **B8** end-to-end scenario.

What B1 applies:
- **D29** validation flow (workspace.composition resolution-time),
- **D30** cross-kind referential integrity (the five check categories),
- **D32** boot-time resolution (multi-binding, cycle detection, load order),
- **D33** version-conflict resolution (range intersection over npm-style ranges).

B2 hosts the in-process substrate (D12 + D17 capabilities `hooks` / `skills` / `event-streaming`); B3 attaches a generic shape (D13) with authority-binding enforcement. Adapter / specialist runtime execution = B4–B6.

## Install

```bash
cd fresh-plan/impl
pip install -e .
```

(or `uv pip install -e .` if `uv` is your packaging tool of choice.)

## CLI

```bash
fresh-plan-validate <workspace.json|workspace.yaml> --extensions-dir <path>
```

Exits 0 on success; non-zero with a structured failure report otherwise.

## Library

```python
from pathlib import Path
import json
from fresh_plan.validator import validate_workspace_boot

manifest = json.load(open("workspace.json"))
result = validate_workspace_boot(manifest, Path("./extensions"))

if not result.success:
    for f in result.failures:
        print(f"[{f.category}] {f.path}: {f.reason}")
```

## Extension on-disk layout

```
<extensions-dir>/
  <extension-id>/
    <version>/
      extension-manifest.json
      # spec-refs referenced from manifest live alongside as relative paths
```

The validator scans `<extensions-dir>` recursively; each `<extension-id>/<version>/extension-manifest.json` is treated as one extension version.

## Naming conventions

Conventions that emerged from worked examples in B1 + B2 + B3. **Revisable when a workstream surfaces a structural reason** — not aesthetic preference. Revision = update this section + every in-tree reference in one pass.

### Extensions and provisions

1. **Extension-id**: kebab-case, `-ext` suffix. Examples: `inprocess-substrate-ext`, `generic-shape-ext`. Anticipated next: `mcp-server-ext` (B4), `direct-api-ext` (B5), `practitioner-shape-ext` (Phase D), `pbs-schulz-ext` (Phase D).
2. **Provision-id**: kebab-case, **no** `-ext` suffix. The provision is the *thing the extension provides*, distinct from the extension itself. Examples: `inprocess-substrate` (provided by `inprocess-substrate-ext`), `generic-shape` (provided by `generic-shape-ext`).
3. **Cross-extension reference**: fully-qualified form `<ext-id>:<provision-id>`. Used in workspace-manifest binding `provision` slots and per D29 namespacing semantics. Examples: `inprocess-substrate-ext:inprocess-substrate`, `generic-shape-ext:generic-shape`.

### Test fixtures

4. **Workspace fixture directory**: `tests/fixtures/workspace-<test-case>/`, where `<test-case>` describes what the fixture exercises. Examples: `workspace-valid`, `workspace-cycle`, `workspace-version-conflict`, `workspace-substrate-test`, `workspace-generic-shape`. Fixtures bundle a `workspace.json` + an `extensions/` subtree with copies of the extensions that fixture exercises. Fixtures are disposable test inputs — they are NOT canonical extensions; canonical extensions live at `impl/extensions/`.

## Known limitations

- **Per-event runtime checks** (D30 §4 "per-event" portion) require runtime state and are deferred to B2 (substrate impl).
- **`spec-ref` content** (per D29: opaque-string-resolvable-by-the-loader) is loaded as JSON if the path resolves as a local file; otherwise the validator records the spec-ref string without further dereferencing. Remote URLs and registry references are out of scope at this layer.
