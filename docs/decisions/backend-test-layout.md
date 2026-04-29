# Decision: backend test layout

**Status**: ACCEPTED — session 5 (2026-04-29).
**Convention reference**: `docs/backend-conventions.md` §1.

## Verdict

`backend/mcp-server/tests/` at the top level, split into `unit/`
+ `integration/` subdirs. Pytest. Real in-memory DBs (LanceDB,
SQLite) over mocks; fixtures in `conftest.py`. Tests mirror src
module structure under `unit/`.

## Alternatives considered

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

## Revisit trigger

Test suite runtime exceeds ~30s on CI and slows the dev loop
(suggests aggressive integration-marking or selective mocking); OR
a full external dependency (e.g. a paid API) enters the stack and
mock-based tests become unavoidable.
