# Decision record: Sparring ARCH topic (Phase 3.4 third Pattern A protocol topic)

## Status

ACCEPTED — session 16 (2026-05-02); 2-round sharpening per `decision-design-sharpening` v0.6.0 layered coverage observation. Persisted under DR template locked in `MAINTENANCE.md` Layer 4 (per `doc-organization-templates.md` composite DR).

## Owner

Phase 3.4 Per-architectural-Protocol detail rebuild; third Pattern A protocol topic (substrate first; adapter second; sparring third per foundation-up ordering).

## Related

- Locked GLOSSARY `sparring (axis 2)` entry (DERIVED axis-2 success mode; Sparring Protocol = Pattern A primitive; 8 sub-mechanisms)
- Locked GLOSSARY `answer-machine AI` / `oracle AI` / `validator AI` entries (axis-2 failure modes)
- Locked GLOSSARY `engaged authorship` entry (sparring events ARE the production-phase substrate for engaged-authorship two-phase composite)
- `arch/substrate.md` (Surface §B hook registration + §D structured output validation; load-bearing for architecturally-encoded sub-mechanisms)
- `arch/adapter.md` (skill-side audit emission discipline pattern; sparring follows same shape)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (architecturally-encoded vs behaviorally-enforced discriminator)
- `doc-organization-templates.md` (DR template + arch/<topic>.md template)
- Archived sources: `archive/docs/decisions/sparring-output-v1.md`

## Context

Sparring is the third Pattern A protocol topic in Phase 3.4 sequence (foundation-up: substrate → adapter → sparring → 5 remaining). Validates Pattern A 18-section template + introduces NEW per-shape activation-matrix variation (substrate = singular tier-aware; adapter = multi-instance per-class; sparring = singular per-shape-policy-driven sub-mechanism activation).

Critical architectural distinctions:
- **Single-layer Surface** (substrate-style; NOT adapter's two-layer META + per-class)
- **8 sub-mechanism capability categories**: 4 architecturally-encoded + 4 behaviorally-enforced per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator
- **Per-shape activation matrix**: shape policy declares which sub-mechanisms active (NOT impl-multiplicity like adapter; NOT singular-forever like substrate)
- **Cross-axis dependency**: sparring fires per claim; sparring events ARE production-phase substrate for engaged-authorship two-phase composite (axis-2 → axis-3)

## Decision

`arch/sparring.md` LOCKED with 18 sections per Pattern A protocol topic template. Surface = 8 sub-mechanism capability categories: counter-argument / confidence calibration / visible reasoning / selective friction (architecturally-encoded); anti-sycophancy / asymmetric knowledge respect / commit-to-recommendations / what's-missing (behaviorally-enforced).

Architectural shape locked; Pydantic Protocol contract + per-sub-mechanism schemas → Phase 6 spec.

## Sharpening provenance

### Round 1 (full monty; architectural decisions layer per layered coverage observation)

7 EXPANSIONS surfaced:
1. Single-layer Surface (substrate-style; sub-mechanisms are capability categories of unified axis-2 concern)
2. 8 sub-mechanism capability categories per locked GLOSSARY
3. Cardinality: 1 impl per workspace; per-shape sub-mechanism activation
4. 4 architecturally-encoded vs 4 behaviorally-enforced split per TOP-LEVEL DESIGN PRINCIPLES §1 discriminator
5. Composition with `claim` (load-bearing): per-claim sparring granularity; sparring events = production-phase engagement signal for engaged-authorship
6. Cross-shape policy variation explicit (practitioner-shape always-on / autonomous-business per business policy / personal-OS subset)
7. Per-action audit emission via MCP gate (skill-side; like adapter)

### Round 2 (USER-TRIGGERED; cross-cutting + schema-detail layer)

13 EXPANSIONS surfaced:
1. Per-sub-mechanism architectural schema categories (Pydantic shapes → Phase 6)
2. Orchestrator wiring + retry semantics
3. Per-sub-mechanism event-kind catalog
4. Axis-2 failure-mode detection events (answer_machine_detected / oracle_mode_detected / validator_mode_detected)
5. Selective-friction claim-ambiguity threshold (shape-policy-mandated parameter)
6. Sparring + workflow_instance composition (workflow-orthogonal at framework level)
7. Boot/lifecycle ordering (boot after substrate; flush before substrate shutdown)
8. Per-shape escalation behavior (fail-closed practitioner / fail-open-with-alert autonomous-business / fail-open personal-OS)
9. Cross-session state for sub-mechanisms (confidence calibration persists per claim across session pauses)
10. Anti-sycophancy heuristic detection (impl-specific threshold; architectural-level only declares "fires + emits event")
11. Bypass-with-reason audit semantics (event format + L8 auditor reasoning-chain reconstruction)
12. Composition with substrate Surface §D (architecturally-encoded sub-mechanisms 1-4 leverage substrate's structured-output validation)
13. Watch-list refinements (W1 behavioral→structural promotion; W2 anti-sycophancy false-positive friction-budget; W3 cross-shape activation matrix; W4 per-domain extension)

### Manufactured-criticism rejections (5 across both rounds)

Round 1:
- "Sub-mechanisms should be separate Pattern A protocols, not categories" → REJECT (8 sub-mechanisms compose within unified axis-2 concern; separating inflates primitive count without independent structural content)
- "All 8 sub-mechanisms should be architecturally-encoded" → REJECT (heuristic / declarative / context-dependent → behavioral per TOP-LEVEL DESIGN PRINCIPLES §1 discriminator)
- "Sparring is just per-skill validation, not Pattern A" → REJECT (composes with substrate's hook surface AS runtime mechanism; runs across skills + per-shape variation; Pattern A captures cleanly)

Round 2:
- "Each sub-mechanism should be its own arch topic" → REJECT (8 sub-mechanisms compose within unified Sparring Protocol Surface; per-sub-mechanism arch topic inflates count without cross-cutting coherence)
- "Anti-sycophancy heuristic threshold should be architectural-level locked" → REJECT (heuristic at AI-runtime is prose-convention territory per TOP-LEVEL DESIGN PRINCIPLES §1)

### GLOSSARY back-check (Round 2 termination)

Considered: per-sub-mechanism failure-mode events as glossary-grade vocabulary; selective-friction threshold as primitive sharpening. **Verdict: NOT glossary-grade** — failure-mode events derive from already-locked answer-machine / oracle / validator AI entries; selective-friction threshold is impl-mechanic. **No retro-fit fires.**

### REVISION/EXPANSION self-check

All 20 EXPANSIONS classified additive coverage; none REVISION-flavored. 2-tier classification holds.

### Profile-anchored validation

4/4 clusters PASS with cited profile content (current-context profiles; reused per within-session continuity discipline):

- **Cluster A (L1)**: specialist DEFINITION can bundle skill outputs satisfying sparring schemas
- **Cluster B (L5a)**: line 128 "Sparring as load-bearing runtime mechanism (axis 2 sub-mechanisms used per drafting session; not occasional)" → DIRECTLY validates §5 always-on for practitioner-shape
- **Cluster C (L5a)**: line 67 "AI engagement state shifts: deep sparring during drafting (axis 2)" + "rubber-stamp risk during deadline-pressure send (axis 3 risk)" → §13 sparring + workflow_instance composition (sparring during drafting; axis-3 failure independent dimension)
- **Cluster D (G + L8)**: G line 157 cross-shape consumption → §12 cross-shape policy variation; L8 line 29 audit-trail integrity → §8 + §10 (sparring events surviving deployment migrations; bypass-with-reason audit semantics)

### Sharpening totals

| Round | EXPANSIONS | REVISIONS | Manufactured-criticism rejected |
|---|---|---|---|
| Round 1 | 7 | 0 | 3 |
| Round 2 | 13 | 0 | 2 |
| **Total** | **20** | **0** | **5** |

### Decomposition mode

Mode 1 (single-decision; not composite). 20 EXPANSIONS within 2-round sweet spot per layered coverage observation; no decomposition needed.

## Composition with existing architecture

- 18-section Pattern A protocol topic template (per `MAINTENANCE.md` Layer 3 description; established by substrate; validated by adapter; reinforced by sparring) holds across third Pattern A protocol topic. Template is robust.
- NEW per-shape activation matrix variation (sparring) introduces third Pattern A cardinality pattern alongside substrate (singular tier-aware) + adapter (multi-instance per-class). Cardinality variation IS the architectural distinction across Pattern A protocols at this layer.
- Sparring's load-bearing composition with substrate Surface §D (structured output validation) for architecturally-encoded sub-mechanisms 1-4 demonstrates substrate's foundational role for axis-2 enforcement.
- Sparring's load-bearing composition with `claim` + `engaged authorship` GLOSSARY entries demonstrates per-claim granularity discipline + axis-2 → axis-3 dependency chain.
- Sparring + workflow_instance composition (workflow-orthogonal) validates `workflow` GLOSSARY entry's optional-overlay design + `work-unit` GLOSSARY entry's always-present container claim.

## Constraints flowing to downstream commitments

### → Phase 3.4 remaining ARCH topics (audit / coordination / trust / time / quality-gate at 3.6)

- Pattern A 18-section template precedent reinforced (3 topics now use it: substrate / adapter / sparring)
- Sparring's per-shape activation-matrix variation establishes precedent for per-shape Pattern A variation in remaining topics where applicable
- Sparring's skill-side MCP-gate emission discipline (like adapter) is the default for Pattern A protocols where architecturally-encoded sub-mechanisms run within skill execution

### → Phase 3.5 primitive cluster topics

- `arch/claim-defensibility.md` will deepen sparring → engaged-authorship → defensibility chain (axis-2 → axis-3 dependency mechanics)
- `arch/specialist-skill.md` will document specialist bundling skill outputs satisfying sparring schemas

### → Phase 3.6 quality-gate ARCH topic

- Quality-gate consumes sparring-event emissions for axis-2 enforcement
- Per-shape quality-gate enforcement composes with sparring's cross-shape policy variation

### → Phase 6 spec

- Pydantic Protocol contracts: Sparring Protocol Surface + per-sub-mechanism schemas (architecturally-encoded sub-mechanisms 1-4)
- Concrete default Sparring Protocol Implementation with substrate Surface §D wiring
- Per-shape activation matrices (practitioner-shape primary; second-shape per W3 watch-list)
- Pre-implementation operational concerns (orchestrator retry mechanics; heuristic-detection thresholds; bypass-with-reason UX surface)

## Files touched

- `arch/sparring.md` (NEW; 18 sections per Pattern A protocol topic template)
- `docs/decisions/sparring-arch-topic.md` (this file; NEW; status ACCEPTED)
- `ARCHITECTURE.md` (cascade-update: Phase 3.4 progress 3 of 8; topic catalog sparring row drafted; locked decisions section)
- `BACKLOG.md` (cascade-update: Phase 3.4 sparring Resolved; remaining 5 Pattern A protocol topics pending)
- `HANDOFF.md` (Note 38: sparring ARCH topic locked; third Pattern A protocol topic; per-shape activation-matrix variation introduced)

## Revisit triggers

- Operational evidence accumulates for behavioral → structural promotion of sub-mechanisms 5-8 (W1)
- First production deployment surfaces anti-sycophancy false-positive friction patterns (W2)
- Second-shape productization triggers cross-shape activation matrix expansion (W3)
- Specific archetype (legal-practice / research-lab) surfaces domain-specific axis-2 mechanism (W4)
- Phase 6 pre-implementation sharpening surfaces architectural flow-back (~10-20% per `pre-implementation-sharpening` skill)
- VISION axis-2 framing refinement (Ming research deepening per Phase 3.7 cross-cutting investigations)
