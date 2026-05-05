"""Practitioner-shape authority-binding mechanism — Phase 6.1 reference impl.

Per `glossary/authority-binding.md` + `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE
concept-by-concept table 'Authority binding' row + `docs/decisions/audit-arch-
topic.md` §7 Trust subsumption rationale: authority-binding is its own
framework primitive (mechanism-level, NOT Pattern A protocol); per-shape
policy declares the trust model parameterizing how that binding satisfies
shape-specific accountability requirements.

This module realizes the **practitioner-shape policy bundle** for the
authority-binding mechanism Surface (`AuthorityBindingProtocol`). The
practitioner-shape trust model (PRACTITIONER_JUDGMENT) declares HUMAN
actor required for accountability-bearing legal-bind moments
(signature_applied / send_authorized / claim_attested /
work_unit_archived / workflow_phase_transition events) per
`glossary/authority-binding.md` cross-archetype examples + `arch/audit.md`
§14 cross-shape policy variation 'Trust model' row.

Surface satisfaction (`pbs.authority_binding.AuthorityBindingProtocol`):

- **Per-event actor declaration** → `check(event)` validates `event.actor_kind`
  against `binding_catalog[event.event_kind].required_actor_kinds` for
  catalog-listed event_kinds; non-catalog events accepted (framework-baseline
  declaration only — `AuditEventBase` schema enforces field presence)
- **Per-claim author attribution** → `require_actor_kind(event_kind)` returns
  the per-shape required `actor_kind` set; consumers (skill code,
  pre-emission introspection) consult before constructing AuditEvent
- **Authority-decision binding** → `bind_decision(decision_kind, actor_kind,
  actor_id, context)` emits `AuthorityDecisionBound` via injected
  `AuditEmitter` per `arch/substrate.md` §2.C composition wiring point;
  Phase 6.1 collapses substrate permission flow → bind_decision callsite
  to direct injection; Phase 6.2 wires substrate's `request_permission` →
  `bind_decision()` end-to-end

Composition with audit class (per `arch/audit.md` §11 + Phase 6.1
`pbs/impls/claude_agent_sdk_audit.py` `AuthorityChecker` injection point):

```python
binding = await PractitionerShapeAuthorityBinding.from_config_with_emitter(
    config=PractitionerShapeAuthorityBindingConfig(),
    emitter=audit.emit,
)
audit_config = ClaudeAgentSDKAuditConfig(
    audit_trail_path=path,
    authority_checker=binding.check,  # bound method conforming to AuthorityChecker
)
```

Audit's `emit()` consults `binding.check` at every emission per `arch/audit.md`
§2.A; on policy denial, audit raises `AuditTrustError` (the mechanism
returns False; audit raises the error category — clean separation per
`AuthorityBindingProtocol.check` docstring).

Per `arch/audit.md` §10 + `ARCHITECTURE.md` §6 composite boot subsection:
audit-phase 1-3 ready BEFORE this mechanism is constructed (the mechanism
emits `AuthorityDecisionBound` through the injected `audit.emit`).

Phase 6.1 thin-slice scope per `BACKLOG.md` §224: practitioner-shape only;
autonomous-business-shape-authority-binding (BUDGET_POLICY trust model;
budget-threshold + HITL approval) + personal-OS-shape-authority-binding
(INDIVIDUAL trust model; minimal enforcement) deferred to Phase 6.2 per
W1 second-shape productization.

Phase 6 wiring points (marked explicitly in docstrings):

- Substrate permission flow → `bind_decision()` callsite end-to-end
  (substrate Surface §C `request_permission` resolves → bind_decision
  records the binding; Phase 6.2 wires the substrate impl side)
- Per-shape catalog finalization per pioneer deployment data (W2 watch-
  list); reference impl ships canonical accountability-bearing event_kind
  catalog drawn from `glossary/authority-binding.md` cross-archetype
  examples + composes-with relationships in `glossary/work-unit.md` /
  `glossary/workflow.md` / `glossary/claim.md`
- Cross-deployment authority-binding portability — claim_made +
  authority_decision_bound events carry actor identity at Owner B per
  `arch/scope-model.md` E5 placement pattern; cross-deployment ingestion
  semantics per `arch/practitioner.md` W1 + `arch/scope-model.md` W2
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import ConfigDict, Field

from pbs.authority_binding import (
    AuditEmitter,
    AuthorityBindingConfig,
    AuthorityBindingUnreachable,
    AuthorityChecker,
    AuthorityDecisionBound,
    BindingRequirement,
    DecisionBindingFailure,
    TrustModel,
)
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Practitioner-shape default binding catalog
# ---------------------------------------------------------------------------


PRACTITIONER_SHAPE_BINDING_CATALOG: dict[str, BindingRequirement] = {
    "signature_applied": BindingRequirement(
        required_actor_kinds=frozenset({ActorKind.HUMAN}),
    ),
    "send_authorized": BindingRequirement(
        required_actor_kinds=frozenset({ActorKind.HUMAN}),
    ),
    "claim_attested": BindingRequirement(
        required_actor_kinds=frozenset({ActorKind.HUMAN}),
    ),
    "work_unit_archived": BindingRequirement(
        required_actor_kinds=frozenset({ActorKind.HUMAN}),
    ),
    "workflow_phase_transition": BindingRequirement(
        required_actor_kinds=frozenset({ActorKind.HUMAN}),
    ),
    "claim_made": BindingRequirement(
        required_actor_kinds=frozenset(
            {ActorKind.AI_RUNTIME, ActorKind.HUMAN}
        ),
        required_detail_fields=frozenset({"skill_id"}),
    ),
    "sparring_round_completed": BindingRequirement(
        required_actor_kinds=frozenset({ActorKind.AI_RUNTIME}),
    ),
}
"""Per `glossary/authority-binding.md` cross-archetype 'Practitioner-shape'
example: HUMAN actor required for legal-bind moments + AI_RUNTIME for
production-phase engagement attribution.

Catalog sources:
- `signature_applied` / `send_authorized` / `claim_attested` — practitioner
  legal-bind moments per `glossary/authority-binding.md`
- `work_unit_archived` — per `glossary/work-unit.md` composes-with
  authority-binding row 'practitioner-shape send/archive = practitioner-only
  per defensibility-critical'
- `workflow_phase_transition` — per `glossary/workflow.md` composes-with
  authority-binding row 'phase-transition events bound to authority-decision
  actor per workflow definition `phase_authority_requirements`'
- `claim_made` — per `glossary/authority-binding.md` cross-archetype
  'every claim_made event records actor_kind: skill (or ai_runtime per
  actor.md naming-note) + skill identifier'; AI_RUNTIME OR HUMAN both
  valid (skill-emitted vs. human-attested claim creation)
- `sparring_round_completed` — per `glossary/authority-binding.md`
  cross-archetype 'every sparring_round_completed event records
  actor_kind: ai_runtime'

Reference catalog — Phase 6.1 thin-slice; Phase 6.2 deployment-instance
wiring may EXTEND (per-specialist accountability events per `arch/audit.md`
§2.E catalog management three-layer model)."""


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class PractitionerShapeAuthorityBindingConfig(AuthorityBindingConfig):
    """Per-shape config bundle for the practitioner-shape authority-binding
    mechanism. Pins `trust_model=PRACTITIONER_JUDGMENT` + ships the
    practitioner-shape default `binding_catalog`.

    Per `glossary/authority-binding.md` 'Composes with policy' + `arch/audit.md`
    §14: the per-shape policy declares the trust model; the mechanism Surface
    is fixed at framework-mechanism layer.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    trust_model: TrustModel = TrustModel.PRACTITIONER_JUDGMENT

    binding_catalog: dict[str, BindingRequirement] = Field(
        default_factory=lambda: dict(PRACTITIONER_SHAPE_BINDING_CATALOG),
    )


# ---------------------------------------------------------------------------
# PractitionerShapeAuthorityBinding — Implementation class
# ---------------------------------------------------------------------------


class PractitionerShapeAuthorityBinding:
    """Practitioner-shape authority-binding mechanism satisfying
    `AuthorityBindingProtocol` per `glossary/authority-binding.md`.

    Surface satisfaction is structural — instances pass
    `isinstance(binding, AuthorityBindingProtocol)` per the `runtime_checkable`
    Protocol decorator on `pbs.authority_binding.AuthorityBindingProtocol`.

    State (instance-private):

    - `_config`: per-shape config bundle (trust_model + binding_catalog)
    - `_emitter`: injected `AuditEmitter` callable for `bind_decision()`
      emissions (Phase 6.1 collapses substrate permission flow → audit
      Surface §A path to direct injection)
    - `_instance_id`: stable identity used as `actor_id` on
      `AuthorityDecisionBound` events emitted by this mechanism
    - `_is_ready`: True between construction and shutdown
    - `_is_shutting_down`: idempotent guard for repeated shutdown calls

    Per `AuthorityBindingProtocol.shutdown` docstring: `check()` remains
    consultable after shutdown (policy-pure stateless lookup) so audit
    Surface §A `emit()` continues to validate during audit's OWN shutdown
    drain per `ARCHITECTURE.md` §6 composite shutdown subsection step 9
    audit-storage-realization-shuts-down-LAST invariant. `bind_decision()`
    is the gated capability — raises `AuthorityBindingUnreachable` after
    shutdown.
    """

    def __init__(
        self,
        config: PractitionerShapeAuthorityBindingConfig,
        emitter: AuditEmitter,
    ) -> None:
        """Internal constructor. Use `from_config_with_emitter()` factory."""
        self._config = config
        self._emitter = emitter
        self._instance_id: str = (
            f"authority_binding:practitioner_shape:"
            f"{config.trust_model.value}"
        )
        self._is_ready: bool = False
        self._is_shutting_down: bool = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @classmethod
    async def from_config_with_emitter(
        cls,
        config: PractitionerShapeAuthorityBindingConfig,
        emitter: AuditEmitter,
    ) -> PractitionerShapeAuthorityBinding:
        """Boot per `glossary/authority-binding.md` framework-mechanism
        lifetime + `ARCHITECTURE.md` §6 composite boot subsection.

        Precondition: audit-phase 1-3 ready (the mechanism's
        `bind_decision()` emits through the injected `emitter`); substrate-
        phase 1+ may proceed in parallel since the mechanism produces a
        `check()` callable consumed by audit Surface §A only when audit
        emits.

        The mechanism is ready immediately after construction (no boot
        phases beyond initialization). Async factory matches the precedent
        across `pbs/impls/claude_agent_sdk_audit.py` /
        `pbs/impls/practitioner_shape_gate.py` for cross-impl consistency.

        Raises:
            DecisionBindingFailure: emitter is None / not callable.
        """
        if emitter is None or not callable(emitter):
            raise DecisionBindingFailure(
                "PractitionerShapeAuthorityBinding requires a callable "
                "AuditEmitter at construction; received None / non-callable."
            )
        instance = cls(config, emitter)
        instance._is_ready = True
        return instance

    @property
    def is_ready(self) -> bool:
        return self._is_ready and not self._is_shutting_down

    @property
    def trust_model(self) -> TrustModel:
        return self._config.trust_model

    async def shutdown(self) -> None:
        """Per `AuthorityBindingProtocol.shutdown`. Idempotent. Flips
        `is_ready` to False; `bind_decision()` then raises
        `AuthorityBindingUnreachable`. `check()` remains consultable
        (policy-pure stateless lookup) per the Surface contract — audit
        Surface §A continues to validate during audit's OWN shutdown
        drain.
        """
        if self._is_shutting_down:
            return
        self._is_shutting_down = True
        self._is_ready = False

    # ------------------------------------------------------------------
    # Per-event actor declaration (sub-aspect 1)
    # ------------------------------------------------------------------

    def check(self, event: AuditEventBase) -> bool:
        """Per `AuthorityBindingProtocol.check`. Returns True if the event
        satisfies the practitioner-shape binding catalog requirement for
        its `event_kind`; False on:

        - `event.actor_kind` not in `BindingRequirement.required_actor_kinds`
        - `event.actor_id` empty (framework-level field present per Pydantic
          schema; per-shape policy adds non-empty requirement)
        - any `BindingRequirement.required_detail_fields` entry missing /
          empty in `event.details`

        Events whose `event_kind` is not in `binding_catalog` are accepted
        (framework-baseline emission only; `AuditEventBase` schema enforces
        actor_kind / actor_id presence already).

        Pure-policy lookup; remains consultable after shutdown per
        `AuthorityBindingProtocol.shutdown` contract (audit Surface §A
        emit consults this during audit's own shutdown drain).
        """
        requirement = self._config.binding_catalog.get(event.event_kind)
        if requirement is None:
            return True
        if event.actor_kind not in requirement.required_actor_kinds:
            return False
        if not event.actor_id:
            return False
        for detail_field in requirement.required_detail_fields:
            value = event.details.get(detail_field)
            if value is None or value == "":
                return False
        return True

    # ------------------------------------------------------------------
    # Per-claim author attribution (sub-aspect 2)
    # ------------------------------------------------------------------

    def require_actor_kind(
        self, event_kind: str
    ) -> frozenset[ActorKind] | None:
        """Per `AuthorityBindingProtocol.require_actor_kind`. Returns the
        per-shape required `actor_kind` set for the given event_kind, or
        None if the event_kind is not accountability-bearing under the
        practitioner-shape catalog.
        """
        requirement = self._config.binding_catalog.get(event_kind)
        if requirement is None:
            return None
        return requirement.required_actor_kinds

    # ------------------------------------------------------------------
    # Authority-decision binding (sub-aspect 3)
    # ------------------------------------------------------------------

    def bind_decision(
        self,
        decision_kind: str,
        actor_kind: ActorKind,
        actor_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Per `AuthorityBindingProtocol.bind_decision`. Emits
        `AuthorityDecisionBound` via injected `AuditEmitter`.

        Validation (raises before emission attempt):
        - `decision_kind` non-empty
        - `actor_id` non-empty

        Lifecycle gate:
        - Mechanism in ready state (raises `AuthorityBindingUnreachable`
          after shutdown)

        Phase 6 wiring point: substrate Surface §C `request_permission` →
        `bind_decision()` callsite end-to-end. Reference impl is direct
        emission via injected emitter (matches Phase 6.1 precedent across
        `pbs/impls/claude_agent_sdk_substrate.py` /
        `pbs/impls/practitioner_shape_gate.py`).
        """
        if not self.is_ready:
            raise AuthorityBindingUnreachable(
                f"PractitionerShapeAuthorityBinding not in ready state; "
                f"bind_decision('{decision_kind}') rejected."
            )
        if not decision_kind:
            raise DecisionBindingFailure(
                "bind_decision: decision_kind must be non-empty."
            )
        if not actor_id:
            raise DecisionBindingFailure(
                "bind_decision: actor_id must be non-empty per per-shape "
                "policy (PRACTITIONER_JUDGMENT requires identified actor)."
            )
        details: dict[str, Any] = {
            "decision_kind": decision_kind,
            "trust_model": self._config.trust_model.value,
        }
        if context is not None:
            details["context"] = dict(context)
        event = AuthorityDecisionBound(
            actor_kind=actor_kind,
            actor_id=actor_id,
            timestamp=datetime.now(tz=UTC),
            details=details,
        )
        self._emitter(event)

    # ------------------------------------------------------------------
    # Audit Surface §A injection helper
    # ------------------------------------------------------------------

    def to_authority_checker(self) -> AuthorityChecker:
        """Returns the bound `check` method as an `AuthorityChecker` callable
        for audit Surface §A injection per `pbs/impls/claude_agent_sdk_audit.py`
        `AuthorityChecker` injection point.

        Equivalent to passing `binding.check` directly; this helper exists
        for explicit composition + future wrapping (e.g., adding telemetry
        hook subscriptions per Phase 6.2).
        """
        return self.check
