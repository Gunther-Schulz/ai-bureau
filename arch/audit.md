---
title: Audit
topic-cluster: Pattern A protocol topics (#4 of 8)
status: drafted (Phase 3.4 Round 2; locked)
---

# Audit

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the Audit Protocol (Pattern A). Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the Pydantic Protocol contract + AuditEvent schema (Mode 3).

## 1. Topic scope

The **Audit Protocol** formalizes the audit-trail-as-canonical-source architectural commitment + composes substrate / adapter / sparring emission paths into unified event stream. Per locked GLOSSARY `event` entry: events are atomic structured emission units; audit-trail is their COMPOSITION (sequence over time). This topic articulates the COMPOSITION mechanics + Surface contract for any Audit Protocol Implementation.

**Single-layer Surface** (substrate-style; like sparring). Audit-trail concerns are unified (emission / persistence / query / integrity / event-kind catalog management).

**Cardinality**: 1 Audit Protocol Implementation per workspace; per-shape policy declares granularity + event-kind catalog (claim-level / action-level / light per locked event entry Cross-archetype illustration).

**Cross-axis foundation**: events are cross-axis structural substrate per locked GLOSSARY TOC §4. Audit-trail enables axis-3 defensibility (reconstructible reasoning chain) primarily; plus axis-1 trust + axis-2 sparring records.

**Composition with framework**:
- Pattern A protocol per `protocol (architectural)` GLOSSARY entry
- Audit Protocol Surface IS a `mechanism` (framework-level interface contract; AuditEvent schema is the canonical mechanism per locked entry)
- Implementations live at `Framework C scope` as distributable definitions
- Running instance bound to `Owner B scope` per workspace deployment
- Per-shape policy declares granularity + mandatory event kinds

**Phase routing**: AuditEvent Pydantic schema + per-shape event-kind catalogs → Phase 6 spec (Mode 3). Concrete Audit Protocol Implementation (file-format mechanics; hash-chain integrity; query implementation) → Phase 6.

## 2. Audit Protocol Surface (architectural-level capability categories)

Six capability categories define the Surface:

### A. Emission API + actor declaration

The Audit Protocol provides emission entry point. Each emission declares: actor (per `actor_kind` enum) + event_kind + timestamp + per-event-kind details. Substrate-internal direct emission (architectural moments per substrate §8) + skill-side MCP audit gate emission (skill operations per adapter §8 + sparring §8) both invoke this Surface category. Both paths converge in same audit-trail.

### B. Append-only persistence

Audit Protocol Implementation enforces append-only at write boundary (file-handle exclusive write; no rewind; no truncate; no per-event-rewrite). Violations raise integrity errors. Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator: gate-dispatched on every write → structural enforcement (NOT prose convention).

### C. Query for reasoning-chain reconstruction

Surface provides query primitives for L8 auditor reasoning-chain reconstruction:
- per-claim reasoning chain (events filtered by claim_id, ordered by timestamp)
- per-actor activity (events filtered by actor_kind + actor_id)
- per-time-window event range (start_ts, end_ts)
- per-event-kind aggregation (count + content extraction)
- per-work-unit attribution (events filtered by work-unit-id)

Query implementation Phase 6; architectural-level commitment: queries are first-class capability.

### D. Integrity verification

Hash-chain or append-log integrity primitive: each event's prev-hash references prior event; hash-chain unbroken signal = audit-trail unmodified. Cross-deployment migration verifies hash-chain unbroken. Architectural-level: integrity-verifiable; specific algorithm (hash function; verification interval; cross-deployment migration mechanics) is Phase 6.

### E. Event-kind catalog management

Surface manages event-kind catalog at three layers:
- **Framework baseline**: substrate architectural events (§ from `arch/substrate.md`); adapter per-action events (§ from `arch/adapter.md`); sparring per-sub-mechanism events (§ from `arch/sparring.md`); audit-internal integrity events
- **Per-shape extensions**: shape policy declares which event kinds MANDATORY per shape (practitioner-shape claim-level; autonomous-business action-level; personal-OS light)
- **Per-specialist extensions**: specialist DEFINITIONs may declare per-specialist event kinds (planning-document-work specialist may emit `bplan_section_drafted`; legal-research specialist may emit `precedent_cited`)

### F. State-rendering-from-events

Workspace state (workflow_instance state; claim status; per-actor activity) is DERIVED from event sequence. Architectural commitment: state IS the rendered view; events ARE the source of truth. Per archived audit-trail-v2 single-write architecture. State-rendering implementation Phase 6; architectural-level commitment: workspace state queryable via audit-trail rendering.

### Logic placement mode

Surface contract articulated here (Mode 4 conceptual) + Phase 6 spec (Mode 3 Pydantic Protocol + AuditEvent schema + per-shape event-kind catalog declarations + companion docs). Mode 1 production-runtime AI (skills + specialists) emits events via skill-side MCP audit gate (per substrate §8 + adapter §8 + sparring §8 patterns).

## 3. Common-surface boundary criteria

Decision rule for "in Audit Protocol Surface" vs "out":

| Decision criterion | Verdict | Examples |
|---|---|---|
| Emission / persistence / query / integrity / catalog management for AuditEvent stream | Surface | Six capability categories above |
| Per-shape mandatory event-kind declarations | Out (composes with `shape` GLOSSARY entry; declared in shape policy bundles) |
| Per-claim attestation events (axis-3 success mode) | Out (composes with `engaged authorship` per axis-3 → `arch/claim-defensibility.md` Phase 3.5) |
| Cross-claim audit coordination (multiple claims in same workflow_instance share audit-trail context) | Out (composes with `coordination` Pattern A — `arch/coordination.md`) |
| Authority decisions (who can sign / approve) | Out (composes with `trust` Pattern A — `arch/trust.md`) |
| Quality-gate consumption of audit-event emissions | Out (composes with quality-gate Pattern A — `arch/quality-gate.md` Phase 3.6) |
| File-format mechanics (jsonl line structure; per-line schema validation; encoding) | Phase 6 spec (Mode 3) |

## 4. Per-implementation aspect

Implementations live at `Framework C scope` as distributable definitions. Each Implementation wraps native primitives of an underlying audit-trail backend.

### Pattern level

Any implementation satisfying the 6-category Surface qualifies. Pattern level is audit-trail-backend-shape-neutral.

### Current Implementation set (CIRCA 2026)

- **Default Audit Protocol Implementation**: jsonl file-backed (per archived audit-trail-v2.md); local filesystem persistence; hash-chain integrity primitive; line-delimited AuditEvent records; query implementation reads file + filters

Future Implementations may emerge per deployment-tier scaling needs (cloud-backed for Tier 2; federation-aware for Tier 3; hash-chain-with-Merkle for high-integrity deployments). Not yet locked.

### Per-implementation declares

Each Implementation declares:
- **Audit-trail format** (jsonl is default; alternative formats per impl)
- **Append-only enforcement mechanism** (file-handle exclusive write; OS-level append-only flag; impl-specific)
- **Hash-chain algorithm** (per impl; SHA-256 default for jsonl impl)
- **Query implementation** (file-scan for jsonl; index-backed for cloud impls)
- **Cross-deployment migration mechanics** (export / import; integrity verification across backends)
- **Per-shape event-kind catalog support** (impl validates per-shape mandatory kinds present)
- **Error mapping** (impl-native errors → AuditError categories per §10)

## 5. Selection mechanics

Audit Protocol selection bound to workspace-level configuration (similar to substrate; NOT shape-policy-driven like sparring — every workspace needs audit-trail; impl variation is deployment-tier-driven).

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Audit Protocol Implementations active per workspace | 1 | workspace.md `audit_impl:` field selects |
| Implementations per Framework C catalog | M | Default jsonl; future cloud-backed / federation-aware |

### Validation at workspace boot

Audit Protocol selection validated at workspace boot:
- Selected impl id resolves to known Implementation (per Framework C catalog)
- Selected impl compatible with deployment tier (Tier 2+ may require cloud-backed; Tier 3 federation-aware)
- Active shape's mandatory event-kind catalog supported by impl
- Existing audit-trail (if workspace pre-exists) hash-chain verifiable by impl

### Re-binding semantics

Audit Protocol Implementation re-bindable across substrate migrations (workspace identity persists; audit-trail migrates; integrity verification at migration boundary). Per L8 line 32 cross-deployment evidence requirement.

## 6. Tri-aspect reconciliation

Audit Protocol as tri-aspect Pattern A primitive:

| Aspect | Layer | What it is |
|---|---|---|
| **Surface** (6 capability categories) | mechanism (framework-level) | Atomic interface contract; AuditEvent schema + emission/persistence/query/integrity/catalog/state-rendering categories |
| **Implementations** | Framework C scope | Distributable definitions wrapping native audit-trail-backend primitives |
| **Running Instance** | Owner B scope | Bound to workspace deployment via workspace.md selection |

### Audit-trail-as-canonical-source (load-bearing architectural commitment)

Per archived audit-trail-v2 single-write architecture: audit-trail is single source of truth for reasoning chain; workspace state rendered FROM events; events append-only; never rewritten. Per L8 line 29: "Audit-trail integrity must survive intact across deployments / migrations." This commitment is foundational for axis-3 defensibility.

### Audit-coupling impossible-by-construction

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code targeting Audit Protocol Surface is portable across Implementations; skill code reaching Implementation-internal primitives (file-format / hash-algorithm / query-implementation) is impl-pinned by construction.

### Distinct from substrate / adapter / sparring Pattern A

- substrate = singular per workspace; tier-aware
- adapter = multi-instance; per-class Surface variation
- sparring = singular per workspace; per-shape activation matrix
- **audit = singular per workspace; deployment-tier-driven impl variation** (every workspace needs audit; impl varies per tier scaling)

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Audit Protocol is one mechanism category within the framework |
| `mechanism` | AuditEvent schema IS a mechanism (framework-level interface contract per locked entry); query primitives are mechanisms |
| `Framework C scope` | Audit Protocol Implementations live there as distributable definitions |
| `shape` | Shape policy declares per-shape mandatory event-kind catalog + audit error semantics |
| `workspace` | Workspace selects Audit Protocol Implementation via workspace.md |
| `Owner B scope` | Running Audit Protocol Instance bound to workspace deployment |
| `protocol (architectural)` | Audit Protocol is Pattern A protocol instance |
| **`event`** | **Locked GLOSSARY primitive: atomic structured emission unit; audit-trail is COMPOSITION (sequence over time). This topic articulates the composition mechanics** |
| `actor` | Every event declares emitting actor; Audit Protocol enforces actor declaration at emission |
| **`substrate`** | **Substrate Surface §8 dual-emission (substrate-internal direct + skill-side via MCP gate) converges in audit-trail; substrate emits architectural events; Audit Protocol persists** |
| **`adapter`** | **Adapter §8 skill-side MCP-gate emission converges in audit-trail; per-action audit-event kinds per integration class** |
| **`sparring`** | **Sparring §8 skill-side MCP-gate emission converges in audit-trail; per-sub-mechanism event-kind catalog + axis-2 failure-mode detection events** |
| `claim` | Claims emit `claim_made` events (per claim entry composes-with); per-claim reasoning chain reconstructed via audit-trail query |
| `engaged authorship` | Per-claim attestation events ARE attestation-phase substrate; production-phase substrate is sparring events + source-grounded events |
| `defensibility` | Audit-trail provides reconstructible reasoning chain — one of three structural conditions defensibility tests |
| `rubber-stamping` | Events alone don't prevent rubber-stamping (events record sign-off, not engagement that would make sign-off substantive); per-claim attestation requirements + sparring-event presence are counter-mechanism |
| `quality-gate` (Phase 3.6) | Quality-gate consumes audit-event emissions for axis enforcement; per-shape policy declares quality-gate enforcement of audit requirements |
| `coordination` (separate ARCH topic) | Cross-claim audit coordination (multiple claims in same workflow_instance share audit-trail context) via coordination Protocol; query patterns compose |
| `workflow` | Workflow_instance lifecycle emits events (workflow_started, phase_transitioned, workflow_completed, etc.); audit-trail records workflow_instance state transitions |
| `work-unit` | Events scoped to work-unit (per `event` entry composes-with); per-work-unit attribution mandatory |
| `session` | Session_id field on events identifies session boundaries; cross-session audit-trail continuity preserved |

## 8. Substrate-internal vs skill-side audit emission (architectural-event kinds catalog)

### Architectural commitment

Audit Protocol accepts events from two paths converging in single audit-trail:

| Emitter | Path | Use case |
|---|---|---|
| Substrate internal | Direct Python emission (substrate has direct internal access; NOT through MCP gate) | Substrate-architectural moments (registration / permission decision / boot complete / shutdown initiated) |
| Skill / specialist | MCP audit gate (`record_audit_event`) | Skill-side events (claim_made / sparring round / adapter operation / specialist activity) |

Both writes go through same Pydantic AuditEvent schema; both land in same `audit-trail.jsonl` per default impl; both validate identically. Reader (auditor or quality-gate) sees unified event stream.

### Audit-internal events (this Protocol's own emissions)

The Audit Protocol emits its own integrity events:
- `audit_trail_integrity_verified` (periodic; per query / per migration boundary)
- `audit_trail_integrity_violated` (hash-chain broken; immediate emission)
- `audit_trail_migrated` (cross-deployment migration completed)
- `audit_trail_archived` (audit-trail compression / archival event; future per W3 watch-list)

Self-audit primitive: Audit Protocol audits its own integrity.

### Cross-substrate event-kind translation

Per G line 159 backup-restore-migration round-trip: substrate-specific metadata may be lost across substrate migrations. Audit Protocol architectural commitment: substrate-specific metadata explicitly tagged at emission (e.g., `substrate_kind: claude_agent_sdk`); cross-substrate migration preserves event semantics OR marks substrate-specific-metadata-loss explicitly.

## 9. Cardinality + lifecycle

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Audit Protocol Implementations per workspace | 1 | workspace.md `audit_impl:` field |
| Audit-trails per workspace | 1 (logical) | Single audit-trail per workspace; impl may use multiple files (rotation; archival) but logically unified |
| Events per audit-trail | Unbounded | Append-only; no per-event rewrite; archival per W3 |

### Lifecycle ownership

- **Creator**: framework-runtime instantiates Audit Protocol Implementation per workspace boot (selecting impl per workspace.md)
- **Owner**: workspace deployment runtime (Owner B scope)
- **Destroyer**: framework-runtime at workspace shutdown (audit-trail file persists; Implementation released)

### Mutability

- **Configuration immutable** across single audit-impl boot (impl selection + file path + integrity-config loaded at boot)
- **Audit-trail content append-only** (events never rewritten; per §2.B)
- **Cross-session persistence**: audit-trail persists across sessions (workspace lifetime); session_id field on events identifies session boundaries; session resumption preserves prior audit-trail state per substrate Surface §F

## 10. Audit error categories (architectural-level)

| Category | Architectural meaning |
|---|---|
| `AuditWriteError` | Audit-trail write failure (filesystem unavailable; permission denied; disk full) |
| `AuditIntegrityError` | Hash-chain broken (audit-trail tampered OR corruption detected) |
| `AuditAppendOnlyViolation` | Attempted rewrite / truncate / rewind on audit-trail (architectural-rule violation; impl rejects) |
| `AuditSchemaError` | Event doesn't match AuditEvent Pydantic schema |
| `AuditCatalogError` | Event_kind not in active shape's mandatory catalog OR not in baseline framework catalog |
| `AuditQueryError` | Query failure (impl-internal; corruption; index issue) |
| `AuditMigrationError` | Cross-deployment migration failure (integrity not verifiable; format incompatible) |

### Per-shape error semantics

- **practitioner-shape**: fail-closed on AuditWriteError (defensibility-critical; can't operate without audit-trail; architectural integrity required)
- **autonomous-business-shape**: fail-open with alert + queued-retry (continuity prioritized; alert on failure; retry mechanism)
- **personal-OS-shape**: fail-open with retry (lightweight; degradation acceptable)

Per-class Pydantic shape → Phase 6 spec.

## 11. Boot + shutdown phase ordering

### Boot sequence

Audit Protocol boots BEFORE substrate (substrate's own events emit through audit gate; audit-trail must be ready before substrate emission per substrate §10):

1. Workspace boot triggers Audit Protocol Implementation instantiation
2. Implementation loads config (file path; impl-specific config); validates audit-trail file path accessible
3. If existing audit-trail present: verify hash-chain integrity (load prior tail event; verify ready-state)
4. Implementation `is_ready` becomes True; emission API ready
5. Substrate boot proceeds (per `arch/substrate.md` §10); substrate events emit through audit gate from step 5 onwards

### Shutdown sequence

Audit Protocol shuts down LAST (substrate shutdown drains in-flight events; audit must persist them all):

1. Substrate shutdown initiates (per `arch/substrate.md` §10): `shutdown_initiated` event emitted
2. In-flight agent runs drain; final events emit through audit gate
3. Substrate `shutdown_complete` emitted
4. Adapter / sparring / coordination Pattern A protocols drain; final events emit
5. Audit Protocol drains pending events; flushes audit-trail to disk
6. Audit Protocol verifies hash-chain integrity at shutdown
7. `audit_trail_integrity_verified` emitted (final event)
8. Audit Protocol shutdown returns

This ordering preserves invariant: every emitted event is persisted in audit-trail before workspace shutdown completes.

## 12. Cross-shape policy variation

Per `profiles/G-composability-gate.md` line 157: "Cross-shape consumption ... Shape's policy bundle determines if specialist activates fully or partially."

Per-shape audit policy (mandatory event-kind catalog + error semantics):

| Shape | Granularity | Mandatory event kinds | Error semantics |
|---|---|---|---|
| **practitioner-shape** (per L5a line 41 "claim_made events emitted per substantive claim") | Claim-level | claim_made / source_grounded / sparring_round / per_claim_attestation / signature_applied + framework baseline | Fail-closed on AuditWriteError; defensibility-critical |
| **autonomous-business-shape** | Action-level | task_started / task_completed / budget_consumed / approval_requested / external_action_taken + framework baseline | Fail-open with alert + queued-retry |
| **personal-OS-shape** | Light | User-decided emission per skill (no mandatory shape-level catalog beyond framework baseline) | Fail-open with retry |
| **federation-shape** (future per second-shape watch-list) | Cross-node + per-tenant | Federation-trust events + cross-node-coordination events + per-tenant audit-trail isolation (each tenant has own audit-trail; federation events span) | Fail-closed within node; fail-open across nodes |

## 13. Cross-deployment evidence + audit-trail integrity

Per `profiles/L8-auditor-reviewer-posthoc.md` line 29 "Audit-trail integrity must survive intact across deployments / migrations" + line 32 "Cross-deployment evidence: practitioner moved firms / migrated workspace; L8 evidence must follow" + line 33 "External-format requirements: L8 may not access framework directly; needs exportable audit-trail in standard formats."

### Audit-trail integrity verification

Per §2.D + §10 AuditIntegrityError: hash-chain unbroken signal at every query / migration / shutdown moment. Architectural commitment is integrity-VERIFIABLE; specific algorithm Phase 6.

### Cross-deployment migration

Per §5 re-binding semantics + §10 AuditMigrationError: workspace identity persists across migrations; audit-trail migrates with workspace; integrity verification at migration boundary. `audit_trail_migrated` event emitted at completion.

### External-format requirements (L8 auditor)

L8 auditor may not access framework runtime; needs exportable audit-trail in standard formats:
- jsonl raw (default impl) directly readable
- PDF reports (audit-trail rendered for regulator submission)
- CSV event logs (per-event-kind aggregation; per-claim reasoning chain export)

External-format export is impl capability per Surface §C query category; specific format implementations Phase 6.

## 14. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level:

- **AuditEvent Pydantic schema** (exact field shapes; required vs optional; per-event-kind discriminated union)
- **Audit-trail file format mechanics** (jsonl line structure; encoding; line-delimited validation)
- **Hash-chain algorithm choice** (SHA-256 default; alternative for high-integrity deployments)
- **Query implementation** (file-scan vs index-backed; performance characteristics; query language)
- **Append-only enforcement OS-level** (filesystem flags; alternative for impls without OS support)
- **Cross-deployment migration mechanics** (export format; import validation; integrity verification at boundary)
- **Audit-trail compression / archival strategy at scale** (W3; rotation policies; archival to cold storage)
- **External-format export** (PDF rendering; CSV aggregation; regulator-submission format)
- **Per-shape event-kind catalog declaration syntax** (in shape policy bundles)
- **Audit-trail-state-rendering implementation** (state derived from event sequence; per-impl performance)

These belong to Phase 6 pre-implementation sharpening; ARCH topic explicitly does NOT lock these.

## 15. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| W1 | Hash-chain algorithm choice | First Tier 2+ deployment with concrete integrity requirements | Pick algorithm at Phase 6 implementation; hash-chain-with-Merkle for federation; SHA-256 for default |
| W2 | Cross-substrate event-kind translation rules | First substrate migration in production deployment | Define translation rules per substrate-pair; preserve substrate-specific metadata explicitly OR mark loss |
| W3 | Audit-trail compression / archival strategy at scale | First deployment with multi-year audit-trail accumulation | Define rotation policy; archival format; query mechanics across rotated/archived audit-trails |
| W4 | Cloud-backed Audit Protocol Implementation | First Tier 2 cloud deployment | Implement cloud-backed impl satisfying same Surface; audit-trail-integrity verification across cloud boundaries |
| W5 | Federation-aware Audit Protocol Implementation | First Tier 3 federated deployment | Implement federation-aware impl; cross-node audit-trail coordination; per-tenant isolation |

## 16. Decision-design provenance

Source materials:
- `archive/docs/decisions/audit-trail-v2.md` — single-write architecture (state rendered FROM events; append-only discipline)
- `archive/docs/decisions/audit-trail-v1.md` — initial audit-trail design
- `archive/docs/audit-pre-rag.md` — pre-RAG audit-trail considerations
- VISION axis-3 framing (defensibility test; reconstructible reasoning chain)
- Locked GLOSSARY `event` entry (atomic emission unit; audit-trail composition)

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: Audit Protocol stays shape-neutral / archetype-neutral / pioneer-neutral. Per-shape event-kind catalogs handle archetypal variation via shape policy.

## 17. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.4 | LOCKED |
| AuditEvent Pydantic schema | 6 | Mode 3 spec; per-event-kind discriminated union |
| Default Audit Protocol Implementation (jsonl file-backed) | 6 | Concrete impl; append-only enforcement; SHA-256 hash-chain; query implementation |
| Per-shape event-kind catalog declarations | 6 | In shape policy bundles |
| Cloud-backed Implementation | TBD per W4 signal | First Tier 2 cloud deployment |
| Federation-aware Implementation | TBD per W5 signal | First Tier 3 federated deployment |
| External-format export (PDF / CSV) | 6 | Per L8 auditor external-format requirements |
| Pre-implementation operational concerns | 6 | Pre-implementation sharpening at Phase 6 implementation-start |

## 18. Cross-references

- **GLOSSARY**: `event` (canonical primitive); `actor`, `mechanism`, `Framework C scope`, `Owner B scope`, `protocol (architectural)`, `substrate`, `adapter`, `sparring`, `claim`, `engaged authorship`, `defensibility`, `rubber-stamping`, `quality-gate`, `workflow`, `work-unit`, `session`, `shape`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (append-only as gate-dispatched-structural); `DISCIPLINES.md` Discipline 9 (coherence-audit cadence — Audit Protocol's audit-trail is the corpus those audits operate on)
- **Profiles validated**: `G-composability-gate.md` (line 159 backup-restore-migration round-trip; line 168 substrate-portability + substrate-pinned variation); `L5a-planner-pbs-schulz.md` (line 41 claim_made events emitted per substantive claim — DIRECTLY validates §12 practitioner-shape claim-level granularity); `L8-auditor-reviewer-posthoc.md` (line 29 audit-trail integrity; line 32 cross-deployment evidence; line 33 external-format requirements — DIRECTLY validate §13)
- **ARCH topics composing with audit**: `arch/substrate.md` (Surface §8 dual-emission converges here); `arch/adapter.md` (§8 per-action emission); `arch/sparring.md` (§8 per-sub-mechanism emission); `arch/coordination.md` (Phase 3.4; cross-claim audit-trail coordination); `arch/quality-gate.md` (Phase 3.6; consumes audit-event emissions for axis enforcement); `arch/claim-defensibility.md` (Phase 3.5; audit-trail provides reconstructible reasoning chain for defensibility test)
- **Phase 6 spec target**: `docs/specs/audit.md` (AuditEvent Pydantic schema + per-impl spec + per-shape event-kind catalog declarations)
- **Archived sources**: `archive/docs/decisions/audit-trail-v2.md`, `archive/docs/decisions/audit-trail-v1.md`, `archive/docs/audit-pre-rag.md`
