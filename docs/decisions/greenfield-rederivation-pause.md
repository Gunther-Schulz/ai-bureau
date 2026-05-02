# Decision record: Greenfield re-derivation pause (Phase 3 procedural-laxness response)

## Status

PROPOSED — procedure locked pending user approval; execution log + findings populate as work proceeds; Status amends to ACCEPTED-WITH-FINDINGS or ACCEPTED-VALIDATED upon execution completion + decision per Step 7.

## Owner

Phase 3 procedural-fidelity META-failure response; coordinates with `DISCIPLINES.md` Discipline 10 (greenfield evaluation of archived material) + hook deployment (`plugin/hooks/architectural_commit_gate.py`) + 3-layer execution-fidelity defense locked session 16.

## Related

- `docs/decisions/substrate-arch-topic.md` (REVISION-1 retroactive greenfield-pass record per Discipline 10; commit `a602dc7`)
- `DISCIPLINES.md` Discipline 10 (greenfield evaluation of archived material)
- `drafts/execution-fidelity.md` (META-framework concern; this pause IS the structural escalation when procedural defense recurs)
- `docs/decisions/doc-organization-templates.md` (DR template + arch/<topic>.md template; both locked sources need greenfield-evaluation)
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE (Pattern A vs B vs C framework; locked pre-Phase-3.4 — needs greenfield-evaluation)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 (preliminary-lock; everything except VISION axes is revisable)
- `plugin/hooks/architectural_commit_gate.py` (continues firing on architectural-artifact writes during execution)

## Context

Session-16 retroactive greenfield-pass on HIGH-risk Phase 3.4 topics (substrate + audit; per Discipline 10) yielded 1 architectural REVISION (substrate.md §10 boot/shutdown contradicted audit.md §11; cross-topic-cascade-miss). User flagged broader concern: "we are trying to build the framework from scratch treating the archive as a loose resource. I feel like this whole process has been too much relying on the archive in the past, otherwise this situation wouldn't have arisen."

User direction: "let's take stock for a moment before continuing... if you look what we have as a whole (full ARCH set, full glossary) what would you do different? what are the gaps? really take your time here. there is a chance we need to invalidate all work, do not consider sunk-cost."

Per AI honest stock-taking response (chat; this DR's context):

**Tier 1: HIGH RISK FOUNDATIONAL** — could invalidate substantial work:
- Pattern A protocol topic 18-section template anchored on substrate's cargo-culted shape
- 8 Pattern A protocols list (substrate / adapter / sparring / audit / coordination / trust / time / quality-gate) inherits archive's protocol categorization
- Pattern A vs Pattern B vs Pattern C three-pattern framework may be archive-influenced
- Phase 3.2 topic taxonomy (14-topic catalog) locked predates Discipline 10

**Tier 2: MEDIUM RISK STRUCTURAL** — cascade fixes:
- Phase 3.1 4 decisions may have cross-topic-cascade-miss (analogous to substrate REVISION-1)
- Sparring 8-sub-mechanism count from archive (7 + selective-friction)
- Profile validation depth shallow with skeleton profiles
- GLOSSARY entries (Phase 2; 35 locked) lack per-element greenfield-evaluation

**Tier 3: PROCESS** — improvements:
- Discipline 10 should have been Discipline 1 from session-16 launch
- Hook should have deployed at session-16 launch
- Archive cross-references should flag "consult-with-skepticism" by default

**Tier 4: GAPS** — architectural concerns not yet addressed:
- Concrete orchestrator mechanics (per-skill routing; multi-skill coordination)
- Onboarding pathway / template-instantiation UX (L4a deployer scenarios)
- Federation / Tier 3 specifics (cross-node A2A; trust handshake)
- Multi-VISION model (Phase 3.7)
- Markdown-validation feasibility (Phase 3.7)
- Marketplace / OSS distribution mechanics
- Per-shape policy bundle SCHEMA

This DR captures the procedure to investigate Tier 1 + Tier 2 concerns greenfield. Tier 3 + Tier 4 surface as cross-cutting findings.

## Decision

Pause Phase 3.4 work (5 remaining Pattern A protocol topics: coordination / trust / time + audit + ?? + quality-gate at 3.6 + adapter remaining elements). Execute 7-step greenfield re-derivation procedure (below). Resume Phase 3.4 only after Step 7 decision committed.

Hook (`architectural_commit_gate.py`) continues firing during execution; catches drift in real-time. Discipline 10 procedure applies per archive-citation throughout.

## Procedure (7 steps)

### Step 1: Re-read VISION + locked GLOSSARY in entirety

**Action**: full Read of `VISION.md` (~255 lines; anchored thesis; 3 axes; falsification) + `GLOSSARY.md` (~2300 lines; 35 locked entries).

**No summary-pattern-matching.** Per `DISCIPLINES.md` Discipline 1 source-grounded rule + Discipline 10 (archive is INPUT not template — applies at corpus level): VISION + GLOSSARY are first-class sources that ground every subsequent derivation.

**Verification**: chat output cites specific VISION line numbers + specific GLOSSARY entry sections during Steps 2-4.

**Output**: full VISION + GLOSSARY content in working context; no derivation done yet.

### Step 2: Greenfield-derive Pattern A vs B vs C primitive-classification framework

**Action**: ignoring `MAINTENANCE.md` current TOP-LEVEL ARCHITECTURE locked Pattern A/B/C framework, derive from scratch:
- From VISION axes (intertwining / sparring / authorship preservation) + falsification framing + structural primitives mention
- From 35 GLOSSARY primitives' classifications (PRIMITIVE / META-PRIMITIVE / DERIVED / SCOPE-CLASSIFICATION) + multi-aspect tagging (single / bipartite / tri-aspect)
- What primitive-classification framework emerges?

**Stress-test**:
- Are 3 patterns (A pluggable / B bipartite / C cross-cutting) the right framing?
- Could 2 patterns suffice (A + B, with C subsumed under B as singleton-bipartite)?
- Could N patterns be needed (e.g., add pattern for Layer A content classification)?

**Output**:
- Greenfield-derived classification framework
- Comparison table: current Pattern A/B/C vs greenfield framework
- Greenfield verdict per current pattern: GREENFIELD-EQUIVALENT / NEEDS-REVISION / NEEDS-REWORK

### Step 3: Greenfield-derive Pattern A protocol list

**Action**: From VISION + GLOSSARY (output of Step 1 + 2), derive: which protocols emerge as distinct Pattern A?

**Stress-test each current Pattern A protocol** (from Phase 3.2 topic catalog):
1. **substrate** — derives from VISION axis-1 (intertwining; AI-as-runtime) + locked GLOSSARY substrate entry (tri-aspect Pattern A; cross-axis runtime)
2. **adapter** — derives from external-integration concern (locked GLOSSARY adapter entry; internal-vs-external axis distinction from substrate)
3. **sparring** — derives from VISION axis-2 (sparring as load-bearing runtime mechanism)
4. **audit** — derives from cross-axis structural substrate (locked TOC §4) + axis-3 defensibility (reconstructible reasoning chain)
5. **coordination** — derives from? (UNCERTAIN; could be substrate hook system + audit event subscription)
6. **trust** — derives from? (UNCERTAIN; could be substrate permission flow + audit)
7. **time** — derives from? (UNCERTAIN; could be substrate scheduling + adapter time-driven operations)
8. **quality-gate** — derives from per-axis runtime observability concern

For each: does it derive from VISION-axis-mechanism need OR locked GLOSSARY primitive composes-with? Or is it archive-derived without independent grounding?

**Output**:
- Greenfield-derived Pattern A protocol list (count: TBD)
- Comparison to current 8-protocol catalog
- Per protocol verdict: GREENFIELD-DERIVED-DISTINCT-PROTOCOL / SUBSUMED-IN-OTHER (with named composition target) / ARCHIVE-CARGO-CULT (no greenfield grounding)

### Step 4: Greenfield-derive Pattern A protocol topic template

**Action**: From Pattern A definition (Step 2 output) + locked architectural disciplines + locked DR template + greenfield-derived protocol list (Step 3): what minimal common topic structure derives?

**Stress-test current 18-section template**:
- Which sections are STRUCTURALLY-REQUIRED by Pattern A definition (Surface + Implementations + Selection)?
- Which sections are PROTOCOL-SPECIFIC (apply only to certain protocols based on their nature)?
- Which sections were INHERITED from substrate's archive-shaped structure without architectural grounding?

**Specific stress-tests**:
- §10 Boot/shutdown ordering — required for substrate (runtime); applicable to audit (boot-before-substrate); less applicable to sparring / adapter (different lifecycle shape)
- §11 Error categories — applicable to all but per-protocol semantics differ
- §12 Transport variation — substrate-specific (MCP transport); not adapter (per-class shape) or sparring (no transport)
- §13 Deployment-tier awareness — substrate-specific
- §8 Substrate-internal vs skill-side audit emission — substrate-specific concept; other protocols compose with audit but don't have substrate-internal emission

**Output**:
- Greenfield-derived template structure: minimal common-required + per-protocol-extended
- Comparison to current 18-section template
- Verdict: which sections drop / merge / move-to-per-protocol

### Step 5: Compare to current locked work

**Action**: Apply outputs from Steps 2-4 against current locked work:
- `arch/substrate.md` + `substrate-arch-topic.md` DR (already audited; REVISION-1 applied per commit `a602dc7`)
- `arch/adapter.md` + `adapter-arch-topic.md` DR
- `arch/sparring.md` + `sparring-arch-topic.md` DR
- `arch/audit.md` + `audit-arch-topic.md` DR
- Phase 3.2 topic catalog in `ARCHITECTURE.md` §4 + `phase-3-2-doc-organization.md` DR
- Phase 3.1 4 decisions: workflow-bipartite / work-unit-bipartite / deployment-derived / engaged-authorship-operational

**Per element verdict**:
- **GREENFIELD-EQUIVALENT** — locked work matches what greenfield process produces (no revision needed)
- **NEEDS-REVISION** — cargo-culted; specific revision identified
- **NEEDS-REWORK** — foundationally drifted; substantial redo

### Step 6: Surface revisions

**Action**: organize Step 5 findings into tiered revision list:

**Tier 1 (foundational; cascades affect multiple ARCH topics)**:
- Pattern A vs B vs C framework revisions
- 8 Pattern A protocol list revisions (subsume / split / drop)
- Pattern A protocol topic template revisions

**Tier 2 (per-topic)**:
- Per-topic revisions in substrate / adapter / sparring / audit (beyond REVISION-1 already applied to substrate)

**Tier 3 (Phase 3.2 + 3.1)**:
- Topic catalog revisions
- Phase 3.1 4 decision revisions

**For each finding**: cite source-grounded evidence + greenfield-derivation chain.

### Step 7: Decide

**Action**: per Tier finding, commit to one of:
- **REVISE FOUNDATIONS + CASCADE** — apply revision to locked work; cascade to all dependent docs in same commit (or tightly-coupled sequence per `MAINTENANCE.md` cascade discipline)
- **VALIDATE GREENFIELD-EQUIVALENT** — locked work passes greenfield check; continue with confidence

**Decision criteria per Tier**:
- Tier 1 revisions trigger Phase 3.4 redo of substrate / adapter / sparring / audit (cascade-aware)
- Tier 2 revisions trigger per-topic amendments
- Tier 3 revisions trigger ARCHITECTURE.md catalog updates + Phase 3.1 DR amendments

**Resume signal**: Step 7 decisions committed → Phase 3.4 work resumes (coordination Round 1 redo + remaining 3 topics) under strengthened discipline (Discipline 10 + hook + Round 1 termination checklist).

## Anti-patterns to avoid during execution

Per `drafts/execution-fidelity.md` disguises catalog + lessons from session-16 META-failure recurrence:

| Anti-pattern | Counter-mechanism |
|---|---|
| Pattern-matching from substrate / adapter / sparring / audit content already in context (RISK: current ARCH topic shape contaminates greenfield derivation) | Step 1 mandatory full Re-Read of VISION + GLOSSARY refreshes context; subsequent steps must cite VISION/GLOSSARY explicitly per derivation claim |
| Self-validation bias on "current locked work matches greenfield" | Stress-test per element: explicitly enumerate greenfield-derivation chain BEFORE checking match against locked work |
| Skipping stress-tests on uncomfortable findings | Manufactured-criticism check inverted: if a finding is uncomfortable (would invalidate substantial work), apply EXTRA scrutiny vs less |
| Shortcut to "validate greenfield-equivalent" verdict | Step 5 verdict requires explicit greenfield-derivation chain cited per element; "looks similar" insufficient |
| Confirmation bias from prior 0-REVISION metrics | Substrate audit yielded 1 REVISION despite earlier 0-REVISION metric; metric proven misleading; ignore prior verdicts |

## Sharpening provenance

This DR is procedure-locking, not architectural-decision-locking. Sharpening light:

**Round 1**: AI surfaced 7-step procedure responding to user's explicit list. Acknowledged worry validated (1 REVISION found in substrate audit). Tiered analysis (Tier 1-4) presented; user authorized procedure documentation pre-execution.

**Round 2**: NOT applicable (procedure-locking; user explicitly requested write-out before execution; sharpening fires per-step DURING execution per Step 6 revision-surfacing).

**GLOSSARY back-check**: NOT applicable at procedure-lock-time; fires at execution end per Step 6 findings.

**Profile-anchored validation**: NOT applicable to procedure itself; applies to per-element greenfield-derivation in Step 2-4.

## Composition with existing architecture

- Discipline 10 procedure (per `DISCIPLINES.md`) applies at corpus level here (vs per-element in normal sharpening rounds)
- Discipline 1 source-grounded rule applies during Steps 1, 5 (cite file:line; flag synthesis vs citation)
- Discipline 9 coherence-audit cadence: this work is mid-Phase audit (between C1 cadence checkpoints; could be considered partial-C1-execution-now-on-foundations)
- Hook (`architectural_commit_gate.py`) continues firing during execution; catches drift on architectural-artifact writes
- DR template (per `MAINTENANCE.md` Layer 4 description) + arch/<topic>.md template (per Layer 3) — both are SUBJECTS of this audit, not just procedural framings

## Constraints flowing to downstream commitments

### → Phase 3.4 paused

5 remaining Pattern A protocol topics + arch/coordination.md Round 1 redo all paused until Step 7 decisions committed.

### → Hook fires + checklist applies during execution

Hook continues firing on architectural-artifact writes (`arch/*.md` / `docs/decisions/*.md` / etc.). Round 1 termination checklist (per `decision-design-sharpening` v0.7.0) applies to any sharpening rounds that fire during execution (none expected; this is corpus-audit not within-decision sharpening).

### → Possible cascade-aware redo (worst case)

If Step 7 yields Tier 1 revisions: substrate / adapter / sparring / audit ARCH topics + DRs may need substantial redo (cascade-aware sequence). HANDOFF Note documents redo trajectory.

### → Best case: validation + resume

If Step 7 yields all-validated: Phase 3.4 resumes with high confidence; remaining 3 Pattern A protocol topics (coordination / trust / time) + adapter incremental + quality-gate (3.6) proceed under strengthened discipline.

## Files touched

This commit:
- `docs/decisions/greenfield-rederivation-pause.md` (NEW; this file; status PROPOSED)
- `HANDOFF.md` (Note 41: pause + procedure + execution starts after user approval)

Future commits (per execution):
- This DR amended at end of each Step (execution log section)
- Final commit at Step 7: status PROPOSED → ACCEPTED-VALIDATED or ACCEPTED-WITH-FINDINGS; findings + decisions documented
- If revisions: cascade commits per affected topic / DR / GLOSSARY

## Revisit triggers

- Procedure executed → DR amended with findings + decisions
- User-triggered re-execution if Step 7 findings ambiguous
- Phase 3.8 C3 audit (per `DISCIPLINES.md` Discipline 9) may revisit findings as part of comprehensive corpus audit
- New procedural-fidelity META-failure recurrence → escalate beyond hook (additional structural enforcement)
- Tier 4 gaps may trigger separate watch-list / Phase routing

## Execution log

(populated as work proceeds)

### Step 1: Re-read VISION + locked GLOSSARY

(pending)

### Step 2: Greenfield-derive Pattern A vs B vs C framework

(pending)

### Step 3: Greenfield-derive Pattern A protocol list

(pending)

### Step 4: Greenfield-derive Pattern A protocol topic template

(pending)

### Step 5: Compare to current locked work

(pending)

### Step 6: Surface revisions

(pending)

### Step 7: Decide

(pending)

## Findings

(populated at execution end; per-Tier verdict per element)

## Decisions

(populated at execution end; revise-foundations vs validate-greenfield-equivalent per Tier)
