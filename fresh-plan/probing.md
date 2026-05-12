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
- **Investigation-bias / claim-without-evidence** — AI states facts about existing code, state, or documents without Reading or Citing source. Pattern-completion produces plausible-looking claims (e.g., "the function probably accepts `*args/**kwargs`" because that's the most common variadic pattern) that masquerade as verified. Distinct from pattern-completion (which is structural prediction); this is direct factual confabulation about specific entities. Targeted by the investigation-before-claim discipline immediately below.

The discipline doesn't claim to address every failure mode (some require routine outside-reader cadence beyond AI dispatch). It addresses the load-bearing ones with bounded mechanisms.

---

## Investigation-before-claim discipline (load-bearing for D-entry drafting)

Per global CLAUDE.md Cite-or-Read-or-Flag — **every claim a D-entry makes about existing impl** (function signatures, code-path behavior, line-level details, runtime sequencing, schema content, state at specific moments) MUST be backed by one of:

- **Cite**: the cited code was Read in current session; entry cites specific file:line or symbol name
- **Read**: read the cited code NOW (before drafting that section), then assert
- **Flag**: explicitly tag the claim as "inferred from adjacent signal X — not verified by reading source" — and prefer Read over Flag for load-bearing claims (those driving impl follow-through OR locking new contract)

**Pattern-completion masquerading as fact is the failure mode this discipline targets specifically.** AI's tendency to confabulate plausible-looking claims about code (because variadic `*args/**kwargs` is the "most common" pattern, etc.) produces D-entries that look authoritative but contain factual errors. **Drafting from pattern-recall is not Read or Cite; it's an unflagged inference.**

Canonical motivating instance: D47 §B.3 originally claimed `HookRegistry.fire(name, *args, **kwargs)` without reading `hooks.py` first; the actual API is `fire(name, context: dict)`. Caught at impl-planning time before commit; would have shipped a wrong contract into the ledger if not caught. This was the SAME pattern as the activation-scope finding (load-bearing claim made without verification) but at the D-entry-drafting layer rather than the slot-interpretation layer.

**Procedural enforcement** (composes with Procedures 1, 3 below):
- Procedure 1 (decision-shape template) FAILS / WHO / CROSS fields: any claim about impl behavior MUST be Read-or-Cite-backed at draft time.
- Procedure 3 (pre-lock probe) brief menu includes "what code claims are unverified?" — fires before lock to catch any inferred-but-not-flagged claims.
- Procedure 3 (refined audit-driven-skip): when an entry establishes NEW contract content (not pure audit cleanup), the pre-lock probe MUST fire even when audit-driven. The audit motivates the gap; the entry's resolution may include new claims that need verification.

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
- **FAILS** — what happens when the decision's subject is malformed, missing, or contradictory. Where the failure surfaces. What error the user sees. What recovery path exists. ("Should never happen" without alerting / logging is not a failure mode answer.) **Pattern (per D44 precedent)**: every runtime decision should have a **detection + surface + recovery** triad explicitly named — named exception type, user-visible diagnostic, recovery path. The 2026-05-12 failure-mode audit found D44 was the *only* runtime decision that honored this; every other decision (D7, D9, D10, D12, D13, D16, D19, D20, D29, D30, D32, D34, D37, D39, D40 §A) lacked it. **Citing "Failure-modes-are-first-class" as rationale ≠ applying it as a check.** Pre-lock probe (Procedure 3) should test whether the answer is real, not just present. **Code-claim verification (per investigation-before-claim discipline above)**: any FAILS claim about how impl behaves under failure (which exception type raises, what state survives, what diagnostic surfaces) MUST be Read-or-Cite-backed at draft time. Pattern-completed claims (e.g., "the function probably raises XError") are unflagged inferences and violate the discipline.
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
- **Detection-surface-recovery audit** — sharper version of failure-mode coverage, specifically checking for the D44 triad (named exception type / user-visible diagnostic / recovery path) on every runtime decision. The 2026-05-12 audit established D44 as the precedent — this audit shape generalizes it as a standing check.
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
- **What code claims does this entry make? List each. For each: was the cited code Read in this session, OR is the claim inferred? Verify any inferred claim against actual code now.** — investigation-bias flavor; specifically catches the pattern-completion-masquerading-as-fact case (D47 §B.3 unverified `HookRegistry.fire` signature is the canonical motivating instance).

**Audit-driven-skip refinement**: D45 §E established the precedent that pre-lock probe can be SKIPPED for entries grounded in fresh-context audit findings (re-probing is circular — the audit motivated the entry; the entry codifies the audit's recommendation). D46 followed it cleanly (pure typed-exception application). D47 followed it but introduced new contract content (hook firing integration sites — the audit said "fire is never called", not "here's how fire should work") and slipped two unverified claims past lock-time. **Refined skip rule**: skip applies to entries that are PURE pattern application (typed-exception application of an existing pattern). Entries that establish NEW contract content not in the audit's findings MUST run pre-lock probe even when audit-driven, with the brief specifically targeting the new content (especially the code-claim-verification brief above).

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
| **Workstream completion** | After each named workstream lands (B1, B2, B2b, ..., B8 in Phase B; equivalents in other phases). Tracked in `roadmap.md`. | Procedure 2 audit menu — STANDING minimum: slot-interpretation + failure-mode coverage + abandonment-path (per 2026-05-12 audit findings — these three are systemic categories, not rotating choices) | Scoped to workstream's added content (lighter than phase-boundary) |
| **Pre-refinement-pass start** | At the START of a named refinement workstream (Bref, future Cref, etc.) — before processing the tracked deliverables list begins | Procedure 2 audit menu, adapted brief: "What's NOT on the tracked deliverables list that should be?" | Scoped to refinement-pass scope-setting |
| **Phase boundary (closure)** | End of each phase (Phase A closed at D35; Phase B closure pending) | Procedure 2 audit menu — ALL audit shapes (full menu, not rotating); the standing minimum from workstream-completion plus pattern-imposition + cross-decision coherence + "what's not a kind" + detection-surface-recovery | Full phase corpus |
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
- **Track audit findings count over time** at each checkpoint. Audit shapes producing *increasing* findings over successive instances suggest the underlying discipline gap is not closing — escalate priority of addressing the discipline pattern (not just the surfaced suspects). Audit shapes producing *decreasing* findings suggest the discipline is being internalized — keep the audit but reduce frequency. Empirical input: 2026-05-12 slot-interpretation audit = 24 SUSPECT, failure-mode + abandonment-path audit = 33 SUSPECT (more findings on smaller surface). Both audit shapes promoted to standing checkpoint cadence as a result.

The discipline framework is meant to grow with the corpus, not be locked exhaustively up front. New procedures get proposed when failure modes surface that current procedures didn't catch. Existing procedures get sharpened when the answers they produce stop being meaningful.

## Acknowledged limits

Worth being honest about what this discipline does and doesn't do:

- **Does**: catches missing-from-list items at named checkpoints; forces stop-and-test against forward-motion bias; separates writer-from-prober for authority-deference; rotates question shape against frame-acceptance and pattern-completion.
- **Doesn't**: catch categories of question we haven't learned to ask (still requires user / outside readers to surface those organically); guarantee the discipline is honored (depends on session-start-procedure compliance and on the authoring session not skipping); replace genuine outside-reader review (sub-agents share AI failure modes; cheaper-than-outside-readers approximation only).
- **The deeper fix** beyond this discipline: routine outside-reader cadence (real human readers reading at named milestones). Most expensive; most effective. Not always available; cadence-named when it becomes available.

**Empirical calibration data point (2026-05-12)**: First non-original audit run (failure-mode coverage + abandonment-path) produced 33 SUSPECT findings on ~38 audited surface — *more findings per surface* than the slot-interpretation audit's 24-of-78. The discipline catches more than initial calibration suggested. Cross-category overlap (same decisions surface in both probes) indicates a systemic underlying pattern (frame-acceptance + no-failure-mode imagination + forward-motion bias), not isolated gaps. Continued empirical tracking needed at each checkpoint to refine which audit shapes earn their cadence — and to surface when the underlying discipline is closing the gap (decreasing findings) vs not (steady or increasing findings).

The discipline is a foundation, not a solution. Foundation = something to build on; doesn't claim to be sufficient.
