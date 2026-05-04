---
title: Adapter
topic-cluster: Pattern A protocol topics (#2 of 3)
status: locked
---

# Adapter

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the adapter Pattern A protocol. Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the Pydantic Protocol contract per per-integration-class Surface (Mode 3). Foundation-up dependency: adapter composes with substrate's Surface §C (permission flow) + §B (MCP server registration) + audit emission paths (per `arch/substrate.md` §8).

## 1. Topic scope

**Adapter** is the external-integration-boundary primitive — the workspace's contract with EXTERNAL-WORLD systems. Per locked GLOSSARY entry: tri-aspect Pattern A (per-integration-class Adapter Protocol surface = mechanism; implementations = Framework C definitions; running instance(s) = workspace-bound at Owner B per workspace.md adapter bindings, typically MULTIPLE simultaneously).

**Internal-vs-external axis (load-bearing distinction from substrate)**: substrate = INTERNAL runtime contract for agent execution within the workspace; adapter = EXTERNAL-WORLD integration boundary connecting workspace to outside systems. Both are Pattern A primitives; cardinality follows from this distinction (substrate singular per workspace; adapter multiple per workspace).

**Cross-axis**: different adapters serve different axes — email-adapter primarily axis-3 (sending semantics; engaged-authorship attestation moments at send); accounting-adapter cross-cutting business operations; MCP-adapter cross-axis tooling.

**Cardinality**: multi-instance per workspace (bounded by `workspace.md` adapter bindings list; per-shape policy may declare maximum); cardinality variation IS the architectural distinction from substrate's structural-singularity. Pioneer (PBS-Schulz per `profiles/L5a-planner-pbs-schulz.md` line 90): "Active adapters: email (Outlook); LaTeX compile; document signing (qualified electronic signature for sent docs)" — three adapters concurrently active in single workspace illustrate the multi-instance shape (instance count not architecturally fixed; bound by workspace declaration).

**Composition with framework**:
- One mechanism category within `framework`
- Per-integration-class Adapter Protocol surface IS a `mechanism` per class
- Implementations live at `Framework C scope` as distributable definitions
- Running instances bound to `Owner B scope` per workspace deployment (multiple simultaneous)
- Pattern A protocol per `protocol (architectural)` GLOSSARY entry (parallel to substrate)

This topic articulates: META-Surface pattern + per-integration-class Surfaces (email / accounting / MCP-server / A2A-peer / file-sync as named instances; future per ecosystem maturity), boundary criteria, multi-instance Implementation aspect, Selection mechanics (workspace.md adapter bindings), tri-aspect reconciliation, composition with framework primitives, audit emission via MCP gate (skill-side), permission flow composition with substrate, cross-shape policy variation, and pre-implementation forward-references.

**Phase routing**: Pydantic Protocol contract (per per-integration-class Surface) → Phase 6 spec (Mode 3). Per-adapter-Implementation work → Phase 6. This topic locks the architectural shape; Phase 6 locks typed contracts + impls.

## 2. Adapter Protocol Surface (architectural-level)

Adapter has a **two-layer Surface structure** distinct from substrate's single-layer Surface:

### META-Surface (cross-class architectural pattern)

Every adapter Implementation must satisfy the META-Surface (architectural conventions applying across all integration classes):

- **Lifecycle entry**: `from_config(config)` boot; `shutdown()` graceful; `is_ready` property; per-instance identity
- **Auth surface**: per-class auth model declared (OAuth / API key / shared secret / certificate / none); auth-refresh capability; auth-state persistence semantics
- **Permission flow integration**: write operations request permission via substrate Surface §C before action (per §7 Composition + §8 audit-event kinds)
- **Audit emission**: per-action audit events emitted via MCP audit gate (skill-side; NOT substrate-internal direct emission per §6 Audit emission); per-class event-kind catalog
- **Error mapping**: per-class native errors mapped to common architectural categories (per §10)
- **Health check**: per-instance health-status query (architectural; Phase 6 typed)
- **Versioning**: semver-like Implementation version; declared min-version + compat-version per workspace.md binding

### Per-integration-class Surfaces (semantically coherent per class)

Each integration class has its own Surface contract — the META-Surface conventions plus class-specific capability categories. Five named per-class Surfaces (current set; future per ecosystem):

| Per-class Surface | Capability categories (architectural-level) |
|---|---|
| **Email Adapter Surface** | send (compose + send) / fetch (poll + filter) / threading (in-reply-to + references); inbound webhook subscription (where supported) |
| **Accounting Adapter Surface** | invoice (create + modify + cancel) / payment (record + match) / ledger (sync + query); period-lock awareness |
| **MCP-Server Adapter Surface** | tool registration (per substrate Surface §B; transport selection in-process / subprocess / HTTP) / capability negotiation / tool invocation |
| **A2A-Peer Adapter Surface** | peer handshake (capability declaration + trust check) / request-send (federation message) / response-receive (async return) / capability discovery |
| **File-Sync Adapter Surface** | source declaration (filesystem / cloud / repository) / sync (fetch + push) / conflict resolution / change subscription |

Per-class Surfaces are NOT extension Protocols — every implementation in a class MUST satisfy that class's Surface. Per-class Surfaces are independently versionable + extensible.

### Explicitly NOT in Surface (cross-class concerns)

The following are NOT in any per-class Surface; they're cross-class architectural concerns handled at META-Surface level OR via composition:
- Substrate-coupling (handled via composition; adapter runs within substrate per §7)
- Specialist composition (handled via specialist Pattern B bundling per `specialist` GLOSSARY entry)
- Cross-adapter coordination (handled via substrate hooks + event-bus per `arch/substrate.md` §2.E; coordination Pattern A protocol CANCELLED per `docs/decisions/greenfield-rederivation-pause.md` Step 3 cascade)

### Logic placement mode

Surface contracts articulated here (Mode 4 conceptual) + Phase 6 spec (Mode 3 Pydantic Protocol per per-integration-class Surface + companion docs). Mode 1 production-runtime AI doesn't load this topic — production AI loads Mode 1 markdown above the Surface abstraction.

## 3. Common-surface boundary criteria

Decision rule for "in META-Surface" vs "in per-class Surface" vs "out of any Surface":

| Decision criterion | Verdict | Examples |
|---|---|---|
| Architectural convention applying to ALL adapter classes | META-Surface | Auth surface; lifecycle entry; permission flow integration; audit emission; error mapping; versioning |
| Capability native to a specific integration class with consistent shape across implementations within that class | Per-class Surface | Email send/fetch/threading; accounting invoice/payment/ledger; MCP tool registration |
| Capability specific to a SINGLE implementation only (no other impl in class supports) | Implementation-internal (NOT in any Surface) | Outlook-specific MAPI extension; Fastbill-specific German tax-form fields; Anthropic-MCP-specific extension |
| Cross-adapter / cross-class concern | Composition with another Pattern A protocol | Cross-adapter coordination → coordination protocol; trust-handshake → trust protocol |
| Future-only feature (not supported in current implementations) | Don't add yet (per no-defer principle's external-info-test) | Wait for impl to ship |

Boundary criteria operate at:
- META-Surface design moment (this ARCH topic + Phase 6 spec)
- Per-class Surface design moment (this ARCH topic per current 5 classes; new classes added via DR amendment per cascade discipline)
- Per-Implementation design moment (Phase 6 implementation work)

### Framework-baseline class vs shape-extension class

Per-class Surfaces partition into two categories along a layer-of-introduction discriminator. The discriminator determines WHERE the class lives + WHEN it activates + WHO defines it; per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (framework primitives stay shape-neutral; shape policy bundle handles per-shape variation).

| Category | Defined by | Applicability | Activation | Lifecycle |
|---|---|---|---|---|
| **Framework-baseline class** | Framework-mechanism layer (this ARCH topic + Phase 6 META-Surface + per-class Pydantic Protocol spec) | ALL framework-supported shape archetypes (practitioner / autonomous-business / personal-OS / federation / hybrid) — universal applicability | Available in any workspace regardless of selected shape; shape policy may activate / restrict / set per-shape adapter behavior (per §14 cross-shape policy variation) but does NOT redefine the per-class Surface semantically | Lives in framework distribution; new classes added via framework-mechanism-layer DR amendment per cascade discipline |
| **Shape-extension class** | Shape policy bundle (additive layer per shape; lives in shape's distributable artifacts) | Specific shape's archetype only (per shape that introduces it; not necessarily reusable across other shapes) | Activated only in workspaces using the introducing shape (or shapes that inherit from it); NOT a framework-mechanism modification — additive layer per shape | Lives in shape policy bundle distribution; new shape-extension classes added via shape-policy-bundle DR per shape definer (L2 profile) |

**Discriminator test** (when first instance of a candidate per-class Surface surfaces):

1. **Universal-applicability test**: Would this per-class Surface apply across ALL framework-supported shape archetypes — testable via hypothetical legal-practice / research-paper / engineering-doc workspaces (per `glossary/authority-binding.md` boundary-test pattern)? If yes → framework-baseline candidate.
2. **Shape-specific test**: Does this per-class Surface only make sense within a specific shape's archetype scope (introduced by that shape's policy bundle as additional class beyond framework-baseline)? If yes → shape-extension candidate.
3. **Semantic-redefinition test**: Does the per-class Surface require redefining a framework-baseline class's semantics for a specific shape (vs additive new class)? If yes → NOT shape-extension; that's framework-mechanism-layer revision per cascade discipline.

**Current 5 per-class Surfaces — CONFIRMED FRAMEWORK-BASELINE**:

| Per-class Surface | Framework-baseline confirmation |
|---|---|
| **Email Adapter Surface** | Universal-applicability: hypothetical legal-practice (brief delivery via email), research-paper (manuscript correspondence), engineering-doc (specification distribution) workspaces all need send / fetch / threading semantics. Email is a framework-baseline integration boundary despite Email having domain shape; the per-class Surface is shape-neutral. |
| **Accounting Adapter Surface** | Universal-applicability: hypothetical legal-practice (firm billing), research-paper (grant accounting), engineering-doc (project budget tracking) workspaces all need invoice / payment / ledger semantics. Accounting is a framework-baseline integration boundary despite Accounting having domain shape; the per-class Surface is shape-neutral (period-lock awareness is universal across accounting use cases). |
| **MCP-Server Adapter Surface** | Universal-applicability: any framework-supported shape may consume MCP-protocol-exposed tools (corpus retrieval / external-system query / capability extension). Tool registration + capability negotiation + invocation are shape-neutral architectural concerns. |
| **A2A-Peer Adapter Surface** | Universal-applicability: any framework-supported shape may participate in cross-node specialist sharing (federation-shape primary; other shapes inherit via federation participation). Peer handshake + request-send + response-receive + capability discovery are shape-neutral architectural concerns. |
| **File-Sync Adapter Surface** | Universal-applicability: any framework-supported shape may need source-of-truth synchronization (filesystem / cloud / repository). Source declaration + sync + conflict resolution + change subscription are shape-neutral architectural concerns. |

**Shape-extension class candidates** (forward-pointer):
- Future per-class Surfaces emerging from shape policy bundle introduction land as shape-extension classes — they live in the introducing shape's distributable policy bundle, NOT in framework-mechanism-layer adapter distribution
- Examples (illustrative; not yet locked): document-signing class introduced by practitioner-shape (qualified-electronic-signature flow per L5a pioneer reality); compliance-reporting class introduced by autonomous-business-shape (regulatory-reporting flow per business compliance policy); per-domain integration boundaries surfaced by specific shape archetypes
- Lifecycle: additive layer per shape; new shape-extension classes added via shape-policy-bundle DR per shape definer (L2 profile); framework-baseline 5-class enumeration unchanged by shape-extension additions
- Resolution: when first candidate per-class Surface surfaces, apply discriminator test above to classify as framework-baseline (universal applicability → framework-mechanism-layer DR amendment) OR shape-extension (specific shape's policy bundle additive extension → shape-policy-bundle DR)

## 4. Per-implementation aspect

Implementations live at `Framework C scope` as distributable definitions. Each Implementation belongs to ONE integration class + satisfies that class's Surface + the META-Surface conventions.

### Pattern level

Any external-system integration that can satisfy a per-class Surface qualifies as an Implementation of that class. Pattern level is integration-system-shape-neutral within class boundaries.

### Current Implementation set (CIRCA 2026)

Named per-class Implementations (per GLOSSARY cross-archetype illustration + archived sources):

| Per-class Surface | Implementations |
|---|---|
| **Email Adapter** | gmail-adapter / outlook-adapter / generic-SMTP-adapter / Microsoft Graph email API |
| **Accounting Adapter** | fastbill-adapter / lexware-adapter / sevdesk-adapter / generic-OAuth-accounting-adapter |
| **MCP-Server Adapter** | Anthropic-MCP-server-adapter / generic-MCP-stdio-adapter / generic-MCP-HTTP-adapter |
| **A2A-Peer Adapter** | A2A-protocol-adapter (per archived `a2a-and-gemini-pattern-emulation.md`); federation-peer-adapter |
| **File-Sync Adapter** | git-adapter / dropbox-adapter / OneDrive-adapter / generic-WebDAV-adapter |

Per `profiles/L5a-planner-pbs-schulz.md` line 90: pioneer concurrent adapters = email (Outlook) + LaTeX compile + qualified-electronic-signature (document-signing). Document-signing is a candidate per-class Surface (cryptographic-signing-adapter; future per ecosystem maturity) — currently bundled via specialist or Layer A content.

### Per-implementation declares

Each Implementation declares:
- **Adapter identity** (id; e.g., `gmail`, `outlook`, `fastbill`, `mcp_anthropic`)
- **Integration class** (which per-class Surface this satisfies)
- **Per-class Surface satisfaction** (claim + impl mapping each capability category to native primitives)
- **META-Surface satisfaction** (auth model declared; permission integration; audit emission)
- **Configuration schema** (per-impl config — Pydantic; Phase 6)
- **Error mapping** (impl-native errors → common architectural categories per §10)
- **Bidirectional vs unidirectional shape** (per integration-class architectural pattern; e.g., email = mostly outbound + threading on inbound; A2A = bidirectional async; MCP = request/response)
- **Deployment-tier compatibility** (Tier 1 / Tier 2 / Tier 3; per-impl tier-specific behavior)
- **Versioning info** (semver; min-substrate-version; compat-substrate-versions)

### Bidirectional vs unidirectional architectural patterns

Per-integration-class architectural shape varies (per locked GLOSSARY claim):

| Pattern | Per-class examples |
|---|---|
| **Mostly outbound + threading on inbound** | Email (send dominant; threading manages inbound replies) |
| **Bidirectional sync (request/response)** | Accounting (invoice → response); CRM-adapters (Phase 6+ when added) |
| **Bidirectional async** | A2A-peer (federation; peer messages flow both directions independently) |
| **Push-receiver style** | File-sync with subscribe-to-changes; webhook adapters |
| **Pull-only** | Read-only file-sync; reference-data MCP adapters |

Per-class architectural shape determines lifecycle (when to drain inbound on shutdown; when to expect async returns; when to subscribe vs poll). Phase 6 spec encodes per-class shape in Pydantic Protocol typing.

## 5. Selection mechanics

`workspace.md` adapter bindings list selects which adapter Implementations to activate (multiple simultaneous). Each binding entry declares: integration class + Implementation id + per-instance config + min-version constraint.

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Adapter Implementations active per workspace | bounded by `workspace.md` adapter bindings list (no architectural cap; per-shape policy may declare maximum) | workspace.md adapter bindings list; per-binding entry; shape policy bundle may impose cap |
| Adapters per integration class per workspace | 1 by default; multi-account mechanics deferred to W4 watch-list resolution per §16 | Workspace can bind multiple instances when W4 multi-account mechanics resolve (e.g., personal + work email); shape policy may declare per-class cardinality constraints |
| Implementations per Framework C catalog | M per class | Multiple distributable definitions per class; current set named in §4 |
| Per-class Surfaces in framework | 5 currently; future per ecosystem | Email / Accounting / MCP-Server / A2A-Peer / File-Sync |

### Validation at workspace boot

Adapter binding validated at workspace boot:
- Each binding's Implementation id resolves to known Implementation (per Framework C definition catalog)
- Each binding's class matches Implementation's declared class
- Each binding compatible with active shape's policy bundle (shape may mandate / forbid / restrict adapter classes — see §11)
- Auth credentials present and valid per binding's auth model
- Per-instance config passes Implementation's schema validation

### Re-binding semantics (hot-swap)

Adapter instances re-bindable mid-workspace-life — distinct architectural commitment from substrate's deploy-time-bound. Examples:
- Pioneer swaps gmail-adapter for outlook-adapter without workspace re-deployment
- Firm IT swaps fastbill-adapter for lexware-adapter on tax-software change
- A2A-peer-adapter re-bound when federation membership changes

Workflow_instances using adapter MUST handle re-binding semantics (re-binding events emitted; in-flight operations may need replay or quarantine). Per-impl declares re-binding compatibility.

## 6. Tri-aspect reconciliation

Adapter as tri-aspect Pattern A primitive:

| Aspect | Layer | What it is |
|---|---|---|
| **Surface** (META + per-class) | mechanism (framework-level) | META-Surface conventions + per-integration-class Surface contracts |
| **Implementations** | Framework C scope | Distributable per-impl definitions wrapping native primitives to satisfy a class's Surface + META |
| **Running Instance(s)** | Owner B scope | One-or-more bound to workspace deployment; per-binding instance-id; multiple simultaneous |

### Adapter-internal vs adapter-external state

| State category | Owner | Persistence |
|---|---|---|
| **Auth tokens** | Adapter instance internal | At Owner B with security boundary; encrypted-at-rest per shape policy (practitioner-shape mandates) |
| **Circuit state** (closed/open/half-open) | Adapter instance internal | At Owner B; resets on substrate restart; configurable persistence per impl |
| **Quota counters** | Adapter instance internal | At Owner B; rolling-window per per-class quota model |
| **Threading caches** (email) | Adapter instance internal | At Owner B; per-impl persistence; cleanup on instance shutdown |
| **Per-instance config** | Workspace-owned | At Owner B; declared in workspace.md; mutable via re-binding |
| **Binding declarations** (which adapters bound) | Workspace-owned | At Owner B; declared in workspace.md |

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 "make wrong shapes impossible, not solvable": skill code targeting per-class Surface is portable across Implementations within that class; skill code reaching Implementation-internal primitives is impl-pinned by construction. The same structural-typing-plus-isinstance-check mechanism that protects substrate (per `arch/substrate.md` §6) protects adapter — one principle, two applications.

### Distinct from substrate's tri-aspect

Substrate tri-aspect = singular per workspace (1 substrate Surface satisfied by 1 selected Implementation; 1 running Instance). Adapter tri-aspect = multi-aspect-multi-class:
- N per-class Surfaces (5 currently)
- M Implementations per class in Framework C catalog
- N Running Instances per workspace (one per active binding)

The cardinality variation IS the architectural distinction between substrate Pattern A and adapter Pattern A.

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Adapter is one mechanism category within the framework (parallel to substrate; internal-vs-external axis) |
| `mechanism` | Each per-class Adapter Protocol Surface IS a mechanism (atomic interface contract per class) |
| `Framework C scope` | Adapter Implementations live there as distributable definitions |
| `shape` | Shapes declare adapter compatibility / mandates / restrictions per shape policy bundle (see §14 cross-shape policy variation; per-shape error semantics in §11) |
| `workspace` | Workspace activates one-or-more adapter Instances via `workspace.md` adapter bindings |
| `Owner B scope` | Running adapter Instances bound to workspace deployment; multiple simultaneous; instance-state at Owner B |
| `protocol (architectural)` | Adapter is Pattern A protocol instance; META-PRIMITIVE Protocol describes Pattern A pattern shape |
| **`substrate`** | **Counterpart Pattern A primitive (substrate INTERNAL; adapter EXTERNAL). Adapters run WITHIN substrate's execution. Adapter writes (axis-3 send) request permission via substrate Surface §C. MCP-Server-Adapter composes with substrate Surface §B (MCP registration).** |
| `skill` | Skills invoke adapters at runtime (e.g., `draft-cover-mail` → email-adapter; `verify-citations` → MCP-corpus-adapter); adapter operations are skill-side tool-use invocations |
| `specialist` | Specialists may bundle adapter Implementations as part of their package (per locked specialist entry composes-with) |
| `audit` | Adapter actions emit audit events via MCP audit gate (per-class event-kind catalog; see §8) |
| `event` | Adapter-emitted events first-class in audit-trail (per integration class) |
| `coordination` (CANCELLED) | Cross-adapter coordination subsumed into substrate hooks + event-bus per `docs/decisions/greenfield-rederivation-pause.md` Step 3; per-shape policy configures coordination shape (call-shaped vs event-shaped) via substrate Surface §E |
| `trust` (CANCELLED) | Trust handshake (especially A2A federation) subsumed into authority-binding mechanism per `docs/decisions/greenfield-rederivation-pause.md` Step 3; authority-binding is its own framework primitive (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table); per-shape trust policy declares trust model |
| `time` (CANCELLED) | Time-driven adapter operations (scheduled email send; periodic accounting sync) subsumed into substrate-impl temporal semantics + adapter time-driven operations themselves (no separate Time Pattern A topic) per `docs/decisions/greenfield-rederivation-pause.md` Step 3 |
| `quality-gate` | Quality-gate observability via adapter's audit-event emission + per-class quota/rate-limit metrics; shape policy declares per-shape adapter-action enforcement |
| `category collapse` | Cross-axis force quality-gate guards against; adapter operations participate in axis-3 send-class moments where rubber-stamping risk applies (per L5a hybrid moments line 67); adapter audit-event emission feeds quality-gate's cross-axis collapse-detection |

## 8. Substrate-internal vs skill-side audit emission

**N/A** — per Pattern A template `MAINTENANCE.md:256`, §8 is substrate-specific (substrate registers MCP audit gate; substrate has dual-emission paths — substrate-internal direct + skill-side via MCP gate — to resolve MCP-gate-circularity). Adapter does not register the MCP audit gate; adapter operations are skill-side invocations of adapter primitives. Adapter has no circularity issue and no dual-emission framing to discuss — adapter actions emit audit events via MCP audit gate (skill-side) only.

Per-class audit event-kind catalog (architectural enumeration of adapter-emitted events, skill-side via MCP gate) lives in §11 Per-integration-class error categories alongside the per-class error refinements (both are per-class architectural enumerations).

## 9. Cardinality + lifecycle

Adapter follows multi-instance cardinality (distinct from substrate's singular per workspace) — per Pattern A template `MAINTENANCE.md` §9 common-required section.

### Cardinality

(Per §5 Selection mechanics; restated here for template-fidelity.)

- N adapter Instances active per workspace (bounded by `workspace.md` adapter bindings list; per-shape policy may declare maximum)
- 1 per integration class by default (multi-account mechanics deferred to W4 watch-list resolution per §16)
- M Implementations per class in Framework C catalog
- 5 per-class Surfaces in framework (Email / Accounting / MCP-Server / A2A-Peer / File-Sync; future per ecosystem)

### Lifecycle ownership

- **Creator**: framework-runtime (workspace activation orchestrator) — instantiates one Implementation class per active workspace.md adapter binding at workspace boot
- **Owner**: workspace deployment runtime (Owner B scope membership; per-instance state at Owner B)
- **Destroyer**: framework-runtime at workspace shutdown (per-binding shutdown in reverse declaration order; see §10 phase ordering)

### Mutability

- **Per-instance config** mutable via re-binding mid-workspace-life (hot-swap; distinct architectural commitment from substrate's deploy-time-bound)
- **Auth tokens** persist across substrate restart at Owner B with security boundary (encrypted-at-rest per shape policy — practitioner-shape mandates per defensibility; autonomous-business per business policy; personal-OS per user preference)
- **Adapter-internal state** (circuit state, quota counters, threading caches) per §6 adapter-internal vs adapter-external table; per-impl persistence semantics

### Cross-session persistence

Per-impl persistence semantics declare which adapter-instance-state survives substrate restart vs which resets. Auth tokens persist (encrypted-at-rest per shape); circuit state typically resets on substrate restart unless per-impl declares persistence; quota counters per-class quota-model semantics.

### Adapter Implementation versioning

Semver-like:
- **Major**: breaking changes to per-class Surface satisfaction OR auth model OR config schema
- **Minor**: new capabilities; backward-compatible
- **Patch**: bug fixes; no API changes

Each Implementation declares: version + min-substrate-version + compat-substrate-versions + min-class-Surface-version. Workspace.md adapter binding declares: integration class + Implementation id + min-version constraint + (optional) max-version constraint.

### Hot-swap migration (cross-session)

Per §5 Re-binding semantics, adapter Implementations re-bindable mid-workspace-life. Migration mechanics:
1. New Implementation bound; both old + new active during transition window
2. In-flight operations on old drain to completion (or quarantine if past drain timeout)
3. Workflow_instances using adapter notified; per-impl re-binding compatibility check
4. Old Implementation shut down per §10 lifecycle phase ordering
5. `adapter_rebound` event emitted with old + new identities

Breaking-change migration (major version): explicit migration path declared; workflow_instances may pause until migration complete.

## 10. Lifecycle phase ordering + auth refresh (adapter-conditional)

Per Pattern A template `MAINTENANCE.md:257`: "Boot + shutdown phase ordering" is substrate-specific by template default; adapter has multi-instance lifecycle distinct from substrate's singular boot, plus auth-refresh semantics — both warrant adapter-conditional §10 detail.

### Per-class auth models

| Class | Typical auth model |
|---|---|
| **Email** | OAuth (gmail / outlook); SMTP basic auth (legacy); IMAP password |
| **Accounting** | OAuth (modern APIs); API key (Fastbill / Lexware); shared secret |
| **MCP-Server** | None (in-process); subprocess-trust; HTTP bearer / mTLS |
| **A2A-Peer** | mTLS (federation); shared secret (initial handshake); capability-token |
| **File-Sync** | OAuth (cloud storage); SSH key (git); credential pair |

Each Implementation declares its specific auth model; META-Surface validates the declaration.

### Auth-refresh lifecycle (architectural commitment)

- **Proactive refresh**: refresh tokens at 80% of expiry window (avoid auth-expired-mid-operation)
- **Reactive refresh**: on auth-expired error, refresh + retry once before propagating failure
- **Refresh-failure handling**: emit `adapter_auth_expired` event; circuit-breaker may open; shape policy declares per-shape escalation (practitioner-shape blocks workflow; personal-OS may continue with degraded auth)

### Per-instance boot sequence (per workspace)

1. Workspace boot triggers adapter binding orchestration (per workspace.md adapter bindings list)
2. Per-binding (in declaration order): instantiate Implementation; load auth state; validate config; `from_config(config)` boot
3. Per-binding emit `adapter_started` audit event
4. Per-binding `is_ready` becomes True; workspace's overall boot waits for all adapters ready
5. Adapter operations now accessible to skills via per-class Surface

### Per-instance shutdown sequence (per workspace)

1. Workspace shutdown triggers per-adapter drain
2. Per-binding (in REVERSE declaration order): drain in-flight adapter operations
3. Per-binding stop accepting new operations
4. Per-binding flush adapter-internal state (auth tokens persisted; circuit state captured; threading caches cleaned)
5. Per-binding emit `adapter_stopped` audit event
6. Per-binding shutdown returns

Reverse-order drain ensures adapters with dependencies on each other (e.g., email adapter depending on auth adapter) drain in correct order.

## 11. Per-integration-class error categories + audit event-kind catalog (adapter-conditional)

Per Pattern A template `MAINTENANCE.md:258`: per-protocol error semantics differ; adapter has cross-class architectural categories + per-class refinements + cross-class operational concerns (quota / rate-limit / circuit-breaker) — all warrant adapter-conditional §11 detail. Per-class audit event-kind catalog (skill-side emission via MCP gate; relocated from §8 per template applicability) co-located here as the per-class architectural enumerations parallel structurally.

### Per-class audit event-kind catalog (architectural-level)

Per-integration-class event kinds (architectural enumeration; per-event-shape Pydantic schema → Phase 6):

| Class | Event kinds |
|---|---|
| **Email** | `email_sent` / `email_send_failed` / `email_fetched` / `email_threaded` / `email_delivery_status_received` |
| **Accounting** | `invoice_created` / `invoice_modified` / `invoice_cancelled` / `payment_received` / `payment_matched` / `ledger_synced` / `accounting_op_failed` / `period_lock_encountered` |
| **MCP-Server** | `mcp_tool_invoked` / `mcp_query_executed` / `mcp_capability_negotiated` / `mcp_op_failed` |
| **A2A-Peer** | `a2a_request_sent` / `a2a_response_received` / `a2a_handshake_completed` / `a2a_capability_discovered` / `a2a_peer_unreachable` |
| **File-Sync** | `file_synced` / `file_pushed` / `file_conflict_resolved` / `sync_subscription_started` / `sync_op_failed` |

### Cross-class event kinds (META-Surface-level)

Cross-class architectural events (apply to any adapter class):

- `adapter_started` / `adapter_stopped` (lifecycle)
- `adapter_auth_refreshed` / `adapter_auth_expired` (auth)
- `adapter_circuit_opened` / `adapter_circuit_closed` (circuit-breaker state changes)
- `adapter_rebound` (hot-swap event)
- `adapter_quota_threshold_reached` (quota approaching limit)

### Composition with audit-trail integrity

Per `profiles/L8-auditor-reviewer-posthoc.md` audit-trail integrity must survive intact across deployments / migrations: adapter-emitted events are first-class in audit-trail along with substrate-emitted events (per `arch/substrate.md` §8) and skill-claim events. Auditor reads unified event stream for reasoning chain reconstruction.

### Cross-class architectural categories

| Category | Architectural meaning |
|---|---|
| `AdapterUnreachable` | External system unreachable (network / DNS / target down) |
| `AdapterAuthExpired` | Auth tokens expired; refresh required (or refresh failed) |
| `AdapterAuthFailed` | Auth refresh attempted; permanent failure (e.g., revoked tokens) |
| `AdapterQuotaExceeded` | API quota / rate-limit hit; back-off required |
| `AdapterCircuitBreakerOpen` | Circuit-breaker tripped; recovery probing in progress |
| `AdapterValidationError` | Operation validation failed (impl-side) |
| `AdapterPermissionDenied` | substrate's permission flow returned deny |
| `AdapterOpFailed` | Catch-all impl-native failure not categorized above |

### Per-class refinements

Each class refines architectural categories with class-specific error conditions:

- **Email**: `SMTPAuthFailed` / `SendQuotaExceeded` / `DNSResolutionFailure` / `MessageRejected` (e.g., spam-filter) / `ThreadingConflict`
- **Accounting**: `InvoiceValidationFailure` / `PeriodLocked` / `LedgerConflict` / `TaxFormFieldsMissing`
- **MCP-Server**: `RegistrationConflict` (per substrate Surface §B) / `CapabilityMismatch` / `TransportFailure` / `ToolNotFound`
- **A2A-Peer**: `PeerUnreachable` / `HandshakeFailed` / `CapabilityIncompatible` / `FederationTrustFailure`
- **File-Sync**: `SyncConflict` / `ConflictResolutionFailed` / `RemoteAccessDenied` / `FileNotFound`

### Per-shape error semantics

Shape policy declares per-shape adapter error escalation:
- **practitioner-shape**: fail-closed (defensibility-critical; adapter failures must surface to practitioner; no silent degradation; especially axis-3 send operations where rubber-stamping risk applies)
- **autonomous-business-shape**: fail-open with alert (continuity prioritized; alert on failure; circuit-breaker may auto-recover)
- **personal-OS-shape**: fail-open (lightweight; degradation acceptable; auto-retry with reduced verbosity)

### Quota tracking (architectural commitment)

Adapter instances track quota counters per integration-class quota model:
- **Token-bucket**: requests/sec; refills at fixed rate (typical for API quotas)
- **Sliding window**: requests/minute / hour / day; rolling window
- **Per-resource quotas**: per-message-size / per-record-count / per-attachment-size

Quota configuration per impl + workspace.md binding (workspace may set tighter limits than impl default).

### Rate-limit handling

- **Pre-flight check**: query quota state before operation (where supported)
- **In-flight back-off**: on rate-limit error, exponential back-off + retry
- **Per-shape policy**: practitioner-shape may queue with alert; personal-OS may discard

### Circuit-breaker semantics

- **Closed**: normal operation; failures counted in rolling window
- **Open**: failure threshold exceeded; operations rejected immediately; recovery timer started
- **Half-open**: recovery probe (one operation allowed); success → closed; failure → open with extended timeout
- Per-instance state; shape policy declares per-shape thresholds

Circuit-breaker state-changes emit `adapter_circuit_opened` / `adapter_circuit_closed` audit events.

Per-class Pydantic shape (errors + quota + circuit-breaker) → Phase 6 spec.

## 12. Transport variation + per-tier mapping

**N/A** — per Pattern A template `MAINTENANCE.md:259`, transport-variation §12 is substrate-specific (MCP-transport-variation surfaces at substrate Surface §B). Adapter operates over per-class transports declared per Implementation (e.g., email = SMTP/IMAP/MAPI/HTTP-API per impl; A2A = HTTP/gRPC per impl); transport choice is impl-internal per per-class Surface satisfaction, not a substrate-style transport-tier-mapping framework concern. Per-impl transport declared in §4 per-implementation declarations + §10 per-class auth models.

## 13. Deployment-tier awareness

**N/A** — per Pattern A template `MAINTENANCE.md:260`, tier-awareness §13 is substrate-specific (substrate is tier-uniform Surface with per-tier behavior in impl). Adapter behavior is shape-class-shape (per §14 cross-shape policy variation) + integration-class-shape, NOT tier-shape. Per-impl tier-compatibility declared in §4 (Tier 1 / Tier 2 / Tier 3 compatibility per Implementation), but per-class Surface contracts themselves are tier-uniform.

## 14. Cross-shape policy variation

Per Pattern A template `MAINTENANCE.md` Layer 3 description §14 conditional applicability: applies when protocol behavior is shape-policy-mediated. Adapter behavior is shape-policy-mediated per `profiles/G-composability-gate.md` line 157 cross-shape consumption framing ("practitioner-shape specialist mandates audit-emission used in personal-OS-shape workspace; shape's policy bundle determines if specialist activates fully or partially").

| Shape | Adapter audit emission | Adapter permission flow | Adapter error escalation |
|---|---|---|---|
| **practitioner-shape** | Per-action audit mandatory (defensibility) | HITL on send-class operations (axis-3 critical) | Fail-closed |
| **autonomous-business-shape** | Per-action audit recommended; shape policy may relax | Permission flow per business policy (autonomy-graded) | Fail-open with alert |
| **personal-OS-shape** | Per-action audit optional; user-preference-driven | Light permission flow; user-decision per session | Fail-open |
| **federation-shape** | Per-action audit + cross-node-trust audit | Federation-trust-handshake-bound permission | Fail-closed within node; fail-open across nodes (pending peer recovery) |

Shape policy declares per-shape adapter-action enforcement at workspace boot. Adapter Implementations themselves are shape-neutral; shape policy interprets architectural events + decisions per shape's mandate.

## 15. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening:

- **OAuth flow mechanics**: redirect URI handling; PKCE; refresh-before-expiry timing
- **API key rotation**: graceful key-rollover; multi-key concurrent acceptance; revocation
- **Quota tracking persistence**: counter persistence across substrate restart; reset semantics
- **Circuit-breaker persistence**: state persistence semantics; cold-start behavior
- **Retry policies**: per-class retry strategies; jitter; back-off formulas
- **Failure-mode escalation**: alert routing; user-facing error messages per shape
- **Auth-state encryption-at-rest mechanics**: per-shape encryption requirements; key management
- **Webhook subscription mechanics** (where supported): subscription lifecycle; delivery confirmation
- **Multi-account adapter scenarios**: how single class + multiple accounts (e.g., personal + work email) are bound
- **Cross-adapter operation atomicity**: when a workflow involves multiple adapter writes (invoice + email), atomicity boundaries

Per layered coverage observation in `decision-design-sharpening` v0.6.0: these belong to Phase 6 pre-implementation sharpening, not decision-design phase. ARCH topic explicitly does NOT lock these.

## 16. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| W1 | New per-class Surface emergence | New integration domain ships ecosystem-wide patterns (e.g., CRM as ecosystem-pattern; or document-signing-adapter as locked class given pioneer reality) | Surface-design moment per cascade discipline; new per-class Surface added with DR amendment |
| W2 | Federation-shape mature → A2A-Peer Surface refinement | First federation-shape deployment with concrete cross-node trust model | Re-evaluate A2A-Peer Surface against federation realities; per-shape adapter behavior in §11 may sharpen |
| W3 | Candidate **framework-baseline OR shape-extension** class (e.g., document-signing per pioneer qualified-electronic-signature pattern at L5a line 90; future domain-specific integration boundaries) | Either bundle in specialist OR first instance of candidate per-class Surface surfaces with concrete pattern | Apply §3 framework-baseline-vs-shape-extension discriminator test (universal-applicability across hypothetical legal-practice / research-paper / engineering-doc workspaces? → framework-baseline via framework-mechanism-layer DR amendment; introduced by specific shape's policy bundle as additive layer? → shape-extension via shape-policy-bundle DR per L2 shape-definer profile). Document-signing example: passes universal-applicability test if all three hypothetical workspaces share signing-flow semantics → framework-baseline candidate; fails if practitioner-shape qualified-electronic-signature is shape-specific addition → shape-extension candidate |
| W4 | Multi-account same-class binding patterns | Multi-account workspaces (personal + work email common) surface integration friction | §5 Selection mechanics may need explicit multi-account-per-class semantics; Phase 6 spec impl |
| W5 | Cross-adapter operation atomicity | Workflows involving multiple adapter writes (invoice + email) surface failure-recovery friction | May require coordination protocol amendment OR adapter-side compensation patterns; defer to coordination ARCH topic + cross-decision audit |

## 17. Decision-design provenance

This topic articulates adapter as Pattern A protocol per locked GLOSSARY entry.

**Archive sources** (INPUT only per `disciplines/10-greenfield-evaluation.md` — archive citations name SOURCE where input came from, NOT TEMPLATE where structure transferred; each cited element greenfield-evaluated against current locked vocabulary, not transcribed):

- A2A peer adapter pattern (federation-shape); Tier-3 reframing per pattern-vs-instance discipline (archived A2A + Gemini pattern emulation DR)
- MCP-tool integration; Anthropic plugin manifest patterns (archived plugin-conventions)
- MCP-corpus adapter pattern (LanceDB backend); request/response sync (archived backend-conventions)

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: per-class Adapter Surfaces stay shape-neutral / archetype-neutral / pioneer-neutral. Pioneer reality (PBS-Schulz / outlook + LaTeX + signing) grounds the adapter primitive without leaking pioneer specifics into Surface contracts.

## 18. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.4 | LOCKED |
| Pydantic Protocol contract per per-integration-class Surface | 6 | Mode 3 spec; META-Surface conventions + 5 per-class Pydantic Protocols |
| Concrete adapter Implementations | 6 | Per-class implementations (gmail / outlook / fastbill / Anthropic-MCP / etc.) |
| Pre-implementation operational concerns | 6 | Pre-implementation sharpening at Phase 6 implementation-start |
| Auth + lifecycle persistence mechanics | 6 | Per-shape encryption mechanics; per-impl persistence schemas |
| Multi-account scenarios | 6 (potentially with W4 watch-list trigger earlier) | Architectural shape covers multi-instance; per-class multi-account refinement at Phase 6 |
| New per-class Surface additions (Watch-list W1, W3) | TBD per signal | Cascade discipline: DR amendment + new per-class Surface added |

## 19. Cross-references

- **GLOSSARY**: `adapter` (canonical entry); `framework`, `mechanism`, `Framework C scope`, `Owner B scope`, `workspace`, `protocol (architectural)`, `substrate`, `skill`, `specialist`, `audit`, `event`, `coordination`, `trust`, `time`, `shape`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 "make wrong shapes impossible, not solvable" (per-class Surface typing + isinstance check on Implementation make impl-coupling-by-accident impossible); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (per-class Surface neutrality); `ARCHITECTURE.md` cross-cutting principles "AI as runtime" (Mode-2 Python runtime); `DISCIPLINES.md` Discipline 1 (skill+profile sub-section) (procedural fidelity)
- **Profiles validated**: `G-composability-gate.md` (line 157 cross-shape consumption); `L5a-planner-pbs-schulz.md` (line 90 active adapters; line 66 ad-hoc communication via adapter); `L1-specialist-creator.md` (line 23 specialist DEFINITION boundary; specialist may bundle adapter Implementations); `L4a-workspace-deployer-solo.md` (line 23 adapter configuration: email integration; document-signing; LaTeX compile); `L8-auditor-reviewer-posthoc.md` (line 29 audit-trail integrity across deployments)
- **ARCH topics composing with adapter**: `arch/substrate.md` (Surface §B MCP registration + §C permission flow + §8 dual audit emission); `arch/audit.md` (mechanism class; per-action audit emission via MCP gate skill-side); `arch/sparring.md` (mechanism class peer; sub-mechanisms emit per same skill-side discipline as adapter); `arch/quality-gate.md` (Pattern A protocol; observability via adapter audit + quota metrics); `arch/specialist-skill.md` (Phase 3.5 primitive-cluster; specialists may bundle adapter implementations per `glossary/specialist.md` composes-with adapter row + `arch/specialist-skill.md` §10 bundle composition; specialist's `activation_prereqs.adapter-bindings` declares required adapter bindings; skills invoke adapters at runtime via per-class Surfaces per §2); `arch/practitioner.md` (Phase 3.5 second primitive-cluster; W2 Identity-class adapter Surface candidate per `arch/practitioner.md` §14 watch-list — concrete adapter implementations per Personio / Microsoft Entra / Coolify SSO trigger 6th-class candidate per §3 framework-baseline-vs-shape-extension partition currently 5 classes; archived `governance-and-identity-sourcing.md` decision 2 native-vs-adapter mode pattern grounds practitioner-RECORD source-mechanics composition with adapter §3); `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster; adapters invoked by skills firing within workflow_instance phases per `glossary/skill.md` composes-with adapter row + `arch/workflow-work-unit.md` §4 composition with adapter; adapter Surface composition mediated through containing specialist's bundle per `arch/specialist-skill.md` §4 composition row); `arch/claim-defensibility.md` (Phase 3.5 fourth primitive-cluster LOCKED; adapters invoked by skills firing during claim production per `glossary/skill.md` composes-with adapter row + `arch/claim-defensibility.md` §4 composition table claim row; adapter invocations attributed to claim emission via skill-side MCP audit gate per `arch/substrate.md` §8 dual-emission; defensibility's Cond #2 reconstructible-reasoning-chain captures adapter invocation reasoning chain per `arch/claim-defensibility.md` §18 — every adapter call emitted to audit-trail per per-class event-kind catalog per `arch/adapter.md` §11; cross-deployment claim portability per `arch/claim-defensibility.md` §8 6-row matrix composes with adapter Surface across deployment migrations); `arch/scope-model.md` (Phase 3.5 first cross-cutting integrator LOCKED — adapter Pattern A tri-aspect composes through scope-model per §4 E5 authority-binding placement pattern parallel: adapter Surface (META + per-class) + Implementations (Framework C distributable definitions) + Instance bindings per workspace at Owner B (multiple typically); framework-baseline-vs-shape-extension partition per §3 composes with `arch/scope-model.md` §8 cross-shape policy variation 6-row matrix substrate selection constraints + workspace.md required fields rows; §18 per-primitive composition table adapter row). Cancelled per `docs/decisions/greenfield-rederivation-pause.md` Step 3: `arch/coordination.md` (cross-adapter coordination subsumed into substrate hooks + event-bus) + `arch/trust.md` (federation trust handshake subsumed into authority-binding mechanism) + `arch/time.md` (scheduled adapter operations subsumed into substrate-impl temporal semantics + adapter's own time-driven operations).
- **Phase 6 spec target**: `docs/specs/adapter.md` (META-Surface + 5 per-class Pydantic Protocols + per-impl spec)
- **Archived sources**: `archive/docs/a2a-and-gemini-pattern-emulation.md`, `archive/docs/plugin-conventions.md`, `archive/docs/backend-conventions.md`
