"""Schema loading.

Loads all 15 Phase A schemas (D35 inventory) with cross-file `$ref`
resolution. Uses the `referencing` library (the canonical pattern for
jsonschema 4.18+; `RefResolver` is deprecated). Schemas are registered
by their canonical `$id` URL (https://pbs-bureau.dev/fresh-plan/schemas/...);
the relative `$ref`s in the schemas (e.g., `actor.schema.json` from
within `workspace.schema.json`) resolve against the referrer's `$id`.

Per the `fresh-plan/schemas/README.md` convention, all schemas must be
loaded before any validation — single-schema loading fails on $ref.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


# Canonical base URL for all fresh-plan schema $ids.
SCHEMA_BASE_URL = "https://pbs-bureau.dev/fresh-plan/schemas/"


# Default location of Phase A schemas relative to this file (../../../../schemas).
# Two parents up from this file is fresh_plan/, then ../../../schemas reaches
# fresh-plan/schemas/. Computed dynamically so the package works from any cwd.
def default_schemas_dir() -> Path:
    """Return the absolute path to fresh-plan/schemas/ (Phase A locked artifacts)."""
    # impl/src/fresh_plan/validator/schemas.py
    # parents[0]=validator, [1]=fresh_plan, [2]=src, [3]=impl, [4]=fresh-plan
    here = Path(__file__).resolve()
    return here.parents[4] / "schemas"


@dataclass
class SchemaStore:
    """Loaded schemas + a Registry suitable for per-schema validators.

    Keep `store` (filename → dict) for direct lookup by filename, and
    `registry` for jsonschema's `referencing.Registry` interface. Both
    point at the same schema dicts; do not mutate after construction.
    """

    store: dict[str, dict]
    registry: Registry

    def validator_for(self, filename: str) -> Draft202012Validator:
        """Return a Draft202012Validator bound to the schema at `filename`."""
        if filename not in self.store:
            raise KeyError(f"schema {filename!r} not loaded")
        return Draft202012Validator(self.store[filename], registry=self.registry)


def load_schemas(schemas_dir: Optional[Path] = None) -> SchemaStore:
    """Load all `*.schema.json` files from `schemas_dir`.

    Defaults to `fresh-plan/schemas/` (resolved relative to this package).
    Raises ValueError if a schema is missing `$id`.
    """
    if schemas_dir is None:
        schemas_dir = default_schemas_dir()
    schemas_dir = Path(schemas_dir).resolve()
    if not schemas_dir.is_dir():
        raise FileNotFoundError(f"schemas directory not found: {schemas_dir}")

    store: dict[str, dict] = {}
    resources: list[tuple[str, Resource]] = []
    for path in sorted(schemas_dir.glob("*.schema.json")):
        with path.open() as f:
            schema = json.load(f)
        if "$id" not in schema:
            raise ValueError(f"schema {path.name} missing $id")
        store[path.name] = schema
        resources.append((schema["$id"], Resource(contents=schema, specification=DRAFT202012)))

    if not store:
        raise FileNotFoundError(f"no schemas found in {schemas_dir}")

    registry = Registry().with_resources(resources)
    return SchemaStore(store=store, registry=registry)


def schema_filename_for_kind(kind: str) -> str:
    """Map a provision-kind to its formal schema filename."""
    # Per D29 §3: provisions are kind = substrate | shape | adapter | specialist.
    mapping = {
        "substrate": "substrate.schema.json",
        "shape": "shape.schema.json",
        "adapter": "adapter.schema.json",
        "specialist": "specialist.schema.json",
    }
    if kind not in mapping:
        raise ValueError(f"no schema for provision kind {kind!r}")
    return mapping[kind]


def iter_validation_errors(
    schema_store: SchemaStore, schema_filename: str, instance: dict
) -> Iterable:
    """Iterate JSON Schema errors for `instance` against the named schema."""
    return schema_store.validator_for(schema_filename).iter_errors(instance)
