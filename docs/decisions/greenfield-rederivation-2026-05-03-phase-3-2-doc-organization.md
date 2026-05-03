# Greenfield-rederivation execution — Phase 3.2 doc-organization composite DRs cluster

## Status

PROPOSED. Cluster definition + Wave decomposition persisted. Writer wave not yet dispatched.

Audit-pattern: greenfield-rederivation v0.1.0 (`plugin/skills/greenfield-rederivation/SKILL.md`). Per-cluster scope; per-artifact Writer + Reviewer sub-agent dispatch; tiered-divergence verdict scheme; user-decision per divergence.

## Owner

Phase 3 audit family (greenfield-rederivation skill execution; cluster scope). Doc-organization cluster (META work — composite DRs deciding HOW the corpus is organized; not architectural-content primitives).

## Related

- Audit-pattern source: `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0
- Prior cluster execution (HISTORICAL INPUT only; not authoritative for this execution): `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-1-drs.md` (Phase 3.1 4 DRs cluster; ACCEPTED-WITH-FINDINGS)
- v1 procedure DR (HISTORICAL INPUT only; not authoritative): `docs/decisions/greenfield-rederivation-pause.md` (SUPERSEDED)
- Cluster artifacts under audit:
  - `docs/decisions/phase-3-2-doc-organization.md` (composite — 4 sub-decisions: taxonomy / naming / cross-cutting placement / ARCHITECTURE.md structure)
  - `docs/decisions/doc-organization-templates.md` (composite — arch/<topic>.md template + DR template + memory consolidation rules)
- Composes-with disciplines (`DISCIPLINES.md`):
  - Discipline 1 (source-grounded; skill+profile sub-section)
  - Discipline 6 (foundation-up ordering; complementary to doc-organization decisions)
  - Discipline 9 (coherence-audit cadence; greenfield-rederivation runs at same checkpoint windows)
  - Discipline 10 (greenfield evaluation of archived material; this skill is the per-cluster orchestrated procedure)
- Anchor sources for greenfield derivation (META work — derivation traces through first-principles disciplines, not directly through VISION axes):
  - `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE (framework=mechanisms / shape=policies; A-B-C scope model)
  - `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §§1/2/3
  - `MAINTENANCE.md` 5-layer doc model (Layer 0 anchors / Layer 1 GLOSSARY / Layer 2 ARCHITECTURE / Layer 3 arch topics / Layer 4 DRs / Layer 5 specs)
  - `MAINTENANCE.md` cascade discipline + provenance-hygiene meta-home rule
  - `coherence-audit` Lens 5 v0.2.1 (provenance hygiene) + Lens 8 (pattern-vs-instance) + Lens 9 (VISION-grounding through first-principles transitive chain)
  - `VISION.md` (anchor for axes; doc-organization decisions trace transitively through MAINTENANCE first-principles which themselves serve VISION)
- Profile-cluster coverage planned per artifact: see Sharpening provenance §Wave-1 dispatch table

## Context

The 2 Phase 3.2 doc-organization composite DRs were locked under the same cascade-load conditions identified as a META-failure surface (single-AI execution; oversized mandatory load; cascade-mode adherence collapse). They were both produced before Lens 5 v0.2.1 codification (provenance hygiene) was lifted to first-class discipline status; phase-3-2-doc-organization predates Lens 5 v0.2.1 entirely; doc-organization-templates explicitly references Lens 5 v0.2.1 in its Decision body but was itself produced under cascade-load conditions.

Doc-organization is META work: these DRs decide HOW the corpus is organized (topic taxonomy / naming / placement / templates / memory consolidation), not WHAT primitives exist. Greenfield derivation traces through `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE + 5-layer doc model + first-principles design principles + DISCIPLINES, not directly through VISION axes (the linkage is transitive: VISION serves practitioner outcomes; MAINTENANCE first-principles preserve practitioner outcomes via doc-system shape; doc-organization decisions instantiate MAINTENANCE first-principles).

Cluster choice rationale (per skill §When-to-use cluster examples):
- **Foundation-second**: Phase 3.1 closure was foundational architectural questions; Phase 3.2 closure was foundational doc-system organization. Phase 3.2 sits one layer above Phase 3.1 in foundation-up ordering; auditing it after Phase 3.1 is consistent with Discipline 6 (foundation-up).
- **Smallest-eligible cluster**: 2 composite DRs fits 1 Wave parallel-dispatch comfortably.
- **High-load-bearing-error risk**: doc-organization decisions cascade across the entire corpus. Topic taxonomy decides what arch/* files exist; DR template decides what shape every DR takes; arch template decides what shape every Pattern A protocol topic takes; memory consolidation rules decide what stays in memory vs absorbed-into-DR. Drift in any of these cascades multiplicatively.

What this audit aims to surface (per skill §Reviewer brief — 4 lenses, applied in META context):
- **Pattern-vs-instance leakage**: do these DRs embed PBS-Schulz / DACH-EU / regulatory-instance assumptions in framework-level doc-organization claims?
- **VISION-grounding (transitive)**: does each doc-organization claim trace through MAINTENANCE first-principles disciplines back to VISION axes? META work doesn't trace directly to VISION; intermediate first-principles must be cited explicitly.
- **Provenance hygiene**: do canonical sections (Decision / sub-decisions / templates) contain narrative breadcrumbs ("session N", "AMENDED session N", "as of <date>") that should live in HANDOFF + git log + §Sharpening provenance?
- **Cascade-miss**: are cross-references between the 2 DRs symmetric (each cites the other where dependency exists)? Does doc-organization-templates correctly cascade from phase-3-2-doc-organization (which it depends on for taxonomy + naming)?

## Decision

Pre-execution. Per-artifact verdicts + tiered findings populated post-Wave-1.

### Headline result

(Pending Wave-1 + Reviewer wave + main-session aggregation.)

### Per-artifact verdict table

(Pending.)

### Position commits per divergence

(Pending Reviewer wave + main-session position commitment per `feedback_judgment_and_automate.md`.)

### Verdict scheme reference (per skill §Verdict scheme)

| Per-artifact verdict | Meaning |
|---|---|
| GREENFIELD-VALID | Locked content passes greenfield-derivation chain |
| INPUT-ONLY-VALID | Archive/prior is INPUT not TEMPLATE; greenfield-chain holds |
| NEEDS-REVISION | Specific revision identified |
| NEEDS-REWORK | Substantial redo required |

Tier:
- T1 framework-shape-changing (cascades) | T2 topic-rewriting | T3 mechanical edit | T4 confirms-locked

User-decision verdict per divergence: REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED.

## Sharpening provenance

### Wave decomposition

| Wave | Artifacts | Parallelism | Foundation-up dependency |
|---|---|---|---|
| 1 | phase-3-2-doc-organization.md / doc-organization-templates.md | 2 Writers in parallel + 2 Reviewers in parallel | None within cluster — each Writer derives from MAINTENANCE first-principles + 5-layer model + DISCIPLINES + GLOSSARY substrate independently. Cross-DR dependency (templates DR depends on taxonomy DR) lives in MAINTENANCE Layer-3 description + DR-template convention; each derivation runs from primitives. |

Cluster within skill's stated 2-6 artifact / 3-4 parallel sweet spot per `plugin/skills/greenfield-rederivation/SKILL.md` §When-to-use + §Per-Wave step 1.

### Wave-1 Writer dispatch table (planned)

| Artifact | Writer brief profile-cluster coverage | Required reads (skill §Writer brief — adapted for META work) |
|---|---|---|
| phase-3-2-doc-organization.md | A Producers (L1 specialist creator + L2 shape definer + L3 deployment template creator) + D Validators (G + L8) — doc-organization decisions cascade into producer-side artifact structure (Pattern A protocol topics; primitive-cluster topics) + validator-side audit-trail meta-home (DR provenance) | VISION + MAINTENANCE TOP-LEVEL ARCHITECTURE + 5-layer doc model + TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 + cascade discipline + GLOSSARY index + DISCIPLINES Discipline 1 + Discipline 6 + Discipline 9 + Discipline 10 + profiles/INDEX.md + L1 + G + L8 + L4a |
| doc-organization-templates.md | A Producers (L1 + L2 + L3) + D Validators (G + L8) — template decisions cascade into every produced ARCH topic + every DR + memory-vs-DR placement | VISION + MAINTENANCE TOP-LEVEL ARCHITECTURE + 5-layer doc model + TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 + cascade discipline + Lens 5 v0.2.1 provenance hygiene + GLOSSARY index + DISCIPLINES Discipline 1 + Discipline 6 + Discipline 9 + Discipline 10 + profiles/INDEX.md + L1 + G + L8 + L4a |

Each Writer brief explicitly excludes reading the artifact under audit during derivation + excludes reading the peer cluster artifact + excludes reading v1 findings (greenfield-rederivation-pause.md) + excludes reading prior v2 cluster findings (greenfield-rederivation-2026-05-03-phase-3-1-drs.md). Per skill §Sub-agent brief template — greenfield-Writer "DO NOT READ during derivation".

### Wave-1 Reviewer dispatch table (planned)

| Artifact | Reviewer brief inputs | 4 lenses applied |
|---|---|---|
| phase-3-2-doc-organization.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Pattern-vs-instance leakage / VISION-grounding (transitive through first-principles) / provenance hygiene / cascade-miss |
| doc-organization-templates.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Same 4 lenses (Lens 5 self-application — does this DR's own canonical content satisfy the provenance-hygiene rule it codifies?) |

### Wave-1 dispatch summary (executed)

(Pending.)

### Per-sub-agent Ralph self-check verification (per skill §Termination criteria)

(Pending; populated as sub-agents return.)

### Decomposition mode

Mode 2 upfront-known composite (per `decision-design-sharpening` v0.6.0): 2 tightly-coupled doc-organization composite DRs identified at cluster definition time (not emergent from drift). Both Phase 3.2-era; both composite Mode-2 sub-decision DRs themselves; both subject to same META-failure-surface conditions.

## Composition with existing architecture

- **Coherence-audit composition**: this audit catches per-artifact derivation drift / cargo-cult / instance-leakage / cascade-miss in doc-organization decisions; coherence-audit catches set-level + vocabulary-level + cascade-level drift via 10 universal lenses. Both compose at phase boundaries (per skill §Composition with other PBS dev skills). This execution is per-cluster (greenfield-rederivation territory); set-level lens scan over the whole doc-system would compose as separate coherence-audit invocation.
- **Cascade discipline**: any user-approved REVISE-LOCKED divergence triggers cascade per `MAINTENANCE.md` TOP-LEVEL RULE (UPSTREAM + DOWNSTREAM + SIDEWAYS); cascade execution itself delegated to fresh-context sub-agent per `CLAUDE.md` M3.
- **Phase 3 sub-phase status**: Phase 3.2 marked CLOSED in `ARCHITECTURE.md` §2 with composite DR amended per v1 procedure cascade (Pattern A catalog 14→11; Pattern A protocol catalog 8→3; sparring + audit reclassified as mechanism classes; coordination + trust + time cancelled). This v2 audit re-tests that closure under sub-agent + Writer-Reviewer orchestration to surface any drift the original closure + amendment cascade missed under cascade-load conditions.
- **v2 skill empirical-evidence accumulation**: this is the second cluster-execution of v2 greenfield-rederivation skill v0.1.0. Per skill §Status (preliminary-locked at v0.1.0; ≥2 cluster-executions threshold for amendment), completion of this execution moves the skill from single-execution-evidence to two-execution-evidence — the empirical threshold for skill v0.1.1 amendment review.

## Constraints flowing to downstream commitments

(Pending user-reconciliation per divergence.)

## Files touched

- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-2-doc-organization.md` (this DR — to be created PROPOSED → Wave-1 findings persisted → user-reconciled → cascade-completion + status transition to ACCEPTED-WITH-FINDINGS or ACCEPTED-VALIDATED)
- (Pending; cluster artifacts touched only if user approves REVISE-LOCKED / AMEND-LOCKED divergences)

## Revisit triggers

- New artifact added to Phase 3.2 cluster (none expected; Phase 3.2 closed)
- Stable-corpus signal: if 0 NEEDS-REVISION + 0 NEEDS-REWORK across all 2 artifacts (only T4-confirms-locked findings) → cluster greenfield-stable; cadence shifts to delta-audits per `coherence-audit` audit-scaling
- User-flagged drift on cluster artifact post-execution (e.g., new evidence surfaces during Phase 3.5 or 3.6 work that contradicts Phase 3.2 lock)
- Phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` (e.g., Phase 3.4 close C1 audit may compose with this re-audit)
- Lens 5 v0.2.1 amendment OR new provenance-hygiene rules emerge — re-audit doc-organization-templates against amended discipline (the DR's own canonical content must self-satisfy)
