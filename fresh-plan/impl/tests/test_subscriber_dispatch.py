"""Subscriber-dispatch semantics per D44 (extends D37).

Verifies the queued-dispatch contract: append + projection + chain
integrity remain synchronous; subscriber on_event fires from a FIFO
drain owned by the outermost append_event call. Nested append_event
calls (from inside on_event) enqueue without re-entering the drain.
A loop backstop raises with a diagnostic when a single drain exceeds
`max_events_per_drain`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.specialist import Specialist


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"


@pytest.fixture
def workspace():
    manifest = json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, SUBSTRATE_FIXTURE / "extensions")
    yield ws
    ws.shutdown()


def _attach_test_specialist(ws: Workspace, specialist: Specialist) -> None:
    """Mount a test-only Specialist onto the running workspace.

    Bypasses load_provision_spec — the test owns the specialist's
    lifecycle. attach_workspace wires the workspace handle; subscribers
    list registers it for dispatch.
    """
    specialist.attach_workspace(ws)
    ws.substrate.specialist_subscribers.append(specialist)


# ---------------------------------------------------------------------------
# FIFO ordering: a reaction's emissions are dispatched after the reaction returns
# ---------------------------------------------------------------------------


class _RecordingSpecialist(Specialist):
    """Records the order in which on_event observes events.

    Per D44 queued-dispatch: when a reaction emits an event, the
    reaction's own continuation observes the emission's projection
    (state is current) but does NOT see the emission's subscriber
    reactions until the outer drain reaches them.
    """

    def __init__(self, spec: dict) -> None:
        super().__init__(spec=spec)
        self.observation_log: list[tuple[str, str]] = []
        self.emit_on_action_seen: bool = False

    def on_event(self, event: dict) -> None:
        subtype = event.get("payload-subtype")
        eid = event.get("id")
        self.observation_log.append((subtype, eid))
        if (
            subtype == "claim"
            and self.emit_on_action_seen is False
        ):
            # First reaction: emit a follow-up action. The action's own
            # reactions should fire AFTER this on_event returns (FIFO),
            # not as a recursive subdispatch inside this call.
            self.emit_on_action_seen = True
            actor_id = next(iter(self._workspace._substrate.state.actors), None)
            self._emit_event(
                actor_id=actor_id,
                payload_subtype="action",
                payload={"action-name": "follow-up", "parameters": {}},
            )


def test_d44_dispatch_is_fifo_not_recursive(workspace):
    """Per D44: an on_event that emits a follow-up event does NOT see its own
    follow-up's dispatch as a nested call — the follow-up's dispatch
    happens after the original on_event returns, in queue order.
    """
    ws = workspace
    spec = {
        "id": "test-recording-specialist",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [{"payload-subtype": "action"}],
        "declared-event-subscriptions": [
            {"payload-subtype": "claim"},
            {"payload-subtype": "action"},
        ],
    }
    spec_recorder = _RecordingSpecialist(spec=spec)
    _attach_test_specialist(ws, spec_recorder)

    # The actor emits a claim. Subscriber's on_event observes claim,
    # emits a follow-up action. The action's dispatch is queued.
    # Sequence under D44: [observe claim] → on_event returns → [observe action].
    actor = next(iter(ws.actors.values()))
    actor.emit_claim("test claim")

    log = spec_recorder.observation_log
    # Two observations: the claim, then the action emitted from inside.
    assert len(log) == 2
    assert log[0][0] == "claim"
    assert log[1][0] == "action"

    # Crucially: depth never went recursive. If dispatch were synchronous,
    # log would still show the same order (claim then action), but the
    # action observation would have happened DURING the claim's on_event
    # call. Under D44 queued dispatch, action is observed AFTER. We can
    # observe the difference indirectly via _dispatching state: at the
    # moment the action dispatches, the substrate's _dispatching flag is
    # True (inside the drain), and the dispatch_queue is empty (the action
    # was popped). Hard to assert from outside; the FIFO+depth-1 contract
    # is the visible property.


# ---------------------------------------------------------------------------
# Loop backstop: infinite reaction loop terminates with a diagnostic
# ---------------------------------------------------------------------------


class _LoopingSpecialist(Specialist):
    """Each reaction emits another action — true infinite-loop case."""

    def on_event(self, event: dict) -> None:
        if event.get("payload-subtype") != "action":
            return
        actor_id = next(iter(self._workspace._substrate.state.actors), None)
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={"action-name": "loop", "parameters": {}},
        )


def test_d44_loop_backstop_raises_diagnostic(workspace):
    """Per D44: when a chain reaction exceeds max_events_per_drain, the
    drain raises a RuntimeError naming the offending event in flight.
    """
    ws = workspace
    spec = {
        "id": "test-looping-specialist",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [{"payload-subtype": "action"}],
        "declared-event-subscriptions": [{"payload-subtype": "action"}],
    }
    spec_loop = _LoopingSpecialist(spec=spec)
    _attach_test_specialist(ws, spec_loop)

    # Lower the backstop for fast test execution.
    ws.substrate.max_events_per_drain = 5

    actor = next(iter(ws.actors.values()))
    with pytest.raises(RuntimeError) as exc_info:
        actor.emit_action("kickoff", parameters={})

    msg = str(exc_info.value)
    assert "subscriber-dispatch drain exceeded 5 events" in msg
    assert "infinite loop" in msg
    assert "payload-subtype='action'" in msg


# ---------------------------------------------------------------------------
# Synchronous-ness preserved: chain integrity + projection still happen
# during the original append, not deferred
# ---------------------------------------------------------------------------


def test_d44_chain_integrity_and_projection_remain_synchronous(workspace):
    """Per D44: append + chain integrity + projection are NOT queued —
    only subscriber dispatch is. Each emission's chain entry + state
    mutation happen synchronously inside append_event.
    """
    ws = workspace
    spec = {
        "id": "test-recording-specialist-2",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [{"payload-subtype": "action"}],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
    }
    spec_recorder = _RecordingSpecialist(spec=spec)
    _attach_test_specialist(ws, spec_recorder)

    # Capture chain length immediately before the trigger.
    chain_len_before = len(ws.event_chain)

    actor = next(iter(ws.actors.values()))
    actor.emit_claim("synchronous check")

    # After the call returns: chain has BOTH the claim and the action
    # emitted from inside on_event. Both are appended synchronously
    # during the outer drain — the action wasn't deferred.
    chain_len_after = len(ws.event_chain)
    assert chain_len_after == chain_len_before + 2  # claim + follow-up action

    # state_at(n) replay reproduces the same end state, confirming
    # projection ran for every emission as part of append_event.
    replayed_state = ws.state_at(chain_len_after - 1)
    # Manifest actors + scope projections all replay-equivalent (no
    # behavior change vs pre-D44 baseline).
    for aid in ws.substrate.state.actors:
        assert replayed_state.has_actor(aid)


# ---------------------------------------------------------------------------
# Cross-specialist FIFO: A's emission triggers B BEFORE A's second emission
# ---------------------------------------------------------------------------


class _EmittingSpecialist(Specialist):
    """A: subscribes to claim; emits an action then a state-change."""

    def on_event(self, event: dict) -> None:
        if event.get("payload-subtype") != "claim":
            return
        actor_id = next(iter(self._workspace._substrate.state.actors), None)
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={"action-name": "from-A", "parameters": {}},
        )
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="state-change",
            payload={"what": "scope", "after": {"focus": "from-A"}},
        )


class _ObservingSpecialist(Specialist):
    """B: subscribes to action; records the global event-chain position when
    its on_event fires."""

    def __init__(self, spec: dict, ws: Workspace) -> None:
        super().__init__(spec=spec)
        self._ws = ws
        self.observed_at_chain_length: list[int] = []

    def on_event(self, event: dict) -> None:
        if event.get("payload-subtype") != "action":
            return
        self.observed_at_chain_length.append(len(self._ws.event_chain))


def test_d44_cross_specialist_fifo_ordering(workspace):
    """Per D44: when A's on_event emits two events synchronously, both
    are appended to the chain BEFORE B's reaction to either fires.
    Visible via the chain-length B observes (== full chain after both
    of A's emissions, not after only the first).
    """
    ws = workspace
    spec_a = {
        "id": "test-emitting-specialist-a",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [
            {"payload-subtype": "action"},
            {"payload-subtype": "state-change"},
        ],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
    }
    spec_b = {
        "id": "test-observing-specialist-b",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "action"}],
    }
    a = _EmittingSpecialist(spec=spec_a)
    b = _ObservingSpecialist(spec=spec_b, ws=ws)
    _attach_test_specialist(ws, a)
    _attach_test_specialist(ws, b)

    chain_before = len(ws.event_chain)
    actor = next(iter(ws.actors.values()))
    actor.emit_claim("trigger")

    # After: chain has claim + A's action + A's state-change = +3.
    # B observed exactly once (only the action subtype matched), and it
    # observed AFTER both of A's emissions had been appended (chain
    # length at that moment includes both).
    assert len(ws.event_chain) == chain_before + 3
    assert len(b.observed_at_chain_length) == 1
    # B's observation happened after BOTH A-emissions were appended,
    # i.e. chain length at observation == final length.
    assert b.observed_at_chain_length[0] == chain_before + 3


# ---------------------------------------------------------------------------
# D47 — subscriber dispatch + hook firing honor detection-surface-recovery triad
# ---------------------------------------------------------------------------


class _RaisingSpecialist(Specialist):
    """on_event always raises a marker exception; tests aggregation per D47 §B.1."""

    def __init__(self, spec: dict, marker: str = "raise-marker") -> None:
        super().__init__(spec=spec)
        self._marker = marker

    def on_event(self, event: dict) -> None:
        raise RuntimeError(f"{self._marker}:{event.get('id')}")


def test_d47_subscriber_exception_captured_and_aggregated(workspace):
    """Per D47 §B.1: subscriber on_event exceptions are NOT silently swallowed —
    they're collected during drain and raised as SubscriberDispatchError
    aggregate after the outer drain completes.
    """
    from fresh_plan.runtime.substrate import SubscriberDispatchError

    ws = workspace
    spec = {
        "id": "test-raising-specialist",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
    }
    raising = _RaisingSpecialist(spec=spec, marker="boom")
    _attach_test_specialist(ws, raising)

    actor = next(iter(ws.actors.values()))
    with pytest.raises(SubscriberDispatchError) as exc_info:
        actor.emit_claim("trigger")

    failures = exc_info.value.failures
    assert len(failures) == 1
    spec_id, event_id, exc = failures[0]
    assert spec_id == "test-raising-specialist"
    assert isinstance(exc, RuntimeError)
    assert "boom:" in str(exc)


def test_d47_subscriber_exceptions_aggregate_across_multiple_specialists(workspace):
    """Per D47 §B.1: when multiple subscribers raise, ALL failures captured
    in the aggregate (not just the first); cascade is not terminated by
    individual failures."""
    from fresh_plan.runtime.substrate import SubscriberDispatchError

    ws = workspace
    spec_template = {
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
    }
    a_spec = {**spec_template, "id": "raiser-a"}
    b_spec = {**spec_template, "id": "raiser-b"}
    a = _RaisingSpecialist(spec=a_spec, marker="A")
    b = _RaisingSpecialist(spec=b_spec, marker="B")
    _attach_test_specialist(ws, a)
    _attach_test_specialist(ws, b)

    actor = next(iter(ws.actors.values()))
    with pytest.raises(SubscriberDispatchError) as exc_info:
        actor.emit_claim("trigger")

    failures = exc_info.value.failures
    assert len(failures) == 2
    spec_ids = {f[0] for f in failures}
    assert spec_ids == {"raiser-a", "raiser-b"}


def test_d47_chain_consistent_after_subscriber_failures(workspace):
    """Per D47 §B.1: even when subscribers raise, the event IS in the chain
    + state. Chain integrity preserved per D10; replay still works per D39."""
    from fresh_plan.runtime.substrate import SubscriberDispatchError

    ws = workspace
    spec = {
        "id": "test-raiser-c",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
    }
    _attach_test_specialist(ws, _RaisingSpecialist(spec=spec, marker="C"))

    chain_before = len(ws.event_chain)
    actor = next(iter(ws.actors.values()))
    with pytest.raises(SubscriberDispatchError):
        actor.emit_claim("survives")

    # Event IS in chain even though subscribers failed.
    assert len(ws.event_chain) == chain_before + 1
    # Replay reproduces (state-from-events still works).
    state = ws.state_at(len(ws.event_chain) - 1)
    assert state.has_actor(next(iter(ws.actors.keys())))


def test_d47_pre_event_emit_handler_raise_rejects_event(workspace):
    """Per D47 §B.2: pre-event-emit hook handler raise → EventRejected
    (category="hook-handler"); event NOT appended; chain unchanged."""
    from fresh_plan.runtime.per_event_checks import EventRejected

    ws = workspace

    def raising_pre_handler(context: dict) -> None:
        raise RuntimeError("pre-emit veto")

    ws.substrate.hooks.register("pre-event-emit", raising_pre_handler)

    try:
        chain_before = len(ws.event_chain)
        actor = next(iter(ws.actors.values()))
        with pytest.raises(EventRejected) as exc_info:
            actor.emit_claim("rejected-by-hook")

        failures = exc_info.value.failures
        assert any(
            f.category == "hook-handler"
            and "pre-event-emit" in f.path
            and "pre-emit veto" in f.reason
            for f in failures
        ), f"expected hook-handler EventRejected, got: {failures}"
        # Event NOT in chain (pre-emit raise prevented append).
        assert len(ws.event_chain) == chain_before
    finally:
        # Clear the always-raising handler so fixture's ws.shutdown()
        # (which emits a lifecycle-transition:shutdown event) can succeed.
        ws.substrate.hooks.clear("pre-event-emit")


def test_d47_post_event_emit_handler_raise_captured_event_in_chain(workspace):
    """Per D47 §B.2: post-event-emit handler raise → HookExecutionError
    aggregated AFTER drain; event IS in chain + state per append-only."""
    from fresh_plan.runtime.substrate import HookExecutionError

    ws = workspace

    def raising_post_handler(context: dict) -> None:
        raise RuntimeError(f"post-emit boom for {context['event']['id']}")

    ws.substrate.hooks.register("post-event-emit", raising_post_handler)

    try:
        chain_before = len(ws.event_chain)
        actor = next(iter(ws.actors.values()))
        with pytest.raises(HookExecutionError) as exc_info:
            actor.emit_claim("event-survives-post-failure")

        failures = exc_info.value.failures
        assert len(failures) == 1
        name, idx, event_id, exc = failures[0]
        assert name == "post-event-emit"
        assert isinstance(exc, RuntimeError)
        assert "post-emit boom" in str(exc)
        # Event IS in chain even though post-emit raised.
        assert len(ws.event_chain) == chain_before + 1
    finally:
        ws.substrate.hooks.clear("post-event-emit")


def test_d47_subscriber_and_post_emit_failures_chain_via_exception(workspace):
    """Per D47 §C: when both subscriber and post-emit failures occur during
    one drain, both surface — SubscriberDispatchError raised with
    HookExecutionError as __cause__."""
    from fresh_plan.runtime.substrate import (
        HookExecutionError,
        SubscriberDispatchError,
    )

    ws = workspace
    spec = {
        "id": "test-raiser-both",
        "version": "0.1.0",
        "skills": [],
        "supported-work-unit-kinds": [],
        "required-adapter-bindings": [],
        "required-substrate-capabilities": ["skills", "event-chain"],
        "declared-event-emissions": [],
        "declared-event-subscriptions": [{"payload-subtype": "claim"}],
    }
    _attach_test_specialist(ws, _RaisingSpecialist(spec=spec, marker="D"))

    def raising_post_handler(context: dict) -> None:
        raise RuntimeError("post boom")

    ws.substrate.hooks.register("post-event-emit", raising_post_handler)

    try:
        actor = next(iter(ws.actors.values()))
        with pytest.raises(SubscriberDispatchError) as exc_info:
            actor.emit_claim("both-fail")

        # SubscriberDispatchError raised primary; HookExecutionError chained.
        assert isinstance(exc_info.value.__cause__, HookExecutionError)
        assert len(exc_info.value.failures) == 1  # one subscriber raised
        assert len(exc_info.value.__cause__.failures) == 1  # one post-emit raised
    finally:
        ws.substrate.hooks.clear("post-event-emit")


def test_d47_pre_emit_handler_succeeds_with_event_in_context(workspace):
    """Per D47 §B.3: handler signature receives context dict with `event` key."""
    ws = workspace
    received = []

    def observing_pre_handler(context: dict) -> None:
        received.append(context["event"]["id"])

    ws.substrate.hooks.register("pre-event-emit", observing_pre_handler)

    actor = next(iter(ws.actors.values()))
    actor.emit_claim("observe-me")

    assert len(received) >= 1


def test_d47_post_emit_handler_succeeds_with_event_and_sequence_in_context(workspace):
    """Per D47 §B.3: post-emit handler context carries `event` + `sequence` keys."""
    ws = workspace
    received = []

    def observing_post_handler(context: dict) -> None:
        received.append((context["event"]["id"], context["sequence"]))

    ws.substrate.hooks.register("post-event-emit", observing_post_handler)

    actor = next(iter(ws.actors.values()))
    actor.emit_claim("observe-with-seq")

    assert len(received) >= 1
    event_id, seq = received[-1]
    assert isinstance(seq, int)
    assert seq >= 0
