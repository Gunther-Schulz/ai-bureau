---
references_used:
  - {law: BauGB, paragraph: §9}
  - {law: BauGB, paragraph: §10}
  - {law: BNatSchG, paragraph: §44}
---

# LaTeX style specification — universal B-Plan domain

This document captures the **structural domain** of B-Plan LaTeX
production: which document classes to use, which conventions are
universal across German Planungsbüros, and which macros and patterns
the app's skeletons assume.

**Office-specific choices** (geometry, fonts, header layouts,
TOC styling, color schemes, identity macros) are NOT here. They live
in each office's `office-style.sty` under
`office_config.templates.office_style_dir`. That `.sty` is loaded by
the app's skeletons via `\usepackage{office-style}` and supplies the
office's aesthetic on top of the structural skeleton.

A B-Plan project produces **two LaTeX documents** that share metadata
but have different shapes. Both compile with **pdflatex**:

| Doctype | Class | Output shape | Master file |
|---|---|---|---|
| **Begründung** | `scrreprt` | Multi-page narrative report | `B-Plan Begründung.tex` |
| **Textliche Festsetzungen** | `article` | Single long page (Satzung Teil B Text) | `Textteil-B-B-Plan.tex` |

Naming clarification: `Textteil-B-B-Plan.tex` refers to "Teil B Text"
of the B-Plan Satzung (Teil A = Planzeichnung, Teil B = Text). It is
**not** "Textteil B" in the older Bundesländer-convention sense. The
Begründung is a separate explanatory document outside the Satzung.

---

## Doctype A — Begründung (scrreprt)

### Document class

```latex
\documentclass[12pt, a4paper, parskip=half,
  bibliography=totoc, captions=tableheading,
  toc=listof]{scrreprt}
```

- KOMA-Script `scrreprt` (chapter-based, but chapters typically
  not used — sections are top-level).
- `parskip=half` — half-line space between paragraphs.
- `bibliography=totoc` — bibliography appears in TOC.
- `captions=tableheading` — table captions above tables.
- Office-specific: `BCOR`, `headings`, font option (`times`,
  `palatino`, etc.), `numbered`/`print`/`index` flags. Set in
  the office's `office-style.sty` or in office-overlay class options.

### Engine

```
% !TeX program = pdflatex
```

### Encoding & language

```latex
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}    % new German orthography
```

Universal across German planning practice. `ngerman` enables German
hyphenation patterns; combined with `pdflatex` + `utf8 inputenc` it
handles UTF-8 source (umlauts, ß, German quotation marks).

### Hyphenation tuning

```latex
\usepackage{hyphenat}
\tolerance=1500
\emergencystretch=3em
\hyphenpenalty=50
\exhyphenpenalty=50
\hbadness=10000
```

Permits some hyphenation rather than fighting all breaks, while
suppressing badness warnings. Office may add specific hyphenation
hints (`\hyphenation{Bun-des-na-tur-schutz-ge-setz}`) for
frequently-bad-breaking compounds in office-style.sty.

### Headers

The Begründung uses `scrlayer-scrpage` (NOT `fancyhdr`):

```latex
\usepackage[automark]{scrlayer-scrpage}
\clearpairofpagestyles
```

Header content (`\ihead`, `\ohead`) and TOC pagestyle definitions
are **office choice** — set in `office-style.sty`. Conventional
content: inner head shows `Gemeinde \Gemeinde / \BPlanTyp`, outer
head shows `Begründung / Seite \thepage`.

### Page numbering: Roman → Arabic flip

```latex
\newcommand{\startroman}{%
  \cleardoublepage
  \pagenumbering{Roman}        % capital-Roman
  \setcounter{page}{1}
}
\newcommand{\startarabic}{%
  \cleardoublepage
  \pagenumbering{arabic}
  \setcounter{page}{1}
}
```

Used to switch numbering between prelims (Title, TOC, List of Tables)
and main body. **Capital Roman** (`I, II, III`), not lowercase.
Universal in German planning practice for legal-document layout.

### Section numbering (re-declared)

```latex
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}
```

Forces flat arabic numbering even though the doc is `scrreprt` (where
chapters would otherwise prefix all numbering). Sections at top level
are numbered `1`, `2`, `3` — chapters not used.

### Number formatting (siunitx, German conventions)

```latex
\usepackage{siunitx}
\sisetup{
  output-decimal-marker={,},
  group-separator={.},
  group-minimum-digits=4
}
\newcommand{\formatnumber}[1]{\num[round-mode=places,round-precision=0]{#1}}
```

- Decimal: comma (German style).
- Thousands separator: dot, applied to numbers ≥ 4 digits.

Universal in German legal/planning documents.

### Master document assembly

```latex
\documentclass[...]{scrreprt}
\usepackage{office-style}      % office's styling overlay
\input{office-identity}        % office identity macros (auto-generated)
\input{Projektdaten.tex}       % per-project metadata

\begin{document}
\startroman
\pagestyle{tocstyle}           % style defined in office-style.sty

\input{Textbausteine/Titelseite.tex}
\cleardoublepage
\tableofcontents
\cleardoublepage
\listoftables
\cleardoublepage

\startarabic
\pagestyle{scrheadings}

\input{Textbausteine/<section-1>.tex}
\input{Textbausteine/<section-2>.tex}
% ... per the section list below
\end{document}
```

### Begründung canonical section order

The standard B-Plan Begründung section list, observed across German
planning bureau practice:

1. Titelseite
2. Aufgaben und Inhalte der Planung
3. Grundlagen der Planung — Aufstellungsverfahren
4. Geltungsbereich
5. Planinhalte und Festsetzungen
6. Ver- und Entsorgungsanlagen
7. Vorbeugender Brandschutz — Löschwasserversorgung
8. Gewässerschutz
9. Bodenschutz
10. Immissions- und Klimaschutz — Blendwirkung
11. Altlasten und Altlastverdachtsflächen
12. Belange der Forst
13. Denkmalschutz
14. Kataster- und Vermessungswesen
15. Alternativprüfung
16. Kosten und Finanzierung
17. Signatur

Project-specific deviations from this list are normal — sections may
be omitted (when not applicable) or extended (project-specific topics).
The `validate-checklist` skill marks each section as REQUIRED /
EXPECTED / OPTIONAL per the doctype checklist.

### Textbausteine subfolder

- `Textbausteine/` next to master.
- Filenames in mixed-case German with spaces and umlauts.
- pdflatex handles UTF-8 filenames since the doc uses `inputenc utf8`.

---

## Doctype B — Textliche Festsetzungen (article, infinite page)

### Document class & engine

```latex
\documentclass[12pt]{article}
% pdflatex
```

Plain `article`. No KOMA, no chapters. Single document.

### Encoding

```latex
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}
```

### Other packages (typical)

```latex
\usepackage[final]{microtype}
\usepackage{enumitem}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{url}
```

### Body font

Festsetzungen body is conventionally rendered **sans-serif** (visual
distinction from the serif-typeset Begründung — sans-serif signals
the "binding rules" portion vs the narrative explanation). Specific
font choice is office aesthetic.

### Geometry — single infinite page

The Festsetzungen output is **one PDF page** containing the full
text, designed to be embedded as Teil B of the B-Plan Satzung
document. Implementation:

```latex
\geometry{
  paperwidth=210mm,            % A4 width
  paperheight=4000pt,           % effectively one infinitely-long page
  left=0in, right=0in,
  top=0in, bottom=0in
}
```

A4 width but paperheight maxed (≈141 cm; TeX limit ≈575 cm). No
margins inside the geometry — content controls its own indentation.
Will not paginate; very long Festsetzungen could overflow `4000pt` —
in practice rare.

### Document body structure

1. Header: `\textbf{Satzung der Gemeinde \Gemeinde{} über den \BPlan{}}`
2. `\subsection*{Präambel}` — long sentence reciting BauGB §10 plus
   state-LBauO references and Beschlussfassung clause.
3. `\subsection*{Teil A: Planzeichnung i. M. 1 : 2.000}` (heading
   placeholder; the actual Planzeichnung is separate).
4. `\section*{Teil B Text}`
5. Numbered Planungsrechtliche Festsetzungen gemäß §9 BauGB:
   - Art der baulichen Nutzung
   - Maß der baulichen Nutzung
   - Schutzmaßnahmen
   - Artenschutzrechtliche Festsetzungen (when §44 BNatSchG triggered)
   - Örtliche Bauvorschriften (per state LBauO)
6. `\section*{Verfahrensvermerke}` — placeholder dates and signature
   blocks. The exact reihenfolge is state-specific and per Verfahrenstyp
   — see `bauleitplanung-phasen.md` and the state-leitfaden corpus.
7. `\section*{Hinweis}` — Denkmalschutz boilerplate (per state DSchG).
8. Centered title-block: `SATZUNG DER GEMEINDE / \Gemeinde / ÜBER DEN /
   \BPlanTyp`.
9. `\section*{Rechtsgrundlagen}` — bullet list of cited laws with full
   citations: BauGB, BauNVO, PlanZV, BNatSchG (federal); state LBauO,
   NatSchAG, KV (state).

### enumerate styling pattern

```latex
\begin{enumerate}[label=\arabic*., leftmargin=*, labelsep=20pt, font=\bfseries]
  \item \textbf{...}
        \begin{enumerate}[label=\arabic{enumi}.\arabic*., leftmargin=0pt, labelsep=10pt]
          \item ...
        \end{enumerate}
\end{enumerate}
```

- Top-level: `1.`, `2.`, `3.` in bold.
- Nested: `1.1.`, `1.2.` flat-aligned to `0pt` margin.

### Verfahrensvermerke pattern

Repetitive block per Verfahrensschritt:

```latex
\item Aufgestellt aufgrund des Aufstellungsbeschlusses der Gemeindevertretung vom ...........
      Der Aufstellungsbeschluss ist am ........... durch Abdruck ...

      \begin{tabbing}
        \hspace{6cm} \= \hspace{4cm} \= \kill
        \Gemeinde{}, \> Siegel \> \hspace{8pt} <Bürgermeister-Name> \\
        \> \> — Bürgermeister —
      \end{tabbing}
```

- Placeholder dates rendered as `................`.
- Signature block uses tabbing (not tabular) for left-aligned location,
  middle-aligned `Siegel`, right-aligned name + title.

---

## Project metadata convention (Projektdaten.tex)

Both doctypes read a `Projektdaten.tex` of identical structure:

```latex
\newcommand{\Gemeinde}{<Gemeinde>}
\newcommand{\Stadt}{---STADT---}              % set or leave placeholder
\newcommand{\Gemarkung}{<Gemarkung>}
\newcommand{\Ortsteil}{<Ortsteil>}
\newcommand{\Landkreis}{<Landkreis>}
\newcommand{\BPlanAbrv}{B-Plan}
\newcommand{\BPlanNr}{<N>}
\newcommand{\BPlanName}{„<BPlan-Name>"}
\newcommand{\BPlan}{vorhabensbezogenen Bebauungsplan Nr. <N> mit integriertem Vorhaben- und Erschließungsplan}
\newcommand{\BPlanTyp}{Vorhabensbezogener Bebauungsplan Nr. <N> mit integriertem Vorhaben- und Erschließungsplan}
\newcommand{\GeltungsbereichHa}{<X,XX>}
\newcommand{\GeltungsbereichHaSolar}{<X,XX>}
\newcommand{\Planungsregion}{<Region>}
% \newcommand{\Landesverordnung}{...}
```

**Key convention:** `\BPlan` is **lowercase-leading** (used inside
running prose, e.g. "...des vorhabensbezogenen Bebauungsplans..."),
while `\BPlanTyp` is **capitalized-leading** (used at sentence start
or in headings). Different macros for different grammatical positions.

Placeholder values use `---FIELDNAME---` shouted-uppercase to make
unfilled fields glaringly visible. Each new project should fill all
slots before compile.

These macros are universal — every German B-Plan project needs them.
The app's skeleton ships a Projektdaten.tex template with these
fields as placeholders; setup_project / scaffold_project instantiates
the values from project metadata.

---

## Cross-doctype conventions

- **Engine:** pdflatex everywhere. Never xelatex.
- **Encoding:** utf8 inputenc + T1 fontenc + ngerman babel.
- **Compile chain:** `latexmk -pdf` (pulls in pdflatex iterations as
  needed). Multiple passes required for stable TOC / refs.
- **Numbers in prose:** German format (decimal `,`, thousands `.`).
  Use `siunitx` in tables; use `~` non-breaking space before units in
  prose (`5~m`, `30,37~ha`).
- **Quotation marks:** `\glqq{}…\grqq{}` for German-style quotes
  (low-9 open, high-6 close). Never straight `"`.
- **Legal references:** `§~9 BauGB`, `§~44 BNatSchG` — non-breaking
  space between `§` and number.
- **Compound word hyphenation:** when LaTeX breaks German compounds
  badly, add to `\hyphenation{...}` in office-style.sty OR insert
  `\-` in source.

---

## Office-specific layer (office-style.sty)

Per `office_config.templates.office_style_dir`. Authored once per
office. Provides:

- Geometry (margins, BCOR, headheight, marginparwidth).
- Header layout: content of `\ihead`, `\ohead` per page style.
- Heading fonts (sizes via `\addtokomafont`).
- TOC styling (indent values, leader-fill, page-number alignment,
  Inhaltsverzeichnis case).
- Color theme (if any).
- Office logo / Briefkopf.
- Office-specific `\hyphenation{...}` hints.
- Festsetzungen-specific `\titleformat{\section}{...}` choices.

The app's skeleton is loadable WITHOUT office-style.sty (a default
minimal one is shipped) — the office layer customizes appearance
without affecting structural correctness.

---

## Office-identity layer (office-identity.tex)

Auto-generated by the backend before each compile from
`office_config.office.*` (post-v3 merge of identity into office). Provides:

- `\OfficeName` — full office name.
- `\OfficeShort` — abbreviation.
- `\OfficeAddressLines` — multi-line address block.
- `\OfficePhone`, `\OfficeEmail`, `\OfficeWeb` — contact data
  (when set in identity).
- `\OfficeSignatureBlock` — signature paragraph.
- `\OfficeSigner` — signer name from active practice.

These macros are consumed by `office-style.sty` (e.g. in headers,
title pages, signatures). Single source of truth: the office-config
`identity:` section.
