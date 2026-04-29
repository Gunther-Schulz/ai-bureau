---
name: audit
description: This skill should be used when the user requests a system audit / drift sweep — phrases like "audit", "audit the system", "drift check", "drift sweep", "structural sweep", "pre-phase audit", "audit gate", "comprehensive audit", "Drift-Prüfung", "Systemaudit". Distinct from validate-checklist (document structural review) and validate-bausteine (baustein freshness sweep) — this audits the architecture, codebase, and documentation themselves for drift. Triggered before phase boundaries, after meta-rule additions / refactor sweeps, when stale claims are noticed, or as a periodic sweep.
version: 0.2.0
license: MIT
mcp_tools_required: []
mcp_tools_optional: [list_skills]
fallback_when_mcp_absent: "skill is filesystem-only; dispatches general-purpose subagents that read files directly. list_skills is convenience for skill enumeration but agents glob plugin/skills/*/SKILL.md if absent."
summary: Drift audit for the system itself — architecture, plugin entities, backend code, documentation. Compliance-focused (does X match what X claims to be?).
routing_mode: direct
triggers:
  - {phrase: "audit", lang: en}
  - {phrase: "drift check", lang: en}
  - {phrase: "structural sweep", lang: en}
  - {phrase: "pre-phase audit", lang: en}
  - {phrase: "audit gate", lang: en}
  - {phrase: "comprehensive audit", lang: en}
  - {phrase: "Drift-Prüfung", lang: de}
  - {phrase: "Systemaudit", lang: de}
handoffs: []
phase_role: meta
---

# audit

Comprehensive drift audit for the pbs-bureau system itself —
architecture, plugin entities, backend code, documentation, and
their cross-references. Codifies the procedure proven across
session 5's four parallel-agent audit rounds (12 + 12 + 6 + 14
findings; 3 BLOCKERS caught).

The audit is **operational**, not advisory: it dispatches focused
slice agents, synthesizes findings, surfaces user-decision items,
executes fix-now drift, and decides whether another round is
warranted. Each instance produces a frozen artifact at
`docs/audits/<scope>-<YYYYMMDD>.md`.

## Load this now

Read the three reference files (in this order):

1. `references/drift-surfaces-and-slices.md` — the 6 drift-surface
   categories the audit looks for, plus the slice library
   (10 reusable slice templates). Each slice catches a specific
   subset of drift surfaces.
2. `references/triggers-and-stopping.md` — when to run an audit
   (mandatory triggers, periodic schedule, on-suspicion); when to
   stop iterating rounds (the stopping criterion that prevented
   audit-fatigue in session 5).
3. `references/output-conventions.md` — findings format
   (numbered, structured), severity levels, resolution categories,
   the **claim-scope rule** (every "verified clean" specifies its
   scope), closure-tracking pattern.

PROCEDURE.md walks the multi-round checkpoint logic.

## When invoked

Three modes:

- **Full audit** (default) — pre-phase-boundary or major-refactor
  sweep. Dispatches multiple slices in parallel; iterates rounds
  until stopping criterion fires.
- **Focused slice** — when a specific drift surface is suspected
  (e.g. "audit the cross-doc consistency" or "audit backend code
  for legacy patterns"). Single-slice dispatch; no iteration.
- **Verification pass** — after a fix-now batch lands, re-check
  the specific findings to confirm closure. Smaller scope than
  a full slice; targeted at the changed files.

Trigger detection:

| Phrase | Mode |
|---|---|
| "comprehensive audit", "full audit", "pre-phase audit", "audit gate" | full |
| "audit X" where X names a surface (skills, backend, docs, ...) | focused |
| "verify the fixes", "confirm closure", "did the F-batch land" | verification |
| "drift check", "drift sweep", "Drift-Prüfung" | full (default) |

If unclear, ask the user once: "full audit, or focused slice on X?"

## Behavior

Follow `PROCEDURE.md`. At a glance:

1. **Scope decision** — pick which slice(s) per
   `references/drift-surfaces-and-slices.md`. Default to the
   full slice library for first-round of full audit; pick
   targeted slices for focused mode.
2. **Dispatch in parallel** — for each slice, spawn a
   `general-purpose` subagent with the slice's brief template
   from `references/drift-surfaces-and-slices.md`. Multiple
   slices run in one tool-call batch; agents return structured
   findings.
3. **Synthesize** — consolidate findings into one audit report.
   Group by drift-surface category. Flag BLOCKERS prominently.
   Apply the **claim-scope rule** to every "verified clean"
   claim.
4. **Commit positions** on user-decision items (per memory:
   commit to positions, don't present menus).
5. **Execute fix-now batch** — mechanical drift items,
   batched in one commit per logical group.
6. **Decide round N+1 or stop** — apply stopping criterion
   from `references/triggers-and-stopping.md`. If stopping,
   write the frozen audit artifact + add closure banner if
   findings landed in commits.

## Output

A frozen audit artifact at
`docs/audits/<scope>-<YYYYMMDD>.md`. Format per
`references/output-conventions.md`:

- Title + date + trigger reason + slice scope
- **Verdict** (pass / conditional pass / fail) at the top
- **Findings** (numbered, grouped by severity)
- **Closure status** (which findings landed in which commits;
  added as banner-update after fix-now batch)
- **Verified clean** (scope-bounded — the claim-scope rule)
- **Recommended next action**

The audit doc is **frozen** — it captures findings as of the
audit moment. Closures live in HANDOFF / commit history;
audit doc gets a one-line closure banner pointing forward.

## Edge cases

- **Round caught zero new findings**: stopping criterion fires.
  Declare audit complete. Write artifact with verified-clean
  emphasis.
- **Round found a BLOCKER**: don't stop. Run another round
  *after* the BLOCKER lands; verify the fix didn't introduce
  new drift in adjacent surfaces.
- **Slice agent returns garbled / off-topic findings**: discard
  that slice, re-dispatch with a tightened brief. Note in
  artifact.
- **User pushes back on a fix-now item**: pause execution at
  Checkpoint 5; revert if already-applied; re-classify as
  user-decision.
- **Audit-the-auditor**: this skill itself can drift. It's
  tested by its own first run + meta-checks of its slice
  library against actual session-5 audit slices. Schedule a
  self-audit every N runs (default: every 5 audit instances).

## Tools used

- `Agent` (built-in) — dispatch slice subagents (parallel).
- `Glob`, `Grep`, `Read` — direct filesystem reads when the
  skill body needs to verify a claim before delegating.
- `Edit`, `Write`, `Bash` — execute fix-now batch.
- `list_skills` (MCP, optional) — quick inventory; agents
  fall back to `glob plugin/skills/*/SKILL.md` if MCP absent.
