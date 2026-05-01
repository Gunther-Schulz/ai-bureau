"""Accounting adapter protocol."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AccountingAdapter(Protocol):
    def probe(self) -> dict[str, Any]: ...

    def list_invoices(
        self,
        client: str | None = None,
        project: str | None = None,
        status: str | None = None,           # "draft"|"sent"|"paid"|"overdue"
    ) -> list[dict[str, Any]]: ...

    def get_invoice(self, invoice_id: str) -> dict[str, Any]: ...

    def list_expenses(
        self,
        project: str | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]]: ...
