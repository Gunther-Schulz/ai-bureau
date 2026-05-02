---
title: Substrate
topic-cluster: Pattern A protocol topics (#1 of 8)
status: drafted (Phase 3.4 Round 2; locked pending optional Round 3 trigger)
---

# Substrate

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the substrate Pattern A protocol. Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the Pydantic Protocol contract (Mode 3). Foundation-up dependency: Pattern A protocol topics 2-7 (adapter / sparring / audit / coordination / trust / time) compose with substrate's Surface contract.

## 1. Topic scope

**Substrate** is the deployment-runtime mechanism — the runtime contract any workspace operates on. Per locked GLOSSARY entry: tri-aspect Pattern A (Protocol surface = mechanism; implementations = Framework C definitions; running instance = workspace-bound at Owner B).

**Cross-axis**: substrate hosts all axes' runtime behavior. Axis 1 (intertwining) realized through substrate's agent-loop primitives. Axis 2 (sparring) realized through substrate's hook + permission mechanisms. Axis 3 (authorship preservation) realized through substrate's session/audit primitives.

**Cardinality**: 1:1 with workspace at framework level. Workspace selects exactly one substrate impl via `workspace.md` `substrate:` field. Multi-environment = N workspaces (each binds one substrate); multi-tenant = substrate-Implementation-level concern (not framework primitive).

**Composition with framework**:
- One mechanism category within `framework`
- Surface IS a `mechanism` (framework-level interface contract)
- Implementations live at `Framework C scope` as distributable definitions
- Running instance bound to `Owner B scope` per workspace deployment
- Pattern A protocol per `protocol (architectural)` GLOSSARY entry

This topic articulates: the Surface contract (architectural-level capability categories), the boundary criteria (Surface vs per-impl extensions), the Implementation aspect (Framework C distributable definitions), Selection mechanics (workspace.md), tri-aspect reconciliation, composition with framework primitives, substrate-internal vs skill-side audit emission, cardinality + lifecycle, and pre-implementation forward-references.

**Phase routing**: Pydantic Protocol contract → Phase 6 spec (Mode 3). Per-substrate concrete implementation work → Phase 6. This topic locks the architectural shape; Phase 6 locks the typed contract + impl.

## 2. Substrate Protocol Surface (architectural-level capability categories)

The Surface is the universal/shape-neutral interface any substrate impl must satisfy. **Articulated here at architectural-conceptual level** — not Pydantic Protocol typing (Phase 6 spec lands typed contract).

Seven capability categories define the Surface:

### A. Agent loop entry

The substrate provides the entry point for starting an agent run. Run takes prompt + system_prompt + tools + structured-output schema + max-turns; returns result with status / final output / messages / tokens-used / duration. Conceptually equivalent to "give the substrate a task to execute and receive structured result."

### B. MCP server registration + discovery

The substrate supports tool registration as MCP server, with multiple transport modes as first-class peers (in-process / subprocess / HTTP — see §5 Transport variation). Discovery API enables runtime introspection: list registered servers, get server by name, list available tools per server.

### C. Permission flow

Runtime authorization mechanism. The substrate exposes `request_permission` accepting typed decision-kind (tool use / write / etc.) + decision-context; returns allow/deny with reason. Skills + specialists invoke permission flow before authority-bound operations; substrate impl dispatches to native primitives (Claude Agent SDK CanUseTool callback; MS AF agent middleware HITL approval).

### D. Structured output validation

Schema-validated agent output with auto-retry semantics. Skill or specialist declares Pydantic schema; substrate forces agent output to satisfy schema; auto-retries with corrective instructions on validation fail.

### E. Hook registration

Common-subset lifecycle event registration. Hook events: PRE/POST tool use, agent start, agent end. Hooks return typed structured output capable of denying or modifying agent behavior. Substrate-extension Protocols expose substrate-specific hook events (subagent lifecycle, pre-compact, etc.) — those are NOT in Surface.

### F. Session/context management

Session identity + parent-session reference + activity timestamps + metadata. Per-substrate persistence semantics (in-memory / file / pluggable history-provider) accessed via Surface-typed session-store handle. Cross-session persistence guarantees defined by substrate impl per Implementation aspect (§4).

### G. Specialist registration

Translates substrate-neutral `SpecialistDescriptor` (per `specialist` GLOSSARY entry's Pattern B DEFINITION aspect) into substrate-native form at boot-time. Per-substrate materialization: Claude Agent SDK substrate registers as Anthropic plugin manifest; MS AF substrate registers as module spec. Substrate-coupling impossible-by-construction — skills + workflow definitions written against `SpecialistDescriptor` work on any substrate impl.

### Explicitly NOT in Surface (per-impl extensions)

The following are per-substrate extension Protocols, NOT Surface:
- Subagent primitives (Claude Agent SDK only)
- Workflow engine + checkpointing (MS AF only)
- Compaction strategies — varies wildly per impl (Claude Agent SDK = single PreCompact hook; MS AF = 6+ strategies)
- Channels / event-driven push (Claude Agent SDK Channels)
- Sandbox / Thinking config (Claude Agent SDK)
- 3-layer middleware (MS AF specific shape)
- Workflow agent fan-out / fan-in / switch-case (MS AF)

These primitives accessible at use site via isinstance check on typed extension Protocol (`ClaudeAgentSDKExtensions`, `MSAgentFrameworkExtensions`). Skill code that uses only Surface methods is substrate-portable; skill code reaching extension Protocols is substrate-pinned by construction.

### Logic placement mode

The Surface contract is articulated here (Mode 4 conceptual; this topic) and encoded structurally in Phase 6 spec (Mode 3 Pydantic Protocol + companion docs). Mode 1 production-runtime AI doesn't load this topic — production AI loads Mode 1 markdown (skills + specialists + workspace.md) above the Surface abstraction. Per `feedback_ai_as_runtime.md`: substrate Surface is Mode-2 Python-side runtime contract; the conceptual articulation here is for framework-developer orientation.

## 3. Common-surface boundary criteria

Decision rule for "in Surface" vs "in per-impl extension" — applied each time a new capability is considered:

| Decision criterion | Verdict | Examples |
|---|---|---|
| Both/all candidate substrates support natively with comparable shape | Surface | run_agent, register_mcp_server, request_permission, structured output validation |
| One substrate native + others can hand-roll equivalent | Surface w/ substrate-conditional impl | register_mcp_server (Claude Agent SDK supports in-process; MS AF subprocess only with audit-emitted fallback) |
| Only one substrate supports natively; others can't equivalent | Per-impl extension Protocol | Subagent primitives (Claude Agent SDK only); workflow engine (MS AF only) |
| Each substrate has substantially different shape | Per-impl extension Protocols | Compaction strategies (Claude Agent SDK = single hook; MS AF = 6+ strategies) |
| Future-only feature not yet supported by either | Don't add yet (per no-defer principle's external-info-test) | Wait for substrate to ship |

The boundary criteria operate at the SURFACE-DESIGN moment (decision-design phase per `decision-design-sharpening`); revisited when new substrate candidate emerges (per Watch-list §12).

## 4. Per-implementation aspect

Implementations live at `Framework C scope` as distributable definitions. Each impl wraps the native primitives of an underlying agentic runtime to satisfy the Surface contract.

### Pattern level

Any agentic-runtime that can satisfy the Surface qualifies. Pattern level is substrate-runtime-shape-neutral.

### Current instance set (CIRCA 2026)

Three concrete substrate Implementations (per `substrate-agentic-framework.md` archive + `substrate-protocol-design.md` archive):

- **Claude Agent SDK** (Anthropic) — primary substrate; Anthropic ecosystem alignment by construction; deepest MCP integration; SKILL.md format native; RunHooks lifecycle; pioneer (PBS-Schulz) deployment per `profiles/L5a-planner-pbs-schulz.md` line 88
- **MS Agent Framework** (Microsoft) — second substrate; multi-provider connectors; 3-layer middleware; workflow engine + checkpointing; Agent Skills uses SKILL.md format
- **Hand-rolled (Python + MCP + Pydantic)** — Tier 1 fallback; minimal direct implementation; baseline for substrate-pluggability validation

### Per-implementation declares

Each Implementation declares:
- **Substrate identity** (id; e.g., `claude_agent_sdk` / `ms_agent_framework` / `hand_rolled_tier1`)
- **Surface satisfaction** (claim + impl mapping each Surface capability category to native primitives)
- **Supported extension Protocols** (typed extension Protocol(s) the impl implements)
- **Configuration schema** (per-impl config — Pydantic; Phase 6)
- **Error mapping** (impl-native errors → common SubstrateError category; see §X Error categories)
- **Deployment-tier compatibility** (Tier 1 local / Tier 2 cloud / Tier 3 federated; see §X Deployment-tier awareness)

### Per-substrate extension Protocols pattern

Substrate-specific value-adds accessed via typed extension Protocols, isinstance-checked at use site:

```
if isinstance(substrate, ClaudeAgentSDKExtensions):
    subagent = await substrate.spawn_subagent(...)
else:
    # fall back to in-orchestrator execution OR raise NotSupportedError
```

This is structural: skill code using only Surface methods is substrate-portable by construction; skill code reaching extension Protocols is substrate-pinned by construction (per `feedback_wrong_shapes_impossible.md` — wrong shapes impossible).

Validated by `profiles/L1-specialist-creator.md` "Cross-substrate compatibility (specialist substrate-agnostic vs substrate-pinned)" + `profiles/G-composability-gate.md` "Cross-substrate composition rules: specialist must be substrate-agnostic OR explicitly substrate-pinned; consumer must verify before install" (lines 155-156).

## 5. Selection mechanics

`workspace.md` `substrate:` field selects exactly one Substrate Implementation by id. The selection is workspace-bound per Owner B scope membership.

### Cardinality

1:1 with workspace at framework level. Multi-environment deployments produce N workspaces (each binds one substrate); multi-tenant within single substrate impl is the impl's own concern (Tier 2+ per-tenant isolation; out of scope for framework primitive).

### Validation at workspace boot

Substrate selection validated at workspace boot:
- Selected substrate id resolves to known Implementation (per Framework C definition catalog)
- Selected substrate compatible with active shape's policy bundle (shape may declare substrate-compatibility constraints)
- Selected substrate compatible with deployment tier (Tier 2 cloud may require HTTP-transport-supporting substrate; etc.)

### Re-binding semantics

Workspace identity persists across substrate migrations (backup→restore on different substrate; substrate API drift triggering re-deployment). The deployment count (per `deployment` GLOSSARY entry — DERIVED workspace-as-bound-runtime) increments; workspace identity stable. Per `profiles/L8-auditor-reviewer-posthoc.md` "Cross-deployment evidence: practitioner moved firms / migrated workspace; L8 evidence must follow" (line 32) — workspace audit-trail must survive substrate migration intact.

Substrate migration mechanics → Phase 6 spec (workspace-portability concern).

## 6. Tri-aspect reconciliation

Substrate as tri-aspect Pattern A primitive (per locked GLOSSARY entry):

| Aspect | Layer | What it is |
|---|---|---|
| **Surface** | mechanism (framework-level) | Atomic interface contract; the seven capability categories articulated in §2 |
| **Implementations** | Framework C scope | Distributable per-substrate-runtime definitions wrapping native primitives to satisfy Surface |
| **Running Instance** | Owner B scope | Bound to workspace deployment at workspace boot; runs while workspace active; released at workspace shutdown |

### Substrate-coupling impossible-by-construction

Per `feedback_wrong_shapes_impossible.md`: Surface-typed skill code structurally cannot reach native primitives without explicit isinstance check on extension Protocol. The architectural commitment makes substrate-coupling-by-accident impossible — wrong shapes don't compile.

This is one of the canonical examples of structural-over-conventional discipline applied at framework primitive design.

### Distinct from specialist's Pattern B manifestation

Specialist Pattern B = bipartite (DEFINITION + INSTANCE). Substrate Pattern A = tri-aspect (Surface + Implementations + running Instance). Specialist has no per-implementation aspect (no multiple implementations of same specialist DEFINITION); substrate does. The two patterns compose orthogonally: specialist DEFINITION at Framework C contains substrate-neutral SpecialistDescriptor (per Surface category G); substrate Implementation at Framework C materializes SpecialistDescriptor per native form at workspace boot.

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Substrate is one mechanism category within the framework |
| `mechanism` | The substrate's Protocol Surface IS a mechanism (framework-level interface contract) |
| `Framework C scope` | Substrate Implementations live there as distributable definitions |
| `shape` | Shapes declare compatibility with substrates (not all shapes work on all substrates); per-shape policy bundles may constrain substrate selection |
| `workspace` | Workspace selects exactly one substrate via `workspace.md`; substrate is what workspace runs ON |
| `Owner B scope` | Running substrate Instance bound to workspace deployment (Owner B) |
| `protocol (architectural)` | Substrate Surface is one of the framework's architectural Protocols (Pattern A) |
| `adapter` | Distinct mechanism category — substrate hosts the runtime; adapter integrates external systems via auth-bound channels. Both Pattern A protocols. |
| `audit` | Substrate emits substrate-internal audit events (§8); skill emits via MCP audit gate; both writes converge in audit-trail |
| `event` | Substrate-emitted events are first-class events in audit-trail (architectural-event kinds: see §8) |
| `session` | Substrate's session/context-management capability (Surface §F) implements `session` primitive's runtime aspect |
| `specialist` | Substrate's specialist-registration capability (Surface §G) translates substrate-neutral SpecialistDescriptor into substrate-native form |
| `coordination` | Coordination Protocol (separate ARCH topic) composes with substrate's actor/session primitives |
| `trust` | Trust Protocol (separate ARCH topic) composes with substrate's permission flow + audit emission |
| `time` | Time Protocol (separate ARCH topic) composes with substrate's session activity timestamps + scheduled-task primitives |
| `quality-gate` | Quality-gate Pattern A protocol (Phase 3.6 ARCH topic) is substrate-agnostic — shape policy declares enforcement; substrate provides observability infrastructure (audit emission + permission flow) |

## 8. Substrate-internal vs skill-level audit emission

### Architectural commitment

Substrate has DIRECT internal access to audit-trail emission path — NOT through MCP audit gate. This resolves a potential circularity: MCP audit gate is itself registered VIA substrate; if substrate-emitted events went through the MCP gate, registration-time events would have no path.

**Resolution**: dual emission paths converging in single audit-trail.

| Emitter | Path | Use case |
|---|---|---|
| Substrate internal | Direct Python emission to audit-trail | Substrate-level events (registration / permission decision / boot complete / shutdown initiated) |
| Skill / specialist | MCP audit gate (`record_audit_event`) | Skill-side events (claim made / sparring round / attestation) |

Both writes go through same Pydantic AuditEvent schema; both land in same `audit-trail.jsonl`; both validate identically. Reader (auditor or quality-gate) sees unified event stream.

### Architectural-event kinds (substrate-emitted)

Substrate emits AuditEvents at architectural moments. Event kinds (architectural-level enumeration; per-event-shape Pydantic schema → Phase 6):

- `mcp_server_registered` — MCP server registration completed (in-process / subprocess / HTTP transport)
- `mcp_server_registration_fallback` — registration transport degraded (e.g., MS AF in-process unavailable; fallback to subprocess; emitted with details)
- `mcp_server_started` / `mcp_server_stopped` / `mcp_server_crashed` — MCP server lifecycle (per pre-implementation surfacing; actual events at Phase 6)
- `permission_decision` — request_permission resolved with allow/deny + reason
- `boot_complete` — substrate is_ready; agent loop accepting runs
- `shutdown_initiated` / `shutdown_complete` — substrate shutdown lifecycle
- `agent_run_started` / `agent_run_completed` / `agent_run_failed` — agent loop lifecycle
- `specialist_registered` — SpecialistDescriptor materialized to substrate-native form

Per `profiles/G-composability-gate.md` line 159 ("Backup-restore-migration round-trip; some events lose substrate-specific metadata"): substrate-emitted events with substrate-specific metadata MUST be tagged so cross-substrate migration can preserve event semantics OR mark substrate-specific-metadata-loss explicitly.

Per `profiles/L8-auditor-reviewer-posthoc.md` line 29 ("Audit-trail integrity must survive intact across deployments / migrations"): substrate-emitted events are first-class; auditor reads them in audit-trail along with skill-side events for reasoning chain reconstruction.

## 9. Cardinality + lifecycle

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Substrate Implementations per workspace | 1 | `workspace.md` `substrate:` field declares; framework-level 1:1 with workspace |
| Running Instance per workspace | 1 | Bound at workspace boot; one process boundary at framework level (multi-tenant isolation = impl-internal) |
| Implementations per Framework C catalog | N | Multiple distributable definitions; current set: Claude Agent SDK / MS AF / hand-rolled |
| Per-substrate extension Protocols per Implementation | N (per-substrate variability) | Each impl declares which extension Protocols it satisfies |

### Lifecycle ownership

- **Creator**: framework-runtime (workspace activation orchestrator) — instantiates Implementation class per `workspace.md` substrate selection at workspace boot
- **Owner**: workspace deployment runtime (Owner B scope membership)
- **Destroyer**: framework-runtime at workspace shutdown (or process termination)

### Mutability

- **Configuration immutable** across single substrate boot (config loaded at boot; immutable until next boot)
- **Runtime state evolves** during substrate lifetime (sessions opened, hooks registered, permissions decided, audit events emitted)
- **Workspace identity stable across substrate migrations** (per `deployment` DERIVED entry — workspace-as-bound-runtime; multiple deployments over time = multiple substrate bindings)

### Cross-session persistence

Per-impl SessionStore Protocol determines cross-session persistence semantics:
- In-memory (Tier 1 dev / debugging) — sessions lost at substrate shutdown
- File-backed (Tier 1 production) — sessions persist via filesystem
- HTTP / cloud-backed (Tier 2+) — sessions persist via cloud storage

Per-impl session-store Protocol exposed via Surface §F session-management category; specific persistence semantics declared per Implementation.

## 10. Boot + shutdown phase ordering (architectural-level)

The substrate has explicit boot phase + shutdown phase with ordered stages. Ordering is architectural commitment — deviations break audit-trail invariants (e.g., flush audit-trail before resource release prevents event loss).

### Boot sequence (architectural ordering)

1. Load substrate configuration (per workspace.md + per-impl config schema)
2. Determine deployment tier from configuration (Tier 1 / Tier 2 / Tier 3)
3. Instantiate substrate Implementation: `substrate = await ChosenSubstrate.from_config(config)`
4. Register configured MCP servers (per config.mcp_servers list)
5. Register lifecycle hooks (substrate-level + skill-level)
6. Register specialists (per active specialists list; substrate-native materialization per Surface §G)
7. Activate substrate: `await substrate.is_ready` becomes True
8. Emit `boot_complete` audit event
9. Begin agent loop: `result = await substrate.run_agent(...)`

### Shutdown sequence (architectural ordering)

1. Emit `shutdown_initiated` audit event
2. Wait for in-flight agent runs to complete OR cancel per cancellation policy (pre-implementation forward-reference)
3. Stop accepting new run_agent calls
4. Drain pending permission requests
5. Stop MCP servers (subprocess MCP servers gracefully terminate)
6. Flush audit-trail (must complete before resource release)
7. Release resources
8. Emit `shutdown_complete` audit event
9. `await substrate.shutdown()` returns

The flush-before-release ordering preserves audit-trail integrity across shutdown — prevents reasoning-chain-reconstruction failures L8 auditor (per `profiles/L8-auditor-reviewer-posthoc.md`) would encounter on workspace shutdown.

## 11. Substrate error categories (architectural-level)

Substrate operations may fail in named architectural categories. Each Implementation maps native errors to common categories.

| Category | Architectural meaning |
|---|---|
| `SubstrateUnreachable` | Substrate or its dependencies (model API, MCP transport) unreachable. Per `mcp-fallback-policy` archive: fail-closed in practitioner-shape (defensibility-critical); shape policy declares per-shape error semantics |
| `PermissionDenied` | Permission decision = deny. Caller handles per-decision-kind |
| `RegistrationConflict` | Registration failure (MCP server name collision, transport unavailable, specialist id collision) |
| `AgentRunFailure` | Agent loop failure; status field on AgentRunResult also captures finer-grain failure mode |
| `StructuredOutputValidation` | Auto-retry exhausted; output doesn't match declared schema |

Per-shape error semantics:
- **practitioner-shape**: fail-closed (defensibility-critical; substrate failures must surface to practitioner; no silent degradation)
- **autonomous-business-shape**: fail-open with alert (continuity prioritized; alert on failure)
- **personal-OS-shape**: fail-open (lightweight; degradation acceptable)

Per-class Pydantic shape → Phase 6 spec (Mode 3).

## 12. Transport variation + per-tier mapping

MCP server registration supports multiple transports as first-class peers (NOT in-process-as-default; transport explicit per registration):

| Transport | Use case | Per-tier mapping |
|---|---|---|
| **In-process** | Same-Python-process MCP server (skills as in-process tools) | Tier 1 local; high-performance dev workflow |
| **Subprocess** | Out-of-process MCP server (subprocess MCP) | Tier 1 local + Tier 2 cloud (when in-process unavailable) |
| **HTTP** | Cross-process / cross-machine MCP server | Tier 2 cloud + Tier 3 federated (cross-deployment communication) |

### Per-impl transport support varies

- Claude Agent SDK substrate: native in-process (`create_sdk_mcp_server`) + subprocess + HTTP
- MS Agent Framework substrate: subprocess + HTTP native; in-process registration falls back to subprocess (emits `mcp_server_registration_fallback` audit event with details)
- Hand-rolled substrate: subprocess + HTTP minimum; in-process per-impl-decision

Transport registration is explicit per call (not implicit-default) — caller declares transport at registration time. Substrate may degrade transport per per-impl support (fallback emits audit event for traceability).

## 13. Deployment-tier awareness

Substrate is aware of which deployment tier it runs at; `SubstrateConfig.deployment_tier` is required field at boot.

### Three tiers

- **Tier 1 (local)**: solo practitioner / development; substrate runs on practitioner's machine; no multi-user concerns
- **Tier 2 (cloud)**: small-firm hosted deployment; multi-user collaboration possible; tenant isolation = substrate-impl concern (e.g., shared substrate per office; tenant-scoped state via session_id + actor_id discrimination)
- **Tier 3 (federated)**: enterprise multi-agent A2A platform; per-tenant isolation strict; substrate determines deployment platform (Claude Agent SDK = separate Tier-3 effort; MS AF = MS AF on Azure AI Foundry / Gemini Enterprise / AWS Bedrock AgentCore as instances)

### Per-tier behavior in impl, not Surface

The Surface contract is tier-neutral — same Surface methods at all tiers. Per-tier behavior variation lives in Implementation:
- Transport selection (Tier 1 in-process default; Tier 2 HTTP; Tier 3 HTTP + federation)
- Multi-tenant isolation mode (Tier 1 single-tenant; Tier 2+ tenant-scoped state)
- Actor-id requirement (Tier 2+ required at agent run; Tier 1 optional)

Substrate selection per workspace.md may be tier-constrained — per-tier-compatibility declared by Impl.

## 14. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced here as forward-reference for Phase 6 pre-implementation sharpening (per `pre-implementation-sharpening` skill). These are explicitly NOT decision-design-phase concerns; the ARCH topic deliberately stops at architectural-conceptual articulation.

Concerns surfaced from archived material (`substrate-protocol-design.md` round 3):

- **Cancellation semantics**: `cancel_agent_run(session_id, reason)`; `agent_run_canceled` hook event
- **Wall-clock + idle timeouts**: per-run timeout configuration; `wall_clock_timeout` / `idle_timeout` status values
- **Rate-limit handling**: `RateLimitInfo` / `RateLimitStatus`; `rate_limit_hit` hook event; per-substrate API quota awareness
- **Health checks**: `health_check()` returning `HealthStatus` (overall + per-component-status)
- **Per-tenant isolation (Tier 2+)**: `tenant_isolation_mode` config field; `actor_id` required at run; `tenant_id` for Tier 3 federation
- **Streaming output semantics**: agent output streaming vs non-streaming
- **HookCallback signatures**: typed hook input/output Pydantic shapes
- **MCP server lifecycle proactive events**: `mcp_server_started` / `mcp_server_stopped` / `mcp_server_crashed`
- **Compaction strategies** (per-impl extensions): summarization / sliding window / token budget composed / tool result compaction / truncation

These are per-implementation operational concerns — locked at Phase 6 implementation-start. ARCH topic explicitly does NOT lock these (per layered coverage observation in `decision-design-sharpening` v0.6.0: R1 = arch decisions; R2 = cross-cutting + schema-detail; R3 = patterns; operational concerns belong to Phase 6 pre-implementation sharpening).

## 15. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| W1 | Substrate-pluggability discipline-section promotion | Phase 3.8 ARCH-discipline coherence-audit at major-boundary (per MAINTENANCE deprecation procedure rule 6) | At Stage 4 sweep evaluating ARCH discipline section structure, evaluate whether per-substrate extension Protocols pattern deserves dedicated discipline section vs staying as Pattern-A-protocol-instance discussion in this topic |
| W2 | New substrate candidate emergence | New substrate framework ships major release affecting ecosystem (e.g., post-2026 lightweight + enterprise entrants) | Re-evaluate against boundary criteria (§3); add as new Implementation OR document why not |
| W3 | SDK API drift triggering Surface revision | Claude Agent SDK / MS AF major-version release affecting Surface composition | Re-validate Surface contract against new SDK shape; update affected Surface category if needed; trigger DR amendment per cascade discipline |
| W4 | Tier 3 substrate-determines-deployment-platform reframing | First Tier 3 enterprise deployment with concrete platform constraints (Gemini Enterprise / Azure AI Foundry / AWS AgentCore) | Per-platform deployment-detail decisions land at deployment time; reframing per pattern-vs-instance discipline (Tier 3 = enterprise multi-agent A2A platform; Gemini Enterprise = canonical exemplar but not only valid instance) |

## 16. Decision-design provenance

This topic articulates substrate as Pattern A protocol per locked GLOSSARY entry. Source materials (archived for Phase 6 implementation reference):

- `archive/docs/decisions/substrate-protocol-design.md` — synthesis of common Substrate Protocol surface (rounds 1+2 architectural lock; round 3 operational/runtime concerns captured as pre-implementation surfacing for Phase 6)
- `archive/docs/decisions/substrate-agentic-framework.md` — substrate evaluation; 4-survivor recommendation (Claude Agent SDK + MS AF + Strands + hand-rolled); pattern-vs-instance reframing of Tier 3
- `archive/docs/decisions/sdk-deep-read.md` — SDK code-level verification; substrate Protocol surface refinement; per-substrate extension Protocols pattern formalization

Per `feedback_pattern_not_instance_defers.md`: substrate Surface stays shape-neutral / archetype-neutral / pioneer-neutral. Pioneer (PBS-Schulz / Claude Agent SDK) reality grounds the substrate primitive (per `profiles/L5a-planner-pbs-schulz.md` line 88, 126) without leaking pioneer specifics into the Surface contract.

## 17. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.4 | LOCKED |
| Pydantic Protocol contract | 6 | Mode 3 spec; Surface category typing; SubstrateError class hierarchy; supporting Pydantic types (TransportMode / DeploymentTier / SubstrateConfig / HookEvent / etc.) |
| Concrete substrate implementations | 6 | ClaudeAgentSDKSubstrate full impl; MSAgentFrameworkSubstrate full backend; HandRolledSubstrate fallback impl |
| Pre-implementation operational concerns (cancellation / timeouts / rate-limit / health / per-tenant / streaming) | 6 | Pre-implementation sharpening at #9 implementation-start; per-implementation-sharpening skill applies |
| Per-impl extension Protocols (ClaudeAgentSDKExtensions / MSAgentFrameworkExtensions) | 6 | Designed alongside Substrate Protocol; each impl satisfies Surface + declares extension Protocols |
| Substrate identity portability across migrations | 6 | Workspace identity portability spec; backup/restore/migration mechanics |

## 18. Cross-references

- **GLOSSARY**: `substrate` (canonical entry); `framework`, `mechanism`, `Framework C scope`, `Owner B scope`, `workspace`, `protocol (architectural)`, `adapter`, `audit`, `event`, `session`, `specialist`, `deployment`
- **Disciplines**: `feedback_wrong_shapes_impossible.md` (substrate-coupling impossible-by-construction); `feedback_pattern_not_instance_defers.md` (pioneer-neutrality of Surface); `feedback_ai_as_runtime.md` (Mode-2 Python runtime); `feedback_skill_files_are_sources.md` (procedural fidelity at session-16 substrate Round 1)
- **Profiles validated**: `G-composability-gate.md` (lines 155-156, 159, 168) + `L5a-planner-pbs-schulz.md` (lines 88, 126, 129) + `L1-specialist-creator.md` (line 27) + `L4a-workspace-deployer-solo.md` (lines 22, 38) + `L8-auditor-reviewer-posthoc.md` (lines 29, 32)
- **ARCH topics composing with substrate**: `arch/adapter.md` (Pattern A protocol; integrates external systems); `arch/audit.md` (substrate-emitted vs skill-emitted dual-emission paths); `arch/coordination.md`, `arch/trust.md`, `arch/time.md` (Pattern A protocols composing with substrate); `arch/quality-gate.md` (substrate-agnostic; observability infrastructure)
- **Phase 6 spec target**: `docs/specs/substrate.md` (Pydantic Protocol + supporting types + per-substrate-impl spec)
- **Archived sources**: `archive/docs/decisions/substrate-protocol-design.md`, `substrate-agentic-framework.md`, `sdk-deep-read.md`
