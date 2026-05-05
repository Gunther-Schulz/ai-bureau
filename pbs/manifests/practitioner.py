"""Practitioner-RECORD descriptor schema — per `arch/practitioner.md`.

Per `arch/practitioner.md` §2.2 + §16: practitioner-RECORD Pydantic schema
lands Phase 6 (Mode 3 spec). This module defines the typed contract for
the practitioner-RECORD manifest + practitioner-lifecycle event-kind
catalog (§5) + PractitionerError categories (§7).

Per §1: practitioner is bipartite Pattern C — HUMAN aspect (cross-cutting;
the natural person bearing legal/professional accountability in the
world; framework records nothing about the human directly) +
practitioner-RECORD aspect (Owner B; system representation enabling per-
event attribution per `glossary/authority-binding.md`). This module
schemas the RECORD aspect only — the HUMAN aspect is non-system per §2.1.

Per §3 multi-practitioner workspace mechanics: each session binds to ONE
practitioner-record at session-open via `session.bound_practitioner_id`
(per `arch/substrate.md` §F session/context management). Cross-session
within workspace = N practitioner-records active concurrently in
different sessions; never multiple in single session.

Per §13 archival-as-default: deactivated practitioners marked
`lifecycle_state: dormant`; record NOT deleted (preserves audit-trail
attribution to historic outputs per axis-3 defensibility-critical).
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict

from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Manifest enums (§2.2 frontmatter manifest schema)
# ---------------------------------------------------------------------------


class SigningAuthority(StrEnum):
    """Per-practitioner signing authority per `arch/practitioner.md` §2.2.

    Framework-level enum constraining WHO can sign claims at framework
    level (gate-enforced structural per `MAINTENANCE.md` TOP-LEVEL DESIGN
    PRINCIPLES §1); per-shape policy declares which categories REQUIRED
    per shape per §8.

    Different scope from `role_bindings` (per §2.2 schema explanation):
    `signing_authority` constrains WHO can sign claims at framework-
    mechanism level; `role_bindings` constrains WHICH actions per shape
    policy.
    """

    INDEPENDENT = "independent"
    UNDER_SUPERVISION = "under-supervision"
    FIRM_BOUND = "firm-bound"


class PractitionerRecordMode(StrEnum):
    """Practitioner-RECORD source mechanics per `arch/practitioner.md` §2.2.

    `native` = PBS-native md file is source of truth; PBS owns the data.
    `adapter` = RECORD sourced from external HR/identity system via
    adapter Surface per W2 Identity-class adapter Surface candidate per
    `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition.
    """

    NATIVE = "native"
    ADAPTER = "adapter"


class PractitionerLifecycleState(StrEnum):
    """Practitioner-RECORD lifecycle state per `arch/practitioner.md` §5.

    Two-state machine: `active` → eligible for session binding;
    `dormant` → not eligible (preserves audit-trail attribution to
    historic outputs without permitting new claim-signing per §13).

    Naming aligned with `arch/practitioner.md` §SD-4 + parallel to
    workflow_instance + work-unit instance lifecycle states per cross-
    pattern coherence.
    """

    ACTIVE = "active"
    DORMANT = "dormant"


# ---------------------------------------------------------------------------
# PractitionerRecord (§2.2 manifest schema)
# ---------------------------------------------------------------------------


class PractitionerRecord(BaseModel):
    """Practitioner-RECORD manifest per `arch/practitioner.md` §2.2.

    System representation of a practitioner — workspace-scope managed
    entity at Owner B per `glossary/owner-b-scope.md` members list. The
    RECORD enables every per-event attribution chain that authority-
    binding mechanism enforces per `glossary/authority-binding.md` per-
    event actor declaration sub-aspect.

    The HUMAN aspect (cross-cutting; the natural person in the world) is
    NOT represented here — framework's contract with the HUMAN is mediated
    through this RECORD per §2.1 architectural positioning.

    Per §6 logic placement: practitioner-record entity-md is Mode 1
    production-runtime LLM-MD (workspace AI reads at session-open + at
    attestation moments); THIS Pydantic shape is Mode 3 hybrid spec layer.

    Per §13 archival-as-default destruction: deactivated practitioners
    remain in `dormant` state preserving audit-trail attribution; never
    deleted (per axis-3 defensibility-critical preservation).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    """Practitioner-record identifier; per-deployment uniqueness convention
    (deployment-side prose-rule pattern per archived governance-and-
    identity-sourcing greenfield-evaluated per §15)."""

    legal_name: str
    """Full legal name of the natural person; the HUMAN aspect's
    identifier in the world (per §2.2 schema row)."""

    actor_kind: Literal[ActorKind.HUMAN] = ActorKind.HUMAN
    """Always HUMAN per `glossary/actor.md` (practitioner is one specific
    actor kind; not multiple-kinds-of-practitioner per §2.2). Enforced as
    Literal so schema rejects non-HUMAN actor_kind at validation.
    """

    email: str | None = None
    """Contact + identity-mapping anchor for auth/SSO integration per W2
    watch-list adapter-mode mechanics."""

    signing_authority: SigningAuthority
    """Framework-level signing-authority enum per §2.2 + §8 cross-shape
    policy variation. Gate-enforced structural per `MAINTENANCE.md`
    TOP-LEVEL DESIGN PRINCIPLES §1 (the gate dispatches on it for every
    signed-claim emission)."""

    role_bindings: tuple[str, ...] = ()
    """Per-workspace role list constraining WHICH actions per shape policy
    (shape-policy-enforced; cross-references shape-policy role primitive
    per archived governance-and-identity-sourcing decision 1 greenfield-
    evaluated per §15)."""

    credentials: tuple[str, ...] = ()
    """Professional credentials (license number; bar admission; medical
    license; chamber membership) — per-shape-policy-mandated per §8 (e.g.,
    legal-practice shape may mandate bar admission credential)."""

    mode: PractitionerRecordMode = PractitionerRecordMode.NATIVE
    """Source mechanics per §2.2 (native = PBS-native md file; adapter =
    HR-system-sourced via adapter Surface)."""

    adapter_binding: str | None = None
    """Adapter ID when `mode == ADAPTER` (e.g., `personio` /
    `microsoft-entra` / `coolify-sso`); composes with `arch/adapter.md`
    Identity-class Surface per W2."""

    lifecycle_state: PractitionerLifecycleState
    """Active or dormant per §SD-4 lifecycle states (deactivation =
    dormant-not-deleted per axis-3 defensibility-critical preservation
    per §13)."""

    firm_binding: str | None = None
    """Reference to workspace.md `legal_entity_context` workspace_id (per
    §3 below; for legal-entity-shape workspaces only — practitioner-
    record references back to firm-level workspace context)."""


# ---------------------------------------------------------------------------
# Practitioner-lifecycle event-kind catalog (§5)
# ---------------------------------------------------------------------------


class PractitionerRecordMinted(AuditEventBase):
    """Practitioner-record created per `arch/practitioner.md` §5.

    Emitted at workspace setup OR per-practitioner-addition (subsequent
    practitioners joining a multi-practitioner workspace per §3
    cardinality matrix).
    """

    event_kind: Literal["practitioner_record_minted"] = "practitioner_record_minted"


class PractitionerRecordUpdated(AuditEventBase):
    """Practitioner-record updated per `arch/practitioner.md` §5.

    Single event-kind with `details.changed_fields: list[str]` (NOT
    separate event-kinds per field; minimal event-kind catalog growth per
    archived audit-trail-v2 `details:` payload precedent — greenfield-
    evaluated per §15). Mutable-with-audit per §5 (changes to credentials
    / signing authority / role bindings emit this event; never silently
    rewritten).
    """

    event_kind: Literal["practitioner_record_updated"] = "practitioner_record_updated"


class PractitionerRecordDeactivated(AuditEventBase):
    """Practitioner deactivated per `arch/practitioner.md` §5.

    Practitioner leaves workspace; `lifecycle_state` transitions to
    `dormant`; record NOT deleted (preserves audit-trail attribution to
    historic outputs per axis-3 defensibility-critical per §13).
    """

    event_kind: Literal["practitioner_record_deactivated"] = "practitioner_record_deactivated"


class PractitionerRecordReactivated(AuditEventBase):
    """Dormant practitioner returns per `arch/practitioner.md` §5.

    `lifecycle_state` transitions back to `active`; eligible for session
    binding again per §13 boot-time activation ordering step 4.
    """

    event_kind: Literal["practitioner_record_reactivated"] = "practitioner_record_reactivated"


# ---------------------------------------------------------------------------
# Error categories (§7 practitioner-error categories)
# ---------------------------------------------------------------------------


class PractitionerError(Exception):
    """Base for all practitioner-class errors per `arch/practitioner.md` §7.

    Per-shape error semantics (§8): practitioner-shape fail-closed
    (defensibility-critical; signing authority violations must surface;
    no silent degradation); autonomous-business-shape N/A or fail-open
    with alert (continuity prioritized); personal-OS-shape fail-open
    (lightweight; degradation acceptable).
    """


class PractitionerRecordValidation(PractitionerError):
    """Frontmatter fails schema validation per §7.

    Missing required fields; invalid enum values; signing_authority not
    in `independent` | `under-supervision` | `firm-bound`.
    """


class PractitionerAdapterHydrationFailure(PractitionerError):
    """Adapter-mode RECORD hydration fails at session-open per §7.

    Adapter Surface error; external HR system unreachable; identity-
    mapping email not found. Composes with `arch/adapter.md` per-class
    Surface failure (fires at adapter binding load step per §13 boot
    ordering step 3).
    """


class PractitionerSigningAuthorityViolation(PractitionerError):
    """Signing-authority constraint violated per §7.

    Practitioner attempts signed-claim emission but `signing_authority`
    doesn't satisfy per-shape required category (e.g., `under-supervision`
    practitioner attempts independent signing in legal-practice shape
    requiring `independent`).
    """


class PractitionerSessionBindingViolation(PractitionerError):
    """Multi-practitioner concurrency violation per §7.

    Session attempts to bind two practitioner-records simultaneously per
    §3 multi-practitioner concurrent-session handling (`session.
    bound_practitioner_id` is set at session-open and immutable for
    session lifetime).
    """


class PractitionerLifecycleStateConflict(PractitionerError):
    """Operation requires `active` but practitioner-record is `dormant`
    per §7.

    E.g., dormant practitioner attempts to sign new claim — preserves
    audit-trail attribution to historic outputs without permitting new
    claim-signing per §13.
    """


class PractitionerCrossPractitionerWriteViolation(PractitionerError):
    """Cross-practitioner write boundary violated per §7.

    Practitioner-A attempts to modify practitioner-B's signed claim
    (per §3 cross-practitioner composition rules; structural per axis-3 —
    each practitioner accountable for own signed claims; cross-
    practitioner write would break attribution chain integrity).
    """
