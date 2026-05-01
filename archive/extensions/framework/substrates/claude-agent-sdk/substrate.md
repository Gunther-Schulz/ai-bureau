---
id: claude-agent-sdk
label: Claude Agent SDK
type: substrate
status: active
last_updated: 2026-05-01

framework_kind: substrate
framework_key: claude-agent-sdk

display_name: Claude Agent SDK
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

agent_loop_implementation: extensions.framework.substrates.claude_agent_sdk.substrate.ClaudeAgentSDKSubstrate

mcp_attach_mechanism: in-process

runhooks_lifecycle:
  - PRE_TOOL_USE
  - POST_TOOL_USE
  - AGENT_START
  - AGENT_END

shape_compat:
  - practitioner
  - personal-OS
  - knowledge-graph
  - federation
  - hybrid

boot_characteristics:
  boot_time: light
  memory_footprint: low
  runtime_deps:
    - python-3.13+
    - claude-agent-sdk
  process_model: in-process
---

# Claude Agent SDK

## What this substrate provides

Claude Agent SDK (CASDK) is the **primary substrate** for PBS-marketed practitioner-shape deployments. Per `substrate-agentic-framework.md` decision (session 12): "Claude Agent SDK adopted as primary substrate (full backend + frontend = Cowork plugin via #11)".

Functional role: provides the agent loop runtime (the engine that takes prompts + tools + system prompts and produces structured output), MCP server attachment (in-process is the native + load-bearing capability), permission flow, structured output validation, RunHooks lifecycle, and session forking + subagent primitives (per the ClaudeAgentSDKExtensions Protocol).

Architectural framing: CASDK is **Shape A runtime** per `substrate-agentic-framework.md` — Claude IS the runtime via Claude Code orchestration. PBS code provides the markdown-body content + Pydantic schemas + MCP gates; CASDK fuses them at runtime. This is the canonical AI-as-runtime hybrid-shape application (per ARCH discipline v0.16).

## Substrate Protocol surfaces implemented

Full common Substrate Protocol surface (per `substrate-protocol-design.md` rounds 1+2 architectural lock):

- **Bootstrap**: `from_config(SubstrateConfig)` async classmethod; `shutdown()`; `is_ready` property; `deployment_tier` property; `protocol_version` property
- **Agent loop**: `run_agent(prompt, system_prompt, tools, output_schema, max_turns, hooks)` — wraps `ClaudeSDKClient` agent loop
- **MCP server registration (R3a)**: `register_mcp_server(name, tools, transport)` — supports IN_PROCESS via `create_sdk_mcp_server` (the load-bearing native capability) AND SUBPROCESS for compatibility
- **MCP discovery**: `list_mcp_servers`, `get_mcp_server(name)`, `list_available_tools()`
- **Permission flow (R3c)**: `request_permission(decision_kind, context)` — dispatches to CanUseTool callback + PermissionResult types
- **Structured output validation (R3b/R3c compose)**: `validate_structured_output(schema, response, auto_retry)` — uses CASDK's output_schema + auto-retry semantics
- **Hook registration (common subset)**: `register_hook(event, callback)` for PRE_TOOL_USE / POST_TOOL_USE / AGENT_START / AGENT_END
- **Session/context management**: `get_session_context()` — wraps CASDK session
- **Specialist registration (per #22 Sub-DR A)**: `register_specialist(SpecialistDescriptor)` materializes specialist as Anthropic plugin manifest; `list_specialists`, `get_specialist(specialist_id)`
- **Substrate-internal audit emission (round 2 Q5)**: `_emit_audit_event(AuditEvent)` for substrate-level events (mcp_server_registration, permission_*, etc.)

Per-substrate extension Protocols (per `substrate-protocol-design.md` R3d): the `ClaudeAgentSDKExtensions` Protocol exposes substrate-specific value-adds — subagent + session forking primitives (`fork_session`, `spawn_subagent`, `list_subagents`), substrate-specific hook events (`register_subagent_lifecycle_hook`, `register_pre_compact_hook`), sandbox + thinking + channels + rate limiting configuration. PBS code accesses these via `isinstance(substrate, ClaudeAgentSDKExtensions)` check at use site.

## Operational characteristics

**Boot**: light. CASDK is a Python library; no separate process to spawn. Boot time = Python module import + `ClaudeSDKClient` instantiation + initial config load. Typical: <1s.

**Memory footprint**: low. In-process (no subprocess overhead). Memory = Python process + SDK objects + per-session state. Typical: ~50-100MB resident.

**MCP attach pattern**: **in-process** (the load-bearing differentiator). CASDK natively supports `create_sdk_mcp_server` for in-process MCP server registration — no subprocess spawn, no IPC overhead, no startup latency. PBS gates (record_audit_event, get_project_state, etc.) attach in-process. This is per R3a in-process MCP server decision.

Subprocess MCP attachment also supported (for legacy / external MCP servers); transport selected per `register_mcp_server(transport=TransportMode.IN_PROCESS | SUBPROCESS)`.

**RunHooks lifecycle**: PRE_TOOL_USE / POST_TOOL_USE / AGENT_START / AGENT_END are the common-surface events. CASDK extensions add subagent lifecycle events + pre_compact hook (accessed via ClaudeAgentSDKExtensions Protocol).

**Session model**: turn-based (Claude responds per user turn). Maps cleanly to practitioner shape's `time_model: turn-based`. Long-running mode (autonomous-business shape) requires substrate adapter implementation per shape-extension W4 watch-list (concrete adapter awaits first autonomous-business shape extension built; CASDK's session forking primitives may serve as building block).

## Compat constraints

`shape_compat`: practitioner / personal-OS / knowledge-graph / federation / hybrid — most workspace shapes work natively on CASDK.

**Excluded**: autonomous-business shape (requires long-running runtime adapter per shape-extension W4 watch-list). When that watch-list resolves with a concrete autonomous-business shape extension built, evaluate whether CASDK's session forking primitives are sufficient or whether a separate long-running adapter is needed.

**Anthropic ecosystem alignment**: CASDK is the natural choice for PBS-marketed deployments because:
- PBS pioneer reference (PBS-Schulz) is built on Claude Code orchestration → CASDK is Claude Code's native SDK
- Cowork plugin (per #11) ships on Anthropic ecosystem → CASDK is the substrate
- Tier 1 + Tier 2 deployments primarily Anthropic-ecosystem (vs Tier 3 federation which uses Microsoft / AWS / Gemini per `a2a-and-gemini-pattern-emulation.md`)

**Lock-in posture**: CASDK adoption locks Claude as the model. This is consistent with already-locked Tier 1-2 architecture (per substrate-agentic-framework.md "Lock-in to Anthropic at model layer" counter-argument). Tier 3 = different archetype = different substrate.

## Migration / version evolution

CASDK is a maintained Anthropic SDK; version evolution follows Anthropic's release cadence. PBS substrate version (this Layer 1 `semver`) tracks PBS-specific compatibility — bumps when PBS substrate adapter needs updating to match new SDK versions.

**Revisit triggers** (per substrate-agentic-framework.md):
- Claude Agent SDK ships breaking API change → re-validate substrate impl + ClaudeAgentSDKExtensions Protocol mapping
- New CASDK capability emerges (e.g., long-running mode native support) → evaluate inclusion in shape_compat or extension Protocol

**Stability posture**: CASDK is in active development; major API changes possible. PBS substrate adapter buffers PBS code from direct CASDK API exposure.

## Known limitations

- **Single-model lock**: CASDK is Claude-only. Multi-provider model swap requires switching to MS Agent Framework substrate (or a future provider-neutral substrate per substrate-pluggability discipline).
- **Subagent primitives in extension Protocol only**: subagent + session forking are CASDK-only capabilities; not in common Substrate Protocol surface. Code using these is CASDK-specific (per `subagent-primitives-adoption.md` R3d boundary criteria).
- **Long-running mode**: not supported natively in v1; addressed via substrate adapter when first concrete need surfaces (per shape-extension W4 watch-list).
- **Enterprise primitives** (workflow engine, hydration, checkpointing): not supported natively; MS Agent Framework substrate provides these for enterprise-scale deployments.

## Cross-references

- `docs/decisions/substrate-agentic-framework.md` — substrate decision; CASDK as primary
- `docs/decisions/substrate-protocol-design.md` — common Substrate Protocol surface + ClaudeAgentSDKExtensions
- `docs/decisions/sdk-deep-read.md` — CASDK code-level analysis findings (R3a-R3d)
- `docs/decisions/in-process-mcp-server.md` (R3a) — in-process MCP transport decision
- `docs/decisions/permission-abstraction.md` (R3c) — permission flow design
- `docs/decisions/subagent-primitives-adoption.md` (R3d) — extension Protocol boundary criteria
- `~/dev/reference/claude-agent-sdk/` — cloned reference repo for code-level lookup
