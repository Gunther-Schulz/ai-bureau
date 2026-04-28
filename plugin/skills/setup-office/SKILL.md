---
name: setup-office
description: This skill should be used the first time the plugin is deployed to a new planning bureau, when the office-config.yaml is missing, or when the user asks to "set up office", "first-time setup", "bootstrap office", "deploy to a new office", "Kanzlei einrichten", or "configure office". The orchestrator auto-routes here when office_config.load() raises OfficeConfigNotFoundError. Walks the user interactively through every required field, writes office-config.yaml at the resolved location, bootstraps the office state directory tree (templates/, extensions/, _ai-references/, _ai-office-state/), validates the result.
version: 0.1.0
license: MIT
---

# setup-office

First-time deployment wizard. Generates a valid `office-config.yaml`,
creates the office's state directory tree, and validates that the
backend can load the resulting configuration.

## Load this now

Read `references/wizard-flow.md` for the conversational walk-through
script — what to ask in what order, what defaults to suggest, what
to write where.

Read `<repo>/docs/office-config.schema.yaml` for the schema this
skill must produce.

## When invoked

Three modes:

- **First-time bootstrap** (most common): no office-config exists
  anywhere. Trigger: orchestrator calls this skill on session start
  when `office_config.discover_path()` returns `None`. Or user says
  "set up office".
- **Migration** (future): an existing config has a lower
  `schema_version` than the running app supports. Trigger: app on
  load detects version mismatch.
- **Reconfigure**: user asks to change a value (e.g. add a
  practice, register a new state extension). Trigger: phrases like
  "add a practice", "register MV references", "change office
  address".

## Behavior — first-time bootstrap

1. **Determine config location**:
   - If `$PBS_OFFICE_CONFIG` is set, use that path.
   - Else default to `${XDG_CONFIG_HOME:-~/.config}/pbs-bureau/office.yaml`.
   - Tell the user where the file will be written; allow override.

2. **Walk the wizard** (per `references/wizard-flow.md`). Required
   fields:
   - `office.name`, `office.short`, `office.language` (always
     `de_DE` for now).
   - `identity.address_lines` (≥1), `identity.signature_block`.
     Optional `identity.phone`, `identity.email`, `identity.web`.
   - `practices[]` (≥1 entry; for single-practice offices, default
     to `[{id: main, label: "Büro"}]`).
   - `paths.state_root`, `paths.references_root`,
     `paths.projects_root`. Optional `paths.local_repos_root`.
   - `conventions.project_naming` (default
     `"{year_2}-{nr} {client} - {location}"`).
   - `conventions.project_numbering.{pattern,auto_increment}`
     (defaults `YY-NN`, `true`).
   - `conventions.project_folder_layout.*` (defaults `inputs/`,
     `Auslieferung/`, `Schriftverkehr/`, `TöB/`).
   - `templates.skeleton_source` (default `"app"`),
     `templates.office_style_dir` (default
     `<state_root>/templates`), `templates.identity_macros`
     (default `"auto"`).
   - `extensions.references_manifests` — empty by default. For
     each Bundesland the office expects to operate in, prompt
     whether to register an extension manifest now (with default
     path `<state_root>/extensions/<STATE>/references-manifest.yaml`).

3. **Write the YAML**. Validate against the schema (load via
   `office_config.load()`); abort + surface error if invalid.

4. **Bootstrap the office state directory**:
   - `<state_root>/projects-index.md` (empty header).
   - `<state_root>/pending-actions.md` (empty header).
   - `<state_root>/recent-correspondence.md` (empty header).
   - `<state_root>/templates/office-style.sty` (copy of
     `<repo>/plugin/templates/office-style/office-style.default.sty`).
   - `<state_root>/extensions/<STATE>/references-manifest.yaml` for
     each registered extension (copy of
     `<repo>/docs/office-extensions/<STATE>/references-manifest.example.yaml`
     if it exists; otherwise empty skeleton).
   - `<references_root>/` with subdirectories `gesetze/{bund,eu}`,
     `gesetze/<STATE>` for each registered state, `leitfaeden/`,
     `urteile/`, `beispiele/`, plus an empty `changelog.md`.

5. **Verify**: re-run `office_config.load()` and confirm it
   succeeds. List the created paths.

6. **Suggest next steps**:
   - "Run `research-references` to fetch the federal-core manifest
     entries into your references corpus."
   - "Register your first project via `setup_project`."

## Behavior — reconfigure

1. Identify which value(s) the user wants to change.
2. Read existing `office-config.yaml`.
3. Walk only the changed sections (don't re-prompt unchanged ones).
4. Write the updated file. Validate.
5. If new state extension was added, scaffold its directories.

## Behavior — migration

1. Read existing config; detect `schema_version`.
2. For each version step from old → current, apply the migration
   recipe (load from `references/migrations/v<N>-to-v<N+1>.md`).
3. Write the migrated file. Validate.
4. Report: which fields were added/renamed/removed.

## Conversational style

Match the user's language (German or English). Surface defaults
clearly so the user can accept with `y`/`Enter`. Don't ask
philosophical questions — just walk through what's required.

For single-practice offices, suggest the simplest answer
(`practices: [{id: main, label: "Büro"}]`); offer to expand only
if the user mentions multiple sub-disciplines.

## Output

A summary block at the end:

```
Office configured at: <config-path>
Office state at: <state-root>
References corpus at: <references-root>
Projects root at: <projects-root>
Practices: <id-1>, <id-2>, ...
Registered state extensions: <STATE-1>, <STATE-2>, ...
Office style: default (customize at <state-root>/templates/office-style.sty)

Next steps:
  - Run /research-references to fetch the federal-core manifest.
  - Optionally register state extensions for the Bundesländer you
    work in.
  - Bind your first project: setup_project <name>.
```

## Edge cases

- **Path doesn't exist**: state_root, references_root,
  projects_root may not exist when first declared. Create them
  (with user confirmation) — bootstrap would fail otherwise.
- **Path is on a network mount that's offline**: surface error;
  ask user to mount or pick a different path.
- **Existing office-config at the resolved path**: don't overwrite
  silently. Offer: reconfigure existing | overwrite | abort.
- **Office wants no practices distinction**: still write one entry
  (`{id: main, label: "Büro"}`). The data model is uniform.
- **User wants to skip extension setup at first run**: allow.
  Extensions can be added later via reconfigure mode.
- **state_root coincides with projects_root** (some offices
  prefer this): allowed, but warn — co-locating means office state
  files appear inside the projects folder listing.

## Tools used

- Direct filesystem `Write` for the YAML and bootstrap files.
- `Bash` for `mkdir -p` and copying defaults.
- The backend's `office_config.load()` after writing, to validate.
- No MCP backend dependency for the wizard itself.
