"""Sparring mechanism class Surface — per `arch/sparring.md`.

Per `arch/sparring.md` §1: the runtime mechanism set realizing axis-2
(sparring) as a load-bearing pillar in practitioner-shape workspaces. Each
of the 8 sub-mechanisms is its own atomic mechanism contract; the Sparring
class aggregates the 8 under a single architectural-conceptual home,
parameterized by per-shape policy.

Per `arch/sparring.md` §6: this is a **mechanism class**, NOT Pattern A —
sub-mechanism realization is per-sub-mechanism (no whole-class alternative
architecture swap). Per §5: 8 sub-mechanisms fixed at framework-mechanism
layer (4 architecturally-encoded + 4 behaviorally-enforced); per-shape
policy declares activation matrix + thresholds + retry budget.

Per `arch/sparring.md` §8: sparring sub-mechanisms emit events via MCP
audit gate (skill-side) per audit mechanism class emission discipline; not
substrate-internal direct emission. Same convention as adapter §8 +
quality-gate §8.

Sub-mechanism Surfaces (§2; 8 sub-Protocols):

Architecturally-encoded (4; gate-dispatched at every output):
- §2.A `CounterArgumentSubMechanism` — counter-argument as first-class output
- §2.B `ConfidenceCalibrationSubMechanism` — typed confidence + basis
- §2.C `VisibleReasoningSubMechanism` — chain-of-inference disclosure
- §2.D `SelectiveFrictionSubMechanism` — per-claim-ambiguity threshold

Behaviorally-enforced (4; AI applies at judgment time):
- §2.E `AntiSycophancySubMechanism` — soften-without-evidence detection
- §2.F `AsymmetricKnowledgeRespectSubMechanism` — local-context declarative
- §2.G `CommitToRecommendationsSubMechanism` — context-dependent commit
- §2.H `WhatsMissingCheckpointSubMechanism` — Phase B layered review

The aggregating `SparringProtocol` Surface exposes the 8 sub-mechanisms +
class-level lifecycle (`from_shape_policy` / `is_ready` / `shutdown`).

Per §10: N/A — sparring sub-mechanisms run within skill execution
lifecycle; no separate sparring-impl boot/shutdown phases beyond
sub-mechanism schema registration via substrate Surface §D at substrate
boot.

Per §12 + §13: N/A — transport-uniform + tier-uniform at architectural
level (per-tier variation lives at substrate-impl + per-shape policy).

Per §14: per-shape activation matrix is the PRIMARY conditional —
practitioner-shape activates all 8 (axis-2 critical for defensibility);
autonomous-business-shape activates 4-6 per business policy; personal-OS-
shape activates 1-3 per user preference.
"""

from enum import StrEnum
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Supporting enums (§2.B confidence; §11 failure modes; §14 per-shape
# activation matrix shape identifier)
# ---------------------------------------------------------------------------


class ConfidenceLevel(StrEnum):
    """Typed confidence per `arch/sparring.md` §2.B.

    Architecturally-encoded sub-mechanism B requires every sparring-mode
    skill output to declare a confidence level + basis-of-confidence;
    schema-validated via substrate Surface §D structured output validation.
    Missing field fails validation per §11 `SparringValidationError`.
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SubMechanismKind(StrEnum):
    """Sub-mechanism identifier per `arch/sparring.md` §2.

    Eight framework-baseline sub-mechanisms (4 architecturally-encoded +
    4 behaviorally-enforced) per §3 + §4 framework-baseline confirmation.
    Used as activation-matrix key in per-shape policy + as `details`
    field discriminator in failure-mode-detected events per §8.

    Shape-extension sub-mechanisms (per §3 + §4 + W4 watch-list) are
    additive in shape policy bundle distribution; framework-baseline
    enumeration here is fixed.
    """

    COUNTER_ARGUMENT = "counter_argument"
    CONFIDENCE_CALIBRATION = "confidence_calibration"
    VISIBLE_REASONING = "visible_reasoning"
    SELECTIVE_FRICTION = "selective_friction"
    ANTI_SYCOPHANCY = "anti_sycophancy"
    ASYMMETRIC_KNOWLEDGE_RESPECT = "asymmetric_knowledge_respect"
    COMMIT_TO_RECOMMENDATIONS = "commit_to_recommendations"
    WHATS_MISSING_CHECKPOINT = "whats_missing_checkpoint"


class FailureMode(StrEnum):
    """Axis-2 failure mode per `arch/sparring.md` §8.

    Per locked GLOSSARY answer-machine-ai / oracle-ai / validator-ai
    entries: axis-2 collapse modes sparring is the success mode against.
    Sparring impl may emit `failure_mode_detected` events when sub-
    mechanism violations cluster; events feed quality-gate's axis-2
    enforcement per `arch/quality-gate.md` §2.B per-axis signal ingestion.
    """

    ANSWER_MACHINE = "answer_machine"
    ORACLE_MODE = "oracle_mode"
    VALIDATOR_MODE = "validator_mode"


# ---------------------------------------------------------------------------
# Per-shape policy (§4 + §5 + §14) + per-claim sparring round result models
# ---------------------------------------------------------------------------


class SparringPolicy(BaseModel):
    """Per-shape sparring policy bundle per `arch/sparring.md` §4 + §5 + §14.

    Loaded from active shape's policy bundle at workspace boot per §10
    composition with substrate boot (sub-mechanism schema registration
    happens within substrate boot per substrate topic §10).

    Per-shape activation matrix table per §5: practitioner-shape activates
    all 8 (fail-closed; ≥1 sparring-event per claim mandatory);
    autonomous-business-shape activates subset per business policy
    (fail-open with alert); personal-OS-shape activates subset per user
    preference (fail-open).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    shape_id: str
    """Active shape identifier (e.g., `practitioner`, `autonomous_business`,
    `personal_os`) per `glossary/shape.md`."""

    active_sub_mechanisms: frozenset[SubMechanismKind]
    """Activation matrix: which framework-baseline sub-mechanisms enforced
    in this shape. Per §5 cardinality: 0-8 active per workspace."""

    selective_friction_threshold: str = "substantive"
    """Selective-friction claim-ambiguity threshold per §14 per-shape
    profiles. Practitioner-shape default: `substantive` (medium-or-higher
    triggers); per-shape declarations may override."""

    anti_sycophancy_threshold: float = 0.0
    """Anti-sycophancy heuristic-detection threshold per §15 pre-
    implementation operational concerns (impl-tunable). 0.0 = disabled;
    higher = stricter. Specific scoring semantics per Phase 6 per-impl spec."""

    retry_budget: int = 3
    """Orchestrator retry budget before bypass-with-reason escalation per
    §14 per-shape profiles. Practitioner-shape default: 3."""

    fail_closed: bool = True
    """Per §14 per-shape error semantics: practitioner-shape fail-closed
    (defensibility-critical); autonomous-business-shape + personal-OS-shape
    fail-open. True → validation failures escalate; False → degrade with
    alert per shape policy."""


class SparringRoundResult(BaseModel):
    """Per-claim sparring round outcome per `arch/sparring.md` §9 cardinality
    + §11 error categories.

    Returned by `SparringProtocol.run_round()` after a sparring round
    completes for a given claim; aggregates per-sub-mechanism verdicts +
    retry count + bypass reason (when applicable). Composes with engaged-
    authorship two-phase composite per §1 cross-axis dependency.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_id: str
    """Claim attribution per `arch/claim-defensibility.md` per-claim
    reasoning chain reconstruction."""

    status: Literal["completed", "bypass_with_reason", "retry_exhausted", "failed"]
    """Round lifecycle status. Per §11 + §14 per-shape error semantics:
    `bypass_with_reason` requires `bypass_reason` populated;
    `retry_exhausted` raises `SparringRetryExhaustedError` for fail-closed
    shapes."""

    sub_mechanism_verdicts: dict[SubMechanismKind, bool] = Field(default_factory=dict)
    """Per-sub-mechanism pass/fail verdict for active sub-mechanisms.
    True = sub-mechanism satisfied (architecturally-encoded: schema valid;
    behaviorally-enforced: AI applied at judgment time)."""

    retry_count: int = 0
    """Number of retry attempts before completion / bypass / exhaustion.
    Compared against `SparringPolicy.retry_budget` for escalation."""

    bypass_reason: str | None = None
    """Required when `status == "bypass_with_reason"` per §8 bypass-with-
    reason audit semantics. First-class in audit-trail for L8 auditor
    reasoning-chain reconstruction."""


class CounterArgument(BaseModel):
    """Counter-argument output per `arch/sparring.md` §2.A.

    Architecturally-encoded sub-mechanism A requires sparring-mode skill
    outputs to declare a counter-argument category; substrate Surface §D
    enforces presence + min-content. Schema-validated; missing fails
    validation per §11 `SparringValidationError`.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    content: str
    """Counter-argument body. Min-length enforced via Pydantic validation
    per Phase 6 per-impl spec."""

    targets_claim_id: str
    """Claim the counter-argument targets per `arch/sparring.md` §1 cross-
    axis dependency (sparring fires AT claim granularity)."""


class ConfidenceDeclaration(BaseModel):
    """Confidence calibration output per `arch/sparring.md` §2.B.

    Architecturally-encoded sub-mechanism B requires sparring-mode skill
    outputs to declare confidence + basis. Schema-validated; missing fails
    validation per §11 `SparringValidationError`.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    level: ConfidenceLevel
    basis: str
    """Basis-of-confidence rationale per §2.B. Min-content enforced via
    Pydantic validation per Phase 6 per-impl spec."""


class VisibleReasoning(BaseModel):
    """Visible-reasoning output per `arch/sparring.md` §2.C.

    Architecturally-encoded sub-mechanism C requires sparring-mode skill
    outputs to declare a chain-of-inference reasoning category (not just a
    verdict); min-content enforced.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    chain_of_inference: str
    """Reasoning chain. Min-content enforced via Pydantic validation per
    Phase 6 per-impl spec."""


class SelectiveFrictionDecision(BaseModel):
    """Selective-friction firing decision per `arch/sparring.md` §2.D.

    Sub-mechanism D fires per claim-ambiguity threshold; threshold is
    shape-policy-mandated (gate-dispatched parameter via
    `SparringPolicy.selective_friction_threshold`). Records the firing
    decision + per-claim ambiguity score for downstream audit emission.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    fired: bool
    """True when per-claim ambiguity exceeded shape-policy threshold;
    skill paused for friction injection."""

    ambiguity_score: float
    """Per-claim ambiguity scoring per Phase 6 per-impl spec. Compared
    against `SparringPolicy.selective_friction_threshold` semantics."""

    targets_claim_id: str


# ---------------------------------------------------------------------------
# Per-sub-mechanism event-kind catalog (§8 — skill-side via MCP audit gate)
# ---------------------------------------------------------------------------


class CounterArgumentProduced(AuditEventBase):
    """Counter-argument produced per `arch/sparring.md` §8."""

    event_kind: Literal["counter_argument_produced"] = "counter_argument_produced"


class CounterArgumentMissing(AuditEventBase):
    """Counter-argument missing per `arch/sparring.md` §8.

    Composes with `SparringValidationError` (raised at validation site;
    this event records the failure in audit-trail per §11)."""

    event_kind: Literal["counter_argument_missing"] = "counter_argument_missing"


class ConfidenceCalibrated(AuditEventBase):
    """Confidence calibration declaration per `arch/sparring.md` §8.

    `details` field carries `level` + `basis` from `ConfidenceDeclaration`."""

    event_kind: Literal["confidence_calibrated"] = "confidence_calibrated"


class ConfidenceMissing(AuditEventBase):
    """Confidence declaration missing per `arch/sparring.md` §8."""

    event_kind: Literal["confidence_missing"] = "confidence_missing"


class VisibleReasoningProvided(AuditEventBase):
    """Visible-reasoning chain-of-inference provided per `arch/sparring.md` §8."""

    event_kind: Literal["visible_reasoning_provided"] = "visible_reasoning_provided"


class VisibleReasoningMissing(AuditEventBase):
    """Visible-reasoning chain-of-inference missing per `arch/sparring.md` §8."""

    event_kind: Literal["visible_reasoning_missing"] = "visible_reasoning_missing"


class SelectiveFrictionApplied(AuditEventBase):
    """Selective-friction fired per `arch/sparring.md` §8.

    `details` field carries `ambiguity_score` + threshold context per
    `SelectiveFrictionDecision`."""

    event_kind: Literal["selective_friction_applied"] = "selective_friction_applied"


class SelectiveFrictionSkipped(AuditEventBase):
    """Selective-friction below threshold per `arch/sparring.md` §8."""

    event_kind: Literal["selective_friction_skipped"] = "selective_friction_skipped"


class AntiSycophancyFlagRaised(AuditEventBase):
    """Anti-sycophancy heuristic detection fired per `arch/sparring.md` §8.

    Behaviorally-enforced sub-mechanism E heuristic compares current skill
    output against prior turn for soften-without-evidence pattern; emits
    when detected per §2.E."""

    event_kind: Literal["anti_sycophancy_flag_raised"] = "anti_sycophancy_flag_raised"


class AsymmetricKnowledgeRespected(AuditEventBase):
    """Asymmetric-knowledge-respect declarative emission per `arch/sparring.md` §8.

    Behaviorally-enforced sub-mechanism F: AI emits at completion when
    "I'm drawing on X; local context Y might change this" surfaced per §2.F."""

    event_kind: Literal["asymmetric_knowledge_respected"] = "asymmetric_knowledge_respected"


class RecommendationCommitted(AuditEventBase):
    """Commit-to-recommendations applied per `arch/sparring.md` §8.

    Behaviorally-enforced sub-mechanism G: AI applies per-claim commit-vs-
    question discrimination at judgment time per §2.G."""

    event_kind: Literal["recommendation_committed"] = "recommendation_committed"


class WhatsMissingChecked(AuditEventBase):
    """What's-missing checkpoint applied per `arch/sparring.md` §8.

    Behaviorally-enforced sub-mechanism H: Phase B layered review
    checkpoint applied per §2.H."""

    event_kind: Literal["whats_missing_checked"] = "whats_missing_checked"


# Cross-cutting (sparring-round level; §8)


class SparringRoundCompleted(AuditEventBase):
    """Sparring round completed for a claim per `arch/sparring.md` §8."""

    event_kind: Literal["sparring_round_completed"] = "sparring_round_completed"


class SparringBypassWithReason(AuditEventBase):
    """User bypass after retry-count exhausted per `arch/sparring.md` §8.

    `details` field carries `bypass_reason: str` per §8 bypass-with-reason
    audit semantics; first-class in audit-trail for L8 auditor reasoning-
    chain reconstruction per L8 audit-trail integrity discipline."""

    event_kind: Literal["sparring_bypass_with_reason"] = "sparring_bypass_with_reason"


class SparringValidationRetry(AuditEventBase):
    """Validation-failed retry per `arch/sparring.md` §8.

    Per §14 per-shape retry budget; emits per-retry until exhaustion."""

    event_kind: Literal["sparring_validation_retry"] = "sparring_validation_retry"


# Axis-2 failure-mode detection (§8)


class AnswerMachineDetected(AuditEventBase):
    """Answer-machine pattern detected per `arch/sparring.md` §8 + locked
    GLOSSARY `answer-machine-ai` entry. Feeds quality-gate axis-2
    enforcement per `arch/quality-gate.md` §2.B."""

    event_kind: Literal["answer_machine_detected"] = "answer_machine_detected"


class OracleModeDetected(AuditEventBase):
    """Oracle-mode pattern detected per `arch/sparring.md` §8 + locked
    GLOSSARY `oracle-ai` entry."""

    event_kind: Literal["oracle_mode_detected"] = "oracle_mode_detected"


class ValidatorModeDetected(AuditEventBase):
    """Validator-mode pattern detected per `arch/sparring.md` §8 + locked
    GLOSSARY `validator-ai` entry."""

    event_kind: Literal["validator_mode_detected"] = "validator_mode_detected"


# ---------------------------------------------------------------------------
# Error categories (§11 sparring error categories)
# ---------------------------------------------------------------------------


class SparringError(Exception):
    """Base for all sparring class errors per `arch/sparring.md` §11.

    Per-shape error semantics (§11 + §14): practitioner-shape fail-closed
    (defensibility-critical; ≥1 sparring-event per claim mandatory);
    autonomous-business-shape fail-open with alert (continuity prioritized);
    personal-OS-shape fail-open (lightweight; degradation acceptable).
    """


class SparringValidationError(SparringError):
    """Architecturally-encoded sub-mechanism missing or invalid per
    `arch/sparring.md` §11.

    Counter-argument missing; confidence not provided; reasoning insufficient;
    selective-friction policy not satisfied. Composes with per-sub-mechanism
    `*Missing` events (event records the failure in audit-trail; this error
    is raised at validation site).
    """


class SparringSchemaError(SparringError):
    """Output schema mismatch per `arch/sparring.md` §11.

    Pydantic validation failed at substrate Surface §D structured output
    validation boundary; impl-level. Composes with substrate
    `StructuredOutputValidation` (substrate raises after auto-retry
    exhausted)."""


class SparringRetryExhaustedError(SparringError):
    """Orchestrator retry-count exceeded per `arch/sparring.md` §11.

    Bypass-with-reason path activated OR shape-policy-mandated fail-closed
    escalation per `SparringPolicy.fail_closed` + `retry_budget`."""


class SparringHeuristicError(SparringError):
    """Heuristic detection failure per `arch/sparring.md` §11.

    Anti-sycophancy threshold corrupted; impl-internal. Behaviorally-
    enforced sub-mechanism heuristic-detection state issue."""


class SparringPolicyError(SparringError):
    """Shape policy declaration invalid per `arch/sparring.md` §11.

    Activation matrix references unknown sub-mechanism; threshold value
    out of range; retry budget negative. Caught at workspace boot per §5
    activation matrix validation."""


# ---------------------------------------------------------------------------
# Sub-mechanism Sub-Protocols (§2; 8 atomic mechanism contracts)
#
# Per `arch/sparring.md` §2: each sub-mechanism declares its own atomic
# Surface (the mechanism's interface contract). Per §6 mechanism-class
# structural reconciliation: skill code targeting sub-mechanism Surface
# contracts is portable across realizations within shape; skill code
# reaching realization-internal heuristic-thresholds is realization-pinned.
# ---------------------------------------------------------------------------


@runtime_checkable
class CounterArgumentSubMechanism(Protocol):
    """Architecturally-encoded sub-mechanism A per `arch/sparring.md` §2.A.

    Skill outputs in sparring-mode declare a required counter-argument
    category; substrate Surface §D structured output validation enforces
    presence + min-content. Missing fails validation; orchestrator retries
    per `SparringPolicy.retry_budget`.
    """

    def validate(self, output: Any, claim_id: str) -> CounterArgument:
        """Validate sparring-mode output declares a counter-argument.

        Returns the validated `CounterArgument` payload on success; raises
        on missing/invalid.

        Raises:
            SparringValidationError: counter-argument missing or below
                min-content threshold.
            SparringSchemaError: schema mismatch at validation boundary.
        """
        ...


@runtime_checkable
class ConfidenceCalibrationSubMechanism(Protocol):
    """Architecturally-encoded sub-mechanism B per `arch/sparring.md` §2.B.

    Skill outputs in sparring-mode declare a required confidence category
    (typed enum: high / medium / low) + accompanying basis-of-confidence;
    schema-validated.
    """

    def validate(self, output: Any, claim_id: str) -> ConfidenceDeclaration:
        """Validate sparring-mode output declares confidence + basis.

        Raises:
            SparringValidationError: confidence missing or basis below
                min-content threshold.
        """
        ...


@runtime_checkable
class VisibleReasoningSubMechanism(Protocol):
    """Architecturally-encoded sub-mechanism C per `arch/sparring.md` §2.C.

    Skill outputs in sparring-mode declare required reasoning category
    (chain of inference, not just verdict); min-content enforced.
    """

    def validate(self, output: Any, claim_id: str) -> VisibleReasoning:
        """Validate sparring-mode output declares chain-of-inference reasoning.

        Raises:
            SparringValidationError: reasoning missing or below min-content.
        """
        ...


@runtime_checkable
class SelectiveFrictionSubMechanism(Protocol):
    """Architecturally-encoded sub-mechanism D per `arch/sparring.md` §2.D.

    Selective-friction fires per claim-ambiguity threshold. Threshold is
    shape-policy-mandated (gate-dispatched parameter via
    `SparringPolicy.selective_friction_threshold`). Architectural
    commitment: per-shape threshold declaration in policy bundle; impl
    applies threshold uniformly.
    """

    def evaluate(self, claim_id: str, ambiguity_score: float) -> SelectiveFrictionDecision:
        """Evaluate per-claim ambiguity against shape-policy threshold;
        return firing decision."""
        ...


@runtime_checkable
class AntiSycophancySubMechanism(Protocol):
    """Behaviorally-enforced sub-mechanism E per `arch/sparring.md` §2.E.

    Heuristic detection compares current skill output against prior turn
    for soften-without-evidence pattern. Threshold + detection mechanism
    is impl-specific. Architectural-level: heuristic fires; emits event
    when detected.
    """

    def detect(self, current_output: str, prior_output: str | None) -> bool:
        """Detect soften-without-evidence pattern; emits
        `AntiSycophancyFlagRaised` event when True returned."""
        ...


@runtime_checkable
class AsymmetricKnowledgeRespectSubMechanism(Protocol):
    """Behaviorally-enforced sub-mechanism F per `arch/sparring.md` §2.F.

    Declarative ("I'm drawing on X; local context Y might change this").
    Too discretionary to schema-enforce; AI applies at judgment time.
    """

    def emit(self, claim_id: str, context: dict[str, Any]) -> None:
        """Record asymmetric-knowledge-respect declaration; emits
        `AsymmetricKnowledgeRespected` event."""
        ...


@runtime_checkable
class CommitToRecommendationsSubMechanism(Protocol):
    """Behaviorally-enforced sub-mechanism G per `arch/sparring.md` §2.G.

    Context-dependent enforcement (sometimes a question IS the right move;
    sometimes a commit is). AI applies per claim.
    """

    def emit(self, claim_id: str, recommendation: str) -> None:
        """Record per-claim recommendation commitment; emits
        `RecommendationCommitted` event."""
        ...


@runtime_checkable
class WhatsMissingCheckpointSubMechanism(Protocol):
    """Behaviorally-enforced sub-mechanism H per `arch/sparring.md` §2.H.

    Phase B layered review checkpoint; structural in skill body but content
    is judgment-applied.
    """

    def emit(self, claim_id: str, coverage_gaps: list[str]) -> None:
        """Record what's-missing checkpoint application; emits
        `WhatsMissingChecked` event with `coverage_gaps` in `details`."""
        ...


# ---------------------------------------------------------------------------
# Sparring mechanism class Surface — aggregating Protocol exposing the 8
# sub-mechanism contracts + class-level lifecycle
# ---------------------------------------------------------------------------


@runtime_checkable
class SparringProtocol(Protocol):
    """The Sparring mechanism class Surface (Phase 6.1 Mode 3 spec).

    Per `arch/sparring.md` §6 mechanism-class structural reconciliation:
    the Surface is the aggregation of 8 sub-mechanism Surfaces (each its
    own atomic interface contract per §2); per-shape policy bundle declares
    activation matrix + thresholds + retry budget; per-sub-mechanism
    realizations live within skill execution lifecycle.

    Distinct from Pattern A protocols (substrate / adapter / quality-gate)
    per §6: sparring has NO whole-class alternative architectures —
    sub-mechanism realization variation only.

    Cardinality (§9): 8 sub-mechanisms in the class (fixed at framework-
    mechanism layer); 0-8 active per workspace per shape policy activation
    matrix; ≥1 sparring-event per claim mandatory in practitioner-shape.

    Per §10: sparring sub-mechanisms run within skill execution lifecycle
    (no separate sparring-impl boot/shutdown beyond sub-mechanism schema
    registration via substrate Surface §D at substrate boot). The
    `from_shape_policy` / `is_ready` / `shutdown` methods integrate with
    workspace-level lifecycle via shape policy load + workspace boot.

    Per §14 cross-shape policy variation: per-shape activation matrix is
    PRIMARY conditional. Practitioner-shape activates all 8; autonomous-
    business-shape activates 4-6 per business policy; personal-OS-shape
    activates 1-3 per user preference.
    """

    # ------------------------------------------------------------------
    # Lifecycle (§9 + composition with substrate boot per §10)
    # ------------------------------------------------------------------

    @classmethod
    async def from_shape_policy(cls, policy: SparringPolicy) -> "SparringProtocol":
        """Instantiate sparring class per active shape's policy bundle.

        Loads activation matrix + thresholds + retry budget; resolves
        per-sub-mechanism realizations (architecturally-encoded sub-
        mechanisms 1-4 leverage substrate Surface §D structured output
        validation; behaviorally-enforced sub-mechanisms 5-8 apply skill
        body prose conventions + heuristic-detection emission).

        Raises:
            SparringPolicyError: activation matrix references unknown
                sub-mechanism; threshold value out of range.
        """
        ...

    @property
    def is_ready(self) -> bool:
        """True after sub-mechanism realizations resolved + activation
        matrix validated. Once True, `run_round()` accepts per-claim
        sparring rounds."""
        ...

    async def shutdown(self) -> None:
        """Sparring shutdown — N/A separate phases per §10. Provided for
        Surface-uniformity with mechanism-class peers (audit / quality-
        gate). Releases per-sub-mechanism state held by realizations
        (e.g., heuristic-detection state for anti-sycophancy)."""
        ...

    # ------------------------------------------------------------------
    # Sub-mechanism accessors (§2; 8 sub-Protocols)
    # ------------------------------------------------------------------

    @property
    def counter_argument(self) -> CounterArgumentSubMechanism:
        """Architecturally-encoded sub-mechanism A per `arch/sparring.md` §2.A."""
        ...

    @property
    def confidence_calibration(self) -> ConfidenceCalibrationSubMechanism:
        """Architecturally-encoded sub-mechanism B per `arch/sparring.md` §2.B."""
        ...

    @property
    def visible_reasoning(self) -> VisibleReasoningSubMechanism:
        """Architecturally-encoded sub-mechanism C per `arch/sparring.md` §2.C."""
        ...

    @property
    def selective_friction(self) -> SelectiveFrictionSubMechanism:
        """Architecturally-encoded sub-mechanism D per `arch/sparring.md` §2.D."""
        ...

    @property
    def anti_sycophancy(self) -> AntiSycophancySubMechanism:
        """Behaviorally-enforced sub-mechanism E per `arch/sparring.md` §2.E."""
        ...

    @property
    def asymmetric_knowledge_respect(self) -> AsymmetricKnowledgeRespectSubMechanism:
        """Behaviorally-enforced sub-mechanism F per `arch/sparring.md` §2.F."""
        ...

    @property
    def commit_to_recommendations(self) -> CommitToRecommendationsSubMechanism:
        """Behaviorally-enforced sub-mechanism G per `arch/sparring.md` §2.G."""
        ...

    @property
    def whats_missing_checkpoint(self) -> WhatsMissingCheckpointSubMechanism:
        """Behaviorally-enforced sub-mechanism H per `arch/sparring.md` §2.H."""
        ...

    # ------------------------------------------------------------------
    # Per-claim sparring round entry point (§9 cardinality)
    # ------------------------------------------------------------------

    async def run_round(
        self,
        claim_id: str,
        skill_output: Any,
        prior_output: str | None = None,
    ) -> SparringRoundResult:
        """Run a sparring round for a claim per `arch/sparring.md` §1 + §9.

        Aggregates per-active-sub-mechanism validation/emission per
        activation matrix. Architecturally-encoded sub-mechanisms 1-4
        validate skill_output via substrate Surface §D; behaviorally-
        enforced sub-mechanisms 5-8 apply at judgment time + emit
        per-completion events.

        Orchestrator retry semantics: validation failures retry up to
        `SparringPolicy.retry_budget` then escalate per shape policy
        (`fail_closed` → `SparringRetryExhaustedError`; otherwise
        bypass-with-reason path).

        Emits `SparringRoundCompleted` on success; per-sub-mechanism
        events per activation matrix; `SparringBypassWithReason` /
        `SparringValidationRetry` per orchestrator path.

        Raises:
            SparringValidationError: architecturally-encoded sub-mechanism
                missing/invalid (after retries; fail-closed shapes).
            SparringRetryExhaustedError: orchestrator retry-count exceeded
                + fail-closed escalation per `SparringPolicy.fail_closed`.
            SparringSchemaError: substrate-side structured output
                validation failed.
        """
        ...

    # ------------------------------------------------------------------
    # Failure-mode detection (§8 — feeds quality-gate axis-2 enforcement)
    # ------------------------------------------------------------------

    def report_failure_mode(self, mode: FailureMode, claim_id: str | None) -> None:
        """Emit a `failure_mode_detected` event per `arch/sparring.md` §8.

        Sparring impl reports clustered sub-mechanism violations as
        axis-2 failure modes (answer-machine / oracle / validator). Events
        feed quality-gate's axis-2 enforcement per `arch/quality-gate.md`
        §2.B per-axis signal ingestion.

        Emits `AnswerMachineDetected` / `OracleModeDetected` /
        `ValidatorModeDetected` per `mode` discriminator.
        """
        ...
