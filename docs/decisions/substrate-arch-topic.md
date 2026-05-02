# Decision record: Substrate ARCH topic (Phase 3.4 first canonical arch/<topic>.md)

**Status**: ACCEPTED — session 16 (2026-05-02); 2-round sharpening (Round 1 full monty + Round 2 cross-cutting + schema-detail layer per `decision-design-sharpening` v0.6.0 layered coverage observation) + retroactive profile-anchored validation pass (post-procedural-discipline lock; ≥3 cluster representatives Read with cited content). **AMENDED session 16 (post-Phase-3.4-#4) per `DISCIPLINES.md` Discipline 10 retroactive greenfield-pass: REVISION-1 applied to §10 boot/shutdown ordering — substrate.md §10 was archive-anchored with substrate-flushes-audit-trail; corrected to align with `arch/audit.md` §11 (audit Protocol owns audit-trail flush; shuts down AFTER substrate).**

**Owner**: Phase 3.4 Per-architectural-Protocol detail rebuild; foundation for Pattern A protocol topics 2-7 (adapter / sparring / audit / coordination / trust / time) which compose with substrate's Surface contract.

**Related**: 
- Per locked GLOSSARY substrate entry (Pattern A tri-aspect; cross-axis; multi-aspect classification)
- Per `phase-3-2-doc-organization.md` (composite Phase 3.2 lock; topic catalog Sub-decision 1; arch/<slug>.md naming Sub-decision 2; cross-cutting placement Sub-decision 3; ARCHITECTURE.md structure Sub-decision 4)
- Per `DISCIPLINES.md` Discipline 1 (skill+profile sub-section) (procedural discipline applied during this DR's Round 2; canonical session-16 case)
- Archived sources: `archive/docs/decisions/substrate-protocol-design.md`, `substrate-agentic-framework.md`, `sdk-deep-read.md`

## Context

Phase 3.4 begins with substrate (foundation-up dependency: 7 other Pattern A protocol topics compose with substrate's Surface contract). First canonical `arch/<topic>.md` — establishes pattern + budget + structure for remaining 13 topics (per ARCHITECTURE.md §4 Topic catalog).

Substrate is broad architectural surface (substrate-eval-grade synthesis per archived sources) — empirical sweet-spot allows 2-3 rounds. 2-round sweet spot empirically validated as sufficient per layered coverage observation (R1 = arch decisions / R2 = cross-cutting + schema-detail).

Decision-design sharpening fired against the substrate Pattern A protocol detail; Phase 6 spec lands the Pydantic Protocol contract (Mode 3); this topic articulates Mode 4 conceptual.

## Decision

`arch/substrate.md` LOCKED with 18 sections covering:

1. Topic scope (substrate as Pattern A; cross-axis; 1:1 cardinality with workspace)
2. Surface contract (7 capability categories: agent loop / MCP register+discover / permission / structured-output / hooks / session / specialist registration)
3. Common-surface boundary criteria (decision rule for Surface vs per-impl extension)
4. Per-implementation aspect (Pattern level + current instance set + per-impl extension Protocols pattern)
5. Selection mechanics (workspace.md substrate field; cardinality; validation; re-binding)
6. Tri-aspect reconciliation (Surface + Implementations + Running Instance)
7. Composition with framework primitives (15 cross-references)
8. Substrate-internal vs skill-level audit emission (architectural-event kinds enumerated; dual emission paths converging in audit-trail)
9. Cardinality + lifecycle (creator / owner / destroyer; mutability; cross-session persistence)
10. Boot + shutdown phase ordering (architectural-level)
11. Substrate error categories (architectural-level; per-shape error semantics)
12. Transport variation + per-tier mapping (in-process / subprocess / HTTP first-class peers)
13. Deployment-tier awareness (Tier 1/2/3; per-tier behavior in impl, not Surface)
14. Pre-implementation operational concerns (Phase 6 forward reference; explicitly NOT locked at ARCH level)
15. Watch-list (W1-W4)
16. Decision-design provenance (archived sources + pattern-vs-instance discipline)
17. Phase routing (Pydantic spec → Phase 6; impl work → Phase 6)
18. Cross-references

## Refinements applied

### Round 1 (full monty; per `decision-design-sharpening` v0.6.0 R1 = architectural decisions layer)

- 6-category Surface (A. agent loop / B. MCP register+discover / C. permission / D. structured-output / E. hooks / F. session)
- Common-surface boundary criteria
- Per-impl extension Protocols pattern
- Selection mechanics
- Tri-aspect reconciliation
- Composition with framework primitives (initial set)
- Substrate-internal audit emission distinction
- Cardinality + lifecycle (initial)
- Pre-implementation forward-reference (initial list)
- Phase routing + watch-list

**Round 1 EXPANSIONS surfaced (2)**:
1. Logic placement mode for substrate (Mode 4 conceptual + Mode 3 spec contract distinction; explicit subsection)
2. MCP-compatibility as baseline-assumption (per locked criterion-1 disqualifying screen; named explicitly)

**Round 1 manufactured criticisms rejected (3)**: smaller Surface (3 vs 6 categories) / per-impl extension over-engineering / substrate-bound running instance as separate primitive.

**Round 1 termination position FAILURE**: Round 1 self-check produced premature STABLE LOCK — missed `decision-design-sharpening` v0.6.0 layered coverage observation (R1 = arch / R2 = cross-cutting + schema-detail). Root cause: applied skill from synthesized memory of prior usage WITHOUT Reading SKILL.md (procedural fidelity failure; canonical session-16 case documented in `learnings/ai-app-development.md` Observation 28 + `drafts/execution-fidelity.md`).

### Round 2 (USER-TRIGGERED; cross-cutting + schema-detail layer per layered coverage observation)

After user prompted skill check ("do check our specialised sharpening skills") + SKILL.md re-Read, surfaced 11 EXPANSIONS:

1. Boot + shutdown phase ordering (NEW §10)
2. Substrate error categories (NEW §11)
3. Transport variation + per-tier mapping (NEW §12)
4. Deployment-tier awareness (NEW §13)
5. Audit-trail integration architectural-event kinds (enriched §8)
6. Specialist registration as Surface category G — Surface 6→7 categories (REVISION-flavored EXPANSION; corrects Round 1 omission per session-13 archive amendment)
7. Composition with `session` primitive (added to §7)
8. Lifecycle ownership clarification in §9 (creator / mutability / cross-session-persistence)
9. §14 retitled "Pre-implementation operational concerns (Phase 6 forward reference)"
10. Substrate-coupling impossible-by-construction (added to §6 tri-aspect; per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1)
11. Watch-list W1: substrate-pluggability discipline-section promotion at Phase 3.8 (refined from archived W7)

**Round 2 manufactured criticisms rejected (0; all 11 surfaced were Pareto-improving)**.

### Retroactive profile-anchored validation pass (post-procedural-discipline lock)

After 5-location procedural redundancy locked (canonical session-16 fix for skill+profile pattern-matching failure), applied properly-grounded profile-anchored validation:

- Read `profiles/INDEX.md` (cluster A/B/C/D structure)
- Read FULL DETAIL profiles: `G-composability-gate.md` + `L5a-planner-pbs-schulz.md`
- Read SKELETON-but-EXEMPLIFIES profiles: `L1-specialist-creator.md` + `L4a-workspace-deployer-solo.md` + `L8-auditor-reviewer-posthoc.md`
- Per-cluster profile content cited in arch/substrate.md cross-references (§18 Profiles validated)

**4/4 clusters PASS with cited profile content** (not pattern-matched cluster letters). 0 architectural REVISIONS surfaced; profile content REINFORCES Round 1 + Round 2 expansions.

### Sharpening totals

| Round | EXPANSIONS | REVISIONS | Manufactured-criticism rejected |
|---|---|---|---|
| Round 1 | 2 | 0 | 3 |
| Round 2 | 11 | 0 | 0 |
| Profile validation | 0 (reinforced) | 0 | 0 |
| **Total** | **13** | **0** | **3** |

### Retroactive greenfield-pass amendment (session 16; post-Phase-3.4-#4; `DISCIPLINES.md` Discipline 10)

User-triggered audit: investigated WHY procedural laxness allowed `arch/coordination.md` Round 1 cargo-cult drift. Concern: laxness pattern likely affected earlier locked work too. HIGH-risk Phase 3.4 topics (substrate + audit) audited per Discipline 10 discriminator (re-validate / stress-test / pattern-vs-instance / greenfield-derive per archive-derived element).

**substrate.md audit findings**:

| Element | Source | Verdict |
|---|---|---|
| 7 Surface capability categories | Archive (`substrate-protocol-design.md`) | GREENFIELD-VALID — each independently derives from locked architecture |
| Per-impl extension Protocols pattern | Archive (`sdk-deep-read.md` R3d) | GREENFIELD-VALID — per TOP-LEVEL DESIGN PRINCIPLES §1 wrong-shapes-impossible (typed Protocols + isinstance = structural) |
| Boundary criteria (5-row decision rule) | Archive R3d P4 | GREENFIELD-VALID |
| 3 substrate Implementations (CIRCA 2026) | Archive (`substrate-agentic-framework.md`) | GREENFIELD-VALID — time-stamping properly applied |
| **Boot/shutdown phase ordering (§10)** | Archive (`substrate-protocol-design.md` round-2 Q6) | **REVISION-1 REQUIRED** — substrate-flushes-audit-trail contradicts `arch/audit.md` §11 (locked later; audit Protocol owns flush; shuts down AFTER substrate) |
| Substrate error categories (5) | Archive round-2 Q2 | GREENFIELD-VALID |
| Transport variation (3 modes) | Archive | GREENFIELD-VALID |
| Deployment-tier awareness | Archive | GREENFIELD-VALID |
| Substrate-internal direct emission | Archive | GREENFIELD-VALID — structurally required (resolves MCP-gate-circularity) |
| Per-shape error semantics | Greenfield-derived (not archive) | GREENFIELD-VALID |

**REVISION-1 applied this commit**: §10 boot sequence adds Audit-Protocol-must-be-booted precondition; §10 shutdown sequence removes substrate-flushes-audit-trail step; explicit cross-ref to `arch/audit.md` §11 for ordering. Substrate releases its own runtime resources; Audit Protocol's later shutdown handles audit-trail flush + integrity verification.

**Root cause of REVISION-1**: archived `substrate-protocol-design.md` had no Audit-Protocol-as-separate-Pattern-A; substrate handled audit-trail flush directly. When `arch/audit.md` locked Audit Protocol AS Pattern A (Phase 3.4 #4), the cascade back to substrate.md §10 was missed. Canonical greenfield-evaluation failure mode: substrate.md adopted archive's substrate-handles-audit-trail commitment without re-validating after audit Protocol Pattern A locked.

**arch/audit.md audit findings**: 0 architectural REVISIONS. Audit topic was written LATER in Phase 3.4 sequence with stronger procedural awareness; audit-trail-as-canonical-source + audit-Protocol-shuts-down-AFTER-substrate are greenfield-derived architectural commitments that properly composed with already-locked substrate (which is why audit topic surfaced the substrate-handles-audit-trail issue and broke the dependency at lock time — but the cascade back to substrate.md was missed).

**Audit corpus totals**: 1 architectural REVISION across HIGH-risk topics (substrate + audit). Validates user's worry that procedural laxness introduced architectural drift; magnitude tractable (1 cross-topic inconsistency, not deep cargo-cult).

## Composition with existing architecture

- Surface + per-impl + Selection = Pattern A pluggable subsystem template (per ARCHITECTURE.md §6 Pattern-A semantics) — sets pattern for adapter / sparring / audit / coordination / trust / time / quality-gate per-protocol topics
- Tri-aspect Pattern A reconciliation distinct from Pattern B (specialist / workflow / work-unit) bipartite — preserves locked GLOSSARY classification
- Cross-cutting concern composition: substrate's Surface categories compose with adapter's Surface (auth-bound channels) + audit's Surface (event emission + audit-trail integrity) + coordination's actor primitives + trust's authority-binding + time's temporal semantics — substrate is foundational
- Logic placement modes (4-mode distribution per ARCHITECTURE.md §6): Surface contract = Mode 4 conceptual articulation here + Mode 3 Pydantic Protocol at Phase 6 spec; production-runtime AI doesn't load this topic (Mode 4 boundary)

## Constraints flowing to downstream commitments

### → Phase 3.4 remaining ARCH topics (adapter / sparring / audit / coordination / trust / time / quality-gate)

- Pattern A topic structure precedent: 18-section template established by substrate.md
- Surface + per-impl + Selection pattern: each Pattern A protocol follows same structure
- Common-surface boundary criteria template: each Pattern A protocol applies analogous decision rule
- Composition cross-references to substrate's Surface categories (where relevant): every Pattern A protocol composes with substrate

### → Phase 3.5 primitive cluster topics (specialist+skill / practitioner / workflow+work-unit / claim+defensibility) + cross-cutting integrators (scope-model / axis-interactions)

- specialist+skill topic composes with substrate's Surface category G (specialist registration)
- workflow+work-unit topic references substrate's session/context-management Surface category F
- claim+defensibility topic references substrate's audit-trail integration (substrate-emitted + skill-emitted dual paths)
- axis-interactions integrator references how substrate hosts all 3 axes' runtime behavior

### → Phase 3.6 quality-gate ARCH topic

- Quality-gate Pattern A protocol is substrate-agnostic (composes with substrate's audit emission + permission flow); shape policy declares enforcement
- Per-axis observability via substrate-emitted audit-event kinds (§8 enumeration)

### → Phase 6 spec

- Pydantic Protocol contract for Substrate Surface (7 capability categories typed)
- SubstrateError class hierarchy (per §11 architectural categories)
- Supporting Pydantic types (TransportMode / DeploymentTier / SubstrateConfig / HookEvent / SessionContext / etc.)
- Concrete substrate Implementations: ClaudeAgentSDKSubstrate (full backend + frontend via Cowork) / MSAgentFrameworkSubstrate (full backend) / HandRolledSubstrate (Tier 1 fallback)
- Per-substrate extension Protocols: ClaudeAgentSDKExtensions (subagent + session forking + permission + sandbox + thinking + Channels) / MSAgentFrameworkExtensions (workflow + checkpointing + evaluation + 6+ compaction strategies + 3-layer middleware + history providers)
- Pre-implementation sharpening at Phase 6 implementation-start (operational/runtime concerns per §14 forward reference)

### → ARCHITECTURE.md cascade

- Phase 3 sub-phase status update: 3.4 partially complete (1 of 8 topics drafted); status table updated
- Topic catalog row for substrate: status drafted (per locked Phase 3.2 conventions)
- Locked decisions section: substrate ARCH topic added to locked set

## Files touched (this DR)

- `arch/substrate.md` (NEW; 18 sections; locked Phase 3.4 first canonical arch topic)
- `docs/decisions/substrate-arch-topic.md` (this file; NEW; status ACCEPTED)
- `ARCHITECTURE.md` (cascade-update: Phase 3.4 sub-phase status; substrate topic catalog row drafted-status; locked decisions section)
- `BACKLOG.md` (cascade-update: Phase 3.4 substrate moved to Resolved; remaining 7 Pattern A protocol topics flagged Pending)
- `HANDOFF.md` (Note 35: substrate ARCH topic locked; first canonical arch/<topic>.md established; profile-anchored validation properly executed under 5-location procedural discipline)

## Revisit triggers

- New substrate candidate emerges (Watch-list W2): re-evaluate against boundary criteria (§3); add as new Implementation OR document why not
- SDK API drift triggering Surface revision (Watch-list W3): re-validate Surface contract against new SDK shape; affected Surface category amendments trigger DR amendment per cascade discipline
- Tier 3 substrate-determines-deployment-platform reframing (Watch-list W4): per-platform deployment-detail decisions land at deployment time
- Phase 3.8 ARCH-discipline coherence-audit (Watch-list W1): evaluate whether per-substrate extension Protocols pattern deserves dedicated ARCH discipline section vs staying as Pattern-A-protocol-instance discussion in this topic
- Phase 6 pre-implementation sharpening surfaces architectural flow-back (~10-20% per `pre-implementation-sharpening` skill); flow back as DR amendment per two-phase pattern

## Pattern note (meta)

This DR's sharpening was **paused mid-Round-1** by user-detected procedural-fidelity failure (AI applied decision-design-sharpening from synthesized memory; missed layered coverage observation). User intervention triggered:

1. SKILL.md re-Read (corrects within-session procedural drift)
2. 5-location procedural redundancy lock (structural fix; commit `be7c8fa`)
3. Round 2 properly executed under just-codified discipline
4. Retroactive profile-anchored validation under just-codified discipline (≥3 cluster representatives Read; cited profile content)

The DR thus serves as canonical session-16 case for `DISCIPLINES.md` Discipline 1 (skill+profile sub-section) discipline. The pattern note belongs in DR provenance because the procedural-fidelity work was load-bearing for this DR's correctness.
