# D66 — 2026-05-17 — Roadmap deliverable #20 — PreToolUse hook for grounded-reads discipline structural enforcement

**Decision (substantive; new framework-development plugin component)**: Close Roadmap deliverable #20 by landing a PreToolUse hook (`fresh-plan/plugin/hooks/fresh_plan_grounding_gate.py`) that blocks Edit/Write/MultiEdit on substantive fresh-plan artifacts unless required preparatory Reads (`fresh-plan/CLIPPY-COMPANION.md` + `fresh-plan/probing.md`) happened in the current session. Hook adapts the pbs-bureau parent `plugin/hooks/architectural_commit_gate.py` to fresh-plan path patterns and a narrowed single check (required-Reads freshness via whole-session transcript scan). Structural backstop for README session-start step 5 HARD RULE (Cite-or-Read-or-Flag); deterministic enforcement per Anthropic engineering guidance.

## A. Scope of cluster

ONE path: structural enforcement of grounded-reads discipline at the Edit/Write boundary for substantive fresh-plan artifacts.

In scope:

- **Substantive artifact path patterns** (block on Edit/Write/MultiEdit):
  - `fresh-plan/decisions/D<NN>-*.md` — append-only ledger entries
  - `fresh-plan/impl/src/**/*.py` — runtime impl code
  - `fresh-plan/schemas/*.json` — formal schemas
- **Required Reads** (must appear in current session transcript): `fresh-plan/CLIPPY-COMPANION.md` + `fresh-plan/probing.md`
- **Freshness window**: whole-session transcript scan (main + sibling sub-agent transcripts), mirroring `architectural_commit_gate.py` rationale (no call-count window; sub-agent Reads count for freshness)
- **Plugin tree** lives at `fresh-plan/plugin/` (parallel to `fresh-plan/impl/` + `fresh-plan/decisions/`); fresh-plan-clippy branch only per C1 branch isolation
- **Roadmap deliverable #20** closure: row status → DONE with reference to this D-entry

Out of scope (see §D for explicit deferrals).

Cross-references:
- `fresh-plan/README.md` session-start step 5 (HARD RULE — Cite-or-Read-or-Flag) + step 6 (the line that already names this hook as the "Tracked structural backstop" for the HARD RULE).
- `fresh-plan/CLIPPY-COMPANION.md` D-entry shape template.
- `fresh-plan/probing.md` §"Investigation-before-claim discipline".
- pbs-bureau `plugin/hooks/architectural_commit_gate.py` (368 LOC; 4 checks) — parent reference; D66 narrows to 1 check.
- pbs-bureau `plugin/.claude-plugin/plugin.json` — parent plugin manifest mirrored.

## B. Substantive content — detection-surface-recovery applied to the hook itself

The hook IS a runtime decision (it fires on every Edit/Write/MultiEdit); per D45 it carries the detection-surface-recovery triad.

| Triad element | Lock |
|---|---|
| **Detection** | Hook fires on Edit/Write/MultiEdit (matcher `"Edit\|Write\|MultiEdit"` in plugin.json). Validates `tool_input.file_path` against `SUBSTANTIVE_PATTERNS` (3 regexes). For matching paths, aggregates main-session transcript + sibling sub-agent transcripts and extracts all Read `file_path` arguments via `extract_read_paths`. Checks each `REQUIRED_READS` entry against the aggregated session-read list using suffix-matching (`path_matches`). Whole-session scan strategy mirrors `architectural_commit_gate.py` (no call-count window — prep Reads done at session start get pushed out of fixed-size windows during long cascades). |
| **Surface** | When any required Read is missing: hook prints a structured block message to stderr listing each missing Read by path, names the discipline source (`README.md` step 5 HARD RULE + CLIPPY-COMPANION.md + probing.md), and exits with code 2. Claude Code displays the stderr text as the tool-failure block reason; the AI sees the explicit "Missing Reads:" list with resolve-by instructions. When all required Reads present: exit 0 (silent pass). |
| **Recovery** | The AI invokes the Read tool against each named missing file, then retries the original Edit/Write. The whole-session scan picks up the new Reads on retry. No state mutation; hook is idempotent at the same write-payload. For non-substantive paths or non-Edit/Write/MultiEdit tools: hook returns 0 immediately (no false-positive load on routine work). |

## C. Impl follow-through (landed atomically with this D-entry per [design+impl] criterion)

Files created:

- `fresh-plan/plugin/.claude-plugin/plugin.json` (~30 lines) — PreToolUse hook registration; mirrors pbs-bureau parent plugin.json structure with fresh-plan-specific name + description + hook command path.
- `fresh-plan/plugin/hooks/__init__.py` (empty) — package marker.
- `fresh-plan/plugin/hooks/fresh_plan_grounding_gate.py` (~212 LOC including docstrings) — adapted from `plugin/hooks/architectural_commit_gate.py`; replaces `ARCHITECTURAL_PATTERNS` with `SUBSTANTIVE_PATTERNS`, replaces `REQUIRED_SKILL` + `REQUIRED_PROFILE_INDEX` + `PROFILE_GLOB_PATTERN` with `REQUIRED_READS`, removes profile-anchored validation (parent Check 2), archive-citation cross-check (parent Check 3), and provenance-hygiene breadcrumb regex (parent Check 4 + `BREADCRUMB_PATTERNS` + `find_breadcrumbs`). Keeps `extract_write_content` as defensive helper for future tightening (§D D-1). Single check: required-Reads freshness. Executable bit set (`chmod +x`).
- `fresh-plan/plugin/tests/__init__.py` (empty) — package marker.
- `fresh-plan/plugin/tests/test_grounding_gate.py` (3 subprocess tests) — invokes hook with synthetic stdin payload + tempfile transcript JSONL. Test 1: D-entry write with required Reads → exit 0. Test 2: D-entry write missing probing.md → exit 2 + stderr names probing.md. Test 3: impl/src write with empty transcript → exit 2 + stderr lists both missing Reads.

Roadmap row #20 status: NOT STARTED → DONE with reference to D66.
decisions.md index: append D66 row.

Test discipline:
- Plugin tests: `python3 -m unittest fresh-plan.plugin.tests.test_grounding_gate -v` → 3 passed.
- impl baseline preserved: `cd fresh-plan/impl && .venv/bin/python -m pytest -q` → 229 passed (unchanged; plugin tests are SEPARATE from impl pytest baseline per C4).

Activation note: hook is registered via plugin.json but does NOT auto-activate. Requires `/reload-plugins` to be picked up by Claude Code. This is the operational handoff; framework concern is just landing the tracked artifact.

## D. What is NOT in this decision (explicit deferrals)

- **D-1 (content-pattern checks)**: parent `architectural_commit_gate.py` Check 4 scans write content for narrative-breadcrumb regex patterns (session-N references, etc.). D66 omits this — fresh-plan corpus is younger and the natural-failure-mode patterns haven't surfaced as recurring. Defer to Phase C+ if recurring breadcrumb pollution surfaces. The `extract_write_content` helper is kept in the hook code as defensive scaffolding for this future tightening.
- **D-2 (per-write-type required-Reads granularity)**: e.g., D-entry citing D<N> in cross-references could require Read of D<N>.md; impl/src writes touching event_chain.py could require Read of D45 + relevant cluster supersedes. Defer to Phase C+ — current single REQUIRED_READS list is the conservative starting bar; finer granularity earns its keep only when natural-failure surfaces the gap.
- **D-3 (profile-cluster-style sub-check)**: parent Check 2 enforces ≥3 profile reads from `profiles/` cluster directory. fresh-plan has no profile concept (profiles are pbs-bureau-specific shape policy). N/A by design.
- **D-4 (performance under long sessions)**: whole-session transcript scan is O(transcript) per write. For multi-thousand-event transcripts, this could add measurable latency to every Edit/Write. Defer to Phase C+ if hot-path latency surfaces; mitigation would be event-count window with explicit head-vs-tail strategy.
- **D-5 (cross-branch portability)**: plugin lives on fresh-plan-clippy branch only per C1 branch isolation. Promotion to main / other branches is a separate decision; this entry locks fresh-plan-clippy-only scope.
- **D-6 (activation discipline)**: `/reload-plugins` is required after the plugin lands for Claude Code to pick up the hook. Operational note; not a framework concern. The fact that the plugin needs reload to fire is documented in §C activation note, not enforced by D66.

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: PreToolUse hook structurally enforces grounded-reads discipline at Edit/Write boundary for substantive fresh-plan artifacts; closes Roadmap deliverable #20.
- **WHO**: `framework-development tooling (out-of-band)` — Claude Code harness executes the hook per plugin.json registration; not framework-runtime layer. Analogous to pbs-bureau `architectural_commit_gate.py` which the harness executes, not the substrate.
- **FAILS**: Hook firing failures themselves fail open (return 0) — see `main()` exception handling for `json.JSONDecodeError` on stdin. Rationale: don't block AI work on hook bugs. Diagnostic: stderr block message names each missing Read + Resolve-by instruction; AI sees this as tool-failure block reason. Recovery: AI Reads the named files via Read tool, retries Edit/Write.
- **CROSS**: README.md session-start step 5 + step 6 (canonical discipline source); CLIPPY-COMPANION.md (D-entry shape template invoked by D66 itself); probing.md investigation-before-claim discipline (motivates the grounded-reads bar); pbs-bureau `plugin/hooks/architectural_commit_gate.py` (parent reference; same shape, narrower scope).
- **DEFERS**: per §D — content-pattern checks (D-1), per-write-type required-Reads granularity (D-2), profile-cluster sub-check (D-3 — N/A), perf optimization (D-4), cross-branch portability (D-5), activation discipline (D-6).

## E. Pre-lock probe disposition (per probing.md Procedure 3 refined-skip rule)

D66 **FIRED** the pre-lock probe per refined-skip rule + D48 §E + D50 §E + D52 §E precedent: D66 introduces NEW contract content (not pure pattern application).

The three new-contract elements:

1. **NEW plugin component** — first plugin under `fresh-plan/`; establishes the `fresh-plan/plugin/` directory layout convention. No prior fresh-plan plugin to pattern-extend.
2. **NEW hook semantics** — substantive-artifact gating (3 path patterns specific to fresh-plan). Distinct from parent `architectural_commit_gate.py` which targets pbs-bureau Layer 0/1/2/3 architectural artifacts. The path-pattern set is a new contract.
3. **NEW required-Reads contract** — `REQUIRED_READS = [CLIPPY-COMPANION.md, probing.md]`. Distinct from parent's `REQUIRED_SKILL = decision-design-sharpening/SKILL.md`. New discipline-source mapping.

Probe outcome (in-line during draft, this session 2026-05-17): code claims verified by direct Read of parent `architectural_commit_gate.py` (368 LOC; 4 checks; whole-session scan rationale at lines 36-46), parent `plugin.json` (PreToolUse matcher + command structure), `CLIPPY-COMPANION.md` (D-entry shape template), `probing.md` (investigation-before-claim discipline + Procedure 3 refined-skip rule), `README.md` line 14 (existing "Tracked structural backstop" reference to this hook). 6 quiet assumptions surfaced + named as explicit DEFERS in §D D-1 through D-6 (content-pattern checks; per-write-type granularity; profile-cluster N/A; perf; cross-branch portability; activation discipline).

This pattern continues the FIRED disposition for entries with new contract content (D48 §E + D50 §E + D52 §E precedent).

## Rationale

The 2026-05-12 sketch-without-grounding incident is the canonical motivating instance: AI drafted substantive D-entry content (D47 §B.3 `HookRegistry.fire` API claim) by pattern-completion from common variadic API shape without Reading `hooks.py` first. The actual API is `fire(name, context: dict)`. The mistake was caught at impl-planning time by user intervention, not by any codified discipline.

The discipline lives at README.md session-start step 5 (HARD RULE — Cite-or-Read-or-Flag) + step 6 (which already names this hook as the "Tracked structural backstop"). Prose rules empirically drift across sessions; the canonical AI failure mode is exactly the kind of insufficient-context-reading that step 5 targets. Per Anthropic engineering guidance: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." This D-entry lands the structural backstop.

A second motivating data point surfaced during this autopilot session itself: D52 → D63 admission revealed that performative-Clippy executions bypassed clippy:reviewer fresh-context verification. The grounded-reads bar is exactly the discipline that catches pattern-completion masquerading as verified-claim; the hook is the structural floor for that discipline at the write boundary.

Design choice — narrow to 1 check vs port all 4 checks from parent:
- **Pro (single check)**: smallest viable backstop; the recurring failure mode is missing-Reads, not pollution-in-content; tighten later when natural-failure surfaces the next gap.
- **Con (single check)**: leaves content-pattern, citation cross-check, and profile-cluster gaps open; would catch fewer failure modes than parent.
- **Net**: the canonical failure mode (insufficient-context-Read) maps to the single check that lands. Pollution patterns + citation drift + profile-validation are deferred per §D until natural-failure surfaces.

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): D66 is **framework-development tooling** — not framework-core. The hook protects the integrity of the dev process (grounded-reads discipline); it does not become a framework runtime kind. Lives at `fresh-plan/plugin/` parallel to `fresh-plan/impl/`. Promotion or deletion is operational; framework-core stays untouched.

**Cross-references**: README.md session-start step 5 (HARD RULE — Cite-or-Read-or-Flag; canonical discipline source) + step 6 (the line that already named D66's hook as the "Tracked structural backstop" for the HARD RULE; this D-entry closes that loop); CLIPPY-COMPANION.md (D-entry shape template applied here); probing.md §"Investigation-before-claim discipline" (motivating discipline) + Procedure 3 refined-skip rule (D66 §E disposition); global CLAUDE.md §"Honesty about sources" (Cite-or-Read-or-Flag canonical source); pbs-bureau `plugin/hooks/architectural_commit_gate.py` (parent reference; D66 adapts its `read_transcript_events` + `gather_session_transcript_paths` + `extract_read_paths` + `normalize_path` + `path_matches` + `main()` structure); pbs-bureau `plugin/.claude-plugin/plugin.json` (parent plugin manifest mirrored); D45 (detection-surface-recovery triad standing requirement applied to the hook in §B); D48 §E + D50 §E + D52 §E (FIRED pre-lock probe precedent for new contract content); D49 first-pass scope-cardinality-honesty (D66 honors honest 1-path cluster scope, does not inflate to match parent's 4 checks); roadmap.md row #20 (Roadmap deliverable this D-entry closes).

## Honest basis caveats

Direct Reads this session (load-bearing for D66):
- `fresh-plan/CLIPPY-COMPANION.md` (full; for D-entry shape template + Sketch-then-lock + pre-lock probe rules)
- `fresh-plan/probing.md` (full; for Procedure 3 refined-skip rule + investigation-before-claim discipline + decision-shape template)
- `plugin/hooks/architectural_commit_gate.py` (full 368 LOC; for adaptation source)
- `plugin/.claude-plugin/plugin.json` (full 30 lines; for plugin manifest mirroring)
- `fresh-plan/decisions/D52-extends-d10-d13-d39-composition-change-cluster-honors-detection-surface-recovery.md` §E (FIRED pre-lock probe documentation pattern)
- `fresh-plan/roadmap.md` row #20 (existing wording; for status-update target)
- `fresh-plan/decisions.md` (full; for index conventions + last entry D65)
- `fresh-plan/README.md` step 5 + step 6 + line 14 (Cite-or-Read-or-Flag + Tracked structural backstop references)

Inferred-not-Read claims (flagged):
- Claude Code transcript JSONL session-scope semantics ("each transcript JSONL has a single sessionId across all events") — taken from parent `architectural_commit_gate.py` docstring lines 36-43, not independently verified against Claude Code source. The parent hook's behavior is well-established; this claim is inherited rather than re-verified.
- `/reload-plugins` activation requirement — taken from CLAUDE.md memory entry on plugin marketplace clone sync, not directly tested in this session for the new plugin tree.

No claims about the impl/src/ runtime or other Layer 2/3 artifacts in this D-entry; D66 lives at framework-development-tooling layer, parallel to fresh-plan's other dev artifacts.
