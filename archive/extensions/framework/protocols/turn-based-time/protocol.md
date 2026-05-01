---
id: turn-based-time
label: Turn-Based Time Model
type: protocol
status: active
last_updated: 2026-05-01

framework_kind: protocol
framework_key: turn-based-time

display_name: Turn-Based Time Model
protocol_kind: time
semver: "0.1.0"
pydantic_class: extensions.framework.protocols.turn_based_time.TurnBasedTimeProtocol

shape_compat:
  - practitioner
  - personal-OS
  - knowledge-graph

substrate_compat:
  - claude-agent-sdk
  - ms-agent-framework

option_b_axiom: null

failure_modes:
  - mode: agent_run_exceeds_max_turns
    recovery: return_max_turns_reached_status; preserve_partial_output; emit_audit_event
  - mode: idle_timeout_during_turn
    recovery: cancel_run; preserve_state; allow_user_resume_via_continuation
  - mode: substrate_does_not_support_turn_continuation
    recovery: emit_warning; require_session_id_for_resume_attempts
---

# Turn-Based Time Model Protocol

## What this implementation does

Practitioner workflow is turn-based: practitioner engages → AI responds → practitioner reviews → AI continues. Between practitioner turns, AI does NOT make accountability-bearing decisions autonomously.

Concrete enforcement (per Substrate Protocol common surface):
- `run_agent(prompt, max_turns, ...)` — bounded turn count per invocation; substrate enforces
- Status field on `AgentRunResult` includes `max_turns_reached` for graceful handling
- Session continuation semantics (per substrate-protocol-design.md round 3 R3): `session_id: str | None` allows resuming a turn-based session across run_agent invocations
- Wall-clock timeout + idle timeout (per round 3 R4): bound runaway turns; preserve partial output
- Cancellation support (per round 3 R5): `cancel_agent_run(session_id, reason)` + `AGENT_RUN_CANCELED` hook event

This Protocol implements `default_configs.time_model: turn-based`. Maps cleanly to:
- Claude Agent SDK's session model (CASDK is turn-based natively)
- MS Agent Framework's AgentExecutor (MS AF supports both turn-based and long-running; this Protocol uses turn-based mode)

Long-running mode (autonomous-business shape default `time_model: long-running`) requires substrate adapter implementation per shape-extension W4 watch-list — concrete adapter awaits first autonomous-business shape extension built.

## Configuration knobs

- **`max_turns_per_run: int`** (default `50`) — upper bound on turns per `run_agent` invocation; prevents runaway loops
- **`wall_clock_timeout: timedelta | null`** (default `null` — no timeout) — overall time budget per run
- **`idle_timeout: timedelta | null`** (default `5 minutes`) — abandon if no progress for this duration
- **`session_continuation_window: timedelta`** (default `24 hours`) — how long a session_id remains valid for resumption

## Compat constraints

**Shapes**:
- ✅ practitioner (default time Protocol; matches turn-based practitioner workflow)
- ✅ personal-OS (single-human turn-based interaction)
- ✅ knowledge-graph (queries are turn-based; no long-running corpus loop needed)
- ❌ autonomous-business — uses `long-running-time` (operator-supervised AI workforce runs continuously between approval cycles; substrate adapter required per W4 watch-list)
- ⚠ federation — depends on per-node shape; turn-based fits if practitioner-shape nodes
- ⚠ hybrid — explicit per hybrid extension; may compose turn-based + long-running for different sub-areas

**Substrates**:
- ✅ Claude Agent SDK — native turn-based session model; no special handling needed
- ✅ MS Agent Framework — supports turn-based mode out of box; `run_agent` wraps AgentExecutor in turn-based config

## Failure modes + recovery

| Mode | Detection | Recovery |
|---|---|---|
| Agent run exceeds max_turns | Substrate counts turns; `run_agent` returns `max_turns_reached` status when limit hit | Preserve partial output (per AgentRunResult.final_output partial state); emit audit event; user can resume via session_id continuation |
| Idle timeout during turn | Substrate detects no progress for `idle_timeout` | Cancel run; preserve state at last checkpoint; allow user resume via continuation |
| Wall-clock timeout | Substrate detects elapsed time > `wall_clock_timeout` | Same as idle_timeout — cancel + preserve + resumable |
| User cancellation | User invokes `cancel_agent_run(session_id, reason)` | Substrate cancels; emit `AGENT_RUN_CANCELED` hook event; preserve state |
| Substrate doesn't support continuation | Some substrates may not implement session_id resumption fully | Warning emitted on first resumption attempt; user notified; session restarts from beginning |
| Stale session resume | session_id older than `session_continuation_window` | Reject resume attempt; user must start new session |

## Option B axiom binding

`option_b_axiom: null` — time model is configurable per shape (turn-based / long-running). Not one of the 3 non-overridable axioms.

However, **time model composes with trust model**: turn-based aligns naturally with practitioner-judgment-trust (practitioner engages between turns; gates fire at turn boundaries). Long-running aligns with budget-policy-trust (operator authorizes budget; AI runs within bounds between approval cycles).

Time model + trust model + author primitive together define the shape's accountability posture. Mismatched compositions (e.g., long-running time + practitioner-judgment trust + per-output author granularity) would be incoherent — gate validation at workspace boot rejects.

## Migration / version evolution

v0.1.0 — initial implementation; max_turns + idle_timeout + wall_clock_timeout + cancellation + session continuation.

**Future versions**:
- v0.2.0 (long-running mode adapter — W4 resolution): when first autonomous-business shape extension surfaces, evaluate whether long-running mode is sufficient as a separate Protocol implementation OR requires substrate adapter beneath; decision depends on substrate-specific long-running primitives (CASDK session forking; MS AF workflow engine)
- v0.3.0 (per-axis turn budgets): if practitioner-shape deployments surface need for per-decision-class turn budgets (different limits for drafting vs reviewing), evaluate parameter expansion

## Cross-references

- `docs/decisions/substrate-protocol-design.md` — Substrate Protocol common surface (run_agent, max_turns, session continuation, cancellation, timeout); round 3 R3-R5 pre-implementation surfacing
- `docs/decisions/shape-extension-and-architectural-floor.md` — W4 watch-list (long-running runtime substrate adapter awaits first autonomous-business shape extension)
- `ROADMAP.md` #25 — Time Protocol pluggability scope
- `docs/decisions/entity-md-scope-model-restructure.md` — three-category scope model
