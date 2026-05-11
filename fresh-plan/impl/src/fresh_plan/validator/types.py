"""Public dataclasses for validator results.

Per D30, the validator produces structured failure records (category +
path + reason + value). The category vocabulary is closed at the eight
documented failure categories below.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


# Closed vocabulary of failure categories.
# Per D30 (resolution / capability / vocabulary / identity / binding),
# D32 (circular-dependency), D33 (version-conflict), and schema-level
# failures from the per-kind schemas (Phase A artifacts).
FAILURE_CATEGORIES = frozenset(
    {
        "schema",  # JSON Schema validation failure (Phase A formal schemas)
        "resolution",  # D30 §1 — referenced provision / extension not loadable
        "capability",  # D30 §2 — required-capabilities unsatisfied
        "vocabulary",  # D30 §3 — fully-qualified id not registered
        "identity",  # D30 §4 — workspace-internal id reference dangles
        "binding",  # D30 §5 — specialist requires adapter binding not present
        "circular-dependency",  # D32 §2 — cycle in extension dependency graph
        "version-conflict",  # D33 §B — range intersection empty / no version available
    }
)


@dataclass(frozen=True)
class ValidationFailure:
    """One concrete failure surfaced by the validator.

    `path` is a JSON-pointer-style string locating the failure within the
    manifest or aggregate state being validated. `value` is the offending
    value (for human-readable reports). `declarers` is populated for
    version-conflict failures with the extensions declaring the
    conflicting ranges.
    """

    category: str
    path: str
    reason: str
    value: Any = None
    declarers: Optional[list[str]] = None

    def __post_init__(self) -> None:
        if self.category not in FAILURE_CATEGORIES:
            raise ValueError(
                f"unknown failure category {self.category!r}; "
                f"allowed: {sorted(FAILURE_CATEGORIES)}"
            )


@dataclass
class ValidationResult:
    """Aggregate result of validate_workspace_boot.

    success is True only if `failures` is empty. `loaded_extensions` and
    `vocabulary_tables` are populated on success (for callers that want
    to inspect the resolved state); on failure they may be partial or
    None.
    """

    success: bool
    failures: list[ValidationFailure] = field(default_factory=list)
    loaded_extensions: Optional[dict[str, dict]] = None
    vocabulary_tables: Optional[dict[str, dict]] = None

    def __bool__(self) -> bool:
        return self.success
