---
name: validate-bausteine
description: This skill should be used to sweep memory for stale or flagged bausteine — review_due dates passed, status=flagged, citation drift detected, or successive UNB rejections. Triggered at session-open by the orchestrator (when the in-scope domain has bausteine), by direct user phrases like "check bausteine", "freshness sweep", "are my bausteine current", or after a research-references run that may have flagged dependents.
version: 0.4.0
license: MIT
mcp_tools_required: [list_bausteine]
mcp_tools_optional: [list_reference_manifests, find_bausteine_by_reference, search_corpus, flag_baustein, archive_baustein]
fallback_when_mcp_absent: "without list_bausteine the skill cannot operate — bausteine are contract-bearing (frontmatter has status, last_validated, review_due invariants per ARCHITECTURE meta-rule 4 fail-closed corollary). The skill's whole purpose is freshness sweep; without the gate it cannot reliably read invalidation contract fields. Surface 'MCP unreachable; restart backend' and stop."
summary: Sweeps memory for stale or flagged bausteine — review_due passed, status=flagged, citation drift, successive UNB rejections.
routing_mode: direct
triggers:
  - check bausteine freshness
  - sweep stale bausteine
handoffs: []
phase_role: utility
---

# validate-bausteine

Specialist skill for periodic baustein freshness sweeps. Walks
in-scope bausteine via `list_bausteine` (MCP tool, scope-aware
per orthogonality), identifies staleness signals, and surfaces
candidates for review.

## Load this now

Read `<repo>/plugin/skills/save-baustein/references/format.md` for
baustein frontmatter schema (especially `status`, `last_validated`,
`review_due`, `references[]` with `verified_against_version` slot,
`flagged_reason`, `cross_project_visible`).

Read `<repo>/memory/universal/conventions/korrektur-rules.md` for
content-style conventions used in baustein bodies.

## When invoked

Three modes:

- **Session-open sweep** (automatic) — orchestrator runs at
  session open if in-scope bausteine are loaded. Surfaces stale
  candidates as surfacings, not blocking.
- **On-demand sweep** — user request "freshness check on
  bausteine".
- **Post-references-update** — after `research-references`
  updates legal texts, sweep affected bausteine for drift via
  the `verified_against_version` field.

Inputs:

- **Scope filter** (optional) — which scope/scope_key to check.
  Default: walks all in-scope bausteine
  (`list_bausteine(scope=None)`).
- **Project filter** (optional) — for project-scope bausteine of
  a specific project (supply project_root or scope_key).

## Behavior

1. **Enumerate bausteine in scope** via
   `list_bausteine(scope?, scope_key?, project_root?)`. Returns
   the layered baustein set per office's scope. No more
   filesystem Glob — the MCP tool handles path resolution.

2. **For each baustein, check freshness signals**:

   - **review_due passed**: `frontmatter.review_due < today`
   - **status flagged**: `status != active`
   - **flagged_reason mentions reference change**: indicates
     research-references found drift
   - **last_validated > 1 year ago** (regardless of review_due)
   - **rejected_uses non-empty AND no successful_uses since last
     rejection**: track record gone bad
   - **citation in references[] drifted**: per priority
     touchpoint refactor — compare each
     `references[N].verified_against_version` against the
     manifest's current `current_amendment_form` (via
     `list_reference_manifests` + per-entry lookup). If a
     reference amended since the baustein was last verified,
     flag for re-validation. Delegate the deeper drift check
     to `verify-citations` for the actual cited-content
     comparison.

3. **Build candidate list** with priority:

   - **High**: status=flagged + flagged_reason indicates legal
     change; OR `verified_against_version` drift detected
   - **Medium**: review_due passed OR last_validated > 1 year
   - **Low**: status=active but use_count=0 in 6+ months (stale
     by non-use rather than by content drift)

4. **Surface candidates** as four-way menu items (one per
   baustein):

   ```
   Noticed: §45-nr5-innenbereich-privat (domain/Naturschutz) is
   flagged because BNatSchG §45 verified_against_version
   "i.d.F. 08.12.2022" lags manifest current
   "i.d.F. 23.10.2024". Review?
   → capture-now (re-validate as-is) / handle-now (open + edit) /
     backlog / drop-flag (clear flag without changes)
   ```

5. **Per user decision per baustein**:

   - `capture-now (re-validate)`: update `last_validated: today`,
     reset `review_due: today + 1y`, optionally update
     `references[].verified_against_version` to current. Status
     remains flagged unless user explicitly clears.
   - `handle-now (open + edit)`: open the baustein for editing.
     User makes changes; re-save updates `last_validated` and
     may clear flag. Optionally route to `verify-citations` for
     deep drift inspection first.
   - `backlog`: append to `<repo>/memory/product-backlog.md` with
     reason and date.
   - `drop-flag`: clear `status=active`, `flagged_reason=null`.
     Log reasoning to baustein History section.

6. **Don't bulk-update** — each baustein gets its own decision.

## Output

```
Baustein freshness sweep — scope=domain/Naturschutz

Found 7 bausteine. 3 candidates surfaced:

[High] §45-nr5-innenbereich-privat (domain/Naturschutz)
  Status: flagged
  Reason: BNatSchG §45 amendment 2024-10-23; last verified
          against "i.d.F. 08.12.2022"
  Last validated: 2025-04-22 (1 year ago)
  → capture-now / handle-now / backlog / drop-flag

[Medium] steinriegel-spec (domain/Naturschutz)
  review_due: 2026-04-22 (passed)
  Last validated: 2025-04-22 (1 year ago)
  use_count: 4 (still active)
  → capture-now / handle-now / backlog / drop-flag

[Low] umweltbericht-zusammenfassung-template (universal)
  Last used: 2025-08-15 (8 months ago)
  Status: active, no flag
  → capture-now (revalidate without changes) / drop (archive)
```

## Edge cases

- **Baustein status=archived**: skip from sweep; don't re-surface.
- **Baustein in project scope but project state=archived**:
  surface as candidate for project-scope cleanup.
- **Citation in baustein references[] not in any in-scope
  manifest**: surface as "out-of-scope citation; can't verify".
  Suggest user add to manifest if relevant.
- **Massive volume of stale bausteine** (e.g. >50): cap surfacing
  at top-N by priority; offer "show more" continuation.
- **`cross_project_visible` bausteine** (project-scope but
  cross-visible): include in sweeps for OTHER projects too. The
  source project's lifecycle drives validity, but the visibility
  flag means consumers in other projects also benefit from
  freshness-aware retrieval.

## Tools used

- `list_bausteine(scope?, scope_key?, project_root?, status?)`
  (MCP, required) — scope-aware enumeration; replaces filesystem
  Glob. Handles the layered tree.
- `list_reference_manifests(scope_filter=true)` (MCP, optional) —
  for citation-drift checks against current `current_amendment_form`.
- `find_bausteine_by_reference(law?, paragraph?, ruling?,
  leitfaden?)` (MCP, optional) — when user wants to scope sweep
  to bausteine affected by a specific reference (e.g. after
  research-references diff).
- `search_corpus(query, filter)` (MCP, optional) — for the
  deeper citation-drift inspection if user routes via
  verify-citations.
- `flag_baustein(name, reason)` (MCP, optional) — apply
  status=flagged from sweep findings.
- `archive_baustein(name, superseded_by?)` (MCP, optional) —
  for `drop (archive)` action on stale-by-non-use bausteine.

When MCP backend unreachable: fall back to `Glob` over
`memory/bausteine/{universal,domain/<X>,state/<X>}/` tree and
`Read` of frontmatter directly. Citation-drift check skipped
(no manifest access without backend). Warn user about degraded
mode.
