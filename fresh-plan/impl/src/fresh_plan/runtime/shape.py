"""Shape runtime — D13 policy bundle attached to a substrate.

Per D13, the shape kind carries substantive identity as a policy bundle of
authority-bindings, roles, hooks, actor-requirements, and capability
requirements. Per D26, this module is intentionally a *generic* minimal
shape impl — not practitioner-shape (pioneer-instance bias avoidance).

Runtime concerns owned here:
  - Per-event authority-binding enforcement (D13 authority-bindings).
  - Hook-name stub registration so declared hooks are observable / firable.

Out of scope (handled elsewhere):
  - actor-requirements cardinality — workspace-level concern, boot-time
    (B1 / future).
  - required-capabilities — resolved at boot via the B1 capability check.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from fresh_plan.runtime.hooks import HookRegistry
from fresh_plan.runtime.workspace_state import WorkspaceState
from fresh_plan.validator.types import ValidationFailure


def _stub_handler(ctx: dict) -> None:
    """No-op handler stub shared across declared hook names."""
    return None


@dataclass
class GenericShape:
    """Generic minimal shape impl per D13 + D26.

    Holds the loaded shape spec dict and exposes the slot accessors plus
    runtime enforcement (authority-binding check + hook stub registration).
    """

    spec: dict

    @property
    def id(self) -> str:
        return self.spec["id"]

    @property
    def version(self) -> str:
        return self.spec["version"]

    @property
    def authority_bindings(self) -> list[dict]:
        return list(self.spec.get("authority-bindings", []) or [])

    @property
    def roles(self) -> list[dict]:
        return list(self.spec.get("roles", []) or [])

    @property
    def hooks(self) -> list[dict]:
        return list(self.spec.get("hooks", []) or [])

    @property
    def required_capabilities(self) -> list[str]:
        return list(self.spec.get("required-capabilities", []) or [])

    @property
    def optional_capabilities(self) -> list[str]:
        return list(self.spec.get("optional-capabilities", []) or [])

    @property
    def actor_requirements(self) -> Any:
        return self.spec.get("actor-requirements")

    # ---------------------------------------------------------------
    # Per-event authority-binding enforcement (D13)
    # ---------------------------------------------------------------

    def check_authority(
        self, event: dict, state: WorkspaceState
    ) -> list[ValidationFailure]:
        """Enforce D13 authority-bindings against this event.

        For each binding matching the event's payload-subtype (and qualifier
        when the binding declares one), verify at least one actor in
        `event.actors[]` has `role == required-role` AND the registered
        actor record's `subtype == required-actor-subtype`.

        Returns one ValidationFailure (category="authority") per unsatisfied
        binding. Empty `event.actors` short-circuits (per-event identity
        checks catch missing actors).
        """
        actors = event.get("actors") or []
        if not actors:
            return []

        subtype = event.get("payload-subtype")
        payload = event.get("payload") or {}
        failures: list[ValidationFailure] = []

        for binding in self.authority_bindings:
            if binding.get("payload-subtype") != subtype:
                continue
            qualifier = binding.get("qualifier")
            if qualifier is not None and payload.get("qualifier") != qualifier:
                continue

            required_role = binding.get("required-role")
            required_subtype = binding.get("required-actor-subtype")

            matched = False
            for actor_ref in actors:
                if actor_ref.get("role") != required_role:
                    continue
                aid = actor_ref.get("id")
                if aid is None or not state.has_actor(aid):
                    continue
                if state.get_actor(aid).get("subtype") == required_subtype:
                    matched = True
                    break

            if not matched:
                qual_clause = f", qualifier={qualifier!r}" if qualifier is not None else ""
                failures.append(
                    ValidationFailure(
                        category="authority",
                        path="event.actors",
                        value=None,
                        reason=(
                            f"shape {self.id!r} authority-binding for "
                            f"payload-subtype={subtype!r}{qual_clause} requires "
                            f"role={required_role!r} on an actor with "
                            f"subtype={required_subtype!r}; no matching actor present"
                        ),
                    )
                )

        return failures

    # ---------------------------------------------------------------
    # Hook stub registration
    # ---------------------------------------------------------------

    def register_stub_handlers(self, hook_registry: HookRegistry) -> None:
        """Register a no-op handler for each declared hook name."""
        for hook in self.hooks:
            name = hook.get("name")
            if name:
                hook_registry.register(name, _stub_handler)


def load_shape_from_provision(
    provision_ref: str, extensions_dir: Path
) -> GenericShape:
    """Load a shape spec from a `<ext-id>:<provision-id>` ref.

    Mirrors the substrate-provision loading path in boot.py step 3.
    """
    from fresh_plan.validator.extensions import (
        discover_extensions,
        load_extension,
    )

    ext_id, prov_id = provision_ref.split(":", 1)
    discovered = discover_extensions(extensions_dir)
    if ext_id not in discovered:
        raise ValueError(
            f"shape provision {provision_ref!r}: extension {ext_id!r} not discovered "
            f"under {extensions_dir!s}"
        )
    spec: Optional[dict] = None
    for version, manifest_path in discovered[ext_id].items():
        loaded_ext, _errs = load_extension(ext_id, version, manifest_path)
        spec = loaded_ext.provisions_loaded.get(prov_id)
        if spec is not None:
            break
    if spec is None:
        raise ValueError(
            f"shape provision {provision_ref!r}: provision id {prov_id!r} not found "
            f"in any version of extension {ext_id!r}"
        )
    return GenericShape(spec=spec)
