# Invalidation-contract audit (slice 15, first run)

**Date**: 2026-04-29
**Scope**: per slice 15 spec
**Trigger**: verification run for ARCHITECTURE.md meta-rule 3
audit coverage gap (identified during design-review target 8
first run earlier this session).
**Skill version**: audit 0.5.0

---

## Summary

- **Total findings**: 2 (both Pattern 1 reframed; both informational)
- **BLOCKERS**: 0 (the first-run agent flagged 1 BLOCKER; this
  artifact rejects that classification — see "Agent push-back"
  below)
- **Pre-launch population gaps noted**: 1 (bausteine directory
  intentionally empty; pattern coverage deferred until first save)

The codebase **adheres to meta-rule 3 at the document-discipline
level**. All currently-populated entities carry their declared
invalidation contracts. The findings are about *enforcement layer*:
the contracts are honored by convention but not validated by code.
Two findings:

1. No Pydantic model validates manifest YAML structure (contract is
   document-discipline only, not code-enforced at parse time).
2. ARCHITECTURE.md meta-rule 3 prose could be sharpened to make
   the two-skill layered reading of bausteine `verified_against_version`
   explicit.

---

## Findings

### F1 — Pattern 1 (reframed): No Pydantic model for manifest YAMLs

**Re-classification of the first-run agent's BLOCKER finding.** The
agent claimed `ManifestInfo.last_updated: str | None = None` in
`backend/mcp-server/src/pbs_mcp/schemas.py:367` was a contract
violation. **This artifact rejects that claim**:

- `ManifestInfo` is the discovery tool's *response* schema (what
  `list_reference_manifests` returns), not the manifest YAML's
  *input* schema.
- The Optional shape on the response is correct: if a manifest
  exists but is malformed (missing `last_updated`), the tool
  reports `None` rather than crashing. That's graceful degradation,
  not contract violation.
- All currently-populated manifests (verified by spot-check) carry
  `last_updated`: 8 manifest files, 8 declared contract fields,
  zero misses.

The actual gap is smaller and different: **there is no Pydantic
model for the manifest YAML structure itself**. The loader reads
manifests via `yaml.safe_load(...)` as a plain dict, walks them
opportunistically, and never validates. Per meta-rule 3's contract,
manifests should require `last_updated` + per-entry `last_fetched`
+ `checksum_sha256`. Today this is enforced by author discipline
(every manifest happens to have these fields), not by code.

**Severity**: LOW (contract is honored today; gap is *forward-
looking* — a future malformed manifest would slip through).

**Proposed canonical home**: New Pydantic models in `pbs_mcp/`
(probably new file `manifest_schema.py`):
- `ReferencesManifest` — top-level shape with required
  `version`, `scope`, `scope_key`, `last_updated`, `maintainer`
- `ReferenceEntry` — per-entry shape with required `id`, `title`,
  `source_url`, `fetch_method`, `canonical_path`, optional
  `last_fetched`, `checksum_sha256`
- `DoctypesManifest` — analogous

Discovery tool keeps its current Optional response schema (it's
the right shape for graceful failure reporting); validation
becomes the loader's responsibility, surfaced via an MCP tool
like `validate_manifest(path)` that returns shape + drift findings.

**Defer reason**: real architecture addition. Half-day to design
the schema, day to build + test. Pre-launch is fine without it
because document discipline is holding. Pull-forward trigger:
before first multi-author manifest contribution OR before
manifest-population grows past the 8 current files where
discipline can be visually checked.

### F2 — Pattern 4 (informational): ARCHITECTURE.md meta-rule 3 prose obscures two-skill layering

ARCHITECTURE.md line 220-225 says:

> **Cross-cutting concern handler.** `research-references` is the
> canonical refresh skill: after fetching an updated reference, it
> scans both bausteine (`references[]`) and memory docs
> (`references_used[]`) for matches. Bausteine matching → flagged.
> Memory docs matching → logged to `memory/product-backlog.md`
> with affected paths.

But the actual contract reading is split across two skills:

- `research-references` reads `references[]` to find which
  bausteine cite an updated law. It flags them.
- `validate-bausteine` reads `references[].verified_against_version`
  to detect drift between cited form and current form. It runs
  the drift comparison.

ARCHITECTURE.md's prose names only `research-references`, which
could mislead readers into thinking it owns the full
contract-reading flow. It doesn't — it's the *trigger*; the
*comparison* is in `validate-bausteine`.

**Severity**: INFORMATIONAL (no broken behavior; documentation
clarity issue).

**Fix**: small ARCHITECTURE.md prose sharpening. Add a sentence
making the layered reading explicit: "research-references detects
*which* bausteine cite updated laws; validate-bausteine reads the
verified_against_version field to detect drift." 30-second edit.

**Action**: applied in this session as part of the slice 15
follow-up (small enough to fold in; Pareto-positive).

---

## Pre-launch population gaps (separate, non-findings)

- **Bausteine**: `memory/bausteine/` exists but contains only
  `README.md` and empty scope subdirs (universal, domain, state).
  Pattern 1 (missing-contract entities) and Pattern 2 (incorrect-
  contract shape) checks for bausteine yield zero findings until
  first baustein is saved. Per HANDOFF, this is intentional.

---

## Verification of handler-reads-contract (Pattern 3)

All declared invalidation hooks are read by their consuming
handler:

- `research-references/SKILL.md` step 6 (lines 118-131) explicitly
  scans `references_used[]` (memory docs) and `references[]`
  (bausteine) for matches — reads contract ✓
- `validate-bausteine/SKILL.md` step 2.6 (lines 73-81) reads
  `references[].verified_against_version` — reads contract ✓
- Backend `memory.py:find_bausteine_by_reference` reads frontmatter
  `references[]` field — reads contract ✓
- Backend `discovery.py:_manifest_info` reads top-level
  `last_updated` field — reads contract ✓

No declared-but-unread contracts. Pattern 3 returned empty.

---

## Stopping decision

**Slice 15 is complete on this first run.** The exercise validated
slice 15 as a useful audit tool — it surfaced a real
architectural-enforcement gap (F1 reframed) and a small
documentation-clarity opportunity (F2). The agent's verdict-
overreach (calling F1 a BLOCKER when it isn't) demonstrates the
value of the human cross-check baked into slice review (per
target 8 finding F3 pattern from earlier this session).

Re-run slice 15 after:
- Manifest Pydantic models land (F1 follow-up) — verify schema-doc-skill agreement post-implementation.
- Any bausteine are saved — pattern 2 checks become live.
- ARCHITECTURE.md meta-rule 3 contract table is extended (e.g., new
  entity type added) — verify all sources of truth get updated.

The slice 15 procedure is keepable as-is. The four-pattern
framing held up; pattern 4 (three-source-of-truth disagreement)
is the most valuable for catching subtle drift the other patterns
miss.
