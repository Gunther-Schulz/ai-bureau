# DR: work-unit bipartite-classification (Pattern B; always-present container)

**Status**: ACCEPTED (Phase 3.1 lock)
**Locked**: session 16 (2026-05-02)
**Sharpening**: 2-round pattern (Round 1 full monty + Round 2 user-triggered) under G + multi-axis + D gate disciplines
**Phase**: 3.1 (open architectural questions; cascades from workflow's resolution earlier this session)

## Decision

`work-unit` is **bipartite multi-aspect Pattern B** parallel to `specialist` + `workflow`:
- **KIND DEFINITION aspect**: specialist-defined kind discriminator + per-kind structural conventions; lives at Framework C via specialist's distributable bundle (specialists declare supported `work-unit kind`s in their DEFINITION)
- **INSTANCE aspect**: `work-unit instance` entity at Owner B (workspace-scope managed entity per workspace per active kind)
- **Always-present container** (load-bearing asymmetry vs workflow): every accountability-bearing piece of work IS a work-unit. No optional-overlay discount.
- **Vocabulary**: `work-unit` = primitive; `work-unit kind` = DEFINITION aspect; `work-unit instance` = INSTANCE aspect

## Context

Work-unit GLOSSARY entry was locked Phase 2 with explicit hedge: "Could be reclassified bipartite Pattern B (parallel to specialist) if Phase 3 ARCH determines kind-discriminator deserves multi-aspect treatment. Currently single-aspect cross-cutting." Workflow's resolution earlier in session 16 set the precedent (bipartite Pattern B + optional applicability); work-unit's parallel question became immediate cascade work.

Critical insight surfaced in Round 1: work-unit's asymmetry vs workflow. Workflow is OPTIONAL overlay (engages only when codified pattern); work-unit is ALWAYS-PRESENT (every accountability-bearing piece of work IS a work-unit, regardless of workflow primitive engagement). Reciprocal property — surfaced from Lens 6 symmetry consideration during Round 2 user prompt.

## Adoption options considered

**Q1 type classification**:
- **A**: Keep single-aspect cross-cutting (kind discriminator just data inside specialist DEFINITION; no multi-aspect elevation)
- **B (CHOSEN)**: Bipartite Pattern B parallel to specialist + workflow; KIND DEFINITION at Framework C via specialist + INSTANCE at Owner B
- **C**: Bipartite WITH optional applicability (mirror workflow's ad-hoc-vs-codified branching)

## Rationale for B

**Kind discriminator deserves multi-aspect treatment** — not just data; structural conventions per kind matter (lifecycle states, artifact attachment shape, audit-trail attribution semantics differ per kind). Bipartite Pattern B captures this cleanly: DEFINITION aspect holds the conventions; INSTANCE aspect holds workspace-bound state.

**Parallel structure with workflow + specialist**: three Pattern B primitives composing coherently — specialist DEFINITION holds work-unit kinds + workflow definitions; workspace activates specialists; work-unit instances + workflow_instances live at Owner B.

**Option C rejected upfront**: work-unit has NO ad-hoc-vs-codified branching. Every accountability-bearing piece of work IS a work-unit; ad-hoc work doesn't live "outside" work-unit primitive. Optional-applicability discount would fabricate a branch that doesn't exist.

## Always-present container (load-bearing asymmetry)

Reciprocal to workflow's optional applicability:

| Property | work-unit | workflow_instance |
|---|---|---|
| Engagement | always-present | optional overlay |
| Trigger | accountability-bearing work | codified pattern existence |
| Cardinality vs other | 1 anchor → N workflow_instances | 1 instance → 1 work-unit |
| Ad-hoc support | first-class (no workflow required) | n/a (ad-hoc work has no workflow_instance) |

This asymmetry is what makes ad-hoc work first-class supported in the framework: work-unit primitive is always-engaged anchor; workflow primitive is opt-in via codified pattern.

## Refinements applied (Round 2 expansions)

| ID | Refinement | Status |
|---|---|---|
| E1 | Always-present subsection (Lens 6 reciprocal symmetry to workflow's optional applicability) | Applied to GLOSSARY canonical (work-unit + workflow reciprocal cross-ref) |
| E2 | Kind-namespace disambiguation (multiple specialists offering same kind name; resolved via active-specialist set + creator's specialist context) | Applied as note + flagged for Phase 3.5 schema-detail |
| E3 | Multi-workflow_instance composition against single work-unit (cardinality asymmetry: 1 work-unit ↔ N workflow_instances; potentially across specialists) | Applied to Composes-with (work-unit + workflow reciprocal) |
| E4 | Kind snapshot semantics on instance creation (mirrors workflow_instance definition-snapshot; preserves audit integrity if specialist version bumps) | Applied to lifecycle subsection; flagged for ARCH 3.5 schema |
| E5 | Quality-gate observability source (work-unit lifecycle events + per-claim emissions feed quality-gate drift detection) | Applied to Composes-with `quality-gate` |
| E6 | Multi-practitioner authorship (federation + multi-user shapes; signing/attribution semantics per shape policy) | Applied to Cardinality + lifecycle; flagged for ARCH 3.5 |
| E7 | Authority binding on lifecycle transitions (who can transition initiated→in-progress→sent→archived per shape policy) | Applied to Composes-with `mechanism` |
| E8 | Orphan instances on specialist deactivation (preserved per persistence rule; reactivation restores; no auto-archive) | Applied to lifecycle subsection |

## REVISION-grade stress-tests

| ID | Test | Verdict |
|---|---|---|
| **R1** | Should kind be split into PRIMITIVE in own right (separate `work-unit kind` + `work-unit instance` GLOSSARY entries)? | **REJECTED** — Pattern B keeps both aspects under one primitive name (matches workflow + specialist precedent); splitting fragments vocabulary; loses reciprocal anchoring. |
| **R2** | Does "always-present" hold across all shapes? Test autonomous-business-shape ephemeral AI batches — could they be sub-work-unit ephemera? | **REJECTED revision** — accountability-bearing batch = work-unit regardless of duration. Autonomous-business-shape work-units are shorter-lived (minutes vs weeks) but always-present property holds. Ephemeral ≠ absent. |
| **R3** | Should kind be MOVED out of specialist DEFINITION to its own Framework C placement (kind as standalone distributable)? | **REJECTED** — kinds are inseparable from specialist competence (specialist that "knows how to do project work" owns `project` kind); decoupling creates orphan kinds with no codified-handler. |

## Composition with existing architecture

| Existing primitive | Composition |
|---|---|
| `specialist` (Pattern B) | Specialists DEFINE work-unit kinds at work-unit's DEFINITION aspect (kind discriminator + per-kind structural conventions in specialist's bundle); workspace's active specialists determine which kinds are available. **Two Pattern B primitives composing**. |
| `workflow` (Pattern B with optional applicability) | Workflow_instance attaches to work-unit instance when codified pattern applies. Cardinality asymmetry: 1 work-unit ↔ N workflow_instances. Reciprocal: work-unit always-present + workflow_instance optional-overlay. **Two Pattern B primitives composing cleanly**. |
| `workspace` | Contains work-unit instances at Owner B; cardinality multiple per workspace per active kind |
| `Owner B scope` | Work-unit INSTANCE aspect lives there as workspace-scope managed entity |
| `Framework C scope` | Work-unit KIND DEFINITION aspect lives there via specialist's distributable bundle |
| `event` | Work-unit lifecycle emits events (work_unit_created / state_transitioned / work_unit_completed / sent / archived); audit-emission captures |
| `claim` | Claims compose into work-unit instance output content (1 work-unit → N claims) |
| `practitioner` | Practitioners sign work-unit outputs; defensibility test resolves at work-unit granularity (composable from claim-level tests) |
| `mechanism` | Composes with persistent-state, audit-emission, authority-binding (lifecycle transitions per shape policy) |
| `quality-gate` (Pattern A) | Work-unit lifecycle + per-claim emissions feed quality-gate's drift detection (e.g., rapid sign-off cadence → axis-3 rubber-stamping signal at attestation moment) |

## Defers (D-gate-validated; Phase 3.5 schema territory)

| Defer | Awaited signal | Reason valid |
|---|---|---|
| Per-kind structural conventions schema (lifecycle states; artifact attachment shape; audit attribution semantics) | Phase 3.5 work-unit-mechanics ARCH topic | Schema-detail per-kind |
| Kind-namespace disambiguation mechanics (resolution algorithm when multiple specialists offer same name) | Phase 3.5 ARCH topic | Mechanism-detail |
| Multi-workflow_instance composition mechanics (parallel + sequential composition against single work-unit) | Phase 3.5 ARCH topic | Composition mechanics |
| Multi-practitioner authorship + signing semantics | Phase 3.5 + per-shape policy work | Per-shape policy variation |
| Authority-binding lifecycle transitions schema | Phase 3.5 + per-shape policy | Per-shape policy variation |
| Orphan-instance handling specifics (UI exposure; reactivation flow) | Phase 3.5 ARCH topic | Implementation-specific |

D Gate verdict: all defers genuine schema-detail (HOW), not architectural-decision (WHAT). All defers valid.

## Constraints flowing

This decision flows constraints into:
- **Phase 3.4** per-architectural-Protocol detail (Substrate + Adapter Pattern A; specialist Pattern B; — work-unit Pattern B may not need Phase 3.4 dedicated topic since structural overlay simpler than Pattern A protocols)
- **Phase 3.5** primitive-detail topics (work-unit-mechanics ARCH topic: per-kind conventions schema + kind-namespace + lifecycle state machine + multi-workflow_instance composition + orphan handling)
- **Phase 3.3** per-mechanism detail (audit-emission + authority-binding compose with work-unit lifecycle; their detail informs work-unit's transition mechanics)
- **Phase 3.6** quality-gate full ARCH topic (work-unit observability source for quality-gate signals)
- **Phase 6** workspace serialization spec (work-unit instance entity-md schema part of workspace state portability)

## Files touched

- `GLOSSARY.md` work-unit entry (rewrite: Class + Layer + Vocabulary disambiguation + Canonical + What-it-is + Always-present subsection + Cardinality+lifecycle + What-it-is-NOT + Cross-archetype + Boundary test + Composes-with + Source + See)
- `GLOSSARY.md` workflow entry (Optional applicability subsection: reciprocal cross-ref to work-unit's always-present)
- `GLOSSARY.md` workflow Composes-with `work-unit` (sharpened to reflect bipartite cleanness + cardinality asymmetry)
- `GLOSSARY.md` specialist Composes-with `work-unit` (sharpened to "specialists DEFINE work-unit kinds at work-unit's DEFINITION aspect")
- `GLOSSARY.md` Owner B scope members list (sharpened "work-unit instances per Pattern B INSTANCE aspect")
- `GLOSSARY.md` Owner B scope Composes-with `work-unit` (Pattern B reference)
- `GLOSSARY.md` TOC entries (work-unit + workflow Pattern B annotations)
- `ARCHITECTURE.md` Locked architectural decisions section (work-unit lock entry added)
- `ARCHITECTURE.md` Phase 3 sub-phase status table (3.1 work-unit LOCKED)
- `BACKLOG.md` Phase 3.1 (work-unit bipartite-classification → Resolved)
- `docs/decisions/work-unit-bipartite-classification.md` (this file)

## Revisit triggers

This DR should be revisited if:
- Phase 3.5 work-unit-mechanics ARCH detail surfaces operational concerns the bipartite shape can't accommodate
- Second-shape productization (autonomous-business OR personal-OS) reveals work-unit semantics differ structurally beyond shape-policy variation
- Multi-practitioner authorship work surfaces structural concerns requiring framework-level (not just shape-policy) treatment
- Multi-workflow_instance composition mechanics reveal Pattern B insufficient (e.g., parallel composition needs primitive-level coordination support)
- Pioneer-deployment data shows kind-namespace disambiguation is structurally insufficient

## Sharpening rounds metadata

- **Round 1**: AI full monty — 3 adoption options + 11 stress tests (ST1-ST11) + Round 1 position committed (Option B: Pattern B parallel to workflow + specialist; without optional-applicability discount; always-present anchor)
- **Round 2**: USER-TRIGGERED + USER-PROMPTED LENS-6 SYMMETRY CHECK — 8 EXPANSIONS applied (E1-E8; including always-present subsection per user's Lens 6 prompt) + 3 REVISION-candidates rejected (R1-R3 manufactured criticism)
- **Self-check**: STABLE; 0 architectural REVISIONS; all findings EXPANSIONS or rejected manufactured criticism

Total: 2 rounds. Per `feedback_pre_decision_sharpening.md` 2-round sweet spot empirical pattern. Narrow architectural surface (single primitive re-classification cascading from established workflow pattern) → 2 rounds sufficient.
