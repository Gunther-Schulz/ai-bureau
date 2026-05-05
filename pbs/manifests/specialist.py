"""Specialist + Skill descriptor schemas — per `arch/specialist-skill.md`.

Per `arch/specialist-skill.md` §2.3 + §16: SpecialistDescriptor +
SkillDescriptor Pydantic schemas land Phase 6 (Mode 3 spec). This module
defines the typed contracts for the specialist DEFINITION manifest +
skill DEFINITION + the specialist-lifecycle event-kind catalog (§7) +
SpecialistError categories (§7).

Per §1: specialist is bipartite Pattern B (DEFINITION at Framework C;
INSTANCE-CONTENT at Owner B); skill is single-aspect cross-cutting
within specialist context. Per §10 specialist-namespace: skill identity
within specialist is `<specialist-name>:<skill-name>` (fully-qualified).

Per §2.2 specialist-skill structural boundary (PBS architectural
commitment): skill canNOT exist standalone outside specialist context;
skill DEFINITIONs are bundled under specialist's `skills/` subdirectory
per §2.3 directory structure.

Per §8 cross-shape policy variation: specialist + skill DEFINITIONs stay
shape-neutral per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2; the
`shape_compatibility` manifest field declares specialist-side shape
applicability, but per-shape activation policy lives in shape policy
bundle.

Resolves substrate.py SpecialistDescriptor `Any` placeholder (Phase 6.1
Note 71); substrate.py refines `register_specialist(descriptor: Any)` to
`register_specialist(descriptor: SpecialistDescriptor)` after this
module lands.
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Manifest enums (§2.3 frontmatter manifest schema)
# ---------------------------------------------------------------------------


class AxisClaim(StrEnum):
    """Per-specialist axis-claim per `arch/specialist-skill.md` §2.3.

    Declares which axis the specialist primarily serves; cross-axis when
    the specialist's bundled skills serve multiple axes per §1 cross-axis
    claim ("specialists support any axis through their bundled skills +
    entities + adapters").
    """

    AXIS_1 = "axis-1"
    AXIS_2 = "axis-2"
    AXIS_3 = "axis-3"
    CROSS_AXIS = "cross-axis"


class SpecialistTier(StrEnum):
    """Two-tier specialist classification per `arch/specialist-skill.md` §9.

    Per §9 two-tier classification: `domain-anchored` specialists serve
    one archetype's domain (e.g., planning-document-work for PBS-Schulz);
    `cross-archetype` specialists usable across ≥2 distinct workspace
    archetypes (e.g., citation-verification across legal + research +
    planning).
    """

    DOMAIN_ANCHORED = "domain-anchored"
    CROSS_ARCHETYPE = "cross-archetype"


class ShapeCompatibility(StrEnum):
    """Per-specialist shape applicability per `arch/specialist-skill.md` §2.3.

    Declares which shape policy bundles the specialist can deploy under
    per `profiles/G-composability-gate.md` cross-shape consumption framing.
    `cross-shape` declares the specialist applies to all shapes uniformly.
    """

    PRACTITIONER = "practitioner-shape"
    AUTONOMOUS_BUSINESS = "autonomous-business-shape"
    PERSONAL_OS = "personal-OS-shape"
    CROSS_SHAPE = "cross-shape"


# ---------------------------------------------------------------------------
# Activation prereqs + capability declarations (§2.3 sub-objects)
# ---------------------------------------------------------------------------


class ActivationPrereqs(BaseModel):
    """Specialist activation prerequisites per `arch/specialist-skill.md` §2.3.

    Declares structural dependencies that must be satisfied at workspace
    boot per §13 boot-time specialist activation ordering step 3:
    substrate-class pinning + adapter bindings + other-specialist
    dependencies. Failure paths surface per §7 SpecialistError categories
    (`SpecialistSubstrateClassPinViolation` /
    `SpecialistAdapterDependencyUnmet` /
    `SpecialistCrossDependencyUnmet`).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    substrate_class_pinned: tuple[str, ...] = ()
    """Substrate-impl id list constraining specialist to specific substrate
    Implementations (e.g., `claude_agent_sdk`, `ms_agent_framework`).
    Empty tuple = substrate-agnostic per §11 cross-substrate compatibility.
    """

    adapter_bindings: tuple[str, ...] = ()
    """Required adapter classes + min-version (e.g., `mcp_server>=1.0`).
    Validated against `WorkspaceManifest.adapter_bindings` at boot per §13
    boot-time activation ordering step 3 (`SpecialistAdapterDependencyUnmet`
    if missing).
    """

    other_specialists: tuple[str, ...] = ()
    """Required other-specialist names + min-version (e.g.,
    `citation-verification>=1.2`). Resolved against workspace's
    `specialists_active` list; activation ordering per dependency graph
    per §7 other operational concerns (`SpecialistCrossDependencyUnmet`
    if missing).
    """


class ShapePolicyConformance(BaseModel):
    """Per-specialist shape-policy-conformance assertion per `arch/
    specialist-skill.md` §2.3 capability_declarations.

    Declares per-shape mandate-fulfilment claims (e.g., "satisfies
    practitioner-shape claim-level audit-emission"); used by per-shape
    policy at workspace boot to validate specialist's shape compatibility.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    shape_id: str
    """Active shape identifier (e.g., `practitioner-shape`)."""

    mandate_fulfilment: tuple[str, ...] = ()
    """Per-shape mandate the specialist satisfies (e.g., "claim-level
    audit-emission", "sparring sub-mechanisms 1-4 architecturally-encoded").
    Free-form architectural-level assertion; per-shape policy interprets.
    """


class CapabilityDeclarations(BaseModel):
    """Specialist capability declarations per `arch/specialist-skill.md` §2.3.

    Bundle composition manifest: enumerates skills + entity-kinds +
    workflow-definitions + work-unit-kinds the specialist DEFINITION
    bundles + per-shape mandate-fulfilment assertions.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    skills: tuple[str, ...]
    """Skill names within bundle (local; specialist-namespace per §10
    `<specialist-name>:<skill-name>` for cross-specialist references).
    Each entry must have a corresponding skill file under specialist's
    `skills/` subdirectory per §2.3 directory structure.
    """

    entity_kinds: tuple[str, ...] = ()
    """Entity-kinds the deployed specialist instance owns at Owner B
    (e.g., bausteine kind / specialist-specific reference kinds per §2.1
    DEFINITION aspect).
    """

    workflow_definitions: tuple[str, ...] = ()
    """Workflow definition names within bundle per `arch/workflow-work-
    unit.md` §2.1 (specialist DEFINITION declares workflow patterns per
    §2.3 capability_declarations).
    """

    work_unit_kinds: tuple[str, ...] = ()
    """Work-unit kind names within bundle per `arch/workflow-work-unit.md`
    §2.3 (specialist DEFINITION declares its kinds per §2.3
    capability_declarations).
    """

    shape_policy_conformance: tuple[ShapePolicyConformance, ...] = ()
    """Per-shape mandate-fulfilment claims; per-shape policy at workspace
    boot validates these against shape's mandate set.
    """


# ---------------------------------------------------------------------------
# SkillDescriptor (§2.2 atomic structure)
# ---------------------------------------------------------------------------


class SkillDescriptor(BaseModel):
    """Skill DEFINITION per `arch/specialist-skill.md` §2.2.

    Atomic unit of work logic within a specialist; trigger frontmatter +
    body content + optional output schema. Per §2.2 specialist-skill
    structural boundary: skill canNOT exist standalone outside specialist
    context; SkillDescriptor is always bundled within SpecialistDescriptor.

    Per §6 logic placement: skill body content is Mode 1 production-runtime
    LLM-MD (AI runtime reads at activation); output schema (when declared)
    is Mode 2 production-runtime Python (substrate Surface §D structured
    output validation).

    Loading semantics (auto-load / explicit-load / lazy-load) per substrate
    Pattern A; this descriptor declares SHAPE not loading mode.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    """Skill name local to specialist (specialist-namespace per §10;
    fully-qualified `specialist-name:skill-name` for cross-specialist
    references)."""

    description: str
    """Skill description (substrate-defined trigger keyword convention;
    auto-load activation conditions per §2.2 trigger frontmatter)."""

    when_to_use: str | None = None
    """Trigger conditions per §2.2 (substrate-defined keyword convention;
    when this skill fires)."""

    version: str | None = None
    """Skill version (inherits specialist version per §5 skill lifecycle;
    no per-skill semver — declared optional for substrate-specific
    metadata only)."""

    output_schema_ref: str | None = None
    """Reference to Pydantic schema for structured output validation per
    substrate Surface §D (per §2.2 optional output schema). When present,
    skill firings emit structured output validated against the schema;
    auto-retry on validation fail per substrate impl."""


# ---------------------------------------------------------------------------
# SpecialistDescriptor (§2.3 manifest schema)
# ---------------------------------------------------------------------------


class SpecialistDescriptor(BaseModel):
    """Specialist DEFINITION manifest per `arch/specialist-skill.md` §2.3.

    Bipartite Pattern B; this descriptor describes the DEFINITION aspect
    at Framework C scope (the distributable bundle). INSTANCE-CONTENT
    aspect at Owner B is workspace-scope managed entities owned by the
    deployed specialist instance — that's deployment-state, not framework
    schema; see `pbs.manifests.workspace` for workspace-scope hydration.

    Manifest is contract between specialist DEFINITION (what the bundle
    PROVIDES) + workspace (what the deployment NEEDS via
    `specialists_active`). Substrate Surface §G validates the manifest at
    workspace boot per §13 boot-time activation ordering.

    Resolves substrate.py SpecialistDescriptor `Any` placeholder (Phase
    6.1 Note 71). Per §6 logic placement: specialist manifest itself is
    Mode 1 production-runtime LLM-MD (workspace AI reads at activation);
    THIS Pydantic shape is Mode 3 hybrid spec layer.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    """Specialist identifier (namespace root for KIND + workflow
    disambiguation per §10 specialist-namespace)."""

    version: str
    """Specialist semver per §5 specialist lifecycle (major / minor /
    patch); a specialist version is immutable once published per §5.
    Format validation per Phase 6 per-impl spec.
    """

    axis_claim: AxisClaim
    """Primary axis-claim per §2.3."""

    tier: SpecialistTier
    """Two-tier classification per §9."""

    shape_compatibility: tuple[ShapeCompatibility, ...]
    """Per-shape applicability per §2.3 (per `profiles/G-composability-
    gate.md` cross-shape consumption framing). At least one entry; may
    include `cross-shape` for shape-uniform applicability."""

    capability_declarations: CapabilityDeclarations
    """Bundle composition manifest per §2.3 (skills + entity-kinds +
    workflow-definitions + work-unit-kinds + shape_policy_conformance)."""

    skills: tuple[SkillDescriptor, ...]
    """Bundled skill DEFINITIONs per §2.3 directory structure
    `skills/<skill-name>.md`. Must align with `capability_declarations.
    skills` (each enumerated skill-name has matching SkillDescriptor)."""

    activation_prereqs: ActivationPrereqs = Field(default_factory=ActivationPrereqs)
    """Substrate-class-pinned + adapter-bindings + other-specialists
    dependencies per §2.3 (optional fields default to empty)."""

    license: str | None = None
    """SPDX license identifier (e.g., `Apache-2.0` / `MIT` / proprietary
    marker) per §2.3 + §11 Distribution shape; load-bearing for G
    Composability Gate consumption modes (OSS / marketplace).
    """


# ---------------------------------------------------------------------------
# Specialist-lifecycle event-kind catalog (§7)
# ---------------------------------------------------------------------------


class SpecialistActivated(AuditEventBase):
    """Specialist activated per `arch/specialist-skill.md` §7.

    `specialists_active` set acquired this specialist; substrate Surface
    §G registered it; new skills available per §5 mid-session re-binding.
    Composes with substrate-phase 4 specialist registration step per §13.
    """

    event_kind: Literal["specialist_activated"] = "specialist_activated"


class SpecialistDeactivated(AuditEventBase):
    """Specialist deactivated per `arch/specialist-skill.md` §7.

    `specialists_active` set released this specialist; INSTANCE-CONTENT
    preserved per §5 persistence rule (deactivating a specialist preserves
    accumulated content per `glossary/specialist.md`).
    """

    event_kind: Literal["specialist_deactivated"] = "specialist_deactivated"


class SpecialistSkillRegistered(AuditEventBase):
    """Skill within specialist registered per `arch/specialist-skill.md` §7.

    Individual skill within specialist became substrate-registered per
    substrate Surface §G materialization. Emitted per-skill at substrate-
    phase 4 step 5 per §13 boot-time activation ordering.
    """

    event_kind: Literal["specialist_skill_registered"] = "specialist_skill_registered"


class SpecialistLoadFailed(AuditEventBase):
    """Specialist load failure per `arch/specialist-skill.md` §7.

    Manifest validation OR skill load OR dependency check failed;
    specialist NOT activated. `details` carries failure category per §7
    error categories (`SpecialistManifestValidation` /
    `SpecialistSkillLoadFailure` / `SpecialistEntityKindConflict` / etc.).
    """

    event_kind: Literal["specialist_load_failed"] = "specialist_load_failed"


class SpecialistVersionBumped(AuditEventBase):
    """Specialist version-bump observation per `arch/specialist-skill.md` §7.

    Workspace observed specialist version change (e.g., re-deployment with
    newer specialist version); cross-version compatibility check fired
    per §8 specialist version-bump mid-session policy.
    """

    event_kind: Literal["specialist_version_bumped"] = "specialist_version_bumped"


# ---------------------------------------------------------------------------
# Error categories (§7 specialist-error categories)
# ---------------------------------------------------------------------------


class SpecialistError(Exception):
    """Base for all specialist-class errors per `arch/specialist-skill.md` §7.

    Per-shape error semantics (§8): practitioner-shape fail-closed
    (defensibility-critical; specialist load failures must surface to
    practitioner; no silent degradation); autonomous-business-shape
    fail-open with alert (continuity prioritized; alert + fallback to
    remaining active specialists); personal-OS-shape fail-open
    (lightweight; degradation acceptable).
    """


class SpecialistManifestValidation(SpecialistError):
    """Manifest frontmatter fails schema validation per §7.

    Missing required fields; invalid enum values; semver malformed.
    """


class SpecialistSkillLoadFailure(SpecialistError):
    """Skill loading fails at substrate registration per §7.

    Substrate Surface §G error; skill file unparseable; substrate-defined
    trigger conventions violated.
    """


class SpecialistEntityKindConflict(SpecialistError):
    """Specialist's entity-kind DEFINITION collides with already-registered
    kind from another active specialist per §7.

    Resolved via specialist-namespace per §10 (fully-qualified
    `specialist-name:kind-name`).
    """


class SpecialistCrossDependencyUnmet(SpecialistError):
    """Specialist activation requires another specialist (per
    `activation_prereqs.other_specialists`) that isn't activated per §7.

    Workspace boot fails OR mid-session activation rejected.
    """


class SpecialistAdapterDependencyUnmet(SpecialistError):
    """Specialist requires adapter binding (per `activation_prereqs.
    adapter_bindings`) that isn't in workspace.md adapter bindings list
    per §7.
    """


class SpecialistSubstrateClassPinViolation(SpecialistError):
    """Specialist declares substrate-impl pin (per `activation_prereqs.
    substrate_class_pinned`) incompatible with selected substrate per §7.
    """
