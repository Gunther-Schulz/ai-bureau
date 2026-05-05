"""Practitioner-shape sparring mechanism class — Phase 6.1 reference impl.

Per `arch/sparring.md` §6 mechanism-class structural reconciliation: the
Sparring class is the architectural-conceptual aggregation of 8 sub-mechanism
Surfaces (each its own atomic interface contract per §2). Per §1 + §6: NOT
Pattern A — there are no whole-class alternative architectures that swap in/
out per workspace; sub-mechanism realization variation is per-sub-mechanism,
parameterized by per-shape policy (activation matrix + thresholds + retry
budget).

This module realizes the **practitioner-shape policy bundle** for the
8-sub-mechanism Sparring class: 8 sub-mechanism impl classes (4
architecturally-encoded + 4 behaviorally-enforced) + 1 aggregating
`PractitionerShapeSparring` class satisfying `SparringProtocol`.

Surface satisfaction (`pbs.sparring.SparringProtocol`):

- §A `counter_argument` / §B `confidence_calibration` / §C
  `visible_reasoning` / §D `selective_friction` (architecturally-encoded
  sub-Protocols 1-4)
- §E `anti_sycophancy` / §F `asymmetric_knowledge_respect` / §G
  `commit_to_recommendations` / §H `whats_missing_checkpoint`
  (behaviorally-enforced sub-Protocols 5-8)
- `from_shape_policy()` async factory matching the Phase 6.1 mechanism-impl
  factory convention (audit / gate / authority-binding precedent)
- `is_ready` / `shutdown()` lifecycle uniformity with mechanism-class peers
  (audit / quality-gate)
- `run_round()` orchestrator aggregating per-active-sub-mechanism
  validation + emission per activation matrix; retry-on-fail + bypass-with-
  reason path per `arch/sparring.md` §11 + §14 fail-closed practitioner-
  shape error semantics
- `report_failure_mode()` axis-2 failure-mode emission feeding quality-gate
  axis-2 enforcement per `arch/quality-gate.md` §2.B per-axis signal
  ingestion

Audit emission discipline (per `arch/sparring.md` §8): sparring sub-
mechanisms run within skill execution; emit skill-side via MCP audit gate
ONLY (parallel to adapter §8 + quality-gate §8). Phase 6.1 collapses the
skill-side MCP audit gate path to a directly-injected `AuditEmitter`
callable matching substrate's emitter shape per the Note 75-79 thin-slice
convention; Phase 6.2 wires the actual MCP audit gate routing sparring
emissions through the gate's MCP `record_audit_event` tool to the audit
storage realization.

Phase 6.1 thin-slice scope per `BACKLOG.md` §224: practitioner-shape only
(activation matrix all 8 active per §14 practitioner-shape profile; fail-
closed; ≥1 sparring-event per claim mandatory; retry budget 3). Autonomous-
business-shape + personal-OS-shape sparring impls deferred to Phase 6.2 per
W3 second-shape productization watch-list.

Per-sub-mechanism realization details (`arch/sparring.md` §15 pre-
implementation operational concerns; reference-impl values; concrete tuning
per W2 pioneer deployment data):

- Counter-argument min content length: 20 chars (substantive engagement vs
  one-liner)
- Confidence-calibration basis min length: 10 chars
- Visible-reasoning chain-of-inference min length: 30 chars
- Selective-friction threshold semantics: `substantive` → 0.5 ambiguity
  score (medium-or-higher per §14 practitioner-shape profile);
  `low` → 0.2; `high` → 0.7
- Anti-sycophancy heuristic: keyword-based soften-without-evidence pattern
  detection over current-vs-prior output; threshold 0.0 disabled, >0
  enables (Phase 6.2 tunes per W2 false-positive friction-budget watch-
  list)
- Failure-mode classification: clustered architecturally-encoded sub-
  mechanism FAILs over a sparring round map to FailureMode per impl-level
  convention; reference impl uses simple count-based mapping (Phase 6.2
  refines per `arch/sparring.md` §15 failure-mode detection thresholds)

Per `arch/sparring.md` §10 + `ARCHITECTURE.md` §6 composite boot subsection:
audit-phase 1-3 ready BEFORE this mechanism is constructed (the orchestrator
emits sparring events through the injected `emitter`). Substrate-phase
1-5 may proceed in parallel; sparring sub-mechanism schema registration
via substrate Surface §D happens at substrate boot per substrate topic
§10 — NOT in this impl's lifecycle.

Phase 6 wiring points (marked explicitly):

- Substrate Surface §D structured output validation: Phase 6.1 collapses
  the substrate-side schema-validation auto-retry path to in-impl
  validation — `validate()` raises `SparringValidationError` on missing/
  invalid; orchestrator reproduces the auto-retry pattern for this thin-
  slice. Phase 6.2 wires the actual substrate Surface §D registration
  per skill output-schema declaration so the substrate's structured
  output validation auto-retry handles the architecturally-encoded sub-
  mechanism enforcement (per `arch/sparring.md` §4 architecturally-encoded
  realization via substrate Surface §D)
- Quality-gate axis-2 signal ingestion: Phase 6.1 emits the failure-mode
  events (`AnswerMachineDetected` / `OracleModeDetected` /
  `ValidatorModeDetected`) via the injected `emitter`; Phase 6.2 wires
  the actual quality-gate `ingest_signal()` callback subscription per
  `arch/quality-gate.md` §2.B
- Heuristic-detection state for anti-sycophancy: Phase 6.1 reference
  impl is stateless (current-vs-prior comparison only); Phase 6.2 W2
  watch-list tunes per false-positive friction-budget data — possibly
  cross-claim heuristic state per `arch/sparring.md` §9 mutability
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

from pbs.sparring import (
    AnswerMachineDetected,
    AntiSycophancyFlagRaised,
    AntiSycophancySubMechanism,
    AsymmetricKnowledgeRespected,
    AsymmetricKnowledgeRespectSubMechanism,
    CommitToRecommendationsSubMechanism,
    ConfidenceCalibrated,
    ConfidenceCalibrationSubMechanism,
    ConfidenceDeclaration,
    ConfidenceLevel,
    ConfidenceMissing,
    CounterArgument,
    CounterArgumentMissing,
    CounterArgumentProduced,
    CounterArgumentSubMechanism,
    FailureMode,
    OracleModeDetected,
    RecommendationCommitted,
    SelectiveFrictionApplied,
    SelectiveFrictionDecision,
    SelectiveFrictionSkipped,
    SelectiveFrictionSubMechanism,
    SparringBypassWithReason,
    SparringPolicy,
    SparringPolicyError,
    SparringRetryExhaustedError,
    SparringRoundCompleted,
    SparringRoundResult,
    SparringValidationError,
    SparringValidationRetry,
    SubMechanismKind,
    ValidatorModeDetected,
    VisibleReasoning,
    VisibleReasoningMissing,
    VisibleReasoningProvided,
    VisibleReasoningSubMechanism,
    WhatsMissingChecked,
    WhatsMissingCheckpointSubMechanism,
)
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Sparring identity + audit-binding type alias
# ---------------------------------------------------------------------------


SPARRING_IMPL_ID: str = "practitioner_shape_sparring"
"""Sparring class Implementation identity for audit-trail attribution.

Sparring is NOT Pattern A per `arch/sparring.md` §6 — the Surface itself
does not introduce a `SparringImplKind` enum (sub-mechanism realization is
per-sub-mechanism, not per-class). This identity string identifies the
practitioner-shape impl in audit-event `actor_id` for cross-deployment
audit-trail reasoning-chain reconstruction per `arch/audit.md` §2.C
per-actor query."""


AuditEmitter = Callable[[AuditEventBase], None]
"""Audit Surface §A emit binding per `arch/sparring.md` §8 skill-side MCP
audit gate path. Injected at construction; the callable shape matches
substrate's `AuditEmitter` for single-process Phase 6.1 deployment
(parallel to gate / authority-binding impl emitter convention).

Phase 6.2 wires the actual MCP audit gate (registered by substrate per
`arch/substrate.md` §8) routing sparring emissions through the gate's MCP
`record_audit_event` tool to the audit storage realization."""


# ---------------------------------------------------------------------------
# Practitioner-shape default thresholds + activation matrix
# ---------------------------------------------------------------------------


PRACTITIONER_SHAPE_ACTIVE_SUB_MECHANISMS: frozenset[SubMechanismKind] = frozenset(
    {
        SubMechanismKind.COUNTER_ARGUMENT,
        SubMechanismKind.CONFIDENCE_CALIBRATION,
        SubMechanismKind.VISIBLE_REASONING,
        SubMechanismKind.SELECTIVE_FRICTION,
        SubMechanismKind.ANTI_SYCOPHANCY,
        SubMechanismKind.ASYMMETRIC_KNOWLEDGE_RESPECT,
        SubMechanismKind.COMMIT_TO_RECOMMENDATIONS,
        SubMechanismKind.WHATS_MISSING_CHECKPOINT,
    }
)
"""Per `arch/sparring.md` §14 practitioner-shape profile: all 8 sub-
mechanisms active (axis-2 critical for defensibility; ≥1 sparring-event
per claim mandatory)."""


COUNTER_ARGUMENT_MIN_CONTENT_LENGTH: int = 20
"""Counter-argument min content length per `arch/sparring.md` §15 pre-
implementation operational concerns. Reference value enforces substantive
engagement vs one-liner. Phase 6.2 may tune per pioneer deployment data."""


CONFIDENCE_BASIS_MIN_LENGTH: int = 10
"""Confidence-basis min length per `arch/sparring.md` §15. Reference value
enforces non-empty rationale beyond "high" / "medium" / "low" alone."""


VISIBLE_REASONING_MIN_LENGTH: int = 30
"""Visible-reasoning chain-of-inference min length per `arch/sparring.md`
§15. Reference value enforces multi-step reasoning vs verdict alone."""


SELECTIVE_FRICTION_THRESHOLD_BANDS: dict[str, float] = {
    "low": 0.2,
    "substantive": 0.5,
    "high": 0.7,
}
"""Per `arch/sparring.md` §14 practitioner-shape profile: `substantive`
threshold (medium-or-higher claim ambiguity triggers). Mapped to numeric
ambiguity-score band per `SparringPolicy.selective_friction_threshold`
semantics; impl applies threshold uniformly per §2.D architectural
commitment."""


ANTI_SYCOPHANCY_KEYWORDS: tuple[str, ...] = (
    "you make a good point",
    "you might be right",
    "i should reconsider",
    "i agree with you",
    "you're correct",
    "actually, i was wrong",
    "let me reconsider",
    "fair point",
)
"""Reference-impl keyword set for anti-sycophancy heuristic per
`arch/sparring.md` §2.E + §15. Phase 6.2 tunes per W2 false-positive
friction-budget watch-list — keyword-based detection is a simple Phase
6.1 stand-in for richer heuristic detection (semantic similarity over
current-vs-prior output; LLM-prompted classifier; etc.)."""


FAILURE_MODE_VIOLATION_THRESHOLD: int = 3
"""Reference-impl threshold for clustered architecturally-encoded sub-
mechanism failures triggering failure-mode classification per
`arch/sparring.md` §8 axis-2 failure-mode detection events. Phase 6.2
refines per `arch/sparring.md` §15 failure-mode detection thresholds."""


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class PractitionerShapeSparringConfig(BaseModel):
    """Per-shape config bundle for the practitioner-shape sparring class.

    Per `arch/sparring.md` §5 + §14 + `glossary/shape.md`: per-shape policy
    parameterizes the framework-mechanism Surface; this config carries the
    practitioner-shape declarations.

    Loaded via active shape's policy bundle at workspace boot per
    `arch/sparring.md` §10 composition with substrate boot.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    actor_id: str
    """Sparring Running Instance identity per `arch/audit.md` §2.A actor_id
    + `arch/sparring.md` §7 composition with `actor`. AI_RUNTIME actor per
    cross-archetype convention (sparring partner is the AI runtime;
    practitioner is the engagement subject). Used as `actor_id` on every
    sparring event emission."""


# ---------------------------------------------------------------------------
# Sub-mechanism impl classes — architecturally-encoded (1-4)
# ---------------------------------------------------------------------------


class _PractitionerShapeCounterArgument:
    """Architecturally-encoded sub-mechanism A impl per `arch/sparring.md` §2.A.

    Validates sparring-mode skill output declares a counter-argument with
    substantive content (min `COUNTER_ARGUMENT_MIN_CONTENT_LENGTH` chars).
    Output may be a `CounterArgument` instance directly OR a dict with
    `counter_argument` key (str or dict mappable to `CounterArgument`).
    """

    def validate(self, output: Any, claim_id: str) -> CounterArgument:
        if isinstance(output, CounterArgument):
            payload = output
        elif isinstance(output, dict):
            raw = output.get("counter_argument")
            if raw is None:
                raise SparringValidationError(
                    f"counter_argument missing in sparring-mode output for "
                    f"claim_id={claim_id!r}"
                )
            if isinstance(raw, CounterArgument):
                payload = raw
            elif isinstance(raw, str):
                payload = CounterArgument(content=raw, targets_claim_id=claim_id)
            elif isinstance(raw, dict):
                payload = CounterArgument(
                    content=raw.get("content", ""),
                    targets_claim_id=raw.get("targets_claim_id", claim_id),
                )
            else:
                raise SparringValidationError(
                    f"counter_argument has unsupported type {type(raw).__name__} "
                    f"for claim_id={claim_id!r}"
                )
        else:
            raise SparringValidationError(
                f"sparring-mode output must be CounterArgument | dict; got "
                f"{type(output).__name__} for claim_id={claim_id!r}"
            )
        if len(payload.content) < COUNTER_ARGUMENT_MIN_CONTENT_LENGTH:
            raise SparringValidationError(
                f"counter_argument content below practitioner-shape "
                f"min-length {COUNTER_ARGUMENT_MIN_CONTENT_LENGTH} "
                f"(got {len(payload.content)}) for claim_id={claim_id!r}"
            )
        if payload.targets_claim_id != claim_id:
            raise SparringValidationError(
                f"counter_argument targets_claim_id={payload.targets_claim_id!r} "
                f"does not match round claim_id={claim_id!r}"
            )
        return payload


class _PractitionerShapeConfidenceCalibration:
    """Architecturally-encoded sub-mechanism B impl per `arch/sparring.md` §2.B.

    Validates sparring-mode output declares typed `ConfidenceLevel` + basis-
    of-confidence (`CONFIDENCE_BASIS_MIN_LENGTH` chars min).
    """

    def validate(self, output: Any, claim_id: str) -> ConfidenceDeclaration:
        if isinstance(output, ConfidenceDeclaration):
            payload = output
        elif isinstance(output, dict):
            raw_level = output.get("confidence") or output.get("level")
            raw_basis = output.get("basis")
            if raw_level is None:
                raise SparringValidationError(
                    f"confidence level missing in sparring-mode output for "
                    f"claim_id={claim_id!r}"
                )
            if raw_basis is None:
                raise SparringValidationError(
                    f"confidence basis missing in sparring-mode output for "
                    f"claim_id={claim_id!r}"
                )
            try:
                level = (
                    raw_level
                    if isinstance(raw_level, ConfidenceLevel)
                    else ConfidenceLevel(raw_level)
                )
            except ValueError as exc:
                raise SparringValidationError(
                    f"confidence level {raw_level!r} not in ConfidenceLevel "
                    f"enum for claim_id={claim_id!r}"
                ) from exc
            if not isinstance(raw_basis, str):
                raise SparringValidationError(
                    f"confidence basis must be str; got "
                    f"{type(raw_basis).__name__} for claim_id={claim_id!r}"
                )
            payload = ConfidenceDeclaration(level=level, basis=raw_basis)
        else:
            raise SparringValidationError(
                f"sparring-mode output must be ConfidenceDeclaration | dict; "
                f"got {type(output).__name__} for claim_id={claim_id!r}"
            )
        if len(payload.basis) < CONFIDENCE_BASIS_MIN_LENGTH:
            raise SparringValidationError(
                f"confidence basis below practitioner-shape min-length "
                f"{CONFIDENCE_BASIS_MIN_LENGTH} (got {len(payload.basis)}) "
                f"for claim_id={claim_id!r}"
            )
        return payload


class _PractitionerShapeVisibleReasoning:
    """Architecturally-encoded sub-mechanism C impl per `arch/sparring.md` §2.C.

    Validates sparring-mode output declares chain-of-inference reasoning
    with `VISIBLE_REASONING_MIN_LENGTH` chars min.
    """

    def validate(self, output: Any, claim_id: str) -> VisibleReasoning:
        if isinstance(output, VisibleReasoning):
            payload = output
        elif isinstance(output, dict):
            raw = (
                output.get("chain_of_inference")
                or output.get("reasoning")
                or output.get("visible_reasoning")
            )
            if raw is None:
                raise SparringValidationError(
                    f"chain_of_inference missing in sparring-mode output for "
                    f"claim_id={claim_id!r}"
                )
            if not isinstance(raw, str):
                raise SparringValidationError(
                    f"chain_of_inference must be str; got "
                    f"{type(raw).__name__} for claim_id={claim_id!r}"
                )
            payload = VisibleReasoning(chain_of_inference=raw)
        else:
            raise SparringValidationError(
                f"sparring-mode output must be VisibleReasoning | dict; got "
                f"{type(output).__name__} for claim_id={claim_id!r}"
            )
        if len(payload.chain_of_inference) < VISIBLE_REASONING_MIN_LENGTH:
            raise SparringValidationError(
                f"visible_reasoning chain_of_inference below practitioner-"
                f"shape min-length {VISIBLE_REASONING_MIN_LENGTH} (got "
                f"{len(payload.chain_of_inference)}) for claim_id={claim_id!r}"
            )
        return payload


class _PractitionerShapeSelectiveFriction:
    """Architecturally-encoded sub-mechanism D impl per `arch/sparring.md` §2.D.

    Compares per-claim ambiguity score against shape-policy threshold band
    (`SELECTIVE_FRICTION_THRESHOLD_BANDS`); returns firing decision. Per
    `arch/sparring.md` §2.D architectural commitment: threshold is shape-
    policy-mandated; impl applies threshold uniformly.
    """

    def __init__(self, threshold_band: str) -> None:
        if threshold_band not in SELECTIVE_FRICTION_THRESHOLD_BANDS:
            raise SparringPolicyError(
                f"selective_friction_threshold {threshold_band!r} not in "
                f"reference-impl threshold bands "
                f"{tuple(SELECTIVE_FRICTION_THRESHOLD_BANDS)}"
            )
        self._threshold_band = threshold_band
        self._threshold_value = SELECTIVE_FRICTION_THRESHOLD_BANDS[threshold_band]

    def evaluate(
        self, claim_id: str, ambiguity_score: float
    ) -> SelectiveFrictionDecision:
        if ambiguity_score < 0.0 or ambiguity_score > 1.0:
            raise SparringValidationError(
                f"ambiguity_score {ambiguity_score} outside [0.0, 1.0] for "
                f"claim_id={claim_id!r}"
            )
        return SelectiveFrictionDecision(
            fired=ambiguity_score >= self._threshold_value,
            ambiguity_score=ambiguity_score,
            targets_claim_id=claim_id,
        )


# ---------------------------------------------------------------------------
# Sub-mechanism impl classes — behaviorally-enforced (5-8)
# ---------------------------------------------------------------------------


class _PractitionerShapeAntiSycophancy:
    """Behaviorally-enforced sub-mechanism E impl per `arch/sparring.md` §2.E.

    Heuristic detection compares current output against prior turn for
    soften-without-evidence keyword pattern. Phase 6.1 reference impl is a
    simple keyword-match heuristic; Phase 6.2 W2 watch-list refines per
    false-positive friction-budget data.
    """

    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def detect(self, current_output: str, prior_output: str | None) -> bool:
        if self._threshold <= 0.0:
            return False
        if prior_output is None:
            return False
        lowered = current_output.lower()
        match_count = sum(
            1 for keyword in ANTI_SYCOPHANCY_KEYWORDS if keyword in lowered
        )
        if match_count == 0:
            return False
        score = match_count / len(ANTI_SYCOPHANCY_KEYWORDS)
        return score >= self._threshold


class _PractitionerShapeAsymmetricKnowledgeRespect:
    """Behaviorally-enforced sub-mechanism F impl per `arch/sparring.md` §2.F.

    Records "I'm drawing on X; local context Y might change this"
    declarations; AI applies at judgment time. Phase 6.1 reference impl
    captures the declaration via `emit()` callsite and routes through the
    aggregating class's audit emission path.
    """

    def __init__(self, on_emit: Callable[[str, dict[str, Any]], None]) -> None:
        self._on_emit = on_emit

    def emit(self, claim_id: str, context: dict[str, Any]) -> None:
        self._on_emit(claim_id, dict(context))


class _PractitionerShapeCommitToRecommendations:
    """Behaviorally-enforced sub-mechanism G impl per `arch/sparring.md` §2.G.

    Records per-claim recommendation commitment; AI applies context-
    dependent commit-vs-question discrimination at judgment time.
    """

    def __init__(self, on_emit: Callable[[str, str], None]) -> None:
        self._on_emit = on_emit

    def emit(self, claim_id: str, recommendation: str) -> None:
        self._on_emit(claim_id, recommendation)


class _PractitionerShapeWhatsMissingCheckpoint:
    """Behaviorally-enforced sub-mechanism H impl per `arch/sparring.md` §2.H.

    Records Phase B layered-review what's-missing checkpoint application;
    structural in skill body but content is judgment-applied per §2.H.
    """

    def __init__(self, on_emit: Callable[[str, list[str]], None]) -> None:
        self._on_emit = on_emit

    def emit(self, claim_id: str, coverage_gaps: list[str]) -> None:
        self._on_emit(claim_id, list(coverage_gaps))


# ---------------------------------------------------------------------------
# PractitionerShapeSparring — aggregating Implementation class
# ---------------------------------------------------------------------------


class PractitionerShapeSparring:
    """Practitioner-shape sparring mechanism class satisfying
    `SparringProtocol` per `arch/sparring.md`.

    Surface satisfaction is structural — instances pass
    `isinstance(sparring, SparringProtocol)` per the `runtime_checkable`
    Protocol decorator on `pbs.sparring.SparringProtocol`.

    State (instance-private):

    - `_policy`: per-shape policy bundle (activation matrix + thresholds +
      retry budget + fail-closed flag)
    - `_config`: per-shape impl config (actor_id)
    - `_emitter`: injected `AuditEmitter` callable for sparring event
      emission (Phase 6.1 collapses skill-side MCP audit gate path to
      direct injection per Note 75-79 thin-slice convention)
    - 8 `_<sub_mechanism>` private fields holding the sub-mechanism impl
      instances exposed via the 8 SparringProtocol property accessors
    - `_is_ready`: True between construction and shutdown
    - `_is_shutting_down`: idempotent shutdown guard
    """

    def __init__(
        self,
        policy: SparringPolicy,
        config: PractitionerShapeSparringConfig,
        emitter: AuditEmitter,
    ) -> None:
        """Internal constructor. Use `from_shape_policy()` factory."""
        self._policy = policy
        self._config = config
        self._emitter = emitter
        self._is_ready: bool = False
        self._is_shutting_down: bool = False

        # Architecturally-encoded sub-mechanism impl instances (1-4)
        self._counter_argument = _PractitionerShapeCounterArgument()
        self._confidence_calibration = _PractitionerShapeConfidenceCalibration()
        self._visible_reasoning = _PractitionerShapeVisibleReasoning()
        self._selective_friction = _PractitionerShapeSelectiveFriction(
            threshold_band=policy.selective_friction_threshold
        )

        # Behaviorally-enforced sub-mechanism impl instances (5-8) wired with
        # closures so emit() callsites route through the aggregating class's
        # audit emission path (skill-side MCP audit gate per §8).
        self._anti_sycophancy = _PractitionerShapeAntiSycophancy(
            threshold=policy.anti_sycophancy_threshold
        )
        self._asymmetric_knowledge_respect = _PractitionerShapeAsymmetricKnowledgeRespect(
            on_emit=self._emit_asymmetric_knowledge_respected
        )
        self._commit_to_recommendations = _PractitionerShapeCommitToRecommendations(
            on_emit=self._emit_recommendation_committed
        )
        self._whats_missing_checkpoint = _PractitionerShapeWhatsMissingCheckpoint(
            on_emit=self._emit_whats_missing_checked
        )

    # ------------------------------------------------------------------
    # Lifecycle (§9 + composition with substrate boot per §10)
    # ------------------------------------------------------------------

    @classmethod
    async def from_shape_policy(
        cls,
        policy: SparringPolicy,
        config: PractitionerShapeSparringConfig,
        emitter: AuditEmitter,
    ) -> PractitionerShapeSparring:
        """Boot per `arch/sparring.md` §10 (N/A separate sparring-impl boot
        phases) + Phase 6.1 mechanism-impl factory convention (audit /
        gate / authority-binding precedent).

        Per-policy validation:
        - retry_budget non-negative
        - selective_friction_threshold band recognized
        - anti_sycophancy_threshold within [0.0, 1.0]
        - emitter callable (Phase 6.1 thin-slice precondition matching
          `practitioner_shape_authority_binding.from_config_with_emitter`)

        Raises:
            SparringPolicyError: activation matrix / threshold / retry-
                budget value out of range.
        """
        if emitter is None or not callable(emitter):
            raise SparringPolicyError(
                "PractitionerShapeSparring requires a callable AuditEmitter "
                "at construction; received None / non-callable."
            )
        if policy.retry_budget < 0:
            raise SparringPolicyError(
                f"retry_budget must be non-negative; got {policy.retry_budget}"
            )
        if not 0.0 <= policy.anti_sycophancy_threshold <= 1.0:
            raise SparringPolicyError(
                f"anti_sycophancy_threshold {policy.anti_sycophancy_threshold} "
                f"outside [0.0, 1.0]"
            )
        if policy.selective_friction_threshold not in SELECTIVE_FRICTION_THRESHOLD_BANDS:
            raise SparringPolicyError(
                f"selective_friction_threshold "
                f"{policy.selective_friction_threshold!r} not in reference-"
                f"impl threshold bands "
                f"{tuple(SELECTIVE_FRICTION_THRESHOLD_BANDS)}"
            )
        for kind in policy.active_sub_mechanisms:
            if not isinstance(kind, SubMechanismKind):
                raise SparringPolicyError(
                    f"active_sub_mechanisms entry {kind!r} not a "
                    f"SubMechanismKind value"
                )
        instance = cls(policy=policy, config=config, emitter=emitter)
        instance._is_ready = True
        return instance

    @property
    def is_ready(self) -> bool:
        return self._is_ready and not self._is_shutting_down

    async def shutdown(self) -> None:
        """Per `SparringProtocol.shutdown` + `arch/sparring.md` §10 (N/A
        separate phases). Idempotent. Releases per-sub-mechanism state
        (Phase 6.1 reference impls are stateless; preserved for Surface
        uniformity with mechanism-class peers audit / quality-gate)."""
        if self._is_shutting_down:
            return
        self._is_shutting_down = True
        self._is_ready = False

    # ------------------------------------------------------------------
    # Sub-mechanism accessors (8 properties per `SparringProtocol`)
    # ------------------------------------------------------------------

    @property
    def counter_argument(self) -> CounterArgumentSubMechanism:
        return self._counter_argument

    @property
    def confidence_calibration(self) -> ConfidenceCalibrationSubMechanism:
        return self._confidence_calibration

    @property
    def visible_reasoning(self) -> VisibleReasoningSubMechanism:
        return self._visible_reasoning

    @property
    def selective_friction(self) -> SelectiveFrictionSubMechanism:
        return self._selective_friction

    @property
    def anti_sycophancy(self) -> AntiSycophancySubMechanism:
        return self._anti_sycophancy

    @property
    def asymmetric_knowledge_respect(self) -> AsymmetricKnowledgeRespectSubMechanism:
        return self._asymmetric_knowledge_respect

    @property
    def commit_to_recommendations(self) -> CommitToRecommendationsSubMechanism:
        return self._commit_to_recommendations

    @property
    def whats_missing_checkpoint(self) -> WhatsMissingCheckpointSubMechanism:
        return self._whats_missing_checkpoint

    # ------------------------------------------------------------------
    # Per-claim sparring round entry point (§9 cardinality + §11 errors)
    # ------------------------------------------------------------------

    async def run_round(
        self,
        claim_id: str,
        skill_output: Any,
        prior_output: str | None = None,
    ) -> SparringRoundResult:
        """Run a sparring round for `claim_id` per `arch/sparring.md` §1 + §9.

        Validates architecturally-encoded sub-mechanisms 1-4 against
        `skill_output` (per activation matrix); behaviorally-enforced sub-
        mechanisms 5-8 are emit-driven (caller invokes their `emit()` at
        judgment time, not aggregated here) — anti-sycophancy heuristic IS
        evaluated within run_round since it has structural detection
        (current vs prior).

        Retry semantics: validation failures retry up to
        `policy.retry_budget` then escalate per `policy.fail_closed`
        (`SparringRetryExhaustedError` for fail-closed; bypass-with-reason
        path for fail-open). Phase 6.1 thin-slice: a single skill_output
        is provided per call; "retry" semantics surface as orchestrator-
        level retry by the caller (this method validates once + emits per-
        retry events when invoked repeatedly with the same claim_id by an
        outer orchestrator). Per `arch/sparring.md` §15 orchestrator wiring
        operational concerns: full retry-on-fail orchestration (skill re-
        invocation) lives at Phase 6 deployment-instance wiring; this impl
        emits the per-call audit-trail events.

        Emits:
        - Per architecturally-encoded sub-mechanism (1-4): `*_produced` /
          `*_calibrated` / `*_provided` / `*_applied` on PASS;
          `*_missing` / `*_skipped` on FAIL
        - `AntiSycophancyFlagRaised` when sub-mechanism E heuristic fires
        - `SparringRoundCompleted` at round close (always emitted; status
          carries verdict)
        - `SparringValidationRetry` on per-call validation failure when
          retry budget remaining; `SparringBypassWithReason` if caller
          passes bypass via failure path
        """
        if not self.is_ready:
            raise SparringRetryExhaustedError(
                f"PractitionerShapeSparring not in ready state; run_round "
                f"rejected for claim_id={claim_id!r}"
            )

        verdicts: dict[SubMechanismKind, bool] = {}
        validation_failures: list[SparringValidationError] = []

        # Architecturally-encoded 1-4 — only validate when active per matrix.
        if SubMechanismKind.COUNTER_ARGUMENT in self._policy.active_sub_mechanisms:
            try:
                ca = self._counter_argument.validate(skill_output, claim_id)
                self._emit(
                    CounterArgumentProduced(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={
                            "content_length": len(ca.content),
                            "targets_claim_id": ca.targets_claim_id,
                        },
                    )
                )
                verdicts[SubMechanismKind.COUNTER_ARGUMENT] = True
            except SparringValidationError as exc:
                self._emit(
                    CounterArgumentMissing(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={"reason": str(exc)},
                    )
                )
                verdicts[SubMechanismKind.COUNTER_ARGUMENT] = False
                validation_failures.append(exc)

        if (
            SubMechanismKind.CONFIDENCE_CALIBRATION
            in self._policy.active_sub_mechanisms
        ):
            try:
                cd = self._confidence_calibration.validate(skill_output, claim_id)
                self._emit(
                    ConfidenceCalibrated(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={
                            "level": cd.level.value,
                            "basis": cd.basis,
                        },
                    )
                )
                verdicts[SubMechanismKind.CONFIDENCE_CALIBRATION] = True
            except SparringValidationError as exc:
                self._emit(
                    ConfidenceMissing(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={"reason": str(exc)},
                    )
                )
                verdicts[SubMechanismKind.CONFIDENCE_CALIBRATION] = False
                validation_failures.append(exc)

        if SubMechanismKind.VISIBLE_REASONING in self._policy.active_sub_mechanisms:
            try:
                vr = self._visible_reasoning.validate(skill_output, claim_id)
                self._emit(
                    VisibleReasoningProvided(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={"chain_length": len(vr.chain_of_inference)},
                    )
                )
                verdicts[SubMechanismKind.VISIBLE_REASONING] = True
            except SparringValidationError as exc:
                self._emit(
                    VisibleReasoningMissing(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={"reason": str(exc)},
                    )
                )
                verdicts[SubMechanismKind.VISIBLE_REASONING] = False
                validation_failures.append(exc)

        if SubMechanismKind.SELECTIVE_FRICTION in self._policy.active_sub_mechanisms:
            ambiguity_score = (
                skill_output.get("ambiguity_score", 0.0)
                if isinstance(skill_output, dict)
                else 0.0
            )
            try:
                decision = self._selective_friction.evaluate(
                    claim_id, ambiguity_score
                )
                if decision.fired:
                    self._emit(
                        SelectiveFrictionApplied(
                            actor_kind=ActorKind.AI_RUNTIME,
                            actor_id=self._config.actor_id,
                            timestamp=self._now(),
                            claim_id=claim_id,
                            details={
                                "ambiguity_score": decision.ambiguity_score,
                                "threshold_band": (
                                    self._policy.selective_friction_threshold
                                ),
                            },
                        )
                    )
                else:
                    self._emit(
                        SelectiveFrictionSkipped(
                            actor_kind=ActorKind.AI_RUNTIME,
                            actor_id=self._config.actor_id,
                            timestamp=self._now(),
                            claim_id=claim_id,
                            details={
                                "ambiguity_score": decision.ambiguity_score,
                                "threshold_band": (
                                    self._policy.selective_friction_threshold
                                ),
                            },
                        )
                    )
                verdicts[SubMechanismKind.SELECTIVE_FRICTION] = True
            except SparringValidationError as exc:
                verdicts[SubMechanismKind.SELECTIVE_FRICTION] = False
                validation_failures.append(exc)

        # Behaviorally-enforced E — heuristic detection within run_round
        # (current-vs-prior comparison happens here, not at emit-callsite).
        if SubMechanismKind.ANTI_SYCOPHANCY in self._policy.active_sub_mechanisms:
            current_str = (
                skill_output
                if isinstance(skill_output, str)
                else str(skill_output)
            )
            sycophancy_detected = self._anti_sycophancy.detect(
                current_output=current_str, prior_output=prior_output
            )
            if sycophancy_detected:
                self._emit(
                    AntiSycophancyFlagRaised(
                        actor_kind=ActorKind.AI_RUNTIME,
                        actor_id=self._config.actor_id,
                        timestamp=self._now(),
                        claim_id=claim_id,
                        details={
                            "threshold": self._policy.anti_sycophancy_threshold,
                        },
                    )
                )
            verdicts[SubMechanismKind.ANTI_SYCOPHANCY] = not sycophancy_detected

        # Behaviorally-enforced F/G/H — emit-callsite-driven; mark verdict
        # True at round close (caller invokes emit() at judgment time).
        for kind in (
            SubMechanismKind.ASYMMETRIC_KNOWLEDGE_RESPECT,
            SubMechanismKind.COMMIT_TO_RECOMMENDATIONS,
            SubMechanismKind.WHATS_MISSING_CHECKPOINT,
        ):
            if kind in self._policy.active_sub_mechanisms:
                verdicts[kind] = True

        # Round close — determine status per validation failures + fail-closed.
        if validation_failures and self._policy.fail_closed:
            self._emit(
                SparringValidationRetry(
                    actor_kind=ActorKind.AI_RUNTIME,
                    actor_id=self._config.actor_id,
                    timestamp=self._now(),
                    claim_id=claim_id,
                    details={
                        "failure_count": len(validation_failures),
                        "first_reason": str(validation_failures[0]),
                    },
                )
            )
            result = SparringRoundResult(
                claim_id=claim_id,
                status="failed",
                sub_mechanism_verdicts=verdicts,
                retry_count=0,
            )
            self._emit_round_completed(result)
            raise SparringValidationError(
                f"sparring round failed for claim_id={claim_id!r}: "
                f"{len(validation_failures)} sub-mechanism violation(s); "
                f"first: {validation_failures[0]}"
            )

        result = SparringRoundResult(
            claim_id=claim_id,
            status="completed",
            sub_mechanism_verdicts=verdicts,
            retry_count=0,
        )
        self._emit_round_completed(result)
        return result

    def bypass_round(
        self,
        claim_id: str,
        bypass_reason: str,
        retry_count: int,
    ) -> SparringRoundResult:
        """Caller-driven bypass-with-reason path per `arch/sparring.md` §8.

        Phase 6.1 thin-slice exposes the bypass emission as an explicit
        callsite (Phase 6.2 wires the orchestrator retry-exhaustion → bypass
        callback). Emits `SparringBypassWithReason` with `bypass_reason` in
        details; per §8 first-class in audit-trail for L8 auditor reasoning-
        chain reconstruction.

        Raises:
            SparringRetryExhaustedError: practitioner-shape fail-closed
                semantics — bypass blocked when retry-count exceeded
                (defensibility-critical; per `arch/sparring.md` §14 row 1).
                Caller catches + raises to user per `arch/sparring.md` §11
                error semantics.
        """
        if not self.is_ready:
            raise SparringRetryExhaustedError(
                f"PractitionerShapeSparring not in ready state; bypass_round "
                f"rejected for claim_id={claim_id!r}"
            )
        if not bypass_reason:
            raise SparringValidationError(
                f"bypass_reason must be non-empty for claim_id={claim_id!r}"
            )
        self._emit(
            SparringBypassWithReason(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=self._now(),
                claim_id=claim_id,
                details={
                    "bypass_reason": bypass_reason,
                    "retry_count": retry_count,
                },
            )
        )
        result = SparringRoundResult(
            claim_id=claim_id,
            status="bypass_with_reason",
            retry_count=retry_count,
            bypass_reason=bypass_reason,
        )
        self._emit_round_completed(result)
        if self._policy.fail_closed:
            raise SparringRetryExhaustedError(
                f"sparring round bypass-with-reason for claim_id={claim_id!r} "
                f"raised under practitioner-shape fail-closed semantics; "
                f"caller surfaces to practitioner per `arch/sparring.md` §14"
            )
        return result

    # ------------------------------------------------------------------
    # Failure-mode detection (§8 — feeds quality-gate axis-2 enforcement)
    # ------------------------------------------------------------------

    def report_failure_mode(
        self, mode: FailureMode, claim_id: str | None
    ) -> None:
        """Per `SparringProtocol.report_failure_mode`. Emits the
        `*_detected` event per `mode` discriminator; events feed quality-
        gate's axis-2 enforcement per `arch/quality-gate.md` §2.B per-axis
        signal ingestion."""
        if not self.is_ready:
            raise SparringRetryExhaustedError(
                "PractitionerShapeSparring not in ready state; "
                "report_failure_mode rejected"
            )
        timestamp = self._now()
        common_details = {"mode": mode.value}
        event: AuditEventBase
        if mode is FailureMode.ANSWER_MACHINE:
            event = AnswerMachineDetected(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=timestamp,
                claim_id=claim_id,
                details=common_details,
            )
        elif mode is FailureMode.ORACLE_MODE:
            event = OracleModeDetected(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=timestamp,
                claim_id=claim_id,
                details=common_details,
            )
        elif mode is FailureMode.VALIDATOR_MODE:
            event = ValidatorModeDetected(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=timestamp,
                claim_id=claim_id,
                details=common_details,
            )
        else:
            raise SparringValidationError(
                f"unknown FailureMode {mode!r}; reference impl supports "
                f"answer_machine / oracle_mode / validator_mode"
            )
        self._emit(event)

    # ------------------------------------------------------------------
    # Internal emission helpers (skill-side via injected emitter per §8)
    # ------------------------------------------------------------------

    def _emit(self, event: AuditEventBase) -> None:
        self._emitter(event)

    def _emit_round_completed(self, result: SparringRoundResult) -> None:
        verdict_payload = {
            kind.value: passed
            for kind, passed in result.sub_mechanism_verdicts.items()
        }
        details: dict[str, Any] = {
            "status": result.status,
            "retry_count": result.retry_count,
            "verdicts": verdict_payload,
        }
        if result.bypass_reason is not None:
            details["bypass_reason"] = result.bypass_reason
        self._emit(
            SparringRoundCompleted(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=self._now(),
                claim_id=result.claim_id,
                details=details,
            )
        )

    def _emit_asymmetric_knowledge_respected(
        self, claim_id: str, context: dict[str, Any]
    ) -> None:
        self._emit(
            AsymmetricKnowledgeRespected(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=self._now(),
                claim_id=claim_id,
                details={"context": context},
            )
        )

    def _emit_recommendation_committed(
        self, claim_id: str, recommendation: str
    ) -> None:
        self._emit(
            RecommendationCommitted(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=self._now(),
                claim_id=claim_id,
                details={"recommendation": recommendation},
            )
        )

    def _emit_whats_missing_checked(
        self, claim_id: str, coverage_gaps: list[str]
    ) -> None:
        self._emit(
            WhatsMissingChecked(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._config.actor_id,
                timestamp=self._now(),
                claim_id=claim_id,
                details={"coverage_gaps": coverage_gaps},
            )
        )

    @staticmethod
    def _now() -> datetime:
        return datetime.now(tz=UTC)


# ---------------------------------------------------------------------------
# Module-level helper for default practitioner-shape SparringPolicy
# ---------------------------------------------------------------------------


def practitioner_shape_default_policy(
    *,
    shape_id: str = "practitioner",
    selective_friction_threshold: str = "substantive",
    anti_sycophancy_threshold: float = 0.3,
    retry_budget: int = 3,
) -> SparringPolicy:
    """Convenience constructor for the canonical practitioner-shape
    `SparringPolicy` per `arch/sparring.md` §14 practitioner-shape profile:
    all 8 sub-mechanisms active; fail-closed; retry budget 3.

    Reference defaults — Phase 6.1 thin-slice; Phase 6.2 deployment-instance
    wiring may override via the explicit `SparringPolicy(...)` constructor
    per `arch/sparring.md` §15 pre-implementation operational concerns.
    """
    return SparringPolicy(
        shape_id=shape_id,
        active_sub_mechanisms=PRACTITIONER_SHAPE_ACTIVE_SUB_MECHANISMS,
        selective_friction_threshold=selective_friction_threshold,
        anti_sycophancy_threshold=anti_sycophancy_threshold,
        retry_budget=retry_budget,
        fail_closed=True,
    )


def practitioner_shape_default_actor_id() -> str:
    """Convenience constructor for sparring Running Instance `actor_id` per
    `arch/sparring.md` §7 composition with `actor` (AI_RUNTIME). Generates
    a stable per-Instance identity matching the Phase 6.1 substrate impl
    actor_id convention."""
    return f"{SPARRING_IMPL_ID}:{uuid4()}"
