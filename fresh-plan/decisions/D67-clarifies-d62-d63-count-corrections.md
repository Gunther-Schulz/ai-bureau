# D67 — 2026-05-17 — Clarifies D62 + D63 — count corrections per retro-validation Group 4 finding

**Decision (clarifies D62 + D63 honest-basis-caveats + header counts)**: D62 (Bref output workstream entry) and D63 (Phase B closure entry) carry count-drift in their headers + Honest-basis-caveats sections that needs append-only correction. Per Cite-or-Read-or-Flag discipline (README session-start step 5 HARD RULE + global CLAUDE.md §"Honesty about sources"), false-verified count claims in the basis-caveats block — the project's load-bearing honesty-hygiene mechanism — violate the discipline. D67 converts the false-verified claims into Flagged-and-corrected per the discipline's recovery path. The substance of D62 and D63 stands; the body enumerations are correct; the drift is confined to (a) header / synthesis-line counts and (b) `(verified N test files)` / `(verified N modules)` basis-caveat assertions. Append-only ledger discipline preserved (D62 + D63 not edited; readers cross-referencing D62/D63 against actual lock-time state can find D67 in `decisions.md` index + apply the corrections).

## A. Drift inventory (lock-time evidence)

At D62 / D63 lock-time (commit `60eb310` — `fresh-plan: D62 + D63 [design] — Bref output + Phase B closure; PHASE B COMPLETE`), `git ls-tree -r 60eb310` returns:

| Claim in D62 / D63 | Source location | Actual at lock-time |
|---|---|---|
| "32 test files" | D62 §A line 9; D62 §E line 70; D62 basis-caveat line 98; D63 §A line 7; D63 §B line 23; D63 basis-caveat line 110 | **28** `test_*.py` files in `impl/tests/` (verified `git ls-tree -r 60eb310 -- fresh-plan/impl/tests/ \| grep "test_.*\.py$" \| wc -l` → 28) |
| "15 runtime modules" | D63 §A line 7; D63 §B line 17; D63 basis-caveat line 110 | **13** modules in `impl/src/fresh_plan/runtime/` excluding `__init__.py` (verified `git ls-tree -r 60eb310 -- fresh-plan/impl/src/fresh_plan/runtime/ \| grep "\.py$"` → 14 entries including `__init__.py`; substantive runtime modules = 13) |
| "7 validator modules" | D63 §B + basis-caveat | **8 entries at lock-time** (1 `__init__.py` + 7 substantive). D63 §B body line 21 enumerates the 7 NAMED substantive modules (correct ✓); D63's basis-caveat "verified 7 entries" is itself a false-Cite class (claims verification against directory listing which has 8 entries). Honest correction: D63 body claim "7 substantive validator modules" stands ✓; D63 basis-caveat verification statement was inaccurate (false-Cite class, same as the test-files + runtime-modules drift). |
| "218 pytest pass" | D62 §A line 3; D62 §E line 70; D62 basis-caveat line 98; D63 §A line 7; D63 §B line 23; D63 basis-caveat line 110 | **218** ✓ (correct) |
| "5 substantive Extends entries (D54-D58 + D59)" | D62 line 3 + line 9 | **range-vs-count drift**: range `D54-D58 + D59` enumerates 6 entries (D54 + D55 + D56 + D57 + D58 + D59); count says 5. D62 §D line 56 carries the honest framing: "5 substantive Extends-D-entries (D55-D59)" — narrow scope; D54 separate as migration-safety per its own framing. Lines 3 and 9 conflate D54 into the slot-pass scope. |

**Verification of body enumerations (these stand)**:

- D62 §B lines 24-25 enumerate 28 test file names — count matches lock-time evidence. Readers using §B for actual content get the right inventory.
- D63 §B line 18 enumerates 13 runtime module names — count matches lock-time evidence excluding `__init__.py`. Header count "15" is inflated by 2.
- D63 §B line 21 enumerates 7 NAMED substantive modules: workspace.py, checks.py, dependency.py, extensions.py, schemas.py, types.py, shape_migration.py. `__init__.py` is NOT in the enumeration; the body claim of 7 substantive modules is correct.
- D63 §B lines 24-25 enumerate 28 test file names — count matches lock-time evidence.

## B. Substantive content (what the drift is and isn't)

The drift is in two places:
1. **Header / synthesis-line count claims** — load-bearing for readers skimming the entry for the headline state-at-close summary.
2. **`(verified N test files)` / `(verified N modules)` basis-caveat claims** — load-bearing because the basis-caveats block IS the discipline mechanism that bounds claim-rigor. A basis-caveat claiming verification without actual verification is the canonical AI failure mode the Cite-or-Read-or-Flag discipline is designed to catch — and that mode slipped through at D62/D63 lock-time.

**Three false-Cite classes catalogued** (the basis-caveat block in D62/D63 carried verification claims that did not match the directory listings they cited):
- D62/D63 basis-caveat: "32 test files verified" — actual 28 (false-Cite; body §B enumerates 28 correctly).
- D63 basis-caveat: "15 runtime modules verified" — actual 13 substantive (body §B enumerates 13 correctly).
- D63 basis-caveat: "7 validator entries verified" — actual 8 entries (1 `__init__.py` + 7 substantive). Body §B enumerates 7 NAMED substantive modules CORRECTLY ✓; the basis-caveat "7" conflates substantive-count with directory-listing-count and claims verification against an 8-entry listing.

The drift is NOT in:
- Body enumerations (correct in both entries; readers cross-referencing §B against the impl tree get accurate inventory).
- Substantive architectural claims (cluster supersedes mapping; forward-bars; FAILURE_CATEGORIES count; Phase B closure criteria satisfaction).
- The architectural conclusion (Phase B closes structurally clean; no T1 findings; foundation holds).

## B.2 Honest framing — meta-data point

D67 is born OF the retro-validation pass that the user invoked precisely BECAUSE D62-D63 went through performative-Clippy (general-purpose sub-agents bypassing `clippy:reviewer`). D67 itself goes through real `clippy:autopilot` (this autopilot cycle). The discipline closes the loop: retroactive `clippy:reviewer` found what performative-Clippy missed; append-only ledger absorbs the correction; the lesson reinforces "use the real Clippy autopilot lifecycle" for future synthesis entries.

The Group 4 retro-validation sub-agent report explicitly flagged the test-file count + runtime-module count as basis-caveat false-Cite class. The retro-validation Plan A protocol fired exactly the gate that pre-lock `clippy:reviewer` would have fired had D62/D63 been authored through the autopilot lifecycle. Lesson: synthesis-class entries (D34 / D35 / D62 / D63) — which inventory state at lock-time — are HIGH-risk for count-drift between header summaries and body enumerations because the entry-author drafts both sides of the entry from different working memories; the basis-caveat block should be sourced from the SAME enumeration that body §B carries, not re-asserted from synthesis recall.

**Recursive lesson — D67 attempt 1 carried its own self-applicability violation**: The first draft of D67 (attempt 1) treated the validator-module count as "stands as written if `modules` includes `__init__.py`; flagged for transparency only" — itself a false-Cite on the validator-directory listing (8 entries, not 7) AND a missed false-Cite on D63's own basis-caveat verification claim. `clippy:reviewer` (attempt 2 fix-mode invocation) caught the recursion: D67 — the entry written to correct false-Cites — carried a fresh false-Cite of exactly the same class in its OWN basis-caveats and §A row. The discipline empirically holds: pre-lock `clippy:reviewer` catches recursive false-Cite even in entries authored to correct false-Cites. The lesson reinforces "use the real `clippy:autopilot` lifecycle" — the discipline correction is itself subject to the discipline; the lifecycle catches the recursion. Self-applicability is non-trivial: an entry CAN violate the very rule it codifies, and only an outside-fresh-context reviewer reliably surfaces that violation.

## C. Impl follow-through

NONE — pure ledger clarification; no impl change. Tests baseline 229 pre + post D67 lock (lock-time impl state is `a694caa` HEAD; D67 adds no runtime / test code).

## D. Defers

NONE — small clarification entry; no Phase C/D concerns surfaced.

## E. Pre-lock probe disposition

**SKIPPED** per `probing.md` Procedure 3 refined skip rule + D49 + D60 + D61 SKIP precedent. D67 is pure clarification — no new contract content, no new typed exception, no new category vocabulary, no new sub-procedure. It corrects locked-entry drift via append-only ledger. D49 is the canonical precedent (same shape: clarifies prior locked entries with corrections); D60 + D61 are further SKIP-on-clarifies precedents. The Group 4 retro-validation sub-agent finding already played the probe role for D67 — surfacing the drift class before D67 was drafted is structurally equivalent to a pre-lock probe firing.

## Decision-shape template self-application

- **WHAT**: lock count corrections for D62 + D63 lock-time drift; convert false-verified basis-caveat claims into Flagged-and-corrected per Cite-or-Read-or-Flag recovery path. Headers / synthesis lines / basis-caveats in the source entries stand textually (append-only); readers cross-reference D67 for the corrected counts.
- **WHO**: enforced by *opaque (documentary)* at framework-core (ledger correction; no runtime contract; no schema change; no validator change).
- **FAILS** (recursive — what happens if synthesis entries continue to drift if D67 is not the last correction?): *Detection*: retroactive `clippy:reviewer` pass (Group 4 retro-validation Plan A protocol). *Surface*: false-Cite findings on basis-caveat blocks. *Recovery*: append-only clarifies entries per D49 / D67 precedent. Long-term fix: use real `clippy:autopilot` lifecycle for synthesis-class entries (not just for substantive cluster supersedes), so `clippy:reviewer` fires pre-lock instead of retroactively.
- **CROSS**: D34 (Phase A refinement output; synthesis-entry shape — analog precedent); D35 (Phase A closure; analog precedent for D63 shape); D49 (clarifies-entry shape precedent for correcting locked entries via append-only — D67 follows this shape exactly); D60 + D61 (clarifies-entry SKIP precedent); D62 (clarified — Bref output synthesis); D63 (clarified — Phase B closure synthesis); README session-start step 5 HARD RULE (Cite-or-Read-or-Flag canonical discipline statement); global CLAUDE.md §"Honesty about sources" + §"Cite-or-Read-or-Flag" (canonical discipline statement); session retro-validation Plan A protocol (Group 4 retro-reviewer finding source).
- **DEFERS**: per §D — NONE.

## Rationale

Synthesis-class entries (D34 / D35 / D62 / D63) carry inventory counts that are honest snapshots at lock-time. Drift between header counts and body enumerations is a class of failure that pre-lock `clippy:reviewer` would catch (Group 4 retro empirically demonstrated). The canonical AI failure mode the Cite-or-Read-or-Flag discipline is designed to catch — claiming verification of N items without actual verification — is exactly what slipped through in D62/D63 basis-caveats.

Per append-only ledger discipline (README "Operating disciplines" + CLIPPY-COMPANION §"Append-only ledger"): D67 doesn't edit D62/D63 substance; clarifies via cross-reference. Readers cross-referencing D62/D63 against actual lock-time state can find D67 in `decisions.md` index + apply the corrections. The body enumerations in D62/D63 §B remain authoritative; D67's value is the explicit acknowledgment + correction of the basis-caveat false-Cite class.

Lesson for forward work: use the real `clippy:autopilot` lifecycle for synthesis entries (not only for substantive cluster supersedes). Reviewer at lock-time catches what self-review misses. The retro-validation pass is recoverable; the better operational answer is to put the gate at lock-time, not retroactively.

D67 is itself a synthesis-class entry. Its own basis-caveats are subject to the same discipline mechanism it corrects. Self-applicability is non-trivial — D67 attempt 1 carried a recursive false-Cite (validator-directory verification claim) of exactly the class D67 is authored to correct. `clippy:reviewer` (fix-mode attempt 2) caught it; the counts cited in §A are now re-grounded via direct `git ls-tree` on the lock-time blob with the false-Cite class explicitly catalogued (test files + runtime modules + validator basis-caveat).

**Cross-references**: D34 (Phase A refinement output; synthesis-entry shape precedent); D35 (Phase A closure; analog precedent for D63); D49 (clarifies-entry shape; corrects D47 + D48 via append-only; D67 follows this shape exactly); D60 + D61 (clarifies-entry SKIP precedent); D62 (clarified — Bref output workstream synthesis; drift in §A line 9 + §E line 70 + basis-caveat line 98 + headline line 3); D63 (clarified — Phase B closure synthesis; drift in §A line 7 + §B lines 17 + 20 + 23 + basis-caveat line 110); README session-start step 5 HARD RULE (Cite-or-Read-or-Flag); global CLAUDE.md §"Honesty about sources" + §"Cite-or-Read-or-Flag" (canonical discipline statement); session retro-validation Plan A protocol (Group 4 retro-reviewer finding source — see `.ai/tasks/` Group 4 sub-agent transcript for the original finding).

## Honest basis caveats

- **Read directly this session**: D62 + D63 entries (full); D49 + D60 + D61 (full for precedent); D34 + D35 (Phase A analog precedents); README session-start step 5 wording; `git ls-tree -r 60eb310 -- fresh-plan/impl/tests/` (verified 28 `test_*.py` files at lock-time); `git ls-tree -r 60eb310 -- fresh-plan/impl/src/fresh_plan/runtime/` (verified 14 entries including `__init__.py`; 13 substantive runtime modules); `git ls-tree -r 60eb310 -- fresh-plan/impl/src/fresh_plan/validator/` returns **8 entries** (1 `__init__.py` + 7 substantive: workspace.py, checks.py, dependency.py, extensions.py, schemas.py, types.py, shape_migration.py) — D63 body claim of 7 substantive modules stands ✓; D63 basis-caveat false-Cite on "7 entries verified" (claimed verification against 8-entry directory); `decisions.md` index for D-entry order; D49 SKIP rationale wording; `pytest -q` baseline 229 pass at HEAD `a694caa`.
- **Verified via direct git evidence**: 28 test files at lock-time (not 32); 13 runtime modules excluding `__init__.py` at lock-time (not 15); validator directory carries 8 entries (1 `__init__.py` + 7 substantive) at lock-time — D63 body claim "7 validator modules" is CORRECT substantively ✓ (names match the 7 substantive entries); D63 basis-caveat "verified 7 entries" was FALSE-CITE (the directory listing has 8 entries; the "7" in basis-caveat conflates substantive-count with directory-listing-count); 218 pytest pass at lock-time (correct).
- **Inferred** (non-load-bearing): the specific drafting-process by which D62/D63 sub-agents computed counts independently of enumerations — grounded in the structural shape of both errors (header-vs-enumeration delta in both entries), not in any session-context record. The hypothesis that performative-Clippy bypassed `clippy:reviewer` is grounded in the Group 4 retro-validation sub-agent report framing, not in session-context direct observation of the original D62/D63 drafting session.
- **Meta-discipline note**: D67 IS itself a synthesis-class entry. Its OWN basis-caveats are subject to the same discipline mechanism it corrects. Self-applicability is non-trivial: D67 attempt 1 violated the rule by reporting "verified 7 validator entries including `__init__.py`" — itself a false-Cite (actual directory has 8 entries). `clippy:reviewer` (attempt 2 fix-mode) caught the recursion. The empirical lesson: the outside-fresh-context reviewer reliably catches false-Cite even in entries authored to correct false-Cites. Attempt-2 caveats above re-grounded against `git ls-tree -r 60eb310` directly; the 229-pytest baseline cited is verified against current HEAD, not against D62/D63 lock-time.
