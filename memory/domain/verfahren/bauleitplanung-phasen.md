---
name: bauleitplanung-phasen
description: Phases of the Bauleitplanverfahren in PBS's M-V practice —
  how Vorentwurf, Entwurf, public participation rounds, TöB rounds,
  and Satzung interact. Sources are §§ 1-13a BauGB (federal), §17 LPlG
  M-V (state-specific), and PBS's own Verfahrensvermerke as seen in
  the Friedrichshof Festsetzungen template.
type: domain
---

# Bauleitplanung-Phasen (Bebauungsplan, M-V practice)

The Bebauungsplan-Verfahren is structurally federal (BauGB) but has
M-V-specific touches (§17 LPlG raumordnungsbehördliche Beteiligung,
publication via `bplan.geodaten-mv.de`). PBS does almost exclusively
M-V projects. This file documents the canonical Regelverfahren plus
the two simplified variants, and how each phase maps to project state,
folder structure, and Verfahrensvermerke.

**Authoritative sources used:**
- `~/dev/Planungsbüro-Schulz/22-16-Maxsolar---Friedrichshof---B-Plan---Begruendung/BauGB.txt`
  (PBS's local BauGB snapshot — as of late 2023; predates the 2024
  reintroduction of §13b).
- The Verfahrensvermerke section of the Friedrichshof Festsetzungen
  master file (`Textteil-B-B-Plan.tex`) — encodes office practice
  for Vorhabensbezogener B-Plan in M-V, Klein Belitz / Amt Bützow-Land.
- §17 LPlG M-V (raumordnungsbehördliche Beteiligung) — referenced
  but not stored locally.

---

## 1. The two-axis structure

Two parallel beteiligungs-axes run through every Verfahren:

| Axis | Frühzeitige Phase | Förmliche Phase |
|---|---|---|
| **Öffentlichkeit** | §3 Abs.1 BauGB | §3 Abs.2 BauGB |
| **Behörden / TöB** | §4 Abs.1 BauGB | §4 Abs.2 BauGB |

§4a Abs.2 explicitly permits running both axes simultaneously (the
frühzeitige rounds in parallel, the förmlichen rounds in parallel).
PBS practice does this — there is one "frühzeitige Beteiligung" event
covering both Öffentlichkeit and Behörden, and one "förmliche
Beteiligung" event likewise.

---

## 2. Regelverfahren — phase by phase

### Phase 0 — Aufstellungsbeschluss

The Gemeindevertretung formally decides to start the planning. Required
when starting a B-Plan; the Beschluss must be ortsüblich bekannt
gemacht (§2 Abs.1 BauGB).

- **Documents:** Aufstellungsbeschluss-Vorlage, amtliche Bekanntmachung.
- **Project state:** `draft` (orchestrator default for new projects).
- **Verfahrensvermerk #1:** "Aufgestellt aufgrund des
  Aufstellungsbeschlusses der Gemeindevertretung vom ... Der
  Aufstellungsbeschluss ist am ... durch Abdruck im amtlichen
  Bekanntmachungsblatt ... sowie im Internet ortsüblich
  bekanntgemacht worden."
- **Folder:** `B-Plan/Aufstellungsverfahren/0-aufstellungsbeschluss/`.

### Phase 1 — §17 LPlG-Beteiligung (M-V-specific)

The raumordnungs-zuständige Stelle is beteiligt nach §17
Landesplanungsgesetz M-V. Federal BauGB doesn't require this; M-V
practice does. Often happens early, before or alongside frühzeitige
Beteiligung.

- **Documents:** Anschreiben an die Raumordnungsbehörde mit
  Vorentwurf-Material.
- **Verfahrensvermerk #2:** "Die für die Raumordnung und Landesplanung
  zuständige Stelle ist gemäß §17 LPlG beteiligt worden."
- **Folder:** `B-Plan/Aufstellungsverfahren/1-raumordnung/`.

### Phase 2 — Frühzeitige Beteiligung (Vorentwurf)

Both §3 Abs.1 (Öffentlichkeit) and §4 Abs.1 (Behörden / TöB) typically
run together (per §4a Abs.2). The "Vorentwurf" is the planning
document used for this phase — usually less detailed than the
Entwurf, sufficient to convey Ziele, Lösungsalternativen, and
voraussichtliche Auswirkungen.

#### Phase 2a — §3 Abs.1 frühzeitige Öffentlichkeitsbeteiligung

- **Format:** "möglichst frühzeitig … öffentlich zu unterrichten;
  Gelegenheit zur Äußerung und Erörterung." Often an Einwohner-
  versammlung. Kinder und Jugendliche sind ausdrücklich umfasst.
- **Documents:** Vorentwurf (Plan + Begründung), Anschreiben /
  Einladung zur Öffentlichkeitsversammlung.
- **Verfahrensvermerk #3:** "Die frühzeitige Unterrichtung der
  Öffentlichkeit nach §3 Abs.1 BauGB ist in der Zeit vom ... bis zum
  ... durchgeführt worden."
- **Verfahrensvermerk #4 (M-V practice):** Often a separate vermerk
  for the Einwohnerinformations-Termin (date + Uhrzeit + Ort).
- **Folder:** `B-Plan/Aufstellungsverfahren/2a-frueh-oeffentlichkeit/`.

#### Phase 2b — §4 Abs.1 frühzeitige Behördenbeteiligung

- **Format:** Behörden und sonstige Träger öffentlicher Belange
  (whose Aufgabenbereich berührt sein könnte) sind zu unterrichten
  und zur Äußerung aufzufordern, auch zu Umfang und Detaillierungs-
  grad der Umweltprüfung (§2 Abs.4).
- **Documents:** Anschreiben mit Vorentwurf-Material an alle TöB,
  TöB-Liste.
- **Verfahrensvermerk #5:** "Die frühzeitige Unterrichtung der
  Behörden und sonstigen Träger öffentlicher Belange nach §4 Abs.1
  BauGB ist mit Schreiben vom ... erfolgt."
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
- **Folder:** Internal working notes, possibly under
  `B-Plan/Aufstellungsverfahren/3-auswertung-vorentwurf/`.

### Phase 4 — Billigungs- und Auslegungsbeschluss

The Gemeindevertretung billigt den Entwurf and bestimmt die
Auslegung. This is a prerequisite for §3 Abs.2 / §4 Abs.2.

- **Documents:** Entwurf (Plan + Begründung) als billigungsreife
  Fassung, Sitzungsvorlage, Beschluss-Protokoll.
- **Verfahrensvermerk #6:** "Die Gemeindevertretung hat am ... den
  Entwurf des Bebauungsplans mit Begründung gebilligt und zur
  Auslegung bestimmt."
- **Folder:** `B-Plan/Aufstellungsverfahren/4-billigungsbeschluss/`.

### Phase 5 — Förmliche Beteiligung (Entwurf)

Both §3 Abs.2 and §4 Abs.2 run, typically simultaneously per §4a Abs.2.

#### Phase 5a — §3 Abs.2 öffentliche Auslegung

- **Format:** Veröffentlichung im Internet für mindestens 30 Tage
  (§3 Abs.2 Satz 1) PLUS mindestens eine andere leicht erreichbare
  Zugangsmöglichkeit (öffentliche Auslegung, Lesegerät, etc.).
  Veröffentlichungsfrist UND Hinweise auf Stellungnahme-Möglichkeit
  müssen vorab ortsüblich bekanntgemacht werden.
- **M-V-specific:** Veröffentlichung über das zentrale Landesportal
  `bplan.geodaten-mv.de` ist als ergänzende Zugangsmöglichkeit
  etabliert. Im Friedrichshof-Beispiel wird BEIDES genutzt: lokale
  Auslegung im Amt + Veröffentlichung auf Gemeindehomepage + Eintrag
  in `bplan.geodaten-mv.de`.
- **Bekanntmachungsmittel (M-V Praxis):** amtliches Bekanntmachungs-
  blatt des Amts + Homepage des Amts + Landesportal.
- **Documents:** Auslegungs-Bekanntmachung, Auslegungs-Exemplar des
  Entwurfs, ggf. wesentliche umweltbezogene Stellungnahmen die
  bereits vorliegen.
- **Verfahrensvermerk #7:** "Der Entwurf des Bebauungsplans hat mit
  der Begründung und den wesentlichen umweltbezogenen Stellungnahmen
  in der Zeit vom ... bis zum ... während der Dienst- und
  Öffnungszeiten nach §3 Abs.2 BauGB im ... sowie in der Zeit vom ...
  bis zum ... durch Einstellung in das Internet auf der Homepage der
  Gemeinde ... unter ... und zusätzlich im Bau- und Planungsportal
  M-V unter https://bplan.geodaten-mv.de/bauportal/ gemäß §3 BauGB
  öffentlich ausgelegen. Die öffentliche Auslegung ist mit Angaben
  dazu, welche Arten umweltbezogener Informationen verfügbar sind,
  und mit dem Hinweis, dass Stellungnahmen während der Auslegungs-
  frist abgegeben werden können und dass nicht fristgerecht
  abgegebene Stellungnahmen unberücksichtigt bleiben können, am ...
  durch Abdruck im amtlichen Bekanntmachungsblatt ... ortsüblich
  bekanntgemacht worden."
- **Folder:** `B-Plan/Aufstellungsverfahren/5a-foerml-oeffentlichkeit/`.

#### Phase 5b — §4 Abs.2 förmliche Behördenbeteiligung

- **Format:** Stellungnahmen sind innerhalb eines Monats abzugeben,
  mindestens 30 Tage. Bereitstellung soll elektronisch erfolgen
  (§4 Abs.2 Satz 2).
- **Documents:** Anschreiben + Entwurfs-Exemplar an alle TöB,
  aktualisierte TöB-Liste, eingehende Stellungnahmen.
- **Verfahrensvermerk #8:** "Die Behörden und sonstigen Träger
  öffentlicher Belange, deren Aufgabenbereich durch die Planung
  berührt werden kann, sind nach §4 Abs.2 BauGB mit Schreiben vom
  ... zur Abgabe einer Stellungnahme aufgefordert worden."
- **Folder:** `B-Plan/Aufstellungsverfahren/5b-foerml-toeb/`.

### Phase 6 — Abwägung

The Gemeinde prüft die fristgemäß abgegebenen Stellungnahmen aus
beiden Beteiligungsrunden und gewichtet sie ab. Ergebnis ist
mitzuteilen (§3 Abs.2 Satz 6, §4a Abs.5).

- **Documents:** Abwägungstabelle (Stellungnahme → Antwort →
  Abwägungsergebnis pro Eintrag). Dies ist das eigene Doctype
  (`abwaegung` in `doctypes.yaml`).
- **Verfahrensvermerk #9:** "Die Gemeindevertretung hat die
  fristgemäß abgegebenen Stellungnahmen der Öffentlichkeit sowie der
  Behörden und sonstigen Träger öffentlicher Belange am ... geprüft.
  Das Ergebnis ist mitgeteilt worden."
- **Project state:** `internal-review` → `revision-requested` (if
  major Stellungnahmen forcen änderungen) → back through earlier
  phases per §4a Abs.3 if Grundzüge berührt werden, or directly
  forward.
- **Folder:** `B-Plan/Aufstellungsverfahren/6-abwaegung/`.

### Phase 7 — Erneute Auslegung (falls erforderlich)

If the Entwurf nach §4a Abs.3 changed (Grundzüge berührt), erneute
Auslegung nach §3 Abs.2 ist erforderlich (kann aber verkürzt werden,
und kann auf die berührte Öffentlichkeit + TöB beschränkt werden,
wenn Grundzüge nicht berührt).

- Loops back to Phase 5 with verkürzten Fristen.
- Each loop adds Verfahrensvermerke. Office practice numbers them
  (z. B. "2. Auslegung", "3. Auslegung").

### Phase 8 — Katastermäßige Bestätigung

Vor Satzungsbeschluss bestätigt der öffentlich bestellte Vermesser
den katastermäßigen Bestand im Geltungsbereich. M-V practice has a
formelhafter vermerk dazu (mit Vorbehalt zur lagerichtigen
Darstellung in 1:2.000 Maßstab).

- **Verfahrensvermerk #10:** "Der katastermäßige Bestand innerhalb
  des Geltungsbereiches am ... wird als richtig dargestellt
  bescheinigt. Hinsichtlich der lagerichtigen Darstellung der
  Grenzpunkte gilt der Vorbehalt, dass eine Prüfung nur grob
  erfolgte, da die rechtsverbindliche Flurkarte im Maßstab 1:2.000
  vorliegt."

### Phase 9 — Satzungsbeschluss

Die Gemeinde beschließt den Bebauungsplan als Satzung (§10 Abs.1
BauGB). Ohne weitere Genehmigung ist der Plan damit beschlussreif —
es sei denn, ein Genehmigungserfordernis besteht (siehe Phase 10).

- **Documents:** Satzungsbeschluss-Vorlage, Beschluss-Protokoll.
- **Project state:** `internal-review` → ready for `sent-to-authority`
  (if Genehmigung erforderlich) or directly to `finalized`-near.

### Phase 10 — Höhere Verwaltungsbehörde (falls Genehmigung erforderlich)

Genehmigung der höheren Verwaltungsbehörde ist erforderlich nur in
den Fällen §10 Abs.2 BauGB (Bebauungspläne nach §8 Abs.2 Satz 2,
Abs.3 Satz 2, Abs.4) — also vor allem für Bebauungspläne, die nicht
aus dem Flächennutzungsplan entwickelt sind, und für vorzeitige
Bebauungspläne. PBS-Praxis: Solar-Park-Pläne sind regelmäßig
genehmigungspflichtig wegen Abweichung vom F-Plan.

- **Documents:** Genehmigungsantrag, ggf. Auflagen / Nebenbestimm-
  ungen.
- **Verfahrensvermerk #11:** "Die Genehmigung der Satzung, bestehend
  aus der Planzeichnung (Teil A) und dem Text (Teil B), wurde mit
  Verfügung der höheren Verwaltungsbehörde vom ... , AZ: ... mit
  Auflagen, Nebenbestimmungen und Hinweisen erteilt."
- **Project state:** `sent-to-authority` → `awaiting-response` →
  `revision-requested` (if Auflagen) → loop or proceed.

### Phase 11 — Ausfertigung

Der Bürgermeister fertigt den Bebauungsplan aus.

- **Verfahrensvermerk #12:** "Der Bebauungsplan, bestehend aus der
  Planzeichnung (Teil A) und dem Text (Teil B), wird hiermit
  ausgefertigt."

### Phase 12 — Bekanntmachung des Inkrafttretens

Erteilung der Genehmigung (oder Beschluss, falls keine Genehmigung
erforderlich) ist ortsüblich bekannt zu machen. Mit der
Bekanntmachung tritt der Bebauungsplan in Kraft (§10 Abs.3 BauGB).

- **Documents:** Bekanntmachungstext mit den Hinweisen auf §214f
  (Geltendmachung von Verfahrens-/Formfehlern), §44 BauGB (Erlöschen
  Entschädigungsansprüche), §5 Abs.5 KV M-V.
- **Verfahrensvermerk #13:** "Die Satzung des Bebauungsplans sowie
  die Stelle, bei der der Plan auf Dauer während der Dienststunden
  von jedermann eingesehen werden kann und über dessen Inhalt
  Auskunft zu erhalten ist, sind am ... ortsüblich bekannt gemacht
  worden. In der Bekanntmachung wurde auf die Geltendmachung und
  Verletzung von Verfahrens- und Formvorschriften und von Mängeln
  der Abwägung sowie auf die Rechtsfolgen (§214 f. BauGB), die
  Fälligkeit und das Erlöschen von Entschädigungsansprüchen (§44
  BauGB) und auf die Bestimmungen des §5 Abs.5 KV M-V hingewiesen.
  Die Satzung ist am ... in Kraft getreten."
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
- Plan enthält nur Festsetzungen nach §9 Abs.2a oder Abs.2b.

UND:
- Keine UVP-Pflicht der zugelassenen Vorhaben.
- Keine Anhaltspunkte auf Beeinträchtigung Schutzgüter §1 Abs.6
  Nr.7b.
- Keine schweren-Unfälle-Pflichten §50 BImSchG.

**Was kann entfallen:**
- Frühzeitige Unterrichtung §3 Abs.1 / §4 Abs.1 (kann entfallen, §13
  Abs.2 Nr.1).
- Stattdessen: Öffentlichkeit / TöB Gelegenheit zur Stellungnahme in
  angemessener Frist (§13 Abs.2 Nr.2/3) — alternativ kann auch direkt
  §3 Abs.2 / §4 Abs.2 durchgeführt werden.
- Umweltprüfung (§2 Abs.4) entfällt, Umweltbericht (§2a) entfällt,
  Hinweise auf umweltbezogene Informationen (§3 Abs.2 Satz 4) entfällt,
  zusammenfassende Erklärung (§6a / §10a) entfällt, Überwachung (§4c)
  entfällt.

**Use case bei PBS:** Selten direkt anwendbar bei neu aufgestellten
Solar-Park-B-Plänen (UVP-Vorprüfung kann erforderlich sein, abhängig
von Anlagengröße). Gelegentlich relevant bei Änderungen bestehender
B-Pläne.

---

## 4. Beschleunigtes Verfahren (§13a BauGB) — Innenentwicklung

Bebauungsplan für Wiedernutzbarmachung, Nachverdichtung, oder andere
Maßnahmen der Innenentwicklung (Innenentwicklung im engeren Sinn).

**Voraussetzungen:**
- Zulässige Grundfläche (§19 Abs.2 BauNVO):
  - <20.000 m² → ohne Vorprüfung anwendbar.
  - 20.000 – 70.000 m² → Vorprüfung des Einzelfalls erforderlich
    (Anlage 2 BauGB), ergibt voraussichtlich keine erheblichen
    Umweltauswirkungen.
- Keine UVP-Pflicht der ermöglichten Vorhaben.
- Keine Anhaltspunkte für FFH/Vogelschutz-Beeinträchtigung.
- Keine schweren-Unfälle-Pflichten.

**Verfahrenserleichterungen (gleich wie §13 Abs.2/3):**
- Frühzeitige Beteiligung kann entfallen.
- Umweltprüfung / Umweltbericht / Zusammenfassende Erklärung können
  entfallen.
- Eingriffe gelten als bereits vor planerischer Entscheidung
  zulässig (§13a Abs.2 Nr.4) — keine Eingriffs-Ausgleichs-Bilanzierung
  erforderlich für <20.000 m² Variante.
- Plan kann von F-Plan abweichen, FNP wird per Berichtigung angepasst.

**Use case bei PBS:** Anwendbar wenn Plan sich auf bereits versiegelte
oder im Innenbereich gelegene Flächen bezieht. Z. B. die Holthusen-
Vorbeck-Diskussion aus dem Hendrik-Transcript ("Innenbereichssatzung
mit klarem planerischen Willen zur Wohnbebauung").

---

## 5. §13b BauGB

§13b (Wohnnutzung am Ortsrand, beschleunigtes Verfahren ergänzend)
existed in earlier BauGB versions, was struck down by the BVerwG
2022, and reintroduced in modified form in 2024. The local BauGB.txt
snapshot in this repo PREDATES the 2024 reintroduction and does not
contain §13b.

**Action item:** if a project ever needs §13b, fetch the current
text from `gesetze-im-internet.de/baugb/__13b.html` first and update
this document. PBS's Solar-PV portfolio rarely qualifies (§13b
Wohnnutzung-spezifisch), so this is low priority.

---

## 6. Vorhabenbezogener Bebauungsplan (§12 BauGB)

PBS practice for Solar-Parks uses §12 vorhabenbezogenen B-Plan with
integriertem Vorhaben- und Erschließungsplan (V&E-Plan). Procedural
implications:

- Verfahren folgt grundsätzlich dem Regelverfahren (Phasen 0-12
  oben).
- Vorhabenträger schließt Durchführungsvertrag mit der Gemeinde
  vor Satzungsbeschluss (§12 Abs.1 Satz 1).
- Im V&E-Bereich ist die Gemeinde nicht an §9-Festsetzungen
  gebunden — Vorhabenträger gestaltet das Vorhaben selbst.
- Wechsel des Vorhabenträgers bedarf Zustimmung der Gemeinde
  (§12 Abs.5).
- Wird der V&E-Plan nicht innerhalb der Frist durchgeführt, soll
  die Gemeinde den Plan aufheben — Aufhebung im vereinfachten
  Verfahren (§13) zulässig.

**Verfahrensvermerk-Anpassung:** Festsetzungen-Einleitung lautet
"vorhabensbezogener Bebauungsplan Nr. X mit integriertem Vorhaben-
und Erschließungsplan", nicht der einfache "Bebauungsplan Nr. X"-
Wortlaut.

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

The new-project folder structure (`memory/domain/project-structure.md`)
provides `B-Plan/Aufstellungsverfahren/` and `TöB/` as the per-phase
holding spots. Recommended subfolder naming:

```
B-Plan/Aufstellungsverfahren/
├── 0-aufstellungsbeschluss/
├── 1-raumordnung/                     §17 LPlG
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

**Open question for v0.2:** is one organization preferable, or should
both views coexist? PBS practice from Vorbeck shows `B-Plan/TöB-
Verfahren/§ 4 (1)/` — they organize by §-paragraph at the TöB-axis
level. Aligns with our `TöB/4_1-...` proposal.

---

## 9. Verfahrensvermerk-Reihenfolge (Friedrichshof reference)

The Friedrichshof Festsetzungen template encodes the canonical
Vermerk-Reihenfolge (13 entries observed). When generating a new
Festsetzungen, this order is the default; project-specific deviations
are logged in `_ai/decisions.md`.

1. Aufstellungsbeschluss + Bekanntmachung
2. Beteiligung Raumordnung §17 LPlG
3. Frühzeitige Öffentlichkeitsbeteiligung §3 Abs.1
4. Frühzeitige Einwohnerinformation (separate vermerk)
5. Frühzeitige Behördenbeteiligung §4 Abs.1
6. Billigungs- und Auslegungsbeschluss
7. Auslegung §3 Abs.2 (mit M-V Bauportal)
8. Behördenbeteiligung §4 Abs.2
9. Ergebnis der Stellungnahmen + Mitteilung
10. Katastermäßige Bestätigung Vermesser
11. Genehmigung höhere Verwaltungsbehörde
12. Ausfertigung
13. Bekanntmachung Inkrafttreten + §214 f. BauGB Hinweis

Each Vermerk has a tabbing-Block for Ort, Datum, Siegel, Unterschrift
des Bürgermeisters. Re-used pattern in
`Textbausteine/Verfahrensvermerke.tex` (when extracted as a
modular Textbaustein).

---

## 10. Heilung und Rügeprivileg (§§ 214, 215 BauGB)

Verfahrens- oder Formfehler bei Beteiligung können nur unter engen
Voraussetzungen geltend gemacht werden (§214 BauGB) und müssen
innerhalb eines Jahres nach Bekanntmachung gerügt werden (§215 BauGB).
Diese Hinweise gehören in die Bekanntmachung des Inkrafttretens
(siehe Verfahrensvermerk #13).

Wird ein Mangel innerhalb der Rügefrist nicht geltend gemacht, gilt
er als geheilt für die Bestandskraft der Satzung. Praktische
Konsequenz: PBS-Bekanntmachungstexte enthalten den expliziten
Hinweis auf §214 f. BauGB.

---

## 11. Open questions / TODOs

- **Q1:** §13b BauGB-Text fehlt im lokalen BauGB.txt-Snapshot. Bei
  erstem §13b-Projekt: WebFetch von `gesetze-im-internet.de/baugb/__13b.html`,
  diesen Abschnitt hier ergänzen.
- **Q2:** Welcher Bekanntmachungs-Modus gilt für Gemeinden ohne
  amtliches Bekanntmachungsblatt (eher kleinere M-V-Gemeinden)? Per-
  project-Detail; Friedrichshof nutzt "Bützower Landkurier" als
  amtliches Blatt des Amts Bützow-Land.
- **Q3:** Gibt es M-V-spezifische Fristverkürzungen oder -verlängerungen
  jenseits des Bundesrahmens? §3/§4 BauGB-Fristen sind bundeseinheit-
  lich, aber LBauO M-V oder LPlG könnten zusätzliche Vorgaben
  enthalten.
- **Q4:** Wie integriert sich die Umweltprüfung (§2 Abs.4) zeitlich
  in die Phasen? Muss vor Auslegung abgeschlossen sein; Umfang im
  Rahmen §4 Abs.1 von TöB festgelegt (Scoping). Detail-Doc als
  separates `memory/domain/verfahren/umweltpruefung.md` lohnt, wenn
  PBS-Projekt das erstmals ausführlich behandelt.

These belong on the product backlog. As specific projects raise them,
update this document in place.
