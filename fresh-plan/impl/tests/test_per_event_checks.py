"""Tests for D30 §4 per-event runtime identity checks."""
from __future__ import annotations

from fresh_plan.runtime.per_event_checks import (
    CORE_PAYLOAD_SUBTYPES,
    check_event_references,
)
from fresh_plan.runtime.workspace_state import WorkspaceState


def _state_with_actors(*actor_ids: str) -> WorkspaceState:
    state = WorkspaceState()
    for aid in actor_ids:
        state.add_actor({"id": aid, "subtype": "human-actor", "declared-name": aid})
    return state


def _event(
    *,
    actors: list[dict],
    payload_subtype: str = "action",
    work_unit_id: str | None = None,
) -> dict:
    e = {
        "id": "evt-x",
        "prev-event": None,
        "timestamp": "2026-05-11T00:00:00Z",
        "actors": actors,
        "payload-subtype": payload_subtype,
        "payload": {},
    }
    if work_unit_id is not None:
        e["work-unit-id"] = work_unit_id
    return e


def test_actor_resolves_positive():
    state = _state_with_actors("alice")
    failures = check_event_references(
        _event(actors=[{"id": "alice"}]),
        state,
        set(),
        set(),
    )
    assert failures == []


def test_actor_unknown_negative():
    state = _state_with_actors("alice")
    failures = check_event_references(
        _event(actors=[{"id": "ghost"}]),
        state,
        set(),
        set(),
    )
    assert len(failures) == 1
    assert failures[0].category == "identity"
    assert "ghost" in failures[0].reason


def test_work_unit_resolves_positive():
    state = _state_with_actors("alice")
    state.add_work_unit({"id": "wu-1", "kind": "ext:k", "status": "created"})
    failures = check_event_references(
        _event(actors=[{"id": "alice"}], work_unit_id="wu-1"),
        state,
        set(),
        set(),
    )
    assert failures == []


def test_work_unit_unknown_negative():
    state = _state_with_actors("alice")
    failures = check_event_references(
        _event(actors=[{"id": "alice"}], work_unit_id="wu-missing"),
        state,
        set(),
        set(),
    )
    assert any(
        f.path == "event.work-unit-id" and "wu-missing" in f.reason for f in failures
    )


def test_payload_subtype_core_admitted():
    state = _state_with_actors("alice")
    for subtype in CORE_PAYLOAD_SUBTYPES:
        failures = check_event_references(
            _event(actors=[{"id": "alice"}], payload_subtype=subtype),
            state,
            set(),
            set(),
        )
        assert failures == [], f"core subtype {subtype} rejected: {failures}"


def test_payload_subtype_extension_registered_admitted():
    state = _state_with_actors("alice")
    failures = check_event_references(
        _event(actors=[{"id": "alice"}], payload_subtype="ext:custom-subtype"),
        state,
        {"ext:custom-subtype"},
        set(),
    )
    assert failures == []


def test_payload_subtype_unknown_rejected():
    state = _state_with_actors("alice")
    failures = check_event_references(
        _event(actors=[{"id": "alice"}], payload_subtype="ext:not-registered"),
        state,
        set(),
        set(),
    )
    assert any(
        f.category == "vocabulary" and f.path == "event.payload-subtype"
        for f in failures
    )


def test_rejected_events_do_not_enter_chain():
    """E2E with the substrate: a rejected event must NOT be appended."""
    import json
    from pathlib import Path

    from fresh_plan.runtime import EventRejected, Workspace

    here = Path(__file__).parent / "fixtures" / "workspace-substrate-test"
    manifest = json.loads((here / "workspace.json").read_text())
    with Workspace.boot(manifest, here / "extensions") as ws:
        before = len(ws.event_chain)
        bad = {
            "id": "evt-bad",
            "prev-event": ws.event_chain.tail["id"],
            "timestamp": "2026-05-11T00:00:00.000000Z",
            "actors": [{"id": "ghost-actor"}],
            "payload-subtype": "action",
            "payload": {"action-name": "noop"},
        }
        try:
            ws.substrate.append_event(bad)
        except EventRejected:
            pass
        assert len(ws.event_chain) == before


# ---------------------------------------------------------------
# D51 §B.1 — per-work-unit identity checks at work-unit-creation event time
# ---------------------------------------------------------------


def _work_unit_created_event(
    *,
    actors: list[dict],
    after: dict,
) -> dict:
    """Construct a state-change/work-unit-created event with given record."""
    return {
        "id": "evt-wu-create",
        "prev-event": None,
        "timestamp": "2026-05-12T00:00:00Z",
        "actors": actors,
        "payload-subtype": "state-change",
        "payload": {"what": "work-unit-created", "after": after},
    }


def test_work_unit_created_with_valid_references_passes():
    """D51 §B.1: valid contributing-actors + contributing-specialists + kind → no failures."""
    state = _state_with_actors("alice", "bob")
    event = _work_unit_created_event(
        actors=[{"id": "alice"}],
        after={
            "id": "wu-1",
            "kind": "ext:task",
            "contributing-actors": [{"id": "alice"}, {"id": "bob"}],
            "contributing-specialists": ["sp-primary"],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=["sp-primary"],
        registered_work_unit_kinds=["ext:task"],
    )
    assert failures == []


def test_work_unit_created_with_unknown_contributing_actor_fails():
    """D51 §B.1 (i): contributing-actors[].id referencing non-existent actor → identity failure."""
    state = _state_with_actors("alice")
    event = _work_unit_created_event(
        actors=[{"id": "alice"}],
        after={
            "id": "wu-1",
            "kind": "ext:task",
            "contributing-actors": [{"id": "alice"}, {"id": "ghost"}],
            "contributing-specialists": [],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=[],
        registered_work_unit_kinds=["ext:task"],
    )
    assert len(failures) == 1
    f = failures[0]
    assert f.category == "identity"
    assert "contributing-actors[1].id" in f.path
    assert f.value == "ghost"


def test_work_unit_created_with_unbound_specialist_fails():
    """D51 §B.1 (ii): contributing-specialists[] referencing unbound binding-id → failure."""
    state = _state_with_actors("alice")
    event = _work_unit_created_event(
        actors=[{"id": "alice"}],
        after={
            "id": "wu-1",
            "kind": "ext:task",
            "contributing-actors": [{"id": "alice"}],
            "contributing-specialists": ["sp-bound", "sp-unbound"],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=["sp-bound"],
        registered_work_unit_kinds=["ext:task"],
    )
    assert len(failures) == 1
    f = failures[0]
    assert f.category == "identity"
    assert "contributing-specialists[1]" in f.path
    assert f.value == "sp-unbound"


def test_work_unit_created_with_unregistered_kind_fails():
    """D51 §B.1 (iii): kind not registered → failure."""
    state = _state_with_actors("alice")
    event = _work_unit_created_event(
        actors=[{"id": "alice"}],
        after={
            "id": "wu-1",
            "kind": "ext:unknown-kind",
            "contributing-actors": [{"id": "alice"}],
            "contributing-specialists": [],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=[],
        registered_work_unit_kinds=["ext:task"],
    )
    assert len(failures) == 1
    f = failures[0]
    assert f.category == "identity"
    assert "kind" in f.path
    assert f.value == "ext:unknown-kind"


# ---------------------------------------------------------------
# §B-3 (D62 §B cheap impl) — event.actors[].role vocabulary check
# ---------------------------------------------------------------


def test_event_actor_role_not_in_shape_vocabulary_fails():
    """§B-3: role on event.actors[] must be declared in the bound shape's roles[]."""
    state = _state_with_actors("alice")
    event = _event(
        actors=[{"id": "alice", "role": "fabricated-role"}],
        payload_subtype="action",
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        shape_role_ids={"author", "reviewer"},
    )
    assert len(failures) == 1
    f = failures[0]
    assert f.category == "vocabulary"
    assert f.path == "event.actors[0].role"
    assert f.value == "fabricated-role"


def test_event_actor_role_present_in_shape_vocabulary_passes():
    """§B-3: role declared in shape vocabulary passes; absent role also passes (optional)."""
    state = _state_with_actors("alice", "bob")
    event_with_role = _event(
        actors=[{"id": "alice", "role": "author"}],
        payload_subtype="action",
    )
    failures = check_event_references(
        event_with_role,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        shape_role_ids={"author", "reviewer"},
    )
    assert failures == []
    # Role absence is legal (only authority-bindings require role; check is
    # a vocabulary-when-present check, not a presence requirement).
    event_no_role = _event(
        actors=[{"id": "bob"}],
        payload_subtype="action",
    )
    failures = check_event_references(
        event_no_role,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        shape_role_ids={"author", "reviewer"},
    )
    assert failures == []


# ---------------------------------------------------------------
# §B-7 (D62 §B cheap impl) — work-unit contributing-actors[].role vocabulary
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# §B-4 (D62 §B cheap impl) — work-unit.payload schema validation
# ---------------------------------------------------------------


def test_work_unit_payload_validates_against_registered_schema_pass():
    """§B-4: payload conforms to registered schema → no failures."""
    state = _state_with_actors("alice")
    schema = {
        "type": "object",
        "required": ["task-id"],
        "properties": {"task-id": {"type": "string"}},
    }
    event = _work_unit_created_event(
        actors=[{"id": "alice"}],
        after={
            "id": "wu-1",
            "kind": "ext:task",
            "payload": {"task-id": "T-001"},
            "contributing-actors": [{"id": "alice"}],
            "contributing-specialists": [],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=[],
        registered_work_unit_kinds=["ext:task"],
        work_unit_kind_payload_schemas={"ext:task": schema},
    )
    assert failures == []


def test_work_unit_payload_missing_required_field_fails():
    """§B-4: payload missing required field per registered schema → vocabulary failure."""
    state = _state_with_actors("alice")
    schema = {
        "type": "object",
        "required": ["task-id"],
        "properties": {"task-id": {"type": "string"}},
    }
    event = _work_unit_created_event(
        actors=[{"id": "alice"}],
        after={
            "id": "wu-1",
            "kind": "ext:task",
            "payload": {"unrelated": "value"},  # missing 'task-id'
            "contributing-actors": [{"id": "alice"}],
            "contributing-specialists": [],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=[],
        registered_work_unit_kinds=["ext:task"],
        work_unit_kind_payload_schemas={"ext:task": schema},
    )
    assert len(failures) >= 1
    f = failures[0]
    assert f.category == "vocabulary"
    assert "payload" in f.path
    assert "ext:task" in f.reason


def test_work_unit_contributing_actor_role_unknown_fails():
    """§B-7: contributing-actors[].role must appear in shape's roles[] vocabulary."""
    state = _state_with_actors("alice")
    event = _work_unit_created_event(
        actors=[{"id": "alice", "role": "author"}],
        after={
            "id": "wu-1",
            "kind": "ext:task",
            "contributing-actors": [
                {"id": "alice", "role": "author"},
                {"id": "alice", "role": "ghost-role"},
            ],
            "contributing-specialists": [],
        },
    )
    failures = check_event_references(
        event,
        state,
        CORE_PAYLOAD_SUBTYPES,
        known_binding_ids=[],
        known_specialist_binding_ids=[],
        registered_work_unit_kinds=["ext:task"],
        shape_role_ids={"author", "reviewer"},
    )
    assert len(failures) == 1
    f = failures[0]
    assert f.category == "vocabulary"
    assert "contributing-actors[1].role" in f.path
    assert f.value == "ghost-role"
