"""Work-unit kind + instance descriptor schemas — per `arch/workflow-work-
unit.md`.

Per `arch/workflow-work-unit.md` §2.3 + §2.4 + §16: WorkUnitKindDescriptor
+ work-unit instance Pydantic schemas land Phase 6 (Mode 3 spec). This
module defines the typed contracts for the work-unit kind DEFINITION
manifest + work-unit instance entity + work-unit lifecycle event-kind
catalog (§13) + WorkUnitError categories (§7).

Per §1: work-unit is bipartite Pattern B (KIND DEFINITION at Framework C
via specialist's bundle; INSTANCE at Owner B as work-unit instance
entity). Per §3 always-present asymmetry: work-unit is ALWAYS-PRESENT
container (every accountability-bearing piece of work IS a work-unit) —
reciprocal to workflow's optional applicability.

Per §3 cardinality asymmetry: 1 work-unit per workflow_instance
(workflow_instance has exactly 1 work-unit attribution); N
workflow_instances per work-unit (potentially across specialists per
`glossary/work-unit.md`).

Per §3 snapshot pattern (cross-primitive structural commitment): work-
unit instance uses `kind_snapshot` at creation for defensibility-
preservation across specialist version bumps (mirrors
workflow_instance's `definition_snapshot` per §2.4).

Per §13 archival-as-default destruction: cross-pattern coherence with
`arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 + `arch/
claim-defensibility.md` §13 (same `instance_content_dissolution_policy`
field per workspace.md).
"""

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Default work-unit lifecycle states (§13 + §2.3 kind extensibility)
# ---------------------------------------------------------------------------


class DefaultWorkUnitLifecycleState(StrEnum):
    """Default work-unit lifecycle states per `arch/workflow-work-unit.md`
    §13 work-unit instance state machine.

    Kind-default; per-kind extensibility via `WorkUnitKindDescriptor.
    lifecycle_states` field per §2.3 (e.g., `audit` kind may add
    `under-review` between `in-progress` and `completed`; `manuscript`
    kind may add `revision` between `completed` and `sent`).

    Default transitions per §13: initiated → in-progress; in-progress →
    completed | sent; completed → sent | archived; sent → archived.
    """

    INITIATED = "initiated"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    SENT = "sent"
    ARCHIVED = "archived"


# ---------------------------------------------------------------------------
# WorkUnitKindDescriptor (§2.3 manifest schema)
# ---------------------------------------------------------------------------


class WorkUnitKindDescriptor(BaseModel):
    """Work-unit KIND DEFINITION manifest per `arch/workflow-work-unit.md`
    §2.3.

    Specialist-defined discriminator + per-kind structural conventions
    (e.g., `project` for planning bureau, `matter` for legal practice,
    `case` for medical practice, `engagement` for consulting,
    `manuscript` for research lab, `audit` for accounting). Always-
    present container per `glossary/work-unit.md`: every accountability-
    bearing piece of work IS a work-unit.

    Per §1: KIND DEFINITION lives at `Framework C scope` via specialist's
    bundle (work-unit inherits Framework C placement via specialist
    composition, NOT as standalone framework primitive). Versioning
    inherits specialist version per §5 work-unit kind lifecycle.

    Per §6 logic placement: kind manifest body content is Mode 1
    production-runtime LLM-MD (workspace AI reads at activation + at
    instance creation); THIS Pydantic shape is Mode 3 hybrid spec layer.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    """Kind discriminator per §2.3 (`project` / `matter` / `case` /
    `engagement` / `manuscript` / `audit` / `task` / `order` per
    `glossary/work-unit.md` cross-archetype illustration); specialist-
    namespace per `arch/specialist-skill.md` §10 (fully-qualified
    `specialist-name:kind-name`)."""

    version: str
    """Inherits specialist version per §5 work-unit kind lifecycle (work-
    unit kind immutable per specialist version; changes require specialist
    version bump)."""

    lifecycle_states: tuple[str, ...] = (
        DefaultWorkUnitLifecycleState.INITIATED,
        DefaultWorkUnitLifecycleState.IN_PROGRESS,
        DefaultWorkUnitLifecycleState.COMPLETED,
        DefaultWorkUnitLifecycleState.SENT,
        DefaultWorkUnitLifecycleState.ARCHIVED,
    )
    """Kind-specific state machine per §2.3; default = initiated /
    in-progress / completed / sent / archived per `glossary/work-unit.md`
    lifecycle. Per-kind extensibility (e.g., `audit` adds `under-review`).
    Stored as str tuple to permit kind-specific extensions beyond the
    default enum.
    """

    artifact_attachment_shape: dict[str, Any] = Field(default_factory=dict)
    """Per-kind structural conventions (drafts / references / sent
    versions); INPUT from archived entity-md-scope-model-restructure.md
    greenfield-evaluated per §15. Free-form per Phase 6 spec; per-kind
    schema standardization per W3 watch-list."""

    audit_attribution_semantics: dict[str, Any] = Field(default_factory=dict)
    """Per-kind event scoping rules (which events scope to this kind's
    instances); per `glossary/work-unit.md` "events scoped to work-unit
    per archived audit-trail-v2 schema" greenfield-evaluated per §15."""


# ---------------------------------------------------------------------------
# WorkUnitKindSnapshot (§3 snapshot pattern; §2.4 kind_snapshot field)
# ---------------------------------------------------------------------------


class WorkUnitKindSnapshot(BaseModel):
    """Snapshot of work-unit KIND DEFINITION at instance creation per
    `arch/workflow-work-unit.md` §3 snapshot pattern + §2.4.

    Preserves audit-trail integrity if specialist version bumps mid-
    instance-lifetime (mirrors workflow_instance `definition_snapshot`
    pattern per §2.2). Per `glossary/work-unit.md`: "kind is FIXED at
    creation; pivot creates new work-unit" — kind_snapshot freezes the
    kind structure at the moment the instance was created.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind_name: str
    """Specialist-namespaced kind name (`specialist-name:kind-name`)."""

    kind_version: str
    """Kind version at snapshot moment (inherits specialist version)."""

    lifecycle_states: tuple[str, ...]
    """Kind state machine at snapshot moment; preserves transitions
    semantics across specialist version bumps."""

    artifact_attachment_shape: dict[str, Any] = Field(default_factory=dict)
    audit_attribution_semantics: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# WorkUnitInstance (§2.4 schema)
# ---------------------------------------------------------------------------


class WorkUnitAttribution(BaseModel):
    """Per-instance practitioner-RECORD authorship per `arch/workflow-work-
    unit.md` §2.4.

    Composes through practitioner-RECORD per `glossary/work-unit.md`
    composes-with practitioner row; multi-practitioner-shape variants =
    shape-policy per `arch/practitioner.md` §3 + §8.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    primary_practitioner_id: str
    """Primary accountable practitioner-record id per axis-3 defensibility
    (defensibility test asks "will THIS practitioner defend THIS work-
    unit's outputs?" per `glossary/practitioner.md`)."""

    co_practitioner_ids: tuple[str, ...] = ()
    """Multi-practitioner co-attribution per `arch/practitioner.md` §3
    cardinality matrix (partnership-shape = N; legal-entity-firm-shape =
    N under firm context). Each practitioner-record id present in the
    workspace's `practitioners` list."""


class WorkUnitInstance(BaseModel):
    """Work-unit instance per `arch/workflow-work-unit.md` §2.4.

    Specific deployment-bound artifact-container at Owner B. Always-
    present anchor per `glossary/work-unit.md`: every accountability-
    bearing work IS a work-unit (no optional-overlay discount; reciprocal
    to workflow's optional applicability).

    Carries lifecycle state (initiated → in-progress → completed / sent /
    archived per default; per-kind extensible), associated artifacts
    (drafts, references, sent versions), decisions made, sources cited,
    sparring outcomes, and audit-trail attribution (events emitted scoped
    to this instance).

    Per §3 cardinality asymmetry: N workflow_instances per work-unit
    (potentially across specialists per `glossary/work-unit.md`); 1
    work-unit per workflow_instance (enforced by workflow_instance side).

    Per `MAINTENANCE.md` TOP-LEVEL SCOPE: per-deployment work-unit
    instance entity-md authoring lives at deployment-instance, NOT
    framework. THIS schema describes the SHAPE; per-deployment storage
    convention is Phase 6 deployment territory.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    """Per-deployment uniqueness convention (deployment-side prose-rule
    pattern per archived governance-and-identity-sourcing decision 3
    greenfield-evaluated per §15)."""

    kind_snapshot: WorkUnitKindSnapshot
    """CREATION snapshot per §3 snapshot pattern + `glossary/work-unit.md`
    lifecycle ("preserves audit-trail integrity if specialist version
    bumps mid-instance-lifetime; mirrors workflow_instance definition-
    snapshot pattern")."""

    kind_ref: str
    """Fully-qualified `specialist-name:kind-name@version` per `arch/
    specialist-skill.md` §10 specialist-namespace."""

    lifecycle_state: str
    """References kind `lifecycle_states` enum; FIXED kind at creation
    per `glossary/work-unit.md` ("kind is FIXED at creation; pivot
    creates new work-unit"). String typing permits per-kind extensible
    states beyond the default enum."""

    attached_workflow_instances: tuple[str, ...] = ()
    """N workflow_instances per cardinality asymmetry per §3 (potentially
    across specialists per `glossary/work-unit.md`). Empty tuple = ad-hoc
    work first-class per §3."""

    owning_specialist_id: str
    """Per `glossary/work-unit.md` composes-with specialist row (work-unit
    instance is owned by deployed specialist instance). Cross-specialist
    work-unit ATTACHMENT permitted; ownership mutation PROHIBITED per §3
    cross-specialist composition rules."""

    attribution: WorkUnitAttribution
    """practitioner-RECORD authorship per §2.4 + `glossary/work-unit.md`
    composes-with practitioner row."""

    predecessor_work_unit_id: str | None = None
    """Pivot link per `glossary/work-unit.md` ("kind is FIXED at creation;
    pivot creates new work-unit linked via predecessor_id"); set when this
    instance was created via pivot from a prior work-unit. Per §13
    `work_unit_pivoted` event-kind."""


# ---------------------------------------------------------------------------
# Work-unit instance event-kind catalog (§13)
# ---------------------------------------------------------------------------


class WorkUnitCreated(AuditEventBase):
    """Work-unit instance created per `arch/workflow-work-unit.md` §13.

    `details` carries `kind_ref` + `owning_specialist_id` + `attribution`
    per §2.4 work-unit instance schema. Emitted at runtime when
    accountability-bearing work begins (instance created against active
    kind).
    """

    event_kind: Literal["work_unit_created"] = "work_unit_created"


class WorkUnitStateTransitioned(AuditEventBase):
    """Work-unit lifecycle state transition per `arch/workflow-work-unit.md`
    §13.

    `details` carries `from_state` + `to_state` per archived audit-trail-
    v2 `details:` payload precedent (greenfield-evaluated per §15).
    Single event-kind for all transitions (NOT separate event-kinds per
    transition; minimal event-kind catalog growth).
    """

    event_kind: Literal["work_unit_state_transitioned"] = "work_unit_state_transitioned"


class WorkUnitCompleted(AuditEventBase):
    """Work-unit terminal completion per `arch/workflow-work-unit.md` §13."""

    event_kind: Literal["work_unit_completed"] = "work_unit_completed"


class WorkUnitSent(AuditEventBase):
    """Work-unit terminal send per `arch/workflow-work-unit.md` §13.

    Practitioner-shape signed-claim emission moment per `glossary/
    authority-binding.md` line 35 ("every signature_applied event records
    actor_kind: human + practitioner identity for legal-bind moments").
    Per §8 cross-shape policy variation: practitioner-shape send/archive
    = practitioner-only authority per defensibility-critical.
    """

    event_kind: Literal["work_unit_sent"] = "work_unit_sent"


class WorkUnitArchived(AuditEventBase):
    """Work-unit terminal archive per `arch/workflow-work-unit.md` §13.

    Preserves audit-trail attribution per `arch/practitioner.md` §13
    archival-as-default cross-pattern coherence. Per §13 cross-pattern
    destruction: workspace.md `instance_content_dissolution_policy`
    declares archive vs delete-with-audit policy.
    """

    event_kind: Literal["work_unit_archived"] = "work_unit_archived"


class WorkUnitPivoted(AuditEventBase):
    """Work-unit pivot per `arch/workflow-work-unit.md` §13.

    Kind-FIXED-at-creation enforcement per `glossary/work-unit.md` ("kind
    is FIXED at creation; pivot creates new work-unit"). `details` carries
    `predecessor_work_unit_id` + new `kind_ref`; new work-unit instance
    is emitted via separate `WorkUnitCreated` event linked via
    `predecessor_work_unit_id` per §2.4.
    """

    event_kind: Literal["work_unit_pivoted"] = "work_unit_pivoted"


# ---------------------------------------------------------------------------
# Error categories (§7 work-unit-error categories)
# ---------------------------------------------------------------------------


class WorkUnitError(Exception):
    """Base for all work-unit-class errors per `arch/workflow-work-unit.md`
    §7.

    Per-shape error semantics (§8): practitioner-shape strict (defensibility-
    critical preservation; sent/archived states preserve attribution chain;
    rapid-archive prohibited under deadline per `glossary/category-
    collapse.md` axis-3 risk); autonomous-business-shape archival OR
    delete-with-audit per business policy; personal-OS-shape minimal
    lifecycle (deletion permitted per user preference).
    """


class WorkUnitKindValidation(WorkUnitError):
    """Manifest schema fail per §7.

    Missing required fields; lifecycle_states malformed;
    artifact_attachment_shape malformed.
    """


class WorkUnitKindCollision(WorkUnitError):
    """Within-specialist kind name collision per §7.

    Cross-specialist disambiguated via specialist-namespace per `arch/
    specialist-skill.md` §10 (fully-qualified `specialist-name:kind-
    name`).
    """


class WorkUnitInstanceLifecycleStateConflict(WorkUnitError):
    """State transition not in kind's `lifecycle_states` enum per §7.

    Per §13 work-unit instance state machine; kind-specific extensions
    enforced per `WorkUnitKindDescriptor.lifecycle_states` field.
    """


class WorkUnitInstancePivotViolation(WorkUnitError):
    """Attempt to switch kind mid-lifecycle per §7.

    Per `glossary/work-unit.md` "kind is FIXED at creation; pivot creates
    new work-unit"; pivot must create new work-unit linked via
    `details.predecessor_work_unit_id` per §13 `work_unit_pivoted`
    event-kind.
    """
