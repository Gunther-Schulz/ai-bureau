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


# ---------------------------------------------------------------
# D50 — specialist cluster supersedes per D45 §C
# ---------------------------------------------------------------


def test_skill_execution_error_propagates_with_structured_fields(booted_workspace):
    """D50 §B.1: SkillExecutionError carries structured fields (specialist_id,
    skill_id, category, detail) + chains the original exception via `from`.

    Phase B stubs cannot fail meaningfully; this test uses a monkeypatched
    subclass to exercise the forward-bar contract Phase C+ real-wire impls
    must honor. Direct invocation path: caller catches SkillExecutionError raw.
    """
    from fresh_plan.runtime.specialist import SkillExecutionError

    class _FailingSpecialist(GenericSpecialist):
        def handle_skill(self, skill_id, params):
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="domain-error",
                detail={"reason": "required-citation missing", "section": "§3.2"},
            )

    failing = _FailingSpecialist(spec=dict(SPECIALIST_SPEC))
    failing.attach_workspace(booted_workspace)

    with pytest.raises(SkillExecutionError) as excinfo:
        failing.handle_skill("do-task", {"section": "§3.2"})

    e = excinfo.value
    assert e.specialist_id == "generic-specialist"
    assert e.skill_id == "do-task"
    assert e.category == "domain-error"
    assert e.detail == {"reason": "required-citation missing", "section": "§3.2"}
    # Structured diagnostic visible without reading server logs.
    assert "[domain-error]" in str(e)
    assert "generic-specialist" in str(e)
    assert "do-task" in str(e)


def test_skill_execution_error_aggregated_via_subscriber_dispatch(booted_workspace):
    """D50 §B.2 composition with D47 §B.1: SkillExecutionError raised inside
    a specialist's on_event (subscriber-dispatch path; via delegation to
    handle_skill) is captured into substrate._subscriber_failures and
    aggregated as SubscriberDispatchError after the outer drain completes.
    """
    from fresh_plan.runtime.specialist import SkillExecutionError
    from fresh_plan.runtime.substrate import SubscriberDispatchError

    class _DelegatingFailingSpecialist(GenericSpecialist):
        """on_event delegates to handle_skill which raises — exercises the
        D44 + D47 + D50 composition path."""

        def handle_skill(self, skill_id, params):
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="skill-execution",
                detail={"trigger_event_id": params.get("event_id")},
            )

        def on_event(self, event):
            # Delegate to own handle_skill — will raise SkillExecutionError;
            # captured per D47 §B.1.
            self.handle_skill("react-to-event", {"event_id": event["id"]})

    delegating = _DelegatingFailingSpecialist(
        spec={
            "id": "delegating-test-specialist",
            "version": "0.1.0",
            "roles": [],
            "skills": [],
            "supported-work-unit-kinds": [],
            "required-adapter-bindings": [],
            "declared-event-subscriptions": [{"payload-subtype": "state-change"}],
        }
    )
    substrate = booted_workspace._substrate
    delegating.attach_workspace(booted_workspace)
    substrate.specialist_subscribers.append(delegating)

    actor_id = next(iter(substrate.state.actors))
    with pytest.raises(SubscriberDispatchError) as excinfo:
        booted_workspace._emit_event(
            actor_id=actor_id,
            payload_subtype="state-change",
            payload={"what": "test-state-change"},
        )

    failures = excinfo.value.failures
    assert len(failures) == 1
    spec_id, evt_id, captured_exc = failures[0]
    assert spec_id == "delegating-test-specialist"
    assert isinstance(captured_exc, SkillExecutionError)
    assert captured_exc.category == "skill-execution"
    assert captured_exc.specialist_id == "delegating-test-specialist"
    assert captured_exc.skill_id == "react-to-event"
