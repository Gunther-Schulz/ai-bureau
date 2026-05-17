"""Tests for D56 §B.1 — shape authority-binding additional-constraints grammar + evaluation.

Per D56 §C: 3 tests covering the contract:

  Test 1 — equals pass: constraint satisfied; event passes authority check.
  Test 2 — equals fail: constraint unsatisfied; authority failure surfaces.
  Test 3 — boot-time grammar parse failure: WorkspaceBootError(category=
           "authority-constraint-grammar") at Shape construction.
"""
from __future__ import annotations

import json

import pytest

from fresh_plan.runtime.boot import WorkspaceBootError
from fresh_plan.runtime.shape import GenericShape
from fresh_plan.runtime.workspace_state import WorkspaceState


def _make_shape_spec(constraint_obj: dict) -> dict:
    """Build a minimal shape spec with one authority-binding carrying the constraint."""
    return {
        "id": "test-shape",
        "version": "0.1.0",
        "actor-requirements": "none",
        "required-capabilities": [],
        "optional-capabilities": [],
        "authority-bindings": [
            {
                "payload-subtype": "claim",
                "required-role": "author",
                "required-actor-subtype": "agent-actor",
                "additional-constraints": json.dumps(constraint_obj),
            }
        ],
        "roles": [{"id": "author", "description": "Test author role."}],
        "hooks": [],
    }


def _make_state_with_actor(actor_id: str, **actor_fields) -> WorkspaceState:
    state = WorkspaceState()
    actor = {"id": actor_id, "subtype": "agent-actor", **actor_fields}
    state.add_actor(actor)
    return state


def test_authority_constraint_equals_pass() -> None:
    """D56 §B.1 — equals constraint satisfied; authority check returns no failures."""
    # Constraint: event.payload.tier equals literal "trusted".
    spec = _make_shape_spec(
        {"equals": {"lhs": "event.payload.tier", "rhs": "literal:trusted"}}
    )
    shape = GenericShape(spec=spec)
    state = _make_state_with_actor("agent-1")

    event = {
        "payload-subtype": "claim",
        "actors": [{"id": "agent-1", "role": "author"}],
        "payload": {"tier": "trusted", "assertion": "ok"},
    }
    failures = shape.check_authority(event, state)
    assert failures == [], f"expected no failures; got {failures}"


def test_authority_constraint_equals_fail_surfaces_authority_failure() -> None:
    """D56 §B.1 — equals constraint unsatisfied; one authority failure citing constraint."""
    spec = _make_shape_spec(
        {"equals": {"lhs": "event.payload.tier", "rhs": "literal:trusted"}}
    )
    shape = GenericShape(spec=spec)
    state = _make_state_with_actor("agent-1")

    event = {
        "payload-subtype": "claim",
        "actors": [{"id": "agent-1", "role": "author"}],
        "payload": {"tier": "untrusted", "assertion": "no"},
    }
    failures = shape.check_authority(event, state)
    assert len(failures) == 1
    failure = failures[0]
    assert failure.category == "authority"
    assert "additional-constraints" in failure.path
    assert "evaluated false" in failure.reason


def test_authority_constraint_grammar_violation_at_shape_construction() -> None:
    """D56 §B.1 — malformed constraint raises WorkspaceBootError(category=
    "authority-constraint-grammar") at Shape.__init__.
    """
    # Top-level admits only 'equals' or 'in'.
    spec = _make_shape_spec({"unknown-op": "x"})

    with pytest.raises(WorkspaceBootError) as exc_info:
        GenericShape(spec=spec)
    failures = exc_info.value.failures
    assert len(failures) == 1
    assert failures[0].category == "authority-constraint-grammar"
