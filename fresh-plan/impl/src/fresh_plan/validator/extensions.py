"""Extension discovery + manifest loading.

On-disk layout (per impl/README):

    extensions_dir/
      <extension-id>/
        <version>/
          extension-manifest.json
          # spec-refs reference paths relative to this directory

`spec-ref` resolution per D29: opaque-string-resolvable-by-the-loader.
This loader resolves a spec-ref as:

    1. A path relative to the manifest's directory, loaded as JSON if it
       exists as a file.
    2. Otherwise the raw string is retained (not dereferenced); the
       validator surfaces this as a non-failure for now — remote URLs /
       registry references are out of scope at this layer.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class LoadedExtension:
    """One concrete extension version found on disk.

    `manifest` is the parsed extension-manifest.json. `provisions_loaded`
    maps provision-id → parsed spec-ref content (when locally resolvable).
    `manifest_path` is the on-disk path; used for spec-ref resolution.
    """

    extension_id: str
    version: str
    manifest: dict
    manifest_path: Path
    provisions_loaded: dict[str, dict] = field(default_factory=dict)
    provision_load_errors: dict[str, str] = field(default_factory=dict)


def discover_extensions(extensions_dir: Path) -> dict[str, dict[str, Path]]:
    """Scan `extensions_dir` and return {ext-id: {version: manifest-path}}.

    Skips entries that don't have an `extension-manifest.json`. Returns an
    empty dict if the directory does not exist (the caller handles this
    as a resolution failure if the workspace references extensions).
    """
    extensions_dir = Path(extensions_dir)
    discovered: dict[str, dict[str, Path]] = {}
    if not extensions_dir.is_dir():
        return discovered

    for ext_dir in sorted(extensions_dir.iterdir()):
        if not ext_dir.is_dir():
            continue
        ext_id = ext_dir.name
        for ver_dir in sorted(ext_dir.iterdir()):
            if not ver_dir.is_dir():
                continue
            manifest_path = ver_dir / "extension-manifest.json"
            if manifest_path.is_file():
                discovered.setdefault(ext_id, {})[ver_dir.name] = manifest_path

    return discovered


def load_extension_manifest(manifest_path: Path) -> dict:
    """Read a single extension manifest from disk."""
    with manifest_path.open() as f:
        return json.load(f)


def resolve_provision_spec(
    manifest_dir: Path, spec_ref: str
) -> tuple[Optional[dict], Optional[str]]:
    """Resolve a `spec-ref` to its parsed content if locally resolvable.

    Returns (content, error). On success: (parsed_dict, None). On a path
    that resolves to a missing file: (None, error_message). On a non-path
    spec-ref (e.g., URL, registry reference): (None, None) — not an
    error, just unresolved at this layer (per D29 opaque-string semantics).
    """
    if "://" in spec_ref:
        # URL / registry reference — out of scope at this layer.
        return None, None
    candidate = (manifest_dir / spec_ref).resolve()
    if not candidate.is_file():
        return None, f"spec-ref path not found: {spec_ref}"
    try:
        with candidate.open() as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"spec-ref not valid JSON: {spec_ref}: {e}"


def load_extension(
    extension_id: str, version: str, manifest_path: Path
) -> tuple[LoadedExtension, list[str]]:
    """Load one extension's manifest + provisions.

    Returns (loaded_extension, load_errors). Load errors are strings;
    the workspace-level validator wraps them into ValidationFailures.
    """
    errors: list[str] = []
    manifest = load_extension_manifest(manifest_path)

    ext = LoadedExtension(
        extension_id=extension_id,
        version=version,
        manifest=manifest,
        manifest_path=manifest_path,
    )

    manifest_dir = manifest_path.parent
    for provision in manifest.get("provisions", []):
        prov_id = provision.get("id")
        spec_ref = provision.get("spec-ref")
        if prov_id is None or spec_ref is None:
            # Will be caught by schema validation of the manifest itself.
            continue
        content, err = resolve_provision_spec(manifest_dir, spec_ref)
        if err is not None:
            ext.provision_load_errors[prov_id] = err
            errors.append(f"provision {prov_id!r}: {err}")
        elif content is not None:
            ext.provisions_loaded[prov_id] = content

    return ext, errors


def select_version(available_versions: list[str], preferred: str) -> Optional[str]:
    """Pick a version (returns the string from available_versions) or None.

    Wrapper around the version-range library, used by callers that need
    to resolve `(id, version-range)` against discovered versions. See
    fresh_plan.validator.dependency for the full multi-range
    intersection algorithm (D33).
    """
    from fresh_plan.validator.dependency import max_satisfying

    return max_satisfying(available_versions, preferred)


def iter_loaded_provisions(loaded: dict[str, LoadedExtension]) -> Any:
    """Yield (ext-id, kind, provision-id, spec-ref) tuples across all loaded extensions."""
    for ext_id, ext in loaded.items():
        for prov in ext.manifest.get("provisions", []):
            yield ext_id, prov.get("kind"), prov.get("id"), prov.get("spec-ref")
