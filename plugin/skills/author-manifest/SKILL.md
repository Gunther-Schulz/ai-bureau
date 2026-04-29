---
name: author-manifest
description: This skill should be used to author a brand-new manifest in the layered extensions tree — when a domain doesn't yet have content (e.g. first office deploys with Hochwasserschutz domain) or a Bundesland's manifest is still placeholder-only. Triggered by phrases like "create a new domain manifest", "scaffold Hochwasserschutz domain", "author manifest for BB", "neue Domain anlegen", "Manifest für SH erstellen". Distinct from research-references — this skill creates the file structure, research-references populates entries afterwards.
version: 0.2.0
license: MIT
mcp_tools_required: []
mcp_tools_optional: []
fallback_when_mcp_absent: "skill is filesystem-only (Glob/Read/Write/Edit/Bash + office_config.load() Python helper); no MCP dependencies."
---

# author-manifest

Authoring skill for new layered manifests. Creates the file structure
and a populated skeleton; downstream skills (`research-references`)
fill in entries.

## When invoked

Three modes — picked by parameters:

- **New domain manifest**: user wants to add a new planning domain
  (e.g. `Hochwasserschutz`, `Stadtsanierung`, `Verkehrsplanung`)
  and needs the manifest skeleton at
  `extensions/domain/<X>/references-manifest.yaml` (and optionally
  `doctypes.yaml`).
- **New state manifest**: user works in a Bundesland not yet
  populated (e.g. `BB`, `SH`, `BW`) and needs a state manifest
  skeleton at `extensions/state/<X>/<...>.yaml`.
- **New manifest type within existing layer**: e.g. existing
  domain has `references-manifest.yaml` but user wants to add a
  `doctypes.yaml` for it.

Trigger detection: phrases like
- "create a new domain manifest"
- "scaffold <DomainName> domain"
- "author manifest for <STATE>"
- "neue Domain anlegen"
- "Manifest für <STATE> erstellen"

## Parameters (collected interactively if not provided)

| Parameter | Values | Notes |
|---|---|---|
| `layer` | universal \| domain \| state | which axis of the orthogonal scope |
| `key` | name (for domain) or 2-letter code (for state) | null for universal |
| `manifest_type` | references \| doctypes \| both | what to scaffold |
| `seed_categories` | list | which categories to pre-stub (default: all standard) |

## Behavior

1. **Resolve target paths**:
   - References manifest: `<repo>/extensions/<layer>/<key>/references-manifest.yaml`
   - Doctypes manifest: `<repo>/extensions/<layer>/<key>/doctypes.yaml`
   - For `layer == universal`, key is empty: paths are
     `<repo>/extensions/universal/...`

2. **Check for collisions**: if the file already exists, ask the
   user — `overwrite | edit existing | abort`. Default: abort.

3. **Build the skeleton YAML** with proper top-level fields:

   For references-manifest:
   ```yaml
   version: 1
   scope: <layer>
   scope_key: <key>          # null for universal
   last_updated: <today>
   maintainer: <user-name from git config or office>

   # <Header comment per template — see references/templates/>

   categories:
     gesetze:
       <jurisdiction>: []     # bund | eu | <state-code>
     leitfaeden: []
     urteile: []
     beispiele: []
     methodik: []
   ```

   For doctypes manifest:
   ```yaml
   version: 1
   scope: <layer>
   scope_key: <key>
   last_updated: <today>

   doctypes: {}
   ```

4. **Add header comment** appropriate to the layer:
   - Universal: "applies to every German Planungsbüro deploying this app"
   - Domain: "applies when scope.domains contains <key>"
   - State: "applies when scope.states contains <key>; layered on top
     of universal-core for projects in this Bundesland"

5. **Write file(s)**.

6. **Remove `.gitkeep`** if present in the target dir (no longer
   needed once real manifest content lands).

7. **Update office-config**: if the user wants to immediately add
   this manifest to their scope, propose the edit:
   - Add `<key>` to `scope.{domains|states}` if not already there.
   - Add `<layer>.<key>: <path>` to
     `extensions.{references|doctypes}_manifests.<layer>`.
   - Re-validate office-config via `office_config.load()`.

8. **Suggest next steps**:
   - "Run `research-references` and add entries via its new-entry
     mode to populate <key>'s manifest."
   - For domain manifests: "Consider also creating a domain
     office-style overlay at
     `plugin/templates/office-style/office-style.<key>.sty`."

## Edge cases

- **Layer `universal` already exists**: there's only one universal
  manifest per type. Refuse to author a second; redirect to
  `research-references` new-entry mode if user wants to add entries.
- **Key contains invalid characters**: validate against pattern
  `[A-Za-z0-9-_]+` for domains, `^(BB|BW|BY|BE|HB|HH|HE|MV|NI|NW|RP|SH|SL|SN|ST|TH)$`
  for states. Reject + ask again.
- **Scope changes office-config but office-config is owned by
  user**: write proposed edit to a temp file or stdout and ask user
  to approve before applying.
- **User wants doctypes-only without references-manifest**: allowed.
  Some domains may have doctypes that don't need their own legal
  references (rare).

## What this skill is NOT

- NOT for adding individual entries to an existing manifest. Use
  `research-references` new-entry mode for that.
- NOT for updating existing manifests' entries. Use
  `research-references` full-/targeted-refresh modes.
- NOT for deleting manifests. Manual operation; the skill won't
  destroy file content.

## Tools used

- `Glob` to check for existing manifest files at target paths.
- `Bash` for `mkdir -p` if intermediate dirs missing.
- `Write` for the new YAML files.
- `Read` + `Edit` for office-config update (when user opts in).
- `office_config.load()` for re-validation.
- Hands off to `research-references` to populate.
