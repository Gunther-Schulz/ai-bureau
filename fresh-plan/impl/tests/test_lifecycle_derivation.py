"""Tests for D58 §B.1 — work-unit.lifecycle.started-at / completed-at derivation
+ boot-time reconciliation against chain.

Per D58 §C: 2 tests covering the two surfaces:

  Test 1 — chain-derives-started-at: a work-unit-status transition event
           writes its `at` field into the work-unit's lifecycle.started-at;
           replay reproduces the same timestamp (idempotent guard).
  Test 2 — mismatch-rejected-at-boot: manifest declares a lifecycle.completed-at
           with no matching transition event in chain → reconciliation
           produces ValidationFailure(category="lifecycle-derivation-mismatch").
"""
from __future__ import annotations

from fresh_plan.runtime.event_chain import AppendOnlyEventChain, apply_event_to_state
from fresh_plan.runtime.workspace_state import WorkspaceState
from fresh_plan.validator.workspace import check_work_unit_lifecycle_derivation


def test_chain_derives_lifecycle_started_at_via_projection() -> None:
    """D58 §B.1 — work-unit-status transition to "in-progress" writes event.at
    into work-unit's lifecycle.started-at; idempotent on replay.
    """
    state = WorkspaceState()
    # Seed an actor (events need ≥1 actor).
    state.add_actor({"id": "agent-1", "subtype": "agent-actor"})
    # Seed a work-unit in `created` status.
    state.add_work_unit(
        {
            "id": "wu-1",
            "kind": "core:task",
            "status": "created",
            "lifecycle": {"created-at": "2026-05-17T09:00:00Z"},
        }
    )

    # Apply a status-transition event projecting `at` into lifecycle.started-at.
    transition_event = {
        "id": "evt-transition-1",
        "actors": [{"id": "agent-1"}],
        "work-unit-id": "wu-1",
        "payload-subtype": "state-change",
        "payload": {"what": "work-unit-status", "after": "in-progress"},
        "at": "2026-05-17T10:30:00Z",
    }
    apply_event_to_state(transition_event, state)

    record = state.work_units["wu-1"]
    assert record["status"] == "in-progress"
    assert record["lifecycle"]["started-at"] == "2026-05-17T10:30:00Z"

    # Replay (idempotent) — applying again should NOT overwrite.
    second_event = dict(transition_event)
    second_event["at"] = "2026-05-17T99:99:99Z"  # different timestamp
    apply_event_to_state(second_event, state)
    assert (
        record["lifecycle"]["started-at"] == "2026-05-17T10:30:00Z"
    ), "lifecycle.started-at must be idempotent (only-write-if-unset)"


def test_manifest_declared_lifecycle_mismatch_surfaces_failure() -> None:
    """D58 §B.1 — manifest declares lifecycle.completed-at with no matching
    transition event → ValidationFailure(category="lifecycle-derivation-mismatch").
    """
    # Manifest declares a work-unit completed at a timestamp; chain has no
    # transition event into completed → derived state has no completed-at.
    manifest = {
        "id": "test-ws",
        "composition": {},
        "work-units": [
            {
                "id": "wu-1",
                "kind": "core:task",
                "lifecycle": {"completed-at": "2026-05-17T10:00:00Z"},
            }
        ],
    }
    # Empty chain (no transitions).
    chain = AppendOnlyEventChain()
    failures = check_work_unit_lifecycle_derivation(manifest, event_chain=chain)
    assert len(failures) == 1
    failure = failures[0]
    assert failure.category == "lifecycle-derivation-mismatch"
    assert "wu-1" in failure.path
    assert "completed-at" in failure.path
