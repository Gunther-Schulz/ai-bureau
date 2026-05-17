"""Shape-migration classifier per D54 §B.1 — Phase B forward-bar contract.

Pure-function classifier comparing prior shape spec vs new shape spec
per the D54 §B.1 per-slot table. Returns ordered list of
``(slot, prior_value, new_value, category)`` tuples where ``category`` is
one of ``{"safe-in-place", "new-era", "breaking"}``.

Phase B forward-bar: classifier + ``FAILURE_CATEGORIES`` entry
``"shape-migration-unsafe"`` exist; substrate/validator integration is
deferred to Phase C+ once a persistence-layer source-of-truth for "prior
shape version" lands (per D54 §D D-1).

Per D54 §B.1 — slot-by-slot classification rules:

- ``id``: any change → breaking (D7 mandates exactly-1-shape; id-change =
  new workspace).
- ``version``: metadata-only patch (safe-in-place), additive minor
  (new-era), removal/narrowing major (breaking). The version slot's
  classification is informational; the *content* differences across
  other slots drive the migration-safety call.
- ``actor-requirements``: tightening ``min`` upward or ``max`` downward
  on existing subtype → new-era; loosening (``min`` downward, ``max``
  upward, adding optional subtype) → safe-in-place; removing a
  required subtype → breaking.
- ``required-capabilities[]``: additive → new-era; removal →
  breaking.
- ``optional-capabilities[]``: additive or removal → safe-in-place
  (loosens).
- ``authority-bindings[]``: loosening (widening role / actor-subtype) →
  safe-in-place; tightening (narrowing) or adding new binding →
  new-era; removing a binding existing events relied on → breaking.
- ``roles[]``: additive → safe-in-place; role-semantics change under
  stable id → new-era; removal → breaking.
- ``hooks[]``: additive or description clarification → safe-in-place;
  new-firing on existing payload-subtypes → new-era; removal → breaking.
"""
from __future__ import annotations

from typing import Any


# Slot-classification category vocabulary per D54 §B.2.
_SAFE = "safe-in-place"
_NEW_ERA = "new-era"
_BREAKING = "breaking"


def _bindings_by_key(bindings: list[dict]) -> dict[tuple, dict]:
    """Index authority-bindings by (payload-subtype, qualifier) tuple."""
    out: dict[tuple, dict] = {}
    for b in bindings or []:
        key = (b.get("payload-subtype"), b.get("qualifier"))
        out[key] = b
    return out


def _roles_by_id(roles: list) -> dict[str, dict]:
    """Index roles[] by id slot (D13 roles are dict objects with id)."""
    out: dict[str, dict] = {}
    for r in roles or []:
        if isinstance(r, dict):
            rid = r.get("id")
            if rid is not None:
                out[rid] = r
        elif isinstance(r, str):
            out[r] = {"id": r}
    return out


def _hooks_by_name(hooks: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for h in hooks or []:
        if isinstance(h, dict):
            name = h.get("name")
            if name is not None:
                out[name] = h
    return out


def classify_shape_change(
    prior_spec: dict, new_spec: dict
) -> list[tuple[str, Any, Any, str]]:
    """Classify per-slot changes between two shape specs per D54 §B.1.

    Returns an ordered list of ``(slot_path, prior_value, new_value, category)``
    tuples. ``category`` is one of ``"safe-in-place"``, ``"new-era"``,
    ``"breaking"`` per the D54 table.

    Slots reflecting NO change between specs are omitted from the result.
    Per the framework's fail-closed bar: a returned ``"breaking"`` or
    ``"new-era"`` entry is what the eventual boot-time activation (deferred
    per D54 §D D-1) would surface as ``WorkspaceBootError(category=
    "shape-migration-unsafe")``.
    """
    changes: list[tuple[str, Any, Any, str]] = []

    # id — any change is breaking per D7 exactly-1-shape semantics.
    prior_id = prior_spec.get("id")
    new_id = new_spec.get("id")
    if prior_id != new_id:
        changes.append(("id", prior_id, new_id, _BREAKING))

    # version — informational; semver-bump direction is shape-author concern.
    prior_ver = prior_spec.get("version")
    new_ver = new_spec.get("version")
    if prior_ver != new_ver:
        # Version-string difference alone is metadata-only safe-in-place;
        # the *content* of other slots drives the actual migration call.
        changes.append(("version", prior_ver, new_ver, _SAFE))

    # actor-requirements — tightening / loosening / removal classification.
    prior_reqs = prior_spec.get("actor-requirements")
    new_reqs = new_spec.get("actor-requirements")
    if prior_reqs != new_reqs:
        if isinstance(prior_reqs, dict) and isinstance(new_reqs, dict):
            # Per-subtype comparison.
            for subtype, prior_c in prior_reqs.items():
                if subtype not in new_reqs:
                    # Required subtype removed → breaking.
                    changes.append(
                        (
                            f"actor-requirements.{subtype}",
                            prior_c,
                            None,
                            _BREAKING,
                        )
                    )
                    continue
                new_c = new_reqs[subtype]
                if prior_c == new_c:
                    continue
                # Compare min/max.
                if isinstance(prior_c, dict) and isinstance(new_c, dict):
                    prior_min = prior_c.get("min")
                    new_min = new_c.get("min")
                    prior_max = prior_c.get("max")
                    new_max = new_c.get("max")
                    tightening = (
                        (
                            prior_min is not None
                            and new_min is not None
                            and new_min > prior_min
                        )
                        or (
                            prior_max is not None
                            and new_max is not None
                            and new_max < prior_max
                        )
                    )
                    loosening = (
                        (
                            prior_min is not None
                            and new_min is not None
                            and new_min < prior_min
                        )
                        or (
                            prior_max is not None
                            and new_max is not None
                            and new_max > prior_max
                        )
                        or (prior_max is not None and new_max is None)
                        or (prior_min is not None and new_min is None)
                    )
                    if tightening and not loosening:
                        cat = _NEW_ERA
                    elif loosening and not tightening:
                        cat = _SAFE
                    else:
                        cat = _NEW_ERA
                    changes.append(
                        (
                            f"actor-requirements.{subtype}",
                            prior_c,
                            new_c,
                            cat,
                        )
                    )
                else:
                    changes.append(
                        (
                            f"actor-requirements.{subtype}",
                            prior_c,
                            new_c,
                            _NEW_ERA,
                        )
                    )
            for subtype, new_c in new_reqs.items():
                if subtype not in prior_reqs:
                    # New subtype added: loosens if optional, tightens if required.
                    changes.append(
                        (
                            f"actor-requirements.{subtype}",
                            None,
                            new_c,
                            _SAFE,
                        )
                    )
        else:
            # Non-dict reqs (e.g., "none" → dict or vice-versa): treat as new-era.
            changes.append(("actor-requirements", prior_reqs, new_reqs, _NEW_ERA))

    # required-capabilities[] — additive new-era; removal breaking.
    prior_req_caps = set(prior_spec.get("required-capabilities", []) or [])
    new_req_caps = set(new_spec.get("required-capabilities", []) or [])
    for cap in sorted(new_req_caps - prior_req_caps):
        changes.append((f"required-capabilities.{cap}", None, cap, _NEW_ERA))
    for cap in sorted(prior_req_caps - new_req_caps):
        changes.append((f"required-capabilities.{cap}", cap, None, _BREAKING))

    # optional-capabilities[] — additive or removal both safe-in-place.
    prior_opt_caps = set(prior_spec.get("optional-capabilities", []) or [])
    new_opt_caps = set(new_spec.get("optional-capabilities", []) or [])
    for cap in sorted(new_opt_caps - prior_opt_caps):
        changes.append((f"optional-capabilities.{cap}", None, cap, _SAFE))
    for cap in sorted(prior_opt_caps - new_opt_caps):
        changes.append((f"optional-capabilities.{cap}", cap, None, _SAFE))

    # authority-bindings[] — keyed by (payload-subtype, qualifier).
    prior_ab = _bindings_by_key(prior_spec.get("authority-bindings", []) or [])
    new_ab = _bindings_by_key(new_spec.get("authority-bindings", []) or [])
    for key, prior_b in prior_ab.items():
        if key not in new_ab:
            changes.append(
                (f"authority-bindings.{key}", prior_b, None, _BREAKING)
            )
            continue
        new_b = new_ab[key]
        if prior_b == new_b:
            continue
        # Compare required-role and required-actor-subtype.
        prior_role = prior_b.get("required-role")
        new_role = new_b.get("required-role")
        prior_subtype = prior_b.get("required-actor-subtype")
        new_subtype = new_b.get("required-actor-subtype")
        # Loosening = relaxing role (None) or relaxing actor-subtype (None).
        if (prior_role is not None and new_role is None) or (
            prior_subtype is not None and new_subtype is None
        ):
            cat = _SAFE
        elif prior_role == new_role and prior_subtype == new_subtype:
            cat = _SAFE
        else:
            cat = _NEW_ERA
        changes.append((f"authority-bindings.{key}", prior_b, new_b, cat))
    for key, new_b in new_ab.items():
        if key not in prior_ab:
            # New binding tightens the contract → new-era.
            changes.append(
                (f"authority-bindings.{key}", None, new_b, _NEW_ERA)
            )

    # roles[] — additive safe; semantics-change under stable id new-era;
    # removal breaking.
    prior_roles = _roles_by_id(prior_spec.get("roles", []) or [])
    new_roles = _roles_by_id(new_spec.get("roles", []) or [])
    for rid, prior_r in prior_roles.items():
        if rid not in new_roles:
            changes.append((f"roles.{rid}", prior_r, None, _BREAKING))
            continue
        new_r = new_roles[rid]
        if prior_r != new_r:
            changes.append((f"roles.{rid}", prior_r, new_r, _NEW_ERA))
    for rid, new_r in new_roles.items():
        if rid not in prior_roles:
            changes.append((f"roles.{rid}", None, new_r, _SAFE))

    # hooks[] — keyed by name; additive safe; new-firing new-era; removal
    # breaking. (Distinguishing "new-firing" from "description clarification"
    # requires inspecting the firing trigger; classifier returns new-era for
    # any non-identical hook body under stable name and lets the shape-author
    # downgrade in their migration-safety review.)
    prior_hooks = _hooks_by_name(prior_spec.get("hooks", []) or [])
    new_hooks = _hooks_by_name(new_spec.get("hooks", []) or [])
    for name, prior_h in prior_hooks.items():
        if name not in new_hooks:
            changes.append((f"hooks.{name}", prior_h, None, _BREAKING))
            continue
        new_h = new_hooks[name]
        if prior_h != new_h:
            changes.append((f"hooks.{name}", prior_h, new_h, _NEW_ERA))
    for name, new_h in new_hooks.items():
        if name not in prior_hooks:
            changes.append((f"hooks.{name}", None, new_h, _SAFE))

    return changes
