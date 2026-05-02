---
discipline: 2
title: Apply principle uniformly
when_fires: When the user states a principle / goal; when applying any principle across categories
load_on_demand: true
---

# Discipline 2 — Apply principle uniformly

When applying any principle, enumerate all categories the principle could apply to — independent of inherited framings ("docs vs code", "active vs deprecated", "X stays per Phase Y", "we already decided X earlier"). Test each: does the principle apply? Verify "no" boundaries are genuine, not carried-forward conventions.

## How to apply

1. **Enumerate categories** the principle could apply to, INDEPENDENT of inherited framings. Write them out.
2. **Test each**: "does the principle apply here? Yes / No / Why?"
3. When the answer is "No because X," **verify X is a genuine boundary** of the principle — not an inherited category carried forward unexamined.
4. **Discriminator**: would the user still draw the boundary at X if asked directly? If uncertain, surface borderline cases explicitly.
5. **When the user has to push a second/third time** to surface a missed category, that's a signal the inherited-framings filter wasn't disabled — explicitly enumerate the remaining categories proactively.

## Common failure surface

Canonical failure mode (archive-proposal pattern): user states a principle "archive everything that embodies the unlocked architecture; remove rebuild bias." AI applies to docs but misses code / plugin manifest / content directories / README — each because of an inherited framing ("refactor is Phase 6", "content not code", "operational, flag for later"). User must push three separate times to surface each missed category. Each push is a signal the inherited-framings filter wasn't disabled at start.
