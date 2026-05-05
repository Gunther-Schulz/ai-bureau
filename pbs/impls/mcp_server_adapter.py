"""MCP-Server adapter — Phase 6.1 reference impl.

Per `arch/adapter.md` §3 + §4 per-implementation aspect: wraps generic MCP
protocol primitives to satisfy the MCP-Server per-class Adapter Surface
(`McpServerAdapterProtocol`) + cross-class META-Surface (`AdapterProtocol`).
Implementations live at Framework C scope as distributable definitions per
`glossary/framework-c-scope.md` + `arch/adapter.md` §6 tri-aspect (Surface
META + per-class = mechanism; Implementations = Framework C definitions;
Running Instance(s) = workspace-bound at Owner B per workspace.md adapter
bindings, multiple simultaneous).

Per `arch/adapter.md` §4 per-implementation declares:

- **Adapter identity**: `mcp_server` (generic reference impl; specific
  Anthropic-MCP / corpus-MCP / external-tool-MCP bindings configure the
  transport details + per-impl extension config, not separate Implementation
  classes at this thin-slice scope)
- **Integration class**: `MCP_SERVER` per `IntegrationClass` enum
- **Per-class Surface satisfaction**: `register_with_substrate` (composes
  with substrate Surface §B) / `negotiate_capabilities` / `invoke_tool` /
  `list_tools` per `arch/adapter.md` §2 MCP-Server Adapter Surface row
- **META-Surface satisfaction**: lifecycle (`from_config` / `is_ready` /
  `shutdown`) + auth (`auth_model` + `refresh_auth`) + permission flow
  integration (via substrate Surface §C composition; not exposed on
  adapter) + audit emission (via skill-side MCP audit gate; see §8 below)
  + error mapping (per §11 categories) + health check (`health_status`) +
  versioning (`version`)
- **Configuration schema**: `McpServerAdapterConfig` (subclass of
  `AdapterConfig` pinning adapter_id / integration_class / direction)
- **Error mapping**: MCP-protocol native errors → `AdapterError` category
  per §11; concrete mapping surfaces at Phase 6 pre-implementation-
  sharpening + deployment-instance MCP-server binding
- **Bidirectional vs unidirectional shape**: REQUEST_RESPONSE per
  `AdapterDirection` enum (MCP tool invocation = request/response
  per `arch/adapter.md` §4)
- **Deployment-tier compatibility**: Tier 1 / Tier 2 / Tier 3 (in_process
  Tier 1 native; subprocess Tier 1 + Tier 2; HTTP Tier 2 + Tier 3)

Per `arch/adapter.md` §6 adapter-coupling impossible-by-construction +
`MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code using only
`McpServerAdapterProtocol` methods is portable across MCP-Server adapter
Implementations within the class; impl-internal MCP-protocol primitives
are NOT in Surface — Phase 6.2 introduces per-impl extension Protocols
for the isinstance-gated impl-pinned code path.

Per `arch/adapter.md` §8 substrate-internal vs skill-side audit emission
N/A: adapter does not register the MCP audit gate; adapter actions emit
audit events via MCP audit gate (skill-side) only. Phase 6.1 thin-slice
collapses the skill-side MCP audit gate path to a directly-injected
`AuditEmitter` callable matching substrate's emitter shape (single-process
deployment); Phase 6.2 wires an actual MCP audit gate (registered by
substrate per `arch/substrate.md` §8) which routes adapter emissions
through the gate's MCP `record_audit_event` tool to the audit storage
realization. The structural distinction (substrate-internal direct vs
skill-side via MCP gate) is preserved in the docstrings + emitter
abstraction; the wire format converges at Phase 6.2.

Phase 6.1 thin-slice scope per BACKLOG §223: structural Surface
satisfaction (META + per-class) + concrete lifecycle (META boot via
`from_config_with_emitter` + per-class boot via `register_with_substrate`
+ shutdown) + concrete in-memory state mgmt (tool-catalog cache; circuit
state; substrate reference) + concrete audit emission. Real MCP transport
bring-up (in-process via `create_sdk_mcp_server`; subprocess stdio; HTTP)
+ real capability negotiation (MCP protocol exchange) + real tool
invocation (MCP request/response) are explicit Phase 6 wiring points
marked via `NotImplementedError` + docstring annotation; concrete delivery
happens at Phase 6 pre-implementation-sharpening + deployment-instance
MCP-server binding.

Per `arch/adapter.md` §15 pre-implementation operational concerns
(retry policies / timeouts / result streaming / per-tool quota tracking /
auth-state encryption-at-rest / multi-account scenarios): surfaced as
configuration fields + TODO markers; concrete semantics per Phase 6
pre-implementation-sharpening.

Per `arch/adapter.md` §11 per-shape error semantics: practitioner-shape =
fail-closed (defensibility-critical; especially axis-3 send operations);
autonomous-business-shape = fail-open with alert; personal-OS-shape =
fail-open. Phase 6.1 thin-slice is practitioner-shape per `BACKLOG.md`
§224 — concrete shape policy bundle declaration syntax surfaces at
Phase 6 wiring point.

Per `arch/adapter.md` §11 circuit-breaker semantics: per-instance
state machine (CLOSED / OPEN / HALF_OPEN). Phase 6.1 reference impl
exposes the state field + `health_status()` composes the state into
`HealthReport`; concrete failure-threshold tracking + recovery probe
mechanics are Phase 6 wiring points (per `arch/adapter.md` §15).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import ConfigDict, Field

from pbs.adapter import (
    AdapterAuthFailed,
    AdapterAuthRefreshed,
    AdapterConfig,
    AdapterDirection,
    AdapterError,
    AdapterStarted,
    AdapterStopped,
    AdapterUnreachable,
    AuthModel,
    CircuitState,
    HealthReport,
    HealthStatus,
    IntegrationClass,
    McpCapabilityNegotiated,
    McpServerAdapterProtocol,
    McpToolInvoked,
)
from pbs.substrate import (
    RegistrationConflict,
    SubstrateProtocol,
    TransportMode,
)
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Adapter identity + audit emitter type
# ---------------------------------------------------------------------------


ADAPTER_ID: Literal["mcp_server"] = "mcp_server"
"""Adapter Implementation identity per `arch/adapter.md` §4. The
generic-MCP-server-adapter reference impl spans the in-process / subprocess
/ HTTP transports per `pbs.substrate.TransportMode`; specific MCP server
bindings (Anthropic-MCP-server / corpus-MCP-server / external-tool-MCP-
server) configure transport details + per-impl extension fields rather
than registering as separate Implementation classes at this thin-slice
scope. Phase 6.2 introduces per-MCP-impl Implementation classes (e.g.,
`anthropic_mcp_server_adapter`) when concrete deployment evidence
warrants the discriminator.
"""


ADAPTER_VERSION = "0.1.0"
"""Reference-impl semver per `arch/adapter.md` §9 versioning. Major
bump on Phase 6 transport bring-up + real MCP protocol negotiation."""


AuditEmitter = Callable[[AuditEventBase], None]
"""Audit Surface §A emit binding per `arch/adapter.md` §8 skill-side MCP
audit gate path. Injected at construction; the callable shape matches
substrate's `AuditEmitter` for single-process Phase 6.1 deployment.

Per `arch/adapter.md` §8: adapter emits audit events ONLY via skill-side
MCP audit gate (no substrate-internal direct emission path; no
dual-emission framing). Phase 6.1 collapses the skill-side MCP audit
gate path to a directly-injected `AuditEmitter` callable matching
substrate's emitter shape; Phase 6.2 wires an actual MCP audit gate
(registered by substrate per `arch/substrate.md` §8) routing adapter
emissions through the gate's MCP `record_audit_event` tool to the audit
storage realization.

Per `arch/audit.md` §10 + `ARCHITECTURE.md` §6 composite boot subsection
audit-phase-1-3 ordering: audit storage realization MUST be ready BEFORE
adapter emits its first audit event (parallel to substrate Precondition).
"""


# ---------------------------------------------------------------------------
# Configuration (per-impl extension of AdapterConfig)
# ---------------------------------------------------------------------------


class McpServerAdapterConfig(AdapterConfig):
    """Per-impl configuration per `arch/adapter.md` §4 per-implementation
    declares 'Configuration schema (per-impl config — Pydantic; Phase 6)'.

    Extends `AdapterConfig` with MCP-server specifics. Framework-level
    config (`adapter_id` / `integration_class` / `auth_model` / `version` /
    `direction` / `deployment_tier_compat` / `auth_config` / `impl_config`)
    inherited from `AdapterConfig`.

    Pinned fields (Literal types narrow base AdapterConfig): `adapter_id` =
    "mcp_server"; `integration_class` = MCP_SERVER; `direction` =
    REQUEST_RESPONSE.

    Per `arch/adapter.md` §10 per-class auth models for MCP-Server: NONE
    (in-process); SUBPROCESS_TRUST (stdio); BEARER (HTTP); MTLS (HTTP
    federation). Per-binding auth selection via `auth_model` field;
    associated credentials referenced via `auth_config` (per-impl auth
    bundle — never literal secrets per substrate `api_key_ref` discipline).

    Per `arch/adapter.md` §15 pre-implementation operational concerns: per-
    invocation timeout fields surface here as nullable (None = no
    enforcement); concrete enforcement semantics + cancellation propagation
    per Phase 6 pre-implementation-sharpening.

    Secrets discipline (parallel to `pbs/impls/claude_agent_sdk_substrate.
    py` `api_key_ref` convention): `bearer_token_ref` carries a REFERENCE
    (env var name OR secrets-manager handle) — never the literal secret
    value. Resolution to the live secret happens at MCP transport call
    site via deployment-instance secrets-loader, NOT in the framework
    adapter config.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    adapter_id: Literal["mcp_server"] = ADAPTER_ID
    """Override base `AdapterConfig.adapter_id` to the literal MCP-server
    reference identity per `arch/adapter.md` §4."""

    integration_class: Literal[IntegrationClass.MCP_SERVER] = (
        IntegrationClass.MCP_SERVER
    )
    """Pinned per `arch/adapter.md` §3 MCP-Server class membership."""

    direction: Literal[AdapterDirection.REQUEST_RESPONSE] = (
        AdapterDirection.REQUEST_RESPONSE
    )
    """Pinned per `arch/adapter.md` §4 MCP = request/response architectural
    pattern."""

    version: str = ADAPTER_VERSION
    """Reference-impl semver per `arch/adapter.md` §9 versioning."""

    server_command: list[str] = Field(default_factory=list)
    """Subprocess MCP server command + args (used when `transport ==
    SUBPROCESS` at `register_with_substrate` time). Phase 6 wiring point:
    real subprocess spawn + stdio framing per MCP protocol; reference impl
    records the command without spawning."""

    server_url: str | None = None
    """HTTP MCP server URL (used when `transport == HTTP` at
    `register_with_substrate` time). Phase 6 wiring point: real HTTP
    client + connection pool; reference impl records the URL without
    connecting."""

    bearer_token_ref: str | None = None
    """Reference to bearer token (env var name OR secrets-manager handle);
    never the literal secret value. Phase 6 deployment-instance wiring
    resolves this at MCP transport call site."""

    invoke_timeout_seconds: float | None = None
    """Per-invocation wall-clock timeout per `arch/adapter.md` §15 pre-
    implementation operational concerns. None = no enforcement."""


# ---------------------------------------------------------------------------
# McpServerAdapter — Implementation class
# ---------------------------------------------------------------------------


class McpServerAdapter:
    """MCP-Server adapter Implementation satisfying `McpServerAdapterProtocol`
    (which extends `AdapterProtocol`).

    Per `arch/adapter.md` §6 tri-aspect Pattern A: this class IS the
    Implementation aspect at Framework C scope; instances bound at
    workspace boot per `workspace.md` adapter bindings list are the
    Running Instance aspect at Owner B (multiple simultaneous per
    `arch/adapter.md` §5 cardinality). Surface satisfaction is structural
    — instances pass `isinstance(adapter, McpServerAdapterProtocol)` per
    the `runtime_checkable` Protocol decorator on
    `pbs.adapter.McpServerAdapterProtocol`.

    Per `arch/adapter.md` §6 adapter-coupling impossible-by-construction:
    skills using only `McpServerAdapterProtocol` methods are portable
    across MCP-Server adapter Implementations by construction. Phase 6.2
    introduces per-MCP-impl extension Protocols exposing impl-native
    primitives accessed via isinstance gate at use site.

    Lifecycle (per `arch/adapter.md` §10 + `ARCHITECTURE.md` §6 composite
    boot subsection):

    - META boot via `from_config_with_emitter(config, audit_emit)`
      (testable factory; Protocol-required `from_config(config)` works
      with a no-op emitter for type-conformance only)
    - `is_ready` becomes True after META boot completes (matches the
      `AdapterProtocol.from_config` Protocol docstring: 'caller emits the
      audit event after `from_config` returns + `is_ready` becomes True'
      — reference impl emits `adapter_started` + sets is_ready inline)
    - Per-class boot via `register_with_substrate(substrate, transport)`
      which composes with substrate Surface §B (substrate emits
      `mcp_server_registered` from its end; this adapter records the
      registration internally and gates `negotiate_capabilities` /
      `invoke_tool` / `list_tools` on `_is_registered`)
    - `shutdown()` runs §10 per-instance shutdown sequence steps 1-6

    State (instance-private):

    - Substrate reference (post-`register_with_substrate`; None pre-
      registration)
    - Tool catalog cache (post-`negotiate_capabilities`; empty list at
      Phase 6.1 reference)
    - Circuit-breaker state (CLOSED initially; transitions Phase 6 wiring
      point per `arch/adapter.md` §15)
    - Last-success / last-failure timestamps (per `HealthReport` shape)

    Audit emission (per `arch/adapter.md` §11 per-class audit event-kind
    catalog + cross-class event kinds): emits `adapter_started` /
    `adapter_stopped` / `adapter_auth_refreshed` (META cross-class) +
    `mcp_capability_negotiated` / `mcp_tool_invoked` / `mcp_op_failed`
    (MCP-Server per-class) via injected `audit_emit` callable per
    `arch/adapter.md` §8 skill-side MCP audit gate path.
    """

    def __init__(
        self,
        config: McpServerAdapterConfig,
        audit_emit: AuditEmitter,
    ) -> None:
        """Internal constructor.

        Use `from_config_with_emitter()` factory per `arch/adapter.md` §10
        per-instance boot sequence step 2; this constructor is the
        underlying primitive.
        """
        self._config = config
        self._audit_emit = audit_emit
        self._instance_id_str: str = f"{ADAPTER_ID}:{uuid4()}"
        self._is_ready: bool = False
        self._is_shutting_down: bool = False
        self._is_registered: bool = False
        self._substrate: SubstrateProtocol | None = None
        self._registered_transport: TransportMode | None = None
        self._tool_catalog: list[str] = []
        self._capabilities: dict[str, Any] = {}
        self._circuit_state: CircuitState = CircuitState.CLOSED
        self._last_success_at: datetime | None = None
        self._last_failure_at: datetime | None = None

    # ------------------------------------------------------------------
    # Per-instance identity + versioning (META-Surface)
    # ------------------------------------------------------------------

    @property
    def adapter_id(self) -> str:
        """Per `arch/adapter.md` §4."""
        return self._config.adapter_id

    @property
    def instance_id(self) -> str:
        """Per `arch/adapter.md` §5 per-binding instance identifier
        (workspace-unique). Reference impl generates a UUID-based
        identifier at construction; Phase 6.2 wires per-binding
        instance_id from `workspace.md` `AdapterBinding.instance_id`
        through `from_config` argument plumbing."""
        return self._instance_id_str

    @property
    def integration_class(self) -> IntegrationClass:
        """Per `arch/adapter.md` §4."""
        return self._config.integration_class

    @property
    def version(self) -> str:
        """Per `arch/adapter.md` §9 versioning."""
        return self._config.version

    @property
    def auth_model(self) -> AuthModel:
        """Per `arch/adapter.md` §10 per-class auth models for MCP-Server:
        NONE / SUBPROCESS_TRUST / BEARER / MTLS."""
        return self._config.auth_model

    @property
    def direction(self) -> AdapterDirection:
        """Per `arch/adapter.md` §4 — pinned REQUEST_RESPONSE for
        MCP-Server class."""
        return self._config.direction

    # ------------------------------------------------------------------
    # Lifecycle (§10 per-instance boot + shutdown)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(cls, config: AdapterConfig) -> McpServerAdapterProtocol:
        """Boot per `arch/adapter.md` §10 per-instance boot sequence step 2
        — Protocol-required factory.

        Type-narrowed in two steps: META Adapter Surface contract takes the
        base `AdapterConfig` (adapter-impl-neutral); this impl narrows via
        isinstance check + raises `AdapterError` on mismatch.

        Audit emission caveat: no `AuditEmitter` is available through the
        Protocol-required signature. This factory uses a no-op emitter and
        emits `AdapterStarted` for type-conformance only. Production callers
        SHOULD use `from_config_with_emitter()` so the audit Surface §A
        binding is real per `arch/audit.md` §10 Precondition + `arch/
        adapter.md` §8 skill-side MCP audit gate path. Phase 6 pre-
        implementation-sharpening formalizes the emitter-injection pattern
        across adapter impls.

        Raises:
            AdapterError: `config` not `McpServerAdapterConfig`.
        """
        if not isinstance(config, McpServerAdapterConfig):
            raise AdapterError(
                f"McpServerAdapter requires McpServerAdapterConfig; "
                f"got {type(config).__name__}"
            )

        def _noop_emit(_event: AuditEventBase) -> None:
            return None

        instance = cls(config, audit_emit=_noop_emit)
        instance._is_ready = True
        instance._audit_emit(
            AdapterStarted(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=instance._instance_id_str,
                timestamp=datetime.now(tz=UTC),
                details={
                    "adapter_id": instance._config.adapter_id,
                    "integration_class": instance._config.integration_class.value,
                    "auth_model": instance._config.auth_model.value,
                    "direction": instance._config.direction.value,
                },
            )
        )
        return instance

    @classmethod
    async def from_config_with_emitter(
        cls,
        config: McpServerAdapterConfig,
        audit_emit: AuditEmitter,
    ) -> McpServerAdapter:
        """Phase 6.1 testable factory honoring `arch/audit.md` §10
        Precondition (audit storage realization ready BEFORE adapter emits
        its first audit event) + `arch/adapter.md` §8 skill-side MCP audit
        gate path.

        Production boot path; the audit Surface §A emitter must be wired
        before this factory fires per `ARCHITECTURE.md` §6 composite boot
        subsection audit-phase-1-3 ordering.

        Per `arch/adapter.md` §10 step 3 'Per-binding emit `adapter_started`
        audit event' + step 4 '`is_ready` becomes True': both happen here
        in sequence (sets is_ready then emits, matching substrate's
        BootComplete pattern). `register_with_substrate` is a separate
        per-class boot sub-step; methods that depend on substrate
        registration (`negotiate_capabilities` / `invoke_tool` /
        `list_tools`) check `_is_registered` independently.
        """
        instance = cls(config, audit_emit)
        instance._is_ready = True
        instance._audit_emit(
            AdapterStarted(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=instance._instance_id_str,
                timestamp=datetime.now(tz=UTC),
                details={
                    "adapter_id": instance._config.adapter_id,
                    "integration_class": instance._config.integration_class.value,
                    "auth_model": instance._config.auth_model.value,
                    "direction": instance._config.direction.value,
                },
            )
        )
        return instance

    @property
    def is_ready(self) -> bool:
        """Per `arch/adapter.md` §10 per-instance boot sequence step 4.
        True after META boot completes (does NOT require substrate
        registration). Once True, META-Surface operations are accessible;
        per-class operations that depend on substrate registration check
        `_is_registered` independently and raise `AdapterUnreachable` if
        called pre-registration. Becomes False at shutdown."""
        return self._is_ready and not self._is_shutting_down

    @property
    def circuit_state(self) -> CircuitState:
        """Per `arch/adapter.md` §11 circuit-breaker semantics. Read-only;
        transitions managed impl-internally. Phase 6 wiring point: real
        failure-threshold tracking + recovery probe mechanics per
        `arch/adapter.md` §15."""
        return self._circuit_state

    async def shutdown(self) -> None:
        """Per `arch/adapter.md` §10 per-instance shutdown sequence steps
        1-6.

        Idempotent: repeated calls return without re-emitting events.

        Steps:

        1. Drain in-flight adapter operations (Phase 6 wiring point —
           reference impl has no in-flight state to drain)
        2. Stop accepting new operations (sets `_is_shutting_down`)
        3. Flush adapter-internal state (auth tokens persisted; circuit
           state captured; threading caches cleaned — Phase 6 wiring
           points; reference impl clears in-memory state)
        4. Emit `AdapterStopped` audit event
        5. Per-binding shutdown returns
        6. Workspace's overall shutdown waits for all adapters drained
           per reverse declaration order (orchestrated by workspace boot;
           not enforced here)

        Audit-trail flush + integrity verification happen LATER in audit
        storage realization shutdown per `arch/audit.md` §10 audit-shuts-
        down-LAST + per `ARCHITECTURE.md` §6 composite boot+shutdown
        sequence — adapter does NOT flush the audit-trail itself.
        """
        if self._is_shutting_down:
            return
        self._is_shutting_down = True

        # Steps 1-3: drain in-flight + stop accepting + flush state. Phase
        # 6 wiring point surfaces concrete cancellation + in-flight-tracking
        # semantics; reference impl clears in-memory state.
        self._tool_catalog.clear()
        self._capabilities.clear()
        self._is_registered = False
        self._substrate = None
        self._registered_transport = None

        # Step 4: emit adapter_stopped.
        self._audit_emit(
            AdapterStopped(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id_str,
                timestamp=datetime.now(tz=UTC),
                details={
                    "adapter_id": self._config.adapter_id,
                    "integration_class": self._config.integration_class.value,
                },
            )
        )
        self._is_ready = False

    # ------------------------------------------------------------------
    # Auth surface (§10 auth-refresh lifecycle)
    # ------------------------------------------------------------------

    async def refresh_auth(self) -> None:
        """Per `arch/adapter.md` §10 auth-refresh lifecycle.

        For MCP-Server class auth models per `arch/adapter.md` §10:

        - `NONE` (in-process): no auth state to refresh; emits
          `AdapterAuthRefreshed` as a no-op record for trail consistency
        - `SUBPROCESS_TRUST` (stdio): subprocess identity is the trust
          anchor; no token to refresh; emits `AdapterAuthRefreshed`
          no-op
        - `BEARER` (HTTP): Phase 6 wiring point — real token refresh
          against IdP; reference impl raises `AdapterAuthFailed` to
          mark the wiring point explicitly
        - `MTLS` (HTTP federation): Phase 6 wiring point — cert rotation
          against PKI; reference impl raises `AdapterAuthFailed` to
          mark the wiring point explicitly

        Raises:
            AdapterUnreachable: adapter not ready.
            AdapterAuthFailed: BEARER / MTLS Phase 6 wiring point
                (reference impl marks the path).
        """
        if not self.is_ready:
            raise AdapterUnreachable(
                f"Adapter {self._instance_id_str} not ready; cannot refresh "
                f"auth."
            )
        if self._config.auth_model in {AuthModel.NONE, AuthModel.SUBPROCESS_TRUST}:
            self._audit_emit(
                AdapterAuthRefreshed(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id_str,
                    timestamp=datetime.now(tz=UTC),
                    details={
                        "adapter_id": self._config.adapter_id,
                        "auth_model": self._config.auth_model.value,
                        "outcome": "no_op",
                    },
                )
            )
            return
        raise AdapterAuthFailed(
            f"Adapter {self._instance_id_str} auth_model="
            f"{self._config.auth_model.value} is a Phase 6 wiring point "
            f"per `arch/adapter.md` §10 auth-refresh lifecycle + §15 "
            f"pre-implementation operational concerns."
        )

    # ------------------------------------------------------------------
    # Health check (META-Surface)
    # ------------------------------------------------------------------

    def health_status(self) -> HealthReport:
        """Per `arch/adapter.md` §2 META-Surface 'Health check' capability.

        Composes circuit-breaker state (§11) into health verdict per the
        canonical mapping in `arch/adapter.md` §2 + `pbs.adapter.
        HealthReport` docstring:

        - `CircuitState.OPEN` → `HealthStatus.UNHEALTHY`
        - `CircuitState.HALF_OPEN` → `HealthStatus.DEGRADED`
        - `CircuitState.CLOSED` (with recent successes OR no activity) →
          `HealthStatus.HEALTHY`

        ISO 8601 timestamps reported as `last_success_at` /
        `last_failure_at` (None if never succeeded / failed).
        """
        if self._circuit_state is CircuitState.OPEN:
            status = HealthStatus.UNHEALTHY
        elif self._circuit_state is CircuitState.HALF_OPEN:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.HEALTHY
        return HealthReport(
            status=status,
            circuit_state=self._circuit_state,
            last_success_at=(
                self._last_success_at.isoformat()
                if self._last_success_at is not None
                else None
            ),
            last_failure_at=(
                self._last_failure_at.isoformat()
                if self._last_failure_at is not None
                else None
            ),
            details={
                "adapter_id": self._config.adapter_id,
                "instance_id": self._instance_id_str,
                "is_registered": self._is_registered,
                "tool_catalog_size": len(self._tool_catalog),
            },
        )

    # ------------------------------------------------------------------
    # MCP-Server per-class Surface — substrate composition (§B)
    # ------------------------------------------------------------------

    async def register_with_substrate(
        self,
        substrate: SubstrateProtocol,
        transport: TransportMode,
    ) -> None:
        """Per `arch/adapter.md` §2 MCP-Server Adapter Surface tool
        registration + `arch/substrate.md` §2.B MCP server registration +
        §12 transport variation.

        Calls `substrate.register_mcp_server(name, transport, config)`
        with this adapter's instance identity + selected transport.
        Substrate emits `mcp_server_registered` (or
        `mcp_server_registration_fallback` if per-impl support degrades
        the requested transport per `arch/substrate.md` §8); this adapter
        does NOT emit a separate registration event (avoiding
        double-emission with substrate's authoritative path).

        After successful registration, `_is_registered` becomes True and
        `negotiate_capabilities` / `invoke_tool` / `list_tools` become
        usable.

        Phase 6 wiring point: real MCP transport setup per per-transport
        config (in-process via `create_sdk_mcp_server`; subprocess via
        `server_command` spawn + stdio framing; HTTP via `server_url` +
        bearer token resolution from `bearer_token_ref`). Reference impl
        records the registration without spawning + composes with
        substrate's in-memory MCP registry.

        Raises:
            AdapterUnreachable: adapter not ready (META boot incomplete)
                OR shutting down.
            pbs.substrate.RegistrationConflict: substrate-side name
                collision (propagated from
                `substrate.register_mcp_server`).
        """
        if not self.is_ready:
            raise AdapterUnreachable(
                f"Adapter {self._instance_id_str} not ready; cannot "
                f"register with substrate."
            )
        if self._is_registered:
            raise RegistrationConflict(
                f"Adapter {self._instance_id_str} already registered with "
                f"substrate (transport={self._registered_transport})."
            )
        await substrate.register_mcp_server(
            name=self._instance_id_str,
            transport=transport,
            config={
                "adapter_id": self._config.adapter_id,
                "auth_model": self._config.auth_model.value,
                "server_command": list(self._config.server_command),
                "server_url": self._config.server_url,
            },
        )
        self._substrate = substrate
        self._registered_transport = transport
        self._is_registered = True
        self._last_success_at = datetime.now(tz=UTC)

    # ------------------------------------------------------------------
    # MCP-Server per-class Surface — capability negotiation
    # ------------------------------------------------------------------

    async def negotiate_capabilities(self) -> Mapping[str, Any]:
        """Per `arch/adapter.md` §2 MCP-Server Adapter Surface capability
        negotiation.

        Phase 6 wiring point: real MCP capability exchange per protocol
        (tool catalog version; prompt support; resource support; sampling
        support). Reference impl returns an empty mapping after emitting
        the audit event; concrete capability negotiation happens at
        Phase 6 pre-implementation-sharpening + deployment-instance
        MCP-server binding.

        Emits `McpCapabilityNegotiated` audit event with negotiated
        capability set in `details`.

        Raises:
            AdapterUnreachable: adapter not ready OR not registered with
                substrate (registration is a precondition for capability
                negotiation per the per-class boot sequence).
        """
        self._require_registered("negotiate_capabilities")
        # Phase 6 wiring point: real MCP protocol exchange. Reference impl
        # records empty negotiated capability set.
        self._capabilities = {}
        self._audit_emit(
            McpCapabilityNegotiated(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id_str,
                timestamp=datetime.now(tz=UTC),
                details={
                    "adapter_id": self._config.adapter_id,
                    "instance_id": self._instance_id_str,
                    "capabilities": dict(self._capabilities),
                },
            )
        )
        self._last_success_at = datetime.now(tz=UTC)
        return dict(self._capabilities)

    # ------------------------------------------------------------------
    # MCP-Server per-class Surface — tool invocation
    # ------------------------------------------------------------------

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Mapping[str, Any],
    ) -> Any:
        """Per `arch/adapter.md` §2 MCP-Server Adapter Surface tool
        invocation.

        Phase 6.1 reference impl surfaces the audit-emission lifecycle
        bracket but raises `NotImplementedError` on actual MCP call
        (parallel to substrate `run_agent` Phase 6 wiring pattern).
        Concrete delivery per Phase 6 pre-implementation-sharpening +
        deployment-instance MCP-server binding (real MCP request/response
        per protocol; per-tool timeout enforcement; result streaming;
        per-tool quota tracking).

        Emits `McpToolInvoked` audit event with `tool_name` + argument
        shape (count, not values; values may be sensitive) + Phase 6
        wiring marker in `details`.

        Raises:
            AdapterUnreachable: adapter not ready OR not registered with
                substrate.
            NotImplementedError: Phase 6 wiring point (real MCP
                request/response).
        """
        self._require_registered("invoke_tool")
        self._audit_emit(
            McpToolInvoked(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id_str,
                timestamp=datetime.now(tz=UTC),
                details={
                    "adapter_id": self._config.adapter_id,
                    "instance_id": self._instance_id_str,
                    "tool_name": tool_name,
                    "arg_count": len(arguments),
                    "transport": (
                        self._registered_transport.value
                        if self._registered_transport is not None
                        else None
                    ),
                },
            )
        )
        raise NotImplementedError(
            f"McpServerAdapter.invoke_tool('{tool_name}') is a Phase 6 "
            f"wiring point per `arch/adapter.md` §15 pre-implementation "
            f"operational concerns. Reference impl emits McpToolInvoked "
            f"but defers actual MCP request/response to Phase 6 pre-"
            f"implementation-sharpening + deployment-instance MCP-server "
            f"binding."
        )

    def list_tools(self) -> list[str]:
        """Per `arch/adapter.md` §2 MCP-Server Adapter Surface tool
        invocation.

        Returns the tool-name catalog as known to this adapter (cached
        from last `negotiate_capabilities()` call OR refreshed per
        impl-internal policy). Reference impl returns the cached
        `_tool_catalog` (empty list at Phase 6.1 since
        `negotiate_capabilities` returns empty capability set; Phase 6
        wiring populates the catalog from real MCP capability exchange).

        Raises:
            AdapterUnreachable: adapter not ready OR not registered with
                substrate.
        """
        self._require_registered("list_tools")
        return list(self._tool_catalog)

    # ------------------------------------------------------------------
    # Internal: registration precondition
    # ------------------------------------------------------------------

    def _require_registered(self, op_name: str) -> None:
        """Per-class operation precondition gate.

        Per `arch/adapter.md` §10 per-instance boot sequence: per-class
        operations (negotiate_capabilities / invoke_tool / list_tools)
        require completed `register_with_substrate`. META-Surface
        operations (auth refresh / health check / shutdown) do NOT
        require registration.

        Raises:
            AdapterUnreachable: adapter not ready (META boot incomplete /
                shutting down) OR not registered with substrate.
        """
        if not self.is_ready:
            raise AdapterUnreachable(
                f"Adapter {self._instance_id_str} not ready; cannot "
                f"{op_name}."
            )
        if not self._is_registered:
            raise AdapterUnreachable(
                f"Adapter {self._instance_id_str} not registered with "
                f"substrate; cannot {op_name}. Call "
                f"register_with_substrate() first per `arch/adapter.md` "
                f"§10 per-instance boot sequence."
            )
