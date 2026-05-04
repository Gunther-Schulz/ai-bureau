---
discipline: 11
title: Effort-switch cluster-execution map
when_fires: At dispatch-class transitions during Phase 3.5+ cluster-execution procedure; at audit-checkpoint executions (C1-C5)
load_on_demand: true
---

# Discipline 11 — Effort-switch cluster-execution map

Operationalizes the Working-procedure "Effort-level switch suggestion is a pause-point" bullet by enumerating the exact dispatch-points where AI surfaces switch suggestions during a primitive-cluster cluster-execution. Codifies WHEN the suggestion fires; the abstract rule (suggest + pause; user decides) lives in `DISCIPLINES.md` Working procedure.

## Composes with

- Working-procedure "Effort-level switch suggestion is a pause-point" bullet (this file is the operational map for that abstract rule)
- Working-procedure "Scope-bounded autonomous authority grant" bullet (effort-switch is the explicit exception within otherwise-autonomous scope)
- `process-kit/structural-invariants.md` "Sizing principle" (cost-of-error + reasoning-density govern mitigation depth — including reasoning-depth via effort level)

## Full primitive-cluster cluster-execution procedure (28 steps)

| # | Step | Role | Optimal effort | Switch suggestion at this step? |
|---|---|---|---|---|
| 1 | Session-start reads (CLAUDE / VISION / MAINTENANCE / DISCIPLINES / HANDOFF / BACKLOG / ARCHITECTURE / GLOSSARY index / profiles) | Main | xhigh | START at xhigh |
| 2 | Read prior cluster's HANDOFF Note (carryover) | Main | xhigh | — |
| 3 | Round 1 sharpening (Mode 2 composite if applicable; full monty) | Main | xhigh | — |
| 4 | User triggers Round 2 | (transition) | xhigh | — |
| 5 | Round 2 sharpening (deeper surface; cross-cutting; profile-anchored validation) | Main | xhigh | — |
| 6 | User locks en bloc | (transition) | xhigh | — |
| 7 | Dispatch Wave-1 Writer | Main → sub-agent | xhigh (current Phase 3.5 — see exception below) | No suggestion currently. *Future*: `xhigh → high` if Writer is executing fully-anchored template |
| 8 | Wait for Wave-1 Writer | — | — | — |
| 9 | Dispatch Wave-1 Reviewer | Main → sub-agent | xhigh | If at high (because step 7 downshifted): suggest `high → xhigh` |
| 10 | Wait for Wave-1 Reviewer | — | — | — |
| 11 | Read Wave-1 outputs + judge T1/T2/T3/T4 findings | Main | xhigh | — |
| 12 | Apply Reviewer-flagged refinements (direct edits or re-dispatch) | Main | xhigh | — |
| 13 | Commit Wave-1 | Main | xhigh-or-high (mechanical; not worth toggle) | No suggestion (toggle overhead > savings) |
| **14** | **Dispatch Wave-2 Cascade-Writer** | Main → sub-agent | high (mechanical cascade per locked DR; ~10-15 file edits well-specified) | **Suggest `xhigh → high`** |
| 15 | Wait for Cascade-Writer | — | — | — |
| **16** | **Dispatch Wave-2 Cascade-Reviewer** | Main → sub-agent | xhigh (Lens 6 reciprocity + cross-ref consistency = reasoning-dense) | **Suggest `high → xhigh`** |
| 17 | Wait for Cascade-Reviewer | — | — | — |
| 18 | Read Wave-2 outputs + judge findings | Main | xhigh | — |
| 19 | Apply Reviewer-flagged refinements | Main | xhigh | — |
| 20 | Commit Wave-2 | Main | xhigh-or-high (mechanical) | No suggestion |
| 21 | Dispatch Wave-2.5 Cleanup-Writer + integrated recheck | Main → sub-agent | xhigh (the integrated recheck is the final load-bearing pass; recheck-misses cost more than generation-overhead saved) | No suggestion (stay xhigh) |
| 22 | Wait for Cleanup-Writer + recheck | — | — | — |
| 23 | Read Wave-2.5 outputs + judge | Main | xhigh | — |
| 24 | Commit Wave-2.5 | Main | xhigh-or-high | No suggestion |
| **25** | **HANDOFF write** (Note documenting cluster execution) | Main | high (structured generation; pattern well-known; not novel reasoning) | **Suggest `xhigh → high`** |
| 26 | Commit HANDOFF + push | Main | high | — |
| 27 | Surface /clear recommendation + HARD STOP | Main | high | — |
| 28 | (next cluster starts) | — | — | Suggest `high → xhigh` at step 1 of next cluster |

## Practical 3-toggle map (current Phase 3.5 state)

```
START → xhigh
[xhigh through steps 1-13: session start + Round 1/2 + Wave-1 Writer + Reviewer + lock + commit]
xhigh → high   ⟵ before dispatching Wave-2 Cascade-Writer (step 14)
high → xhigh   ⟵ before dispatching Wave-2 Cascade-Reviewer (step 16)
[xhigh through steps 17-24]
xhigh → high   ⟵ before HANDOFF write (step 25)
[high through steps 26-27]
END → /clear, next session re-enters at xhigh
```

**3 effort-switch suggestion moments per cluster execution** (steps 14, 16, 25). All other steps stay at current level.

## Exception: new-template-class anchor (Wave-1 Writer effort)

When Wave-1 Writer is establishing a new template-class variant (not executing a fully-anchored template), keep at xhigh — Writer is reasoning-dense (precedent-setting), not just generating per spec.

Phase 3.5 instances of new-template-class anchoring (all kept Wave-1 Writer at xhigh):
- specialist-skill — 12+5 primitive-cluster topic template anchor
- practitioner — Pattern C topic-template-class anchor
- workflow-work-unit — two-Pattern-B topic-template-class anchor
- claim-defensibility — PRIMITIVE + DERIVED topic-template-class anchor

The downshift suggestion (Wave-1 Writer `xhigh → high`) only fires when Writer is 2nd-instance of an already-anchored template-class. That state hasn't been reached in Phase 3.5 yet; surface the suggestion when it does.

## Coherence-audit checkpoint procedure (different shape — C1-C5)

Coherence-audit checkpoint executions follow a different procedure than primitive-cluster cluster-execution. The C1 shape (per Note 55 retrospective):

- Wave 0: parallel Auditors split by lens-focus + Auditor-Reviewer (M4 Writer-Reviewer pattern)
- Cascade waves per finding-class (Wave 1 / Wave 2 / Waves 3-6 etc.)
- Recheck rounds (Round 2 + Round 3 termination signals per skill §Termination signals)

Audit work is **reasoning-dense throughout** (lens-application + cross-cluster pattern detection + density-decay judgment). Recommendation: **xhigh for nearly every step**. Exception: cascade-execution sub-agents (Cascade-Writer-N applying Auditor findings as mechanical edits) mirror primitive-cluster Cascade-Writer characteristics → high.

For audit checkpoints: practical map is "stay xhigh; downshift only when dispatching cascade-execution sub-agents".

## Why surface at dispatch transitions, not constantly

The switch-suggestion fires at dispatch-class boundaries because that's where workload-class changes are most predictable + the user is naturally available (waiting for sub-agent result). Surfacing within a step (e.g., mid-Round-2) creates noise and disrupts flow.

## Failure modes prevented

- **Always-xhigh waste**: spending xhigh tokens on Cascade-Writer mechanical generation OR HANDOFF structured-generation
- **Always-high under-reasoning**: missing subtle lens-findings during Reviewer or audit reasoning; weak Round 1/2 sharpening; agentic-laziness on judgment moments
- **Toggle-overhead noise**: too many switch suggestions per cluster (capped at 3 per practical map; the suggestion is a pause-point, so each one costs user attention)

## When this map needs revision

- New cluster-execution shape lands (e.g., Phase 4 DR-block execution; Phase 6 implementation cycles) — extend or fork the map per new procedure
- Phase 3.5 reaches state where ≥2 instances of same template-class exist → add the Wave-1 Writer downshift suggestion to the map
- Sub-agent effort becomes independently configurable (currently sub-agents inherit session effort) → revisit per-sub-agent calibration
- Empirical evidence shows a recommended effort was wrong (Cascade-Writer at high produced bad output; Reviewer at high missed findings; etc.) — adjust per `process-kit/structural-invariants.md` Sizing principle calibration discipline

## Canonical exemplars

- HANDOFF Notes 56-58 (specialist-skill / practitioner / workflow-work-unit cluster executions; all anchored new template-class variants → Wave-1 Writer kept at xhigh)
- Current claim-defensibility cluster execution (PRIMITIVE + DERIVED anchor; first invocation of this discipline mid-flight)
- Note 55 C1 audit (canonical reasoning-dense-throughout shape; reference for C2+ audit checkpoints)
