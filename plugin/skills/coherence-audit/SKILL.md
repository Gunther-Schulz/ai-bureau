---
name: coherence-audit
description: "**READ THIS FILE BEFORE APPLYING. Use the Read tool to load this SKILL.md at every invocation, regardless of prior usage in same session — pattern-matching from memory of prior usage FAILS load-bearing discipline elements (per `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)).** Use when multiple architectural decisions / GLOSSARY entries / DRs / specs have already been locked and the user wants a CROSS-DECISION audit pass on the corpus as a SET — not within-decision sharpening. Triggers via natural-language prompts including \"audit the glossary\", \"review the corpus\", \"cross-entry audit\", \"is the architecture clean\", \"are these the right primitives\", \"primitive-set audit\", \"set-level review\", \"coherence check\", \"is the vocabulary coherent\". Phase 3 of the dev-skill family — distinct from `decision-design-sharpening` (pre-decision; one decision; pre-commit) and `pre-implementation-sharpening` (one decision; at implementation-start). NOT for within-entry refinement on a single decision (use decision-design-sharpening). NOT for operational-detail surfacing on one decision (use pre-implementation-sharpening)."
when_to_use: After multiple decisions / GLOSSARY entries / DRs are locked; user wants a SET-level audit. Natural triggers: "audit glossary", "review corpus", "cross-entry audit", "are these the right primitives", "primitive-set audit", "is the architecture clean", "coherence check". Do NOT use for single-decision sharpening — that's decision-design-sharpening.
version: 0.3.3
---

# Coherence audit (Phase 3 dev skill)

> **Extends `sharpen`** (the generic critical-pass skill) with formality specific to cross-decision corpus audit: 10 universal lenses (set composition / tag corrections / vocabulary coherence / cross-ref cascade health / mechanical compliance / symmetry / definition contradictions / pattern-vs-instance / VISION-grounding / cardinality+lifecycle) + corpus-specific lenses (ARCH 11-15; DR-set 16; spec-set 17-18) + cascade-aware revision application. The core mechanic (read → critical lens → Pareto-graded positions → counter-validation → self-check) is inherited from `sharpen`; this skill adds the context-specific lenses + corpus-level procedure.

Cross-decision audit applied AFTER multiple architectural decisions are locked. Operates on the corpus as a SET — different from per-decision sharpening which operates on one decision pre-commit.

## Why this skill exists (vs the other two sharpening skills)

| Skill | Scope | Timing | Mode |
|---|---|---|---|
| `decision-design-sharpening` | ONE decision | PRE-commit | Sparring (challenge proposed shape) |
| `pre-implementation-sharpening` | ONE decision | AT implementation-start | Coverage (operational + runtime + deployment layers) |
| **`coherence-audit`** (this skill) | MULTIPLE decisions | AFTER several commits | Set-level (does the corpus cohere?) |

Per-decision sharpening can't see set-level problems: primitive-set correctness, cross-entry vocabulary clashes, cascade-health across the locked set, missing primitives, redundant primitives. Those need a corpus-as-a-whole pass.

## Why this skill is distinct from drift-detection / soundness-review (which would be app-skill territory)

- **Drift detection** scans for what's CHANGED relative to a baseline (post-mortem)
- **Soundness review** validates against declared rules (validator-mode)
- **Coherence audit** asks "is the corpus structurally right?" — closer to sparring-mode, applied at SET level

The first two are app-skill territory (PBS-domain workflow); coherence-audit is dev-skill territory (work ON the framework).

## When this skill fires

- User signals: "audit glossary" / "review corpus" / "are these the right primitives" / "is the architecture clean" / "primitive-set audit" / "cross-entry audit" / "coherence check"
- After a sequence of decisions has been locked (typically 5+ entries / DRs since last audit)
- Before promoting locked entries to higher-stability classification
- Before a phase boundary (e.g., before Phase 3 ARCH rebuild starts)

NOT for:
- Single-decision sharpening (use `decision-design-sharpening`)
- Implementation-start operational-detail surfacing (use `pre-implementation-sharpening`)
- Post-decision drift detection (different concern)
- Validating against a declared rules-set (validator-mode; different concern)

## The 10 lenses (v0.2.0 reorg)

Run each lens explicitly. **Lens 1 (set composition) + Lens 7 (pattern-vs-instance) + Lens 8 (VISION-grounding) are the load-bearing ones** — they're what per-decision sharpening structurally cannot see and what self-validation bias suppresses without explicit prompting.

**v0.2.0 changes** (from v0.1.0): split former Lens 1 into Lens 1 (set composition, 5 sub-q) + Lens 2 (tag corrections, 5 sub-q); promoted Symmetry sub-question to standalone Lens 6; merged former Lens 4 (tag consistency) + Lens 6 (source-grounded) → Lens 5 (mechanical compliance); dropped former Lens 7 (within-entry sharpening — defer to decision-design-sharpening); added new Lens 10 (cardinality + lifecycle).

### Lens 1: Set composition (LOAD-BEARING)

The "is the set right?" lens. 5 sub-questions, all about WHICH primitives exist:

1. **MERGE** — should any primitives combine into one? (Two cover overlapping ground; or one is a refinement of the other → could be DERIVED)
2. **SPLIT** — should any primitive split into two? (One primitive doing two jobs; clearer separated)
3. **ADD** — any missing primitives? (Concept load-bearing across multiple entries with no canonical home)
4. **REMOVE** — any redundant primitives? (Exists only as cross-ref / nomenclature anchor; no independent semantic content)
5. **REDEFINE BOUNDARIES** — primitive A's What-it-is-NOT vs primitive B's What-it-is cleanly partition conceptual space? Or overlap / leave gaps?

This lens runs AGAINST the corpus, not against any single entry. Surfacing requires reading multiple entries together.

**Anti-pattern**: surfacing only within-entry refinements when running this lens (those belong in `decision-design-sharpening`). If Lens 1 yields zero findings, force the question: "did I actually try MERGE / SPLIT / ADD / REMOVE / BOUNDARY, or did I default to in-entry critique?" Self-validation bias defaults to the latter.

### Lens 2: Tag corrections

The "are tags right?" lens. 5 sub-questions, all about HOW primitives are classified:

1. **Class re-classification** — PRIMITIVE↔META-PRIMITIVE↔DERIVED↔SCOPE-CLASSIFICATION↔STUB
2. **Layer re-classification** — cross-cutting↔multi-aspect↔framework-mechanism↔shape-policy↔framework-meta
3. **Pattern membership** — correctly assigned to Pattern A/B/C? Wrong/missing assignment?
4. **Multi-aspect manifestation** — single↔bipartite↔tri-aspect tagged correctly?
5. **Axis attribution** — cross-axis with primary anchor noted where applicable, or genuinely cross-axis with no anchor?

Distinct from Lens 1 because a primitive can be the right primitive (no set-composition change) but mistagged. Both can fire on the same entry.

### Lens 3: Vocabulary coherence + naming collisions

Cross-entry vocabulary check.

- Same term used consistently across entries? (e.g., does "instance" mean the same thing in entry A and entry B?)
- Naming collisions: same word with two distinct meanings? (e.g., `skill` the work-logic primitive vs `actor_kind: skill` enum value — collision)
- Disambiguation explicit where needed? (e.g., `protocol (architectural)` vs `Pydantic Protocol`)
- Casual usage of locked terms in colloquial sense (e.g., "behavioral protocol" when locked vocabulary reserves protocol for Pattern A architectural primitives)

### Lens 4: Cross-reference cascade health

Mechanical check.

- Run `git grep "<locked-term> .*forthcoming"` for every locked term — find stale "(forthcoming)" markers referring to now-locked terms (cascade-pass discipline failure)
- Verify "See" / "Composes with" cross-refs resolve (cited entry exists)
- Verify Source citations resolve (cited file:line exists; line numbers correct)
- Per `MAINTENANCE.md` cascade discipline: every reference to a now-changed term should have been updated when the change locked

### Lens 5: Mechanical compliance (tags + sources + provenance hygiene)

Schema + discipline check across entries (was Lens 4 + Lens 6 in v0.1.0; merged because both are checklist-driven mechanical checks rather than architectural sparring).

- Class tags drawn from declared enumeration; no ad-hoc values
- Layer / Axis / VISION-usage tags consistent
- Boundary-test format roughly parallel where applicable (don't force standardization that costs more than it saves)
- Source sections cite file:line where claims have file:line basis (per `DISCIPLINES.md` Discipline 1)
- Synthesis flagged distinctly from citation
- "Pattern-matched / inferred" basis flagged at low confidence
- **Provenance hygiene** (v0.2.1): entries should NOT contain audit/revision history breadcrumbs ("per RA4 Round 3 audit", "per A1 — primitive-set lens, applied session 16", "per Phase 1.75 + feedback_X resolution"). Provenance lives in HANDOFF.md notes + git log + commit messages. Discriminator:
  - **Strip**: audit-revision-history markers ("per <audit-name>", "applied session N", "Round N audit"). These pollute canonical-definition prose.
  - **Keep**: load-bearing forward-references / discipline notes ("deferred to Phase 3 ARCH", "deliberately NOT 'X' — X is locked vocabulary for Y", "Phase 6 reconciles..."). These are SEMANTIC context future readers need.
  - The test: would removing this breadcrumb confuse a fresh reader's understanding of WHAT THE PRIMITIVE IS? If no, strip; if yes, keep.

### Lens 6: Symmetry

Composes-with reciprocity (promoted from Lens 1 sub-q in v0.1.0 because it's a distinct fault mode from set-composition).

- For each Composes-with claim of form "A composes with B because <reason>": is the reciprocal listed in B's Composes-with?
- Asymmetric is fine when genuinely one-way (e.g., specialist contains skill; skill doesn't contain specialist). Asymmetric is a bug when load-bearing reciprocal is missing (e.g., skill ↔ adapter where skills CALL adapters and adapter is CALLED BY skills — both directions load-bearing).

### Lens 7: Definition contradictions

Internal + cross-entry.

- Within-entry: does Canonical contradict What-it-is-NOT? (e.g., Canonical says "natural-or-legal-person" but What-it-is-NOT says "always natural person")
- Cross-entry: does Entry A's claim about Entry B match Entry B's self-description?
- Compositional contradictions: does A claim it composes with B in some way that B's self-description denies?

### Lens 8: Pattern-vs-instance discipline (LOAD-BEARING)

Directly catches the failure mode that triggered the session-16 PBS rebuild: **instance-anchoring leakage**.

For each primitive, ask:
- Is this primitive smuggling instance-specific assumptions into the pattern layer?
- Examples of past leakage (session-16 findings):
  - Practitioner assumed = solo human (instance assumption from PBS-Schulz pioneer; pattern level should be natural-person, kind-variation at workspace level)
  - EU/DACH framing baked into substrate level (pioneer-jurisdiction; pattern level should be jurisdiction-neutral)
  - `project` enum tied to planning-domain (pioneer-domain; pattern level should be specialist-defined work-unit kind)
  - Art-25 naming inheriting EU regulatory specifics into framework (pioneer-regulatory-context)

**Test for leakage**: would this primitive work for a hypothetical legal-practice / research-paper-review / engineering-doc workspace? Or does the definition embed pioneer-instance specifics (PBS-Schulz, planning bureau, German Begründungen)?

**Composes with**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (the no-defer principle protecting framework purity).

**Why this is a separate lens** (not just within Lens 1): merge/split/add/remove operations don't catch this — a primitive can be the right primitive (no merge needed) but its DEFINITION leaks instance-specifics. Different fault mode.

### Lens 9: VISION-grounding (LOAD-BEARING)

Every locked primitive should trace to VISION — either directly (VISION usage: directly used) or derived (composes with VISION-grounded terms).

For each primitive, test:
- Can you state which VISION axis or framing this primitive supports?
- If derived, what's the chain back to a VISION-grounded primitive?
- Any primitive that surfaces in conversation, gets locked, but has no VISION grounding? Flag as speculation territory — either lift the framing into VISION (if it's load-bearing) or reconsider whether the primitive belongs.

**Why this is a separate lens**: counter-mechanism to scope-creep — primitives can accumulate organically over conversations without each one's VISION grounding being explicit. Periodic VISION-grounding check ensures the primitive set stays anchored to the thesis VISION articulates rather than drifting.

**Composes with**: VISION's preliminary-lock principle (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3); only VISION axes are anchored — every other primitive is preliminary AND should be VISION-grounded.

### Lens 10: Cardinality + lifecycle

Each primitive has implicit cardinality and lifecycle semantics; this lens makes them explicit.

**Cardinality questions**:
- How many instances per workspace? (e.g., substrate=1, adapter=N, specialist=N active, practitioner=1+ depending on shape, workflow=?, work-unit=N per active workflow)
- Singleton vs unbounded vs bounded-by-policy?
- Is cardinality stated explicitly somewhere in the entry, or only implicit?

**Lifecycle questions**:
- When does instance start? End?
- Mutability: append-only (events) / replaceable (workspace.md selections) / mutable-with-audit (specialist instance content) / immutable (Framework C definitions)?
- Lifecycle ownership: who creates / who destroys?
- Cross-session persistence: persists across sessions / scoped to session / session-internal-only?

**Why this lens earns its place**: cardinality + lifecycle ambiguity is the kind of question that surfaces in implementation but should be settled at architectural level. Currently scattered across What-it-is + Composes-with prose; explicit lens detects gaps.

**Anti-pattern check**: if cardinality is stated only as "typically N" or "usually one," that's ambiguity; sharpen to mechanism-defined-cardinality (workspace.md field selects? shape policy mandates? unbounded by-design?).

## Procedure

### Step 1: Run all 10 lenses sequentially

Don't batch. Don't skip. **Especially don't skip Lens 1, Lens 8, Lens 9** (load-bearing). Self-validation bias defaults to Lens 5 (mechanical compliance — feels productive without questioning structure) or Lens 7 (definition contradictions — within-entry feel) and skips the load-bearing ones (which require actually questioning the existing primitive set / catching instance-leakage / verifying VISION-grounding).

For each lens, surface findings in two categories:

| Category | Definition | Pareto verdict |
|---|---|---|
| **REVISIONS** (~30%) | Genuine architectural changes (merge / split / redefine / boundary fix / contradiction resolution / vocabulary clash) | Each surfaced revision: what's gained vs what's lost? Pareto-improving or genuine tradeoff? |
| **EXPANSIONS** (~70%) | Coverage additions (missing citations, missing What-it-is-NOT, refined boundary test) | Pareto-improving by nature |

### Step 2: Apply Pareto discipline per finding

Each surfaced finding: is it Pareto-improving? If not, force the "why?" challenge — could be manufactured criticism. Reject manufactured criticism.

### Step 3: Distinguish corpus-level from per-entry findings

Corpus-level (changes affecting multiple entries OR architectural commitments): Lens 1 (set composition), Lens 3 (vocabulary), Lens 4 (cascade health), Lens 6 (symmetry), Lens 8 (pattern-vs-instance), Lens 9 (VISION-grounding), Lens 10 (cardinality + lifecycle).

Per-entry (changes within a single entry): Lens 2 (tag corrections), Lens 5 (mechanical compliance), Lens 7 (definition contradictions).

Corpus-level findings cascade — locking one revision propagates to multiple entries. Per-entry findings are local.

### Step 4: Position findings as committed recommendations

Per `feedback_judgment_and_automate.md`: don't menu the findings; commit a position per finding. User adjusts/challenges/confirms.

**Auto-add to BACKLOG.md** (v0.2.2): when audit surfaces items that aren't actionable in current scope (e.g., "Phase 3 ARCH resolves..." forward-references; deferred details; Lens 11-15 corpus-specific findings during Phase 2 GLOSSARY audit), add corresponding entries to `BACKLOG.md` under the relevant phase section in same commit as the audit application. BACKLOG is the central work-item tracker; coherence-audit's deferrals must surface there or risk getting lost.

**Post-audit self-check (v0.3.3 update)**: at end of audit, comprehensive termination criteria per `plugin/skills/sharpen/SKILL.md` v0.11.0 — Layer 1 empirical signals + Layer 2 counter-bias mechanisms + Layer 3 verdict logic + Layer 4 mandatory output. Single-metric verdicts insufficient; surface-coverage is multi-signal.

**Surface-type declaration**: coherence-audit = SET-LEVEL AUDIT. Density profile: per-cluster (audit may yield findings across many rounds without decay UNTIL specific cluster exhausted). Pattern-matching architectural-decision decay (6→5→3→0-1) onto SET-LEVEL surface = recurrent bias.

**Empirical density check**: count substantive findings (HIGH + MEDIUM; exclude cosmetic / NO-ACTION) current audit-pass vs previous. ≥50% drop = decay confirmed; within ±25% = decay NOT confirmed.

**Lens-coverage check** (specific to SET-LEVEL AUDIT): even if density drops, verify ALL 10 universal lenses applied (Lens 1+8+9 LOAD-BEARING required). Per cluster: verify lens applied per-cluster, not just corpus-wide. Lens-coverage incomplete → CONTINUE regardless of density.

**Honest termination test (Q1-Q5)**:
- Q1: Current pass substantive count?
- Q2: Previous pass substantive count?
- Q3: Density change (%)?
- Q4: If CONTINUE: which specific lens surfaced load-bearing gaps? OR new architectural decisions locked since last audit warrant another pass? OR specific cluster not yet audited?
- Q5: If STABLE: can I name specific termination signal? (e.g., "Lens 1+8+9 collective REVISION count = 0 AND density decay confirmed AND all clusters audited")

**Verdict criteria**:
- STABLE: density decay confirmed AND Lens 1+8+9 REVISIONs = 0 AND all clusters covered AND Q5 cites specific signal
- CONTINUE: density holds OR Lens-coverage incomplete OR Q4 names specific gap OR user explicit signal

Manufactured-criticism counter-test + manufactured-comfort counter-test BOTH applied (per `sharpen` v0.10.0). Pattern-matching expected decay onto SET-LEVEL audit surface = manufactured comfort.

### Step 5: Apply revisions in cascade-aware order

Per `MAINTENANCE.md` cascade discipline: when locking a corpus-level revision, identify all affected entries and update in same commit (or tightly-coupled sequence explicitly marked as completing the cascade).

**Provenance discipline when applying revisions** (v0.2.1): when applying a finding's revision to an entry, do NOT embed audit-revision-history breadcrumbs in the entry text. Provenance goes in:
- **HANDOFF.md note** for the audit run (records what was changed + why)
- **Commit message** (records exact diff + rationale)
- **git log** (full history)

The entry stays canonical: definition prose without "per RA4 Round 3 audit" / "per A1 — primitive-set lens, applied session 16" markers. Fresh readers see the locked definition; readers wanting provenance check HANDOFF + git log.

Anti-pattern caught by Lens 5 provenance-hygiene check: AI applying a revision feels productive when it adds an "applied session X" marker (signals work-was-done). But that marker pollutes the canonical layer. Resist the urge.

**Exception**: load-bearing forward-references / discipline notes ("deferred to Phase 3 ARCH", "deliberately NOT 'X'") stay because they're SEMANTIC context, not provenance.

### Step 6: Output

| Output | Form |
|---|---|
| Lens-by-lens findings list | In chat, before commit |
| Position per finding | Committed recommendation, not menu |
| Cascade-aware revision order | Sequence stated before applying |
| Diff per entry touched | Single commit (or coupled-sequence) per cascade |

### Step 7 (v0.3.1): REVISION/EXPANSION classification self-check

Detection mechanism for awaited 3-tier discriminator codification (per BACKLOG watch-list "3-tier discriminator codification"). At audit completion, before locking findings, ask explicitly:

> Any finding classified as EXPANSION that on second look would reclassify as REVISION? Any EXPANSION whose cascade-implications feel REVISION-flavored — load-bearing reciprocal asymmetry / structural elevation of implicit-to-explicit / glossary-grade distinction?

If yes repeatedly across audits → signal that 2-tier (REVISION/EXPANSION) is producing under-precision; revisit per BACKLOG watch-list. If consistently no → 2-tier holds; signal hasn't materialized; defer codification.

Empirical signal threshold: ≥3 borderline classifications across consecutive audits OR user pushback that classifications feel under-precise OR cascade-work-lag (Lens-6-style reciprocal gaps caught at audit-time that should have been caught at sharpening-time).

## Termination signals

| Signal | Action |
|---|---|
| User says "lock" / "apply" / "looks good" | Apply revisions in cascade-aware order |
| Lens 1 + 8 + 9 collectively yield zero REVISIONS after honest run | Strong signal corpus is set-coherent OR you're skipping load-bearing lenses. Force re-run with explicit prompts. |
| Lens 5 or Lens 7 yields most of the findings | Self-validation bias triggered; you defaulted to mechanical compliance / within-entry contradictions. Re-run load-bearing lenses (1, 8, 9) explicitly. |
| Lens 8 catches instance-leakage on locked primitive | High-priority cascade — affects framework purity per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2. Lock immediately. |
| Lens 9 surfaces ungrounded primitive | Either lift framing into VISION (if load-bearing) OR reconsider whether primitive belongs. Don't leave ungrounded. |
| Lens 10 surfaces cardinality ambiguity | Sharpen the entry's cardinality statement; "typically N" is a smell — name the mechanism that determines N. |
| Found findings are all Pareto-fail | Manufactured criticism territory; lock corpus as-is |
| Round 2 of audit yields nothing new | Audit complete |

## Audit scaling strategies (v0.3.0 — when to use which)

Audit cost grows multiplicatively with profile count × entry count. Pure systematic audit at every invocation is unsustainable as corpus grows. Combination approach scales sustainably.

| Strategy | Cost | Rigor | When to use |
|---|---|---|---|
| **Cluster compression** | Low | Medium (cluster-level coverage; risks within-cluster gaps) | Routine periodic health-checks. Group profiles into 4-7 clusters by shared concerns; audit per-cluster against entries; spot-check intra-cluster variation. |
| **Audit deltas** | Very low | High (for affected scope) | Incremental work where baseline audit exists. Re-audit only profiles + entries affected by recent decision; assume rest unchanged. |
| **On-demand fleshing** | Medium | High (within affected scope) | High-impact specific decisions. Flesh out skeleton profiles for primitives the decision touches; full systematic within fleshed scope; skeleton-level for others. |
| **Sampling representative profiles** | Low-Medium | Medium-High (depends on rep selection) | Quick corpus-health-check. Pick 1-2 representatives per cluster covering shared concerns; audit fully against representatives; assume cluster-coverage. |
| **Full systematic** (every profile × every entry) | High | Maximum | Phase boundary audits + introducing new discipline corpus-wide. Reserve for these high-stakes moments; not default. |

**Combination approach** (recommended for ongoing work):
- Cluster compression for routine periodic health-checks
- Audit deltas for incremental decisions (most common)
- On-demand fleshing for high-impact decisions
- Full systematic ONLY at phase boundaries or new-discipline introductions

**Anti-pattern**: defaulting to full systematic for every audit invocation. Becomes expensive AND introduces self-validation bias (large effort → seeking findings to justify effort). Match audit-strategy to audit-context.

**Cluster split when needed**: if cluster-internal heterogeneity becomes load-bearing for a specific decision (e.g., L1 specialist creator vs L3 template composer concerns diverge sharply), split the cluster temporarily. Don't pre-split; pre-split adds cost without proportional benefit.

## Corpus-kind awareness (lens activation per target)

Coherence-audit operates on different corpus kinds. The 10 universal lenses apply to any corpus; corpus-kind-specific lenses activate when target matches.

| Corpus kind | Universal lenses | Corpus-specific lenses (additional) |
|---|---|---|
| **GLOSSARY** (Layer 1) | 1-10 (Lens 2 tag-correction sub-questions tuned for entry-tag schema) | — |
| **ARCH** (Layer 3) | 1-10 (Lens 2 sub-questions adjust to ARCH topic schema; Lens 8 elevated to MOST critical because richer detail = more leakage surface) | Lenses 11-15 below |
| **DR-set** (Layer 4) | 1-10 (Lens 2 sub-questions adjust to DR structure) | Lens 16: decision-linkage / constraint-flow tracking |
| **Spec-set** (Layer 5) | 1-10 (Lens 2 sub-questions adjust to spec schema) | Lens 17: schema completeness; Lens 18: spec/impl divergence (Phase 6+) |

### ARCH-specific lenses (11-15) — Phase 3+

**Lens 11: Inter-layer consistency**
ARCH topics cite GLOSSARY entries (Layer 1) + DRs (Layer 4) + specs (Layer 5). Verify:
- Cited GLOSSARY terms are locked (not forthcoming)
- Cited DRs exist + are at the cited section
- Cited specs exist + are at the cited section
- ARCH usage of GLOSSARY terms matches their canonical definitions

**Lens 12: Specs traceability**
For each ARCH topic with implementation contract:
- Is there a corresponding spec? (file in `docs/specs/`)
- If no, is "no spec needed" explicit? (vs. accidentally missing)
- If yes, does the spec match the ARCH topic's claimed contract?

**Lens 13: Architectural protocol completeness**
For each Pattern A primitive locked in GLOSSARY (substrate, adapter, named architectural Protocols):
- Does it have per-protocol detail in ARCH Layer 3? (Surface specification, per-impl detail, selection mechanics)
- If deferred, is the deferral explicit?
- Coverage gaps = either missing ARCH topic OR missing explicit deferral

**Lens 14: DR coverage gap**
Every architectural commitment should either:
- Live in ARCH proper (Layer 3 topical) OR
- Have an explanatory DR (Layer 4 single-decision capture)

Walk every locked architectural commitment in MAINTENANCE.md / DISCIPLINES.md / GLOSSARY entries / ARCH topics. Verify each has DR coverage OR is self-contained in ARCH/MAINTENANCE/DISCIPLINES.

**Lens 15: Granularity match**
Per MAINTENANCE.md budget: ARCH topics ~500 lines each, 15-20 topics total.
- Topic significantly over budget (1000+ lines) → decomposition signal (split into sub-topics)
- Topic significantly under budget (<100 lines) → merge signal (combine with adjacent topic OR remove if redundant)
- Inconsistent budgets across topics → schema drift signal

### DR-set-specific lens (16) — Phase 4+

**Lens 16: Decision-linkage / constraint-flow tracking**
For DR-set audits:
- Does each DR's "Composition with existing architecture" cleanly identify which other DRs it depends on / extends / amends?
- Do "Constraints flowing" sections form a closed graph (every constraint flow has both source DR + target consumer)?
- Are there orphan DRs (cited nowhere, no constraints flowing in or out)?

### Spec-set-specific lenses (17-18) — Phase 6+

**Lens 17: Schema completeness**
- Each Pydantic model / schema fully specified (all fields documented; types declared; validation rules declared)
- Cross-spec schema references resolve

**Lens 18: Spec/impl divergence**
- Implemented code matches spec
- Spec amendments trigger code amendments (or vice versa, with audit trail)

## Composition with other skills

| Skill | Composition |
|---|---|
| `decision-design-sharpening` | Operates UPSTREAM (per-decision pre-commit); coherence-audit operates DOWNSTREAM (post-multi-commit) |
| `pre-implementation-sharpening` | Different timing entirely (implementation-start); coherence-audit can run any time multiple decisions are locked |
| Cascade discipline (MAINTENANCE.md) | Coherence-audit USES cascade discipline (Lens 4 mechanical check) |

## Self-validation bias warning (specific to this skill)

This skill is unusually vulnerable to self-validation bias because:

1. The corpus exists; the AI proposed many of the entries; defending one's own proposals is the default
2. Lens 5 (mechanical compliance) feels productive AND validates the existing structure (no merging / splitting / redefining → no architectural anxiety)
3. Lens 1 (set composition) + Lens 8 (pattern-vs-instance) require admitting "an existing primitive might be wrong" — uncomfortable

**Counter-mechanism**: every coherence-audit run MUST produce a Lens 1 + Lens 8 + Lens 9 collective finding count. If the count is zero, treat as suspicious — either the corpus is genuinely set-coherent (rare for early-stage corpora) OR the load-bearing lenses weren't actually run.

**User-trigger advantage**: per `DISCIPLINES.md` Discipline 3, user-triggered passes outperform AI-self-triggered. Coherence-audit IS user-triggered by definition (the skill fires on user signal, not AI auto-run). Counter-bias is partially built-in.

## Concrete invocation example

```
1. User signals: "audit the glossary" / "are these the right primitives?"

2. Skill activates; AI runs all 10 lenses sequentially
   → "Running Lens 1 (set composition)... Surfacing 2 REVISIONS:
      R1: REMOVE AI runtime entry (STUB-only; redundant)
      R2: ADD work-unit primitive (missing canonical home)"
   → "Running Lens 2 (tag corrections)... ..."
   → "Running Lens 3 (vocabulary coherence + collisions)... ..."
   → ... (continues through all 10 lenses)

3. AI presents committed-position findings list
   → categorized REVISIONS vs EXPANSIONS
   → Pareto verdict per finding
   → Cascade-aware revision order

4. User accepts / adjusts / challenges per finding

5. AI applies in cascade-aware sequence; commits with cascade-pass evidence

6. Output: corpus-set-level revisions applied; per-entry refinements applied
```

## Audit-trail integration (optional)

If deployment has audit-trail infrastructure, each coherence-audit can emit:
- `event_kind=coherence_audit_started` with `corpus_kind` (glossary / dr-set / spec-set) + `entries_in_scope` count
- `event_kind=coherence_audit_finding_surfaced` per finding with `lens_kind` (1-10 universal; 11-18 corpus-specific) + `category` (REVISION/EXPANSION) + `pareto_verdict`
- `event_kind=coherence_audit_completed` with totals

Composes with audit-trail-as-canonical-source pattern.
