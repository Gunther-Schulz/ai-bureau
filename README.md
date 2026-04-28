# pbs-bureau

Claude Code plugin and local backend for drafting, reviewing, and refining
planning documents (B-Plan Begründung, Textliche Festsetzungen,
Umweltberichte, Artenschutzbewertungen, etc.) in the workflow of
Planungsbüro Schulz.

Status: scaffolding in progress.

## Layout

```
pbs-bureau/
├── .claude-plugin/marketplace.json    marketplace registration
├── plugin/                            the Claude Code plugin
│   ├── .claude-plugin/plugin.json
│   ├── CLAUDE.md
│   └── skills/orchestrator/           master skill (SKILL.md + PROCEDURE.md)
├── memory/                            shared memory (not part of plugin distribution)
│   └── domain/
│       ├── style/style-spec.md
│       ├── conventions/korrektur-rules.md
│       ├── doctypes.yaml
│       └── project-structure.md
├── backend/                           MCP server + Docker stack (planned)
└── dev-link.sh                        symlink the plugin into Claude's cache for dev
```

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
