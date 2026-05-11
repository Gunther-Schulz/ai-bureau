"""Tests for fresh_plan.validator.schemas — Phase A schema loading."""
from __future__ import annotations

import json

import pytest

from fresh_plan.validator.schemas import (
    SchemaStore,
    load_schemas,
    schema_filename_for_kind,
)


def test_load_schemas_loads_all_fifteen(schemas_dir):
    """All 15 Phase A schemas (per D35 inventory) load."""
    store = load_schemas(schemas_dir)
    assert isinstance(store, SchemaStore)
    assert len(store.store) == 15
    # Spot-check inventory
    for fn in [
        "_common.schema.json",
        "extension-manifest.schema.json",
        "workspace.schema.json",
        "actor.schema.json",
        "event.schema.json",
        "substrate.schema.json",
        "shape.schema.json",
        "adapter.schema.json",
        "specialist.schema.json",
        "work-unit.schema.json",
        "payload-claim.schema.json",
        "payload-action.schema.json",
        "payload-state-change.schema.json",
        "payload-composition-change.schema.json",
        "payload-lifecycle-transition.schema.json",
    ]:
        assert fn in store.store, f"missing schema {fn}"


def test_cross_file_ref_resolves(schemas_dir):
    """workspace.schema.json $refs actor.schema.json — should resolve cleanly."""
    store = load_schemas(schemas_dir)
    # Validate a Phase A example which exercises cross-file $ref:
    examples_dir = schemas_dir / "examples"
    ws = json.loads((examples_dir / "workspace-pbs-schulz.json").read_text())
    validator = store.validator_for("workspace.schema.json")
    errors = list(validator.iter_errors(ws))
    assert errors == [], f"expected no errors, got {[e.message for e in errors]}"


def test_all_phase_a_examples_validate(schemas_dir):
    """All 10 worked examples (per D35) validate against their schemas."""
    store = load_schemas(schemas_dir)
    pairs = {
        "workspace-pbs-schulz.json": "workspace.schema.json",
        "a2a-protocol-ext.manifest.json": "extension-manifest.schema.json",
        "actor-agent.json": "actor.schema.json",
        "actor-human.json": "actor.schema.json",
        "event-claim.json": "event.schema.json",
        "substrate-claude-agent-sdk.json": "substrate.schema.json",
        "shape-practitioner.json": "shape.schema.json",
        "adapter-a2a-peer.json": "adapter.schema.json",
        "specialist-planning-document-work.json": "specialist.schema.json",
        "work-unit-b-plan-section.json": "work-unit.schema.json",
    }
    examples_dir = schemas_dir / "examples"
    for example_name, schema_name in pairs.items():
        inst = json.loads((examples_dir / example_name).read_text())
        v = store.validator_for(schema_name)
        errs = list(v.iter_errors(inst))
        assert errs == [], f"{example_name} failed: {[e.message for e in errs]}"


def test_load_schemas_missing_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_schemas(tmp_path / "does-not-exist")


def test_load_schemas_rejects_malformed_json(tmp_path):
    bad = tmp_path / "bad.schema.json"
    bad.write_text("{not valid json")
    with pytest.raises(json.JSONDecodeError):
        load_schemas(tmp_path)


def test_schema_filename_for_kind():
    assert schema_filename_for_kind("substrate") == "substrate.schema.json"
    assert schema_filename_for_kind("shape") == "shape.schema.json"
    assert schema_filename_for_kind("adapter") == "adapter.schema.json"
    assert schema_filename_for_kind("specialist") == "specialist.schema.json"
    with pytest.raises(ValueError):
        schema_filename_for_kind("workspace")  # not a provision kind per D29
