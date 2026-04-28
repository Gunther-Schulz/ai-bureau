# draft-textteil-b — drafting workflow

Detailed section-by-section workflow for drafting a B-Plan Begründung
from source materials. Loaded by SKILL.md when this skill is active.

## Section drafting order

Match the canonical B-Plan Begründung section order documented in
`memory/universal/style/style-spec.md`. Each section is drafted to a
checkpoint then user reviews before next section starts.

```
1.  Titelseite
2.  Aufgaben und Inhalte der Planung
3.  Grundlagen der Planung — Aufstellungsverfahren
4.  Geltungsbereich
5.  Planinhalte und Festsetzungen
6.  Ver- und Entsorgungsanlagen
7.  Vorbeugender Brandschutz — Löschwasserversorgung
8.  Gewässerschutz
9.  Bodenschutz
10. Immissions- und Klimaschutz — Blendwirkung
11. Altlasten und Altlastverdachtsflächen
12. Belange der Forst
13. Denkmalschutz
14. Kataster- und Vermessungswesen
15. Alternativprüfung
16. Kosten und Finanzierung
17. Stand des Aufstellungsverfahrens
18. Ergebnisse Beteiligung
19. Änderungen Vorentwurf → Entwurf
20. Flächenbilanz
21. Sicherung der Plandurchführung
22. Quellenverzeichnis
23. Signatur
```

Order is canonical but not rigid; project-specific reordering
allowed with explicit decisions.md entry.

## Per-section workflow (applied to every section)

### 1. Identify required content

Read the section's canonical scope from
`<repo>/plugin/skills/validate-checklist/references/checklists/
b-plan-begruendung.md`:

- What this section MUST contain.
- What it SHOULD contain (recommended).
- What's project-specific.

### 2. Pull inputs

For each section, identify which `inputs/` are relevant:

| Section | Typical inputs |
|---|---|
| Aufgaben und Inhalte | briefing, Auftraggeber-Vorgaben |
| Aufstellungsverfahren | Schriftverkehr, Aufstellungsbeschluss, Behörden-Stellungnahmen |
| Geltungsbereich | Vermessung, GIS-data |
| Planinhalte | briefing, technische Daten |
| Erschließung | Erschließungs-Konzept, Versorgungsträger |
| Brandschutz | Brandschutzkonzept (extern oder PBS) |
| Gewässerschutz | Wasserrechtliche Stellungnahmen, GIS Wasser |
| Bodenschutz | Bodengutachten, BBB-Konzept |
| Klimaschutz | KNE-Studien, Blendgutachten |
| Forst | Forstbehörde-Stellungnahme |
| Denkmal | ULD-Stellungnahme, Bodendenkmalpflege |
| Alternativprüfung | Standortwahl-Dokumentation |
| Kosten | Vorhabenträger-Kalkulation |

### 3. Corpus search

For each section, search past projects:

```
search_corpus(
  query="<section-topic> <doctype> <Verfahren-typ>",
  filter={
    doctype: "b-plan-begruendung",
    section: "<section-name>"
  },
  k=5
)
```

Surface 2-3 best hits as inspiration. User picks a reference (or
declines).

### 4. Baustein application

For sections with reusable patterns:

| Section | Likely bausteine |
|---|---|
| Brandschutz | brandschutz-pv-loeschwasser-spec |
| Bodenschutz | bbb-konzept-spec |
| Klimaschutz | blendwirkung-pv-arg, klimaschutz-pv-positiv-arg |
| Alternativprüfung | innenbereich-vor-aussenbereich-arg |
| Eingriff (Section 5) | eingriffs-argumentation-solar |

When applying a baustein:
- Read content from baustein file.
- Adapt project-specific values (\Gemeinde, \BPlan, \GeltungsbereichHa, etc.).
- Cite in History section: "Applied baustein <name> for project <id>."

### 5. Draft prose

Apply korrektur-rules during drafting:

- German quotes: `\glqq...\grqq{}` not `"..."`.
- Non-breaking spaces: `~` before units (`5~m`, `30,37~ha`), `§`
  (`§~9 BauGB`).
- Number format: comma decimal, dot thousands (`30.370` not `30,370`
  or `30370`).
- Hyphenation hints for long compounds in `\hyphenation{...}` if
  preamble doesn't already cover them.
- Source line wrap: ~80 characters per line for diff-friendliness.

Section content ranges:
- Short (Brandschutz, Denkmalschutz when not relevant): 200-400
  words.
- Medium (Geltungsbereich, Erschließung): 600-1200 words.
- Long (Planinhalte, Eingriff): 1500-3000+ words.

### 6. User checkpoint per section

After drafting a section:

```
Section "<name>" drafted at <path>.
Sources used: <list of inputs cited, bausteine applied, corpus
references>.
Length: ~<word count>.

Review now, or continue to next section?
```

User options:
- review-now → switch to review mode for this section
- continue → next section
- pause → save and resume later

### 7. Compile checkpoints

After every 3-4 sections, run compile_latex on the work-in-progress
document:

- Catches LaTeX errors early.
- Validates Projektdaten.tex macros are all defined.
- Verifies preamble configuration.
- Surface compile log warnings (overfull boxes, undefined refs).

If compile fails: address errors before continuing. Don't accumulate
broken state.

## Verfahren-specific section variations

### §13 vereinfachtes Verfahren

- Section "Frühzeitige Beteiligung" can be shortened or omitted (§13
  Abs.2 Nr.1 erlaubt das Auslassen).
- Section "Umweltbericht" entfällt (§13 Abs.3).
- Section "Stand des Aufstellungsverfahrens" mentioned that vereinfachtes
  Verfahren angewendet wurde, mit Begründung.

### §13a beschleunigtes Verfahren (Innenentwicklung)

- Same as §13 erleichterungen.
- Section "Geltungsbereich" must justify Innenentwicklungs-Lage und
  ggf. Vorprüfung-Ergebnis (für §13a Abs.1 Satz 2 Nr.2 Variante).
- Eingriffs-Ausgleichs-Bilanzierung entfällt für <20.000 m²
  Variante (§13a Abs.2 Nr.4).

### §12 vorhabensbezogener B-Plan

- Section "Planinhalte und Festsetzungen" verweist auf den V&E-Plan
  (Vorhaben- und Erschließungsplan).
- Section "Vorhabenträger" zusätzlich (kein Pflichtteil aber im PBS-
  Konzept üblich).
- Section "Durchführungsvertrag" oder Hinweis darauf in
  Sicherung der Plandurchführung.

## Module decisions log entries

For every optional section the user includes or excludes, append to
`<project>/_ai/module-decisions.md`:

```markdown
## B-Plan/Begründung

| Date | Module | Decision | Reasoning |
|---|---|---|---|
| <today> | <section>.tex | included | <reason from input/Stellungnahme> |
| <today> | <section>.tex | excluded | <reason> |
```

## End-of-draft handoff

When all canonical sections drafted + compile passes:

1. Final compile_latex run with full TOC + Listoftables.
2. Surface PDF path to user.
3. Update `_ai/state.md`:
   - `lifecycle: internal-review` (if was draft)
   - `phase`: confirm with user (likely "Vorentwurf-fertig" or "4-billigungs-prep")
4. Append History entry: "Begründung-Erstentwurf fertig <date>".
5. Hand control to orchestrator for Phase B review entry.

## What not to do

- **Don't auto-submit Stellungnahmen-prüfung** as part of drafting.
  That's Phase B (review-draft) work.
- **Don't write to ProjektBeispiel-B-Plan/** or Vorlagen/Latex/. Those
  are templates, not project artifacts.
- **Don't compile the Festsetzungen** alongside the Begründung —
  draft-textteil-c handles that. They're separate LaTeX projects.
- **Don't decide Verfahrenstyp** without user confirmation. Surface
  gap if ambiguous.
- **Don't ignore failed compiles**. Fix before continuing.
