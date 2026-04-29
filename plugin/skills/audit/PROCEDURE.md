# audit — PROCEDURE

Multi-round audit checkpoint logic. Each checkpoint has a clear gate;
proceed only when the gate's criterion fires.

---

## Checkpoint 1 — Scope decision

**Inputs**: invocation phrase, prior audit context (if any), trigger
condition (per `references/triggers-and-stopping.md`).

**Decision**: which slice(s) to run this round.

**Rules**:

- **Full audit, first round**: default to slices 1 (cross-doc) + 2
  (skill-drift) + 3 (backend-tools) running in parallel. These cover
  the highest-leverage drift surfaces; rounds 2+ expand based on
  what round 1 found.
- **Full audit, round N+1**: run slices that target the surfaces
  *adjacent* to where round N found drift. E.g. round 1 found drift
  in skills → round 2 audits memory/manifest content + plugin-side
  scaffolding (where skills reference but the scope didn't reach).
- **Focused slice**: run only the named slice.
- **Verification pass**: read the specific files that should have
  changed; confirm closure; no full slice dispatch.

**Output**: ordered list of slice IDs (from
`references/drift-surfaces-and-slices.md`) for this round.

**Gate**: scope is bounded — every slice has explicit file scope, no
"audit everything" without slicing.

---

## Checkpoint 2 — Dispatch in parallel

**Inputs**: slice IDs from Checkpoint 1.

**Action**: for each slice, dispatch a `general-purpose` subagent
with the brief template from
`references/drift-surfaces-and-slices.md`. **Send all slice
agents in a single message** (parallel tool-call batch) so they
run concurrently.

**Brief contents per agent**:

- Context: what session/state the audit fires from
- Files to read (explicit list — agents shouldn't guess scope)
- Specific checks (drift surfaces this slice catches)
- Output format: numbered findings + severity + suggested
  resolution + verified-clean paragraph (with claim-scope per
  `references/output-conventions.md`)
- Word cap (typically 800–1200)
- Anti-instructions: don't fix; audit only

**Gate**: all agents return structured findings.

---

## Checkpoint 3 — Synthesize

**Inputs**: agent return payloads.

**Action**:

1. Consolidate findings across slices. **Watch for convergence** —
   when multiple slices flag the same finding, that's a higher-
   confidence signal (also a sign the slice scopes overlap, which
   is fine).
2. Group by severity: **BLOCKERS first**, then drift, then
   hygiene, then expected-gap.
3. Apply the **claim-scope rule** (per
   `references/output-conventions.md`): every "verified clean"
   from agents must specify its scope. Tighten any over-broad
   claims.
4. Group findings by surface category (per
   `references/drift-surfaces-and-slices.md` taxonomy).

**Output**: synthesized audit-round artifact in working memory
(not yet a file).

**Gate**: every finding has severity + suggested resolution.
BLOCKERS are not buried.

---

## Checkpoint 4 — Commit positions on user-decision items

**Inputs**: synthesized findings.

**Action**: for each `needs-user-decision` finding, **commit to a
position with reasoning** (per memory: don't present menus, commit
to a position so discussion emerges from substance).

Format per item:

- The finding
- My call: <decision>
- Reasoning: <why this over alternatives>

User can intercept any of these before Checkpoint 5 executes them.
If user is silent or confirms, proceed.

**Gate**: every user-decision finding has a committed position.

---

## Checkpoint 5 — Execute fix-now batch

**Inputs**: confirmed positions + all `fix-now` findings.

**Action**:

1. Group fix-now items by logical theme (e.g. "scope vocabulary
   drift" — multiple files, one theme).
2. Execute in parallel where files don't overlap.
3. **One commit per coherent theme** (not one per file). Title
   convention: `audit: <theme> (closes findings #X-Y)`.
4. **For BLOCKERS**: prioritize. Fix BLOCKERS first; verify by
   re-reading the affected files / running a quick grep for
   the legacy pattern.

**Gate**: working tree clean. Each fix-now finding maps to a
commit + line edit.

---

## Checkpoint 6 — Decide round N+1 or stop

**Inputs**: this round's findings; cumulative findings from prior
rounds; stopping criterion from
`references/triggers-and-stopping.md`.

**Decision logic**:

```
if round caught zero new findings:
    stop  # nothing new to find
elif findings all in already-audited surfaces with no new scope:
    stop  # diminishing returns
elif this round explicitly verified "no new unaudited territory":
    stop  # exhaustive coverage claimed
elif a fix-now finding from this round was a BLOCKER:
    iterate one more round  # verify the fix didn't introduce drift
    # specifically: dispatch slices that touch the changed files
elif user explicitly authorizes another round:
    iterate
else:
    propose stopping; ask user for green light
```

**Output**: stop or continue.

If stopping, proceed to Checkpoint 7.
If continuing, return to Checkpoint 1 with refined scope.

**Gate**: stopping decision has explicit reasoning attached.

---

## Checkpoint 7 — Write the frozen artifact

**Inputs**: cumulative findings + closures (which findings landed
in which commits) + verdict.

**Action**: write `docs/audits/<scope>-<YYYYMMDD>.md` per
`references/output-conventions.md` format:

- Title + date + trigger reason + slice scope (which slices ran
  across all rounds)
- Verdict (pass / conditional pass / fail)
- Findings (numbered, grouped, with closure status inline if fixes
  landed)
- Verified clean (scope-bounded)
- Recommended next action

**Closure-tracking pattern** (audit doc is frozen, but a closure
banner can be appended above the title):

> **Closure status (post-<event>):** F1–F9 + U1 + U2 closed in
> commits `<sha>` / `<sha>` / `<sha>`. See HANDOFF for current
> state.

**Update HANDOFF.md** (separate commit) to reflect:

- Audit instance ran on `<date>` for `<reason>`
- Findings summary (# blockers / # drift / # deferred)
- Pointer to `docs/audits/<scope>-<YYYYMMDD>.md`

**Gate**: frozen artifact committed. HANDOFF reflects new state.
Audit instance is complete.

---

## Common patterns across checkpoints

- **Token economy**: don't read entire files into the orchestrating
  Claude's context. Delegate to subagents whose context is
  ephemeral.
- **Parallel where possible**: slices, fix-now edits across
  non-overlapping files.
- **Sequential where required**: BLOCKER fix → verification →
  next round.
- **One commit per theme**: not per file, not per finding.
- **Permission to stop**: each round must be authorized to stop
  (Checkpoint 6's explicit decision), not implicitly drift into
  more rounds.

---

## Failure modes

- **Slice agent returns garbled findings**: discard that slice,
  tighten the brief, re-dispatch. Don't include garbled output
  in synthesis.
- **Two slices contradict on the same finding**: read the
  affected file directly, decide which slice's read was correct,
  document the disagreement in the artifact.
- **Fix-now batch breaks something downstream**: revert the
  problematic fix, re-classify as needs-user-decision, surface
  to user.
- **Audit fatigue (round 5+)**: forcing-function — the stopping
  criterion is binding. If a round is justified, document the
  reason explicitly.
