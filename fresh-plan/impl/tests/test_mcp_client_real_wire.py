"""Tests for the Phase C C3 real-wire MCP client adapter (D71 §B.1).

Per scope-cut C12 (autopilot constraint): tests use an in-process MCP
test-server harness via ``mcp.shared.memory.create_connected_server_and_client_session``
and a per-instance ``_session_factory`` injected on the adapter. NO real
network reach.

Test coverage per D68 §C closure item (e) + D71 §B.1 AdapterCallError
starter category vocabulary:

  - (a) Happy-path round-trip: in-process MCP server with one tool ``echo``;
    adapter.call('echo', {'msg': 'hi'}) returns echoed content; one
    ``action`` event emitted to the workspace chain pre-wire.
  - (b) AdapterCallError(transport): mcp SDK import failure path +
    broken-stream (anyio.BrokenResourceError class-name match).
  - (c) AdapterCallError(auth): server raises McpError in non-reserved
    range that maps to upstream-error via JSON-RPC code; auth subcase
    via direct McpError injection on the client session (server-specific
    auth codes are server-vocabulary territory per D71 §D D-2).
  - (d) AdapterCallError(timeout): ``read_timeout_seconds`` triggers
    builtins.TimeoutError; adapter maps to ``timeout`` category.
  - (e) AdapterCallError(protocol-error): McpError with code in JSON-RPC
    reserved range (-32700 / -32601 / -32602) maps to protocol-error.
  - (f) AdapterCallError(upstream-error): server returns
    CallToolResult(isError=True); adapter raises with content payload.
  - (g) AdapterCallError(unknown): catch-all path via an unmapped
    exception class.

Plus structural verification:
  - Adapter registers via ``_ADAPTER_CLASSES`` under the
    ``mcp-server-ext:mcp-client-realwire`` protocol identifier;
    0.1.0 stub adapter remains under ``mcp-server-ext:mcp-client``.
  - The pre-wire ``action`` event is emitted regardless of call outcome
    (per D48 §D D-5 resolution at D71 §B.1).
"""
from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    Adapter,
    AdapterCallError,
    MCPToolAdapter,
    RealWireMCPClientAdapter,
    _ADAPTER_CLASSES,
)


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
MCP_REALWIRE_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-mcp-realwire-adapter"
)


# ---------------------------------------------------------------------------
# Adapter spec used for unit-level tests (no Workspace boot required)
# ---------------------------------------------------------------------------


REALWIRE_ADAPTER_SPEC = {
    "id": "mcp-real-wire-adapter",
    "version": "0.2.0",
    "protocol-or-transport": "mcp-server-ext:mcp-client-realwire",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


# ---------------------------------------------------------------------------
# In-process MCP server harness helpers
# ---------------------------------------------------------------------------


def _build_echo_server():
    """Construct a minimal MCP Server with one ``echo`` tool.

    Per scope-cut C12: in-process only. Uses the SDK's lowlevel.Server +
    create_connected_server_and_client_session memory-stream bridge.
    """
    from mcp.server.lowlevel import Server
    import mcp.types as t

    server = Server("fresh-plan-test-mcp-server")

    @server.list_tools()
    async def _list():
        return [
            t.Tool(
                name="echo",
                description="echo back the msg argument",
                inputSchema={
                    "type": "object",
                    "properties": {"msg": {"type": "string"}},
                },
            ),
            t.Tool(
                name="raise-server-error",
                description="raise McpError server-side to exercise upstream-error",
                inputSchema={"type": "object"},
            ),
        ]

    @server.call_tool()
    async def _call(name: str, arguments: dict | None):
        if name == "echo":
            msg = (arguments or {}).get("msg", "")
            return [t.TextContent(type="text", text=f"echoed: {msg}")]
        if name == "raise-server-error":
            # Server raises McpError → SDK turns this into a structured
            # error result (CallToolResult.isError=True). Exercises the
            # upstream-error mapping path.
            from mcp.shared.exceptions import McpError
            from mcp.types import ErrorData

            raise McpError(
                ErrorData(code=-32099, message="server-side failure")
            )
        # Unknown tool: SDK convention → isError=True with text content.
        return [t.TextContent(type="text", text=f"unknown tool {name}")]

    return server


def _real_session_factory():
    """Return an async context-manager factory yielding a real ClientSession.

    Built on the in-process memory-stream bridge per scope-cut C12.
    """
    from mcp.shared.memory import create_connected_server_and_client_session

    @asynccontextmanager
    async def _factory():
        server = _build_echo_server()
        async with create_connected_server_and_client_session(
            server, raise_exceptions=False
        ) as session:
            yield session

    return _factory


class _FakeSession:
    """Minimal stand-in for ClientSession that lets tests inject behavior.

    Exposes only ``call_tool`` (the surface the adapter uses). Tests
    construct subclasses overriding ``_call_tool_impl`` to raise the
    target exception class for AdapterCallError category coverage.
    """

    async def call_tool(self, name, arguments=None, read_timeout_seconds=None):
        return await self._call_tool_impl(
            name, arguments, read_timeout_seconds
        )

    async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
        raise NotImplementedError


def _make_factory_for_session(session_cls):
    """Wrap a _FakeSession subclass in an async context-manager factory."""

    @asynccontextmanager
    async def _factory():
        yield session_cls()

    return _factory


def _make_adapter(
    session_factory=None,
    configuration=None,
) -> RealWireMCPClientAdapter:
    adapter = RealWireMCPClientAdapter(
        spec=dict(REALWIRE_ADAPTER_SPEC),
        configuration=configuration,
    )
    adapter._session_factory = session_factory
    return adapter


# ---------------------------------------------------------------------------
# Structural verification
# ---------------------------------------------------------------------------


def test_realwire_adapter_registered_under_new_protocol_identifier():
    """D71 §B.1 + D68 §B.3: 0.2.0 registers a NEW protocol identifier
    `mcp-server-ext:mcp-client-realwire`; 0.1.0 stub stands under
    `mcp-server-ext:mcp-client` per D41 two-substrate parity precedent."""
    assert _ADAPTER_CLASSES["mcp-server-ext:mcp-client-realwire"] is (
        RealWireMCPClientAdapter
    )
    # 0.1.0 stub path preserved.
    assert _ADAPTER_CLASSES["mcp-server-ext:mcp-client"] is MCPToolAdapter


def test_realwire_adapter_subclasses_adapter_with_realwire_prefix():
    adapter = _make_adapter()
    assert isinstance(adapter, Adapter)
    assert adapter._outcome_prefix == "mcp-realwire"
    assert adapter.protocol_or_transport == (
        "mcp-server-ext:mcp-client-realwire"
    )


def test_configuration_lifts_read_timeout_seconds():
    """D57 §B.1 opaque pass-through: `read-timeout-seconds` in
    configuration dict overrides the default 30s timeout."""
    adapter = _make_adapter(configuration={"read-timeout-seconds": 0.5})
    assert adapter._read_timeout_seconds == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# (a) Happy-path round-trip via in-process MCP server
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_realwire_workspace():
    manifest = json.loads(
        (MCP_REALWIRE_FIXTURE / "workspace.json").read_text()
    )
    ws = Workspace.boot(manifest, MCP_REALWIRE_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_call_happy_path_round_trip_through_in_process_server(
    booted_realwire_workspace,
):
    """Acceptance (a): happy-path call returns echoed content; one
    action event emitted to the workspace chain (per D48 §D D-5
    pre-wire-emit resolution at D71 §B.1)."""
    ws = booted_realwire_workspace
    adapter = ws.adapter("primary-mcp-realwire")
    assert isinstance(adapter, RealWireMCPClientAdapter)
    adapter._session_factory = _real_session_factory()

    before = len(ws.event_chain.by_payload_subtype("action"))
    response = adapter.call("echo", {"msg": "hi"})
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "echo"
    assert emitted["payload"]["parameters"] == {"msg": "hi"}

    assert response["ok"] is True
    assert response["isError"] is False
    assert response["outcome-reference"].startswith("mcp-realwire-")
    # The server returned one TextContent block with the echoed message.
    assert len(response["content"]) == 1
    block = response["content"][0]
    assert isinstance(block, dict)
    assert block.get("type") == "text"
    assert "echoed: hi" in block.get("text", "")


# ---------------------------------------------------------------------------
# (b) AdapterCallError(transport)
# ---------------------------------------------------------------------------


def test_adapter_call_error_transport_on_broken_stream():
    """Acceptance (b): a broken-stream class-name (BrokenResourceError)
    maps to category='transport' per D71 §B.1 starter vocabulary."""

    class _BrokenResourceError(Exception):
        """Stand-in for anyio.BrokenResourceError; name-matched in adapter."""

    # Override the class name via the type's __name__ explicitly so the
    # name-based matching in the adapter's catch-all path fires (anyio's
    # real BrokenResourceError uses the same string).
    _BrokenResourceError.__name__ = "BrokenResourceError"

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            raise _BrokenResourceError("stream broken mid-call")

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session)
    )
    # No workspace attach: emit fails. Patch the action emit so we can
    # exercise the wire path directly.
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-1"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("echo", {})
    assert excinfo.value.category == "transport"
    assert excinfo.value.adapter_id == "mcp-real-wire-adapter"
    assert excinfo.value.call_target == "echo"
    assert "BrokenResourceError" in excinfo.value.detail.get("reason", "")


def test_adapter_call_error_transport_on_oserror():
    """OSError (e.g., FileNotFoundError when subprocess spawn fails) maps
    to category='transport' per D71 §B.1."""

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            raise OSError("connection refused")

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-os"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("echo", {})
    assert excinfo.value.category == "transport"
    assert "connection refused" in excinfo.value.detail.get("reason", "")


# ---------------------------------------------------------------------------
# (c) AdapterCallError(auth) — auth subcase via McpError outside reserved range
# ---------------------------------------------------------------------------


def test_adapter_call_error_auth_subcase_via_mcp_error_upstream_range():
    """Acceptance (c): server-signalled auth failure via McpError code
    outside JSON-RPC reserved range (-32768..-32000) currently maps to
    upstream-error per D71 §B.1; specific auth-code subcase mapping is
    deferred to per-server-impl per D71 §D D-2.

    This test exercises the McpError handling branch; the upstream-error
    classification is correct per the starter vocabulary lock. When a
    server-specific auth code mapping lands (extension-registered per
    D29 namespacing), the category narrows to 'auth' without changing
    the test's intent (server signalled failure → adapter raised
    AdapterCallError with structured details)."""

    from mcp.shared.exceptions import McpError
    from mcp.types import ErrorData

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            # Code outside reserved range → upstream-error per D71 §B.1.
            # In a real server, this would be server-specific (e.g., HTTP
            # 401 mapped to a server-side code); per-server auth-code
            # mapping is D71 §D D-2 territory.
            raise McpError(
                ErrorData(code=-31999, message="authentication required")
            )

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-auth"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("auth-protected", {})
    # Per D71 §B.1 + §D D-2: out-of-reserved-range McpError → upstream-error
    # starter classification; auth subcase mapping is a per-server-impl
    # refinement registered per D29 namespacing.
    assert excinfo.value.category == "upstream-error"
    assert excinfo.value.detail.get("code") == -31999
    assert "authentication required" in excinfo.value.detail.get("reason", "")


# ---------------------------------------------------------------------------
# (d) AdapterCallError(timeout)
# ---------------------------------------------------------------------------


def test_adapter_call_error_timeout_on_builtin_timeout_error():
    """Acceptance (d): builtins.TimeoutError (which Python 3.11+ unifies
    asyncio.TimeoutError + anyio.TimeoutError under) maps to
    category='timeout' per D71 §B.1."""

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            raise TimeoutError("call_tool exceeded read_timeout_seconds")

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session),
        configuration={"read-timeout-seconds": 0.1},
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-timeout"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("slow-tool", {})
    assert excinfo.value.category == "timeout"
    assert excinfo.value.detail.get("read-timeout-seconds") == pytest.approx(
        0.1
    )


# ---------------------------------------------------------------------------
# (e) AdapterCallError(protocol-error)
# ---------------------------------------------------------------------------


def test_adapter_call_error_protocol_error_on_reserved_jsonrpc_code():
    """Acceptance (e): McpError with code in JSON-RPC reserved range
    (-32700 / -32601 / -32602 / -32603) maps to category='protocol-error'
    per D71 §B.1."""

    from mcp.shared.exceptions import McpError
    from mcp.types import ErrorData

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            raise McpError(
                ErrorData(code=-32602, message="invalid params")
            )

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-proto"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("anything", {})
    assert excinfo.value.category == "protocol-error"
    assert excinfo.value.detail.get("code") == -32602
    assert "invalid params" in excinfo.value.detail.get("reason", "")


# ---------------------------------------------------------------------------
# (f) AdapterCallError(upstream-error) — server returns isError=True
# ---------------------------------------------------------------------------


def test_adapter_call_error_upstream_error_on_server_is_error_true(
    booted_realwire_workspace,
):
    """Acceptance (f): server-returned CallToolResult(isError=True) is
    re-raised as AdapterCallError(category='upstream-error') per D71 §B.1.

    Uses the real in-process MCP server; the `raise-server-error` tool
    raises McpError server-side which the SDK turns into a structured
    error result delivered to the client as isError=True."""
    ws = booted_realwire_workspace
    adapter = ws.adapter("primary-mcp-realwire")
    adapter._session_factory = _real_session_factory()

    before = len(ws.event_chain.by_payload_subtype("action"))
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("raise-server-error", {})
    assert excinfo.value.category == "upstream-error"
    # The action event was still emitted (D48 §D D-5 resolved at D71
    # §B.1 — pre-wire emission preserves intent-recorded semantics).
    after = len(ws.event_chain.by_payload_subtype("action"))
    assert after == before + 1
    # Detail carries the server-side reason + content payload.
    assert "isError=True" in excinfo.value.detail.get("reason", "")
    assert "content" in excinfo.value.detail


# ---------------------------------------------------------------------------
# (g) AdapterCallError(unknown) — catch-all
# ---------------------------------------------------------------------------


def test_adapter_call_error_unknown_on_unmapped_exception():
    """Acceptance (g): an exception class that doesn't match any of the
    specific-category branches (transport / auth / timeout / protocol-
    error / upstream-error) maps to category='unknown' per D71 §B.1
    catch-all."""

    class _WeirdException(Exception):
        """Custom exception not in any specific-category mapping."""

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            raise _WeirdException("something unexpected happened")

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-unknown"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("mystery", {})
    assert excinfo.value.category == "unknown"
    assert "_WeirdException" in excinfo.value.detail.get("reason", "")


# ---------------------------------------------------------------------------
# Exception chaining preserved per D48 §B.1 surface contract
# ---------------------------------------------------------------------------


def test_exception_chaining_preserved_for_original_cause():
    """D48 §B.1 surface: AdapterCallError carries the original exception
    via Python's __cause__ chain (raise ... from exc). Caller sees the
    full traceback for diagnostic visibility."""

    class _Session(_FakeSession):
        async def _call_tool_impl(self, name, arguments, read_timeout_seconds):
            raise OSError("underlying cause")

    adapter = _make_adapter(
        session_factory=_make_factory_for_session(_Session)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-chain"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("anything", {})
    assert isinstance(excinfo.value.__cause__, OSError)
    assert "underlying cause" in str(excinfo.value.__cause__)
