---
name: pre-implementation-sharpening
description: Use at implementation-start moment for major architectural commitment (e.g., #9 entity gate begins; #11 Cowork integration begins). Surfaces operational/runtime/deployment details that decision-design phase intentionally deferred. Triggers via natural-language prompts including "let's start implementing X" / "before we implement, what details haven't we surfaced" / "implementation-readiness check" / "solidify before implement" / "lock down implementation details" / "challenge/review/refine before we ship" / "verify implementation readiness" / "what implementation details are we missing". Phase 2 of two-phase pattern (Phase 1 = decision-design-sharpening). AKA the challenge/review/refine to solidify cycle applied at implementation-start moment. Output is implementation-readiness checklist + DR amendments for ~10-20% architectural flow-back. NOT for decision-formation moments (use decision-design-sharpening instead) or post-implementation drift detection (use audit/design-review).
when_to_use: At IMPLEMENTATION-START MOMENT for major commitment. After architectural decisions are LOCKED in DRs; before implementation code is written. Fires when user signals "start implementing X" / "implementation-readiness check" / "solidify before implement" / "challenge/review/refine implementation readiness" / "lock down implementation details" / "before we ship X". Do NOT use for decision-formation moments — that's decision-design-sharpening.
department: office
version: 0.1.0
---

# Pre-implementation sharpening (Phase 2)

**AKA the challenge/review/refine to solidify cycle applied at implementation-start moment** — this skill IS that operation, formalized as 2-3 disciplined rounds. The original framing (challenge → review → refine → solidify) describes what each round actually does; "sharpening" is the collapsed shorthand. Both terminologies map to this skill.

Disciplined sharpening protocol applied at implementation-start moment, AFTER architectural decisions are LOCKED in DRs but BEFORE implementation code is written. Surfaces operational/runtime/deployment details that decision-design phase intentionally deferred.

For Phase 1 (decision-design), see `decision-design-sharpening` skill.

For shared theoretical grounding (5 mechanisms / decomposition trigger / expansion-vs-revision / layered coverage hypothesis), see `memory/feedback_pre_decision_sharpening.md`.

## When this skill fires

- AT IMPLEMENTATION-START MOMENT for major architectural commitment
  - Examples: #9 entity gate implementation begins; #11 Cowork integration begins; #13 deployment flexibility implementation begins
- User signals "let's start implementing X" / "before we implement, what details haven't we surfaced" / "implementation-readiness check"
- AFTER architectural decisions are LOCKED in DRs (decision-design phase complete)
- BEFORE implementation code is written

NOT for:
- Decision-formation moments (use `decision-design-sharpening` instead)
- Post-implementation drift detection (use `audit` skill)
- Post-implementation soundness review (use `design-review` skill)
- Trivial implementations

## Phase 2 procedure (2-3 rounds preliminary — refine empirically)

**Preliminary observation**: 2-3 rounds likely sweet spot per implementation phase, mirroring decision-design phase pattern. Refine empirically as #9/#11/#13 implementation phases happen.

### Round 1: AI full monty (initial implementation-readiness pass)

When implementation begins, AI surveys the locked DRs and surfaces:
- Operational events (lifecycle, monitoring)
- Rate limiting + budgets
- Session continuation semantics
- Timeouts (wall-clock vs idle vs max-turns)
- Cancellation support
- Multi-tenant isolation (if Tier 2+)
- Health checks + observability
- Error boundaries + failure signaling
- Deployment-specific concerns (Tier 1/2/3 differences)
- Infrastructure prerequisites
- Integration test surface

Comprehensive readiness checklist per `memory/feedback_full_monty_upfront.md`.

### WAIT for user signal to run further rounds

Same user-trigger discipline as decision-design phase. AI does NOT auto-run round 2.

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

Run when implementation surface is complex (e.g., implementing #9 entity gate which spans multiple architectural surfaces).

Surfaces additional implementation concerns that round 2 missed.

### Output: Implementation-readiness checklist + DR amendments

After 2-3 rounds:
- Implementation-readiness checklist (concrete deliverables per implementation phase)
- DR amendments for ~10-20% architectural findings that surface in pre-implementation rounds (per `memory/feedback_pre_decision_sharpening.md` empirical observation)
- Persist amendments per `memory/feedback_propose_before_commit.md`

## CRITICAL: Architectural finding flow-back

**Watch for ~10-20% genuine architectural findings during pre-implementation sharpening**:

These are findings that AREN'T just operational details — they REVISE earlier architectural decisions. Examples:

- **R6 from Substrate Protocol round 3** (per-tenant isolation): surfaced during pre-implementation sharpening (round 3 was operational layer); BUT the decision (shared substrate per office vs per-user isolated) is architecturally significant. Flowed back to Substrate Protocol design DR.
- **P3 from R3d round 3** (per-substrate extension Protocols pattern): NEW architectural pattern surfaced during what was supposed to be subagent-adoption sharpening. Flowed back as new ARCH discipline candidate.

When a pre-implementation sharpening round surfaces architectural finding:
1. STOP at that finding; surface to user
2. Decide: is this an architectural revision OR just an operational detail?
3. If revision: flow back as DR amendment; potentially trigger decision-design-sharpening on the affected DR
4. If operational: continue with implementation-readiness checklist

## Decomposition trigger applies (same as Phase 1)

If pre-implementation sharpening genuinely needs >3 rounds, that signals implementation phase is too large. Decompose:
- #9 entity gate implementation might decompose into Bundles A/B/C/D/E (already planned per #9 ROADMAP entry)
- Each bundle gets its own pre-implementation sharpening rounds (2-3 per bundle)

**Empirical validation hypothesis**: pre-implementation phase rounds also follow 2-3 sweet spot per decomposed sub-implementation. Refine as data accumulates.

## Layered coverage observation (Phase 2 specific)

Each round at pre-implementation phase covers a different operational concern layer:

| Round | Layer of concern |
|---|---|
| **Round 1** | Obvious operational concerns (lifecycle, errors, timeouts, basic observability) |
| **Round 2** | Failure modes + performance + migration + monitoring + security |
| **Round 3 (optional)** | Compliance + audit + rollout strategy + testing strategy + integration surface |

If round content shifts to architectural decisions at pre-implementation phase, that's a signal to FLOW BACK as architectural finding to upstream DR.

## EXPANSION vs REVISION calibration (Phase 2)

Pre-implementation phase rounds yield ratio:
- ~80-90% EXPANSIONS (operational details, implementation specifics)
- ~10-20% genuine ARCHITECTURAL FINDINGS (flow back to DRs)

Watch for the architectural findings; they're the high-signal moments worth deep attention.

## Composition with other PBS skills

| Skill | Composition |
|---|---|
| `decision-design-sharpening` | Phase 1 of same pattern; fires at decision-formation moment, NOT at implementation-start |
| `audit` | Drift-detection POST-implementation; this skill operates BEFORE implementation begins |
| `design-review` | Soundness-review POST-implementation; same — this skill before implementation |
| `orchestrator` | Could route to this skill when implementation phase begins for major commitment |
| `frame-task` (#8) | Frames task before work begins; this skill operates AFTER decisions locked, BEFORE implementation |

## Output

Per round:
- Surface implementation concerns (operational + occasional architectural findings) as structured chat content
- Wait for user accept/reject/refine
- After accepted refinements: incorporate into implementation-readiness checklist
- After 2-3 rounds: persist checklist + DR amendments per `memory/feedback_propose_before_commit.md`

## Audit-trail integration

When audit-trail v2 ships per #6, each sharpening round emits:
- `event_kind=sharpening_round_started` with `round_number` + `decision_kind` + `phase=pre_implementation`
- `event_kind=sharpening_round_completed` with `refinements_surfaced` count + `expansion_count` + `architectural_findings_count`

Composes with audit-trail-as-canonical-source discipline + defensibility per VISION axis 3.

## Source memory + shared methodology

`memory/feedback_pre_decision_sharpening.md` — full theoretical grounding shared between this skill + `decision-design-sharpening`:
- 5 mechanisms (anchoring bias / sunk-cost / sparring vs validation / fresh-context / greenfield-still-anchored)
- Decomposition trigger details
- User-triggered round discipline
- Layered coverage hypothesis
- Expansion-vs-revision calibration
- Empirical validation from session 12 R3a-R3d work
- Two-phase pattern
