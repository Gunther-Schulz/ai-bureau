"""End-to-end validator tests.

Covers the orchestrated `validate_workspace_boot` path on each fixture.
"""
from __future__ import annotations

import json
from pathlib import Path

from fresh_plan.validator import validate_workspace_boot


def _run(fixtures_dir: Path, name: str):
    fx = fixtures_dir / name
    ws = json.loads((fx / "workspace.json").read_text())
    return validate_workspace_boot(ws, fx / "extensions")


def test_valid_workspace_boots(fixtures_dir):
    result = _run(fixtures_dir, "workspace-valid")
    assert result.success, [f"{f.category}/{f.path}: {f.reason}" for f in result.failures]
    assert result.loaded_extensions is not None
    assert "core-ext" in result.loaded_extensions
    assert result.vocabulary_tables is not None


def test_cycle_workspace_fails_with_circular_dependency(fixtures_dir):
    result = _run(fixtures_dir, "workspace-cycle")
    assert not result.success
    cycles = [f for f in result.failures if f.category == "circular-dependency"]
    assert len(cycles) == 1
    # Cycle should include both ext-a and ext-b
    cycle_value = cycles[0].value
    if isinstance(cycle_value, list):
        assert set(cycle_value) >= {"ext-a", "ext-b"}


def test_version_conflict_workspace_fails(fixtures_dir):
    result = _run(fixtures_dir, "workspace-version-conflict")
    assert not result.success
    vc_failures = [f for f in result.failures if f.category == "version-conflict"]
    assert len(vc_failures) == 1
    assert vc_failures[0].value == "dep-ext"
    assert vc_failures[0].declarers is not None
    # Two declarers; one each from consumer-a and consumer-b
    assert len(vc_failures[0].declarers) == 2


def test_resolution_fail_workspace(fixtures_dir):
    result = _run(fixtures_dir, "workspace-resolution-fail")
    assert not result.success
    res = [f for f in result.failures if f.category == "resolution"]
    assert res


def test_capability_fail_workspace(fixtures_dir):
    result = _run(fixtures_dir, "workspace-capability-fail")
    assert not result.success
    cats = {f.category for f in result.failures}
    assert "capability" in cats


def test_vocabulary_fail_workspace(fixtures_dir):
    result = _run(fixtures_dir, "workspace-vocabulary-fail")
    assert not result.success
    cats = {f.category for f in result.failures}
    assert "vocabulary" in cats


def test_identity_fail_workspace(fixtures_dir):
    result = _run(fixtures_dir, "workspace-identity-fail")
    assert not result.success
    cats = {f.category for f in result.failures}
    assert "identity" in cats


def test_binding_fail_workspace(fixtures_dir):
    result = _run(fixtures_dir, "workspace-binding-fail")
    assert not result.success
    cats = {f.category for f in result.failures}
    assert "binding" in cats


def test_result_success_implies_empty_failures(fixtures_dir):
    """Boolean coercion + invariants."""
    result = _run(fixtures_dir, "workspace-valid")
    assert bool(result) is True
    assert result.failures == []
    fail_result = _run(fixtures_dir, "workspace-cycle")
    assert bool(fail_result) is False
    assert fail_result.failures


def test_pbs_schulz_phase_a_example_surfaces_resolution_failures(schemas_dir, tmp_path):
    """The PBS-Schulz example references extensions not present as on-disk artifacts.

    Per the B1 brief: that example was prose-only at Phase A; the validator
    should report extensions-not-found resolution failures when run against
    an empty extensions directory.
    """
    ws = json.loads((schemas_dir / "examples" / "workspace-pbs-schulz.json").read_text())
    result = validate_workspace_boot(ws, tmp_path)  # empty extensions dir
    assert not result.success
    res = [f for f in result.failures if f.category == "resolution"]
    # Each of the four declared extensions should produce a "not found in extensions-dir" failure.
    not_found_ids = {f.value for f in res if "not found" in f.reason}
    assert not_found_ids >= {
        "a2a-protocol-ext",
        "mcp-protocol-ext",
        "practitioner-shape-ext",
        "pbs-schulz-ext",
    }
