# LaTeX style specification

PBS produces B-Plan documents as **two separate LaTeX projects per
B-Plan**. They have different structures, different document classes,
and different output shapes. Both compile with **pdflatex** (not
xelatex). Engine choice is uniform.

| Doctype | Class | Output shape | Master file naming |
|---|---|---|---|
| **Begründung** | `scrreprt` | Multi-page narrative report | `B-Plan Begründung.tex` |
| **Textliche Festsetzungen** | `article` | Single long page (Satzung Teil B Text) | `Textteil-B-B-Plan.tex` |

Naming clarification: the file `Textteil-B-B-Plan.tex` refers to
"Teil B Text" of the B-Plan Satzung (Teil A = Planzeichnung,
Teil B = Text). It is **not** Textteil B in the standard
Bundesländer-convention sense. The Begründung is a separate
explanatory document outside the Satzung.

---

## Doctype A — Begründung (scrreprt)

Source of truth: `~/dev/Planungsbüro-Schulz/22-16-Maxsolar---Friedrichshof---B-Plan---Begruendung/`

### Document class
```latex
\documentclass[12pt, a4paper, times, numbered, print, index, parskip=half,
  BCOR=5mm, headings=normal, toc=listof, bibliography=totoc,
  captions=tableheading]{scrreprt}
```
- KOMA-Script `scrreprt` (chapter-based)
- 12pt, A4, Times font (built-in via `times` option)
- `parskip=half` — half-line space between paragraphs
- `BCOR=5mm` — binding correction
- `bibliography=totoc` — bibliography appears in TOC
- `captions=tableheading` — table captions above tables

### Engine
```
% !TeX program = pdflatex
```

**Heads-up:** the Friedrichshof master file has a stale magic comment
`% !TeX root = Textteil-C.tex` at the top — leftover from a copy. The
actual root is `B-Plan Begründung.tex`. Should be cleaned up.

### Geometry
```latex
\usepackage[a4paper, left=25mm, right=25mm, top=30mm, bottom=25mm,
  headheight=30pt, marginparwidth=0pt]{geometry}
```

### Encoding & language
```latex
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}    % new German orthography
```

### Hyphenation tuning
```latex
\usepackage{hyphenat}
\tolerance=1500
\emergencystretch=3em
\hyphenpenalty=50
\exhyphenpenalty=50
\hbadness=10000
```
Notably **softer** than the older office templates (which used 10000 for
every penalty). This pdflatex setup permits some hyphenation rather than
fighting all breaks, while suppressing badness warnings.

### Headers (scrlayer-scrpage, NOT fancyhdr)
```latex
\usepackage[automark]{scrlayer-scrpage}
\clearpairofpagestyles

\ihead{\small\parbox[t]{0.45\textwidth}{Gemeinde \Gemeinde{} \\
       \BPlanTyp{} \BPlan{}}}
\ohead{\small Begründung \\ \small Seite \thepage}

\newpairofpagestyles[scrheadings]{tocstyle}{
  \ihead{...same as main...}
  \ohead{\small Begründung \\ \small Seite \thepage}
}
\renewcommand*{\chapterpagestyle}{tocstyle}
```
- Inner head: `Gemeinde X / BPlanTyp BPlan`
- Outer head: `Begründung / Seite N`
- Custom `tocstyle` so prelim pages keep the same header
- `\automark` to drive content from chapter/section names

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
Used in the master to switch numbering between prelims (Title, TOC, LOT)
and main body. **Capital Roman** (`I, II, III`), not lowercase.

### Heading fonts
```latex
\addtokomafont{section}{\normalfont\Large\bfseries}
\addtokomafont{subsection}{\normalfont\large\bfseries}
\addtokomafont{subsubsection}{\normalfont\normalsize\bfseries}
```

### Section numbering (re-declared)
```latex
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}
```
Forces flat arabic numbering even though the doc is `scrreprt`
(otherwise sections would be `1.1` under chapters; here chapters aren't
used and sections are top-level numbered as `1`, `2`, `3`).

### TOC styling (tocbasic, NOT tocloft)
```latex
\usepackage{tocbasic}
\setcounter{tocdepth}{3}

\RedeclareSectionCommands[
  tocdynnumwidth,
  toclinefill=\TOCLineLeaderFill,
  tocraggedpagenumber=true
]{section,subsection,subsubsection}

\DeclareTOCStyleEntry[indent=0pt, numwidth=2em, level=1,
                     entryformat=\normalfont]{tocline}{section}
\DeclareTOCStyleEntry[indent=2em, numwidth=3em, level=2,
                     entryformat=\normalfont]{tocline}{subsection}
\DeclareTOCStyleEntry[indent=5em, numwidth=4em, level=3,
                     entrynumberformat=\itshape,
                     entryformat=\normalfont\itshape]{tocline}{subsubsection}
\DeclareTOCStyleEntry[beforeskip=1.0em plus 1pt]{tocline}{section}

\renewcaptionname{ngerman}{\contentsname}{\MakeUppercase{Inhaltsverzeichnis}}
```
- Subsubsections italicized in TOC
- "Inhaltsverzeichnis" forced UPPERCASE
- Page numbers right-ragged (no leader-dot fill)

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
- Decimal: comma (German style)
- Thousands separator: dot, applied to numbers ≥ 4 digits

### Master document assembly
```latex
\documentclass[...]{scrreprt}
\input{preamble.tex}
\input{Projektdaten.tex}

\begin{document}
\startroman
\pagestyle{tocstyle}

\input{Textbausteine/Titelseite.tex}
\cleardoublepage
\tableofcontents
\cleardoublepage
% \listoffigures
% \cleardoublepage
\listoftables
\cleardoublepage

\startarabic
\pagestyle{scrheadings}

\input{Textbausteine/Aufgaben und Inhalte der Planung.tex}
\input{Textbausteine/Grundlagen der Planung - Aufstellungsverfahren.tex}
\input{Textbausteine/Geltungsbereich.tex}
\input{Textbausteine/Planinhalte und Festsetzungen.tex}
\input{Textbausteine/Ver- und Entsorgungsanlagen.tex}
\cleardoublepage
\input{Textbausteine/Vorbeugender Brandschutz - Löschwasserversorgung.tex}
\input{Textbausteine/Gewässerschutz.tex}
\input{Textbausteine/Bodenschutz.tex}
\input{Textbausteine/Immissions- und Klimaschutz - Blendwirkung.tex}
\input{Textbausteine/Altlasten und Altlastverdachtsflächen.tex}
\input{Textbausteine/Belange der Forst.tex}
\input{Textbausteine/Denkmalschutz.tex}
\input{Textbausteine/Kataster- und Vermessungswesen.tex}
\input{Textbausteine/Alternativpüfung}            % typo: Alternativprüfung
\input{Textbausteine/Kosten und Finanzierung.tex}
\input{Textbausteine/Signatur.tex}
\end{document}
```

### Begründung canonical section order (Friedrichshof)
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

This is one project's order; section list may vary slightly per
project. Survey other projects to confirm the canonical superset.
The "Alternativpüfung" filename has a typo (missing 'r' before 'p')
that's been carried in the master `\input{}`.

### Textbausteine subfolder
- `Textbausteine/` next to master
- Filenames in mixed-case German with spaces and umlauts
- pdflatex handles UTF-8 filenames since the doc is `inputenc utf8`

---

## Doctype B — Textliche Festsetzungen (article, infinite page)

Source of truth: `~/dev/Planungsbüro-Schulz/22-16-Maxsolar---Friedrichshof---B-Plan-Textliche-Festsetzungen/Textteil-B-B-Plan.tex`

### Document class & engine
```latex
\documentclass[12pt]{article}
% pdflatex
```
Plain `article`. No KOMA, no chapters.

### Encoding
```latex
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}
```

### Other packages
```latex
\usepackage[final]{microtype}
\usepackage{enumitem}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{url}
```

### Sans-serif font (override default)
```latex
\renewcommand{\familydefault}{\sfdefault}
```
Different from Begründung — Festsetzungen body is **sans-serif**, while
Begründung uses Times serif. Visual marker that Festsetzungen are the
"binding rules" portion vs the narrative explanation.

### Hyphenation
```latex
\setlength{\emergencystretch}{3em}
\hyphenation{Na-tur-schutz-aus-füh-rungs-ge-setz Bun-des-na-tur-schutz-ge-setz}
```
Pre-declared hyphenation hints for long compound words that LaTeX
otherwise breaks badly.

### Geometry — single infinite page
```latex
\geometry{
  paperwidth=210mm,            % A4 width
  paperheight=4000pt,           % effectively one infinitely-long page
  left=0in, right=0in,
  top=0in, bottom=0in
}
```
- A4 width but paperheight maxed (~141 cm; TeX limit ~575cm)
- No margins inside the geometry — content controls its own indentation
- Output is **one PDF page** containing the full text, designed to be
  embedded as Teil B of the B-Plan Satzung document
- Will not paginate; very long Festsetzungen could overflow `4000pt`,
  but in practice fits

### Section title formatting
```latex
\titleformat{\section}
  {\normalfont\normalsize\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries}{\thesubsubsection}{1em}{}
```
All heading levels render at **normalsize bold**. No size escalation.
Compact, list-like presentation — fitting for a Satzung.

### Document body structure
1. Header: `\textbf{Satzung der Gemeinde \Gemeinde{} über den \BPlan{}}`
2. `\subsection*{Präambel}` — long sentence reciting BauGB §10 + LBauO M-V references and the Beschlussfassung clause
3. `\subsection*{Teil A: Planzeichnung i. M. 1 : 2.000}` (just a heading)
4. `\section*{Teil B Text}`
5. `\section*{I.\hspace{17pt} Planungsrechtliche Festsetzungen gemäß §~9 BauGB}`
   - Numbered enumerate: Art der baulichen Nutzung, Maß der baulichen
     Nutzung, Schutzmaßnahmen, Artenschutzrechtliche Festsetzungen,
     Örtliche Bauvorschriften
   - Each with nested subitems
6. `\section*{Verfahrensvermerke}` — placeholder dates and signature blocks
7. `\section*{Hinweis}` — Denkmalschutz boilerplate
8. Title-block of cente blocks: `SATZUNG DER GEMEINDE / Klein Belitz /
   ÜBER DEN / Vorhabensbezogener Bebauungsplan ... `
9. `\section*{Rechtsgrundlagen}` — bullet list of BauGB, BauNVO, PlanZV,
   KV M-V, BNatSchG, NatSchAG M-V, LBauO M-V with full citations

### enumerate styling pattern
```latex
\begin{enumerate}[label=\arabic*., leftmargin=*, labelsep=20pt, font=\bfseries]
  \item \textbf{...}
        \begin{enumerate}[label=\arabic{enumi}.\arabic*., leftmargin=0pt, labelsep=10pt]
          \item ...
        \end{enumerate}
\end{enumerate}
```
- Top-level: `1.`, `2.`, `3.` in bold
- Nested: `1.1.`, `1.2.` flat-aligned to `0pt` margin
- `labelsep` controls space between label and content

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
- Placeholder dates rendered as `................`
- Signature block uses tabbing (not tabular) for left-aligned location,
  middle-aligned `Siegel`, right-aligned name + title

---

## Project metadata convention (Projektdaten.tex)

Both doctypes read a `Projektdaten.tex` of identical structure:

```latex
\newcommand{\Gemeinde}{Klein Belitz}
\newcommand{\Stadt}{---STADT---}
\newcommand{\Gemarkung}{Friedrichshof}
\newcommand{\Ortsteil}{Friedrichshof}
\newcommand{\Landkreis}{Rostock}
\newcommand{\BPlanAbrv}{B-Plan}
\newcommand{\BPlanNr}{3}
\newcommand{\BPlanName}{„Solarpark Friedrichshof"}
\newcommand{\BPlan}{vorhabensbezogenen Bebauungsplan Nr. 3 mit integriertem Vorhaben- und Erschließungsplan}
\newcommand{\BPlanTyp}{Vorhabensbezogener Bebauungsplan Nr. 3 mit integriertem Vorhaben- und Erschließungsplan}
\newcommand{\GeltungsbereichHa}{43,57}
\newcommand{\GeltungsbereichHaSolar}{30,37}
\newcommand{\Planungsregion}{Rostock}
% \newcommand{\Landesverordnung}{...}
```

**Key convention:** `\BPlan` is **lowercase-leading** (used inside running prose, e.g. "...des vorhabensbezogenen Bebauungsplans..."), while `\BPlanTyp` is **capitalized-leading** (used at sentence start or in headings). Different macros for different grammatical positions.

Placeholder values use `---FIELDNAME---` shouted-uppercase to make
unfilled fields glaringly visible. Each new project should fill all
slots before compile.

---

## Per-project file layout

Each project folder is its **own git repo** at
`~/dev/Planungsbüro-Schulz/<long-name>/`, containing:

```
<project-repo>/
├── B-Plan Begründung.tex          # Begründung master (or)
├── Textteil-B-B-Plan.tex          # Festsetzungen master
├── preamble.tex                   # doctype-specific preamble
├── Projektdaten.tex               # macros for this project
├── Textbausteine/                 # per-section .tex files (Begründung)
├── Bilder/                        # images (Begründung)
├── Vorlage/                       # local template variants (some projects)
├── BauGB.txt                      # reference text colocated with project
├── EEG 2023 - Gesetz für den Ausbau...txt   # ditto
├── README.md                      # project notes (sparse)
├── korrektur-prompt.txt           # the legacy AI proofing prompt
├── korrektur-prompt-old.txt       # earlier version
├── clean_latex_aux.sh             # cleanup auxiliary files
├── fix_quotes.py                  # German-quote fixup helper
├── pdf_to_image.sh                # PDF→PNG (for OCR or thumbnails)
└── B-Plan Begründung.{aux,fdb_latexmk,fls,log,lot,pdf,synctex.gz,toc,tex}
                                   # build artifacts (should be gitignored)
```

Notes:
- Reference text files (BauGB.txt, EEG.txt, etc.) are colocated **per
  project** rather than centralized. Duplicate content across projects.
  When a law changes, every project's copy goes stale unless updated
  individually. (Roadmap: centralize references via the RAG.)
- LaTeX build artifacts are committed to git in some repos. These
  should be in `.gitignore` (will need cleanup migration when projects
  adopt our system).
- `clean_latex_aux.sh` removes the artifacts manually; `fix_quotes.py`
  applies regex-based German-quote conversion; `pdf_to_image.sh`
  rasterizes for OCR pre-processing. All three are migration material —
  their function should fold into our MCP server's `compile_latex`,
  validation hooks, and an OCR helper.

---

## Cross-doctype conventions

- **Engine:** pdflatex everywhere. Never xelatex (that was a wrong
  reading of an old hidrive Vorlagen folder; the local templates are
  authoritative).
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
  badly, add to `\hyphenation{...}` in preamble OR insert `\-` in
  source.

---

## Cleanup items (already noted; backlog candidates)

1. **Stale magic comment** in Friedrichshof Begründung master:
   `% !TeX root = Textteil-C.tex` should be removed.
2. **Filename typo** in Textbausteine: `Alternativpüfung` (missing 'r').
   Fix the file and the `\input{...}` reference.
3. **Build artifacts in git** in some project repos. `.gitignore` for
   `*.aux *.fdb_latexmk *.fls *.log *.lot *.toc *.synctex.gz` etc.
4. **Reference texts duplicated across projects** (BauGB.txt, EEG.txt
   per project). Centralize in the RAG once references are ingested.
5. **Helper scripts** (`clean_latex_aux.sh`, `fix_quotes.py`,
   `pdf_to_image.sh`) duplicated across projects. Fold into MCP server.

---

## Open questions for confirmation

- Q1: Is the section list in Friedrichshof Begründung the canonical set,
  or do other projects (e.g. Waren-Grabowhöfe) have additional / different
  sections? Should be answered by surveying other Begründung repos.
- Q2: For Festsetzungen, the layout uses `paperheight=4000pt`. Any
  Festsetzungen ever overflowed this? Workaround if so?
- Q3: Are Begründung and Festsetzungen always paired 1:1 per B-Plan, or
  do some B-Plans have only one? (The two existing 22-20 repos suggest
  pairing is normal.)
- Q4: F-Plan Begründung — same template as B-Plan Begründung, or its own
  variant? (The existing local repos cover only B-Plan; F-Plan exists in
  hidrive project folders but no LaTeX repo here yet.)
