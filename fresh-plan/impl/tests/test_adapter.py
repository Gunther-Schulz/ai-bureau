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


# ---------------------------------------------------------------
# D48 — adapter cluster supersedes per D45 §C
# ---------------------------------------------------------------


def test_adapter_call_error_propagates_with_structured_fields(booted_workspace):
    """D48 §B.1: AdapterCallError carries structured fields (adapter_id,
    call_target, category, detail) + chains the original exception via `from`.

    Phase B stubs cannot fail meaningfully; this test uses a monkeypatched
    subclass to exercise the forward-bar contract Phase C real-wire impls
    must honor.
    """
    from fresh_plan.runtime.adapter import AdapterCallError

    class _FailingAdapter(MCPToolAdapter):
        def call(self, tool_name, parameters=None, *, attributing_actor_id=None):
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="timeout",
                detail={"elapsed_ms": 30000, "limit_ms": 30000},
            )

    failing = _FailingAdapter(spec=dict(ADAPTER_SPEC))
    failing.attach_workspace(booted_workspace)

    with pytest.raises(AdapterCallError) as excinfo:
        failing.call("plan", {"target": "doc-1"})

    e = excinfo.value
    assert e.adapter_id == "mcp-tool-adapter"
    assert e.call_target == "plan"
    assert e.category == "timeout"
    assert e.detail == {"elapsed_ms": 30000, "limit_ms": 30000}
    # Structured diagnostic visible without reading server logs.
    assert "[timeout]" in str(e)
    assert "mcp-tool-adapter" in str(e)


def test_adapter_call_error_aggregated_via_subscriber_dispatch(booted_workspace):
    """D48 §B.1 composition with D47 §B.1: AdapterCallError raised inside a
    specialist's on_event (subscriber-dispatch path) is captured into
    substrate._subscriber_failures and aggregated as SubscriberDispatchError
    after the outer drain completes.
    """
    from fresh_plan.runtime.adapter import AdapterCallError
    from fresh_plan.runtime.specialist import Specialist
    from fresh_plan.runtime.substrate import SubscriberDispatchError

    class _FailingAdapter(MCPToolAdapter):
        def call(self, tool_name, parameters=None, *, attributing_actor_id=None):
            raise AdapterCallError(
                adapter_id=self.id,
                call_target=tool_name,
                category="upstream-error",
                detail={"status": 503},
            )

    class _ReactingSpecialist(Specialist):
        """Reacts to claim events by invoking the bound adapter — exercises
        the D44 + D47 + D48 composition path."""

        def __init__(self, spec, adapter):
            super().__init__(spec=spec)
            self._test_adapter = adapter
            self.spec.setdefault(
                "declared-event-subscriptions", [{"payload-subtype": "state-change"}]
            )

        def handle_skill(self, skill_id, params):
            return None

        def on_event(self, event):
            # Will raise AdapterCallError — captured per D47 §B.1.
            self._test_adapter.call("react-to-claim", {"event_id": event["id"]})

    failing = _FailingAdapter(spec=dict(ADAPTER_SPEC))
    failing.attach_workspace(booted_workspace)

    reacting = _ReactingSpecialist(
        spec={
            "id": "reacting-test-specialist",
            "version": "0.1.0",
            "roles": [],
            "skills": [],
            "supported-work-unit-kinds": [],
            "required-adapter-bindings": [],
            "declared-event-subscriptions": [{"payload-subtype": "state-change"}],
        },
        adapter=failing,
    )
    substrate = booted_workspace._substrate
    substrate.specialist_subscribers.append(reacting)

    actor_id = next(iter(substrate.state.actors))
    with pytest.raises(SubscriberDispatchError) as excinfo:
        booted_workspace._emit_event(
            actor_id=actor_id,
            payload_subtype="state-change",
            payload={"what": "test-state-change"},
        )

    failures = excinfo.value.failures
    assert len(failures) == 1
    spec_id, evt_id, captured_exc = failures[0]
    assert spec_id == "reacting-test-specialist"
    assert isinstance(captured_exc, AdapterCallError)
    assert captured_exc.category == "upstream-error"
    assert captured_exc.adapter_id == "mcp-tool-adapter"


def test_adapter_attach_failure_surfaces_as_workspace_boot_error(tmp_path):
    """D48 §B.2: when an adapter's attach_workspace raises, boot.py wraps
    as WorkspaceBootError(category="adapter-attach") naming the failing
    adapter-binding + the underlying cause.
    """
    from fresh_plan.runtime.adapter import _ADAPTER_CLASSES
    from fresh_plan.runtime.boot import WorkspaceBootError

    class _AttachFailingAdapter(MCPToolAdapter):
        def attach_workspace(self, workspace):
            raise RuntimeError("simulated Phase-C-style attach failure (e.g., auth handshake)")

    # Register the failing class against the MCP protocol so the existing
    # MCP fixture instantiates it; restore at test end.
    original = _ADAPTER_CLASSES["mcp-server-ext:mcp-client"]
    _ADAPTER_CLASSES["mcp-server-ext:mcp-client"] = _AttachFailingAdapter
    try:
        manifest = json.loads((MCP_FIXTURE / "workspace.json").read_text())
        with pytest.raises(WorkspaceBootError) as excinfo:
            Workspace.boot(manifest, MCP_FIXTURE / "extensions")
        failures = excinfo.value.failures
        assert any(f.category == "adapter-attach" for f in failures)
        attach_failure = next(f for f in failures if f.category == "adapter-attach")
        assert "primary-mcp" in attach_failure.path
        assert attach_failure.value == "mcp-tool-adapter"
        assert "attach_workspace failed" in attach_failure.reason
        assert "auth handshake" in attach_failure.reason
    finally:
        _ADAPTER_CLASSES["mcp-server-ext:mcp-client"] = original
