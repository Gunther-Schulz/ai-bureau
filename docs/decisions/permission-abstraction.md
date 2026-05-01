# Decision record: Unified PBS permission abstraction (R3c from #21 SDK deep-read)

**Status**: ACCEPTED — session 12 (2026-04-30); 2-round sharpening (full monty + T1-T8 schema/lifecycle refinements) + M5 from R3a round 2 (MCP server registration governance) + P1 + P5 + P2 from R3d round 3 (subagent permission inheritance + identity routing + sparring bypass authority chain)
**Owner**: ROADMAP commitment #21 (SDK deep-read R3c); architectural foundation for all human-authority gates
**Related**: `substrate-agentic-framework.md` (#18 — Substrate Protocol where this method lives), `sdk-deep-read.md` (#21 — origin findings), `governance-and-identity-sourcing.md` (governance gate composes here), `sparring-output-v1.md` (sparring backstop composes here), `audit-trail-v2.md` (permission events emit AuditEvents), `office-level-managed-entities.md` (#15 — Actor.roles for routing; PermissionRequest entity at Tier 2+), `mcp-fallback-policy.md` (fail-closed corollary applies), `in-process-mcp-server.md` (R3a — `ToolExecutionContext.transport_mode` field references TransportMode), `eval-framework-adoption.md` (R3b — eval validates permission flow AuditEvents)

## Context

PBS has multiple "human-authority gates" patterns that currently don't share infrastructure:

- **Governance gate**: tier-conditional write authorization (per `governance-and-identity-sourcing.md` decision 1)
- **Sparring backstop**: 3x-fail bypass-with-reason (per `sparring-output-v1.md` v0.29)
- **Send gate**: confirmation before external transmission (per VISION axis 1)
- **Four-way decision menu**: capture / handle / backlog / drop (per orchestrator)
- **Lifecycle transition**: state machine state advances require explicit acknowledgment
- **Tool execution control**: destructive operations need permission (per R3a in-process gates)
- **Multi-user approval**: `approval_requested` / `granted` / `rejected` event kinds (per #6 audit-trail v2)

Claude Agent SDK provides rich permission primitives (`CanUseTool`, `PermissionMode`, `PermissionResult` Allow/Deny, `ToolPermissionContext`, `PermissionRequestHookInput/Output`). MS AF provides equivalents via 3-layer middleware + HITL approval (`ApprovalRequiredAIFunction`, `RequestInfoEvent` with `ToolApprovalRequestContent`).

The R3c question: adopt these primitives as unified backbone for ALL human-authority gates, or per-gate hand-rolled patterns?

## Decision

**Unified PBS permission abstraction (Option C). `Substrate.request_permission()` Protocol method as architectural backbone for ALL human-authority gates. Substrate dispatches to native primitives.**

Per "Make wrong shapes impossible" (v0.21): structural enforcement = ONE way to request permission across the architecture; substrate dispatches; no per-feature hand-rolling drift.

### Substrate Protocol method

```python
class PermissionDecisionKind(Enum):
    GOVERNANCE_WRITE = "governance_write"
    SPARRING_BYPASS = "sparring_bypass"
    EXTERNAL_SEND = "external_send"
    FOUR_WAY_DECISION = "four_way_decision"
    LIFECYCLE_TRANSITION = "lifecycle_transition"
    TOOL_EXECUTION = "tool_execution"
    MULTI_USER_APPROVAL = "multi_user_approval"

class PermissionDecision(BaseModel):
    decision: Literal["allow", "deny", "deferred"]
    reasoning: str = Field(min_length=10)  # human-readable justification
    actor_id: str
    decision_kind: PermissionDecisionKind
    context: dict[str, Any]  # decision-kind-specific (typed via PermissionRequestContext discriminated union)
    timestamp: datetime
    audit_event_id: str  # ties decision to its AuditEvent record
    expires_at: datetime | None = None  # T6: time-bound decisions
    delegated_from: ActorId | None = None  # T7: Tier 2/3 delegation
    revoked_at: datetime | None = None  # T3: revocation timestamp
    revocation_reason: str | None = None  # T3: revocation justification
    inherited_from_parent: bool = False  # P1: subagent inheriting from parent orchestrator (R3d)

class Substrate(Protocol):
    async def request_permission(
        self,
        decision_kind: PermissionDecisionKind,
        context: PermissionRequestContext,  # discriminated union per decision_kind
    ) -> PermissionDecision: ...
```

### Per-`PermissionDecisionKind` Context schemas (T1)

```python
class GovernanceWriteContext(BaseModel):
    entity_type: str  # e.g., "planning.project", "mcp_server" (per R3a M5)
    entity_id: str
    requested_action: Literal["create", "update", "delete", "register"]  # "register" added per R3a M5 for MCP server governance
    current_actor: ActorId
    field_changes: dict[str, Any] | None  # for update operations
    # When entity_type="mcp_server", context includes: server_name, transport, tool_names, source (skill/marketplace)

class SparringBypassContext(BaseModel):
    skill_name: str
    output_attempt: dict  # the failing output
    validation_failure_history: list[FailureRecord]  # 3x failure detail
    requested_bypass_reason: str = Field(min_length=20)

class ExternalSendContext(BaseModel):
    recipient: str
    content_summary: str  # not full content (PII concerns); summary for permission UI
    project_id: str
    transport: Literal["unb_submission", "email", "api_post", "other"]
    snapshot_id: str  # for defensibility — exact content snapshot

class FourWayDecisionContext(BaseModel):
    item: dict  # the captured item
    applicable_options: list[Literal["capture", "handle", "backlog", "drop"]]
    suggested_default: Literal["capture", "handle", "backlog", "drop"] | None

class LifecycleTransitionContext(BaseModel):
    entity_type: str
    entity_id: str
    from_state: str
    to_state: str
    triggering_event: str

class ToolExecutionContext(BaseModel):
    tool_name: str
    args_summary: dict  # not full args (may be large)
    called_by_skill: str
    transport_mode: Literal["in_process", "subprocess"]  # composes with R3a TransportMode

class MultiUserApprovalContext(BaseModel):
    subject_entity_type: str
    subject_entity_id: str
    requested_action: str
    required_approvers: list[ActorRoleQuery]  # role-based routing
    deadline: datetime | None
    preliminary_context: dict

# All context types may include:
# originating_subagent_id: str | None  # P5: when subagent (acting on behalf of parent's actor) requests permission (R3d)
```

### Subagent permission inheritance (P1 from R3d round 3)

When subagent (spawned by orchestrator) requests permission, inheritance behavior depends on decision kind:

| PermissionDecisionKind | Inheritance behavior in subagent context | Reason |
|---|---|---|
| `GOVERNANCE_WRITE` | RE-PERMISSION required in subagent | Potentially destructive; subagent context isolation |
| `EXTERNAL_SEND` | RE-PERMISSION required in subagent | External transmission must be re-authorized |
| `LIFECYCLE_TRANSITION` | RE-PERMISSION required in subagent | State machine advances cross subagent boundary |
| `TOOL_EXECUTION` | INHERITED from parent (with `inherited_from_parent=True`) | Sandboxed within subagent's scope; parent already authorized tool universe |
| `FOUR_WAY_DECISION` | INHERITED from parent | Decision menu items scoped to parent's task |
| `SPARRING_BYPASS` | RE-PERMISSION required AT PARENT (not subagent — see P2) | Bypass authority lives with parent orchestrator |
| `MULTI_USER_APPROVAL` | RE-PERMISSION required in subagent | Multi-user routing must re-evaluate per subagent action |

`PermissionDecision.inherited_from_parent: bool` records inheritance status. Audit-trail records which decisions were inherited vs re-permission for defensibility.

### Sparring bypass authority chain (P2 from R3d round 3)

When subagent produces output failing sparring schema 3x:
- Subagent emits `sparring_bypass_proposed` AuditEvent
- Parent orchestrator receives proposal; surfaces to user via `SPARRING_BYPASS` permission flow
- User approves at orchestrator scope (not subagent scope)
- Subagent receives approval token; bypass authorized
- Subagent CANNOT self-bypass (architectural integrity per VISION axis 2)

Authority chain: subagent → parent orchestrator → user. Documented in R3d for full reasoning.

### Subagent identity for multi-user permission routing (P5 from R3d round 3)

When subagent requests permission requiring multi-user approval:
- Subagent inherits parent orchestrator's actor identity (`current_actor` field)
- Subagent does NOT have separate user identity
- `PermissionRequestContext.originating_subagent_id` field records subagent that triggered request (audit clarity; routing unchanged)
- Required-approvers routing per parent's actor's roles + action's required-approvers

Pydantic discriminated union via `decision_kind` field on `PermissionRequestContext` wrapper.

### Per-substrate impl

| Substrate | Mechanism |
|---|---|
| Claude Agent SDK | Dispatches to `CanUseTool` callback + `PermissionResult` types; uses `PermissionRequestHookInput/Output` for hook surface |
| MS AF | Dispatches to agent middleware + HITL approval (`ApprovalRequiredAIFunction` / function approval) |
| Hand-rolled (Tier 1 fallback) | Synchronous prompt + audit-trail emit |

## PermissionRequest as entity at Tier 2+ (T2)

Architectural distinction surfaced by stress-testing:

- **Tier 1 (single-user synchronous)**: PermissionRequest = immediate-resolved event (request → response in single async call). Just AuditEvents; no entity lifecycle.
- **Tier 2+ (multi-user async)**: PermissionRequest = managed entity (`type: office.permission_request`). Lifecycle: REQUESTED → ROUTED → AWAITING_RESPONSE → (PARTIAL_APPROVED for multi-approver) → FINAL_DECIDED.

Per entity-elevation 3-test for Tier 2+:
- Stable identity: yes (request_id UUID)
- State of record: yes (current state of pending request)
- Lifecycle: yes (REQUESTED → ... → FINAL_DECIDED)

Substrate Protocol method handles both shapes (returns immediately at Tier 1; returns request_id for polling at Tier 2+ async case). Composes with #15 office-level managed entities + entity-md-spec.

## Tier-conditional behavior

| Tier | Behavior |
|---|---|
| **Tier 1 (single-user local)** | Most permission kinds auto-allow + audit-trail emit; only EXTERNAL_SEND + FOUR_WAY_DECISION require interactive prompt |
| **Tier 2 (multi-user cloud)** | Governance/multi-user kinds activate role-check + approval workflow per Actor.roles; others tier-1-shaped |
| **Tier 3 (federated)** | Cross-org approval flows; A2A signed permission requests |

Per `governance-and-identity-sourcing.md` decision 1: tier-conditional role enforcement built once, activates at Tier 2.

## Scheduled / autonomous flow handling (T5)

What happens when substrate can't reach user (scheduled task fires at 3am; user absent)?

```python
class PermissionMode(Enum):
    INTERACTIVE_REQUIRED = "interactive_required"  # default; must reach user; fail-closed if no user
    AUTONOMOUS_ALLOWED = "autonomous_allowed"      # pre-configured policy auto-allows (with audit-trail)
    AUTONOMOUS_DEFERRED = "autonomous_deferred"    # queues for next user-present moment
```

Per-decision-kind policy configured per office-config (e.g., scheduled deadline-warning emission can be `AUTONOMOUS_ALLOWED`; scheduled UNB-submission must be `INTERACTIVE_REQUIRED` or fail).

Composes with: #13 Gap A scheduler (`register_scheduled_trigger`), audit-trail-v2 (autonomous decisions emit `actor_kind=external_agent` per #10), tier-conditional behavior.

## Dev-mode escape hatch (T4)

For development/debugging, devs might want to bypass interactive permission flows. Per fail-closed corollary: NO silent bypasses.

- Environment variable `PBS_DEV_AUTO_ALLOW=true` (NOT a config setting; explicit env)
- When set: substrate auto-allows BUT emits LOUD AuditEvent: `event_kind=permission_dev_mode_bypass` with `actor_kind=developer_override`, `dev_mode_reason` (env reason), full context preserved
- Audit slice 22 (wrong-shapes-solvable scan) flags any deployment where `PBS_DEV_AUTO_ALLOW` is set in production
- Documented escape hatch (per "make wrong shapes impossible" — visible-by-construction, not hidden)

## Permission UI rendering (T8)

Substrate impls render permission requests in their native UI. PBS provides `PermissionUIPayload`:

```python
class PermissionUIPayload(BaseModel):
    prompt: str  # human-readable request
    sparring_payload: ReviewOutput | RecommendationOutput | None  # sparring-shaped UI
    action_options: list[str]  # available decisions (allow/deny + decision-kind-specific)
    context_summary: dict  # decision-relevant context for user
```

Substrate dispatches through native UI primitives (Claude Agent SDK = via Cowork-native UX or Claude Code prompts; MS AF = AG-UI integration).

## Permission gates vs Quality gates — architectural distinction (NEW round 1 R10)

R3c surfaces a distinction not previously explicit in ARCH:

| Gate type | Definition | Examples | R3c covers? |
|---|---|---|---|
| **Permission gate** | Decision: should this action proceed? Allow/Deny based on authority + context | Governance write, sparring bypass, send, four-way, lifecycle, tool execution, multi-user approval | ✅ All unified under `request_permission` |
| **Quality gate** | Check: does this artifact meet quality criteria? Pass/Fail based on validation | Compile gate, layered review gate, verify-citations, sparring schema validation, structural conformance | ❌ Different mechanism (validation, not permission) |

Permission gates ask AUTHORITY; quality gates ask CONFORMANCE. R3c unifies the former; R3b operates in the latter space. To be added as architectural distinction in ARCH (reference card row + brief discipline note) per comprehensive doc review post-#22.

## Sparring-shaped permission UI (R5 from round 1)

When permission requests are surfaced to user, they should be SPARRING-SHAPED (not oracle-mode prompts). Permission UI uses sparring patterns:
- "I want to do X. Counter-argument against doing X: Y. Confidence: Z. Reasoning: W."
- User decides with full context
- Anti-sycophancy applied to the permission ASK itself

`PermissionRequestContext.sparring_payload` field for sparring view.

## Audit-trail integration (R2 from round 1 + T3 revocation)

Every `request_permission` call + decision emits AuditEvents:

| Event kind | Emitted when |
|---|---|
| `permission_requested` | Every request (audit-trail entry created with request_id) |
| `permission_granted` | Decision = allow |
| `permission_denied` | Decision = deny |
| `permission_revoked` (T3) | Previously-granted decision revoked |
| `permission_dev_mode_bypass` (T4) | Dev-mode escape hatch triggered |

`audit_event_id` field on `PermissionDecision` ties decision to its audit record. Defensibility comes from audit-trail integration: "what was decided when, by whom, with what reasoning, in what context."

## Permission decisions are EVENTS, not entities (R8 from round 1)

Applying entity-elevation 3-test:
- Stable identity: yes (UUID per decision; persisted in audit-trail)
- State of record: NO — decisions are timestamped + immutable; history matters but no evolving state per decision
- Lifecycle: NO — no phases per decision

**Verdict**: NOT a managed entity. Permission decisions are AuditEvents. Composes with existing pattern; no entity-md sprawl.

(Distinct from PermissionRequest at Tier 2+ which IS entity per T2.)

## Composition with existing architecture

| Concern | R3c interaction |
|---|---|
| `governance-and-identity-sourcing.md` decision 1 | R3c PROVIDES the gate-level enforcement infrastructure |
| `sparring-output-v1.md` v0.29 | R3c EMITS `sparring_bypass` AuditEvent via permission flow |
| #6 audit-trail v2 retrofit | R3c EMITS `approval_requested/granted/rejected` events + `permission_*` events |
| #15 Actor entity | R3c routes multi-user approvals via Actor.roles |
| `mcp-fallback-policy.md` | R3c fails-closed on substrate unreachable |
| ARCH "Make wrong shapes impossible" (v0.21) | R3c IS the structural enforcement of human-authority gates |
| VISION axis 1 ("explicit human-authority gates") | R3c is the IMPLEMENTATION of this mechanism |
| #11 Cowork integration | R3c's permission UI may adopt Cowork-native consent patterns |
| #13 Gap A scheduler + Gap B adapter callbacks | Scheduled/autonomous flow handling per T5 |
| R3a TransportMode | `ToolExecutionContext.transport_mode` references TransportMode; permission fires BEFORE tool dispatch |
| R3b eval framework | Permission flows generate AuditEvents R3b's `audit_event_emitted_check` validates |

## Phase 0 scope

1. `Substrate.request_permission()` Protocol method definition (lands in #9 Substrate Protocol design)
2. `PermissionDecisionKind` enum + `PermissionDecision` Pydantic type
3. Per-kind context schemas (7 schemas)
4. Hand-rolled substrate impl (Tier 1 default)
5. Claude Agent SDK substrate impl (delegates to `CanUseTool` + `PermissionResult`)
6. Wire 3 initial gates through abstraction: SEND_GATE + FOUR_WAY_DECISION + LIFECYCLE_TRANSITION
7. Audit-trail integration (emit `permission_requested` / `permission_granted` / `permission_denied` events)

## Decisions + phase routing (re-examined session 15 under v0.33 no-defer principle)

> **Session 15 amendment**: previously titled "Defers (chronological-valid)" with 14 entries. Re-examined under v0.33 no-defer principle: 6 entries reframed as decisions made now (effort-asymmetry test failed; could decide today); 8 entries are phase routing (work scheduled to specific implementation phase per ROADMAP queue, not chronological gaps). Per v0.33 preliminary-lock: this DR remains preliminary-locked.

### Decisions made now (D6, D7, D9, D10, D11, D12)

**D6 (was defer): Permission caching via PermissionMode** — DECISION: v1 does NOT cache permissions (always-fresh permission request). v2+ may add caching as performance optimization when concrete need surfaces (e.g., real workload shows permission flow as latency hotspot).

**D7 (was defer): PermissionRequest as managed entity** — DECISION: v1 does NOT elevate PermissionRequest to managed entity (per entity-elevation 3-test: lifecycle is single-action; no state-of-record needs persistence beyond audit-trail; no stable identity referenced by other entities). PermissionRequest stays as in-flow data + AuditEvent record. v2+ may revisit if Tier 2 multi-user surfaces lifecycle need.

**D9 (was defer): Conditional permission ("allow IF" semantics)** — DECISION: v1 does NOT support conditional permissions. PermissionDecision is binary (allow/deny) with optional reason text. v2+ may add conditional grants when concrete use case surfaces with specific constraint shape.

**D10 (was defer): Bulk permissions (multi-decision batch)** — DECISION: v1 does NOT support bulk permissions. Each PermissionDecisionKind requested individually via `request_permission`. v2+ may add bulk shape when real workflow patterns surface (e.g., layered review with N items requiring same authorization).

**D11 (was defer): Propose vs execute two-stage permission** — DECISION: v1 single-stage permission (propose+execute coupled). v2+ may add two-stage when concrete use case surfaces requiring "AI proposes; user authorizes proposal; AI executes authorized proposal" semantics distinct from "AI requests; user authorizes; AI proceeds".

**D12 (was defer): Denial appeals mechanism** — DECISION: v1 supports re-request with additional context (skill receives PermissionDeniedError; can include user-feedback context in next request). No formal appeals mechanism. v2+ may add formal appeals when audit-trail accumulates patterns showing appeal need.

### Phase routing (work scheduled per implementation queue)

| Item | Phase |
|---|---|
| MS AF substrate impl of `request_permission` (was D1) | Per #18 dual-substrate plan; sequenced with #11/#13 |
| Tier 2 multi-user approval workflows (was D2) | #13 deployment flexibility |
| Tier 3 A2A signed permission requests (was D3) | #10 A2A interop expansion (Tier 3 trigger) |
| Design-review target "permission gate coverage scan" (was D4) | Post-#9 implementation when permission flow has multiple call sites; bundled with #9 design-review ripple |
| Cowork-native consent UI integration (was D5) | #11 Cowork integration phase |
| Permission revocation flow implementation (was D8) | #6 audit-trail v2 retrofit (bundled with approval events ship) |
| Rate limiting / cost protection (was D13) | #13 Tier 2 multi-user deployment |
| PII handling / encryption in permission contexts (was D14) | #13 deployment-instance per existing PII defer |

### Re-examination methodology

D6, D7, D9-D12 had generic "defer to specific use case need" / "Too complex for Phase 0" / "Premature optimization" framings — failed external-information test (no specific external signal named). Could decide today (effort-asymmetry test failed). Reframed as v1 decisions with v2+ revisit triggers.

D1-D5, D8, D13-D14 are scheduled to specific implementation phases per ROADMAP queue — phase routing, not chronological gaps.

## Constraints flowing to downstream commitments

- **→ #9 (Substrate Protocol design)**: `request_permission()` method definition + `PermissionDecisionKind` enum + `PermissionDecision` + 7 per-kind context schemas
- **→ governance-and-identity-sourcing.md**: R3c IS the gate-level enforcement infrastructure for decision 1
- **→ sparring-output-v1.md**: R3c emits `sparring_bypass` via permission flow (per v0.29 amendment)
- **→ #6 audit-trail v2 retrofit**: event kinds added: `permission_requested`, `permission_granted`, `permission_denied`, `permission_revoked`, `permission_dev_mode_bypass`; existing approval events flow through R3c
- **→ #15 office-level entities**: Actor.roles for routing; `office.permission_request` entity at Tier 2+
- **→ #11 Cowork integration**: permission UI integration (Cowork-native consent patterns)
- **→ #13 deployment flexibility**: Tier 2 multi-user; Tier 3 A2A; PermissionMode policy per office-config
- **→ R3a (TransportMode)**: `ToolExecutionContext.transport_mode` field references TransportMode
- **→ R3b (eval framework)**: eval validates permission flow AuditEvents
- **→ ARCHITECTURE.md**: Permission gates vs Quality gates architectural distinction (reference card row + brief discipline note); deferred to comprehensive doc review post-#22

## Revisit triggers

- **Claude Agent SDK changes permission primitives** → re-validate Substrate impl
- **MS AF changes middleware shape** → re-validate Substrate impl
- **First Tier 2 deployment surfaces multi-user approval workflow friction** → re-evaluate routing
- **First scheduled task scenario surfaces autonomous flow friction** → re-evaluate PermissionMode shape
- **Sparring backstop ships per `sparring-output-v1.md` v0.29** → SPARRING_BYPASS gate wires up
- **TOOL_EXECUTION gate need surfaces** (R3a destructive actions) → wires up
- **First permission revocation use case** → revocation flow implementation proceeds

## Files touched

- `docs/decisions/permission-abstraction.md` — this file (NEW; status ACCEPTED)
- `sdk-deep-read.md` — updated to reference this DR as detailed implementation
- `ARCHITECTURE.md` — Permission gates vs Quality gates architectural distinction (deferred to comprehensive doc review post-#22)
- `audit-trail-v2.md` — event kinds addition (with #6 retrofit)
