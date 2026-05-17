"""Tests for the Phase C C7 real-wire RAG specialist (D75 §B.1).

Per D68 §A C7 + §C closure items (c) + (f). The c7 RealWireRAGSpecialist
replaces the B7 RAGSpecialist stub by invoking the c3 RealWireMCPClientAdapter
(D71) end-to-end through the bound `mcp-server-ext:mcp-real-wire-adapter`
provision. Activates the D50 §B.1 SkillExecutionError forward-bar; first
concrete D50 §D D-5 composition resolution (WRAP AdapterCallError as
SkillExecutionError(category='external-dependency-error') with __cause__
chain).

Test coverage maps directly to D75 §B.1 + D68 §C closure items:

  - Happy-path retrieve closure item (c): real adapter round-trip through
    in-process MCP server; action event emitted + emitting-specialist
    attribution (D64 §B.1) + real retrieved chunks threaded through
    handle_skill return value.
  - SkillExecutionError category coverage per closure item (f) D50 §B.1
    starter vocabulary: domain-error / external-dependency-error /
    skill-execution / unknown.
  - D50 §D D-5 composition resolution: AdapterCallError raised by adapter
    is WRAPped as SkillExecutionError(external-dependency-error) with
    __cause__ chain preserving the original AdapterCallError.
  - D64 §B.1 emit-attribution: emitted event carries
    emitting_specialist=<binding-id> via the closure-wrap inherited from
    Specialist.attach_workspace.

Per scope-cut C12: in-process MCP server harness via
`mcp.shared.memory.create_connected_server_and_client_session`; no
external MCP wire reach.
"""
from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    AdapterCallError,
    RealWireMCPClientAdapter,
)
from fresh_plan.runtime.specialist import (
    RealWireRAGSpecialist,
    SkillExecutionError,
    Specialist,
    load_specialist_from_provision,
)


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
RAG_REALWIRE_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-rag-realwire-via-mcp"
)


# ---------------------------------------------------------------------------
# In-process MCP server harness — registers a `retrieve` tool that returns
# canned TextContent blocks the specialist parses into chunks.
# ---------------------------------------------------------------------------


def _build_retrieve_server():
    """Construct a minimal MCP Server with a `retrieve` tool.

    The retrieve tool echoes the query into k TextContent blocks; each
    block's text is what RealWireRAGSpecialist parses into a chunk's
    `content`. The server also exposes a `retrieve-malformed` tool that
    returns content blocks missing the `text` field, used to exercise
    the skill-execution category mapping.
    """
    from mcp.server.lowlevel import Server
    import mcp.types as t

    server = Server("fresh-plan-test-retrieve-server")

    @server.list_tools()
    async def _list():
        return [
            t.Tool(
                name="retrieve",
                description="canned retrieval; returns k TextContent blocks",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "k": {"type": "integer"},
                    },
                },
            ),
        ]

    @server.call_tool()
    async def _call(name: str, arguments: dict | None):
        args = arguments or {}
        if name == "retrieve":
            query = args.get("query", "")
            k = int(args.get("k", 3))
            return [
                t.TextContent(
                    type="text", text=f"hit-{i + 1} for {query!r}"
                )
                for i in range(k)
            ]
        return [t.TextContent(type="text", text=f"unknown tool {name}")]

    return server


def _real_session_factory():
    from mcp.shared.memory import create_connected_server_and_client_session

    @asynccontextmanager
    async def _factory():
        server = _build_retrieve_server()
        async with create_connected_server_and_client_session(
            server, raise_exceptions=False
        ) as session:
            yield session

    return _factory


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_rag_realwire_workspace():
    manifest = json.loads(
        (RAG_REALWIRE_FIXTURE / "workspace.json").read_text()
    )
    ws = Workspace.boot(manifest, RAG_REALWIRE_FIXTURE / "extensions")
    # Wire the adapter's session factory to drive the in-process MCP
    # server per scope-cut C12.
    adapter = ws.adapter("primary-mcp-realwire")
    assert isinstance(adapter, RealWireMCPClientAdapter)
    adapter._session_factory = _real_session_factory()
    try:
        yield ws
    finally:
        ws.shutdown()


# ---------------------------------------------------------------------------
# Structural verification
# ---------------------------------------------------------------------------


def test_realwire_rag_specialist_loads_from_0_2_0_provision():
    """D75 §C: rag-via-mcp-ext/0.2.0 specialist provision resolves to
    RealWireRAGSpecialist (the c7 NEW class), preserving B7's 0.1.0
    rag-specialist provision → RAGSpecialist mapping unchanged."""
    specialist = load_specialist_from_provision(
        "rag-via-mcp-ext:rag-realwire-specialist", IMPL_EXTENSIONS_DIR
    )
    assert isinstance(specialist, RealWireRAGSpecialist)
    assert isinstance(specialist, Specialist)
    assert specialist.id == "rag-realwire-specialist"
    assert specialist.version == "0.2.0"
    assert specialist.required_adapter_bindings == [
        "mcp-server-ext:mcp-real-wire-adapter"
    ]


# ---------------------------------------------------------------------------
# Closure item (c): real-wire happy-path end-to-end + D64 §B.1 attribution
# ---------------------------------------------------------------------------


def test_retrieve_happy_path_returns_real_chunks_via_mcp_round_trip(
    booted_rag_realwire_workspace,
):
    """Closure item (c) + D75 §B.1: handle_skill('retrieve', ...) invokes
    the c3 RealWireMCPClientAdapter end-to-end through the in-process
    MCP server; the retrieved TextContent blocks thread through the
    specialist's parser into chunks; the return value carries the real
    (not stubbed) result payload + adapter outcome-reference.
    """
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    response = specialist.handle_skill(
        "retrieve", {"query": "what is durable?", "k": 3}
    )
    assert response["ok"] is True
    assert response["skill"] == "retrieve"
    assert response["query"] == "what is durable?"
    assert response["k"] == 3
    assert "stub" not in response  # confirms NOT the B7 stub return shape
    assert isinstance(response["chunks"], list)
    assert len(response["chunks"]) == 3
    # Real content threaded through from the in-process MCP server's
    # TextContent blocks — NOT the B7 stub's f-string template.
    for i, chunk in enumerate(response["chunks"]):
        assert chunk["id"] == f"chunk-{i + 1}"
        assert chunk["content"] == f"hit-{i + 1} for 'what is durable?'"
    # The adapter's outcome-reference (`mcp-realwire-<N>`) threads
    # through; confirms the c3 adapter was the wire endpoint.
    assert response["adapter-outcome-ref"].startswith("mcp-realwire-")


def test_retrieve_emits_action_event_with_emitting_specialist_attribution(
    booted_rag_realwire_workspace,
):
    """Closure item (c) + D64 §B.1: the specialist's action emission at
    handle_skill entry carries `emitting-specialist=<binding-id>` via
    the closure-wrap inherited from Specialist.attach_workspace
    (specialist.py:226-237). Verifies emit-attribution INHERITANCE — no
    override needed in RealWireRAGSpecialist.
    """
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    before = len(ws.event_chain.by_payload_subtype("action"))
    specialist.handle_skill("retrieve", {"query": "attribution", "k": 2})
    actions = ws.event_chain.by_payload_subtype("action")
    # Two emissions: (1) the specialist's pre-wire action emit, (2) the
    # c3 adapter's pre-wire action emit per D71 §B.1.
    assert len(actions) == before + 2
    specialist_action = actions[-2]
    adapter_action = actions[-1]
    # D64 §B.1: emitting-specialist field present on the specialist's
    # own emission + carries the binding-id (NOT the spec id).
    assert specialist_action["emitting-specialist"] == (
        "primary-rag-realwire-specialist"
    )
    assert specialist_action["payload"]["action-name"] == "retrieve"
    assert specialist_action["payload"]["parameters"] == {
        "query": "attribution",
        "k": 2,
    }
    # The adapter's action event is attributed to the same specialist
    # because the adapter inherits the workspace's _emit_event which
    # was wrapped by the specialist's attach_workspace closure when the
    # specialist invoked adapter.call. Adapter action carries the
    # outcome-reference per D71 §B.1.
    assert "outcome-reference" in adapter_action["payload"]


# ---------------------------------------------------------------------------
# Closure item (f) — SkillExecutionError per starter category vocabulary
# ---------------------------------------------------------------------------


def test_domain_error_on_empty_query(booted_rag_realwire_workspace):
    """Closure item (f) domain-error: params validation rejects empty
    query → SkillExecutionError(category='domain-error') per D75 §B.1.
    """
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    with pytest.raises(SkillExecutionError) as excinfo:
        specialist.handle_skill("retrieve", {"query": "", "k": 3})
    assert excinfo.value.category == "domain-error"
    assert excinfo.value.specialist_id == "rag-realwire-specialist"
    assert excinfo.value.skill_id == "retrieve"
    assert "non-empty string" in excinfo.value.detail["reason"]


def test_domain_error_on_non_string_query(booted_rag_realwire_workspace):
    """Closure item (f) domain-error: non-string query → SkillExecutionError(
    category='domain-error') per D75 §B.1."""
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    with pytest.raises(SkillExecutionError) as excinfo:
        specialist.handle_skill("retrieve", {"query": 42, "k": 3})
    assert excinfo.value.category == "domain-error"


def test_domain_error_on_invalid_k(booted_rag_realwire_workspace):
    """Closure item (f) domain-error: k < 1 → SkillExecutionError(
    category='domain-error') per D75 §B.1."""
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    with pytest.raises(SkillExecutionError) as excinfo:
        specialist.handle_skill("retrieve", {"query": "x", "k": 0})
    assert excinfo.value.category == "domain-error"
    assert "k must be >= 1" in excinfo.value.detail["reason"]


def test_external_dependency_error_wraps_adapter_call_error_with_cause_chain(
    booted_rag_realwire_workspace,
):
    """Closure item (f) external-dependency-error + D75 §B.1 D-5
    RESOLUTION: AdapterCallError raised by the bound adapter is WRAPped
    as SkillExecutionError(category='external-dependency-error') with
    __cause__ chain preserving the original AdapterCallError for caller
    introspection.

    First concrete D50 §D D-5 composition precedent: WRAP (not propagate
    raw). Rationale per D75 §B.1: uniform skill-failure surface +
    __cause__ chain preserves wire-layer diagnostic detail.
    """
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    adapter = ws.adapter("primary-mcp-realwire")

    # Monkey-patch adapter.call to raise AdapterCallError directly,
    # simulating any of the c3 starter category vocabulary failure
    # modes (transport / auth / timeout / protocol-error / upstream-error
    # / unknown — they all surface to the specialist the same way).
    original_call = adapter.call
    injected_error = AdapterCallError(
        adapter_id="mcp-real-wire-adapter",
        call_target="retrieve",
        category="transport",
        detail={"reason": "simulated broken stream"},
    )

    def _fail(*args, **kwargs):
        raise injected_error

    adapter.call = _fail
    try:
        with pytest.raises(SkillExecutionError) as excinfo:
            specialist.handle_skill("retrieve", {"query": "fail", "k": 2})
    finally:
        adapter.call = original_call

    # WRAP per D-5 RESOLUTION + D75 §B.1.
    assert excinfo.value.category == "external-dependency-error"
    assert excinfo.value.specialist_id == "rag-realwire-specialist"
    assert excinfo.value.skill_id == "retrieve"
    # Detail carries the original adapter category + adapter_id +
    # call_target for diagnosis without forcing __cause__ unwrap.
    assert excinfo.value.detail["adapter-category"] == "transport"
    assert excinfo.value.detail["adapter-id"] == "mcp-real-wire-adapter"
    assert excinfo.value.detail["call-target"] == "retrieve"
    # __cause__ chain preserves the original AdapterCallError per D75
    # §B.1 WRAP-with-from-clause.
    assert excinfo.value.__cause__ is injected_error
    assert isinstance(excinfo.value.__cause__, AdapterCallError)


def test_skill_execution_error_on_malformed_adapter_result(
    booted_rag_realwire_workspace,
):
    """Closure item (f) skill-execution: when the adapter returns a result
    with a malformed content-block shape (missing 'text'), result
    parsing raises SkillExecutionError(category='skill-execution') per
    D75 §B.1.
    """
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    adapter = ws.adapter("primary-mcp-realwire")

    # Monkey-patch adapter.call to return a malformed result — a content
    # block with NO 'text' field. Specialist's parser must classify
    # this as skill-execution (not unknown, not external-dependency).
    original_call = adapter.call

    def _malformed(*args, **kwargs):
        return {
            "outcome-reference": "mcp-realwire-test",
            "ok": True,
            "isError": False,
            "content": [
                {"type": "image", "data": "not-a-text-block"},
            ],
        }

    adapter.call = _malformed
    try:
        with pytest.raises(SkillExecutionError) as excinfo:
            specialist.handle_skill(
                "retrieve", {"query": "parse-fail", "k": 1}
            )
    finally:
        adapter.call = original_call

    assert excinfo.value.category == "skill-execution"
    assert "missing 'text'" in excinfo.value.detail["reason"]


def test_unknown_category_on_unexpected_exception_from_adapter(
    booted_rag_realwire_workspace,
):
    """Closure item (f) unknown: an unexpected exception class (NOT
    AdapterCallError) raised by adapter.call surfaces as
    SkillExecutionError(category='unknown') with __cause__ chained per
    D75 §B.1 catch-all branch.
    """
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    adapter = ws.adapter("primary-mcp-realwire")

    class _WeirdException(Exception):
        """Not in any pre-classified category."""

    original_call = adapter.call

    def _weird(*args, **kwargs):
        raise _WeirdException("something nobody expected")

    adapter.call = _weird
    try:
        with pytest.raises(SkillExecutionError) as excinfo:
            specialist.handle_skill("retrieve", {"query": "weird", "k": 1})
    finally:
        adapter.call = original_call

    assert excinfo.value.category == "unknown"
    assert excinfo.value.detail["exception-type"] == "_WeirdException"
    assert "something nobody expected" in excinfo.value.detail["exception"]
    assert isinstance(excinfo.value.__cause__, _WeirdException)


def test_unknown_skill_id_raises_not_implemented(
    booted_rag_realwire_workspace,
):
    """Pre-condition guard per D50 §D D-1 — dispatch-miss is a Python
    idiom (NotImplementedError), NOT SkillExecutionError. Mirrors the
    B7 RAGSpecialist convention preserved at c7."""
    ws = booted_rag_realwire_workspace
    specialist = ws.specialist("primary-rag-realwire-specialist")
    with pytest.raises(NotImplementedError) as excinfo:
        specialist.handle_skill("not-a-real-skill", {})
    assert "rag-realwire-specialist" in str(excinfo.value)
    assert "not-a-real-skill" in str(excinfo.value)
