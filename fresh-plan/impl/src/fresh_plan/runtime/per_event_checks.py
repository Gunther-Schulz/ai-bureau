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

from typing import Iterable, Optional

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
    known_specialist_binding_ids: Optional[Iterable[str]] = None,
    registered_work_unit_kinds: Optional[Iterable[str]] = None,
    registered_payload_vocabulary: Optional[dict[str, Iterable[str]]] = None,
    shape_role_ids: Optional[Iterable[str]] = None,
    work_unit_kind_payload_schemas: Optional[dict[str, dict]] = None,
) -> list[ValidationFailure]:
    """Run D30 §4 per-event runtime checks; return any failures.

    Per D34 §A.5: resolution is against current state (the live actor +
    work-unit registries on `state`), not the manifest snapshot. The
    "current state" reading extends to state-after-applying-this-event:
    when the event itself adds an actor or creates a work-unit, that
    actor / work-unit is admitted as a reference target on the same
    event ("self-attestation" — see Bref closure of D39 tensions).
    This is what enables boot-time manifest-actor seeding (which would
    otherwise hit a chicken-and-egg: composition-change:add for the
    first manifest actor needs ≥1 actor in event.actors[] but no actor
    is in state yet) and work-unit creation events that carry the
    work-unit-id slot for query-by-work-unit support.

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

    payload = event.get("payload") or {}
    subtype = event.get("payload-subtype")

    # Self-attestation: when this event itself adds an actor (composition-
    # change:add + binding-kind=actor), the actor referenced in
    # event.actors[].id may be the very one being added.
    self_attested_actor: Optional[str] = None
    if (
        subtype == "composition-change"
        and payload.get("change-type") == "add"
        and payload.get("binding-kind") == "actor"
    ):
        self_attested_actor = payload.get("binding-reference")

    # Self-attestation: when this event itself creates a work-unit
    # (state-change + what=work-unit-created), event.work-unit-id may
    # match the work-unit being created (carried as `payload.after.id`
    # per Bref closure of D39 tension 2).
    self_attested_work_unit: Optional[str] = None
    if subtype == "state-change" and payload.get("what") == "work-unit-created":
        after = payload.get("after")
        if isinstance(after, dict):
            self_attested_work_unit = after.get("id")

    # Materialize shape role vocabulary (if provided) for §B-3 + §B-7 checks.
    # When None: shape-role check skipped (no shape bound OR shape declares no
    # roles vocabulary). When provided: roles on event.actors[] + work-unit
    # contributing-actors[] are validated against the vocabulary.
    _shape_role_ids: Optional[set[str]] = (
        set(shape_role_ids) if shape_role_ids is not None else None
    )

    # event.actors[].id → existing actor in current state
    for i, actor_ref in enumerate(event.get("actors", []) or []):
        aid = actor_ref.get("id")
        if aid is None:
            # Schema layer catches missing id; nothing to resolve.
            continue
        if not state.has_actor(aid) and aid != self_attested_actor:
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
        # §B-3 (D62 §B cheap impl): event.actors[].role vocabulary check.
        # Per D13: roles are declared by the bound shape's `roles[]` slot.
        # When the actor-ref omits role (legal — only authority-bindings
        # require role), skip. When the shape has no roles vocabulary
        # (_shape_role_ids is None or empty), skip. Otherwise the role
        # value must appear in the shape's roles vocabulary.
        if _shape_role_ids:
            role = actor_ref.get("role")
            if role is not None and role not in _shape_role_ids:
                failures.append(
                    ValidationFailure(
                        category="vocabulary",
                        path=f"event.actors[{i}].role",
                        value=role,
                        reason=(
                            f"event.actors[{i}].role {role!r} is not declared "
                            "in the bound shape's roles[] vocabulary"
                        ),
                    )
                )

    # event.work-unit-id (when non-null) → existing work-unit in current state
    wu_id = event.get("work-unit-id")
    if (
        wu_id is not None
        and not state.has_work_unit(wu_id)
        and wu_id != self_attested_work_unit
    ):
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

    # Per D59 §B.1 — open-vocab payload-body validation. For each of the
    # four core payload-subtypes carrying an open-vocab string slot, check
    # that the value (when present + non-empty) is registered by some
    # loaded extension. Empty / absent values pass (slots optional).
    if registered_payload_vocabulary is not None:
        _payload_slot_map = [
            ("claim", "confidence", "claim.confidence"),
            ("action", "action-name", "action.action-name"),
            ("state-change", "what", "state-change.what"),
            ("lifecycle-transition", "trigger", "lifecycle-transition.trigger"),
        ]
        for owning_subtype, slot_key, slot_qualified in _payload_slot_map:
            if subtype != owning_subtype:
                continue
            value = payload.get(slot_key)
            if not isinstance(value, str) or not value:
                continue
            registered = set(registered_payload_vocabulary.get(slot_qualified, []) or [])
            # Opt-in enforcement: check fires only when the per-slot table has
            # at least one registration. Pre-registration state leaves the
            # slot unconstrained (back-compat with existing event sites that
            # pre-date D59 vocabulary registration). Once an extension
            # registers ANY value for a slot, all values for that slot become
            # subject to closed-vocabulary enforcement.
            if not registered:
                continue
            if value not in registered:
                failures.append(
                    ValidationFailure(
                        category="vocabulary",
                        path=f"event.payload.{slot_key}",
                        value=value,
                        reason=(
                            f"payload-{owning_subtype} {slot_key} {value!r} is "
                            "not registered by any loaded extension's "
                            "payload-vocabulary-registrations"
                        ),
                    )
                )

    # known_binding_ids is unused for event-level checks; included for the
    # substrate's parallel composition-change handling per D34 §A.5.
    _ = list(known_binding_ids)

    # Per D51 §B.1 — per-work-unit identity checks at work-unit-creation
    # event time (D30 §4 per-work-unit portion). Work-units are created via
    # state-change events with what="work-unit-created"; payload.after carries
    # the full work-unit record. Validate (i) contributing-actors[].id; (ii)
    # contributing-specialists[]; (iii) kind. Reuses category="identity"
    # (same semantic class as event-level identity per D30 §4).
    if (
        subtype == "state-change"
        and payload.get("what") == "work-unit-created"
    ):
        after = payload.get("after")
        if isinstance(after, dict):
            wu_path_base = "event.payload.after"
            # (i) contributing-actors[].id → existing actor (with self-attestation)
            for j, ca in enumerate(after.get("contributing-actors", []) or []):
                if not isinstance(ca, dict):
                    continue
                ca_id = ca.get("id")
                if ca_id is None:
                    continue  # Schema layer catches missing id
                # Self-attestation: actors added on this very event (composition-
                # change:add) are admitted; for work-unit-created the actor
                # references must already exist OR be the self-attested-actor
                # from a co-emitted composition-change (single-event-only case
                # not currently supported; rare).
                if not state.has_actor(ca_id):
                    failures.append(
                        ValidationFailure(
                            category="identity",
                            path=f"{wu_path_base}.contributing-actors[{j}].id",
                            value=ca_id,
                            reason=(
                                f"work-unit creation references contributing-actor "
                                f"{ca_id!r} which does not resolve to a registered "
                                "actor in current workspace state"
                            ),
                        )
                    )
                # §B-7 (D62 §B cheap impl; composes with §B-3): contributing-actors
                # role vocabulary check against shape's roles vocabulary.
                if _shape_role_ids:
                    ca_role = ca.get("role")
                    if ca_role is not None and ca_role not in _shape_role_ids:
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=(
                                    f"{wu_path_base}.contributing-actors[{j}].role"
                                ),
                                value=ca_role,
                                reason=(
                                    f"work-unit contributing-actors[{j}].role "
                                    f"{ca_role!r} is not declared in the bound "
                                    "shape's roles[] vocabulary"
                                ),
                            )
                        )
            # (ii) contributing-specialists[] → bound specialist binding-id
            if known_specialist_binding_ids is not None:
                known_sp_set = set(known_specialist_binding_ids)
                for j, sp_bid in enumerate(after.get("contributing-specialists", []) or []):
                    if not isinstance(sp_bid, str):
                        continue
                    if sp_bid not in known_sp_set:
                        failures.append(
                            ValidationFailure(
                                category="identity",
                                path=f"{wu_path_base}.contributing-specialists[{j}]",
                                value=sp_bid,
                                reason=(
                                    f"work-unit creation references specialist "
                                    f"binding-id {sp_bid!r} which is not bound "
                                    "in the workspace"
                                ),
                            )
                        )
            # (iii) kind → registered work-unit-kind
            if registered_work_unit_kinds is not None:
                known_kinds = set(registered_work_unit_kinds)
                wu_kind = after.get("kind")
                if wu_kind is not None and wu_kind not in known_kinds:
                    failures.append(
                        ValidationFailure(
                            category="identity",
                            path=f"{wu_path_base}.kind",
                            value=wu_kind,
                            reason=(
                                f"work-unit kind {wu_kind!r} is not registered "
                                "by any loaded extension's vocabulary-registrations"
                            ),
                        )
                    )
            # §B-4 (D62 §B cheap impl) — work-unit.payload schema validation
            # against the work-unit-kind's registered payload schema. Per D20
            # + work-unit.schema.json: framework conformance validator (D30)
            # validates payload against the kind's spec-ref schema. No-op
            # when (a) no schemas registered, (b) this kind has no registered
            # schema (spec-ref omitted / unresolvable). Reuses `vocabulary`
            # category since payload-shape conformance is a per-kind
            # vocabulary check (D30 §3 spirit).
            if (
                work_unit_kind_payload_schemas
                and isinstance(after.get("kind"), str)
                and isinstance(after.get("payload"), dict)
            ):
                wu_kind = after["kind"]
                schema = work_unit_kind_payload_schemas.get(wu_kind)
                if schema is not None:
                    # Lazy import: jsonschema is already a dependency via
                    # validator/schemas.py; lazy here to keep the per-event
                    # checks module's import footprint light when no
                    # work-unit-creation events are flowing.
                    from jsonschema import Draft202012Validator

                    validator = Draft202012Validator(schema)
                    for err in validator.iter_errors(after["payload"]):
                        path_parts = list(err.absolute_path)
                        sub_path = "".join(
                            f"[{p}]" if isinstance(p, int) else f".{p}"
                            for p in path_parts
                        )
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{wu_path_base}.payload{sub_path}",
                                value=(
                                    err.instance
                                    if not isinstance(err.instance, (dict, list))
                                    else None
                                ),
                                reason=(
                                    f"work-unit payload (kind={wu_kind!r}) "
                                    f"violates registered payload schema: "
                                    f"{err.message}"
                                ),
                            )
                        )

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
