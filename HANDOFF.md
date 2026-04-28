# Session handoff — pbs-bureau

End of session 2026-04-28 (second major session). The previous
HANDOFF described "backend smoke test green; CUDA confirmed"; this
session pivoted to a deep architectural cleanup: app vs office-config
split, memory↔RAG rule, per-project state, layered LaTeX template
stack, modular integrations. The repo is now a deployable generic
German-planning-bureau workflow app, with PBS as the reference
deployment.

**Read order for next session**:
1. This file (HANDOFF.md)
2. `ARCHITECTURE.md` — meta-rules + 7 entity types + decision rules
3. `docs/office-config.schema.yaml` — the deployment-config schema
4. `plugin/skills/orchestrator/SKILL.md` + `PROCEDURE.md`
5. Whichever skill the user invokes

---

## Status snapshot

### ✅ Architecture transformation (this session)

- **App vs office split** (ARCHITECTURE.md meta-rule + skill-author
  checklist): no PBS-specific values in repo content. All paths,
  identity, practices, state-extensions, LaTeX styling come from
  `office-config.yaml` resolved via env-var-then-XDG.
- **Memory ↔ RAG rule** (ARCHITECTURE.md): cross-cutting memory
  uses §-references as labels only; verbatim legal text lives in
  RAG. Memory docs declare `references_used[]` in frontmatter;
  `research-references` flags both bausteine and memory docs on
  law change.
- **State per-project** (`state.md.bundesland`), never office-level.
  `office.state` removed. `extensions.references_manifests` is a
  `dict[StateCode, Path]` keyed by Bundesland.
- **3-layer LaTeX stack**: app `.cls` + skeletons (Layer 1) +
  office `office-style.sty` + auto-generated `office-identity.tex`
  (Layer 2) + per-project `Projektdaten.tex` (Layer 3). Compile
  composes TEXINPUTS across layers.
- **practices vs partners**: practices = internal sub-units of
  this office. partners = external collaborators (other offices)
  with own email/identity/match-patterns. Both can carry signer +
  email_match_patterns (fnmatch-style).
- **Manifest split**: federal-core in repo
  (`references-manifest.yaml`), state extensions per Bundesland in
  `<state_root>/extensions/<STATE>/`, with example template at
  `docs/office-extensions/MV/references-manifest.example.yaml`.
- **Modular integrations roadmap** (ROADMAP.md): email/calendar/
  scanner/etc. as office-config-declared adapter classes — not
  implemented, principle established.

### ✅ Backend (commit `0fbe511`)

- New `office_config.py` — pydantic schema + loader
  (env-var-then-XDG resolution, validation, identity-macro
  generator helpers).
- `config.py` — delegates path resolution to office_config.
- `tools/projects.py` — practices, folder-layout, project-name
  generation, project-number auto-increment all from config.
- `tools/build.py` — TEXINPUTS-aware compile, auto-regenerates
  `office-identity.tex` from `identity:` section before each
  build.
- `tools/ingest.py` — path classification by config-derived roots.
- `schemas.py` — SourceSubtype renamed (`hidrive-project` →
  `project-folder`, `gesetz-mv` → `gesetz-state`).

### ✅ New surface (commit `ee31899`)

- **`setup-office` skill** — first-time deployment wizard with
  conversational prompt-by-prompt flow (`references/wizard-flow.md`).
  Creates office-config, bootstraps state directory tree, copies
  default office-style + state-extension templates.
- **`setup_project` MCP tool** — single entry point for project
  work. Mode auto-detected from target_root state: absent →
  create+scaffold; empty → scaffold inside; populated → fall back
  to bind. Generates folder name from naming template, scaffolds
  layout per `conventions.project_folder_layout`, copies skeleton
  per doctype, patches Projektdaten.tex placeholders, seeds
  `.ai/state.md`, appends to projects-index.

  Backend now exposes 18 tools (was 17).

### ✅ Identity model extended (commit `9dbe067`)

- Identity gained: `title`, `mobile`, `fax`, `specializations[]`,
  `logo_path`, `signature_image_path`.
- `office-identity.tex` generator emits `\OfficeTitle`,
  `\OfficeMobile`, `\OfficeFax`, `\OfficeSpecializations`,
  `\OfficeLogoPath`, `\OfficeSignaturePath` for office-style.sty
  to consume.
- Bugfix: `\OfficeSignatureBlock` was double-escaping LaTeX line
  breaks; now escapes per-line then joins.

### ✅ PBS deployment configured

`~/.config/pbs-bureau/office.yaml` (NOT in repo):

- Office: **Planungsbüro G. Schulz** (note: with G.); short PBS;
  language de_DE
- Identity: Dipl.-Ing. Gunther Schulz, An der Pferdekoppel 3,
  23972 Dorf Mecklenburg, Tel/Fax 03841/62 0 66 11, Funk
  0178 3268495, mail@planungsbuero-schulz.de,
  www.planungsbuero-schulz.de
- Specializations: Garten-/Landschaftsarchitektur, Solar-/Wind-
  energieplanung, Landschaftsplanung, Stadtplanung
- Practice (internal): `main` — Dipl.-Ing. Gunther Schulz
- Partner: `hendrik` — Hendrik Sönnichsen
  (`hs@deroekologe.de`, `*@deroekologe.de`)
- Paths: hidrive-rooted (state_root, references_root,
  projects_root) + local_repos_root at
  `~/dev/Planungsbüro-Schulz`
- MV state-extension registered at
  `<state_root>/extensions/MV/references-manifest.yaml`

State directory bootstrapped at hidrive:
- `<state_root>/projects-index.md`, `pending-actions.md`,
  `recent-correspondence.md` (empty seeds)
- `<state_root>/templates/office-style.sty` (copy of
  `office-style.default.sty`)
- `<state_root>/templates/office-logo.png`,
  `office-signature.png` (provided + copied)
- `<state_root>/extensions/MV/references-manifest.yaml` (copy of
  example)
- `<references_root>/` with empty subdirs: `gesetze/{bund,eu,MV}`,
  `leitfaeden/`, `urteile/`, `beispiele/`, `changelog.md`

End-to-end smoke test green: office_config loads, all paths
resolve, MV extension reaches manifest, federal-core manifest
reachable, identity macros generate cleanly, practice/partner
email routing works (case-insensitive wildcards), `list_projects`
returns empty (clean state).

### ⏳ Pending — first thing for next session

**Run `research-references` first-time fetch**. Now feasible —
office config + state-extension manifest are in place. Steps:

1. **Reload plugin** (`/reload-plugins`) so the session sees the
   new `setup_project` tool + the office-config-aware backend.
2. **Run research-references**: traverses both
   `<repo>/references-manifest.yaml` (federal core) and
   `<state_root>/extensions/MV/references-manifest.yaml` (state
   extension). For each entry:
   - `web-text` / `web-html` / `web-pdf` entries: WebFetch + write
     to `<references_root>/<canonical_path>`.
   - `manual` entries (KNE leitfäden, LUNG-MV, Verfahrenserlass-MV,
     Brandschutzkonzept-MV): per the new policy, Claude browses
     the publisher site to discover the canonical PDF URL, then
     downloads. **No reading from legacy `Literatur/` folder.**
3. **Ingest references** via `ingest_paths` into LanceDB. First
   call downloads bge-m3 + reranker (~3GB). RTX 5090 picks up
   CUDA automatically.
4. **Sample search**: verify hybrid + reranker pipeline returns
   sensible hits.

After that:
5. Bind first project (any existing hidrive project — orchestrator
   routes through survey-project → bind_project, no schema
   migration needed).
6. Optional: wire `\OfficeLogoPath`, `\OfficeSpecializations` into
   the default `office-style.sty` letterhead layout if you want
   richer compile output.

### ❌ Deferred (not blocking)

- **PBS project migration to colocated layout** — explicitly
  dropped this session. PBS keeps its current per-doctype-LaTeX-repo
  layout under `~/dev/Planungsbüro-Schulz/`. The orchestrator's
  binding flow uses survey-project for adoption.
- **Email integration** — see ROADMAP.md "Modular integrations
  declared at office setup". Adapter pattern locked in;
  Thunderbird-maildir adapter is first implementation when needed.
- **Office-style.sty letterhead** — default version doesn't yet
  use the new `\OfficeLogoPath` / `\OfficeSpecializations`
  macros. Cosmetic; structural compile works without.

---

## Key architectural decisions made (with reasoning)

| Decision | Reasoning |
|---|---|
| **App vs office-config split** | Repo must be deployable to other German planning bureaus. PBS-specific values live in `office-config.yaml` outside repo, resolved via env-var-then-XDG. ARCHITECTURE.md meta-rule + skill-author checklist enforce. |
| **Memory ↔ RAG split** | Memory shadows RAG → drift. Strict rule: §-refs as labels OK; verbatim legal/Verfahrensvermerk text in RAG only; cross-cutting memory declares `references_used[]`; `research-references` flags affected docs on law change. |
| **State per-project** | Offices work cross-state. `office.state` (singular or plural) was wrong. `state.md.bundesland` selects which state-extension manifest applies; office holds a `dict[StateCode, Path]` of registered extensions. |
| **practices vs partners** | Internal sub-practices ≠ external collaborators. PBS itself is one practice (`main`); Hendrik (deroekologe.de) is a partner. Same partner can be co-producer (`state.md.partners[]`) or client (`state.md.client`) on different projects — email match patterns work either way. |
| **3-layer LaTeX stack** | App ships universal cls + skeletons (Layer 1). Office authors `office-style.sty` once for aesthetic (Layer 2). Project provides `Projektdaten.tex` (Layer 3). Identity macros auto-generated from office-config into `office-identity.tex`. TEXINPUTS composes the layers. PBS migration of existing inline-styled masters is a clean rewrite per layer (no backwards-compat). |
| **Federal-core manifest in repo, state extensions out** | Federal laws + KNE leitfäden + BVerwG/EuGH apply to every German bureau (in repo). State laws + state Verfahrenserlasse vary by Bundesland (in office state extensions). Example template at `docs/office-extensions/MV/`. |
| **Auto-incrementing project numbers** | Default per `conventions.project_numbering.{pattern, auto_increment}`. Scans both projects-index AND projects_root for the highest-numbered folder. User can always override. |
| **No project migration this session** | PBS has 16+ existing projects across hidrive + dev tree. One-time conversational migration (not a skill) — deferred until user wants it. |
| **Modular integrations** | email/calendar/scanner/etc. as adapter classes declared in `office-config.integrations:`. Same architectural lesson as paths: no hardcoded mechanism. Roadmap-only for now. |
| **Symlink dev install** | Unchanged from prior session. `dev-link.sh` keeps `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` → `<repo>/plugin/`. Re-run if Claude Code replaces with copy. |

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/` | Claude Code plugin |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/templates/` | App-shipped LaTeX classes + skeletons + default office-style |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/` | Cross-cutting domain memory (universal German planning) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/backend/mcp-server/` | Python MCP backend (18 tools) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/docs/office-config.schema.yaml` | Office-config schema |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/docs/office-extensions/MV/` | M-V state-extension example |
| `~/.config/pbs-bureau/office.yaml` | **PBS office config (NOT in repo)** |
| `/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte/_ai-office-state/` | PBS office state (templates/, extensions/MV/, projects-index, etc.) |
| `/mnt/data2t/hidrive/.../_ai-references/` | PBS AI-owned legal references corpus (subdirs ready, content not yet fetched) |
| `/mnt/data2t/hidrive/.../Projekte/` | All client projects (16+) |
| `~/dev/Planungsbüro-Schulz/` | PBS local per-doctype LaTeX working copies |

---

## Working-style notes (lessons from this session)

1. **Apply ARCHITECTURE.md rules rigorously**. The meta-rules
   (app/office, memory/RAG) catch leakage that's easy to miss in
   isolation. When placing or generating new content, walk the
   meta-rules first.
2. **Memory must NOT contain verbatim legal text**. §-refs as
   labels only. Verbatim wording lives in RAG, retrieved per
   project bundesland. Adding `references_used[]` lets
   `research-references` track dependents.
3. **No "legacy" mentions in skills or app code**. The app
   assumes AI-owned worldview throughout. Bridge to legacy only
   via `survey-project` when binding existing project folders.
4. **State is per-project** (`state.md.bundesland`). Skills resolve
   state-specific references through the project's bundesland,
   never through office-level config.
5. **practices ≠ partners**. Same person/entity (e.g. Hendrik)
   can be partner on one project and client on another. Email
   patterns route correctly either way.
6. **Don't double-escape in LaTeX generators**. Escape per-line
   user content first, THEN add structural LaTeX (line breaks,
   wrappers). Earlier `_generate_identity_macros` had this bug
   in the signature_block; fixed in `9dbe067`.
7. **Source-grounding guard unchanged**. Any legal citation in
   produced output must be backed by a tool result. §-numbers
   appearing in memory don't satisfy the citation-evidence
   requirement.
8. **Commit at coherent checkpoints**. This session: 4 commits
   pushed (`0fbe511`, `ee31899`, `0e4aea7`, `9dbe067`) — each is
   a stable, testable milestone.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Plugin cache symlink**: was getting overwritten by
  Claude Code earlier; re-run `bash dev-link.sh` if
  `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` is a regular
  directory rather than a symlink.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Dotfiles**: global CLAUDE.md and settings.json tracked in
  `~/dev/Gunther-Schulz/dotfiles/claude/`. After editing either,
  commit + push the dotfiles repo.
