"""Shape runtime — D13 policy bundle attached to a substrate.

Per D13, the shape kind carries substantive identity as a policy bundle of
authority-bindings, roles, hooks, actor-requirements, and capability
requirements. `Shape` is the base class reading off D13 + shape.schema.json;
concrete shape impls subclass it. `GenericShape` is the deliberately
neutral first impl (B3), explicitly NOT practitioner-shape per D26.

Runtime concerns owned by Shape:
  - Hold the loaded shape spec dict; expose D13 slot accessors.
  - Per-event authority-binding enforcement (D13 authority-bindings) —
    universal across shape impls.
  - Hook-handler registration interface (`register_handlers`) — each
    shape impl supplies its own registration logic.

Out of scope (handled elsewhere):
  - actor-requirements cardinality — workspace-level concern, boot-time.
  - required-capabilities — resolved at boot via the B1 capability check.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fresh_plan.runtime.hooks import HookRegistry
from fresh_plan.runtime.provision import load_provision_spec
from fresh_plan.runtime.workspace_state import WorkspaceState
from fresh_plan.validator.types import ValidationFailure


def _stub_handler(ctx: dict) -> None:
    """No-op handler stub shared across declared hook names."""
    return None


@dataclass
class Shape:
    """Base class for shape runtime impls per D13 + shape.schema.json.

    Holds the loaded spec, exposes D13 slot accessors, enforces
    authority-bindings on emitted events. Subclasses override
    `register_handlers` to install policy-specific hook handlers.
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
    # Hook handler registration (abstract; subclass-owned)
    # ---------------------------------------------------------------

    def register_handlers(self, hook_registry: HookRegistry) -> None:
        """Install policy handlers for the declared hook names.

        Subclasses MUST override. Real-shape impls install policy-specific
        handlers; stub-style shapes (like GenericShape) install no-op stubs.
        """
        raise NotImplementedError("Shape subclasses must implement register_handlers")


@dataclass
class GenericShape(Shape):
    """Neutral first shape impl per D26 (B3) — deliberately NOT practitioner-shape.

    Registers a no-op stub handler for every declared hook name so hooks
    are observable and firable; pioneer-instance practitioner-shape (Phase D)
    replaces stubs with real policy behavior in its own subclass of Shape.
    """

    def register_handlers(self, hook_registry: HookRegistry) -> None:
        for hook in self.hooks:
            name = hook.get("name")
            if name:
                hook_registry.register(name, _stub_handler)


@dataclass
class MinShape(Shape):
    """Truly minimal shape — no roles, no hooks, no authority-bindings.

    Used by B2-era substrate-only test fixtures (e.g., `workspace-substrate-
    test`) that exercise substrate runtime mechanics in isolation, without
    shape-policy interference. Distinct from GenericShape: GenericShape has
    illustrative authority-bindings + hooks for B3 shape-impl tests; MinShape
    has none — purely "shape slot satisfied; no policy."

    Registered runtime class for `min-shape` provision-id per D46 §B.1
    (every shape provision must have a registered runtime class).
    """

    def register_handlers(self, hook_registry: HookRegistry) -> None:
        # No hooks declared in MinShape spec; nothing to register.
        for hook in self.hooks:
            name = hook.get("name")
            if name:
                hook_registry.register(name, _stub_handler)


# Module-level registry of (shape.id → runtime class). Populated as new shape
# impls land. For Phase B there's GenericShape (B3 reference impl) + MinShape
# (test-fixture-only minimal shape per D46); Phase D's practitioner-shape
# will register here.
_SHAPE_CLASSES: dict[str, type[Shape]] = {
    "generic-shape": GenericShape,
    "min-shape": MinShape,
}


def load_shape_from_provision(
    provision_ref: str, extensions_dir: Path
) -> Shape:
    """Load a shape spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.id` to the registered runtime class. Raises
    ValueError if the spec's id has no registered runtime class.
    """
    spec = load_provision_spec(provision_ref, extensions_dir)
    shape_id = spec.get("id")
    cls = _SHAPE_CLASSES.get(shape_id)
    if cls is None:
        raise ValueError(
            f"shape provision {provision_ref!r}: spec id {shape_id!r} has no "
            f"registered Shape runtime class"
        )
    return cls(spec=spec)
