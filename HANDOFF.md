# Session handoff — pbs-bureau

This document captures the state of pbs-bureau at end of session
2026-04-28 so the next Claude Code session can pick up cleanly with
fresh context.

**Read order for next session**:
1. This file (HANDOFF.md)
2. `ARCHITECTURE.md` — taxonomy + decision rules
3. `plugin/skills/orchestrator/SKILL.md` + `PROCEDURE.md` — framework
4. Whichever skill is next on the build list

---

## What pbs-bureau is

A Claude Code plugin + local Python MCP backend for drafting,
reviewing, and finalizing planning documents for Planungsbüro Schulz
(PBS). Doctypes: B-Plan Begründung, B-Plan Textliche Festsetzungen,
Umweltbericht, Artenschutzbewertung, Gutachten variants. Uses local
RAG (LanceDB + sentence-transformers + bge-m3 + bge-reranker-v2-m3),
no Docker, no external API.

Project root: `/home/g/dev/Gunther-Schulz/pbs-bureau/`
GitHub: <https://github.com/Gunther-Schulz/pbs-bureau> (private)

---

## Status snapshot (what's done, what's not)

### ✅ Completed in this session

- **Repo + GitHub remote** with marketplace + plugin manifest layout
  matching the user's other plugins (bildhauer, clippy, skill-craft).
- **Plugin scaffolding** — `plugin/.claude-plugin/plugin.json`,
  `plugin/CLAUDE.md`, `.claude-plugin/marketplace.json`.
- **Symlink-based dev install** — `dev-link.sh` symlinks
  `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` to repo's `plugin/`.
  Settings in `dotfiles/claude/settings.json` register marketplace +
  enable plugin. Updates to plugin files are picked up by
  `/reload-plugins` without reinstall.
- **Hooks updated** — `restrict-bash-paths.py` (rewrote in Python
  with `shlex` for quoting + Unicode handling), added
  `restrict-file-paths.py` for Read/Edit/Write/Glob/Grep/NotebookEdit
  with same allowlist. Hidrive path
  `/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/...`
  whitelisted.
- **Backend Python project scaffolded** at `backend/mcp-server/` —
  `pyproject.toml`, `uv.lock`, `.python-version` (3.13),
  `src/pbs_mcp/__init__.py`, `server.py` (stdio MCP entry),
  `config.py` (path resolution). Deps installed via `uv sync`. Server
  imports cleanly; `list_tools` returns `[]` (no tools wired yet).
- **ARCHITECTURE.md** at repo root — 6 entity types + 5 decision
  rules for placement.
- **Memory reference content** in `memory/domain/`:
  - `style/style-spec.md` — both LaTeX doctypes (Begründung scrreprt,
    Festsetzungen article) with exact preamble specs, drawn from
    canonical local repos (`~/dev/Planungsbüro-Schulz/22-16-Maxsolar-
    --Friedrichshof---*`).
  - `conventions/korrektur-rules.md` — distilled from legacy
    korrektur-prompt.txt (German quotes, non-breaking spaces, German
    number format, hyphenation, source line wrap, lists).
  - `project-structure.md` — clean AI-native folder layout for new
    projects (`.ai/` hidden, `inputs/` subdivided by source, doctype
    subfolders, `Schriftverkehr/`, `TöB/`, `Auslieferung/`).
  - `doctypes.yaml` — registry of doctypes with status (active,
    deferred), template paths, master file conventions.
  - `verfahren/bauleitplanung-phasen.md` — 13-phase Regelverfahren +
    §13/§13a/§13b variants + §12 vorhabensbezogen, drawn from local
    BauGB.txt + Friedrichshof Festsetzungen Verfahrensvermerke.
- **Skill references** in `plugin/skills/<skill>/references/`:
  - `save-baustein/references/format.md` — baustein file format spec
  - `record-feedback/references/format.md` — feedback entry format
  - `research-references/references/manifest-schema.md` — manifest
    schema
  - `validate-checklist/references/checklists/{4 files}` — per-doctype
    structural checklists (b-plan-begruendung, b-plan-festsetzungen,
    umweltbericht, gutachten-generic)
  - `orchestrator/references/state-format.md` — `_ai/state.md`
    format including `doctype_status` field for per-project scope
- **Backend docs** in `backend/mcp-server/docs/`:
  - `vector-metadata-schema.md` — LanceDB columns + filter patterns
  - `chunking-strategy.md` — per-source-type chunker registry
- **All 14 specialist skill specs**:
  1. **orchestrator** (master, SKILL.md + PROCEDURE.md, references/
     state-format.md) — three-scope framework, watch list, four-way
     menu, hard gates, hard guards, validation, specialist routing
  2. **draft-textteil-b** (heavy, SKILL.md + PROCEDURE.md) — Phase A
     entry for Begründung
  3. **draft-textteil-c** (heavy, SKILL.md + PROCEDURE.md) — Phase A
     entry for Festsetzungen
  4. **review-draft** (heavy, SKILL.md + PROCEDURE.md) — Phase B
     layered review
  5. **save-baustein** (light, references/format.md) — capture
  6. **record-feedback** (light, references/format.md) — feedback
  7. **research-references** (light, references/manifest-schema.md) —
     legal corpus maintenance
  8. **validate-checklist** (light, references/checklists/) —
     Layer 1 structural
  9. **validate-latex-style** (light) — Layer 3 formal style
  10. **verify-citations** (light) — citation freshness
  11. **draft-cover-mail** (light) — transmittal mails
  12. **survey-project** (light) — first-bind clustering
  13. **promote-to-skill** (light) — memory→skill graduation
  14. **validate-bausteine** (light) — freshness sweep

### ⏳ Designed, decided, NOT yet built

- **Backend implementation** — Python source for the MCP tools. The
  scaffold exists (server runs, list_tools returns empty); each tool
  needs implementation:
  - Embedder wrapper (`embedder.py`) — sentence-transformers + bge-m3
    + bge-reranker-v2-m3, GPU when 5090 available
  - LanceDB wrapper (`db.py`) — table schema per
    `vector-metadata-schema.md`, hybrid search + reranker pipeline
  - Tools (`tools/`):
    - `corpus.py` — search_corpus, read_corpus_file
    - `ingest.py` — ingest_paths, ingest_project_inputs, search_inputs
    - `memory.py` — list_bausteine, get_baustein, save_baustein,
      flag_baustein, archive_baustein, find_bausteine_by_reference
    - `projects.py` — list_projects, bind_project, unbind_project,
      survey_project (lightweight; full survey is in skill)
    - `build.py` — compile_latex (latexmk wrapper),
      scaffold_project (template tree copy + git init for Overleaf)
  - Per-source chunkers per `chunking-strategy.md`
  - Schema register for tool I/O Pydantic models
  - Update `server.py` to import tools and wire them into
    `list_tools()` + per-tool handlers

- **`references-manifest.yaml`** at repo root — populate Tier 1
  entries (~22 docs):
  - **Federal**: BauGB, BauNVO, BNatSchG, EEG, BImSchG, UVPG, PlanZV, ROG
  - **EU**: FFH-RL (92/43/EWG), Vogelschutz-RL (2009/147/EG)
  - **M-V**: LPlG-MV, LBauO-MV, NatSchAG-MV, KV-MV
  - **Leitfäden**: KNE-PV-Naturschutz (have), KNE-Anlagengestaltung
    (have), KNE-Standortsteuerung (have), KNE-Landschaftsbild (have),
    KNE-Folgenutzung-Acker-Gruenland (have), LUNG-MV-
    Artenschutzleitfaden (need), Verfahrenserlass-Bauleitplanung-MV
    (need), Brandschutzkonzept-Leitfaden-PV-MV (need; verify exists)
  - **Urteile**: BVerwG-9-A-3-06, BVerwG-9-A-14-07, BVerwG-9-A-39-07
    (Freiberg), BVerwG-9-A-22-11 (§45 Nr.5), EuGH-C-127-02
    (Waddenzee), EuGH-C-258-11 (Sweetman)
  - **Methodik (cite-only)**: Suedbeck-2005-Brutvoegel,
    Dietz-Kiefer-2014-Fledermaeuse

- **Reference fetch + initial ingest** — once backend tools online:
  1. Run `research-references` skill to fetch all manifest entries
     into `<hidrive>/_ai-references/`.
  2. Run `ingest_paths` to embed references + the 4 local
     Planungsbüro-Schulz repos + the 16 hidrive project folders into
     LanceDB.

- **Office state seeding** — `<hidrive>/_ai-office-state/`:
  - `projects-index.md` — registry of 16 hidrive projects (name,
    path, last-modified, lifecycle=unknown for now)
  - `pending-actions.md` — empty template
  - `recent-correspondence.md` — empty template

- **Office identity config** — `memory/global/identity.md` (or
  `memory/office/identity.md` per future refactor) — PBS-specific:
  Schwerin office address, signature, contact, language convention.

### ❌ NOT designed yet (deferred backlog)

These are explicitly deferred. Not blocking; pick up later when need
arises.

- **Email integration** — Thunderbird mbox reader to populate
  `Schriftverkehr/eml/` automatically. v1 has manual `.eml` drop.
  Roadmap: parse local maildir, filter by domain whitelist, route
  to project correspondence/.
- **Phone call note format** — small markdown spec for
  `Schriftverkehr/telefonnotizen/<date>-<party>.md`.
- **Maps/GIS integration** — gis-utils MCP coexistence with
  pbs-bureau MCP for joint Schulz+Hendrik projects.
- **Overleaf sync workflow detail** — git init per LaTeX subfolder
  is decided; the actual GitHub-remote-creation + branch protection
  + push-on-save details are TBD.
- **Reference versioning** — keep history vs overwrite when laws
  amend. Initial decision: archive old per `archive_versions: true`,
  keep N=5. Refine with use.
- **Reference internal cross-refs** — §44 BNatSchG mentions §1; how
  do we resolve that during retrieval? Probably handled by reranker;
  test with real queries first.
- **Subagents** — legal-reviewer, style-auditor agents (separate
  Claude instances spawned for deep passes). v1+, when context
  pressure justifies.
- **Umweltprüfung verfahren reference** — separate
  `memory/domain/verfahren/umweltpruefung.md` with §2 Abs.4 BauGB
  + Anlage 1 detail.
- **FFH-Vorprüfung verfahren reference** — `ffh-vorpruefung.md`,
  §34 BNatSchG + Erheblichkeitsabschätzung detail.
- **Abwägung mechanism + doctype** — per-Stellungnahme structure:
  quote → analyze → Abwägungsergebnis. Add to doctypes.yaml.
- **Artenschutz / SPA verfahren reference** — Hendrik's domain;
  joint projects need it.
- **Hooks / event triggers** — currently none in v1. Possibly add
  state-transition hooks, snapshot-on-send hooks later.

---

## Key architectural decisions made (with reasoning)

| Decision | Reasoning |
|---|---|
| **Python backend, no Docker** | One Python process holds LanceDB + embedder + LaTeX wrapper. Fewer moving parts. fastembed considered but switched to sentence-transformers for GPU + reranker support. |
| **bge-m3 + bge-reranker-v2-m3** | Best open multilingual quality for German legal text. User has 5090, GPU acceleration trivial. Reranker promoted from v0.2 to v1 because cost is near-zero on 5090. |
| **LanceDB (single table)** | Embedded, hybrid search native, namespace by metadata not separate tables. Simpler than Qdrant or Chroma for solo use. |
| **No /commands** | Conversational interface only. User explicitly rejected commands as too rigid. |
| **No modes / mode-switching** | Three scopes (office, project, product) operate contextually based on conversation, not toggled. |
| **Four-way decision menu** | capture-now / handle-now / backlog / drop. Central conversational pattern when orchestrator surfaces something. |
| **Symlink dev install** | Eliminates reinstall friction during heavy iteration. `dev-link.sh` does it. |
| **Memory taxonomy locked** | 6 entity types, 5 decision rules. See `ARCHITECTURE.md`. Format specs went to skill references; cross-cutting reference content stays in memory/domain. |
| **AI-owned new projects** | Full project-folder ownership; `.ai/` hidden meta-state. Existing projects use `_ai/` (visible) with `ownership_mode: migrate | new-work-only | quarantine`. |
| **Per-project LaTeX folders are separate git repos** | For Overleaf sync. The wider project root is hidrive-synced, not git-tracked. |
| **AI-owned references separate from human Literatur/** | `<hidrive>/_ai-references/` for fetched legal corpus; `<hidrive>/Projekte/Literatur/` stays as human-curated. |
| **Office state on hidrive, not in repo** | `<hidrive>/_ai-office-state/` for projects-index, pending-actions, recent-correspondence. Repo holds the assistant; hidrive holds the office's data. |

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/` | Claude Code plugin |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/` | Cross-cutting memory (reference content) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/backend/mcp-server/` | Python MCP backend |
| `/home/g/dev/Gunther-Schulz/Planungsbüro-Schulz/` | Local per-doctype git working copies (canonical LaTeX templates) |
| `/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte/` | All client projects (16+) |
| `/mnt/data2t/hidrive/.../Projekte/_ai-references/` | AI-owned legal references (to be created) |
| `/mnt/data2t/hidrive/.../Projekte/_ai-office-state/` | Office runtime state (to be created) |
| `/mnt/data2t/hidrive/.../Projekte/Literatur/` | Human-curated reference docs (existing) |
| `/mnt/data2t/hidrive/.../Projekte/<YY-NN ...>/_ai/` | Per-project state (created on first bind) |

---

## What the next session should do FIRST

**Pick up at backend implementation.**

1. Read this file (HANDOFF.md), `ARCHITECTURE.md`, and
   `plugin/skills/orchestrator/SKILL.md` for context.
2. `cd backend/mcp-server` and verify the scaffold:
   - `uv sync` (re-resolve deps if needed)
   - `uv run python -c "from pbs_mcp.server import server; print('ok')"`
3. **Implement embedder + db**:
   - `src/pbs_mcp/embedder.py` — sentence-transformers wrapper
     (model: BAAI/bge-m3, with GPU detection); reranker (model:
     BAAI/bge-reranker-v2-m3).
   - `src/pbs_mcp/db.py` — LanceDB connection at
     `config.lancedb_path()`, schema per
     `backend/mcp-server/docs/vector-metadata-schema.md`. Hybrid
     search + reranker pipeline per the same doc's flow section.
4. **Implement tools** in `src/pbs_mcp/tools/`:
   - Per the surface declared in
     `plugin/skills/orchestrator/SKILL.md` "MCP tool surface" and
     individual skill SKILL.md files.
   - Pydantic schemas for tool I/O in `src/pbs_mcp/schemas.py`.
5. **Wire tools into server**: update
   `src/pbs_mcp/server.py` to register tools (decorate with
   `@server.call_tool`) and return them from `list_tools()`.
6. **Per-source chunkers**: implement `src/pbs_mcp/chunkers/` per
   `backend/mcp-server/docs/chunking-strategy.md`.
7. Run smoke test: server starts; `list_tools()` returns full
   surface; manual MCP request via stdio test gets a real response.
8. **Commit + push**.
9. **Update `.mcp.json`** in `plugin/` to register the local
   server. Test via `/reload-plugins` in Claude Code.

After backend is working, then:

- `references-manifest.yaml` population
- `research-references` actually fetches Tier 1 docs
- Ingest references + corpus + bausteine into LanceDB
- Office state seeding (`_ai-office-state/`)
- Office identity config (`memory/global/identity.md`)

THEN the system can be tested end-to-end on a real project (e.g.
binding the 23-12 Vorbeck project, doing a phase A/B/C cycle).

After that, "Not designed yet" backlog items as they're needed.

---

## Working-style notes (lessons from this session)

For the next session to avoid the failure modes I hit:

1. **Apply `ARCHITECTURE.md` rules rigorously**. When placing new
   content, walk Rules 1-5 in order. Don't generalize patterns from
   skill-craft to memory or vice versa.
2. **Memory file format**: pure markdown, no frontmatter unless it's
   a data record (D type). Skills always have frontmatter
   (Claude Code requires it). Skill references — frontmatter only if
   it serves a queryable purpose.
3. **No "consumed by skill X" cross-refs in content**. They don't
   change AI behavior. Documentation of inter-module references
   belongs in code comments or commit messages.
4. **Skill triggers**: detailed, specific German + English phrases.
   Not abstract.
5. **For Begründung/Festsetzungen drafting**: the canonical templates
   are at `~/dev/Planungsbüro-Schulz/22-16-Maxsolar---Friedrichshof---*`,
   NOT at hidrive `Vorlagen/Latex/` (that was old/abandoned).
6. **Source-grounding guard**: any legal citation must be backed by
   a tool result (search_corpus or read_corpus_file). Never invent
   citations from training memory. (BNatSchG amendment date in
   training memory was wrong; current is Art. 48 vom 23.10.2024.)
7. **PBS uses pdflatex everywhere**. Never xelatex.
8. **Project labels**: PBS uses "Textteil B" / "Textteil C" folder
   names but the file names confuse: `Textteil-B-B-Plan.tex` is in
   the Festsetzungen folder. Begründung is multi-page narrative;
   Festsetzungen is the single-page article-class doc that goes
   into the Satzung as Teil B Text. Don't get confused.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM available for GPU
  models). Python 3.13 will be auto-installed by uv if missing.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Skill-craft**: invoke when authoring/improving skills. We did
  for the orchestrator. For new skills in next session, may want to
  use it again — depends on complexity.
- **Hidrive auth**: hidrive paths are accessible because hooks were
  updated this session. Verify symlink at
  `/home/g/.claude/settings.json -> dotfiles/claude/settings.json`
  is intact. If broken, restore per
  `/home/g/.claude/CLAUDE.md` instructions.
- **Plugin reload**: after this session ends, the next session will
  pick up the latest skills automatically (they're symlinked into
  cache). User can run `/reload-plugins` if any are stale.
