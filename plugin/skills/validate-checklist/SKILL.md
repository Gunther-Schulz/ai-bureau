---
name: validate-checklist
description: This skill should be used during the structural review layer of any layered review (orchestrator Checkpoint 4.2, layer 1) — checks a document against its doctype-specific required sections, project-data macros, and end-blocks. Triggered when the user asks to "review", "prüfen", "structural check", "strukturell prüfen", "validate structure", "check Festsetzungen", or as part of pre-send validation.
version: 0.1.0
license: MIT
---

# validate-checklist

Specialist skill for doctype-specific structural validation. Runs at
Layer 1 of layered review (structural → fachlich → formal).

## Load this now

Identify the document's doctype, then read the relevant checklist
from `references/checklists/`:

- `references/checklists/b-plan-begruendung.md`
- `references/checklists/b-plan-festsetzungen.md`
- `references/checklists/umweltbericht.md`
- `references/checklists/gutachten-generic.md` (fallback for any
  Gutachten doctype without its own checklist)

Also load `<repo>/memory/domain/style/style-spec.md` to validate
document class + engine + packages against the canonical style.

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
3. **Content sniff** — `\documentclass{...}` + headings on first
   page.
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
2. **Load checklist** from `references/checklists/`.
3. **Walk the document**:
   - Parse `\documentclass{...}` and options.
   - Parse `\usepackage[opts]{pkg}` lines.
   - Parse `\geometry{...}` settings.
   - Parse `\sisetup{...}` settings (if expected).
   - Parse `scrlayer-scrpage` or `fancyhdr` config (header text).
   - Walk `\input{...}` sequence to detect section ordering.
   - Read referenced `Projektdaten.tex` for macro definitions.
   - Detect placeholder values matching `---[A-Z\-]+---`.
4. **Build severity rollup** per checklist's structure:
   - `required_missing[]` — block-level
   - `expected_missing[]` — warnings
   - `optional_missing[]` — informational
   - `unfilled_placeholders[]` — macro values matching `---X---`
   - `header_mismatch` — if `\ohead` or `\rhead` says wrong doctype
   - `package_violations[]` — vs style-spec.md
   - `cross_check_failures[]` — `\cite`/`\ref`/`\input` without
     matching target
5. **Surface findings** with line numbers + spec references. Each
   finding: `{severity, location, rule, message}`.
6. **Block layered review progression** on any `required_missing`
   item.

## Output

Structured finding list grouped by severity:

```
Required missing (BLOCK):
  - L42: Section "Geltungsbereich" not found (b-plan-begruendung.md §canonical-sections)
  - Projektdaten.tex: \BPlanName not defined (b-plan-begruendung.md §required-macros)

Expected missing (WARN):
  - L168: Section "Bodenschutz" not found
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
- **Multiple `\documentclass` or conflicting settings**: surface as a
  block-level "document is malformed" finding.

## Tools used

- `Read` — document and Projektdaten.tex.
- `Grep` — find references to macros, citations, labels.
- `Glob` — locate Textbausteine and project files.

No MCP backend dependencies. Pure document parsing.
