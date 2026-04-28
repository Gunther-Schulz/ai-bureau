"""Pluggable integration adapters declared at office setup.

Each integration class (email, calendar, scanner, phone, accounting)
has its own subpackage with a `protocol.py` (the small interface
adapters implement) and one or more concrete adapter modules
(starting with `none.py` — the no-op default).

Resolution: `office_config.integrations.<class>.adapter` names the
adapter; this package's `load_adapter(class_name)` imports the
matching module and instantiates it with the adapter's config dict.

Why adapters: each integration class is independently swappable. An
office on Thunderbird picks `email.adapter: thunderbird-maildir`; an
office on Microsoft 365 picks `email.adapter: outlook-pst`. The MCP
tools that consume these (`fetch_emails`, `list_calendar_events`,
etc.) work against the protocol, not the adapter.

This is the pattern discussed in ROADMAP.md "Modular integrations
declared at office setup". Currently all classes default to `none`;
real adapters land per ROADMAP priority.
"""
from __future__ import annotations

import importlib
import logging
from typing import Any

from pbs_mcp import office_config

logger = logging.getLogger(__name__)


VALID_CLASSES = ("email", "calendar", "scanner", "phone", "accounting")


def load_adapter(class_name: str) -> Any:
    """Resolve the configured adapter for an integration class.

    Returns an instantiated adapter ready to call. Raises
    AdapterResolutionError on misconfiguration (unknown adapter, missing
    config, etc.).
    """
    if class_name not in VALID_CLASSES:
        raise ValueError(
            f"unknown integration class {class_name!r}; valid: {VALID_CLASSES}"
        )

    cfg = office_config.load().integrations
    integration_cfg = getattr(cfg, class_name)
    adapter_name = integration_cfg.adapter
    adapter_config = integration_cfg.config

    module_path = f"pbs_mcp.integrations.{class_name}.{adapter_name.replace('-', '_')}"
    try:
        mod = importlib.import_module(module_path)
    except ImportError as e:
        raise AdapterResolutionError(
            f"adapter {adapter_name!r} for class {class_name!r} not implemented; "
            f"expected module at {module_path}: {e}"
        )

    if not hasattr(mod, "Adapter"):
        raise AdapterResolutionError(
            f"adapter module {module_path} missing `Adapter` class"
        )

    return mod.Adapter(config=adapter_config)


class AdapterResolutionError(RuntimeError):
    """Raised when an adapter can't be loaded or instantiated."""
