---
discipline: 1
title: Source-grounded; cite file:line; flag synthesis vs citation
when_fires: Asserting what a doc / DR / architectural commitment says; starting substantive work; invoking a specialized skill or profile-anchored validation
load_on_demand: true
---

# Discipline 1 — Source-grounded; cite file:line; flag synthesis vs citation

Before asserting what a doc / DR / architectural commitment says, read the source. Cite specific `file:line` when applicable. Flag synthesis vs citation distinctly. Calibrate confidence by basis:

- "Per `<file>:<line>`, X" → high confidence (direct citation)
- "From HANDOFF/MEMORY summary, X" → medium confidence (flag explicitly)
- "Pattern-matched / inferred / my synthesis" → low confidence (flag explicitly)

Pattern-matching from HANDOFF prose, memory summaries, or prior-conversation knowledge is **NOT direct evidence** per global `~/.claude/CLAUDE.md` honesty-about-sources rule. The temptation to skip source-reading because "I remember roughly what it said" is the failure mode; cost-bias is legitimate sometimes (stating a quick recollection is fine when flagged), but honesty about basis is the rule.

**Discriminator**: am I citing or synthesizing? If I can name file:line with confidence, citing. Otherwise synthesizing (flag explicitly).

**Common failure surfaces**: malformed schema examples without verifying schema; over-confident defense of locked decisions without reading source DR; attribution of quotes to wrong source files. Common mechanism: pattern-matching from inherited summaries / conventions / prior framings instead of testing against current goal.

## Re-grounding in VISION + ARCHITECTURE for substantive work

For any substantive session work in pbs-bureau (architectural decisions, design discussions, commitment design, DR authorship, strategic positioning), READ `VISION.md` + `ARCHITECTURE.md` alongside `HANDOFF.md` before substantive work. Without VISION re-grounding, AI drifts toward oracle-mode or validator-mode framings (per Vivienne Ming research: only sparring-mode produces value rivaling human+AI hybrid). Without ARCHITECTURE in context, proposals re-suggest already-discarded patterns.

**Re-grounding mid-session is valid** when you notice your own framing has drifted toward easy answers, or you've forgotten which architectural discipline applies, or the user pushes back on an answer that suggests oracle-mode drift.

## Skill + profile files are a first-class source class

When invoking a sharpening / audit / validation skill (`decision-design-sharpening`, `pre-implementation-sharpening`, `coherence-audit`, `sharpen`), READ the SKILL.md file via Read tool at the moment of invocation — every time, regardless of prior usage in same session. Same for `profiles/*.md` when profile-anchored validation triggers (READ `profiles/INDEX.md` + ≥3 representative cluster members).

Skills + profiles evolve frequently (decision-design-sharpening went v0.4.0 → v0.6.0 across a single session); compaction collapses prior Read content into synthesis-summaries; fresh sessions have no breadcrumbs at all. Pattern-matching memory of prior usage misses load-bearing discipline elements.

**Verification (proves Read happened, not pattern-matched)**: chat output cites specific skill section names (e.g., "per layered coverage observation"; "per Lens 8") + specific profile content (not just cluster letters A/B/C/D). Without these citations, the procedure was pattern-matched, not executed.

**Canonical failure mode**: substrate Round 1 post-compact applied `decision-design-sharpening` from synthesized memory; missed layered coverage observation; phase-routed cross-cutting concerns to a later phase too aggressively; user had to force re-Read; Round 2 then surfaced 11 EXPANSIONS that should have been visible at Round 2 design.
