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
# Extended per D45 / D46 / D47 (Phase B Bref cluster supersedes) for
# runtime-failure categories that share the validator's failure shape:
# actor-seeding (D46 §B.2 boot manifest-actor seeding rollback),
# hook-handler (D47 §B.2 pre-event-emit hook handler raise),
# adapter-attach + adapter-binding-resolution (D48 §B.2 + §B.3 adapter cluster).
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
        "authority",  # D13 — shape authority-binding requirement unsatisfied
        "actor-seeding",  # D46 §B.2 — boot-time manifest-actor seeding rejection
        "hook-handler",  # D47 §B.2 — pre-event-emit hook handler raise
        "adapter-attach",  # D48 §B.2 — adapter.attach_workspace failure (Phase C real-wire)
        "adapter-binding-resolution",  # D48 §B.3 — specialist required-adapter-binding miss
        "composition-validity",  # D52 §B.1 — composition-change post-projection state violates shape policy
        "shape-migration-unsafe",  # D54 §B.2 — shape-version bump classified as breaking/new-era by classifier
        "activation-scope-grammar",  # D55 §B.1 — specialist activation-scope grammar parse failure at attach time
        "authority-constraint-grammar",  # D56 §B.1 — shape authority-binding additional-constraints grammar parse failure
        "configuration-rejected",  # D57 §B.1 — kind-runtime constructor rejected its `composition.*.configuration` dict
        "lifecycle-derivation-mismatch",  # D58 §B.1 — manifest-declared work-unit lifecycle timestamps disagree with chain-derived
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
    # Per D59 §B.1 — registered payload-body open-vocab values per slot.
    # Keys: "claim.confidence", "action.action-name", "state-change.what",
    # "lifecycle-transition.trigger". Values: list of qualified
    # `<ext-id>:<value>` strings.
    payload_vocabulary_tables: Optional[dict[str, list[str]]] = None

    def __bool__(self) -> bool:
        return self.success
