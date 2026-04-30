# Decision record: In-process MCP server adoption (R3a from #21 SDK deep-read)

**Status**: ACCEPTED — session 12 (2026-04-30); 2-round sharpening (full monty + first-class peers reframing)
**Owner**: ROADMAP commitment #21 (SDK deep-read R3a); composes with #18 substrate decision; lands at #11 Cowork integration
**Related**: `substrate-agentic-framework.md` (#18 — Substrate Protocol where this method lives), `sdk-deep-read.md` (#21 — origin findings), `mcp-fallback-policy.md` (fail-closed corollary applies), `permission-abstraction.md` (R3c — permission flow fires before tool dispatch), `eval-framework-adoption.md` (R3b — `mcp_gate_parity` scenario type validates both transport modes)

## Context

Claude Agent SDK provides `create_sdk_mcp_server(name, tools=[...])` — register Python functions decorated with `@tool` as an MCP server **that runs in the same Python process as the agent**. No subprocess. No IPC overhead.

Currently planned PBS architecture: `pbs_mcp` = separate Python process; Claude Code invokes via stdio MCP transport.

The R3a question: do we adopt in-process pattern as PRIMARY for Claude Agent SDK substrate?

## Decision

**Adopt in-process MCP via Claude Agent SDK for PBS-native gates as PRIMARY. Both `IN_PROCESS` + `SUBPROCESS` are first-class architectural peer choices via `TransportMode` enum.**

### Substrate Protocol method

```python
class TransportMode(Enum):
    IN_PROCESS = "in_process"
    SUBPROCESS = "subprocess"

class Substrate(Protocol):
    def register_mcp_server(
        self,
        name: str,
        tools: list[MCPTool],
        transport: TransportMode,  # explicit; both modes equally valid; no default
    ) -> MCPServerHandle: ...
```

Per-substrate impl:

| Substrate | IN_PROCESS | SUBPROCESS |
|---|---|---|
| Claude Agent SDK | ✅ Native (`create_sdk_mcp_server`) | ✅ Native (subprocess MCP) |
| MS AF | ❌ Not supported (graceful fallback to SUBPROCESS + audit-trail emit) | ✅ Native (`MCPStdioTool`/`MCPStreamableHTTPTool`/`MCPWebsocketTool`) |
| Hand-rolled (Tier 1 fallback) | Direct registration | Subprocess via stdio MCP |

### Decision principle for caller (documented convention; NOT enforced)

| Gate type | TransportMode | Reason |
|---|---|---|
| PBS-native gates (read_entity, audit, state) | `IN_PROCESS` | Shared state with agent; lightweight; fast invocation |
| Adapter gates (Lexware, Personio, calendar) | `SUBPROCESS` | External by nature (third-party SaaS connectors) |
| Heavy-compute gates (large RAG operations) | `SUBPROCESS` | Isolation; doesn't block agent process |
| Marketplace gates (community-published) | `SUBPROCESS` | Isolation; independent lifecycle |
| Sandbox-required gates (untrusted code) | `SUBPROCESS` | Security boundary |

## Why this architecture (not "escape hatch")

Original draft framed subprocess as "escape hatch from in-process default." Sharpened in round 2 to **first-class architectural peers**. Reasons:

- Both modes are valid architectural choices; subprocess is the historical/default MCP pattern
- "Escape hatch" framing implies subprocess is exceptional — incorrect for adapter gates which are subprocess by nature
- Explicit choice at registration call = architectural intent visible in code
- Documentation tone shifts from defensive to peer choice

### Real wins (not raw performance)

| Win | Why |
|---|---|
| Operational simplicity | No subprocess management; single Python process to deploy + observe (for IN_PROCESS gates) |
| Debugging | Direct stack traces across gate boundary (IN_PROCESS); same process state visible to debugger |
| Type safety preserved | Direct Python function calls (IN_PROCESS) preserve full typing; no JSON serialization roundtrip |
| Audit-trail consistency | In-process gates emit AuditEvents to same Python state; no cross-process synchronization |

(Performance is a side-benefit, not the headline. IPC overhead is negligible at PBS interactive tool-call rates.)

## Module layout decision

Keep `backend/mcp-server/src/pbs_mcp/` structure. Within:

- Gate functions become importable: `from pbs_mcp.gates import read_entity, write_entity, ...`
- Standalone server entry point (`pbs_mcp.__main__`) STAYS — used for SUBPROCESS registration mode
- Module name unchanged (`pbs_mcp` not renamed) — preserves existing references; gate functions are the contract surface, server wrapper is one of two registration paths

## CI parity testing

Parity test suite registers gates in BOTH modes (IN_PROCESS + SUBPROCESS); runs identical test cases through both; expects identical results. Catches:
- Substrate-divergence bugs (gate works in-process but not subprocess or vice versa)
- Serialization corner cases (some Python types may not roundtrip cleanly through stdio MCP JSON)
- Error format compatibility

Implemented as scenario type `mcp_gate_parity` in R3b eval framework (per cross-reference).

## Composition with existing architecture

| Concern | R3a interaction |
|---|---|
| Substrate Protocol design (#9) | This method definition lands there as architectural foundation |
| #11 Cowork integration | Cowork plugin = single Python module with embedded MCP gates (no subprocess to manage) |
| #13 deployment flexibility | TransportMode × tier matrix; mixed-mode supported per substrate |
| R3b eval framework | `mcp_gate_parity` scenario type validates both transport modes |
| R3c permission flow | Permission fires BEFORE tool dispatch; orthogonal concerns |
| `mcp-fallback-policy.md` (fail-closed corollary) | Both transport modes apply fail-closed; substrate unreachable = surface + stop |
| `audit-trail-v2.md` | In-process gates emit AuditEvents directly to same Python state |

## Defers (chronological-valid)

| Defer | Home | Reason |
|---|---|---|
| **D1**: Detailed `pbs_mcp` module reorganization | #11 implementation phase | Reorganization needs concrete consumer (Cowork integration) to test against |
| **D2**: Substrate-specific extension Protocols (Claude-Agent-SDK-only primitives like `create_sdk_mcp_server`) | #9 Substrate Protocol design | Substrate-specific extensions designed alongside common Protocol |
| **D3**: Tool function signature compatibility verification | Implementation time | Verifies at code-write moment; not architectural |

## Constraints flowing to downstream commitments

- **→ #9 (Substrate Protocol design)**: `register_mcp_server(name, tools, transport)` method definition + `TransportMode` enum + `MCPServerHandle` typed return
- **→ #11 (Cowork integration)**: Plugin = single Python module with embedded MCP gates registered as IN_PROCESS via Claude Agent SDK; no subprocess management
- **→ #13 (deployment flexibility)**: TransportMode × tier matrix per gate; documented per-deployment configuration patterns
- **→ R3b (eval framework)**: `mcp_gate_parity` scenario type added; CI runs identical tests in both modes
- **→ R3c (permission flow)**: `ToolExecutionContext.transport_mode` field references TransportMode for permission decision context
- **→ External integrations (adapters)**: always SUBPROCESS regardless of substrate (external by nature)

## Revisit triggers

- **Claude Agent SDK changes in-process MCP API** → re-validate Substrate impl
- **MS AF adds in-process MCP support** → reconsider parity assumption (currently MS AF is SUBPROCESS-only)
- **Performance friction in production** → revisit assumption that subprocess overhead is negligible at PBS rates
- **First mixed-mode deployment use case** (e.g., heavy-compute gate isolation) → validate TransportPreference enum shape with real workload

## Files touched

- `docs/decisions/in-process-mcp-server.md` — this file (NEW; status ACCEPTED)
- `sdk-deep-read.md` — updated to reference this DR as detailed implementation
