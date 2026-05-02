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

Pattern-matching from HANDOFF prose, memory summaries, or prior-conversation knowledge is **NOT direct evidence** per global `~/.claude/CLAUDE.md` honesty-about-sources rule. The temptation to skip source-reading because "I remember roughly what it said" is the failure mode; cost-bias is legitimate sometimes (stating a quick recollection is fine when flagged), but honesty about basis is the rule.

**Discriminator**: am I citing or synthesizing? If I can name file:line with confidence, citing. Otherwise synthesizing (flag explicitly).

**Common failure surfaces** (session 16): malformed schema examples without verifying schema; over-confident defense of locked decisions without reading source DR; attribution of quotes to wrong source files. Common mechanism: pattern-matching from inherited summaries / conventions / prior framings instead of testing against current goal.

#### Re-grounding in VISION + ARCHITECTURE for substantive work

For any substantive session work in pbs-bureau (architectural decisions, design discussions, commitment design, DR authorship, strategic positioning), READ `VISION.md` + `ARCHITECTURE.md` alongside `HANDOFF.md` before substantive work. Without VISION re-grounding, AI drifts toward oracle-mode or validator-mode framings (per Vivienne Ming research: only sparring-mode produces value rivaling human+AI hybrid). Without ARCHITECTURE in context, proposals re-suggest already-discarded patterns.

**Re-grounding mid-session is valid** when you notice your own framing has drifted toward easy answers, or you've forgotten which architectural discipline applies, or the user pushes back on an answer that suggests oracle-mode drift.

#### Skill + profile files are a first-class source class

When invoking a sharpening / audit / validation skill (`decision-design-sharpening`, `pre-implementation-sharpening`, `coherence-audit`, `sharpen`), READ the SKILL.md file via Read tool at the moment of invocation — every time, regardless of prior usage in same session. Same for `profiles/*.md` when profile-anchored validation triggers (READ `profiles/INDEX.md` + ≥3 representative cluster members).

Skills + profiles evolve frequently (decision-design-sharpening went v0.4.0 → v0.6.0 mid-session 16); compaction collapses prior Read content into synthesis-summaries; fresh sessions have no breadcrumbs at all. Pattern-matching memory of prior usage misses load-bearing discipline elements.

**Verification (proves Read happened, not pattern-matched)**: chat output cites specific skill section names (e.g., "per layered coverage observation"; "per Lens 8") + specific profile content (not just cluster letters A/B/C/D). Without these citations, the procedure was pattern-matched, not executed.

**Canonical failure (session 16)**: substrate Round 1 post-compact applied `decision-design-sharpening` from synthesized memory; missed layered coverage observation; phase-routed cross-cutting concerns to Phase 6 too aggressively; user had to force re-Read; Round 2 surfaced 11 EXPANSIONS that should have been visible at Round 2 design.

### 2. Apply principle uniformly

When applying any principle, enumerate all categories the principle could apply to — independent of inherited framings ("docs vs code", "active vs deprecated", "X stays per Phase Y", "we already decided X earlier"). Test each: does the principle apply? Verify "no" boundaries are genuine, not carried-forward conventions.

**How to apply**:
1. **Enumerate categories** the principle could apply to, INDEPENDENT of inherited framings. Write them out.
2. **Test each**: "does the principle apply here? Yes / No / Why?"
3. When the answer is "No because X," **verify X is a genuine boundary** of the principle — not an inherited category carried forward unexamined.
4. **Discriminator**: would the user still draw the boundary at X if asked directly? If uncertain, surface borderline cases explicitly.
5. **When the user has to push a second/third time** to surface a missed category, that's a signal the inherited-framings filter wasn't disabled — explicitly enumerate the remaining categories proactively.

**Common failure surface** (session 16 archive proposal): user stated principle "archive everything that embodies the unlocked architecture; remove rebuild bias." AI applied to docs but missed code / plugin manifest / content directories / README — each because of inherited framing ("refactor is Phase 6", "content not code", "operational, flag for later"). User pushed three separate times to surface each missed category.

### 3. Pre-decision sharpening

At decision-formation moments, run sharpening rounds BEFORE locking:
- **Round 1** = full monty (proactive comprehensive — stress-tests + edge cases + counter-arguments engaged; Pareto-disciplined; reject manufactured criticism)
- **Round 2+** = USER-TRIGGERED (external-perspective friction; AI-self-triggered rounds drift toward manufactured criticism)

**Pre-decision sharpening outperforms post-mortem audits** (5 mechanisms):
1. **Anchoring bias**: post-mortem looks at WHAT IS; pre-decision can explore WHAT COULD BE
2. **Sunk-cost protection**: post-decision reviewers protect existing investment; pre-decision has no sunk cost
3. **Sparring vs validation mode**: sharpening = SPARRING (challenge); audits = VALIDATION (confirm). Per Vivienne Ming research: sparring outperforms validation
4. **Fresh-context advantage**: design context is hot during sharpening; cold during audits
5. **Greenfield-still-anchored problem**: even greenfield checks ("would we build this from scratch?") look AT existing shape; pre-decision sharpening generates alternatives directly

**Sweet spot per surface type** (NEW v0.8.0; per session-16 procedure-document META-failure):
- ARCHITECTURAL-DECISION: 2-3 rounds; expected decay 6→5→3→0-1
- PROCEDURE-DOCUMENT (process docs / methodology): density-check governs; sweet spot may be 4-5 rounds
- SET-LEVEL AUDIT (corpus-level): per-cluster density; rounds continue until cluster exhausted
- META-ARCHITECTURAL (foundational discipline / framework rebuild): user-trigger primary

Pattern-matching architectural-decision decay onto procedure-document or set-level audit = recurrent bias. **Empirical density check mandatory at every round termination** (count substantive findings current vs previous; ≥50% drop = decay confirmed). Decomposition trigger (Round 4+ signals decomposition missing) applies to ARCHITECTURAL-DECISION surface only.

**Two-phase pattern**:
- **Decision-design phase**: 2-3 rounds at decision-formation moment; architectural-decision lock
- **Pre-implementation phase**: additional rounds at implementation-start moment; operational/runtime details + ~10-20% architectural flow-back as DR amendments

**Layered coverage observation**: each round emphasizes (but doesn't exclusively cover) different concern layer:
- Round 1 = architectural decisions (what methods + types + abstractions)
- Round 2 = cross-cutting + schema details (boot, errors, transport, tier-awareness, audit integration)
- Round 3 (optional) = additional architectural patterns (broad surface only)
- Round 4+ → defer to Phase 2 pre-implementation (operational/runtime concerns)

**Decomposition trigger** (Mode 1 emergent): if a decision genuinely needs >3 rounds at decision-design phase → decompose into sub-decisions; each gets standard 2-3 rounds.

**Mode 2 composite decomposition** (upfront-known; per `decision-design-sharpening` v0.6.0): when 3+ tightly-coupled sub-decisions visible at framing time with foundation-up dependencies, decompose upfront: sub-decision inventory → foundation-up ordering → per-sub-decision 2-round sharpening → final synthesis pass → composite DR.

**Skills implementing this discipline**: `plugin/skills/decision-design-sharpening/` (Phase 1 decision-formation) + `plugin/skills/pre-implementation-sharpening/` (Phase 2 implementation-start) + `plugin/skills/sharpen/` (generic critical-pass) + `plugin/skills/coherence-audit/` (post-decision corpus-set audit).

#### Multi-axis validation for primitive proposals

When proposing or refining a primitive's classification / scope / applicability claim, validate across three orthogonal dimensions — single-axis validation misses gaps:

1. **Archetypes** — does primitive work for planner / lawyer / researcher / auditor / consultant / etc.?
2. **Work-types within an archetype** — does primitive work for codified workflow / ad-hoc exploratory / one-off communication / research-mode / maintenance / learning?
3. **Roles** — does primitive work for practitioner / workflow-designer / specialist-author / instance-deployer / AI-runtime / multi-user-collaborator / auditor-reviewer?

**Plus explicit non-coverage question**: "what use cases does this primitive NOT cover, and is that intentional or a gap?"

Single-axis validation creates blind spots. Cross-archetype illustration with constant work-type = "codified workflow" makes codified case look universal when ad-hoc work is also first-class.

#### Profile-anchored validation

For high-impact decisions (primitive classifications; per-mechanism / per-protocol / per-primitive-detail design — Phase 3.3-3.6 territory), test against ≥3 of 4 profile-clusters in `profiles/INDEX.md`:
- Cluster A Producers (L1+L2+L3+L9)
- Cluster B Deployers (L4a+L4b+L5a)
- Cluster C Consumers (L5a-L5j+L5e+L5f)
- Cluster D Validators (L8+G+D gates)

Flesh skeleton-profile if specific decision affects it (per `coherence-audit` on-demand fleshing). For routine decisions or cascade-from-established-pattern, multi-axis principle-level check sufficient. Discriminator: shape-specific or instance-specific surface → profile-anchored; purely structural cascade → multi-axis principle-level.

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

D Gate is structural per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (prefer structural constraints over conventions). Memory alone is insufficient as trigger — D Gate codifies the mental-modeling-first discipline as procedural enforcement at the decision moment.

Per memory: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (no-defer principle, v0.34 with D Gate), `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (defer-instinct disguises) (defer-instinct in disguises).

### 6. Anchored vs preliminary-locked

- **VISION axes are anchored** — revise only on real-world falsification per VISION's own falsification criteria
- **Everything else is preliminary-locked** — current best position derived from available reasoning; revisable when VISION ideal design demands. DRs, ARCH disciplines, meta-rules, specs, ROADMAP, code = living drafts

Per memory: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3.

### 7. Cascade discipline (structural consistency)

When changing any concept, decision, primitive, or term in any doc: identify every other place it appears and update each in the same commit (or tightly-coupled sequence explicitly marked as completing the cascade). Changes propagate **up, down, and sideways**.

Detailed mechanism: `MAINTENANCE.md` "TOP-LEVEL RULE — Cascade discipline".

### 8. Foundation-up workflow ordering

When ordering compositional/architectural work (GLOSSARY entries, DRs, ARCH topics, specs, layered design), default to foundation-up: items others depend on come first; downstream items come last. Parallel-depth items batch with shared sharpening passes.

**Why**: locking downstream items first creates rework when their foundations land later (definitions need updating; cross-references need fixing). Foundation-up minimizes rework + ensures downstream items can cleanly reference locked foundations.

**How to apply**:
- Identify dependencies between items before ordering
- Lock items with no dependencies (or only on already-locked items) first
- Lock items that compose with multiple already-locked items last
- For parallel-depth items, batch them

**When NOT to apply**:
- Independent work (bug fixes, ad-hoc tasks) without inter-dependencies
- Chronological/event-driven order more important than dependency order
- Stakeholder timing forces non-foundation-up sequence

### 9. Coherence-audit cadence

When `coherence-audit` skill fires across Phase 3-6 work. Codifies WHEN audits run (vs `coherence-audit` SKILL.md which codifies HOW).

**5 hard checkpoints** (scheduled in BACKLOG.md per Phase):

| # | When | Scope | Purpose |
|---|---|---|---|
| **C1** | Post-Phase-3.4 close | After 7 Pattern A protocol topics locked (substrate / adapter / sparring / audit / coordination / trust / time) | Validates Pattern A precedent set + 18-section template + per-Pattern-A cardinality variations before primitive-cluster topics extend |
| **C2** | Post-Phase-3.5 close | After 4 primitive cluster + 2 cross-cutting integrator topics locked | Validates primitive clusters compose cleanly with Pattern A protocols |
| **C3** | Phase 3.8 phase-boundary | ARCH-specific Lenses 11-15 activate (inter-layer consistency / specs traceability / architectural-protocol completeness / DR coverage gap / granularity match) | Comprehensive corpus-set audit before Phase 4 starts |
| **C4** | Phase 6 pre-implementation | Architectural-validation pass before implementation work begins; Lens 17 (schema completeness) activates | Catches architectural drift accumulated across Phase 4-5 |
| **C5** | Post-Phase-6 close | Final audit; full corpus including specs + code; Lens 18 (spec/impl divergence) activates | Before stability lock + promotion to higher-classification |

**3 trigger conditions** (mid-phase auto-fire candidates; per `coherence-audit` SKILL.md "When this skill fires"):

| Trigger | When | Scope |
|---|---|---|
| **5+ DRs since last audit** | Per skill SKILL.md: "After a sequence of decisions has been locked" | Mid-phase audit on accumulated DRs since prior audit |
| **Composite-DR lock** | After Mode-2 composite decomposition lands (multiple sub-decisions in one DR) | Scoped audit on composite decision's surface |
| **Pre-promotion-to-stability** | Before any locked corpus segment promoted to higher-stability classification | Signal-driven; user-triggered |

**Why this cadence**:
- Phase 3.4 mid-audit (after 5 of 7 topics) deferred — Pattern A pattern already validated by 3 topics; mid-phase audit before C1 = cost without benefit
- Phase 5 close audit skipped — ROADMAP is concise; subsumed into C4 (Phase 6 pre-implementation) which validates ROADMAP + spec planning together
- Phase 4 close audit subsumed into C4 — DR-set audit (Lens 16 decision-linkage / constraint-flow tracking) activates within C4 unless 5+ DR trigger fires mid-Phase-4
- Per-DR audit rejected — would fire too frequently; trigger condition (5+ DRs) catches accumulation

**Composition with `coherence-audit` SKILL.md**: skill defines HOW (10 universal lenses + corpus-specific 11-18); this discipline defines WHEN (5 hard checkpoints + 3 triggers). Together: at each checkpoint or trigger fire, READ skill (per Discipline 1 skill+profile sub-section); apply procedure; cite specific lens names + findings in chat output.

**Persistence target**: BACKLOG.md scheduled audit checkpoints per Phase. ARCHITECTURE.md §2 sub-phase status table (Phase 3.8 row already present; C1 + C2 cross-ref BACKLOG).

### 10. Greenfield evaluation of archived material

When ARCH topic / DR / spec work cites archived material (`archive/docs/decisions/*` / `archive/extensions/*` / archived ARCHITECTURE / etc.), each cited element MUST be greenfield-evaluated against current locked vocabulary — NOT transcribed as template.

**Why**: Archive embodies session-1-15 architectural commitments — much of which was unlocked / instance-anchored / contradiction-bearing per session-16 rebuild rationale. Cargo-cult adoption of archived elements re-introduces the failure modes the rebuild was designed to fix. Per `MAINTENANCE.md` rebuild context: "the prior v0.35 corpus grew beyond easy handling... contained internal contradictions... arose because cascade discipline was implicit."

**Failure surface (canonical session-16 case)**: arch/coordination.md Round 1 cargo-cult'd archived event-coordination protocol (capability categories + 3 failure modes + no-direct-call discipline directly transcribed) without explicit greenfield-evaluation per element. User caught the drift.

**Discriminator** (per cited archived element):
- Was element re-validated against locked GLOSSARY entries that exist NOW (not the v0.35 vocabulary)?
- Was element stress-tested against profile clusters in current `profiles/INDEX.md`?
- Pattern-vs-instance check: does archived element embed pioneer-instance / archetype-instance / regulatory-instance assumptions that current architecture rejected?
- Greenfield derivation: would we design THIS element THIS WAY today, ignoring archive?

If any check yields NO → element needs revision OR archive-citation is INPUT-ONLY (informs current design but doesn't transfer structure directly).

**How to apply**:

1. **At Round 1 sharpening**, when archive citation considered: surface the cited element + greenfield-evaluation result per criterion above. NOT "per archived X" as terminating evidence.
2. **At Round 2 sharpening termination**, run greenfield-citation self-check: every "per archived X" claim → was X greenfield-evaluated, or transcribed?
3. **Coherence-audit Lens 5 v0.2.1 provenance hygiene** extends: ARCH topics + DRs hold greenfield-evaluated content; archive citations live in §16 "Decision-design provenance" sections naming SOURCE (where input came from), NOT TEMPLATE (where structure transferred).

**Recognition-pattern bias**: stress-testing pressure DECREASES when archived material "fits" the topic shape — exactly when greenfield-evaluation is MOST important (high archive-fit = highest cargo-cult risk). Counter-bias: when archive seems to fit well, increase stress-testing rigor.

**Composition**: per `DISCIPLINES.md` Discipline 1 source-grounded rule extended to archive (archived material is a source class; cite specifically; flag synthesis vs citation; greenfield-evaluation is the synthesis-not-citation step). Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 preliminary-lock: archived "locked" decisions are NOT preliminary-locked relative to current rebuild — they're archived UNlocked (rebuild rejected v0.35 corpus per session-16 launch). Greenfield evaluation re-establishes locked status.

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

## Discipline map — when each fires

Disciplines compose. Different disciplines fire at different decision moments. This table shows when each engages so AI applies the right ones in context.

### Validation gates (structural; fire before specific work proceeds)

| Gate | Fires when | Codified at |
|---|---|---|
| **G — Composability Gate** | Designing any L1-L4 producer artifact (specialist / shape / template / workspace) | `profiles/G-composability-gate.md` + `profiles/INDEX.md` |
| **D — Defer Gate** | AI considers deferring any architectural item | `profiles/INDEX.md` "D Gate procedure" + `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 |

### Decision-design disciplines (fire during architectural decisions)

| Discipline | Fires when | Codified at |
|---|---|---|
| Pre-decision sharpening (Round 1 full monty + Round 2 user-triggered; sweet spot per surface type) | Substantive architectural decisions | `DISCIPLINES.md` Discipline 3 + `plugin/skills/decision-design-sharpening/` v0.8.0 (Mode 1 emergent + Mode 2 upfront-known composite decomposition; layered coverage observation: R1 arch decisions / R2 cross-cutting + schema-detail / R3 patterns; Round 1 termination checklist mandatory per Discipline 10; mandatory empirical density check + surface-type declaration + honest termination test (Q1-Q5) at every round termination per v0.8.0 + sharpen v0.10.0; GLOSSARY back-check + REVISION/EXPANSION self-check at Round 2 termination) |
| Multi-axis validation (archetype × work-type × role + non-coverage) | Primitive classification proposals | `DISCIPLINES.md` Discipline 3 (multi-axis sub-section) + `profiles/INDEX.md` |
| Foundation-up workflow ordering | Compositional/architectural work (GLOSSARY, DRs, ARCH, specs) | `DISCIPLINES.md` Discipline 8 |
| Apply principle uniformly | When user states a principle/goal | `DISCIPLINES.md` Discipline 2 |
| Decision-phase approval; content-phase no approval | Surfacing positions/framings to user | `feedback_propose_before_commit.md` + `feedback_judgment_and_automate.md` |

### Cross-session work disciplines (fire on every substantive session)

| Discipline | Fires when | Codified at |
|---|---|---|
| Re-ground in VISION + ARCH | Start of substantive PBS work | `DISCIPLINES.md` Discipline 1 (re-grounding sub-section) |
| Source-grounded; cite file:line | Asserting what a doc/DR says | `DISCIPLINES.md` Discipline 1 |
| Cascade discipline | Changing concept/primitive/term in any doc | `MAINTENANCE.md` "TOP-LEVEL RULE — Cascade" |
| Commit regularly + push after commit | Per-logical-unit work completion | `feedback_push_after_commit.md` |
| LLM-instruction tightness for markdown layer | Authoring skill / ARCH / GLOSSARY content | `ARCHITECTURE.md` cross-cutting principles "LLM-instruction tightness" |

### Architectural commitments (anchor framework decisions)

| Commitment | Codified at |
|---|---|
| AI as runtime, not consumer | `ARCHITECTURE.md` cross-cutting principles "AI as runtime" |
| Make wrong shapes impossible (structural over conventional) | `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 |
| Pattern-vs-instance discipline | `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 |
| Repo identity: framework source, not deployment instance | `MAINTENANCE.md` TOP-LEVEL SCOPE + `MAINTENANCE.md` "TOP-LEVEL SCOPE" |
| Preliminary lock except VISION axes | `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 |

### Audit + coherence disciplines (fire during corpus validation)

| Discipline | Fires when | Codified at |
|---|---|---|
| Coherence-audit 10 universal lenses + corpus-specific | Cross-decision corpus validation | `plugin/skills/coherence-audit/` v0.3.1 (Step 7 REVISION/EXPANSION self-check) |
| Audit scaling strategies (cluster compression / deltas / on-demand fleshing / sampling / full systematic) | Audit-load-management decisions | `plugin/skills/coherence-audit/` v0.3.1 "Audit scaling strategies" |
| Provenance hygiene (no audit-history breadcrumbs in canonical content) | Applying lock revisions | coherence-audit Lens 5 v0.2.1 |
| Profile-grounded validation | Pre-validation + post-validation | `profiles/INDEX.md` |

### Operational disciplines

| Discipline | Fires when | Codified at |
|---|---|---|
| Stop on block; don't work around | Hook/permission/sandbox blocks | `feedback_blocked_actions.md` |
| Plugin reload doesn't sync marketplace clone | Stale skill list after pushing plugin changes | `feedback_plugin_marketplace_clone_sync.md` |

## Memory composition (cross-session AI behavioral preferences)

Memory holds **cross-session AI behavioral preferences only** (per session-16 doc-organization composite DR). Operational disciplines (HOW we operate) absorbed into THIS doc; architectural commitments absorbed into MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES + ARCHITECTURE.md cross-cutting principles.

Retained memory feedback files (5):

| File | Role |
|---|---|
| `feedback_propose_before_commit.md` | Decision phase = approval needed for positions/framings (chat surfaces decisions+reasons, NOT verbatim content); content phase = write directly |
| `feedback_judgment_and_automate.md` | Commit positions instead of menus; routine work without asking |
| `feedback_push_after_commit.md` | Push immediately after each commit |
| `feedback_blocked_actions.md` | Surface hook/permission/sandbox blocks immediately; never workaround |
| `feedback_plugin_marketplace_clone_sync.md` | Operational tool note (marketplace clone sync mechanics) |

Memory location: `/home/g/.claude/projects/-home-g-dev-Gunther-Schulz-pbs-bureau/memory/`. Index: `MEMORY.md` in same directory.

Memory feedback files migrated (14; deleted from memory dir; absorbed into structured docs):
- `DISCIPLINES.md` Discipline 1 → DISCIPLINES.md Discipline 1
- `DISCIPLINES.md` Discipline 1 (re-grounding sub-section) → DISCIPLINES.md Discipline 1 (sub-section)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section) → DISCIPLINES.md Discipline 1 (sub-section)
- `DISCIPLINES.md` Discipline 2 → DISCIPLINES.md Discipline 2
- `DISCIPLINES.md` Discipline 3 → DISCIPLINES.md Discipline 3
- `DISCIPLINES.md` Discipline 3 (multi-axis sub-section) → DISCIPLINES.md Discipline 3 (sub-section)
- `DISCIPLINES.md` Discipline 8 → DISCIPLINES.md Discipline 8
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 → MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §2 (no-defer + pattern-vs-instance + D Gate consolidated)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 → MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §1
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 → MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §3
- `MAINTENANCE.md` TOP-LEVEL SCOPE → MAINTENANCE.md TOP-LEVEL SCOPE
- `ARCHITECTURE.md` cross-cutting principles "AI as runtime" → ARCHITECTURE.md cross-cutting principles
- `ARCHITECTURE.md` cross-cutting principles "LLM-instruction tightness" → ARCHITECTURE.md cross-cutting principles (alongside Logic placement modes)
- `DISCIPLINES.md` Discipline 3 (full-monty consolidated) → consolidated into pre_decision_sharpening (already retired session 16)

---

## When this doc itself changes

DISCIPLINES.md is foundational. Changes affect every subsequent session's discipline. When changing:

1. Identify what existing discipline is being changed/added/removed
2. Verify or update memory feedback files that compose with the changed discipline
3. Update `HANDOFF.md` to flag the change for future-session readers
4. Update relevant references in `MAINTENANCE.md` if architectural-foundation territory is touched
5. Cascade-pass: any docs referencing the changed discipline get updated in same commit

This doc is preliminary-locked like everything else (per discipline 6 above) — but changes should be deliberate, not casual.
