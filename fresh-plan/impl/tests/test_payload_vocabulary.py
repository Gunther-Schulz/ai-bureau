"""Tests for D59 §B.1 — payload-vocabulary registration + per-event validation.

Per D59 §C: 2 tests covering the contract:

  Test 1 — registered value accepted: per-event check passes when value
           is in registered_payload_vocabulary table.
  Test 2 — unregistered value rejected: per-event check returns
           ValidationFailure(category="vocabulary") when slot table has
           registrations but the value isn't among them.

D59 enforces opt-in: per-slot tables that are EMPTY leave the slot
unconstrained (pre-D59 behavior preserved). Once an extension registers
ANY value for a slot, all values for that slot become subject to
closed-vocabulary enforcement.
"""
from __future__ import annotations

from fresh_plan.runtime.per_event_checks import check_event_references
from fresh_plan.runtime.workspace_state import WorkspaceState


def test_registered_payload_vocabulary_value_accepted() -> None:
    """D59 §B.1 — claim event with registered confidence value passes."""
    state = WorkspaceState()
    state.add_actor({"id": "agent-1", "subtype": "agent-actor"})

    event = {
        "id": "evt-1",
        "prev-event": None,
        "timestamp": "2026-05-17T00:00:00Z",
        "actors": [{"id": "agent-1"}],
        "payload-subtype": "claim",
        "payload": {
            "assertion": "x",
            "confidence": "core-ext:high",  # registered value
        },
    }
    registered = {"claim.confidence": {"core-ext:high", "core-ext:medium"}}
    failures = check_event_references(
        event,
        state,
        set(),  # registered_payload_subtypes (claim is core)
        set(),  # known_binding_ids
        registered_payload_vocabulary=registered,
    )
    assert failures == [], f"expected no failures; got {failures}"


def test_unregistered_payload_vocabulary_value_rejected() -> None:
    """D59 §B.1 — claim event with unregistered confidence value (where slot
    has at least one registration) surfaces as vocabulary failure.
    """
    state = WorkspaceState()
    state.add_actor({"id": "agent-1", "subtype": "agent-actor"})

    event = {
        "id": "evt-2",
        "prev-event": None,
        "timestamp": "2026-05-17T00:00:00Z",
        "actors": [{"id": "agent-1"}],
        "payload-subtype": "claim",
        "payload": {
            "assertion": "x",
            "confidence": "unknown-grade",  # NOT in registered table
        },
    }
    registered = {"claim.confidence": {"core-ext:high", "core-ext:medium"}}
    failures = check_event_references(
        event,
        state,
        set(),
        set(),
        registered_payload_vocabulary=registered,
    )
    vocab_failures = [f for f in failures if f.category == "vocabulary"]
    assert len(vocab_failures) == 1
    assert vocab_failures[0].path == "event.payload.confidence"
    assert vocab_failures[0].value == "unknown-grade"
