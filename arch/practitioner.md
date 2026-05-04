---
title: Practitioner
topic-cluster: primitive-cluster (#2 of 4)
status: locked
---

# Practitioner

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the practitioner primitive cluster (the human-expert-author unit; Pattern C bipartite per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern C row). Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the practitioner-RECORD Pydantic schema (Mode 3). Foundation-up dependency: practitioner-RECORD is the human-actor anchor for authority-binding's per-event actor declaration (per `glossary/authority-binding.md`); locking practitioner second after specialist-skill means future Phase 3.5 `arch/claim-defensibility.md` topic locks per-claim attestation chain against an already-validated human-actor primitive.

## 1. Topic scope + frontmatter

**Cluster identity**: practitioner — the human-expert-author primitive cluster. Single-primitive cluster with bipartite structure: HUMAN aspect (cross-cutting; the natural person bearing legal/professional accountability in the world) + practitioner-RECORD aspect (Owner B; system representation enabling per-event attribution). Both aspects of one PRIMITIVE per locked GLOSSARY.

**Primitives covered**:
- `practitioner` — bipartite Pattern C (HUMAN cross-cutting + RECORD at Owner B); the human author unit around which axis 3 is built

**Cross-axis claim**: practitioner is the role axis 3 (authorship preservation) protects — primary axis-3 anchor — with cross-axis composition (axis-1 intertwining: practitioner is the human side of the co-worker pairing per `glossary/co-worker.md`; axis-2 sparring: practitioner is engagement subject of production-phase sparring per `glossary/engaged-authorship.md`). Axis-3 lean is load-bearing per `glossary/practitioner.md` axis classification.

**Cardinality at cluster level** (per-primitive detail in §5):
- Practitioner-RECORD cardinality per workspace = 1+ depending on shape (practitioner-shape solo workspace = 1; multi-practitioner-shape partnership workspace = N; legal-entity-shape workspace = N named practitioners under firm context per §3)
- HUMAN aspect: not "placed" in any scope; the person exists in the world; framework records nothing about the human directly — only the RECORD

**Cluster boundary**: this topic locks the bipartite HUMAN-vs-RECORD partition, the practitioner-RECORD frontmatter manifest schema, multi-practitioner workspace mechanics, legal-entity workspace context, lifecycle + deactivation semantics, and authority-binding integration. It does NOT lock claim mechanics (Phase 3.5 `arch/claim-defensibility.md` topic) or workflow + work-unit mechanics (Phase 3.5 `arch/workflow-work-unit.md` topic) or the workspace primitive itself (Phase 3.5 `arch/scope-model.md` topic) — those compose with this cluster's primitive but live in their own topics.

**Composition with framework**:
- HUMAN aspect lives at cross-cutting layer (not placed in any scope; the legal/professional accountability bearer in the world per `glossary/practitioner.md` line 16 + `glossary/owner-b-scope.md` line 32)
- practitioner-RECORD aspect lives at `Owner B scope` as workspace-scope managed entity (per `glossary/owner-b-scope.md` members list)
- Pattern C classification per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern C row (practitioner is the canonical Pattern C anchor)
- Authority-binding mechanism Surface (per `glossary/authority-binding.md`) consumes practitioner-RECORD identity for `actor_kind: human` event attribution; practitioner-RECORD IS the human authority bound to claim_made / signature_applied / sparring-engagement events
- Practitioner is one specific actor kind per `glossary/actor.md` (`actor_kind: human`); actor is the broader event-emitter category

**Phase routing**: practitioner-RECORD Pydantic schema → Phase 6 spec (Mode 3). Per-deployment practitioner-record entity-md authoring → workspace deployment (NOT this repo per `MAINTENANCE.md` TOP-LEVEL SCOPE instance-content lives at deployment-instance). This topic locks the architectural shape; Phase 6 locks typed contracts.

## 2. Per-primitive structural overview

### 2.1 HUMAN aspect (cross-cutting)

Per locked GLOSSARY `practitioner` entry: the human expert author who bears accountability for produced work — the natural person under whose name accountability-bearing output is signed and defended. The HUMAN aspect is **cross-cutting**, NOT placed in any scope. Framework records nothing about the human directly — the human exists in the world; framework's job is to make the human's accountability defensible via the RECORD aspect (per `glossary/practitioner.md` line 16).

**Architectural positioning**:
- The HUMAN bears accountability legally + professionally in the world (UNB challenge; opposing counsel; medical board review; peer review; engineering liability)
- The HUMAN is the legal/professional accountability bearer — the role the defensibility test (per `glossary/defensibility.md`) asks "will THIS person defend THIS output six months from now"
- The HUMAN is NOT a system entity, NOT placed in any framework scope, NOT addressable by any framework mechanism beyond what the practitioner-RECORD captures
- Framework's contract with the HUMAN is mediated through the practitioner-RECORD: every `actor_kind: human` event in the audit trail records the practitioner-RECORD identity, which references the HUMAN by legal name + (optionally) email

This aspect-asymmetry is load-bearing: framework does not pretend to model the HUMAN; framework models the RECORD that makes accountability traceable. The HUMAN remains the legal/professional accountability bearer regardless of framework state.

### 2.2 Practitioner-RECORD aspect (Owner B managed entity)

Per locked GLOSSARY `practitioner` entry + `glossary/owner-b-scope.md` members list: the system representation of a practitioner — a workspace-scope managed entity at Owner B carrying identity, credentials, signing authority, role bindings. The RECORD enables every per-event attribution chain that authority-binding mechanism enforces (per `glossary/authority-binding.md` per-event actor declaration sub-aspect).

**Frontmatter manifest schema** (architectural-level enumeration; Phase 6 lands Pydantic shape):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | str | required | Practitioner-record identifier; per-deployment uniqueness convention (deployment-side, NOT framework-side; deployment documents the convention per `extensions/<deployment>/conventions.md` per archived governance precedent §3 below) |
| `legal_name` | str | required | Full legal name of the natural person; the HUMAN aspect's identifier in the world |
| `actor_kind` | enum | required | `human` per `glossary/actor.md` actor_kind enum (practitioner is one specific actor kind; not multiple-kinds-of-practitioner) |
| `email` | str | optional | Contact + identity-mapping anchor for auth/SSO integration (per W2 watch-list adapter-mode mechanics) |
| `signing_authority` | enum | required | `independent` \| `under-supervision` \| `firm-bound` — framework-level enum constraining WHO can sign claims at framework level (gate-enforced structural per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1); per-shape policy declares which categories REQUIRED per shape per §8 |
| `role_bindings` | list | optional | Per-workspace role list constraining WHICH actions per shape policy (shape-policy-enforced); cross-references shape-policy role primitive (different scope from `signing_authority`; signing_authority constrains WHO can sign at framework level, role_bindings constrain WHICH actions per shape) |
| `credentials` | list | optional | Professional credentials (license number; bar admission; medical license; chamber membership) — per-shape-policy-mandated (e.g., legal-practice shape may mandate bar admission credential) |
| `mode` | enum | optional | `native` \| `adapter` — practitioner-RECORD source mechanics (PBS-native md file vs HR-system-sourced via adapter); composes with W2 Identity-class adapter Surface candidate per `arch/adapter.md` §3 partition |
| `adapter_binding` | str | optional | Adapter ID when `mode: adapter` (e.g., `personio` / `microsoft-entra` / `coolify-sso`); composes with `arch/adapter.md` Identity-class Surface per W2 |
| `lifecycle_state` | enum | required | `active` \| `dormant` per §SD-4 lifecycle states (deactivation = dormant-not-deleted per axis-3 defensibility-critical preservation rule) |
| `firm_binding` | str | optional | Reference to workspace.md `legal_entity_context` block (per §3 below; for legal-entity-shape workspaces only — practitioner-record references back to firm-level workspace context) |

**Schema explanation**: `signing_authority` and `role_bindings` operate at different scopes. `signing_authority` constrains WHO can sign claims at framework-mechanism level — gate-enforced structural per TOP-LEVEL DESIGN PRINCIPLES §1 (the gate dispatches on it for every signed-claim emission). `role_bindings` constrains WHICH actions per shape policy — shape-policy-enforced (declared per shape policy bundle; shape policy interprets which roles permit which actions). Different scopes; both load-bearing; not redundant.

**Adapter-mode source mechanics**: when `mode: adapter`, practitioner-RECORD is sourced from external HR/identity system via adapter Surface. The RECORD entity-md file contains frontmatter declaring `mode: adapter` + `adapter_binding: <adapter-id>`; body content is free-form prose describing how the deployment uses the external system. At session-open, gate hydrates RECORD via adapter (per W2 forward-link to `arch/adapter.md` Identity-class adapter Surface candidate). Native mode: RECORD entity-md file is source of truth; PBS owns the data.

## 3. Cross-primitive composition within the cluster

The practitioner cluster contains a single primitive with bipartite aspects (Pattern C). Cross-primitive composition is the bipartite HUMAN ↔ RECORD relationship + multi-practitioner workspace mechanics + legal-entity workspace context.

### Bipartite HUMAN ↔ RECORD composition

The HUMAN and RECORD aspects of a single practitioner compose as accountability-bearer + system-representation:
- The HUMAN bears legal/professional accountability in the world; the RECORD makes that accountability traceable in the audit trail
- The RECORD's `legal_name` field references the HUMAN; the RECORD's `id` field is the in-system identifier used in event attribution
- The defensibility test (per `glossary/defensibility.md`) asks "will THIS HUMAN defend THIS output"; the audit-trail reconstruction (per `arch/audit.md` §C query API) traces back through the RECORD to the HUMAN
- Per-claim attribution chain: every `claim_made` event records `actor_kind: human` + RECORD id; six-months-later defensibility test reconstructs WHO signed each claim by RECORD-to-HUMAN reference

### Multi-practitioner workspace mechanics

Cardinality matrix (per shape; per `glossary/practitioner.md` cardinality + lifecycle):

| Shape | Cardinality | Workspace context |
|---|---|---|
| **practitioner-shape solo** | 1 practitioner-record | Single-practitioner workspace; sole accountability bearer |
| **multi-practitioner-shape partnership** | N practitioner-records | N independent practitioners share workspace; each bears accountability for own work |
| **legal-entity-shape firm** | N practitioner-records | N named practitioners under firm-level legal-entity context (per §legal-entity workspace context below) |

**Cross-practitioner composition rules**:

| Composition direction | Permitted? | Mechanism |
|---|---|---|
| Practitioner-A READS practitioner-B's signed claim | YES | Audit-trail attribution preserved; reads cross practitioner-record boundary at framework level |
| Practitioner-A WRITES (modifies) practitioner-B's signed claim | NO | Per-claim ownership boundary structural per axis-3 defensibility (each practitioner accountable for own signed claims; cross-practitioner write would break attribution chain integrity) |
| Cross-practitioner workflow handoff (mid-workflow) | YES | Phase transition with attribution chain preserving prior + new owner; emits audit event recording handoff (`workflow_handoff` event-kind composes with workflow_instance state per `arch/workflow-work-unit.md` LOCKED) |
| Cross-practitioner SPARRING engagement | YES via AI runtime | Sparring engagement events record `actor_kind: ai_runtime` per `arch/sparring.md` §4 + `glossary/engaged-authorship.md`; cross-practitioner REVIEW (one practitioner reviews another's draft) is a separate workflow phase per archived `office-level-managed-entities.md` decision 1 layered enforcement pattern (greenfield-evaluated per §15 provenance) |

**Multi-practitioner concurrent-session handling**: each session binds to ONE practitioner-record at session-open via `session.bound_practitioner_id: str` field. Cross-session within workspace = multiple practitioner-records active concurrently in different sessions (one practitioner-record per session). Never multiple practitioners in single session — bipartite HUMAN aspect is singular per session; the practitioner-record bound at session-open is the human authority for all `actor_kind: human` events emitted within that session.

### Legal-entity workspace context

Legal-entity context (firm-level contracting party) lives at WORKSPACE level, NOT at practitioner level. Per `glossary/practitioner.md` "Legal-entity context (firm-level contracting party) lives at WORKSPACE level... not at practitioner level — practitioner is always a natural person":

- `workspace.md` may declare `legal_entity_context: { entity_name, entity_type, jurisdiction }` block for legal-entity-shape workspaces (firm = the legal entity contracting party; named practitioners sign under firm context)
- Practitioner-record references back to firm context via `firm_binding: workspace_id` field (per §2.2 schema; populated when workspace has legal-entity context)
- Practitioner is always a natural person regardless of workspace context — the firm doesn't sign claims; the named practitioner signs each claim under the firm's legal-entity context
- Cross-archetype examples: solo-practitioner workspace (no legal_entity_context); multi-practitioner-partnership workspace (N practitioners, no firm-level legal entity); legal-entity-firm workspace (N named practitioners under firm legal entity)

This separation is load-bearing per pattern-vs-instance discipline (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2): firm-level context is workspace-scope deployment configuration; practitioner is always the natural-person primitive.

## 4. Composition with framework primitives outside the cluster

| Primitive | Composition |
|---|---|
| `framework` | Practitioner is a framework primitive within `framework`'s primitive set; bipartite Pattern C per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE |
| `mechanism` | Practitioner-RECORD is consumed by `authority-binding` framework mechanism for `actor_kind: human` event attribution; gate-enforced at every accountability-bearing emission |
| `Owner B scope` | Practitioner-RECORD lives there as workspace-scope managed entity (per `glossary/owner-b-scope.md` members list) |
| `workspace` | Workspace contains 1+ practitioner-records as workspace-scope managed entities (per `glossary/workspace.md` "workspace serves practitioner(s); records at Owner B"); workspace cardinality per shape per §3 multi-practitioner mechanics; legal-entity workspace context per §3 |
| `shape` | Shape policy declares per-shape practitioner mandates (cardinality-per-shape; signing_authority-required-categories; deactivation policy; trust model variation per §8); per-shape consumption per `profiles/G-composability-gate.md` cross-shape framing |
| `actor` | Practitioner is one specific actor kind (`actor_kind: human` per `glossary/actor.md`); actor is the broader event-emitter category — practitioner is the human-actor primitive that authority-binding enforces accountability for |
| `authority-binding` (mechanism) | Practitioner-RECORD IS the human authority bound to `claim_made` / `signature_applied` / sparring-engagement events per `glossary/authority-binding.md` line 35 ("every `signature_applied` event records `actor_kind: human` + practitioner identity for legal-bind moments"); per-claim author attribution chain composes through practitioner-RECORD identity |
| `audit` (mechanism class) | All practitioner-related events flow through audit Surface §A emission per `arch/audit.md` §A; per-shape audit emission granularity composes with practitioner attribution per `arch/audit.md` §14 (claim-level / action-level / light per shape); cross-practitioner audit-trail query pattern via audit Surface §C query API for defensibility test mechanic |
| `substrate` (Pattern A) | Substrate Surface §C permission flow records practitioner identity at HITL approval moments (per `arch/substrate.md` §C; HITL approval requires recorded human-actor identity for the binding); substrate-emitted events carry practitioner attribution for `actor_kind: human` events |
| `adapter` (Pattern A) | Adapter Surface composes with practitioner-RECORD adapter-mode (W2 Identity-class adapter Surface candidate per `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition); adapter mode hydrates practitioner-RECORD from external HR/identity system at session-open per §2.2 |
| `sparring` (mechanism class) | Sparring engagement events record `actor_kind: ai_runtime` (per `arch/sparring.md` §4 + `glossary/engaged-authorship.md` "AI-runtime sparring events serve as the production-phase substrate"); practitioner is engagement subject — sparring fires AT practitioner judgment moments, not BY practitioner |
| `specialist-skill` (Phase 3.5 first primitive-cluster) | Cross-specialist activation actor binding: when specialist activates mid-session per `arch/specialist-skill.md` §5 mid-session re-binding, the activating actor (workspace-runtime activator per `arch/specialist-skill.md` §7 specialist_activated event-kind) is the practitioner-RECORD bound to current session; back-link to practitioner identity preserves attribution chain across capability changes |
| `claim` (`arch/claim-defensibility.md` LOCKED) | Practitioners are accountable for individual claims they author; defensibility test resolves at claim granularity (per `glossary/claim.md` + `glossary/defensibility.md`); per-claim attestation event records practitioner-RECORD identity for the attesting actor; full claim mechanics → `arch/claim-defensibility.md` |
| `engaged-authorship` (DERIVED axis-3) | Production-phase engagement (per `glossary/engaged-authorship.md`) tested via human-actor events (`actor_kind: human` for practitioner engagement signals); attestation-phase per-claim attestation event records practitioner-RECORD for attesting actor (full mechanics → `arch/claim-defensibility.md` LOCKED) |
| `co-worker` (DERIVED axis-1) | Practitioner is the human side of the co-worker pairing per `glossary/co-worker.md` (axis-1 intertwining; AI runtime is the AI side); practitioner-RECORD persists across sessions enabling cross-session co-worker continuity per axis-1 architectural support |
| `defensibility` (DERIVED axis-3) | Defensibility test asks "will THIS practitioner defend THIS output six months from now" per `glossary/defensibility.md`; practitioner is the role the test resolves against; practitioner-RECORD's persistence + lifecycle (dormant-not-deleted per §SD-4) preserves historic-claim attribution for re-runable defensibility tests |
| `session` | Session binds to ONE practitioner-record at session-open (`session.bound_practitioner_id: str`); cross-session multi-practitioner concurrency is workspace-level (per §3) |
| `event` | Every accountability-bearing event records `actor_kind` + practitioner-RECORD identity (when `actor_kind: human`) per `glossary/event.md` + authority-binding mechanism Surface enforcement |

## 5. Cardinality + lifecycle (per primitive)

### Practitioner-record cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Practitioner-records per workspace | 1+ | Per shape cardinality matrix per §3 (solo = 1; partnership = N; legal-entity-firm = N under firm context) |
| HUMAN aspect cardinality | N/A — not "placed" | Cross-cutting; the human exists in the world; framework records nothing about the human directly |
| Practitioner-records per session | exactly 1 | Per multi-practitioner concurrent-session handling (§3); session binds to ONE practitioner-record at session-open |
| Concurrent practitioner-records active | N (per workspace) | Multiple practitioner-records active concurrently across different sessions within workspace; never multiple in single session |

### Practitioner-record lifecycle

**Lifecycle states**: `active` | `dormant` (per §SD-4).

- **Creator**: workspace runtime at workspace setup (initial practitioner) OR per-practitioner-addition (subsequent practitioners joining a multi-practitioner workspace per `glossary/practitioner.md` cardinality + lifecycle)
- **Owner**: Owner B scope (workspace-bound; per `glossary/owner-b-scope.md` members list)
- **Mutability**: mutable-with-audit per `glossary/practitioner.md` (changes to credentials / signing authority / role bindings emit `practitioner_record_updated` events with `details.changed_fields: list[str]`; never silently rewritten)
- **Persistence across sessions**: practitioner-records persist through workspace lifetime; deactivated practitioners marked `lifecycle_state: dormant` per §SD-4 deactivation semantics
- **Destructor**: workspace dissolution per §13 archival-as-default (cross-pattern coherence with `arch/specialist-skill.md` §13)

### Practitioner-record lifecycle event-kind catalog (architectural-level)

Substrate emits AuditEvents at practitioner-record lifecycle moments. Event kinds (architectural enumeration; per-event-shape Pydantic schema → Phase 6):

- `practitioner_record_minted` — practitioner-record created at workspace setup OR per-practitioner-addition
- `practitioner_record_updated` — single event-kind with `details.changed_fields: list[str]` (NOT separate event-kinds per field; minimal event-kind catalog growth per archived `audit-trail-v2.md` `details:` payload precedent — greenfield-evaluated per §15)
- `practitioner_record_deactivated` — practitioner leaves workspace; `lifecycle_state` transitions to `dormant`; record NOT deleted (preserves audit-trail attribution to historic outputs per axis-3 defensibility-critical)
- `practitioner_record_reactivated` — dormant practitioner returns; `lifecycle_state` transitions back to `active`

Practitioner-lifecycle events compose with substrate §10 boot/shutdown sequence per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection — practitioner-record activation integrates within substrate-phase 3 adapter bindings load step (per §13 boot ordering integration).

## 6. Logic placement mode

Per `ARCHITECTURE.md` §6 Logic placement modes:
- **Practitioner-record entity-md** (`extensions/<deployment>/practitioners/<id>.md` frontmatter + body): Mode 1 production-runtime LLM-MD (workspace AI reads at session-open + at attestation moments) — though instance-content storage convention is deferred to Phase 6 deployment per R-SD-1 (per `MAINTENANCE.md` TOP-LEVEL SCOPE: instance-content storage is deployment-instance not framework)
- **Adapter-mode hydrated practitioner-RECORD** (when `mode: adapter`): Mode 2 production-runtime Python (substrate gate hydrates RECORD via adapter Surface at session-open)
- **Practitioner-RECORD Pydantic schema** (Phase 6 spec): Mode 3 hybrid spec layer
- **THIS topic + DR + GLOSSARY entries**: Mode 4 development-time documentation (NOT production-runtime)

Primitive-cluster topics are Mode 4 development-time documentation — articulating the architectural shape framework developers need to understand, not what production AI loads at runtime. Production AI in a deployed PBS workspace loads Mode 1 markdown (practitioner-record entity-md files at workspace level; not THIS framework topic).

**LLM-instruction tightness asymmetry** (per `ARCHITECTURE.md` §6 cross-cutting principles): Mode 1 markdown (practitioner-record body content; per-deployment convention prose for ID minting per archived governance-and-identity-sourcing pattern §4 prose-rules — greenfield-evaluated per §15) requires the highest LLM-instruction tightness review effort because LLMs paper over imprecise markdown by inference. Phase 6 deployment authoring inherits this discipline.

## 7. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns.

### Practitioner-error categories (architectural-level)

Per-shape error escalation policy lives in §8 Cross-shape policy variation; the categories themselves are framework-level:

| Category | Architectural meaning |
|---|---|
| `PractitionerRecordValidation` | Frontmatter fails schema validation (missing required fields; invalid enum values; signing_authority not in `independent` \| `under-supervision` \| `firm-bound`) |
| `PractitionerAdapterHydrationFailure` | Adapter-mode RECORD hydration fails at session-open (adapter Surface error; external HR system unreachable; identity-mapping email not found) |
| `PractitionerSigningAuthorityViolation` | Practitioner attempts signed-claim emission but `signing_authority` doesn't satisfy per-shape required category (e.g., `under-supervision` practitioner attempts independent signing in legal-practice shape requiring `independent`) |
| `PractitionerSessionBindingViolation` | Multi-practitioner concurrency violation (e.g., session attempts to bind two practitioner-records simultaneously per §3 multi-practitioner concurrent-session handling) |
| `PractitionerLifecycleStateConflict` | Operation requires `active` but practitioner-record is `dormant` (e.g., dormant practitioner attempts to sign new claim) |
| `PractitionerCrossPractitionerWriteViolation` | Practitioner-A attempts to modify practitioner-B's signed claim (per §3 cross-practitioner composition rules; structural per axis-3) |

### Other operational concerns (Phase 6)

- **Practitioner-record entity-md storage convention**: per-deployment storage path (e.g., `extensions/<deployment>/practitioners/<id>.md`) is deployment-instance per `MAINTENANCE.md` TOP-LEVEL SCOPE; specific path schema lands Phase 6 deployment (R-SD-1)
- **Per-deployment ID uniqueness convention**: prose-rule pattern per archived `governance-and-identity-sourcing.md` §4 (greenfield-evaluated per §15 — convention prose lives at deployment level, NOT framework level; AI applies at mint-time per Mode 1 markdown discipline)
- **Adapter-mode hydration caching**: per-session caching of hydrated practitioner-RECORD; cache invalidation on adapter-side updates; per W2 forward link
- **Cross-practitioner workflow handoff mechanics**: per W4 second-multi-practitioner-deployment-surface signal (full mechanics → Phase 6 + future Phase 3.5 `arch/workflow-work-unit.md` topic composition)
- **Multi-practitioner concurrent-session lock semantics**: implementation mechanics for `session.bound_practitioner_id` enforcement per §3 multi-practitioner concurrent-session handling
- **Per-claim attestation rate limits**: per-shape policy may impose attestation rate limits to detect rapid-batch rubber-stamping risk per `glossary/engaged-authorship.md` quality signals; per-shape implementation
- **Practitioner-record signing mechanism for historic-claim defensibility**: cryptographic signing format awaits W3 Phase 6 `arch/audit.md` §D integrity verification implementation

## 8. Cross-shape policy variation (cluster-conditional; APPLIES)

Per primitive-cluster topic template `MAINTENANCE.md` Layer 3 §8 conditional applicability + Pattern A template §14 cross-shape policy variation precedent + `arch/adapter.md` §14 + `arch/audit.md` §14: this section applies when primitive behavior is shape-policy-mediated. Practitioner cluster IS shape-policy-mediated (cardinality-per-shape + signing_authority-required-categories per shape + multi-practitioner mechanics per shape + legal-entity context per shape + deactivation policy + trust model variation).

**What is shape-uniform** (NOT shape-policy-mediated):
- Bipartite Pattern C HUMAN-vs-RECORD partition (same architectural commitment across all shapes)
- Practitioner-record frontmatter manifest schema (same fields across all shapes; per-shape policy declares which optional fields REQUIRED per shape)
- `actor_kind: human` enum value (same per actor.md across all shapes)
- Cross-practitioner write boundary (NO cross-practitioner writes to signed claims; structural per axis-3; same architectural commitment across all shapes; per-shape tightening additive, not relaxation)
- Lifecycle state enum (`active` | `dormant`; same across all shapes; archival-as-default destruction semantics same across all shapes per §13)

**What is shape-policy-mediated**:

| Dimension | practitioner-shape | autonomous-business-shape | personal-OS-shape |
|---|---|---|---|
| **Cardinality enforcement** | Solo: ≥1 mandatory; partnership/firm: N permitted | N/A (no human-practitioner concept in pure autonomous business; operator/board are humans but not "practitioners") | Single-user (typically 1; no professional-accountability concern) |
| **`signing_authority` required categories** | `independent` mandatory for solo + multi-practitioner; `firm-bound` permitted for legal-entity-firm; `under-supervision` permitted only with explicit handoff workflow per shape | N/A (no claim-signing concept; budget-policy-only authority per `arch/audit.md` §14 autonomous-business trust model) | Optional (no professional-accountability binding) |
| **`role_bindings` required** | Per shape policy (e.g., legal-practice shape may mandate roles like `partner` / `associate` / `paralegal`); shape policy interprets | N/A | Light (user-preference per session) |
| **`credentials` required** | Per shape policy (legal-practice shape may mandate bar admission; medical shape may mandate license) | N/A | Optional |
| **Practitioner-error escalation** (per §7 categories) | Fail-closed (defensibility-critical; signing authority violations must surface; no silent degradation) | N/A or fail-open with alert (continuity prioritized) | Fail-open (lightweight; degradation acceptable) |
| **Deactivation policy** | Strict preservation (record marked `dormant`; never deleted; audit-trail attribution preserved per axis-3) | Archival OR deletion-with-audit per business policy | Minimal lifecycle (deletion permitted per user preference; no professional-accountability concern) |
| **Cross-practitioner-handoff at deactivation** | May require explicit handoff-to-named-practitioner per shape policy (preserves attribution chain on outstanding workflow_instances) | May permit auto-routing per business policy | N/A (single-user) |
| **Multi-practitioner concurrency** | Multiple practitioner-records active concurrently in different sessions per workspace per §3 | N/A | N/A (single-user) |
| **Per-claim audit emission granularity** (composes with `arch/audit.md` §14) | Claim-level mandatory (per `arch/audit.md` §14 practitioner-shape granularity); each `claim_made` records practitioner identity per authority-binding | Action-level (per `arch/audit.md` §14 autonomous-business granularity); coarser attribution | Light (per `arch/audit.md` §14 personal-OS granularity); minimal binding |
| **Trust model parameterization** (per `arch/audit.md` §14) | Practitioner-judgment trust (every claim defensibility-required; signature_applied for legal-bind moments) | Budget-policy trust (signature only for budget-threshold; programmatic attestation per shape policy) | Individual trust (minimal; no professional-accountability binding) |

**Per-shape trust model parameterizes practitioner-record's accountability surface** (per `arch/audit.md` §14):
- practitioner-shape: every claim defensibility-required; six-months-later test concrete
- autonomous-business-shape: signature only for budget-threshold; operator-attestation programmatic
- personal-OS-shape: minimal accountability binding; light audit

Practitioner cluster primitives stay shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (practitioner is always a natural person regardless of shape; bipartite Pattern C structure is uniform). The per-shape variation lives in shape policy bundle declaring which optional fields REQUIRED + per-shape cardinality + per-shape lifecycle policy + per-shape trust model.

## 9. Granularity tests (cluster-conditional; N/A)

**N/A** — practitioner cluster has NO granularity discriminator. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §9 applies when primitives have granularity discriminators (e.g., specialist + skill 3-tests; two-tier classification per `arch/specialist-skill.md` §9). Practitioner has no such discriminator — one human-author = one practitioner; the bipartite-aspect partition (HUMAN vs RECORD) is NOT granularity (it's structural aspect-decomposition, not cardinality discriminator).

The question "should this be ONE practitioner or split into multiple?" doesn't arise — practitioner is singular always per `glossary/practitioner.md` "Not multiple-kinds-of-practitioner — practitioner is singular always; kind variation (solo / partnership / legal-entity-firm) lives at WORKSPACE LEVEL". Multi-practitioner workspace mechanics (§3) are workspace-level cardinality, not practitioner-level granularity.

§9 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule (preserves template-anchoring stability for downstream primitive-cluster topics).

## 10. Bundle composition (cluster-conditional; N/A)

**N/A** — practitioner-RECORD doesn't bundle artifacts. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §10 applies when a primitive in the cluster BUNDLES other artifacts (e.g., specialist BUNDLES skills + entity-kinds + workflows + work-unit-kinds + adapter implementations per `arch/specialist-skill.md` §10). Practitioner-RECORD is an identity entity, not a bundling primitive — it carries identity + credentials + signing authority + role bindings as schema fields, but doesn't BUNDLE other artifacts in a directory-structure sense.

§10 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule.

## 11. Marketplace + distribution mechanics (cluster-conditional; N/A)

**N/A** — practitioner-records aren't distributable. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template "5 cluster-conditional sections" applicability rule: §11 applies when a primitive in the cluster is canonical distributable (e.g., specialist as canonical distributable per `glossary/specialist.md` + `arch/specialist-skill.md` §11). Practitioner-records are identity entities owned-by-workspace at Owner B (per `glossary/owner-b-scope.md`) — they are workspace-bound deployment-specific instances, NOT distributable Framework C artifacts.

A practitioner-record is the system representation of a specific natural person within a specific workspace; it cannot be distributed (the HUMAN aspect is unique to the natural person; the RECORD aspect is bound to the specific workspace). Cross-deployment portability concerns (e.g., practitioner moves between firms) are workspace-migration mechanics per W2 + `profiles/G-composability-gate.md` backup-migration mode, NOT practitioner-record distribution mechanics.

§11 documented N/A explicitly per template "document N/A explicitly when section is omitted" rule.

## 12. Cross-references reservation

Cross-references for this topic are consolidated in §17 below per primitive-cluster topic template convention; this section number reserved as **N/A-parity slot** preserving visual numbering parity with substrate's §12 Transport variation N/A + `arch/specialist-skill.md` §12 reservation. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template §-numbering convention: "**§12 reserved as N/A-parity slot** (parity with substrate's §12 Transport variation N/A — preserves visual numbering parity across topic-templates; downstream primitive-cluster topic Writers MUST keep §12 reserved as N/A-parity rather than omit-§12 or fill-§12-with-content; prevents template drift)."

## 13. Per-primitive lifecycle ordering (cluster-conditional; APPLIES)

Practitioner-record activation cycles via workspace-scope events (per-practitioner-addition; deactivation; reactivation) + multi-practitioner activation has load-bearing ordering distinct from §5 cardinality + lifecycle treatment. Lifecycle ordering integrates with substrate boot/shutdown phases per `ARCHITECTURE.md` §6 "Workspace boot + shutdown composite sequence" subsection.

### Boot-time practitioner-record activation ordering

Per `ARCHITECTURE.md` §6 composite boot subsection substrate-phase 3 (adapter bindings load step), within that step practitioner-record activation orders as:

1. Per workspace.md `practitioners` declaration (or workspace.md state hydration mechanism), iterate practitioner-record set
2. For each practitioner-record: parse frontmatter; validate schema (`PractitionerRecordValidation` error if fail per §7)
3. Resolve `mode`:
   - `native`: load from entity-md file (per-deployment storage path per R-SD-1 Phase 6)
   - `adapter`: hydrate via adapter Surface at adapter binding load step (per `arch/adapter.md` §10 per-instance boot; `PractitionerAdapterHydrationFailure` if fail per §7)
4. Validate `lifecycle_state`: `active` → eligible for session binding; `dormant` → not eligible (preserves audit-trail attribution to historic outputs without permitting new claim-signing)
5. Per-shape policy applies cardinality + required-category enforcement (per §8 cross-shape policy variation; e.g., practitioner-shape mandates ≥1 active practitioner-record with `signing_authority: independent`)
6. Authority-binding mechanism Surface registers active practitioner-records as eligible `actor_kind: human` event emitters (per `glossary/authority-binding.md` per-event actor declaration sub-aspect)
7. Practitioner-record activation completes BEFORE substrate-phase 4 (specialist registration per `arch/specialist-skill.md` §13) — specialist activation may emit events recording activating actor (workspace-runtime activator binds to practitioner-record per cross-specialist activation actor binding composition)

### Mid-session activation ordering

Mid-session per-practitioner-addition (subsequent practitioner joins multi-practitioner workspace) follows boot-time activation ordering steps 2-6 for newly-added practitioner-records. Newly-deactivated practitioners (lifecycle_state transitions to `dormant`) follow shutdown ordering below. In-flight workflow_instances handled per shape policy (e.g., practitioner-shape may require explicit handoff-to-named-practitioner per §8 cross-practitioner-handoff at deactivation row).

Session-bound practitioner-record changes mid-session: NOT permitted per multi-practitioner concurrent-session handling — `session.bound_practitioner_id` is set at session-open and immutable for session lifetime; cross-practitioner workflow handoff mid-workflow opens new session bound to new practitioner per W4.

### Shutdown-time practitioner-record deactivation ordering

Per `ARCHITECTURE.md` §6 composite shutdown subsection, practitioner-record state persists across substrate shutdown (practitioner-records are workspace-scope managed entities at Owner B; persist through workspace lifetime per §5 lifecycle). No explicit deactivation step at substrate shutdown; practitioner-records remain in their `lifecycle_state` (active or dormant) for next workspace boot.

Per-practitioner deactivation event (`practitioner_record_deactivated` per §5 catalog) is workspace-event level (mid-workspace-lifetime), not substrate-shutdown level. Deactivation orders:

1. Per shape policy: cross-practitioner-handoff if required (per §8 cross-practitioner-handoff at deactivation row)
2. Drain in-flight signed-claim emissions for deactivating practitioner (per shape policy fail-closed vs fail-open)
3. Update practitioner-record `lifecycle_state` to `dormant`
4. Authority-binding mechanism Surface marks practitioner-record NOT-eligible for new event emissions (preserves historic-event attribution; permits no new event emissions)
5. Emit `practitioner_record_deactivated` event per §5 catalog

### Workspace dissolution (destruction semantics)

This topic LOCKS **archival as default** for practitioner-records on workspace dissolution per axis-3 defensibility-critical preservation rule (cross-pattern coherence with `arch/specialist-skill.md` §13 archival-as-default; same axis-3 reasoning):

- **Default**: archival preserves historic-claim attribution (six-months-later defensibility test re-runable; reconstructible attribution chain per `glossary/authority-binding.md` requires practitioner-RECORD persistence)
- **Opt-in**: deletion-with-audit policy declared at `workspace.md` level (workspace declares `instance_content_dissolution_policy: archive | delete-with-audit` per `arch/specialist-skill.md` §13 precedent; same field shape — cross-pattern coherence)
- Per-shape policy may restrict the opt-in (practitioner-shape policy may prohibit deletion-with-audit per defensibility-critical concern; per §8 deactivation policy row)

Archival mechanics → Phase 6 (workspace serialization mechanics; archive format; restoration semantics; per `profiles/G-composability-gate.md` backup-migration mode).

## 14. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| **W1** | Multi-tenant federation practitioner identity | Tier 3 cross-org federated deployment per archived governance-and-identity-sourcing.md decision 1 OR `arch/audit.md` §15 federated audit-trail W5 signal | Cross-tenant practitioner identity isolation mechanics + cross-org attribution chain semantics design fires when concrete federation deployment surface emerges; `BACKLOG.md` Phase 5+ ROADMAP entry |
| **W2** | Adapter-mode practitioner-RECORD source mechanics + Identity-class adapter Surface candidate | Concrete adapter implementation surface (Personio / Microsoft Entra / Coolify SSO / BambooHR) | Per-class Identity Surface design fires per `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition (universal-applicability across practitioner-shape / autonomous-business-shape / personal-OS-shape? → framework-baseline candidate; introduced by specific shape's policy bundle? → shape-extension candidate); 6th-class adapter Surface candidate per `arch/adapter.md` §4 per-class enumeration |
| **W3** | Practitioner-record signing mechanism for historic-claim defensibility | Phase 6 `arch/audit.md` §D integrity verification + cryptographic-signature implementation | Practitioner-record signing format design fires when Phase 6 audit-trail integrity implementation lands; integrates with practitioner-record `signing_authority` field per §2.2 |
| **W4** | Cross-practitioner workflow handoff mechanics + per-shape policy variation | Second multi-practitioner deployment surface (pioneer is solo per `profiles/L5a-planner-pbs-schulz.md` lines 95-101) | Per-shape cross-practitioner-handoff mechanics (workflow_handoff event-kind shape; attribution chain preservation rules; per-shape required-handoff-recipient enforcement) design fires when concrete multi-practitioner deployment friction surfaces; `BACKLOG.md` Phase 5+ ROADMAP entry; composes with future Phase 3.5 `arch/workflow-work-unit.md` topic |

## 15. Decision-design provenance

Provenance for this topic lives in DR + HANDOFF + git log per `MAINTENANCE.md` Lens 5 v0.2.1 provenance hygiene + per `coherence-audit` Lens 5. See `docs/decisions/practitioner-arch-topic.md` for sharpening trajectory + Round 1 + Round 2 EXPANSIONS + manufactured-criticism rejections + GLOSSARY back-check verdict + profile-anchored validation cluster citations + Mode 2 composite decomposition rationale.

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: practitioner cluster primitives stay shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz) reality (per `profiles/L5a-planner-pbs-schulz.md` lines 12-17 single-practitioner reality + lines 95-101 solo workspace evidence) grounds the cluster primitive without leaking pioneer specifics into the framework definition (PBS-specific terms like Bauleitplanung / B-Plan-Begründung / UNB / Stellungnahme do NOT appear in this topic's primitive definition; cross-archetype illustration in §4 + §8 anchors framework neutrality).

## 16. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.5 | LOCKED |
| Practitioner-RECORD Pydantic schema | 6 | Mode 3 spec; manifest schema typing per §2.2; PractitionerError class hierarchy per §7 |
| Per-deployment practitioner-record entity-md authoring | Workspace deployment (NOT this repo) | Per `MAINTENANCE.md` TOP-LEVEL SCOPE: instance-content storage convention is deployment-instance per R-SD-1; build into deployed workspace (Phase 6 deployment) |
| Per-deployment ID uniqueness convention prose | Workspace deployment (NOT this repo) | Prose-rule pattern per archived governance-and-identity-sourcing §4 (greenfield-evaluated per §15); deployment-side prose, AI applies at mint time per Mode 1 markdown discipline |
| Identity-class adapter Surface (W2) | Phase 6 | Per W2 watch-list; per `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition; concrete adapter implementations (Personio / Microsoft Entra / Coolify SSO) trigger 6th-class candidate |
| Practitioner-record signing mechanism (W3) | 6 | Per W3 watch-list; integrates with `arch/audit.md` §D integrity verification + cryptographic-signature implementation |
| Multi-tenant federation practitioner identity (W1) | 5+ | Per W1 watch-list; awaits Tier 3 cross-org federated deployment |
| Cross-practitioner workflow handoff (W4) | 5+ | Per W4 watch-list; awaits second multi-practitioner deployment; composes with Phase 3.5 `arch/workflow-work-unit.md` |
| Workspace serialization / archival format | 6 | Per §13 workspace dissolution; archival mechanics |

## 17. Cross-references

- **GLOSSARY**: `practitioner` (canonical Pattern C bipartite entry); `actor` (`actor_kind: human` for practitioner-emitted events); `authority-binding` (per-event actor declaration; practitioner-RECORD as human authority); `workspace` (workspace serves practitioner(s); records at Owner B; multi-practitioner mechanics + legal-entity context); `Owner B scope` (practitioner-RECORD placement); `defensibility` (axis-3 operational test resolves at practitioner-author granularity); `engaged-authorship` (production-phase + attestation-phase per-claim engagement composes through practitioner-RECORD identity); `co-worker` (practitioner is human side of axis-1 co-worker pairing); `claim` (practitioners accountable for individual claims; defensibility resolves at claim granularity through practitioner attribution); `session` (session binds to ONE practitioner-record at session-open per multi-practitioner concurrency rule); `event` (every accountability-bearing event records practitioner-RECORD identity when `actor_kind: human`); `framework`, `mechanism`, `shape`, `substrate`, `adapter`, `audit`, `sparring`, `specialist`, `skill`, `work-unit`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern C row (practitioner is canonical Pattern C anchor); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (signing_authority gate-enforced structural; cross-practitioner write boundary structural per axis-3); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (practitioner is always natural person regardless of shape; pioneer-neutrality of cluster primitive); `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment practitioner-record instance-content lives at deployment-instance, not framework repo); `ARCHITECTURE.md` §6 cross-cutting principles "AI as runtime" + "LLM-instruction tightness for Mode 1 markdown layer" + "Workspace boot + shutdown composite sequence"; `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 10 (greenfield-evaluation of archived sources)
- **Profiles validated**: `G-composability-gate.md` (lines 14-22 multi-mode consumption framing for cross-shape practitioner-record handling; lines 154-157 cross-shape consumption rules for shape-policy-mediated practitioner cardinality + signing_authority requirements; lines 162-184 architectural concerns surfaced — backup-migration round-trip implicates practitioner-record portability per W1) + `L5a-planner-pbs-schulz.md` (lines 12-17 single-practitioner reality + lines 76-83 solo specialist activation set + lines 95-101 multi-user-moments evidence — solo workspace + external actors as engagement targets, not workspace users; lines 119-129 stress-tests including solo defensibility scenario + capacity-building) + `L1-specialist-creator.md` (lines 18-29 specialist creator stress-tests cited as Cluster A producer evidence — practitioner is one of the L1 producer's intended-stress-test surfaces; specialist creator profile validates cross-shape compatibility surface for practitioner-RECORD shape-policy-mediated mandate per §8) + `INDEX.md` D Defer Gate procedure (per `profiles/INDEX.md` "D Gate procedure" — applied to W1 + W4 deferrals; mental-modeling-resolves test passed for shape-uniform Pattern C structural articulation; genuine awaited-evidence test passed for multi-practitioner federation + cross-practitioner handoff per absence of pioneer evidence)
- **ARCH topics composing with practitioner**: `arch/substrate.md` (Surface §C permission flow records practitioner identity at HITL approval moments; substrate registration of authority-binding-eligible actor records); `arch/audit.md` (§A emission API enforces actor declaration per practitioner-RECORD identity; §C query API for cross-practitioner audit-trail defensibility test; §14 cross-shape policy variation parameterizes per-shape audit emission granularity per practitioner attribution; §15 W5 federated audit-trail watch composes with W1 multi-tenant federation); `arch/sparring.md` (sub-mechanism engagement events `actor_kind: ai_runtime` per `glossary/engaged-authorship.md`; practitioner is engagement subject — sparring fires AT practitioner judgment moments); `arch/adapter.md` (W2 Identity-class adapter Surface candidate per §3 framework-baseline-vs-shape-extension partition; adapter-mode practitioner-RECORD source mechanics); `arch/specialist-skill.md` (cross-specialist activation actor binding back-link per §5 mid-session re-binding; activating actor is practitioner-RECORD bound to current session). `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster LOCKED; workflow_instance `bound_practitioner_id` + work-unit instance attribution compose through practitioner-RECORD per `arch/workflow-work-unit.md` §2.2 + §2.4 + §3 — multi-practitioner concurrent-session handling (each session binds to ONE practitioner-record; workflow_instance attribution composes through session-bound practitioner); cross-practitioner workflow handoff mechanics per §14 W4 composes with `arch/workflow-work-unit.md` W2 — same awaited-signal). `arch/claim-defensibility.md` (Phase 3.5 fourth primitive-cluster LOCKED; per-claim attestation chain via authority-binding + practitioner-RECORD identity per `arch/claim-defensibility.md` §3 + §13 — per-claim attestation event records `actor_kind: human` + practitioner-RECORD identity per `arch/practitioner.md` §4 session-bound practitioner; defensibility resolves at claim granularity through practitioner-RECORD attribution per `glossary/defensibility.md`; defensibility test asks "will THIS practitioner defend THIS output six months from now"; multi-practitioner co-attestation mechanics per `arch/claim-defensibility.md` §14 W3 cross-link to `arch/practitioner.md` §14 W4 + W1 — same awaited-signal). `arch/scope-model.md` (Phase 3.5 first cross-cutting integrator LOCKED — practitioner Pattern C bipartite composes through scope-model per §4 E4 cross-cutting non-placed pattern (HUMAN aspect cross-cutting NOT placed — the natural person bearing legal/professional accountability in the world; framework records nothing about HUMAN directly per §2.1) + RECORD aspect placed at Owner B as workspace-scope managed entity universal per `arch/practitioner.md` §2.2; multi-practitioner cardinality + legal-entity workspace context placement at WORKSPACE level per §3 composes with `arch/scope-model.md` §8 cross-shape policy variation 6-row matrix workspace.md required fields per shape row; §18 per-primitive composition table practitioner row); `arch/axis-interactions.md` (Phase 3.5 sixth + final ARCH topic LOCKED; second cross-cutting integrator extending scope-model anchor WITHOUT variation — practitioner Pattern C bipartite cross-axis per §4.1 per-primitive axis-anchoring catalog: axis-1 co-worker pairing (practitioner is the human side of the co-worker pairing per `glossary/co-worker.md`); axis-2 sparring engagement subject (sparring fires AT practitioner judgment moments per `arch/sparring.md` §4 + `arch/practitioner.md` §4 — practitioner-RECORD identity enables actor-binding for sparring engagement); axis-3 authorship preservation ROLE protected (practitioner is the role axis-3 protects per `glossary/authorship-preservation.md`; defensibility resolves at practitioner-author granularity); §18 per-primitive composition table practitioner row — Phase 3.5 CLOSED with this lock)
- **Phase 6 spec target**: `docs/specs/practitioner.md` (PractitionerRecord Pydantic schema; signing_authority enum; lifecycle state machine; practitioner-error class hierarchy)
- **Archived sources** (INPUT only per `disciplines/10-greenfield-evaluation.md` — archive citations name SOURCE where input came from, NOT TEMPLATE where structure transferred; each cited element greenfield-evaluated against current locked vocabulary per Discipline 10): `archive/docs/decisions/office-level-managed-entities.md` (NAMING SUPERSEDED per archived header — "Office-level managed entities" → "Workspace-scope managed entities" per current locked vocabulary; ActorEntity schema lines 84-95 cited as INPUT for practitioner-RECORD field enumeration but NOT transcribed verbatim — archive conflates actor + practitioner; current locked vocabulary SEPARATES them per `glossary/actor.md` "actor is broader category, practitioner is one actor kind"; greenfield-derived practitioner-RECORD schema per current Pattern C bipartite); `archive/docs/decisions/governance-and-identity-sourcing.md` (decision 1 = role primitive at shape-policy per current vocabulary — applied to `role_bindings` field per §2.2 / §8; decision 2 = native vs adapter mode for practitioner-RECORD source — applied to `mode` + `adapter_binding` fields per §2.2; decision 3 = per-deployment uniqueness convention preserved as deployment-side commitment per §7 / §16; decision 4 = prose-rules pattern for ID minting cited as deployment-level discipline)

## 18. Composition table

How practitioner cluster primitive composes with key framework primitives + Pattern A protocols + mechanism classes (single-primitive cluster per Pattern C; one column per cluster primitive — practitioner):

| Composing primitive | Practitioner composition |
|---|---|
| **substrate Surface §C** (permission flow) | Substrate Surface §C records practitioner-RECORD identity at HITL approval moments; permission decisions bind to identified human actor per `glossary/authority-binding.md` "authority-decision binding" sub-aspect |
| **substrate Surface §F** (session/context management) | Session binds to ONE practitioner-record at session-open via `session.bound_practitioner_id`; substrate manages session lifecycle preserving practitioner attribution across session events |
| **audit mechanism class** (Surface §A emission API) | Every accountability-bearing event records `actor_kind` + practitioner-RECORD identity per `glossary/authority-binding.md` per-event actor declaration; per-shape audit emission granularity composes (claim-level for practitioner-shape; action-level for autonomous-business; light for personal-OS) |
| **audit mechanism class** (Surface §C query API) | Cross-practitioner audit-trail query pattern for defensibility test mechanic; reconstruct historic-claim attribution chain through practitioner-RECORD identity (six-months-later test) |
| **authority-binding mechanism** | Practitioner-RECORD IS the human authority bound to `claim_made` / `signature_applied` / sparring-engagement events per `glossary/authority-binding.md` line 35; per-claim author attribution chain composes through practitioner-RECORD identity |
| **adapter** (Pattern A protocol) | Adapter-mode practitioner-RECORD source mechanics per W2 Identity-class adapter Surface candidate per `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition; hydration via adapter Surface at session-open |
| **sparring** (mechanism class) | Sparring engagement events record `actor_kind: ai_runtime` per `arch/sparring.md` §4; practitioner is engagement subject — production-phase engagement composition per `glossary/engaged-authorship.md` |
| **specialist-skill** (Phase 3.5 first primitive-cluster) | Cross-specialist activation actor binding: when specialist activates mid-session per `arch/specialist-skill.md` §5 mid-session re-binding, the activating actor is practitioner-RECORD bound to current session; back-link preserves attribution chain across capability changes |
| **claim primitive** (Phase 3.5 `arch/claim-defensibility.md`) | Practitioners accountable for individual claims per `glossary/claim.md`; per-claim attestation event records practitioner-RECORD identity for attesting actor; defensibility resolves at claim granularity through practitioner attribution chain |
| **engaged-authorship** (DERIVED axis-3) | Production-phase + attestation-phase per-claim engagement (per `glossary/engaged-authorship.md` two-phase composite test) composes through practitioner-RECORD identity for `actor_kind: human` engagement signals; AI-runtime sparring events serve as production-phase substrate, practitioner-RECORD events serve as attestation-phase substrate |
| **co-worker** (DERIVED axis-1) | Practitioner is human side of co-worker pairing per `glossary/co-worker.md`; practitioner-RECORD persists across sessions enabling cross-session co-worker continuity per axis-1 architectural support |
| **defensibility** (DERIVED axis-3) | Defensibility test resolves at practitioner-author granularity per `glossary/defensibility.md`; practitioner-RECORD persistence + dormant-not-deleted lifecycle (per §13) preserves historic-claim attribution for re-runable defensibility tests |
| **workspace** | Workspace contains 1+ practitioner-records as workspace-scope managed entities per `glossary/workspace.md`; workspace cardinality per shape per §3 multi-practitioner mechanics; legal-entity workspace context per §3 |
| **shape** | Shape policy declares per-shape practitioner cardinality + signing_authority required categories + role_bindings + credentials + deactivation policy + trust model variation per §8 |
| **Pattern A protocols** (substrate / adapter / quality-gate) | Practitioner composes with substrate Surface §C + §F (permission flow + session management); adapter Surface §3 partition (W2 Identity-class candidate); quality-gate Pattern A LOCKED Phase 3.6 per `arch/quality-gate.md` composes with practitioner-attestation events for axis-3 intervention per `glossary/engaged-authorship.md` quality-gate row |
| **Pattern B primitives** (specialist / workflow / work-unit) | Practitioner is co-worker pairing partner with specialist activation (per `arch/specialist-skill.md` §5); workflow handoff mechanics per W4 (cross-practitioner workflow handoff); work-unit per `glossary/work-unit.md` (practitioners are human authors signing work-unit outputs; defensibility test asks "will the practitioner defend THIS work-unit's outputs?") |
