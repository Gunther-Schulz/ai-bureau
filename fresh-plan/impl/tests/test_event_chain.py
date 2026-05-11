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


# -------------- state_at(n) per D40 §A minimum query interface --------------


def _comp_change_add_actor(eid, prev, actor_id, record, attributing="actor-1"):
    return {
        "id": eid,
        "prev-event": prev,
        "timestamp": "2026-05-11T00:00:00Z",
        "actors": [{"id": attributing}],
        "payload-subtype": "composition-change",
        "payload": {
            "change-type": "add",
            "binding-reference": actor_id,
            "binding-kind": "actor",
            "record": record,
        },
    }


def _state_change_scope(eid, prev, after, actor_id="actor-1"):
    return {
        "id": eid,
        "prev-event": prev,
        "timestamp": "2026-05-11T00:00:00Z",
        "actors": [{"id": actor_id}],
        "payload-subtype": "state-change",
        "payload": {"what": "scope", "after": after},
    }


def test_state_at_empty_chain(schema_store):
    chain = AppendOnlyEventChain()
    state = chain.state_at(0)
    assert state.actors == {}
    assert state.current_scope is None


def test_state_at_negative_returns_empty(schema_store):
    chain = AppendOnlyEventChain()
    record = {"id": "sub-1", "subtype": "agent-actor", "substrate-binding": "primary"}
    chain.append(_comp_change_add_actor("evt-1", None, "sub-1", record), schema_store)
    assert chain.state_at(-1).actors == {}


def test_state_at_replays_composition_change_actor_add(schema_store):
    """Per D39 + D40 §A: state_at replays composition-change:add events using
    the D39 `record` slot."""
    chain = AppendOnlyEventChain()
    record_a = {"id": "sub-a", "subtype": "agent-actor", "substrate-binding": "primary"}
    record_b = {"id": "sub-b", "subtype": "agent-actor", "substrate-binding": "primary"}
    chain.append(_comp_change_add_actor("evt-1", None, "sub-a", record_a), schema_store)
    chain.append(
        _comp_change_add_actor("evt-2", "evt-1", "sub-b", record_b),
        schema_store,
    )
    state = chain.state_at(1)
    assert state.has_actor("sub-a")
    assert state.has_actor("sub-b")
    assert state.get_actor("sub-a")["substrate-binding"] == "primary"


def test_state_at_n_bounds_replay(schema_store):
    """state_at(n) reflects only events 0..n; later events are not included."""
    chain = AppendOnlyEventChain()
    record_a = {"id": "sub-a", "subtype": "agent-actor", "substrate-binding": "primary"}
    record_b = {"id": "sub-b", "subtype": "agent-actor", "substrate-binding": "primary"}
    chain.append(_comp_change_add_actor("evt-1", None, "sub-a", record_a), schema_store)
    chain.append(
        _comp_change_add_actor("evt-2", "evt-1", "sub-b", record_b),
        schema_store,
    )
    state_after_first = chain.state_at(0)
    assert state_after_first.has_actor("sub-a")
    assert not state_after_first.has_actor("sub-b")


def test_state_at_replays_scope_change(schema_store):
    chain = AppendOnlyEventChain()
    record_a = {"id": "sub-a", "subtype": "agent-actor", "substrate-binding": "primary"}
    chain.append(_comp_change_add_actor("evt-1", None, "sub-a", record_a), schema_store)
    chain.append(
        _state_change_scope(
            "evt-2", "evt-1", {"focus": "section-3"}, actor_id="sub-a"
        ),
        schema_store,
    )
    chain.append(
        _state_change_scope(
            "evt-3", "evt-2", {"focus": "section-4"}, actor_id="sub-a"
        ),
        schema_store,
    )
    # At sequence 1: scope = section-3 (first scope event)
    assert chain.state_at(1).current_scope == {"focus": "section-3"}
    # At tail: scope = section-4 (latest scope event)
    assert chain.state_at(2).current_scope == {"focus": "section-4"}


def test_state_at_clamps_beyond_tail(schema_store):
    chain = AppendOnlyEventChain()
    record_a = {"id": "sub-a", "subtype": "agent-actor", "substrate-binding": "primary"}
    chain.append(_comp_change_add_actor("evt-1", None, "sub-a", record_a), schema_store)
    # n past tail: clamp to tail
    state = chain.state_at(99)
    assert state.has_actor("sub-a")


def test_state_at_returns_fresh_state_each_call(schema_store):
    """state_at returns a fresh WorkspaceState; mutating it must not
    affect the chain or subsequent calls."""
    chain = AppendOnlyEventChain()
    record_a = {"id": "sub-a", "subtype": "agent-actor", "substrate-binding": "primary"}
    chain.append(_comp_change_add_actor("evt-1", None, "sub-a", record_a), schema_store)
    first = chain.state_at(0)
    first.actors.clear()
    second = chain.state_at(0)
    assert second.has_actor("sub-a")  # second call not poisoned by first's mutation
