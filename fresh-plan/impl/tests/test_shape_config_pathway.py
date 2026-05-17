"""Tests for D65 §B.1 — state.shape_config population pathway.

Per D65 §C: 2 tests. boot.py threads
``composition['shape'].get('configuration', {}) or {}`` to
``substrate.state.shape_config`` after substrate construction; immutable
post-boot per D4 + D13 shape-as-substantive-identity.

Closes D56 §D D-7 (state.shape_config population pathway deferred from
the D56 grammar lock).
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from fresh_plan.runtime import Workspace


GENERIC_SHAPE_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-generic-shape"
)


def test_shape_config_populated_from_manifest_configuration() -> None:
    """D65 §B.1 — composition.shape.configuration populates substrate.state.shape_config.

    Manifest carries composition.shape.configuration={"required-attester":
    "actor-1"}; boot → workspace.substrate.state.shape_config equals that
    dict.
    """
    manifest = json.loads((GENERIC_SHAPE_FIXTURE / "workspace.json").read_text())
    manifest = deepcopy(manifest)
    manifest["composition"]["shape"]["configuration"] = {
        "required-attester": "actor-1"
    }

    ws = Workspace.boot(manifest, GENERIC_SHAPE_FIXTURE / "extensions")

    assert ws.substrate.state.shape_config == {"required-attester": "actor-1"}


def test_shape_config_absent_configuration_yields_empty_dict() -> None:
    """D65 §B.1 — absent composition.shape.configuration → state.shape_config == {}.

    Manifest omits configuration field on composition.shape (default
    fixture state); boot → workspace.substrate.state.shape_config is
    an empty dict (default per WorkspaceState field).
    """
    manifest = json.loads((GENERIC_SHAPE_FIXTURE / "workspace.json").read_text())
    # Defensive: ensure the fixture does not pre-declare configuration.
    assert "configuration" not in manifest["composition"]["shape"]

    ws = Workspace.boot(manifest, GENERIC_SHAPE_FIXTURE / "extensions")

    assert ws.substrate.state.shape_config == {}
