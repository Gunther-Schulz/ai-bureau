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

Anything that has empirically failed as prose discipline becomes structurally enforced — hooks, pre-tool gates, regex checks, OR other strong-form enforcement patterns when hook-style enforcement is infeasible (see "Strong-form enforcement patterns" below). Treat advisory rules as best-effort hints; treat structural enforcement as guarantees.

**Failure mode addressed**: Prose discipline silently fails under context pressure. The AI follows it sometimes, drops it under load. Structural enforcement guarantees the action happens — or at minimum, makes its absence observable.

**Basis**: Anthropic engineering guidance: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." Well-evidenced for hook-style enforcement. The strong-form patterns below are derived from review of clippy plugin (single-sample); cross-framework validation pending.

### Strong-form enforcement patterns (when hooks are infeasible)

Some failure modes cannot be intercepted by PreToolUse hooks — most notably, assertions in natural-language output (see invariant 8 "Structural-enforcement gap"). For these, structural enforcement comes from procedural patterns observable in artifacts and tool-call sequences. Six patterns observed in clippy plugin's investigate-design + verify skills:

1. **Multi-level status indicators**: replace binary claim/no-claim with gradient levels (e.g., `[NOT VERIFIED]` / `[PARTIALLY VERIFIED]` / `[VERIFIED]` / `[VIOLATION]`). Forces gradient grading; "I'm not yet sure" is a first-class status. Single-component evidence is structurally distinguishable from cross-component evidence.

2. **Default-state = NOT READY with cycle counting**: framing default state as "incomplete, correct" prevents rush-to-completion as a structural matter. Single-pass assertions of "done" are structurally framed as wrong. Expected cycle count (e.g., 2-5+ before READY) makes single-cycle declarations of completion observable as anti-pattern.

3. **Discovery vs. verification distinction**: define what counts as evidence per artifact type. For code: grep finds locations; `read_file` is evidence; need 2-3+ distinct components for systemic patterns. For documents: grep finds sections; reading the section is evidence. The distinction is domain-specific but the pattern is universal — "I searched" ≠ "I read."

4. **Run-the-tool-show-the-output mandate**: for claims about verification state (tests pass, build succeeds, schema validates), require invocation of the verification tool AND showing its output. Output is the evidence; absence of output = unverified. Domain-specific verification tools (linters, type-checkers, test runners, validation scripts) become observable evidence sources.

5. **Structured disk artifacts as basis records**: tracker files (e.g., `.ai/investigation/tracker.yaml`) hold verification state per finding. Status is structurally observable; readers can inspect the artifact to see what's at what level. Forces accumulation of evidence over time and makes basis grading auditable post-hoc.

6. **Explicit anti-pattern enumeration**: per-discipline "DO NOT" lists naming common failure modes by name. Examples: "Mark [RESOLVED] after only reading structure/pattern"; "Assume pattern understanding = verification"; "Defer X when investigation can resolve it." Naming failure modes is a stronger guard than naming only success criteria.

These patterns compose. A discipline using all six is structurally stronger than one relying on prose alone, even without PreToolUse hooks. They are particularly relevant for invariant 8 (basis explicit) and invariant 9 (self-audit before done) where the failure mode happens in natural-language output and hooks cannot intercept.

**Application during derivation**: when running `derivation-procedure.md` Step 3 (derive hooks) and Step 4 (derive named skills), consider these strong-form patterns as alternatives to hooks for failure modes where natural-language output is the failure surface. Per-project procedures may adopt some, all, or none depending on cost-of-error calibration.

**Basis (this sub-section)**: Single-sample — derived from review of clippy plugin (`investigate-design/SKILL.md`, `verify/SKILL.md`, `references/VERIFICATION_EXAMPLES.md`). Other agent-style frameworks may surface additional or different patterns. Tagged judgment-call per `meta-rules.md` evidence-tier scale until cross-framework validation accumulates. First adopters' experience refines this pattern set.

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

**Procedural rule (the cite-or-flag-or-read decision)**: Before asserting any claim about code behavior, system state, or what a document says, take ONE of three paths:

- (a) **Cite** — the source has been read in current session; cite specific file:line or section name
- (b) **Read** — read the source now, then assert
- (c) **Flag** — explicitly tag the assertion as "inferred from adjacent signal X — not verified by reading source"

Defaulting to confident assertion without one of these three IS the failure mode. Particularly load-bearing for claims that adjacent signals (commit messages, file names, function names, doc titles, recall of prior conversations, framework-pattern-matching) make plausible — these are precisely the cases where inference most often produces wrong-but-confident results.

**Failure mode addressed**: Assertions defaulting to fabricated confidence. The honest basis is often weaker than the assertion implies; without explicit basis, the AI presents synthesis as observation. Particularly common when adjacent signals exist (commit messages, function names, doc titles) that make a plausible-sounding inference available without verification — the inference feels like knowledge to the AI, but the basis is pattern-match, not evidence.

**Basis**: Cross-validated; standard practice in well-cited human research; particularly load-bearing for AI given known confabulation tendency. Procedural rule strengthening (cite-or-flag-or-read) responds to assertion-without-basis as a recurring failure mode observed across multiple agent-style AI projects — the descriptive form ("make basis explicit") is necessary but not action-prescribing; AI under context pressure defaults to confident assertion unless given an explicit decision tree.

**Structural-enforcement gap**: Unlike invariants enforceable via PreToolUse hooks (e.g., prep-reads before writing to architectural artifacts — see invariant 5), this invariant cannot be deterministically enforced — assertions happen in natural-language output, not in tool calls. See `meta-rules.md` "Honest residual concerns" for the residual.

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
