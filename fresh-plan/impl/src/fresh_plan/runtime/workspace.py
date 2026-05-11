"""Workspace handle — user-facing API atop the InProcessSubstrate.

Per the B2 brief public API surface: `Workspace.boot(...)` is the
classmethod entry point; `with Workspace.boot(...) as ws:` enters a
context-managed lifecycle (shutdown event on exit). Actors are exposed
as ActorHandle objects so callers can emit events via natural calls.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional

from fresh_plan.runtime.substrate import Substrate
from fresh_plan.runtime.workspace_state import WORK_UNIT_STATUSES


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class ActorHandle:
    """Per-actor convenience for emitting events with the actor as attribution.

    Each emit_* method builds a properly-shaped event dict (chained off
    the current tail) and appends via the substrate. The substrate runs
    per-event D30 §4 + schema + chain-integrity checks; on failure the
    event is REJECTED (not appended) and an exception propagates per the
    B2 brief.
    """

    def __init__(self, workspace: "Workspace", actor_id: str) -> None:
        self._workspace = workspace
        self._actor_id = actor_id

    @property
    def id(self) -> str:
        return self._actor_id

    @property
    def record(self) -> dict:
        return self._workspace._substrate.state.get_actor(self._actor_id)

    # -------------- emit helpers (per D10 payload subtypes) --------------

    def emit_claim(
        self,
        assertion: str,
        confidence: Optional[str] = None,
        evidence_references: Optional[list[str]] = None,
        *,
        role: Optional[str] = None,
        work_unit_id: Optional[str] = None,
        event_id: Optional[str] = None,
    ) -> dict:
        payload: dict = {"assertion": assertion}
        if confidence is not None:
            payload["confidence"] = confidence
        if evidence_references is not None:
            payload["evidence-references"] = evidence_references
        return self._workspace._emit_event(
            actor_id=self._actor_id,
            payload_subtype="claim",
            payload=payload,
            role=role,
            work_unit_id=work_unit_id,
            event_id=event_id,
        )

    def emit_action(
        self,
        action_name: str,
        parameters: Optional[dict] = None,
        outcome_reference: Optional[str] = None,
        *,
        role: Optional[str] = None,
        work_unit_id: Optional[str] = None,
        event_id: Optional[str] = None,
    ) -> dict:
        payload: dict = {"action-name": action_name}
        if parameters is not None:
            payload["parameters"] = parameters
        if outcome_reference is not None:
            payload["outcome-reference"] = outcome_reference
        return self._workspace._emit_event(
            actor_id=self._actor_id,
            payload_subtype="action",
            payload=payload,
            role=role,
            work_unit_id=work_unit_id,
            event_id=event_id,
        )

    def emit_state_change(
        self,
        what: str,
        before: object = None,
        after: object = None,
        *,
        role: Optional[str] = None,
        work_unit_id: Optional[str] = None,
        event_id: Optional[str] = None,
    ) -> dict:
        payload: dict = {"what": what}
        if before is not None:
            payload["before"] = before
        if after is not None:
            payload["after"] = after
        return self._workspace._emit_event(
            actor_id=self._actor_id,
            payload_subtype="state-change",
            payload=payload,
            role=role,
            work_unit_id=work_unit_id,
            event_id=event_id,
        )


class WorkUnitHandle:
    """Per-work-unit handle: transition() emits a state-change event per D20."""

    def __init__(self, workspace: "Workspace", work_unit_id: str) -> None:
        self._workspace = workspace
        self._work_unit_id = work_unit_id

    @property
    def id(self) -> str:
        return self._work_unit_id

    @property
    def record(self) -> dict:
        return self._workspace._substrate.state.get_work_unit(self._work_unit_id)

    @property
    def status(self) -> str:
        return self.record["status"]

    def transition(
        self,
        to_status: str,
        *,
        attributing_actor_id: Optional[str] = None,
        role: Optional[str] = None,
    ) -> dict:
        """Transition this work-unit; emits a state-change event per D20.

        Per Bref closure of D39: the state mutation is performed by the
        projection on append (apply_event_to_state). We read the current
        status here only to carry it as `payload.before` on the event.
        """
        if to_status not in WORK_UNIT_STATUSES:
            raise ValueError(
                f"target status {to_status!r} not in core enum {sorted(WORK_UNIT_STATUSES)}"
            )
        from_status = self._workspace._substrate.state.get_work_unit(
            self._work_unit_id
        ).get("status")

        # Per D20: lifecycle transitions are events.
        actor_id = (
            attributing_actor_id
            or next(iter(self._workspace._substrate.state.actors), None)
        )
        return self._workspace._emit_event(
            actor_id=actor_id,
            payload_subtype="state-change",
            payload={
                "what": "work-unit-status",
                "before": from_status,
                "after": to_status,
            },
            role=role,
            work_unit_id=self._work_unit_id,
        )


class Workspace:
    """User-facing handle wrapping a Substrate.

    Lifecycle: created by `Workspace.boot(...)` (which fires the boot
    lifecycle-transition event); context-manager `__exit__` fires the
    shutdown lifecycle-transition event.

    Per the B2 brief + D41: this is the surface other code uses to
    interact with the running workspace, agnostic of the concrete
    Substrate subclass.
    """

    def __init__(self, substrate: Substrate, manifest: dict) -> None:
        self._substrate = substrate
        self._manifest = manifest
        self._actor_handles: dict[str, ActorHandle] = {
            aid: ActorHandle(self, aid) for aid in substrate.state.actors
        }
        self._work_unit_handles: dict[str, WorkUnitHandle] = {}
        self._shutdown_emitted = False
        self._event_id_counter = 0

    # ------------------------ classmethod entry ------------------------

    @classmethod
    def boot(
        cls,
        manifest: dict,
        extensions_dir: Path,
        schemas_dir: Optional[Path] = None,
    ) -> "Workspace":
        from fresh_plan.runtime.boot import boot_workspace

        return boot_workspace(manifest, extensions_dir, schemas_dir)

    # ------------------------ context-manager API ------------------------

    def __enter__(self) -> "Workspace":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.shutdown()

    def shutdown(self) -> None:
        """Emit the lifecycle-transition:shutdown event (idempotent)."""
        if self._shutdown_emitted:
            return
        first_actor_id = next(iter(self._substrate.state.actors), None)
        try:
            self._emit_event(
                actor_id=first_actor_id,
                payload_subtype="lifecycle-transition",
                payload={"transition-type": "shutdown", "trigger": "host-process"},
            )
        finally:
            self._shutdown_emitted = True

    # ------------------------ properties ------------------------

    @property
    def workspace_id(self) -> str:
        return self._substrate.workspace_id

    @property
    def runtime_shape(self) -> str:
        return self._substrate.runtime_shape

    @property
    def manifest(self) -> dict:
        return self._manifest

    @property
    def substrate(self) -> Substrate:
        return self._substrate

    @property
    def event_chain(self):
        return self._substrate.event_chain

    @property
    def hooks(self):
        return self._substrate.hooks

    @property
    def skills(self):
        return self._substrate.skills

    @property
    def current_scope(self) -> Optional[dict]:
        return self._substrate.state.current_scope

    @property
    def actors(self) -> dict[str, ActorHandle]:
        # Ensure handles are present for runtime-added actors too.
        for aid in self._substrate.state.actors:
            if aid not in self._actor_handles:
                self._actor_handles[aid] = ActorHandle(self, aid)
        return self._actor_handles

    @property
    def work_units(self) -> dict[str, WorkUnitHandle]:
        for wid in self._substrate.state.work_units:
            if wid not in self._work_unit_handles:
                self._work_unit_handles[wid] = WorkUnitHandle(self, wid)
        return self._work_unit_handles

    @property
    def adapters(self) -> dict:
        return self._substrate.adapter_instances

    def adapter(self, binding_id: str):
        """Return the adapter instance bound at `binding_id` (KeyError on miss)."""
        return self._substrate.adapter_instances[binding_id]

    @property
    def specialists(self) -> dict:
        return self._substrate.specialist_instances

    def specialist(self, binding_id: str):
        """Return the specialist instance bound at `binding_id` (KeyError on miss)."""
        return self._substrate.specialist_instances[binding_id]

    # ------------------------ work-unit + sub-agent ------------------------

    def create_work_unit(
        self,
        *,
        id: str,
        kind: str,
        payload: dict,
        contributing_actors: Optional[list[dict]] = None,
        contributing_specialists: Optional[list[str]] = None,
        attributing_actor_id: Optional[str] = None,
    ) -> WorkUnitHandle:
        """Create a work-unit in status=`created` and emit a state-change event.

        Per D20: status `created` is the entry state; richer lifecycle
        history derives from events filtered by work-unit-id. Per Bref
        closure of D39: the full work-unit record rides on
        `payload.after` so state_at(n) replay reconstructs the work-unit
        (not only by id, as before). State mutation happens via the
        projection on append; no direct state.add_work_unit here.
        Self-attestation in event.work-unit-id is admitted by the
        per-event check (the work-unit being created may reference
        itself before it exists in state).
        """
        wu = {
            "id": id,
            "kind": kind,
            "status": "created",
            "payload": payload,
            "contributing-actors": contributing_actors or [],
            "contributing-specialists": contributing_specialists or [],
            "lifecycle": {"created-at": _utcnow_iso()},
        }
        handle = WorkUnitHandle(self, id)
        self._work_unit_handles[id] = handle

        # Audit-trail per I3: every state mutation is an event.
        actor_id = attributing_actor_id or next(
            iter(self._substrate.state.actors), None
        )
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="state-change",
            payload={"what": "work-unit-created", "after": wu},
            work_unit_id=id,
        )
        return handle

    def register_agent_actor(
        self,
        *,
        id: str,
        substrate_binding: str,
        attributing_actor_id: Optional[str] = None,
    ) -> ActorHandle:
        """Register a sub-agent per D19; emits a composition-change event.

        Per D34 §A.5: actors added via composition-change become valid
        event targets *after* the composition-change is appended.

        Per D19: sub-agents are not a separate kind — they're agent-actors
        registered via composition-change. The substrate-binding must
        reference a known binding-id (D30 §4 boot-time check; we replay
        it here for runtime additions).
        """
        if substrate_binding not in self._substrate.known_binding_ids:
            raise ValueError(
                f"substrate-binding {substrate_binding!r} not in known binding-ids "
                f"{sorted(self._substrate.known_binding_ids)}"
            )

        actor_record = {
            "id": id,
            "subtype": "agent-actor",
            "substrate-binding": substrate_binding,
        }

        # Per D39: composition-change:add carries the full actor record in
        # `payload.record` so workspace state is fully derivable from the
        # event chain. Per D34 §A.5: the attributing actor (already in state)
        # appears in event.actors[]; the new actor is registered by the
        # substrate side-effect AFTER append, so it becomes a valid event
        # target for subsequent events.
        attributing = attributing_actor_id or next(
            iter(self._substrate.state.actors), None
        )
        self._emit_event(
            actor_id=attributing,
            payload_subtype="composition-change",
            payload={
                "change-type": "add",
                "binding-reference": id,
                "binding-kind": "actor",
                "record": actor_record,
            },
        )
        handle = ActorHandle(self, id)
        self._actor_handles[id] = handle
        return handle

    # ------------------------ internal: event builder ------------------------

    def _next_event_id(self) -> str:
        # Monotonic per-workspace internal counter; deterministic for tests.
        # event.id is an instance-identifier; the auto-generated form uses
        # the workspace-id prefix + counter.
        self._event_id_counter += 1
        return f"evt-{self._substrate.workspace_id}-{self._event_id_counter:06d}"

    def _emit_event(
        self,
        *,
        actor_id: Optional[str],
        payload_subtype: str,
        payload: dict,
        role: Optional[str] = None,
        work_unit_id: Optional[str] = None,
        event_id: Optional[str] = None,
    ) -> dict:
        """Build a chained event dict and append it via the substrate.

        Per D10: every event needs ≥1 actor. We require `actor_id` to be
        provided when there are any actors registered; if none are
        registered (impossible per workspace schema minItems=1, but
        defensive) we accept the event with an empty actors list — the
        substrate's schema check will reject it.
        """
        tail = self._substrate.event_chain.tail
        prev_id = tail["id"] if tail else None
        actor_entry: dict = {}
        if actor_id is not None:
            actor_entry["id"] = actor_id
        if role is not None:
            actor_entry["role"] = role
        event = {
            "id": event_id or self._next_event_id(),
            "prev-event": prev_id,
            "timestamp": _utcnow_iso(),
            "actors": [actor_entry] if actor_entry else [],
            "payload-subtype": payload_subtype,
            "payload": payload,
        }
        if work_unit_id is not None:
            event["work-unit-id"] = work_unit_id
        self._substrate.append_event(event)
        return event

    # ------------------------ iteration helpers ------------------------

    def events(self) -> Iterator[dict]:
        return iter(self._substrate.event_chain)

    def state_at(self, sequence_n: int):
        """Per D40 §A: workspace state derived from events 0..n.

        Pure-replay against a fresh state. Per Bref closure of D39,
        all state mutations are event-driven (manifest-actor seeding +
        work-unit creation/transition flow through the chain), so the
        replayed state matches the live state at the same sequence.
        """
        return self._substrate.event_chain.state_at(sequence_n)
