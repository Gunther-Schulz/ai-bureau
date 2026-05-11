"""fresh-plan reference implementation (Phase B per D36).

This package houses the B1 conformance validator. Subsequent Phase B
workstreams (B2 substrate, B3 shape, etc.) will extend this package.
"""
from __future__ import annotations

__version__ = "0.1.0"

from fresh_plan.validator import (
    ValidationFailure,
    ValidationResult,
    validate_workspace_boot,
)

__all__ = ["ValidationFailure", "ValidationResult", "validate_workspace_boot", "__version__"]
