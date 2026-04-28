---
name: save-baustein
description: This skill should be used when the user authorizes capturing a reusable text, argumentation pattern, technical specification, or citation as a baustein in memory. Triggered by the orchestrator's four-way decision menu when "capture-now" is chosen, or by direct user phrases like "save this as a baustein", "speichere das", "merken für später", "capture", "festhalten als baustein".
version: 0.1.0
license: MIT
---

# save-baustein

Specialist skill for writing bausteine (reusable knowledge modules)
to memory in the canonical format.

## Load this now

Read `references/format.md` for the full baustein format
specification — frontmatter schema, body structure, lifecycle field
rules, and concrete examples.

## When invoked

By orchestrator after a "capture-now" decision in the four-way menu,
or by direct user request. Inputs needed:

- **Content** — what to save (text, argumentation, spec, citation, textbaustein, template).
- **Type** — one of: `argumentation`, `technical-spec`, `citation`, `checklist`, `textbaustein`, `template`.
- **Scope** — `global`, `domain`, or `project`. If unclear, propose based on heuristics:
  - Office identity / signatures / language conv. → `global`
  - Reusable across projects in same domain → `domain`
  - Single-project fact → `project`
- **Domain** (required if scope=domain) — `artenschutz`, `b-plan`, `umweltbericht`, `common`, etc.
- **Project** (required if scope=project) — project ID matching state.md.
- **Title** — human-readable title (≠ filename).
- **References** — list of `{law, paragraph, cited_form?}` entries the baustein depends on. Surgical hook for research-references downstream.

If any required field is missing, ask the user for it before
proceeding. Don't write incomplete bausteine.

## Behavior

1. **Determine path** per `references/format.md` location rules:
   - `global` → `<repo>/memory/global/<name>.md`
   - `domain` → `<repo>/memory/<domain>/<name>.md`
   - `project` → `<project-root>/_ai/bausteine/<name>.md`

2. **Validate name uniqueness** within the scope. If a baustein with
   the same name already exists:
   - Surface the existing one to the user.
   - Ask: replace, supersede (archive old, write new), or rename?
   - Never silently overwrite.

3. **Compose frontmatter** with all required fields populated.
   Defaults applied:
   - `status: active`
   - `last_validated: <today>`
   - `review_due: <today + 1 year>`
   - `use_count: 0`
   - `last_used: null`
   - `successful_uses: []`
   - `rejected_uses: []`
   - `flagged_reason: null`
   - `superseded_by: null`

4. **Compose body** with required sections:
   - `# Title`
   - `## When to use` — concrete trigger conditions (mandatory)
   - `## Content` — the reusable material (mandatory)
   - `## Notes / caveats` — limitations (recommended)
   - `## History` — first entry: today's date + capture event

5. **Write to disk** at the determined path.

6. **Update scope's INDEX.md** — append a row with `name | type | tags | path`. Create INDEX.md if it doesn't exist.

7. **Confirm to user** in one line: "Saved: `<path>` (scope=<scope>, type=<type>)."

## Output

The user sees a single confirmation line plus a one-sentence summary
of what was captured. No verbose narration.

## Edge cases

- **Scope can't be determined**: propose `domain` with most likely
  domain inferred from content tags; ask user to confirm.
- **References block empty**: warn that staleness machinery won't
  catch updates affecting this baustein. Save anyway if user
  explicitly authorized.
- **User wants to capture as multiple types**: propose splitting into
  multiple bausteine (one per type). Don't write one baustein with
  conflated types.

## Tools used (when MCP backend lands)

- `save_baustein(scope, name, content, source_project, type, references[])` — primary write.
- `list_bausteine(scope, domain?)` — collision check.

Until backend lands: direct filesystem `Write` + `Edit` on INDEX.md,
following the same protocol.
