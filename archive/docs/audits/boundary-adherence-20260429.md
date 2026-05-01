# Boundary-adherence audit (slice 14, first run)

**Date**: 2026-04-29
**Scope**: per slice 14 spec (skills + PROCEDURE.md + Python backend)
**Trigger**: verification run for ARCHITECTURE.md meta-rule 4's
session-6 sharpening (refinements A + B).
**Skill version**: audit 0.4.0

---

## Summary

- **Total findings**: 3 (1 in Pattern 1, 1 in Pattern 2, 1 in Pattern 3)
- **BLOCKERS**: 0
- **Pre-launch placement debt**: 3 (all three are honestly debt — real
  architectural placement issues with non-trivial fix cost; deferred
  to ROADMAP)

The codebase **adheres to meta-rule 4's core principle**. Skills are
for judgment + conversation; deterministic operations live in MCP
gates. The 3 findings are placement *refinements* — opportunities
to move logic to its more correct home — not ship-blocking
violations.

Pattern 4 (reuse-direction) found nothing. No two skills carry
duplicated procedural blocks; no two MCP tools duplicate
determinism. The Skill Bundle pattern is being used correctly.

---

## Findings

### Pattern 1 — Inverted-determinism in skills

**Finding 1a — `save-baustein` describes dedupe logic in skill prose**

- **File**: `plugin/skills/save-baustein/SKILL.md` lines 65-75
- **What's described**: Dedupe guard procedure — call
  `list_bausteine(scope, scope_key)`, then surface candidates whose
  `title` or `tags` "overlap meaningfully" with the new baustein.
  Title + tag match is described as "the practical guard."
- **Violation**: The matching algorithm (what counts as "overlap
  meaningfully") is described in skill prose. Two implementations
  would not necessarily agree byte-for-byte. The skill body is
  *describing how to do* something deterministic instead of
  *calling a tool* that does it.
- **Proposed canonical home**: New MCP tool `dedupe_bausteine(scope,
  scope_key, title, tags) → list[BausteinCandidate]` that returns
  ranked candidates. Skill calls tool; tool owns the matching
  algorithm with a reproducible scoring rule.
- **Severity**: LOW. Pre-launch the skill body is functional;
  user is in the loop on collision decisions. Becomes debt when
  the matching algorithm wants to grow (HyDE-style paraphrase
  search is already mentioned as a future enhancement in the same
  skill prose).
- **Defer reason**: Building `dedupe_bausteine` requires Pydantic
  schema for candidate output, scoring rule design, and tests.
  Half-day diff; deserves its own design pass.

---

### Pattern 2 — Inverted-judgment in Python

**Finding 2a — `_infer_source_subtype` hardcodes path-pattern
classification**

- **File**: `backend/mcp-server/src/pbs_mcp/tools/ingest.py` lines
  182-226
- **The decision being made**: classifies a path into one of
  `snapshot | correspondence | project-folder | local-repo |
  external | gesetz-bund | gesetz-eu | gesetz-state | leitfaden |
  urteil | beispiel | reference | universal | domain | state |
  project | baustein` based on substring matches like
  `"/_ai/snapshots/" in p_lower`,
  `"/gesetze/bund/" in p_lower`,
  `"/bausteine/universal/" in p_lower`.
- **Why this is a placement issue**: The classification rules ARE
  deterministic per-deployment. But they're *not invariant* across
  deployments — an office that uses `.ai/` instead of `_ai/`, or
  flat `Gesetze-Bund/` instead of `gesetze/bund/`, would get
  silent wrong classification. The function's docstring claims
  "classification is by path containment rather than substring
  matching, so it works on any office layout" — but that's
  partially false (lines 196, 203, 207, 217 onward are substring
  match, not containment).
- **Reframe**: This isn't truly inverted-judgment (the verdict
  isn't ambiguous within a fixed convention). It's
  **deployment-tunability drift**: deterministic logic that should
  be configurable per-office is hardcoded as if invariant.
- **Proposed canonical home**: Move classification rules to
  office-config schema (e.g., `conventions.path_classification:
  {snapshot_pattern: "/_ai/snapshots/", correspondence_patterns:
  [...]}`). Deterministic, but per-deployment-correct. Function
  consults config rather than hardcoding.
- **Severity**: MEDIUM. Wrong classification lands as silent
  metadata in LanceDB. Search filters by `source_subtype =
  "snapshot"` would miss real snapshots in mis-classified
  deployments. Pre-launch: easy to fix; post-ingest: requires
  re-indexing.
- **Defer reason**: The fix touches office-config schema (would
  bump v3 → v4) plus the ingest classifier plus migration. That's
  not a 30-minute change. Deserves a design pass on the schema
  shape (single regex per class? list of patterns? matched in
  order?). Captured as ROADMAP entry.

---

### Pattern 3 — Persistence-boundary leak

**Finding 3a — `record-feedback` directly Edits baustein
frontmatter**

- **File**: `plugin/skills/record-feedback/SKILL.md` lines 117-120
- **What's being written**: Skill body directs:
  > Append `{project, date, feedback_path}` to baustein's
  > `rejected_uses[]` (via Edit; future MCP tool
  > `record_baustein_use` could atomicize).
- **Why this is a leak**: Bausteine are schema-bearing — frontmatter
  is owned by Pydantic models in `pbs_mcp/schemas.py`/`memory.py`
  with cross-reference invariants. Direct skill `Edit` of frontmatter
  fields bypasses validation, forward-migration, and any future
  cross-reference enforcement (e.g., feedback_id linking).
- **Counter-example (NOT a violation)**: record-feedback also writes
  the feedback entry itself as a prose `.md` file under
  `_ai/feedback/` — that's loose markdown, no schema, fine.
- **Proposed canonical home**: New MCP tool `record_baustein_use(
  baustein_name, scope, scope_key, kind, project, date,
  feedback_path) → BausteinSummary` where `kind ∈ {rejected,
  successful}`. Tool owns frontmatter mutation, validation,
  cross-reference. Skill calls tool.
- **Severity**: LOW (pre-launch). Frontmatter schema is simple
  today; direct Edit doesn't break invariants yet. Becomes debt
  the moment frontmatter gains structure (e.g., feedback_id
  references).
- **Self-acknowledged**: the skill body itself flags this as known
  debt with the parenthetical *"future MCP tool record_baustein_use
  could atomicize"*. Not a hidden violation.
- **Defer reason**: same as 1a — schema + handler + tests for
  the new tool. Half-day diff.

---

### Pattern 4 — Reuse-direction violation

**No findings.**

Cross-skill check: skills with overlapping conceptual territory
(draft-textteil-b, draft-textteil-c; review-draft + the validate-*
trio) have differentiated procedural bodies. No copy-paste blocks
≥10 lines.

Cross-tool check: MCP tools in `pbs_mcp/tools/` are thin handlers
delegating to `office_config`/`config`/`memory` modules. No
duplicated determinism between handlers.

The Skill Bundle reference convention (`references/<topic>.md`)
is being used correctly: shared interpretive scaffolding lives in
references files, not pasted into multiple SKILL.md bodies.

---

## Pre-launch placement debt

All 3 findings → ROADMAP. Each requires a non-trivial diff
(schema work + Pydantic + tests for the new MCP tool, OR
schema + migration for office-config). None are 30-minute fixes.

| Finding | Proposed canonical home | Trigger to build |
|---|---|---|
| 1a save-baustein dedupe | `dedupe_bausteine` MCP tool | When matching algorithm grows beyond title+tag (planned: HyDE paraphrase search via search_corpus over indexed bausteine) |
| 2a `_infer_source_subtype` | `office-config.conventions.path_classification` block + config-driven classifier | **RESOLVED in-session 2026-04-29.** Landed as purely-additive optional block in v3 (no schema bump). PathClassification Pydantic model + classifier consults config first, falls back to hardcoded patterns. |
| 3a record-feedback frontmatter Edit | `record_baustein_use` MCP tool | When baustein frontmatter gains cross-reference structure (e.g., feedback_id linking) |

---

## Stopping decision

**Slice 14 is complete on this first run.**

The codebase passes the boundary-adherence test at the architectural
level. All findings are forward-looking placement debt with clear
canonical homes; none are silent wrong-shipping logic. No need to
re-run slice 14 until either:

1. A major refactor moves logic across the boundary (then re-run as
   verification), or
2. One of the proposed canonical homes lands (then verify the new
   tool actually owns what the skill previously described).

The audit slice 14 procedure is itself validated by this run — it
detects real placement issues without false positives, and Pattern 4
correctly returned empty rather than manufacturing similarity-
findings. Procedure is keepable as-is.
