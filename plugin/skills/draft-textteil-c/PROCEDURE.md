# draft-textteil-c — drafting workflow

Detailed rule-by-rule and section-by-section workflow for drafting
B-Plan Textliche Festsetzungen.

## Document structure (top-down)

```
1. Header (Satzung der Gemeinde ...)
2. Präambel
3. Teil A reference (placeholder)
4. \section*{Teil B Text}
5. \section*{I. Planungsrechtliche Festsetzungen gemäß §~9 BauGB}
   5.1 Rule 1: Art der baulichen Nutzung
   5.2 Rule 2: Maß der baulichen Nutzung
   5.3 Rule 3: Flächen + Maßnahmen Schutz
   5.4 Rule 4: Artenschutzrechtliche (conditional)
   5.5 Rule 5: Örtliche Bauvorschriften LBauO M-V
6. \section*{Verfahrensvermerke} (13 entries)
7. \section*{Hinweis} (Denkmalschutz §11 DSchG M-V)
8. Centered title-block
9. \section*{Rechtsgrundlagen} (bullet list)
```

## Per-rule workflow

### Rule 1 — Art der baulichen Nutzung (§9 Abs.1 BauGB)

Required nested sub-rules:

```
1.1 Baugebiet
1.2 Art der Nutzung im SO
1.3 Nutzungszeitraum/Folgenutzung (für Solar PV mit zeitlicher
    Begrenzung — meist 30 Jahre)
```

For Solar PV typical content:
- Sonstiges Sondergebiet gem. §11 (2) BauNVO
- Energiegewinnung auf der Basis solarer Strahlungsenergie (SO EBS)
- Zwischennutzung gem. §9 (2) Satz 1 Nr.1 BauGB
- Folgenutzung landwirtschaftlich (§9 Abs.1 Nr.18a BauGB)
- 30-Jahre-Frist mit konkretem Ablaufdatum

Source for Vorhaben-spezifische Werte: `get_project_state(project).state` + briefing inputs (state.md is gate-only per meta-rule 4).

### Rule 2 — Maß der baulichen Nutzung

Required: maximale Höhe baulicher Anlagen. Solar PV typical 4,00 m
incl. Höhenbeschränkung-Ausnahme für technische Aufbauten. NHN-Bezug
(DHHN 2016) Standard.

Aufschüttungen/Abgrabungen ±0,50 m typischer Wert.

### Rule 3 — Schutz/Pflege/Entwicklung Boden, Natur, Landschaft (§9 Abs.1 Nr.20)

Common sub-rules for Solar PV:

```
3.1 Einzäunung — max. 2,20 m mit Übersteigschutz, Kleintierdurchlass
3.2 Befestigung Wege/Zufahrten — wasser- und luftdurchlässig
3.3 Niederschlagswasser — Versickerung erlaubnisfrei
3.4 Zwischenmodulflächen + Grünlandpflege — Regiosaatgut, Mahd nach
    1. Juli, Mahdgut abtransportieren
3.5 Bodenkundliche Baubegleitung (BBB)
3.6 Verhalten bei archäologischen Funden
```

Source for konkrete Werte: site-specific Bodenschutz-Konzept,
Gemeinde-Vorgaben.

### Rule 4 — Artenschutzrechtliche Festsetzungen (conditional)

Required if §44 BNatSchG triggered (almost always for Solar PV with
Bestand-Funden or hohem Potenzial).

Common content:

```
4.1 Bauzeitenregelung — Baufeldvorbereitung 1.10. - 29.2.; bei
    Arbeit zwischen 1.3. - 30.9. öBB + Vergrämungsmaßnahmen
4.2 CEF-Maßnahme — z.B. Aufwertung Grünland, Steinriegel-Anlage
4.3 (optional) FCS-Maßnahmen — z.B. fassadenintegrierte Fledermaus-
    quartiere
```

Source: Artenschutzbewertung (eigenständige Gutachten — meist
Hendrik) + Stellungnahmen UNB.

Cross-check with Begründung: Artenschutzrechtliche Argumentation
und §45-Nr.5-Ausnahmebegründung muss konsistent sein.

### Rule 5 — Örtliche Bauvorschriften (§86 Abs.3 LBauO M-V)

Common content:

```
5.1 Geländeregulierung — ±0,50 m
5.2 Sicherheits- und Informationsmaßnahmen am Tor — Schlüsselsafe
    Feuerwehr, Hinweis Anlagenbetreiber
```

## Verfahrensvermerke — 13-entry sequence

Per `bauleitplanung-phasen.md` Section 9. Each entry follows pattern:

```latex
\item <Verfahrensschritt-Beschreibung mit Verweis auf
       BauGB/LPlG/etc. + Datum + Bekanntmachungsblatt>

      \begin{tabbing}
        \hspace{6cm} \= \hspace{4cm} \= \kill
        \Gemeinde{}, \> Siegel \> \hspace{8pt} <Bürgermeister> \\
        \> \> — Bürgermeister —
      \end{tabbing}
```

Placeholder Daten `................` für unausgefüllte Termine
(typisch beim Vorentwurf).

## Hinweis (Denkmalschutz, state-specific)

Standard Denkmalschutz-Hinweis per the project's bundesland (e.g.
§11 DSchG-MV in Mecklenburg-Vorpommern). Verbatim wording lives in
the state-leitfaden corpus — retrieve via `search_corpus(filter=
{source_subtype: leitfaden, jurisdiction: <bundesland>})` keyed on
"Denkmalschutz Hinweis" and use the result verbatim in the
Festsetzungen.

## Rechtsgrundlagen — Bullet List

Minimum required entries (each citation must include current
amendment form, fetched from references corpus — never written
from training memory):

Federal (always required):
- BauGB
- BauNVO
- PlanZV
- BNatSchG

State (required, per project bundesland — resolved from state-
extension manifest):
- Kommunalverfassung des Landes (e.g. KV-MV)
- Naturschutzausführungsgesetz des Landes (e.g. NatSchAG-MV)
- Landesbauordnung (e.g. LBauO-MV)

Optional federal (include if cited in body): BImSchG, WHG, BBodSchG,
BWaldG.

Optional state (include if cited in body, per state extension):
state-Wassergesetz, state-Denkmalschutzgesetz, etc.

For each citation, fetch current amendment form via:
```
read_corpus_file(<references_root>/gesetze/{bund|<state>}/<id>.md)
```
The cited form is `<id> i.d.F. der Bekanntmachung vom <date>,
zuletzt geändert durch <art> des Gesetzes vom <date>` — exact text
from the reference corpus, never reconstructed.

verify-citations skill checks each amendment date against the
references-manifest (federal-core + state-extension). Drift → flag.

## Compile + verify

After every major section authored:

1. `compile_latex(<project>/B-Plan/Festsetzungen)`.
2. Verify single-page output (`pdfinfo final.pdf` shows 1 page).
3. If overflow (>4000pt height): paperheight is too small. Surface
   for user — typically split into two-pager Satzung Variante (rare).

## Cross-consistency check (with Begründung)

When Festsetzungen authored alongside or after Begründung:

1. Read both `Projektdaten.tex` files (Begründung's and
   Festsetzungen').
2. Diff macros: must be identical for shared values (\Gemeinde,
   \BPlanNr, \BPlanName, \BPlanTyp, \GeltungsbereichHa, etc.).
3. Verify rule content aligns with Begründung argumentation:
   - Rule 1 (Nutzungszeitraum 30 Jahre) ↔ Begründung Folgenutzungs-
     section
   - Rule 3.4 (Grünlandpflege Mahd 1.7.) ↔ Begründung Bodenschutz
     + Klima-Kapitel
   - Rule 4 (Artenschutz CEF) ↔ Begründung Artenschutz-Kapitel
   - Rule 5.1 (Geländeregulierung ±0.5m) ↔ Begründung
     Bodenschutz/Bauhöhen
4. Surface inconsistencies for resolution before declaring done.

## Module decisions log entries

Per orchestrator Checkpoint 6.3:

```markdown
## B-Plan/Festsetzungen

| Date | Module | Decision | Reasoning |
|---|---|---|---|
| <today> | Artenschutzrechtliche Festsetzungen.tex | included | §44 BNatSchG triggered von Stellungnahme UNB |
| <today> | Wasserwirtschaftliche Festsetzungen.tex | excluded | keine wasserrelevanten Eingriffe |
```

## End-of-draft handoff

When all required rules + Verfahrensvermerke + Hinweis +
Rechtsgrundlagen drafted:

1. Final compile_latex with full structure.
2. Verify single-page output.
3. Cross-consistency check with Begründung.
4. Surface PDF + .tex source paths.
5. Call `update_project_state(project, updates={}, body_append="- <YYYY-MM-DD> — Festsetzungen-Erstentwurf fertig.")`. Never write state.md directly (meta-rule 4).
6. Hand control to orchestrator for Phase B review.

## What not to do

- **Don't fabricate Verfahrensvermerke-Daten**. Use
  `................` placeholders for terms not yet known. Daten
  konkret nur einzutragen wenn Verfahrensschritt tatsächlich
  abgeschlossen.
- **Don't include rules that aren't justified in Begründung**.
  Festsetzungen-Inhalt muss von Begründung getragen sein —
  Verwaltungsgericht-Abwägungs-Disziplin.
- **Don't compile to multi-page PDF** silently. Single-page is the
  Doctype-B contract; surface overflows.
- **Don't ignore cross-consistency failures**. Surface for user;
  inconsistent doc-pair will be rejected at UNB-Prüfung.
