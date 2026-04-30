# Decision record: Subagent primitives adoption (R3d from #21 SDK deep-read)

**Status**: ACCEPTED — session 12 (2026-04-30); 3-round sharpening (full monty + AI-self round 2 + user-triggered round 3); per-substrate extension Protocols pattern surfaced as NEW architectural pattern
**Owner**: ROADMAP commitment #21 (SDK deep-read R3d); deferred broader terminology question to #22
**Related**: `substrate-agentic-framework.md` (#18 — Substrate Protocol where extension Protocols compose), `sdk-deep-read.md` (#21 — origin findings), `in-process-mcp-server.md` (R3a — TransportMode inheritance), `eval-framework-adoption.md` (R3b — subagent invocation parity scenarios), `permission-abstraction.md` (R3c — subagent permission inheritance + identity routing per P1 + P5), `office-vs-department.md` (#12 — capability composition concept), `office-level-managed-entities.md` (#15 — Actor identity for permission routing)

## Context

Claude Agent SDK provides rich subagent + session-management primitives:
- `SubagentStartHookInput`, `SubagentStopHookInput`
- `get_subagent_messages`, `list_subagents`, `get_subagent_messages_from_store`
- `fork_session`, `ForkSessionResult` (related but distinct from subagents)
- Session-store + mutations + summary primitives
- `AgentDefinition` Pydantic type for declaring agents

Question: do PBS skills naturally map to Claude Agent SDK subagents, or stay distinct concepts?

## Decision

**Hybrid (Option C). PBS skills remain capability-composition primitive (orchestrator routes to skills based on task semantics). Claude Agent SDK subagent primitives adopted opportunistically for execution-context-branching scenarios via per-substrate extension Protocol — NOT part of common Substrate Protocol surface.**

### Why skills ≠ subagents

| Dimension | PBS Skill | Claude Agent SDK Subagent |
|---|---|---|
| Concept | Capability composition (what kind of work) | Execution context (where work runs) |
| Lifetime | Stable; per-skill SKILL.md persists across sessions | Per-invocation; spawned + terminated within agent run |
| State | Shares orchestrator session state | Isolated context; separate state |
| Output visibility | Direct to orchestrator | Requires explicit `get_subagent_messages` |
| Routing | Orchestrator routes based on task semantics | Programmatically spawned by main agent for specific reason |

Conflating: every skill becomes a subagent → loses orchestrator's continuous-state advantage; every subagent IS a skill → subagents become heavy-weight + over-coupled to capability framework.

### Specific scenarios where subagent primitives WIN

| Use case | Pattern | Composes with |
|---|---|---|
| **Explore alternative drafting paths** | Fork session; spawn 2-3 subagents drafting variants in parallel; orchestrator picks best | Sparring discipline (multiple perspectives) |
| **Isolated review with fresh context** | Spawn subagent for `review-draft` with no prior conversation context; avoids reviewer being primed | VISION axis 2 (anti-anchoring sparring purity) |
| **Parallel skill execution** (genuinely independent) | `verify-citations` + `style-check` on same doc | Performance optimization |
| **Long-running speculative work** | Research subagent gathering evidence from references corpus; doesn't block orchestrator main loop | Phase 1 corpus work |
| **Tier 2+ multi-user parallel approval** | Spawn subagents to query each required-approver in parallel; aggregate responses | R3c MultiUserApprovalContext |

## Per-substrate extension Protocols pattern (NEW architectural pattern surfaced by R3d)

R3d introduces extension Protocols distinct from common Substrate Protocol. This is itself a **NEW architectural pattern** worth naming:

> **Per-substrate extension Protocol**: substrate-specific value-adds accessed via separate Protocol typed per substrate. Code uses `isinstance` check at use site to opt into substrate-specific functionality. Falls back to common Substrate Protocol OR raises `NotSupportedError` when extension unavailable.

```python
# Common Substrate Protocol — does NOT include subagent primitives
class Substrate(Protocol):
    async def run_agent(...) -> AgentRunResult: ...
    def register_mcp_server(...) -> MCPServerHandle: ...
    async def request_permission(...) -> PermissionDecision: ...
    # ... other common methods (per #18 Substrate Protocol design)

# Per-substrate extension Protocols — substrate-specific value-adds
class ClaudeAgentSDKExtensions(Protocol):
    async def fork_session(self, ...) -> ForkSessionResult: ...
    async def spawn_subagent(self, definition: AgentDefinition, ...) -> SubagentHandle: ...
    async def list_subagents(self) -> list[SubagentHandle]: ...
    async def get_subagent_messages(self, subagent_id: str) -> list[Message]: ...
    def list_available_subagents(self) -> list[SubagentDefinition]: ...  # discovery API per N6

class MSAgentFrameworkExtensions(Protocol):
    def create_workflow_agent(self, ...) -> WorkflowAgent: ...
    def fan_out_workflow(self, agents: list[Agent], ...) -> FanOutEdgeGroup: ...
    async def evaluate_agent(self, ...) -> EvalResults: ...  # composes with R3b adoption
    # ... other MS AF-specific value-adds
```

PBS code that uses subagent pattern checks substrate type at use site:

```python
if isinstance(substrate, ClaudeAgentSDKExtensions):
    subagent = await substrate.spawn_subagent(...)
    # use subagent
else:
    # fall back to in-orchestrator execution OR raise NotSupportedError
```

Pattern composes with: Substrate Protocol pattern (introduced #18); Make-wrong-shapes-impossible v0.21 (extension Protocol typed = wrong shapes impossible at type-check time); Pattern-vs-instance discipline (don't force common surface for per-substrate-instance features).

**ARCH integration**: full discipline section deferred to comprehensive doc review post-#22; for now documented in this DR with cross-reference forward.

## Common surface boundary criteria (P4 — explicit decision criteria for #9 + future)

When deciding whether something belongs in common Substrate Protocol surface vs per-substrate extension:

| Decision criterion | Verdict | Examples |
|---|---|---|
| Both substrates support it natively with comparable shapes | Common surface | `run_agent`, `register_mcp_server`, `request_permission`, structured output validation |
| One substrate supports natively + other can hand-roll equivalent reasonably | Common surface with substrate-conditional impl | `register_mcp_server` (Claude Agent SDK in-process; MS AF subprocess only with fallback per R3a M3) |
| Only one substrate supports it; other can't do equivalent | Per-substrate extension Protocol | Subagent primitives (Claude Agent SDK only); workflow engine (MS AF only) |
| Each substrate has substantially different shape for similar concept | Per-substrate extension Protocols (not forced common) | Compaction strategies (Claude Agent SDK = single PreCompact hook; MS AF = 6+ strategies) |
| Future-only feature not yet supported by either | Don't add yet (per sharp defer rule v0.20) | Wait for substrate to ship |

## Substrate-specific extensions per substrate (current state)

**ClaudeAgentSDKExtensions Protocol includes**:
- Subagent + session forking primitives (R3d focus)
- Permission model (`CanUseTool`, `PermissionMode`, `PermissionResult`) — used by R3c substrate impl internally
- Sandbox primitives (`SandboxSettings`, `SandboxNetworkConfig`)
- Thinking mode config (`ThinkingConfig` adaptive/disabled/enabled)
- Channels event-driven push (Gap B per #12 + #13)
- Rate limit handling
- In-process MCP via `create_sdk_mcp_server` (R3a uses this for IN_PROCESS transport)

**MSAgentFrameworkExtensions Protocol includes**:
- 3-layer middleware (`AgentMiddleware`, `ChatMiddleware`, `FunctionMiddleware`) — used by R3c substrate impl internally
- Workflow engine + checkpointing (`WorkflowAgent`, `AgentExecutor`, `CheckpointStorage`, edge primitives)
- 6+ compaction strategies + `TokenizerProtocol`
- Evaluation framework (`Evaluator`, `EvalResults`, `evaluate_agent/_workflow`) — used directly by R3b adoption
- History providers (`FileHistoryProvider`, `InMemoryHistoryProvider`)
- Multi-provider connector lazy-loading

## Subagent permission inheritance (P1 — affects R3c)

Hybrid permission inheritance per decision kind:

| PermissionDecisionKind | Inheritance behavior in subagent context | Reason |
|---|---|---|
| `GOVERNANCE_WRITE` | RE-PERMISSION required in subagent | Potentially destructive; subagent context isolation |
| `EXTERNAL_SEND` | RE-PERMISSION required in subagent | External transmission must be re-authorized |
| `LIFECYCLE_TRANSITION` | RE-PERMISSION required in subagent | State machine advances cross subagent boundary |
| `TOOL_EXECUTION` | INHERITED from parent | Sandboxed within subagent's scope; parent already authorized tool universe |
| `FOUR_WAY_DECISION` | INHERITED from parent | Decision menu items scoped to parent's task |
| `SPARRING_BYPASS` | RE-PERMISSION required AT PARENT (not subagent) | Per P2 — bypass authority lives with parent orchestrator |
| `MULTI_USER_APPROVAL` | RE-PERMISSION required in subagent | Multi-user routing must re-evaluate per subagent action |

Implementation: `PermissionDecision.context` extends with `inherited_from_parent: bool` field. Audit-trail records which decisions were inherited vs re-permission.

## Subagent + sparring backstop authority chain (P2 — affects sparring discipline)

If subagent produces output failing sparring schema 3x (per `sparring-output-v1.md` v0.29 bypass-with-reason):

**Authority chain**: subagent → parent orchestrator → user

- Subagent emits `sparring_bypass_proposed` AuditEvent
- Parent orchestrator receives proposal; surfaces to user via R3c `SPARRING_BYPASS` decision
- User approves at orchestrator scope
- Subagent receives approval token; bypass authorized
- Subagent CANNOT self-bypass (architectural integrity per VISION axis 2)

Documented authority chain preserves sparring discipline across execution-context boundary.

## Subagent identity for multi-user permission routing (P5 — affects R3c)

When subagent (spawned by orchestrator acting for user X) makes request requiring multi-user approval:

- Subagent inherits parent orchestrator's actor identity (`current_actor` field in PermissionRequestContext)
- Subagent does NOT have separate user identity
- Required-approvers routing per parent's actor's roles + the action's required-approvers (per existing R3c MultiUserApprovalContext shape)
- Audit-trail clarity via `originating_subagent_id: str | None` field on PermissionRequestContext (NEW per P5)

Documents subagent as "acting on behalf of" parent's user for permission routing purposes.

## Subagent governance for spawning (N1 — Tier 2+; affects R3c)

Spawning subagent consumes resources (separate context window; separate model API costs). At Tier 2+, subagent spawning is governance-gated:

- Per-actor subagent spawn budget (configured via office-config)
- Permission required for non-routine subagent invocations
- Composes with R3c — extends `TOOL_EXECUTION` PermissionDecisionKind with sub-context `subagent_invocation` flag

Avoids enum bloat (no separate `SUBAGENT_SPAWN` kind); reuses existing flow.

## Subagent failure handling (P7)

Substrate Protocol returns typed result for subagent operations:

```python
class SubagentResult(BaseModel):
    status: Literal["completed", "failed", "timed_out"]
    failure_reason: str | None
    messages: list[Message]
    duration: timedelta
    tokens_used: dict[str, int]  # per-model breakdown
```

Orchestrator handles per scenario: retry / propagate to user / use partial output / fall back to in-orchestrator execution.

## Subagent + R3a TransportMode interaction (P8)

Subagent makes its own MCP gate calls; **inherits parent's MCP server registry**. Subagent doesn't register new MCP servers (would be substrate-controlled per security). Same TransportMode applies as parent.

## Subagent definition discovery (N6)

Pre-defined subagents loaded as entities per entity-md spec:

```
extensions/{department}/subagents/{subagent-id}/
  ├── subagent.md (entity-md, type: <dept>.subagent_definition)
  └── definition.py (optional Python AgentDefinition factory)
```

Loaded via #9 entity gate; discovered via `ClaudeAgentSDKExtensions.list_available_subagents()`.

Pre-defined subagents = discoverable + reusable; ad-hoc programmatic spawning still possible.

## Subagent vs forked session distinction (N3)

Per Claude Agent SDK: `fork_session` and subagents are RELATED but DISTINCT primitives.

| Primitive | Use case | API |
|---|---|---|
| **Fork session** | Explore alternatives within same skill ("draft this section under §13a OR §13b") | `await substrate.fork_session(branch_name=...)` |
| **Subagent** | Spawn DIFFERENT capability ("research-subagent gathers refs; main agent drafts") | `await substrate.spawn_subagent(definition=...)` |

Both available in `ClaudeAgentSDKExtensions`. Different patterns, different primitives.

## Subagent internal audit event aggregation (P6)

Subagent's internal AuditEvents reference `parent_session_id` per audit-trail-v2 schema:

```python
audit_event = AuditEvent(
    event_kind="...",
    actor_kind="subagent",
    parent_session_id=parent_orchestrator_session_id,
    originating_subagent_id=subagent_session_id,
    # ...
)
```

Aggregated at `subagent_completed` time + queryable via `query_audit_trail(session_id=parent_session_id, include_subagents=True)`.

## AgentDefinition Pydantic shape (P9)

Use Claude Agent SDK's `AgentDefinition` directly per R3b precedent (don't wrap; extend with PBS-specific subclass if needed). Composes with `ClaudeAgentSDKExtensions` Protocol.

## MS AF parity via workflow primitives (N5 — when needed)

MS AF has `WorkflowAgent` + `AgentExecutor` + edge primitives that achieve similar parallel-execution patterns. If PBS deployment runs on MS AF substrate AND needs subagent-shaped scenarios, MS AF extension Protocol wraps its workflow primitives:

```python
class MSAgentFrameworkExtensions(Protocol):
    def create_workflow_agent(self, ...) -> WorkflowAgent: ...
    def fan_out_workflow(self, agents: list[Agent], ...) -> FanOutEdgeGroup: ...
```

Different shape; same architectural intent (parallel execution + isolated context). Not forced into common surface (per P4 boundary criteria).

## Composition with R3a/R3b/R3c/Substrate Protocol

| R3 / Substrate Protocol | Interaction |
|---|---|
| R3a (in-process MCP) | Subagents inherit parent's MCP server registry; same TransportMode (P8) |
| R3b (eval framework) | Eval scenarios test subagent invocation patterns; `subagent_invocation_parity` scenario type candidate (substrate-conditional via S2 `applicable_substrates`) |
| R3c (permission flow) | Subagent permission inheritance (P1); subagent identity routing (P5); sparring backstop authority chain (P2); subagent spawn governance at Tier 2+ (N1) |
| Common Substrate Protocol | Per-substrate extension Protocols pattern (P3) — subagent primitives in `ClaudeAgentSDKExtensions`, NOT in common surface |
| #9 implementation | Common surface boundary criteria (P4) guides design; per-substrate extension Protocols sketched here |
| #22 (terminology re-eval) | Broader terminology question (does "skill" rename? does "subagent" become PBS concept?) explicitly deferred — orthogonal to R3d adoption decision |

## Phase 0 / Implementation scope

**Phase 0 (in #9 implementation)**:
- Common Substrate Protocol design honors P4 boundary criteria
- Per-substrate extension Protocols sketched: `ClaudeAgentSDKExtensions` + `MSAgentFrameworkExtensions`
- Substrate impls implement common surface + their respective extensions
- PBS code that uses subagents = `isinstance` check pattern documented as convention

**Future scope (deferred)**:
- Detailed scenario list for subagent adoption — emerges per actual workflow scenarios
- Pre-defined subagent definitions (entity-md instances) — first scenario where pre-definition pays off
- MS AF subagent-equivalent extension Protocol design — when MS AF substrate backend lands
- Cross-substrate subagent equivalence enforcement — NOT required (per-substrate extensions intentionally distinct)

## Defers (chronological-valid)

| Defer | Home | Reason |
|---|---|---|
| **D1**: Detailed scenario list for subagent adoption | Per actual scenario emergence (post-#9 implementation) | Use cases surface in real workflows |
| **D2**: Pre-defined subagent definitions (entity-md instances) | First scenario where pre-definition pays off | Premature without specific use case |
| **D3**: MS AF subagent-equivalent extension Protocol design | When MS AF substrate backend lands per #18 | Substrate-specific work |
| **D4**: Broader terminology re-evaluation (skill vs subagent vs Expert) | #22 dedicated session | Pattern-vs-instance discipline applied to terminology — its own work item |
| **D5**: Per-substrate extension Protocols pattern as full ARCH discipline section | Comprehensive doc review post-#22 | ARCH integration deferred until terminology re-eval informs naming |
| **D6**: Subagent vs ad-hoc execution context boundary refinement | Implementation-time when boundary fuzziness surfaces | Architectural detail; resolves with concrete code |
| **D7**: Cross-subagent communication coordination | Not current need; defer until use case emerges | Premature without specific scenario |
| **D8**: Subagent reuse vs respawn semantics | Implementation detail | Per-implementation decision |

## Constraints flowing to downstream commitments

- **→ #9 (Substrate Protocol design)**:
  - Common surface boundary criteria (P4) explicit — guides Substrate Protocol method selection
  - Per-substrate extension Protocols sketched: `ClaudeAgentSDKExtensions` + `MSAgentFrameworkExtensions`
  - PBS code uses `isinstance` check pattern at use site for substrate-specific functionality
- **→ R3c (permission abstraction)**:
  - `PermissionDecision.context` extends with `inherited_from_parent: bool` field (P1)
  - `PermissionRequestContext` extends with `originating_subagent_id: str | None` field (P5)
  - `TOOL_EXECUTION` decision kind extended with `subagent_invocation` sub-context flag (N1)
  - `SPARRING_BYPASS` decisions when subagent requesting → re-evaluated AT PARENT scope (P2)
- **→ R3b (eval framework)**:
  - `subagent_invocation_parity` scenario type candidate (substrate-conditional)
  - Discovery API extends to `list_available_subagents()` for scenario authoring
- **→ R3a (in-process MCP)**:
  - Subagent inherits parent's MCP server registry + TransportMode (P8)
- **→ ARCHITECTURE.md**:
  - Per-substrate extension Protocols pattern (P3) — section addition deferred to comprehensive doc review post-#22
  - Common surface boundary criteria (P4) — reference card row candidate
- **→ #22 (terminology re-eval)**:
  - Subagent terminology + concept positioning explicitly deferred
  - "Expert" composable abstract capability question (per session-12 user direction) orthogonal to R3d
- **→ entity-md spec**:
  - New entity type candidate: `<dept>.subagent_definition` (when pre-defined subagents land)
- **→ #6 audit-trail v2 retrofit**:
  - Event kinds: `subagent_started`, `subagent_completed`, `sparring_bypass_proposed` (subagent emits; parent decides)
  - `actor_kind=subagent` value
  - `parent_session_id` + `originating_subagent_id` fields

## Revisit triggers

- **First subagent adoption scenario in implementation** → validate decision criteria against real workflow
- **MS AF substrate backend lands** → MS AF extensions Protocol design (workflow-engine + AgentExecutor wrapping)
- **#22 terminology re-eval completes** → revisit subagent terminology + concept positioning
- **Per-substrate extension Protocols pattern usage accumulates** → formalize as full ARCH discipline section
- **Cross-substrate subagent-equivalent scenario surfaces** → re-evaluate forced-common-surface vs per-substrate-extension boundary

## Files touched

- `docs/decisions/subagent-primitives-adoption.md` — this file (NEW; status ACCEPTED)
- `docs/decisions/permission-abstraction.md` — amended with P1 + P5 fields + P2 note
- `docs/decisions/sdk-deep-read.md` — Recommendations section references this DR
- `ARCHITECTURE.md` — Per-substrate extension Protocols pattern section (deferred to comprehensive doc review post-#22)
- `audit-trail-v2.md` — `actor_kind=subagent` + `parent_session_id` + `originating_subagent_id` + new event kinds (with #6 retrofit)
