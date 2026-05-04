---
discipline: 4
title: Cascade prevention (greenfield-draft + minimize-embedded + cascade-pass + foundation-first)
when_fires: When locking a new architectural commitment that depends on or composes with prior work (GLOSSARY entries, DRs, ARCH topics, specs, layered design)
load_on_demand: true
---

# Discipline 4 — Cascade prevention

When locking a new architectural commitment that depends on or composes with prior work:

1. **Greenfield-draft from primary sources** (VISION, locked architectural commitments in MAINTENANCE.md, first principles) — NOT from prior cross-references as anchors.

2. **Minimize embedded descriptions of not-yet-locked terms** — use brief role tags + cross-ref to authoritative source; don't carry the not-yet-locked term's full definition inline.

3. **Cascade-pass after locking — at lock-TIME, NOT deferred** — before committing the lock of a new term, run **two greps** at lock-time:

   - **Within-cluster**: `git grep "<term> .*forthcoming" --` for the term being locked — find stale forward-references now resolved.
   - **Cross-corpus**: `git grep -l "(forthcoming)" glossary/ arch/` + `git grep -nE "Phase [0-9]\.[0-9]+ forthcoming|placeholder until Phase|canonical entry forthcoming" glossary/ arch/` — detect placeholder framings of OTHER terms the just-locked work now makes citable (cross-cluster carryovers; cross-phase carryovers from prior phase-set persisting into current one).

   Update placeholders → LOCKED links in same commit. Per `MAINTENANCE.md` "How to find cascades" step 5.

   **Recurring failure mode**: cascade-pass deferred → stale forthcoming markers accumulate → next sharpening round catches them but they've already polluted the corpus. The within-cluster grep alone does not catch cross-cluster + cross-phase carryovers; the two-grep pair does.

4. **Lock foundation-first when sequence has discretion** — when multiple entries could be locked next, prefer the most foundational (most cross-referenced; most-composed-against). Bottom-up locking matches the architecture's compositional structure: derived terms compose on foundational ones. Inverse direction creates churn (every foundational lock cascades through many prior derived entries) and bias (foundationals get drafted against speculative cross-refs already established by derived entries).

## Origin

Originated in GLOSSARY entry-by-entry workflow during the foundational rebuild; generalizable to any architectural locking work where prior entries forward-reference not-yet-locked terms.
