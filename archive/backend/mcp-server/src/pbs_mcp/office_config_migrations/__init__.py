"""Office-config schema migrations.

Each migration is a function `(data: dict) -> dict` that takes a parsed
office-config dict at version N and returns one at version N+1.
Migrations live one-per-file as `vN_to_vN1.py` exporting `migrate(data)`.

The dispatcher reads `data["schema_version"]` and applies migrations
sequentially up to the requested target version. Used both at load time
(in-memory forward migration) and by the `setup-office` skill (writes
migrated config back to disk).
"""
from __future__ import annotations

import importlib
import logging
from typing import Callable

logger = logging.getLogger(__name__)

# Registry of (from_version, to_version) → migrate function. Populated
# lazily on first call to apply_migrations.
_REGISTRY: dict[tuple[int, int], Callable[[dict], dict]] | None = None


def _build_registry() -> dict[tuple[int, int], Callable[[dict], dict]]:
    """Discover migrations by importing the v{N}_to_v{N+1} modules."""
    registry: dict[tuple[int, int], Callable[[dict], dict]] = {}
    for from_v, to_v in [(1, 2), (2, 3)]:
        modname = f"pbs_mcp.office_config_migrations.v{from_v}_to_v{to_v}"
        try:
            mod = importlib.import_module(modname)
        except ImportError as e:
            logger.warning("migration module %s not importable: %s", modname, e)
            continue
        if not hasattr(mod, "migrate"):
            logger.warning("migration module %s missing `migrate` function", modname)
            continue
        registry[(from_v, to_v)] = mod.migrate
    return registry


def apply_migrations(data: dict, target: int) -> dict:
    """Apply migrations to bring `data` up to `target` schema version.

    No-op if data is already at target. Raises if no migration path exists.
    Migrations are pure functions; the input dict is not mutated.
    """
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _build_registry()

    current = int(data.get("schema_version", 1))
    if current == target:
        return data
    if current > target:
        raise ValueError(
            f"office-config at version {current} is newer than target {target}; "
            "no downgrade migrations exist"
        )

    while current < target:
        step = (current, current + 1)
        if step not in _REGISTRY:
            raise ValueError(
                f"no migration registered for schema_version {current} → {current + 1}"
            )
        logger.info("applying office-config migration v%d → v%d", *step)
        data = _REGISTRY[step](data)
        current += 1
    return data
