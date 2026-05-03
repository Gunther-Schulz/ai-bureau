# Greenfield-rederivation execution — Phase 3.1 4 DRs cluster

## Status

PROPOSED → (will transition to ACCEPTED-VALIDATED or ACCEPTED-WITH-FINDINGS at user-reconciliation phase per skill §Post-cluster).

Audit-pattern: greenfield-rederivation v0.1.0 (`plugin/skills/greenfield-rederivation/SKILL.md`). Per-cluster scope; per-artifact Writer + Reviewer sub-agent dispatch; tiered-divergence verdict scheme; user-decision per divergence.

## Owner

Phase 3 audit family (greenfield-rederivation skill execution; cluster scope). Foundation-first cluster (smallest cluster; high-load-bearing-error risk if any).

## Related

- Audit-pattern source: `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0
- Predecessor (HISTORICAL INPUT only; not authoritative): `docs/decisions/greenfield-rederivation-pause.md` (v1 procedure DR; SUPERSEDED)
- Cluster artifacts under audit:
  - `docs/decisions/workflow-bipartite-classification.md`
  - `docs/decisions/work-unit-bipartite-classification.md`
  - `docs/decisions/deployment-derived-classification.md`
  - `docs/decisions/engaged-authorship-operational-definition.md`
- Composes-with disciplines (`DISCIPLINES.md`):
  - Discipline 1 (source-grounded; skill+profile sub-section)
  - Discipline 9 (coherence-audit cadence; greenfield-rederivation runs at same checkpoint windows)
  - Discipline 10 (greenfield evaluation of archived material; this skill is the per-cluster orchestrated procedure)
- GLOSSARY entries treated as derivation substrate (Anchor): `mechanism`, `policy`, `framework`, `shape`, `Framework C scope`, `Owner B scope`, `Layer A scope`, `workspace`, `substrate`, `specialist`, `skill`, `practitioner`, `session`, `workflow`, `work-unit`, `claim`, `defensibility`, `engaged authorship`, `deployment`, `pioneer instance`, `event`, `actor`, `protocol (architectural)`, `quality-gate`, `rubber-stamping`, `sparring (axis 2)`, `authorship preservation (axis 3)`
- Profile-cluster coverage planned per artifact: see Sharpening provenance §Wave-1 dispatch table

## Context

The 4 Phase 3.1 DRs were locked under cascade-load conditions identified as a META-failure surface (single-AI execution; oversized mandatory load; cascade-mode adherence collapse). Tier-1 findings during the v1 procedure execution (Pattern A catalog 8→3; template restructure 18→12+6) confirmed that prior architectural work HAD errors detectable by foundation-up re-derivation; the v1 procedure was itself executed under the same cascade conditions, leaving its verdicts partially self-praise-biased (single-agent Writer + Judge).

The audit pattern (re-derive each DR from primitives in isolation; compare to locked content; surface divergences) was correct in v1; the orchestration shape (single-agent under cascade-load) was the META-failure surface. v2 corrects orchestration via per-cluster scope + per-artifact sub-agent dispatch + Writer-Reviewer separation per `CLAUDE.md` Cascade discipline M3+M4.

Cluster choice rationale (per skill §When-to-use cluster examples):
- **Foundation-first**: Phase 3.1 closure was the foundational architectural-question wave; everything in Phase 3.2-3.4 composes downstream. If primitive classifications here drifted from VISION/GLOSSARY-derivation, downstream drift cascades.
- **Smallest cluster**: 4 artifacts fits 1 Wave parallel-dispatch sweet spot.
- **High-load-bearing-error risk**: Pattern B classifications (workflow / work-unit) + DERIVED meta-concept (deployment) + DERIVED axis-3 success mode (engaged-authorship) — each touches multiple downstream artifacts.

What this audit aims to surface (per skill §Reviewer brief — 4 lenses):
- **Pattern-vs-instance leakage**: do locked DRs embed PBS-Schulz / DACH-EU / regulatory-instance assumptions in framework primitive content?
- **VISION-grounding**: does each claim trace to VISION axes / GLOSSARY primitives / first-principles disciplines?
- **Provenance hygiene**: do canonical sections contain narrative breadcrumbs that should be in HANDOFF + git log?
- **Cascade-miss**: are cross-references / composes-with claims symmetric with cited entries?

## Decision

(POPULATED AS WAVES COMPLETE)

Per-artifact verdict + tier per divergence + user-decision per divergence will land here after Wave-1 completes + user-reconciliation phase. Currently empty per Status PROPOSED.

Verdict scheme (per skill §Verdict scheme):

| Per-artifact verdict | Meaning |
|---|---|
| GREENFIELD-VALID | Locked content passes greenfield-derivation chain |
| INPUT-ONLY-VALID | Archive/prior is INPUT not TEMPLATE; greenfield-chain holds |
| NEEDS-REVISION | Specific revision identified |
| NEEDS-REWORK | Substantial redo required |

Tier (for NEEDS-REVISION + NEEDS-REWORK):

| Tier | Meaning |
|---|---|
| T1 | Framework-shape-changing (cascades; multiple artifacts) |
| T2 | Topic-rewriting (substantive single-artifact rewrite) |
| T3 | Mechanical edit (localized fix) |
| T4 | Confirms-locked (no revision; tracks completeness) |

User-decision verdict per divergence (post-Reviewer):
- REVISE-LOCKED — apply revision per Reviewer recommendation; cascade
- KEEP-LOCKED — locked content stands; Reviewer divergence rejected
- AMEND-LOCKED — partial application; specific amendment differs
- SUPERSEDE-LOCKED — locked artifact superseded by new artifact

## Sharpening provenance

### Wave decomposition

| Wave | Artifacts | Parallelism | Foundation-up dependency |
|---|---|---|---|
| 1 | workflow-bipartite-classification.md / work-unit-bipartite-classification.md / deployment-derived-classification.md / engaged-authorship-operational-definition.md | 4 Writers in parallel + 4 Reviewers in parallel | None within cluster — each Writer derives from VISION + locked GLOSSARY (which already includes all 4 entries as derivation substrate) + MAINTENANCE first-principles + DISCIPLINES; cross-DR concept relations (work-unit always-present ↔ workflow optional-overlay asymmetry; engaged-authorship → claim/sparring/defensibility composition) live in GLOSSARY entries, so each derivation runs independently |

Cluster within skill's stated 2-6 artifact / 3-4 parallel sweet spot per `plugin/skills/greenfield-rederivation/SKILL.md` §When-to-use + §Per-Wave step 1.

### Wave-1 Writer dispatch table (planned)

| Artifact | Writer brief profile-cluster coverage | Required reads (skill §Writer brief) |
|---|---|---|
| workflow-bipartite-classification.md | A Producers + B Deployers + C Consumers + D Validators (primitive-set-shaping) | VISION + MAINTENANCE §§1/2/3 + GLOSSARY index + workflow / work-unit / specialist / session / claim / event / intertwining glossary entries + DISCIPLINES Discipline 1 + Discipline 10 + profiles/INDEX.md + L1 + L5a + G + L8 |
| work-unit-bipartite-classification.md | A Producers + B Deployers + C Consumers + D Validators (primitive-set-shaping; always-present container) | VISION + MAINTENANCE §§1/2/3 + GLOSSARY index + work-unit / workflow / specialist / claim / event / actor / Owner B scope glossary entries + DISCIPLINES Discipline 1 + Discipline 10 + profiles/INDEX.md + L1 + L5a + L8 + G |
| deployment-derived-classification.md | A Producers + B Deployers + D Validators (DERIVED meta-concept; deployment-mechanics) | VISION + MAINTENANCE §§1/2/3 + GLOSSARY index + deployment / workspace / pioneer instance / substrate / shape / framework glossary entries + DISCIPLINES Discipline 1 + Discipline 10 + profiles/INDEX.md + L4a + L5a + G + L8 |
| engaged-authorship-operational-definition.md | A Producers + C Consumers + D Validators (cross-axis; defensibility-anchored) | VISION + MAINTENANCE §§1/2/3 + GLOSSARY index + engaged authorship / authorship preservation / defensibility / rubber-stamping / claim / sparring / event / quality-gate glossary entries + DISCIPLINES Discipline 1 + Discipline 10 + profiles/INDEX.md + L5a + L8 + G + L4a |

Each Writer brief explicitly excludes reading the artifact under audit during derivation + excludes reading peer cluster artifacts + excludes reading v1 findings (HISTORICAL INPUT only; bias-free derivation per skill §Sub-agent brief template — greenfield-Writer "DO NOT READ during derivation").

### Wave-1 Reviewer dispatch table (planned)

| Artifact | Reviewer brief inputs | 4 lenses applied |
|---|---|---|
| workflow-bipartite-classification.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Pattern-vs-instance leakage / VISION-grounding / provenance hygiene / cascade-miss |
| work-unit-bipartite-classification.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Same 4 lenses |
| deployment-derived-classification.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Same 4 lenses |
| engaged-authorship-operational-definition.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Same 4 lenses |

### Per-Wave + per-cluster Ralph self-checks (per skill §Termination criteria)

Persisted per artifact + per Wave + per cluster after each phase. Empty until execution proceeds.

## Composition with existing architecture

- **Coherence-audit composition**: this audit catches per-artifact derivation drift / cargo-cult / instance-leakage / cascade-miss; coherence-audit catches set-level + vocabulary-level + cascade-level drift via 10 universal lenses. Both compose at phase boundaries (per skill §Composition with other PBS dev skills). This execution is per-cluster (greenfield-rederivation territory); set-level lens scan would compose as separate coherence-audit invocation.
- **Cascade discipline**: any user-approved REVISE-LOCKED divergence triggers cascade per `MAINTENANCE.md` TOP-LEVEL RULE (UPSTREAM + DOWNSTREAM + SIDEWAYS); cascade execution itself delegated to fresh-context sub-agent per `CLAUDE.md` M3.
- **Phase 3 sub-phase status**: Phase 3.1 marked CLOSED in `ARCHITECTURE.md` §2 with 0 architectural REVISIONS in original closure audit; this v2 audit re-tests that closure under sub-agent + Writer-Reviewer orchestration to surface any drift the original closure audit missed under cascade-load conditions.

## Constraints flowing to downstream commitments

(POPULATED AS DECISIONS LAND)

If user-approved revisions exist:
- Per-revision cascade scope (which downstream artifacts touch the changed primitive)
- Cascade-completion commitment (tightly-coupled commits per affected layer; foundation-up ordering)
- Reviewer pass on cascade diff before push (per `CLAUDE.md` M4)

## Files touched (this DR's commit + per-Wave findings amendments)

- This DR: `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-1-drs.md` (PROPOSED status; pre-Wave-1)
- Per-Wave findings amendments: this same DR's Decision section + Sharpening provenance section (incremental per Wave)
- Cascade artifacts: TBD per user-decided revisions

## Revisit triggers

- New artifact added to Phase 3.1 cluster (none expected; Phase 3.1 closed)
- Stable-corpus signal: if 0 NEEDS-REVISION + 0 NEEDS-REWORK across all 4 artifacts (only T4-confirms-locked findings) → cluster greenfield-stable; cadence shifts to delta-audits per `coherence-audit` audit-scaling
- User-flagged drift on cluster artifact post-execution (e.g., new evidence surfaces during Phase 3.5 work that contradicts Phase 3.1 lock)
- Phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` (e.g., Phase 3.4 close C1 audit may compose with this re-audit)
