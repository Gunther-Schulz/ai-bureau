---
discipline: 10
title: Greenfield evaluation of archived material
when_fires: ARCH topic / DR / spec work cites archived material (`archive/docs/decisions/*` / `archive/extensions/*` / archived ARCHITECTURE / etc.); Round 1 sharpening surfaces archive citation; Round 2 termination self-check
load_on_demand: true
---

# Discipline 10 — Greenfield evaluation of archived material

When ARCH topic / DR / spec work cites archived material (`archive/docs/decisions/*` / `archive/extensions/*` / archived ARCHITECTURE / etc.), each cited element MUST be greenfield-evaluated against current locked vocabulary — NOT transcribed as template.

## Why

Archive embodies pre-rebuild architectural commitments — much of which was unlocked / instance-anchored / contradiction-bearing per the foundational-rebuild rationale. Cargo-cult adoption of archived elements re-introduces the failure modes the rebuild was designed to fix. Per `MAINTENANCE.md` rebuild context: "the prior v0.35 corpus grew beyond easy handling... contained internal contradictions... arose because cascade discipline was implicit."

## Failure surface (canonical case)

`arch/coordination.md` Round 1 cargo-cult'd archived event-coordination protocol (capability categories + 3 failure modes + no-direct-call discipline directly transcribed) without explicit greenfield-evaluation per element. User caught the drift.

## Discriminator (per cited archived element)

- Was element re-validated against locked GLOSSARY entries that exist NOW (not the v0.35 vocabulary)?
- Was element stress-tested against profile clusters in current `profiles/INDEX.md`?
- Pattern-vs-instance check: does archived element embed pioneer-instance / archetype-instance / regulatory-instance assumptions that current architecture rejected?
- Greenfield derivation: would we design THIS element THIS WAY today, ignoring archive?

If any check yields NO → element needs revision OR archive-citation is INPUT-ONLY (informs current design but doesn't transfer structure directly).

## How to apply

1. **At Round 1 sharpening**, when archive citation considered: surface the cited element + greenfield-evaluation result per criterion above. NOT "per archived X" as terminating evidence.
2. **At Round 2 sharpening termination**, run greenfield-citation self-check: every "per archived X" claim → was X greenfield-evaluated, or transcribed?
3. **Coherence-audit Lens 5 v0.2.1 provenance hygiene** extends: ARCH topics + DRs hold greenfield-evaluated content; archive citations live in §16 "Decision-design provenance" sections naming SOURCE (where input came from), NOT TEMPLATE (where structure transferred).

## Recognition-pattern bias

Stress-testing pressure DECREASES when archived material "fits" the topic shape — exactly when greenfield-evaluation is MOST important (high archive-fit = highest cargo-cult risk). Counter-bias: when archive seems to fit well, increase stress-testing rigor.

## Composition

- Per Discipline 1 source-grounded rule extended to archive (archived material is a source class; cite specifically; flag synthesis vs citation; greenfield-evaluation is the synthesis-not-citation step).
- Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 preliminary-lock: archived "locked" decisions are NOT preliminary-locked relative to current rebuild — they're archived UNlocked (rebuild rejected v0.35 corpus at launch). Greenfield evaluation re-establishes locked status.
