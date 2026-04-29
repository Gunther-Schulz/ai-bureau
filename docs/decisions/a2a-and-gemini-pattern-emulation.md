# Decision record: A2A schema compatibility + Gemini Enterprise pattern emulation

**Status**: ACCEPTED (session 8, 2026-04-29)
**Owner**: per-session HANDOFF; ARCHITECTURE.md pattern-vs-instance discipline; ROADMAP commitment #10
**Related**: ROADMAP v2 "Gemini Enterprise migration path" (Tier 3 of deployment ladder); commitments #6 (audit-trail v2 retrofit), #11 (Cowork integration), #12 (office-vs-department modularization), #13 (deployment flexibility)

## Context

PBS-bureau is built on a **single-big-model orchestration archetype** (Tiers 1-2 of the deployment ladder per ROADMAP v2). The Linux-Foundation-governed **A2A protocol** v1.0 (Anthropic + Microsoft + Google + AWS + Salesforce + SAP + ServiceNow) defines a different archetype — N agents communicating via signed message-passing — that becomes load-bearing only at Tier 3 (Gemini Enterprise scale: 1000+ users, federated authority, cross-org workflows).

Tier 3 may never be needed. But two facts make pre-RAG decisions about A2A worthwhile anyway:

1. **Schema additions cost nothing now and a lot later.** AuditEvent + ProjectState fields shaped for future A2A-compat are ~1 hour of work pre-RAG; refactoring once thousands of events exist is a migration script + multi-skill retrofit.
2. **Some Google archetypal choices generalize today, regardless of archetype.** Distinguishing skill-as-actor vs human-as-actor in audit events is correct under our archetype too — Google's Agent Identity gestures at a discrimination we should make for our own reasons (#11 plugin agents, #12 departments).

This decision record commits per row of the v2 Gemini Enterprise comparison table what to adopt **proactively now**, what to defer (with documented path), and the concrete defensive schema additions to AuditEvent.

The two-sided framing per ROADMAP commitment #10:

- **Defensive (A) — A2A-shape compatibility**: which schemas should grow A2A-friendly fields now so future migration is cheap?
- **Proactive (B) — pattern emulation**: which Google archetypal choices to adopt within our single-big-model archetype, additively, because they're independently good?

## Decisions per row

The v2 comparison table maps 1:1 to the rows below. Each row gets a verdict, rationale, and (if adopted) the concrete commitment.

### Row 1 — Orchestrator (single Opus session vs N agents via A2A)

**Verdict: stay single-Opus orchestration. Defer internal A2A-shape.**

**Why**: forcing internal skill→agent calls into A2A message envelope introduces protocol overhead (serialize/deserialize, transport abstraction) with zero current consumer. Commitment #11 adds plugin agents (`research-references-fetcher`, `audit-slice-runner`, `design-review-target-runner`) as worker delegates — they're not A2A peers; they're skill-internal subagents. The "same protocol internal + external" elegance argument is speculative; the cost (every internal invocation pays envelope construction) is concrete.

**What's defensive about deferring**: AuditEvent's `actor_kind` discrimination (Row 5 below) is the field that would need to move differently if we adopted A2A internally. By adopting `actor_kind` now (skill / human / external_agent), we preserve the option to retrofit internal calls as A2A messages later — the audit trail already distinguishes the right categories.

**Revisit trigger**: a concrete second consumer of skill outputs emerges (a non-MCP frontend, or a cross-process department coordinator) and the call shape would need to be serializable across that boundary anyway.

### Row 2 — Backend transport (local stdio vs HTTP managed)

**Verdict: adopt HTTP MCP alongside stdio. Implementation in commitment #13, not here.**

**Why**: Tier 2 of the deployment ladder (cloud-hosted container, same archetype, multi-user-per-office) is realistic near-term for consulting engagements. Anthropic's `legal` plugin (knowledge-work-plugins) demonstrates the Cowork pattern for HTTP MCP via custom connectors (`mcp.box.com` etc.). Our backend needs the same dual-transport shape: stdio for solo/local, HTTP for cloud-deployed clients.

**What #10 commits**: the **decision** to support both transports as pluggable layers. Concrete implementation is commitment #13's pre-RAG scope (deployment flexibility + Coolify reference deployment + multi-user readiness).

**What #10 does NOT commit**: an actual HTTP endpoint, auth scheme, or session model. Those are #13.

### Row 3 — Persistent state (state.md vs Memory Bank)

**Verdict: stay with current taxonomy. Defer session-spanning office-memory concept.**

**Why**: our memory taxonomy (universal × domain × state × project, plus department once #12 lands) is already richer along orthogonal axes than Memory Bank's flat session-scoped store. Introducing an "office-memory" sub-kind now would (a) compete with the department axis #12 will introduce, (b) duplicate solo-relevant content already covered by `memory/universal/`, (c) require schema design without a load-bearing consumer.

**What survives migration**: per ROADMAP v2, layered scopes port to Memory Bank scopes when (if) Tier 3 arrives. The taxonomy is the load-bearing IP; Memory Bank's API is a transport.

**Revisit trigger**: first cross-project session-spanning state emerges (e.g., bureau-wide deadline tracker, cross-project actor reputation, cross-project korrektur-style) that doesn't fit `memory/universal/` prose or per-project `_ai/`.

### Row 4 — Cross-department workflow (in-session orchestration vs A2A messages)

**Verdict: architectural constraint for commitment #12 — cross-department coordination MUST be event-shaped, not call-shaped.**

**Why**: #12 will design the office-vs-department boundary. The shape it picks for cross-department coordination determines whether Tier 3 migration is feasible. **Event-shaped** coordination (typed events on the audit trail, in-process subscribers today) is transport-swappable to A2A messages later without refactor. **Call-shaped** coordination (department-A's Python imports department-B's functions) is not.

**What #10 commits to #12**: when designing department-to-department coordination, use AuditEvent (or a sibling typed-event mechanism) as the coordination channel. Departments listen for events relevant to them; emit events when their actions affect other departments. No direct cross-department function calls in business logic.

**What #10 does NOT decide**: which event kinds carry cross-department coordination, the subscriber dispatch mechanism, or whether departments share AuditEvent or get their own log. Those are #12.

### Row 5 — Audit trail (custom JSONL vs Agent Identity cryptographic)

**Verdict: adopt three additive AuditEvent fields. Defer cryptographic signing and canonicalization to Tier 3 migration.**

**Concrete schema additions** (`backend/mcp-server/src/pbs_mcp/audit_trail.py`):

```python
ActorKind = Literal["human", "skill", "external_agent"]

class AuditEvent(StrictModel):
    # ... existing fields unchanged ...
    actor_kind: ActorKind                        # NEW: required
    actor_card: str | None = None                # NEW: optional
    origin_agent_card: str | None = None         # NEW: optional

    @model_validator(mode="after")
    def _check_external_agent_origin(self) -> "AuditEvent":
        if self.actor_kind == "external_agent" and not self.origin_agent_card:
            raise ValueError(
                f"actor_kind='external_agent' requires origin_agent_card; "
                f"event {self.id} cannot be external without naming its source peer"
            )
        return self
```

**Field semantics**:

| Field | Required? | Today's values | Future on Tier 3 |
|---|---|---|---|
| `actor_kind` | yes | `"human"` (Gunther + colleagues), `"skill"` (PBS skills emitting events), `"external_agent"` reserved | Same three values; A2A peers always `external_agent` |
| `actor_card` | no | None for human, skill name for skill, None for external (today there are none) | Agent-card URL (RFC TBD by A2A spec) for skill + external |
| `origin_agent_card` | no | None for local events (human + skill); required for external_agent | A2A peer's agent-card URL |

**Why required for `actor_kind`**: per the strict-validation discipline (ARCHITECTURE.md meta-rule 4), required fields fail loud; no silent defaults masking missing data. Every event-producing skill retrofit (#6) declares which kind its actor is. No live AuditEvents exist yet (zero projects bound), so no migration concerns.

**Why deferred for signing**: AuditEvent JSONL is append-only. Adding a `signature?: str | None` field at Tier 3 migration is a single optional-field addition — every existing event reads as `signature=None` (correct: pre-Tier-3 events were never signed). Adding canonicalization function is also deferrable for the same reason. Pre-RAG cost ≈ Tier-3-day cost; no pre-RAG advantage.

**Why this generalizes beyond A2A**: distinguishing skill-as-actor from human-as-actor is independently valuable for #11 (plugin agents emit events as `actor_kind=skill, actor_card=<agent-name>`) and #12 (department analytics — which department emitted what). The A2A motivation is a forcing function; the discrimination is correct under our archetype too.

### Row 6a — Agent Gateway analogue (data classification)

**Verdict: defer to commitment #13.**

**Why**: data classification (PII / business-sensitive / public field annotations) is load-bearing at Tier 2 (multi-user-per-office, where one user must not see another user's PII fields) and Tier 3 (cross-org governance). Solo Tier 1 has one user with access to everything; classification metadata has no consumer.

#13 owns multi-user readiness — User Pydantic model, AuditEvent.user_id, optimistic locking. Data classification is the same workstream: it's the field-level governance complement to user-level access. Doing it in #13 means the classifications and their consumers (auth gates) ship together.

**What if Tier 1 wants it anyway**: even solo Gunther benefits from classification annotations as documentation (which fields contain client-confidential content?). But: Pydantic Field annotations are documentation in any case; the gating consumer is #13's auth layer. Adding annotations now without consumer is decoration without contract.

### Row 6b — Model Armor analogue (input validation against prompt injection)

**Verdict: defer; document path.**

**Why**: solo Tier 1 with trusted input has minimal prompt-injection surface. Tier 2/3 with untrusted user inputs (cloud clients, cross-org) need MCP-gate-level input validation. Pre-RAG: not load-bearing. Path: when #13 adds HTTP MCP transport, every gate gains an input-validation step before contract validation.

### Row 6c — Agent Simulation analogue (cross-agent stress test)

**Verdict: defer to v2.**

**Why**: heavy work; partial coverage already exists via audit + design-review (orchestrator-led validation across skill workflows). Full simulation harness for cross-agent edge cases is appropriate when the AI-office-builder (v2) ships and multiple instance offices exist to stress-test against.

### Row 7 — Model

**Verdict: skip. No archetype difference.**

Anthropic Claude in both archetypes (Tier 3 via Gemini Enterprise's Model Garden as Claude Opus 4.7 / Sonnet / Haiku). No decision needed.

## Summary table

| Row | Verdict | Where it lands |
|---|---|---|
| 1. Orchestrator | Stay single-Opus; defer internal A2A | (no change to schema; constraint via Row 5) |
| 2. Backend transport | Adopt HTTP MCP alongside stdio | Implementation in #13 |
| 3. Persistent state | Stay with current memory taxonomy | (no change) |
| 4. Cross-department workflow | Event-shaped coordination required | Constraint for #12 |
| 5. Audit trail | Adopt 3 additive fields | THIS commitment — schema in audit_trail.py |
| 6a. Data classification | Defer | #13 (multi-user readiness) |
| 6b. Model Armor analogue | Defer | Documented; revisits at #13 HTTP MCP |
| 6c. Agent Simulation analogue | Defer to v2 | ROADMAP v2 |
| 7. Model | Skip | (no archetype difference) |

## Implementation scope (this commitment)

**Schema additions**:
- `audit_trail.py`: `ActorKind` Literal type; `actor_kind` required; `actor_card` + `origin_agent_card` optional; `_check_external_agent_origin` model validator.

**Documentation**:
- `ARCHITECTURE.md` v0.9 → v0.10: pattern-vs-instance discipline gains an A2A-shape-compatibility paragraph noting that schema decisions are made pattern-level for archetype portability. Meta-rule 3 invalidation table: AuditEvent row mentions actor_kind dimension.
- `ROADMAP.md`: commitment #10 marked shipped; per-row decisions cross-referenced here.
- `HANDOFF.md`: session 8 closing state with shipped #10 entry.

**What's NOT in this commitment**:
- HTTP MCP endpoint implementation (→ #13)
- Data classification annotations (→ #13)
- Cross-department coordination design (→ #12)
- Skill retrofits to populate `actor_kind` (→ #6 audit-trail v2 retrofit)
- Cryptographic signing fields (→ Tier 3 migration if/when triggered)
- Test harness for backend (deferred — no backend tests exist yet; establishing the pattern is its own scope)

## Constraints for downstream commitments

**For #6 (audit-trail v2 retrofit)** — when retrofitting skills to call `record_audit_event` / `record_decision`:
- Every call MUST set `actor_kind` explicitly. Skill retrofits pass `actor_kind="skill", actor_card=<skill-name>`. Human-confirmed events (decisions, send approvals) pass `actor_kind="human", actor_card=None`. The discrimination is required by the strict-validation contract.
- The `user_confirmation` event kind (per audit-trail-v2.md) emits as `actor_kind="human"` — the user confirming is the actor, not the skill drafting.

**For #11 (Cowork integration)** — when plugin agents formalize:
- Plugin agents emit events as `actor_kind="skill", actor_card=<agent-name>`. Same shape as in-skill emissions; the agent IS a skill from the audit perspective.

**For #12 (office-vs-department modularization)** — when designing coordination:
- Cross-department coordination MUST be event-shaped (typed events on audit trail or sibling mechanism), not call-shaped. The transport-swap-to-A2A path depends on this.
- Department identity (probably `department: <slug>` frontmatter field per #11/#12 work) is independent of `actor_kind` — a department is a grouping of skills, not an actor kind. Per-department audit views are a query filter on `actor_card` ↔ skill-membership, not a new `actor_kind` value.

**For #13 (deployment flexibility)** — when adding HTTP transport + multi-user:
- Pluggable transport abstraction: stdio (current) and HTTP (new) implement the same contract. Decision recorded here; design+impl in #13.
- Data classification annotations land here (Row 6a deferred to #13).
- AuditEvent.user_id field (per #13 multi-user readiness) is additive; semantics: the human user attributed to a skill-emitted event. Distinct from `actor_kind` (which categorizes the event's emitter). When `actor_kind="human"`, `user_id == actor`. When `actor_kind="skill"`, `user_id` is the human under whose session the skill emitted. When `actor_kind="external_agent"`, `user_id` is None or the upstream peer's principal.

## Why pre-RAG (timing)

Same logic as commitments #6 + #9: schema decisions made pre-data-accumulation are cheap; same decisions made post-accumulation cost a migration script + multi-skill retrofit per change. Today zero projects are bound and zero AuditEvents exist; the schema additions are a Pydantic edit. After Phase 1 corpus download starts (and especially after first project bind), every additional schema change pays the migration tax.

The asymmetry argues for over-shooting on cheap defensive additions: even if `actor_card` and `origin_agent_card` go unused for years, their cost today is two `Optional` field declarations. If they DO become load-bearing later (Tier 3 migration, third-party plugin emits events into our trail, audit trail consumed by an external auditor), they're already present.

## Revisit triggers

- **Anytime** a real cross-organizational scenario emerges (consulting prospect, plugin marketplace external publish, etc.) — re-read the deferred items (signing, canonicalization, data classification) and decide if they're now load-bearing.
- **At #6 (audit-trail v2 retrofit)**: confirm the three new fields' semantics survive contact with real skill retrofits. Adjust if a fourth `actor_kind` value emerges (e.g., `system` for migration scripts, scheduled tasks).
- **At #12 (office-vs-department)**: confirm event-shaped coordination is workable. If pure-event coordination produces unacceptable latency or coupling, revisit and consider a hybrid (events for cross-department signaling, in-process function calls for tight coupling within a department).
- **At #13 (deployment flexibility)**: confirm `user_id` field added per multi-user readiness composes cleanly with the three `actor_*` fields here. If the four fields together are confusing, refactor the actor model.
- **First Tier 3 trigger** (per ROADMAP v2 "When this might pull forward"): activate the deferred signing + canonicalization + Memory Bank port + Apigee bridge work.

## Files touched

- `docs/decisions/a2a-and-gemini-pattern-emulation.md` — this file
- `backend/mcp-server/src/pbs_mcp/audit_trail.py` — three new fields + cross-ref validator
- `ARCHITECTURE.md` — v0.9 → v0.10; pattern-vs-instance discipline; meta-rule 3 invalidation table for AuditEvent
- `ROADMAP.md` — commitment #10 moved to "shipped" list
- `HANDOFF.md` — session 8 closing state
