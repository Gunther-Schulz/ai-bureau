# Umweltbericht — required structure

The Umweltbericht is the environmental report attached to a B-Plan,
required under §2a BauGB and Anlage 1. PBS uses (or will use) the
modular Kapitel_UB assembly with paired `_UB` (Bestand) /
`_Mas_UB` (Maßnahmen) files per Schutzgut.

Severities: REQUIRED, EXPECTED, OPTIONAL.

## Document class and engine

| Rule | Severity |
|---|---|
| `\documentclass[...]{scrreprt}` (PBS-Bericht style) | REQUIRED |
| Engine = pdflatex | REQUIRED |
| `babel` with `[ngerman]` | REQUIRED |
| `biblatex` with biber backend, authoryear style | EXPECTED |
| `\title{Umweltbericht}` in `Projekt.tex` | REQUIRED |
| `\renewcommand{\typ}{Umweltbericht}` in `Projekt.tex` | REQUIRED |

## Master assembly structure

Required chapters in order:

| # | Chapter | Severity |
|---|---|---|
| 1 | `\chapter{Einleitung}` → `Einleitung_UB.tex` | REQUIRED |
| 2 | `\chapter{Bestandsaufnahme und Bewertung der Umweltauswirkungen}` | REQUIRED |
| 3 | `\chapter{Prognose über die Entwicklung des Umweltzustands bei Nichtdurchführung der Planung}` → `Prognose_Nichtdurchfuehrung_UB.tex` | REQUIRED |
| 4 | `\chapter{Alternative Planungsmöglichkeiten}` → `AlternativePlanung_UB.tex` | REQUIRED |
| 5 | `\chapter{Geplante Maßnahmen zur Vermeidung, Verringerung und zum Ausgleich}` | REQUIRED |
| 6 | `\chapter{Naturschutzrechtliche Eingriffsregelung in der Bauleitplanung}` → `EAB_UB.tex` | REQUIRED |
| 7 | `\chapter{Maßnahmen zur Überwachung (Monitoring)}` → `Monitoring_UB.tex` | REQUIRED |
| 8 | `\chapter{Allgemein verständliche Zusammenfassung}` → `Zusammenfassung_UB.tex` | REQUIRED |

## Chapter 2 — required Bestand sub-sections

| File | Severity |
|---|---|
| `Standort_UB.tex` | REQUIRED |
| `MethodikGutachten_UB.tex` | REQUIRED |
| `Schutzgut_Boden_UB.tex` | REQUIRED |
| `Schutzgut_Wasser_UB.tex` | REQUIRED |
| `Schutzgut_TierePflanzen_UB.tex` | REQUIRED |
| `Schutzgut_KlimaLuft_UB.tex` | REQUIRED |
| `\section{Schutzgut Mensch}` (manual section header) | REQUIRED |
| `Schutzgut_MenschEmi_UB.tex` | REQUIRED |
| `Schutzgut_MenschErh_UB.tex` | REQUIRED |
| `Schutzgut_Landschaft_UB.tex` | REQUIRED |
| `Schutzgut_KulturSachgut_UB.tex` | REQUIRED |

Wechselwirkungen between Schutzgüter: optional explicit section.

## Chapter 5 — required Maßnahmen sub-sections

| File | Severity | When required |
|---|---|---|
| `Schutzgut_Boden_Mas_UB.tex` | REQUIRED if Boden-Eingriff | almost always |
| `Schutzgut_Wasser_Mas_UB.tex` | REQUIRED if Wasser-Eingriff | conditional |
| `Schutzgut_TierePflanzen_Mas_UB.tex` | REQUIRED if Arten-Eingriff | almost always for solar |
| `Schutzgut_KlimaLuft_Mas_UB.tex` | OPTIONAL | rarely required |
| `\section{Schutzgut Mensch}` | REQUIRED if MenschEmi+Mas exists | header |
| `Schutzgut_MenschEmi_Mas_UB.tex` | EXPECTED for solar (Blendwirkung) | |
| `Schutzgut_MenschErh_Mas_UB.tex` | OPTIONAL | rarely required |
| `Schutzgut_Landschaft_Mas_UB.tex` | REQUIRED if Landschaft-Eingriff | almost always for solar |
| `Schutzgut_KulturSachgut_Mas_UB.tex` | OPTIONAL | only if KulturSachgut tangiert |

## Schutzgut paired-file integrity

For each Schutzgut, both `_UB` (Bestand) and `_Mas_UB` (Maßnahmen)
files must exist if either is needed:

- `Schutzgut_X_UB.tex` exists but `Schutzgut_X_Mas_UB.tex` missing
  AND Bestand discusses Eingriffe → flag MISSING-Maßnahmen.
- `Schutzgut_X_Mas_UB.tex` exists but `Schutzgut_X_UB.tex`
  empty/stub → flag MISSING-Bestand.

The project's `module-decisions.md` must record include/exclude
choices per Schutzgut with reasoning.

## Required content per Schutzgut Bestand

Each `Schutzgut_X_UB.tex` should contain:

- Brief description of the Schutzgut at the project location
- Methodik / Datenbasis
- Bestandsaufnahme (current state)
- Bewertung (significance)
- Prognose der Auswirkungen

Stub content (Lorem ipsum) flagged as unfilled.

## Required content per Schutzgut Maßnahmen

Each `Schutzgut_X_Mas_UB.tex` should contain:

- Vermeidungsmaßnahmen
- Verringerungsmaßnahmen
- Ausgleichsmaßnahmen (with Eingriffs-Ausgleichs-Bilanzierung)
- Begründung der Auswahl

## Required project-data macros (`Projekt.tex`)

| Macro | Severity |
|---|---|
| `\title{<Berichtstitel>}` | REQUIRED |
| `\author{<Bearbeiter>}` | REQUIRED |
| `\date{\today}` | REQUIRED |
| `\typ` (Berichtstyp = "Umweltbericht") | REQUIRED |
| `\auftrag` (Auftraggeber) | REQUIRED |
| `\titel` (drives titlepage) | REQUIRED |
| `\projekt` (full B-Plan reference) | REQUIRED |
| `\autor` (Bearbeiter) | REQUIRED |
| `\area` (Geltungsbereich, format `XX,X\,ha`) | REQUIRED |

## EAB content (chapter 6)

`EAB_UB.tex` should:

- Quantify Eingriff (Flächengröße, Schwere)
- Quantify Ausgleich (Flächen für Maßnahmen, Punkteberechnung wo
  zutreffend)
- Demonstrate Bilanzierungs-Saldo (Eingriff ≤ Ausgleich)
- Reference §15 BNatSchG-Methodik

PBS-MV: typically uses the **MV-Verfahren zur Eingriffsbilanzierung**
(NSchAG M-V) — confirm citation and methodology references.

## Monitoring content (chapter 7)

`Monitoring_UB.tex` should include:

- CEF-Maßnahmen-Monitoring (intervals; default per
  `monitoring-intervalle` baustein when authored)
- FCS-Maßnahmen-Monitoring (intervals)
- Risikomanagement / Korrekturmechanismus
- Verantwortlichkeit (Vorhabenträger / Gemeinde / UNB)
- §4c BauGB-Bezug

## Zusammenfassung content (chapter 8, §10a Anlage 1)

`Zusammenfassung_UB.tex` is required by §10a BauGB / Nr.3 Anlage 1.
Must be:

- Allgemein verständlich (laienverständlich, kein Fachsprech)
- Self-contained (readable without rest of report)
- Cover Vorhaben, Umweltauswirkungen, Maßnahmen, Fazit

## Bibliographie

`literatur.bib` referenced via `\addbibresource{literatur.bib}`. Must
include:

- BauGB, BNatSchG (current amendments)
- KNE-PV-Naturschutzkriterien (when relevant)
- Methodik-Quellen (Südbeck, Dietz/Kiefer per Schutzgut)
- Lokale / regionale Quellen (LUNG-MV-Datenbestände, MultiBaseCS)

`\printbibliography` at document end.

## Cross-checks

- Each Schutzgut listed in Bestand has corresponding Maßnahmen entry
  (or explicit decision in `module-decisions.md` for exclusion).
- Total Eingriff (EAB chapter) numerically consistent with
  Geltungsbereich-Daten in `Projekt.tex`.
- Methodik-Quellen cited in Section 2 appear in Bibliographie.
- `\area` value matches `\GeltungsbereichHa` from the corresponding
  B-Plan Begründung's `Projektdaten.tex`.

## Severity rollup

Same structure as Begründung. Missing Schutzgut-section that's
required by project context (per `module-decisions.md`) is
block-level.
