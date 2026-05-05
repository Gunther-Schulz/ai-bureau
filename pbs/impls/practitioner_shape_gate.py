"""Practitioner-shape quality-gate Implementation — Phase 6.1 reference impl.

Per `arch/quality-gate.md` §4 per-implementation aspect: wraps per-shape
engagement-quality enforcement to satisfy the Quality-gate Pattern A Surface
(`QualityGateProtocol`). Implementations live at Framework C scope as
distributable definitions per `glossary/framework-c-scope.md` + `arch/quality-
gate.md` §6 tri-aspect (Surface = mechanism; Implementations = Framework C
definitions per shape; Running Instance = workspace-bound at Owner B at
boot via shape-mediated selection per §5).

Per `arch/quality-gate.md` §4 per-implementation declares (this impl):

- **Implementation identity**: `practitioner_shape_gate`
- **Surface satisfaction**: §A `fire()` / §B `ingest_signal()` / §C
  `evaluate()` / §D `intervene()` / §E audit emission catalog (skill-side
  via injected `AuditEmitter` per §8) / §F `get_state()` / `set_state()`
  (audit-trail-as-state-store reframe)
- **Per-axis signal threshold declarations**: configured via
  `GateConfig.per_axis_thresholds`; reference impl ships practitioner-shape
  defaults (axis-3 PRIMARY: rubber-stamping detection mandatory per
  `glossary/rubber-stamping.md`; axis-2 sparring-bypass + answer-machine
  extraction tracked; axis-1 workflow-bypass tracked) per §14 row 2
- **Per-shape intervention mechanics**: friction + nudge + block +
  practitioner attestation + re-engagement per §14 row 3 practitioner-shape
  column; `block` routes through substrate Surface §C `request_permission`
  (HITL approval) per §2.D; `friction` / `nudge` / `audit_only` skill-side
  direct emission
- **Per-shape error semantics**: fail-closed (defensibility-critical;
  gate failures must surface to practitioner; no silent degradation) per
  §11 + §14 row 4 — parallel to practitioner-shape adapter §11 + audit §11
- **State-management mode**: stateful (cumulative engagement signals
  across session via audit-trail per §2.F audit-trail-as-state-store
  reframe) per §14 row 5
- **Deployment-tier compatibility**: Tier 1 native; Tier 2 cloud (multi-
  tenant gate state isolation via `session_id` + `actor_id` discrimination
  per §13); Tier 3 federated per W3 watch-list

Per `arch/quality-gate.md` §6 gate-coupling impossible-by-construction +
`MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code using only
`QualityGateProtocol` methods is gate-portable across shape impls; per-
shape intervention mechanics specifics are NOT in Surface (per §2 'Explicitly
NOT in Surface' list) — Phase 6 introduces a typed
`PractitionerShapeGateExtension` Protocol per §4 + §15 per-shape extension
Protocols pattern for the isinstance-gated gate-impl-pinned code path
(parallel to `arch/substrate.md` §4 + `arch/adapter.md` §4).

Per `arch/quality-gate.md` §8: gate emits skill-side via MCP audit gate
ONLY (no substrate-internal direct emission path; no dual-emission
framing — N/A per Pattern A template §8 conditional applicability rule).
Phase 6.1 collapses the skill-side MCP audit gate path to a directly-
injected `AuditEmitter` callable matching substrate's emitter shape per
the Note 75-77 thin-slice convention; Phase 6.2 wires the actual MCP
audit gate (registered by substrate per `arch/substrate.md` §8) routing
gate emissions through the gate's MCP `record_audit_event` tool to the
audit storage realization. Read-back path (state restore) injected as
`AuditEventKindQuerier` callable matching audit Surface §C
`query_per_event_kind` shape; Phase 6.2 wires the actual audit Surface
§C query API end-to-end.

Per `arch/quality-gate.md` §10 boot phase ordering (gate-phase 1-4
follows substrate-phase 5 `boot_complete` per cross-axis composite boot
integration per `arch/axis-interactions.md` §3.5): audit-phase 1-3 ready
+ substrate-phase 1-5 complete BEFORE gate-phase 1.

Phase 6.1 thin-slice scope per `BACKLOG.md` §224: practitioner-shape-gate
only; autonomous-business-shape-gate + personal-OS-shape-gate +
research-lab-shape-gate (W1) deferred to Phase 6.2+. Per-axis observability
hook signal-set spec + per-axis threshold-set tuning per W2 watch-list
deliver at Phase 1+ pioneer deployment data.

Phase 6 wiring points (marked explicitly in docstrings + via skill-side
hook gaps where load-bearing):

- Per-axis observability hook subscription (gate-phase 3): substrate
  Surface §B telemetry hooks + audit Surface §C query API + sparring
  sub-mechanism event-emission subscriptions per `arch/sparring.md` §4
  (reference impl records intent only)
- Real intervention mechanics (friction display; nudge delivery; block
  enforcement via substrate Surface §C `request_permission`): reference
  impl emits `GateInterventionApplied` audit event but defers concrete
  display + HITL approval flow to Phase 6 deployment-instance wiring
- Per-axis signal-kind catalog finalization per W2: reference impl
  accepts any `signal_kind` string; Phase 6 spec lands the full signal-kind
  catalog + threshold semantics + diagnostic emission contract
- Cross-deployment gate-state portability mechanics per W3: reference
  impl persists state via `gate_state_persisted` events (first-class in
  audit-trail per `arch/audit.md` §G external-format export); concrete
  cross-deployment ingestion semantics per `arch/practitioner.md` W1 +
  `arch/scope-model.md` W1+W2
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import ConfigDict

from pbs.quality_gate import (
    AxisKind,
    CheckpointKind,
    EventEmissionFailure,
    GateActive,
    GateConfig,
    GateContext,
    GateDecision,
    GateFired,
    GateImplKind,
    GateInterventionApplied,
    GateSessionSummary,
    GateSignal,
    GateState,
    GateStatePersisted,
    GateStateRestoreFailure,
    GateStateRestored,
    GateThresholdCrossed,
    GateUnreachable,
    GateVerdict,
    InterventionDispatchFailure,
    InterventionKind,
    SignalEvaluationFailure,
    SignalSeverity,
)
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Gate identity + audit-binding type aliases
# ---------------------------------------------------------------------------


GATE_IMPL_ID: Literal[GateImplKind.PRACTITIONER_SHAPE_GATE] = (
    GateImplKind.PRACTITIONER_SHAPE_GATE
)
"""Quality-gate Implementation identity per `arch/quality-gate.md` §4. This
Implementation is one of three concrete gate Impls in the current set
(practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-
shape-gate) + extensible per W1 second-shape productization watch-list
(research-lab-shape-gate preliminary).
"""


AuditEmitter = Callable[[AuditEventBase], None]
"""Audit Surface §A emit binding per `arch/quality-gate.md` §8 skill-side
MCP audit gate path. Injected at construction; the callable shape matches
substrate's `AuditEmitter` for single-process Phase 6.1 deployment.

Per `arch/quality-gate.md` §8: gate emits audit events ONLY via skill-side
MCP audit gate (no substrate-internal direct emission path; no dual-
emission framing). Phase 6.1 collapses the skill-side MCP audit gate
path to a directly-injected `AuditEmitter` callable matching substrate's
emitter shape; Phase 6.2 wires an actual MCP audit gate (registered by
substrate per `arch/substrate.md` §8) routing gate emissions through the
gate's MCP `record_audit_event` tool to the audit storage realization.

Per `arch/audit.md` §10 + `ARCHITECTURE.md` §6 composite boot subsection:
audit-phase 1-3 ready + substrate-phase 1-5 complete BEFORE gate-phase
1 (parallel to substrate Precondition).
"""


AuditEventKindQuerier = Callable[[str], list[AuditEventBase]]
"""Audit Surface §C `query_per_event_kind` binding per `arch/quality-gate.md`
§2.F audit-trail-as-state-store reframe + §10 boot phase 2 state-restore.

Returns the list of prior `AuditEventBase` instances whose `event_kind`
matches the argument. Reference impl filters by `session_id` /
`work_unit_id` in pure Python after fetching the per-event-kind result;
Phase 6.2 wires composite query primitives + indexed lookup per
`arch/audit.md` §15 query implementation.

Phase 6.1 collapses the audit Surface §C query API to a single per-event-
kind callable matching the audit Surface's existing
`query_per_event_kind` method (`pbs.audit.AuditProtocol.query_per_event_kind`);
Phase 6.2 wires the full audit Surface §C query API surface end-to-end
(per-claim / per-actor / per-time-window / per-work-unit composability).
"""


# ---------------------------------------------------------------------------
# Per-shape policy defaults (§14 row 2-5 practitioner-shape column)
# ---------------------------------------------------------------------------


PRACTITIONER_SHAPE_ACTIVE_CHECKPOINTS: frozenset[CheckpointKind] = frozenset(
    {
        CheckpointKind.PRE_SEND,
        CheckpointKind.PRE_CLAIM_FINALIZATION,
        CheckpointKind.PER_EDIT,
        CheckpointKind.DRIFT_AUDIT,
    }
)
"""Per `arch/quality-gate.md` §14 row 1 practitioner-shape column: full
enforcement (pre_send + pre_claim_finalization + per_edit + drift_audit).
Authoritative gate-firing-checkpoints set for the practitioner shape."""


PRACTITIONER_SHAPE_DEFAULT_THRESHOLDS: dict[AxisKind, dict[str, float]] = {
    AxisKind.AXIS_1_INTERTWINING: {
        "workflow_bypass_rate": 0.30,
    },
    AxisKind.AXIS_2_SPARRING: {
        "sparring_bypass_rate": 0.20,
        "answer_machine_extraction_rate": 0.20,
    },
    AxisKind.AXIS_3_AUTHORSHIP_PRESERVATION: {
        "rubber_stamping_detected": 1.0,
        "engagement_depth_floor": 0.40,
    },
}
"""Per `arch/quality-gate.md` §14 row 2 practitioner-shape column: strict
per-axis (axis-3 PRIMARY; rubber-stamping detection mandatory per
`glossary/rubber-stamping.md`).

Reference defaults — concrete catalog + tuning per W2 (Phase 1+ pioneer
deployment data); reference values are Phase 6.1 placeholders sufficient
for Surface satisfaction + structural smoke-test verification, NOT
production-tuned thresholds. Per-axis signal-kind names align with the
`GateSignal.signal_kind` field; values are 'value at-or-above signals
threshold-cross' per `evaluate()` semantics.
"""


# ---------------------------------------------------------------------------
# Configuration (per-impl extension surface; reuses GateConfig directly)
# ---------------------------------------------------------------------------


class PractitionerShapeGateConfig(GateConfig):
    """Per-impl configuration per `arch/quality-gate.md` §4 per-implementation
    declares 'Configuration schema (per-impl config — Pydantic; Phase 6)'.

    Pins `gate_impl` to `PRACTITIONER_SHAPE_GATE` and `fail_closed` to True
    per §11 + §14 row 4 (defensibility-critical; gate failures must surface
    to practitioner; no silent degradation). `stateful` pinned True per §14
    row 5 (cumulative engagement signals across session via audit-trail).

    Framework-level config (`shape_id` / `deployment_tier` /
    `active_checkpoints` / `per_axis_thresholds` / `actor_id` / `impl_config`)
    inherited from `GateConfig`. Reference impl ships practitioner-shape
    defaults for `active_checkpoints` + `per_axis_thresholds` when the
    caller does not supply explicit values via the construction helper
    `with_practitioner_defaults()`.

    Per `arch/quality-gate.md` §15 pre-implementation operational concerns:
    per-checkpoint timeout / per-impl extension config (engagement-procedure
    config; nudge-wording catalog; re-engagement cadence) lives in
    `impl_config` and surfaces concretely at Phase 6 pre-implementation-
    sharpening + deployment-instance wiring.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    gate_impl: Literal[GateImplKind.PRACTITIONER_SHAPE_GATE] = GATE_IMPL_ID
    """Pinned per `arch/quality-gate.md` §4 per-implementation declares
    Implementation identity."""

    fail_closed: Literal[True] = True
    """Pinned True per `arch/quality-gate.md` §11 + §14 row 4 practitioner-
    shape error semantics (fail-closed; defensibility-critical)."""

    stateful: Literal[True] = True
    """Pinned True per `arch/quality-gate.md` §14 row 5 practitioner-shape
    state management (cumulative engagement signals across session via
    audit-trail-as-state-store)."""

    @classmethod
    def with_practitioner_defaults(
        cls,
        shape_id: str,
        deployment_tier: object,
        actor_id: str,
    ) -> PractitionerShapeGateConfig:
        """Construct a practitioner-shape-gate config carrying the
        reference defaults for `active_checkpoints` + `per_axis_thresholds`.

        Helper for tests + minimal deployment wiring; production deployments
        SHOULD provide explicit per-axis thresholds tuned per W2 pioneer
        deployment data.
        """
        from pbs.substrate import DeploymentTier

        if not isinstance(deployment_tier, DeploymentTier):
            raise TypeError(
                f"deployment_tier must be DeploymentTier; got "
                f"{type(deployment_tier).__name__}"
            )
        return cls(
            gate_impl=GATE_IMPL_ID,
            shape_id=shape_id,
            deployment_tier=deployment_tier,
            active_checkpoints=PRACTITIONER_SHAPE_ACTIVE_CHECKPOINTS,
            per_axis_thresholds=PRACTITIONER_SHAPE_DEFAULT_THRESHOLDS,
            actor_id=actor_id,
        )


# ---------------------------------------------------------------------------
# PractitionerShapeGate — Implementation class
# ---------------------------------------------------------------------------


class PractitionerShapeGate:
    """Practitioner-shape quality-gate Implementation satisfying
    `QualityGateProtocol`.

    Per `arch/quality-gate.md` §6 tri-aspect Pattern A: this class IS the
    Implementation aspect at Framework C scope; instances bound at
    workspace boot via shape-mediated selection per §5 are the Running
    Instance aspect at Owner B (1 active gate per workspace per §9
    cardinality). Surface satisfaction is structural — instances pass
    `isinstance(gate, QualityGateProtocol)` per the `runtime_checkable`
    Protocol decorator on `pbs.quality_gate.QualityGateProtocol`.

    Per `arch/quality-gate.md` §6 gate-coupling impossible-by-construction:
    skills using only `QualityGateProtocol` methods are gate-portable
    across shape impls by construction. Phase 6 introduces a typed
    `PractitionerShapeGateExtension` Protocol exposing per-shape
    intervention mechanics specifics (engagement-procedure config;
    re-engagement nudges) accessed via isinstance gate at use site
    (parallel to substrate-extension + adapter-extension Protocols).

    Lifecycle (per `arch/quality-gate.md` §10 + `ARCHITECTURE.md` §6
    composite boot subsection — gate-phase 1-4 follows substrate-phase 5
    `boot_complete`):

    - Boot via `from_config_with_emitter(config, audit_emit, audit_query)`
      (testable production factory; Protocol-required `from_config(config)`
      works with no-op emitter + empty querier for type-conformance only)
    - Boot phases:
      - gate-phase 1: instantiate per shape policy bundle declaration
      - gate-phase 2: state-restore from audit-trail (stateful impl reads
        prior `gate_state_persisted` events via injected
        `audit_query`); emits `GateStateRestored` upon completion
      - gate-phase 3: register checkpoint-firing handlers (Phase 6 wiring
        point — reference impl records intent only)
      - gate-phase 4: emit `GateActive`; `is_ready` becomes True
    - `shutdown()` runs §10 shutdown sequence steps 1-4 (final drift
      report + state persistence + observability-hook unsubscribe + return)

    State (instance-private):

    - `_cumulative_signals`: ingested per-axis signal accumulation across
      session/work-unit context (§2.F state-management; audit-trail-as-
      state-store reframe — also persisted via `gate_state_persisted`
      events for cross-restart durability)
    - `_last_verdict`: most-recent `evaluate()` verdict
    - `_last_evaluated_at`: timestamp of last evaluation
    - `_is_ready` / `_is_shutting_down`: lifecycle flags
    - `_session_id` / `_work_unit_id`: per-construction scope identifiers
      bound at `from_config_with_emitter()`-time when supplied (else None)
      for state-restore + state-persistence scoping per §13 multi-tenant
      gate state isolation

    Audit emission (per `arch/quality-gate.md` §2.E catalog): `GateFired` /
    `GateInterventionApplied` / `GateThresholdCrossed` / `GateStatePersisted` /
    `GateStateRestored` / `GateActive` / `GateSessionSummary` emit via
    injected `audit_emit` per §8 skill-side MCP audit gate path.
    """

    def __init__(
        self,
        config: PractitionerShapeGateConfig,
        audit_emit: AuditEmitter,
        audit_query: AuditEventKindQuerier,
        session_id: str | None = None,
        work_unit_id: str | None = None,
    ) -> None:
        """Internal constructor.

        Use `from_config_with_emitter()` factory per `arch/quality-gate.md`
        §10 boot sequence; this constructor is the underlying primitive.
        """
        self._config = config
        self._audit_emit = audit_emit
        self._audit_query = audit_query
        self._instance_id: str = (
            f"{GateImplKind.PRACTITIONER_SHAPE_GATE.value}:{uuid4()}"
        )
        self._session_id: str | None = session_id
        self._work_unit_id: str | None = work_unit_id
        self._is_ready: bool = False
        self._is_shutting_down: bool = False
        self._cumulative_signals: list[GateSignal] = []
        self._last_verdict: GateVerdict | None = None
        self._last_evaluated_at: datetime | None = None

    # ------------------------------------------------------------------
    # Per-instance identity (Surface uniformity with Pattern A peers)
    # ------------------------------------------------------------------

    @property
    def gate_impl(self) -> GateImplKind:
        """Per `arch/quality-gate.md` §4."""
        return self._config.gate_impl

    @property
    def shape_id(self) -> str:
        """Per `arch/quality-gate.md` §5 shape-mediated selection."""
        return self._config.shape_id

    # ------------------------------------------------------------------
    # Lifecycle (§10 boot + shutdown — composite sequence at
    # `ARCHITECTURE.md` §6 gate-phase 1-4)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(cls, config: GateConfig) -> PractitionerShapeGate:
        """Boot per `arch/quality-gate.md` §10 boot sequence — Protocol-
        required factory.

        Type-narrowed: gate-Protocol contract takes the base `GateConfig`
        (gate-impl-neutral); this impl narrows via isinstance check +
        raises `GateUnreachable` on mismatch.

        Audit emission caveat: no `AuditEmitter` / `AuditEventKindQuerier`
        is available through the Protocol-required signature. This factory
        uses a no-op emitter + empty-result querier and emits `GateActive`
        for type-conformance only. Production callers SHOULD use
        `from_config_with_emitter()` so the audit Surface §A binding is
        real per `arch/quality-gate.md` §10 Precondition (audit-phase 1-3
        ready + substrate-phase 1-5 complete BEFORE gate-phase 1).

        Raises:
            GateUnreachable: `config` not `PractitionerShapeGateConfig`.
        """
        if not isinstance(config, PractitionerShapeGateConfig):
            raise GateUnreachable(
                f"PractitionerShapeGate requires "
                f"PractitionerShapeGateConfig; got {type(config).__name__}"
            )

        def _noop_emit(_event: AuditEventBase) -> None:
            return None

        def _empty_query(_event_kind: str) -> list[AuditEventBase]:
            return []

        instance = cls(config, audit_emit=_noop_emit, audit_query=_empty_query)
        await instance._boot()
        return instance

    @classmethod
    async def from_config_with_emitter(
        cls,
        config: PractitionerShapeGateConfig,
        audit_emit: AuditEmitter,
        audit_query: AuditEventKindQuerier,
        session_id: str | None = None,
        work_unit_id: str | None = None,
    ) -> PractitionerShapeGate:
        """Phase 6.1 testable factory honoring `arch/quality-gate.md` §10
        Precondition (audit-phase 1-3 ready + substrate-phase 1-5 complete
        BEFORE gate-phase 1) + §8 skill-side audit emission convergence.

        Production boot path; the audit Surface §A emit + §C query bindings
        must be wired before this factory fires per `ARCHITECTURE.md` §6
        composite boot subsection cross-axis composite boot integration.

        `session_id` / `work_unit_id` scope the state-restore + state-
        persistence per §13 multi-tenant gate state isolation; supply at
        boot when a workspace already has a known session/work-unit
        context; otherwise leave None (gate operates in workspace-global
        scope).
        """
        instance = cls(
            config,
            audit_emit,
            audit_query,
            session_id=session_id,
            work_unit_id=work_unit_id,
        )
        await instance._boot()
        return instance

    async def _boot(self) -> None:
        """Internal boot — composite sequence gate-phase 1-4 implementation
        per `arch/quality-gate.md` §10 boot sequence.

        - gate-phase 1: instance constructed (caller already invoked
          constructor); validate per-axis thresholds against impl's
          per-axis signal-kind catalog (basic structural check; full
          per-axis signal-kind catalog finalization per W2)
        - gate-phase 2: state-restore from audit-trail via injected
          `audit_query` (stateful impl per `PractitionerShapeGateConfig.
          stateful = True`); reconstructs cumulative engagement signals
          across session/work-unit context; emits `GateStateRestored`
        - gate-phase 3: register checkpoint-firing handlers — Phase 6
          wiring point (reference impl records intent via audit emission
          shape only; real subscription to substrate Surface §B telemetry
          hooks + audit Surface §C query subscriptions + sparring sub-
          mechanism event-emission subscriptions per `arch/sparring.md`
          §4 deferred to deployment-instance wiring)
        - gate-phase 4: emit `GateActive`; `_is_ready` becomes True
        """
        self._validate_thresholds()
        await self._restore_state()
        # gate-phase 3 (observability-hook subscriptions): Phase 6 wiring
        # point — reference impl records intent only via the GateActive
        # emission below; real subscription happens at deployment-instance
        # wiring per arch/quality-gate.md §15 pre-implementation operational
        # concerns.
        self._is_ready = True
        self._audit_emit(
            GateActive(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                session_id=self._session_id,
                work_unit_id=self._work_unit_id,
                details={
                    "gate_impl": self._config.gate_impl.value,
                    "shape_id": self._config.shape_id,
                    "active_checkpoints": sorted(
                        c.value for c in self._config.active_checkpoints
                    ),
                },
            )
        )

    def _validate_thresholds(self) -> None:
        """Per `arch/quality-gate.md` §5 validation at workspace boot:
        'Shape policy bundle's per-axis threshold-set declarations validate
        against gate-impl's per-axis signal-kind catalog.'

        Reference impl performs basic structural check (per-axis-threshold
        keys are non-empty strings; values are float-castable). Full per-
        axis signal-kind catalog per W2 (Phase 1+ pioneer deployment data).

        Raises:
            SignalEvaluationFailure: per-shape threshold-set declaration
                ill-formed.
        """
        for axis_kind, thresholds in self._config.per_axis_thresholds.items():
            for signal_kind, value in thresholds.items():
                if not signal_kind:
                    raise SignalEvaluationFailure(
                        f"Empty signal_kind in per_axis_thresholds for "
                        f"{axis_kind.value}."
                    )
                if not isinstance(value, (int, float)):
                    raise SignalEvaluationFailure(
                        f"Non-numeric threshold for {axis_kind.value}/"
                        f"{signal_kind}: {value!r}"
                    )

    async def _restore_state(self) -> None:
        """Per `arch/quality-gate.md` §10 boot phase 2 + §2.F audit-trail-
        as-state-store reframe.

        Reads prior `gate_state_persisted` events via injected `audit_query`;
        reconstructs `_cumulative_signals` from the most-recent persisted
        snapshot scoped to `session_id` / `work_unit_id`. Emits
        `GateStateRestored` upon completion.

        Raises:
            GateStateRestoreFailure: audit-trail integrity violation;
                state reconstruction failure (per-shape continuation
                semantics — practitioner-shape fail-closed per §11 +
                §14 row 4).
        """
        try:
            events = self._audit_query("gate_state_persisted")
        except Exception as exc:  # noqa: BLE001
            raise GateStateRestoreFailure(
                f"Audit-trail query failed during gate state-restore: {exc}"
            ) from exc

        scoped = [
            e
            for e in events
            if (self._session_id is None or e.session_id == self._session_id)
            and (
                self._work_unit_id is None
                or e.work_unit_id == self._work_unit_id
            )
        ]
        if scoped:
            # Most-recent persisted snapshot wins (events are append-only
            # per audit Surface §B; ordering by timestamp ascending).
            snapshot = max(scoped, key=lambda e: e.timestamp)
            cumulative_raw = snapshot.details.get("cumulative_signals", [])
            try:
                self._cumulative_signals = [
                    GateSignal.model_validate(raw) for raw in cumulative_raw
                ]
            except Exception as exc:  # noqa: BLE001
                raise GateStateRestoreFailure(
                    f"gate_state_persisted snapshot has malformed "
                    f"cumulative_signals: {exc}"
                ) from exc

        self._audit_emit(
            GateStateRestored(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                session_id=self._session_id,
                work_unit_id=self._work_unit_id,
                details={
                    "restored_signal_count": len(self._cumulative_signals),
                },
            )
        )

    @property
    def is_ready(self) -> bool:
        """Per `arch/quality-gate.md` §10 boot phase 4. Once True, `fire()`
        accepts per-checkpoint events. Becomes False at shutdown step 4."""
        return self._is_ready and not self._is_shutting_down

    async def shutdown(self) -> None:
        """Per `arch/quality-gate.md` §10 shutdown sequence steps 1-4.

        Per `ARCHITECTURE.md` §6 invariant: gate state events are persisted
        in audit-trail BEFORE workspace shutdown completes (gate-shutdown
        2 `gate_state_persisted` flush → audit storage realization shutdown
        LAST per `arch/audit.md` §10 shutdown step 4-7).

        Steps:

        1. Emit final drift report event (`GateSessionSummary`) — per-impl
           shape carries cumulative-signal summary
        2. Gate state persistence — flush cumulative signals via
           `GateStatePersisted` event emission (preserves cross-deployment
           portability per audit-trail composition + W3)
        3. Gate unsubscribes from observability hooks — Phase 6 wiring
           point (reference impl has no live subscriptions to release)
        4. Gate shutdown returns; audit storage realization shutdown
           follows per `arch/audit.md` §10 shutdown steps 4-7

        Idempotent: repeated calls return without re-emitting events.
        """
        if self._is_shutting_down:
            return
        self._is_shutting_down = True

        # Step 1: emit final drift report event.
        self._audit_emit(
            GateSessionSummary(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                session_id=self._session_id,
                work_unit_id=self._work_unit_id,
                details={
                    "cumulative_signal_count": len(self._cumulative_signals),
                    "last_verdict": (
                        self._last_verdict.value
                        if self._last_verdict is not None
                        else None
                    ),
                    "last_evaluated_at": (
                        self._last_evaluated_at.isoformat()
                        if self._last_evaluated_at is not None
                        else None
                    ),
                },
            )
        )

        # Step 2: gate state persistence (skip emission if no cumulative
        # state — empty state has nothing to preserve, and an empty
        # GateStatePersisted would carry no signal). Practitioner-shape is
        # stateful per §14 row 5; persistence runs on every shutdown that
        # accumulated signals.
        if self._cumulative_signals:
            self._audit_emit(
                GateStatePersisted(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id,
                    timestamp=datetime.now(tz=UTC),
                    session_id=self._session_id,
                    work_unit_id=self._work_unit_id,
                    details={
                        "cumulative_signals": [
                            s.model_dump(mode="json")
                            for s in self._cumulative_signals
                        ],
                    },
                )
            )

        # Step 3: unsubscribe from observability hooks — Phase 6 wiring
        # point; no live subscriptions in reference impl.

        # Step 4: shutdown returns.
        self._is_ready = False

    # ------------------------------------------------------------------
    # §A Checkpoint firing API
    # ------------------------------------------------------------------

    async def fire(
        self,
        checkpoint_kind: CheckpointKind,
        context: GateContext,
    ) -> GateDecision:
        """Per `arch/quality-gate.md` §2.A.

        Composite operation: evaluates accumulated signals (§C); decides
        intervention kind per per-shape policy (`fail_closed = True` →
        `WARN` issues `nudge`; `FAIL` issues `block` for axis-3 mandatory
        kinds + `friction` otherwise); dispatches via `intervene()`; emits
        `GateFired` audit event with verdict.

        Per `arch/quality-gate.md` §14 row 1 practitioner-shape column,
        only `pre_send` / `pre_claim_finalization` / `per_edit` /
        `drift_audit` checkpoints are active for this impl. Inactive
        checkpoint-kinds return a `PASS` decision with
        `intervention_kind=AUDIT_ONLY` and emit `GateFired` for visibility
        without firing intervention mechanics.

        Raises:
            GateUnreachable: gate not ready.
            SignalEvaluationFailure: per-shape threshold-set ill-formed;
                signal-set incomplete for evaluation.
            InterventionDispatchFailure: intervention mechanics failure.
            EventEmissionFailure: gate-fired event emission failure.
        """
        if not self.is_ready:
            raise GateUnreachable(
                f"PractitionerShapeGate {self._instance_id} not ready; "
                f"cannot fire at checkpoint '{checkpoint_kind.value}'."
            )

        if checkpoint_kind not in self._config.active_checkpoints:
            decision = GateDecision(
                checkpoint_kind=checkpoint_kind,
                verdict=GateVerdict.PASS,
                intervention_kind=InterventionKind.AUDIT_ONLY,
                reason=(
                    f"checkpoint '{checkpoint_kind.value}' not active for "
                    f"shape '{self._config.shape_id}'; pass-through."
                ),
                triggering_signals=[],
            )
            self._emit_gate_fired(decision, context)
            return decision

        verdict = self.evaluate(checkpoint_kind, list(self._cumulative_signals))
        triggering = self._signals_above_threshold()
        intervention = self._select_intervention(verdict, triggering)
        reason = self._format_reason(checkpoint_kind, verdict, triggering)

        decision = GateDecision(
            checkpoint_kind=checkpoint_kind,
            verdict=verdict,
            intervention_kind=intervention,
            reason=reason,
            triggering_signals=triggering,
        )

        if intervention is not InterventionKind.AUDIT_ONLY:
            await self.intervene(decision, context)

        self._emit_gate_fired(decision, context)
        return decision

    def _emit_gate_fired(
        self, decision: GateDecision, context: GateContext
    ) -> None:
        """Emit `GateFired` for the given decision per `arch/quality-gate.md`
        §2.E + §8 skill-side audit emission.

        Raises:
            EventEmissionFailure: emission via injected emitter failed.
        """
        try:
            self._audit_emit(
                GateFired(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id,
                    timestamp=datetime.now(tz=UTC),
                    session_id=context.session_id or self._session_id,
                    work_unit_id=context.work_unit_id or self._work_unit_id,
                    claim_id=context.claim_id,
                    workflow_instance_id=context.workflow_instance_id,
                    details={
                        "checkpoint_kind": decision.checkpoint_kind.value,
                        "verdict": decision.verdict.value,
                        "intervention_kind": decision.intervention_kind.value,
                        "reason": decision.reason,
                        "triggering_signal_count": len(
                            decision.triggering_signals
                        ),
                    },
                )
            )
        except Exception as exc:  # noqa: BLE001
            raise EventEmissionFailure(
                f"GateFired emission failed: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # §B Per-axis signal ingestion
    # ------------------------------------------------------------------

    def ingest_signal(self, signal: GateSignal) -> None:
        """Per `arch/quality-gate.md` §2.B.

        Practitioner-shape is stateful per §14 row 5: signals accumulate
        in `_cumulative_signals` for cross-checkpoint cumulative
        observability per the cross-axis failure cascade pattern
        (`arch/axis-interactions.md` §3.4).

        Emits `GateThresholdCrossed` when ingested signal value crosses
        per-axis threshold (pre-intervention drift visibility) per §2.E.
        """
        self._cumulative_signals.append(signal)
        threshold = self._threshold_for(signal)
        if threshold is not None and signal.value >= threshold:
            self._audit_emit(
                GateThresholdCrossed(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id,
                    timestamp=datetime.now(tz=UTC),
                    session_id=self._session_id,
                    work_unit_id=self._work_unit_id,
                    details={
                        "axis_kind": signal.axis_kind.value,
                        "signal_kind": signal.signal_kind,
                        "value": signal.value,
                        "threshold": threshold,
                        "severity": signal.severity.value,
                        "source_event_ref": signal.source_event_ref,
                    },
                )
            )

    def _threshold_for(self, signal: GateSignal) -> float | None:
        """Resolve per-axis threshold for the given signal; None when
        the per-shape policy declares no threshold for this signal-kind
        (Phase 6 spec lands the full per-axis signal-kind catalog per W2)."""
        per_axis = self._config.per_axis_thresholds.get(signal.axis_kind, {})
        return per_axis.get(signal.signal_kind)

    # ------------------------------------------------------------------
    # §C Signal evaluation
    # ------------------------------------------------------------------

    def evaluate(
        self,
        checkpoint_kind: CheckpointKind,
        signal_set: list[GateSignal],
    ) -> GateVerdict:
        """Per `arch/quality-gate.md` §2.C.

        Cumulative observability across axes — single evaluation point
        ingesting per-axis signals into one cumulative state per the
        cross-axis failure cascade pattern requirement (`arch/axis-
        interactions.md` §3.4).

        Verdict logic (practitioner-shape; defensibility-critical):

        - Any signal with `severity = CRITICAL` → `FAIL`
        - Any signal at-or-above declared per-axis threshold AND severity
          ∈ {`HIGH`, `CRITICAL`} → `FAIL`
        - Any signal at-or-above declared per-axis threshold (lower
          severity) → `WARN`
        - Otherwise → `PASS`

        Per `arch/quality-gate.md` §14 row 2 practitioner-shape strict
        per-axis (axis-3 PRIMARY): `axis_3_authorship_preservation` signals
        flagged at any severity above-threshold escalate to `FAIL` (rubber-
        stamping detection mandatory per `glossary/rubber-stamping.md`).

        Raises:
            SignalEvaluationFailure: signal_set ill-formed (caught at
                threshold validation in `_boot()` for the per-shape
                threshold-set; for per-checkpoint signal-set caller-
                supplied issues, the verdict path treats unknown signal
                kinds as PASS — Phase 6 spec tightens this per W2).
        """
        verdict: GateVerdict = GateVerdict.PASS
        for signal in signal_set:
            threshold = self._threshold_for(signal)
            crossed = threshold is not None and signal.value >= threshold

            if signal.severity is SignalSeverity.CRITICAL:
                verdict = GateVerdict.FAIL
                continue

            if crossed and signal.axis_kind is AxisKind.AXIS_3_AUTHORSHIP_PRESERVATION:
                # Axis-3 PRIMARY for practitioner-shape per §14 row 2.
                verdict = GateVerdict.FAIL
                continue

            if crossed and signal.severity in (
                SignalSeverity.HIGH,
                SignalSeverity.CRITICAL,
            ):
                verdict = GateVerdict.FAIL
                continue

            if crossed and verdict is GateVerdict.PASS:
                verdict = GateVerdict.WARN

        self._last_verdict = verdict
        self._last_evaluated_at = datetime.now(tz=UTC)
        return verdict

    def _signals_above_threshold(self) -> list[GateSignal]:
        """Return cumulative signals at-or-above declared per-axis thresholds
        (used as `GateDecision.triggering_signals`)."""
        triggering: list[GateSignal] = []
        for signal in self._cumulative_signals:
            threshold = self._threshold_for(signal)
            if threshold is not None and signal.value >= threshold:
                triggering.append(signal)
            elif signal.severity is SignalSeverity.CRITICAL:
                triggering.append(signal)
        return triggering

    def _select_intervention(
        self,
        verdict: GateVerdict,
        triggering: list[GateSignal],
    ) -> InterventionKind:
        """Per `arch/quality-gate.md` §14 row 3 practitioner-shape
        intervention mechanics: friction + nudge + block + practitioner
        attestation + re-engagement.

        Mapping (Phase 6.1 reference):

        - `PASS` → `AUDIT_ONLY`
        - `WARN` → `NUDGE` (drift signal present; advisory)
        - `FAIL` with axis-3 triggering signal → `BLOCK` (defensibility-
          critical; HITL approval via substrate Surface §C
          `request_permission` per §2.D)
        - `FAIL` without axis-3 triggering signal → `FRICTION` (axis-1 or
          axis-2 failure; surface friction; allow practitioner override)
        """
        if verdict is GateVerdict.PASS:
            return InterventionKind.AUDIT_ONLY
        if verdict is GateVerdict.WARN:
            return InterventionKind.NUDGE
        # FAIL: axis-3 triggers BLOCK; otherwise FRICTION.
        for signal in triggering:
            if signal.axis_kind is AxisKind.AXIS_3_AUTHORSHIP_PRESERVATION:
                return InterventionKind.BLOCK
        return InterventionKind.FRICTION

    @staticmethod
    def _format_reason(
        checkpoint_kind: CheckpointKind,
        verdict: GateVerdict,
        triggering: list[GateSignal],
    ) -> str:
        """Compose human-readable reason for the `GateDecision`. Captured
        in `GateInterventionApplied.details` for L8 auditor reasoning-chain
        reconstruction per `arch/quality-gate.md` §2.D."""
        if not triggering:
            return (
                f"checkpoint '{checkpoint_kind.value}' verdict "
                f"'{verdict.value}' — no triggering signals."
            )
        rendered = ", ".join(
            f"{s.axis_kind.value}/{s.signal_kind}={s.value}"
            for s in triggering
        )
        return (
            f"checkpoint '{checkpoint_kind.value}' verdict "
            f"'{verdict.value}' — triggering signals: {rendered}"
        )

    # ------------------------------------------------------------------
    # §D Intervention dispatch
    # ------------------------------------------------------------------

    async def intervene(
        self,
        decision: GateDecision,
        context: GateContext,
    ) -> None:
        """Per `arch/quality-gate.md` §2.D.

        Authority-binding records `actor_kind: ai_runtime` per
        `glossary/authority-binding.md` (gate is AI-runtime actor at
        intervention emission). Composes with substrate
        `PermissionDecisionEvent` for `BLOCK` interventions (substrate-side
        authority-bound denial flow at `request_permission`).

        Phase 6 wiring point (per `arch/quality-gate.md` §15 pre-
        implementation operational concerns): real intervention mechanics
        — friction display; nudge delivery; block enforcement via substrate
        Surface §C `request_permission`; practitioner attestation; re-
        engagement nudges. Reference impl emits `GateInterventionApplied`
        with the decision shape; concrete delivery + HITL approval flow
        deliver at deployment-instance wiring.

        Raises:
            InterventionDispatchFailure: intervention mechanics failure.
            EventEmissionFailure: emission of `GateInterventionApplied`
                failed.
        """
        try:
            self._audit_emit(
                GateInterventionApplied(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id,
                    timestamp=datetime.now(tz=UTC),
                    session_id=context.session_id or self._session_id,
                    work_unit_id=context.work_unit_id or self._work_unit_id,
                    claim_id=context.claim_id,
                    workflow_instance_id=context.workflow_instance_id,
                    details={
                        "intervention_kind": decision.intervention_kind.value,
                        "verdict": decision.verdict.value,
                        "checkpoint_kind": decision.checkpoint_kind.value,
                        "reason": decision.reason,
                        "triggering_signal_count": len(
                            decision.triggering_signals
                        ),
                        # `BLOCK` requires substrate Surface §C
                        # `request_permission` follow-up per §2.D; reference
                        # impl marks the intent on the event so deployment-
                        # instance wiring can route accordingly.
                        "requires_substrate_permission": (
                            decision.intervention_kind
                            is InterventionKind.BLOCK
                        ),
                    },
                )
            )
        except Exception as exc:  # noqa: BLE001
            raise EventEmissionFailure(
                f"GateInterventionApplied emission failed: {exc}"
            ) from exc

        if decision.intervention_kind is InterventionKind.BLOCK:
            # Phase 6 wiring point: invoke substrate Surface §C
            # `request_permission` for HITL approval. Reference impl
            # records intent via the audit emission above; concrete
            # delivery happens at deployment-instance wiring per
            # `arch/quality-gate.md` §15.
            return
        if decision.intervention_kind in (
            InterventionKind.FRICTION,
            InterventionKind.NUDGE,
        ):
            # Phase 6 wiring point: friction display / nudge delivery via
            # substrate-mediated UI surface. Reference impl records intent
            # via the audit emission above; concrete delivery at deployment-
            # instance wiring.
            return
        if decision.intervention_kind is InterventionKind.AUDIT_ONLY:
            return
        # Defensive: per-shape error semantics fail-closed (§11 + §14 row
        # 4) — unknown intervention kinds must surface, not silently pass.
        raise InterventionDispatchFailure(
            f"Unknown intervention_kind '{decision.intervention_kind}' for "
            f"practitioner-shape-gate; fail-closed per §11."
        )

    # ------------------------------------------------------------------
    # §F State management (audit-trail-as-state-store reframe)
    # ------------------------------------------------------------------

    def get_state(
        self,
        session_id: str | None = None,
        work_unit_id: str | None = None,
    ) -> GateState:
        """Per `arch/quality-gate.md` §2.F.

        Reads via injected `audit_query` (audit Surface §C `query_per_event_kind`)
        filtering by `gate_state_persisted` events for the given
        session/work-unit context. Practitioner-shape is stateful per §14
        row 5 — populates `cumulative_signals` from in-memory accumulation
        when the requested scope matches the gate's bound scope; otherwise
        re-reads from the audit-trail.

        Per audit-trail-as-state-store reframe: state IS the rendered view
        of `gate_state_persisted` event sequence per the same pattern as
        workspace state rendered from event-stream per `arch/audit.md` §F.

        Raises:
            GateStateRestoreFailure: audit-trail integrity violation;
                state reconstruction failure.
        """
        # In-memory fast path when the requested scope matches this gate
        # Instance's bound scope.
        scope_matches = (
            (session_id is None or session_id == self._session_id)
            and (work_unit_id is None or work_unit_id == self._work_unit_id)
        )
        if scope_matches:
            return GateState(
                session_id=self._session_id,
                work_unit_id=self._work_unit_id,
                cumulative_signals=list(self._cumulative_signals),
                last_verdict=self._last_verdict,
                last_evaluated_at=self._last_evaluated_at,
            )

        # Cross-scope: re-read from audit-trail.
        try:
            events = self._audit_query("gate_state_persisted")
        except Exception as exc:  # noqa: BLE001
            raise GateStateRestoreFailure(
                f"Audit-trail query failed during get_state: {exc}"
            ) from exc

        scoped = [
            e
            for e in events
            if (session_id is None or e.session_id == session_id)
            and (work_unit_id is None or e.work_unit_id == work_unit_id)
        ]
        if not scoped:
            return GateState(
                session_id=session_id,
                work_unit_id=work_unit_id,
            )
        snapshot = max(scoped, key=lambda e: e.timestamp)
        try:
            cumulative = [
                GateSignal.model_validate(raw)
                for raw in snapshot.details.get("cumulative_signals", [])
            ]
        except Exception as exc:  # noqa: BLE001
            raise GateStateRestoreFailure(
                f"gate_state_persisted snapshot has malformed "
                f"cumulative_signals: {exc}"
            ) from exc
        return GateState(
            session_id=session_id,
            work_unit_id=work_unit_id,
            cumulative_signals=cumulative,
        )

    def set_state(self, state: GateState) -> None:
        """Per `arch/quality-gate.md` §2.F.

        IS `gate_state_persisted` event emission via audit Surface §A.
        Audit-trail IS state-store: NO separate gate-state-store. Avoids
        dual-store divergence; preserves single-write architecture per
        `arch/audit.md` §10 audit-trail-as-canonical-source.

        Aligns the gate's in-memory `_cumulative_signals` with the
        provided `state` so subsequent `evaluate()` / `fire()` operate on
        the persisted shape (consistent with audit-trail-as-state-store
        reframe — events ARE the source of truth, in-memory mirrors the
        latest rendered view).

        Raises:
            EventEmissionFailure: `gate_state_persisted` emission failed
                (composes with audit Surface §11 error categories).
        """
        try:
            self._audit_emit(
                GateStatePersisted(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._instance_id,
                    timestamp=datetime.now(tz=UTC),
                    session_id=state.session_id or self._session_id,
                    work_unit_id=state.work_unit_id or self._work_unit_id,
                    details={
                        "cumulative_signals": [
                            s.model_dump(mode="json")
                            for s in state.cumulative_signals
                        ],
                        "last_verdict": (
                            state.last_verdict.value
                            if state.last_verdict is not None
                            else None
                        ),
                        "last_evaluated_at": (
                            state.last_evaluated_at.isoformat()
                            if state.last_evaluated_at is not None
                            else None
                        ),
                    },
                )
            )
        except Exception as exc:  # noqa: BLE001
            raise EventEmissionFailure(
                f"GateStatePersisted emission failed: {exc}"
            ) from exc

        # Mirror in-memory to the persisted shape when the state's scope
        # matches this gate Instance's bound scope.
        scope_matches = (
            (state.session_id is None or state.session_id == self._session_id)
            and (
                state.work_unit_id is None
                or state.work_unit_id == self._work_unit_id
            )
        )
        if scope_matches:
            self._cumulative_signals = list(state.cumulative_signals)
            self._last_verdict = state.last_verdict
            self._last_evaluated_at = state.last_evaluated_at
