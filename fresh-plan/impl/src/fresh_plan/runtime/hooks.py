"""Hook registry (per D13 hooks + D17 core abstract capability `hooks`).

D13 hooks are *semantic declarations of policy hook points* on shapes;
D17 declares `hooks` as a core abstract substrate capability. Per the
substrate kind contract (D12), the substrate exposes the hook interface
that shape policies register handlers into.

Per B2 design lock: hooks fire synchronously, in registration order;
each fire returns the list of handler return values. Async hooks are
deferred.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# Type alias for a hook handler. The context dict is whatever the
# firing site passes; handlers return any value (collected at fire-time).
HookHandler = Callable[[dict], Any]


@dataclass
class HookRegistry:
    """Hook name → list of registered handlers, fired sync in registration order.

    Per D34 §A.1 hook names are vocabulary-identifiers (kebab-strict),
    but we don't enforce the pattern at runtime — the schema layer
    enforces it on declared hook names; runtime registrations come from
    shape policy code that knows the names.
    """

    _handlers: dict[str, list[HookHandler]] = field(default_factory=dict)

    def register(self, name: str, handler: HookHandler) -> None:
        """Register a handler for the named hook."""
        if not callable(handler):
            raise TypeError(f"hook handler must be callable; got {type(handler).__name__}")
        self._handlers.setdefault(name, []).append(handler)

    def fire(self, name: str, context: dict) -> list[Any]:
        """Invoke all handlers for `name` in registration order. Returns return values.

        If no handlers are registered for the name, returns an empty list
        (firing an unregistered hook is not an error — many hook names
        are declared but have no policy attached).
        """
        results: list[Any] = []
        for handler in self._handlers.get(name, []):
            results.append(handler(context))
        return results

    def registered_names(self) -> list[str]:
        """List of hook names that have at least one handler."""
        return sorted(self._handlers.keys())

    def handler_count(self, name: str) -> int:
        return len(self._handlers.get(name, []))

    def clear(self, name: Optional[str] = None) -> None:
        """Clear handlers — for one named hook (if `name` given) or all hooks.

        Useful in tests to reset hook state between scenarios. Production
        code should not need this; shapes register handlers once at boot.
        """
        if name is None:
            self._handlers.clear()
        else:
            self._handlers.pop(name, None)
