---
name: sharpen
description: Apply rigorous critical evaluation to any content — drafts, proposals, plans, reasoning chains, writeups, ideas, summaries, decisions, architectural sketches, message drafts. Surfaces load-bearing vs decorative, overclaim vs grounded, redundant vs essential, gaps vs covered. Default output: KEEP / REVISE / CUT positions per finding, with rationale, with explicit counter-validation against self-validation bias. Forces refine-by-cut alongside refine-by-add. Triggers via natural prompts including "sharpen this", "sharpen the {target}", "review this critically", "what would you push back on", "challenge this", "what's load-bearing vs decorative", "what should I cut", "tighten this", "where are the gaps", "be ruthless on this", "another round", "go deeper", "what else". Single critical pass by default; iterates when user signals deeper.
when_to_use: User has content and wants critical evaluation with explicit discipline (Pareto check, counter-validation, refine-by-cut). Anti-pattern signal: AI defaulting to "looks good" or to addition-suggestions only — that's self-validation bias triggered; this skill counters it.
version: 0.2.0
---

# Sharpen — critical-pass discipline

Rigorous critical evaluation applied to content. The procedure is generalizable: read → critical lens → Pareto-graded positions → counter-validation → self-check. Works on drafts, proposals, plans, reasoning chains, writeups, decisions, sketches — anything that benefits from one honest critical pass before commit / send / lock.

## When to use

- After producing content (your own or under review)
- When tempted to ship something but want one more honest pass
- When user asks "sharpen this" / "what would you push back on" / "what should I cut" / "tighten this" / "be ruthless"
- When AI's default is "looks good" — that's the moment to engage this skill, not skip it

## The procedure

### 1. Read the target fully

Source-grounded: cite the content; don't pattern-match from memory of similar things. Pattern-matching produces fake findings about content that isn't there.

### 2. Apply critical lens

Surface findings against load-bearing questions (in order — substance before surface):

- **Load-bearing vs decorative**: what's actually doing work vs fluff?
- **Overclaim vs grounded**: what's stated more strongly than evidence supports?
- **Redundant**: what could be cut without loss?
- **Missing / gap**: what should be there but isn't?
- **Unclear / could be sharper**: what reads ambiguously?
- **Internal contradiction**: does the content contradict itself?
- **External contradiction**: does it contradict source material, locked vocabulary, established commitments?

The questions are ordered intentionally. Surface-level findings (typos, phrasing, formatting) come AFTER substance findings — never as substitutes.

### 3. Apply Pareto discipline per finding

Pareto-improving = better in some dimension WITHOUT being worse in others. If a finding isn't Pareto-improving, force the "why?" challenge — could be manufactured criticism. Reject manufactured criticism.

### 4. Commit positions per finding

Each finding gets a verdict with rationale:

- **KEEP** — "this is solid because X" (explicit; not silent omission)
- **REVISE** — specific revision proposed
- **CUT** — rationale citing what's redundant / overclaim / decorative

Don't menu the findings. Commit positions. User adjusts / challenges / confirms.

### 5. Counter self-validation bias

The bias triggers in two predictable directions:

- **Defending the content** — sycophancy on recent work; "looks good" defaults
- **Refining-by-add only** — easy direction; addition-suggestions feel productive

Counter-mechanism: force the cut-questions explicitly. What's redundant? What's overclaim? What's decorative? What could be removed without loss? If the pass produces only addition-suggestions or only "looks good," bias triggered — re-engage with cut-questions.

### 6. Post-pass self-check

Commit STABLE or CONTINUE position with rationale citing specific signal:

- **STABLE** — zero substantive findings after honest run; counter-validation passed; surface size doesn't warrant another round
- **CONTINUE** — real gaps remain; specific lens underexplored; user signaled deeper

If user signals "another round" / "go deeper" / "what else" / "be more ruthless": iterate. Same procedure; typically different angle (first pass: structure + cuts; second pass: substance + clarity; third pass: cross-references + dependencies).

## Mandatory output

Every sharpen pass MUST produce at least one of:

- A KEEP position with explicit rationale (not silent omission)
- A REVISE position with specific revision
- A CUT position with rationale

If a pass produces only "looks good" without explicit KEEP-rationale, OR produces only addition-suggestions without any CUT or REVISE, **self-validation bias triggered**. Re-engage with cut-questions.

## Anti-patterns (failure modes the skill counters)

- **Pattern-matching from memory** — produces fake findings about content that isn't there
- **Validator-mode** — checking conformance to declared rules vs sparring-mode (challenging assumptions, generating alternatives)
- **Manufactured criticism** — Pareto-fail refinements
- **Defending recent content** — sycophancy / self-validation bias
- **Refining-by-add only** — addition-bias; force the symmetric cut-questions
- **Skipping load-bearing questions** — surface findings (typos, phrasing) defaulting because they feel productive while substance questions stay unasked
- **Silent KEEP** — not stating "this is solid because X" leaves implicit-acceptance; explicit rationale matters

## Concrete invocation

```
1. User: "sharpen this" / "review this critically" / "what would you cut" / "be ruthless"

2. Read target fully (source-grounded).
   Apply critical lens (substance questions first; surface questions after).
   Pareto-grade each finding.
   Commit KEEP / REVISE / CUT position per finding with rationale.

3. Surface findings list in chat:
   F1: [observation] → KEEP / REVISE / CUT (rationale)
   F2: [observation] → KEEP / REVISE / CUT (rationale)
   ...

4. Self-check: STABLE (cite zero-substantive-findings + counter-validation-passed) or CONTINUE (cite specific gap)?

5. User: confirms / adjusts / challenges per finding.
   Apply confirmed positions.

6. (Optional) User signals another round → iterate same procedure; different angle.
```

## Why this skill earns its place

Without explicit critical-pass discipline:

- Evaluation happens implicitly; varies by mood / context
- Pareto check skipped; manufactured criticism unflagged
- Counter-validation applied inconsistently
- Refine-by-add dominates; refine-by-cut neglected
- "Looks good" sycophancy on recent work goes unchallenged
- Surface findings (typos, phrasing) substitute for substance findings

With this skill: the procedure is mechanical and repeatable. Discipline survives mood / context / sycophancy pressure. Cut-questions get explicit airtime.

## Composition with more-formal contexts

For most content, the procedure above is sufficient. Specific contexts may benefit from added formality:

| Context | Extension |
|---|---|
| Decision-record-grade architectural commitment, pre-commit | `decision-design-sharpening` adds Round-1-full-monty + Round-2 user-triggered + decomposition trigger + persistence shape |
| Implementation-start moment, post-decision-lock | `pre-implementation-sharpening` adds operational/runtime-detail surfacing + DR-amendment flow-back |
| Cross-decision corpus / SET of locked decisions | `coherence-audit` adds 10 universal lenses + corpus-specific lenses |

The extensions preserve the same core mechanic (read → lens → Pareto-positions → counter-validation → self-check) and add context-specific lenses / formal output. The core mechanic does most of the work; extensions add formality where context warrants.
