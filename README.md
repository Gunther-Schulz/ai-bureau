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

This codebase enforces three meta-rules. New content goes through
them before placement:

1. **App vs office** — no PBS-specific values in repo content. All
   identity / paths / practices / styling come from `office-config.yaml`
   resolved via env-var-then-XDG.
2. **Memory vs RAG** — verbatim legal text lives in the RAG corpus
   (queryable on demand); memory holds workflow logic, conventions,
   §-references as labels only.
3. **Scope orthogonality (universal × domain × state)** — references,
   doctypes, skeletons, bausteine all decompose along the same three
   axes. Bureaus pick their `(domains × states)` selection in
   `office-config.yaml > scope`; layered loaders merge accordingly.

See `ARCHITECTURE.md` for full specification.

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
