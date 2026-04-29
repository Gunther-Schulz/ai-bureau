---
references_used:
  - {law: BauGB, paragraph: §3 Abs.1}
  - {law: BauGB, paragraph: §3 Abs.2}
  - {law: BauGB, paragraph: §4 Abs.1}
  - {law: BauGB, paragraph: §4 Abs.2}
---

# New-project folder structure

Every new project is created with this layout under
`office_config.roots.projects`. The folder name follows
`office_config.conventions.project_naming` (default
`{year_2}-{nr} {client} - {location}`). The AI owns the entire project
root (full ownership, not quarantined).

```
<project-folder>/
│
├── .ai/                            ← hidden, AI meta-state (fresh AI-owned)
│   ├── state.md                    │   _ai/ for adopted existing projects
│   ├── decisions.md
│   ├── module-decisions.md
│   ├── file-map.md
│   ├── correspondence-log.md
│   └── snapshots/
│       └── YYYY-MM-DD-recipient/
│
├── inputs/                         ← all source materials, by source
│   ├── auftraggeber/                briefings, contracts, plans-as-given
│   ├── behoerden/                   regulatory inputs, requirements
│   ├── erhebungen/                  surveys, vermessungen, drone scans
│   ├── gis-data/                    raw GIS data inputs
│   └── stellungnahmen/              for Abwägung phase, by date
│
├── B-Plan/                         ← primary doctype (B-Plan projects)
│   ├── Begründung/                  multi-page narrative LaTeX project
│   │   ├── B-Plan Begründung.tex   (master, copy of app skeleton)
│   │   ├── Projektdaten.tex
│   │   ├── Textbausteine/
│   │   ├── Bilder/
│   │   └── (build artifacts gitignored)
│   ├── Festsetzungen/               Teil B Text der Satzung LaTeX project
│   │   ├── Textteil-B-B-Plan.tex
│   │   ├── Projektdaten.tex
│   │   └── ...
│   ├── Aufstellungsverfahren/       process documents per phase
│   ├── Verfahrensvermerke/          signed Verfahrensvermerke (scanned)
│   └── Plan/                        Planzeichnung exports (Teil A)
│
├── F-Plan/                         ← if applicable, mirrors B-Plan structure
│
├── Umweltbericht/                  ← if applicable
│   ├── Bericht.tex
│   ├── Projekt.tex
│   ├── Kapitel/                     per-Schutzgut sections (paired _UB / _Mas_UB)
│   └── Bilder/
│
├── Externe Gutachten/              ← third-party reports (read-only resources)
│
├── Kartierung/                     ← field survey outputs
│
├── Karten/                         ← map deliverables (PDF/PNG exports)
│
├── Fotos/                          ← site photos, organized by Begehung date
│
├── Schriftverkehr/                 ← all correspondence
│   ├── eml/                         mail-client export drop zone
│   ├── telefonnotizen/              call notes (one .md per call)
│   ├── besprechungsprotokolle/      meeting minutes
│   └── ausgehend/                   outgoing letters/mails (drafted by AI)
│
├── TöB/                            ← Träger öffentlicher Belange
│   ├── 4_1-fruehzeitig/              §4 Abs.1 BauGB round
│   ├── 4_2-foermlich/                §4 Abs.2 BauGB round
│   └── (subsequent rounds as needed)
│
├── Vorlagen/                       ← project-specific template overrides
│
├── Zeichnungen/                    ← technical drawings (engineering, not Karten)
│
└── Auslieferung/                   ← finalized deliverables, ready to ship
    └── YYYY-MM-DD-recipient/
```

The literal folder names for the role-keyed subfolders (inputs,
sent_versions/Auslieferung, correspondence/Schriftverkehr, toeb/TöB)
are configurable per office in
`office_config.conventions.project_folder_layout`. Doctype subfolders
(B-Plan/, Umweltbericht/, Externe Gutachten/, Karten/, Fotos/,
Vorlagen/, Zeichnungen/) are the German-domain conventional names.

## Folder rules

### `.ai/` — hidden meta-state

Hidden because the project is AI-owned end-to-end, so meta-state should
not visually clutter the listing. Contents per orchestrator
Checkpoint 11.6:

- `state.md` — lifecycle (draft / internal-review / sent-to-authority /
  awaiting-response / revision-requested / finalized / archived),
  practices (one or more ids from `office_config.practices`),
  ownership_mode (always `full` for new projects), project name, root
  path, dates.
- `decisions.md` — major decisions with date, decision, reasoning,
  source (user, UNB, client). Audit trail.
- `module-decisions.md` — which optional template modules included or
  excluded per doctype, with reasoning. Required by Checkpoint 6.3.
- `file-map.md` — interpretation of files when project structure
  diverges from this canonical layout. Empty for new projects until
  divergence appears.
- `correspondence-log.md` — index of mails / calls / meetings with
  one row per item: date, party, type (mail/call/in-person), subject,
  artifact path. Updated whenever a new `.eml` lands or call note is
  added.
- `snapshots/` — immutable artifact bundles created by the send gate
  (Checkpoint 4.3). One subfolder per send event.

### `inputs/` — source materials

The orchestrator reads from `inputs/` to understand project context.
Subdivided by source rather than by document type, because the same
type of document (e.g. a Vermessung) means different things depending
on whether the Auftraggeber or a Behörde provided it.

- `auftraggeber/` — what the client gave us (briefing, contract,
  plans-as-given, technical specs, contact data).
- `behoerden/` — regulatory inputs (UNB requirements, RREP excerpts,
  Innenbereichssatzung text, planungsrechtliche Vorgaben).
- `erhebungen/` — empirical inputs gathered for the project
  (Vermessungen, Bestandsaufnahmen, drone scans, photo surveys, OCR
  output of older docs).
- `gis-data/` — raw GIS data the project depends on (shapefiles,
  geopackages from external sources). For multi-practice projects, a
  GIS sibling practice's workspace consumes from here.
- `stellungnahmen/` — incoming Stellungnahmen during public/Behörden
  consultation, organized by submitter and date. Source material for
  the Abwägung doctype.

Subfolder layout inside `inputs/` is flexible — flat dump or nested
subfolders both work. The chunker doesn't care about depth; metadata
picks up subfolder names as tags.

When new files arrive (e.g. drone scan dropped into `erhebungen/`),
the orchestrator notices on next session and proposes ingestion via
`ingest_project_inputs` (or fallback Read).

### Doctype folders (B-Plan, F-Plan, Umweltbericht, …)

Each doctype lives in its own top-level folder. Inside each:

- A subfolder per document (`Begründung/`, `Festsetzungen/`, …) holding
  one LaTeX project (master file from app skeleton + Projektdaten +
  Textbausteine).
- Working build artifacts (`*.aux`, `*.fdb_latexmk`, `*.log`, etc.) live
  inside the document subfolder. Gitignored at project root.
- Compiled outputs (`*.pdf`) live alongside source. The send gate copies
  the final compile output to `Auslieferung/<date>-<recipient>/`.

### `Schriftverkehr/` — correspondence

Single pane for all communication. The `eml/` subfolder is the drop
zone for mail-client-exported messages (manual drop initially;
automated poller deferred).

`ausgehend/` is for mails / letters that the AI drafts for sending.
Each draft becomes immutable (snapshotted) on send via the send gate.

### `TöB/` — Träger öffentlicher Belange

Per BauGB consultation rounds. New round = new subfolder named after
the legal basis (e.g. `4_1-fruehzeitig` for §4 Abs.1 BauGB consultation).

Each round folder holds:
- The Anschreiben (outgoing letter to TöB) drafted by the AI
- Incoming Stellungnahmen (or pointers to where they are in
  `inputs/stellungnahmen/`)
- The TöB-list (which Behörden/Träger were addressed)

### Multi-practice projects

For projects involving more than one practice (per `state.md.practices[]`),
each practice owns its own working area. The orchestrator's practice
does not write into another practice's directories (e.g. a sibling
GIS practice's `scripts/`, `workflow.yaml`, `*.qgz`). It reads outputs
the other practice publishes (e.g. to `Karten/`) for inclusion in
narrative documents.

For single-practice projects, no other-practice folders need exist.

### `Auslieferung/` — final deliverables

The send gate (Checkpoint 4.3) creates a subfolder per send event
named `YYYY-MM-DD-recipient/`. Contents:

- The signed-off PDF
- The source `.tex` files used to compile (immutable copy)
- The cover mail draft (final version sent)
- A `manifest.txt` listing what was sent and when

This is the audit trail when a revision request comes back six months
later. Diff `Auslieferung/<date>-<recipient>/source.tex` against the
current Begründung to see exactly what changed.

## Non-goals

- This structure is for new (AI-owned) projects. Existing projects
  keep whatever structure they have; the binding flow records the
  actual layout in `_ai/file-map.md`.
- Office-shared materials (e.g. shared bibliographies, regional
  standards, office-internal admin folders) live at the parent
  `paths.projects_root` level or under `paths.state_root`, not inside
  individual project folders. Not addressed here.
