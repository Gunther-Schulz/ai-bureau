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
| **3.5** | Per-primitive detail topics (4 primitive-cluster topics + 2 cross-cutting integrators) | CLOSED — ALL 6 of 6 ARCH topics LOCKED (specialist-skill + practitioner + workflow-work-unit + claim-defensibility + scope-model + axis-interactions); coherence-audit checkpoint C2 CLOSED 2026-05-04 per `disciplines/09-coherence-audit-cadence.md` cadence |
| **3.6** | Quality-gate ARCH topic | CLOSED — Pattern A 12+7 third instance LOCKED (FORMAL STABILITY achieved 3 of 3 Pattern A instances complete with this lock); resolves axis-interactions §7 E2 + §14 W4 forward-references |
| **3.7** | v1.x ARCH amendment candidates (non-sequential; post-thin-slice-lock per evidence triggers): PydanticAI substrate Implementations enumeration; framework-level RAG-engagement architecture HOW | Pending (non-sequential) |
| **3.8** | Coherence-audit checkpoint C3 (phase-boundary; ARCH-specific Lenses 11-15 activate) per `DISCIPLINES.md` Discipline 9 | Pending — C1 (post-3.4) CLOSED + C2 (post-3.5) CLOSED 2026-05-04 per cadence in `BACKLOG.md` Phase 3 audit-checkpoints |
| **6.1** | Specs + minimal reference impls (Mode 3 specs ~11 + Mode 2 reference impls thin-slice + stub MCP server backend + items 1-5 deployment-instance content + minimal Layer A) per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE | Pending |
| **6.2** | Production-grade infrastructure + extended impls (LanceDB stack + real Layer A domain + MS AF substrate + extended adapter classes + extended shape gates) per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE | Pending |

Foundation-up ordering applied (per `DISCIPLINES.md` Discipline 8): questions before structure before content before audit.

## 3. Doc structure (Phase 3.0 LOCKED)

**Hybrid**: single overview + per-topic files.

| Doc | Purpose | Lines | Status |
|---|---|---|---|
| `ARCHITECTURE.md` (this file) | Overview + topic catalog + cross-cutting principles + Phase 3 status | ~350 target | Active |
| `arch/<topic-slug>.md` × 11 | Per-topic detail | ~500 each | Active (11 of 11 LOCKED: substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility / scope-model / axis-interactions / quality-gate) |

**Why hybrid**: pure-single (10K lines) is unwieldy + context-budget concern; pure-multi has no entry point + cross-cutting orphaning. Hybrid aligns with progressive-disclosure principle (skill-craft pattern: SKILL.md → PROCEDURE.md → references/).

## 4. Topic catalog (Phase 3.2 LOCKED — 11 topics)

11 ARCH topics in protocol-centric aggregation with primitive-cluster topics. Foundation-up ordered. Per Phase 3.2 Sub-decision 1 lock + greenfield-rederivation cascade (per `docs/decisions/greenfield-rederivation-pause.md` Step 3); filenames per Sub-decision 2 lock.

| # | Topic file | Primary content (one-liner) | Phase |
|---|---|---|---|
| 1 | `arch/substrate.md` | Substrate Protocol Surface + per-impl + persistent-state + session interaction; subsumes Coordination (hooks + event-bus) + Time (temporal semantics per impl) | 3.4 — DRAFTED |
| 2 | `arch/adapter.md` | Adapter Protocol Surface (META + per-integration-class) + per-impl + lifecycle/auth; subsumes Time (time-driven adapter operations) | 3.4 — DRAFTED |
| 3 | `arch/sparring.md` | Sparring **mechanism class** (RECLASSIFIED — not Pattern A): 8 sub-mechanism contracts + per-shape policy declares which active + how-enforced | 3.4 — DRAFTED |
| 4 | `arch/audit.md` | Audit **mechanism class** (RECLASSIFIED — not Pattern A): AuditEvent schema = mechanism Surface + per-shape granularity policy + substrate-mediated storage backend; subsumes Trust (authority-binding + per-shape trust policy) | 3.4 — DRAFTED |
| 5 | `arch/quality-gate.md` | Quality-gate Pattern A Surface + per-shape implementations + signal catalog | 3.6 — DRAFTED |
| 6 | `arch/specialist-skill.md` | Specialist DEFINITION + skill granularity + bundle structure + marketplace | 3.5 |
| 7 | `arch/practitioner.md` | Practitioner Pattern C bipartite + record placement + multi-practitioner | 3.5 |
| 8 | `arch/workflow-work-unit.md` | Workflow Pattern B + work-unit Pattern B + workflow_instance state machine + orchestration | 3.5 |
| 9 | `arch/claim-defensibility.md` | Claim primitive + defensibility test + source-grounding + engaged-authorship + per-claim attestation | 3.5 |
| 10 | `arch/scope-model.md` | Workspace + Framework C / Owner B / Layer A scope categories + entity placement | 3.5 — DRAFTED |
| 11 | `arch/axis-interactions.md` | 3 VISION axes interaction + co-worker frame + category-collapse cross-axis force | 3.5 — DRAFTED |

**Cancelled topics** (per `docs/decisions/greenfield-rederivation-pause.md` Step 3): `arch/coordination.md`, `arch/trust.md`, `arch/time.md` — never written; subsumed into substrate/audit/adapter. Saves ~1500 lines of un-written ARCH content.

**Aggregation discipline**: aggregate when items tightly coupled OR individually <100 lines (per coherence-audit Lens 15). Each topic targets ~500 lines avg; per-topic flex acceptable.

**Foundation-up dependency**: topics 1-2 are Pattern A protocols (foundational mechanism layer); 3-4 are mechanism-class topics (per-shape policy variation, not Pattern A); 5 quality-gate Pattern A composes with all axes (Phase 3.6); 6-9 are primitive clusters; 10-11 are cross-cutting integrators (load LAST).

**Phase 3.7 ARCH amendments / follow-ups excluded from topic catalog** (concrete amendment candidates that compose with locked topics, not new topic-shaped items): PydanticAI substrate Implementations enumeration / Framework-level RAG-engagement architecture HOW.

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
9. **gate-phase 1**: Quality-gate Implementation instantiates per shape policy bundle declaration (`gate = await ChosenGate.from_shape_policy(shape_policy)`)
10. **gate-phase 2**: Quality-gate state-restore from audit-trail (stateful impls reads prior `gate_state_persisted` events via audit Surface §C; reconstructs cumulative engagement signals; emits `gate_state_restored` upon completion per `arch/quality-gate.md` §10)
11. **gate-phase 3**: Quality-gate registers checkpoint-firing handlers (subscribes to per-axis observability hooks per `arch/axis-interactions.md` §7 + `arch/quality-gate.md` §2 capability category B)
12. **gate-phase 4**: `gate_active` event emitted via audit Surface; quality-gate ready to fire at workspace runtime checkpoints

**Shutdown composite ordering** (reverse with explicit flush-before-release invariants):

1. Substrate shutdown initiates: `shutdown_initiated` event emitted via audit Surface
2. In-flight agent runs drain to completion OR cancel per cancellation policy
3. Substrate stops accepting new run_agent calls
4. Adapter bindings shut down in REVERSE declaration order (per `arch/adapter.md` §10 per-instance shutdown); per-binding drains in-flight operations + flushes auth tokens / circuit state / threading caches; per-binding `adapter_stopped` events emitted
5. MCP servers stop (subprocess MCP servers gracefully terminate)
6. Substrate releases substrate-internal runtime resources; `shutdown_complete` event emitted via audit Surface
7. Quality-gate emits final drift report event; stateful impls flush cumulative engagement signals via `gate_state_persisted` event emission to audit Surface §A; quality-gate unsubscribes from observability hooks per `arch/quality-gate.md` §10
8. Sparring (mechanism class peer) emissions drain; final events emit via audit Surface
9. Audit storage realization shutdown LAST (per `arch/audit.md` §10 shutdown steps 5-8): substrate-impl drains pending audit-trail writes; flushes audit-trail to storage; verifies hash-chain integrity; `audit_trail_integrity_verified` emitted (final event); audit storage realization shutdown returns

**Invariant preserved**: every emitted event is persisted in audit-trail BEFORE workspace shutdown completes. Audit storage available BEFORE substrate emits first architectural event AND audit storage shuts down AFTER substrate releases (boot-before-substrate / shutdown-after-substrate ordering per `arch/audit.md` §10). **Quality-gate runs AFTER substrate is fully ready (consumes per-axis observability requiring all 3 axes operational) AND shuts down BEFORE audit storage realization (gate-state-persistence emissions must reach audit-trail before storage shuts down) per `arch/quality-gate.md` §10**.

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

**Resolution**: `arch/substrate.md` LOCKED as first canonical Pattern A protocol topic. Establishes 12+7-section template (12 common-required + 7 protocol-specific-conditional per `MAINTENANCE.md` Pattern A / mechanism-class topic template); 7 capability categories on Surface; Tri-aspect Pattern A (Surface + Implementations + Running Instance); per-impl extension Protocols pattern; substrate-internal vs skill-side audit emission dual paths. Full detail: `arch/substrate.md` + `docs/decisions/substrate-arch-topic.md`.

### Adapter ARCH topic (Phase 3.4 second Pattern A protocol) — LOCKED

**Resolution**: `arch/adapter.md` LOCKED. Validates 12+7-section template + introduces **two-layer Surface variation** (META-Surface conventions + per-integration-class Surfaces — 5 currently: Email / Accounting / MCP-Server / A2A-Peer / File-Sync). Multi-instance cardinality; hot-swap re-binding; per-class auth + lifecycle; per-shape audit + circuit-breaker policies; §14 Cross-shape policy variation applies per shape-policy-mediated nature. Full detail: `arch/adapter.md` + `docs/decisions/adapter-arch-topic.md`.

### Sparring ARCH topic (Phase 3.4 third — RECLASSIFIED mechanism class) — LOCKED

**Resolution**: `arch/sparring.md` LOCKED. 8 sub-mechanism capability categories (4 architecturally-encoded gate-dispatched + 4 behaviorally-enforced); per-shape activation matrix; sparring events ARE production-phase substrate for `engaged authorship` (axis-2 → axis-3 dependency); per-action audit emission via skill-side MCP gate. Full detail: `arch/sparring.md` + `docs/decisions/sparring-arch-topic.md`.

### Audit ARCH topic (Phase 3.4 fourth — RECLASSIFIED mechanism class) — LOCKED

**Resolution**: `arch/audit.md` LOCKED. 7 Surface capability categories (emission / persistence / query / integrity / event-kind catalog / state-rendering / cross-deployment external-format export); **audit-trail-as-canonical-source** (single-write architecture; state rendered FROM events; append-only); append-only enforced architecturally per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1; per-shape event-kind catalog; boot-before-substrate / shutdown-after-substrate ordering; hash-chain integrity; §14 Cross-shape policy variation (per shape-policy granularity / event-kind catalog / trust model / error semantics). Audit composes with authority-binding mechanism (independent framework primitive per TOP-LEVEL ARCHITECTURE concept-by-concept table); per-shape trust policy lives at shape-policy declaring trust model. Trust as Pattern A protocol CANCELLED per `docs/decisions/greenfield-rederivation-pause.md` Step 3. Full detail: `arch/audit.md` + `docs/decisions/audit-arch-topic.md`.

### Specialist-skill ARCH topic (Phase 3.5 first primitive-cluster) — LOCKED

**Resolution**: `arch/specialist-skill.md` LOCKED as first canonical primitive-cluster ARCH topic. Anchors **12+5 primitive-cluster topic template** (12 common-required + 5 cluster-conditional per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template subsection); 6 sub-decisions per Mode 2 upfront-known composite decomposition. Specialist DEFINITION as Framework C bundle (manifest schema enumerated; specialist-namespace mechanic for work-unit kinds + workflow definitions per per-specialist scoping). Skill atomic structure + substrate Surface §G integration + mid-session hot-activation re-binding semantics. Cross-specialist composition rules (skill invocation via `specialist-name:skill-name`; cross-specialist entity reads permitted; entity writes prohibited at framework level). Specialist + skill granularity 3-tests + two-tier classification (domain-anchored vs cross-archetype). Marketplace deferred per W1; destruction semantics archival-as-default per axis-3 reasoning. Composes with substrate Surface §G + §C + §D + audit Surface + adapter + claim primitive + authority-binding mechanism. Full detail: `arch/specialist-skill.md` + `docs/decisions/specialist-skill-arch-topic.md`.

### Practitioner ARCH topic (Phase 3.5 second primitive-cluster) — LOCKED

**Resolution**: `arch/practitioner.md` LOCKED as second canonical primitive-cluster ARCH topic. Anchors **Pattern C topic-template-class** (12+5 primitive-cluster template extends to Pattern C without variation; per-pattern conditional applicability rules surfaced — §8 cross-shape policy variation + §13 per-primitive lifecycle ordering APPLY; §9 granularity / §10 bundle / §11 marketplace N/A documented explicitly; §12 N/A-parity preserved). Bipartite Pattern C: HUMAN aspect cross-cutting (the natural person bearing legal/professional accountability in the world; not "placed" in any scope) + practitioner-RECORD aspect at Owner B (workspace-scope managed entity carrying identity / credentials / signing authority / role bindings via 11-field manifest schema). Multi-practitioner cardinality matrix per shape (solo = 1; partnership = N; legal-entity-firm = N under firm context); legal-entity workspace context placement at WORKSPACE level NOT practitioner level (workspace.md `legal_entity_context` block; practitioner-RECORD `firm_binding` references back). Lifecycle 4-event-kind catalog (`practitioner_record_minted` / `_updated` with `details.changed_fields` / `_deactivated` / `_reactivated`); deactivation = dormant-not-deleted per axis-3 defensibility-critical preservation rule; archival-as-default destruction on workspace dissolution per cross-pattern coherence with `arch/specialist-skill.md` §13. Cross-axis composition: axis-1 co-worker (practitioner is human side of co-worker pairing) / axis-2 sparring engagement subject (sparring fires AT practitioner judgment moments via AI-runtime sparring-partner) / axis-3 authorship preservation ROLE protected (defensibility resolves at practitioner-author granularity). Per-shape trust model parameterizes practitioner-record's accountability surface per `arch/audit.md` §14 (practitioner-judgment / budget-policy / individual). W1-W4 watch-list (multi-tenant federation / Identity-class adapter Surface candidate per `arch/adapter.md` §3 6th-class / cryptographic signing per `arch/audit.md` §D / cross-practitioner workflow handoff). Composes with substrate Surface §C + audit Surface §A/§C + adapter (W2 Identity-class candidate) + sparring + specialist-skill (cross-specialist activation actor binding back-link) + authority-binding mechanism. Mode 2 upfront-known composite decomposition (5 sub-decisions covering template + bipartite + manifest schema + multi-practitioner + legal-entity + lifecycle + archival + authority-binding cross-axis + W1-W4). Full detail: `arch/practitioner.md` + `docs/decisions/practitioner-arch-topic.md`.

### Workflow + work-unit ARCH topic (Phase 3.5 third primitive-cluster) — LOCKED

**Resolution**: `arch/workflow-work-unit.md` LOCKED as third canonical primitive-cluster ARCH topic. Anchors **two-Pattern-B topic-template-class** (12+5 primitive-cluster template extends WITHOUT variation; per-pattern conditional applicability rules surfaced — §8 cross-shape policy variation + §9 granularity tests + §13 per-primitive lifecycle ordering APPLY; §10 bundle / §11 marketplace N/A documented explicitly per workflow + work-unit are bundled IN specialist not bundlers themselves; §12 N/A-parity preserved — 18 sections / 482 lines). Bipartite-pair structural overview: workflow DEFINITION at Framework C via specialist's bundle (optional structural overlay per `glossary/workflow.md`) + workflow_instance at Owner B + work-unit KIND DEFINITION at Framework C via specialist's bundle (always-present container per `glossary/work-unit.md`) + work-unit instance at Owner B. Always-present asymmetry load-bearing (every accountability-bearing work IS a work-unit; workflow_instance optional overlay). Cardinality asymmetry: 1 work-unit per workflow_instance; N workflow_instances per work-unit (potentially across specialists). Ad-hoc work first-class (carried by session + work-unit + skill + claim + event without workflow_instance). Snapshot pattern at creation (workflow `definition_snapshot` + work-unit `kind_snapshot`; preserves defensibility under specialist version bumps mid-instance-lifetime). Cross-specialist composition rules: cross-specialist work-unit READ permitted; ownership mutation PROHIBITED structural per axis-3 (per `arch/specialist-skill.md` §10 + workflow-work-unit §3). Two state machines: workflow_instance 5-state (`running` | `suspended` | `completed` | `abandoned` | `failed`) + work-unit instance 5-state default per kind (`initiated` → `in-progress` → `completed` | `sent` | `archived`) with per-kind extensible state machine. Per-shape policy variation 6-row matrix (multi-practitioner authorship / workflow_instance flexibility / audit emission granularity / authority-binding requirements / per-kind structural conventions / archival semantics). 8-category error catalog (workflow_instance + work-unit instance lifecycle errors). W1-W4 watch-list (workflow_pattern primitive vs Layer A reusable templates / cross-practitioner workflow handoff mechanics composes with `arch/practitioner.md` W4 / per-kind structural conventions schema standardization / multi-workflow_instance phase choreography mechanics). Composes with substrate Surface §C/§F + audit Surface §A/§C + adapter + sparring + specialist-skill (cross-specialist work-unit attachment + boot integration step 9) + practitioner (session-binding + attribution chain) + authority-binding mechanism. Cross-axis composition: axis-1 PRIMARY anchor for workflow (workflow is what intertwined AI intertwines WITH per VISION) + axis-1 cross-axis for work-unit (artifact-container all axes operate against) + axis-2 sparring orthogonal (sparring fires DURING workflow_instance phase progression AND ad-hoc work-unit progression) + axis-3 work-unit attribution chain (defensibility resolves through work-unit + claim attribution chain). Mode 2 upfront-known composite decomposition (6 sub-decisions covering template + 4-sub-section structural overview + 4 manifest schemas + within-cluster composition + snapshot pattern + lifecycle ordering + cross-pattern destruction + orphan handling + boot integration + two granularity 3-tests subordinate to specialist 3-test + cross-shape policy variation + cross-axis composition + W1-W4 watch-list). Full detail: `arch/workflow-work-unit.md` + `docs/decisions/workflow-work-unit-arch-topic.md`.

### Claim + defensibility ARCH topic (Phase 3.5 fourth primitive-cluster) — LOCKED

**Resolution**: `arch/claim-defensibility.md` LOCKED as fourth canonical primitive-cluster ARCH topic. Anchors **PRIMITIVE+DERIVED topic-template-class** (12+5 primitive-cluster template extends WITHOUT variation; per-pattern conditional applicability rules surfaced — §8 cross-shape policy variation + §9 granularity tests + §13 per-primitive lifecycle ordering APPLY; §10 bundle / §11 marketplace N/A documented explicitly per claim is content-unit IN work-unit not bundler + defensibility is property/test not entity-having; §12 N/A-parity preserved = 18 sections / 422 lines). Bipartite per-primitive 2-sub-section structural overview (NO manifest schemas — claim isn't Framework C bundle; defensibility isn't entity): claim PRIMITIVE 4-property structure (atomic + accountability-bearing + judgment-bearing + source-grounded) + claim-event composition + revision per-version semantics + production / revision / finalization moments; defensibility DERIVED 3-condition operational test (engaged-authorship Cond #1 + reconstructible-reasoning-chain Cond #2 + source-grounded Cond #3) + claim-granularity resolution + composability + Q1-Q4 boundary tests + re-run-ability via audit-trail reconstruction. 4 within-cluster commitments: reciprocal asymmetry (defensibility-tests-claims, never claims-bundle-defensibility; one-way directional composition) + composability-of-defensibility-test (per-claim defensibility composes work-unit defensibility; ONE indefensible claim taints output) + per-claim attestation chain mechanics (6-step ordered emissions: claim_made → production-phase engaged-authorship sparring events → revision events → finalization → per-claim attestation event → composition INTO work-unit attribution chain) + pre-existing-claim ingestion semantics (load-bearing within-cluster commitment for legacy-claim import; resolution mechanics in `arch/claim-defensibility.md` §3 + W2 watch-list). Engaged-authorship cross-cluster composition (DERIVED entry's 2-phase test composes WITHIN claim-defensibility cluster as defensibility Cond #1 operational definition; engaged-authorship lives at GLOSSARY but operational mechanics compose INTO this cluster). Per-shape policy variation 6-row matrix (claim-emission audit granularity / engaged-authorship enforcement / per-claim source-grounding strictness / attestation-event mandatoriness / quality-gate signal-set / cross-deployment claim portability all shape-policy-mediated per `arch/audit.md` §14 + engaged-authorship DR Framework-level enforcement). 6-event-kind catalog candidate (`claim_made` / `claim_revised` / `claim_finalized` / `claim_attested` / `claim_re_attested` / `defensibility_test_run`; Phase 6 audit-emission catalog territory). Cross-pattern destruction inheritance (claims inherit work-unit's `instance_content_dissolution_policy` per cross-pattern coherence with `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13 + `arch/workflow-work-unit.md` §13 archival-as-default). Cross-axis composition: axis-3 PRIMARY anchor (claim is unit-of-defense; defensibility IS axis-3 success criterion test) + axis-2 sparring orthogonal at claim granularity + axis-1 cross-axis (claims are content-units AI co-authors with practitioner). W1-W4 watch-list (per-claim-kind variation schema / pre-existing-claim ingestion semantics resolution / multi-practitioner co-attestation mechanics / cryptographic signing per claim). Composes with substrate Surface §F session/context cross-deployment + §G specialist registration + §C permission flow at HITL approval moments + audit Surface §A emission API + §B append-only persistence + §C query API + §D integrity verification + §10 boot ordering + §14 cross-shape policy variation + adapter (cross-deployment claim portability) + sparring Surface §D (production-phase substrate for engaged-authorship Cond #1) + specialist-skill (skills produce claims per §4 composition table) + practitioner (cross-axis attribution chain via per-claim attestation event records `actor_kind: human` + practitioner-RECORD identity per `arch/practitioner.md` §4) + workflow-work-unit (claim is content-unit IN work-unit; per-claim attestation chain composes INTO work-unit attribution chain per `arch/workflow-work-unit.md` §3 + §4) + engaged-authorship DERIVED (Cond #1 cross-cluster) + authority-binding mechanism (per-claim author attribution chain composes through skill identifier → specialist → workspace; reconstructible attribution chain is precondition for defensibility Cond #2). Mode 2 upfront-known composite decomposition (6 sub-decisions covering template + per-primitive 2-sub-section structural overview + within-cluster composition + cross-cluster engaged-authorship + outside-cluster framework primitives composition + cardinality + lifecycle ordering + 6-event-kind catalog candidate + cross-pattern destruction + boot integration + granularity tests with claim 3-test SUBORDINATE to work-unit kind 3-test + defensibility resolution-granularity test + two-tier classification N/A + cross-shape policy variation 6-row matrix + cross-axis composition + W1-W4 watch-list). Full detail: `arch/claim-defensibility.md` + `docs/decisions/claim-defensibility-arch-topic.md`.

### Scope-model ARCH topic (Phase 3.5 fifth ARCH topic; first cross-cutting integrator) — LOCKED

**Resolution**: `arch/scope-model.md` LOCKED as fifth canonical Phase 3.5 ARCH topic + first cross-cutting integrator. Anchors **cross-cutting integrator topic-template-class** (12+5 primitive-cluster template extends WITHOUT variation; per-pattern conditional applicability rules surfaced — §8 cross-shape policy variation APPLIES (engagement-target Owner B managed entities shape-policy-mandated per `glossary/owner-b-scope.md`); §9 granularity tests / §10 bundle composition / §11 marketplace + distribution / §13 per-element lifecycle ordering N/A documented (cross-cutting integrators have no granularity-test / bundle / marketplace / per-element lifecycle-ordering surface — those concerns live in respective primitive-cluster + Pattern A topics whose entities ARE placed across scopes); §12 N/A-parity preserved = 18 sections / 442 lines). Per-scope structural overview (3 sub-sections — Framework C / Owner B / Layer A) articulating each scope structurally without duplicating MAINTENANCE.md TOP-LEVEL ARCHITECTURE (per Phase 3.2 Sub-decision 3 LOCK no content migration). Workspace integration as cross-scope composition WITHIN cluster (workspace IS the central Owner B instance + container binding all three scopes; workspace.shape + workspace.substrate + workspace.specialists_active select Framework C definitions; workspace contains Owner B instances; workspace.scope.{domains, states} resolves Layer A content; 1:1 reciprocal with deployment per `glossary/deployment.md`; workspace boot integration with composite boot sequence per `ARCHITECTURE.md` §6 — scope-categorization realization fires INSIDE substrate-phase 1-5 envelope per E1). 4 NEW load-bearing patterns surfaced through scope-model articulation: E2 nested-bundle pattern (specialist Framework C bundle nests skill / workflow / work-unit-kind / adapter Implementations under specialist-namespace); E3 content-unit-IN-instance pattern (claim INHERITS work-unit's Owner B placement; NOT separately scoped); E4 cross-cutting non-placed pattern (defensibility / engaged-authorship / category-collapse / VISION axes / co-worker / failure modes / HUMAN practitioner aspect NOT placed; manifest through behavior of placed entities); E5 authority-binding placement pattern (mechanism dual-aspect: Framework C definition + Owner B event recording on `actor_kind`; same shape as substrate Surface + Implementations + audit AuditEvent schema). Per-primitive composition narrative + per-primitive composition table covering all 8 already-locked primitive surfaces (substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility) + foundational meta-primitives + cross-cutting derivatives. Per-scope cardinality + lifecycle (Framework C distributable lifecycle + Owner B workspace-lifetime + Layer A content-versioning). Per-element Mode distribution within scopes (Mode 1 / Mode 2 / Mode 4 mapping per scope category; THIS topic Mode 4 development-time documentation). Cross-shape policy variation 6-row matrix (engagement-target Owner B managed entity catalog per shape + workspace.md required fields per shape + workspace-scope managed entity universals + shape-extensions per shape + Layer A scope configuration defaults per shape + specialists_active recommended set per shape + substrate selection constraints per shape). Cross-axis composition (axis-1 workspace IS container for AI-co-worker intertwining + axis-2 sparring events captured at Owner B + axis-3 defensibility resolves at claim/work-unit granularity at Owner B). W1-W4 watch-list (multi-tenant federation cross-link to `arch/practitioner.md` W1 + cross-deployment claim portability cross-link to `arch/claim-defensibility.md` W2 + `arch/substrate.md` §F + workspace identity persistence schema Phase 6 spec cross-link to `arch/practitioner.md` W3 + `arch/audit.md` §D + `arch/claim-defensibility.md` W4 + engagement-target entity catalog per second-shape productization cross-link to BACKLOG shape-neutrality watch-list). Mode 2 upfront-known composite decomposition (6 sub-decisions covering cross-cutting integrator template structure + per-scope structural overview + workspace placement integration + cross-scope composition + per-primitive composition table + per-shape policy variation + cross-axis composition + W1-W4 watch-list + cross-references). Closes 5 of 6 Phase 3.5 ARCH topics; 1 cross-cutting integrator remains (axis-interactions Phase 3.5 sixth + final). Full detail: `arch/scope-model.md` + `docs/decisions/scope-model-arch-topic.md`.

### Axis-interactions ARCH topic (Phase 3.5 sixth + final ARCH topic; second cross-cutting integrator) — LOCKED

**Resolution**: `arch/axis-interactions.md` LOCKED as sixth + final canonical Phase 3.5 ARCH topic + second cross-cutting integrator. Extends **cross-cutting integrator topic-template-class** anchored at `arch/scope-model.md` WITHOUT variation (12+5 primitive-cluster template; §8 cross-shape policy variation APPLIES per cross-axis activation matrix shape-policy-mediated; §9 granularity / §10 bundle / §11 marketplace / §13 per-element lifecycle ordering N/A documented per cross-cutting integrator pattern; §12 N/A-parity preserved = 18 sections / 372 lines). **Cross-cutting integrator topic-template-class FORMAL STABILITY achieved with second instance lock** (12+5 extends WITHOUT variation across both scope-model anchor + axis-interactions instance per per-pattern instance-driven trigger pattern; 2 of 2 cross-cutting integrator instances complete with Phase 3.5 close). Per-axis structural overview (3 sub-sections — axis-1 intertwining + axis-2 sparring + axis-3 authorship-preservation) articulating each axis structurally without duplicating VISION axis-bodies. Cross-axis composition WITHIN cluster: 3 pairwise composition relationships (sparring fires WITHIN intertwined co-work / defensibility resolves AT axis-1 work-products / sparring events ARE production-phase substrate for engaged-authorship Cond #1) + 1 triple integration (intertwined sparring partnership in service of defensible authorship per VISION line 43) + asymmetric composition (axis-1 FOUNDATIONAL substrate for axes 2+3 / axis-2 OPERATIONAL within axis-1 / axis-3 EVALUATIVE about axes 1+2 OUTPUTS) + **CC-1 cross-axis failure cascade pattern** (load-bearing structural commitment: axis-1 failure forecloses axes 2+3 / axis-2 failure cascades to axis-3 production-phase / axis-3 attestation-phase failure INDEPENDENTLY possible) + E1 cross-axis composite boot integration (audit-phase 1-3 axis-3 evidence ready BEFORE substrate-phase 1-5 axes 1+2 activate per `ARCHITECTURE.md` §6 composite boot subsection) + E6 per-claim cross-axis lifecycle composition (production-phase axis-2 sparring events MUST precede axis-3 attestation event for engaged-authorship Cond #1; per claim per version). 14 EXPANSIONS across Round 1 (sub-decision-batched 7 EXPANSIONS) + Round 2 (8 surfacing operations: E1 boot integration + E2 observability hooks + E3 governance + E4 cross-axis errors + E5 falsification schema + E6 per-claim lifecycle + CC-1 + per-pattern stability confirmation). Per-primitive narrative + per-primitive composition table covering all 9 already-locked primitive surfaces (substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility / scope-model) + co-worker frame as cross-axis vocabulary per §4.2 + category-collapse as cross-axis force per §4.3 (per-axis manifestations: axis-1 collapse to "AI feature catalog" / axis-2 collapse to "answer machine" / axis-3 collapse to "rubber-stamp signing"; quality-gate Pattern A as architectural counter-mechanism LOCKED Phase 3.6 per `arch/quality-gate.md`) + E3 cross-axis governance integration + cross-axis attribution chain. Per-axis cardinality + lifecycle (3 anchored VISION axes; per-axis activation per workspace shape-policy-mediated; per-axis falsification per VISION §Falsification criteria). Per-element Mode distribution (VISION axes Mode 4; per-axis primitive content lives in respective ARCH topics in respective Modes 1+2+3+4). Cross-shape policy variation 6-row matrix (axis-1 intertwining depth + axis-2 sparring activation matrix + axis-3 engaged-authorship enforcement + per-shape failure-mode salience + per-shape category-collapse vulnerability + axes-served per shape across practitioner-shape / autonomous-business-shape / research-lab-shape / personal-OS-shape). Per-axis falsification criteria. W1-W4 watch-list (shape-neutrality validation cross-axis re-mapping per shape cross-link to BACKLOG shape-neutrality watch-list + `arch/scope-model.md` §14 W4 / VISION update triggers per-axis empirical signal accumulation cross-link to `VISION.md` §Falsification criteria / cross-deployment cross-axis composition patterns cross-link to `arch/claim-defensibility.md` §14 W2 + `arch/scope-model.md` §14 W2 + `arch/substrate.md` §F / quality-gate cross-axis signal-set integration Phase 3.6 cross-link to `arch/quality-gate.md`). Mode 2 upfront-known composite decomposition (6 sub-decisions covering cross-cutting integrator template extension + per-axis structural overview + cross-axis composition WITHIN cluster + cross-axis failure cascade pattern + composition with framework primitives outside cluster + per-primitive axis-anchoring catalog + co-worker frame + category-collapse + cross-axis governance integration + cross-shape cross-axis policy variation + falsification criteria + W1-W4 watch-list + cross-references). **Closes Phase 3.5** (6 of 6 ARCH topics LOCKED); unblocks Coherence-audit C2 post-Phase-3.5 close per `disciplines/09-coherence-audit-cadence.md` cadence. Full detail: `arch/axis-interactions.md` + `docs/decisions/axis-interactions-arch-topic.md`.

### Quality-gate ARCH topic (Phase 3.6; Pattern A 12+7 third instance) — LOCKED

**Resolution**: `arch/quality-gate.md` LOCKED as third canonical Pattern A protocol topic. Pattern A 12+7 template extends WITHOUT variation per per-pattern instance-driven trigger pattern (12 common-required + 7 conditional; per-pattern conditional applicability: §3 + §8 + §12 N/A documented + §10 boot/shutdown phase ordering + §11 substrate error categories + §13 deployment-tier awareness + §14 cross-shape policy variation APPLIES = 4 APPLIES + 3 N/A documented = 19 numbered §-headers / 410 lines). **Pattern A 12+7 topic-template-class FORMAL STABILITY achieved with third instance lock** (12+7 extends WITHOUT variation across substrate anchor + adapter + quality-gate; 3 of 3 Pattern A instances complete with Phase 3.6 close). Single-layer mechanism-shaped Surface with 6 capability categories: Checkpoint firing API (two-class checkpoint_kind taxonomy: event-triggered pre_send / pre_claim_finalization / pre_decision_lock / per_edit / workflow_phase_transition / session_end; periodic/threshold-triggered drift_audit) + Per-axis signal ingestion (per-axis-failure-mode signal catalog: axis-1 tacked-on/workflow-bypass/co-work-vs-transactional; axis-2 oracle/validator/answer-machine extraction patterns/sparring-bypass/counter-argument acceptance/engagement-depth; axis-3 rubber-stamping/engagement-depth-production/reasoning-chain-reconstructability) + Signal evaluation (engagement-quality verdict; per-shape thresholds + evaluation logic) + Intervention dispatch (intervention_kind ∈ {friction / nudge / block / audit_only}; block via substrate Surface §C `request_permission`; friction + nudge skill-side direct emission; authority-binding records `actor_kind: ai_runtime`) + Audit emission (gate-fired events via audit Surface §A; 6 candidate event-kinds: gate_fired / gate_intervention_applied / gate_threshold_crossed / gate_state_persisted / gate_state_restored / gate_active) + State management (audit-trail-as-state-store reframe: stateful impls render state FROM events via audit Surface §C query API; `gate.set_state()` is `gate_state_persisted` emission via Surface §A; NO separate gate-state-store; preserves single-write architecture per `arch/audit.md` §10 audit-trail-as-canonical-source). Per-implementation aspect: 3 concrete impls + extensible (practitioner-shape-gate fail-closed stateful + autonomous-business-shape-gate fail-open with alert stateless + personal-OS-shape-gate fail-open stateful lightweight; research-lab-shape-gate at second-shape productization per W1). Selection mechanics: shape-mediated NOT direct workspace.md selection (workspace selects shape via `workspace.md` `shape:` field; transitive gate-impl selection through shape policy bundle declaration; 1:1 cardinality 1 active gate impl per workspace). Tri-aspect reconciliation: Surface + Implementations + Running Instance; gate-coupling impossible-by-construction at Surface level via Phase 6 per-shape Extension Protocol isinstance check. Boot/shutdown ordering: gate-phase 1-4 fires AFTER substrate-phase 5 `boot_complete` (gate consumes per-axis observability requiring all 3 axes operational) + gate-shutdown 1-4 fires AFTER substrate releases BEFORE audit storage realization shutdown (gate-state-persistence emissions must reach audit-trail before storage shuts down); composite sequence amendment per `ARCHITECTURE.md` §6 Workspace boot + shutdown composite sequence subsection. Cross-axis dependency: gate consumes per-axis observability hooks per `arch/axis-interactions.md` §7 (per-axis observability hook signal-set) + §14 W4 (quality-gate cross-axis signal-set integration); resolves both forward-references. Per-shape error semantics: practitioner-shape-gate fail-closed (defensibility-critical) + autonomous-business-shape-gate fail-open with alert (continuity prioritized) + personal-OS-shape-gate fail-open (lightweight). 6 architectural error categories: GateUnreachable / SignalIngestionFailure / SignalEvaluationFailure / InterventionDispatchFailure / GateStateRestoreFailure / EventEmissionFailure. Deployment-tier awareness: Tier 1 local full enforcement default + advisory-mode candidate; Tier 2 cloud full enforcement multi-tenant gate state via session_id+actor_id discrimination; Tier 3 federated per-tenant isolation strict + W3 cross-deployment portability cross-link. Cross-shape policy variation 6-row matrix (parallel to scope-model §8 + axis-interactions §8 + claim-defensibility §8 + workflow-work-unit §8 6-row precedents): gate firing checkpoints + per-axis signal thresholds + intervention mechanics + error semantics + state management + per-shape failure-mode salience all per-shape variation across practitioner-shape / autonomous-business-shape / research-lab-shape (preliminary) / personal-OS-shape. Cross-axis composition: quality-gate Pattern A IS architectural counter-mechanism for category-collapse cross-axis force per `arch/axis-interactions.md` §4.3; per-axis observability hook signal-set integration per axis-interactions §7. Composes with all 9 prior locked Phase 3.4 + 3.5 ARCH topics + scope-model + axis-interactions cross-cutting integrators + authority-binding mechanism (gate verifies authority-binding completeness as gate condition: pre_send checkpoint evaluates "all claims in send batch have `claim_attested` event with `actor_kind: human`" → if any claim lacks attestation → fail-closed block per shape semantics). W1-W4 watch-list: W1 second-shape productization gate variation + W2 per-axis observability hook signal-set + threshold-set evidence accumulation + W3 cross-deployment gate-state portability via audit-trail composition + W4 quality-gate intervention efficacy empirical evidence. Mode 2 upfront-known composite decomposition (6 sub-decisions covering Pattern A 12+7 template extension + single-layer mechanism-shaped Surface 6 capability categories + per-implementation aspect + selection mechanics + tri-aspect reconciliation + cardinality + lifecycle + boot/shutdown ordering + error categories + tier-awareness + cross-shape policy variation 6-row matrix + composition + W1-W4 watch-list + cross-references + phase routing). **Closes Phase 3.6** (1 of 1 ARCH topic LOCKED); unblocks Phase 3.7 cross-cutting investigations + Phase 3.8 Coherence-audit C3 phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` cadence. Full detail: `arch/quality-gate.md` + `docs/decisions/quality-gate-arch-topic.md`.

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
