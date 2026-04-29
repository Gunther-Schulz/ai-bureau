---
name: record-feedback
description: This skill should be used when external feedback (rejection, approval, partial, suggestion) on planning-bureau work needs to be captured. Triggered by user pasting a UNB Stellungnahme, mentioning a Behörden-Reaktion, "UNB hat abgelehnt", "approval kam von <Person>", "Stellungnahme festhalten", "feedback log", "record this rejection", or similar.
version: 0.4.0
license: MIT
mcp_tools_required: [list_bausteine, flag_baustein]
mcp_tools_optional: [find_bausteine_by_reference, search_corpus, read_corpus_file]
fallback_when_mcp_absent: "without list_bausteine / flag_baustein the skill cannot operate on bausteine — bausteine are contract-bearing (frontmatter has status, last_validated, review_due invariants) per ARCHITECTURE meta-rule 4 fail-closed corollary. Surface 'MCP unreachable; restart backend' and stop. Per-concern cross-referencing via Grep is fine when the gate is up (corpus is content, not contract)."
summary: Captures external feedback (rejection/approval/partial/suggestion) on PBS work, with side-effects on addressed bausteine.
routing_mode: direct
triggers:
  - record feedback
  - capture Stellungnahme        # German technical anchor
  - log UNB rejection
handoffs: []
phase_role: utility
---

# record-feedback

Specialist skill for capturing external feedback (rejections,
approvals, partials, suggestions) and propagating effects to
dependent bausteine. Per priority touchpoint refactor (HANDOFF),
uses **per-concern iteration** for Stellungnahmen with multiple
addressed points instead of one-shot bulk processing — fetch
relevant baseline + ruling + similar past Abwägung per concern.

## Load this now

Read `references/format.md` for the feedback entry format —
frontmatter schema (including scope orthogonality), body
structure, lifecycle, and side effects on addressed bausteine.

## When invoked

By user pasting/referencing a Stellungnahme or feedback artifact,
or explicit phrases. Inputs needed:

- **Date** of the feedback (ISO).
- **Authority** — full name (e.g. "UNB Landkreis Rostock"). Derive
  `authority_slug` (kebab-case, e.g. `UNB-rostock`).
- **Project** — project ID.
- **Type** — `rejection`, `approval`, `partial`, or `suggestion`.
- **Phase** — current bauleitplanung-phase if applicable.
- **Content** — the feedback text or excerpt.
- **Source artifact** — path to the original (mail, PDF,
  snapshot). Must be immutable; if pointing at a live working
  file, refuse and ask for a snapshot instead.

If the user just pastes a Stellungnahme, parse the above fields
from content where possible and ask for missing ones.

## Behavior — per-concern iteration (priority refactor)

Old pattern: parse Stellungnahme, find addressed bausteine in
bulk, save one feedback entry, flag all addressed bausteine
together. Replaced with per-concern iteration: a Stellungnahme
typically raises multiple distinct concerns (FFH, §45, Bodenschutz,
Wasserschutz, etc.); each deserves its own analysis pass.

1. **Parse Stellungnahme structure**:
   - Detect overall verdict tone (rejection / approval language).
   - Decompose into discrete concerns. Most Stellungnahmen
     enumerate (Punkt 1, Punkt 2; or thematic sections). Some
     are monolithic — treat as single concern then.

2. **Per concern, iterate**:

   a. **Identify the addressed argument(s)**: which baustein(s)
      or which arguments in the document does this concern
      address? Surface candidates to user if ambiguous.

   b. **Fetch baseline reference**: `search_corpus(query=<§
      cited in concern>, filter={source_type: reference})` —
      what does the relevant law actually say? Compare to the
      cited form. Catches authority's own citation drift if
      any.

   c. **Fetch interpreting ruling** (if cited or applicable):
      `search_corpus(query=<docket or topic>, filter={
      source_type: reference, source_subtype: urteil})`. Useful
      because authority Stellungnahmen often invoke court
      precedent; surfacing the actual ruling text grounds the
      concern.

   d. **Find similar past Abwägung**: if PBS has past Abwägung
      content addressing the same concern (corpus or bausteine),
      surface via `search_corpus` for context. Don't auto-apply;
      surface for user to inform their response strategy.

   e. **Find affected bausteine**:
      `find_bausteine_by_reference(law=<X>, paragraph=<Y>)` —
      identifies bausteine whose `references[]` mention the
      same law/paragraph. These are downstream candidates for
      flagging if the concern is a rejection/partial.

   f. **Synthesize per-concern entry**: which baustein(s) this
      concern addresses, what the verdict implies, what
      alternative the authority suggests (if any), what
      similar past response existed.

3. **Compose feedback entry** with full frontmatter per format.md:
   - `addresses_bausteine: []` populated with names from step e.
   - `addresses_arguments: []` with human descriptions per concern.
   - `verdict_reasoning` and `suggested_alternative` from content.
   - `source_artifact` validated as immutable.
   - `scope` + `scope_key` on the entry itself: feedback inherits
     scope from the addressed baustein(s); single-scope per entry.
     Multi-baustein-scope-mismatch → split into multiple entries.

4. **Write to disk** at the layered feedback path per format.md
   (resolved by scope/scope_key).

5. **Apply lifecycle effects to addressed bausteine** (one tool
   call per affected baustein):
   - **Rejection / partial**: `flag_baustein(name, reason="see
     <feedback path>")`. Append `{project, date, feedback_path}`
     to baustein's `rejected_uses[]` (via Edit; future MCP tool
     `record_baustein_use` could atomicize).
   - **Approval**: append `{project, date, feedback_path}` to
     `successful_uses[]`. Set `last_validated: <feedback.date>`.
   - **Suggestion**: no auto-flag. Surface as advisory finding
     next session.

6. **Update domain's `feedback/INDEX.md`** — append row with
   `date | authority | type | project | topic | status | path`.
   Sort by date descending.

7. **Confirm to user** with summary: feedback path, type, and
   number of bausteine affected per concern.

## Output

Confirmation including:

- Path of the saved feedback entry.
- Per-concern iteration summary: for each concern, baseline
  reference fetched, similar past Abwägung found (if any),
  affected bausteine flagged.
- Names of bausteine flagged (for rejections) or marked successful
  (for approvals).
- Suggested next action if applicable (e.g. "Project <name>
  has a rejection feedback open — author successor argumentation?
  Past similar response: <path>").

## Edge cases

- **Source artifact is a live working file**: refuse to save
  until a snapshot exists. Ask user to make snapshot or point
  to existing.
- **Feedback addresses arguments without a corresponding
  baustein**: save the feedback entry anyway with empty
  `addresses_bausteine[]` but populated `addresses_arguments[]`.
  Surface as a candidate baustein-to-create later.
- **Multi-baustein-scope mismatch**: a single feedback addresses
  bausteine in different scopes (e.g. a domain baustein + a
  project baustein). Split into multiple feedback entries, one
  per scope, cross-referenced.
- **Multiple authorities cite the same Stellungnahme** (rare,
  e.g. joint Stellungnahme): record one entry with `authority`
  set to the primary, mention secondaries in body.
- **Feedback contradicts an existing approval** (e.g. an
  authority approves an argument in one project but later
  rejects the same argument in another): surface as a
  calibration issue. Don't try to reconcile automatically.
- **Concern decomposition uncertain**: surface to user before
  iterating — "I see N concerns; should I treat them separately
  or as a single block?"

## Tools used

- `list_bausteine(scope?, scope_key?)` (MCP, required) — locate
  candidate addressed bausteine by name + tags.
- `flag_baustein(name, reason)` (MCP, required) — apply
  rejection/partial side-effect.
- `find_bausteine_by_reference(law?, paragraph?, ruling?,
  leitfaden?)` (MCP, optional) — find downstream bausteine
  affected by the same legal claim.
- `search_corpus(query, filter)` (MCP, optional) — per-concern
  baseline fetch + similar-past-Abwägung lookup.
- `read_corpus_file(path)` (MCP, optional) — read full ruling
  text when interpretation matters.

When MCP backend unreachable: fall back to filesystem `Write` for
feedback entry; `Edit` on baustein files directly. Per-concern
cross-referencing via `Grep` instead of `search_corpus`. Warn
user about degraded mode.
