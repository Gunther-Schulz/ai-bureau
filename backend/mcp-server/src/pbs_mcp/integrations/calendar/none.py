"""No-op calendar adapter."""
from __future__ import annotations

from typing import Any


class Adapter:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

    def probe(self) -> dict[str, Any]:
        return {"ok": True, "detail": "calendar integration disabled"}

    def list_events(self, between_start, between_end, calendar=None) -> list[dict[str, Any]]:
        return []

    def get_event(self, event_id: str) -> dict[str, Any]:
        raise NotImplementedError("no calendar adapter configured")

    def normalize(self, raw_event: Any) -> dict[str, Any]:
        raise NotImplementedError("no calendar adapter configured")
