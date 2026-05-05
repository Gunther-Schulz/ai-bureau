"""Workflow descriptor + instance schemas — per `arch/workflow-work-unit.md`.

Per `arch/workflow-work-unit.md` §2.1 + §2.2 + §16: WorkflowDescriptor +
workflow_instance Pydantic schemas land Phase 6 (Mode 3 spec). This
module defines the typed contracts for the workflow DEFINITION manifest
+ workflow_instance entity + workflow_instance lifecycle event-kind
catalog (§13) + WorkflowError categories (§7).

Per §1: workflow is bipartite Pattern B with optional applicability
(DEFINITION at Framework C via specialist's bundle; INSTANCE at Owner B
as workflow_instance entity). Per §3 always-present asymmetry: workflow_
instance is OPTIONAL overlay (engages only when codified pattern
applies); reciprocal to work-unit's always-present container per
`pbs.manifests.work_unit`.

Per §3 cardinality asymmetry: 1 work-unit per workflow_instance
(workflow_instance has exactly 1 work-unit attribution); N
workflow_instances per work-unit (potentially across specialists).

Per §3 snapshot pattern (cross-primitive structural commitment):
workflow_instance uses `definition_snapshot` at workflow-start for
defensibility-preservation across specialist version bumps (mirrors
work-unit instance `kind_snapshot` per §2.2).

Per §1 cross-axis claim: workflow is the **axis-1 PRIMARY anchor** —
workflow is what intertwined AI intertwines WITH per `glossary/workflow.
md` ("Workflow as precondition" implication per VISION).
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Workflow definition manifest schema (§2.1)
# ---------------------------------------------------------------------------


class PhaseAuthorityRequirement(BaseModel):
    """Per-phase authority requirement per `arch/workflow-work-unit.md` §2.1.

    Workflow definition declares per-phase authority requirements per
    `glossary/workflow.md` composes-with authority-binding row; per-shape
    policy declares trust model parameterizing authority-binding
    satisfaction per §8 (e.g., review → send transition requires
    practitioner-only authority per defensibility-critical in
    practitioner-shape).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    phase: str
    """Phase identifier; must be in `WorkflowDescriptor.phases`."""

    required_authority: str
    """Authority requirement (e.g., `practitioner-only`, `under-supervision-
    permitted`, `programmatic`); per-shape policy declares trust model
    interpretation."""


class WorkflowDescriptor(BaseModel):
    """Workflow DEFINITION manifest per `arch/workflow-work-unit.md` §2.1.

    Reusable pattern (specialist-bundled): "how does B-Plan-Begründung
    drafting actually proceed?" or "how does a legal brief get from
    intake to filing?" — sequence of activities + artifacts + decisions +
    handoffs + per-phase authority requirements. Optional structural
    overlay per `glossary/workflow.md`: workflow primitive engages
    OPTIONALLY — only when work follows a codified pattern.

    Per §1: DEFINITION lives at `Framework C scope` via specialist's
    bundle (workflow inherits Framework C placement via specialist
    composition, NOT as standalone framework primitive). Versioning
    inherits specialist version per §5 workflow definition lifecycle.

    Per §6 logic placement: workflow manifest body content is Mode 1
    production-runtime LLM-MD (workspace AI reads at activation + at
    workflow-start); THIS Pydantic shape is Mode 3 hybrid spec layer.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    """Workflow name local to specialist; specialist-namespace per `arch/
    specialist-skill.md` §10 (fully-qualified `specialist-name:workflow-
    name`)."""

    version: str
    """Inherits specialist version per §5 workflow definition lifecycle
    (workflow definition immutable per specialist version; specialist
    version bump may include workflow definition changes)."""

    phases: tuple[str, ...]
    """Phase identifiers in sequence (e.g., `intake → research → draft →
    review → send → response_handling` per `profiles/L5a-planner-pbs-
    schulz.md` lines 22-29 B-Plan workflow). Ordered tuple — phase
    progression follows tuple order per §13 workflow_instance state
    machine."""

    phase_authority_requirements: tuple[PhaseAuthorityRequirement, ...] = ()
    """Per-phase authority binding per §2.1 + `glossary/workflow.md`
    composes-with authority-binding row. Empty tuple = no per-phase
    authority constraints (default-permissive per shape policy)."""

    triggered_skills: dict[str, tuple[str, ...]] = Field(default_factory=dict)
    """Per-phase skill triggers per §2.1; key = phase identifier; value =
    tuple of skill references in containing specialist by local name +
    cross-specialist via fully-qualified `specialist-name:skill-name` per
    `arch/specialist-skill.md` §3 + §10. Empty dict = no per-phase skill
    triggers (skills fire on independent triggers per substrate Surface
    §G)."""

    optional_overlay_marker: bool = True
    """Always-true at framework level per §2.1 + `glossary/workflow.md`
    optional applicability (workflow primitive engages OPTIONALLY);
    documented for clarity (not configurable; immutable architectural
    commitment)."""


# ---------------------------------------------------------------------------
# Workflow_instance state machine (§13)
# ---------------------------------------------------------------------------


class WorkflowInstanceLifecycleState(StrEnum):
    """Workflow_instance lifecycle state per `arch/workflow-work-unit.md`
    §13 state machine.

    Per `glossary/workflow.md` lifecycle: `running` ↔ `suspended` (pause/
    resume); `running | suspended → completed | abandoned | failed`
    (terminal). Naming aligned with work-unit instance + practitioner
    `lifecycle_state` per cross-pattern coherence per §13.
    """

    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# WorkflowDefinitionSnapshot (§3 snapshot pattern; §2.2 definition_snapshot)
# ---------------------------------------------------------------------------


class WorkflowDefinitionSnapshot(BaseModel):
    """Snapshot of workflow DEFINITION at workflow-start per `arch/workflow-
    work-unit.md` §3 snapshot pattern + §2.2.

    Preserves defensibility per `glossary/workflow.md` lifecycle
    ("preserves defensibility — execution reproducible per original
    definition"); cross-primitive snapshot pattern per §3 (mirrors
    work-unit instance `kind_snapshot` per `pbs.manifests.work_unit`).

    Captures the workflow definition shape at the moment workflow_instance
    started so version bumps to the underlying workflow definition don't
    invalidate in-flight workflow_instance state.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    """Specialist-namespaced workflow name (`specialist-name:workflow-
    name`)."""

    version: str
    """Workflow version at snapshot moment (inherits specialist version)."""

    phases: tuple[str, ...]
    """Phases at snapshot moment; preserves phase progression semantics
    across specialist version bumps."""

    phase_authority_requirements: tuple[PhaseAuthorityRequirement, ...] = ()
    triggered_skills: dict[str, tuple[str, ...]] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# WorkflowInstance (§2.2 schema)
# ---------------------------------------------------------------------------


class PhaseTransition(BaseModel):
    """Workflow_instance phase transition record per `arch/workflow-work-
    unit.md` §2.2 phase_history field.

    Records per-phase progression with timestamp + actor + audit event
    reference for defensibility-test reconstruction (Cond #2 reasoning
    chain reconstructible per `arch/claim-defensibility.md` §2.2).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    from_phase: str
    to_phase: str
    actor_id: str
    """Identity of actor who triggered the transition (typically session-
    bound practitioner-record-id per `arch/practitioner.md` §4)."""
    audit_event_id: str
    """Reference to the AuditEvent recording the transition (per §13
    `workflow_phase_transitioned` event-kind)."""


class WorkflowInstance(BaseModel):
    """Workflow_instance per `arch/workflow-work-unit.md` §2.2.

    Specific execution against a work-unit (Owner B). The primitive
    engages OPTIONALLY — only when work follows a codified pattern; ad-
    hoc work without codified pattern engages session + work-unit + skill
    + claim + event WITHOUT workflow_instance per §3 ad-hoc work first-
    class commitment.

    Per §3 cardinality asymmetry: workflow_instance has exactly 1 work-
    unit attribution (`attached_work_unit_id` is single reference); the
    work-unit may have N workflow_instances attached per `pbs.manifests.
    work_unit`.

    Per `MAINTENANCE.md` TOP-LEVEL SCOPE: per-deployment workflow_instance
    entity-md authoring lives at deployment-instance, NOT framework. THIS
    schema describes the SHAPE; per-deployment storage convention is
    Phase 6 deployment territory.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    """workflow_instance identifier; per-deployment uniqueness convention
    (deployment-side prose-rule pattern per archived governance-and-
    identity-sourcing greenfield-evaluated per §15)."""

    definition_snapshot: WorkflowDefinitionSnapshot
    """Snapshot of workflow definition at workflow-start per §3 snapshot
    pattern + §2.2."""

    definition_ref: str
    """Fully-qualified `specialist-name:workflow-name@version` per `arch/
    specialist-skill.md` §10 specialist-namespace."""

    current_phase: str
    """References definition `phases` list; current progression position."""

    lifecycle_state: WorkflowInstanceLifecycleState
    """Per §13 state machine (`running` ↔ `suspended`; terminal `completed`
    | `abandoned` | `failed`)."""

    attached_work_unit_id: str
    """work-unit instance attribution; cardinality asymmetry (1 work-unit
    per workflow_instance per §3)."""

    bound_practitioner_id: str
    """practitioner-RECORD attribution per `arch/practitioner.md` §4 (each
    session binds to ONE practitioner-record; workflow_instance attribution
    composes through session-bound practitioner)."""

    phase_history: tuple[PhaseTransition, ...] = ()
    """Phase transitions with timestamps + actor + audit event references
    per §2.2 phase_history field. Empty tuple at workflow_started;
    accumulates per `workflow_phase_transitioned` event."""


# ---------------------------------------------------------------------------
# Workflow_instance event-kind catalog (§13)
# ---------------------------------------------------------------------------


class WorkflowStarted(AuditEventBase):
    """Workflow_instance created per `arch/workflow-work-unit.md` §13.

    `details` carries `definition_ref` + `attached_work_unit_id` +
    `bound_practitioner_id` per §2.2 schema. Emitted at runtime when
    codified pattern applies to new work-unit instance.
    """

    event_kind: Literal["workflow_started"] = "workflow_started"


class WorkflowPhaseTransitioned(AuditEventBase):
    """Workflow_instance phase transition per `arch/workflow-work-unit.md`
    §13.

    `details` carries `from_phase` + `to_phase` per archived audit-trail-
    v2 `details:` payload precedent (greenfield-evaluated per §15).
    Single event-kind for all transitions (NOT separate event-kinds per
    transition; minimal event-kind catalog growth).
    """

    event_kind: Literal["workflow_phase_transitioned"] = "workflow_phase_transitioned"


class WorkflowSuspended(AuditEventBase):
    """Workflow_instance running → suspended per `arch/workflow-work-unit.
    md` §13."""

    event_kind: Literal["workflow_suspended"] = "workflow_suspended"


class WorkflowResumed(AuditEventBase):
    """Workflow_instance suspended → running per `arch/workflow-work-unit.
    md` §13."""

    event_kind: Literal["workflow_resumed"] = "workflow_resumed"


class WorkflowCompleted(AuditEventBase):
    """Workflow_instance terminal completion per `arch/workflow-work-unit.
    md` §13."""

    event_kind: Literal["workflow_completed"] = "workflow_completed"


class WorkflowAbandoned(AuditEventBase):
    """Workflow_instance terminal abandon per `arch/workflow-work-unit.md`
    §13.

    Practitioner explicitly abandoned workflow (e.g., project cancelled
    mid-workflow). Distinct from `failed` (which carries a failure
    category).
    """

    event_kind: Literal["workflow_abandoned"] = "workflow_abandoned"


class WorkflowFailed(AuditEventBase):
    """Workflow_instance terminal failure per `arch/workflow-work-unit.md`
    §13.

    `details` carries `failure_category` per §7 error categories (e.g.,
    `WorkflowInstancePhaseTransitionViolation` /
    `WorkflowInstanceAuthorityBindingFailure` /
    `WorkflowInstanceOrphanReactivationFailure`).
    """

    event_kind: Literal["workflow_failed"] = "workflow_failed"


# ---------------------------------------------------------------------------
# Error categories (§7 workflow-error categories)
# ---------------------------------------------------------------------------


class WorkflowError(Exception):
    """Base for all workflow-class errors per `arch/workflow-work-unit.md`
    §7.

    Per-shape error semantics (§8): practitioner-shape strict (state
    transitions audit-emitted; rollback prohibited per defensibility —
    only re-start a new workflow_instance); autonomous-business-shape
    tolerant (auto-rollback per business retry policy permitted);
    personal-OS-shape tolerant.
    """


class WorkflowDefinitionValidation(WorkflowError):
    """Manifest frontmatter fails schema validation per §7.

    Missing required fields; invalid enum values; phases list malformed;
    phase_authority_requirements references undefined phase.
    """


class WorkflowInstancePhaseTransitionViolation(WorkflowError):
    """Illegal state transition per §7.

    Terminal state → running; phase out-of-sequence per workflow
    definition per §13 state machine.
    """


class WorkflowInstanceAuthorityBindingFailure(WorkflowError):
    """Phase transition requires authority not present per §7.

    Per `phase_authority_requirements` (e.g., review phase requires
    practitioner-only authority but session bound to under-supervision
    practitioner per `arch/practitioner.md` §2.2 signing_authority
    enum).
    """


class WorkflowInstanceOrphanReactivationFailure(WorkflowError):
    """Specialist reactivated but workflow_instance state can't resume
    per §7.

    Version incompatibility between `definition_snapshot` and current
    specialist version per §13 orphan handling. Surfaces when specialist
    deactivated (workspace `specialists_active` change) → existing
    workflow_instances orphaned → reactivation hits version-incompatibility.
    """

