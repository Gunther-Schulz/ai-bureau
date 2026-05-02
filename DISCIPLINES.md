# Working disciplines — how we operate across sessions

This document persists the cross-session working discipline for pbs-bureau development. **Read at session start** alongside `VISION.md` + `MAINTENANCE.md` + `HANDOFF.md` + `BACKLOG.md`.

Scope: this doc is **cross-session** — applies to all future dev work on this project regardless of phase. Phase-specific state (current rebuild progression, what we're working on now) lives in `HANDOFF.md`.

Locked session 16 during the foundational rebuild after we'd worked out a coherent set of disciplines mid-session. Persisting prevents future sessions from devolving into chaos by having to reconstruct the framing from scratch.

---

## Working procedure

**The flow**: AI proposes positions → user adjusts/challenges/confirms → AI persists on sign-off.

- **Decision phase** (positions, framings, choices): user approval needed before persistence
- **Content phase** (markdown content following locked decisions): write directly without per-content approval
- **Commit positions, don't menu**: AI commits to recommendations with rationale; user shapes via challenge or confirmation. Avoid presenting open menus.
- **Commit and push often**: no per-commit confirmation needed; treat push as part of commit

Per memory: `feedback_propose_before_commit.md`, `feedback_judgment_and_automate.md`, `feedback_push_after_commit.md`.

---

## Cross-session disciplines

### 1. Source-grounded; cite file:line; flag synthesis vs citation

Before asserting what a doc/DR/architectural commitment says, read the source. Cite specific `file:line` when applicable. Flag synthesis vs citation distinctly. Calibrate confidence by basis:
- "Per `<file>:<line>`, X" → high confidence (direct citation)
- "From HANDOFF/MEMORY summary, X" → medium confidence (flag explicitly)
- "Pattern-matched / inferred / my synthesis" → low confidence (flag explicitly)

Pattern-matching from HANDOFF prose, memory summaries, or prior-conversation knowledge is **NOT direct evidence** per global `~/.claude/CLAUDE.md` honesty-about-sources rule.

Per memory: `feedback_source_grounded.md`, `feedback_vision_arch_grounding.md`.

### 2. Apply principle uniformly

When applying any principle, enumerate all categories the principle could apply to — independent of inherited framings ("docs vs code", "active vs deprecated", "X stays per Phase Y", etc.). Test each: does the principle apply? Verify "no" boundaries are genuine, not carried-forward conventions.

Per memory: `feedback_apply_principle_uniformly.md`.

### 3. Pre-decision sharpening

At decision-formation moments, run sharpening rounds BEFORE locking:
- **Round 1** = full monty (proactive comprehensive — stress-tests + edge cases + counter-arguments)
- **Round 2+** = user-triggered (external-perspective friction)

Pre-decision sharpening outperforms post-mortem audits because pre-decision is sparring-mode (axis 2) while audits are validator-mode anchored to existing content.

Per memory: `feedback_pre_decision_sharpening.md`, `feedback_full_monty_upfront.md`.

### 4. Cascade prevention (greenfield-draft + minimize-embedded + cascade-pass + foundation-first)

When locking a new architectural commitment that depends on or composes with prior work:

1. **Greenfield-draft** from primary sources (VISION, locked architectural commitments in MAINTENANCE.md, first principles) — NOT from prior cross-references as anchors
2. **Minimize embedded descriptions** of not-yet-locked terms — use brief role tags + cross-ref to authoritative source; don't carry the not-yet-locked term's full definition inline
3. **Cascade-pass after locking — at lock-TIME, NOT deferred** — before committing the lock of a new term, run grep across all docs for the term's mentions; identify any "(canonical entry forthcoming)" or "(forthcoming)" markers referencing the now-locked term; update them in the same commit. **Recurring failure mode** (caught in Round 2 + Round 3 sharpening of session 16): cascade-pass deferred → stale forthcoming markers accumulate → next sharpening round catches them but they've already polluted the corpus. Make it literal: `git grep "<term> .*forthcoming" --` before committing any lock.
4. **Lock foundation-first when sequence has discretion** — when multiple entries could be locked next, prefer the most foundational (most cross-referenced; most-composed-against). Bottom-up locking matches the architecture's compositional structure: derived terms compose on foundational ones. Inverse direction creates churn (every foundational lock cascades through many prior derived entries) and bias (foundationals get drafted against speculative cross-refs already established by derived entries). Originated in GLOSSARY entry-by-entry workflow + session-16 round-2 sharpening when missed cascade-pass demonstrated the cost of non-foundational-first sequencing.

Originated in GLOSSARY entry-by-entry workflow (session 16); generalizable to any architectural locking work where prior entries forward-reference not-yet-locked terms.

### 5. No-defer; mental-model first; surface info-gaps as watch-list entries

Never defer. Before deferring, run **D Gate** (Defer Gate; per `profiles/INDEX.md`):

1. **Mental modeling within profile grounding** — construct hypothetical scenarios across L1-L9 profiles + G consumer gate; check primitive's classification holds across mental scenarios
2. **External-information test** — name a SPECIFIC external signal whose absence prevents the decision. "We haven't designed it yet" / "downstream isn't locked when we could lock it now" — fail the test
3. **Effort-asymmetry test** — could we do the design today if we chose? If yes — even if it might be wrong — NOT a chronological gap

If mental modeling resolves → evolve answer NOW (Round 1+2 sharpening). Don't defer when tools (profiles + multi-axis discipline + G gate + sharpen + decision-design-sharpening) are sufficient.

If mental modeling genuinely cannot resolve AND tests confirm external-info-gap → surface as **watch-list entry** naming the specific external signal awaited. Watch-list entries have resolution mechanisms; defers languish.

D Gate is structural per `feedback_wrong_shapes_impossible.md` (prefer structural constraints over conventions). Memory alone is insufficient as trigger — D Gate codifies the mental-modeling-first discipline as procedural enforcement at the decision moment.

Per memory: `feedback_pattern_not_instance_defers.md` (no-defer principle, v0.34 with D Gate), `feedback_defer_instinct.md` (defer-instinct in disguises).

### 6. Anchored vs preliminary-locked

- **VISION axes are anchored** — revise only on real-world falsification per VISION's own falsification criteria
- **Everything else is preliminary-locked** — current best position derived from available reasoning; revisable when VISION ideal design demands. DRs, ARCH disciplines, meta-rules, specs, ROADMAP, code = living drafts

Per memory: `feedback_preliminary_lock.md`.

### 7. Cascade discipline (structural consistency)

When changing any concept, decision, primitive, or term in any doc: identify every other place it appears and update each in the same commit (or tightly-coupled sequence explicitly marked as completing the cascade). Changes propagate **up, down, and sideways**.

Detailed mechanism: `MAINTENANCE.md` "TOP-LEVEL RULE — Cascade discipline".

---

## Architectural foundation (current rebuild — see `MAINTENANCE.md` for detail)

The foundational architectural commitments that future sessions inherit:

- **Repo identity: framework source, not deployment instance** (locked session 16): this repo holds framework + dev tooling only; app skills + per-deployment instance content belong in deployment workspaces, not here
- **Framework = MECHANISMS; Shape = POLICIES** (foundational architectural commitment; locked session 16)
- **Atoms vs containers**: `mechanism` + `policy` are atomic primitives; `framework` + `shape` are meta-primitive containers
- **A-B-C scope model** (preliminary-locked): Framework C (definitions) + Owner B (instances) derived from framework/shape; Layer A (layered content) orthogonal axis
- **5-layer doc structure**: Entry → Foundations → Overview → Architecture detail → DRs → Specs (+ Memory orthogonal)
- **GLOSSARY entry classification**: 4-axis tagging (Class / Layer / Axis / VISION usage)

Detail in `MAINTENANCE.md` "TOP-LEVEL SCOPE" + "TOP-LEVEL ARCHITECTURE" sections.

---

## Memory composition (locked feedback rules)

The following memory files compose with this framing:

| File | Role |
|---|---|
| `feedback_propose_before_commit.md` | Decision-phase approval; content-phase doesn't |
| `feedback_judgment_and_automate.md` | Commit positions; routine work without asking |
| `feedback_push_after_commit.md` | Push immediately after commit |
| `feedback_source_grounded.md` | Cite file:line; flag synthesis vs citation |
| `feedback_vision_arch_grounding.md` | Re-ground in VISION + ARCH for substantive work |
| `feedback_apply_principle_uniformly.md` | Test inherited categories independently |
| `feedback_pre_decision_sharpening.md` | Sharpening rounds before locking |
| `feedback_full_monty_upfront.md` | Comprehensive refinement upfront |
| `feedback_pattern_not_instance_defers.md` | Never defer; watch-list info-gaps |
| `feedback_defer_instinct.md` | Defer-instinct in disguises |
| `feedback_preliminary_lock.md` | VISION axes anchored; everything else preliminary |
| `feedback_blocked_actions.md` | Surface blocks; don't workaround |
| `feedback_refine_pareto.md` | Challenge most-aggressive change before shipping |
| `feedback_llm_instruction_tightness.md` | Sharpen markdown instruction layer |
| `feedback_links_plain_text.md` | Bare URLs; CLI doesn't render markdown links |
| `feedback_ai_as_runtime.md` | AI as runtime, not consumer |
| `feedback_wrong_shapes_impossible.md` | Structural constraints over conventional solutions |
| `feedback_dev_vs_app_skills.md` | Repo is framework source; dev skills live here, app skills don't |

Memory location: `/home/g/.claude/projects/-home-g-dev-Gunther-Schulz-pbs-bureau/memory/`. Index: `MEMORY.md` in same directory.

---

## When this doc itself changes

DISCIPLINES.md is foundational. Changes affect every subsequent session's discipline. When changing:

1. Identify what existing discipline is being changed/added/removed
2. Verify or update memory feedback files that compose with the changed discipline
3. Update `HANDOFF.md` to flag the change for future-session readers
4. Update relevant references in `MAINTENANCE.md` if architectural-foundation territory is touched
5. Cascade-pass: any docs referencing the changed discipline get updated in same commit

This doc is preliminary-locked like everything else (per discipline 6 above) — but changes should be deliberate, not casual.
