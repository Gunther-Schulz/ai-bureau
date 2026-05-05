"""Workspace manifest schema — per `arch/scope-model.md`.

Per `arch/scope-model.md` §3 cross-scope composition WITHIN cluster
(workspace integration): workspace IS the integration point binding all
three scopes — the architectural surface where Framework C selections +
Owner B instances + Layer A content compose at workspace deployment time.

Per `glossary/workspace.md` lines 16-18: workspace IS the deployment-
instance container that integrates framework mechanisms + shape policies
+ active specialists + practitioners + state into a coherent unit.

Per §3 workspace integration spans:
- Framework C selections (workspace.shape + workspace.substrate +
  workspace.specialists_active)
- Owner B instance ownership (workspace itself + workspace-scope managed
  entities universal/shape-policy-mandated)
- Layer A scope-resolution (workspace.scope.{domains, states} configuration
  determines which Layer A content applies)

Per §8 cross-shape policy variation: workspace.md required fields per
shape (per `arch/practitioner.md` §4 multi-practitioner authorship +
legal-entity context); shape-policy-mandated engagement-target Owner B
managed entity catalog per shape; Layer A scope configuration defaults
per shape; specialists_active recommended set per shape; substrate
selection constraints per shape.

Per §13 cross-pattern destruction (cross-pattern coherence with `arch/
specialist-skill.md` §13 + `arch/practitioner.md` §13 + `arch/workflow-
work-unit.md` §13 + `arch/claim-defensibility.md` §13): same
`instance_content_dissolution_policy` field shape across all primitive-
cluster ARCH topics.
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Workspace enums (§3 + §8 + §13)
# ---------------------------------------------------------------------------


class InstanceContentDissolutionPolicy(StrEnum):
    """Workspace dissolution destruction semantics per `arch/scope-model.md`
    §13 (cross-pattern coherence).

    Same field shape across all 4 primitive-cluster ARCH topics per cross-
    pattern coherence convention (`arch/specialist-skill.md` §13 + `arch/
    practitioner.md` §13 + `arch/workflow-work-unit.md` §13 + `arch/
    claim-defensibility.md` §13). Default = archive (preserves practitioner
    work + axis-3 authorship preservation + 6-months-later defensibility
    test re-runable); opt-in delete-with-audit may be restricted by
    per-shape policy (practitioner-shape policy may prohibit deletion-
    with-audit per defensibility-critical).
    """

    ARCHIVE = "archive"
    DELETE_WITH_AUDIT = "delete-with-audit"


class WorkspaceShapeId(StrEnum):
    """Active shape identifier per `glossary/shape.md` + `arch/scope-model.
    md` §8 cross-shape policy variation.

    Framework-baseline shapes per `arch/audit.md` §14 + `arch/sparring.md`
    §14 cross-shape policy variation precedents. Shape selection at
    workspace deployment time selects exactly one shape per `glossary/
    workspace.md`.
    """

    PRACTITIONER = "practitioner-shape"
    AUTONOMOUS_BUSINESS = "autonomous-business-shape"
    PERSONAL_OS = "personal-OS-shape"
    RESEARCH_LAB = "research-lab-shape"


# ---------------------------------------------------------------------------
# Workspace integration sub-models (§3 cross-scope composition)
# ---------------------------------------------------------------------------


class LegalEntityContext(BaseModel):
    """Firm-level legal entity context per `arch/practitioner.md` §3.

    Per `glossary/practitioner.md` "Legal-entity context (firm-level
    contracting party) lives at WORKSPACE level... not at practitioner
    level — practitioner is always a natural person". Populated for
    legal-entity-shape workspaces (firm = the legal entity contracting
    party; named practitioners sign under firm context per `arch/
    practitioner.md` §3).

    Practitioner-record references back to firm context via
    `practitioner.firm_binding: str` field per `arch/practitioner.md`
    §2.2 (populated when workspace has legal_entity_context).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    entity_name: str
    """Firm legal name (e.g., `Schulz Planning GmbH`)."""

    entity_type: str
    """Legal entity type (e.g., `GmbH` / `LLP` / `LLC` / `Inc` / sole-
    proprietorship); jurisdiction-specific per `entity_type` semantics."""

    jurisdiction: str
    """Legal jurisdiction (e.g., `DE-BB` / `DE-BY` / `US-CA`); composes
    with `WorkspaceScopeConfig.states` for Layer A jurisdiction-specific
    content."""


class WorkspaceScopeConfig(BaseModel):
    """Layer A scope configuration per `arch/scope-model.md` §3 + §8 +
    `glossary/workspace.md` composes-with Layer A row.

    `workspace.scope.{domains, states}` configuration determines which
    Layer A content applies per `glossary/layer-a-scope.md` Layer values:
    universal applies to every deployment; domain applies to deployments
    in specific domains; state applies to deployments in specific
    jurisdictions. Multiple domains/states may be active simultaneously
    per `glossary/layer-a-scope.md`.

    Per §8 cross-shape policy variation: practitioner-shape =
    {planning / naturschutz / environmental-law / baurecht} +
    {DE-BB / DE-BY / etc.}; autonomous-business / research-lab / personal-
    OS = shape-specific defaults.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    domains: tuple[str, ...] = ()
    """Active Layer A domains; effective content = universal + active-
    domains + active-states per `glossary/layer-a-scope.md`."""

    states: tuple[str, ...] = ()
    """Active Layer A jurisdictions; effective content = universal +
    active-domains + active-states per `glossary/layer-a-scope.md`."""


class AdapterBinding(BaseModel):
    """Workspace adapter binding per `arch/adapter.md` §10 per-instance
    boot/shutdown.

    Workspace declares which adapter classes + per-instance configurations
    bind at workspace boot per substrate-phase 3 (Adapter bindings load
    step) per `arch/scope-model.md` §3 workspace boot integration.

    Resolves with `arch/specialist-skill.md` §2.3 `activation_prereqs.
    adapter_bindings` per §13 boot ordering step 3 (specialists declaring
    adapter dependencies validated against workspace's adapter bindings
    list; `SpecialistAdapterDependencyUnmet` if missing).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    adapter_id: str
    """Adapter implementation id (e.g., `email-smtp` / `mcp-corpus` /
    `personio` / `microsoft-entra`)."""

    integration_class: str
    """Per-class category per `arch/adapter.md` §3 (e.g., `mcp_server` /
    `email` / `accounting` / `a2a_peer` / `file_sync` / `identity`).
    Free-form str at framework level; per-impl validation per Phase 6."""

    config: dict[str, str] = Field(default_factory=dict)
    """Per-binding configuration (per-impl semantics; secrets resolved
    per substrate / deployment)."""


# ---------------------------------------------------------------------------
# WorkspaceManifest (§3 workspace integration)
# ---------------------------------------------------------------------------


class WorkspaceManifest(BaseModel):
    """Workspace manifest per `arch/scope-model.md` §3 + `glossary/
    workspace.md`.

    The central Owner B instance + container for workspace-scope managed
    entities (practitioner-record + Actor universal + engagement-target
    entities shape-policy-mandated). workspace.md is the binding-instance
    entity at Owner B per `glossary/workspace.md`.

    Per §3 workspace integration spans Framework C selections + Owner B
    instance ownership + Layer A scope-resolution.

    Per §3 1:1 reciprocal cardinality with deployment per `glossary/
    deployment.md`: deployment = workspace-as-bound-runtime; exactly 1
    deployment per workspace at any moment of active runtime. Multi-
    environment scenarios (dev / staging / prod) = N workspaces.

    Per `MAINTENANCE.md` TOP-LEVEL SCOPE: per-deployment workspace.md
    authoring lives at deployment-instance, NOT framework. THIS schema
    describes the SHAPE; per-deployment storage convention is Phase 6
    deployment territory.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    workspace_id: str
    """Workspace identifier; per-deployment uniqueness convention
    (deployment-side prose-rule pattern per archived governance-and-
    identity-sourcing greenfield-evaluated per §15)."""

    shape: WorkspaceShapeId
    """Selects exactly one shape from Framework C shape catalog per
    `glossary/workspace.md` line 16-18 + `arch/scope-model.md` §3
    Framework C selections."""

    substrate: str
    """Selects exactly one substrate Implementation from Framework C
    substrate catalog (e.g., `claude_agent_sdk` / `ms_agent_framework`)
    per §3 Framework C selections."""

    specialists_active: tuple[str, ...]
    """List referencing Framework C specialist DEFINITIONs (`specialist-
    name@version`) per `arch/specialist-skill.md` §2.3 + §10 + §13 boot-
    time activation ordering. Per `glossary/specialist.md`: specialist
    activation per workspace.md `specialists_active` field; per-shape
    policy may declare maximum cardinality."""

    practitioners: tuple[str, ...]
    """Practitioner-record ids per `arch/practitioner.md` §3 cardinality
    matrix. practitioner-shape solo = 1; multi-practitioner-shape
    partnership = N; legal-entity-shape firm = N (under
    `legal_entity_context`). At least one practitioner-record required
    per shape policy per `arch/practitioner.md` §8."""

    legal_entity_context: LegalEntityContext | None = None
    """Firm-level legal entity context per `arch/practitioner.md` §3.
    Populated for legal-entity-shape workspaces only — practitioner-
    record references back via `firm_binding` field."""

    adapter_bindings: tuple[AdapterBinding, ...] = ()
    """Workspace adapter bindings per `arch/adapter.md` §10 per-instance
    boot. Resolved at substrate-phase 3 per §3 workspace boot integration;
    composes with `SpecialistDescriptor.activation_prereqs.adapter_bindings`
    per `arch/specialist-skill.md` §13 boot ordering step 3."""

    scope: WorkspaceScopeConfig = Field(default_factory=WorkspaceScopeConfig)
    """Layer A scope configuration per §3 + `glossary/workspace.md`
    composes-with Layer A row. Default empty (universal-only)."""

    instance_content_dissolution_policy: InstanceContentDissolutionPolicy = (
        InstanceContentDissolutionPolicy.ARCHIVE
    )
    """Workspace dissolution destruction policy per §13 cross-pattern
    coherence (same field shape across all 4 primitive-cluster ARCH
    topics). Default `archive` preserves practitioner work + axis-3
    authorship preservation + 6-months-later defensibility test re-
    runable per `arch/practitioner.md` §13 + `arch/specialist-skill.md`
    §13 + `arch/workflow-work-unit.md` §13 + `arch/claim-defensibility.
    md` §13.
    """


# ---------------------------------------------------------------------------
# Workspace lifecycle event-kind catalog
# ---------------------------------------------------------------------------


class WorkspaceBooted(AuditEventBase):
    """Workspace boot completion per `arch/scope-model.md` §3 workspace
    boot integration.

    Per `ARCHITECTURE.md` §6 composite boot subsection step 5 (substrate-
    phase 5: boot_complete event emitted; workspace-scope managed entities
    loaded; workflow_instance + work-unit instances loaded; Layer A
    content scope-resolved per workspace.scope configuration).
    """

    event_kind: Literal["workspace_booted"] = "workspace_booted"


class WorkspaceShutdown(AuditEventBase):
    """Workspace shutdown per `arch/scope-model.md` §3 workspace boot
    integration.

    Per `ARCHITECTURE.md` §6 composite shutdown subsection: practitioner-
    record state persists across substrate shutdown (workspace-scope
    managed entities at Owner B persist through workspace lifetime per
    `arch/practitioner.md` §13).
    """

    event_kind: Literal["workspace_shutdown"] = "workspace_shutdown"


class WorkspaceDissolved(AuditEventBase):
    """Workspace dissolution per cross-pattern destruction §13.

    Per `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 +
    `arch/workflow-work-unit.md` §13 + `arch/claim-defensibility.md` §13
    cross-pattern coherence: archival-as-default; opt-in delete-with-
    audit per `WorkspaceManifest.instance_content_dissolution_policy`.
    """

    event_kind: Literal["workspace_dissolved"] = "workspace_dissolved"


# ---------------------------------------------------------------------------
# Error categories (§7 + scope-categorization errors per E7)
# ---------------------------------------------------------------------------


class WorkspaceError(Exception):
    """Base for all workspace-class errors per `arch/scope-model.md` §7.

    Per `arch/scope-model.md` §7 scope-categorization error categories +
    recovery semantics — Phase 6 spec for full error catalog. Per-shape
    error semantics per §8 cross-shape policy variation: practitioner-
    shape fail-closed (defensibility-critical); autonomous-business-shape
    fail-open with alert; personal-OS-shape fail-open.
    """


class WorkspaceManifestValidation(WorkspaceError):
    """workspace.md frontmatter fails schema validation.

    Missing required fields (shape / substrate / specialists_active /
    practitioners); invalid enum values (shape not in
    `WorkspaceShapeId`); legal_entity_context required for legal-entity-
    shape but missing.
    """


class InvalidFrameworkKindReference(WorkspaceError):
    """workspace.specialists_active references non-existent specialist
    DEFINITION per `arch/scope-model.md` §7 (Framework C resolution
    failure).
    """


class OrphanOwnerScopeReference(WorkspaceError):
    """Workspace-scope managed entity references non-existent workspace
    per `arch/scope-model.md` §7 (Owner B integrity failure).

    E.g., practitioner-record's `firm_binding` references workspace_id
    that doesn't exist.
    """


class LayerAScopeMismatch(WorkspaceError):
    """workspace.scope.domains lists domain with no Layer A content
    available per `arch/scope-model.md` §7 (Layer A applicability gap).
    """


class CrossDeploymentScopeResolutionFailure(WorkspaceError):
    """Workspace identity persistence W3-related per `arch/scope-model.
    md` §7 (cross-substrate migration scope-resolution gap).

    Per `glossary/deployment.md` "Multi-deployment-of-same-workspace
    patterns" (backup→restore / substrate migration / re-activation);
    workspace identity invariants across deployments awaits Phase 6 spec
    per `arch/scope-model.md` §14 W3 watch-list.
    """
