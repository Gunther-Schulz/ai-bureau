"""Tests for the B7 minimal RAG-via-MCP impl (per D19 + D38 + D26).

Demonstrates: one protocol (mcp-server-ext:mcp-client) supports multiple
semantically-distinct provisions — B4's mcp-tool-adapter and B7's
rag-retriever-adapter both dispatch to MCPToolAdapter via protocol-or-transport,
but the provision specs differentiate the semantic role.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    MCPToolAdapter,
    load_adapter_from_provision,
)
from fresh_plan.runtime.specialist import (
    RAGSpecialist,
    Specialist,
    load_specialist_from_provision,
)


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
RAG_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-rag-via-mcp"


RAG_SPECIALIST_SPEC = {
    "id": "rag-specialist",
    "version": "0.1.0",
    "roles": ["retriever"],
    "skills": [
        {
            "id": "retrieve",
            "description": "Retrieve relevant context chunks from the bound MCP retriever for a query.",
        }
    ],
    "supported-work-unit-kinds": ["rag-via-mcp-ext:retrieval-task"],
    "required-adapter-bindings": ["rag-via-mcp-ext:rag-retriever-adapter"],
    "required-substrate-capabilities": ["skills", "event-streaming"],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-subscriptions": [],
}


@pytest.fixture
def rag_specialist() -> RAGSpecialist:
    return RAGSpecialist(spec=dict(RAG_SPECIALIST_SPEC))


@pytest.fixture
def booted_workspace():
    manifest = json.loads((RAG_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, RAG_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_rag_specialist_accessors(rag_specialist):
    assert rag_specialist.id == "rag-specialist"
    assert rag_specialist.version == "0.1.0"
    assert rag_specialist.roles == ["retriever"]
    assert rag_specialist.skills[0]["id"] == "retrieve"
    assert rag_specialist.supported_work_unit_kinds == [
        "rag-via-mcp-ext:retrieval-task"
    ]
    assert rag_specialist.required_adapter_bindings == [
        "rag-via-mcp-ext:rag-retriever-adapter"
    ]
    assert rag_specialist.required_substrate_capabilities == [
        "skills",
        "event-streaming",
    ]
    assert rag_specialist.declared_event_emissions == [{"payload-subtype": "action"}]
    assert rag_specialist.declared_event_subscriptions == []


def test_handle_skill_retrieve_returns_retrieval_shaped_response(booted_workspace):
    ws = booted_workspace
    specialist = ws.specialist("primary-rag-specialist")
    response = specialist.handle_skill("retrieve", {"query": "hello world"})
    assert response["ok"] is True
    assert response["skill"] == "retrieve"
    assert response["query"] == "hello world"
    assert response["k"] == 3
    assert response["stub"] is True
    assert isinstance(response["chunks"], list)
    assert len(response["chunks"]) == 3
    for i, chunk in enumerate(response["chunks"]):
        assert chunk["id"] == f"chunk-{i + 1}"
        assert "stub chunk" in chunk["content"]
    assert response["adapter-outcome-ref"].startswith("mcp-stub-")


def test_handle_skill_unknown_skill_raises(booted_workspace):
    ws = booted_workspace
    specialist = ws.specialist("primary-rag-specialist")
    with pytest.raises(NotImplementedError) as excinfo:
        specialist.handle_skill("not-a-real-skill", {})
    assert "rag-specialist" in str(excinfo.value)
    assert "not-a-real-skill" in str(excinfo.value)


def test_retrieve_registered_in_substrate_skills(booted_workspace):
    ws = booted_workspace
    assert ws.substrate.skills.has("retrieve")
    response = ws.substrate.skills.invoke("retrieve", {"query": "test"})
    assert response["ok"] is True
    assert response["skill"] == "retrieve"
    assert response["query"] == "test"
    assert len(response["chunks"]) == 3


def test_skill_invocation_emits_two_action_events_chained(booted_workspace):
    """Per the architectural pattern B7 demonstrates: invoking retrieve produces
    two action events — one from the specialist (its own emission), then one
    from the adapter (via adapter.call). The specialist's response carries
    adapter-outcome-ref equal to the adapter's emitted outcome-reference.
    """
    ws = booted_workspace
    before = len(ws.event_chain.by_payload_subtype("action"))
    response = ws.substrate.skills.invoke("retrieve", {"query": "ordering", "k": 2})
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 2

    specialist_action = actions[-2]
    adapter_action = actions[-1]

    assert specialist_action["payload"]["action-name"] == "retrieve"
    assert specialist_action["payload"]["parameters"] == {"query": "ordering", "k": 2}
    # Specialist's own action emission carries no outcome-reference (only the
    # adapter's request/response action does, per Adapter._emit_action).
    assert "outcome-reference" not in specialist_action["payload"]

    assert adapter_action["payload"]["action-name"] == "retrieve"
    assert adapter_action["payload"]["parameters"] == {"query": "ordering", "k": 2}
    assert adapter_action["payload"]["outcome-reference"] == response["adapter-outcome-ref"]

    # Chain integrity: adapter_action's prev-event references specialist_action.
    assert adapter_action["prev-event"] == specialist_action["id"]


def test_protocol_vs_provision_dispatch(booted_workspace):
    """B7's architectural point: both mcp-server-ext:mcp-tool-adapter and
    rag-via-mcp-ext:rag-retriever-adapter share protocol-or-transport
    `mcp-server-ext:mcp-client` and dispatch to the same MCPToolAdapter
    runtime class, but their provision ids differ. One protocol, multiple
    semantically-distinct provisions.
    """
    mcp_tool = load_adapter_from_provision(
        "mcp-server-ext:mcp-tool-adapter", IMPL_EXTENSIONS_DIR
    )
    rag_retriever = load_adapter_from_provision(
        "rag-via-mcp-ext:rag-retriever-adapter", IMPL_EXTENSIONS_DIR
    )
    # Same runtime class.
    assert isinstance(mcp_tool, MCPToolAdapter)
    assert isinstance(rag_retriever, MCPToolAdapter)
    assert type(mcp_tool) is type(rag_retriever)
    # Same protocol-or-transport identifier.
    assert mcp_tool.protocol_or_transport == "mcp-server-ext:mcp-client"
    assert rag_retriever.protocol_or_transport == "mcp-server-ext:mcp-client"
    # Distinct provision ids — the semantic differentiator.
    assert mcp_tool.id == "mcp-tool-adapter"
    assert rag_retriever.id == "rag-retriever-adapter"
    assert mcp_tool.id != rag_retriever.id


def test_load_specialist_from_provision_finds_rag_specialist():
    specialist = load_specialist_from_provision(
        "rag-via-mcp-ext:rag-specialist", IMPL_EXTENSIONS_DIR
    )
    assert isinstance(specialist, RAGSpecialist)
    assert isinstance(specialist, Specialist)
    assert specialist.id == "rag-specialist"
    assert specialist.version == "0.1.0"
