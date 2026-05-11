# fresh-plan/impl — Phase B reference implementation

Per **D36 + D41 + D42** (Phase B planning + amendments), this directory hosts the Phase B reference impl. **Impl side is complete**: all of B1, B2 (+ followons), B2b, B3, B4, B5, B6, B7, B8 shipped. **164 tests pass.** Remaining for Phase B closure: Bref (refinement workstream per D42; seven tracked deliverables; canonical list in `../CONCEPTS.md` open-questions) → Phase B closure entry (analog of D25 / D35).

What each workstream contributes:
- **B1** — Conformance validator. Applies D29 validation flow + D30 cross-kind referential integrity + D32 boot-time resolution (multi-binding, cycle detection, load order) + D33 version-conflict resolution. Library + CLI (`fresh-plan-validate`).
- **B2** — In-process substrate runtime (D12 + D17 capabilities `hooks` / `skills` / `event-streaming`). Now refactored into `Substrate` base + `InProcessSubstrate(Substrate)` subclass per B2b. Per-event D30 §4 runtime checks + D13 shape authority-binding check + chain integrity + subscriber dispatch (D37) all gated in `Substrate.append_event`. B2-followon-1 (D39 record emission on composition-change) + B2-followon-2 (D40 §A `state_at(n)` pure-replay) both landed.
- **B2b** — `MSAgentFrameworkSubstrate(Substrate)` stub per D41 two-substrate parity. Triggers `Substrate` base extraction (Implementation discipline + second-concrete-impl rule). Surfaces D17 capability-vocabulary cross-tension for Bref refinement.
- **B3** — Generic minimal shape (D13). `Shape` base + `GenericShape(Shape)` impl with per-event authority-binding enforcement.
- **B4** — Stub MCP-server-protocol adapter (D16 + D29 protocol-identifier registration). `Adapter` base + `MCPToolAdapter(Adapter)` impl. No real MCP wire (Phase C+).
- **B5** — Stub direct-api adapter. `DirectAPIAdapter(Adapter)`. Demonstrates non-MCP adapter path; loader dispatches by `protocol-or-transport`.
- **B6** — Generic minimal specialist (D19). `Specialist` base + `GenericSpecialist(Specialist)` impl. Substrate gains subscriber-dispatch giving D17 `event-streaming` real push semantics per D37.
- **B7** — RAG-via-MCP (per D38: retrieval composes via existing primitives). `RAGSpecialist(Specialist)` + new extension. Demonstrates one-protocol-many-provisions architectural property.
- **B8** — End-to-end scenario. Fixture composing all 5 shipped extensions; 7 tests satisfying D36 §C closure criterion 1-6.

## Tests

```bash
cd fresh-plan/impl
.venv/bin/python -m pytest -q     # (or use system Python + uv pip install -e .[dev])
```

164 tests; deterministic.

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

1. **Extension-id**: kebab-case, `-ext` suffix. Shipped: `inprocess-substrate-ext` (B2), `ms-agent-framework-substrate-ext` (B2b), `generic-shape-ext` (B3), `mcp-server-ext` (B4), `direct-api-ext` (B5), `generic-specialist-ext` (B6), `rag-via-mcp-ext` (B7). Anticipated for Phase D: `practitioner-shape-ext`, `pbs-schulz-ext`. Phase C will add real-wire variants (e.g., `mcp-server-realwire-ext` or rename pattern).
2. **Provision-id**: kebab-case, **no** `-ext` suffix. The provision is the *thing the extension provides*, distinct from the extension itself. Examples: `inprocess-substrate` (provided by `inprocess-substrate-ext`), `generic-shape` (provided by `generic-shape-ext`), `mcp-tool-adapter` (provided by `mcp-server-ext`), `rag-specialist` (provided by `rag-via-mcp-ext`).
3. **Cross-extension reference**: fully-qualified form `<ext-id>:<provision-id>`. Used in workspace-manifest binding `provision` slots and per D29 namespacing semantics. Examples: `inprocess-substrate-ext:inprocess-substrate`, `mcp-server-ext:mcp-tool-adapter`, `rag-via-mcp-ext:rag-specialist`. **Protocol-or-transport identifiers** follow the same qualified form (e.g., `mcp-server-ext:mcp-client`); B7 demonstrates that one protocol-or-transport can be declared by multiple provisions (different adapter specs, same runtime class via loader dispatch).

### Test fixtures

4. **Workspace fixture directory**: `tests/fixtures/workspace-<test-case>/`, where `<test-case>` describes what the fixture exercises. Examples: `workspace-valid`, `workspace-cycle`, `workspace-version-conflict`, `workspace-substrate-test`, `workspace-generic-shape`. Fixtures bundle a `workspace.json` + an `extensions/` subtree with copies of the extensions that fixture exercises. Fixtures are disposable test inputs — they are NOT canonical extensions; canonical extensions live at `impl/extensions/`.

## Known limitations

- **`spec-ref` content** (per D29: opaque-string-resolvable-by-the-loader) is loaded as JSON if the path resolves as a local file; otherwise the validator records the spec-ref string without further dereferencing. Remote URLs and registry references are out of scope at this layer.
- **All Phase B adapter / substrate / specialist runtimes are stubs.** Real-wire integration (real MCP JSON-RPC; real Claude Agent SDK; real MS Agent Framework; real RAG over corpus + vector DB; real direct-api function dispatch) is Phase C / D territory. The stubs prove the spec is implementable + that compositions wire cleanly.
- **D39 out-of-band-state tensions remain at Phase B**: pure `state_at(n)` replay does not reconstruct manifest-declared actors at boot (path #a) and reconstructs work-unit status only (not full record; path #b). Both are tracked Bref deliverables (synthetic-event-at-boot or explicit ledger amendment).
