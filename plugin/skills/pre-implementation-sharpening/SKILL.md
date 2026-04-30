---
name: pre-implementation-sharpening
description: Use at implementation-start moment for major architectural commitment (after architectural decisions are LOCKED in decision records; before implementation code is written). Surfaces operational/runtime/deployment details that decision-design phase intentionally deferred. Triggers via natural-language prompts including "let's start implementing X" / "before we implement, what details haven't we surfaced" / "implementation-readiness check" / "solidify before implement" / "lock down implementation details" / "challenge/surface/refine before we ship" (or original "challenge/review/refine before we ship") / "verify implementation readiness" / "what implementation details are we missing". Phase 2 of two-phase pattern (Phase 1 = decision-design-sharpening). AKA the challenge → surface → refine → solidify cycle applied at implementation-start moment. Output is implementation-readiness checklist + decision-record amendments for ~10-20% architectural flow-back. NOT for decision-formation moments (use decision-design-sharpening instead) or post-implementation drift detection (use drift-detection skills).
when_to_use: At IMPLEMENTATION-START MOMENT for major commitment. After architectural decisions are LOCKED in decision records; before implementation code is written. Fires when user signals "start implementing X" / "implementation-readiness check" / "solidify before implement" / "challenge/surface/refine implementation readiness" / "lock down implementation details" / "before we ship X". Do NOT use for decision-formation moments — that's decision-design-sharpening.
version: 0.2.0
---

# Pre-implementation sharpening (Phase 2)

Disciplined sharpening protocol applied at implementation-start moment, AFTER architectural decisions are LOCKED in decision records but BEFORE implementation code is written. Surfaces operational/runtime/deployment details that decision-design phase intentionally deferred.

## The cycle: challenge → surface → refine → solidify (Phase 2 specifics)

Refined from original "challenge/review/refine to solidify" framing; "review" sharpened to "surface" because the operation is bringing up what's NOT visible. "Sharpening" is the collapsed shorthand. Original "review" terminology still routes here.

### Per-term definitions (Phase 2 specifics)

| Term | Operation (Phase 2 specific) | Mode |
|---|---|---|
| **Challenge** | Stress-test implementation readiness: failure modes, performance edge cases, "what breaks at scale?" | Sparring mode (anti-oracle for implementation) |
| **Surface** | Bring up what's NOT visible: operational events, lifecycle, rate limiting, sessions, timeouts, cancellation, multi-tenancy, observability, security hardening, deployment concerns | Coverage mode (continuous awareness of operational concerns) |
| **Refine** | Improve specifics: tighten implementation details, add operational primitives; validate against existing decision records (watch for ~10-20% architectural flow-back) | Improvement + implicit validation |
| **Solidify** | Lock implementation-readiness checklist + decision-record amendments: persist for implementation reference | Decision/output (defensible implementation choices) |

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
- Operational events (lifecycle, monitoring)
- Rate limiting + budgets
- Session continuation semantics
- Timeouts (wall-clock vs idle vs max-turns)
- Cancellation support
- Multi-tenant isolation (if multi-user)
- Health checks + observability
- Error boundaries + failure signaling
- Deployment-specific concerns (per deployment tier/scale)
- Infrastructure prerequisites
- Integration test surface

Comprehensive readiness checklist; do FULL pass upfront.

### WAIT for user signal to run further rounds

Same user-trigger discipline as decision-design phase. AI does NOT auto-run round 2.

USER-TRIGGERED rounds outperform AI-self-triggered rounds because external-perspective friction forces AI past its self-validation comfort threshold.

### Round 2: First implementation-detail sharpening (USER-TRIGGERED)

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

### Output: Implementation-readiness checklist + decision-record amendments

After 2-3 rounds:
- Implementation-readiness checklist (concrete deliverables per implementation phase)
- Decision-record amendments for ~10-20% architectural findings that surface in pre-implementation rounds
- Persist via chat-first-then-file pattern

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

**Empirical validation hypothesis**: pre-implementation phase rounds also follow 2-3 sweet spot per decomposed sub-implementation. Refine as data accumulates.

## Layered coverage observation (Phase 2 specific)

Each round at pre-implementation phase covers a different operational concern layer:

| Round | Layer of concern |
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

## Composition with other skills

| Skill type | Composition |
|---|---|
| `decision-design-sharpening` | Phase 1 of same pattern; fires at decision-formation moment, NOT at implementation-start |
| Drift-detection skills (e.g., audit) | Operate POST-implementation; this skill operates BEFORE implementation begins |
| Soundness-review skills (e.g., design-review) | Operate POST-implementation; same — this skill before implementation |
| Orchestrator skills | Could route to this skill when implementation phase begins for major commitment |
| Framing/scoping skills | Frame task before work begins; this skill operates AFTER decisions locked, BEFORE implementation |

## Output

Per round:
- Surface implementation concerns (operational + occasional architectural findings) as structured chat content
- Wait for user accept/reject/refine
- After accepted refinements: incorporate into implementation-readiness checklist
- After 2-3 rounds: persist checklist + decision-record amendments via chat-first-then-file pattern

## Audit-trail integration (optional; composable with audit-trail infrastructure if available)

If deployment has audit-trail infrastructure, each sharpening round can emit:
- `event_kind=sharpening_round_started` with `round_number` + `decision_kind` + `phase=pre_implementation`
- `event_kind=sharpening_round_completed` with `refinements_surfaced` count + `expansion_count` + `architectural_findings_count`

Composes with audit-trail-as-canonical-source pattern + later-defensibility.

---

## PBS-specific empirical validation (PBS deployment notes; remove/replace for other deployments)

**This section is PBS-deployment-specific and should be removed or replaced when this skill is elevated to a global plugin or adopted by another deployment.**

### Deployment metadata
- `department: office` (PBS-specific via #12 office-vs-department modularization)

### Empirical validation source
This skill emerged from PBS session 12 (2026-04-30) #21 SDK deep-read multi-round sharpening work. Pattern discovered + validated across decision-design phase rounds; pre-implementation phase rounds 2-3 sweet spot is preliminary observation pending empirical validation at PBS commitments #9 (entity gate) / #11 (Cowork integration) / #13 (deployment flexibility) implementation starts.

### PBS VISION axis mappings
PBS-specific terminology citations for the cycle:
- **Challenge** → cited in PBS as VISION axis 2 (sparring partner mode; per `VISION.md` §200-235 / Vivienne Ming research)
- **Surface** → cited in PBS as VISION axis 1 (intertwining-AI-workflow; continuous awareness of operational concerns)
- **Refine** → improvement + validation against PBS architectural disciplines (per `ARCHITECTURE.md`)
- **Solidify** → cited in PBS as VISION axis 3 (authorship preservation; defensible implementation choices)

### PBS skill cross-references
This skill composes with PBS skills:
- `decision-design-sharpening` (Phase 1 of two-phase pattern)
- `audit` (drift-detection POST-implementation)
- `design-review` (soundness-review POST-implementation)
- `frame-task` (framing BEFORE work — pre-RAG commitment #8)
- `orchestrator` (workflow routing)

### PBS source memory
- `memory/feedback_pre_decision_sharpening.md` — full theoretical grounding + empirical observations
- `memory/feedback_full_monty_upfront.md` — round-1 comprehensiveness discipline
- `memory/feedback_propose_before_commit.md` — chat-first-then-file discipline

### PBS commitment context
- ROADMAP commitment #23 — local skill scaffolded session 12; future global plugin elevation deferred to post-marketplace decision (per ROADMAP v3 marketplace framing)
- Audit-trail integration composes with PBS audit-trail v2 retrofit per ROADMAP #6
- Architectural finding flow-back examples (R6 per-tenant isolation; P3 per-substrate extension Protocols pattern) discovered session 12 during Substrate Protocol synthesis pre-implementation surfacing
