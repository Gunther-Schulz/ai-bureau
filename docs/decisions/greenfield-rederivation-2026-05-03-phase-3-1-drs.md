# Greenfield-rederivation execution — Phase 3.1 4 DRs cluster

## Status

ACCEPTED-WITH-FINDINGS. User-reconciliation complete (P1-P4 + P7 REVISE/AMEND-LOCKED en bloc; P5 + P6 KEEP-LOCKED). Cascade execution complete (Cascade Writer sub-agent in fresh context; Cascade Reviewer sub-agent verdict READY-TO-PUSH; 3 DRs amended in single tightly-coupled commit per `MAINTENANCE.md` cascade discipline).

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

Wave-1 findings persisted; user-reconciliation phase pending (status remains PROPOSED until reconciliation completes).

### Headline result

**0 T1 (framework-shape-changing) findings. 0-2 T2 (topic-rewriting; borderline) findings. ~10 T3 (mechanical edit) findings — concentrated in Lens 5 provenance hygiene + Lens 8 pioneer-instance leakage.**

Core architectural commitments across all 4 DRs survive greenfield re-derivation under sub-agent + Writer-Reviewer orchestration. Divergences detected are template-conformance + provenance-hygiene drift; locked DRs predate Lens 5 v0.2.1 codification + the M1-M8 cascade-load mitigations.

### Per-artifact verdict table

| DR | Per-artifact verdict | Tier | Reviewer summary |
|---|---|---|---|
| workflow-bipartite-classification | GREENFIELD-VALID on architecture; NEEDS-REVISION on Status-line breadcrumbs + pioneer-instance leakage in Context/Rationale + trajectory breadcrumbs in canonical sections + missing decomposition-mode tag | T3 (×6) | Architecture survives; mechanical Lens-5/Lens-8/template-conformance cleanup |
| work-unit-bipartite-classification | GREENFIELD-VALID across all elements | T4 confirms-locked (×optional T3 sharpening on event/actor composition rows) | CONFIRMS-LOCKED; Writer + locked converge cleanly |
| deployment-derived-classification | GREENFIELD-VALID on architecture; NEEDS-REVISION on Status-line "session 16" tag | T3 (×1) | CONFIRMS-LOCKED on architecture; single Lens-5 status-line cleanup |
| engaged-authorship-operational-definition | GREENFIELD-VALID on core architecture (two-phase composite + per-claim per-version + two-layer + per-shape + multi-claim batch + workflow_instance + authority-binding + AI-runtime distinction); NEEDS-REVISION on Status-line breadcrumbs + revisit triggers expansion | T3 (×~5); T2 (×1 borderline on pre-existing-claim ingestion option-a-vs-OR — recommendation KEEP-LOCKED watch-list framing) | CONFIRMS-LOCKED on architecture; Writer simplifications-vs-locked = Writer-side divergence not locked-DR drift in most T3s |

### Position commits per divergence (main-session AI commits per `feedback_judgment_and_automate.md`)

**P1 — Status-line provenance breadcrumbs (workflow / deployment / engaged-authorship DRs)**: REVISE-LOCKED (T3 mechanical). Strip "Locked: session 16 (2026-05-02)" + "Sharpening: 2-round pattern..." from Status headers; keep date-only via DR date convention per `MAINTENANCE.md:334`. Trajectory metadata already lives in §6 Sharpening provenance section in each DR; Status-line entries are duplication-with-narrative-tag. Lens 5 v0.2.1 explicit.

**P2 — Pioneer-instance leakage in Context + Rationale (workflow DR)**: REVISE-LOCKED (T3 mechanical). Re-frame B-Plan-Begründung references as cross-archetype illustration: shape-neutral architectural claim first; pioneer + 1-2 alternative-archetype examples as parallel illustrations. Demote pioneer to one example among several. Lens 8 + `MAINTENANCE.md:131-147` pattern-vs-instance discipline.

**P3 — Trajectory breadcrumbs in canonical sections (workflow DR — Critical-refinement / Cross-specialist / Validated-under-new-disciplines sections)**: REVISE-LOCKED (T3 mechanical). Move "Round 1 framing → Round 2 user push" + "Round 2 ST9 deferred → retrospective D Gate" + "After Phase 3.1 introduced new disciplines, workflow revisited" prose into §Sharpening provenance section per `MAINTENANCE.md:288` meta-home rule. Replace canonical-section content with shape-only claims.

**P4 — Missing decomposition-mode tag (workflow DR)**: REVISE-LOCKED (T3 mechanical). Add "Decomposition mode: Mode 1 emergent (single decision; no upfront-known sub-decision split)" to §Sharpening provenance per `MAINTENANCE.md:294` template requirement.

**P5 — Optional sharpening (work-unit DR — event/actor composition rows)**: KEEP-LOCKED. Locked DR's framing acceptable; optional cleanup not load-bearing.

**P6 — Engaged-authorship pre-existing-claim ingestion (T2 borderline)**: KEEP-LOCKED. Locked DR keeps option-(a) OR template-with-attribution as deferred to Phase 3.5 with watch-list framing per `MAINTENANCE.md:134-145` no-defer discipline. Writer's hardline option-(a) commit is forward-progress beyond locked DR's scope; resolving here would commit ARCH-level decision the locked DR explicitly defers. Watch-list framing stands.

**P7 — Engaged-authorship revisit triggers expansion**: AMEND-LOCKED (T3 mechanical). Incorporate Writer's 3 added triggers (workspace migration cross-substrate event-schema lossy / coherence-audit Lens 6+9 vocabulary collision / pre-existing-claim ingestion real evidence). Pareto-improving expansions; no architectural shift.

### v1 vs v2 audit comparison

v1 (`docs/decisions/greenfield-rederivation-pause.md` SUPERSEDED) surfaced Tier-1 findings (Pattern A catalog 8→3; template restructure 18→12+6) under single-AI cascade-load conditions; those Tier-1 findings cascaded across the corpus prior to this v2 execution. v2 — running on the SAME 4 Phase 3.1 DRs that v1 audited — surfaces 0 T1 + ~10 T3 housekeeping. This is the expected stable-corpus shape post-Tier-1-cascade: foundational classifications were correct; drift is provenance-hygiene drift accumulated under cascade-load before M1-M8 + Lens 5 v0.2.1 codification.

### User-reconciliation phase (pending)

Per skill §Post-cluster step 2 (decision phase = user approval per `DISCIPLINES.md` working procedure). User decides per P1-P7. Status will transition PROPOSED → ACCEPTED-WITH-FINDINGS post-decision. Cascade execution (P1-P4 + P7) delegated to fresh-context sub-agent per `CLAUDE.md` M3 + skill §Cascade execution.

Verdict scheme reference (per skill §Verdict scheme):

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

### Wave-1 dispatch summary (executed)

**Writer wave**: 4 sub-agents dispatched in parallel (single message; 4 Agent tool invocations). Each Writer in fresh context with focused brief (artifact path; required reads list; explicit DO-NOT-READ list including artifact-under-audit + peer cluster artifacts + v1 findings + current execution DR). Each Writer derived greenfield content for Context / Decision / Sharpening provenance / Composition / Constraints / Revisit triggers from VISION + locked GLOSSARY substrate + first-principles MAINTENANCE + DISCIPLINES + ≥3 cluster-relevant profile files. All 4 Writers returned 200-400 line greenfield-derivation summaries with file:line citations + Ralph self-check confirmation.

**Reviewer wave**: 4 sub-agents dispatched in parallel against respective Writer outputs (sequenced after Writer wave; Reviewer needs Writer derivation as input). Each Reviewer in fresh context with brief (locked-artifact path + inline Writer derivation + 4-lens framework: Lens 5 provenance hygiene + Lens 8 pattern-vs-instance + Lens 9 VISION-grounding + cascade-miss). Each Reviewer produced per-element verdict table + tier per finding + recommendation per finding + Ralph self-check confirmation.

### Per-sub-agent Ralph self-check verification (per skill §Termination criteria)

| Sub-agent | Required-reads complete | Discipline 10 applied | Avoided locked-artifact / peer-cluster / v1-findings reads | Cited specific GLOSSARY/VISION/MAINTENANCE refs |
|---|---|---|---|---|
| Writer-1 (workflow) | ✅ | ✅ | ✅ | ✅ |
| Writer-2 (work-unit) | ✅ | ✅ | ✅ | ✅ |
| Writer-3 (deployment) | ✅ | ✅ | ✅ | ✅ |
| Writer-4 (engaged-authorship) | ✅ | ✅ | ✅ | ✅ |
| Reviewer-1 (workflow) | ✅ (locked + Writer + lenses) | n/a (Reviewer applies lenses) | n/a (Reviewer reads locked) | ✅ |
| Reviewer-2 (work-unit) | ✅ | n/a | n/a | ✅ |
| Reviewer-3 (deployment) | ✅ | n/a | n/a | ✅ |
| Reviewer-4 (engaged-authorship) | ✅ | n/a | n/a | ✅ |

**Main-session Ralph self-check** (per skill §Ralph self-check at apparent completion + `CLAUDE.md` M7):
- Read SKILL.md fresh at invocation: ✅
- Each Writer + Reviewer Ralph self-check confirmed at completion: ✅ (8/8)
- Avoided executing greenfield-derivation in main session: ✅ (orchestrator role only)
- Dispatched Reviewer separate from Writer per artifact: ✅ (4+4 in fresh contexts)
- Persisted Wave-1 findings to per-execution DR before next Wave: ✅ (this commit)
- Cascade-execution discipline preserved: pending user-reconciliation; cascade delegated to fresh-context sub-agent per M3 + skill §Cascade execution
- Provenance-hygiene check on this DR: ✅ (Decision section holds shape-only verdict claims; trajectory + Wave dispatch summary in Sharpening provenance per `MAINTENANCE.md:288`)

## Composition with existing architecture

- **Coherence-audit composition**: this audit catches per-artifact derivation drift / cargo-cult / instance-leakage / cascade-miss; coherence-audit catches set-level + vocabulary-level + cascade-level drift via 10 universal lenses. Both compose at phase boundaries (per skill §Composition with other PBS dev skills). This execution is per-cluster (greenfield-rederivation territory); set-level lens scan would compose as separate coherence-audit invocation.
- **Cascade discipline**: any user-approved REVISE-LOCKED divergence triggers cascade per `MAINTENANCE.md` TOP-LEVEL RULE (UPSTREAM + DOWNSTREAM + SIDEWAYS); cascade execution itself delegated to fresh-context sub-agent per `CLAUDE.md` M3.
- **Phase 3 sub-phase status**: Phase 3.1 marked CLOSED in `ARCHITECTURE.md` §2 with 0 architectural REVISIONS in original closure audit; this v2 audit re-tests that closure under sub-agent + Writer-Reviewer orchestration to surface any drift the original closure audit missed under cascade-load conditions.

## Constraints flowing to downstream commitments

User-reconciled cascade applied:
- **P1** (3 DRs: workflow / deployment / engaged-authorship): Status-line provenance breadcrumbs stripped; replaced with shape-only Status + Date-only metadata per `MAINTENANCE.md:334`.
- **P2** (workflow DR): Pioneer-instance B-Plan-Begründung references in Rationale re-framed; pattern-first claim leads; pioneer demoted to one of N parallel cross-archetype illustrations (planning bureau / legal practice / research lab / accounting practice).
- **P3** (workflow DR): Trajectory breadcrumbs moved from canonical sections (Critical-refinement / Cross-specialist / Validated-under-new-disciplines) into §Sharpening provenance section; canonical sections hold shape-only claims.
- **P4** (workflow DR): Decomposition-mode tag added to §Sharpening provenance (`Mode 1 emergent (single decision; no upfront-known sub-decision split)`).
- **P7** (engaged-authorship DR): 3 added revisit triggers appended (workspace migration cross-substrate event-schema lossy / coherence-audit Lens 6+9 vocabulary collision / pre-existing-claim ingestion real evidence); 5 existing triggers preserved.

Cascade verification: Reviewer sub-agent (fresh context) verdict READY-TO-PUSH on all 7 positions. Architectural content (Decision / Composition / Constraints flowing / Defers / REVISION stress-tests) preserved across all 3 DRs. No new vocabulary; no scope-creep; no out-of-scope edits.

Minor non-blocking observation (Reviewer-surfaced; not actioned this Wave): section-name "Sharpening rounds metadata" in deployment + engaged-authorship DRs could normalize to template-canonical "Sharpening provenance" per `MAINTENANCE.md:288` — cosmetic only; deferred to backlog or next cluster pass if normalization is desired.

## Files touched

- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-1-drs.md` (this DR — created PROPOSED → Wave-1 findings persisted → user-reconciled → cascade-completion + status transition to ACCEPTED-WITH-FINDINGS)
- `docs/decisions/workflow-bipartite-classification.md` (P1 + P2 + P3 + P4 cascade)
- `docs/decisions/deployment-derived-classification.md` (P1 cascade)
- `docs/decisions/engaged-authorship-operational-definition.md` (P1 + P7 cascade)

## Revisit triggers

- New artifact added to Phase 3.1 cluster (none expected; Phase 3.1 closed)
- Stable-corpus signal: if 0 NEEDS-REVISION + 0 NEEDS-REWORK across all 4 artifacts (only T4-confirms-locked findings) → cluster greenfield-stable; cadence shifts to delta-audits per `coherence-audit` audit-scaling
- User-flagged drift on cluster artifact post-execution (e.g., new evidence surfaces during Phase 3.5 work that contradicts Phase 3.1 lock)
- Phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` (e.g., Phase 3.4 close C1 audit may compose with this re-audit)
