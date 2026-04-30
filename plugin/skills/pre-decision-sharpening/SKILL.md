---
name: pre-decision-sharpening
description: Use when an architectural decision needs disciplined sharpening before commit to file (decision record, ARCHITECTURE.md, VISION.md, ROADMAP.md, or other load-bearing artifact). Triggers via "do another round" / "sharpen again" / "review/refine" / "challenge this" / "what did we miss" prompts after AI proposes architectural decision. Two-phase pattern (decision-design + pre-implementation) with 2-3 round sweet spot per phase per decomposed sub-decision. NOT for trivial decisions or pure-implementation work.
when_to_use: After AI proposes architectural decision (decision-record-grade); user wants disciplined sharpening pass before commit. Empirically validated to outperform post-mortem audits/reviews because pre-decision is sparring-mode (VISION axis 2) while audits are validator-mode anchored to existing content.
department: office
version: 0.1.0
---

# Pre-decision sharpening

Disciplined sharpening protocol applied at decision-formation moment. Operates UPSTREAM of `audit` + `design-review` skills (which serve drift-detection role post-decision). Empirically validated session 12 (#21 SDK deep-read R3a-R3d) — yields more genuine architectural refinements than post-mortem audits/reviews.

## Why pre-decision sharpening > post-mortem audit/review

Five mechanisms documented in `memory/feedback_pre_decision_sharpening.md`:

1. **Anchoring bias**: post-mortem looks at WHAT IS; pre-decision can explore WHAT COULD BE
2. **Sunk-cost protection**: post-decision reviewers protect existing investment; pre-decision has no sunk cost
3. **Sparring vs validation mode**: sharpening = SPARRING (challenge); audits = VALIDATION (confirm). Per VISION axis 2 + Vivienne Ming research: sparring outperforms validation
4. **Fresh-context advantage**: sharpening = design context is hot; audits = context is cold
5. **Greenfield-still-anchored problem**: even greenfield checks LOOK AT existing shape; reviewers can't easily generate alternatives outside what's surfaced. Pre-decision sharpening asks designer to GENERATE alternatives directly

## Two-phase pattern

### Phase 1: Decision-design phase (2-3 rounds total — sweet spot)

**When**: AI proposes architectural decision; before commit to file.

**Procedure**:

1. **Round 1: AI full monty (initial proactive proposal)**
   - Comprehensive proposal with stress-tests, refinements, edge cases, framing sharpening, counter-arguments engaged
   - Per `feedback_full_monty_upfront.md` — do FULL refinement upfront in initial proposal; don't fragment
   - Cover: architectural decision + main refinements + counter-arguments

2. **WAIT for user signal** to run further rounds
   - Do NOT auto-run round 2
   - User triggers via: explicit "do another round" / "sharpen again" / "review/refine" / "challenge this" prompt; OR via direct challenge questions warranting deeper look

3. **Round 2: First sharpening (USER-TRIGGERED)**
   - Stress-test what round 1 missed:
     - Schema fields incomplete?
     - Lifecycle distinctions missing?
     - Composition gaps with other decisions?
     - Governance integration?
     - Observability hooks?
     - New architectural patterns surfacing?
     - Cross-cutting concerns (boot/shutdown, errors, transport, tier-awareness)?
   - Surface 4-10 genuine refinements per round (empirical observation)
   - Distinguish EXPANSIONS (~80-90%) from REVISIONS (~10-20%)

4. **Round 3 (OPTIONAL, complexity-dependent): Second sharpening (USER-TRIGGERED)**
   - Run when broader architectural surface warrants (large unified abstraction; cross-decision synthesis)
   - Surfaces additional architectural patterns OR coverage of layers AI didn't think to address
   - Empirical: R3a/R3b/R3c locked at 2 rounds; R3d at 3 rounds (broader surface — subagent + per-substrate extension Protocols pattern); Substrate Protocol synthesis at 3 rounds

5. **After 2-3 rounds → architecturally LOCKED → persist DR**
   - Decision-design phase COMPLETE
   - Do NOT continue into operational/runtime details at this phase; defer to pre-implementation phase

### Phase 2: Pre-implementation phase (additional rounds at implementation-start; 2-3 sweet spot — preliminary observation)

**When**: At implementation-start moment for major commitment (e.g., #9 entity gate begins; #11 Cowork integration begins). User-triggered.

**Procedure**:

1. **At implementation-start moment**: run user-triggered pre-implementation sharpening rounds AGAINST locked DRs
2. **Round-N at pre-implementation = "what implementation details haven't we surfaced?"**:
   - Operational events (lifecycle, monitoring)
   - Rate limiting + budgets
   - Session continuation semantics
   - Timeouts (wall-clock vs idle vs max-turns)
   - Cancellation support
   - Multi-tenant isolation (if Tier 2+)
   - Health checks + observability
   - Error boundaries + failure signaling
   - Deployment-specific concerns
3. **Output**: implementation-readiness checklist + DR amendments for ~10-20% architectural flow-back
4. **Continue rounds until implementation-readiness sufficient** (typically 2-3 rounds — preliminary observation; refine empirically per phase)

## CRITICAL: Decomposition trigger

**If a decision genuinely needs >3 rounds at decision-design phase → DECOMPOSE**.

>3 rounds signals decomposition is missing. Decompose decision into sub-decisions; each sub-decision gets standard 2-3 rounds.

**Empirical validation**: #21 SDK deep-read decomposed into R3a/R3b/R3c/R3d/Synthesis. Each sub-decision fit 2-3 rounds. Total sharpening across all sub-decisions was 12+ rounds, but each sub-decision was tractable.

**Decomposition criteria**:
- Decision spans multiple architectural surfaces (substrate + transport + observability + permissions = decompose)
- Decision has independent sub-concerns that can be separately locked
- Decision feels too large to hold in mind during single round

After decomposition: each sub-decision gets full 2-3 round treatment + final synthesis pass.

## Pattern hypothesis: rounds correspond to LAYERS of architectural concern

Each round covers a different layer; rounds aren't iterative refinement of same layer:

| Round | Phase | Layer of concern |
|---|---|---|
| **Round 1** | Decision-design | Architectural decisions (what methods + types + abstractions) |
| **Round 2** | Decision-design | Cross-cutting + schema details (boot, errors, transport, tier, audit integration) |
| **Round 3** | Decision-design (optional) | Occasionally surfaces new architectural patterns (per-substrate extensions; common surface boundary criteria) — complexity-dependent |
| **Round 4+** | Pre-implementation | Operational + runtime concerns (lifecycle events, rate limit, sessions, timeouts, cancellation, multi-tenant, observability, deployment) |

Each phase serves different purpose; rounds within phase add coverage layer by layer.

## EXPANSION vs REVISION — calibrate expectations

Most refinements (~80-90%) are coverage EXPANSIONS (adding concerns layer by layer). Genuine architectural REVISIONS (~10-20%) change existing decisions.

**EXPANSION examples** (~80-90% of refinements):
- New schema fields (S1-S4 from R3b round 2)
- Per-kind context schemas (T1 from R3c round 2)
- Hook events (R1, R5 from Substrate Protocol round 3)
- Operational primitives (rate limit, timeouts, cancellation)

**REVISION examples** (~10-20% of refinements — high signal):
- T2 (PermissionRequest as entity at Tier 2+) — changed from "events only" to "entity at Tier 2+"
- Q3 (HTTP transport added to TransportMode) — extended R3a decision
- Q5 (audit-trail integration circularity resolution) — clarified architectural concern
- M5 (governance for MCP server registration) — extended R3c GOVERNANCE_WRITE

Watch for revisions; treat as DR amendments (potentially flow back to upstream decisions). Most rounds yield expansions — still valuable; just calibrate expectations.

## User-triggered rounds outperform AI-self-triggered rounds

Empirically validated session 12 R3d: AI-self round 2 felt comprehensive; USER-triggered round 3 surfaced 5 substantive + 4 smaller refinements including NEW architectural pattern (per-substrate extension Protocols) + 2 R3c amendments.

**Why user-trigger > AI-self-trigger**:
1. Self-validation bias: AI-self-driven sharpening operates within AI's existing frame; tendency to confirm own thinking
2. External-perspective effect: user-trigger introduces friction — AI is forced to reconsider rather than affirm. Trigger itself functions as sparring pushback
3. Scale-of-effort matching: AI-self-driven rounds tend toward Pareto-comfort; user-trigger forces past comfort threshold
4. Per VISION axis 2: user pushing back IS sparring; AI self-review is validator-mode by tendency

**Discipline**: AI does NOT auto-run round 2+. User signals "go deeper"; AI complies with disciplined sharpening pass.

## Composition with other PBS skills

| Skill | Composition |
|---|---|
| `audit` | Drift-detection POST-decision; pre-decision-sharpening operates UPSTREAM at decision-formation moment |
| `design-review` | Soundness-review POST-decision; same — pre-decision-sharpening upstream |
| `orchestrator` | Could route to pre-decision-sharpening when architectural-decision moment surfaces in workflow |
| `frame-task` (#8) | Frames task BEFORE work begins; pre-decision-sharpening operates AFTER first proposal exists, BEFORE commit |

Pre-decision-sharpening doesn't replace audit/design-review; OPERATES UPSTREAM preventing decisions from needing audit-driven correction.

## Output

When invoked, this skill orchestrates the round-by-round sharpening pattern. Per round:

- Surface refinements (expansions + occasional revisions) as structured chat content
- Wait for user accept/reject/refine
- After accepted refinements: incorporate into proposal
- After 2-3 rounds (decision-design phase) or implementation-readiness sufficient (pre-implementation phase): persist DR per `feedback_propose_before_commit.md`

## Audit-trail integration

Each sharpening round emits AuditEvent (when audit-trail v2 ships per #6):
- `event_kind="sharpening_round_started"` with round_number + decision_kind + phase
- `event_kind="sharpening_round_completed"` with refinements_surfaced count + expansion_count + revision_count
- Composes with audit-trail-as-canonical-source discipline + defensibility

## Source memory

`memory/feedback_pre_decision_sharpening.md` — full theoretical grounding + 5 mechanisms + pattern hypothesis + empirical validation from session 12 R3a-R3d work.

## Future elevation

Per ROADMAP commitment #23: this skill scoped for elevation to global plugin (Anthropic plugin marketplace OR PBS-as-framework distribution). When elevated:
- Generalizes beyond PBS to any architectural-discipline workflow
- Composes with consulting-deployment workflows
- Marketplace-asset shape (per ROADMAP v3 marketplace framing)

Until elevation: this skill is local to PBS plugin; uses PBS-specific terminology + cross-references; refines as additional empirical data accumulates.
