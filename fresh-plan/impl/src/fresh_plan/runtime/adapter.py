"""Adapter runtime — D16 + adapter.schema.json + D29 protocol-identifier registration.

Per D16, adapters integrate a workspace with external surfaces via a single
protocol-or-transport (extension-registered per D2 strict reading + D29
namespacing). `Adapter` is the base class reading off D16; concrete adapter
impls subclass it.

The base supports the **request/response invocation shape** (per D16's
"request/response tool" pattern) via `call(tool_name, parameters)`.
Delegation peer + passive event source patterns may require alternative
invocation interfaces — re-evaluate when first non-request/response impl
lands (Phase C+).

For Phase B, both shipped adapters (MCPToolAdapter, future DirectAPIAdapter)
are stubs: they emit one `action` event per call() and return a canned
response. Real-wire protocol implementations are Phase C territory.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ClassVar, Optional

from fresh_plan.runtime.provision import load_provision_spec


class AdapterCallError(Exception):
    """Adapter ``call()`` runtime failure per D48 §B.1 (adapter cluster supersedes per D45 §C).

    Phase C real-wire forward-bar: real-wire adapter impls (subclasses of
    ``Adapter`` overriding ``call()``) SHALL raise this on protocol /
    transport / auth / timeout / upstream failures. Phase B stubs do not
    trigger this exception — the contract is defined now so Phase C impls
    have a clear bar to meet rather than a happy-path-only example to
    reverse-engineer from.

    Composes with D47 §B.1 SubscriberDispatchError aggregation: when
    AdapterCallError fires from inside a specialist's ``on_event``
    (subscriber-dispatch path per D37 + D44), it is captured per D47 §B.1
    into substrate's ``_subscriber_failures`` (substrate.py:310-320) and
    aggregated as SubscriberDispatchError after the outer drain.

    Per D48 §D D-1: call-lifecycle raise-point (before-wire / mid-wire /
    after-wire) is per-real-wire-impl choice. Per D48 §D D-3: starter
    category vocabulary (transport / auth / timeout / protocol-error /
    upstream-error / unknown) is HTTP/JSON-RPC-shaped; non-HTTP transports
    register additional categories per D29 namespacing.
    """

    def __init__(
        self,
        *,
        adapter_id: str,
        call_target: str,
        category: str,
        detail: Optional[dict] = None,
    ) -> None:
        self.adapter_id = adapter_id
        self.call_target = call_target
        self.category = category
        self.detail = dict(detail) if detail else {}
        super().__init__(
            f"[{category}] adapter={adapter_id!r} target={call_target!r}: {self.detail}"
        )


@dataclass
class Adapter:
    """Base class for adapter runtime impls per D16 + adapter.schema.json.

    Holds the loaded spec, exposes D16 slot accessors, manages workspace
    attachment + event-emit infrastructure. Subclasses override `call()` to
    implement protocol-specific invocation.
    """

    spec: dict
    # Per D57 §B.1: opaque pass-through configuration dict from
    # composition.adapter-bindings[i].configuration. None when slot omitted.
    configuration: Optional[dict] = None
    _emit_event: Optional[Callable[..., dict]] = field(default=None, repr=False)
    _workspace: Any = field(default=None, repr=False)
    _outcome_counter: int = field(default=0, repr=False)

    # Subclasses override to give their outcome-references a distinct prefix.
    _outcome_prefix: ClassVar[str] = "stub"

    @property
    def id(self) -> str:
        return self.spec["id"]

    @property
    def version(self) -> str:
        return self.spec["version"]

    @property
    def protocol_or_transport(self) -> str:
        return self.spec["protocol-or-transport"]

    @property
    def required_substrate_capabilities(self) -> list[str]:
        return list(self.spec.get("required-substrate-capabilities", []) or [])

    @property
    def declared_event_emissions(self) -> list[dict]:
        return list(self.spec.get("declared-event-emissions", []) or [])

    @property
    def declared_event_consumptions(self) -> list[dict]:
        return list(self.spec.get("declared-event-consumptions", []) or [])

    # ---------------------------------------------------------------
    # Workspace attachment (boot-ordering: post-Workspace construction)
    # ---------------------------------------------------------------

    def attach_workspace(self, workspace: Any) -> None:
        """Wire the workspace's event-emit callback into the adapter."""
        self._workspace = workspace
        self._emit_event = workspace._emit_event

    # ---------------------------------------------------------------
    # Convenience for request/response stub + real impls
    # ---------------------------------------------------------------

    def _emit_action(
        self,
        tool_name: str,
        parameters: dict,
        attributing_actor_id: Optional[str] = None,
    ) -> str:
        """Emit one `action` event for a tool-call invocation; return its outcome-reference."""
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "adapter not attached to a workspace; call attach_workspace first"
            )
        self._outcome_counter += 1
        outcome_reference = f"{self._outcome_prefix}-{self._outcome_counter}"
        actor_id = attributing_actor_id or next(
            iter(self._workspace._substrate.state.actors), None
        )
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": tool_name,
                "parameters": parameters,
                "outcome-reference": outcome_reference,
            },
        )
        return outcome_reference

    # ---------------------------------------------------------------
    # Invocation interface (abstract; subclass-owned)
    # ---------------------------------------------------------------

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Invoke this adapter for a tool-call. Subclasses MUST override."""
        raise NotImplementedError("Adapter subclasses must implement call()")


@dataclass
class MCPToolAdapter(Adapter):
    """Stub MCP-server-protocol adapter per D16 + B4.

    No real MCP wire is opened; `call()` emits one `action` event into the
    workspace event chain and returns a canned response carrying the
    outcome-reference. Phase C replaces the body with a real JSON-RPC
    client.
    """

    _outcome_prefix: ClassVar[str] = "mcp-stub"

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        params = parameters or {}
        outcome_reference = self._emit_action(tool_name, params, attributing_actor_id)
        return {
            "outcome-reference": outcome_reference,
            "ok": True,
            "stub": True,
            "tool": tool_name,
            "parameters": params,
        }


@dataclass
class DirectAPIAdapter(Adapter):
    """Stub direct-api adapter per D16 + B5.

    The non-MCP request/response path: an in-process direct call, no
    protocol wrapper. `call()` emits one `action` event and returns a
    canned response. Phase C / Phase D replace the body with real
    direct-call dispatch into target Python APIs.
    """

    _outcome_prefix: ClassVar[str] = "direct-stub"

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        params = parameters or {}
        outcome_reference = self._emit_action(tool_name, params, attributing_actor_id)
        return {
            "outcome-reference": outcome_reference,
            "ok": True,
            "stub": True,
            "kind": "direct-api",
            "tool": tool_name,
            "parameters": params,
        }


@dataclass
class RealWireMCPClientAdapter(Adapter):
    """Phase C real-wire MCP client adapter per D71 §B.1 (closes C3).

    Per D68 §A C3 + §B.3 (verify-at-workstream-start; MCP Python SDK
    confirmed at C3 workstream start) + D68 §C closure item (e). Activates
    D48 §B.1 AdapterCallError forward-bar under real-wire conditions per
    starter category vocabulary (transport / auth / timeout / protocol-error
    / upstream-error / unknown).

    The MCP Python SDK ships an async-only ``ClientSession``; this adapter
    wraps it synchronously per D44 ("no async substrate model" at Phase C)
    using ``asyncio.run`` to drive the underlying coroutines — mirroring
    the D69 ClaudeAgentSDKSubstrate pattern.

    Per D48 §D D-5 (action-event timing): this adapter emits the ``action``
    event BEFORE the wire round-trip so partial-success / failure paths
    leave the intent-recorded action event in the chain (per D5 §I3
    accountability anchor + D10 chain integrity). Caller of a failed
    ``call()`` may emit a subsequent ``state-change`` event to record
    outcome; the action event itself stands regardless.

    Per D48 §B.1 + §D D-1 (call-lifecycle raise-point): real-wire
    exceptions from any of (a) ClientSession construction, (b)
    ``initialize()``, (c) ``call_tool()``, (d) iterating streams are
    caught and mapped to ``AdapterCallError`` per starter category
    vocabulary. Mid-wire raise-point chosen: action event emitted at
    method entry; AdapterCallError can raise from anywhere downstream.

    Per scope-cut C12 (autopilot constraint) + the in-process test-server
    harness pattern: tests inject a ``_session_factory`` (per-instance
    field) that returns an async context-manager yielding a ClientSession.
    Production callers pass a configuration dict via
    ``composition.adapter-bindings[i].configuration`` (per D57 §B.1 opaque
    pass-through) carrying transport parameters; default factory builds a
    stdio_client subprocess. Phase C scope = test-harness exercise of the
    AdapterCallError starter category vocabulary; production stdio/sse/
    http transport selection is Phase C+ refinement per D-3 (extension-
    author concern per D29 namespacing).

    Per D48 §D D-3 starter category vocabulary mapping (resolves D-1+D-3
    for MCP transport per D71 §B.1):

      - ``transport`` ← OSError / ConnectionRefusedError / FileNotFoundError
        (subprocess spawn failure) / anyio.BrokenResourceError /
        anyio.ClosedResourceError (stream broken mid-call).
      - ``auth`` ← McpError with code indicating auth required
        (server-specific; mapped via auth-code subcase when known).
      - ``timeout`` ← TimeoutError (asyncio + anyio share the same name in
        Python 3.11+); raised from ``read_timeout_seconds`` parameter or
        from ``asyncio.wait_for`` boundary.
      - ``protocol-error`` ← JSONRPCError raw + McpError with JSON-RPC
        parse / method-not-found / invalid-params subcase (MCP error
        codes -32700 / -32601 / -32602 per JSON-RPC 2.0 spec).
      - ``upstream-error`` ← McpError from server returning structured
        error result OR CallToolResult with ``isError=True``.
      - ``unknown`` ← catch-all ``except Exception`` last branch.
    """

    _outcome_prefix: ClassVar[str] = "mcp-realwire"

    # Per-instance test-injection hook. Async callable returning an async
    # context manager that yields an initialized ClientSession. Tests set
    # this to a function building a session from anyio memory streams.
    # None → resolve default factory (stdio_client subprocess) at call() time.
    _session_factory: Optional[Callable[..., Any]] = field(
        default=None, repr=False
    )

    # Read-timeout for the call_tool round-trip, in seconds. Configurable per
    # D57 §B.1 opaque pass-through (`configuration.read-timeout-seconds`).
    _read_timeout_seconds: float = field(default=30.0, repr=False)

    def __post_init__(self) -> None:
        # Lift `read-timeout-seconds` from configuration dict if present
        # (per D57 §B.1 opaque pass-through). Default 30s preserves prior
        # behavior when no configuration is supplied.
        config = self.configuration or {}
        timeout = config.get("read-timeout-seconds")
        if timeout is not None:
            self._read_timeout_seconds = float(timeout)

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Invoke a remote MCP tool via JSON-RPC; return server result.

        Per D48 §B.1 surface contract: on protocol / transport / auth /
        timeout / upstream failures, raises ``AdapterCallError`` with the
        starter category vocabulary + original exception chained via
        Python's ``from`` clause.

        Per D48 §D D-5 (resolved by D71 §B.1): the ``action`` event is
        emitted BEFORE the wire round-trip. Partial-success / failure
        paths leave the intent-recorded action event in the chain.

        Args:
            tool_name: MCP tool name to invoke at the server.
            parameters: optional dict of tool arguments (passed as JSON-
                serializable kwargs to the remote tool).
            attributing_actor_id: override the default first-actor
                attribution for the emitted action event.

        Returns:
            Dict carrying ``outcome-reference`` (the action event's
            unique ref), ``ok`` (True on success), ``isError`` (mirror of
            server-side flag), and ``content`` (list of CallToolResult
            content blocks serialized to dicts when present).

        Raises:
            AdapterCallError: on any wire / protocol / auth / timeout /
                upstream failure — see §B.1 category vocabulary.
        """
        import asyncio

        params = parameters or {}

        # Emit the action event FIRST so the intent is recorded in the
        # chain even if the wire round-trip fails partway through. Per D48
        # §D D-5 resolution at D71 §B.1.
        outcome_reference = self._emit_action(
            tool_name, params, attributing_actor_id
        )

        async def _drive() -> dict:
            # Resolve factory: per-instance override (test injection) OR
            # default stdio_client (production). Default deliberately
            # raises NotImplementedError when no factory is set — keeps
            # the Phase C scope test-harness-focused per scope-cut C12
            # while leaving a clear extension point for production.
            factory = self._session_factory
            if factory is None:
                raise NotImplementedError(
                    f"RealWireMCPClientAdapter {self.id!r}: no "
                    "_session_factory set; production stdio/sse/http "
                    "transport selection is deferred to Phase C+ per "
                    "D71 §D D-3"
                )
            async with factory() as session:
                from datetime import timedelta

                timeout = timedelta(seconds=self._read_timeout_seconds)
                result = await session.call_tool(
                    tool_name,
                    arguments=params,
                    read_timeout_seconds=timeout,
                )
            # CallToolResult fields: content / structuredContent / isError /
            # meta (per mcp.types.CallToolResult).
            is_error = bool(getattr(result, "isError", False))
            content = getattr(result, "content", None) or []
            serialized_content = []
            for block in content:
                # Best-effort serialization: pydantic-model blocks expose
                # .model_dump(); fall back to str() if missing.
                dump = getattr(block, "model_dump", None)
                serialized_content.append(
                    dump(mode="json") if callable(dump) else str(block)
                )
            if is_error:
                # Server returned a structured error result per MCP spec
                # (CallToolResult.isError=True). Map to upstream-error
                # category per starter vocabulary.
                raise AdapterCallError(
                    adapter_id=self.id,
                    call_target=tool_name,
                    category="upstream-error",
                    detail={
                        "reason": "MCP server returned isError=True",
                        "content": serialized_content,
                    },
                )
            return {
                "outcome-reference": outcome_reference,
                "ok": True,
                "isError": is_error,
                "content": serialized_content,
            }

        # Lazy import — keeps adapter module load-cost low when MCP SDK
        # is not used (e.g., direct-api-only workspaces).
        try:
            from mcp.shared.exceptions import McpError
        except ImportError as exc:
            # mcp SDK missing despite pyproject declaration (e.g., uninstalled
            # local dev env). Surface as transport per starter vocabulary —
            # the call cannot proceed because the wire library is absent.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": f"mcp SDK import failed: {exc}"},
            ) from exc

        try:
            return asyncio.run(_drive())
        except AdapterCallError:
            # Already mapped (e.g., upstream-error inside _drive). Pass
            # through without re-wrapping.
            raise
        except TimeoutError as exc:
            # asyncio.TimeoutError + anyio.TimeoutError both surface as
            # builtins.TimeoutError in Python 3.11+.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="timeout",
                detail={
                    "reason": str(exc) or "MCP call_tool timed out",
                    "read-timeout-seconds": self._read_timeout_seconds,
                },
            ) from exc
        except McpError as exc:
            # MCP SDK structured error. ErrorData carries (code / message /
            # data). JSON-RPC reserved codes (-32700 / -32600 / -32601 /
            # -32602 / -32603) → protocol-error; auth-bearing codes
            # (server-specific; commonly -32001 / -32002 etc.) → auth;
            # anything else → upstream-error.
            error_data = getattr(exc, "error", None)
            code = getattr(error_data, "code", None) if error_data else None
            message = (
                getattr(error_data, "message", str(exc))
                if error_data
                else str(exc)
            )
            if code is not None and -32768 <= code <= -32000:
                # JSON-RPC reserved range = protocol-error per spec.
                # Auth subcase deferred per D71 §D D-2 — server-specific
                # codes outside reserved range may map to auth when
                # known; current mapping treats any reserved-range code
                # as protocol-error.
                category = "protocol-error"
            else:
                category = "upstream-error"
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category=category,
                detail={
                    "reason": message,
                    "code": code,
                },
            ) from exc
        except (OSError, ConnectionError) as exc:
            # Transport-layer failure: subprocess spawn (FileNotFoundError),
            # connection refused, broken pipe, stream closed.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": str(exc) or type(exc).__name__},
            ) from exc
        except Exception as exc:
            # Catch-all per D48 §B.1 starter vocabulary `unknown` category.
            # Includes anyio.BrokenResourceError + anyio.ClosedResourceError
            # which derive from Exception but not OSError; both surface as
            # transport semantically but Python typing doesn't make this
            # discriminable without importing anyio at adapter-call-time.
            # Per-protocol extension may register a richer subcategory per
            # D29 namespacing (deferred per D71 §D D-3).
            anyio_resource_names = {
                "BrokenResourceError",
                "ClosedResourceError",
                "EndOfStream",
            }
            if type(exc).__name__ in anyio_resource_names:
                raise AdapterCallError(
                    adapter_id=self.id,
                    call_target=tool_name,
                    category="transport",
                    detail={
                        "reason": f"{type(exc).__name__}: {exc}",
                    },
                ) from exc
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="unknown",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc


# Module-level registry of (protocol-or-transport → runtime class). Populated
# as new adapter impls land. Phase C real-wire impls add alongside Phase B
# stubs (per D41 two-substrate parity precedent + D69 substrate-alongside
# pattern) rather than replacing them — preserves 0.1.0 stub path for back-
# compat + lets workspaces opt into real-wire by binding the 0.2.0 provision.
_ADAPTER_CLASSES: dict[str, type[Adapter]] = {
    "mcp-server-ext:mcp-client": MCPToolAdapter,
    "mcp-server-ext:mcp-client-realwire": RealWireMCPClientAdapter,
    "direct-api-ext:direct-api": DirectAPIAdapter,
}


def load_adapter_from_provision(
    provision_ref: str,
    extensions_dir: Path,
    *,
    configuration: Optional[dict] = None,
) -> Adapter:
    """Load an adapter spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.protocol-or-transport` to the registered runtime
    class. Raises ValueError if the spec uses a protocol-or-transport with
    no registered runtime class (boot.py wraps as ``category="resolution"``).
    Constructor-raises are caught at boot.py and wrapped as
    ``category="configuration-rejected"`` per D57 §B.1.
    """
    from fresh_plan.runtime.provision import ProvisionResolutionError

    spec = load_provision_spec(provision_ref, extensions_dir)
    protocol = spec.get("protocol-or-transport")
    cls = _ADAPTER_CLASSES.get(protocol)
    if cls is None:
        raise ProvisionResolutionError(
            f"adapter provision {provision_ref!r}: protocol-or-transport "
            f"{protocol!r} has no registered Adapter runtime class"
        )
    return cls(spec=spec, configuration=configuration)
