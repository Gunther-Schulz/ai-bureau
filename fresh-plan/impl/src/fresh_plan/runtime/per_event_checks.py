"""Per-event D30 §4 runtime referential integrity (the runtime portion).

Per D30 §4, identity checks split into two timing modes:
  - boot-time (validated by B1): agent-actor.substrate-binding resolution,
    duplicate binding-ids, etc.
  - per-event (this module, runtime): event.actors[].id resolves; event
    work-unit-id (when non-null) resolves; event.payload-subtype is
    registered (core or extension).

Per D34 §A.5 (clarification of D30 §4): identity resolution is against
*current state*, not the boot-time manifest snapshot — sub-agents added
via composition-change events are valid event targets after their
composition-change is appended.

Per D30 timing-modes table: per-event failures REJECT the event (it is
not appended to the chain). Per the B2 brief: this raises
`EventRejected` so the caller can handle.
"""
from __future__ import annotations

from typing import Iterable

from fresh_plan.runtime.workspace_state import WorkspaceState
from fresh_plan.validator.types import ValidationFailure


# Core payload subtypes per D10. Extension-registered subtypes live in
# the substrate's payload-subtype registry (populated from loaded
# extensions' vocabulary-registrations at boot).
CORE_PAYLOAD_SUBTYPES = frozenset(
    {"claim", "action", "state-change", "composition-change", "lifecycle-transition"}
)


def check_event_references(
    event: dict,
    state: WorkspaceState,
    registered_payload_subtypes: Iterable[str],
    known_binding_ids: Iterable[str],
) -> list[ValidationFailure]:
    """Run D30 §4 per-event runtime checks; return any failures.

    Per D34 §A.5: resolution is against current state (the live actor +
    work-unit registries on `state`), not the manifest snapshot.

    `registered_payload_subtypes` is the runtime registry of extension-
    registered subtypes (managed by the substrate; populated from the
    loaded extensions' vocabulary-registrations at boot). Core subtypes
    are admitted unconditionally per D10.

    `known_binding_ids` is included so substrate-binding references that
    might appear in actor records can be cross-checked when a runtime-
    added actor (per D19 sub-agent) is being validated against state —
    but per D30 §4 the per-event identity check covers event.actors[].id
    only; substrate-binding integrity is boot-time + composition-change-
    time, not per-event. This parameter is exposed for the
    composition-change handling path in the substrate.
    """
    failures: list[ValidationFailure] = []

    # event.actors[].id → existing actor in current state
    for i, actor_ref in enumerate(event.get("actors", []) or []):
        aid = actor_ref.get("id")
        if aid is None:
            # Schema layer catches missing id; nothing to resolve.
            continue
        if not state.has_actor(aid):
            failures.append(
                ValidationFailure(
                    category="identity",
                    path=f"event.actors[{i}].id",
                    value=aid,
                    reason=(
                        f"event.actors[{i}].id {aid!r} does not resolve to a "
                        "registered actor in current workspace state"
                    ),
                )
            )

    # event.work-unit-id (when non-null) → existing work-unit in current state
    wu_id = event.get("work-unit-id")
    if wu_id is not None and not state.has_work_unit(wu_id):
        failures.append(
            ValidationFailure(
                category="identity",
                path="event.work-unit-id",
                value=wu_id,
                reason=(
                    f"event.work-unit-id {wu_id!r} does not resolve to a "
                    "registered work-unit in current workspace state"
                ),
            )
        )

    # event.payload-subtype → core or extension-registered
    subtype = event.get("payload-subtype")
    if subtype is not None:
        if (
            subtype not in CORE_PAYLOAD_SUBTYPES
            and subtype not in set(registered_payload_subtypes)
        ):
            failures.append(
                ValidationFailure(
                    category="vocabulary",
                    path="event.payload-subtype",
                    value=subtype,
                    reason=(
                        f"payload-subtype {subtype!r} is neither a core "
                        "subtype (D10) nor registered by any loaded extension"
                    ),
                )
            )

    # known_binding_ids is unused for event-level checks; included for the
    # substrate's parallel composition-change handling per D34 §A.5.
    _ = list(known_binding_ids)

    return failures


class EventRejected(Exception):
    """Per-event identity-check failure (D30 §4 runtime portion).

    Per D30 timing-modes table: a per-event failure REJECTS the event
    (it is not appended to the chain). The substrate raises this so
    callers can handle programmatically.
    """

    def __init__(self, failures: list[ValidationFailure]) -> None:
        self.failures = failures
        msg = "; ".join(f"[{f.category}] {f.path}: {f.reason}" for f in failures)
        super().__init__(msg or "event rejected")
