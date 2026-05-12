"""Tests for the B6 generic minimal specialist impl (per D19 + D37 + D36)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.specialist import (
    GenericSpecialist,
    Specialist,
    load_specialist_from_provision,
)


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
SPECIALIST_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-generic-specialist"


SPECIALIST_SPEC = {
    "id": "generic-specialist",
    "version": "0.1.0",
    "roles": ["author"],
    "skills": [
        {
            "id": "do-task",
            "description": "Generic task execution skill.",
        }
    ],
    "supported-work-unit-kinds": ["generic-specialist-ext:generic-task"],
    "required-adapter-bindings": ["mcp-server-ext:mcp-tool-adapter"],
    "required-substrate-capabilities": ["skills", "event-chain"],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-subscriptions": [{"payload-subtype": "claim"}],
}


@pytest.fixture
def specialist() -> GenericSpecialist:
    return GenericSpecialist(spec=dict(SPECIALIST_SPEC))


@pytest.fixture
def booted_workspace():
    manifest = json.loads((SPECIALIST_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, SPECIALIST_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_generic_specialist_accessors(specialist):
    assert specialist.id == "generic-specialist"
    assert specialist.version == "0.1.0"
    assert specialist.roles == ["author"]
    assert specialist.skills[0]["id"] == "do-task"
    assert specialist.supported_work_unit_kinds == [
        "generic-specialist-ext:generic-task"
    ]
    assert specialist.required_adapter_bindings == [
        "mcp-server-ext:mcp-tool-adapter"
    ]
    assert specialist.required_substrate_capabilities == ["skills", "event-chain"]
    assert specialist.declared_event_emissions == [{"payload-subtype": "action"}]
    assert specialist.declared_event_subscriptions == [{"payload-subtype": "claim"}]
    assert specialist.activation_scope is None


def test_handle_skill_before_attach_raises(specialist):
    with pytest.raises(RuntimeError) as excinfo:
        specialist.handle_skill("do-task", {})
    assert "attach_workspace" in str(excinfo.value)


def test_attach_workspace_resolves_required_adapter(booted_workspace):
    ws = booted_workspace
    specialist = ws.specialist("primary-specialist")
    assert "mcp-server-ext:mcp-tool-adapter" in specialist._adapters
    # The resolved entry is the same instance as ws.adapter("primary-mcp").
    assert (
        specialist._adapters["mcp-server-ext:mcp-tool-adapter"]
        is ws.adapter("primary-mcp")
    )


def test_attach_workspace_raises_on_missing_required_adapter(specialist):
    """Hand-built workspace stand-in with no matching adapter-binding.

    Per D48 §B.3 (adapter cluster supersedes per D45 §C): raises structured
    WorkspaceBootError(category="adapter-binding-resolution") instead of the
    pre-D48 bare RuntimeError. Path names the offending specialist binding-id
    (None here because _MockSubstrate.specialist_instances is empty) and
    references the unresolved provision via `failures[i].value`.
    """
    from fresh_plan.runtime.boot import WorkspaceBootError

    class _MockSubstrate:
        adapter_bindings: dict = {}
        specialist_instances: dict = {}
        state = None

    class _MockWorkspace:
        _substrate = _MockSubstrate()

        def _emit_event(self, *a, **kw):
            return None

        def adapter(self, bid):
            raise KeyError(bid)

    with pytest.raises(WorkspaceBootError) as excinfo:
        specialist.attach_workspace(_MockWorkspace())
    failures = excinfo.value.failures
    assert len(failures) == 1
    f = failures[0]
    assert f.category == "adapter-binding-resolution"
    assert f.value == "mcp-server-ext:mcp-tool-adapter"
    assert "mcp-server-ext:mcp-tool-adapter" in f.reason
    assert "generic-specialist" in f.reason


def test_register_skills_adds_invokable_handler(booted_workspace):
    ws = booted_workspace
    assert ws.substrate.skills.has("do-task")
    response = ws.substrate.skills.invoke("do-task", {})
    assert response == {
        "ok": True,
        "skill": "do-task",
        "stub": True,
        "parameters": {},
    }


def test_skill_invocation_emits_one_action_event(booted_workspace):
    ws = booted_workspace
    before = len(ws.event_chain.by_payload_subtype("action"))
    ws.substrate.skills.invoke("do-task", {"x": 1})
    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "do-task"
    assert emitted["payload"]["parameters"] == {"x": 1}


def test_event_subscription_fires_on_event_for_matching_subtype():
    """A subscribing specialist receives on_event for matching payload-subtypes."""

    class _RecordingSpecialist(GenericSpecialist):
        received: list = []

        def on_event(self, event: dict) -> None:
            self.received.append(event)

    manifest = json.loads((SPECIALIST_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, SPECIALIST_FIXTURE / "extensions")
    try:
        # Swap the booted specialist for a recording subclass with the same
        # spec; re-register subscription path so dispatch lands on it.
        recording = _RecordingSpecialist(spec=dict(SPECIALIST_SPEC))
        recording.attach_workspace(ws)
        ws.substrate.specialist_subscribers = [recording]

        primary = ws.actors["agent-primary"]
        primary.emit_claim("section drafted", role="author")

        assert len(recording.received) == 1
        assert recording.received[0]["payload-subtype"] == "claim"
        assert recording.received[0]["payload"]["assertion"] == "section drafted"
    finally:
        ws.shutdown()


def test_load_specialist_from_provision_finds_impl_shipped_generic_specialist():
    specialist = load_specialist_from_provision(
        "generic-specialist-ext:generic-specialist", IMPL_EXTENSIONS_DIR
    )
    assert isinstance(specialist, GenericSpecialist)
    assert isinstance(specialist, Specialist)
    assert specialist.id == "generic-specialist"
    assert specialist.version == "0.1.0"
