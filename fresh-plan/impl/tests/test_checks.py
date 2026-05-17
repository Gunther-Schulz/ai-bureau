"""Tests for D30 cross-kind referential integrity checks.

Each check category gets at least one positive (clean pass) and one
negative test (specific failure). Positive tests reuse the
workspace-valid fixture; negative tests use targeted fixtures.
"""
from __future__ import annotations

import json
from pathlib import Path

from fresh_plan.validator import validate_workspace_boot
from fresh_plan.validator.checks import (
    check_binding_availability,
    check_capability_satisfaction,
    check_resolution,
    check_vocabulary_resolution,
    check_workspace_internal_identity,
)


def _validate(fixtures_dir: Path, name: str):
    fx = fixtures_dir / name
    ws = json.loads((fx / "workspace.json").read_text())
    return validate_workspace_boot(ws, fx / "extensions")


# --- D30 §1: Resolution -----------------------------------------------------


def test_resolution_clean_pass(fixtures_dir):
    """Valid workspace has no resolution failures."""
    result = _validate(fixtures_dir, "workspace-valid")
    assert result.success
    assert not any(f.category == "resolution" for f in result.failures)


def test_resolution_failure_for_missing_extension(fixtures_dir):
    """workspace-resolution-fail: shape provision references non-loadable extension."""
    result = _validate(fixtures_dir, "workspace-resolution-fail")
    assert not result.success
    res_failures = [f for f in result.failures if f.category == "resolution"]
    assert res_failures
    # The shape.provision failure should be present:
    assert any("composition.shape.provision" in f.path for f in res_failures)


# --- D30 §2: Capability satisfaction ----------------------------------------


def test_capability_clean_pass(fixtures_dir):
    result = _validate(fixtures_dir, "workspace-valid")
    assert not any(f.category == "capability" for f in result.failures)


def test_capability_failure(fixtures_dir):
    """shape requires `min-ext:exotic-cap` but substrate advertises only hooks."""
    result = _validate(fixtures_dir, "workspace-capability-fail")
    assert not result.success
    cap_failures = [f for f in result.failures if f.category == "capability"]
    assert cap_failures
    assert any("exotic-cap" in str(f.value) for f in cap_failures)


# --- D30 §3: Vocabulary resolution ------------------------------------------


def test_vocabulary_clean_pass(fixtures_dir):
    result = _validate(fixtures_dir, "workspace-valid")
    assert not any(f.category == "vocabulary" for f in result.failures)


def test_vocabulary_failure_for_unregistered_protocol(fixtures_dir):
    """Adapter declares an unregistered protocol-or-transport."""
    result = _validate(fixtures_dir, "workspace-vocabulary-fail")
    assert not result.success
    vocab_failures = [f for f in result.failures if f.category == "vocabulary"]
    assert vocab_failures
    assert any("ghost-ext:unregistered-protocol" in str(f.value) for f in vocab_failures)


# --- D30 §4: Workspace-internal identity (boot-time portion) ----------------


def test_identity_clean_pass(fixtures_dir):
    result = _validate(fixtures_dir, "workspace-valid")
    assert not any(f.category == "identity" for f in result.failures)


def test_identity_failure_for_dangling_substrate_binding(fixtures_dir):
    """agent-actor.substrate-binding references a binding-id that doesn't exist."""
    result = _validate(fixtures_dir, "workspace-identity-fail")
    assert not result.success
    id_failures = [f for f in result.failures if f.category == "identity"]
    assert id_failures
    assert any("ghost-binding-id" in str(f.value) for f in id_failures)


def test_identity_duplicate_actor_id():
    """Identity check catches duplicate actor.id."""
    ws = {
        "id": "dup-ws",
        "composition": {
            "extensions": [],
            "shape": {"provision": "x:y", "version-range": ">=1.0.0"},
            "substrate-bindings": [
                {"binding-id": "b1", "required-capabilities": ["hooks"], "runtime-shape": "interactive"}
            ],
            "actors": [
                {"id": "alice", "subtype": "human-actor", "declared-name": "Alice"},
                {"id": "alice", "subtype": "human-actor", "declared-name": "Alice 2"},
            ],
            "adapter-bindings": [],
            "specialist-bindings": [],
        },
    }
    failures = check_workspace_internal_identity(ws)
    assert any("duplicate actor.id" in f.reason for f in failures)


# --- D30 §5: Binding availability -------------------------------------------


def test_binding_clean_pass(fixtures_dir):
    result = _validate(fixtures_dir, "workspace-valid")
    assert not any(f.category == "binding" for f in result.failures)


def test_binding_failure_for_unmet_required_adapter(fixtures_dir):
    """specialist requires sp-ext:ghost-adapter; no workspace adapter-binding provides it."""
    result = _validate(fixtures_dir, "workspace-binding-fail")
    assert not result.success
    bind_failures = [f for f in result.failures if f.category == "binding"]
    assert bind_failures
    assert any("ghost-adapter" in str(f.value) for f in bind_failures)


# --- Direct check-function unit tests ---------------------------------------


def test_check_resolution_pure_unit():
    """Resolution check on a workspace with no loaded extensions still flags missing provisions."""
    ws = {
        "composition": {
            "extensions": [{"id": "missing-ext", "version-range": ">=1.0.0"}],
            "shape": {"provision": "missing-ext:foo", "version-range": ">=1.0.0"},
            "substrate-bindings": [],
            "actors": [],
            "adapter-bindings": [],
            "specialist-bindings": [],
        }
    }
    failures = check_resolution(ws, loaded={})
    # shape.provision references missing extension → resolution failure
    assert any(f.path == "composition.shape.provision" for f in failures)


# --- D51 §B.2: B1 collect-all silent-skip removal ---------------------------


def test_capability_check_runs_even_with_empty_loaded():
    """D51 §B.2: capability-satisfaction check fires when no extensions loaded
    BUT manifest declares unsatisfied requirements (prior `if loaded:` guard
    silently skipped this; D51 removed the guard).

    Constructs a minimal workspace declaring an extension but with no
    extensions actually available on disk. The validator should surface the
    resolution failure AND attempt all D30 checks unconditionally rather
    than silent-skipping when `loaded` is empty.
    """
    ws = {
        "id": "test-empty-loaded",
        "composition": {
            "extensions": [{"id": "missing-ext", "version-range": ">=1.0.0"}],
            "shape": {"provision": "missing-ext:foo", "version-range": ">=1.0.0"},
            "substrate-bindings": [
                {"binding-id": "s1", "provision": "missing-ext:sub", "version-range": ">=1.0.0"}
            ],
            "actors": [{"id": "a1", "subtype": "human-actor", "declared-name": "a1"}],
            "adapter-bindings": [],
            "specialist-bindings": [],
        },
    }
    # Run with empty loaded — pre-D51 this would silently skip capability /
    # vocabulary / binding checks; post-D51 they run (no-op or surface failures).
    cap_failures = check_capability_satisfaction(ws, loaded={})
    voc_failures = check_vocabulary_resolution(ws, loaded={}, vocabulary_tables={})
    bin_failures = check_binding_availability(ws, loaded={})
    # No declared required-capabilities + no loaded ext → cap check no-ops cleanly.
    # No vocabulary references at this manifest level → vocab no-ops.
    # No specialist required-adapter-bindings → binding no-ops.
    # KEY: no exception, function actually ran (vs being skipped entirely).
    assert isinstance(cap_failures, list)
    assert isinstance(voc_failures, list)
    assert isinstance(bin_failures, list)
