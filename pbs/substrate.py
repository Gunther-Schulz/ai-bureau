"""Substrate Protocol Surface — Pattern A protocol per `arch/substrate.md`.

Per `arch/substrate.md` §1: the deployment-runtime mechanism — runtime
contract any workspace operates on. Tri-aspect Pattern A (Surface =
mechanism; Implementations = Framework C definitions; Running Instance =
workspace-bound at Owner B). 1:1 with workspace at framework level.

Surface (§2; 7 capability categories):
- §A Agent loop entry → `run_agent()`
- §B MCP server registration + discovery → `register_mcp_server()` +
  `discover_mcp_servers()` + `get_mcp_server()` + `list_tools()`
- §C Permission flow → `request_permission()`
- §D Structured output validation → integrated into `run_agent()` via
  `output_schema` parameter (auto-retry on validation fail)
- §E Hook registration + event-bus → `register_hook()` + event-bus
  internal dispatch (subsumes prior `coordination` Pattern A topic per
  `docs/decisions/greenfield-rederivation-pause.md` Step 3)
- §F Session/context management → `get_session_store()` returning
  per-impl SessionStore Protocol
- §G Specialist registration → `register_specialist()` taking
  substrate-neutral SpecialistDescriptor

Per §3: substrate has a single unified Surface (no multi-class boundary
criteria; per Pattern A template §3 N/A for substrate).

Per §14: substrate Surface is shape-uniform (no per-shape behavioral
variation); shape policy interprets substrate-emitted events at shape
primitive's domain, not at substrate's. (Pattern A template §14 N/A
documented in arch.)

Per `docs/decisions/substrate-hand-rolled-drop.md`: current Implementation
set = {Claude Agent SDK, MS Agent Framework} (Pattern A ≥2 discriminator
preserved). Hand-rolled dropped per thin-slice scope-narrowing.

Phase 6.1 reference impl: `pbs/impls/claude_agent_sdk_substrate.py`
(forthcoming) satisfies this Protocol via Anthropic Claude Agent SDK
native primitives.
"""

from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from pbs.manifests.specialist import SpecialistDescriptor
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Supporting enums (§12 transport variation; §13 deployment-tier awareness)
# ---------------------------------------------------------------------------


class TransportMode(StrEnum):
    """MCP server transport per `arch/substrate.md` §12.

    Three transports as first-class peers (NOT in-process-as-default;
    transport explicit per registration). Per-impl support varies (§12
    per-impl transport support varies sub-section); registration may
    degrade per impl support (`mcp_server_registration_fallback` event
    emits with details).
    """

    IN_PROCESS = "in_process"
    SUBPROCESS = "subprocess"
    HTTP = "http"


class DeploymentTier(StrEnum):
    """Deployment tier per `arch/substrate.md` §13.

    Per-tier behavior variation lives in Implementation, NOT Surface
    (Surface is tier-neutral). Substrate selection per `workspace.md` may
    be tier-constrained per-tier-compatibility declared by Impl.
    """

    TIER_1 = "tier_1"  # local; solo practitioner / development
    TIER_2 = "tier_2"  # cloud; small-firm hosted; multi-user collaboration
    TIER_3 = "tier_3"  # federated; enterprise multi-agent A2A platform


class HookEventKind(StrEnum):
    """Common-subset hook event kinds per `arch/substrate.md` §2.E.

    Per-substrate extension Protocols (Claude Agent SDK / MS AF) may
    expose substrate-specific hook events (subagent lifecycle, pre-compact,
    etc.) — those are NOT in this enum.
    """

    PRE_TOOL_USE = "pre_tool_use"
    POST_TOOL_USE = "post_tool_use"
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"


class PermissionDecisionKind(StrEnum):
    """Permission decision-kind per `arch/substrate.md` §2.C.

    Skills + specialists invoke `request_permission()` before authority-
    bound operations; substrate impl dispatches to native primitives
    (Claude Agent SDK CanUseTool callback; MS AF agent middleware HITL
    approval).
    """

    TOOL_USE = "tool_use"
    WRITE = "write"
    EXTERNAL_CALL = "external_call"


# ---------------------------------------------------------------------------
# Configuration + result models
# ---------------------------------------------------------------------------


class SubstrateConfig(BaseModel):
    """Substrate configuration loaded at workspace boot.

    Per `arch/substrate.md` §10 boot sequence step 1: loaded from
    workspace.md + per-impl config schema. Per `SubstrateConfig.deployment_tier`
    required field per §13.

    Per-impl extension config (e.g., Claude Agent SDK API keys + endpoints;
    MS AF middleware config) lives in per-impl SubstrateConfig subclasses
    OR in `details` field; this base captures framework-level config only.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    substrate_id: str
    """Substrate Implementation identity (e.g., `claude_agent_sdk`,
    `ms_agent_framework`) per `arch/substrate.md` §4 per-implementation-
    declares Substrate identity."""

    deployment_tier: DeploymentTier
    """Required field per `arch/substrate.md` §13."""

    mcp_servers: list[dict[str, Any]] = Field(default_factory=list)
    """MCP server registration list (per `arch/substrate.md` §10 boot
    sequence step 4). Each entry: name + transport + per-transport config.
    Refined to typed schema in pbs/manifests/mcp_server.py (Phase 6.1
    forthcoming)."""

    actor_id: str | None = None
    """Required at agent run for Tier 2+ per `arch/substrate.md` §13;
    optional for Tier 1."""

    tenant_id: str | None = None
    """Tier 3 federation per-tenant isolation per `arch/substrate.md` §13."""

    impl_config: dict[str, Any] = Field(default_factory=dict)
    """Per-impl extension config — refined per Implementation (Claude Agent
    SDK config; MS AF middleware config; etc.). Pydantic schemas per impl
    live in `pbs/impls/<impl>_config.py` (Phase 6.1 forthcoming)."""


class AgentRunResult(BaseModel):
    """Agent run result per `arch/substrate.md` §2.A.

    Returned by `run_agent()` after the agent loop completes.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    status: Literal[
        "completed",
        "wall_clock_timeout",
        "idle_timeout",
        "max_turns_exceeded",
        "canceled",
        "failed",
    ]
    """Lifecycle status. Per `arch/substrate.md` §15 pre-implementation
    operational concerns: wall_clock_timeout / idle_timeout per timeout
    config; canceled per cancel_agent_run; max_turns_exceeded per
    max_turns parameter."""

    final_output: Any = None
    """Final agent output. If `output_schema` was provided to run_agent,
    this is a validated instance of that schema (per `arch/substrate.md`
    §2.D structured output validation)."""

    messages: list[dict[str, Any]] = Field(default_factory=list)
    """Conversation messages (request + agent + tool messages). Shape per
    Phase 6 spec (per-impl message schema)."""

    tokens_used: int = 0
    """Total tokens consumed across the run."""

    duration_seconds: float = 0.0
    """Wall-clock duration of the run."""

    failure_reason: str | None = None
    """Non-None when status != 'completed'; describes finer-grain failure
    mode (per `arch/substrate.md` §11 SubstrateError category mapping)."""


class PermissionDecision(BaseModel):
    """Permission decision result per `arch/substrate.md` §2.C.

    Returned by `request_permission()`. Caller handles per-decision-kind
    behavior on deny.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    decision: Literal["allow", "deny"]
    reason: str
    """Human-readable explanation. Used in audit emission
    (`permission_decision` event records reason)."""


class SessionContext(BaseModel):
    """Session context per `arch/substrate.md` §2.F.

    Carries session identity + parent-session reference + activity
    timestamps + metadata. Per-substrate persistence semantics (in-memory
    / file / pluggable history-provider) accessed via SessionStore Protocol.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: str
    parent_session_id: str | None = None
    started_at: datetime
    last_activity_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class HookEvent(BaseModel):
    """Hook event payload per `arch/substrate.md` §2.E.

    Hooks return typed structured output capable of denying or modifying
    agent behavior. Concrete per-event-kind shape per Phase 6 spec
    (per-event-kind discriminated union).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    event_kind: HookEventKind
    timestamp: datetime
    details: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Substrate-emitted events (§8 — substrate-internal direct emission catalog)
# ---------------------------------------------------------------------------


class McpServerRegistered(AuditEventBase):
    """MCP server registration completed per `arch/substrate.md` §8."""

    event_kind: Literal["mcp_server_registered"] = "mcp_server_registered"


class McpServerRegistrationFallback(AuditEventBase):
    """Registration transport degraded per `arch/substrate.md` §8 + §12.

    Emitted when per-impl support degrades requested transport (e.g., MS
    AF in-process unavailable; fallback to subprocess). `details` field
    carries fallback reason + actual transport selected.
    """

    event_kind: Literal["mcp_server_registration_fallback"] = (
        "mcp_server_registration_fallback"
    )


class PermissionDecisionEvent(AuditEventBase):
    """request_permission resolved per `arch/substrate.md` §8."""

    event_kind: Literal["permission_decision"] = "permission_decision"


class BootComplete(AuditEventBase):
    """Substrate is_ready; agent loop accepting runs per `arch/substrate.md` §8."""

    event_kind: Literal["boot_complete"] = "boot_complete"


class ShutdownInitiated(AuditEventBase):
    """Substrate shutdown lifecycle initiated per `arch/substrate.md` §8 + §10."""

    event_kind: Literal["shutdown_initiated"] = "shutdown_initiated"


class ShutdownComplete(AuditEventBase):
    """Substrate shutdown lifecycle completed per `arch/substrate.md` §8 + §10."""

    event_kind: Literal["shutdown_complete"] = "shutdown_complete"


class AgentRunStarted(AuditEventBase):
    """Agent run started per `arch/substrate.md` §8."""

    event_kind: Literal["agent_run_started"] = "agent_run_started"


class AgentRunCompleted(AuditEventBase):
    """Agent run completed per `arch/substrate.md` §8."""

    event_kind: Literal["agent_run_completed"] = "agent_run_completed"


class AgentRunFailed(AuditEventBase):
    """Agent run failed per `arch/substrate.md` §8.

    `details` field carries failure_reason + status from AgentRunResult.
    """

    event_kind: Literal["agent_run_failed"] = "agent_run_failed"


class SpecialistRegistered(AuditEventBase):
    """SpecialistDescriptor materialized to substrate-native form per
    `arch/substrate.md` §8 + §2.G."""

    event_kind: Literal["specialist_registered"] = "specialist_registered"


# ---------------------------------------------------------------------------
# Error categories (§11 substrate error categories)
# ---------------------------------------------------------------------------


class SubstrateError(Exception):
    """Base for all substrate class errors per `arch/substrate.md` §11.

    Per-shape error semantics (§11 + per-shape policy bundles):
    practitioner-shape fail-closed; autonomous-business-shape fail-open
    with alert; personal-OS-shape fail-open.
    """


class SubstrateUnreachable(SubstrateError):
    """Substrate or its dependencies unreachable per `arch/substrate.md` §11.

    Per `mcp-fallback-policy` archive: fail-closed in practitioner-shape
    (defensibility-critical); shape policy declares per-shape error
    semantics.
    """


class PermissionDenied(SubstrateError):
    """Permission decision = deny per `arch/substrate.md` §11.

    Caller handles per-decision-kind. Composes with audit
    `PermissionDecisionEvent` (event records the deny + reason).
    """


class RegistrationConflict(SubstrateError):
    """Registration failure per `arch/substrate.md` §11.

    MCP server name collision; transport unavailable; specialist id
    collision.
    """


class AgentRunFailure(SubstrateError):
    """Agent loop failure per `arch/substrate.md` §11.

    `AgentRunResult.status` field also captures finer-grain failure mode.
    """


class StructuredOutputValidation(SubstrateError):
    """Auto-retry exhausted per `arch/substrate.md` §11.

    Output doesn't match declared schema after all retries.
    """


class CrossSubstrateMigration(SubstrateError):
    """Workspace serialization/deserialization across substrate boundaries
    per `arch/substrate.md` §11.

    Sub-categories: WorkspaceFormatIncompatible / SubstrateMetadataLoss /
    AuditTrailIntegrityViolation.
    """


class WorkspaceFormatIncompatible(CrossSubstrateMigration):
    """Workspace format incompatible with target substrate."""


class SubstrateMetadataLoss(CrossSubstrateMigration):
    """Substrate-specific metadata lost in cross-substrate migration.

    Per `profiles/G-composability-gate.md` line 159 backup-restore-migration
    round-trip; explicit marking required on cross-substrate migration.
    """


class AuditTrailIntegrityViolation(CrossSubstrateMigration):
    """Audit-trail integrity violated during cross-substrate restore.

    Per `arch/substrate.md` §11 + `arch/audit.md` §2.D integrity verification.
    Composes with audit `AuditIntegrityError` (raised at violation site).
    """


# ---------------------------------------------------------------------------
# Sub-Protocols (per-substrate session store; per-substrate extensions)
# ---------------------------------------------------------------------------


@runtime_checkable
class SessionStore(Protocol):
    """Per-substrate-impl session storage per `arch/substrate.md` §F.

    Per-substrate persistence semantics (in-memory / file / pluggable
    history-provider) per Implementation. Specific persistence semantics
    declared per Implementation via `SubstrateConfig.impl_config`.
    """

    def get_session(self, session_id: str) -> SessionContext | None:
        """Retrieve session by id; None if not found."""
        ...

    def save_session(self, session: SessionContext) -> None:
        """Persist session per impl semantics (in-memory / file / cloud)."""
        ...

    def list_sessions(self) -> list[str]:
        """Enumerate known session ids."""
        ...


@runtime_checkable
class HookHandle(Protocol):
    """Hook registration handle per `arch/substrate.md` §2.E.

    Returned by `register_hook()`; carries unregistration capability for
    cleanup at substrate shutdown.
    """

    def unregister(self) -> None:
        """Unregister the hook."""
        ...


# ---------------------------------------------------------------------------
# Substrate Protocol Surface — 7 capability categories typed
# ---------------------------------------------------------------------------


@runtime_checkable
class SubstrateProtocol(Protocol):
    """The Substrate Pattern A protocol Surface (Phase 6.1 Mode 3 spec).

    Per `arch/substrate.md` §6 tri-aspect: Surface (this Protocol; mechanism
    layer) + Implementations (Framework C distributable definitions
    wrapping native agentic runtimes) + Running Instance (workspace-bound
    at Owner B at boot).

    Cardinality (§5 + §9): 1:1 with workspace at framework level.
    `workspace.md` `substrate:` field selects exactly one Implementation
    by id.

    Substrate-coupling impossible-by-construction per §6 + `MAINTENANCE.md`
    TOP-LEVEL DESIGN PRINCIPLES §1: Surface-typed skill code structurally
    cannot reach native primitives without explicit isinstance check on
    extension Protocol (per §4 per-substrate extension Protocols pattern).

    Phase 6.1 reference impl: `pbs/impls/claude_agent_sdk_substrate.py`
    (forthcoming) satisfies this Protocol via Anthropic Claude Agent SDK
    native primitives.
    """

    # ------------------------------------------------------------------
    # Lifecycle (§9 + §10 boot sequence)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(cls, config: SubstrateConfig) -> "SubstrateProtocol":
        """Instantiate substrate Implementation per `arch/substrate.md` §10
        boot sequence step 3.

        Loads config; determines deployment tier; initializes per-impl
        runtime resources. Returns ready-to-register-MCP-servers instance.
        """
        ...

    @property
    def is_ready(self) -> bool:
        """True after boot sequence completes per `arch/substrate.md` §10
        boot sequence step 7. Once True, agent loop accepts runs (step 9).
        """
        ...

    async def shutdown(self) -> None:
        """Substrate shutdown per `arch/substrate.md` §10 shutdown sequence.

        Substrate releases its own runtime resources. Audit-trail flush +
        integrity verification happen LATER in audit storage realization
        shutdown (per `arch/audit.md` §10 audit-shuts-down-LAST + per
        `ARCHITECTURE.md` §6 composite boot+shutdown sequence).

        Steps 1-7 per substrate.md §10:
        1. Emit shutdown_initiated audit event
        2. Wait for in-flight runs / cancel per policy
        3. Stop accepting new run_agent calls
        4. Drain pending permission requests
        5. Stop MCP servers
        6. Release substrate-internal runtime resources
        7. Emit shutdown_complete audit event
        """
        ...

    # ------------------------------------------------------------------
    # §A Agent loop entry
    # ------------------------------------------------------------------

    async def run_agent(
        self,
        prompt: str,
        system_prompt: str | None = None,
        tools: list[str] | None = None,
        output_schema: type[BaseModel] | None = None,
        max_turns: int | None = None,
    ) -> AgentRunResult:
        """Start an agent run per `arch/substrate.md` §2.A.

        `output_schema` parameter enables §2.D structured output validation
        with auto-retry semantics; if provided, `AgentRunResult.final_output`
        is a validated instance of the schema.

        Pre-implementation operational concerns (Phase 6 forward-reference
        per §15): cancellation semantics; wall_clock_timeout; idle_timeout;
        rate_limit handling; streaming output. Reference impl handles per
        Phase 6 spec.

        Raises:
            AgentRunFailure: agent loop failure (status field also
                captures finer-grain mode).
            StructuredOutputValidation: auto-retry exhausted; output
                doesn't match `output_schema`.
            SubstrateUnreachable: substrate / dependencies unreachable.
        """
        ...

    # ------------------------------------------------------------------
    # §B MCP server registration + discovery
    # ------------------------------------------------------------------

    async def register_mcp_server(
        self,
        name: str,
        transport: TransportMode,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Register MCP server per `arch/substrate.md` §2.B + §12 transport
        variation.

        `transport` is explicit per call (not implicit-default per §12).
        Substrate may degrade transport per per-impl support (fallback
        emits `mcp_server_registration_fallback` audit event with details).

        Raises:
            RegistrationConflict: name collision OR transport unavailable
                (after fallback attempts exhausted).
        """
        ...

    def discover_mcp_servers(self) -> list[str]:
        """List registered MCP server names per `arch/substrate.md` §2.B."""
        ...

    def get_mcp_server(self, name: str) -> Any:
        """Retrieve registered MCP server by name per `arch/substrate.md`
        §2.B. Returns substrate-impl-specific server handle; specific shape
        per Phase 6 spec.
        """
        ...

    def list_tools(self, server_name: str) -> list[str]:
        """List available tools per registered MCP server per
        `arch/substrate.md` §2.B."""
        ...

    # ------------------------------------------------------------------
    # §C Permission flow
    # ------------------------------------------------------------------

    async def request_permission(
        self,
        decision_kind: PermissionDecisionKind,
        decision_context: dict[str, Any],
    ) -> PermissionDecision:
        """Request permission per `arch/substrate.md` §2.C.

        Skills + specialists invoke before authority-bound operations.
        Substrate impl dispatches to native primitives (Claude Agent SDK
        CanUseTool callback; MS AF agent middleware HITL approval).

        Composes with `glossary/authority-binding.md` for authority-decision
        moments where authority decisions require actor-binding evidence
        (HITL approval requires recorded human-actor identity).

        Emits `PermissionDecisionEvent` audit event.
        """
        ...

    # ------------------------------------------------------------------
    # §E Hook registration + event-bus
    # ------------------------------------------------------------------

    def register_hook(
        self,
        event_kind: HookEventKind,
        callback: Callable[[HookEvent], Any],
    ) -> HookHandle:
        """Register hook per `arch/substrate.md` §2.E.

        Hooks return typed structured output capable of denying or
        modifying agent behavior. Substrate-extension Protocols expose
        substrate-specific hook events (subagent lifecycle, pre-compact,
        etc.) — those are NOT in this Surface.

        Event-bus mechanism (substrate-internal; subsumes prior
        `coordination` Pattern A topic per
        `docs/decisions/greenfield-rederivation-pause.md` Step 3) dispatches
        events to registered callbacks.
        """
        ...

    # ------------------------------------------------------------------
    # §F Session/context management
    # ------------------------------------------------------------------

    def get_session_store(self) -> SessionStore:
        """Retrieve per-impl SessionStore handle per `arch/substrate.md` §2.F.

        Per-impl persistence semantics (in-memory / file / pluggable
        history-provider) declared per Implementation.
        """
        ...

    # ------------------------------------------------------------------
    # §G Specialist registration
    # ------------------------------------------------------------------

    async def register_specialist(self, descriptor: SpecialistDescriptor) -> None:
        """Register specialist per `arch/substrate.md` §2.G + `arch/specialist-skill.md` §10.

        Translates substrate-neutral SpecialistDescriptor (per `glossary/
        specialist.md` Pattern B DEFINITION aspect) into substrate-native
        form at boot-time. Per-substrate materialization: Claude Agent SDK
        registers as Anthropic plugin manifest; MS AF as module spec.

        Substrate-coupling impossible-by-construction (skills + workflow
        definitions written against SpecialistDescriptor work on any
        substrate impl).

        Per `arch/specialist-skill.md` §13 boot-time activation ordering:
        substrate Surface §G translates SpecialistDescriptor → substrate-
        native form at substrate-phase 4 step 4; per-skill registration
        emits `SpecialistSkillRegistered` per step 5.

        Emits `SpecialistRegistered` audit event.

        Raises:
            RegistrationConflict: specialist id collision.
            SpecialistManifestValidation: manifest fails schema validation
                (per `pbs.manifests.specialist`).
            SpecialistSubstrateClassPinViolation: descriptor's
                `activation_prereqs.substrate_class_pinned` incompatible
                with this substrate impl.
        """
        ...
