"""Substrate runtime — D12 + D17 + D41 two-substrate parity for Phase B.

Per D12, a substrate hosts the agent loop and exposes interfaces
(capabilities) for other extensions to hook into. Per D17 (renamed by
D43), the three core abstract capabilities are `hooks`, `skills`,
`event-chain`.

Per D41 Phase B closure: two substrate impls ship in Phase B —
InProcessSubstrate (B2) + MSAgentFrameworkSubstrate (B2b). Both are
stubs at Phase B; their existence proves the D12 contract is satisfiable
by more than one named-framework alignment. Real-wire integration is
Phase C.

Per D12 binding resolution: substrates declare `runtime-shapes[]`; each
binding selects exactly one. The substrate instance tracks its bound
runtime-shape for state visibility; runtime-shape semantics beyond that
are implementation per D11.

Per D44 (extends D37): subscriber dispatch is queued. Append + projection
+ chain integrity remain synchronous (preserves D10 + D39 + D40 §A);
subscribers' on_event fires from a FIFO drain at the outermost
append_event call. Nested append_event calls (emitted from inside
on_event) just enqueue the new event for dispatch. A loop backstop
(`max_events_per_drain`, default 1000) raises with a diagnostic if a
single drain exceeds the limit, so genuine infinite loops surface fast.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from fresh_plan.runtime.event_chain import (
    AppendOnlyEventChain,
    apply_event_to_state,
)
from fresh_plan.runtime.hooks import HookRegistry
from fresh_plan.runtime.per_event_checks import (
    EventRejected,
    check_event_references,
)
from fresh_plan.runtime.provision import load_provision_spec
from fresh_plan.runtime.skills import SkillRegistry
from fresh_plan.runtime.workspace_state import WorkspaceState
from fresh_plan.validator.schemas import SchemaStore

if TYPE_CHECKING:
    from fresh_plan.runtime.adapter import Adapter
    from fresh_plan.runtime.shape import Shape
    from fresh_plan.runtime.specialist import Specialist


@dataclass
class Substrate:
    """Base class for substrate runtime impls per D12 + D17.

    Holds the workspace event chain + state + hook/skill registries,
    enforces the per-event D30 §4 runtime checks + D13 shape authority-
    binding check on every append, and dispatches matching events into
    subscribed specialists per D37. Subclasses override behavior only
    when real-wire integration diverges from the in-process baseline;
    Phase B stubs share the base behavior unchanged.
    """

    workspace_id: str
    runtime_shape: str
    schema_store: SchemaStore

    # Core data structures
    state: WorkspaceState = field(default_factory=WorkspaceState)
    event_chain: AppendOnlyEventChain = field(default_factory=AppendOnlyEventChain)
    hooks: HookRegistry = field(default_factory=HookRegistry)
    skills: SkillRegistry = field(default_factory=SkillRegistry)

    # Runtime registries derived from loaded extensions (B1 returns
    # vocabulary_tables at boot success — substrate copies the relevant
    # slices here for per-event checks).
    registered_payload_subtypes: set[str] = field(default_factory=set)
    known_binding_ids: set[str] = field(default_factory=set)

    # Capabilities advertised; populated from the resolved substrate provision.
    capabilities: list[str] = field(default_factory=list)

    # Shape policy bundle (D13) attached at boot when composition.shape resolves.
    shape: Optional["Shape"] = None

    # Adapter / specialist binding metadata stored for inspection by callers.
    adapter_bindings: dict[str, dict] = field(default_factory=dict)
    specialist_bindings: dict[str, dict] = field(default_factory=dict)

    # Instantiated adapter runtimes per binding-id (B4 / B5).
    adapter_instances: dict[str, "Adapter"] = field(default_factory=dict)

    # Instantiated specialist runtimes per binding-id (B6 + D19).
    # `specialist_subscribers` duplicates the values list for the
    # append_event hot path (D37 event-driven coordination).
    specialist_instances: dict[str, "Specialist"] = field(default_factory=dict)
    specialist_subscribers: list["Specialist"] = field(default_factory=list)

    # Per D44: subscriber dispatch is queued. The outermost append_event
    # drains; nested append_event calls (emitted from on_event) enqueue
    # without re-entering the drain. The loop backstop raises with a
    # diagnostic if a single drain exceeds `max_events_per_drain`.
    max_events_per_drain: int = 1000
    _dispatch_queue: deque = field(default_factory=deque, repr=False)
    _dispatching: bool = field(default=False, repr=False)

    # ---------------------------------------------------------------
    # Event append (the integrity gate)
    # ---------------------------------------------------------------

    def append_event(self, event: dict) -> int:
        """Validate per D30 §4 runtime + chain integrity, then append.

        Per D44 (extends D37): per-event check + shape authority + schema
        + chain integrity + state projection all run synchronously
        (preserves D10 chain order + D39 state-from-events + D40 §A
        replay equivalence). Subscriber dispatch is queued — the
        outermost append_event call drains the queue FIFO; nested
        append_event calls (from inside on_event) enqueue without
        re-entering the drain. A loop backstop raises with a diagnostic
        if a single drain exceeds `max_events_per_drain`.

        On per-event identity failure: raise EventRejected; event is not
        appended (per D30 timing-modes table).

        On schema / chain-integrity failure: raise MalformedEventError
        (also a rejection — event is not appended).

        Per D34 §A.5: identity is against current state; sub-agents added
        via composition-change events are valid event targets *after*
        their composition-change is appended.
        """
        ident_failures = check_event_references(
            event,
            self.state,
            self.registered_payload_subtypes,
            self.known_binding_ids,
        )
        if ident_failures:
            raise EventRejected(ident_failures)

        if self.shape is not None:
            auth_failures = self.shape.check_authority(event, self.state)
            if auth_failures:
                raise EventRejected(auth_failures)

        seq = self.event_chain.append(event, self.schema_store)

        self._apply_runtime_side_effects(event)

        if not self.specialist_subscribers:
            return seq

        # Queued dispatch (D44). Nested calls just enqueue; the outermost
        # call owns the drain.
        self._dispatch_queue.append(event)
        if self._dispatching:
            return seq
        self._dispatching = True
        try:
            n_dispatched = 0
            while self._dispatch_queue:
                n_dispatched += 1
                if n_dispatched > self.max_events_per_drain:
                    offender = self._dispatch_queue[0]
                    self._dispatch_queue.clear()
                    raise RuntimeError(
                        f"subscriber-dispatch drain exceeded "
                        f"{self.max_events_per_drain} events; likely "
                        f"infinite loop. Last event in flight: "
                        f"id={offender.get('id')!r} "
                        f"payload-subtype={offender.get('payload-subtype')!r}"
                    )
                e = self._dispatch_queue.popleft()
                self._dispatch_event_to_subscribers(e)
        finally:
            self._dispatching = False
        return seq

    def _dispatch_event_to_subscribers(self, event: dict) -> None:
        """Fire on_event on each subscribing specialist with a matching subscription."""
        subtype = event.get("payload-subtype")
        payload = event.get("payload") or {}
        for sub in self.specialist_subscribers:
            for subscription in sub.declared_event_subscriptions:
                if subscription.get("payload-subtype") != subtype:
                    continue
                qualifier = subscription.get("qualifier")
                if qualifier is not None and payload.get("qualifier") != qualifier:
                    continue
                try:
                    sub.on_event(event)
                except Exception:
                    pass
                break

    def _apply_runtime_side_effects(self, event: dict) -> None:
        """Apply state mutations driven by the event per D7 §3 + D10.

        Delegates to the canonical projection `apply_event_to_state`
        (shared with AppendOnlyEventChain.state_at(n)) so live-append
        and replay paths cannot diverge.
        """
        apply_event_to_state(event, self.state)

    # ---------------------------------------------------------------
    # Capability advertisement
    # ---------------------------------------------------------------

    def has_capability(self, name: str) -> bool:
        return name in self.capabilities

    def declared_capabilities(self) -> list[str]:
        return list(self.capabilities)


@dataclass
class InProcessSubstrate(Substrate):
    """First concrete substrate impl per D12 — in-memory Python harness; no
    real LLM wire; provides B2/B6 stub behavior. Phase C real-wire integration
    (e.g., Claude Agent SDK) extends or replaces this.
    """


@dataclass
class MSAgentFrameworkSubstrate(Substrate):
    """MS Agent Framework substrate stub per B2b / D41.

    Behaviorally identical to InProcessSubstrate at Phase B stub level;
    declared separately to satisfy two-substrate parity (proves D17
    capability vocabulary is concept-substantiated by a non-Claude-shape
    framework, even if names lean Claude-flavored — see Bref). Phase C
    real-wire integration would map MS Agent Framework primitives
    (workflows + agents + middleware + tools + checkpointing) onto the
    Substrate contract surface.
    """


# Module-level registry of (substrate.id → runtime class). Populated as new
# substrate impls land. Phase C real-wire impls replace stub classes here.
_SUBSTRATE_CLASSES: dict[str, type[Substrate]] = {
    "inprocess-substrate": InProcessSubstrate,
    "ms-agent-framework-substrate": MSAgentFrameworkSubstrate,
}


def load_substrate_from_provision(
    provision_ref: str,
    extensions_dir: Path,
    *,
    workspace_id: str,
    runtime_shape: str,
    schema_store: SchemaStore,
    capabilities: list[str],
) -> Substrate:
    """Load a substrate spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.id` to the registered runtime class. Raises
    ValueError if the spec's id has no registered runtime class.
    """
    spec = load_provision_spec(provision_ref, extensions_dir)
    substrate_id = spec.get("id")
    cls = _SUBSTRATE_CLASSES.get(substrate_id)
    if cls is None:
        raise ValueError(
            f"substrate provision {provision_ref!r}: spec id {substrate_id!r} "
            f"has no registered Substrate runtime class"
        )
    return cls(
        workspace_id=workspace_id,
        runtime_shape=runtime_shape,
        schema_store=schema_store,
        capabilities=list(capabilities),
    )
