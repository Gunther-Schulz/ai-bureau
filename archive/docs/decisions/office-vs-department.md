# Decision record: office-vs-department modularization

> ## ⚠ NAMING SUPERSEDED session 13 per #22 (`docs/decisions/terminology-and-specialist-primitive.md`)
>
> This DR's **structural decisions** (office contains N departments;
> cross-department coordination via events; skills singleton-department;
> per-department phase/lifecycle on ProjectState; memory taxonomy 4th axis;
> all 7 question resolutions; defers D1-D3) **REMAIN VALID** with renamed
> primitives:
>
> | Old (this DR) | New (Sub-DR A) |
> |---|---|
> | Office | Workspace |
> | Department | Specialist (pattern primitive) + Department (deployment-instance optional grouping) |
> | `extensions/department/<dept>/department.md` | `extensions/specialists/<id>/specialist.md` |
> | `office-config.yaml` | `workspace.md` (also adopts hybrid-shape per #16) |
> | Skill `department:` frontmatter | Skill `specialist:` frontmatter |
> | `departments_active: list[str]` | `specialists_active: list[str]` |
> | `OfficeEntity` / `DepartmentEntity` | `WorkspaceEntity` / `SpecialistEntity` |
>
> **Use `terminology-and-specialist-primitive.md` (Sub-DR A) for current
> primitive vocabulary.** This DR retained as historical record of the
> structural reasoning (questions Q1-Q7; downstream constraints; defers).

**Status**: ACCEPTED (session 9, 2026-04-29); **NAMING SUPERSEDED session 13 per #22 Sub-DR A**
**Owner**: per-session HANDOFF; ARCHITECTURE.md "Workspace-vs-specialist distinction" section (renamed v0.31); ROADMAP commitment #12 (shipped) + #22 (shipped)
**Related**: ROADMAP commitment #11 (Cowork integration — slash command namespacing depends on this), #14 (Memory Bank — uses 4th memory axis), #6 (audit-trail v2 retrofit — actor_kind + specialist-aware), #9 (Pattern-vs-instance split — handles per-specialist phase/lifecycle on ProjectState), `a2a-and-gemini-pattern-emulation.md` Row 4 (cross-specialist coordination must be event-shaped), `terminology-and-specialist-primitive.md` (Sub-DR A — supersedes naming)

## Context

Per ARCHITECTURE.md v0.9 "Office-vs-department distinction (open architectural question)": PBS today **conflates "office" with "single department."** We have one department (planning-document-work) wrapped in office-level scaffolding (setup-office, orchestrator, projects-index, references-manifest, audit trail, file-map, office-config). Real Schulz Planungsbüro eventually wants three departments: planning + project-management + invoicing. Other PBS-shaped offices (legal, research, medical) have analogous shapes.

This decision record resolves the open question. The architectural distinction:

- **Office** = container for N departments + office-level infrastructure. Provides the coordination substrate; doesn't do domain work itself. Office-level: setup, projects-index, references corpus, audit trail, identity, actors, user/auth, file-map.
- **Department** = single capability area with its own skills, doctypes, workflow phases, memory taxonomy, external authorities. Examples: planning-document-work (current PBS), project-management, invoicing, legal-work, clinical-care, grant-management, brand-voice.

The pattern generalizes. Every "AI office" has office-level scaffolding + 0..N departments + cross-department coordination via shared lifecycle events. Single-department offices (Anthropic's brand-voice partner-built plugin) and zero-department offices (single-skill utilities) are valid edge cases.

## Decisions

### Skill classification

Every skill declares a `department:` frontmatter field. **Required, no silent default** (matches `actor_kind` strict-validation discipline from #10).

| Skill | `department:` |
|---|---|
| `setup-office` | office |
| `orchestrator` | office |
| `survey-project` | office |
| `author-manifest` | office |
| `research-references` | office |
| `watch-list` | office |
| `validate-bausteine` | office |
| `integrate-department` (new) | office |
| `draft-textteil-b` | planning |
| `draft-textteil-c` | planning |
| `draft-cover-mail` | planning |
| `validate-checklist` | planning |
| `review-draft` | planning |
| `validate-latex-style` | planning |
| `verify-citations` | planning |
| `save-baustein` | office (department-agnostic; takes `department:` arg from caller) |
| `record-feedback` | office (same) |
| `promote-to-skill` | office (same) |

### Memory taxonomy: 4th orthogonal axis

`(universal × domain × state × department)`. Opt-in per memory entry — most existing entries stay in 3-axis cells; department-specific entries declare the 4th axis. `extensions/department/<dept>/{references-manifest,doctypes-manifest,...}.yaml` for department-axis content.

Universal-cross-department entries (style-spec, korrektur-rules, bauleitplanung-phasen) stay at 3-axis layer — apply across all departments. Department-specific entries (invoicing-billing-templates, PM-deadline-conventions) live in the 4th-axis cell.

### Office-config schema additions

```yaml
departments:
  planning:
    scope:
      domains: [pv-ffa, naturschutz]
      states: [BB]
  pm:
    enabled: false
    integration:
      time_tracking_class: timesheet-app
      deadline_calendar_class: caldav
  invoicing:
    enabled: false
    integration:
      accounting_class: lexware
    pricing:
      default_hourly_rate: 95
```

**Section presence implies enabled.** Optional `enabled: false` only for "configured but paused" cases. No required `enabled` field.

Schema bump (CURRENT_SCHEMA_VERSION + migration) implemented as part of **commitment #11** (Cowork integration touches office-config heavily — `pbs.local.md` migration is the right home).

### Cross-department coordination: AuditEvent + extended watch-list

Per Row 4 of #10: event-shaped, not call-shaped. **Reuses existing AuditEvent infrastructure**; no new typed-event mechanism (subsumption check per session-7 target 9: don't add alongside what exists).

Each department declares `event_subscriptions: [<event_kind>, ...]` in `extensions/department/<dept>/department.yaml` (new file format; spec'd here, implemented in #11):

```yaml
# extensions/department/planning/department.yaml
event_subscriptions: [phase_transition, send, decision]

# extensions/department/pm/department.yaml
event_subscriptions: [phase_transition, lifecycle_transition, send]

# extensions/department/invoicing/department.yaml
event_subscriptions: [send, lifecycle_transition]
```

At session start, orchestrator queries recent audit events, filters by enabled departments × their subscriptions × `actor_card NOT IN self_dept_skills` (self-emitted events excluded). Surfaces relevant ones to user via existing watch-list mechanism.

User decides which department's skill should respond (or none). Cross-department signal example:

> "FYI: planning sent Begründung to UNB on 2026-04-29 (audit event abc-123). PM department: should we log this billable phase transition? Invoicing: ready to draft milestone invoice?"

### Memory tooling skills are department-agnostic

`save_baustein`, `record_feedback`, `promote_to_skill` — all `department: office` skills that take an explicit `department:` argument at call time. Calling skill's body literally does:

```python
save_baustein(name="...", department="planning", ...)
```

Source of truth: the calling skill's frontmatter `department:` field. Body hardcodes the matching value. Audit slice can verify body's `department=` calls match the skill's frontmatter.

Rejected: MCP-side frontmatter introspection (invasive, breaks skill↔MCP boundary); runtime "current department" state (ambiguous in cross-department flows).

### Office-level skills' `department:` arg = runtime context

When an office-level skill (orchestrator, watch-list, etc.) calls a department-aware MCP tool (`save_baustein`, etc.), it passes `department:` based on **current orchestration context** — typically derived from `ProjectState.departments_active` + which department's workflow is currently routed. Defaults to `"office"` when no department context applies (e.g., office-wide configuration changes).

### Skills are singleton-department

A skill belongs to **exactly one** department (or `office`). Multi-department coordination happens via **office-level orchestrating skills** that consume from multiple departments. Rejected: `departments: [planning, pm]` array (breaks routing, complicates the mental model).

Office-level orchestrators are the answer for cross-department flows.

### Offices have 0..N departments

- **Zero-department office**: single-skill utility (brand-voice equivalent). All skills are `department: office`. No slash-command namespacing.
- **Single-department office**: PBS today. Less ceremony — all department skills share one slug; cross-department coordination not used.
- **Multi-department office**: full apparatus — namespacing, subscriptions, integrate-department onboarding flow.

### `research-references` placement: office-level skill, manifest gains department axis

Skill stays at `department: office` (corpus-management infrastructure is shared). Manifest content is **layered along the 4th axis**: `extensions/department/<dept>/references-manifest.yaml` for department-specific corpus subsets (planning uses BauGB/BNatSchG; invoicing might use UStG/EStG; PM might use HOAI/AHO).

### `search_corpus` gets optional `department_filter:` arg

Defaults to **calling-skill's department**. Override possible (broaden / cross-department search). Today's full-merge across (universal × domain × state) extends to filter by department at query time. Planning skills don't surface invoicing-relevant tax-law references; invoicing skills don't surface BauGB.

Implementation deferred to **Phase 1 corpus work** (per Row 8 of #10 — retrieval interface design lands there).

### `query_audit_trail` gets optional `department:` filter

Backend maintains a **cached skill→department registry**, refreshed on `/reload-plugins`. Filter resolves to "events whose `actor_card ∈ skills_in_dept`."

Implementation deferred to **commitment #6** (audit-trail v2 retrofit — natural home; same time as `actor_kind` retrofits land).

### ProjectState gains `departments_active: list[str]`

Required for routing + audit-filter purposes. Empty default ("not-yet-known" semantic; zero departments have engaged with this project yet). Gate-mediated update: `record_audit_event` atomically updates `departments_active` when writing an event whose `actor_card ∈ skills_in_dept`. Same pattern as `record_decision`'s atomic dual-write.

**Schema addition shipped this commitment** (analogous to #10's AuditEvent.actor_kind addition). Gate-side update logic deferred to **commitment #6**.

### Setup integration: separate `integrate-department` skill

`setup-office` handles office-level + the primary department (the user's main capability area). Adding more departments later → new skill `integrate-department <slug>`.

Reasons:
- Real flow: Schulz adds PM in 6 months, invoicing in 12. Each is its own onboarding event.
- Clean separation of concerns (office vs department are different concept levels).
- Pattern-level: any office adopting a new department uses the same skill.

Skill scaffolding (SKILL.md + PROCEDURE.md) implemented as part of **commitment #11** (when slash-command namespacing + skill-frontmatter sweep is done).

### Department-managed entities + delivery modes (session-9 followup)

**The deeper realization** (post-#12 first pass): each department defines its own entity types — completely. Planning's primary entity = Project; PM's = Timesheet/BillingPeriod; Invoicing's = Invoice/PaymentReceipt; legal-work's = Matter/Brief; brand-voice's = Asset/BrandGuideline. **There is no universal entity-type core.** Pattern-vs-instance check: each entity is fundamentally department-instance, not "extension of a universal entity."

This refinement also surfaces a real-world constraint: companies have existing infrastructure (Lexware for invoicing, Harvest/MOCO for time tracking, BambooHR for employees). PBS doesn't replace those tools; **PBS coordinates around them via integration adapters**. So entity ownership splits into two delivery modes.

**Terminology**: a **department-managed entity** (or just "managed entity" in context) is a domain object the department is responsible for, delivered in one of two modes.

| Term | Meaning |
|---|---|
| **Managed entity** | A domain object a department manages (Project, Invoice, Asset, Matter, Timesheet) |
| **Native delivery mode** | PBS owns system-of-record. Pydantic schema + native MCP tools + LanceDB/file persistence. Used when no mature external alternative exists OR for memory-shaped data (conventions, rules, preferences). |
| **Adapter delivery mode** | External system owns system-of-record. PBS reads/writes via integration adapter (Pydantic Protocol + concrete adapter). Used when companies have existing tools. Generalizes meta-rule 1's existing integration-adapter pattern (auxiliary integrations: email, calendar) to primary department system-of-record. |

**Mixed-mode is required, per-entity not per-department.** A single department typically mixes:
- Invoicing department: Invoice → adapter (Lexware); BillingRule → native (per-client conventions, memory-shaped); PaymentReceipt → adapter (paired with Invoice).
- PM department: Timesheet → adapter (Harvest/MOCO); Project deadlines → native (planning conventions live in PBS); BillableMilestone → adapter (paired with Timesheet).
- Planning department (PBS today): Project → native (no external "B-Plan management tool" exists — PBS IS the system of record).

**Where the boundary falls** (light + flexible, not heavy):
- PBS owns **the contract for department modules** + native-mode entity infrastructure
- PBS owns **entity types only for departments where it IS the natural system of record** (planning Project, brand-voice Asset, research Manuscript — domains without mature off-the-shelf alternatives)
- PBS **delegates to external systems via adapters** for entities where mature tools exist (PM Timesheet, Invoicing Invoice, HR Employee)
- **Architecture supports both modes** with a uniform contract (audit, memory, cross-department coordination work the same regardless of mode)

#### Setup flow (`integrate-department <slug>`)

The skill walks user through entities + asks mode per entity. The department module declares its managed entities (with descriptions + recommended-default modes); user picks per entity.

```
> Integrating invoicing department (PBS-bureau invoicing module v1.0).

  This department manages 3 entities:

  Invoice — issued invoices to clients
  Mode? [a]dapter / [n]ative (default: a — recommended for ≥5 invoices/month)
  > a
  Adapter: [1] lexware  [2] fastbill  [3] sevdesk  [4] custom
  > 1
  Configuring lexware adapter (tenant ID, API key)…

  BillingRule — per-client billing conventions
  Mode? [a]dapter / [n]ative (default: n — convention-shaped, memory-friendly)
  > n
  Native schema registered.

  PaymentReceipt — incoming payment tracking
  Mode? [a]dapter / [n]ative (default: a — pairs with Invoice adapter)
  > a
  Auto-configured: lexware (matches Invoice adapter you set up above).

> Invoicing department integrated. 3 entities configured.
```

#### Schema additions (spec'd here, implemented in #11)

**1. `extensions/department/<dept>/department.yaml`** gains `managed_entities:` section:

```yaml
event_subscriptions: [send, lifecycle_transition]
managed_entities:
  invoice:
    description: "issued invoices to clients"
    default_mode: adapter
    adapter_protocol: invoice-system
  billing_rule:
    description: "per-client billing conventions"
    default_mode: native
    native_schema: BillingRule
  payment_receipt:
    description: "incoming payment tracking"
    default_mode: adapter
    adapter_protocol: payment-system
    pairs_with: invoice
```

**2. Office-config** records per-deployment choices:

```yaml
departments:
  invoicing:
    entities:
      invoice:
        mode: adapter
        adapter: lexware
        config: {tenant_id_ref: <env-var>, api_key_ref: <secret>}
      billing_rule:
        mode: native
      payment_receipt:
        mode: adapter
        adapter: lexware  # auto-paired
```

**3. Adapter Protocols** at `extensions/department/<dept>/adapters/<entity>/protocol.py` (Pydantic `Protocol`); concrete adapters at `<entity>/<adapter-name>.py`. **Same pattern as existing meta-rule 1 integration adapters** — generalizes the existing concept from auxiliary integrations to primary department system-of-record.

**4. Native-mode schemas** at `extensions/department/<dept>/entities/<entity>.py` (Pydantic), with matching MCP tools wrapping CRUD. Pattern same as today's ProjectState (which becomes planning department's `entities/project.py` post-#9 refactor).

#### Project (PBS bauleitplanung) is the canonical native managed entity

For clarity:

- **Project** = planning department's primary managed entity, **native delivery mode**
- **Schema location post-#9**: `extensions/department/planning/entities/project.py` (refactor — today the schema lives at `backend/mcp-server/src/pbs_mcp/project_state.py`)
- **No "abstract Project" at architecture layer** — there is no universal Project-shaped concept being extended. The planning-department-module's Project IS the bauleitplanung-shaped schema.
- **PBS-specific fields** (verfahren_type, bundesland, b_plan_nr, geltungsbereich_ha, etc.) are baked into the planning department's contribution. They're not "extensions of a universal Project."

**Per-company customization within a department-module's managed entities** is a separate layer (e.g., a specific bureau wants a custom field in Project for internal review tracking). Designed in **#9** with at least three options on the table:
- Pydantic subclass per deployment (heavy, type-safe)
- Office-config-declared `extra_fields: dict[str, type]` per entity (lighter, less type-safe)
- Free-form `metadata: dict` escape hatch on the base entity (loosest)

**Constraint passed to #9**: design and choose between these per-company customization mechanisms.

#### What this concept subsumes (target 9 subsumption check)

Per session-7 design-review target 9: when adding a new mechanism, ask what it subsumes.

- **Generalizes meta-rule 1 integration-adapter pattern**: previously scoped to auxiliary integrations (email, scanner, calendar); now also the implementation layer for adapter-mode managed entities. The Pydantic Protocol + concrete adapter contract is the same; the consumer set expands.
- **Reframes the original "ProjectState core/extension split"** from #9: instead of "extract universal core from PBS-specific extension," #9 now reframes as "recognize ProjectState as planning department's native managed entity; refactor location; design per-company customization mechanism."
- **Doctype-manifest generalization** (originally a separate #9 line item) fits naturally — each department contributes its own doctypes per its mode.

No new mechanisms left in legacy. Subsumption check passes.

#### Sub-entities — composable, but mostly via nesting

Real entities have sub-structure: Invoice has LineItems, Project has Tasks, Matter has Filings, Manuscript has Sections. Three patterns, with criteria for choosing:

| Pattern | When to use | Example |
|---|---|---|
| **Nested fields** (default) | Sub-entity has no independent operations; CRUD'd through parent | Invoice → LineItems (always together; Lexware exposes them as nested response fields) |
| **First-class with `parent_entity:`** | Sub-entity has independent operations, audit events, or different delivery mode than parent | Project → Tasks where Tasks live in Asana adapter while Project is native |
| **Hybrid (Protocol-internal)** | Adapter mode where external system handles sub-entity access internally; PBS doesn't model sub-entities at architecture layer | PM department → Timesheet's daily entries (Harvest API exposes them; PBS treats Timesheet as a single entity) |

**Criterion to elevate a sub-entity to first-class managed entity** (any one):
- Independent system-of-record / different delivery mode than parent
- Independent audit events meaningful (e.g., "task X completed by colleague Y" needs its own audit attribution)
- Independent CRUD operations needed (not just via-parent access)

If none apply: keep nested. The default is the parsimonious choice.

`department.yaml` schema gains optional `parent_entity:` + `cardinality:` fields when first-class:

```yaml
managed_entities:
  project:
    description: "B-Plan project"
    default_mode: native
  task:
    description: "task within a project"
    default_mode: adapter
    adapter_protocol: task-system
    parent_entity: project
    cardinality: many
```

#### When to elevate to managed entity (the three-test discipline)

Adding a managed entity is **heavy** (Pydantic schema, MCP tools, persistence layer, possibly an adapter contract). Adding event kinds or memory entries is **light** (a `Literal` value, audit-event details `dict`, or a memory record).

The risk if undisciplined: **the architecture creeps toward a relational SQL schema** — one entity per noun, foreign keys, joins, normalization rules. That's catastrophic for an LLM-mediated AI office: it makes the architecture brittle, slow to evolve, and re-implements enterprise software's worst tendency. AI offices should sit closer to **knowledge graph + document store with stable references**, not Oracle.

**Test (all three required to elevate to managed entity)**:
1. **Stable identity** — has an ID/slug that persists across sessions and is referenced by other things
2. **State of record** — has fields whose authoritative current value matters (not just historical)
3. **Lifecycle** — has phases or status that progress over time

If all three: managed entity. If any missing: prefer **event kinds + nested fields + memory entries**.

**Worked examples**:

| Concept | Identity | State | Lifecycle | Verdict |
|---|---|---|---|---|
| **Client** | yes (stable across years) | yes (contact info, billing terms, conflict flags) | yes (active/dormant/terminated) | ✅ managed entity |
| **Actor** (person) | yes (person identity persists) | yes (role, contact, email) | partial (joined/active/left) | ✅ managed entity |
| **Project** | yes | yes | yes | ✅ managed entity (planning) |
| **Invoice** | yes | yes | yes (drafted/sent/paid) | ✅ managed entity (invoicing) |
| **Approval** | no (each approval is one moment) | no (it's a fact, not state) | no (instantaneous) | ❌ **event kinds** (e.g., `approval_requested`, `approval_granted`, `approval_rejected` on AuditEvent) |
| **LineItem** (within Invoice) | only as part of Invoice | not independently | no | ❌ nested field |
| **Deadline** | no (date attached to something) | no | no | ❌ nested field on Project / Invoice |
| **Document version** | maybe (snapshots have IDs) | minimal | partial | ❌ events + snapshot bytes (already what audit trail does) |
| **Task** (within Project) | maybe (if independently tracked) | maybe | maybe | depends — first-class only if tracked independently |
| **BusinessCalendar** (work hours, holidays) | yes | yes | minimal | borderline; defer until concrete need |

**How "joins" are answered without foreign keys**:

| Question | SQL approach | PBS approach |
|---|---|---|
| "All invoices for client X" | `SELECT ... JOIN ...` | Adapter API: `lexware.invoices(client_id=X)`. Or audit-trail filter: `kind=invoice_issued AND details.client_id=X`. |
| "All projects with overdue deadlines" | `SELECT ... WHERE deadline < NOW()` | Native query on Project entity store filtered by `deadlines[].date < today`. |
| "Audit history of decisions made by colleague Y" | Multi-table join | Audit-trail filter: `actor=Y AND kind=decision`. |
| "Which bausteine cite §44 BNatSchG?" | Full-text + reference table | Memory query (per #14): `search_memory(query="§44 BNatSchG", kinds=["baustein"])`. |

Everything's a filtered query over a small set of stores: native entities, audit trail, memory, adapter APIs. **No join planner needed.**

**The principle, stated**:

> **Prefer events + nested fields + memory entries over new managed entity types. Elevate to first-class managed entity only when stable-identity + state-of-record + lifecycle all apply.**

This belongs as a discipline check at design time. Likely **target 11 of design-review** (and a future audit slice that scans for over-modeled entities). Captured here as binding architectural guidance for future commitments touching managed entities.

#### Approval flows are event-driven, not entity-shaped

Application of the three-test discipline. Real businesses have hierarchical approvals: "Invoice >€10K needs partner approval"; "B-Plan submission needs principal sign-off." Approval is a fact (it happened), not an entity (with state evolving over time). The thing being approved IS an entity (Invoice, Project-submission); the approval chain is in its event history.

**Implementation** (folded into #6 audit-trail v2 retrofit; NOT a separate commitment):

- New AuditEvent kinds: `approval_requested`, `approval_granted`, `approval_rejected`. Details payload includes `approving_actor`, `policy_rule` (which authorization rule triggered), `subject_entity_id` (what was approved).
- Authorization rules ("Invoice >€10K needs partner approval") live in **skill logic**, not entity schema. The skill drafting an Invoice checks the rule and emits `approval_requested` if needed; orchestrator surfaces to the human approver.
- Entity gains a queryable status via audit-trail filter: "this Invoice's most recent approval-event chain says: requested → granted by Anna at T."
- No new managed entity. No schema migration for approval state. Light, correct.

Folds into commitment #6 (audit-trail v2 retrofit) — that retrofit is already adding event kinds; approval kinds added there.

#### Broader review — companies as they actually work

Critical-eye pass against real-world business operations to check for systemic gaps. Each item run through the entity-elevation discipline + pattern-vs-instance check. **Net result: zero new commitment numbers.** All resolved via existing infrastructure, scope expansions of existing commitments, defer to concrete need, or out-of-scope per pattern-vs-instance.

| Concern | Disposition | Why |
|---|---|---|
| **Document versioning** | Already handled (audit trail send events + snapshots/ + `causes[]` chains for explicit supersession) | Snapshots are immutable bytes (no lifecycle); send events capture moment of creation (3-test fails for entity) |
| **Notifications / proactive nudges** | Fold into #13 multi-user scope: `notification-channel` adapter class + `notification_sent` audit event kind | Receiving system (email/Slack inbox) IS state-of-record; PBS handles trigger + delivery + log. No new entity. |
| **Role-based actors** | Already in #15 scope: `Actor.roles: list[str]` field (open-ended; auth integration in #13 maps roles to permissions) | Actor is the entity; roles are nested-fields data |
| **Reports / metrics / dashboards** | Defer post-RAG: generalize `render_audit_trail` to `render_report` when concrete need arises | Reports are projections (fail 3-test), not entities. UX concern, not architectural. |
| **Conflicts-of-interest tracking** | NOT pattern-level. Domain-specific to legal-practice department; AI-office-builder-generated legal offices contribute their own `Conflict` managed entity | PBS planning doesn't have this concept; pattern-vs-instance pushes to per-department |
| **Business calendar (Werktage-aware deadlines)** | Defer to concrete need: office-config field + helper function (~half-session) | Reference data with no lifecycle (fails 3-test); fits as config + library, not entity |
| **Knowledge depreciation beyond legal references** | Already handled by `review_due` on memory records (works for any record type, not just legal-citation drift) | Convention reminder for non-legal records to set `review_due` |

**The discipline pays off**: the 3-test correctly identified Notifications, Reports, and BusinessCalendar as NOT entities (despite each having entity-feeling intuition). Mapping to adapter / render-artifact / config keeps the architecture light. Conflict correctly pushed to per-department-per-domain.

**What this confirms**: the architecture as it stands captures common business workflows without major gaps. New business primitives (when they arise) should run through the 3-test before being elevated. Most will fail and resolve to event-kinds + nested fields + memory entries. The few that pass are genuinely entities.

#### Infrastructure-primitive review (session-9 followup #4)

Distinct from the broader app-concern review above: this pass stress-tests our **core infrastructure primitives** (skills, managed entities, audit events, memory, integration adapters, cross-department coordination) against expressibility of arbitrary business processes. **Two genuine architectural gaps surface**, both fold into existing commitments:

**Gap A — Proactive time-driven triggers**: today's event sources are reactive (audit events fire when skills emit) + interactive (user starts session). Missing: proactive (deadline fires when no session is active; Frist-X-days-before warning surfaces without anyone present). Concrete failure: "B-Plan deadline approaching → notify principal" can detect-when-asked but can't fire-when-due. **Folds into #13** (Tier 2 cloud deployment naturally hosts a scheduler). Server-side cron-like infrastructure fires "tick" audit events on a schedule; subscribers react via existing event-subscription primitive. No new primitive type — extends event sources from "skill-emitted only" to "skill-emitted + time-emitted." MCP tool sketch: `register_scheduled_trigger(condition, event_kind)`.

**Gap B — Adapter-emitted events** (external state changes): integration adapters today are request-response (PBS asks Lexware → Lexware answers). Missing: adapters surfacing changes (Lexware webhooks PBS when invoice paid; Harvest tells PBS when timesheet edited externally). Concrete failure: external action in adapter-mode system → PBS audit trail misses it until next reconciliation. **Folds into #9** (department module contract design — when generalizing the integration-adapter pattern). Adapter Protocol gains `subscribe_to_changes(callback)` OR `poll_for_changes() -> list[Event]`. External changes translate to native AuditEvents with `actor_kind=external_agent` per #10's existing design.

**Coverage after gap-fills** (9/9 process expressibility):

| Process need | Primitive |
|---|---|
| State | managed entities |
| Actions | skills + audit events |
| Rules | skill logic + event subscriptions |
| History | audit trail |
| Knowledge | memory |
| People | Actor entity (post-#15) |
| Time | deadlines (nested) + scheduler (Gap A — folded into #13) |
| External world | integration adapters + adapter-emitted events (Gap B — folded into #9) |
| Workflows / sequences | phases + lifecycle on entities |

**Smaller future-watch items (deferred with documented intent)**:
- Workflow-as-data (BPMN-style declarative state machines for high-compliance environments) — defer until first compliance-strict client demands.
- Centralized RBAC policy engine — defer; per-skill authorization fine for solo + small bureau.
- Team hierarchy (sub-department actor groupings) — defer; nested relationships under Department + Actor; first-class only when concrete need.
- Resource modeling for limited shared resources (rooms, equipment) — adapter pattern handles; no new primitive needed.

**Net assessment**: zero new commitment numbers from this pass. Architecture's core primitives are sufficient after the two folded gaps land in #13 + #9.

## Implementation scope (this commitment)

**Schema additions** (ship now):
- `project_state.py`: `ProjectState.departments_active: list[str] = Field(default_factory=list)` — additive, no migration needed (zero projects bound).

**Documentation** (ship now):
- `docs/decisions/office-vs-department.md` — this file.
- `ARCHITECTURE.md` v0.10 → v0.11: convert "open question" section to "resolved"; meta-rule 3 invalidation table for ProjectState; scope-orthogonality 4th axis; skill bundle convention.
- `ROADMAP.md` commitment #12 collapsed; downstream constraints noted on #6/#9/#11/#14.
- `HANDOFF.md` session 9 closing state.

**What's NOT in this commitment**:
- Skill frontmatter `department:` field sweep (→ #11; same retrofit pass as Cowork plugin shape conformance).
- Office-config `departments.<name>` schema bump + migration (→ #11; co-located with `pbs.local.md` migration).
- `extensions/department/<dept>/department.yaml` event_subscriptions file format implementation (→ #11; spec'd here).
- `integrate-department` skill creation (→ #11).
- `record_audit_event` gate-side `departments_active` update logic (→ #6; co-located with v2 retrofit).
- `query_audit_trail` `department:` filter + skill→department cache (→ #6).
- `search_corpus` `department_filter:` arg (→ Phase 1 corpus work).
- Memory tooling skills' `department:` arg threading (→ #6 + #11; depends on the broader retrofit).

## Constraints for downstream commitments

**For #6 (audit-trail v2 retrofit)**:
- Skill retrofits MUST set `actor_kind` (per #10) AND pass `department:` argument to memory tooling calls (per #12).
- `record_audit_event` gate-side: atomically update `ProjectState.departments_active` when event's `actor_card ∈ skills_in_dept`. Skill→department cache lookup.
- `query_audit_trail` gains optional `department:` filter; backend cached registry.

**For #9 (Pattern-vs-instance best-effort split — REFRAMED MISSION per session-9 followup)**:
- **Mission reframed** from "extract universal core from PBS-specific extension" to "**design the department module contract + managed-entity concept with two delivery modes**." The core/extension framing was wrong — there is no universal entity-type core; each department defines its own entity types completely (some native, some adapter-delegated).
- Define **department module contract**: how a department contributes skills + managed entities + workflow phases + memory + manifests + audit subscriptions to an office.
- Define **managed-entity concept** with two delivery modes (native + adapter), per-entity choice, mixed-mode within a department supported.
- Refactor `ProjectState` location: from `backend/mcp-server/src/pbs_mcp/project_state.py` to `extensions/department/planning/entities/project.py` (planning department's primary native managed entity).
- Per-department phase tracking (`phases: dict[str, str]`) and per-department lifecycle (`lifecycle: dict[str, Lifecycle]`) on ProjectState — today's single-valued fields are PBS-instance assumptions.
- **Project-as-long-running-entity is itself opt-in per department** — some departments (PM tracking via Timesheets-only-no-Project, single-skill utilities) don't have a Project-shaped entity. The pattern supports project-having and project-less departments uniformly via the managed-entity concept.
- **Per-company customization mechanism**: design how a specific deployment customizes a department-module's managed-entity schema. Three options on the table: Pydantic subclass per deployment, office-config-declared `extra_fields: dict[str, type]`, or free-form `metadata: dict` escape hatch. Choose with rationale.
- Doctype-manifest generalization: each department contributes its own doctypes; fits naturally into the managed-entity / department-module contract.
- Output: `pattern-vs-instance-split-rationale.md` documenting per-decision reasoning, including chosen per-company customization mechanism.

**For #11 (deep Cowork integration)**:
- All skills get `department:` frontmatter field added (REQUIRED, no default). Sweep covers all 19+ skills.
- Slash commands namespaced: `/<department-slug>:<skill-name>` → `/planning:draft-begruendung`, `/office:setup-office`, `/office:integrate-department`, etc.
- Office-config schema bump for `departments.<name>` sections + per-entity `entities.<entity>.{mode,adapter,config}` sub-sections; co-located with `pbs.local.md` migration.
- `extensions/department/<dept>/department.yaml` file format implementation (event_subscriptions + managed_entities declarations).
- `integrate-department` skill scaffolding (new skill bundle) — walks the per-entity-mode setup flow described above.

**For #14 (Memory Bank)**:
- `search_memory` interface accepts `department:` filter (defaults to calling-skill's department); same shape as `search_corpus`'s eventual `department_filter:`.
- LanceDB memory index schema includes department metadata for filter queries.

## Pattern-vs-instance check

Generalizes to:
- **Legal practice**: legal-work + matter-management + invoicing. Cross-department events: matter filed → log billable hours, prepare retainer invoice. ✓
- **Research lab**: research + grant-management + lab-operations. Cross-department events: grant deadline → finalize manuscript, schedule lab time. ✓
- **Clinical care**: clinical-work + intake + billing. Cross-department events: trial enrollment → schedule visits, generate insurance billing. ✓
- **Consulting**: domain-work + project-management + invoicing. Same pattern as PBS. ✓
- **Single-skill utility (brand-voice)**: zero departments, all skills `department: office`. Pattern degrades gracefully. ✓

**Limitation surfaced in refinement**: project-as-long-running-entity is PBS-instance, not pattern-universal. Some offices have analogues (matter, trial, grant, engagement, campaign); some genuinely don't (brand-voice). The pattern supports both project-having and project-less offices. Constraint passed to #9.

## Why pre-RAG (timing)

Per #10's "three multipliers" framing — same logic applies to #12:

1. **AI-office-builder (v2)**: PBS schemas are the pattern. The builder will scaffold them into every generated office. Department-aware office shape locked pre-RAG = every generated office is multi-department-ready by inheritance.
2. **Consulting business**: enterprise consulting clients almost certainly want multi-department offices (legal practice with N departments, hospital network with N units). Mid-engagement schema refactor = credibility hit.
3. **PBS itself**: Schulz's PM + invoicing departments will land mid-term. Pre-RAG schema-aware vs post-data-accumulation refactor = same cost asymmetry as #10.

Cost asymmetry: pre-RAG, with zero projects bound and `departments_active` defaulting to `[]`, the schema addition is a 1-line Pydantic field. Post-Phase-1 + post-first-bind: every existing state.md needs migration; every audit event needs department-awareness retrofit; every memory entry potentially re-categorized.

## Defers — re-examined session 15 under v0.33 no-defer principle

> **Session 15 amendment**: re-examined the 3 entries below. Result: D1 + D2 are phase routing to #9 (Pattern-vs-instance split for ProjectState refactor). D3 (state.md migration to multi-department-aware shape) is a valid watch-list entry — names a chronological-valid signal (target-schema-not-yet-locked; awaits #9 + #11 finalization of state.md schema). Per v0.33 preliminary-lock: this DR remains preliminary-locked AND naming-superseded by #22 Sub-DR A. Original entries kept below as historical record.

### Original entries (with proper-home identification)

Three honest defers, each with specific home + cost being avoided:

**D1. Per-department phase tracking on ProjectState (`phases: dict[str, str]` instead of single `phase`).**
- **Home**: #9 (Pattern-vs-instance split).
- **Cost being avoided**: pre-empting #9's ProjectState schema refactor in #12 is wasted churn — #9 examines ProjectState comprehensively for PBS-coupling and splits core/extension fields together. Doing per-department phases in #12, then refactoring again in #9, is double work.
- **#12 commits**: documents the constraint that #9 must address.

**D2. Per-department lifecycle (`lifecycle: dict[str, Lifecycle]` instead of single `lifecycle`).**
- **Home**: #9. Same shape as D1.
- **Cost being avoided**: same as D1.

**D3. Migration of existing state.md files to multi-department-aware shape.**
- **Home**: first-bind moment (when first project is bound after #12+#11+#13 ship).
- **Cost being avoided** (chronological — session-11 retroactive
  reframe per v0.20): migration logic shape depends on the
  finalized state.md schema, which is designed in #9 (managed-
  entity concept) and reshaped under #11's multi-department
  schema. Writing migration logic before those commitments lock
  the target shape would lock the wrong target. **Note**:
  original framing "academic today; zero projects bound" was
  instance-anchored per v0.20; the chronological reason
  (target-schema-not-yet-locked) is what actually justifies
  the defer.
- **#12 commits**: documents migration steps for future implementation.

Per "Defer-instinct produces manufactured restraint" check: each defer names a specific cost being avoided + a specific home. Not generic "YAGNI." Honest defers.

## Revisit triggers

- **At #11 (Cowork integration)**: confirm slash-command namespacing + skill frontmatter sweep work cleanly under the `department:` discipline. Adjust if a fourth department type emerges (e.g., a "shared services" department for cross-department utility skills that's neither office-level nor department-of-domain-work).
- **At #6 (audit-trail v2 retrofit)**: confirm gate-side `departments_active` update logic composes cleanly with `actor_kind` updates. If two-field updates create race conditions or atomicity issues, refactor.
- **At #9 (Pattern-vs-instance split)**: confirm per-department phase/lifecycle split is implementable; if `phases: dict[str, str]` proves cumbersome, revisit shape.
- **At #14 (Memory Bank)**: confirm `search_memory` department filter composes naturally with the 4th memory axis. If filter logic gets complex (e.g., department-aware bauseine require multi-axis intersection), revisit.
- **First multi-department deployment** (Schulz adds PM, real or hypothetical second-domain office): confirm the architecture survives contact with a second department. Adjust per signal #1 (immediate empirical check) per ARCHITECTURE.md "Validation under the single-domain-pioneer constraint."
- **First builder-generated office with N≠1 departments**: confirm the pattern propagates correctly. If generated offices need per-domain customization of the department abstraction, revisit pattern level.

## Files touched

- `docs/decisions/office-vs-department.md` — this file
- `backend/mcp-server/src/pbs_mcp/project_state.py` — `departments_active` field
- `ARCHITECTURE.md` — v0.10 → v0.11; office-vs-department open-question section converted to resolved; meta-rule 3 invalidation table; scope-orthogonality 4th axis
- `ROADMAP.md` — #12 collapsed to shipped-summary; downstream constraint notes on #6/#9/#11/#14
- `HANDOFF.md` — session 9 closing state
