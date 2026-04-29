# Decision: backend logging

**Status**: ACCEPTED — session 5 (2026-04-29).
**Convention reference**: `docs/backend-conventions.md` §2.

## Verdict

Standard `logger = logging.getLogger(__name__)` per module.
`basicConfig` happens once in `server.main`. Output to stderr
(stdout reserved for MCP JSON-RPC). INFO default; switch to DEBUG
via `PBS_LOG_LEVEL=DEBUG` env var. No structured logging. Use
%-format in log calls (lazy-eval; ruff `G` rule); never f-strings
inside `logger.*` calls.

## Alternatives considered

- **structlog / structured JSON logs**: rejected for now — local
  single-user backend; JSON logs add ceremony without analytics
  consumption.
- **Custom logger setup per module**: rejected — `logging.getLogger(__name__)`
  + single basicConfig in `main` is the standard Python pattern;
  no reason to deviate.
- **f-strings everywhere** (in log calls): rejected — %-format
  defers interpolation to the moment a log handler decides to
  emit; f-strings always interpolate even when filtered out.
  Negligible at our scale, but it's also the linter's preference.

## Revisit trigger

Backend graduates to multi-user / hosted deployment (structured
logs become useful for log aggregation); OR debugging needs
cross-tool correlation (suggests adding a session-id correlation
field to log records).
