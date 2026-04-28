---
name: validate-bausteine
description: This skill should be used to sweep memory for stale or flagged bausteine — review_due dates passed, status=flagged, citation drift detected, or successive UNB rejections. Triggered at session-open by the orchestrator (when the in-scope domain has bausteine), by direct user phrases like "check bausteine", "freshness sweep", "are my bausteine current", or after a research-references run that may have flagged dependents.
version: 0.1.0
license: MIT
---

# validate-bausteine

Specialist skill for periodic baustein freshness sweeps. Walks
in-scope bausteine, identifies staleness signals, and surfaces
candidates for review.

## Load this now

Read `<repo>/plugin/skills/save-baustein/references/format.md` for
baustein frontmatter schema (especially `status`, `last_validated`,
`review_due`, `references[]`, `flagged_reason`).

Read `<repo>/memory/domain/conventions/korrektur-rules.md` for
content-style conventions used in baustein bodies.

## When invoked

Three modes:

- **Session-open sweep** (automatic) — orchestrator runs at session
  open if domain bausteine are loaded. Surfaces stale candidates as
  surfacings, not blocking.
- **On-demand sweep** — user request "freshness check on bausteine".
- **Post-references-update** — after `research-references` updates
  legal texts, sweep affected bausteine for drift.

Inputs:
- **Scope filter** (optional) — which scope(s) to check. Default:
  all loaded scopes.
- **Domain filter** (optional) — specific domain.

## Behavior

1. **Enumerate bausteine in scope**:
   - For global: `<repo>/memory/global/*.md`
   - For domain: `<repo>/memory/<domain>/*.md`
   - For project: `<project-root>/_ai/bausteine/*.md`

2. **For each baustein, check freshness signals**:
   - **review_due passed**: `frontmatter.review_due < today`
   - **status flagged**: `status != active`
   - **flagged_reason mentions reference change**: indicates
     research-references found drift
   - **last_validated > 1 year ago** (regardless of review_due)
   - **rejected_uses non-empty AND no successful_uses since last
     rejection**: track record gone bad
   - **citation in references[] drifted**: cross-check with
     references-manifest current_amendment_form

3. **Build candidate list** with priority:
   - **High**: status=flagged + flagged_reason indicates legal change
   - **Medium**: review_due passed OR last_validated > 1 year
   - **Low**: status=active but use_count=0 in 6+ months (stale by
     non-use rather than by content drift)

4. **Surface candidates** as four-way menu items (one per baustein):
   ```
   Noticed: §45-nr5-innenbereich-privat is flagged because BNatSchG
   amendment 2024-10-23 changed the §45 wording. Review?
   → capture-now (re-validate as-is) / handle-now (open + edit) /
     backlog / drop-flag (clear flag without changes)
   ```

5. **Per user decision per baustein**:
   - `capture-now (re-validate)`: update `last_validated: today`,
     reset `review_due: today + 1y`. Status remains flagged unless
     user explicitly clears.
   - `handle-now (open + edit)`: open the baustein for editing.
     User makes changes; re-save updates `last_validated` and may
     clear flag.
   - `backlog`: append to `<repo>/memory/product-backlog.md` with
     reason and date.
   - `drop-flag`: clear `status=active`, `flagged_reason=null`. Log
     reasoning to baustein History section.

6. **Don't bulk-update** — each baustein gets its own decision.

## Output

```
Baustein freshness sweep — domain artenschutz

Found 7 bausteine. 3 candidates surfaced:

[High] §45-nr5-innenbereich-privat
  Status: flagged
  Reason: BNatSchG §45 reworded by 2024-10-23 amendment
  Last validated: 2026-04-22 (4 months ago)
  → capture-now / handle-now / backlog / drop-flag

[Medium] steinriegel-spec
  review_due: 2026-04-22 (passed)
  Last validated: 2025-04-22 (1 year ago)
  use_count: 4 (still active)
  → capture-now / handle-now / backlog / drop-flag

[Low] umweltbericht-zusammenfassung-template
  Last used: 2025-08-15 (8 months ago)
  Status: active, no flag
  → capture-now (revalidate without changes) / drop (archive)
```

## Edge cases

- **Baustein status=archived**: skip from sweep; don't re-surface.
- **Baustein in project scope but project state=archived**: surface
  as candidate for project-scope cleanup.
- **Citation in baustein references[] not in references-manifest**:
  surface as "out-of-scope citation; can't verify". Suggest user add
  to manifest.
- **Massive volume of stale bausteine** (e.g. >50): cap surfacing at
  top-N by priority; offer "show more" continuation.

## Tools used

- `Glob` — enumerate bausteine paths.
- `Read` — baustein content + frontmatter.
- `search_corpus` (when MCP backend lands, with filter
  source_type=reference) — verify references[].
- `Edit` — update baustein frontmatter on user decisions.

Until backend lands: `Grep` against `<hidrive>/_ai-references/`
for manual citation freshness check (slower but works).
