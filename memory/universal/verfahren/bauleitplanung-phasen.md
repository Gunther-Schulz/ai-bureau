---
references_used:
  - {law: BauGB, paragraph: §1a Abs.2}
  - {law: BauGB, paragraph: §2 Abs.1}
  - {law: BauGB, paragraph: §2 Abs.4}
  - {law: BauGB, paragraph: §2a}
  - {law: BauGB, paragraph: §3 Abs.1}
  - {law: BauGB, paragraph: §3 Abs.2}
  - {law: BauGB, paragraph: §4 Abs.1}
  - {law: BauGB, paragraph: §4 Abs.2}
  - {law: BauGB, paragraph: §4a Abs.2}
  - {law: BauGB, paragraph: §4a Abs.3}
  - {law: BauGB, paragraph: §4a Abs.5}
  - {law: BauGB, paragraph: §4c}
  - {law: BauGB, paragraph: §6a}
  - {law: BauGB, paragraph: §8 Abs.2}
  - {law: BauGB, paragraph: §9 Abs.2a}
  - {law: BauGB, paragraph: §9 Abs.2b}
  - {law: BauGB, paragraph: §10 Abs.1}
  - {law: BauGB, paragraph: §10 Abs.2}
  - {law: BauGB, paragraph: §10 Abs.3}
  - {law: BauGB, paragraph: §10a}
  - {law: BauGB, paragraph: §12}
  - {law: BauGB, paragraph: §13}
  - {law: BauGB, paragraph: §13 Abs.2}
  - {law: BauGB, paragraph: §13a}
  - {law: BauGB, paragraph: §13b}
  - {law: BauGB, paragraph: §44}
  - {law: BauGB, paragraph: §214}
  - {law: BauNVO, paragraph: §19 Abs.2}
  - {law: BImSchG, paragraph: §50}
---

# Bauleitplanung-Phasen (Bebauungsplan)

The Bebauungsplan-Verfahren is structurally federal (BauGB). State-
specific touches (raumordnungsbehördliche Beteiligung per the
respective Landesplanungsgesetz, publication channels per state)
overlay the federal procedure. This file documents the canonical
Regelverfahren plus the two simplified variants, and how each phase
maps to project state, folder structure, and Verfahrensvermerk
identifiers.

**Memory-vs-RAG rule (per ARCHITECTURE.md):** this document uses
§-references **as labels only** for navigation. The actual law text
and the verbatim Verfahrensvermerk wording (which is state-specific
and per Verfahrenstyp) are NOT here. Both are retrieved on demand
from the references corpus:

- `search_corpus(filter={source_subtype: gesetz-bund, reference_id: BauGB})`
  for federal law text.
- `search_corpus(filter={source_subtype: leitfaden, jurisdiction: <state>})`
  for state-flavored Verfahrensvermerk wording.

State-specific overlays (per the project's `state.md.bundesland`)
live in the office's references corpus and extension manifest, not
in this domain document.

**Authoritative federal source:** BauGB current text via
`gesetze-im-internet.de/baugb/` — fetched and indexed by
`research-references` into `office_config.paths.references_root`.

---

## 1. The two-axis structure

Two parallel beteiligungs-axes run through every Verfahren:

| Axis | Frühzeitige Phase | Förmliche Phase |
|---|---|---|
| **Öffentlichkeit** | §3 Abs.1 BauGB | §3 Abs.2 BauGB |
| **Behörden / TöB** | §4 Abs.1 BauGB | §4 Abs.2 BauGB |

§4a Abs.2 BauGB explicitly permits running both axes simultaneously
(the frühzeitige rounds in parallel, the förmlichen rounds in
parallel). Common practice does this — there is one "frühzeitige
Beteiligung" event covering both Öffentlichkeit and Behörden, and
one "förmliche Beteiligung" event likewise.

---

## 2. Regelverfahren — phase by phase

### Phase 0 — Aufstellungsbeschluss

The Gemeindevertretung formally decides to start the planning.
Required when starting a B-Plan; the Beschluss must be ortsüblich
bekannt gemacht (§2 Abs.1 BauGB).

- **Documents:** Aufstellungsbeschluss-Vorlage, amtliche Bekanntmachung.
- **Project state:** `draft` (orchestrator default for new projects).
- **Verfahrensvermerk #1:** corresponds to this phase. Canonical wording
  in the state-leitfaden corpus (per project's bundesland).
- **Folder:** `B-Plan/Aufstellungsverfahren/0-aufstellungsbeschluss/`.

### Phase 1 — Raumordnungsbehördliche Beteiligung (state-specific)

Most Bundesländer require beteiligung der raumordnungs-zuständigen
Stelle per the respective Landesplanungsgesetz. Federal BauGB does
not require this directly. The exact §-reference and Verfahrensvermerk
wording lives in the state extension manifest / leitfaden corpus for
the project's `bundesland`. Often happens early, before or alongside
frühzeitige Beteiligung.

- **Documents:** Anschreiben an die Raumordnungsbehörde mit
  Vorentwurf-Material.
- **Verfahrensvermerk #2:** corresponds to this phase; resolve §-ref
  and wording from the state-leitfaden.
- **Folder:** `B-Plan/Aufstellungsverfahren/1-raumordnung/`.

### Phase 2 — Frühzeitige Beteiligung (Vorentwurf)

Both §3 Abs.1 (Öffentlichkeit) and §4 Abs.1 (Behörden / TöB) typically
run together (per §4a Abs.2). The "Vorentwurf" is the planning
document used for this phase — usually less detailed than the
Entwurf, sufficient to convey Ziele, Lösungsalternativen, and
voraussichtliche Auswirkungen.

#### Phase 2a — §3 Abs.1 frühzeitige Öffentlichkeitsbeteiligung

- **Format:** öffentliche Unterrichtung; Gelegenheit zur Äußerung
  und Erörterung. Often an Einwohnerversammlung. Kinder und
  Jugendliche sind ausdrücklich umfasst (per §3 Abs.1 BauGB).
- **Documents:** Vorentwurf (Plan + Begründung), Anschreiben /
  Einladung zur Öffentlichkeitsversammlung.
- **Verfahrensvermerke #3 / #4:** correspond to this phase
  (Unterrichtungs-Vermerk + ggf. separater Vermerk für Einwohner-
  informations-Termin). Canonical wording in state-leitfaden.
- **Folder:** `B-Plan/Aufstellungsverfahren/2a-frueh-oeffentlichkeit/`.

#### Phase 2b — §4 Abs.1 frühzeitige Behördenbeteiligung

- **Format:** Behörden und sonstige Träger öffentlicher Belange
  (whose Aufgabenbereich berührt sein könnte) sind zu unterrichten
  und zur Äußerung aufzufordern, auch zu Umfang und Detaillierungsgrad
  der Umweltprüfung (per §2 Abs.4 BauGB).
- **Documents:** Anschreiben mit Vorentwurf-Material an alle TöB,
  TöB-Liste.
- **Verfahrensvermerk #5:** corresponds to this phase. Canonical
  wording in state-leitfaden.
- **Folder:** `B-Plan/Aufstellungsverfahren/2b-frueh-toeb/` containing
  Anschreiben, TöB-Liste, eingehende Stellungnahmen.

### Phase 3 — Auswertung Vorentwurf-Stellungnahmen

The Stellungnahmen from §3 Abs.1 / §4 Abs.1 are evaluated. Output
feeds into the Entwurf. This phase has no Verfahrensvermerk per se
but is the work-bridge between Vorentwurf and Entwurf.

- **Documents:** Auswertung der Stellungnahmen (could be a tabular
  summary), revised draft.
- **Project state:** moves toward `internal-review` as the Entwurf
  takes shape.
- **Folder:** `B-Plan/Aufstellungsverfahren/3-auswertung-vorentwurf/`.

### Phase 4 — Billigungs- und Auslegungsbeschluss

The Gemeindevertretung billigt den Entwurf and bestimmt die
Auslegung. This is a prerequisite for §3 Abs.2 / §4 Abs.2.

- **Documents:** Entwurf (Plan + Begründung) als billigungsreife
  Fassung, Sitzungsvorlage, Beschluss-Protokoll.
- **Verfahrensvermerk #6:** corresponds to this phase. Canonical
  wording in state-leitfaden.
- **Folder:** `B-Plan/Aufstellungsverfahren/4-billigungsbeschluss/`.

### Phase 5 — Förmliche Beteiligung (Entwurf)

Both §3 Abs.2 and §4 Abs.2 run, typically simultaneously per §4a Abs.2.

#### Phase 5a — §3 Abs.2 öffentliche Auslegung

- **Format:** Veröffentlichung im Internet für mindestens 30 Tage
  (Frist per §3 Abs.2 Satz 1 BauGB) PLUS mindestens eine andere
  leicht erreichbare Zugangsmöglichkeit. Veröffentlichungsfrist und
  Hinweise auf Stellungnahme-Möglichkeit müssen vorab ortsüblich
  bekanntgemacht werden.
- **State-specific:** most Bundesländer have a central B-Plan
  Landesportal as a supplementary publication channel. Resolve the
  exact portal URL and required Bekanntmachungsmittel from the
  project's state-leitfaden.
- **Bekanntmachungsmittel:** amtliches Bekanntmachungsblatt des Amts
  + Homepage des Amts + ggf. Landesportal (state-specific list in
  state-leitfaden).
- **Documents:** Auslegungs-Bekanntmachung, Auslegungs-Exemplar des
  Entwurfs, ggf. wesentliche umweltbezogene Stellungnahmen die
  bereits vorliegen.
- **Verfahrensvermerk #7:** corresponds to this phase. Canonical
  wording in state-leitfaden — note: includes specifics like the
  Internet portal URL and amtliches Bekanntmachungsblatt name, both
  state-/Amts-specific.
- **Folder:** `B-Plan/Aufstellungsverfahren/5a-foerml-oeffentlichkeit/`.

#### Phase 5b — §4 Abs.2 förmliche Behördenbeteiligung

- **Format:** Stellungnahmen sind innerhalb eines Monats abzugeben,
  mindestens 30 Tage. Bereitstellung soll elektronisch erfolgen
  (per §4 Abs.2 Satz 2 BauGB).
- **Documents:** Anschreiben + Entwurfs-Exemplar an alle TöB,
  aktualisierte TöB-Liste, eingehende Stellungnahmen.
- **Verfahrensvermerk #8:** corresponds to this phase. Canonical
  wording in state-leitfaden.
- **Folder:** `B-Plan/Aufstellungsverfahren/5b-foerml-toeb/`.

### Phase 6 — Abwägung

The Gemeinde prüft die fristgemäß abgegebenen Stellungnahmen aus
beiden Beteiligungsrunden und gewichtet sie ab. Ergebnis ist
mitzuteilen (per §3 Abs.2 Satz 6, §4a Abs.5 BauGB).

- **Documents:** Abwägungstabelle (Stellungnahme → Antwort →
  Abwägungsergebnis pro Eintrag). Eigenes Doctype (`abwaegung` in
  `doctypes.yaml`).
- **Verfahrensvermerk #9:** corresponds to this phase. Canonical
  wording in state-leitfaden.
- **Project state:** `internal-review` → `revision-requested` (if
  major Stellungnahmen forcen Änderungen) → back through earlier
  phases per §4a Abs.3 if Grundzüge berührt werden, or directly
  forward.
- **Folder:** `B-Plan/Aufstellungsverfahren/6-abwaegung/`.

### Phase 7 — Erneute Auslegung (falls erforderlich)

If the Entwurf nach §4a Abs.3 BauGB changed (Grundzüge berührt),
erneute Auslegung nach §3 Abs.2 ist erforderlich (kann aber verkürzt
werden, und kann auf die berührte Öffentlichkeit + TöB beschränkt
werden, wenn Grundzüge nicht berührt).

- Loops back to Phase 5 with verkürzten Fristen.
- Each loop adds Verfahrensvermerke. Office practice numbers them
  (z. B. "2. Auslegung", "3. Auslegung").

### Phase 8 — Katastermäßige Bestätigung

Vor Satzungsbeschluss bestätigt der öffentlich bestellte Vermesser
den katastermäßigen Bestand im Geltungsbereich.

- **Verfahrensvermerk #10:** corresponds to this phase. State-flavored
  wording in state-leitfaden (typically with Vorbehalt zur
  lagerichtigen Darstellung in 1:2.000 Maßstab).

### Phase 9 — Satzungsbeschluss

Die Gemeinde beschließt den Bebauungsplan als Satzung (per §10 Abs.1
BauGB). Ohne weitere Genehmigung ist der Plan damit beschlussreif —
es sei denn, ein Genehmigungserfordernis besteht (siehe Phase 10).

- **Documents:** Satzungsbeschluss-Vorlage, Beschluss-Protokoll.
- **Project state:** `internal-review` → ready for `sent-to-authority`
  (if Genehmigung erforderlich) or directly to `finalized`-near.

### Phase 10 — Höhere Verwaltungsbehörde (falls Genehmigung erforderlich)

Genehmigung der höheren Verwaltungsbehörde ist erforderlich nur in
den Fällen §10 Abs.2 BauGB (Bebauungspläne nach §8 Abs.2 Satz 2,
Abs.3 Satz 2, Abs.4) — insb. für Bebauungspläne, die nicht aus dem
Flächennutzungsplan entwickelt sind, und für vorzeitige Bebauungspläne.
Praxis: B-Pläne, die vom F-Plan abweichen, sind regelmäßig
genehmigungspflichtig.

- **Documents:** Genehmigungsantrag, ggf. Auflagen / Nebenbestimmungen.
- **Verfahrensvermerk #11:** corresponds to this phase. Canonical
  wording in state-leitfaden.
- **Project state:** `sent-to-authority` → `awaiting-response` →
  `revision-requested` (if Auflagen) → loop or proceed.

### Phase 11 — Ausfertigung

Der Bürgermeister fertigt den Bebauungsplan aus.

- **Verfahrensvermerk #12:** corresponds to this phase. Canonical
  wording in state-leitfaden.

### Phase 12 — Bekanntmachung des Inkrafttretens

Erteilung der Genehmigung (oder Beschluss, falls keine Genehmigung
erforderlich) ist ortsüblich bekannt zu machen. Mit der Bekanntmachung
tritt der Bebauungsplan in Kraft (per §10 Abs.3 BauGB).

- **Documents:** Bekanntmachungstext mit den erforderlichen Hinweisen
  (Geltendmachung von Verfahrens-/Formfehlern per §214 BauGB; Erlöschen
  Entschädigungsansprüche per §44 BauGB; ggf. state-Kommunalverfassung-
  spezifische Hinweise — letztere im state-leitfaden).
- **Verfahrensvermerk #13:** corresponds to this phase. Canonical
  wording in state-leitfaden — note: includes state-specific
  Hinweise auf Kommunalverfassung des Landes.
- **Project state:** `finalized` after Bekanntmachung. Then `archived`
  once the project is closed administratively.

### Phase 13 — §10a Zusammenfassende Erklärung

Dem in Kraft getretenen Bebauungsplan ist eine zusammenfassende
Erklärung beizufügen über die Art und Weise, wie die Umweltbelange
und die Beteiligungsergebnisse berücksichtigt wurden, und über die
Gründe der Auswahl. Stellt einen integralen Bestandteil dar.

- **Documents:** Zusammenfassende Erklärung (separates Dokument oder
  als Anhang zur Begründung). Auch ins Internet einzustellen.

---

## 3. Vereinfachtes Verfahren (§13 BauGB)

Anwendbar wenn:
- Änderung / Ergänzung berührt nicht die Grundzüge der Planung, ODER
- Aufstellung in §34-Gebiet ohne wesentliche Veränderung des
  Zulässigkeitsmaßstabs, ODER
- Plan enthält nur Festsetzungen nach §9 Abs.2a oder Abs.2b BauGB.

UND:
- Keine UVP-Pflicht der zugelassenen Vorhaben.
- Keine Anhaltspunkte auf Beeinträchtigung Schutzgüter §1 Abs.6
  Nr.7b BauGB.
- Keine schweren-Unfälle-Pflichten §50 BImSchG.

**Was kann entfallen** (per §13 Abs.2 BauGB):
- Frühzeitige Unterrichtung §3 Abs.1 / §4 Abs.1 (kann entfallen).
- Stattdessen: Öffentlichkeit / TöB Gelegenheit zur Stellungnahme in
  angemessener Frist — alternativ kann auch direkt §3 Abs.2 / §4 Abs.2
  durchgeführt werden.
- Umweltprüfung (§2 Abs.4) entfällt, Umweltbericht (§2a) entfällt,
  Hinweise auf umweltbezogene Informationen (§3 Abs.2 Satz 4) entfällt,
  zusammenfassende Erklärung (§6a / §10a) entfällt, Überwachung (§4c)
  entfällt.

**Typische Anwendung:** Selten direkt anwendbar bei neu aufgestellten
B-Plänen mit UVP-Vorprüfungs-Pflicht. Gelegentlich relevant bei
Änderungen bestehender B-Pläne.

---

## 4. Beschleunigtes Verfahren (§13a BauGB) — Innenentwicklung

Bebauungsplan für Wiedernutzbarmachung, Nachverdichtung, oder andere
Maßnahmen der Innenentwicklung.

**Voraussetzungen** (per §13a BauGB):
- Zulässige Grundfläche (per §19 Abs.2 BauNVO):
  - <20.000 m² → ohne Vorprüfung anwendbar.
  - 20.000 – 70.000 m² → Vorprüfung des Einzelfalls erforderlich
    (Anlage 2 BauGB), ergibt voraussichtlich keine erheblichen
    Umweltauswirkungen.
- Keine UVP-Pflicht der ermöglichten Vorhaben.
- Keine Anhaltspunkte für FFH/Vogelschutz-Beeinträchtigung.
- Keine schweren-Unfälle-Pflichten.

**Verfahrenserleichterungen** (gleich wie §13 Abs.2/3 BauGB):
- Frühzeitige Beteiligung kann entfallen.
- Umweltprüfung / Umweltbericht / Zusammenfassende Erklärung können
  entfallen.
- Eingriffe gelten als bereits vor planerischer Entscheidung
  zulässig (per §13a Abs.2 Nr.4 BauGB) — keine Eingriffs-Ausgleichs-
  Bilanzierung erforderlich für <20.000 m² Variante.
- Plan kann von F-Plan abweichen, FNP wird per Berichtigung angepasst.

**Typische Anwendung:** Plan auf bereits versiegelte oder im
Innenbereich gelegene Flächen.

---

## 5. §13b BauGB

§13b (Wohnnutzung am Ortsrand, beschleunigtes Verfahren ergänzend)
existed in earlier BauGB versions, was struck down by the BVerwG
2022, and reintroduced in modified form in 2024.

**Action item:** if a project requires §13b, run `research-references`
to ensure the current text of §13b BauGB is in the references corpus,
then retrieve via `search_corpus`. §13b is Wohnnutzung-specific —
projects outside that scope generally don't qualify.

---

## 6. Vorhabenbezogener Bebauungsplan (§12 BauGB)

A common pattern (e.g. for Solar-Parks) is a §12 vorhabenbezogener
B-Plan mit integriertem Vorhaben- und Erschließungsplan (V&E-Plan).
Procedural implications:

- Verfahren folgt grundsätzlich dem Regelverfahren (Phasen 0-12 oben).
- Vorhabenträger schließt Durchführungsvertrag mit der Gemeinde
  vor Satzungsbeschluss (per §12 Abs.1 Satz 1 BauGB).
- Im V&E-Bereich ist die Gemeinde nicht an §9-Festsetzungen
  gebunden — Vorhabenträger gestaltet das Vorhaben selbst.
- Wechsel des Vorhabenträgers bedarf Zustimmung der Gemeinde
  (per §12 Abs.5 BauGB).
- Wird der V&E-Plan nicht innerhalb der Frist durchgeführt, soll
  die Gemeinde den Plan aufheben — Aufhebung im vereinfachten
  Verfahren (§13 BauGB) zulässig.

**Verfahrensvermerk-Anpassung:** Festsetzungen-Einleitung lautet
"vorhabensbezogener Bebauungsplan Nr. X mit integriertem Vorhaben-
und Erschließungsplan", nicht der einfache "Bebauungsplan Nr. X"-
Wortlaut. Exact wording per state-leitfaden.

---

## 7. Mapping: Phase → orchestrator project state

The orchestrator's lifecycle states (from
`plugin/skills/orchestrator/PROCEDURE.md` Checkpoint 8.1) map roughly
to phases as follows:

| Project state | Phases active in this state |
|---|---|
| `draft` | 0–3 (work toward Vorentwurf, evaluation, Entwurf-prep) |
| `internal-review` | 4 (Billigungs-Prep), 5–7 (Beteiligung-aktiv), 8 (Kataster), 9 (Satzung-Prep) |
| `sent-to-authority` | 10 (Genehmigung höhere VB) |
| `awaiting-response` | 10 (waiting for Genehmigung-Antwort) |
| `revision-requested` | Auflagen / Nebenbestimmungen — back to 6/7 if substantial |
| `finalized` | 11–13 (Ausfertigung, Bekanntmachung, Inkrafttreten) |
| `archived` | post-Inkrafttreten, project administratively closed |

State transitions during Phases 5–7 (Beteiligungsrunden) are tricky
because the same `internal-review` state covers multiple discrete
events (frühzeitige Beteiligung, förmliche Beteiligung, mögliche
Wiederholung). The orchestrator should treat each Beteiligungs-
Auslegung as a distinct sub-event logged in `_ai/decisions.md`,
not as a state transition.

---

## 8. Mapping: Phase → folder structure

The new-project folder structure (`memory/universal/project-structure.md`)
provides `B-Plan/Aufstellungsverfahren/` and `TöB/` as the per-phase
holding spots. Recommended subfolder naming:

```
B-Plan/Aufstellungsverfahren/
├── 0-aufstellungsbeschluss/
├── 1-raumordnung/                     state-LandesPlG-§
├── 2a-frueh-oeffentlichkeit/          §3 Abs.1
├── 2b-frueh-toeb/                     §4 Abs.1
├── 3-auswertung-vorentwurf/
├── 4-billigungsbeschluss/
├── 5a-foerml-oeffentlichkeit/         §3 Abs.2
├── 5b-foerml-toeb/                    §4 Abs.2
├── 6-abwaegung/
├── 7-erneute-auslegung/               (only if needed)
├── 8-kataster/
├── 9-satzungsbeschluss/
├── 10-genehmigung/
├── 11-ausfertigung/
└── 12-bekanntmachung/
```

The numeric prefixes ensure stable sort order regardless of locale
and make the procedural sequence visible at a glance.

For the TöB-specific correspondence subfolder we previously
proposed `TöB/4_1-fruehzeitig/`, `TöB/4_2-foermlich/` — these
remain valid as a parallel pane focused only on the §4 axis (the
TöB-Listen, individual Anschreiben + eingehende Stellungnahmen pro
Behörde). They duplicate some content with `Aufstellungsverfahren/2b`
and `5b` but serve a different organizing principle (per-Behörde
vs per-Phase).

**Open question:** is one organization preferable, or should
both views coexist? Some offices organize by §-paragraph at the TöB-
axis level (e.g. `TöB-Verfahren/§ 4 (1)/`), which aligns with our
`TöB/4_1-...` proposal.

---

## 9. Verfahrensvermerk-Reihenfolge

The canonical Vermerk-Reihenfolge for a B-Plan in Regelverfahren is
a 13-entry sequence (variants exist for §13/§13a). When generating
a new Festsetzungen, this order is the default; project-specific
deviations are noted.

The Vermerk numbers above (#1 through #13) are stable identifiers
across this document. The verbatim wording for each Vermerk is
state-specific and per Verfahrenstyp — fetch via:

```
search_corpus(query="Verfahrensvermerk #<N> <verfahrenstyp>",
              filter={source_subtype: leitfaden,
                      jurisdiction: <bundesland>})
```

---

## 10. Hinweise zu §214 BauGB-Bekanntmachungstext

§214 f. BauGB regelt die Geltendmachung von Verfahrens- und
Formfehlern; konkret §215 die Frist (1 Jahr nach Bekanntmachung).
Konsequenz: Übliche Bekanntmachungstexte enthalten den expliziten
Hinweis auf §214 f. BauGB (verbatim Wortlaut staatsspezifisch im
state-leitfaden).

---

## 11. Open questions / TODOs

- **Q1:** Bei §13b-Projekt: aktuelle Fassung über
  `research-references` in das references-corpus laden, dann
  diesen Abschnitt hier ergänzen.
- **Q2:** Welcher Bekanntmachungs-Modus gilt für Gemeinden ohne
  amtliches Bekanntmachungsblatt? Per-project detail, oft via Amts-
  bzw. lokales Anzeigeblatt geregelt — Detail im jeweiligen
  state-leitfaden (LBauO / Kommunalverfassung des Landes).
- **Q3:** Gibt es state-spezifische Fristverkürzungen oder
  -verlängerungen jenseits des Bundesrahmens? §3/§4 BauGB-Fristen
  sind bundeseinheitlich, aber LBauO oder LPlG der jeweiligen Länder
  können zusätzliche Vorgaben enthalten — pro Bundesland im
  state-leitfaden klären.
- **Q4:** Wie integriert sich die Umweltprüfung (§2 Abs.4 BauGB)
  zeitlich in die Phasen? Muss vor Auslegung abgeschlossen sein;
  Umfang im Rahmen §4 Abs.1 von TöB festgelegt (Scoping). Detail-
  Doc als separates `memory/universal/verfahren/umweltpruefung.md`
  lohnt, wenn Projekt das erstmals ausführlich behandelt.

These belong on the product backlog. As specific projects raise them,
add findings here and update `references_used[]`.
