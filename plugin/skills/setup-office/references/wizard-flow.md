# setup-office wizard flow

Conversational walk-through for first-time office configuration.
Each step shows the prompt, the default, and what to write.

## Pre-flight

Before prompting:
- Resolve config path (env var or XDG default). Tell user the path.
- Check parent directory writable.
- If existing config at path: ask `reconfigure | overwrite | abort`.

## Step 1 — Office identity

```
Office name: ________________
   (required, full name, e.g. "Planungsbüro Schmidt")

Short name / abbreviation: ____
   (required, used in IDs/filenames, e.g. "PSchmidt")

Output language: [de_DE]
   (only de_DE supported currently; just confirm)
```

Map to: `office.name`, `office.short`, `office.language`.

## Step 2 — Address & contact

```
Address lines (one per line, blank to finish):
> ________________
> ________________
> ________________

Phone (optional, blank to skip): ____
Email (optional, blank to skip): ____
Web URL (optional, blank to skip): ____

Signature block (will be inserted verbatim into cover mails).
Multi-line, end with blank line:
> ________________
> ________________
```

Map to: `identity.{address_lines, phone, email, web,
signature_block}`.

## Step 3 — Practices

```
Does the office have multiple distinct sub-practices (e.g. text
documents and GIS)? [y/N]

If N (default — single practice):
  → write practices: [{id: main, label: "Büro"}]

If y:
  For each practice:
    Practice ID (short, kebab-case, e.g. "schulz"): ____
    Practice label: ________________
    Per-practice signer (optional, blank = use office signature): ____

  Repeat until user enters blank ID.
```

Map to: `practices[]`.

## Step 4 — Filesystem paths

```
State root (where _ai-office-state/ + templates/ + extensions/ live):
  Default: <user-suggestion based on home dir>
  Path: ________________

References corpus root (AI-fetched legal references):
  Default: <state_root>/_ai-references     (alternative: own path)
  Path: ________________

Projects root (where client project folders live):
  Default: ________________  (often hidrive / NAS / cloud-sync mount)
  Path: ________________

Local LaTeX repos root (optional — if office keeps per-doctype LaTeX
in a dev tree):
  Default: skip
  Path: ____ (or blank)
```

Validate: each path exists OR ask permission to create. If on a
non-mounted volume, abort + tell user to mount first.

Map to: `paths.{state_root, references_root, projects_root,
local_repos_root}`.

## Step 5 — Conventions

```
Project naming template
  (placeholders: {year_2}, {year_4}, {nr}, {nr_pad:N}, {client}, {location}):
  Default: "{year_2}-{nr} {client} - {location}"
  Pattern: ________________

Project numbering pattern: [YY-NN | YYYY-NN | NN | YY/NN]
  Default: YY-NN

Auto-increment project number? [Y/n]
  Default: Yes

Folder layout (role → literal name):
  inputs/         [default: inputs/]
  sent versions/  [default: Auslieferung/]
  correspondence/ [default: Schriftverkehr/]
  TöB/            [default: TöB/]

  Press Enter to accept defaults; type a different name to override.
```

Map to: `conventions.project_naming`,
`conventions.project_numbering.{pattern, auto_increment}`,
`conventions.project_folder_layout.{inputs, sent_versions,
correspondence, toeb}`.

## Step 6 — Templates

```
LaTeX skeleton source: [app | <override-path>]
  Default: app   (uses skeletons shipped with this plugin)

Office style directory: <state_root>/templates
  (where office-style.sty lives — accept default unless you have a
  specific reason)

Identity macros: [auto | <hand-maintained-path>]
  Default: auto   (regenerated from identity: section before each compile)
```

Map to: `templates.{skeleton_source, office_style_dir,
identity_macros}`. Leave `templates.doctype_overrides` empty.

## Step 7 — Reference extensions

```
Federal-core references (BauGB, BNatSchG, EEG, KNE leitfäden,
BVerwG/EuGH rulings, etc.) ship with the app.

Will the office work on projects in specific German Bundesländer
that need state-law extensions? [y/N]

If y:
  Enter Bundesland codes (one per line; valid:
  BB BW BY BE HB HH HE MV NI NW RP SH SL SN ST TH).

  For each:
    Code: ____
    Path: [default: <state_root>/extensions/<CODE>/references-manifest.yaml]
    Use default? [Y/n]

  Repeat until user enters blank code.

If N:
  Skip — extensions can be added later via reconfigure.
```

Map to: `extensions.references_manifests` map.

For each registered extension, if the app ships an example template
at `<repo>/docs/office-extensions/<CODE>/references-manifest.example.yaml`,
copy it to the registered path so the user starts with a working
state-extension manifest. Otherwise create an empty skeleton.

## Step 8 — Bootstrap state directory

After config is written + validated, create:

```
<state_root>/
├── projects-index.md         (empty header)
├── pending-actions.md        (empty header)
├── recent-correspondence.md  (empty header)
├── templates/
│   └── office-style.sty      (copy of office-style.default.sty)
├── extensions/
│   └── <CODE>/
│       └── references-manifest.yaml   (per registered extension)

<references_root>/
├── gesetze/
│   ├── bund/                 (empty)
│   ├── eu/                   (empty)
│   └── <CODE>/               (per registered state, empty)
├── leitfaeden/               (empty)
├── urteile/                  (empty)
├── beispiele/                (empty)
└── changelog.md              (empty header)
```

If `paths.projects_root` doesn't exist yet, ask if it should be
created. Don't create silently — projects_root is often on a
shared/cloud-synced volume and creating an empty folder might
clobber meaningful content.

## Step 9 — Validate + summarize

Re-run `office_config.load()` → must succeed.

Output the summary block per SKILL.md `## Output` section.

## Helpful defaults to suggest by environment

When the user is on Linux and a hidrive folder is mounted, suggest
those paths as defaults:

```
state_root:    <hidrive-mount>/_ai-office-state
references_root: <hidrive-mount>/_ai-references
projects_root: <hidrive-mount>/Projekte
```

The skill must NOT assume any specific hidrive mount path; detect
mounted volumes via `Bash` `mount | grep` or just ask. Don't
hardcode.
