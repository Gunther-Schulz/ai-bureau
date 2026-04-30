# Validation gating — systems overview

**Status**: navigational + systems-view (session 11). Not authoritative content — every section points to a source-of-truth detailed doc. Single place to scan "how is X validated over its lifecycle?" without chasing ARCH + ROADMAP + skill references + decision records.

**Owner**: ARCHITECTURE.md "Make wrong shapes impossible" discipline (v0.21) + meta-rule 4 + AI-as-runtime hybrid-shape principle.

**Maintenance**: see ARCH "Maintenance discipline" rule 3 (reference card sync) + rule 5 (inventory update — added v0.22). When adding a new gate / slice / target / convention, the inventory below updates in the same commit as the source-of-truth artifact.

---

## 1. Why this doc exists

Validation gating permeates every architectural layer in the framework: every read/write of contract-bearing data, every prose convention applied at mint-time, every retrospective drift scan, every prospective design check. The pieces are spread across:

- ARCH disciplines (each carries its enforcement story)
- meta-rules 1-4 (placement + invalidation + boundary)
- entity-md-spec (Layer 1 + Layer 2 + Layer 3 contracts)
- decision records (per-decision rationale)
- audit skill `references/drift-surfaces-and-slices.md` (24 drift surfaces × 23 slices)
- design-review skill `references/scope-and-targets.md` (15 named targets + focused-mode targets)
- ROADMAP commitments (each produces specific gates)

This doc consolidates the **systems-view** — how the pieces compose, where each lives, what stage each is at. Not a re-statement of any individual rule.

The reference card in ARCHITECTURE answers **"where does X go?"** for a given design concern (one row, one rule). This doc answers **"how is X validated over its lifecycle?"** (multi-layer, multi-stage). Different question; complementary tools.

---

## 2. The five layers of validation

Every concern in the system is validated through one or more of these five layers. The layers compose: L3 + L4 catch what L1 + L2 miss; L4 prevents new L1 + L2 gaps before they land; L5 enforces contracts at the external boundary where L1's internal Pydantic gate doesn't reach.

### L1 — Runtime structural (gate / Pydantic / dispatch — fail-loud, hot path)

What it does: at every read/write of contract-bearing data, the MCP gate validates the data against its Pydantic contract. Fail-loud on missing required fields, type mismatches, enum violations, cross-reference failures.

When it fires: every `read_entity` / `write_entity` / `record_audit_event` / `update_project_state` / etc. call. Hot path; no opt-out.

What it covers: machine contracts — interfaces / identity / persistence / dispatch (per AI-as-runtime hybrid-shape boundary).

What it does NOT cover: domain semantics, process flow, conditional rules, contextual knowledge — those live in L2.

**Source of truth**: meta-rule 4 (`ARCHITECTURE.md`) + meta-rule 4 fail-closed corollary (`docs/decisions/mcp-fallback-policy.md`) + entity-md-spec §3-§5 + per-Pydantic-class file in `backend/mcp-server/src/pbs_mcp/` (and post-#9 in `extensions/<scope>/<...>/entities/<type>.py`).

### L2 — Runtime conventional (AI-applied prose + audit-trailed)

What it does: at mint-time / decision-time / reasoning-time, AI reads a deployment-specific prose convention and applies it. The act of application emits an AuditEvent with `convention_applied: {file, section, git_sha}` so the rule + its application is reconstructible later.

When it fires: when AI is asked to perform a deployment-specific action — minting an actor ID, deciding archival, naming a doctype instance, applying a cross-department coordination trigger.

What it covers: deployment-instance rules that vary bureau-to-bureau (actor-id minting conventions, archive policies, naming styles, notification triggers).

What it does NOT cover: machine-contract enforcement (that's L1) or semantic precision of the prose itself (a Layer-3 LLM audit sub-check, not enforcement).

**Source of truth**: `docs/decisions/governance-and-identity-sourcing.md` decision 4 (prose conventions as the unifying mechanism) + AI-as-runtime hybrid-shape principle (`docs/decisions/ai-as-runtime-hybrid-shape.md`) + `docs/conventions/entity-md-spec.md` §3.1 (identifier uniqueness conventions) + AuditEvent schema in `backend/mcp-server/src/pbs_mcp/audit_trail.py`.

### L3 — Retrospective scan (audit slices)

What it does: scans the codebase + manifests + entity-mds + decision records for drift from declared contracts, conventions, and disciplines. Catches what slipped past L1 + L2 (e.g., a new contract-bearing surface that lacks a gate; a convention that's drifting between deployments).

When it fires: on user demand (`audit`), before phase boundaries, after meta-rule additions or refactor sweeps, when stale claims are noticed.

What it covers: discipline-aligned drift detection — boundary placement (slice 14), invalidation-contract coverage (slice 15), validation-gate strictness (slice 16), legacy retirement (slice 18), pattern-vs-instance (slice 19), entity-elevation (slice 20), entity-md frontmatter + body conformance (slice 21), wrong-shapes-solvable (slice 22, NEW v0.21), gate coverage comprehensiveness (slice 23, planned in #17).

**Source of truth**: `plugin/skills/audit/references/drift-surfaces-and-slices.md` (24 drift surfaces + 23 slices). Skill version 0.11.0 (post-slice-22).

### L4 — Prospective design (design-review targets)

What it does: at design time (before code lands), reviews proposals for soundness against the eight named architectural disciplines + meta-rules. Prevents new L1 + L2 gaps before they ship.

When it fires: before any non-trivial commitment lands. Triggered explicitly via `design review`; recommended before phase boundaries; recommended for in-flight bundles.

What it covers: design-time enforcement of the eight disciplines + meta-rules. Specifically the discipline-aligned targets — LLM/Python boundary (target 7), VISION↔ARCH coupling (target 8), subsumption (target 9), pattern-vs-instance (target 10), entity-elevation (target 11), entity-md authoring (target 12), pattern emergence (target 13), discipline-gap detection (target 14), make-wrong-shapes-impossible (target 15, NEW v0.21).

**Source of truth**: `plugin/skills/design-review/references/scope-and-targets.md` + `references/failure-mode-catalog.md` + `references/anti-bias-mechanism.md`. Skill version 0.10.0 (post-target-15).

### L5 — External-boundary validation (added v0.23 ultrathink-review)

What it does: validates contracts at the boundary between PBS and external systems. Different mechanisms than L1's internal Pydantic gate — cryptographic signing for A2A, token validation for auth, schema validation for CloudEvents, signed agent cards.

When it fires: at every external interaction — A2A peer sends event, OAuth user authenticates, external scheduler triggers, adapter receives webhook, PBS produces signed event for external consumer.

What it covers (inbound): A2A peer signature validation, OAuth token validation, CloudEvents shape validation when consuming external events, webhook signature verification.

What it covers (outbound): cryptographic signing for outbound events, JOSE/JWT/JWS for outbound A2A, CloudEvents-conformant serialization of AuditEvents (per #10 ROADMAP standards-eval).

What it does NOT cover: internal contract validation (that's L1) or AI-applied conventions (L2).

Today: largely deferred (Tier 3 federation triggers most). Implementation surface fragmented across #10 (A2A signing — Tier 3) + #13 (auth token validation — Tier 2) + #6 (CloudEvents conformance evaluation per session-11 standards-eval) + adapter-specific webhook signature checks (per-adapter implementation in #11/#15).

**Source of truth**: `docs/decisions/a2a-and-gemini-pattern-emulation.md` (A2A schema + signing) + `docs/decisions/governance-and-identity-sourcing.md` (auth) + ROADMAP #10 standards-conformance evaluations (CloudEvents, JOSE, OAuth/OIDC/SAML/SCIM) + per-adapter Pydantic Protocol implementations.

### How the layers compose

```
L4 (prospective)            →  prevents new L1+L2 gaps from landing
L1+L2 (runtime, hot path)    →  enforce on every read/write + mint-time application
L3 (retrospective)           →  catches drift that slipped past L1+L2
                                 + detects coverage gaps L4 should add
L5 (boundary, inbound+outbound) →  enforces external contracts at PBS↔external boundary
                                    (different mechanisms: signing, tokens, schema validation)
```

A failure mode caught at L3 typically becomes either:
- A tightening of L1 (new structural constraint, eliminates the drift surface) — preferred per "Make wrong shapes impossible"
- A new L4 target (design-time check that prevents future instances)
- An update to the failure-mode catalog (so target 14 picks it up next run)

---

## 3. The discriminator — choosing the layer

For any concern X, two questions decide which layer enforces it:

1. **Does the gate / Pydantic / dispatch code touch X on every read/write?**
   - Yes → L1 (structural, impossible-by-construction)
   - No, but external system / scheduler / cron dispatches on X → L1 (per Gap A from #12 infrastructure-primitive review)
   - No → continue
2. **Does AI apply X at mint-time / decision-time / reasoning-time?**
   - Yes → L2 (prose convention, audit-trailed via `convention_applied`)
   - No → not validation-gating territory; X may be free-form prose, computation, or transient state

If neither L1 nor L2 fits, but X is still a load-bearing concern, design-review target 14 (discipline-gap detection) flags it for review.

L3 + L4 are NOT chosen per concern — they're systemic; every L1 + L2 concern is automatically subject to retrospective + prospective scans through the slice + target framework.

**Source of truth**: ARCHITECTURE.md "Make wrong shapes impossible, not solvable" discipline + reference card row 3 + governance-and-identity-sourcing decision 4.

---

## 4. Inventory

Every load-bearing validation gate, convention, slice, and target. Status legend: ✅ shipped / 🔄 in-flight / ⏳ planned-in-commitment / 🆕 new this session.

### L1 — Runtime structural gates

| Gate | Validates | Status | Source of truth |
|---|---|---|---|
| `record_audit_event` | AuditEvent shape (incl. `actor_kind`, `actor_card`, `origin_agent_card`, `convention_applied`) | ✅ session 6/8 (events); `convention_applied` in #6 retrofit | `backend/mcp-server/src/pbs_mcp/audit_trail.py` + `docs/decisions/audit-trail-v2.md` |
| `query_audit_trail` | Filter shape; cross-ref invariants | ✅ session 6 + `department:` filter session 9 | `pbs_mcp/audit_trail.py` |
| `get_project_state` / `update_project_state` | ProjectState (incl. `departments_active` per #12) | ✅ session 6/9 (relocates to `extensions/department/planning/entities/project.py` per #16 + #9) | `pbs_mcp/project_state.py` |
| `validate_skill_output` | ReviewOutput, RecommendationOutput sparring schemas | ✅ session 6 | `docs/decisions/sparring-output-v1.md` |
| `find_bausteine_by_reference` | Cross-ref graph for bausteine | ✅ session 4 | `pbs_mcp/tools/memory.py` |
| `find_memory_docs_by_reference` | Cross-ref graph for memory docs | ⏳ #7 (pulled forward to v1) | ROADMAP "Tier 2 MCP cross-reference tools" |
| `find_manifest_entry` | Single-entry lookup across in-scope manifests | ⏳ #7 (pulled forward to v1) | ROADMAP same |
| Tier 3 MCP introspection tools (`get_active_practices`, `get_signature_block`, `get_office_identity`, `list_snapshots`, `list_correspondence`, `list_decisions`, `list_office_style_overlays`) | Schema introspection helpers | ⏳ #7 (pulled forward to v1) | ROADMAP "Tier 3 MCP introspection tools" |
| Generic entity gate (`read_entity` / `write_entity` / `list_entities`) | Layer 1 + Layer 2 frontmatter via type-dispatch to Pydantic subclass; body preserved as-is | ⏳ #9 (current immediate work) | `docs/decisions/ai-as-runtime-hybrid-shape.md` + entity-md-spec |
| `DepartmentEntity` / `OfficeEntity` / `UniversalEntity` Pydantic | Registration files (`department.md` / `office.md` / `universal.md`) | ⏳ #9 Bundle A | HANDOFF Bundle A close-out + entity-md-spec §3.2 |
| `ManagedEntityRegistration` Pydantic | At-least-one-of `{instances_at, adapter}` validator | ⏳ #9 Bundle A | HANDOFF Bundle A close-out |
| Type namespacing dispatch (`<scope-id>.<short-name>`) | Cross-department type collision (impossible by construction) | ⏳ #9 Bundle A 🆕 | entity-md-spec §3.2 |
| Layer 3 mechanism (TBD: Pydantic subclass / declared `extra_fields` / `metadata: dict`) | Per-deployment customization fields | ⏳ #9 Bundle B (Layer 3 decision pending; first target for new design-review target 15) | entity-md-spec §5 + ai-as-runtime-hybrid-shape.md D1 |
| Adapter Protocol (`subscribe_to_changes` / `poll_for_changes`) | Adapter interface uniformity (Pydantic Protocol) | ⏳ #9 Bundle E (restored from #11 deferral) 🆕 | HANDOFF Bundle A close-out |
| Schema migration framework (entity gate applies migrations on read; per-record `schema_version` Layer 1 field) | Forward-migration of memory data records | ⏳ #9 (absorbed from v1.x) 🆕 | ROADMAP "Schema migration framework" |
| Manifest Pydantic models (post-#16: per-entity md files; gate's Layer 2 dispatch IS the manifest validator; `validate_manifest(path)` MCP tool) | Manifest invalidation contracts (`last_updated`, `last_fetched`, `checksum_sha256`) | ⏳ #9 (absorbed from v1.x) 🆕 | ROADMAP "Manifest Pydantic models" |
| `dedupe_bausteine` MCP tool | Reproducible dedup scoring + Pydantic candidate output | ⏳ #6 (absorbed from v1.x) 🆕 | ROADMAP "Boundary placement refinements" |
| `record_baustein_use` MCP tool | Atomic frontmatter mutation (`rejected_uses[]` / `successful_uses[]`) with validation | ⏳ #6 (absorbed from v1.x) 🆕 | ROADMAP same |
| `create_manifest` / `create_office_config` (bootstrap-write) | First-write through Pydantic loader (closes meta-rule 4 fail-closed gap) | ⏳ #7 | ROADMAP commitment #7 |
| `record_decision` / `render_audit_trail` (audit-trail v2 retrofit) | Single-write architecture: gate atomically mirrors event → `decisions.md` | ⏳ #6 | `docs/decisions/audit-trail-v2.md` |
| `backfill_audit_trail` | Migration: legacy prose sources → audit-trail v2 events | ⏳ #6 | same |
| Tier-conditional role enforcement (Actor.roles + approval events) | Multi-user write authorization (gate-level) | ⏳ #13 (built once, activates at Tier 2) | `docs/decisions/governance-and-identity-sourcing.md` decision 1 |
| `register_scheduled_trigger` (Gap A from #12 infrastructure-primitive review) | Time-driven event sources (extends event sources to "skill-emitted + time-emitted") | ⏳ #13 | ROADMAP #13 |
| HTTP MCP transport / multi-user auth / cross-tier migration tools | Tier 2 cloud deployment readiness | ⏳ #13 | ROADMAP #13 |

### L2 — Runtime conventional (prose + AuditEvent integration)

| Convention surface | Where it lives | Application moment | Audit trail | Status |
|---|---|---|---|---|
| Actor-id minting convention | `extensions/office/conventions/actor-conventions.md` (or office-config.md body) | Mint-time when adding new actor | AuditEvent with `convention_applied: {file, section, git_sha}` | ⏳ #15 (Actor entity) + #6 (`convention_applied` field) |
| Archive policy | `extensions/office/conventions/archive-conventions.md` | Decision-time when archiving | Same | ⏳ #6 |
| Naming conventions (file / folder / instance) | `extensions/office/conventions/naming-conventions.md` | Mint-time when creating named artifacts | Same | ⏳ #6 |
| Notification triggers (cross-department coordination) | `extensions/office/conventions/notification-conventions.md` | Workflow-event-time | Same | ⏳ #6 + #13 (notification adapter) |
| Audit conventions (what gets recorded) | `extensions/office/conventions/audit-conventions.md` | Per audit event emission | Self-referential (audit trail itself) | ⏳ #6 |
| Department-specific conventions | `extensions/department/<dept>/department.md` body OR `extensions/department/<dept>/conventions/<topic>.md` | Per-department workflow moments | Same | ⏳ #9 Bundle A (body section catalog) + #6 |
| Process-as-md (verfahren flow, doctype-required-when conditions) | `extensions/department/<dept>/processes/<process>.md` body | At decision-time when AI reasons about "what's next" / "what's missing" | Reasoning chain captured via decision events | ⏳ #16 (principle shipped) + #9 (process-entity migrations) |
| Body conventions per entity type (recommended sections) | entity-md-spec §6 + body-spec per type | At authoring-time (recommended-not-enforced) | Audit slice 21 + design-review target 12 flag missing sections | ⏳ #9 (per-type body specs) |

### L3 — Retrospective scan (audit slices, discipline-aligned)

| Slice | Discipline / failure mode | Status | Source of truth |
|---|---|---|---|
| Slice 14 — boundary-adherence | Meta-rule 4 (LLM/Python boundary) | ✅ shipped session 6+; first-run done | drift-surfaces §slice 14 |
| Slice 15 — invalidation-contract coverage | Meta-rule 3 (source-of-truth + invalidation) | ✅ shipped; first-run done | §slice 15 |
| Slice 16 — validation-gate coverage (strictness) | Strict-validation discipline | ✅ shipped; first-run done | §slice 16 |
| Slice 18 — legacy retirement scan | (paired with target 9 subsumption) | ✅ shipped session 7 | §slice 18 |
| Slice 19 — pattern-vs-instance scan | Pattern-vs-instance discipline (v0.8) | ✅ shipped session 8 | §slice 19 |
| Slice 20 — entity-elevation drift | Entity-elevation discipline (v0.13) | ✅ shipped session 9 followup | §slice 20 |
| Slice 21 — entity-md frontmatter + body conformance + body-size telemetry (D2 trigger) | AI-as-runtime hybrid-shape (v0.16) | 🔄 scaffold session 10 followup; first-run scheduled with #9 entity-md migrations | §slice 21 |
| Slice 22 — wrong-shapes-solvable scan | Make wrong shapes impossible (v0.21) | 🆕 session 11; first-run scheduled session 12+ | §slice 22 |
| Slice 23 — gate coverage comprehensiveness | Incomplete-gate-coverage failure mode | ⏳ planned in #17 (renumbered from "slice 22" per session 11) | ROADMAP #17 |

Slices 1-13 cover compliance (does X match its claims?) + implementation quality (test coverage, security, performance) — not discipline-aligned, but part of the L3 layer. See drift-surfaces-and-slices.md for full catalog.

### L5 — External-boundary validation (PBS↔external)

| Boundary | Mechanism | Status |
|---|---|---|
| **Inbound A2A peer event** | Signed agent card validation; cryptographic signature verification | ⏳ Tier 3 trigger; #10 deferred items + governance-and-identity-sourcing decision 2 |
| **Inbound OAuth / OIDC / SAML token** | Token validation; user identification; role hydration via Actor adapter | ⏳ #13 + governance-and-identity-sourcing decision 2 |
| **Inbound webhook (e.g., Lexware, Personio)** | Per-adapter signature verification | ⏳ #11 + #15 (per-adapter implementation) |
| **Inbound CloudEvents** (cross-system event consumption) | Schema validation against CloudEvents spec | ⏳ #10 standards-conformance eval (0.5 session before #6) |
| **Outbound signed AuditEvent** (for cross-org consumption) | Cryptographic signing (JOSE / JWT / JWS) + deterministic JSON canonicalization | ⏳ #10 deferred items (Tier 3 trigger) |
| **Outbound CloudEvents-conformant serialization** | Map AuditEvent to CloudEvents core fields (`id`, `source`, `type`, `specversion`, `time`) | ⏳ #6 (if conformance accepted per evaluation) |

L5 is largely Tier-2/Tier-3 territory; minimal in Tier 1 (single-process, single-user, no external boundary). Becomes load-bearing as deployments cross PBS↔external boundaries (cloud auth, federated agents, cross-system event consumption).

### L4 — Prospective design (design-review targets, discipline-aligned)

| Target | Discipline | Status | Source of truth |
|---|---|---|---|
| Target 7 — LLM/Python boundary (placement-soundness) | Meta-rule 4 | ✅ shipped | scope-and-targets §target 7 |
| Target 8 — VISION ↔ ARCHITECTURE coupling | VISION axes + traceability | ✅ shipped | §target 8 |
| Target 9 — Subsumption check (legacy retirement at design time) | Maintenance discipline | ✅ shipped session 7 | §target 9 |
| Target 10 — Pattern-vs-instance check | Pattern-vs-instance discipline | ✅ shipped session 8 | §target 10 |
| Target 11 — Entity-elevation check | Entity-elevation discipline (v0.13) | ✅ shipped session 9 | §target 11 |
| Target 12 — Entity-md authoring conformance | AI-as-runtime hybrid-shape (v0.16) | ✅ scaffold session 10 followup; first-run bundled with #9 | §target 12 |
| Target 13 — Pattern emergence / unnamed convergence | (Catches silent-convergence failure mode) | ✅ session 10 followup; first-run session 11+ | §target 13 |
| Target 14 — Discipline-gap detection | Top-down lens against failure-mode catalog | ✅ session 10 followup; first-run immediate | §target 14 |
| Target 15 — Make wrong shapes impossible check | Make wrong shapes impossible (v0.21) | 🆕 session 11; first-run on Bundle B Layer-3-mechanism decision | §target 15 |

Targets 1-6 cover ARCHITECTURE meta-rules + entity types + decision rules + maintenance + orchestrator + skill frontmatter + office-config schema — foundational, not discipline-aligned per se. See scope-and-targets.md for full catalog.

---

## 5. Composition + lifecycle

### How the layers compose

- **L1 + L2 are the runtime stack**: structural enforcement on the hot path (L1) + AI-applied conventions at decision moments (L2). Together, every read/write + every mint-time decision is validated.
- **L3 catches what L1 + L2 miss**: drift introduced over time, new contract-bearing surfaces that lack gates, conventions that drift between deployments. Discovery mode for L1/L2 gaps.
- **L4 prevents new L1 + L2 gaps**: design-time review for proposals before code lands. Catches the gap at the cheapest possible moment.

When L3 catches a recurring drift pattern, the response order:

1. **Tighten L1** if possible (per "Make wrong shapes impossible") — eliminate the drift surface structurally.
2. **Add L4 target** — design-time check that prevents future instances of the same pattern.
3. **Update failure-mode catalog** — so target 14 picks it up next run.
4. **Update L2** — if the pattern is genuinely deployment-instance, formalize as a prose convention with audit-trail integration.

### Lifecycle: how a new concern enters the system

When a new validation concern surfaces (new entity type, new contract-bearing field, new cross-cutting rule):

1. **Reference card → row 3**: run the gate-dispatch discriminator. Determines L1 vs L2.
2. **If L1**:
   - Add Pydantic field / validator / discriminated union to the relevant entity / event / config schema.
   - Verify gate enforcement covers the new field (slice 16 strictness check; slice 23 comprehensiveness check post-#17).
   - If new entity type, add Layer 2 schema row to entity-md-spec §4 + body section catalog row in §6.
3. **If L2**:
   - Document convention in `extensions/office/conventions/<topic>.md` or `extensions/department/<dept>/department.md` body.
   - Verify AI applies it at mint-time and emits AuditEvent with `convention_applied`.
   - Verify `convention_applied` field validates the prose location exists.
4. **L3 update**: if the new concern fits an existing slice (boundary, invalidation, validation-gate, etc.), no new slice needed. If it surfaces a new failure mode, add to failure-mode catalog and consider new slice.
5. **L4 update**: if the new concern represents a new discipline or check, add to scope-and-targets.md as a new target. Otherwise existing targets cover.
6. **Inventory**: add row to this doc's L1 / L2 / L3 / L4 inventory table in the same commit.

### Lifecycle: how a concern is retired

When a concern is no longer load-bearing (deprecated entity type, retired convention, subsumed mechanism):

1. Run target 9 (subsumption check) — what does the new mechanism replace?
2. Apply `docs/deprecation-procedure.md` (per ARCH).
3. Update inventory rows (mark deprecated; cross-ref the replacement).
4. Slice 18 (legacy retirement scan) verifies retirement is complete.

---

## 6. Cross-refs

**Architectural disciplines** (the WHY behind validation gating):

- `ARCHITECTURE.md` "Pattern-vs-instance discipline" + sharp defer rule (v0.20) — frame the framework-vs-instance line for any validation choice.
- `ARCHITECTURE.md` "Make wrong shapes impossible, not solvable" (v0.21) — the discriminator between L1 and L2.
- `ARCHITECTURE.md` "AI-as-runtime hybrid-shape principle" (v0.16) — assigns the structured/prose boundary at the top level.
- `ARCHITECTURE.md` "Entity-elevation discipline" (v0.13) — when a noun gets a Pydantic schema vs stays in event / memory / nested.
- `ARCHITECTURE.md` "Validation layering: deterministic primary, LLM secondary" (v0.18) — within L3 + L4, deterministic checks before LLM judgment.
- `ARCHITECTURE.md` "Three evolution patterns" (v0.19) — mutable / append-only / forward-only-prose; affects migration framework shape.
- `ARCHITECTURE.md` meta-rule 3 (source-of-truth + invalidation) — what L1 + L2 enforce.
- `ARCHITECTURE.md` meta-rule 4 (execution-determinism + fail-closed corollary) — placement of validation logic.

**Reference card**: `ARCHITECTURE.md` "Data + boundary reference card" — answers "where does X go?" per design concern. Single-row distillation; this doc is the multi-layer expansion.

**Decision records**:

- `docs/decisions/ai-as-runtime-hybrid-shape.md` — three-layer frontmatter contract; gate generalization spec.
- `docs/decisions/governance-and-identity-sourcing.md` — prose conventions + governance enforcement spec.
- `docs/decisions/audit-trail-v2.md` — single-write architecture; `convention_applied` payload.
- `docs/decisions/mcp-fallback-policy.md` — fail-closed corollary.
- `docs/decisions/office-vs-department.md` — managed-entity concept; 4-axis scope orthogonality.

**Skill references** (the HOW of L3 + L4):

- `plugin/skills/audit/references/drift-surfaces-and-slices.md` — full slice catalog (currently 23; slice 22 added v0.21, slice 23 planned in #17).
- `plugin/skills/design-review/references/scope-and-targets.md` — full target catalog (currently 15; target 15 added v0.21).
- `plugin/skills/design-review/references/failure-mode-catalog.md` — living catalog of failure modes + their coverage status (target 14 reads).
- `plugin/skills/design-review/references/anti-bias-mechanism.md` — anti-status-quo bias mechanism for design review.

**Conventions docs**:

- `docs/conventions/entity-md-spec.md` — Layer 1 + Layer 2 + Layer 3 contracts; body conventions; type namespacing (§3.2).
- `docs/plugin-conventions.md` — skill frontmatter contracts; trigger conventions (§11); fallback policy (§11b).
- `docs/backend-conventions.md` — backend code idioms.

**ROADMAP commitments** (each produces specific gates):

- #6 audit-trail v2 retrofit — adds `record_decision`, `render_audit_trail`, `convention_applied` field, approval events; absorbs `dedupe_bausteine` + `record_baustein_use`.
- #7 bootstrap-write MCP tools — adds `create_manifest` + `create_office_config`; absorbs Tier 2 cross-ref + Tier 3 introspection.
- #9 Department contract + managed-entity concept + generic entity gate — produces L1 backbone for entity-md ecosystem; absorbs Bundle E + activation skill + schema migration framework + manifest Pydantic.
- #11 Cowork integration — concrete adapter implementations against #9-produced Protocol; skill frontmatter sweep with `department:` field.
- #13 Deployment flexibility — Tier-conditional role enforcement; HTTP MCP transport; cross-tier migration tools.
- #15 Office-level managed entities (Client + Actor) — Actor.roles primitive; identifier convention application.
- #17 MCP gate coverage comprehensiveness review — slice 23 scaffolding.

---

## 7. Maintenance

This doc is load-bearing for cross-cutting validation visibility. Drift here means future sessions don't see the layered picture and re-derive each time.

**Maintenance discipline rule 5** (added ARCH v0.22): when adding a new gate / slice / target / convention, the inventory tables in §4 update in the same commit as the source-of-truth artifact. Same-commit prevents drift.

**No new content lives here**. Every fact is cross-referenced to its source-of-truth file. If you find content here that isn't in any linked source, it's a sign the source needs updating, not the inventory.

When a layer or discriminator itself changes (rare — would be a new ARCH discipline), §2 + §3 update in the same commit as ARCH version bump.

---

**Last meaningful edit**: 2026-04-30 (session 11 — initial authoring; ARCH v0.21 → v0.22 + maintenance rule 5).
