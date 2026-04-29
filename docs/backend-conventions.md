# Backend conventions

> **Scope boundary.** This doc covers idioms within Type E (backend
> Python). For "where does X belong?" questions, see
> `ARCHITECTURE.md`. Specifically, meta-rule 5 (execution locality)
> decides what is a tool vs. skill behavior; this doc decides
> *how* a tool is written once that's settled. Plugin-side
> idioms (Type A/B — skills + skill references) live in
> `docs/plugin-conventions.md`.

Conventions for `backend/mcp-server/` Python code. Resolves audit
deferred items D1 (test layout), D2 (logging), D3 (MCP error
format) — see `docs/audit-pre-rag.md`.

**Status**: ACCEPTED. First applied in RAG-pipeline work (next
phase after this doc lands).

**Why now**: ROADMAP "Backend conventions doc" pull-forward
trigger was "write the doc when Tier 1 MCP tools land — that's
when conventions get applied for the first time." Tier 1 landed
in session 4. RAG-pipeline additions (OCR/DRM/ColPali, legal
§-graph, hybrid retrieval) start next; doing them under explicit
conventions is cheaper than retrofitting.

---

## 1. Test layout

### Structure

```
backend/mcp-server/
├── src/pbs_mcp/
│   ├── server.py
│   ├── tools/
│   │   ├── discovery.py
│   │   └── memory.py
│   └── chunkers/
│       └── ...
└── tests/
    ├── conftest.py             # shared fixtures
    ├── unit/
    │   ├── test_discovery.py   # mirror src/pbs_mcp/tools/discovery.py
    │   ├── test_memory.py
    │   └── ...
    └── integration/
        ├── test_search_corpus.py   # needs LanceDB
        ├── test_research_references.py  # needs network (mark @pytest.mark.network)
        └── ...
```

- **Unit tests** — pure-Python, no I/O outside `tmp_path` fixtures.
  Run on every commit.
- **Integration tests** — touch LanceDB / SQLite / network.
  Marked with `@pytest.mark.integration` (or `@pytest.mark.network`
  for outbound HTTP). Run pre-merge, not on every commit.
- **No mocking of in-process state** — use real LanceDB tables in
  `tmp_path`, real SQLite databases. The tests run locally; speed
  is not the load-bearing constraint.
- **Test files mirror module structure** under `unit/`. One test
  file per src module. If a src module grows past ~300 lines, its
  test file mirrors any internal split.

### Fixtures

Shared fixtures in `tests/conftest.py`:

- `tmp_office_config` — minimal valid `office.yaml` in `tmp_path`
- `tmp_lancedb` — fresh LanceDB instance in `tmp_path`
- `tmp_legal_graph` — fresh SQLite legal-graph DB in `tmp_path`
- `sample_chunks` — pre-canned test chunks for retrieval tests
- `clean_env` — clears `PBS_OFFICE_CONFIG` env var

### What to test

- **Always**: input/output Pydantic shapes (validation matches
  contract), happy path, the most likely failure modes (file
  missing, malformed YAML, empty corpus, no scope match).
- **Often**: edge cases that have been a bug source (path
  resolution, scope_key vs domain mapping, manifest layering).
- **Sometimes**: full end-to-end via MCP server stdio loop —
  reserved for one or two smoke tests.

### Running tests

```bash
# Unit only (fast)
uv run pytest tests/unit/

# Full suite
uv run pytest

# Skip integration (e.g. offline)
uv run pytest -m "not integration and not network"
```

### Pytest config

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "integration: needs LanceDB or other I/O",
    "network: needs outbound HTTP",
]
```

**Alternatives considered**:

- **`tests/` co-located with `src/` modules** (every source dir
  has its own `tests/` subdir): rejected — duplicates structure
  and pytest discovery is happier with a top-level `tests/`.
- **unittest** instead of pytest: rejected — pytest is already in
  dev-dependencies; pytest fixtures + parametrize are noticeably
  ergonomic.
- **Mock-heavy unit tests** (mock LanceDB, SQLite, filesystem):
  rejected — local backend with embedded DBs makes real-instance
  tests cheap; mocks would diverge from runtime behavior and
  mask integration issues.

**Revisit trigger**: test suite runtime exceeds ~30s on CI and
slows the dev loop (suggests aggressive integration-marking or
selective mocking); OR a full external dependency (e.g. a paid
API) enters the stack and mock-based tests become unavoidable.

---

## 2. Logging

### Pattern

```python
# top of every module
import logging
logger = logging.getLogger(__name__)

# usage — %-format (ruff G rule), not f-string in log calls
logger.info("loaded %d manifests from scope", count)
logger.warning("manifest at %s missing entries", path)
logger.exception("tool %s raised", name)  # captures stack
```

### Configuration

`basicConfig` happens **exactly once**, in `server.main()`:

```python
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
```

- Output to **stderr** (stdout is reserved for MCP JSON-RPC).
- INFO default; switch to DEBUG via `PBS_LOG_LEVEL=DEBUG` env var
  when investigating.
- No structured logging (no JSON logs) — local single-user backend
  doesn't justify it.

### Levels

| Level | Use for |
|---|---|
| `DEBUG` | Per-chunk / per-row detail (off by default). |
| `INFO` | Lifecycle events (tool started, ingest completed N entries, server starting). |
| `WARNING` | Recoverable degradation (manifest entry malformed, fell back to default). |
| `ERROR` | Unrecoverable but caught (exception caught + returned to caller as error envelope). |
| `CRITICAL` | Reserved (don't use; nothing in this backend justifies it). |

### Style: %-formatting in log calls

`logger.info("loaded %d manifests", count)`, NOT
`logger.info(f"loaded {count} manifests")`.

Reason: %-formatting defers string interpolation to the moment a
log handler decides to emit; f-strings always interpolate even if
the message is filtered out. Negligible at our scale, but it's
also the linter's preference — adopt it for consistency.

Add to ruff config:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "G"]  # +G: logging-format
```

The `G` rule flags f-strings inside `logger.*` calls.

### What NOT to log

- Tool input arguments at INFO (they may contain user-content
  fragments). Use DEBUG for argument details.
- Embedding vectors, full chunk text, raw PDF bytes.
- Exceptions silently swallowed (always either re-raise or
  `logger.exception` + return error envelope).

**Alternatives considered**:

- **structlog / structured JSON logs**: rejected for now — local
  single-user backend; JSON logs add ceremony without analytics
  consumption.
- **Custom logger setup per module**: rejected — `logging.getLogger(__name__)`
  + single basicConfig in `main` is the standard Python pattern;
  no reason to deviate.
- **f-strings everywhere** (in log calls): rejected — see above;
  consistency + linter alignment + lazy-eval.

**Revisit trigger**: backend graduates to multi-user / hosted
deployment (structured logs become useful for log aggregation);
OR debugging needs cross-tool correlation (suggests adding a
session-id correlation field to log records).

---

## 3. MCP error format

### Envelope

All tool responses are JSON-encoded `TextContent`. Success and
error paths share a single shape so callers can branch on a
sentinel field:

**Success** — bare result payload (Pydantic `model_dump`):

```json
{
  "manifests": [...],
  "total": 5,
  "scope_filtered": true
}
```

**Error** — sentinel `_error` key, no other top-level fields:

```json
{
  "_error": {
    "code": "input_validation",
    "message": "scope must be one of [universal, domain, state, project]",
    "details": {
      "field": "scope",
      "received": "global"
    }
  }
}
```

The sentinel `_error` is reserved across all Pydantic output models
in `pbs_mcp/schemas.py` — never use it as a model field name.

### Error codes

| Code | When |
|---|---|
| `input_validation` | Pydantic input validation failed (wrong types, missing required fields, illegal enum value). |
| `config_missing` | `office_config.load()` raises `OfficeConfigNotFoundError` or equivalent — caller should route user to `setup-office`. |
| `config_invalid` | Office-config file present but malformed / schema-violating. Caller should surface to user, not retry. |
| `not_found` | Requested resource (manifest, baustein, project) doesn't exist. Distinct from `not_in_scope`. |
| `not_in_scope` | Resource exists but the active office scope filters it out. Caller may suggest scope adjustment. |
| `corpus_unavailable` | LanceDB / embedder / reranker not loadable — backend not ready. Fail loud. |
| `tool_runtime` | Catch-all for unexpected exceptions inside a handler. Logged with `logger.exception`; surfaced with exception type-name in `details.exception_type`. |
| `external_api` | Outbound HTTP failed (network down, source URL 404, etc.). Caller may retry or use a fallback path. |
| `not_implemented` | Tool exists but the requested mode/option isn't built yet. Caller should not retry. |

Codes are stable identifiers — once shipped, don't rename.

### How handlers signal errors

Handlers raise typed exceptions; the server-level wrapper
(`server.call_tool`) catches and converts:

```python
# In a handler
class ToolError(Exception):
    code: str
    details: dict[str, Any]

    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}

# Use:
raise ToolError("not_in_scope",
                "domain Wind not in office scope",
                {"requested_domain": "Wind", "active_scope": ["PV-FFA"]})
```

The wrapper produces the envelope:

```python
except ToolError as e:
    return [TextContent(type="text", text=json.dumps(
        {"_error": {"code": e.code, "message": str(e), "details": e.details}},
        ensure_ascii=False, indent=2))]
except Exception as e:
    logger.exception("tool %s raised", name)
    return [TextContent(type="text", text=json.dumps(
        {"_error": {"code": "tool_runtime", "message": f"{type(e).__name__}: {e}",
                    "details": {"exception_type": type(e).__name__}}},
        ensure_ascii=False, indent=2))]
```

Domain-specific exception subclasses (`OfficeConfigNotFoundError`,
`AdapterResolutionError`, etc.) get re-raised inside the handler as
`ToolError("config_missing", ...)` etc., so the wrapper sees a
uniform shape.

### How skills consume errors

In skill protocols (and any MCP client code), parse the response
JSON and check for `_error`:

```
result = json.loads(tool_response.text)
if "_error" in result:
    code = result["_error"]["code"]
    if code == "config_missing":
        # route user to setup-office
    elif code == "not_in_scope":
        # surface to user with scope-adjust suggestion
    else:
        # surface message + details
else:
    # success — use result directly
```

Skill protocols document the error codes they expect to handle in
their `mcp_tools_required` declarations (one line per (tool, code)
pair if branching matters).

### Why JSON envelope (not `mcp.McpError`)

MCP protocol-level errors (raised via `raise mcp.McpError(...)`)
travel as JSON-RPC error responses. They're the right vehicle for
**protocol-level** problems (unknown method, malformed params at
the JSON-RPC layer). For **tool-execution** problems we want the
caller to branch on, the envelope-in-`TextContent` pattern is
better:

- The MCP Python SDK doesn't surface `McpError` details cleanly
  to many MCP clients (Claude Code includes); the message often
  flattens to a generic "tool failed."
- An envelope is uniform with the success path (both are JSON in
  `TextContent`) — single parse contract for skills.
- Errors carry structured `details` that protocol errors can't.

**Alternatives considered**:

- **`raise mcp.McpError(...)` for all errors**: rejected — see
  above; client-side fidelity insufficient for skill branching.
- **Plain string `TextContent` for errors** (current state):
  rejected — strings can't carry structured `details`; skills can
  only regex-match on message text, which couples skill code to
  error wording.
- **HTTP-style status codes** (200/400/500): rejected — codes are
  meant for protocol layer, not application semantics. Named
  string codes are more self-documenting.
- **Result type with `is_ok: bool`** (Pydantic discriminated
  union): considered — would be cleaner type-wise but breaks
  backward compatibility with the bare-payload success path. The
  `_error` sentinel preserves bare-payload success and only adds
  shape on the error path.

**Revisit trigger**: skills accumulate enough branching on error
codes that a discriminated-union result type would simplify the
parsing contract; OR a non-Claude-Code MCP client adopts pbs-mcp
and its error-handling contract conflicts with the envelope.

---

## Migration order

1. Create `tests/` directory + `conftest.py` (this can land before
   any tests — having the structure ready unblocks RAG-pipeline
   testing).
2. Add `G` to ruff selection + sweep existing log calls to convert
   f-strings → %-format. Small, mechanical.
3. Add `ToolError` exception class to `pbs_mcp/`. Update
   `server.call_tool` wrapper to catch it + emit envelope.
   Update existing handlers to raise `ToolError` instead of
   bare exceptions.
4. Document in skill `references/` files which error codes each
   tool emits (per skill that wraps an MCP tool).

Items 1 and 2 are independent; 3 must precede 4. Land in the same
PR as RAG-pipeline ingest additions, since those are the first
real consumers of the new conventions.
