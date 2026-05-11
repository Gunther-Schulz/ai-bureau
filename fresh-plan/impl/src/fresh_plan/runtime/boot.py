"""Boot procedure: orchestrates B1 validation + substrate instantiation.

Per the B2 brief boot procedure spec:

  1. Call B1 to validate the manifest (D29 + D30 + D32 + D33).
  2. Resolve the substrate provision from composition.substrate-bindings[].
  3. Load the resolved substrate provision's spec.
  4. Instantiate the substrate runtime (InProcessSubstrate for B2).
  5. Register manifest-declared actors into the registry.
  6. Load shape policies (B2: record names; full impl is B3).
  7. Bind adapters (B2: store metadata; runtime is B4/B5).
  8. Bind specialists (B2: store metadata; register skills as stubs; runtime is B6).
  9. Emit lifecycle-transition:boot event into the chain.
 10. Return the Workspace handle.

For the in-process substrate, "instantiation" is just constructing a
Python object — no separate process to spawn.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fresh_plan.runtime.substrate import InProcessSubstrate
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

    # 3. Load the substrate provision spec (already in result.loaded_extensions —
    # but we need the resolved spec dict, not just the manifest, so we re-read
    # it through the validator's extension loader).
    capabilities: list[str] = []
    prov_ref = primary_binding.get("provision")
    if prov_ref:
        ext_id, prov_id = prov_ref.split(":", 1)
        # Use the validator's `extensions.load_extension` path indirectly:
        # the validator already validated everything, so we just re-walk the
        # extensions-dir to get the provision spec.
        from fresh_plan.validator.extensions import (
            discover_extensions,
            load_extension,
        )

        discovered = discover_extensions(extensions_dir)
        if ext_id in discovered:
            # Pick the version selected by the validator (any present here).
            # Per D32 multi-version handling — we trust whichever the validator
            # chose; for B2's single-version test fixtures this is unambiguous.
            for version, manifest_path in discovered[ext_id].items():
                loaded_ext, _errs = load_extension(ext_id, version, manifest_path)
                spec = loaded_ext.provisions_loaded.get(prov_id)
                if spec is not None:
                    capabilities = list(spec.get("capabilities", []))
                    break

    # If the binding is purely capability-based, advertise the required
    # capabilities (per D12 mixed binding semantics).
    for cap in primary_binding.get("required-capabilities", []) or []:
        if cap not in capabilities:
            capabilities.append(cap)

    # 4. Instantiate the substrate runtime.
    substrate = InProcessSubstrate(
        workspace_id=manifest["id"],
        runtime_shape=runtime_shape,
        schema_store=schema_store,
        capabilities=capabilities,
    )

    # 5. Register manifest-declared actors.
    for actor in composition.get("actors", []):
        substrate.state.add_actor(dict(actor))

    # Cache known binding-ids (for D30 §4 per-event check support and
    # for the workspace's introspection API).
    substrate.known_binding_ids = {
        b.get("binding-id") for b in substrate_bindings if b.get("binding-id")
    }

    # Populate the runtime payload-subtype registry from loaded extensions'
    # vocabulary-registrations.
    for slot_qids in (result.vocabulary_tables or {}).get("event.payload-subtype", []):
        substrate.registered_payload_subtypes.add(slot_qids)

    # 6. Shape policies (D13 + B3): load + attach the shape impl when a
    # provision is bound; register stub handlers for declared hook names.
    shape_ref = composition.get("shape", {}).get("provision")
    substrate.bound_shape_provision = shape_ref  # type: ignore[attr-defined]
    if shape_ref:
        from fresh_plan.runtime.shape import load_shape_from_provision

        try:
            shape = load_shape_from_provision(shape_ref, extensions_dir)
        except ValueError:
            shape = None
        if shape is not None:
            substrate.shape = shape
            shape.register_handlers(substrate.hooks)

    # 7. Adapter bindings: store metadata + instantiate adapter runtimes.
    # Workspace attachment happens after Workspace is constructed (below).
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
        except ValueError:
            continue
        substrate.adapter_instances[bid] = adapter

    # 8. Specialist bindings: store metadata + register skill stubs.
    for binding in composition.get("specialist-bindings", []):
        bid = binding.get("binding-id")
        if bid:
            substrate.specialist_bindings[bid] = dict(binding)
        # Look up the specialist provision spec to enumerate its declared skills.
        prov_ref = binding.get("provision")
        if not prov_ref:
            continue
        ext_id, prov_id = prov_ref.split(":", 1)
        from fresh_plan.validator.extensions import (
            discover_extensions,
            load_extension,
        )

        discovered = discover_extensions(extensions_dir)
        if ext_id not in discovered:
            continue
        for version, manifest_path in discovered[ext_id].items():
            loaded_ext, _errs = load_extension(ext_id, version, manifest_path)
            spec = loaded_ext.provisions_loaded.get(prov_id)
            if spec is None:
                continue
            for skill in spec.get("skills", []) or []:
                skill_id = skill if isinstance(skill, str) else skill.get("id")
                if skill_id and not substrate.skills.has(skill_id):
                    substrate.skills.register_stub(skill_id)
            break

    # Construct the Workspace handle and emit the boot lifecycle event.
    # Import here to avoid circular imports at module load time.
    from fresh_plan.runtime.workspace import Workspace

    workspace = Workspace(substrate=substrate, manifest=manifest)

    # Attach the workspace to each instantiated adapter (B4 boot-ordering).
    for adapter in substrate.adapter_instances.values():
        adapter.attach_workspace(workspace)

    # 9. Emit lifecycle-transition:boot. Use the first manifest-declared
    # actor as the attributing actor (every event needs ≥1 actor per D10;
    # boot is workspace-level, so any registered actor is a reasonable
    # attribution — schema validates the actor exists in state).
    first_actor_id = composition.get("actors", [{}])[0].get("id")
    boot_event = {
        "id": f"evt-boot-{substrate.workspace_id}",
        "prev-event": None,
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
