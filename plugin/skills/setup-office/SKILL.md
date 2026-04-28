---
name: setup-office
description: This skill should be used the first time the plugin is deployed to a new planning bureau, when the office-config.yaml is missing, or when the user asks to "set up office", "first-time setup", "bootstrap office", "deploy to a new office", "Kanzlei einrichten", or "configure office". The orchestrator auto-routes here when office_config.load() raises OfficeConfigNotFoundError. Walks the user interactively through every required field, writes office-config.yaml at the resolved location, bootstraps the office state directory tree, validates the result.
version: 0.2.0
license: MIT
---

# setup-office

First-time deployment wizard for a German Planungsbüro. Generates a
valid `office-config.yaml`, registers the office's planning **scope**
(domains + Bundesländer), wires up integration adapters, creates the
office's state directory tree, and validates that the backend can
load the resulting configuration.

## Load this now

Read `references/wizard-flow.md` for the conversational walk-through
script — what to ask in what order, what defaults to suggest, what
to write where.

Read `<repo>/docs/office-config.schema.yaml` for the schema this
skill must produce (currently v2).

## When invoked

Three modes:

- **First-time bootstrap** (most common): no office-config exists.
  Trigger: orchestrator calls this skill on session start when
  `office_config.discover_path()` returns `None`. Or user says
  "set up office".
- **Migration**: an existing config has a lower `schema_version`
  than the running app supports. Backend forward-migrates in memory
  on load; this skill is responsible for writing the migrated form
  back to disk + asking the user to fill in any newly-required
  fields (e.g. v1→v2 leaves `scope` empty — user picks domains/states
  here).
- **Reconfigure**: user asks to change a value (add a domain to
  scope, register an additional state, swap an integration adapter,
  add a practice). Trigger: phrases like "add Wind to scope",
  "register BB references", "switch to thunderbird email", "add a
  practice".

## Behavior — first-time bootstrap

1. **Determine config location**:
   - `$PBS_OFFICE_CONFIG` if set, else
     `${XDG_CONFIG_HOME:-~/.config}/pbs-bureau/office.yaml`.
   - Tell the user where the file will land; allow override.

2. **Walk the wizard** (per `references/wizard-flow.md`). The wizard
   covers, in order:
   - Office identity (name, short, language, address, signature).
   - Practices (default: single `main` practice).
   - Partners (optional list of external collaborators).
   - Filesystem paths (state_root, references_root, projects_root).
   - **Scope** (NEW v0.2): multi-select domains + Bundesländer from
     what's available under `<repo>/extensions/{domain,state}/`.
   - Conventions (project naming, numbering, folder layout).
   - Templates (skeleton source, office_style_dir, identity_macros)
     — and for each domain in scope, offer the matching domain-style
     overlay (`office-style.<DOMAIN>.sty`) as starter content.
   - **Reference + doctype manifests** (NEW shape v0.2): build the
     layered `extensions.{references,doctypes}_manifests` map
     automatically from scope. The user does not list paths
     individually — the skill derives:
       - `universal: <repo>/extensions/universal/<...>.yaml`
       - For each domain: `<repo>/extensions/domain/<X>/<...>.yaml`
       - For each state: `<repo>/extensions/state/<X>/<...>.yaml`
     The user is shown the resolved set + asked to confirm.
   - **Integrations** (NEW v0.2): per class (email, calendar,
     scanner, phone, accounting), default `none`. Offer the
     available adapters; if the user wants email integration,
     also collect adapter-specific config.

3. **Write the YAML**. Validate by calling
   `office_config.load()`; abort + surface error if invalid.

4. **Bootstrap the office state directory** (per
   `references/wizard-flow.md` Step 9):
   - Empty state files at `<state_root>/`.
   - `<state_root>/templates/office-style.sty` — copy of the
     app-shipped default.
   - For each domain in scope: optionally copy
     `office-style.<DOMAIN>.sty` overlay if user wanted it.
   - Empty `<references_root>/{gesetze/{bund,eu,<state>},
     leitfaeden,urteile,beispiele}/` + `changelog.md`.

5. **Verify**: re-run `office_config.load()`; confirm
   `cfg.all_references_manifests()` returns a non-empty list (means
   scope properly wires through to manifests).

6. **Suggest next steps**:
   - "Run `research-references` to fetch the references corpus
     based on your scope."
   - "Register your first project via `setup_project`."

## Behavior — reconfigure

1. Identify which value(s) the user wants to change.
2. Read existing `office-config.yaml`.
3. Walk only the changed sections (don't re-prompt unchanged ones).
4. If scope changes (adding a domain or state):
   - Update `scope.{domains,states}`.
   - Add the corresponding entries to
     `extensions.{references,doctypes}_manifests.{domain,state}`.
   - Bootstrap any missing directories (e.g. new state's
     `<references_root>/gesetze/<state>/`).
5. Write the updated file. Validate.

## Behavior — migration

1. Read existing config; detect `schema_version`.
2. The backend already forward-migrates on load (see
   `office_config_migrations/`). Re-run `office_config.load()` to get
   the migrated dict.
3. For each newly-required field with empty defaults, prompt the
   user to fill in (most commonly: `scope.domains`, `scope.states`,
   `extensions.{references,doctypes}_manifests.universal`).
4. Write the fully-migrated + filled-in form back to disk. Validate.
5. Report: which fields were added, which the user filled in.

## Conversational style

Match the user's language (German or English). Surface defaults
clearly so the user can accept with `y`/`Enter`. Don't ask
philosophical questions — just walk through what's required.

For single-practice offices, suggest the simplest answer
(`practices: [{id: main, label: "Büro"}]`); offer to expand only
if the user mentions multiple sub-disciplines.

For scope: discover what's available by listing
`<repo>/extensions/domain/*/` and `<repo>/extensions/state/*/`.
Skip empty placeholder dirs (those with only `.gitkeep`).

## Output

A summary block at the end:

```
Office configured at: <config-path>
Office state at: <state-root>
References corpus at: <references-root>
Projects root at: <projects-root>

Scope:
  Domains: PV-FFA, Wind, Naturschutz
  States: MV

Practices: main, …
Partners: hendrik (deroekologe), …

Reference manifests selected (in load order):
  universal: <repo>/extensions/universal/references-manifest.yaml
  domain/PV-FFA: <repo>/extensions/domain/PV-FFA/references-manifest.yaml
  domain/Wind: <repo>/extensions/domain/Wind/references-manifest.yaml
  domain/Naturschutz: <repo>/extensions/domain/Naturschutz/references-manifest.yaml
  state/MV: <repo>/extensions/state/MV/references-manifest.yaml

Integrations:
  email: thunderbird-maildir → ~/.thunderbird/<profile>/
  calendar: none
  scanner: hot-folder → ~/Documents/Scans/
  phone: none
  accounting: none

Office style: default + PV-FFA overlay + Wind overlay
  (customize at <state-root>/templates/office-style.sty and
  office-style.PV-FFA.sty + office-style.Wind.sty)

Next steps:
  - Run /research-references to fetch your scoped references corpus.
  - Bind your first project: setup_project <name>.
```

## Edge cases

- **Path doesn't exist**: state_root, references_root, projects_root
  may not exist when first declared. Create them with user
  confirmation.
- **Path on offline network mount**: surface error; ask user to
  mount or pick a different path.
- **Existing office-config at the resolved path**: don't overwrite
  silently. Offer: reconfigure existing | overwrite | abort.
- **Empty domain/state list discovered under extensions/**: warn
  the user — they may have an outdated repo. Still allow them to
  proceed with universal-only.
- **User picks a state with no canonical manifest** (most non-MV
  states currently): warn that the state extension is
  placeholder-only; offer to scaffold an empty manifest at
  `<repo>/extensions/state/<X>/references-manifest.yaml` and route
  through `author-manifest` to populate.
- **state_root coincides with projects_root**: allowed, warn.

## Tools used

- `Glob` to discover available domain/state extensions under
  `<repo>/extensions/`.
- `Read` for the universal references-manifest to show user what
  ships in scope.
- `Write` for the YAML and bootstrap files.
- `Bash` for `mkdir -p` and copying defaults.
- The backend's `office_config.load()` after writing, to validate.
- Hands off to `author-manifest` if the user wants to author a
  state/domain manifest that doesn't yet exist.
