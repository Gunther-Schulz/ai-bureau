"""Calendar adapter protocol."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CalendarAdapter(Protocol):
    def probe(self) -> dict[str, Any]: ...

    def list_events(
        self,
        between_start: str,
        between_end: str,
        calendar: str | None = None,
    ) -> list[dict[str, Any]]:
        """List events in [between_start, between_end] (ISO dates)."""
        ...

    def get_event(self, event_id: str) -> dict[str, Any]: ...

    def normalize(self, raw_event: Any) -> dict[str, Any]:
        """Unified shape:
        {
            "id": str,
            "title": str,
            "start": str,                 # ISO 8601
            "end": str,                   # ISO 8601
            "location": str,
            "attendees": [{"name": str, "email": str}, ...],
            "description": str,
            "calendar": str,
        }
        """
        ...
