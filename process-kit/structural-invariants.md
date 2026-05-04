# Structural invariants — kept verbatim across derivations

These are the cross-domain claims about what makes AI-partnered work robust. They are applied as-is to every project running the derivation procedure. They are NOT customized per project — what gets customized is the implementation details (which artifacts trigger which hooks, what counts as a high-stakes cascade, what numeric thresholds to use, etc.). Implementation details belong in `derivation-procedure.md`.

Each invariant: the rule, the failure mode it addresses, the basis for the claim.

## 1. Load mandatory context at every fresh start

A small, anchor-grade entry document names the must-reads and the bootstrap order for any session beginning substantive work. The entry document auto-loads (or is the first thing read) so even fresh sessions with no prior context arrive at the project's specialized procedures.

**Failure mode addressed**: Fresh-session amnesia. Without an explicit anchor, every session reverts to ad-hoc behavior, missing the project's specialized procedures.

**Basis**: Anthropic guidance on auto-loading anchor documents; cross-validated by direct observation of fresh-session drift.

## 2. Bound and refresh context aggressively

Split large anchor documents into per-topic files loaded on demand. Recommend explicit context resets at natural work-unit boundaries. Externalize state at those boundaries (handoff log, commits, task list) so context loss costs nothing.

**Failure mode addressed**: Long-session context-rot — instruction-adherence degrades as context grows; accumulated corrections drift from current intent.

**Basis**: Chroma context-rot research; Anthropic engineering guidance on bloated entry docs causing instruction-following collapse; cross-validated by direct observation.

## 3. Route multi-file or high-stakes work through fresh sub-contexts

The main session orchestrates; sub-agents in clean contexts execute. Each sub-agent is briefed with focused scope, not the full corpus.

**Failure mode addressed**: Cascade-mode load — when working on multiple coupled files, the AI drops disciplines that were active at session start. Sub-agents preserve focus by isolating exploration and implementation in clean contexts.

**Basis**: Anthropic engineering guidance: "subagents are one of the most powerful tools available... preserve context by keeping exploration and implementation out of your main conversation." Cross-validated by direct observation.

## 4. Separate the doer from the judge

Writer-Reviewer (or Investigator-Implementer) in different contexts. The agent producing work should not be the same agent evaluating it.

**Failure mode addressed**: Self-validation bias / self-praise bias. An agent reviewing its own work tends to confirm rather than challenge.

**Basis**: Anthropic engineering guidance: "Separating the agent doing the work from the agent judging it proves to be a strong lever." Well-evidenced.

## 5. Make load-bearing rules deterministic, not advisory

Anything that has empirically failed as prose discipline becomes a hook, pre-tool gate, or regex check. Treat advisory rules as best-effort hints; treat hooks as guarantees.

**Failure mode addressed**: Prose discipline silently fails under context pressure. The AI follows it sometimes, drops it under load. Structural enforcement guarantees the action happens.

**Basis**: Anthropic engineering guidance: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." Well-evidenced.

## 6. Force re-grounding at every invocation of a procedure

When invoking a named procedure or skill, read its source document fresh; cite a section name; quote source-of-truth file:line when asserting. Do not pattern-match from synthesized memory of prior invocations.

**Failure mode addressed**: Pattern-matching from synthesized memory of prior usage silently drops load-bearing steps. Memory of "I've done this before" is not direct evidence and produces directionally-correct-but-load-bearing-incomplete results.

**Basis**: Cross-validated by direct observation of repeated drift incidents; consistent with honesty-about-sources discipline (see invariant 8).

## 7. Distinguish memory-as-preference from memory-as-truth

Behavioral preferences ("user wants terse summaries") persist freely. Factual claims about state ("function X exists at path Y") must be verified against current files before acting on them.

**Failure mode addressed**: Stale memory leading to confidently wrong claims about current state. Memory ages; reality moves; conflating the two produces overconfident errors.

**Basis**: Direct observation; consistent with how durable institutional memory works in human contexts (preferences endure, facts need refresh).

## 8. Make basis explicit in every assertion

Every claim has a citation — a named basis. Without one, the claim defaults to "known from direct evidence in current context." When the basis isn't direct evidence, name what it actually is (summary, synthesis, memory, pattern-match).

**Failure mode addressed**: Assertions defaulting to fabricated confidence. The honest basis is often weaker than the assertion implies; without explicit basis, the AI presents synthesis as observation.

**Basis**: Cross-validated; standard practice in well-cited human research; particularly load-bearing for AI given known confabulation tendency.

## 9. Self-audit before declaring done

Before claiming a task complete, run an explicit checklist: did I read every required source, apply every cited discipline, leave any thread open?

**Failure mode addressed**: Agentic laziness on long-running tasks — premature claim of completion, trailing threads dropped silently, partial work presented as complete.

**Basis**: Direct observation; consistent with Anthropic long-running-Claude research findings on completion-bias.

## 10. Defense in depth

No single mechanism is trusted to hold across all conditions. Layer redundantly; the catch is always the next layer down. Each layer should know which failure mode it addresses; layers that address no observed mode should be retired.

**Failure mode addressed**: Single-point-of-failure architectures fail silently when their one mechanism degrades. Redundant layering catches drift that any individual layer would miss.

**Basis**: Cross-domain — security engineering, aerospace, finance all rely on defense-in-depth for the same reason. Particularly applicable to AI where degradation is silent and gradual.

## Sizing principle (governs how to apply 1-10)

Mitigation density should scale with cost-of-error and irreversibility. The full stack is heavy; it is worth its cost only when errors cascade and are expensive to unwind. For low-stakes work, applying all ten invariants is over-engineered.

The right question per project, per artifact, per work-unit: **what's the blast radius of getting this wrong, and how reversible is it?**

Sizing is not an invariant; it is a calibration step performed during derivation (see `derivation-procedure.md` Step 8). Different artifact types within the same project may warrant different sizing.
