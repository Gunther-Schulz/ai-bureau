# Decision record: Substrate Protocol design (synthesis from R3a-R3d + #18)

> **Amendment session 13 per #22 Sub-DR A (`docs/decisions/terminology-and-specialist-primitive.md`)**:
> SpecialistDescriptor Pydantic Protocol added to common Substrate Protocol
> surface (section: "Supporting Pydantic types"). Substrate
> implementations materialize SpecialistDescriptor per substrate (Anthropic
> plugin manifest in CASDK; module spec in MS AF). Substrate-coupling
> impossible-by-construction per ARCH v0.21.

**Status**: ACCEPTED — session 12 (2026-04-30); 3-round sharpening (full monty + cross-cutting + pre-implementation early-surfacing); decision-design phase rounds 1+2 architecturally lock the design; round 3 marked clearly as pre-implementation surfacing (early); **session 13 amendment adds SpecialistDescriptor per #22 Sub-DR A**; **session 15 amendment** (2026-05-01) re-examines Defers section under v0.33 no-defer principle (most entries reframed as phase routing; W7 valid watch-list). Per v0.33 preliminary-lock principle, this DR remains preliminary-locked; revisable when VISION ideal design demands. Substrate Protocol surface holds under v0.34 entity-md scope model restructure (substrate definitions become Framework C entity-md; substrate selection relocates from backend composition root to workspace.md per Definition vs instance binding pattern — substrate.md schemas in entity-md-spec §4 map cleanly to common Substrate Protocol surface).
**Owner**: ROADMAP commitment #21 (SDK deep-read R3a-R3d synthesis); architectural foundation for #9 implementation
**Related**: `substrate-agentic-framework.md` (#18 — Substrate Protocol pattern introduced); `sdk-deep-read.md` (#21 — origin findings); `in-process-mcp-server.md` (R3a — register_mcp_server method); `eval-framework-adoption.md` (R3b — substrate-agnostic eval); `permission-abstraction.md` (R3c — request_permission method); `subagent-primitives-adoption.md` (R3d — per-substrate extension Protocols pattern + common surface boundary criteria); `terminology-and-specialist-primitive.md` (#22 Sub-DR A — SpecialistDescriptor Protocol amendment)

## Context

R3a-R3d locked individual architectural decisions via #21 SDK deep-read. This DR SYNTHESIZES those into the unified Substrate Protocol design that #9 implementation phase implements.

**Decision-design phase (rounds 1+2)** locks the architectural shape: common Substrate Protocol method set + per-substrate extension Protocols + boundary criteria + cross-cutting concerns (boot/shutdown, error hierarchy, transport, tier-awareness, audit-trail integration).

**Pre-implementation surfacing (round 3, marked separately)** captures operational/runtime concerns that ARE valuable but at WRONG TIME for decision-lock — flagged here as head-start for #9 implementation phase pre-implementation sharpening rounds.

## Common Substrate Protocol surface (decision-design lock — rounds 1+2)

```python
class Substrate(Protocol):
    """Common surface — both Claude Agent SDK + MS AF + hand-rolled
    (Tier 1 fallback) substrates implement these primitives.
    
    Per-substrate value-adds accessed via separate extension Protocols
    (ClaudeAgentSDKExtensions, MSAgentFrameworkExtensions). See
    `subagent-primitives-adoption.md` for boundary criteria."""
    
    # === Bootstrap (round 2 Q1) ===
    
    @classmethod
    async def from_config(cls, config: SubstrateConfig) -> "Substrate":
        """Boot substrate from configuration (office-config.yaml + env)."""
        ...
    
    async def shutdown(self) -> None:
        """Graceful shutdown: stop MCP servers, flush audit-trail, release resources."""
        ...
    
    @property
    def is_ready(self) -> bool: ...
    
    @property
    def deployment_tier(self) -> DeploymentTier: ...  # round 2 Q4
    
    @property
    def protocol_version(self) -> str: ...  # round 3 R11
    
    # === Agent loop entry ===
    
    async def run_agent(
        self,
        prompt: str,
        system_prompt: str | None,
        tools: list[ToolType],
        output_schema: type[BaseModel] | None,
        max_turns: int | None,
        hooks: dict[HookEvent, list[HookCallback]] | None = None,
    ) -> AgentRunResult: ...
    
    # === MCP server registration (R3a) ===
    
    def register_mcp_server(
        self,
        name: str,
        tools: list[MCPTool],
        transport: TransportMode,  # explicit; both modes valid; no default
    ) -> MCPServerHandle: ...
    
    # === MCP discovery (R3a M2) ===
    
    def list_mcp_servers(self) -> list[MCPServerHandle]: ...
    def get_mcp_server(self, name: str) -> MCPServerHandle | None: ...
    def list_available_tools(self) -> dict[str, list[str]]: ...
    
    # === Permission flow (R3c) ===
    
    async def request_permission(
        self,
        decision_kind: PermissionDecisionKind,
        context: PermissionRequestContext,  # discriminated union per kind
    ) -> PermissionDecision: ...
    
    # === Structured output validation (R3b/R3c compose) ===
    
    async def validate_structured_output(
        self,
        schema: type[BaseModel],
        response: str,
        auto_retry: bool = True,
    ) -> ValidationResult: ...
    
    # === Hook registration (common subset) ===
    
    def register_hook(
        self,
        event: HookEvent,  # common subset: PRE_TOOL_USE, POST_TOOL_USE, AGENT_START, AGENT_END
        callback: HookCallback,
    ) -> HookHandle: ...
    
    # === Session/context management (common subset) ===
    
    def get_session_context(self) -> SessionContext: ...
    
    # === Substrate-internal audit emission (round 2 Q5 — circularity resolution) ===
    
    def _emit_audit_event(self, event: AuditEvent) -> None:
        """Internal — substrate uses this for substrate-level events.
        Skills use record_audit_event MCP gate. Both writes converge in audit-trail."""
        ...
```

### Supporting Pydantic types (substrate-agnostic; round 1+2)

```python
class TransportMode(Enum):
    IN_PROCESS = "in_process"
    SUBPROCESS = "subprocess"
    HTTP = "http"  # round 2 Q3 — Tier 2 cloud per #13

class DeploymentTier(Enum):
    TIER_1_LOCAL = "tier_1_local"
    TIER_2_CLOUD = "tier_2_cloud"
    TIER_3_FEDERATED = "tier_3_federated"

class SubstrateConfig(BaseModel):
    deployment_tier: DeploymentTier  # required; from office-config
    mcp_servers: list[MCPServerSpec]  # configured at boot
    # ... other config fields per substrate impl

class HookEvent(Enum):  # Common subset; substrates extend
    PRE_TOOL_USE = "pre_tool_use"
    POST_TOOL_USE = "post_tool_use"
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"

class AgentRunResult(BaseModel):
    status: Literal["completed", "failed", "max_turns_reached"]
    final_output: str | BaseModel
    messages: list[Message]
    total_turns: int
    duration: timedelta
    tokens_used: dict[str, int]

class SessionContext(BaseModel):
    session_id: str
    parent_session_id: str | None
    started_at: datetime
    metadata: dict[str, Any]

class ValidationResult(BaseModel):
    valid: bool
    parsed: BaseModel | None
    error: ValidationError | None
    retry_count: int

class HookHandle(BaseModel):
    event: HookEvent
    handle_id: str
    
    def deregister(self) -> None: ...
```

### SpecialistDescriptor (added session 13 per #22 Sub-DR A)

```python
class SpecialistDescriptor(Protocol):
    """Substrate-neutral specialist description.
    
    Substrate implementations materialize this per-substrate:
    - Claude Agent SDK substrate: SpecialistDescriptor → Anthropic plugin manifest
    - MS Agent Framework substrate: SpecialistDescriptor → module spec
    
    Substrate-coupling impossible-by-construction per ARCH v0.21
    (make-wrong-shapes-impossible). Per #22 Sub-DR A
    `terminology-and-specialist-primitive.md`.
    """
    specialist_id: str
    competence_area: str
    skills: list[SkillDescriptor]
    entities: dict[str, ManagedEntityDescriptor]
    process_entities: list[ProcessEntityDescriptor]
    references: list[ReferenceDescriptor]
    event_subscriptions: list[str]
    substrate_compat: list[SubstrateId]
    classification: Literal["cross-archetype", "domain-anchored"]


class SubstrateId(Enum):
    CLAUDE_AGENT_SDK = "claude_agent_sdk"
    MS_AGENT_FRAMEWORK = "ms_agent_framework"
    HAND_ROLLED_TIER1 = "hand_rolled_tier1"  # fallback per #18 hybrid


# Specialist registration via Substrate Protocol's register_specialist
# (added to common surface; concrete substrates dispatch to native form)
class Substrate(Protocol):  # extends earlier definition
    def register_specialist(
        self,
        descriptor: SpecialistDescriptor,
    ) -> SpecialistHandle: ...
    
    def list_specialists(self) -> list[SpecialistHandle]: ...
    def get_specialist(self, specialist_id: str) -> SpecialistHandle | None: ...
```

### Typed exception hierarchy (round 2 Q2)

```python
class SubstrateError(Exception):
    """Base substrate error."""

class SubstrateUnreachableError(SubstrateError):
    """Substrate or its dependencies (MCP, model API) unreachable.
    Fail-closed per mcp-fallback-policy."""

class PermissionDeniedError(SubstrateError):
    """Permission decision = deny. Caller handles."""

class MCPRegistrationError(SubstrateError):
    """Registration conflict or transport unavailable."""

class AgentRunFailureError(SubstrateError):
    """Agent loop failure; status field on AgentRunResult also captures."""

class StructuredOutputValidationError(SubstrateError):
    """Auto-retry exhausted; output doesn't match schema."""
```

## Per-substrate extension Protocols (R3d P3 + P4)

```python
class ClaudeAgentSDKExtensions(Protocol):
    """Substrate-specific value-adds from Claude Agent SDK.
    Accessed via isinstance check at use site."""
    
    # Subagent + session forking (R3d core)
    async def fork_session(self, branch_name: str) -> ForkSessionResult: ...
    async def spawn_subagent(self, definition: AgentDefinition, ...) -> SubagentHandle: ...
    async def list_subagents(self) -> list[SubagentHandle]: ...
    async def get_subagent_messages(self, subagent_id: str) -> list[Message]: ...
    def list_available_subagents(self) -> list[SubagentDefinition]: ...
    
    # Substrate-specific hook events
    def register_subagent_lifecycle_hook(...) -> HookHandle: ...
    def register_pre_compact_hook(...) -> HookHandle: ...
    
    # Sandbox / Thinking / Channels / Rate limiting
    def configure_sandbox(self, settings: SandboxSettings) -> None: ...
    def configure_thinking(self, config: ThinkingConfig) -> None: ...
    async def subscribe_to_channel(self, channel: str, callback: ChannelCallback) -> ChannelSubscription: ...

class MSAgentFrameworkExtensions(Protocol):
    """Substrate-specific value-adds from MS Agent Framework.
    Accessed via isinstance check at use site."""
    
    # Workflow engine + checkpointing
    def create_workflow_agent(self, ...) -> WorkflowAgent: ...
    def fan_out_workflow(self, agents: list[Agent], ...) -> FanOutEdgeGroup: ...
    def create_checkpoint_storage(self, ...) -> CheckpointStorage: ...
    
    # Evaluation framework (R3b adopts pure Python types directly; this exposes substrate-bound)
    async def evaluate_agent(self, agent: Agent, scenarios: list[EvalItem]) -> EvalResults: ...
    async def evaluate_workflow(self, workflow: WorkflowAgent, scenarios: list[EvalItem]) -> EvalResults: ...
    
    # Compaction strategies (6+)
    def configure_compaction(self, strategy: CompactionStrategy) -> None: ...
    
    # 3-layer middleware (used internally by substrate's R3c request_permission impl)
    def register_agent_middleware(self, middleware: AgentMiddleware) -> None: ...
    def register_function_middleware(self, middleware: FunctionMiddleware) -> None: ...
    def register_chat_middleware(self, middleware: ChatMiddleware) -> None: ...
    
    # History providers
    def configure_history_provider(self, provider: HistoryProvider) -> None: ...
```

PBS code uses isinstance check at use site:

```python
if isinstance(substrate, ClaudeAgentSDKExtensions):
    subagent = await substrate.spawn_subagent(...)
else:
    # fall back to in-orchestrator execution OR raise NotSupportedError
```

## Common surface boundary criteria (R3d P4)

When deciding whether something belongs in common Substrate Protocol surface vs per-substrate extension:

| Decision criterion | Verdict | Examples |
|---|---|---|
| Both substrates support natively with comparable shapes | Common surface | `run_agent`, `register_mcp_server`, `request_permission`, structured output validation |
| One substrate native + other can hand-roll equivalent | Common with substrate-conditional impl | `register_mcp_server` (Claude SDK in-process; MS AF subprocess only with fallback per R3a M3) |
| Only one substrate supports; other can't do equivalent | Per-substrate extension Protocol | Subagent primitives (Claude SDK only); workflow engine (MS AF only) |
| Each substrate has substantially different shape | Per-substrate extension Protocols | Compaction strategies (Claude SDK = single hook; MS AF = 6+ strategies) |
| Future-only feature not yet supported by either | Don't add yet (per sharp defer rule v0.20) | Wait for substrate to ship |

## Boot / shutdown ordering (round 2 Q6)

**Boot sequence**:
1. Load office-config from `~/.config/pbs-bureau/office.yaml` (or per-deployment path)
2. Determine deployment tier from config
3. Instantiate substrate: `substrate = await ChosenSubstrate.from_config(config)`
4. Register configured MCP servers (per office-config.mcp_servers list)
5. Register lifecycle hooks (substrate-level + skill-level)
6. Activate substrate: `await substrate.is_ready` becomes True
7. Begin agent loop: `result = await substrate.run_agent(...)`

**Shutdown sequence**:
1. Wait for in-flight agent runs to complete (or cancel per round 3 R5)
2. Stop accepting new run_agent calls
3. Drain pending permission requests
4. Stop MCP servers (subprocess MCP servers gracefully terminate)
5. Flush audit-trail
6. Release resources
7. `await substrate.shutdown()` returns

## Substrate-internal audit-trail integration (round 2 Q5 — circularity resolution)

Substrate emits AuditEvents (`mcp_server_registration`, `permission_*`, `mcp_server_registration_fallback`). MCP gate `record_audit_event` is registered VIA substrate (potentially circular).

**Resolution**: substrate has DIRECT internal access to audit-trail emission path (NOT through MCP gate). `_emit_audit_event` method handles substrate-level events. MCP gate `record_audit_event` is for SKILL-side emission. Both writes converge in same audit-trail.jsonl; both validate against AuditEvent Pydantic schema; no circularity.

## Concrete substrate impl shape

```python
class ClaudeAgentSDKSubstrate:
    """Implements Substrate + ClaudeAgentSDKExtensions Protocols."""
    
    @classmethod
    async def from_config(cls, config: SubstrateConfig) -> "ClaudeAgentSDKSubstrate":
        instance = cls(config)
        await instance._boot()
        return instance
    
    async def run_agent(self, ...) -> AgentRunResult:
        # Wraps ClaudeSDKClient
        ...
    
    def register_mcp_server(self, name, tools, transport):
        if transport == TransportMode.IN_PROCESS:
            handle = create_sdk_mcp_server(name=name, tools=tools)
        else:  # SUBPROCESS
            handle = self._spawn_subprocess_mcp(name, tools)
        return MCPServerHandle(...)
    
    async def request_permission(self, decision_kind, context):
        # Dispatches to CanUseTool callback + PermissionResult types
        ...
    
    # Extensions methods
    async def fork_session(self, branch_name):
        return await self._sdk_client.fork_session(branch_name)
    
    async def spawn_subagent(self, definition, ...):
        ...

class MSAgentFrameworkSubstrate:
    """Implements Substrate + MSAgentFrameworkExtensions Protocols."""
    
    @classmethod
    async def from_config(cls, config: SubstrateConfig) -> "MSAgentFrameworkSubstrate":
        instance = cls(config)
        await instance._boot()
        return instance
    
    async def run_agent(self, ...) -> AgentRunResult:
        # Wraps AgentExecutor
        ...
    
    def register_mcp_server(self, name, tools, transport):
        if transport == TransportMode.IN_PROCESS:
            self._emit_audit_event(AuditEvent(
                event_kind="mcp_server_registration_fallback",
                details={...},
            ))
            transport = TransportMode.SUBPROCESS
        return MCPServerHandle(transport=transport, fallback_occurred=True, ...)
    
    async def request_permission(self, decision_kind, context):
        # Dispatches to agent middleware + HITL approval (ApprovalRequiredAIFunction)
        ...

class HandRolledSubstrate:
    """Tier 1 fallback; minimal direct implementation."""
    # Implements common Substrate Protocol; no extensions
    ...
```

## Pre-implementation surfacing (round 3 — operational/runtime concerns; early)

**Round 3 was performed at decision-design phase but yielded mostly OPERATIONAL/RUNTIME concerns** that belong in pre-implementation phase (per session-12 user-direction two-phase pattern). Captured here as head-start for #9 implementation pre-implementation sharpening; clearly marked as such.

### MCP server lifecycle proactive events (R1)

Add hook events:

```python
class HookEvent(Enum):
    # ... existing
    MCP_SERVER_STARTED = "mcp_server_started"
    MCP_SERVER_STOPPED = "mcp_server_stopped"
    MCP_SERVER_CRASHED = "mcp_server_crashed"
```

### Substrate-level rate limit handling (R2)

```python
class RateLimitInfo(BaseModel):
    limit_type: Literal["requests_per_minute", "tokens_per_minute", "requests_per_day"]
    remaining: int
    reset_at: datetime
    limit: int

class HookEvent(Enum):
    # ... existing
    RATE_LIMIT_HIT = "rate_limit_hit"

class Substrate(Protocol):
    def get_rate_limit_status(self) -> dict[str, RateLimitInfo]: ...
```

### Session continuation semantics (R3)

```python
async def run_agent(
    self,
    ...
    session_id: str | None = None,  # if provided, continues that session
    continue_session: bool = False,  # explicit opt-in to continuation semantics
) -> AgentRunResult: ...

class SessionContext(BaseModel):
    session_id: str
    parent_session_id: str | None
    started_at: datetime
    last_activity_at: datetime  # NEW
    metadata: dict[str, Any]
    is_active: bool  # NEW
```

### Timeout handling (R4)

```python
async def run_agent(
    self,
    ...
    wall_clock_timeout: timedelta | None = None,
    idle_timeout: timedelta | None = None,
) -> AgentRunResult: ...

class AgentRunResult(BaseModel):
    status: Literal[
        "completed", "failed", "max_turns_reached",
        "wall_clock_timeout", "idle_timeout", "canceled",  # NEW values
    ]
    # ...
```

### Cancellation support (R5)

```python
class Substrate(Protocol):
    async def cancel_agent_run(self, session_id: str, reason: str) -> bool: ...

class HookEvent(Enum):
    AGENT_RUN_CANCELED = "agent_run_canceled"
```

### Per-tenant substrate isolation (R6 — ARCHITECTURAL FINDING flow-back to consider)

**Note: this surfaced in pre-implementation surfacing but IS architecturally significant** — Tier 2+ multi-user behavior decision.

**Decision**: shared substrate per office; tenant-scoped state via session_id + actor_id discrimination.

```python
class SubstrateConfig(BaseModel):
    # ...
    tenant_isolation_mode: Literal["shared_per_office", "per_user_isolated"] = "shared_per_office"

async def run_agent(
    self,
    ...
    actor_id: str,  # required at Tier 2+
    tenant_id: str | None = None,  # for Tier 3 federation
) -> AgentRunResult: ...
```

This is one of the ~10-20% genuine architectural findings that surfaces in pre-implementation rounds; flows back to Substrate Protocol shape.

### Health check (R7)

```python
class Substrate(Protocol):
    async def health_check(self) -> HealthStatus: ...

class HealthStatus(BaseModel):
    overall: Literal["healthy", "degraded", "unhealthy"]
    component_statuses: dict[str, ComponentHealth]
    timestamp: datetime
```

### Streaming + ToolType + HookCallback signatures + subagent identity (R7-R11)

Smaller refinements documented for #9 implementation phase reference. Implementation-time details.

## Composition with R3a/R3b/R3c/R3d

| Decision | Synthesis impact |
|---|---|
| R3a (in-process MCP) | TransportMode + register_mcp_server + discovery API in common surface |
| R3b (eval framework) | Substrate-agnostic; eval primitives are pure Python types; runs on any substrate impl |
| R3c (permission abstraction) | request_permission method + 7 PermissionDecisionKinds in common surface; substrate impl dispatches to native primitives |
| R3d (subagent + extensions) | Per-substrate extension Protocols pattern; common surface boundary criteria; subagent primitives in ClaudeAgentSDKExtensions |

## Implementation phase routing + watch-list (re-examined session 15 under v0.33 no-defer principle)

> **Session 15 amendment**: previously this section was titled "Defers (chronological-valid)" with 7 entries. Under v0.33 no-defer principle, re-examined: most entries are PHASE ROUTING (work scheduled in #9/#11/#13 implementation phases per two-phase pattern), not chronological gaps. Reframed accordingly. One entry (D7) is a real watch-list candidate.

### Phase routing (work scheduled per two-phase pattern + ROADMAP queue)

These are scheduled to specific implementation phases — not chronological gaps. The design is locked here; concrete work happens in the named phase:

| Item | Implementation phase | Notes |
|---|---|---|
| Detailed implementation of common Substrate Protocol methods (was D1) | #9 implementation phase | This DR locks design; #9 implements |
| ClaudeAgentSDKSubstrate full implementation (was D2) | #11 Cowork integration phase | Primary substrate; Cowork is natural deployment target |
| MSAgentFrameworkSubstrate full implementation (was D3) | Per #18 dual-substrate plan; sequenced with #11/#13 | Second backend; Path B frontend awaits W2 below |
| HandRolledSubstrate fallback implementation (was D4) | Tier 1 default; lands with #9 | Minimal impl per #18 hybrid plan |
| Pre-implementation sharpening rounds at #9 implementation start (was D5) | #9 implementation phase | Per session-12 two-phase pattern; surfaces operational details + ~10-20% architectural flow-back |
| Round 3 operational concerns (R1-R11) implementation (was D6) | #9/#11/#13 implementation phases | Pre-implementation sharpening rounds per phase determine what's needed when |

### Watch-list entry (W7)

**W7 (was D7): Per-substrate extension Protocols pattern as full ARCH discipline section** — awaiting **comprehensive doc review during Stage 4 sweep** (per session-15 work plan: Stage 4 reviews ARCH disciplines themselves at major version boundaries per Maintenance discipline rule 6). Resolution: when Stage 4 sweep covers ARCH disciplines, evaluate whether per-substrate extension Protocols pattern deserves dedicated discipline section vs staying as v0.30 changelog reference. Currently mentioned in v0.30 changelog; may warrant promotion to dedicated section.

### Re-examination methodology

D1-D6 fail external-information test (no specific external signal awaited — they're scheduled work) but they're not defers either; they're phase routing. Reframed as routing entries to clarify status.

D7 is the only entry naming a specific external signal (Stage 4 sweep that hasn't run yet); valid watch-list.

Decisions made: substrate-pluggability discipline holds (per v0.30 ARCH); all substrate-design choices locked; Stage 4 sweep evaluates ARCH discipline section structure separately.

## Constraints flowing to downstream commitments

- **→ #9 (implementation phase)**:
  - Common Substrate Protocol surface implementation
  - HandRolledSubstrate impl (Tier 1 default)
  - ClaudeAgentSDKSubstrate impl + ClaudeAgentSDKExtensions
  - Pre-implementation sharpening rounds at #9 start to surface implementation details + flow-back architectural findings
- **→ #11 (Cowork integration)**: ClaudeAgentSDKSubstrate adopted as primary; MCP gates registered IN_PROCESS via Claude Agent SDK
- **→ #13 (deployment flexibility)**:
  - SubstrateConfig.deployment_tier honors per-tier behavior
  - HTTP transport via TransportMode.HTTP for Tier 2 cloud
  - Tenant isolation mode per Tier 2+ deployments
- **→ #18 (substrate decision)**: this DR is the synthesis output of #18's dual-substrate plan; implementation work in #9 implements both substrate impls
- **→ ARCHITECTURE.md**:
  - Substrate Protocol pattern formalized (per #18 v0.30 already)
  - Per-substrate extension Protocols pattern documented (deferred to comprehensive doc review post-#22)
  - Common surface boundary criteria documented (deferred to same)
- **→ pre-implementation phase practice (NEW per session-12 two-phase pattern)**:
  - Run user-triggered sharpening rounds at #9/#11/#13 implementation-start moments
  - Surface operational/runtime/deployment details
  - Flow architectural findings back as DR amendments

## Revisit triggers

- **Claude Agent SDK changes core API** → re-validate ClaudeAgentSDKSubstrate impl + ClaudeAgentSDKExtensions Protocol
- **MS AF changes core API** → re-validate MSAgentFrameworkSubstrate impl + MSAgentFrameworkExtensions Protocol
- **First Tier 2 deployment** → tenant isolation mode + HTTP transport validated against real workload
- **Pre-implementation sharpening rounds at #9 start** → architectural findings flow back as DR amendments per two-phase pattern
- **#22 terminology re-eval completes** → reconsider naming if terminology shifts
- **New substrate candidate emerges** (post-#18 substrate decision) → evaluate against common surface boundary criteria; add as third substrate impl OR document why not

## Files touched (session 12)

- `docs/decisions/substrate-protocol-design.md` — this file (NEW; status ACCEPTED)
- `sdk-deep-read.md` — references this DR as substrate synthesis
- `HANDOFF.md` — updated with two-phase pattern + this DR as decision-design lock
- `memory/feedback_pre_decision_sharpening.md` — refined with two-phase pattern per user direction

## Pattern note (meta)

This DR was synthesized via 3-round sharpening at decision-design phase:
- **Round 1 (AI full monty proactive)**: assembled common surface from R3a-R3d; sketched per-substrate extensions
- **Round 2 (USER-TRIGGERED)**: cross-cutting concerns (boot/shutdown, error hierarchy, HTTP transport, tier-awareness, audit-trail integration circularity, boot ordering)
- **Round 3 (USER-TRIGGERED, broader-surface justification)**: operational/runtime concerns (lifecycle events, rate limit, sessions, timeouts, cancellation, multi-tenant) — captured as PRE-IMPLEMENTATION SURFACING (early); intended for #9 implementation phase pre-implementation sharpening rounds; clearly separated above

Per session-12 two-phase pattern (locked in `memory/feedback_pre_decision_sharpening.md`):
- Decision-design phase: 2-3 rounds (1 initial + 1-2 sharpening); architectural lock
- Pre-implementation phase: additional rounds at implementation-start; operational/runtime details + ~10-20% architectural flow-back

Substrate Protocol synthesis at 3 rounds = upper bound of decision-design phase due to broad architectural surface (R3a+R3b+R3c+R3d assembly).
