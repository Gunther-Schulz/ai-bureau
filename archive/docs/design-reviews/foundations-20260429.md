# Design review — Load-bearing foundations — 2026-04-29

**Trigger**: User-invoked "lets do it" after design-review skill landed; first real run; load-bearing foundations were the agreed first-run scope per the skill's `references/scope-and-targets.md`.

**Scope**: 6 load-bearing foundations (Architecture meta-rules, Entity types + decision rules, Orchestrator, Skill frontmatter contract, Office-config schema, Decision rules + Maintenance discipline meta-infrastructure)

**Mode**: full first-principles review

**Stage**: pre-launch / pre-distribution; radical reshapes are cost-cheap

---

## Verdict summary

| Subsystem | Verdict |
|---|---|
| 1. Architecture meta-rules | **Rough and worth refining** |
| 2. Entity types + decision rules | **Rough and worth refining** |
| 3. Orchestrator | **Rough and worth refining** |
| 4. Skill frontmatter contract | **Refactor with conviction** (functionally sound, but `description` overloaded) |
| 5. Office-config schema | **Refactor** (with 2 Reshapes — `extensions.*_manifests` block; integrations classes) |
| 6. Meta-infrastructure (decision rules + conventions + audit/design-review pair) | **Rough but adequate** (with 2 Reshapes) |

Net signal: **the foundations are coherent and the orthogonality work is real, but ~5 years of accreted distinctions can be collapsed.** The system has 5 meta-rules where 3-4 would do, 9 entity types where 5 would do, 6 decision rules where 3 would do, and 2 review skills where 1 with modes might do. None of these are wrong; all of them are heavier than greenfield would build. Pre-launch is exactly when to consolidate.

---

## Per-subsystem reviews

### Subsystem 1 — Architecture meta-rules

**Verdict**: Rough and worth refining

**Greenfield sketch**: 3 meta-rules + 1 named convention. The three fundamental axes are (1) **WHO ships it** (app vs deployment — absorbs integration adapter as a mechanism subsection), (2) **what changes invalidate it** (memory's prose-conventions vs RAG's amendable-source-text vs code's deterministic-logic — absorbs source-of-truth + invalidation), and (3) **execution determinism** (where deterministic single-right-answer logic lives vs. where judgment lives — currently named "execution locality" which obscures the actual axis). Scope-orthogonality (universal × domain × state) demoted from meta-rule to **layering convention** that applies *within* deployment-controlled content (manifests, bausteine, skeletons).

**Recommendations**:

#### Reshape — Demote integration-adapter from meta-rule to corollary of app-vs-office

- **Greenfield grounding**: app-vs-office is the deployment-portability axis; adapter pattern is the *implementation* of that axis for "external systems with varying mechanisms." Same lesson as paths-via-config. Currently they're sibling-level meta-rules.
- **What it unlocks**: 5 → 4 meta-rules; one coherent home for "everything that varies per deployment"; clearer narrative arc.
- **What breaks**: Type I (integration adapters) loses top-level meta-rule pointer; needs a sub-section under app-vs-office.
- **Cost**: S

#### Reshape — Demote scope-orthogonality from meta-rule to layering convention

- **Greenfield grounding**: scope (universal × domain × state) is a layering pattern applied to multiple entity types (manifests, bausteine, skeletons, office-style overlays), not a placement axis itself. It doesn't answer "where does this go?" — it answers "once you know what type, which subdirectory?" That's a different question from app-vs-office or memory-vs-RAG.
- **What it unlocks**: clarifies that meta-rules answer placement-by-type; layering answers within-type sub-placement. Makes scope's actual scope visible (it has no force for types A, B, C, E, F, G, I — currently obscured by giving it equal billing with rules that DO have force across all types).
- **What breaks**: demotes the document's strongest concrete contribution. Author-manifest skill, layered loaders, manifest schema all still operate; only the rule's *level* changes.
- **Cost**: S-M

#### Refactor — Rename "execution locality" → "execution determinism"

- **Greenfield grounding**: the actual axis is determinism (single-right-answer → MCP, judgment → skill). The current name suggests *physical location* (which process). The persistence-layer-boundary is a useful proxy heuristic but not the principle.
- **What it unlocks**: rule name matches its decision criterion.
- **What breaks**: forward references in conventions docs + HANDOFF need a search-and-replace.
- **Cost**: S

#### Add — Source-of-truth & invalidation meta-rule

- **Greenfield grounding**: every entity type must declare its invalidation contract — schema_version, references_used[], review_due, status flags. Today this is scattered: bausteine have it (status, review_due, references[]), memory C-docs have references_used[], office-config has schema_version, but skills (A) and references (B) just have semver with no formal trigger semantics, and external data (F) has no invalidation pointer at all.
- **What it unlocks**: forces every new entity type to answer "how does the system know you're stale?" before shipping. Makes the audit-trail ROADMAP item (currently homeless) a natural extension of an existing meta-rule rather than a new entity type.
- **What breaks**: adds work to entity-type definitions; may surface gaps (F has no invalidation hook).
- **Cost**: M

#### Refactor — Drop or fold "Backend organization" sub-section into meta-rule 5

- **Greenfield grounding**: the `pbs_core/` vs `pbs_mcp/tools/` split is a *consequence* of execution-determinism, not its own concern. Currently it's its own H2 between entity-types and decision-rules.
- **What it unlocks**: tightens document; surfaces the conceptual unity.
- **What breaks**: loses standalone discoverability for backend authors; mitigate by linking from `docs/backend-conventions.md`.
- **Cost**: S

---

### Subsystem 2 — Entity types + decision rules

**Verdict**: Rough and worth refining

**Greenfield sketch**: decompose by **(audience, mutability, locality)** rather than by an A-I letter list. Three audiences: *Claude-at-runtime* (skill bundles), *backend code* (Python core + adapters + tools), *durable state* (everything persisted: configs, manifests, instance records, project state). Then tag each by mutability (authored / generated / external) and by scope (universal/domain/state) when it lives in `extensions/`. Five categories cover it: **Skill Bundle** (SKILL.md + its references — one entity), **Backend Module** (core + adapters + tool wrappers — one entity), **Configuration** (office-config + layered manifests — both deployment-controlled YAML), **Memory** (authored prose + saved records — keep split because mutability differs sharply), **External Data** (user files outside the app boundary). Decision: one branch per audience, then by mutability. Three rules, not six.

**Recommendations**:

#### Reshape — Collapse A+B into "Skill Bundle"

- **Greenfield grounding**: a skill reference (B) has no meaning outside its parent skill — it's a chapter of the skill, not a peer. The taxonomy hides this by giving it a letter; Rule 4's "ONE vs MULTIPLE skills" branch exists only to police the A/B boundary.
- **What it unlocks**: Rule 4 collapses to "is it cross-cutting prose? → C, else it's part of the skill bundle." Eliminates one borderline case category and one rule branch.
- **What breaks**: re-labeling only.
- **Cost**: S

#### Reshape — Merge G + H into "Configuration (scoped YAML)"

- **Greenfield grounding**: office-config (G) and layered manifests (H) are both deployment-controlled YAML; the only difference is single-file vs scope-keyed. Splitting them suggests they're more different than they are.
- **What it unlocks**: Rule 2 disappears or becomes "is this configuration? → if scope-keyed, place in extensions/<scope>/; else office-config." One fewer entity type, one fewer rule.
- **What breaks**: a reader who wants to know "what gets loaded at startup" loses a label. Schema-versioning + migrations story unchanged.
- **Cost**: S

#### Reshape — Demote I (integration adapters) from peer entity type

- **Greenfield grounding**: integration adapters are an internal organizing pattern of E (backend code) — same language, same package, same restart semantics. Promoting to letter peer with C (memory reference content) implies a category-level distinction that doesn't exist. Rule 1 already has a sub-question to disambiguate I vs E — the smell that I isn't peer-level.
- **What it unlocks**: combined with the above two collapses, **9 types becomes 5**.
- **What breaks**: the "swappable mechanism" story still needs telling — but it lives naturally in backend-conventions.md alongside other internal patterns.
- **Cost**: S

#### Reshape — Drop the A-I letter scheme

- **Greenfield grounding**: letters create false ordinality (why is Skill before Skill reference before Memory…?) and false peerage. The only place letters are used outside the table is in worked examples ("→ `C`") which read as opaque jargon. Names ("Skill Bundle", "Memory record") are self-documenting.
- **What it unlocks**: no special vocabulary; new contributors infer placement from names.
- **What breaks**: ~20 references repo-wide need a sed.
- **Cost**: S

#### Reshape — Reduce 6 rules to 3 by audience-first decomposition

- **Greenfield grounding**: walk in audience order, not type order: (1) Is this consumed by Claude at runtime as behavior? → Skill bundle. (2) Is this Python? → Backend. (3) Then by mutability: authored prose vs generated record vs external data vs configuration. Current Rules 4 & 5 ("HOW vs WHAT") is real but only relevant inside Memory — sub-rule, not top-level.
- **What it unlocks**: walker terminates in 1-3 questions for ~95% of content.
- **What breaks**: existing classifications need re-checking; most should land identically.
- **Cost**: M

#### Drop bloat — Move "Borderline cases" into entity-type definitions

- **Greenfield grounding**: a standing "borderline" section is a smell — a holding pen for cases the taxonomy can't decide. Each entry should either become a clarifying example *inside* the relevant type's definition, or trigger a taxonomy refinement.
- **What it unlocks**: doc no longer needs a "we'll figure this out later" register.
- **What breaks**: loses a "here's what we considered" trail; mitigate by moving to per-decision records under `docs/decisions/`.
- **Cost**: S

#### Add — Make "scope" a property orthogonal to entity type

- **Greenfield grounding**: scope (universal/domain/state) recurs across H (manifests), D (bausteine), partially G (office-config selects scope), and templates. Architecture currently re-explains scope inside each type. Greenfield: scope is a *dimension* applied to anything in `extensions/` or `memory/bausteine/`, not a per-type concept.
- **What it unlocks**: single canonical scope-placement section; entity types stop carrying half-redundant scope explanations.
- **What breaks**: nothing — meta-rule "scope orthogonality" is already framed this way; the entity-type table just hasn't caught up.
- **Cost**: S

---

### Subsystem 3 — Orchestrator skill

**Verdict**: Rough and worth refining

**Greenfield sketch**: a thin **router skill** (≤150 lines) that does only three things — detect scope (office/project/product), load the right context bundle, and route phrases-to-specialists via `list_skills()` capability matching. Everything else (watch-list classification, send/setup/binding gates, source-grounding invariant, layered-review sequencing) becomes **specialist skills with their own auto-load triggers** or **MCP-side validators** (per meta-rule 5). The "framework is operational, not advisory" claim becomes "the router auto-loads; it dispatches to specialists who own their own invariants." Watch triggers T1-T6 become a single `watch-list` skill with a notice/menu protocol; gates 4.1/4.3/4.4 become `gate-compile`, `gate-send`, `gate-state-transition` skills that any specialist can invoke.

**Recommendations**:

#### Reshape — Split orchestrator into router + watch-list + gates

- **Greenfield grounding**: a 460-line PROCEDURE.md with 14 checkpoints crossing routing, gates, lifecycle, ingestion, MCP fallbacks, conversational style, and session close is doing the job of 5-7 skills. `list_callables` / `list_skills` exists — capability-based dispatch is feasible without a master coordinator.
- **What it unlocks**: each piece evolves independently; specialists can self-trigger; the "loaded means active, never bypass" framing dissolves into "each invariant has its own owning skill that auto-loads when relevant."
- **What breaks**: the "single entry point" guarantee. Cross-skill coordination becomes a contract problem (which is what skill descriptions + `list_skills` are for).
- **Cost**: L (real refactor — but pre-launch)

#### Drop bloat — Remove MCP fallback tables from PROCEDURE.md §9

- **Greenfield grounding**: each specialist already declares `fallback_when_mcp_absent` in frontmatter (per meta-rule 5). Orchestrator's §9 duplicates this for 15+ tools. Single source of truth violation.
- **What it unlocks**: ~70 lines gone.
- **What breaks**: nothing — `list_skills()` already returns this info.
- **Cost**: S

#### Drop bloat — Move CP11 (binding) and CP12 (new-project) into specialist skills

- **Greenfield grounding**: both checkpoints describe specialist work in detail. PROCEDURE.md §11 is 30 lines telling the orchestrator how to do binding; `survey-project` exists for exactly this. §12 describes the `setup_project` MCP tool's behavior — that belongs in the tool's contract.
- **What it unlocks**: routing-layer concerns separate from doing-the-work concerns. ~70 lines gone.
- **What breaks**: orchestrator must trust specialists.
- **Cost**: S-M

#### Reshape — "Loaded means active, never bypass" framing is over-rigid

- **Greenfield grounding**: modern Claude Code skills are composable; each declares its own trigger conditions. The "never bypass" framing treats orchestrator as a kernel — but when the user asks an unrelated coding question, the orchestrator must distinguish "in scope" vs "out of scope" anyway. Same judgment a normal trigger description requires.
- **What it unlocks**: orchestrator becomes a skill among skills; reduces bureaucratic feel.
- **What breaks**: user's mental model of "every PBS session goes through one place."
- **Cost**: S (mostly wording)

#### Add — Watch-list (T1-T6) needs explicit data model and decay rules

- **Greenfield grounding**: PROCEDURE.md §2 says triggers fire "whenever they match" and surface "immediately"; §3 says "do not batch silently across multiple turns" but also "at natural pauses run a one-pass sweep." Contradictory. No specified queue, no TTL, no per-session cap, no de-dup across reframings.
- **What it unlocks**: predictable surface behavior; avoids spamming.
- **What breaks**: nothing — missing spec.
- **Cost**: S

#### Reverse manufactured restraint — T6 (capability gap) should auto-create a backlog entry, not surface a menu

- **Greenfield grounding**: when the orchestrator notices a missing tool/skill and works around it, that's diagnostic information. Asking the user "capture-now / handle-now / backlog / drop?" for an internal observation is the wrong audience.
- **What it unlocks**: less menu fatigue; T6 becomes a real gap-tracking signal.
- **What breaks**: the "every memory-write corresponds to an explicit four-way decision" invariant — but product-backlog isn't a memory write.
- **Cost**: S

#### Surface anchoring — Three-phase model (draft → review → finalize) is implicit, not declared

- **Greenfield grounding**: `draft-textteil-b/SKILL.md` references "Phase A per the orchestrator's three-phase model"; `review-draft` says "Phase B per orchestrator framework" — but PROCEDURE.md never declares this model. Phantom anchor.
- **What it unlocks**: alignment.
- **What breaks**: nothing.
- **Cost**: S

#### Drop bloat — Remove §13 (conversational style) — belongs in plugin-conventions

- **Greenfield grounding**: "Match user's language", "be terse", "no emoji" are cross-skill conventions, not orchestrator procedure.
- **What it unlocks**: conventions live in one place.
- **What breaks**: nothing.
- **Cost**: S

---

### Subsystem 4 — Skill frontmatter contract

**Verdict**: Refactor with conviction (functionally sound, but `description` overloaded)

**Greenfield sketch**: the frontmatter splits cleanly into four bands: **identity** (`name`, `version`, `license`), **routing** (`triggers: [{phrase, lang, mode: direct|delegated}]` separated from a one-paragraph `summary:` for humans), **dependencies** (`mcp_tools_required[]`, `mcp_tools_optional[]`, `fallback_when_mcp_absent`, plus an explicit `handoffs: [skill-name, ...]` so rename drift becomes a CI check), and **lifecycle hooks** (a small `phase_role:` enum to replace the prose-only "Phase A entry skill" markers scattered across bodies). I would NOT yet add `capabilities[]`, `produces_artifacts[]`, or `phase_gates[]` — those are tempting, but the registry that would consume them is still embryonic; load-bearing fields without consumers are decoration.

**Recommendations**:

#### Refactor — Split `description` into `summary` + `triggers[]`

- **Greenfield grounding**: today `description` is doing three jobs: human-readable summary, auto-routing trigger source, and delegation hint. The validate-checklist description shows the strain — it inlines a routing footnote in prose because the schema can't express "delegation-bound, narrow triggers only."
- **What it unlocks**: machine-checkable trigger discipline (`list_skills` can flag overlap automatically); rename drift in `delegated_from` becomes a CI assertion.
- **What breaks**: Claude Code's auto-router still reads `description` natively — splitting means either platform support OR a build step concatenates `summary + triggers` back to a synthesized `description`. Latter is a 5-line build step.
- **Cost**: M (frontmatter migration across 17 skills + build step)

#### Add — Explicit `handoffs:` field

- **Greenfield grounding**: §7 says "verify B exists when adding a handoff (rename drift breaks handoffs silently)." Greenfield: if rename drift is a known failure mode, declare the dependency, don't audit for it. `handoffs: [author-manifest, review-draft]` makes drift detection a one-line CI check.
- **What it unlocks**: structural drift detection.
- **What breaks**: skills need to declare their handoffs (currently inferred from prose).
- **Cost**: S

#### Add — `phase_role:` enum

- **Greenfield grounding**: 5 skills self-identify in prose as "Phase A entry skill" / "Layer 1" / "watch list responder T6". That's information the orchestrator already needs structurally. Make it frontmatter so PROCEDURE.md routing tables can be regenerated, not maintained as a parallel hand-edited list.
- **What it unlocks**: machine-derivable routing tables.
- **What breaks**: 17 skills need to declare their phase role.
- **Cost**: S

#### Defer — `capabilities[]` field

- **Greenfield grounding**: would let orchestrator planning move from "match keywords in description" to "find skills with capability=review for doctype=festsetzungen." But the doctype manifest isn't capability-tagged either; adding `capabilities[]` to skills without the doctype side is half a refactor.
- **Defer trigger**: when first non-trivial consumer appears (registry use case beyond `list_callables`).
- **Cost when activated**: S (per-skill addition)

#### Keep — `mcp_tools_required[]` / `mcp_tools_optional[]` / `fallback_when_mcp_absent`

- **Greenfield grounding**: meta-rule 5 is real; `list_skills` consumes them; planning depends on them. Empty-array-as-positive-declaration discipline is correct.

#### Keep — Two-track semver split (per-skill vs. plugin.json)

- **Greenfield grounding**: skills evolve at very different cadences. Session-5 minor-vs-patch retroactive correction proves the rule is load-bearing.

---

### Subsystem 5 — Office-config schema

**Verdict**: Refactor (with 2 Reshapes — `extensions.*_manifests` block; integrations classes)

**Greenfield sketch**: top-level keys would be `schema_version`, `office` (identity merged in), `actors` (one list — internal practices and external partners share schema, distinguished by `kind: internal|external`), `roots` (one filesystem-roots block), `scope` (`{domains, states}` unchanged), `conventions`, `templates` (skeleton-source + identity-macros only), and `integrations` (free-form list of `{class, adapter, config}` triples). The `extensions.*_manifests` block disappears entirely — manifests are discovered by walking `<repo>/extensions/{universal,domain/<X>,state/<X>}/` filtered by `scope`. ~30% fewer fields, no derived state stored, no enum-of-integration-classes to outgrow.

**Recommendations**:

#### Reshape — Delete `extensions.{references,doctypes}_manifests`

- **Greenfield grounding**: pure derived state. Wizard already says "this step is mostly automatic — derived from `scope`." Storing derivation = double-bookkeeping; offices end up with stale entries when extension files are renamed.
- **What it unlocks**: ~20 lines from schema, ~30 from wizard; loader walks `<repo>/extensions/...` filtered by scope.
- **What breaks**: requires loader rule update.
- **Cost**: S

#### Reshape — Replace fixed `integrations.{email,calendar,scanner,phone,accounting}` with free-form list

- **Greenfield grounding**: the 5-class taxonomy is a guess. Real planning bureaus integrate with: DMS, GIS, CAD, TöB-Portal, Zeiterfassung, Project-management, Cloud sync, Backup. Current list omits all and includes `phone`/`accounting` (speculative).
- **What it unlocks**: open to extension without schema bumps.
- **What breaks**: trivial migration (flatten the 5-key map into a list).
- **Cost**: S

#### Refactor — Merge `office` and `identity`

- **Greenfield grounding**: split is a v1→v2 artifact. `office.name` and `identity.address_lines[0]` collide; `office.short` and `identity.title` are both naming concerns.
- **Cost**: S

#### Refactor — Merge `practices` and `partners` into `actors`

- **Greenfield grounding**: identical shape. Semantic difference (internal vs. external) is one bit (`kind: internal|external`). Merging makes email-routing logic uniform.
- **Cost**: S

#### Refactor — Consolidate filesystem roots into one `roots:` block

- **Greenfield grounding**: `templates.office_style_dir` is a path. So is `paths.state_root`. Split solely because of historical accident.
- **Cost**: S

#### Keep — `scope = {domains, states}`

- **Greenfield grounding**: load-bearing decomposition for layered manifests. Greenfield alternatives (capability-based, verfahren-stage-based) don't match how legal references actually layer. This is the right axis.

#### Keep — `schema_version` + migration framework

- **Greenfield grounding**: pre-launch normally argues against migration scaffolding. But schema is at v2, migration shipped. Removing now would require re-introducing it the first time real deployment exists. The Reshapes above will produce a v3 — exercise the framework.

---

### Subsystem 6 — Decision rules + Maintenance discipline + conventions docs + audit/design-review pair

**Verdict**: Rough but adequate (with 2 Reshapes)

**Greenfield sketch**: (1) a single `placement.md` containing meta-rules + a flowchart with ~3 questions ("touches durable state? → which scope? → who reads it?") that classifies into the (collapsed) entity types, replacing the linear 6-rule walk; (2) ARCHITECTURE.md as a *thin index* (vision anchor, entity table, link out to placement.md, scope-orthogonality, execution-locality, designed-extensions); (3) conventions split by *concern* not *tier* — `frontmatter-contract.md`, `versioning.md`, `error-envelope.md`, `test-layout.md`; (4) **one** `review` skill with two modes (`compliance` and `soundness`); (5) a real "Maintenance discipline" section that is a *checklist a future session walks* (3 items, not the current narrative paragraph), or removal if it's not load-bearing.

**Recommendations**:

#### Reshape — Collapse Rules 4 + 5 into a single "consumer breadth" question

- **Greenfield grounding**: Rule 4 = "HOW for one or many skills?", Rule 5 = "WHAT (factual reference)?". In practice every cross-cutting memory doc has *both* HOW and WHAT properties (`korrektur-rules.md` is rules + examples; `bauleitplanung-phasen.md` is process facts + reasoning). The HOW/WHAT axis isn't real; the *consumer breadth* axis is (one skill → B; many skills → C).
- **What it unlocks**: 6 rules → 5; the borderline-case discussion ("instruction or knowledge?") becomes moot.
- **Cost**: S (combines with Subsystem 2's collapse)

#### Reshape — Unify audit + design-review into one `review` skill, two modes

- **Greenfield grounding**: both skills are dispatch engines that fan out subagents with a brief and synthesize results. Behavior, output structure, edge cases are nearly identical. Only meaningful difference is brief content — compliance brief vs. greenfield-reframe brief.
- **What it unlocks**: ~50% smaller meta-infrastructure surface; shared PROCEDURE.md; future review modes (security review, performance review) compose as additional briefs without new skills.
- **What breaks**: ARCHITECTURE.md "Maintenance discipline" reference; trigger phrases need explicit mode disambiguation.
- **Counter to consider**: anti-status-quo bias is *load-bearing different* from compliance bias — keeping skills separate enforces the cognitive split. Mode flag in one skill achieves the same separation; trigger phrases already distinguish them.
- **Cost**: M

#### Refactor — Demote ARCHITECTURE.md "Maintenance discipline" to a 3-line checklist

- **Greenfield grounding**: current section is a narrative paragraph + pointers to two skills. Not a checklist anyone walks; a *description of the audit/design-review pair*.
- **What it unlocks**: ARCHITECTURE.md drops ~30 lines; "what to do" becomes 3 imperatives.
- **Cost**: S

#### Add — Deprecation/sunset procedure

- **Greenfield grounding**: plugin has 17 skills, conventions get bumped, MCP tool names declared stable. Yet there's no procedure for *deprecating* a skill, retiring an entity type, or sunsetting a meta-rule. Pre-launch this is theoretical; post-launch it's a real maintenance gap.
- **What it unlocks**: structural lifecycle for retired concepts.
- **Cost**: S

#### Refactor — Backend-conventions.md is half conventions, half ADR

- **Greenfield grounding**: sections include "Alternatives considered" + "Revisit trigger" — these are decision-record artifacts, not conventions. The decision-recording convention (per commit `d6d75f9`) is a different doc-class.
- **What it unlocks**: conventions docs stay scannable as the system grows; alternatives + revisit triggers move to per-decision records under `docs/decisions/` mirroring `docs/rag-pipeline-decisions.md`.
- **Cost**: S

#### Keep — Conventions split by tier (plugin/backend), with scope-boundary headers

- **Greenfield grounding**: temptation is to fold both into ARCHITECTURE.md or split per-concern. Both worse: ARCHITECTURE.md is already long; per-concern split fragments the "I'm writing a skill, what do I need?" entry point.

#### Keep — `mcp_tools_required[]` frontmatter contract

- **Greenfield grounding**: machine-checkable, foreign-key-ready, forces graceful failure. The meta-infrastructure earning the most keep across all reviews.

---

## Cross-cutting recommendations

### CC1 — Architectural simplification pass (meta-rules + entity types + decision rules together)

**Affected subsystems**: 1, 2, 6

**Pattern**: three subsystems independently surfaced "we have too many sibling-level concepts." Across them: 5 → 3-4 meta-rules, 9 → 5 entity types, 6 → 3 decision rules. The recommendations are interdependent (collapsing entity types simplifies decision rules; demoting meta-rules clarifies what entity types are for).

**Suggested action**: do them in one ARCHITECTURE.md rewrite, not piecemeal. The doc emerges shorter, sharper, with a single coherent placement story. Cost: M-L (one focused rewrite session). Impact: every future skill author / reviewer sees the simplified surface.

### CC2 — Lifecycle as first-class concern (invalidation + deprecation + freshness)

**Affected subsystems**: 1, 4, 6

**Pattern**: Subsystem 1 wants an invalidation meta-rule. Subsystem 6 wants a deprecation procedure. Subsystem 4 considered but deferred capability-tagging (a freshness concern in disguise). Existing scattered hooks (review_due, references_used[], schema_version, status flags) all serve lifecycle but aren't unified.

**Suggested action**: a unified lifecycle story across entity types. Adds meta-rule "every entity declares its invalidation contract"; adds deprecation procedure to ARCHITECTURE.md; surfaces existing scattered hooks under a single heading. Cost: M.

### CC3 — Audit + design-review unification

**Affected subsystems**: 6, 3 (orchestrator routing), 4 (one fewer skill)

**Pattern**: subsystem 6 explicitly recommends. The two skills have ~70% structural overlap; their distinct value is in the brief content, not the dispatch engine.

**Counter-argument**: we just built these two skills with deliberate separation. The user explicitly endorsed the split (compliance vs. soundness as distinct cognitive tasks). Trigger phrases are already distinct.

**Suggested action**: **needs-user-decision**. My committed position below.

### CC4 — Frontmatter as machine-checkable contract (handoffs, phase_role, eventually capabilities)

**Affected subsystems**: 4, 3, 6

**Pattern**: subsystem 4 proposes splitting `description` + adding `handoffs[]`/`phase_role:`. Subsystem 3's recommendations rely on machine-derivable routing tables. Subsystem 6 implies conventions docs gain CI-checkable structure.

**Suggested action**: bundle subsystem 4's frontmatter changes (split description, add handoffs, add phase_role) in one migration commit affecting all 17 skills. Defer `capabilities[]` until consumer exists. Cost: M.

### CC5 — Scope as universal layering dimension (not per-type repetition)

**Affected subsystems**: 1, 2, 5

**Pattern**: subsystem 1 demotes scope-orthogonality from meta-rule. Subsystem 2 lifts scope to type-orthogonal property. Subsystem 5 keeps scope = (domains, states) at config level. All three converge on: scope is one universal dimension, applied where it applies, not re-explained per entity type.

**Suggested action**: in the architectural simplification pass (CC1), extract scope into a single canonical section that types reference, not repeat.

---

## Committed positions on user-decision items

### Position on CC3 — audit + design-review unification

**My call: PRESERVE the split** (do not unify).

**Reasoning** (cost-specific, not generic principle):
- The two skills' bodies overlap structurally (~70%), but their *briefs* (the load-bearing differentiator) are deliberately different. Compliance review and soundness review are different cognitive tasks; conflating them via mode flag risks mode-confusion in dispatch.
- Trigger phrases are already distinct (no overlap risk).
- The unification cost is M; the marginal benefit is ~50% smaller meta-infrastructure surface — but that surface is small today (2 skills, ~1500 lines combined). Optimization on a small surface = premature.
- If a third review mode (security, performance) emerges, **then** unification's benefit grows; revisit at that point.
- Counter-counter: this conversation produced both skills carefully; throwing one away would feel like the kind of sunk-cost-adjacent move the design-review skill is supposed to enable AVOIDING. So I checked: would a from-scratch designer build two skills or one? Given the brief-difference is the load-bearing thing, and the dispatch-engine is shared in both, a from-scratch designer might genuinely build one. But the cost of unification post-build > cost of unification pre-build (even pre-launch), so the decision should be: act if you'd build it that way fresh, defer if existing form is "rough but adequate." For this case I judge: **rough but adequate**.

### Position on CC1 — Architectural simplification pass

**My call: ACT, but stage-gate by reviewing one subsystem at a time before committing the others.**

**Reasoning**:
- The recommendations across subsystems 1, 2, 6 are genuinely interdependent — collapsing entity types simplifies decision rules; demoting meta-rules clarifies what entity types are for.
- Doing all three in one rewrite is the lowest-friction path.
- BUT: ARCHITECTURE.md is the most load-bearing doc in the system. A single-shot rewrite of it is high-risk. Stage-gate: rewrite meta-rules first, get user buy-in, then entity types, then decision rules.
- Estimated cost: M-L (1-2 sessions).

### Position on Subsystem 3's orchestrator split (Cost: L)

**My call: ACT — start with extracting watch-list as separate skill (smallest piece). Evaluate before going further.**

**Reasoning**:
- Splitting orchestrator into 3-7 skills is the largest reshape recommended. Doing it all at once is high-risk.
- Watch-list (T1-T6) is the most clearly separable piece — it's a self-contained sub-skill with its own data model.
- Extract it first; if the resulting orchestrator+watch-list shape feels right, continue with gates next, router last. If watch-list extraction reveals problems, reconsider.

### Position on Subsystem 5's office-config Reshapes

**My call: ACT — the schema migration framework exists for exactly this.**

**Reasoning**:
- Both Reshapes (delete `extensions.*_manifests`; replace fixed integrations with free-form list) are well-justified with specific cost-benefit.
- The migration framework (v1→v2 already shipped) is built to handle this.
- `extensions.*_manifests` deletion is especially compelling — it's pure derived state; storing it is double-bookkeeping that already shows in the wizard ("this step is mostly automatic").
- Cost: S each, with schema migration to v3.

### Position on Subsystem 4's frontmatter changes

**My call: ACT — bundle (split description, add handoffs, add phase_role) in one migration commit affecting all 17 skills. Defer `capabilities[]` until consumer exists.**

**Reasoning**:
- `handoffs[]` and `phase_role:` close real drift surfaces with specific cost (declarative beats prose).
- Splitting `description` requires a build step (synthesize description from summary + triggers) — small additional cost, big dividend in machine-checkable trigger discipline.
- 17-skill migration is mechanical (~30 minutes per the precedent of session-5 F-batch + meta-audit batch).
- `capabilities[]` deferral is honest: registry is embryonic; doctypes aren't capability-tagged; half-typed system. Specific reasons, not generic restraint.

---

## Recommended next action

Three immediate paths, in priority order:

### Path 1 (highest leverage) — CC1 architectural simplification pass

Rewrite ARCHITECTURE.md to absorb subsystems 1+2+6 recommendations as one coherent simplification. Stage-gate per session: meta-rules first, then entity types, then decision rules. Each stage gets user review before next.

**Cost**: M-L (1-2 sessions). **Impact**: every future skill author and reviewer sees the simplified surface; every audit and design-review run benefits.

### Path 2 (highest absolute confidence) — Subsystem 5 office-config Reshapes

Delete `extensions.*_manifests`; replace fixed integrations with free-form list; merge office+identity, practices+partners; consolidate roots. Schema migration v2 → v3.

**Cost**: M (one focused session). **Impact**: schema becomes ~30% smaller, no derived state stored, integration surface stops being a guess.

### Path 3 (lowest cost, high mechanical impact) — Subsystem 4 frontmatter migration

Split `description` → `summary` + `triggers[]`; add `handoffs[]`; add `phase_role:`. 17-skill mechanical migration with build step for synthesized description.

**Cost**: S-M (one session). **Impact**: machine-checkable trigger + handoff discipline.

### Defer (per committed positions)

- CC3 audit/design-review unification — preserve split
- CC2 lifecycle-as-first-class — bundles into CC1
- Subsystem 3 orchestrator full split — start with watch-list extraction only

### Recommended ordering

Path 2 → Path 3 → Path 1, then watch-list extraction. Reason: Path 1 is highest-impact but highest-risk; Paths 2 and 3 are bounded mechanical work that builds confidence. After Paths 2+3 land, Path 1's stage-gated rewrite has more confidence behind it.
