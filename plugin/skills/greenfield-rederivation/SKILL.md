---
name: greenfield-rederivation
description: "**READ THIS FILE BEFORE APPLYING. Use the Read tool to load this SKILL.md at every invocation, regardless of prior usage in same session — pattern-matching from memory of prior usage FAILS load-bearing discipline elements (per `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)).** Use to re-derive a CLUSTER of already-locked architectural artifacts (DRs / ARCH topics / GLOSSARY entry-bodies) from primitives — VISION + locked GLOSSARY + first-principles disciplines — and compare to currently-locked content to surface drift / cargo-cult / cascade-miss / instance-leakage that prior cascade-load conditions allowed through. Triggers via natural-language prompts including \"audit the foundation\", \"re-derive from scratch\", \"greenfield-check this cluster\", \"are these still right\", \"foundation re-derivation pass\", \"audit prior architectural work\", \"v2 greenfield audit\". Phase 3 audit family — distinct from `decision-design-sharpening` (Phase 1; pre-decision; one decision; pre-commit) and `pre-implementation-sharpening` (Phase 2; one decision; at implementation-start) and `coherence-audit` (Phase 3; cross-decision corpus audit; lens-driven). Greenfield-rederivation is the audit pattern that re-derives from primitives rather than scanning across the corpus — distinct from coherence-audit's lens-driven corpus scan. NOT for in-flight decision-design (use decision-design-sharpening). NOT for trivial single-DR re-reads. NOT a substitute for coherence-audit (different fault modes; the two compose)."
when_to_use: After a CLUSTER of locked architectural artifacts (DRs / ARCH topics / GLOSSARY entry-bodies) has accumulated under conditions that may have impaired faithful execution (cascade-load; oversized context; single-AI execution without Reviewer pass); user wants foundation-up greenfield-rederivation audit per cluster. Natural triggers: "re-derive from scratch", "greenfield-check this cluster", "audit foundation", "v2 audit pass". Do NOT use for in-flight single-decision sharpening — that's decision-design-sharpening.
version: 0.1.0
---

# Greenfield-rederivation (Phase 3 audit family)

> **Extends `sharpen`** (the generic critical-pass skill) with formality specific to per-cluster foundation-up re-derivation: each artifact in the cluster is re-derived from primitives (VISION + locked GLOSSARY + first-principles disciplines) by an isolated greenfield-Writer sub-agent, then compared to the locked content by an independent Reviewer sub-agent, with divergences surfaced for user reconciliation. The core mechanic (read → critical lens → Pareto-graded positions → counter-validation → self-check) is inherited from `sharpen`; this skill adds the per-cluster sub-agent-orchestration procedure + tiered-divergence verdict scheme + per-execution DR shape.

Cross-artifact audit applied to a CLUSTER of already-locked work. Operates by re-deriving each artifact from primitives in isolation, then comparing the greenfield-derivation against the locked content. Different from `coherence-audit` (which scans the corpus through lenses; this skill re-derives from foundations).

## Status — preliminary-locked at v0.1.0

Amendments per empirical-evidence rule: ≥2 cluster-executions of pattern threshold before the skill itself is amended. Per `sharpen` v0.12.0 empirical-evidence amendment rule. Single-execution evidence does NOT justify amendment; cross-execution pattern does. This skill is itself a methodology artifact and is governed by the same amendment discipline it codifies for the architectural artifacts it audits.

## Spirit (anchor for future revisions)

The audit pattern this skill codifies: **re-derive each artifact greenfield from VISION + locked GLOSSARY + first-principles disciplines; compare to locked content; surface divergences as Tiered findings; user reconciles each.** The pattern is sound. What makes it WORK in practice — vs being undermined by the same conditions that produced the drift it's designed to detect — is the orchestration shape:

1. **Per-cluster scope**, not full-corpus. Smaller scope keeps any single execution within context-budgets where instruction-adherence holds.
2. **Per-artifact sub-agent dispatch**. Each artifact's greenfield-derivation runs in a fresh-context sub-agent with focused brief, NOT in a long-context main session. The audit pattern applied to itself: the audit must not be executed by an agent under the same load conditions it's auditing.
3. **Writer-Reviewer pattern per artifact**. Same agent writes greenfield-derivation AND judges it against locked content = self-praise bias. Separate Reviewer sub-agent against the diff counters this.
4. **HARD STOP per wave**. Multi-wave executions span sessions. Each wave persists its own findings; main session orchestrates without accumulating context.
5. **User-reconciliation per divergence**. The audit surfaces divergences + recommendations; the user decides per finding. Auto-applying divergences would substitute audit-judgment for architectural authority.

Future revisions test: does the change preserve the per-cluster + per-artifact-sub-agent + Writer-Reviewer + user-reconciliation shape? If a revision allows main-session execution OR single-agent Writer-and-Reviewer OR auto-applied divergences, it drifts from spirit.

**Why this shape, not a simpler one**: the audit pattern (re-derive from primitives; compare; surface divergences) was field-tested as a 7-step single-session procedure. The procedure was sound; the execution surface (single-agent under cascade-load) reproduced the META-failure conditions the procedure was meant to detect, leaving the audit itself unable to credibly claim it caught all errors. The orchestration shape above corrects the META-failure surface while preserving the audit pattern.

**Self-applicability test**: this skill must remain runnable on any cluster of pbs-bureau architectural artifacts without re-tooling. If a revision makes the skill specific to one cluster type (e.g., only DRs; only ARCH topics), it has drifted from spirit.

## When to use

- A cluster of architectural artifacts has been locked AND user wants foundation-up re-derivation audit
- Cluster examples (foundation-first ordering recommended):
  - Phase 3.1 4 DRs (workflow / work-unit / deployment / engaged-authorship)
  - Phase 3.2 composite DR + topic catalog
  - Substrate ARCH topic (+ DR)
  - Adapter ARCH topic (+ DR)
  - Sparring ARCH topic (+ DR; post-reclassification)
  - Audit ARCH topic (+ DR; post-reclassification)
  - Per-DR-cluster of remaining DRs
  - GLOSSARY entry-bodies grouped by category (likely 3+ executions across 36 entries; categorization defined per-execution rather than prescribed by skill)
- Cluster size: aim for 2-6 artifacts per execution. Larger → decompose into multiple cluster-executions.

## When NOT to use

- **In-flight decision-design** (decision not yet locked) → use `decision-design-sharpening`
- **Implementation-start operational-detail surfacing** → use `pre-implementation-sharpening`
- **Cross-decision lens-driven corpus audit** (asking "is the set composition right?" / "are tags right?" / "is symmetry intact?") → use `coherence-audit`. The two compose: coherence-audit catches set-level / vocabulary-level / cascade-level issues by scanning across; greenfield-rederivation catches drift / cargo-cult / instance-leakage / cascade-miss within each artifact by re-deriving from primitives. Run both at phase boundaries.
- **Trivial single-DR re-read** that doesn't merit sub-agent orchestration → just re-read it
- **A cluster already audited at v2 within recent sessions with no new locked work since** → audit deltas suffice (per `coherence-audit` audit-scaling)

## Inputs to a v2 execution

| Input | Authority | Used as |
|---|---|---|
| `VISION.md` | Anchor | Primary derivation source for each artifact |
| Locked `GLOSSARY.md` + `glossary/<entry>.md` | Anchor for locked entries | Primary derivation source; primitive-vocabulary the artifact must speak |
| First-principles disciplines (`MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1/§2/§3; A-B-C scope model; framework=mechanisms / shape=policies; pattern-vs-instance) | Anchor | Derivation chain checks |
| `DISCIPLINES.md` + relevant `disciplines/<id>.md` | Anchor | Procedure + provenance hygiene + greenfield-evaluation discipline |
| Each cluster artifact (current locked content) | Comparison target | Greenfield-vs-locked diff |
| Prior greenfield-rederivation findings (any superseded / archived predecessor) | HISTORICAL INPUT — not authoritative | Context for reviewer; does NOT pre-determine current verdicts. Current execution may confirm or diverge. |

**Authority note**: VISION axes are anchored (revise only on real-world falsification per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3); GLOSSARY is preliminary-locked but treated as derivation-substrate during an execution (revising GLOSSARY changes the substrate; surface as a separate derivation chain rather than mid-execution). If execution surfaces a finding that GLOSSARY itself needs revision, that's a Tier-1 finding triggering its own GLOSSARY-cluster execution before downstream artifacts re-audit.

## Procedure

### Pre-execution: cluster definition + Wave decomposition

Main-session orchestrator (the AI invoking this skill) does, in order:

1. **Define cluster scope**. Name the artifacts in scope (paths). Aim 2-6 artifacts. If more, propose decomposition into multiple cluster-executions (each its own per-execution DR).
2. **Identify Waves within the cluster**. Each Wave = 3-4 artifacts dispatched in parallel sub-agents. A 6-artifact cluster = 2 Waves. A 3-artifact cluster = 1 Wave.
3. **Identify foundation-up dependencies within cluster**. If artifact B depends on artifact A's locked classification (e.g., per-topic ARCH depends on Pattern-A framework lock), Wave-1 audits A; Wave-2 audits B with A's verdict in hand. Per `DISCIPLINES.md` Discipline 8 foundation-up ordering.
4. **Surface cluster + Waves to user before dispatch**. User confirms scope or adjusts. Per `DISCIPLINES.md` working procedure (decision phase = approval).
5. **Create per-execution DR stub** at `docs/decisions/greenfield-rederivation-<YYYY-MM-DD>-<cluster-slug>.md`. Status: PROPOSED. Cluster definition + Wave decomposition persisted before any sub-agent fires. Per `MAINTENANCE.md` DR template (Layer 4).

### Per-Wave: parallel sub-agent dispatch

For each Wave:

1. **For each artifact in the Wave, dispatch TWO sub-agents in parallel** (single message; multiple Agent tool invocations):
   - **Writer sub-agent** with greenfield-Writer brief (template below)
   - **Reviewer sub-agent** with Reviewer brief (template below) — runs against the Writer's output once Writer returns
2. **Wait for all Writers to return**. Then dispatch all Reviewers in parallel against their respective Writer outputs (or, if context allows, dispatch Writer + Reviewer-on-Writer-completion as a single chained invocation per artifact).
3. **Main session does NOT do greenfield-derivation itself**. Main session is orchestrator only. Per `CLAUDE.md` Cascade discipline M3: "Sub-agent works in clean fresh context; returns summary; main agent reviews + commits + pushes."
4. **Aggregate per-Wave findings into per-execution DR**. Each artifact's verdict + tiered divergences persisted. Per-execution DR's "Findings" section grows per Wave.
5. **Recommend `/clear` to user before next Wave** (if more Waves remain). Per `CLAUDE.md` Cascade discipline M5.
6. **HARD STOP at Wave boundary** if multi-Wave execution. Persist findings; commit + push; STOP. Resume next session for next Wave. Per `CLAUDE.md` Cascade discipline M6.

### Post-cluster: user-reconciliation phase

After all Waves complete:

1. **Surface each divergence to user with recommendation**. AI commits a position per divergence (REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED) per `feedback_judgment_and_automate.md` (commit positions; don't menu).
2. **User decides per divergence**. Decision phase = user approval per `DISCIPLINES.md` working procedure.
3. **Per-execution DR status**: PROPOSED → ACCEPTED-VALIDATED (no divergences) OR ACCEPTED-WITH-FINDINGS (divergences with user-decisions persisted).
4. **DO NOT auto-apply divergences**. Auto-apply substitutes audit-judgment for architectural authority. Surface, recommend, await user.

### Cascade execution (post-reconciliation)

If user-decided revisions exist:

1. **Cascade execution is itself architectural multi-file work** → per `CLAUDE.md` Cascade discipline M3, delegate cascade to fresh-context sub-agent(s). Do NOT execute cascade in main session.
2. Per `MAINTENANCE.md` cascade discipline + foundation-up ordering: tightly-coupled commits per affected layer.
3. Reviewer sub-agent against the cascade diff before push (Writer-Reviewer per `CLAUDE.md` M4).
4. Per-execution DR amended with cascade-completion note when cascade finishes.

## Sub-agent brief template — greenfield-Writer

The Writer sub-agent re-derives ONE artifact from primitives in isolation. It does NOT see the locked artifact during derivation.

```
You are a greenfield-Writer sub-agent for a pbs-bureau cluster audit.

# Task
Greenfield-derive the following artifact from primitives, working in isolation.

# Artifact
<path to artifact under audit; e.g., `docs/decisions/workflow-bipartite-classification.md`>

# Required reads (in order; do all before deriving)
1. `VISION.md` — full file
2. `MAINTENANCE.md` — TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 + TOP-LEVEL ARCHITECTURE
3. `GLOSSARY.md` (index) + relevant `glossary/<entry>.md` files for primitives the artifact handles
4. `DISCIPLINES.md` index + `disciplines/01-source-grounded.md` + `disciplines/10-greenfield-evaluation.md`
5. `profiles/INDEX.md` + ≥3 cluster-relevant profile files (cite which clusters apply)

# DO NOT READ during derivation
- The artifact under audit (you derive greenfield; comparison happens at Reviewer stage)
- Other locked architectural artifacts in the same cluster (each is derived independently)
- Prior greenfield-rederivation findings (HISTORICAL INPUT only; bias-free derivation requested)

# Derive
Per the artifact's stated scope (Title + Status + Owner; provided in brief), produce a greenfield derivation:
- What primitives apply (cite GLOSSARY entries)?
- What VISION axes ground them (cite line numbers)?
- What first-principles disciplines constrain shape (cite MAINTENANCE §§)?
- What does the artifact's content shape look like derived from primitives alone?

Cite EVERY claim (file:line). Flag synthesis vs citation per Discipline 1.

# Output (return to main session)
- Greenfield-derivation summary (the shape you'd lock today; 200-400 lines)
- Citation chain per claim
- Self-check at completion (Ralph Loop):
  - Did I read every required-read file?
  - Did I apply Discipline 10 (greenfield-evaluation; archive citations as INPUT not TEMPLATE)?
  - Did I avoid reading the locked artifact?
  - Did I cite specific GLOSSARY entries / VISION line numbers / MAINTENANCE §§?

# Constraints
- Provenance hygiene: NO "session N" / "AMENDED" / "as of <date>" breadcrumbs in derivation content
- Sub-agent-first: you are a Writer sub-agent; do NOT delegate further
- HARD STOP at completion: return summary; do not continue beyond brief
```

## Sub-agent brief template — Reviewer

The Reviewer sub-agent compares the Writer's greenfield-derivation against the locked artifact and surfaces tiered divergences.

```
You are a Reviewer sub-agent for a pbs-bureau cluster audit.

# Task
Compare a greenfield-derivation (from Writer sub-agent) against the currently-locked artifact. Surface divergences as Tiered findings.

# Inputs
- Writer's greenfield-derivation summary: <inline or path>
- Locked artifact path: <path>

# Required reads (in order; do all before reviewing)
1. The locked artifact (full file)
2. `VISION.md` (full)
3. `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES + TOP-LEVEL ARCHITECTURE
4. `disciplines/10-greenfield-evaluation.md`
5. `plugin/skills/coherence-audit/SKILL.md` Lens 5 (provenance hygiene) + Lens 8 (pattern-vs-instance) + Lens 9 (VISION-grounding)

# Surface divergences per element
For each element where greenfield-derivation diverges from locked content, classify:

| Verdict | Meaning |
|---|---|
| GREENFIELD-VALID | Element derives cleanly from VISION / GLOSSARY / first-principles WITHOUT archive contamination; current locked shape passes greenfield-derivation chain |
| INPUT-ONLY-VALID | Element references archived/prior material as INPUT (informs shape) but greenfield-derivation chain holds independently; archive is source-of-context not template |
| NEEDS-REVISION | Locked content has cargo-cult / ambiguity / partial drift; specific revision identifiable (rename / re-classify / sharpen / fix instance-leakage) |
| NEEDS-REWORK | Foundational drift; substantial redo required; affects downstream artifacts |

For each NEEDS-REVISION or NEEDS-REWORK, additionally tier:

| Tier | Meaning |
|---|---|
| T1 — framework-shape-changing | Cascades across multiple artifacts (e.g., primitive-set change; pattern-classification change; topic-catalog change) |
| T2 — topic-rewriting | Substantive single-artifact rewrite (frontmatter + body sections) |
| T3 — mechanical edit | Localized fix (rename / cross-ref correction / minor language sharpening) |
| T4 — confirms-locked | No revision; locked content survives greenfield comparison |

Cite source-grounded evidence per finding (file:line).

# Apply lenses
- Pattern-vs-instance leakage (per coherence-audit Lens 8): does locked content embed pioneer-instance / archetype-instance / regulatory-instance assumptions?
- VISION-grounding (per coherence-audit Lens 9): does each claim trace to VISION?
- Provenance hygiene (per coherence-audit Lens 5): does locked content contain narrative breadcrumbs ("session N", "AMENDED", "as of <date>") in canonical sections?
- Cascade-miss: are cross-references / composes-with claims symmetric with cited entries?

# Output (return to main session)
- Per-element verdict table (verdict + tier + cited evidence)
- Highest-tier finding summary (any T1? any T2?)
- Recommendation per finding (REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED)
- Self-check at completion (Ralph Loop):
  - Did I read the locked artifact AND the Writer derivation?
  - Did I apply each of the 4 lenses (pattern-vs-instance / VISION-grounding / provenance hygiene / cascade-miss)?
  - Did I tier each NEEDS-REVISION or NEEDS-REWORK finding?
  - Did I leave any element unverdict-ed?

# Constraints
- Provenance hygiene: NO breadcrumbs in your output that would cascade into canonical content if applied
- Self-praise counter: you did NOT write the greenfield-derivation; surface divergences honestly even if Writer "feels right"
- HARD STOP at completion: return summary; do not continue
```

## Verdict scheme

**Per-artifact verdict (Writer-derived shape vs locked content)**:
- **GREENFIELD-VALID** — locked content passes greenfield-derivation chain
- **INPUT-ONLY-VALID** — archive/prior material is INPUT not TEMPLATE; greenfield-chain holds
- **NEEDS-REVISION** — specific revision identified
- **NEEDS-REWORK** — substantial redo required

**Tier (for NEEDS-REVISION + NEEDS-REWORK)**:
- **T1** — framework-shape-changing (cascades; multiple artifacts affected)
- **T2** — topic-rewriting (substantive single-artifact rewrite)
- **T3** — mechanical edit (localized fix)
- **T4** — confirms-locked (verdict applied to non-divergence; tracks audit completeness)

**User-decision verdict per divergence (post-Reviewer)**:
- **REVISE-LOCKED** — apply revision per Reviewer's recommendation; cascade
- **KEEP-LOCKED** — locked content stands; Reviewer's divergence rejected
- **AMEND-LOCKED** — partial application; specific amendment differs from Reviewer's recommendation
- **SUPERSEDE-LOCKED** — locked artifact superseded by new artifact; per `MAINTENANCE.md` DR supersession discipline

## Per-execution DR shape

Each execution produces `docs/decisions/greenfield-rederivation-<YYYY-MM-DD>-<cluster-slug>.md`. Follows `MAINTENANCE.md` Layer 4 DR template; populates these fields:

| Field | Content |
|---|---|
| Status | PROPOSED → ACCEPTED-VALIDATED (no findings) OR ACCEPTED-WITH-FINDINGS (findings + user-decisions) |
| Owner | Phase 3 audit family; this skill version; cluster scope |
| Related | This SKILL.md; cluster artifacts (paths); any prior greenfield-rederivation DR for context (HISTORICAL INPUT) |
| Context | Why this cluster, why now (cluster-bounded scope; cluster's foundation-up position; any prior-execution context) |
| Decision | Per-artifact verdict + tier per divergence; user-decision per divergence |
| Sharpening provenance | Wave decomposition; per-Wave Writer + Reviewer dispatch summary; Ralph self-check confirmation per sub-agent |
| Composition with existing architecture | Cascade scope if revisions; downstream artifacts affected (foundation-up); coherence-audit composition (this audit catches re-derivation drift; coherence-audit catches set-level drift) |
| Constraints flowing | Per-artifact revisions (paths + nature); cascade-completion commitment |
| Files touched | This DR + per-Wave Findings amendments + cascade artifacts (in cascade commits) |
| Revisit triggers | New artifact added to cluster; user-flagged drift on cluster; phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` |

## Anti-patterns

| Anti-pattern | Counter |
|---|---|
| Single-AI cascade execution (main session does Writer + Reviewer + cascade) | Per-cluster + per-artifact sub-agent + Writer-Reviewer separation per `CLAUDE.md` M3+M4. The audit pattern applied to itself. |
| Skipping Reviewer pass on Writer output | Self-praise bias; same agent writes + judges = predictable confirmation. Reviewer is structural counter per `CLAUDE.md` M4. |
| Auto-applying divergences without user decision | Substitutes audit-judgment for architectural authority. User decides per divergence. |
| Cluster too large for single execution (>6 artifacts) | Decompose into multiple cluster-executions. Smaller scope keeps adherence within context-budgets. |
| Pattern-matching from prior greenfield-rederivation findings | Prior findings are HISTORICAL INPUT not AUTHORITATIVE VERDICTS. Each execution re-derives fresh. Per `disciplines/01-source-grounded.md` (pattern-matching from synthesis ≠ direct evidence). |
| Reading the locked artifact during Writer derivation | Contaminates greenfield-derivation; produces "looks-similar-therefore-validated" shortcut. Writer must NOT read locked artifact. |
| Provenance breadcrumbs in derivation output OR Reviewer output | Cascades into canonical content if applied. Per coherence-audit Lens 5. |
| Recognition-pattern bias (high archive-fit = "feels right" = lower stress-test) | Per `disciplines/10-greenfield-evaluation.md`: when archive seems to fit, INCREASE stress-test rigor. |
| Skipping HARD STOP at Wave boundary | Main-session context accumulates; subsequent Waves degrade. Per `CLAUDE.md` M6. |

## Termination criteria

**Per-Writer (sub-agent self-check)**: Ralph Loop at completion. Brief returns only after the sub-agent verifies — did-I-read-everything / apply-every-discipline / leave-anything-unfinished. Per `CLAUDE.md` M7.

**Per-Reviewer (sub-agent self-check)**: Ralph Loop at completion. Brief returns only after Reviewer verifies — read both Writer + locked, applied 4 lenses, tiered each finding, no element unverdict-ed.

**Per-Wave (main-session)**: All Writers returned + all Reviewers returned + per-artifact verdict persisted to per-execution DR + commit + push + recommend `/clear` to user → HARD STOP if more Waves.

**Per-cluster (main-session)**: All Waves complete + user-reconciliation per divergence + per-execution DR status set (ACCEPTED-VALIDATED or ACCEPTED-WITH-FINDINGS) + cascade scoped (delegated to sub-agent if needed) + commit + push.

**Per-multi-cluster (multi-execution audit campaign)**: Each cluster-execution is its own logical unit; HARD STOP between cluster-executions. No "audit everything in one session" framing — that's the META-failure surface this skill exists to avoid.

**Stable-corpus signal**: when consecutive cluster-executions yield 0 NEEDS-REVISION + 0 NEEDS-REWORK across all artifacts (only T4-confirms-locked findings), corpus is greenfield-stable for that scope. Cadence shifts to delta-audits per `coherence-audit` audit-scaling strategies.

## Composition with other PBS dev skills

| Skill | Composition |
|---|---|
| `decision-design-sharpening` | Phase 1 of decision lifecycle; PRE-decision; this skill operates POST-lock on accumulated decisions. The two cover different lifecycle moments. |
| `pre-implementation-sharpening` | Phase 2 of decision lifecycle; AT implementation-start. This skill operates BEFORE implementation begins for any of its cluster artifacts; orthogonal timing. |
| `coherence-audit` | Peer Phase 3 audit skill. Coherence-audit scans corpus through 10 lenses (set composition / tags / vocabulary / cascade / mechanical / symmetry / contradictions / pattern-vs-instance / VISION-grounding / cardinality+lifecycle); greenfield-rederivation re-derives each artifact from primitives. **The two compose** at phase-boundary audits: coherence-audit catches set-level + vocabulary-level + cascade-level drift; greenfield-rederivation catches per-artifact derivation drift / cargo-cult / instance-leakage / cascade-miss. Run both at phase boundaries; coherence-audit first (set-level) then greenfield-rederivation (per-cluster). |
| `sharpen` | Generic critical-pass parent. This skill extends the read → critical lens → Pareto-graded positions → counter-validation → self-check core. |
| Cascade discipline (`MAINTENANCE.md` TOP-LEVEL RULE) | This skill's post-reconciliation cascade execution USES cascade discipline (foundation-up ordering; tightly-coupled commits; sub-agent delegation per `CLAUDE.md` M3). |
| Discipline 9 — Coherence-audit cadence (`disciplines/09-coherence-audit-cadence.md`) | This skill activates at the same checkpoint windows where coherence-audit fires. Phase-boundary audits run BOTH skills (composed). |
| Discipline 10 — Greenfield evaluation of archived material (`disciplines/10-greenfield-evaluation.md`) | This skill is the codified per-cluster procedure for what Discipline 10 prescribes per element. Discipline 10 = the rule; this skill = the orchestrated multi-file procedure. |

## Concrete invocation example

```
1. User signals: "let's run greenfield-rederivation on Phase 3.1 4 DRs"

2. Main session activates skill; reads SKILL.md fresh (per Discipline 1 skill+profile sub-section)

3. Main session defines cluster + Wave decomposition
   → Cluster: workflow / work-unit / deployment / engaged-authorship DRs (4 artifacts)
   → 1 Wave (4 artifacts; within 3-4 parallel sweet-spot)
   → Per-execution DR stub created at docs/decisions/greenfield-rederivation-<date>-phase-3-1-drs.md

4. User confirms scope

5. Main session dispatches 4 Writer sub-agents in parallel (single message; 4 Agent invocations)
   → Each Writer: reads VISION + GLOSSARY + MAINTENANCE + DISCIPLINES + ≥3 profiles; derives target artifact greenfield; does NOT read locked artifact
   → Each Writer returns greenfield-derivation summary

6. Main session dispatches 4 Reviewer sub-agents in parallel
   → Each Reviewer: reads locked artifact + Writer derivation + 4 lenses; produces verdict + tier per divergence

7. Main session aggregates findings into per-execution DR

8. User-reconciliation phase
   → AI surfaces each divergence + recommendation (REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED)
   → User decides per divergence

9. Per-execution DR status: ACCEPTED-VALIDATED or ACCEPTED-WITH-FINDINGS

10. If revisions: cascade delegated to fresh sub-agent (Writer-Reviewer per cascade chunk)

11. Commit + push; HANDOFF note; HARD STOP
```

## Ralph self-check at apparent completion (mandatory)

Before declaring an execution complete, main-session AI explicitly verifies:

- Did I read this SKILL.md fresh at invocation (not pattern-matched)?
- Did each Writer sub-agent confirm Ralph self-check at its completion?
- Did each Reviewer sub-agent confirm Ralph self-check at its completion?
- Did I avoid executing greenfield-derivation in main session?
- Did I dispatch Reviewer separate from Writer per artifact?
- Did I persist per-Wave findings to per-execution DR before next Wave?
- Did I recommend `/clear` at Wave boundaries?
- Did I HARD STOP at multi-Wave session boundaries?
- Did I commit positions per divergence to user (not menu options)?
- Did I delegate cascade execution to sub-agent rather than execute in main session?
- Did the per-execution DR pass provenance-hygiene (no narrative breadcrumbs in canonical content)?

If any answer is NO, address before declaring complete. Per `CLAUDE.md` M7 + `feedback_ralph_self_check.md`.
