"""Tests for the append-only event chain (D10 + D23)."""
from __future__ import annotations

import pytest

from fresh_plan.runtime.event_chain import (
    AppendOnlyEventChain,
    MalformedEventError,
)
from fresh_plan.validator.schemas import load_schemas


@pytest.fixture
def schema_store(schemas_dir):
    return load_schemas(schemas_dir)


def _make_event(
    eid: str,
    prev: str | None,
    subtype: str = "action",
    payload: dict | None = None,
    actor_id: str = "actor-1",
    work_unit_id: str | None = None,
) -> dict:
    e = {
        "id": eid,
        "prev-event": prev,
        "timestamp": "2026-05-11T00:00:00Z",
        "actors": [{"id": actor_id}],
        "payload-subtype": subtype,
        "payload": payload or {"action-name": "noop"},
    }
    if work_unit_id is not None:
        e["work-unit-id"] = work_unit_id
    return e


def test_first_event_requires_prev_null(schema_store):
    chain = AppendOnlyEventChain()
    seq = chain.append(_make_event("evt-1", None), schema_store)
    assert seq == 0
    assert len(chain) == 1


def test_first_event_with_non_null_prev_rejected(schema_store):
    chain = AppendOnlyEventChain()
    with pytest.raises(MalformedEventError) as exc_info:
        chain.append(_make_event("evt-1", "evt-0"), schema_store)
    assert any(f.path == "event.prev-event" for f in exc_info.value.failures)
    assert len(chain) == 0


def test_sequential_appends_assign_monotonic_seq(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None), schema_store)
    chain.append(_make_event("evt-2", "evt-1"), schema_store)
    chain.append(_make_event("evt-3", "evt-2"), schema_store)
    assert [chain.sequence_of(f"evt-{i}") for i in (1, 2, 3)] == [0, 1, 2]


def test_prev_event_mismatch_rejected(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None), schema_store)
    with pytest.raises(MalformedEventError):
        # prev-event references evt-0 but tail is evt-1
        chain.append(_make_event("evt-2", "evt-0"), schema_store)
    assert len(chain) == 1
    assert chain.tail["id"] == "evt-1"


def test_duplicate_event_id_rejected(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None), schema_store)
    with pytest.raises(MalformedEventError) as exc_info:
        chain.append(_make_event("evt-1", "evt-1"), schema_store)
    assert any(f.path == "event.id" for f in exc_info.value.failures)


def test_schema_validation_rejects_malformed_payload(schema_store):
    """Per D10/D34 §A.8: payload validated by per-subtype schema."""
    chain = AppendOnlyEventChain()
    bad = _make_event("evt-1", None, subtype="claim", payload={})  # missing assertion
    with pytest.raises(MalformedEventError) as exc_info:
        chain.append(bad, schema_store)
    assert any(f.category == "schema" for f in exc_info.value.failures)


def test_query_by_id(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None), schema_store)
    chain.append(_make_event("evt-2", "evt-1"), schema_store)
    assert chain.by_id("evt-2")["id"] == "evt-2"
    assert chain.by_id("evt-nope") is None


def test_query_by_actor(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None, actor_id="alice"), schema_store)
    chain.append(_make_event("evt-2", "evt-1", actor_id="bob"), schema_store)
    chain.append(_make_event("evt-3", "evt-2", actor_id="alice"), schema_store)
    alice = chain.by_actor("alice")
    assert [e["id"] for e in alice] == ["evt-1", "evt-3"]


def test_query_by_work_unit(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None, work_unit_id="wu-a"), schema_store)
    chain.append(_make_event("evt-2", "evt-1"), schema_store)
    chain.append(_make_event("evt-3", "evt-2", work_unit_id="wu-a"), schema_store)
    assert [e["id"] for e in chain.by_work_unit("wu-a")] == ["evt-1", "evt-3"]


def test_query_by_payload_subtype(schema_store):
    chain = AppendOnlyEventChain()
    chain.append(_make_event("evt-1", None, subtype="action"), schema_store)
    chain.append(
        _make_event(
            "evt-2",
            "evt-1",
            subtype="claim",
            payload={"assertion": "x"},
        ),
        schema_store,
    )
    chain.append(_make_event("evt-3", "evt-2", subtype="action"), schema_store)
    actions = chain.by_payload_subtype("action")
    assert {e["id"] for e in actions} == {"evt-1", "evt-3"}


def test_tail_and_iteration(schema_store):
    chain = AppendOnlyEventChain()
    assert chain.tail is None
    chain.append(_make_event("evt-1", None), schema_store)
    chain.append(_make_event("evt-2", "evt-1"), schema_store)
    assert chain.tail["id"] == "evt-2"
    assert [e["id"] for e in chain] == ["evt-1", "evt-2"]
