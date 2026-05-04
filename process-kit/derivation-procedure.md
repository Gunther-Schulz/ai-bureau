# Derivation procedure — producing a per-project procedure document

This is the step-by-step procedure for deriving your project's own procedure document. The output is a separate artifact that lives in your project (not in this kit). The structural invariants from `structural-invariants.md` are applied verbatim; everything else in your output is derived from your project's specifics.

## Inputs (gather before starting)

1. **Domain definition** — what kind of work is this? (software engineering, compliance documents, content production, research, design, regulatory submissions, etc.) Different domains have different artifact types and different failure surfaces
2. **Cost-of-error calibration** — for each artifact type your project produces, what is the cost of errors? How reversible are they? This drives mitigation density (per the sizing principle in `structural-invariants.md`)
3. **Failure history** — for existing projects: what has gone wrong before? Pattern-recognized, not anecdotal — same failure observed independently multiple times is the clear signal
4. **Anticipated failure modes** — for new projects: which of the structural invariants' addressed failure modes are most likely to bite given your domain?
5. **Collaboration model** — solo vs. team, AI roles, human roles, review structure, what the AI is permitted to do autonomously vs. what requires confirmation

## Step 1 — Apply structural invariants verbatim

Treat invariants 1-10 in `structural-invariants.md` as universal. Do not modify, soften, or skip them. Their *implementation details* vary per project; the rules themselves do not.

If you find yourself wanting to skip an invariant: that is a signal either (a) you're working at a scope that doesn't need this kit (apply the sizing principle and stop), or (b) you've misunderstood the invariant. Re-read.

## Step 2 — Identify protected artifacts

Within your project, which files / outputs / decisions are high-stakes? Criteria:

- Errors cascade across multiple files or downstream artifacts
- Fixing errors after-the-fact is expensive
- The artifact is referenced as authoritative by other parts of the system
- Errors are not visible immediately (they surface later, after compounding)

These are the artifacts that warrant structural protection (hooks, gates, deterministic checks). Lower-stakes artifacts get advisory rules at most.

Output of this step: a list of protected-artifact categories, with cost-of-error notes per category.

## Step 3 — Derive your hooks

For each protected-artifact category from Step 2:

- What pre-condition must hold before writing? (e.g., specific source documents must have been read recently in this session)
- What content patterns are forbidden? (e.g., narrative breadcrumbs that should live in commit messages, not artifact content; placeholder text that escaped a draft)
- What composition rules must hold? (e.g., this artifact type must reference X but never Y; cross-references must resolve)
- What state must be valid after writing? (e.g., the artifact must be syntactically valid; the cross-reference graph must remain acyclic)

These become hooks (PreToolUse / PostToolUse / equivalent in your tooling). Implement as deterministic checks — regex, file-existence, session-state inspection — not as prose instructions to the AI. Per invariant 5.

Output of this step: hook specifications (what they check, what they block, what error message they emit).

## Step 4 — Derive your named skills

A procedure earns codification as a named skill when:

- It repeats across multiple work-units (a project-calibrated threshold; e.g., observed ≥3 times)
- It has steps that are silently dropped under context pressure when not codified
- It benefits from re-reading the source on each invocation (per invariant 6)

For each candidate skill: write a SKILL document with explicit procedure, named sections, and the failure mode the skill protects against. Reference the skill from procedures that should invoke it. Specify "READ this file at every invocation" as part of the skill's invocation discipline.

Output of this step: a list of named skills, each with a SKILL document.

## Step 5 — Derive your anchor documents

What must auto-load (or be read first) at every session start? Candidate roles:

- A vision / goal document — what this project is for; the success criteria the procedure must keep serving
- A working-discipline document — how the team / human / AI operate together
- A current-state document — handoff log, in-progress work, recent decisions
- A backlog document — phase-tagged forward-work tracker

Keep auto-loaded content compact. If anchor documents grow large, split them: index in the auto-loaded layer, detail loaded on-demand. Per invariant 2.

Output of this step: list of anchor documents, with size budgets and split-points where applicable.

## Step 6 — Derive your sub-agent routing thresholds

What counts as a "high-stakes cascade" in your domain? Implementation: a numeric threshold (e.g., ≥N protected files touched in one work-unit) plus categorical rules (e.g., any change to artifacts of type X always routes to sub-agent regardless of count).

Above the threshold: sub-agent dispatch is mandatory. Below it: main session may execute directly.

Output of this step: explicit routing rules with named thresholds.

## Step 7 — Derive your HARD STOP boundaries

What is a "logical work unit" for your project? Examples:

- One architectural decision committed
- One feature implemented and tested
- One document section landed and cross-referenced
- One regulatory submission package assembled

At the boundary: write to handoff log, commit, push (or domain equivalent), STOP. Per invariant 2 (externalize state at boundaries).

Output of this step: definition of "logical work unit" for the project plus the close-out actions at each boundary.

## Step 8 — Calibrate sizing

For each artifact type and work-unit type, decide mitigation density:

- **High cost / low reversibility**: full stack of invariants applied; hooks; sub-agent routing; writer-reviewer separation; explicit re-grounding
- **Medium**: structural invariants 1, 2, 6, 8 minimum (context, re-grounding, basis-honesty); other invariants advisory
- **Low**: advisory only; treat the invariants as guidance not enforcement

The sizing decisions belong in your derived procedure document, made explicit so the project can revisit them as cost calibration shifts.

Output of this step: a sizing table (artifact type → mitigation density → which invariants apply structurally vs. advisorily).

## Step 9 — Write your project's procedure document

Combine outputs of Steps 2-8 into a single anchor document for your project. Suggested sections:

- What this procedure is for (your goal-doc or a pointer to it)
- Structural invariants applied (reference this kit's `structural-invariants.md` so updates propagate)
- Protected artifacts (list, with cost-of-error and mitigation density per type)
- Hooks (what they check, what they block)
- Named skills (with cross-references to SKILL files)
- Anchor documents (what auto-loads at session start)
- Sub-agent routing rules
- Work-unit boundaries
- Sizing table
- Maintenance protocol (per Step 10)

## Step 10 — Maintenance protocol for the derived procedure

Your derived procedure must include its own maintenance discipline. This lives in the *output*, not in this kit:

- **Failure log** — when a mitigation fired correctly, when it should have but didn't, when it fired falsely. Date + work-unit + mode + outcome
- **Refresh cadence** — periodic re-read of own procedure (project-calibrated; e.g., every N work-units or every M months)
- **Retirement criteria** — when to remove a mitigation that hasn't fired or only fires falsely
- **Adoption criteria** — when to add a new mitigation (observed failure ≥N times within this project; never speculative)
- **Re-derivation triggers** — when to re-run this whole derivation procedure (major domain shift, recurring failure not addressed, kit itself updated per `self-application.md`)

These thresholds (N, M) are project-calibrated. The kit does not prescribe specific numbers — calibrate from your domain's failure cadence and cost-of-error.

## Output

A single procedure document (or small set of documents) anchored in your project. Once derived, it becomes the project's living procedure — evolved by its own maintenance protocol, not by re-running this kit.

The kit is consulted again only when the kit itself updates (per `self-application.md`).
