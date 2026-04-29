# Session handoff — pbs-bureau

## ⚡ For next session — essential framing

**Read these three before substantive work, in this order:**

1. **This file (`HANDOFF.md`)** — current session state, queue, recent decisions
2. **`VISION.md`** — three axes (intertwining-AI-workflow + sparring partnership + authorship preservation) + Vivienne Ming's research foundation (oracle / validator / sparring-partner modes; only sparring outperforms human-alone or AI-alone). **Without this, AI drifts toward oracle/validator-mode framings — gives easy answers instead of generating productive friction. Empirically confirmed session 9: VISION re-grounding caught a misframing mid-conversation, prompted the role-shift refinement.**
3. **`ARCHITECTURE.md`** — **v0.16**. Seven durable disciplines (pattern-vs-instance, archetype-portability, office-vs-department, managed-entity concept, entity-elevation 3-test, glue-not-replacement, **AI-as-runtime hybrid-shape**) + four meta-rules + entity types + scope orthogonality. **Without this, architectural proposals re-suggest already-discarded patterns or violate established discipline.**

**Read conditionally** (when context calls for it):
- `docs/strategic-positioning.md` — consulting positioning, marketplace decisions, brand questions, sparring-mode pitch
- `docs/decisions/<specific>.md` — when working in that decision's area (audit-trail-v2 for retrofits; office-vs-department for department modules; a2a-and-gemini-pattern-emulation for schema work)
- Specific ROADMAP commitment #N entry — when working on commitment #N
- Specific skill bundle (`plugin/skills/<name>/SKILL.md` + `references/`) — when modifying that skill
- `docs/plugin-conventions.md` (especially §11 + §11b) — writing or editing skills
- `docs/backend-conventions.md` — backend code work
- `~/dev/reference/knowledge-work-plugins/` — when working on #11 (Cowork integration)

**Read situationally** (rare; when explicitly relevant):
- `docs/audits/` + `docs/design-reviews/` — running follow-up reviews
- `docs/rag-pipeline-decisions.md` — Phase 0/1 RAG work
- All decision records together — when designing a new architectural discipline (rare)

The detailed "Read order for next session" section further down is the long-form version of this trio + conditional list. The trio above is the **minimum viable framing** for any session.

**Re-grounding mid-session is valid** when drift is detected — when AI's framings lean toward easy answers, when an architectural discipline isn't being applied, when the user pushes back on something that suggests oracle-mode drift. See `memory/feedback_vision_arch_grounding.md`.

---

End of session 10 (2026-04-29). This session executed pre-RAG
commitment **#16 (AI-as-runtime hybrid-shape contract)** —
single-session framing-pass work resolving the structured-vs-
markdown boundary for managed entities + manifests, before #11's
`department.yaml` format would lock the wrong choice. Same shape
as session 9's #12 work: decision record + ARCHITECTURE bump +
ROADMAP slot + downstream constraints.

**What shipped session 10**:

- **Decision record**: `docs/decisions/ai-as-runtime-hybrid-shape.md`
  — the principle ("AI is the runtime that fuses structured +
  markdown, not a bridging layer between them"), three-layer
  frontmatter contract (Layer 1 universal Pydantic base + Layer 2
  type Pydantic subclass + Layer 3 per-deployment deferred to #9),
  body conventions per entity type (recommended-not-enforced),
  resolution of "where do conditional rules live" (process-as-md,
  not entity-shaped), MCP gate generalization spec, worked
  examples (b-plan-begruendung, BauGB, adapter-mode Invoice), 6
  defers each with specific home + cost being avoided.
- **ARCHITECTURE.md v0.15 → v0.16**: new top-level discipline
  section "AI-as-runtime hybrid-shape principle" added (parallel
  to pattern-vs-instance + entity-elevation + glue-not-replacement).
  Version log entry. Boundary: structured for interfaces / identity
  / persistence / machine contracts; markdown for semantics / rules
  / domain knowledge / process descriptions.
- **ROADMAP.md commitment #16** inserted at position 1 of pre-RAG
  queue (BEFORE #11). Constraints flowed to #11 (department.yaml
  adopts hybrid-shape from inception, NOT pure YAML), #15 (Client
  + Actor entity definitions land as md files following the
  contract), #9 (gate generalization + body specs + doctypes
  migration + audit slice 21 + design-review target 12 all
  bundled), #6 (gate-side conformance check; AuditEvent format
  unchanged). Recommended next-session order updated.
- **Memory `feedback_ai_as_runtime.md`** added — captures the
  pattern correction: when AI processing is named as load-bearing
  pillar of an architecture, mirror the memory pattern (minimal
  skeleton + md body + AI as runtime); resist adding rule-encoding
  layers (even in prose) because that's the SQL-DB trap in
  disguise.

**Migration timing per #16 (no urgent migration this session)**:

- `extensions/universal/doctypes.yaml` + per-domain `doctypes.yaml`
  → per-entity md files: bundled with #9.
- `extensions/{universal,domain,state}/references-manifest.yaml`
  → per-reference md files: bundled with Phase 1 corpus
  (`research-references` already touches every entry during a
  full refresh).
- `extensions/department/<dept>/department.yaml` (new file format,
  #11): adopts hybrid-shape from inception — never persisted as
  pure YAML to begin with.
- Audit slice 21 + design-review target 12 implementation:
  bundled with #9 (depends on entity gate existence).

**Carried forward — session 9 work** (not duplicated, see
prior history below for full detail). #12 office-vs-department
shipped session 9; #15 Client+Actor added session-9 followup #2;
ARCH v0.10 → v0.15 cumulative.

---

End of session 9 (2026-04-29). This session executed pre-RAG
commitment **#12 (Office-vs-department modularization)** —
primarily design work resolving the open architectural question
from session 7 about offices conflating with single departments.
Plus a session-8 followup that landed earlier in this window:
#14 Memory Bank added to the v1 commitment queue scheduled
alongside Phase 1 corpus.

**What shipped session 9**:

- **Decision record**: `docs/decisions/office-vs-department.md`
  — full per-question reasoning (skill classification, memory
  4th axis, cross-department coordination shape, office-config
  schema, setup integration, pattern-vs-instance check). 11
  refinements from second pass + 3 explicit defers with
  proper-home identification.
- **ProjectState schema addition**:
  `departments_active: list[str] = Field(default_factory=list)` —
  routing + audit-filter dimension. Smoke-tested: default empty,
  explicit list, YAML round-trip preserves.
- **ARCHITECTURE.md v0.10 → v0.11**: office-vs-department
  open-question section converted to resolved; meta-rule 3
  invalidation table updated for ProjectState; scope-orthogonality
  layering convention extended from 3 to 4 axes (department added).
- **ROADMAP.md commitment #12** collapsed to shipped-summary;
  downstream constraint notes propagated to #6, #9, #11, #14, and
  Phase 1 corpus work.

**What also shipped earlier in this window** (session-8 followup):
- **Decision record framing pass** on a2a-and-gemini-pattern-
  emulation.md — three multipliers (builder / consulting / mid-
  term cross-boundary scenarios) replace PBS-Tier-3-centric
  framing.
- **Decision record Rows 8 + 9** added — RAG/Grounding
  architecture (constraint for Phase 1) + Evaluation/Simulation
  Service (constraint for Phase 0 #5).
- **#14 Memory Bank** added to v1 commitment queue (selective
  retrieval over memory layer; Vertex Memory Bank-inspired).
- **v2 Agent Simulation** entry added.
- **#13 hardware-spec research note** persisted (Hetzner tier
  ladder CCX23 → CCX33 → GEX44 → GEX131 with ingestion-vs-serving
  split architectural pattern).

**Constraints recorded session 9 for downstream commitments**:

- **#6 (audit-trail v2 retrofit)**: skill retrofits MUST set
  `actor_kind` (per #10) AND pass `department:` arg to memory
  tooling (per #12). Gate-side `departments_active` update logic.
  `query_audit_trail` `department:` filter + cached
  skill→department registry.
- **#9 (Pattern-vs-instance split)**: ProjectState core/extension
  split MUST handle per-department phase tracking
  (`phases: dict[str, str]`) and per-department lifecycle. Project-
  as-long-running-entity itself is PBS-instance; project entity
  becomes an opt-in extension.
- **#11 (Cowork integration)**: skill `department:` frontmatter
  sweep (REQUIRED, no default); slash commands namespaced; office-
  config `departments.<name>` schema bump + migration; department
  yaml file format; `integrate-department` skill creation.
- **#14 (Memory Bank)**: `search_memory` accepts `department:`
  filter (defaults to calling-skill's department); LanceDB memory
  index includes department metadata.
- **Phase 1 corpus work**: `search_corpus` gains optional
  `department_filter:` arg (defaults to calling-skill's department).

**Defers from session 9** (per office-vs-department.md):
- D1: per-department phase tracking on ProjectState → #9 (still
  pre-RAG)
- D2: per-department lifecycle on ProjectState → #9 (still pre-RAG)
- D3: state.md migration to multi-dept shape → first-bind moment
  (academic; zero projects bound today)

Each defer has a specific home + a specific cost being avoided.
Per "Defer-instinct produces manufactured restraint" check: honest
defers, not YAGNI.

---

## Read order for next session

1. **This file (HANDOFF.md)** — current state
2. **`ARCHITECTURE.md`** — **v0.16**. AI-as-runtime hybrid-shape
   discipline added (session 10). Office-vs-department resolved
   (v0.11); scope-orthogonality 4 axes; meta-rule 3 invalidation
   includes ProjectState.departments_active.
3. **`docs/decisions/ai-as-runtime-hybrid-shape.md`** — session-10
   load-bearing artifact. Read before tackling #11 (which adopts
   the hybrid-shape principle for `department.yaml` from
   inception). Three-layer frontmatter contract; body conventions
   per entity type; process-as-md.
4. **`docs/decisions/office-vs-department.md`** — session-9
   load-bearing artifact. Read before tackling #11 (which
   implements much of the structural sweep).
5. **`docs/decisions/a2a-and-gemini-pattern-emulation.md`** —
   session-8 artifact. Per-row decisions + constraints. Rows 8-9
   added in session-8 followup.
6. **`docs/decisions/`** — other authoritative records:
   - `mcp-fallback-policy.md` (session 7, fail-closed corollary)
   - `trigger-convention.md` (session 7, concept labels)
   - `audit-trail-v2.md` (session 7, single-write supersedes v1)
   - `audit-trail-v1.md` (SUPERSEDED, header note)
   - `sparring-output-v1.md` (session 6)
   - `backend-{test-layout,logging,mcp-error-format}.md` (session 5)
7. **`ROADMAP.md`** — commitments #10 + #12 + #16 shipped.
   Remaining pre-RAG queue: **#11 → #13 → #15 → #6 → #7 → #9 →
   #8 → C → D → Phase 0 → Phase 1+#14**. Generalize-and-publish
   in v1.x. AI-office builder + Agent Simulation in v2.
8. **`docs/plugin-conventions.md`** — §11 (triggers) + §11b
   (fail-closed fallback policy)
9. **`VISION.md`** — pioneer-instance milestones
10. **`docs/audits/`** + **`docs/design-reviews/`** — first runs
11. **`docs/rag-pipeline-decisions.md`** — Phase 0/1/2/3/4 phasing
12. **`docs/backend-conventions.md`** — backend idioms
13. **`plugin/CLAUDE.md`** — meta-rule 4 summary
14. **`plugin/skills/audit/`** — **0.9.0** (slice 20 added; slice
    21 entity-md conformance scheduled with #9)
15. **`plugin/skills/design-review/`** — **0.8.0** (target 11
    added; target 12 entity authoring conformance scheduled with
    #9)
16. **`plugin/skills/orchestrator/`** — **0.10.0**
17. **`backend/mcp-server/src/pbs_mcp/audit_trail.py`** —
    session 8 schema with ActorKind + new fields + cross-ref
    validator
18. **`backend/mcp-server/src/pbs_mcp/project_state.py`** —
    session 9 `departments_active` field; will refactor to
    `extensions/department/planning/entities/project.md` per
    #16 + #9
19. All other 16 skills — session-7 versions snapshot still
    current (no skill bodies touched sessions 8, 9, or 10)

---

## ⏳ Pre-RAG gating items (post-session-10 — #16 shipped)

**#10 ✅ shipped session 8.** **#12 ✅ shipped session 9.**
**#16 ✅ shipped session 10** (AI-as-runtime hybrid-shape contract).
**#14 (Memory Bank) added session-8 followup.** **#15 (Client +
Actor) added session-9 followup #2** — pre-RAG, scheduled between
#13 and #6. Recommended execution order:

```
Session 11-14: #11 (deep Cowork integration refactor)         3-5 sessions
Session 15-17: #13 (deployment flexibility + Coolify ref dep)  2-3 sessions
Session 18-19: #15 (Client + Actor as office entities)         1-2 sessions
Session 20+:  #6 → #7 → #9 → #8                               per existing queue
              C (sparring-output integration)
              D (plugin version bump)
Then:         Phase 0 items 4 + 5 → Phase 1 corpus + #14 (Memory Bank bundled)
```

### Already shipped (architectural backstops)

1. ✅ **Unified audit trail v1** — schema + Pydantic + 2 MCP
   tools shipped session 6.
2. ✅ **Sparring-output structural promotion** — schemas + MCP
   tool + plugin-conventions field shipped session 6.
3. ✅ **State.md MCP gate** — Pydantic + 2 MCP tools shipped
   session 6. **Skill retrofits done session 7.**
4. ✅ **Fail-closed corollary** — done session 7.
5. ✅ **Trigger-convention simplification** — done session 7.
6. ✅ **Audit-trail v2 decision** — record done session 7;
   implementation deferred to commitment #6 (in remaining queue).
7. ✅ **A2A schema compatibility + Gemini Enterprise pattern
   emulation** — **done session 8**. Decision record + AuditEvent
   schema additions + ARCHITECTURE bump.
8. ✅ **Office-vs-department modularization** — **done session 9**.
   Decision record + ProjectState schema addition + ARCHITECTURE
   bump.
9. ✅ **AI-as-runtime hybrid-shape contract** — **done session 10**.
   Decision record + ARCHITECTURE bump (v0.15→v0.16) + ROADMAP
   commitment #16 + downstream constraints to #11/#15/#9/#6.
   Three-layer frontmatter contract (universal Pydantic base +
   per-type Pydantic subclass + per-deployment deferred). Body
   conventions per entity type, recommended-not-enforced.
   Process-as-md, not state-machine-as-data.

### Remaining for next-immediate-session-before-RAG

**#11 — Cowork as primary end-user runtime, DEEP integration**
(ROADMAP commitment #11) — **POSITION 1 in remaining queue**:
- Deep + complete integration directive: adopt Anthropic's plugin
  shape wholesale where it differs from ours.
- **Per #12 constraint**: all 19+ skills get `department:`
  frontmatter (REQUIRED, no default). Slash commands namespaced
  (`/<dept>:<skill>` — `/planning:draft-begruendung`,
  `/office:setup-office`, etc.). Office-config `departments.<name>`
  schema bump + migration co-located with `pbs.local.md`.
  `extensions/department/<dept>/department.yaml` file format
  implementation. New `integrate-department` skill creation.
- **Per #10 constraint**: plugin agents emit events as
  `actor_kind="skill", actor_card=<agent-name>`.
- 3-5 sessions; substantial refactor touching every user-facing
  surface.

**#13 — Deployment flexibility + Coolify reference deployment**
(ROADMAP commitment #13) — **POSITION 2 in remaining queue**:
- Pluggable persistence + auth + transport abstractions.
- **Per #10 constraint**: HTTP MCP transport implementation lands
  here. AuditEvent.user_id field for multi-user attribution. Data
  classification annotations.
- **Hardware spec persisted** (session-8 followup): start
  CCX23/CCX33 Hetzner Cloud, ingestion-vs-serving split (heavy
  compute on RTX 5090 local, rsync indices to cloud), upgrade-
  triggered to GEX44/GEX131 if needed.
- 2-3 sessions.

**#15 — Office-level managed entities (Client + Actor)** (added
session-9 followup #2):
- Office-level managed entities concept introduced —
  `extensions/office/entities/<entity>.py` (parallel to
  `extensions/department/<dept>/entities/`).
- **Client** Pydantic schema (native default) — referenced by
  Project (planning), Invoice (invoicing), Timesheet (PM), etc.
- **Actor** refactor — migrate from `office-config.actors[]`
  semi-typed config to first-class native managed entity. Identity
  primitive for #13's multi-user auth.
- Cross-department reference convention: entities hold
  `<entity>_id: str` fields; gate validates references exist;
  no FK enforcement at storage layer.
- 1-2 sessions; AFTER #13 (multi-user); BEFORE #6 (audit retrofit
  references Actor).

**#6 — Audit-trail v2 retrofit** (per `audit-trail-v2.md`,
**scope expanded session-9 followup #2**):
- Backend: `record_decision` + `render_audit_trail` tools;
  `user_confirmation` event kind; `reasoning_full_text` in
  decision/module_decision details; drop `phase_history` from
  ProjectState.
- **Per #10 constraint**: every retrofit explicitly sets
  `actor_kind` on every event.
- **Per #12 constraint**: every retrofit passes `department:` arg
  to memory tooling. Gate-side `departments_active` update logic
  + cached skill→department registry. `query_audit_trail`
  `department:` filter.
- **Per #15 constraint**: AuditEvent.actor references Actor.id
  (office-level managed entity); replaces today's free-form actor
  string with typed reference.
- **Per session-9 followup #2 (approval flows)**: add event kinds
  `approval_requested`, `approval_granted`, `approval_rejected`.
  Details payload: `approving_actor`, `policy_rule`, `subject_entity_id`.
  Approval flows are event-driven, NOT entity-shaped (per the
  3-test entity-elevation discipline). Authorization rules live in
  skill logic, not entity schema.
- Skills: orchestrator + save-baustein + record-feedback +
  draft-textteil-b/c + review-draft + research-references retrofits.
- Migration: `backfill_audit_trail` walks legacy prose sources.

**#7 — Bootstrap-write MCP tools**:
- `create_manifest` + `create_office_config` (Pydantic-validated
  first-write through loader).
- `author-manifest` + `setup-office` skill retrofits.

**#9 — Department module contract + managed-entity concept**
(reframed session-9 followup; was "Pattern-vs-instance best-
effort split"):
- **Mission**: design the department module contract +
  managed-entity concept with two delivery modes (native +
  adapter-delegated). The original "extract universal core"
  framing was wrong — there is no universal entity-type core;
  each department defines its own entity types completely.
- **Per #12 constraints**:
  - Per-department phase tracking (`phases: dict[str, str]`)
  - Per-department lifecycle (`lifecycle: dict[str, Lifecycle]`)
  - Project-as-long-running-entity becomes opt-in per department
- **Managed-entity concept work**:
  - Two delivery modes per entity (native + adapter), mixed-mode
    within a department supported
  - Adapter mode generalizes meta-rule 1's existing integration-
    adapter pattern (same Pydantic Protocol + concrete adapter
    contract; expanded consumer set from auxiliary integrations
    to primary department system-of-record)
  - ProjectState refactor: from
    `backend/mcp-server/src/pbs_mcp/project_state.py` to
    `extensions/department/planning/entities/project.py`
    (planning department's primary native managed entity)
  - Per-company customization mechanism design: choose between
    Pydantic subclass / `extra_fields: dict[str, type]` /
    `metadata: dict` escape hatch
- Office-config schema: `departments.<name>.entities.<entity>.
  {mode,adapter,config}` per-entity sub-sections
- Doctype-manifest generalization (per-department contribution)
- Output: refactored backend + skill retrofits + passing PBS
  tests + `pattern-vs-instance-split-rationale.md` documenting
  per-decision reasoning
- **Order note**: AFTER #6 + #7 (so #9 examines stable post-v2
  schemas + bootstrap-write tool interfaces); BEFORE #8.
- **Scope**: 2-3 sessions (was 1-2; expanded per session-9
  followup reframe).

**#8 — Pre-action framing skill**:
- Design + scaffold meta-skill (`frame-task` or `scoping`).
- Triggered on non-trivial task starts.
- **Order note**: AFTER #9 — codifies pattern-vs-instance reasoning
  produced by #9 into a repeatable check.

**#14 — Memory Bank** (session-8 followup):
- `search_memory` + `read_memory_entry` MCP tools; LanceDB index
  over `memory/`; embedding job.
- **Per #12 constraint**: `search_memory` accepts `department:`
  filter (defaults to calling-skill's department).
- Bundled with Phase 1 corpus work — shares embedding
  infrastructure (bge-m3 + LanceDB + rerank).

### Sparring-output integration (still per v1 plan)

- `review-draft` declares `output_schema: ReviewOutput`; body adds
  Output Format section.
- `orchestrator` PROCEDURE Checkpoint 13 declares
  `RecommendationOutput` schema; calls `validate_skill_output`.

### Plugin version bump

- `plugin.json` 0.3.0 → 0.5.0 after #6/#7/#9 retrofits land.
  Run `bash dev-link.sh` after.

### Then — Phase 0 items 4 + 5

- **Phase 0 item 4 — Feature-survey skill**: greenfield-the-vision
  sibling to audit + design-review.
- **Phase 0 item 5 — Testing methodology + harness**: discussion-
  first. **Per #10 constraint**: design eval-result schema as
  Pydantic contracts (`EvalRun` / `Scenario` / `EvalResult` /
  `RegressionSuite`).

### Then — Phase 1 corpus download + #14 bundled

Fetch all 57 entries via `research-references` full refresh.
**No embeddings yet on corpus during fetch** — raw fetch +
checksum + manifest population. Embedding pass **runs locally on
RTX 5090** per #13's ingestion-vs-serving architectural pattern
(persisted in #13 hardware-spec note); LanceDB indices then rsync
to cloud serving node. Memory Bank index built on serving node
directly (continuous low-rate writes).

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis (canonical "why") |
| `ARCHITECTURE.md` | **v0.16** — AI-as-runtime hybrid-shape principle added (session 10); office-vs-department resolved (v0.11) + 4-axis scope-orthogonality |
| `ROADMAP.md` | 16 v1 commitments (#10 + #12 + #16 ✅ shipped); remaining queue + downstream constraints |
| `~/dev/reference/knowledge-work-plugins/` | Cloned Anthropic plugins repo for #11 study |
| `docs/decisions/ai-as-runtime-hybrid-shape.md` | **Session-10 deliverable** — three-layer frontmatter contract + body conventions per entity type + process-as-md + gate generalization spec + 6 defers |
| `docs/decisions/office-vs-department.md` | **Session-9 deliverable** — per-question decisions + downstream constraints + 3 defers |
| `docs/decisions/a2a-and-gemini-pattern-emulation.md` | Session-8 deliverable — 9 rows of decisions + multipliers framing |
| `docs/decisions/mcp-fallback-policy.md` | Session-7 fail-closed corollary |
| `docs/decisions/trigger-convention.md` | Session-7 concept labels |
| `docs/decisions/audit-trail-v2.md` | Session-7 reversal; supersedes v1 |
| `docs/decisions/audit-trail-v1.md` | SUPERSEDED |
| `docs/decisions/sparring-output-v1.md` | Session-6 v1 commitment |
| `docs/decisions/backend-{test-layout,logging,mcp-error-format}.md` | Session-5 backend records |
| `docs/audits/boundary-adherence-20260429.md` | Slice 14 first run (session 6) |
| `docs/audits/invalidation-contract-20260429.md` | Slice 15 first run (session 6) |
| `docs/audits/validation-gate-20260429.md` | Slice 16 first run (session 6) |
| `docs/design-reviews/vision-arch-coupling-20260429.md` | Target 8 first run (session 6) |
| `docs/design-reviews/foundations-20260429.md` | Session-5 design-review |
| `backend/mcp-server/src/pbs_mcp/audit_trail.py` | Session 8 — ActorKind + 3 new fields + cross-ref validator |
| `backend/mcp-server/src/pbs_mcp/project_state.py` | **Session 9** — `departments_active: list[str]` field |
| `plugin/skills/audit/` | **0.8.0** — slices 1-16 + 18 + 19 |
| `plugin/skills/design-review/` | **0.7.0** — targets 1-10 |
| `plugin/skills/orchestrator/` | **0.10.0** |
| `plugin/CLAUDE.md` | Updated meta-rule 4 summary |
| `docs/plugin-conventions.md` | §11 (triggers) + §11b (fallback policy) |
| `~/.config/pbs-bureau/office.yaml` | v3 (session 6 migration) |

---

## Skill versions snapshot (post-session 9 — unchanged from session 7)

No skill versions changed sessions 8 or 9. Both were backend-
schema + decision-record work; no skill bodies touched. The
session-7 versions snapshot remains current. Will change
significantly in session 10+ when #11 introduces `department:`
frontmatter sweep + slash command namespacing.

| Skill | Version |
|---|---|
| audit | **0.9.0** (slice 20 — entity-elevation drift scan, session-9 followup) |
| author-manifest | 0.4.0 |
| design-review | **0.8.0** (target 11 — entity-elevation check, session-9 followup) |
| draft-cover-mail | 0.6.0 |
| draft-textteil-b | 0.5.0 |
| draft-textteil-c | 0.5.0 |
| orchestrator | 0.10.0 |
| promote-to-skill | 0.5.0 |
| record-feedback | 0.4.0 |
| research-references | 0.5.0 |
| review-draft | 0.5.0 |
| save-baustein | 0.4.0 |
| setup-office | 0.6.0 |
| survey-project | 0.5.0 |
| validate-bausteine | 0.4.0 |
| validate-checklist | 0.6.0 |
| validate-latex-style | 0.5.0 |
| verify-citations | 0.5.0 |
| watch-list | 0.2.0 |
| plugin.json | 0.3.0 (will bump to 0.5.0 after #6/#7/#9) |

---

## MCP tools shipped session 9

None this session — schema-only addition to existing ProjectState.
The session-6 tools (5 new) + session-8 AuditEvent additions
remain the current backend surface. Backend tools planned for
next-immediate-session retrofit (per #11 + #6 queue):
- `record_decision` (audit-trail v2 — for #6)
- `render_audit_trail` (audit-trail v2 — for #6)
- `create_manifest` (bootstrap-write — for #7)
- `create_office_config` (bootstrap-write — for #7)

Schema-side, ProjectState gained `departments_active: list[str]`
defaulting to empty. Gate-side update logic (gate appends
department to list when event's `actor_card ∈ skills_in_dept`)
deferred to #6.

---

## Working-style notes (carried + new)

1. **Pre-action framing matters more than post-action review**
   (carried). Session 9 explicitly used the framing-pass pattern
   for #12: drafted in chat, reviewed once, refined once with
   explicit defer-instinct check, THEN persisted.

2. **Defensive pre-RAG schema additions are nearly free** —
   confirmed again session 9. ProjectState.departments_active
   was a 1-line Pydantic field + smoke-test, ~10 minutes of work.
   Migration cost post-data-accumulation would be a multi-skill
   retrofit.

3. **"No menus, commit to positions"** (carried). Session 9
   produced verdicts on each of 7 open questions; refinement
   pass added 11 more committed positions; defers explicitly
   named with proper homes.

4. **Defer-instinct check is now explicit discipline.** Session 9
   listed 3 defers, each named with specific home + specific cost
   being avoided. Per "feedback_defer_instinct" memory: not
   generic YAGNI — honest defers.

5. **Pattern-vs-instance discipline catches real coupling.**
   Surfaced in #12 refinement: project-as-long-running-entity is
   PBS-instance, not pattern-universal. Some offices (brand-voice,
   single-skill utilities) have no project entity. Constraint
   passed to #9 (Pattern-vs-instance split). Without the check
   we'd have shipped a pattern that doesn't actually generalize.

6. **Entity-elevation discipline (session-9 followup #2)**: prefer
   events + nested fields + memory entries over new managed entity
   types. Elevate to first-class managed entity only when stable-
   identity + state-of-record + lifecycle ALL apply. Avoids the
   architecture creeping toward an SQL schema (catastrophic for
   LLM-mediated AI offices). Right level: knowledge graph + document
   store with stable references, not Oracle. Demoted Approval from
   proposed managed entity to event-kinds on AuditEvent (folded
   into #6's scope). Future audit/design-review check (target 11)
   should scan for over-modeled entities. **Broader-review pass
   (session-9 followup #3)** confirmed zero major gaps in capturing
   common business workflows: 7 candidate concerns (document
   versioning, notifications, role-based actors, reports, conflicts,
   business calendar, knowledge depreciation) all resolved via
   existing infrastructure / scope expansion of existing commitments
   / defer-to-concrete-need / out-of-scope-per-pattern-vs-instance.
   No new commitment numbers added.
   **Infrastructure-primitive review pass (session-9 followup #4)**
   stress-tested core primitives (skills, managed entities, audit
   events, memory, integration adapters, cross-department
   coordination) against business-process expressibility. 9/9
   coverage after two genuine gaps fold into existing commitments:
   Gap A (proactive time-driven triggers → server-side scheduler
   in #13) and Gap B (adapter-emitted events for external state
   changes → adapter Protocol generalization in #9). No new
   commitment numbers.

7. **Memory captures**: existing 6 feedback memories carry
   forward. The "leave legacy behind" + "judgment-not-menus" +
   "defer-instinct" + "entity-elevation discipline" principles all
   paid off in this conversation cycle.

8. **Glue-not-replacement principle (session-9 followup #6)**: PBS
   is the glue/coordination layer that brings AI to existing
   infrastructure; not a replacement for BPMN engines / accounting
   tools / CRMs / calendars / etc. Generalizes meta-rule 1's
   integration-adapter pattern as the canonical mechanism. Different
   addressable market than vertical-SaaS-replacement plays. ARCH
   v0.14 → v0.15 codifies as top-level discipline. ROADMAP v1.x-v2
   gains BPMN-empowerment entry as concrete positioning. ROADMAP v2
   AI-office-builder gains marketplace-as-v3 subsection (concept
   only; decision deferred; v2 builder output format must be
   marketplace-compatible from start). New `docs/strategic-
   positioning.md` captures the full strategic framing for
   consulting positioning (open-source-as-edge / three-tier content
   strategy / glue-not-replacement / cognitive-load-reduction
   framing / three risks / revenue model / marketplace arc /
   competitive landscape).

---

## Session 9 commits (chronological)

| # | Commit | Theme |
|---|---|---|
| 1 | (this commit) | session 9: pre-RAG #12 shipped — office-vs-department modularization. Decision record + ProjectState.departments_active + ARCHITECTURE v0.10→v0.11 + ROADMAP collapse + downstream constraints for #6/#9/#11/#14/Phase-1. |

Plus session-8 followups landing earlier in this conversation
window:
- `b6faaa6` — A2A decision record framing pass (3 multipliers)
- `b8390d7` — Rows 8 + 9 (RAG/Grounding + Eval/Simulation gaps)
- `9aa6d8d` — #14 Memory Bank + v2 Agent Simulation
- `1c5837c` — #13 hardware-spec research note (Hetzner ladder)

All pushed to origin/main.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **Plugin cache symlink**: bump `plugin.json` AND re-run
  `bash dev-link.sh` after #6/#7/#9 retrofits.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Office-config**: v3 on disk; no `path_classification` block.
  v4 schema bump (departments) lands in #11.
- **No projects bound yet**: schema additions (AuditEvent fields,
  ProjectState.departments_active) are design-time-pending until
  first project bind.
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md`
  - `feedback_judgment_and_automate.md`
  - `feedback_push_after_commit.md`
  - `feedback_refine_pareto.md`
  - `feedback_defer_instinct.md`
  - `feedback_llm_instruction_tightness.md`
  - `feedback_vision_arch_grounding.md`
  - `feedback_ai_as_runtime.md` (session 10 — when AI processing is named as load-bearing pillar, mirror the memory pattern; resist rule-encoding layers even in prose)
