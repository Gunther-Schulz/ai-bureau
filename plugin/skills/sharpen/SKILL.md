---
name: sharpen
description: "**READ THIS FILE BEFORE APPLYING. Use the Read tool to load this SKILL.md at every invocation, regardless of prior usage in same session — pattern-matching from memory of prior usage FAILS load-bearing discipline elements (per `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)).** Apply rigorous critical evaluation to any content — drafts, proposals, plans, reasoning chains, writeups, ideas, summaries, decisions, architectural sketches, message drafts. Surfaces load-bearing vs decorative, overclaim vs grounded, redundant vs essential, gaps vs covered. Default output: KEEP / REVISE / CUT positions per finding, with rationale, with explicit counter-validation against self-validation bias. Forces refine-by-cut alongside refine-by-add. Triggers via natural prompts including \"sharpen this\", \"sharpen the {target}\", \"review this critically\", \"what would you push back on\", \"challenge this\", \"what's load-bearing vs decorative\", \"what should I cut\", \"tighten this\", \"where are the gaps\", \"be ruthless on this\", \"another round\", \"go deeper\", \"what else\". Single critical pass by default; iterates when user signals deeper."
when_to_use: User has content and wants critical evaluation with explicit discipline (Pareto check, counter-validation, refine-by-cut). Anti-pattern signal: AI defaulting to "looks good" or to addition-suggestions only — that's self-validation bias triggered; this skill counters it.
version: 0.12.0
---

# Sharpen — critical-pass discipline

Rigorous critical evaluation applied to content. The procedure is generalizable: read → critical lens → Pareto-graded positions → counter-validation → self-check. Works on any content needing one honest critical pass before commit / send / lock.

## Spirit (anchor for future revisions)

Honest critical evaluation that counters self-validation bias by forcing **cognitive-mode shifts** the default mode misses (categorical → non-categorical; writer → reader; text-reader → procedure-runner). **Sparring-mode**, not validator-mode: challenges assumptions, generates alternatives, attacks content — doesn't check conformance to declared rules. **Pareto-disciplined**: rejects manufactured criticism alongside refine-by-add bias; trivial-but-Pareto-improving findings count as low-value churn. **Commits positions**, doesn't menu options.

Future revisions test: does the change preserve honest evaluation + cognitive-mode-shifting + sparring-orientation + Pareto discipline + position-committing? Or does it drift toward validator-mode / consensus-seeking / completeness-for-its-own-sake / rate-and-rank scoring?

**Self-applicability test**: this skill must remain runnable on itself. If a revision makes the skill un-self-applicable (e.g., requires external context the skill itself doesn't have, or assumes a target shape the skill isn't), the revision drifts from spirit. Run sharpen on the sharpen skill periodically to verify.

**AI-executor test**: this skill is executed by AI. Form should prompt mechanical AI iteration (bulleted sequential engagement; structured cognitive-mode prompts) over narrative gist-extraction. When form tradeoffs arise (compact prose vs nested bullets; flowing paragraph vs explicit checklist), default to the form that prompts iteration — not the form that reads cleanest to a human.

## When to use

- After producing content (your own or under review)
- When tempted to ship something but want one more honest pass
- When AI's default is "looks good" — that's the moment to engage this skill, not skip it

## The procedure

### 1. Read the target fully

Source-grounded: cite the content; don't pattern-match from memory of similar things. Pattern-matching produces fake findings about content that isn't there.

When surfacing findings that reference external claims, distinguish synthesis (your interpretation) from citation (verifiable from source). The sharpening discipline applies to your own findings, not just the target's content.

### 2. Apply critical lens

Surface findings against load-bearing questions (in order — substance before surface):

- **Load-bearing vs decorative**: what's actually doing work vs fluff?
- **Overclaim vs grounded**: what's stated more strongly than evidence supports?
- **Redundant**: what could be cut without loss?
- **Missing / gap**: what should be there but isn't?
- **Unclear / could be sharper**: what reads ambiguously?
- **Internal contradiction**: does the content contradict itself?
- **External contradiction**: does it contradict source material, locked vocabulary, established commitments?
- **Scope-fit**: does this content fit the target's scope/territory, or does it leak into adjacent scope (e.g., positioning into a stance doc; methodology into vision; implementation-detail into a value-claim)?

The questions are ordered intentionally. Surface-level findings (typos, phrasing, formatting) come AFTER substance findings — never as substitutes.

Lens questions that don't apply to the target are skippable — don't manufacture findings to fill all categories.

**Frame-level question (fires once per pass)**: Is this the right target? Sharpen evaluates the content as given, but the load-bearing finding sometimes isn't *in* the target — it's that the target answers the wrong question or addresses a poorly-framed underlying need. If so, surface that *before* sharpening the target itself. The user can always redirect — but they decide with that perspective surfaced, not without.

### 3. Apply Pareto discipline per finding

Pareto-improving = better in some dimension WITHOUT being worse in others. If a finding isn't Pareto-improving, force the "why?" challenge — could be manufactured criticism. Reject manufactured criticism.

Trivial cosmetic findings — even if Pareto-improving — count as low-value churn and are rejectable. Pareto-pass alone isn't sufficient; the finding must also be substantive enough to warrant the change.

### 4. Commit positions per finding (mandatory output)

Each finding requires explicit verdict with rationale — silent acceptance is not allowed. The verdict types:

- **KEEP** — explicit "this is solid because X" (not silent omission)
- **REVISE** — specific revision proposed
- **CUT** — rationale citing what's redundant / overclaim / decorative

All three verdicts need explicit rationale. CUT-without-rationale is also bias (refine-by-cut momentum) — "this feels verbose" is not a cut rationale; "this is dead weight because X" is.

Don't menu the findings. Commit positions. User adjusts / challenges / confirms. (Per `feedback_judgment_and_automate.md`.)

If a pass produces only "looks good" without explicit KEEP-rationale, OR produces only addition-suggestions without any CUT or REVISE, **self-validation bias triggered**. Re-engage with cut-questions (Step 5).

### 5. Counter self-validation bias

The bias triggers in two predictable directions:

- **Defending the content** — sycophancy on recent work; "looks good" defaults
- **Refining-by-add only** — easy direction; addition-suggestions feel productive

Counter-mechanism: force the cut-questions explicitly. What's redundant? What's overclaim? What's decorative? What could be removed without loss?

### 6. Post-pass self-check (cognitive-mode passes)

Before declaring STABLE: the lens questions in Step 2 are categorical (each tests for content matching a category). Run additional **cognitive-mode passes** — each prompts a different default the categorical lens misses:

- **Non-categorical pass** — catches findings that fall *between* the structured categories:
  - What's implicit but unstated?
  - Where is coverage asymmetric? (e.g., one bias guarded but its inverse unguarded)
  - What edge case is unguarded?
  - What assumption is smuggled in?
- **Cold-read pass** — simulate a reader without the author's context; catches author-context-blindness:
  - Would they parse this correctly?
  - Where would they stumble?
  - What unstated assumptions need surfacing?
  - (Author-context only; domain-knowledge gaps are usually intentional scope decisions, not failures.)
- **Mechanism-simulation pass** (applies to procedural targets or procedural sections of mixed-content targets — skills, prompts, runbooks, rules, checklists, decision-trees, or procedure-blocks within a larger doc) — mentally execute the procedure; catches procedural gaps masked by text-coherent surface:
  - Does it produce the intended output?
  - Missing termination conditions?
  - Ambiguous branching?
  - Steps depending on outputs not produced?

Simulate honestly across all passes — don't manufacture findings the simulation wouldn't actually produce.

## Termination criteria — comprehensive framework (v0.12.0)

**Goal**: STABLE = evidence that surface is COVERED, NOT "no findings this round." Density / surface-type / Q-test are INSTRUMENTATION verifying the goal — never substitutes for the goal.

Single-metric verdicts (density alone / HIGH-count alone / Q4 alone) are insufficient. Surface-coverage is multi-signal.

**Target-type modifier (v0.12.0)**: declared at sharpening start; affects framework verdict logic.

| Target type | Examples | Behavior |
|---|---|---|
| **LOCK-HARD** | Architectural decisions; foundational primitives; locked-vocabulary entries; spec contracts | Pre-execution sharpening must be exhaustive (downstream cascade cost high if revised). Any HIGH → C1 fires regardless of magnitude. |
| **AMENDABLE-IN-FLIGHT** | Procedure docs; methodology; process documents; runbooks (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 preliminary-lock — amendable per execution evidence) | Pre-execution sharpening optimized for "good enough to start." Only STRUCTURAL-LOAD-BEARING HIGH → C1 fires; MECHANICS-OPERATIONAL HIGH → soft signal (user-decision). |

User declares target-type at sharpening start. Default: LOCK-HARD (conservative). AMENDABLE-IN-FLIGHT requires explicit declaration.

### Layer 1 — Empirical evidence signals (positive coverage indicators)

Track at each round termination:

| Signal | Measure | Coverage interpretation |
|---|---|---|
| **Cognitive-mode pass coverage** | Per-round track which passes applied (categorical lens / non-categorical / cold-read / mechanism-simulation) | All applicable applied = surface explored |
| **Counter-stress survival** | % of prior-round findings that survive Round N stress-test (vs being revised/withdrawn) | Trending toward 100% = surface stabilizing |
| **HIGH-finding count** | HIGH count current round | 0 in current round = load-bearing rigor saturating |
| **HIGH-impact magnitude classification (v0.12.0)** | Per HIGH finding: STRUCTURAL-LOAD-BEARING (affects target's fundamental shape) vs MECHANICS-OPERATIONAL (refinement; doesn't change shape; amendable in-flight) | LOCK-HARD targets: any HIGH triggers C1; AMENDABLE-IN-FLIGHT targets: only STRUCTURAL-LOAD-BEARING HIGH triggers C1 |
| **HIGH-finding decay** | HIGH count trend across rounds | Trending toward 0 = saturating |
| **Cost-benefit trajectory (v0.12.0)** | Pareto-acceptance ratio trend (last 2 rounds); LOW-finding count vs HIGH+MEDIUM ratio | Pareto-acceptance dropping ≥30% in last 2 rounds OR LOW > 2x HIGH+MEDIUM = manufactured-criticism territory approaching; STABLE-candidate signal even if C-conditions hold |
| **Total substantive density** | (HIGH+MEDIUM) count current vs previous | ≥50% drop = decay; ≥25% drop = partial decay; <25% = holding |
| **Pareto-acceptance ratio** | Accepted findings / surfaced findings (per round) | Dropping = manufactured-criticism territory approaching |
| **Q4 specific-concern test** | Specific Round-N+1 concern nameable with substance | Unanswerable when forced = manufactured criticism territory |

**Surface-type declaration (mandatory)**: ARCHITECTURAL-DECISION / PROCEDURE-DOCUMENT / SET-LEVEL AUDIT / META-ARCHITECTURAL. Different surfaces have different baseline density profiles; pattern-matching wrong decay = surface-type-mismatch bias.

Surface-type sweet spots (informational baselines for orientation, NOT verdict criteria):
- ARCHITECTURAL-DECISION: typically 2-3 rounds (per `DISCIPLINES.md` Discipline 3 empirical pattern from session-12)
- PROCEDURE-DOCUMENT: typically 4-5+ rounds (broader cognitive-pass surface; per session-16 empirical)
- SET-LEVEL AUDIT: per-cluster (each cluster sharpens until cluster-exhausted)
- META-ARCHITECTURAL: indeterminate; user-trigger primary

### Layer 2 — Counter-bias mechanisms (verify signals are honest)

Every termination verdict requires explicit counter-bias check:

| Counter | Catches |
|---|---|
| **Manufactured-comfort** | Premature STABLE due to round-fatigue / completion-comfort |
| **Manufactured-criticism** | Extending rounds with non-Pareto / cosmetic findings |
| **Surface-type-mismatch** | Pattern-matching wrong-surface decay |
| **Self-validation** | Confirming current verdict without independent test |
| **Single-metric tunnel-vision** | Using one signal alone instead of multi-signal coverage assessment |
| **Coverage-blindness** | Declaring STABLE without tracking cognitive-mode passes applied |
| **Counter-stress avoidance** | Pure-extension (only adding new findings) without testing prior findings |

### Layer 3 — Verdict logic

**CONTINUE when ANY of** (v0.12.0 target-type aware):
- **C1**: Round N has HIGH findings — for LOCK-HARD targets, ANY HIGH fires C1; for AMENDABLE-IN-FLIGHT targets, only STRUCTURAL-LOAD-BEARING HIGH fires C1; MECHANICS-OPERATIONAL HIGH on amendable targets is soft signal (user-decision via Layer 3 USER-DECISION path)
- C2: Cognitive-mode passes incomplete (specific pass not yet applied per Layer 1 coverage)
- C3: Specific Round-N+1 concern nameable with substance (Q4 answerable)
- C4: Counter-stress survival incomplete (Round N extends rather than tests prior; pure-add bias)
- C5: User explicit trigger ("another round" / "go deeper" / "what else")
- C6: Pareto-acceptance ratio holding (findings still substantive; no manufactured-criticism trend)

**STABLE when ALL of**:
- S1: HIGH count = 0 in current round (load-bearing rigor saturated)
- S2: All applicable cognitive-mode passes applied (Layer 1 coverage matrix complete)
- S3: Q4 unanswerable (no specific Round-N+1 concern with substance)
- S4: Counter-stress survival ≥80% (surface stable; not actively shifting)
- S5: Density decay confirmed (HIGH-only ≥50% drop AND total substantive ≥25% drop)
- S6: Pareto-acceptance ratio dropping (manufactured-criticism territory approaching)
- S7: Specific termination signal cited (not "feels done")
- S8: Manufactured-comfort counter-test passes (round-fatigue not the driver)

**USER-DECISION** when:
- Mixed signals (some CONTINUE conditions hold; some STABLE conditions hold)
- HIGH count partially decayed but ≠ 0
- User-trigger overrides AI-judgment unless ALL S-conditions verified

### Layer 4 — Mandatory output at every round termination

AI surfaces in chat (NOT skipped; NOT pattern-matched):

1. **Coverage matrix**: which cognitive-mode passes applied this round? Which not yet?
2. **Density count**: substantive findings (HIGH/MEDIUM/LOW/NO-ACTION) current vs previous
3. **HIGH-finding decay trend**: current HIGH count + trend across rounds
4. **Counter-stress survival rate**: % of prior-round findings tested + survived
5. **Pareto-acceptance ratio**: accepted findings / surfaced findings
6. **Q4 + Q5 honest answers**: specific Round-N+1 concern OR specific termination signal cited
7. **Counter-bias checks** (all of Layer 2): each counter explicitly checked
8. **Verdict**: CONTINUE / STABLE / USER-DECISION with rationale citing specific Layer 3 conditions

### Iteration discipline

- **AI-side iteration**: NOT auto-triggered; user-triggered or driven by C-conditions Layer 3
- **User-trigger CONTINUE**: HONORED unless ALL S-conditions verified (Disguise #5 prevention: AI-judgment-override of user-trigger is structurally suspect)
- **STABLE verdict requires structural evidence**: density decay + coverage complete + counter-stress survival + Q4 unanswerable + counter-bias checks pass

**Iteration is USER-TRIGGERED for AI-side rounds**. Don't auto-iterate after STABLE verdict — AI-self-triggered rounds drift toward manufactured criticism. When user signals "another round" / "go deeper" / "what else" / "be more ruthless": iterate; user-trigger overrides AI-judgment STABLE unless ALL S-conditions verified.

## Empirical-evidence amendment rule (v0.12.0; counters recursive-tuning trap)

This skill's termination framework is preliminary-locked at v0.12.0. Future framework amendments require **observed-pattern evidence threshold**:

1. **Pattern observed across ≥2 sessions** (not single-case)
2. **Pattern can't be addressed via existing user-decision path** (Layer 3 USER-DECISION case)
3. **Amendment captures systematic difference**, not edge case

**Why this rule exists**: session 16 surfaced 3 systematic patterns requiring framework amendment (v0.10.0 surface-type; v0.11.0 multi-signal; v0.12.0 target-type + magnitude + trajectory). Each was Pareto-improving when locked. BUT: each meta-iteration also has diminishing marginal value AND risks recursive-tuning trap (endlessly amending framework based on theoretical concerns).

**Counter to recursion**: amendments require observed evidence, not pre-emptive imagination. If a future round-termination case feels mishandled by current framework, log as observation; don't immediately amend. After ≥2 sessions show same pattern, amend.

**What's NOT covered by amendment rule**:
- Edge cases (single-occurrence; no systematic pattern)
- Hypothetical concerns (not observed)
- Theoretical completeness (framework can never be perfectly complete)

User-decision path always available for cases framework doesn't capture. Don't reach for amendment when user-decision suffices.

## Anti-patterns (failure modes the skill counters)

- **Pattern-matching from memory** — produces fake findings about content that isn't there
- **Validator-mode** — checking conformance to declared rules vs sparring-mode (challenging assumptions, generating alternatives)
- **Manufactured criticism** — Pareto-fail refinements
- **Manufactured findings to fill all categories** — surfacing one finding per lens question even when the question doesn't apply to the target
- **Skipping load-bearing questions** — surface findings (typos, phrasing) defaulting because they feel productive while substance questions stay unasked
- **Silent KEEP** — not stating "this is solid because X" leaves implicit-acceptance; explicit rationale matters
- **CUT-without-rationale** — refine-by-cut momentum bias; "this feels verbose" isn't a cut rationale
- **Auto-iteration after STABLE** — AI-self-triggered rounds drift toward manufactured criticism; iteration is user-triggered
- **Manufactured comfort** — AI-bias toward STABLE without empirical decay measurement; pattern-matching expected decay vs measuring actual density (canonical session-16 case: STABLE LOCK at Round 3 of procedure-sharpening when density was holding flat 9→10→9, not decaying)
- **Pattern-matching termination signals** — applying architectural-decision decay (6→5→3→0-1) to procedure-document or set-level audit surface types; surface-type-mismatch bias
- **Single-metric tunnel-vision** — using density alone OR HIGH-count alone OR Q4 alone instead of multi-signal coverage assessment
- **Coverage-blindness** — declaring STABLE without tracking which cognitive-mode passes applied
- **Counter-stress avoidance** — pure-extension (only adding new findings) without testing prior findings
- **Self-validation on verdict** — confirming current STABLE/CONTINUE without independent test (counter-bias check skipped)
