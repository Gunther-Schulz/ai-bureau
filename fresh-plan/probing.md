# fresh-plan probing discipline (adversarial stress-testing)

Working-process disciplines aimed at AI's structural failure modes — specifically, what AI doesn't naturally notice. The forward-motion bias that produced the slot-interpretation gaps (surfaced by the activation-scope finding and the 24-suspect audit it triggered) is the canonical motivating instance.

This file lives parallel to `README.md` because that file describes how work proceeds; this one describes how work gets stress-tested against itself. Not loaded by default at session-start — consult on demand when running a probe, writing a substantive D-entry, or running a phase-boundary audit. README's "Working patterns" cross-references this file.

## Why this exists

AI assistants are pattern-completion engines that excel at "do this task" and are systematically bad at "notice what's NOT in the frame." A framework's quality depends on noticing exactly that. Without engineered probing, the framework's quality reduces to "how often does the user ask sharp out-of-frame questions on a given day" — a fragile dependency.

The discipline is small on purpose. It is itself subject to the failure modes it targets (procedures can ossify or miss categories) and is meant to evolve via observation across sessions, not via comprehensive up-front design.

## Failure modes this discipline targets

- **Frame-acceptance** — AI executes the task as given; doesn't ask "what does this task not ask?"
- **Local-over-global** — each decision well-formed in its own scope; cross-cutting integration questions live nowhere.
- **Forward-motion bias** — AI prefers landing the next thing over stress-testing the previous thing.
- **Pattern-completion over pattern-questioning** — AI sees a precedent (D17 → D43 supersedes-by-rename) and mirrors the pattern in the next case without asking "does the precedent's reasoning genuinely apply here?"
- **No-failure-mode imagination** — AI builds for the happy path; doesn't naturally enumerate unhappy paths.
- **Authority-deference** — AI honors what's locked rather than probing whether the lock was right.
- **Recency-bias** — AI weights recent conversation context heavily; older corpus content fades from active probing range even when load-bearing.

The discipline doesn't claim to address every failure mode (some require routine outside-reader cadence beyond AI dispatch). It addresses the load-bearing ones with bounded mechanisms.

---

## Procedure 1 — Decision-shape template (mandatory for substantive D-entries)

Every substantive D-entry must carry answers to a fixed set of framing questions. Clarification / supersedes entries that touch only one slot may answer proportionally (the WHO + FAILS questions for that slot only). Absence of an answer means the entry can't lock; "TBD" or "deferred" is a valid answer if the deferral target is named.

The framing fields (named in the entry text, not necessarily as separate sections):

- **WHAT** — what this decision establishes. Already implicit in current entries; surface explicitly if not obvious from the title + opening paragraph.
- **WHO** — who interprets / consumes / enforces this, and at which layer. Choose from:
  - `framework-validator (B1)` — checked at boot or per-event by the conformance validator
  - `substrate (runtime)` — interpreted by the substrate at append / dispatch time
  - `shape (policy)` — interpreted by shape policy hooks or authority-bindings
  - `specialist (impl)` — interpreted by individual specialist runtime
  - `extension (registered)` — interpreted by the registering extension
  - `opaque (documentary)` — not consumed at runtime; serves as documentation / metadata for downstream tools / auditors
  - `deferred (named target phase)` — interpretation explicitly deferred to a future phase; the target phase MUST be named
  - Multi-layer answers acceptable when the decision genuinely spans (e.g., "shape declares; substrate enforces at append").
- **FAILS** — what happens when the decision's subject is malformed, missing, or contradictory. Where the failure surfaces. What error the user sees. What recovery path exists. ("Should never happen" without alerting / logging is not a failure mode answer.)
- **CROSS** — what other decisions this cross-cuts. The existing `**Cross-references**:` line names related entries; the CROSS field forces the author to name *which slots in those decisions* this entry interacts with.
- **DEFERS** — what this entry deliberately doesn't decide, and where it gets decided (which phase, which future entry). Composes with the existing `### What is NOT in this decision` section in substantive entries.

**Targets**: frame-acceptance + local-over-global + no-failure-mode + (partially) authority-deference. The WHO field specifically catches the activation-scope class.

**Risk**: becomes box-checking. Mitigation: pre-lock probe (Procedure 3 below) when invoked tests whether the answers are real.

---

## Procedure 2 — Structured audit (mandatory at multiple checkpoints — see Checkpoint cadence)

A menu of audit shapes — multiple probes, each a different question shape. Each probe runs in fresh context (sub-agent dispatch with adversarial brief). Outputs feed the relevant refinement entry (Bref-shape at phase-boundary; per-workstream commit notes at workstream-completion; etc.) as findings to fix or defer-with-named-home.

This procedure defines WHAT probes exist (the menu below). The "Checkpoint cadence" section after Procedure 5 defines WHEN they fire (workstream-completion / pre-refinement-pass / phase-boundary / pre-phase-transition).

The menu accumulates over time as new probe shapes prove valuable.

The current audit menu:

- **Slot-interpretation audit** — for each slot in each kind, is the WHO layer named in the contract entry or the schema? Suspects: slots where the layer is implicit, ambiguous, or where the impl never reads what the spec claims it should. Canonical instance: the audit run during Bref that produced the 24-suspect list.
- **Failure-mode coverage audit** — for each significant decision, is the failure path named? What happens when X is malformed / missing / contradictory? Are failures user-visible or buried in logs?
- **Abandonment-path audit** — when a process fails mid-cascade (event rejected, dispatch loop terminated by backstop, B1 validation failure mid-boot), what state is left? Is recovery defined?
- **Cross-decision coherence audit** — do entries that cross-reference each other actually preserve what they claim? E.g., D44 asserts it preserves D10 + D39 + D40 §A — does the impl + corpus actually verify that?
- **Pattern-imposition audit** — for entries that follow a structural precedent (supersedes-shaped, kind-contract-shaped, refinement-shaped), examine whether the precedent's logic genuinely fit each case or whether the pattern was applied because-it-was-the-pattern. Catches cases where consistency-of-shape silently imposed constraints that shouldn't apply.
- **"What's not a kind" audit** — what mechanisms have we absorbed into existing kinds that would benefit from being decomposed differently? D8 (no `discipline` kind) and D38 (no `knowledge` kind) are precedents; what other absorptions are silently load-bearing?

Adding new audit shapes to the menu is itself a discipline-evolution moment (see "Evolution" below).

**Targets**: forward-motion bias (forces structural stop) + frame-acceptance (multiple probes from different angles) + recency-bias (fresh-context dispatch reads cold) + pattern-completion (pattern-imposition audit specifically).

---

## Procedure 3 — Pre-lock adversarial probe (invoked when warranted)

Before locking a Tier-3 substantive D-entry (new kind, new contract, major mechanism, scope-defining roadmap, end-of-phase closure), dispatch a sub-agent with one rotating brief from the menu. Probe runs ~5-10 min and returns a "find me reasons not to lock" report.

Brief menu (rotates across instances; pick the brief that fires hardest for the entry's content):

- **What does this entry not name that it should?** — slot-interpretation flavor; catches missing WHO / FAILS / CROSS answers.
- **What other entries does this contradict or strain?** — cross-decision coherence flavor; catches conflicts the author didn't notice.
- **What's the failure path?** — failure-mode flavor; catches happy-path-only thinking.
- **What would a hostile reader misinterpret?** — frame-acceptance flavor; catches assumptions the entry treats as obvious.
- **What assumption is this entry quietly making?** — frame-acceptance flavor; surfaces unspoken premises.
- **What precedent is this entry mirroring? Does the precedent's reasoning actually apply here, or is the pattern being imposed?** — pattern-completion flavor; specifically catches cases where the author defaulted to a precedent's resolution shape without stress-testing fit.

Fires when the entry is genuinely substantive. NOT for clarification entries or mechanical refactors — those are bounded enough that the decision-shape template alone suffices.

**Targets**: authority-deference (separates writer from prober) + pattern-completion + frame-acceptance.

---

## Procedure 4 — Mid-cycle exploratory dispatch (cadence-driven)

Once per ~10 sessions or ~10 substantive D-entries (whichever comes first), dispatch a fresh-context sub-agent with a *pure exploration brief* — no specific question, just "read this corpus cold, tell me what doesn't add up." Compensates for categories of question we haven't learned to ask yet.

The brief shape:

> Read fresh-plan/README.md, CONCEPTS.md, decisions.md, and the schemas/ directory cold. You're a fresh reader with no prior context. Tell me: (a) what claims feel unsupported, (b) what cross-cutting commitments seem unverified, (c) what's named ambiguously, (d) what you'd ask the authors to clarify before relying on this corpus. Don't fix anything; report findings only.

**Targets**: blind-spot-sharing limit of single-author work + recency-bias + the meta-blindness category ("we don't know what we don't know to ask").

---

## Procedure 5 — Cross-decision artifact probe (invoked when warranted)

When a workspace manifest, event sequence, worked example, or other cross-cutting artifact is introduced or modified, verify it against multiple decisions simultaneously rather than testing per-decision. Catches local-over-global gaps that per-decision review misses.

Invoke when:
- Introducing a new cross-cutting artifact (e.g., a worked example demonstrating how a Phase D shape composes)
- Audits surface coherence concerns
- A decision claims to preserve / extend multiple prior decisions (e.g., "extends D10 + D39 + D40 §A" — verify against all three on a concrete artifact)

Mechanism: dispatch a sub-agent with the artifact + the relevant decisions, brief is "verify this artifact against all of these decisions; report any inconsistencies or unverified claims."

**Targets**: local-over-global + cross-decision coherence drift.

---

## Checkpoint cadence — when probes fire

Procedures 1-5 above define WHAT probes exist. This section defines WHEN they fire. The same probe shape can fire at multiple checkpoints with different scope (e.g., the slot-interpretation audit fires at workstream-completion scoped to the workstream, AND at phase-boundary scoped to the full phase).

Checkpoints accumulate as new ones prove valuable. Per the discipline's evolution rule below, retire checkpoints that produce no findings across 3+ instances.

### Checkpoint catalog

| Checkpoint | When | Probes invoked | Scope |
|---|---|---|---|
| **Substantive D-entry lock** | Every substantive D-entry author moment | Procedure 1 (decision-shape template, mandatory) + Procedure 3 (pre-lock probe, when warranted for Tier-3) | Per-entry |
| **Workstream completion** | After each named workstream lands (B1, B2, B2b, ..., B8 in Phase B; equivalents in other phases). Tracked in `roadmap.md`. | Procedure 2 audit menu — minimum slot-interpretation + failure-mode coverage | Scoped to workstream's added content (lighter than phase-boundary) |
| **Pre-refinement-pass start** | At the START of a named refinement workstream (Bref, future Cref, etc.) — before processing the tracked deliverables list begins | Procedure 2 audit menu, adapted brief: "What's NOT on the tracked deliverables list that should be?" | Scoped to refinement-pass scope-setting |
| **Phase boundary (closure)** | End of each phase (Phase A closed at D35; Phase B closure pending) | Procedure 2 audit menu — full menu, multiple shapes rotated | Full phase corpus |
| **Pre-phase-transition** | Before starting the next phase (especially pre-Phase-D where deferred items concentrate) | Procedure 2 audit menu, adapted brief: "What deferred items come due now? What cross-phase coherence isn't verified?" | Cross-phase deferral inventory + dependency check |
| **Mid-cycle exploratory** | ~Every 10 sessions or 10 substantive D-entries | Procedure 4 (mid-cycle exploratory dispatch) | Pure exploration; no specific question |
| **Cross-cutting artifact change** | When introducing / modifying a cross-cutting artifact (workspace manifest, event sequence, worked example) | Procedure 5 (cross-decision artifact probe) | Per-artifact |

### Why these specific checkpoints

- **Substantive D-entry lock + Workstream completion** catch issues at write-time when the author's context is fresh and the scope is bounded. Cheaper than discovering the same issues at phase-boundary when the audit scope has ballooned across multiple workstreams.
- **Pre-refinement-pass start** is the checkpoint that would have caught the slot-interpretation discipline gap BEFORE Bref deliverables 1-3 had landed. Refinement passes process tracked deliverables; a probe BEFORE the pass starts asks "what should be ON the tracked list that isn't?" Different question shape from the audit menu's per-decision probes.
- **Phase boundary** is the catch-all: full audit menu with multiple shapes rotated. Catches what slipped through earlier checkpoints + what's only visible across multiple workstreams.
- **Pre-phase-transition** matters because phases name "deferred to Phase X" items as they go. At the transition moment, those deferrals come due simultaneously. A probe surfaces the deferral inventory + checks coherence across them. Especially load-bearing pre-Phase-D where pioneer-instance touches every layer.
- **Mid-cycle exploratory** is the time-based safety net for what the structured probes don't ask about.
- **Cross-cutting artifact change** catches local-over-global gaps that per-decision review misses.

### Scope notes

- **Workstream-completion probes are deliberately lighter** than phase-boundary (~5-10 min sub-agent dispatch vs ~30 min full-phase audit). The point is to catch workstream-local issues before they compound, not to re-audit the whole corpus on every workstream landing.
- **Pre-refinement-pass scope is the deliverables-list itself**, not the corpus. The probe asks whether the list captures the right scope, not whether each item is well-formed.
- **Pre-phase-transition scope is deferred items + cross-phase dependencies**, not a re-audit of the just-closed phase (that already ran at the phase boundary).

## Ownership

- **Sub-agent dispatch is the default executor** for all probe shapes. Brief includes the scope (workstream / phase / artifact) and the brief variant (pure exploration / specific question).
- **The change-author triggers** workstream-completion + cross-cutting artifact change checkpoints (these are bounded enough that the author owns initiating).
- **The session managing a refinement-pass / phase-closure entry triggers** pre-refinement-pass / phase-boundary / pre-phase-transition checkpoints.
- **Mid-cycle exploratory** is discretionary; tracked by counting sessions / substantive entries since last run.
- **Outside human readers (eventual)** augment but don't replace sub-agent dispatch. Sub-agents share some AI failure modes; outside readers don't, but cost more and aren't always available.

---

## Evolution (meta-discipline)

This procedure framework is itself subject to the failure modes it targets. To prevent ossification:

- **Add new audit shapes** to the phase-boundary menu when a probe-shape proves valuable across multiple instances. Don't add speculatively.
- **Add new probe briefs** to the pre-lock menu when a new failure-mode category surfaces and existing briefs don't catch it.
- **Retire procedures** that produce no findings across 3+ instances (likely calibrated for a problem that no longer exists or a problem we never had).
- **Audit the procedures themselves** at every other phase-boundary audit (alternating: even phases audit corpus, odd phases audit procedures + corpus).
- **Distinguish "discipline drift" from "discipline retirement"** — drift = forgot to do it; retirement = explicit decision it's not earning its keep. Drift is bad; retirement after evidence is fine.

The discipline framework is meant to grow with the corpus, not be locked exhaustively up front. New procedures get proposed when failure modes surface that current procedures didn't catch. Existing procedures get sharpened when the answers they produce stop being meaningful.

## Acknowledged limits

Worth being honest about what this discipline does and doesn't do:

- **Does**: catches missing-from-list items at named checkpoints; forces stop-and-test against forward-motion bias; separates writer-from-prober for authority-deference; rotates question shape against frame-acceptance and pattern-completion.
- **Doesn't**: catch categories of question we haven't learned to ask (still requires user / outside readers to surface those organically); guarantee the discipline is honored (depends on session-start-procedure compliance and on the authoring session not skipping); replace genuine outside-reader review (sub-agents share AI failure modes; cheaper-than-outside-readers approximation only).
- **The deeper fix** beyond this discipline: routine outside-reader cadence (real human readers reading at named milestones). Most expensive; most effective. Not always available; cadence-named when it becomes available.

The discipline is a foundation, not a solution. Foundation = something to build on; doesn't claim to be sufficient.
