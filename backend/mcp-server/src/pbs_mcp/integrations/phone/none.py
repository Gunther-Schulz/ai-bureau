"""No-op phone adapter."""
from __future__ import annotations

from typing import Any


class Adapter:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

    def probe(self) -> dict[str, Any]:
        return {"ok": True, "detail": "phone integration disabled"}

    def list_calls(self, since=None, direction=None) -> list[dict[str, Any]]:
        return []

    def get_call(self, call_id: str) -> dict[str, Any]:
        raise NotImplementedError("no phone adapter configured")
