---
title: Audit
topic-cluster: mechanism-class topics (sparring + audit; per-shape policy variation; not Pattern A)
status: drafted (Phase 3.4 Round 2; mechanism class with per-shape granularity policy per `docs/decisions/greenfield-rederivation-pause.md` Step 3 verdict)
---

# Audit

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the Audit **mechanism class** with per-shape granularity policy. Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the AuditEvent Pydantic schema (Mode 3).

## 1. Topic scope

The **Audit mechanism class** formalizes the audit-trail-as-canonical-source architectural commitment + composes substrate / adapter / sparring emission paths into unified event stream. Per locked GLOSSARY `event` entry: events are atomic structured emission units; audit-trail is their COMPOSITION (sequence over time). This topic articulates the COMPOSITION mechanics + the AuditEvent schema as the class's central mechanism Surface, plus per-shape granularity policy parameterizing emission catalog + error semantics + trust model.

**Mechanism class Surface** (AuditEvent schema + audit-trail composition + 6 capability categories — emission / persistence / query / integrity / event-kind catalog management / state-rendering). The class does NOT have multiple alternative implementations realizing one whole-class Surface differently — that's the discriminator distinguishing it from Pattern A protocols (substrate / adapter / quality-gate). Storage-backend variation (jsonl / LanceDB / Postgres / cloud-backed) is **substrate-impl level** (per substrate Surface §F session+context management), not class-level pluggability — the substrate provides the storage substrate; audit's mechanism Surface is independent of how bytes land.

**Cardinality**: 1 audit-trail per workspace (always present; not selectable); per-shape policy declares granularity + event-kind catalog (claim-level / action-level / light per locked event entry Cross-archetype illustration); per-substrate-impl storage realization (jsonl default; alternative backends per substrate-impl).

**Cross-axis foundation**: events are cross-axis structural substrate per locked GLOSSARY TOC §4. Audit-trail enables axis-3 defensibility (reconstructible reasoning chain) primarily; plus axis-1 trust + axis-2 sparring records.

**Composition with framework**:
- AuditEvent schema IS a `mechanism` (framework-level interface contract per locked event entry); audit-trail composition + 6 capability categories constitute the class
- Per-shape policy declares granularity + mandatory event kinds + error semantics + authority-binding trust model (subsumed prior Trust Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade)
- Storage backend mediated via substrate Surface §F (jsonl / LanceDB / Postgres / cloud-backed all substrate-impl-pinned, NOT audit-class-level)
- Architectural-event emission paths (substrate-internal direct + skill-side via MCP gate) converge in audit-trail; both validated against AuditEvent schema

**Phase routing**: AuditEvent Pydantic schema + per-shape event-kind catalogs → Phase 6 spec (Mode 3). Storage-backend mechanics (file-format / hash-chain integrity algorithm / query implementation) live at substrate-impl level → Phase 6.

## 2. Audit mechanism class Surface (architectural-level capability categories)

Six capability categories define the class's Surface (AuditEvent schema + audit-trail composition unified):

### A. Emission API + actor declaration

The audit class provides emission entry point. Each emission declares: actor (per `actor_kind` enum) + event_kind + timestamp + per-event-kind details. Substrate-internal direct emission (architectural moments per substrate §8) + skill-side MCP audit gate emission (skill operations per adapter §8 + sparring §8) both invoke this Surface category. Both paths converge in same audit-trail.

### B. Append-only persistence

Substrate-impl enforces append-only at write boundary (file-handle exclusive write; no rewind; no truncate; no per-event-rewrite). Violations raise integrity errors. Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator: gate-dispatched on every write → structural enforcement (NOT prose convention). Audit class Surface mandates append-only; substrate-impl provides the gate.

### C. Query for reasoning-chain reconstruction

Surface provides query primitives for L8 auditor reasoning-chain reconstruction:
- per-claim reasoning chain (events filtered by claim_id, ordered by timestamp)
- per-actor activity (events filtered by actor_kind + actor_id)
- per-time-window event range (start_ts, end_ts)
- per-event-kind aggregation (count + content extraction)
- per-work-unit attribution (events filtered by work-unit-id)

Query implementation Phase 6 (substrate-impl level); architectural-level commitment: queries are first-class capability of the class Surface.

### D. Integrity verification

Hash-chain or append-log integrity primitive: each event's prev-hash references prior event; hash-chain unbroken signal = audit-trail unmodified. Cross-deployment migration verifies hash-chain unbroken. Architectural-level: integrity-verifiable; specific algorithm (hash function; verification interval; cross-deployment migration mechanics) is substrate-impl level (Phase 6).

### E. Event-kind catalog management

Surface manages event-kind catalog at three layers:
- **Framework baseline**: substrate architectural events (§ from `arch/substrate.md`); adapter per-action events (§ from `arch/adapter.md`); sparring per-sub-mechanism events (§ from `arch/sparring.md`); audit-internal integrity events
- **Per-shape extensions**: shape policy declares which event kinds MANDATORY per shape (practitioner-shape claim-level; autonomous-business action-level; personal-OS light)
- **Per-specialist extensions**: specialist DEFINITIONs may declare per-specialist event kinds (planning-document-work specialist may emit `bplan_section_drafted`; legal-research specialist may emit `precedent_cited`)

### F. State-rendering-from-events

Workspace state (workflow_instance state; claim status; per-actor activity) is DERIVED from event sequence. Architectural commitment: state IS the rendered view; events ARE the source of truth. Per archived audit-trail-v2 single-write architecture. State-rendering implementation Phase 6 (substrate-impl level); architectural-level commitment: workspace state queryable via audit-trail rendering.

### Logic placement mode

Surface contract articulated here (Mode 4 conceptual) + Phase 6 spec (Mode 3 Pydantic AuditEvent schema + per-shape event-kind catalog declarations + companion docs). Mode 1 production-runtime AI (skills + specialists) emits events via skill-side MCP audit gate (per substrate §8 + adapter §8 + sparring §8 patterns).

## 3. Class boundary criteria

Decision rule for "in Audit mechanism class" vs "out":

| Decision criterion | Verdict | Examples |
|---|---|---|
| Emission / persistence / query / integrity / catalog management for AuditEvent stream | In class | Six capability categories above |
| Per-shape mandatory event-kind declarations | Out (composes with `shape` GLOSSARY entry; declared in shape policy bundles) |
| Per-claim attestation events (axis-3 success mode) | Out (composes with `engaged authorship` per axis-3 → `arch/claim-defensibility.md` Phase 3.5) |
| Cross-claim audit coordination (multiple claims in same workflow_instance share audit-trail context) | Out (subsumed into substrate hooks + event-bus per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade — see `arch/substrate.md`; per-shape policy configures coordination shape — call-shaped vs event-shaped). Prior `coordination` Pattern A topic CANCELLED per same DR. |
| Authority decisions (who can sign / approve; trust model) | **In class — subsumes prior `trust` Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade**: authority-binding mechanism with per-shape trust policy (practitioner-judgment / budget-policy / individual) lives in this class. Substrate Surface §C permission flow integrates. Prior `trust` Pattern A topic CANCELLED per same DR. |
| Quality-gate consumption of audit-event emissions | Out (composes with quality-gate Pattern A — `arch/quality-gate.md` Phase 3.6) |
| File-format mechanics (jsonl line structure; per-line schema validation; encoding; hash-algorithm) | Out (substrate-impl level per substrate Surface §F session+context management; storage backend variation is substrate-impl-pinned, not audit-class-level) |
| Time-driven audit operations (scheduled archival; cron-driven exports) | Out (subsumed into substrate-impl temporal semantics + adapter time-driven operations per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade — no separate Time Pattern A topic; prior `time` topic CANCELLED) |

## 4. Per-substrate-impl realization aspect

The Audit mechanism class is realized at framework-mechanism layer (AuditEvent schema + audit-trail composition + 6 capability categories) + parameterized by per-shape policy (granularity + event-kind catalog + error semantics + trust model). Storage-backend variation is **per-substrate-impl** (not class-level pluggability) — that's the discriminator distinguishing this class from Pattern A protocols.

### Per-substrate-impl storage realization

Substrate Surface §F (session + context management) provides the storage substrate; audit's class Surface is independent of how bytes land. Per-substrate-impl variation:

- **Default Claude Agent SDK substrate**: jsonl file-backed (per archived audit-trail-v2.md); local filesystem persistence; hash-chain integrity primitive; line-delimited AuditEvent records; query implementation reads file + filters
- **MS Agent Framework substrate** (future): may use different storage (Postgres / Azure Storage); audit-trail integrity via different mechanism; query via index-backed
- **Cloud-backed substrate impls** (future per Tier 2 deployment): cloud-storage-backed audit-trail; cross-region replication; integrity-verifiable across cloud boundaries
- **Federation-aware substrate impls** (future per Tier 3): cross-node audit-trail coordination; per-tenant isolation

In every case, the AuditEvent schema + audit-trail composition + 6 capability categories are the same — only the storage realization varies per substrate-impl. There are no alternative whole-class architectures realizing one Audit Surface differently; that's why this is a mechanism class rather than a Pattern A protocol.

### Per-shape policy declares

Each per-shape policy bundle declares:
- **Granularity** (claim-level / action-level / light per locked event entry Cross-archetype illustration)
- **Mandatory event-kind catalog** (per-shape required emissions; framework baseline always present)
- **Error semantics** (fail-closed for practitioner-shape; fail-open with alert for autonomous-business; fail-open with retry for personal-OS)
- **Trust model** (per-shape authority-binding policy: practitioner-judgment / budget-policy / individual — subsumes prior Trust Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade)
- **Append-only enforcement reference** (gate-dispatched-structural per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1; substrate-impl provides the gate)
- **Error mapping** (substrate-native errors → AuditError categories per §10)

## 5. Per-shape policy mechanics

The Audit mechanism class is **always present** in every workspace (not selectable; every workspace needs audit-trail). Per-shape granularity policy + per-substrate-impl storage realization are the variation knobs:

- **Per-shape variation**: granularity / event-kind catalog / error semantics / trust model declared in shape policy bundle
- **Per-substrate-impl variation**: storage backend (jsonl / Postgres / cloud / federation) inherits from selected substrate Implementation per substrate Surface §F

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Audit class Surface per workspace | 1 | Always present at framework-mechanism layer; not selectable |
| Audit-trails per workspace | 1 (logical; substrate-impl may use multiple files for rotation/archival but logically unified) | Always present; not selectable |
| Whole-class alternative implementations | N/A (not Pattern A) | AuditEvent schema + 6 capability categories fixed at framework-mechanism layer; storage variation is per-substrate-impl |
| Per-shape policy variants | Per-shape | Shape policy declares granularity + catalog + error semantics + trust model |

### Validation at workspace boot

Audit class validated at workspace boot:
- Selected substrate-impl provides storage substrate compatible with audit's append-only requirement
- Active shape's mandatory event-kind catalog supported by substrate-impl
- Existing audit-trail (if workspace pre-exists) hash-chain verifiable by substrate-impl
- Trust model from shape policy bundle composes with substrate Surface §C permission flow

### Re-binding semantics

Audit-trail re-bindable across substrate migrations (workspace identity persists; audit-trail migrates with workspace; integrity verification at migration boundary). Per L8 line 32 cross-deployment evidence requirement. Class Surface unchanged across substrate migration; only storage realization changes.

## 6. Mechanism-class structural reconciliation

Audit as mechanism class with per-shape granularity policy + per-substrate-impl storage realization:

| Aspect | Layer | What it is |
|---|---|---|
| **Class Surface** (AuditEvent schema + 6 capability categories) | mechanism (framework-level) | Framework-level interface contract; AuditEvent schema + emission/persistence/query/integrity/catalog/state-rendering categories — same across all substrate-impls |
| **Per-substrate-impl realization** | substrate Surface §F | Storage backend (jsonl / Postgres / cloud / federation) inherits from selected substrate Implementation; audit class Surface unchanged |
| **Per-shape policy bundle** | shape (policy layer) | Granularity + mandatory event-kind catalog + error semantics + trust model declared in shape policy bundle |
| **Skill-side + substrate-internal emission** | runtime | Substrate emits architectural events directly; skills emit via MCP audit gate; both validated against AuditEvent schema; both land in same audit-trail |

### Audit-trail-as-canonical-source (load-bearing architectural commitment)

Per archived audit-trail-v2 single-write architecture: audit-trail is single source of truth for reasoning chain; workspace state rendered FROM events; events append-only; never rewritten. Per L8 line 29: "Audit-trail integrity must survive intact across deployments / migrations." This commitment is foundational for axis-3 defensibility.

### Audit-class skill-portability

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code targeting Audit class Surface (AuditEvent schema + 6 capability categories) is portable across substrate-impls (storage backend swap doesn't break skill); skill code reaching substrate-impl-internal primitives (file-format / hash-algorithm / query-implementation) is substrate-impl-pinned by construction.

### Distinct from Pattern A protocols (substrate / adapter / quality-gate)

- substrate (Pattern A) = singular per workspace; tier-aware; alternative architectural designs (Claude Agent SDK / MS AF) realize Surface differently
- adapter (Pattern A) = multi-instance; per-class Surface variation; alternative impls per integration class realize Surface differently
- quality-gate (Pattern A) = singular per workspace per shape; alternative architectural designs (practitioner-shape-gate stateful procedure / autonomous-business-shape-gate programmatic threshold / personal-OS-shape-gate light reporting) realize Surface differently
- **audit = mechanism class** (AuditEvent schema + 6 capability categories fixed at framework-mechanism layer; per-shape granularity policy + per-substrate-impl storage realization vary; NO whole-class alternative architectures)
- **sparring = mechanism class** (8 sub-mechanism Surfaces; per-shape activation matrix; NO whole-class alternative architectures — see `arch/sparring.md`; sister mechanism class peer)

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Audit is a mechanism class within the framework's mechanism layer |
| `mechanism` | AuditEvent schema IS a mechanism (framework-level interface contract per locked entry); query primitives + 6 capability categories are mechanisms; the Audit class aggregates them |
| `shape` | Shape policy declares per-shape mandatory event-kind catalog + audit error semantics + trust model (per-shape authority-binding policy subsumed from prior Trust Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade) |
| `workspace` | Workspace inherits audit class Surface always (not selectable); shape policy provides granularity + catalog + trust |
| `protocol (architectural)` | Audit is **NOT** a Pattern A protocol per `docs/decisions/greenfield-rederivation-pause.md` Step 3 verdict (AuditEvent schema IS the Surface; per-shape granularity is POLICY-level; storage backend variation is substrate-impl level). Distinct from substrate / adapter / quality-gate. |
| **`event`** | **Locked GLOSSARY primitive: atomic structured emission unit; audit-trail is COMPOSITION (sequence over time). This topic articulates the composition mechanics + class Surface** |
| `actor` | Every event declares emitting actor; audit class Surface enforces actor declaration at emission |
| **`substrate`** | **Substrate Surface §8 dual-emission (substrate-internal direct + skill-side via MCP gate) converges in audit-trail; substrate emits architectural events; audit class persists. Substrate Surface §F (session + context management) provides storage realization. Substrate Surface §C (permission flow) integrates with audit's authority-binding mechanism (subsumed prior Trust Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade). Substrate also subsumes prior `coordination` Pattern A topic per same DR (substrate hooks + event-bus subsume cross-claim audit coordination).** |
| **`adapter`** | **Adapter §8 skill-side MCP-gate emission converges in audit-trail; per-action audit-event kinds per integration class. Adapter time-driven operations subsume prior `time` Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade.** |
| **`sparring` (mechanism class peer)** | **Sparring §8 skill-side MCP-gate emission converges in audit-trail; per-sub-mechanism event-kind catalog + axis-2 failure-mode detection events. Sparring is sister mechanism class — see `arch/sparring.md`.** |
| `claim` | Claims emit `claim_made` events (per claim entry composes-with); per-claim reasoning chain reconstructed via audit-trail query |
| `engaged authorship` | Per-claim attestation events ARE attestation-phase substrate; production-phase substrate is sparring events + source-grounded events |
| `defensibility` | Audit-trail provides reconstructible reasoning chain — one of three structural conditions defensibility tests |
| `rubber-stamping` | Events alone don't prevent rubber-stamping (events record sign-off, not engagement that would make sign-off substantive); per-claim attestation requirements + sparring-event presence are counter-mechanism |
| `quality-gate` (Phase 3.6) | Quality-gate (Pattern A protocol) consumes audit-event emissions for axis enforcement; per-shape policy declares quality-gate enforcement of audit requirements |
| Authority binding mechanism | Subsumes prior `trust` Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade; per-shape policy declares trust model (practitioner-judgment / budget-policy / individual). Lives in this class; substrate Surface §C permission flow integrates. |
| `workflow` | Workflow_instance lifecycle emits events (workflow_started, phase_transitioned, workflow_completed, etc.); audit-trail records workflow_instance state transitions |
| `work-unit` | Events scoped to work-unit (per `event` entry composes-with); per-work-unit attribution mandatory |
| `session` | Session_id field on events identifies session boundaries; cross-session audit-trail continuity preserved |

## 8. Substrate-internal vs skill-side audit emission (architectural-event kinds catalog; conditional section per template)

> **Template note**: This section is one of the 6 protocol-specific-conditional sections per the restructured Pattern A template (per `MAINTENANCE.md` Pattern A protocol topic template). For the audit mechanism class, the section applies because audit IS where dual-path emission converges — load-bearing for understanding the class.

### Architectural commitment

Audit class accepts events from two paths converging in single audit-trail:

| Emitter | Path | Use case |
|---|---|---|
| Substrate internal | Direct Python emission (substrate has direct internal access; NOT through MCP gate) | Substrate-architectural moments (registration / permission decision / boot complete / shutdown initiated) |
| Skill / specialist | MCP audit gate (`record_audit_event`) | Skill-side events (claim_made / sparring round / adapter operation / specialist activity) |

Both writes go through same Pydantic AuditEvent schema; both land in same `audit-trail.jsonl` per default substrate-impl; both validate identically. Reader (auditor or quality-gate) sees unified event stream.

### Audit-internal events (the class's own emissions)

The audit class emits its own integrity events:
- `audit_trail_integrity_verified` (periodic; per query / per migration boundary)
- `audit_trail_integrity_violated` (hash-chain broken; immediate emission)
- `audit_trail_migrated` (cross-deployment migration completed)
- `audit_trail_archived` (audit-trail compression / archival event; future per W3 watch-list)

Self-audit primitive: audit class audits its own integrity.

### Cross-substrate event-kind translation

Per G line 159 backup-restore-migration round-trip: substrate-specific metadata may be lost across substrate migrations. Audit class architectural commitment: substrate-specific metadata explicitly tagged at emission (e.g., `substrate_kind: claude_agent_sdk`); cross-substrate migration preserves event semantics OR marks substrate-specific-metadata-loss explicitly.

## 9. Cardinality + lifecycle

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Audit class Surface per workspace | 1 | Always present at framework-mechanism layer; not separately instantiated |
| Audit-trails per workspace | 1 (logical) | Single audit-trail per workspace; substrate-impl may use multiple files (rotation; archival) but logically unified |
| Events per audit-trail | Unbounded | Append-only; no per-event rewrite; archival per W3 |

### Lifecycle ownership

- **Class Surface**: framework-mechanism layer (always present; not separately instantiated)
- **Per-substrate-impl storage realization**: substrate-impl initializes audit storage realization at workspace boot (per substrate Surface §F)
- **Audit-trail file**: persists across workspace lifetime; substrate-impl owns; survives session boundaries

### Mutability

- **Class Surface immutable** at framework-mechanism layer (AuditEvent schema + 6 capability categories fixed)
- **Per-shape policy immutable** across single workspace boot (granularity + catalog + error semantics + trust model loaded at boot)
- **Audit-trail content append-only** (events never rewritten; per §2.B)
- **Cross-session persistence**: audit-trail persists across sessions (workspace lifetime); session_id field on events identifies session boundaries; session resumption preserves prior audit-trail state per substrate Surface §F

## 10. Boot + shutdown phase ordering (conditional section per template; load-bearing for audit class)

> **Template note**: This section is one of the 6 protocol-specific-conditional sections per the restructured Pattern A template. The audit class Surface lives at framework-mechanism layer (no per-instance boot of its own), but **audit's storage realization via substrate Surface §F has load-bearing ordering invariants** — the storage substrate must be ready BEFORE substrate emits its first architectural event (preserves invariant: every emitted event is persisted before workspace shutdown completes). Reframed as substrate-storage-realization ordering rather than separate audit-impl boot/shutdown lifecycle.

### Boot sequence

Audit storage realization (via substrate Surface §F) initializes BEFORE substrate emits its first architectural event:

1. Workspace boot triggers substrate-impl initialization (per `arch/substrate.md` §10)
2. Substrate-impl initializes its audit storage realization (per substrate Surface §F session+context management): loads config (file path; storage-specific config); validates audit-trail storage accessible
3. If existing audit-trail present: substrate-impl verifies hash-chain integrity (load prior tail event; verify ready-state)
4. Substrate-impl `audit_storage_ready` becomes True; emission API ready
5. Substrate proceeds with own boot; substrate events emit through audit gate from step 5 onwards (audit class Surface available before substrate emission)

### Shutdown sequence

Audit storage realization shuts down LAST (substrate shutdown drains in-flight events; audit must persist them all):

1. Substrate shutdown initiates (per `arch/substrate.md` §10): `shutdown_initiated` event emitted
2. In-flight agent runs drain; final events emit through audit gate
3. Substrate `shutdown_complete` emitted
4. Adapter + sparring (mechanism class peer) emissions drain; final events emit
5. Substrate-impl drains pending audit-trail writes; flushes audit-trail to storage
6. Substrate-impl verifies hash-chain integrity at shutdown
7. `audit_trail_integrity_verified` emitted (final event)
8. Substrate-impl audit storage realization shutdown returns

This ordering preserves invariant: every emitted event is persisted in audit-trail before workspace shutdown completes.

## 11. Audit error categories (conditional section per template; class-level error semantics)

> **Template note**: This section is one of the 6 protocol-specific-conditional sections per the restructured Pattern A template. For the audit mechanism class, error semantics differ per source layer (class-level vs substrate-impl-level vs shape-policy-level); documented here because per-shape error semantics are load-bearing for fail-closed/fail-open behavior.

| Category | Architectural meaning | Layer |
|---|---|---|
| `AuditWriteError` | Audit-trail write failure (filesystem unavailable; permission denied; disk full) | Substrate-impl raises; class Surface declares category |
| `AuditIntegrityError` | Hash-chain broken (audit-trail tampered OR corruption detected) | Substrate-impl detects; class Surface declares category |
| `AuditAppendOnlyViolation` | Attempted rewrite / truncate / rewind on audit-trail (architectural-rule violation; substrate-impl rejects) | Substrate-impl gate enforces; class Surface declares category |
| `AuditSchemaError` | Event doesn't match AuditEvent Pydantic schema | Class-level (schema is class Surface) |
| `AuditCatalogError` | Event_kind not in active shape's mandatory catalog OR not in baseline framework catalog | Class-level + per-shape-policy validation |
| `AuditQueryError` | Query failure (substrate-impl-internal; corruption; index issue) | Substrate-impl raises; class Surface declares category |
| `AuditMigrationError` | Cross-deployment migration failure (integrity not verifiable; format incompatible) | Substrate-impl raises; class Surface declares category |
| `AuditTrustError` | Authority-binding mechanism failure (per-shape trust policy violated; e.g., budget-policy threshold exceeded without practitioner approval) | Per-shape policy + substrate Surface §C permission flow integrate |

### Per-shape error semantics

- **practitioner-shape**: fail-closed on AuditWriteError + AuditTrustError (defensibility-critical; can't operate without audit-trail; architectural integrity required)
- **autonomous-business-shape**: fail-open with alert + queued-retry (continuity prioritized; alert on failure; retry mechanism)
- **personal-OS-shape**: fail-open with retry (lightweight; degradation acceptable)

Per-class Pydantic shape → Phase 6 spec.

## 12. Transport variation

> **Template note**: §12 (substrate-specific MCP transport variation) does NOT apply to the audit class — audit emission rides through whatever transport the substrate-impl provides (skill-side via MCP audit gate; substrate-internal via direct Python). Transport variation is **substrate-impl-level** (per `arch/substrate.md` §12), not audit-class-level. Section retained as N/A marker per restructured template's conditional applicability rule.

## 13. Deployment-tier awareness

> **Template note**: §13 (substrate-specific Tier 1/2/3 per-tier behavior) does NOT apply to the audit class as separate per-tier behavior — audit class Surface is tier-uniform; tier-driven variation lands at substrate-impl storage realization (Tier 2 may use cloud-backed storage; Tier 3 federation-aware) per `arch/substrate.md` §13. Section retained as N/A marker per restructured template's conditional applicability rule. Per-tier audit observability per L8 cross-deployment evidence requirement is documented in §10 boot/shutdown ordering + §11 error semantics, not as separate per-tier behavior on the class Surface.

## 14. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level:

- **AuditEvent Pydantic schema** (exact field shapes; required vs optional; per-event-kind discriminated union)
- **Audit-trail file format mechanics** (jsonl line structure; encoding; line-delimited validation; substrate-impl level)
- **Hash-chain algorithm choice** (SHA-256 default; alternative for high-integrity deployments; substrate-impl level)
- **Query implementation** (file-scan vs index-backed; performance characteristics; query language; substrate-impl level)
- **Append-only enforcement OS-level** (filesystem flags; alternative for substrate-impls without OS support)
- **Cross-deployment migration mechanics** (export format; import validation; integrity verification at boundary; substrate-impl level)
- **Audit-trail compression / archival strategy at scale** (W3; rotation policies; archival to cold storage; substrate-impl level)
- **External-format export** (PDF rendering; CSV aggregation; regulator-submission format)
- **Per-shape event-kind catalog declaration syntax** (in shape policy bundles)
- **Per-shape trust model declaration syntax** (in shape policy bundles; authority-binding per-shape configuration)
- **Audit-trail-state-rendering implementation** (state derived from event sequence; per-substrate-impl performance)

These belong to Phase 6 pre-implementation sharpening; ARCH topic explicitly does NOT lock these.

## 15. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| W1 | Hash-chain algorithm choice | First Tier 2+ deployment with concrete integrity requirements | Pick algorithm at Phase 6 implementation (substrate-impl level); hash-chain-with-Merkle for federation; SHA-256 for default |
| W2 | Cross-substrate event-kind translation rules | First substrate migration in production deployment | Define translation rules per substrate-pair; preserve substrate-specific metadata explicitly OR mark loss |
| W3 | Audit-trail compression / archival strategy at scale | First deployment with multi-year audit-trail accumulation | Define rotation policy; archival format; query mechanics across rotated/archived audit-trails (substrate-impl level) |
| W4 | Cloud-backed substrate-impl audit storage realization | First Tier 2 cloud deployment | Implement cloud-backed substrate-impl satisfying audit class Surface; audit-trail-integrity verification across cloud boundaries |
| W5 | Federation-aware substrate-impl audit storage realization | First Tier 3 federated deployment | Implement federation-aware substrate-impl; cross-node audit-trail coordination; per-tenant isolation |
| W6 | Per-shape trust-model concrete declarations | First second-shape productization (autonomous-business / personal-OS) | Validate per-shape trust model (practitioner-judgment / budget-policy / individual) against second-shape reality; potential refinement of authority-binding mechanism within audit class |

## 16. Decision-design provenance

Source materials:
- `archive/docs/decisions/audit-trail-v2.md` — single-write architecture (state rendered FROM events; append-only discipline)
- `archive/docs/decisions/audit-trail-v1.md` — initial audit-trail design
- `archive/docs/audit-pre-rag.md` — pre-RAG audit-trail considerations
- VISION axis-3 framing (defensibility test; reconstructible reasoning chain)
- Locked GLOSSARY `event` entry (atomic emission unit; audit-trail composition)

This topic articulates the audit **mechanism class** per `docs/decisions/greenfield-rederivation-pause.md` Step 3 verdict: AuditEvent schema IS the Surface (not "Surface + alternative architectural impls"); per-shape granularity (claim-level / action-level / light) is POLICY-level (which event kinds mandatory + at what granularity), not IMPL-level alternative architectures; storage backend variation (jsonl / LanceDB / Postgres / cloud-backed / federation) is **substrate-impl level** (per substrate Surface §F session+context management), not audit-class-level pluggability. Cross-validated by GLOSSARY `event` entry tags (Class **PRIMITIVE single-aspect** — not Pattern A).

**Trust Pattern A topic subsumption**: per same DR, prior `trust` Pattern A topic CANCELLED; trust model (practitioner-judgment / budget-policy / individual) folded into audit class as authority-binding mechanism with per-shape trust policy. Substrate Surface §C permission flow integrates. Trust as alternative-architectural-design Pattern A protocol failed greenfield derivation (per-shape variation is POLICY-level, not IMPL-level alternative architectures).

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: audit class stays shape-neutral / archetype-neutral / pioneer-neutral. Per-shape event-kind catalogs + per-shape trust models handle archetypal variation via shape policy.

## 17. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.4 | LOCKED |
| AuditEvent Pydantic schema | 6 | Mode 3 spec; per-event-kind discriminated union |
| Default substrate-impl audit storage realization (jsonl file-backed) | 6 | Concrete substrate-impl realization; append-only enforcement; SHA-256 hash-chain; query implementation |
| Per-shape event-kind catalog declarations | 6 | In shape policy bundles |
| Per-shape trust-model declarations | 6 | In shape policy bundles (per-shape authority-binding policy) |
| Cloud-backed substrate-impl realization | TBD per W4 signal | First Tier 2 cloud deployment |
| Federation-aware substrate-impl realization | TBD per W5 signal | First Tier 3 federated deployment |
| External-format export (PDF / CSV) | 6 | Per L8 auditor external-format requirements |
| Pre-implementation operational concerns | 6 | Pre-implementation sharpening at Phase 6 implementation-start |

## 18. Cross-references

- **GLOSSARY**: `event` (canonical primitive); `actor`, `mechanism`, `Framework C scope`, `Owner B scope`, `protocol (architectural)`, `substrate`, `adapter`, `sparring (axis 2)`, `claim`, `engaged authorship`, `defensibility`, `rubber-stamping`, `quality-gate`, `workflow`, `work-unit`, `session`, `shape`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (append-only as gate-dispatched-structural); `DISCIPLINES.md` Discipline 9 (coherence-audit cadence — audit class's audit-trail is the corpus those audits operate on)
- **Profiles validated**: `G-composability-gate.md` (line 159 backup-restore-migration round-trip; line 168 substrate-portability + substrate-pinned variation); `L5a-planner-pbs-schulz.md` (line 41 claim_made events emitted per substantive claim — DIRECTLY validates §11 practitioner-shape claim-level granularity); `L8-auditor-reviewer-posthoc.md` (line 29 audit-trail integrity; line 32 cross-deployment evidence; line 33 external-format requirements — DIRECTLY validate §10 boot/shutdown ordering + §14 external-format export)
- **ARCH topics composing with audit**: `arch/substrate.md` (Surface §8 dual-emission converges here; Surface §F provides storage realization; Surface §C permission flow integrates with audit's authority-binding mechanism; subsumes prior `coordination` Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade — substrate hooks + event-bus subsume cross-claim audit-trail coordination); `arch/adapter.md` (§8 per-action emission; subsumes prior `time` Pattern A topic per same DR — adapter time-driven operations subsume scheduled audit operations); `arch/sparring.md` (§8 per-sub-mechanism emission; mechanism class peer to audit); `arch/quality-gate.md` (Phase 3.6; Pattern A protocol consuming audit-event emissions for axis enforcement); `arch/claim-defensibility.md` (Phase 3.5; audit-trail provides reconstructible reasoning chain for defensibility test). Cancelled per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade: `arch/coordination.md` (subsumed into substrate hooks + event-bus) + `arch/trust.md` (folded into this audit class as authority-binding mechanism per above) + `arch/time.md` (subsumed into substrate-impl temporal semantics + adapter time-driven operations).
- **Phase 6 spec target**: `docs/specs/audit.md` (AuditEvent Pydantic schema + per-substrate-impl realization spec + per-shape event-kind catalog + per-shape trust-model declarations)
- **Archived sources**: `archive/docs/decisions/audit-trail-v2.md`, `archive/docs/decisions/audit-trail-v1.md`, `archive/docs/audit-pre-rag.md`
