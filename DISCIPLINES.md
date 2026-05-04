# Working disciplines — how we operate across sessions

This document persists the cross-session working discipline for pbs-bureau development. **Read at session start** alongside `VISION.md` + `MAINTENANCE.md` + `HANDOFF.md` + `BACKLOG.md`.

Scope: this doc is **cross-session** — applies to all future dev work on this project regardless of phase. Phase-specific state (current rebuild progression, what we're working on now) lives in `HANDOFF.md`.

This file is the **index**. Per-discipline detail lives in `disciplines/<NN-slug>.md`, loaded on-demand when the discipline fires. Splitting prevents the foundational session-start load from breaching context-budget thresholds where instruction-adherence collapses.

---

## Working procedure

**The flow**: AI proposes positions → user adjusts/challenges/confirms → AI persists on sign-off.

- **Decision phase** (positions, framings, choices): user approval needed before persistence
- **Content phase** (markdown content following locked decisions): write directly without per-content approval
- **Commit positions, don't menu**: AI commits to recommendations with rationale; user shapes via challenge or confirmation. Avoid presenting open menus.
- **Commit and push often**: no per-commit confirmation needed; treat push as part of commit
- **Scope-bounded autonomous authority grant**: when user grants scope-bounded autonomy (e.g., "until next /clear checkpoint" / "go ahead through Wave-N" / "do all tasks for this cluster"), AI proceeds through subsequent decision-phases within that scope without per-step confirmation. Chat surfaces still carry positions/decisions/reasons (decision-phase visibility preserved); locks happen en bloc; sub-agent dispatch + content-phase work proceed automatically. Per `CLAUDE.md` "Executing actions with care": authorization stands for the scope specified — NOT beyond. Match action scope to what was requested. Composes with `feedback_propose_before_commit.md` + `feedback_judgment_and_automate.md` decision-vs-content-phase distinction. Canonical exemplar: HANDOFF Note 58 cluster-execution (workflow-work-unit primitive-cluster Wave-1 + Wave-2 + Wave-2.5 + HANDOFF write proceeded post Round-2-lock without per-step user confirmation).
- **Effort-level switch suggestion is a pause-point even within autonomous scope**: when AI judges that switching effort level (xhigh ↔ high) would better match the upcoming workload-class, AI surfaces the suggestion AND pauses for user confirmation before proceeding. User decides whether to switch; AI does not auto-toggle. Sizing rationale per `process-kit/structural-invariants.md` "Sizing principle" (cost-of-error + reasoning-density govern mitigation depth): reasoning-dense moments (Round 1/2 sharpening, lock decisions, audit reasoning, Reviewer roles) → xhigh; generation-dense pattern-execution (Cascade-Writer, well-specified mechanical cascades) → high. Symmetric for both downshifts (xhigh → high) and upshifts (high → xhigh). Effort changes materially affect cost + speed; pause is appropriate within otherwise-autonomous scope.

Per memory: `feedback_propose_before_commit.md`, `feedback_judgment_and_automate.md`, `feedback_push_after_commit.md`.

---

## Cross-session disciplines (index)

Each row links to the per-discipline file with full detail (sub-sections, examples, "How to apply", failure surfaces, canonical exemplars). When a discipline fires, READ the linked file before applying.

| # | Discipline | When it fires | Detail |
|---|---|---|---|
| 1 | Source-grounded; cite file:line; flag synthesis vs citation | Asserting what a doc/DR says; starting substantive work; invoking specialized skill or profile-anchored validation | `disciplines/01-source-grounded.md` |
| 2 | Apply principle uniformly | User states a principle/goal; applying any principle across categories | `disciplines/02-apply-principle-uniformly.md` |
| 3 | Pre-decision sharpening | At decision-formation moments before locking; primitive proposals (multi-axis); high-impact decisions (profile-anchored) | `disciplines/03-pre-decision-sharpening.md` |
| 4 | Cascade prevention (greenfield-draft + minimize-embedded + cascade-pass + foundation-first) | Locking new architectural commitment that depends on or composes with prior work | `disciplines/04-cascade-prevention.md` |
| 5 | No-defer; mental-model first; surface info-gaps as watch-list entries | AI considers deferring any architectural item; D Gate procedure activates | `disciplines/05-no-defer.md` |
| 6 | Anchored vs preliminary-locked | Considering whether to revise a decision / commitment / ARCH entry / spec | `disciplines/06-anchored-vs-preliminary-locked.md` |
| 7 | Cascade discipline (structural consistency) | Changing any concept, decision, primitive, or term in any doc | `disciplines/07-cascade-discipline.md` |
| 8 | Foundation-up workflow ordering | Compositional / architectural work (GLOSSARY, DRs, ARCH, specs, layered design) | `disciplines/08-foundation-up-ordering.md` |
| 9 | Coherence-audit cadence | Phase 3-6 work checkpoints; mid-phase trigger conditions; BACKLOG-scheduled checkpoints | `disciplines/09-coherence-audit-cadence.md` |
| 10 | Greenfield evaluation of archived material | ARCH/DR/spec work cites archived material; Round 1 sharpening surfaces archive citation; Round 2 termination self-check | `disciplines/10-greenfield-evaluation.md` |
| 11 | Effort-switch cluster-execution map | At dispatch-class transitions during Phase 3.5+ cluster-execution; at audit-checkpoint executions (C1-C5) | `disciplines/11-effort-switch-cluster-map.md` |

Anchor-stable section headings below preserve resolvability of existing `DISCIPLINES.md#discipline-N-...` cross-references from other docs. Each section is a one-line summary + cross-ref to per-discipline file.

## Discipline 1 — Source-grounded; cite file:line; flag synthesis vs citation

Read source before asserting; calibrate confidence by basis (citation vs summary vs synthesis); pattern-matching from memory is NOT direct evidence. Includes re-grounding sub-section (VISION + ARCHITECTURE for substantive work) and skill+profile sub-section (READ SKILL.md / `profiles/INDEX.md` at every invocation).

Detail: `disciplines/01-source-grounded.md`.

## Discipline 2 — Apply principle uniformly

Enumerate categories independent of inherited framings; test each; verify "no" boundaries are genuine. When user pushes a second/third time to surface a missed category, the inherited-framings filter wasn't disabled.

Detail: `disciplines/02-apply-principle-uniformly.md`.

## Discipline 3 — Pre-decision sharpening

Round 1 = full monty; Round 2+ = user-triggered. Sweet spot per surface type (architectural-decision / procedure-document / set-level audit / meta-architectural). Layered coverage observation. Mode 1 emergent + Mode 2 upfront-known composite decomposition. Includes multi-axis validation sub-section (archetype × work-type × role + non-coverage) and profile-anchored validation sub-section.

Detail: `disciplines/03-pre-decision-sharpening.md`.

## Discipline 4 — Cascade prevention (greenfield-draft + minimize-embedded + cascade-pass + foundation-first)

Greenfield-draft from primary sources; minimize embedded descriptions of not-yet-locked terms; run cascade-pass at lock-time (not deferred); lock foundation-first when sequence has discretion.

Detail: `disciplines/04-cascade-prevention.md`.

## Discipline 5 — No-defer; mental-model first; surface info-gaps as watch-list entries

Run D Gate (mental-modeling test + external-information test + effort-asymmetry test) before any defer. If mental modeling resolves → evolve answer NOW. If genuinely external-info-gap → surface as watch-list entry naming specific external signal.

Detail: `disciplines/05-no-defer.md`.

## Discipline 6 — Anchored vs preliminary-locked

VISION axes anchored (revise only on real-world falsification); everything else preliminary-locked (current best position; revisable when VISION ideal design demands).

Detail: `disciplines/06-anchored-vs-preliminary-locked.md`.

## Discipline 7 — Cascade discipline (structural consistency)

Changes propagate up, down, and sideways — identify every other place a changed concept appears and update each in the same commit (or tightly-coupled sequence completing the cascade).

Detail: `disciplines/07-cascade-discipline.md`. Detailed mechanism: `MAINTENANCE.md` "TOP-LEVEL RULE — Cascade discipline".

## Discipline 8 — Foundation-up workflow ordering

Default to foundation-up: items others depend on come first; downstream items last; parallel-depth items batch with shared sharpening passes.

Detail: `disciplines/08-foundation-up-ordering.md`.

## Discipline 9 — Coherence-audit cadence

5 hard checkpoints (C1-C5 across Phase 3.4 / 3.5 / 3.8 / 6 pre-impl / 6 close) + 3 trigger conditions (5+ DRs accumulated / composite-DR lock / pre-promotion-to-stability). Codifies WHEN audits run; `coherence-audit` SKILL.md codifies HOW.

Detail: `disciplines/09-coherence-audit-cadence.md`.

## Discipline 10 — Greenfield evaluation of archived material

Each cited archived element MUST be greenfield-evaluated against current locked vocabulary — NOT transcribed as template. Archive embodies pre-rebuild commitments, much of which was unlocked / instance-anchored / contradiction-bearing per rebuild rationale.

Detail: `disciplines/10-greenfield-evaluation.md`.

## Discipline 11 — Effort-switch cluster-execution map

Operationalizes the Working-procedure "Effort-level switch suggestion is a pause-point" bullet by enumerating exact dispatch-points where AI surfaces switch suggestions during cluster execution. 3-toggle practical map for primitive-cluster cluster-execution: `xhigh → high` before Wave-2 Cascade-Writer (step 14); `high → xhigh` before Wave-2 Cascade-Reviewer (step 16); `xhigh → high` before HANDOFF write (step 25). Audit checkpoints (C1-C5) follow different shape: stay xhigh; downshift only when dispatching cascade-execution sub-agents.

Detail: `disciplines/11-effort-switch-cluster-map.md`.

---

## Architectural foundation (current rebuild — see `MAINTENANCE.md` for detail)

The foundational architectural commitments that future sessions inherit:

- **Repo identity: framework source, not deployment instance**: this repo holds framework + dev tooling only; app skills + per-deployment instance content belong in deployment workspaces, not here
- **Framework = MECHANISMS; Shape = POLICIES** (foundational architectural commitment)
- **Atoms vs containers**: `mechanism` + `policy` are atomic primitives; `framework` + `shape` are meta-primitive containers
- **A-B-C scope model** (preliminary-locked): Framework C (definitions) + Owner B (instances) derived from framework/shape; Layer A (layered content) orthogonal axis
- **5-layer doc structure**: Entry → Foundations → Overview → Architecture detail → DRs → Specs (+ Memory orthogonal)
- **GLOSSARY entry classification**: 4-axis tagging (Class / Layer / Axis / VISION usage)

Detail in `MAINTENANCE.md` "TOP-LEVEL SCOPE" + "TOP-LEVEL ARCHITECTURE" sections.

---

## Discipline map — when each fires

Disciplines compose. Different disciplines fire at different decision moments. This table shows when each engages so AI applies the right ones in context.

### Validation gates (structural; fire before specific work proceeds)

| Gate | Fires when | Codified at |
|---|---|---|
| **G — Composability Gate** | Designing any L1-L4 producer artifact (specialist / shape / template / workspace) | `profiles/G-composability-gate.md` + `profiles/INDEX.md` |
| **D — Defer Gate** | AI considers deferring any architectural item | `profiles/INDEX.md` "D Gate procedure" + `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 |

### Decision-design disciplines (fire during architectural decisions)

| Discipline | Fires when | Codified at |
|---|---|---|
| Pre-decision sharpening (Round 1 full monty + Round 2 user-triggered; sweet spot per surface type) | Substantive architectural decisions | `disciplines/03-pre-decision-sharpening.md` + `plugin/skills/decision-design-sharpening/` |
| Multi-axis validation (archetype × work-type × role + non-coverage) | Primitive classification proposals | `disciplines/03-pre-decision-sharpening.md` (multi-axis sub-section) + `profiles/INDEX.md` |
| Foundation-up workflow ordering | Compositional/architectural work (GLOSSARY, DRs, ARCH, specs) | `disciplines/08-foundation-up-ordering.md` |
| Apply principle uniformly | When user states a principle/goal | `disciplines/02-apply-principle-uniformly.md` |
| Decision-phase approval; content-phase no approval | Surfacing positions/framings to user | `feedback_propose_before_commit.md` + `feedback_judgment_and_automate.md` |

### Cross-session work disciplines (fire on every substantive session)

| Discipline | Fires when | Codified at |
|---|---|---|
| Re-ground in VISION + ARCH | Start of substantive PBS work | `disciplines/01-source-grounded.md` (re-grounding sub-section) |
| Source-grounded; cite file:line | Asserting what a doc/DR says | `disciplines/01-source-grounded.md` |
| Cascade discipline | Changing concept/primitive/term in any doc | `MAINTENANCE.md` "TOP-LEVEL RULE — Cascade" |
| Commit regularly + push after commit | Per-logical-unit work completion | `feedback_push_after_commit.md` |
| LLM-instruction tightness for markdown layer | Authoring skill / ARCH / GLOSSARY content | `ARCHITECTURE.md` cross-cutting principles "LLM-instruction tightness" |

### Architectural commitments (anchor framework decisions)

| Commitment | Codified at |
|---|---|
| AI as runtime, not consumer | `ARCHITECTURE.md` cross-cutting principles "AI as runtime" |
| Make wrong shapes impossible (structural over conventional) | `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 |
| Pattern-vs-instance discipline | `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 |
| Repo identity: framework source, not deployment instance | `MAINTENANCE.md` TOP-LEVEL SCOPE |
| Preliminary lock except VISION axes | `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 |

### Audit + coherence disciplines (fire during corpus validation)

| Discipline | Fires when | Codified at |
|---|---|---|
| Coherence-audit 10 universal lenses + corpus-specific | Cross-decision corpus validation | `plugin/skills/coherence-audit/` |
| Audit scaling strategies (cluster compression / deltas / on-demand fleshing / sampling / full systematic) | Audit-load-management decisions | `plugin/skills/coherence-audit/` "Audit scaling strategies" |
| Provenance hygiene (no audit-history breadcrumbs in canonical content) | Applying lock revisions | coherence-audit Lens 5 |
| Profile-grounded validation | Pre-validation + post-validation | `profiles/INDEX.md` |

### Operational disciplines

| Discipline | Fires when | Codified at |
|---|---|---|
| Stop on block; don't work around | Hook/permission/sandbox blocks | `feedback_blocked_actions.md` |
| Plugin reload doesn't sync marketplace clone | Stale skill list after pushing plugin changes | `feedback_plugin_marketplace_clone_sync.md` |

---

## Memory composition (cross-session AI behavioral preferences)

Memory holds **cross-session AI behavioral preferences only**. Operational disciplines (HOW we operate) are absorbed into THIS doc; architectural commitments are absorbed into MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES + ARCHITECTURE.md cross-cutting principles.

| File | Role |
|---|---|
| `feedback_propose_before_commit.md` | Decision phase = approval needed for positions/framings (chat surfaces decisions+reasons, NOT verbatim content); content phase = write directly |
| `feedback_judgment_and_automate.md` | Commit positions instead of menus; routine work without asking |
| `feedback_push_after_commit.md` | Push immediately after each commit |
| `feedback_blocked_actions.md` | Surface hook/permission/sandbox blocks immediately; never workaround |
| `feedback_plugin_marketplace_clone_sync.md` | Operational tool note (marketplace clone sync mechanics) |

Memory location: `/home/g/.claude/projects/-home-g-dev-Gunther-Schulz-pbs-bureau/memory/`. Index: `MEMORY.md` in same directory.

---

## When this doc itself changes

DISCIPLINES.md is foundational. Changes affect every subsequent session's discipline.

- Identify what existing discipline is being changed/added/removed; update relevant per-discipline file in `disciplines/` if detail changes
- Cascade-pass: any docs referencing the changed discipline get updated in same commit; verify memory feedback files still compose
- This doc is preliminary-locked like everything else (per Discipline 6) — but changes should be deliberate, not casual
