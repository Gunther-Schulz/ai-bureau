# DR: Phase 3.2 doc-organization (composite — taxonomy + naming + cross-cutting placement + ARCHITECTURE.md structure)

**Status**: ACCEPTED (Phase 3.2 closed; composite synthesis)
**Locked**: session 16 (2026-05-02)
**Sharpening**: Mode-2 composite decomposition per `decision-design-sharpening` v0.6.0 — 4 tightly-coupled sub-decisions in foundation-up dependency order; per-sub-decision standard 2-round sweet spot; this DR is the final synthesis pass.
**Phase**: 3.2 (composite of 4 sub-decisions; closes phase before 3.3 per-mechanism / 3.4 per-protocol / 3.5 per-primitive-detail content begins)

## Decision (composite of 4 sub-decisions)

Phase 3.2 produces 4 locked sub-decisions organizing how Phase 3.3-3.7 content lives:

1. **Topic taxonomy** — 14 ARCH topics (8 Pattern A protocols + 4 primitive-cluster topics + 2 cross-cutting integrators); protocol-centric aggregation
2. **File naming convention** — flat `arch/<slug>.md`; lowercase kebab-case slug = topic name; aggregation join via hyphen; no prefixes / sub-directories / arch-README
3. **Cross-cutting topics placement** — TOPICS-vs-CONCERNS distinction; cross-cutting topics get dedicated arch/ files; cross-cutting concerns live in ARCHITECTURE.md sections
4. **ARCHITECTURE.md overview structure** — 9 sections (Audience+scope / Phase status / Doc structure / Topic catalog / Reading order / Cross-cutting principles / Locked decisions / Disciplines / Watch-list); explicit consumer-model + Logic placement modes 4-mode codification

**All 4 sub-decisions composed coherently**: taxonomy decides WHAT topics exist; naming decides HOW they're named; cross-cutting placement decides WHERE different content lives (arch/ vs ARCHITECTURE.md); ARCHITECTURE.md structure decides HOW the overview presents catalog + principles + decisions to readers.

## Context

Phase 3.0 locked hybrid doc structure (single ARCHITECTURE.md overview + per-topic arch/<slug>.md files). Phase 3.1 closed all open architectural questions (workflow / work-unit / deployment / engaged-authorship). Phase 3.2 organizes how Phase 3.3-3.7 content (~30 BACKLOG items across 5 buckets: mechanism / protocol / primitive-detail / quality-gate / cross-cutting) maps to the locked hybrid structure.

Per-sub-decision sharpening sequence (foundation-up dependency):
- Sub-decision 1 (taxonomy) is foundation — what topics exist before naming/placement/structure
- Sub-decision 2 (naming) builds on taxonomy
- Sub-decision 3 (cross-cutting placement) builds on taxonomy + naming
- Sub-decision 4 (ARCHITECTURE.md structure) builds on all 3 prior sub-decisions

Mid-sharpening user question ("is ARCHITECTURE.md purely documentation or drawn from during production?") surfaced the foundational consumer-model question that drove explicit codification of Logic placement modes (4-mode distribution) + Audience+scope section in Sub-decision 4. This is the canonical example of bidirectional cascade per `MAINTENANCE.md`: ARCH-territory work surfaced glossary-grade structural fact about logic-distribution; codified into ARCHITECTURE.md before lock.

## Sub-decision 1: Topic taxonomy — 14 topics, protocol-centric aggregation

**Resolution**: 14 ARCH topics in protocol-centric aggregation with primitive-cluster topics. Foundation-up ordered. Under MAINTENANCE budget (15-20 cap) with 6-topic headroom for emergent additions during Phase 3.3-3.6 work.

**Topic structure**:
- 8 Pattern A protocol topics (substrate / adapter / sparring / audit / coordination / trust / time / quality-gate)
- 4 primitive-cluster topics (specialist+skill / practitioner / workflow+work-unit / claim+defensibility)
- 2 cross-cutting integrator topics (scope-model / axis-interactions)

**Aggregation rationale**: Pattern A protocols are natural topic anchors (Surface + per-impl + composing mechanisms + composing primitives all coherent); primitives without Pattern A home cluster by composition tightness (specialist contains skill; workflow attaches to work-unit; claim resolves at defensibility-granularity); cross-cutting integrators for irreducibly cross-axis content. Per Lens 15: aggregate when items tightly coupled OR individually <100 lines.

**Phase 3.7 cross-cutting investigations excluded** from topic count (research/strategic items, not ARCH-topic-shaped): PydanticAI eval / Markdown-validation feasibility / Ming research / Adjacent thinkers / Multi-VISION model.

**Round 1**: 3 options + 12 stress tests + position (Option A: protocol-centric).
**Round 2**: 10 EXPANSIONS applied (foundation-up ordering codified; forward-reference handling explicit; archived corpus integration noted; topic granularity calibration confirmed; axis-interactions confirmed; workspace coverage in scope-model; cross-topic primitive references; DR-vs-topic relationship; reading path deferred to Sub-decision 4; topic stability via cascade) + 6 REVISIONs rejected (R1 protocol/primitive splits / R2 specialist+skill split / R3 claim+defensibility split / R4 axis-interactions merge / R5 ARCHITECTURE.md as topic / R6 missing-topics check passed).

## Sub-decision 2: File naming convention — flat arch/ + plain kebab-case

**Resolution**: `arch/<slug>.md` flat directory; lowercase kebab-case slug = topic name; no prefixes; no sub-directories.

**Slug rules**:
- Path: `arch/<slug>.md`
- Slug: lowercase kebab-case; matches topic name in catalog
- Aggregation join: hyphen (`specialist+skill` → `specialist-skill.md`)
- No prefix (numeric / bucket / category)
- Plain `.md` extension; flat `arch/` directory; NO sub-directories per topic-cluster
- NO `arch/README.md` or `arch/INDEX.md`

**Cross-doc link conventions**: relative paths within arch/; `arch/<slug>.md` from elsewhere; GitHub-flavored anchors.

**File header convention**: minimal frontmatter (title; topic-cluster; status); H1 = de-kebab-cased slug.

**Why these conventions**: slug stability across taxonomy refinements (no embedded ordering / bucketing in path); visual + grep parity with GLOSSARY TOC anchors; flat directory simplifies navigation.

**Round 1**: 3 options + 7 stress tests + position (Option A: plain kebab-case slug).
**Round 2**: 9 EXPANSIONS applied (cross-doc consistency confirmed; flat arch/ explicit anti-pattern; slug stability noted; no arch/README anti-pattern; plain .md extension; cross-doc link conventions; anchor convention; file header convention; renaming protocol via cascade) + 5 REVISIONs rejected (bucket sub-dirs / numbered prefix / `+` aggregation char / multi-aspect sub-files / generic-word ambiguity).

## Sub-decision 3: Cross-cutting topics placement — TOPICS-vs-CONCERNS distinction

**Resolution**: cross-cutting CONCERNS vs cross-cutting TOPICS distinction is load-bearing.

- **Cross-cutting TOPICS** (dedicated `arch/<topic>.md` files): axis-interactions / scope-model / quality-gate
- **Cross-cutting CONCERNS** (ARCHITECTURE.md sections): Pattern-A/B/C semantics / cascade direction / scope-categorization framing / foundation-up ordering / G+D gate disciplines / Logic placement modes

**Distinction**: TOPIC = architectural content (lives in arch/); CONCERN = meta-principle (lives in ARCHITECTURE.md). Different placement, different KIND.

**Reading order for cross-cutting topics**: axis-interactions + scope-model LAST in foundation-up sequence (integrate across all prior).

**No content migration** between MAINTENANCE.md (Layer 0 discipline) and arch/scope-model.md (Layer 3 detail) — layer-distinction maintained; cross-refs only.

**Round 1**: 3 options + 7 stress tests + position (Option A: uniform-summary; cross-cutting topics treated like other topics in catalog).
**Round 2**: 8 EXPANSIONS applied (CONCERNS-vs-TOPICS distinction explicit; cross-cutting principles section scope vs Disciplines section; reading order; MAINTENANCE-vs-arch layer split; quality-gate dual nature; cross-refs via relative paths; forward-reference handling per Sub-decision 1; category-collapse placement) + 4 REVISIONs rejected (separate cross-cutting principles doc; arch/cross-cutting-principles.md as 15th topic; one-liner-vs-paragraph deferred; cross-cutting-concern-vs-topic naming applied).

## Sub-decision 4: ARCHITECTURE.md overview structure — 9 sections + Audience+scope + Logic placement modes

**Resolution**: 9-section structure with explicit consumer-model + Logic placement modes codification.

**9 sections** (foundation-up reader-orientation order):
1. Audience + scope (framework-developer documentation; Mode 4; NOT production-runtime)
2. Phase 3 sub-phase status (current progress table)
3. Doc structure (Phase 3.0 hybrid pattern + line budget)
4. Topic catalog (locked 14 topics + filenames + one-liners)
5. Reading order (recommended foundation-up path for new readers)
6. Cross-cutting principles (Pattern-A/B/C semantics + cascade direction + scope-categorization framing + foundation-up ordering + Logic placement modes + how topics compose + composability + pattern-vs-instance discipline)
7. Locked architectural decisions (Phase 3.0/3.1/3.2/3.6 lock summaries; short with cross-refs to detail)
8. Disciplines applying to all ARCH work (validation gates + multi-axis + profile-anchored + audit scaling + procedural rules)
9. Watch-list (open architectural questions awaiting evidence; cross-refs BACKLOG for actionable detail)

**Audience + scope explicit (Section 1)**: ARCHITECTURE.md is framework-developer documentation; loaded at framework-development session start; NOT production-runtime by deployed-workspace AI. Per `feedback_ai_as_runtime.md` discipline, AI in deployed PBS workspace loads runtime-relevant markdown (workspace.md / specialist DEFINITIONs / skill SKILL.md / shape policy bundles), not framework architecture documentation. Three consumer modes documented (framework-development / template+shape composition / production-runtime).

**Logic placement modes — 4-mode distribution (Section 6 cross-cutting principles)**:
- **Mode 1**: Production-runtime LLM-MD (operational layer — skills + specialist DEFINITIONs + workspace.md + shape policy bundles + bausteine; AI reads + interprets at runtime; highest LLM-instruction tightness required per `feedback_llm_instruction_tightness.md`)
- **Mode 2**: Production-runtime Python (substrate-side — substrate Instance impl + mechanism Python impls + adapter implementations + quality-gate Pattern A impls + Pydantic schema validation; substrate runtime executes; standard Python development discipline; self-falsifying via tests + type errors)
- **Mode 3**: Hybrid Phase 6 specs (spec layer — Pydantic = Python validation; spec docs = LLM-MD reference; bridges Modes 1+2)
- **Mode 4**: Development-time LLM-MD (documentation — ARCHITECTURE.md / arch/* / DRs / MAINTENANCE.md / VISION / GLOSSARY / profiles / learnings / DISCIPLINES.md; loaded at framework-development session start; NOT production-runtime; optimize for human readability + AI-developer orientation)

**Anti-pattern named**: encoding framework rules in Mode 4 docs intending production AI to follow them = SQL-DB trap per `feedback_ai_as_runtime.md`. Production AI follows Mode 1; Mode 4 is documentation, not runtime substrate.

**Catalog uniformity**: cross-cutting topics + Pattern A protocols + primitive clusters all get same one-liner depth in Section 4 Topic catalog. Topics earn detail in their own arch/<topic>.md files.

**Locked decisions section growth mitigation**: each lock summary stays SHORT (resolution + 1-2 sentence rationale + cross-ref to arch/<topic>.md detail OR DR for full content). Detail lives elsewhere; ARCHITECTURE.md keeps catalog-style summaries.

**Round 1**: 3 options + 8 stress tests + position (Option A: 8-section structure; later expanded to 9 with Audience+scope as new Section 1).
**Round 2**: 8 EXPANSIONS applied (Audience+scope as new Section 1; Logic placement modes section in cross-cutting principles; 9-section structure; Topic catalog REPLACEMENT with locked 14-topic version; reading order recommendation foundation-up; cross-cutting principles section structure; locked decisions growth mitigation discipline; watch-list cross-ref to BACKLOG) + 3 REVISIONs (R1 Logic placement modes as own topic — rejected as cross-cutting CONCERN per Sub-decision 3; R2 Audience+scope as separate Section 1 vs part of Doc structure — applied as separate Section 1 per E1; R3 hard line budget cap — applied as soft target).

## Composition with existing architecture

| Existing element | Composition |
|---|---|
| Phase 3.0 hybrid doc structure | Phase 3.2 organizes Phase 3.3+ content under hybrid structure (single ARCHITECTURE.md + per-topic arch/<slug>.md) |
| Phase 3.1 locked decisions (workflow / work-unit / deployment / engaged-authorship) | Each lock summary appears in Section 7 Locked decisions; full detail in GLOSSARY entries + DRs |
| Phase 3.6 quality-gate scope-lock | Pattern A protocol topic; foundational sequence position 8; Phase 3.6 produces full design |
| GLOSSARY entries (35 locked) | Each topic cross-references relevant GLOSSARY entries; vocabulary inheritance |
| `MAINTENANCE.md` cascade discipline + 5-layer doc model | Doc-system discipline (Layer 0); ARCHITECTURE.md (Layer 2) sits within model |
| `decision-design-sharpening` v0.6.0 + `coherence-audit` v0.3.1 | Sharpening discipline applied to each sub-decision (Round 1 + Round 2; Mode-2 composite); GLOSSARY back-check + REVISION/EXPANSION self-check active |
| `profiles/INDEX.md` + 4 profile clusters | Multi-axis + profile-anchored validation thresholds available; light-multi-axis applied to Phase 3.2 (structural decisions; no shape-specific surface) |

## Constraints flowing

This composite decision flows constraints into:

- **Phase 3.3 per-mechanism detail**: mechanisms subsumed under Pattern A protocol topics (per Sub-decision 1 aggregation); audit-emission + audit-trail + event in arch/audit.md; persistent-state in arch/substrate.md; orchestration in arch/workflow-work-unit.md; etc.
- **Phase 3.4 per-architectural-Protocol detail**: 8 Pattern A topics ready for content (substrate / adapter / sparring / audit / coordination / trust / time / quality-gate); foundation-up sequence locked
- **Phase 3.5 primitive-detail topics**: 4 primitive-cluster topics + 2 cross-cutting integrators ready for content
- **Phase 3.6 quality-gate full ARCH topic**: arch/quality-gate.md ready for Phase 3.6 detail (Surface specification + per-implementation + signal catalog + intervention mechanics + error semantics + tier-awareness)
- **Phase 4 DRs**: each Phase 3.3-3.7 architectural decision may produce its own DR; this composite DR is the precedent for grouped sub-decision DRs (per Mode-2)
- **Phase 6 specs**: Mode 3 hybrid spec layer (Pydantic + spec docs) per Logic placement modes codification

## Files touched

- `ARCHITECTURE.md` (full restructure to 9-section form; 449 → 389 lines after dedup; Audience+scope + Logic placement modes new sections; Topic catalog replacement; Reading order new section; section reordering for foundation-up reader path)
- `BACKLOG.md` (Phase 3.2 sub-phase header; all 4 sub-decisions resolved; composite DR placeholder marked complete this commit)
- `docs/decisions/phase-3-2-doc-organization.md` (this file — composite DR)
- (Earlier in Phase 3.2 sequence: GLOSSARY references; per-sub-decision commits)

## Revisit triggers

This composite DR should be revisited if:
- Phase 3.3-3.6 content work surfaces topic-aggregation insufficiency (e.g., one topic genuinely splits into two; new emergent topic needed beyond 6-topic headroom)
- Production deployment surfaces production-runtime AI loading patterns differing from Mode 4 documentation framing (e.g., template/shape creators (L3) operationally need Mode 4 docs more than "occasionally")
- 3-tier REVISION/EXPANSION discriminator codification triggers (per BACKLOG watch-list) — would amend Phase 3.2 sub-decision rounds metadata
- Phase 6 spec work reveals Mode 3 hybrid boundaries differing from current spec/code split intuition

## Sharpening rounds metadata

**Mode-2 composite decomposition** (per `decision-design-sharpening` v0.6.0; first canonical application of upfront-known composite mode):

- **Sub-decision 1**: Round 1 (3 options + 12 stress tests + position) + Round 2 (10 EXPANSIONS / 0 REVISIONS / 6 REVISIONs rejected)
- **Sub-decision 2**: Round 1 (3 options + 7 stress tests + position) + Round 2 (9 EXPANSIONS / 0 REVISIONS / 5 REVISIONs rejected)
- **Sub-decision 3**: Round 1 (3 options + 7 stress tests + position) + Round 2 (8 EXPANSIONS / 0 REVISIONS / 4 REVISIONs rejected)
- **Sub-decision 4**: Round 1 (3 options + 8 stress tests + position) + Round 2 (8 EXPANSIONS / 0 REVISIONS / 3 REVISIONs rejected)
- **Foundational consumer-model question** (raised mid-Sub-decision-4): drove Audience+scope section + Logic placement modes codification — canonical bidirectional cascade example

**Self-check** across all 4 sub-decisions: STABLE; 0 architectural REVISIONS; 35 EXPANSIONS total (all coverage additions or framing sharpenings; none reclassifiable as REVISION per v0.6.0 detection mechanism). Mode-2 composite-decomposition pattern empirically validated on first application.

**REVISION/EXPANSION classification self-check**: signal not yet warranted for 3-tier codification (per BACKLOG watch-list). 2-tier discrimination held across all 35 expansions.

**GLOSSARY back-check**: no glossary-grade structural facts surfaced (Phase 3.2 is doc-organization decisions; vocabulary already locked). Logic placement modes is meta-principle, not vocabulary; lives in ARCHITECTURE.md cross-cutting principles.

Total: 4 sub-decisions × 2 rounds = 8 sharpening rounds + 1 final synthesis (this DR). Per `feedback_pre_decision_sharpening.md` Mode-2 sweet spot: per-sub-decision 2-round + final synthesis pass. Phase 3.2 closed.
