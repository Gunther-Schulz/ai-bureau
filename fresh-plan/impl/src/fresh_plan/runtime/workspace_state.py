"""Workspace state: actor registry, work-unit tracker, scope (per D7 §3).

Per D7 §3, workspace state is `events + work-units + scope`. The event
chain lives in `event_chain.py`; this module holds the other two
buckets plus the actor registry.

Per D7 §4 + D34 §A.5: composition is mutable; runtime-added actors
(sub-agents per D19) join via `composition-change` events. Identity
resolution checks (D30 §4 runtime portion) resolve against the
current state — not the boot-time manifest snapshot. This module's
`add_actor` is the runtime mutation path that keeps the registry in
sync with applied composition-change events.

Per D20: work-units have a fixed core lifecycle status enum
(`created` / `in-progress` / `paused` / `completed` / `abandoned`).
Transitions are validated; framework does not constrain the *conditions*
for transitions (shape / specialist concern).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# Per D20 — fixed core lifecycle status enum. Extensions cannot add states.
WORK_UNIT_STATUSES = frozenset(
    {"created", "in-progress", "paused", "completed", "abandoned"}
)


class UnknownActorError(KeyError):
    """Raised when a referenced actor id is not in the registry."""


class DuplicateActorError(ValueError):
    """Raised when registering an actor whose id is already known."""


class UnknownWorkUnitError(KeyError):
    """Raised when a referenced work-unit id is not in the tracker."""


class InvalidWorkUnitTransitionError(ValueError):
    """Raised when a work-unit transition targets an unknown status."""


@dataclass
class WorkspaceState:
    """In-memory state: actors + work-units + scope.

    Per B2 design lock: in-memory only. Persistence is deferred to a
    follow-on workstream (D7 §3 says state survives runtime episodes;
    that survival mechanism is implementation per D11 and out of scope
    for B2).
    """

    actors: dict[str, dict] = field(default_factory=dict)
    work_units: dict[str, dict] = field(default_factory=dict)
    current_scope: Optional[dict] = None

    # -----------------------------------------------------------------
    # Actor registry (per D9; manifest-declared + runtime-added per D19)
    # -----------------------------------------------------------------

    def add_actor(self, actor: dict) -> None:
        """Register an actor. Used at boot for manifest-declared actors AND
        at runtime when a `composition-change` event adds a sub-agent
        (per D19; per D34 §A.5 identity resolution is against current state).
        """
        aid = actor.get("id")
        if aid is None:
            raise ValueError("actor must have id")
        if aid in self.actors:
            raise DuplicateActorError(f"actor {aid!r} already registered")
        self.actors[aid] = actor

    def get_actor(self, actor_id: str) -> dict:
        if actor_id not in self.actors:
            raise UnknownActorError(actor_id)
        return self.actors[actor_id]

    def has_actor(self, actor_id: str) -> bool:
        return actor_id in self.actors

    # -----------------------------------------------------------------
    # Work-unit tracker (per D20)
    # -----------------------------------------------------------------

    def add_work_unit(self, work_unit: dict) -> None:
        wid = work_unit.get("id")
        if wid is None:
            raise ValueError("work-unit must have id")
        if wid in self.work_units:
            raise ValueError(f"work-unit {wid!r} already exists")
        status = work_unit.get("status")
        if status not in WORK_UNIT_STATUSES:
            raise InvalidWorkUnitTransitionError(
                f"work-unit status {status!r} not in core enum {sorted(WORK_UNIT_STATUSES)}"
            )
        self.work_units[wid] = work_unit

    def get_work_unit(self, work_unit_id: str) -> dict:
        if work_unit_id not in self.work_units:
            raise UnknownWorkUnitError(work_unit_id)
        return self.work_units[work_unit_id]

    def has_work_unit(self, work_unit_id: str) -> bool:
        return work_unit_id in self.work_units

    def transition_work_unit(self, work_unit_id: str, to_status: str) -> tuple[str, str]:
        """Update a work-unit's status. Returns (from_status, to_status).

        Per D20: framework enforces the fixed status enum; it does NOT
        enforce transition conditions (those are shape / specialist
        concerns). Any enum-valid transition is accepted at this layer.
        """
        if to_status not in WORK_UNIT_STATUSES:
            raise InvalidWorkUnitTransitionError(
                f"target status {to_status!r} not in core enum {sorted(WORK_UNIT_STATUSES)}"
            )
        wu = self.get_work_unit(work_unit_id)
        from_status = wu.get("status")
        wu["status"] = to_status
        return from_status, to_status

    # -----------------------------------------------------------------
    # Scope (per D7 §3)
    # -----------------------------------------------------------------

    def set_scope(self, scope: Optional[dict]) -> Optional[dict]:
        """Set current scope. Returns the prior scope (for event payload)."""
        prior = self.current_scope
        self.current_scope = scope
        return prior
