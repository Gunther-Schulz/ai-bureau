"""End-to-end substrate scenario test (B2 brief §"Tests" § test_substrate_e2e.py).

Boot a workspace; register a sub-agent (composition-change); emit claim +
action + state-change events; create + transition a work-unit; shutdown.
Verify the event chain has the expected sequence + types.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import EventRejected, Workspace


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"
GENERIC_SHAPE_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-generic-shape"
)
MCP_ADAPTER_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-mcp-adapter"
GENERIC_SPECIALIST_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-generic-specialist"
)
RAG_VIA_MCP_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-rag-via-mcp"
)
MS_AGENT_FRAMEWORK_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-ms-agent-framework"
)


@pytest.fixture
def workspace():
    manifest = json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, SUBSTRATE_FIXTURE / "extensions")
    yield ws
    ws.shutdown()


def test_scripted_scenario_produces_expected_chain(workspace):
    ws = workspace
    primary = ws.actors["agent-primary"]

    # Register a sub-agent (composition-change).
    sub = ws.register_agent_actor(id="subagent-1", substrate_binding="primary")
    assert sub.id == "subagent-1"
    assert "subagent-1" in ws.substrate.state.actors

    # Sub-agent emits action.
    sub.emit_action("plan", parameters={"target": "subtask"})

    # Primary emits claim + state-change.
    primary.emit_claim("section drafted", confidence="medium")
    primary.emit_state_change("scope", before=None, after={"focus": "section-3"})
    assert ws.current_scope == {"focus": "section-3"}

    # Create + transition a work-unit.
    wu = ws.create_work_unit(
        id="wu-test-1",
        kind="min-shape-ext:dummy-kind",
        payload={"note": "ok"},
    )
    wu.transition("in-progress")
    wu.transition("completed")
    assert wu.status == "completed"


def test_e2e_event_chain_subtypes_in_order(workspace):
    ws = workspace
    primary = ws.actors["agent-primary"]
    sub = ws.register_agent_actor(id="subagent-1", substrate_binding="primary")
    sub.emit_action("plan", parameters={})
    primary.emit_claim("assertion", confidence="high")
    primary.emit_state_change("scope", after={"domain": "x"})
    wu = ws.create_work_unit(id="wu-1", kind="min-shape-ext:k", payload={})
    wu.transition("in-progress")
    wu.transition("completed")
    ws.shutdown()

    subtypes = [e["payload-subtype"] for e in ws.events()]
    # Per Bref closure of D39: boot emits N composition-change:add events
    # (manifest-actor seeding) BEFORE the lifecycle-transition:boot, so
    # subtypes[0] is composition-change, not lifecycle-transition. The
    # boot + shutdown transitions are both present; shutdown is last.
    assert subtypes[-1] == "lifecycle-transition"  # shutdown
    transitions = [
        e for e in ws.events() if e["payload-subtype"] == "lifecycle-transition"
    ]
    assert [t["payload"]["transition-type"] for t in transitions] == [
        "boot",
        "shutdown",
    ]
    assert "composition-change" in subtypes
    assert "claim" in subtypes
    assert "action" in subtypes
    assert "state-change" in subtypes


def test_e2e_work_unit_id_propagates_to_events(workspace):
    """Per D23 + D20 — events referencing a work-unit carry work-unit-id."""
    ws = workspace
    wu = ws.create_work_unit(id="wu-track", kind="min-shape-ext:k", payload={})
    wu.transition("in-progress")
    related = ws.event_chain.by_work_unit("wu-track")
    assert len(related) >= 2  # creation event + transition event
    for e in related:
        assert e["work-unit-id"] == "wu-track"


def test_e2e_sub_agent_is_valid_event_target_after_composition_change(workspace):
    """Per D34 §A.5: sub-agents added via composition-change are valid event
    targets AFTER the composition-change is appended."""
    ws = workspace
    sub = ws.register_agent_actor(id="subagent-1", substrate_binding="primary")
    # If the new actor weren't a valid event target, the next emit would
    # raise EventRejected.
    sub.emit_action("noop", parameters={})
    by_actor = ws.event_chain.by_actor("subagent-1")
    assert any(e["payload-subtype"] == "action" for e in by_actor)


def test_e2e_composition_change_carries_record_per_d39(workspace):
    """Per D39: composition-change:add events MUST carry the full added
    binding's record in `payload.record` so workspace state is fully
    derivable from the event chain alone."""
    ws = workspace
    ws.register_agent_actor(id="subagent-rec", substrate_binding="primary")
    comp_events = ws.event_chain.by_payload_subtype("composition-change")
    add_events = [
        e for e in comp_events
        if e["payload"]["change-type"] == "add"
        and e["payload"].get("binding-reference") == "subagent-rec"
    ]
    assert len(add_events) == 1
    record = add_events[0]["payload"].get("record")
    assert isinstance(record, dict)
    assert record["id"] == "subagent-rec"
    assert record["subtype"] == "agent-actor"
    assert record["substrate-binding"] == "primary"


def test_e2e_actor_registry_derivable_from_event_chain(workspace):
    """Per D39 (Bref-closed): replaying composition-change:add events against
    a fresh WorkspaceState reconstructs every actor — including
    manifest-declared ones, which now seed via synthetic composition-change
    events at boot.
    """
    from fresh_plan.runtime.workspace_state import WorkspaceState

    ws = workspace
    ws.register_agent_actor(id="subagent-replay-a", substrate_binding="primary")
    ws.register_agent_actor(id="subagent-replay-b", substrate_binding="primary")

    replayed = WorkspaceState()
    for e in ws.event_chain.by_payload_subtype("composition-change"):
        p = e["payload"]
        if p["change-type"] == "add" and p.get("binding-kind") == "actor":
            replayed.add_actor(p["record"])

    # Manifest actors + runtime sub-agents all reconstructed.
    assert replayed.has_actor("human-1")
    assert replayed.has_actor("agent-primary")
    assert replayed.has_actor("subagent-replay-a")
    assert replayed.has_actor("subagent-replay-b")
    assert replayed.get_actor("subagent-replay-a")["substrate-binding"] == "primary"


def test_e2e_state_at_reflects_runtime_added_actors(workspace):
    """Per D40 §A: Workspace.state_at(n) replays events 0..n. Runtime-added
    sub-agents (D19 + D39) appear in the replayed state at and after their
    composition-change event."""
    ws = workspace
    # Capture initial chain length (post-boot: N manifest-actor seeds +
    # the boot lifecycle event already in the chain).
    initial_len = len(ws.event_chain)
    ws.register_agent_actor(id="sub-state-at", substrate_binding="primary")
    # The composition-change event is at sequence initial_len.
    comp_seq = initial_len
    # Before composition-change: no sub-agent in replayed state.
    state_before = ws.state_at(comp_seq - 1)
    assert not state_before.has_actor("sub-state-at")
    # At composition-change: sub-agent appears.
    state_after = ws.state_at(comp_seq)
    assert state_after.has_actor("sub-state-at")


def test_e2e_chain_remains_continuous(workspace):
    ws = workspace
    primary = ws.actors["agent-primary"]
    for i in range(5):
        primary.emit_action(f"step-{i}", parameters={})
    ws.shutdown()
    events = list(ws.events())
    for prior, current in zip(events, events[1:]):
        assert current["prev-event"] == prior["id"]


# ---------------------------------------------------------------
# B3 — generic-shape end-to-end (D13 authority-binding enforcement)
# ---------------------------------------------------------------


def test_e2e_generic_shape_attached_and_enforces_authority_bindings():
    """Per D13 + B3: shape is attached at boot, hook stubs registered, and
    authority-bindings reject `claim` events lacking the author role.
    """
    manifest = json.loads((GENERIC_SHAPE_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, GENERIC_SHAPE_FIXTURE / "extensions")
    try:
        # Shape attached + hook stubs registered.
        assert ws.substrate.shape is not None
        assert ws.substrate.shape.id == "generic-shape"
        registered = set(ws.hooks.registered_names())
        assert {"pre-event-emit", "post-event-emit"} <= registered

        primary = ws.actors["agent-primary"]

        # Valid claim with role=author on an agent-actor passes.
        primary.emit_claim("section drafted", role="author")

        # Claim without the author role is rejected by the authority binding.
        with pytest.raises(EventRejected) as excinfo:
            primary.emit_claim("unauthorized claim")
        assert any(f.category == "authority" for f in excinfo.value.failures)
    finally:
        ws.shutdown()


# ---------------------------------------------------------------
# B4 — MCP tool-adapter end-to-end (D16 stub adapter)
# ---------------------------------------------------------------


def test_e2e_mcp_adapter_call_emits_action_into_chain():
    """Per D16 + B4: boot a workspace binding the mcp-tool-adapter; call()
    emits an action event with the right outcome-reference; B1 validation
    passed (boot did not raise)."""
    manifest = json.loads((MCP_ADAPTER_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, MCP_ADAPTER_FIXTURE / "extensions")
    try:
        adapter = ws.adapter("primary-mcp")
        response = adapter.call("echo", {"x": 1})
        actions = ws.event_chain.by_payload_subtype("action")
        assert len(actions) == 1
        emitted = actions[0]
        assert emitted["payload"]["action-name"] == "echo"
        assert emitted["payload"]["parameters"] == {"x": 1}
        assert emitted["payload"]["outcome-reference"] == response["outcome-reference"]
    finally:
        ws.shutdown()


# ---------------------------------------------------------------
# B6 — generic specialist end-to-end (D19 + D37)
# ---------------------------------------------------------------


def test_e2e_generic_specialist_skill_invocation_emits_action():
    """Per D19 + B6: boot a workspace binding generic-specialist + the
    required mcp-tool-adapter; the specialist resolves its adapter binding,
    registers `do-task` into substrate.skills, and invoking the skill emits
    one action event into the chain."""
    manifest = json.loads((GENERIC_SPECIALIST_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, GENERIC_SPECIALIST_FIXTURE / "extensions")
    try:
        specialist = ws.specialist("primary-specialist")
        assert specialist is not None
        # Required adapter is resolved + present in the specialist's _adapters.
        assert ws.adapter("primary-mcp") is specialist._adapters[
            "mcp-server-ext:mcp-tool-adapter"
        ]
        # Skill invocation emits an action event.
        before = len(ws.event_chain.by_payload_subtype("action"))
        response = ws.substrate.skills.invoke("do-task", {"target": "doc-1"})
        actions = ws.event_chain.by_payload_subtype("action")
        assert len(actions) == before + 1
        emitted = actions[-1]
        assert emitted["payload"]["action-name"] == "do-task"
        assert emitted["payload"]["parameters"] == {"target": "doc-1"}
        assert response["ok"] is True
        assert response["stub"] is True
    finally:
        ws.shutdown()


# ---------------------------------------------------------------
# B7 — minimal RAG-via-MCP end-to-end (D19 + D38; protocol-vs-provision)
# ---------------------------------------------------------------


def test_e2e_rag_specialist_retrieve_emits_chained_action_events():
    """Per D38 + B7: boot a workspace binding rag-specialist + rag-retriever-adapter
    (both reusing mcp-server-ext:mcp-client); invoking `retrieve` produces two
    action events in the chain — specialist's own emission, then the adapter's
    action from adapter.call — and the specialist response references the
    adapter's outcome-reference.
    """
    manifest = json.loads((RAG_VIA_MCP_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, RAG_VIA_MCP_FIXTURE / "extensions")
    try:
        specialist = ws.specialist("primary-rag-specialist")
        assert specialist is not None
        # Required retriever adapter is resolved + present in the specialist's _adapters.
        assert ws.adapter("primary-rag-retriever") is specialist._adapters[
            "rag-via-mcp-ext:rag-retriever-adapter"
        ]
        before = len(ws.event_chain.by_payload_subtype("action"))
        response = ws.substrate.skills.invoke(
            "retrieve", {"query": "doc-1", "k": 2}
        )
        actions = ws.event_chain.by_payload_subtype("action")
        assert len(actions) == before + 2
        # Order: specialist emission first, then adapter emission via adapter.call.
        assert actions[-2]["payload"]["action-name"] == "retrieve"
        assert "outcome-reference" not in actions[-2]["payload"]
        assert actions[-1]["payload"]["action-name"] == "retrieve"
        assert actions[-1]["payload"]["outcome-reference"] == response["adapter-outcome-ref"]
        # Chain continuity across the two action events.
        assert actions[-1]["prev-event"] == actions[-2]["id"]
        assert response["ok"] is True
        assert response["stub"] is True
        assert len(response["chunks"]) == 2
    finally:
        ws.shutdown()


# ---------------------------------------------------------------
# B2b — MS Agent Framework substrate stub end-to-end (D12 + D17 + D41)
# ---------------------------------------------------------------


def test_e2e_ms_agent_framework_specialist_skill_invocation_emits_action():
    """Per B2b + D41: same composition as the generic-specialist e2e but
    hosted on the MSAgentFrameworkSubstrate stub; specialist invocation
    still lands an action event into the chain."""
    manifest = json.loads((MS_AGENT_FRAMEWORK_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, MS_AGENT_FRAMEWORK_FIXTURE / "extensions")
    try:
        before = len(ws.event_chain.by_payload_subtype("action"))
        ws.substrate.skills.invoke("do-task", {"target": "ms-doc-1"})
        actions = ws.event_chain.by_payload_subtype("action")
        assert len(actions) == before + 1
        assert actions[-1]["payload"]["action-name"] == "do-task"
    finally:
        ws.shutdown()
