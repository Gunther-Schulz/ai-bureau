---
name: sharpen
description: Use to apply critical-pass sharpening discipline to ANY content — drafts, proposals, plans, reasoning chains, writeups, ideas, summaries. The generic version of the sharpening-skill spirit (challenge → surface → refine → commit position) applicable to anything not covered by the three specialized sharpening skills (`decision-design-sharpening` for pre-commit decisions; `pre-implementation-sharpening` for implementation-start; `coherence-audit` for cross-decision corpus). Triggers via natural prompts including "sharpen this", "sharpen the {target}", "review this critically", "what would you push back on", "challenge this", "what's load-bearing vs decorative", "what should I cut", "tighten this", "where are the gaps", "be ruthless on this", or any request to evaluate content rigorously without phase / artifact-type formality. Default: single critical pass with KEEP / REVISE / CUT positions per finding. Iterates if user signals "another round" / "go deeper".
when_to_use: User has content (any kind — draft, proposal, plan, reasoning, writeup, idea, summary, message draft, review note, brainstorm output) and wants critical evaluation. Applies the sharpening spirit lightly — no formal Round-1-full-monty / Round-2 structure unless target is decision-record-grade (in which case defer to `decision-design-sharpening`). Catches everything the specialized skills don't. Composes naturally with other skills: defer to specialized skills when target fits their scope; use `sharpen` as catch-all critical-pass.
version: 0.1.0
---

# Sharpen — generic critical-pass skill

The sharpening-skill spirit applied to anything. Different from the three specialized skills because:

- **Not phase-anchored** (any time)
- **Not artifact-anchored** (any content)
- **Lightweight by default** — single critical pass; iterate only if user signals
- **No formal output** — findings list with positions; user adjusts/challenges/confirms

## When to use this skill vs specialized

| Target | Skill |
|---|---|
| One decision, pre-commit (decision-record-grade architectural commitment) | `decision-design-sharpening` |
| One decision at implementation-start moment (locked DR; before code) | `pre-implementation-sharpening` |
| Cross-decision corpus / SET of locked decisions (GLOSSARY, ARCH, DR-set, spec-set) | `coherence-audit` |
| Anything else (drafts, proposals, plans, writeups, reasoning, ideas, summaries, message drafts, review notes) | **`sharpen`** (this skill) |

The specialized skills bring formal procedure (Round 1 + Round 2; per-corpus lenses; phase-specific output). `sharpen` brings the same SPIRIT without the formal scaffolding.

## The sharpening spirit (universal)

What stays consistent across all four skills:

1. **Read the target fully** — context-grounded, not pattern-matched. Per `feedback_source_grounded.md`: cite content; flag synthesis vs citation.
2. **Critical lens** — surface what's wrong, weak, missing, redundant, unclear, contradictory. Default questions:
   - **Load-bearing vs decorative**: what's actually doing work vs what's fluff?
   - **Overclaim vs grounded**: what's stated more strongly than evidence supports?
   - **Redundant**: what could be cut without loss?
   - **Missing / gap**: what should be there but isn't?
   - **Unclear / could be sharper**: what reads ambiguously?
   - **Internal contradiction**: does the content contradict itself?
   - **External contradiction**: does it contradict locked vocabulary, established commitments, source material?
3. **Pareto discipline per finding** — Pareto-improving means better in some dimension WITHOUT being worse in others. If not Pareto-improving, force the "why?" challenge — could be manufactured criticism. Reject manufactured criticism.
4. **Commit positions per finding** — KEEP / REVISE / CUT (with rationale citing the specific reason). Per `feedback_judgment_and_automate.md`: don't menu the findings; commit positions; user adjusts/challenges/confirms.
5. **Counter self-validation bias** — actively look for what could be wrong, not what confirms current state. Especially: refining-by-CUT is harder than refining-by-ADD; force the cut question.
6. **Post-pass self-check** — STABLE or CONTINUE position with rationale citing specific signal:
   - **STABLE**: zero substantive findings; counter-validation passed; surface size doesn't warrant another round
   - **CONTINUE**: real gaps remain; specific lens (load-bearing question) underexplored; user signals deeper

## Procedure (single-pass default)

1. Read the target. Source-grounded discipline applies (cite content; don't pattern-match from summaries).
2. Apply critical lens. Surface findings with brief description per finding.
3. Commit positions (KEEP / REVISE / CUT) with rationale per finding.
4. Self-check: STABLE or CONTINUE? Cite specific signal.
5. Output: findings list with positions in chat. User confirms / adjusts / challenges.

If user signals "another round" / "go deeper" / "what else" / "be more ruthless": iterate. Same procedure; usually different angle (e.g., first pass: structure + cuts; second pass: substance + clarity; third pass: cross-references + dependencies).

## Anti-patterns

- **Pattern-matching from memory of similar content** — read the actual target. Per source-grounded discipline.
- **Validator-mode** — checking conformance to declared rules vs sparring-mode (challenge assumptions, generate alternatives). Per `feedback_pre_decision_sharpening.md`: sparring outperforms validator-mode for surfacing genuine refinements.
- **Manufactured criticism** — refinements that aren't Pareto-improving. Force the "why?" challenge.
- **Defending content because user just wrote it** — sycophancy / self-validation bias on user's recent work. The sharpen skill exists BECAUSE this defensive instinct is the default; counter-mechanism: if your first impulse is "looks good," that IS the bias triggering — re-engage critically.
- **Refining-by-add only** — easier direction; add suggestions feel productive. Force the symmetric: what could be CUT? what's REDUNDANT? what's BLOAT?
- **Skipping the load-bearing questions** — the structural ones (load-bearing vs decorative; overclaim; missing) are uncomfortable because they point at substance, not surface. Don't default to mechanical-compliance findings (typo / formatting / phrasing) when load-bearing questions are unanswered.

## Composition with other skills

| Skill | Composition |
|---|---|
| `decision-design-sharpening` | Defer when target IS a decision-record-grade architectural commitment pre-commit; that skill brings formal Round-1 + Round-2 + decomposition trigger structure |
| `pre-implementation-sharpening` | Defer at implementation-start moment; that skill brings operational/runtime-detail surfacing + DR-amendment flow-back |
| `coherence-audit` | Defer when target is a SET of locked decisions; that skill brings 10 universal lenses + corpus-specific lenses |
| Cascade discipline (MAINTENANCE.md) | When sharpening surfaces revisions affecting multiple docs, cascade applies — update affected docs in same commit |
| Source-grounded discipline (`feedback_source_grounded.md`) | Always: cite target content; flag synthesis vs citation |

## Self-validation bias warning

Like the specialized sharpening skills, this one is vulnerable to:

1. **Defending recent content** — sycophancy on user's recent work
2. **Mechanical-compliance findings dominating** — surface findings (typo / phrasing) that feel productive without actually challenging substance
3. **Refining-by-add bias** — easier to suggest additions than cuts
4. **Avoiding the load-bearing questions** — "what's wrong with the substance?" is harder than "what could be added?"

**Counter-mechanism**: every sharpen pass MUST produce at least one of:
- A KEEP position with rationale (explicit "this is solid because X")
- A REVISE position with specific revision
- A CUT position with rationale

If pass produces only "looks good" or only addition-suggestions, self-validation bias triggered. Force re-engagement with cut-questions: what's redundant? what's overclaim? what's decorative? what could be removed without loss?

## Concrete invocation example

```
1. User: "sharpen this draft" / "review this critically" / "what would you cut here"

2. AI activates skill.
   Reads target.
   Applies critical lens.
   Surfaces findings:
   - F1: [load-bearing observation] → REVISE / CUT / KEEP with rationale
   - F2: [overclaim observation] → REVISE with specific suggestion
   - F3: [redundant observation] → CUT with reasoning
   - ...

3. Self-check: STABLE (zero substantive REVISE/CUT findings) or CONTINUE (more gaps to explore)?
   Commit position with cited signal.

4. User: confirms / adjusts / challenges per finding.
   AI applies confirmed positions.

5. (Optional) User signals another round → iterate same procedure with different angle.
```

## Why this skill earns its place (vs ad-hoc critical evaluation)

Without this skill:
- Critical evaluation happens implicitly when user asks
- AI defaults vary by mood / context
- Counter-validation discipline applied inconsistently
- Pareto check skipped / manufactured-criticism not flagged

With this skill:
- Explicit critical-pass discipline (read fully, lens, positions, self-check)
- Counter-validation built into procedure
- Pareto discipline mechanical (every finding gets verdict)
- Stable-vs-continue self-check at end
- Composes cleanly with specialized skills (defer when scope-fit)

The skill applies the spirit of the three specialized skills to everything else — generic `sharpen` is the catch-all sharpening tool.
