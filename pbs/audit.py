"""Audit mechanism class Surface — 7 capability categories per `arch/audit.md` §2.

Per `arch/audit.md`: Audit is a mechanism class (NOT Pattern A). The
class's mechanism Surface (this module) is fixed at framework-mechanism
layer; per-shape policy declares granularity + event-kind catalog +
error semantics + trust model; per-substrate-impl realizes storage.

Surface (§2):
- §A Emission API + actor declaration → `emit()`
- §B Append-only persistence → enforced by impl at write boundary
- §C Query for reasoning-chain reconstruction → `query_*()` methods
- §D Integrity verification → `verify_integrity()`
- §E Event-kind catalog management → at three layers (framework baseline /
  per-shape / per-specialist); managed at impl level via active shape's
  catalog; class Surface does not expose catalog mutation methods (the
  catalog is policy-data, not Surface-method)
- §F State-rendering-from-events → `render_state()`
- §G Cross-deployment external-format export → `export()`

Audit-internal events (§8) + error categories (§11) defined inline.
Per-event-kind details are discriminated-union types extending
`AuditEventBase` (this module covers audit-internal events; substrate /
adapter / sparring / claim event-kinds live in their respective modules).

Phase 6.1 reference impl: jsonl file-backed via Claude Agent SDK
substrate Surface §F (per `arch/audit.md` §4 default substrate-impl
storage realization). See `pbs/impls/claude_agent_sdk_audit.py` (Phase
6.1 forthcoming).
"""

from datetime import datetime
from typing import Any, Literal, Protocol, runtime_checkable

from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Audit-internal events (§8 — the class's own emissions)
# ---------------------------------------------------------------------------


class AuditTrailIntegrityVerified(AuditEventBase):
    """Periodic / per-query / per-migration-boundary integrity check passed.

    Per `arch/audit.md` §8: the audit class audits its own integrity.
    Final shutdown event per §10 boot/shutdown phase ordering step 7.
    """

    event_kind: Literal["audit_trail_integrity_verified"] = (        "audit_trail_integrity_verified"
    )


class AuditTrailIntegrityViolated(AuditEventBase):
    """Hash-chain broken — audit-trail tampered OR corruption detected.

    Per `arch/audit.md` §8: immediate emission on detection. Composes with
    `AuditIntegrityError` (raised at the violation site; this event records
    the detection in the audit-trail itself, preserving forensic visibility).
    """

    event_kind: Literal["audit_trail_integrity_violated"] = (        "audit_trail_integrity_violated"
    )


class AuditTrailMigrated(AuditEventBase):
    """Cross-deployment migration completed (per `arch/audit.md` §8 + §2.G).

    Records substrate migration / cross-region replication / cloud transition
    boundaries. Hash-chain integrity verified at migration boundary per
    §2.D before this event emits.
    """

    event_kind: Literal["audit_trail_migrated"] = "audit_trail_migrated"

class AuditTrailArchived(AuditEventBase):
    """Audit-trail compression / archival event (per `arch/audit.md` §8).

    Future per W3 watch-list (audit-trail compression / archival strategy
    at scale; first deployment with multi-year accumulation).
    """

    event_kind: Literal["audit_trail_archived"] = "audit_trail_archived"

# ---------------------------------------------------------------------------
# Error categories (§11 — class-level error semantics)
# ---------------------------------------------------------------------------


class AuditError(Exception):
    """Base for all Audit class errors per `arch/audit.md` §11.

    Per-shape error semantics (§11 + §14): practitioner-shape fail-closed;
    autonomous-business-shape fail-open with alert + queued-retry;
    personal-OS-shape fail-open with retry.
    """


class AuditWriteError(AuditError):
    """Audit-trail write failure (filesystem unavailable; permission denied;
    disk full). Substrate-impl raises; class Surface declares category."""


class AuditIntegrityError(AuditError):
    """Hash-chain broken (audit-trail tampered OR corruption detected).

    Substrate-impl detects; class Surface declares category. Composes with
    `AuditTrailIntegrityViolated` event (event records detection; this
    error is raised at violation site)."""


class AuditAppendOnlyViolation(AuditError):
    """Attempted rewrite / truncate / rewind on audit-trail (architectural-
    rule violation; substrate-impl gate rejects). Per `arch/audit.md` §2.B
    append-only persistence enforced gate-dispatched-structural per
    `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1."""


class AuditSchemaError(AuditError):
    """Event doesn't match AuditEvent Pydantic schema (class-level — schema
    is class Surface)."""


class AuditCatalogError(AuditError):
    """Event_kind not in active shape's mandatory catalog OR not in baseline
    framework catalog. Class-level + per-shape-policy validation."""


class AuditQueryError(AuditError):
    """Query failure (substrate-impl-internal; corruption; index issue)."""


class AuditMigrationError(AuditError):
    """Cross-deployment migration failure (integrity not verifiable; format
    incompatible)."""


class AuditTrustError(AuditError):
    """Authority-binding mechanism failure per `glossary/authority-binding.md`.

    Per-shape trust policy violated (e.g., budget-policy threshold exceeded
    without practitioner approval per `arch/audit.md` §11). Substrate
    Surface §C permission flow + per-shape policy integrate."""


# ---------------------------------------------------------------------------
# Protocol Surface — 7 capability categories typed
# ---------------------------------------------------------------------------


@runtime_checkable
class AuditProtocol(Protocol):
    """The Audit mechanism class Surface (Phase 6.1 Mode 3 spec).

    Per `arch/audit.md` §6 mechanism-class structural reconciliation: the
    Surface (this Protocol) is fixed at framework-mechanism layer + same
    across all substrate-impls; per-substrate-impl realization (jsonl /
    Postgres / cloud / federation) inherits from selected substrate
    Implementation per substrate Surface §F; per-shape policy declares
    granularity + event-kind catalog + error semantics + trust model.

    Cardinality (§5 + §9): 1 audit-trail per workspace (always present;
    not selectable). Class Surface is always present; not separately
    instantiated.

    Phase 6.1 reference impl satisfies this Protocol via jsonl file-backed
    storage realization (per Claude Agent SDK substrate Surface §F).
    """

    # ------------------------------------------------------------------
    # §A Emission API + actor declaration (§B append-only enforced by impl)
    # ------------------------------------------------------------------

    def emit(self, event: AuditEventBase) -> None:
        """Emit an event to the audit-trail.

        Per `arch/audit.md` §2.A: the entry point for both substrate-internal
        direct emission + skill-side MCP audit gate emission. Both paths
        converge through this method into a single audit-trail.

        Per §2.B append-only enforced at write boundary by substrate-impl
        gate (file-handle exclusive write; no rewind; no truncate; no
        per-event-rewrite). Violations raise `AuditAppendOnlyViolation`.

        Per §2.E catalog validation: emission validates `event.event_kind`
        against active shape's catalog (raises `AuditCatalogError` on
        miss). Per-shape mandatory event kinds checked at active-shape
        boot per §5.

        Raises:
            AuditWriteError: storage failure (filesystem / permission / disk).
            AuditAppendOnlyViolation: append-only gate violation.
            AuditSchemaError: schema mismatch.
            AuditCatalogError: event_kind not in active catalog.
            AuditTrustError: authority-binding policy violated.
        """
        ...

    # ------------------------------------------------------------------
    # §C Query for reasoning-chain reconstruction
    # ------------------------------------------------------------------

    def query_per_claim(self, claim_id: str) -> list[AuditEventBase]:
        """Per-claim reasoning chain (events filtered by claim_id, ordered
        by timestamp). Per `arch/audit.md` §2.C.

        Used by L8 auditor reasoning-chain reconstruction +
        `arch/claim-defensibility.md` §2.2 re-run-ability via audit-trail
        reconstruction.
        """
        ...

    def query_per_actor(
        self, actor_kind: ActorKind, actor_id: str
    ) -> list[AuditEventBase]:
        """Per-actor activity (events filtered by actor_kind + actor_id).

        Per `arch/audit.md` §2.C. Used by `arch/practitioner.md` cross-
        practitioner audit-trail query pattern.
        """
        ...

    def query_per_time_window(
        self, start: datetime, end: datetime
    ) -> list[AuditEventBase]:
        """Per-time-window event range query.

        Per `arch/audit.md` §2.C. Range is inclusive of `start`, exclusive
        of `end` (standard half-open interval).
        """
        ...

    def query_per_event_kind(self, event_kind: str) -> list[AuditEventBase]:
        """Per-event-kind aggregation (count + content extraction).

        Per `arch/audit.md` §2.C. Used by quality-gate per-axis signal
        ingestion + per-shape policy enforcement.
        """
        ...

    def query_per_work_unit(self, work_unit_id: str) -> list[AuditEventBase]:
        """Per-work-unit attribution (events filtered by work_unit_id).

        Per `arch/audit.md` §2.C. Used by `arch/workflow-work-unit.md`
        per-work-unit audit-trail attribution chain.
        """
        ...

    # ------------------------------------------------------------------
    # §D Integrity verification
    # ------------------------------------------------------------------

    def verify_integrity(self) -> bool:
        """Verify audit-trail hash-chain unbroken.

        Per `arch/audit.md` §2.D: each event's prev_hash references prior
        event; hash-chain unbroken signal = audit-trail unmodified. Returns
        True if hash-chain verifies; raises `AuditIntegrityError` on
        violation (also emits `AuditTrailIntegrityViolated` event for
        forensic visibility).

        Algorithm choice (SHA-256 default per W1 watch-list) is substrate-
        impl level; the method's existence is class-level Surface
        commitment.
        """
        ...

    # ------------------------------------------------------------------
    # §F State-rendering-from-events
    # ------------------------------------------------------------------

    def render_state(self, kind: str) -> dict[str, Any]:
        """Render workspace state derived from event sequence.

        Per `arch/audit.md` §2.F + archived audit-trail-v2 single-write
        architecture: state IS the rendered view; events ARE the source
        of truth.

        `kind` selects the rendering target (e.g., "workflow_instance"
        renders workflow_instance state map; "claim_status" renders per-
        claim status). Specific kind catalog per-substrate-impl level.
        """
        ...

    # ------------------------------------------------------------------
    # §G Cross-deployment external-format export
    # ------------------------------------------------------------------

    def export(self, format: str) -> bytes:
        """Export audit-trail to external format for cross-deployment /
        regulatory submission / L8 post-hoc engagement.

        Per `arch/audit.md` §2.G + `profiles/L8-auditor-reviewer-posthoc.md`
        line 33 external-format requirements. `format` selects the export
        format (e.g., "pdf", "csv", "regulator_submission"). Specific
        format catalog per-substrate-impl level.
        """
        ...
