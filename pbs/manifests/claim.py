"""Claim + defensibility schemas — per `arch/claim-defensibility.md`.

Per `arch/claim-defensibility.md` §13 + §16: claim-event Pydantic schema
+ 6-event-kind catalog land Phase 6 (Mode 3 spec). This module defines
the typed contracts for the claim PRIMITIVE + per-claim attestation
chain mechanics + 6-event-kind catalog candidate (§13) + ClaimError
categories.

Per §1: claim is **axis-3 PRIMARY anchor** — claim is unit-of-defense
per the defensibility test (per `glossary/claim.md` axis classification);
defensibility IS the axis-3 success criterion test (per `glossary/
defensibility.md`). Defensibility is DERIVED property/test (NOT entity-
having); resolves at claim granularity per §3 reciprocal asymmetry.

Per §2.1 four distinguishing properties (all four must hold for assertion
to qualify as claim):
1. Atomic — semantic-unit of one assertion
2. Accountability-bearing — practitioner can be challenged on it
3. Judgment-bearing — NOT lookup-shaped (fact-statements aren't claims)
4. Source-grounded — every claim traces to source per source-grounding
   mechanism (framework-level guarantee)

Per §3 per-claim attestation chain (mechanics):
1. claim_made emission (`actor_kind: ai_runtime` + skill identifier)
2. Production-phase engaged-authorship sparring events DURING production
3. Revision = new claim_made event (append-only NOT rewrite)
4. Finalization moment
5. Per-claim attestation event AT finalization (`actor_kind: human` +
   practitioner-RECORD identity per `arch/practitioner.md` §4)
6. Composition INTO work-unit attribution chain

Per §13 cross-pattern destruction inheritance: claims inherit work-unit's
`instance_content_dissolution_policy` per `arch/workflow-work-unit.md`
§13 + cross-pattern coherence with `arch/specialist-skill.md` §13 +
`arch/practitioner.md` §13 (NO separate per-claim destruction policy).
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Claim PRIMITIVE (§2.1 four distinguishing properties)
# ---------------------------------------------------------------------------


class Claim(BaseModel):
    """Claim PRIMITIVE per `arch/claim-defensibility.md` §2.1.

    Atomic accountability-bearing assertion within a work-unit's produced
    output — the smallest unit of content the practitioner-author can be
    challenged on, must defend, and bears regulatory/professional
    accountability for.

    Four distinguishing properties (all four must hold; per §2.1):
    atomic + accountability-bearing + judgment-bearing + source-grounded.

    Per §3 reciprocal asymmetry: defensibility tests claims (NOT entity-
    having; one-way directional composition — defensibility-tests-claims,
    never claims-bundle-defensibility).

    Per §5 claim lifecycle: created during workflow execution; revised
    (append-only new event); finalized at send/sign moment; mutability =
    append-only at audit level (claim revision = new event preserving
    prior state per `arch/audit.md` §B).

    Claims are NOT separately scoped at Owner B — per `arch/scope-model.
    md` §4 E3 content-unit-IN-instance pattern: claim INHERITS work-unit's
    Owner B placement (bundled INTO work-unit instance content; NO
    separate `owner_scope` + `owner_key`).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    """Per-deployment claim id; per-deployment uniqueness convention
    (deployment-side prose-rule pattern per archived governance-and-
    identity-sourcing decision 3 + decision 4 greenfield-evaluated per
    §15)."""

    content: str
    """Asserted content — the atomic semantic-unit of one assertion per
    §2.1 property #1. Min-content / atomicity constraints per Phase 6
    per-impl spec; framework-level shape: free-form str."""

    work_unit_id: str
    """Containing work-unit instance id per §1 cluster cardinality (claim
    is content-unit IN work-unit per `arch/scope-model.md` §4 E3); claim
    INHERITS work-unit's Owner B placement."""

    workflow_instance_id: str | None = None
    """Workflow_instance attribution per §4 (claims emitted during
    workflow_instance execution attribute to that workflow_instance);
    None for ad-hoc work claims (attribute to work-unit + session without
    workflow_instance per `glossary/claim.md` composes-with workflow
    row)."""

    authoring_skill_id: str
    """Skill identifier that authored the claim per §2.1 claim-event
    composition (`actor_kind: ai_runtime` + skill identifier records
    authoring actor per authority-binding mechanism Surface). Fully-
    qualified `specialist-name:skill-name` per `arch/specialist-skill.md`
    §10 specialist-namespace."""

    source_refs: tuple[str, ...] = ()
    """Source-grounding references per §2.1 property #4 (every claim
    traces to source per source-grounding mechanism). Framework-level
    guarantee that no claim is unsourced; format per Phase 6 source-
    grounding mechanism spec.
    """

    version: int = 1
    """Claim version per §2.1 revision per-version semantics. Revision
    increments version + emits new `claim_made` event preserving prior
    state per append-only audit (per `arch/audit.md` §B). Engaged-
    authorship of v1 does NOT carry forward to v2 — re-attestation
    required on revision per `glossary/engaged-authorship.md`.
    """


class ClaimAttestation(BaseModel):
    """Per-claim attestation per `arch/claim-defensibility.md` §3 per-claim
    attestation chain step 5.

    Records attestation-phase per-claim attestation event payload —
    `actor_kind: human` + practitioner-RECORD identity per `arch/
    practitioner.md` §4 (session-bound practitioner) + `glossary/
    authority-binding.md` line 35.

    Per §2.2 defensibility's Cond #1 (engaged authorship): production-
    phase engagement (axis-2-anchored sparring events) + attestation-
    phase engagement (axis-3-anchored per-claim attestation event); both
    phases must structurally complete for engaged-authorship to hold.

    Per §3 pre-existing-claim ingestion semantics: re-engagement event
    on import OR template-with-attribution policy per shape; preserves
    engaged-authorship-presence guarantee at framework level for legacy
    claims per W2 watch-list.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    claim_id: str
    """Claim being attested."""

    claim_version: int
    """Per §2.1 revision per-version semantics — attestation binds to
    specific claim version (re-attestation required on revision per
    `glossary/engaged-authorship.md`)."""

    attesting_practitioner_id: str
    """practitioner-RECORD id per `arch/practitioner.md` §2.2; the session-
    bound practitioner attesting per §4 multi-practitioner concurrent-
    session handling (each session binds to ONE practitioner-record)."""

    is_re_attestation: bool = False
    """True for post-revision attestation (claim v2 = new engaged-
    authorship test cycle per `glossary/engaged-authorship.md`); emits
    `ClaimReAttested` event vs `ClaimAttested`."""


# ---------------------------------------------------------------------------
# 6-event-kind catalog candidate (§13)
# ---------------------------------------------------------------------------


class ClaimMade(AuditEventBase):
    """Claim production fired per `arch/claim-defensibility.md` §13.

    `actor_kind: ai_runtime` + skill identifier records authoring actor
    per authority-binding mechanism Surface (per `glossary/authority-
    binding.md` per-event actor declaration). Carries claim content +
    work_unit_id + (optional) workflow_instance_id attribution. Production-
    phase moment per `glossary/claim.md` lifecycle.
    """

    event_kind: Literal["claim_made"] = "claim_made"


class ClaimRevised(AuditEventBase):
    """Claim revision per `arch/claim-defensibility.md` §13.

    New event preserving prior claim state per append-only audit (per
    `arch/audit.md` §B). `details.previous_event_id` references prior
    `claim_made` event per §13 6-event-kind catalog candidate.

    Per `glossary/claim.md` "REVISED during review (revision emits new
    event preserving prior claim state per append-only audit)"; per
    `glossary/engaged-authorship.md` v2 attestation does NOT carry
    forward from v1 — re-attestation required on revision.
    """

    event_kind: Literal["claim_revised"] = "claim_revised"


class ClaimFinalized(AuditEventBase):
    """Claim finalization per `arch/claim-defensibility.md` §13.

    Transition to send/sign-ready state per `glossary/claim.md`
    lifecycle; signed-claim_made event preceding per-claim attestation
    event per §3 per-claim attestation chain step 4.
    """

    event_kind: Literal["claim_finalized"] = "claim_finalized"


class ClaimAttested(AuditEventBase):
    """Per-claim attestation event per `arch/claim-defensibility.md` §13.

    Attestation-phase per-claim attestation event per `glossary/engaged-
    authorship.md`; fires AT finalization. Records `actor_kind: human` +
    practitioner-RECORD identity per `arch/practitioner.md` §4 (session-
    bound practitioner) + `glossary/authority-binding.md` line 35 ("every
    signature_applied event records actor_kind: human + practitioner
    identity for legal-bind moments").
    """

    event_kind: Literal["claim_attested"] = "claim_attested"


class ClaimReAttested(AuditEventBase):
    """Post-revision attestation per `arch/claim-defensibility.md` §13.

    Per §3 per-claim attestation chain step 6 ("re-attest-on-revision —
    claim v2 = new engaged-authorship test cycle"); v1's engagement
    doesn't carry forward to v2 (per-claim per-version semantics per
    `glossary/engaged-authorship.md`). Distinct from `ClaimAttested` so
    audit-trail reconstruction can identify revision-bound attestations.
    """

    event_kind: Literal["claim_re_attested"] = "claim_re_attested"


class DefensibilityTestRun(AuditEventBase):
    """Defensibility post-hoc reconstruction event per `arch/claim-
    defensibility.md` §13.

    Per `glossary/defensibility.md` re-run-ability: six-months-later (or
    years-later) reconstruction via audit-trail Surface §C query API.
    Records test invocation + outcome (passed / failed) + reconstructed
    reasoning chain reference per §13 6-event-kind catalog candidate.

    Implementation mechanics → Phase 6 audit-emission catalog territory
    + Phase 6 spec per §7 other operational concerns.
    """

    event_kind: Literal["defensibility_test_run"] = "defensibility_test_run"


# ---------------------------------------------------------------------------
# Error categories
# ---------------------------------------------------------------------------


class ClaimError(Exception):
    """Base for all claim-class errors per `arch/claim-defensibility.md`.

    Per-shape error semantics (§8): practitioner-shape friction/block
    fail-closed (defensibility-critical; missing per-claim engagement
    events surface to practitioner; quality-gate intervention per
    `arch/quality-gate.md`); autonomous-business-shape programmatic block
    (operator-attestation programmatic; programmatic policy gate);
    personal-OS-shape audit-only (drift-check report; no friction;
    lightweight).
    """


class ClaimSourceGroundingViolation(ClaimError):
    """Claim emitted without source-grounding per §2.1 property #4.

    Framework-level guarantee that no claim is unsourced (per `glossary/
    claim.md` "every claim must trace to source"); raised when
    `Claim.source_refs` is empty under shape policy mandating
    source-grounding (practitioner-shape MANDATORY no-unsourced per §8;
    autonomous-business per-action source aggregation OK; personal-OS
    optional).
    """


class ClaimAttestationMissing(ClaimError):
    """Per-claim attestation event missing at finalization per §2.2 + §3.

    Defensibility's Cond #1 attestation-phase requires per-claim
    attestation event AT finalization per `glossary/engaged-authorship.
    md`; missing attestation = rubber-stamping signal per `glossary/
    rubber-stamping.md` (axis-3 failure mode failing Cond #1 attestation-
    phase).
    """


class ClaimReAttestationRequired(ClaimError):
    """Post-revision attestation required per §3 per-claim attestation
    chain step 6.

    Engaged-authorship of claim v1 doesn't carry forward to v2 if v2
    wasn't engaged per `glossary/engaged-authorship.md`; raised at v2
    finalization when no `ClaimReAttested` event is found.
    """


class ClaimRevisionAppendViolation(ClaimError):
    """Claim revision attempted as rewrite instead of append-only per §2.1.

    Per `glossary/claim.md` "REVISED during review (revision emits new
    event preserving prior claim state per append-only audit)" + `arch/
    audit.md` §B append-only persistence; raised when impl attempts to
    mutate prior `claim_made` event instead of emitting new
    `ClaimRevised` event.
    """


# ---------------------------------------------------------------------------
# Defensibility test invocation (§5 lifecycle; re-run-able)
# ---------------------------------------------------------------------------


class DefensibilityTestInvocation(BaseModel):
    """Defensibility test invocation per `arch/claim-defensibility.md` §5
    defensibility lifecycle.

    Records a defensibility test run for post-hoc reconstruction per
    `glossary/defensibility.md` re-run-ability ("six-months-later or
    years-later, when challenged, the reasoning chain is reconstructed
    via audit trail; defensibility doesn't expire").

    Test invocation captures: which claims were tested + outcome per
    claim + reconstructed reasoning chain reference. Composes with
    `DefensibilityTestRun` event per §13 catalog (event records
    invocation occurrence; this model carries the test payload).

    Defensibility is DERIVED (property/test, NOT entity-having) per §1 +
    §5 cardinality — this model is for invocation tracking only, not a
    persistent entity.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    invoking_actor_id: str
    """Actor invoking the test (e.g., practitioner-record id for self-
    test; L8 auditor identity for audit invocation; regulator id for
    challenge invocation)."""

    tested_claim_ids: tuple[str, ...]
    """Claims under test per §2.2 claim-granularity resolution
    (defensibility resolves at claim granularity per `glossary/
    defensibility.md`)."""

    per_claim_outcomes: dict[str, bool] = Field(default_factory=dict)
    """Per-claim test outcome (True = defensible; False = indefensible).
    Composability per §3: ONE indefensible claim taints the work-unit's
    output regardless of other claims passing.
    """

    reasoning_chain_ref: str | None = None
    """Reference to reconstructed reasoning chain (audit-trail query
    result per `arch/audit.md` §C); enables L8 auditor reasoning-chain
    reconstruction per `arch/audit.md` §A query primitive."""
