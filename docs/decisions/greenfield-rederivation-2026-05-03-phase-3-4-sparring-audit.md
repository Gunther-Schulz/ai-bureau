# Decision record: Greenfield-rederivation v2-audit — Phase 3.4 sparring + audit reclassified-mechanism-class sub-cluster

## Status

PROPOSED — 2026-05-03. Wave-1 sub-agent dispatch pending. Per `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 §Per-execution DR shape (status flow: PROPOSED → ACCEPTED-VALIDATED OR ACCEPTED-WITH-FINDINGS).

## Owner

Phase 3 audit family — fourth v2 greenfield-rederivation cluster-execution after Phase 3.1 4-DRs + Phase 3.2 composite DR + Phase 3.4 substrate+adapter sub-cluster. Closes Phase 3.4 v2-audit campaign on the two reclassified-mechanism-class topics. Cluster scope = 4 artifacts (sparring topic + sparring DR + audit topic + audit DR).

Skill version: v0.1.0 preliminary-locked. Per skill §Status: ≥2-execution threshold met since prior cluster-executions; this is the 4th execution maintaining empirical-evidence base.

## Related

- `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 (this skill; per-execution DR template)
- `plugin/skills/decision-design-sharpening/SKILL.md` v0.10.0 (composes via skill-skill-pattern per prior cluster-executions)
- `plugin/skills/coherence-audit/SKILL.md` Lens 5 v0.2.1 + Lens 8 + Lens 9 (Reviewer brief lenses)
- `MAINTENANCE.md` Layer 3 description (Pattern A protocol topic template; 12+7 conditional sections post-amendment)
- `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` (deferred §14 application path (c) for sparring + audit topics)
- `docs/decisions/greenfield-rederivation-pause.md` Step 3 (sparring + audit reclassified-mechanism-class verdict)
- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-4-substrate-adapter.md` (Phase 3.4 substrate+adapter sub-cluster v2-audit; immediate prior execution)
- `docs/decisions/greenfield-rederivation-pause.md` Step 1 (Phase 3.1 4-DRs first execution)
- `arch/sparring.md` + `docs/decisions/sparring-arch-topic.md` (cluster artifacts; sparring pair)
- `arch/audit.md` + `docs/decisions/audit-arch-topic.md` (cluster artifacts; audit pair)
- `ARCHITECTURE.md` §6 (Pattern-A/B/C semantics — sparring + audit RECLASSIFIED as mechanism class, NOT Pattern A)
- `BACKLOG.md` Phase 3.4 (cluster + bundled deferred items entry)
- HISTORICAL INPUT (not authoritative; per skill §Inputs): original Round-1+Round-2 sharpening provenance in `sparring-arch-topic.md` + `audit-arch-topic.md`; reclassification amendment; substrate+adapter pattern-stable cross-execution signal

## Context

Per prior session step 5: "Phase 3.4 sparring+audit reclassified-mechanism-class sub-cluster v2-audit (4 artifacts: `arch/sparring.md` + `arch/audit.md` + their DRs `sparring-arch-topic.md` + `audit-arch-topic.md`) — natural follow-up to substrate+adapter; closes Phase 3.4 v2-audit campaign". Per `BACKLOG.md` Phase 3.4 cluster-entry: bundles deferred work from prior cluster.

**Why this cluster, why now**:

1. **Closes Phase 3.4 v2-audit campaign** — Phase 3.1 (4 DRs) + Phase 3.2 (composite DR) + Phase 3.4 substrate+adapter (4 artifacts) v2-audited and CONFIRMS-LOCKED on architecture. Phase 3.4 sparring+audit are the two remaining locked topics in the phase; v2-audit completes coverage.
2. **Reclassified-mechanism-class status** — sparring + audit reclassified from Pattern A → mechanism class with per-shape policy variation per `docs/decisions/greenfield-rederivation-pause.md` Step 3 verdict. Both topics carry the reclassification framing. v2-audit re-derives both from primitives (VISION + locked GLOSSARY + first-principles disciplines) without inheriting reclassification-framing assumptions.
3. **Bundled deferred items reconciliation** — three items deferred from prior sessions for bundling into this v2-audit per BACKLOG Phase 3.4:
   - **(a) §14 cross-shape policy variation application + §14-§18 → §15-§19 renumbering** for BOTH topics per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` REV-1 deferred path (c). Sparring has cross-shape-variation content at OLD slot §12 + custom §13 workflow_instance — both template-divergences to reconcile during v2-audit re-derivation.
   - **(b) `arch/substrate.md:42` §5 mis-reference fix** (pre-existing bug; surfaced by prior Cascade-Reviewer; line says "see §5 Transport variation" but substrate.md §5 is "Selection mechanics"; transport is §12).
   - **(c) `arch/substrate.md:396` residual breadcrumb** strip (prior cascade NB carryover; pattern-equivalent to S7 cleanup).
4. **Pattern A template at 12+7 post-amendment** — Pattern A protocol topic template now at 12 common-required + 7 protocol-specific-conditional (per `MAINTENANCE.md` Layer 3 + `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`). However, sparring + audit are RECLASSIFIED-mechanism-class topics (NOT Pattern A) per `ARCHITECTURE.md` §6. Greenfield-derivation needs to navigate template-applicability boundary: how much of Pattern A template applies to mechanism-class topics; which sections N/A; whether mechanism-class needs its own template.

**Cluster's foundation-up position**: sparring + audit compose UPSTREAM with substrate (Surface §B + §D for sparring; Surface §F + §C + §8 for audit) + adapter (§8 emission convergence) — both already v2-audited. Foundation-up dependency satisfied: prior-tier topics validated; this cluster validates downstream-composing topics.

**Foundation-up dependency check** (per skill §Pre-execution step 3): sparring + audit are sister mechanism-class peers; neither depends on the other's locked classification. Both depend on substrate/adapter (already v2-audited) + GLOSSARY entries (Phase-2 locked). Single Wave dispatch valid.

## Decision

(To be populated post-Wave-1 + post-reconciliation per skill §Per-execution DR shape.)

### Wave decomposition

**Wave 1 (this execution)** — 4 artifacts, single Wave:

| Artifact pair | Writer | Reviewer |
|---|---|---|
| Sparring (`arch/sparring.md` + `docs/decisions/sparring-arch-topic.md`) | Writer-1 (fresh sub-agent context) | Reviewer-1 (fresh sub-agent context) |
| Audit (`arch/audit.md` + `docs/decisions/audit-arch-topic.md`) | Writer-2 (fresh sub-agent context) | Reviewer-2 (fresh sub-agent context) |

**Per-Wave dispatch shape** (per skill §Per-Wave + validated empirical pattern across 3 prior executions):
- 2 Writer-pairs in parallel (each Writer handles one artifact-pair = 1 ARCH topic + 1 DR)
- 2 Reviewers (one per Writer-pair; each compares Writer's greenfield-derivation against the locked pair)
- Total: 4 Wave-1 sub-agents in fresh contexts
- Main session orchestrator-only per `CLAUDE.md` M3 + skill §Per-Wave step 3

### Per-artifact verdict (post-Reviewer aggregation; populated when Wave-1 completes)

| Artifact | Verdict | Highest tier | Findings |
|---|---|---|---|
| `arch/sparring.md` | TBD | TBD | TBD |
| `arch/audit.md` | TBD | TBD | TBD |
| `docs/decisions/sparring-arch-topic.md` | TBD | TBD | TBD |
| `docs/decisions/audit-arch-topic.md` | TBD | TBD | TBD |

### User-decisions per divergence (post-reconciliation; populated after user reconciles each finding)

(TBD — populated when each Reviewer finding gets REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED.)

### Bundled deferred-item dispositions (populated when Cascade execution applies)

| Deferred item | Disposition | Cascade target |
|---|---|---|
| (a) §14 application sparring | TBD | `arch/sparring.md` |
| (a) §14 application audit | TBD | `arch/audit.md` |
| (a) §14-§18 → §15-§19 renumbering both topics | TBD | both ARCH topics + internal cross-refs |
| (b) substrate.md:42 §5 mis-ref fix | TBD | `arch/substrate.md` line 42 |
| (c) substrate.md:396 breadcrumb strip | TBD | `arch/substrate.md` line 396 |

## Sharpening provenance

(Populated post-Wave-1 + post-Reviewer per skill §Per-execution DR shape.)

### Wave decomposition + dispatch summary

(To be populated when each sub-agent returns: per-Writer brief delivered + per-Reviewer brief delivered + Ralph self-check confirmation per sub-agent.)

### Per-Writer Ralph self-check verification

| Sub-agent | Required-reads completed | Discipline 10 applied | Locked artifact NOT read | Citations file:line | Verdict |
|---|---|---|---|---|---|
| Writer-1 (sparring pair) | TBD | TBD | TBD | TBD | TBD |
| Writer-2 (audit pair) | TBD | TBD | TBD | TBD | TBD |

### Per-Reviewer Ralph self-check verification

| Sub-agent | Locked + Writer read | 4 lenses applied | Tiered each finding | No element unverdict-ed | Verdict |
|---|---|---|---|---|---|
| Reviewer-1 (sparring pair) | TBD | TBD | TBD | TBD | TBD |
| Reviewer-2 (audit pair) | TBD | TBD | TBD | TBD | TBD |

### Decomposition mode

Mode 1 (single-decision audit; not composite). Cluster = single audit unit; one Wave; per-artifact verdicts aggregate into single execution outcome.

## Composition with existing architecture

**Cross-execution position**: 4th greenfield-rederivation cluster-execution per skill empirical-evidence rule. Pattern-stable signal continues per prior executions: substantive architecture survives greenfield re-derivation; drift = Lens 5 v0.2.1 retro-application + cascade-miss to upstream/downstream artifacts predating M1-M8.

**Phase 3.4 v2-audit campaign closure**: this execution closes the Phase 3.4 audit campaign. Post-execution status: Phase 3.1 (4 DRs) + Phase 3.2 (composite DR) + Phase 3.4 substrate+adapter (4 artifacts) + Phase 3.4 sparring+audit (4 artifacts) all v2-audited. Coherence-audit checkpoint C1 (post-Phase-3.4 close per `BACKLOG.md` audit-checkpoint cadence) becomes runnable post-this-execution.

**Pattern A template extensibility validation**: post-amendment template at 12+7 conditional sections. Sparring + audit are mechanism-class topics (NOT Pattern A). Writer briefs surface template-applicability boundary: which Pattern A sections apply / which N/A / whether mechanism-class warrants its own template (potential T1 finding if greenfield-derivation surfaces this as architectural gap).

**Bundled deferred-item composition**: §14 application + substrate.md fixes are operationally bundled into this v2-audit's Cascade execution per BACKLOG Phase 3.4 + skill §Cascade execution. Cascade-Writer brief explicit on bundled scope.

**Coherence-audit composition**: per skill §Composition with other PBS dev skills — greenfield-rederivation catches per-artifact derivation drift; coherence-audit catches set-level drift. Phase-boundary audit C1 (post-Phase-3.4) runs both skills composed; this execution provides the per-cluster greenfield-derivation pass; coherence-audit follows.

## Constraints flowing to downstream commitments

(To be populated based on Wave-1 findings + user reconciliation.)

### Provisional (pre-Wave-1):

- **Cascade scope** — at minimum, bundled deferred items (a)+(b)+(c) require cascade application even if 0 NEEDS-REVISION findings surface; cascade is delegated to fresh-context Cascade-Writer + Cascade-Reviewer per `CLAUDE.md` M3+M4 + skill §Cascade execution
- **Phase 3.4 v2-audit campaign close** — post-this-execution, no further Phase 3.4 v2-audit clusters scheduled; coherence-audit C1 (post-Phase-3.4) becomes runnable
- **Phase 3.5 + 3.6 unblocked** — sparring+audit v2-audit closure removes any v2-audit prerequisite for Phase 3.5 primitive-cluster work + Phase 3.6 quality-gate ARCH topic
- **Cross-execution stable-corpus signal candidacy** — if this execution yields 0 NEEDS-REVISION + 0 NEEDS-REWORK across all 4 artifacts (only T4-confirms-locked findings), Phase 3.4 corpus-set may be greenfield-stable; cadence shift candidate per skill §Termination criteria

## Files touched

- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-4-sparring-audit.md` (this file; PROPOSED at stub-creation; ACCEPTED-* at finalization)
- `arch/sparring.md` (cascade target if Wave-1 surfaces revisions OR §14 application bundle fires)
- `arch/audit.md` (cascade target if Wave-1 surfaces revisions OR §14 application bundle fires)
- `docs/decisions/sparring-arch-topic.md` (cascade target if Wave-1 surfaces revisions)
- `docs/decisions/audit-arch-topic.md` (cascade target if Wave-1 surfaces revisions)
- `arch/substrate.md` (cascade target for bundled (b) line 42 mis-ref fix + (c) line 396 breadcrumb strip)
- `glossary/<entry>.md` (cascade targets if DOWNSTREAM glossary back-check surfaces retro-fits)
- `BACKLOG.md` (cascade-update: Phase 3.4 sparring+audit Resolved post-execution; bundled-items resolution)
- `HANDOFF.md` (next session-log Note: v2-audit completion + bundled deferred items reconciled + Phase 3.4 v2-audit campaign closure)

## Revisit triggers

- New artifact added to Phase 3.4 cluster (e.g., quality-gate ARCH topic Phase 3.6 if it surfaces composition issues with sparring+audit)
- User-flagged drift on either topic post-execution
- Phase-boundary coherence-audit (C1 per `BACKLOG.md` audit-checkpoint cadence) surfaces set-level cascade-miss involving sparring+audit
- `arch/audit.md` + `arch/sparring.md` already-existing-status resolution per `pattern-a-template-7th-conditional-cross-shape-variation.md` REV-1 deferred path (c) — this v2-audit IS the resolution mechanism
- Skill version increment (v0.1.0 → v0.2.0+) if cross-execution pattern surfaces amendment-warranting findings
