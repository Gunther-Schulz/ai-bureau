"""Claude Agent SDK substrate Implementation — Phase 6.1 reference impl.

Per `arch/substrate.md` §4 per-implementation aspect: wraps Anthropic Claude
Agent SDK native primitives to satisfy the Substrate Pattern A Surface
(`SubstrateProtocol`). Implementations live at Framework C scope as
distributable definitions per `glossary/framework-c-scope.md` + `arch/
substrate.md` §6 tri-aspect (Surface = mechanism; Implementations = Framework
C definitions; Running Instance = workspace-bound at Owner B at boot).

Per `arch/substrate.md` §4 per-implementation declares:

- **Substrate identity**: `claude_agent_sdk`
- **Surface satisfaction**: §A run_agent / §B register_mcp_server + discover +
  get + list_tools / §C request_permission / §D output_schema parameter on
  run_agent / §E register_hook + event-bus / §F get_session_store / §G
  register_specialist — all 7 capability categories satisfied structurally
- **Supported extension Protocols**: Phase 6.2 forward-reference per `arch/
  substrate.md` §15 pre-implementation operational concerns (subagent
  primitives / Channels / Sandbox / Thinking config / PreCompact hook); not
  satisfied by this Phase 6.1 reference impl
- **Configuration schema**: `ClaudeAgentSDKSubstrateConfig` (subclass of
  `SubstrateConfig`)
- **Error mapping**: SDK-native errors → `SubstrateError` category per §11;
  concrete mapping surfaces at Phase 6 pre-implementation-sharpening +
  deployment-instance wiring
- **Deployment-tier compatibility**: Tier 1 native; Tier 2 cloud via
  `api_endpoint` override; Tier 3 federated per W4 watch-list

Per `arch/substrate.md` §6 substrate-coupling impossible-by-construction +
`MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code using only
SubstrateProtocol methods is substrate-portable; SDK-native primitives are
NOT in Surface (per `arch/substrate.md` §2 'Explicitly NOT in Surface'
list) — Phase 6.2 introduces `ClaudeAgentSDKExtensions` Protocol for the
isinstance-gated substrate-pinned code path.

Per `arch/substrate.md` §8 substrate-internal vs skill-side audit emission
dual paths: this Implementation emits substrate-architectural events
(`mcp_server_registered` / `permission_decision` / `boot_complete` /
`shutdown_initiated` / etc.) via DIRECT internal access to the audit-trail
(NOT through MCP audit gate). The emitter is injected at construction via
`AuditEmitter` callable, honoring the §10 boot-sequence Precondition (audit
storage realization ready BEFORE substrate emits its first architectural
event).

Phase 6.1 thin-slice scope per BACKLOG §222: structural Surface satisfaction
+ concrete lifecycle (boot/shutdown) + concrete state mgmt (in-memory MCP
registry / hooks / specialists / sessions) + concrete audit emission. SDK-
backed agent-execution + MCP transport bring-up + permission CanUseTool
dispatch are explicit Phase 6 wiring points marked via NotImplementedError
+ docstring annotation; concrete delivery happens at Phase 6 pre-
implementation-sharpening + deployment-instance SDK binding.

Per `arch/substrate.md` §15 pre-implementation operational concerns
(cancellation semantics / wall_clock_timeout / idle_timeout / rate_limit /
health checks / streaming output / per-tenant isolation / HookCallback
signatures): surfaced as configuration fields + TODO markers; concrete
semantics per Phase 6 pre-implementation-sharpening.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel

from pbs.manifests.specialist import (
    SpecialistDescriptor,
    SpecialistSubstrateClassPinViolation,
)
from pbs.substrate import (
    AgentRunResult,
    AgentRunStarted,
    BootComplete,
    HookEvent,
    HookEventKind,
    HookHandle,
    McpServerRegistered,
    PermissionDecision,
    PermissionDecisionEvent,
    PermissionDecisionKind,
    RegistrationConflict,
    SessionContext,
    SessionStore,
    ShutdownComplete,
    ShutdownInitiated,
    SpecialistRegistered,
    SubstrateConfig,
    SubstrateError,
    SubstrateProtocol,
    SubstrateUnreachable,
    TransportMode,
)
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Substrate identity + audit emitter type
# ---------------------------------------------------------------------------


SUBSTRATE_ID: Literal["claude_agent_sdk"] = "claude_agent_sdk"
"""Substrate Implementation identity per `arch/substrate.md` §4 per-
implementation declares + Pattern A ≥2 implementation discriminator
preserved (current set: claude_agent_sdk + ms_agent_framework per `docs/
decisions/substrate-hand-rolled-drop.md`).
"""


AuditEmitter = Callable[[AuditEventBase], None]
"""Audit Surface §A emit binding per `arch/substrate.md` §8 substrate-
internal direct emission path. Injected at construction so the substrate
Instance can emit architectural events without routing through the MCP
audit gate (which is itself registered VIA the substrate — circularity
avoided per §8 dual-emission resolution).

Per `ARCHITECTURE.md` §6 composite boot subsection audit-phase-1-3 ordering:
audit storage realization MUST be ready BEFORE substrate emits its first
architectural event. The emitter is the contract for the audit Surface §A
binding the substrate uses for its dual-emission path.
"""


# ---------------------------------------------------------------------------
# Configuration (per-impl extension of SubstrateConfig)
# ---------------------------------------------------------------------------


class ClaudeAgentSDKSubstrateConfig(SubstrateConfig):
    """Per-impl configuration per `arch/substrate.md` §4 per-implementation
    declares 'Configuration schema (per-impl config — Pydantic; Phase 6)'.

    Extends `SubstrateConfig` with Claude Agent SDK specifics. Framework-
    level config (`substrate_id` / `deployment_tier` / `mcp_servers` /
    `actor_id` / `tenant_id`) inherited from `SubstrateConfig`.

    Per `arch/substrate.md` §15 pre-implementation operational concerns: per-
    run timeout fields surface here as nullable (None = no enforcement);
    concrete enforcement semantics + cancellation propagation per Phase 6
    pre-implementation-sharpening.

    Secrets discipline: `api_key_ref` carries a REFERENCE (env var name OR
    secrets-manager handle) — never the literal secret value. Resolution to
    the live secret happens at SDK call site via deployment-instance
    secrets-loader, NOT in the framework substrate config.
    """

    substrate_id: Literal["claude_agent_sdk"] = SUBSTRATE_ID
    """Override base `SubstrateConfig.substrate_id` to the literal SDK
    identity per `arch/substrate.md` §4."""

    api_endpoint: str = "https://api.anthropic.com"
    """Anthropic API endpoint. Tier 2 cloud + Tier 3 federated may override
    for proxy / on-prem / regional routing per `arch/substrate.md` §13 per-
    tier behavior in impl."""

    api_key_ref: str | None = None
    """Reference to API key (env var name OR secrets-manager handle); never
    the literal secret value. Phase 6 deployment-instance wiring resolves
    this at SDK call site."""

    model: str = "claude-opus-4-7"
    """Default Claude model id. Per-run override via per-call argument
    surfaced at Phase 6 pre-implementation-sharpening (extension to
    `run_agent` signature)."""

    max_turns_default: int = 50
    """Default agent-run max-turns ceiling per `arch/substrate.md` §2.A.
    Used when `run_agent(max_turns=None)`; explicit value at call site
    overrides."""

    wall_clock_timeout_seconds: float | None = None
    """Per-run wall-clock timeout per `arch/substrate.md` §15 pre-
    implementation operational concerns. None = no enforcement."""

    idle_timeout_seconds: float | None = None
    """Per-run idle timeout per `arch/substrate.md` §15 pre-implementation
    operational concerns. None = no enforcement."""


# ---------------------------------------------------------------------------
# SessionStore + HookHandle internal impls (Surface §F + §E)
# ---------------------------------------------------------------------------


class _InMemorySessionStore:
    """In-memory `SessionStore` impl per `arch/substrate.md` §F + §9 cross-
    session persistence.

    Tier 1 default: sessions lost at substrate shutdown (per `arch/substrate.
    md` §9 'In-memory (Tier 1 dev / debugging) — sessions lost at substrate
    shutdown'). Phase 6.2 file-backed + cloud-backed `SessionStore` impls
    surface per `arch/substrate.md` §F per-impl persistence semantics
    declared per Implementation.

    Satisfies `pbs.substrate.SessionStore` Protocol structurally.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, SessionContext] = {}

    def get_session(self, session_id: str) -> SessionContext | None:
        return self._sessions.get(session_id)

    def save_session(self, session: SessionContext) -> None:
        self._sessions[session.session_id] = session

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())


class _HookRegistration:
    """`HookHandle` impl per `arch/substrate.md` §2.E.

    Returned by `register_hook()`; carries unregistration capability for
    cleanup at substrate shutdown step 6 'Release substrate-internal runtime
    resources' per `arch/substrate.md` §10.
    """

    def __init__(
        self,
        substrate: ClaudeAgentSDKSubstrate,
        hook_id: str,
    ) -> None:
        self._substrate = substrate
        self._hook_id = hook_id

    def unregister(self) -> None:
        self._substrate._hooks.pop(self._hook_id, None)


# ---------------------------------------------------------------------------
# ClaudeAgentSDKSubstrate — Implementation class
# ---------------------------------------------------------------------------


class ClaudeAgentSDKSubstrate:
    """Claude Agent SDK substrate Implementation satisfying `SubstrateProtocol`.

    Per `arch/substrate.md` §6 tri-aspect Pattern A: this class IS the
    Implementation aspect at Framework C scope; instances bound at workspace
    boot are the Running Instance aspect at Owner B. Surface satisfaction is
    structural — instances pass `isinstance(s, SubstrateProtocol)` per the
    `runtime_checkable` Protocol decorator on `SubstrateProtocol`.

    Per `arch/substrate.md` §6 substrate-coupling impossible-by-construction:
    skills using only `SubstrateProtocol` methods are substrate-portable by
    construction. Phase 6.2 introduces a typed `ClaudeAgentSDKExtensions`
    Protocol exposing SDK-native primitives (subagents / Channels / etc.)
    accessed via isinstance gate at use site.

    Lifecycle (per `arch/substrate.md` §10 + `ARCHITECTURE.md` §6 composite
    boot subsection):

    - Boot via `from_config_with_emitter(config, audit_emit)` (testable
      factory; the substrate-Protocol-required `from_config(config)` works
      with a no-op emitter for type-conformance only)
    - `is_ready` becomes True after construction completes
    - `shutdown()` runs §10 shutdown sequence steps 1-7

    State (instance-private):

    - MCP server registry (per Surface §B)
    - Hook registry (per Surface §E)
    - Specialist registry (per Surface §G)
    - Session store (per Surface §F; in-memory `_InMemorySessionStore`)

    Audit emission (per `arch/substrate.md` §8 substrate-internal direct
    emission catalog): `mcp_server_registered` / `permission_decision` /
    `boot_complete` / `shutdown_initiated` / `shutdown_complete` /
    `agent_run_started` / `specialist_registered` etc. emit via injected
    `audit_emit` per §8 dual-emission path.
    """

    def __init__(
        self,
        config: ClaudeAgentSDKSubstrateConfig,
        audit_emit: AuditEmitter,
    ) -> None:
        """Internal constructor.

        Use `from_config_with_emitter()` factory per `arch/substrate.md` §10
        boot sequence step 3; this constructor is the underlying primitive.
        """
        self._config = config
        self._audit_emit = audit_emit
        self._instance_id: str = f"{SUBSTRATE_ID}:{uuid4()}"
        self._is_ready: bool = False
        self._is_shutting_down: bool = False
        self._mcp_servers: dict[str, dict[str, Any]] = {}
        self._hooks: dict[
            str,
            tuple[HookEventKind, Callable[[HookEvent], Any]],
        ] = {}
        self._specialists: dict[str, SpecialistDescriptor] = {}
        self._session_store: SessionStore = _InMemorySessionStore()
        self._started_at: datetime = datetime.now(tz=UTC)

    # ------------------------------------------------------------------
    # Lifecycle (§10 boot + shutdown)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(cls, config: SubstrateConfig) -> SubstrateProtocol:
        """Boot per `arch/substrate.md` §10 boot sequence step 3 — Protocol-
        required factory.

        Type-narrowed in two steps: substrate-Protocol contract takes the
        base `SubstrateConfig` (substrate-impl-neutral); this impl narrows
        via isinstance check + raises `SubstrateError` on mismatch.

        Audit emission caveat: no `AuditEmitter` is available through the
        Protocol-required signature. This factory uses a no-op emitter and
        emits `BootComplete` for type-conformance only. Production callers
        SHOULD use `from_config_with_emitter()` so the audit Surface §A
        binding is real per `arch/substrate.md` §10 Precondition + §8
        dual-emission resolution. Phase 6 pre-implementation-sharpening
        formalizes the emitter-injection pattern across substrate impls.

        Raises:
            SubstrateError: `config` not `ClaudeAgentSDKSubstrateConfig`.
        """
        if not isinstance(config, ClaudeAgentSDKSubstrateConfig):
            raise SubstrateError(
                f"ClaudeAgentSDKSubstrate requires "
                f"ClaudeAgentSDKSubstrateConfig; got {type(config).__name__}"
            )

        def _noop_emit(_event: AuditEventBase) -> None:
            return None

        instance = cls(config, audit_emit=_noop_emit)
        instance._is_ready = True
        instance._audit_emit(
            BootComplete(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=instance._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
            )
        )
        return instance

    @classmethod
    async def from_config_with_emitter(
        cls,
        config: ClaudeAgentSDKSubstrateConfig,
        audit_emit: AuditEmitter,
    ) -> ClaudeAgentSDKSubstrate:
        """Phase 6.1 testable factory honoring `arch/substrate.md` §10
        Precondition (audit storage realization ready BEFORE substrate emits
        its first architectural event) + §8 dual-emission convergence.

        Production boot path; the audit Surface §A emitter must be wired
        before this factory fires per `ARCHITECTURE.md` §6 composite boot
        subsection audit-phase-1-3 ordering.
        """
        instance = cls(config, audit_emit)
        instance._is_ready = True
        instance._audit_emit(
            BootComplete(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=instance._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
            )
        )
        return instance

    @property
    def is_ready(self) -> bool:
        """Per `arch/substrate.md` §10 boot sequence step 7. Once True, agent
        loop accepts runs (step 9). Becomes False at shutdown step 7."""
        return self._is_ready and not self._is_shutting_down

    async def shutdown(self) -> None:
        """Per `arch/substrate.md` §10 shutdown sequence steps 1-7.

        Substrate releases its own runtime resources. Audit-trail flush +
        integrity verification happen LATER in audit storage realization
        shutdown per `arch/audit.md` §10 audit-shuts-down-LAST + per
        `ARCHITECTURE.md` §6 composite boot+shutdown sequence — substrate
        does NOT flush the audit-trail itself.

        Idempotent: repeated calls return without re-emitting events.
        """
        if self._is_shutting_down:
            return
        self._is_shutting_down = True

        # Step 1: emit shutdown_initiated.
        self._audit_emit(
            ShutdownInitiated(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
            )
        )

        # Steps 2-4: wait for in-flight runs / cancel per policy + stop
        # accepting new runs + drain pending permission requests. Phase 6
        # pre-implementation-sharpening surfaces concrete cancellation +
        # in-flight-tracking semantics; reference impl has no in-flight
        # state to drain.

        # Step 5: stop MCP servers.
        # Phase 6 wiring point: subprocess MCP servers gracefully terminate
        # (current reference impl just clears the in-memory registry; real
        # SDK termination of subprocess transports happens at deployment-
        # instance wiring).
        self._mcp_servers.clear()

        # Step 6: release substrate-internal runtime resources.
        self._hooks.clear()

        # Step 7: emit shutdown_complete.
        self._is_ready = False
        self._audit_emit(
            ShutdownComplete(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
            )
        )

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
        """Per `arch/substrate.md` §2.A.

        Phase 6.1 reference impl surfaces the audit-emission lifecycle bracket
        but raises `NotImplementedError` on actual SDK call. Concrete delivery
        per Phase 6 pre-implementation-sharpening + deployment-instance SDK
        binding (real `claude-agent-sdk` / `anthropic.AsyncClient.messages.
        create` invocation; structured-output validation + auto-retry per
        `arch/substrate.md` §2.D; cancellation + timeout enforcement per
        §15 operational concerns).

        Raises:
            SubstrateUnreachable: substrate not ready.
            NotImplementedError: Phase 6 wiring point.
        """
        if not self.is_ready:
            raise SubstrateUnreachable(
                f"Substrate {self._instance_id} not ready; cannot run agent."
            )
        run_id = f"run-{uuid4()}"
        self._audit_emit(
            AgentRunStarted(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
                details={
                    "run_id": run_id,
                    "max_turns": max_turns or self._config.max_turns_default,
                    "model": self._config.model,
                    "has_output_schema": output_schema is not None,
                    "tools_count": len(tools) if tools else 0,
                    "system_prompt_present": system_prompt is not None,
                    "prompt_length": len(prompt),
                },
            )
        )
        raise NotImplementedError(
            "ClaudeAgentSDKSubstrate.run_agent is a Phase 6 wiring point per "
            "`arch/substrate.md` §15 pre-implementation operational concerns. "
            "Reference impl emits AgentRunStarted but defers actual agent "
            "execution to Phase 6 pre-implementation-sharpening + deployment-"
            "instance SDK binding."
        )

    # ------------------------------------------------------------------
    # §B MCP server registration + discovery
    # ------------------------------------------------------------------

    async def register_mcp_server(
        self,
        name: str,
        transport: TransportMode,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Per `arch/substrate.md` §2.B + §12 transport variation.

        Per `arch/substrate.md` §12 per-impl transport support: Claude Agent
        SDK substrate supports all three transports natively (in-process via
        `create_sdk_mcp_server` / subprocess / HTTP) — no transport
        degradation needed (vs MS AF in-process → subprocess fallback).
        `mcp_server_registration_fallback` event is therefore not emitted by
        this Implementation under normal operation.

        Phase 6 wiring point: real SDK server-process spawn + transport setup
        per deployment-instance wiring; reference impl records the
        registration in the in-memory registry + emits the audit event.

        Raises:
            SubstrateUnreachable: substrate not ready.
            RegistrationConflict: server name already registered.
        """
        if not self.is_ready:
            raise SubstrateUnreachable(
                f"Substrate {self._instance_id} not ready; cannot register "
                f"MCP server '{name}'."
            )
        if name in self._mcp_servers:
            raise RegistrationConflict(
                f"MCP server '{name}' already registered."
            )
        self._mcp_servers[name] = {
            "transport": transport,
            "config": config or {},
        }
        self._audit_emit(
            McpServerRegistered(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
                details={
                    "server_name": name,
                    "transport": transport.value,
                },
            )
        )

    def discover_mcp_servers(self) -> list[str]:
        """Per `arch/substrate.md` §2.B."""
        return list(self._mcp_servers.keys())

    def get_mcp_server(self, name: str) -> Any:
        """Per `arch/substrate.md` §2.B.

        Returns substrate-impl-specific server handle; specific shape per
        Phase 6 pre-implementation-sharpening (current reference impl
        returns the registration dict).

        Raises:
            RegistrationConflict: server not registered.
        """
        if name not in self._mcp_servers:
            raise RegistrationConflict(
                f"MCP server '{name}' not registered."
            )
        return self._mcp_servers[name]

    def list_tools(self, server_name: str) -> list[str]:
        """Per `arch/substrate.md` §2.B.

        Phase 6 wiring point: real SDK introspection of registered server's
        tool catalog. Reference impl returns empty list.

        Raises:
            RegistrationConflict: server not registered.
        """
        if server_name not in self._mcp_servers:
            raise RegistrationConflict(
                f"MCP server '{server_name}' not registered."
            )
        return []

    # ------------------------------------------------------------------
    # §C Permission flow
    # ------------------------------------------------------------------

    async def request_permission(
        self,
        decision_kind: PermissionDecisionKind,
        decision_context: dict[str, Any],
    ) -> PermissionDecision:
        """Per `arch/substrate.md` §2.C.

        Phase 6 wiring point: real SDK CanUseTool callback dispatch + HITL
        approval flow per deployment-instance wiring. Reference impl
        returns default-allow with the audit emission shape per `arch/
        substrate.md` §8 `permission_decision` event-kind.

        Composes with `glossary/authority-binding.md` for authority-decision
        moments where authority decisions require actor-binding evidence
        (HITL approval requires recorded human-actor identity).

        Raises:
            SubstrateUnreachable: substrate not ready.
        """
        if not self.is_ready:
            raise SubstrateUnreachable(
                f"Substrate {self._instance_id} not ready; cannot request "
                f"permission."
            )
        decision = PermissionDecision(
            decision="allow",
            reason=(
                "Phase 6.1 reference impl default-allow; Phase 6 wiring "
                "delivers concrete CanUseTool callback dispatch + HITL "
                "approval flow per `arch/substrate.md` §15 pre-implementation "
                "operational concerns."
            ),
        )
        self._audit_emit(
            PermissionDecisionEvent(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
                details={
                    "decision_kind": decision_kind.value,
                    "decision": decision.decision,
                    "reason": decision.reason,
                    "decision_context": decision_context,
                },
            )
        )
        return decision

    # ------------------------------------------------------------------
    # §E Hook registration + event-bus
    # ------------------------------------------------------------------

    def register_hook(
        self,
        event_kind: HookEventKind,
        callback: Callable[[HookEvent], Any],
    ) -> HookHandle:
        """Per `arch/substrate.md` §2.E.

        Substrate-extension hook events (subagent lifecycle / pre-compact /
        etc.) are NOT in this Surface — they belong to Phase 6.2
        `ClaudeAgentSDKExtensions` Protocol per `arch/substrate.md` §2 + §4
        per-substrate extension Protocols pattern.

        The event-bus mechanism (substrate-internal; subsumes prior
        `coordination` Pattern A topic per `docs/decisions/greenfield-
        rederivation-pause.md` Step 3) dispatches events to registered
        callbacks at the substrate's lifecycle hook moments (PRE/POST tool
        use; agent start; agent end). Phase 6 wiring point: real SDK hook
        dispatch (RunHooks per Claude Agent SDK).
        """
        hook_id = f"hook-{uuid4()}"
        self._hooks[hook_id] = (event_kind, callback)
        return _HookRegistration(self, hook_id)

    # ------------------------------------------------------------------
    # §F Session/context management
    # ------------------------------------------------------------------

    def get_session_store(self) -> SessionStore:
        """Per `arch/substrate.md` §2.F + §9 cross-session persistence.

        Returns the in-memory SessionStore (Tier 1 default). Phase 6.2
        file-backed + cloud-backed SessionStore impls surface per `arch/
        substrate.md` §F per-impl persistence semantics.
        """
        return self._session_store

    # ------------------------------------------------------------------
    # §G Specialist registration
    # ------------------------------------------------------------------

    async def register_specialist(self, descriptor: SpecialistDescriptor) -> None:
        """Per `arch/substrate.md` §2.G + `arch/specialist-skill.md` §13
        boot-time activation ordering step 4.

        Translates substrate-neutral `SpecialistDescriptor` (per `glossary/
        specialist.md` Pattern B DEFINITION aspect) into substrate-native
        form. Phase 6 wiring point: real Claude Agent SDK plugin manifest
        registration per `arch/substrate.md` §2.G ('Claude Agent SDK
        substrate registers as Anthropic plugin manifest'); reference impl
        records the descriptor in the in-memory registry.

        Validates substrate-class pin per `descriptor.activation_prereqs.
        substrate_class_pinned` per `arch/specialist-skill.md` §11 cross-
        substrate compatibility — raises
        `SpecialistSubstrateClassPinViolation` if descriptor pinned to
        substrate impl(s) excluding `claude_agent_sdk`.

        Raises:
            SubstrateUnreachable: substrate not ready.
            RegistrationConflict: specialist `name` already registered.
            SpecialistSubstrateClassPinViolation: descriptor pinned to other
                substrate impl(s).
        """
        if not self.is_ready:
            raise SubstrateUnreachable(
                f"Substrate {self._instance_id} not ready; cannot register "
                f"specialist '{descriptor.name}'."
            )
        if descriptor.name in self._specialists:
            raise RegistrationConflict(
                f"Specialist '{descriptor.name}' already registered."
            )
        pinned = descriptor.activation_prereqs.substrate_class_pinned
        if pinned and SUBSTRATE_ID not in pinned:
            raise SpecialistSubstrateClassPinViolation(
                f"Specialist '{descriptor.name}' pinned to {pinned}; this "
                f"substrate is '{SUBSTRATE_ID}'."
            )
        self._specialists[descriptor.name] = descriptor
        self._audit_emit(
            SpecialistRegistered(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
                details={
                    "specialist_name": descriptor.name,
                    "version": descriptor.version,
                    "skill_count": len(descriptor.skills),
                },
            )
        )
