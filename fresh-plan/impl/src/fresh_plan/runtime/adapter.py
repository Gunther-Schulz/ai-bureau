"""Adapter runtime — minimal MCP-server-protocol adapter (D16 + D2 + D29).

Per D16, an adapter integrates a workspace with an external surface via a
single protocol-or-transport (extension-registered per D2 strict reading +
D29 namespacing). Per D36 / B4 scope: this module ships a *stub* adapter
that validates the MCP adapter pattern + the registered `mcp-client`
protocol identifier. The stub emits a workspace `action` event per call
and returns a canned response. Real-wire MCP integration (JSON-RPC over
stdio / HTTP) is Phase C territory.

Runtime concerns owned here:
  - Hold the loaded adapter spec dict and expose D16 slot accessors.
  - Attach to a Workspace post-construction (boot-ordering subtlety:
    Workspace is constructed after the substrate; the adapter is
    instantiated at step 7 and attached after Workspace exists, before
    the boot lifecycle event).
  - `call(tool_name, parameters)` emits one `action` event and returns
    a stub response carrying an outcome-reference.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass
class MCPToolAdapter:
    """Stub MCP-server-protocol adapter per D16 + B4.

    Holds the loaded adapter spec dict and exposes the D16 slot accessors
    plus a `call()` method that emits one `action` event into the
    workspace event chain and returns a canned response. No real MCP wire
    is opened in B4; Phase C replaces the stub `call()` body with a real
    JSON-RPC client.
    """

    spec: dict
    _emit_event: Optional[Callable[..., dict]] = field(default=None, repr=False)
    _outcome_counter: int = field(default=0, repr=False)
    _workspace: Any = field(default=None, repr=False)

    @property
    def id(self) -> str:
        return self.spec["id"]

    @property
    def version(self) -> str:
        return self.spec["version"]

    @property
    def protocol_or_transport(self) -> str:
        return self.spec["protocol-or-transport"]

    @property
    def required_substrate_capabilities(self) -> list[str]:
        return list(self.spec.get("required-substrate-capabilities", []) or [])

    @property
    def declared_event_emissions(self) -> list[dict]:
        return list(self.spec.get("declared-event-emissions", []) or [])

    @property
    def declared_event_consumptions(self) -> list[dict]:
        return list(self.spec.get("declared-event-consumptions", []) or [])

    # ---------------------------------------------------------------
    # Workspace attachment (boot-ordering: post-Workspace construction)
    # ---------------------------------------------------------------

    def attach_workspace(self, workspace: Any) -> None:
        """Wire the workspace's event-emit callback into the adapter."""
        self._workspace = workspace
        self._emit_event = workspace._emit_event

    # ---------------------------------------------------------------
    # Stub MCP tool-call
    # ---------------------------------------------------------------

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Stub MCP tool-call: emit one `action` event, return canned response."""
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "adapter not attached to a workspace; call attach_workspace first"
            )
        self._outcome_counter += 1
        outcome_reference = f"mcp-stub-{self._outcome_counter}"
        params = parameters or {}
        actor_id = attributing_actor_id or next(
            iter(self._workspace._substrate.state.actors), None
        )
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": tool_name,
                "parameters": params,
                "outcome-reference": outcome_reference,
            },
        )
        return {
            "outcome-reference": outcome_reference,
            "ok": True,
            "stub": True,
            "tool": tool_name,
            "parameters": params,
        }


def load_adapter_from_provision(
    provision_ref: str, extensions_dir: Path
) -> MCPToolAdapter:
    """Load an adapter spec from a `<ext-id>:<provision-id>` ref.

    Mirrors `load_shape_from_provision` in shape.py.
    """
    from fresh_plan.validator.extensions import (
        discover_extensions,
        load_extension,
    )

    ext_id, prov_id = provision_ref.split(":", 1)
    discovered = discover_extensions(extensions_dir)
    if ext_id not in discovered:
        raise ValueError(
            f"adapter provision {provision_ref!r}: extension {ext_id!r} not discovered "
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
            f"adapter provision {provision_ref!r}: provision id {prov_id!r} not found "
            f"in any version of extension {ext_id!r}"
        )
    return MCPToolAdapter(spec=spec)
