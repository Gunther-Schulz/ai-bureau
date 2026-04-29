---
name: review-draft
description: This skill should be used when the user asks to review a drafted document — Begründung, Festsetzungen, Umweltbericht, or Gutachten. Triggered by phrases like "review draft", "prüfe das", "Begründung durchgehen", "structural + fachlich + formal", "korrigieren", "Lektorat", "schau mal drüber". Phase B entry skill — runs the layered review framework after Phase A drafting completes.
version: 0.2.0
license: MIT
mcp_tools_required: [compile_latex]
mcp_tools_optional: [list_doctypes_manifests, search_corpus, list_reference_manifests]
fallback_when_mcp_absent: "warn user; degrade to Bash latexmk for compile. Layered review delegations (validate-checklist, validate-latex-style, verify-citations) each have their own fallback paths."
---

# review-draft

Specialist skill for layered document review (Phase B per
orchestrator framework). Three layers run in strict order:
structural → fachlich → formal. Each layer surfaces findings;
user decides per finding before next layer starts. The skill
itself orchestrates; specialist delegates do the per-layer work
and bring their own scope-aware MCP tool dependencies.

## Load this now

Read `PROCEDURE.md` from this skill's directory for the layered
review workflow with per-layer detail.

While operating, hold these references loaded:

- `<repo>/memory/universal/conventions/korrektur-rules.md` —
  formal-layer writing conventions.
- `<repo>/plugin/skills/validate-checklist/SKILL.md` — layer 1
  delegation target; declares its own
  `mcp_tools_required: [list_doctypes_manifests]`.
- `<repo>/plugin/skills/validate-latex-style/SKILL.md` — layer
  3 delegation target.
- `<repo>/plugin/skills/verify-citations/SKILL.md` — layer 2 +
  3 delegation target; declares its own
  `mcp_tools_required: [search_corpus,
  list_reference_manifests]`.

This skill's MCP requirements are minimal (`compile_latex` for
the precondition check); the heavy lifting is in the delegated
specialists.

## When invoked

By orchestrator (Phase B entry) or direct user request. Inputs:

- **Document path** — what to review.
- **Doctype** (optional; identified by path/content if absent).
- **Project context** — state.md, decisions.md,
  module-decisions.md.
- **Source materials** (optional) — for fachlich layer to
  cross-check claims against inputs.

## Behavior

1. **Pre-condition: compile gate**.
   - Run `compile_latex(project_path)` first. If compile
     fails, refuse to review; fixing compile errors comes
     first (orchestrator Compile Gate 4.1).

2. **Layer 1 — Structural** (delegate to `validate-checklist`).
   - Identifies doctype, loads checklist + doctype manifest
     entry (via `list_doctypes_manifests`), walks document for
     required sections / macros / end-blocks / cross-checks.
     Per-priority-touchpoint refactor: also fetches the actual
     defining reference for each requirement and surfaces
     drift if section name OK but cite has aged.
   - Surfaces severity-rolled findings.
   - **Block on `required_missing`**. User authorizes fix-now
     or defer-with-reason before next layer.

3. **Layer 2 — Fachlich** (manual + delegate verify-citations).
   - For each section: check claims against source materials,
     argument internal consistency, completeness vs project
     context. Use `search_corpus` for cross-reference grounding
     where relevant.
   - Source-grounding guard: every legal citation must come
     from a tool result (delegate to `verify-citations`,
     which iterates per-citation per its priority refactor).
   - Apply A/B/C taxonomy from transcript:
     - A: Fachlich-inhaltlich offene Punkte (substantive
       content gaps)
     - B: Formal-strukturelle Punkte — pulled into Layer 3
     - C: Juristisch kritische Kernstellen (mark for extra
       scrutiny)
   - Findings deepen: each finding traces implications to
     adjacent sections.

4. **Layer 3 — Formal** (delegate to `validate-latex-style` +
   `verify-citations`).
   - Style-spec compliance per layered office-style stack
     (canonical universal style + per-active-domain overlays
     like `office-style.PV-FFA.sty`, `office-style.Wind.sty`).
   - Korrektur-rules adherence (German quotes, non-breaking
     spaces, German number formatting).
   - Citation freshness (verify-citations iterative resolution).
   - Section-level edits encouraged (orchestrator Validation
     7.3); avoid whole-document Write.

5. **Between layers**: pause for user confirmation ("Layer 1
   done, 3 required-missing fixed, 2 expected-missing deferred.
   Proceed to Layer 2 fachlich?"). Don't bundle findings
   across layers.

6. **Per finding**:
   - Surface with location + spec reference + severity.
   - User decides: fix-now / defer-to-after-review /
     accept-with-reasoning / drop.
   - For fix-now: apply edit (section-level via Edit, not
     whole-document Write).
   - Log significant decisions to `_ai/decisions.md`.

## Output

Per-layer summary:

```
Layer 1 — Structural validation:
  3 required missing → all fixed
  2 expected missing → deferred (logged in decisions.md)
  1 unfilled placeholder → fixed
  1 reference_drift (NEW per priority refactor) → user
    decided to update cite to current amendment
  PASS at level 1.

Layer 2 — Fachlich review:
  A. 5 substantive findings:
     - A1: FFH-Vorprüfung fehlt (kritisch) → user decided
            rhetorical handling, decisions.md updated
     - A2: §45 Nr.5 argumentation needs §1a-Erweiterung →
            fixed (verify-citations iteration confirmed
            current amendment)
     - A3-A5: minor wording → fixed
  C. 1 juristisch critical → marked for external/Opus review.

Layer 3 — Formal review:
  Style-spec: 1 minor (header text mismatch) → fixed.
              Per-domain overlay (office-style.PV-FFA.sty)
              checked: clean.
  Citations: BNatSchG drift detected (verify-citations
             iteration: defining chapter unchanged; only
             amendment-form lag) → updated.
  Korrektur-rules: 4 quote-mark fixes, 6 non-breaking-space
                   fixes → all batched + applied.
  PASS at level 3.

Review complete. Document at <path>. Compile passes. Ready for
Phase C (finalization)?
```

## Edge cases

- **Compile fails on entry**: refuse review; fix compile first.
- **Document is a draft so incomplete that Layer 1 fails
  massively**: surface — Layer 1 won't pass; suggest more
  drafting work first before review.
- **User wants to skip a layer**: discouraged but allowed with
  explicit acknowledgment. Skip-record logged in
  `_ai/decisions.md`.
- **A finding spans layers** (e.g. "missing §45 argumentation
  section is both structural and fachlich"): surface in Layer
  1 (structural) but cross-reference Layer 2 implications.
- **Document's doctype not in any manifest** (newly-deployed
  office or doctype not yet registered): validate-checklist
  surfaces as T6 capability gap; review still possible at
  reduced rigor.

## Tools used

- `compile_latex(project_path)` (MCP, required) — precondition
  + after edits.
- `list_doctypes_manifests(scope_filter=true)` (MCP, optional)
  — used implicitly via validate-checklist delegation; loaded
  here for cross-referencing doctype context.
- `search_corpus(query, filter)` (MCP, optional) — Layer 2
  fachlich cross-reference grounding.
- `list_reference_manifests(scope_filter=true)` (MCP, optional)
  — for citation context across delegated specialists.
- `Read` — document + cross-references.
- `Edit` — section-level edits (NOT whole-document Write).
- Delegations to `validate-checklist`,
  `validate-latex-style`, `verify-citations` (each declares
  its own MCP requirements).

When MCP backend unreachable: fall back to `Bash latexmk` for
compile. Layered review delegations each have their own
fallback paths; review still functions but recall + grounding
worse without semantic search.
