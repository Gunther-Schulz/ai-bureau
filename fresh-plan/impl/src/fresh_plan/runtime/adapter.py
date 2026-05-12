"""Adapter runtime — D16 + adapter.schema.json + D29 protocol-identifier registration.

Per D16, adapters integrate a workspace with external surfaces via a single
protocol-or-transport (extension-registered per D2 strict reading + D29
namespacing). `Adapter` is the base class reading off D16; concrete adapter
impls subclass it.

The base supports the **request/response invocation shape** (per D16's
"request/response tool" pattern) via `call(tool_name, parameters)`.
Delegation peer + passive event source patterns may require alternative
invocation interfaces — re-evaluate when first non-request/response impl
lands (Phase C+).

For Phase B, both shipped adapters (MCPToolAdapter, future DirectAPIAdapter)
are stubs: they emit one `action` event per call() and return a canned
response. Real-wire protocol implementations are Phase C territory.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ClassVar, Optional

from fresh_plan.runtime.provision import load_provision_spec


class AdapterCallError(Exception):
    """Adapter ``call()`` runtime failure per D48 §B.1 (adapter cluster supersedes per D45 §C).

    Phase C real-wire forward-bar: real-wire adapter impls (subclasses of
    ``Adapter`` overriding ``call()``) SHALL raise this on protocol /
    transport / auth / timeout / upstream failures. Phase B stubs do not
    trigger this exception — the contract is defined now so Phase C impls
    have a clear bar to meet rather than a happy-path-only example to
    reverse-engineer from.

    Composes with D47 §B.1 SubscriberDispatchError aggregation: when
    AdapterCallError fires from inside a specialist's ``on_event``
    (subscriber-dispatch path per D37 + D44), it is captured per D47 §B.1
    into substrate's ``_subscriber_failures`` (substrate.py:310-320) and
    aggregated as SubscriberDispatchError after the outer drain.

    Per D48 §D D-1: call-lifecycle raise-point (before-wire / mid-wire /
    after-wire) is per-real-wire-impl choice. Per D48 §D D-3: starter
    category vocabulary (transport / auth / timeout / protocol-error /
    upstream-error / unknown) is HTTP/JSON-RPC-shaped; non-HTTP transports
    register additional categories per D29 namespacing.
    """

    def __init__(
        self,
        *,
        adapter_id: str,
        call_target: str,
        category: str,
        detail: Optional[dict] = None,
    ) -> None:
        self.adapter_id = adapter_id
        self.call_target = call_target
        self.category = category
        self.detail = dict(detail) if detail else {}
        super().__init__(
            f"[{category}] adapter={adapter_id!r} target={call_target!r}: {self.detail}"
        )


@dataclass
class Adapter:
    """Base class for adapter runtime impls per D16 + adapter.schema.json.

    Holds the loaded spec, exposes D16 slot accessors, manages workspace
    attachment + event-emit infrastructure. Subclasses override `call()` to
    implement protocol-specific invocation.
    """

    spec: dict
    _emit_event: Optional[Callable[..., dict]] = field(default=None, repr=False)
    _workspace: Any = field(default=None, repr=False)
    _outcome_counter: int = field(default=0, repr=False)

    # Subclasses override to give their outcome-references a distinct prefix.
    _outcome_prefix: ClassVar[str] = "stub"

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
    # Convenience for request/response stub + real impls
    # ---------------------------------------------------------------

    def _emit_action(
        self,
        tool_name: str,
        parameters: dict,
        attributing_actor_id: Optional[str] = None,
    ) -> str:
        """Emit one `action` event for a tool-call invocation; return its outcome-reference."""
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "adapter not attached to a workspace; call attach_workspace first"
            )
        self._outcome_counter += 1
        outcome_reference = f"{self._outcome_prefix}-{self._outcome_counter}"
        actor_id = attributing_actor_id or next(
            iter(self._workspace._substrate.state.actors), None
        )
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": tool_name,
                "parameters": parameters,
                "outcome-reference": outcome_reference,
            },
        )
        return outcome_reference

    # ---------------------------------------------------------------
    # Invocation interface (abstract; subclass-owned)
    # ---------------------------------------------------------------

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        """Invoke this adapter for a tool-call. Subclasses MUST override."""
        raise NotImplementedError("Adapter subclasses must implement call()")


@dataclass
class MCPToolAdapter(Adapter):
    """Stub MCP-server-protocol adapter per D16 + B4.

    No real MCP wire is opened; `call()` emits one `action` event into the
    workspace event chain and returns a canned response carrying the
    outcome-reference. Phase C replaces the body with a real JSON-RPC
    client.
    """

    _outcome_prefix: ClassVar[str] = "mcp-stub"

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        params = parameters or {}
        outcome_reference = self._emit_action(tool_name, params, attributing_actor_id)
        return {
            "outcome-reference": outcome_reference,
            "ok": True,
            "stub": True,
            "tool": tool_name,
            "parameters": params,
        }


@dataclass
class DirectAPIAdapter(Adapter):
    """Stub direct-api adapter per D16 + B5.

    The non-MCP request/response path: an in-process direct call, no
    protocol wrapper. `call()` emits one `action` event and returns a
    canned response. Phase C / Phase D replace the body with real
    direct-call dispatch into target Python APIs.
    """

    _outcome_prefix: ClassVar[str] = "direct-stub"

    def call(
        self,
        tool_name: str,
        parameters: Optional[dict] = None,
        *,
        attributing_actor_id: Optional[str] = None,
    ) -> dict:
        params = parameters or {}
        outcome_reference = self._emit_action(tool_name, params, attributing_actor_id)
        return {
            "outcome-reference": outcome_reference,
            "ok": True,
            "stub": True,
            "kind": "direct-api",
            "tool": tool_name,
            "parameters": params,
        }


# Module-level registry of (protocol-or-transport → runtime class). Populated
# as new adapter impls land. Phase C real-wire impls replace stub classes here.
_ADAPTER_CLASSES: dict[str, type[Adapter]] = {
    "mcp-server-ext:mcp-client": MCPToolAdapter,
    "direct-api-ext:direct-api": DirectAPIAdapter,
}


def load_adapter_from_provision(
    provision_ref: str, extensions_dir: Path
) -> Adapter:
    """Load an adapter spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.protocol-or-transport` to the registered runtime
    class. Raises ValueError if the spec uses a protocol-or-transport with
    no registered runtime class.
    """
    spec = load_provision_spec(provision_ref, extensions_dir)
    protocol = spec.get("protocol-or-transport")
    cls = _ADAPTER_CLASSES.get(protocol)
    if cls is None:
        raise ValueError(
            f"adapter provision {provision_ref!r}: protocol-or-transport "
            f"{protocol!r} has no registered Adapter runtime class"
        )
    return cls(spec=spec)
