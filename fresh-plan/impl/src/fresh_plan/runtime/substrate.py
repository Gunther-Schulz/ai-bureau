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
from fresh_plan.validator.types import ValidationFailure


class SubscriberDispatchError(Exception):
    """Aggregated subscriber on_event exceptions per D47 §B.1.

    Raised after the outer subscriber-dispatch drain completes if any
    subscribing specialist's on_event raised during dispatch. Each failure
    is (specialist_id, event_id, exception). Cascade is NOT terminated by
    individual failures — subsequent subscribers continue to fire; the
    aggregate surfaces all failures at drain end.
    """

    def __init__(self, failures: list[tuple]) -> None:
        self.failures = failures
        msg = "; ".join(
            f"specialist={spec_id!r} event={evt_id!r}: {exc}"
            for spec_id, evt_id, exc in failures
        )
        super().__init__(msg or "subscriber dispatch failures")


class HookExecutionError(Exception):
    """Aggregated post-event-emit hook handler exceptions per D47 §B.2.

    Raised after the outer subscriber-dispatch drain completes if any
    post-event-emit handler raised during the drain. Each failure is
    (hook_name, handler_index, event_id, exception). Event(s) IS in chain
    + state per D10 + D39; only post-emit observation failed.

    Note: pre-event-emit handler raises do NOT collect here — they raise
    immediately as EventRejected(category="hook-handler") per D47 §B.2,
    rejecting the event before it lands in the chain.
    """

    def __init__(self, failures: list[tuple]) -> None:
        self.failures = failures
        msg = "; ".join(
            f"hook={name!r}[handler={idx}] event={evt_id!r}: {exc}"
            for name, idx, evt_id, exc in failures
        )
        super().__init__(msg or "hook execution failures")

if TYPE_CHECKING:
    from fresh_plan.runtime.adapter import Adapter
    from fresh_plan.runtime.persistence import PersistenceLayer
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
    registered_work_unit_kinds: set[str] = field(default_factory=set)
    # §B-4 (D62 §B cheap impl) — work-unit-kind payload schemas. Maps
    # qualified work-unit-kind id (`<ext-id>:<kind>`) → JSON Schema dict.
    # Populated at boot from validator's work_unit_kind_payload_schemas.
    # When a kind has no registered payload schema (spec-ref omitted /
    # unresolvable), per-event payload check no-ops for that kind.
    work_unit_kind_payload_schemas: dict[str, dict] = field(default_factory=dict)
    known_binding_ids: set[str] = field(default_factory=set)
    # Per D59 §B.1 — open-vocab payload-body registry per slot. Keys are
    # the four payload-slot identifiers; values are sets of qualified
    # `<ext-id>:<value>` strings registered by loaded extensions.
    registered_payload_vocabulary: dict[str, set[str]] = field(
        default_factory=lambda: {
            "claim.confidence": set(),
            "action.action-name": set(),
            "state-change.what": set(),
            "lifecycle-transition.trigger": set(),
        }
    )

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

    # Per D57 §B.1: opaque pass-through configuration dict from
    # composition.substrate-bindings[i].configuration. None when omitted.
    configuration: Optional[dict] = None

    # Per D70 §B (Phase C C2): optional JSONL persistence layer. None for
    # tests that don't need on-disk persistence (in-memory only); set by
    # boot.py step 4.5 when persistence is configured for the workspace.
    # When non-None, append_event mirrors each successful append to the
    # persistence file (POSIX-atomic append).
    persistence: Optional["PersistenceLayer"] = None

    # Per D44: subscriber dispatch is queued. The outermost append_event
    # drains; nested append_event calls (emitted from on_event) enqueue
    # without re-entering the drain. The loop backstop raises with a
    # diagnostic if a single drain exceeds `max_events_per_drain`.
    max_events_per_drain: int = 1000
    _dispatch_queue: deque = field(default_factory=deque, repr=False)
    _dispatching: bool = field(default=False, repr=False)

    # Per D47 §B.1 + B.2: subscriber on_event exceptions + post-event-emit
    # hook handler exceptions are collected into these lists during the
    # outer drain; aggregated errors raised after the drain completes.
    _subscriber_failures: list = field(default_factory=list, repr=False)
    _post_emit_failures: list = field(default_factory=list, repr=False)

    # ---------------------------------------------------------------
    # Event append (the integrity gate)
    # ---------------------------------------------------------------

    def append_event(self, event: dict) -> int:
        """Validate per D30 §4 runtime + chain integrity + D47 hook firing,
        then append.

        Per D44 + D47 + D52 ordered steps (synchronous through enqueue; queued
        dispatch via outer drain):

          1. per-event identity check (D30 §4 + D34 §A.5)
          2. shape authority check (D13)
          2.5. post-projection state validity check (D52 §B.1 NEW); for
             composition-change events affecting actors, simulates projection
             on copy of state + validates against shape.actor_requirements;
             EventRejected(category="composition-validity") on failure;
             event NOT appended; state NOT mutated
          3. pre-event-emit hook fire (D47 §B.2 NEW); handler raise →
             EventRejected(category="hook-handler"); event NOT appended
          4. event_chain.append (schema + chain integrity per D10)
          5. _apply_runtime_side_effects (projection per D39)
          6. enqueue for dispatch (D44 queued FIFO)
          7. post-event-emit hook fire (D47 §B.2 NEW); handler raise
             collected (NOT raised) — aggregated after outer drain
          8. (outer call only) drain queue (D44 backstop applies)
          9. (outer call only) raise aggregated SubscriberDispatchError +
             HookExecutionError if collection lists non-empty

        Per-event check / shape authority / pre-emit hook failures REJECT
        the event (event NOT in chain). Post-emit hook + subscriber
        on_event failures are POST-APPEND observation failures: event IS
        in chain + state; aggregated diagnostic surfaces after drain.
        """
        # Step 1: per-event identity check (D30 §4 + D34 §A.5; D51 §B.1 for
        # work-unit-creation-event per-work-unit identity; §B-3 + §B-7 for
        # event.actors[].role + work-unit contributing-actors[].role vocabulary
        # against shape's roles[] vocabulary when shape is bound).
        _shape_role_ids: Optional[set[str]] = None
        if self.shape is not None:
            _shape_role_ids = {
                r["id"]
                for r in self.shape.roles
                if isinstance(r, dict) and r.get("id")
            }
            if not _shape_role_ids:
                _shape_role_ids = None
        # Per D64 §B.1: build per-bound-specialist emissions vocabulary
        # map for emit-attribution check. Pure derivation from
        # specialist_instances; one dict-comp per emit (cheap; could
        # cache as a field if profiling shows hot path).
        specialist_emissions_map: dict[str, set[str]] = {
            bid: {
                e.get("payload-subtype")
                for e in sp.declared_event_emissions
                if e.get("payload-subtype")
            }
            for bid, sp in self.specialist_instances.items()
        }
        ident_failures = check_event_references(
            event,
            self.state,
            self.registered_payload_subtypes,
            self.known_binding_ids,
            known_specialist_binding_ids=self.specialist_bindings.keys(),
            registered_work_unit_kinds=self.registered_work_unit_kinds,
            registered_payload_vocabulary=self.registered_payload_vocabulary,
            shape_role_ids=_shape_role_ids,
            work_unit_kind_payload_schemas=self.work_unit_kind_payload_schemas
            or None,
            specialist_emissions_map=specialist_emissions_map,
        )
        if ident_failures:
            raise EventRejected(ident_failures)

        # Step 2: shape authority check (D13)
        if self.shape is not None:
            auth_failures = self.shape.check_authority(event, self.state)
            if auth_failures:
                raise EventRejected(auth_failures)

        # Step 2.5: post-projection state validity check (D52 §B.1)
        if self.shape is not None:
            comp_failures = self.shape.check_post_event_state_validity(
                event, self.state
            )
            if comp_failures:
                raise EventRejected(comp_failures)

        # Step 3: pre-event-emit hook fire (D47 §B.2 NEW CONTRACT)
        try:
            self.hooks.fire("pre-event-emit", {"event": event})
        except Exception as exc:
            raise EventRejected(
                [
                    ValidationFailure(
                        category="hook-handler",
                        path="hook[pre-event-emit]",
                        value=event.get("id"),
                        reason=(
                            f"pre-event-emit handler raised: {exc} — "
                            f"event NOT appended (chain integrity preserved)"
                        ),
                    )
                ]
            ) from exc

        # Step 4: chain append (assigns seq; D10 + D44)
        seq = self.event_chain.append(event, self.schema_store)

        # Step 4a (D70 §B Phase C C2): mirror successful append to JSONL
        # persistence layer when configured. IO error propagates — the
        # in-memory chain already contains the event (integrity preserved
        # per D10); the persistence write failure surfaces to caller via
        # PersistenceCorruptionError. Future Phase C+ refinement may
        # rollback the in-memory chain on persistence failure (per D70
        # §D D-2 deferral); current behavior keeps in-memory as
        # source-of-truth.
        if self.persistence is not None:
            self.persistence.save_event(event)

        # Step 5: projection (D39 state-from-events)
        self._apply_runtime_side_effects(event)

        # Step 6: enqueue for subscriber dispatch (D44 queued FIFO)
        if self.specialist_subscribers:
            self._dispatch_queue.append(event)

        # Step 7: post-event-emit hook fire (D47 §B.2 NEW CONTRACT)
        # Collect, don't raise — aggregated after outer drain completes.
        if self.hooks.handler_count("post-event-emit") > 0:
            try:
                self.hooks.fire(
                    "post-event-emit", {"event": event, "sequence": seq}
                )
            except Exception as exc:
                # HookRegistry.fire iterates handlers serially; on raise,
                # only the failing handler's exception surfaces. Index is
                # not knowable from the catch site without re-iterating;
                # captured as -1 (= "first-raising handler in registration
                # order"). Future probing audit may surface this as a gap;
                # acceptable for Phase B impl per D47 §D.
                self._post_emit_failures.append(
                    ("post-event-emit", -1, event.get("id"), exc)
                )

        # Nested call: outer drain handles aggregation; just return seq.
        if self._dispatching:
            return seq

        # Step 8: outer call drains the queue.
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

        # Step 9: aggregated error raise per D47 §C.
        sub_fail = self._subscriber_failures
        post_fail = self._post_emit_failures
        self._subscriber_failures = []
        self._post_emit_failures = []

        if sub_fail and post_fail:
            # Both visible via Python's exception chaining (__context__).
            try:
                raise HookExecutionError(post_fail)
            except HookExecutionError as he:
                raise SubscriberDispatchError(sub_fail) from he
        elif sub_fail:
            raise SubscriberDispatchError(sub_fail)
        elif post_fail:
            raise HookExecutionError(post_fail)

        return seq

    def _dispatch_event_to_subscribers(self, event: dict) -> None:
        """Fire on_event on each subscribing specialist with a matching subscription.

        Per D47 §B.1: subscriber exceptions captured into
        `self._subscriber_failures` rather than silently swallowed.
        Aggregated + raised as `SubscriberDispatchError` after the outer
        drain in `append_event` completes. Cascade is NOT terminated by
        individual failures — subsequent subscribers continue firing.
        """
        subtype = event.get("payload-subtype")
        payload = event.get("payload") or {}
        for sub in self.specialist_subscribers:
            # Per D55 §B.1: specialist-level gate evaluated BEFORE per-subscription
            # filter. If the predicate evaluates false, skip the specialist entirely.
            # Predicate-raise routes through D47 §B.1 SubscriberDispatchError
            # aggregation (existing 3-tuple shape) — cascade NOT terminated.
            predicate = getattr(sub, "_activation_predicate", None)
            if predicate is not None:
                try:
                    if not predicate(event):
                        continue
                except Exception as exc:
                    spec_id = (
                        sub.spec.get("id")
                        if hasattr(sub, "spec")
                        else type(sub).__name__
                    )
                    self._subscriber_failures.append(
                        (spec_id, event.get("id"), exc)
                    )
                    continue
            for subscription in sub.declared_event_subscriptions:
                if subscription.get("payload-subtype") != subtype:
                    continue
                qualifier = subscription.get("qualifier")
                if qualifier is not None and payload.get("qualifier") != qualifier:
                    continue
                try:
                    sub.on_event(event)
                except Exception as exc:
                    spec_id = (
                        sub.spec.get("id")
                        if hasattr(sub, "spec")
                        else type(sub).__name__
                    )
                    self._subscriber_failures.append(
                        (spec_id, event.get("id"), exc)
                    )
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


@dataclass
class ClaudeAgentSDKSubstrate(Substrate):
    """Phase C real-wire substrate using the Claude Agent SDK Python package.

    Per D68 §B.1 (substrate library lock) + D69 §B.1 (real-wire forward-bar +
    NEW `sdk-init` failure category). The Claude Agent SDK ships an
    async-only ``ClaudeSDKClient`` interface; this substrate wraps it in
    a synchronous boot/session lifecycle per D44 ("no async substrate model"
    at Phase C) using ``asyncio.run`` to drive the underlying coroutines.

    The SDK lives **inside** the substrate as ``_sdk_client``. Caller controls
    session lifecycle:

      - ``boot_workspace(...)`` returns the ``Workspace`` handle (per D7 boot
        procedure); no SDK session is started during boot.
      - Caller invokes ``substrate.start_session(prompt=...)`` to spin up an
        SDK session, drive one round-trip with the SDK, and translate SDK
        responses into framework events via ``append_event`` (existing
        integrity gate per D44 + D47 + D52).
      - Caller invokes ``substrate.stop_session()`` to release SDK resources
        (idempotent; safe to call when no session is active).

    Per D45 detection-surface-recovery triad applied to the ``sdk-init`` path:

      - **Detection** — any exception raised by the SDK during ``connect`` /
        ``query`` / response-streaming is caught by ``start_session``.
      - **Surface** — wrapped as ``WorkspaceBootError`` carrying
        ``ValidationFailure(category="sdk-init", path="substrate.session.start",
        value=<sdk-class-name>, reason=<diagnostic>)`` with the original SDK
        exception chained via ``from`` for full diagnostic visibility.
        ``WorkspaceBootError`` is reused (not a new exception type) because
        ``sdk-init`` failures share the abort-and-discard semantics of boot
        failures — the session never fully started, no observable state
        survives.
      - **Recovery** — caller catches ``WorkspaceBootError``, inspects the
        ``sdk-init`` category, decides retry vs abort. Substrate is left in a
        clean state: ``_sdk_client`` is None and ``stop_session`` is a no-op.

    Per scope-cut C12 (autopilot constraint): tests use a monkeypatched SDK
    client (no real Anthropic API calls). The ``_sdk_client_factory`` class
    attribute defaults to ``claude_agent_sdk.ClaudeSDKClient``; tests
    subclass and override the factory to inject a fake client whose
    ``connect`` / ``receive_response`` / ``disconnect`` behaviors are
    controlled by the test.

    Per D69 §D D-1: SDK callback signatures (specifically the
    ``receive_response`` async iterator yielding ``Message`` subclasses) are
    verified against ``claude_agent_sdk.client.ClaudeSDKClient`` 0.2.82.
    Future SDK version bumps may require adapter changes; the
    verify-at-workstream-start discipline (D68 §B.3) re-grounds the SDK API
    claim at each Phase C workstream consuming it.
    """

    # Per-instance SDK state. Set during start_session; cleared by stop_session.
    _sdk_client: Optional[object] = field(default=None, repr=False)
    _session_active: bool = field(default=False, repr=False)

    # Class-level factory hook for test injection. Default: real SDK class.
    # Tests override at subclass level to inject a fake client with controlled
    # connect/receive_response/disconnect semantics (per scope-cut C12 — no
    # real Anthropic API calls in autopilot loop).
    _sdk_client_factory: Optional[object] = field(default=None, repr=False)

    # ---------------------------------------------------------------
    # Session lifecycle (Phase C real-wire — D69 §B.1)
    # ---------------------------------------------------------------

    def _resolve_sdk_client_factory(self) -> object:
        """Return the SDK client factory — instance override, else SDK default.

        Resolution order:
          1. ``self._sdk_client_factory`` if set (test injection / subclass).
          2. ``claude_agent_sdk.ClaudeSDKClient`` resolved lazily on first use.

        Import is lazy so the framework doesn't hard-require the SDK at
        import time. SDK missing at start_session → ImportError surfaces as
        sdk-init failure.
        """
        if self._sdk_client_factory is not None:
            return self._sdk_client_factory
        try:
            from claude_agent_sdk import ClaudeSDKClient
        except ImportError as exc:
            raise WorkspaceBootError_sdk_init(
                self,
                detail=f"claude-agent-sdk import failed: {exc}",
                cause=exc,
            )
        return ClaudeSDKClient

    def start_session(
        self,
        prompt: Optional[str] = None,
        options: Optional[object] = None,
    ) -> list[int]:
        """Start an SDK session, drive one round-trip, emit events.

        Per D69 §B.1 + D44 no-async-substrate-model: synchronously wraps the
        SDK's async lifecycle (``connect`` → optional ``query`` → drain
        ``receive_response`` → translate to events) using ``asyncio.run``.

        SDK responses are translated to framework events via ``append_event``
        — preserving D10 chain integrity + D44 queued subscriber dispatch +
        D47 hook firing + D52 composition-validity checks. The first
        manifest actor (any registered ``agent-actor`` subtype) is the
        attribution; if no agent actor is present, the first registered
        actor is used as a fallback.

        Args:
            prompt: optional initial prompt to send via ``client.query``.
                When None, the session opens with no initial message
                (caller may interact via subsequent calls — though Phase C
                scope is one round-trip per start_session).
            options: optional ``ClaudeAgentOptions`` instance forwarded to
                the SDK client constructor. None lets the SDK use defaults.

        Returns:
            List of event sequence numbers appended during this session
            (length matches the number of SDK messages translated to events;
            empty list when no messages flowed before disconnect).

        Raises:
            WorkspaceBootError: category ``sdk-init`` on SDK init / auth /
                connection failure (caught from ``connect`` / ``query`` /
                ``receive_response``). The substrate is left in a clean
                state (``_sdk_client`` is None; ``_session_active`` False).
        """
        import asyncio

        if self._session_active:
            raise WorkspaceBootError_sdk_init(
                self,
                detail="start_session called while session already active",
                cause=None,
            )

        factory = self._resolve_sdk_client_factory()
        try:
            client = factory(options=options) if options is not None else factory()
        except Exception as exc:
            raise WorkspaceBootError_sdk_init(
                self,
                detail=f"SDK client construction failed: {exc}",
                cause=exc,
            )
        self._sdk_client = client
        self._session_active = True

        emitted_seqs: list[int] = []

        async def _drive() -> None:
            await client.connect(prompt if isinstance(prompt, str) else None)
            if prompt is not None and not isinstance(prompt, str):
                # Streaming-mode prompt (per ClaudeSDKClient.connect contract).
                pass
            elif prompt is None:
                # No initial prompt; session connected but idle. Caller may
                # invoke subsequent operations OR immediately stop_session.
                return
            async for message in client.receive_response():
                event = self._translate_sdk_message_to_event(message)
                if event is not None:
                    seq = self.append_event(event)
                    emitted_seqs.append(seq)

        # Lazy import — avoids module-load circular dep (boot imports substrate).
        from fresh_plan.runtime.boot import WorkspaceBootError as _WBE
        from fresh_plan.runtime.event_chain import MalformedEventError as _MEE
        try:
            asyncio.run(_drive())
        except (_WBE, _MEE, EventRejected, SubscriberDispatchError,
                HookExecutionError):
            # Framework-level rejections from append_event during translation
            # (per-event check / authority / composition-validity / hook /
            # subscriber dispatch). Surface unchanged — distinct from
            # sdk-init failures. The SDK round-trip succeeded; the framework
            # rejected the resulting event.
            self._cleanup_session_state()
            raise
        except Exception as exc:
            # SDK-side failure (connect / query / receive_response) OR
            # unexpected exception during translation. Wrap as sdk-init per
            # D69 §B.1 triad.
            self._cleanup_session_state()
            raise WorkspaceBootError_sdk_init(
                self,
                detail=f"SDK session failed: {exc}",
                cause=exc,
            )
        return emitted_seqs

    def stop_session(self) -> None:
        """Release SDK resources. Idempotent — safe to call without a session.

        Per D69 §B.1 recovery contract: leaves the substrate in a clean
        state. If the SDK ``disconnect`` raises, the exception surfaces to
        the caller (sdk-init failures during teardown are still sdk-init
        per the triad — caller decides whether to retry or abort the
        workspace). After stop_session returns (success or raise), the
        substrate's ``_sdk_client`` is None and a subsequent ``start_session``
        is valid.
        """
        import asyncio

        client = self._sdk_client
        if client is None:
            return

        async def _drive_disconnect() -> None:
            await client.disconnect()

        try:
            asyncio.run(_drive_disconnect())
        except Exception as exc:
            self._cleanup_session_state()
            raise WorkspaceBootError_sdk_init(
                self,
                detail=f"SDK disconnect failed: {exc}",
                cause=exc,
            )
        self._cleanup_session_state()

    def _cleanup_session_state(self) -> None:
        """Reset SDK fields. Internal — called by start_session/stop_session.
        """
        self._sdk_client = None
        self._session_active = False

    def _translate_sdk_message_to_event(
        self, message: object
    ) -> Optional[dict]:
        """Translate one SDK message to a framework event dict, or None.

        Per D69 §B.1 + D10 chain integrity: each translatable SDK message
        becomes one ``action`` event attributed to the first registered
        actor in workspace state. Non-translatable messages (system /
        rate-limit / stream-control) return None and are not appended.

        SDK message taxonomy (per claude_agent_sdk.types 0.2.82):
          - UserMessage / AssistantMessage / SystemMessage / ResultMessage /
            StreamEvent / RateLimitEvent.

        Phase C C1 scope: translate AssistantMessage + UserMessage +
        ResultMessage as ``action`` events with structured payload (per the
        ``msg_class_name in {...}`` set below). Other shapes return None.
        Per D-1 (future Phase C+ refinement): finer-grained mapping
        (tool-use → adapter.call action events; tool-result → state-change
        events; thinking-blocks → claim events) lands as the contract surface
        sharpens. C1 keeps translation minimal — proves the round-trip
        without over-committing to a message-taxonomy contract that the
        SDK may evolve.
        """
        # Use duck-typing rather than isinstance to keep tests SDK-import-free.
        msg_class_name = type(message).__name__

        # Identify attribution actor (first agent-actor, else first actor).
        attribution_id: Optional[str] = None
        for actor_id, actor_rec in self.state.actors.items():
            if actor_rec.get("subtype") == "agent-actor":
                attribution_id = actor_id
                break
        if attribution_id is None and self.state.actors:
            attribution_id = next(iter(self.state.actors.keys()))
        if attribution_id is None:
            # No actor to attribute the event to — translate-and-skip rather
            # than crash. Phase C+ may surface this as a structured warning;
            # C1 keeps it silent to preserve the round-trip happy path.
            return None

        prev_id = self.event_chain.tail["id"] if self.event_chain.tail else None
        from datetime import datetime, timezone

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        event_id = (
            f"evt-sdk-{msg_class_name.lower()}-{len(self.event_chain)}-"
            f"{self.workspace_id}"
        )

        if msg_class_name in {"AssistantMessage", "UserMessage", "ResultMessage"}:
            return {
                "id": event_id,
                "prev-event": prev_id,
                "timestamp": timestamp,
                "actors": [{"id": attribution_id}],
                "payload-subtype": "action",
                "payload": {
                    "action-name": "claude-agent-sdk-substrate-ext:sdk-message",
                    # Per action-payload-schema additionalProperties=false:
                    # the SDK message class is stashed inside `parameters`
                    # (free-form object slot per action.schema.json).
                    "parameters": {"sdk-message-class": msg_class_name},
                },
            }
        return None


def WorkspaceBootError_sdk_init(
    substrate: "ClaudeAgentSDKSubstrate",
    *,
    detail: str,
    cause: Optional[BaseException],
) -> "WorkspaceBootError":
    """Construct a WorkspaceBootError carrying the sdk-init ValidationFailure.

    Per D69 §B.1 surface contract — wraps SDK failures with structured
    ValidationFailure(category='sdk-init'); chains the original exception
    via Python's ``from`` clause so callers see the SDK-side root cause.
    Helper function (not a method) so it can be called by both instance
    paths and (in principle) external callers wanting to construct the
    error shape from outside the substrate.
    """
    from fresh_plan.runtime.boot import WorkspaceBootError as _WBE

    factory = substrate._sdk_client_factory
    factory_name = (
        getattr(factory, "__name__", repr(factory))
        if factory is not None
        else "claude_agent_sdk.ClaudeSDKClient"
    )
    err = _WBE(
        [
            ValidationFailure(
                category="sdk-init",
                path="substrate.session.start",
                value=factory_name,
                reason=detail,
            )
        ]
    )
    if cause is not None:
        err.__cause__ = cause
    return err


# Module-level registry of (substrate.id → runtime class). Populated as new
# substrate impls land. Phase C real-wire impls replace stub classes here.
_SUBSTRATE_CLASSES: dict[str, type[Substrate]] = {
    "claude-agent-sdk-substrate": ClaudeAgentSDKSubstrate,
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
    configuration: Optional[dict] = None,
) -> Substrate:
    """Load a substrate spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.id` to the registered runtime class. Raises
    ValueError if the spec's id has no registered runtime class (boot.py
    wraps as ``category="resolution"``). Constructor-raises are caught
    at boot.py and wrapped as ``category="configuration-rejected"`` per
    D57 §B.1.
    """
    from fresh_plan.runtime.provision import ProvisionResolutionError

    spec = load_provision_spec(provision_ref, extensions_dir)
    substrate_id = spec.get("id")
    cls = _SUBSTRATE_CLASSES.get(substrate_id)
    if cls is None:
        raise ProvisionResolutionError(
            f"substrate provision {provision_ref!r}: spec id {substrate_id!r} "
            f"has no registered Substrate runtime class"
        )
    return cls(
        workspace_id=workspace_id,
        runtime_shape=runtime_shape,
        schema_store=schema_store,
        capabilities=list(capabilities),
        configuration=configuration,
    )
