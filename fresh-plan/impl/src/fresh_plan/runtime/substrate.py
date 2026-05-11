"""InProcessSubstrate — the B2 in-process substrate runtime.

Per D12, a substrate hosts the agent loop and exposes interfaces
(capabilities) for other extensions to hook into. Per D17, the three
core abstract capabilities are `hooks`, `skills`, `event-streaming`.

Per the B2 design lock: this is the *in-process* substrate (no Claude
Agent SDK integration in B2; that's a follow-on). The substrate is
just a Python container that holds WorkspaceState + AppendOnlyEventChain
+ HookRegistry + SkillRegistry, plus the per-event D30 §4 runtime
checks invoked on every event append.

Per D12 binding resolution: substrates declare `runtime-shapes[]`; each
binding selects exactly one. The substrate instance tracks its bound
runtime-shape for state visibility; runtime-shape semantics beyond that
are implementation per D11.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from fresh_plan.runtime.event_chain import (
    AppendOnlyEventChain,
    MalformedEventError,
    apply_event_to_state,
)
from fresh_plan.runtime.hooks import HookRegistry
from fresh_plan.runtime.per_event_checks import (
    EventRejected,
    check_event_references,
)
from fresh_plan.runtime.skills import SkillRegistry
from fresh_plan.runtime.workspace_state import WorkspaceState
from fresh_plan.validator.schemas import SchemaStore

if TYPE_CHECKING:
    from fresh_plan.runtime.adapter import MCPToolAdapter
    from fresh_plan.runtime.shape import GenericShape


@dataclass
class InProcessSubstrate:
    """In-memory substrate container per D12 + D17.

    Capabilities advertised: `hooks`, `skills`, `event-streaming` (the
    three core abstract per D17). Additional extension-registered
    capabilities are out of scope for the B2 reference substrate.
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
    # None for fixtures that don't bind a real shape impl.
    shape: Optional["GenericShape"] = None

    # Adapter / specialist binding metadata stored for inspection by callers.
    # The B2 substrate does NOT execute adapters or specialists — those are
    # B4 / B5 / B6 workstreams. We store metadata so consumers can verify the
    # boot path resolved everything correctly.
    adapter_bindings: dict[str, dict] = field(default_factory=dict)
    specialist_bindings: dict[str, dict] = field(default_factory=dict)

    # Instantiated adapter runtimes per binding-id (B4: MCPToolAdapter).
    # Populated at boot step 7; workspace attached post-Workspace
    # construction (pre boot-lifecycle event) per B4 boot-ordering.
    adapter_instances: dict[str, "MCPToolAdapter"] = field(default_factory=dict)

    # ---------------------------------------------------------------
    # Event append (the integrity gate)
    # ---------------------------------------------------------------

    def append_event(self, event: dict) -> int:
        """Validate per D30 §4 runtime + chain integrity, then append.

        On per-event identity failure: raise EventRejected; event is not
        appended (per D30 timing-modes table).

        On schema / chain-integrity failure: raise MalformedEventError
        (also a rejection — event is not appended).

        Per D34 §A.5: identity is against current state; sub-agents added
        via composition-change events are valid event targets *after*
        their composition-change is appended. The substrate enforces this
        by:
          1. Running per-event identity checks against current state.
          2. Appending the event (so it's now part of state).
          3. For composition-change:add events, applying the composition
             mutation AFTER append (so subsequent events see the new
             state, but the composition-change event itself doesn't
             reference its own additions in `actors[]`).

        Step 3's ordering choice: the composition-change event records
        *who added* the new binding (actors[]), referencing actors that
        already exist; the new binding becomes visible to events appended
        *after* the composition-change.
        """
        # Per-event identity checks (D30 §4 runtime portion)
        ident_failures = check_event_references(
            event,
            self.state,
            self.registered_payload_subtypes,
            self.known_binding_ids,
        )
        if ident_failures:
            raise EventRejected(ident_failures)

        # Shape authority-binding check (D13). Skipped when no shape attached
        # (legacy fixtures binding `min-shape` etc.).
        if self.shape is not None:
            auth_failures = self.shape.check_authority(event, self.state)
            if auth_failures:
                raise EventRejected(auth_failures)

        # Schema + chain-integrity validation lives in the event chain.
        # MalformedEventError propagates to the caller; event is not
        # appended on raise.
        seq = self.event_chain.append(event, self.schema_store)

        # Apply runtime side effects of certain payload subtypes.
        self._apply_runtime_side_effects(event)

        return seq

    def _apply_runtime_side_effects(self, event: dict) -> None:
        """Apply state mutations driven by the event per D7 §3 + D10.

        Delegates to the canonical projection `apply_event_to_state`
        (shared with AppendOnlyEventChain.state_at(n)) so live-append
        and replay paths cannot diverge.

        Other composition-change targets (adapters / specialists added at
        runtime) are tracked but not 'bound' — B4-B6 owns runtime
        adapter / specialist registration.
        """
        apply_event_to_state(event, self.state)

    # ---------------------------------------------------------------
    # Capability advertisement
    # ---------------------------------------------------------------

    def has_capability(self, name: str) -> bool:
        return name in self.capabilities

    def declared_capabilities(self) -> list[str]:
        return list(self.capabilities)
