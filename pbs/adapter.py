"""Adapter Protocol Surface — Pattern A protocol per `arch/adapter.md`.

Per `arch/adapter.md` §1: the external-integration-boundary primitive — the
workspace's contract with EXTERNAL-WORLD systems. Tri-aspect Pattern A
(per-integration-class Surface = mechanism per class; Implementations =
Framework C definitions; Running Instance(s) = workspace-bound at Owner B
per `workspace.md` adapter bindings, typically MULTIPLE simultaneously).

Internal-vs-external axis: substrate = INTERNAL runtime contract for agent
execution; adapter = EXTERNAL-WORLD integration boundary. Both Pattern A;
cardinality follows (substrate singular per workspace; adapter multiple
per workspace).

Surface (§2; two-layer structure):

- META-Surface (cross-class architectural conventions): lifecycle entry
  (`from_config` / `shutdown` / `is_ready`) + auth surface (`auth_model` +
  `refresh_auth`) + permission flow integration (via substrate Surface §C
  composition; not exposed on adapter) + audit emission (via MCP audit
  gate skill-side; via composition with audit Surface) + error mapping
  (per §11 categories) + health check (`health_status`) + versioning
  (`version` + `min_substrate_version`).
- Per-integration-class Surfaces (5 classes per §3 framework-baseline
  confirmed): Email / Accounting / MCP-Server / A2A-Peer / File-Sync.
  Per-class Surfaces are NOT extension Protocols — every implementation
  in a class MUST satisfy that class's Surface.

Per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE thin-slice scope +
`BACKLOG.md` Phase 6.1: this Phase 6.1 spec covers the META-Surface
(`AdapterProtocol`) + the MCP-Server per-class Surface
(`McpServerAdapterProtocol`) only. The Email / Accounting / A2A-Peer /
File-Sync per-class Surfaces are deferred to Phase 6.2 (the
`IntegrationClass` enum lists all 5 since the architectural shape is
LOCKED at 5 classes per `arch/adapter.md` §3; only the per-class Surface
Protocols + impls for the deferred 4 land in 6.2).

Per §8: N/A for adapter — adapter actions emit audit events via MCP
audit gate (skill-side) only; adapter does not register the MCP audit
gate (substrate does); no dual-emission framing applies.

Per §13: N/A — adapter behavior is shape-class-shape + integration-class-
shape, NOT tier-shape. Per-impl tier-compatibility declared in
`AdapterConfig.deployment_tier_compat` (Surface contracts themselves are
tier-uniform).

Per §14: per-shape policy variation applies (audit emission granularity /
permission flow / error escalation) per shape policy bundles —
adapter Implementations themselves are shape-neutral; shape policy
interprets architectural events + decisions per shape's mandate.

Phase 6.1 reference impl: `pbs/impls/mcp_server_adapter.py` (forthcoming)
satisfies `McpServerAdapterProtocol` for the MCP-Server class.
"""

from collections.abc import Mapping
from enum import StrEnum
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from pbs.substrate import DeploymentTier, SubstrateProtocol, TransportMode
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Supporting enums (§3 integration classes; §10 auth models; §11 circuit;
# META-Surface health check; §4 bidirectional/unidirectional shape)
# ---------------------------------------------------------------------------


class IntegrationClass(StrEnum):
    """Per-integration-class identifier per `arch/adapter.md` §3.

    Five framework-baseline classes locked per §3 framework-baseline-vs-
    shape-extension partition (universal-applicability test passed for
    each across hypothetical legal-practice / research-paper / engineering-
    doc workspaces).

    Phase 6.1 spec covers `MCP_SERVER` per-class Surface only;
    `EMAIL` / `ACCOUNTING` / `A2A_PEER` / `FILE_SYNC` per-class Surface
    Protocols + impls deferred to Phase 6.2 per `MAINTENANCE.md` TOP-LEVEL
    MILESTONE STRUCTURE + `BACKLOG.md` §215-228. The enum lists all 5
    because the architectural shape is LOCKED at 5 classes per §3.
    """

    EMAIL = "email"
    ACCOUNTING = "accounting"
    MCP_SERVER = "mcp_server"
    A2A_PEER = "a2a_peer"
    FILE_SYNC = "file_sync"


class AuthModel(StrEnum):
    """Per-class typical auth models per `arch/adapter.md` §10.

    Each Implementation declares its specific auth model; META-Surface
    validates the declaration (`AdapterProtocol.auth_model` property).
    Per-class typical defaults per §10:

    - Email: OAUTH (gmail / outlook), BASIC_AUTH (SMTP legacy), PASSWORD
      (IMAP)
    - Accounting: OAUTH (modern APIs), API_KEY (Fastbill / Lexware),
      SHARED_SECRET
    - MCP-Server: NONE (in-process), SUBPROCESS_TRUST, BEARER (HTTP),
      MTLS
    - A2A-Peer: MTLS (federation), SHARED_SECRET (initial handshake),
      CAPABILITY_TOKEN
    - File-Sync: OAUTH (cloud storage), SSH_KEY (git), CREDENTIAL_PAIR
    """

    NONE = "none"
    OAUTH = "oauth"
    API_KEY = "api_key"
    BASIC_AUTH = "basic_auth"
    PASSWORD = "password"
    BEARER = "bearer"
    MTLS = "mtls"
    SUBPROCESS_TRUST = "subprocess_trust"
    SHARED_SECRET = "shared_secret"
    CAPABILITY_TOKEN = "capability_token"
    SSH_KEY = "ssh_key"
    CREDENTIAL_PAIR = "credential_pair"


class CircuitState(StrEnum):
    """Circuit-breaker state per `arch/adapter.md` §11.

    Per-instance state. Per-shape policy declares per-shape failure
    threshold + recovery timer (§14 cross-shape policy variation).

    Transitions per §11 circuit-breaker semantics:

    - `CLOSED` → `OPEN` when failure threshold exceeded in rolling window
      (emits `AdapterCircuitOpened`)
    - `OPEN` → `HALF_OPEN` after recovery timer elapses (recovery probe
      window)
    - `HALF_OPEN` → `CLOSED` on probe success (emits
      `AdapterCircuitClosed`)
    - `HALF_OPEN` → `OPEN` on probe failure (extended timeout)
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class HealthStatus(StrEnum):
    """META-Surface health-check verdict per `arch/adapter.md` §2 META-
    Surface "Health check" capability + §11 circuit-breaker integration.
    """

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class AdapterDirection(StrEnum):
    """Per-integration-class architectural direction per `arch/adapter.md`
    §4 bidirectional vs unidirectional patterns.

    Per-class shape determines lifecycle (when to drain inbound on
    shutdown; when to expect async returns; when to subscribe vs poll).
    Declared at Implementation level (read via Implementation property);
    Phase 6 spec encodes per-class shape in Pydantic Protocol typing.
    """

    MOSTLY_OUTBOUND_THREADING_INBOUND = "mostly_outbound_threading_inbound"
    """Email pattern: send dominant; threading manages inbound replies."""

    BIDIRECTIONAL_SYNC = "bidirectional_sync"
    """Accounting / CRM-adapter pattern: invoice → response."""

    BIDIRECTIONAL_ASYNC = "bidirectional_async"
    """A2A-peer pattern: federation peer messages flow both directions
    independently."""

    PUSH_RECEIVER = "push_receiver"
    """File-sync with subscribe-to-changes; webhook adapters."""

    PULL_ONLY = "pull_only"
    """Read-only file-sync; reference-data MCP adapters."""

    REQUEST_RESPONSE = "request_response"
    """MCP-Server pattern: tool invocation request/response."""


# ---------------------------------------------------------------------------
# Configuration + binding + health models
# ---------------------------------------------------------------------------


class AdapterConfig(BaseModel):
    """Adapter configuration loaded at workspace boot per `arch/adapter.md`
    §10 per-instance boot sequence step 2.

    Per `arch/adapter.md` §4 per-implementation declares: adapter
    identity + integration class + auth model + version + deployment-tier
    compatibility + per-impl extension config.

    Per-impl extension config (e.g., gmail OAuth client + scopes;
    Anthropic-MCP server transport details) lives in per-impl
    `AdapterConfig` subclasses OR in `impl_config` field; this base
    captures framework-level config only.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    adapter_id: str
    """Adapter Implementation identity (e.g., `gmail`, `outlook`,
    `fastbill`, `mcp_anthropic`) per `arch/adapter.md` §4."""

    integration_class: IntegrationClass
    """Which per-class Surface this Implementation satisfies per
    `arch/adapter.md` §4."""

    auth_model: AuthModel
    """Auth model declared per Implementation per `arch/adapter.md` §10
    per-class auth models."""

    version: str
    """Implementation semver-like version per `arch/adapter.md` §9
    versioning."""

    min_substrate_version: str | None = None
    """Minimum compatible substrate version per `arch/adapter.md` §9
    versioning."""

    compat_substrate_versions: list[str] = Field(default_factory=list)
    """Compatible substrate versions per `arch/adapter.md` §9
    versioning."""

    direction: AdapterDirection
    """Per-class architectural direction per `arch/adapter.md` §4
    bidirectional vs unidirectional patterns."""

    deployment_tier_compat: list[DeploymentTier] = Field(
        default_factory=lambda: [
            DeploymentTier.TIER_1,
            DeploymentTier.TIER_2,
            DeploymentTier.TIER_3,
        ]
    )
    """Per-impl deployment-tier compatibility per `arch/adapter.md` §13
    N/A note: per-class Surfaces are tier-uniform; per-impl declares
    which tiers it can run on. Reuses `pbs.substrate.DeploymentTier`."""

    auth_config: dict[str, Any] = Field(default_factory=dict)
    """Per-impl auth configuration (OAuth client / API key reference /
    cert path / etc.). Refined per Implementation; auth-state encryption-
    at-rest mechanics per §15 + per-shape policy."""

    impl_config: dict[str, Any] = Field(default_factory=dict)
    """Per-impl extension config — refined per Implementation
    (gmail-specific options; fastbill-specific tax-form fields; etc.).
    Pydantic schemas per impl live in `pbs/impls/<impl>_config.py`
    (Phase 6 forthcoming)."""


class AdapterBinding(BaseModel):
    """One entry in `workspace.md` adapter bindings list per
    `arch/adapter.md` §5 selection mechanics.

    Workspace binds N adapter Implementations simultaneously per §5
    cardinality; per-binding entry declares: integration class +
    Implementation id + per-instance config + min-version constraint.

    Per-shape policy may impose per-class cardinality cap (§5).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    integration_class: IntegrationClass
    """Which per-class Surface this binding consumes."""

    adapter_id: str
    """Implementation id (must resolve to known Implementation per
    Framework C definition catalog)."""

    instance_id: str
    """Per-binding instance identifier (workspace-unique). Enables
    multi-account same-class binding when W4 watch-list resolves
    (e.g., personal + work email per `arch/adapter.md` §16 W4)."""

    min_version: str | None = None
    """Minimum compatible Implementation version constraint."""

    max_version: str | None = None
    """Maximum compatible Implementation version constraint (optional)."""

    instance_config: dict[str, Any] = Field(default_factory=dict)
    """Per-instance config; merged with Implementation defaults at
    `from_config` boot."""


class HealthReport(BaseModel):
    """Adapter health-check report per `arch/adapter.md` §2 META-Surface
    "Health check" capability.

    Returned by `AdapterProtocol.health_status()`. Composes with circuit-
    breaker state (§11) — `CircuitState.OPEN` typically maps to
    `HealthStatus.UNHEALTHY`; `HALF_OPEN` to `DEGRADED`.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    status: HealthStatus
    circuit_state: CircuitState
    last_success_at: str | None = None
    """ISO 8601 timestamp of last successful op; None if never succeeded."""

    last_failure_at: str | None = None
    """ISO 8601 timestamp of last failed op; None if never failed."""

    details: dict[str, Any] = Field(default_factory=dict)
    """Per-impl health details (auth-state, quota counters, etc.)."""


# ---------------------------------------------------------------------------
# Cross-class adapter events (§11 META-Surface-level event-kind catalog)
# ---------------------------------------------------------------------------


class AdapterStarted(AuditEventBase):
    """Adapter instance booted + ready per `arch/adapter.md` §10
    per-instance boot sequence step 3 + §11 cross-class event kinds."""

    event_kind: Literal["adapter_started"] = "adapter_started"


class AdapterStopped(AuditEventBase):
    """Adapter instance shut down per `arch/adapter.md` §10 per-instance
    shutdown sequence step 5 + §11 cross-class event kinds."""

    event_kind: Literal["adapter_stopped"] = "adapter_stopped"


class AdapterAuthRefreshed(AuditEventBase):
    """Auth tokens refreshed per `arch/adapter.md` §10 auth-refresh
    lifecycle proactive refresh + §11 cross-class event kinds."""

    event_kind: Literal["adapter_auth_refreshed"] = "adapter_auth_refreshed"


class AdapterAuthExpiredEvent(AuditEventBase):
    """Auth-refresh failure per `arch/adapter.md` §10 refresh-failure
    handling + §11 cross-class event kinds.

    Composes with `AdapterAuthExpired` error (raised at refresh-failure
    site; this event records the failure in audit-trail). Class name
    suffixed with `Event` to disambiguate from `AdapterAuthExpired`
    error class (parallel to `pbs/substrate.py` `PermissionDecisionEvent`
    naming convention).
    """

    event_kind: Literal["adapter_auth_expired"] = "adapter_auth_expired"


class AdapterCircuitOpened(AuditEventBase):
    """Circuit-breaker opened (failure threshold exceeded) per
    `arch/adapter.md` §11 circuit-breaker semantics + cross-class
    event kinds."""

    event_kind: Literal["adapter_circuit_opened"] = "adapter_circuit_opened"


class AdapterCircuitClosed(AuditEventBase):
    """Circuit-breaker closed (recovery probe succeeded) per
    `arch/adapter.md` §11 circuit-breaker semantics + cross-class
    event kinds."""

    event_kind: Literal["adapter_circuit_closed"] = "adapter_circuit_closed"


class AdapterRebound(AuditEventBase):
    """Hot-swap re-binding completed per `arch/adapter.md` §5 re-binding
    semantics + §9 hot-swap migration mechanics + §11 cross-class event
    kinds.

    `details` field carries old + new Implementation identities + version
    delta.
    """

    event_kind: Literal["adapter_rebound"] = "adapter_rebound"


class AdapterQuotaThresholdReached(AuditEventBase):
    """Quota counter approaching limit per `arch/adapter.md` §11 quota
    tracking + cross-class event kinds.

    `details` field carries quota model (`token_bucket` / `sliding_window`
    / `per_resource`) + current/limit ratio.
    """

    event_kind: Literal["adapter_quota_threshold_reached"] = (
        "adapter_quota_threshold_reached"
    )


# ---------------------------------------------------------------------------
# MCP-Server per-class adapter events (§11 per-class event-kind catalog)
#
# Phase 6.1 covers MCP-Server class only; Email / Accounting / A2A-Peer /
# File-Sync per-class events deferred to Phase 6.2 per `MAINTENANCE.md`
# TOP-LEVEL MILESTONE STRUCTURE + `BACKLOG.md` §215-228.
# ---------------------------------------------------------------------------


class McpToolInvoked(AuditEventBase):
    """MCP tool invocation per `arch/adapter.md` §11 MCP-Server per-class
    event kinds. `details` carries tool_name + arg shape + result hash."""

    event_kind: Literal["mcp_tool_invoked"] = "mcp_tool_invoked"


class McpQueryExecuted(AuditEventBase):
    """MCP query execution per `arch/adapter.md` §11 MCP-Server per-class
    event kinds. `details` carries query type + result count."""

    event_kind: Literal["mcp_query_executed"] = "mcp_query_executed"


class McpCapabilityNegotiated(AuditEventBase):
    """MCP capability negotiation completed per `arch/adapter.md` §11
    MCP-Server per-class event kinds. `details` carries negotiated
    capability set."""

    event_kind: Literal["mcp_capability_negotiated"] = "mcp_capability_negotiated"


class McpOpFailed(AuditEventBase):
    """MCP operation failure per `arch/adapter.md` §11 MCP-Server
    per-class event kinds. `details` carries op + failure category +
    architectural error category mapping (`AdapterError` subclass)."""

    event_kind: Literal["mcp_op_failed"] = "mcp_op_failed"


# ---------------------------------------------------------------------------
# Error categories (§11 cross-class architectural categories +
# MCP-Server per-class refinements)
#
# Cross-class categories per `arch/adapter.md` §11 architectural categories
# table apply to every adapter; per-class refinements extend the cross-
# class set per integration class.
# ---------------------------------------------------------------------------


class AdapterError(Exception):
    """Base for all adapter class errors per `arch/adapter.md` §11.

    Per-shape error semantics (§11 per-shape error semantics + §14
    cross-shape policy variation): practitioner-shape fail-closed
    (defensibility-critical; especially axis-3 send operations);
    autonomous-business-shape fail-open with alert (continuity
    prioritized); personal-OS-shape fail-open (lightweight); federation-
    shape fail-closed within node + fail-open across nodes (pending
    peer recovery).
    """


class AdapterUnreachable(AdapterError):
    """External system unreachable (network / DNS / target down) per
    `arch/adapter.md` §11 cross-class architectural categories."""


class AdapterAuthExpired(AdapterError):
    """Auth tokens expired; refresh required (or refresh failed) per
    `arch/adapter.md` §11 cross-class architectural categories.

    Composes with `AdapterAuthExpiredEvent` (event records the failure
    in audit-trail; this error is raised at refresh-failure site).
    """


class AdapterAuthFailed(AdapterError):
    """Auth refresh attempted; permanent failure (e.g., revoked tokens)
    per `arch/adapter.md` §11 cross-class architectural categories."""


class AdapterQuotaExceeded(AdapterError):
    """API quota / rate-limit hit; back-off required per `arch/adapter.md`
    §11 cross-class architectural categories + §11 rate-limit handling."""


class AdapterCircuitBreakerOpen(AdapterError):
    """Circuit-breaker tripped; recovery probing in progress per
    `arch/adapter.md` §11 cross-class architectural categories + §11
    circuit-breaker semantics."""


class AdapterValidationError(AdapterError):
    """Operation validation failed (impl-side) per `arch/adapter.md` §11
    cross-class architectural categories."""


class AdapterPermissionDenied(AdapterError):
    """Substrate permission flow returned deny per `arch/adapter.md` §11
    cross-class architectural categories.

    Composes with `pbs.substrate.PermissionDenied` (substrate-side
    permission decision) — adapter raises this when its substrate-
    permission request returns `decision == "deny"`.
    """


class AdapterOpFailed(AdapterError):
    """Catch-all impl-native failure not categorized above per
    `arch/adapter.md` §11 cross-class architectural categories."""


# MCP-Server per-class refinements per `arch/adapter.md` §11 per-class
# refinements. `RegistrationConflict` (per substrate Surface §B name
# collision) lives in `pbs.substrate` — MCP-Server adapter callers
# observing registration collisions catch `pbs.substrate.RegistrationConflict`
# rather than redeclaring it here.


class CapabilityMismatch(AdapterError):
    """MCP capability negotiation produced incompatible capability set
    per `arch/adapter.md` §11 MCP-Server per-class refinements."""


class TransportFailure(AdapterError):
    """MCP transport (in-process / subprocess / HTTP) failure per
    `arch/adapter.md` §11 MCP-Server per-class refinements + per
    `arch/substrate.md` §12 transport variation."""


class ToolNotFound(AdapterError):
    """Requested MCP tool not registered with this MCP server per
    `arch/adapter.md` §11 MCP-Server per-class refinements."""


# ---------------------------------------------------------------------------
# Adapter Protocol Surface — META-Surface (cross-class architectural
# conventions every adapter Implementation MUST satisfy per `arch/adapter.md`
# §2 META-Surface)
# ---------------------------------------------------------------------------


@runtime_checkable
class AdapterProtocol(Protocol):
    """The Adapter Pattern A META-Surface (Phase 6.1 Mode 3 spec).

    Per `arch/adapter.md` §6 tri-aspect: Surface (this Protocol +
    per-class Protocols extending it; mechanism layer) + Implementations
    (Framework C distributable definitions wrapping native external-
    integration primitives) + Running Instance(s) (workspace-bound at
    Owner B at boot; multiple simultaneous per `workspace.md` adapter
    bindings list).

    Cardinality (§5 + §9): N per workspace (bounded by `workspace.md`
    adapter bindings; per-shape policy may declare maximum); 1 per
    integration class by default (multi-account mechanics deferred to
    `arch/adapter.md` §16 W4 watch-list).

    Adapter-coupling impossible-by-construction per §6 + `MAINTENANCE.md`
    TOP-LEVEL DESIGN PRINCIPLES §1: skill code targeting per-class
    Surface (e.g., `McpServerAdapterProtocol`) is portable across
    Implementations within that class; skill code reaching Implementation-
    internal primitives is impl-pinned by structural construction (the
    same per-class-Surface-typing-plus-isinstance-check mechanism that
    protects substrate per `arch/substrate.md` §6 protects adapter).

    Per `arch/adapter.md` §2 META-Surface: every adapter Implementation
    must satisfy lifecycle (`from_config` / `is_ready` / `shutdown`) +
    auth (`auth_model` + `refresh_auth`) + permission flow integration
    (via substrate Surface §C composition) + audit emission (via MCP
    audit gate; via composition with audit Surface) + error mapping
    (per §11 categories) + health check (`health_status`) + versioning
    (`version` + `min_substrate_version`).

    Per-class Surfaces (e.g., `McpServerAdapterProtocol`) extend this
    META-Surface adding class-specific capability categories per §2
    per-class capability categories table.
    """

    # ------------------------------------------------------------------
    # Per-instance identity + versioning (META-Surface)
    # ------------------------------------------------------------------

    @property
    def adapter_id(self) -> str:
        """Adapter Implementation identity per `arch/adapter.md` §4."""
        ...

    @property
    def instance_id(self) -> str:
        """Per-binding instance identifier (workspace-unique) per
        `arch/adapter.md` §5."""
        ...

    @property
    def integration_class(self) -> IntegrationClass:
        """Which per-class Surface this Implementation satisfies per
        `arch/adapter.md` §4."""
        ...

    @property
    def version(self) -> str:
        """Implementation semver-like version per `arch/adapter.md` §9
        versioning."""
        ...

    @property
    def auth_model(self) -> AuthModel:
        """Declared auth model per `arch/adapter.md` §10 per-class auth
        models."""
        ...

    @property
    def direction(self) -> AdapterDirection:
        """Per-class architectural direction per `arch/adapter.md` §4
        bidirectional vs unidirectional patterns."""
        ...

    # ------------------------------------------------------------------
    # Lifecycle (§9 + §10 per-instance boot/shutdown sequence)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(cls, config: AdapterConfig) -> "AdapterProtocol":
        """Instantiate adapter Implementation per `arch/adapter.md` §10
        per-instance boot sequence step 2.

        Loads config; validates schema; loads auth state; initializes
        per-impl runtime resources. Returns ready-to-emit-`adapter_started`
        instance (caller emits the audit event after `from_config`
        returns + `is_ready` becomes True).
        """
        ...

    @property
    def is_ready(self) -> bool:
        """True after per-instance boot sequence completes per
        `arch/adapter.md` §10 per-instance boot sequence step 4. Once
        True, adapter operations accessible to skills via per-class
        Surface."""
        ...

    async def shutdown(self) -> None:
        """Adapter shutdown per `arch/adapter.md` §10 per-instance
        shutdown sequence.

        Steps 1-6 per `arch/adapter.md` §10 per-instance shutdown
        sequence:

        1. Drain in-flight adapter operations
        2. Stop accepting new operations
        3. Flush adapter-internal state (auth tokens persisted; circuit
           state captured; threading caches cleaned)
        4. Emit `AdapterStopped` audit event
        5. Per-binding shutdown returns
        6. Workspace's overall shutdown waits for all adapters drained
           per reverse declaration order
        """
        ...

    # ------------------------------------------------------------------
    # Auth surface (§10 auth-refresh lifecycle)
    # ------------------------------------------------------------------

    async def refresh_auth(self) -> None:
        """Refresh adapter auth tokens per `arch/adapter.md` §10
        auth-refresh lifecycle.

        Two trigger contexts (per §10 architectural commitment):

        - **Proactive**: framework calls at 80% of expiry window to
          avoid auth-expired-mid-operation
        - **Reactive**: framework calls on `AdapterAuthExpired` error,
          retries op once before propagating failure

        Emits `AdapterAuthRefreshed` on success.

        Raises:
            AdapterAuthFailed: refresh attempted; permanent failure
                (e.g., revoked tokens). Emits `AdapterAuthExpiredEvent`.
            AdapterUnreachable: auth provider unreachable.
        """
        ...

    # ------------------------------------------------------------------
    # Health check (META-Surface)
    # ------------------------------------------------------------------

    def health_status(self) -> HealthReport:
        """Per-instance health-status query per `arch/adapter.md` §2
        META-Surface "Health check" capability.

        Composes circuit-breaker state (§11) into health verdict
        (`OPEN` → `UNHEALTHY`; `HALF_OPEN` → `DEGRADED`; `CLOSED` +
        recent successes → `HEALTHY`).
        """
        ...

    @property
    def circuit_state(self) -> CircuitState:
        """Per-instance circuit-breaker state per `arch/adapter.md` §11
        circuit-breaker semantics. Read-only; transitions managed
        impl-internally."""
        ...


# ---------------------------------------------------------------------------
# MCP-Server per-class Protocol Surface
#
# Per `arch/adapter.md` §2 per-class capability categories table for
# MCP-Server: tool registration (per substrate Surface §B; transport
# selection in-process / subprocess / HTTP) + capability negotiation +
# tool invocation.
#
# Per `arch/adapter.md` §2: per-class Surfaces are NOT extension Protocols
# — every implementation in a class MUST satisfy that class's Surface.
#
# Phase 6.1 covers MCP-Server class only; Email / Accounting / A2A-Peer /
# File-Sync per-class Surface Protocols deferred to Phase 6.2.
# ---------------------------------------------------------------------------


@runtime_checkable
class McpServerAdapterProtocol(AdapterProtocol, Protocol):
    """MCP-Server per-class Surface (Phase 6.1 Mode 3 spec).

    Per `arch/adapter.md` §2 MCP-Server Adapter Surface row: tool
    registration (per `arch/substrate.md` Surface §B; transport
    selection per `pbs.substrate.TransportMode`) + capability
    negotiation + tool invocation.

    Composes with substrate Surface §B per `arch/adapter.md` §7
    composition with framework primitives. The MCP-Server adapter
    instance registers itself as an MCP server with the workspace's
    substrate at boot via `register_with_substrate()`; once registered,
    skills + specialists discover this MCP server via substrate Surface
    §B (`substrate.discover_mcp_servers()` / `substrate.list_tools()`)
    and invoke its tools either directly through substrate or through
    `invoke_tool()` on this Protocol.

    Phase 6.1 reference impl: `pbs/impls/mcp_server_adapter.py`
    (forthcoming) satisfies this Protocol via the MCP stdio /
    in-process / HTTP transports per `pbs.substrate.TransportMode`.
    """

    # ------------------------------------------------------------------
    # Tool registration (composes with substrate Surface §B)
    # ------------------------------------------------------------------

    async def register_with_substrate(
        self,
        substrate: SubstrateProtocol,
        transport: TransportMode,
    ) -> None:
        """Register this MCP server with the workspace's substrate per
        `arch/adapter.md` §2 MCP-Server Adapter Surface tool registration
        + `arch/substrate.md` §2.B MCP server registration + §12 transport
        variation.

        Calls `substrate.register_mcp_server(name, transport, config)`
        with this adapter's identity + selected transport. Substrate may
        degrade transport per per-impl support (fallback emits
        `mcp_server_registration_fallback` audit event with details per
        `arch/substrate.md` §8).

        Raises:
            pbs.substrate.RegistrationConflict: name collision OR
                transport unavailable (after substrate fallback attempts
                exhausted).
            TransportFailure: transport-level connection failure (e.g.,
                subprocess spawn failed; HTTP unreachable).
            AdapterUnreachable: MCP server itself unreachable.
        """
        ...

    # ------------------------------------------------------------------
    # Capability negotiation
    # ------------------------------------------------------------------

    async def negotiate_capabilities(self) -> Mapping[str, Any]:
        """Negotiate MCP capabilities with the connected MCP server per
        `arch/adapter.md` §2 MCP-Server Adapter Surface capability
        negotiation.

        Returns the agreed-upon capability set (tool catalog version;
        prompt support; resource support; sampling support; etc. per
        MCP protocol). Emits `McpCapabilityNegotiated` audit event with
        negotiated capability set in `details`.

        Raises:
            CapabilityMismatch: incompatible capability set (e.g., MCP
                server lacks tools required by this adapter).
            TransportFailure: transport-level failure during negotiation.
            AdapterUnreachable: MCP server unreachable mid-negotiation.
        """
        ...

    # ------------------------------------------------------------------
    # Tool invocation
    # ------------------------------------------------------------------

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Mapping[str, Any],
    ) -> Any:
        """Invoke a tool on the connected MCP server per `arch/adapter.md`
        §2 MCP-Server Adapter Surface tool invocation.

        Emits `McpToolInvoked` audit event with `tool_name` + argument
        shape + result hash in `details`.

        Pre-implementation operational concerns (Phase 6 forward-reference
        per `arch/adapter.md` §15): retry policies; timeouts; result
        streaming; per-tool quota tracking. Reference impl handles per
        Phase 6 spec.

        Raises:
            ToolNotFound: `tool_name` not registered with this MCP
                server.
            TransportFailure: transport-level failure during invocation.
            AdapterUnreachable: MCP server unreachable.
            AdapterQuotaExceeded: per-tool quota exhausted (where
                applicable).
            AdapterValidationError: arguments failed MCP server's
                validation.
            McpOpFailed: catch-all MCP-side failure not categorized
                above (emits `McpOpFailed` audit event).
        """
        ...

    def list_tools(self) -> list[str]:
        """List tools available on the connected MCP server per
        `arch/adapter.md` §2 MCP-Server Adapter Surface tool invocation.

        Returns the tool-name catalog as known to this adapter (cached
        from last `negotiate_capabilities()` call OR refreshed per
        impl-internal policy)."""
        ...
