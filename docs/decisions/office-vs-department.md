# Decision record: office-vs-department modularization

**Status**: ACCEPTED (session 9, 2026-04-29)
**Owner**: per-session HANDOFF; ARCHITECTURE.md office-vs-department section; ROADMAP commitment #12
**Related**: ROADMAP commitment #11 (Cowork integration — slash command namespacing depends on this), #14 (Memory Bank — uses 4th memory axis), #6 (audit-trail v2 retrofit — actor_kind + department-aware), #9 (Pattern-vs-instance split — handles per-department phase/lifecycle on ProjectState), `a2a-and-gemini-pattern-emulation.md` Row 4 (cross-department coordination must be event-shaped)

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

**For #9 (Pattern-vs-instance best-effort split)**:
- ProjectState core/extension split MUST handle per-department phase tracking (`phases: dict[str, str]`) and per-department lifecycle (`lifecycle: dict[str, Lifecycle]`). Today's single-valued `phase` and `lifecycle` are PBS-instance assumptions that don't generalize to multi-department offices. #12 documents the constraint; #9 implements the split.
- Project-as-long-running-entity is itself a PBS-instance assumption. Some offices (brand-voice, single-skill utilities) have no project entity. ProjectState core/extension split should make the project entity itself an opt-in extension, not a pattern-level mandatory.

**For #11 (deep Cowork integration)**:
- All skills get `department:` frontmatter field added (REQUIRED, no default). Sweep covers all 19+ skills.
- Slash commands namespaced: `/<department-slug>:<skill-name>` → `/planning:draft-begruendung`, `/office:setup-office`, `/office:integrate-department`, etc.
- Office-config schema bump for `departments.<name>` sections; co-located with `pbs.local.md` migration.
- `extensions/department/<dept>/department.yaml` file format implementation (event_subscriptions).
- `integrate-department` skill scaffolding (new skill bundle).

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

## Defers (with proper-home identification)

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
- **Cost being avoided**: writing migration logic against a hypothetical that may never run. Today: zero projects bound. When first-bind happens, the actual current state.md shape is known; migration is straightforward (likely `departments_active: ["planning"]` injection + nothing else).
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
