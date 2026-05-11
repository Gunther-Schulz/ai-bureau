"""Shared pytest fixtures."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def schemas_dir() -> Path:
    """Path to Phase A schemas (locked at D35)."""
    here = Path(__file__).resolve()
    # tests/conftest.py: parents[0]=tests, [1]=impl, [2]=fresh-plan
    return here.parents[2] / "schemas"


def load_workspace(fixture_root: Path) -> dict:
    """Helper: load a fixture's workspace.json."""
    return json.loads((fixture_root / "workspace.json").read_text())
