---
name: validate-checklist
description: This skill should be used during the structural review layer of any layered review (orchestrator Checkpoint 4.2, layer 1) — checks a document against its doctype-specific required sections, project-data macros, and end-blocks. Triggered when the user asks "structural check", "strukturell prüfen", "validate structure", "Strukturprüfung", "check Festsetzungen", "check required sections", or as part of pre-send validation. NOTE — generic phrases like "review" / "prüfen" route to review-draft (the orchestrator-level review entry), which then delegates here for Layer 1.
version: 0.4.0
license: MIT
mcp_tools_required: [list_doctypes_manifests]
mcp_tools_optional: [search_corpus, read_corpus_file, list_reference_manifests]
fallback_when_mcp_absent: "warn user; degrade to filesystem Read of extensions/{universal,domain/<X>}/doctypes.yaml directly. Reference-fetch enrichment skipped (matches section names only, not the citing references)."
summary: Layer-1 structural review — checks document against doctype-specific required sections, project-data macros, end-blocks. Mostly delegated from review-draft.
routing_mode: delegated
triggers:
  - {phrase: "structural check", lang: en}
  - {phrase: "strukturell prüfen", lang: de}
  - {phrase: "validate structure", lang: en}
  - {phrase: "Strukturprüfung", lang: de}
  - {phrase: "check Festsetzungen", lang: en}
delegated_from: [review-draft]
handoffs: []
phase_role: layer_1
---

# validate-checklist

Specialist skill for doctype-specific structural validation. Runs at
Layer 1 of layered review (structural → fachlich → formal). Per
priority touchpoint refactor (HANDOFF), each checklist hit fetches
the actual reference defining the requirement (when applicable),
not just matches section names. Strengthens the structural layer
by grounding requirements in the laws / leitfäden / methodologies
that define them.

## Load this now

Identify the document's doctype, then load:

1. **Doctype-specific checklist** from `references/checklists/`:
   - `references/checklists/b-plan-begruendung.md`
   - `references/checklists/b-plan-festsetzungen.md`
   - `references/checklists/umweltbericht.md`
   - `references/checklists/gutachten-generic.md` (fallback for any
     Gutachten doctype without its own checklist)

2. **Layered doctypes registry** via `list_doctypes_manifests()` —
   returns the universal + per-active-domain doctype manifest set.
   Each manifest entry declares the doctype's `sections_canonical`,
   `references_required` (laws/leitfäden whose presence in the doc
   defines the requirement), and ownership rules. Required for
   reference-fetch enrichment.

3. **Style spec** at `<repo>/memory/universal/style/style-spec.md` —
   used to validate document class + engine + packages against the
   canonical structural style.

## Doctype identification

In order of preference:

1. **Explicit user designation** — "review the Festsetzungen", "check
   the Umweltbericht".
2. **Path heuristic**:
   - File contains `Begründung` in name → `b-plan-begruendung`
   - File matches `Textteil-B-B-Plan.tex` or path contains
     `Festsetzungen` → `b-plan-festsetzungen`
   - Path contains `Umweltbericht` or `Kapitel_UB` → `umweltbericht`
   - Path contains `Gutachten` or matches Gutachten-class doctype →
     `gutachten-generic`
3. **Content sniff** — `\documentclass{...}` + headings on first page.
4. **Fallback** — ask user.

## When invoked

By orchestrator at Layer 1 of layered review, or by direct user
request. Inputs:

- **Document path** — the .tex file to validate.
- **Project context** (optional) — for `_ai/state.md` data so
  doctype_status and module-decisions can inform what's
  required/optional.

## Behavior

1. **Identify doctype** per above.

2. **Load checklist** from `references/checklists/<doctype>.md` and
   the doctype's manifest entry from `list_doctypes_manifests()`.

3. **Walk the document for structural elements**:
   - Parse `\input{...}` sequence to detect section ordering
     (delegate package/preamble parsing to validate-latex-style; this
     skill is structural, not formal).
   - Read referenced `Projektdaten.tex` for macro definitions.
   - Detect placeholder values matching `---[A-Z\-]+---`.
   - Build the document's actual section list.

4. **Compare against checklist's `sections_canonical`** + the
   doctype manifest's `references_required`. For each required
   section/element:

   a. **Match section name** — present or missing?

   b. **Reference enrichment** (priority touchpoint refactor) —
      if the manifest's `references_required[]` for this
      requirement names a law/leitfaden (e.g. "§9 BauGB defines
      Festsetzungs-types; §9 Abs.1 Nr.20 defines Schutz/Pflege/
      Entwicklung-flächen"), fetch the defining reference via
      `search_corpus(filter={reference_id: <id>})`. Verify the
      requirement actually still exists in the current reference
      text (not just match the section name). Catches:
      - Section is named per old law version; current law moved
        the requirement elsewhere → finding is "section name
        present but cites obsolete §"
      - Required element was repealed → finding upgrades to
        "no longer required by current reference; suggest
        re-evaluation"
      - Required element is new in current reference but the
        doctype's checklist hasn't been updated → log as
        capability-gap T6 trigger to product-backlog

5. **Build severity rollup**:
   - `required_missing[]` — block-level (canonical section absent)
   - `expected_missing[]` — warnings
   - `optional_missing[]` — informational
   - `unfilled_placeholders[]` — macro values matching `---X---`
   - `cross_check_failures[]` — `\cite`/`\ref`/`\input` without
     matching target
   - `reference_drift[]` — section name present but citing reference
     has drifted; surface for review (NEW per priority refactor)
   - `requirement_obsolete[]` — section required by checklist no
     longer exists in current reference; surface for re-evaluation
     (NEW)

6. **Surface findings** with line numbers + spec/reference references.
   Each finding: `{severity, location, rule, message, defining_reference?}`.

7. **Block layered review progression** on any `required_missing` item.

## Output

```
Required missing (BLOCK):
  - L42: Section "Geltungsbereich" not found
    (b-plan-begruendung.md §canonical-sections; defining ref: §9
     Abs.1 BauGB requires Geltungsbereichs-Festlegung)
  - Projektdaten.tex: \BPlanName not defined
    (b-plan-begruendung.md §required-macros)

Reference drift (REVIEW):
  - L168: Section "Bodenschutz" present but cites BBodSchG
    pre-2023 amendment; current §s reorganized.
    Verify content still matches current §11-13 BBodSchG.

Expected missing (WARN):
  - L168: Section "Bodenschutz" content sparse
  - L4: \listoffigures not loaded (recommended for begruendung)

Unfilled placeholders:
  - Projektdaten.tex L4: \Ortsteil = "---ORTSTEIL---"

Cross-check failures:
  - L201: \cite{Suedbeck2005} not in Quellenverzeichnis
```

End with one-line verdict: `BLOCK / WARN / PASS` based on highest
severity present.

## Edge cases

- **Document doesn't compile** (LaTeX errors): pre-condition check.
  If compile failed (orchestrator's compile gate), structural review
  doesn't make sense yet. Refuse to validate; refer back to fixing
  compile errors first.
- **Doctype unknown after all heuristics**: ask user. Don't guess.
- **Project's `state.md.doctype_status` says doctype is
  `not-applicable`**: warn the user — they're trying to validate
  something they declared out-of-scope. Confirm intent.
- **Doctype manifest entry missing for the identified doctype**: the
  doctypes manifest hasn't been populated for this doctype yet.
  Surface as T6 capability gap; fall back to checklist-only
  validation (no reference enrichment). Suggest running
  `author-manifest` to add the entry.
- **References corpus empty** (newly-deployed office, research-
  references not yet run): reference enrichment unavailable. Fall
  back to checklist-only validation. Recommend running
  research-references first for full validation.
- **Multiple `\documentclass` or conflicting settings**: surface as
  block-level "document is malformed" finding.

## Tools used

- `list_doctypes_manifests(scope_filter=true)` (MCP, required) —
  layered doctype registry per office's scope.
- `search_corpus(query, filter)` (MCP, optional) — fetch defining
  references for the priority-refactor reference-enrichment step.
- `read_corpus_file(path)` (MCP, optional) — read full reference
  text when fuzzy-match suggests drift.
- `list_reference_manifests(scope_filter=true)` (MCP, optional) —
  cross-reference for "is this reference even tracked in our
  manifests?"
- `Read` — document and Projektdaten.tex.
- `Grep` — find references to macros, citations, labels.
- `Glob` — locate Textbausteine and project files.

When MCP backend unreachable: fall back to direct filesystem reads
of `extensions/{universal,domain/<X>}/doctypes.yaml`. Reference-
enrichment step skipped; degrades to section-name matching only.
Warn user.
