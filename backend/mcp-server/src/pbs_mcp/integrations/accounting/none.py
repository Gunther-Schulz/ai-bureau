"""No-op accounting adapter."""
from __future__ import annotations

from typing import Any


class Adapter:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

    def probe(self) -> dict[str, Any]:
        return {"ok": True, "detail": "accounting integration disabled"}

    def list_invoices(self, client=None, project=None, status=None) -> list[dict[str, Any]]:
        return []

    def get_invoice(self, invoice_id: str) -> dict[str, Any]:
        raise NotImplementedError("no accounting adapter configured")

    def list_expenses(self, project=None, category=None) -> list[dict[str, Any]]:
        return []
