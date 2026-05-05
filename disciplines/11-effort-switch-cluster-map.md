---
discipline: 11
title: Effort-switch cluster-execution map
when_fires: At dispatch-class transitions during Phase 3.5+ cluster-execution procedure; at audit-checkpoint executions (C1-C5)
load_on_demand: true
---

# Discipline 11 — Effort-switch cluster-execution map

Operationalizes the Working-procedure "Effort-level switch suggestion is a pause-point" bullet by enumerating the exact dispatch-points where AI surfaces switch suggestions during dispatch sequences. Codifies WHEN the suggestion fires; the abstract rule (suggest + pause; user decides) lives in `DISCIPLINES.md` Working procedure.

## Default applicability — single-dispatch shape

**The effort-switch plan applies to single-dispatch single-sub-agent shape as default** (per `MAINTENANCE.md` Procedure-rigor discipline + CLAUDE.md M1 + M2: default cascade-application = single sub-agent at xhigh; multi-sub-agent / Writer-Reviewer / cluster-execution methodology = escalation, not default ceremony).

For single-dispatch work (audits, mechanical cascades, v1.x amendments, audit-checkpoints, Mode 3 Pydantic specs):
- **Default effort = xhigh** for the dispatched sub-agent (reasoning-dense + Lens 5 v0.2.2 subtle-breadcrumb-detection requirement)
- **Effort-switch suggestion** at single explicit pause-point: between the sub-agent's substantive work and any subsequent main-session HANDOFF write (xhigh → high acceptable for HANDOFF write)
- **No multi-step toggle map** for single-dispatch (the 3-toggle map below applies to FULL-CYCLE cluster-execution which is reference-only by default)

**FULL-CYCLE patterns** (Note 60/61/62/63 5-stage Wave-1 + Reviewer + Wave-2 + Reviewer + Wave-2.5 effort-switch sequences) become **reference patterns for substantive new ARCH topic clusters**; NOT default for v1.x amendments / audit-checkpoints / Mode 3 specs / mechanical cascades.

## Composes with

- Working-procedure "Effort-level switch suggestion is a pause-point" bullet (this file is the operational map for that abstract rule)
- Working-procedure "Scope-bounded autonomous authority grant" bullet (effort-switch is the explicit exception within otherwise-autonomous scope)
- `process-kit/structural-invariants.md` "Sizing principle" (cost-of-error + reasoning-density govern mitigation depth — including reasoning-depth via effort level)
- `MAINTENANCE.md` Procedure-rigor discipline subsection (default-light + escalate-on-evidence)
- `disciplines/07-cascade-discipline.md` (cascade structural consistency + procedure-rigor)
- `disciplines/09-coherence-audit-cadence.md` (audit-checkpoint default = single-pass; multi-cascade reserved for T1 escalation)

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

## Lens 5 subtle-breadcrumb-detection requirement (audit-pass dispatches)

For audit-pass dispatches (single-sub-agent default OR Reviewer roles in escalated cluster-execution), effort cannot downshift from xhigh to high — even on narrow-surface audits. Empirical evidence: high-effort audit-pass dispatch misses Lens 5 v0.2.2 sharpening-tier-label leakage at structural-elevation moments. The label feels load-bearing as marker of structural-vs-coverage distinction; subtle-breadcrumb detection requires xhigh reasoning depth.

**Generalization**: dispatches applying Lens 5 v0.2.2 / sharpening-trajectory hygiene at structural-elevation moments require xhigh effort regardless of surface-narrowness. Applies to:
- Single-pass audit dispatch (default audit-checkpoint shape per `disciplines/09-coherence-audit-cadence.md`)
- Wave-1 Reviewer (when escalated cluster-execution methodology has fired)
- Wave-2 Cascade-Reviewer (when escalated)
- Wave-2.5 Cleanup-Writer integrated final recheck (when escalated)

Cascade-execution generation-dense work (mass scrub; mechanical placeholder refresh) MAY downshift to high — those are pure-mechanical-execution shapes, not Lens-5-detection shapes. The discriminator: detection-class work (catching subtle sharpening-tier labels at structural-elevation moments) stays xhigh; execution-class work (applying already-found findings as well-specified edits) downshifts to high.

Composes with the Reviewer-brief checklist requirement codified in `plugin/skills/coherence-audit/SKILL.md` Step 5 (v0.2.2): the dispatch brief MUST enumerate sharpening-tier-label scrub as explicit checklist item AND the dispatching effort level MUST stay xhigh. Both compose; neither alone suffices.

**Cross-cluster Lens 5 v0.2.2 retro-application sweep at phase-set closure** (Note 63 codification) is **DOWNGRADED** from "in-scope at phase-set closure" → **available on T1 escalation; not default**. Per `MAINTENANCE.md` Procedure-rigor discipline: doc-hygiene findings at phase-set closures get fixed inline if significant; performative cleanup-cascade dispatches are methodology-as-default-leak. Reserve cross-cluster retro-sweeps for T1 escalation OR explicit user request.

## Coherence-audit checkpoint procedure (default-light + escalate-on-evidence)

Per `disciplines/09-coherence-audit-cadence.md` audit-checkpoint procedure subsection: **default audit-checkpoint = single sub-agent at xhigh effort** reads relevant corpus + applies named lenses + reports verdict. Effort stays xhigh throughout single-pass audit (reasoning-dense; Lens 5 v0.2.2 subtle-breadcrumb-detection requirement).

**Multi-cascade audit-checkpoint shape** (Note 62 C2 4-parallel auditor + 4-cascade-application precedent — Wave 0 parallel Auditors split by lens-focus + Cascade waves per finding-class + Recheck rounds) **stays available as reference pattern** for T1 escalation OR explicit user request; **NOT default**. When the multi-cascade shape fires under escalation: xhigh for audit-pass + Reviewer dispatches; downshift to high only for cascade-execution sub-agents applying already-found findings as mechanical edits.

C1 shape (Note 55 retrospective: Wave 0 + Wave 1-6 + Round 2/3 recheck) is **historical reference**; future audit-checkpoints fire under default-light unless escalation triggered.

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
