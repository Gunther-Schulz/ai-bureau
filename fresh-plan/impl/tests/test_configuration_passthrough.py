"""Tests for D57 §B.1 — workspace.composition.*.configuration pass-through.

Per D57 §C: 4 tests covering each of the four kind constructors. Each
test monkey-patches a ``_Failing<Kind>`` subclass into the kind's runtime
registry that raises from the constructor on a sentinel configuration
value; boots a manifest declaring that configuration; asserts
``WorkspaceBootError(category="configuration-rejected", path=...)`` with
the underlying exception chained via ``__cause__``.
"""
from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    DirectAPIAdapter,
    _ADAPTER_CLASSES,
)
from fresh_plan.runtime.boot import WorkspaceBootError
from fresh_plan.runtime.shape import MinShape, _SHAPE_CLASSES
from fresh_plan.runtime.specialist import (
    GenericSpecialist,
    _SPECIALIST_CLASSES,
)
from fresh_plan.runtime.substrate import (
    InProcessSubstrate,
    _SUBSTRATE_CLASSES,
)


SUBSTRATE_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-substrate-test"
RAG_FIXTURE = Path(__file__).parent / "fixtures" / "workspace-generic-specialist"


@dataclass
class _FailingShape(MinShape):
    """Raises from constructor when configuration carries the sentinel."""

    def __post_init__(self) -> None:
        if self.configuration and self.configuration.get("fail-on-construct"):
            raise RuntimeError("shape configuration rejected by test stub")
        super().__post_init__()


@dataclass
class _FailingAdapter(DirectAPIAdapter):
    def __post_init__(self) -> None:
        if self.configuration and self.configuration.get("fail-on-construct"):
            raise RuntimeError("adapter configuration rejected by test stub")


@dataclass
class _FailingSpecialist(GenericSpecialist):
    def __post_init__(self) -> None:
        if self.configuration and self.configuration.get("fail-on-construct"):
            raise RuntimeError("specialist configuration rejected by test stub")


@dataclass
class _FailingSubstrate(InProcessSubstrate):
    def __post_init__(self) -> None:
        if self.configuration and self.configuration.get("fail-on-construct"):
            raise RuntimeError("substrate configuration rejected by test stub")


@pytest.fixture
def restore_registries():
    """Snapshot and restore runtime registries so tests don't leak."""
    snapshot = (
        dict(_SHAPE_CLASSES),
        dict(_ADAPTER_CLASSES),
        dict(_SPECIALIST_CLASSES),
        dict(_SUBSTRATE_CLASSES),
    )
    yield
    _SHAPE_CLASSES.clear()
    _SHAPE_CLASSES.update(snapshot[0])
    _ADAPTER_CLASSES.clear()
    _ADAPTER_CLASSES.update(snapshot[1])
    _SPECIALIST_CLASSES.clear()
    _SPECIALIST_CLASSES.update(snapshot[2])
    _SUBSTRATE_CLASSES.clear()
    _SUBSTRATE_CLASSES.update(snapshot[3])


def test_shape_configuration_rejected(restore_registries) -> None:
    """D57 §B.1 — Shape constructor raises on configuration → WorkspaceBootError(category="configuration-rejected")."""
    _SHAPE_CLASSES["min-shape"] = _FailingShape
    manifest = json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text())
    manifest = deepcopy(manifest)
    manifest["composition"]["shape"]["configuration"] = {"fail-on-construct": True}

    with pytest.raises(WorkspaceBootError) as exc_info:
        Workspace.boot(manifest, SUBSTRATE_FIXTURE / "extensions")
    failures = exc_info.value.failures
    assert len(failures) == 1
    assert failures[0].category == "configuration-rejected"
    assert "composition.shape.configuration" in failures[0].path
    # Underlying RuntimeError chained via from.
    assert isinstance(exc_info.value.__cause__, RuntimeError)


def test_substrate_configuration_rejected(restore_registries) -> None:
    """D57 §B.1 — Substrate constructor raises → WorkspaceBootError(category="configuration-rejected")."""
    _SUBSTRATE_CLASSES["inprocess-substrate"] = _FailingSubstrate
    manifest = json.loads((SUBSTRATE_FIXTURE / "workspace.json").read_text())
    manifest = deepcopy(manifest)
    manifest["composition"]["substrate-bindings"][0]["configuration"] = {
        "fail-on-construct": True
    }

    with pytest.raises(WorkspaceBootError) as exc_info:
        Workspace.boot(manifest, SUBSTRATE_FIXTURE / "extensions")
    failures = exc_info.value.failures
    assert len(failures) == 1
    assert failures[0].category == "configuration-rejected"
    assert "substrate-bindings" in failures[0].path
    assert isinstance(exc_info.value.__cause__, RuntimeError)


def test_adapter_configuration_rejected(restore_registries) -> None:
    """D57 §B.1 — Adapter constructor raises → WorkspaceBootError(category="configuration-rejected").

    Uses the RAG fixture (which has adapter bindings) and replaces the
    direct-api adapter class with the failing stub.
    """
    # Locate adapter via direct-api protocol identifier registered for
    # DirectAPIAdapter in the runtime registry.
    _ADAPTER_CLASSES["direct-api-ext:direct-api"] = _FailingAdapter
    # Build a minimal workspace with one adapter binding pointing at a
    # direct-api adapter fixture. Reuse RAG fixture's manifest pattern.
    if not RAG_FIXTURE.exists():
        pytest.skip("rag fixture not present; adapter binding test needs adapter fixture")
    manifest = json.loads((RAG_FIXTURE / "workspace.json").read_text())
    manifest = deepcopy(manifest)
    # Inject configuration into the first adapter binding.
    ab = manifest["composition"]["adapter-bindings"][0]
    ab["configuration"] = {"fail-on-construct": True}
    # Make the failing class apply to whatever protocol this adapter uses.
    # Read its provision to find the protocol.
    from fresh_plan.runtime.provision import load_provision_spec

    spec = load_provision_spec(ab["provision"], RAG_FIXTURE / "extensions")
    protocol = spec.get("protocol-or-transport")
    _ADAPTER_CLASSES[protocol] = _FailingAdapter

    with pytest.raises(WorkspaceBootError) as exc_info:
        Workspace.boot(manifest, RAG_FIXTURE / "extensions")
    failures = exc_info.value.failures
    assert len(failures) == 1
    assert failures[0].category == "configuration-rejected"
    assert "adapter-bindings" in failures[0].path
    assert isinstance(exc_info.value.__cause__, RuntimeError)


def test_specialist_configuration_rejected(restore_registries) -> None:
    """D57 §B.1 — Specialist constructor raises → WorkspaceBootError(category="configuration-rejected")."""
    if not RAG_FIXTURE.exists():
        pytest.skip("rag fixture not present; specialist binding test needs specialist fixture")
    manifest = json.loads((RAG_FIXTURE / "workspace.json").read_text())
    manifest = deepcopy(manifest)
    sb = manifest["composition"]["specialist-bindings"][0]
    sb["configuration"] = {"fail-on-construct": True}
    from fresh_plan.runtime.provision import load_provision_spec

    spec = load_provision_spec(sb["provision"], RAG_FIXTURE / "extensions")
    specialist_id = spec.get("id")
    _SPECIALIST_CLASSES[specialist_id] = _FailingSpecialist

    with pytest.raises(WorkspaceBootError) as exc_info:
        Workspace.boot(manifest, RAG_FIXTURE / "extensions")
    failures = exc_info.value.failures
    assert len(failures) == 1
    assert failures[0].category == "configuration-rejected"
    assert "specialist-bindings" in failures[0].path
    assert isinstance(exc_info.value.__cause__, RuntimeError)
