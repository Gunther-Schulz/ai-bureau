# Meta-rules — calibrating trust in the kit itself

These rules govern how to read, apply, and update the kit. They are not invariants about AI-partnered work (those live in `structural-invariants.md`); they are rules about the kit itself — its provenance, its evidence, its honest scope.

## Sample-size tagging

Each claim in the kit should carry a sample-size note: from how many independent projects / domains has this been validated?

- **Cross-domain validated** — observed across multiple distinct projects in different domains. Sturdier
- **Single-domain validated** — observed in one project (potentially many sessions, but one domain). Calibrate for transferability
- **Externally cross-validated** — supported by published research or industry guidance independent of any one project

Most structural invariants in the current kit are externally cross-validated (Anthropic engineering guidance, Chroma context-rot research, AgentIF benchmark, plus direct observation in the originating project). The derivation procedure itself is currently single-domain.

## Evidence-tier tagging

Each claim should be marked by evidence tier:

- **Well-evidenced** — cited research plus observed incident data; multiple independent sources point the same way
- **Judgment-call** — plausible based on first principles but not strongly empirically validated
- **Speculative** — proposed but unverified; included as candidate, flagged explicitly

The kit prefers well-evidenced claims as load-bearing. Judgment-calls and speculative claims should be marked as such and not treated as load-bearing until evidence accumulates.

## Citation-date tagging

Any citation of external research carries the date it was last verified. Citations older than ~12-18 months are candidates for re-verification — research moves and positions evolve.

When the kit updates, citation-dates update too (per `self-application.md` Step 5).

## Basis tagging

For each claim, distinguish the basis:

- **Observed in our own work** — direct evidence from project sessions; the strongest evidence for that specific context, but transferability is a separate question
- **Read in published research** — strong for the published claim's scope; transferability depends on study design
- **Synthesized from multiple sources** — explicit synthesis; weaker than direct observation but useful when no single source covers the question
- **Pattern-matched from prior usage** — flagged as not-direct-evidence per `structural-invariants.md` invariant 8; acceptable as hypothesis, not as load-bearing claim

Basis affects how a claim can be falsified:

- Observed claims are falsified by new observations
- Read claims by re-reading the source (it may have been misread, or it may have been retracted or superseded)
- Synthesized claims by examining the synthesis logic
- Pattern-matched claims by re-grounding (which usually invalidates them)

## Honest residual concerns

The kit currently has the following acknowledged limitations:

- **The derivation procedure is single-sample-derived** — distilled from observation of one project (`pbs-bureau`, a framework-source repo for AI-partnered expert-craft cultivation). The first projects to adopt and run it may surface refinements to the procedure itself. The self-application protocol catches this when cross-project evidence accumulates
- **Sizing thresholds are not numeric in the kit** — specific numbers (≥N recurrences before codification, M-month refresh cadences, etc.) are project-calibrated, not kit-prescribed. This is intentional but means first-time adopters do real work calibrating from their own domain
- **The structural invariants are stated cleanly but their *interaction* is less well-evidenced** — defense-in-depth (invariant 10) assumes layers compose without conflict. Direct observation has confirmed this for many pairs of invariants but not exhaustively. It is possible that some invariants conflict in some domains; adopters should watch for this and report
- **The kit currently has no live falsifier** — the self-application protocol relies on adopters to detect triggers and run re-derivation. There is no central maintainer obligated to do this. Adopters wanting assurance should designate the role internally
- **Assertion-without-basis is named (invariant 8) but not hook-enforceable** — tool-call interception hooks (e.g., PreToolUse in Claude Code) can enforce prep-reads before specific tool actions, but cannot intercept natural-language assertions in output text. The cite-or-flag-or-read procedural rule (invariant 8) raises the bar but does not eliminate the failure under context pressure. Mitigation relies on: (1) the procedural rule firing reliably, (2) basis-honesty making after-the-fact catches cheap (AI confesses the actual basis without ego when probed), (3) user sparring as load-bearing falsifier — direct probes ("are you guessing?" / "did you read X?") are the most reliable fallback when the procedural rule misfires, (4) **strong-form enforcement patterns** per invariant 5 sub-section (multi-level status indicators / default-state-NOT-READY / discovery-vs-verification / run-the-tool-show-output / structured disk artifacts / anti-pattern enumeration) — these don't require hooks but are still structural; per-project derivations may adopt some or all. This is one of the hardest failure modes to address; the kit reduces frequency, does not eliminate. Domain-specific hooks may strengthen further (e.g., requiring recent Read of regulatory source before any tool action that emits a regulatory claim), but no such hook intercepts the prose-output channel itself

These limitations should be visible to adopters. The kit's value depends on adopters knowing what it does and does not yet have evidence for.

## Reading discipline (for kit users)

When applying the kit:

- Read each invariant freshly when invoking it; do not pattern-match from memory of "I read this before" (per invariant 6, applied recursively to the kit itself)
- Cite the specific section name when reasoning from the kit; "per `structural-invariants.md` invariant 4 (Separate the doer from the judge)" beats "per the kit"
- When the kit's claim conflicts with your direct observation in your project, trust your observation but record the conflict — it may be a per-domain calibration point, or it may be a kit defect surfacing through your project's data

## When meta-rules update

Meta-rules update when the kit updates (per `self-application.md`). They are not separately maintained — they are part of the kit's own provenance discipline.

If meta-rules themselves need restructuring (e.g., new evidence tiers prove necessary, sample-size taxonomy needs refinement), that is itself a kit update and goes through the self-application protocol.
