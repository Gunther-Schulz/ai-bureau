---
title: Greenfield-rederivation execution — Phase 3.4 substrate+adapter sub-cluster
topic-cluster: greenfield-rederivation
status: ACCEPTED-WITH-FINDINGS
---

# Greenfield-rederivation execution — Phase 3.4 substrate+adapter sub-cluster

## Status

ACCEPTED-WITH-FINDINGS. User en-bloc-accepted all 22 AI-committed positions per Decision section table (S1-S11 + A1-A11). Cascade execution follows per skill §Cascade execution + `CLAUDE.md` M3 (fresh-context Cascade-Writer sub-agent + Cascade-Reviewer per M4).

## Owner

- **Phase**: Phase 3 audit family (greenfield-rederivation campaign per `HANDOFF.md` Notes 49-51)
- **Skill version**: `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0
- **Cluster scope**: Phase 3.4 substrate+adapter Pattern A protocol topics — 4 artifacts (2 ARCH topics + 2 DRs)
- **Cluster execution number**: 3rd v2 cluster-execution (after Phase 3.1 4 DRs + Phase 3.2 doc-organization 2 composite DRs)

## Related

**Cluster artifacts** (audit targets):
- `arch/substrate.md`
- `arch/adapter.md`
- `docs/decisions/substrate-arch-topic.md`
- `docs/decisions/adapter-arch-topic.md`

**Skill artifact**:
- `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 — codifies the per-cluster procedure

**Prior greenfield-rederivation executions** (HISTORICAL INPUT — not authoritative for current verdicts):
- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-1-drs.md` (ACCEPTED-WITH-FINDINGS; corpus-stable signal: 0 T1 + ~10 T3 housekeeping)
- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-2-doc-organization.md` (ACCEPTED-WITH-FINDINGS; 0 T1 + 2 T2 + ~13 T3; load-bearing cascade-miss closed)
- `docs/decisions/greenfield-rederivation-pause.md` (v1; SUPERSEDED; Tier-1 findings on Pattern A catalog 8→3 + 18→12+6 template restructure cascaded across corpus pre-v2)

**Disciplines applied**:
- `DISCIPLINES.md` Discipline 1 (source-grounded; skill+profile sub-section)
- `DISCIPLINES.md` Discipline 8 (foundation-up workflow ordering)
- `DISCIPLINES.md` Discipline 9 (coherence-audit cadence)
- `DISCIPLINES.md` Discipline 10 (greenfield evaluation of archived material)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 (structural-impossibility / pattern-vs-instance / preliminary-lock)
- `CLAUDE.md` M3 (sub-agent-first cascade routing) + M4 (Writer-Reviewer per artifact) + M6 (HARD STOP per logical unit) + M7 (Ralph self-check at apparent completion)

## Context

**Why this cluster, why now**:

Per `HANDOFF.md` Note 50 (option-1 next-cluster choice, deferred to Note 51 follow-up) + Note 51 (Phase 3.4 substrate+adapter sub-cluster locked as next substantive cluster-execution): substrate + adapter are the 2 surviving Pattern A protocol topics post-greenfield-rederivation v1 reclassification (sparring + audit RECLASSIFIED mechanism-class; coordination + trust + time CANCELLED per `docs/decisions/greenfield-rederivation-pause.md` Step 3). They are the load-bearing anchors for the Pattern A template + per-impl extension Protocols pattern.

**Foundation-up rationale per `DISCIPLINES.md` Discipline 8**: substrate is the most foundational ARCH topic (anchor for the 12-common-required + 6-conditional-section template per `MAINTENANCE.md` §3 Pattern A protocol topic template); adapter validated 2-layer Surface variation (META-Surface + per-integration-class Surfaces). Both topics predate Lens 5 v0.2.1 codification + M1-M8 cascade-load mitigations + the v2 skill itself. Drift — particularly provenance-hygiene drift + cascade-miss between locked artifact + current MAINTENANCE template — is plausibly present.

**Cluster sweet-spot fit per skill §When-to-use**: 4 artifacts is within 2-6 sweet-spot; 1 Wave with 2 Writer-pairs (each Writer covers ARCH topic + paired DR as tightly-coupled pair) fits skill §Per-Wave parallel-dispatch shape.

**Why NOT decompose into 2 single-Writer Waves**: the ARCH topic + its paired DR are tightly coupled (DR captures decision-rationale FOR the ARCH topic; same primitives; same VISION axes; same disciplines). Single Writer per topic-pair preserves derivation coherence + reduces cross-Writer reconciliation noise. 2 Writer-pairs in 1 Wave is the empirical-evidenced shape from Notes 49-50 Wave executions.

**Cluster-pair signal context** (per Note 50 cross-execution observation): two prior cluster-executions yielded 0 T1 + 0-2 T2 + ~10-13 T3 each — substantive architecture survives greenfield-derivation; drift concentrates in Lens 5 provenance hygiene + Lens 8 instance-leakage + cascade-miss to upstream/downstream artifacts. This cluster will test whether the pattern holds for the FOUNDATIONAL Pattern A topics (substrate as anchor) — higher-stakes than the prior two clusters.

## Decision

**Cluster-level summary** (post-Wave-1 reconciliation pending):

| Tier | Count | Concentration |
|---|---|---|
| T1 — framework-shape-changing | 0 | n/a |
| T2 — topic-rewriting | 5 | DR procedural-narrative blocks (substrate ×3) + adapter §2 per-class catalog (bidirectional architectural question) + adapter DR §Decision section-count cascade |
| T3 — mechanical edit | 17 | Lens 5 provenance hygiene (status breadcrumbs; "session N"; Pattern-note-(meta) sections) + cascade-miss (Hand-rolled GLOSSARY back-check; missing actor cross-ref; "#2 of 8" stale; template section-numbering renumbering) |
| T4 — confirms-locked | 35 | Substantive architecture (Surfaces; tri-aspect; cardinality+lifecycle; selection mechanics; composition claims; phase routing; cross-references on architectural content) survives greenfield-derivation chain |

**Cross-cluster pattern signal** (per HANDOFF.md Note 50 cluster-pair observation, now extended to 3rd cluster-execution): substantive Pattern A architecture survives greenfield-derivation; drift concentrates in (a) Lens 5 v0.2.1 provenance hygiene retro-application gaps (locked artifacts predate Lens 5 v0.2.1 codification + M1-M8 cascade-load mitigations) + (b) cascade-miss between locked artifact and current MAINTENANCE template / current GLOSSARY entries.

**Per-finding verdict + AI-committed position table** (user-reconciliation pending):

### substrate-pair findings

| # | Finding | Tier | AI-committed position | Rationale |
|---|---|---|---|---|
| S1 | `arch/substrate.md` frontmatter status: "drafted (Phase 3.4 Round 2; locked pending optional Round 3 trigger)" | T3 | AMEND-LOCKED | Strip Round/phase breadcrumb → `status: locked` per `MAINTENANCE.md:273` minimal frontmatter + Lens 5 v0.2.1 |
| S2 | `arch/substrate.md` §3 Common-surface boundary criteria — substrate has SINGLE Surface; §3 per `MAINTENANCE.md:255` applies "when protocol has multi-class Surface (e.g., adapter)"; locked uses §3 for "Surface vs per-impl-extension boundary" instead | T3 (bidirectional) | REVISE-LOCKED | Reframe substrate.md §3 as N/A with note (substrate has single unified Surface; Surface-vs-extension boundary covered in §4) — substrate is template anchor; resolution propagates to all Pattern A topics |
| S3 | `arch/substrate.md` §4 enumerates "Three concrete substrate Implementations: Claude Agent SDK / MS Agent Framework / Hand-rolled (Python + MCP + Pydantic)" — Hand-rolled NOT in `glossary/substrate.md:26-29` cross-archetype illustration | T3 (cascade-miss) | REVISE-LOCKED | Add Hand-rolled to `glossary/substrate.md` as third concrete Implementation per `MAINTENANCE.md:18-22` GLOSSARY back-check (DOWNSTREAM cascade direction) |
| S4 | `arch/substrate.md` §7 missing `actor` row — locked content cites "Substrate's running Instance IS the `actor_kind: ai_runtime`" claim implicitly but composition table omits actor reciprocal | T3 (Lens 6 symmetry) | AMEND-LOCKED | Add `actor` row to §7 composition table per Lens 6 reciprocity gap |
| S5 | `arch/substrate.md` §11 missing cross-substrate-portability error category despite §9 workspace-identity-persists-across-substrate-migrations claim being locked | T3 | AMEND-LOCKED | Add 6th error category for cross-substrate migration / portability errors per `profiles/G-composability-gate.md:154-155` |
| S6 | `docs/decisions/substrate-arch-topic.md` Status: heavy session-N + "AMENDED session 16" + "post-Phase-3.4-#4" provenance breadcrumbs | T3 | AMEND-LOCKED | Strip session breadcrumbs; preserve sharpening-rounds-metadata semantics per `MAINTENANCE.md:283`; relocate provenance content to §Sharpening provenance |
| S7 | `docs/decisions/substrate-arch-topic.md` Related — Discipline 1 reference suffixed with "(procedural discipline applied during this DR's Round 2; canonical session-16 case)" | T3 | AMEND-LOCKED | Strip session-16 narrative suffix; keep Discipline 1 reference |
| S8 | `docs/decisions/substrate-arch-topic.md` Refinements applied block + "Round 1 termination position FAILURE" sub-section + "After user prompted skill check..." narrative | T2 | AMEND-LOCKED | Restructure under §Sharpening provenance per `MAINTENANCE.md:288-294`; preserve Round-by-Round substantive content (EXPANSIONS list, manufactured-criticism counts); strip session-narrative wrapping |
| S9 | `docs/decisions/substrate-arch-topic.md` "Retroactive greenfield-pass amendment" sub-section — process-narrative wrapping load-bearing REVISION-1 content | T2 | AMEND-LOCKED | Restructure: keep audit-findings table + REVISION-1 substantive content as §Sharpening provenance REVISIONS-surfaced sub-section; strip "User-triggered audit" / "session 16" / "post-Phase-3.4-#4" framing |
| S10 | `docs/decisions/substrate-arch-topic.md` Files touched embeds "(Note 35: substrate ARCH topic locked; first canonical arch/<topic>.md established; profile-anchored validation properly executed under 5-location procedural discipline)" | T3 | AMEND-LOCKED | Strip Note-35 narrative parenthetical; keep `HANDOFF.md` file-list entry |
| S11 | `docs/decisions/substrate-arch-topic.md` "Pattern note (meta)" final section — entire section is meta-narrative about session 16 procedural-fidelity work | T2 | AMEND-LOCKED | Strip entire section per Lens 5 strip-test (would removing confuse fresh reader's understanding of decision? No); preserve in HANDOFF + git log narrative |

### adapter-pair findings

| # | Finding | Tier | AI-committed position | Rationale |
|---|---|---|---|---|
| A1 | `arch/adapter.md` frontmatter status: "drafted (Phase 3.4 Round 2; locked)" + `topic-cluster: Pattern A protocol topics (#2 of 8)` — Round breadcrumb + STALE 8-count post-3→reduction per `glossary/protocol-architectural.md:39-43` | T3 | REVISE-LOCKED | Strip "Phase 3.4 Round 2" → `status: locked`; update count "#2 of 8" → "#2 of 3" (3 Pattern A topics post-greenfield-rederivation v1: substrate / adapter / quality-gate) |
| A2 | `arch/adapter.md` §2 per-class Surface catalog — locked names {Email / Accounting / MCP-Server / A2A-Peer / File-Sync}; Writer derived {Email / Accounting / corpus / federation-peer / file-sync}; bidirectional architectural question on whether MCP-Server is first-class per-integration-class Surface OR shape underneath broader "corpus" class | T2 (bidirectional) | KEEP-LOCKED + surface-to-user | Locked frame (MCP-Server first-class) defensibly composes with substrate Surface §B per `arch/substrate.md` reference; Writer's "corpus" framing under-recognizes substrate-composition. Surface as user-decision question — could be Writer-derivation drift OR genuine simplification opportunity |
| A3 | `arch/adapter.md` §8 over-extended — locked treats §8 as ACTIVE with full per-class event-kind catalog ("Per-action audit emission via MCP gate"); template `MAINTENANCE.md:256` treats §8 as substrate-conditional | T3 | AMEND-LOCKED | Move per-class event-kind catalog to its own section OR §11; keep §8 as N/A-with-rationale per template |
| A4 | `arch/adapter.md` §9 title drift — locked: "Auth + lifecycle semantics (architectural-level)"; template `MAINTENANCE.md:244`: "Cardinality + lifecycle (Creator / owner / destroyer; mutability; cross-session persistence)" | T3 | REVISE-LOCKED | Rename §9 to template-faithful "Cardinality + lifecycle"; move auth content to §10 conditional |
| A5 | `arch/adapter.md` §10/§11/§12/§13 silent renumbering — locked uses slots for non-template content (Per-integration-class error categories / Cross-shape policy variation / Quota+rate-limit+circuit-breaker / Versioning+migration); silently skipped multiple template conditionals without explicit N/A | T3 | REVISE-LOCKED | Renumber to match Pattern A template per `MAINTENANCE.md:251-265`; document N/A explicitly for skipped conditionals; map auth → §10; per-impl errors → §11; skipped §12/§13 explicit-N/A |
| A6 | `arch/adapter.md` §16 Decision-design provenance — archive citations clean but missing Discipline 10 explicit "INPUT only" framing | T3 | AMEND-LOCKED | Add "INPUT only (per `disciplines/10-greenfield-evaluation.md` — not transcribed as template)" qualifier to archive citations |
| A7 | `arch/adapter.md` §18 Cross-references — coined "adapter-coupling impossible-by-construction" not anchored in MAINTENANCE | T3 | REVISE-LOCKED | Rephrase to cite the existing "make wrong shapes impossible" per `MAINTENANCE.md:117-128` § (TOP-LEVEL DESIGN PRINCIPLES §1) — don't coin parallel principle |
| A8 | `arch/adapter.md` DR §Decision lists 18 sections matching locked ARCH topic; Pattern A template expects ~15-16 for adapter per `MAINTENANCE.md:264` | T2 | REVISE-LOCKED (cascades from A5) | Renumber DR §Decision section list to match A5 renumbering output (~15-16 sections) |
| A9 | `docs/decisions/adapter-arch-topic.md` Status contains "session 16 (2026-05-02)" narrative breadcrumb | T3 | REVISE-LOCKED | Strip "session 16"; date can stay; rephrase per `MAINTENANCE.md:283` template |
| A10 | `docs/decisions/adapter-arch-topic.md` Sharpening provenance contains session-state language "still in evidence from substrate Round 2 retroactive pass" | T3 | AMEND-LOCKED | Strip session-state language; rephrase as structured cluster verdict |
| A11 | `docs/decisions/adapter-arch-topic.md` "Pattern note (meta)" section — process-narrative-breadcrumb per `MAINTENANCE.md:271` provenance-hygiene rule | T3 | REVISE-LOCKED | Remove section per Lens 5 strip-test; content (if load-bearing) moves to HANDOFF |

### KEEP-LOCKED (T4 confirms)

35 elements across both topic-pairs survive greenfield-derivation chain unchanged. Per Reviewer detail in §Sharpening provenance below. Includes: substrate.md §1/§2/§5/§6/§8/§9/§10/§12/§13/§14/§15/§16/§17/§18; substrate-arch-topic.md Owner/Context/Decision/Composition/Constraints/Revisit triggers; adapter.md §1/§3/§4/§5/§6/§7/§14/§15/§17; adapter-arch-topic.md Related/Context/Composition/Constraints/Files/Revisit triggers.

**Status transition**: PROPOSED → ACCEPTED-WITH-FINDINGS (user en-bloc-accepted all 22 positions). Cascade execution follows.

## Sharpening provenance

### Wave decomposition

| Wave | Artifacts | Writer count | Reviewer count | Rationale |
|---|---|---|---|---|
| 1 | substrate (arch/substrate.md + docs/decisions/substrate-arch-topic.md) + adapter (arch/adapter.md + docs/decisions/adapter-arch-topic.md) | 2 (1 per topic-pair) | 2 (1 per Writer output) | Tightly-coupled topic+DR pairs; preserves derivation coherence; matches user-instructed "2 Writer + 2 Reviewer in parallel" shape per `HANDOFF.md` Note 51 step 5 |

### Per-Wave dispatch summary

**Wave-1 dispatch** (4 sub-agents in fresh contexts; main session orchestrator-only per skill §Per-Wave step 3):

- **Writer-1 (substrate-pair)**: 660-line greenfield-derivation summary covering both `arch/substrate.md` 18-section Pattern A topic + `docs/decisions/substrate-arch-topic.md` 10-section DR. Read sequence: VISION + MAINTENANCE + 12 GLOSSARY entries (substrate / protocol-architectural / mechanism / policy / framework / shape / framework-c-scope / owner-b-scope / workspace / session / event / actor) + DISCIPLINES index + disciplines/01 + disciplines/10 + profiles/INDEX + L4a + L5a + G. Ralph self-check: PASS (5/5 confirmations).
- **Writer-2 (adapter-pair)**: 403-line greenfield-derivation summary covering both `arch/adapter.md` 12+~3-4-conditional Pattern A topic + `docs/decisions/adapter-arch-topic.md` DR. Read sequence: VISION + MAINTENANCE + 12 GLOSSARY entries (adapter / substrate / protocol-architectural / mechanism / policy / framework / shape / framework-c-scope / owner-b-scope / workspace / event / actor) + DISCIPLINES index + disciplines/01 + disciplines/10 + profiles/INDEX + L4a + L5a + G. Ralph self-check: PASS (5/5 confirmations).
- **Reviewer-1 (against Writer-1 output)**: per-element verdict table covering all 18 `arch/substrate.md` sections + all 8 + 4 sub-elements of `docs/decisions/substrate-arch-topic.md`. Tiered findings: 0 T1 + 3 T2 + 8 T3 + 22 T4-confirms. 4 lenses applied (pattern-vs-instance / VISION-grounding / provenance-hygiene / cascade-miss). Ralph self-check: PASS (6/6 confirmations).
- **Reviewer-2 (against Writer-2 output)**: per-element verdict table covering all 18 `arch/adapter.md` sections + all 10 sections + Pattern-note-(meta) of `docs/decisions/adapter-arch-topic.md`. Tiered findings: 0 T1 + 2 T2 + 9 T3 + 13 T4-confirms. 4 lenses applied. Ralph self-check: PASS (4/4 confirmations).

**Aggregate cluster signal** (per Decision section table above): 0 T1 + 5 T2 + 17 T3 + 35 T4-confirms across both topic-pairs.

**Cross-execution pattern signal** (3rd cluster-execution; corpus-stable signal continuing per `HANDOFF.md` Notes 49-50):
- Phase 3.1 (4 DRs): 0 T1 + 0-2 T2 + ~10 T3
- Phase 3.2 (2 DRs): 0 T1 + 2 T2 + ~13 T3 (1 load-bearing cascade-miss closed)
- **Phase 3.4 substrate+adapter (4 artifacts)**: 0 T1 + 5 T2 + 17 T3 (5 T2 includes 1 bidirectional architectural question on adapter §2 per-class catalog; rest is provenance-narrative restructuring)
- **Stable-corpus pattern**: substantive Pattern A architecture survives greenfield-derivation chain; drift concentrates in (a) Lens 5 v0.2.1 provenance hygiene retro-application + (b) cascade-miss to upstream/downstream artifacts predating M1-M8 + Lens 5 v0.2.1 codification.

### Foundation-up dependency analysis (within cluster)

- **substrate** has zero dependency on adapter; foundational primitive (Pattern A anchor).
- **adapter** composes WITH substrate Surface §C (permission flow) per locked `arch/adapter.md`. For greenfield re-derivation, both Writers derive independently from primitives + GLOSSARY entries (each GLOSSARY entry self-anchors); adapter Writer cites substrate-as-composition-target without contaminating greenfield derivation.
- → 1 Wave with 2 parallel Writers acceptable. No within-cluster foundation-up Wave-split needed.

### Pre-validation prep reads (main-session orchestrator)

Per `HANDOFF.md` Note 51 step 3 + Note 50 hook-prep pattern, main-session orchestrator read BEFORE first Edit:
- `VISION.md`, `MAINTENANCE.md`, `DISCIPLINES.md`, `HANDOFF.md`, `BACKLOG.md`, `ARCHITECTURE.md`, `GLOSSARY.md` (mandatory session-start reads per `CLAUDE.md`)
- `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0 (active skill)
- `plugin/skills/decision-design-sharpening/SKILL.md` v0.10.0 (hook gate prep)
- `profiles/INDEX.md` (cluster structure)
- 3 profile files: `profiles/L5a-planner-pbs-schulz.md` (Cluster B+C anchor) + `profiles/G-composability-gate.md` (Cluster D) + `profiles/L4a-workspace-deployer-solo.md` (Cluster B; substrate-selection grounding)

## Composition with existing architecture

### How this audit composes

- **vs `coherence-audit`**: peer audit skill (lens-driven corpus scan); both run at phase boundaries per `disciplines/09-coherence-audit-cadence.md`. Greenfield-rederivation re-derives per artifact from primitives; coherence-audit scans for set-level / vocabulary-level / cascade-level drift. Different fault modes; the two compose. This execution is greenfield-only (per skill §Procedure); coherence-audit would run separately at C1 (post-3.4 close) per `BACKLOG.md` Phase 3 audit-checkpoints.
- **vs `decision-design-sharpening`**: phase-1 pre-decision skill operates UPSTREAM (before lock). This skill operates POST-lock on accumulated decisions. Different lifecycle moments.
- **vs `pre-implementation-sharpening`**: phase-2 implementation-start skill. Phase 6 spec/code work for substrate + adapter would invoke pre-implementation-sharpening; this audit is foundational verification BEFORE implementation begins.

### Cascade scope if revisions surface

**Potential downstream artifacts (cascade targets if T1/T2 surface)**:
- `ARCHITECTURE.md` §4 topic catalog one-liners (substrate + adapter rows; lines 58-59)
- `ARCHITECTURE.md` §7 Locked architectural decisions (substrate + adapter sections; lines 207-213)
- `MAINTENANCE.md` Pattern A protocol topic template (if T2 finding on template-fit, since substrate is anchor)
- `arch/sparring.md` + `arch/audit.md` cross-refs to substrate (composition claims)
- `glossary/substrate.md` + `glossary/adapter.md` (if greenfield surfaces vocabulary refinement glossary-grade per `MAINTENANCE.md` Bidirectional cascade)

**Cascade execution per skill §Cascade execution** (post-reconciliation): if revisions exist, cascade delegated to fresh-context Cascade-Writer sub-agent + Cascade-Reviewer per `CLAUDE.md` M3+M4. Tightly-coupled commits per `MAINTENANCE.md` cascade discipline.

## Constraints flowing to downstream commitments

**TO BE POPULATED POST-RECONCILIATION** (per-artifact revisions if any).

## Files touched (this DR's commit + Wave-1 + reconciliation + cascade)

- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-4-substrate-adapter.md` (this DR; PROPOSED stub commit)
- Wave-1 findings amendment commits (per-Wave persistence)
- Cascade target files if revisions (separate cascade commits)
- HANDOFF.md Note 52 (closure)

## Revisit triggers

- New artifact added to substrate/adapter sub-cluster (e.g., per-impl Phase 6 specs land)
- User-flagged drift on substrate or adapter primitives
- Phase 3.5 primitive-cluster work surfaces composition gap with substrate or adapter Surfaces
- Phase 3.6 quality-gate ARCH topic work surfaces composition gap with substrate Surface §D (sparring sub-mechanisms architecturally-encoded)
- Coherence-audit Checkpoint C1 (post-Phase-3.4 close per `BACKLOG.md` Phase 3 audit-checkpoints) — this DR's verdicts inform C1 lens activation
- Phase-boundary audit per `disciplines/09-coherence-audit-cadence.md`
