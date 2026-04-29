---
name: setup-office
description: This skill should be used the first time the plugin is deployed to a new planning bureau, when the office-config.yaml is missing, or when the user asks to "set up office", "first-time setup", "bootstrap office", "deploy to a new office", "Kanzlei einrichten", or "configure office". The orchestrator auto-routes here when office_config.load() raises OfficeConfigNotFoundError. Walks the user interactively through every required field, writes office-config.yaml at the resolved location, bootstraps the office state directory tree, validates the result.
version: 0.6.0
license: MIT
mcp_tools_required: []
mcp_tools_optional: []
fallback_when_mcp_absent: "skill is filesystem-only (Glob/Read/Write/Edit/Bash + office_config.load() Python helper); no MCP dependencies. Bootstrap-then-validate pattern: the wizard writes office-config.yaml directly then calls office_config.load() in-process to validate. This bypasses the gate-only-write rule by design (no `create_office_config` MCP tool exists for first-deploy bootstrap; the validation-after-write closes the loop). Future fix: a `create_office_config` MCP tool for full fail-closed compliance — tracked in ROADMAP."
summary: First-time office deployment wizard — writes office-config.yaml + bootstraps state directory tree. Re-runs for migration or reconfigure.
routing_mode: direct
triggers:
  - set up office
  - first-time deployment
  - configure office
  - Kanzlei einrichten        # German technical anchor
handoffs: [author-manifest]
phase_role: bureau_setup
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
skill must produce (currently v3 — post-design-review session 5
consolidation: office+identity merged, paths→roots, practices+
partners→actors, manifests now derived from scope, integrations is
a free-form list).

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
  fields. Migration paths: v1→v2 (legacy), v2→v3 (current).
- **Reconfigure**: user asks to change a value (add a domain to
  scope, register an additional state, swap an integration adapter,
  add an actor). Trigger: phrases like "add Wind to scope",
  "register BB references", "switch to thunderbird email", "add a
  practice", "add a partner".

## Behavior — first-time bootstrap

1. **Determine config location**:
   - `$PBS_OFFICE_CONFIG` if set, else
     `${XDG_CONFIG_HOME:-~/.config}/pbs-bureau/office.yaml`.
   - Tell the user where the file will land; allow override.

2. **Walk the wizard** (per `references/wizard-flow.md`). The wizard
   covers, in order:
   - **Office identity** (single block — name, short, language,
     title, address_lines, phone/mobile/email/web optional,
     specializations, logo/signature image paths, signature_block).
   - **Actors** (≥1 internal required; external partners optional).
     Each: id, kind (internal|external), label, signer, email,
     email_match_patterns, optional phone/web/specialization. Default:
     single internal actor with id=main.
   - **Filesystem roots** (state, references, projects; optional
     local_repos, office_style_dir, office_extensions).
   - **Scope**: multi-select domains + Bundesländer from what's
     available under `<repo>/extensions/{domain,state}/`. Manifests
     are no longer listed in config — they're auto-discovered from
     scope at runtime.
   - **Integrations** (free-form list): for each external system
     the office uses (email, calendar, scanner, etc.), declare
     `{class, adapter, config}`. Omit classes the office doesn't
     use. Available adapters per class are discovered from
     `backend/.../integrations/<class>/*.py`.
   - **Conventions** (project naming, numbering, folder layout).
   - **Templates**: skeleton_source (default `app`),
     identity_macros (default `auto`), doctype_overrides (rare).
     For each domain in scope, offer the matching domain-style
     overlay (`office-style.<DOMAIN>.sty`) as starter content
     (`roots.office_style_dir` will host them).

3. **Write the YAML**. Validate by calling
   `office_config.load()`; abort + surface error if invalid.

4. **Bootstrap the office state directory** (per
   `references/wizard-flow.md`):
   - Empty state files at `<roots.state>/`.
   - `<roots.office_style_dir>/office-style.sty` — copy of the
     app-shipped default.
   - For each domain in scope: optionally copy
     `office-style.<DOMAIN>.sty` overlay if user wanted it.
   - Empty `<roots.references>/{gesetze/{bund,eu,<state>},
     leitfaeden,urteile,beispiele}/` + `changelog.md`.

5. **Verify**: re-run `office_config.load()`; confirm
   `config.all_references_manifests()` returns a non-empty list
   (means scope properly wires through to manifests).

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
   - **No** manifest-map updates needed (v3 derives manifests from
     scope at runtime). Confirm the corresponding extension files
     exist at `<repo>/extensions/{domain,state}/<X>/...`; if not,
     hand off to `author-manifest` to scaffold.
   - Bootstrap any missing directories (e.g. new state's
     `<roots.references>/gesetze/<state>/`).
5. Write the updated file. Validate.

## Behavior — migration

1. Read existing config; detect `schema_version`.
2. The backend already forward-migrates on load (see
   `office_config_migrations/`). Re-run `office_config.load()` to get
   the migrated dict.
3. For each newly-required field with empty defaults, prompt the
   user to fill in. Most common cases:
   - v1→v2 left `scope` empty — user picks domains/states
   - v2→v3 dropped the manifest map (now derived) and reshaped
     several blocks; verify the migrated shape is correct
4. Write the fully-migrated + filled-in form back to disk. Validate.
5. Report: which fields were added/reshaped, which the user filled in.

## Conversational style

Match the user's language (German or English). Surface defaults
clearly so the user can accept with `y`/`Enter`. Don't ask
philosophical questions — just walk through what's required.

For single-actor offices, suggest the simplest answer:
`actors: [{id: main, kind: internal, label: "Büro", signer: "<name>"}]`;
offer to expand only if the user mentions multiple sub-disciplines or
external partners.

For scope: discover what's available by listing
`<repo>/extensions/domain/*/` and `<repo>/extensions/state/*/`.
Skip empty placeholder dirs (those with only `.gitkeep`).

For integrations: ask which external systems the office actually
uses; only declare those. Don't fill in `adapter: none` placeholders
— omit the class entirely.

## Output

A summary block at the end:

```
Office configured at: <config-path>
Office state at: <roots.state>
References corpus at: <roots.references>
Projects root at: <roots.projects>

Scope:
  Domains: PV-FFA, Wind, Naturschutz
  States: MV

Actors:
  internal: main (Planungsbüro Schulz, signer: G. Schulz)
  external: hendrik (deroekologe), …

Reference manifests in scope (auto-discovered, in load order):
  universal: <repo>/extensions/universal/references-manifest.yaml
  domain/PV-FFA: <repo>/extensions/domain/PV-FFA/references-manifest.yaml
  domain/Wind: <repo>/extensions/domain/Wind/references-manifest.yaml
  domain/Naturschutz: <repo>/extensions/domain/Naturschutz/references-manifest.yaml
  state/MV: <repo>/extensions/state/MV/references-manifest.yaml

Integrations:
  email: thunderbird-maildir → ~/.thunderbird/<profile>/
  scanner: hot-folder → ~/Documents/Scans/
  (other classes omitted — declare in office-config when needed)

Office style: default + PV-FFA overlay + Wind overlay + Naturschutz overlay
  (customize at <roots.office_style_dir>/office-style.sty and
  office-style.PV-FFA.sty etc.)

Next steps:
  - Run /research-references to fetch your scoped references corpus.
  - Bind your first project: setup_project <name>.
```

## Edge cases

- **Path doesn't exist**: roots.state, roots.references, roots.projects
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
- **roots.state coincides with roots.projects**: allowed, warn.
- **office_extensions tree not present even though field set**: the
  loader silently skips missing directories — this is fine for
  initial setup; user adds office-local extensions over time.

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
