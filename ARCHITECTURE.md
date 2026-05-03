# Architecture — Phase 3 rebuild (in progress)

> **Status**: Phase 3 ARCH rebuild ACTIVE. Phase 2 GLOSSARY foundational vocabulary lock COMPLETE (36 entries per `docs/decisions/greenfield-rederivation-pause.md` Step 1.A). Phase 3.1 closed; Phase 3.2 topic taxonomy + structure LOCKED. Per-topic detail lives in `arch/<topic-slug>.md` files as Phase 3.3+ topic content lands.

## 1. Audience + scope

**This doc is framework-developer documentation.** Layer 2 Overview per `MAINTENANCE.md` 5-layer doc model. Loaded at framework-development session start (along with VISION + MAINTENANCE.md + HANDOFF) for architectural orientation.

**NOT loaded at production runtime by deployed-workspace AI.** AI in a deployed PBS workspace doing accountability-bearing work loads runtime-relevant markdown (workspace.md / active specialist DEFINITIONs / skill SKILL.md / shape policy bundles) — not framework architecture documentation.

**Three consumer modes**:

| Mode | Consumer | Loads ARCHITECTURE.md? |
|---|---|---|
| Framework development (current Phase 3+ work) | AI as framework-developer-collaborator + human framework developers | YES — orientation at session start |
| Deployment template creation (L3) / shape composition (L4) | Template/shape creators needing framework architecture understanding | OCCASIONALLY — on-demand reference |
| Production runtime (deployed PBS workspace) | AI runtime processing accountability-bearing work | NO — framework architecture not needed for per-claim work |

**Optimization target**: human readability + framework-developer orientation. NOT optimized for AI runtime parsing.

**Scope**: Phase 3 progress + topic catalog + reading order + cross-cutting principles + locked architectural decisions + active disciplines + watch-list. Migrates toward stable architectural overview as Phase 3 completes.

**Cites**: GLOSSARY entries (Layer 1; locked) + DRs (Layer 4; selective rebuild Phase 4) + specs (Layer 5; Phase 6 territory).

## 2. Phase 3 sub-phase status

| Sub-phase | Scope | Status |
|---|---|---|
| **3.0** | Doc structure (single ARCHITECTURE.md vs topic-per-file vs hybrid) | LOCKED — hybrid |
| **3.1** | Open architectural questions (workflow / work-unit / deployment / engaged-authorship) | COMPLETE — all 4 LOCKED. Coherence-audit ran at phase boundary; 0 architectural REVISIONS. |
| **3.2** | Topic taxonomy + naming + cross-cutting placement + ARCHITECTURE.md structure (4 sub-decisions) | COMPLETE — all 4 sub-decisions LOCKED. Composite DR `phase-3-2-doc-organization.md`. |
| **3.3** | Per-mechanism detail (12 mechanisms; subsumed into Pattern A protocol topics) | Pending |
| **3.4** | Per-architectural-Protocol detail (3 Pattern A protocol topics: substrate / adapter; quality-gate at 3.6) | Effectively COMPLETE — substrate + adapter remain Pattern A; sparring + audit RECLASSIFIED as mechanism classes per `docs/decisions/greenfield-rederivation-pause.md` Step 3; coordination + trust + time CANCELLED (subsumed). |
| **3.5** | Per-primitive detail topics (4 primitive-cluster topics + 2 cross-cutting integrators) | Pending |
| **3.6** | Quality-gate ARCH topic | Pending |
| **3.7** | Cross-cutting investigations (PydanticAI re-eval; markdown-validation; Ming research; multi-VISION) | Pending |
| **3.8** | Coherence-audit checkpoint C3 (phase-boundary; ARCH-specific Lenses 11-15 activate) per `DISCIPLINES.md` Discipline 9 | Pending — preceded by C1 (post-3.4) + C2 (post-3.5) per cadence in `BACKLOG.md` Phase 3 audit-checkpoints |

Foundation-up ordering applied (per `DISCIPLINES.md` Discipline 8): questions before structure before content before audit.

## 3. Doc structure (Phase 3.0 LOCKED)

**Hybrid**: single overview + per-topic files.

| Doc | Purpose | Lines | Status |
|---|---|---|---|
| `ARCHITECTURE.md` (this file) | Overview + topic catalog + cross-cutting principles + Phase 3 status | ~350 target | Active |
| `arch/<topic-slug>.md` × 11 | Per-topic detail | ~500 each | Active (4 of 11 drafted: substrate / adapter / sparring / audit) |

**Why hybrid**: pure-single (10K lines) is unwieldy + context-budget concern; pure-multi has no entry point + cross-cutting orphaning. Hybrid aligns with progressive-disclosure principle (skill-craft pattern: SKILL.md → PROCEDURE.md → references/).

## 4. Topic catalog (Phase 3.2 LOCKED — 11 topics)

11 ARCH topics in protocol-centric aggregation with primitive-cluster topics. Foundation-up ordered. Per Phase 3.2 Sub-decision 1 lock + greenfield-rederivation cascade (per `docs/decisions/greenfield-rederivation-pause.md` Step 3); filenames per Sub-decision 2 lock.

| # | Topic file | Primary content (one-liner) | Phase |
|---|---|---|---|
| 1 | `arch/substrate.md` | Substrate Protocol Surface + per-impl + persistent-state + session interaction; subsumes Coordination (hooks + event-bus) + Time (temporal semantics per impl) | 3.4 — DRAFTED |
| 2 | `arch/adapter.md` | Adapter Protocol Surface (META + per-integration-class) + per-impl + lifecycle/auth; subsumes Time (time-driven adapter operations) | 3.4 — DRAFTED |
| 3 | `arch/sparring.md` | Sparring **mechanism class** (RECLASSIFIED — not Pattern A): 8 sub-mechanism contracts + per-shape policy declares which active + how-enforced | 3.4 — DRAFTED |
| 4 | `arch/audit.md` | Audit **mechanism class** (RECLASSIFIED — not Pattern A): AuditEvent schema = mechanism Surface + per-shape granularity policy + substrate-mediated storage backend; subsumes Trust (authority-binding + per-shape trust policy) | 3.4 — DRAFTED |
| 5 | `arch/quality-gate.md` | Quality-gate Pattern A Surface + per-shape implementations + signal catalog | 3.6 |
| 6 | `arch/specialist-skill.md` | Specialist DEFINITION + skill granularity + bundle structure + marketplace | 3.5 |
| 7 | `arch/practitioner.md` | Practitioner Pattern C bipartite + record placement + multi-practitioner | 3.5 |
| 8 | `arch/workflow-work-unit.md` | Workflow Pattern B + work-unit Pattern B + workflow_instance state machine + orchestration | 3.5 |
| 9 | `arch/claim-defensibility.md` | Claim primitive + defensibility test + source-grounding + engaged-authorship + per-claim attestation | 3.5 |
| 10 | `arch/scope-model.md` | Workspace + Framework C / Owner B / Layer A scope categories + entity placement | 3.5 |
| 11 | `arch/axis-interactions.md` | 3 VISION axes interaction + co-worker frame + category-collapse cross-axis force | 3.5 |

**Cancelled topics** (per `docs/decisions/greenfield-rederivation-pause.md` Step 3): `arch/coordination.md`, `arch/trust.md`, `arch/time.md` — never written; subsumed into substrate/audit/adapter. Saves ~1500 lines of un-written ARCH content.

**Aggregation discipline**: aggregate when items tightly coupled OR individually <100 lines (per coherence-audit Lens 15). Each topic targets ~500 lines avg; per-topic flex acceptable.

**Foundation-up dependency**: topics 1-2 are Pattern A protocols (foundational mechanism layer); 3-4 are mechanism-class topics (per-shape policy variation, not Pattern A); 5 quality-gate Pattern A composes with all axes (Phase 3.6); 6-9 are primitive clusters; 10-11 are cross-cutting integrators (load LAST).

**Phase 3.7 cross-cutting investigations excluded** (research/strategic items, not ARCH-topic-shaped): PydanticAI substrate eval / Markdown-validation feasibility / Ming research deepening / Adjacent thinkers expansion / Multi-VISION model question.

**Headroom**: 9 emergent topics may be added (11 → 20 cap) during Phase 3.3-3.6 work without taxonomy revision.

## 5. Reading order

**For new readers** orienting to framework architecture, foundation-up:

1. **VISION.md** (Layer 1) — three-axis thesis; falsification framing
2. **GLOSSARY.md** (Layer 1) — locked vocabulary (36 entries)
3. **MAINTENANCE.md** (Layer 0) — doc-system discipline + TOP-LEVEL ARCHITECTURE
4. **ARCHITECTURE.md** (Layer 2; this doc) — overview + topic catalog + cross-cutting principles
5. **arch/<topic>.md** (Layer 3) — topic detail in foundation-up order:
   - **Pattern A protocols**: substrate → adapter → quality-gate
   - **Mechanism classes** (per-shape policy variation; not Pattern A): sparring → audit
   - **Primitive clusters**: specialist-skill → practitioner → workflow-work-unit → claim-defensibility
   - **Cross-cutting integrators** (LAST): scope-model → axis-interactions
6. **DRs** (Layer 4) — decision rationale for specific commits
7. **Specs** (Layer 5; Phase 6) — Pydantic schemas + spec docs

**For session-resumption**: read HANDOFF.md + BACKLOG.md before substantive work.

**For specific debugging / contextual entry**: experienced readers can enter at relevant `arch/<topic>.md` directly; reading order is recommendation not gate.

## 6. Cross-cutting principles

Concise summaries; full content in `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES + 5-layer doc model.

### Pattern-A vs Pattern-B vs Pattern-C structural semantics

| Pattern | Shape | Examples |
|---|---|---|
| **Pattern A** (pluggable subsystem) | Surface (interface contract) + Implementations (per-shape variation) + Selection (workspace.md / shape policy declares which impl) | Substrate / Adapter / Quality-gate |
| **Pattern B** (bipartite definition + instance) | DEFINITION aspect (Framework C) + INSTANCE aspect (Owner B) | Specialist / Workflow / Work-unit |
| **Pattern C** (cross-cutting human + record) | HUMAN aspect (lives outside workspace) + RECORD aspect (Owner B) | Practitioner |

Sparring + Audit RECLASSIFIED as mechanism classes (not Pattern A) per `docs/decisions/greenfield-rederivation-pause.md` Step 3; Coordination + Trust + Time SUBSUMED. Cross-pattern composition (e.g., specialist Pattern B containing workflow Pattern B) is locked per GLOSSARY entries.

### Cascade direction (UPSTREAM + DOWNSTREAM bidirectional per `MAINTENANCE.md`)

- **UPSTREAM**: GLOSSARY change → cascade to ARCH/DRs/specs (Layer 1 → 2-5)
- **DOWNSTREAM**: ARCH/DR/spec work surfacing glossary-grade structural fact → retro-fit GLOSSARY before locking (Layer 2-5 → 1)

GLOSSARY back-check fires at decision-design-sharpening Round 2 termination + ARCH topic completion + DR drafting.

### Scope-categorization framing

Three scope categories (per locked GLOSSARY entries):
- **Framework C** — distributable definitions (specialist DEFINITIONs / shape policies / Pattern A protocols / mechanism interface contracts)
- **Owner B** — workspace-bound instances (workspace.md / specialist instances / work-unit instances / workflow_instances / practitioner-records / Actor records / engagement-target entities per shape)
- **Layer A** — content varying by deployment context (universal / domain-keyed / state-keyed)

Detail in `arch/scope-model.md` (Phase 3.5).

### Foundation-up ordering principle

Lock items others depend on FIRST; downstream items composing with multiple foundations come last. Applied across Phase 3.1 sub-decisions / topic ordering / within-Sub-decision sharpening. Per `DISCIPLINES.md` Discipline 8 + cascade discipline.

### Workspace boot + shutdown composite sequence

Step-by-step composite boot ordering across audit + substrate + adapter, resolving substrate §10 + audit §10 step-numbering ambiguity. Substrate §10 + audit §10 reference THIS subsection rather than duplicating ordering.

**Boot composite ordering** (audit-phase precedes substrate-phase precedes adapter-phase per audit-storage-realization-before-first-substrate-event invariant):

1. **audit-phase 1**: AuditEvent schema validation (Pydantic schema available; emission API defined)
2. **audit-phase 2**: Substrate-internal storage backend availability check (filesystem accessible; existing audit-trail (if present) hash-chain verifiable per `arch/audit.md` §10 boot step 3)
3. **audit-phase 3**: Audit Surface available (`audit_storage_ready` per `arch/audit.md` §10 boot step 4); emission API ready BEFORE substrate emits its first architectural event
4. **substrate-phase 1**: Substrate Implementation instantiates per workspace.md selection (`substrate = await ChosenSubstrate.from_config(config)` per `arch/substrate.md` §10 boot step 3); agent-loop entry available
5. **substrate-phase 2**: Substrate registers configured MCP servers (per `arch/substrate.md` §10 boot step 4); substrate-emitted events flow through audit Surface from this point (per substrate §8 dual-emission)
6. **substrate-phase 3**: Adapter bindings load (per workspace.md adapter bindings list; per-binding instantiation per `arch/adapter.md` §10 per-instance boot in declaration order; adapter-emitted events flow through audit Surface)
7. **substrate-phase 4**: Specialist registration (substrate-native materialization per substrate Surface §G)
8. **substrate-phase 5**: `boot_complete` event emitted via audit Surface; agent loop accepts runs (per substrate §10 boot steps 8-9); `workspace_booted` event-kind first-class in audit-trail

**Shutdown composite ordering** (reverse with explicit flush-before-release invariants):

1. Substrate shutdown initiates: `shutdown_initiated` event emitted via audit Surface
2. In-flight agent runs drain to completion OR cancel per cancellation policy
3. Substrate stops accepting new run_agent calls
4. Adapter bindings shut down in REVERSE declaration order (per `arch/adapter.md` §10 per-instance shutdown); per-binding drains in-flight operations + flushes auth tokens / circuit state / threading caches; per-binding `adapter_stopped` events emitted
5. MCP servers stop (subprocess MCP servers gracefully terminate)
6. Substrate releases substrate-internal runtime resources; `shutdown_complete` event emitted via audit Surface
7. Sparring (mechanism class peer) emissions drain; final events emit via audit Surface
8. Audit storage realization shutdown LAST (per `arch/audit.md` §10 shutdown steps 5-8): substrate-impl drains pending audit-trail writes; flushes audit-trail to storage; verifies hash-chain integrity; `audit_trail_integrity_verified` emitted (final event); audit storage realization shutdown returns

**Invariant preserved**: every emitted event is persisted in audit-trail BEFORE workspace shutdown completes. Audit storage available BEFORE substrate emits first architectural event AND audit storage shuts down AFTER substrate releases (boot-before-substrate / shutdown-after-substrate ordering per `arch/audit.md` §10).

### Logic placement modes (4-mode distribution)

Where actual framework logic lives, by interpretability:

| Mode | Layer | Examples |
|---|---|---|
| **Mode 1** Production-runtime LLM-MD | Operational (AI reads at runtime) | Skills / specialist DEFINITIONs / `workspace.md` / shape policy bundles / bausteine |
| **Mode 2** Production-runtime Python | Substrate-side | Substrate Instance impl / mechanism Python impls / adapter implementations / Pydantic validation |
| **Mode 3** Hybrid Phase 6 specs | Spec layer | Phase 6 spec files (Pydantic + companion docs) |
| **Mode 4** Development-time LLM-MD | Documentation (NOT production-runtime) | ARCHITECTURE.md / arch/* / DRs / MAINTENANCE.md / VISION / GLOSSARY / profiles / learnings / DISCIPLINES.md |

**Discipline implications**: Mode 1 = highest LLM-instruction tightness required; Mode 2 = standard Python (self-falsifying); Mode 4 = optimize for human readability, NOT production-runtime parsing.

**Anti-pattern**: encoding framework rules in Mode 4 intending production AI to "follow them" — that's the SQL-DB trap. Production AI follows Mode 1 markdown; Mode 4 is documentation, not runtime substrate.

### AI as runtime, not AI as consumer

When user names AI capability as *the mechanism* (not as a feature being added on), the architectural shape mirrors how Claude already operates: minimal structured skeleton (identity, cross-refs, persistence) + markdown body (semantics, rules, domain process) + AI reads at runtime.

**Do NOT add an "encoded rules" layer** — that's the SQL-DB trap in disguise. Memories work because Claude IS the runtime; same pattern applies to managed entities, specialist DEFINITIONs, doctype manifests.

- **Structured for**: interfaces / identity / persistence
- **Markdown for**: semantics / rules / domain process
- **AI is the runtime** that fuses them

### LLM-instruction tightness for Mode 1 markdown layer

LLMs paper over imprecise markdown by inference. That guessing is brittle / has overhead / drifts silently / compounds. Deterministic Python self-fails on wrong shapes; markdown doesn't.

**Asymmetric review effort follows**: heavier on Mode 1 markdown (skill instructions; specialist DEFINITIONs; workspace.md; shape policy bundles); lighter on Mode 2 Python.

**Bias toward sharpening** when: pre-launch / Mode 1/4 markdown / "LLM is inferring the right answer most of the time" (warning sign) / cross-layer coupling not made structural. **Bias toward feature-forward** when: deterministic Python / post-launch / instruction layer concrete + well-coupled.

### How topics compose

- **Mechanisms** are atomic interface contracts; primitives + protocols + axes COMPOSE WITH multiple mechanisms
- **Protocols** (Pattern A) bundle Surface + Implementations + Selection
- **Primitive clusters** group tightly-coupled primitives by composition
- **Cross-cutting integrators** (axis-interactions; scope-model) analyze composition across all prior topics
- **Composing relations** explicitly cross-referenced in each `arch/<topic>.md`

### Composability + boundaries (per G gate)

Every L1-L4 producer level (specialist / shape / template / workspace) must produce packageable artifacts that support multi-mode consumption. See `profiles/G-composability-gate.md`.

### Pattern-vs-instance discipline

Framework primitives stay shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer-instance specifics live at workspace level, NOT in framework primitive definitions. See `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 + `profiles/L5a-planner-pbs-schulz.md`.

## 7. Locked architectural decisions

Each lock = 1-line resolution + cross-ref to DR/GLOSSARY for full content.

### Quality-gate scope-lock (Phase 3.6 prerequisite) — LOCKED

**Resolution**: `quality-gate` re-classified to **Pattern A protocol with mechanism-shaped Surface**; per-axis-failure-mode signal catalog; per-shape implementation variation; fail-closed/open semantics per shape. Full detail: `GLOSSARY.md` quality-gate entry + `docs/decisions/quality-gate-scope-lock.md`.

### Workflow bipartite-classification (Phase 3.1) — LOCKED

**Resolution**: `workflow` re-classified to **bipartite Pattern B with optional applicability** — DEFINITION in specialist's distributable bundle (Framework C); INSTANCE = workflow_instance entity at Owner B; engages ONLY when work follows codified pattern (ad-hoc work first-class). Full detail: `GLOSSARY.md` workflow entry + `docs/decisions/workflow-bipartite-classification.md`.

### Work-unit bipartite-classification (Phase 3.1) — LOCKED

**Resolution**: `work-unit` re-classified to **bipartite Pattern B with always-present container** — KIND DEFINITION in specialist's distributable bundle; INSTANCE = work-unit instance at Owner B; every accountability-bearing piece of work IS a work-unit. Asymmetry vs workflow (always-present vs optional-overlay) is load-bearing. Full detail: `GLOSSARY.md` work-unit entry + `docs/decisions/work-unit-bipartite-classification.md`.

### Deployment definition (Phase 3.1) — LOCKED

**Resolution**: `deployment` locked as **DERIVED concept** = workspace-as-bound-runtime; 1:1 with workspace at framework primitive level; no independent structural content beyond workspace's runtime aspect. Full detail: `GLOSSARY.md` deployment entry + `docs/decisions/deployment-derived-classification.md`.

### Engaged-authorship operational definition (Phase 3.1) — LOCKED

**Resolution**: `engaged authorship` locked as **DERIVED axis-3 success mode** with two-phase composite: production-phase engagement (per-claim sparring participation) + attestation-phase engagement (per-claim attestation event); both independent + both must structurally complete; granularity per-claim per-version. Framework-level = PRESENCE (Y/N event-existence); shape-policy-level = QUALITY (depth signals via quality-gate). Full detail: `GLOSSARY.md` engaged authorship entry + `docs/decisions/engaged-authorship-operational-definition.md`.

### Substrate ARCH topic (Phase 3.4 first canonical) — LOCKED

**Resolution**: `arch/substrate.md` LOCKED as first canonical Pattern A protocol topic. Establishes 18-section template; 7 capability categories on Surface; Tri-aspect Pattern A (Surface + Implementations + Running Instance); per-impl extension Protocols pattern; substrate-internal vs skill-side audit emission dual paths. Full detail: `arch/substrate.md` + `docs/decisions/substrate-arch-topic.md`.

### Adapter ARCH topic (Phase 3.4 second Pattern A protocol) — LOCKED

**Resolution**: `arch/adapter.md` LOCKED. Validates 18-section template + introduces **two-layer Surface variation** (META-Surface conventions + per-integration-class Surfaces — 5 currently: Email / Accounting / MCP-Server / A2A-Peer / File-Sync). Multi-instance cardinality; hot-swap re-binding; per-class auth + lifecycle; per-shape audit + circuit-breaker policies. Full detail: `arch/adapter.md` + `docs/decisions/adapter-arch-topic.md`.

### Sparring ARCH topic (Phase 3.4 third — RECLASSIFIED mechanism class) — LOCKED

**Resolution**: `arch/sparring.md` LOCKED. 8 sub-mechanism capability categories (4 architecturally-encoded gate-dispatched + 4 behaviorally-enforced); per-shape activation matrix; sparring events ARE production-phase substrate for `engaged authorship` (axis-2 → axis-3 dependency); per-action audit emission via skill-side MCP gate. Full detail: `arch/sparring.md` + `docs/decisions/sparring-arch-topic.md`.

### Audit ARCH topic (Phase 3.4 fourth — RECLASSIFIED mechanism class) — LOCKED

**Resolution**: `arch/audit.md` LOCKED. 7 Surface capability categories (emission / persistence / query / integrity / event-kind catalog / state-rendering / cross-deployment external-format export); **audit-trail-as-canonical-source** (single-write architecture; state rendered FROM events; append-only); append-only enforced architecturally per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1; per-shape event-kind catalog; boot-before-substrate / shutdown-after-substrate ordering; hash-chain integrity; §14 Cross-shape policy variation (per shape-policy granularity / event-kind catalog / trust model / error semantics). Audit composes with authority-binding mechanism (independent framework primitive per TOP-LEVEL ARCHITECTURE concept-by-concept table); per-shape trust policy lives at shape-policy declaring trust model. Trust as Pattern A protocol CANCELLED per `docs/decisions/greenfield-rederivation-pause.md` Step 3. Full detail: `arch/audit.md` + `docs/decisions/audit-arch-topic.md`.

### Phase 3.1 closed

All 4 open architectural questions resolved. Coherence-audit ran at phase boundary; 0 architectural REVISIONS; 9 cascade-fix EXPANSIONS applied.

### Topic taxonomy (Phase 3.2 Sub-decision 1) — LOCKED

**Resolution**: 11 ARCH topics in protocol-centric aggregation with primitive-cluster topics. Foundation-up ordering. Under MAINTENANCE budget (15-20 cap) with headroom. Full topic list: §4 above. Composite DR: `docs/decisions/phase-3-2-doc-organization.md`.

### File naming convention (Phase 3.2 Sub-decision 2) — LOCKED

**Resolution**: Plain kebab-case slug = topic name; flat `arch/` directory; no prefixes; no sub-directories. Aggregation join uses hyphen. Cross-doc links use relative paths within arch/ + GitHub-flavored anchors. Minimal frontmatter (title; topic-cluster; status). NO `arch/README.md` — ARCHITECTURE.md is canonical entry point.

### Cross-cutting topics placement (Phase 3.2 Sub-decision 3) — LOCKED

**Resolution**: cross-cutting CONCERNS vs cross-cutting TOPICS distinction codified. TOPICS (dedicated `arch/<topic>.md`): axis-interactions / scope-model / quality-gate. CONCERNS (ARCHITECTURE.md sections): Pattern-A/B/C semantics / cascade direction / scope-categorization framing / foundation-up ordering / G+D gates / Logic placement modes. No content migration between MAINTENANCE.md and arch/scope-model.md (layer-distinction maintained).

### ARCHITECTURE.md overview structure (Phase 3.2 Sub-decision 4) — LOCKED

**Resolution**: 9-section structure (this doc). Foundation-up ordered for new-reader path. Audience + scope explicit (§1; Mode 4 placement). Logic placement modes codified (§6). Catalog uniformity (§4 one-liner depth). Locked-decisions section growth mitigation: each lock summary stays SHORT (resolution + cross-ref). Composite DR: `docs/decisions/phase-3-2-doc-organization.md`.

## 8. Disciplines applying to all ARCH work

Cross-refs to canonical sources; no duplicated content here.

### Validation gates (structural)

| Gate | Fires when | Blocks until |
|---|---|---|
| **G — Composability Gate** | Designing any L1-L4 producer artifact | Multi-mode consumption requirements satisfied |
| **D — Defer Gate** | AI considers deferring any architectural item | Mental modeling within profile grounding attempted |

Both STRUCTURAL — wrong shapes can't pass. Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1. Codified in `profiles/INDEX.md`. Decision-design-sharpening v0.6.0 references in Round 2 stress-test.

### Multi-axis validation

Per `DISCIPLINES.md` Discipline 3 (multi-axis sub-section). Validate primitive classifications across archetype / work-type-within-archetype / role; plus explicit non-coverage question.

### Profile-anchored validation

Per `decision-design-sharpening` v0.5.0+ + `profiles/INDEX.md` clusters. For high-impact decisions test against ≥3 of 4 profile-clusters (A Producers / B Deployers / C Consumers / D Validators). 17 profiles (2 full + 15 skeletons; on-demand fleshing).

### Audit scaling strategy

Per coherence-audit v0.3.0. Cluster compression (routine) / audit deltas (incremental) / on-demand fleshing (high-impact) / full systematic (RESERVED for phase boundaries). Don't default to full systematic.

### Other disciplines

- **Foundation-up workflow ordering** — per `DISCIPLINES.md` Discipline 8
- **2-round sweet spot** — per `DISCIPLINES.md` Discipline 3 + sharpen v0.9.0
- **Composite-decision decomposition** — per `decision-design-sharpening` v0.6.0 (emergent + upfront-known modes)
- **Cascade discipline** — per `MAINTENANCE.md`; UPSTREAM + DOWNSTREAM bidirectional; GLOSSARY back-check at Round 2 termination
- **Pattern-vs-instance** — per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2; no instance-leakage
- **AI-as-runtime hybrid-shape** — production AI follows Mode 1, not Mode 4
- **Provenance hygiene** — per coherence-audit Lens 5 v0.2.1; no audit-history breadcrumbs in canonical content; provenance lives in HANDOFF + git log + commit messages
- **Codify upfront vs wait-for-evidence** — per `learnings/ai-app-development.md` Observation 27; 5-question discriminator; when deferring, add detection mechanism

## 9. Watch-list (architectural items awaiting external evidence)

Per D gate + `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 no-defer principle.

| Watch-list item | Awaited signal | Resolution mechanism |
|---|---|---|
| Shape-neutrality validation for second-shape productization | Second-shape design begins (autonomous-business OR personal-OS) | Validate primitive framings + new shape's policies handle variations cleanly |
| Cross-specialist shared workflow patterns insufficient via Layer A | If Layer A growth proves insufficient for genuinely-cross-archetype pattern | Examine then; `workflow_pattern` framework primitive remains unwarranted by default |
| 3-tier REVISION/EXPANSION discriminator codification | ≥3 borderline classifications across consecutive decisions/audits OR user pushback OR cascade-work-lag | Detection mechanisms in place: self-check at decision-design-sharpening v0.6.0 Round 2 termination + coherence-audit v0.3.1 Step 7 |

See BACKLOG.md for actionable detail + Phase 4-6 forward work.

## Cross-references

- `MAINTENANCE.md` — 5-layer doc model + cascade discipline + TOP-LEVEL ARCHITECTURE
- `VISION.md` — three-axis thesis + falsification + foundations
- `GLOSSARY.md` — Layer 1 vocabulary (36 locked entries)
- `BACKLOG.md` — Phase 3 work-item tracker
- `HANDOFF.md` — session log
- `profiles/INDEX.md` — usage profiles + G + D gates + 4 profile clusters
- `docs/decisions/` — locked DRs
- `drafts/composability-tooling.md` — composability tooling concepts (Phase 5+ ROADMAP)
- `archive/INDEX.md` — v0.35 archived corpus
