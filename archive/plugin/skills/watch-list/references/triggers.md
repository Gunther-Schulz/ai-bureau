# Watch-list trigger taxonomy

Six triggers fire during continuous monitoring. This file documents
the detection criteria, examples, and side-effects for each.

---

## T1 — Reusable pattern

**Fires when**: a drafted argument, justification, or section reads
as something that could apply across projects in the same domain
(or across multiple domains for universal-scope candidates).

**Detection signals**:
- Boilerplate-shaped prose ("Die Eingriffsregelung erfordert...")
- Citation-anchored argumentation that could be parameterized
- Standardized §-references with consistent reasoning patterns

**Side-effect on accept**:
- **capture-now** → `save-baustein` with type `argumentation` or
  `text-block`, scope determined by content (universal/domain/state)
- **backlog** → product-backlog entry "candidate baustein: <text>"
- **drop** → no action

**Examples**:
- A standardized §44 BNatSchG reasoning paragraph (PV-FFA domain)
- A boilerplate Zusammenfassende Erklärung opening (universal)

---

## T2 — Citation drift

**Fires when**: a legal citation in memory or in the current
document differs from what the RAG returns for the same reference
today (different amendment form, different paragraph numbering
post-amendment, different cited form).

**Detection signals**:
- `verify-citations` returns "drift detected" for a §-reference
- A baustein's `verified_against_version` predates the current
  manifest's `current_amendment_form`
- A document references "§45 Abs.7 Nr.5 BNatSchG i.d.F. 2024" but
  current manifest is "i.d.F. 2025"

**Side-effect on accept**:
- **handle-now** → `verify-citations` re-runs against current
  reference; if user authorizes, updates citation text in-place
- **capture-now** → mark baustein `flagged` with reason
  "citation drift detected"
- **backlog** → product-backlog entry "citation update needed"
- **drop** → user judges drift is non-substantive

**Detection priority**: HIGH (correctness boundary). Surface
immediately, not at natural pause.

---

## T3 — Promotion

**Fires when**: a baustein has been referenced ≥ 3 times across
the last 30 days of session history (use_count from
`list_bausteine` / per-baustein frontmatter), suggesting codify-as-
skill is justified.

**Detection signals**:
- `list_bausteine` returns entries with `use_count >= 3`
- New session-history reference brings a baustein over the threshold

**Side-effect on accept**:
- **capture-now** → invoke `promote-to-skill` skill
- **backlog** → product-backlog entry "promote candidate: <name>"
- **drop** → user judges baustein remains baustein-shaped

**Detection priority**: LOW (stable enough to wait for natural
pause). Once per session per baustein (TTL = session).

---

## T4 — Style deviation

**Fires when**: the current document violates `style-spec.md`
(different document class, different package set, different
geometry, missing required macros).

**Detection signals**:
- `validate-latex-style` returns findings
- Manual scan of preamble vs. style-spec divergence
- Compile warnings about missing required macros

**Side-effect on accept**:
- **handle-now** → invoke `validate-latex-style` recommendations,
  apply the fix
- **backlog** → product-backlog entry "style cleanup: <file>"
- **drop** → user judges deviation is intentional / project-
  specific

**Detection priority**: MEDIUM (immediate during review-draft,
batched at natural pause otherwise). Per-trigger cap of 3 per
session (style deviations cluster).

---

## T5 — Standing rule

**Fires when**: the user says "always X", "remember Y", "never Z",
"from now on", or any phrasing that prescribes future behavior
across sessions.

**Detection signals**:
- Conversation patterns matching the above
- User explicitly proposes a convention or override

**Side-effect on accept**:
- **capture-now** → `save-baustein` with type `rule` or
  `standing-rule`; scope determined by content (often universal
  for cross-project rules, project for project-specific)
- **backlog** → product-backlog entry "rule pending"
- **drop** → user retracts or judges rule was situational

**Detection priority**: HIGH (user expressed an intent — confirm
before proceeding). Once-per-session per rule (TTL = session).

---

## T6 — Capability gap

**Fires when**: a tool, skill, or template that would have helped
does not exist. The orchestrator notices this when it has to
perform a workaround.

**Detection signals**:
- An MCP tool call would have been ideal but the tool doesn't
  exist; orchestrator falls back to filesystem
- A skill would have handled the situation but the skill doesn't
  exist; orchestrator does the work inline
- A template / scaffold is missing; orchestrator hand-builds

**Side-effect** (NO menu — auto-backlog per PROCEDURE §6):
- Always auto-append to `<repo>/memory/product-backlog.md` with:
  - date + project context
  - what's missing (tool/skill/template name)
  - what the orchestrator did instead (workaround)
- At session-close: one-line summary "T6 capability gaps captured: N"

T6 is internal observation about the toolkit; user can't typically
act on it in-the-moment. Auto-backlog converts T6 into a
gap-tracking signal instead of menu fatigue.

---

## Trigger detection ownership

Most triggers are detected by the orchestrator during normal
workflow:

- **T1, T5**: detected by orchestrator parsing user/assistant
  prose
- **T2, T4**: detected during review (`verify-citations`,
  `validate-latex-style`); these skills hand candidates back to
  watch-list via the orchestrator
- **T3**: detected at session-open or after `list_bausteine` calls
  (orchestrator watches use_count)
- **T6**: detected by orchestrator when it has to perform a
  workaround; logged immediately

Watch-list skill receives the candidate and handles the queue +
surface + dispatch protocol.
