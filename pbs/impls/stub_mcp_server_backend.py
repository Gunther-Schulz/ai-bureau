"""Stub MCP server backend — Phase 6.1 reference impl.

Per `BACKLOG.md` §226 + `HANDOFF.md` Note 80 close: minimum-viable
filesystem-backed MCP server backend exercising the §224 mechanism set
end-to-end. Production backend (LanceDB + fastembed + bge-m3 + LaTeX
compile wrapper) deferred to Phase 6.2 per `BACKLOG.md` §248.

What this is:

- An MCP server (in the substrate Surface §B sense — registerable via
  `substrate.register_mcp_server`) exposing 3 MCP tools that compose
  with the §224 mechanism impl set:
    - `read_entity(entity_kind, entity_id)` → entity payload
    - `write_entity(entity_kind, entity_id, payload)` → ack with status
    - `record_audit_event(event_payload)` → ack (forwards to audit
      Surface §A `emit()`)
- Filesystem-backed entity persistence under `<workspace_root>/entities/
  <kind>/<id>.json` (JSON serialization for runtime entities; Mode 1
  human-authored deployment-instance content (workspace.md / practitioner-
  RECORD.md / shape policy bundle / specialist DEFINITION) is read by
  substrate at boot — NOT via this backend per `BACKLOG.md` §227 scope
  distinction)
- Skill-side MCP audit gate path: `record_audit_event` reconstructs an
  `AuditEventBase` from the wire dict + forwards to the injected audit
  Implementation's `emit()` per `arch/audit.md` §8 dual-emission. Closes
  the §8 dual-emission target gap noted in Notes 77 / 78 / 79 / 80 as
  Phase 6.1 → "Phase 6.2 wires actual MCP audit gate" — this batch
  makes that wiring real at Phase 6.1.

What this is NOT:

- NOT a production backend (no LanceDB / fastembed / RAG retrieval —
  deferred to Phase 6.2 per `BACKLOG.md` §248)
- NOT the audit storage tier (audit storage realization owns the audit-
  trail file path per `arch/audit.md` §9 lifecycle ownership; this
  backend FORWARDS events to it)
- NOT a permission gate (entity writes are unconditional at Phase 6.1;
  authority-binding mechanism gates AT audit Surface §A emission per
  `pbs/impls/practitioner_shape_authority_binding.py` Note 79 — wiring
  AuthorityChecker into `write_entity` would re-introduce the cross-
  cutting concern at the wrong layer; Phase 6.2 may surface specific
  need)
- NOT multi-workspace (single `workspace_root` config; multi-workspace
  persistence schema is W3 deferred to Phase 6.2 per `arch/scope-model.md`)

Composition with §224 mechanism-impl set:

- `pbs/impls/claude_agent_sdk_substrate.py` — backend registers via
  `register_with_substrate(substrate, transport=IN_PROCESS)` calling
  `substrate.register_mcp_server(name, transport, config)` per
  `arch/substrate.md` §2.B; substrate emits `mcp_server_registered`
  authoritative event from its end (this backend does NOT emit a
  separate registration event — avoiding double-emission per
  `pbs/impls/mcp_server_adapter.py` precedent)
- `pbs/impls/mcp_server_adapter.py` — Phase 6.2 wiring point: the
  adapter becomes a CLIENT of this backend (adapter `invoke_tool`
  currently raises `NotImplementedError`); Phase 6.1 deployment-
  instance code calls the backend's typed methods directly OR via
  the `invoke_tool` dispatcher
- `pbs/impls/claude_agent_sdk_audit.py` — backend's `record_audit_event`
  reconstructs `AuditEventBase` from the wire dict per the same
  collapsed-promotion convention as `claude_agent_sdk_audit.py`
  `_reconstruct_base` + calls the injected audit Implementation's
  `emit()`; backend itself does NOT own audit-trail storage
- `pbs/impls/practitioner_shape_authority_binding.py` — composes via
  the audit Implementation's `AuthorityChecker` injection: backend's
  `record_audit_event` triggers audit's authority validation per
  `arch/audit.md` §11 (no separate authority gating at backend layer)

Phase 6 wiring points (marked explicitly in docstrings):

- Real MCP wire protocol (subprocess stdio per `TransportMode.SUBPROCESS`
  / HTTP per `TransportMode.HTTP`); reference impl uses `IN_PROCESS`
  exclusively at Phase 6.1; deployment-instance code holds the backend
  instance in-process and invokes its typed methods OR `invoke_tool`
  dispatcher directly
- Per-entity-kind typed Pydantic deserialization (currently dict
  passthrough on the wire; Phase 6.2 may resolve to `pbs.manifests.*`
  typed entities at backend boundary)
- Multi-workspace persistence schema per `arch/scope-model.md` W3
- LanceDB / fastembed / bge-m3 production backend per `BACKLOG.md` §248

Foundation-up: imports from `pbs.audit` (AuditProtocol Surface) +
`pbs.substrate` (SubstrateProtocol + TransportMode) + `pbs.types.*`
(AuditEventBase + ActorKind); no reverse imports; backend impl peer-
import-free with all §224 mechanism impls (composition is via injection
+ structural Surface satisfaction).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from pbs.audit import AuditProtocol
from pbs.substrate import SubstrateProtocol, TransportMode
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------


BACKEND_ID: Final[Literal["stub_mcp_server_backend"]] = "stub_mcp_server_backend"
"""Stable backend identity per `arch/audit.md` §2.A actor identity
convention. Used as the `actor_id` on backend-self-emitted events
(boot / shutdown markers); skill-emitted events forwarded via
`record_audit_event` carry the originating skill's own actor_id from
the wire dict."""


VERSION: Final[str] = "0.1.0"
"""Phase 6.1 reference-impl version per `BACKLOG.md` §226 thin-slice."""


DEFAULT_ENTITY_KINDS: Final[frozenset[str]] = frozenset(
    {
        "workflow_instance",
        "work_unit_instance",
        "claim",
    }
)
"""Default supported entity kinds at Phase 6.1 thin-slice — the three
runtime-emitted entities per `pbs/manifests/`. Mode 1 human-authored
deployment-instance content (workspace.md / practitioner-RECORD.md /
shape policy bundle / specialist DEFINITION) is read by substrate
directly at boot per `BACKLOG.md` §227 scope. Per-deployment may extend
via `StubMcpServerBackendConfig.supported_entity_kinds`."""


ENTITY_DIRNAME: Final[str] = "entities"
"""Subdirectory under `workspace_root` holding per-kind entity JSON
files. Layout: `<workspace_root>/entities/<kind>/<id>.json`. Phase 6.2
production backend may parameterize via deployment config."""


TOOL_NAMES: Final[frozenset[str]] = frozenset(
    {
        "read_entity",
        "write_entity",
        "record_audit_event",
    }
)
"""The 3 MCP tools this backend exposes. `invoke_tool(tool_name,
arguments)` dispatcher accepts only these names; unknown tool_names
raise `StubMcpServerBackendToolError`."""


# ---------------------------------------------------------------------------
# Error categories
# ---------------------------------------------------------------------------


class StubMcpServerBackendError(Exception):
    """Base for all stub-MCP-server-backend errors per `BACKLOG.md` §226
    thin-slice. Phase 6.2 production backend introduces its own error
    hierarchy; this category exists for Phase 6.1 uniform error surface."""


class StubMcpServerBackendUnreachable(StubMcpServerBackendError):
    """Backend not in ready state (pre-boot OR post-shutdown). All tool
    invocations raise this when `is_ready=False`."""


class EntityKindUnsupportedError(StubMcpServerBackendError):
    """Requested `entity_kind` not in `supported_entity_kinds` per
    config. Phase 6.1 thin-slice ships 3-kind default
    (workflow_instance / work_unit_instance / claim); deployment may
    extend via config."""


class EntityNotFoundError(StubMcpServerBackendError):
    """`read_entity(kind, id)` could not find the requested entity at
    `<workspace_root>/entities/<kind>/<id>.json`. Distinct from disk-IO
    errors which surface as `StubMcpServerBackendStorageError`."""


class EntityValidationError(StubMcpServerBackendError):
    """`write_entity` payload validation failed. Phase 6.1 thin-slice
    rejects non-mapping payloads + empty entity_id; Phase 6.2 may layer
    per-kind Pydantic deserialization here."""


class StubMcpServerBackendStorageError(StubMcpServerBackendError):
    """Filesystem operation failed (permission denied / disk full / path
    not writable). Distinct from `EntityNotFoundError` (the expected
    miss path) per Phase 6.1 fail-loud thin-slice."""


class StubMcpServerBackendToolError(StubMcpServerBackendError):
    """Unknown `tool_name` in `invoke_tool` dispatch (not in `TOOL_NAMES`).
    Phase 6.2 may surface tool-extension via deployment config."""


class AuditEventValidationError(StubMcpServerBackendError):
    """`record_audit_event` payload could not be reconstructed as
    `AuditEventBase` per `pbs/types/event_base.py` schema. Required
    fields: event_kind / timestamp / actor_kind / actor_id; per-event-
    kind promoted fields fold back into `details` per the reconstruction
    convention (`pbs/impls/claude_agent_sdk_audit.py` `_reconstruct_base`
    pattern)."""


# ---------------------------------------------------------------------------
# Backend self-emitted event-kinds (boot/shutdown markers)
# ---------------------------------------------------------------------------


class StubBackendBooted(AuditEventBase):
    """Backend boot marker emitted at end of `from_config_with_audit`.
    Per `arch/audit.md` §10 audit-phase boot ordering: audit-phase 1-3
    ready BEFORE this event emits. Phase 6.1 backend-self-emission
    (substrate `mcp_server_registered` is the substrate-authoritative
    registration event; this event records the backend's own readiness
    independent of registration timing).
    """

    event_kind: Literal["stub_backend_booted"] = "stub_backend_booted"


class StubBackendShutdown(AuditEventBase):
    """Backend shutdown marker emitted at start of `shutdown()`. Per
    `arch/audit.md` §10 shutdown ordering: backend shuts down BEFORE
    audit storage realization; this event records the backend's
    shutdown-initiation moment with audit still ready to receive.
    """

    event_kind: Literal["stub_backend_shutdown"] = "stub_backend_shutdown"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class StubMcpServerBackendConfig(BaseModel):
    """Per-deployment configuration for the stub MCP server backend.

    Per `BACKLOG.md` §226 thin-slice: filesystem-backed entity persistence
    under `<workspace_root>/entities/<kind>/<id>.json`. Production
    backend (LanceDB / fastembed / RAG retrieval) is Phase 6.2.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    workspace_root: Path
    """Filesystem root for entity persistence. Backend creates
    `<workspace_root>/entities/<kind>/` subdirectories on first write
    per kind. Per `arch/scope-model.md` W3 (multi-workspace persistence
    schema deferred Phase 6.2), Phase 6.1 thin-slice assumes single-
    workspace deployment."""

    supported_entity_kinds: frozenset[str] = Field(
        default_factory=lambda: frozenset(DEFAULT_ENTITY_KINDS),
    )
    """Per-deployment entity-kind catalog. Phase 6.1 default is the 3
    runtime-emitted kinds (workflow_instance / work_unit_instance /
    claim); deployment may extend (e.g., `practitioner` / `specialist`)
    if it chooses to back human-authored entities through the same
    backend rather than substrate-direct reads."""

    audit_event_kind_allowlist: frozenset[str] | None = None
    """Optional skill-side MCP audit gate event_kind allowlist. Default
    None = forward all reconstructable `AuditEventBase` emissions to the
    injected audit Implementation; non-None = backend-side pre-filter
    rejecting unlisted event_kinds with `AuditEventValidationError`.
    Phase 6.2 may align with audit `mandatory_catalog` enforcement per
    `arch/audit.md` §2.E."""


# ---------------------------------------------------------------------------
# StubMcpServerBackend — Implementation class
# ---------------------------------------------------------------------------


class StubMcpServerBackend:
    """Stub MCP server backend per `BACKLOG.md` §226 thin-slice.

    Phase 6.1 minimum-viable filesystem-backed MCP server exposing 3 MCP
    tools (`read_entity` / `write_entity` / `record_audit_event`) that
    compose with the §224 mechanism-impl set end-to-end. Production
    backend (LanceDB + fastembed + bge-m3 + LaTeX) deferred to Phase 6.2.

    Surface satisfaction is structural — there is no `BackendProtocol`
    at Phase 6.1 (only one backend impl exists; YAGNI per Phase 6.1
    thin-slice). Phase 6.2 production backend MAY motivate a typed
    Protocol; until then, deployment-instance code consumes typed
    methods (`read_entity` / `write_entity` / `record_audit_event`) OR
    the `invoke_tool` dispatcher.

    Lifecycle (matches the §224 mechanism-impl boot/shutdown convention):

    - Boot via `from_config_with_audit(config, audit)` — async factory;
      validates audit Implementation injection + workspace_root parent
      directory existence; creates `<workspace_root>/entities/`
      subdirectory if absent; emits `stub_backend_booted` through the
      injected audit
    - `register_with_substrate(substrate, transport=IN_PROCESS)` —
      optional registration step calling `substrate.register_mcp_server`
      per `arch/substrate.md` §2.B; substrate emits the authoritative
      `mcp_server_registered` event from its end
    - Tool invocation via `read_entity` / `write_entity` /
      `record_audit_event` typed methods OR `invoke_tool(tool_name,
      arguments)` dispatcher (MCP-protocol-shaped surface)
    - `shutdown()` is idempotent — emits `stub_backend_shutdown` BEFORE
      flipping `is_ready=False` so audit Surface §A still accepts the
      event during the backend's own shutdown initiation moment

    State (instance-private):

    - `_config`: per-deployment config (workspace_root + supported kinds
      + allowlist)
    - `_audit`: injected `AuditProtocol` Implementation (Note 76
      `ClaudeAgentSDKAudit` at Phase 6.1 default)
    - `_instance_id`: stable per-Instance identity (matches §224
      mechanism-impl `actor_id` convention)
    - `_substrate`: substrate reference post-`register_with_substrate`
      (None pre-registration; remains None if backend used standalone)
    - `_registered_transport`: transport selected at registration (None
      pre-registration)
    - `_is_ready`: True between construction and shutdown
    - `_is_shutting_down`: idempotent guard for repeated shutdown calls
    """

    def __init__(
        self,
        config: StubMcpServerBackendConfig,
        audit: AuditProtocol,
    ) -> None:
        """Internal constructor. Use `from_config_with_audit()` factory."""
        self._config = config
        self._audit = audit
        self._instance_id: str = f"{BACKEND_ID}:{uuid4()}"
        self._substrate: SubstrateProtocol | None = None
        self._registered_transport: TransportMode | None = None
        self._is_ready: bool = False
        self._is_shutting_down: bool = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @classmethod
    async def from_config_with_audit(
        cls,
        config: StubMcpServerBackendConfig,
        audit: AuditProtocol,
    ) -> StubMcpServerBackend:
        """Boot per `BACKLOG.md` §226 + the §224 mechanism-impl factory
        convention (`pbs/impls/practitioner_shape_authority_binding.py`
        / `pbs/impls/practitioner_shape_sparring.py` precedent).

        Precondition: audit-phase 1-3 ready (the backend emits
        `stub_backend_booted` through `audit.emit` at end of construction);
        substrate-phase 1+ may proceed in parallel — registration is a
        separate step via `register_with_substrate()`.

        Validation:
        - `audit` must satisfy `AuditProtocol` structurally (runtime check
          via `isinstance` is the Surface contract per `pbs/audit.py`)
        - `config.workspace_root.parent` must exist + be writable;
          backend creates `<workspace_root>/entities/` if absent

        Raises:
            StubMcpServerBackendStorageError: workspace_root parent
                missing OR not writable.
        """
        if not isinstance(audit, AuditProtocol):
            raise StubMcpServerBackendStorageError(
                "StubMcpServerBackend requires an AuditProtocol-conforming "
                "audit Implementation; received non-conforming object."
            )
        parent = config.workspace_root.parent
        if not parent.exists():
            raise StubMcpServerBackendStorageError(
                f"workspace_root parent {parent} does not exist; backend "
                f"cannot create the workspace_root directory beneath a "
                f"missing parent."
            )
        config.workspace_root.mkdir(parents=True, exist_ok=True)
        entities_dir = config.workspace_root / ENTITY_DIRNAME
        try:
            entities_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise StubMcpServerBackendStorageError(
                f"Could not create entities directory {entities_dir}: {exc}"
            ) from exc

        instance = cls(config, audit)
        instance._is_ready = True
        instance._audit.emit(
            StubBackendBooted(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=instance._instance_id,
                timestamp=datetime.now(tz=UTC),
                details={
                    "backend_id": BACKEND_ID,
                    "version": VERSION,
                    "workspace_root": str(config.workspace_root),
                    "supported_entity_kinds": sorted(
                        config.supported_entity_kinds
                    ),
                },
            )
        )
        return instance

    @property
    def is_ready(self) -> bool:
        return self._is_ready and not self._is_shutting_down

    @property
    def instance_id(self) -> str:
        """Stable per-Instance identity. Used as `actor_id` on backend-
        self-emitted events; deployment-instance code may also use this
        as the substrate registration `name` to keep events + registration
        record traceable."""
        return self._instance_id

    @property
    def is_registered(self) -> bool:
        """True if `register_with_substrate()` succeeded; False otherwise.
        Backend may be used standalone (no registration) at Phase 6.1
        thin-slice — registration is not a precondition for tool
        invocation."""
        return self._substrate is not None

    async def shutdown(self) -> None:
        """Idempotent shutdown per `arch/audit.md` §10 shutdown ordering.

        Emits `stub_backend_shutdown` BEFORE flipping `is_ready=False`
        so the audit Implementation still accepts the event during the
        backend's own shutdown-initiation moment. After this returns,
        all tool invocations raise `StubMcpServerBackendUnreachable`.

        Audit Implementation shutdown is the responsibility of the
        deployment-instance composition root (per
        `pbs/impls/claude_agent_sdk_audit.py` `shutdown()` ordering — the
        audit storage realization shuts down LAST).
        """
        if self._is_shutting_down:
            return
        if self._is_ready:
            self._audit.emit(
                StubBackendShutdown(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id,
                    timestamp=datetime.now(tz=UTC),
                    details={
                        "backend_id": BACKEND_ID,
                        "is_registered": self.is_registered,
                    },
                )
            )
        self._is_shutting_down = True
        self._is_ready = False

    # ------------------------------------------------------------------
    # Substrate registration (per `arch/substrate.md` §2.B)
    # ------------------------------------------------------------------

    async def register_with_substrate(
        self,
        substrate: SubstrateProtocol,
        transport: TransportMode = TransportMode.IN_PROCESS,
    ) -> None:
        """Register this backend with the substrate per
        `arch/substrate.md` §2.B + §12 transport variation.

        Phase 6.1 thin-slice: `IN_PROCESS` transport only (the backend
        instance is held in-process by the deployment composition root
        + tool invocations dispatch via this object's typed methods OR
        `invoke_tool`). Phase 6.2 wires `SUBPROCESS` (stdio framing) +
        `HTTP` (MCP-over-HTTP) transports per per-deployment substrate
        impl support.

        Substrate emits the authoritative `mcp_server_registered` event
        from its end; this backend does NOT emit a separate registration
        event (avoids double-emission per
        `pbs/impls/mcp_server_adapter.py` `register_with_substrate`
        precedent).

        Raises:
            StubMcpServerBackendUnreachable: backend not in ready state
                OR shutting down.
            pbs.substrate.RegistrationConflict: substrate-side name
                collision (propagated from
                `substrate.register_mcp_server`).
        """
        if not self.is_ready:
            raise StubMcpServerBackendUnreachable(
                f"StubMcpServerBackend {self._instance_id} not ready; "
                f"cannot register with substrate."
            )
        await substrate.register_mcp_server(
            name=self._instance_id,
            transport=transport,
            config={
                "backend_id": BACKEND_ID,
                "version": VERSION,
                "workspace_root": str(self._config.workspace_root),
                "supported_entity_kinds": sorted(
                    self._config.supported_entity_kinds
                ),
                "tools": sorted(TOOL_NAMES),
            },
        )
        self._substrate = substrate
        self._registered_transport = transport

    # ------------------------------------------------------------------
    # Tool 1 — read_entity
    # ------------------------------------------------------------------

    async def read_entity(
        self,
        entity_kind: str,
        entity_id: str,
    ) -> dict[str, Any]:
        """Read a persisted entity payload from the filesystem store.

        Path: `<workspace_root>/entities/<entity_kind>/<entity_id>.json`.
        Phase 6.1 thin-slice returns the raw JSON-deserialized dict; per-
        kind typed Pydantic deserialization is a Phase 6.2 wiring point.

        Raises:
            StubMcpServerBackendUnreachable: backend not in ready state.
            EntityKindUnsupportedError: entity_kind not in
                `supported_entity_kinds`.
            EntityNotFoundError: file does not exist at expected path.
            StubMcpServerBackendStorageError: disk-IO error OR file
                contents are not valid JSON.
        """
        self._require_ready("read_entity")
        self._validate_entity_kind(entity_kind)
        if not entity_id:
            raise EntityValidationError(
                "read_entity: entity_id must be non-empty."
            )
        path = self._entity_path(entity_kind, entity_id)
        if not path.exists():
            raise EntityNotFoundError(
                f"Entity not found: kind={entity_kind} id={entity_id} "
                f"path={path}"
            )
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise StubMcpServerBackendStorageError(
                f"read_entity: filesystem read failed at {path}: {exc}"
            ) from exc
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise StubMcpServerBackendStorageError(
                f"read_entity: file at {path} is not valid JSON: {exc}"
            ) from exc
        if not isinstance(payload, dict):
            raise StubMcpServerBackendStorageError(
                f"read_entity: file at {path} did not deserialize to a "
                f"JSON object (got {type(payload).__name__})."
            )
        return {
            "entity_kind": entity_kind,
            "entity_id": entity_id,
            "payload": payload,
        }

    # ------------------------------------------------------------------
    # Tool 2 — write_entity
    # ------------------------------------------------------------------

    async def write_entity(
        self,
        entity_kind: str,
        entity_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Persist an entity payload to the filesystem store.

        Path: `<workspace_root>/entities/<entity_kind>/<entity_id>.json`.
        Per-kind subdirectory is created on first write for that kind.
        JSON serialization with `indent=2` for human readability +
        diff-friendliness; the deployment composition root is responsible
        for atomic-write semantics if cross-process concurrency surfaces
        at Phase 6.2.

        Phase 6.1 thin-slice does NOT route through authority-binding
        (entity writes are unconditional at this layer); authority-
        binding gates AT audit Surface §A emission per
        `pbs/impls/practitioner_shape_authority_binding.py` Note 79.

        Raises:
            StubMcpServerBackendUnreachable: backend not in ready state.
            EntityKindUnsupportedError: entity_kind not in
                `supported_entity_kinds`.
            EntityValidationError: empty entity_id OR non-mapping payload.
            StubMcpServerBackendStorageError: disk-IO error OR JSON
                serialization failure.
        """
        self._require_ready("write_entity")
        self._validate_entity_kind(entity_kind)
        if not entity_id:
            raise EntityValidationError(
                "write_entity: entity_id must be non-empty."
            )
        if not isinstance(payload, dict):
            raise EntityValidationError(
                f"write_entity: payload must be a JSON-object-shaped dict; "
                f"received {type(payload).__name__}."
            )
        path = self._entity_path(entity_kind, entity_id)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise StubMcpServerBackendStorageError(
                f"write_entity: could not create kind directory "
                f"{path.parent}: {exc}"
            ) from exc
        try:
            serialized = json.dumps(payload, indent=2, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise StubMcpServerBackendStorageError(
                f"write_entity: payload not JSON-serializable for "
                f"kind={entity_kind} id={entity_id}: {exc}"
            ) from exc
        try:
            path.write_text(serialized, encoding="utf-8")
        except OSError as exc:
            raise StubMcpServerBackendStorageError(
                f"write_entity: filesystem write failed at {path}: {exc}"
            ) from exc
        return {
            "status": "ok",
            "entity_kind": entity_kind,
            "entity_id": entity_id,
            "path": str(path),
            "byte_count": len(serialized.encode("utf-8")),
        }

    # ------------------------------------------------------------------
    # Tool 3 — record_audit_event (skill-side MCP audit gate)
    # ------------------------------------------------------------------

    async def record_audit_event(
        self,
        event_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Skill-side MCP audit gate per `arch/audit.md` §8 dual-emission.

        Reconstructs `AuditEventBase` from the wire dict per the
        collapsed-promotion convention (`pbs/impls/claude_agent_sdk_audit.
        py` `_reconstruct_base` precedent: subclass-promoted fields fold
        back into `details`) + forwards to the injected audit
        Implementation's `emit()`. The audit Impl handles append-only
        storage + hash-chain integrity + authority-binding validation
        per `arch/audit.md` §2 — backend is the GATE, not the storage.

        Wire format: `event_payload` is a JSON-object dict matching
        `AuditEventBase` schema (event_kind / timestamp / actor_kind /
        actor_id / optional session_id / work_unit_id / workflow_
        instance_id / claim_id / substrate_kind / details). Per-event-
        kind subclass-specific fields outside `AuditEventBase.model_
        fields` fold back into `details` so the gate remains schema-
        uniform; the audit Implementation may surface them on read-back
        via the same convention.

        Raises:
            StubMcpServerBackendUnreachable: backend not in ready state.
            AuditEventValidationError: payload not reconstructable as
                `AuditEventBase` OR event_kind not in allowlist (when
                `audit_event_kind_allowlist` is configured).
            (Audit-class errors propagate unchanged: `AuditWriteError` /
             `AuditAppendOnlyViolation` / `AuditSchemaError` /
             `AuditCatalogError` / `AuditTrustError` per `arch/audit.md`
             §11.)
        """
        self._require_ready("record_audit_event")
        if not isinstance(event_payload, dict):
            raise AuditEventValidationError(
                f"record_audit_event: event_payload must be a dict; "
                f"received {type(event_payload).__name__}."
            )
        event_kind = event_payload.get("event_kind")
        if not isinstance(event_kind, str) or not event_kind:
            raise AuditEventValidationError(
                "record_audit_event: event_payload['event_kind'] must be "
                "a non-empty string."
            )
        allowlist = self._config.audit_event_kind_allowlist
        if allowlist is not None and event_kind not in allowlist:
            raise AuditEventValidationError(
                f"record_audit_event: event_kind '{event_kind}' not in "
                f"backend allowlist; deployment-instance allowlist "
                f"configured to gate skill-side emissions."
            )
        event = self._reconstruct_audit_event(event_payload)
        self._audit.emit(event)
        return {
            "status": "ok",
            "event_kind": event_kind,
            "actor_kind": event.actor_kind.value,
            "actor_id": event.actor_id,
        }

    # ------------------------------------------------------------------
    # MCP-protocol-shaped tool dispatcher
    # ------------------------------------------------------------------

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """MCP-protocol-shaped dispatch surface per `arch/adapter.md` §2
        MCP-Server tool invocation contract.

        Phase 6.1 reference impl dispatches `tool_name` to the typed
        method; Phase 6.2 production wiring (real MCP transport) wraps
        this dispatcher in subprocess-stdio / HTTP marshalling.

        Tool argument conventions:
        - `read_entity`: arguments = {entity_kind, entity_id}
        - `write_entity`: arguments = {entity_kind, entity_id, payload}
        - `record_audit_event`: arguments = {event} (the AuditEventBase-
          shaped dict)

        Raises:
            StubMcpServerBackendUnreachable: backend not in ready state.
            StubMcpServerBackendToolError: tool_name not in `TOOL_NAMES`.
            (Per-tool errors propagate unchanged.)
        """
        self._require_ready("invoke_tool")
        if tool_name not in TOOL_NAMES:
            raise StubMcpServerBackendToolError(
                f"invoke_tool: unknown tool_name '{tool_name}'; expected "
                f"one of {sorted(TOOL_NAMES)}."
            )
        if tool_name == "read_entity":
            return await self.read_entity(
                entity_kind=str(arguments.get("entity_kind", "")),
                entity_id=str(arguments.get("entity_id", "")),
            )
        if tool_name == "write_entity":
            payload = arguments.get("payload")
            if not isinstance(payload, dict):
                raise EntityValidationError(
                    "invoke_tool('write_entity'): arguments['payload'] "
                    "must be a JSON-object-shaped dict."
                )
            return await self.write_entity(
                entity_kind=str(arguments.get("entity_kind", "")),
                entity_id=str(arguments.get("entity_id", "")),
                payload=payload,
            )
        # tool_name == "record_audit_event"
        event = arguments.get("event")
        if not isinstance(event, dict):
            raise AuditEventValidationError(
                "invoke_tool('record_audit_event'): arguments['event'] "
                "must be a dict matching AuditEventBase schema."
            )
        return await self.record_audit_event(event_payload=event)

    def list_tools(self) -> list[str]:
        """Per `arch/adapter.md` §2 MCP-Server tool catalog. Returns the
        backend's supported tool names sorted alphabetically. Phase 6.2
        production backend may extend per deployment config (e.g.,
        retrieval / ingestion tools when LanceDB lands)."""
        return sorted(TOOL_NAMES)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _require_ready(self, op_name: str) -> None:
        """Per-operation precondition gate. Raises
        `StubMcpServerBackendUnreachable` if backend not in ready state."""
        if not self.is_ready:
            raise StubMcpServerBackendUnreachable(
                f"StubMcpServerBackend {self._instance_id} not in ready "
                f"state; {op_name} rejected."
            )

    def _validate_entity_kind(self, entity_kind: str) -> None:
        """Per-deployment entity-kind catalog gate."""
        if not entity_kind:
            raise EntityKindUnsupportedError(
                "entity_kind must be non-empty."
            )
        if entity_kind not in self._config.supported_entity_kinds:
            raise EntityKindUnsupportedError(
                f"entity_kind '{entity_kind}' not in supported set "
                f"{sorted(self._config.supported_entity_kinds)}."
            )

    def _entity_path(self, entity_kind: str, entity_id: str) -> Path:
        """Resolve the filesystem path for a given (kind, id). Layout
        per module-level `ENTITY_DIRNAME` convention."""
        return (
            self._config.workspace_root
            / ENTITY_DIRNAME
            / entity_kind
            / f"{entity_id}.json"
        )

    def _reconstruct_audit_event(
        self,
        raw: dict[str, Any],
    ) -> AuditEventBase:
        """Collapse subclass-promoted fields back into `AuditEventBase`
        per the same convention as
        `pbs/impls/claude_agent_sdk_audit.py` `_reconstruct_base`.

        Subclass-specific fields (those not in `AuditEventBase.model_
        fields`) merge into the base `details` dict so the audit
        Implementation receives a uniform schema. The wire format is
        kept liberal at the gate boundary; the audit storage realization
        owns strict validation per `arch/audit.md` §11.

        Raises:
            AuditEventValidationError: payload could not validate as
                `AuditEventBase`.
        """
        base_field_names = set(AuditEventBase.model_fields.keys())
        base_data: dict[str, Any] = {}
        promoted: dict[str, Any] = {}
        for key, value in raw.items():
            if key in base_field_names:
                base_data[key] = value
            else:
                promoted[key] = value
        if promoted:
            details_value = base_data.get("details") or {}
            if not isinstance(details_value, dict):
                raise AuditEventValidationError(
                    f"record_audit_event: 'details' field must be a "
                    f"dict; received {type(details_value).__name__}."
                )
            merged_details = dict(details_value)
            merged_details.update(promoted)
            base_data["details"] = merged_details
        try:
            return AuditEventBase.model_validate(base_data)
        except Exception as exc:  # noqa: BLE001
            raise AuditEventValidationError(
                f"record_audit_event: payload could not be reconstructed "
                f"as AuditEventBase: {exc}"
            ) from exc


# ---------------------------------------------------------------------------
# Convenience helpers (per `pbs/impls/practitioner_shape_sparring.py`
# `practitioner_shape_default_actor_id` / `practitioner_shape_default_policy`
# precedent — convenience constructors for canonical Phase 6.1 thin-slice
# defaults)
# ---------------------------------------------------------------------------


def stub_mcp_server_backend_default_actor_id() -> str:
    """Convenience constructor for backend per-Instance `actor_id`
    matching the §224 mechanism-impl convention. Generates a stable
    UUID-suffixed identity used for backend-self-emitted events
    (`stub_backend_booted` / `stub_backend_shutdown`).

    Note: the typical path is to use `backend.instance_id` after
    construction (the constructor allocates the UUID); this helper
    exists for pre-construction identity preview (e.g., when
    deployment composition root needs the registration name BEFORE
    the backend is instantiated, which is rare at Phase 6.1 thin-
    slice).
    """
    return f"{BACKEND_ID}:{uuid4()}"
