---
name: review-draft
description: This skill should be used when the user asks to review a drafted document — Begründung, Festsetzungen, Umweltbericht, or Gutachten. Triggered by phrases like "review draft", "prüfe das", "Begründung durchgehen", "structural + fachlich + formal", "korrigieren", "Lektorat", "schau mal drüber". Phase B entry skill — runs the layered review framework after Phase A drafting completes.
version: 0.1.0
license: MIT
---

# review-draft

Specialist skill for layered document review (Phase B per orchestrator
framework). Three layers run in strict order: structural →
fachlich → formal. Each layer surfaces findings; user decides per
finding before next layer starts.

## Load this now

Read `PROCEDURE.md` from this skill's directory for the layered
review workflow with per-layer detail.

While operating, hold these references loaded:

- `<repo>/memory/domain/conventions/korrektur-rules.md` — formal-layer
  writing conventions.
- `<repo>/plugin/skills/validate-checklist/SKILL.md` — layer 1
  delegation target.
- `<repo>/plugin/skills/validate-latex-style/SKILL.md` — layer 3
  delegation target.
- `<repo>/plugin/skills/verify-citations/SKILL.md` — layer 2 + 3
  delegation target.

## When invoked

By orchestrator (Phase B entry) or direct user request. Inputs:

- **Document path** — what to review.
- **Doctype** (optional; identified by path/content if absent).
- **Project context** — state.md, decisions.md, module-decisions.md.
- **Source materials** (optional) — for fachlich layer to cross-
  check claims against inputs.

## Behavior

1. **Pre-condition: compile gate**.
   - Run compile_latex first. If compile fails, refuse to review;
     fixing compile errors comes first (orchestrator Compile Gate
     4.1).

2. **Layer 1 — Structural** (delegate to `validate-checklist`).
   - Identifies doctype, loads checklist, walks document for
     required sections / macros / end-blocks / cross-checks.
   - Surfaces severity-rolled findings.
   - **Block on `required_missing`**. User authorizes fix-now or
     defer-with-reason before next layer.

3. **Layer 2 — Fachlich** (manual + delegate verify-citations).
   - For each section: check claims against source materials,
     argument internal consistency, completeness vs project context.
   - Source-grounding guard: every legal citation must come from
     RAG hit (delegate to verify-citations).
   - Apply A/B/C taxonomy from transcript:
     - A: Fachlich-inhaltlich offene Punkte (substantive content
       gaps)
     - B: Formal-strukturelle Punkte — pulled into Layer 3
     - C: Juristisch kritische Kernstellen (mark for extra scrutiny)
   - Findings deepen: each finding traces implications to adjacent
     sections.

4. **Layer 3 — Formal** (delegate to validate-latex-style + verify-
   citations).
   - Style-spec compliance, korrektur-rules adherence, citation
     freshness, packaging, geometry, headers.
   - Section-level edits encouraged (orchestrator Validation 7.3).

5. **Between layers**: pause for user confirmation ("Layer 1 done,
   3 required-missing fixed, 2 expected-missing deferred. Proceed to
   Layer 2 fachlich?"). Don't bundle findings across layers.

6. **Per finding**:
   - Surface with location + spec reference + severity.
   - User decides: fix-now / defer-to-after-review / accept-with-
     reasoning / drop.
   - For fix-now: apply edit (section-level via Edit, not whole-
     document Write).
   - Log significant decisions to `_ai/decisions.md`.

## Output

Per-layer summary:

```
Layer 1 — Structural validation:
  3 required missing → all fixed
  2 expected missing → deferred (logged in decisions.md)
  1 unfilled placeholder → fixed
  PASS at level 1.

Layer 2 — Fachlich review:
  A. 5 substantive findings:
     - A1: FFH-Vorprüfung fehlt (kritisch) → user decided rhetorical
            handling, decisions.md updated
     - A2: §45 Nr.5 argumentation needs §1a-Erweiterung → fixed
     - A3-A5: minor wording → fixed
  C. 1 juristisch critical → marked for external/Opus review.

Layer 3 — Formal review:
  Style-spec: 1 minor (header text mismatch) → fixed
  Citations: BNatSchG drift detected → updated
  Korrektur-rules: 4 quote-mark fixes, 6 non-breaking-space fixes
                   → all batched + applied
  PASS at level 3.

Review complete. Document at <path>. Compile passes. Ready for
Phase C (finalization)?
```

## Edge cases

- **Compile fails on entry**: refuse review; fix compile first.
- **Document is a draft so incomplete that Layer 1 fails massively**:
  surface — Layer 1 won't pass; suggest more drafting work first
  before review.
- **User wants to skip a layer**: discouraged but allowed with
  explicit acknowledgment. Skip-record logged in `_ai/decisions.md`.
- **A finding spans layers** (e.g. "missing §45 argumentation
  section is both structural and fachlich"): surface in Layer 1
  (structural) but cross-reference Layer 2 implications.

## Tools used

- `compile_latex` (precondition + after edits).
- `Read` — document + cross-references.
- `Edit` — section-level edits (NOT whole-document Write).
- Delegations to validate-checklist, validate-latex-style,
  verify-citations.
