"""Top-level orchestrator for the conformance validator (B1).

Order roughly mirrors D29 §validation flow + D30:

    1. Schema-validate workspace manifest (Phase A formal schema).
    2. Discover available extensions on disk.
    3. Resolve composition.extensions[] → load each extension manifest
       (D29 step 2). Multiple versions per extension may be discovered;
       a per-extension union of declared ranges drives the selection
       (D33 §B). Transitive `dependencies.required-extensions[]` extend
       the requirement set.
    4. Schema-validate each loaded extension manifest (D29 step 3).
    5. Schema-validate each provision's loaded spec against its kind
       schema.
    6. Build dependency graph + detect cycles (D32 §2).
    7. Compute load order via topological sort (D32 §3); merge
       vocabulary tables in that order.
    8. Run D30 cross-kind checks (§1 resolution, §2 capability, §3
       vocabulary, §4 identity boot-time portion, §5 binding).

Failure collection is collect-all: each step records failures and
continues; later steps that need loaded state guard accordingly.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from fresh_plan.validator import checks
from fresh_plan.validator.dependency import (
    DependencyGraph,
    VersionConflict,
    find_cycle,
    resolve_versions,
    topological_sort,
)
from fresh_plan.validator.extensions import (
    LoadedExtension,
    discover_extensions,
    load_extension,
)
from fresh_plan.validator.schemas import (
    SchemaStore,
    load_schemas,
    schema_filename_for_kind,
)
from fresh_plan.validator.types import ValidationFailure, ValidationResult


def validate_workspace_boot(
    manifest: dict,
    extensions_dir: Path,
    schemas_dir: Optional[Path] = None,
) -> ValidationResult:
    """Validate a workspace boot per D29 + D30 + D32 + D33.

    Args:
        manifest: parsed workspace manifest (JSON / YAML already parsed).
        extensions_dir: directory containing on-disk extensions.
        schemas_dir: override for the Phase A schemas directory (testing).

    Returns:
        ValidationResult with success + all collected failures + (on
        success) loaded_extensions map and vocabulary_tables.
    """
    failures: list[ValidationFailure] = []
    extensions_dir = Path(extensions_dir)

    # --- 1. Schema-validate workspace manifest ---
    schema_store = load_schemas(schemas_dir)
    failures += _schema_validate(
        schema_store, "workspace.schema.json", manifest, path_prefix="workspace"
    )

    # If the manifest is so malformed it lacks a composition section,
    # subsequent checks cannot run usefully — return early.
    if not isinstance(manifest.get("composition"), dict):
        return ValidationResult(success=False, failures=failures)

    # --- 2. Discover + 3. resolve composition.extensions[] ---
    available = discover_extensions(extensions_dir)
    # `available[ext-id]` → {version: manifest_path}
    available_versions = {ext_id: sorted(versions.keys()) for ext_id, versions in available.items()}

    loaded: dict[str, LoadedExtension] = {}
    composition_extensions = manifest["composition"].get("extensions", [])

    # Build initial requirements set from workspace.composition.extensions[].
    # requirements: ext-id → list of (declarer, range)
    requirements: dict[str, list[tuple[str, str]]] = {}
    for ext_ref in composition_extensions:
        ext_id = ext_ref.get("id")
        rng = ext_ref.get("version-range")
        if ext_id and rng:
            requirements.setdefault(ext_id, []).append(("workspace", rng))

    # Iteratively pull in transitive dependencies. At each iteration:
    #   (a) resolve current requirements to selected versions;
    #   (b) load any newly-selected (ext, version) manifests;
    #   (c) merge their `required-extensions[]` into requirements;
    #   (d) repeat until requirements stabilize.
    # If version-conflicts arise, record them and stop adding transitives
    # for the affected extension (subsequent checks gracefully degrade).
    resolved_versions: dict[str, str] = {}
    version_conflicts: list[VersionConflict] = []
    seen_ranges: dict[str, set[tuple[str, str]]] = {}

    for _iteration in range(64):  # generous safety bound; cycles caught separately
        changed = False
        for ext_id, decls in requirements.items():
            seen_ranges.setdefault(ext_id, set())
            new_decls = [d for d in decls if d not in seen_ranges[ext_id]]
            if new_decls:
                changed = True
                seen_ranges[ext_id].update(new_decls)

        if not changed and resolved_versions:
            break

        selected, conflicts = resolve_versions(requirements, available_versions)
        version_conflicts = conflicts
        for ext_id, version in selected.items():
            prev = resolved_versions.get(ext_id)
            if prev == version:
                continue
            resolved_versions[ext_id] = version
            manifest_path = available[ext_id][version]
            ext, load_errs = load_extension(ext_id, version, manifest_path)
            for err in load_errs:
                failures.append(
                    ValidationFailure(
                        category="resolution",
                        path=f"loaded-extensions[{ext_id}@{version}]",
                        reason=err,
                        value=err,
                    )
                )
            loaded[ext_id] = ext
            changed = True
            # Pull transitive requirements from this manifest
            for dep in ext.manifest.get("dependencies", {}).get("required-extensions", []):
                d_id = dep.get("id")
                d_rng = dep.get("version-range")
                if d_id and d_rng:
                    decl = (ext_id, d_rng)
                    seen_ranges.setdefault(d_id, set())
                    if decl not in seen_ranges[d_id]:
                        requirements.setdefault(d_id, []).append(decl)

        if not changed:
            break

    # Surface version conflicts (D33 §B)
    for conflict in version_conflicts:
        failures.append(
            ValidationFailure(
                category="version-conflict",
                path=f"composition.extensions[id={conflict.extension_id}]",
                value=conflict.extension_id,
                reason=conflict.reason,
                declarers=[f"{declarer}: {rng}" for declarer, rng in conflict.declarers],
            )
        )

    # Surface unresolved extensions (declared in composition but not on disk).
    # Skip ones already flagged as version-conflicts (where the range
    # intersection was non-empty but no local version satisfied it). The
    # check_resolution check will catch "extension not in loaded" downstream,
    # but only surfaces it once per extension here for clarity at the
    # composition-extensions level.
    conflict_ids = {c.extension_id for c in version_conflicts}
    reported_missing: set[str] = set()
    for ext_ref in composition_extensions:
        ext_id = ext_ref.get("id")
        if ext_id and ext_id not in loaded and ext_id not in conflict_ids:
            if ext_id not in available and ext_id not in reported_missing:
                failures.append(
                    ValidationFailure(
                        category="resolution",
                        path=f"composition.extensions[id={ext_id}]",
                        value=ext_id,
                        reason=(
                            f"extension {ext_id!r} declared in composition.extensions[] "
                            "but not found in extensions-dir"
                        ),
                    )
                )
                reported_missing.add(ext_id)

    # --- 4. Schema-validate each loaded extension manifest ---
    for ext_id, ext in loaded.items():
        failures += _schema_validate(
            schema_store,
            "extension-manifest.schema.json",
            ext.manifest,
            path_prefix=f"loaded-extensions[{ext_id}]",
        )

    # --- 5. Schema-validate each provision's loaded spec ---
    for ext_id, ext in loaded.items():
        for prov in ext.manifest.get("provisions", []):
            kind = prov.get("kind")
            pid = prov.get("id")
            if not kind or not pid:
                continue
            spec = ext.provisions_loaded.get(pid)
            if spec is None:
                if pid in ext.provision_load_errors:
                    # Already recorded as a resolution failure (or non-error
                    # if unresolved URL). Skip schema validation.
                    failures.append(
                        ValidationFailure(
                            category="resolution",
                            path=f"loaded-extensions[{ext_id}].provisions[{pid}]",
                            value=ext.provision_load_errors[pid],
                            reason=ext.provision_load_errors[pid],
                        )
                    )
                continue
            try:
                schema_filename = schema_filename_for_kind(kind)
            except ValueError as e:
                failures.append(
                    ValidationFailure(
                        category="schema",
                        path=f"loaded-extensions[{ext_id}].provisions[{pid}].kind",
                        value=kind,
                        reason=str(e),
                    )
                )
                continue
            failures += _schema_validate(
                schema_store,
                schema_filename,
                spec,
                path_prefix=f"loaded-extensions[{ext_id}].provisions[{pid}]",
            )

    # --- 6. Cycle detection (D32 §2) ---
    graph = _build_dependency_graph(loaded)
    sorted_nodes, remainder = topological_sort(graph)
    if remainder:
        cycle = find_cycle(graph, remainder)
        failures.append(
            ValidationFailure(
                category="circular-dependency",
                path="composition.extensions",
                value=cycle or remainder,
                reason=(
                    "circular dependency among extensions: "
                    + " -> ".join(cycle) if cycle else
                    f"unsorted remainder (cycle present): {remainder}"
                ),
            )
        )

    # --- 7. Merge vocabulary tables in load order ---
    # vocabulary_tables: slot -> set of qualified-ids
    vocabulary_tables: dict[str, set[str]] = {}
    for ext_id in sorted_nodes:
        ext = loaded.get(ext_id)
        if ext is None:
            continue
        for reg in ext.manifest.get("vocabulary-registrations", []):
            slot = reg.get("slot")
            ident = reg.get("identifier")
            if slot and ident:
                vocabulary_tables.setdefault(slot, set()).add(f"{ext_id}:{ident}")

    # --- 8. D30 checks ---
    # Skip vocabulary-resolution if no extensions loaded (no vocabularies to
    # resolve against — orchestration would emit noise).
    failures += checks.check_resolution(manifest, loaded)
    failures += checks.check_workspace_internal_identity(manifest)
    if loaded:
        failures += checks.check_capability_satisfaction(manifest, loaded)
        failures += checks.check_vocabulary_resolution(manifest, loaded, vocabulary_tables)
        failures += checks.check_binding_availability(manifest, loaded)

    success = len(failures) == 0
    return ValidationResult(
        success=success,
        failures=failures,
        loaded_extensions={k: v.manifest for k, v in loaded.items()} if success else None,
        vocabulary_tables=(
            {k: sorted(v) for k, v in vocabulary_tables.items()} if success else None
        ),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _schema_validate(
    schema_store: SchemaStore, schema_filename: str, instance: dict, path_prefix: str
) -> list[ValidationFailure]:
    """Run JSON Schema validation, wrap errors as ValidationFailures."""
    validator = schema_store.validator_for(schema_filename)
    out: list[ValidationFailure] = []
    for err in validator.iter_errors(instance):
        path_tail = checks.format_jsonpath(err.absolute_path)
        joined = path_prefix if path_tail == "<root>" else f"{path_prefix}.{path_tail}"
        out.append(
            ValidationFailure(
                category="schema",
                path=joined,
                value=err.instance if not isinstance(err.instance, (dict, list)) else None,
                reason=err.message,
            )
        )
    return out


def _build_dependency_graph(loaded: dict[str, LoadedExtension]) -> DependencyGraph:
    """Build graph from loaded extensions' dependencies.required-extensions[]."""
    g = DependencyGraph()
    for ext_id, ext in loaded.items():
        g.add_node(ext_id)
        for dep in ext.manifest.get("dependencies", {}).get("required-extensions", []):
            d_id = dep.get("id")
            if d_id:
                # `ext_id` depends on `d_id`; load d_id before ext_id.
                g.add_edge(d_id, ext_id)
    return g
