"""Tests for the Phase C C5 real-wire A2A peer adapter (D73 §B).

Per scope-cut C12 (autopilot constraint) + D68 §C closure item (a) — A2A
peer simulator harness in-process: a real stdlib ThreadingHTTPServer is
spawned on a background daemon thread; an httpx.Client inside the same
pytest process issues GET /.well-known/agent.json + POST /tasks against
``http://localhost:<bound_port>/``. NO external A2A peer reach.

Test coverage per D73 §B (closes Phase C C5 per D68 §A + closure item (a)):

  - Structural verification:
    - A2APeerAdapter registered under ``a2a-peer-ext:a2a-peer`` in the
      module ``_ADAPTER_CLASSES`` registry.
    - Subclasses Adapter with ``_outcome_prefix = "a2a-peer"``.
    - Lifts ``bind-host`` / ``port`` / ``peer-url`` /
      ``read-timeout-seconds`` from configuration per D57 §B.1.
  - Inbound publisher (D73 §B.1):
    - (a) GET /.well-known/agent.json → AgentCard JSON contains the
      publicly-exposed skill (closure item (a)).
    - (c) publicly-exposed=False skill is NOT in the agent-card (filter
      semantics per D60).
    - GET /unknown-path → HTTP 404.
  - Inbound task receiver (D73 §B.3):
    - (b) POST /tasks {skill_id, params} → specialist.handle_skill invoked;
      response carries the result + ok=True.
    - POST /tasks with unknown skill_id → HTTP 404 + error response.
    - POST /tasks with malformed JSON → HTTP 400.
    - POST /tasks with publicly-exposed=False skill_id → HTTP 404
      (not exposed; not invokable via A2A surface).
  - Outbound call() (D73 §B.2 — parallel to D72 §B.1):
    - (d) AdapterCallError(transport) on httpx.ConnectError.
    - AdapterCallError(auth) on HTTP 401 from peer.
    - AdapterCallError(timeout) on httpx.ReadTimeout.
    - Happy-path call() round-trip via in-process server returns parsed body.
  - Server-bind failure (D73 §B.1 — REUSES D48 §B.2 adapter-attach
    category):
    - (e) Attempting to attach with a port already in use surfaces as
      WorkspaceBootError(category='adapter-attach').
"""
from __future__ import annotations

import json
import socket
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    Adapter,
    A2APeerAdapter,
    AdapterCallError,
    _ADAPTER_CLASSES,
)
from fresh_plan.runtime.boot import WorkspaceBootError


A2A_PEER_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-a2a-peer-adapter"
)


# ---------------------------------------------------------------------------
# Adapter spec used for unit-level tests (no Workspace boot required)
# ---------------------------------------------------------------------------


A2A_PEER_ADAPTER_SPEC = {
    "id": "a2a-peer-adapter",
    "version": "0.1.0",
    "protocol-or-transport": "a2a-peer-ext:a2a-peer",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


def _make_outbound_factory_for_handler(
    handler, *, base_url: str = "http://peer.test/"
):
    """Wrap an httpx MockTransport handler in an async context-manager factory.

    Used for outbound-call tests: tests pass a handler that returns or
    raises to inject the target failure / response shape from a mock
    peer A2A endpoint.
    """

    @asynccontextmanager
    async def _factory():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(
            transport=transport, base_url=base_url
        ) as client:
            yield client

    return _factory


def _make_adapter_unbooted(
    *,
    session_factory=None,
    configuration=None,
) -> A2APeerAdapter:
    """Build an unbooted A2APeerAdapter (no attach_workspace called)."""
    adapter = A2APeerAdapter(
        spec=dict(A2A_PEER_ADAPTER_SPEC),
        configuration=configuration,
    )
    adapter._session_factory = session_factory
    return adapter


# ---------------------------------------------------------------------------
# Structural verification
# ---------------------------------------------------------------------------


def test_a2a_peer_adapter_registered_under_protocol_identifier():
    """D73 §B + D68 §B.3: A2APeerAdapter registered under
    `a2a-peer-ext:a2a-peer` in module `_ADAPTER_CLASSES`."""
    assert _ADAPTER_CLASSES["a2a-peer-ext:a2a-peer"] is A2APeerAdapter


def test_a2a_peer_adapter_subclasses_adapter_with_outcome_prefix():
    adapter = _make_adapter_unbooted()
    assert isinstance(adapter, Adapter)
    assert adapter._outcome_prefix == "a2a-peer"
    assert adapter.protocol_or_transport == "a2a-peer-ext:a2a-peer"


def test_configuration_lifts_all_slots_per_d57_b1():
    """D57 §B.1 opaque pass-through: bind-host, port, peer-url,
    read-timeout-seconds in configuration dict override defaults."""
    adapter = _make_adapter_unbooted(
        configuration={
            "bind-host": "127.0.0.1",
            "port": 12345,
            "peer-url": "https://peer.test/api/",
            "read-timeout-seconds": 0.5,
        }
    )
    assert adapter._bind_host == "127.0.0.1"
    assert adapter._bind_port == 12345
    assert adapter._peer_url == "https://peer.test/api/"
    assert adapter._read_timeout_seconds == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# In-process server fixture (full Workspace boot)
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_a2a_peer_workspace():
    manifest = json.loads((A2A_PEER_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, A2A_PEER_FIXTURE / "extensions")
    adapter = ws.adapter("primary-a2a-peer")
    try:
        yield ws, adapter
    finally:
        # Stop the server thread first so port is released cleanly.
        adapter.shutdown()
        ws.shutdown()


# ---------------------------------------------------------------------------
# (a) Inbound publisher — GET /.well-known/agent.json
# ---------------------------------------------------------------------------


def test_get_well_known_agent_card_serves_aggregated_skills(
    booted_a2a_peer_workspace,
):
    """Acceptance (a) + closure item (a): GET /.well-known/agent.json
    returns the aggregated AgentCard JSON for the workspace. Filtered
    per D60 — only publicly-exposed=True skills surface."""
    _ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/.well-known/agent.json"
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
    assert response.status_code == 200
    card = response.json()
    assert card["name"] == "a2a-peer-adapter-ws"
    assert card["version"] == "1.0.0"
    # Only the publicly-exposed=True "echo" skill should appear.
    skill_ids = [sk["id"] for sk in card["skills"]]
    assert "echo" in skill_ids


def test_publicly_exposed_false_skill_filtered_out_of_agent_card(
    booted_a2a_peer_workspace,
):
    """D60 + D73 §B.1: skills with publicly-exposed=False are NOT
    included in the served agent-card."""
    _ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/.well-known/agent.json"
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
    card = response.json()
    skill_ids = [sk["id"] for sk in card["skills"]]
    assert "internal-only" not in skill_ids


def test_get_unknown_path_returns_404(booted_a2a_peer_workspace):
    """Routes other than /.well-known/agent.json return HTTP 404 + an
    A2A-shaped error response body."""
    _ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/unknown-path"
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
    assert response.status_code == 404
    assert "error" in response.json()


# ---------------------------------------------------------------------------
# (b) Inbound task receiver — POST /tasks
# ---------------------------------------------------------------------------


def test_post_tasks_routes_to_specialist_handle_skill(
    booted_a2a_peer_workspace,
):
    """Acceptance (b) + closure item (a): POST /tasks with
    {skill_id, params} routes to specialist.handle_skill and returns
    the result wrapped as {ok: True, result: ...}."""
    ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/tasks"
    payload = {"skill_id": "echo", "params": {"msg": "hello"}}
    before = len(ws.event_chain.by_payload_subtype("action"))
    with httpx.Client(timeout=5.0) as client:
        response = client.post(url, json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    # GenericSpecialist.handle_skill emits one action event per call;
    # the server-side specialist invocation should leave the chain with
    # one additional action event.
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "echo"
    assert emitted["payload"]["parameters"] == {"msg": "hello"}


def test_post_tasks_unknown_skill_id_returns_404(booted_a2a_peer_workspace):
    """A2A task targeting an unknown skill_id (no specialist binding
    declares it) surfaces as HTTP 404 + A2A error response."""
    _ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/tasks"
    payload = {"skill_id": "no-such-skill", "params": {}}
    with httpx.Client(timeout=5.0) as client:
        response = client.post(url, json=payload)
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "skill-not-found"


def test_post_tasks_non_publicly_exposed_skill_returns_404(
    booted_a2a_peer_workspace,
):
    """publicly-exposed=False skills are filtered from BOTH the
    agent-card AND task-routing per D21 §"Per-skill exposure control"
    — internal-only skills are not invokable via the A2A surface."""
    _ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/tasks"
    payload = {"skill_id": "internal-only", "params": {}}
    with httpx.Client(timeout=5.0) as client:
        response = client.post(url, json=payload)
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "skill-not-found"


def test_post_tasks_malformed_json_returns_400(booted_a2a_peer_workspace):
    """A POST /tasks body that isn't parseable JSON surfaces as HTTP 400."""
    _ws, adapter = booted_a2a_peer_workspace
    url = f"http://localhost:{adapter.bound_port}/tasks"
    with httpx.Client(timeout=5.0) as client:
        response = client.post(
            url,
            content=b"not json {{",
            headers={"Content-Type": "application/json"},
        )
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "malformed-json"


# ---------------------------------------------------------------------------
# (d) Outbound call() — parallel to D72 §B.1 mapping
# ---------------------------------------------------------------------------


def test_outbound_call_adapter_call_error_transport_on_connect_error():
    """Acceptance (d): httpx.ConnectError from outbound call maps to
    category='transport' per D73 §B.2 (parallel to D72 §B.1)."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("DNS lookup failed")

    adapter = _make_adapter_unbooted(
        session_factory=_make_outbound_factory_for_handler(_handler),
        configuration={"peer-url": "http://peer.test/"},
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-tr"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("any-skill", {})
    assert excinfo.value.category == "transport"
    assert excinfo.value.adapter_id == "a2a-peer-adapter"


def test_outbound_call_adapter_call_error_auth_on_401():
    """HTTP 401 from peer maps to category='auth' per D73 §B.2 (NATIVE
    HTTP mapping per D72 §B.1 pattern)."""

    def _handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "unauthorized"})

    adapter = _make_adapter_unbooted(
        session_factory=_make_outbound_factory_for_handler(_handler),
        configuration={"peer-url": "http://peer.test/"},
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-auth"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("protected-skill", {})
    assert excinfo.value.category == "auth"
    assert excinfo.value.detail.get("status-code") == 401


def test_outbound_call_adapter_call_error_timeout_on_read_timeout():
    """httpx.ReadTimeout maps to category='timeout' per D73 §B.2."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("response timed out", request=request)

    adapter = _make_adapter_unbooted(
        session_factory=_make_outbound_factory_for_handler(_handler),
        configuration={
            "peer-url": "http://peer.test/",
            "read-timeout-seconds": 0.1,
        },
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-tmo"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("slow-skill", {})
    assert excinfo.value.category == "timeout"


def test_outbound_call_happy_path_round_trip_via_mock_peer():
    """Outbound call() against a mock peer (MockTransport handler
    returning 200 + JSON body) returns the parsed body + emits one
    action event in the local chain per D73 §B.2 pre-wire emit."""

    def _handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else {}
        return httpx.Response(
            200,
            json={"ok": True, "result": {"echo": body.get("params", {})}},
        )

    adapter = _make_adapter_unbooted(
        session_factory=_make_outbound_factory_for_handler(_handler),
        configuration={"peer-url": "http://peer.test/"},
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-happy"
    response = adapter.call("echo", {"msg": "hi"})
    assert response["ok"] is True
    assert response["status-code"] == 200
    assert response["outcome-reference"] == "test-outcome-happy"


# ---------------------------------------------------------------------------
# (e) Server-bind failure — REUSES D48 §B.2 adapter-attach category
# ---------------------------------------------------------------------------


def test_server_bind_failure_surfaces_as_adapter_attach_workspaceerror(
    tmp_path,
):
    """Acceptance (e): when the configured port is already in use,
    A2APeerAdapter.attach_workspace raises OSError which boot.py wraps
    as WorkspaceBootError(category='adapter-attach') per D48 §B.2 +
    boot.py:599 (REUSE — no new FAILURE_CATEGORIES entry needed)."""
    # Reserve a port by binding a real socket on it; the workspace boot
    # will try to bind the same port and fail.
    occupier = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    occupier.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    occupier.bind(("localhost", 0))
    occupied_port = occupier.getsockname()[1]
    occupier.listen(1)
    try:
        manifest = json.loads(
            (A2A_PEER_FIXTURE / "workspace.json").read_text()
        )
        # Patch the manifest to use the occupied port.
        for binding in manifest["composition"]["adapter-bindings"]:
            if binding["binding-id"] == "primary-a2a-peer":
                binding["configuration"]["port"] = occupied_port
        with pytest.raises(WorkspaceBootError) as excinfo:
            Workspace.boot(manifest, A2A_PEER_FIXTURE / "extensions")
        # D48 §B.2 + boot.py:599 category for adapter attach failures.
        assert any(
            f.category == "adapter-attach" for f in excinfo.value.failures
        ), [f.category for f in excinfo.value.failures]
    finally:
        occupier.close()
