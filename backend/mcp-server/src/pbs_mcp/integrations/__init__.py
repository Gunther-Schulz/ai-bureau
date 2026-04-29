"""Pluggable integration adapters declared at office setup.

Each integration class (email, calendar, scanner, phone, accounting,
DMS, GIS, ...) has its own subpackage with a `protocol.py` (the small
interface adapters implement) and one or more concrete adapter modules
(starting with `none.py` — the no-op default).

v3 (post-design-review) makes integration declarations a free-form
list rather than a fixed-key map. To declare email integration:

    integrations:
      - class: email
        adapter: thunderbird-maildir
        config: {profile_path: ...}

Resolution: `office_config.find_integration(class_name)` finds the
declared integration; this package's `load_adapter(class_name)`
imports the matching `pbs_mcp.integrations.<class>.<adapter>` module
and instantiates its `Adapter` class with the adapter's config dict.

Why adapters: each integration class is independently swappable. An
office on Thunderbird picks `email.adapter: thunderbird-maildir`; an
office on Microsoft 365 picks `email.adapter: outlook-pst`. The MCP
tools that consume these (`fetch_emails`, `list_calendar_events`,
etc.) work against the protocol, not the adapter.

The class set is open: any string is valid; resolution succeeds
when a matching subpackage with a matching adapter module exists.
"""
from __future__ import annotations

import importlib
import logging
from typing import Any

from pbs_mcp import office_config

logger = logging.getLogger(__name__)


def load_adapter(class_name: str) -> Any:
    """Resolve the configured adapter for an integration class.

    Returns an instantiated adapter ready to call. Raises:
    - IntegrationNotConfiguredError: no integration with this class is declared
    - AdapterResolutionError: declared but the adapter module doesn't exist
      or doesn't expose an `Adapter` class
    """
    cfg = office_config.load()
    integration = cfg.find_integration(class_name)
    if integration is None:
        raise IntegrationNotConfiguredError(
            f"no integration declared for class {class_name!r}; "
            f"add `- class: {class_name}, adapter: <name>` to office-config.integrations"
        )

    adapter_name = integration.adapter
    adapter_config = integration.config

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


class IntegrationNotConfiguredError(RuntimeError):
    """Raised when an integration class has no entry in office-config.integrations."""


class AdapterResolutionError(RuntimeError):
    """Raised when an adapter module can't be loaded or instantiated."""
