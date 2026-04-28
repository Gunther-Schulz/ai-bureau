---
name: validate-latex-style
description: This skill should be used during the formal review layer of any layered review (orchestrator Checkpoint 4.2, layer 3) — diffs a LaTeX document's preamble and structural choices against the canonical style-spec.md. Triggered by user phrases like "style check", "spec-Abweichung", "validate style", "stilprüfung", or as part of pre-send formal review.
version: 0.1.0
license: MIT
---

# validate-latex-style

Specialist skill for formal LaTeX style validation. Compares document
preamble + structural choices against `<repo>/memory/domain/style/
style-spec.md` and surfaces deviations.

## Load this now

Read `<repo>/memory/domain/style/style-spec.md` to know the canonical
office style for both doctypes (Begründung scrreprt + Festsetzungen
article).

Also read `<repo>/memory/domain/conventions/korrektur-rules.md` for
the writing conventions (German quotes, non-breaking spaces, German
number formatting, hyphenation hints, source line wrap).

## When invoked

By orchestrator at Layer 3 of layered review (formal), or by direct
user request.

Inputs:
- **Document path** — the .tex file to validate.
- **Doctype** (optional) — explicit. If absent, identified by file
  name + content sniff.

## Behavior

1. **Identify doctype** — `b-plan-begruendung` (scrreprt) or
   `b-plan-festsetzungen` (article infinite-page). Other doctypes use
   the closest matching style profile.

2. **Parse document preamble**:
   - `\documentclass[opts]{class}` — class name + options
   - `\usepackage[opts]{pkg}` — every loaded package
   - `\geometry{...}` — paper, textwidth, margins
   - `\setmainfont{...}` (xelatex) or default (pdflatex)
   - `\sisetup{...}` — siunitx config
   - `\titleformat{...}` (festsetzungen) — heading sizes
   - Header/footer config (scrlayer-scrpage `\ihead`/`\ohead` or
     fancyhdr `\lhead`/`\rhead`)
   - `\hyphenpenalty`, `\exhyphenpenalty`, `\widowpenalty`,
     `\clubpenalty` — penalty values
   - `\renewcommand{\familydefault}{...}` — sans/serif override
   - Magic comments at top (`% !TeX program`, `% !TeX root`)

3. **Compare against style-spec.md** for the doctype:
   - Document class match.
   - Engine match (pdflatex, never xelatex per spec).
   - Required packages all present.
   - Forbidden packages absent.
   - Geometry values match.
   - Number-formatting siunitx config matches.
   - Header text correct (says "Begründung" for begruendung, etc.).
   - Penalty values match (if spec specifies).
   - Magic comments correct (especially `% !TeX root` not stale).

4. **Body-level style checks** (optional but useful):
   - German quotes: `\glqq...\grqq{}`, never `"..."`.
   - Non-breaking spaces: `~` before units (`5~m`, `30,37~ha`),
     before `§` (`§~9 BauGB`).
   - Number format in prose: comma decimal, dot thousands.
   - No hardcoded Windows paths (`D:\\...`).

5. **Build finding list** with file:line citations:
   - `style-mismatch` — value differs from spec
   - `missing-required-package` — required pkg not loaded
   - `unauthorized-package` — pkg loaded but not in spec
   - `header-mismatch` — wrong doctype tag (begruendung header on
     festsetzungen, etc.)
   - `convention-violation` — body-level korrektur rule violated
   - `magic-comment-stale` — `% !TeX root` points at wrong file

6. **Return rolled-up findings** with severity:
   - `high` — block (engine mismatch, missing required package,
     class mismatch)
   - `medium` — warn (geometry off by small amount, missing optional
     package, magic-comment stale)
   - `low` — informational (convention violation, unfilled
     placeholder in macro)

## Output

Compact finding list:

```
HIGH:
  - L3: \documentclass{article} but doctype is b-plan-begruendung;
    expected scrreprt (style-spec.md §doctype-A)

MEDIUM:
  - L18: geometry textwidth=6.5in; expected 25mm/25mm/30mm/25mm
  - L1: % !TeX root points at non-existent file

LOW:
  - L142: "Regiosaatgut" should be \glqq Regiosaatgut\grqq{}
  - L155: "5 m" should be "5~m"
```

End with one-line verdict: `BLOCK / WARN / PASS`.

## Edge cases

- **Mixed-engine indicators**: `\setmainfont` + `pdflatex` magic
  comment. Surface as conflict; ask which is intended.
- **Custom macros that look like packages**: don't false-flag user-
  defined commands as unauthorized.
- **Unicode characters in source** that pdflatex can't handle: detect
  and surface as encoding issue.
- **Doctype unknown**: ask user before validating against wrong spec.

## Tools used

- `Read` — document and preamble files.
- `Grep` — find specific style markers across the doc.
- No MCP backend dependency. Pure document parsing.
