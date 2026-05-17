"""Tests for the Phase C C4 real-wire direct-API HTTP adapter (D72 §B.1).

Per scope-cut C12 (autopilot constraint): tests use ``httpx.MockTransport``
with a handler function (Request → Response OR raise) for in-process fault
injection. NO real network reach.

Pure pattern application of D71 §B.1 (RealWireMCPClientAdapter) test
structure: SAME shape, httpx-specific exception branches differ. Test
coverage per D68 §C closure item (e) + D72 §B.1 AdapterCallError starter
category vocabulary:

  - (a) Happy-path round-trip: MockTransport returns 200 OK + JSON body;
    adapter.call returns parsed body; one ``action`` event emitted to
    the workspace chain pre-wire.
  - (b) AdapterCallError(transport): httpx.ConnectError raised by handler.
  - (c) AdapterCallError(auth): MockTransport returns 401 / 403 / 407;
    NATIVE HTTP auth-category mapping (first Phase C adapter to populate
    auth natively — unlike D71 §D D-2 deferral for MCP).
  - (d) AdapterCallError(timeout): httpx.ReadTimeout raised by handler.
  - (e) AdapterCallError(protocol-error): httpx.RemoteProtocolError raised;
    AND malformed JSON body via response.json() ValueError path.
  - (f) AdapterCallError(upstream-error): MockTransport returns 500 / 503.
  - (g) AdapterCallError(unknown): catch-all path via an unmapped
    exception class.

Plus structural verification:
  - Adapter registers via ``_ADAPTER_CLASSES`` under the
    ``direct-api-ext:direct-api-realwire`` protocol identifier;
    0.1.0 stub adapter remains under ``direct-api-ext:direct-api``.
  - The pre-wire ``action`` event is emitted regardless of call outcome
    (per D48 §D D-5 resolution at D71 §B.1; D72 §B.1 carries this).
"""
from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    Adapter,
    AdapterCallError,
    DirectAPIAdapter,
    RealWireDirectAPIAdapter,
    _ADAPTER_CLASSES,
)


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
DIRECT_API_REALWIRE_FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "workspace-direct-api-realwire-adapter"
)


# ---------------------------------------------------------------------------
# Adapter spec used for unit-level tests (no Workspace boot required)
# ---------------------------------------------------------------------------


REALWIRE_ADAPTER_SPEC = {
    "id": "direct-api-realwire-adapter",
    "version": "0.2.0",
    "protocol-or-transport": "direct-api-ext:direct-api-realwire",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


# ---------------------------------------------------------------------------
# In-process httpx test harness helpers (MockTransport-based)
# ---------------------------------------------------------------------------


def _make_factory_for_handler(handler, *, base_url: str = "http://test/"):
    """Wrap an httpx MockTransport handler in an async context-manager factory.

    Tests pass `handler(request: httpx.Request) -> httpx.Response` (or raising
    handlers) to inject the target failure / response shape. The factory
    builds an httpx.AsyncClient bound to the MockTransport so the adapter's
    `_drive()` exercises real httpx code paths up to the boundary.
    """

    @asynccontextmanager
    async def _factory():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(
            transport=transport, base_url=base_url
        ) as client:
            yield client

    return _factory


def _make_adapter(
    session_factory=None,
    configuration=None,
) -> RealWireDirectAPIAdapter:
    adapter = RealWireDirectAPIAdapter(
        spec=dict(REALWIRE_ADAPTER_SPEC),
        configuration=configuration,
    )
    adapter._session_factory = session_factory
    return adapter


# ---------------------------------------------------------------------------
# Structural verification
# ---------------------------------------------------------------------------


def test_realwire_direct_api_adapter_registered_under_new_protocol_identifier():
    """D72 §B.1 + D68 §B.3: 0.2.0 registers a NEW protocol identifier
    `direct-api-ext:direct-api-realwire`; 0.1.0 stub stands under
    `direct-api-ext:direct-api` per D41 two-substrate parity precedent."""
    assert _ADAPTER_CLASSES["direct-api-ext:direct-api-realwire"] is (
        RealWireDirectAPIAdapter
    )
    # 0.1.0 stub path preserved.
    assert _ADAPTER_CLASSES["direct-api-ext:direct-api"] is DirectAPIAdapter


def test_realwire_direct_api_adapter_subclasses_adapter_with_realwire_prefix():
    adapter = _make_adapter()
    assert isinstance(adapter, Adapter)
    assert adapter._outcome_prefix == "direct-realwire"
    assert adapter.protocol_or_transport == (
        "direct-api-ext:direct-api-realwire"
    )


def test_configuration_lifts_base_url_headers_and_read_timeout_seconds():
    """D57 §B.1 opaque pass-through: `base-url`, `headers`, and
    `read-timeout-seconds` in configuration dict override defaults."""
    adapter = _make_adapter(
        configuration={
            "base-url": "https://example.test/api/",
            "headers": {"Authorization": "Bearer tok"},
            "read-timeout-seconds": 0.5,
        }
    )
    assert adapter._base_url == "https://example.test/api/"
    assert adapter._headers == {"Authorization": "Bearer tok"}
    assert adapter._read_timeout_seconds == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# (a) Happy-path round-trip via httpx.MockTransport
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_direct_api_realwire_workspace():
    manifest = json.loads(
        (DIRECT_API_REALWIRE_FIXTURE / "workspace.json").read_text()
    )
    ws = Workspace.boot(
        manifest, DIRECT_API_REALWIRE_FIXTURE / "extensions"
    )
    try:
        yield ws
    finally:
        ws.shutdown()


def test_call_happy_path_round_trip_through_mock_transport(
    booted_direct_api_realwire_workspace,
):
    """Acceptance (a): happy-path call returns parsed JSON body; one
    action event emitted to the workspace chain (per D48 §D D-5
    pre-wire-emit resolution at D71 §B.1 carried by D72 §B.1)."""
    ws = booted_direct_api_realwire_workspace
    adapter = ws.adapter("primary-direct-api-realwire")
    assert isinstance(adapter, RealWireDirectAPIAdapter)

    def _handler(request: httpx.Request) -> httpx.Response:
        # Echo back the request URL path + JSON body.
        body = json.loads(request.content) if request.content else {}
        return httpx.Response(
            200,
            json={"echoed-path": request.url.path, "params": body},
        )

    adapter._session_factory = _make_factory_for_handler(_handler)

    before = len(ws.event_chain.by_payload_subtype("action"))
    response = adapter.call("echo", {"msg": "hi"})
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "echo"
    assert emitted["payload"]["parameters"] == {"msg": "hi"}

    assert response["ok"] is True
    assert response["status-code"] == 200
    assert response["outcome-reference"].startswith("direct-realwire-")
    assert response["body"]["params"] == {"msg": "hi"}
    # The path 'echo' became part of the URL we sent.
    assert response["body"]["echoed-path"].endswith("echo")


# ---------------------------------------------------------------------------
# (b) AdapterCallError(transport)
# ---------------------------------------------------------------------------


def test_adapter_call_error_transport_on_connect_error():
    """Acceptance (b): httpx.ConnectError raised by transport maps to
    category='transport' per D72 §B.1 starter vocabulary."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("DNS lookup failed")

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-tr"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("any-endpoint", {})
    assert excinfo.value.category == "transport"
    assert excinfo.value.adapter_id == "direct-api-realwire-adapter"
    assert excinfo.value.call_target == "any-endpoint"
    assert "DNS lookup failed" in excinfo.value.detail.get("reason", "")


def test_adapter_call_error_transport_on_oserror_in_handler():
    """OSError raised by the handler maps to category='transport' via
    the OSError branch (covers MockTransport handlers that raise lower-
    level errors not wrapped by httpx)."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise OSError("socket level: connection reset")

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-os"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("any-endpoint", {})
    assert excinfo.value.category == "transport"
    assert "connection reset" in excinfo.value.detail.get("reason", "")


# ---------------------------------------------------------------------------
# (c) AdapterCallError(auth) — NATIVE HTTP mapping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status_code", [401, 403, 407])
def test_adapter_call_error_auth_on_native_http_status_codes(status_code):
    """Acceptance (c): HTTP 401 / 403 / 407 responses map to category='auth'
    NATIVELY per D72 §B.1 — unlike D71 §D D-2 deferral for MCP (where the
    auth subcase folds into upstream-error pending per-server extension),
    HTTP cleanly discriminates auth-required from upstream errors via
    response.status_code."""

    def _handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json={"error": "unauthorized"})

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: f"test-outcome-auth-{status_code}"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("protected-endpoint", {})
    assert excinfo.value.category == "auth"
    assert excinfo.value.detail.get("status-code") == status_code


# ---------------------------------------------------------------------------
# (d) AdapterCallError(timeout)
# ---------------------------------------------------------------------------


def test_adapter_call_error_timeout_on_read_timeout():
    """Acceptance (d): httpx.ReadTimeout (a TimeoutException subclass) maps
    to category='timeout' per D72 §B.1."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("response timed out", request=request)

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler),
        configuration={"read-timeout-seconds": 0.1},
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-timeout"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("slow-endpoint", {})
    assert excinfo.value.category == "timeout"
    assert excinfo.value.detail.get("read-timeout-seconds") == pytest.approx(
        0.1
    )


# ---------------------------------------------------------------------------
# (e) AdapterCallError(protocol-error)
# ---------------------------------------------------------------------------


def test_adapter_call_error_protocol_error_on_remote_protocol_error():
    """Acceptance (e1): httpx.RemoteProtocolError raised by transport maps
    to category='protocol-error' per D72 §B.1."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise httpx.RemoteProtocolError(
            "server disconnected without sending a response",
            request=request,
        )

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-proto"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("anything", {})
    assert excinfo.value.category == "protocol-error"
    assert "RemoteProtocolError" in excinfo.value.detail.get("reason", "")


def test_adapter_call_error_protocol_error_on_malformed_json_body():
    """Acceptance (e2): a 200 response with content-type=application/json
    but non-JSON body raises json.JSONDecodeError (ValueError) on
    response.json() — maps to category='protocol-error' per D72 §B.1
    (server returned 2xx but body didn't conform to declared content-type)."""

    def _handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"this is not json",
            headers={"content-type": "application/json"},
        )

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-proto-json"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("malformed-json-endpoint", {})
    assert excinfo.value.category == "protocol-error"
    assert "JSONDecodeError" in excinfo.value.detail.get(
        "reason", ""
    ) or "JSON" in excinfo.value.detail.get("reason", "")


# ---------------------------------------------------------------------------
# (f) AdapterCallError(upstream-error) — 5xx + non-auth 4xx
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status_code", [500, 502, 503, 400, 404, 422, 429])
def test_adapter_call_error_upstream_error_on_5xx_and_non_auth_4xx(
    status_code,
):
    """Acceptance (f): 5xx + non-auth 4xx (400/404/422/429) map to
    category='upstream-error' per D72 §B.1 (auth 401/403/407 discriminated
    separately per acceptance (c))."""

    def _handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json={"error": "server failure"})

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: f"test-outcome-up-{status_code}"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("any-endpoint", {})
    assert excinfo.value.category == "upstream-error"
    assert excinfo.value.detail.get("status-code") == status_code


# ---------------------------------------------------------------------------
# (g) AdapterCallError(unknown) — catch-all
# ---------------------------------------------------------------------------


def test_adapter_call_error_unknown_on_unmapped_exception():
    """Acceptance (g): an exception class that doesn't match any of the
    specific-category branches (transport / auth / timeout / protocol-
    error / upstream-error) maps to category='unknown' per D72 §B.1
    catch-all."""

    class _WeirdException(Exception):
        """Custom exception not in any specific-category mapping."""

    def _handler(request: httpx.Request) -> httpx.Response:
        raise _WeirdException("something unexpected happened")

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
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

    def _handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("underlying cause")

    adapter = _make_adapter(
        session_factory=_make_factory_for_handler(_handler)
    )
    adapter._emit_action = lambda *args, **kwargs: "test-outcome-chain"
    with pytest.raises(AdapterCallError) as excinfo:
        adapter.call("anything", {})
    assert isinstance(excinfo.value.__cause__, httpx.ConnectError)
    assert "underlying cause" in str(excinfo.value.__cause__)
