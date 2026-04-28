# pbs-bureau plugin

This file is loaded into context when the `pbs-bureau` plugin is active.

## What this plugin does

Coordinates document work for German planning bureaus (Planungsbüros): drafting, reviewing,
and finalizing B-Plan Begründungen, Textliche Festsetzungen,
Umweltberichte, and various Gutachten. The actual workflow logic lives
in the **orchestrator** skill — see `skills/orchestrator/SKILL.md`.

## System map

- **Plugin** (this directory) — skills + agents + hooks
- **Backend** (`<repo>/backend/`) — single Python MCP server holding
  LanceDB (vector store), an in-process embedder (fastembed +
  `BAAI/bge-m3`), and a LaTeX compile wrapper. No Docker, no separate
  services. Spawned by Claude Code per session via stdio MCP.
- **Cross-cutting memory** (`<repo>/memory/`) — global, domain, and
  office-level memory shared across all projects. NOT part of the plugin
  distribution; lives in the user's checkout of the repo.
- **Per-project memory** (`<project>/_ai/` or `<project>/.ai/`) — state,
  decisions, file-map, snapshots. Lives WITH each project at the
  configured `paths.projects_root` location. Created on first bind.

## When this plugin activates

- Auto-load: orchestrator skill auto-activates whenever any session
  references planning-bureau work (project under
  `office_config.paths.projects_root` or
  `office_config.paths.local_repos_root`, or German planning
  terminology in user input).
- Specialist skills (`draft-textteil-b`, `review-draft`,
  `save-baustein`, etc.) load when their context matches.
- `setup-office` runs first if `office-config.yaml` is missing.

## What goes WHERE

- **Skills** in `skills/<name>/SKILL.md` — orchestrator + specialists,
  conversational logic.
- **Agents** in `agents/<name>.md` — focused subagents for deep passes
  (legal-reviewer, style-auditor — deferred to v1+).
- **Hooks** in `hooks/hooks.json` — only if event-driven automation
  proves necessary; currently none.
- **Memory bausteine, style-spec, korrektur-rules** — at repo level
  under `<repo>/memory/`, NOT here.
- **MCP server (Python, stdio)** — at repo level under `<repo>/backend/`,
  NOT here.

## Versioning

Version in `plugin.json` follows semver. Bump on:
- Skill behavior changes → minor
- Bug fixes / wording → patch
- Breaking changes to MCP tool surface → major
