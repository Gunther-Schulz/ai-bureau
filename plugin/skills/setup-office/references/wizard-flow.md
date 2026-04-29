# setup-office wizard flow

Conversational walk-through for first-time office configuration
(schema **v3** — post-design-review session 5 consolidation). Each
step shows the prompt, the default, and what to write into
`office-config.yaml`.

**v3 reshape summary** (vs v2):
- `office` and `identity` merged into one `office` block
- `practices` and `partners` merged into `actors[]` with
  `kind: internal|external` discriminator
- `paths` renamed to `roots` with shorter field names (state,
  references, projects, local_repos)
- `templates.office_style_dir` moved into `roots.office_style_dir`
- `extensions:` block dropped (manifests auto-discovered from scope)
- `integrations:` is a free-form list, not a fixed-key map

## Pre-flight

Before prompting:
- Resolve config path (env var or XDG default). Tell user the path.
- Check parent directory writable.
- If existing config at path: ask `reconfigure | overwrite | abort`.
- Discover available domains: `Glob extensions/domain/*/` (skip
  dirs containing only `.gitkeep`).
- Discover available states: `Glob extensions/state/*/` (likewise).

## Step 1 — Office identity (single block)

```
Office name: ________________
   (required, full name, e.g. "Planungsbüro Schmidt")

Short name / abbreviation: ____
   (required, used in IDs/filenames, e.g. "PSchmidt")

Output language: [de_DE]
   (only de_DE supported currently)

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

Logo image path (optional, blank to skip): ____
Signature image path (optional, blank to skip): ____

Signature block (will be inserted verbatim into cover mails).
Multi-line, end with blank line:
> ________________
> ________________
```

Map to: `office.{name, short, language, title, address_lines, phone,
mobile, fax, email, web, specializations, logo_path,
signature_image_path, signature_block}`. All in one block; v2's
separate `identity:` no longer exists.

## Step 2 — Actors (internal practices + external partners)

```
Actors are signing entities — internal practices (sub-units of THIS
office) and external partners (collaborators). They share the same
shape; `kind` discriminates. At least one internal actor is required.

Default: single internal actor with id=main.

Internal actors (sub-practices of this office):
  Does the office have multiple distinct sub-practices (e.g. text
  documents and GIS)? [y/N]

  If N (default — single practice):
    → write actors: [{id: main, kind: internal, label: "Büro",
                      signer: "<your name>"}]

  If y:
    For each internal actor:
      ID (short, kebab-case, e.g. "schulz"): ____
      Label: ________________
      Signer name (optional, blank = use office signature_block): ____
      Email (optional): ____
      Email match patterns (optional, fnmatch-style):
        > "*@<domain>"

External actors (partners):
  Does the office regularly collaborate with external partners (other
  offices that co-produce on some projects, or recurring clients)? [y/N]

  If y:
    For each external actor:
      ID: ____
      Label: ________________
      Signer name: ____
      Specialization (optional, e.g. "Landschaftsökologie"): ____
      Email: ____
      Email match patterns: ____
      Phone (optional): ____
      Web (optional): ____
```

Map to: `actors[]`. Order: internal first, then external. Each entry
has `kind: internal|external` set.

## Step 3 — Filesystem roots

```
State root (where _ai-office-state/ + templates/ live):
  Default: <suggest based on home dir or detected hidrive mount>
  Path: ________________

References corpus root (AI-fetched legal references):
  Default: <state>/_ai-references     (alternative: own path)
  Path: ________________

Projects root (where client project folders live):
  Default: ________________  (often hidrive / NAS / cloud-sync mount)
  Path: ________________

Local LaTeX repos root (optional — if office keeps per-doctype LaTeX
in a dev tree):
  Default: skip
  Path: ____ (or blank)

Office style directory (optional — defaults to <state>/templates):
  Default: <state>/templates
  Path: ____ (or blank to accept default)

Office extensions directory (optional — for office-local references
manifest additions; mirrors <repo>/extensions/<scope>/ layout):
  Default: skip
  Path: ____ (or blank)
```

Validate: each path exists OR ask permission to create. If on a
non-mounted volume, abort + tell user to mount first.

Map to: `roots.{state, references, projects, local_repos,
office_style_dir, office_extensions}`.

## Step 4 — Scope

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

Map to: `scope.domains`, `scope.states`. **Manifests are NOT
declared anywhere** — the loader walks `<repo>/extensions/...`
filtered by scope at runtime (and `roots.office_extensions/` if set).

## Step 5 — Integrations (free-form list)

```
Which external systems does the office integrate with?

Common classes:
  email      mail integration (Thunderbird, IMAP, Outlook .pst, mbox)
  calendar   calendar (CalDAV, Exchange EWS, .ical)
  scanner    scanner / hot-folder OCR
  phone      call log integration
  accounting accounting / invoicing
  (other)    DMS, GIS, CAD, project-management, TöB-Portal, ...

For each class the office uses, declare it. Skip the rest.

Email? [y/N]
  If y, available adapters (discovered from
  backend/.../integrations/email/*.py):
    thunderbird-maildir   read Thunderbird local mail folders
    imap                  IMAP server (configure host/user/password)
    outlook-pst           read Outlook .pst files
    mbox-file             single mbox file

  Choose adapter: ____
  Config (adapter-specific):
    thunderbird-maildir: profile_path: ____
    imap: server, port, user, password_ref (1Password key, env var, etc.)
    ...

Scanner? [y/N]
  If y, adapter + config (similar prompt).

Calendar? [y/N]
Phone? [y/N]
Accounting? [y/N]

(Other classes — DMS, GIS, etc. — only if user explicitly mentions.
The class set is open; any string is valid as long as a matching
subpackage exists.)
```

Map to: `integrations: [{class, adapter, config}, ...]`. Omit any
class the office doesn't use; v3 lists declared integrations only,
no `adapter: none` placeholders.

## Step 6 — Conventions

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

## Step 7 — Templates

```
LaTeX skeleton source: [app | <override-path>]
  Default: app

Identity macros: [auto | <hand-maintained-path>]
  Default: auto
```

Map to: `templates.{skeleton_source, identity_macros, doctype_overrides}`.

Note: `office_style_dir` was moved to `roots:` block in v3 (see
Step 3).

## Step 8 — Office-style overlays per scope

For each domain in `scope.domains`, check whether
`<repo>/plugin/templates/office-style/office-style.<DOMAIN>.sty`
exists. If yes:

```
Available office-style overlay for <DOMAIN> domain.
Copy to <roots.office_style_dir>/office-style.<DOMAIN>.sty so you
can customize? [Y/n]
```

If yes, copy the file. Offices then tune their copy (or remove it
and rely on the universal office-style alone).

## Step 9 — Bootstrap state directory

After config is written + validated, create:

```
<roots.state>/
├── projects-index.md         (empty header)
├── pending-actions.md        (empty header)
├── recent-correspondence.md  (empty header)
└── (further state files added by other skills as needed)

<roots.office_style_dir>/      (default: <roots.state>/templates/)
├── office-style.sty                        (copy of default)
├── office-style.<DOMAIN>.sty               (copy per domain in scope)
├── office-logo.png                         (if office.logo_path set)
└── office-signature.png                    (if signature_image_path set)

<roots.references>/
├── gesetze/
│   ├── bund/                 (empty)
│   ├── eu/                   (empty)
│   └── <CODE>/               (per state in scope, empty)
├── leitfaeden/               (empty)
├── urteile/                  (empty)
├── beispiele/                (empty)
└── changelog.md              (empty header)
```

If `roots.projects` doesn't exist yet, ask before creating.
Don't create silently — projects root is often on a shared volume
and creating an empty folder might mask a mount issue.

## Step 10 — Validate + summarize

Re-run `office_config.load()` → must succeed.

Verify `config.all_references_manifests()` returns a non-empty list
(otherwise scope didn't propagate to manifests — show the bug; v3
returns triples `(path, layer, scope_key)`).

Output the summary block per SKILL.md `## Output` section.

## Helpful defaults to suggest by environment

When the user is on Linux and a hidrive folder is mounted, suggest:

```
roots.state:      <hidrive-mount>/_ai-office-state
roots.references: <hidrive-mount>/_ai-references
roots.projects:   <hidrive-mount>/Projekte
```

Detect mounted volumes via `Bash` `mount | grep` or just ask. Don't
hardcode specific user paths.
