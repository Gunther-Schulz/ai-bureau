"""End-to-end substrate scenario test (B2 brief §"Tests" § test_substrate_e2e.py).

Boot a workspace; register a sub-agent (composition-change); emit claim +
action + state-change events; create + transition a work-unit; shutdown.
Verify the event chain has the expected sequence + types.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"


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
        kind="ext:dummy-kind",
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
    wu = ws.create_work_unit(id="wu-1", kind="ext:k", payload={})
    wu.transition("in-progress")
    wu.transition("completed")
    ws.shutdown()

    subtypes = [e["payload-subtype"] for e in ws.events()]
    assert subtypes[0] == "lifecycle-transition"  # boot
    assert subtypes[-1] == "lifecycle-transition"  # shutdown
    # Every core subtype except composition-change appears via actor emits;
    # composition-change appears via register_agent_actor.
    assert "composition-change" in subtypes
    assert "claim" in subtypes
    assert "action" in subtypes
    assert "state-change" in subtypes


def test_e2e_work_unit_id_propagates_to_events(workspace):
    """Per D23 + D20 — events referencing a work-unit carry work-unit-id."""
    ws = workspace
    wu = ws.create_work_unit(id="wu-track", kind="ext:k", payload={})
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
    """Per D39: replaying composition-change:add events against a fresh
    WorkspaceState reconstructs the runtime-added actors."""
    from fresh_plan.runtime.workspace_state import WorkspaceState

    ws = workspace
    ws.register_agent_actor(id="subagent-replay-a", substrate_binding="primary")
    ws.register_agent_actor(id="subagent-replay-b", substrate_binding="primary")

    replayed = WorkspaceState()
    # Seed with manifest-declared actors (boot snapshot — out of band of
    # the runtime composition-change path; B2-followon-2 will provide
    # state_at(n) that includes this).
    for aid, rec in ws.substrate.state.actors.items():
        if aid in {"subagent-replay-a", "subagent-replay-b"}:
            continue
        replayed.add_actor(rec)
    # Apply composition-change:add events.
    for e in ws.event_chain.by_payload_subtype("composition-change"):
        p = e["payload"]
        if p["change-type"] == "add" and p.get("binding-kind") == "actor":
            replayed.add_actor(p["record"])

    assert replayed.has_actor("subagent-replay-a")
    assert replayed.has_actor("subagent-replay-b")
    assert replayed.get_actor("subagent-replay-a")["substrate-binding"] == "primary"


def test_e2e_chain_remains_continuous(workspace):
    ws = workspace
    primary = ws.actors["agent-primary"]
    for i in range(5):
        primary.emit_action(f"step-{i}", parameters={})
    ws.shutdown()
    events = list(ws.events())
    for prior, current in zip(events, events[1:]):
        assert current["prev-event"] == prior["id"]
