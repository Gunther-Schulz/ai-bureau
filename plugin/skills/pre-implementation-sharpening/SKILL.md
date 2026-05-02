---
name: pre-implementation-sharpening
description: Use at implementation-start moment for major architectural commitment (after architectural decisions are LOCKED in decision records; before implementation code is written). Surfaces operational/runtime/deployment details that decision-design phase intentionally deferred. Triggers via natural-language prompts including "let's start implementing X" / "before we implement, what details haven't we surfaced" / "implementation-readiness check" / "solidify before implement" / "lock down implementation details" / "challenge/surface/refine before we ship" (or original "challenge/review/refine before we ship") / "verify implementation readiness" / "what implementation details are we missing". Phase 2 of two-phase pattern (Phase 1 = decision-design-sharpening). AKA the challenge → surface → refine → solidify cycle applied at implementation-start moment. Applies Pareto discipline (refine for Pareto improvement, not for change) per round. Output is implementation-readiness checklist + decision-record amendments for ~10-20% architectural flow-back. NOT for decision-formation moments (use decision-design-sharpening instead) or post-implementation drift detection (use drift-detection skills).
when_to_use: At IMPLEMENTATION-START MOMENT for major commitment. After architectural decisions are LOCKED in decision records; before implementation code is written. Fires when user signals "start implementing X" / "implementation-readiness check" / "solidify before implement" / "challenge/surface/refine implementation readiness" / "lock down implementation details" / "before we ship X". Do NOT use for decision-formation moments — that's decision-design-sharpening.
version: 0.3.1
---

# Pre-implementation sharpening (Phase 2)

> **Extends `sharpen`** (the generic critical-pass skill) with formality specific to implementation-start moment: operational/runtime-detail surfacing + DR-amendment flow-back (~10-20% architectural findings) + implementation-readiness checklist output. The core mechanic (read → critical lens → Pareto-graded positions → counter-validation → self-check) is inherited from `sharpen`; this skill adds the context-specific procedure.

Disciplined sharpening protocol applied at implementation-start moment, AFTER architectural decisions are LOCKED in decision records but BEFORE implementation code is written. Surfaces operational/runtime/deployment details that decision-design phase intentionally deferred.

## Why this skill exists (vs relying on Claude's native sharpening behavior)

Claude naturally sharpens proposals when prompted. This explicit skill adds:

| Value-add | Why it matters |
|---|---|
| **Discipline structure** | Explicit 4-phase cycle + 2-3 round pattern + Pareto check + decomposition trigger applied to operational concerns — Claude's native sharpening lacks this structure |
| **Repeatability** | Same methodology applies across implementation phases; doesn't depend on Claude's mood/context |
| **Composition** | Composes explicitly with decision-design-sharpening (Phase 1) + drift-detection + soundness-review skills; native sharpening doesn't compose |
| **Architectural flow-back discipline** | Explicit recognition that ~10-20% of pre-implementation findings are architectural REVISIONS that flow back to upstream DRs; native sharpening doesn't track this |
| **Anti-bias mechanism** | Explicit user-trigger discipline + Pareto check counters self-validation bias; native sharpening doesn't have these mechanisms |

## The cycle: challenge → surface → refine → solidify (Phase 2 specifics)

Refined from original "challenge/review/refine to solidify" framing; "review" sharpened to "surface" because the operation is bringing up what's NOT visible. "Sharpening" is the collapsed shorthand. Original "review" terminology still routes here.

### Per-term definitions (Phase 2 specifics)

| Term | Operation (Phase 2 specific) | Mode |
|---|---|---|
| **Challenge** | Stress-test implementation readiness: failure modes, performance edge cases, "what breaks at scale?" | Sparring mode (anti-oracle for implementation) |
| **Surface** | Bring up what's NOT visible: operational events, lifecycle, rate limiting, sessions, timeouts, cancellation, multi-tenancy, observability, security hardening, deployment concerns | Coverage mode (continuous awareness of operational concerns) |
| **Refine** | Improve specifics: tighten implementation details, add operational primitives; validate against existing decision records (watch for ~10-20% architectural flow-back) | Improvement + implicit validation |
| **Solidify** | Lock implementation-readiness checklist + decision-record amendments: persist for implementation reference | Decision/output (commit moment AFTER all rounds; not per-round operation) |

### Round-vs-phase relationship

Rounds and phases are NOT 1:1. Each round runs the full cycle conceptually but emphasizes different layers:
- **Round 1 (full monty)**: emphasizes obvious operational concerns (lifecycle + errors + timeouts + basic observability)
- **Round 2 (user-triggered)**: emphasizes failure modes + performance + security + monitoring
- **Round 3 (when run)**: emphasizes compliance + audit + rollout + integration surface
- **Solidify**: COMMIT moment after all rounds; persists implementation-readiness checklist + DR amendments

## When this skill fires

- AT IMPLEMENTATION-START MOMENT for major architectural commitment
- User signals "let's start implementing X" / "before we implement, what details haven't we surfaced" / "implementation-readiness check" / "solidify before implement"
- AFTER architectural decisions are LOCKED in decision records (decision-design phase complete)
- BEFORE implementation code is written

NOT for:
- Decision-formation moments (use `decision-design-sharpening` instead)
- Post-implementation drift detection (use drift-detection skills)
- Post-implementation soundness review (use soundness-review skills)
- Trivial implementations

## Phase 2 procedure (2-3 rounds preliminary — refine empirically)

**Preliminary observation**: 2-3 rounds likely sweet spot per implementation phase, mirroring decision-design phase pattern. Refine empirically as implementation phases happen.

### Round 1: AI full monty (initial implementation-readiness pass)

When implementation begins, AI surveys the locked decision records and surfaces:
- **Operational events** (lifecycle, monitoring)
- **Rate limiting + budgets**
- **Session continuation semantics**
- **Timeouts** (wall-clock vs idle vs max-turns)
- **Cancellation support**
- **Multi-tenant isolation** (if multi-user)
- **Health checks + observability**
- **Error boundaries + failure signaling**
- **Deployment-specific concerns** (per deployment tier/scale)
- **Infrastructure prerequisites**
- **Integration test surface**

Comprehensive readiness checklist; do FULL pass upfront.

### WAIT for user signal to run further rounds

Same user-trigger discipline as decision-design phase. AI does NOT auto-run round 2.

USER-TRIGGERED rounds outperform AI-self-triggered rounds because external-perspective friction forces AI past its self-validation comfort threshold.

### Round 2: First implementation-detail sharpening (USER-TRIGGERED)

Apply Pareto discipline: each surfaced refinement should be Pareto-improving (better in some dimension without being worse in others). If not Pareto-improving, force "why?" challenge — could be manufactured criticism past where evidence warrants.

Stress-test what round 1 missed:
- **Failure modes**: timeouts, crashes, cascading failures, rollback semantics
- **Performance characteristics**: throughput, latency, resource consumption
- **Migration paths**: from current state to implemented state
- **Observability dashboards**: what metrics matter; alert thresholds
- **Security hardening**: input validation, secret management, sandboxing
- **Compliance + audit requirements**: PII handling, regulatory requirements
- **Testing strategy**: unit, integration, end-to-end, property-based
- **Rollout strategy**: gradual rollout, feature flags, kill switches

### Round 3 (OPTIONAL): Second implementation-detail sharpening (USER-TRIGGERED)

Run when implementation surface is complex (e.g., implementing a foundational architectural commitment that spans multiple architectural surfaces).

Surfaces additional implementation concerns that round 2 missed.

**Empirical sweet-spot pattern**:
- Narrow implementation surface (single bundle): 2-round sweet spot; round 3 yields diminishing returns
- Broad implementation surface (foundational commitment spanning multiple surfaces): up to 3-round sweet spot

### Output: Implementation-readiness checklist + decision-record amendments

After 2-3 rounds:
- Implementation-readiness checklist (concrete deliverables per implementation phase)
- Decision-record amendments for ~10-20% architectural findings that surface in pre-implementation rounds
- Persist via chat-first-then-file pattern

### Auto-add to BACKLOG.md (v0.3.1)

When pre-implementation sharpening surfaces items that aren't actionable in current scope (e.g., implementation-readiness checklist items deferred to next phase; DR amendments needed for related decisions; cross-cutting concerns spanning multiple implementation phases), add corresponding entries to `BACKLOG.md` under the relevant phase section in same commit. BACKLOG is the central work-item tracker.

### Post-round self-check (v0.3.1)

At the end of each round (after surfacing findings + applying Pareto verdicts), AI explicitly evaluates against termination signals + sweet-spot pattern + flow-back rate (architectural-finding percentage) and commits a position:

- **STABLE — implementation-readiness is sufficient** with reasons (cite: "Round N yielded 0 substantive refinements", "narrow implementation surface = 2-round sweet spot", "flow-back rate within expected ~10-20% range")
- **CONTINUE — Round N+1 warranted** with reasons (cite specific category that surfaced incomplete coverage: lifecycle gaps, transport unspecified, error-handling deferred, deployment-tier ambiguity)

User confirms or overrides. Counters self-validation bias in BOTH directions: defaulting to "continue" because more rounds feel productive (manufactured-criticism risk) vs defaulting to "stable" because shipping is comfortable (premature-implementation risk). Forcing explicit position with rationale makes the self-check observable.

The check is mechanical — termination signals from the next section are the discriminator. Don't override signals with vague "feels stable" or "could go deeper" — name the specific signal.

## Round termination signals

Lock + persist when ANY of these signals fire:

| Signal | Action |
|---|---|
| User explicitly says "ready to implement" / "checklist accepted" / "lock" | Lock immediately + persist checklist + DR amendments |
| Round surfaces 0 substantive refinements (after Pareto screen) | Strong signal implementation-readiness is sufficient OR next round = manufactured criticism. Default to LOCK |
| 2 rejected rounds in a row (no refinements accepted) | Suggest: "rounds are surfacing nothing accepted; either implementation-readiness is sufficient (lock) OR scope needs reframing (decompose implementation phase)" |
| User requests round 4+ at pre-implementation phase | Respond: "round 4+ at pre-implementation phase signals implementation phase is too large; recommend decomposing this implementation into sub-implementations" |
| AI surfaces only manufactured criticism (Pareto-fail refinements) | Respond: "refinements surfaced are not Pareto-improving; recommend lock OR explicit acknowledgment of manufactured-criticism territory" |

## CRITICAL: Architectural finding flow-back

**Watch for ~10-20% genuine architectural findings during pre-implementation sharpening**:

These are findings that AREN'T just operational details — they REVISE earlier architectural decisions. Examples:

- Multi-tenant isolation discovered during operational sharpening — but the decision (shared substrate per tenant-group vs per-user-isolated) is architecturally significant. Flows back to upstream decision record.
- New architectural pattern surfaced during what was supposed to be operational-detail sharpening — flows back as candidate for new architectural discipline section.

When a pre-implementation sharpening round surfaces architectural finding:
1. STOP at that finding; surface to user
2. Decide: is this an architectural revision OR just an operational detail?
3. If revision: flow back as decision-record amendment; potentially trigger `decision-design-sharpening` on the affected decision record
4. If operational: continue with implementation-readiness checklist

## Decomposition trigger applies (same as Phase 1)

If pre-implementation sharpening genuinely needs >3 rounds, that signals implementation phase is too large. Decompose:
- Implementation might decompose into per-bundle sub-implementations (per the architectural commitment's bundle structure)
- Each bundle gets its own pre-implementation sharpening rounds (2-3 per bundle)

**Pareto + decomposition interaction**: if a refinement is genuinely not Pareto-improving (real tradeoff) AND isn't manufactured criticism, that's a SIGNAL that decomposition may be missing. The trade-off should be evaluated at sub-implementation granularity.

**Empirical validation hypothesis**: pre-implementation phase rounds also follow 2-3 sweet spot per decomposed sub-implementation. Refine as data accumulates.

## Layered coverage observation (Phase 2 specific)

Each round at pre-implementation phase EMPHASIZES (but doesn't exclusively cover) a different operational concern layer:

| Round | Layer of concern emphasized |
|---|---|
| **Round 1** | Obvious operational concerns (lifecycle, errors, timeouts, basic observability) |
| **Round 2** | Failure modes + performance + migration + monitoring + security |
| **Round 3 (optional)** | Compliance + audit + rollout strategy + testing strategy + integration surface |

If round content shifts to architectural decisions at pre-implementation phase, that's a signal to FLOW BACK as architectural finding to upstream decision record.

## EXPANSION vs REVISION calibration (Phase 2)

Pre-implementation phase rounds yield ratio:
- ~80-90% EXPANSIONS (operational details, implementation specifics)
- ~10-20% genuine ARCHITECTURAL FINDINGS (flow back to decision records)

Watch for the architectural findings; they're the high-signal moments worth deep attention.

**Pareto calibration**: EXPANSIONS are Pareto-improving by nature (add operational coverage without breaking existing decisions). ARCHITECTURAL FINDINGS can be Pareto-improving OR worth-the-tradeoff — flowing changes back to upstream decision records might lose something to gain something; require explicit tradeoff justification.

## Inter-round state management

Inter-round state is conversation-context by default. For long sessions OR sessions spanning multiple chat turns, recommend tracking in chat as a "round log":
- Surfaced refinements per round
- Per-refinement disposition (accepted / rejected / deferred / flow-back-to-DR)
- Pareto verdict per refinement

Optionally persist to session-store if substrate supports session continuation.

## Phase 1 → Phase 2 transition

Phase 1 (`decision-design-sharpening`) completes when DR locked + persisted. Phase 2 (this skill) fires AT IMPLEMENTATION-START MOMENT — NOT immediately after Phase 1 completion.

There may be substantial time gap between Phase 1 lock and Phase 2 trigger (could be hours, days, or weeks depending on when implementation begins).

This skill reads the locked DR + sharpens against operational/runtime concerns. Architectural findings flow back to Phase 1 DR as amendments (potentially triggering new Phase 1 sharpening on the affected DR — per ~10-20% architectural flow-back).

## Composition with other skills

| Skill type | Composition |
|---|---|
| Framing/scoping skills (e.g., frame-task pattern) | Operate UPSTREAM of decision-design phase (Phase 1) — long before this skill fires |
| `decision-design-sharpening` | Phase 1 of same pattern; fires at decision-formation moment, NOT at implementation-start |
| Drift-detection skills (e.g., audit) | Operate POST-implementation; this skill operates BEFORE implementation begins |
| Soundness-review skills (e.g., design-review) | Operate POST-implementation; same — this skill before implementation |
| Orchestrator skills | Could route to this skill when implementation phase begins for major commitment |

## Output specification

Concrete output of complete pre-implementation-sharpening session:

- **Implementation-readiness checklist** (markdown OR YAML structured)
  - Concrete deliverables per implementation phase
  - Operational concerns covered (per round emphasis)
  - Pareto verdict per item (must-have vs nice-to-have vs deferred)
- **Decision-record amendments** (the ~10-20% architectural flow-back)
  - Specific DRs affected
  - Per-DR amendment proposed
  - Sharpening lineage (which round surfaced; why architectural)
- **Rounds-summary section** noting:
  - Round count + which rounds were user-triggered
  - Refinements incorporated count + breakdown (X expansions; Y architectural-findings)
  - Pareto verdict per refinement

## Concrete invocation example

```
1. Major architectural commitment ready for implementation
   → User: "let's start implementing #9 entity gate" OR
     "implementation-readiness check before #9"

2. Skill activates (Phase 2, Round 1)
   → AI surveys locked DRs (substrate-protocol-design.md +
     in-process-mcp-server.md + permission-abstraction.md +
     subagent-primitives-adoption.md + eval-framework-adoption.md)
   → AI surfaces comprehensive readiness checklist + operational
     concerns

3. User reviews + triggers Round 2
   → "what about failure modes / migration / security?"
   → AI surfaces deeper operational sharpening
   → Pareto verdict per refinement

4. (Optional) User triggers Round 3
   → AI surfaces compliance / audit / rollout concerns

5. Architectural finding flow-back during a round
   → AI: "this finding is architectural, not just operational"
   → User: "flow back to substrate-protocol-design.md as amendment"
   → AI: "noted; will draft amendment + propose"

6. User triggers lock
   → "checklist accepted, ready to implement"
   → AI persists implementation-readiness checklist + DR amendments
     (chat-first-then-file)

7. Output: implementation-readiness checklist persisted; DR
   amendments persisted; sharpening rounds metadata recorded
```

## Audit-trail integration (optional; composable with audit-trail infrastructure if available)

If deployment has audit-trail infrastructure, each sharpening round can emit:
- `event_kind=sharpening_round_started` with `round_number` + `decision_kind` + `phase=pre_implementation`
- `event_kind=sharpening_round_completed` with `refinements_surfaced` count + `expansion_count` + `architectural_findings_count`

Composes with audit-trail-as-canonical-source pattern + later-defensibility.
