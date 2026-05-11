"""Tests for Workspace context-manager lifecycle (boot + shutdown events)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"


@pytest.fixture
def boot_kwargs():
    return {
        "manifest": json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text()),
        "extensions_dir": SUBSTRATE_FIXTURE / "extensions",
    }


def test_context_manager_exit_emits_shutdown(boot_kwargs):
    """Per Bref closure of D39: boot emits N composition-change:add events
    (one per manifest actor) plus a lifecycle-transition:boot. The boot
    and shutdown events still form a valid pair around the session."""
    with Workspace.boot(**boot_kwargs) as ws:
        n_actors = len(boot_kwargs["manifest"]["composition"]["actors"])
        boot_count = len(ws.event_chain)
        assert boot_count == n_actors + 1
    # After exit, the shutdown event was appended.
    chain = ws.event_chain
    assert len(chain) == n_actors + 2
    transitions = [
        e for e in chain if e["payload-subtype"] == "lifecycle-transition"
    ]
    assert [t["payload"]["transition-type"] for t in transitions] == [
        "boot",
        "shutdown",
    ]


def test_explicit_shutdown_idempotent(boot_kwargs):
    ws = Workspace.boot(**boot_kwargs)
    ws.shutdown()
    n_after_first = len(ws.event_chain)
    ws.shutdown()  # second call should be no-op
    assert len(ws.event_chain) == n_after_first


def test_boot_event_present_in_chain(boot_kwargs):
    """Per Bref closure of D39: the lifecycle-transition:boot is the LAST
    event emitted at boot — preceded by N composition-change:add events
    (one per manifest actor). The first event in the chain has prev-event=None.
    """
    with Workspace.boot(**boot_kwargs) as ws:
        events = list(ws.events())
        assert events[0]["prev-event"] is None
        # Exactly one boot transition; it's the tail at this point.
        boot_events = [
            e
            for e in events
            if e["payload-subtype"] == "lifecycle-transition"
            and e["payload"]["transition-type"] == "boot"
        ]
        assert len(boot_events) == 1
        assert boot_events[0] is events[-1]


def test_event_chain_integrity_across_lifecycle(boot_kwargs):
    """Every event's prev-event references the prior; chain is intact end-to-end."""
    ws = Workspace.boot(**boot_kwargs)
    ws.actors["human-1"]
    ws.actors["agent-primary"].emit_action("test", parameters={})
    ws.shutdown()
    events = list(ws.events())
    assert events[0]["prev-event"] is None
    for prior, current in zip(events, events[1:]):
        assert current["prev-event"] == prior["id"]
