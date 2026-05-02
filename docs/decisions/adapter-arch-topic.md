# Decision record: Adapter ARCH topic (Phase 3.4 second Pattern A protocol topic)

**Status**: ACCEPTED — session 16 (2026-05-02); 2-round sharpening (Round 1 full monty + Round 2 cross-cutting + schema-detail per `decision-design-sharpening` v0.6.0 layered coverage observation) under just-codified procedural-fidelity discipline (`feedback_skill_files_are_sources.md`).

**Owner**: Phase 3.4 Per-architectural-Protocol detail rebuild; second Pattern A protocol topic (substrate first; adapter second per foundation-up ordering).

**Related**:
- Locked GLOSSARY adapter entry (Pattern A tri-aspect; cross-axis; multi-instance; internal-vs-external axis distinction from substrate)
- `arch/substrate.md` (substrate Surface §B MCP registration + §C permission flow + §8 dual audit emission compose with adapter operations)
- `phase-3-2-doc-organization.md` (composite Phase 3.2 lock; topic catalog Sub-decision 1; arch/<slug>.md naming Sub-decision 2)
- `feedback_skill_files_are_sources.md` (procedural discipline applied throughout)
- Archived sources: `a2a-and-gemini-pattern-emulation.md`, `plugin-conventions.md`, `backend-conventions.md`

## Context

Adapter is the second Pattern A protocol topic in Phase 3.4 sequence (foundation-up: substrate → adapter → 6 remaining). Establishes pattern variation for "multi-instance Pattern A with per-integration-class Surfaces" — distinct from substrate's "singular Pattern A with single Surface."

Critical architectural distinctions from substrate (load-bearing for the topic's correctness):
- **Internal-vs-external axis**: substrate INTERNAL runtime contract; adapter EXTERNAL integration boundary
- **Cardinality**: substrate singular per workspace; adapter typically multiple
- **Surface granularity**: substrate single Surface; adapter META-Surface + per-integration-class Surfaces (5 named: email / accounting / MCP-server / A2A-peer / file-sync)
- **Audit emission**: substrate dual-paths (internal direct + skill-side via MCP gate); adapter skill-side ONLY (no circularity issue)

## Decision

`arch/adapter.md` LOCKED with 18 sections covering:

1. Topic scope (adapter as Pattern A; cross-axis; multi-instance; internal-vs-external axis distinction from substrate)
2. Two-layer Surface (META-Surface conventions + per-integration-class Surfaces — 5 currently)
3. Common-surface boundary criteria (META vs per-class vs implementation-internal)
4. Per-implementation aspect (Pattern level + current Implementation set per class + bidirectional vs unidirectional architectural patterns)
5. Selection mechanics (workspace.md adapter bindings list; multi-instance; hot-swap re-binding mid-workspace-life)
6. Tri-aspect reconciliation (META-Surface + per-class Surfaces / Implementations / Running Instance(s); adapter-internal vs external state separation)
7. Composition with framework primitives (15+ cross-references; substrate composition load-bearing)
8. Per-action audit emission via MCP gate (skill-side ONLY; per-class event-kind catalog + cross-class architectural events)
9. Auth + lifecycle semantics (per-class auth models; refresh lifecycle; per-instance lifecycle ordering)
10. Per-integration-class error categories (cross-class architectural categories + per-class refinements)
11. Cross-shape policy variation (per `profiles/G-composability-gate.md` line 157)
12. Quota + rate-limit + circuit-breaker semantics
13. Versioning + migration (semver; hot-swap mechanics)
14. Pre-implementation operational concerns (Phase 6 forward reference)
15. Watch-list (W1-W5)
16. Decision-design provenance
17. Phase routing
18. Cross-references

## Refinements applied

### Round 1 (full monty; architectural decisions layer)

8 EXPANSIONS surfaced:
1. Topic structure: same 18-section template as substrate (Pattern A consistency)
2. Surface granularity: per-integration-class (NOT monolithic) — locked by GLOSSARY claim
3. Cardinality: multiple adapter instances per workspace (norm; pioneer concrete reality per L5a line 90)
4. Distinction from substrate: internal-vs-external axis explicit
5. Audit emission: skill-side via MCP gate (NOT substrate-internal direct)
6. Permission flow: explicit composition with substrate Surface §C
7. Bidirectional vs unidirectional: per-integration-class architectural shape
8. Pre-implementation operational concerns: external-world-specific (auth refresh, quota, circuit breaker, etc.)

3 manufactured-criticism revisions rejected:
- "Per-integration-class granularity over-engineering; one monolithic Adapter Protocol?" → REJECT (semantically incoherent across classes; GLOSSARY locks per-class)
- "Adapter merge into substrate as 'external substrate'?" → REJECT (internal-vs-external axis is locked architectural distinction)
- "Audit-emission-via-MCP-gate creates dependency on substrate Read?" → ACCEPT scoping; REJECT as Round-1-pivot (this IS the locked relationship per substrate's §8)

### Round 2 (USER-TRIGGERED; cross-cutting + schema-detail layer)

12 EXPANSIONS surfaced:
1. Auth + lifecycle semantics architectural-level
2. Per-integration-class error categories (cross-class + per-class refinements)
3. Multi-instance lifecycle ordering (distinct from substrate's singular)
4. Quota + rate-limit per integration class
5. Circuit-breaker semantics
6. Per-action audit-event kinds (architectural enumeration per class + cross-class)
7. Permission flow composition with substrate Surface §C explicit
8. Cross-shape policy variation explicit
9. Adapter-internal vs adapter-external state separation
10. Hot-swap / re-binding semantics
11. Versioning + migration per Implementation
12. Bidirectional vs unidirectional shape detail per per-class Surface

2 manufactured-criticism revisions rejected:
- "Multi-instance Pattern A as new META-classification?" → REJECT (inflates primitive count; Pattern A admits cardinality variation per locked GLOSSARY)
- "Hot-swap defer to Phase 6?" → REJECT (architectural commitment; load-bearing for L4a deployer)

### GLOSSARY back-check (per Round 2 termination)

Considered: multi-instance-Pattern-A as standalone classification refinement; auth-state-at-Owner-B as new sub-category. **Verdict: NOT glossary-grade** — already implicit in `protocol (architectural)` GLOSSARY entry's "cardinality variation between substrate and adapter" + Owner B scope's existing entity-state framing. **No retro-fit fires.**

### REVISION/EXPANSION self-check (per skill v0.6.0)

All 20 EXPANSIONS classified additive coverage; none REVISION-flavored. 2-tier classification holds; signal hasn't materialized for 3-tier codification per BACKLOG watch-list.

### Profile-anchored validation

4/4 clusters PASS with cited profile content (current-context profiles G + L5a + L1 + L4a + L8 still in evidence from substrate Round 2 retroactive pass):

- **Cluster A (L1)**: "Specialist DEFINITION boundary (Framework C)" + composes-with bundling adapter implementations — DIRECTLY validates §4 + §7 specialist composition
- **Cluster B (L4a + L5a)**: L5a line 90 "Active adapters: email (Outlook); LaTeX compile; document signing" + L4a line 23 "Adapter configuration: email integration; document-signing; LaTeX compile" — DIRECTLY validates §5 multi-instance + per-archetype adapter set
- **Cluster C (L5a)**: L5a line 66 "ad-hoc: communication (one-off email to municipality coordinator)" — adapter cross workflow_instance ↔ ad-hoc — validates §1 cross-axis + adapter operations during both modes
- **Cluster D (G + L8)**: G line 157 "Cross-shape consumption ... Shape's policy bundle determines if specialist activates fully or partially" — DIRECTLY validates §11 cross-shape policy variation; L8 line 29 audit-trail integrity validates §8 + §10

### Sharpening totals

| Round | EXPANSIONS | REVISIONS | Manufactured-criticism rejected |
|---|---|---|---|
| Round 1 | 8 | 0 | 3 |
| Round 2 | 12 | 0 | 2 |
| **Total** | **20** | **0** | **5** |

## Composition with existing architecture

- Two-layer Surface pattern (META + per-class) establishes precedent for ARCH topics where Pattern A protocol has per-instance-class semantic variation. Future Pattern A protocol topics may adopt this pattern if per-class semantic coherence applies.
- Internal-vs-external axis (substrate vs adapter) introduces architectural-axis vocabulary potentially useful for other Pattern A protocols (audit = INTERNAL emission; trust = EXTERNAL handshakes; coordination = MIXED). Not formalized as cross-cutting yet; may surface at Phase 3.5 cross-cutting integrators.
- Adapter operations compose with substrate's permission flow (Surface §C) + MCP server registration (Surface §B) + dual audit emission (§8). Substrate is foundational; adapter is layered above.
- Cross-shape policy variation (§11) anchors shape-policy-mediated adapter behavior — sets pattern for how shape policies modulate Pattern A protocol behavior. Quality-gate ARCH topic (Phase 3.6) will compose with adapter audit emission + quota metrics for observability.

## Constraints flowing to downstream commitments

### → Phase 3.4 remaining ARCH topics (sparring / audit / coordination / trust / time / quality-gate)

- Pattern A topic structure precedent: 18-section template established by substrate.md; adapter validates two-layer Surface variation
- META-Surface + per-class Surface pattern available where applicable (sparring may have per-shape Surface variation; audit may have per-axis Surface variation)
- Composition with substrate's foundational mechanisms (permission flow + MCP registration + audit emission) applies to all Pattern A protocols at this layer

### → Phase 3.5 primitive cluster topics + cross-cutting integrators

- specialist+skill topic composes with adapter via specialist bundling adapter Implementations (per `specialist` GLOSSARY entry composes-with)
- workflow+work-unit topic references adapter operations during workflow_instance execution (per L5a hybrid moments)
- claim+defensibility topic references adapter audit-event integration (axis-3 send operations are claim-attestation moments)
- scope-model integrator references Owner B scope adapter-instance-state + auth-token-state security boundary
- axis-interactions integrator references adapter cross-axis serving (email = axis-3; accounting = cross-cutting; MCP = cross-axis)

### → Phase 3.6 quality-gate ARCH topic

- Quality-gate observability via adapter audit-event emission + per-class quota/rate-limit metrics
- Per-shape quality-gate enforcement composes with adapter cross-shape policy variation (§11)
- Shape policy declares per-shape adapter-action enforcement at workspace boot

### → Phase 6 spec

- Pydantic Protocol contracts: META-Surface + 5 per-class Surfaces (Email / Accounting / MCP-Server / A2A-Peer / File-Sync)
- Per-impl Implementations: gmail / outlook / fastbill / lexware / Anthropic-MCP / A2A-protocol / etc.
- Auth + lifecycle persistence mechanics (per-shape encryption; per-impl persistence schemas)
- Hot-swap migration mechanics (workflow_instance re-binding compatibility)
- Multi-account scenarios (W4 watch-list)
- Pre-implementation sharpening at Phase 6 implementation-start

## Files touched (this DR)

- `arch/adapter.md` (NEW; 18 sections; locked Phase 3.4 second Pattern A protocol topic)
- `docs/decisions/adapter-arch-topic.md` (this file; NEW; status ACCEPTED)
- `ARCHITECTURE.md` (cascade-update: Phase 3.4 progress 2 of 8; topic catalog adapter row drafted; locked decisions section)
- `BACKLOG.md` (cascade-update: Phase 3.4 adapter Resolved; remaining 6 Pattern A protocol topics pending)
- `HANDOFF.md` (Note 36: adapter ARCH topic locked; second Pattern A protocol topic; two-layer Surface pattern established)

## Revisit triggers

- New per-class Surface emergence (Watch-list W1; e.g., document-signing per pioneer reality)
- Federation-shape mature → A2A-Peer Surface refinement (W2)
- Document-signing as candidate per-class Surface (W3; pioneer experience accumulates)
- Multi-account same-class binding patterns (W4)
- Cross-adapter operation atomicity (W5; defer to coordination ARCH topic)
- Phase 6 pre-implementation sharpening surfaces architectural flow-back (~10-20% per `pre-implementation-sharpening` skill)
- New adapter Implementation submitted (per cascade discipline; impl declares class + Surface satisfaction; class Surface validates)

## Pattern note (meta)

Adapter as second Pattern A protocol topic VALIDATES substrate-established 18-section template AND introduces two-layer Surface variation (META + per-class). Pattern: ARCH topics for Pattern A protocols with per-instance-class semantic variation can adopt two-layer Surface; ARCH topics for singular-shape Pattern A protocols use single-layer Surface (substrate). Decision criterion: does per-instance-class admit semantic coherence within class but heterogeneity across classes? If yes → two-layer; if no → single-layer.

This DR also serves as second canonical execution of the just-codified procedural fidelity discipline (`feedback_skill_files_are_sources.md`) post-substrate-Round-2-retroactive-pass — chat output cited specific skill section names (layered coverage observation; Round 2 cross-cutting + schema-detail layer; GLOSSARY back-check at Round 2 termination; REVISION/EXPANSION self-check; profile-anchored validation cluster citations) per verification discipline.
