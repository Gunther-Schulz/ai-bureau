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
| **C1** | Post-Phase-3.4 close | After 7 Pattern A protocol topics locked (substrate / adapter / sparring / audit / coordination / trust / time) | Validates Pattern A precedent set + 18-section template + per-Pattern-A cardinality variations before primitive-cluster topics extend |
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

- Phase 3.4 mid-audit (after 5 of 7 topics) deferred — Pattern A pattern already validated by 3 topics; mid-phase audit before C1 = cost without benefit
- Phase 5 close audit skipped — ROADMAP is concise; subsumed into C4 (Phase 6 pre-implementation) which validates ROADMAP + spec planning together
- Phase 4 close audit subsumed into C4 — DR-set audit (Lens 16 decision-linkage / constraint-flow tracking) activates within C4 unless 5+ DR trigger fires mid-Phase-4
- Per-DR audit rejected — would fire too frequently; trigger condition (5+ DRs) catches accumulation

## Composition with `coherence-audit` SKILL.md

Skill defines HOW (10 universal lenses + corpus-specific 11-18); this discipline defines WHEN (5 hard checkpoints + 3 triggers). Together: at each checkpoint or trigger fire, READ skill (per Discipline 1 skill+profile sub-section); apply procedure; cite specific lens names + findings in chat output.

## Persistence target

BACKLOG.md scheduled audit checkpoints per Phase. ARCHITECTURE.md §2 sub-phase status table (Phase 3.8 row already present; C1 + C2 cross-ref BACKLOG).
