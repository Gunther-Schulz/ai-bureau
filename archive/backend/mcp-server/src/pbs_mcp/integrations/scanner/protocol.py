"""Scanner / OCR adapter protocol."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ScannerAdapter(Protocol):
    def probe(self) -> dict[str, Any]: ...

    def list_pending_scans(self) -> list[dict[str, Any]]:
        """List scanned documents not yet ingested.

        Returned items: {"path": str, "scanned_at": str, "size": int}.
        """
        ...

    def claim_scan(self, scan_path: str) -> dict[str, Any]:
        """Atomically move a pending scan into a 'claimed' state.

        Used by ingestion pipeline to prevent double-processing.
        Returns the new path + metadata.
        """
        ...

    def ocr(self, scan_path: str) -> str:
        """Run OCR on a scanned PDF/image; return extracted text."""
        ...
