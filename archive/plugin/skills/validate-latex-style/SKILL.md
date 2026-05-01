---
name: validate-latex-style
description: This skill should be used during the formal review layer of any layered review (orchestrator Checkpoint 4.2, layer 3) — diffs a LaTeX document's preamble and structural choices against the canonical style-spec.md plus any per-active-domain office-style overlays. Triggered by user phrases like "style check", "spec-Abweichung", "validate style", "stilprüfung", or as part of pre-send formal review.
version: 0.5.0
license: MIT
mcp_tools_required: []
mcp_tools_optional: []
fallback_when_mcp_absent: "skill operates entirely on filesystem reads of contract-free files (style-spec.md prose + LaTeX source + per-domain overlay files). Office-config is loaded by the orchestrator before delegating here — this skill consumes the already-validated `scope.domains` for overlay enumeration. No contract-bearing reads of its own — no fail-closed concern."
summary: Layer-3 formal review — diffs LaTeX preamble + structural choices against canonical style-spec.md plus per-domain office-style overlays.
routing_mode: delegated
triggers:
  - style check
  - validate LaTeX style
  - Stilprüfung        # German technical anchor
delegated_from: [review-draft]
handoffs: []
phase_role: layer_3
---

# validate-latex-style

Specialist skill for formal LaTeX style validation. Compares
document preamble + structural choices against
`<repo>/memory/universal/style/style-spec.md` (universal
structural style — KOMA scrreprt for Begründung, article for
Festsetzungen, etc.) PLUS the office's layered office-style
stack:

- `office_config.templates.office_style_dir/office-style.default.sty` —
  base office styling
- `office_config.templates.office_style_dir/office-style.<DOMAIN>.sty` —
  per-active-domain overlays (e.g. `office-style.PV-FFA.sty`,
  `office-style.Wind.sty`) for each domain in
  `office_config.scope.domains` that has its own overlay file

Surfaces deviations against both the structural baseline (style-spec)
and the office-specific stack.

## Load this now

Read `<repo>/memory/universal/style/style-spec.md` to know the
canonical universal structural style for both doctypes
(Begründung scrreprt + Festsetzungen article).

Read `<repo>/memory/universal/conventions/korrektur-rules.md`
for the writing conventions (German quotes, non-breaking spaces,
German number formatting, hyphenation hints, source line wrap).

Enumerate the office's office-style stack from
`office_config.templates.office_style_dir`. Per office's
`scope.domains`, check for per-domain overlay files
(`office-style.<DOMAIN>.sty`). The active stack is:

1. `office-style.default.sty` (base)
2. `office-style.<DOMAIN>.sty` for each `<DOMAIN>` in
   `scope.domains` (in scope.domains order)

This skill's role is to validate the document against both the
universal structural style AND the active office-style stack.
Universal structural deviations are universal-spec violations;
office-style deviations point at specific overlay files for
remediation.

## When invoked

By orchestrator at Layer 3 of layered review (formal), or by
direct user request.

Inputs:

- **Document path** — the .tex file to validate.
- **Doctype** (optional) — explicit. If absent, identified by
  file name + content sniff.

## Behavior

1. **Identify doctype** — `b-plan-begruendung` (scrreprt) or
   `b-plan-festsetzungen` (article infinite-page). Other
   doctypes use the closest matching style profile.

2. **Parse document preamble**:
   - `\documentclass[opts]{class}` — class name + options
   - `\usepackage[opts]{pkg}` — every loaded package
   - `\geometry{...}` — paper, textwidth, margins
   - `\setmainfont{...}` (xelatex) or default (pdflatex)
   - `\sisetup{...}` — siunitx config
   - `\titleformat{...}` (festsetzungen) — heading sizes
   - Header/footer config (scrlayer-scrpage `\ihead`/`\ohead`
     or fancyhdr `\lhead`/`\rhead`)
   - `\hyphenpenalty`, `\exhyphenpenalty`, `\widowpenalty`,
     `\clubpenalty` — penalty values
   - `\renewcommand{\familydefault}{...}` — sans/serif override
   - Magic comments at top (`% !TeX program`, `% !TeX root`)
   - `\usepackage{office-style.<DOMAIN>}` or equivalent —
     overlay loads (validate against active stack)

3. **Compare against universal style-spec.md** for the doctype:
   - Document class match.
   - Engine match (pdflatex, never xelatex per spec).
   - Required packages all present.
   - Forbidden packages absent.
   - Number-formatting siunitx config matches.
   - Header text correct.
   - Penalty values match (if spec specifies).
   - Magic comments correct (especially `% !TeX root` not stale).

4. **Compare against office-style stack** (NEW per
   alignment-sweep):
   - Base office style loaded? (`office-style.default.sty`)
   - For each active domain, expected overlay loaded? (e.g.
     project tagged for PV-FFA work should load
     `office-style.PV-FFA.sty`)
   - Geometry values match the office overlay (overlay can
     legitimately override universal defaults).
   - Office-specific commands (`\OfficeName`, `\OfficeAddressLines`,
     `\OfficeSigner`) auto-generated correctly per
     ARCHITECTURE.md meta-rule 1 — don't hand-write these.
   - Surface "office-overlay missing for active domain" as a
     warning (project may legitimately not need that domain's
     styling, but flag).

5. **Body-level style checks** (optional but useful):
   - German quotes: `\glqq...\grqq{}`, never `"..."`.
   - Non-breaking spaces: `~` before units (`5~m`, `30,37~ha`),
     before `§` (`§~9 BauGB`).
   - Number format in prose: comma decimal, dot thousands.
   - No hardcoded Windows paths (`D:\\...`).

6. **Build finding list** with file:line citations:
   - `style-mismatch` — value differs from universal spec
   - `missing-required-package` — required pkg not loaded
   - `unauthorized-package` — pkg loaded but not in spec
   - `header-mismatch` — wrong doctype tag
   - `convention-violation` — body-level korrektur rule
     violated
   - `magic-comment-stale` — `% !TeX root` points at wrong
     file
   - `office-overlay-missing` — expected per-active-domain
     overlay not loaded (NEW)
   - `office-overlay-conflict` — overlay overrides universal
     in a way that violates structural spec (NEW)

7. **Return rolled-up findings** with severity:
   - `high` — block (engine mismatch, missing required
     package, class mismatch)
   - `medium` — warn (geometry off by small amount, missing
     optional package, magic-comment stale, office-overlay
     missing)
   - `low` — informational (convention violation, unfilled
     placeholder in macro)

## Output

Compact finding list:

```
HIGH:
  - L3: \documentclass{article} but doctype is
        b-plan-begruendung; expected scrreprt
        (style-spec.md §doctype-A)

MEDIUM:
  - L18: geometry textwidth=6.5in; expected
         25mm/25mm/30mm/25mm
  - L1: % !TeX root points at non-existent file
  - office-overlay-missing: project tagged for Wind domain;
    office-style.Wind.sty not loaded

LOW:
  - L142: "Regiosaatgut" should be \glqq Regiosaatgut\grqq{}
  - L155: "5 m" should be "5~m"
```

End with one-line verdict: `BLOCK / WARN / PASS`.

## Edge cases

- **Mixed-engine indicators**: `\setmainfont` + `pdflatex`
  magic comment. Surface as conflict; ask which is intended.
- **Custom macros that look like packages**: don't false-flag
  user-defined commands as unauthorized.
- **Unicode characters in source** that pdflatex can't handle:
  detect and surface as encoding issue.
- **Doctype unknown**: ask user before validating against
  wrong spec.
- **Office has no per-domain overlays at all** (e.g.
  newly-deployed office hasn't customized): no
  office-overlay-missing warnings; document only validated
  against universal style-spec + office-style.default.sty.
- **Document loads an overlay for a domain not in
  office.scope.domains** (e.g. someone manually included
  `office-style.Wind.sty` but Wind isn't in scope): surface
  as `office-overlay-conflict` — either the project's scope
  is wrong or the overlay shouldn't be there.

## Tools used

- `Read` — document and preamble files; office-style stack
  files.
- `Grep` — find specific style markers across the doc.
- Office-config values (in-memory; loaded by orchestrator)
  for `templates.office_style_dir` + `scope.domains`.
- No MCP backend dependency. Pure document parsing + filesystem.

When MCP backend unreachable: skill is unaffected (no MCP
dependencies). Office-config is loaded by orchestrator at
session-open and held in-memory; this skill reads from there.
