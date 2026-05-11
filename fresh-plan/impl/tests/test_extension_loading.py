"""Tests for fresh_plan.validator.extensions."""
from __future__ import annotations

import json
from pathlib import Path

from fresh_plan.validator.extensions import (
    discover_extensions,
    load_extension,
    load_extension_manifest,
    resolve_provision_spec,
)


def test_discover_extensions_finds_versions(fixtures_dir):
    """Two-version layout in workspace-version-conflict fixture is discovered."""
    ext_dir = fixtures_dir / "workspace-version-conflict" / "extensions"
    discovered = discover_extensions(ext_dir)
    assert "dep-ext" in discovered
    assert set(discovered["dep-ext"].keys()) == {"1.0.0", "2.0.0"}
    assert "consumer-a" in discovered
    assert "consumer-b" in discovered


def test_discover_extensions_empty_dir(tmp_path):
    """Empty / nonexistent directory returns empty dict."""
    assert discover_extensions(tmp_path) == {}
    assert discover_extensions(tmp_path / "does-not-exist") == {}


def test_load_extension_manifest(fixtures_dir):
    path = fixtures_dir / "workspace-valid" / "extensions" / "core-ext" / "1.0.0" / "extension-manifest.json"
    manifest = load_extension_manifest(path)
    assert manifest["id"] == "core-ext"
    assert manifest["version"] == "1.0.0"


def test_load_extension_resolves_provisions(fixtures_dir):
    """Loaded extension should have provisions_loaded populated from local specs."""
    path = fixtures_dir / "workspace-valid" / "extensions" / "core-ext" / "1.0.0" / "extension-manifest.json"
    ext, errors = load_extension("core-ext", "1.0.0", path)
    assert errors == []
    assert "minimal-substrate" in ext.provisions_loaded
    assert ext.provisions_loaded["minimal-substrate"]["id"] == "minimal-substrate"
    assert "minimal-shape" in ext.provisions_loaded


def test_resolve_provision_spec_url_is_unresolved(tmp_path):
    """Per D29: spec-ref is opaque-string-resolvable-by-the-loader; URLs are out of scope."""
    content, err = resolve_provision_spec(tmp_path, "https://example.org/x.schema.json")
    assert content is None
    assert err is None  # not an error — just unresolved at this layer


def test_resolve_provision_spec_missing_file(tmp_path):
    content, err = resolve_provision_spec(tmp_path, "./does-not-exist.json")
    assert content is None
    assert err is not None
    assert "not found" in err
