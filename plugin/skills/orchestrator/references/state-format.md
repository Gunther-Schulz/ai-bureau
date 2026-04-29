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

**Access via MCP tools, not direct Read/Write.** state.md is
schema-bearing per ARCHITECTURE.md meta-rule 4 refinement A: a
`ProjectState` Pydantic model owns the frontmatter contract,
forward-migrations apply on read, and cross-reference invariants
(lifecycle/phase consistency, date order, required-fields-present)
fail loud on parse. Skills MUST use:

- `get_project_state(project)` — read + validate; returns typed
  state + raw markdown body. Raises on contract violation.
- `update_project_state(project, updates, body_append?)` — apply
  partial frontmatter merge + validate before writing; never
  writes a partial-invalid state.

Direct skill `Read`/`Write`/`Edit` of state.md is a meta-rule 4
persistence-boundary leak. Audit slice 14 catches violations.

The schema below is the *frontmatter shape* the Pydantic model
enforces. Owning module: `pbs_mcp/project_state.py`. The
markdown body (History section, free-form notes) is preserved
unchanged across read/write cycles; not schema-validated.

```yaml
---
# Identity
project: <YY-NN>-<location-slug>
project_root: <projects_root>/<YY-NN> <Client> - <Location>
client: <Client>
client_contact: <Contact-Name> <contact@example.de>
location: <Location> (Gemeinde <Gemeinde>)
gemeinde: <Gemeinde>
landkreis: <Landkreis>
bundesland: MV    # required. ISO state code: BB|BW|BY|BE|HB|HH|HE|MV|NI|NW|RP|SH|SL|SN|ST|TH
                  # Picks which state-extension references-manifest applies
                  # for this project (federal-core always applies).

# Dates
created: YYYY-MM-DD
last_session: YYYY-MM-DD

# Lifecycle
lifecycle: internal-review                # draft | internal-review | sent-to-authority | awaiting-response | revision-requested | finalized | archived
ownership_mode: new-work-only              # full | migrate | new-work-only | quarantine
practices: [<practice-id-1>, <practice-id-2>]   # ids from office_config.actors (kind=internal)
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
  - {phase: 0-aufstellungsbeschluss, entered: YYYY-MM-DD}
  - {phase: 2a-frueh-oeffentlichkeit, entered: YYYY-MM-DD}
  - {phase: 5a-foerml-oeffentlichkeit, entered: YYYY-MM-DD}

# Deadlines
deadlines:
  - {kind: behoerdliche-frist, date: YYYY-MM-DD, description: "Stellungnahme-Frist UNB"}
  - {kind: client-deadline, date: YYYY-MM-DD, description: "Beschlussreife <Client>"}

linked_projects: []

# Plan content
geltungsbereich_ha: <ha>
geltungsbereich_solar_ha: <ha>
b_plan_nr: <N>
b_plan_name: "<BPlan-Name>"

notes: |
  Free-text notes on this specific project — historical context, prior
  cooperation experience, related projects to use as reference, etc.
---

# History

Append-only record of state transitions and major events.

- YYYY-MM-DD — Aufstellungsbeschluss durch Gemeindevertretung <Gemeinde>.
- YYYY-MM-DD — frühzeitige Beteiligung §3/§4 Abs.1 abgeschlossen.
- YYYY-MM-DD — Auslegungsbeschluss; Auslegung gestartet.
- YYYY-MM-DD — UNB Stellungnahme eingegangen, in Abwägung.
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
project: <YY-NN>-<location-slug>
last_survey: YYYY-MM-DD
last_modified_at_survey: YYYY-MM-DD
survey_method: orchestrator-binding        # binding-flow | manual-edit | research-references-update
---

# Current artifacts

- B-Plan/Begründung/<doctype-master>.tex     [working draft]
- B-Plan/Festsetzungen/<doctype-master>.tex  [working draft]

# Sent / archived versions

- alt/Begründung_v2_UNB-YYYY-MM.tex          [sent to UNB YYYY-MM-DD]

# Inputs (active)

- inputs/auftraggeber/briefing-YYYY-MM.pdf
- inputs/erhebungen/vermessung-YYYY-MM.pdf

# Inputs (superseded)

- inputs/auftraggeber/briefing-YYYY-MM.pdf

# Stellungnahmen (awaiting Abwägung)

- inputs/stellungnahmen/YYYY-MM/UNB-<authority-slug>.pdf

# Resources (read-only)

- /Bilder — site photos from Begehung YYYY-MM-DD
- /<other-practice-workspace> — sibling practice's working area
- /Externe Gutachten — third-party reports

# Cruft to ignore

- *.aux, *.fdb_latexmk, *.fls, *.log, *.toc, *.synctex.gz
- ~$* (Office lock files)
- .DS_Store, ._.*

# Notes

- Free-text notes on file-map quirks (folder-name typos, layout
  divergences from canonical, etc.) — this is the right place to
  document such things rather than silently fixing them.
```

---

## decisions.md

Append-only log. Decisions never edited in place — if reversed, a new
entry supersedes.

```markdown
# Decisions log — <YY-NN>-<location-slug>

---

## YYYY-MM-DD — Apply combined §45-Nr.5 + §1a Abs.2 argumentation

**Reasoning:** Authority previously rejected straight Innenbereichs-
satzungs-Argumentation. Pattern from baustein/§45-nr5-innenbereich-
privat with §1a-Erweiterung.
**Source:** orchestrator suggestion based on rejection feedback;
user approved.

---

## YYYY-MM-DD — Vorhabensbezogenen B-Plan with V&E-Plan

**Reasoning:** Client requires klare Bindung an konkretes Vorhaben.
§12 BauGB ermöglicht Durchführungsvertrag mit Frist X Jahre für die
Zwischennutzung.
**Source:** Abstimmung Client + Bürgermeister YYYY-MM-DD.

---

## YYYY-MM-DD — Geltungsbereich auf X,XX ha festgelegt

**Reasoning:** Erweiterung des ursprünglichen X ha auf X,XX ha zur
Aufnahme der Folgenutzungs-Grünlandflächen.
**Source:** Vermessung YYYY-MM; Bürgermeister-Zustimmung; vor
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
# Correspondence log — <YY-NN>-<location-slug>

| Date | Type | Party | Subject | Artifact path |
|---|---|---|---|---|
| YYYY-MM-DD | mail-out | UNB <Landkreis> (<Sachbearbeiter>) | Anschreiben §4 Abs.1 | Schriftverkehr/eml/YYYY-MM-DD-UNB-out.eml |
| YYYY-MM-DD | mail-in | UNB <Landkreis> (<Sachbearbeiter>) | Stellungnahme §4 Abs.1 | Schriftverkehr/eml/YYYY-MM-DD-UNB-in.eml |
| YYYY-MM-DD | meeting | <Client> + Bürgermeister <Gemeinde> | Abstimmung Verfahrenstyp | Schriftverkehr/besprechungsprotokolle/YYYY-MM-DD-client-buergermeister.md |
| YYYY-MM-DD | mail-in | UNB <Landkreis> | Stellungnahme zur Auslegung | inputs/stellungnahmen/YYYY-MM/UNB-<authority-slug>.pdf |
| YYYY-MM-DD | call | UNB <Landkreis> (<Sachbearbeiter>) | Klärung §45-Bedenken | Schriftverkehr/telefonnotizen/YYYY-MM-DD-UNB-<authority-slug>.md |
```

Type values: `mail-in`, `mail-out`, `call`, `meeting`,
`tel-conference`. For multi-party events, comma-separate parties or
point at meeting-minutes artifact.

Append-only; no entries removed.

---

## module-decisions.md

Per-doctype tables. Append-only.

```markdown
# Module assembly decisions — <YY-NN>-<location-slug>

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
date: YYYY-MM-DD
recipient: UNB Landkreis <Landkreis>
recipient_contact: <Sachbearbeiter>
recipient_address: <authority>@...
project: <YY-NN>-<location-slug>
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
