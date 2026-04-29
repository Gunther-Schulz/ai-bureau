"""Migration: office-config schema v2 → v3.

v2 → v3 changes (per design-review/foundations-20260429.md, Subsystem 5):

- **Merge `office` + `identity`** into a single `office` block. All
  identity fields (address_lines, signature_block, phone, etc.) move
  into `office`.
- **Merge `practices[]` + `partners[]`** into `actors[]` with a
  `kind: internal|external` discriminator. Practices map to internal;
  partners map to external. Order: internal first, then external.
- **Rename `paths` → `roots`** with shorter field names:
  - paths.state_root        → roots.state
  - paths.references_root   → roots.references
  - paths.projects_root     → roots.projects
  - paths.local_repos_root  → roots.local_repos
- **Move `templates.office_style_dir` → `roots.office_style_dir`**.
- **Drop `extensions:` block entirely**. Manifests are now discovered by
  walking `<repo>/extensions/` filtered by scope (see config.py).
- **Convert `integrations` map → list**. v2's
  `{email: {...}, calendar: {...}, ...}` becomes
  `[{class: email, ...}, {class: calendar, ...}, ...]`. Entries with
  `adapter: none` are dropped (they were no-ops); declare a class
  only if you intend an actual adapter.

The migration is conservative: every field with a v2 value is carried
forward into v3. The `extensions:` block is silently dropped (its
content was already derived data — manifest discovery handles it now).
"""
from __future__ import annotations

from copy import deepcopy


def migrate(data: dict) -> dict:
    out = deepcopy(data)
    out["schema_version"] = 3

    # --- office + identity merge -----------------------------------------
    office = out.get("office") or {}
    identity = out.pop("identity", None) or {}
    # Identity fields fold into office. Office's existing fields take
    # precedence in the unlikely case of overlap (none expected).
    for key, val in identity.items():
        if key not in office:
            office[key] = val
    out["office"] = office

    # --- practices + partners → actors -----------------------------------
    practices = out.pop("practices", None) or []
    partners = out.pop("partners", None) or []
    actors: list[dict] = []
    for p in practices:
        actor = dict(p)
        actor["kind"] = "internal"
        actors.append(actor)
    for p in partners:
        actor = dict(p)
        actor["kind"] = "external"
        actors.append(actor)
    out["actors"] = actors

    # --- paths → roots ---------------------------------------------------
    paths = out.pop("paths", None) or {}
    templates = out.get("templates") or {}
    office_style_dir = templates.pop("office_style_dir", None)
    roots: dict = {}
    if "state_root" in paths:
        roots["state"] = paths["state_root"]
    if "references_root" in paths:
        roots["references"] = paths["references_root"]
    if "projects_root" in paths:
        roots["projects"] = paths["projects_root"]
    if "local_repos_root" in paths:
        roots["local_repos"] = paths["local_repos_root"]
    if office_style_dir is not None:
        roots["office_style_dir"] = office_style_dir
    out["roots"] = roots
    if templates:
        out["templates"] = templates
    else:
        out.pop("templates", None)

    # --- drop extensions block (now derived) -----------------------------
    out.pop("extensions", None)

    # --- integrations map → list -----------------------------------------
    integrations_v2 = out.pop("integrations", None) or {}
    integrations_v3: list[dict] = []
    if isinstance(integrations_v2, dict):
        for class_name, conf in integrations_v2.items():
            adapter = (conf or {}).get("adapter") or "none"
            if adapter == "none":
                continue  # drop no-op entries
            integrations_v3.append({
                "class": class_name,
                "adapter": adapter,
                "config": (conf or {}).get("config") or {},
            })
    elif isinstance(integrations_v2, list):
        # Already in v3 shape (rare — manual edit). Pass through.
        integrations_v3 = list(integrations_v2)
    out["integrations"] = integrations_v3

    return out
