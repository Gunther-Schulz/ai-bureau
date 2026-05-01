---
id: ms-agent-framework
label: Microsoft Agent Framework
type: substrate
status: active
last_updated: 2026-05-01

framework_kind: substrate
framework_key: ms-agent-framework

display_name: Microsoft Agent Framework
semver: "0.1.0"

substrate_protocol_compat:
  - from_config
  - shutdown
  - is_ready
  - deployment_tier
  - protocol_version
  - run_agent
  - register_mcp_server
  - list_mcp_servers
  - get_mcp_server
  - list_available_tools
  - request_permission
  - validate_structured_output
  - register_hook
  - get_session_context
  - register_specialist
  - list_specialists
  - get_specialist
  - _emit_audit_event

agent_loop_implementation: extensions.framework.substrates.ms_agent_framework.substrate.MSAgentFrameworkSubstrate

mcp_attach_mechanism: subprocess

runhooks_lifecycle:
  - PRE_TOOL_USE
  - POST_TOOL_USE
  - AGENT_START
  - AGENT_END

shape_compat:
  - practitioner
  - autonomous-business
  - knowledge-graph
  - federation
  - hybrid

boot_characteristics:
  boot_time: medium
  memory_footprint: medium
  runtime_deps:
    - python-3.13+
    - microsoft-agent-framework
  process_model: in-process-with-subprocess-mcp
---

# Microsoft Agent Framework

## What this substrate provides

Microsoft Agent Framework (MS AF) is the **secondary backend substrate** for PBS deployments needing enterprise-grade primitives (workflow engine, checkpointing, hydration) or non-Anthropic ecosystem alignment. Per `substrate-agentic-framework.md` decision (session 12): "Microsoft Agent Framework adopted as second backend (full backend; Path B frontend deferred to consulting signal)".

Functional role: provides the agent loop runtime via AgentExecutor + workflow engine; MCP server attachment via subprocess (no in-process native support — fallback per R3a M3); permission flow via 3-layer middleware + ApprovalRequiredAIFunction; structured output validation; lifecycle hooks; plus enterprise primitives (workflow engine, fan-out, checkpointing, evaluation framework, compaction strategies) accessed via `MSAgentFrameworkExtensions` Protocol.

Architectural framing: MS AF is **Shape B runtime** per `substrate-agentic-framework.md` — Python program IS the runtime; MS AF orchestrates agents directly. Multi-provider-pluggable at model layer (vs CASDK's Claude-only). Used for: (1) Tier 3 enterprise federation deployments where Microsoft / Azure ecosystem alignment matters; (2) consulting clients explicitly requesting non-Anthropic substrate (W5 watch-list); (3) enterprise-scale deployments where workflow engine + checkpointing pay off.

## Substrate Protocol surfaces implemented

Full common Substrate Protocol surface (parity with CASDK at common-surface level per `substrate-protocol-design.md`):

- **Bootstrap**: `from_config(SubstrateConfig)` async classmethod; `shutdown()`; `is_ready` property; `deployment_tier` property; `protocol_version` property
- **Agent loop**: `run_agent(...)` — wraps `AgentExecutor`
- **MCP server registration (R3a)**: `register_mcp_server(name, tools, transport)` — IN_PROCESS request triggers fallback to SUBPROCESS with `mcp_server_registration_fallback` AuditEvent emission (MS AF doesn't natively support in-process MCP servers per R3a code-level analysis); SUBPROCESS supported natively
- **MCP discovery**: `list_mcp_servers`, `get_mcp_server(name)`, `list_available_tools()`
- **Permission flow (R3c)**: `request_permission(decision_kind, context)` — dispatches to agent middleware + HITL approval (ApprovalRequiredAIFunction)
- **Structured output validation**: `validate_structured_output(...)` — uses MS AF's response format + Pydantic validator integration
- **Hook registration (common subset)**: `register_hook(event, callback)` for the 4 common events; mapped to MS AF lifecycle hooks internally
- **Session/context management**: `get_session_context()` — wraps MS AF AgentThread + history provider
- **Specialist registration (per #22 Sub-DR A)**: `register_specialist(SpecialistDescriptor)` materializes specialist as MS AF module spec; `list_specialists`, `get_specialist`
- **Substrate-internal audit emission**: `_emit_audit_event(AuditEvent)` for substrate-level events including the in-process-MCP fallback events

Per-substrate extension Protocols (per `substrate-protocol-design.md` R3d): the `MSAgentFrameworkExtensions` Protocol exposes substrate-specific value-adds — workflow engine + checkpointing (`create_workflow_agent`, `fan_out_workflow`, `create_checkpoint_storage`); evaluation framework (`evaluate_agent`, `evaluate_workflow` against EvalItem scenarios — pure Python types per R3b); compaction strategies (6+ strategies; `configure_compaction`); 3-layer middleware (agent / function / chat); history providers. PBS code accesses these via `isinstance(substrate, MSAgentFrameworkExtensions)` check.

## Operational characteristics

**Boot**: medium. MS AF is heavier than CASDK — workflow engine + middleware stack + checkpointing infrastructure all instantiate at boot. Boot time: ~2-5s depending on configured extensions.

**Memory footprint**: medium. In-process Python with substantial framework objects + per-agent state + workflow engine state. Typical: ~150-300MB resident.

**MCP attach pattern**: **subprocess** (NOT in-process). MS AF doesn't natively support in-process MCP servers; PBS gates attach as subprocess MCP servers spawned at boot. IN_PROCESS transport request triggers fallback with audit emission (per R3a M3). This is a known limitation; documented + accepted (gate functionality identical; just process model differs).

**RunHooks lifecycle**: 4 common-surface events mapped to MS AF lifecycle hooks. MS AF extensions add workflow checkpoint events + middleware-related events (accessed via extension Protocol).

**Session model**: turn-based (compatible with practitioner shape) AND long-running modes (compatible with autonomous-business shape via extension Protocol's workflow + checkpointing primitives). MS AF natively supports both modes — different from CASDK's turn-based-only.

## Compat constraints

`shape_compat`: practitioner / autonomous-business / knowledge-graph / federation / hybrid — broader than CASDK because MS AF supports long-running modes natively.

**Why also practitioner shape**: even though CASDK is the primary substrate for practitioner deployments, MS AF can host practitioner shape too. Use case: consulting client wants Microsoft ecosystem alignment but practitioner-shape work pattern. MS AF backend serves practitioner shape's accountability-bearing requirements (claim-level audit + Option B floor enforcement work via MS AF hooks + middleware) at the cost of subprocess MCP overhead.

**Why excellent for autonomous-business shape**: MS AF's workflow engine + checkpointing + 6+ compaction strategies + fan-out workflows are the natural primitives for autonomous-business shape's long-running operator-supervised AI workforce. When community-built autonomous-business shape extension lands (per shape-extension W4 watch-list resolution), MS AF substrate is the natural pairing.

**Excluded**: personal-OS shape — MS AF's enterprise overhead (workflow engine + middleware + checkpointing) is over-engineering for single-human personal life management. Personal-OS shape pairs with CASDK or lighter substrates.

**Multi-provider posture**: MS AF supports multiple model providers (OpenAI, Azure OpenAI, Mistral, Claude via Anthropic adapter, etc.). This is the key value-add over CASDK for non-Anthropic-ecosystem deployments.

**Tier 3 alignment**: MS AF is the natural Tier 3 enterprise substrate per `a2a-and-gemini-pattern-emulation.md` reframing — Tier 3 = enterprise multi-agent A2A platform; Microsoft / Azure ecosystem fits.

## Migration / version evolution

MS AF is a maintained Microsoft framework; version evolution follows Microsoft's release cadence. PBS substrate version (`semver`) tracks PBS-specific compatibility.

**Revisit triggers** (per substrate-agentic-framework.md):
- MS AF ships breaking API change → re-validate substrate impl + MSAgentFrameworkExtensions Protocol mapping
- MS AF gains in-process MCP server support → upgrade `mcp_attach_mechanism` from subprocess to in-process; remove fallback emission
- New MS AF capability relevant to PBS shapes → evaluate inclusion

**Stability posture**: MS AF is enterprise-grade with longer release cycles than CASDK; API changes typically backward-compatible.

## Known limitations

- **Subprocess MCP only**: no native in-process MCP server support. Fallback to subprocess transport with audit emission. Operationally fine; cosmetically less clean than CASDK's in-process model.
- **Heavier boot**: ~2-5s boot vs CASDK's <1s; matters at Tier 1 solo-user deployments where boot speed visible. At Tier 2/3 cloud deployments where boot is one-time, irrelevant.
- **Cognitive heaviness**: workflow engine + 6+ compaction strategies + 3-layer middleware = more abstractions to learn before being productive. Per `substrate-agentic-framework.md` substrate eval: heaviness scales with deployment tier; appropriate at Tier 2/3 enterprise; over-engineering at Tier 1 solo.
- **Ecosystem alignment**: Microsoft/Azure-leaning. Anthropic-native deployments use CASDK; deployments needing multi-provider model swap or Tier 3 enterprise federation use MS AF.

## Cross-references

- `docs/decisions/substrate-agentic-framework.md` — substrate decision; MS AF as second backend (Path B frontend in W5 watch-list)
- `docs/decisions/substrate-protocol-design.md` — common Substrate Protocol surface + MSAgentFrameworkExtensions
- `docs/decisions/sdk-deep-read.md` — MS AF code-level analysis findings (R3a-R3d)
- `docs/decisions/in-process-mcp-server.md` (R3a M3) — fallback mechanism for non-in-process substrates
- `docs/decisions/permission-abstraction.md` (R3c) — agent middleware + ApprovalRequiredAIFunction integration
- `docs/decisions/eval-framework-adoption.md` (R3b) — MS AF evaluation framework primitives
- `~/dev/reference/agent-framework/` — cloned reference repo for code-level lookup
