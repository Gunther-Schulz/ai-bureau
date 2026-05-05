---
discipline: 3
title: Pre-decision sharpening
when_fires: At decision-formation moments before locking; before architectural commitments persist; primitive classification proposals (multi-axis sub-section); high-impact decisions (profile-anchored sub-section)
load_on_demand: true
---

# Discipline 3 — Pre-decision sharpening

At decision-formation moments, run sharpening rounds BEFORE locking:

- **Round 1** = full monty (proactive comprehensive — stress-tests + edge cases + counter-arguments engaged; Pareto-disciplined; reject manufactured criticism)
- **Round 2+** = USER-TRIGGERED (external-perspective friction; AI-self-triggered rounds drift toward manufactured criticism)

## Why pre-decision outperforms post-mortem audits (5 mechanisms)

1. **Anchoring bias**: post-mortem looks at WHAT IS; pre-decision can explore WHAT COULD BE
2. **Sunk-cost protection**: post-decision reviewers protect existing investment; pre-decision has no sunk cost
3. **Sparring vs validation mode**: sharpening = SPARRING (challenge); audits = VALIDATION (confirm). Per Vivienne Ming research: sparring outperforms validation
4. **Fresh-context advantage**: design context is hot during sharpening; cold during audits
5. **Greenfield-still-anchored problem**: even greenfield checks ("would we build this from scratch?") look AT existing shape; pre-decision sharpening generates alternatives directly

## Sweet spot per surface type

- **ARCHITECTURAL-DECISION**: 2-3 rounds; expected decay 6→5→3→0-1
- **PROCEDURE-DOCUMENT** (process docs / methodology): density-check governs; sweet spot may be 4-5 rounds
- **SET-LEVEL AUDIT** (corpus-level): per-cluster density; rounds continue until cluster exhausted
- **META-ARCHITECTURAL** (foundational discipline / framework rebuild): user-trigger primary

Pattern-matching architectural-decision decay onto procedure-document or set-level audit = recurrent bias. **Empirical density check mandatory at every round termination** (count substantive findings current vs previous; ≥50% drop = decay confirmed). Decomposition trigger (Round 4+ signals decomposition missing) applies to ARCHITECTURAL-DECISION surface only.

## Two-phase pattern

- **Decision-design phase**: 2-3 rounds at decision-formation moment; architectural-decision lock
- **Pre-implementation phase**: additional rounds at implementation-start moment; operational/runtime details + ~10-20% architectural flow-back as DR amendments

## Layered coverage observation

Each round emphasizes (but doesn't exclusively cover) different concern layer:

- Round 1 = architectural decisions (what methods + types + abstractions)
- Round 2 = cross-cutting + schema details (boot, errors, transport, tier-awareness, audit integration)
- Round 3 (optional) = additional architectural patterns (broad surface only)
- Round 4+ → defer to Phase 2 pre-implementation (operational/runtime concerns)

## Decomposition triggers

- **Mode 1 emergent**: if a decision genuinely needs >3 rounds at decision-design phase → decompose into sub-decisions; each gets standard 2-3 rounds.
- **Mode 2 composite decomposition** (upfront-known; per `decision-design-sharpening` v0.6.0): when 3+ tightly-coupled sub-decisions visible at framing time with foundation-up dependencies, decompose upfront: sub-decision inventory → foundation-up ordering → per-sub-decision 2-round sharpening → final synthesis pass → composite DR.

## Skills implementing this discipline

- `plugin/skills/decision-design-sharpening/` (Phase 1 decision-formation)
- `plugin/skills/pre-implementation-sharpening/` (Phase 2 implementation-start)
- `plugin/skills/sharpen/` (generic critical-pass)
- `plugin/skills/coherence-audit/` (post-decision corpus-set audit)

## Multi-axis validation for primitive proposals

When proposing or refining a primitive's classification / scope / applicability claim, validate across three orthogonal dimensions — single-axis validation misses gaps:

1. **Archetypes** — does primitive work for planner / lawyer / researcher / auditor / consultant / etc.?
2. **Work-types within an archetype** — does primitive work for codified workflow / ad-hoc exploratory / one-off communication / research-mode / maintenance / learning?
3. **Roles** — does primitive work for practitioner / workflow-designer / specialist-author / instance-deployer / AI-runtime / multi-user-collaborator / auditor-reviewer?

**Plus explicit non-coverage question**: "what use cases does this primitive NOT cover, and is that intentional or a gap?"

Single-axis validation creates blind spots. Cross-archetype illustration with constant work-type = "codified workflow" makes codified case look universal when ad-hoc work is also first-class.

## Profile-anchored validation

For high-impact decisions (primitive classifications; per-mechanism / per-protocol / per-primitive-detail design — Phase 3.3-3.6 territory), test against ≥3 of 4 profile-clusters in `profiles/INDEX.md`:

- Cluster A Producers (L1+L2+L3+L9)
- Cluster B Deployers (L4a+L4b+L5a)
- Cluster C Consumers (L5a-L5j+L5e+L5f)
- Cluster D Validators (L8+G+D gates)

Flesh skeleton-profile if specific decision affects it (per `coherence-audit` on-demand fleshing). For routine decisions or cascade-from-established-pattern, multi-axis principle-level check sufficient. Discriminator: shape-specific or instance-specific surface → profile-anchored; purely structural cascade → multi-axis principle-level.

## Mode 3 spec writing — routine-cascade default (Phase 6.1)

Mode 3 Pydantic Protocol specs operationalize already-locked ARCH topic Surface contracts (purely structural cascade per the profile-anchored discriminator above). **No default sharpening fire per spec**; spec writing is content-phase mechanical work. `decision-design-sharpening` + `pre-implementation-sharpening` skills fire on-demand only when an unexpected substantive decision surfaces (cardinality not implied by ARCH; ambiguous Pydantic shape between valid alternatives; schema choice forces not-yet-locked architectural commitment). Default = direct schema-writing per `MAINTENANCE.md` Procedure-rigor discipline subsection → per-shape application Mode 3 row.
