# Anti-bias mechanism

The load-bearing core of design-review. Without an explicit
mechanism, "review for design soundness" collapses to incremental
critique under the weight of incumbent advantage. This file
specifies the mechanism + how it applies to subagent briefs + the
5-category refinement framework that backs it.

---

## The status-quo bias problem

When reviewing existing infrastructure, several biases push toward
incremental thinking and away from radical reshapes:

| Bias | Manifestation |
|---|---|
| **Incumbent advantage** | "It exists, therefore it's worth keeping" |
| **Sunk cost fallacy** | "We already built this; rewriting wastes that work" |
| **Confirmation bias** | "We picked this design — surely we picked correctly" |
| **Status-quo bias** | "Changing things is risky; not changing things is safe" |
| **Maintenance perspective** | "How do we improve this?" instead of "What would we build?" |

These collectively produce **surface-level patches where structural
changes are warranted**. The right call (when warranted) might be
"delete this concept and rewrite from scratch," but it gets
filtered out before being voiced.

The five biases share a root: they all treat the existing form as
the **baseline against which alternatives must justify themselves**.
The corrective is to invert the baseline — make the alternative
(greenfield) the baseline, and require the existing form to justify
itself against that.

---

## The greenfield reframe

For each subsystem under review, the agent is required to engage
with this question (in private reasoning, not output):

> If we were starting today, with the same goals + constraints +
> system context, but no existing implementation — what would we
> build for this subsystem?

The greenfield sketch doesn't have to be exhaustive — a paragraph
of architecture-level thinking is enough. What matters is that the
agent **commits** to a hypothetical design, not just criticizes
the existing one.

Then, every finding the agent produces is **grounded against the
greenfield**:

- "This concept doesn't exist in the from-scratch design" → finding
  candidate
- "From-scratch would organize this differently" → finding candidate
- "From-scratch would have less of this" → finding candidate
- "From-scratch would have more of this" → finding candidate
- "From-scratch would look identical" → no finding (this part is
  already right-shape)

**Why required-but-private**: required because LLMs under pressure
to be helpful default to incremental thinking, and "just keep
greenfield in mind" doesn't reliably survive that pressure. Private
because producing the greenfield as a separate output artifact is
ceremony — the agent has to commit to it in reasoning, but the
artifact only carries findings + grounding lines.

The greenfield mindset is the **only mechanism** that catches
deep-design issues. Surface bloat we'd find with simple code
review. Wrong-shape abstractions we ONLY find when forced to
imagine an alternative.

---

## Bias-explicit briefs

Every subagent brief MUST include this language verbatim or its
close paraphrase:

> **Stage assumption**: the system is in a pre-launch /
> pre-distribution context. There are no users to break, no
> production data to migrate, no shipping deadline pressure.
> Radical rewrites are cost-cheap. **Recommend total reshapes
> freely; do NOT bias toward incremental change.**
>
> **Anti-bias prompts**: when you find yourself reasoning "this
> exists therefore it's worth keeping" / "rewriting wastes prior
> work" / "the existing design must be considered correct," that's
> incumbent advantage talking. Set it aside. Use the greenfield
> reframe (above): if starting today, what would you build?
> That's the baseline. The existing form has to justify itself
> against that, not the other way around.
>
> **Output expectation**: be willing to recommend Reshape (delete
> the concept and rebuild differently) when warranted. Don't
> default to Keep or Refactor out of caution.

This isn't decoration — it's the corrective force that resists
the LLM's helpful-incrementalist default.

---

## The 5-category refinement framework

When the skill applies a self-refinement pass on its own
recommendations (PROCEDURE Checkpoint 4), it asks all five
questions, not just "is there bloat?":

### 1. Drop bloat

- Oversized scope (recommendation covers more than it should)
- Premature abstraction (recommendation introduces a new concept
  not yet warranted)
- Duplicate concerns (two recommendations addressing the same
  underlying issue)

### 2. Add missing

- Under-scope (the review didn't reach a subsystem that should
  have been included)
- Missing recommendation type (e.g., review surfaced reasons to
  delete a concept entirely but recommendation only proposes
  refactor)
- Missing context that future-Claude or future-user will need

### 3. Reshape wrong-shape abstractions

- Right scope, wrong concept (the recommendation captures the
  right area but frames it in an awkward abstraction)
- Wrong bucket (Refactor when it should be Reshape, or vice
  versa)
- Wrong axis of recommendation (recommendation is about the
  implementation when the issue is conceptual, or vice versa)

### 4. Surface anchoring

- The whole review is anchored on a framing that itself needs
  challenge (e.g., "given the current 9 entity types, how do we
  improve them?" anchors on 9; greenfield might propose 7 or 12)
- The recommendations all stay within an existing decomposition
  even though greenfield would re-decompose

### 5. Reverse manufactured criticism / restraint

- **Manufactured criticism**: a recommendation flagged as Reshape
  whose justification reduces to abstract caution rather than
  specific evidence ("speculative API," "premature abstraction")
- **Manufactured restraint**: a Keep recommendation whose
  justification reduces to "won't matter for months" / "YAGNI" /
  "low cost so we can defer" without naming the specific cost
  being avoided by deferral

Both directions of false signal need active resistance. Apply
"why?" challenge to any recommendation whose reasoning feels
generic rather than specific to the case.

---

## What "manufactured" looks like

The signal: defense reduces to **principles** rather than
**specifics about this case**.

| Manufactured | Honest |
|---|---|
| "It's premature abstraction" | "Building this now requires X engineering hours; the consumer for it doesn't exist; the cost-benefit doesn't justify pre-building" |
| "We can defer this — it's YAGNI" | "Adding this now costs <specific>; deferring saves <specific>; the future cost of adding later is <bounded>; X > Y" |
| "Speculative API risk" | "Designing the API now without consumer X means we'll guess shape Y; if consumer Z arrives needing W, we'd have to rework. Cost of rework is <bounded>" |
| "Status-quo bias suggests..." | "If starting from scratch, we'd build <specific alternative>; the existing form differs in <specific ways>; the difference doesn't pay off because <specific reason>" |

Generic principles don't survive the "why for this case
specifically?" challenge. Specifics do.

This applies symmetrically:

- **Adding a recommendation**: defense should be specific value,
  not generic principle
- **Deferring a recommendation**: defense should be specific cost,
  not generic restraint

---

## When the user pushes back

In interactive mode, the user serves as the cross-check. Their
"why?" pushback is the corrective force for both manufactured
criticism and manufactured restraint. When they push back:

- Treat the pushback as a "why?" challenge — does the
  recommendation/deferral survive on case-specific grounds?
- If yes: defend with specific reasoning, not principle
- If no: revise or reverse

In autonomous mode (no user actively in loop), the absence of
external pushback is a known weakness. Document recommendations
extra-carefully so the eventual reviewer can apply the "why?"
challenge themselves.
