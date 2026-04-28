"""No-op email adapter — the default when no integration is configured."""
from __future__ import annotations

from typing import Any


class Adapter:
    """Email integration disabled. All operations return empty / no-op."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

    def probe(self) -> dict[str, Any]:
        return {"ok": True, "detail": "email integration disabled (adapter=none)"}

    def list_messages(self, since=None, folder=None, limit=None) -> list[dict[str, Any]]:
        return []

    def fetch_message(self, message_id: str) -> dict[str, Any]:
        raise NotImplementedError(
            "no email adapter configured; set integrations.email.adapter "
            "in office-config.yaml to enable."
        )

    def normalize(self, raw_message: Any) -> dict[str, Any]:
        raise NotImplementedError(
            "no email adapter configured; nothing to normalize."
        )
