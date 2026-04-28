# B-Plan Festsetzungen — required structure

The Festsetzungen is the binding-rules document attached to the
B-Plan Satzung as "Teil B Text" (Teil A = Planzeichnung).

Severities: REQUIRED (block), EXPECTED (warn), OPTIONAL (info).

## Document class and engine

| Rule | Severity |
|---|---|
| `\documentclass[12pt]{article}` | REQUIRED |
| Engine = pdflatex | REQUIRED |
| `babel` with `[ngerman]` | REQUIRED |
| Body sans-serif: `\renewcommand{\familydefault}{\sfdefault}` | REQUIRED |
| Geometry: A4 width × ~141cm height (`paperheight=4000pt`), zero margins | REQUIRED |
| `titlesec` loaded for heading customization | REQUIRED |
| `enumitem` loaded for nested enumerate lists | REQUIRED |
| `url` loaded for `\url{}` in Verfahrensvermerke | EXPECTED |
| Pre-declared hyphenation hints for long compounds | EXPECTED |

## Heading style

```latex
\titleformat{\section}{\normalfont\normalsize\bfseries}...
\titleformat{\subsection}{\normalfont\normalsize\bfseries}...
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries}...
```

All heading levels at `\normalsize\bfseries` — no size escalation.
Flag any `\Large`, `\LARGE`, `\Huge` in `\titleformat`.

## Required document sections (in order)

| # | Section | Severity |
|---|---|---|
| 1 | `\textbf{Satzung der Gemeinde \Gemeinde{} über den \BPlan{}}` (header) | REQUIRED |
| 2 | `\subsection*{Präambel}` | REQUIRED |
| 3 | `\subsection*{Teil A: Planzeichnung i. M. 1 : 2.000}` | REQUIRED |
| 4 | `\section*{Teil B Text}` | REQUIRED |
| 5 | `\section*{I.\hspace{17pt} Planungsrechtliche Festsetzungen gemäß §~9 BauGB}` | REQUIRED |
| 6 | (numbered enumerate of rules under section 5) | REQUIRED |
| 7 | `\section*{Verfahrensvermerke}` | REQUIRED |
| 8 | `\section*{Hinweis}` | REQUIRED |
| 9 | (centered title-block of `\begin{center}\textbf{...}\end{center}` lines) | REQUIRED |
| 10 | `\section*{Rechtsgrundlagen}` | REQUIRED |

## Required rules under "Teil B Text"

The numbered enumerate must include AT LEAST these top-level rules.
Order matters for behördentaugliche Lesbarkeit.

| # | Rule title | Severity |
|---|---|---|
| 1 | `\textbf{Art der baulichen Nutzung §~9 Abs. 1 BauGB}` | REQUIRED |
| 2 | `\textbf{Maß der baulichen Nutzung §~9 (1) Nr. 1 BauGB}` | REQUIRED |
| 3 | `\textbf{Flächen und Maßnahmen zum Schutz, zur Pflege und zur Entwicklung von Boden, Natur und Landschaft §~9 Abs. 1 Nr. 20 BauGB}` | REQUIRED |
| 4 | `\textbf{Artenschutzrechtliche Festsetzungen}` | REQUIRED if §44 BNatSchG triggered |
| 5 | `\textbf{Örtliche Bauvorschriften gemäß §~86 Abs. 3 LBauO M-V}` | REQUIRED |

## Required Verfahrensvermerke (13-entry sequence, in order)

Each entry numbered with a tabbing-Block for Ort, Datum, Siegel,
Unterschrift.

| # | Verfahrensvermerk | Severity |
|---|---|---|
| 1 | Aufstellungsbeschluss + Bekanntmachung (amtliches Bekanntmachungsblatt + Internet) | REQUIRED |
| 2 | Beteiligung Raumordnung §17 LPlG | REQUIRED for M-V |
| 3 | Frühzeitige Öffentlichkeitsbeteiligung §3 Abs.1 BauGB | REQUIRED |
| 4 | Frühzeitige Einwohnerinformation (Termin) | EXPECTED |
| 5 | Frühzeitige Behördenbeteiligung §4 Abs.1 BauGB | REQUIRED |
| 6 | Billigungs- und Auslegungsbeschluss | REQUIRED |
| 7 | Auslegung §3 Abs.2 BauGB (mit M-V Bauportal `bplan.geodaten-mv.de`) | REQUIRED |
| 8 | Behördenbeteiligung §4 Abs.2 BauGB | REQUIRED |
| 9 | Ergebnis der Stellungnahmen + Mitteilung | REQUIRED |
| 10 | Katastermäßige Bestätigung Vermesser | REQUIRED |
| 11 | Genehmigung höhere Verwaltungsbehörde | REQUIRED if §10 Abs.2 BauGB greift (Solar-PV almost always) |
| 12 | Ausfertigung | REQUIRED |
| 13 | Bekanntmachung Inkrafttreten + §214 f. BauGB Hinweis | REQUIRED |

Tabbing-Block format:

```latex
\begin{tabbing}
  \hspace{6cm} \= \hspace{4cm} \= \kill
  \Gemeinde{}, \> Siegel \> \hspace{8pt} <Bürgermeister-Name> \\
  \> \> — Bürgermeister —
\end{tabbing}
```

Placeholder dates `................` allowed at draft stage; replaced
with concrete dates pre-Bekanntmachung.

## Required Rechtsgrundlagen (last section)

Minimum required entries (each with full citation including current
amendment date — cross-checked by verify-citations):

- BauGB
- BauNVO
- PlanZV
- KV M-V
- BNatSchG
- NatSchAG M-V
- LBauO M-V

OPTIONAL (include if cited in body): BImSchG, WHG, LWaG M-V,
BBodSchG, BWaldG, DSchG M-V.

## Required project-data macros (`Projektdaten.tex`)

Same set as Begründung. Festsetzungen also requires:

| Macro | Severity | Used in |
|---|---|---|
| `\BPlanName` | REQUIRED | header (`„Solarpark Friedrichshof"`) |
| `\BPlan` | REQUIRED | Präambel and centered title-block |

## Required Hinweis content

Standard Denkmalschutz boilerplate per §11 DSchG M-V. Verbatim text
expected (allowed paraphrase up to 20%):

> Wenn während der Erdarbeiten Funde oder auffällige Bodenverfärbungen
> entdeckt werden, ist gemäß §11 DschGM-V (GVBI. M-V Nr. 1 vom
> 14.01.98, S. 12) die untere Denkmalschutzbehörde zu benachrichtigen
> ...

## Cross-checks

- Every `§N Abs.M` reference in body resolves to a current law text.
- `\Gemeinde`, `\BPlan`, `\BPlanName`, `\BPlanTyp` macros referenced
  in body must be defined in `Projektdaten.tex`.
- Bürgermeister-Name in tabbing-blocks consistent across all 13
  Verfahrensvermerke (no typos / variants).
- Bekanntmachungsblatt name (e.g. „Bützower Landkurier") consistent
  across Verfahrensvermerke 1, 7, 13.

## Severity rollup

Same structure as Begründung. Block on `required_missing`. Specifically:
missing Verfahrensvermerk in the 13-entry sequence is block-level —
UNB will reject the Satzung.
