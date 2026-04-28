---
name: style-spec
description: Canonical LaTeX style specification for Planungsbüro Schulz
  documents. Two distinct toolchains exist (B-Plan Textteil vs PBS-Bericht);
  this file documents both, when to use each, and the conventions shared
  between them. Drafted from canonical templates in
  Vorlagen/Latex/22-16 Maxsolar - Friedrichshof/Textteil-C/ and
  Vorlagen/Latex/Bericht - PBS/.
type: domain
---

# LaTeX style specification

The office uses **two distinct LaTeX toolchains** depending on document type.
They diverge in engine, document class, font, and structure. They are NOT
interchangeable — picking the wrong one breaks compilation.

| Style | Engine | Class | Doctypes | Source of truth |
|---|---|---|---|---|
| **A: B-Plan Textteil** | `xelatex` | `article` | b-plan-begruendung (Textteil B), b-plan-festsetzungen (Textteil C) | `Vorlagen/Latex/22-16 Maxsolar - Friedrichshof/Textteil-C/` |
| **B: PBS-Bericht** | `pdflatex` | `scrreprt` | umweltbericht, artenschutz, andere Gutachten/Berichte | `Vorlagen/Latex/Bericht - PBS/` |

When drafting, the orchestrator picks the style by doctype. New document types
may need a new style; never silently mix.

---

## Style A — B-Plan Textteil (xelatex / article / Verdana)

### Magic comments (top of master .tex file)
```
% !TeX root = Textteil-C.tex
% !TeX program = xelatex
```
These are editor hints (TeXShop/VSCode-LaTeX-Workshop). Required for the
editor to know which engine to call and which file is the master. Must
appear in every master file.

### Document class & engine
```latex
\documentclass{article}
\input{preamble.tex}
```
Engine: **xelatex** (NOT pdflatex). Reason: native font support via
`fontspec`, used to set Verdana.

### Font
```latex
\usepackage{fontspec}
\setmainfont{Verdana}
```
Verdana is the active choice (Helvetica / Arial / Palatino are commented-out
alternates kept in source for reference). System must have Verdana installed.

### Geometry
```latex
\usepackage[a4paper, textwidth=7in, top=20mm, bottom=20mm]{geometry}
```
- A4 paper
- textwidth = 7in (~17.78 cm; remaining ~3.22 cm split between left/right
  margins, ~1.6 cm each side — narrow)
- top/bottom = 20 mm

### Spacing
```latex
\setlength{\parindent}{0pt}     % no first-line indent
\setlength{\parskip}{10pt}      % 10pt between paragraphs
```

### Penalty settings (aggressive break prevention)
```latex
\clubpenalty=10000               % no orphan lines
\widowpenalty=10000              % no widow lines
\setlist[itemize]{beginpenalty=10000}  % don't break items across pages
\hyphenpenalty=10000             % avoid hyphenating words
\exhyphenpenalty=10000
```
House preference: produce documents with no awkward page breaks even at
the cost of looser spacing.

### Required packages (in order)
```latex
\usepackage{fontspec}
\usepackage[a4paper, textwidth=7in, top=20mm, bottom=20mm]{geometry}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{float}
\usepackage{caption}
\usepackage[ngerman]{babel}
\usepackage{longtable}
\usepackage{array}
\usepackage{booktabs}
\usepackage{tocloft}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{ulem}
\usepackage{tabularx}
\usepackage[table]{xcolor}
\usepackage{makecell}
```
Notes:
- `inputenc utf8` and `fontenc T1` are explicitly NOT used (incompatible
  with xelatex; the source has them commented out).
- `xcolor` is loaded with `[table]` option but the Friedrichshof template
  doesn't use color in body text. Headings stay black.

### Table of contents customization
```latex
\setlength{\cftsecnumwidth}{2em}
\setlength{\cftsubsecindent}{2em}
\setlength{\cftsubsecnumwidth}{3em}
\setlength{\cftsubsubsecindent}{5em}
```

### Table style
```latex
\renewcommand\theadalign{cb}        % vertically center table headers
\renewcommand\theadfont{\normalsize}
```
With `booktabs` providing `\toprule`/`\midrule`/`\bottomrule`. No vertical
rules; tables are minimalist.

### Headers and footers (fancyhdr)
```latex
\pagestyle{fancy}
\fancyhf{}
\lhead{\small \Gemeinde{} OT \Ortsteil{} \\ \small \BPlanEr{}}
\rhead{\small Begründung \\ \small Seite \thepage}
\setlength{\headheight}{23.24652pt}
```
Header references project commands defined in `Projektdaten.tex`. **The
right header reads "Begründung" verbatim** — for Textteil C this should
likely be "Festsetzungen" (TODO: confirm).

### Project metadata (Projektdaten.tex)
Defined as `\newcommand` macros referenced throughout the document:
```latex
\newcommand{\Gemeinde}{Klein Belitz}
\newcommand{\Gemarkung}{Friedrichshof}
\newcommand{\Ortsteil}{Friedrichshof}
\newcommand{\Landkreis}{Rostock}
\newcommand{\BebauungsplanEn}{vorhabensbezogenen Bebauungsplan}
\newcommand{\BebauungsplanEns}{vorhabensbezogenen Bebauungsplans}
\newcommand{\BebauungsplanEnes}{vorhabensbezogenen Bebauungsplanes}
\newcommand{\BebauungsplanE}{vorhabensbezogene Bebauungsplan}
\newcommand{\BPlanEr}{vorhabensbezogener Bebauungsplan Nr. 3 „Solarpark Friedrichshof"}
\newcommand{\BPlanEn}{vorhabensbezogenen Bebauungsplan Nr. 3 „Solarpark Friedrichshof"}
\newcommand{\BPlanEnes}{vorhabensbezogenen Bebauungsplanes Nr. 3 „Solarpark Friedrichshof"}
\newcommand{\BPlanN}{vorhabensbezogene Bebauungsplan Nr. 3}
\newcommand{\BPlanNa}{vorhabensbezogenen Bebauungsplan Nr. 3}
\newcommand{\Geltungsbereich}{44,7 ha}
\newcommand{\Planungsregion}{Rostock}
\newcommand{\SUR}{Rostock}
\newcommand{\Landesverordnung}{Regionale Raumentwicklungsprogramm Mittleres Mecklenburg/Rostock (RREP MMR)}
\newcommand{\RREP}{MMR}
```
The grammatical-case suffixes (`En` = Akkusativ singular, `Ens` = Genitiv,
`Enes` = older Genitiv form, `E` = Nominativ, `Er` = Nominativ with article,
`N` = without "vorhabensbezogen" prefix) are used so prose flows correctly
in different sentence positions. **Preserve this convention** when scaffolding
new projects.

### Modular Textbausteine (master .tex assembly)
Textteil-C.tex acts as an assembler:
```latex
\documentclass{article}
\input{preamble.tex}
\begin{document}
\begin{sloppy}
    \input{Textbausteine/Titelseite.tex}
    \newpage
    \tableofcontents
    \newpage
    \listoffigures
    \listoftables
    \newpage

    \input{Textbausteine/ERFORDERLICHKEIT DER PLANUNG.tex}
    \input{Textbausteine/Räumliche Einordnung und Zielsetzung.tex}
    \input{Textbausteine/PLANUNGSGRUNDLAGEN.tex}
    \input{Textbausteine/Vorgaben übergeordneter Planungen.tex}
    \input{Textbausteine/ANGABEN ZUM BESTAND.tex}
    \input{Textbausteine/PLANUNGSINHALTE.tex}
    \input{Textbausteine/ERSCHLIESSUNG DES PLANGEBIETES.tex}
    \input{Textbausteine/UMWELTBERICHT.tex}
    \input{Textbausteine/STAND DES AUFSTELLUNGSVERFAHRENS.tex}
    \input{Textbausteine/ERGEBNISSE DER ÖFFENTLICHKEITS- UND BEHÖRDENBETEILIGUNG.tex}
    \input{Textbausteine/ÄNDERUNGEN DES PLANENTWURFS GEGENÜBER DEM VORENTWURF.tex}
    \input{Textbausteine/FLÄCHENBILANZ.tex}
    \input{Textbausteine/SICHERUNG DER PLANDURCHFÜHRUNG.tex}
\end{sloppy}
\end{document}
```
Notes:
- Wrapped in `\begin{sloppy}…\end{sloppy}` to allow looser line-breaking
  (compensates for the strict penalty settings).
- `Textbausteine/` subfolder. Filenames are German, mixed-case with spaces
  and umlauts. xelatex handles Unicode filenames natively.
- Section files use ALL-CAPS for major sections, mixed-case for subsections.

### Standard B-Plan Textteil B section list (canonical order)
1. Titelseite
2. Erforderlichkeit der Planung
3. Räumliche Einordnung und Zielsetzung
4. Planungsgrundlagen
5. Vorgaben übergeordneter Planungen
6. Angaben zum Bestand
7. Planungsinhalte
8. Erschließung des Plangebietes
9. Umweltbericht (referenced from here, separate document)
10. Stand des Aufstellungsverfahrens
11. Ergebnisse der Öffentlichkeits- und Behördenbeteiligung
12. Änderungen des Planentwurfs gegenüber dem Vorentwurf
13. Flächenbilanz
14. Sicherung der Plandurchführung

This is the canonical Textteil B (Begründung) structure. Textteil C
(Festsetzungen) section list is a TODO — not yet observed in this
template (the file was named "Textteil-C" but its master assembly
matches Textteil B content; needs verification with user).

---

## Style B — PBS-Bericht (pdflatex / scrreprt / biblatex)

### Document class
```latex
\documentclass[12pt, a4paper, times, numbered, print, index, parskip=half,
  BCOR=5mm, headings=normal, toc=listof, bibliography=totoc,
  captions=tableheading]{scrreprt}
```
- `scrreprt` (KOMA-Script report) — chapter-based, suitable for long
  multi-chapter Berichte.
- `12pt`, A4, Times font (built-in via `times` option)
- `parskip=half` — half-line space between paragraphs
- `BCOR=5mm` — binding correction
- `bibliography=totoc` — bibliography appears in TOC
- `captions=tableheading` — table captions go above tables

### Engine
**pdflatex** (NOT xelatex). Uses `inputenc utf8 + fontenc T1 + ae +
aecompl` for Unicode + clean Type 1 font output.

### Required packages (in order observed)
```latex
\usepackage[german]{babel}
\usepackage{color}
\usepackage{setspace}
\usepackage{pdfpages}
\usepackage{amssymb}
\usepackage[table,xcdraw]{xcolor}
\usepackage{graphicx}
\usepackage[T1]{fontenc}
\usepackage{ae,aecompl}
\usepackage[utf8]{inputenc}
\usepackage[tableposition=top]{caption}
\usepackage{rotating}
\usepackage{multirow}
\usepackage{textcomp}
\usepackage{pdflscape}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{acronym}
\usepackage{longtable}
\usepackage{hyperref}
\usepackage{float}
\usepackage{pythontex}
```
Notes:
- `babel` here uses `german` (old orthography) — Textteil-C uses
  `ngerman` (new orthography). Inconsistency. **TODO:** confirm
  whether this is intentional or should be normalized.
- `pythontex` is a heavy dependency for embedded Python computations
  in TeX. Used for what specifically? TODO confirm.

### Bibliography (biblatex + biber)
```latex
\usepackage[backend=biber, style=authoryear, citestyle=authoryear,
  maxcitenames=2, uniquename=true]{biblatex}
\addbibresource{literatur.bib}
```
- backend = `biber` (NOT `bibtex`)
- author-year citation style
- `\printbibliography` at document end

### Layout
```latex
\begin{onehalfspace}    % 1.5 line spacing for body text
...
\end{onehalfspace}
```

### Title page (custom, hardcoded)
```latex
\begin{titlepage}
    \centering
    \vspace{1cm}
    {\scshape\LARGE \titel \par}
    {\scshape\Large zur \par}
    \vspace{1 cm}
    {\LARGE\bfseries \projekt \par}
    \vspace{1cm}
    \includegraphics*[width=0.2\textwidth]{logo.png}
    \vspace{0.5cm}
    {\scshape\Large Auftragnehmer: \par}
    {\Large\itshape Planungsbüro G. Schulz \par}
    {\Large\itshape Garten und Landschaftsarchitektur \par}
    {\Large\itshape Landschaftsplanung \par}
    {\Large\itshape Stadtplanung \par}
    \vspace{0.5 cm}
    {\scshape\Large Auftraggeber: \par}
    {\Large\itshape <client name> \par}
    ...
    {\large Schwerin, \today\par}
\end{titlepage}
```
- Title: small caps + LARGE
- Subtitle "zur" + projekt name
- `logo.png` at 20% textwidth
- Office identity block: Auftragnehmer, three lines of practice areas
- Office location: **Schwerin** (per `\today`)

### Project metadata (Projekt.tex)
```latex
\newcommand{\typ}{Umweltbericht}
\newcommand{\auftrag}{\textit{MaxSolar GmbH}}
\newcommand{\titel}{Umweltbericht}
\newcommand{\projekt}{Vorhabensbezogener Bebauungsplan Nr. 3 \textit{Friedrichshof} der Gemeinde Klein Belitz}
\newcommand{\autor}{Hendrik Sönnichsen}
\newcommand{\area}{42,5\,ha}
```
Different variable convention from Style A. Style B uses `\titel`,
`\projekt`, `\autor`, `\area`, `\auftrag`. Style A uses `\Gemeinde`,
`\Ortsteil`, `\BPlanEr`, `\Geltungsbereich`. **Conventions are not
unified across styles.**

### Modular Kapitel structure
Master file (`Bericht_PBS.tex`) loads exactly one Berichtstyp:
```latex
%\input{../Kapitel_AA/Ausnahmeantrag_Kapitel.tex}
%\input{../Kapitel_AFB/AFB_Kapitel.tex}
%\input{../Kapitel_GK/Gebaeudekontrolle_Kapitel.tex}
%\input{../Kapitel_KB/Kartierbericht_Kapitel.tex}
%\input{../Kapitel_LBP/LBP_Kapitel.tex}
%\input{../Kapitel_SPA_HP/SPA_Hauptpruefung_Kapitel.tex}
%\input{../Kapitel_SPA_VP/SPA_Vorpruefung_Kapitel.tex}
\input{../Kapitel_UB/Umweltbericht_Kapitel.tex}
%\input{../Kapitel_ZAV/Zielabweichung_Kapitel.tex}
```

This implies a much larger Berichtstyp catalog than just Umweltbericht:

| Folder | Berichtstyp |
|---|---|
| `Kapitel_AA` | Ausnahmeantrag |
| `Kapitel_AFB` | Artenschutzfachbeitrag |
| `Kapitel_GK` | Gebäudekontrolle |
| `Kapitel_KB` | Kartierbericht |
| `Kapitel_LBP` | Landschaftspflegerischer Begleitplan |
| `Kapitel_SPA_HP` | Speziell artenschutzrechtliche Prüfung — Hauptprüfung |
| `Kapitel_SPA_VP` | Speziell artenschutzrechtliche Prüfung — Vorprüfung |
| `Kapitel_UB` | Umweltbericht (the only confirmed-populated one) |
| `Kapitel_ZAV` | Zielabweichungsverfahren |

Most are commented out in the master, suggesting they exist as folders
but may be empty or stub-content. **TODO:** survey each folder, see
what's populated, treat populated ones as available doctypes.

### Umweltbericht_Kapitel.tex assembly
```latex
\chapter{Einleitung}
\input{../Kapitel_UB/Einleitung_UB}

\chapter{Bestandsaufnahme und Bewertung der Umweltauswirkungen}
\input{../Kapitel_UB/Standort_UB}
\input{../Kapitel_UB/MethodikGutachten_UB}
\input{../Kapitel_UB/Schutzgut_Boden_UB}
\input{../Kapitel_UB/Schutzgut_Wasser_UB}
\input{../Kapitel_UB/Schutzgut_TierePflanzen_UB}
\input{../Kapitel_UB/Schutzgut_KlimaLuft_UB}
\section{Schutzgut Mensch}
\input{../Kapitel_UB/Schutzgut_MenschEmi_UB}
\input{../Kapitel_UB/Schutzgut_MenschErh_UB}
\input{../Kapitel_UB/Schutzgut_Landschaft_UB}
\input{../Kapitel_UB/Schutzgut_KulturSachgut_UB}

\chapter{Prognose über die Entwicklung des Umweltzustands bei Nichtdurchführung der Planung}
\input{../Kapitel_UB/Prognose_Nichtdurchfuehrung_UB}

\chapter{Alternative Planungsmöglichkeiten}
\input{../Kapitel_UB/AlternativePlanung_UB}

\chapter{Geplante Maßnahmen zur Vermeidung, Verringerung und zum Ausgleich}
\input{../Kapitel_UB/Schutzgut_Boden_Mas_UB}
\input{../Kapitel_UB/Schutzgut_Wasser_Mas_UB}
\input{../Kapitel_UB/Schutzgut_TierePflanzen_Mas_UB}
\input{../Kapitel_UB/Schutzgut_KlimaLuft_Mas_UB}
\section{Schutzgut Mensch}
\input{../Kapitel_UB/Schutzgut_MenschEmi_Mas_UB}
\input{../Kapitel_UB/Schutzgut_MenschErh_Mas_UB}
\input{../Kapitel_UB/Schutzgut_Landschaft_Mas_UB}
\input{../Kapitel_UB/Schutzgut_KulturSachgut_Mas_UB}

\chapter{Naturschutzrechtliche Eingriffsregelung in der Bauleitplanung}
\input{../Kapitel_UB/EAB_UB}

\chapter{Maßnahmen zur Überwachung (Monitoring)}
\input{../Kapitel_UB/Monitoring_UB}

\chapter{Allgemein verständliche Zusammenfassung}
\input{../Kapitel_UB/Zusammenfassung_UB}
```

**Schutzgut paired-file pattern:** each Schutzgut has two files —
`Schutzgut_<Name>_UB.tex` (description / Bestandsaufnahme) AND
`Schutzgut_<Name>_Mas_UB.tex` (Maßnahmen). They appear in different
chapters (Bestand chapter vs Maßnahmen chapter). When drafting a new
project's Umweltbericht, both files must be created/edited per
Schutzgut. The orchestrator should treat them as a unit.

**Schutzgüter (canonical list):**
- Boden
- Wasser
- TierePflanzen
- KlimaLuft
- Mensch (split: MenschErh = Erholung, MenschEmi = Emissionen)
- Landschaft
- KulturSachgut

---

## Conventions shared across both styles

### Project metadata location
- Style A: `Projektdaten.tex` in same folder as master
- Style B: `Projekt.tex` in same folder as master
- Both use `\input{...}` to load it
- Both use `\newcommand` for all variables

### Modular section files
- Both use `\input{...}` for section assembly
- Style A: `Textbausteine/` subfolder, German UPPERCASE filenames with spaces
- Style B: sibling `Kapitel_XX/` folders with `_XX` suffix on filenames

### File naming
- ASCII underscores in Style B (`Schutzgut_Boden_UB.tex`)
- Spaces and umlauts in Style A (`Räumliche Einordnung und Zielsetzung.tex`)
- Both work in their respective engines

### Compile expectations
- Style A: `xelatex Textteil-C.tex` (single pass usually sufficient with TOC; second pass for stable cross-refs)
- Style B: `pdflatex` + `biber` + `pdflatex` + `pdflatex` (or use `latexmk -pdf`); `pythontex` step required if Python is used
- Recommend `latexmk` as wrapper for both

### What's NOT used
- No tcolorbox in either style (the Hendrik Artenschutz transcript used
  tcolorbox; that was Hendrik's personal style for Holthusen-Gutachten,
  separate from PBS canonical templates)
- No custom color palette in body text
- No images in headers/footers

---

## Known issues / cleanup items

These are observations for future cleanup; not blockers for v1.

1. **Hardcoded Windows path** in `Bericht - PBS/Bericht_PBS.tex`:
   ```latex
   \input{D://LaTeX/Befehle.tex}
   ```
   Won't work on Linux. Either move `Befehle.tex` to a relative location
   or use a configurable path. Investigate what's in Befehle.tex.

2. **Inconsistent babel option:**
   - Style A: `\usepackage[ngerman]{babel}` (new German orthography)
   - Style B: `\usepackage[german]{babel}` (old German orthography)
   - Should be `ngerman` everywhere (new orthography is standard since 2006).

3. **Duplicate `\usepackage{enumitem}`** in Style A's preamble (lines 29 and 45
   in current source). Cosmetic.

4. **Right header in Textteil-C reads "Begründung"** — but Textteil C is
   "Festsetzungen". Either the Friedrichshof template was originally Textteil B
   and got copied/repurposed, or this is intentional. Confirm with user.

5. **Textteil-C section list matches Textteil B canonical order** — same
   confirmation needed. If Textteil C has different sections (Festsetzungen
   tend to be much shorter and prescriptive rather than narrative), the
   template needs a separate Textteil B variant.

6. **`pythontex` dependency** in Style B is heavy. What computations does
   it do? Could it be removed if not used in current projects?

7. **Title page uses `Schwerin, \today`** in Style B — Hendrik works from
   Holthusen, Schulz from Schwerin. Joint projects? Configurable?

---

## Open questions for confirmation

- Q1: Is the Friedrichshof "Textteil-C" template actually a Textteil-B
  template (based on its section list)? If yes, what's the canonical
  Textteil-C section list?
- Q2: Of the nine `Kapitel_XX` Berichtstyp folders, which are populated
  with content vs empty stubs? (Survey needed.)
- Q3: What's in `D://LaTeX/Befehle.tex` (Style B's hardcoded include)?
  Possibly common command shortcuts.
- Q4: Should `german`/`ngerman` be normalized to `ngerman`?
- Q5: Does PBS use a logo file at standard location across all projects,
  or is `logo.png` per-project?

These belong on the product backlog and get resolved when we encounter
them in real project work.
