---
name: sharpen
description: Apply rigorous critical evaluation to any content — drafts, proposals, plans, reasoning chains, writeups, ideas, summaries, decisions, architectural sketches, message drafts. Surfaces load-bearing vs decorative, overclaim vs grounded, redundant vs essential, gaps vs covered. Default output: KEEP / REVISE / CUT positions per finding, with rationale, with explicit counter-validation against self-validation bias. Forces refine-by-cut alongside refine-by-add. Triggers via natural prompts including "sharpen this", "sharpen the {target}", "review this critically", "what would you push back on", "challenge this", "what's load-bearing vs decorative", "what should I cut", "tighten this", "where are the gaps", "be ruthless on this", "another round", "go deeper", "what else". Single critical pass by default; iterates when user signals deeper.
when_to_use: User has content and wants critical evaluation with explicit discipline (Pareto check, counter-validation, refine-by-cut). Anti-pattern signal: AI defaulting to "looks good" or to addition-suggestions only — that's self-validation bias triggered; this skill counters it.
version: 0.8.0
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

### 6. Post-pass self-check

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

Commit STABLE or CONTINUE position with rationale citing specific signal:

- **STABLE** — zero substantive findings after honest run (categorical AND additional passes per Step 6); counter-validation passed; surface size doesn't warrant another round
- **CONTINUE** — real gaps remain; specific lens underexplored; user signaled deeper

Substantive = affects load-bearing claims, structural integrity, or reader's mental model. Cosmetic-only findings don't block STABLE.

**Iteration is USER-TRIGGERED.** Don't auto-iterate after STABLE verdict — AI-self-triggered rounds drift toward manufactured criticism (per `feedback_pre_decision_sharpening`). When user signals "another round" / "go deeper" / "what else" / "be more ruthless": iterate. Same procedure; typically different angle (first pass: structure + cuts; second pass: substance + clarity; third pass: cross-references + dependencies).

## Anti-patterns (failure modes the skill counters)

- **Pattern-matching from memory** — produces fake findings about content that isn't there
- **Validator-mode** — checking conformance to declared rules vs sparring-mode (challenging assumptions, generating alternatives)
- **Manufactured criticism** — Pareto-fail refinements
- **Manufactured findings to fill all categories** — surfacing one finding per lens question even when the question doesn't apply to the target
- **Skipping load-bearing questions** — surface findings (typos, phrasing) defaulting because they feel productive while substance questions stay unasked
- **Silent KEEP** — not stating "this is solid because X" leaves implicit-acceptance; explicit rationale matters
- **CUT-without-rationale** — refine-by-cut momentum bias; "this feels verbose" isn't a cut rationale
- **Auto-iteration after STABLE** — AI-self-triggered rounds drift toward manufactured criticism; iteration is user-triggered

