"""Tests for D52 §B.1 post-projection state validity check.

Verifies `Shape.check_post_event_state_validity` enforces shape policy
against the simulated post-projection state for composition-change
events. Failures surface as `ValidationFailure(category="composition-
validity")` per D52 §B.1; the substrate translates them into
`EventRejected` at step 2.5 of the emit pipeline.
"""
from __future__ import annotations

import pytest

from fresh_plan.runtime.shape import GenericShape
from fresh_plan.runtime.workspace_state import WorkspaceState


def _shape(actor_requirements):
    return GenericShape(
        spec={
            "id": "test-shape",
            "version": "0.0.1",
            "actor-requirements": actor_requirements,
            "required-capabilities": [],
            "optional-capabilities": [],
            "authority-bindings": [],
            "roles": [],
            "hooks": [],
        }
    )


def _remove_actor_event(actor_id: str) -> dict:
    return {
        "payload-subtype": "composition-change",
        "payload": {
            "change-type": "remove",
            "binding-kind": "actor",
            "binding-reference": actor_id,
        },
    }


def _add_actor_event(actor_id: str, subtype: str) -> dict:
    return {
        "payload-subtype": "composition-change",
        "payload": {
            "change-type": "add",
            "binding-kind": "actor",
            "binding-reference": actor_id,
            "record": {"id": actor_id, "subtype": subtype},
        },
    }


def test_min_violation_when_removing_last_required_actor():
    """Shape requires min=1 human-actor; removing the only one violates."""
    shape = _shape({"human-actor": {"min": 1}})
    state = WorkspaceState()
    state.add_actor({"id": "human-1", "subtype": "human-actor"})

    failures = shape.check_post_event_state_validity(
        _remove_actor_event("human-1"), state
    )

    assert len(failures) == 1
    assert failures[0].category == "composition-validity"
    assert failures[0].path == "event.payload.binding-reference"
    assert failures[0].value == "human-1"
    assert "human-actor" in failures[0].reason
    assert "min=1" in failures[0].reason


def test_max_violation_when_adding_actor_above_cap():
    """Shape caps agent-actor at max=2; adding a 3rd violates."""
    shape = _shape({"agent-actor": {"max": 2}})
    state = WorkspaceState()
    state.add_actor({"id": "agent-1", "subtype": "agent-actor"})
    state.add_actor({"id": "agent-2", "subtype": "agent-actor"})

    failures = shape.check_post_event_state_validity(
        _add_actor_event("agent-3", "agent-actor"), state
    )

    assert len(failures) == 1
    assert failures[0].category == "composition-validity"
    assert failures[0].value == "agent-3"
    assert "agent-actor" in failures[0].reason
    assert "max=2" in failures[0].reason


def test_no_check_when_actor_requirements_is_none():
    """Shape with actor-requirements='none' enforces no cardinality."""
    shape = _shape("none")
    state = WorkspaceState()
    state.add_actor({"id": "human-1", "subtype": "human-actor"})

    # Removing the only human-actor would violate if reqs were declared;
    # actor-requirements='none' means no enforcement.
    assert shape.check_post_event_state_validity(
        _remove_actor_event("human-1"), state
    ) == []


def test_state_not_mutated_by_check():
    """The check deepcopies state per D52 §B.1; live state must not change."""
    shape = _shape({"agent-actor": {"max": 2}})
    state = WorkspaceState()
    state.add_actor({"id": "agent-1", "subtype": "agent-actor"})
    state.add_actor({"id": "agent-2", "subtype": "agent-actor"})

    shape.check_post_event_state_validity(
        _add_actor_event("agent-3", "agent-actor"), state
    )

    assert set(state.actors.keys()) == {"agent-1", "agent-2"}


def test_non_composition_change_event_short_circuits():
    """Only composition-change events trigger the check."""
    shape = _shape({"human-actor": {"min": 1}})
    state = WorkspaceState()  # empty — would violate min if check ran

    claim_event = {
        "payload-subtype": "claim",
        "payload": {"assertion": "x"},
    }
    assert shape.check_post_event_state_validity(claim_event, state) == []
