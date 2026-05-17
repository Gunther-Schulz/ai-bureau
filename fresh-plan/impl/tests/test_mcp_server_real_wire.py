"""Tests for the Phase C C6 real-wire MCP server adapter (D74 §B).

Per scope-cut C12 (autopilot constraint) + D68 §C closure item (b) — the
workspace's own MCP client invokes the workspace's own MCP server in
test fixture: the test fixture constructs the Workspace + reads the
adapter's prepared ``server`` attribute (populated by ``attach_workspace``)
and drives ``mcp.shared.memory.create_connected_server_and_client_session``
inside ``asyncio.run`` for the in-process round-trip. NO external MCP
client reach.

Test coverage per D74 §B (closes Phase C C6 per D68 §A + closure item (b)):

  - Structural verification:
    - MCPServerAdapter registered under ``mcp-server-side-ext:mcp-server``
      in the module ``_ADAPTER_CLASSES`` registry.
    - Subclasses Adapter with ``_outcome_prefix = "mcp-server"``.
    - attach_workspace builds an mcp.server.lowlevel.Server instance
      readable via ``adapter.server``.
  - Tool aggregation (D74 §B + D21 §generalization + D60 filter):
    - (a) list_tools → publicly-exposed=True skill present as MCP tool
      named ``"<binding_id>.<skill_id>"``.
    - (c) publicly-exposed=False skill is NOT in the list_tools output
      (filter semantics per D60).
  - Tool routing (D74 §B.2):
    - (b) call_tool round-trip → specialist.handle_skill invoked + result
      returned in mcp.types.TextContent block (closure item (b)).
    - (d) Unknown tool name → McpError(-32601) Method-not-found surfaced
      as CallToolResult(isError=True).
    - (e) specialist.handle_skill raises → McpError(-32603) Internal-error
      with handler exception name + message preserved.
    - (f) publicly-exposed=False skill_id at call_tool → McpError(-32601)
      (filter authoritative at BOTH list_tools AND call_tool surfaces).
  - Outbound call() not implemented per D74 §D:
    - adapter.call() raises NotImplementedError naming the deferral.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    Adapter,
    MCPServerAdapter,
    _ADAPTER_CLASSES,
)


MCP_SERVER_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-mcp-server-side-adapter"
)


# ---------------------------------------------------------------------------
# Adapter spec used for unit-level tests (no Workspace boot required)
# ---------------------------------------------------------------------------


MCP_SERVER_ADAPTER_SPEC = {
    "id": "mcp-server-side-adapter",
    "version": "0.1.0",
    "protocol-or-transport": "mcp-server-side-ext:mcp-server",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


# ---------------------------------------------------------------------------
# Structural verification
# ---------------------------------------------------------------------------


def test_mcp_server_adapter_registered_under_protocol_identifier():
    """D74 §B + D68 §B.3: MCPServerAdapter registered under
    `mcp-server-side-ext:mcp-server` in module `_ADAPTER_CLASSES`."""
    assert (
        _ADAPTER_CLASSES["mcp-server-side-ext:mcp-server"]
        is MCPServerAdapter
    )


def test_mcp_server_adapter_subclasses_adapter_with_outcome_prefix():
    adapter = MCPServerAdapter(spec=dict(MCP_SERVER_ADAPTER_SPEC))
    assert isinstance(adapter, Adapter)
    assert adapter._outcome_prefix == "mcp-server"
    assert adapter.protocol_or_transport == "mcp-server-side-ext:mcp-server"


# ---------------------------------------------------------------------------
# In-process server fixture (full Workspace boot)
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_mcp_server_workspace():
    manifest = json.loads(
        (MCP_SERVER_FIXTURE / "workspace.json").read_text()
    )
    ws = Workspace.boot(manifest, MCP_SERVER_FIXTURE / "extensions")
    adapter = ws.adapter("primary-mcp-server")
    try:
        yield ws, adapter
    finally:
        ws.shutdown()


def test_attach_workspace_builds_sdk_server(booted_mcp_server_workspace):
    """D74 §B.1: attach_workspace constructs an mcp.server.lowlevel.Server
    instance readable via the ``adapter.server`` property."""
    _ws, adapter = booted_mcp_server_workspace
    from mcp.server.lowlevel import Server

    assert isinstance(adapter.server, Server)


# ---------------------------------------------------------------------------
# Tool aggregation (D74 §B + D21 §generalization + D60 publicly-exposed)
# ---------------------------------------------------------------------------


def test_list_tools_returns_publicly_exposed_skills(
    booted_mcp_server_workspace,
):
    """Acceptance (a) + closure item (b): list_tools round-trip returns
    the workspace's publicly-exposed=True skills as MCP tools. Tool name
    follows ``<binding_id>.<skill_id>`` convention per D74 §B."""
    from mcp.shared.memory import create_connected_server_and_client_session

    _ws, adapter = booted_mcp_server_workspace

    async def _run():
        async with create_connected_server_and_client_session(
            adapter.server, raise_exceptions=False
        ) as session:
            return await session.list_tools()

    result = asyncio.run(_run())
    names = [tool.name for tool in result.tools]
    # Only the publicly-exposed=True "echo" skill of the "publisher"
    # specialist binding should appear.
    assert "publisher.echo" in names


def test_list_tools_filters_publicly_exposed_false(
    booted_mcp_server_workspace,
):
    """Acceptance (c): publicly-exposed=False skills are NOT in the
    list_tools output (D60 filter semantics)."""
    from mcp.shared.memory import create_connected_server_and_client_session

    _ws, adapter = booted_mcp_server_workspace

    async def _run():
        async with create_connected_server_and_client_session(
            adapter.server, raise_exceptions=False
        ) as session:
            return await session.list_tools()

    result = asyncio.run(_run())
    names = [tool.name for tool in result.tools]
    assert "publisher.internal-only" not in names


# ---------------------------------------------------------------------------
# Tool routing (D74 §B.2: call_tool → specialist.handle_skill)
# ---------------------------------------------------------------------------


def test_call_tool_routes_to_specialist_handle_skill(
    booted_mcp_server_workspace,
):
    """Acceptance (b) + closure item (b): call_tool round-trip invokes
    specialist.handle_skill(skill_id, params) and returns the result as
    TextContent. The GenericSpecialist stub emits one action event per
    handle_skill call; verifies the server-side specialist invocation
    actually drove the workspace's chain forward."""
    from mcp.shared.memory import create_connected_server_and_client_session

    ws, adapter = booted_mcp_server_workspace

    before = len(ws.event_chain.by_payload_subtype("action"))

    async def _run():
        async with create_connected_server_and_client_session(
            adapter.server, raise_exceptions=False
        ) as session:
            return await session.call_tool(
                "publisher.echo", {"msg": "hello"}
            )

    result = asyncio.run(_run())
    assert result.isError is False
    assert len(result.content) == 1
    text = result.content[0].text
    payload = json.loads(text)
    assert payload["ok"] is True
    assert payload["skill"] == "echo"
    assert payload["parameters"] == {"msg": "hello"}

    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "echo"
    assert emitted["payload"]["parameters"] == {"msg": "hello"}


def test_call_tool_unknown_name_surfaces_method_not_found(
    booted_mcp_server_workspace,
):
    """Acceptance (d) + D74 §B.3: an unknown tool name surfaces as
    McpError(-32601) — the ClientSession.call_tool delivers this as
    CallToolResult(isError=True) with the diagnostic message in content."""
    from mcp.shared.memory import create_connected_server_and_client_session

    _ws, adapter = booted_mcp_server_workspace

    async def _run():
        async with create_connected_server_and_client_session(
            adapter.server, raise_exceptions=False
        ) as session:
            return await session.call_tool("publisher.unknown-skill", {})

    result = asyncio.run(_run())
    assert result.isError is True
    assert len(result.content) >= 1
    text = result.content[0].text
    assert "unknown MCP tool name" in text
    assert "unknown-skill" in text


def test_call_tool_specialist_handle_skill_raises_surfaces_internal_error(
    booted_mcp_server_workspace,
):
    """Acceptance (e) + D74 §B.2: when specialist.handle_skill raises, the
    handler wraps as McpError(-32603) Internal-error preserving the
    underlying type + message; ClientSession.call_tool delivers as
    CallToolResult(isError=True)."""
    from mcp.shared.memory import create_connected_server_and_client_session

    ws, adapter = booted_mcp_server_workspace
    specialist = ws._substrate.specialist_instances["publisher"]
    # Monkey-patch handle_skill on the specialist instance to raise; the
    # handler should catch + wrap as McpError per D74 §B.2.
    orig_handle = specialist.handle_skill

    def _raising_handle(skill_id, params):
        raise RuntimeError("simulated skill body failure")

    specialist.handle_skill = _raising_handle  # type: ignore[method-assign]
    try:

        async def _run():
            async with create_connected_server_and_client_session(
                adapter.server, raise_exceptions=False
            ) as session:
                return await session.call_tool(
                    "publisher.echo", {"msg": "bad"}
                )

        result = asyncio.run(_run())
    finally:
        specialist.handle_skill = orig_handle  # type: ignore[method-assign]

    assert result.isError is True
    text = result.content[0].text
    # The McpError message embeds the underlying exception's type +
    # message per D74 §B.2 wrap-shape.
    assert "RuntimeError" in text
    assert "simulated skill body failure" in text


def test_call_tool_non_publicly_exposed_skill_surfaces_method_not_found(
    booted_mcp_server_workspace,
):
    """Acceptance (f) + D74 §B.4 + D60: publicly-exposed=False skills are
    filtered from BOTH list_tools AND call_tool routing. An attempt to
    invoke a non-publicly-exposed skill_id surfaces as McpError(-32601)
    — by-obscurity bypass is incorrect per D21 §"Per-skill exposure
    control"."""
    from mcp.shared.memory import create_connected_server_and_client_session

    _ws, adapter = booted_mcp_server_workspace

    async def _run():
        async with create_connected_server_and_client_session(
            adapter.server, raise_exceptions=False
        ) as session:
            return await session.call_tool(
                "publisher.internal-only", {}
            )

    result = asyncio.run(_run())
    assert result.isError is True
    text = result.content[0].text
    assert "internal-only" in text
    assert "not exposed" in text


def test_call_tool_binding_id_collision_routes_correctly(
    booted_mcp_server_workspace,
):
    """Tool name convention ``<binding_id>.<skill_id>`` prevents skill_id
    collision across specialists in the same workspace. Verified by
    asserting the route_tool_call helper rejects bare skill names (no
    dot separator) with McpError(-32601)."""
    from mcp.shared.exceptions import McpError

    _ws, adapter = booted_mcp_server_workspace
    with pytest.raises(McpError) as excinfo:
        adapter.route_tool_call("bare-name-no-dot", {})
    # The McpError carries ErrorData with code -32601 per JSON-RPC 2.0
    # method-not-found semantics.
    err_data = excinfo.value.error
    assert err_data.code == -32601
    assert "expected" in err_data.message
    assert "<binding_id>.<skill_id>" in err_data.message


# ---------------------------------------------------------------------------
# Outbound call() not implemented per D74 §D
# ---------------------------------------------------------------------------


def test_outbound_call_raises_not_implemented(booted_mcp_server_workspace):
    """D74 §D: c6 IS the server; outbound peer-as-server is deferred.
    Calling adapter.call() raises NotImplementedError with a diagnostic
    message naming the deferral + the alternate adapter to use for
    outbound MCP."""
    _ws, adapter = booted_mcp_server_workspace
    with pytest.raises(NotImplementedError) as excinfo:
        adapter.call("any-tool", {})
    msg = str(excinfo.value)
    assert "SERVER side" in msg
    assert "RealWireMCPClientAdapter" in msg
