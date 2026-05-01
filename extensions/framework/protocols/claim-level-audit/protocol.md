---
id: claim-level-audit
label: Claim-Level Audit
type: protocol
status: active
last_updated: 2026-05-01

framework_kind: protocol
framework_key: claim-level-audit

display_name: Claim-Level Audit
protocol_kind: audit
semver: "0.1.0"
pydantic_class: extensions.framework.protocols.claim_level_audit.ClaimLevelAuditProtocol

shape_compat:
  - practitioner
  - autonomous-business
  - knowledge-graph
  - federation
  - hybrid

substrate_compat:
  - claude-agent-sdk
  - ms-agent-framework

option_b_axiom: claim_level_audit

failure_modes:
  - mode: claim_emitted_without_sources
    recovery: gate_rejects_audit_event; skill_must_resubmit_with_sources_array
  - mode: sources_reference_unknown_entities
    recovery: gate_rejects_at_write_time; cross_reference_validator_flags
  - mode: causes_chain_broken
    recovery: gate_rejects; require_explicit_root_cause_marker_when_no_parent
---

# Claim-Level Audit Protocol

## What this implementation does

Every claim made by the AI in produced output is bound to evidence at write-time. AuditEvent emission with `sources[]` (where the claim came from) + `causes[]` (what triggered this output) for every accountability-bearing claim.

Concrete enforcement (per `audit-trail-v2.md`):
- `AuditEvent.sources: list[SourceRef]` — required for legal/regulatory/factual claims; each SourceRef points to a specific tool result, reference entity, or prior decision
- `AuditEvent.causes: list[CauseRef]` — required for module-decision-bearing claims; each CauseRef points to triggering event (user request, prior event, scheduled trigger)
- Pydantic gate validation at `record_audit_event` MCP tool: empty sources for accountability-bearing event_kinds rejected; cross-reference validator confirms sources/causes point to existing entities
- Substrate-level emission via `_emit_audit_event` for substrate-internal events (mcp_server_registration etc.); skill-level emission via MCP gate for skill-driven events

This is one of the 3 **Option B floor axioms** — structurally enforced regardless of workspace shape (per `shape-extension-and-architectural-floor.md` Part 2). Claim-level audit is the defensibility foundation: VISION axis 3's "user can defend output six months from now" requires reconstructable claim-evidence chain.

## Configuration knobs

- **`accountability_bearing_event_kinds: list[str]`** (default: legal/regulatory/factual claim event kinds) — which event kinds require sources[] populated; configurable per shape but practitioner-shape default includes all citation + reference + decision events
- **`min_sources_per_claim: int`** (default `1`) — minimum source references per accountability-bearing claim
- **`source_freshness_check: bool`** (default `true`) — at emission time, verify sources reference current state (not stale references); reject if source entity has been amended/superseded since claim was generated

## Compat constraints

**Shapes**:
- ✅ practitioner (default; required for accountability-bearing posture per Option B floor)
- ✅ autonomous-business (required even for autonomous AI workforce; output to clients/regulators needs claim-level audit)
- ✅ knowledge-graph (required for citation hygiene)
- ✅ federation (required for cross-node defensibility)
- ✅ hybrid (required regardless of composition)
- **Note**: claim_level_audit IS one of the 3 Option B floor axioms — not optional regardless of shape. Even shapes that configure other axes lighter (action-level audit overlay; sparring optional) cannot disable claim-level audit baseline.

**Substrates**:
- ✅ Claude Agent SDK — sources binding via RunHooks PRE/POST tool emission; cross-ref validator runs in MCP gate
- ✅ MS Agent Framework — sources binding via lifecycle hooks emission; cross-ref validator runs in MCP gate

**Action-level audit overlay** (per practitioner-shape's `protocols_allowed.audit: [claim-level-audit, claim-level-audit-with-action-overlay]`): action-level events (who/what/when/cost) can be ADDED on top of claim-level baseline. claim-level is the structural floor; action-level is optional addition for shapes that want it (e.g., autonomous-business operator wants action-level cost tracking).

## Failure modes + recovery

| Mode | Detection | Recovery |
|---|---|---|
| Claim emitted without sources | Gate Pydantic validation at `record_audit_event` | Reject AuditEvent; skill must resubmit with sources[] populated |
| Sources reference unknown entities | Gate cross-reference validator at write-time | Reject; skill must verify entity ids before claiming |
| Causes chain broken (claim references parent event that doesn't exist) | Gate cross-reference validator | Reject; skill must explicitly mark root-cause events when no parent |
| Source freshness violation | Optional check at emission (per `source_freshness_check` config) | Warning emitted in audit-trail; or reject if config strict |
| Substrate-internal event without sources/causes | Substrate emits via `_emit_audit_event` | Substrate-internal events (e.g., `mcp_server_registration_fallback`) are exempt from sources requirement (substrate has no claim-source distinction) |

## Option B axiom binding

`option_b_axiom: claim_level_audit` — this Protocol IS the implementation of one of the 3 structural axioms. Cannot be disabled regardless of shape configuration. Per `shape-extension-and-architectural-floor.md` Part 2:

> "Claim-level audit emission (decision provenance + sources[] + causes[]) — Defensibility cannot be reconstructed if claims aren't bound to evidence at write-time. Action-level audit is necessary but insufficient. Claim-level always emitted; shapes can ADD action-level overlay."

The axiom binding means: gate validation is non-overridable. Workspace-level config cannot disable claim-level audit. The `option_b_floor_override: NonPBSConformant` workspace.md field (per shape-extension D5 reframe session 15) is the only path to opt out, and it produces non-PBS-conformant deployment.

## Migration / version evolution

v0.1.0 — initial implementation; sources[] + causes[] required fields; cross-reference validator at gate.

**Future versions**:
- v0.2.0 (CloudEvents conformance evaluation): per `a2a-and-gemini-pattern-emulation.md` standards-conformance entry; if cross-system event interop becomes concrete need, sources/causes shape adopts CloudEvents `source` + `subject` fields for cross-system compatibility
- v0.3.0 (PROV-O conformance): if cross-org regulated deployment surfaces requirement (per `a2a-and-gemini-pattern-emulation.md` PROV-O watch position), sources/causes shape evolves to W3C Provenance Ontology compatibility

## Cross-references

- `docs/decisions/audit-trail-v2.md` — AuditEvent schema; record_audit_event MCP tool; cross-reference validator
- `docs/decisions/shape-extension-and-architectural-floor.md` Part 2 — Option B floor 3 axioms; claim-level audit as non-overridable
- `VISION.md` axis 3 — defensibility test; authorship preservation
- `docs/decisions/a2a-and-gemini-pattern-emulation.md` — CloudEvents + PROV-O standards-conformance evaluation
