"""Authority-binding mechanism Surface — framework primitive per
`glossary/authority-binding.md`.

Per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table +
`docs/decisions/audit-arch-topic.md` §7 Trust subsumption rationale +
`docs/decisions/greenfield-rederivation-pause.md` Step 3: authority-binding
is its own framework primitive (mechanism-level, NOT Pattern A protocol);
per-shape policy declares the trust model parameterizing how that binding
satisfies shape-specific accountability requirements. Trust as a Pattern
A protocol was CANCELLED — per-shape variation was POLICY-level on the
trust-model dimension, not IMPL-level alternative architectures.

Three architectural sub-aspects per `glossary/authority-binding.md`:

1. **Per-event actor declaration** — every AuditEvent carries `actor_kind`
   + actor identity; framework-level guarantee per `pbs/types/event_base.py`
   `AuditEventBase` schema (Pydantic-required fields). The mechanism Surface
   adds per-shape requirements ON TOP of the schema-level guarantee
   (e.g., practitioner-shape REQUIRES `actor_kind=HUMAN` for
   `signature_applied` events; auto-binding wrong actor → policy denial).
2. **Per-claim author attribution** — every claim_made event records the
   authoring actor; reconstructible via audit-trail query (per `arch/audit.md`
   §2.C `query_per_claim`). The mechanism enforces per-claim binding at
   emission via `check()`.
3. **Authority-decision binding** — substrate Surface §C permission flow
   (per `arch/substrate.md` §2.C) integrates with the mechanism so authority-
   bearing decisions (signature_applied; send_authorized; budget_consumed-
   with-approval) bind to identified actor. The mechanism exposes
   `bind_decision()` for substrate permission flow → AuditEvent emission.

Composition with audit class:
- `arch/audit.md` §11 `AuditTrustError` is raised when authority-binding
  policy denies an emission (mechanism produces the denial; audit class
  raises the error category)
- `arch/audit.md` §14 cross-shape policy variation 'Trust model' row:
  per-shape policy declares trust model (PRACTITIONER_JUDGMENT for
  practitioner-shape; BUDGET_POLICY for autonomous-business-shape;
  INDIVIDUAL for personal-OS-shape) — each parameterizes this mechanism
- The mechanism produces an `AuthorityChecker` callable (matching audit
  impl's existing injection point per `pbs/impls/claude_agent_sdk_audit.py`
  Phase 6.1 thin-slice); audit's `emit()` consumes the callable at every
  emission

Composition with substrate Surface §C:
- `arch/substrate.md` §2.C `request_permission` resolves to a
  `PermissionDecision` (allow / deny). When the decision binds an
  authority-bearing action to an identified actor, the mechanism's
  `bind_decision()` records the binding in the audit-trail via the
  injected emitter (Phase 6.1 reference; Phase 6.2 wires the substrate
  permission flow → `bind_decision()` callsite end-to-end).

Phase 6.1 reference impls (per `BACKLOG.md` §224 thin-slice):
- `pbs/impls/practitioner_shape_authority_binding.py` — practitioner-shape
  reference (PRACTITIONER_JUDGMENT trust model; HUMAN actor required for
  signature_applied / send_authorized / claim_attested / work_unit_archived
  / workflow_phase_transition events; AI_RUNTIME required for claim_made
  + sparring_round_completed)
- autonomous-business-shape + personal-OS-shape impls deferred to Phase 6.2
  per W1 second-shape productization
"""

from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Trust-model dimension (per `arch/audit.md` §14 cross-shape policy variation)
# ---------------------------------------------------------------------------


class TrustModel(StrEnum):
    """Per-shape trust model dimension parameterizing authority-binding.

    Per `arch/audit.md` §14 cross-shape policy variation 'Trust model' row +
    `glossary/authority-binding.md` 'Composes with policy' (per-shape policy
    parameterizes mechanism). Three values mirror the audit storage
    realization's `AuditTrustModel` (Phase 6.1 reference; Phase 6.2 may
    harmonize the two enums per cross-mechanism vocabulary alignment).
    """

    PRACTITIONER_JUDGMENT = "practitioner_judgment"
    """practitioner-shape: human-actor required in accountability-bearing
    output chain (signature_applied / send_authorized / claim_attested /
    work_unit_archived / workflow_phase_transition events)."""

    BUDGET_POLICY = "budget_policy"
    """autonomous-business-shape: programmatic threshold-based; HUMAN
    approval required when budget threshold crossed (Phase 6.2 wiring)."""

    INDIVIDUAL = "individual"
    """personal-OS-shape: single-user attestation; no chain-of-defense
    requirement (Phase 6.2 wiring)."""


# ---------------------------------------------------------------------------
# Binding requirement (per-event-kind required-actor catalog)
# ---------------------------------------------------------------------------


class BindingRequirement(BaseModel):
    """Per-event-kind authority-binding requirement.

    Per `glossary/authority-binding.md` cross-archetype examples: each
    accountability-bearing event_kind has a required `actor_kind` (and
    optionally required actor-identity-related fields in `details`) per
    shape policy. Reference impls construct a catalog mapping event_kind →
    BindingRequirement; the mechanism's `check()` consults the catalog at
    emission time.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    required_actor_kinds: frozenset[ActorKind]
    """Acceptable `actor_kind` values for this event_kind. Single-element
    frozenset for strict requirements (e.g., `signature_applied` →
    `{HUMAN}`); multi-element for permissive (e.g., `claim_made` →
    `{AI_RUNTIME, HUMAN}` because both skill-emitted and human-attested
    claim creation are valid)."""

    required_detail_fields: frozenset[str] = Field(default_factory=frozenset)
    """Names of `details` keys that MUST be present + non-empty for the
    binding to be considered well-formed. Reference impl uses this for
    skill-id presence on `claim_made` events (per `glossary/authority-
    binding.md` 'every claim_made event records skill identifier')."""


# ---------------------------------------------------------------------------
# Authority-decision binding event (substrate Surface §C composition)
# ---------------------------------------------------------------------------


class AuthorityDecisionBound(AuditEventBase):
    """Records substrate Surface §C permission flow binding to identified
    actor per `glossary/authority-binding.md` sub-aspect 3.

    Emitted by `bind_decision()` when substrate's `request_permission` →
    `PermissionDecision(allow)` binds an authority-bearing action to an
    identified actor (HITL approval moments per `arch/substrate.md` §2.C).
    The event's `actor_kind` + `actor_id` carry the binding; `details`
    carries the decision_kind + bound action context.
    """

    event_kind: Literal["authority_decision_bound"] = "authority_decision_bound"


# ---------------------------------------------------------------------------
# Error categories (composes with `arch/audit.md` §11 `AuditTrustError`)
# ---------------------------------------------------------------------------


class AuthorityBindingError(Exception):
    """Base for all authority-binding mechanism errors per `glossary/authority-
    binding.md`. Composes with `arch/audit.md` §11 `AuditTrustError`: when
    audit's `emit()` consults the mechanism's `AuthorityChecker` and the
    callable returns False, audit raises `AuditTrustError` (the mechanism's
    own categories surface at the `bind_decision()` callsite + at direct
    `check()` consumers)."""


class MissingActorBinding(AuthorityBindingError):
    """Event's `actor_kind` does not satisfy the per-event-kind
    `BindingRequirement.required_actor_kinds` for the active shape's policy.

    Example: practitioner-shape `signature_applied` event emitted with
    `actor_kind=AI_RUNTIME` (catalog requires HUMAN)."""


class MalformedActorBinding(AuthorityBindingError):
    """Event's `actor_id` is empty OR a `BindingRequirement.required_detail_fields`
    entry is missing / empty.

    Example: `claim_made` event without `skill_id` in `details` when the
    binding catalog requires it."""


class DecisionBindingFailure(AuthorityBindingError):
    """Substrate Surface §C permission flow could not bind the decision to
    an identified actor (emitter unavailable; permission flow returned an
    indeterminate state; binding pre-conditions violated)."""


class AuthorityBindingUnreachable(AuthorityBindingError):
    """Mechanism not in ready state (pre-init / post-shutdown). Parallels
    `arch/substrate.md` §11 `SubstrateUnreachable` + `arch/quality-gate.md`
    §11 `GateUnreachable` per Pattern A error semantics."""


# ---------------------------------------------------------------------------
# Authority-checker callable signature (audit Surface §A injection)
# ---------------------------------------------------------------------------


AuthorityChecker = Callable[[AuditEventBase], bool]
"""Callable signature consumed by audit Surface §A emission per
`pbs/impls/claude_agent_sdk_audit.py` `AuthorityChecker` injection point.

Returns True if the event passes the per-shape trust policy + framework-
level binding requirements; False indicates policy denial → audit raises
`AuditTrustError` per `arch/audit.md` §11.

Mechanism instances expose `check` as a bound method conforming to this
signature so audit can wire the mechanism via `audit_config =
ClaudeAgentSDKAuditConfig(authority_checker=binding.check, ...)`.
"""


AuditEmitter = Callable[[AuditEventBase], None]
"""Audit Surface §A emit binding per `arch/audit.md` §8 skill-side MCP
audit gate path. Injected at construction; the callable shape matches
audit storage realization's emit method.

Per `arch/audit.md` §10 + `ARCHITECTURE.md` §6 composite boot subsection:
audit-phase 1-3 ready BEFORE the mechanism is constructed (the mechanism
emits `authority_decision_bound` events through the injected emitter).
"""


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class AuthorityBindingConfig(BaseModel):
    """Authority-binding mechanism configuration per `glossary/authority-
    binding.md`. Per-shape policy declares the trust model + binding
    catalog; this config carries those declarations.

    Per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table:
    authority-binding is the framework primitive; per-shape policy
    parameterizes via this config. Reference impls declare per-shape
    defaults (PractitionerShapeAuthorityBinding ships PRACTITIONER_JUDGMENT
    + practitioner-shape catalog; autonomous-business / personal-OS impls
    Phase 6.2).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    trust_model: TrustModel
    """Per-shape trust model parameterizing the mechanism per `arch/audit.md`
    §14 cross-shape policy variation 'Trust model' row."""

    binding_catalog: dict[str, BindingRequirement] = Field(default_factory=dict)
    """Mapping from accountability-bearing event_kind → BindingRequirement.
    Events whose `event_kind` is NOT in the catalog are accepted without
    binding enforcement (framework-baseline declaration only); events whose
    `event_kind` IS in the catalog are checked against the requirement."""


# ---------------------------------------------------------------------------
# Protocol Surface — runtime_checkable
# ---------------------------------------------------------------------------


@runtime_checkable
class AuthorityBindingProtocol(Protocol):
    """Authority-binding mechanism Surface per `glossary/authority-binding.md`.

    Three sub-aspect capabilities:

    1. **Per-event actor declaration**: `check(event)` enforces per-shape
       binding requirements at emission time (consumed by audit Surface §A
       via `AuthorityChecker` injection)
    2. **Per-claim author attribution**: `require_actor_kind(event_kind)`
       declares per-shape actor requirement for given event_kind (claim_made
       inclusive)
    3. **Authority-decision binding**: `bind_decision(decision_kind,
       actor_kind, actor_id, context)` records substrate Surface §C
       permission flow binding to identified actor via `AuthorityDecisionBound`
       event emission (Phase 6.1 reference; Phase 6.2 wires substrate
       permission flow callsite end-to-end)

    Lifecycle: lightweight; mechanism instance is ready immediately after
    construction (no boot phases); `is_ready` flips to False on `shutdown()`.
    """

    @property
    def trust_model(self) -> TrustModel:
        """Active per-shape trust model parameterizing this mechanism
        instance per `arch/audit.md` §14."""
        ...

    @property
    def is_ready(self) -> bool:
        """True between construction and shutdown."""
        ...

    def check(self, event: AuditEventBase) -> bool:
        """Per-event authority-binding check (consumed by audit Surface §A
        via `AuthorityChecker` injection per
        `pbs/impls/claude_agent_sdk_audit.py`).

        Returns True if the event satisfies the per-shape binding catalog +
        framework-level binding requirements; False signals policy denial
        (audit then raises `AuditTrustError` per `arch/audit.md` §11).

        Implementations MUST NOT raise `AuthorityBindingError` from `check`
        — the callable contract is True/False; the error category surfaces
        at `bind_decision()` callsites + at direct introspection. Returning
        False keeps the audit/binding contract clean (audit raises the
        error category; mechanism returns the verdict).
        """
        ...

    def require_actor_kind(
        self, event_kind: str
    ) -> frozenset[ActorKind] | None:
        """Returns the required `actor_kind` set for the given event_kind
        per the active shape's binding catalog, or None if the event_kind
        is not accountability-bearing (no binding requirement; framework-
        baseline emission accepted with any `actor_kind`).

        Used by callers needing pre-emission binding-requirement introspection
        (e.g., skill code constructing AuditEvent decides which `actor_kind`
        to declare based on the requirement).
        """
        ...

    def bind_decision(
        self,
        decision_kind: str,
        actor_kind: ActorKind,
        actor_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Record substrate Surface §C permission flow binding to identified
        actor via `AuthorityDecisionBound` event emission.

        Per `arch/substrate.md` §2.C: `request_permission` resolves to a
        `PermissionDecision` (allow / deny); when the decision binds an
        authority-bearing action to an identified actor, this callsite
        records the binding. Phase 6.1 reference: wired via injected
        `AuditEmitter`; Phase 6.2 wires the substrate permission flow →
        `bind_decision()` callsite end-to-end.

        Raises:
            DecisionBindingFailure: emitter unavailable / shutdown initiated.
            MalformedActorBinding: `actor_id` empty / decision_kind blank.
            AuthorityBindingUnreachable: mechanism not in ready state.
        """
        ...

    async def shutdown(self) -> None:
        """Idempotent shutdown — flip `is_ready` to False; subsequent
        `bind_decision()` calls raise `AuthorityBindingUnreachable`.

        Per `ARCHITECTURE.md` §6 composite shutdown subsection: authority-
        binding is consumed by audit Surface §A `emit()`, so the mechanism's
        `check()` MUST remain consultable until audit storage realization
        shuts down LAST. Reference impl keeps `check()` policy-pure (stateless
        lookup against `binding_catalog`) so it continues to function after
        shutdown; `bind_decision()` (which emits events through the injected
        emitter) is the gated capability."""
        ...
