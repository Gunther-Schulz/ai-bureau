"""B8 end-to-end scenario (Phase B closure trigger per D36 §C + D41 + D42).

Boots the workspace-end-to-end fixture composing all five shipped
extensions; exercises all 8 layer-2 kinds, emits ≥1 event of each of
the 5 core payload-subtypes, transitions a work-unit through ≥2
lifecycle states, verifies B1 conformance, verifies state_at(n)
replay per D40 §A, and verifies chain integrity end-to-end.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.substrate import Substrate
from fresh_plan.validator import validate_workspace_boot


E2E_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-end-to-end"


def _load_manifest() -> dict:
    return json.loads((E2E_FIXTURE / "workspace.json").read_text())


@pytest.fixture
def workspace():
    ws = Workspace.boot(_load_manifest(), E2E_FIXTURE / "extensions")
    yield ws
    ws.shutdown()


def _run_full_payload_walk(ws: Workspace) -> None:
    """Walk the workspace through events of each of the five core payload-subtypes."""
    ws.register_agent_actor(id="sub-e2e", substrate_binding="primary")
    primary = ws.actors["agent-primary"]
    primary.emit_claim("section drafted", role="author", confidence="high")
    primary.emit_state_change("scope", after={"focus": "task-A"})
    ws.substrate.skills.invoke("do-task", {"target": "T1"})
    ws.adapter("primary-direct").call("ping", {"x": 1})


def test_b8_boot_succeeds_with_all_eight_kinds_present(workspace):
    """All 8 layer-2 kinds (D25) are observable on a freshly booted workspace."""
    ws = workspace

    # D12 — substrate.
    assert isinstance(ws.substrate, Substrate)

    # D13 — shape.
    assert ws.substrate.shape is not None
    assert ws.substrate.shape.id == "generic-shape"

    # D9 — actor (both core subtypes exercised).
    assert ws.actors["agent-primary"].record["subtype"] == "agent-actor"
    assert ws.actors["human-supervisor"].record["subtype"] == "human-actor"

    # D16 — adapter (multi-binding composition).
    assert "primary-mcp" in ws.adapters
    assert "primary-direct" in ws.adapters

    # D19 — specialist.
    assert "primary-specialist" in ws.specialists

    # D10 — event chain (per Bref closure of D39: boot emits N
    # composition-change:add events for manifest actors, then the
    # lifecycle-transition:boot event).
    assert len(ws.event_chain) >= 1

    # D7 — workspace identity.
    assert ws.workspace_id == "end-to-end-ws"

    # D20 — work-unit kind is exercised by test 3 (creation + lifecycle).


def test_b8_emits_all_five_core_payload_subtypes(workspace):
    """All five D10 + D23 core payload-subtypes appear in the chain after the scripted walk."""
    ws = workspace
    _run_full_payload_walk(ws)
    subtypes = {e["payload-subtype"] for e in ws.events()}
    assert subtypes >= {
        "claim",
        "action",
        "state-change",
        "composition-change",
        "lifecycle-transition",
    }


def test_b8_work_unit_lifecycle_through_extension_registered_kind(workspace):
    """D20 work-unit lifecycle: create → in-progress → completed produces state-change events."""
    ws = workspace
    wu = ws.create_work_unit(
        id="wu-e2e-1",
        kind="generic-specialist-ext:generic-task",
        payload={"note": "test"},
    )
    wu.transition("in-progress")
    wu.transition("completed")
    assert wu.status == "completed"

    status_changes = [
        e
        for e in ws.events()
        if e["payload-subtype"] == "state-change"
        and e["payload"].get("what") == "work-unit-status"
    ]
    assert len(status_changes) >= 2


def test_b8_state_at_replay_reproduces_event_driven_state(workspace):
    """D40 §A state-at(n) replay reflects event-driven state per D39.

    Per Bref closure of D39, replay reproduces ALL state, including
    paths previously surfaced as tensions:
      (a) manifest-declared actors (now seeded at boot via synthetic
          composition-change:add events; full record in payload.record).
      (b) work-units (full record now carried in state-change:work-unit-
          created's payload.after; status changes projected from
          state-change:work-unit-status).
    """
    ws = workspace
    ws.register_agent_actor(id="sub-e2e", substrate_binding="primary")
    ws.actors["agent-primary"].emit_state_change(
        "scope", after={"focus": "replay-check"}
    )
    wu = ws.create_work_unit(
        id="wu-replay-1",
        kind="generic-specialist-ext:generic-task",
        payload={"note": "replay"},
    )
    wu.transition("in-progress")

    state = ws.state_at(len(ws.event_chain) - 1)
    # Manifest-declared actors reproduced (Bref closure of D39 tension 1).
    assert state.has_actor("agent-primary")
    assert state.has_actor("human-supervisor")
    # Runtime-added sub-agent reproduced.
    assert state.has_actor("sub-e2e")
    # Scope reproduced.
    assert state.current_scope == {"focus": "replay-check"}
    # Work-unit full record reproduced (Bref closure of D39 tension 2).
    assert state.has_work_unit("wu-replay-1")
    replayed_wu = state.get_work_unit("wu-replay-1")
    assert replayed_wu["kind"] == "generic-specialist-ext:generic-task"
    assert replayed_wu["payload"] == {"note": "replay"}
    assert replayed_wu["status"] == "in-progress"


def test_b8_validator_accepts_workspace_manifest():
    """D29 + D30 + D32 + D33: B1 conformance validator accepts the B8 fixture."""
    manifest = _load_manifest()
    result = validate_workspace_boot(manifest, E2E_FIXTURE / "extensions")
    if not result.success:
        pytest.fail(f"B1 validation failed: {result.failures}")
    assert result.success


def test_b8_chain_integrity_across_full_scenario(workspace):
    """D10 prev-event chain integrity holds across the full scripted scenario."""
    ws = workspace
    _run_full_payload_walk(ws)
    wu = ws.create_work_unit(
        id="wu-integrity", kind="generic-specialist-ext:generic-task", payload={}
    )
    wu.transition("in-progress")
    wu.transition("completed")

    events = list(ws.events())
    assert events[0]["prev-event"] is None
    for prior, current in zip(events, events[1:]):
        assert current["prev-event"] == prior["id"]


def test_b8_shutdown_emits_lifecycle_transition_shutdown():
    """D10 lifecycle-transition:shutdown lands as the last event in the chain."""
    ws = Workspace.boot(_load_manifest(), E2E_FIXTURE / "extensions")
    ws.actors["agent-primary"].emit_action("noop", parameters={})
    ws.shutdown()

    tail = ws.event_chain.tail
    assert tail["payload-subtype"] == "lifecycle-transition"
    assert tail["payload"]["transition-type"] == "shutdown"
