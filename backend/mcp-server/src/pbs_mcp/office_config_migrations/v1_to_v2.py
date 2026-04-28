"""Migration: office-config schema v1 → v2.

v1 → v2 changes:
  - Adds top-level `scope: {domains: [], states: []}` (empty defaults).
  - Reshapes `extensions.references_manifests` from a flat
    `{<state>: <path>}` dict into a layered
    `{universal: <path>, domain: {}, state: {<state>: <path>}}` map.
  - Adds parallel `extensions.doctypes_manifests` with the same shape.
  - Adds `integrations: {email, calendar, scanner, phone, accounting}`
    with all adapters defaulting to `none`.

The repo's universal references manifest is at
`extensions/universal/references-manifest.yaml` post-Phase-1; this
migration does NOT auto-populate the universal pointer because it
depends on the deployment's repo location. The user must re-run
setup-office (or hand-edit) to register the universal manifest.

Migration is conservative: existing state-extension entries are
preserved verbatim under `state:`. The user gets a non-empty config
that loads, with empty `scope.domains`/`scope.states` until they pick
a scope via setup-office.
"""
from __future__ import annotations

from copy import deepcopy


def migrate(data: dict) -> dict:
    out = deepcopy(data)
    out["schema_version"] = 2

    out.setdefault("scope", {"domains": [], "states": []})

    extensions = out.get("extensions") or {}

    old_refs = extensions.get("references_manifests")
    new_refs = {"universal": None, "domain": {}, "state": {}}
    if isinstance(old_refs, dict):
        if "universal" in old_refs or "domain" in old_refs or "state" in old_refs:
            # Already in v2 shape (rare — manual edits).
            new_refs.update({k: v for k, v in old_refs.items() if k in new_refs})
        else:
            # Flat {state: path} — migrate to state[].
            new_refs["state"] = dict(old_refs)
    extensions["references_manifests"] = new_refs

    extensions.setdefault(
        "doctypes_manifests",
        {"universal": None, "domain": {}, "state": {}},
    )
    out["extensions"] = extensions

    out.setdefault("integrations", {
        "email": {"adapter": "none", "config": {}},
        "calendar": {"adapter": "none", "config": {}},
        "scanner": {"adapter": "none", "config": {}},
        "phone": {"adapter": "none", "config": {}},
        "accounting": {"adapter": "none", "config": {}},
    })

    return out
