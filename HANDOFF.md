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
6. **Dev skills resurrected from archive (post-Phase-1) + repo-identity commitment locked**: `plugin/skills/decision-design-sharpening/` v0.3.0 + `plugin/skills/pre-implementation-sharpening/` restored along with `.claude-plugin/marketplace.json` + `plugin/.claude-plugin/plugin.json`. **Categorical distinction surfaced + locked in `MAINTENANCE.md` "TOP-LEVEL SCOPE — Repo identity: framework source, not deployment instance" section**: this repo is the **framework source** (starting point for deployments), NOT a deployment instance. Dev skills (sharpening, framing, etc.) live here permanently — they're for working ON the framework. App skills (orchestrator, draft-textteil-b, validate-checklist, etc.) **never live in this repo** — they belong to deployment instances (Phase 6 builds PBS-Schulz pioneer instance separately, not into this repo). Archive history bundled both because v0.35 conflated framework with pioneer instance; the rebuild reverses that. Skipped during restore: `archive/plugin/CLAUDE.md` + `archive/plugin/.mcp.json` (PBS-domain references). Plugin manifest descriptions cleaned (PBS-domain references removed; neutral placeholder describing framework-source role + dev-tooling-only state — full positioning rewrite when framework-distribution mechanics surface in Phase 3+). Memory: `feedback_dev_vs_app_skills.md` updated to reference TOP-LEVEL SCOPE commitment.

7. **GLOSSARY coherence audit (post-lock cross-entry pass)**: ran 9-lens primitive-set + sharpening pass on locked GLOSSARY (22 entries). Surfaced + applied:
   - **Within-entry sharpening** (R1, R2, R3, E4-E9): protocol entry promoted to META-PRIMITIVE (named architectural Protocols + substrate + adapter are the PRIMITIVE Pattern A instances); practitioner canonical fixed (natural-or-legal-person → natural person; legal-entity context lives at workspace level); framework architectural-protocols enumeration completed (added Substrate + Adapter); skill canonical "behavioral protocol" → "behavioral procedure" (terminology clash fix); STUB added as 5th Class value; axis entries got file:line citations to VISION; actor axis tag noted axis-3 lean; skill's specialist-context constraint flagged as PBS architectural commitment (vs Anthropic bare-skill convention); substrate canonical neutralized SDK-specific vocabulary.
   - **Primitive-set lens revisions** (A1+A2+A3): **A1** — specific mechanism instances (audit trail, source-grounding, persistent state, orchestration + 8 sparring sub-mechanisms = 12 entries planned) deferred to ARCH Layer 3 (NOT separate GLOSSARY entries — they're instances of abstract `mechanism` primitive); **A2** — `actor_kind: skill` enum value renamed to `actor_kind: ai_runtime` (eliminated naming collision with `skill` primitive — work-logic unit); **A3** — workflow re-tagged with bipartite-candidacy hedge (single-aspect cross-cutting current; bipartite Pattern B candidacy under examination at ARCH).
   - **GLOSSARY entry count revised**: was planned ~40 entries; now ~28 (12 specific-mechanism entries moved to ARCH Layer 3 territory).

8. **3rd dev skill written**: `plugin/skills/coherence-audit/` v0.1.0 — cross-decision audit operating on the corpus as a SET. Distinct from `decision-design-sharpening` (per-decision pre-commit) and `pre-implementation-sharpening` (per-decision at implementation-start). 9 lenses, with **Lens 1 (primitive-set redesign)**, **Lens 8 (pattern-vs-instance discipline)**, **Lens 9 (VISION-grounding)** as load-bearing. Lens 1 has 11 sub-questions (merge / split / add / remove / redefine / class re-classification / layer re-classification / pattern membership / multi-aspect manifestation / axis attribution / symmetry). Lens 8 directly addresses the instance-anchoring leakage that triggered the rebuild. Lens 9 ensures every primitive traces to VISION (anti-scope-creep). Decision-design-sharpening updated to back-port primitive-set lens + naming-collision check into Round 2 stress-test list.

9. **Adapter entry locked (final Pattern A primitive)** — Round 1 + Round 2 sharpening with 4 refinements applied (R1 internal-vs-external dimension; R2 skill↔adapter composition gap; E3 boundary test sharpening; E4 bidirectional/unidirectional shape variation). Cascade-pass through TOC + protocol entry + specialist entry + skill entry + MAINTENANCE.md. Pattern A trio complete: substrate (INTERNAL runtime) + adapter (EXTERNAL integration) + protocol META-PRIMITIVE (the pattern itself).

10. **Round 2 coherence-audit on full corpus + skill v0.2.0 reorg** — applied coherence-audit to the 23-entry corpus (user direction: "previous entries received only Round 1 — question each critically"). Surfaced + applied:
    - **R1 REMOVE AI runtime entry** — was STUB-only redirecting to substrate's Instance aspect; permanent zombie slot. Removed; "AI runtime" continues as informal shorthand in docs without glossary anchor. STUB also dropped from Class enum.
    - **R2 ADD work-unit primitive** — concept was load-bearing across 3+ entries (Owner B scope members; workspace cross-archetype examples; specialist context) but had no canonical home. Locked as PRIMITIVE: deployment-bound work-artifact; specialist-defines kind (project / matter / case / engagement / manuscript / audit). Added to TOC §2 Compositional primitives.
    - **R3 workspace ↔ workflow Composes-with reciprocal** — workflow listed workspace but workspace didn't list workflow. Symmetry fixed; also added work-unit reciprocal.
    - **R4 skill bipartite reclassification REJECTED** after deeper push — skill firing is execution, not bipartite manifestation; specialist's Pattern B captures owned-entities-at-Owner-B which skill doesn't have.
    - **E1 + E2 substrate/skill instance-leakage neutralization** (Lens 8 marginal) — skill canonical: "auto-loaded" → "behavioral procedure invoked when..." (load semantics substrate-defined per Pattern A); substrate canonical: "agent execution loop" → "execution model (agent loop, dataflow, event-driven, etc. — substrate-impl-defined)".
    - **E3 sparring/authorship/trust mechanism cascade-pass** — stale "(canonical entry forthcoming)" markers updated to "ARCH Layer 3 per A1" (collective-term references; per-mechanism detail = ARCH Layer 3).
    - **GLOSSARY entry count**: was 22 + adapter = 23; -AI runtime + work-unit = 23 (net same). Plan stable at ~28 final.
    - **Coherence-audit skill bumped to v0.2.0 with lens reorg** based on usage learnings: split former Lens 1 (11 sub-q) into Lens 1 (set composition, 5 sub-q) + Lens 2 (tag corrections, 5 sub-q); promoted Symmetry to standalone Lens 6; merged Lens 4 (tag consistency) + Lens 6 (source-grounded) → Lens 5 (mechanical compliance); dropped former Lens 7 (within-entry sharpening — defer to decision-design-sharpening); added new Lens 10 (cardinality + lifecycle). Total 10 universal lenses + 8 corpus-kind-specific (Phase 3+/4+/6+).

11. **Round 3 coherence-audit (using v0.2.0 lens system)** — applied 10-lens audit to 23-entry corpus. Surfaced + applied:
    - **RA2 work-unit reciprocal cascade-pass cleanup**: R2 added work-unit primitive but missed reciprocal Composes-with on specialist, workflow, event, actor, practitioner. Cascade-pass discipline failure caught by Lens 6 (Symmetry); reciprocals added to all 5 entries.
    - **RA3 work-unit bipartite-candidacy hedge** (Lens 2 Tag corrections): added hedge parallel to workflow's A3 hedge — KIND DISCRIMINATOR at Framework C (in specialist DEFINITION) + INSTANCE at Owner B; Phase 3 ARCH resolves bipartite vs single-aspect classification.
    - **RA4 "Client" instance-leakage at framework level fixed** (Lens 8 Pattern-vs-instance LOAD-BEARING): "Client" was enumerated as universal workspace-scope managed entity in Owner B scope members + workspace entry — but Client is practitioner-shape-anchored (engagement-target), not universal (personal-OS-shape has no clients; research-lab has funders/co-authors not clients; etc.). Same failure-mode shape as session-16 `project` enum tied to planning-domain. Corrected: engagement-target managed entities are shape-policy-mandated (practitioner-shape mandates Client; autonomous-business-shape mandates Customer; research-lab-shape mandates Funder/Co-author/Institution; etc.), NOT framework-level. Same applies to workspace entry's "What it is" section.
    - **EA1-EA5 cardinality + lifecycle clarifications** (Lens 10 NEW): added explicit cardinality + lifecycle paragraphs to specialist (instance-content lifecycle: persists across activation/deactivation cycles), workflow (specialist-defined; cardinality = sum across active specialists), actor (1 ai_runtime + 1+ humans + N external; per-shape variation), practitioner (record lifecycle: created at workspace setup or per-practitioner addition; mutable-with-audit), workspace ("deployment" preliminary-defined as one git-clone-instance + active substrate + workspace.md).
    - **Lens 1 + 8 + 9 collective REVISION count**: 2 (RA1 candidate + RA4) — non-zero counter-validation passes. Lens 10 (NEW) earned its place with 5 EXPANSIONS surfaced.
    - **RA1 (ADD `claim` primitive)**: surfaced in Lens 1 as load-bearing missing primitive (atomic accountability-bearing-assertion within work-unit output; cross-archetype). Held for separate Round 1 + Round 2 sharpening per `feedback_full_monty_upfront.md` discipline (new architectural addition deserves full pre-decision sharpening, not bundled with cleanup batch).

12. **`claim` primitive locked + Round 4 cleanup batch + skill v0.2.1 provenance discipline**:
    - **`claim` entry locked** (Round 1 full-monty + Round 2 sharpening — 4 refinements applied: boundary test disambiguates claim vs assertion vs statement via 3 distinguishing properties; axis tags explicitly mapped axis-3 primary + axis-2 sparring-target connection; source-grounding mechanism cross-reference added; audit-granularity policy clarified — claim-level / action-level / light distinction explained as shape-policy values configuring the audit-emission mechanism). Cardinality + lifecycle paragraph included. Cascade-pass added claim reciprocals to: work-unit, authorship preservation, sparring, event, practitioner Composes-with sections.
    - **Coherence-audit skill bumped v0.2.0 → v0.2.1**: provenance hygiene discipline added. Lens 5 (mechanical compliance) gained sub-check for audit/revision-history breadcrumbs ("per RA4 Round 3 audit", "per A1 — primitive-set lens, applied session 16", etc.) — entries should NOT contain such markers; provenance lives in HANDOFF + git log + commit messages. Discriminator: strip audit-revision-history markers; keep load-bearing forward-references / discipline notes. Step 5 (apply revisions) gained explicit instruction NOT to embed provenance breadcrumbs when applying findings — anti-pattern: AI feels productive adding "applied session X" markers, but they pollute canonical layer.
    - **Breadcrumb cleanup cascade-pass**: stripped audit-history markers from GLOSSARY entries that had accumulated through Round 2 + Round 3 — "per A1", "per A2", "per RA4 Round 3 audit", "applied session 16", "(per EA1-5)", "Phase 1.75 + feedback_apply_principle_uniformly resolution" — all removed; semantic content preserved. Forward-references ("Phase 3 ARCH resolves...", "deliberately NOT 'X'") kept. Result: 23 GLOSSARY entries → 24 (with claim) all canonical without provenance pollution.

13. **`defensibility` primitive locked + post-round self-check added to all 3 sharpening skills**:
    - **`defensibility` entry locked** (Round 1 full-monty + Round 2 sharpening; Round 2 yielded 0 REVISIONS / 4 EXPANSIONS — boundary-test 4th positive-marker question; cross-archetype failure-mode illustration; three structural conditions mapped to specific framework mechanisms; re-run-able lifecycle detail). DERIVED class — operational test for axis 3, not a primitive-with-instances. Cardinality N/A; the test applies whenever practitioner is challenged but structural conditions must hold at production time. Cascade-pass: stripped "(canonical entry forthcoming)" markers in authorship preservation + practitioner + event Composes-with; added defensibility ↔ claim reciprocal; TOC §8 updated.
    - **Stable-vs-continue self-check formalized**: previously ad-hoc; now part of all 3 sharpening skills (decision-design-sharpening v0.3.0 → v0.3.1; pre-implementation-sharpening v0.3.0 → v0.3.1; coherence-audit v0.2.1 → v0.2.2). At end of each round, AI explicitly commits STABLE-or-CONTINUE position with rationale citing specific termination signals — counters self-validation bias in both directions (defaulting to "continue" / manufactured-criticism risk vs defaulting to "stable" / premature-lock risk).
    - GLOSSARY: 24 → 25 locked entries.

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
