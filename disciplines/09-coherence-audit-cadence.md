---
discipline: 9
title: Coherence-audit cadence
when_fires: Phase 3-6 work checkpoints; mid-phase trigger conditions (5+ DRs / composite-DR lock / pre-promotion); BACKLOG-scheduled audit checkpoints
load_on_demand: true
---

# Discipline 9 — Coherence-audit cadence

When `coherence-audit` skill fires across Phase 3-6 work. Codifies WHEN audits run (vs `coherence-audit` SKILL.md which codifies HOW).

## 5 hard checkpoints (scheduled in BACKLOG.md per Phase)

| # | When | Scope | Purpose |
|---|---|---|---|
| **C1** | Post-Phase-3.4 close | After 3 Pattern A protocol topics locked (substrate / adapter / quality-gate) + 2 reclassified mechanism-class ARCH topics locked (sparring / audit). (coordination / trust / time were Pattern-A candidates but cancelled per `docs/decisions/phase-3-2-doc-organization.md` §Amendments — subsumed into substrate hooks + authority-binding mechanism + substrate-impl temporal semantics + adapter time-driven operations.) | Validates Pattern A precedent set + 12-required + 7-conditional template (per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`) + per-Pattern-A cardinality variations before primitive-cluster topics extend |
| **C2** | Post-Phase-3.5 close | After 4 primitive cluster + 2 cross-cutting integrator topics locked | Validates primitive clusters compose cleanly with Pattern A protocols |
| **C3** | Phase 3.8 phase-boundary | ARCH-specific Lenses 11-15 activate (inter-layer consistency / specs traceability / architectural-protocol completeness / DR coverage gap / granularity match) | Comprehensive corpus-set audit before Phase 4 starts |
| **C4** | Phase 6 pre-implementation | Architectural-validation pass before implementation work begins; Lens 17 (schema completeness) activates | Catches architectural drift accumulated across Phase 4-5 |
| **C5** | Post-Phase-6 close | Final audit; full corpus including specs + code; Lens 18 (spec/impl divergence) activates | Before stability lock + promotion to higher-classification |

## 3 trigger conditions (mid-phase auto-fire candidates; per `coherence-audit` SKILL.md "When this skill fires")

| Trigger | When | Scope |
|---|---|---|
| **5+ DRs since last audit** | Per skill SKILL.md: "After a sequence of decisions has been locked" | Mid-phase audit on accumulated DRs since prior audit |
| **Composite-DR lock** | After Mode-2 composite decomposition lands (multiple sub-decisions in one DR) | Scoped audit on composite decision's surface |
| **Pre-promotion-to-stability** | Before any locked corpus segment promoted to higher-stability classification | Signal-driven; user-triggered |

## Why this cadence

- Phase 3.4 mid-audit deferred — Pattern A pattern already validated by the 3 Pattern A topics; mid-phase audit before C1 = cost without benefit
- Phase 5 close audit skipped — ROADMAP is concise; subsumed into C4 (Phase 6 pre-implementation) which validates ROADMAP + spec planning together
- Phase 4 close audit subsumed into C4 — DR-set audit (Lens 16 decision-linkage / constraint-flow tracking) activates within C4 unless 5+ DR trigger fires mid-Phase-4
- Per-DR audit rejected — would fire too frequently; trigger condition (5+ DRs) catches accumulation

## Composition with `coherence-audit` SKILL.md

Skill defines HOW (10 universal lenses + corpus-specific 11-18); this discipline defines WHEN (5 hard checkpoints + 3 triggers). Together: at each checkpoint or trigger fire, READ skill (per Discipline 1 skill+profile sub-section); apply procedure; cite specific lens names + findings in chat output.

## Audit-checkpoint procedure (default-light + escalate-on-evidence)

**Default audit-checkpoint procedure** = single sub-agent at xhigh effort reads relevant corpus + applies named lenses + reports verdict. T1 findings (architectural REVISION) trigger cascade-application of revisions ONLY for what's actually broken; T2/T3 findings get triaged inline + skip cascade ceremony.

**Multi-cascade audit-checkpoint shape** (per Note 62 C2 4-parallel auditor + 4-cascade-application precedent: GLOSSARY auditor + ARCH auditor + DR-set auditor + carryover-signals evaluator + 4-cascade Step 5 cascade-aware revision application) **stays available as reference pattern** for T1 escalation OR explicit user request; **NOT default**. Heavy ceremony applied to routine doc-hygiene findings is methodology-as-default-leak per `MAINTENANCE.md` Procedure-rigor discipline subsection.

**C3 + future C4/C5 fire under default-light** unless escalation triggered. The done-criterion for design phase per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE: design is done when (a) single-pass C3 audit clean (b) ~11 Mode 3 specs written and typecheckable (c) Pydantic schemas cross-reference cleanly. Then implementation begins.

**Empirical grounding**: 0 T1 across C1 + C2 + 14 cluster-executions per HANDOFF Notes 61-65 cross-execution pattern signal tracking. T2/T3 findings at C2 (per Note 62 verdict shape) clustered at signal (b) cross-cluster Lens 4 carryover + signal (c) Phase 3.5 Lens 5 v0.2.x systemic leakage + signal (d) DR provenance-hygiene + signal (e) Discipline 11 plan-deviation correction — all DOCUMENT-HYGIENE class catchable by single xhigh auditor; the 4-parallel multi-cascade did not surface a different finding-class. Pattern-recurrence at C3 expected: doc-hygiene findings, not architectural correctness findings.

**Composes with**: `MAINTENANCE.md` TOP-LEVEL RULE — Cascade discipline → Procedure-rigor discipline subsection (default-light + escalate-on-evidence general rule); `disciplines/07-cascade-discipline.md`; `disciplines/11-effort-switch-cluster-map.md` (effort-switch plan applies to single-dispatch by default).

## Persistence target

BACKLOG.md scheduled audit checkpoints per Phase. ARCHITECTURE.md §2 sub-phase status table (Phase 3.8 row already present; C1 + C2 cross-ref BACKLOG).
