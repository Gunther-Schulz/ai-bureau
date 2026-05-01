---
name: orchestrator
description: This skill should be used when the user works on Planungsbüro (German planning bureau) documents — any path under the office's configured projects_root or local LaTeX repos directory, mentions of B-Plan, Bebauungsplan, Begründung, Festsetzungen, Umweltbericht, Artenschutz, FFH-Vorprüfung, Stellungnahme, Abwägung, Gutachten, TöB, ZAV, or related German planning terminology, project work matching the office's project-naming convention (e.g. "YY-NN <Client> - <Location>"), or any reference to the office's configured project folders. Auto-loads at session start when planning-bureau context is detected. Coordinates the entire conversational flow for all office document work.
version: 0.10.0
license: MIT
mcp_tools_required: [list_projects, list_skills, get_project_state, update_project_state]
mcp_tools_optional: [list_reference_manifests, list_doctypes_manifests, list_skeletons, list_bausteine, search_corpus, read_corpus_file, find_bausteine_by_reference, bind_project, setup_project]
fallback_when_mcp_absent: "warn user and suggest backend restart. Without get/update_project_state, orchestrator cannot read or transition project lifecycle (state.md is a strict-validated contract — no direct skill Read/Write per ARCHITECTURE meta-rule 4). Other capabilities (project enumeration, watch-list cross-references) degrade to filesystem reads."
summary: Master coordination skill — routes user input + holds workflow gates. Auto-loads when in planning-bureau scope; specialists own their own invariants. Watch-list logic delegated to `watch-list` skill (post-v0.5 split per design-review S3).
routing_mode: always_active
triggers:
  - auto-loaded on planning-bureau context        # meta — not user-typed
handoffs: [setup-office, draft-textteil-b, draft-textteil-c, review-draft, save-baustein, validate-bausteine, record-feedback, promote-to-skill, validate-latex-style, validate-checklist, verify-citations, draft-cover-mail, research-references, author-manifest, survey-project, audit, design-review, watch-list]
phase_role: routing
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
- **Doctypes registry** — call `list_doctypes_manifests()` (MCP
  tool) to enumerate the layered doctype set: universal layer plus
  per-active-domain overlays from `extensions/{universal,domain/<X>}/
  doctypes.yaml`. Do not reference the legacy
  `memory/universal/doctypes.yaml` path — registries moved to
  `extensions/` (Configuration entity per ARCHITECTURE.md) post-orthogonality
  refactor.

Resolve `<repo>` to the plugin's repo root. From inside the plugin,
that is two directories up from this SKILL.md.

## System map

Four layers:

| Layer | Where | Purpose |
|---|---|---|
| Plugin | `<repo>/plugin/` | Skills (this one + specialists), agents, hooks |
| Backend | `<repo>/backend/` | MCP server (Python, stdio) — embedded LanceDB + in-process embedder + reranker |
| Cross-cutting memory | `<repo>/memory/` | layered bausteine (universal / domain / state) + specs + reference content |
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
`bind_project`'s result or from `get_project_state(project).state.project_root`.
Do not infer paths from convention. Direct Read/Write of state.md is a
meta-rule 4 persistence-boundary leak — always route through the MCP gate.

## Specialist skills

The orchestrator routes to specialist skills rather than drafting,
reviewing, or finalizing directly. When a routing target does not
yet exist as its own skill, perform the work inline AND log a T6
(capability gap) trigger.

For canonical, queryable inventory: call `list_skills()` (MCP tool)
— returns every skill's `name`, `description`, `version`, and
declared `mcp_tools_required[]`. This list below is for at-glance
reference; the MCP tool is authoritative.

- `setup-office` — first-time deployment wizard (creates
  office-config.yaml, bootstraps state directories, walks
  scope multi-select for domains + states)
- `setup_project` — create / initialize / bind a project (called
  via the MCP tool of the same name)
- `survey-project` — first-bind clustering of project files into
  a `_ai/file-map.md`
- `draft-textteil-b` — draft a Begründung from project sources
- `draft-textteil-c` — draft Textliche Festsetzungen (Teil B Text)
- `review-draft` — layered review of an existing draft
- `save-baustein` — capture a reusable text or argument to memory
  (validated via `save_baustein` MCP gate per meta-rule 4)
- `validate-bausteine` — periodic freshness sweep of saved
  bausteine; surfaces stale / flagged / review_due candidates
- `record-feedback` — capture external feedback (UNB Stellungnahmen,
  approvals, rejections); side-effects on addressed bausteine
- `promote-to-skill` — promote a frequently-used baustein to a
  skill (orchestrator guard 6.4: source project must be finalized)
- `validate-latex-style` — diff a doc against `style-spec.md` +
  the office's `office-style.sty` (+ per-active-domain overlays)
- `validate-checklist` — run doctype-specific required-section
  checks; consults layered doctypes manifest via
  `list_doctypes_manifests()`
- `verify-citations` — cross-check legal references against the
  RAG; iterative resolution per priority touchpoint refactor
- `draft-cover-mail` — draft transmittal mails to authorities
- `research-references` — fetch / refresh legal references corpus
  (walks layered manifest set per office's scope)
- `author-manifest` — scaffold new domain or state manifests for
  scopes that don't yet have content
- `audit` — comprehensive drift audit (architecture / plugin /
  backend / docs / cross-references); triggered by phrases like
  "audit", "drift check", "structural sweep", "pre-phase audit"
- `design-review` — first-principles soundness review with
  explicit anti-status-quo bias (greenfield reframe); challenges
  the design itself, not its compliance. Triggered by phrases
  like "design review", "is this design right", "would we build
  this from scratch", "rough cut review"
- `watch-list` — continuous T1-T6 watch-list infrastructure
  (queue + TTL + dedup + decision menu + decay). Mostly delegated
  from this orchestrator during workflow; admin phrases like
  "show watch queue", "watch list status" route directly

## What this skill is and is not

- **Is:** the auto-loaded coordination layer for sessions in
  planning-bureau scope.
- **Is:** workflow-and-judgment hybrid — phases with gates,
  routing to specialists, delegating watch-list infrastructure
  to the `watch-list` skill.
- **Is not:** a drafting skill. Delegate to a specialist or perform
  inline; specialists own their own invariants.
- **Is not:** project-specific. Every project goes through the same
  framework with project-specific details loaded from per-project
  state.
- **Is not:** office-specific. The framework is identical across
  deployments; office values come from `office-config.yaml`.

## When in scope

Auto-loads when the session has planning-bureau context — project
under `office_config.roots.projects` or
`office_config.roots.local_repos`, or German planning terminology
in user input.

When in scope: orchestrator's PROCEDURE applies; specialists are
invoked per their trigger phrases + this orchestrator's routing.

When NOT in scope (user asks an unrelated coding question with no
domain context): this skill does not apply. Other skills in the
session compose normally.

## When office-config is missing

If `office_config.load()` raises `OfficeConfigNotFoundError`, route
the user immediately to the `setup-office` skill before doing any
other work. The framework cannot operate without a configured office.
