# Triggers + stopping criterion

## When to run an audit

### Mandatory triggers

These are non-negotiable. If one fires, run an audit before the
next blocking action.

1. **Before phase boundaries**: pre-RAG kickoff, pre-deployment,
   pre-second-office-bind, pre-major-feature-launch. The
   session-5 pre-RAG audit is the canonical example.

2. **After meta-rule additions**: any change to ARCHITECTURE.md
   meta-rules ripples through all skills. The execution-locality
   meta-rule (5) added in session 4 was the trigger for the
   alignment sweep + session-5 audit.

3. **After major refactor sweeps**: the orthogonality refactor
   (universal × domain × state) was the trigger for the
   session-5 audit. Any refactor that touches multiple entity
   types qualifies.

4. **Before "audit gate closed" claims**: never declare a gate
   closed without running at least one full audit. Session-5's
   first HANDOFF claimed the gate was closed prematurely; rounds
   3 + 4 found 3 BLOCKERS. The lesson: claims of closure require
   verification.

5. **After a BLOCKER lands**: any fix that touches load-bearing
   code (chunkers, schema, scope vocabulary, ingest pipeline)
   should be followed by a verification pass to catch
   side-effects.

### Periodic triggers

If no mandatory trigger fires, run a full audit:

- **Every 10 sessions** (or quarterly, whichever fires first).
- **Before any user-facing release** (plugin version bump that
  changes tool surface or skill set).

This periodic discipline catches slow-drift that no specific
event flagged.

### On-suspicion triggers

Any of these is enough to justify an audit (or at least a
focused slice):

- A "verified clean" claim was noticed and feels stale
- A skill's behavior surprised the user (suggests frontmatter ↔
  body drift)
- A reference (path / tool name / handoff target) looked
  outdated
- The user senses staleness — even one example is enough

In on-suspicion mode, prefer a **focused slice** to a full
audit. Cheap; surfaces specific drift; builds confidence
without audit fatigue.

---

## When to stop iterating rounds

The session-5 audit ran 4 rounds. Each round caught new things.
Without a binding stopping criterion, audits drift into "let's
run another round just in case" forever. The criterion below is
**binding** — if it fires, stop, don't run another round just to
feel safe.

### Stopping criterion (decide at Checkpoint 6 of PROCEDURE)

```
if round caught zero new findings:
    STOP  # genuinely nothing new
elif findings all in already-audited surfaces with no new scope:
    STOP  # diminishing returns
elif this round's brief explicitly verified "no new unaudited
     territory" (the slice 10 final-pass verdict):
    STOP  # exhaustive coverage claimed
elif a fix-now finding from this round was a BLOCKER:
    iterate one more round  # verify the fix didn't introduce
                            # adjacent drift
    # the verification round's scope = changed files + their
    # dependents only, not a full re-sweep
elif user explicitly authorizes another round:
    iterate
else:
    propose stopping; ask user for green light
```

### Examples from session 5

- Rounds 1, 2, 3 each found new categories of drift → continue.
- Round 3 found 2 BLOCKERS → ran round 4 specifically to verify
  + check adjacent surfaces.
- Round 4 explicitly verified "no new unaudited territory" + had
  one new BLOCKER (the live-code one) → fixed BLOCKER, ran a
  short verification (re-grep for `global \| domain \| project`)
  → stopped.

The signal that mattered: each successive round had to *expand
scope* to find new things. Round 4's verdict said scope was
exhausted. That's a binding stop.

### Signals that a round is wasted

If you notice any of these mid-round, abort and stop:

- Slice agents are returning the same findings the prior round
  caught
- Slice scopes overlap entirely with prior rounds
- The brief is "audit everything again" without targeted
  surfaces
- The user is asking "are we done yet?"

Audit fatigue is a real cost. Binding stopping prevents it.

---

## Audit cadence in practice

| Trigger | Mode | Slices |
|---|---|---|
| Pre-phase boundary | Full audit | 1+2+3 → expand based on findings |
| After meta-rule addition | Full audit | All slices touching the affected entity types |
| After refactor sweep | Full audit | All slices |
| Before audit-gate-closed claim | Full audit | Whatever's needed for the claim's scope |
| Periodic | Full audit (lighter — assume less drift) | 1+2+3, stop early if clean |
| On suspicion of one drift | Focused slice | Targeted slice for that surface |
| Post-BLOCKER fix | Verification pass | Changed files + immediate dependents |

---

## When NOT to audit

- During active feature development. Audits are gates between
  phases, not a continuous activity.
- Mid-debugging. Different problem class; debugging is targeted,
  audits are systematic.
- After every commit. That's a hook (which we explicitly defer
  per ARCHITECTURE meta-rule 5).
- For every minor wording fix. Reserve audits for state changes
  in skills, code, manifests, conventions.
