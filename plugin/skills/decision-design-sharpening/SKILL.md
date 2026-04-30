---
name: decision-design-sharpening
description: Use when an architectural decision needs disciplined sharpening BEFORE commit to file (decision record, ARCHITECTURE.md, VISION.md, ROADMAP.md, or other load-bearing artifact). Triggers via natural-language prompts including "solidify this decision" / "lock down this decision" / "make this solid" / "challenge/surface/refine to solidify" (or original "challenge/review/refine to solidify") / "challenge this" / "review/refine" / "do another round" / "sharpen again" / "what did we miss" / "what are we surfacing" / "verify completeness before commit" — all after AI proposes architectural decision. Phase 1 of two-phase pattern (Phase 2 = pre-implementation-sharpening). AKA the challenge → surface → refine → solidify cycle — this skill IS that operation, formalized as 2-3 disciplined rounds. Empirically validated to outperform post-mortem audits/reviews because pre-decision is sparring-mode (VISION axis 2) while audits are validator-mode anchored to existing content. NOT for trivial decisions, pure-implementation work, or implementation-start moments (use pre-implementation-sharpening instead).
when_to_use: After AI proposes architectural decision (decision-record-grade); user wants to solidify / lock down / challenge-surface-refine before commit. Fires AT DECISION-FORMATION MOMENT. Natural triggers: "solidify" / "lock down" / "challenge" / "surface" / "review/refine" / "another round" / "sharpen" / "what did we miss". Do NOT use for implementation-start sharpening — that's pre-implementation-sharpening.
department: office
version: 0.1.0
---

# Decision-design sharpening (Phase 1)

**The cycle**: **challenge → surface → refine → solidify** (refined from original "challenge/review/refine to solidify"; "review" sharpened to "surface" to capture what each round ACTUALLY does — bringing up what's NOT visible, not just checking what's there). "Sharpening" is the collapsed shorthand for this 4-operation cycle. Original "review" terminology still routes here.

### The cycle — per-term definitions (VISION-axis-aligned)

| Term | Operation | VISION mapping |
|---|---|---|
| **Challenge** | Stress-test proposal: counter-arguments, weaknesses, edge cases, "what's the strongest argument against?" | Axis 2 (sparring partner mode — Vivienne Ming's productive mode) |
| **Surface** | Bring up what's NOT visible: schema gaps, lifecycle distinctions, composition concerns, governance integration, observability hooks, missing architectural patterns, layered coverage check | Axis 1 (intertwining — continuous coverage across architectural layers) |
| **Refine** | Improve specifics: tighten language, add missing fields, sharpen definitions; validate against existing decisions/VISION/ARCH disciplines | Improvement + implicit validation |
| **Solidify** | Lock for commit: persist as DR, anchor for future reference, ensure 6-months-later-defensible | Axis 3 (authorship preservation — output user can defend) |

Disciplined sharpening protocol applied at decision-formation moment, BEFORE commit to file. Operates UPSTREAM of `audit` + `design-review` skills (which serve drift-detection role post-decision).

For Phase 2 (pre-implementation), see `pre-implementation-sharpening` skill.

For shared theoretical grounding (5 mechanisms / decomposition trigger / expansion-vs-revision / layered coverage hypothesis), see `memory/feedback_pre_decision_sharpening.md`.

## When this skill fires

- AI proposes architectural decision (decision-record-grade)
- User signals "do another round" / "sharpen again" / "review/refine" / "challenge this" / "what did we miss"
- BEFORE commit to file (DR, ARCH, VISION, ROADMAP)

NOT for:
- Trivial decisions or pure-implementation work
- Implementation-start moments (use `pre-implementation-sharpening` instead)
- Post-decision drift detection (use `audit` skill instead)
- Post-decision soundness review (use `design-review` skill instead)

## Phase 1 procedure (2-3 rounds total — sweet spot)

### Round 1: AI full monty (initial proactive proposal)

When AI proposes the architectural decision:
- Comprehensive proposal with stress-tests, refinements, edge cases, framing sharpening, counter-arguments engaged
- Per `memory/feedback_full_monty_upfront.md` — do FULL refinement upfront in initial proposal; don't fragment
- Cover: architectural decision + main refinements + counter-arguments

### WAIT for user signal to run further rounds

Do NOT auto-run round 2. User triggers via:
- Explicit prompts: "do another round" / "sharpen again" / "review/refine" / "challenge this"
- Direct challenge questions warranting deeper look
- "What did we miss?" / "What about X?"

Per `memory/feedback_pre_decision_sharpening.md` user-trigger discipline: USER-TRIGGERED rounds outperform AI-self-triggered rounds because external-perspective friction forces AI past comfort threshold.

### Round 2: First sharpening (USER-TRIGGERED)

Stress-test what round 1 missed:
- **Schema fields incomplete?** Missing required fields, optional fields, validation rules?
- **Lifecycle distinctions missing?** State machines, entity lifecycle, request lifecycle?
- **Composition gaps with other decisions?** How does this interact with existing decisions?
- **Governance integration?** Permission flow? Audit-trail emission?
- **Observability hooks?** Telemetry, logging, monitoring?
- **New architectural patterns surfacing?** Patterns the round 1 didn't name explicitly?
- **Cross-cutting concerns?** Boot/shutdown, errors, transport, tier-awareness, audit integration

Surface 4-10 genuine refinements per round (empirical observation). Distinguish EXPANSIONS (~80-90%) from REVISIONS (~10-20%).

### Round 3 (OPTIONAL, complexity-dependent): Second sharpening (USER-TRIGGERED)

Run when broader architectural surface warrants:
- Large unified abstraction (e.g., Substrate Protocol synthesis)
- Cross-decision synthesis (multiple sub-decisions composing)
- Genuinely complex architectural surface

Surfaces additional architectural patterns OR coverage of layers AI didn't think to address.

**Empirical guidance**:
- R3a/R3b/R3c locked at 2 rounds (round 1 + 1 user-triggered sharpening)
- R3d at 3 rounds (broader architectural surface — subagent + per-substrate extension Protocols pattern)
- Substrate Protocol synthesis at 3 rounds (broadest surface — 4-decision synthesis)

### After 2-3 rounds → architecturally LOCKED → persist DR

Decision-design phase COMPLETE. Per `memory/feedback_propose_before_commit.md`, propose final structure in chat before committing to file. Then commit + push.

**Do NOT continue into operational/runtime details at this phase** — defer to pre-implementation phase (`pre-implementation-sharpening` skill).

## CRITICAL: Decomposition trigger

**If a decision genuinely needs >3 rounds at decision-design phase → DECOMPOSE**.

>3 rounds signals decomposition is missing. Decompose decision into sub-decisions; each sub-decision gets standard 2-3 rounds.

**Decomposition criteria**:
- Decision spans multiple architectural surfaces (substrate + transport + observability + permissions = decompose)
- Decision has independent sub-concerns that can be separately locked
- Decision feels too large to hold in mind during single round

**Empirical validation**: #21 SDK deep-read decomposed into R3a/R3b/R3c/R3d/Synthesis. Each sub-decision fit 2-3 rounds. Total sharpening across all sub-decisions was 12+ rounds, but each sub-decision was tractable.

After decomposition: each sub-decision gets full 2-3 round treatment + final synthesis pass.

## Layered coverage observation (Phase 1 specific)

Each round at decision-design phase covers a different architectural concern layer:

| Round | Layer of concern |
|---|---|
| **Round 1** | Architectural decisions (what methods + types + abstractions) |
| **Round 2** | Cross-cutting + schema details (boot, errors, transport, tier, audit integration) |
| **Round 3 (optional)** | Occasionally surfaces new architectural patterns (per-substrate extensions; common surface boundary criteria) — complexity-dependent |
| **Round 4+ (DEFER to Phase 2)** | Operational + runtime + deployment concerns belong in `pre-implementation-sharpening` |

If round content shifts to operational/runtime concerns at decision-design phase, that's a signal to STOP this skill and DEFER content to pre-implementation phase.

## EXPANSION vs REVISION calibration

Most refinements (~80-90%) are coverage EXPANSIONS (adding concerns layer by layer). Genuine architectural REVISIONS (~10-20%) change existing decisions.

**EXPANSION examples** (most refinements):
- New schema fields (S1-S4 from R3b round 2)
- Per-kind context schemas (T1 from R3c round 2)
- Hook events (R1, R5 from Substrate Protocol round 3)
- Operational primitives (rate limit, timeouts, cancellation)

**REVISION examples** (high signal):
- T2 (PermissionRequest as entity at Tier 2+) — changed from "events only" to "entity at Tier 2+"
- Q3 (HTTP transport added to TransportMode) — extended R3a decision
- Q5 (audit-trail integration circularity resolution) — clarified architectural concern
- M5 (governance for MCP server registration) — extended R3c GOVERNANCE_WRITE

Watch for REVISIONS; treat as DR amendments (potentially flow back to upstream decisions). Most rounds yield expansions — still valuable; just calibrate expectations.

## Composition with other PBS skills

| Skill | Composition |
|---|---|
| `pre-implementation-sharpening` | Phase 2 of same pattern; fires at implementation-start moment, NOT at decision-formation moment |
| `audit` | Drift-detection POST-decision; this skill operates UPSTREAM at decision-formation moment |
| `design-review` | Soundness-review POST-decision; same — this skill upstream |
| `orchestrator` | Could route to this skill when architectural-decision moment surfaces in workflow |
| `frame-task` (#8) | Frames task BEFORE work begins; this skill operates AFTER first proposal exists, BEFORE commit |

## Output

Per round:
- Surface refinements (expansions + occasional revisions) as structured chat content
- Wait for user accept/reject/refine
- After accepted refinements: incorporate into proposal
- After 2-3 rounds: persist DR per `memory/feedback_propose_before_commit.md`

## Audit-trail integration

When audit-trail v2 ships per #6, each sharpening round emits:
- `event_kind=sharpening_round_started` with `round_number` + `decision_kind` + `phase=decision_design`
- `event_kind=sharpening_round_completed` with `refinements_surfaced` count + `expansion_count` + `revision_count`

Composes with audit-trail-as-canonical-source discipline + defensibility per VISION axis 3.

## Source memory + shared methodology

`memory/feedback_pre_decision_sharpening.md` — full theoretical grounding:
- 5 mechanisms (anchoring bias / sunk-cost / sparring vs validation / fresh-context / greenfield-still-anchored)
- Decomposition trigger details
- User-triggered round discipline
- Layered coverage hypothesis
- Expansion-vs-revision calibration
- Empirical validation from session 12 R3a-R3d work

Shared between this skill + `pre-implementation-sharpening`.
