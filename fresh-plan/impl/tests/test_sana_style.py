"""Sana-style worked-example test suite (D53 §C).

Validates D38's rejection of `knowledge` as a core fresh-plan kind by
exercising the full 8-kind composition (workspace + actor + event +
substrate + shape + adapter + specialist + work-unit) against a
Sana-style knowledge-platform-shaped scenario. The fixture binds:

  - ``inprocess-substrate-ext`` (reused; B7 precedent)
  - ``sana-knowledge-shape-ext`` (NEW — declares pre-citation +
    post-corpus-write hooks + actor-requirements {human-actor:{min:1}})
  - ``mcp-server-ext`` (reused; B7 precedent — provides mcp-client
    protocol identifier)
  - ``sana-style-ext`` (NEW — knowledge-retriever-adapter +
    knowledge-writer-adapter both reusing mcp-client protocol, plus
    knowledge-agent-specialist + synthesis-task work-unit-kind)

Tests cover the §C test list:
  1. Boot succeeds; 8 kinds present + hooks registered.
  2. Curator emits claim (role=curator) → accepted.
  3. kb-agent invokes retrieve skill → action events into chain.
  4. kb-agent invokes synthesize skill → action + claim with
     evidence-references resolving against prior retrieve action
     outcome-references → passes pre-citation hook.
  5. Synthesize with empty evidence-references → pre-citation hook
     raises → EventRejected(category="hook-handler").
  6. ``state_at(n)`` replay reconstructs corpus-related projections
     deterministically.

Honest-basis: this test file Reads from the workspace-sana-style
fixture (workspace.json + ext spec files), the sana_style_ext Python
stub package, and the framework runtime registries (registered into
via ``register()`` + cleaned via ``unregister()`` in the fixture
teardown so other tests' baselines aren't perturbed).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.extensions.sana_style_ext import register, unregister
from fresh_plan.runtime import EventRejected, Workspace


SANA_STYLE_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-sana-style"
)


@pytest.fixture
def sana_workspace():
    """Boot the Sana-style fixture; register Sana stubs first, unregister
    in teardown so other tests see clean registries."""
    register()
    try:
        manifest = json.loads((SANA_STYLE_FIXTURE / "workspace.json").read_text())
        ws = Workspace.boot(manifest, SANA_STYLE_FIXTURE / "extensions")
        try:
            yield ws
        finally:
            ws.shutdown()
    finally:
        unregister()


# ----------------------------------------------------------------------
# Test 1 — D53 §C test 1: boot succeeds; all 8 kinds present; shape attached
# + hooks registered (also exercises D52 §B.1 step 2.5 for the FIRST time
# in a fixture per D52 §D D-7 forward-bar).
# ----------------------------------------------------------------------


def test_d53_t1_boot_succeeds_with_eight_kinds_and_hooks_registered(sana_workspace):
    """All 8 fresh-plan kinds compose without surfacing a framework-core gap."""
    ws = sana_workspace

    # (1) workspace kind — boot returned a Workspace handle with the
    # manifest id.
    assert ws.workspace_id == "sana-style-ws"

    # (2) actor kind — three actors registered; curator-1 + consumer-1 +
    # kb-agent. The manifest places curator-1 FIRST so D52 step 2.5
    # admits the seeding sequence (first add → human-actor count = 1
    # satisfies min=1).
    assert set(ws.actors.keys()) == {"curator-1", "consumer-1", "kb-agent"}
    assert ws.substrate.state.get_actor("curator-1")["subtype"] == "human-actor"
    assert ws.substrate.state.get_actor("consumer-1")["subtype"] == "human-actor"
    assert ws.substrate.state.get_actor("kb-agent")["subtype"] == "agent-actor"

    # (3) event kind — boot emitted lifecycle + seeding events into the
    # chain (D39 + D44 + D52).
    chain = ws.event_chain
    assert len(chain) >= 4  # 3 actor-add + 1 lifecycle:boot
    assert chain.tail["payload-subtype"] == "lifecycle-transition"

    # (4) substrate kind — bound substrate exposes hooks/skills/event-chain.
    assert ws.substrate is not None
    assert "hooks" in ws.substrate.capabilities
    assert "skills" in ws.substrate.capabilities
    assert "event-chain" in ws.substrate.capabilities

    # (5) shape kind — sana-knowledge-shape attached + hooks registered.
    shape = ws.substrate.shape
    assert shape is not None
    assert shape.id == "sana-knowledge-shape"
    registered = set(ws.hooks.registered_names())
    # The lifecycle hooks (substrate-fired) carry policy-real handlers;
    # pre-citation + post-corpus-write are semantic declarations carrying
    # no-op stub handlers (per GenericShape pattern). All four are
    # observable via registered_names().
    assert {"pre-event-emit", "post-event-emit",
            "pre-citation", "post-corpus-write"} <= registered

    # (6) adapter kind — both retriever + writer bound + resolvable.
    assert "knowledge-retriever" in ws.adapters
    assert "knowledge-writer" in ws.adapters
    retriever = ws.adapter("knowledge-retriever")
    writer = ws.adapter("knowledge-writer")
    assert retriever.protocol_or_transport == "mcp-server-ext:mcp-client"
    assert writer.protocol_or_transport == "mcp-server-ext:mcp-client"

    # (7) specialist kind — knowledge-agent bound; required adapters resolved.
    spec = ws.specialist("knowledge-agent")
    assert spec is not None
    assert spec.id == "knowledge-agent-specialist"
    # Required-adapter-bindings resolved into specialist._adapters.
    assert spec._adapters["sana-style-ext:knowledge-retriever-adapter"] is retriever
    assert spec._adapters["sana-style-ext:knowledge-writer-adapter"] is writer
    # Skill registry populated.
    assert "retrieve" in ws.skills.registered_ids()
    assert "synthesize" in ws.skills.registered_ids()

    # (8) work-unit kind — synthesis-task vocabulary registered for the
    # workspace (D51 §B.1 — registered at boot from ext manifest).
    assert "sana-style-ext:synthesis-task" in ws.substrate.registered_work_unit_kinds


# ----------------------------------------------------------------------
# Test 2 — D53 §C test 2: curator emits a claim (role=curator) into the
# chain. Demonstrates that human-actors emit claims unrestricted by the
# pre-citation gate (only role='author' triggers it).
# ----------------------------------------------------------------------


def test_d53_t2_curator_emits_claim_accepted(sana_workspace):
    ws = sana_workspace
    before = len(ws.event_chain.by_payload_subtype("claim"))
    curator = ws.actors["curator-1"]
    curator.emit_claim(
        "Document doc-1 has been curated.",
        role="curator",
    )
    claims = ws.event_chain.by_payload_subtype("claim")
    assert len(claims) == before + 1
    emitted = claims[-1]
    assert emitted["payload"]["assertion"] == "Document doc-1 has been curated."
    assert emitted["actors"][0]["id"] == "curator-1"
    assert emitted["actors"][0]["role"] == "curator"
    # No evidence-references required for curator role per
    # sana-knowledge-shape pre-citation policy (only role=author triggers).
    assert "evidence-references" not in emitted["payload"]


# ----------------------------------------------------------------------
# Test 3 — D53 §C test 3: kb-agent invokes retrieve skill via specialist.
# Asserts the action chain (specialist emit + adapter emit) and the
# outcome-reference is observable for downstream synthesize.
# ----------------------------------------------------------------------


def test_d53_t3_kb_agent_retrieve_emits_chained_action_events(sana_workspace):
    ws = sana_workspace
    before = len(ws.event_chain.by_payload_subtype("action"))
    response = ws.skills.invoke("retrieve", {"query": "doc-1", "k": 2})
    actions = ws.event_chain.by_payload_subtype("action")
    # Two new action events: specialist intent + adapter wire-call.
    assert len(actions) == before + 2
    # Specialist's emission has no outcome-reference; adapter's does.
    spec_action = actions[-2]
    adapter_action = actions[-1]
    assert spec_action["payload"]["action-name"] == "retrieve"
    assert "outcome-reference" not in spec_action["payload"]
    assert adapter_action["payload"]["action-name"] == "retrieve"
    assert adapter_action["payload"]["outcome-reference"] == response["adapter-outcome-ref"]
    # Both attribute to kb-agent.
    assert spec_action["actors"][0]["id"] == "kb-agent"
    assert adapter_action["actors"][0]["id"] == "kb-agent"
    # Response surfaces stub chunks.
    assert response["ok"] is True
    assert len(response["chunks"]) == 2


# ----------------------------------------------------------------------
# Test 4 — D53 §C test 4: kb-agent invokes synthesize skill. Asserts that
# emitted synthesis claim carries evidence-references resolving against
# prior retrieve action outcome-references; pre-citation hook accepts.
# ----------------------------------------------------------------------


def test_d53_t4_synthesize_with_resolvable_evidence_refs_accepted(sana_workspace):
    ws = sana_workspace
    # Prime the chain with a retrieve so outcome-refs exist.
    retrieve_response = ws.skills.invoke("retrieve", {"query": "doc-1", "k": 1})
    expected_ref = retrieve_response["adapter-outcome-ref"]

    before_claims = len(ws.event_chain.by_payload_subtype("claim"))
    before_actions = len(ws.event_chain.by_payload_subtype("action"))

    # Synthesize without explicit evidence-references — specialist
    # collects from chain (which now has one retrieve outcome-ref).
    synth_response = ws.skills.invoke(
        "synthesize", {"query": "doc-1", "synthesis": "doc-1 says X."}
    )

    claims = ws.event_chain.by_payload_subtype("claim")
    actions = ws.event_chain.by_payload_subtype("action")

    # +1 action (synthesize action emission) + 1 claim (the synthesis claim).
    assert len(actions) == before_actions + 1
    assert len(claims) == before_claims + 1
    synth_claim = claims[-1]
    assert synth_claim["payload"]["assertion"] == "doc-1 says X."
    assert synth_claim["payload"]["evidence-references"] == [expected_ref]
    assert synth_claim["actors"][0]["id"] == "kb-agent"
    assert synth_claim["actors"][0]["role"] == "author"
    assert synth_response["evidence-references"] == [expected_ref]


# ----------------------------------------------------------------------
# Test 5 — D53 §C test 5: synthesize with empty evidence-references →
# pre-citation hook raises → EventRejected(category="hook-handler").
# Validates D38 §3 hook-based knowledge discipline (the citation
# requirement is policy, not core-kind).
# ----------------------------------------------------------------------


def test_d53_t5_synthesize_without_evidence_refs_rejected(sana_workspace):
    ws = sana_workspace
    # Prime with a retrieve so the chain has data (the missing-refs
    # check is independent of chain content; just want to ensure the
    # check isn't trivially short-circuited).
    ws.skills.invoke("retrieve", {"query": "doc-1", "k": 1})

    # Explicitly pass empty evidence-references — specialist propagates
    # the empty list into the claim payload; pre-citation hook treats
    # empty as "missing".
    with pytest.raises(EventRejected) as excinfo:
        ws.skills.invoke(
            "synthesize",
            {"synthesis": "claim without evidence", "evidence-references": []},
        )
    failures = excinfo.value.failures
    assert any(f.category == "hook-handler" for f in failures), (
        f"expected hook-handler failure; got {[f.category for f in failures]!r}"
    )
    # Reason names the missing-evidence-references condition.
    reasons = " ".join(f.reason for f in failures)
    assert "evidence-references" in reasons

    # The rejected claim must NOT be in the chain (chain-integrity-
    # preserved per D47 §B.2 substrate.py:230 contract).
    claims_post = ws.event_chain.by_payload_subtype("claim")
    assert all(
        c["payload"].get("assertion") != "claim without evidence"
        for c in claims_post
    )


# ----------------------------------------------------------------------
# Test 6 — D53 §C test 6: state_at(n) replay reconstructs Sana-style
# projections (actors + work-unit) deterministically. Validates D38 §2
# framing (workspace state event projections carry assertional content).
# ----------------------------------------------------------------------


def test_d53_t6_state_at_replay_reconstructs_corpus_related_projections(
    sana_workspace,
):
    ws = sana_workspace
    # Drive some workspace activity: a curate claim + a retrieve + a
    # synthesis-task work-unit creation.
    ws.actors["curator-1"].emit_claim("Curated doc-1.", role="curator")
    ws.skills.invoke("retrieve", {"query": "doc-1", "k": 1})
    wu_seq_pre = len(ws.event_chain)
    ws.create_work_unit(
        id="wu-synth-1",
        kind="sana-style-ext:synthesis-task",
        payload={"query": "doc-1"},
    )
    final_seq = len(ws.event_chain) - 1

    # Before the work-unit-creation event, the work-unit is not in state.
    state_before = ws.state_at(wu_seq_pre - 1)
    assert not state_before.has_work_unit("wu-synth-1")
    # After the full chain, the work-unit IS in state.
    state_after = ws.state_at(final_seq)
    assert state_after.has_work_unit("wu-synth-1")
    wu = state_after.get_work_unit("wu-synth-1")
    assert wu["kind"] == "sana-style-ext:synthesis-task"
    # Pure replay equals live state: both replayed actors and live
    # state actors share the same set.
    assert set(state_after.actors.keys()) == set(ws.substrate.state.actors.keys())
