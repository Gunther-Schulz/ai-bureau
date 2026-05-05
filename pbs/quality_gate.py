"""Quality-gate Protocol Surface — Pattern A protocol per `arch/quality-gate.md`.

Per `arch/quality-gate.md` §1: the runtime-checkpoint Pattern A protocol
with mechanism-shaped Surface — a pluggable subsystem firing at runtime
checkpoints (event-triggered + periodic/threshold-triggered) to monitor
for category-collapse manifestations across all three VISION axes, surface
drift signals, and intervene per shape policy. Tri-aspect Pattern A
(Surface = mechanism; Implementations = Framework C distributable
definitions per shape; Running Instance = workspace-bound at Owner B).

Per `arch/quality-gate.md` §3: single-layer mechanism-shaped Surface (NOT
multi-class per-axis). Per the cross-axis failure cascade pattern per
`arch/axis-interactions.md` §3.4, single observation point ingesting
per-axis signals into one cumulative state is required to detect cascades
vs. independent failures.

Cardinality (§9): 1 active gate Implementation per workspace; selection
shape-mediated (NOT direct workspace.md selection — distinct from
substrate's direct selection per `arch/quality-gate.md` §5). Selection
flows: workspace.md `shape:` field → shape policy bundle gate-impl-id →
Framework C catalog resolution at workspace boot.

Surface (§2; 6 capability categories):
- §A Checkpoint firing API → `fire()`
- §B Per-axis signal ingestion → `ingest_signal()`
- §C Signal evaluation → `evaluate()`
- §D Intervention dispatch → `intervene()`
- §E Audit emission → via composition with audit Surface §A; events
  defined inline (`gate_fired` / `gate_intervention_applied` /
  `gate_threshold_crossed` / `gate_state_persisted` / `gate_state_restored`
  / `gate_active`)
- §F State management → `get_state()` (audit-trail-as-state-store reframe;
  reads via audit Surface §C); `set_state()` IS `gate_state_persisted`
  emission via audit Surface §A

Per §8: N/A — quality-gate emits skill-side via MCP audit gate ONLY
(parallel to adapter §8 + sparring §8 N/A precedents). No circularity;
no dual-emission framing.

Per §12: N/A — substrate-agnostic; Surface contracts transport-uniform.

Per §13: per-tier behavior in impl, NOT Surface. Per-impl
`deployment_tier_compat` declared per Implementation; multi-tenant gate
state isolation via session_id + actor_id discrimination at Tier 2+.

Per §14: per-shape policy variation IS the topic's PRIMARY conditional —
quality-gate IS shape-policy-mediated by definition per scope-lock DR
Hybrid Option C. Per-shape variation captured at Implementation aspect
(practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-
shape-gate / research-lab-shape-gate per W1).

Phase 6.1 thin-slice scope per `BACKLOG.md` §224: Surface itself is
shape-agnostic (the Pattern A Surface that all shape gates implement).
Concrete `practitioner_shape_gate.py` impl is the Phase 6.1 reference;
`autonomous_business_shape_gate.py` + `personal_os_shape_gate.py` +
`research_lab_shape_gate.py` impls deferred to Phase 6.2+.
"""

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from pbs.substrate import DeploymentTier
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Supporting enums (§2.A checkpoint taxonomy; §2.B per-axis signal catalog;
# §2.D intervention kinds; §4 per-impl identity)
# ---------------------------------------------------------------------------


class CheckpointKind(StrEnum):
    """Runtime checkpoint kinds per `arch/quality-gate.md` §2.A.

    Two-class checkpoint taxonomy:

    - Event-triggered checkpoints fire AT specific runtime events; gate
      evaluates engagement-quality at the event moment per ingested
      signal-set up to that moment
    - Periodic/threshold-triggered checkpoints fire on time-period elapse
      or signal-threshold crossing; gate evaluates cumulative drift
      signals across session/work-unit lifetime

    Per-shape policy declares which checkpoint-kinds active + threshold
    values + intervention mechanics per §14 cross-shape policy variation.
    """

    # Event-triggered
    PRE_SEND = "pre_send"
    PRE_CLAIM_FINALIZATION = "pre_claim_finalization"
    PRE_DECISION_LOCK = "pre_decision_lock"
    PER_EDIT = "per_edit"
    WORKFLOW_PHASE_TRANSITION = "workflow_phase_transition"
    SESSION_END = "session_end"
    # Periodic/threshold-triggered
    DRIFT_AUDIT = "drift_audit"


class AxisKind(StrEnum):
    """VISION axis identifier per `arch/quality-gate.md` §2.B per-axis
    signal catalog.

    Three axes per VISION.md (intertwining + sparring + authorship
    preservation). Used as `axis_kind` parameter to `ingest_signal()` +
    as discriminator in per-axis signal threshold declarations.
    """

    AXIS_1_INTERTWINING = "axis_1_intertwining"
    AXIS_2_SPARRING = "axis_2_sparring"
    AXIS_3_AUTHORSHIP_PRESERVATION = "axis_3_authorship_preservation"


class InterventionKind(StrEnum):
    """Intervention dispatch kinds per `arch/quality-gate.md` §2.D.

    `block` requires substrate Surface §C `request_permission` (authority-
    bound denial); `friction` + `nudge` are skill-side direct emission
    (no permission flow); `audit_only` records evaluation without
    practitioner-visible intervention.
    """

    FRICTION = "friction"
    NUDGE = "nudge"
    BLOCK = "block"
    AUDIT_ONLY = "audit_only"


class GateImplKind(StrEnum):
    """Per-shape gate-impl identifier per `arch/quality-gate.md` §4.

    Three concrete Implementations + extensible per W1 second-shape
    productization watch-list. Phase 6.1 reference impl: practitioner-
    shape-gate (full engagement procedure; fail-closed; stateful);
    Phase 6.2+ for autonomous-business / personal-OS / research-lab.

    Per §4 per-implementation declares: identity + Surface satisfaction +
    per-axis signal threshold declarations + per-shape intervention
    mechanics + per-shape error semantics + state-management mode +
    deployment-tier compatibility.
    """

    PRACTITIONER_SHAPE_GATE = "practitioner_shape_gate"
    AUTONOMOUS_BUSINESS_SHAPE_GATE = "autonomous_business_shape_gate"
    PERSONAL_OS_SHAPE_GATE = "personal_os_shape_gate"
    RESEARCH_LAB_SHAPE_GATE = "research_lab_shape_gate"


class SignalSeverity(StrEnum):
    """Per-signal severity per `arch/quality-gate.md` §2.B + §2.C.

    Per-shape thresholds compare ingested signal severity against
    per-axis threshold-set declared per Implementation (§4) — driving
    `evaluate()` verdict + `intervene()` dispatch.
    """

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GateVerdict(StrEnum):
    """Engagement-quality verdict per `arch/quality-gate.md` §2.C.

    Returned by `evaluate()`; drives `intervene()` dispatch. `pass` =
    engagement-quality acceptable; `warn` = drift signals present but
    below intervention threshold; `fail` = intervention required per
    shape policy.
    """

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


# ---------------------------------------------------------------------------
# Configuration + signal + decision + state models
# ---------------------------------------------------------------------------


class GateConfig(BaseModel):
    """Quality-gate configuration loaded at workspace boot per
    `arch/quality-gate.md` §10 boot phase 1.

    Per `arch/quality-gate.md` §4 per-implementation declares: gate-impl
    identity + per-axis signal threshold declarations + per-shape
    intervention mechanics + per-shape error semantics + state-management
    mode + deployment-tier compatibility.

    Loaded via shape-mediated selection per §5: workspace.md `shape:`
    field → shape policy bundle gate-impl-id → Framework C catalog
    resolution. Per-impl extension config (per-shape threshold-set
    specifics; intervention mechanics tuning) lives in `impl_config`.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    gate_impl: GateImplKind
    """Quality-gate Implementation identity per `arch/quality-gate.md` §4."""

    shape_id: str
    """Active shape identifier per `glossary/shape.md`. Composes with
    `gate_impl` — shape-mediated selection per §5."""

    deployment_tier: DeploymentTier
    """Per `arch/quality-gate.md` §13 + composes with substrate
    `DeploymentTier`. Per-impl deployment-tier compatibility validated
    at workspace boot per §5."""

    active_checkpoints: frozenset[CheckpointKind]
    """Checkpoint activation per §14 per-shape variation. Practitioner-
    shape activates all event-triggered + drift_audit; autonomous-
    business activates autonomous-decision checkpoints; personal-OS
    activates session_end + drift_audit only."""

    per_axis_thresholds: dict[AxisKind, dict[str, float]] = Field(default_factory=dict)
    """Per-axis signal threshold declarations per `arch/quality-gate.md`
    §4 per-impl declares + §14 per-shape variation. Inner dict maps
    signal-kind name to threshold value (specific signal-kind catalog
    per Phase 6 per-axis observability hook signal-set spec per W2)."""

    fail_closed: bool = True
    """Per §11 per-shape error semantics: practitioner-shape fail-closed
    (defensibility-critical); autonomous-business + personal-OS fail-open."""

    stateful: bool = True
    """State-management mode per §4 + §14. Stateful impls accumulate
    signals via audit-trail-as-state-store; stateless impls evaluate
    per-checkpoint without cumulative state."""

    actor_id: str
    """Gate Running Instance is `actor_kind: ai_runtime` per §7
    composition with `actor`; `actor_id` identifies the gate Instance
    in audit emissions."""

    impl_config: dict[str, Any] = Field(default_factory=dict)
    """Per-impl extension config — refined per Implementation
    (practitioner-shape-gate engagement-procedure config; autonomous-
    business-shape-gate budget-policy config; personal-OS-shape-gate
    drift-check config). Pydantic schemas per impl live in
    `pbs/impls/<impl>_gate.py` (Phase 6.1+ forthcoming)."""


class GateSignal(BaseModel):
    """Per-axis signal payload ingested at Surface §B per `arch/quality-
    gate.md` §2.B.

    Per §2.B per-axis signal catalog (axis-1 / axis-2 / axis-3 signals).
    Sources: substrate Surface §B telemetry hooks; audit Surface §C
    query API; sparring sub-mechanism event-emissions per
    `arch/sparring.md` §4; per-claim attestation chain per
    `arch/claim-defensibility.md` §3.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    axis_kind: AxisKind
    signal_kind: str
    """Per-axis signal identifier (e.g., `workflow_bypass_rate` for axis-1;
    `sparring_bypass_rate` for axis-2; `rubber_stamping_detected` for
    axis-3). Specific catalog per Phase 6 per-axis observability hook
    signal-set spec per W2."""

    value: float
    """Signal magnitude. Compared against per-axis threshold-set per
    `evaluate()` per `GateConfig.per_axis_thresholds`."""

    severity: SignalSeverity = SignalSeverity.INFO
    source_event_ref: str | None = None
    """Reference to upstream emission (audit-event id; substrate hook
    event id; sparring event id) for reasoning-chain reconstruction per
    `arch/audit.md` §2.C query API."""

    timestamp: datetime
    details: dict[str, Any] = Field(default_factory=dict)


class GateContext(BaseModel):
    """Per-checkpoint context per `arch/quality-gate.md` §2.A.

    Carries per-checkpoint scope identifiers (claim_id / work_unit_id /
    workflow_instance_id / session_id) for `fire()` evaluation. Composes
    with audit-trail per-claim / per-work-unit query semantics per
    `arch/audit.md` §2.C.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_id: str | None = None
    work_unit_id: str | None = None
    workflow_instance_id: str | None = None
    session_id: str | None = None
    actor_id: str | None = None
    """Practitioner-RECORD identity for HITL approval moments at `block`
    intervention per Surface §D + substrate Surface §C."""

    details: dict[str, Any] = Field(default_factory=dict)


class GateDecision(BaseModel):
    """Gate firing decision per `arch/quality-gate.md` §2.A.

    Returned by `fire()`; aggregates evaluation verdict + chosen
    intervention + reason. When `intervention_kind == BLOCK`, caller
    invokes substrate Surface §C `request_permission` per Surface §D.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    checkpoint_kind: CheckpointKind
    verdict: GateVerdict
    intervention_kind: InterventionKind
    reason: str
    """Human-readable explanation. Captured in
    `GateInterventionApplied.details` for L8 auditor reasoning-chain
    reconstruction."""

    triggering_signals: list[GateSignal] = Field(default_factory=list)
    """Signals that drove the verdict. Empty when `verdict == PASS`."""


class GateState(BaseModel):
    """Cumulative gate state per `arch/quality-gate.md` §2.F + §9 cross-
    session persistence.

    Per audit-trail-as-state-store reframe (§2.F): state IS the rendered
    view of `gate_state_persisted` event sequence; events ARE source of
    truth. `get_state()` reads via audit Surface §C query API filtering
    by `gate_state_persisted` events for current session/work-unit
    context. Stateless impls return an empty `GateState` (no `set_state()`
    emissions).

    Cross-deployment portability composes via audit-trail portability per
    `arch/audit.md` §G external-format export — gate state events are
    first-class in audit-trail; cross-deployment migration preserves gate
    state per audit-trail integrity invariants.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: str | None = None
    work_unit_id: str | None = None
    cumulative_signals: list[GateSignal] = Field(default_factory=list)
    """Cumulative per-axis signal accumulation across session/work-unit
    context. Stateful impls populate; stateless impls leave empty."""

    last_verdict: GateVerdict | None = None
    last_evaluated_at: datetime | None = None
    details: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Gate-emitted events (§2.E — skill-side via MCP audit gate)
# ---------------------------------------------------------------------------


class GateFired(AuditEventBase):
    """Gate fired at checkpoint per `arch/quality-gate.md` §2.E.

    `details` field carries `checkpoint_kind` + `verdict` from
    `GateDecision`."""

    event_kind: Literal["gate_fired"] = "gate_fired"


class GateInterventionApplied(AuditEventBase):
    """Intervention dispatched per `arch/quality-gate.md` §2.E.

    `details` field carries `intervention_kind` + `reason` per `GateDecision`.
    For `BLOCK` interventions, composes with substrate `PermissionDecisionEvent`
    (substrate-side authority-bound denial)."""

    event_kind: Literal["gate_intervention_applied"] = "gate_intervention_applied"


class GateThresholdCrossed(AuditEventBase):
    """Signal threshold exceeded per `arch/quality-gate.md` §2.E.

    Pre-intervention signal — emits when ingested signal value crosses
    per-axis threshold but before `intervene()` dispatch. Useful for
    pre-intervention drift visibility."""

    event_kind: Literal["gate_threshold_crossed"] = "gate_threshold_crossed"


class GateStatePersisted(AuditEventBase):
    """Gate state persistence event per `arch/quality-gate.md` §2.F audit-
    trail-as-state-store reframe.

    For stateful impls; this event IS the persistence mechanism (no
    separate gate-state-store). Composes with `arch/audit.md` §10 audit-
    trail-as-canonical-source single-write architecture."""

    event_kind: Literal["gate_state_persisted"] = "gate_state_persisted"


class GateStateRestored(AuditEventBase):
    """Gate state restored from audit-trail at boot per `arch/quality-
    gate.md` §10 boot phase 2.

    Stateful impls reconstruct cumulative engagement signals from prior
    `gate_state_persisted` events via audit Surface §C query API; emits
    upon completion."""

    event_kind: Literal["gate_state_restored"] = "gate_state_restored"


class GateActive(AuditEventBase):
    """Gate ready to fire per `arch/quality-gate.md` §10 boot phase 4.

    Composes with §9 gate-firing-vs-gate-active lifecycle distinction:
    gate-active is workspace-lifetime state from this point until shutdown;
    gate-firing is per-checkpoint event lifecycle within gate-active."""

    event_kind: Literal["gate_active"] = "gate_active"


class GateSessionSummary(AuditEventBase):
    """Final drift report event per `arch/quality-gate.md` §10 shutdown
    step 1.

    Per-impl shape (e.g., personal-OS-shape-gate periodic drift-check
    report at session_end checkpoint). `details` field carries per-impl
    summary structure."""

    event_kind: Literal["gate_session_summary"] = "gate_session_summary"


# ---------------------------------------------------------------------------
# Error categories (§11 quality-gate error categories)
# ---------------------------------------------------------------------------


class QualityGateError(Exception):
    """Base for all quality-gate class errors per `arch/quality-gate.md` §11.

    Per-shape error semantics (§11 + §14): practitioner-shape fail-closed
    (defensibility-critical; gate failures must surface to practitioner;
    no silent degradation; especially axis-3 attestation moments where
    rubber-stamping risk applies); autonomous-business-shape fail-open
    with alert (continuity prioritized; gate may auto-recover after
    intervention dispatch failure); personal-OS-shape fail-open
    (lightweight; degradation acceptable; auto-retry with reduced
    verbosity).
    """


class GateUnreachable(QualityGateError):
    """Gate impl unreachable per `arch/quality-gate.md` §11.

    Per-shape fail-closed/open semantics determines downstream behavior."""


class SignalIngestionFailure(QualityGateError):
    """Per-axis signal ingestion failure per `arch/quality-gate.md` §11.

    Substrate Surface §B telemetry hook unreachable; audit Surface §C
    query API failure; sparring sub-mechanism event-emission unreachable."""


class SignalEvaluationFailure(QualityGateError):
    """Threshold evaluation failure per `arch/quality-gate.md` §11.

    Per-shape threshold-set declaration ill-formed; signal-set incomplete
    for evaluation."""


class InterventionDispatchFailure(QualityGateError):
    """Intervention mechanics failure per `arch/quality-gate.md` §11.

    Friction not displayed; nudge not delivered; block not enforced via
    substrate Surface §C. Per-shape escalation semantics determines
    behavior."""


class GateStateRestoreFailure(QualityGateError):
    """Boot-time state-restore failure for stateful impls per
    `arch/quality-gate.md` §11.

    Audit-trail integrity violation; missing prior `gate_state_persisted`
    event. Per-shape continuation semantics — practitioner-shape fail-
    closed; autonomous-business fail-open with alert; personal-OS fail-
    open."""


class EventEmissionFailure(QualityGateError):
    """Gate-fired event emission failure per `arch/quality-gate.md` §11.

    Composes with audit Surface §11 error categories per `arch/audit.md`
    §11 (`AuditWriteError` / `AuditAppendOnlyViolation` / `AuditSchemaError`)."""


# ---------------------------------------------------------------------------
# Quality-gate Protocol Surface — 6 capability categories typed
# ---------------------------------------------------------------------------


@runtime_checkable
class QualityGateProtocol(Protocol):
    """The Quality-gate Pattern A protocol Surface (Phase 6.1 Mode 3 spec).

    Per `arch/quality-gate.md` §6 tri-aspect: Surface (this Protocol;
    mechanism layer) + Implementations (Framework C distributable
    definitions per shape — practitioner-shape-gate / autonomous-business-
    shape-gate / personal-OS-shape-gate / research-lab-shape-gate per W1)
    + Running Instance (workspace-bound at Owner B at boot via shape-
    mediated selection per §5).

    Cardinality (§5 + §9): 1 active gate Implementation per workspace;
    selection shape-mediated (NOT direct workspace.md). N gate-firing
    events per workspace lifetime.

    Gate-coupling impossible-by-construction per §6 + `MAINTENANCE.md`
    TOP-LEVEL DESIGN PRINCIPLES §1: Surface-typed skill code structurally
    cannot reach impl-specific intervention mechanics without explicit
    isinstance check on per-shape Extension Protocol (per §15 forward-
    reference; Phase 6 spec target). One of three canonical examples of
    structural-over-conventional discipline applied at framework primitive
    design (parallel to substrate-coupling-impossible per
    `arch/substrate.md` §6 + adapter-impl-coupling-impossible per
    `arch/adapter.md` §6).

    Pattern A topic-template-class FORMAL STABILITY achieved with three
    instances complete (substrate anchor + adapter second + quality-gate
    third) per `arch/quality-gate.md` §17 + `docs/decisions/pattern-a-
    template-7th-conditional-cross-shape-variation.md` per-pattern
    instance-driven trigger.

    Phase 6.1 thin-slice scope per `BACKLOG.md` §224: this Surface is
    shape-agnostic; Phase 6.1 reference impl is practitioner-shape-gate
    (`pbs/impls/practitioner_shape_gate.py` forthcoming); autonomous-
    business / personal-OS / research-lab impls deferred to Phase 6.2+.
    """

    # ------------------------------------------------------------------
    # Per-instance identity (Surface uniformity with Pattern A peers)
    # ------------------------------------------------------------------

    @property
    def gate_impl(self) -> GateImplKind:
        """Quality-gate Implementation identity per `arch/quality-gate.md` §4."""
        ...

    @property
    def shape_id(self) -> str:
        """Active shape identifier per `glossary/shape.md`. Composes with
        `gate_impl` — shape-mediated selection per §5."""
        ...

    # ------------------------------------------------------------------
    # Lifecycle (§9 + §10 boot/shutdown sequence)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(cls, config: GateConfig) -> "QualityGateProtocol":
        """Instantiate gate Implementation per `arch/quality-gate.md` §10
        boot phase 1.

        Loads config; validates per-axis threshold declarations against
        gate-impl's per-axis signal-kind catalog (per §5); validates
        gate-impl deployment-tier compatibility against `config.deployment_tier`.
        Returns ready-to-restore-state instance (caller invokes restore-
        state for stateful impls before `is_ready` becomes True).

        Raises:
            GateUnreachable: gate impl unreachable.
            SignalEvaluationFailure: per-shape threshold-set declaration
                ill-formed at validation.
        """
        ...

    @property
    def is_ready(self) -> bool:
        """True after boot phase 4 completes (gate emitted `GateActive`
        event) per `arch/quality-gate.md` §10. Once True, `fire()` accepts
        per-checkpoint events."""
        ...

    async def shutdown(self) -> None:
        """Quality-gate shutdown per `arch/quality-gate.md` §10 shutdown
        sequence.

        Steps 1-4 per §10:

        1. Emit final drift report event (`gate_session_summary` or
           per-impl shape; e.g., personal-OS-shape-gate periodic drift-
           check report at session_end checkpoint)
        2. Gate state persistence — stateful impls flush cumulative
           signals via `gate_state_persisted` event emission to audit
           Surface §A
        3. Gate unsubscribes from observability hooks (substrate Surface
           §B telemetry hooks; audit Surface §C query subscriptions;
           sparring sub-mechanism event-emission subscriptions)
        4. Gate shutdown returns; audit storage realization shutdown
           follows per `arch/audit.md` §10 shutdown steps 4-7 (drains
           pending events including gate state events; flushes audit-
           trail to storage; verifies hash-chain integrity)
        """
        ...

    # ------------------------------------------------------------------
    # §A Checkpoint firing API
    # ------------------------------------------------------------------

    async def fire(
        self,
        checkpoint_kind: CheckpointKind,
        context: GateContext,
    ) -> GateDecision:
        """Fire the gate at a runtime checkpoint per `arch/quality-gate.md`
        §2.A.

        Two-class checkpoint taxonomy (event-triggered + periodic/
        threshold-triggered) per `CheckpointKind`. Per-shape policy
        declares which checkpoint-kinds active per
        `GateConfig.active_checkpoints`. Composite operation: evaluates
        ingested signal-set per `evaluate()`; dispatches intervention
        per `intervene()` when verdict != `PASS`; emits `GateFired` audit
        event with verdict.

        Raises:
            SignalEvaluationFailure: per-shape threshold-set declaration
                ill-formed; signal-set incomplete for evaluation.
            InterventionDispatchFailure: intervention mechanics failure
                (friction not displayed; nudge not delivered; block not
                enforced via substrate Surface §C).
            EventEmissionFailure: gate-fired event emission failure.
        """
        ...

    # ------------------------------------------------------------------
    # §B Per-axis signal ingestion
    # ------------------------------------------------------------------

    def ingest_signal(self, signal: GateSignal) -> None:
        """Ingest a per-axis-failure-mode signal per `arch/quality-gate.md`
        §2.B.

        Sources: substrate Surface §B telemetry hooks; audit Surface §C
        query API; sparring sub-mechanism event-emissions per
        `arch/sparring.md` §4; per-claim attestation chain mechanics per
        `arch/claim-defensibility.md` §3.

        For stateful impls, ingested signals accumulate in `GateState.cumulative_signals`
        for cross-checkpoint cumulative observability per the cross-axis
        failure cascade pattern per `arch/axis-interactions.md` §3.4.
        Stateless impls evaluate in-memory per-checkpoint without
        accumulation.

        Emits `GateThresholdCrossed` when ingested signal value crosses
        per-axis threshold (pre-intervention drift visibility).

        Raises:
            SignalIngestionFailure: ingestion failure (signal source
                unreachable; schema mismatch).
        """
        ...

    # ------------------------------------------------------------------
    # §C Signal evaluation
    # ------------------------------------------------------------------

    def evaluate(
        self,
        checkpoint_kind: CheckpointKind,
        signal_set: list[GateSignal],
    ) -> GateVerdict:
        """Evaluate signal-set against per-shape threshold-set per
        `arch/quality-gate.md` §2.C.

        Per-shape impl declares thresholds + evaluation logic per
        Implementation aspect (§4). Cumulative observability across axes
        — single evaluation point ingesting per-axis signals into one
        cumulative state per the cross-axis failure cascade pattern
        requirement per `arch/axis-interactions.md` §3.4.

        Returns engagement-quality verdict (`PASS` / `WARN` / `FAIL`).
        Drives `intervene()` dispatch.

        Raises:
            SignalEvaluationFailure: per-shape threshold-set declaration
                ill-formed; signal-set incomplete for evaluation.
        """
        ...

    # ------------------------------------------------------------------
    # §D Intervention dispatch
    # ------------------------------------------------------------------

    async def intervene(
        self,
        decision: GateDecision,
        context: GateContext,
    ) -> None:
        """Dispatch intervention per `arch/quality-gate.md` §2.D.

        `intervention_kind` per `GateDecision`:
        - `BLOCK` → authority-bound denial via substrate Surface §C
          `request_permission`; emits `GateInterventionApplied` after
          permission flow resolves
        - `FRICTION` / `NUDGE` → skill-side direct emission (no permission
          flow); emits `GateInterventionApplied`
        - `AUDIT_ONLY` → records evaluation without practitioner-visible
          intervention; emits `GateInterventionApplied`

        Authority-binding records `actor_kind: ai_runtime` per
        `glossary/authority-binding.md` (gate is AI-runtime actor at
        intervention emission); composes with substrate
        `PermissionDecisionEvent` for `BLOCK` interventions.

        Raises:
            InterventionDispatchFailure: intervention mechanics failure.
            EventEmissionFailure: emission of `GateInterventionApplied`
                failed.
        """
        ...

    # ------------------------------------------------------------------
    # §F State management (audit-trail-as-state-store reframe)
    # ------------------------------------------------------------------

    def get_state(
        self,
        session_id: str | None = None,
        work_unit_id: str | None = None,
    ) -> GateState:
        """Retrieve gate state per `arch/quality-gate.md` §2.F.

        Reads via audit Surface §C query API filtering by
        `gate_state_persisted` events for given session/work-unit
        context. Stateless impls return empty `GateState` (no
        accumulation).

        Per audit-trail-as-state-store reframe: state IS the rendered
        view of `gate_state_persisted` event sequence per the same
        pattern as workspace state rendered from event-stream per
        `arch/audit.md` §F.

        Raises:
            GateStateRestoreFailure: audit-trail integrity violation;
                state reconstruction failure.
        """
        ...

    def set_state(self, state: GateState) -> None:
        """Persist gate state per `arch/quality-gate.md` §2.F.

        IS `gate_state_persisted` event emission via audit Surface §A.
        Audit-trail IS state-store: NO separate gate-state-store. Avoids
        dual-store divergence; preserves single-write architecture per
        `arch/audit.md` §10 audit-trail-as-canonical-source.

        Stateless impls treat as no-op (configuration `stateful = False`
        per `GateConfig`).

        Raises:
            EventEmissionFailure: `gate_state_persisted` emission failed
                (composes with audit Surface §11 error categories).
        """
        ...
