"""Tests for Phase C C9 standards-compatibility export converters (D77 §B).

Pure-converter coverage for ``fresh_plan.runtime.standards_export``:

  1. ``to_cloudevents`` happy-path: fresh-plan event → CloudEvent with
     id / source / type / data / specversion / datacontenttype.
  2. ``to_cloudevents`` malformed event → ValueError (detection per
     D77 §B.2).
  3. ``event_chain_to_prov_json`` happy-path: 3-event chain → PROV-JSON
     with 3 Activities + N Agents + attribution links.
  4. ``event_chain_to_prov_json`` empty chain → PROV-JSON with 0
     Activities but workspace Agent present (no failure).
  5. ``event_chain_to_prov_json`` malformed event → ValueError.
  6. ``write_prov_json`` writes JSON to disk + returns the same dict
     (round-trip via reread).

Per D77 §A NON-BREAKING contract: these converters do not mutate the
fresh-plan event envelope; they emit a separate standards-shape view.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime.standards_export import (
    PROV_NAMESPACE,
    event_chain_to_prov_json,
    to_cloudevents,
    write_prov_json,
)


# ---------------------------------------------------------------------------
# Sample fresh-plan events (schemas/event.schema.json compliant)
# ---------------------------------------------------------------------------


def _sample_claim_event(
    event_id: str = "evt-001",
    actor_id: str = "actor-curator",
    timestamp: str = "2026-05-17T10:00:00+00:00",
) -> dict:
    return {
        "id": event_id,
        "prev-event": None,
        "timestamp": timestamp,
        "actors": [{"id": actor_id, "role": "drafter"}],
        "payload-subtype": "claim",
        "payload": {
            "claim-id": f"claim-{event_id}",
            "content": {"text": "hello world"},
        },
    }


def _sample_action_event(
    event_id: str = "evt-002",
    actor_id: str = "actor-reviewer",
    timestamp: str = "2026-05-17T10:05:00+00:00",
    prev: str = "evt-001",
) -> dict:
    return {
        "id": event_id,
        "prev-event": prev,
        "timestamp": timestamp,
        "actors": [{"id": actor_id, "role": "actor"}],
        "payload-subtype": "action",
        "payload": {
            "action-name": "review",
            "parameters": {"target": "claim-evt-001"},
            "outcome-reference": "stub-1",
        },
    }


# ---------------------------------------------------------------------------
# 1 — to_cloudevents happy-path
# ---------------------------------------------------------------------------


def test_to_cloudevents_maps_required_attributes():
    """D77 §B.1: fresh-plan event → CloudEvent with mapped attributes.

    Per CNCF CloudEvents 1.0 spec required attributes (id / source /
    specversion / type) + recommended (datacontenttype / time) +
    payload-as-data.
    """
    event = _sample_claim_event()
    ce = to_cloudevents(event, workspace_id="test-ws")

    assert ce["id"] == "evt-001"
    assert ce["source"] == "workspace://test-ws"
    assert ce["type"] == "claim"
    assert ce["specversion"] == "1.0"
    assert ce["datacontenttype"] == "application/json"
    assert ce["time"] == "2026-05-17T10:00:00+00:00"
    # Data carries the original payload (NON-BREAKING — no envelope rewrite).
    assert ce.data == {
        "claim-id": "claim-evt-001",
        "content": {"text": "hello world"},
    }


def test_to_cloudevents_default_source_when_workspace_id_omitted():
    """D77 §B.1: workspace_id omitted → source falls back to
    ``workspace://unknown`` (CloudEvents source is REQUIRED per spec)."""
    event = _sample_claim_event()
    ce = to_cloudevents(event)
    assert ce["source"] == "workspace://unknown"


# ---------------------------------------------------------------------------
# 2 — to_cloudevents detection (D77 §B.2)
# ---------------------------------------------------------------------------


def test_to_cloudevents_raises_value_error_on_missing_required_field():
    """D77 §B.2 Detection: malformed event missing required envelope
    field → ValueError (no silent substitution)."""
    bad_event = {
        # missing "id"
        "timestamp": "2026-05-17T10:00:00+00:00",
        "actors": [{"id": "a"}],
        "payload-subtype": "claim",
        "payload": {},
    }
    with pytest.raises(ValueError) as exc_info:
        to_cloudevents(bad_event)
    msg = str(exc_info.value)
    assert "missing required" in msg
    assert "id" in msg


def test_to_cloudevents_raises_on_empty_actors():
    """D77 §B.2: actors must be a non-empty list per D10 schema."""
    bad_event = {
        "id": "evt-x",
        "timestamp": "2026-05-17T10:00:00+00:00",
        "actors": [],
        "payload-subtype": "claim",
        "payload": {},
    }
    with pytest.raises(ValueError):
        to_cloudevents(bad_event)


# ---------------------------------------------------------------------------
# 3 — event_chain_to_prov_json happy-path
# ---------------------------------------------------------------------------


def test_event_chain_to_prov_json_3_events_produces_3_activities():
    """D77 §B.1: 3 fresh-plan events → 3 prov:Activity entries +
    de-duplicated prov:Agent entries + (actor, event) wasAttributedTo."""
    events = [
        _sample_claim_event(
            event_id="evt-1",
            actor_id="actor-A",
            timestamp="2026-05-17T10:00:00+00:00",
        ),
        _sample_action_event(
            event_id="evt-2",
            actor_id="actor-B",
            timestamp="2026-05-17T10:05:00+00:00",
            prev="evt-1",
        ),
        _sample_claim_event(
            event_id="evt-3",
            actor_id="actor-A",  # same as evt-1 → de-dup
            timestamp="2026-05-17T10:10:00+00:00",
        ),
    ]
    # evt-3 prev-event would normally point to evt-2 (chain integrity),
    # but the converter doesn't enforce chain linkage; per D77 the export
    # is one-way and chain integrity is upstream (event_chain.append).
    events[2]["prev-event"] = "evt-2"

    doc = event_chain_to_prov_json(events, workspace_id="ws-test")

    # Prefix block carries the prov namespace per W3C PROV-JSON spec.
    assert doc["prefix"]["prov"] == PROV_NAMESPACE
    assert "fresh-plan" in doc["prefix"]

    # 3 Activities (1 per event)
    activities = doc["activity"]
    assert len(activities) == 3
    assert "fresh-plan:event:evt-1" in activities
    assert "fresh-plan:event:evt-2" in activities
    assert "fresh-plan:event:evt-3" in activities
    # Activity carries prov:startTime + prov:type per D77 §B.1
    assert (
        activities["fresh-plan:event:evt-1"]["prov:startTime"]
        == "2026-05-17T10:00:00+00:00"
    )
    assert activities["fresh-plan:event:evt-1"]["prov:type"] == "claim"
    assert activities["fresh-plan:event:evt-2"]["prov:type"] == "action"

    # Agents: 2 unique actors (A, B) + 1 workspace agent.
    agents = doc["agent"]
    assert "fresh-plan:actor:actor-A" in agents
    assert "fresh-plan:actor:actor-B" in agents
    assert "fresh-plan:workspace:ws-test" in agents
    assert len(agents) == 3

    # Attributions: per (actor, event) + per (workspace, event).
    # actor-A attributes evt-1 + evt-3 (2 attrs)
    # actor-B attributes evt-2 (1 attr)
    # workspace attributes evt-1 + evt-2 + evt-3 (3 attrs)
    # Total: 6 attribution relations.
    attributions = doc["wasAttributedTo"]
    assert len(attributions) == 6

    # Verify a specific actor-A → evt-1 attribution exists with
    # canonical prov:activity + prov:agent shape.
    a_to_e1 = attributions["fresh-plan:attr:evt-1_actor-A"]
    assert a_to_e1["prov:activity"] == "fresh-plan:event:evt-1"
    assert a_to_e1["prov:agent"] == "fresh-plan:actor:actor-A"


# ---------------------------------------------------------------------------
# 4 — empty chain
# ---------------------------------------------------------------------------


def test_event_chain_to_prov_json_empty_chain_succeeds_with_workspace_agent():
    """D77 §B.1: empty event chain → 0 Activities, 0 actor-Agents,
    BUT the workspace Agent is anchored unconditionally per D77 design
    (the PROV-JSON document is still valid + carries workspace identity)."""
    doc = event_chain_to_prov_json([], workspace_id="ws-empty")
    assert doc["activity"] == {}
    assert doc["wasAttributedTo"] == {}
    # Workspace agent still anchored.
    assert "fresh-plan:workspace:ws-empty" in doc["agent"]
    assert len(doc["agent"]) == 1


def test_event_chain_to_prov_json_raises_on_empty_workspace_id():
    """Fail-closed: empty workspace_id raises ValueError per D77 §B.2."""
    with pytest.raises(ValueError):
        event_chain_to_prov_json([], workspace_id="")


# ---------------------------------------------------------------------------
# 5 — malformed event in chain
# ---------------------------------------------------------------------------


def test_event_chain_to_prov_json_raises_on_malformed_event():
    """D77 §B.2: a chain containing a malformed event → ValueError naming
    the offending position + missing field."""
    events = [
        _sample_claim_event(event_id="evt-good"),
        {"id": "evt-bad"},  # missing timestamp/payload-subtype/actors/payload
    ]
    with pytest.raises(ValueError) as exc_info:
        event_chain_to_prov_json(events, workspace_id="ws-test")
    msg = str(exc_info.value)
    assert "missing required" in msg
    assert "evt-bad" in msg


def test_event_chain_to_prov_json_raises_on_actor_missing_id():
    """D77 §B.2: actor entry without `id` field → ValueError."""
    events = [
        {
            "id": "evt-1",
            "prev-event": None,
            "timestamp": "2026-05-17T10:00:00+00:00",
            "actors": [{"role": "drafter"}],  # missing id
            "payload-subtype": "claim",
            "payload": {},
        }
    ]
    with pytest.raises(ValueError) as exc_info:
        event_chain_to_prov_json(events, workspace_id="ws-test")
    assert "actor without `id`" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 6 — write_prov_json IO round-trip
# ---------------------------------------------------------------------------


def test_write_prov_json_writes_file_and_returns_dict(tmp_path: Path):
    """D77 §B.1: write_prov_json persists JSON to disk + returns the
    same dict for caller introspection. Reread the file + assert
    structural equivalence."""
    events = [_sample_claim_event()]
    output = tmp_path / "prov.json"

    returned_doc = write_prov_json(events, "ws-test", output)
    assert output.exists()

    persisted_doc = json.loads(output.read_text())
    assert persisted_doc == returned_doc
    assert len(persisted_doc["activity"]) == 1
    assert "fresh-plan:workspace:ws-test" in persisted_doc["agent"]
