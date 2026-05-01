---
id: practitioner-judgment-trust
label: Practitioner-Judgment Trust Model
type: protocol
status: active
last_updated: 2026-05-01

framework_kind: protocol
framework_key: practitioner-judgment-trust

display_name: Practitioner-Judgment Trust Model
protocol_kind: trust
semver: "0.1.0"
pydantic_class: extensions.framework.protocols.practitioner_judgment_trust.PractitionerJudgmentTrustProtocol

shape_compat:
  - practitioner

substrate_compat:
  - claude-agent-sdk
  - ms-agent-framework

option_b_axiom: null

failure_modes:
  - mode: send_without_explicit_confirmation
    recovery: gate_blocks_external_transmission; require_user_send_confirmation_step
  - mode: lifecycle_transition_silent
    recovery: gate_blocks_state_advance_without_acknowledgment
  - mode: four_way_decision_skipped
    recovery: orchestrator_pauses_at_decision_point; surface_to_user
---

# Practitioner-Judgment Trust Model Protocol

## What this implementation does

Trust between practitioner and AI cooperation is bounded by **practitioner judgment** — not by budget caps (autonomous-business shape) or implicit trust (personal-OS). The practitioner explicitly authorizes accountability-bearing decisions; AI never proceeds unilaterally on accountability moments.

Concrete enforcement mechanisms (per VISION axis 1 intertwining-requirements + axis 2 sparring-requirements):

- **Four-way decision menu** (capture / handle / backlog / drop) at every memory-write or backlog-append. Practitioner explicitly chooses; AI never silently captures.
- **Send gate** (compile-then-send): explicit practitioner confirmation before any external transmission. AI prepares; practitioner reviews; practitioner sends.
- **Compile gate**: explicit confirmation before compiling drafts to artifacts (LaTeX → PDF, etc.). Catches errors before they propagate to send.
- **Layered review gate**: structural / fachlich / formal review layers; practitioner-driven, AI-supported.
- **State-transition gate**: lifecycle phase transitions require explicit acknowledgment. No silent state advancement.
- **Selective friction calibration** (per VISION axis 2): friction at accountability moments + judgment moments; mechanical work automated seamlessly.

This Protocol implements `default_configs.trust_model: practitioner-judgment` for practitioner shape. Other shapes use different trust models (autonomous-business: budget-policy; personal-OS: individual; knowledge-graph: corpus-trust).

## Configuration knobs

- **`send_gate_required_actors: list[str]`** (default `["accountability-bearer"]`) — which actor roles must confirm send; default = the practitioner who authors the output
- **`lifecycle_acknowledgment_required: bool`** (default `true`) — whether state transitions require explicit acknowledgment
- **`four_way_menu_threshold: enum`** (default `all`) — when to surface four-way menu: `all` (every memory candidate) / `large_only` (only substantial candidates) / `flagged` (only AI-flagged-as-uncertain)
- **`mechanical_automation_threshold: SkillCategory`** — which skill categories are auto-executed without explicit confirmation (e.g., `format-cleanup`, `citation-lookup`); accountability-moments always confirm

## Compat constraints

**Shapes**:
- ✅ practitioner (default trust Protocol; load-bearing per VISION axes 1 + 2 + 3)
- ❌ autonomous-business — uses `budget-policy-trust` (operator authorizes budget caps; AI executes within bounds; per-output authorization not required)
- ❌ personal-OS — uses `individual-trust` (single human; lighter gates; no external accountability concern)
- ❌ knowledge-graph — uses `no-trust-protocol` (corpus + retrieval; no decision-bearing transitions)
- ⚠ federation / hybrid — depends on per-node / per-composition trust posture

**Substrates**:
- ✅ Claude Agent SDK — gates implemented as CASDK CanUseTool callbacks + permission flow; four-way menu UX in skill body
- ✅ MS Agent Framework — gates implemented as MS AF agent middleware + ApprovalRequiredAIFunction; four-way menu UX in skill body

## Failure modes + recovery

| Mode | Detection | Recovery |
|---|---|---|
| Send without explicit confirmation | Gate detects external transmission attempt without prior `user_confirmation` AuditEvent | Block transmission; require user send-confirmation step; emit `unauthorized_send_attempted` event |
| Lifecycle transition silent | Gate detects state.md.lifecycle change without acknowledgment AuditEvent | Block state advance; surface to user for explicit acknowledgment |
| Four-way decision skipped | Orchestrator detects memory-write attempt outside menu flow | Pause at decision point; surface menu to user; never silently capture |
| Compile gate bypassed | Gate detects artifact compile without confirmation | Block compile; require explicit confirmation step |
| Layered review skipped | Gate detects send attempt without all review layers having run | Block; require completing review layers OR explicit-bypass-with-reason (with audit emission) |

## Option B axiom binding

`option_b_axiom: null` — trust model is configurable per shape (practitioner-judgment / budget-policy / none / individual). Not one of the 3 non-overridable axioms.

However, **practitioner-judgment trust composes with axiom 3** (human authority somewhere in accountability-bearing output chain): for practitioner shape, the human authority granularity is `per-output` (every external send requires practitioner confirmation) — this Protocol's send gate IS the per-output enforcement. Other shapes with different `author_primitive` configs (per-decision-class / per-policy / per-budget-cycle) implement axiom 3 differently but must implement it.

## Migration / version evolution

v0.1.0 — initial implementation; gates as substrate-permission-flow + skill-body-orchestration.

**Future versions**:
- v0.2.0 (compile gate as MCP tool): if compile gate logic centralizes, may extract to MCP tool with structured Pydantic input/output (per validation-layering deterministic-primary discipline)
- v0.3.0 (audit-driven gate review): retrospective gate-bypass analysis if `feedback_pattern_not_instance_defers` mechanism surfaces gate-bypass patterns warranting structural changes

## Cross-references

- `VISION.md` axes 1+2+3 — intertwining requirements + sparring selective-friction calibration + authorship preservation gates
- `docs/decisions/audit-trail-v2.md` — `user_confirmation` event kind; gate emission contract
- `docs/decisions/sparring-output-v1.md` — `RecommendationOutput` for orchestrator's commit-to-recommendations
- `docs/decisions/governance-and-identity-sourcing.md` — gate-vs-prose-convention boundary
