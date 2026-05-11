"""Tests for SkillRegistry (D19 skills + D17 core capability)."""
from __future__ import annotations

import pytest

from fresh_plan.runtime.skills import SkillRegistry, UnknownSkillError


def test_register_and_invoke_concrete_skill():
    s = SkillRegistry()
    s.register("draft-section", lambda params: f"drafted({params['topic']})")
    assert s.invoke("draft-section", {"topic": "Section 3.2"}) == "drafted(Section 3.2)"


def test_unknown_skill_raises():
    s = SkillRegistry()
    with pytest.raises(UnknownSkillError):
        s.invoke("nope", {})


def test_duplicate_registration_rejected():
    s = SkillRegistry()
    s.register("x", lambda _p: 1)
    with pytest.raises(ValueError):
        s.register("x", lambda _p: 2)


def test_stub_skill_raises_not_implemented():
    """Per B2 brief: manifest-declared specialist skills register as stubs."""
    s = SkillRegistry()
    s.register_stub("review-section")
    with pytest.raises(NotImplementedError) as exc_info:
        s.invoke("review-section", {})
    assert "B2 stub" in str(exc_info.value)


def test_registered_ids_and_has():
    s = SkillRegistry()
    s.register("alpha", lambda _p: None)
    s.register_stub("beta")
    assert s.registered_ids() == ["alpha", "beta"]
    assert s.has("alpha") and s.has("beta")
    assert not s.has("gamma")


def test_non_callable_rejected():
    s = SkillRegistry()
    with pytest.raises(TypeError):
        s.register("x", "not callable")  # type: ignore[arg-type]
