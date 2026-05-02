# Architecture — Phase 3 rebuild (in progress)

> **Status**: Phase 3 ARCH rebuild ACTIVE. Phase 2 GLOSSARY foundational vocabulary lock COMPLETE (34 entries). This doc is the overview; per-topic detail will live in `arch/<topic-slug>.md` files as Phase 3.3+ topic content lands (directory not yet created).

## What this doc is

Layer 2 Overview per `MAINTENANCE.md` 5-layer doc model. Read on substantive sessions involving architectural work. Cites GLOSSARY entries (Layer 1; locked) + DRs (Layer 4; selective rebuild Phase 4) + specs (Layer 5; Phase 6 territory).

Currently captures **Phase 3 progress** + **locked architectural decisions** + **active disciplines** + **provisional topic taxonomy**. Migrates toward stable architectural overview as Phase 3 completes.

## Phase 3 sub-phase status

| Sub-phase | Scope | Status |
|---|---|---|
| **3.0** | Doc structure (single ARCHITECTURE.md vs topic-per-file vs hybrid) | ✅ LOCKED — hybrid |
| **3.1** | Open architectural questions (workflow / work-unit / deployment / engaged-authorship) | IN PROGRESS — workflow LOCKED; work-unit NEXT; deployment + engaged-authorship pending |
| **3.2** | Topic taxonomy (which 15-20 topics; aggregation vs 1:1 mapping) | Pending |
| **3.3** | Per-mechanism detail (12 mechanisms) | Pending |
| **3.4** | Per-architectural-Protocol detail (7 protocols + Pattern A primitives) | Pending |
| **3.5** | Per-primitive detail topics (9 primitives + axis-interactions) | Pending |
| **3.6** | Quality-gate ARCH topic | Pending |
| **3.7** | Cross-cutting investigations (PydanticAI re-eval; markdown-validation; Ming research; multi-VISION) | Pending |
| **3.8** | Coherence-audit Lenses 11-15 activation (phase-boundary audit before Phase 4) | Pending |

Foundation-up ordering applied (per `feedback_foundation_up_ordering.md`): questions before structure before content before audit.

## Doc structure (Phase 3.0 LOCKED)

**Hybrid**: single overview + per-topic files.

| Doc | Purpose | Lines | Status |
|---|---|---|---|
| `ARCHITECTURE.md` (this file) | Overview + topic catalog + cross-cutting principles + how topics compose + Phase 3 status tracking | ~1-2K | Active |
| `arch/<topic-slug>.md` × 15-20 | Per-topic detail | ~500 each | Not yet created (created as Phase 3.3+ produces topic content) |

**Why hybrid**: pure-single (10K lines) is unwieldy + context-budget concern; pure-multi has no entry point + cross-cutting orphaning. Hybrid aligns with progressive-disclosure principle (skill-craft pattern: SKILL.md → PROCEDURE.md → references/) + sharpen's AI-executor test (cognitive iteration via structure, not gist-extraction across 10K lines).

## Locked architectural decisions

### Workflow bipartite-classification (Phase 3.1) — LOCKED

**Resolution**: `workflow` re-classified to **bipartite Pattern B with optional applicability**:
- DEFINITION aspect: contained in specialist's distributable bundle (specialist DEFINITION at Framework C contains workflow definitions; not standalone Framework C primitive)
- INSTANCE aspect: workflow_instance entity at Owner B (per workspace per work-unit when codified pattern applies)
- **Optional applicability**: workflow_instance engages ONLY when work follows codified pattern. Ad-hoc work outside primitive scope (engages session + work-unit + skill + claim + event WITHOUT workflow_instance). Per workflow Round 2 + user push: ad-hoc work is first-class, not "degenerate Pattern B."
- Vocabulary disambiguation: `workflow` = the primitive; `workflow definition` = DEFINITION aspect; `workflow_instance` = INSTANCE aspect (entity-md per Owner B convention)

**workflow_pattern question** (cross-specialist shared workflows): RESOLVED via D gate mental modeling. Shared patterns live as **Layer A reusable templates / specialist-bundled bausteine** (content, NOT framework primitive). Watch-list signal: if Layer A growth proves insufficient for genuinely-cross-archetype pattern, examine then.

**Round 2 expansions applied**: vocabulary disambiguation; snapshot versioning at workflow_instance creation (preserves defensibility); composes with claim/skill/authority-binding/observability; lifecycle DEFINITION-vs-INSTANCE distinction (immutable per specialist version vs mutable-with-audit); evolution path (ad-hoc → codified through pattern recognition); failure modes (abandoned/failed/suspended) flagged for 3.5; multi-practitioner ownership flagged for 3.5.

**Validated under post-lock disciplines**: Round 1 + Round 2 revisit (with G gate + multi-axis + D gate applied) confirmed lock holds. 0 architectural REVISIONS surfaced.

**Full detail**: `GLOSSARY.md` workflow entry.

**Future DR target**: workflow bipartite-classification decision warrants Phase 4 DR (rationale + options considered + why B3 chosen) per coherence-audit Lens 14 (DR coverage gap). Not yet created.

## Disciplines applying to all ARCH work

These disciplines fire during architectural decision-making + validation. Codified via memory feedback rules + structural gates + sharpening skills.

### Validation gates (structural)

| Gate | Fires when | Blocks until |
|---|---|---|
| **G — Composability Gate** | Designing any L1-L4 producer artifact | Multi-mode consumption requirements satisfied (consulting / firm-reuse / OSS / marketplace-future / backup-migration) |
| **D — Defer Gate** | AI considers deferring any architectural item | Mental modeling within profile grounding attempted; defer only valid if mental modeling genuinely cannot resolve |

Both gates are STRUCTURAL — wrong shapes can't pass. Per `feedback_wrong_shapes_impossible.md`: prefer structural constraints that make wrong shapes impossible.

Gates are codified in `profiles/INDEX.md`. Decision-design-sharpening v0.4.0 references them in Round 2 stress-test list.

### Multi-axis validation (per `feedback_multi_axis_validation.md`)

Validate primitive classifications across three orthogonal dimensions:
- **Archetype**: planner / lawyer / researcher / auditor / etc.
- **Work-type within archetype**: codified workflow / ad-hoc exploratory / one-off communication / research-mode / maintenance / learning
- **Role**: practitioner / workflow-designer / specialist-author / instance-deployer / AI-runtime / multi-user-collaborator

Plus explicit non-coverage question: what use cases does primitive NOT cover; intentional or gap?

### Profile-grounded validation (per `profiles/INDEX.md`)

Profiles are persistent grounding for who-and-what the framework serves. Span lifecycle stages × shape variations × archetypes. Replace single-axis cross-archetype illustrations with multi-axis profile-anchored validation.

17 profiles (2 full + 15 skeletons). Skeletons fleshed out on-demand when specific decisions need them.

### Other disciplines

- **Foundation-up workflow ordering** (per `feedback_foundation_up_ordering.md`): items others depend on come first; downstream items that compose with multiple foundations come last; parallel-depth items batch with shared sharpening
- **2-round sweet spot** per architectural decision (per `feedback_pre_decision_sharpening.md` + sharpen v0.9.0)
- **Cascade discipline** (per `MAINTENANCE.md`): changes propagate up/down/sideways in same commit
- **Pattern-vs-instance** (per `feedback_pattern_not_instance_defers.md`): no instance-leakage; cross-archetype illustrations required
- **AI-as-runtime hybrid-shape** (per `feedback_ai_as_runtime.md`): don't add rule-encoding layer
- **Provenance hygiene** (per coherence-audit Lens 5 v0.2.1): no audit-history breadcrumbs in canonical content; provenance lives in HANDOFF + git log + commit messages

## Topic catalog (Phase 3.2 PROVISIONAL — not yet locked)

Provisional topic list per BACKLOG sub-phase 3.3-3.7. To be locked at Phase 3.2 (taxonomy decision: aggregation vs 1:1 mapping; file naming convention; cross-cutting topic placement).

### Phase 3.3 — Per-mechanism topics (12 mechanisms)

Foundation-up: defensibility-supporting mechanisms first.

- `arch/source-grounding.md` — every claim traces to source; framework-level enforcement
- `arch/audit-emission.md` — AuditEvent Pydantic schema; event_kind catalog
- `arch/audit-trail.md` — sequence-of-events composition; append-only discipline; retention policy
- `arch/sparring-sub-mechanisms.md` (or split per sub-mechanism) — counter-argument; confidence calibration; visible reasoning; selective friction; asymmetric knowledge respect; anti-sycophancy; commit-to-recommendations; what's-missing
- `arch/orchestration.md` — continuous decision layer; orchestrator skill mechanics
- `arch/persistent-state.md` — state across sessions; cross-session-handoff schema
- `arch/authority-binding.md` — actor_kind enum extension; authorization flow

### Phase 3.4 — Per-architectural-Protocol topics (7 Pattern A protocols)

Foundation-up: substrate first.

- `arch/substrate-protocol.md` (Surface specification + per-impl detail)
- `arch/adapter-protocol.md` (per-integration-class Surface specs)
- `arch/sparring-protocol.md` (Surface + impl variations)
- `arch/audit-protocol.md` (Surface + granularity-policy variation)
- `arch/coordination-protocol.md` (Surface + impl variations)
- `arch/trust-protocol.md` (Surface + trust-model variations)
- `arch/time-protocol.md` (Surface + temporal-semantics variations)

### Phase 3.5 — Primitive-detail topics + axis-interaction analysis

- `arch/specialist-mechanics.md` (granularity 3-test + composability + marketplace mechanics)
- `arch/skill-mechanics.md` (granularity 3-test + frontmatter schema + output validation)
- `arch/practitioner-mechanics.md` (deactivation + multi-practitioner + legal-entity context)
- `arch/workflow-mechanics.md` (representation schema + handoff + multi-session continuity + state machine + failure modes)
- `arch/session-mechanics.md` (boundary semantics + context-handoff + persistent-state migration)
- `arch/event-schema.md` (AuditEvent Pydantic shape + event_kind catalog)
- `arch/actor-mechanics.md` (full actor_kind enum + A2A + identity sourcing)
- `arch/claim-mechanics.md` (claim-event schema + revision + finalization + per-claim source-grounding)
- `arch/defensibility-mechanics.md` (conditions formalization + six-months-later test + regulatory-challenge schema)
- `arch/axis-interactions.md` (cross-axis composition; sparring within intertwining; defensibility resolves at claim-granularity in axis-1 work-products)

### Phase 3.6 — Quality-gate ARCH topic

- `arch/quality-gate.md` (runtime mechanism resisting category-collapse; Surface specification + per-shape variation + observability schema + intervention mechanics)

### Phase 3.7 — Cross-cutting investigations (varies by outcome)

- PydanticAI substrate evaluation outcome → may inform `arch/substrate-protocol.md` per-impl section
- Markdown-validation feasibility → may produce `arch/markdown-validation.md` topic
- Ming research deepening → may update VISION Foundations (or surface as separate analysis)
- Multi-VISION model decision → STRATEGY territory or VISION update

## Open architectural questions (Phase 3.1 remaining)

| Question | Status | Cascades from |
|---|---|---|
| **work-unit bipartite-classification** | NEXT (after current discussion) | workflow's resolution likely informs |
| "deployment" definition sharpening | Pending | workspace primitive |
| Engaged-authorship operational definition | Pending | defensibility primitive |

Resolution per Phase 3.1 protocol: Round 1 + Round 2 sharpening with G gate + multi-axis + D gate disciplines applied from start. Outcomes update GLOSSARY + may warrant Phase 4 DRs.

Workspace bipartite-classification (surfaced this session as candidate): D-gate-resolved during retrospective audit (workspace stays single-aspect; template aspect handled by L3 deployment template). No separate Round needed unless Round-style rigor preferred.

## Watch-list (architectural items awaiting external evidence)

Per D gate + `feedback_pattern_not_instance_defers.md` no-defer principle.

| Watch-list item | Awaited signal | Resolution mechanism |
|---|---|---|
| Shape-neutrality validation for second-shape productization | Second-shape design begins (autonomous-business OR personal-OS) | Validate primitive framings + new shape's policies handle variations cleanly; per-axis variants surface in shape policies |
| Cross-specialist shared workflow patterns insufficient via Layer A | If Layer A growth proves insufficient for genuinely-cross-archetype pattern | Examine then; `workflow_pattern` framework primitive remains unwarranted by default per workflow Round 2 D-gate resolution |

## Cross-cutting principles

### How topics compose

- **Mechanisms** (Phase 3.3) are atomic interface contracts; primitives + protocols + axes COMPOSE WITH multiple mechanisms
- **Protocols** (Phase 3.4) are Pattern A pluggable subsystems; Surface + Implementations + Selection
- **Primitives** (Phase 3.5) have rich detail per primitive
- **Quality-gate** (Phase 3.6) composes with mechanisms + axes + workflow + claim observability — cross-cutting integration topic
- **Axis-interactions** (Phase 3.5) — cross-axis composition pattern (sparring within intertwining; defensibility resolves at claim-granularity in axis-1 work-products) — cross-cutting topic

### Composability + boundaries (per G gate)

Every L1-L4 producer level (specialist / shape / template / workspace) must produce packageable artifacts that support multi-mode consumption. Architectural decisions that produce non-composable artifacts fail G gate. See `profiles/G-composability-gate.md`.

### Pattern-vs-instance discipline

Framework primitives stay shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer-instance specifics live at workspace level (per practitioner-shape policy mandates), NOT in framework primitive definitions. See `feedback_pattern_not_instance_defers.md` + `profiles/L5a-planner-pbs-schulz.md` (anchor profile demonstrates pioneer reality).

## Reading order at session start (per `MAINTENANCE.md`)

1. `DISCIPLINES.md` — cross-session working discipline
2. `VISION.md` — three-axis thesis + framework anchor
3. `MAINTENANCE.md` — doc system rules
4. `HANDOFF.md` — session log
5. `BACKLOG.md` — work-item tracker
6. `profiles/INDEX.md` — usage profiles taxonomy
7. **`ARCHITECTURE.md`** (this file) — Layer 2 overview when working in architectural area
8. `GLOSSARY.md` — vocabulary state (Layer 1)

Specific `arch/<topic>.md` files load on-demand when working in topic area.

## Cross-references

- `MAINTENANCE.md` — 5-layer doc model + cascade discipline + TOP-LEVEL ARCHITECTURE
- `VISION.md` — three-axis thesis + falsification + foundations
- `GLOSSARY.md` — Layer 1 vocabulary (34 locked entries)
- `BACKLOG.md` — Phase 3 work-item tracker
- `HANDOFF.md` — session log (Phase 3 launch + continuation notes)
- `profiles/INDEX.md` — usage profiles + G + D gates
- `drafts/quality-gate.md` — quality-gate exploratory draft (Phase 3.6 prerequisite)
- `drafts/composability-tooling.md` — composability tooling concepts (Phase 5+ ROADMAP)
- `archive/INDEX.md` — v0.35 archived corpus (consult during Phase 3+)
