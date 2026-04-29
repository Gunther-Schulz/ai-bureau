# pbs-bureau vision

This document anchors the deepest "why" behind the architecture.
Every architectural decision in `ARCHITECTURE.md` and every
ROADMAP item traces back to one thesis. When in doubt about
whether a proposed feature belongs, check it against this
thesis first.

## The thesis

PBS is built on three interlocking principles. None alone is
sufficient; all three together define the design space:

1. **PBS is intertwined-AI-workflow, not tacked-on AI features.**
   The AI is a co-worker in the workflow itself, not a feature
   bolted onto an unchanged human workflow.

2. **The AI is a sparring partner, not an answer machine.** It
   challenges, generates counter-arguments, names uncertainty,
   resists giving easy answers — keeping the user critically
   engaged with the work.

3. **PBS produces output the user remains the author of.** Not
   teaching, not capacity-building in the abstract; preserving
   the user's role as the expert author who can defend, sign,
   and stand behind the produced work.

Three axes. Each must be served:

| Layer | Axis | Failure mode | PBS aim |
|---|---|---|---|
| Surface | Workflow embedding | Tacked-on: discrete AI features in unchanged workflow | Intertwined: AI as continuous co-worker |
| Process | Interaction mode | Answer machine: oracle / sycophant / easy answers | Sparring partner: challenger / interrogator / counter-argument |
| Purpose | Outcome orientation | Rubber-stamping: AI produces, human signs without engagement | Authorship preservation: user remains defensible expert author |

A system can fail on any axis independently:

- Tacked-on but well-designed sparring (a "find weaknesses"
  button) is still tacked-on (axis 1 failure).
- Intertwined but answer-machine (AI runs the office, human
  rubber-stamps) breaks axes 2 and 3.
- Intertwined sparring that produces work the user can't defend
  (no audit trail, opaque reasoning, no engagement with
  judgment calls) breaks axis 3.

PBS aims for all three: **intertwined sparring partnership in
service of defensible authorship.**

## Foundations

Vision documents need anchors. PBS draws on specific research and
thinking that future alignment checks should reference back to:

- **Vivienne Ming** (theoretical neuroscientist and cognitive
  scientist). Wall Street Journal article and book *Robot-Proof:
  When Machines Have All The Answers, Build Better People*. Her
  experiment on AI-human hybrid teams (three modes: oracle,
  validator, sparring partner) is the research basis for axis 2
  of the thesis. Her concept of the **Information-Exploration
  Paradox** (as the cost of information approaches zero, human
  exploration collapses) anchors why axes 2 and 3 matter
  operationally. Full treatment in "Sparring partner, not answer
  machine" section below.

When auditing for drift (per "How to use this document" below),
this foundation is the reference point: are we still doing what
Ming's research identified as the productive mode? Are we still
serving the concerns she names about capacity atrophy? PBS's
framing is its own (three axes; authorship preservation as the
third); the alignment with Ming is on axis 2 (sparring) and on
the underlying capacity-atrophy concern that motivates axis 3.
Axis 1 (intertwining) is our own framing, not derived from her
work.

Foundations grow as we engage with more research. Add new entries
here when external work becomes a reference for our own alignment
checks.

The contrast that makes axis 1 concrete:

| Tacked-on AI | Intertwined AI |
|---|---|
| Discrete features bolted onto existing tools | AI is a co-worker in the workflow itself |
| Transactional ("summarize this email") | Continuous ("what's pending; what's next; draft this section") |
| Workflow stays human-driven; AI offers convenience | Workflow is fundamentally collaborative |
| Trust is low; user checks every output | Trust is high; AI participates in real work output |
| No persistent state; each invocation fresh | Persistent state across sessions; AI remembers context |
| AI is an assistant on the side | AI is in the loop |

The "summarize this email" button is tacked-on. Most "AI agent"
demos in 2026 are still tacked-on. PBS aims for the deep end:
real intertwining where the AI is a participating colleague in
the actual production of B-Plan-Begründungen, Stellungnahmen,
Abwägungen — not a feature that helps you write them faster.

## What this means architecturally (intertwining requirements)

Intertwined AI is not "more AI" or "better AI." It has specific
architectural requirements that tacked-on doesn't need. The
minimum set:

- **Persistent state across sessions.** Project state, decisions,
  history, correspondence, sent versions. Without this, every
  session is fresh and the AI is back to "tool you invoke," not
  colleague you work with. PBS: per-project `_ai/state.md`,
  `decisions.md`, `correspondence-log.md`, `module-decisions.md`,
  bausteine memory, office-state under `paths.state_root`.

- **Orchestration as primary, not features as primary.** A
  continuous decision-making layer above individual tool calls.
  The orchestrator routes, surfaces decisions, holds context.
  Without it, AI fragments into disconnected feature invocations.
  PBS: the orchestrator skill + `PROCEDURE.md` checkpoints + the
  watch list.

- **Source-grounded outputs.** AI claims must be traceable;
  otherwise trust breaks and you fall back to "human checks
  everything" — which is tacked-on collapse in disguise. PBS:
  source-grounding guard (PROCEDURE.md Checkpoint 5),
  `verify-citations` skill, MCP tools as the canonical evidence
  source.

- **Audit trail.** What was decided, when, why, by whom.
  Necessary for trust-over-time and for tracing back when
  something later needs explanation (UNB asks "what changed
  between Vorentwurf and Entwurf for §X" — six months later).
  PBS: `decisions.md`, `snapshots/`, future unified audit trail
  (ROADMAP).

- **Continuous awareness of context.** What's pending, overdue,
  recently sent, due next; which projects are open; which
  Stellungnahmen need response. PBS: orchestrator session-open
  load, pending-actions, projects-index, watch list.

- **Explicit human-authority gates.** Points where the human
  makes the call, not the AI. This is PART of intertwining, not
  opposed to it: the gates ARE what makes the AI a colleague
  rather than a runaway agent. PBS: four-way decision menu,
  compile gate, send gate, layered review gate, state-transition
  gate.

**Future architectural choices can audit themselves against this
list.** Does the proposed feature serve persistent-state /
orchestration / source-grounding / audit / continuous-awareness /
human-authority — or is it a discrete convenience? If discrete,
ask whether it belongs.

## Trust as first-class infrastructure

Intertwined AI requires high human trust. You're letting the AI
draft a Begründung that goes to authorities, not just summarize
emails. The architecture EARNS that trust through specific
mechanisms:

- **Source-grounding** — every legal citation backed by a tool
  result, never invented from training memory. The model's recall
  of "BNatSchG zuletzt geändert durch Art. 1 vom 08.12.2022" is
  not evidence; the citation must come from a tool result.
- **Snapshots** — every send creates an immutable artifact bundle;
  what was sent is recoverable byte-for-byte for revision-request
  diffing later.
- **Send gate** — explicit user confirmation before any external
  transmission; AI never sends unilaterally.
- **Four-way decision menu** — capture / handle / backlog / drop;
  every memory-write or backlog-append corresponds to an explicit
  user decision.
- **Module-decision logging** — when AI includes/excludes optional
  sections, reasoning is captured in `module-decisions.md` for
  later review.
- **Lifecycle gates** — state transitions require explicit
  acknowledgment; no silent state advancement.

These are not process overhead. They are the trust infrastructure
that makes intertwining viable. Without them, intertwining
collapses — either back to tacked-on (low-trust, every output
checked) or forward into "AI runs the office" (false-trust,
undetectable drift). Both fail.

## Sparring partner, not answer machine

The second axis. Even an intertwined AI can fail badly if it
operates in answer-machine mode.

### The research

Theoretical neuroscientist and cognitive scientist **Vivienne Ming**
ran an experiment (reported in Wall Street Journal; expanded in her
book *Robot-Proof: When Machines Have All The Answers, Build Better
People*) testing human teams, AI teams, and human-AI hybrid teams
at predicting real-world events against prediction markets. Three
modes of hybrid interaction emerged, with starkly different
outcomes:

- **AI as oracle** (most hybrid teams): humans submitted AI's
  answer as their own. Human contribution: zero. Performance:
  same as AI alone.
- **AI as validator** (some hybrid teams): humans asked AI to
  support their preconceptions. Confirmation-bias loop;
  sycophancy. Performance: **worse than AI alone.**
- **AI as sparring partner** (5–10% of hybrid teams): humans
  pushed back, demanded evidence, interrogated assumptions. AI
  generated counter-arguments, surfaced doubts, resisted easy
  answers. Performance: rivaled or beat prediction markets —
  insights neither human nor AI alone could reach.

Only the third mode produces the value. The first two waste
the human partner — and the second actively degrades it.

### The deeper warning

Ming names the **Information-Exploration Paradox**: as the cost
of information approaches zero, human exploration collapses.
Students perform better on AI-assisted tasks, worse on
everything afterward. Developers ship more code, understand it
less. "We are slowly optimizing ourselves out of the loop."

The capacities AI is consuming are precisely the ones that
matter:

- Capacity to be wrong in public and stay curious
- Sitting with a question your phone could answer in three
  seconds
- Reading a confident, fluent AI response and asking "what's
  missing?" instead of defaulting to "great, that's done"
- Disagreeing with something that sounds authoritative and
  trusting your instinct enough to follow it

Most AI products are designed to deliver the answer before the
user feels the discomfort of not having one. PBS aims for the
opposite: deliver discomfort productively, in service of the
user's growing capacity.

### What this means architecturally (sparring requirements)

Sparring-partner mode has its own architectural requirements,
distinct from intertwining requirements:

- **Counter-argument as first-class output.** Every significant
  AI-generated argument or recommendation comes with the
  strongest case against it. User reviews both. Borrows Ming's
  specific recommendation: *"before you accept an AI's answer,
  ask it for the strongest argument against itself."*
- **Confidence calibration.** When AI is high-confidence, name
  it and explicitly invite challenge. When low-confidence, name
  uncertainty rather than hide it. Resist false-confidence
  sycophancy.
- **"What's missing?" as an explicit checkpoint.** Layered
  review currently asks "are required elements present?" The
  sparring extension also asks "what's absent that should be
  considered?" Different question, different mode.
- **Anti-sycophancy guard.** The orchestrator does not
  capitulate to user disagreement without reason. If a position
  is defensible, it defends. If user disagreement reveals a
  real flaw, it updates. But it does not soften because the
  user pushed back.
- **Selective friction calibration.** PBS is **frictionless
  except where you need to be.** Mechanical work — compile,
  format, citation lookup, scaffold, routine cross-references —
  is automated seamlessly. Friction is reserved for accountability
  moments (send, lifecycle transitions) and judgment moments
  (which argumentation type, scope changes, module decisions —
  places where the user's expertise must engage). The
  architectural question for any new feature: "is this mechanical
  or judgment-bearing?" Automate the first; surface the second.
- **Asymmetric knowledge respect.** Sparring is not between
  equals. AI's strength is **codified knowledge** — the legal
  corpus, prior projects, every captured baustein, statistical
  pattern recognition across the historical record. The user's
  strength is **tacit, current, causal** — this Bürgermeister's
  politics, the conversation in last week's Gemeinderat, the
  client's recent shift in priorities, the political moment.
  The gap is largely *temporal*: AI has historical depth, user
  has present awareness. The asymmetry is also *dynamic* — as
  bausteine accumulate and project state persists, AI gains
  depth in PBS-specific context; what stays user-only is the
  most-recent and the unrecorded.

  PBS surfaces the asymmetry **tentatively**: when the
  orchestrator proposes, it can name "here's what I'm drawing
  on; this might be a case where local/recent context I don't
  have should change the conclusion — does it?" Not deference
  ("you decide, I'm just suggesting") and not authority ("here's
  the answer") — a deliberate naming of which knowledge each
  party brings.

  *Asymmetric respect is not user-deference.* If the AI sees a
  structural issue, it pushes back even when the user has better
  local context. The asymmetry is about *what kind* of knowledge,
  not *whose* knowledge wins.
- **Commit to recommendations.** The orchestrator surfaces
  decisions as recommendation + tradeoff, not as open menu.
  Discussion emerges from the position taken; non-commitment
  turns interaction into permission-seeking and breaks sparring
  (you can't argue with a question; you can argue with a
  position). Already in PROCEDURE.md Checkpoint 13: "commit to
  a position the user can react to." The sparring framing
  elevates it from style note to architectural requirement.
- **Visible reasoning.** AI outputs come with reasoning, not
  just verdicts. The user can interrogate the reasoning, not
  just accept the conclusion.

### Why text-first matters here

Sparring is a text-shaped interaction. You can argue with text
— push back, demand evidence, ask follow-ups, sit with a
counter-argument. You cannot argue with a "summarize" button or
an autocomplete suggestion. The CLI's pure text I/O is the
most sparring-shaped surface possible.

Speech-to-text counts (text-equivalent). GUIs that funnel
through chat-shaped surfaces count. But GUIs that reduce
interaction to button-presses and form-fills break sparring —
they revert toward answer-machine mode by design. This is part
of the category-collapse risk in frontend integrations: a host
environment that doesn't support text-first discussion will
collapse PBS into a tacked-on feature regardless of architectural
intent.

## Authorship preservation, not rubber-stamping

The third axis. Even an intertwined AI in sparring mode can
fail if the produced output isn't something the user can
genuinely defend.

### What PBS is and isn't

PBS is **an output-producing tool for an expert practitioner.**
It is not a teaching tool. The user is already an expert
Begründungs-author with years of domain knowledge; PBS does
not exist to make them a better Begründungs-writer. It exists
to help them produce more Begründungen, more consistently,
with better citation hygiene, in less time.

But the produced Begründungen go out under the user's name.
They get signed, sent to authorities, defended in Stellungnahme
exchanges, debated in council meetings. The user is legally
and professionally accountable for everything PBS produces on
their behalf.

This creates the third axis: **PBS produces output; the user
remains the author.** Authorship in the professional/legal
sense — capable of defending the output, accountable for what's
signed, having engaged with the judgment calls. Capacity-
building in the abstract is a side effect when it happens;
authorship preservation is the actual purpose.

### The defensibility test

A sharp, operational test for whether the architecture is doing
its job:

> **Will the user be able to defend this output six months
> from now under UNB challenge, having forgotten the details?**

If yes — the user understood the judgment calls, the reasoning
is reconstructable, the audit trail captures the why — the
architecture works. If no — AI did the work, user signed; no
engagement, no defense — that's authorship collapse, regardless
of how good the output looked when shipped.

This test cuts through edge cases:

- A perfectly automated drafting feature that removes the
  user's engagement with §45 argumentation choice fails
  (user can't defend the choice later).
- A "skip review" shortcut that bypasses layered review fails.
- A summarization feature that compresses reasoning into pithy
  bullet points (losing the chain) fails (defense requires the
  full chain).
- A fully automated send pipeline (no user review of the cover
  mail) fails (the user owns the words sent under their name).

All might pass axes 1 and 2 (intertwined, sparring-friendly in
some sense). They fail axis 3.

### What authorship preservation requires

- **The user understands what they're signing** — visible
  reasoning, not black-box outputs. Layered review preserves
  this; rendering of the full reasoning chain at checkpoints
  reinforces it.
- **The user has engaged with judgment calls** — sparring
  surfaces them; selective friction makes the user pause at
  the right moments.
- **The user is the explicit decision-maker at gates** — four-
  way menu, send confirmations, lifecycle transitions are
  authored, not automatic.
- **The user can reconstruct *why* later** — audit trail (when
  it lands), `decisions.md`, `module-decisions.md`, snapshots
  all preserve the chain of reasoning for future challenge.
- **AI does the labor; user provides the judgment + the
  signature** — clear division. AI assembles, drafts, looks
  up, formats, cross-references. User chooses argumentation
  type, weighs alternatives, authorizes transitions, signs.

### Trust + sparring + authorship together

Three layers, three forms of protection:

- **Trust infrastructure** (axis 1 mechanisms): protects the
  user *from* the AI — no invented citations, no silent state
  changes, no unauthorized sends.
- **Sparring infrastructure** (axis 2): protects the user
  *from comfortable but degrading interaction patterns* — no
  oracle worship, no sycophancy loop, no easy answers
  everywhere.
- **Authorship preservation** (axis 3): protects the user's
  *professional/legal standing* in everything PBS produces on
  their behalf — no rubber-stamping, no signature without
  engagement, no work the user can't defend.

A system with full trust + sparring but weak authorship
preservation produces accurate, well-reasoned drafts the user
signs without understanding — works until challenged. A system
with full authorship preservation but weak trust or sparring
is engaged but unreliable — the user defends bad output well.
PBS aims for all three, in service of work that is **correct,
defensible, and genuinely the user's.**

## Implications and open questions

Downstream of the thesis. Surfaced here so future sessions have
handles, not buried in implicit assumptions.

### Workflow as precondition

Intertwined AI needs a workflow to intertwine with. Domains with
rich, structured workflows (planning, law, engineering, healthcare,
accounting) are natural fits — there's a real pattern of work to
embed in. Generic "knowledge work" without explicit workflow is
much harder; nothing concrete to intertwine with.

Implication for the consulting / second-deployment story: the
first question to a prospect is not "do you want AI?" — it's
"what's your workflow?" If the answer is fuzzy, the engagement
is workflow-definition first, AI integration second. Selling
PBS-style intertwining to a company without a defined workflow
sells nothing.

### Office as multi-human + AI eventually

PBS today is effectively single-user (Gunther; Hendrik as
sibling-practice with read-only crossing). The "office" concept
implies team + AI: multiple humans plus AI participating in
shared workflow. This introduces architectural axes not yet
addressed in v1:

- Multi-user state (whose decisions? whose authorizations?)
- Concurrent collaboration (two humans + AI editing simultaneously?)
- Shared memory (bausteine across team members; whose
  successful_uses[] entries?)
- Conflict resolution (when humans in the same office disagree,
  what does the AI do?)

Significant for the SaaS angle and for PBS itself once Hendrik
becomes a full participant. v2+ axis; not addressed in v1
deliberately.

### The transition path for adopters

Companies don't jump from no-AI to intertwined-AI. The typical
path: no-AI → tacked-on AI → realize tacked-on's limits → move
toward intertwined. Most prospects in 2026 are at no-AI or
tacked-on stage.

Implication: PBS as an adoption story has to bridge prospects
at the tacked-on stage. The patterns and methodology
(transferable IP — meta-rules, entity types, intertwining
requirements above) matter as much as the code (cloneable
artifact). The consulting angle is the natural fit for early-
stage prospects; clone-and-deploy is harder until prospects have
caught up to the intertwined model.

### Frontend determines accessibility

CLI works for power users (Gunther). Intertwined AI accessible
ONLY via CLI is locked to power users. Native GUI / web frontends
are not just ergonomic conveniences — they are how intertwining
becomes available to non-technical colleagues. As the AI-augmented
workforce grows, this gap matters more.

Increases the weight of the multi-frontend story (web UI on
ROADMAP; future Anthropic-native-app or other GUI-client
integrations). Architectural foundation is in place: meta-rule
5's `pbs_core` / `pbs_mcp` discipline + the deferred-but-designed
physical split for the web UI explicitly anticipates multiple
frontends over the same engine.

### The category-collapse risk

The biggest risk to the thesis is **category collapse**: PBS
gradually reduced to a "tacked-on" feature catalog because each
discrete addition seemed reasonable in isolation. Especially at
risk: GUI integrations into hosts (Anthropic-native-app,
third-party workspaces) where the host's UX paradigm is
feature-driven. Each integration must be checked: does it expose
intertwined workflow, or does it reduce PBS to a "summarize this"
plugin in someone else's tool? The first is a frontend; the
second is category collapse.

## PBS as pioneer instance

All deployment possibilities below depend on a deeper purpose.
PBS is **a pioneer instance of a category that doesn't yet
exist mature in the market**: intertwined-AI-workflow +
sparring-partner + authorship-preservation as integrated
pattern in expert-practitioner work. The transferable IP is
the architecture (meta-rules, trust mechanisms, three axes,
scope orthogonality, MCP discipline); PBS-specific code is
incidental.

"Pioneer instance" is more accurate than "proving ground." A
proving ground validates an existing thesis. PBS is doing more
— *co-discovering* the architectural patterns through the work
itself. The patterns don't pre-exist waiting to be proven; they
emerge as the construction proceeds. The five-month design
pass that produced this vision document, the meta-rules, the
three-axis framing — that wasn't preparation for the work. It
was the work.

### Triple purpose, all simultaneous

- **Working tool** for the practitioner's actual planning bureau
  work. Precondition; without it, nothing real is being
  validated. PBS must serve Gunther's daily output, or the
  pioneer claim is empty.
- **Proving ground** for the architectural patterns. Deliberate
  IP capture; the meta-rules and decision rules are designed
  to be transferable to other expert-practitioner domains.
  What works for German planning bureau work should generalize
  to legal, medical, engineering, accounting, etc. with domain
  swap-out.
- **Research lab** for discovering what AI-augmented expert
  work can be. Construction-as-research: the architectural
  discussions ARE the work, not preparation for it. We're not
  proving a known architecture; we're co-discovering one.
  This third purpose justifies the architectural depth even
  before real-project density accumulates.

### Implicit hierarchy among deployment possibilities

Under the pioneer-instance framing, the three deployment
possibilities below are not parallel — they form a sequence
with implicit ranking:

1. **Production + consulting** (primary). Pattern transfer is
   the natural realization of pioneer IP. Other companies
   adopt the architecture (with domain swap-out); PBS as
   reference deployment + Gunther as consultant.
2. **Sell to other Planungsbüros** (secondary). Productizing
   creates tension with pioneering — products are rigid,
   optimized for adoption rather than discovery. Possible
   later, after patterns stabilize. Not a near-term goal.
3. **SaaS / multi-frontend** (distant). Fully productized; the
   pioneer phase is over by then. Years out, not months.

Optimizing too early for productization (possibilities 2 or 3)
sacrifices pioneer-instance value. Stay in pioneer mode until
the patterns are mature enough to bear product weight.

### The honest risks of one-user pioneering

A pioneer instance with one user generates thin validation:

- **Survivorship bias** — what works for Gunther might not
  generalize.
- **Architectural over-fitting** — optimized for one
  practitioner's specific style.
- **Low evidence sample** — few real-world tests to validate
  patterns against.
- **Confirmation bias** — the user also designed the
  architecture; testing his own hypotheses.

The triple-purpose framing partially addresses these (the
research-lab role accepts that discovery, not just proof, is
happening). But the risks are real and shouldn't be hand-
waved. Validation strategy must acknowledge them and find ways
to compensate — synthetic projects with expert review,
historical-project replay, comparison with documented
professional standards, etc. **The validation evidence types
that count for a pioneer instance with sparse real-world tests
are different from what counts for a productized tool with
many users.** This is an open work area, not a solved problem.

### Milestones (not a terminal state)

There's no "proven" terminal state. Patterns evolve as the
field matures. But there are milestones worth naming:

- First month of fully-operational intertwined workflow.
- First real-project test where source-grounding catches an
  error.
- First counter-argument from sparring that prevents a real
  misstep.
- First successful Stellungnahme defense traceable to
  authorship-preservation infrastructure.
- First cross-deployment of patterns to another domain
  (consulting engagement; second deployment) — the manual,
  hand-built path.
- First office *generated by an AI-office builder* rather than
  hand-built. The architectural endpoint of pioneer-instance
  framing: the patterns mature enough that the builder
  scaffolds new domain offices from a domain spec + the
  accumulated patterns. PBS is the pioneer instance; the
  builder is what the pioneering produces. See `ROADMAP.md`
  v2 "AI-office builder" entry for the long-arc vision and
  staged validation triggers.

These are the *evidence types* the pioneer instance generates
over time. They accumulate as the system runs. None requires
PBS to be "done."

### The pioneer-instance commitment as architectural discipline

Pioneer-instance framing isn't a marketing label; it's a working
discipline that constrains every architectural decision in this
repo. Captured formally in `ARCHITECTURE.md` "Pattern-vs-instance
discipline": every commitment must work at pattern level (not
just for PBS), tested against 3-5 hypothetical-domain thought
experiments. The pattern is the IP; PBS is the proving instance.

Validation under the single-domain-pioneer constraint
(`ARCHITECTURE.md` extends this): the user is a planning-domain
expert and won't authentically build offices in other domains.
"Build 2-3 hand-instances and measure overlap" is the textbook
validation path but wrong for this constraint. Working method
is **best-effort split via careful reasoning + PBS-regression
validation** (signal #1, immediately checkable) + **second-
domain validation when/if a real natural trigger arises**
(signal #2, deferred and possibly indefinite). Pre-RAG ROADMAP
commitment #9 is the immediate concrete realization.

## Three deployment possibilities

Realistic futures for PBS as a pioneer instance of the
intertwined-AI-workflow vision. All three reinforce the
architecture as built; none demand stripping it back. Hierarchy
under the pioneer framing is named above (production +
consulting primary; selling secondary; SaaS distant).

1. **Real production + testing/validation ground for consulting.**
   PBS runs as Gunther Schulz's actual planning bureau AND serves
   as the proving ground for "AI office" patterns transferable
   to other companies. The patterns themselves (meta-rules,
   entity types, scope orthogonality, app/office split,
   `pbs_core`/`pbs_mcp` discipline, intertwining requirements
   above) are the IP; PBS-specific code is incidental.

2. **Sell the app to other Planungsbüros** (or consult them to
   build their own stack). The layered scope
   (`scope.domains: [PV-FFA, Wind, Naturschutz]`) was designed
   for this. A narrower-scope office picks fewer domains; a
   broader one picks more. Other Planungsbüros adopt directly;
   the orthogonality refactor IS this product feature.

3. **SaaS / multi-frontend.** Eventually PBS-Office-style
   intertwining becomes available beyond CLI. Web UI,
   Anthropic-native-app integration, future SaaS frontend — all
   surfaces over the same `pbs_core` engine. The
   `pbs_core`/`pbs_mcp` discipline + the "physical split deferred
   until web UI lands" architecture explicitly anticipates this.

These are not exclusive — possibility 1 generates IP that
informs possibilities 2 and 3; possibility 2's deployments
become use cases for possibility 3's hosted version.

## How to use this document

Three checklists, one per axis:

**Axis 1 — Workflow embedding (intertwining):**

- Does the proposed feature serve persistent-state /
  orchestration / source-grounding / audit / continuous-
  awareness / human-authority? If discrete and disconnected,
  ask whether it belongs.

**Axis 2 — Interaction mode (sparring):**

- Does the proposed feature support counter-argument /
  confidence calibration / "what's missing?" checkpoints /
  selective friction / asymmetric knowledge respect /
  commit-to-recommendations / visible reasoning? Or does it
  deliver easy answers, suppress uncertainty, automate
  engagement away?

**Axis 3 — Authorship preservation (defensibility):**

- Will the user be able to defend the output six months from
  now under challenge, having forgotten the details? Does the
  feature preserve the user's role as expert author, or edge
  them toward rubber-stamping?

**For frontend integrations:**

- Axis 1 check: does it expose intertwined workflow, or reduce
  PBS to a tacked-on feature in someone else's tool?
- Axis 2 check: does the frontend support text-first discussion,
  or funnel through buttons that break sparring?
- Axis 3 check: does the frontend preserve the user's visible
  engagement with judgment calls, or hide them behind UX
  convenience?

**For drift audits:**

- Has any recent addition collapsed PBS toward "AI feature
  catalog" (axis 1 drift)?
- Has any recent addition collapsed PBS toward "answer machine"
  (axis 2 drift)?
- Has any recent addition collapsed PBS toward "rubber-stamp
  signing" (axis 3 drift)?

This is the deepest anchor. ARCHITECTURE.md describes how the
system is structured; this document describes why and against
what failure modes.
