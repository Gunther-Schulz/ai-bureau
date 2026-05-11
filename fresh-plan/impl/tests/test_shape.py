"""Tests for the B3 generic minimal shape impl (per D13 + D26)."""
from __future__ import annotations

from pathlib import Path

import pytest

from fresh_plan.runtime.hooks import HookRegistry
from fresh_plan.runtime.shape import GenericShape, load_shape_from_provision
from fresh_plan.runtime.workspace_state import WorkspaceState


IMPL_EXTENSIONS_DIR = (
    Path(__file__).resolve().parents[1] / "extensions"
)


GENERIC_SHAPE_SPEC = {
    "id": "generic-shape",
    "version": "0.1.0",
    "actor-requirements": "none",
    "required-capabilities": ["hooks", "skills"],
    "optional-capabilities": ["event-streaming"],
    "authority-bindings": [
        {
            "payload-subtype": "claim",
            "required-role": "author",
            "required-actor-subtype": "agent-actor",
        }
    ],
    "roles": [
        {"id": "author", "description": "Generic emitter role."},
        {"id": "reviewer", "description": "Generic witness role."},
    ],
    "hooks": [
        {"name": "pre-event-emit", "purpose": "Fired before an event is appended."},
        {"name": "post-event-emit", "purpose": "Fired after an event is appended."},
    ],
}


@pytest.fixture
def shape() -> GenericShape:
    return GenericShape(spec=GENERIC_SHAPE_SPEC)


@pytest.fixture
def state() -> WorkspaceState:
    s = WorkspaceState()
    s.add_actor({"id": "agent-1", "subtype": "agent-actor"})
    s.add_actor({"id": "human-1", "subtype": "human-actor"})
    return s


def test_generic_shape_accessors(shape):
    assert shape.id == "generic-shape"
    assert shape.version == "0.1.0"
    assert shape.required_capabilities == ["hooks", "skills"]
    assert shape.optional_capabilities == ["event-streaming"]
    assert shape.actor_requirements == "none"
    assert len(shape.authority_bindings) == 1
    assert shape.authority_bindings[0]["payload-subtype"] == "claim"
    role_ids = {r["id"] for r in shape.roles}
    assert role_ids == {"author", "reviewer"}
    hook_names = {h["name"] for h in shape.hooks}
    assert hook_names == {"pre-event-emit", "post-event-emit"}


def test_check_authority_passes_on_matching_role_and_subtype(shape, state):
    event = {
        "payload-subtype": "claim",
        "actors": [{"id": "agent-1", "role": "author"}],
        "payload": {"assertion": "ok"},
    }
    assert shape.check_authority(event, state) == []


def test_check_authority_fails_on_wrong_role(shape, state):
    event = {
        "payload-subtype": "claim",
        "actors": [{"id": "agent-1", "role": "reviewer"}],
        "payload": {"assertion": "ok"},
    }
    failures = shape.check_authority(event, state)
    assert len(failures) == 1
    assert failures[0].category == "authority"
    assert failures[0].path == "event.actors"
    assert "author" in failures[0].reason


def test_check_authority_fails_on_wrong_subtype(shape, state):
    event = {
        "payload-subtype": "claim",
        "actors": [{"id": "human-1", "role": "author"}],
        "payload": {"assertion": "ok"},
    }
    failures = shape.check_authority(event, state)
    assert len(failures) == 1
    assert failures[0].category == "authority"
    assert "agent-actor" in failures[0].reason


def test_check_authority_passes_when_binding_not_applicable(shape, state):
    event = {
        "payload-subtype": "action",
        "actors": [{"id": "agent-1"}],
        "payload": {"action-name": "noop"},
    }
    assert shape.check_authority(event, state) == []


def test_check_authority_skips_when_actors_empty(shape, state):
    event = {
        "payload-subtype": "claim",
        "actors": [],
        "payload": {"assertion": "ok"},
    }
    assert shape.check_authority(event, state) == []


def test_register_stub_handlers_makes_hooks_firable(shape):
    registry = HookRegistry()
    shape.register_stub_handlers(registry)
    assert set(registry.registered_names()) == {"pre-event-emit", "post-event-emit"}
    assert registry.handler_count("pre-event-emit") == 1
    assert registry.fire("pre-event-emit", {}) == [None]
    assert registry.fire("post-event-emit", {}) == [None]


def test_load_shape_from_provision_finds_impl_shipped_generic_shape():
    shape = load_shape_from_provision(
        "generic-shape-ext:generic-shape", IMPL_EXTENSIONS_DIR
    )
    assert isinstance(shape, GenericShape)
    assert shape.id == "generic-shape"
    assert shape.version == "0.1.0"
    assert shape.authority_bindings[0]["required-role"] == "author"


def test_check_authority_honours_qualifier_when_binding_declares_one(state):
    spec = dict(GENERIC_SHAPE_SPEC)
    spec["authority-bindings"] = [
        {
            "payload-subtype": "claim",
            "qualifier": "defensibility-grade",
            "required-role": "attester",
            "required-actor-subtype": "agent-actor",
        }
    ]
    shape = GenericShape(spec=spec)
    # Qualifier not matching => binding doesn't apply => no failure.
    event_no_qual = {
        "payload-subtype": "claim",
        "actors": [{"id": "agent-1"}],
        "payload": {"assertion": "x"},
    }
    assert shape.check_authority(event_no_qual, state) == []
    # Qualifier matching, missing attester role => failure.
    event_with_qual = {
        "payload-subtype": "claim",
        "actors": [{"id": "agent-1", "role": "reporter"}],
        "payload": {"assertion": "x", "qualifier": "defensibility-grade"},
    }
    failures = shape.check_authority(event_with_qual, state)
    assert len(failures) == 1
    assert failures[0].category == "authority"
    assert "defensibility-grade" in failures[0].reason
