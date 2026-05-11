"""Skill registry (per D19 skills + D17 core abstract capability `skills`).

Per D19: specialists declare `skills[]`. Per D17, `skills` is a core
abstract substrate capability; specialists' skill bundles are loaded
into the substrate's `skills` capability and invoked through it.

Per B2 design lock: specialist runtime is workstream B6. Here the
substrate registers each manifest-declared specialist's skills as
STUB callables that raise `NotImplementedError` when invoked. Real
skill behavior arrives in B6. Tests may register concrete callables
to exercise the invoke path.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


SkillCallable = Callable[[dict], Any]


class UnknownSkillError(KeyError):
    """Raised when invoking a skill id that is not registered."""


def _stub_for(skill_id: str) -> SkillCallable:
    """Construct a stub skill callable per the B2 scope cut.

    Per the B2 brief: specialists from the manifest are registered as
    stub skills that raise `NotImplementedError` on invoke. Real skill
    behavior is B6.
    """

    def _stub(_params: dict) -> Any:
        raise NotImplementedError(
            f"skill {skill_id!r} is a B2 stub; real behavior lands in B6"
        )

    return _stub


@dataclass
class SkillRegistry:
    """Skill-id → callable, with explicit stub registration for B2 specialists."""

    _skills: dict[str, SkillCallable] = field(default_factory=dict)

    def register(self, skill_id: str, callable_: SkillCallable) -> None:
        if not callable(callable_):
            raise TypeError(f"skill must be callable; got {type(callable_).__name__}")
        if skill_id in self._skills:
            raise ValueError(f"skill {skill_id!r} already registered")
        self._skills[skill_id] = callable_

    def register_stub(self, skill_id: str) -> None:
        """Register a stub for a manifest-declared specialist skill (B2 default)."""
        self.register(skill_id, _stub_for(skill_id))

    def invoke(self, skill_id: str, params: dict) -> Any:
        if skill_id not in self._skills:
            raise UnknownSkillError(skill_id)
        return self._skills[skill_id](params)

    def registered_ids(self) -> list[str]:
        return sorted(self._skills.keys())

    def has(self, skill_id: str) -> bool:
        return skill_id in self._skills
