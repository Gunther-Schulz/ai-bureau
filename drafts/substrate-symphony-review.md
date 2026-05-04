STATUS: DRAFT — not locked, not final, candidate among many. Future amendment to `arch/substrate.md` NOT yet sharpened or DR-locked.

# Substrate Pattern A — Symphony §10 review

## Origin context

Surfaced 2026-05-04 during process-kit session reviewing openai/symphony for relevance. Symphony's §10 (Agent Runner Protocol) is more prescriptive at the subprocess+turn level than pbs-bureau's `arch/substrate.md` Surface contract. Three gaps surfaced as candidate amendments to substrate Pattern A topic.

NOT yet validated against `docs/decisions/` (whether the gaps were intentionally left open is unverified — first maturity-test gate before graduation).

## Three candidate gaps

### Gap 1 — Trust posture documentation requirement per substrate Implementation

**Symphony reference** (`SPEC.md:1025-1031`):

> "Each implementation MUST document its chosen approval, sandbox, and operator-confirmation posture. Approval requests and user-input-required events MUST NOT leave a run stalled indefinitely."

**Current pbs-bureau coverage**: `arch/substrate.md` §11 has per-shape error semantics (fail-closed for practitioner / fail-open for autonomous-business / fail-open for personal-OS — `arch/substrate.md:305-309`). Per-implementation declarations in §4 list configuration schema + error mapping + deployment-tier compatibility but NOT trust-posture documentation.

**Gap**: each substrate Implementation should document its OWN trust posture beyond what's inherited from shape-policy. Shape-policy + implementation-policy are different layers.

**Candidate amendment**: add to `arch/substrate.md` §4 "Per-implementation declares" sub-bullet — "Approval/sandbox/user-input-required policy (implementation-documented; composes with shape-policy fail-closed/open semantics from §11)"

### Gap 2 — Tool call non-stalling architectural commitment

**Symphony reference** (`SPEC.md:1039-1045`):

> "If the agent requests a dynamic tool call that is not supported, return a tool failure response using the targeted protocol and continue the session. This prevents the session from stalling on unsupported tool execution paths."

**Current pbs-bureau coverage**: `arch/substrate.md` §2.B MCP server registration covers tool registration + discovery API but does NOT make non-stalling on unsupported tool requests an architectural invariant.

**Gap**: substrate-level invariant missing — agents can request unregistered tools; substrate must handle non-stallingly. This is a real failure mode (agent stalls on unsupported tool execution path).

**Candidate amendment**: add to `arch/substrate.md` §2.B as architectural invariant — "Substrate MUST NOT stall on unsupported dynamic tool requests; unsupported tool requests resolve to typed tool failure response so agent loop continues"

### Gap 3 — Turn-lifecycle states

**Symphony reference** (`SPEC.md:974-981`):

> "Targeted-protocol turn completion signal -> success / failure signal -> failure / cancellation signal -> failure / turn timeout -> failure / subprocess exit -> failure"

**Current pbs-bureau coverage**: `arch/substrate.md` §2.A Agent loop entry mentions max-turns + AgentRunResult status; §11 includes AgentRunFailure category. Turn-level granularity (completed / failed / cancelled / timed-out / runtime-failure) is NOT separated in §2.A.

**Gap**: turn outcomes not enumerated at architectural level. AgentRunResult status field captures finer-grain failure but the architectural enumeration of turn outcomes is implicit, not explicit.

**Candidate amendment**: add to `arch/substrate.md` §2.A sub-bullet — turn outcomes enumerated (success / agent-failure / cancellation / timeout / runtime-failure) with mapping to AgentRunResult status field

## What from Symphony §10 is at WRONG abstraction level (NOT borrowed)

- **Subprocess Launch Contract** (`SPEC.md:925-933` — `bash -lc <codex.command>`): pbs-bureau substrate is NOT subprocess-coupled by design. Claude Agent SDK is in-process Python (`arch/substrate.md:101`); MS AF is middleware-based; only Codex is subprocess
- **Codex thread/turn semantics** (`SPEC.md:962-968`): provider-specific
- **`bash -lc` invocation**: host-OS specific

These would lower abstraction inappropriately if borrowed.

## Maturity test (what graduates this draft to locked content)

This draft graduates when ALL hold:

1. The three candidate gaps are individually validated (read `docs/decisions/` to confirm gaps are real, not intentionally-deferred)
2. Round 1 + Round 2 sharpening per `disciplines/03-pre-decision-sharpening.md` applied to each candidate amendment
3. User locks each amendment en bloc (per `feedback_judgment_and_automate.md`)
4. ARCH amendment cluster-execution per Phase 3.5+ pattern (Wave-1 Writer + Reviewer / Wave-2 Cascade-Writer + Reviewer / Wave-2.5 Cleanup-Writer + integrated recheck)
5. Composes-with check: GLOSSARY back-check (per `MAINTENANCE.md` bidirectional cascade) + peer ARCH §19 reciprocal back-mentions + DR provenance per Layer 4

Until all 5 hold, treat as exploratory thinking for future amendment work. Per `drafts/README.md` discipline: drafts can be discarded; not a failure if this never matures.

## Honest basis

Source: `arch/substrate.md` direct read (lines 1-120 + 200-320; partial coverage), `SPEC.md` direct read (lines 1-200 + 700-1050 + 1900-2110; partial coverage). NOT verified: `docs/decisions/` related to substrate (whether gaps were intentionally deferred — first maturity-test gate). Comparison done at architectural level; subprocess+turn-level patterns excluded by design (different abstraction).

## Backlog reference

See `BACKLOG.md` Phase 3.7 Cross-cutting investigations for backlog entry pointing here.
