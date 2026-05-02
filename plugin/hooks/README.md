# pbs plugin hooks

Structural enforcement hooks per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (wrong-shapes-impossible). Hooks fire mechanically; AI internal vigilance not relied upon.

## architectural_commit_gate.py

**Type**: `PreToolUse` hook on `Edit | Write | MultiEdit`.

**Purpose**: blocks architectural-artifact writes unless preparatory Reads happened in current session. Implements Option A from session-16 doc-organization-templates.md / drafts/execution-fidelity.md mechanism candidates.

**Triggers on path patterns**:
- `arch/*.md` (per-topic ARCH detail)
- `docs/decisions/*.md` (DRs)
- `ARCHITECTURE.md` / `GLOSSARY.md` / `MAINTENANCE.md` / `DISCIPLINES.md` (top-level architectural docs)

**Skips** for: `HANDOFF.md` / `BACKLOG.md` / non-architectural files (operational; not architectural artifacts).

**Checks**:

| # | Check | Block message |
|---|---|---|
| 1 | `decision-design-sharpening/SKILL.md` Read in last 100 tool calls | "READ decision-design-sharpening SKILL.md before architectural commit." |
| 2 | `profiles/INDEX.md` + ≥3 `profiles/L*.md` cluster members Read in last 100 tool calls (only for `arch/*.md` + new DRs) | "READ profiles/INDEX.md + ≥3 cluster members for profile-anchored validation." |
| 3 | Archive paths cited in write content also Read in current session (greenfield-evaluation discipline) | "Archive source <path> cited but not Read in current session — greenfield-evaluation requires direct Read." |

**Resolution**: Read the named files via Read tool, then retry Write/Edit.

**Honest limitations**:
- Detects FILE-READ-HAPPENED, not GREENFIELD-EVALUATION-HAPPENED. Quality remains convention-grade.
- Hook fires at write-boundary; doesn't gate Round 2 sharpening semantically (no per-Round mechanical signal).
- Hook can be bypassed by AI directly invoking Bash for file writes — by-design (Edit/Write/MultiEdit are the standard architectural-commit paths).

**Failure modes covered** (per `drafts/execution-fidelity.md` disguises catalog):
- #1 Compaction pattern-matching: skill-freshness check forces re-Read post-compact
- #2 Fresh-session no-breadcrumbs: same checks fire post-fresh-start
- #4 Skipping steps that feel covered: blocking forces explicit Read at write-boundary
- #5 Substituting AI judgment for codified rule: hook is the rule; AI judgment can't bypass
- #8 Surface compliance without depth: archive-citation cross-check forces Read of cited sources

**Provenance**: implemented session 16 (commit TBD) per user direction after recurrent META-failure (substrate Round 1 procedural fidelity failure + arch/coordination.md cargo-cult drift). Procedural redundancy fix (5-location structural fix; commit be7c8fa) addressed compaction-pattern-matching (Disguise #1) only; this hook addresses Disguises #4 + #5 + #8 structurally.

## Re-loading hooks after plugin update

After modifying hook scripts or plugin.json hooks section:
1. `/reload-plugins` in Claude Code (or restart CLI)
2. Per `feedback_plugin_marketplace_clone_sync.md` (memory) — if /reload-plugins shows stale hook list, marketplace clone at `~/.claude/plugins/marketplaces/<name>/` may need manual `git fetch + reset --hard origin/main`

## Testing the hook

Manual smoke test:

```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"/test/arch/foo.md","new_string":"test"},"transcript_path":"/nonexistent"}' | \
  python3 /home/g/dev/Gunther-Schulz/pbs-bureau/plugin/hooks/architectural_commit_gate.py
```

Expected: exit 2 (block); stderr names missing Reads.
