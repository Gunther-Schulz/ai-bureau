---
name: validate-checklist
description: This skill should be used during the structural review layer of any layered review (orchestrator Checkpoint 4.2, layer 1) — checks a document against its doctype-specific required sections, project-data macros, and end-blocks. Triggered when the user asks to "review", "prüfen", "structural check", "strukturell prüfen", or as part of pre-send validation.
version: 0.1.0
license: MIT
---

# validate-checklist

Specialist skill for doctype-specific structural validation. Runs at
Layer 1 of layered review (structural → fachlich → formal).

## Load this now

Read the relevant doctype checklist from `references/checklists/`:

- `references/checklists/b-plan-begruendung.md`
- `references/checklists/b-plan-festsetzungen.md`
- `references/checklists/umweltbericht.md`
- `references/checklists/gutachten-generic.md` (fallback for any
  Gutachten doctype without its own checklist)

Select based on the document's detected doctype (from path, content
heuristics, or explicit user designation).

## When invoked

By orchestrator at Layer 1 of layered review, or by direct user
request like "structural check", "prüfe Struktur".

## Behavior

1. Identify doctype.
2. Load corresponding checklist from `references/checklists/`.
3. Walk the document:
   - Document class + engine + packages match style-spec.md
   - Required sections present in order
   - Required project-data macros defined and filled
   - Required end-blocks present
   - Headers / footers / number formatting per spec
   - Cross-checks (cite refs, label refs, input refs)
4. Build severity rollup:
   - `required_missing` — block-level
   - `expected_missing` — warning
   - `optional_missing` — informational
   - `unfilled_placeholders` — `---X---` patterns in macros
   - `header_mismatch` — wrong doctype tag in headers
   - `package_violations` — vs style-spec
5. Surface findings with line numbers + spec references.
6. Block layered review progression on any `required_missing`.

## Status

v0.1: stub. Checklists are complete; behavior implementation follows
when document parsing utilities land.
