# Building AI-centric apps — methodological observations

**Status**: PRELIMINARY observations. Mostly true probably — not fully proven yet. These are subject to revision as evidence accumulates across sessions. See `learnings/README.md` for status discipline.

**Why this doc exists**: the user (experienced Python developer) noticed mid-session 16 that building AI-centric apps differs substantively from typical Python app development. Block-by-block run-and-test (which works well for Python) doesn't carry over cleanly. Capturing the observed differences while memory is fresh; the eventual goal is an AI-app-development-facilitation skill (per HANDOFF "Future ROADMAP items") that distills these into transferable practice.

---

## Observation 1: AI apps need upfront foundation in a way Python apps don't

**Pattern**: Python apps tolerate block-by-block development because the compiler catches contradictions, type-checking enforces interfaces, tests verify behavior. AI apps (markdown-heavy, LLM-mediated) lack these structural correctness checks. Cross-cutting vocabulary + framework/shape framing must be locked BEFORE tactical work, or contradictions silently accumulate.

**Evidence (session 16)**: archived corpus had `framework=mechanisms / shape=policies` framing named in session 14 but not consistently applied — instance-anchoring leakage in 5+ primitives surfaced session 16. Each finding had the same root: foundational vocabulary not crisply defined. Incremental patching kept failing because each patch landed on inconsistent foundation.

**Implication**: foundational layer (vocabulary + framing) precedes architectural detail. Don't try to "iterate to clarity" the way you'd iterate Python code — clarity in a markdown corpus requires upfront discipline, then growth from a stable base.

**Test it against**: building a new AI-centric module without a foundational vocabulary lock; observe whether contradictions surface within 2-3 sessions.

---

## Observation 2: Pattern-matching from summaries is a constant drift force in LLM-mediated work

**Pattern**: LLMs naturally pattern-match — they generate plausible-sounding content from partial context (summaries, headers, prior sessions' notes) without reading the actual source. Without explicit discipline, this corrupts assertions silently. The same failure mode that produces hallucinations in factual recall produces architecture-corruption in design work.

**Evidence (session 16)**: AI repeatedly asserted what session-14 DRs said, what schema shapes looked like, what Option B floor enforced — without re-reading the actual DRs. User caught this multiple times. Specific failures: malformed `groupings` schema example; over-confident defense of Option B as "universal"; quote attribution to wrong source file.

**Implication**: source-grounded discipline (`feedback_source_grounded.md`) is mandatory for AI-mediated architecture work. Cite `file:line`. Flag synthesis vs citation. Calibrate confidence by basis. The discipline itself is non-trivial to maintain — it requires explicit attention.

**Test it against**: asserting things without cite-by-line; observe whether assertions hold up to verification.

---

## Observation 3: Cascade discipline is load-bearing for AI apps

**Pattern**: Concepts in markdown reference each other heavily (term X mentions term Y mentions term Z). Without explicit same-commit cascade rule, when you change X, references in Y and Z drift out of sync silently. Pure code has compiler/linker enforcement; markdown has no such backstop.

**Evidence (session 16)**: archived corpus had multiple examples of the same concept defined inconsistently across DRs (e.g., shape-extension DR's filesystem location vs v0.34 entity-md restructure's location). The contradictions accumulated session-by-session because cascade discipline was implicit, not enforced.

**Implication**: cascade discipline (changes propagate up/down/sideways in same commit, per MAINTENANCE.md TOP-LEVEL RULE) must be top-level architectural rule. Glossary entries that cross-reference need cascade-pass after locking.

**Test it against**: making a vocabulary change without grep-cascade-pass; observe whether stale references emerge.

---

## Observation 4: Pre-decision sharpening > post-mortem audits for AI architecture

**Pattern**: For Python apps, write-then-test-then-fix is efficient because tests catch problems mechanically. For AI apps with markdown architecture, post-mortem audits are validator-mode (LLM anchored to existing content; manufactured criticism risk) while pre-decision sharpening is sparring-mode (LLM not yet committed; fresh perspective generates real refinements). Same architectural decisions get vastly better outcomes when sparred at formation moment.

**Evidence (session 16)**: multi-round sharpening on framework/shape/A-B-C surfaced 19 refinements with high quality; subsequent audit-style passes mostly produced noise. Memory `feedback_pre_decision_sharpening.md` documents the empirical pattern.

**Implication**: build sharpening into decision-formation flow (round 1 full monty + user-triggered rounds 2+); don't rely on post-mortem audits as primary quality mechanism. Audits remain useful for drift-detection, but pre-decision sharpening is where the value compounds.

**Test it against**: skipping pre-decision sharpening on a new architectural commitment; observe whether subsequent sessions surface preventable refinements.

---

## Observation 5: Working procedure (propose → adjust/challenge/confirm → persist) makes AI collaboration sustainable

**Pattern**: Without a clear procedure, AI either over-steps (acts on inferred intent without sign-off) or under-steps (asks for confirmation on every micro-decision). Both degrade collaboration — over-stepping erodes trust; under-stepping bottlenecks work. The decision-phase / content-phase split (decision needs sign-off; content doesn't) plus "commit positions, don't menu" balances throughput with control.

**Evidence (session 16)**: locked early in this session via `feedback_propose_before_commit` + `feedback_judgment_and_automate`; held throughout session 16's substantive work (archive, doc structure, VISION tightening, GLOSSARY entries). User explicitly said "no need to confirm" for routine commits — efficient flow.

**Implication**: AI-app development needs explicit human-AI collaboration discipline. Without it, project velocity oscillates between AI-doing-too-much and AI-doing-too-little.

**Test it against**: AI-mediated work where no procedure is locked; observe whether collaboration friction increases.

---

## Observation 6: Archive-as-reference works for AI-app pivots

**Pattern**: AI-centric app development involves substantial pivoting (new ideas, reframings, abandoned directions). Pure deletion loses hard-won detail; carrying everything forward creates corpus bloat. Keeping prior corpus accessible in `archive/` while building fresh against locked foundation prevents both failure modes — archive becomes evidence of "what was tried" + reference for forgotten detail; new corpus stays clean.

**Evidence (session 16)**: archived 30 DRs + ARCH (3231 lines) + ROADMAP + multi-session HANDOFF + extensions/framework/ + backend/ + plugin/ etc. Archive reference consulted multiple times during rebuild; no detail lost; new corpus building cleanly against locked foundation.

**Implication**: AI-app development should adopt archive-as-reference as a methodology pattern. When an architectural pivot is needed, archive the old + build fresh against new foundation; consult archive selectively rather than cargo-culting forward.

**Test it against**: an AI-app project that doesn't archive pivoted-from material; observe whether pivots become harder over time as accumulated cruft compounds.

---

## Observation 7: Foundation-up rebuild is sometimes the structural fix

**Pattern**: When incremental patching keeps surfacing the same root issue (in pbs-bureau case: "foundational vocabulary not crisply defined"), wholesale rebuild is structurally correct, not over-reaction. Pre-launch deprecation is essentially free; the cost of accumulating contradictions exceeds the cost of foundation-up rebuild.

**Evidence (session 16)**: 6 findings during clarification phase all converged on one root cause. Incremental fixes would have patched each finding individually; wholesale rebuild dissolved them all in one structural move. Memory `feedback_full_monty_upfront` validates: comprehensive refinement upfront beats fragmenting.

**Implication**: when the same root surfaces repeatedly, that's a signal the architecture needs rebuild not patching. AI-app projects should reserve permission for foundation-up rebuilds; the alternative (incremental forever) compounds drift.

**Test it against**: AI-app project where same root issue recurs across 3+ sessions without wholesale rebuild; observe whether patching mode delivers stable architecture or whether drift compounds.

---

## Promotion path

When an observation here holds across multiple sessions + multiple contexts, it earns promotion:
- Behavioral rule → memory feedback file (e.g., `feedback_source_grounded.md` was promoted from observation 2's repeated occurrence)
- Architectural commitment → MAINTENANCE.md / GLOSSARY / DR (e.g., cascade discipline was promoted from observation 3)
- Methodological pattern → eventual AI-app-development-facilitation skill

Until promotion, observations stay PRELIMINARY here. Don't treat as locked discipline elsewhere in the corpus.
