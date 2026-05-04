# Process kit — building robust AI-collaboration procedures

## What this is

An **instructional kit** for deriving project-specific procedures that make AI-partnered work robust against documented AI failure modes (context drift, pattern-matching from synthesized memory, self-validation bias, cascade-mode degradation, agentic laziness, sycophancy, prose-discipline silent failure, etc.).

This kit is **not a template** to copy. It is a **generator** — a procedure for producing your project's own procedure document. The kit stays at the meta level; the per-project artifacts implement.

## What it produces

For each project that runs the kit's derivation procedure, the output is:

- A per-project procedure document (anchor docs, hooks, named skills, sub-agent routing thresholds, work-unit boundaries, sizing calibration)
- A goal-doc — what the procedure must keep serving — that lives inside the project
- A maintenance protocol scoped to that project (failure log, refresh cadence, retirement criteria, adoption criteria)

## Who it's for

Projects where:

- AI is doing high-stakes coupled work (decisions cascade across files; errors are expensive to unwind)
- Naive prompting and ad-hoc instructions fail repeatedly in observable ways
- The cost of building a structured procedure is justified by the cost of errors

For one-shot scripts, throwaway prototypes, or low-coupling work, this kit is over-engineered. Mitigation density should match cost-of-error. See `structural-invariants.md` "Sizing principle".

## Files in this folder

- `README.md` (this file) — what the kit is, who it's for, how to use it
- `structural-invariants.md` — cross-domain rules kept verbatim across all derivations
- `derivation-procedure.md` — step-by-step procedure for producing a per-project procedure
- `self-application.md` — when and how the kit updates itself
- `meta-rules.md` — basis tagging, evidence tiers, honest caveats

## How to use

1. Read `structural-invariants.md` first — these are the universal claims you'll apply verbatim
2. Run `derivation-procedure.md` against your project — produces your per-project procedure document
3. Maintain that derived procedure per its own internal maintenance section (Step 10 of the derivation procedure)
4. Periodically (or on triggers) consult `self-application.md` — when fundamental new information arrives, the kit itself can be refreshed by applying its own derivation procedure to itself

## Provenance and basis

This kit was distilled from observation of one project (`pbs-bureau`, a framework-source repo for AI-partnered expert-craft cultivation) over multiple development sessions. Many of the structural invariants are externally cross-validated (Anthropic engineering guidance, Chroma context-rot research, AgentIF benchmark, observed failures across many users of agent-style AI tools). The derivation procedure itself is currently single-sample.

See `meta-rules.md` for evidence-tier tagging per claim and honest residual limitations.

The first projects to adopt this kit are doing the kit a favor — their derivation experience is the empirical input needed to refine the derivation procedure itself. Feedback is requested.
