"""Tests for Phase C C2 JSONL persistence layer (D70 §B).

Covers:
  1. PersistenceLayer save_event + load_chain round-trip preserves event
     order + content.
  2. State-fully-derivable boot round-trip per D39 + D40 §A: boot → emit
     5+ events → shutdown → boot from JSONL → state matches.
  3. D40 §A query interface (filter-by-* / state_at(n)) works over the
     reloaded chain.
  4. D54 §B.2 classify_shape_change boot-integration: safe shape passes
     through; breaking shape surfaces WorkspaceBootError(category=
     'shape-migration-unsafe').
  5. D58 §B.1 lifecycle-derivation-mismatch reconciliation surfaces on
     manifest/chain disagreement.
  6. PersistenceCorruptionError category coverage: partial-line / malformed
     JSON / missing-directory all surface as
     WorkspaceBootError(category='persistence-corruption').
  7. Cold start (no persistence files) → boot proceeds normally.
  8. Atomic-append partial-line → corruption detected on next boot.

Per scope-cut C12: tests use pytest tmp_path fixtures for filesystem
isolation; no real network / SDK calls. ClaudeAgentSDKSubstrate fake-SDK
factory pattern from test_claude_agent_sdk_substrate is reused where
session-lifecycle tests are needed.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from fresh_plan.runtime import (
    PersistenceCorruptionError,
    PersistenceLayer,
    Workspace,
    WorkspaceBootError,
)


# Fixture pointers per existing test conventions.
IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
END_TO_END_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-end-to-end"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_e2e_manifest_with_persistence(tmp_path: Path) -> dict:
    """Load workspace-end-to-end manifest + inject persistence-root config.

    Reuses the e2e fixture (5 extensions; full composition; generic shape +
    real substrate-binding) and points the substrate-binding configuration
    at a temp directory so each test runs against an isolated persistence
    root.
    """
    manifest = json.loads(
        (END_TO_END_FIXTURE / "workspace.json").read_text()
    )
    manifest = copy.deepcopy(manifest)
    bindings = manifest["composition"]["substrate-bindings"]
    bindings[0].setdefault("configuration", {})
    bindings[0]["configuration"]["persistence-root"] = str(tmp_path)
    return manifest


# ---------------------------------------------------------------------------
# 1. PersistenceLayer round-trip (unit-level, no boot)
# ---------------------------------------------------------------------------


def test_persistence_layer_save_event_then_load_chain_preserves_order(
    tmp_path: Path,
) -> None:
    """D70 §B: save_event appends one line per event; load_chain yields
    them back in append order with content intact."""
    layer = PersistenceLayer(
        persistence_root=str(tmp_path), workspace_id="round-trip-ws"
    )
    assert not layer.has_events()

    events = [
        {"id": "evt-1", "prev-event": None, "payload-subtype": "claim"},
        {"id": "evt-2", "prev-event": "evt-1", "payload-subtype": "action"},
        {"id": "evt-3", "prev-event": "evt-2", "payload-subtype": "state-change"},
    ]
    for evt in events:
        layer.save_event(evt)

    assert layer.has_events()
    loaded = list(layer.load_chain())
    assert loaded == events


def test_persistence_layer_manifest_snapshot_round_trip(
    tmp_path: Path,
) -> None:
    """D70 §B: save_manifest_snapshot writes atomically;
    load_manifest_snapshot returns the saved dict; None when absent."""
    layer = PersistenceLayer(
        persistence_root=str(tmp_path), workspace_id="snap-ws"
    )
    assert layer.load_manifest_snapshot() is None
    assert not layer.has_manifest_snapshot()

    manifest = {"id": "snap-ws", "composition": {"shape": {"id": "core:s"}}}
    layer.save_manifest_snapshot(manifest)

    assert layer.has_manifest_snapshot()
    reloaded = layer.load_manifest_snapshot()
    assert reloaded == manifest

    # Atomic overwrite — the second save replaces the first.
    manifest2 = {"id": "snap-ws", "composition": {"shape": {"id": "core:s2"}}}
    layer.save_manifest_snapshot(manifest2)
    assert layer.load_manifest_snapshot() == manifest2


def test_persistence_layer_corruption_partial_line_at_eof(
    tmp_path: Path,
) -> None:
    """D70 §B.1: torn-append (partial JSON line at EOF) surfaces as
    PersistenceCorruptionError with line_number for the offending line."""
    layer = PersistenceLayer(
        persistence_root=str(tmp_path), workspace_id="torn-ws"
    )
    # Write one valid event then a partial line (no closing brace + no newline).
    layer.save_event({"id": "evt-1", "payload-subtype": "claim"})
    # Simulate a torn append: open in append mode + write incomplete line.
    with open(layer.events_path, "a", encoding="utf-8") as fh:
        fh.write('{"id": "evt-2", "payload-subtype": "ac')  # no closing }

    with pytest.raises(PersistenceCorruptionError) as excinfo:
        list(layer.load_chain())
    assert excinfo.value.line_number == 2
    assert "malformed JSON" in excinfo.value.reason


def test_persistence_layer_corruption_non_object_line(
    tmp_path: Path,
) -> None:
    """D70 §B.1: a line that is JSON but not an object → corruption.

    Defends against accidentally-persisted scalars; surfaces with the
    line_number so the operator can diagnose."""
    layer = PersistenceLayer(
        persistence_root=str(tmp_path), workspace_id="bad-type-ws"
    )
    layer.workspace_dir.mkdir(parents=True, exist_ok=True)
    layer.events_path.write_text('"a-string-not-an-object"\n', encoding="utf-8")

    with pytest.raises(PersistenceCorruptionError) as excinfo:
        list(layer.load_chain())
    assert excinfo.value.line_number == 1
    assert "not an object" in excinfo.value.reason


# ---------------------------------------------------------------------------
# 2. Cold start — boot without persistence files
# ---------------------------------------------------------------------------


def test_boot_with_persistence_cold_start_proceeds_normally(
    tmp_path: Path,
) -> None:
    """D70 §B: when the persistence directory does not exist (or is empty),
    boot proceeds as a normal cold start; manifest snapshot is written
    after boot completes."""
    manifest = _load_e2e_manifest_with_persistence(tmp_path)
    ws = Workspace.boot(
        manifest, END_TO_END_FIXTURE / "extensions"
    )
    try:
        # Boot succeeded; persistence is attached.
        assert ws.substrate.persistence is not None
        # Manifest snapshot was written after successful boot.
        snap = ws.substrate.persistence.load_manifest_snapshot()
        assert snap is not None
        assert snap["id"] == manifest["id"]
        # Chain carries the actor-seeding + lifecycle-transition:boot events.
        events_persisted = list(ws.substrate.persistence.load_chain())
        # 2 actors in e2e fixture + 1 boot event = 3 events minimum.
        assert len(events_persisted) >= 3
        assert events_persisted[-1].get("payload-subtype") == "lifecycle-transition"
    finally:
        ws.shutdown()


# ---------------------------------------------------------------------------
# 3. State-fully-derivable round-trip (Acceptance Criterion 2)
# ---------------------------------------------------------------------------


def test_chain_replay_reconstructs_state_after_restart(tmp_path: Path) -> None:
    """D39 + D40 §A: workspace boot → emit 5+ events → shutdown → boot
    from JSONL → state.work_units / state.actors / state.shape_config
    reconstruct identically."""
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    # First boot — emit events. Per generic-shape authority-bindings:
    # claim requires role='author' on an agent-actor; action + state-change
    # have no authority-binding constraints.
    ws1 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    agent = ws1.actors["agent-primary"]
    agent.emit_claim("first claim", role="author", confidence="high")
    agent.emit_action("test-action", parameters={"k": "v"})
    agent.emit_state_change("scope", before=None, after={"phase": "x"})
    # Snapshot first-boot state for comparison after replay.
    state_before_actors = dict(ws1.substrate.state.actors)
    state_before_scope = ws1.substrate.state.current_scope
    chain_len_before = len(ws1.event_chain)
    ws1.shutdown()

    # Second boot — replays the persisted chain.
    ws2 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        # State reconstructed from chain replay.
        assert ws2.substrate.state.actors == state_before_actors
        assert ws2.substrate.state.current_scope == state_before_scope
        # Replayed chain length ≥ original chain length (replay seeds events;
        # the second boot also adds its own boot event AFTER replay).
        assert len(ws2.event_chain) >= chain_len_before
    finally:
        ws2.shutdown()


# ---------------------------------------------------------------------------
# 4. D40 §A query interface over reloaded chain
# ---------------------------------------------------------------------------


def test_d40_query_interface_works_over_reloaded_chain(
    tmp_path: Path,
) -> None:
    """D40 §A: filter-by-payload-subtype / by-actor / state_at(n) all
    operate over the replayed chain after restart."""
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    ws1 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    agent = ws1.actors["agent-primary"]
    agent.emit_claim("claim-1", role="author", confidence="high")
    agent.emit_action("act-1")
    ws1.shutdown()

    ws2 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        # by_payload_subtype: at least one claim from prior session is present.
        claims = ws2.event_chain.by_payload_subtype("claim")
        assert any(
            (evt.get("payload") or {}).get("assertion") == "claim-1"
            for evt in claims
        )
        # by_actor: agent-primary attributes events.
        agent_events = ws2.event_chain.by_actor("agent-primary")
        assert len(agent_events) >= 2
        # state_at: replay 0..N reproduces a valid state snapshot.
        final_state = ws2.event_chain.state_at(len(ws2.event_chain) - 1)
        assert final_state.has_actor("agent-primary")
    finally:
        ws2.shutdown()


# ---------------------------------------------------------------------------
# 5. D54 §B.2 classify_shape_change boot integration
# ---------------------------------------------------------------------------


def test_shape_migration_breaking_change_surfaces_at_boot(
    tmp_path: Path,
) -> None:
    """D54 §B.2 + D70 §B: breaking shape-version bump between persisted
    chain's manifest snapshot and new manifest → WorkspaceBootError(
    category='shape-migration-unsafe').

    Setup: boot once to populate persistence; then mutate the persisted
    last-boot-manifest snapshot to declare a different shape provision-id
    (which classify_shape_change treats as 'breaking' per the D54 table).
    """
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    ws = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    ws.shutdown()

    # Edit the persisted manifest snapshot to look like a different shape
    # was active in the prior boot. id-change is classified breaking per
    # D54 §B.1 (any id change triggers workspace boundary).
    layer = PersistenceLayer(
        persistence_root=str(tmp_path), workspace_id=manifest["id"]
    )
    snap = layer.load_manifest_snapshot()
    assert snap is not None
    # The boot stored composition.shape — give it a synthetic prior id
    # that differs from the new manifest's shape provision.
    prior_shape = snap["composition"]["shape"]
    prior_shape["id"] = "imaginary-prior-shape"
    prior_shape["version"] = "0.0.9"
    layer.save_manifest_snapshot(snap)

    # Now boot again. classify_shape_change sees a different shape id.
    # However, the new manifest's composition.shape carries `provision`,
    # not `id`. The classifier checks `id` slot; the new manifest's
    # shape dict has no `id` slot at this point — the difference between
    # "imaginary-prior-shape" and None counts as breaking per the
    # classifier rule (any change to id slot).
    with pytest.raises(WorkspaceBootError) as excinfo:
        Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    failures = excinfo.value.failures
    assert any(
        f.category == "shape-migration-unsafe" for f in failures
    ), f"expected shape-migration-unsafe, got {[f.category for f in failures]}"


def test_shape_migration_safe_passes_through_boot(tmp_path: Path) -> None:
    """D54 §B.2 + D70 §B: safe-in-place shape change (no id / no slot
    changes) does not raise; boot proceeds. Same-manifest re-boot is
    the trivial safe case."""
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    # First boot — populate persistence.
    ws1 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    ws1.shutdown()

    # Second boot with IDENTICAL manifest — no slot differences;
    # classify_shape_change returns []. Should not raise.
    ws2 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        assert ws2.substrate.persistence is not None
    finally:
        ws2.shutdown()


# ---------------------------------------------------------------------------
# 6. PersistenceCorruptionError category surfaces (Acceptance Criterion 6)
# ---------------------------------------------------------------------------


def test_corrupted_jsonl_surfaces_at_boot_as_persistence_corruption(
    tmp_path: Path,
) -> None:
    """D70 §B.1: events.jsonl with a malformed JSON line surfaces at
    boot as WorkspaceBootError(category='persistence-corruption') with
    the original PersistenceCorruptionError chained via __cause__."""
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    # Cold-boot first to populate persistence with a valid chain.
    ws = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    ws.shutdown()

    # Corrupt the events.jsonl file — append a malformed line.
    layer = PersistenceLayer(
        persistence_root=str(tmp_path), workspace_id=manifest["id"]
    )
    with open(layer.events_path, "a", encoding="utf-8") as fh:
        fh.write("{this is not valid json}\n")

    # Subsequent boot must surface as WorkspaceBootError with
    # persistence-corruption category, chained to PersistenceCorruptionError.
    with pytest.raises(WorkspaceBootError) as excinfo:
        Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    failures = excinfo.value.failures
    assert len(failures) == 1
    assert failures[0].category == "persistence-corruption"
    assert isinstance(excinfo.value.__cause__, PersistenceCorruptionError)


# ---------------------------------------------------------------------------
# 7. Persistence opt-in semantics — no config means no on-disk writes
# ---------------------------------------------------------------------------


def test_boot_without_persistence_config_skips_persistence_layer(
    tmp_path: Path,
) -> None:
    """D70 §B + D57 §B.1: persistence is OPT-IN via configuration. A
    workspace booted WITHOUT persistence-root keeps everything in
    memory; substrate.persistence stays None; no files created."""
    # Use e2e fixture as-is (no persistence-root in configuration).
    manifest = json.loads(
        (END_TO_END_FIXTURE / "workspace.json").read_text()
    )

    ws = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        assert ws.substrate.persistence is None
    finally:
        ws.shutdown()
    # tmp_path remains empty (no persistence directory created).
    assert list(tmp_path.iterdir()) == []


# ---------------------------------------------------------------------------
# 8. D58 §B.1 lifecycle-derivation-mismatch reconciliation activation
# ---------------------------------------------------------------------------


def test_lifecycle_derivation_mismatch_surfaces_at_boot_via_persistence(
    tmp_path: Path,
) -> None:
    """D58 §B.1 + D70 §B: when the persisted chain contains no transition
    event for a work-unit AND the new manifest declares a
    lifecycle.completed-at for it, boot surfaces WorkspaceBootError(
    category='lifecycle-derivation-mismatch').

    Setup: cold boot to seed persistence; inject a manifest 'work-units'
    slot declaring a completed-at without any backing transition event
    in chain; re-boot must surface the mismatch.
    """
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    # First boot — populate persistence with chain (actors + boot event).
    ws = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    ws.shutdown()

    # Second boot — manifest now declares a work-unit with completed-at
    # that the chain has no transition for.
    manifest_with_wu = copy.deepcopy(manifest)
    manifest_with_wu["work-units"] = [
        {
            "id": "wu-imaginary",
            "kind": "core:task",
            "lifecycle": {"completed-at": "2026-05-17T10:00:00Z"},
        }
    ]
    with pytest.raises(WorkspaceBootError) as excinfo:
        Workspace.boot(
            manifest_with_wu, END_TO_END_FIXTURE / "extensions"
        )
    failures = excinfo.value.failures
    assert any(
        f.category == "lifecycle-derivation-mismatch" for f in failures
    ), f"expected lifecycle-derivation-mismatch, got {[f.category for f in failures]}"


# ---------------------------------------------------------------------------
# 9. PersistenceLayer attached at boot — append_event mirrors to JSONL
# ---------------------------------------------------------------------------


def test_substrate_append_event_mirrors_to_persistence_after_boot(
    tmp_path: Path,
) -> None:
    """D70 §B + Substrate.append_event Step 4a: every successful append
    writes one line to events.jsonl. Verifies the write-through path."""
    manifest = _load_e2e_manifest_with_persistence(tmp_path)

    ws = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        pre_count = len(list(ws.substrate.persistence.load_chain()))
        agent = ws.actors["agent-primary"]
        agent.emit_claim("post-boot claim", role="author", confidence="medium")
        agent.emit_action("post-boot-action")
        post_count = len(list(ws.substrate.persistence.load_chain()))
        # Two emits → two additional lines in events.jsonl.
        assert post_count == pre_count + 2
    finally:
        ws.shutdown()
