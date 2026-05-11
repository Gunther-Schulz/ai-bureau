"""Tests for WorkspaceState: actor registry + work-unit tracker + scope."""
from __future__ import annotations

import pytest

from fresh_plan.runtime.workspace_state import (
    DuplicateActorError,
    InvalidWorkUnitTransitionError,
    UnknownActorError,
    UnknownWorkUnitError,
    WORK_UNIT_STATUSES,
    WorkspaceState,
)


def test_add_actor_and_lookup():
    state = WorkspaceState()
    state.add_actor({"id": "alice", "subtype": "human-actor", "declared-name": "Alice"})
    assert state.has_actor("alice")
    assert state.get_actor("alice")["declared-name"] == "Alice"


def test_unknown_actor_raises():
    state = WorkspaceState()
    with pytest.raises(UnknownActorError):
        state.get_actor("ghost")


def test_duplicate_actor_rejected():
    state = WorkspaceState()
    state.add_actor({"id": "alice", "subtype": "human-actor", "declared-name": "Alice"})
    with pytest.raises(DuplicateActorError):
        state.add_actor({"id": "alice", "subtype": "human-actor", "declared-name": "X"})


def test_work_unit_create_and_lookup():
    state = WorkspaceState()
    state.add_work_unit({"id": "wu-1", "kind": "ext:k", "status": "created"})
    assert state.has_work_unit("wu-1")
    assert state.get_work_unit("wu-1")["status"] == "created"


def test_work_unit_invalid_status_rejected():
    state = WorkspaceState()
    with pytest.raises(InvalidWorkUnitTransitionError):
        state.add_work_unit({"id": "wu-1", "status": "wat"})


def test_work_unit_transition_updates_status():
    state = WorkspaceState()
    state.add_work_unit({"id": "wu-1", "status": "created"})
    frm, to = state.transition_work_unit("wu-1", "in-progress")
    assert (frm, to) == ("created", "in-progress")
    assert state.get_work_unit("wu-1")["status"] == "in-progress"


def test_work_unit_transition_unknown_status_rejected():
    state = WorkspaceState()
    state.add_work_unit({"id": "wu-1", "status": "created"})
    with pytest.raises(InvalidWorkUnitTransitionError):
        state.transition_work_unit("wu-1", "magical")


def test_transition_unknown_work_unit_raises():
    state = WorkspaceState()
    with pytest.raises(UnknownWorkUnitError):
        state.transition_work_unit("ghost", "in-progress")


def test_set_scope_returns_prior():
    state = WorkspaceState()
    assert state.set_scope({"domain": "a"}) is None
    assert state.current_scope == {"domain": "a"}
    prior = state.set_scope({"domain": "b"})
    assert prior == {"domain": "a"}


def test_status_enum_locked_per_d20():
    # D20 fixes the lifecycle status enum at framework-core.
    assert WORK_UNIT_STATUSES == {
        "created",
        "in-progress",
        "paused",
        "completed",
        "abandoned",
    }
