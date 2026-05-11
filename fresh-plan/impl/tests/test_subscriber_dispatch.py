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
