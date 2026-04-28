# setup-office wizard flow

Conversational walk-through for first-time office configuration
(schema v2). Each step shows the prompt, the default, and what to
write into `office-config.yaml`.

## Pre-flight

Before prompting:
- Resolve config path (env var or XDG default). Tell user the path.
- Check parent directory writable.
- If existing config at path: ask `reconfigure | overwrite | abort`.
- Discover available domains: `Glob extensions/domain/*/` (skip
  dirs containing only `.gitkeep`).
- Discover available states: `Glob extensions/state/*/` (likewise).

## Step 1 — Office identity

```
Office name: ________________
   (required, full name, e.g. "Planungsbüro Schmidt")

Short name / abbreviation: ____
   (required, used in IDs/filenames, e.g. "PSchmidt")

Output language: [de_DE]
   (only de_DE supported currently)
```

Map to: `office.name`, `office.short`, `office.language`.

## Step 2 — Address & contact

```
Akademischer Titel (optional, blank to skip): ____
   (e.g. "Dipl.-Ing.")

Address lines (one per line, blank to finish):
> ________________
> ________________
> ________________

Phone (optional, blank to skip): ____
Mobile / Funk (optional, blank to skip): ____
Fax (optional, blank to skip): ____
Email (optional, blank to skip): ____
Web URL (optional, blank to skip): ____

Specializations (one per line, blank to finish; printed on
letterhead — e.g. "Garten- und Landschaftsarchitektur"):
> ________________
> ________________

Logo image path (optional, blank to skip): ____
Signature image path (optional, blank to skip): ____

Signature block (will be inserted verbatim into cover mails).
Multi-line, end with blank line:
> ________________
> ________________
```

Map to: `identity.{title, address_lines, phone, mobile, fax, email,
web, specializations, logo_path, signature_image_path,
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
    Per-practice email (optional): ____
    Email match patterns (optional, fnmatch-style):
      > "*@<domain>"
      > ____

  Repeat until user enters blank ID.
```

Map to: `practices[]`.

## Step 4 — Partners

```
Does the office regularly collaborate with external partners (other
offices that co-produce on some projects, or are recurring clients)?
[y/N]

If y:
  For each partner:
    Partner ID: ____
    Label: ________________
    Signer name (optional): ____
    Specialization (optional, e.g. "Landschaftsökologie"): ____
    Email: ____
    Email match patterns (fnmatch-style):
      > "*@<domain>"
    Phone (optional): ____
    Web (optional): ____

  Repeat until user enters blank ID.
```

Map to: `partners[]`.

## Step 5 — Filesystem paths

```
State root (where _ai-office-state/ + templates/ live):
  Default: <suggest based on home dir or detected hidrive mount>
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

## Step 6 — Scope (NEW v2)

```
Available planning domains (under <repo>/extensions/domain/):
  [ ] PV-FFA           Photovoltaik-Freiflächenanlagen
  [ ] Wind             Windenergie an Land
  [ ] Naturschutz      Naturschutz / Artenschutz / FFH
  [ ] Innenentwicklung Urban Innenentwicklung (placeholder — populate via author-manifest)
  ...

Select all that apply (comma-separated keys, e.g. "PV-FFA,Wind,Naturschutz"):
> ________________

Available Bundesländer (under <repo>/extensions/state/):
  [ ] MV   Mecklenburg-Vorpommern   (canonical content available)
  [ ] BB   Brandenburg              (placeholder)
  [ ] BW   Baden-Württemberg        (placeholder)
  ...  (16 codes total)

Select all that apply (comma-separated codes, e.g. "MV,BB"):
> ________________
```

For each placeholder state/domain the user selects, warn:

```
"<X> is a placeholder — no canonical manifest content yet. You can
proceed with empty extension and populate later via author-manifest,
or pick a different scope."
```

Map to: `scope.domains`, `scope.states`.

## Step 7 — Conventions

```
Project naming template:
  Default: "{year_2}-{nr} {client} - {location}"
  Pattern: ________________

Project numbering pattern: [YY-NN | YYYY-NN | NN | YY/NN]
  Default: YY-NN

Auto-increment project number? [Y/n]

Folder layout:
  inputs/         [default: inputs/]
  sent versions/  [default: Auslieferung/]
  correspondence/ [default: Schriftverkehr/]
  TöB/            [default: TöB/]
```

Map to: `conventions.*`.

## Step 8 — Templates

```
LaTeX skeleton source: [app | <override-path>]
  Default: app

Office style directory: <state_root>/templates
  (where office-style.sty lives — accept default unless you have a
  specific reason)

Identity macros: [auto | <hand-maintained-path>]
  Default: auto
```

Map to: `templates.{skeleton_source, office_style_dir, identity_macros}`.

## Step 9 — Office-style overlays per scope

For each domain in `scope.domains`, check whether
`<repo>/plugin/templates/office-style/office-style.<DOMAIN>.sty`
exists. If yes:

```
Available office-style overlay for <DOMAIN> domain.
Copy to <state_root>/templates/office-style.<DOMAIN>.sty so you can
customize? [Y/n]
```

If yes, copy the file. Offices then tune their copy (or remove it
and rely on the universal office-style alone).

## Step 10 — Build the layered extensions map

This step is mostly automatic — the skill derives the manifest map
from `scope`:

```yaml
extensions:
  references_manifests:
    universal: <repo>/extensions/universal/references-manifest.yaml
    domain:
      PV-FFA: <repo>/extensions/domain/PV-FFA/references-manifest.yaml
      Wind: <repo>/extensions/domain/Wind/references-manifest.yaml
      Naturschutz: <repo>/extensions/domain/Naturschutz/references-manifest.yaml
    state:
      MV: <repo>/extensions/state/MV/references-manifest.yaml

  doctypes_manifests:
    universal: <repo>/extensions/universal/doctypes.yaml
    domain:
      Naturschutz: <repo>/extensions/domain/Naturschutz/doctypes.yaml   # if exists
    state: {}
```

Show the user the resolved set + ask to confirm. Mention that
office-local state overrides (when an office wants to add regional
Leitfäden) can be added by pointing the state entry at a
`<state_root>/extensions/<X>/references-manifest.yaml` instead.

## Step 11 — Integrations

```
Email integration:
  Available adapters:
    none                  no email integration (default)
    thunderbird-maildir   read Thunderbird local mail folders
    imap                  IMAP server (configure host/user/password)
    outlook-pst           read Outlook .pst files
    mbox-file             single mbox file

  Choose adapter [none]: ____

  If thunderbird-maildir: profile_path: ____
  If imap: server, port, user, password_ref (1Password key, env var, etc.)
  ...

Calendar integration: [none | caldav | exchange-ews | ical-file]
Scanner integration: [none | hot-folder | escli | tesseract]
Phone integration: [none | call-log-csv]
Accounting integration: [none] (no adapters yet)
```

For each, store as `{adapter: <name>, config: {<adapter-specific>}}`.

## Step 12 — Bootstrap state directory

After config is written + validated, create:

```
<state_root>/
├── projects-index.md         (empty header)
├── pending-actions.md        (empty header)
├── recent-correspondence.md  (empty header)
├── templates/
│   ├── office-style.sty                        (copy of default)
│   ├── office-style.<DOMAIN>.sty               (copy per domain in scope)
│   ├── office-logo.png                         (if identity.logo_path set)
│   └── office-signature.png                    (if signature_image_path set)

<references_root>/
├── gesetze/
│   ├── bund/                 (empty)
│   ├── eu/                   (empty)
│   └── <CODE>/               (per state in scope, empty)
├── leitfaeden/               (empty)
├── urteile/                  (empty)
├── beispiele/                (empty)
└── changelog.md              (empty header)
```

If `paths.projects_root` doesn't exist yet, ask before creating.
Don't create silently — projects_root is often on a shared volume
and creating an empty folder might mask a mount issue.

## Step 13 — Validate + summarize

Re-run `office_config.load()` → must succeed.

Verify `cfg.all_references_manifests()` returns a non-empty list
(otherwise scope didn't propagate to manifests — show the bug).

Output the summary block per SKILL.md `## Output` section.

## Helpful defaults to suggest by environment

When the user is on Linux and a hidrive folder is mounted, suggest:

```
state_root:    <hidrive-mount>/_ai-office-state
references_root: <hidrive-mount>/_ai-references
projects_root: <hidrive-mount>/Projekte
```

Detect mounted volumes via `Bash` `mount | grep` or just ask. Don't
hardcode specific user paths.
