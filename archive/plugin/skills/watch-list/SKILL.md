---
name: watch-list
description: This skill carries the continuous watch-list infrastructure — six triggers (T1 reusable-pattern / T2 citation-drift / T3 baustein-promotion / T4 style-deviation / T5 standing-rule / T6 capability-gap) detected during work, with explicit data model, decay rules, and the four-way decision menu. Mostly invoked by the orchestrator as part of normal workflow rather than by user phrase — but admin/debug phrases like "show watch queue", "check watch list state", "watch-list status" route here directly.
version: 0.2.0
license: MIT
mcp_tools_required: []
mcp_tools_optional: [list_bausteine]
fallback_when_mcp_absent: "skill is mostly an in-conversation protocol over ephemeral session state — no contract-bearing reads of its own. The T3 detection (use_count check) needs list_bausteine to read use_count from frontmatter; without it, T3 detection is skipped (skill cannot read invalidation-contract fields by direct Read per ARCHITECTURE meta-rule 4 fail-closed corollary). Surfacing a partial watch list with T1/T2/T4/T5/T6 still works since those don't read contract-bearing data."
summary: Continuous in-session watch list — surfaces six trigger types via four-way decision menu with explicit data model + decay rules; auto-backlogs T6 capability gaps. Mostly invoked by orchestrator.
routing_mode: delegated
triggers:
  - show watch list
  - watch-list status
delegated_from: [orchestrator]
handoffs: [save-baustein, promote-to-skill, validate-latex-style, verify-citations]
phase_role: utility
---

# watch-list

Continuous-monitoring infrastructure for the orchestrator. Six
trigger types (T1-T6) fire whenever they match in conversation or
in produced output. Each surfaces a four-way decision menu (per
trigger; T6 auto-backlogs without menu — see §6). Explicit data
model + decay rules prevent the user from being spammed by the
same trigger across long sessions.

Per ARCHITECTURE meta-rule 4 (execution-determinism): trigger
*detection* is in skill (judgment); but the queue/TTL/dedup
state is session-ephemeral and stays in skill, not MCP. Persisted
side-effects (saved bausteine, backlog entries, baustein flags)
go through MCP gates as before.

(Extracted from orchestrator skill in v0.5 per
design-review/foundations-20260429.md Subsystem 3 recommendation —
"watch-list (T1-T6) needs explicit data model and decay rules" +
"start with watch-list extraction only.")

## Load this now

Read `references/triggers.md` for the per-trigger detection
criteria, examples, and side-effects on accepted action.

PROCEDURE.md walks the queue/TTL/dedup data model, the four-way
decision menu, and the decay rules.

## When invoked

Two modes:

- **Continuous (delegated)**: orchestrator's normal workflow —
  whenever a trigger matches in conversation or produced output,
  orchestrator hands off to this skill to enqueue + surface +
  dispatch the user's choice. This is the dominant invocation
  pattern.
- **Direct admin (rare)**: user phrases like "show watch queue",
  "watch list status" surface the current queue state for
  inspection. Useful for debugging or session-end review.

## Behavior (continuous mode)

Follow `PROCEDURE.md`. At a glance:

1. **Detect**: trigger matches T1-T6 criteria (see
   `references/triggers.md`).
2. **Enqueue**: add candidate to per-session queue with TTL +
   dedup signature (per PROCEDURE §1).
3. **Surface decision** at the right moment (immediate for
   high-priority triggers; sweep at natural pauses for batched
   surfacing per §2).
4. **Dispatch on user decision** via four-way menu (capture-now /
   handle-now / backlog / drop) per §3.
5. **Decay**: at session close, drop items past TTL; backlog any
   T6s still queued.

## Output

- Per surfaced item: one-line menu format
  `Noticed: <thing>. → capture-now / handle-now / backlog / drop?`
- Per accepted action: confirmation in one line.
- Per backlog: append entry to `<repo>/memory/product-backlog.md`
  with date + project context + proposed action.

In admin mode: dump current queue state.

## Edge cases

- **Same trigger repeats across turns**: dedup signature catches
  this; suppress repeat surfacings within TTL window.
- **Multiple triggers fire simultaneously**: queue all, sweep at
  next natural pause, surface 1-N as a batched menu.
- **User declines decision menu**: don't push; mark as deferred,
  re-surface next natural pause.
- **T6 (capability gap)**: don't surface menu — auto-append to
  product-backlog with date + workaround context. T6 is internal
  observation; menu was wrong audience (see PROCEDURE §6).

## Tools used

- `list_bausteine` (MCP, optional) — used by T3 detection to
  check use_count freshness; falls back to filesystem scan of
  baustein frontmatter.
- `Edit` / `Write` — for backlog append + state writes.
- Hands off to:
  - `save-baustein` for capture-now decisions on T1 triggers
  - `promote-to-skill` for capture-now decisions on T3 triggers
  - `validate-latex-style` for handle-now on T4 triggers
  - `verify-citations` for handle-now on T2 triggers
