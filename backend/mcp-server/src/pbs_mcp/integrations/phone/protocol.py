"""Phone-system adapter protocol."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PhoneAdapter(Protocol):
    def probe(self) -> dict[str, Any]: ...

    def list_calls(
        self,
        since: str | None = None,
        direction: str | None = None,        # "inbound" | "outbound" | None
    ) -> list[dict[str, Any]]:
        """List call records matching filter.

        Returned: {"id", "direction", "from", "to", "started_at",
                   "duration_s", "answered": bool, "voicemail_path": str|None}.
        """
        ...

    def get_call(self, call_id: str) -> dict[str, Any]: ...
