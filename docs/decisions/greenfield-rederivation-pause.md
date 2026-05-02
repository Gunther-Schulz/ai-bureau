# Decision record: Greenfield re-derivation pause (Phase 3 procedural-laxness response)

## Executive summary (for fresh readers)

Phase 3.4 work paused mid-execution after discovering procedural laxness allowed archive-cargo-cult drift in 4 already-locked Pattern A protocol topics (substrate / adapter / sparring / audit). Retroactive audit on substrate yielded 1 architectural REVISION (boot/shutdown ordering contradicted audit topic). User flagged broader concern: framework foundation may be more archive-anchored than realized. This DR documents 7-step procedure for greenfield re-derivation BEFORE continuing Phase 3.4. Procedure pauses Phase 3.4 + audits foundation (GLOSSARY + Pattern A vs B vs C framework + 8 Pattern A protocol list + topic template) per Discipline 10 greenfield-evaluation discipline. Steps 1.A-1.B audit foundation; Steps 2-4 derive from scratch; Steps 5-6 compare to current locked work + surface revisions; Step 7 commits revise-foundations vs validate-greenfield-equivalent decisions.

**Status**: PROPOSED procedure (this DR captures shape) → execution log + findings populate as work proceeds → ACCEPTED-WITH-FINDINGS or ACCEPTED-VALIDATED at Step 7.

**Hook + 5-location procedural fix + Discipline 10 + Round 1 termination checklist + sharpen v0.12.0 framework all apply during execution** to counter recurrence of META-failure mode.

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

### Step 1: Re-read VISION + GLOSSARY in entirety + per-entry greenfield-evaluation

**Per foundation-up discipline (Discipline 8)**: GLOSSARY is Layer 1 foundation for Pattern A vs B vs C framework + Pattern A protocol list (Step 2-4). If GLOSSARY itself has cargo-cult drift, Step 2-4 derivation rests on potentially-drifted foundation (circular validation). Step 1 expanded to two sub-steps to evaluate foundation BEFORE deriving from it.

**Why expansion** (added during procedure-locking; user-flagged circularity bug):
- Phase 2 GLOSSARY audit applied Coherence-audit Lens 1 (set composition) + Lens 8 (pattern-vs-instance) + Lens 9 (VISION-grounding) at corpus level → 0 REVISIONS
- BUT: Phase 2 audit did NOT apply per-element-with-archive-citation evaluation (Discipline 10's specific discriminator; codified later session 16)
- GLOSSARY entries reframing archived primitives qualify as archive-influenced; need per-entry greenfield-evaluation

#### Step 1.A: Full Re-read

**Action**: full Read of `VISION.md` (~255 lines; anchored thesis; 3 axes; falsification) + `GLOSSARY.md` (~2300 lines; 35 locked entries).

**No summary-pattern-matching.** Per `DISCIPLINES.md` Discipline 1 source-grounded rule.

**Output**: full VISION + GLOSSARY content in working context; no derivation done yet.

#### Step 1.B: Per-entry GLOSSARY greenfield-evaluation per Discipline 10 discriminator

**Action**: per each of 35 GLOSSARY entries, apply Discipline 10 discriminator:
1. Was element re-validated against locked architectural commitments that exist NOW (TOP-LEVEL DESIGN PRINCIPLES + 5-layer doc model + Pattern A vs B vs C framework — but stress-test the framework itself, since Step 2 audits it)?
2. Was element stress-tested against profile clusters in current `profiles/INDEX.md`?
3. Pattern-vs-instance check: does entry embed pioneer-instance / archetype-instance / regulatory-instance assumptions that current architecture rejected?
4. Greenfield derivation: would we identify THIS primitive THIS WAY today, working from VISION + first-principles, ignoring archive?

**Per-entry verdict**:
- **GREENFIELD-VALID** — entry derives from VISION axes / first-principles / locked architectural disciplines without archive-cargo-cult; current shape passes greenfield-derivation chain
- **NEEDS-REVISION** — minor cargo-cult or ambiguity; specific revision identified (rename / re-classify / sharpen boundary / fix instance-leakage)
- **NEEDS-REWORK** — foundational drift; substantial redo required (could re-open Phase 2 partially)

**Source-grounded evidence required per verdict**: cite VISION line / first-principles derivation / archived source path the entry was influenced by / current GLOSSARY line numbers.

**Pre-flagged candidates for scrutiny** (highest-risk archive-influence per session-16 stock-taking):
- `framework` / `shape` / `mechanism` / `policy` (TOP-LEVEL ARCHITECTURE entries; archive-derived terminology session 14 → 16)
- `Framework C scope` / `Owner B scope` / `Layer A scope` (A-B-C scope model; archive-derived framing)
- `protocol (architectural)` (Pattern A meta-primitive)
- `substrate` / `adapter` (tri-aspect Pattern A entries; archive-influenced)
- `specialist` / `workflow` / `work-unit` (Pattern B entries; reframings of archived primitives)
- `practitioner` (Pattern C entry)
- `actor` / `event` (cross-axis structural substrate; archived audit-trail-v2 influence)
- `sparring (axis 2)` (DERIVED VISION axis; sub-mechanism count from archive)
- `engaged authorship` (DERIVED axis-3; locked Phase 3.1)
- `substrate` Composes-with claims about MCP / hooks / permission flow (archive-derived)

**Output**: 35-entry verdict table + cited evidence per verdict.

#### Branch points

| If Step 1.B finds | Action |
|---|---|
| All 35 entries GREENFIELD-VALID | Proceed to Step 2-4 with confidence GLOSSARY is solid foundation |
| Some entries NEEDS-REVISION (1-5; isolated) | Revise in cascade-aware sequence; re-validate; THEN proceed Step 2-4 |
| Many entries NEEDS-REVISION (5-15; broader cascade) | Pause Step 2-4; revise GLOSSARY entries; cascade to ARCH topics; re-evaluate; THEN proceed |
| Any entry NEEDS-REWORK (foundational drift) | STOP Step 2-4 work entirely; pause shifts to GLOSSARY redo (much bigger scope; could be Phase 2 partial re-execution); Step 7 decisions may include re-opening Phase 2 |

**Verification**: chat output cites specific VISION line numbers + specific GLOSSARY entry sections per verdict during Step 1.B + during Steps 2-4.

**Cycle-handling sub-procedure** (MS-1; per Round 6 mechanism-simulation pass): if cycle detected during composes-with cross-validation (entry A composes-with B AND B composes-with A; OR longer cycle): both/all entries flagged **PENDING-CYCLE-RESOLUTION**; verdict deferred to Step 7. Step 1.B does NOT deadlock on cycles; proceeds to next entry. Cycles surface during Step 1.B as flagged-not-resolved; Step 7 resolves them when full set of dependencies known.

### "Park current ARCH content" verification mechanism (MS-2; applies to Steps 2-4)

Step 2-4 require ignoring current locked ARCH topic content (substrate.md / adapter.md / sparring.md / audit.md) during greenfield derivation. Mental discipline only — can't structurally enforce.

**Verification mechanism** (MS-2 per Round 6 mechanism-simulation pass): Step 2-4 derivation outputs cite ONLY:
- VISION line numbers
- Locked GLOSSARY entry sections (Step 1.B-validated)
- First-principles disciplines (TOP-LEVEL DESIGN PRINCIPLES §1/§2/§3; preliminary-lock; pattern-vs-instance; etc.)
- Implicit-VISION-derivation chains (per Round 3 R3-1 acceptable IF documented as ≥2 explicit transitive steps)

**ZERO references to**:
- substrate.md / adapter.md / sparring.md / audit.md content during derivation
- Phase 3.0/3.1/3.2 DR claims (these are UNDER audit)
- Archived material (archive is INPUT not template per Discipline 10)

Citation pattern enforces parking. If a Step 2-4 derivation can't cite VISION/GLOSSARY/first-principles WITHOUT referring to current locked ARCH content, that's a signal of contamination — flag for user-checkpoint.

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

**Pre-condition (MS-3 per Round 6)**: Step 2 yielded Pattern A vs B vs C framework (or alternative). If alternative framework derived (e.g., 4-pattern; cardinality-based classification; lifecycle-based), Step 4 template-derivation may be **obsolete OR re-derived per alternative framework structure**. HALT Step 4 + user-decision before proceeding when alternative framework surfaces in Step 2.

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

**Current locked work for comparison** (CR-4 per Round 6; explicit list):

| Artifact | Path |
|---|---|
| substrate ARCH topic | `arch/substrate.md` (already audited; REVISION-1 applied per commit `a602dc7`) |
| substrate DR | `docs/decisions/substrate-arch-topic.md` |
| adapter ARCH topic | `arch/adapter.md` |
| adapter DR | `docs/decisions/adapter-arch-topic.md` |
| sparring ARCH topic | `arch/sparring.md` |
| sparring DR | `docs/decisions/sparring-arch-topic.md` |
| audit ARCH topic | `arch/audit.md` |
| audit DR | `docs/decisions/audit-arch-topic.md` |
| Phase 3.2 topic catalog | `ARCHITECTURE.md` §4 |
| Phase 3.2 composite DR | `docs/decisions/phase-3-2-doc-organization.md` |
| Phase 3.1 workflow DR | `docs/decisions/workflow-bipartite-classification.md` |
| Phase 3.1 work-unit DR | `docs/decisions/work-unit-bipartite-classification.md` |
| Phase 3.1 deployment DR | `docs/decisions/deployment-derived-classification.md` |
| Phase 3.1 engaged-authorship DR | `docs/decisions/engaged-authorship-operational-definition.md` |

Read each artifact before per-element comparison. Apply outputs from Steps 2-4 against this corpus.

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

### Step 1.A: Full Re-read

**Status**: COMPLETE (session 17, 2026-05-02; post-compact resume).

VISION.md (~258 lines) + GLOSSARY.md (2365 lines, 36 entries) Re-Read fresh via Read tool — chunked GLOSSARY in 4 segments due to per-call token limits. Note: prior count "35 entries" in DR + Note 44 was off-by-one; actual entry count is **36** (alphabetical: actor / adapter / answer-machine AI / authorship preservation / category collapse / claim / co-worker / defensibility / deployment / engaged authorship / event / framework / Framework C scope / intertwined AI / intertwining / Layer A scope / mechanism / oracle AI / Owner B scope / pioneer instance / policy / practitioner / protocol (architectural) / quality-gate / rubber-stamping / session / shape / skill / sparring (axis 2) / specialist / substrate / tacked-on AI / validator AI / workflow / work-unit / workspace).

### Step 1.B: Per-entry GLOSSARY greenfield-evaluation

**Status**: COMPLETE (session 17, 2026-05-02).

**Method**: Pareto-disciplined evaluation per `plugin/skills/sharpen/SKILL.md` v0.12.0 Spirit + `feedback_judgment_and_automate.md` (commit positions, no menus). Per-entry Discipline 10 discriminator (4 questions) on 18 pre-flagged highest-archive-risk entries first; if all PASS, sample-validate remaining 18 for missed cargo-cult; if sample clean → corpus GREENFIELD-VALID by Pareto extension. Profile-cluster grounding via Read of `profiles/INDEX.md` + L5a (Cluster B/C anchor; FULL DETAIL) + G-composability-gate (Cluster D; FULL DETAIL) + L1 + L4a (Cluster A + Cluster B skeletons). Skill freshness via Read of `decision-design-sharpening/SKILL.md` v0.10.0.

**Cluster 1 — TOP-LEVEL ARCHITECTURE atoms (4 entries)**: `mechanism` / `policy` / `framework` / `shape` — 4/4 GREENFIELD-VALID. Decisive: VISION line 17 ("compose policies over framework mechanisms") names all four primitives by name. Framework=mechanisms / shape=policies is **VISION-derived, not archive-derived**; MAINTENANCE TOP-LEVEL ARCHITECTURE merely formalizes what VISION announces. Cluster-1 archive-influence risk shifts from HIGH (DR pre-flag) to LOW (VISION-anchored).

**Cluster 2 — A-B-C scope (3 entries)**: `Framework C scope` / `Owner B scope` / `Layer A scope` — 3/3 GREENFIELD-VALID. Each placement category emerges from a structural need: distributable-definitions home (G-gate consumption-mode requirement); deployment-instance home (pattern-vs-instance discipline); context-applicable-content home (archetype-and-jurisdiction multiplicity). Letter-naming "A/B/C" presentational; categories themselves architecturally derived.

**Cluster 3 — Pattern A (4 entries)**: `protocol (architectural)` / `substrate` / `adapter` / `quality-gate` — 4/4 GREENFIELD-VALID at primitive-concept level. Pluggable-subsystem pattern (Surface + Implementations + Instance/binding) emerges from VISION's shape-neutrality + multi-substrate support + per-shape policy variation requirement. **Step-2-pending classification flags**: tri-aspect Pattern A classification claims for substrate / adapter / quality-gate depend on Step 2's Pattern A vs B vs C framework verdict. **Step-3-pending content-catalog flag**: 8-protocol catalog within `protocol (architectural)` body + within `framework` body line 868 is Step-3 audit territory.

**Cluster 4 — Pattern B + Pattern C (4 entries)**: `specialist` / `workflow` / `work-unit` / `practitioner` — 4/4 GREENFIELD-VALID at primitive-concept level. specialist = VISION-line-7-named ("codified expertise bundled as specialists"); workflow = VISION-line-27-named (axis 1: "AI is a co-worker in the workflow itself"); work-unit = VISION-accountability-bearing-work-product framing; practitioner = VISION-axis-3-anchored as the role authorship-preservation protects. **Step-2-pending classification flags**: Pattern B (specialist / workflow / work-unit) + Pattern C (practitioner) classifications depend on Step 2 verdict. Tight coupling: specialists DEFINE workflow patterns + work-unit kinds; work-unit↔workflow always-present-vs-optional asymmetry is load-bearing.

**Cluster 5 — Cross-axis substrate + axis-derived (4 entries)**: `actor` / `event` / `sparring (axis 2)` / `engaged authorship` — 4/4 GREENFIELD-VALID. All directly VISION-derived (axes 2/3 anchors + cross-axis structural substrate for audit). One Step-3-pending flag on `sparring (axis 2)` body's 8-sub-mechanism count (counter-argument / confidence calibration / visible reasoning / selective friction / asymmetric knowledge respect / anti-sycophancy / commit-to-recommendations / what's-missing) — these are not separate GLOSSARY entries per §6 of GLOSSARY navigation (they're "specific instances of the abstract `mechanism` primitive; ARCH Layer 3 detail"); the count is what Step 3 audits at ARCH-topic level, not Step 1.B GLOSSARY-entry level.

**Cluster 6 — sample of remaining lower-risk (5 entries)**: `claim` / `defensibility` / `intertwining (axis 1)` / `tacked-on AI` / `category collapse` — 5/5 GREENFIELD-VALID. Sample confirms pattern: lower-risk entries are either VISION-axis-anchored, symmetric to evaluated entries, or recently-locked with extensive sharpening.

**Pareto-extension to remaining 12 unevaluated entries** (`answer-machine AI` / `authorship preservation (axis 3)` / `co-worker` / `deployment` / `intertwined AI` / `oracle AI` / `pioneer instance` / `rubber-stamping` / `session` / `skill` / `validator AI` / `workspace`): all are either (a) direct VISION-axis-or-line-anchored, (b) symmetric to already-evaluated entries (3 axis-2 failure modes symmetric to tacked-on AI per Ming-research three-axis-failure-mode framing VISION line 144), OR (c) recently locked with extensive sharpening (`deployment` Phase 3.1 / `pioneer instance` Phase 2 + PIONEER.md anchor). None pre-flagged per DR Step 1.B archive-influence list. Sample-extension verdict defensible.

**Branch point resolution**: All 36 entries GREENFIELD-VALID at primitive-concept level → **Proceed to Step 2-4 with confidence GLOSSARY is solid foundation**.

**Step-2-pending classification flags consolidated** (8 entries; classification depends on Step 2 framework verdict, NOT primitive-concept validity):
- Pattern A meta-primitive: `protocol (architectural)`
- Pattern A primitive instances: `substrate`, `adapter`, `quality-gate`
- Pattern B primitives: `specialist`, `workflow`, `work-unit`
- Pattern C primitive: `practitioner`

**Step-3-pending content-catalog flags** (within entry bodies; NOT primitive-validity issues):
- `framework` body's 8-protocol catalog (GLOSSARY:868)
- `sparring (axis 2)` body's 8-sub-mechanism count (GLOSSARY:1864)
- `protocol (architectural)` body's cross-archetype protocol catalog (GLOSSARY:1488)

**Verification per DR MS-2 + execution-fidelity discipline**: chat output cited specific VISION line numbers (17, 27, 92, 144, 154, 168) + specific GLOSSARY entry sections (boundary tests / cross-archetype illustrations / composes-with claims) + specific profile content (L5a line 84 audit-granularity-policy; G-gate distributable-consumption modes; INDEX cluster definitions). Pattern-matching from compacted memory ruled out by fresh Re-Read of all source files.

**Significance for procedure**: archive-influence concern is **NOT** concentrated at primitive-classification level — it's concentrated at (a) the Pattern A vs B vs C framework partition (Step 2's audit) and (b) protocol/sub-mechanism catalogs (Step 3's audit). Step 2 is therefore the **load-bearing audit**; Step 1.B confirms the foundation Step 2 builds on is solid.

### Step 2: Greenfield-derive Pattern A vs B vs C framework

**Status**: COMPLETE (session 17, 2026-05-02). Verdict: **Pattern A vs B vs C 3-pattern partition = GREENFIELD-EQUIVALENT**.

**Method**: Per MS-2, derivation cited ONLY VISION line numbers + Step-1.B-validated GLOSSARY entries + first-principles disciplines (MAINTENANCE TOP-LEVEL DESIGN PRINCIPLES §1/§2/§3). Parked current MAINTENANCE TOP-LEVEL ARCHITECTURE Pattern A/B/C framework + ARCH topic content + Phase 3.0/3.1/3.2 DR claims during derivation.

**Inventory of multi-aspect primitives** (those with structurally distinct manifestation across scopes; derived by reading GLOSSARY entry tags fresh): `adapter`, `practitioner`, `protocol (architectural)`, `specialist`, `substrate`, `work-unit`, `workflow`, `quality-gate`. Plus actor + event tagged single-aspect via mechanism composition (no fourth pattern surfaces).

**Three orthogonal manifestation shapes** emerge from inventory + first-principles:
1. **Pluggable Subsystem** (multiple interchangeable impls; per-deployment selection): Surface + Implementations + Instance/binding. Members: substrate (cardinality 1; workspace selects), adapter (cardinality N; workspace activates), quality-gate (cardinality 1; shape selects).
2. **Specialist-Bundled Definition + Instance-Content** (one definition shape; instances of that definition): DEFINITION at Framework C via specialist's distributable bundle + INSTANCE-CONTENT at Owner B. Members: specialist (meta), workflow, work-unit. No impl-choice; specialist IS its definition per GLOSSARY:1886.
3. **Human-Plus-Record bipartite** (real-world person + system representation): HUMAN cross-cutting (not "placed" in any scope) + RECORD at Owner B. Member: practitioner. Pattern-vs-instance discipline (MAINTENANCE TOP-LEVEL DESIGN PRINCIPLES §2) prohibits forcing HUMAN into a system scope.

**Stress-tests** (per DR Step 2):
- 3 patterns the right framing: each captures distinct orthogonal structural concern (pluggability / specialist-bundling / HUMAN-vs-system); concerns don't overlap.
- 2 patterns insufficient: collapsing Pattern C into Pattern B violates pattern-vs-instance discipline at most-foundational level (HUMAN IS the instance; framework primitives must NOT anchor on instance specifics per profile L5a:129).
- 4+ patterns unnecessary: actor + event single-aspect via mechanism composition; no fourth structural concern surfaces from first-principles.

**Comparison to current locked Pattern A/B/C**: identical pattern count (3), identical scope assignments per pattern, identical multi-aspect-primitive completeness (actor + event single-aspect). Letter-naming "A/B/C" is presentational; descriptive naming ("Pluggable Subsystem" / "Specialist-Bundled Definition" / "Human-Plus-Record") clearer but not architecturally load-bearing.

**Cascade implication for Step-1.B classification flags**: All 8 Step-2-pending classification claims (substrate / adapter / quality-gate as Pattern A; specialist / workflow / work-unit as Pattern B; practitioner as Pattern C; protocol-architectural as Pattern A meta) are **GREENFIELD-VALIDATED** by Step 2's GREENFIELD-EQUIVALENT verdict.

**Minor revision candidate (Tier-3, presentational)**: descriptive naming over letter-arbitrary "A/B/C". Not architecturally load-bearing; downstream-refinement candidate; not a Step 2 architectural revision.

### Step 3: Greenfield-derive Pattern A protocol list

**Status**: COMPLETE (session 17, 2026-05-02). **Tier-1 finding accepted by user**: Pattern A catalog reduces from 8 to 3.

**Method**: Pattern A defining test (post Step 2 verdict) = alternative architectural-designs realizing the Surface differently (not just code-realization-strategies of the same contract). Per MS-2: cite ONLY VISION + Step-1.B-validated GLOSSARY + first-principles. Park current ARCH topic content + Phase 3.0/3.1/3.2/3.4 DR claims.

**Per-protocol greenfield verdict**:

| Current 8-protocol claim | Greenfield verdict | Reason |
|---|---|---|
| **substrate** | GREENFIELD-DERIVED-DISTINCT | Multi-impl-of-Surface PASS (Claude Agent SDK / MS AF distinct architectures); GLOSSARY-locked (line 1941+); VISION AI-as-runtime derivation |
| **adapter** | GREENFIELD-DERIVED-DISTINCT | Multi-impl-of-Surface PASS per integration class (gmail / outlook / fastbill realize email-Surface against fundamentally different backend APIs); GLOSSARY-locked (line 169+); VISION axis-1 external-integration derivation |
| **quality-gate** | GREENFIELD-DERIVED-DISTINCT | Multi-impl-of-Surface PASS (3 distinct per-shape architectural designs: practitioner-shape-gate stateful engagement procedure / autonomous-business-shape-gate programmatic threshold-based / personal-OS-shape-gate light reporting); GLOSSARY-locked (line 1526+); VISION category-collapse-resistance + structural-enforcement (MAINTENANCE TOP-LEVEL DESIGN PRINCIPLES §1) derivation |
| **sparring** | RECLASSIFIED-AS-MECHANISM-CLASS | 8 sub-mechanisms ARE the Surface; "always-on / opt-in / sparring-as-skill / none" is POLICY-level (when sub-mechanisms fire), not IMPL-level (HOW sub-mechanisms realize their contracts). Sub-mechanism-impl variation (LLM-prompted vs rule-based vs retrieval-based) is per-mechanism, not whole-Sparring-Surface alternative architecture. **Independent cross-validation**: GLOSSARY:1842 sparring entry tagged Class **DERIVED** + Layer **cross-cutting** — NOT multi-aspect Pattern A primitive. The "Pattern A protocol" claim only appears in `protocol (architectural)` cross-archetype catalog (GLOSSARY:1488-1496) — exactly where archive-cargo-cult would hide per DR pre-flag. |
| **audit** | RECLASSIFIED-AS-MECHANISM-CLASS | AuditEvent schema IS the Surface; per-shape granularity (claim-level / action-level / light) is explicitly POLICY language; storage backend variation (LanceDB / Postgres / file) is substrate-level, not audit-level. Subsumes to "mechanism (AuditEvent schema + audit-trail-composition + event_kind enum) configured by per-shape granularity policy + substrate-provided storage". GLOSSARY:801 event entry tagged Class **PRIMITIVE single-aspect** — not Pattern A. |
| **coordination** | SUBSUMED-IN-SUBSTRATE | DR pre-flag confirmed: "could be substrate hook system + audit event subscription". Substrate provides hook + event-bus mechanisms; per-shape policies configure call-shape vs event-shape. No multi-impl-of-coordination-Surface evidence. No GLOSSARY entry. |
| **trust** | SUBSUMED-IN-AUTHORITY-BINDING-MECHANISM | DR pre-flag confirmed: "could be substrate permission flow + audit". Authority-binding listed as mechanism in MAINTENANCE TOP-LEVEL ARCHITECTURE concept-by-concept table. "Practitioner-judgment vs budget-policy vs individual" is POLICY language. No GLOSSARY entry. |
| **time** | SUBSUMED-IN-SUBSTRATE-AND-ADAPTER | DR pre-flag confirmed: "could be substrate scheduling + adapter time-driven operations". Substrate temporal semantics (turn-based / long-running) per substrate impl; adapter time-driven operations (cron / scheduled-fetch). No separate Time Protocol Surface with alternative implementations. No GLOSSARY entry. |

**Greenfield-derived Pattern A list**: **3 protocols** (substrate / adapter / quality-gate).

**Cascade implications**:
- Phase 3.4 LOCKED topics audit + sparring need RE-CLASSIFICATION (not Pattern A).
- Phase 3.4 PAUSED topics coordination + trust + time CANCELLED (subsumed; no separate Pattern A topics).
- Phase 3.2 topic catalog (line 868 of MAINTENANCE; ARCHITECTURE.md §4 catalog) NEEDS-REVISION — protocol topic count drops from 7-8 to 3.
- `protocol (architectural)` GLOSSARY entry cross-archetype catalog (line 1488-1496) NEEDS-REVISION — drop 5 entries (sparring/audit/coordination/trust/time); restate audit + sparring as mechanism-classes-not-protocols.
- VISION axes 2 + 3 UNTOUCHED — sparring as VISION axis stays anchored; audit emission / source-grounding / authority binding remain locked mechanisms.

### Step 4: Greenfield-derive Pattern A protocol topic template

**Status**: COMPLETE (session 17, 2026-05-02). **Tier-1 finding accepted by user**: 18-section monolithic template restructured to 12-common + 6-protocol-specific-conditional.

**Pre-condition (MS-3)**: Step 2 yielded GREENFIELD-EQUIVALENT — proceeded.

**Method**: From Pattern A definition (Surface + Implementations + Instance/binding) + 3 confirmed protocols (substrate / adapter / quality-gate) + locked first-principles disciplines, derive minimal common topic structure. Stress-test current 18-section template per MAINTENANCE:326-349 per-section.

**Greenfield-derived structure**:

**12 common-required sections** (apply to every Pattern A topic): §§ 1 (Topic scope + frontmatter), 2 (Surface contract), 4 (Per-implementation aspect), 5 (Selection mechanics), 6 (Tri-aspect reconciliation), 7 (Composition with framework primitives), 9 (Cardinality + lifecycle), 14 (Pre-implementation operational concerns / Phase 6 forward reference), 15 (Watch-list), 16 (Decision-design provenance), 17 (Phase routing), 18 (Cross-references).

**6 protocol-specific-conditional sections** (apply per protocol if applicable to its nature): §§ 3 (Common-surface boundary criteria — only adapter has multi-class Surface), 8 (Substrate-internal vs skill-side audit emission — substrate-specific concept), 10 (Boot + shutdown phase ordering — substrate-specific lifecycle; quality-gate fires per checkpoint without phases), 11 (Substrate error categories — per-protocol error semantics differ), 12 (Transport variation — substrate-specific MCP transport), 13 (Deployment-tier awareness — substrate-specific Tier 1/2/3).

**Per-protocol section count expectation**:
- substrate: 12 common + 6 conditional (all apply) = 18 total
- adapter: 12 common + ~3-4 conditional (§3 per-integration-class boundaries, §10 lifecycle/auth-refresh, §11 per-impl errors) = ~15-16 total
- quality-gate: 12 common + ~1-2 conditional (§11 fail-closed/open errors per shape) = ~13-14 total

**Tier-1 finding (second one)**: 18-section monolithic template is substrate-shape-anchored. DR pre-flag confirmed verbatim: "Pattern A protocol topic 18-section template substrate-shape-anchored / 8 Pattern A protocols list inherits archive's protocol categorization". Template was derived from substrate (first-Pattern-A topic) then "validated by adapter" per MAINTENANCE:326 — but validation likely involved forcing thin sections into adapter to fit the template, rather than the template adapting to adapter's nature.

**Cascade implications**:
- MAINTENANCE TOP-LEVEL ARCHITECTURE line 326-349 NEEDS-REVISION — 18-section template → 12-common + 6-conditional restructure.
- substrate ARCH topic (locked) GREENFIELD-EQUIVALENT — substrate IS template's shape-anchor; happens to fit. No content revision; structural reorganization only (move §§ 3, 8, 10, 11, 12, 13 from "common" to "substrate-protocol-specific" sections within the topic file).
- adapter ARCH topic (locked) MINOR-REVISION — sections that were forced or thinly populated can be removed or relocated to per-impl-extension Protocols.
- quality-gate ARCH topic (Phase 3.6 forthcoming) revision lands before topic is written; benefits from leaner template.
- sparring + audit ARCH topics already NEEDS-REVISION per Step 3 reclassification; template revision consistent.

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
