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
        assert set(ws.substrate.capabilities) >= {"hooks", "skills", "event-streaming"}
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
    ws = boot_workspace(substrate_manifest, substrate_extensions_dir)
    try:
        events = list(ws.events())
        assert len(events) == 1
        assert events[0]["payload-subtype"] == "lifecycle-transition"
        assert events[0]["payload"]["transition-type"] == "boot"
        assert events[0]["prev-event"] is None
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
