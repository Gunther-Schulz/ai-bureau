# Decision record: Greenfield-rederivation v2-audit — Phase 3.4 sparring + audit reclassified-mechanism-class sub-cluster

## Status

ACCEPTED-WITH-FINDINGS — 2026-05-03. Wave-1 + user-reconciliation + cascade execution + Cascade-Reviewer pass + Cleanup-Writer follow-up all complete. Per skill §Per-execution DR shape: status finalized.

**Execution timeline**:
1. PROPOSED — DR stub commit `7dfdfa5` (cluster definition + Wave decomposition; per skill §Pre-execution step 5)
2. Wave-1 — 4 sub-agents in fresh contexts (2 Writers + 2 Reviewers); main session orchestrator-only per `CLAUDE.md` M3
3. ACCEPTED-WITH-FINDINGS — DR commit `69f944e` (12 findings + 5 bundled deferred items aggregated; user-reconciliation en bloc)
4. Cascade execution — commit `0d53e1e` (Cascade-Writer in fresh sub-agent; 5 files; 70 insertions / 67 deletions)
5. Cascade-Reviewer pass — surfaced 3 T3 cascade-miss + 1 borderline-T3 scope-question; NON-BLOCKING verdict
6. Cleanup-Writer follow-up — commit `f327e6f` (3 T3 cascade-miss + 5 audit-arch-topic.md Pattern-A scrub broadening per user sign-off; 17 insertions / 17 deletions)

**Findings summary** (Wave-1 aggregate):
- 0 T1 (framework-shape-changing)
- 3 T2 (topic-rewriting; all in audit pair: Trust framing reframe + §14 addition + §14-§18 renumber)
- 8 T3 (mechanical edits; 5 sparring + 3 audit)
- 21 T4 (confirms-locked)
- + 3 Cascade-Reviewer follow-up T3 (post-cascade cascade-miss: capability-count cross-refs + 2 error-mapping §-refs)
- + 1 user-broadened T3 (5 audit-arch-topic.md Pattern-A self-references)

**Cross-execution pattern signal continues** per Notes 50/51/52: 4th cluster-execution; substantive architecture survives greenfield re-derivation; drift = Lens 5 v0.2.1 retro-application + cascade-miss legacy + 1 substantive REVISION (audit's Trust-subsumption framing reframed to audit-composes-with-authority-binding-mechanism). Cross-execution pattern across all 4 cluster-executions stable: 0 T1 across all clusters; T2/T3 drift attributable to Lens 5 v0.2.1 retro-application + cascade-miss to upstream/downstream artifacts predating M1-M8 + (newly surfaced this execution) substantive-framing-debt accumulated under prior cascade-load conditions.

**Skill v0.1.0 empirical-evidence threshold**: maintained at ≥2-execution; this is 4th consecutive successful cluster-execution validating orchestration shape end-to-end. No amendment-warranting patterns surfaced this execution; skill stays preliminary-locked at v0.1.0.

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

### Per-artifact verdict (post-Reviewer aggregation; Wave-1 complete)

| Artifact | Verdict | Highest tier | Findings |
|---|---|---|---|
| `arch/sparring.md` | NEEDS-REVISION | T3 mechanical | 5 mechanical edits (§14 relocation + §14-§18 renumber + §13 fold + §10/§11 duplicate + breadcrumb strips) |
| `arch/audit.md` | NEEDS-REVISION | T2 topic-rewriting | 1 T2 (Trust-subsumption framing 9 occurrences) + 1 T2 (§14 load-bearing section addition) + 1 T2 (§14-§18 renumber) + 2 T3 (capability count 6→7 + composition row cascade-flow) |
| `docs/decisions/sparring-arch-topic.md` | GREENFIELD-VALID | T4 confirms-locked | DR provenance hygiene clean per Lens 5 v0.2.1; Session-17 amendment narrative legitimately in DR §Composition |
| `docs/decisions/audit-arch-topic.md` | NEEDS-REVISION | T3 mechanical | 1 T3 (Pattern-A self-description scrub: lines 9, 25, 116, 118, 127) + cascade-flow from audit topic Trust framing |

**Cross-cascade target** (not in 4-artifact cluster but flagged):
- `ARCHITECTURE.md` §7 line 219-221 — Trust framing cascade-flow from A2 ("subsumes Trust" → "audit composes with authority-binding mechanism; Trust folded into authority-binding mechanism with per-shape trust policy")

### User-decisions per divergence

User accepted all 12 findings en bloc (per `feedback_judgment_and_automate.md` commit-positions-don't-menu; AI surfaced positions as REVISE-LOCKED / AMEND-LOCKED / KEEP-LOCKED with rationale; user reply "agreed").

**Sparring findings** (5 REVISE-LOCKED + KEEP-LOCKED for verdict-confirmations):

| # | Element | Tier | User-decision |
|---|---|---|---|
| S1 | Mechanism-class verdict + 4+4 split | T4 | KEEP-LOCKED |
| S2 | §14 application: relocate current §12 → canonical §14 | T3 | REVISE-LOCKED |
| S3 | §14-§18 → §15-§19 renumbering | T3 | REVISE-LOCKED |
| S4 | §13 workflow_instance composition fold into §7 | T3 | REVISE-LOCKED |
| S5 | §10 + §11 duplicate-numbered headings (delete §11 template-meta) | T3 | REVISE-LOCKED |
| S6 | Trust-subsumption breadcrumb strip + "NOT a Pattern A per Step 3 verdict" framing breadcrumbs | T3 | REVISE-LOCKED |
| S7 | "Template note" provenance breadcrumbs strip from §8 + §11 | T3 | REVISE-LOCKED |

**Audit findings** (3 T2 REVISE-LOCKED + 3 T3 REVISE-LOCKED-or-AMEND-LOCKED + KEEP-LOCKED for verdict-confirmations):

| # | Element | Tier | User-decision |
|---|---|---|---|
| A1 | Mechanism-class verdict + audit-trail-as-canonical-source + boot/shutdown ordering + per-shape variation + class boundaries + watch-list + provenance-hygiene + pattern-vs-instance | T4 | KEEP-LOCKED |
| A2 | Trust subsumption framing reframe (audit COMPOSES with authority-binding; doesn't subsume) | **T2** | REVISE-LOCKED |
| A3 | §14 cross-shape policy variation as load-bearing section addition | **T2** | REVISE-LOCKED |
| A4 | §14-§18 → §15-§19 renumbering | **T2** | REVISE-LOCKED |
| A5 | Capability category count 6 → 7 (promote external-format export to G) | T3 | AMEND-LOCKED |
| A6 | Composition row "Authority binding mechanism" cascade-flow from A2 | T3 | REVISE-LOCKED |
| A7 | DR Pattern-A self-description scrub (lines 9, 25, 116, 118, 127) | T3 | REVISE-LOCKED |

### Bundled deferred-item dispositions (cascade-execution scope)

| Deferred item | Disposition | Cascade target |
|---|---|---|
| (a) §14 application sparring | APPLY (relocate current §12 → §14; per S2) | `arch/sparring.md` |
| (a) §14 application audit | APPLY (consolidate distributed §5 + §11 sub-section + §6 row → canonical §14 with 4-dimension matrix; per A3) | `arch/audit.md` |
| (a) §14-§18 → §15-§19 renumbering | APPLY (both topics; per S3 + A4) | both ARCH topics + internal cross-references |
| (b) substrate.md:42 §5 mis-ref fix | APPLY (line 42 says "see §5 Transport variation" but substrate.md §5 is "Selection mechanics"; transport is §12) | `arch/substrate.md` line 42 |
| (c) substrate.md:396 breadcrumb strip | APPLY (`(procedural fidelity at session-16 substrate Round 1)` qualifier on Discipline 1 cross-reference; pattern-equivalent to S7 cleanup) | `arch/substrate.md` line 396 |

## Sharpening provenance

### Wave decomposition + dispatch summary

Single Wave; 4 Wave-1 sub-agents in fresh contexts (validated empirical pattern across 3 prior cluster-executions per Notes 50/51/52). Main session orchestrator-only per `CLAUDE.md` M3.

| Sub-agent | Brief scope | Output |
|---|---|---|
| Writer-1 (sparring pair) | greenfield-derive `arch/sparring.md` + `docs/decisions/sparring-arch-topic.md` from primitives without reading locked content | 9-aspect derivation + 5+3 architecturally/behaviorally split divergence (rejected by Reviewer); §14 framing load-bearing at mechanism-class level; mechanism-class verdict stress-tested + held |
| Writer-2 (audit pair) | greenfield-derive `arch/audit.md` + `docs/decisions/audit-arch-topic.md` from primitives without reading locked content | 11-aspect derivation + 3 candidate REVISION findings (capability count 6→7, Trust subsumption reframing, §14 structurally-required at mechanism-class) |
| Reviewer-1 (sparring pair) | compare Writer-1 derivation vs locked sparring pair; tier divergences | 17 elements verdict-ed; 0 T1 + 0 T2 + 5 T3 + 12 T4; Writer-1's 5+3 split divergence rejected under MAINTENANCE.md §1 discriminator |
| Reviewer-2 (audit pair) | compare Writer-2 derivation vs locked audit pair; tier divergences | 16 elements verdict-ed; 0 T1 + 3 T2 + 3 T3 + 9 T4; Trust subsumption reframing surfaced as T2 substantive (not just breadcrumb); §14 application + renumber as T2 (deferred-resolution mechanism) |

### Per-Writer Ralph self-check verification

| Sub-agent | Required-reads completed | Discipline 10 applied | Locked artifact NOT read | Citations file:line | Verdict |
|---|---|---|---|---|---|
| Writer-1 (sparring pair) | YES (VISION + MAINTENANCE + 16 GLOSSARY + DISCIPLINES 01+10 + 4 profiles + ARCHITECTURE + 2 prior-DRs) | YES (mechanism-class verdict re-derived independently; pause-decision Step 3 cited as INPUT; archive material not transcribed as template) | YES (arch/sparring.md + sparring-arch-topic.md + arch/audit.md + arch/substrate.md + arch/adapter.md NOT read) | YES (per-claim citation chain in §3) | PASS |
| Writer-2 (audit pair) | YES (VISION + MAINTENANCE + 16 GLOSSARY + DISCIPLINES 01+09+10 + 4 profiles + ARCHITECTURE + 2 prior-DRs) | YES (mechanism-class verdict + Trust subsumption stress-tested independently; pause-decision Step 3 + audit-trail-v2 archive cited as INPUT not template) | YES (arch/audit.md + audit-arch-topic.md + arch/sparring.md + arch/substrate.md + arch/adapter.md NOT read) | YES (per-claim citation chain in §3) | PASS |

### Per-Reviewer Ralph self-check verification

| Sub-agent | Locked + Writer read | 4 lenses applied | Tiered each finding | No element unverdict-ed | Verdict |
|---|---|---|---|---|---|
| Reviewer-1 (sparring pair) | YES (arch/sparring.md 367 lines + sparring-arch-topic.md 182 lines + Writer-1 inline derivation) | YES (Lens 5 v0.2.1 provenance hygiene + Lens 8 pattern-vs-instance + Lens 9 VISION-grounding + cascade-miss) | YES (5 NEEDS-REVISION at T3 + 0 T2 + 0 T1; rest T4) | NO (all 17 elements E1-E17 verdict-ed) | PASS |
| Reviewer-2 (audit pair) | YES (arch/audit.md 368 lines + audit-arch-topic.md 168 lines + Writer-2 inline derivation) | YES (Lens 5 v0.2.1 + Lens 6 symmetry + Lens 7 contradictions + Lens 8 + Lens 9 + Discipline 10) | YES (3 T2 + 3 T3 + 0 T1; rest T4) | NO (all 16 elements verdict-ed) | PASS |

### Decomposition mode

Mode 1 (single-decision audit; not composite). Cluster = single audit unit; one Wave; per-artifact verdicts aggregated into single execution outcome. Single Cascade-Writer + Cascade-Reviewer pair handles all 12 findings + 5 bundled deferred items in one cascade commit.

### Decomposition mode (provisional pre-Wave-1 framing; superseded by Mode 1 confirmed above)

Provisional framing kept for trace; superseded by confirmed Mode 1 above.

## Composition with existing architecture

**Cross-execution position**: 4th greenfield-rederivation cluster-execution per skill empirical-evidence rule. Pattern-stable signal continues per prior executions: substantive architecture survives greenfield re-derivation; drift = Lens 5 v0.2.1 retro-application + cascade-miss to upstream/downstream artifacts predating M1-M8.

**Phase 3.4 v2-audit campaign closure**: this execution closes the Phase 3.4 audit campaign. Post-execution status: Phase 3.1 (4 DRs) + Phase 3.2 (composite DR) + Phase 3.4 substrate+adapter (4 artifacts) + Phase 3.4 sparring+audit (4 artifacts) all v2-audited. Coherence-audit checkpoint C1 (post-Phase-3.4 close per `BACKLOG.md` audit-checkpoint cadence) becomes runnable post-this-execution.

**Pattern A template extensibility validation**: post-amendment template at 12+7 conditional sections. Sparring + audit are mechanism-class topics (NOT Pattern A). Writer briefs surface template-applicability boundary: which Pattern A sections apply / which N/A / whether mechanism-class warrants its own template (potential T1 finding if greenfield-derivation surfaces this as architectural gap).

**Bundled deferred-item composition**: §14 application + substrate.md fixes are operationally bundled into this v2-audit's Cascade execution per BACKLOG Phase 3.4 + skill §Cascade execution. Cascade-Writer brief explicit on bundled scope.

**Coherence-audit composition**: per skill §Composition with other PBS dev skills — greenfield-rederivation catches per-artifact derivation drift; coherence-audit catches set-level drift. Phase-boundary audit C1 (post-Phase-3.4) runs both skills composed; this execution provides the per-cluster greenfield-derivation pass; coherence-audit follows.

## Constraints flowing to downstream commitments

### Cascade scope (delegated to fresh-context Cascade-Writer + Cascade-Reviewer per `CLAUDE.md` M3+M4)

5 files in tightly-coupled cascade commit:
1. `arch/sparring.md` — apply S2-S7 (5 mechanical edits + bundled deferred (a))
2. `arch/audit.md` — apply A2-A6 (Trust framing reframe + §14 addition + §14-§18 renumber + capability G promotion + composition row cascade-flow + bundled deferred (a))
3. `docs/decisions/audit-arch-topic.md` — apply A7 (Pattern-A self-description scrub: 5 occurrences)
4. `ARCHITECTURE.md` §7 line 219-221 — Trust framing cascade-flow from A2
5. `arch/substrate.md` — apply bundled deferred (b) line 42 mis-ref fix + (c) line 396 breadcrumb strip

### Post-cascade implications

- **Phase 3.4 v2-audit campaign close** — post-cascade, all Phase 3.4 v2-audit clusters complete (Phase 3.1 4-DRs + Phase 3.2 composite + Phase 3.4 substrate+adapter + Phase 3.4 sparring+audit). Coherence-audit checkpoint C1 (post-Phase-3.4) becomes runnable per `BACKLOG.md` audit-checkpoint cadence + `disciplines/09-coherence-audit-cadence.md`
- **Phase 3.5 + 3.6 unblocked** — sparring+audit v2-audit closure removes any v2-audit prerequisite for Phase 3.5 primitive-cluster work + Phase 3.6 quality-gate ARCH topic
- **Authority-binding mechanism standalone status** (consequence of A2 Trust framing reframe) — authority-binding is its OWN framework mechanism per `MAINTENANCE.md`:69; not subsumed by audit. Future quality-gate ARCH topic (Phase 3.6) composes with authority-binding directly per substrate Surface §C permission flow integration. No new ARCH topic for authority-binding warranted (mechanism-level treatment in MAINTENANCE.md TOP-LEVEL ARCHITECTURE concept-by-concept table sufficient; no full ARCH-topic surface)
- **Cross-execution stable-corpus signal status** — Phase 3.4 cluster did not yield T4-only verdicts (3 T2 + 8 T3 surfaced); does NOT meet stable-corpus signal per skill §Termination criteria. Per-cluster greenfield-rederivation cadence holds for any future Phase 3.5+ clusters surfacing similar deferred-resolution-debt or substantive-framing-debt
- **Pattern across all four cluster-executions stable**: 0 T1 across all clusters (substantive architecture survives) + scoped T2/T3 drift = Lens 5 v0.2.1 retro-application + cascade-miss legacy + (newly) substantive-framing-debt accumulated under prior cascade-load conditions. Skill v0.1.0 stays preliminary-locked; ≥2-execution amendment threshold unchanged

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
