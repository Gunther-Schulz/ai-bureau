---
name: orchestrator
description: This skill should be used when the user works on Planungsbüro (German planning bureau) documents — any path under the office's configured projects_root or local LaTeX repos directory, mentions of B-Plan, Bebauungsplan, Begründung, Festsetzungen, Umweltbericht, Artenschutz, FFH-Vorprüfung, Stellungnahme, Abwägung, Gutachten, TöB, ZAV, or related German planning terminology, project work matching the office's project-naming convention (e.g. "YY-NN <Client> - <Location>"), or any reference to the office's configured project folders. Auto-loads at session start when planning-bureau context is detected. Coordinates the entire conversational flow for all office document work.
version: 0.1.0
license: MIT
---

# Bureau orchestrator

Master skill for Planungsbüro document workflows. Coordinates
drafting, review, and finalization across all configured doctypes.
The framework is operational, not advisory — every session in this
plugin runs through it.

## Load this now

Read `PROCEDURE.md` from this skill's directory. Follow it.

While operating, hold these references loaded as authoritative ground
truth:

- `<repo>/memory/universal/style/style-spec.md` — universal structural
  domain for B-Plan LaTeX (KOMA scrreprt, ngerman babel, German
  number conventions, Roman/Arabic numbering, Projektdaten macro
  framework). Office-specific styling lives in the office's
  `office-style.sty` (loaded by the compile pipeline, not by this
  skill).
- `<repo>/memory/universal/conventions/korrektur-rules.md` — German
  writing conventions (German quotes `\glqq…\grqq{}`, non-breaking
  spaces before §/units/dates, German number formatting, hyphenation
  hints, source line wrap).
- `<repo>/memory/universal/doctypes.yaml` — registry of supported
  doctypes, master file conventions, ownership rules.

Resolve `<repo>` to the plugin's repo root. From inside the plugin,
that is two directories up from this SKILL.md.

## System map

Four layers:

| Layer | Where | Purpose |
|---|---|---|
| Plugin | `<repo>/plugin/` | Skills (this one + specialists), agents, hooks |
| Backend | `<repo>/backend/` | MCP server (Python, stdio) — embedded LanceDB + in-process embedder + reranker |
| Cross-cutting memory | `<repo>/memory/` | global / domain bausteine, specs, registry |
| Per-project memory | `<project-root>/_ai/` or `.ai/` | state, file-map, decisions, snapshots |

Project artifacts and office state live under user-owned roots
configured per deployment in `office-config.yaml`:

- **Projects root** (`paths.projects_root`) — where client project
  folders live. Resolve at runtime via the `list_projects` /
  `bind_project` MCP tools, never hardcode.
- **Office state root** (`paths.state_root`) — projects-index,
  pending-actions, recent-correspondence, office templates, AI
  references corpus.
- **Local LaTeX repos root** (`paths.local_repos_root`, optional) —
  set if the office keeps per-doctype LaTeX repos separate from the
  project folder.

If the user works on a project, get its root path from
`bind_project`'s result or from `_ai/state.md.project_root`. Do not
infer paths from convention.

## Specialist skills

The orchestrator routes to specialist skills rather than drafting,
reviewing, or finalizing directly. When a routing target does not
yet exist as its own skill, perform the work inline AND log a T6
(capability gap) trigger.

- `setup-office` — first-time deployment wizard (creates
  office-config.yaml, bootstraps state directories)
- `setup_project` — create / initialize / bind a project (called via
  the MCP tool of the same name)
- `draft-textteil-b` — draft a Begründung from project sources
- `draft-textteil-c` — draft Textliche Festsetzungen (Teil B Text)
- `review-draft` — layered review of an existing draft
- `save-baustein` — capture a reusable text or argument to memory
- `promote-to-skill` — promote a frequently-used baustein to a skill
- `validate-latex-style` — diff a doc against `style-spec.md` + the
  office's `office-style.sty`
- `validate-checklist` — run doctype-specific required-section checks
- `verify-citations` — cross-check legal references against the RAG
- `draft-cover-mail` — draft transmittal mails to authorities
- `survey-project` — first-bind clustering of project files into a
  `_ai/file-map.md`
- `research-references` — fetch / refresh legal references corpus

## What this skill is and is not

- **Is:** the always-on operational framework for any session under
  this plugin.
- **Is:** workflow-and-judgment hybrid — phases with gates, plus
  watch-list classification that surfaces decisions for the user.
- **Is not:** a drafting skill. Delegate to a specialist or perform
  inline; never bypass the framework.
- **Is not:** project-specific. Every project goes through the same
  framework with project-specific details loaded from per-project
  state.
- **Is not:** office-specific. The framework is identical across
  deployments; office values come from `office-config.yaml`.

## When to bypass

Never. Loaded means active. If a request is plainly unrelated to
planning-bureau work (e.g., user asks an unrelated coding question
with no domain context), this skill does not apply and `PROCEDURE.md`
need not be consulted. Detect non-domain context from the absence of
trigger phrases and project paths.

## When office-config is missing

If `office_config.load()` raises `OfficeConfigNotFoundError`, route
the user immediately to the `setup-office` skill before doing any
other work. The framework cannot operate without a configured office.
