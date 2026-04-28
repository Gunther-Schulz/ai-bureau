---
name: record-feedback
description: This skill should be used when external feedback (rejection, approval, partial, suggestion) on PBS work needs to be captured. Triggered by user pasting a UNB Stellungnahme, mentioning a Behörden-Reaktion, "UNB hat abgelehnt", "approval kam", "Stellungnahme festhalten", or similar.
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
explicit phrases like "record this feedback", "log the rejection",
"festhalten".

## Behavior

1. Parse feedback content for type, addressed arguments, reasoning.
2. Identify addressed bausteine (match by argument or explicit name).
3. Compose feedback entry with full frontmatter.
4. Write to `memory/domain/<domain>/feedback/<YYYY-MM-DD>-<authority>-<topic>.md`.
5. Apply lifecycle effects to addressed bausteine:
   - `rejection` / `partial` → `status: flagged`, `flagged_reason: <this entry>`
   - `approval` → append to `successful_uses[]`, set `last_validated: feedback.date`
   - `suggestion` → no auto-flag; surface as advisory finding
6. Update domain's `feedback/INDEX.md`.
7. Confirm to user.

## Status

v0.1: stub. Format reference is complete; behavior implementation
follows when MCP tool surface lands.
