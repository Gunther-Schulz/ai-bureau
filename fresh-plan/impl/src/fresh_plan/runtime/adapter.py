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


@dataclass
class RealWireDirectAPIAdapter(Adapter):
    """Phase C real-wire direct-API HTTP adapter per D72 §B.1 (closes C4).

    Per D68 §A C4 + §B.3 (verify-at-workstream-start; httpx 0.28.1 confirmed
    at C4 workstream start) + D68 §C closure item (e). Pure pattern
    application of D71 §B.1 (RealWireMCPClientAdapter) for HTTP transport:
    SAME class shape, SAME asyncio.run sync-wrap pattern, SAME
    _session_factory test-injection hook, SAME D48 §B.1 starter category
    vocabulary (transport / auth / timeout / protocol-error / upstream-error
    / unknown). The httpx-specific exception branches differ; the framework
    contract is unchanged.

    The httpx library ships ``httpx.AsyncClient`` (async-only here for
    Phase C pattern consistency with D69 + D71); this adapter wraps it
    synchronously per D44 ("no async substrate model" at Phase C) using
    ``asyncio.run`` to drive the underlying coroutines — mirroring the
    D69 + D71 sync-wrap precedent.

    Per D48 §D D-5 (action-event timing; resolved by D71 §B.1 for adapter
    cluster): this adapter emits the ``action`` event BEFORE the wire
    round-trip so partial-success / failure paths leave the intent-recorded
    action event in the chain (per D5 §I3 accountability anchor + D10 chain
    integrity). Caller of a failed ``call()`` may emit a subsequent
    ``state-change`` event to record outcome; the action event itself
    stands regardless.

    Per D48 §B.1 + §D D-1 (call-lifecycle raise-point): real-wire exceptions
    from any of (a) AsyncClient construction, (b) HTTP request send,
    (c) response status validation, (d) JSON decoding are caught and
    mapped to ``AdapterCallError`` per starter category vocabulary.
    Mid-wire raise-point chosen: action event emitted at method entry;
    AdapterCallError can raise from anywhere downstream.

    Per scope-cut C12 (autopilot constraint) + the in-process test
    harness pattern: tests inject a ``_session_factory`` (per-instance
    field) that returns an async context-manager yielding a configured
    ``httpx.AsyncClient`` (typically with a ``MockTransport`` handler
    function). Production callers pass a configuration dict via
    ``composition.adapter-bindings[i].configuration`` (per D57 §B.1
    opaque pass-through) carrying ``base-url`` + ``headers`` + (optional)
    ``read-timeout-seconds``; default factory builds a real
    ``AsyncClient`` from configuration. Phase C scope = test-harness
    exercise of the AdapterCallError starter category vocabulary;
    production per-API auth-flow specifics (OAuth / JWT refresh / etc.)
    are Phase D refinement per D72 §D D-2 (extension-author concern per
    D29 namespacing).

    Per D48 §D D-3 starter category vocabulary mapping (HTTP-native;
    extends D71's MCP mapping with native auth-category discrimination —
    unlike MCP per D71 §D D-2 deferral, HTTP cleanly discriminates 401
    / 403 / 407 from upstream-error 4xx/5xx via response.status_code):

      - ``transport`` ← httpx.ConnectError / httpx.NetworkError + plain
        OSError (subclasses cover TLS-handshake / DNS / socket).
      - ``auth`` ← httpx.HTTPStatusError with response.status_code in
        {401, 403, 407}. NATIVE HTTP semantics — first Phase C adapter
        to populate the auth starter category natively.
      - ``timeout`` ← httpx.TimeoutException (covers ConnectTimeout +
        ReadTimeout + WriteTimeout + PoolTimeout subclasses).
      - ``protocol-error`` ← httpx.RemoteProtocolError + httpx.DecodingError
        + json.JSONDecodeError / ValueError raised by response.json().
      - ``upstream-error`` ← httpx.HTTPStatusError with status_code >=
        500 OR non-auth 4xx (400 / 404 / 405 / 409 / 422 / 429 / etc.).
      - ``unknown`` ← catch-all ``except Exception`` last branch.
    """

    _outcome_prefix: ClassVar[str] = "direct-realwire"

    # Per-instance test-injection hook. Async callable returning an async
    # context manager that yields a configured httpx.AsyncClient. Tests
    # set this to a function building a client with a MockTransport
    # handler for fault injection. None → resolve default factory
    # (real httpx.AsyncClient from configuration) at call() time.
    _session_factory: Optional[Callable[..., Any]] = field(
        default=None, repr=False
    )

    # Read-timeout for the HTTP request round-trip, in seconds. Configurable
    # per D57 §B.1 opaque pass-through (`configuration.read-timeout-seconds`).
    _read_timeout_seconds: float = field(default=30.0, repr=False)

    # Configuration-lifted fields used to build the default factory's
    # AsyncClient + the per-call request. Lifted in __post_init__ from
    # `configuration` per D57 §B.1 opaque pass-through.
    _base_url: str = field(default="", repr=False)
    _headers: dict = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        # Lift configuration per D57 §B.1 opaque pass-through. Defaults
        # preserve the unconfigured shape (empty base_url + headers; 30s
        # timeout).
        config = self.configuration or {}
        timeout = config.get("read-timeout-seconds")
        if timeout is not None:
            self._read_timeout_seconds = float(timeout)
        base_url = config.get("base-url")
        if base_url is not None:
            self._base_url = str(base_url)
        headers = config.get("headers")
        if headers is not None:
            self._headers = dict(headers)

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Invoke a remote HTTP endpoint as ``POST {base_url}/{tool_name}``;
        return parsed JSON body.

        Per D48 §B.1 surface contract: on protocol / transport / auth /
        timeout / upstream failures, raises ``AdapterCallError`` with the
        starter category vocabulary + original exception chained via
        Python's ``from`` clause.

        Per D48 §D D-5 (resolved by D71 §B.1 + carried by D72 §B.1): the
        ``action`` event is emitted BEFORE the wire round-trip. Partial-
        success / failure paths leave the intent-recorded action event
        in the chain.

        Args:
            tool_name: path component appended to ``base_url`` for the
                outgoing request (e.g., ``"chat/completions"``).
            parameters: optional dict of request body parameters (JSON-
                serializable). Sent as the JSON body of a POST.
            attributing_actor_id: override the default first-actor
                attribution for the emitted action event.

        Returns:
            Dict carrying ``outcome-reference`` (the action event's
            unique ref), ``ok`` (True on success), ``status-code`` (HTTP
            status code), and ``body`` (parsed JSON response body when
            content-type is JSON; raw text otherwise).

        Raises:
            AdapterCallError: on any wire / protocol / auth / timeout /
                upstream failure — see §B.1 category vocabulary.
        """
        import asyncio

        params = parameters or {}

        # Emit the action event FIRST so the intent is recorded in the
        # chain even if the wire round-trip fails partway through. Per
        # D48 §D D-5 resolution at D71 §B.1; D72 §B.1 carries this for
        # HTTP transport.
        outcome_reference = self._emit_action(
            tool_name, params, attributing_actor_id
        )

        # Lazy import — keeps adapter module load-cost low when httpx is
        # not used (e.g., MCP-only workspaces).
        try:
            import httpx
        except ImportError as exc:
            # httpx missing despite pyproject declaration (e.g.,
            # uninstalled local dev env). Surface as transport per
            # starter vocabulary — the call cannot proceed because the
            # wire library is absent.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": f"httpx import failed: {exc}"},
            ) from exc

        async def _drive() -> dict:
            # Resolve factory: per-instance override (test injection) OR
            # default real AsyncClient (production). Default builds a
            # client from lifted configuration; tests inject a factory
            # that wires MockTransport for in-process exception / status
            # injection.
            factory = self._session_factory
            if factory is None:
                # Build the default AsyncClient from configuration.
                from contextlib import asynccontextmanager

                @asynccontextmanager
                async def _default_factory():
                    async with httpx.AsyncClient(
                        base_url=self._base_url,
                        headers=self._headers,
                        timeout=self._read_timeout_seconds,
                    ) as client:
                        yield client

                factory = _default_factory

            async with factory() as client:
                response = await client.post(tool_name, json=params)
                # raise_for_status() surfaces non-2xx as
                # httpx.HTTPStatusError. We catch it in the outer
                # mapping branch to discriminate auth (401/403/407) vs
                # upstream-error (5xx + other 4xx).
                response.raise_for_status()
                status_code = response.status_code
                # Attempt JSON decode; fall back to text on non-JSON
                # responses. response.json() raises json.JSONDecodeError
                # (a ValueError subclass) on malformed JSON — mapped to
                # protocol-error in the outer branch.
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type.lower():
                    body: Any = response.json()
                else:
                    body = response.text
            return {
                "outcome-reference": outcome_reference,
                "ok": True,
                "status-code": status_code,
                "body": body,
            }

        try:
            return asyncio.run(_drive())
        except AdapterCallError:
            # Already mapped (none currently raised inside _drive on the
            # happy path, but keep for symmetry with D71 + future
            # in-_drive mappings).
            raise
        except httpx.TimeoutException as exc:
            # Covers ConnectTimeout + ReadTimeout + WriteTimeout +
            # PoolTimeout subclasses per httpx exception hierarchy.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="timeout",
                detail={
                    "reason": str(exc) or type(exc).__name__,
                    "read-timeout-seconds": self._read_timeout_seconds,
                },
            ) from exc
        except httpx.HTTPStatusError as exc:
            # raise_for_status() surfaced a non-2xx response. Discriminate
            # auth (401/403/407 per RFC 7235 + 7239) vs upstream-error
            # (5xx + other 4xx). NATIVE HTTP auth-category mapping —
            # unlike MCP per D71 §D D-2 deferral.
            status_code = exc.response.status_code
            if status_code in (401, 403, 407):
                category = "auth"
            else:
                category = "upstream-error"
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category=category,
                detail={
                    "reason": str(exc) or f"HTTP {status_code}",
                    "status-code": status_code,
                },
            ) from exc
        except (httpx.RemoteProtocolError, httpx.DecodingError) as exc:
            # Protocol-level failures: malformed HTTP framing / chunked
            # encoding / encoding declared but not decodable.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="protocol-error",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc
        except ValueError as exc:
            # json.JSONDecodeError (subclass of ValueError) raised by
            # response.json() on malformed JSON body. Map to
            # protocol-error per starter vocabulary — server returned
            # 2xx but body didn't conform to declared JSON content-type.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="protocol-error",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc
        except (httpx.ConnectError, httpx.NetworkError) as exc:
            # Transport-layer failure: DNS / connection-refused / TLS
            # handshake / socket-level errors. Note: ConnectError is a
            # subclass of NetworkError; listing both for clarity.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": str(exc) or type(exc).__name__},
            ) from exc
        except OSError as exc:
            # Lower-level OS failure not wrapped by httpx (rare but
            # possible — e.g., raised by MockTransport handler directly).
            # Maps to transport semantically.
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": str(exc) or type(exc).__name__},
            ) from exc
        except Exception as exc:
            # Catch-all per D48 §B.1 starter vocabulary `unknown` category.
            # Per-protocol extension may register a richer subcategory per
            # D29 namespacing (deferred per D72 §D D-2).
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="unknown",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc


@dataclass
class A2APeerAdapter(Adapter):
    """Phase C real-wire A2A peer adapter per D73 §B (closes C5).

    Per D68 §A C5 + §B.3 (verify-at-workstream-start; a2a-sdk 1.0.3 confirmed
    at C5 workstream start) + D68 §C closure item (a) (A2A peer simulator
    harness; in-process). Combines THREE concerns in one adapter class:

      (a) **Inbound agent-card publisher** — serves the workspace's
          aggregated agent-card at ``GET /.well-known/agent.json`` per D21
          (workspace-as-A2A-peer deployability) + D60 (specialist.skills
          publicly-exposed slot is the documentary anticipation D21
          consumes here).
      (b) **Inbound A2A task receiver** — routes ``POST /tasks`` requests
          to the matching specialist's ``handle_skill(skill_id, params)``
          per D19 + the substrate.specialist_instances registry.
      (c) **Outbound A2A peer client** — ``call(tool_name, parameters)``
          POSTs to a configured ``peer_url`` per D72 §B.1 pattern
          (httpx.AsyncClient + asyncio.run sync-wrap + AdapterCallError
          per starter category vocabulary). Mirrors c4 for outbound.

    Server lifecycle (stdlib ``http.server.ThreadingHTTPServer`` on a
    background daemon thread per coherence-advisory #3 + D44 "no async
    substrate model"):

      - ``attach_workspace(workspace)``: super().attach_workspace; then
        ``ThreadingHTTPServer((bind_host, bind_port), HandlerCls)`` + start
        a daemon ``threading.Thread`` running ``server.serve_forever()``.
        Bind failures (port in use) raise ``OSError`` which boot.py wraps
        as ``WorkspaceBootError(category='adapter-attach')`` per D48 §B.2
        (REUSE — no new FAILURE_CATEGORIES entry).
      - ``shutdown()``: ``server.shutdown()`` + ``thread.join(timeout=5)``.
        Idempotent; safe to call from any thread. Test fixtures call this
        in their finally-block.
      - Port resolution: if ``configuration['port']`` is 0 or omitted,
        stdlib ``ThreadingHTTPServer`` auto-allocates; the assigned port
        is readable via ``self._server.server_address[1]`` post-start.

    Per D48 §B.1 + §D D-1 (call-lifecycle raise-point): outbound `call()`
    exceptions from httpx are caught and mapped to ``AdapterCallError``
    per starter category vocabulary (transport / auth / timeout /
    protocol-error / upstream-error / unknown — same as D72 §B.1).
    Mid-wire raise-point: action event emitted at method entry; AdapterCallError
    can raise from anywhere downstream.

    Per D48 §D D-3 outbound starter category vocabulary mapping (HTTP-native;
    parallel to D72 §B.1 since A2A wire format is HTTP-shaped):

      - ``transport`` ← httpx.ConnectError / httpx.NetworkError + OSError.
      - ``auth`` ← httpx.HTTPStatusError with status_code in {401, 403, 407}.
      - ``timeout`` ← httpx.TimeoutException (subclasses included).
      - ``protocol-error`` ← httpx.RemoteProtocolError / DecodingError /
        ValueError from response.json() on malformed body.
      - ``upstream-error`` ← httpx.HTTPStatusError with other 4xx / 5xx.
      - ``unknown`` ← catch-all ``except Exception`` last branch.

    Inbound handler exceptions (specialist.handle_skill raises during
    POST /tasks routing) are caught inside the HTTP request handler and
    surface as HTTP 500 + an A2A error response body. These are NOT
    AdapterCallError because they're server-side; the framework process
    is the receiver, not the caller — no AdapterCallError consumer exists.
    The HTTP 500 IS the surface (caller-side, an external A2A peer would
    see it; in tests, the httpx.Client used by the harness observes it).
    """

    _outcome_prefix: ClassVar[str] = "a2a-peer"

    # Per-instance test-injection hook for outbound call(); parallels D72.
    # None → default factory builds a real httpx.AsyncClient using
    # `_peer_url` + `_read_timeout_seconds` at call() time.
    _session_factory: Optional[Callable[..., Any]] = field(
        default=None, repr=False
    )

    # Configuration-lifted fields. Lifted in __post_init__ from
    # `configuration` per D57 §B.1 opaque pass-through.
    _bind_host: str = field(default="localhost", repr=False)
    _bind_port: int = field(default=0, repr=False)  # 0 → auto-allocate
    _peer_url: str = field(default="", repr=False)
    _read_timeout_seconds: float = field(default=30.0, repr=False)

    # Server-state — populated by attach_workspace; cleared by shutdown.
    _server: Any = field(default=None, repr=False)
    _thread: Any = field(default=None, repr=False)

    def __post_init__(self) -> None:
        # Lift configuration per D57 §B.1 opaque pass-through. Defaults
        # preserve unconfigured shape.
        config = self.configuration or {}
        bind_host = config.get("bind-host")
        if bind_host is not None:
            self._bind_host = str(bind_host)
        bind_port = config.get("port")
        if bind_port is not None:
            self._bind_port = int(bind_port)
        peer_url = config.get("peer-url")
        if peer_url is not None:
            self._peer_url = str(peer_url)
        timeout = config.get("read-timeout-seconds")
        if timeout is not None:
            self._read_timeout_seconds = float(timeout)

    # ---------------------------------------------------------------
    # Server lifecycle (inbound publisher + task receiver)
    # ---------------------------------------------------------------

    def attach_workspace(self, workspace: Any) -> None:
        """Wire workspace + start the inbound HTTP server thread.

        Per D48 §B.2: any OSError from socket-bind (e.g., port in use)
        propagates out and is wrapped at boot.py:599 as
        ``WorkspaceBootError(category='adapter-attach')`` per the
        existing REUSE path (no new category needed).
        """
        super().attach_workspace(workspace)

        import threading
        from http.server import ThreadingHTTPServer

        adapter_self = self
        handler_cls = _make_a2a_request_handler(adapter_self)
        # bind_port=0 → stdlib auto-allocates a free port; read back via
        # server.server_address[1] post-construction.
        self._server = ThreadingHTTPServer(
            (self._bind_host, self._bind_port), handler_cls
        )
        # Update the lifted port to the actual bound value (important when
        # configuration requested auto-allocate via port=0).
        self._bind_port = self._server.server_address[1]
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name=f"A2APeerAdapter[{self.id}]",
            daemon=True,
        )
        self._thread.start()

    def shutdown(self) -> None:
        """Stop the inbound HTTP server thread. Idempotent."""
        if self._server is not None:
            try:
                self._server.shutdown()
            finally:
                self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None

    @property
    def bound_port(self) -> int:
        """The actual port the inbound HTTP server is bound to.

        Equal to ``configuration['port']`` when explicit; auto-allocated
        value when ``configuration['port']`` was 0 or omitted. Test
        harnesses read this to build the ``http://localhost:<port>`` URL
        for in-process httpx.Client requests.
        """
        return self._bind_port

    # ---------------------------------------------------------------
    # Agent-card aggregation (per D21 + D60)
    # ---------------------------------------------------------------

    def build_agent_card_json(self) -> str:
        """Build the workspace's aggregated A2A AgentCard as JSON bytes.

        Walks ``workspace._substrate.specialist_instances`` (per D19 +
        substrate.py:158-159). For each specialist's ``spec.skills[]``
        entry, filter by ``publicly-exposed=True`` (per D60 + specialist
        schema lines 46-51); map to ``a2a.types.AgentSkill`` (the
        protobuf-generated canonical type from a2a-sdk 1.0.3); embed in
        ``a2a.types.AgentCard``. Serialize via
        ``google.protobuf.json_format.MessageToJson`` for canonical JSON
        output preserving snake_case proto field names per the A2A
        public spec.

        Per D21 §"What this requires from extensions": exposure control
        ensures internal-only skills don't leak into the agent-card.

        Returns:
            JSON string in canonical A2A AgentCard shape.
        """
        from a2a.types import AgentCard, AgentSkill
        from google.protobuf import json_format

        skills_pb = []
        if self._workspace is not None:
            substrate = self._workspace._substrate
            for binding_id, specialist in substrate.specialist_instances.items():
                for skill in specialist.skills:
                    if skill.get("publicly-exposed") is not True:
                        continue
                    skills_pb.append(
                        AgentSkill(
                            id=skill["id"],
                            name=skill["id"],
                            description=skill.get("description", ""),
                            tags=[binding_id],
                            input_modes=list(
                                skill.get("input-modalities", []) or []
                            ),
                            output_modes=list(
                                skill.get("output-modalities", []) or []
                            ),
                        )
                    )

        workspace_id = (
            self._workspace.workspace_id
            if self._workspace is not None
            else self.id
        )
        card = AgentCard(
            name=workspace_id,
            description=(
                f"A2A peer agent-card for workspace {workspace_id!r}"
            ),
            version="1.0.0",
            skills=skills_pb,
        )
        return json_format.MessageToJson(
            card, preserving_proto_field_name=True
        )

    # ---------------------------------------------------------------
    # Inbound task routing (POST /tasks → specialist.handle_skill)
    # ---------------------------------------------------------------

    def handle_inbound_task(self, task_payload: dict) -> dict:
        """Route an inbound A2A task to a specialist's handle_skill.

        The task payload is expected to carry ``{"skill_id": "...",
        "params": {...}}``. Looks up the first specialist whose spec
        declares a publicly-exposed skill matching ``skill_id``; invokes
        ``specialist.handle_skill(skill_id, params)`` and returns the
        result wrapped as ``{"ok": True, "result": <handle_skill_return>}``.

        If no specialist owns a publicly-exposed skill matching
        ``skill_id``, raises ``KeyError`` (handler converts to HTTP 404 +
        A2A error response shape).

        If specialist.handle_skill raises, the exception propagates out
        (handler converts to HTTP 500 + A2A error response shape).

        Returns:
            Dict with ``ok: True`` + ``result`` carrying the
            ``handle_skill`` return value.
        """
        skill_id = task_payload.get("skill_id") or task_payload.get(
            "skill-id"
        )
        if not skill_id:
            raise KeyError("task payload missing 'skill_id'")
        params = task_payload.get("params") or {}

        if self._workspace is None:
            raise RuntimeError(
                "adapter not attached to a workspace; "
                "call attach_workspace first"
            )
        substrate = self._workspace._substrate
        for binding_id, specialist in substrate.specialist_instances.items():
            for skill in specialist.skills:
                if skill.get("publicly-exposed") is not True:
                    continue
                if skill["id"] == skill_id:
                    result = specialist.handle_skill(skill_id, params)
                    return {"ok": True, "result": result}
        raise KeyError(
            f"no specialist binding declares a publicly-exposed skill "
            f"named {skill_id!r}"
        )

    # ---------------------------------------------------------------
    # Outbound call() — D48 §B.1 forward-bar under HTTP transport
    # ---------------------------------------------------------------

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Invoke a peer A2A endpoint as ``POST {peer_url}/tasks``.

        Per D48 §B.1 surface contract: on protocol / transport / auth /
        timeout / upstream failures, raises ``AdapterCallError`` with
        the starter category vocabulary + original exception chained
        via Python's ``from`` clause.

        Per D48 §D D-5 (resolved by D71 §B.1; carried by D72 §B.1; D73
        §B.2 carries forward for A2A peer transport): the ``action``
        event is emitted BEFORE the wire round-trip. Partial-success /
        failure paths leave the intent-recorded action event in the
        chain.

        Args:
            tool_name: skill_id at the peer to invoke (mapped into the
                task payload's ``skill_id`` field; the URL path is
                ``/tasks`` constant per A2A peer task convention).
            parameters: optional dict of task parameters sent as the
                ``params`` field of the JSON task payload.
            attributing_actor_id: override the default first-actor
                attribution for the emitted action event.

        Returns:
            Dict carrying ``outcome-reference`` (action event ref),
            ``ok`` (True on success), ``status-code`` (HTTP status code),
            and ``body`` (parsed JSON response from the peer).

        Raises:
            AdapterCallError: on any wire / protocol / auth / timeout /
                upstream failure — see D72 §B.1 category vocabulary
                (parallel mapping for HTTP transport).
        """
        import asyncio

        params = parameters or {}
        outcome_reference = self._emit_action(
            tool_name, params, attributing_actor_id
        )

        try:
            import httpx
        except ImportError as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": f"httpx import failed: {exc}"},
            ) from exc

        async def _drive() -> dict:
            factory = self._session_factory
            if factory is None:
                from contextlib import asynccontextmanager

                @asynccontextmanager
                async def _default_factory():
                    async with httpx.AsyncClient(
                        base_url=self._peer_url,
                        timeout=self._read_timeout_seconds,
                    ) as client:
                        yield client

                factory = _default_factory

            task_payload = {"skill_id": tool_name, "params": params}
            async with factory() as client:
                response = await client.post("/tasks", json=task_payload)
                response.raise_for_status()
                status_code = response.status_code
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type.lower():
                    body: Any = response.json()
                else:
                    body = response.text
            return {
                "outcome-reference": outcome_reference,
                "ok": True,
                "status-code": status_code,
                "body": body,
            }

        try:
            return asyncio.run(_drive())
        except AdapterCallError:
            raise
        except httpx.TimeoutException as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="timeout",
                detail={
                    "reason": str(exc) or type(exc).__name__,
                    "read-timeout-seconds": self._read_timeout_seconds,
                },
            ) from exc
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            if status_code in (401, 403, 407):
                category = "auth"
            else:
                category = "upstream-error"
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category=category,
                detail={
                    "reason": str(exc) or f"HTTP {status_code}",
                    "status-code": status_code,
                },
            ) from exc
        except (httpx.RemoteProtocolError, httpx.DecodingError) as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="protocol-error",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc
        except ValueError as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="protocol-error",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc
        except (httpx.ConnectError, httpx.NetworkError) as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": str(exc) or type(exc).__name__},
            ) from exc
        except OSError as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={"reason": str(exc) or type(exc).__name__},
            ) from exc
        except Exception as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="unknown",
                detail={
                    "reason": f"{type(exc).__name__}: {exc}",
                },
            ) from exc


def _make_a2a_request_handler(adapter: "A2APeerAdapter"):
    """Build a BaseHTTPRequestHandler subclass closing over the adapter.

    The handler routes:
      - ``GET /.well-known/agent.json`` → adapter.build_agent_card_json()
      - ``POST /tasks`` → adapter.handle_inbound_task(json_body)
      - everything else → HTTP 404

    Handler exceptions from ``handle_inbound_task`` surface as HTTP 500 +
    A2A-shaped error response body. KeyError (unknown skill_id) surfaces
    as HTTP 404. JSON decode errors on inbound body surface as HTTP 400.
    These error surfaces ARE the recovery path per D73 §B.3 inbound-
    handler triad (NOT AdapterCallError — server-side; no caller in
    framework process).
    """
    import json as _json
    from http.server import BaseHTTPRequestHandler

    class _A2ARequestHandler(BaseHTTPRequestHandler):
        # Silence stdlib's default stderr access-log; tests don't need it
        # and noisy logs obscure the actual pytest output.
        def log_message(self, format, *args):  # type: ignore[override]
            return

        def _write_json(self, status: int, body: dict) -> None:
            payload = _json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802 (stdlib API name)
            if self.path == "/.well-known/agent.json":
                try:
                    card_json = adapter.build_agent_card_json()
                except Exception as exc:  # pragma: no cover defensive
                    self._write_json(
                        500,
                        {
                            "error": {
                                "code": "agent-card-build-failed",
                                "message": str(exc),
                            }
                        },
                    )
                    return
                payload = card_json.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            self._write_json(
                404, {"error": {"code": "not-found", "path": self.path}}
            )

        def do_POST(self) -> None:  # noqa: N802 (stdlib API name)
            if self.path != "/tasks":
                self._write_json(
                    404,
                    {"error": {"code": "not-found", "path": self.path}},
                )
                return
            length = int(self.headers.get("Content-Length", "0") or "0")
            raw = self.rfile.read(length) if length else b""
            try:
                payload = _json.loads(raw) if raw else {}
            except ValueError as exc:
                self._write_json(
                    400,
                    {
                        "error": {
                            "code": "malformed-json",
                            "message": str(exc),
                        }
                    },
                )
                return
            try:
                result = adapter.handle_inbound_task(payload)
            except KeyError as exc:
                self._write_json(
                    404,
                    {
                        "error": {
                            "code": "skill-not-found",
                            "message": str(exc),
                        }
                    },
                )
                return
            except Exception as exc:
                # Per D73 §B.3 inbound-handler triad: specialist
                # handle_skill exception surfaces as HTTP 500 + A2A
                # error response body. Recovery path = caller sees error
                # response; logged on the wire side.
                self._write_json(
                    500,
                    {
                        "error": {
                            "code": "skill-execution-error",
                            "type": type(exc).__name__,
                            "message": str(exc),
                        }
                    },
                )
                return
            self._write_json(200, result)

    return _A2ARequestHandler


@dataclass
class MCPServerAdapter(Adapter):
    """Phase C real-wire MCP SERVER adapter per D74 §B (closes C6; closes
    Phase C closure item (b) — workspace-as-MCP-server).

    Per D68 §A C6 + §B.3 (verify-at-workstream-start; mcp Python SDK
    confirmed via prior C3 introspection per D71; same package, server-side
    surface) + D68 §C closure item (b) (in-process self-test harness per
    scope-cut C12 — workspace's own MCP client invokes workspace's own MCP
    server). Validates D21 §generalization (workspace-as-MCP-server) by
    providing the concrete extension impl exposing loaded specialists'
    skills as MCP tools to an MCP client.

    HYBRID pattern application of D71 (MCP SDK; ClientSession side) + D73
    (server-side aggregator; specialist_instances filter publicly-exposed
    + tool-routing-to-handle_skill). Unlike D73 (HTTP server via stdlib
    ThreadingHTTPServer on a daemon thread), this adapter is **async-native**
    — the mcp SDK's ``Server.run`` API is an asyncio coroutine, and the
    self-test fixture uses ``mcp.shared.memory.create_connected_server_and_client_session(server)``
    which bridges client+server inside the SAME asyncio event loop. No
    background thread; no ThreadingHTTPServer.

    Per scope-cut C12 (Phase C autopilot constraint): tests use the SDK's
    in-process memory bridge directly — the test fixture constructs the
    workspace, reads the adapter's prepared ``server`` attribute (populated
    by ``attach_workspace``), and drives ``create_connected_server_and_client_session(server)``
    inside ``asyncio.run`` to assert list_tools + call_tool round-trips.
    There is NO long-running server task at framework attach time —
    production transports (stdio / sse / streamable_http) are Phase D
    pioneer-instance territory (deferred per D74 §D).

    Per D45 triad applied per path:

      §B.1 Server-bind failure at attach_workspace lifecycle: SDK Server
      construction failures (rare; mostly init-arg-shape) propagate as
      Exception which boot.py:599 wraps as ``WorkspaceBootError(category=
      'adapter-attach')`` per D48 §B.2 REUSE — no new FAILURE_CATEGORIES
      needed.

      §B.2 Inbound tool-call failure (NEW shape parallel to D73 §B.3): the
      registered ``@server.call_tool()`` handler catches specialist.handle_skill
      exceptions and surfaces them via ``mcp.shared.exceptions.McpError`` with
      JSON-RPC error code (server-side error surface; the ClientSession's
      ``call_tool`` call propagates the McpError to the caller). Server task
      stays alive — per-call exceptions do not abort the server. NOT
      AdapterCallError — this adapter IS the server; no caller exists in the
      framework process for the inbound side.

      §B.3 Tool-not-found at @call_tool: ``McpError`` raised with JSON-RPC
      code -32601 (Method not found) per the spec. The SDK turns the unknown
      tool name into a McpError when ``call_tool`` is invoked with an
      unregistered name.

      §B.4 Skill-not-publicly-exposed at @call_tool: same surface as §B.3
      — the handler returns ``McpError(-32601)`` because the skill is not
      part of the exposed tool surface (filter is authoritative at both
      list_tools aggregator AND call_tool dispatch).

    Per D21 §generalization (workspace-as-MCP-server) + D60 publicly-exposed
    slot semantics: the skill aggregator walks
    ``workspace._substrate.specialist_instances`` (per D19 + substrate.py:
    specialist_instances registry); for each specialist's ``spec.skills[]``
    entry filtered by ``publicly-exposed=True``, builds a ``mcp.types.Tool``
    entry. Tool name convention: ``"<binding_id>.<skill_id>"`` to prevent
    name collision across specialists in the same workspace; reverse-mapping
    splits on the first ``.`` to route at call_tool time. Dot separator
    chosen per MCP SEP-986 tool-name character set (A-Z / a-z / 0-9 / _ /
    - / .); colon would warn at server registration.

    NO outbound ``adapter.call()`` impl — c6 IS server; outbound peer-as-server
    (cross-impl) is explicitly deferred per D74 §D. Calling ``call()`` raises
    ``NotImplementedError`` with a diagnostic message naming the deferral.
    """

    _outcome_prefix: ClassVar[str] = "mcp-server"

    # Per-instance test-injection hook. When set, ``attach_workspace`` calls
    # ``factory(self)`` instead of constructing the default
    # ``mcp.server.lowlevel.Server``. Default behavior: construct a real SDK
    # Server keyed off ``workspace.workspace_id``. Tests can override the
    # factory to inject a stubbed Server for unit-shape coverage; the
    # canonical in-process round-trip uses the default factory.
    _server_factory: Optional[Callable[..., Any]] = field(
        default=None, repr=False
    )

    # Per-instance pre-built server. Populated by attach_workspace. Read by
    # the test harness (which drives create_connected_server_and_client_session
    # against it) and by future production transport hooks.
    _server: Any = field(default=None, repr=False)

    # ---------------------------------------------------------------
    # Server lifecycle (attach builds the SDK Server + registers handlers)
    # ---------------------------------------------------------------

    def attach_workspace(self, workspace: Any) -> None:
        """Wire workspace + construct the SDK Server with registered handlers.

        Per D48 §B.2: any Exception from SDK Server construction or handler
        registration propagates out and is wrapped at boot.py:599 as
        ``WorkspaceBootError(category='adapter-attach')`` per the existing
        REUSE path (no new category needed).

        Decorators ``@server.list_tools()`` and ``@server.call_tool()``
        register the closures that reference ``self`` to access
        ``workspace._substrate.specialist_instances`` at request time. Per
        D74 §B.1: there is NO long-running server task started here;
        production transport binding (stdio / sse / http) is deferred per
        D74 §D.
        """
        super().attach_workspace(workspace)

        # Resolve factory: per-instance override (test injection) OR the
        # default that builds an mcp.server.lowlevel.Server. The default
        # is the production path (an SDK Server ready for stdio / sse /
        # http transport binding) but Phase C scope = in-process self-test
        # only per scope-cut C12.
        factory = self._server_factory
        if factory is None:
            factory = _default_mcp_server_factory

        self._server = factory(self)

    @property
    def server(self) -> Any:
        """The MCP SDK Server instance built at attach_workspace.

        Test harnesses pass this to
        ``mcp.shared.memory.create_connected_server_and_client_session(server)``
        to drive the in-process self-test round-trip per D74 §B + closure
        item (b). None until ``attach_workspace`` has been called.
        """
        return self._server

    # ---------------------------------------------------------------
    # Tool aggregation (per D21 §generalization + D60)
    # ---------------------------------------------------------------

    def build_tools(self) -> list:
        """Walk specialist_instances + return publicly-exposed skills as Tools.

        Per D21 §generalization (workspace-as-MCP-server) + D60: filters
        ``specialist.skills[]`` by ``publicly-exposed=True``; maps each to
        ``mcp.types.Tool`` with name ``"<binding_id>:<skill_id>"`` (binding-
        id prefix prevents skill_id collision across specialists in the
        same workspace).

        Returns:
            list[mcp.types.Tool] in canonical SDK shape; empty list when
            no workspace attached OR no publicly-exposed skills declared.
        """
        from mcp import types as t

        tools: list = []
        if self._workspace is None:
            return tools
        substrate = self._workspace._substrate
        for binding_id, specialist in substrate.specialist_instances.items():
            for skill in specialist.skills:
                if skill.get("publicly-exposed") is not True:
                    continue
                skill_id = skill.get("id")
                if not skill_id:
                    continue
                tool_name = f"{binding_id}.{skill_id}"
                tools.append(
                    t.Tool(
                        name=tool_name,
                        description=skill.get(
                            "description", f"specialist skill {skill_id}"
                        ),
                        inputSchema={
                            "type": "object",
                            "additionalProperties": True,
                        },
                    )
                )
        return tools

    # ---------------------------------------------------------------
    # Tool routing (per D74 §B.2: inbound call → specialist.handle_skill)
    # ---------------------------------------------------------------

    def route_tool_call(self, tool_name: str, arguments: Optional[dict]) -> Any:
        """Route an inbound MCP tool-call to a specialist's handle_skill.

        Per D74 §B.2 + §B.3 + §B.4: looks up the specialist + skill_id by
        reverse-mapping the tool name (``"<binding_id>.<skill_id>"``); if
        the name format is wrong, the binding_id has no specialist, the
        skill_id is unknown, or the skill is NOT publicly-exposed, raises
        ``McpError`` with code -32601 (Method not found). Otherwise invokes
        ``specialist.handle_skill(skill_id, params)`` and returns the
        result.

        If ``handle_skill`` itself raises (D50 SkillExecutionError, an
        AdapterCallError from chained adapter.call, or arbitrary Exception),
        the exception is wrapped as ``McpError`` per D74 §B.2 (server-side
        error surface; ClientSession's call_tool propagates to the caller).
        """
        from mcp.shared.exceptions import McpError
        from mcp.types import ErrorData

        if self._workspace is None:
            raise McpError(
                ErrorData(
                    code=-32603,
                    message=(
                        "adapter not attached to a workspace; "
                        "call attach_workspace first"
                    ),
                )
            )

        # Reverse-map tool name to (binding_id, skill_id). The convention is
        # ``"<binding_id>.<skill_id>"`` (built in build_tools above; dot
        # separator per MCP SEP-986 tool-name character set).
        if "." not in tool_name:
            raise McpError(
                ErrorData(
                    code=-32601,
                    message=(
                        f"unknown MCP tool name {tool_name!r}: expected "
                        "format '<binding_id>.<skill_id>'"
                    ),
                )
            )
        binding_id, _, skill_id = tool_name.partition(".")

        substrate = self._workspace._substrate
        specialist = substrate.specialist_instances.get(binding_id)
        if specialist is None:
            raise McpError(
                ErrorData(
                    code=-32601,
                    message=(
                        f"unknown MCP tool name {tool_name!r}: no specialist "
                        f"binding {binding_id!r}"
                    ),
                )
            )

        # Verify the skill is BOTH declared AND publicly-exposed. Filter is
        # authoritative at call_tool entry — internal-only skills are not
        # invokable via the MCP server surface (parallel to D73 §B.3 +
        # §"Per-skill exposure control" — by-obscurity bypass would be
        # incorrect).
        matching_skill = None
        for skill in specialist.skills:
            if skill.get("id") == skill_id:
                matching_skill = skill
                break
        if matching_skill is None or (
            matching_skill.get("publicly-exposed") is not True
        ):
            raise McpError(
                ErrorData(
                    code=-32601,
                    message=(
                        f"unknown MCP tool name {tool_name!r}: skill "
                        f"{skill_id!r} not exposed by specialist "
                        f"{binding_id!r}"
                    ),
                )
            )

        params = arguments or {}
        try:
            return specialist.handle_skill(skill_id, params)
        except McpError:
            # Specialist raised an MCP-shaped error directly — propagate
            # without rewrapping.
            raise
        except Exception as exc:
            # Per D74 §B.2: server-side error surface. The framework process
            # is the receiver (no AdapterCallError consumer); wrap as
            # McpError(-32603) Internal-error per JSON-RPC 2.0 spec with the
            # underlying exception's type + message preserved for caller
            # diagnostic visibility. Exception chained via ``from``.
            raise McpError(
                ErrorData(
                    code=-32603,
                    message=(
                        f"skill {skill_id!r} on specialist {binding_id!r} "
                        f"failed: {type(exc).__name__}: {exc}"
                    ),
                )
            ) from exc

    # ---------------------------------------------------------------
    # Outbound call() — NOT IMPLEMENTED for c6 per D74 §D
    # ---------------------------------------------------------------

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """NOT IMPLEMENTED for the server-side adapter per D74 §D.

        c6 (MCPServerAdapter) IS the server; outbound peer-as-server
        (workspace acting as a client of another workspace's MCP server)
        is a cross-impl deferral — the existing
        ``RealWireMCPClientAdapter`` (D71) covers the client side. Calling
        this method raises ``NotImplementedError`` with a diagnostic
        message naming the deferral.
        """
        raise NotImplementedError(
            f"MCPServerAdapter {self.id!r} is the SERVER side; outbound "
            "peer-as-server is deferred per D74 §D — bind a "
            "RealWireMCPClientAdapter (mcp-server-ext:mcp-client-realwire) "
            "for outbound MCP calls."
        )


def _default_mcp_server_factory(adapter: "MCPServerAdapter") -> Any:
    """Build the default MCP SDK Server with handlers registered.

    Per D74 §B: constructs ``mcp.server.lowlevel.Server`` named off the
    workspace id; registers ``@server.list_tools()`` + ``@server.call_tool()``
    closures that reference ``adapter`` for substrate access at request
    time.

    @list_tools returns the aggregator output (per D21 §generalization +
    D60 publicly-exposed filter).

    @call_tool dispatches to ``adapter.route_tool_call`` (per D74 §B.2 +
    §B.3 + §B.4 error surface). On success returns a list of
    ``mcp.types.TextContent`` blocks carrying the JSON-serialized
    ``handle_skill`` return.
    """
    from mcp.server.lowlevel import Server
    from mcp import types as t

    workspace_id = (
        adapter._workspace.workspace_id
        if adapter._workspace is not None
        else adapter.id
    )
    server = Server(workspace_id)

    @server.list_tools()
    async def _list_tools() -> list:
        return adapter.build_tools()

    @server.call_tool()
    async def _call_tool(name: str, arguments: Optional[dict]) -> list:
        result = adapter.route_tool_call(name, arguments)
        # Serialize the handle_skill return as JSON text content. The
        # specialist may return any JSON-serializable shape (dict / list /
        # primitive); fall back to ``str()`` if json.dumps cannot encode.
        import json as _json

        try:
            text = _json.dumps(result, default=str)
        except Exception:
            text = str(result)
        return [t.TextContent(type="text", text=text)]

    return server


@dataclass
class ProvJsonExportAdapter(Adapter):
    """Phase C real-wire PROV-JSON export adapter per D77 §B (closes C9;
    closes Phase C closure item — standards-compatibility engagement at
    impl-level per D68 §A5 split).

    Per D77 §B.1 + D24 standards-compat tracker + W3C PROV-DM 2013-04-30
    spec + W3C PROV-JSON 2014-04-30 spec: workspace-side EXPORT-ONLY
    adapter that converts the workspace event chain into a W3C PROV-JSON
    document. NEW adapter sub-shape: **export-only** — no inbound surface
    (unlike a2a-peer-ext / mcp-server-side-ext server-side adapters which
    accept inbound requests); no outbound real-wire reach (unlike the
    real-wire client adapters which POST/dispatch over HTTP/JSON-RPC).
    The call surface is a synchronous conversion that either returns the
    PROV-JSON dict OR writes a file at the caller-supplied output-path.

    Per D77 §A (NON-BREAKING contract): fresh-plan event envelope is
    UNCHANGED. PROV-JSON is a one-way export-time serialization of the
    canonical fresh-plan chain. Future export adapters (OpenTelemetry /
    AsyncAPI / Activity Streams per D24 carry-overs) register at the same
    EXPORT-ONLY sub-shape per D29 namespacing.

    Per D45 + D77 §B.2 triad applied per path:

      §B.2 Conversion + IO failure path: pre-export ``action`` event
      emitted via ``_emit_action`` per D71 pre-wire convention; if
      ``standards_export.event_chain_to_prov_json`` raises ``ValueError``
      (malformed event envelope), the adapter wraps as
      ``AdapterCallError(category='protocol-error')`` per D48 §D D-3
      starter category vocabulary REUSE. If file IO fails (read-only
      target / permission denied / disk full), the adapter wraps as
      ``AdapterCallError(category='transport')`` per D48 §D D-3 REUSE.
      Catch-all on unexpected exception types → ``category='unknown'``.

    Per scope-cut C12 (Phase C autopilot constraint): in-process tests
    only via pytest ``tmp_path`` fixtures; no real export-target reach.
    Production deployment-specific PROV-O practitioner-shape mappings +
    per-payload-subtype prov:Entity assertion + EU AI Act Article 12
    audit-record-bundle format are deferred per D77 §D / D24 / D68 §D
    external-trigger 2026-08-02.

    Configuration (per D57 §B.1 opaque pass-through):
      - ``output-path`` (str, optional) — filesystem path. When set,
        ``call('export', ...)`` writes the PROV-JSON document to this
        path AND returns the dict in the result. When absent, call()
        returns the dict without filesystem side-effects (useful for
        in-memory inspection / piping into another export step).
      - ``output-path`` may also be supplied at call() time via the
        ``parameters`` argument — the call-time value overrides the
        configuration-time value when both are present.
    """

    _outcome_prefix: ClassVar[str] = "prov-json-export"

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Export the workspace event chain to PROV-JSON.

        Per D77 §B.2 + D71 pre-wire convention: emit action event BEFORE
        the conversion call so the export is itself attribution-recorded
        in the chain. Then invoke ``standards_export.event_chain_to_prov_json``
        on the workspace's event chain (excluding the just-emitted action
        event to keep export-side-effect separate from exported content).

        Args:
            tool_name: call dispatch identifier. ``"export"`` is the
                canonical operation. Unknown names fall through to the
                same conversion path (the adapter has one operation).
            parameters: optional call-time parameters:
                - ``output-path``: filesystem path to write the JSON
                  document to (overrides ``configuration.output-path``).
            attributing_actor_id: optional actor id for the action event
                attribution.

        Returns:
            dict with shape::

                {
                    "outcome-reference": "prov-json-export-<n>",
                    "ok": True,
                    "activity-count": <int>,
                    "agent-count": <int>,
                    "attribution-count": <int>,
                    "output-path": <str or None>,
                    "prov-json": <PROV-JSON document dict>,
                }

        Raises:
            AdapterCallError: per §B.2 triad — category='protocol-error'
                for malformed event envelope (ValueError from converter);
                category='transport' for file IO failure; category=
                'unknown' for unexpected exceptions.
        """
        from fresh_plan.runtime import standards_export

        params = parameters or {}
        # Pre-export action event per D71 pre-wire convention.
        outcome_reference = self._emit_action(
            tool_name, params, attributing_actor_id
        )

        if self._workspace is None:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="unknown",
                detail={
                    "reason": "adapter not attached to a workspace",
                },
            )

        # Resolve effective output-path: call-time overrides configuration.
        config = self.configuration or {}
        output_path_str = params.get("output-path") or config.get(
            "output-path"
        )

        # Walk events; drop the just-emitted pre-export action event from
        # the export payload so the export-side-effect is recorded in the
        # chain (transparency) but not in the exported PROV document
        # (otherwise every export would carry a meta-event referring to
        # itself, polluting the workspace's substantive provenance).
        chain = list(self._workspace._substrate.event_chain.all_events())
        # The last event is the action we just emitted; exclude it.
        if chain and chain[-1].get("payload", {}).get(
            "outcome-reference"
        ) == outcome_reference:
            chain = chain[:-1]

        workspace_id = self._workspace.workspace_id

        try:
            if output_path_str is not None:
                output_path = Path(output_path_str)
                prov_doc = standards_export.write_prov_json(
                    chain, workspace_id, output_path
                )
            else:
                prov_doc = standards_export.event_chain_to_prov_json(
                    chain, workspace_id
                )
        except ValueError as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="protocol-error",
                detail={
                    "reason": "PROV-JSON conversion: malformed event envelope",
                    "error": str(exc),
                },
            ) from exc
        except OSError as exc:
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="transport",
                detail={
                    "reason": "PROV-JSON file write failed",
                    "output-path": output_path_str,
                    "error": str(exc),
                },
            ) from exc
        except Exception as exc:  # pragma: no cover - catch-all
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="unknown",
                detail={
                    "reason": "PROV-JSON export: unexpected error",
                    "error": str(exc),
                    "error-type": type(exc).__name__,
                },
            ) from exc

        return {
            "outcome-reference": outcome_reference,
            "ok": True,
            "activity-count": len(prov_doc.get("activity", {})),
            "agent-count": len(prov_doc.get("agent", {})),
            "attribution-count": len(prov_doc.get("wasAttributedTo", {})),
            "output-path": output_path_str,
            "prov-json": prov_doc,
        }


# Module-level registry of (protocol-or-transport → runtime class). Populated
# as new adapter impls land. Phase C real-wire impls add alongside Phase B
# stubs (per D41 two-substrate parity precedent + D69 substrate-alongside
# pattern) rather than replacing them — preserves 0.1.0 stub path for back-
# compat + lets workspaces opt into real-wire by binding the 0.2.0 provision.
_ADAPTER_CLASSES: dict[str, type[Adapter]] = {
    "mcp-server-ext:mcp-client": MCPToolAdapter,
    "mcp-server-ext:mcp-client-realwire": RealWireMCPClientAdapter,
    "direct-api-ext:direct-api": DirectAPIAdapter,
    "direct-api-ext:direct-api-realwire": RealWireDirectAPIAdapter,
    "a2a-peer-ext:a2a-peer": A2APeerAdapter,
    "mcp-server-side-ext:mcp-server": MCPServerAdapter,
    "prov-json-export-ext:prov-json-export": ProvJsonExportAdapter,
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
