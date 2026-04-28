# Gutachten generic — minimum structure

A "Gutachten" is any expert report produced for a specific question
(artenschutzrechtliche Bewertung, FFH-Vorprüfung, Artenschutz-
fachbeitrag, Speziell artenschutzrechtliche Prüfung, LBP, Boden-
gutachten, etc.). They share a common skeleton even when substantive
content differs.

This checklist is the fallback when no specific Gutachten checklist
exists for the doctype. Specific checklists (when authored) inherit
and refine these rules.

Severities: REQUIRED, EXPECTED, CONDITIONAL, OPTIONAL.

## Document class and engine

| Rule | Severity |
|---|---|
| `\documentclass[...]{scrreprt}` (PBS-Bericht style) | REQUIRED |
| OR `\documentclass[...]{scrartcl}` for shorter Gutachten | OPTIONAL alternative |
| Engine = pdflatex | REQUIRED |
| `babel` with `[ngerman]` | REQUIRED |
| `biblatex` with biber, authoryear | EXPECTED |

## Required sections (in order)

| # | Section | Severity | Content |
|---|---|---|---|
| 1 | Veranlassung und rechtlicher Rahmen | REQUIRED | who commissioned, what's being assessed, which laws apply |
| 2 | Methodik und Rahmenbedingungen | REQUIRED | Begehung, Datenbasis, Methodik-Quellen |
| 3 | Ergebnisse der Bestandserfassung / Bewertung | REQUIRED | what was found, what it means |
| 4 | Gefährdungs-/Wirkprognose (paragraph-strukturiert nach einschlägigen Verboten) | REQUIRED | for Artenschutz: §44 Abs.1 Nr.1/2/3 separately. For FFH-VP: §34 BNatSchG |
| 5 | Ausnahme- / Befreiungsprüfung | CONDITIONAL | for Artenschutz: §45 Abs.7 BNatSchG. For FFH-VP: §34 Abs.3-5 BNatSchG |
| 6 | Maßnahmen-/Auflagenkonzept | REQUIRED | M1, M2, ... — Vermeidung, Verringerung, CEF, FCS |
| 7 | Fazit | REQUIRED | clear yes/no on Zulässigkeit unter den genannten Maßgaben |
| 8 | Quellen und Leitfäden | REQUIRED | bibliography or Auswahlliste |
| 9 | Unterschriftenblock | REQUIRED | Ort, Datum, Bearbeiter, Unterschrift |
| 10 | Anhang: Fotodokumentation | OPTIONAL but EXPECTED for site-visit-based Gutachten |

## Required project-data fields

Either via `Projektdaten.tex` (B-Plan style) or `Projekt.tex`
(PBS-Bericht style):

| Field | Severity |
|---|---|
| Auftraggeber | REQUIRED |
| Vorhaben (kurze Bezeichnung) | REQUIRED |
| Behörde (zuständige) | REQUIRED for Gutachten with behördlicher Bezug |
| Bearbeiter (Gutachter-Name) | REQUIRED |
| Bearbeitungszeitraum / Datum | REQUIRED |
| Standort (Gemeinde, Ortsteil, Landkreis) | REQUIRED |

## Section content expectations

### Section 1 — Veranlassung

- Project context (one sentence describing the Vorhaben)
- Rechtsgrundlage of the Gutachten
- Auftrags-Bezug (who asked for what)
- For Bauantrags-related Gutachten: bauplanungsrechtliche Lage
  (§34 BauGB, B-Plan-Geltungsbereich, Innenbereichssatzung)

### Section 2 — Methodik

- Method type (Bestandsaufnahme, Potenzialabschätzung, Worst-Case)
- Data sources (Erhebungen, Datenbanken, Sekundärquellen)
- Methodik-Quellen (Südbeck, Dietz/Kiefer, BfN-Kartieranleitungen)
- Begehungs-Daten (date, time, weather, observer) when applicable
- Limitations / Prognose-Unsicherheiten

### Section 3 — Ergebnisse

- Strukturiert nach Artgruppen / Schutzgütern / Belangen
- Konkrete Funde mit Datum, Ort, Anzahl
- Einordnung jedes Befunds (Anhang II/IV FFH-RL? Rote-Liste?)

### Section 4 — Gefährdungs-/Wirkprognose

For Artenschutz: separate sub-sections per §44 Abs.1 BNatSchG-Verbot:

- Tötungs- und Verletzungsverbot (Nr.1) — mit Signifikanzprüfung
- Störungsverbot (Nr.2) — bezogen auf Erhaltungszustand
- Verbot der Zerstörung von Fortpflanzungs- und Ruhestätten (Nr.3)

For FFH-VP: separate sub-sections per §34-Tatbestand:

- Erheblichkeitsabschätzung
- Beeinträchtigung der Erhaltungsziele
- Kumulative Wirkung

### Section 5 — Ausnahmeprüfung (when required)

Three-step structure:

- Ausnahmegrund (welche §-Nr. einschlägig)
- Zumutbare Alternativen
- Erhaltungszustand (keine Verschlechterung)

### Section 6 — Maßnahmenkonzept

Numbered M1, M2, M3, ... Per Maßnahme:

- Beschreibung
- Wirkung
- Räumliche Lage / Umfang
- Zeitpunkt / Reihenfolge
- Pflege / Unterhaltung
- Sicherung (rechtlich, vertraglich)
- Monitoring (when applicable)

CEF: explizit bezeichnet, Wirksamkeit-vor-Eingriff nachgewiesen.
FCS: explizit bezeichnet, Erhaltungszustand-Bezug ausgeführt.

### Section 7 — Fazit

- Klare Aussage: zulässig / zulässig unter Maßgabe / nicht zulässig
- Bei "zulässig unter Maßgabe": welche M1-MN zwingend
- Bei "nicht zulässig" ohne Ausnahme: was wäre erforderlich

### Section 8 — Quellen

Minimum:

- Einschlägige Gesetze mit aktuellen Fassungen
- Methodik-Standards (mindestens 1 pro untersuchter Artgruppe)
- Spezielle Literatur zum Vorhabentyp
- Lokale/regionale Quellen

### Section 9 — Unterschriftenblock

Tabbing-Block mit:

- Ort, Datum (ohne Platzhalter im Final)
- Unterschrift des Bearbeiters
- Name + Qualifikation gedruckt unter der Unterschrift
- Bei mehreren Bearbeitern: separate Blöcke

## Cross-checks

- Each gesetzliche Tatbestand cited in Section 4 has current
  amendment date.
- Each Maßnahme M-N referenced in Fazit appears in Maßnahmenkonzept
  and vice versa.
- Each Methodik-Quelle in Section 2 appears in Section 8.
- Bearbeiter-Name in Unterschriftenblock matches Projekt.tex
  `\autor` macro.

## Limits

Doctype-specific structural rules (e.g. SPA-Hauptprüfung's eigene
Gliederung mit Verbreitungsgebiete-Karten + Reproduktionsmonitoring)
need their own checklist file. This generic checklist is the floor;
specifics raise the ceiling.

When a specific Gutachten-checklist is authored, this checklist's
required-sections list serves as the inheritance base.

## Severity rollup

Same structure as Begründung. Missing Section 1-9 = block. Missing
Unterschriftenblock or unfilled placeholder in it = block-level —
Gutachten ohne Unterschrift unakzeptabel für Behörden.
