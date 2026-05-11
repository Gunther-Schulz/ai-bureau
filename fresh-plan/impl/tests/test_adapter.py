"""Tests for the B4 + B5 stub adapters (MCP-server + direct-api) per D16 + D2 + D29."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    Adapter,
    DirectAPIAdapter,
    MCPToolAdapter,
    load_adapter_from_provision,
)


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
MCP_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-mcp-adapter"
DIRECT_API_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-direct-api-adapter"


ADAPTER_SPEC = {
    "id": "mcp-tool-adapter",
    "version": "0.1.0",
    "protocol-or-transport": "mcp-server-ext:mcp-client",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


@pytest.fixture
def adapter() -> MCPToolAdapter:
    return MCPToolAdapter(spec=dict(ADAPTER_SPEC))


@pytest.fixture
def booted_workspace():
    manifest = json.loads((MCP_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, MCP_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_mcp_tool_adapter_accessors(adapter):
    assert adapter.id == "mcp-tool-adapter"
    assert adapter.version == "0.1.0"
    assert adapter.protocol_or_transport == "mcp-server-ext:mcp-client"
    assert adapter.required_substrate_capabilities == []
    assert adapter.declared_event_emissions == [{"payload-subtype": "action"}]
    assert adapter.declared_event_consumptions == []


def test_call_before_attach_raises(adapter):
    with pytest.raises(RuntimeError) as excinfo:
        adapter.call("echo", {"x": 1})
    assert "attach_workspace" in str(excinfo.value)


def test_call_after_attach_returns_stub_response(booted_workspace):
    ws = booted_workspace
    adapter = ws.adapter("primary-mcp")
    response = adapter.call("echo", {"x": 1})
    assert response["ok"] is True
    assert response["stub"] is True
    assert response["tool"] == "echo"
    assert response["parameters"] == {"x": 1}
    assert response["outcome-reference"].startswith("mcp-stub-")


def test_call_emits_one_action_event(booted_workspace):
    ws = booted_workspace
    adapter = ws.adapter("primary-mcp")
    before = len(ws.event_chain.by_payload_subtype("action"))
    response = adapter.call("plan", {"target": "doc-1"})
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "plan"
    assert emitted["payload"]["parameters"] == {"target": "doc-1"}
    assert emitted["payload"]["outcome-reference"] == response["outcome-reference"]


def test_call_emitted_event_passes_generic_shape_authority_check(booted_workspace):
    """generic-shape has no authority-binding for `action`, so the emit must
    succeed without a role hint (verifies B3 + B4 compose)."""
    ws = booted_workspace
    adapter = ws.adapter("primary-mcp")
    # No EventRejected raised; response returned cleanly.
    response = adapter.call("noop", {})
    assert response["ok"] is True


def test_load_adapter_from_provision_finds_impl_shipped_mcp_tool_adapter():
    adapter = load_adapter_from_provision(
        "mcp-server-ext:mcp-tool-adapter", IMPL_EXTENSIONS_DIR
    )
    assert isinstance(adapter, MCPToolAdapter)
    assert adapter.id == "mcp-tool-adapter"
    assert adapter.version == "0.1.0"
    assert adapter.protocol_or_transport == "mcp-server-ext:mcp-client"


# ---------------------------------------------------------------
# B5 — DirectAPIAdapter (parallel to the MCPToolAdapter tests above)
# ---------------------------------------------------------------


DIRECT_API_SPEC = {
    "id": "direct-api-adapter",
    "version": "0.1.0",
    "protocol-or-transport": "direct-api-ext:direct-api",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


@pytest.fixture
def direct_adapter() -> DirectAPIAdapter:
    return DirectAPIAdapter(spec=dict(DIRECT_API_SPEC))


@pytest.fixture
def booted_direct_workspace():
    manifest = json.loads((DIRECT_API_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, DIRECT_API_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_direct_api_adapter_accessors(direct_adapter):
    assert direct_adapter.id == "direct-api-adapter"
    assert direct_adapter.version == "0.1.0"
    assert direct_adapter.protocol_or_transport == "direct-api-ext:direct-api"
    assert direct_adapter.declared_event_emissions == [{"payload-subtype": "action"}]


def test_direct_api_call_before_attach_raises(direct_adapter):
    with pytest.raises(RuntimeError) as excinfo:
        direct_adapter.call("noop", {})
    assert "attach_workspace" in str(excinfo.value)


def test_direct_api_call_after_attach_returns_stub_response(booted_direct_workspace):
    ws = booted_direct_workspace
    adapter = ws.adapter("primary-direct")
    response = adapter.call("compute", {"x": 2})
    assert response["ok"] is True
    assert response["stub"] is True
    assert response["kind"] == "direct-api"
    assert response["tool"] == "compute"
    assert response["parameters"] == {"x": 2}
    assert response["outcome-reference"].startswith("direct-stub-")


def test_direct_api_call_emits_one_action_event(booted_direct_workspace):
    ws = booted_direct_workspace
    adapter = ws.adapter("primary-direct")
    before = len(ws.event_chain.by_payload_subtype("action"))
    response = adapter.call("compute", {"x": 2})
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "compute"
    assert emitted["payload"]["parameters"] == {"x": 2}
    assert emitted["payload"]["outcome-reference"] == response["outcome-reference"]


def test_load_adapter_dispatches_by_protocol_or_transport():
    """Loader returns the correct concrete subclass per spec.protocol-or-transport."""
    mcp = load_adapter_from_provision(
        "mcp-server-ext:mcp-tool-adapter", IMPL_EXTENSIONS_DIR
    )
    direct = load_adapter_from_provision(
        "direct-api-ext:direct-api-adapter", IMPL_EXTENSIONS_DIR
    )
    assert isinstance(mcp, MCPToolAdapter)
    assert isinstance(direct, DirectAPIAdapter)
    # Both share the Adapter base contract.
    assert isinstance(mcp, Adapter)
    assert isinstance(direct, Adapter)
