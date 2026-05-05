"""AuditEvent base — per `arch/audit.md` §2.A emission API + §11 schema.

The framework-level interface contract for atomic structured emission.
Every emission converging in the audit-trail (substrate-internal direct +
skill-side via MCP audit gate) MUST validate against this schema (per
`arch/audit.md` §8 dual-emission convergence).

Field shape per `arch/audit.md` §2.A + §10 boot ordering + `glossary/
event.md` (atomic structured emission unit) + `glossary/authority-binding.
md` (per-event actor declaration enforcement).

Per-event-kind details surface as discriminated-union models in domain-
specific modules (`pbs/audit.py` audit-internal events; `pbs/substrate.py`
substrate architectural events; `pbs/sparring.py` per-sub-mechanism
events; etc.). This module defines the COMMON BASE every event-kind
extends.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.actor_kind import ActorKind


class AuditEventBase(BaseModel):
    """Common base for all AuditEvents (framework-level interface contract).

    Per `arch/audit.md` §2.A: every emission declares actor + event_kind +
    timestamp + per-event-kind details. Per §2.D integrity verification:
    `prev_hash` references prior event for hash-chain. Per §8 cross-
    substrate event-kind translation: `substrate_kind` tagged at emission
    for substrate-specific metadata preservation across migrations.

    Concrete event types extend this base + add discriminator field
    `event_kind: Literal["..."]` + per-kind detail fields.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    event_kind: str
    """Discriminator for per-event-kind catalog routing.

    Concrete subclasses set as `Literal["..."]`. Catalog managed at three
    layers per `arch/audit.md` §2.E (framework baseline / per-shape /
    per-specialist).
    """

    timestamp: datetime
    """Emission timestamp (UTC; ISO 8601). Used for per-time-window query
    (`arch/audit.md` §2.C) + ordering reasoning-chain reconstruction."""

    actor_kind: ActorKind
    """The kind of actor emitting this event (per `glossary/actor.md` +
    `glossary/authority-binding.md`). Framework-level guarantee per
    `glossary/mechanism.md`: declared on every audit event."""

    actor_id: str
    """Identity of the emitting actor within the workspace (per `glossary/
    owner-b-scope.md`: actor records are workspace-scope managed entities
    at Owner B). Examples: practitioner-record-id for HUMAN; substrate
    Instance id for AI_RUNTIME; A2A peer identity for EXTERNAL."""

    session_id: str | None = None
    """Session boundary identifier per `glossary/session.md`. Identifies
    which session boundary the event was emitted within; cross-session
    audit-trail continuity preserved per `arch/audit.md` §9 mutability
    cross-session persistence."""

    work_unit_id: str | None = None
    """Work-unit attribution per `arch/audit.md` §2.C per-work-unit query
    + `glossary/work-unit.md`. Optional because some framework-baseline
    events (workspace_booted; session_started; substrate-internal
    integrity events) precede or transcend any specific work-unit."""

    workflow_instance_id: str | None = None
    """Workflow_instance attribution per `arch/workflow-work-unit.md`
    workflow_instance lifecycle. Optional because ad-hoc work has no
    workflow_instance + many events transcend workflow_instance scope."""

    claim_id: str | None = None
    """Claim attribution per `arch/claim-defensibility.md` per-claim
    reasoning chain reconstruction (per `arch/audit.md` §2.C query
    primitive). Set on claim-related events (claim_made, claim_revised,
    etc.)."""

    substrate_kind: str | None = None
    """Substrate Implementation identity (e.g., `claude_agent_sdk`,
    `ms_agent_framework`) per `arch/audit.md` §8 cross-substrate event-
    kind translation. Tagged for substrate-specific metadata preservation
    across migrations; cross-substrate translation per `glossary/
    substrate.md`. Optional — present when emission is substrate-specific."""

    prev_hash: str | None = None
    """Hash-chain reference to prior event per `arch/audit.md` §2.D
    integrity verification. Algorithm choice (SHA-256 default per W1) is
    substrate-impl level; the field's presence is class-level Surface
    commitment."""

    details: dict[str, Any] = Field(default_factory=dict)
    """Per-event-kind detail fields. Concrete event subclasses promote
    structured fields out of `details` into typed attributes; `details`
    remains for impl-specific or extension data not yet schematized."""
