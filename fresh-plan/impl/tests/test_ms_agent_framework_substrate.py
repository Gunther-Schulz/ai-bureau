"""Tests for the B2b MS Agent Framework substrate stub (per D12 + D17 + D41)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import (
    InProcessSubstrate,
    MSAgentFrameworkSubstrate,
    Substrate,
    Workspace,
    load_substrate_from_provision,
)
from fresh_plan.validator.schemas import load_schemas


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
MS_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-ms-agent-framework"
SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "schemas"


@pytest.fixture
def booted_ms_workspace():
    manifest = json.loads((MS_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, MS_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


def test_load_substrate_from_provision_returns_ms_subclass():
    """Per D41 + D12: the shipped substrate provision dispatches to the
    MSAgentFrameworkSubstrate runtime class with the expected capabilities
    + runtime-shape."""
    schema_store = load_schemas(SCHEMAS_DIR)
    substrate = load_substrate_from_provision(
        "ms-agent-framework-substrate-ext:ms-agent-framework-substrate",
        IMPL_EXTENSIONS_DIR,
        workspace_id="probe-ws",
        runtime_shape="ms-agent-framework-substrate-ext:workflow",
        schema_store=schema_store,
        capabilities=["hooks", "skills", "event-chain"],
    )
    assert isinstance(substrate, MSAgentFrameworkSubstrate)
    assert isinstance(substrate, Substrate)
    assert not isinstance(substrate, InProcessSubstrate)
    assert substrate.capabilities == ["hooks", "skills", "event-chain"]
    assert substrate.runtime_shape == "ms-agent-framework-substrate-ext:workflow"


def test_boot_attaches_ms_substrate_with_full_composition(booted_ms_workspace):
    """Per B2b: booting the fixture instantiates MSAgentFrameworkSubstrate
    (not InProcessSubstrate), attaches generic-shape, and instantiates the
    bound adapter + specialist."""
    ws = booted_ms_workspace
    assert isinstance(ws.substrate, MSAgentFrameworkSubstrate)
    assert isinstance(ws.substrate, Substrate)
    assert not isinstance(ws.substrate, InProcessSubstrate)
    assert ws.substrate.shape is not None and ws.substrate.shape.id == "generic-shape"
    assert "primary-mcp" in ws.substrate.adapter_instances
    assert "primary-specialist" in ws.substrate.specialist_instances


def test_ms_substrate_satisfies_shape_and_specialist_required_capabilities(
    booted_ms_workspace,
):
    """Per D17 + D41: the stub MS substrate advertises the three core
    abstract capabilities; both the bound generic-shape (required-capabilities)
    and generic-specialist (required-substrate-capabilities) are satisfied."""
    ws = booted_ms_workspace
    declared = set(ws.substrate.declared_capabilities())
    assert {"hooks", "skills", "event-chain"} <= declared

    shape = ws.substrate.shape
    for cap in shape.required_capabilities:
        assert ws.substrate.has_capability(cap)

    specialist = ws.specialist("primary-specialist")
    for cap in specialist.required_substrate_capabilities:
        assert ws.substrate.has_capability(cap)


def test_ms_substrate_state_at_n_replays_runtime_added_actors(booted_ms_workspace):
    """Per D39 + D40 §A: state_at(n) replays events 0..n. Cross-substrate
    parity — the MS-stub substrate satisfies the same event-derivable-state
    property the InProcessSubstrate satisfies."""
    ws = booted_ms_workspace
    initial_len = len(ws.event_chain)
    ws.register_agent_actor(id="sub-ms-1", substrate_binding="primary")
    comp_seq = initial_len
    state_before = ws.state_at(comp_seq - 1)
    assert not state_before.has_actor("sub-ms-1")
    state_after = ws.state_at(comp_seq)
    assert state_after.has_actor("sub-ms-1")


def test_load_substrate_from_provision_raises_on_unknown_spec_id(tmp_path):
    """Loader dispatch: an extension whose substrate spec.id has no registered
    runtime class raises ValueError."""
    ext_dir = tmp_path / "unknown-substrate-ext" / "0.1.0"
    ext_dir.mkdir(parents=True)
    (ext_dir / "extension-manifest.json").write_text(
        json.dumps(
            {
                "id": "unknown-substrate-ext",
                "version": "0.1.0",
                "vocabulary-registrations": [],
                "provisions": [
                    {
                        "kind": "substrate",
                        "id": "unknown-substrate",
                        "spec-ref": "./substrate.json",
                    }
                ],
                "dependencies": {
                    "required-core-capabilities": [],
                    "required-extensions": [],
                },
            }
        )
    )
    (ext_dir / "substrate.json").write_text(
        json.dumps(
            {
                "id": "unknown-substrate",
                "version": "0.1.0",
                "capabilities": ["hooks"],
                "runtime-shapes": ["interactive"],
            }
        )
    )
    schema_store = load_schemas(SCHEMAS_DIR)
    with pytest.raises(ValueError) as excinfo:
        load_substrate_from_provision(
            "unknown-substrate-ext:unknown-substrate",
            tmp_path,
            workspace_id="probe-ws",
            runtime_shape="interactive",
            schema_store=schema_store,
            capabilities=["hooks"],
        )
    assert "unknown-substrate" in str(excinfo.value)


def test_inprocess_loader_dispatch_still_resolves_inprocess_class():
    """Existing inprocess-substrate fixtures must keep instantiating
    InProcessSubstrate via the loader path (B2b regression guard)."""
    schema_store = load_schemas(SCHEMAS_DIR)
    substrate = load_substrate_from_provision(
        "inprocess-substrate-ext:inprocess-substrate",
        IMPL_EXTENSIONS_DIR,
        workspace_id="probe-ws",
        runtime_shape="interactive",
        schema_store=schema_store,
        capabilities=["hooks", "skills", "event-chain"],
    )
    assert isinstance(substrate, InProcessSubstrate)
    assert isinstance(substrate, Substrate)
