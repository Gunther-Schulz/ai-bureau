"""No-op scanner adapter."""
from __future__ import annotations

from typing import Any


class Adapter:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

    def probe(self) -> dict[str, Any]:
        return {"ok": True, "detail": "scanner integration disabled"}

    def list_pending_scans(self) -> list[dict[str, Any]]:
        return []

    def claim_scan(self, scan_path: str) -> dict[str, Any]:
        raise NotImplementedError("no scanner adapter configured")

    def ocr(self, scan_path: str) -> str:
        raise NotImplementedError("no scanner adapter configured")
