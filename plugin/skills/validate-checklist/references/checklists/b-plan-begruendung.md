# B-Plan Begründung — required structure

Validation rules for a Begründung document. Each rule has a severity:

- **REQUIRED** — must be present; missing = block.
- **EXPECTED** — should be present; missing = warning.
- **OPTIONAL** — context-dependent; presence/absence informational.

## Document class and engine

| Rule | Severity |
|---|---|
| `\documentclass[...]{scrreprt}` | REQUIRED |
| Engine = pdflatex (no `\setmainfont` from fontspec) | REQUIRED |
| `babel` loaded with `[ngerman]` | REQUIRED |
| `inputenc` with utf8 + `fontenc` with T1 + `ae`/`aecompl` | REQUIRED |
| Magic comment `% !TeX program = pdflatex` | EXPECTED |
| Magic comment `% !TeX root = <master>.tex` correct (not stale) | EXPECTED |

## Master assembly structure

The master `.tex` file must:

| Rule | Severity |
|---|---|
| Load `preamble.tex` and `Projektdaten.tex` via `\input{}` | REQUIRED |
| Begin prelims with `\startroman` + `\pagestyle{tocstyle}` | REQUIRED |
| Include Titelseite via `\input{Textbausteine/Titelseite.tex}` | REQUIRED |
| Include `\tableofcontents` | REQUIRED |
| Include `\listoftables` (after TOC) | EXPECTED |
| Include `\listoffigures` | OPTIONAL |
| Switch to body via `\startarabic` + `\pagestyle{scrheadings}` | REQUIRED |

## Required sections (canonical order)

The master file must `\input{Textbausteine/<file>.tex}` each of these
in order. Project-specific extras allowed.

| # | Section | Severity | Notes |
|---|---|---|---|
| 1 | Titelseite | REQUIRED | rendered as separate file |
| 2 | Aufgaben und Inhalte der Planung | REQUIRED | |
| 3 | Grundlagen der Planung — Aufstellungsverfahren | REQUIRED | |
| 4 | Geltungsbereich | REQUIRED | must reference `\GeltungsbereichHa` |
| 5 | Planinhalte und Festsetzungen | REQUIRED | mirrors Festsetzungen content in narrative |
| 6 | Ver- und Entsorgungsanlagen | REQUIRED | |
| 7 | Vorbeugender Brandschutz — Löschwasserversorgung | REQUIRED for solar/PV | conditional on `solar` tag |
| 8 | Gewässerschutz | EXPECTED | required if water-relevant |
| 9 | Bodenschutz | EXPECTED | required almost always |
| 10 | Immissions- und Klimaschutz — Blendwirkung | REQUIRED for solar/PV | conditional |
| 11 | Altlasten und Altlastverdachtsflächen | EXPECTED | |
| 12 | Belange der Forst | OPTIONAL | required only if Wald tangential |
| 13 | Denkmalschutz | OPTIONAL | required only if Denkmäler im Gebiet |
| 14 | Kataster- und Vermessungswesen | EXPECTED | |
| 15 | Alternativprüfung | REQUIRED | filename: `Alternativpüfung` (sic — typo in Friedrichshof template) |
| 16 | Kosten und Finanzierung | EXPECTED | |
| 17 | Signatur | REQUIRED | Unterschriftsblock |

## Required project-data macros (`Projektdaten.tex`)

Empty or placeholder values (e.g. `---ORTSTEIL---`) flagged as
unfilled.

| Macro | Severity | Used in |
|---|---|---|
| `\Gemeinde` | REQUIRED | header, prose |
| `\Stadt` | OPTIONAL | only when Gemeinde+Stadt distinction matters |
| `\Gemarkung` | REQUIRED | prose |
| `\Ortsteil` | REQUIRED | header, prose |
| `\Landkreis` | REQUIRED | prose |
| `\BPlanAbrv` | REQUIRED | abbreviated B-Plan reference |
| `\BPlanNr` | REQUIRED | numbered B-Plan |
| `\BPlanName` | REQUIRED | name-only form |
| `\BPlan` | REQUIRED | lowercase-leading prose form |
| `\BPlanTyp` | REQUIRED | capitalized-leading form (sentence start) |
| `\GeltungsbereichHa` | REQUIRED | numeric ha value |
| `\GeltungsbereichHaSolar` | REQUIRED for solar | tagged `solar` |
| `\Planungsregion` | REQUIRED | RREP context |

Placeholder pattern: any value matching `---[A-Z\-]+---` is unfilled.

## Required end-blocks

The Begründung body, after the last `\input{Textbausteine/Signatur.tex}`,
should not have additional `\input` lines. The Signatur baustein must
contain:

- Office identity (Planungsbüro Schulz / Schwerin)
- Signature line for Bearbeiter
- Date / Ort signature block

## Header validation (preamble)

`scrlayer-scrpage` config must include:

- `\ihead{...}` with `\Gemeinde` AND (`\BPlanTyp` OR `\BPlan`)
- `\ohead{...}` with literal `Begründung` AND `Seite \thepage`
- `\renewcommand*{\chapterpagestyle}{tocstyle}` for prelim consistency

If `\ohead` says `Festsetzungen` instead of `Begründung`, that's a
template-copy error (high-severity flag).

## Number formatting (siunitx)

`siunitx` must be loaded with German conventions:

```latex
\sisetup{
  output-decimal-marker={,},
  group-separator={.},
  group-minimum-digits=4
}
```

Differences flagged.

## Quellenverzeichnis

OPTIONAL but EXPECTED. If a sources section exists (typically last
section before Signatur), it should:

- List BauGB, BauNVO, BNatSchG, NatSchAG-MV, LBauO-MV at minimum
- Include current amendment dates (cross-checked by verify-citations)
- Cite leitfäden actually used in the document

## Cross-checks

- Every `\cite{...}` resolves to a Quellenverzeichnis entry.
- Every `\ref{fig:...}` and `\ref{tab:...}` has a matching `\label`.
- Every `\input{Textbausteine/<file>.tex}` resolves to an existing file.

## Severity rollup

```yaml
required_missing: []                       # block-level
expected_missing: []                       # warnings
optional_missing: []                       # informational
unfilled_placeholders: []                  # macro values matching ---X---
header_mismatch: null                      # if \ohead says wrong doctype
package_violations: []                     # vs style-spec
```

Block on any `required_missing`. Warn on `expected_missing`. Inform
on the rest.
