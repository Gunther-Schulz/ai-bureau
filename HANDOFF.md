# Session handoff — pbs-bureau (rebuild)

> **🔴 At session start, read `DISCIPLINES.md` FIRST** — working procedure + cross-session disciplines + memory composition. Then `VISION.md`, `MAINTENANCE.md`, this file.

This is the running session log for the **foundational rebuild** launched session 16 (2026-05-01). The previous multi-session running handoff (sessions 1-15) is at `archive/HANDOFF.md` for reference.

## Anchors (carry forward, never rebuilt)

- **`DISCIPLINES.md`** — cross-session working discipline; how we operate (procedure + 7 disciplines + memory composition). **Read FIRST.**
- `VISION.md` — three-axis thesis (intertwining + sparring + authorship preservation); preliminary-lock anchor; the ground truth the rebuild serves
- `MAINTENANCE.md` — doc system rules (5-layer model + cascade discipline + TOP-LEVEL ARCHITECTURE: framework=mechanisms / shape=policies + A-B-C scope model + GLOSSARY entry classification); read at session start
- `GLOSSARY.md` — canonical term definitions (Layer 1 anchor; in-progress as of session 16 Phase 2)
- `memory/` — feedback files (lessons learned across sessions) + bausteine + universal prose; the actual user knowledge
- `archive/INDEX.md` — index of v0.35 corpus + code + content archived at rebuild launch; consult during Phase 3+

**Consult when relevant** (not session-start required):
- `learnings/` — preliminary methodological observations about AI-app development; growing folder; consult during methodological reflection or when the AI-app-dev skill (per future ROADMAP) is being designed

**Session-start reading order**: `DISCIPLINES.md` → `VISION.md` → `MAINTENANCE.md` → `HANDOFF.md` (this file). Plus `GLOSSARY.md` for current vocabulary state.

## Rebuild phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Archive v0.35 corpus | ✅ Done session 16 |
| 1.5 | Design layered doc structure | ✅ Done session 16 (locked in `MAINTENANCE.md`) |
| 1.75 | VISION tightening pass (structure) | ✅ Done session 16 (1069 → 255 lines; content moved out lives in `archive/VISION.md`) |
| 1.8 | VISION terminology audit (term-level) | ✅ Done session 16 (15 candidates across 6 families; 2 inline tightenings; rest deferred to Phase 2 GLOSSARY) |
| 2 | Lock foundational vocabulary (`GLOSSARY.md`) | Next — proposal pending |
| 3 | Rebuild ARCH against locked vocabulary | Pending |
| 4 | Rebuild DRs selectively (collapse where possible) | Pending |
| 5 | Rebuild ROADMAP lean | Pending |
| 6 | Rebuild specs + code refactor (per existing #11 single-touch refactor) | Pending |

**Working procedure**: AI proposes next step → user adjusts/challenges/confirms → AI persists on sign-off. Per `feedback_propose_before_commit.md`.

## Session 16 — Rebuild launched (2026-05-01)

**What happened this session**:
1. Calibration clarifications surfaced 7 findings, all converging on one root: foundational vocabulary not crisply defined → layered approach named (session 14) but not permeated → instance-anchoring leakage in 5 different primitives (Art-25 naming, EU/DACH substrate-level additions, `project` enum, `groupings` primitive, practitioner = solo-human, vocabulary itself).
2. Strategy decision: archive everything (radical rebuild) rather than incremental patching. Rationale: pre-launch deprecation is essentially free per Maintenance discipline; `feedback_full_monty_upfront.md` says do comprehensive refinement upfront; preliminary-lock principle (v0.33) explicitly authorizes wholesale revision.
3. Archive complete: ARCH + ROADMAP + HANDOFF + docs/ (30 DRs + conventions + audits + design-reviews + strategic-positioning + rag-pipeline + plugin-conventions + backend-conventions + what-this-is + audit-pre-rag + office-config.schema) + extensions/framework/ (session-15 prototype) + backend/ (MCP server code) + plugin/ (19 skill bundles + templates) + .claude-plugin/ (plugin manifest) + extensions/{universal,domain,state}/ (PBS content; structure embodies scope-model decisions) + README.md. Code + content archived to remove rebuild bias per user direction; Phase 6 rebuilds against locked architecture. Memory/ + VISION + .claude/ + dev-link.sh + .gitignore stay as anchors / operational infrastructure.
4. `archive/INDEX.md` written with one-line purpose summary per piece + status note documenting known issues.
5. New HANDOFF.md (this file) written as rebuild log skeleton.
6. **Dev skills resurrected from archive (post-Phase-1) + repo-identity commitment locked**: `plugin/skills/decision-design-sharpening/` v0.3.0 + `plugin/skills/pre-implementation-sharpening/` restored along with `.claude-plugin/marketplace.json` + `plugin/.claude-plugin/plugin.json`. **Categorical distinction surfaced + locked in `MAINTENANCE.md` "TOP-LEVEL SCOPE — Repo identity: framework source, not deployment instance" section**: this repo is the **framework source** (starting point for deployments), NOT a deployment instance. Dev skills (sharpening, framing, etc.) live here permanently — they're for working ON the framework. App skills (orchestrator, draft-textteil-b, validate-checklist, etc.) **never live in this repo** — they belong to deployment instances (Phase 6 builds PBS-Schulz pioneer instance separately, not into this repo). Archive history bundled both because v0.35 conflated framework with pioneer instance; the rebuild reverses that. Skipped during restore: `archive/plugin/CLAUDE.md` + `archive/plugin/.mcp.json` (PBS-domain references). Plugin manifest description still references PBS-domain workflow — staleness flagged for separate rewrite when framework-distribution mechanics surface in Phase 3+. Memory: `feedback_dev_vs_app_skills.md` updated to reference TOP-LEVEL SCOPE commitment.

**Phase 1.5 outcome (locked session 16)**:

Layered doc structure designed and persisted in `MAINTENANCE.md` (Layer 0; read at session start). 5-layer model: Entry → Foundations → Overview → Architecture detail → DRs → Specs, plus Memory orthogonal. Cascade discipline elevated to top-level rule (per user direction): all docs stay in consistent state; changes propagate up/down/sideways in same commit.

**Phase 1.75 outcome (locked session 16)**:

VISION tightened from 1069 → 255 lines. Three axes preserved exactly; Ming foundation + IEP + adjacent thinkers preserved inline; falsification + robustness + defensibility test preserved (generalized). Removed: ARCH-territory mechanism lists; pioneer-instance + framework-foundation framing (design disciplines, not value claims); deployment possibilities + transition path + frontend + counter-VISION engagement + Cherry/EU fundability framing; Practitioner vs Specialist vocabulary; multi-practitioner implications. Resolved Option B floor inheritance contradiction. Reframed instance-anchored language to kind-neutral. All removed content lives in `archive/VISION.md` (v0.35 snapshot); new phases consult archive selectively when relevant rather than via promised lift-lists.

**Phase 2 starting state (locked session 16, multi-round sharpening complete)**:

**Foundational architecture locked** (now in MAINTENANCE.md "TOP-LEVEL ARCHITECTURE" section):
- Framework = MECHANISMS (universal interface contracts; no shape-specific values)
- Shape = POLICIES over mechanisms (each shape configures which active, mandatory, defaults)
- Atoms (mechanism, policy) vs containers (framework, shape) distinction
- A-B-C scope model derived from framework/shape framing (preliminary-locked)
- 4-axis classification scheme for GLOSSARY entries

**Term set locked** (~40 entries; multi-round sharpening output):
- 14 atomic primitives: workspace, practitioner, specialist, skill, AI runtime, actor, event, substrate, shape (meta), protocol, session, workflow, mechanism, policy
- 3 scope classifications: Layer A, Owner B, Framework C
- ~25 derived/compositions: workspace shape, practitioner-shape, named shapes catalog, multi-practitioner workspace, legal-entity workspace context, audit trail, sparring sub-mechanisms (8), cross-axis mechanisms (4), the 3 axes, defensibility, co-worker, intertwined-AI/tacked-on AI, pioneer instance, category collapse, framework
- Drops: trust/sparring/authorship mechanisms as separate classes (replaced by axis-tag metadata); shape-extension pattern (merged into shape); practitioner-author/expert practitioner (usage emphasis); practitioner-kind (variation lives at workspace level)

**Lock GLOSSARY entry-by-entry (per user direction "step by step")**. Order: foundational meta-primitives first (framework, shape, mechanism, policy), then atoms (workspace, practitioner, specialist, skill, AI runtime), then scope classifications (Layer A, Owner B, Framework C), then derived (axes, sparring sub-mechanisms, cross-axis mechanisms), then cross-cutting (actor, event, session, workflow, substrate, protocol).

AI proposes entry text → user adjusts/challenges/confirms → AI persists in `GLOSSARY.md`.

## Future ROADMAP items to remember (Phase 5 will consume this)

Items surfaced during the rebuild that should land in the rebuilt ROADMAP when Phase 5 runs. Captured here so they don't get lost between now and Phase 5.

1. **AI-app-development-facilitation skill** (high priority per user direction session 16) — captures cross-project discipline for building AI-centric apps; transferable to other AI-app projects. Consumes accumulated observations from `learnings/` folder. Per user: "should be our first ROADMAP item even though we will have many items that come before it."
2. **`learnings/` distillation** — when per-session entries accumulate stable patterns (typically 3-5 sessions of evidence), distill into structured topic-specific docs in `learnings/`; promote held observations to memory feedback rules / DRs / ARCH disciplines as appropriate. Feeds into the skill above.
3. **Testing harness for the framework** (later) — per user direction session 16. Eventual harness for systematic testing of framework primitives (mechanisms, protocols, shape conformance, sparring-output validation, audit-emission correctness, etc.). Composes with PydanticAI eval framework if adopted (per Phase 3 consideration #7). Distinct from per-skill testing in archived backend; this is harness for the framework layer itself.
4. **Markdown structure validation** (investigation + adoption) — per user direction session 16. Investigate: (a) existing libraries for markdown structural validation (frontmatter conformance, required-sections-present, cross-ref existence, schema-of-allowed-tag-values); (b) what we already had in archived code (`backend/mcp-server/` + `plugin/skills/{audit,design-review}/` per archived `archive/INDEX.md`). Composes with the markdown-validation feasibility analysis (per Phase 3 consideration #8). Distinguishes structural validation (feasible; libraries may exist) from semantic procedure validation (impossible-by-nature; LLM-judged eval territory).

## Inputs to consider for the rebuild (from session-16 findings)

Persisted in `archive/INDEX.md` "Status note" section. Six findings flagged as inputs the rebuild should address at root:

1. Foundational vocabulary lock (framework / shape / mechanism / policy / practitioner / authority chain / Protocol disambiguation)
2. Shape-neutrality vs Option B floor contradiction
3. VISION-scope vs framework-scope contradiction
4. Instance-anchoring leakage (5 sites)
5. "Mechanism vs policy" vocabulary not in corpus (introduced in session-16 conversation; needs to land as named architecture if accepted)
6. Filesystem location drift (shape-extension DR vs v0.34 restructure)

## Phase 3 ARCH rebuild — considerations surfaced

Items surfaced session 16 that Phase 3 (ARCH rebuild) should explicitly address:

7. **PydanticAI revisit** — archived `#18 substrate eval` + `#20 PydanticAI eval` need re-examination when Phase 3 rebuilds substrate decision. Per WebFetch from official PydanticAI docs (session 16): PydanticAI is a Python agent framework with type-safe Pydantic-validated structured outputs + tool registration + 15+ provider model-agnostic. Could be substrate candidate (alone or alongside Claude Agent SDK / MS Agent Framework). Verify by reading archived `substrate-agentic-framework.md` + `permission-abstraction.md` when Phase 3 starts.

8. **Markdown-validation feasibility analysis** — Phase 3 ARCH should explicitly characterize what kinds of validation are feasible for our markdown architecture and what kinds aren't. Per session-16 reasoning + archived AI-as-runtime hybrid-shape principle: validating LLM **outputs** (structured Pydantic-conforming data) is feasible (PydanticAI / vanilla Pydantic); validating LLM **inputs** (markdown procedures, prompts, SKILL bodies) is impossible-by-nature in a typed-system sense — only structural validation possible (frontmatter present, sections conform). Semantic validation of procedures requires LLM-judged eval (Phase 0 testing methodology territory). This distinction informs what kind of structural enforcement ARCH builds vs what's deliberately AI-as-runtime hybrid-shape territory.
