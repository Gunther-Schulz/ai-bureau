# DR: workflow bipartite-classification

**Status**: ACCEPTED
**Locked**: session 16 (2026-05-02)
**Sharpening**: 2-round pattern (Round 1 full monty + Round 2 user-triggered) + retrospective revisit under new disciplines (G + multi-axis + D gate)
**Phase**: 3.1 (open architectural questions)

## Decision

Re-classify `workflow` primitive from **single-aspect cross-cutting** to **bipartite Pattern B with optional applicability**:
- DEFINITION aspect: contained in specialist's distributable bundle (specialist DEFINITION at Framework C contains workflow definitions; not standalone Framework C primitive)
- INSTANCE aspect: workflow_instance entity at Owner B
- **Optional applicability**: workflow_instance engages ONLY when work follows codified pattern. Ad-hoc work outside primitive scope (engages session + work-unit + skill + claim + event WITHOUT workflow_instance).

## Vocabulary

- `workflow` = the primitive (the abstraction; bipartite Pattern B)
- `workflow definition` = DEFINITION aspect (reusable pattern in specialist's bundle)
- `workflow_instance` = INSTANCE aspect (specific run-through; entity-md per Owner B convention)

## Context

Pre-Phase-3 lock (session-16 mid-rebuild) had `workflow` tagged single-aspect cross-cutting with bipartite-candidacy hedge:
> *"DEFINITION aspect (the pattern itself: 'how does B-Plan-Begründung drafting actually proceed?') could be Framework C OR Layer A (domain-keyed); the INSTANCE aspect (workflow execution in a specific workspace) is realized through sessions over time. Phase 3 ARCH resolves whether workflow is single-aspect cross-cutting (current) or bipartite Pattern B."*

Phase 3.1 first item: resolve this hedge.

## Adoption options considered

| Option | Shape | DEFINITION location | INSTANCE location |
|---|---|---|---|
| **A** | Single-aspect cross-cutting (current at lock-time) | n/a — workflow lives wherever; no scope partition | n/a |
| **B1** | Bipartite Pattern B — Framework C standalone | Framework C (workflows as standalone framework primitives) | Owner B (workflow_instance per workspace) |
| **B2** | Bipartite Pattern B — Layer A definition | Layer A (workflows as domain-keyed knowledge) | Owner B |
| **B3 (CHOSEN)** | Bipartite Pattern B — specialist-bundled | Specialist DEFINITION (Framework C via composition; workflows compose into specialist's bundle) | Owner B (workflow_instance) |

## Rationale for B3

1. **Workflow PATTERN is genuinely reusable** (B-Plan-Begründung drafting structure applies across many Bebauungspläne) — bipartite captures the reuse-vs-instance gap that single-aspect glosses over
2. **Workflows aren't standalone framework primitives** — they're specialist-bundled (PlanningSpecialist defines its workflows; AuditingSpecialist defines its workflows) — DEFINITION inherits specialist's Framework C placement via composition; doesn't need workflow as its own Framework C member
3. **Aligns with foundation-up**: specialist (Pattern B Framework C) is the foundational primitive; workflow rides on its structure rather than competing
4. **Cross-archetype**: legal practice's "case-management workflow" lives in LegalSpecialist; research lab's "manuscript-review workflow" lives in ResearchSpecialist — pattern holds

## Why not other options

**Option A (single-aspect cross-cutting)**: doesn't explain the reusability gap. Pattern + instance are genuinely different concepts. Single-aspect makes the architecture lossy.

**Option B1 (Framework C standalone)**: implies workflows are framework-level distributable units — but they're inherently domain/specialist-shaped (B-Plan workflow is planning-specific). Making them Framework C requires workflows to be domain-neutral (impossible) OR Framework C accepts domain-shaped definitions (breaks framework purity).

**Option B2 (Layer A definition)**: Layer A is domain-keyed knowledge (templates, conventions, references). Workflows could fit there but workflows are PROCEDURAL not REFERENCE — they describe how to do work, not what to consult. Specialist DEFINITION is the procedural-bundle home; Layer A is the reference-content home. Different content types.

## Critical refinement: optional applicability

User push during Round 2 surfaced the ad-hoc work case. Round 1 framing implied workflow_instance attaches to every work-unit; user observed: "in practice not everything a practitioner does is tied to a predefined workflow. many processes will be ad-hoc."

**Revised framing (REVISION-grade)**: workflow_instance engages OPTIONALLY — only when work follows a codified pattern. Ad-hoc work-units have NO workflow_instance — they're carried by session(s) + work-unit + skill firings + claim emissions + events alone. Workflow primitive is OPTIONAL structural overlay, not mandatory companion to work-unit.

This generalizes to **partial coverage**: one work-unit may have ZERO / ONE / or MULTIPLE workflow_instances attached over its lifecycle, with ad-hoc phases between them.

Round 1 ST4 had framed ad-hoc as "degenerate Pattern B case." Better framing: ad-hoc work outside workflow primitive scope entirely.

## Cross-specialist shared workflow patterns (workflow_pattern question)

Round 2 ST9 deferred this with watch-list signal. Retrospective D Gate mental modeling resolved it:

**Cross-specialist shared workflow patterns live as Layer A reusable templates / specialist-bundled bausteine** (content, NOT framework primitive). Watch-list signal: if Layer A growth proves insufficient for genuinely-cross-archetype pattern, examine then.

**No `workflow_pattern` framework primitive needed.** Mental modeling resolved the question via available tools (profiles + multi-axis + G gate). The defer was unnecessary; D Gate now codifies that mental modeling fires before defer.

## Refinements applied (Round 2 expansions)

| ID | Refinement | Status |
|---|---|---|
| E1 | Vocabulary disambiguation (workflow / workflow definition / workflow_instance) | Applied to GLOSSARY canonical |
| E2 | Workflow definition versioning: snapshot semantics at workflow_instance creation (preserves defensibility) | Applied; flag for 3.5 schema |
| E3 | Composition with claim (per-claim attribution to workflow_instance) | Applied; cascade-pass to claim entry |
| E4 | Composition with skill (consumption direction: workflow → skill) | Applied |
| E5 | Authority-binding integration (per-phase authority requirements) | Flag for 3.5 schema |
| E6 | Observability beyond lifecycle events (per-phase events; quality-gate composition source) | Applied; flag for 3.6 quality-gate ARCH topic |
| E7 | Mutability semantics (DEFINITION immutable per specialist version; INSTANCE mutable-with-audit) | Applied to GLOSSARY canonical |
| E8 | Failure modes (abandoned / failed / suspended terminal + non-terminal pause) | Flag for 3.5 schema |
| E9 | Multi-practitioner ownership (primary_practitioner + collaborator list) | Flag for 3.5 schema |
| R1 | workflow_pattern cross-specialist shared (Round 2 → defer; D Gate retrospective → Layer A resolution) | Applied; not a framework primitive |

## Cascade applied

GLOSSARY entries updated with reciprocal references:
- `specialist`: workflow definitions in bundle
- `workspace`: workflow_instance at Owner B; capability addition orthogonal to running workflow_instance
- `session`: workflow_instance can span multiple sessions
- `claim`: workflow_instance attribution; ad-hoc claims attribute to work-unit + session
- `event`: workflow_instance lifecycle events
- `intertwining (axis 1)`: applies to codified + ad-hoc work
- `work-unit`: workflow_instance attaches optionally; bipartite-candidacy hedge cascades from workflow's resolution

## Composition with existing architecture

| Existing primitive | Composition |
|---|---|
| `specialist` (Pattern B) | Specialist DEFINITION contains workflow definitions; specialist INSTANCE-CONTENT may include workflow_instance entities |
| `work-unit` | One workflow_instance ↔ one work-unit when codified pattern applies; ad-hoc work-units have no workflow_instance |
| `workspace` | Workspace activates specialists; workflow definitions become available; workspace runs workflow_instances |
| `session` | Workflow_instance spans multiple sessions via persistent-state mechanism |
| `event` | Workflow_instance emits lifecycle events |
| `claim` | Claims emitted during workflow_instance attribute to it |
| `mechanism` | Authority binding + audit emission + persistent state compose |
| `category collapse` / `quality-gate` | Workflow execution telemetry feeds quality-gate drift detection |

## Validated under new disciplines (retrospective revisit)

After Phase 3.1 introduced G Composability Gate + D Defer Gate + multi-axis validation discipline, workflow lock revisited:

- **Multi-axis**: archetype × work-type × role variations all pass
- **G gate**: specialist's distributable bundle (containing workflow definitions) packageable for multi-mode consumption (consulting / firm-reuse / OSS / marketplace-future / backup-migration)
- **D gate**: all original deferrals validated as appropriate Phase 3.x schema territory; workflow_pattern was the suspect; resolved via mental modeling

**Lock holds under new disciplines.** 0 architectural REVISIONS surfaced in revisit.

## Defers (D-gate-validated)

| Defer | Awaited signal | Mechanism |
|---|---|---|
| `workflow_instance` entity-md schema specifics (fields, transitions, state machine) | Phase 3.5 work | ARCH workflow-mechanics topic; not architectural-decision defer |
| Authority-binding per workflow phase (which phases require authority; declaration mechanism) | Phase 3.5 + 3.3 authority-binding mechanism | Schema-detail; mental modeling resolves WHAT primitive does |
| Multi-practitioner workflow_instance ownership specifics | Phase 3.5 multi-practitioner-mechanics | Mental model resolves; schema detail in 3.5 |
| Failure-mode state machine specifics | Phase 3.5 schema topic | Mental model identifies states; transitions in schema |
| Cross-specialist shared workflow patterns lifted to framework primitive | Watch-list — if Layer A growth proves insufficient | Mental modeling resolves to Layer A by default; promotion examined IF triggered |

## Constraints flowing

This decision flows constraints into:
- Phase 3.5 workflow-mechanics ARCH topic (state machine, schema, multi-session continuity, multi-practitioner attribution)
- Phase 3.6 quality-gate ARCH topic (workflow telemetry as observability source)
- Phase 3.3 authority-binding mechanism detail (per-workflow-phase authority declaration)
- Phase 6 workspace serialization spec (workflow_instance entities included in workspace export)
- BACKLOG entries: workflow representation schema (3.5); workflow_pattern Layer A growth watch-list

## Files touched

- `GLOSSARY.md` workflow entry (re-classified; vocabulary disambiguated; lifecycle distinguished; composes-with expanded)
- `GLOSSARY.md` cascade entries (specialist, workspace, session, claim, event, intertwining, work-unit)
- `BACKLOG.md` Phase 3.1 (workflow bipartite-classification → Resolved; work-unit bipartite-classification → NEXT)
- `HANDOFF.md` notes 28+ (Phase 3 launch + workflow lock continuation)
- `ARCHITECTURE.md` (Locked architectural decisions section)

## Revisit triggers

This DR should be revisited if:
- Layer A reusable workflow templates prove insufficient for cross-archetype patterns (workflow_pattern primitive examined then)
- Second-shape productization (autonomous-business / personal-OS) reveals workflow primitive needs shape-policy variation
- Phase 3.5 workflow-mechanics ARCH topic surfaces operational concerns not anticipated at decision time
- Pioneer-deployment evidence shows ad-hoc-vs-codified ratio is different than mental-modeled

## Sharpening rounds metadata

- **Round 1**: AI full monty — 4 adoption options + 9 stress tests + position committed (B3 with optional applicability)
- **Round 2**: USER-TRIGGERED — 9 EXPANSIONS + 1 REVISION (R1 workflow_pattern resolution; user push surfaced ad-hoc scope refinement)
- **Retrospective revisit**: under new G + multi-axis + D gate disciplines — lock holds; 0 architectural REVISIONS

Total: 2 rounds + retrospective validation. Per `feedback_pre_decision_sharpening.md` 2-round sweet spot empirical pattern.
