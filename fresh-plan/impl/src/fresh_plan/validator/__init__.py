"""Conformance validator (Phase B workstream B1 per D36).

Public API:
    validate_workspace_boot(manifest, extensions_dir) -> ValidationResult
    ValidationResult, ValidationFailure dataclasses.

Implements:
    D29 validation flow (workspace.composition resolution-time)
    D30 cross-kind referential integrity (five check categories)
    D32 boot-time resolution (multi-binding, cycles, load order)
    D33 version-conflict resolution
"""
from __future__ import annotations

from fresh_plan.validator.types import ValidationFailure, ValidationResult
from fresh_plan.validator.workspace import validate_workspace_boot

__all__ = ["ValidationFailure", "ValidationResult", "validate_workspace_boot"]
