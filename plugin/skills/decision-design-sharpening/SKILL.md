---
name: decision-design-sharpening
description: "**READ THIS FILE BEFORE APPLYING. Use the Read tool to load this SKILL.md at every invocation, regardless of prior usage in same session — pattern-matching from memory of prior usage FAILS load-bearing discipline elements (per `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)).** Use when an architectural decision needs disciplined sharpening BEFORE commit to file (decision record, architecture doc, vision/strategy doc, roadmap, or other load-bearing artifact). Triggers via natural-language prompts including \"solidify this decision\" / \"lock down this decision\" / \"make this solid\" / \"challenge/surface/refine to solidify\" (or original \"challenge/review/refine to solidify\") / \"challenge this\" / \"review/refine\" / \"do another round\" / \"sharpen again\" / \"what did we miss\" / \"what are we surfacing\" / \"verify completeness before commit\" — all after AI proposes architectural decision. Phase 1 of two-phase pattern (Phase 2 = pre-implementation-sharpening). AKA the challenge → surface → refine → solidify cycle — this skill IS that operation, formalized as 2-3 disciplined rounds. Applies Pareto discipline (refine for Pareto improvement, not for change) per round. Empirically validated to outperform post-mortem audits/reviews because pre-decision is sparring-mode (per Vivienne Ming research on AI-human hybrid teams) while audits are validator-mode anchored to existing content. NOT for trivial decisions, pure-implementation work, or implementation-start moments (use pre-implementation-sharpening instead)."
when_to_use: After AI proposes architectural decision (decision-record-grade); user wants to solidify / lock down / challenge-surface-refine before commit. Fires AT DECISION-FORMATION MOMENT. Natural triggers: "solidify" / "lock down" / "challenge" / "surface" / "review/refine" / "another round" / "sharpen" / "what did we miss". Do NOT use for implementation-start sharpening — that's pre-implementation-sharpening.
version: 0.10.0
---

# Decision-design sharpening (Phase 1)

> **Extends `sharpen`** (the generic critical-pass skill) with formality specific to decision-record-grade architectural commitments at pre-commit moment: Round-1-full-monty + Round-2 user-triggered + decomposition trigger + persistence-shape output. The core mechanic (read → critical lens → Pareto-graded positions → counter-validation → self-check) is inherited from `sharpen`; this skill adds the context-specific procedure.

Disciplined sharpening protocol applied at decision-formation moment, BEFORE commit to file. Operates UPSTREAM of drift-detection / soundness-review skills (which serve POST-decision purposes).

## Why this skill exists (vs relying on Claude's native sharpening behavior)

Claude naturally sharpens proposals when prompted. This explicit skill adds:

| Value-add | Why it matters |
|---|---|
| **Discipline structure** | Explicit 4-phase cycle + 2-3 round pattern + Pareto check + decomposition trigger — Claude's natural sharpening lacks this structure |
| **Repeatability** | Same methodology applies across decisions; doesn't depend on Claude's mood/context |
| **Composition** | Composes explicitly with framing/scoping + drift-detection + soundness-review + orchestrator skills; native sharpening doesn't compose |
| **Audit-trail integration** | Skill emits AuditEvents (optional); native sharpening is invisible |
| **Anti-bias mechanism** | Explicit user-trigger discipline + Pareto check counters self-validation bias; native sharpening doesn't have these mechanisms |

## The cycle: challenge → surface → refine → solidify

Refined from original "challenge/review/refine to solidify" framing; "review" sharpened to "surface" because the operation is bringing up what's NOT visible (not just checking what's there). "Sharpening" is the collapsed shorthand for this 4-operation cycle. Original "review" terminology still routes here.

### Per-term definitions

| Term | Operation | Mode |
|---|---|---|
| **Challenge** | Stress-test proposal: counter-arguments, weaknesses, edge cases, "what's the strongest argument against?" | Sparring mode (per Vivienne Ming research on AI-human hybrid teams — only sparring outperforms human-alone or AI-alone) |
| **Surface** | Bring up what's NOT visible: schema gaps, lifecycle distinctions, composition concerns, governance integration, observability hooks, missing architectural patterns, layered coverage check | Coverage mode |
| **Refine** | Improve specifics: tighten language, add missing fields, sharpen definitions; validate against existing decisions / vision / architectural disciplines | Improvement + implicit validation |
| **Solidify** | Lock for commit: persist as decision record, anchor for future reference, ensure later-defensibility (will reviewer be able to defend this 6 months from now?) | Decision/output (commit moment AFTER all rounds; not per-round operation) |

### Round-vs-phase relationship

Rounds and phases are NOT 1:1. Each round runs the full cycle conceptually but emphasizes different phases:
- **Round 1 (full monty)**: emphasizes challenge + initial surface + initial refine
- **Round 2 (user-triggered)**: emphasizes deeper surface (cross-cutting + schema layers)
- **Round 3 (when run)**: emphasizes additional surface (architectural patterns OR pre-implementation surfacing — see Phase 2)
- **Solidify**: COMMIT moment after all rounds complete; not per-round

## When this skill fires

- AI proposes architectural decision (decision-record-grade)
- User signals "do another round" / "sharpen again" / "review/refine" / "challenge this" / "what did we miss" / "solidify"
- BEFORE commit to file (decision record, architecture doc, vision/strategy doc, roadmap, or other load-bearing artifact)

NOT for:
- Trivial decisions or pure-implementation work
- Implementation-start moments (use `pre-implementation-sharpening` instead)
- Post-decision drift detection (use drift-detection skills instead)
- Post-decision soundness review (use soundness-review skills instead)

## Why pre-decision sharpening > post-mortem audit/review

Five mechanisms:

1. **Anchoring bias**: post-mortem looks at WHAT IS; pre-decision can explore WHAT COULD BE
2. **Sunk-cost protection**: post-decision reviewers protect existing investment; pre-decision has no sunk cost
3. **Sparring vs validation mode**: sharpening = SPARRING (challenge); audits = VALIDATION (confirm). Per Ming research: sparring outperforms validation
4. **Fresh-context advantage**: sharpening = design context is hot; audits = context is cold
5. **Greenfield-still-anchored problem**: even greenfield checks ("would we build this from scratch?") LOOK AT existing shape; reviewers can't easily generate alternatives outside what's surfaced. Pre-decision sharpening asks designer to GENERATE alternatives directly

## Phase 1 procedure (2-3 rounds total — sweet spot)

### Round 1: AI full monty (initial proactive proposal)

When AI proposes the architectural decision, the proposal includes:

- **Adoption options** (where multiple paths exist; e.g., "4 options considered")
- **Position committed** with reasoning
- **Refinements stress-tested upfront** (typically 5-15 refinements per round 1 for substantive decisions)
- **Edge cases + counter-arguments engaged** (each major counter-argument addressed)
- **Composition with existing architecture** (how this decision interacts with prior decisions)
- **Defers** (chronological-valid; what's deferred + why)
- **Decision shape** (final structure + persistence target)

Do FULL refinement upfront in initial proposal; don't fragment into multiple rounds where user prompts each refinement separately.

### Round 1 termination checklist (mandatory; per session-16 procedural-fidelity META-failure)

Before declaring Round 1 complete, AI MUST explicitly verify each item:

- [ ] **Skill SKILL.md Read at THIS invocation** (Read tool used in current Round, not pattern-matched from earlier session usage). Per `DISCIPLINES.md` Discipline 1 skill+profile sub-section.
- [ ] **Profile files Read for THIS validation** (≥3 cluster members; current Round 1; not reused-citation from earlier topic in same session). Per `DISCIPLINES.md` Discipline 3 profile-anchored validation.
- [ ] **Each archived-source citation greenfield-evaluated** (per `DISCIPLINES.md` Discipline 10): re-validated against locked GLOSSARY + ARCHITECTURE; stress-tested against profiles; pattern-vs-instance check; greenfield-derived. NOT transcribed as template.
- [ ] **Pattern-vs-instance stress-test applied** per primitive (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2): no instance-leakage; cross-archetype illustration valid.
- [ ] **G Gate fired** (if L1-L4 producer artifact): multi-mode consumption requirements satisfied (per `profiles/G-composability-gate.md`).
- [ ] **D Gate fired** (if any defer considered): mental modeling within profile grounding attempted; defer ONLY if mental modeling cannot resolve. Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 + `profiles/INDEX.md` D Gate procedure.

If ANY item unchecked: do not declare Round 1 complete. Address gap before proceeding.

**Why this checklist**: per `drafts/execution-fidelity.md` Disguise #4 (skipping steps that "feel covered" by general approach) + Disguise #5 (substituting AI judgment for codified rule) + Disguise #8 (surface compliance without depth — cite the rule but don't apply it). Procedural-redundancy fix (5-location) addressed compaction-pattern-matching only; this checklist addresses the remaining disguises.

**Failure mode this catches** (canonical session-16 case): arch/coordination.md Round 1 cargo-cult'd archived event-coordination protocol without explicit greenfield-evaluation per element. Checklist item 3 (greenfield-evaluation) would have caught this at Round 1 termination.

### WAIT for user signal to run further rounds

Do NOT auto-run round 2. User triggers via:
- Explicit prompts: "do another round" / "sharpen again" / "review/refine" / "challenge this"
- Direct challenge questions warranting deeper look
- "What did we miss?" / "What about X?"

USER-TRIGGERED rounds outperform AI-self-triggered rounds because external-perspective friction forces AI past its self-validation comfort threshold.

### Round 2: First sharpening (USER-TRIGGERED)

Stress-test what round 1 missed:
- **Primitive-set lens** (LOAD-BEARING when proposing a new primitive): should this concept be a SEPARATE primitive, or could it merge with an existing one? Is it really a refinement (DERIVED) of an existing primitive? Does its boundary cleanly partition conceptual space, or overlap / leave gaps with existing primitives? — counters self-validation bias of accepting AI's initial categorization. (For corpus-level set-redesign across multiple already-locked primitives, see `coherence-audit` Lens 1.)
- **Naming collisions?** Does the proposed primitive's name (or any enum/field within it) collide with existing locked vocabulary? Same word with two distinct meanings is a structural smell.
- **Schema fields incomplete?** Missing required fields, optional fields, validation rules?
- **Lifecycle distinctions missing?** State machines, entity lifecycle, request lifecycle?
- **Composition gaps with other decisions?** How does this interact with existing decisions?
- **Governance integration?** Permission flow? Audit-trail emission?
- **Observability hooks?** Telemetry, logging, monitoring?
- **New architectural patterns surfacing?** Patterns the round 1 didn't name explicitly?
- **Cross-cutting concerns?** Boot/shutdown, errors, transport, deployment-tier-awareness, audit integration
- **Multi-axis validation** (per `DISCIPLINES.md` Discipline 3 (multi-axis sub-section) + `profiles/INDEX.md`): does this decision serve archetype × work-type × role variations? Plus explicit non-coverage question — what use cases does primitive NOT cover; intentional or gap?
- **Profile-anchored validation** (v0.5.0; operational instantiation of multi-axis): for high-impact decisions (primitive classifications; per-mechanism / per-protocol / per-primitive-detail design — Phase 3.3-3.6 territory), test against ≥3 profile-clusters in `profiles/` directory. Flesh skeleton-profile if specific decision affects it (per coherence-audit on-demand fleshing strategy). For routine decisions or cascade-from-established-pattern decisions, multi-axis principle-level check is sufficient. Discriminator: does the decision touch shape-specific or instance-specific surface? If yes → profile-anchored. If purely structural cascade → multi-axis principle-level.
- **G Composability Gate** (per `profiles/G-composability-gate.md`): does this decision support multi-mode consumption (consulting / firm-reuse / OSS / marketplace-future / backup-migration)? If not, reshape before proceeding.
- **D Defer Gate** (per `profiles/INDEX.md`): for any item considered for defer, attempt mental modeling within profile grounding FIRST. Construct hypothetical scenarios across L1-L9 profiles + apply G + multi-axis. Defer ONLY IF mental modeling genuinely cannot resolve. Don't defer when tools are sufficient.

Surface 4-10 genuine refinements per round (empirical observation). Distinguish EXPANSIONS (~80-90%) from REVISIONS (~10-20%). Apply Pareto discipline: each surfaced refinement should be Pareto-improving (better in some dimension without being worse in others). If not Pareto-improving, force "why?" challenge — could be manufactured criticism past where evidence warrants.

**Auto-add to BACKLOG.md** (v0.3.1): when sharpening surfaces forward-references / deferred items (after D Gate confirms genuine awaited-evidence, not mental-modeling-resolvable), add corresponding entries to `BACKLOG.md` under the relevant phase section in same commit. BACKLOG is the central work-item tracker; deferrals must surface there or risk getting lost across sessions. Items resolvable via mental modeling don't go to BACKLOG — they get evolved now in Round 1+2.

**GLOSSARY back-check** (v0.5.0; per `MAINTENANCE.md` Bidirectional cascade): at end of Round 2, before locking, ask explicitly: "did this work surface a glossary-grade structural fact, named distinction, reciprocal symmetry, or vocabulary refinement that should retro-fit into GLOSSARY (Layer 1) before locking the ARCH/DR/spec commit?" Glossary-grade = structural facts about primitive nature / reciprocal symmetry between primitives (Lens 6) / load-bearing vocabulary distinctions / cross-axis interactions. NOT glossary-grade = schema details / per-implementation mechanics / per-shape policy variations. Canonical exemplar: session 16 work-unit always-present container surfaced during Round 2 — retro-fitted to GLOSSARY work-unit + workflow entries before lock.

**REVISION/EXPANSION classification self-check** (v0.6.0; detection mechanism for awaited 3-tier discriminator codification — per BACKLOG watch-list): at Round 2 termination, before locking, ask explicitly: "Any finding classified as EXPANSION that on second look would reclassify as REVISION? Any EXPANSION whose cascade-implications feel REVISION-flavored — load-bearing reciprocal asymmetry / structural elevation of implicit-to-explicit / glossary-grade distinction?" If yes repeatedly across decisions → signal that 2-tier (REVISION/EXPANSION) is producing under-precision; revisit per BACKLOG watch-list "3-tier discriminator codification" entry. If consistently no → 2-tier holds; signal hasn't materialized; defer codification.

**Post-round self-check (v0.3.1)**: at the end of each round (after surfacing findings + applying Pareto verdicts), AI explicitly evaluates against termination signals + sweet-spot pattern + Lens 1+8+9 collective REVISION count (where applicable) and commits a position:

- **STABLE — lock at this round** with reasons (cite specific termination signals: "0 REVISIONS surfaced", "narrow architectural surface = 2-round sweet spot", "all findings are EXPANSIONS not architectural pivots")
- **CONTINUE — Round N+1 warranted** with reasons (cite remaining open questions, broad architectural surface, or specific lens that surfaced incomplete coverage)

User confirms or overrides. Counters self-validation bias in BOTH directions: defaulting to "continue" because more rounds feel productive (manufactured-criticism risk) vs defaulting to "stable" because ending is comfortable (premature-lock risk). Forcing explicit position with rationale makes the self-check observable.

The check is mechanical — termination signals from the next section are the discriminator. Don't override signals with vague "feels stable" or "could go deeper" — name the specific signal.

### Round 3 (OPTIONAL, complexity-dependent): Second sharpening (USER-TRIGGERED)

Run when broader architectural surface warrants:
- Large unified abstraction
- Cross-decision synthesis (multiple sub-decisions composing)
- Genuinely complex architectural surface

Surfaces additional architectural patterns OR coverage of layers AI didn't think to address.

**Empirical sweet-spot pattern**:
- Narrow architectural surface (single decision; skill design): 2-round sweet spot; round 3 yields diminishing returns
- Broad architectural surface (substrate-eval-grade synthesis; multi-decision unification): up to 3-round sweet spot

### After 2-3 rounds → architecturally LOCKED → persist decision record

Decision-design phase COMPLETE. Propose final structure in chat before committing to file. Then commit + reference for future.

**Do NOT continue into operational/runtime details at this phase** — defer to pre-implementation phase (`pre-implementation-sharpening` skill).

## Round termination signals

**MANDATORY at every round termination** (v0.10.0; per `plugin/skills/sharpen/SKILL.md` v0.12.0 comprehensive termination framework — Layer 1 empirical signals + Layer 2 counter-bias mechanisms + Layer 3 verdict logic + Layer 4 mandatory output + target-type modifier + HIGH-magnitude tier + cost-benefit trajectory + empirical-evidence amendment rule). Single-metric verdicts insufficient; surface-coverage is multi-signal.

**Target-type for architectural decisions**: LOCK-HARD (default for this skill — architectural decisions cascade hard if revised; pre-execution sharpening must be exhaustive). Any HIGH triggers C1.

### Empirical density check

Count substantive findings (HIGH + MEDIUM impact; exclude cosmetic / NO-ACTION) for current round vs previous round:

| Density behavior | Verdict signal |
|---|---|
| Drops ≥50% | DECAY CONFIRMED → STABLE candidate |
| Holds within ±25% OR increases | DECAY NOT CONFIRMED → CONTINUE candidate |
| Drops 25-50% | AMBIGUOUS → user-decision |

### Surface-type declaration

Different decay profiles per surface type:
- **ARCHITECTURAL-DECISION** (per-decision; sweet spot 2-3 rounds; expected decay 6→5→3→0-1)
- **PROCEDURE-DOCUMENT** (process docs / methodology; sweet spot may be 4-5 rounds; density-check governs)
- **SET-LEVEL AUDIT** (corpus-level; per-cluster density)
- **META-ARCHITECTURAL** (foundational discipline / framework rebuild; user-trigger primary)

Pattern-matching architectural-decision decay onto other surface types = recurrent bias.

### Honest termination test (Q1-Q5 per sharpen v0.10.0)

Before declaring STABLE or CONTINUE, AI explicitly answers Q1-Q5 (count / decay / specific signal). Q5 unanswerable for STABLE → manufactured comfort territory. Q4 unanswerable for CONTINUE → manufactured criticism territory.

### Lock + persist signals (revised)

Lock + persist when ALL of:
- Density check shows DECAY CONFIRMED (per Q3) for current surface type
- Q5 names specific termination signal (not "feels done")
- Counter-validation passes (manufactured-comfort counter-test passed)

OR: User explicitly says "accept" / "lock" / "looks good, persist".

### Continue signals (revised)

Continue when ANY of:
- Density check shows DECAY NOT CONFIRMED (Q3 holds/increases) AND Q4 names specific unaddressed pass
- User explicitly signals deeper ("another round" / "go deeper" / "what else") — user-trigger overrides AI-judgment unless empirical decay confirmed
- Surface-type is PROCEDURE-DOCUMENT / SET-LEVEL / META-ARCHITECTURAL and density holds

### Other termination signals (preserved)

| Signal | Action |
|---|---|
| 2 rejected rounds in a row (no refinements accepted) | Suggest: "rounds are surfacing nothing accepted; either proposal is solid (lock) OR reframe needed (decompose / restart)" |
| User requests round 4+ at decision-design phase (ARCHITECTURAL-DECISION surface only) | Respond: "round 4+ at architectural-decision phase signals decomposition is missing; recommend decomposing into sub-decisions" (per decomposition trigger). NOTE: decomposition trigger doesn't apply to PROCEDURE-DOCUMENT / SET-LEVEL / META-ARCHITECTURAL surfaces. |
| AI surfaces only manufactured criticism (Pareto-fail refinements) | Respond: "refinements not Pareto-improving; recommend lock OR explicit manufactured-criticism territory" |
| User accepts refinements but doesn't trigger lock | Prompt: "ready to lock + persist? OR additional round?" — explicit termination prompt |

### Manufactured-comfort counter-test (NEW; equal-weight to manufactured-criticism)

Round-fatigue / completion-comfort biases toward STABLE. Equal scrutiny required. AI bias toward declaring STABLE without empirical density measurement = Disguise #5 (substituting AI judgment for codified rule). Canonical session-16 case: declared STABLE LOCK at Round 3 of procedure-sharpening when density was 9→10→9 (holding flat, not decaying); pattern-matched expected decay instead of measuring actual.

## CRITICAL: Decomposition trigger

**If a decision genuinely needs >3 rounds at decision-design phase → DECOMPOSE**.

>3 rounds signals decomposition is missing. Decompose decision into sub-decisions; each sub-decision gets standard 2-3 rounds.

**Decomposition criteria**:
- Decision spans multiple architectural surfaces (decompose into per-surface sub-decisions)
- Decision has independent sub-concerns that can be separately locked
- Decision feels too large to hold in mind during single round

**Pareto + decomposition interaction**: if a refinement is genuinely not Pareto-improving (real tradeoff) AND isn't manufactured criticism, that's a SIGNAL that decomposition may be missing. The trade-off should be evaluated at sub-decision granularity, not at current-decision granularity.

After decomposition: each sub-decision gets full 2-3 round treatment + final synthesis pass.

### Two decomposition modes (v0.6.0)

Decomposition fires in two distinct modes — distinguish at start:

**Mode 1: Emergent decomposition** (organic; >3 rounds signal):
- Round count grows past sweet spot during sharpening of a single decision framing
- Decomposition emerges as the fix for round-count drift
- Trigger: rounds 4+ feel like manufactured criticism OR genuinely-not-Pareto-improving refinements surface
- Procedure: stop current decision; decompose into sub-decisions; each gets fresh 2-3 rounds

**Mode 2: Upfront-known composite decomposition** (planned; multiple tightly-coupled sub-decisions known at start):
- Decision has 3+ tightly-coupled sub-decisions identifiable at framing time (not emergent from drift)
- Examples: doc-structure decisions touching taxonomy + naming + placement + structure simultaneously; multi-primitive cascade locks; any decision with declared dependency graph between sub-parts
- Trigger: at decision framing, if ≥3 sub-decisions visible AND they have foundation-up dependencies
- Procedure:
  1. **Sub-decision inventory**: list sub-decisions explicitly at start (before Round 1)
  2. **Foundation-up dependency ordering**: lock dependency-free sub-decisions first; downstream sub-decisions follow
  3. **Per-sub-decision sharpening**: each sub-decision gets standard 2-round sweet spot independently
  4. **Synthesis pass at end**: after all sub-decisions lock, run a final coherence-pass examining cross-sub-decision consistency (mini coherence-audit scoped to the composite decision's surface)
  5. **Single composite DR or N sub-DRs**: if sub-decisions are independently meaningful, separate DRs; if only meaningful as composite, single DR with sub-decision sections

**Distinction matters because**:
- Emergent mode = error correction (stopping a drift)
- Upfront mode = planned discipline (better than entering as composite and discovering need to decompose mid-flight)
- Upfront mode preserves cognitive efficiency by not forcing AI to hold all sub-decisions simultaneously during early rounds

**Composite decomposition criteria** (when to choose Mode 2 upfront):
- Sub-decisions have visible dependency edges (foundation-up identifiable)
- Sub-decisions are individually small enough for 2-round sweet spot
- Total scope would otherwise produce >3 rounds OR force shallow per-aspect treatment in single decision

## Layered coverage observation (Phase 1 specific)

Each round at decision-design phase EMPHASIZES (but doesn't exclusively cover) a different architectural concern layer:

| Round | Layer of concern emphasized |
|---|---|
| **Round 1** | Architectural decisions (what methods + types + abstractions) |
| **Round 2** | Cross-cutting + schema details (boot, errors, transport, tier-awareness, audit integration) |
| **Round 3 (optional)** | Occasionally surfaces new architectural patterns — complexity-dependent |
| **Round 4+ (DEFER to Phase 2)** | Operational + runtime + deployment concerns belong in `pre-implementation-sharpening` |

If round content shifts to operational/runtime concerns at decision-design phase, that's a signal to STOP this skill and DEFER content to pre-implementation phase.

## EXPANSION vs REVISION calibration

Most refinements (~80-90%) are coverage EXPANSIONS (adding concerns layer by layer). Genuine architectural REVISIONS (~10-20%) change existing decisions.

**EXPANSION examples**:
- New schema fields
- Per-kind context schemas
- New hook events
- Operational primitives (rate limit, timeouts, cancellation)

**REVISION examples** (high signal):
- Changing entity-vs-event categorization for a concept
- Adding new transport mode to existing enum (extends earlier decision)
- Resolving architectural circularity
- Extending governance to cover newly-surfaced surface

Watch for REVISIONS; treat as decision-record amendments (potentially flow back to upstream decisions). Most rounds yield expansions — still valuable; just calibrate expectations.

**Pareto calibration**: EXPANSIONS are Pareto-improving by nature (add coverage without breaking existing). REVISIONS can be Pareto-improving OR worth-the-tradeoff — changing existing decisions might lose something to gain something; require explicit tradeoff justification.

## Inter-round state management

Inter-round state is conversation-context by default. For long sessions OR sessions spanning multiple chat turns, recommend tracking in chat as a "round log":
- Surfaced refinements per round
- Per-refinement disposition (accepted / rejected / deferred-to-later-round)
- Pareto verdict per refinement

Optionally persist to session-store if substrate supports session continuation. For audit-trail integration: each refinement disposition can emit AuditEvent.

## Phase 1 → Phase 2 transition

Phase 1 (decision-design-sharpening) completes when DR locked + persisted. Phase 2 (`pre-implementation-sharpening`) fires AT IMPLEMENTATION-START MOMENT — NOT immediately after Phase 1 completion.

There may be substantial time gap between Phase 1 lock and Phase 2 trigger (could be hours, days, or weeks depending on when implementation begins).

Phase 2 reads the locked DR + sharpens against operational/runtime concerns. Phase 2 architectural findings flow back to Phase 1 DR as amendments (potentially triggering new Phase 1 sharpening on the affected DR — per ~10-20% architectural flow-back).

## Composition with other skills

| Skill type | Composition |
|---|---|
| Framing/scoping skills (e.g., frame-task pattern) | Operate UPSTREAM of this skill — framing precedes AI proposal; sharpening operates AFTER proposal exists |
| `pre-implementation-sharpening` | Phase 2 of same pattern; fires at implementation-start moment, NOT at decision-formation moment |
| Drift-detection skills (e.g., audit) | Operate POST-decision; this skill operates UPSTREAM at decision-formation moment |
| Soundness-review skills (e.g., design-review) | Operate POST-decision; same — this skill upstream |
| Orchestrator skills | Could route to this skill when architectural-decision moment surfaces in workflow |

## Output specification

Concrete output of complete decision-design-sharpening session:

- **Decision record (DR) at deployment-conventional path** (e.g., `docs/decisions/<topic>.md`)
- **Status field**: ACCEPTED with sharpening-rounds metadata (e.g., "2-round sharpening: full monty + 1 user-triggered")
- **Refinements summary section** noting:
  - Round count + which rounds were user-triggered
  - Refinements incorporated count + breakdown (X expansions; Y revisions)
  - Pareto verdict per refinement (incorporated vs rejected vs deferred)
- **DR body following standard structure** (per deployment conventions):
  - Status / Owner / Related
  - Context
  - Decision
  - Refinements applied (per round)
  - Composition with existing architecture
  - Defers
  - Constraints flowing
  - Files touched
  - Revisit triggers

## Concrete invocation example

```
1. AI proposes architectural decision in chat
   → "Here's my proposal for X: [comprehensive proposal with 5-10 refinements]"

2. User triggers sharpening
   → "let's solidify this" OR "do another round" OR "challenge/refine"

3. Skill activates (Phase 1, Round 2)
   → AI surfaces 4-10 refinements: "Here's what round 2 surfaces..."
   → Each refinement evaluated for Pareto
   → User accepts/rejects/defers per refinement

4. (Optional) User triggers Round 3
   → AI surfaces additional refinements (complexity-dependent)

5. User triggers lock
   → "looks good, persist" OR "lock"
   → Skill prompts: "ready to commit DR? structure: [shape]" (chat-first)
   → User confirms; AI commits DR to file

6. Output: DR persisted with full sharpening-rounds metadata
```

## Audit-trail integration (optional; composable with audit-trail infrastructure if available)

If deployment has audit-trail infrastructure, each sharpening round can emit:
- `event_kind=sharpening_round_started` with `round_number` + `decision_kind` + `phase=decision_design`
- `event_kind=sharpening_round_completed` with `refinements_surfaced` count + `expansion_count` + `revision_count`

Composes with audit-trail-as-canonical-source pattern + later-defensibility.
