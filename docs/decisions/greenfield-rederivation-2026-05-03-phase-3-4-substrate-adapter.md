---
title: Greenfield-rederivation execution — Phase 3.4 substrate+adapter sub-cluster
topic-cluster: greenfield-rederivation
status: PROPOSED
---

# Greenfield-rederivation execution — Phase 3.4 substrate+adapter sub-cluster

## Status

PROPOSED. Per `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 §Per-execution DR shape: status transitions PROPOSED → ACCEPTED-VALIDATED (no findings) OR ACCEPTED-WITH-FINDINGS (findings + user-decisions persisted) at post-cluster reconciliation.

## Owner

- **Phase**: Phase 3 audit family (greenfield-rederivation campaign per `HANDOFF.md` Notes 49-51)
- **Skill version**: `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0
- **Cluster scope**: Phase 3.4 substrate+adapter Pattern A protocol topics — 4 artifacts (2 ARCH topics + 2 DRs)
- **Cluster execution number**: 3rd v2 cluster-execution (after Phase 3.1 4 DRs + Phase 3.2 doc-organization 2 composite DRs)

## Related

**Cluster artifacts** (audit targets):
- `arch/substrate.md`
- `arch/adapter.md`
- `docs/decisions/substrate-arch-topic.md`
- `docs/decisions/adapter-arch-topic.md`

**Skill artifact**:
- `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 — codifies the per-cluster procedure

**Prior greenfield-rederivation executions** (HISTORICAL INPUT — not authoritative for current verdicts):
- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-1-drs.md` (ACCEPTED-WITH-FINDINGS; corpus-stable signal: 0 T1 + ~10 T3 housekeeping)
- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-2-doc-organization.md` (ACCEPTED-WITH-FINDINGS; 0 T1 + 2 T2 + ~13 T3; load-bearing cascade-miss closed)
- `docs/decisions/greenfield-rederivation-pause.md` (v1; SUPERSEDED; Tier-1 findings on Pattern A catalog 8→3 + 18→12+6 template restructure cascaded across corpus pre-v2)

**Disciplines applied**:
- `DISCIPLINES.md` Discipline 1 (source-grounded; skill+profile sub-section)
- `DISCIPLINES.md` Discipline 8 (foundation-up workflow ordering)
- `DISCIPLINES.md` Discipline 9 (coherence-audit cadence)
- `DISCIPLINES.md` Discipline 10 (greenfield evaluation of archived material)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 (structural-impossibility / pattern-vs-instance / preliminary-lock)
- `CLAUDE.md` M3 (sub-agent-first cascade routing) + M4 (Writer-Reviewer per artifact) + M6 (HARD STOP per logical unit) + M7 (Ralph self-check at apparent completion)

## Context

**Why this cluster, why now**:

Per `HANDOFF.md` Note 50 (option-1 next-cluster choice, deferred to Note 51 follow-up) + Note 51 (Phase 3.4 substrate+adapter sub-cluster locked as next substantive cluster-execution): substrate + adapter are the 2 surviving Pattern A protocol topics post-greenfield-rederivation v1 reclassification (sparring + audit RECLASSIFIED mechanism-class; coordination + trust + time CANCELLED per `docs/decisions/greenfield-rederivation-pause.md` Step 3). They are the load-bearing anchors for the Pattern A template + per-impl extension Protocols pattern.

**Foundation-up rationale per `DISCIPLINES.md` Discipline 8**: substrate is the most foundational ARCH topic (anchor for the 12-common-required + 6-conditional-section template per `MAINTENANCE.md` §3 Pattern A protocol topic template); adapter validated 2-layer Surface variation (META-Surface + per-integration-class Surfaces). Both topics predate Lens 5 v0.2.1 codification + M1-M8 cascade-load mitigations + the v2 skill itself. Drift — particularly provenance-hygiene drift + cascade-miss between locked artifact + current MAINTENANCE template — is plausibly present.

**Cluster sweet-spot fit per skill §When-to-use**: 4 artifacts is within 2-6 sweet-spot; 1 Wave with 2 Writer-pairs (each Writer covers ARCH topic + paired DR as tightly-coupled pair) fits skill §Per-Wave parallel-dispatch shape.

**Why NOT decompose into 2 single-Writer Waves**: the ARCH topic + its paired DR are tightly coupled (DR captures decision-rationale FOR the ARCH topic; same primitives; same VISION axes; same disciplines). Single Writer per topic-pair preserves derivation coherence + reduces cross-Writer reconciliation noise. 2 Writer-pairs in 1 Wave is the empirical-evidenced shape from Notes 49-50 Wave executions.

**Cluster-pair signal context** (per Note 50 cross-execution observation): two prior cluster-executions yielded 0 T1 + 0-2 T2 + ~10-13 T3 each — substantive architecture survives greenfield-derivation; drift concentrates in Lens 5 provenance hygiene + Lens 8 instance-leakage + cascade-miss to upstream/downstream artifacts. This cluster will test whether the pattern holds for the FOUNDATIONAL Pattern A topics (substrate as anchor) — higher-stakes than the prior two clusters.

## Decision

**TO BE POPULATED POST-WAVE-1 + POST-RECONCILIATION**.

Per skill §Per-execution DR shape, this section captures:
- Per-artifact verdict (GREENFIELD-VALID / INPUT-ONLY-VALID / NEEDS-REVISION / NEEDS-REWORK)
- Per-divergence tier (T1 framework-shape-changing / T2 topic-rewriting / T3 mechanical edit / T4 confirms-locked)
- User-decision per divergence (REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED)

## Sharpening provenance

### Wave decomposition

| Wave | Artifacts | Writer count | Reviewer count | Rationale |
|---|---|---|---|---|
| 1 | substrate (arch/substrate.md + docs/decisions/substrate-arch-topic.md) + adapter (arch/adapter.md + docs/decisions/adapter-arch-topic.md) | 2 (1 per topic-pair) | 2 (1 per Writer output) | Tightly-coupled topic+DR pairs; preserves derivation coherence; matches user-instructed "2 Writer + 2 Reviewer in parallel" shape per `HANDOFF.md` Note 51 step 5 |

### Per-Wave dispatch summary

**TO BE POPULATED POST-WAVE-1**:
- Writer-1 (substrate-pair): brief summary + Ralph self-check confirmation
- Writer-2 (adapter-pair): brief summary + Ralph self-check confirmation
- Reviewer-1 (against Writer-1 output): brief summary + tiered-divergence count + Ralph self-check confirmation
- Reviewer-2 (against Writer-2 output): brief summary + tiered-divergence count + Ralph self-check confirmation

### Foundation-up dependency analysis (within cluster)

- **substrate** has zero dependency on adapter; foundational primitive (Pattern A anchor).
- **adapter** composes WITH substrate Surface §C (permission flow) per locked `arch/adapter.md`. For greenfield re-derivation, both Writers derive independently from primitives + GLOSSARY entries (each GLOSSARY entry self-anchors); adapter Writer cites substrate-as-composition-target without contaminating greenfield derivation.
- → 1 Wave with 2 parallel Writers acceptable. No within-cluster foundation-up Wave-split needed.

### Pre-validation prep reads (main-session orchestrator)

Per `HANDOFF.md` Note 51 step 3 + Note 50 hook-prep pattern, main-session orchestrator read BEFORE first Edit:
- `VISION.md`, `MAINTENANCE.md`, `DISCIPLINES.md`, `HANDOFF.md`, `BACKLOG.md`, `ARCHITECTURE.md`, `GLOSSARY.md` (mandatory session-start reads per `CLAUDE.md`)
- `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 (active skill)
- `plugin/skills/decision-design-sharpening/SKILL.md` v0.10.0 (hook gate prep)
- `profiles/INDEX.md` (cluster structure)
- 3 profile files: `profiles/L5a-planner-pbs-schulz.md` (Cluster B+C anchor) + `profiles/G-composability-gate.md` (Cluster D) + `profiles/L4a-workspace-deployer-solo.md` (Cluster B; substrate-selection grounding)

## Composition with existing architecture

### How this audit composes

- **vs `coherence-audit`**: peer audit skill (lens-driven corpus scan); both run at phase boundaries per `disciplines/09-coherence-audit-cadence.md`. Greenfield-rederivation re-derives per artifact from primitives; coherence-audit scans for set-level / vocabulary-level / cascade-level drift. Different fault modes; the two compose. This execution is greenfield-only (per skill §Procedure); coherence-audit would run separately at C1 (post-3.4 close) per `BACKLOG.md` Phase 3 audit-checkpoints.
- **vs `decision-design-sharpening`**: phase-1 pre-decision skill operates UPSTREAM (before lock). This skill operates POST-lock on accumulated decisions. Different lifecycle moments.
- **vs `pre-implementation-sharpening`**: phase-2 implementation-start skill. Phase 6 spec/code work for substrate + adapter would invoke pre-implementation-sharpening; this audit is foundational verification BEFORE implementation begins.

### Cascade scope if revisions surface

**Potential downstream artifacts (cascade targets if T1/T2 surface)**:
- `ARCHITECTURE.md` §4 topic catalog one-liners (substrate + adapter rows; lines 58-59)
- `ARCHITECTURE.md` §7 Locked architectural decisions (substrate + adapter sections; lines 207-213)
- `MAINTENANCE.md` Pattern A protocol topic template (if T2 finding on template-fit, since substrate is anchor)
- `arch/sparring.md` + `arch/audit.md` cross-refs to substrate (composition claims)
- `glossary/substrate.md` + `glossary/adapter.md` (if greenfield surfaces vocabulary refinement glossary-grade per `MAINTENANCE.md` Bidirectional cascade)

**Cascade execution per skill §Cascade execution** (post-reconciliation): if revisions exist, cascade delegated to fresh-context Cascade-Writer sub-agent + Cascade-Reviewer per `CLAUDE.md` M3+M4. Tightly-coupled commits per `MAINTENANCE.md` cascade discipline.

## Constraints flowing to downstream commitments

**TO BE POPULATED POST-RECONCILIATION** (per-artifact revisions if any).

## Files touched (this DR's commit + Wave-1 + reconciliation + cascade)

- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-4-substrate-adapter.md` (this DR; PROPOSED stub commit)
- Wave-1 findings amendment commits (per-Wave persistence)
- Cascade target files if revisions (separate cascade commits)
- HANDOFF.md Note 52 (closure)

## Revisit triggers

- New artifact added to substrate/adapter sub-cluster (e.g., per-impl Phase 6 specs land)
- User-flagged drift on substrate or adapter primitives
- Phase 3.5 primitive-cluster work surfaces composition gap with substrate or adapter Surfaces
- Phase 3.6 quality-gate ARCH topic work surfaces composition gap with substrate Surface §D (sparring sub-mechanisms architecturally-encoded)
- Coherence-audit Checkpoint C1 (post-Phase-3.4 close per `BACKLOG.md` Phase 3 audit-checkpoints) — this DR's verdicts inform C1 lens activation
- Phase-boundary audit per `disciplines/09-coherence-audit-cadence.md`
