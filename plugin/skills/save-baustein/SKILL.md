---
name: save-baustein
description: This skill should be used when the user authorizes capturing a reusable text, argumentation pattern, technical specification, or citation as a baustein in memory. Triggered by the orchestrator's four-way decision menu when "capture-now" is chosen, or by direct user phrases like "save this as a baustein", "speichere das", "merken für später", "capture", "festhalten als baustein".
version: 0.3.0
license: MIT
mcp_tools_required: [save_baustein, list_bausteine]
mcp_tools_optional: [find_bausteine_by_reference]
fallback_when_mcp_absent: "warn user; degrade to filesystem Write of the baustein markdown file at the canonical path per `references/format.md`. Skip dedupe + INDEX.md update."
summary: Captures reusable text, argumentation, technical specs, or citations as bausteine in memory.
routing_mode: direct
triggers:
  - {phrase: "save this as a baustein", lang: en}
  - {phrase: "speichere das", lang: de}
  - {phrase: "merken für später", lang: de}
  - {phrase: "capture", lang: en}
  - {phrase: "festhalten als baustein", lang: de}
handoffs: [promote-to-skill]
phase_role: utility
---

# save-baustein

Specialist skill for writing bausteine (reusable knowledge modules)
to memory in the canonical format. Per ARCHITECTURE.md scope
orthogonality (universal × domain × state) + meta-rule 5 (validation
in MCP gates), all writes go through the `save_baustein` MCP tool —
which validates frontmatter, resolves the layered path, and prevents
silent overwrites.

## Load this now

Read `references/format.md` for the full baustein format
specification — frontmatter schema (including scope orthogonality,
references with `verified_against_version` slots, optional
`cross_project_visible` flag), body structure, lifecycle field
rules, and concrete examples.

## When invoked

By orchestrator after a "capture-now" decision in the four-way menu,
or by direct user request. Inputs needed:

- **Content** — what to save (text, argumentation, spec, citation, textbaustein, template).
- **Type** — one of: `argumentation`, `technical-spec`, `citation`, `checklist`, `textbaustein`, `template`.
- **Scope** (post-orthogonality) — `universal`, `domain`, `state`, or `project`. Heuristics if unclear:
  - Office identity / signatures / language conventions / cross-bureau patterns → `universal`
  - Reusable across projects in a planning domain (e.g. PV-FFA, Wind, Naturschutz) → `domain`
  - State-specific knowledge (LUNG-MV interpretation; OVG-MV ruling application) → `state`
  - Single-project fact (specific UNB contact, project-specific decision) → `project`
- **scope_key** — required for domain/state. The capitalized
  scope key matching the directory under `extensions/` and
  `memory/bausteine/`:
  - For domain: `Naturschutz`, `PV-FFA`, `Wind`, `Innenentwicklung`
  - For state: `MV`, `BB`, `BW`, etc. (ISO Bundesland code)
  - For project: project name (`<YY-NN>-<location-slug>`) or supply `project_root` directly.
- **Title** — human-readable title (≠ filename).
- **References** — list of `{law, paragraph, cited_form?, verified_against_version?}` entries the baustein depends on. Surgical hook for research-references downstream + verify-citations freshness check.
- **cross_project_visible** (optional, project-scope only) — `true` if this baustein, while project-scope, should surface in `list_bausteine` queries from other projects in the same office. Default `false`. Resolves the promote-or-keep-locked binary for mid-stage cross-project bausteine that aren't yet generalizable enough to promote.

If any required field is missing, ask the user for it before
proceeding. Don't write incomplete bausteine.

## Behavior

1. **Dedupe guard** — before writing, check for similar existing
   bausteine in the target scope. Call `list_bausteine(scope=<X>,
   scope_key=<key>)` and surface candidates whose `title` or `tags`
   overlap meaningfully with the new baustein. Future enhancement
   (HyDE-style paraphrase-search via `search_corpus` over
   bausteine) lands when the corpus index includes saved bausteine
   — until then, title + tag match is the practical guard.

   On collision: surface the existing baustein to the user. Ask:
   replace, supersede (archive old, write new with `superseded_by`
   pointer), or rename. Never silently overwrite.

2. **Compose + validate** — the `save_baustein` MCP tool composes
   frontmatter (defaults + provided fields per `references/format.md`)
   and validates the layered path resolution. Defaults applied:
   - `status: active`
   - `last_validated: <today>`
   - `review_due: <today + 1 year>`
   - `use_count: 0`, `last_used: null`
   - `successful_uses: []`, `rejected_uses: []`
   - `flagged_reason: null`, `superseded_by: null`
   - `captured_via: save-baustein-tool` (set by the MCP tool)

3. **Body composition** — required sections:
   - `# Title`
   - `## When to use` — concrete trigger conditions (mandatory)
   - `## Content` — the reusable material (mandatory)
   - `## Notes / caveats` — limitations (recommended)
   - `## History` — first entry: today's date + capture event

4. **Write via MCP tool** — `save_baustein(scope, scope_key,
   project_root?, name, type, title, body, references, tags,
   overwrite=false)`. Tool resolves the path:
   - `universal` → `<repo>/memory/bausteine/universal/<name>.md`
   - `domain` → `<repo>/memory/bausteine/domain/<scope_key>/<name>.md`
   - `state` → `<repo>/memory/bausteine/state/<scope_key>/<name>.md`
   - `project` → `<project_root>/_ai/bausteine/<name>.md`

5. **Update scope's INDEX.md** — append a row with `name | type |
   tags | path`. Create INDEX.md if it doesn't exist. (If the MCP
   backend later moves this into `save_baustein`, the tool handles
   it transactionally; today the skill writes the index entry as
   a follow-up Edit.)

6. **Confirm to user** in one line: `Saved: <path> (scope=<scope>, scope_key=<key>, type=<type>).`

## Output

The user sees a single confirmation line plus a one-sentence summary
of what was captured. No verbose narration.

## Edge cases

- **Scope can't be determined**: propose the most likely scope based
  on tags + content, then ask user to confirm. Default order to
  consider: project (most specific) → state → domain → universal
  (most general). When in doubt, prefer narrower; promotion to
  broader scope happens later if the baustein proves reusable.
- **References block empty**: warn that `verify-citations`
  freshness machinery and `research-references` cross-reference
  flagging won't catch updates affecting this baustein. Save anyway
  if user explicitly authorizes.
- **User wants to capture as multiple types**: propose splitting
  into multiple bausteine (one per type). Don't write one baustein
  with conflated types.
- **Project-scope baustein with `cross_project_visible: true`** —
  acceptable. The flag does not promote the baustein to broader
  scope; it just extends search visibility to other projects in
  the same office. Promotion (project → universal/domain/state)
  remains a separate decision via `promote-to-skill` after the
  source project is `finalized` per orchestrator guard 6.4.

## Tools used

- `save_baustein` (MCP, required) — primary write with full
  validation per meta-rule 5.
- `list_bausteine` (MCP, required) — collision check (dedupe
  guard).
- `find_bausteine_by_reference` (MCP, optional) — cross-reference
  with existing bausteine that share law/ruling/leitfaden citations
  for additional collision detection.

When MCP backend unreachable: fall back to direct `Write` of the
baustein markdown file at the canonical path per
`references/format.md`. Skip dedupe + INDEX update; warn the user
that the system is operating in degraded mode and the baustein
will need re-validation when the backend returns.
