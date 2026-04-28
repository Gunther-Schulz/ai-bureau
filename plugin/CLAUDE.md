# pbs-bureau plugin

This file is loaded into context when the `pbs-bureau` plugin is active.

## What this plugin does

Coordinates document work for Planungsbüro Schulz: drafting, reviewing,
and finalizing B-Plan Begründungen, Textliche Festsetzungen,
Umweltberichte, and various Gutachten. The actual workflow logic lives
in the **orchestrator** skill — see `skills/orchestrator/SKILL.md`.

## System map

- **Plugin** (this directory) — skills + agents + hooks
- **Backend** (`<repo>/backend/`) — local Docker services and MCP
  server. Provides corpus search (LanceDB), embeddings (Ollama), LaTeX
  compile, project ingestion. Started independently via
  `docker compose up -d` in `<repo>/backend/`.
- **Cross-cutting memory** (`<repo>/memory/`) — global, domain, and
  office-level memory shared across all projects. NOT part of the plugin
  distribution; lives in the user's checkout of the repo.
- **Per-project memory** (`<project>/_ai/` or `<project>/.ai/`) — state,
  decisions, file-map, snapshots. Lives WITH each project at its hidrive
  location. Created on first bind to a project.

## When this plugin activates

- Auto-load: orchestrator skill auto-activates whenever any session
  references PBS work (project at `/mnt/data2t/hidrive/Öffentlich
  Planungsbüro Schulz/Projekte/...`, or local
  `~/dev/Planungsbüro-Schulz/...` repos).
- Specialist skills (`draft-textteil-b`, `review-draft`,
  `save-baustein`, etc.) load when their context matches.

## What goes WHERE

- **Skills** in `skills/<name>/SKILL.md` — orchestrator + specialists,
  conversational logic.
- **Agents** in `agents/<name>.md` — focused subagents for deep passes
  (legal-reviewer, style-auditor — deferred to v1+).
- **Hooks** in `hooks/hooks.json` — only if event-driven automation
  proves necessary; currently none.
- **Memory bausteine, style-spec, korrektur-rules** — at repo level
  under `<repo>/memory/`, NOT here.
- **MCP server, Docker stack** — at repo level under `<repo>/backend/`,
  NOT here.

## Versioning

Version in `plugin.json` follows semver. Bump on:
- Skill behavior changes → minor
- Bug fixes / wording → patch
- Breaking changes to MCP tool surface → major
