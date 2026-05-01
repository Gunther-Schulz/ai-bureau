---
id: always-on-sparring
label: Always-On Sparring
type: protocol
status: active
last_updated: 2026-05-01

framework_kind: protocol
framework_key: always-on-sparring

display_name: Always-On Sparring
protocol_kind: sparring
semver: "0.1.0"
pydantic_class: extensions.framework.protocols.always_on_sparring.AlwaysOnSparringProtocol

shape_compat:
  - practitioner

substrate_compat:
  - claude-agent-sdk
  - ms-agent-framework

option_b_axiom: null

failure_modes:
  - mode: counter_argument_field_empty
    recovery: gate_rejects_review_output; skill_must_resubmit_with_counter_argument
  - mode: confidence_basis_field_short
    recovery: gate_rejects_if_below_min_length; skill_must_provide_substantive_basis
  - mode: sparring_attempted_in_oracle_context
    recovery: emit_warning_audit_event; permit_oracle_mode_for_designated_skills_only
---

# Always-On Sparring Protocol

## What this implementation does

Sparring as **load-bearing runtime mechanism** (per VISION axis 2). Counter-argument is FIRST-CLASS output for every accountability-bearing AI generation in the workspace. Confidence calibration always required. Visible reasoning always required. "What's missing?" checkpoint always present.

Concrete enforcement (per `sparring-output-v1.md`):
- `ReviewOutput.counter_argument: str (min_length=100)` — Pydantic schema requires substantive counter-argument; gate rejects empty/short
- `ReviewOutput.confidence: ConfidenceLevel` + `confidence_basis: str (min_length=100)` — calibrated confidence with substantive basis
- `ReviewOutput.reasoning: str (min_length=100)` — visible reasoning chain
- `ReviewOutput.whats_missing: str (min_length=50)` — explicit absence-of checkpoint

Plus behavioral mechanisms (per VISION axis 2 sparring requirements; not yet structurally enforced — chronological-defer awaiting empirical pattern data per `greenfield-architecture-review.md` §3):
- Anti-sycophancy guard (orchestrator doesn't capitulate without reason)
- Asymmetric knowledge respect (AI surfaces "here's what I'm drawing on; might be a case where local context I don't have should change the conclusion")
- Commit-to-recommendations (orchestrator surfaces decisions as recommendation + tradeoff, not open menu)

Per Vivienne Ming research foundation (per VISION axis 2): only sparring mode produces value; oracle mode wastes the human partner; validator mode actively degrades. Always-on enforcement prevents drift toward oracle/validator modes.

## Configuration knobs

- **`min_counter_argument_length: int`** (default `100`) — minimum chars for counter-argument; below threshold rejected by gate
- **`min_confidence_basis_length: int`** (default `100`) — minimum chars for confidence basis
- **`oracle_mode_skills: list[str]`** (default `[]`) — skill ids exempt from sparring requirements (oracle mode acceptable for fact-lookup type skills like `verify-citations`); empty by default per always-on
- **`anti_sycophancy_threshold: int`** (default `5`) — number of real sparring sessions required before structural elevation of anti-sycophancy guard considered (per chronological-defer; awaiting empirical pattern data)

## Compat constraints

**Shapes**:
- ✅ practitioner (default sparring Protocol; load-bearing per VISION axis 2)
- ❌ autonomous-business — uses `optional-sparring` (operator can request sparring per-task; default off because autonomous-business is operator-supervised, not practitioner-engaged)
- ❌ personal-OS — uses `sparring-as-skill` (sparring optional, called per-task)
- ❌ knowledge-graph — uses no sparring Protocol (corpus + retrieval; no workflow loop where sparring engages)
- ⚠ federation — depends on per-node shape; if federation node is practitioner-shape, always-on-sparring applies
- ⚠ hybrid — depends on hybrid composition; explicit per hybrid extension

**Substrates**:
- ✅ Claude Agent SDK — sparring schemas materialize as CASDK output_schema validation
- ✅ MS Agent Framework — sparring schemas materialize as MS AF response format + Pydantic validator integration

## Failure modes + recovery

| Mode | Detection | Recovery |
|---|---|---|
| Counter-argument field empty / below min_length | Gate Pydantic validation at write-time | Reject ReviewOutput; skill must resubmit with substantive counter-argument |
| Confidence basis below min_length | Gate Pydantic validation | Reject; skill must provide substantive basis (not just "high" without explanation) |
| Sparring attempted in oracle-mode context | Skill in `oracle_mode_skills` list shouldn't try to emit ReviewOutput | Warning AuditEvent; permit (orclcle mode skills are exempt) |
| 3x bypass for valid reason (per `sparring-output-v1.md` session-11 amendment) | After 3 failed attempts, explicit-bypass-with-reason allowed | Emit `sparring_bypass` AuditEvent with reason; ReviewOutput accepted with bypass flag; reviewable in audit-trail |

## Option B axiom binding

`option_b_axiom: null` — sparring intensity is configurable per shape (always-on / optional / none); not one of the 3 non-overridable axioms. The structural floor's 3 axioms are anti-Art-25-trap + claim-level audit + human authority chain. Sparring intensity is a separate configurable axis.

However, for **practitioner shape specifically**, sparring-always-on is load-bearing per VISION axis 2. Other shapes legitimately don't need always-on (operator-supervised AI workforce uses different interaction mode).

## Migration / version evolution

v0.1.0 — initial implementation; ReviewOutput + RecommendationOutput schemas; min_length validators; bypass mechanism with audit emission.

**Future versions**:
- v0.2.0 (anti-sycophancy structural elevation): when 5-10 real sparring sessions accumulate empirical data (per `greenfield-architecture-review.md` §3), evaluate structural detection of legitimate-update vs sycophantic-capitulation; promote anti-sycophancy guard from behavioral to structural per validation-layering discipline
- v0.3.0 (asymmetric knowledge respect structural): same chronological pattern; structural elevation pending empirical context-sensitivity data

## Cross-references

- `VISION.md` axis 2 — sparring as load-bearing runtime mechanism (Vivienne Ming foundation)
- `docs/decisions/sparring-output-v1.md` — ReviewOutput + RecommendationOutput schemas + bypass mechanism
- `docs/decisions/greenfield-architecture-review.md` §3 — chronological-defer reasoning for behavioral mechanisms (anti-sycophancy + asymmetric-respect)
- `docs/decisions/counter-vision-engagement.md` — substantive engagement with opposing service-as-software thesis; PBS rejects oracle-replacement framing
