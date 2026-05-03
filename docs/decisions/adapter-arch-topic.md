# Decision record: Adapter ARCH topic (Phase 3.4 second Pattern A protocol topic)

## Status

ACCEPTED. 2-round sharpening (Round 1 full monty + Round 2 cross-cutting + schema-detail per `decision-design-sharpening` v0.6.0 layered coverage observation) under procedural-fidelity discipline (`DISCIPLINES.md` Discipline 1 (skill+profile sub-section)).

## Owner

Phase 3.4 Per-architectural-Protocol detail rebuild; second Pattern A protocol topic (substrate first; adapter second per foundation-up ordering).

## Related

- Locked GLOSSARY adapter entry (Pattern A tri-aspect; cross-axis; multi-instance; internal-vs-external axis distinction from substrate)
- `arch/substrate.md` (substrate Surface §B MCP registration + §C permission flow + §8 dual audit emission compose with adapter operations)
- `docs/decisions/phase-3-2-doc-organization.md` (composite Phase 3.2 lock; topic catalog Sub-decision 1; arch/<slug>.md naming Sub-decision 2)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)
- Archived sources (in `archive/docs/`): a2a-and-gemini-pattern-emulation DR, plugin-conventions, backend-conventions

## Context

Adapter is the second Pattern A protocol topic in Phase 3.4 sequence (foundation-up: substrate → adapter → remaining). Establishes pattern variation for "multi-instance Pattern A with per-integration-class Surfaces" — distinct from substrate's "singular Pattern A with single Surface."

Critical architectural distinctions from substrate (load-bearing for the topic's correctness):
- **Internal-vs-external axis**: substrate INTERNAL runtime contract; adapter EXTERNAL integration boundary
- **Cardinality**: substrate singular per workspace; adapter typically multiple
- **Surface granularity**: substrate single Surface; adapter META-Surface + per-integration-class Surfaces (5 named: email / accounting / MCP-server / A2A-peer / file-sync)
- **Audit emission**: substrate dual-paths (internal direct + skill-side via MCP gate); adapter skill-side ONLY (no circularity issue)

## Decision

`arch/adapter.md` LOCKED with Pattern A common-required + adapter-conditional sections per `MAINTENANCE.md` Pattern A protocol topic template:

1. Topic scope (adapter as Pattern A; cross-axis; multi-instance; internal-vs-external axis distinction from substrate)
2. Two-layer Surface (META-Surface conventions + per-integration-class Surfaces — 5 currently)
3. Common-surface boundary criteria (META vs per-class vs implementation-internal — applies per template since adapter has multi-class Surface)
4. Per-implementation aspect (Pattern level + current Implementation set per class + bidirectional vs unidirectional architectural patterns)
5. Selection mechanics (workspace.md adapter bindings list; multi-instance; hot-swap re-binding mid-workspace-life)
6. Tri-aspect reconciliation (META-Surface + per-class Surfaces / Implementations / Running Instance(s); adapter-internal vs external state separation)
7. Composition with framework primitives (15+ cross-references; substrate composition load-bearing)
8. Substrate-internal vs skill-side audit emission — N/A (substrate-conditional per template; adapter has no MCP-gate circularity; adapter emits skill-side only via MCP audit gate)
9. Cardinality + lifecycle (multi-instance cardinality; lifecycle ownership; mutability; cross-session persistence; versioning + hot-swap migration)
10. Lifecycle phase ordering + auth refresh (adapter-conditional; per-class auth models; auth-refresh lifecycle; per-instance boot/shutdown sequence in reverse declaration order)
11. Per-integration-class error categories + audit event-kind catalog (adapter-conditional; cross-class architectural categories + per-class refinements + per-shape error semantics + quota / rate-limit / circuit-breaker semantics + per-class audit event-kind catalog relocated from §8)
12. Transport variation + per-tier mapping — N/A (substrate-specific; adapter operates over per-class transports declared per Implementation; transport choice impl-internal per per-class Surface satisfaction)
13. Deployment-tier awareness — N/A (substrate-specific; adapter behavior is shape-class-shape + integration-class-shape, not tier-shape; per-impl tier-compatibility declared in §4)
14. Cross-shape policy variation (per Pattern A template 7th conditional per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` — applies per shape-policy-mediated nature: per-shape audit emission / permission flow / error escalation)
15. Pre-implementation operational concerns (Phase 6 forward reference)
15. Watch-list (W1-W5)
16. Decision-design provenance
17. Phase routing
18. Cross-references

**Section count**: 12 common-required + 7 protocol-specific-conditional sections per Pattern A / mechanism-class topic template (per `MAINTENANCE.md` Layer 3 description post `pattern-a-template-7th-conditional-cross-shape-variation.md`). Adapter applies §3 (multi-class Surface) + §10 (multi-instance lifecycle phase ordering + auth-refresh) + §11 (per-impl errors + per-class audit catalog) + §14 (cross-shape policy variation per shape-policy-mediated nature); §8 + §12 + §13 N/A explicitly per template applicability rules.

## Sharpening provenance

### Round 1 (full monty; architectural decisions layer)

8 EXPANSIONS surfaced:
1. Topic structure: same Pattern A template as substrate
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

### GLOSSARY back-check (Round 2 termination)

Considered: multi-instance-Pattern-A as standalone classification refinement; auth-state-at-Owner-B as new sub-category. **Verdict: NOT glossary-grade** — already implicit in `protocol (architectural)` GLOSSARY entry's "cardinality variation between substrate and adapter" + Owner B scope's existing entity-state framing. **No retro-fit fires.**

### REVISION/EXPANSION self-check (per skill v0.6.0)

All 20 EXPANSIONS classified additive coverage; none REVISION-flavored. 2-tier classification holds; signal hasn't materialized for 3-tier codification per BACKLOG watch-list.

### Profile-anchored validation

4/4 clusters PASS with cited profile content (G + L5a + L1 + L4a + L8):

- **Cluster A (L1)**: "Specialist DEFINITION boundary (Framework C)" + composes-with bundling adapter implementations — DIRECTLY validates §4 + §7 specialist composition
- **Cluster B (L4a + L5a)**: L5a line 90 "Active adapters: email (Outlook); LaTeX compile; document signing" + L4a line 23 "Adapter configuration: email integration; document-signing; LaTeX compile" — DIRECTLY validates §5 multi-instance + per-archetype adapter set
- **Cluster C (L5a)**: L5a line 66 "ad-hoc: communication (one-off email to municipality coordinator)" — adapter cross workflow_instance ↔ ad-hoc — validates §1 cross-axis + adapter operations during both modes
- **Cluster D (G + L8)**: G line 157 "Cross-shape consumption ... Shape's policy bundle determines if specialist activates fully or partially" — DIRECTLY validates §14 cross-shape policy variation; L8 line 29 audit-trail integrity validates §11 + §10

### Sharpening totals

| Round | EXPANSIONS | REVISIONS | Manufactured-criticism rejected |
|---|---|---|---|
| Round 1 | 8 | 0 | 3 |
| Round 2 | 12 | 0 | 2 |
| **Total** | **20** | **0** | **5** |

### Greenfield-rederivation v2 amendments

Subsequent greenfield-rederivation cluster execution (per `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-4-substrate-adapter.md`) surfaced cascade-miss findings applied to `arch/adapter.md`:
- A1 frontmatter: Round-breadcrumb stripped; topic-cluster updated 8-to-3 (3 Pattern A topics post-greenfield-rederivation v1: substrate / adapter / quality-gate)
- A3 §8 reframed: per-class audit event-kind catalog relocated to §11; §8 itself N/A-with-rationale per Pattern A template applicability (substrate-specific dual-emission framing not applicable to adapter)
- A4 §9 renamed: "Auth + lifecycle semantics" → "Cardinality + lifecycle" per template; auth content moved to §10
- A5 §10/§11/§12/§13 renumbered to match Pattern A template: §10 adapter-conditional (lifecycle phase ordering + auth refresh); §11 adapter-conditional (per-impl errors + audit event-kind catalog); §12/§13 N/A explicit; §13a appendix for cross-shape policy variation
- A6 §16 archive citations: Discipline 10 INPUT-only framing added per `disciplines/10-greenfield-evaluation.md`
- A7 §18 cross-references: rephrased to cite existing `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 "make wrong shapes impossible"; coined "adapter-coupling impossible-by-construction" replaced with the locked principle

## Composition with existing architecture

- Two-layer Surface pattern (META + per-class) establishes precedent for ARCH topics where Pattern A protocol has per-instance-class semantic variation. Future Pattern A protocol topics may adopt this pattern if per-class semantic coherence applies.
- Internal-vs-external axis (substrate vs adapter) introduces architectural-axis vocabulary potentially useful for other Pattern A protocols (audit = INTERNAL emission; trust = EXTERNAL handshakes; coordination = MIXED). Not formalized as cross-cutting yet; may surface at Phase 3.5 cross-cutting integrators.
- Adapter operations compose with substrate's permission flow (Surface §C) + MCP server registration (Surface §B) + dual audit emission (§8). Substrate is foundational; adapter is layered above.
- Cross-shape policy variation (§14 per Pattern A template 7th conditional) anchors shape-policy-mediated adapter behavior — sets pattern for how shape policies modulate Pattern A protocol behavior. Quality-gate ARCH topic (Phase 3.6) will compose with adapter audit emission + quota metrics for observability.

## Constraints flowing to downstream commitments

### → Phase 3.4 remaining ARCH topic (quality-gate)

- Pattern A topic structure precedent: common-required + conditional sections per template; adapter validates two-layer Surface variation + multi-instance lifecycle conditional; quality-gate may have per-axis Surface variation
- META-Surface + per-class Surface pattern available where applicable
- Composition with substrate's foundational mechanisms (permission flow + MCP registration + audit emission) applies to all Pattern A protocols at this layer

### → Phase 3.5 primitive cluster topics + cross-cutting integrators

- specialist+skill topic composes with adapter via specialist bundling adapter Implementations (per `specialist` GLOSSARY entry composes-with)
- workflow+work-unit topic references adapter operations during workflow_instance execution (per L5a hybrid moments)
- claim+defensibility topic references adapter audit-event integration (axis-3 send operations are claim-attestation moments)
- scope-model integrator references Owner B scope adapter-instance-state + auth-token-state security boundary
- axis-interactions integrator references adapter cross-axis serving (email = axis-3; accounting = cross-cutting; MCP = cross-axis)

### → Phase 3.6 quality-gate ARCH topic

- Quality-gate observability via adapter audit-event emission + per-class quota/rate-limit metrics
- Per-shape quality-gate enforcement composes with adapter cross-shape policy variation (§14)
- Shape policy declares per-shape adapter-action enforcement at workspace boot

### → Phase 6 spec

- Pydantic Protocol contracts: META-Surface + 5 per-class Surfaces (Email / Accounting / MCP-Server / A2A-Peer / File-Sync)
- Per-impl Implementations: gmail / outlook / fastbill / lexware / Anthropic-MCP / A2A-protocol / etc.
- Auth + lifecycle persistence mechanics (per-shape encryption; per-impl persistence schemas)
- Hot-swap migration mechanics (workflow_instance re-binding compatibility)
- Multi-account scenarios (W4 watch-list)
- Pre-implementation sharpening at Phase 6 implementation-start

## Files touched

- `arch/adapter.md` (locked Phase 3.4 second Pattern A protocol topic)
- `docs/decisions/adapter-arch-topic.md` (this file)
- `ARCHITECTURE.md` (cascade-update: Phase 3.4 progress; topic catalog adapter row drafted; locked decisions section)
- `BACKLOG.md` (cascade-update: Phase 3.4 adapter Resolved)
- `HANDOFF.md` (adapter ARCH topic locked; second Pattern A protocol topic; two-layer Surface pattern established)

## Revisit triggers

- New per-class Surface emergence (Watch-list W1; e.g., document-signing per pioneer reality)
- Federation-shape mature → A2A-Peer Surface refinement (W2)
- Document-signing as candidate per-class Surface (W3; pioneer experience accumulates)
- Multi-account same-class binding patterns (W4)
- Cross-adapter operation atomicity (W5; defer to coordination ARCH topic)
- Phase 6 pre-implementation sharpening surfaces architectural flow-back (~10-20% per `pre-implementation-sharpening` skill)
- New adapter Implementation submitted (per cascade discipline; impl declares class + Surface satisfaction; class Surface validates)
