---
name: record-feedback
description: This skill should be used when external feedback (rejection, approval, partial, suggestion) on planning-bureau work needs to be captured. Triggered by user pasting a UNB Stellungnahme, mentioning a Behörden-Reaktion, "UNB hat abgelehnt", "approval kam von <Person>", "Stellungnahme festhalten", "feedback log", "record this rejection", or similar.
version: 0.1.0
license: MIT
---

# record-feedback

Specialist skill for capturing external feedback (rejections,
approvals, partials, suggestions) and propagating effects to
dependent bausteine.

## Load this now

Read `references/format.md` for the feedback entry format —
frontmatter schema, body structure, lifecycle, and side effects on
addressed bausteine.

## When invoked

By user pasting/referencing a Stellungnahme or feedback artifact, or
explicit phrases. Inputs needed:

- **Date** of the feedback (ISO).
- **Authority** — full name (e.g. "UNB Landkreis Rostock"). Derive
  `authority_slug` (kebab-case, e.g. `UNB-rostock`).
- **Project** — project ID.
- **Type** — `rejection`, `approval`, `partial`, or `suggestion`.
- **Phase** — current bauleitplanung-phase if applicable.
- **Content** — the feedback text or excerpt.
- **Source artifact** — path to the original (mail, PDF, snapshot).
  Must be immutable; if pointing at a live working file, refuse and
  ask for a snapshot instead.

If the user just pastes a Stellungnahme, parse the above fields from
content where possible and ask for missing ones.

## Behavior

1. **Parse content** for structure:
   - Identify which arguments are addressed.
   - Detect verdict tone (rejection / approval language).
   - Extract suggested alternatives if mentioned.

2. **Identify addressed bausteine**:
   - Search `memory/universal/<domain>/` for bausteine whose Content
     section matches the addressed arguments.
   - For ambiguous matches, propose candidates to user.
   - Allow explicit user designation if no auto-match.

3. **Compose feedback entry** with full frontmatter per format.md.
   - `addresses_bausteine: []` populated.
   - `addresses_arguments: []` with human descriptions.
   - `verdict_reasoning` and `suggested_alternative` from content.
   - `source_artifact` validated as immutable.

4. **Write to disk** at
   `memory/universal/<domain>/feedback/<YYYY-MM-DD>-<authority-slug>-<topic-slug>.md`.

5. **Apply lifecycle effects** to addressed bausteine:
   - **Rejection / partial**: set `status: flagged`, `flagged_reason: "see <feedback path>"`. Append `{project, date, feedback_path}` to `rejected_uses[]`.
   - **Approval**: append `{project, date, feedback_path}` to `successful_uses[]`. Set `last_validated: <feedback.date>`.
   - **Suggestion**: no auto-flag. Surface as advisory finding next session.

6. **Update domain's `feedback/INDEX.md`** — append row with
   `date | authority | type | project | topic | status | path`.
   Sort by date descending.

7. **Confirm to user** with summary: feedback path, type, and number
   of bausteine affected.

## Output

Confirmation including:
- Path of the saved feedback entry.
- Names of bausteine flagged (for rejections) or marked successful
  (for approvals).
- Suggested next action if applicable (e.g. "Project <name> has a
  rejection feedback open — author successor argumentation?").

## Edge cases

- **Source artifact is a live working file**: refuse to save until
  a snapshot exists. Ask user to make snapshot or point to existing.
- **Feedback addresses arguments without a corresponding baustein**:
  save the feedback entry anyway with empty `addresses_bausteine[]`
  but populated `addresses_arguments[]`. Surface as a candidate
  baustein-to-create later.
- **Multiple authorities cite the same Stellungnahme** (rare, e.g.
  joint Stellungnahme): record one entry with `authority` set to the
  primary, mention secondaries in body.
- **Feedback contradicts an existing approval** (e.g. an authority
  approves an argument in one project but later rejects the same
  argument in another): surface as a calibration issue. Don't try to
  reconcile automatically.

## Tools used (when MCP backend lands)

- Direct filesystem `Write` for feedback entry.
- `list_bausteine(scope, domain)` for matching candidates.
- `flag_baustein(name, reason)` and `archive_baustein(name)` for
  lifecycle effects.

Until backend lands: filesystem `Write` + `Edit` on baustein files
+ `Edit` on INDEX.md.
