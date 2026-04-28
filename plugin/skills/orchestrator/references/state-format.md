# Per-project AI-state format

Each bound project has a `_ai/` (visible, hybrid-ownership existing
project) or `.ai/` (hidden, fully AI-owned new project) directory at
its root. New projects use `.ai/`; existing projects use `_ai/`.

## Directory layout

```
<project-root>/{_ai,.ai}/
├── state.md                  # lifecycle, scope, ownership, deadlines
├── file-map.md               # interpretation of files outside _ai/
├── decisions.md              # major decisions log (append-only)
├── correspondence-log.md     # mail/call/meeting index
├── module-decisions.md       # template module include/exclude rationale
├── bausteine/                # project-scope bausteine (optional)
│   └── <name>.md
└── snapshots/
    └── <YYYY-MM-DD>-<recipient-tag>/
        ├── manifest.yaml
        ├── final.pdf
        ├── source/...
        └── cover-mail.txt
```

---

## state.md

Single source of project lifecycle truth.

```yaml
---
# Identity
project: 23-12-Vorbeck
project_root: /mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte/23-12 Maxsolar - Vorbeck (Schwaan)
client: Maxsolar
client_contact: Gabriel Constantin <gabriel.constantin@maxsolar.de>
location: Vorbeck (Gemeinde Schwaan)
gemeinde: Schwaan
landkreis: Rostock
bundesland: Mecklenburg-Vorpommern

# Dates
created: 2023-12-01
last_session: 2026-04-22

# Lifecycle
lifecycle: internal-review                # draft | internal-review | sent-to-authority | awaiting-response | revision-requested | finalized | archived
ownership_mode: new-work-only              # full | migrate | new-work-only | quarantine
practices: [schulz, hendrik]              # schulz | hendrik | joint
verfahren_type: vorhabensbezogen           # regelverfahren | vereinfachtes (§13) | beschleunigtes (§13a) | vorhabensbezogen (§12)

# Scope — which doctypes are in/out for this project
doctype_status:
  b-plan-begruendung: active
  b-plan-festsetzungen: active
  umweltbericht: applicable
  spa-vorpruefung: tbd
  spa-hauptpruefung: not-applicable
  ffh-vorpruefung: not-applicable
  lbp: not-applicable
  brandschutzkonzept: applicable
  bodenschutzkonzept: applicable

# Bauleitplanung phase tracking
phase: 5a-foerml-oeffentlichkeit
phase_history:
  - {phase: 0-aufstellungsbeschluss, entered: 2023-12-01}
  - {phase: 2a-frueh-oeffentlichkeit, entered: 2024-03-15}
  - {phase: 5a-foerml-oeffentlichkeit, entered: 2026-04-01}

# Deadlines
deadlines:
  - {kind: behoerdliche-frist, date: 2026-05-15, description: "Stellungnahme-Frist UNB"}
  - {kind: client-deadline, date: 2026-06-30, description: "Beschlussreife Maxsolar"}

linked_projects: []

# Plan content
geltungsbereich_ha: 43.57
geltungsbereich_solar_ha: 30.37
b_plan_nr: 3
b_plan_name: "Solarpark Friedrichshof"

notes: |
  UNB Rostock historisch kooperativ. Nachbarprojekte Friedrichshof
  und Waren-Grabowhöfe abgeschlossen — können als Referenz dienen.
---

# History

Append-only record of state transitions and major events.

- 2023-12-01 — Aufstellungsbeschluss durch Gemeindevertretung Schwaan.
- 2024-03-15 — frühzeitige Beteiligung §3/§4 Abs.1 abgeschlossen.
- 2026-04-01 — Auslegungsbeschluss; Auslegung gestartet.
- 2026-04-22 — UNB Stellungnahme eingegangen, in Abwägung.
```

### `doctype_status` values

| Value | Meaning |
|---|---|
| `tbd` | Possibly needed; decision pending (e.g. waiting for Begehung results) |
| `applicable` | Known to be in scope; not yet started |
| `active` | Currently being worked on |
| `finalized` | Completed for this project |
| `not-applicable` | Explicitly out of scope |

Drives which checklists load, which doctype bausteine surface, which
folders are scaffolded, which validations run.

Scope changes mid-project: the orchestrator updates a doctype's status
(e.g. `not-applicable` → `tbd` → `active`) when a new requirement
emerges, logs the change to `decisions.md` with reasoning, and
scaffolds new folders if needed.

### Lifecycle vs phase

- `lifecycle` is the project's overall state (workflow gate state).
- `phase` is the current Bauleitplanungs-phase (procedural step).
- Both advance together but are distinct: a project can be in
  `internal-review` while in phase `5a-foerml-oeffentlichkeit` AND
  again later in phase `7-erneute-auslegung`.

State transitions explicit; never silent. Each transition appends to
`phase_history` and the History body section.

---

## file-map.md

Used when project layout diverges from canonical project-structure
(most existing projects do). Loose structure; orchestrator scans but
doesn't strictly parse.

```yaml
---
project: 23-12-Vorbeck
last_survey: 2026-04-28
last_modified_at_survey: 2026-04-22
survey_method: orchestrator-binding        # binding-flow | manual-edit | research-references-update
---

# Current artifacts

- B-Plan/Textteil B/B-Plan Begründung.tex      [working draft]
- B-Plan/Testteil C/Textteil-B-B-Plan.tex      [working draft — note typo "Testteil C" in folder name]

# Sent / archived versions

- alt/Begründung_v2_UNB-2024-03.tex            [sent to UNB 2024-03-15]

# Inputs (active)

- inputs/auftraggeber/briefing-2024-02.pdf
- inputs/erhebungen/vermessung-2024-03.pdf

# Inputs (superseded)

- inputs/auftraggeber/briefing-2024-01.pdf

# Stellungnahmen (awaiting Abwägung)

- inputs/stellungnahmen/2026-04/UNB-rostock.pdf

# Resources (read-only)

- /Bilder — site photos from Begehung 2024-02-15
- /GIS — Hendrik's QGIS workspace
- /Externe Gutachten — third-party reports

# Cruft to ignore

- *.aux, *.fdb_latexmk, *.fls, *.log, *.toc, *.synctex.gz
- ~$* (Office lock files)
- .DS_Store, ._.*

# Notes

- Folder name typo: "Testteil C" should be "Textteil C". Not fixed
  to avoid breaking existing references.
```

---

## decisions.md

Append-only log. Decisions never edited in place — if reversed, a new
entry supersedes.

```markdown
# Decisions log — 23-12-Vorbeck

---

## 2026-04-22 — Apply combined §45-Nr.5 + §1a Abs.2 argumentation

**Reasoning:** UNB Rostock previously rejected reine Innenbereichs-
satzungs-Argumentation. Pattern from baustein/§45-nr5-innenbereich-
privat with §1a-Erweiterung.
**Source:** orchestrator suggestion based on rejection feedback;
user approved.

---

## 2024-04-01 — Vorhabensbezogenen B-Plan with V&E-Plan

**Reasoning:** Maxsolar verlangt klare Bindung an konkretes Vorhaben.
§12 BauGB ermöglicht Durchführungsvertrag mit Frist 30 Jahre für die
Zwischennutzung.
**Source:** Abstimmung Maxsolar-Konstantin + Bürgermeister Schwaan
2024-03-22.

---

## 2024-03-15 — Geltungsbereich auf 43,57 ha festgelegt (30,37 ha SO EBS)

**Reasoning:** Erweiterung des ursprünglichen 30 ha auf 43,57 ha zur
Aufnahme der Folgenutzungs-Grünlandflächen.
**Source:** Vermessung 2024-03; Bürgermeister-Zustimmung; vor
Auslegungsbeschluss.
```

Each entry: ISO date in heading, title (short), Reasoning (1-3
sentences), Source (who decided, what triggered).

Special entries on doctype scope change:

```markdown
## 2026-05-12 — Add SPA-Vorprüfung to scope

**Reasoning:** UNB Stellungnahme vom 2026-04-28 fordert separate
artenschutzrechtliche Prüfung wegen Funden bei Erhebung 2026-04.
state.md updated: spa-vorpruefung from `tbd` → `active`. Ordner
`B-Plan/SPA/` scaffolded.
**Source:** UNB Stellungnahme; user authorized scope change.
```

---

## correspondence-log.md

Append-only chronological table. Auto-maintained when new
correspondence arrives.

```markdown
# Correspondence log — 23-12-Vorbeck

| Date | Type | Party | Subject | Artifact path |
|---|---|---|---|---|
| 2024-03-15 | mail-out | UNB Rostock (Ratschker) | Anschreiben §4 Abs.1 | Schriftverkehr/eml/2024-03-15-UNB-out.eml |
| 2024-04-12 | mail-in | UNB Rostock (Ratschker) | Stellungnahme §4 Abs.1 | Schriftverkehr/eml/2024-04-12-UNB-in.eml |
| 2024-03-22 | meeting | Maxsolar + Bürgermeister Schwaan | Abstimmung Verfahrenstyp | Schriftverkehr/besprechungsprotokolle/2024-03-22-maxsolar-buergermeister.md |
| 2026-04-22 | mail-in | UNB Rostock | Stellungnahme zur Auslegung | inputs/stellungnahmen/2026-04/UNB-rostock.pdf |
| 2026-04-25 | call | UNB Rostock (Ratschker) | Klärung §45-Bedenken | Schriftverkehr/telefonnotizen/2026-04-25-UNB-ratschker.md |
```

Type values: `mail-in`, `mail-out`, `call`, `meeting`,
`tel-conference`. For multi-party events, comma-separate parties or
point at meeting-minutes artifact.

Append-only; no entries removed.

---

## module-decisions.md

Per-doctype tables. Append-only.

```markdown
# Module assembly decisions — 23-12-Vorbeck

## B-Plan/Begründung

| Date | Module | Decision | Reasoning |
|---|---|---|---|
| 2024-03-15 | Bodenschutz.tex | included | bodenschutzfachliche Belange relevant; BBB gefordert |
| 2024-03-15 | Denkmalschutz.tex | excluded | keine Denkmäler im Geltungsbereich (Stellungnahme ULD M-V vom 2024-02-10) |
| 2024-03-15 | Belange der Forst.tex | excluded | keine Waldflächen tangiert |

## B-Plan/Festsetzungen

| Date | Module | Decision | Reasoning |
|---|---|---|---|
| 2024-04-01 | Artenschutzrechtliche Festsetzungen.tex | included | §45-Ausnahme erforderlich, CEF-Maßnahme festzusetzen |

## Umweltbericht (Schutzgüter)

| Date | Module pair | Decision | Reasoning |
|---|---|---|---|
| 2024-04-01 | Schutzgut_TierePflanzen_(Mas_)UB.tex | included | Funde from Erhebung 2024-02-15 |
| 2024-04-01 | Schutzgut_KulturSachgut_(Mas_)UB.tex | excluded | keine Kulturgüter / Bodendenkmäler bekannt |
```

Append-only. When a decision is reversed (e.g. Denkmalschutz becomes
relevant after Erdarbeiten-Funde), a new row is added with reasoning;
old row stays.

---

## snapshots/<YYYY-MM-DD>-<recipient-tag>/

Immutable artifact bundles created by the send gate. Audit trail.

```
snapshots/<YYYY-MM-DD>-<recipient-slug>/
├── manifest.yaml
├── final.pdf
├── source/
│   ├── B-Plan Begründung.tex
│   ├── preamble.tex
│   ├── Projektdaten.tex
│   └── Textbausteine/*.tex
└── cover-mail.txt          # actual mail sent (if applicable)
```

`manifest.yaml`:

```yaml
---
date: 2026-04-28
recipient: UNB Landkreis Rostock
recipient_contact: Hr. Ratschker
recipient_address: rostock@...
project: 23-12-Vorbeck
phase: 5a-foerml-oeffentlichkeit
artifacts:
  - final.pdf
  - source/B-Plan Begründung.tex
  - cover-mail.txt
sent_by: g
sent_via: email                              # email | post | upload-portal
project_state_at_send: internal-review
project_lifecycle_after_send: sent-to-authority
checksum_sha256:
  final.pdf: "abc..."
notes: |
  Snapshot created automatically by send gate. Cover mail drafted
  by AI, edited by user before send.
---
```

Snapshots NEVER edited after creation. Re-sends create new snapshot
folders. Old ones stay as audit trail. `final.pdf` is the exact PDF
sent. `source/` is the LaTeX source tree that compiled to it (file
copies, not symlinks). Used for revision-request response: diff old
snapshot source against current to see what changed.

---

## Inter-file consistency

- `state.md.lifecycle` advancing past `sent-to-authority` requires at
  least one `snapshots/<...>/` folder.
- `state.md.phase` advancing must be reflected by a corresponding
  `decisions.md` entry.
- `correspondence-log.md` mail-out entries with attachment-mention
  should reference a `snapshots/<...>/` folder.
- `module-decisions.md` decisions must align with
  `state.md.doctype_status` — modules for `not-applicable` doctypes
  are not listed.
