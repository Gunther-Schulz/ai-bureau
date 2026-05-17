"""Tests for D55 §B.1 — specialist activation-scope minimal grammar + dispatch gate.

Per D55 §C: three tests covering the activation-scope contract:

  Test 1 — literal "always": specialist activates for every event.
  Test 2 — structured predicate match + non-match: activates only when
           the predicate evaluates True against the event.
  Test 3 — boot-time grammar violation: WorkspaceBootError(category=
           "activation-scope-grammar") at attach time.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.boot import WorkspaceBootError
from fresh_plan.runtime.specialist import Specialist


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"


@pytest.fixture
def workspace():
    manifest = json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, SUBSTRATE_FIXTURE / "extensions")
    yield ws
    ws.shutdown()


def _attach_test_specialist(ws: Workspace, specialist: Specialist) -> None:
    """Mount a test-only Specialist onto the running workspace."""
    specialist.attach_workspace(ws)
    ws.substrate.specialist_subscribers.append(specialist)


class _RecordingSpecialist(Specialist):
    """Records on_event invocations for assertion."""

    def __init__(self, spec: dict) -> None:
        super().__init__(spec=spec)
        self.observed: list[dict] = []

    def on_event(self, event: dict) -> None:
        self.observed.append(event)


def test_activation_scope_always_admits_all_events(workspace) -> None:
    """D55 §B.1 — literal "always" admits every dispatched event.

    Specialist subscribed to payload-subtype "claim"; emit a claim event;
    assert on_event fired once with the claim.
    """
    ws = workspace
    spec = {
        "id": "test-always-specialist",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
        "activation-scope": "always",
    }
    sp = _RecordingSpecialist(spec=spec)
    _attach_test_specialist(ws, sp)

    actor = next(iter(ws.actors.values()))
    actor.emit_claim("hello")

    assert len(sp.observed) == 1
    assert sp.observed[0]["payload-subtype"] == "claim"


def test_activation_scope_when_predicate_filters_dispatched_events(
    workspace,
) -> None:
    """D55 §B.1 — {"when": {"payload-subtype": "claim"}} gates per-event activation.

    Specialist declares subscriptions for two payload-subtypes (claim +
    action) but activation-scope predicate restricts to claim only.
    Emit one claim + one action; assert on_event fires once for claim.
    """
    ws = workspace
    spec = {
        "id": "test-when-specialist",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [
            {"payload-subtype": "claim"},
            {"payload-subtype": "action"},
        ],
        "activation-scope": {"when": {"payload-subtype": "claim"}},
    }
    sp = _RecordingSpecialist(spec=spec)
    _attach_test_specialist(ws, sp)

    actor = next(iter(ws.actors.values()))
    actor.emit_claim("watched")
    actor.emit_action("ignored", parameters={})

    # Only the claim was admitted by the activation-scope gate.
    assert len(sp.observed) == 1
    assert sp.observed[0]["payload-subtype"] == "claim"


def test_activation_scope_grammar_violation_at_attach_time(workspace) -> None:
    """D55 §B.1 — malformed activation-scope raises WorkspaceBootError(category=
    "activation-scope-grammar") at attach_workspace time.
    """
    ws = workspace
    spec = {
        "id": "test-bad-scope-specialist",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
        # Top-level admits only {"when": {...}}; this is malformed.
        "activation-scope": {"unknown-op": "x"},
    }
    sp = _RecordingSpecialist(spec=spec)

    with pytest.raises(WorkspaceBootError) as exc_info:
        sp.attach_workspace(ws)
    failures = exc_info.value.failures
    assert len(failures) == 1
    assert failures[0].category == "activation-scope-grammar"
