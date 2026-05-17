"""D30 cross-kind referential integrity check categories.

Each function returns a list of ValidationFailure (collect-all, don't
fail-fast). The top-level `validate_workspace_boot` orchestrates them.

D30 §4 splits identity checks into boot-time + per-event. The per-event
portion (event-id resolution against current workspace state; runtime
work-unit reference resolution) requires substrate-runtime context that
B1 doesn't have — those are deferred to B2 per D36's workstream order.
This module implements the boot-time portion of §4 only; the per-event
hooks land in B2 alongside the event-chain substrate capability.
"""
from __future__ import annotations

from typing import Iterable

from fresh_plan.validator.extensions import LoadedExtension
from fresh_plan.validator.types import ValidationFailure


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _split_qualified(qid: str) -> tuple[str, str]:
    """Split `<ext-id>:<id>` → (ext-id, id). Returns ("", qid) if unqualified."""
    if ":" not in qid:
        return "", qid
    head, tail = qid.split(":", 1)
    return head, tail


def _provisions_by_kind(
    loaded: dict[str, LoadedExtension]
) -> dict[str, set[str]]:
    """Index loaded extensions' provisions: kind → set of qualified-ids."""
    by_kind: dict[str, set[str]] = {}
    for ext_id, ext in loaded.items():
        for prov in ext.manifest.get("provisions", []):
            kind = prov.get("kind")
            pid = prov.get("id")
            if kind and pid:
                by_kind.setdefault(kind, set()).add(f"{ext_id}:{pid}")
    return by_kind


def _vocabulary_index(
    loaded: dict[str, LoadedExtension]
) -> dict[str, set[str]]:
    """Index vocabulary registrations: slot → set of qualified-ids."""
    by_slot: dict[str, set[str]] = {}
    for ext_id, ext in loaded.items():
        for reg in ext.manifest.get("vocabulary-registrations", []):
            slot = reg.get("slot")
            ident = reg.get("identifier")
            if slot and ident:
                by_slot.setdefault(slot, set()).add(f"{ext_id}:{ident}")
    return by_slot


# Core (non-extension-registered) vocabulary values per Phase A schemas:
CORE_PAYLOAD_SUBTYPES = frozenset(
    {"claim", "action", "state-change", "composition-change", "lifecycle-transition"}
)
CORE_ACTOR_SUBTYPES = frozenset({"human-actor", "agent-actor"})
CORE_RUNTIME_SHAPES = frozenset(
    {"interactive", "programmatic", "hosted-interactive", "hosted-programmatic"}
)
CORE_CAPABILITIES = frozenset({"hooks", "skills", "event-chain"})


def _is_registered_payload_subtype(value: str, vocab: dict[str, set[str]]) -> bool:
    if value in CORE_PAYLOAD_SUBTYPES:
        return True
    return value in vocab.get("event.payload-subtype", set())


def _is_registered_actor_subtype(value: str, vocab: dict[str, set[str]]) -> bool:
    if value in CORE_ACTOR_SUBTYPES:
        return True
    return value in vocab.get("actor.subtype", set())


def _is_registered_capability(value: str, vocab: dict[str, set[str]]) -> bool:
    if value in CORE_CAPABILITIES:
        return True
    return value in vocab.get("substrate.capabilities", set())


def _is_registered_protocol(value: str, vocab: dict[str, set[str]]) -> bool:
    return value in vocab.get("adapter.protocol-or-transport", set())


def _is_registered_work_unit_kind(value: str, vocab: dict[str, set[str]]) -> bool:
    return value in vocab.get("work-unit.kind", set())


# ---------------------------------------------------------------------------
# D30 §1: Resolution checks
# ---------------------------------------------------------------------------


def check_resolution(
    workspace: dict, loaded: dict[str, LoadedExtension]
) -> list[ValidationFailure]:
    """Every workspace.composition reference resolves to a loaded provision.

    Per D30 §1. Checked references:
        composition.shape.provision
        composition.substrate-bindings[].provision  (when present)
        composition.adapter-bindings[].provision
        composition.specialist-bindings[].provision
        composition.extensions[] → loaded
    """
    failures: list[ValidationFailure] = []
    comp = workspace.get("composition", {})
    by_kind = _provisions_by_kind(loaded)

    # composition.extensions[] → in loaded
    # Note: workspace.py orchestrator surfaces "not found in extensions-dir"
    # (resolution) and version-conflicts at a more specific path. Here we
    # only track the set of declared ids for provision-resolution checks
    # below — no redundant per-extension failure is emitted.
    declared_ext_ids = {e.get("id") for e in comp.get("extensions", [])}

    # composition.shape.provision → shape provision
    shape = comp.get("shape")
    if isinstance(shape, dict):
        prov = shape.get("provision")
        if prov:
            ext_id, _ = _split_qualified(prov)
            if ext_id and ext_id not in declared_ext_ids:
                failures.append(
                    ValidationFailure(
                        category="resolution",
                        path="composition.shape.provision",
                        value=prov,
                        reason=(
                            f"shape provision {prov!r} references extension "
                            f"{ext_id!r} which is not in composition.extensions[]"
                        ),
                    )
                )
            elif prov not in by_kind.get("shape", set()):
                failures.append(
                    ValidationFailure(
                        category="resolution",
                        path="composition.shape.provision",
                        value=prov,
                        reason=(
                            f"shape provision {prov!r} not found in any loaded "
                            "extension's provisions[]"
                        ),
                    )
                )

    # Binding arrays: substrate-bindings, adapter-bindings, specialist-bindings
    for slot, kind in [
        ("substrate-bindings", "substrate"),
        ("adapter-bindings", "adapter"),
        ("specialist-bindings", "specialist"),
    ]:
        for i, binding in enumerate(comp.get(slot, [])):
            prov = binding.get("provision")
            if not prov:
                # Per D51 §C: defensive skip on missing provision.
                # substrate-bindings may omit provision if required-capabilities
                # is present (per workspace.schema.json anyOf — capability-based
                # bindings are validated separately by check_capability_satisfaction).
                # For adapter-bindings + specialist-bindings, schema layer catches
                # missing provision; this skip avoids redundant per-resolution
                # failure when schema would have already failed.
                continue
            ext_id, _ = _split_qualified(prov)
            if ext_id and ext_id not in declared_ext_ids:
                failures.append(
                    ValidationFailure(
                        category="resolution",
                        path=f"composition.{slot}[{i}].provision",
                        value=prov,
                        reason=(
                            f"{kind} provision {prov!r} references extension "
                            f"{ext_id!r} which is not in composition.extensions[]"
                        ),
                    )
                )
            elif prov not in by_kind.get(kind, set()):
                failures.append(
                    ValidationFailure(
                        category="resolution",
                        path=f"composition.{slot}[{i}].provision",
                        value=prov,
                        reason=(
                            f"{kind} provision {prov!r} not found in any loaded "
                            "extension's provisions[]"
                        ),
                    )
                )

    return failures


# ---------------------------------------------------------------------------
# D30 §2: Capability satisfaction
# ---------------------------------------------------------------------------


def _bound_substrate_capabilities(
    workspace: dict, loaded: dict[str, LoadedExtension]
) -> set[str]:
    """Union of capabilities advertised by all bound substrates.

    Per D30 §2 + D12 (mixed bindings): all substrate-bindings'
    capabilities are unioned. Includes both substrate-provision-declared
    capabilities AND any `required-capabilities` declared on a binding
    (D30 §2 union semantics over the bound substrate set).
    """
    caps: set[str] = set()
    comp = workspace.get("composition", {})
    for binding in comp.get("substrate-bindings", []):
        prov = binding.get("provision")
        if prov:
            ext_id, prov_id = _split_qualified(prov)
            ext = loaded.get(ext_id)
            if ext is not None:
                spec = ext.provisions_loaded.get(prov_id)
                if spec is not None:
                    for cap in spec.get("capabilities", []):
                        caps.add(cap)
        # required-capabilities on a binding indicate runtime resolution
        # against any substrate providing them — they ARE the capability
        # set the workspace expects to bind. Include them in the
        # satisfiability set per D12 mixed-binding semantics.
        for cap in binding.get("required-capabilities", []) or []:
            caps.add(cap)
    return caps


def check_capability_satisfaction(
    workspace: dict, loaded: dict[str, LoadedExtension]
) -> list[ValidationFailure]:
    """Per D30 §2 — required-capabilities are unioned across bound substrates."""
    failures: list[ValidationFailure] = []
    comp = workspace.get("composition", {})
    available = _bound_substrate_capabilities(workspace, loaded)

    # Shape required-capabilities
    shape = comp.get("shape")
    if isinstance(shape, dict):
        prov = shape.get("provision")
        if prov:
            ext_id, prov_id = _split_qualified(prov)
            ext = loaded.get(ext_id)
            if ext is not None:
                spec = ext.provisions_loaded.get(prov_id)
                if spec is not None:
                    for cap in spec.get("required-capabilities", []):
                        if cap not in available:
                            failures.append(
                                ValidationFailure(
                                    category="capability",
                                    path="composition.shape.required-capabilities",
                                    value=cap,
                                    reason=(
                                        f"shape requires capability {cap!r} "
                                        "not advertised by any bound substrate"
                                    ),
                                )
                            )

    # Adapter required-substrate-capabilities
    for i, binding in enumerate(comp.get("adapter-bindings", [])):
        prov = binding.get("provision")
        if not prov:
            # Schema layer catches missing provision on adapter-bindings.
            continue
        ext_id, prov_id = _split_qualified(prov)
        ext = loaded.get(ext_id)
        if ext is None:
            # Defensive skip: upstream check_resolution records the resolution
            # failure (ext not declared OR provision not in any loaded ext).
            # Per D51 §C: silent-continue is defensive not silent-degradation.
            continue
        spec = ext.provisions_loaded.get(prov_id)
        if spec is None:
            # Defensive skip: provision spec load failure already recorded by
            # workspace.py:200-217 as resolution failure. Skip avoids double-count.
            continue
        for cap in spec.get("required-substrate-capabilities", []):
            if cap not in available:
                failures.append(
                    ValidationFailure(
                        category="capability",
                        path=f"composition.adapter-bindings[{i}].required-substrate-capabilities",
                        value=cap,
                        reason=(
                            f"adapter {prov!r} requires substrate capability "
                            f"{cap!r} not advertised by any bound substrate"
                        ),
                    )
                )

    # Specialist required-substrate-capabilities
    for i, binding in enumerate(comp.get("specialist-bindings", [])):
        prov = binding.get("provision")
        if not prov:
            # Schema layer catches missing provision on specialist-bindings.
            continue
        ext_id, prov_id = _split_qualified(prov)
        ext = loaded.get(ext_id)
        if ext is None:
            # Defensive skip: upstream check_resolution records the resolution
            # failure. Per D51 §C: silent-continue is defensive not silent-degradation.
            continue
        spec = ext.provisions_loaded.get(prov_id)
        if spec is None:
            # Defensive skip: provision spec load failure already recorded upstream.
            continue
        for cap in spec.get("required-substrate-capabilities", []):
            if cap not in available:
                failures.append(
                    ValidationFailure(
                        category="capability",
                        path=f"composition.specialist-bindings[{i}].required-substrate-capabilities",
                        value=cap,
                        reason=(
                            f"specialist {prov!r} requires substrate capability "
                            f"{cap!r} not advertised by any bound substrate"
                        ),
                    )
                )

    return failures


# ---------------------------------------------------------------------------
# D30 §3: Vocabulary resolution
# ---------------------------------------------------------------------------


def check_vocabulary_resolution(
    workspace: dict,
    loaded: dict[str, LoadedExtension],
    vocabulary_tables: dict[str, set[str]],
) -> list[ValidationFailure]:
    """Per D30 §3 — every fully-qualified vocabulary value resolves.

    Inputs scanned:
        adapter.protocol-or-transport (provision + binding-level)
        adapter.declared-event-emissions/consumptions[].payload-subtype
        specialist.supported-work-unit-kinds[]
        specialist.declared-event-emissions/subscriptions[].payload-subtype
        shape.authority-bindings[].payload-subtype
        shape.authority-bindings[].required-actor-subtype
    """
    failures: list[ValidationFailure] = []
    comp = workspace.get("composition", {})

    # Adapter-binding-level protocol-or-transport
    for i, binding in enumerate(comp.get("adapter-bindings", [])):
        pt = binding.get("protocol-or-transport")
        if pt and not _is_registered_protocol(pt, vocabulary_tables):
            failures.append(
                ValidationFailure(
                    category="vocabulary",
                    path=f"composition.adapter-bindings[{i}].protocol-or-transport",
                    value=pt,
                    reason=(
                        f"protocol-or-transport {pt!r} is not registered by any "
                        "loaded extension's vocabulary-registrations"
                    ),
                )
            )

    # Adapter provisions (loaded specs)
    for ext_id, ext in loaded.items():
        for prov in ext.manifest.get("provisions", []):
            kind = prov.get("kind")
            prov_id = prov.get("id")
            spec = ext.provisions_loaded.get(prov_id)
            if spec is None:
                continue
            base = f"loaded-extensions[{ext_id}].provisions[{prov_id}]"
            if kind == "adapter":
                pt = spec.get("protocol-or-transport")
                if pt and not _is_registered_protocol(pt, vocabulary_tables):
                    failures.append(
                        ValidationFailure(
                            category="vocabulary",
                            path=f"{base}.protocol-or-transport",
                            value=pt,
                            reason=(
                                f"protocol-or-transport {pt!r} (from adapter "
                                f"provision) is not registered"
                            ),
                        )
                    )
                for j, emission in enumerate(spec.get("declared-event-emissions", [])):
                    pst = emission.get("payload-subtype")
                    if pst and not _is_registered_payload_subtype(pst, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.declared-event-emissions[{j}].payload-subtype",
                                value=pst,
                                reason=f"payload-subtype {pst!r} is not registered",
                            )
                        )
                for j, cons in enumerate(spec.get("declared-event-consumptions", [])):
                    pst = cons.get("payload-subtype")
                    if pst and not _is_registered_payload_subtype(pst, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.declared-event-consumptions[{j}].payload-subtype",
                                value=pst,
                                reason=f"payload-subtype {pst!r} is not registered",
                            )
                        )
            elif kind == "specialist":
                for j, kind_ref in enumerate(spec.get("supported-work-unit-kinds", [])):
                    if not _is_registered_work_unit_kind(kind_ref, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.supported-work-unit-kinds[{j}]",
                                value=kind_ref,
                                reason=(
                                    f"work-unit kind {kind_ref!r} is not "
                                    "registered by any loaded extension"
                                ),
                            )
                        )
                for j, emission in enumerate(spec.get("declared-event-emissions", [])):
                    pst = emission.get("payload-subtype")
                    if pst and not _is_registered_payload_subtype(pst, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.declared-event-emissions[{j}].payload-subtype",
                                value=pst,
                                reason=f"payload-subtype {pst!r} is not registered",
                            )
                        )
                for j, sub in enumerate(spec.get("declared-event-subscriptions", [])):
                    pst = sub.get("payload-subtype")
                    if pst and not _is_registered_payload_subtype(pst, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.declared-event-subscriptions[{j}].payload-subtype",
                                value=pst,
                                reason=f"payload-subtype {pst!r} is not registered",
                            )
                        )
            elif kind == "shape":
                for j, ab in enumerate(spec.get("authority-bindings", [])):
                    pst = ab.get("payload-subtype")
                    if pst and not _is_registered_payload_subtype(pst, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.authority-bindings[{j}].payload-subtype",
                                value=pst,
                                reason=f"payload-subtype {pst!r} is not registered",
                            )
                        )
                    ras = ab.get("required-actor-subtype")
                    if ras and not _is_registered_actor_subtype(ras, vocabulary_tables):
                        failures.append(
                            ValidationFailure(
                                category="vocabulary",
                                path=f"{base}.authority-bindings[{j}].required-actor-subtype",
                                value=ras,
                                reason=f"actor-subtype {ras!r} is not registered",
                            )
                        )
            elif kind == "substrate":
                # Substrate capabilities that are qualified must be registered
                for j, cap in enumerate(spec.get("capabilities", [])):
                    if isinstance(cap, str) and ":" in cap:
                        if not _is_registered_capability(cap, vocabulary_tables):
                            failures.append(
                                ValidationFailure(
                                    category="vocabulary",
                                    path=f"{base}.capabilities[{j}]",
                                    value=cap,
                                    reason=(
                                        f"capability {cap!r} is not registered by "
                                        "any loaded extension"
                                    ),
                                )
                            )

    # Actors' subtypes (workspace runtime data; boot-time check is on subtype only)
    for i, actor in enumerate(comp.get("actors", [])):
        st = actor.get("subtype")
        if isinstance(st, str) and ":" in st:
            if not _is_registered_actor_subtype(st, vocabulary_tables):
                failures.append(
                    ValidationFailure(
                        category="vocabulary",
                        path=f"composition.actors[{i}].subtype",
                        value=st,
                        reason=f"actor-subtype {st!r} is not registered",
                    )
                )

    return failures


# ---------------------------------------------------------------------------
# D30 §4: Workspace-internal identity (boot-time portion only)
# ---------------------------------------------------------------------------
#
# Per D34 §A.5: actor/work-unit/specialist-binding references resolve against
# the workspace's *current state* (manifest + applied composition-change
# events), not just the boot-time manifest snapshot. The per-event portion
# (event.actors[].id, event.work-unit-id, etc.) needs runtime state and is
# deferred to B2 (substrate impl). B1 implements only the boot-time portion:
# agent-actor.substrate-binding → existing binding-id within manifest.


def check_workspace_internal_identity(
    workspace: dict,
) -> list[ValidationFailure]:
    """Per D30 §4 boot-time portion (per D34 §A.5 clarification).

    Per-event identity checks (event.actors[].id resolution, work-unit
    references) are deferred to B2 (require runtime state, not manifest).
    """
    failures: list[ValidationFailure] = []
    comp = workspace.get("composition", {})
    binding_ids = {b.get("binding-id") for b in comp.get("substrate-bindings", [])}

    for i, actor in enumerate(comp.get("actors", [])):
        if actor.get("subtype") == "agent-actor":
            sb = actor.get("substrate-binding")
            if sb is None:
                # Schema validation catches missing slot; skip here.
                continue
            if sb not in binding_ids:
                failures.append(
                    ValidationFailure(
                        category="identity",
                        path=f"composition.actors[{i}].substrate-binding",
                        value=sb,
                        reason=(
                            f"agent-actor.substrate-binding {sb!r} does not match "
                            "any binding-id in composition.substrate-bindings[]"
                        ),
                    )
                )

    # Also: each agent-actor's id must be unique within actors; substrate
    # binding-ids unique; adapter / specialist binding-ids unique. Schema
    # doesn't enforce uniqueness across these slots. (D7: identifiers are
    # workspace-scoped.)
    seen_actor_ids: set[str] = set()
    for i, actor in enumerate(comp.get("actors", [])):
        aid = actor.get("id")
        if aid in seen_actor_ids:
            failures.append(
                ValidationFailure(
                    category="identity",
                    path=f"composition.actors[{i}].id",
                    value=aid,
                    reason=f"duplicate actor.id {aid!r} within workspace",
                )
            )
        if aid is not None:
            seen_actor_ids.add(aid)

    for slot in ("substrate-bindings", "adapter-bindings", "specialist-bindings"):
        seen: set[str] = set()
        for i, binding in enumerate(comp.get(slot, [])):
            bid = binding.get("binding-id")
            if bid in seen:
                failures.append(
                    ValidationFailure(
                        category="identity",
                        path=f"composition.{slot}[{i}].binding-id",
                        value=bid,
                        reason=f"duplicate binding-id {bid!r} within composition.{slot}",
                    )
                )
            if bid is not None:
                seen.add(bid)

    return failures


# ---------------------------------------------------------------------------
# D30 §5: Binding availability
# ---------------------------------------------------------------------------


def check_binding_availability(
    workspace: dict, loaded: dict[str, LoadedExtension]
) -> list[ValidationFailure]:
    """Per D30 §5 + D32 §1 — specialist required-adapter-bindings satisfiability.

    For each specialist binding, look up the specialist provision spec
    and check that every entry in its `required-adapter-bindings[]`
    (each a qualified adapter-provision id) is matched by at least one
    workspace `adapter-bindings[].provision`. Multiple matching bindings
    are allowed (D32 §1: framework verifies satisfiability, runtime
    picks).
    """
    failures: list[ValidationFailure] = []
    comp = workspace.get("composition", {})
    bound_adapter_provisions: set[str] = set()
    for binding in comp.get("adapter-bindings", []):
        prov = binding.get("provision")
        if prov:
            bound_adapter_provisions.add(prov)

    for i, sp_binding in enumerate(comp.get("specialist-bindings", [])):
        prov = sp_binding.get("provision")
        if not prov:
            # Schema layer catches missing provision on specialist-bindings.
            continue
        ext_id, prov_id = _split_qualified(prov)
        ext = loaded.get(ext_id)
        if ext is None:
            # Defensive skip: upstream check_resolution records the resolution
            # failure. Per D51 §C: silent-continue is defensive not silent-degradation.
            continue
        spec = ext.provisions_loaded.get(prov_id)
        if spec is None:
            continue
        for required in spec.get("required-adapter-bindings", []):
            if required not in bound_adapter_provisions:
                failures.append(
                    ValidationFailure(
                        category="binding",
                        path=f"composition.specialist-bindings[{i}].required-adapter-bindings",
                        value=required,
                        reason=(
                            f"specialist {prov!r} requires an adapter binding "
                            f"of provision {required!r}; no matching entry in "
                            "composition.adapter-bindings[]"
                        ),
                    )
                )
    return failures


# ---------------------------------------------------------------------------
# Path helper for absolute_path
# ---------------------------------------------------------------------------


def format_jsonpath(parts: Iterable) -> str:
    """Render a JSON-pointer-style path from jsonschema's absolute_path deque."""
    out: list[str] = []
    for p in parts:
        if isinstance(p, int):
            out.append(f"[{p}]")
        else:
            if out:
                out.append(f".{p}")
            else:
                out.append(str(p))
    return "".join(out) if out else "<root>"
