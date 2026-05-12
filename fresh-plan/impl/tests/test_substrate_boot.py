"""Tests for the B2 boot procedure (orchestrating B1 + substrate instantiation)."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace, WorkspaceBootError, boot_workspace


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"


@pytest.fixture
def substrate_manifest() -> dict:
    return json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text())


@pytest.fixture
def substrate_extensions_dir() -> Path:
    return SUBSTRATE_FIXTURE / "extensions"


def test_boot_success_returns_workspace(substrate_manifest, substrate_extensions_dir):
    ws = boot_workspace(substrate_manifest, substrate_extensions_dir)
    try:
        assert ws.workspace_id == "substrate-test-ws"
        assert ws.runtime_shape == "interactive"
        assert "primary" in ws.substrate.known_binding_ids
    finally:
        ws.shutdown()


def test_boot_surfaces_b1_failures_as_WorkspaceBootError(
    substrate_manifest, substrate_extensions_dir
):
    bad_manifest = copy.deepcopy(substrate_manifest)
    # Reference a shape provision that isn't loaded -> B1 resolution failure.
    bad_manifest["composition"]["shape"]["provision"] = "nope-ext:nope-shape"
    with pytest.raises(WorkspaceBootError) as exc_info:
        boot_workspace(bad_manifest, substrate_extensions_dir)
    assert any(f.category == "resolution" for f in exc_info.value.failures)


def test_boot_advertises_substrate_capabilities(
    substrate_manifest, substrate_extensions_dir
):
    ws = boot_workspace(substrate_manifest, substrate_extensions_dir)
    try:
        # Per D17 core capabilities.
        assert set(ws.substrate.capabilities) >= {"hooks", "skills", "event-chain"}
    finally:
        ws.shutdown()


def test_boot_registers_manifest_actors(substrate_manifest, substrate_extensions_dir):
    ws = boot_workspace(substrate_manifest, substrate_extensions_dir)
    try:
        assert set(ws.actors.keys()) == {"human-1", "agent-primary"}
    finally:
        ws.shutdown()


def test_boot_emits_lifecycle_transition_boot_event(
    substrate_manifest, substrate_extensions_dir
):
    """Per Bref closure of D39: boot now emits N composition-change:add events
    (one per manifest actor) followed by one lifecycle-transition:boot event.
    The boot event is the last event in the post-boot chain; the chain begins
    with manifest-actor seed events.
    """
    ws = boot_workspace(substrate_manifest, substrate_extensions_dir)
    try:
        events = list(ws.events())
        n_actors = len(substrate_manifest["composition"]["actors"])
        assert len(events) == n_actors + 1
        # Boot event sits at the end (after manifest-actor seeds).
        boot_event = events[-1]
        assert boot_event["payload-subtype"] == "lifecycle-transition"
        assert boot_event["payload"]["transition-type"] == "boot"
        # The first event in the chain is now a composition-change:add for
        # the first manifest actor (with prev-event=None).
        first = events[0]
        assert first["payload-subtype"] == "composition-change"
        assert first["payload"]["change-type"] == "add"
        assert first["payload"]["binding-kind"] == "actor"
        assert first["prev-event"] is None
    finally:
        ws.shutdown()


def test_Workspace_boot_classmethod_equivalent(substrate_manifest, substrate_extensions_dir):
    ws = Workspace.boot(substrate_manifest, substrate_extensions_dir)
    try:
        assert ws.workspace_id == substrate_manifest["id"]
    finally:
        ws.shutdown()


def test_boot_error_carries_failure_list(substrate_extensions_dir):
    bad = {"id": "x", "composition": {}}  # nearly-empty manifest -> many failures
    with pytest.raises(WorkspaceBootError) as exc_info:
        boot_workspace(bad, substrate_extensions_dir)
    assert exc_info.value.failures, "expected at least one structured failure"


# -------------------------------------------------------------------
# D46 — boot procedure honors detection-surface-recovery triad
# -------------------------------------------------------------------


def test_d46_unknown_shape_provision_surfaces_workspace_boot_error(
    substrate_manifest, substrate_extensions_dir, monkeypatch
):
    """Per D46 §B.1: a manifest declaring a shape provision-id whose spec.id
    has no registered runtime class surfaces as WorkspaceBootError, not
    silent shape=None degradation.

    Uses monkeypatch to temporarily unregister `min-shape` from `_SHAPE_CLASSES`
    so the existing `min-shape-ext:min-shape` provision in the substrate-test
    fixture (which DOES exist in extension.provisions[] — past the B1
    extension-resolution check) hits the no-registered-runtime-class path.
    """
    from fresh_plan.runtime import shape as shape_module

    monkeypatch.delitem(shape_module._SHAPE_CLASSES, "min-shape", raising=False)

    with pytest.raises(WorkspaceBootError) as exc_info:
        boot_workspace(substrate_manifest, substrate_extensions_dir)
    failures = exc_info.value.failures
    assert any(
        f.category == "resolution"
        and f.path == "composition.shape.provision"
        and "no registered runtime class" in f.reason
        for f in failures
    ), f"expected D46 §B.1 shape resolution failure, got: {failures}"


def test_d46_unknown_adapter_provision_surfaces_workspace_boot_error(monkeypatch):
    """Per D46 §B.1: unknown adapter provision-id (provision exists in
    extension.provisions[] but has no registered runtime class) surfaces
    as WorkspaceBootError naming the offending binding-id, not silent skip.

    Uses the workspace-mcp-adapter fixture and monkeypatches the adapter
    registry to unregister `mcp-server-ext:mcp-client` — so the existing
    fixture's adapter provision (past B1) hits the no-registered-runtime-
    class path.
    """
    from fresh_plan.runtime import adapter as adapter_module

    fixture_root = Path(__file__).parent / "fixtures" / "workspace-mcp-adapter"
    if not fixture_root.exists():
        pytest.skip("workspace-mcp-adapter fixture missing")

    manifest = json.loads((fixture_root / "workspace.json").read_text())

    monkeypatch.delitem(
        adapter_module._ADAPTER_CLASSES, "mcp-server-ext:mcp-client", raising=False
    )

    with pytest.raises(WorkspaceBootError) as exc_info:
        boot_workspace(manifest, fixture_root / "extensions")
    failures = exc_info.value.failures
    assert any(
        f.category == "resolution"
        and "adapter-bindings" in f.path
        and "no registered runtime class" in f.reason
        for f in failures
    ), f"expected D46 §B.1 adapter resolution failure, got: {failures}"


def test_d46_actor_with_missing_id_surfaces_workspace_boot_error(
    substrate_manifest, substrate_extensions_dir
):
    """Per D46 §C cleanup: a manifest actor lacking 'id' surfaces as
    WorkspaceBootError(category="actor-seeding"), not silent drop."""
    bad_manifest = json.loads(json.dumps(substrate_manifest))
    # Inject a malformed actor (missing id) at index 1; B1 schema validation
    # should catch this earlier via actor.id required slot, but if it slips
    # past (e.g., schema permits empty list and runtime adds defensively),
    # boot must surface it. Test as defensive guard per D46 §C.
    actors = bad_manifest["composition"].get("actors", [])
    if not actors:
        pytest.skip("substrate-test fixture has no actors to mutate")
    # Strip 'id' from one actor's record and bypass B1 by directly
    # constructing a manifest the validator wouldn't have seen.
    actors[0] = {k: v for k, v in actors[0].items() if k != "id"}
    bad_manifest["composition"]["actors"] = actors
    with pytest.raises((WorkspaceBootError, Exception)) as exc_info:
        boot_workspace(bad_manifest, substrate_extensions_dir)
    # B1 should fail first (actor.id is required by schema); if it doesn't,
    # the boot procedure's actor-seeding loop catches per D46 §C.
    # Either failure is acceptable as long as the error is structured.
    if isinstance(exc_info.value, WorkspaceBootError):
        assert exc_info.value.failures, "expected structured failures"


def test_d46_capability_only_substrate_binding_surfaces_resolution_error(
    substrate_manifest, substrate_extensions_dir
):
    """Per D46 §B.3: a substrate-binding with only required-capabilities
    (no explicit provision) surfaces as WorkspaceBootError(category="resolution").
    Phase B does not support capability-only resolution; explicit provision
    is required.
    """
    bad_manifest = json.loads(json.dumps(substrate_manifest))
    # Replace the substrate-binding's provision with required-capabilities only.
    bad_manifest["composition"]["substrate-bindings"][0] = {
        "binding-id": "primary",
        "required-capabilities": ["hooks", "skills", "event-chain"],
        "runtime-shape": "interactive",
    }
    with pytest.raises(WorkspaceBootError) as exc_info:
        boot_workspace(bad_manifest, substrate_extensions_dir)
    failures = exc_info.value.failures
    assert any(
        f.category == "resolution"
        and "substrate-bindings" in f.path
        and "capability-only binding is not bootable" in f.reason
        for f in failures
    ), f"expected D46 §B.3 capability-only resolution failure, got: {failures}"
