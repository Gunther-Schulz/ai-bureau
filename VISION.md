# pbs-bureau vision

This document anchors the deepest "why" behind the architecture.
Every architectural decision in `ARCHITECTURE.md` and every
ROADMAP item traces back to one thesis. When in doubt about
whether a proposed feature belongs, check it against this
thesis first.

## The thesis

**PBS is intertwined-AI-workflow, not tacked-on AI features.**

The contrast that makes this concrete:

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

## Three deployment possibilities

Realistic futures for PBS as an instance of the intertwined-AI-
workflow vision. All three reinforce the architecture as built;
none demand stripping it back.

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

- **Before adding any new feature**: check it against the
  intertwining requirements list. Does it serve persistent-state /
  orchestration / source-grounding / audit / continuous-awareness /
  human-authority? If not, ask whether it belongs.
- **Before adopting a frontend integration**: check whether it
  exposes intertwined workflow or reduces PBS to a tacked-on
  feature in someone else's tool. The first is a frontend; the
  second is category collapse.
- **When making architectural decisions**: trace back to this
  thesis. The architecture is sound when it serves intertwining;
  over-engineered when it adds layers that don't.
- **When auditing for drift**: check that recent changes still
  serve the thesis. Subtle shifts toward "AI feature catalog"
  are the drift to watch for.

This is the deepest anchor. ARCHITECTURE.md describes how the
system is structured; this document describes why.
