# Framework state — LOCKED 2026-05-06

## Status

This framework is **LOCKED** as of 2026-05-06 per `drafts/lock-and-park-plan.md` (committed `9e32564` on `lock-and-park` branch). Locked means the framework code, architecture docs, DRs, glossary, MAINTENANCE.md, and VISION.md are FROZEN as a coherent body of work pending evidence from concrete PBS deployment.

This is NOT a permanent lock. It is a sequencing pivot: build PBS deployment concretely first, surface what is actually load-bearing in framework primitives via real-world findings, then resume framework work with concrete evidence rather than abstract speculation.

The pivot was triggered in session 35 by a bildhauer pass that surfaced 9 architectural composition gaps in ~90 minutes — gaps that 14 prior cluster-executions of decision-design-sharpening + coherence-audit + greenfield-rederivation had not caught. The audits were checking sharpness of decisions, not viability of the resulting whole as a deployable system.

## What's locked

- `pbs/` — Python package (Surfaces + reference impls + manifest schemas)
- `arch/` — all ARCH topic docs
- `docs/decisions/` — all DRs
- `glossary/` + `GLOSSARY.md`
- `MAINTENANCE.md`
- `VISION.md`
- `ARCHITECTURE.md`
- `DISCIPLINES.md`

## What's allowed during lock

Edits to locked files ONLY for:
- Bug fixes (typos, broken imports, mypy or test failures)
- Doc clarifications that do not change architectural commitments
- Capturing new findings from PBS work in this doc + `findings-from-pbs.md`

NOT allowed during lock:
- New ARCH topic locks
- New Mode 2 reference impl additions
- New Mode 3 spec additions
- Refactoring shape impls (`pbs/impls/practitioner_shape_*.py`)
- Decisions about deferred questions (multi-shape composition, hybrid-shape, engagement-target promotion, etc.)

If something feels like it crosses the line, surface it for explicit approval rather than acting.

## Known questionable points (parked, not solved)

These are load-bearing architectural gaps surfaced in session 35 bildhauer pass. PBS deployment will tell us which are real architectural issues vs theoretical concerns.

1. **Single-shape-per-workspace forces wrong fit for multi-archetype organizations.** Per `pbs/manifests/workspace.py:208`, workspace.shape is single-value. A planning firm doing client deliverables + business ops + maybe personal workflow currently has to pick one shape; any choice mis-fits the other two.

2. **Specialist `shape_compatibility` is a coarse boot-time check, not runtime policy resolution.** Per `arch/specialist-skill.md:97`, specialist declares list of compatible shapes. Boot validates workspace.shape ∈ specialist.shape_compatibility. But all activated specialists then run under workspace.shape's policies regardless of which specialist they came from.

3. **Engagement-target entity catalog conflicts across shapes.** Per `arch/scope-model.md:321-323`, engagement-target is per-shape mandated: practitioner-shape → Client, autonomous-business → Customer. The SAME real entity (a municipality being Client AND Customer) needs two framework representations if a workspace hosts both shapes.

4. **Hybrid-shape escape hatch is named in glossary but undefined.** Per `glossary/shape.md:33`, `hybrid-shape — combinations of above` is in the catalog. But no arch topic locks structural mechanics. It's a placeholder, not a working architecture.

5. **Per-shape policy variation 6-row matrix in scope-model §8 doesn't have a column for "what if multiple shapes apply".** Per `arch/scope-model.md:321-328`, the matrix assumes mutually-exclusive shape selection. There is no row for "multiple-shape composition policy."

6. **Boot sequence assumes single shape.** Per `arch/scope-model.md:147`, substrate-phase 5 loads "engagement-target entity per shape policy" (singular). Boot composition for multi-shape workspaces is not articulated.

7. **Specialist instance content boundary unclear when specialist's natural shape ≠ workspace's selected shape.** A specialist designed for autonomous-business-shape (e.g., invoicing) deployed in practitioner-shape workspace — what does its instance content look like? Customer entities (its native vocab) or Client entities (workspace mandate)? Per `arch/specialist-skill.md:319`, "entities owned by deployed specialist instance live at Owner B per that specialist's namespace" — so it would own Customer-shaped entities even though workspace mandates Client. Two parallel engagement-target entity sets.

8. **Pattern-vs-instance discipline strain on `pbs/impls/practitioner_shape_*.py` impls.** Per `MAINTENANCE.md:179` (pattern-vs-instance): "PBS-Schulz pioneer-instance specifics... live at workspace level." But the practitioner_shape impls in `pbs/impls/` ENCODE policy values that PBS-Schulz happens to need. Are these "framework primitive definitions" (must stay shape-neutral per pattern-vs-instance) or "shape policy bundles realized as code" (Framework C distributables per `glossary/shape.md`)? The discipline language doesn't carve this out cleanly.

9. **Non-session-initiated work has no articulated practitioner-binding mechanism.** Per `arch/practitioner.md:104`, practitioner binding is at session-open via `session.bound_practitioner_id`. Scheduled tasks, AI-proactive monitoring, autonomous workflows that emit events requiring HUMAN actor have no clear binding.

## Other expected shortcomings

- **CLAUDE.md TOP-LEVEL SCOPE summary contradicts MAINTENANCE.md + glossary** on whether specialist DEFINITIONs and per-shape policy bundles are framework-side. Resolution per session 35: glossary is canonical (they ARE Framework C distributables); CLAUDE.md was over-restrictive in summary. Do not blindly trust CLAUDE.md TOP-LEVEL SCOPE wording — read MAINTENANCE.md TOP-LEVEL SCOPE for canonical text.

- **"Shape" as currently locked conflates ~6 dimensions** (governance policies + engagement-target catalog + Layer A defaults + specialists activation policy + workspace.md required fields + substrate selection constraints). Conflation may be the deepest leverage point if framework work resumes; deferred until PBS evidence demands.

## Deferred questions (parked, not parked permanently)

- How shape composition works (if at all) for multi-archetype organizations
- Whether "shape" is one cohesive thing or N orthogonal things glued together
- Whether engagement-target should be its own first-class primitive
- Cross-deployment claim portability mechanics
- Federation primitives
- Multi-tenant + multi-environment workspace mechanics
- "Framework-from-scratch builder" skill idea (user-deferred until PBS deployment milestone 3-4; possibly composes with `clippy` skill set; do NOT explore until PBS deployment scope locked down)

## Reopen criteria

Framework work resumes when ANY of:

- **Trigger A — PBS first-useful-state**: PBS deployment is producing real B-Plan-Begründung successfully (or equivalent first useful work product), AND has been used for ≥4 weeks. Signals concrete patterns are starting to appear.
- **Trigger B — finding count**: ≥5 framework-blocking findings accumulated in `findings-from-pbs.md` (definition of "blocking" in that file).
- **Trigger C — explicit user trigger**: user decides framework concerns warrant attention regardless of triggers A/B.
- **Trigger D — second deployment intent**: someone (you or other) starts authoring a second deployment that is NOT planning-firm shape. Forces shape-neutrality validation.

Reopen does NOT mean restart. It means a structured review session with PBS evidence in hand, deciding which questionable points to address now and which to keep parked.

## How findings get captured

Findings from PBS deployment work that touch framework areas get logged in `findings-from-pbs.md`. See that file for format and severity definitions.

## Cross-references

- Plan: `drafts/lock-and-park-plan.md`
- Plan commit: `9e32564` on `lock-and-park` branch
- Findings aggregator: `findings-from-pbs.md`
- Lock pivot HANDOFF Note 82
- PBS-deployment repo: `pbs-bureau-deployment` (not yet created; first action when deployment work session begins)

## Lifecycle of this doc

- Updated when: PBS finding accumulates that should be mirrored here for visibility
- Updated when: reopen trigger fires (status changes to "Lock under review")
- Updated when: questionable point gets resolved (move to "Resolved" section)
- NOT updated for routine PBS deployment work (that lives in `findings-from-pbs.md`)

## Resolved questionable points

(none yet — populate when reopen + resolution happen)
