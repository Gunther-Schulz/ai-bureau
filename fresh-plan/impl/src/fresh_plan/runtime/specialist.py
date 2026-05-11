"""Specialist runtime — D19 + specialist.schema.json + D37 + D36 B6 brief.

Per D19, specialists are packaged role/skill bundles loaded into a
workspace's substrate via the `skills` capability (D17). `Specialist` is
the base class reading off D19; concrete specialist impls subclass it.

Per D37, cross-specialist coordination is event-driven at framework level
(declared-event-emissions / declared-event-subscriptions per D19); the
substrate's subscriber-dispatch infrastructure dispatches matching events
into `on_event`. RPC-style direct invocation is implementation-shape.

For Phase B, the shipped GenericSpecialist is a stub: `handle_skill`
emits one `action` event per invoke and returns a canned response;
`on_event` is a no-op (subclasses override for reactive policy).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from fresh_plan.runtime.provision import load_provision_spec


@dataclass
class Specialist:
    """Base class for specialist runtime impls per D19 + specialist.schema.json.

    Holds the loaded spec, exposes D19 slot accessors, manages workspace
    attachment + required-adapter resolution + skill-registration into
    the substrate's `skills` capability (D17). Subclasses override
    `handle_skill` to implement skill behavior and `on_event` to react
    to subscribed events (D37).
    """

    spec: dict
    _emit_event: Optional[Callable[..., dict]] = field(default=None, repr=False)
    _workspace: Any = field(default=None, repr=False)
    _adapters: dict[str, "Adapter"] = field(default_factory=dict, repr=False)

    @property
    def id(self) -> str:
        return self.spec["id"]

    @property
    def version(self) -> str:
        return self.spec["version"]

    @property
    def roles(self) -> list[str]:
        return list(self.spec.get("roles", []) or [])

    @property
    def skills(self) -> list[dict]:
        return list(self.spec.get("skills", []) or [])

    @property
    def supported_work_unit_kinds(self) -> list[str]:
        return list(self.spec.get("supported-work-unit-kinds", []) or [])

    @property
    def required_adapter_bindings(self) -> list[str]:
        return list(self.spec.get("required-adapter-bindings", []) or [])

    @property
    def required_substrate_capabilities(self) -> list[str]:
        return list(self.spec.get("required-substrate-capabilities", []) or [])

    @property
    def declared_event_emissions(self) -> list[dict]:
        return list(self.spec.get("declared-event-emissions", []) or [])

    @property
    def declared_event_subscriptions(self) -> list[dict]:
        return list(self.spec.get("declared-event-subscriptions", []) or [])

    @property
    def activation_scope(self) -> Optional[str]:
        return self.spec.get("activation-scope")

    # ---------------------------------------------------------------
    # Workspace attachment (boot-ordering: post-Workspace + post-adapter-attach)
    # ---------------------------------------------------------------

    def attach_workspace(self, workspace: Any) -> None:
        """Wire workspace event-emit + resolve required adapter bindings.

        Per D30 cross-kind referential integrity: every entry in
        `required-adapter-bindings` must resolve to an adapter bound in
        the workspace. Raises RuntimeError on miss (B1 catches the static
        case; this guard covers runtime composition drift).
        """
        self._workspace = workspace
        self._emit_event = workspace._emit_event
        substrate = workspace._substrate
        for required in self.required_adapter_bindings:
            matched_bid: Optional[str] = None
            for bid, binding_dict in substrate.adapter_bindings.items():
                if binding_dict.get("provision") == required:
                    matched_bid = bid
                    break
            if matched_bid is None:
                raise RuntimeError(
                    f"specialist {self.id!r}: required-adapter-binding "
                    f"{required!r} has no matching adapter-binding in workspace"
                )
            self._adapters[required] = workspace.adapter(matched_bid)

    def register_skills(self, skill_registry) -> None:
        """Register each declared skill as a handle_skill-dispatching callable."""
        for skill in self.skills:
            skill_id = skill if isinstance(skill, str) else skill.get("id")
            if not skill_id:
                continue
            skill_registry.register(
                skill_id,
                lambda params, _sid=skill_id: self.handle_skill(_sid, params),
            )

    # ---------------------------------------------------------------
    # Skill dispatch (abstract; subclass-owned)
    # ---------------------------------------------------------------

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        """Dispatch a skill invocation. Subclasses MUST override."""
        raise NotImplementedError("Specialist subclasses must implement handle_skill")

    def on_event(self, event: dict) -> None:
        """React to a subscribed event (D37). Default = no-op; override for policy."""
        return None


@dataclass
class GenericSpecialist(Specialist):
    """First concrete specialist impl per B6 / D26 — deliberately neutral, NOT
    practitioner-specialist; stub behavior emits one action event per skill
    invocation and returns a canned response.
    """

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "specialist not attached to a workspace; call attach_workspace first"
            )
        params = params or {}
        actor_id = next(iter(self._workspace._substrate.state.actors), None)
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": skill_id,
                "parameters": params,
            },
        )
        return {"ok": True, "skill": skill_id, "stub": True, "parameters": params}


# Module-level registry of (specialist.id → runtime class). Populated as new
# specialist impls land. For Phase B there's only GenericSpecialist; future
# practitioner-specialist (Phase D) registers here.
_SPECIALIST_CLASSES: dict[str, type[Specialist]] = {
    "generic-specialist": GenericSpecialist,
}


def load_specialist_from_provision(
    provision_ref: str, extensions_dir: Path
) -> Specialist:
    """Load a specialist spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.id` to the registered runtime class. Raises
    ValueError if the spec's id has no registered runtime class.
    """
    spec = load_provision_spec(provision_ref, extensions_dir)
    specialist_id = spec.get("id")
    cls = _SPECIALIST_CLASSES.get(specialist_id)
    if cls is None:
        raise ValueError(
            f"specialist provision {provision_ref!r}: spec id {specialist_id!r} "
            f"has no registered Specialist runtime class"
        )
    return cls(spec=spec)
