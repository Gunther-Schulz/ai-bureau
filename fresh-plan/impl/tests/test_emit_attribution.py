"""Tests for D64 — specialist emit-attribution mechanism.

Covers the three paths locked by D64 §B.1:

  1. Specialist emitting within its declared-event-emissions[] vocabulary
     → event.emitting-specialist == binding-id; appended to chain.
  2. Specialist emitting OUTSIDE its declared-event-emissions[] vocabulary
     → EventRejected(category="vocabulary"; path="event.emitting-specialist").
  3. Non-specialist emit path (ActorHandle.emit_claim) → no
     emitting-specialist slot; per-event emit-attribution check skipped;
     event in chain.

Per D64 §B.1 + D19 (declared-event-emissions[] is required-with-explicit-
empty) + A2 STRICT lock: empty list = zero allowed.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.specialist import GenericSpecialist
from fresh_plan.runtime.substrate import EventRejected


SPECIALIST_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-generic-specialist"
)


@pytest.fixture
def booted_workspace():
    manifest = json.loads((SPECIALIST_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, SPECIALIST_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_emit_attribution_within_declared_vocabulary_admitted(booted_workspace):
    """D64 Test 1: GenericSpecialist declares-emits action; handle_skill
    emits an action event → accepted; chain event carries
    emitting-specialist=binding-id.
    """
    ws = booted_workspace
    before = len(ws.event_chain.by_payload_subtype("action"))

    ws.substrate.skills.invoke("do-task", {"k": "v"})

    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before + 1
    emitted = actions[-1]
    # D64 §B.1: specialist-wrapped emit path stamps the binding-id.
    assert emitted["emitting-specialist"] == "primary-specialist"
    # Sanity: the bound specialist resolves the same binding-id.
    assert "primary-specialist" in ws.substrate.specialist_instances


def test_emit_attribution_outside_declared_vocabulary_rejected(booted_workspace):
    """D64 Test 2: specialist whose declared-event-emissions[] is
    [{payload-subtype: action}] attempts to emit a `claim` event →
    EventRejected(category="vocabulary"; path="event.emitting-specialist").

    Exercises the D64 §B.1 vocabulary check via a subclass that emits
    outside its declared vocabulary. Reuses EventRejected + "vocabulary"
    per C3 (no new FAILURE_CATEGORIES entry).
    """
    ws = booted_workspace

    class _OffVocabSpecialist(GenericSpecialist):
        """Subclass that emits `claim` despite declaring only `action`."""

        def emit_offvocab(self) -> None:
            actor_id = next(iter(self._workspace._substrate.state.actors))
            # Direct call to the wrapped _emit_event closure; D64 §B.1
            # stamps emitting-specialist on the event; per_event_checks
            # rejects since `claim` is not in declared-event-emissions[].
            self._emit_event(
                actor_id=actor_id,
                payload_subtype="claim",
                payload={"assertion": "off-vocab emission"},
            )

    # SPECIALIST_SPEC declares-emits [{payload-subtype: action}] only.
    spec = dict(ws.substrate.specialist_instances["primary-specialist"].spec)
    offender = _OffVocabSpecialist(spec=spec)
    # Register into the workspace so attach_workspace can look up the
    # binding-id (the closure needs the binding-id at attach time).
    ws.substrate.specialist_instances["offender-specialist"] = offender
    offender.attach_workspace(ws)

    with pytest.raises(EventRejected) as excinfo:
        offender.emit_offvocab()

    failures = excinfo.value.failures
    # There should be exactly one failure from D64 §B.1.
    vocab_failures = [
        f
        for f in failures
        if f.category == "vocabulary"
        and f.path == "event.emitting-specialist"
    ]
    assert len(vocab_failures) == 1
    f = vocab_failures[0]
    assert f.value == "offender-specialist"
    assert "claim" in f.reason
    assert "declared-event-emissions" in f.reason


def test_actor_handle_emit_no_attribution_slot(booted_workspace):
    """D64 Test 3: ActorHandle.emit_claim path emits without specialist
    attribution. Event lands in chain; the per-event emit-attribution
    check is skipped (event.emitting-specialist absent); the event dict
    has no emitting-specialist key.
    """
    ws = booted_workspace
    # Remove the existing claim subscriber (primary-specialist subscribes
    # to claim) so the emit lands without invoking handle_skill — keeps
    # this test focused on the non-specialist emit path.
    ws.substrate.specialist_subscribers = []

    before = len(ws.event_chain.by_payload_subtype("claim"))
    primary = ws.actors["agent-primary"]
    emitted = primary.emit_claim("non-specialist claim", role="author")

    # Event admitted (D64 check skips when slot absent).
    claims = ws.event_chain.by_payload_subtype("claim")
    assert len(claims) == before + 1
    # No emitting-specialist key on the event dict (D64 §B.1: slot is
    # optional; ActorHandle path does not stamp).
    assert "emitting-specialist" not in emitted
    assert "emitting-specialist" not in claims[-1]
