# design-review — PROCEDURE

Multi-checkpoint logic for first-principles review.

---

## Checkpoint 1 — Scope decision

**Inputs**: invocation phrase, prior design-review context (if any),
trigger condition.

**Decision**: which subsystem(s) to review.

**Rules**:

- **Full first-principles review** (first-time or scheduled): default
  scope is the load-bearing foundations enumerated in
  `references/scope-and-targets.md` § "Load-bearing first-run
  targets." Six subsystems: meta-rules, entity types + decision
  rules, orchestrator, skill contract, office-config schema, plus
  any subsystem the user explicitly named.
- **Focused subsystem review**: scope is the named subsystem only.
  Look up its target spec in `references/scope-and-targets.md` to
  determine which files to read.
- **Subsequent rounds** (rare for design-review; most reviews are
  one-shot): scope is what the prior round flagged for further
  attention.

**Output**: ordered list of subsystem IDs + their file scopes.

**Gate**: every subsystem in scope has a defined file set. No
"review everything" without enumeration.

---

## Checkpoint 2 — Dispatch subagents in parallel

**Inputs**: subsystem IDs from Checkpoint 1.

**Action**: for each subsystem, dispatch a `general-purpose`
subagent with a brief built from the templates in
`references/anti-bias-mechanism.md` and
`references/scope-and-targets.md`. **Send all subagents in a single
message** (parallel tool-call batch).

Every brief contains:

1. **Context**: what session/state the review fires from + the
   stage assumption (pre-launch / pre-distribution / freedom to
   recommend total reshapes).
2. **Bias-explicit prompts**: explicit anti-status-quo language
   per `references/anti-bias-mechanism.md` § "Bias-explicit briefs."
3. **Greenfield reframe requirement** (private reasoning step):
   "Before producing findings on this subsystem, draft a
   one-paragraph from-scratch sketch in your reasoning. Then
   ground each finding by reference to that sketch."
4. **Files to read** (explicit list — agents shouldn't guess
   scope).
5. **5-category review questions** to apply to the subsystem:
   drop bloat / add missing / reshape wrong-shape / surface
   anchoring / reverse manufactured criticism.
6. **Output format**: per `references/output-conventions.md` —
   subsystem verdict (Refined / Rough-but-adequate /
   Rough-and-worth-refining / Wrong-shape) + recommendations
   grouped by bucket (Keep / Refactor / Reshape) with required
   greenfield grounding line.
7. **Anti-instructions**: do not modify files; review only.
8. **Word cap**: typically 1500–2000 (substantive review > brief
   findings).

**Gate**: all subagents return per-subsystem reports.

---

## Checkpoint 3 — Synthesize

**Inputs**: agent return payloads.

**Action**:

1. Consolidate per-subsystem reports. Each gets one section in
   the artifact-in-progress.
2. **Identify cross-cutting recommendations** — reshapes that
   ripple across multiple subsystems. Lift these into a
   dedicated cross-cutting section; don't bury in one subsystem's
   recommendations.
3. **Watch for convergence** — when multiple subsystems'
   recommendations point at the same systemic issue, that's a
   higher-confidence signal. Surface it as cross-cutting.
4. **Watch for conflict** — if subsystem A's recommendation
   contradicts subsystem B's, don't try to resolve in synthesis.
   Flag for user decision.

**Output**: artifact-in-progress with per-subsystem sections + a
cross-cutting section.

**Gate**: every recommendation has a bucket + greenfield grounding +
what-it-unlocks + what-breaks + cost. Cross-cutting section exists
(may be empty).

---

## Checkpoint 4 — Self-refinement pass

**Inputs**: synthesized artifact-in-progress.

**Action**: apply the 5-category refinement framework on the
recommendations themselves. Per `references/anti-bias-mechanism.md`:

1. **Drop bloat**: any recommendations that are oversized scope,
   premature abstraction, or duplicate concerns? Trim.
2. **Add missing**: any subsystem whose review felt thin? Any
   recommendation type that should be present and isn't?
3. **Reshape wrong-shape**: any recommendation framed in the wrong
   abstraction? Re-bucket or re-form.
4. **Surface anchoring**: are we anchored on the existing system's
   shape in a way that's obscuring better alternatives? If yes,
   re-engage greenfield reframe for the affected recommendations.
5. **Reverse manufactured criticism / restraint**: any
   recommendation that doesn't survive a "why is this
   load-bearing?" challenge? Any deferral that doesn't survive
   "why defer this specifically?" Revise or revert.

**Stopping criterion**: this pass found no Pareto improvements
across all 5 categories. If pass found at least one improvement,
apply it; one mandatory pass total. Additional passes only if a
change at this checkpoint materially shifted scope (rare).

**Output**: refined artifact-in-progress.

**Gate**: every refinement made at this checkpoint has explicit
reasoning. The "why?" challenge was applied to any aggressive
change.

---

## Checkpoint 5 — Commit positions on user-decision items

**Inputs**: refined recommendations.

**Action**: for each recommendation that requires user choice
(e.g., "Reshape vs Refactor — this could go either way"), commit
to a position with reasoning per memory directive (don't present
menus; commit to positions; let discussion emerge from substance).

Format per item:

- The recommendation
- My call: <decision>
- Reasoning: <why this over alternatives>

User can intercept any of these before Checkpoint 6 produces the
artifact.

**Gate**: every user-decision item has a committed position with
specific (not generic) reasoning.

---

## Checkpoint 6 — Write the frozen artifact

**Inputs**: the refined + position-committed artifact-in-progress.

**Action**: write `docs/design-reviews/<scope>-<YYYYMMDD>.md` per
`references/output-conventions.md` format.

**Closure-tracking pattern**: artifact is frozen at write-time.
Closures (which recommendations the user acted on, which they
deferred, which they rejected) live in HANDOFF.md and commit
history. A one-line closure banner can be appended above the
artifact title after acting on recommendations:

> **Closure status (post-<event>):** <N> recommendations acted on
> in commits `<sha>` / `<sha>`; <M> deferred to <when>; <K>
> rejected with reasoning in HANDOFF.

**Update HANDOFF.md** (separate commit) to reflect:

- Design-review instance ran on `<date>` for `<reason>`
- Verdicts per subsystem (1-line each)
- Recommendation summary (# Reshape / # Refactor / # Keep / #
  cross-cutting)
- Pointer to the artifact

**Gate**: artifact committed. HANDOFF reflects new state. The user
has a clear next step (which recommendations to act on first).

---

## Failure modes

- **Subagent's greenfield reframe is shallow** (treats existing
  shape as inevitable): discard that subsystem's report,
  re-dispatch with a tightened brief — specifically: "name 3 ways
  a from-scratch designer would build this differently, with
  reasoning."
- **Self-refinement pass finds nothing**: this is suspicious for
  first-time reviews of accumulated infrastructure. Did the
  refinement actually engage with the recommendations, or did it
  rubber-stamp? If suspicious, re-run with a tightened brief that
  forces engagement on the most-aggressive recommendation.
- **User rejects most recommendations**: not necessarily a failure
  — the existing system might genuinely be right-shape. But if
  the rejection reasoning is consistently "we already built it
  this way" (status-quo bias surfacing in the user's response),
  flag the meta-pattern: the bias might be in the user, not in
  the recommendations.
- **Recommendations span beyond the bounded scope** (a reshape of
  meta-rule X requires reviewing skill contract Y too): log as a
  follow-up design-review; don't expand current scope. Same
  anti-fatigue pattern as audit.
- **Cross-cutting section accumulates everything** (if every
  recommendation gets lifted to cross-cutting, the per-subsystem
  view becomes empty): tighten the cross-cutting threshold —
  only true 3+-subsystem reshapes belong there.

---

## Common patterns across checkpoints

- **Greenfield is required, not optional**. Without it, the
  bias-correction mechanism isn't load-bearing.
- **Manufactured criticism + manufactured restraint** are both
  real failure modes. Self-refinement at Checkpoint 4
  explicitly addresses both.
- **One commit per logical theme** if the user acts on
  recommendations (mirrors audit's pattern).
- **The user is the cross-check** in interactive mode. Trust the
  dialogue; don't add agent layers to substitute for it.
