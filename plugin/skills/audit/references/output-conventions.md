# Output conventions

## Findings format

Every finding is structured. Subagents return findings in this
shape; the orchestrating skill consolidates without reformatting.

```
### Finding N — <one-line summary>

- **What:** <what's wrong / drifted / missing>
- **Where:** <file:line or file path>
- **Severity:** blocker | drift | hygiene | expected-gap
- **Suggested resolution:** fix-now | defer-with-reasoning | needs-user-decision
- **Reasoning** (optional): <when severity / resolution isn't obvious>
```

Findings are numbered consecutively across the entire audit (not
per-slice — ergonomic for cross-reference in commit messages).

---

## Severity levels

### blocker

Will cause incorrect behavior on first run, or silently corrupts
data, or breaks a load-bearing claim.

**Examples**:
- Live code returning legacy values that downstream consumers
  treat as new (session-5 round-4: ingest.py:217 returning
  `"global"` for baustein source_subtype)
- Schema doc using vocabulary that the code doesn't accept
- HANDOFF claim "audit gate closed" being false

**Action**: BLOCKERS land in the next commit. Don't defer.

### drift

Documentation or convention mismatch that doesn't break
behavior immediately but seeds further drift if left.

**Examples**:
- Stale numerical claims
- Legacy scope vocab in a doc
- Missing meta-rule-5 frontmatter on a skill
- Trigger-phrase overlap

**Action**: include in fix-now batch alongside blockers.

### hygiene

Dead code, unused variables, naming inconsistency, low-impact
typos.

**Examples**:
- Unused regex constant
- F-string in log call (preferred is %-format)
- Email probe wording inconsistent across adapters

**Action**: include in fix-now batch when convenient. Don't
gate audit-complete on these.

### expected-gap

Known unimplemented item that's tracked and intentional.

**Examples**:
- `tests/` directory absent (deferred per
  `docs/backend-conventions.md` migration order)
- ColPali integration absent (Phase 3a)
- LanceDB schema lacks `modality` column (Phase 3a)

**Action**: defer-with-reasoning. Mention in audit artifact for
completeness; don't fix.

---

## Resolution categories

### fix-now

Mechanical, bounded, no judgment call. Execute in fix-now batch.

**Default for**: blockers, drift items where the fix is obvious.

### defer-with-reasoning

Known gap that's intentional. Document the reasoning + the
revisit trigger.

**Default for**: expected-gap; drift items the user has
explicitly deferred (e.g. session-5's `_ai/` vs. `.ai/` pick).

### needs-user-decision

Trade-off where a position needs to be committed but the choice
isn't obvious.

**Default for**: schema convention choices (e.g. retroactive
version rebump?), naming changes affecting external contracts,
strategic deferrals.

For these, **commit to a position with reasoning** at audit
synthesis time (per memory: don't present menus). User can
intercept at Checkpoint 5 of PROCEDURE.

---

## The claim-scope rule

Every "verified clean" assertion must specify its scope. This is
the rule that prevents the session-5 round-1 overclaim
(scope-orthogonality "verified clean" was true for skill bodies
but not backend docs — round 4 caught the overclaim).

### ❌ Wrong (over-broad)

> **Verified clean**: Bausteine path orthogonality.

### ✅ Right (scope-bounded)

> **Verified clean**: Bausteine path orthogonality across all
> 16 SKILL.md bodies (this slice's scope). **Backend docs and
> live ingest code not audited in this slice** — see slice 6
> (backend-code-deep) and slice 8 (READMEs) for those surfaces.

The pattern: state what was checked + what *adjacent surface*
the slice didn't reach. The latter prevents future readers from
assuming the claim is system-wide.

### Apply at Checkpoint 3 (synthesis)

When consolidating, tighten any agent-returned "verified clean"
claim that omits scope. If you can't determine the scope from
the agent's brief, ask the agent for clarification or conduct a
quick spot-check yourself before passing the claim through.

---

## Audit artifact format

```markdown
# <Audit name> — <YYYY-MM-DD>

> **Closure status (post-<event>):** <closure summary if fixes
> have landed; this banner is appended after-the-fact, not at
> initial write>.

**Trigger**: <which mandatory/periodic/suspicion trigger fired>
**Slices run**: <list of slice IDs across all rounds>
**Rounds**: N (round 1 caught X findings; round N caught Y
findings)

## Verdict

**<Pass | Conditional pass | Fail>** — <one-paragraph rationale>.

If conditional pass: list the conditions for full close.

---

## Findings

### Blockers

[grouped, numbered, structured per Findings format]

### Drift (fix-now)

[grouped, numbered]

### Hygiene

[grouped, numbered]

### Expected-gap (defer-with-reasoning)

[grouped, numbered]

### Needs-user-decision

[grouped, numbered, with my committed positions]

---

## Verified clean

[scope-bounded claims per claim-scope rule]

---

## Recommended next action

[concrete: which fix-now items first; which user-decisions to
resolve; whether another round is warranted]
```

---

## Closure tracking

The audit artifact is **frozen** — written at audit-synthesis
time, captures findings as of that moment. Don't edit findings
after the fact (it muddies the historical record).

**Closures live in two places**:

1. **Closure banner** — a single one-line / two-line block
   appended above the artifact's title, pointing at the commits
   that landed fixes. Example:
   ```
   > **Closure status (post-session-5):** F1–F9 + U1 + U2 closed
   > in commits ad01b18 / d0f3f91 / 501eaa1.
   ```

2. **HANDOFF.md** — the active session-state doc. Captures
   which findings closed in which commits, plus rolls up the
   verdict.

This keeps the artifact a snapshot while the closure trail is
discoverable.

---

## File naming + location

Audit artifacts live in `docs/audits/`:

```
docs/audits/<scope>-<YYYYMMDD>.md
```

Examples:
- `docs/audits/pre-rag-20260429.md`
- `docs/audits/post-meta-rule-5-20260601.md`
- `docs/audits/quarterly-20260930.md`

The historical `docs/audit-pre-rag.md` predates this skill and
stays at its current path for reference (closure banner already
in place). Future audits use the `docs/audits/` subdir.
