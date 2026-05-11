# fresh-plan/impl — Phase B workstream B1: conformance validator

Per **D36** (Phase B planning lock), this is the **B1** workstream: a Python library + CLI that validates a workspace boot per the contracts locked in Phase A.

What this is: a **validator**, not a runtime. It applies

- **D29** validation flow (workspace.composition resolution-time),
- **D30** cross-kind referential integrity (the five check categories),
- **D32** boot-time resolution (multi-binding, cycle detection, load order),
- **D33** version-conflict resolution (range intersection over npm-style ranges).

It does NOT execute anything. Substrate / shape / adapter / specialist impls are workstreams B2-B6.

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

## Known limitations

- **Per-event runtime checks** (D30 §4 "per-event" portion) require runtime state and are deferred to B2 (substrate impl).
- **`spec-ref` content** (per D29: opaque-string-resolvable-by-the-loader) is loaded as JSON if the path resolves as a local file; otherwise the validator records the spec-ref string without further dereferencing. Remote URLs and registry references are out of scope at this layer.
