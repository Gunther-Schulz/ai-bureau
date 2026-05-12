"""Boot procedure: orchestrates B1 validation + substrate instantiation.

Per the B2 brief boot procedure spec (refined by Bref closure of D39):

  1. Call B1 to validate the manifest (D29 + D30 + D32 + D33).
  2. Resolve the substrate provision from composition.substrate-bindings[].
  3. Load the resolved substrate provision's spec.
  4. Instantiate the substrate runtime — dispatched by provision id
     (InProcessSubstrate / MSAgentFrameworkSubstrate per D41).
  5. Bind shape, adapters, specialists; construct Workspace handle;
     attach workspace to adapters/specialists.
  6. Per Bref closure of D39: emit synthetic composition-change:add
     events for each manifest-declared actor (full record in
     payload.record). First actor self-attests (per D34 §A.5 extension);
     subsequent ones attribute to the first. Projection adds them to
     state — no direct state mutation.
  7. Emit lifecycle-transition:boot event into the chain.
  8. Return the Workspace handle.

For the in-process substrate, "instantiation" is just constructing a
Python object — no separate process to spawn.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fresh_plan.runtime.provision import load_provision_spec
from fresh_plan.runtime.substrate import load_substrate_from_provision
from fresh_plan.validator import validate_workspace_boot
from fresh_plan.validator.schemas import SchemaStore, load_schemas
from fresh_plan.validator.types import ValidationFailure


class WorkspaceBootError(Exception):
    """B1 validation or boot-procedure failure.

    Carries the structured failure list (same shape as the B1 validator).
    Per D30 boot-time failure semantics: all-or-nothing — the substrate
    is not partially constructed.
    """

    def __init__(self, failures: list[ValidationFailure]) -> None:
        self.failures = failures
        msg = "; ".join(f"[{f.category}] {f.path}: {f.reason}" for f in failures)
        super().__init__(msg or "workspace boot failed")


def _utcnow_iso() -> str:
    """ISO-8601 UTC with Z suffix, matching the schema's date-time format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def boot_workspace(
    manifest: dict,
    extensions_dir: Path,
    schemas_dir: Optional[Path] = None,
) -> "Workspace":
    """Boot a workspace per the B2 boot procedure.

    Args:
        manifest: parsed workspace manifest.
        extensions_dir: directory containing on-disk extensions.
        schemas_dir: override for the Phase A schemas (testing).

    Returns:
        Workspace handle (post-boot lifecycle event emitted).

    Raises:
        WorkspaceBootError: B1 validation failure; substrate not
            instantiated.
    """
    # 1. B1 validation (D29 + D30 boot-time + D32 + D33).
    result = validate_workspace_boot(manifest, extensions_dir, schemas_dir)
    if not result.success:
        raise WorkspaceBootError(result.failures)

    schema_store = load_schemas(schemas_dir)
    composition = manifest["composition"]

    # 2. Resolve the substrate provision from composition.substrate-bindings[].
    # Per D32 §1: multi-binding satisfiability is settled at boot; runtime
    # routing is not at framework level. For B2 we use the first binding —
    # the brief explicitly OKs this scope cut.
    substrate_bindings = composition.get("substrate-bindings", [])
    if not substrate_bindings:
        # The schema requires minItems=1 so B1 would have rejected; defensive.
        raise WorkspaceBootError(
            [
                ValidationFailure(
                    category="resolution",
                    path="composition.substrate-bindings",
                    value=None,
                    reason="no substrate-bindings present after validation success",
                )
            ]
        )
    primary_binding = substrate_bindings[0]
    runtime_shape = primary_binding.get("runtime-shape")
    prov_ref = primary_binding.get("provision")
    if not prov_ref:
        # Per workspace schema substrate-binding anyOf: provision OR required-
        # capabilities. B1 success implies at least one is present; a binding
        # with required-capabilities only cannot be booted in B2b (no
        # registered runtime class to dispatch to). Treat as resolution failure.
        raise WorkspaceBootError(
            [
                ValidationFailure(
                    category="resolution",
                    path="composition.substrate-bindings[0].provision",
                    value=None,
                    reason=(
                        "substrate-binding lacks an explicit provision; "
                        "capability-only binding is not bootable in Phase B"
                    ),
                )
            ]
        )

    # 3. Load the substrate provision spec via the shared helper.
    capabilities: list[str] = list(
        load_provision_spec(prov_ref, extensions_dir).get("capabilities", [])
    )

    # If the binding additionally lists required-capabilities, advertise them
    # (per D12 mixed binding semantics).
    for cap in primary_binding.get("required-capabilities", []) or []:
        if cap not in capabilities:
            capabilities.append(cap)

    # 4. Instantiate the substrate runtime — dispatched by provision id.
    substrate = load_substrate_from_provision(
        prov_ref,
        extensions_dir,
        workspace_id=manifest["id"],
        runtime_shape=runtime_shape,
        schema_store=schema_store,
        capabilities=capabilities,
    )

    # Cache known binding-ids (for D30 §4 per-event check support and
    # for the workspace's introspection API). Manifest-declared actor
    # seeding now happens via synthetic composition-change events emitted
    # below, after shape/adapter/specialist binding is in place — per
    # Bref closure of D39 (no out-of-band state mutation at boot).
    substrate.known_binding_ids = {
        b.get("binding-id") for b in substrate_bindings if b.get("binding-id")
    }

    # Populate the runtime payload-subtype registry from loaded extensions'
    # vocabulary-registrations.
    for slot_qids in (result.vocabulary_tables or {}).get("event.payload-subtype", []):
        substrate.registered_payload_subtypes.add(slot_qids)

    # 6. Shape policies (D13 + B3): load + attach the shape impl when a
    # provision is bound; register stub handlers for declared hook names.
    # Per D46 §B.1: unknown shape provision-id surfaces as WorkspaceBootError
    # rather than silently degrading to shape=None.
    shape_ref = composition.get("shape", {}).get("provision")
    substrate.bound_shape_provision = shape_ref  # type: ignore[attr-defined]
    if shape_ref:
        from fresh_plan.runtime.shape import load_shape_from_provision

        try:
            shape = load_shape_from_provision(shape_ref, extensions_dir)
        except ValueError as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="resolution",
                        path="composition.shape.provision",
                        value=shape_ref,
                        reason=(
                            f"shape provision {shape_ref!r} has no registered "
                            f"runtime class — manifest declares this binding but "
                            f"the framework cannot instantiate it. Underlying: {e}"
                        ),
                    )
                ]
            ) from e
        substrate.shape = shape
        shape.register_handlers(substrate.hooks)

    # 7. Adapter bindings: store metadata + instantiate adapter runtimes.
    # Workspace attachment happens after Workspace is constructed (below).
    # Per D46 §B.1: unknown adapter provision-id surfaces as WorkspaceBootError
    # rather than silently skipping.
    for binding in composition.get("adapter-bindings", []):
        bid = binding.get("binding-id")
        if bid:
            substrate.adapter_bindings[bid] = dict(binding)
        prov_ref = binding.get("provision")
        if not bid or not prov_ref:
            continue
        from fresh_plan.runtime.adapter import load_adapter_from_provision

        try:
            adapter = load_adapter_from_provision(prov_ref, extensions_dir)
        except ValueError as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="resolution",
                        path=f"composition.adapter-bindings[binding-id={bid!r}].provision",
                        value=prov_ref,
                        reason=(
                            f"adapter provision {prov_ref!r} has no registered "
                            f"runtime class — manifest declares this binding but "
                            f"the framework cannot instantiate it. Underlying: {e}"
                        ),
                    )
                ]
            ) from e
        substrate.adapter_instances[bid] = adapter

    # 8. Specialist bindings: store metadata + instantiate specialist runtimes
    # (B6 + D19). Per D46 §B.1: unknown specialist provision-id surfaces as
    # WorkspaceBootError rather than silently falling back to stub-skill
    # registration. The prior fallback path was vestigial — only B1 validator
    # fixtures (workspace-valid using core-ext:minimal-specialist) had no
    # runtime class registered, and those fixtures are never runtime-booted
    # (they exercise validate_workspace_boot only). Production specialists
    # MUST have a registered runtime class.
    from fresh_plan.runtime.specialist import load_specialist_from_provision

    for binding in composition.get("specialist-bindings", []):
        bid = binding.get("binding-id")
        if bid:
            substrate.specialist_bindings[bid] = dict(binding)
        prov_ref = binding.get("provision")
        if not bid or not prov_ref:
            continue
        try:
            specialist = load_specialist_from_provision(prov_ref, extensions_dir)
        except ValueError as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="resolution",
                        path=f"composition.specialist-bindings[binding-id={bid!r}].provision",
                        value=prov_ref,
                        reason=(
                            f"specialist provision {prov_ref!r} has no registered "
                            f"runtime class — manifest declares this binding but "
                            f"the framework cannot instantiate it. Underlying: {e}"
                        ),
                    )
                ]
            ) from e
        substrate.specialist_instances[bid] = specialist

    # Construct the Workspace handle and emit the boot lifecycle event.
    # Import here to avoid circular imports at module load time.
    from fresh_plan.runtime.workspace import Workspace

    workspace = Workspace(substrate=substrate, manifest=manifest)

    # Attach the workspace to each instantiated adapter (B4 boot-ordering).
    # Per D48 §B.2: wrap each call in try/except → WorkspaceBootError(category=
    # "adapter-attach"). Phase B stubs have a trivial attach (cannot fail);
    # the wrapping is defensive for Phase C+ real-wire where attach may run
    # connection-pool setup / auth handshake / pre-flight. Per D48 §D D-2,
    # attach-failure cause-vocabulary inside each adapter-impl's raised
    # exception is extension-defined per protocol.
    for bid, adapter in substrate.adapter_instances.items():
        try:
            adapter.attach_workspace(workspace)
        except Exception as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="adapter-attach",
                        path=f"composition.adapter-bindings[binding-id={bid!r}]",
                        value=adapter.id,
                        reason=(
                            f"adapter {adapter.id!r} attach_workspace failed: {e}"
                        ),
                    )
                ]
            ) from e

    # Attach workspace + register skills for each instantiated specialist (B6
    # boot-ordering). Runs AFTER adapter attach so required-adapter-bindings
    # resolve via workspace.adapter(...). Subscribers list is populated for
    # the append_event hot path (D37 event-driven coordination).
    for specialist in substrate.specialist_instances.values():
        specialist.attach_workspace(workspace)
        specialist.register_skills(substrate.skills)
        substrate.specialist_subscribers.append(specialist)

    # Per Bref closure of D39: seed manifest-declared actors via synthetic
    # composition-change:add events (one per actor). The full actor record
    # rides on payload.record so state_at(n) replay reproduces them. The
    # first actor self-attests in event.actors[]; subsequent ones attribute
    # to the first. Per D34 §A.5 extension (Bref): per-event identity
    # resolution admits state-after-applying-this-event for the actor
    # being added on a composition-change:add event.
    #
    # Per D46 §B.2: mid-cascade rejection during the seeding loop is wrapped
    # as WorkspaceBootError naming the failing actor index; partial-state
    # workspace is partial-and-discardable (no handle returned to caller).
    # Per D46 §C cleanup: actors with missing id surface as WorkspaceBootError
    # instead of silently dropping.
    from fresh_plan.runtime.event_chain import MalformedEventError
    from fresh_plan.runtime.per_event_checks import EventRejected

    manifest_actors = composition.get("actors", []) or []
    first_actor_id: Optional[str] = None
    for idx, actor in enumerate(manifest_actors):
        actor_record = dict(actor)
        aid = actor_record.get("id")
        if aid is None:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="actor-seeding",
                        path=f"composition.actors[{idx}].id",
                        value=None,
                        reason=(
                            f"manifest actor at index {idx} lacks an id; cannot "
                            f"emit synthetic composition-change:add seed event"
                        ),
                    )
                ]
            )
        attributing_id = aid if first_actor_id is None else first_actor_id
        prev_id = (
            substrate.event_chain.tail["id"] if substrate.event_chain.tail else None
        )
        seed_event = {
            "id": f"evt-actor-add-{idx:03d}-{substrate.workspace_id}",
            "prev-event": prev_id,
            "timestamp": _utcnow_iso(),
            "actors": [{"id": attributing_id}],
            "payload-subtype": "composition-change",
            "payload": {
                "change-type": "add",
                "binding-kind": "actor",
                "binding-reference": aid,
                "record": actor_record,
            },
        }
        try:
            substrate.append_event(seed_event)
        except (EventRejected, MalformedEventError) as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="actor-seeding",
                        path=f"composition.actors[{idx}]",
                        value=aid,
                        reason=(
                            f"actor seeding rejected at index {idx} (id={aid!r}): "
                            f"{e}. Workspace handle NOT returned; substrate is "
                            f"partial-and-discardable (actors 0..{idx - 1} were "
                            f"seeded; lifecycle:boot was not emitted)."
                        ),
                    )
                ]
            ) from e
        if first_actor_id is None:
            first_actor_id = aid

    # Emit lifecycle-transition:boot. Use the first manifest-declared actor
    # as the attributing actor (every event needs ≥1 actor per D10; boot
    # is workspace-level, so any registered actor is a reasonable
    # attribution). prev-event chains off the most recent seed event (or
    # is None if the workspace has no manifest actors — schema rejects
    # that case anyway via composition.actors minItems=1).
    prev_id = substrate.event_chain.tail["id"] if substrate.event_chain.tail else None
    boot_event = {
        "id": f"evt-boot-{substrate.workspace_id}",
        "prev-event": prev_id,
        "timestamp": _utcnow_iso(),
        "actors": [{"id": first_actor_id}] if first_actor_id else [],
        "payload-subtype": "lifecycle-transition",
        "payload": {
            "transition-type": "boot",
            "trigger": "host-process",
        },
    }
    substrate.append_event(boot_event)

    return workspace
