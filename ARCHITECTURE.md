# Architecture — Phase 3 rebuild (in progress)

> **Status**: Phase 3 ARCH rebuild ACTIVE. Phase 2 GLOSSARY foundational vocabulary lock COMPLETE (35 entries). Phase 3.1 closed; Phase 3.2 topic taxonomy + structure LOCKED. Per-topic detail will live in `arch/<topic-slug>.md` files as Phase 3.3+ topic content lands (directory not yet created).

## 1. Audience + scope

**This doc is framework-developer documentation.** Layer 2 Overview per `MAINTENANCE.md` 5-layer doc model. Loaded at framework-development session start (along with VISION + MAINTENANCE.md + HANDOFF) for architectural orientation.

**NOT loaded at production runtime by deployed-workspace AI.** Per `ARCHITECTURE.md` cross-cutting principles "AI as runtime" discipline, AI in a deployed PBS workspace doing accountability-bearing work loads runtime-relevant markdown (workspace.md / active specialist DEFINITIONs / skill SKILL.md / shape policy bundles) — not framework architecture documentation.

**Three consumer modes**:

| Mode | Consumer | Loads ARCHITECTURE.md? |
|---|---|---|
| Framework development (current Phase 3+ work) | AI as framework-developer-collaborator + human framework developers | YES — orientation at session start |
| Deployment template creation (L3) / shape composition (L4) | Template/shape creators needing framework architecture understanding | OCCASIONALLY — on-demand reference |
| Production runtime (deployed PBS workspace) | AI runtime processing accountability-bearing work | NO — framework architecture not needed for per-claim work |

**Optimization target**: human readability + framework-developer orientation. NOT optimized for AI runtime parsing (no machine-readable schema; no terse rule encoding). Per `ARCHITECTURE.md` cross-cutting principles "LLM-instruction tightness": instruction tightness matters most for production-runtime markdown layer (Mode 1 in §6 Logic placement modes) — that lives in skills/specialists/workspace.md, not here.

**Scope**: captures **Phase 3 progress** + **topic catalog** + **reading order** + **cross-cutting principles** + **locked architectural decisions** + **active disciplines** + **watch-list**. Migrates toward stable architectural overview as Phase 3 completes.

**Cites**: GLOSSARY entries (Layer 1; locked) + DRs (Layer 4; selective rebuild Phase 4) + specs (Layer 5; Phase 6 territory).

## 2. Phase 3 sub-phase status

| Sub-phase | Scope | Status |
|---|---|---|
| **3.0** | Doc structure (single ARCHITECTURE.md vs topic-per-file vs hybrid) | ✅ LOCKED — hybrid |
| **3.1** | Open architectural questions (workflow / work-unit / deployment / engaged-authorship) | ✅ COMPLETE — all 4 LOCKED. Phase 3.1 closed. Coherence-audit ran at phase boundary; 0 architectural REVISIONS. |
| **3.2** | Topic taxonomy + naming + cross-cutting placement + ARCHITECTURE.md structure (4 sub-decisions) | ✅ COMPLETE — all 4 sub-decisions LOCKED. Composite DR `phase-3-2-doc-organization.md` created. |
| **3.3** | Per-mechanism detail (12 mechanisms; subsumed into Pattern A protocol topics) | Pending |
| **3.4** | Per-architectural-Protocol detail (8 Pattern A protocol topics: substrate ✅ / adapter ✅ / sparring ✅ / audit ✅ / coordination / trust / time / quality-gate is 3.6) | In progress — 4 of 8 (substrate + adapter + sparring + audit drafted; DRs in `docs/decisions/`) |
| **3.5** | Per-primitive detail topics (4 primitive-cluster topics + 2 cross-cutting integrators) | Pending |
| **3.6** | Quality-gate ARCH topic | Pending |
| **3.7** | Cross-cutting investigations (PydanticAI re-eval; markdown-validation; Ming research; multi-VISION) | Pending |
| **3.8** | Coherence-audit checkpoint C3 (phase-boundary; ARCH-specific Lenses 11-15 activate) per `DISCIPLINES.md` Discipline 9 | Pending — preceded by C1 (post-3.4) + C2 (post-3.5) per cadence locked in `BACKLOG.md` Phase 3 audit-checkpoints section |

Foundation-up ordering applied (per `DISCIPLINES.md` Discipline 8): questions before structure before content before audit.

## 3. Doc structure (Phase 3.0 LOCKED)

**Hybrid**: single overview + per-topic files.

| Doc | Purpose | Lines | Status |
|---|---|---|---|
| `ARCHITECTURE.md` (this file) | Overview + topic catalog + cross-cutting principles + how topics compose + Phase 3 status tracking | ~1-2K | Active |
| `arch/<topic-slug>.md` × 14 | Per-topic detail | ~500 each | Not yet created (created as Phase 3.3+ produces topic content) |

**Why hybrid**: pure-single (10K lines) is unwieldy + context-budget concern; pure-multi has no entry point + cross-cutting orphaning. Hybrid aligns with progressive-disclosure principle (skill-craft pattern: SKILL.md → PROCEDURE.md → references/) + sharpen's AI-executor test (cognitive iteration via structure, not gist-extraction across 10K lines).

## 4. Topic catalog (Phase 3.2 LOCKED — 14 topics)

14 ARCH topics in protocol-centric aggregation with primitive-cluster topics. Foundation-up ordered. Per Phase 3.2 Sub-decision 1 lock; filenames per Sub-decision 2 lock.

| # | Topic file | Primary content (one-liner) | Phase |
|---|---|---|---|
| 1 | `arch/substrate.md` ✅ | Substrate Protocol Surface + per-impl + persistent-state + session interaction | 3.4 — DRAFTED |
| 2 | `arch/adapter.md` ✅ | Adapter Protocol Surface (META + per-integration-class) + per-impl + lifecycle/auth | 3.4 — DRAFTED |
| 3 | `arch/sparring.md` ✅ | Sparring Protocol Surface (8 sub-mechanism categories: 4 architecturally-encoded + 4 behaviorally-enforced) + per-shape activation matrix | 3.4 — DRAFTED |
| 4 | `arch/audit.md` ✅ | Audit Protocol Surface (6 capability categories) + audit-trail-as-canonical-source + per-shape event-kind catalog | 3.4 — DRAFTED |
| 5 | `arch/coordination.md` | Coordination Protocol Surface + actor primitive interaction | 3.4 |
| 6 | `arch/trust.md` | Trust Protocol Surface + authority-binding mechanism | 3.4 |
| 7 | `arch/time.md` | Time Protocol Surface + temporal-semantics variations | 3.4 |
| 8 | `arch/quality-gate.md` | Quality-gate Pattern A Surface + per-shape implementations + signal catalog | 3.6 |
| 9 | `arch/specialist-skill.md` | Specialist DEFINITION + skill granularity + bundle structure + marketplace | 3.5 |
| 10 | `arch/practitioner.md` | Practitioner Pattern C bipartite + record placement + multi-practitioner | 3.5 |
| 11 | `arch/workflow-work-unit.md` | Workflow Pattern B + work-unit Pattern B + workflow_instance state machine + orchestration | 3.5 |
| 12 | `arch/claim-defensibility.md` | Claim primitive + defensibility test + source-grounding + engaged-authorship + per-claim attestation | 3.5 |
| 13 | `arch/scope-model.md` | Workspace + Framework C / Owner B / Layer A scope categories + entity placement | 3.5 |
| 14 | `arch/axis-interactions.md` | 3 VISION axes interaction + co-worker frame + category-collapse cross-axis force | 3.5 |

**Aggregation discipline**: aggregate when items tightly coupled OR individually <100 lines (per coherence-audit Lens 15). Each topic targets ~500 lines avg; per-topic flex acceptable.

**Foundation-up dependency**: topics 1-7 are Pattern A protocols (foundational mechanism layer); 8 quality-gate composes with all axes (observability); 9-12 are primitive clusters (operational primitives); 13-14 are cross-cutting integrators (load LAST since they reference all prior topics).

**Phase 3.7 cross-cutting investigations excluded** (research/strategic items, not ARCH-topic-shaped): PydanticAI substrate eval / Markdown-validation feasibility / Ming research deepening / Adjacent thinkers expansion / Multi-VISION model question. May inform topic content but aren't topics themselves.

**Headroom**: 6 emergent topics may be added (14 → 20 cap) during Phase 3.3-3.6 work without taxonomy revision.

## 5. Reading order

**For new readers** orienting to framework architecture, foundation-up:

1. **VISION.md** (Layer 1) — three-axis thesis; falsification framing
2. **GLOSSARY.md** (Layer 1) — locked vocabulary (35 entries)
3. **MAINTENANCE.md** (Layer 0) — doc-system discipline + TOP-LEVEL ARCHITECTURE (framework=mechanisms; shape=policies)
4. **ARCHITECTURE.md** (Layer 2; this doc) — overview + topic catalog + cross-cutting principles
5. **arch/<topic>.md** (Layer 3) — topic detail in foundation-up order:
   - **Pattern A protocols** (mechanism layer): substrate → adapter → audit → trust → coordination → time → sparring → quality-gate
   - **Primitive clusters** (operational layer): specialist-skill → practitioner → workflow-work-unit → claim-defensibility
   - **Cross-cutting integrators** (LAST; reference all prior): scope-model → axis-interactions
6. **DRs** (Layer 4) — decision rationale for specific commits
7. **Specs** (Layer 5; Phase 6) — Pydantic schemas + spec docs

**For session-resumption**: read HANDOFF.md (current session log) + BACKLOG.md (forward-looking work-tracker) before substantive work.

**For specific debugging / contextual entry**: experienced readers can enter at relevant `arch/<topic>.md` directly; reading order is recommendation not gate.

## 6. Cross-cutting principles

### Pattern-A vs Pattern-B vs Pattern-C structural semantics

| Pattern | Shape | Examples | Composition |
|---|---|---|---|
| **Pattern A** (pluggable subsystem) | Surface (interface contract) + Implementations (per-shape variation) + Selection (workspace.md / shape policy declares which impl) | Substrate / Adapter / Sparring / Audit / Coordination / Trust / Time / Quality-gate | Workspace selects exactly one impl per Pattern A slot |
| **Pattern B** (bipartite definition + instance) | DEFINITION aspect (Framework C / specialist's distributable bundle) + INSTANCE aspect (Owner B / workspace-scope managed entity) | Specialist + Workflow + Work-unit | Specialist DEFINITION declares; workspace activates → instances at Owner B |
| **Pattern C** (cross-cutting human + record) | HUMAN aspect (cross-cutting; lives outside workspace) + RECORD aspect (Owner B / workspace-scope) | Practitioner | Human anchored cross-cutting; practitioner-record placed at Owner B per active practitioner |

Architectural decisions classify primitives into Pattern A/B/C (or DERIVED if composing from existing primitives without independent structural content). Cross-pattern composition (e.g., specialist Pattern B containing workflow Pattern B) is locked per GLOSSARY entries.

### Cascade direction (UPSTREAM + DOWNSTREAM bidirectional per `MAINTENANCE.md`)

- **UPSTREAM**: GLOSSARY change → cascade to ARCH/DRs/specs (Layer 1 → 2-5)
- **DOWNSTREAM**: ARCH/DR/spec work surfacing glossary-grade structural fact → retro-fit GLOSSARY before locking (Layer 2-5 → 1)

GLOSSARY back-check fires at decision-design-sharpening Round 2 termination + ARCH topic completion + DR drafting. Prevents architectural insights from staying locked in ARCH/DR layer when they're glossary-grade.

### Scope-categorization framing

Three scope categories (per locked GLOSSARY entries):
- **Framework C** — distributable definitions (specialist DEFINITIONs / shape policies / Pattern A protocols / mechanism interface contracts)
- **Owner B** — workspace-bound instances (workspace.md / specialist instances / work-unit instances / workflow_instances / practitioner-records / Actor records / engagement-target entities per shape)
- **Layer A** — content varying by deployment context (universal / domain-keyed / state-keyed)

Detail in `arch/scope-model.md` (Phase 3.5).

### Foundation-up ordering principle

Lock items others depend on FIRST; downstream items composing with multiple foundations come last. Applied across:
- Phase 3.1 sub-decisions (workflow → work-unit → deployment → engaged-authorship)
- Topic ordering (substrate → adapter → ... → axis-interactions)
- Within Sub-decision sharpening (Round 1 surface → Round 2 expansions per locked Round 1 position)

Per `DISCIPLINES.md` Discipline 8 + cascade discipline.

### Logic placement modes (4-mode distribution)

Where actual framework logic lives, by interpretability:

| Mode | Layer | Interpretability | Examples |
|---|---|---|---|
| **Mode 1** Production-runtime LLM-MD | Operational | AI reads + interprets at workspace activation / per-skill-trigger / per-active-specialist | Skills (`plugin/skills/<skill>/SKILL.md`) / specialist DEFINITIONs / `workspace.md` / shape policy bundles / bausteine |
| **Mode 2** Production-runtime Python | Substrate-side | Substrate runtime executes | Substrate Instance impl / mechanism Python impls / adapter implementations / quality-gate Pattern A impls / Pydantic schema validation |
| **Mode 3** Hybrid Phase 6 specs | Spec layer | Pydantic = Python validation; spec docs = LLM-MD reference | Phase 6 spec files (Pydantic + companion docs) |
| **Mode 4** Development-time LLM-MD | Documentation | Loaded at framework-development session start; NOT production-runtime | ARCHITECTURE.md / arch/* / DRs / MAINTENANCE.md / VISION / GLOSSARY / profiles / learnings / DISCIPLINES.md |

**Discipline implications**:
- **Mode 1 = highest LLM-instruction tightness** required (per `ARCHITECTURE.md` cross-cutting principles "LLM-instruction tightness"); LLMs paper over imprecise instructions silently
- **Mode 2 = standard Python development discipline**; self-falsifying via tests + type errors
- **Mode 3 = bridge** between modes; Pydantic enforces structural shape; spec docs explain semantic intent
- **Mode 4 = optimize for human readability + AI-developer orientation**; NOT for production-runtime parsing

**Anti-pattern**: encoding framework rules in Mode 4 (ARCHITECTURE.md / arch/) intending production AI to "follow them" — that's the SQL-DB trap (see "AI as runtime, not AI as consumer" below). Production AI follows Mode 1 markdown (skills + specialists + workspace.md); Mode 4 is documentation, not runtime substrate.

**Production runtime AI doesn't load Mode 4 docs** (ARCHITECTURE.md / arch/* / VISION / GLOSSARY) — vocabulary + behavior get encoded into Mode 1 skills + specialists at framework-development time. Production AI gets vocabulary via skill instruction inheritance.

### AI as runtime, not AI as consumer

When user names AI capability as *the mechanism* / *pillar* of an architecture (not as a feature being added on), the architectural shape mirrors how Claude already operates in PBS infrastructure: minimal structured skeleton (identity, cross-refs, persistence) + markdown body (semantics, rules, domain process) + AI reads at runtime.

**Do NOT add an "encoded rules" layer** — even one that uses prose instead of code. That's the SQL-DB trap in disguise.

**Why**: framework relies on AI loading markdown at runtime to interpret semantics + rules + domain process. Treating prose-rule-encoding as "the format" rather than as a structural claim about how AI offices are built misses the point. Memories work because Claude IS the runtime — no memory engine. Same pattern applies to managed entities, specialist DEFINITIONs, doctype manifests, anything where domain semantics live.

**How to apply**: when designing PBS infrastructure where AI does the reasoning, ask: "would a memory work here?" If yes, the right shape is frontmatter + markdown body, period — NOT an additional tier for rules. Specifically:
- **Structured for**: interfaces / identity / persistence
- **Markdown for**: semantics / rules / domain process
- **AI is the runtime** that fuses them

The question "where do the rules live?" is itself a tell that you're about to over-structure.

When the user names AI processing as a "pillar" or "the only way," read that as a *load-bearing structural claim*, not an enhancement — design FROM that, not AROUND it.

### LLM-instruction tightness for Mode 1 markdown layer

LLMs paper over imprecise markdown instructions by inference — they're smart enough to guess at proper course of action even when SKILL.md / specialist DEFINITION / workspace.md instructions aren't spot-on. But that guessing:
- **Is brittle** (changes when model, context, or surrounding instructions shift)
- **Has more overhead** (each session re-derives the constraint)
- **Drifts silently** (no failure signal when guess differs from intent)
- **Compounds** (one shaky instruction seeds shakier downstream inferences)

Deterministic Python doesn't have this property — wrong-shape Python surfaces fast (compile error / type error / test failure); wrong-shape markdown surfaces only when behavior diverges from intent and someone notices.

**Asymmetric review effort follows**: heavier on Mode 1 markdown (skill instructions; specialist DEFINITIONs; workspace.md; shape policy bundles); lighter on Mode 2 Python (self-falsifying via tests + type errors).

**How to apply** — bias toward sharpening (vs feature-forward) when:
- The system is pre-launch or pre-deployment-multiplication
- The thing being sharpened is markdown / instructions / VISION / ARCHITECTURE / skill-body conventions (LLM-consumed Mode 1/4 layer)
- Current state is "LLM is inferring the right answer most of the time" — that's the warning sign, NOT the comfortable state it sounds like
- A coupling between layers (VISION → ARCH; ARCH → skills; meta-rule → audit) is asserted but not made structural

Bias toward feature-forward when:
- The thing being sharpened is deterministic Python (it self-fails on ambiguity)
- The system is post-launch and changes are expensive to propagate
- The instruction layer is concrete and well-coupled already

### How topics compose

- **Mechanisms** (instances of `mechanism` primitive) are atomic interface contracts; primitives + protocols + axes COMPOSE WITH multiple mechanisms (audit-emission composes with audit-trail + event; persistent-state composes with substrate + session)
- **Protocols** (Pattern A pluggable subsystems) bundle Surface + Implementations + Selection; topics 1-8
- **Primitive clusters** group tightly-coupled primitives by composition (specialist contains skill; workflow attaches to work-unit; claim resolves at defensibility-granularity); topics 9-12
- **Cross-cutting integrators** (axis-interactions; scope-model) — analyze structural composition across all prior topics; topics 13-14
- **Composing relations between topics** explicitly cross-referenced in each arch/<topic>.md via cross-refs (e.g., arch/audit.md references arch/quality-gate.md as observability consumer)

### Composability + boundaries (per G gate)

Every L1-L4 producer level (specialist / shape / template / workspace) must produce packageable artifacts that support multi-mode consumption. Architectural decisions that produce non-composable artifacts fail G gate. See `profiles/G-composability-gate.md`.

### Pattern-vs-instance discipline

Framework primitives stay shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer-instance specifics live at workspace level (per practitioner-shape policy mandates), NOT in framework primitive definitions. See `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 + `profiles/L5a-planner-pbs-schulz.md` (anchor profile demonstrates pioneer reality).

## 7. Locked architectural decisions

### Quality-gate scope-lock (Phase 3.6 prerequisite) — LOCKED

**Resolution**: `quality-gate` re-classified to **Pattern A protocol with mechanism-shaped Surface**:
- Surface: common observability + emission contract; per-axis-failure-mode signal catalog
- Implementations: structural variation per shape (practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-shape-gate; extensible)
- Selection: shape declares which implementation
- Lifecycle per implementation: stateful vs stateless (per shape)
- Per-shape error semantics: fail-closed (practitioner-shape; defensibility-critical) / fail-open with alert (autonomous-business) / fail-open (personal-OS)
- Naming disambiguation: distinct from G/D validation gates (architectural-decision-time); quality-gate is runtime

**Round 1 + Round 2 sharpening**: 0 architectural REVISIONS surfaced (R1 rename rejected); 7 EXPANSIONS applied (naming disambiguation; lifecycle stateful-vs-stateless; intertwining + co-worker composition; per-axis signal catalog; boot/shutdown/error semantics; authority-binding; tier-awareness).

**Phase 3.6 produces**: full Surface specification + per-implementation detail + per-axis signal catalog + intervention mechanics + error semantics + tier-awareness configuration.

**Full detail**: `GLOSSARY.md` quality-gate entry. **DR**: `docs/decisions/quality-gate-scope-lock.md`.

### Workflow bipartite-classification (Phase 3.1) — LOCKED

**Resolution**: `workflow` re-classified to **bipartite Pattern B with optional applicability**:
- DEFINITION aspect: contained in specialist's distributable bundle (specialist DEFINITION at Framework C contains workflow definitions; not standalone Framework C primitive)
- INSTANCE aspect: workflow_instance entity at Owner B (per workspace per work-unit when codified pattern applies)
- **Optional applicability**: workflow_instance engages ONLY when work follows codified pattern. Ad-hoc work outside primitive scope (engages session + work-unit + skill + claim + event WITHOUT workflow_instance). Per workflow Round 2 + user push: ad-hoc work is first-class, not "degenerate Pattern B."
- Vocabulary disambiguation: `workflow` = the primitive; `workflow definition` = DEFINITION aspect; `workflow_instance` = INSTANCE aspect (entity-md per Owner B convention)

**workflow_pattern question** (cross-specialist shared workflows): RESOLVED via D gate mental modeling. Shared patterns live as **Layer A reusable templates / specialist-bundled bausteine** (content, NOT framework primitive). Watch-list signal: if Layer A growth proves insufficient for genuinely-cross-archetype pattern, examine then.

**Validated under post-lock disciplines**: Round 1 + Round 2 revisit (with G gate + multi-axis + D gate applied) confirmed lock holds. 0 architectural REVISIONS surfaced.

**Full detail**: `GLOSSARY.md` workflow entry. **DR**: `docs/decisions/workflow-bipartite-classification.md`.

### Work-unit bipartite-classification (Phase 3.1) — LOCKED

**Resolution**: `work-unit` re-classified to **bipartite Pattern B with always-present container**:
- KIND DEFINITION aspect: contained in specialist's distributable bundle (specialist DEFINITION at Framework C declares supported `work-unit kind`s + per-kind structural conventions; not standalone Framework C primitive)
- INSTANCE aspect: `work-unit instance` entity at Owner B (per workspace per active kind)
- **Always-present container** (reciprocal to workflow's optional applicability): every accountability-bearing piece of work IS a work-unit; no opt-out path. Workflow_instance is the optional structural overlay that ATTACHES to a work-unit; ad-hoc work-units have no workflow_instance but still exist as work-unit instances.
- Vocabulary disambiguation: `work-unit` = the primitive; `work-unit kind` = DEFINITION aspect; `work-unit instance` = INSTANCE aspect (entity-md per Owner B convention)

**Asymmetry vs workflow** (load-bearing): work-unit always-present + workflow optional-overlay. Together: work-unit is anchor; workflow_instance is opt-in via codified pattern existence. Two Pattern B primitives composing cleanly with reciprocal cardinality (1 work-unit ↔ N workflow_instances; 1 workflow_instance → 1 work-unit).

**Full detail**: `GLOSSARY.md` work-unit entry. **DR**: `docs/decisions/work-unit-bipartite-classification.md`.

### Deployment definition (Phase 3.1) — LOCKED

**Resolution**: `deployment` locked as **DERIVED concept** = workspace-as-bound-runtime (binding-act-aspect of workspace). 1:1 with workspace at framework primitive level.

- **Class**: DERIVED (perspective on workspace; not standalone primitive)
- **Cardinality**: 1:1 with workspace at framework level (multi-environment = N workspaces; multi-tenant = substrate-Instance level concern)
- **Vocabulary distinction**: workspace = entity (configuration view); deployment = binding-relation (runtime view); both describe same primitive object from different angles
- **Workspace identity** can persist across multiple deployments over time (backup→restore, substrate migration, re-activation) — workspace identity is workspace-portability concern (Phase 6 spec); deployment count is the runtime binding count

**Why DERIVED not PRIMITIVE**: deployment introduces no independent structural content beyond workspace's runtime aspect. No separate cardinality, lifecycle, observability surface, or attributes. DERIVED entry preserves vocabulary utility without inflating primitive count.

**Full detail**: `GLOSSARY.md` deployment entry. **DR**: `docs/decisions/deployment-derived-classification.md`.

### Engaged-authorship operational definition (Phase 3.1) — LOCKED

**Resolution**: `engaged authorship` locked as **DERIVED axis-3 success mode** with two-phase composite operational definition:

1. **Production-phase engagement** (axis-2-anchored): per-claim sparring participation observed via sparring-event emissions
2. **Attestation-phase engagement** (axis-3-anchored): per-claim attestation event emitted at finalization (NOT whole-output sign-off)

**Both phases independent + both must structurally complete** (per locked rubber-stamping entry — axis-2 failures and rubber-stamping are INDEPENDENT dimensions).

**Granularity**: per-claim per-version (revised claim = new engagement test cycle).

**Two layers of operationalization**:
- **Framework-level: PRESENCE** — Y/N event-existence test (per-claim production-phase event ≥1 + per-claim attestation event)
- **Shape-policy-level: QUALITY** — depth-of-engagement signals (substantiveness; counter-argument depth; etc.); quality-gate enforces

**Why this elevates from defensibility's Condition #1 to standalone DERIVED entry**: engaged authorship is load-bearing across multiple entries (`defensibility`, `authorship preservation`, `rubber-stamping`, `quality-gate`, `claim`). Standalone entry preserves canonical definition + composition without bloating defensibility.

**Full detail**: `GLOSSARY.md` engaged authorship entry. **DR**: `docs/decisions/engaged-authorship-operational-definition.md`.

### Substrate ARCH topic (Phase 3.4 first canonical) — LOCKED

**Resolution**: `arch/substrate.md` LOCKED as first canonical Pattern A protocol topic. Establishes 18-section template for remaining 7 Pattern A protocol topics (adapter / sparring / audit / coordination / trust / time / quality-gate at 3.6).

- **Surface (architectural-conceptual)**: 7 capability categories (agent loop / MCP register+discover / permission flow / structured-output validation / hook registration / session+context management / specialist registration)
- **Per-impl extension Protocols pattern**: typed Protocols isinstance-checked at use site; substrate-coupling impossible-by-construction
- **Tri-aspect Pattern A**: Surface (mechanism) + Implementations (Framework C) + Running Instance (Owner B)
- **Boundary criteria**: decision rule for Surface vs per-impl extension applied at Surface-design moment
- **Substrate-internal vs skill-side audit emission**: dual paths converging in audit-trail (resolves MCP-gate-circularity)
- **Boot/shutdown ordering, error categories, transport variation, deployment-tier awareness**: cross-cutting + schema-detail layer per `decision-design-sharpening` v0.6.0 layered coverage observation
- **Pre-implementation operational concerns**: explicit Phase 6 forward-reference (cancellation / timeouts / rate-limit / health-check / per-tenant isolation / streaming / etc.)
- **Phase routing**: Pydantic Protocol contract → Phase 6 spec; concrete substrate impls → Phase 6

**Sharpening totals**: 13 EXPANSIONS / 0 REVISIONS / 3 manufactured criticisms rejected (Round 1 = 2 EXPANSIONS / Round 2 cross-cutting + schema-detail layer = 11 EXPANSIONS / Profile validation pass = 0 new findings / 4-cluster PASS reinforced).

**Procedural-fidelity case**: Round 1 initially applied skill from synthesized memory; user-detected; SKILL.md re-Read; Round 2 properly executed under codified discipline. 5-location structural fix (commit `be7c8fa`) locked before Round 2 + retroactive profile-anchored validation pass. Documented as canonical session-16 case in `learnings/ai-app-development.md` Observation 28 + `drafts/execution-fidelity.md`.

**Full detail**: `arch/substrate.md`. **DR**: `docs/decisions/substrate-arch-topic.md`.

### Adapter ARCH topic (Phase 3.4 second Pattern A protocol) — LOCKED

**Resolution**: `arch/adapter.md` LOCKED as second canonical Pattern A protocol topic. Validates substrate-established 18-section template + introduces **two-layer Surface variation** (META-Surface conventions + per-integration-class Surfaces) for Pattern A protocols where per-instance-class admits semantic coherence within class but heterogeneity across classes.

- **Internal-vs-external axis**: substrate INTERNAL runtime contract; adapter EXTERNAL integration boundary — load-bearing distinction
- **META-Surface** (cross-class): lifecycle entry / auth surface / permission flow integration / audit emission / error mapping / health check / versioning
- **Per-integration-class Surfaces** (5 currently): Email / Accounting / MCP-Server / A2A-Peer / File-Sync (each with class-specific capability categories)
- **Multi-instance cardinality**: typically N adapters per workspace (vs substrate's singular)
- **Audit emission**: skill-side via MCP gate ONLY (no circularity issue — adapters don't register MCP gate; substrate does)
- **Permission flow composition**: adapter writes (axis-3 send) request_permission via substrate Surface §C
- **Auth + lifecycle**: per-class auth models (OAuth / API key / shared secret / certificate); proactive + reactive refresh; per-shape encryption mandates
- **Cross-shape policy variation**: practitioner-shape mandates per-action audit + fail-closed on send; autonomous-business relax for continuity; personal-OS skip per-action
- **Hot-swap re-binding**: adapter instances re-bindable mid-workspace-life (NOT deploy-time-only); workflow_instance re-binding compatibility declared
- **Quota + circuit-breaker**: per-class metrics; closed/open/half-open state; per-shape thresholds

**Sharpening totals**: 20 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected (Round 1 = 8 EXPANSIONS / Round 2 cross-cutting + schema-detail layer = 12 EXPANSIONS).

**GLOSSARY back-check**: clean (multi-instance-Pattern-A + auth-state-at-Owner-B already implicit in `protocol (architectural)` + Owner B scope entries). Profile-cluster validation 4/4 PASS with cited content.

**Full detail**: `arch/adapter.md`. **DR**: `docs/decisions/adapter-arch-topic.md`.

### Sparring ARCH topic (Phase 3.4 third Pattern A protocol) — LOCKED

**Resolution**: `arch/sparring.md` LOCKED as third Pattern A protocol topic. Single-layer Surface (substrate-style) with 8 sub-mechanism capability categories. Introduces NEW per-shape activation-matrix variation (third Pattern A cardinality pattern alongside substrate's singular tier-aware + adapter's multi-instance per-class).

- **8 sub-mechanism capability categories**: counter-argument / confidence calibration / visible reasoning / selective friction (architecturally-encoded; gate-dispatched per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1) + anti-sycophancy / asymmetric knowledge respect / commit-to-recommendations / what's-missing (behaviorally-enforced; AI applies at judgment time)
- **Cardinality**: 1 Sparring Protocol Implementation per workspace; shape policy declares which sub-mechanisms active (per-shape activation matrix)
- **Cross-axis dependency**: sparring fires AT claim granularity; sparring events ARE production-phase substrate for `engaged authorship` two-phase composite (axis-2 → axis-3 dependency)
- **Composition with substrate Surface §D** (structured output validation): load-bearing for architecturally-encoded sub-mechanisms 1-4 (Pydantic schema enforcement; auto-retry inherited)
- **Per-shape policy variation**: practitioner-shape mandates all 8 active + fail-closed + ≥1 sparring-event per claim; autonomous-business per business policy with fail-open + alert; personal-OS subset with fail-open
- **Per-action audit emission**: skill-side via MCP gate (like adapter); per-sub-mechanism event-kind catalog + axis-2 failure-mode detection events (answer_machine_detected / oracle_mode_detected / validator_mode_detected)
- **Pre-implementation operational concerns**: explicit Phase 6 forward-reference (per-sub-mechanism schemas / orchestrator retry mechanics / heuristic-detection thresholds / bypass-with-reason UX)

**Sharpening totals**: 20 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected (Round 1 = 7 / Round 2 cross-cutting + schema-detail = 13).

**GLOSSARY back-check**: clean (failure-mode detection events derive from already-locked answer-machine / oracle / validator AI entries; selective-friction threshold is impl-mechanic). Profile-cluster validation 4/4 PASS with cited content.

**Full detail**: `arch/sparring.md`. **DR**: `docs/decisions/sparring-arch-topic.md`.

### Audit ARCH topic (Phase 3.4 fourth Pattern A protocol) — LOCKED

**Resolution**: `arch/audit.md` LOCKED as fourth Pattern A protocol topic. Single-layer Surface (substrate-style) with 6 capability categories. Consolidates emission paths from substrate §8 + adapter §8 + sparring §8 into unified architectural commitment. Introduces NEW deployment-tier-driven cardinality variation (fourth Pattern A pattern alongside substrate's singular tier-aware + adapter's multi-instance per-class + sparring's per-shape activation matrix).

- **6 Surface capability categories**: emission API + actor declaration / append-only persistence / query for reasoning-chain reconstruction / integrity verification / event-kind catalog management / state-rendering-from-events
- **Audit-trail-as-canonical-source** (load-bearing architectural commitment per archived audit-trail-v2): single-write architecture; state rendered FROM events; append-only discipline; never rewritten
- **Append-only enforcement architectural-level** per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator (gate-dispatched on every write → structural)
- **Per-shape event-kind catalog**: practitioner-shape claim-level (claim_made / source_grounded / sparring_round / per_claim_attestation / signature_applied) + autonomous-business action-level + personal-OS light
- **Boot/shutdown ordering**: audit boots BEFORE substrate; shuts down AFTER substrate (preserves invariant: every emitted event is persisted before workspace shutdown)
- **Hash-chain integrity verification** at architectural-level (specific algorithm Phase 6); cross-deployment migration verifies hash-chain unbroken
- **Cross-deployment evidence + external-format export** (per L8 line 33 external-format requirements): jsonl raw + PDF reports + CSV event logs

**Sharpening totals**: 21 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected (Round 1 = 8 / Round 2 cross-cutting + schema-detail = 13).

**GLOSSARY back-check**: clean (append-only-discipline + state-rendering-from-events already implicit in `event` GLOSSARY entry per archived audit-trail-v2 schema). Profile-cluster validation 4/4 PASS with cited content (G line 159 + G line 168 + L5a line 41 + L8 lines 29/32/33).

**Full detail**: `arch/audit.md`. **DR**: `docs/decisions/audit-arch-topic.md`.

### Phase 3.1 closed

All 4 open architectural questions resolved (workflow / work-unit / deployment / engaged-authorship). Coherence-audit ran at phase boundary; 0 architectural REVISIONS; 9 cascade-fix EXPANSIONS applied.

### Topic taxonomy (Phase 3.2 Sub-decision 1) — LOCKED

**Resolution**: 14 ARCH topics in protocol-centric aggregation with primitive-cluster topics. Foundation-up ordering. Under MAINTENANCE budget (15-20 cap) with 6-topic headroom for emergent additions during Phase 3.3-3.6 work.

**Aggregation rationale**:
- Pattern A protocols are natural topic anchors (Surface + per-impl + composing mechanisms + composing primitives all coherent under one topic)
- Primitives without Pattern A home cluster by composition tightness (specialist+skill; workflow+work-unit; claim+defensibility — all tightly coupled per locked entries)
- Cross-cutting topics for irreducibly cross-axis content (scope-model; axis-interactions)

**Full topic list**: see §4 Topic catalog above. **Composite DR**: pending Phase 3.2 final synthesis pass.

### File naming convention (Phase 3.2 Sub-decision 2) — LOCKED

**Resolution**: Plain kebab-case slug = topic name; flat `arch/` directory; no prefixes; no sub-directories.

**Slug rules**:
- Path: `arch/<slug>.md`
- Slug: lowercase kebab-case; matches topic name in topic catalog
- Aggregation join: hyphen (`specialist+skill` → `specialist-skill.md`; `workflow+work-unit` → `workflow-work-unit.md`)
- No prefix (numeric / bucket / category)
- Plain `.md` extension; flat `arch/` directory; NO sub-directories per topic-cluster
- NO `arch/README.md` or `arch/INDEX.md` (ARCHITECTURE.md is canonical entry point)

**Cross-doc link conventions**: relative paths within arch/; `arch/<slug>.md` from elsewhere; GitHub-flavored anchors (`#section-name`).

**File header convention**: minimal frontmatter (title; topic-cluster; status: drafted/locked/forthcoming); H1 = de-kebab-cased slug.

**Why these conventions**: slug stability across taxonomy refinements (no embedded ordering / bucketing in path); visual + grep parity with GLOSSARY TOC anchors; flat directory simplifies navigation.

### Cross-cutting topics placement (Phase 3.2 Sub-decision 3) — LOCKED

**Resolution**: cross-cutting CONCERNS vs cross-cutting TOPICS distinction codified.

- **Cross-cutting TOPICS** (dedicated `arch/<topic>.md` files): axis-interactions / scope-model / quality-gate
- **Cross-cutting CONCERNS** (ARCHITECTURE.md sections): Pattern-A/B/C semantics / cascade direction / scope-categorization framing / foundation-up ordering / G+D gate disciplines / Logic placement modes

**Distinction is load-bearing**: TOPIC = architectural content (lives in arch/); CONCERN = meta-principle (lives in ARCHITECTURE.md). Different placement, different KIND.

**Reading order for cross-cutting topics**: axis-interactions + scope-model LAST in foundation-up sequence (integrate across ALL prior topics). Quality-gate after foundational protocols.

**No content migration** between MAINTENANCE.md (Layer 0 discipline) and arch/scope-model.md (Layer 3 detail) — layer-distinction maintained.

### ARCHITECTURE.md overview structure (Phase 3.2 Sub-decision 4) — LOCKED

**Resolution**: 9-section structure (this doc's structure). Foundation-up ordered for new-reader path: orientation → Phase status → doc structure → topic catalog → reading order → cross-cutting principles → locked decisions → disciplines → watch-list.

**Audience + scope explicit** (Section 1): framework-developer documentation; loaded at framework-development session start; NOT production-runtime by deployed-workspace AI. Per Mode 4 placement (§6 Logic placement modes).

**Logic placement modes** (Section 6 cross-cutting principles): 4-mode distribution (Mode 1 production-runtime LLM-MD / Mode 2 production-runtime Python / Mode 3 hybrid Phase 6 specs / Mode 4 development-time LLM-MD documentation). Codifies where actual framework logic lives by interpretability mode + scopes ARCHITECTURE.md placement.

**Catalog uniformity**: cross-cutting topics + Pattern A protocols + primitive clusters all get same one-liner depth in §4 Topic catalog. Topics earn detail in their own arch/<topic>.md files.

**Locked decisions section growth mitigation**: each lock summary stays SHORT (resolution + 1-2 sentence rationale + cross-ref to arch/<topic>.md detail OR DR for full content). Detail lives elsewhere; ARCHITECTURE.md keeps catalog-style summaries.

**Composite DR pending**: Phase 3.2 final synthesis pass produces single composite DR capturing all 4 sub-decisions per Mode-2 composite decomposition (decision-design-sharpening v0.6.0).

## 8. Disciplines applying to all ARCH work

These disciplines fire during architectural decision-making + validation. Codified via memory feedback rules + structural gates + sharpening skills.

### Validation gates (structural)

| Gate | Fires when | Blocks until |
|---|---|---|
| **G — Composability Gate** | Designing any L1-L4 producer artifact | Multi-mode consumption requirements satisfied (consulting / firm-reuse / OSS / marketplace-future / backup-migration) |
| **D — Defer Gate** | AI considers deferring any architectural item | Mental modeling within profile grounding attempted; defer only valid if mental modeling genuinely cannot resolve |

Both gates are STRUCTURAL — wrong shapes can't pass. Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: prefer structural constraints that make wrong shapes impossible.

Gates are codified in `profiles/INDEX.md`. Decision-design-sharpening v0.6.0 references them in Round 2 stress-test list.

### Multi-axis validation (per `DISCIPLINES.md` Discipline 3 (multi-axis sub-section))

Validate primitive classifications across three orthogonal dimensions:
- **Archetype**: planner / lawyer / researcher / auditor / etc.
- **Work-type within archetype**: codified workflow / ad-hoc exploratory / one-off communication / research-mode / maintenance / learning
- **Role**: practitioner / workflow-designer / specialist-author / instance-deployer / AI-runtime / multi-user-collaborator

Plus explicit non-coverage question: what use cases does primitive NOT cover; intentional or gap?

### Profile-anchored validation (per `decision-design-sharpening` v0.5.0+ + `profiles/INDEX.md` clusters)

For high-impact decisions (primitive classifications; per-mechanism / per-protocol / per-primitive-detail design — Phase 3.3-3.6 territory), test against ≥3 of 4 profile-clusters:
- **Cluster A — Producers**: L1 specialist creator + L2 shape definer + L3 deployment template creator + L9 shape catalog curator
- **Cluster B — Deployers**: L4a solo self-deploy + L4b IT admin at firm + L5a planner-pbs-schulz pioneer (deployer-of-self)
- **Cluster C — Consumers**: L5a-L5j practitioner archetypes + L5e autonomous-business + L5f personal-OS
- **Cluster D — Validators**: L8 auditor/reviewer + G + D gates

For routine decisions or cascade-from-established-pattern decisions, multi-axis principle-level check is sufficient. Discriminator: shape-specific or instance-specific surface → profile-anchored; purely structural cascade → multi-axis principle-level.

17 profiles (2 full + 15 skeletons). Skeletons fleshed out on-demand when specific decisions need them (per coherence-audit on-demand fleshing strategy).

### Audit scaling strategy (per coherence-audit v0.3.0)

Audit cost grows multiplicatively (profiles × entries). Pure systematic at every invocation unsustainable as corpus grows. Combination approach:
- **Cluster compression** for routine health-checks (group profiles into 4-7 clusters; audit per-cluster)
- **Audit deltas** for incremental decisions (re-audit only what changed since last)
- **On-demand fleshing** for high-impact decisions (flesh skeleton profiles for affected scope; systematic within affected scope)
- **Full systematic** RESERVED for phase boundaries + new-discipline introductions (rare; high-stakes)

Don't default to full systematic. Match audit-strategy to audit-context. See coherence-audit v0.3.0 "Audit scaling strategies" section for full pattern.

### Other disciplines

- **Foundation-up workflow ordering** (per `DISCIPLINES.md` Discipline 8): items others depend on come first; downstream items composing with multiple foundations come last; parallel-depth items batch with shared sharpening
- **2-round sweet spot** per architectural decision (per `DISCIPLINES.md` Discipline 3 + sharpen v0.9.0)
- **Composite-decision decomposition** (per `decision-design-sharpening` v0.6.0): two modes — emergent (>3-round drift signal) + upfront-known (3+ tightly-coupled sub-decisions visible at framing); foundation-up sub-decision sequence + per-sub-decision 2-round + final synthesis
- **Cascade discipline** (per `MAINTENANCE.md`): UPSTREAM + DOWNSTREAM bidirectional; changes propagate up/down/sideways in same commit; GLOSSARY back-check at Round 2 termination
- **Pattern-vs-instance** (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2): no instance-leakage; cross-archetype illustrations required
- **AI-as-runtime hybrid-shape** (per `ARCHITECTURE.md` cross-cutting principles "AI as runtime"): don't add rule-encoding layer; production AI follows Mode 1 (skills + specialists + workspace.md) not Mode 4 (documentation)
- **Provenance hygiene** (per coherence-audit Lens 5 v0.2.1): no audit-history breadcrumbs in canonical content; provenance lives in HANDOFF + git log + commit messages
- **Codify upfront vs wait-for-evidence** (per `learnings/ai-app-development.md` Observation 27): situational, not principled-default; 5-question discriminator (pain observability / shape ambiguity / retrofit cost / pattern maturity / overhead amortization); when deferring, add detection mechanism (self-check + watch-list naming awaited signal)

## 9. Watch-list (architectural items awaiting external evidence)

Per D gate + `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 no-defer principle. ARCHITECTURE.md captures architectural-state-relevant items; BACKLOG.md has detailed work-tracking.

| Watch-list item | Awaited signal | Resolution mechanism |
|---|---|---|
| Shape-neutrality validation for second-shape productization | Second-shape design begins (autonomous-business OR personal-OS) | Validate primitive framings + new shape's policies handle variations cleanly; per-axis variants surface in shape policies |
| Cross-specialist shared workflow patterns insufficient via Layer A | If Layer A growth proves insufficient for genuinely-cross-archetype pattern | Examine then; `workflow_pattern` framework primitive remains unwarranted by default per workflow Round 2 D-gate resolution |
| 3-tier REVISION/EXPANSION discriminator codification | ≥3 borderline classifications across consecutive decisions/audits OR user pushback OR cascade-work-lag | Detection mechanisms in place: self-check at decision-design-sharpening v0.6.0 Round 2 termination + coherence-audit v0.3.1 Step 7. Codify 3-tier (or alternative shape — accumulated cases may suggest different cuts) at signal. |

See BACKLOG.md for actionable detail on watch-list items + Phase 4-6 forward work.

## Cross-references

- `MAINTENANCE.md` — 5-layer doc model + cascade discipline + TOP-LEVEL ARCHITECTURE
- `VISION.md` — three-axis thesis + falsification + foundations
- `GLOSSARY.md` — Layer 1 vocabulary (35 locked entries)
- `BACKLOG.md` — Phase 3 work-item tracker
- `HANDOFF.md` — session log (Phase 3 launch + continuation notes)
- `profiles/INDEX.md` — usage profiles + G + D gates + 4 profile clusters
- `docs/decisions/` — locked DRs (Phase 3.0/3.1/3.6)
- `drafts/composability-tooling.md` — composability tooling concepts (Phase 5+ ROADMAP)
- `archive/INDEX.md` — v0.35 archived corpus (consult during Phase 3+)
