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

- **structlog / structured JSON logs**: rejected for now — the
  log-format choice depends on the consuming aggregation system
  (CloudWatch / Datadog / Loki / Grafana / etc.), which is a
  per-deployment decision per #13 deployment flexibility.
  Designing a specific JSON shape now without knowing the
  consumer would lock the wrong format. Note: stdlib
  `logger.info("msg", extra={"k": "v"})` already supports
  structured key-value pairs without committing to a specific
  serialization; any code can use that today without changing
  this decision.
- **Custom logger setup per module**: rejected — `logging.getLogger(__name__)`
  + single basicConfig in `main` is the standard Python pattern;
  no reason to deviate.
- **f-strings everywhere** (in log calls): rejected — %-format
  defers interpolation to the moment a log handler decides to
  emit; f-strings always interpolate even when filtered out.
  Negligible at our scale, but it's also the linter's preference.

## Revisit trigger

First Tier-2 cloud deployment activates (per #13) and a specific
aggregation system is chosen (structured JSON shape gets a
real consumer); OR debugging needs cross-tool correlation
(suggests adding a session-id correlation field to log records).

**Note (session-11 retroactive review)**: prior framing "backend
graduates to multi-user / hosted deployment" was instance-anchored;
multi-user / cloud deployment IS the framework target per #13. The
real defer reason is chronological (aggregation system not chosen),
not "PBS doesn't need it yet."
