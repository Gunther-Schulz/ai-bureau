# pbs-bureau architecture — what goes where

This document is the canonical placement reference. When in doubt
about where new content belongs, walk the **three decision rules**
below. Meta-rules establish principles; the decision rules apply
them.

> **Vision anchor.** PBS is built on three interlocking principles:
> **intertwined-AI-workflow (not tacked-on features)**, **sparring
> partner (not answer machine)**, and **authorship preservation
> (the user remains defensible expert author of everything PBS
> produces on their behalf)**. The architecture serves continuous
> human-AI collaboration with built-in challenge in service of
> defensible output — persistent state, orchestrated behaviors,
> source-grounded outputs, surfaced decisions, explicit human-
> authority gates, counter-arguments, calibrated confidence,
> selective friction. See `VISION.md` for the full thesis.

Status: **v0.16 (session 10 — AI-as-runtime hybrid-shape principle locked + entity-md three-layer frontmatter contract)**.

- v0.1 → v0.2: nine entity types + 6 decision rules.
- v0.2 → v0.3: scope-orthogonality live, layered manifests in
  repo, integration adapter scaffolding deployed, schema migration
  framework in place.
- v0.3 → v0.4: execution-locality meta-rule (skills declare
  `mcp_tools_required[]`; `settings.json` permissions; hooks
  deferred).
- v0.4 → v0.5: design-review-driven simplification. **5 meta-rules
  → 4 + 1 named convention**: integration-adapter demoted to corollary
  of app-vs-office; scope-orthogonality demoted to layering convention;
  execution-locality renamed to execution-determinism; new
  source-of-truth & invalidation meta-rule added. **9 entity types
  → 5**: A+B merged into Skill Bundle; G+H merged into Configuration;
  I demoted (it's an internal pattern of E, not a peer). A-I letter
  scheme dropped — names speak for themselves. **6 decision rules
  → 3** audience-first.
- **v0.5 → v0.6**: meta-rule 4 sharpening. **(A) Persistence-layer
  boundary refined**: the rule applies to durable state with a *typed
  contract* (Pydantic model + loader + cross-reference invariants),
  not to all files indiscriminately; loose markdown is skill-direct.
  **(B) Reuse direction made explicit**: shared deterministic logic →
  MCP tool; shared interpretive logic → Skill Bundle reference. The
  audit's slice 14 + design-review's target 7 land on this sharpened
  boundary.
- **v0.6 → v0.7**: meta-rule 4 fail-closed corollary. The rule
  symmetrizes for reads: when MCP is unreachable, contract-bearing
  reads MUST surface and stop, never bypass via direct filesystem
  `Read`. The strict-validation principle (no bad defaults / fail
  loud) extends to availability: a contract that is enforced on
  successful read but bypassed when MCP is down is not a contract.
  See `docs/decisions/mcp-fallback-policy.md`. Audit slice 14 brief
  extended to scan `fallback_when_mcp_absent` strings for declared
  future violations.
- **v0.7 → v0.8**: **Pattern-vs-instance discipline** added as
  meta-discipline before the meta-rules. Every architectural
  commitment must work at pattern level (the test: would this work
  for a hypothetical legal-practice / research-paper-review /
  engineering-doc office?), not just for PBS. PBS is the pioneer
  instance per VISION.md; the architecture is the pattern. Long-arc
  end-state is the AI-office builder (ROADMAP v2). Connects the
  Skill Bundle convention, meta-rules 1-4, fail-closed corollary,
  target 9 subsumption check — all pattern-level by construction —
  into a coherent discipline that constrains future commitments.
- **v0.8 → v0.9**: **Office-vs-department distinction** captured
  as open architectural question (post-partner-built-comparison
  insight). PBS today conflates "office" with "single department"
  (planning-document-work). Real offices contain multiple
  departments (PM, invoicing, etc.) coordinated via shared state +
  natural abstractions + ad-hoc context sharing + integration/
  setup configuration. Scoped as pre-RAG commitment #12 for
  structural design discussion before Phase 1 corpus download.
- **v0.9 → v0.10**: **A2A-shape compatibility decided per row** of
  the v2 Gemini Enterprise comparison table. AuditEvent grows three
  additive fields (`actor_kind` required, `actor_card` optional,
  `origin_agent_card` optional) — distinguishes human vs skill vs
  external-A2A-peer as event emitter. Pattern-vs-instance discipline
  picks up an explicit archetype-portability paragraph: every
  schema decision is checked against "would this port cleanly to a
  multi-agent A2A archetype?" alongside the cross-domain test. HTTP
  MCP transport, data classification, and signing fields are
  deferred with documented paths to commitments #13 and Tier-3
  migration. Cross-department coordination (open question per v0.9)
  receives a load-bearing constraint: must be event-shaped, not
  call-shaped — preserves transport-swap-to-A2A path for #12. See
  `docs/decisions/a2a-and-gemini-pattern-emulation.md`.
- **v0.10 → v0.11**: **Office-vs-department modularization resolved**
  (open question from v0.9). Office is the container; departments
  are capability areas (PBS = office with one department today,
  planning-document-work; future Schulz adds PM + invoicing).
  Skills declare `department:` frontmatter (REQUIRED, no default —
  matches `actor_kind` strict-validation discipline); office-level
  skills declare `department: office`. Memory taxonomy gains a 4th
  orthogonal axis (department), opt-in per entry. Cross-department
  coordination via AuditEvent + extended watch-list with per-
  department `event_subscriptions:` (no new event mechanism —
  subsumes via existing audit infrastructure). ProjectState gains
  `departments_active: list[str]` field for routing + audit-filter
  purposes. Skills are singleton-department; multi-department
  coordination via office-level orchestrating skills. Offices have
  0..N departments (zero-department = single-skill-utility shape;
  PBS-today = single-department; future Schulz = multi-department).
  Per-department phase/lifecycle on ProjectState deferred to #9
  (Pattern-vs-instance split, still pre-RAG); office-config schema
  bump + skill frontmatter sweep deferred to #11. See
  `docs/decisions/office-vs-department.md`.
- **v0.15 → v0.16**: **AI-as-runtime hybrid-shape principle**
  added as top-level architectural discipline (parallel to
  pattern-vs-instance + entity-elevation + glue-not-replacement).
  The principle: domain semantics, process flow, conditional
  rules, and contextual knowledge live in **markdown bodies
  attached to entity files**, not in encoded schemas or hardcoded
  skill procedures. Cross-domain portability is achieved by AI
  reading prose, not by abstracting over schema variants.
  Structured layers reserved for **interfaces, identity,
  persistence, machine contracts**; everything else is prose;
  AI is the runtime that fuses them at use-time. Three-layer
  frontmatter contract introduced: Layer 1 universal (every
  entity, Pydantic base, strict-locked); Layer 2 type-specific
  (Pydantic subclass per entity type, strict-locked); Layer 3
  per-deployment extension (deferred to #9). Body conventions
  recommended-not-enforced (mirrors how memories conventionally
  use Why:/How-to-apply: lines without validator enforcement).
  Resolves the "where do conditional rules live?" question:
  rules about *when* something applies belong with the *process*
  (process-as-md), not with the entity itself. New v1 commitment
  **#16 (AI-as-runtime hybrid-shape contract — entity-md +
  manifest decomposition + gate generalization)** scheduled
  position 1 in pre-RAG queue, BEFORE #11. Migration of existing
  `doctypes.yaml` + `references-manifest.yaml` (prose squeezed
  into block scalars) bundled with #9 + Phase 1 corpus
  respectively. Audit slice 21 + design-review target 12 added
  for entity-md conformance scanning. See
  `docs/decisions/ai-as-runtime-hybrid-shape.md`.
- **v0.14 → v0.15**: **Glue-not-replacement principle** added as
  top-level architectural discipline (parallel to pattern-vs-
  instance + entity-elevation). PBS is the **glue / coordination
  layer** that brings cross-concern AI to existing infrastructure;
  it does NOT replace existing systems (BPMN engines, accounting
  tools, CRMs, time-tracking, calendars, etc.). The architecture
  is integration-first: the integration-adapter pattern (meta-rule
  1) + adapter-mode managed entities (#12) + adapter-emitted events
  (#9 Gap B) all serve this principle. Where customers have
  existing infrastructure, PBS connects to it; where they don't,
  PBS provides native-mode managed entities + bundled MCP tools as
  an alternative. Both modes work uniformly through the same
  framework. Connects to the BPMN-empowerment positioning (v1.x-v2
  ROADMAP entry) and the consulting-niche framing (`docs/strategic-
  positioning.md`). See "Glue-not-replacement principle" section
  below.
- **v0.13 → v0.14**: **Infrastructure-primitive review pass**
  (session-9 followup #4) — stress-tests core primitives (skills,
  managed entities, audit events, memory, integration adapters,
  cross-department coordination) against expressibility of
  arbitrary business processes. Result: **9/9 process-need
  coverage** (state, actions, rules, history, knowledge, people,
  time, external world, workflows/sequences) after two genuine
  gaps fold into existing commitments. **Gap A — proactive
  time-driven triggers**: today's event sources are reactive +
  interactive only; missing scheduler-fired "tick" events for
  proactive deadline warnings, scheduled reports, Fristverlängerung
  automation. Folds into #13 (Tier 2 cloud naturally hosts
  scheduler); extends event sources from "skill-emitted" to
  "skill-emitted + time-emitted." **Gap B — adapter-emitted
  events**: adapters today are request-response; missing
  surfacing of external state changes (Lexware webhook on payment;
  Harvest external timesheet edit). Folds into #9 (department
  module contract); adapter Protocol gains
  `subscribe_to_changes` / `poll_for_changes`; external changes
  translate to native AuditEvents with `actor_kind=external_agent`
  per #10. No new commitment numbers; both gaps fold into
  existing scope. Smaller deferred items: workflow-as-data,
  centralized RBAC, team hierarchy, resource modeling for limited
  resources. See `docs/decisions/office-vs-department.md`
  "Infrastructure-primitive review" subsection.
- **v0.12 → v0.13**: **Entity-elevation discipline introduced +
  office-level managed entities concept added** (session-9 followup
  #2, post-broader-review). The discipline: prefer events + nested
  fields + memory entries over new managed entity types. Elevate
  to first-class managed entity only when **stable-identity +
  state-of-record + lifecycle all apply**. Avoids the architecture
  creeping toward a relational SQL schema (one entity per noun,
  foreign keys, joins, normalization rules — catastrophic for
  LLM-mediated AI offices). Right level: closer to **knowledge
  graph + document store with stable references**, not Oracle.
  "Joins" are answered via audit-trail filters, per-entity
  ID-based queries, memory queries, or adapter APIs — no join
  planner needed. New concept: **office-level managed entities**
  (Client, Actor) — owned by the office substrate, referenced by
  multiple departments. Distinct from department-level managed
  entities (Project, Invoice, Timesheet) — owned by a single
  department. Cross-department reference convention: entities
  hold `<entity>_id: str` fields referencing other entities; gate
  validates references exist at write time; no FK enforcement at
  storage layer. Approval flows demoted from managed-entity
  proposal to event-kinds on AuditEvent (folds into #6) per the
  three-test discipline. New v1 commitment **#15 (Client + Actor
  as office-level managed entities)** scheduled between #13 and
  #6. See `docs/decisions/office-vs-department.md` "When to
  elevate to managed entity" + "Approval flows are event-driven"
  subsections.
- **v0.11 → v0.12**: **Managed-entity concept introduced + meta-rule
  1 integration-adapter pattern generalized** (session-9 followup).
  The post-#12 first-pass realization: each department defines its
  own entity types completely; **there is no universal entity-type
  core**. Departments contribute "managed entities" (Project for
  planning, Invoice for invoicing, Timesheet for PM, Asset for
  brand-voice, Matter for legal-work) in one of two delivery modes:
  **native** (PBS owns system-of-record; Pydantic schema +
  native MCP tools) or **adapter-delegated** (external system owns
  system-of-record; integration adapter contract). Mixed-mode is
  required and supported per-entity (a department can have some
  entities native + some adapter-delegated). The adapter mode
  **generalizes meta-rule 1's existing integration-adapter pattern**
  from auxiliary integrations (email, calendar, scanner) to primary
  department system-of-record (Invoicing/PM/HR external systems);
  same Pydantic Protocol + concrete adapter contract, expanded
  consumer set. Project (PBS bauleitplanung) reframed as planning
  department's primary native managed entity (not "extension of a
  universal Project core"). #9's mission reframed from "extract
  universal core from PBS-specific extension" to "design the
  department module contract + managed-entity concept + per-
  company customization mechanism." See
  `docs/decisions/office-vs-department.md` "Department-managed
  entities + delivery modes" subsection.

> **Scope boundary.** This doc covers placement (which entity type /
> where). For *within-tier idioms* (how to write the thing once
> you've decided where it goes) see:
>
> - `docs/plugin-conventions.md` — Skill Bundle idioms (frontmatter,
>   semver, body patterns, references organization, routing
>   handoffs).
> - `docs/backend-conventions.md` — Backend idioms (test layout,
>   logging, MCP error format).
>
> Conventions docs trace decisions back here but never re-litigate
> placement.

## Maintenance discipline

A 3-line checklist:

1. Every meta-rule change, schema bump, or significant refactor
   lands in the same commit as the ARCHITECTURE.md update.
2. After meta-rule additions / refactor sweeps, run `audit` (drift
   detection) and `design-review` (soundness review) — see
   `plugin/skills/{audit,design-review}/`.
3. Sunset deprecated concepts via the deprecation procedure (below).

### Deprecation procedure

When retiring a concept (entity type, meta-rule, MCP tool name,
skill, etc.):

| Concept | Procedure |
|---|---|
| **Skill** | Bump major + add `deprecated: true` to frontmatter; remove after 1 plugin release. Document successor in description. |
| **MCP tool** | Alias old name → new for one minor version of pbs-mcp; remove after that. |
| **Entity type** | Pre-launch (now): rewrite ARCHITECTURE.md + sed across repo in one commit. Post-launch: announce in HANDOFF, add to deprecated-concepts list, give 1 release deprecation window. |
| **Meta-rule** | Reformulate in-place with explicit replaces-X note. Audit + design-review on next refactor verifies the replacement holds. |
| **Office-config field** | Bump schema_version + write migration that drops the field; existing offices forward-migrate transparently. |

Pre-launch / pre-distribution: deprecation is essentially
free — change in place. After first user-facing release the
procedure tightens.

---

## Pattern-vs-instance discipline

Every architectural commitment in this repo must work at the
**pattern level**, not just for PBS. PBS is the pioneer instance
(per VISION.md "PBS as pioneer instance"); the architecture is
the pattern. The long-arc end-state is an AI-office builder that
scaffolds new domain offices from a domain spec + the
accumulated patterns (see ROADMAP v2 "AI-office builder"). Every
commitment that doesn't generalize is a future migration cost
the builder will pay; every commitment that does generalize
*is* the builder's foundation.

**The test** when proposing any new meta-rule, entity type,
persistence structure, MCP tool, or decision-record-grade
commitment:

- Would this work for a hypothetical **legal-practice office**
  (intake / discovery / filing / argument phases; courts /
  opposing-counsel / regulators as authorities; precedents +
  citations + templates as memory taxonomy)?
- Would this work for a hypothetical **research-paper-review
  office** (manuscript / review / revision / publication phases;
  journals / co-authors / reviewers as authorities; citations +
  prior-work + templates as memory taxonomy)?
- Would this work for a hypothetical **engineering-doc office**,
  **medical-records-workflow office**, **regulatory-filing
  office**?

If yes for at least 2 of these 3-5 hypothetical domains: the
commitment is pattern-level. Lock it in.

If no for most: the commitment is too PBS-coupled. Push it to
the **instance layer** — skill bodies (drafting drafts plug in
domain-specific doctype templates), manifests (domain-specific
references + actors), office-config (domain-specific scope
fields), korrektur-rules and similar prose memory.

**Where the line typically falls:**

| Layer | Pattern (stays in architecture) | Instance (lives in PBS or its successors) |
|---|---|---|
| Meta-rules 1-4 | All four | (none — they're patterns by construction) |
| Entity types (Skill / Memory / Configuration / etc.) | The taxonomy itself | What entities exist (which skills, which memory records) |
| MCP tool *patterns* | strict-validation discipline; fail-closed corollary; CRUD-style memory tools | Tool *names + bodies* (which gates exist; what they do) |
| office-config *schema shape* | layered manifests, scope.domains, paths.* discipline | Specific fields (verfahren_type values, doctype list, korrektur-rules path) |
| VISION axes | Three-axis framing (intertwining / sparring / authorship preservation) | Per-axis *content* — what counts as authorship in the domain |
| Decision-record format | The structure itself (Context / Decision / Why / Alternatives / Revisit) | Specific decisions — which mechanisms are committed |

**Anti-patterns the discipline catches:**

- ❌ A meta-rule that names "B-Plan" / "Begründung" /
  "Festsetzungen" in its body. Those are PBS instance content;
  the rule should describe the *shape* (e.g., "doctypes have
  required + optional sections per their manifest entry") and
  let PBS provide instance content for that shape.
- ❌ A persistence structure assuming German legal taxonomy
  (gesetze / urteile / leitfäden) at architectural layer.
  Pattern is "layered references manifest with invalidation
  contract"; instance is the German-law taxonomy.
- ❌ An MCP tool whose *interface* embeds domain knowledge
  (e.g., `validate_b_plan_begruendung` as a tool name). Pattern
  is `validate_doctype(doctype: <slug>)`; instance is what
  doctypes exist.
- ❌ A skill body that hardcodes domain-specific values rather
  than reading from office-config or manifests. Already covered
  by plugin-conventions §13 anti-pattern; now also a
  pattern-vs-instance violation.

**Coupling exceptions** (where domain-coupling at architecture
level is allowed):

- The *vocabulary* used in examples (decision records, ARCH
  body) can use PBS terminology for legibility, as long as the
  underlying rule generalizes. "PBS bausteine" in an example is
  fine; a rule that *only* makes sense for PBS bausteine is not.
- The instance directory itself (`extensions/`, `memory/`,
  `office-config.yaml` populated values) is unconditionally
  PBS-instance. The pattern is the *schema*; PBS is the
  *content*.

**Discipline check at audit/design-review time:**

- Audit slice 14 (boundary adherence) extends naturally to this:
  "is this commitment pattern-level or instance-level?" applies
  to placement of decisions across the architecture/instance
  boundary, same way it applies across the LLM/Python boundary.
- Design-review target 9 (Subsumption check) implicitly tests
  this: a new mechanism that subsumes a PBS-specific legacy
  mechanism *and* generalizes is correct; one that subsumes
  PBS-specific in a PBS-specific way perpetuates the coupling.

**Connection to current work**: every session-7 commitment
(meta-rule 4 fail-closed corollary, target 9 subsumption check,
audit slice 18 legacy retirement scan, framing skill, audit-trail
v2 single-write architecture, Skill Bundle frontmatter
convention) is pattern-level by construction. The discipline
makes that property explicit and load-bearing for future work.

### Validation under the single-domain-pioneer constraint

PBS is operated by a single planning-domain expert. Realistically
**we will not implement second-domain instances ourselves** —
legal practice, research, engineering, etc. are domains the user
doesn't work in. Hand-building a "second instance" in a domain
the user doesn't actually practice would produce evidence of
*the user's idea of that domain*, not of the actual domain —
worse than no evidence, because misleading.

This constraint shapes the validation strategy: we **cannot** use
"build 2-3 hand-instances and measure overlap" as the validation
path. Waiting for empirical evidence from a real second-domain
deployment that may never come (consulting engagement; second
office adoption) becomes manufactured restraint disguised as
rigor — a way to defer architectural decisions indefinitely.

**Working method instead — best-effort split + immediate PBS
validation:**

The split is implemented now (pre-RAG), against PBS, with two
distinct validation signals:

| Signal | What it tells us | Source |
|---|---|---|
| **#1 — split doesn't break PBS** | The proposed split is implementable; refactor is executable; tests pass; skills route correctly; project state round-trips. Catches mechanics-level issues that pure reasoning misses. | Implementing the split now against PBS — **immediate** feedback. |
| **#2 — split chose the *right* boundary** | The pattern/instance line generalizes to other domains. Catches the split being too PBS-shaped (overfit). | Only known when a real second-domain implementation lands — **deferred, possibly indefinite**. |

Signal #1 is necessary-but-not-sufficient: confirms no regression
but can't confirm correct boundary. Signal #2 confirms boundary
but requires implementation that may never happen here. **Doing
the split now is the maximum validation we can extract before
signal #2 arrives — and crucially, doing it later is more
painful** (post-data-accumulation refactor + skill retrofits +
migration scripts vs. clean refactor today). The 3-5 hypothetical-
domain thought experiment (legal-practice, research-paper,
engineering-doc, medical-records, regulatory-filing) is the
*reasoning input* to the split; signal #1 is the *immediate
empirical check*; signal #2 waits for real second-domain.

**The thought experiment as legitimate epistemic basis**: it
doesn't require working in those domains, just thinking carefully
about them as architectural-imagination targets. Signal #1
catches what the thought experiment missed at implementation
level; signal #2 (when/if it arrives) catches what both missed
at boundary level.

This explicitly is a **best-effort** discipline, not a proven
one. The split *will* be wrong somewhere; the question is
whether it's *less wrong than no split* and *less expensive to
correct than no-split-then-painful-migration*. Pre-RAG is the
unique window where the cost answer is "yes."

Pre-RAG commitment #9 (`ROADMAP.md`) is the concrete realization:
the reasoning pass + best-effort split implementation + PBS
regression validation are bundled as one work stream, scheduled
before Phase 1 corpus download.

### Office-vs-department distinction (resolved session 9 per #12)

**Problem surfaced session 7 (after partner-built plugin
comparison)**, **resolved session 9** per
`docs/decisions/office-vs-department.md`. This section captures the
architectural distinction; the decision record carries the full
per-question reasoning + downstream constraints + defers.

The term "office" in PBS-bureau was used for two distinct things
that needed separation:

- **Department**: a single capability area with its own
  workflow, doctypes, memory, and external authorities. Examples:
  planning-document-work (what PBS implements today), project-
  management, invoicing, HR, marketing, brand-voice, legal-work.
  Anthropic's `partner-built/brand-voice` is a department-shaped
  plugin (one capability, three skills, three commands).
- **Office**: a container for *multiple departments*, coordinated
  via shared office-level state (projects, clients, deadlines,
  actors), natural abstractions (a "project" entity flows between
  departments), ad-hoc context sharing (explicit data-passing for
  non-obvious flows), and integration/setup configuration.

PBS-bureau today **conflates the two**: we have one department
(planning-document-work) wrapped in office-level scaffolding
(setup-office, office-config.yaml, projects-index, references-
manifest, orchestrator). A real Schulz Planungsbüro has at least
three departments: planning-document-work + project-management +
invoicing. Other PBS-shaped offices would have similar shapes.

**Implications under pattern-vs-instance discipline:**

- Pattern: office structure containing N departments.
- Instance: PBS office contains {planning-document-work, PM,
  invoicing} (eventually); a hypothetical legal practice office
  contains {legal-work, matter-management, invoicing}; a
  research lab office contains {research, grant-management,
  lab-operations}.
- Office-config.yaml gains `departments.<name>` sections.
- Skills gain a `department:` frontmatter field (REQUIRED, no
  silent default per strict-validation discipline); office-level
  skills declare `department: office`.
- Memory taxonomy gains a 4th orthogonal axis: scope-orthogonality
  becomes (universal × domain × state × department), opt-in per
  entry. Most existing entries stay in the original 3 cells;
  department-specific entries declare the 4th.
- Cross-department workflows are **event-shaped, not call-shaped**
  (per Row 4 of `a2a-and-gemini-pattern-emulation.md`). Each
  department declares `event_subscriptions:` in
  `extensions/department/<dept>/department.yaml`; orchestrator's
  watch-list extends to filter by subscription + exclude self-
  emitted events. No new event mechanism — reuses AuditEvent
  infrastructure.
- ProjectState gains `departments_active: list[str]` field for
  routing + audit-filter purposes. Gate-mediated update via
  `record_audit_event` (logic deferred to #6 retrofit).
- Skills are **singleton-department**; multi-department coordination
  via office-level orchestrating skills.
- Offices have **0..N departments** — zero (single-skill utility),
  one (PBS today, brand-voice partner-built plugin), or many
  (Schulz future, hypothetical legal/research/medical offices).
- AI-office-builder (v2) generates offices with whatever department
  composition the domain spec declares. Per-domain spec input
  includes department list + per-department config + integration
  spec.

**Pattern-vs-instance limitation surfaced**: project-as-long-running-
entity is PBS-instance, not pattern-universal. Some offices
(brand-voice, single-skill utilities) have no project entity.
Architecture supports both project-having and project-less offices.
Constraint passed to #9 (Pattern-vs-instance split): ProjectState
core/extension split should make the project entity itself an
opt-in extension, not a pattern-level mandatory.

**What's deferred and where** (per `office-vs-department.md`):
- Per-department phase tracking (`phases: dict[str, str]`) and
  per-department lifecycle (`lifecycle: dict[str, Lifecycle]`) →
  #9 (Pattern-vs-instance split, still pre-RAG).
- Office-config `departments.<name>` schema bump + migration → #11
  (Cowork integration, co-located with `pbs.local.md` migration).
- Skill frontmatter `department:` sweep across all 19+ skills → #11.
- `extensions/department/<dept>/department.yaml` event_subscriptions
  file format implementation → #11.
- `integrate-department <slug>` skill creation → #11.
- `record_audit_event` gate-side `departments_active` update logic
  + `query_audit_trail` `department:` filter → #6 (audit-trail v2
  retrofit).
- `search_corpus` `department_filter:` arg → Phase 1 corpus work.

**Connection to brand-voice comparison**: brand-voice is a
single-department plugin (in our framing: one department, all
skills declare `department: brand-voice`, no cross-department
coordination needed since N=1). PBS today is also a single-
department office (planning-document-work). The pattern handles
N=0/1/many uniformly.

---

## Entity-elevation discipline

A load-bearing companion to pattern-vs-instance discipline. Where
pattern-vs-instance asks "is this commitment at the right *level*
(pattern or instance)?", entity-elevation asks "is this concept
*entity-shaped at all* (vs event / nested / memory / config)?"

**The principle**:

> **Prefer events + nested fields + memory entries over new
> managed entity types. Elevate to first-class managed entity
> only when stable-identity + state-of-record + lifecycle ALL
> apply.**

**Why this matters**: pre-emptively elevating concepts to
first-class managed entities (Pydantic schemas + MCP CRUD tools +
persistence) creates schema sprawl. Each new entity adds: storage
layer commitments, query surface, migration burden, schema
versioning overhead, and cognitive load on every consumer. The
risk if undisciplined is the architecture creeping toward a
**relational SQL schema** — one entity per noun, foreign keys,
joins, normalization. That's catastrophic for LLM-mediated AI
offices: it makes the architecture brittle, slow to evolve, and
re-implements enterprise software's worst tendency.

**Right level**: closer to **knowledge graph + document store
with stable references** than Oracle. Entities have identity
(referenced by ID); relationships ride in audit-event details +
ID fields on entities; "joins" are answered via filtered queries
over events / per-entity stores / memory / adapter APIs. **No
join planner needed.**

### The 3-test (all three required to elevate)

For each candidate, walk all three:

1. **Stable identity** — has an ID/slug that persists across
   sessions and is referenced by other things?
2. **State of record** — has fields whose authoritative current
   value matters (not just historical)?
3. **Lifecycle** — has phases or status that progress over time?

**If all three**: managed entity. Lock in.
**If any missing**: route to the appropriate alternative —
event-kinds (moments-when-things-happened), nested fields
(data only meaningful in context of a parent), memory entries
(prose-shaped knowledge), or reference data (static / config).

### Worked-example reasoning

| Concept | Identity | State | Lifecycle | Verdict |
|---|---|---|---|---|
| Project, Client, Actor, Invoice, Asset, Matter, Manuscript | ✅ | ✅ | ✅ | ✅ entity |
| Approval, Decision, Send, PhaseTransition | each is one moment | fixed at action | doesn't progress | ❌ event kinds on AuditEvent |
| LineItem, Deadline, ContactPerson | only as part of parent | not independent | none | ❌ nested fields |
| Notification | inbox is state-of-record | external system | external system | ❌ adapter + event |
| Report, Dashboard | generated on demand | projection | none | ❌ generated artifact (render_*) |
| BusinessCalendar | yes | yes | none | ❌ reference data (config) |
| DocumentVersion | snapshot ID | immutable | none | ❌ event + bytes |

### How "joins" are answered without foreign keys

| Question | SQL approach | PBS approach |
|---|---|---|
| "All invoices for client X" | `JOIN` | Adapter API: `lexware.invoices(client_id=X)`. Or audit-trail filter. |
| "All projects with overdue deadlines" | `WHERE deadline < NOW()` | Native query on Project store filtered by `deadlines[].date < today`. |
| "Audit history of decisions made by colleague Y" | Multi-table join | Audit-trail filter: `actor=Y AND kind=decision`. |
| "Which bausteine cite §44 BNatSchG?" | Full-text + reference table | Memory query (post-#14): `search_memory(query="§44 BNatSchG", kinds=["baustein"])`. |

Filtered queries over a small set of stores. No join planner.

### Where the discipline is enforced (multi-checkpoint)

Defense in depth — discipline applied at five points in the workflow:

1. **Conversational gate (in-chat)** — when proposing a new entity
   during design discussion, walk the 3-test out loud before
   anything is persisted.
2. **Design-review target 11 (PRIMARY GATE — prospective)** —
   when a decision record / refactor / new commitment proposes a
   managed entity, target 11 enforces the 3-test before persistence.
   Same role as target 9 (subsumption) and target 10 (pattern-vs-
   instance).
3. **Decision-record convention** — any decision record naming a
   new managed entity must include explicit 3-test verdict
   subsection (per-criterion yes/no with reasoning).
4. **`integrate-department` runtime gate (post-#11)** — when
   onboarding a new department to a deployment, the skill walks
   each `managed_entities:` declaration in `department.yaml` and
   runs the 3-test interactively. Catches department-module-
   author drift.
5. **Audit slice 20 (retrospective)** — scheduled / on-demand scan
   of `extensions/.../entities/` Pydantic schemas + decision
   records, scoring against the 3-test. Catches drift over time.

Each catches a different failure mode. Discipline in design AND
in code AND in audit — analogous to meta-rule 4's strict-validation
defense in depth.

### Connection to other disciplines

- **Pattern-vs-instance** (above): different question. Pattern-
  vs-instance asks "right *level*?" Entity-elevation asks
  "entity-shaped *at all*?" Both apply at design time.
- **Subsumption check (target 9 / slice 18)**: when entity-
  elevation passes (entity-shaped is right), subsumption check
  separately asks what existing mechanism it replaces.
- **Strict validation (meta-rule 4)**: once an entity is correctly
  elevated, meta-rule 4's discipline applies to its Pydantic
  contract (required fields strictly required, no silent defaults
  for missing data, fail-loud on contract violation).

See `docs/decisions/office-vs-department.md` "When to elevate to
managed entity (the three-test discipline)" subsection for the
full reasoning + examples.

---

## Glue-not-replacement principle

PBS is **the glue layer** that brings cross-concern AI-mediated
reasoning to existing infrastructure. It is **not** a replacement
for the systems customers already have (BPMN engines, accounting
tools, CRMs, time-tracking, calendars, ticketing systems, etc.).
The architecture is integration-first by design.

**Why this matters**: most enterprises have **decades of
investment** in workflow / accounting / case-management
infrastructure. Selling rip-and-replace is a losing pitch — both
practically (the migration is too expensive) and politically (the
internal champions of those systems block adoption). The
addressable market for "AI office that augments your existing
stack" is **substantially larger** than "AI office that replaces
your existing stack."

**The principle, stated**:

> **PBS connects to existing infrastructure where it exists;
> provides native alternatives where it doesn't. Both modes work
> uniformly through the same framework. We never ask the customer
> to choose between AI augmentation and their existing
> investment.**

**Concrete implications across the architecture**:

| Principle expression | Architectural mechanism |
|---|---|
| Existing accounting tool? Use it. | Adapter-mode managed entity (`Invoice` via Lexware/FastBill/sevDesk adapter) per #12 |
| Existing time-tracking? Use it. | Adapter-mode managed entity (`Timesheet` via Harvest/MOCO adapter) |
| Existing BPMN/workflow engine? Augment it. | BPMN-engine adapter class (v1.x-v2 ROADMAP); service-task delegation + decision-automation + cross-process intelligence layered ON TOP |
| Existing calendar? Connect to it. | Adapter-mode (CalDAV / Google / Microsoft) |
| Existing CRM? Connect to it. | Adapter-mode managed entity (`Client` via Salesforce/HubSpot adapter) |
| No existing tool? Use built-in. | Native-mode managed entity (`Project` for B-Plan workflows; PBS IS the SoR — no external alternative exists) |
| Existing audit / compliance system? Augment with AI-mediated reasoning. | Cross-process events flow as `actor_kind=external_agent`; PBS adds judgment-mediated layer to existing audit infrastructure |

**The architectural mechanism the principle relies on**:

- **Meta-rule 1's integration-adapter pattern** (`Pydantic Protocol` + concrete adapter implementations selected per office-config) — already established
- **Adapter-mode managed entities** (per #12, `office-vs-department.md`) — generalizes the pattern from auxiliary integrations to primary department system-of-record
- **Adapter-emitted events** (per #9 Gap B, `office-vs-department.md` infrastructure-primitive review) — bidirectional flow; external state changes emit `actor_kind=external_agent` audit events
- **Mixed-mode per-entity** (per #12) — a single department can have some entities in adapter mode, some in native mode. Real-world deployments mix.

### Role-shift framing — what changes for the worker (per VISION axes)

The principle has a sharper worker-facing implication, grounded in `VISION.md` axes 1-3 + Vivienne Ming's research on AI-human hybrid teams (oracle / validator / sparring partner modes).

Specialized tools historically did **two jobs in one bundle**:
1. **Authoring** — creating and modifying the underlying data
2. **Presentation / review / output** — rendering, exporting, reviewing the result

The role-shift: **specialized tools' authoring role moves; presentation/review role stays.** But the shift isn't uniform — it splits along VISION axis 2's mode distinction:

**Mechanical authoring** (drawing geometry, formatting LaTeX, computing fields, routine drafting, file-format conversions, cross-reference lookups):
- **Full automation** — AI takes over completely via specialized API layers (gis_utils for GIS, latex/PDF skills for documents, integration adapters for accounting/calendar)
- The worker's cognitive load on this layer → 0
- The specialized GUI tool (QGIS, AutoCAD, etc.) reduces to its **presentation/review surface**

**Substantive authoring** (judgment-bearing decisions: which argumentation type, which legal interpretation, which scope, which classification scheme):
- **Sparring mode** (NOT full automation; per VISION axis 2 — Ming's productive mode)
- AI generates options + counter-arguments + alternatives; human pushes back, interrogates, commits
- Cognitive ENGAGEMENT preserved (per VISION axis 3 defensibility test)
- Time + friction substantially down vs solo work (options presented; counter-arguments surfaced; references at hand; mechanical layer freed time returns to substantive engagement)

**Net result for the worker**: less time + less friction + better accuracy + preserved cognitive engagement. **All four, simultaneously.** The substantive thinking remains theirs; the supporting infrastructure carries weight that used to cost time + friction without adding value. The thinking gets *better-supported*, not *easier in the dishonest "AI did it" sense*.

**The trap to avoid** (per Ming's research warning):
- **Oracle mode** (humans submit AI's answer; performance same as AI alone) — destroys human contribution
- **Validator mode** (humans seek AI confirmation; sycophancy loop; performance worse than AI alone) — actively degrades

**The architecture's job is to keep the worker in sparring mode for substantive work.** VISION axis 2's sparring requirements (counter-argument-as-first-class, anti-sycophancy guard, commit-to-recommendations, asymmetric knowledge respect, visible reasoning, selective friction calibration) make this enforceable rather than aspirational. Per the **Information-Exploration Paradox** (VISION §229-247): without these protections, the AI consumes the worker's exploration capacity; with them, the AI augments it.

**For consulting positioning** (see `docs/strategic-positioning.md`
for full treatment + lived-experience credibility framing):

> **"Your BPMN engine handles the workflow. Your accounting tool
> handles invoicing. Your CRM handles clients. Your calendar
> handles scheduling. Your specialized GUI tools (QGIS, AutoCAD,
> domain-specific apps) become presentation/review surfaces. We
> add the cross-concern AI office layer on top — handling the
> mechanical authoring + cross-tool integration + cross-department
> coordination automatically, while keeping the worker in sparring
> mode (not oracle mode) for substantive decisions. Less time +
> less friction + better accuracy + preserved cognitive
> engagement. The friction in substantive work is the feature,
> not the bug."**

This is **a fundamentally different sale** than "buy our AI tool to
replace [vertical SaaS]." Different addressable market; different
political dynamics within enterprise prospects; different
implementation timelines; different risk profile. Also a
fundamentally different sale than the typical AI-tool pitch
("faster answers" — Ming's validator-mode trap; "AI handles
decisions" — Ming's oracle-mode trap).

**Connection to other disciplines**:

- **Pattern-vs-instance**: the glue principle is itself pattern-
  level (every AI office, regardless of domain, integrates with
  domain-relevant existing infrastructure). Instance content =
  which specific adapters exist for the deployment.
- **Entity-elevation discipline**: helps decide which managed
  entities should be native vs adapter-mode. Strong default toward
  adapter-mode when external system is the natural state-of-record.
- **Meta-rule 1 (app-vs-office)**: the integration-adapter pattern
  is the implementation mechanism; this principle states the
  WHY (connect, don't replace).
- **Meta-rule 4 (execution determinism)**: deterministic gates
  delegate to deterministic external systems where they exist;
  judgment lives in the AI layer.

**When this principle pulls against pure native-mode preference**:

If two viable paths exist (native or adapter), default toward
adapter when the customer has the external system. Only choose
native when:
- No external alternative exists (PBS-bureau planning Project)
- The customer is solo / small enough that running an external
  system is overhead (small deployments per #13's CCX23 tier)
- Native gives demonstrable value the adapter can't (e.g., custom
  domain-specific reasoning that pre-exists in PBS's skills)

The architecture supports both modes uniformly (#12); the
principle expresses the strong preference toward integration when
viable.

---

## AI-as-runtime hybrid-shape principle

> **Domain semantics, process flow, conditional rules, and
> contextual knowledge live in markdown bodies attached to entity
> files — not in encoded schemas or hardcoded skill procedures.
> Cross-domain portability is achieved by AI reading prose, not
> by abstracting over schema variants. Structured layers are
> reserved for interfaces, identity, persistence, and machine
> contracts; everything else is prose; AI is the runtime that
> fuses them at use-time.**

### Why this matters

Trying to capture domain richness (sub-entity required/optional
rules, process flow, conditional logic, expert reasoning) in
formal schemas leads to two failure modes:

1. **The SQL-DB trap**: schemas grow until they recreate
   relational-database complexity. Per the entity-elevation
   discipline this is *catastrophic for LLM-mediated AI offices*
   — brittle, slow to evolve, re-implements enterprise software's
   worst tendency.
2. **Prose squeezed into structured fields**: the existing strain
   visible in `extensions/universal/doctypes.yaml` and
   `references-manifest.yaml` — `description: >` and `notes: |`
   block scalars holding what is fundamentally prose
   (descriptions, expert reasoning, when-this-applies notes).
   Block scalars work mechanically but suppress the form prose
   wants to take: no headings, no structured lists, no links, no
   examples.

The corrective: **AI processing is not a bridging layer between
structured + freeform; it REPLACES the encoded-rules layer
entirely.** The model already in use elsewhere — memories
(frontmatter + markdown body, AI does the understanding) — is the
canonical pattern. There is no memory engine parsing rules; the
memory describes the thing in prose, AI applies it at runtime.

This is the explicit implementation of v0.13's gesture: *"closer
to knowledge graph + document store with stable references, not
Oracle."*

### The three-layer frontmatter contract

Every managed entity, every manifest entry, every doctype
declaration follows this shape:

| Layer | Lock-down | Enforced by |
|---|---|---|
| **Layer 1 — Universal frontmatter** (every entity) | STRICT (fail-loud) | MCP gate (Pydantic base) |
| **Layer 2 — Type frontmatter** (per-entity-type) | STRICT (fail-loud) | MCP gate (Pydantic subclass per type) |
| **Layer 3 — Per-deployment extension fields** | TBD per #9 | TBD per #9 |
| **Body conventions** (recommended sections per type) | RECOMMENDED (warn) | Audit skill + design-review skill (NOT gate) |
| **Body free prose** | UNCONSTRAINED | — |

**Layer 1 fields** (every entity): `id`, `label`, `type`, `scope`,
`scope_key`, `status`, `last_updated`, optional `description`,
optional `tags`. The `type:` field routes to the Layer-2 Pydantic
subclass at gate-read time.

**Layer 2 fields**: per-entity-type, locked. Doctypes have
`style_ref`, `master_file_pattern`, `paired_with`, `document_class`,
etc. References have `source_url`, `canonical_path`,
`fetch_method`, `last_fetched`, `checksum_sha256`, etc. Projects
have `bundesland`, `verfahren_type`, `lifecycle`, `phase`,
`departments_active`, etc. (today's ProjectState fields, relocated).

**Body conventions** (per entity type, documented at
`docs/conventions/entity-md-spec.md`, audit-enforced not
gate-enforced):

| Entity type | Conventional body sections |
|---|---|
| `doctype` | When this doctype applies / Section conventions / Pairing semantics / Domain-specific deviations |
| `reference` | Why this matters / Key sections for our work / Recent amendments / Common citations / Cross-refs |
| `project` | Context / History (append-only) / Open questions / Decisions |
| `client` | Communication preferences / Billing conventions / Project history summary / Watch-outs |
| `process` | Phase sequence / Required doctypes per phase / Mandatory triggers / Exceptions and shortcuts |
| `actor` | Role + responsibilities / Working preferences / Capabilities + limits |

Recommended-not-required avoids the rigidity that hard-enforced
templates produce (entities that don't fit the template get filler
text). Same pattern memories already use — feedback memories
conventionally have **Why:** + **How to apply:** lines (documented
in CLAUDE.md), but no validator enforces it; review/practice does.

### Where conditional rules live

Resolved: **rules about *when* something applies belong with the
*process*, not with the entity itself.** The doctype md describes
what the doctype IS; the **process md** (per verfahren type)
describes the flow + which doctypes the flow produces; the
project entity's body is per-instance narrative, not rules.

Worked example: `extensions/department/planning/processes/
beschleunigtes.md` (§13a) declares its phase sequence WITHOUT
Umweltbericht. `regelverfahren.md` declares Umweltbericht as
required. Project state references `verfahren_type:
beschleunigtes`; orchestrator loads the matching process md to
know what's expected. This is **process-as-md, not
state-machine-as-data**.

### MCP gate generalization (lands in #9)

Today: per-entity tools (`read_project_state`, `write_project_state`).

Tomorrow (per #9 implementation): generic `read_entity(path)` /
`write_entity(path, file)` with `type:`-field dispatch to the
appropriate Layer-2 Pydantic subclass. Body preserved as-is across
read/write cycles (same shape state.md uses today). Replaces
per-entity-tool sprawl.

### Connections to other disciplines

| Discipline | Connection |
|---|---|
| **Entity-elevation** | Hybrid-shape applies AFTER the 3-test verdict. Entity-elevation says "don't over-elevate"; hybrid-shape says "for things that DO elevate, here's their shape." |
| **Pattern-vs-instance** | Hybrid-shape IS how cross-domain portability is achieved. Same shape (frontmatter + body), different prose per domain. |
| **Glue-not-replacement** | Adapter-mode entities use the same hybrid-shape contract; per-deployment markdown body is the natural home for "how does THIS office use the external system." |
| **Strict-validation (meta-rule 4)** | Layer 1 + Layer 2 frontmatter respect strict-validation: required fields fail-loud, no silent defaults. Body is unconstrained by design — that's the principle. |
| **Source-of-truth (meta-rule 3)** | Hybrid-shape doesn't change source-of-truth placement; it changes **how** source-of-truth content is shaped (when content is semantic/process rather than identity/config). |

### What stays structured (counter-cases)

The principle does NOT push everything to markdown. Things that
remain rightly structured:

- **Office-config** (`~/.config/pbs-bureau/office.yaml`):
  deployment switches, paths, mode/adapter selection. Pure config.
- **AuditEvent / Pydantic schemas**: events are interface
  contracts between skills + tools. Structured by design.
- **Adapter Protocols**: Pydantic Protocols defining
  machine-readable contracts that adapter implementations satisfy.
- **plugin.json**: plugin manifest. Mechanical.
- **office-config.schema.yaml**: schema spec. Pure structural.

The boundary: **structured for interfaces, identity, persistence,
machine contracts; markdown for semantics, rules, domain knowledge,
process descriptions; AI as runtime fuses them.**

### Discipline check at audit + design-review time

- **Audit slice 21** (entity-md conformance): scans
  `extensions/**/*.md` entity files for Layer-1 + Layer-2
  frontmatter conformance + body recommended-section presence.
  Warns on missing sections; doesn't fail. Implementation bundled
  with #9.
- **Design-review target 12** (entity authoring conformance):
  when authoring or modifying an entity md, validates frontmatter
  against the appropriate Pydantic subclass + suggests missing
  recommended body sections. Coordinates with target 11
  (entity-elevation) so over-elevation gets caught alongside
  shape-misuse.
- **Decision-record convention**: any decision proposing a new
  managed entity type or new manifest type must include
  Layer-1 + Layer-2 frontmatter spec + body-spec sections.

### Connection to VISION

The principle is the architectural expression of VISION axis 1
(intertwining-AI-workflow). AI is not a feature of the system; it
is the runtime that fuses the layers. Without AI as runtime, the
markdown bodies are inert prose; with AI as runtime, they ARE the
rules + process + domain knowledge.

Memory drift toward oracle-mode framings shows up as architectural
drift toward over-structuring: when AI is treated as a passive
answerer (oracle), the architecture compensates by encoding rules
in schemas. When AI is treated as a workflow participant
(intertwining axis), the architecture relies on AI to read prose.
The hybrid-shape principle locks in the latter.

See `docs/decisions/ai-as-runtime-hybrid-shape.md` for the full
decision record (worked examples, downstream constraints, defers,
revisit triggers).

---

# Meta-rules

The architecture rests on **four meta-rules**. Plus one named
convention (scope-orthogonality) that applies *within* layered
content. New content goes through the relevant meta-rule before
placement.

## Meta-rule 1: app vs office (deployment portability)

The repository is **a generic German planning-bureau workflow app**
that any Planungsbüro can deploy. It is not a PBS-specific instance.
Per-deployment configuration — paths, identity, actors, styling,
state-law extensions — lives **outside the repo** in an
`office-config.yaml` resolved via:

1. `$PBS_OFFICE_CONFIG` (env var, takes precedence)
2. `${XDG_CONFIG_HOME}/pbs-bureau/office.yaml`
3. `~/.config/pbs-bureau/office.yaml`

Schema: `docs/office-config.schema.yaml`. Generated interactively by
the `setup-office` skill on first run.

**Hard rules for app code (skills, backend, hooks, memory):**

- Never hardcode hidrive/projects/state paths. Read them from
  `roots.*` in the loaded office-config.
- Never hardcode office identity (name, address, signature, phone,
  email). Read them from `office.*` (post-v3 merge of identity into
  office).
- Never hardcode actor names. Read `actors[]` from config (kind=internal
  for practices, kind=external for partners).
- Never hardcode client/project names. Use neutral examples in docs
  (`YY-NN <Client> - <Location>`); refer to live projects only via
  paths the user provides at runtime.
- State-specific and domain-specific references are discovered by
  walking `<repo>/extensions/{universal,domain/<X>,state/<X>}/`
  filtered by the office's `scope.{domains,states}` (loader walks
  the union; manifests are NOT enumerated in office-config).
  Bundesland is a per-PROJECT property (`state.md.bundesland`), not
  an office property.
- LaTeX styling lives in the office's `office-style.sty`, NOT in
  app skeletons or classes.
- Office identity macros (`\OfficeName`, `\OfficeAddressLines`,
  `\OfficeSigner`) are auto-generated by the backend from `office.*`
  before each compile, NOT hand-written.

### Mechanism: pluggable integration adapters

Where the app interfaces with external systems whose mechanism
varies per deployment (email service, calendar, scanner, phone,
accounting, DMS, GIS, etc.), the implementation lives behind a
small **protocol + adapter pattern**: a Python `Protocol` defines
the contract; each adapter (`thunderbird-maildir`, `imap`, `caldav`,
etc.) implements it; office-config selects which adapter is active
per class.

Same architectural lesson as paths/identity/actors/scope: no
hardcoded mechanism. The adapter boundary is in place from day one;
concrete adapters land per demand. Adapters live at
`backend/mcp-server/src/pbs_mcp/integrations/<class>/<adapter>.py`,
each exporting an `Adapter(config: dict)` class implementing the
protocol at `<class>/protocol.py`. `load_adapter(class_name)`
resolves via `cfg.find_integration(class_name)` (v3 free-form
list).

The class set is open — any string is valid as long as a matching
subpackage exists. (Per design-review: integration adapters are
*backend-internal organizing pattern*, not a top-level meta-rule
peer; they're a consequence of app-vs-office deployment portability.)

**Generalization to department-managed entities (v0.12 per session-9
followup)**: the same Pydantic Protocol + concrete adapter pattern
also serves as the **adapter delivery mode for department-managed
entities** (per `docs/decisions/office-vs-department.md`). Two
delivery modes per entity: **native** (PBS owns the Pydantic schema
+ MCP CRUD tools — used when no external alternative exists, e.g.,
planning's Project entity for B-Plan workflows; brand-voice's Asset
entity), or **adapter-delegated** (external system owns system-of-
record — used for departments where mature tools exist, e.g.,
Invoicing's Invoice → Lexware/FastBill/sevDesk; PM's Timesheet →
Harvest/MOCO; HR's Employee → BambooHR/Personio). Mixed-mode is
required and supported per-entity within a single department. The
adapter implementation pattern is identical to auxiliary integrations
above; the **consumer set expands** from email/calendar/scanner to
primary department system-of-record. Department-managed-entity
adapters live at `extensions/department/<dept>/adapters/<entity>/`
(per the office-vs-department decision record schema additions).
Office-config selects per-entity mode + adapter via the
`departments.<name>.entities.<entity>.{mode, adapter, config}`
section.

**Schema versioning + migrations.** Adding fields to office-config
schema requires bumping `CURRENT_SCHEMA_VERSION` in
`backend/.../office_config.py` and adding a migration at
`backend/.../office_config_migrations/v<N>_to_v<N+1>.py`. The
dispatcher applies migrations sequentially in-memory on every load.

## Meta-rule 2: memory vs RAG (citation freshness)

A hard line: **what lives in memory** vs **what lives in the RAG
corpus**. The split protects against legal-citation rot.

**Memory** (loaded into context every session) holds:
- Workflow logic — phase order, phase→state mapping, doctype structure.
- Conventions — German number formatting, quotation conventions,
  hyphenation rules, korrektur-rules.
- Reference content (project-structure.md, per-project-memory
  format docs).
- Saved bausteine.
- Universal reasoning patterns that don't depend on current law text.

(Note: doctype + reference registries are NOT memory — they're
layered manifests in `extensions/`. Memory holds prose conventions
and saved instance records.)

**RAG** (`<roots.references>/`, retrieved on demand via
`search_corpus` / `read_corpus_file`) holds:
- Verbatim legal text (BauGB §X, BNatSchG §Y, etc.).
- Verbatim Verfahrensvermerk wording.
- Court ruling text.
- Leitfaden content from publishing bodies (KNE, LUNG, etc.).
- Anything that can be amended at the source.

**§-references as labels are allowed in memory** ("Phase 5a —
§3 Abs.2 BauGB") for navigation. Verbatim legal text and paraphrased
law-text are NOT — those route through RAG.

**Source-grounding rule.** Any legal citation in produced output
(drafts, reviews, mails) must be backed by a tool result — even if
the same §-number appears in memory. Memory's role is naming and
navigation, never authoring. The §-label "§3 Abs.2 BauGB" appearing
in memory does NOT satisfy the citation-evidence requirement when
drafting.

## Meta-rule 3: source-of-truth & invalidation

Every entity declares its invalidation contract: how the system
detects that this thing is stale, superseded, or wrong, and what
needs to happen when it is.

**Per entity type** (see "The five entity types" below for full
list):

| Entity | Invalidation contract |
|---|---|
| Skill Bundle | semver `version:` field; bump on behavior change. Body changes invalidate skill behavior on `/reload-plugins`. |
| Memory (prose) | `references_used: []` frontmatter declares dependent law refs. `research-references` flags affected docs in `memory/product-backlog.md` when a referenced law is updated. |
| Memory (records) | `status: active|flagged|archived|superseded`, `last_validated`, `review_due`, `references[].verified_against_version`. `validate-bausteine` sweeps for stale records. |
| Memory (audit-log) | Append-only `<project>/_ai/audit-trail.jsonl` per docs/decisions/audit-trail-v2.md (single-write supersedes v1's dual-write). Each `AuditEvent` carries `id`, `timestamp`, `kind`, `actor`, `actor_kind` (human/skill/external_agent per a2a-and-gemini-pattern-emulation.md), `actor_card?`, `origin_agent_card?`, `sources[]`. Events never invalidate (immutable history); `causes[]` chain captures supersession. `query_audit_trail` is the canonical query layer; `render_audit_trail` produces prose views from queries. Skills call `record_audit_event` (or `record_decision` for legal-defense provenance via `decisions.md` mirror — gate-mediated). Per the strict-validation discipline, `actor_kind` is required; `external_agent` events MUST name `origin_agent_card`. |
| Backend | Python imports + Pydantic schemas; restart MCP server after changes. No declarative invalidation hook. |
| Configuration | `schema_version` + migration framework. Manifests carry `last_updated` + per-entry `last_fetched` + `checksum_sha256`; `research-references` re-fetches on schema/source change. |
| External data | Per-project `_ai/state.md.lifecycle` declares phase + status (today single-valued — per-department `phases: dict` + `lifecycle: dict` deferred to #9 per `office-vs-department.md` D1+D2). `_ai/state.md.departments_active: list[str]` (added v0.11 per #12) declares which departments have engaged with this project; gate-mediated update via `record_audit_event` (logic deferred to #6). `roots.references_root` corpus carries `changelog.md`. |

**Cross-cutting concern handler.** Contract reading is layered
across two skills:

- `research-references` is the *trigger*: after fetching an
  updated reference, it scans both bausteine (`references[]`) and
  memory docs (`references_used[]`) for matches. Bausteine
  matching → flagged. Memory docs matching → logged to
  `memory/product-backlog.md` with affected paths.
- `validate-bausteine` is the *comparator*: it reads the
  `references[].verified_against_version` field on flagged
  bausteine and compares it against the current
  `current_amendment_form` from the manifest, surfacing drift
  for the user.

The split is intentional — research-references detects *which*
entities cite updated laws; validate-bausteine determines
*whether each entity's cited form is still current*. Both flows
are required to close the invalidation loop; neither alone
suffices.

**Frontmatter declares invalidation hooks.** Cross-cutting docs
that name laws declare them in frontmatter:

```yaml
---
references_used:
  - {law: BauGB, paragraph: §3 Abs.2}
  - {ruling: BVerwG-9-A-22-11}
  - {leitfaden: KNE-Anlagengestaltung}
---
```

This rule was previously implicit (scattered across "What changes
invalidate what" prose + per-entity-type schemas). Promoting to a
meta-rule forces every new entity type to answer "how does the
system know you're stale?" before shipping.

## Meta-rule 4: execution determinism (where deterministic work lives)

About *where* operations execute, not where content lives.

**Core principle.** Operations with a single deterministic correct
execution — validation, schema enforcement, transactional writes,
side-effect coupling, cross-reference consistency, computed
properties (hashes, indexes), migrations — live in **MCP gates**
(backend code, exposed as MCP tools). Skills are for judgment,
conversation, and surfacing decisions; they orchestrate MCP tool
calls, never reimplement what those tools do.

(Renamed from "execution locality" in v0.4. Locality suggests
*physical location*; the actual axis is determinism — single-right-
answer vs. judgment.)

**The persistence-layer boundary.** Cleanest line: *anything that
touches durable state with a **typed contract** (Pydantic model +
loader + cross-reference invariants) goes through MCP; session-
ephemeral state and loose unstructured files stay skill-direct.*
Watch list, in-conversation findings, surfacings queued during a
turn — all skill (ephemeral). Writes to office-config, baustein
YAML, manifests, schema-bearing state files — all MCP (the loader
owns the shape; bypassing MCP bypasses forward-migration and
invariants).

**The line is contract enforcement, not file type.** A file is in
scope of MCP if a Pydantic model + loader owns its shape. If the
file is parsed only by the LLM at read time, direct
`Read`/`Write` is fine. HANDOFF.md, prose memory `.md` files
under `memory/universal/`, top-level docs, READMEs — all
skill-direct, no schema, no migration, no transactional risk. A
markdown file *can* become schema-bearing later (e.g., `state.md`
once typed parsing lands) — at which point its access path
moves to MCP. Audit slice 14 reads each access via this test,
not by extension.

**Deterministic vs interpretive verdicts.** Validation with a
single right answer (frontmatter shape, ISO state code, schema
conformance, citation drift on exact-string match) is deterministic
→ MCP. Validation requiring interpretation (does this baustein
content actually concern §44 BNatSchG? does this language read as
collegiate or formal?) is interpretive → skill, surfaces verdict
to user. When unclear, ask: would two implementations agree byte-
for-byte on the verdict? If yes, MCP. If no, skill.

**Enumeration-vs-selection corollary.** "List the candidates" is
deterministic, scope-aware → MCP (`list_bausteine`,
`list_reference_manifests`). "Pick the right one for this drafting
context" is judgment → skill.

**Reuse direction.** When two consumers share logic, where does the
shared code live? The rule has a positive form, not just the
negative "skills compose, never reimplement":

- **Shared deterministic logic → MCP tool.** Two skills that need
  to dedupe, validate frontmatter, or look up a manifest entry call
  the *same* MCP tool. Don't reimplement; don't copy-paste prompt
  text describing the deterministic procedure into each consumer.
- **Shared interpretive logic → Skill Bundle reference.** Two skills
  that need to reason about korrektur-rules, layered review
  mechanics, or doctype conventions load the *same*
  `references/<topic>.md` file. The Skill Bundle convention exists
  for exactly this — judgment scaffolding shared across skill-side
  consumers without each skill re-stating it.

The negative form ("don't reimplement") tells you what's wrong; the
reuse direction tells you where the right home is. Audit slice 14
flags both directions: re-implemented determinism in skills *and*
re-implemented interpretive scaffolding when a Skill Bundle
reference would have served.

**Skill frontmatter declares MCP-tool dependencies.** Every skill's
`SKILL.md` frontmatter declares which MCP tools it relies on
(`mcp_tools_required[]`, `mcp_tools_optional[]`,
`fallback_when_mcp_absent`). See `docs/plugin-conventions.md` §1
for the full contract. Tools are referenced by snake_case name —
matches the Python function name in `pbs_core/`. Frontmatter is
machine-checkable; future audit slices verify every declared tool
exists in the MCP server's registry.

**Static path-based access control belongs in `settings.json`,
not in code.** Where a path should never be written outside a
specific MCP tool's context, use a permission deny rule. Cheaper
than scaffolding code paths that re-enforce what the harness can
already block.

**Strict-validation discipline.** Every MCP gate that owns a
typed contract validates via Pydantic. Required fields are
strictly required (no `Optional` for required, no silent default
to `None`). On contract violation, raise loud with descriptive
errors naming the offending field; never return partial data,
never coerce a missing required field to a placeholder. Defaults
are reserved for fields where missing semantically means
"not-yet-known" (`None`) — not for required fields where missing
would mean "broken data."

This discipline is what makes the gate a gate. A Pydantic model
that liberally uses `Optional` to "be flexible" silently accepts
malformed data and breaks the contract-enforcement guarantee.

Audit slice 16 (validation-gate coverage) checks adherence: it
walks every MCP tool's input/output models + every entity
Pydantic model and flags `Optional` on fields the rule says are
required, silent defaults that mask missing data, and exception
swallowing that converts contract violations to soft failures.

**Fail-closed for contract-bearing reads.** When MCP is
unreachable, skills MUST surface to the user and stop, never
bypass the contract via direct filesystem `Read`. The gate is the
only correctness path; bypass produces silent invalid output that
violates the strict-validation principle just established.

The rule applies symmetrically to writes (already covered by
"persistence-layer boundary" above) and reads. A skill that
"falls back to direct Read of state.md when MCP is down" gets:

- pre-migration frontmatter the loader would have updated
- partial-invalid state the Pydantic model would have rejected
- cross-reference-broken state (lifecycle ↔ phase mismatch) the
  invariant check would have caught

The right MCP-unreachable behavior for a contract-bearing read is
a clean failure surfacing: "MCP unreachable; cannot operate on
\<X\>. Restart backend." Contract-free prose (HANDOFF.md, prose
memory, decisions.md, file-map.md, READMEs, top-level docs)
remains skill-direct — no contract exists to bypass.

The test for "contract-bearing": Pydantic model owns its shape, OR
`schema_version` with migrations applied on read, OR cross-
reference invariants, OR a loader function in `pbs_mcp/`
constructs a typed object, OR `last_updated` / `last_fetched` /
`checksum_sha256` declares an invalidation contract. If any
yes → fail closed. Otherwise → direct Read fine.

Per-skill: `fallback_when_mcp_absent` strings declare what is
still possible; for contract-bearing dependencies the answer is
"nothing — surface and stop." Audit slice 14 scans these strings
and flags any "fall back to filesystem Read of \<contract-bearing
file\>" pattern as a declared future violation.

See `docs/decisions/mcp-fallback-policy.md` for the full
rationale and rollout.

### Backend organization (consequence of meta-rule 4)

Backend code splits conceptually into two layers:

- **`pbs_core/`** (planned package; currently part of `pbs_mcp/`):
  plain Python — config schema, validation, layered manifest API,
  integration adapters, RAG pipeline, project lifecycle, audit
  trail. Takes Python args, returns Python objects, raises Python
  exceptions. Knows nothing about MCP.
- **`pbs_mcp/tools/`**: thin MCP tool definitions that wrap
  `pbs_core` functions — parse JSON args, call core, format
  response, translate exceptions to MCP errors. Contains no
  business logic.

This is the consumer-side of the meta-rule: meta-rule 4 says
"deterministic logic in MCP gates"; this organization adds "MCP
gates are themselves thin wrappers around plain Python core."

This discipline applies starting now even though the two layers
live in the same module today. When the first non-MCP frontend
emerges (web UI is the load-bearing trigger per ROADMAP), the
physical split — promoting `pbs_core` to its own package — is a
small refactor, not a re-architecture.

**Don't do the physical split until a real second consumer exists.**
The conceptual discipline gives most of the maintainability +
testability benefit at near-zero cost.

---

# Layering convention: scope orthogonality (universal × domain × state × department)

(Demoted from meta-rule in v0.5 per design-review. It's a
*layering pattern* applied to specific entity types, not a placement
axis itself — it doesn't answer "where does this go?", it answers
"once you know it's the kind of thing that layers, which subdirectory?". Extended in v0.11 with the department axis per #12.)

Reference content, doctype registries, skeletons, bausteine, and
department-specific configuration all decompose along **four**
orthogonal axes:

- **universal** — applies to every German Planungsbüro deploying
  this app, regardless of planning domain or Bundesland.
- **domain** — applies to bureaus working in a specific planning
  domain (e.g. PV-FFA, Wind, Naturschutz, Innenentwicklung).
  Multiple domains can be active simultaneously.
- **state** — applies to bureaus working in a specific Bundesland
  (BB, BW, BY, ..., TH). Multiple states can be active simultaneously.
- **department** *(added v0.11 per #12)* — applies to a specific
  capability area within an office (planning, project-management,
  invoicing, brand-voice, legal-work, etc.). Opt-in per entry —
  most existing entries stay in the original 3 axes; department-
  specific entries declare the 4th. Multiple departments can be
  active simultaneously per office.

A bureau's effective content is its `(domains × states × departments)`
selection (set in `office-config.yaml > scope.{domains,states}` and
`departments.<name>`). Layered loaders merge the universal layer
with each selected domain/state/department layer at runtime.

**Where this applies:**

- **References manifests**: `extensions/{universal,domain/<X>,state/<X>,department/<X>}/references-manifest.yaml`
- **Doctype manifests**: `extensions/{universal,domain/<X>,state/<X>,department/<X>}/doctypes.yaml`
- **Skeletons**: `plugin/templates/skeletons/{universal,domain/<X>}/<doctype>/`
- **Bausteine**: `memory/bausteine/{universal,domain/<X>,state/<X>,department/<X>}/<name>.md`
- **Office-style overlays**: `plugin/templates/office-style/office-style.{default,<DOMAIN>}.sty`
- **Department config** *(added v0.11)*: `extensions/department/<X>/department.yaml` (event_subscriptions + per-department metadata; spec'd in `office-vs-department.md`, implementation deferred to #11)

**Hard rules for placing layered content:**

- Decide the scope BEFORE the path. Ask: does this apply to every
  German bureau (universal), every bureau in this domain (domain),
  every bureau in this state (state), or only this department
  (department)?
- A baustein has exactly one scope. If a candidate baustein applies
  to multiple, either promote it up the layer (`universal` if truly
  cross-domain-cross-department) or split it.
- An entry's home is independent of who created it.
- Most universal/domain/state content is department-agnostic — it
  applies across departments. Only declare a `department/<X>` cell
  when content is genuinely department-specific (invoicing-billing-
  templates, PM-deadline-conventions).

**Out of scope (entity types this convention doesn't apply to):**
Skill Bundles, Backend, External Data — none of these layer along
the scope axes. Configuration partially applies (its manifest tree
under `extensions/` does; the office-config file itself doesn't).
Skills declare `department:` in frontmatter (per #12) but skill
*bundles* themselves don't layer along the 4 axes — they're
discovered by their bundle path, not via layered loader merge.

**The `author-manifest` skill** scaffolds new domain, state, or
department manifests for scopes that don't yet have content.

---

# The five entity types

| Type | Where | Invalidation | What it does |
|---|---|---|---|
| **Skill Bundle** | `plugin/skills/<name>/SKILL.md` + `references/*.md` | semver `version:`; reload via `/reload-plugins` | Behavioral protocol auto-loaded on trigger match. SKILL.md is the entry point; references hold detailed format specs / checklists / procedures. (Combines former Type A skill + Type B skill reference — they're chapters of one bundle, not peers.) |
| **Memory** | `memory/universal/...` (prose), `memory/bausteine/{universal,domain/<X>,state/<X>}/...` + `<project>/_ai/...` (records) | references_used/status/review_due/verified_against_version | Two sub-kinds: **authored prose** (universal domain knowledge consumed across skills — style-spec, korrektur-rules, verfahren docs) + **generated records** (bausteine, feedback entries, project state.md). Mutability differs sharply between them; both share Memory's invalidation hooks. |
| **Backend** | `backend/mcp-server/...` (code + protocols + adapters + technical docs) | none declarative; restart MCP server after changes | Python implementation. Splits conceptually into `pbs_core/` (plain Python) + `pbs_mcp/tools/` (MCP wrappers) per meta-rule 4. Integration adapters live as a sub-organization here (`pbs_mcp/integrations/<class>/<adapter>.py`); they're an internal pattern, not a peer entity type. |
| **Configuration** | `office-config.yaml` (single per deployment, outside repo) + `extensions/{universal,domain/<X>,state/<X>}/{references,doctypes}-manifest.yaml` (scope-keyed, in repo) | `schema_version` + migration framework | Deployment-controlled YAML. Two sub-kinds — single-file (office-config) and scope-keyed (layered manifests) — distinguished by where they live + how they're discovered, but both are configuration-shaped (versioned, schema-validated, deployment-scoped). |
| **External data** | Resolved via `roots.*` (projects, references, state) + per-project `<project>/_ai/...` | Varies; project state via `_ai/state.md.lifecycle`; references corpus via `<roots.references>/changelog.md` | Real user data: legal texts, project artifacts, runtime state, correspondence. NOT versioned with the app. |

**Why 5 not 9** (per design-review session 5):
- **Skill Bundle** = former A (Skill) + B (Skill reference). A skill reference has no meaning outside its parent skill — it's a chapter of the bundle, not a peer. Decision rules collapse from "is this a skill or a skill-reference?" to "is it part of a skill bundle?"
- **Configuration** = former G (Office config) + H (Layered manifests). Both are deployment-controlled YAML; the only difference is single-file vs scope-keyed, which is *where* they live, not *what kind of thing* they are.
- **Backend** = former E (Backend code) + I (Integration adapters). Adapters are a backend-internal organizing pattern (same language, same package, same restart semantics) — not a peer entity type.
- **Drop A-I letters**: false ordinality + false peerage. Names ("Skill Bundle", "Memory", "Backend") are self-documenting.

(For migration: any prior reference to "Type A" / "Type B" / "Type C" / etc. should be re-read as the corresponding new name. Most references to the old letters can be dropped without replacement; the new names speak for themselves in context.)

---

# The three decision rules

For any new piece of content, walk these in order. The first to
classify wins.

## Rule 1 — Is this consumed by Claude at runtime as behavior?

If it tells the AI HOW to act, what to load, how to converse, when
to delegate — it's part of a Skill Bundle.

→ **Skill Bundle**: `plugin/skills/<name>/SKILL.md` (entry point,
with frontmatter) + optional `references/*.md` (detailed protocols,
format specs, checklists — no frontmatter).

If multiple skills consume the same content (e.g. korrektur-rules,
style-spec, verfahren-phasen), it's *cross-cutting authored prose*
— route to Rule 3 (Memory: prose).

## Rule 2 — Is this Python code?

If it's `.py` — backend code, MCP tool wrappers, integration
adapters, technical schema docs.

→ **Backend**: `backend/mcp-server/...`. Adapters are a sub-pattern
(same package), not a separate type.

## Rule 3 — Then by mutability:

**3a. Authored prose** (humans/AI write; cross-cutting knowledge):

- Universal domain knowledge → `memory/universal/...` →
  **Memory (prose)**.
- Layered (universal × domain × state) reference manifests +
  doctype registries → `extensions/<scope>/<key>/*.yaml` →
  **Configuration (scope-keyed manifest)**.
- Per-deployment values (paths, identity, actors, scope) →
  `office-config.yaml` (outside repo) → **Configuration (office-config)**.

**3b. Generated records** (tools write; instance state):

- Bausteine, feedback entries, project state — `memory/bausteine/<scope>/<key>/<name>.md` or `<project>/_ai/...` → **Memory (record)**.

**3c. External data** (user files, not versioned with app):

- Legal text corpus, client project artifacts, runtime state →
  `<roots.*>` paths, per-project `_ai/...` → **External data**.

## How the rules compose

Rule 1 catches everything Claude reads as instruction. Rule 2
catches everything written in Python. Rule 3 splits the rest by
who-writes-it (authored vs generated vs external).

The 4-mutability breakdown in Rule 3 is *one rule with sub-cases*,
not 4 separate rules. The decision is "what kind of content is
this?" (prose / record / config / external), not a sequential walk.

(This collapses the v0.4 6-rule walk to 3 rules + sub-cases. The
former Rules 4 and 5 — "HOW vs WHAT" — were a false axis: every
cross-cutting memory doc has *both* HOW and WHAT properties; the
real distinction is consumer breadth, which Rule 1's "multiple
skills" branch handles directly.)

---

# Worked examples

| Content | Reasoning | Type |
|---|---|---|
| `style-spec.md` (universal B-Plan LaTeX domain) | Rule 1: cross-cutting (multiple skills); Rule 3a: authored universal prose. | Memory (prose) |
| `korrektur-rules.md` (German writing conventions) | Same — cross-cutting prose; Rule 3a. | Memory (prose) |
| `bauleitplanung-phasen.md` (BauGB process) | Rule 3a: authored universal prose, cross-cutting. | Memory (prose) |
| `extensions/universal/doctypes.yaml` | Rule 3a: scope-keyed manifest. | Configuration (manifest) |
| `extensions/domain/Naturschutz/doctypes.yaml` | Same; scope=domain/Naturschutz. | Configuration (manifest) |
| `office-config.yaml` (outside repo) | Rule 3a: per-deployment configuration. | Configuration (office-config) |
| `baustein-format.md` (how to write a baustein) | Rule 1: instruction; consumed by ONE skill (save-baustein). Part of skill bundle. | Skill Bundle (reference) |
| `state-format.md` | Rule 1: instruction; single-skill (orchestrator). | Skill Bundle (reference) |
| `manifest-schema.md` | Rule 1: single-skill (research-references). | Skill Bundle (reference) |
| Doctype checklists | Rule 1: single-skill (validate-checklist). | Skill Bundle (reference) |
| `vector-metadata-schema.md` | Rule 2: backend technical schema. | Backend |
| A future saved baustein | Rule 3b: generated record. Apply layering convention to pick scope. | Memory (record) |
| A future feedback entry | Rule 3b: generated record. | Memory (record) |
| A future `<project>/_ai/state.md` | Rule 3b: generated record. | Memory (record) |
| `orchestrator` SKILL.md | Rule 1: skill bundle entry point. | Skill Bundle |
| `save-baustein` SKILL.md declares `mcp_tools_required: [save_baustein, list_bausteine]` | Meta-rule 4: skill is the orchestrator; MCP tool is the validator. Frontmatter makes the dependency explicit. | Skill Bundle |
| Email integration adapter Python | Rule 2: backend Python. (Sub-pattern: integration adapter.) | Backend |
| Court ruling text from BVerwG website | External data; lives in RAG corpus at `<roots.references>/urteile/...`. | External data |
| `references_used: []` frontmatter | Meta-rule 3 invalidation hook. | (per containing entity type) |

---

# Designed extensions, not yet implemented

These ROADMAP items will extend or modify the architecture when
implemented. Recorded here so future sessions don't re-discover
them. Full design lives in `ROADMAP.md`.

> **RAG-related items** (multimodal ingest, structural retrieval,
> query rewriting, agentic retrieval, late-interaction text
> retrieval) are resolved (ACCEPTED in session 5 post-audit) in
> `docs/rag-pipeline-decisions.md`. The bullets below list the
> ROADMAP framings; that doc carries the verdicts + alternatives
> + revisit triggers.

- **Audit trail** — unified change/decision/version log across
  artifacts, references, manifests, configs, integrations,
  bausteine, plans, correspondence. Today scattered (`decisions.md`,
  `snapshots/`, `changelog.md`, manifest archives, git). Will
  formalize as a Memory (record) sub-kind or a new
  Configuration-style log. Per meta-rule 3, every entity already
  declares invalidation; this extension unifies the log.
- **Human-readable artifact generation at checkpoints** — every
  meaningful checkpoint (send-gate, phase transition, draft-invoice,
  baustein-promotion, config-change) produces a PDF/HTML alongside
  machine state.
- **Integration registry** — discovery API over callables (skills,
  MCP tools, adapters) with capability metadata. Skills already
  carry `capabilities[]`-equivalent in their `phase_role` +
  `handoffs[]` frontmatter (post-design-review session 5);
  registry will federate that with backend tool registration.
- **Web UI for collaborative review** — Coolify-hosted; review-
  platform integration adapter class. First non-MCP frontend —
  triggers the `pbs_core/pbs_mcp` physical split.
- **PM + invoicing** — per-project `_ai/billing.md` ledger;
  `log-time` + `draft-invoice` skills; uses accounting integration
  adapter.
- **Multimodal RAG ingest pipeline** — page-image retrieval
  (ColPali), table extraction, OCR, DRM removal. Architecture
  decided: local pre-processing + embedding + matching; reading +
  reasoning happens via the in-loop Claude session.
- **Structural retrieval** — legal §-graph + project-cross-project
  graph + verfahren state-machine. SQLite alongside LanceDB.
- **Query rewriting** (HyDE, decomposition, expansion) +
  **agentic retrieval** (per-claim search) + **late-interaction
  text retrieval** (ColBERT-v2, conditional) — all retrieval-
  pattern improvements.
- **Per-domain memory directories** (`memory/domain/<X>/`) —
  introduce when first domain-scoped reference content lands.
  Mirror of references / doctypes layering.
