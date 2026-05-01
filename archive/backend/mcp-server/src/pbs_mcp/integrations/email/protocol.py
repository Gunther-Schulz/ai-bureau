"""Email adapter protocol.

Adapters implement this small interface; MCP tools (`fetch_emails`,
`route_inbox` — when implemented) consume the protocol, not the
adapter directly.

A normalized message has a stable shape regardless of underlying
storage (Thunderbird mbox/maildir, IMAP, Outlook PST, raw mbox file).
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class EmailAdapter(Protocol):
    """Minimal contract for an email adapter."""

    def probe(self) -> dict[str, Any]:
        """Diagnostic check — verify connectivity / config validity.

        Returns a dict with at least `{ok: bool, detail: str}`. Used by
        setup-office to validate config before persisting.
        """
        ...

    def list_messages(
        self,
        since: str | None = None,
        folder: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """List message envelopes (id, date, from, to, subject) matching filter.

        - `since`: ISO date — only messages after this date.
        - `folder`: optional folder/label scoping.
        - `limit`: cap on number returned.
        """
        ...

    def fetch_message(self, message_id: str) -> dict[str, Any]:
        """Return the full normalized message for a given id."""
        ...

    def normalize(self, raw_message: Any) -> dict[str, Any]:
        """Convert adapter-native message representation to unified shape.

        Unified message shape:
        {
            "id": str,
            "thread_id": str | None,
            "date": str,                  # ISO 8601
            "from": {"name": str, "email": str},
            "to": [{"name": str, "email": str}, ...],
            "cc": [...],
            "subject": str,
            "body_text": str,
            "body_html": str | None,
            "attachments": [{"filename": str, "content_type": str, "size": int}],
            "headers": dict[str, str],
            "folder": str | None,
        }
        """
        ...
