# Session handoff — pbs-bureau (rebuild)

> **🔴 At session start, read `DISCIPLINES.md` FIRST** — working procedure + cross-session disciplines + memory composition. Then `VISION.md`, `MAINTENANCE.md`, this file.

This is the running session log for the **foundational rebuild** launched session 16 (2026-05-01). The previous multi-session running handoff (sessions 1-15) is at `archive/HANDOFF.md` for reference.

## Anchors (carry forward, never rebuilt)

- **`DISCIPLINES.md`** — cross-session working discipline; how we operate (procedure + 7 disciplines + memory composition). **Read FIRST.**
- `VISION.md` — three-axis thesis (intertwining + sparring + authorship preservation) + framework's structural primitives + shape-neutrality + foundations + falsification; PURE STANCE ABOUT THE PRODUCT (tooling lives in DISCIPLINES + plugin/skills + memory); preliminary-lock anchor; the ground truth the rebuild serves
- `MAINTENANCE.md` — doc system rules (5-layer model + cascade discipline + TOP-LEVEL ARCHITECTURE: framework=mechanisms / shape=policies + A-B-C scope model + GLOSSARY entry classification); read at session start
- `BACKLOG.md` — Phase-tagged work-item tracker; pending items across phases; read at session start
- `PIONEER.md` — pioneer-instance (PBS-Schulz) identity-anchor; current deployment status + relation to framework; consult when working on pioneer-instance-specific content
- `profiles/INDEX.md` — usage profiles for framework validation; PRELIMINARY baseline; spans lifecycle stages × shape variations × archetypes; pre-validation (proposing primitives) + post-validation (auditing locked corpus); load specific profile on-demand per `profiles/INDEX.md` taxonomy
- `ARCHITECTURE.md` — Layer 2 overview for Phase 3 ARCH rebuild; Phase 3 status + locked architectural decisions + active disciplines + provisional topic catalog; per-topic detail in `arch/<topic-slug>.md` (created as Phase 3.3+ produces topic content; not yet created)
- `GLOSSARY.md` — canonical term definitions (Layer 1 anchor; in-progress as of session 16 Phase 2)
- `memory/` — feedback files (lessons learned across sessions) + bausteine + universal prose; the actual user knowledge
- `archive/INDEX.md` — index of v0.35 corpus + code + content archived at rebuild launch; consult during Phase 3+

**Consult when relevant** (not session-start required):
- `learnings/` — preliminary methodological observations about AI-app development; growing folder; consult during methodological reflection or when the AI-app-dev skill (per future ROADMAP) is being designed
- `drafts/` — exploratory ideas / future-candidates / brainstorm output (NOT locked, NOT load-bearing); discipline in `drafts/README.md`. Currently holds: `marketing-themes.md` (session-16 marketing-shape thinking captured during VISION clean-stance work)

**Session-start reading order**: `DISCIPLINES.md` → `VISION.md` → `MAINTENANCE.md` → `HANDOFF.md` (this file) → `BACKLOG.md` → `profiles/INDEX.md` → `ARCHITECTURE.md` (Layer 2; read when working in architectural area). Plus `GLOSSARY.md` for current vocabulary state. Specific profiles + per-topic `arch/<topic>.md` files load on-demand.

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

- **Multi-axis validation discipline locked** (per `feedback_multi_axis_validation.md`): three orthogonal dimensions (archetype × work-type × role) + explicit non-coverage question; replaces the previous single-axis cross-archetype illustration approach that missed ad-hoc work as legitimate scope

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

23. **Foundation-up workflow ordering memory persisted** — `feedback_foundation_up_ordering.md` captures: when work items have dependencies (compositional/architectural work — GLOSSARY entries, DRs, ARCH topics, specs), lock items others depend on first; downstream items that compose with multiple foundations come last; parallel-depth items batch with shared sharpening passes. Why: minimizes rework; downstream items reference locked foundations cleanly. Discovered in current session when ordering remaining 6 GLOSSARY entries.

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
| **3.6** | Quality-gate ARCH topic (per drafts/quality-gate.md; prerequisites met after Phase 2 lock) | Runtime mechanism integrating axis-failure-mode taxonomy |
| **3.7** | Cross-cutting investigations (PydanticAI substrate re-eval; markdown-validation feasibility; Ming research deepening; adjacent thinkers expansion; multi-VISION model decision) | When relevant context is loaded |
| **3.8** | Coherence-audit Lenses 11-15 activation (ARCH-specific lenses: inter-layer consistency / specs traceability / architectural protocol completeness / DR coverage gap / granularity match) | Phase-boundary audit before Phase 4 DR rebuild |

**Phase 3 starting commitment**: 3.1 first (questions before structure since question outcomes affect topic taxonomy); within 3.1, **workflow bipartite-classification first** (most-referenced; work-unit cascades from workflow; deployment + engaged-authorship follow). Round 1 + Round 2 sharpening per `sharpen` v0.9.0 + `decision-design-sharpening` v0.3.1 disciplines.

**Phase 3 paused after workflow lock + multi-axis validation surfaced**: workflow bipartite-classification resolved (workflow → bipartite Pattern B with optional applicability). User push during workflow Round 2 surfaced ad-hoc work as legitimate scope outside primitive (REVISION-grade refinement). User additionally surfaced foundational concern: framework risks single-consumer-thinking drift; needs persisted usage profiles to validate against (not just feedback rule). Phase 3 paused to build profile foundation before resuming 3.1 work-unit + remaining items. See note 29 below.

**Disciplines carrying forward into Phase 3**:
- Foundation-up workflow ordering (per `feedback_foundation_up_ordering.md`)
- 2-round sweet spot per architectural decision (per `feedback_pre_decision_sharpening.md` + sharpen v0.9.0)
- Cascade discipline (MAINTENANCE.md)
- Pattern-vs-instance (cross-archetype illustrations required; per `feedback_pattern_not_instance_defers.md`)
- Make-wrong-shapes-impossible (structural over conventional; per `feedback_wrong_shapes_impossible.md`)
- AI-as-runtime hybrid-shape (per `feedback_ai_as_runtime.md`)
- Provenance hygiene (no audit-history breadcrumbs in canonical content; per coherence-audit Lens 5 v0.2.1)
- **Multi-axis validation** (per `feedback_multi_axis_validation.md` + `profiles/INDEX.md`): validate primitive proposals across archetype × work-type × role; explicit non-coverage question
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
