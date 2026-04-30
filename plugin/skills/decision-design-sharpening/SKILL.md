---
name: decision-design-sharpening
description: Use when an architectural decision needs disciplined sharpening BEFORE commit to file (decision record, architecture doc, vision/strategy doc, roadmap, or other load-bearing artifact). Triggers via natural-language prompts including "solidify this decision" / "lock down this decision" / "make this solid" / "challenge/surface/refine to solidify" (or original "challenge/review/refine to solidify") / "challenge this" / "review/refine" / "do another round" / "sharpen again" / "what did we miss" / "what are we surfacing" / "verify completeness before commit" — all after AI proposes architectural decision. Phase 1 of two-phase pattern (Phase 2 = pre-implementation-sharpening). AKA the challenge → surface → refine → solidify cycle — this skill IS that operation, formalized as 2-3 disciplined rounds. Empirically validated to outperform post-mortem audits/reviews because pre-decision is sparring-mode (per Vivienne Ming research on AI-human hybrid teams) while audits are validator-mode anchored to existing content. NOT for trivial decisions, pure-implementation work, or implementation-start moments (use pre-implementation-sharpening instead).
when_to_use: After AI proposes architectural decision (decision-record-grade); user wants to solidify / lock down / challenge-surface-refine before commit. Fires AT DECISION-FORMATION MOMENT. Natural triggers: "solidify" / "lock down" / "challenge" / "surface" / "review/refine" / "another round" / "sharpen" / "what did we miss". Do NOT use for implementation-start sharpening — that's pre-implementation-sharpening.
version: 0.2.0
---

# Decision-design sharpening (Phase 1)

Disciplined sharpening protocol applied at decision-formation moment, BEFORE commit to file. Operates UPSTREAM of drift-detection / soundness-review skills (which serve POST-decision purposes).

## The cycle: challenge → surface → refine → solidify

Refined from original "challenge/review/refine to solidify" framing; "review" sharpened to "surface" because the operation is bringing up what's NOT visible (not just checking what's there). "Sharpening" is the collapsed shorthand for this 4-operation cycle. Original "review" terminology still routes here.

### Per-term definitions

| Term | Operation | Mode |
|---|---|---|
| **Challenge** | Stress-test proposal: counter-arguments, weaknesses, edge cases, "what's the strongest argument against?" | Sparring mode (per Vivienne Ming research on AI-human hybrid teams — only sparring outperforms human-alone or AI-alone) |
| **Surface** | Bring up what's NOT visible: schema gaps, lifecycle distinctions, composition concerns, governance integration, observability hooks, missing architectural patterns, layered coverage check | Coverage mode |
| **Refine** | Improve specifics: tighten language, add missing fields, sharpen definitions; validate against existing decisions / vision / architectural disciplines | Improvement + implicit validation |
| **Solidify** | Lock for commit: persist as decision record, anchor for future reference, ensure later-defensibility (will reviewer be able to defend this 6 months from now?) | Decision/output |

## When this skill fires

- AI proposes architectural decision (decision-record-grade)
- User signals "do another round" / "sharpen again" / "review/refine" / "challenge this" / "what did we miss" / "solidify"
- BEFORE commit to file (decision record, ARCHITECTURE, VISION/strategy, ROADMAP, or other load-bearing artifact)

NOT for:
- Trivial decisions or pure-implementation work
- Implementation-start moments (use `pre-implementation-sharpening` instead)
- Post-decision drift detection (use drift-detection skills instead)
- Post-decision soundness review (use soundness-review skills instead)

## Why pre-decision sharpening > post-mortem audit/review

Five mechanisms:

1. **Anchoring bias**: post-mortem looks at WHAT IS; pre-decision can explore WHAT COULD BE
2. **Sunk-cost protection**: post-decision reviewers protect existing investment; pre-decision has no sunk cost
3. **Sparring vs validation mode**: sharpening = SPARRING (challenge); audits = VALIDATION (confirm). Per Ming research: sparring outperforms validation
4. **Fresh-context advantage**: sharpening = design context is hot; audits = context is cold
5. **Greenfield-still-anchored problem**: even greenfield checks ("would we build this from scratch?") LOOK AT existing shape; reviewers can't easily generate alternatives outside what's surfaced. Pre-decision sharpening asks designer to GENERATE alternatives directly

## Phase 1 procedure (2-3 rounds total — sweet spot)

### Round 1: AI full monty (initial proactive proposal)

When AI proposes the architectural decision:
- Comprehensive proposal with stress-tests, refinements, edge cases, framing sharpening, counter-arguments engaged
- Do FULL refinement upfront in initial proposal; don't fragment into multiple rounds with the user prompting each time
- Cover: architectural decision + main refinements + counter-arguments

### WAIT for user signal to run further rounds

Do NOT auto-run round 2. User triggers via:
- Explicit prompts: "do another round" / "sharpen again" / "review/refine" / "challenge this"
- Direct challenge questions warranting deeper look
- "What did we miss?" / "What about X?"

USER-TRIGGERED rounds outperform AI-self-triggered rounds because external-perspective friction forces AI past its self-validation comfort threshold.

### Round 2: First sharpening (USER-TRIGGERED)

Stress-test what round 1 missed:
- **Schema fields incomplete?** Missing required fields, optional fields, validation rules?
- **Lifecycle distinctions missing?** State machines, entity lifecycle, request lifecycle?
- **Composition gaps with other decisions?** How does this interact with existing decisions?
- **Governance integration?** Permission flow? Audit-trail emission?
- **Observability hooks?** Telemetry, logging, monitoring?
- **New architectural patterns surfacing?** Patterns the round 1 didn't name explicitly?
- **Cross-cutting concerns?** Boot/shutdown, errors, transport, deployment-tier-awareness, audit integration

Surface 4-10 genuine refinements per round (empirical observation). Distinguish EXPANSIONS (~80-90%) from REVISIONS (~10-20%).

### Round 3 (OPTIONAL, complexity-dependent): Second sharpening (USER-TRIGGERED)

Run when broader architectural surface warrants:
- Large unified abstraction
- Cross-decision synthesis (multiple sub-decisions composing)
- Genuinely complex architectural surface

Surfaces additional architectural patterns OR coverage of layers AI didn't think to address.

### After 2-3 rounds → architecturally LOCKED → persist decision record

Decision-design phase COMPLETE. Propose final structure in chat before committing to file. Then commit + reference for future.

**Do NOT continue into operational/runtime details at this phase** — defer to pre-implementation phase (`pre-implementation-sharpening` skill).

## CRITICAL: Decomposition trigger

**If a decision genuinely needs >3 rounds at decision-design phase → DECOMPOSE**.

>3 rounds signals decomposition is missing. Decompose decision into sub-decisions; each sub-decision gets standard 2-3 rounds.

**Decomposition criteria**:
- Decision spans multiple architectural surfaces (decompose into per-surface sub-decisions)
- Decision has independent sub-concerns that can be separately locked
- Decision feels too large to hold in mind during single round

After decomposition: each sub-decision gets full 2-3 round treatment + final synthesis pass.

## Layered coverage observation (Phase 1 specific)

Each round at decision-design phase covers a different architectural concern layer:

| Round | Layer of concern |
|---|---|
| **Round 1** | Architectural decisions (what methods + types + abstractions) |
| **Round 2** | Cross-cutting + schema details (boot, errors, transport, tier-awareness, audit integration) |
| **Round 3 (optional)** | Occasionally surfaces new architectural patterns — complexity-dependent |
| **Round 4+ (DEFER to Phase 2)** | Operational + runtime + deployment concerns belong in `pre-implementation-sharpening` |

If round content shifts to operational/runtime concerns at decision-design phase, that's a signal to STOP this skill and DEFER content to pre-implementation phase.

## EXPANSION vs REVISION calibration

Most refinements (~80-90%) are coverage EXPANSIONS (adding concerns layer by layer). Genuine architectural REVISIONS (~10-20%) change existing decisions.

**EXPANSION examples**:
- New schema fields
- Per-kind context schemas
- New hook events
- Operational primitives (rate limit, timeouts, cancellation)

**REVISION examples** (high signal):
- Changing entity-vs-event categorization for a concept
- Adding new transport mode to existing enum (extends earlier decision)
- Resolving architectural circularity
- Extending governance to cover newly-surfaced surface

Watch for REVISIONS; treat as decision-record amendments (potentially flow back to upstream decisions). Most rounds yield expansions — still valuable; just calibrate expectations.

## Composition with other skills

| Skill type | Composition |
|---|---|
| `pre-implementation-sharpening` | Phase 2 of same pattern; fires at implementation-start moment, NOT at decision-formation moment |
| Drift-detection skills (e.g., audit) | Operate POST-decision; this skill operates UPSTREAM at decision-formation moment |
| Soundness-review skills (e.g., design-review) | Operate POST-decision; same — this skill upstream |
| Orchestrator skills | Could route to this skill when architectural-decision moment surfaces in workflow |
| Framing/scoping skills | Frame task BEFORE work begins; this skill operates AFTER first proposal exists, BEFORE commit |

## Output

Per round:
- Surface refinements (expansions + occasional revisions) as structured chat content
- Wait for user accept/reject/refine
- After accepted refinements: incorporate into proposal
- After 2-3 rounds: persist decision record (propose final structure in chat first; commit after user approval)

## Audit-trail integration (optional; composable with audit-trail infrastructure if available)

If deployment has audit-trail infrastructure, each sharpening round can emit:
- `event_kind=sharpening_round_started` with `round_number` + `decision_kind` + `phase=decision_design`
- `event_kind=sharpening_round_completed` with `refinements_surfaced` count + `expansion_count` + `revision_count`

Composes with audit-trail-as-canonical-source pattern + later-defensibility.

---

## PBS-specific empirical validation (PBS deployment notes; remove/replace for other deployments)

**This section is PBS-deployment-specific and should be removed or replaced when this skill is elevated to a global plugin or adopted by another deployment.**

### Deployment metadata
- `department: office` (PBS-specific via #12 office-vs-department modularization)

### Empirical validation source
This skill emerged from PBS session 12 (2026-04-30) #21 SDK deep-read multi-round sharpening work. Pattern discovered + validated across:
- R3a (in-process MCP server adoption) — 2 rounds locked
- R3b (eval framework adoption) — 2 rounds locked (S1-S4 round-2 refinements)
- R3c (permission abstraction) — 2 rounds locked (T2 genuine architectural revision; T1-T8 round-2 refinements)
- R3d (subagent primitives adoption) — 3 rounds locked (P3 + P4 architectural patterns surfaced in round 3; broader surface justified extra round)
- Substrate Protocol design synthesis — 3 rounds locked (broadest architectural surface — 4-decision synthesis)

12+ rounds across 5 sub-decisions yielded 18+ substantive architectural refinements. Decomposition pattern confirmed: #21 SDK deep-read decomposed into R3a/R3b/R3c/R3d/Synthesis; each sub-decision fit 2-3 rounds.

### PBS VISION axis mappings
PBS-specific terminology citations for the cycle:
- **Challenge** → cited in PBS as VISION axis 2 (sparring partner mode; per `VISION.md` §200-235 / Vivienne Ming research)
- **Surface** → cited in PBS as VISION axis 1 (intertwining-AI-workflow; continuous coverage across architectural layers)
- **Refine** → improvement + validation against PBS architectural disciplines (per `ARCHITECTURE.md`)
- **Solidify** → cited in PBS as VISION axis 3 (authorship preservation; output user can defend 6 months later under challenge)

### PBS skill cross-references
This skill composes with PBS skills:
- `audit` (drift-detection POST-decision)
- `design-review` (soundness-review POST-decision)
- `frame-task` (framing BEFORE work — pre-RAG commitment #8)
- `orchestrator` (workflow routing)

### PBS source memory
- `memory/feedback_pre_decision_sharpening.md` — full theoretical grounding + empirical observations
- `memory/feedback_full_monty_upfront.md` — round-1 comprehensiveness discipline
- `memory/feedback_propose_before_commit.md` — chat-first-then-file discipline

### PBS commitment context
- ROADMAP commitment #23 — local skill scaffolded session 12; future global plugin elevation deferred to post-marketplace decision (per ROADMAP v3 marketplace framing)
- Audit-trail integration composes with PBS audit-trail v2 retrofit per ROADMAP #6
- Pre-implementation phase rounds expected at PBS commitments #9 (entity gate) / #11 (Cowork integration) / #13 (deployment flexibility) implementation starts
