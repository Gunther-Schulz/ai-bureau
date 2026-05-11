"""Tests for HookRegistry (D13 hooks + D17 core capability)."""
from __future__ import annotations

import pytest

from fresh_plan.runtime.hooks import HookRegistry


def test_register_and_fire():
    h = HookRegistry()
    h.register("pre-claim", lambda ctx: ctx["x"] + 1)
    results = h.fire("pre-claim", {"x": 1})
    assert results == [2]


def test_fire_with_no_handlers_returns_empty():
    h = HookRegistry()
    assert h.fire("unbound-hook", {}) == []


def test_multiple_handlers_fire_in_registration_order():
    h = HookRegistry()
    order: list[str] = []
    h.register("hook-a", lambda _ctx: order.append("first"))
    h.register("hook-a", lambda _ctx: order.append("second"))
    h.register("hook-a", lambda _ctx: order.append("third"))
    h.fire("hook-a", {})
    assert order == ["first", "second", "third"]


def test_non_callable_handler_rejected():
    h = HookRegistry()
    with pytest.raises(TypeError):
        h.register("hook", "not-a-callable")  # type: ignore[arg-type]


def test_registered_names_and_handler_count():
    h = HookRegistry()
    h.register("a", lambda _c: None)
    h.register("a", lambda _c: None)
    h.register("b", lambda _c: None)
    assert h.registered_names() == ["a", "b"]
    assert h.handler_count("a") == 2
    assert h.handler_count("missing") == 0


def test_handlers_receive_context_dict():
    h = HookRegistry()
    captured: list[dict] = []
    h.register("h", lambda ctx: captured.append(ctx))
    h.fire("h", {"k": "v"})
    assert captured == [{"k": "v"}]
