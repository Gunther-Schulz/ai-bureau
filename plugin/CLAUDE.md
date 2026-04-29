# pbs-bureau plugin

This file is loaded into context when the `pbs-bureau` plugin is active.

## What this plugin does

Coordinates document work for German planning bureaus (Planungsbüros): drafting, reviewing,
and finalizing B-Plan Begründungen, Textliche Festsetzungen,
Umweltberichte, and various Gutachten. The actual workflow logic lives
in the **orchestrator** skill — see `skills/orchestrator/SKILL.md`.

## System map

- **Plugin** (this directory) — skills (auto-discovered from
  `skills/*/SKILL.md`); `agents/` and `hooks/` deferred to v1+
  per ARCHITECTURE meta-rule 4 (execution-determinism;
  "hooks deferred until concrete need").
- **Backend** (`<repo>/backend/`) — single Python MCP server holding
  LanceDB (vector store), an in-process embedder (fastembed +
  `BAAI/bge-m3`), and a LaTeX compile wrapper. No Docker, no separate
  services. Spawned by Claude Code per session via stdio MCP.
- **Cross-cutting memory** (`<repo>/memory/`) — layered along the
  orthogonal scope axes (universal × domain × state) per
  ARCHITECTURE meta-rule 3. Reference content under
  `memory/universal/{style,conventions,verfahren,...}/`; bausteine
  under `memory/bausteine/{universal,domain/<X>,state/<X>}/`. NOT
  part of the plugin distribution; lives in the user's checkout.
- **Per-project memory** (`<project>/_ai/` or `<project>/.ai/`) — state,
  decisions, file-map, snapshots. Lives WITH each project at the
  configured `paths.projects_root` location. Created on first bind.

## When this plugin activates

- Auto-load: orchestrator skill auto-activates whenever any session
  references planning-bureau work (project under
  `office_config.roots.projects` or
  `office_config.roots.local_repos`, or German planning
  terminology in user input).
- Specialist skills (`draft-textteil-b`, `review-draft`,
  `save-baustein`, etc.) load when their context matches.
- `setup-office` runs first if `office-config.yaml` is missing.

## What goes WHERE

- **Skills** in `skills/<name>/SKILL.md` — orchestrator + specialists,
  conversational logic. Detailed protocols / specs / format references
  live in `skills/<name>/references/<file>.md` (part of the Skill
  Bundle per ARCHITECTURE.md). Idioms for writing skills live in
  `<repo>/docs/plugin-conventions.md`.
- **Agents** (deferred to v1+): planned home is
  `plugin/agents/<name>.md`. Empty until first concrete need.
- **Hooks** (deferred to v1+ per meta-rule 4): planned home is
  `plugin/hooks/hooks.json`. Empty until event-driven automation
  proves necessary; static path-blocks go through
  `settings.json` permissions instead.
- **Memory bausteine, style-spec, korrektur-rules** — at repo level
  under `<repo>/memory/`, NOT here.
- **MCP server (Python, stdio)** — at repo level under `<repo>/backend/`,
  NOT here. Conventions for backend code live in
  `<repo>/docs/backend-conventions.md`.

## Meta-rule 4 (execution-determinism) summary

Skills declare their MCP-tool dependencies in YAML frontmatter:
`mcp_tools_required[]`, `mcp_tools_optional[]`,
`fallback_when_mcp_absent`. The orchestrator + `list_skills` MCP
tool read these to plan tool calls. Deterministic logic lives in
MCP gates (validation, dedupe, etc.); skills compose, never
re-implement. See ARCHITECTURE.md meta-rule 4 for the full rule.

## Versioning

Two semver tracks, separately maintained:

**Per-skill semver** in each `SKILL.md` frontmatter `version:` field:

- Skill behavior changes (including changes to load-bearing
  frontmatter that orchestrator/list_skills consume — e.g. adding
  `mcp_tools_required[]`) → **minor** bump
- Wording / typo / formatting fixes → **patch** bump
- Breaking changes to a skill's external contract (renamed,
  trigger-phrase semantics changed) → **major** bump

**Plugin-wide semver** in `plugin.json`:

- New skill added, skill removed, MCP wiring changed, manifest
  layout change → **minor** bump
- Documentation / README polish → **patch** bump
- Breaking changes (plugin manifest format, plugin name change) →
  **major** bump

The two tracks are decoupled: a single skill can rev to 0.3.0
without touching `plugin.json`'s `0.1.0`.
