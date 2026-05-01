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

---

## Observation 8: Cascade-pass needs a mechanical forcing function, not principle alone

**Pattern**: The cascade-pass discipline (review prior cross-references when locking a new term; reconcile inconsistencies in the same commit) is correct in principle but slips in practice when treated as principle-awareness only. AI working under principle-discipline keeps missing the same cascade-pass cases. Strengthening the discipline by embedding a literal mechanical command (e.g., `git grep "<term> .*forthcoming"` before committing) shifts it from principle-awareness to mechanical enforcement. Round 4 sharpening (after the strengthening) had dramatically fewer cascade-pass-missed findings than Rounds 2 + 3 (before the strengthening).

**Evidence (session 16)**: Round 2 sharpening caught H1 = mechanism cascade-pass not done. Round 3 sharpening caught the same finding shape (event + actor + shape cascade-passes not done). Same recurring failure mode. After Round 3 strengthened the cascade-pass discipline with literal grep command in DISCIPLINES.md sub-rule #3 ("at lock-TIME, NOT deferred"), Round 4 found significantly fewer issues; the strengthening worked.

**Implication**: For AI-mediated architectural work, principles that rely on AI vigilance keep slipping. Discipline rules embedded as explicit mechanical commands (grep, lint, automated check) catch what vigilance doesn't. The mechanical forcing function is asymmetrically more reliable than the principle alone.

**Test it against**: any discipline rule that depends on "AI will check this when locking a new term" — observe whether it actually fires reliably. If sharpening rounds keep catching the same kind of miss, the rule needs mechanical enforcement, not just clearer wording.

---

## Observation 9: Foundation-first locking emerges from cascade economics

**Pattern**: When locking architectural commitments that have compositional structure (some primitives compose ON others), the order of locking matters. Foundation-first locking minimizes cascade churn: each subsequent entry composes against locked foundations + has fewer prior cross-refs to update. Inverse direction (derived-first) creates churn (every foundational lock cascades through many prior derived entries) + bias (foundationals get drafted against speculative cross-refs already established by derived entries).

**Evidence (session 16)**: GLOSSARY entry-by-entry locking explicitly walked the foundational priority ladder (mechanism + policy + framework + shape locked early; workspace + specialist + skill + substrate locked once foundationals were stable; protocol + adapter + practitioner locked last because they reference everything else). When the user asked "should we always walk up the foundational priority ladder?", the answer "yes" was strongly supported by cascade economics — not aesthetic preference.

**Implication**: For any architectural locking work in AI app dev, sequence has compounding cost. Foundation-first isn't just a preference; it's a strategy that makes per-entry work tractable + reduces cascade-pass volume. Lock order matters as much as content.

**Test it against**: an architectural locking project that locks high-level / derived terms first and tries to fill in foundationals after. Observe whether the work compounds (each foundational lock cascades through many prior entries) compared to foundation-first projects.

---

## Observation 10: Sharpening cadence emerges from rebuild rhythm

**Pattern**: Sharpening rounds in entry-by-entry locking work are valuable (catch broader pattern issues) but not free (each round consumes turns). The right cadence emerges empirically: too frequent = noise; too infrequent = compounding errors. In session 16 the cadence converged to "round every ~4-5 entries OR at architectural milestones." This wasn't predetermined — it emerged from observing what frequency caught real issues without bottlenecking.

**Evidence (session 16)**: Round 1 after 8 entries (foundational batch); Round 2 after 10 entries (foundational atom layer complete); Round 3 after 14 entries (4 more added); Round 4 after 21 entries (4 more added — milestone: Pattern A primitives all locked). Each round caught real findings without consuming excessive turns.

**Implication**: Sharpening cadence is a discoverable property of the work, not a predeterminable one. Initial trigger ("after 8 entries") was arbitrary; subsequent triggers calibrated based on observed failure-mode density. AI app dev should expect to discover the right cadence rather than impose it.

**Test it against**: AI app dev project with arbitrary sharpening cadence imposed. Observe whether the cadence matches the work's natural failure-mode density or causes either bottleneck (too frequent) or compounding (too infrequent).

---

## Observation 11: Naming inconsistencies surface during USE, not at lock-time

**Pattern**: Vocabulary that's coherent in isolation can reveal imprecision when applied across multiple entries. AI may invent terminology that's locally clean ("dual-nature") but globally ambiguous (different meanings across entries: bipartite vs tripartite; specialist's vs substrate's). The cross-entry sharpening view catches what per-entry locking doesn't because per-entry work is local + sharpening is global.

**Evidence (session 16)**: "dual-nature" introduced as casual label survived through multiple entries (substrate, specialist, MAINTENANCE.md). User question "so dual nature means they have impls on two pattern levels?" surfaced the imprecision (substrate has 3 aspects, not 2). Sharpening pass renamed to "multi-aspect" with explicit count distinction. Same shape: I conflated three distinct dual-nature patterns (Pattern A / B / C); only the cross-entry view + user prompt revealed it.

**Implication**: Vocabulary lockability is bipartite. Local lockability (does this term work in its own entry?) ≠ global lockability (does it remain crisp across all entries?). Round-N sharpening's cross-entry view is non-redundant with per-entry cascade-pass discipline; both are needed.

**Test it against**: a glossary project where only per-entry sharpening is done (no cross-entry sharpening rounds). Observe whether terminology drift accumulates over time.

---

## Observation 12: User clarifying-questions in long sessions are forcing functions

**Pattern**: In AI-led architectural work over long sessions, AI tends toward local-coherent / globally-fuzzy outputs (per Observation 11). Periodic user clarifying-questions ("is X a mechanism?", "shouldn't this be Y?", "are these really the same pattern?") force AI to articulate distinctions that local-coherent outputs were obscuring. The clarifying-question is itself an architectural input — surfaces what AI's local view didn't.

**Evidence (session 16)**: User questions throughout that surfaced findings AI hadn't:
- "shouldn't workspace configuration be a policy?" → resolved: shape-level vs workspace-level distinction
- "is sparring a mechanism?" → surfaced VISION's loose-vs-locked vocabulary issue (Round 4 H1)
- "should they be decomposed?" → resolved: keep PRIMITIVE class with multi-aspect description; don't multiply primitives
- "doesn't dual-nature mean two pattern levels?" → caught dual-nature → multi-aspect rename
- "why is mechanism not a first-level entry?" → surfaced TOC need for categorical navigation

Each surfaced an issue AI's local-coherent output hadn't.

**Implication**: AI-led architectural work needs human checkpoints. Pure-AI iteration produces local-coherent / globally-fuzzy work; user questioning is the corrective. The questions should be encouraged, not skipped (e.g., "let me just lock 5 more entries before you ask"). Each clarifying-question pays compounding architectural value.

**Test it against**: AI-led architectural session without periodic user clarifying-questions. Observe whether globally-fuzzy outputs accumulate.

---

## Observation 13: Plain-language re-explanations catch AI imprecision

**Pattern**: When user asks AI to explain a just-locked concept "in plain language," the act of plainspeaking forces precision that the formal entry sometimes obscured. Formal entries can hide imprecision behind technical language; plain-language re-explanation strips the technical scaffolding and reveals whether AI actually understands or was pattern-matching.

**Evidence (session 16)**: User asked for plain-language explanations of substrate's tri-aspect (Surface + Impls + Instance) and protocol's mechanism. Each plain-language re-explanation forced AI to articulate distinctions that the formal canonical glossed over (e.g., the "house has heating system" analogy for protocol — Surface + Implementations + Instance all became concrete). Plain-language test surfaced no major imprecision in those cases — but the test exists as a discipline regardless.

**Implication**: For high-stakes architectural definitions, AI should be able to explain in non-technical terms. If the plain-language explanation feels strained or contradictory, the formal entry has imprecision that technical scaffolding was hiding. Asking for plain-language re-explanations is a useful periodic test.

**Test it against**: any architectural primitive locked. Ask AI to explain in non-technical terms with concrete examples. Observe whether the plain-language explanation is consistent with the formal entry.

---

## Observation 14: Decision-shifts deserve explicit commit-flagging

**Pattern**: During architectural work, judgment shifts happen — AI may commit position X early, then re-evaluate and commit position Y later. Without explicit flagging, future-session readers (or AI) see only the final position; the reasoning shift is lost. Flagging decision-shifts in commit messages preserves architectural genealogy.

**Evidence (session 16)**: AI initially committed "AI runtime is its own primitive" (Round 1 sharpening); later shifted to "AI runtime is a stub / cross-ref to substrate" (during entry-locking). The shift commit explicitly flagged: "Decision-shift commit: I'm reconsidering 'AI runtime' — it's effectively the Instance aspect of substrate." Future-session readers see WHY the shift happened, not just THAT it happened.

**Implication**: Commit messages aren't just changelog for code — they're architectural genealogy for AI-mediated work. Decision-shifts should be flagged explicitly so future sessions can trace reasoning. Pure "what changed" commit messages lose context that "why it changed" preserves.

**Test it against**: a multi-session architectural project where decision-shifts happened but weren't flagged. Observe whether future sessions can reconstruct WHY the architecture is shaped a particular way.

---

## Promotion path

When an observation here holds across multiple sessions + multiple contexts, it earns promotion:
- Behavioral rule → memory feedback file (e.g., `feedback_source_grounded.md` was promoted from observation 2's repeated occurrence)
- Architectural commitment → MAINTENANCE.md / GLOSSARY / DR (e.g., cascade discipline was promoted from observation 3)
- Methodological pattern → eventual AI-app-development-facilitation skill

Until promotion, observations stay PRELIMINARY here. Don't treat as locked discipline elsewhere in the corpus.
