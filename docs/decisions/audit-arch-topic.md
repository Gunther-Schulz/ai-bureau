# Decision record: Audit ARCH topic (Phase 3.4 fourth Pattern A protocol topic)

## Status

ACCEPTED — session 16 (2026-05-02); 2-round sharpening per `decision-design-sharpening` v0.6.0 layered coverage observation. Persisted under DR template locked in `MAINTENANCE.md` Layer 4 (per `doc-organization-templates.md` composite DR).

## Owner

Phase 3.4 Per-architectural-Protocol detail rebuild; fourth Pattern A protocol topic (substrate first; adapter second; sparring third; audit fourth per foundation-up ordering — audit composes with all prior emission paths).

## Related

- Locked GLOSSARY `event` entry (atomic emission unit; audit-trail composition; cross-axis structural substrate)
- Locked GLOSSARY `actor` / `mechanism` / `defensibility` entries
- `arch/substrate.md` (Surface §8 dual-emission paths converge in audit-trail)
- `arch/adapter.md` (§8 per-action emission converges in audit-trail)
- `arch/sparring.md` (§8 per-sub-mechanism emission converges in audit-trail)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (append-only as gate-dispatched-structural)
- `DISCIPLINES.md` Discipline 9 (coherence-audit cadence — audit-trail IS the corpus those audits operate on)
- `doc-organization-templates.md` (DR template + arch/<topic>.md template)
- Archived sources: `archive/docs/decisions/audit-trail-v2.md`, `archive/docs/decisions/audit-trail-v1.md`, `archive/docs/audit-pre-rag.md`

## Context

Audit is the fourth Pattern A protocol topic in Phase 3.4 sequence (foundation-up: substrate → adapter → sparring → audit → 4 remaining). Validates Pattern A 18-section template (4th application). Consolidates emission paths from substrate (dual: internal direct + skill-side via MCP gate) + adapter (skill-side via MCP gate) + sparring (skill-side via MCP gate) into unified architectural commitment.

Critical architectural distinctions:
- **Single-layer Surface** (substrate-style; like sparring); audit-trail concerns unified across emission/persistence/query/integrity/catalog/state-rendering
- **Audit-trail-as-canonical-source** (load-bearing architectural commitment from archived audit-trail-v2): single-write architecture; state rendered FROM events; append-only discipline; never rewritten
- **Append-only enforcement architectural-level** per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator (gate-dispatched on every write → structural)
- **Boot/shutdown ordering**: audit boots BEFORE substrate; shuts down AFTER substrate (preserves invariant: every emitted event is persisted before workspace shutdown)

## Decision

`arch/audit.md` LOCKED with 18 sections per Pattern A protocol topic template.

Surface = 6 capability categories: emission API + actor declaration / append-only persistence / query for reasoning-chain reconstruction / integrity verification / event-kind catalog management / state-rendering-from-events.

Per-shape event-kind catalog: practitioner-shape claim-level (claim_made / source_grounded / sparring_round / per_claim_attestation / signature_applied) + autonomous-business action-level + personal-OS light.

Architectural shape locked; AuditEvent Pydantic schema + concrete Audit Protocol Implementation + hash-chain integrity algorithm choice → Phase 6 spec.

## Sharpening provenance

### Round 1 (full monty; architectural decisions layer)

8 EXPANSIONS surfaced:
1. Single-layer Surface (substrate-style; audit-trail concerns unified)
2. Cardinality: 1 impl per workspace; per-shape granularity declared
3. 6 Surface capability categories (emission/persistence/query/integrity/catalog/state-rendering)
4. Audit-trail-as-canonical-source architectural commitment (load-bearing per archived audit-trail-v2)
5. Per-shape granularity policy (claim-level / action-level / light per locked event entry)
6. Composition with substrate / adapter / sparring (consolidates emission paths)
7. Audit-trail-integrity across migrations (per L8 cross-deployment evidence)
8. Pre-implementation operational concerns (Phase 6 forward-reference)

### Round 2 (USER-TRIGGERED; cross-cutting + schema-detail layer)

13 EXPANSIONS surfaced:
1. Per-shape event-kind catalog details
2. Append-only enforcement mechanism (gate-dispatched-structural)
3. State-rendering-from-events architectural detail
4. Audit-trail-integrity verification mechanism (hash-chain)
5. Cross-deployment evidence query patterns (L8 auditor)
6. Boot/lifecycle ordering (audit BEFORE substrate; shutdown AFTER)
7. Per-shape audit error semantics (fail-closed / fail-open-with-alert / fail-open)
8. Cross-session audit-trail continuity (session_id boundary; persistence across)
9. Composition with `coordination` Pattern A protocol
10. Audit-trail format declaration (jsonl per archive)
11. Event-kind catalog management Surface category
12. Audit-trail-integrity audit-event (self-audit primitive)
13. Watch-list refinements (W1 hash-chain choice; W2 cross-substrate translation; W3 archival)

### Manufactured-criticism rejections (5 across both rounds)

Round 1:
- "Audit isn't Pattern A — it's just an event schema + persistence" → REJECT (per locked event + mechanism + protocol entries; Pattern A captures cleanly)
- "Substrate-internal direct emission violates Pattern A's clean Surface boundary" → ACCEPT scoping; REJECT as Round-1-pivot (locked architectural commitment per substrate §8)
- "Audit Protocol should be merged with substrate Pattern A as 'substrate audit-emission'" → REJECT (audit-trail is distinct cross-axis structural substrate per locked GLOSSARY TOC §4)

Round 2:
- "Append-only should be content-convention, not structural" → REJECT (gate-dispatched-on-every-write per TOP-LEVEL DESIGN PRINCIPLES §1)
- "Hash-chain integrity should be Phase 6 only, not architectural-level" → REJECT (architectural commitment is "integrity-verifiable"; Phase 6 picks algorithm)

### GLOSSARY back-check (Round 2 termination)

Considered: append-only-discipline as primitive sharpening; state-rendering-from-events as new vocabulary. **Verdict: NOT glossary-grade** — both already implicit in `event` GLOSSARY entry (events are append-only per locked entry; per archived audit-trail-v2 schema state derived from events). **No retro-fit fires.**

### REVISION/EXPANSION self-check

All 21 EXPANSIONS classified additive coverage; none REVISION-flavored. 2-tier classification holds.

### Profile-anchored validation

4/4 clusters PASS with cited profile content (current-context profiles; reused per within-session continuity discipline):

- **Cluster A (L1)**: specialist DEFINITION may declare per-specialist event_kind catalog (per §2.E catalog management); specialists bundle skills emitting per-claim events
- **Cluster B (L5a)**: line 41 "claim_made events emitted per substantive claim" — DIRECTLY validates §12 practitioner-shape claim-level granularity + §6 composition discipline
- **Cluster C (L5a)**: drafting phase emits per-claim source-grounded events (line 41-43); send-phase emits HITL attestation events (line 50) — validates per-claim audit emission across workflow phases
- **Cluster D (G + L8)**: G line 159 backup-restore-migration round-trip → §13 audit-trail-integrity; G line 168 substrate-portability + substrate-pinned variation → §8 cross-substrate event-kind translation; L8 line 29 audit-trail integrity → §6 audit-trail-as-canonical-source + §13 cross-deployment evidence; L8 line 32-33 cross-deployment evidence + external-format requirements → §13 query patterns + external-format export

### Sharpening totals

| Round | EXPANSIONS | REVISIONS | Manufactured-criticism rejected |
|---|---|---|---|
| Round 1 | 8 | 0 | 3 |
| Round 2 | 13 | 0 | 2 |
| **Total** | **21** | **0** | **5** |

### Decomposition mode

Mode 1 (single-decision; not composite). 21 EXPANSIONS within 2-round sweet spot per layered coverage observation; no decomposition needed.

## Composition with existing architecture

- 18-section Pattern A protocol topic template reinforced (4th application: substrate / adapter / sparring / audit)
- Audit Protocol consolidates emission paths from substrate §8 + adapter §8 + sparring §8 into unified architectural commitment — first Pattern A topic that primarily INTEGRATES other Pattern A protocols (vs being primarily-new-mechanism like prior 3)
- NEW Pattern A cardinality variation: deployment-tier-driven impl variation (substrate = singular tier-aware; adapter = multi-instance per-class; sparring = singular per-shape activation; **audit = singular deployment-tier-driven**). Fourth Pattern A cardinality pattern.
- Audit-trail-as-canonical-source commitment is foundational for axis-3 defensibility (reconstructible reasoning chain) — composes load-bearingly with claim-defensibility ARCH topic (Phase 3.5)
- Append-only enforcement at architectural level (gate-dispatched-structural per TOP-LEVEL DESIGN PRINCIPLES §1) sets precedent for similar enforcement decisions in remaining Pattern A topics
- Boot-before-substrate / shutdown-after-substrate ordering establishes Audit Protocol as foundational Pattern A protocol — substrate composes ABOVE audit at runtime layering

## Constraints flowing to downstream commitments

### → Phase 3.4 remaining ARCH topics (coordination / trust / time / quality-gate at 3.6)

- 4-of-7 Pattern A protocol topics now use 18-section template (substrate / adapter / sparring / audit). Template robust.
- Audit Protocol Surface §C query patterns + §F state-rendering compose with coordination ARCH topic (Phase 3.4)
- Audit Protocol's per-shape event-kind catalog supports trust + time Pattern A protocol event emissions

### → Phase 3.5 primitive cluster topics

- `arch/claim-defensibility.md` will deepen audit-trail's role in axis-3 defensibility (reconstructible reasoning chain via audit-trail query + per-claim attestation events)
- `arch/specialist-skill.md` will document specialist DEFINITION declaring per-specialist event kinds (per §2.E catalog management)
- `arch/workflow-work-unit.md` will document workflow_instance lifecycle event emission

### → Phase 3.6 quality-gate ARCH topic

- Quality-gate consumes audit-event emissions for axis enforcement (Surface §C query patterns)
- Per-axis observability via per-shape event-kind catalogs

### → Phase 6 spec

- AuditEvent Pydantic schema + per-event-kind discriminated union
- Default Audit Protocol Implementation (jsonl file-backed; SHA-256 hash-chain; append-only enforcement; query implementation)
- Per-shape event-kind catalog declarations (in shape policy bundles)
- External-format export (PDF / CSV per L8 auditor requirements)
- Cross-deployment migration mechanics (export / import; integrity verification at boundary)
- Pre-implementation operational concerns (file-format mechanics; query performance; archival strategy)

## Files touched

- `arch/audit.md` (NEW; 18 sections per Pattern A protocol topic template)
- `docs/decisions/audit-arch-topic.md` (this file; NEW; status ACCEPTED per locked DR template)
- `ARCHITECTURE.md` (cascade-update: Phase 3.4 progress 4 of 8; topic catalog audit row drafted; locked decisions section)
- `BACKLOG.md` (cascade-update: Phase 3.4 audit Resolved; remaining 4 Pattern A protocol topics pending)
- `HANDOFF.md` (Note 39: audit ARCH topic locked; fourth Pattern A protocol topic; deployment-tier-driven cardinality variation introduced)

## Revisit triggers

- First Tier 2+ deployment surfaces concrete integrity requirements (W1 hash-chain algorithm choice)
- First substrate migration in production deployment (W2 cross-substrate event-kind translation rules)
- First multi-year audit-trail accumulation (W3 archival strategy)
- First Tier 2 cloud deployment (W4 cloud-backed Audit Protocol Implementation)
- First Tier 3 federated deployment (W5 federation-aware Audit Protocol Implementation)
- Phase 6 pre-implementation sharpening surfaces architectural flow-back (~10-20% per `pre-implementation-sharpening` skill)
- VISION axis-3 framing refinement triggers re-validation of audit-trail-as-canonical-source commitment
