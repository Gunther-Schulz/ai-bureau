"""Provision-spec loading helper shared across kind-loaders.

Splits a `<ext-id>:<provision-id>` ref, discovers extensions, loads the
matching extension, returns the provision spec dict. Used by shape.py
+ adapter.py + (future) specialist.py.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


class ProvisionResolutionError(ValueError):
    """Raised when a provision-ref cannot be resolved to a registered runtime class.

    Per D57 §C: boot.py distinguishes this from constructor-rejection
    raises. Registry-miss → ``WorkspaceBootError(category="resolution")``;
    constructor-raise (anything OTHER than this exception type) →
    ``WorkspaceBootError(category="configuration-rejected")``.
    """


def load_provision_spec(provision_ref: str, extensions_dir: Path) -> dict:
    """Load a provision spec dict from a `<ext-id>:<provision-id>` ref.

    Raises ValueError when the extension is not discoverable under
    `extensions_dir` or no version of it contains a provision with the
    given id.
    """
    from fresh_plan.validator.extensions import (
        discover_extensions,
        load_extension,
    )

    ext_id, prov_id = provision_ref.split(":", 1)
    discovered = discover_extensions(extensions_dir)
    if ext_id not in discovered:
        raise ValueError(
            f"provision {provision_ref!r}: extension {ext_id!r} not discovered "
            f"under {extensions_dir!s}"
        )
    spec: Optional[dict] = None
    for version, manifest_path in discovered[ext_id].items():
        loaded_ext, _errs = load_extension(ext_id, version, manifest_path)
        spec = loaded_ext.provisions_loaded.get(prov_id)
        if spec is not None:
            break
    if spec is None:
        raise ValueError(
            f"provision {provision_ref!r}: provision id {prov_id!r} not found "
            f"in any version of extension {ext_id!r}"
        )
    return spec
