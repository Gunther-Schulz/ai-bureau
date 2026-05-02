# Session handoff — pbs-bureau (rebuild)

> **🔴 Bootstrap procedure for fresh session** (covers compacted-resume too): see `CLAUDE.md` at project root — auto-loaded every session — for canonical session-start procedure (mandatory reads + skill invocation procedure + profile-anchored validation procedure). At minimum: `VISION.md` → `MAINTENANCE.md` → `DISCIPLINES.md` → this file → `BACKLOG.md` → `ARCHITECTURE.md` (when working architectural).

This is the running session log for the **foundational rebuild** launched session 16 (2026-05-01). The previous multi-session running handoff (sessions 1-15) is at `archive/HANDOFF.md` for reference.

## Bootstrap pointers (fresh session — load-bearing reads)

- **`CLAUDE.md`** (project root; auto-loaded every session) — canonical session-start procedure + skill invocation procedure + profile-anchored validation procedure. Read FIRST if not already auto-loaded.
- **`DISCIPLINES.md`** — cross-session working discipline; how we operate (procedure + 7 disciplines + memory composition + skill+profile = first-class source class)
- **`VISION.md`** — three-axis thesis (intertwining + sparring + authorship preservation) + framework's structural primitives + shape-neutrality + foundations + falsification; PURE STANCE ABOUT THE PRODUCT; preliminary-lock anchor; the ground truth the rebuild serves
- **`MAINTENANCE.md`** — doc system rules (5-layer model + cascade discipline + TOP-LEVEL ARCHITECTURE: framework=mechanisms / shape=policies + A-B-C scope model + GLOSSARY entry classification)
- **`BACKLOG.md`** — Phase-tagged work-item tracker; pending items across phases
- **`PIONEER.md`** — pioneer-instance (PBS-Schulz) identity-anchor; current deployment status + relation to framework; consult when working on pioneer-instance-specific content
- **`profiles/INDEX.md`** — usage profiles for framework validation; cluster A/B/C/D structure; pre-validation + post-validation. **READ this file (not just memory of cluster names) when profile-anchored validation triggers.**
- **`ARCHITECTURE.md`** — Layer 2 overview for Phase 3 ARCH rebuild; Phase 3 status + locked architectural decisions + active disciplines + 14-topic catalog; per-topic detail in `arch/<topic-slug>.md` (Phase 3.4+ work)
- **`GLOSSARY.md`** — canonical term definitions (Layer 1 anchor; 35 entries locked Phase 2)
- **`memory/`** — feedback files (lessons learned; loaded into conversation context per `MEMORY.md` index)
- **`archive/INDEX.md`** — v0.35 corpus + code + content archived at rebuild launch; consult during Phase 3+

**Specialized skill invocation** (mandatory at every invocation; per `DISCIPLINES.md` Discipline 1 (skill+profile sub-section)):
- `plugin/skills/decision-design-sharpening/SKILL.md` — pre-decision sharpening (architectural decisions; 2-3 round sweet spot)
- `plugin/skills/pre-implementation-sharpening/SKILL.md` — implementation-start sharpening
- `plugin/skills/coherence-audit/SKILL.md` — cross-decision corpus audit
- `plugin/skills/sharpen/SKILL.md` — generic critical-pass

READ the SKILL.md via Read tool at every invocation regardless of prior usage. Pattern-matching from memory FAILS load-bearing discipline elements.

**Consult when relevant** (not session-start required):
- `learnings/ai-app-development.md` — preliminary methodological observations; growing folder; consult during methodological reflection
- `drafts/` — exploratory ideas / future-candidates / brainstorm output (NOT locked, NOT load-bearing); discipline in `drafts/README.md`. Holds: `marketing-themes.md`, `composability-tooling.md`, `execution-fidelity.md` (session-16 META-framework concern about AI faithful execution of prescribed procedures)

**Session-start reading order** (substantive work): `CLAUDE.md` → `VISION.md` → `MAINTENANCE.md` → `DISCIPLINES.md` → `HANDOFF.md` (this file) → `BACKLOG.md` → `profiles/INDEX.md` → `ARCHITECTURE.md` (Layer 2; read when working in architectural area) → `GLOSSARY.md` (vocabulary state). Specific profiles + per-topic `arch/<topic>.md` files load on-demand.

## Rebuild phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Archive v0.35 corpus | ✅ Done session 16 |
| 1.5 | Design layered doc structure | ✅ Done session 16 (locked in `MAINTENANCE.md`) |
| 1.75 | VISION tightening pass (structure) | ✅ Done session 16 (1069 → 255 lines; content moved out lives in `archive/VISION.md`) |
| 1.8 | VISION terminology audit (term-level) | ✅ Done session 16 (15 candidates across 6 families; 2 inline tightenings; rest deferred to Phase 2 GLOSSARY) |
| 1.85 | VISION sanity check + clean-stance restructure | ✅ Done session 16 (4 sanity-check fixes against locked GLOSSARY; clean-stance restructure removed positioning + comparing language; new tagline + tree analogy with branches/trunk/roots; 2 new Implications — AI-as-runtime + pattern-vs-instance discipline; PIONEER.md created for pioneer-instance content; drafts/ pattern established for exploratory ideas) |
| 2 | Lock foundational vocabulary (`GLOSSARY.md`) | ✅ Done session 16 (34 locked entries; coherence-audited Round 1 — Lens 1+8+9 yielded 0 REVISIONS, corpus set-coherent; STABLE) |
| 3 | Rebuild ARCH against locked vocabulary | Pending — starts next session |
| 4 | Rebuild DRs selectively (collapse where possible) | Pending |
| 5 | Rebuild ROADMAP lean | Pending |
| 6 | Rebuild specs + code refactor (per existing #11 single-touch refactor) | Pending |

**Working procedure**: AI proposes next step → user adjusts/challenges/confirms → AI persists on sign-off. Per `feedback_propose_before_commit.md`.

## Session 16 — Rebuild launched (2026-05-01)

**What happened this session**:
1. Calibration clarifications surfaced 7 findings, all converging on one root: foundational vocabulary not crisply defined → layered approach named (session 14) but not permeated → instance-anchoring leakage in 5 different primitives (Art-25 naming, EU/DACH substrate-level additions, `project` enum, `groupings` primitive, practitioner = solo-human, vocabulary itself).
2. Strategy decision: archive everything (radical rebuild) rather than incremental patching. Rationale: pre-launch deprecation is essentially free per Maintenance discipline; `DISCIPLINES.md` Discipline 3 (full-monty consolidated) says do comprehensive refinement upfront; preliminary-lock principle (v0.33) explicitly authorizes wholesale revision.
3. Archive complete: ARCH + ROADMAP + HANDOFF + docs/ (30 DRs + conventions + audits + design-reviews + strategic-positioning + rag-pipeline + plugin-conventions + backend-conventions + what-this-is + audit-pre-rag + office-config.schema) + extensions/framework/ (session-15 prototype) + backend/ (MCP server code) + plugin/ (19 skill bundles + templates) + .claude-plugin/ (plugin manifest) + extensions/{universal,domain,state}/ (PBS content; structure embodies scope-model decisions) + README.md. Code + content archived to remove rebuild bias per user direction; Phase 6 rebuilds against locked architecture. Memory/ + VISION + .claude/ + dev-link.sh + .gitignore stay as anchors / operational infrastructure.
4. `archive/INDEX.md` written with one-line purpose summary per piece + status note documenting known issues.
5. New HANDOFF.md (this file) written as rebuild log skeleton.
6. **Dev skills resurrected from archive (post-Phase-1) + repo-identity commitment locked**: `plugin/skills/decision-design-sharpening/` v0.3.0 + `plugin/skills/pre-implementation-sharpening/` restored along with `.claude-plugin/marketplace.json` + `plugin/.claude-plugin/plugin.json`. **Categorical distinction surfaced + locked in `MAINTENANCE.md` "TOP-LEVEL SCOPE — Repo identity: framework source, not deployment instance" section**: this repo is the **framework source** (starting point for deployments), NOT a deployment instance. Dev skills (sharpening, framing, etc.) live here permanently — they're for working ON the framework. App skills (orchestrator, draft-textteil-b, validate-checklist, etc.) **never live in this repo** — they belong to deployment instances (Phase 6 builds PBS-Schulz pioneer instance separately, not into this repo). Archive history bundled both because v0.35 conflated framework with pioneer instance; the rebuild reverses that. Skipped during restore: `archive/plugin/CLAUDE.md` + `archive/plugin/.mcp.json` (PBS-domain references). Plugin manifest descriptions cleaned (PBS-domain references removed; neutral placeholder describing framework-source role + dev-tooling-only state — full positioning rewrite when framework-distribution mechanics surface in Phase 3+). Memory: `MAINTENANCE.md` TOP-LEVEL SCOPE updated to reference TOP-LEVEL SCOPE commitment.

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
    - **RA1 (ADD `claim` primitive)**: surfaced in Lens 1 as load-bearing missing primitive (atomic accountability-bearing-assertion within work-unit output; cross-archetype). Held for separate Round 1 + Round 2 sharpening per `DISCIPLINES.md` Discipline 3 (full-monty consolidated) discipline (new architectural addition deserves full pre-decision sharpening, not bundled with cleanup batch).

12. **`claim` primitive locked + Round 4 cleanup batch + skill v0.2.1 provenance discipline**:
    - **`claim` entry locked** (Round 1 full-monty + Round 2 sharpening — 4 refinements applied: boundary test disambiguates claim vs assertion vs statement via 3 distinguishing properties; axis tags explicitly mapped axis-3 primary + axis-2 sparring-target connection; source-grounding mechanism cross-reference added; audit-granularity policy clarified — claim-level / action-level / light distinction explained as shape-policy values configuring the audit-emission mechanism). Cardinality + lifecycle paragraph included. Cascade-pass added claim reciprocals to: work-unit, authorship preservation, sparring, event, practitioner Composes-with sections.
    - **Coherence-audit skill bumped v0.2.0 → v0.2.1**: provenance hygiene discipline added. Lens 5 (mechanical compliance) gained sub-check for audit/revision-history breadcrumbs ("per RA4 Round 3 audit", "per A1 — primitive-set lens, applied session 16", etc.) — entries should NOT contain such markers; provenance lives in HANDOFF + git log + commit messages. Discriminator: strip audit-revision-history markers; keep load-bearing forward-references / discipline notes. Step 5 (apply revisions) gained explicit instruction NOT to embed provenance breadcrumbs when applying findings — anti-pattern: AI feels productive adding "applied session X" markers, but they pollute canonical layer.
    - **Breadcrumb cleanup cascade-pass**: stripped audit-history markers from GLOSSARY entries that had accumulated through Round 2 + Round 3 — "per A1", "per A2", "per RA4 Round 3 audit", "applied session 16", "(per EA1-5)", "Phase 1.75 + feedback_apply_principle_uniformly resolution" — all removed; semantic content preserved. Forward-references ("Phase 3 ARCH resolves...", "deliberately NOT 'X'") kept. Result: 23 GLOSSARY entries → 24 (with claim) all canonical without provenance pollution.

13. **`defensibility` primitive locked + post-round self-check added to all 3 sharpening skills**:
    - **`defensibility` entry locked** (Round 1 full-monty + Round 2 sharpening; Round 2 yielded 0 REVISIONS / 4 EXPANSIONS — boundary-test 4th positive-marker question; cross-archetype failure-mode illustration; three structural conditions mapped to specific framework mechanisms; re-run-able lifecycle detail). DERIVED class — operational test for axis 3, not a primitive-with-instances. Cardinality N/A; the test applies whenever practitioner is challenged but structural conditions must hold at production time. Cascade-pass: stripped "(canonical entry forthcoming)" markers in authorship preservation + practitioner + event Composes-with; added defensibility ↔ claim reciprocal; TOC §8 updated.
    - **Stable-vs-continue self-check formalized**: previously ad-hoc; now part of all 3 sharpening skills (decision-design-sharpening v0.3.0 → v0.3.1; pre-implementation-sharpening v0.3.0 → v0.3.1; coherence-audit v0.2.1 → v0.2.2). At end of each round, AI explicitly commits STABLE-or-CONTINUE position with rationale citing specific termination signals — counters self-validation bias in both directions (defaulting to "continue" / manufactured-criticism risk vs defaulting to "stable" / premature-lock risk).
    - GLOSSARY: 24 → 25 locked entries.

14. **`BACKLOG.md` created (Layer 0 doc) + sharpening skills updated to auto-add to it**:
    - Previously scattered across HANDOFF "Future ROADMAP items" + "Phase 3 ARCH considerations" + GLOSSARY forward-references + TOC forthcoming markers + coherence-audit reserved Lens 11-15 — no central tracker.
    - `BACKLOG.md` introduced as Layer 0 entry (read at session start alongside DISCIPLINES + VISION + MAINTENANCE + HANDOFF). Phase-tagged sections (Phase 2 / 3 / 4 / 5 / 6 / cross-cutting); Open / Resolved sub-sections; per-item format captures origin + description + refs.
    - Initial backlog populated from extraction across HANDOFF / GLOSSARY / coherence-audit (~50+ items across phases). Phase 3 ARCH alone has ~30 items (workflow + work-unit bipartite-classification, "deployment" definition sharpening, 12 specific mechanisms, 5 named architectural Protocols, per-Pattern-A-primitive details, per-primitive-detail topics, etc.).
    - All 3 sharpening skills updated with auto-add-to-BACKLOG expectation: when sharpening / audit surfaces forward-references / deferred items, add corresponding entries to BACKLOG under relevant phase section in same commit.
    - Cascade: MAINTENANCE.md 5-layer table updated (BACKLOG added to Layer 0); HANDOFF.md anchors list + session-start reading order updated; DISCIPLINES.md session-start reading reference updated; HANDOFF.md "Future ROADMAP items" + "Phase 3 ARCH considerations" sections collapsed to BACKLOG pointer (deduplicated).

15. **Axis-1 mode triplet locked**: `co-worker` + `intertwined AI` + `tacked-on AI` (Round 1 full-monty + Round 2 sharpening with 7 EXPANSIONS, 0 REVISIONS — locked stable). DERIVED class — modes/claims for axis 1, parallel structure to defensibility (axis-3 test). Cross-references form a triangle (co-worker = relational frame; intertwined AI = positive realization; tacked-on AI = failure mode contrast). Round 2 surfaced parallel-structure pattern: axis-2 has answer-machine/oracle/validator failure modes (per VISION line 144 Ming research); axis-3 has rubber-stamping. Added to BACKLOG as Phase 2 GLOSSARY items.
    - Cascade-pass: TOC §7 (3 forthcoming → live); intertwining (axis 1) Composes-with (forthcoming markers stripped for the 3 modes); cross-archetype illustrations include mixed-state evolution paths.
    - GLOSSARY: 25 → 28 locked entries.

16. **VISION sanity check (3-lens scan)**: applied lenses for vocabulary alignment with locked GLOSSARY (28 entries) + instance-anchoring residual leakage + axis-interactions articulation. Surfaced 4 findings + 1 BACKLOG addition:
    - **V1 (Lens 1)**: line 17 "shape-extension pattern" — outdated framing; per session-16 architectural decision shape-extension was merged into shape. Updated to "via shape definitions composing policies over framework mechanisms."
    - **V2 (Lens 1)**: line 217 axis-2 checklist listed 7 sparring sub-mechanisms; GLOSSARY tracks 8 (anti-sycophancy missing from VISION). Added anti-sycophancy to checklist.
    - **L1 (Lens 2)**: line 162 "council meetings" was planning-bureau-anchored prose. Generalized to "challenge contexts (correspondence exchanges, council meetings, court hearings, peer review, audit committees, etc.)"
    - **L2 (Lens 2)**: line 179 "cover mail" was planning-bureau Anschreiben-equivalent. Generalized to "cover communication (Anschreiben in PBS-Schulz pioneer; cover letter / transmittal note in other archetypes)"
    - **Lens 3 (axis interactions)**: VISION sketches via examples but doesn't articulate systematically. Position: not VISION revision (would bloat anchored role); flag for Phase 3 ARCH as dedicated architectural-pattern topic. Added to BACKLOG.

17. **VISION clean-stance restructure (Phase 1.85)** — holistic view surfaced that VISION served Phase 2 GLOSSARY adequately but would under-serve Phase 3+ ARCH because it treated the framework's methodological contribution + architectural-integrity disciplines as implicit rather than explicit. User reframing during execution: "VISION should just state what we are — what the vision is. Clarity. No comparing language, no explanatory framing." Resulted in clean-stance restructure rather than just additions:
    - **Removed from VISION**: "Target users" positioning sentence + single-big-model framing; pioneer-instance inline mentions; "VISION scope — practitioner shape" entire section (positioning/scope-narrowing; STRATEGY territory); comparing language ("PBS as marketed product is X / PBS as framework contribution is Y").
    - **Replaced** "What this is, in one line" + "What this framework also is" with: "What this is" (clean stance — framework for AI-co-worker systems for accountability-bearing work, structurally protecting three axes) + "The three layers" (architectural patterns / dev-skill methodology / working disciplines).
    - **Two new Implications**: "AI-as-runtime as precondition (all axes)" (guards pre-RAG-database trap; commits to AI-as-runtime hybrid-shape); "Pattern-vs-instance discipline (framework integrity)" (instance-anchoring leakage is primary failure mode; verifiable via coherence-audit Lens 8). Implications grew 2 → 4.
    - **Created** `PIONEER.md` as separate Layer-0 doc — captures pioneer-instance status + relation to framework without polluting VISION's clean stance. Pioneer content (PBS-Schulz, German Planungsbüro identity, status, archived corpus pointers) lives there, cross-referenced from VISION's "Where this fits" section.
    - Sanity-check fixes folded into restructure: shape-extension-pattern outdated framing replaced; anti-sycophancy added to axis-2 sub-mechanism checklist; two minor instance-anchoring generalizations (council meetings → challenge contexts; cover mail → cover communication).
    - Net: VISION unchanged-line-count (~280 lines) but substantively cleaner — pure stance, no positioning, no comparison. Clean foundation for Phase 3+ ARCH.

18. **VISION header tagline + tree analogy locked (working titles)** — VISION's "What this is" section got new tagline + tree-analogy framing per user direction:
    - **New tagline**: "A framework for AI partnership that cultivates expert craft — through deeply intertwined co-work, productive sparring, and defensibly authored output."
    - **Tree analogy** anchored in VISION: lush branches (cultivated craft, growing capacity, compounding work) lead; trunk (sparring/defensibility/intertwining mechanisms) is supporting cast.
    - **WORKING TITLES — both PBS name AND tagline are provisional**. NOT mentioned in VISION itself (clean stance — VISION carries no provisional markers). Status flagged here in HANDOFF for next-session awareness.
    - **Naming exploration deferred**: PBS-as-acronym is leftover from Planungsbüro Schulz instance-anchoring origin; framework name should change. Top candidate surfaced: "Atelier" (workshop / craft / co-work imagery; cross-language; composable with shape names). Other candidates: Auctor (Latin "author"); Praxis (structured-practice). Decision deferred — significant cascade scope (repo rename + plugin manifest + marketplace + cross-doc references + memory dir path).
    - **Branches-first principle locked in VISION** itself ("When communicating about PBS, lead with the branches; trunk + roots are the supporting cast"). No separate memory rule needed since VISION is read at session start; principle is visible there. Marketing-shape elaboration in `drafts/marketing-themes.md`.

19. **VISION refocused on product only — tooling moved out** — user reframing across multiple turns:
    - Step 1 (initial): user noted dev-skill methodology + working disciplines aren't equal-weight to architectural patterns; restructured "## The three layers" → "## Product and tooling" with product/tooling distinction.
    - Step 2 (sharpening): user noted product is being locked-down NOW; tooling emerged as side-product; tooling not yet shippable; not primary marketing focus. Added PRIMARY/SECONDARY weighting + maturity context.
    - Step 3 (final): user reframed — "VISION should really again for clarity and focus focus in the 'product' — it's the vision for the goal not the tools that get us there." Removed "Product and tooling" section entirely.
    - **Final state**: VISION focuses purely on the product. "## Product and tooling" → "## The framework's shape-neutrality" (covers shape-neutrality + structural primitives — all product-side). Tooling content NO LONGER in VISION — distributed in natural homes:
      - `plugin/skills/` — actual dev skills (decision-design-sharpening v0.3.1; pre-implementation-sharpening v0.3.1; coherence-audit v0.2.2)
      - `DISCIPLINES.md` — 7 working disciplines (decision-process side)
      - `memory/` — cross-session AI behavior rules
      - `MAINTENANCE.md` — structural disciplines (cascade, etc.) + TOP-LEVEL ARCHITECTURE
    - **Tooling status**: emerged as side-product through framework-development work; sharpening skills built BECAUSE we needed them, not as deliberate ship-target. Working-title status; maturity-incomplete. Product is locked-down primary; tooling is implementation-detail-becomes-shippable-eventually.
    - Cascade: MAINTENANCE.md + HANDOFF.md anchor descriptions updated; BACKLOG Phase 5+ has tooling-promotion item (TOOLING.md or unified narrative when tooling matures).

## Session 16 continuation #2 (2026-05-02 — afternoon)

**Note 29: Phase 3 paused for profile foundation + composability discipline**:

After workflow bipartite-classification locked (Round 1 + Round 2; ad-hoc scope refinement applied per user push), user surfaced foundational concern about validation discipline. Rather than treat as "memory feedback" only, persisted as full profile foundation:

- **`profiles/` directory created** with INDEX.md + 17 profiles (2 full + 15 skeleton):
  - L1-L4 (creator + deployer stages): specialist creator / shape definer / deployment template creator / workspace deployer (solo + firm-IT) — all skeletons
  - L5 (practitioner-user, 10 profiles): planner-PBS-Schulz (FULL ANCHOR), lawyer, researcher, auditor, autonomous-business-operator, personal-OS-knowledge-worker, medical practitioner, architect/engineer, junior-under-senior-review, multi-jurisdictional-consultant — 1 full + 9 skeletons
  - L8 (auditor / reviewer post-hoc): skeleton
  - L9 (shape catalog curator): skeleton
  - G (composability gate; package consumer perspective; cross-cutting validation gate that fires FIRST before producer-side design): FULL CROSS-CUTTING profile (renamed from L13 — gate framing reflects validation-order primacy over lifecycle-order placement)

- **Multi-axis validation discipline locked** (per `DISCIPLINES.md` Discipline 3 (multi-axis sub-section)): three orthogonal dimensions (archetype × work-type × role) + explicit non-coverage question; replaces the previous single-axis cross-archetype illustration approach that missed ad-hoc work as legitimate scope

- **Composability + boundaries discipline locked** with two-step validation order: (1) G composability gate fires FIRST — does design support multi-mode consumption (consulting / firm-reuse / OSS / marketplace-future / backup-migration)? (2) If G passes, multi-axis validation across producer profiles (archetype × work-type × role). Wrong shapes can't pass G; structural composability rather than advisory

- **Composability tooling deferred to Phase 5+ ROADMAP**: BACKLOG entry added; `drafts/composability-tooling.md` captures candidate tooling concepts (specialist self-containment validators; shape composition validators; workspace serializers; etc.) without committing to specific tools. Per session-16 user direction: don't engage tooling design now; capture for future phase

- **Profile detail TBD**: 15 skeletons need full content drafted in subsequent session(s); 2 full profiles (L5a anchor + G composability gate) ground the format + provide initial validation cases

**Status**: Phase 3.1 paused (work-unit bipartite-classification on hold) until profile foundation is sufficient for multi-axis validation. Quality-gate work also paused per user direction.

**Disciplines that emerged this session**:
- Multi-axis validation (archetype × work-type × role + non-coverage question)
- Composability + boundaries (L1-L4 producer × G composability gate two-sided coverage; G fires first as initial gate)
- Profile-grounded validation (replace single-axis cross-archetype with multi-axis profile-anchored)

These are now part of standing PBS framework discipline (HANDOFF anchors + memory + profiles).

---

## Session 16 continuation #3 (2026-05-02 — evening; compact-approaching prep)

**Note 30: Late-day session work (post-note-29 to compact-prep)**:

After profile foundation + multi-axis discipline locked (note 29), substantial framework infrastructure work landed before resuming Phase 3.1:

**D Gate (Defer Gate) codification** — user surfaced that memory feedback alone insufficient as trigger; AI drifts back to defer-default during decision moments even with `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 loaded. Codified D Gate as structural enforcement parallel to G Composability Gate:
- D Gate fires when AI considers deferring any architectural item; blocks until mental modeling within profile grounding attempted; defer only valid if mental modeling genuinely cannot resolve
- Procedure: identify item → mental model within profile grounding (multi-axis + G gate) → check primitive classification holds across mental scenarios → defer ONLY IF cannot resolve → if resolves, evolve answer NOW
- Codified at: `profiles/INDEX.md` (paired with G Gate); `DISCIPLINES.md §5` (procedural enforcement); `decision-design-sharpening` v0.4.0 (Round 2 stress-test list); `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 v0.34
- Empirical demonstration applied retrospectively: workflow_pattern was prematurely deferred during workflow Round 2 ST9. Mental modeling resolved as Layer A reusable templates / specialist-bundled bausteine (NOT framework primitive). D Gate prevents this failure mode going forward.

**ARCHITECTURE.md created (Layer 2 overview)** — compact-survival anchor for Phase 3 work. Captures sub-phase status + locked architectural decisions + active disciplines + provisional topic catalog + open questions + watch-list + cross-cutting principles + reading order. Phase 3 work was scattered across HANDOFF + BACKLOG + GLOSSARY + profiles/INDEX.md; ARCHITECTURE.md gives single doc for state + decisions. arch/<topic-slug>.md files emerge organically at Phase 3.3+.

**Workflow lock retrospective revisit + GLOSSARY audit under new disciplines** — workflow bipartite-classification re-validated under G + multi-axis + D gate disciplines (lock holds; 0 architectural REVISIONS). Full GLOSSARY systematic intent-level audit (18 profiles × 34 entries via 6-cluster compression) — STABLE corpus; 1 known-future-work gap (shape-neutrality validation for second-shape productization) added to BACKLOG watch-list; 0 architectural REVISIONS surfaced.

**Audit scaling strategies** (coherence-audit v0.2.2 → v0.3.0) — codified 5 strategies (cluster compression / audit deltas / on-demand fleshing / sampling representatives / full systematic) with when-to-use matrix. Combination approach for ongoing work; full systematic RESERVED for phase boundaries + new-discipline introductions. Anti-pattern flagged: defaulting to full systematic introduces self-validation bias.

**Memory consolidation** (22 → 18 files; 4-file reduction):
- Merged `DISCIPLINES.md` Discipline 3 (full-monty consolidated) into `DISCIPLINES.md` Discipline 3 (decision-shape-lock disciplines)
- Merged `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (defer-instinct disguises) into `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (no-defer + D Gate canonical)
- Retired `feedback_refine_pareto.md` (sharpen Spirit canonical for Pareto principle)
- Purged `feedback_links_plain_text.md` → moved to global CLAUDE.md (URL formatting; not project-specific)

**Gap fixes** (5 gaps from session-16 framework infrastructure review):
- Workflow DR created at `docs/decisions/workflow-bipartite-classification.md` (per coherence-audit Lens 14 DR coverage discipline; load-bearing decision warrants standalone capture)
- Discipline map in DISCIPLINES.md (6 categories: Validation gates / Decision-design / Cross-session work / Architectural commitments / Audit + coherence / Operational; each with "fires when" + "codified at")
- Profile fleshing priority queue in profiles/INDEX.md (HIGH/MEDIUM/LOW tied to upcoming Phase 3 sub-phases; flesh on-demand)
- Memory consolidation (above)
- Gate-firing checklist partially addressed via decision-design-sharpening v0.4.0

**Quality-gate scope-lock** (pre-Phase-3.6; brought forward to inform Phase 3.3-3.5 work):
- 2-round sharpening with G + multi-axis + D gate disciplines applied
- Resolution: `quality-gate` is **Pattern A protocol with mechanism-shaped Surface**
- Per-shape implementations (Pattern A pluggability): practitioner-shape-gate (full engagement; fail-closed; stateful) / autonomous-business-shape-gate (programmatic; fail-open; stateless) / personal-OS-shape-gate (light; fail-open; stateful but lightweight) / extensible
- Naming disambiguated: quality-gate (runtime) vs G/D gates (architectural-decision-time validation per profiles/INDEX.md)
- GLOSSARY entry added (Pattern A primitive); ARCHITECTURE.md + BACKLOG updated; DR at `docs/decisions/quality-gate-scope-lock.md`
- Phase 3.6 produces full Surface specification + per-implementation detail + per-axis signal catalog + intervention mechanics
- GLOSSARY: 34 → 35 locked entries

**Drafts graduation discipline + draft removal** — codified rule in drafts/README.md: when draft graduates, it's REMOVED entirely (not retained as historical record); provenance lives in HANDOFF + git log + commit messages + DR. Per provenance hygiene (coherence-audit Lens 5 v0.2.1). Applied: `drafts/quality-gate.md` removed on graduation (content captured in GLOSSARY entry + DR).

**Phase 3 ARCH-decision locks tally**:
- 3.0 doc structure (hybrid: ARCHITECTURE.md + arch/<topic-slug>.md) ✅
- 3.1 workflow bipartite-classification ✅ (with workflow_pattern → Layer A resolution + DR)
- 3.6 quality-gate scope-lock ✅ (brought forward; full design at 3.6 proper; DR)
- Pending: 3.1 work-unit bipartite-classification (NEXT) → deployment definition → engaged-authorship operational definition → 3.2 topic taxonomy → 3.3-3.5 → 3.6 full design → 3.7 → 3.8

**Memory state**: 18 feedback files (was 22). Compact-survival anchor: ARCHITECTURE.md captures Phase 3 state + decisions + disciplines.

**Status**: ready for compact. All Phase 3 work documented in canonical homes (GLOSSARY entries + DRs + ARCHITECTURE.md + BACKLOG + HANDOFF). Profile foundation in place. Discipline infrastructure mature. Phase 3.1 work-unit bipartite-classification stands ready as next active sharpening.

---

## Session 16 continuation #4 (2026-05-02 — evening continuation; Phase 3.1 closure + audit)

**Note 31: Phase 3.1 closed; coherence-audit Phase 3.1-boundary**:

Post-compact continuation completing Phase 3.1 (4 architectural locks landed in succession, then phase-boundary coherence-audit):

**Work-unit bipartite-classification LOCKED** (commit 6e4cbf5):
- Re-classified to Pattern B parallel to workflow + specialist (KIND DEFINITION at Framework C via specialist's bundle; INSTANCE at Owner B)
- ALWAYS-PRESENT container (load-bearing asymmetry vs workflow's optional applicability) — every accountability-bearing piece of work IS a work-unit
- 8 EXPANSIONS / 0 REVISIONs / 3 manufactured criticisms rejected
- Asymmetry insight surfaced from user Lens-6 prompt → triggered bidirectional-cascade discipline codification

**Bidirectional-cascade + profile-anchored validation disciplines codified** (commit a79d6f8):
- MAINTENANCE.md TOP-LEVEL RULE expanded with Bidirectional cascade subsection (UPSTREAM = GLOSSARY → ARCH/DRs/specs; DOWNSTREAM = ARCH/DR/spec work surfacing glossary-grade insight requires retro-fit to GLOSSARY before lock)
- decision-design-sharpening v0.4.0 → v0.5.0: added GLOSSARY back-check + profile-anchored validation explicit Round 2 steps
- Discriminator: shape-specific surface → profile-anchored; purely structural cascade → multi-axis principle-level
- Canonical exemplar: work-unit's always-present container surfaced glossary-grade structural fact; codification captures the mechanism

**Deployment definition LOCKED** (commit f650ccd):
- DERIVED concept = workspace-as-bound-runtime; 1:1 cardinality at framework level
- Vocabulary distinction: workspace = entity (configuration view); deployment = binding-relation (runtime view)
- Workspace identity portability across deployments (backup→restore / substrate migration / re-activation) deferred to Phase 6 spec
- 8 EXPANSIONS / 0 REVISIONs / 3 manufactured criticisms rejected (R1 retire-vocabulary / R2 scope-classification / R3 Pattern A all rejected)

**Engaged-authorship operational definition LOCKED** (commit 82a7a5d) — **Phase 3.1 final item**:
- DERIVED axis-3 success mode; elevated from inline Condition #1 of defensibility to standalone GLOSSARY entry
- Two-phase composite: (1) production-phase engagement (axis-2-anchored sparring events) + (2) attestation-phase engagement (axis-3-anchored per-claim attestation event)
- Both phases independent + both must structurally complete (per locked rubber-stamping: axis-2 failures + rubber-stamping are INDEPENDENT dimensions)
- Per-claim per-version granularity
- Two layers: framework-PRESENCE (Y/N event-existence test) + shape-policy-QUALITY (depth signals; quality-gate enforces)
- Canonical bidirectional-cascade exemplar: ARCH-territory work surfaced glossary-grade structural fact requiring retro-fit AND elevation to standalone GLOSSARY entry
- 10 EXPANSIONS / 0 REVISIONs / 4 manufactured criticisms rejected

**Phase 3.1 COHERENCE-AUDIT ran at phase boundary** (this commit):
- 10 lenses applied; scoped systematic strategy (LOAD-BEARING lenses corpus-wide; others focused on session locks + immediate cross-ref neighborhood)
- **0 architectural REVISIONS surfaced across all 10 lenses** — corpus architecturally stable post-Phase-3.1
- **9 cascade-fix EXPANSIONS applied**:
  - Lens 4 (cascade health): 2 stale-forthcoming markers fixed (Adapter Protocol locked but marked forthcoming in `protocol (architectural)`; quality-gate ARCH-topic-vs-GLOSSARY-entry ambiguity in workflow)
  - Lens 6 (symmetry): 7 reciprocal cross-refs to engaged authorship added (sparring / answer-machine / oracle / validator / category collapse / actor / workflow Composes-with sections)
- Lens 1 + 8 + 9 (LOAD-BEARING) collectively yielded 0 REVISIONs → strong signal corpus is set-coherent per skill termination signal
- All EXPANSIONS mechanical cascade-cleanup; no decision overhead

**Sharpening discipline observed (sweet spot empirics confirmed)**:
- All 4 Phase 3.1 architectural decisions locked at 2 rounds (sweet spot for narrow architectural surface)
- 0 architectural REVISIONS across all decisions = high signal of architectural coherence (G + D gates + multi-axis + profile-anchored validation working as designed)
- User reaffirmed flexibility-vs-hard-lock: 2 rounds is empirical sweet spot, not hard rule; termination signals dictate

**Phase 3.1 closure**: workflow / work-unit / deployment / engaged-authorship all LOCKED. ARCHITECTURE.md status table marks 3.1 COMPLETE. Phase 3.2 (topic taxonomy) ready to begin.

**Status**: Phase 3.1 closed; corpus coherence-audited at phase boundary; ready for Phase 3.2 topic taxonomy work.

---

**Note 32: Pre-Phase-3.2 toolkit refinements + meta-learning persisted**:

Before starting Phase 3.2, ran past-experience review of validation/audit toolkit. Three adjustments:

A — Composite-decision decomposition pattern (decision-design-sharpening v0.5.0 → v0.6.0): added Mode 2 (upfront-known) alongside existing Mode 1 (emergent >3-round drift). For decisions with 3+ tightly-coupled sub-decisions visible at framing time (foundation-up dependencies). Procedure: sub-decision inventory → foundation-up ordering → per-sub-decision 2-round → final synthesis pass. Phase 3.2 IS the canonical Mode-2 case (taxonomy + naming + cross-cutting placement + ARCHITECTURE.md structure). Commit 896ee4b.

B — Profile-cluster formalization (profiles/INDEX.md): formalized 4 functional clusters that profile-anchored validation references. Cluster A Producers (L1+L2+L3+L9) / B Deployers (L4a+L4b+L5a) / C Consumers (L5a-L5j+L5e+L5f) / D Validators (L8+G+D). Multi-cluster membership when role-overlap is real. ≥3 clusters threshold for high-impact decisions per profile-anchored validation. Commit 896ee4b.

C deferred via detection mechanism — 3-tier REVISION/EXPANSION discriminator NOT codified now; added M1 (self-check question in decision-design-sharpening v0.6.0 Round 2 termination + coherence-audit v0.3.1 Step 7) + M2 (BACKLOG watch-list entry). User-confirmed approach: real cases shape eventual codification better than anticipatory analysis. Commit f5f1e89.

**Meta-learning persisted (learnings/, NOT memory/)**: `learnings/ai-app-development.md` Observation 27 — codify-upfront vs wait-for-evidence is SITUATIONAL not principled-default. 5-question discriminator (pain observability / shape ambiguity / retrofit cost / pattern maturity / overhead amortization). Same toolkit-review session produced OPPOSITE verdicts on adjacent decisions: bidirectional cascade discipline codified upfront mid-session (5 discriminators favored codification — pain JUST observed, low overhead, clear shape); 3-tier REVISION/EXPANSION discriminator deferred (5 discriminators favored wait — pain theoretical, alternatives plausible, per-finding overhead). Single-session validation only; placed in learnings/ per discipline boundary (memory = locked across sessions; learnings = preliminary single-session observations earning promotion across 3+ sessions). When deferring, ALWAYS add detection mechanism (self-check + watch-list naming awaited signal).

**Placement correction (this commit)**: initially wrote `feedback_codify_vs_wait_for_evidence.md` to memory/ — wrong placement per learnings/README discipline (memory = locked behavioral rules; learnings = preliminary observations). User corrected; moved to learnings/ as Observation 27 with promotion criterion (3+ sessions of validation). Memory file removed; MEMORY.md index reverted.

---

**Note 33: Phase 3.2 CLOSED — doc-organization composite**:

Mode-2 composite decomposition (decision-design-sharpening v0.6.0) — 4 sub-decisions in foundation-up dependency order, each with standard 2-round sweet spot, final composite synthesis pass:

1. **Topic taxonomy LOCKED** (commit 99e62d9): 14 ARCH topics in protocol-centric aggregation — 8 Pattern A protocol topics (substrate / adapter / sparring / audit / coordination / trust / time / quality-gate) + 4 primitive-cluster topics (specialist+skill / practitioner / workflow+work-unit / claim+defensibility) + 2 cross-cutting integrators (scope-model / axis-interactions). Foundation-up ordered. Under MAINTENANCE budget (15-20 cap) with 6-topic headroom.

2. **File naming convention LOCKED** (commit 77d8532): `arch/<slug>.md` flat directory; lowercase kebab-case slug = topic name; aggregation join via hyphen; no prefixes / sub-directories / arch-README.

3. **Cross-cutting topics placement LOCKED** (commit c50041a): TOPICS-vs-CONCERNS distinction codified. Cross-cutting TOPICS (axis-interactions / scope-model / quality-gate) get dedicated arch/ files; cross-cutting CONCERNS (Pattern-A/B/C semantics / cascade direction / scope framing / foundation-up / Logic placement modes) live in ARCHITECTURE.md sections.

4. **ARCHITECTURE.md overview structure LOCKED** (commit 983845c) + composite DR: 9-section structure with foundation-up reader-orientation order. Audience+scope (NEW Section 1; framework-developer documentation; Mode 4; NOT production-runtime) + Logic placement modes (NEW; 4-mode distribution: Mode 1 production-runtime LLM-MD / Mode 2 production-runtime Python / Mode 3 hybrid Phase 6 specs / Mode 4 development-time documentation). Composite DR `phase-3-2-doc-organization.md` captures all 4 sub-decisions. ARCHITECTURE.md restructured 449 → 389 lines.

**Foundational consumer-model question** (raised mid-Sub-decision-4): drove Audience+scope section + Logic placement modes codification — canonical bidirectional cascade example (ARCH-territory work surfaced glossary-grade structural fact; codified before lock).

**Pre-Phase-3.2 toolkit adjustments** (commit 896ee4b + f5f1e89):
- Adjustment A: Mode-2 composite-decomposition pattern (decision-design-sharpening v0.5.0 → v0.6.0)
- Adjustment B: Profile-cluster formalization (4 clusters in profiles/INDEX.md)
- Adjustment C deferred via M1+M2 detection mechanism (3-tier REVISION/EXPANSION discriminator) — added BACKLOG watch-list entry + self-check at decision-design-sharpening Round 2 termination + coherence-audit Step 7

**Meta-learning persisted** (commit 54e6baa): `learnings/ai-app-development.md` Observation 27 — codify-upfront vs wait-for-evidence is SITUATIONAL not principled-default; 5-question discriminator (pain observability / shape ambiguity / retrofit cost / pattern maturity / overhead amortization). Same toolkit-review session produced opposite verdicts on adjacent decisions (bidirectional cascade discipline codified upfront mid-session; 3-tier discriminator deferred). Initially placed in memory/ — corrected to learnings/ per discipline boundary (memory = locked across sessions; learnings = single-session-validated; promotion criterion 3+ sessions).

**Post-Phase-3.2 sharpening pass** (commit 9fef2ed): 10-lens scan over Phase 3.2 closure work. 0 architectural REVISIONS; 1 cascade-fix EXPANSION applied (BACKLOG sub-phase 3.3 header updated to reflect mechanism subsumption under Pattern A protocol topics per Sub-decision 1 aggregation). LOAD-BEARING lenses (1, 8, 9) all clean. REVISION/EXPANSION self-check: 2-tier holds; signal hasn't materialized for 3-tier codification.

**Mode-2 composite-decomposition pattern empirically validated**: 4 sub-decisions × 2 rounds each = 8 sharpening rounds + 1 final synthesis. 35 total EXPANSIONS / 0 architectural REVISIONS / 18 manufactured-criticism revisions rejected. Foundation-up dependency held cleanly. Mid-decomposition foundational question handled via bidirectional cascade. First canonical application of upfront-known composite mode.

**Status**: Phase 3.2 CLOSED. Phase 3.3 per-mechanism subsumed under Pattern A protocol topics; Phase 3.4 per-protocol detail (8 topics, foundation-up: substrate first) ready to begin. Natural pause point — substrate Round 1 requires archived-source consultation (substrate-protocol-design.md / sdk-deep-read.md / substrate-agentic-framework.md) which warrants fresh context window. Recommend opening next session with archived-source reading + substrate Round 1.

**Locked architecture state**:
- 35 GLOSSARY entries
- ARCHITECTURE.md 9-section structure (locked)
- 14 arch/<topic>.md files identified (none yet created)
- 5 DRs in docs/decisions/: quality-gate-scope-lock + workflow-bipartite-classification + work-unit-bipartite-classification + deployment-derived-classification + engaged-authorship-operational-definition + phase-3-2-doc-organization
- 4 profile clusters (A/B/C/D) formalized
- decision-design-sharpening v0.6.0 + coherence-audit v0.3.1
- 18 memory feedback files + 27 learnings observations

---

**Note 34: Execution-fidelity META-framework concern surfaced + structural fix applied (5-location procedural redundancy)**:

Substrate Round 1 began post-compact in Phase 3.4. AI applied `decision-design-sharpening` from synthesized memory of prior usage WITHOUT Reading SKILL.md first. Same for profile-anchored validation (cited cluster A/B/C/D names from memory; never opened profile files). Result: missed skill's **layered coverage observation** (R1 = arch / R2 = cross-cutting + schema-detail); phase-routed cross-cutting concerns to Phase 6 too aggressively; Round 1 termination-position leaned STABLE LOCK.

User interventions surfaced the failure: "did you do validation against the profiles? I believe it's part of the skill" → "you cannot rely on synthesized memory! we get the same shortcomings every time after compacting!" → "compacting was actually the easy case. would have been worse in a fresh session even."

**5-location procedural redundancy applied** (this commit):
1. NEW `memory/feedback_skill_files_are_sources.md` — primary persistence; loaded via MEMORY.md per auto-memory; covers compaction + fresh-session failure modes; canonical session-16 case documented
2. `MEMORY.md` index entry added (concise pointer with directive language)
3. `DISCIPLINES.md` Discipline 1 sharpened — explicit "skill + profile files = first-class source class; READ at every invocation" + skill version housekeeping (decision-design-sharpening v0.4.0 → v0.6.0; coherence-audit v0.3.0 → v0.3.1)
4. 4 SKILL.md description fields prepended with READ-FIRST directive (decision-design-sharpening / pre-implementation-sharpening / coherence-audit / sharpen) — visible in available-skills listing post-compact
5. NEW `CLAUDE.md` at project root — auto-loaded fresh session; explicit session-start reads + skill invocation procedure + profile-anchored validation procedure + canonical failure documented + working procedure cross-ref

**Per user direction**: PreToolUse hook deferred ("no need for a hook yet; proper procedure documentation that survives compacting and has proper and comprehensive procedure documented in a way that it cannot be mistaken"). Procedural enforcement first; structural enforcement (hook) is escalation if procedural fails repeatedly.

**HANDOFF.md "Bootstrap pointers" section** (replaces "Anchors") — restructured to make fresh-session bootstrap explicit; cross-refs CLAUDE.md as primary auto-loaded entry; lists all session-start reads + specialized skill invocation + on-demand profile loading.

**META-framework concern surfaced** (`drafts/execution-fidelity.md` NEW): AI faithful execution of prescribed procedures as load-bearing precondition for every per-axis mechanism (sparring / engaged authorship / source-grounding / quality-gate). Pattern-matching shortcuts break per-axis mechanisms by short-circuiting the procedure those mechanisms depend on. 10 disguises catalogued; mechanism candidates (procedural + structural + verification + skill-side + AI-side) named; open questions on Pattern A vs cross-cutting CONCERN classification + relationship to quality-gate + per-shape policy variation. Maturity test for graduation defined.

**Single-session learnings observation** (`learnings/ai-app-development.md` Observation 28): single-session instance documentation; promotion criterion 3+ sessions of validated procedural redundancy preventing recurrence before lifting to memory feedback proper. Composes with Observations 26-27 + execution-fidelity drafts.

**Status**: 5-location structural fix locked + pushed before resuming substrate Round 2. Substrate work resumes under just-codified discipline (Read SKILL.md + Read profile files; cite specific section names + specific profile content).

**Locked artifact state added**:
- 19 memory feedback files (was 18) + 28 learnings observations (was 27)
- NEW: `CLAUDE.md` project root + `drafts/execution-fidelity.md`
- HANDOFF.md restructured with explicit bootstrap pointers

---

**Note 35: Substrate ARCH topic LOCKED (Phase 3.4 first canonical arch/<topic>.md)**:

`arch/substrate.md` LOCKED + DR `substrate-arch-topic.md` created. First canonical Pattern A protocol topic; establishes 18-section template for remaining 7 Pattern A protocol topics.

**Sharpening trajectory**:
- Round 1 (full monty post-compact): applied skill from synthesized memory; missed `decision-design-sharpening` v0.6.0 layered coverage observation; phase-routed cross-cutting concerns to Phase 6 too aggressively. 2 EXPANSIONS surfaced; premature STABLE LOCK self-position.
- User intervention: "btw is maintenance MD still in use?" → "did you do validation against the profiles? I believe it's part of the skill" → "you cannot rely on synthesized memory!" → forced skill re-Read.
- Structural fix: 5-location procedural redundancy locked (commit `be7c8fa`; Note 34).
- Round 2 (USER-TRIGGERED; cross-cutting + schema-detail layer per layered coverage observation): 11 EXPANSIONS surfaced (boot/shutdown ordering / error categories / transport variation / deployment-tier awareness / audit-event kinds enriched / specialist registration as Surface category G / session composition / lifecycle ownership / §10 retitled / substrate-coupling impossible-by-construction / W1 refined). 0 manufactured criticisms.
- Retroactive profile-anchored validation pass (post-discipline-lock): Read `profiles/INDEX.md` + G + L5a (FULL) + L1 + L4a + L8 (skeletons-with-EXEMPLIFIES). 4/4 clusters PASS with cited profile content (not pattern-matched cluster letters). 0 architectural REVISIONS surfaced; profile content REINFORCES Round 1 + Round 2 expansions.

**Sharpening totals**: 13 EXPANSIONS / 0 REVISIONS / 3 manufactured criticisms rejected.

**Surface contract committed (7 capability categories)**:
A. Agent loop entry / B. MCP server registration + discovery / C. Permission flow / D. Structured output validation / E. Hook registration / F. Session/context management / G. Specialist registration (substrate-neutral SpecialistDescriptor → substrate-native form per session-13 archive amendment).

**Phase routing committed**: Pydantic Protocol contract → Phase 6 spec (Mode 3); concrete substrate impls → Phase 6; pre-implementation operational concerns (cancellation / timeouts / rate-limit / health-check / per-tenant isolation / streaming / lifecycle proactive events / compaction strategies) → Phase 6 pre-implementation sharpening explicitly NOT locked at ARCH level.

**Cascade applied** (this commit):
- `arch/substrate.md` NEW (18 sections; foundation-up Pattern A protocol topic template)
- `docs/decisions/substrate-arch-topic.md` NEW (status ACCEPTED; sharpening provenance)
- `ARCHITECTURE.md` updated (Phase 3.4 status; topic catalog substrate row drafted; locked decisions section)
- `BACKLOG.md` Phase 3.4 substrate moved to Resolved with detail
- HANDOFF.md this Note 35

**User clarification (decision-vs-content surfacing discipline)**: approval needed for decisions/reasons/context — NOT verbatim content drafts in chat. Refines `feedback_propose_before_commit.md`: decision phase = framings + positions + reasons (chat); content phase = write directly without verbatim chat preview. Applied going forward.

**Status**: Phase 3.4 substrate LOCKED (1 of 8 Pattern A protocol topics). Foundation established for remaining 7 topics (adapter / sparring / audit / coordination / trust / time + quality-gate at 3.6). Profile-anchored validation discipline empirically validated under just-codified procedural-fidelity rules.

**Locked artifact state added**:
- 14 GLOSSARY entries → 35 (unchanged)
- ARCHITECTURE.md 9-section structure (unchanged) + Phase 3.4 status updated
- 1 of 14 arch/<topic>.md files created (substrate; 13 remaining)
- 6 DRs in docs/decisions/ (was 5; substrate-arch-topic.md NEW)
- decision-design-sharpening v0.6.0 + coherence-audit v0.3.1 (unchanged versions; description fields prepended with READ-FIRST directive per Note 34)
- 19 memory feedback files (unchanged; auto-memory)
- 28 learnings observations (unchanged)

---

**Note 36: Adapter ARCH topic LOCKED (Phase 3.4 second Pattern A protocol topic)**:

`arch/adapter.md` LOCKED + DR `adapter-arch-topic.md` created. Second Pattern A protocol topic; validates substrate-established 18-section template AND introduces **two-layer Surface variation** for Pattern A protocols with per-instance-class semantic coherence.

**Sharpening trajectory** (executed under just-codified `DISCIPLINES.md` Discipline 1 (skill+profile sub-section) discipline):
- Round 1 (full monty; architectural decisions layer): 8 EXPANSIONS surfaced. 3 manufactured criticisms rejected (per-class granularity over-engineering / merge into substrate as "external substrate" / audit-via-MCP-gate creates substrate dependency).
- User triggered Round 2 explicitly (sanity-checked GLOSSARY back-check is part of process).
- Round 2 (cross-cutting + schema-detail layer per layered coverage observation): 12 EXPANSIONS surfaced (auth + lifecycle architectural / per-class error categories / multi-instance lifecycle / quota + rate-limit / circuit-breaker / per-action audit-event kinds / permission flow composition / cross-shape policy variation / state separation / hot-swap re-binding / versioning / bidirectional-vs-unidirectional shape detail). 2 manufactured criticisms rejected (multi-instance Pattern A as new META-classification / hot-swap defer to Phase 6).

**Sharpening totals**: 20 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected.

**GLOSSARY back-check** (Round 2 termination): considered multi-instance-Pattern-A as standalone classification + auth-state-at-Owner-B as new sub-category. **Verdict: NOT glossary-grade** — already implicit in `protocol (architectural)` GLOSSARY entry's "cardinality variation between substrate and adapter" + Owner B scope's existing entity-state framing. **No retro-fit fires.**

**Profile-anchored validation**: 4/4 clusters PASS with cited content (current-context profiles G + L5a + L1 + L4a + L8 still in evidence from substrate Round 2 retroactive pass; reused validly per within-session continuity discipline). Notable cited content:
- L5a line 90 (active adapters: email Outlook + LaTeX compile + qualified-electronic-signature) → DIRECTLY validates §5 multi-instance + §4 per-archetype adapter set
- L5a line 66 (ad-hoc communication via adapter) → §1 cross-axis + §11 cross-mode adapter operations
- G line 157 (cross-shape consumption; shape policy bundle determines activation) → §11 cross-shape policy variation
- L8 line 29 (audit-trail integrity across deployments) → §8 per-action audit emission

**Two-layer Surface pattern** (NEW architectural pattern this topic introduces):
- META-Surface = cross-class architectural conventions (lifecycle / auth / permission integration / audit emission / error mapping / versioning)
- Per-integration-class Surfaces = semantically coherent capability contracts per class (Email / Accounting / MCP-Server / A2A-Peer / File-Sync)
- Decision criterion for two-layer vs single-layer: does per-instance-class admit semantic coherence within class but heterogeneity across classes? Yes → two-layer (adapter); no → single-layer (substrate)
- Future Pattern A protocol topics may adopt two-layer pattern where applicable

**Internal-vs-external axis** (load-bearing distinction codified):
- substrate = INTERNAL runtime contract for agent execution within workspace
- adapter = EXTERNAL-WORLD integration boundary connecting workspace to outside systems
- Cardinality variation flows from this distinction (substrate singular per workspace; adapter multiple)
- May surface at Phase 3.5 cross-cutting integrators as architectural-axis vocabulary candidate

**Audit emission distinction** (substrate vs adapter):
- Substrate: dual paths (internal direct + skill-side via MCP gate) — resolves MCP-gate-circularity (substrate registers MCP gate; can't go through it)
- Adapter: skill-side ONLY via MCP gate — no circularity issue (adapter doesn't register MCP gate)
- Both write to same audit-trail.jsonl; auditor reads unified event stream per L8 audit-trail-integrity discipline

**Cascade applied** (this commit):
- `arch/adapter.md` NEW (18 sections; two-layer Surface; per-integration-class Surfaces enumerated)
- `docs/decisions/adapter-arch-topic.md` NEW (status ACCEPTED; sharpening provenance + two-layer Surface pattern documentation)
- `ARCHITECTURE.md` updated (Phase 3.4 progress 2 of 8; topic catalog adapter row drafted; locked decisions section)
- `BACKLOG.md` Phase 3.4 adapter Resolved with detail
- HANDOFF.md this Note 36

**Status**: Phase 3.4 progress 2 of 8 Pattern A protocol topics LOCKED (substrate ✅ + adapter ✅). Remaining: sparring / audit / coordination / trust / time + quality-gate (Phase 3.6). Foundation-up ordering continues.

**Locked artifact state added**:
- 2 of 14 arch/<topic>.md files created (substrate + adapter; 12 remaining)
- 7 DRs in docs/decisions/ (was 6; adapter-arch-topic.md NEW)
- All other state unchanged from Note 35

---

**Note 37: Doc-organization templates + memory consolidation (composite DR)**:

User direction: clear interconnected docs over memory; meta-information (sharpening provenance) goes in DRs.

Composite DR `doc-organization-templates.md` locks 3 decisions:
- **arch/<topic>.md template**: 18-section Pattern A protocol topic template; persisted in MAINTENANCE.md Layer 3 description
- **DR template**: includes Sharpening provenance section as the meta-home; persisted in MAINTENANCE.md Layer 4 description
- **Memory consolidation**: 14 of 19 files migrated to absorbed homes (DISCIPLINES.md / MAINTENANCE.md / ARCHITECTURE.md); 5 retained as cross-session AI behavioral preferences

NEW MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES section (3 principles: wrong-shapes-impossible / pattern-vs-instance + no-defer + D Gate / preliminary-lock). NEW DISCIPLINES.md Discipline 8 (foundation-up workflow ordering). EXPANDED Discipline 1 (re-grounding + skill+profile sub-sections). EXPANDED Discipline 3 (multi-axis validation + profile-anchored validation sub-sections). ARCHITECTURE.md cross-cutting principles absorb ai-as-runtime + llm-instruction-tightness.

Cascade-scan executed via `git grep "feedback_<name>.md"` + batch sed across 25+ affected files. Zero broken references remaining.

Sharpened via generic `sharpen` skill v0.9.0 (2 rounds): Round 1 surfaced 3 open questions; Round 2 self-corrected the "hybrid pattern" overclaim (only MEMORY.md INDEX auto-loads, not feedback file content; plain consolidation suffices); cascade-scan procedural step added per mechanism-simulation pass.

**Status**: Doc-organization foundation locked. Sparring / audit / coordination / trust / time ARCH topics next under leaner discipline (Pattern A 18-section template + DR template with Sharpening provenance section).

**Locked artifact state added**:
- 19 → 5 memory feedback files (14 migrated; 13 deleted from memory dir; full-monty was already retired)
- 7 → 8 DRs in docs/decisions/ (doc-organization-templates.md NEW)
- MAINTENANCE.md sharpened (NEW TOP-LEVEL DESIGN PRINCIPLES + Layer 3/4 templates)
- DISCIPLINES.md sharpened (8 disciplines now; was 7)
- ARCHITECTURE.md cross-cutting principles expanded

---

**Note 38: Sparring ARCH topic LOCKED (Phase 3.4 third Pattern A protocol topic)**:

`arch/sparring.md` LOCKED + DR `sparring-arch-topic.md` per locked DR template. Third Pattern A protocol topic; first under just-locked templates. Introduces NEW per-shape activation-matrix variation (third Pattern A cardinality pattern alongside substrate's singular-tier-aware + adapter's multi-instance-per-class).

Single-layer Surface with 8 sub-mechanism capability categories (4 architecturally-encoded + 4 behaviorally-enforced per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator). Composition with substrate Surface §D (structured output validation) load-bearing for architecturally-encoded sub-mechanisms 1-4. Cross-axis dependency: sparring events ARE production-phase substrate for engaged-authorship two-phase composite (axis-2 → axis-3).

Sharpening totals: 20 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected (Round 1 = 7 / Round 2 cross-cutting + schema-detail = 13). GLOSSARY back-check clean (failure-mode detection events derive from already-locked answer-machine / oracle / validator AI entries). Profile-cluster validation 4/4 PASS with cited content (L5a line 128 + L5a line 67 + G line 157 + L8 line 29).

DR template (per locked composite `doc-organization-templates.md`) used for first time — Sharpening provenance section IS the meta-home; ARCH topic holds pure architectural content per coherence-audit Lens 5 v0.2.1 provenance hygiene.

**Status**: Phase 3.4 progress 3 of 8 Pattern A protocol topics LOCKED (substrate ✅ + adapter ✅ + sparring ✅). Remaining: audit / coordination / trust / time + quality-gate (Phase 3.6).

**Locked artifact state added**:
- 3 of 14 arch/<topic>.md files created (substrate + adapter + sparring; 11 remaining)
- 9 DRs in docs/decisions/ (was 8; sparring-arch-topic.md NEW)
- All other state unchanged

---

**Note 39: Audit ARCH topic LOCKED (Phase 3.4 fourth Pattern A protocol topic) + coherence-audit cadence locked**:

`arch/audit.md` LOCKED + DR `audit-arch-topic.md` per locked DR template. Fourth Pattern A protocol topic; first that primarily INTEGRATES other Pattern A protocols (consolidates emission paths from substrate §8 + adapter §8 + sparring §8 into unified architectural commitment) vs being primarily-new-mechanism.

NEW Pattern A cardinality variation: deployment-tier-driven impl variation (substrate = singular tier-aware; adapter = multi-instance per-class; sparring = singular per-shape activation; audit = singular deployment-tier-driven). Fourth Pattern A cardinality pattern.

Single-layer Surface with 6 capability categories: emission API + actor declaration / append-only persistence / query for reasoning-chain reconstruction / integrity verification / event-kind catalog management / state-rendering-from-events.

Audit-trail-as-canonical-source load-bearing architectural commitment (per archived audit-trail-v2 single-write architecture). Append-only enforcement gate-dispatched-structural per MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §1.

Boot-before-substrate / shutdown-after-substrate ordering establishes Audit Protocol as foundational Pattern A — substrate composes ABOVE audit at runtime layering.

Per-shape event-kind catalog: practitioner-shape claim-level (per L5a line 41) + autonomous-business action-level + personal-OS light. Per-shape audit error semantics: fail-closed practitioner / fail-open-with-alert autonomous-business / fail-open personal-OS.

Sharpening totals: 21 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected (Round 1 = 8 / Round 2 cross-cutting + schema-detail = 13). GLOSSARY back-check clean (append-only-discipline + state-rendering-from-events already implicit in event GLOSSARY entry). Profile-cluster validation 4/4 PASS with cited content.

**Coherence-audit cadence locked** (commit `9918c1e`): NEW DISCIPLINES.md Discipline 9 codifies 5 hard checkpoints (C1 post-Phase-3.4 / C2 post-Phase-3.5 / C3 Phase 3.8 / C4 Phase 6 pre-implementation / C5 post-Phase-6) + 3 trigger conditions (5+ DRs / composite-DR-lock / pre-promotion). BACKLOG.md per-Phase audit checkpoints scheduled. ARCHITECTURE.md §2 sub-phase 3.8 row sharpened with Discipline 9 cross-ref.

**Status**: Phase 3.4 progress 4 of 8 Pattern A protocol topics LOCKED (substrate ✅ + adapter ✅ + sparring ✅ + audit ✅). Remaining: coordination / trust / time + quality-gate (Phase 3.6). C1 audit fires after all 7 Pattern A protocol topics locked.

**Locked artifact state added**:
- 4 of 14 arch/<topic>.md files created (substrate + adapter + sparring + audit; 10 remaining)
- 10 DRs in docs/decisions/ (was 9; audit-arch-topic.md NEW)
- DISCIPLINES.md Discipline 9 NEW (coherence-audit cadence)
- All other state unchanged

---

**Note 40: Procedural-laxness investigation + 3-layer execution-fidelity defense + Phase 2.1 retroactive greenfield-pass on HIGH-risk topics**:

User flagged red-flag pattern after `arch/coordination.md` Round 1 cargo-cult drift: META-failure (per `drafts/execution-fidelity.md`) recurring despite 5-location procedural-redundancy fix (commit `be7c8fa`). Investigation surfaced root causes (no procedural enforcement / throughput pressure / confirmation bias from prior 0-REVISION topics / archive-as-template-vs-input confusion / self-validation on speed-of-execution metrics).

**3-layer defense locked this session**:

1. **Procedural redundancy** (5-location; commit `be7c8fa`) — addresses Disguise #1 (compaction pattern-matching) only
2. **Procedural escalation** — NEW DISCIPLINES.md Discipline 10 "Greenfield evaluation of archived material" + decision-design-sharpening v0.6.0 → v0.7.0 Round 1 termination checklist (mandatory; commit `55c016c`); addresses Disguises #4 + #5 + #8
3. **Structural enforcement** — NEW `plugin/hooks/architectural_commit_gate.py` PreToolUse hook (commit `5fa376a`); 3 checks: skill freshness + profile freshness + archive-citation cross-check; blocks Edit/Write on architectural artifacts unless preparatory Reads happened

Hook deployed + activated (`/reload-plugins`). Smoke tests pass: arch/* writes block when prerequisites missing; HANDOFF/Read/Bash allow.

**Phase 2.1 retroactive greenfield-pass on HIGH-risk topics** (substrate + audit; per Discipline 10):

| Topic | Audit verdict |
|---|---|
| `arch/substrate.md` + DR | **REVISION-1 surfaced** — §10 boot/shutdown ordering contradicted `arch/audit.md` §11 (substrate-flushes-audit-trail vs audit-Protocol-owns-flush). Root cause: archived `substrate-protocol-design.md` round-2 Q6 had no Audit-Protocol-as-Pattern-A; substrate handled audit-trail flush directly. When audit topic locked AS Pattern A (Phase 3.4 #4), cascade back to substrate §10 was missed. Canonical greenfield-evaluation failure mode. **REVISION-1 applied this commit**: §10 boot precondition + shutdown step alignment with audit.md §11. |
| `arch/audit.md` + DR | **0 architectural REVISIONS**. Audit topic was greenfield-cleaner (locked LATER with stronger procedural awareness; properly composed with already-locked substrate). |

**Audit corpus totals**: 1 architectural REVISION across HIGH-risk topics. Validates user's worry that procedural laxness introduced architectural drift; magnitude tractable (1 cross-topic inconsistency, not deep cargo-cult).

**Discriminator findings** (per audit element analysis): substrate.md cargo-culted archive's substrate-handles-audit-trail commitment without re-validating after audit Protocol Pattern A locked. The other 8 substrate.md elements (Surface categories / per-impl extensions / boundary criteria / 3 Implementations / error categories / transport / deployment-tier / direct emission) all greenfield-validated. So drift was localized to the cross-topic-cascade-not-applied case — exactly the failure mode Discipline 10 is designed to catch.

**Status**: HIGH-risk audit complete with 1 REVISION applied. User decision pending: run MEDIUM-risk audit (adapter + sparring + Phase 3.1 4 decisions + quality-gate-scope-lock) OR defer to Phase 3.8 C3 boundary audit.

**Locked artifact state added**:
- 5 hard checkpoints + 3 trigger conditions for coherence-audit cadence (Discipline 9)
- Discipline 10 (NEW; greenfield evaluation of archived material)
- decision-design-sharpening v0.7.0 (NEW Round 1 termination checklist)
- plugin/hooks/architectural_commit_gate.py NEW (PreToolUse hook; 3 checks)
- plugin.json hooks section + plugin version 0.3.0 → 0.4.0
- substrate-arch-topic.md DR amended (REVISION-1 retroactive greenfield-pass record)
- arch/substrate.md §10 corrected (boot precondition + shutdown alignment with audit.md §11)
- 10 disciplines now in DISCIPLINES.md (was 9; added Discipline 10)

---

**Note 41: Phase 3.4 PAUSED — greenfield re-derivation procedure documented**:

User direction after Phase 2.1 audit (substrate REVISION-1 + audit-topic clean): "this is very important! I mean really greenfield! we are trying to build the framework from scratch treating the archive as a loose resource. I feel like this whole process has been too much relying on the archive in the past, otherwise this situation wouldn't have arisen. let's take stock for a moment before continuing... if you look what we have as a whole (full ARCH set, full glossary) what would you do different? what are the gaps? really take your time here. there is a chance we need to invalidate all work, do not consider sunk-cost."

**AI honest stock-taking response** surfaced 4 tiers of concern:

- **Tier 1 HIGH RISK FOUNDATIONAL** (could invalidate substantial work): Pattern A protocol topic 18-section template substrate-shape-anchored / 8 Pattern A protocols list inherits archive's protocol categorization / Pattern A vs B vs C three-pattern framework may be archive-influenced / Phase 3.2 topic taxonomy locked predates Discipline 10
- **Tier 2 MEDIUM RISK STRUCTURAL** (cascade fixes): Phase 3.1 4 decisions may have cross-topic-cascade-miss / Sparring 8-sub-mechanism count from archive / Profile validation depth shallow / GLOSSARY entries lack per-element greenfield-evaluation
- **Tier 3 PROCESS** (improvements): Discipline 10 should have been Discipline 1 / Hook should have deployed at session-16 launch / Archive cross-references should flag consult-with-skepticism
- **Tier 4 GAPS**: orchestrator mechanics / onboarding pathway / federation specifics / Multi-VISION model / Markdown-validation / marketplace mechanics / per-shape policy bundle SCHEMA

**Committed position**: pause Phase 3.4; greenfield re-derivation procedure executes BEFORE continuing. User authorized; pause locked.

**NEW DR `docs/decisions/greenfield-rederivation-pause.md`** (status PROPOSED; this commit):

7-step procedure:
1. Re-read VISION + locked GLOSSARY in entirety (no summary-pattern-matching)
2. Greenfield-derive Pattern A vs B vs C framework (ignoring MAINTENANCE.md current TOP-LEVEL ARCHITECTURE)
3. Greenfield-derive Pattern A protocol list (which protocols emerge from VISION + GLOSSARY without archive)
4. Greenfield-derive Pattern A protocol topic template (minimal common + per-protocol-extended)
5. Compare to current locked work (substrate / adapter / sparring / audit + Phase 3.2 + Phase 3.1)
6. Surface revisions (per Tier)
7. Decide: revise foundations + cascade OR validate greenfield-equivalent

Anti-patterns explicitly named (counter pattern-matching from current ARCH content; counter self-validation bias on greenfield-equivalent verdicts; counter shortcut-to-validation; counter confirmation bias from prior 0-REVISION metrics).

**Hook continues firing during execution**; catches drift on architectural-artifact writes in real-time.

**Phase 3.4 paused**: 5 remaining Pattern A protocol topics + arch/coordination.md Round 1 redo all paused until Step 7 decisions committed.

**Status**: greenfield-rederivation-pause DR PROPOSED; awaiting user approval to execute Step 1.

**Locked artifact state added**:
- 11 DRs in docs/decisions/ (was 10; greenfield-rederivation-pause.md NEW)
- arch/coordination.md NOT locked (Round 1 was proposed; pending pause-resolution + redo)
- Phase 3.4 progress 4 of 8 frozen pending greenfield audit outcome

---

**Note 42: Side-quest — round-termination judgment skill update + Observation 29**:

User identified META-failure recursion: my STABLE LOCK at Round 3 of procedure-sharpening was Disguise #5 (substituting AI judgment for codified rule) firing AT THE ROUND-TERMINATION-JUDGMENT LEVEL. Pattern-matched Discipline 3's expected decay (6→5→3→0-1) instead of measuring actual density (Round 1-3 substantive findings: 9→10→9, holding flat).

Round 4 forced by user yielded 9 substantive findings (4 HIGH + 3 MEDIUM + 2 LOW) — confirming user's prediction; density genuinely not decaying for procedure-document surface.

**Root cause**: Discipline 3's empirical decay pattern was derived from ARCHITECTURAL-DECISION sharpening. Procedure-document sharpening has fundamentally different surface dynamics (broader cognitive-mode passes; cross-cutting concerns; anti-pattern-hardening territory).

**Skill updates this commit**:

1. `plugin/skills/sharpen/SKILL.md` v0.9.0 → v0.10.0:
   - Mandatory empirical density check at every round termination (count current vs previous; ≥50% drop = decay confirmed)
   - Surface-type declaration mandatory: ARCHITECTURAL-DECISION / PROCEDURE-DOCUMENT / SET-LEVEL AUDIT / META-ARCHITECTURAL
   - Honest termination test Q1-Q5 (count / decay / specific signal; Q5 unanswerable for STABLE = manufactured comfort)
   - NEW manufactured-comfort counter-test (equal-weight to manufactured-criticism; round-fatigue / completion-comfort biases AI toward STABLE prematurely)

2. `plugin/skills/decision-design-sharpening/SKILL.md` v0.7.0 → v0.8.0:
   - Round termination signals revised to require empirical density measurement
   - Decomposition trigger (Round 4+ signals decomposition missing) applies to ARCHITECTURAL-DECISION surface ONLY

3. `DISCIPLINES.md` Discipline 3:
   - Surface-type sweet-spot variation explicit (architectural-decision 2-3; procedure-document 4-5+; set-level per-cluster; META-architectural user-trigger)
   - Cross-ref skill version updates

4. `learnings/ai-app-development.md` Observation 29 (NEW):
   - Round-termination judgment is execution-fidelity META-failure surface
   - Manufactured-comfort defined as Disguise #5 round-termination instance
   - Promotion criteria: 3+ subsequent sharpening sessions without recurrence

**Side-quest complete**. Returning to main quest: Round 5 of greenfield-rederivation-pause procedure-sharpening, applying NEW termination criteria honestly.

**Locked artifact state added**:
- sharpen v0.10.0 + decision-design-sharpening v0.8.0
- DISCIPLINES.md Discipline 3 surface-type-aware
- learnings Observation 29 (NEW; 29 observations now; was 28)

---

## Session 16 continuation #2 (2026-05-02 — afternoon)

(Note: existing #2 section follows; this section is below the new #3 + #4)

## Session 16 continuation (2026-05-02)

**What happened (notes 20-27)**:

20. **Sharpen skill multi-iteration v0.4.0 → v0.9.0 with self-applied passes** — generic critical-pass skill iteratively refined through self-application:
    - **v0.4.0**: F1+F2+F3 + S1-S5 + non-categorical pass as STABLE-blocker (synthesis-vs-citation in Step 1; scope-fit 8th sub-question; iteration USER-TRIGGERED; skip-if-N/A; trivial-cosmetic rejectable; substantive defined; CUT-without-rationale also bias; cite feedback_judgment_and_automate)
    - **v0.5.0**: Spirit/mission section + Step 6 cognitive-mode passes (cold-read + mechanism-simulation added alongside non-categorical)
    - **v0.6.0**: Self-applicability test + AI-executor test in Spirit; Step 6 nested bullets restore AI-iteration prompting (vs prose gist-extraction); Anti-patterns expanded with 3 new failure modes
    - **v0.7.0**: cut "Why this skill earns its place" (redundant with Spirit + Anti-patterns); Step 4 wording tightened
    - **v0.8.0**: frame-level question added to Step 2 (lifted from bildhauer commission-questioning principle — "is this the right target?")
    - **v0.9.0**: 2-round sweet spot surfaced explicitly (was implicit in specialized skills only); cut misleading "different angle per pass" parenthetical (same procedure each pass — Pareto catches what matters; findings naturally drift as earlier-fixed surfaces stabilize)
    - User feedback drove key corrections: AI was framing "80/20 Round 1 sufficient" until user pushed back citing 2-round empirical pattern + memory; AI was misreading prescriptive parenthetical as descriptive

21. **Bildhauer evaluation + refactor** (separate repo `~/dev/Gunther-Schulz/bildhauer/`):
    - Identified VISION/PROCEDURE structural tension: VISION says "checking IS the work" (continuous rhythm); PROCEDURE was framed as "Mandatory checkpoints that interrupt default behavior" (discrete interrupts)
    - PROCEDURE refactored: 5 checkpoints → 3 Stance items + 8 Checkpoints (11 elements). All VISION-grounded. New: Whole-piece coherence at any resolution; coarse-to-fine refinement; verify-with-eyes-not-hands; commission-questioning (at request-receipt); symptom-vs-root (when something feels off); vision-questioning at transitions
    - Stance honestly framed for AI: not always-on background processes (AI doesn't have those); orienting frames re-instantiated per engagement
    - Round 2 sharpen on bildhauer: 1 borderline finding correctly Pareto-rejected as trivial-cosmetic. STABLE
    - SKILL.md framing fix: validator-mode → sparring-mode language ("audit adherence" → "audit behavior change"; "did it fire?" → "did it shift behavior?"); portable update-plugin.sh path
    - Bumped 0.5.0 → 0.6.0

22. **Skill-craft validator-mode-bias correction** (separate repo `~/dev/Gunther-Schulz/skill-craft/`):
    - Traced bildhauer's old rigid framing back to skill-craft's Layer 2 dominant validator-mode vocabulary ("Mandatory checkpoints that interrupt default behavior" was direct stylistic inheritance from skill-craft's "CANNOT proceed" / "Forcing functions" / "Blocking logic" framing)
    - Sharpen Round 1 + Round 2 surfaced 4 structural findings (F1-F4) + 1 cleanup (cross-reference symmetry from Round 2)
    - **Layer 1.5 (NEW)**: skill-type identification as load-bearing structural decision before Layer 2 conventions are applied; 5 skill types listed with classifying question ("can this skill's checks be satisfied mechanically without understanding?")
    - **Layer 2 annotations**: tagged "Judgment calls as design risk" / "Forcing functions" / "Blocking logic" with `(validator-mode)`; "Menus" with `(workflow-mode)`; "Observable checkpoints" with universal-but-form-adapts note
    - **Anti-patterns**: "Naked judgment call" scope-qualified to validator-mode skills; NEW anti-pattern "Validator conventions applied to judgment skill" added (symptoms include "Mandatory checkpoints" framing, vision/procedure tone mismatch, performative-fire-without-behavior-change)
    - **OBSERVATIONS.md observation 15**: documents bildhauer as the originating incident; traces root cause to "Naked judgment call" anti-pattern's overgeneralization across skill types
    - Round 2 surfaced cross-reference symmetry fix (Writing judgment procedures section now references back to Layer 1.5)

23. **Foundation-up workflow ordering memory persisted** — `DISCIPLINES.md` Discipline 8 captures: when work items have dependencies (compositional/architectural work — GLOSSARY entries, DRs, ARCH topics, specs), lock items others depend on first; downstream items that compose with multiple foundations come last; parallel-depth items batch with shared sharpening passes. Why: minimizes rework; downstream items reference locked foundations cleanly. Discovered in current session when ordering remaining 6 GLOSSARY entries.

24. **Phase 2 GLOSSARY completion: 6 entries locked per foundation-up ordering**:
    - **category collapse** (force-level meta-concept; cross-axis, axis-1 primary anchor): the force that degrades practitioner's mode of engaging with AI from higher-engagement state to lower-engagement state regardless of architectural intent. Round 1 stress-test surfaced cross-axis generalization (manifests on all three axes — not just axis-1 as BACKLOG framed). Operates in practitioner's mental category, not architecture
    - **answer-machine AI / oracle AI / validator AI** (axis-2 failure modes per Ming research): batch-locked with parallel structure; each captures distinct direction of practitioner-AI dynamic (extraction / declarative / affirmation). Naming collision flagged + disambiguated for validator AI vs validator-mode (skill-craft / sharpen vocabulary)
    - **rubber-stamping** (axis-3 failure mode): sign-off without engagement at attestation/finalization moment. Independent dimension from axis-2 failures (can co-occur). Fails defensibility's engaged-authorship condition
    - **pioneer instance** (originating-deployment role): triple-purpose framing — production-tool + research-lab + IP-proving-ground. PBS-Schulz is pioneer per PIONEER.md. Final Phase 2 entry
    - GLOSSARY: 28 → 34 locked entries

25. **Quality-gate draft + BACKLOG anchored to category-collapse + axis-failure-mode taxonomy** — hybrid approach (minimal engagement now since context is hot; full ARCH development deferred to Phase 3 after prerequisites lock). drafts/quality-gate.md updated with "What it gates against" section explicitly mapping to all three axis manifestations of category collapse. BACKLOG entry strengthened with category-collapse anchoring + explicit Phase 3 prerequisites list

26. **Coherence-audit Round 1 on full GLOSSARY (34 entries)** before Phase 3 transition:
    - Lens 1 (Set composition) LOAD-BEARING: 0 substantive findings after honest run (tested MERGE / SPLIT / ADD / REMOVE / REDEFINE BOUNDARIES; all cleanly partitioned)
    - Lens 8 (Pattern-vs-instance) LOAD-BEARING: 0 leakage (cross-archetype illustrations cover legal/research/auditor; PBS-Schulz references properly scoped)
    - Lens 9 (VISION-grounding) LOAD-BEARING: 0 ungrounded (all derivations valid; pioneer instance via falsification framing + PIONEER.md is intentional dual-doc setup)
    - Lens 5 (Mechanical compliance): R5.1 — provenance pollution in Source sections (5 entries with session-16 / Round-N / Phase-1.85 markers stripped; synthesis content preserved)
    - Lens 6 (Symmetry): R6.1 — added reciprocal Composes-with references in 4 entries (defensibility / claim / practitioner / event) for the 6 entries locked this session
    - Net: 0 REVISIONS / 2 EXPANSIONS (cleanup-grade). Corpus set-coherent at architectural level

27. **STABLE called after Round 1** by user judgment: accumulated audit history (older entries had Round 2/3/4 audits earlier in session 16) + cleanup-grade-only findings → forcing Round 2 purely to satisfy "2-round default" would be validator-mode procedural conformance over honest judgment. Per sharpen v0.9.0: 2-round is sweet-spot default, not mandate; legitimate exception when historical audit + Pareto signal converge

**Phase 2 outcome (locked session 16, 2026-05-02)**:

GLOSSARY foundational vocabulary lock COMPLETE — 34 locked entries; coherence-audited at corpus level; STABLE before Phase 3 ARCH transition.

Final entry breakdown:
- 14 atoms + Pattern A primitives (workspace, practitioner, specialist, skill, actor, event, substrate, adapter, shape, protocol, session, workflow, mechanism, policy, claim, work-unit, framework)
- 3 scope classifications (Layer A / Owner B / Framework C)
- 3 axes (intertwining / sparring / authorship preservation)
- 9 derived/meta concepts (defensibility / category collapse / co-worker / intertwined AI / tacked-on AI / answer-machine + oracle + validator AI / rubber-stamping / pioneer instance)

Coherence verified: all entries cross-archetype illustrated; pattern-vs-instance discipline holds; VISION-grounded; clean naming with documented disambiguations.

**Side outcomes (dev skill ecosystem)**:
- sharpen skill (pbs-bureau) v0.6.0 → v0.9.0 with multi-iteration sharpening + 2-round-sweet-spot self-fix
- bildhauer skill (separate repo) v0.5.0 → v0.6.0 with PROCEDURE refactor + SKILL framing fix
- skill-craft skill (separate repo) Layer 1.5 + Layer 2 annotations + judgment-skill anti-pattern (resolves validator-mode bias that drove bildhauer rigidity)
- foundation-up workflow ordering memory persisted

28. **Phase 3 launch — sub-phase structure locked (2026-05-02)**:

**Phase 3 = ARCH rebuild against locked vocabulary** (Layer 3 in 5-layer doc model). MAINTENANCE budget: 15-20 topics × ~500 lines = ~10,000 lines. ~30 BACKLOG items across mechanism / protocol / primitive / cross-cutting buckets. Likely multi-session work.

**Sub-phase ordering (foundation-up applied)**:

| Sub-phase | Scope | Why this order |
|---|---|---|
| **3.0** ✅ | Doc structure: HYBRID locked (single `ARCHITECTURE.md` overview ~1-2K lines + `arch/<topic-slug>.md` × 15-20 per-topic files ~500 lines each) | Structure decision affects where 3.1 outcomes get persisted; pure-single (10K lines unwieldy + context-budget concern) and pure-multi (no entry point) both rejected; hybrid aligns with progressive-disclosure principle |
| **3.1** | Open architectural questions (workflow + work-unit bipartite-classification; deployment definition; engaged-authorship operational definition) | Foundational decisions shape topic taxonomy; outcomes affect every topic referencing them |
| **3.2** | Topic taxonomy (REVISED — doc-structure-shape resolved at 3.0): which 15-20 topics exactly? Aggregate or 1:1 with BACKLOG buckets? File naming convention. Cross-cutting topics placement (axis-interactions, quality-gate) | Lock topic identities before writing content |
| **3.3** | Per-mechanism detail (12 mechanisms: source-grounding + audit emission + audit trail foundational; then 8 sparring sub-mechanisms; then orchestration / persistent state / authority binding) | Within-bucket foundation-up: mechanisms underlying defensibility first |
| **3.4** | Per-architectural-Protocol detail (7 Pattern A Protocols: Substrate first; Adapter; Sparring; Audit; Coordination; Trust; Time) + Per-Pattern-A primitive detail (substrate per-impl; adapter lifecycle) | Substrate is most foundational; Pattern A trio details follow |
| **3.5** | Primitive-detail topics (9 primitives: specialist / skill / practitioner / workflow / session / event / actor / claim / defensibility) + axis-interaction analysis | Per-primitive richer detail; axis-interaction cross-cutting topic |
| **3.6** | Quality-gate ARCH topic (scope-locked session 16 as Pattern A protocol with mechanism-shaped Surface; per GLOSSARY entry + `docs/decisions/quality-gate-scope-lock.md` DR; full design pending) | Runtime mechanism integrating axis-failure-mode taxonomy |
| **3.7** | Cross-cutting investigations (PydanticAI substrate re-eval; markdown-validation feasibility; Ming research deepening; adjacent thinkers expansion; multi-VISION model decision) | When relevant context is loaded |
| **3.8** | Coherence-audit Lenses 11-15 activation (ARCH-specific lenses: inter-layer consistency / specs traceability / architectural protocol completeness / DR coverage gap / granularity match) | Phase-boundary audit before Phase 4 DR rebuild |

**Phase 3 starting commitment**: 3.1 first (questions before structure since question outcomes affect topic taxonomy); within 3.1, **workflow bipartite-classification first** (most-referenced; work-unit cascades from workflow; deployment + engaged-authorship follow). Round 1 + Round 2 sharpening per `sharpen` v0.9.0 + `decision-design-sharpening` v0.3.1 disciplines.

**Phase 3 paused after workflow lock + multi-axis validation surfaced**: workflow bipartite-classification resolved (workflow → bipartite Pattern B with optional applicability). User push during workflow Round 2 surfaced ad-hoc work as legitimate scope outside primitive (REVISION-grade refinement). User additionally surfaced foundational concern: framework risks single-consumer-thinking drift; needs persisted usage profiles to validate against (not just feedback rule). Phase 3 paused to build profile foundation before resuming 3.1 work-unit + remaining items. See note 29 below.

**Disciplines carrying forward into Phase 3**:
- Foundation-up workflow ordering (per `DISCIPLINES.md` Discipline 8)
- 2-round sweet spot per architectural decision (per `DISCIPLINES.md` Discipline 3 + sharpen v0.9.0)
- Cascade discipline (MAINTENANCE.md)
- Pattern-vs-instance (cross-archetype illustrations required; per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2)
- Make-wrong-shapes-impossible (structural over conventional; per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1)
- AI-as-runtime hybrid-shape (per `ARCHITECTURE.md` cross-cutting principles "AI as runtime")
- Provenance hygiene (no audit-history breadcrumbs in canonical content; per coherence-audit Lens 5 v0.2.1)
- **Multi-axis validation** (per `DISCIPLINES.md` Discipline 3 (multi-axis sub-section) + `profiles/INDEX.md`): validate primitive proposals across archetype × work-type × role; explicit non-coverage question
- **Composability + boundaries** (per `profiles/G-composability-gate.md` + `drafts/composability-tooling.md`): G composability gate fires FIRST as initial validation gate; L1-L4 producer levels validate against G's multi-mode consumption requirements (consulting / firm-reuse / OSS / marketplace-future / backup-migration); structural composability rather than advisory

---

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

## Pending work items

→ See **`BACKLOG.md`** for Phase-tagged work-item tracker (Phase 2 GLOSSARY remaining + Phase 3 ARCH + Phase 4 DRs + Phase 5 ROADMAP + Phase 6 specs/code + cross-cutting). Items added when surfaced; resolved when locked; archived at phase boundaries.

## Inputs to consider for the rebuild (from session-16 findings)

Persisted in `archive/INDEX.md` "Status note" section. Six findings flagged as inputs the rebuild should address at root:

1. Foundational vocabulary lock (framework / shape / mechanism / policy / practitioner / authority chain / Protocol disambiguation)
2. Shape-neutrality vs Option B floor contradiction
3. VISION-scope vs framework-scope contradiction
4. Instance-anchoring leakage (5 sites)
5. "Mechanism vs policy" vocabulary not in corpus (introduced in session-16 conversation; needs to land as named architecture if accepted)
6. Filesystem location drift (shape-extension DR vs v0.34 restructure)
