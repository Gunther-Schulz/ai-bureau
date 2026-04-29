# watch-list — PROCEDURE

Continuous in-session watch list. Detection lives in orchestrator
+ this skill; the **data model** (queue, TTL, dedup, per-session
cap) and **decision dispatch** logic live here.

---

## Checkpoint 1 — Data model (session-ephemeral)

The watch queue is a list of `WatchItem` records held in skill
state for the duration of the session. **Not persisted across
sessions** — the queue is session-ephemeral; persisted side-effects
(saved bausteine, backlog entries, baustein flags) go through MCP
gates as normal.

```
WatchItem:
  id: <uuid-or-hash>
  trigger: T1 | T2 | T3 | T4 | T5 | T6
  signature: <dedup-key>      # e.g. for T4: "style-violation:<file>:<rule-id>"
  description: <one-line>      # what was noticed
  context: {project?, document?, line?, ...}
  enqueued_at: <timestamp>
  surfaced_at: <timestamp | null>
  decision: pending | capture-now | handle-now | backlog | drop | deferred
  ttl_minutes: 60              # default; per-trigger overrides per §4
```

The queue is the in-conversation-memory canonical state; reads are
live introspection.

**Per-session caps**:

- **Total surface count** per session: 12. After 12 surfacings,
  remaining triggers go directly to deferred (re-surface next
  session).
- **Per-trigger surface cap**: 3 per session for T4 (style
  deviations are repetitive); 2 per session for T1, T2 (drafts
  often have clusters); no cap for T3, T5, T6.

These caps avoid the "spam the user with the same kind of finding
on every turn" failure mode design-review S3 flagged.

---

## Checkpoint 2 — Detection + enqueue

When orchestrator (or another skill) hands off a candidate
trigger:

1. **Compute signature** per trigger type (per §4 below).
2. **Check dedup**: if a queue item with the same signature
   exists with status ∈ {pending, surfaced, deferred} and is
   within TTL → skip (dedup hit).
3. **Check per-trigger cap**: if surface count for this trigger
   in this session ≥ cap → mark deferred immediately.
4. **Enqueue**: add to queue with status `pending`.

---

## Checkpoint 3 — Surface (timing + batching)

**Per-trigger surfacing semantics**:

| Trigger | Surface timing |
|---|---|
| T1 reusable-pattern | At natural pause (compile success, awaiting input, "draft ready"); batched if 2+ pending |
| T2 citation-drift | Immediate (correctness; user wants to know now) |
| T3 promotion | At natural pause; never mid-stream |
| T4 style-deviation | Immediate during review-draft; batched at natural pause otherwise |
| T5 standing-rule | Immediate (user just said "always X" — confirm before proceeding) |
| T6 capability-gap | **NEVER surface menu** — auto-backlog (see §6) |

**Surfacing format** (single line, no surrounding prose):

```
Noticed: <description>. → capture-now / handle-now / backlog / drop?
```

For batched surfacings (multiple T1s queued at natural pause),
list each on its own line under a single "Noticed:" header.

After surfacing, mark the item `surfaced` with timestamp.

---

## Checkpoint 4 — TTL + dedup signatures

**Per-trigger TTL** (after which a re-detection causes re-enqueue):

| Trigger | TTL |
|---|---|
| T1 | 60 min |
| T2 | 15 min (re-fetch may happen quickly) |
| T3 | session (T3 once per session per baustein) |
| T4 | 30 min |
| T5 | session |
| T6 | session (de-dup capability-gap by tool/skill name) |

**Dedup signature** (the key the dedup check matches against):

| Trigger | Signature |
|---|---|
| T1 | `t1:<doctype>:<sha256(text-block)>` |
| T2 | `t2:<law>:<paragraph>:<cited-form-hash>` |
| T3 | `t3:<baustein-name>` |
| T4 | `t4:<file>:<rule-id>` |
| T5 | `t5:<sha256(rule-text)>` |
| T6 | `t6:<missing-tool-or-skill-name>` |

Same signature within TTL = same finding = suppress.

---

## Checkpoint 5 — Four-way decision menu (T1-T5)

When the user replies to a surfaced T1-T5, parse against the
decision table:

| Reply matches | Decision |
|---|---|
| "save", "speichern", "capture", "ja capture", "jetzt speichern" | **capture-now** |
| "fix", "do it", "machen", "handle", "jetzt machen", "now" | **handle-now** |
| "later", "park", "park it", "backlog", "merken", "erstmal nicht" | **backlog** |
| "no", "nein", "drop", "skip", "egal", "nicht relevant" | **drop** |
| Anything else, or contradictory tokens | **ASK** one clarifying question |

Then dispatch:

- **capture-now**: invoke the appropriate skill — `save-baustein`
  for T1, `promote-to-skill` for T3, `save-baustein` (rule-flavored
  baustein) for T5. Confirm in one line.
- **handle-now**: perform the implied action — re-cite via
  `verify-citations` for T2, fix via `validate-latex-style`
  recommendations for T4, save standing rule via `save-baustein`
  for T5. Hand back to flow when done.
- **backlog**: append to `<repo>/memory/product-backlog.md` with
  date + project context + proposed action. Return.
- **drop**: acknowledge in one word. Return.

Never silent capture. Every memory-write or backlog-append
corresponds to an explicit four-way decision the user authorized.

---

## Checkpoint 6 — T6 special case (auto-backlog, no menu)

T6 (capability gap) is an internal observation about the toolkit
— missing tool, missing skill, missing template, missing helper.
The user can't act on most T6s anyway (the orchestrator just
worked around it). Surfacing a menu wastes attention.

**T6 protocol** (per design-review S3 recommendation):

1. When detected, append to `<repo>/memory/product-backlog.md`
   with:
   - date + project context
   - what's missing (tool/skill/template name)
   - what the orchestrator did instead (workaround)
2. Mark item `decision: backlog` with auto-flag.
3. **Do NOT surface menu**.
4. At session-close (per §7), surface a one-line summary if any
   T6s were captured this session: "T6 capability gaps captured:
   N (see product-backlog)."

This makes T6 a real gap-tracking signal instead of menu fatigue.

---

## Checkpoint 7 — Session close + decay

At session close (when the user winds down or explicitly invokes
"end session"):

1. **Decay queue**: drop pending items past TTL.
2. **Surface deferred items**: list any items still in `deferred`
   state with a one-line summary. User can elect to surface them
   now or accept the deferral.
3. **T6 summary**: report count of T6s captured this session.
4. **Persist nothing**: queue itself doesn't persist; only the
   side-effects (saved bausteine, backlog entries) persist.

---

## Failure modes

- **Trigger signature collision** (two different findings hash
  to the same key): drop the second's enqueue. Rare but possible
  with weak hashes; signature scheme errs toward dedup.
- **User reply ambiguous**: ASK one clarifying question per the
  decision-menu's `ASK` branch. Don't assume.
- **Per-trigger cap hit mid-session**: subsequent triggers go
  straight to deferred without surfacing. Visible at session-close
  decay step.
- **Skill-call from menu fails** (e.g. `save-baustein` errors):
  surface the error to user, item remains in queue for retry.
- **T6 cascade** (capability gap detection cascades — missing tool
  exposes missing helper exposes missing skill): each gets its
  own product-backlog entry; no de-dup across the cascade by
  default. Manual cleanup at session-end if user wants.

---

## Common patterns across checkpoints

- **No silent state changes**: every memory-write or backlog-append
  has explicit user authorization (T6 exempted as
  internal-observation).
- **Decay is binding**: TTL + per-trigger caps prevent
  spam-the-user mode. Cap-overrides require explicit user request
  ("show me all T4 deviations regardless of cap").
- **Hand-off via existing skills**: watch-list doesn't write
  bausteine itself — it dispatches to `save-baustein` and similar.
  Keeps the watch-list skill focused on the queue/decision
  protocol, not on the side-effects.
