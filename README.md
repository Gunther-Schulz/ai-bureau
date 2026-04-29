# pbs-bureau

Claude Code plugin and local backend for drafting, reviewing, and refining
planning documents (B-Plan Begründung, Textliche Festsetzungen,
Umweltberichte, Artenschutzbewertungen, etc.) at any German Planungsbüro.
PBS is the reference deployment.

Status: scaffolding in progress.

## Layout

```
pbs-bureau/
├── .claude-plugin/marketplace.json    marketplace registration
├── plugin/                            the Claude Code plugin
│   ├── .claude-plugin/plugin.json
│   ├── CLAUDE.md
│   ├── skills/                        orchestrator + specialists
│   └── templates/
│       ├── classes/                   universal LaTeX cls files
│       ├── skeletons/
│       │   ├── universal/<doctype>/   layered skeletons (every bureau)
│       │   └── domain/<X>/<doctype>/  domain overlays (composed at scaffold)
│       └── office-style/
│           ├── office-style.default.sty
│           ├── office-style.PV-FFA.sty   domain overlays
│           └── office-style.Wind.sty
├── extensions/                        layered manifests
│   ├── universal/{references-manifest,doctypes}.yaml
│   ├── domain/<X>/{references-manifest,doctypes}.yaml
│   └── state/<X>/{references-manifest,doctypes}.yaml
├── memory/                            shared memory (not in plugin distribution)
│   ├── universal/                     universal domain knowledge
│   │   ├── style/style-spec.md
│   │   ├── conventions/korrektur-rules.md
│   │   ├── verfahren/bauleitplanung-phasen.md
│   │   ├── per-project-memory/        state.md / decisions.md formats
│   │   └── project-structure.md
│   └── bausteine/                     saved reusable text patterns
│       ├── universal/
│       ├── domain/<X>/
│       └── state/<X>/
├── backend/                           MCP server (LanceDB + bge-m3 + reranker)
└── docs/office-config.schema.yaml     per-deployment config schema
```

## Architectural meta-rules

This codebase enforces four meta-rules + one named layering
convention. New content goes through them before placement:

1. **App vs office (deployment portability)** — no PBS-specific
   values in repo content. All identity / paths / actors / styling
   come from `office-config.yaml` resolved via env-var-then-XDG.
   Pluggable integration adapters (email/calendar/scanner/etc.)
   are a corollary of this rule — no hardcoded mechanism.
2. **Memory vs RAG (citation freshness)** — verbatim legal text
   lives in the RAG corpus (queryable on demand); memory holds
   workflow logic, conventions, §-references as labels only.
3. **Source-of-truth & invalidation** — every entity declares its
   invalidation contract (semver, references_used, status flags,
   schema_version). `research-references` is the cross-cutting
   refresh handler.
4. **Execution determinism** — deterministic logic lives in MCP
   tools (gates), not skill behavior. Skills declare their
   MCP-tool dependencies in YAML frontmatter
   (`mcp_tools_required[]`, `_optional[]`, `fallback_when_mcp_absent`).

**Plus** a named layering convention: **Scope orthogonality
(universal × domain × state)** — references, doctypes, skeletons,
bausteine all decompose along these three axes. Bureaus pick their
`(domains × states)` selection in `office-config.yaml > scope`;
layered loaders merge accordingly. (Demoted from meta-rule status
in v0.5 — it's a layering pattern *within* configuration entities,
not a placement axis itself.)

See `ARCHITECTURE.md` for the full taxonomy + 5 entity types + 3
decision rules. See also:

- `VISION.md` — three-axis thesis (intertwined-AI-workflow /
  sparring partner / authorship preservation) + pioneer-instance
  framing
- `ROADMAP.md` — deferred work + pull-forward triggers + decision-
  recording convention
- `HANDOFF.md` — current-session state, what's done, what's next
- `docs/rag-pipeline-decisions.md` — pre-RAG architectural
  decisions (ACCEPTED post-audit)
- `docs/{plugin,backend}-conventions.md` — within-tier idioms

## Development workflow

Edits to skills should be picked up by Claude Code on `/reload-plugins`
without needing to bump version or run a full reinstall. To enable that
during active development:

```bash
# One-time, after the marketplace is registered in ~/.claude/settings.json:
./dev-link.sh
```

This replaces the cached plugin copy at
`~/.claude/plugins/cache/pbs-bureau/pbs/<version>/` with a symlink to
this repo's `plugin/` folder. After that, edit any file under
`plugin/` and run `/reload-plugins` in Claude Code. No reinstall.

Re-run `dev-link.sh` whenever:
- You bump the version in `plugin/.claude-plugin/plugin.json` (the
  cache path includes the version).
- You ran `claude plugin uninstall` and want to redo the dev setup.

For releases, the standard install flow takes over:

```bash
claude plugin marketplace update pbs-bureau
claude plugin install pbs@pbs-bureau
```

## First-time setup

1. Add the marketplace to `~/.claude/settings.json`:
   ```json
   "extraKnownMarketplaces": {
     "pbs-bureau": {
       "source": {
         "source": "github",
         "repo": "Gunther-Schulz/pbs-bureau"
       }
     }
   }
   ```
2. Enable the plugin:
   ```json
   "enabledPlugins": {
     "pbs@pbs-bureau": true
   }
   ```
3. Run `./dev-link.sh` from this repo.
4. Restart Claude Code or run `/reload-plugins`.
5. Run the `setup-office` skill — it walks you through identity,
   paths, scope (which planning domains + Bundesländer), and
   integration adapters; writes `office-config.yaml` outside the repo.
6. Run `research-references` to fetch the legal references corpus
   for your selected scope.
