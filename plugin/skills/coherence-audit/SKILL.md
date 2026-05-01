---
name: coherence-audit
description: Use when multiple architectural decisions / GLOSSARY entries / DRs / specs have already been locked and the user wants a CROSS-DECISION audit pass on the corpus as a SET — not within-decision sharpening. Triggers via natural-language prompts including "audit the glossary", "review the corpus", "cross-entry audit", "is the architecture clean", "are these the right primitives", "primitive-set audit", "set-level review", "coherence check", "is the vocabulary coherent". Phase 3 of the dev-skill family — distinct from `decision-design-sharpening` (pre-decision; one decision; pre-commit) and `pre-implementation-sharpening` (one decision; at implementation-start). NOT for within-entry refinement on a single decision (use decision-design-sharpening). NOT for operational-detail surfacing on one decision (use pre-implementation-sharpening).
when_to_use: After multiple decisions / GLOSSARY entries / DRs are locked; user wants a SET-level audit. Natural triggers: "audit glossary", "review corpus", "cross-entry audit", "are these the right primitives", "primitive-set audit", "is the architecture clean", "coherence check". Do NOT use for single-decision sharpening — that's decision-design-sharpening.
version: 0.1.0
---

# Coherence audit (Phase 3 dev skill)

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

## The 9 lenses

Run each lens explicitly. **Lens 1 (primitive-set redesign) + Lens 8 (pattern-vs-instance) + Lens 9 (VISION-grounding) are the load-bearing ones** — they're what per-decision sharpening structurally cannot see and what self-validation bias suppresses without explicit prompting.

### Lens 1: Primitive-set redesign (LOAD-BEARING)

The most important lens. Per-decision sharpening locks individual primitives; this lens asks whether the SET is right.

**11 questions** (expand Lens 1 — early version had only 6):

**Set composition (which primitives exist)**:
1. **MERGE** — should any primitives combine into one? (Two cover overlapping ground; one is a refinement of the other)
2. **SPLIT** — should any primitive split into two? (One primitive doing two jobs; clearer separated)
3. **ADD** — any missing primitives? (Concept load-bearing across multiple entries with no canonical home)
4. **REMOVE** — any redundant primitives? (Exists only as cross-ref; no independent semantic content)
5. **REDEFINE BOUNDARIES** — primitive A's What-it-is-NOT vs primitive B's What-it-is cleanly partition conceptual space? Or overlap / leave gaps?

**Tag corrections (how primitives are classified)**:
6. **Class re-classification** — should the Class tag change? PRIMITIVE↔META-PRIMITIVE↔DERIVED↔SCOPE-CLASSIFICATION↔STUB
7. **Layer re-classification** — should the Layer tag change? cross-cutting↔multi-aspect↔framework-mechanism↔shape-policy↔framework-meta
8. **Pattern membership** — correctly assigned to Pattern A/B/C? Wrong assignment? Missing assignment that should be added?
9. **Multi-aspect manifestation** — single↔bipartite↔tri-aspect tagged correctly?
10. **Axis attribution** — cross-axis with primary anchor noted where applicable, or genuinely cross-axis with no anchor?

**Cross-entry shape**:
11. **Symmetry** — composes-with relationships symmetric where they should be (A composes with B AND B composes with A); asymmetric where genuine

This lens runs AGAINST the corpus, not against any single entry. Surfacing requires reading multiple entries together, not just one.

**Anti-pattern**: surfacing only within-entry refinements when running this lens. If the lens produces zero structural findings (questions 1-11), ask: "did I actually run this lens, or did I default to within-entry sharpening?" — self-validation bias triggers default.

### Lens 2: Vocabulary coherence + naming collisions

Cross-entry vocabulary check.

- Same term used consistently across entries? (e.g., does "instance" mean the same thing in entry A and entry B?)
- Naming collisions: same word with two distinct meanings? (e.g., `skill` the work-logic primitive vs `actor_kind: skill` enum value — collision)
- Disambiguation explicit where needed? (e.g., `protocol (architectural)` vs `Pydantic Protocol`)
- Casual usage of locked terms in colloquial sense (e.g., "behavioral protocol" when locked vocabulary reserves protocol for Pattern A architectural primitives)

### Lens 3: Cross-reference cascade health

Mechanical check.

- Run `git grep "<locked-term> .*forthcoming"` for every locked term — find stale "(forthcoming)" markers referring to now-locked terms (cascade-pass discipline failure)
- Verify "See" / "Composes with" cross-refs resolve (cited entry exists)
- Verify Source citations resolve (cited file:line exists; line numbers correct)
- Per `MAINTENANCE.md` cascade discipline: every reference to a now-changed term should have been updated when the change locked

### Lens 4: Tag consistency

Schema check across entries.

- Class tags drawn from declared enumeration; no ad-hoc values
- Layer tags consistent
- Axis tags consistent (cross-axis vs single-axis; primary-anchor noted where applicable)
- VISION-usage tags consistent
- Boundary-test format roughly parallel where applicable (don't force standardization that costs more than it saves)

### Lens 5: Definition contradictions

Internal + cross-entry.

- Within-entry: does Canonical contradict What-it-is-NOT? (e.g., Canonical says "natural-or-legal-person" but What-it-is-NOT says "always natural person")
- Cross-entry: does Entry A's claim about Entry B match Entry B's self-description?
- Compositional contradictions: does A compose with B per A, but B doesn't list A in its composes-with?

### Lens 6: Source-grounded discipline compliance

Per `feedback_source_grounded.md`.

- Source sections cite file:line where claims have file:line basis
- Synthesis flagged distinctly from citation
- "Pattern-matched / inferred" basis flagged at low confidence
- Calibrate: which entries lean on synthesis where citation should be possible?

### Lens 7: Within-entry sharpening (overlap with decision-design-sharpening)

Catches what per-decision sharpening missed:

- Definition tightness — Canonical statement unambiguous?
- What-it-is-NOT sharply distinguishes from neighbors
- Boundary tests mechanical (yields a clear answer, not "it depends")
- Examples illustrate cross-archetype range (not just pioneer instance)

**Note**: this lens overlaps decision-design-sharpening. Mostly redundant if pre-decision sharpening was rigorous. Run lightly here; flag only obvious cases.

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

**Composes with**: `feedback_pattern_not_instance_defers.md` (the no-defer principle protecting framework purity).

**Why this is a separate lens** (not just within Lens 1): merge/split/add/remove operations don't catch this — a primitive can be the right primitive (no merge needed) but its DEFINITION leaks instance-specifics. Different fault mode.

### Lens 9: VISION-grounding

Every locked primitive should trace to VISION — either directly (VISION usage: directly used) or derived (composes with VISION-grounded terms).

For each primitive, test:
- Can you state which VISION axis or framing this primitive supports?
- If derived, what's the chain back to a VISION-grounded primitive?
- Any primitive that surfaces in conversation, gets locked, but has no VISION grounding? Flag as speculation territory — either lift the framing into VISION (if it's load-bearing) or reconsider whether the primitive belongs.

**Why this is a separate lens**: counter-mechanism to scope-creep — primitives can accumulate organically over conversations without each one's VISION grounding being explicit. Periodic VISION-grounding check ensures the primitive set stays anchored to the thesis VISION articulates rather than drifting.

**Composes with**: VISION's preliminary-lock principle (per `feedback_preliminary_lock.md`); only VISION axes are anchored — every other primitive is preliminary AND should be VISION-grounded.

## Procedure

### Step 1: Run all 9 lenses sequentially

Don't batch. Don't skip. **Especially don't skip Lens 1, Lens 8, Lens 9** (load-bearing). Self-validation bias defaults to Lens 7 (which feels productive — surfaces refinements without questioning structure) and skips the load-bearing ones (which require actually questioning the existing primitive set / catching instance-leakage / verifying VISION-grounding).

For each lens, surface findings in two categories:

| Category | Definition | Pareto verdict |
|---|---|---|
| **REVISIONS** (~30%) | Genuine architectural changes (merge / split / redefine / boundary fix / contradiction resolution / vocabulary clash) | Each surfaced revision: what's gained vs what's lost? Pareto-improving or genuine tradeoff? |
| **EXPANSIONS** (~70%) | Coverage additions (missing citations, missing What-it-is-NOT, refined boundary test) | Pareto-improving by nature |

### Step 2: Apply Pareto discipline per finding

Each surfaced finding: is it Pareto-improving? If not, force the "why?" challenge — could be manufactured criticism. Reject manufactured criticism.

### Step 3: Distinguish corpus-level from per-entry findings

Lens 1 + Lens 2 + Lens 3 + Lens 5 + Lens 8 + Lens 9 produce **corpus-level findings** (changes affecting multiple entries OR architectural commitments). Lens 4 + Lens 6 + Lens 7 produce **per-entry findings** (changes within a single entry).

Corpus-level findings cascade — locking one revision propagates to multiple entries. Per-entry findings are local.

### Step 4: Position findings as committed recommendations

Per `feedback_judgment_and_automate.md`: don't menu the findings; commit a position per finding. User adjusts/challenges/confirms.

### Step 5: Apply revisions in cascade-aware order

Per `MAINTENANCE.md` cascade discipline: when locking a corpus-level revision, identify all affected entries and update in same commit (or tightly-coupled sequence explicitly marked as completing the cascade).

### Step 6: Output

| Output | Form |
|---|---|
| Lens-by-lens findings list | In chat, before commit |
| Position per finding | Committed recommendation, not menu |
| Cascade-aware revision order | Sequence stated before applying |
| Diff per entry touched | Single commit (or coupled-sequence) per cascade |

## Termination signals

| Signal | Action |
|---|---|
| User says "lock" / "apply" / "looks good" | Apply revisions in cascade-aware order |
| Lens 1 + 8 + 9 collectively yield zero REVISIONS after honest run | Strong signal corpus is set-coherent OR you're skipping load-bearing lenses. Force re-run with explicit prompts. |
| Lens 7 yields most of the findings | Self-validation bias triggered; you defaulted to within-entry sharpening. Re-run load-bearing lenses (1, 8, 9) explicitly. |
| Lens 8 catches instance-leakage on locked primitive | High-priority cascade — affects framework purity per `feedback_pattern_not_instance_defers.md`. Lock immediately. |
| Lens 9 surfaces ungrounded primitive | Either lift framing into VISION (if load-bearing) OR reconsider whether primitive belongs. Don't leave ungrounded. |
| Found findings are all Pareto-fail | Manufactured criticism territory; lock corpus as-is |
| Round 2 of audit yields nothing new | Audit complete |

## Corpus-kind awareness (lens activation per target)

Coherence-audit operates on different corpus kinds. The 9 universal lenses apply to any corpus; corpus-kind-specific lenses activate when target matches.

| Corpus kind | Universal lenses | Corpus-specific lenses (additional) |
|---|---|---|
| **GLOSSARY** (Layer 1) | 1-9 (with full tag-classification sub-questions in Lens 1) | — |
| **ARCH** (Layer 3) | 1-9 (Lens 1 sub-questions about tags adjust to ARCH topic schema; Lens 8 elevated to MOST critical because richer detail = more leakage surface) | Lenses 10-14 below |
| **DR-set** (Layer 4) | 1-9 (Lens 1 sub-questions adjust to DR structure) | Lens 15: decision-linkage / constraint-flow tracking |
| **Spec-set** (Layer 5) | 1-9 (Lens 1 sub-questions adjust to spec schema) | Lens 16: schema completeness; Lens 17: spec/impl divergence (Phase 6+) |

### ARCH-specific lenses (10-14) — Phase 3+

**Lens 10: Inter-layer consistency**
ARCH topics cite GLOSSARY entries (Layer 1) + DRs (Layer 4) + specs (Layer 5). Verify:
- Cited GLOSSARY terms are locked (not forthcoming)
- Cited DRs exist + are at the cited section
- Cited specs exist + are at the cited section
- ARCH usage of GLOSSARY terms matches their canonical definitions

**Lens 11: Specs traceability**
For each ARCH topic with implementation contract:
- Is there a corresponding spec? (file in `docs/specs/`)
- If no, is "no spec needed" explicit? (vs. accidentally missing)
- If yes, does the spec match the ARCH topic's claimed contract?

**Lens 12: Architectural protocol completeness**
For each Pattern A primitive locked in GLOSSARY (substrate, adapter, named architectural Protocols):
- Does it have per-protocol detail in ARCH Layer 3? (Surface specification, per-impl detail, selection mechanics)
- If deferred, is the deferral explicit?
- Coverage gaps = either missing ARCH topic OR missing explicit deferral

**Lens 13: DR coverage gap**
Every architectural commitment should either:
- Live in ARCH proper (Layer 3 topical) OR
- Have an explanatory DR (Layer 4 single-decision capture)

Walk every locked architectural commitment in MAINTENANCE.md / DISCIPLINES.md / GLOSSARY entries / ARCH topics. Verify each has DR coverage OR is self-contained in ARCH/MAINTENANCE/DISCIPLINES.

**Lens 14: Granularity match**
Per MAINTENANCE.md budget: ARCH topics ~500 lines each, 15-20 topics total.
- Topic significantly over budget (1000+ lines) → decomposition signal (split into sub-topics)
- Topic significantly under budget (<100 lines) → merge signal (combine with adjacent topic OR remove if redundant)
- Inconsistent budgets across topics → schema drift signal

### DR-set-specific lens (15) — Phase 4+

**Lens 15: Decision-linkage / constraint-flow tracking**
For DR-set audits:
- Does each DR's "Composition with existing architecture" cleanly identify which other DRs it depends on / extends / amends?
- Do "Constraints flowing" sections form a closed graph (every constraint flow has both source DR + target consumer)?
- Are there orphan DRs (cited nowhere, no constraints flowing in or out)?

### Spec-set-specific lenses (16-17) — Phase 6+

**Lens 16: Schema completeness**
- Each Pydantic model / schema fully specified (all fields documented; types declared; validation rules declared)
- Cross-spec schema references resolve

**Lens 17: Spec/impl divergence**
- Implemented code matches spec
- Spec amendments trigger code amendments (or vice versa, with audit trail)

## Composition with other skills

| Skill | Composition |
|---|---|
| `decision-design-sharpening` | Operates UPSTREAM (per-decision pre-commit); coherence-audit operates DOWNSTREAM (post-multi-commit) |
| `pre-implementation-sharpening` | Different timing entirely (implementation-start); coherence-audit can run any time multiple decisions are locked |
| Cascade discipline (MAINTENANCE.md) | Coherence-audit USES cascade discipline (Lens 3 mechanical check) |

## Self-validation bias warning (specific to this skill)

This skill is unusually vulnerable to self-validation bias because:

1. The corpus exists; the AI proposed many of the entries; defending one's own proposals is the default
2. Lens 7 (within-entry sharpening) feels productive AND validates the existing structure (no merging / splitting / redefining → no architectural anxiety)
3. Lens 1 (primitive-set redesign) requires admitting "an existing primitive might be wrong" — uncomfortable

**Counter-mechanism**: every coherence-audit run MUST produce a Lens 1 finding count. If Lens 1 count is zero, treat as suspicious — either the corpus is genuinely set-coherent (rare for early-stage corpora) OR Lens 1 wasn't actually run.

**User-trigger advantage**: per `feedback_pre_decision_sharpening.md`, user-triggered passes outperform AI-self-triggered. Coherence-audit IS user-triggered by definition (the skill fires on user signal, not AI auto-run). Counter-bias is partially built-in.

## Concrete invocation example

```
1. User signals: "audit the glossary" / "are these the right primitives?"

2. Skill activates; AI runs all 7 lenses sequentially
   → "Running Lens 1 (primitive-set redesign)... Surfacing 3 REVISIONS:
      A1: Specific mechanisms should defer to ARCH Layer 3 (12 entries affected)
      A2: actor_kind: skill enum value collides with skill primitive (rename)
      A3: workflow should be multi-aspect Pattern B (re-tag)"
   → "Running Lens 2 (vocabulary coherence)... Surfacing 1 finding..."
   → ... (continues through all 7 lenses)

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
- `event_kind=coherence_audit_finding_surfaced` per finding with `lens_kind` (1-7) + `category` (REVISION/EXPANSION) + `pareto_verdict`
- `event_kind=coherence_audit_completed` with totals

Composes with audit-trail-as-canonical-source pattern.
