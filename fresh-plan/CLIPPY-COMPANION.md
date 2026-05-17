# fresh-plan Clippy companion

Project-local instructions for Clippy when operating on fresh-plan.

**Read at session-start** alongside `fresh-plan/README.md` + global CLAUDE.md.

Companion to Clippy's upstream principles (V1 / D1 / 8-item lifecycle / Honest basis caveats / etc. as of Clippy v0.4.6 — those apply to fresh-plan work unchanged). This document covers fresh-plan-specific shape on top of the upstream baseline.

---

## State directory mapping

Clippy persists at `.ai/` per its DISK_LAYOUT. Fresh-plan's native state lives elsewhere:

- `fresh-plan/decisions/D<NN>-*.md` — per-entry ledger files (append-only)
- `fresh-plan/decisions.md` — chronological index
- `fresh-plan/roadmap.md` — deliverable tracking
- `fresh-plan/README.md` — session-start procedure + current-state snapshot
- `fresh-plan/probing.md` — adversarial discipline + pre-lock probe procedures
- `fresh-plan/CONCEPTS.md` — framework orientation

When working on fresh-plan, Clippy `.ai/` is acceptable for in-flight investigation tracking ONLY. Do NOT duplicate ledger state to `.ai/`. At lock moments, persist canonical state to fresh-plan native files. Clippy `.ai/` is scratch; fresh-plan native state is source of truth.

For impl-only work targeting `fresh-plan/impl/` Python code: Clippy `.ai/` lives at `fresh-plan/impl/.ai/` per Clippy's standard pattern.

---

## Artifact classes — [design] vs [impl] labeling

Every piece of fresh-plan work is one of:

- **[design]** — D-entry / specification / framework architecture / ledger work (`decisions/D<NN>-*.md` files + cross-cutting docs `CONCEPTS.md` / `roadmap.md` / `schemas/`). Append-only; locked entries; supersedes-relationships explicit.
- **[impl]** — runtime code in `impl/src/` + tests in `impl/tests/` + extension specs in `impl/extensions/`. Refactorable; tests-pass discipline.
- **[design+impl]** — ONLY when [design] lock and [impl] follow-through are atomic (same git commit). Otherwise split.

Tag chat reports + commit subjects with the label:
- `fresh-plan: D<N> [design] — <title>`
- `fresh-plan: D<N> [impl] — <summary>`
- `fresh-plan: D<N> [design+impl] — <combined>`

---

## D-entry shape (substantive entries)

When drafting a substantive D-entry, apply this template:

```
# D<N> — <YYYY-MM-DD> — <one-line title>

**Decision (substantive; <cluster type if applicable>)**: <crisp lock statement>

## A. Scope of cluster

<What is in scope; honest cardinality; out-of-scope cross-refs to other clusters>

## B. Triad applied per path

### B.1 — <path 1 name>

| Triad element | Lock |
|---|---|
| **Detection** | <how failure is detected> |
| **Surface** | <how failure becomes observable> |
| **Recovery** | <defined path after detection + surface> |

### B.2 — <path 2 name>
... (additional paths if scope warrants)

## C. Impl follow-through (separate commit; tracked in roadmap.md)

<Specific code changes; new types; refactors; tests; estimated size>

## D. What is NOT in this decision

<Explicit deferrals; no-scope-creep statements; numbered DEFERS if pre-lock probe surfaced quiet assumptions>

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: <one line>
- **WHO**: <enforced by which layer; framework-validator (B1) / substrate (runtime) / shape (policy) / specialist (impl) / extension (registered) / opaque (documentary) / deferred (named phase)>
- **FAILS**: <recursive failure-mode framing>
- **CROSS**: <which slots in which D-entries this interacts with>
- **DEFERS**: <per §D>

## E. Pre-lock probe disposition (per probing.md Procedure 3 refined-skip rule)

<FIRED or SKIPPED with documented reason; if FIRED, summarize probe outcome + quiet assumptions surfaced>

## Rationale

<Why this lock; how it composes with prior entries; durability framing if relevant>

**Cross-references**: <D-N list with section pointers>
```

Clarification / supersedes entries use a smaller template — bold `**Decision (clarifies D<M>)**:` paragraph + optional named subsections only when warranted + Cross-references. See `fresh-plan/README.md` Ledger conventions for the distinction.

---

## Cluster supersedes pattern

Per D45 §C, the bounded-fill plan processes 6 runtime-path clusters via cluster supersedes entries:

1. Boot-procedure cluster (D46) — DONE
2. Subscriber-dispatch cluster (D47) — DONE
3. Adapter cluster (D48) — DONE
4. Specialist cluster (D50) — DONE
5. Validation cluster (D51) — DONE
6. Composition-change cluster (D52) — REMAINING

Each cluster supersedes follows the D-entry shape above. Cluster cardinality is HONEST — D46/D47/D48 had 3 paths each; D50 had 1 path; D51 had 2 paths. **Do NOT inflate scope to match precedent cardinality** — apply Clippy D1 scope-cardinality-honesty sub-check + count actual content cardinality independently.

D49 was a clarification entry (sharpen-surfaced corrections to D47 + D48 from the 2026-05-12 retrospective sweep); not a cluster supersedes.

---

## Pre-lock probe FIRE vs SKIP refined rule

Per probing.md Procedure 3 + D48 §E + D50 §E precedent:

- **SKIP** the pre-lock probe when the cluster supersedes is **PURE pattern application** — operationalizes existing contract; uses existing typed exceptions / categories / composition framings. Cite D45 §E precedent. Pattern: D46 + D47 + D51 SKIPPED.
- **FIRE** the pre-lock probe when the cluster supersedes introduces **NEW contract content** — new typed exception, new category vocabulary, new composition framing, new sub-procedure. Pattern: D48 + D50 FIRED. Cite D48 §E precedent.

Pre-lock probe is a sub-agent dispatch:
- Brief: code-claim verification + Phase C quiet-assumption surfacing
- Brief shape per probing.md Procedure 3 brief menu (rotating; pick the one that fires hardest for the entry)
- Return: structured findings (per-claim verified/wrong; quiet assumptions named)
- Disposition: incorporate quiet assumptions as explicit §D DEFERS

---

## Sketch-then-lock checkpoint (MANDATORY user interrupt, unless batch-authorized)

Before drafting any substantive D-entry, present a SKETCH to the user. Wait for explicit sign-off before drafting the committed entry.

This **OVERRIDES** Clippy autopilot's "do not interrupt user during unit execution" default. Reason: append-only ledger means wrong-locked content requires supersedes entry (ledger inflation); cost of asking > cost of wrong-lock for substantive D-entries.

Sketch contains:
- Proposed title + cluster supersedes / clarification / refinement classification
- §A scope + cluster cardinality (count of paths honest)
- §B triad framing per path (Detection / Surface / Recovery — high-level)
- §C impl follow-through scope (lines / tests estimated)
- §D Phase C / future-phase deferrals named
- §E pre-lock probe disposition lean (FIRE vs SKIP rationale)
- Specific design choices that need user-direction

Skip user-sign-off ONLY for:
- Impl follow-through commits for already-locked D-entries (§C is the brief)
- Routine roadmap status updates after [design]/[impl] cycles
- Mechanical clarifications (e.g., D49 sharpen-surfaced corrections to factual errors)

### Autopilot batch mode (Sketch-then-lock relaxed)

When the user has given **explicit batch authorization** at session start (e.g., "finish all remaining Bref work hands-off"; "autopilot through D53/D54 + slot-pass without per-entry approval"), Sketch-then-lock interrupt is **suspended** for the duration of the authorized scope. Autopilot proceeds through SKETCH → pre-lock probe (FIRE/SKIP per refined rule) → draft → commit without returning to user-checkpoint for the SKETCH-stage approval.

Mitigations that remain in effect under batch mode:
- Pre-lock probe FIRES for entries with new contract content (per D48 §E + D50 §E + D52 §E refined skip rule); SKIP for pure pattern application (per D45 §E precedent — D46/D47/D51 pattern)
- probing.md investigation-before-claim discipline (V1 evidence + secondary-source synthesis discrimination + temporal discipline + class-completeness — now upstream in Clippy v0.4.6)
- Clippy D1 plausibility trace + scope-cardinality-honesty sub-check (now upstream in Clippy v0.4.6)
- Post-build verify phase (Clippy autopilot post-build per references/post-build.md)
- Circuit breakers (3 failures per unit; 3 consecutive unit failures stop build)
- `/clippy:cancel` at any time

**Empirical risk** (honest tradeoff): Sketch-then-lock catches first-pass scope-inflation patterns that codified disciplines empirically miss (D49 first-pass mirroring D48's 3-path structure when D49 had 1 SUSPECT — caught by "do a second pass" user prompt, not by probing.md or pre-lock probe). Without the user-interrupt catch, similar inflations may commit; correction is via supersedes entries (D49-style clarifications) post-hoc. Append-only ledger means corrections accumulate, not overwrite.

Recovery path when batch mode produces a flawed entry:
1. Subsequent sharpen sweep (next sessions or end-of-batch retrospective) surfaces findings
2. Clarification entry (D49 pattern) corrects load-bearing errors via append-only
3. Wording-polish findings log-and-accept (cumulative ledger-load not justified)

Batch mode is a **deliberate trade**: more autonomy, more post-hoc cleanup. Surface this tradeoff explicitly when accepting batch authorization. Do not silently relax Sketch-then-lock — the relaxation is itself an explicit recorded decision per the user's batch-authorization phrasing.

Returning to normal Sketch-then-lock (non-batch mode): when authorized scope completes OR user signals "back to per-entry" / "next D-entry needs sign-off" / explicit cancellation, resume Sketch-then-lock interrupt for subsequent substantive D-entries.

---

## Append-only ledger discipline

Locked D-entries (entries in `decisions/D<NN>-*.md` referenced from `decisions.md`) are IMMUTABLE. Never edit a locked entry's substance. To override:

- **Clarification entry** — narrow scope; clarifies one slot or supersedes one slot of a prior entry. Smaller template (no full §A-§E structure).
- **Supersedes entry** — replaces a prior decision. Title includes "Supersedes D<M>".
- **Extends entry** — adds new contract content built on prior decision. Title includes "Extends D<M>".

Cluster supersedes (D46-D52) are substantive Extends entries per D45 §C.

Sharpen-surfaced wording-polish on locked entries → log-and-accept; original entry stands. Only correct via clarification entry when load-bearing (factual error; contract gap; cold-read ambiguity affecting contract clarity). D49 is the precedent.

---

## After-locking checklist

When a D-entry locks ([design]) OR an [impl] follow-through commits, update:

1. **decisions.md index** — add new D-entry to chronological list with one-line title + date
2. **roadmap.md deliverable row** — update status: `NOT STARTED` → `[design] DONE; [impl] PENDING` → `[design+impl] DONE`
3. **README.md current-state snapshot** — update "Last ledger entry" if changed; update test count if [impl] changed it; update cluster-supersedes-landed list

Test discipline: from `fresh-plan/impl/`, `.venv/bin/python -m pytest -q` must be green before [impl] commit. Note count change in roadmap row + README snapshot.

Working tree: leave the 0-byte UUID-named file at repo root unstaged (session-JSONL smoke-reminder per memory).

---

## Cross-references to canonical docs

- `fresh-plan/README.md` — session-start procedure + working disciplines + ledger conventions
- `fresh-plan/CONCEPTS.md` — framework orientation (what fresh-plan is; 8 kinds; layered model)
- `fresh-plan/decisions.md` — chronological D-entry index
- `fresh-plan/decisions/D45-establishes-detection-surface-recovery-triad-as-standing.md` — canonical cluster supersedes meta-foundation
- `fresh-plan/decisions/D48-extends-d16-adapter-cluster-honors-detection-surface-recovery.md` — pre-lock probe FIRED precedent
- `fresh-plan/decisions/D49-clarifies-d47-c-d-d48-b2-sharpen-surfaced-corrections.md` — clarification entry precedent
- `fresh-plan/probing.md` — adversarial probing discipline (sub-agent dispatch for pre-lock probe; investigation-before-claim; pattern-completion failure mode; Sketch-then-lock pattern)
- `fresh-plan/roadmap.md` — deliverable tracker; current Bref scope

Clippy upstream principles (v0.4.6+) that apply unchanged:
- V1 verification standard + secondary-source synthesis + temporal discipline + class-completeness (VERIFICATION_EXAMPLES.md)
- D1 pre-lock plausibility trace + scope-cardinality honesty sub-check (READINESS.md)
- Honest basis caveats cross-phase output convention (composer.md)
- 8-item lifecycle / C-checklist / P-checklist / U-checklist / READY self-check
