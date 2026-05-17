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
    # Per D57 §B.1: registry-miss → ProvisionResolutionError →
    # category="resolution"; constructor-raise → category="configuration-rejected".
    from fresh_plan.runtime.provision import ProvisionResolutionError

    try:
        substrate = load_substrate_from_provision(
            prov_ref,
            extensions_dir,
            workspace_id=manifest["id"],
            runtime_shape=runtime_shape,
            schema_store=schema_store,
            capabilities=capabilities,
            configuration=primary_binding.get("configuration"),
        )
    except ProvisionResolutionError as e:
        raise WorkspaceBootError(
            [
                ValidationFailure(
                    category="resolution",
                    path="composition.substrate-bindings[0].provision",
                    value=prov_ref,
                    reason=(
                        f"substrate provision {prov_ref!r} resolution failed: {e}"
                    ),
                )
            ]
        ) from e
    except Exception as e:
        raise WorkspaceBootError(
            [
                ValidationFailure(
                    category="configuration-rejected",
                    path="composition.substrate-bindings[0].configuration",
                    value=prov_ref,
                    reason=(
                        f"substrate {prov_ref!r} runtime rejected configuration: {e}"
                    ),
                )
            ]
        ) from e

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

    # Per D51 §B.1: populate registered_work_unit_kinds for per-work-unit
    # identity check at work-unit-creation event time (D30 §4 per-work-unit).
    for wu_kind in (result.vocabulary_tables or {}).get("work-unit.kind", []):
        substrate.registered_work_unit_kinds.add(wu_kind)

    # §B-4 (D62 §B cheap impl): populate work_unit_kind_payload_schemas from
    # validator's resolved spec-refs (vocabulary-registrations for
    # work-unit.kind whose spec-ref resolves to a JSON Schema). Per D20 +
    # work-unit.schema.json the framework validates payload shape via this
    # schema. Schemas absent for kinds without spec-refs (no-op).
    if result.work_unit_kind_payload_schemas:
        substrate.work_unit_kind_payload_schemas.update(
            result.work_unit_kind_payload_schemas
        )

    # Per D59 §B.1: populate registered_payload_vocabulary from validator's
    # payload_vocabulary_tables. Per-slot merge into substrate's preset
    # four-slot dict.
    for slot, values in (result.payload_vocabulary_tables or {}).items():
        substrate.registered_payload_vocabulary.setdefault(slot, set()).update(values)

    # 6. Shape policies (D13 + B3): load + attach the shape impl when a
    # provision is bound; register stub handlers for declared hook names.
    # Per D46 §B.1: unknown shape provision-id surfaces as WorkspaceBootError
    # rather than silently degrading to shape=None.
    shape_ref = composition.get("shape", {}).get("provision")
    substrate.bound_shape_provision = shape_ref  # type: ignore[attr-defined]
    if shape_ref:
        from fresh_plan.runtime.shape import load_shape_from_provision

        try:
            shape = load_shape_from_provision(
                shape_ref,
                extensions_dir,
                configuration=composition.get("shape", {}).get("configuration"),
            )
        except ProvisionResolutionError as e:
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
        except WorkspaceBootError:
            # Shape.__post_init__ may raise WorkspaceBootError directly
            # (e.g., D56 authority-constraint-grammar). Surface unchanged.
            raise
        except Exception as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="configuration-rejected",
                        path="composition.shape.configuration",
                        value=shape_ref,
                        reason=(
                            f"shape {shape_ref!r} runtime rejected configuration: {e}"
                        ),
                    )
                ]
            ) from e
        substrate.shape = shape
        shape.register_handlers(substrate.hooks)

        # §B cheap impl: log shape.optional-capabilities that are NOT advertised
        # by the substrate. Optional capabilities (D13) are nice-to-have; absence
        # is non-fatal but should be observable. Recorded on the substrate for
        # introspection; not raised. Phase C+ may surface via diagnostic API.
        unmet_optional = [
            cap for cap in shape.optional_capabilities if cap not in capabilities
        ]
        substrate.unmet_optional_capabilities = unmet_optional  # type: ignore[attr-defined]

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
            adapter = load_adapter_from_provision(
                prov_ref,
                extensions_dir,
                configuration=binding.get("configuration"),
            )
        except ProvisionResolutionError as e:
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
        except Exception as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="configuration-rejected",
                        path=(
                            f"composition.adapter-bindings[binding-id={bid!r}]"
                            f".configuration"
                        ),
                        value=prov_ref,
                        reason=(
                            f"adapter {prov_ref!r} runtime rejected configuration: {e}"
                        ),
                    )
                ]
            ) from e
        substrate.adapter_instances[bid] = adapter

    # §B-5 (D62 §B cheap impl): adapter.declared-event-emissions[] cross-checked
    # against shape's authority-bindings vocabulary. Per D16 line 11 ("Lets
    # shapes' authority-bindings reason about adapter outputs at composition
    # validation time"): record adapter emissions whose payload-subtype has
    # no corresponding shape.authority-bindings[].payload-subtype. Non-fatal
    # — adapter emissions without shape authority-binding may be intentional
    # (out-of-scope events, observability-only emissions). Stored on
    # substrate as parallel to `unmet_optional_capabilities` (item 1 §B
    # cheap impl pattern). Empty list = full coverage OR no shape bound OR
    # no shape authority-bindings declared.
    unmet_adapter_emissions: list[dict] = []
    if substrate.shape is not None:
        bound_payload_subtypes: set[str] = {
            ab.get("payload-subtype")
            for ab in substrate.shape.authority_bindings
            if ab.get("payload-subtype")
        }
        # Skip the check when shape declares no authority-bindings at all
        # (e.g., MinShape / test fixtures). The shape has not opted into
        # constraining emission shape-side, so all emissions are accepted
        # silently.
        if bound_payload_subtypes:
            for bid, adapter in substrate.adapter_instances.items():
                for emission in adapter.declared_event_emissions:
                    pst = emission.get("payload-subtype")
                    if pst and pst not in bound_payload_subtypes:
                        unmet_adapter_emissions.append(
                            {
                                "binding-id": bid,
                                "adapter-id": adapter.id,
                                "payload-subtype": pst,
                            }
                        )
    # type: ignore comment — attribute set dynamically per item-1 pattern.
    substrate.unmet_adapter_emissions = unmet_adapter_emissions  # type: ignore[attr-defined]

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
            specialist = load_specialist_from_provision(
                prov_ref,
                extensions_dir,
                configuration=binding.get("configuration"),
            )
        except ProvisionResolutionError as e:
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
        except Exception as e:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="configuration-rejected",
                        path=(
                            f"composition.specialist-bindings[binding-id={bid!r}]"
                            f".configuration"
                        ),
                        value=prov_ref,
                        reason=(
                            f"specialist {prov_ref!r} runtime rejected configuration: {e}"
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
