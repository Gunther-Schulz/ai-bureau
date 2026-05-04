# Decision record: Scope model ARCH topic (Phase 3.5 first cross-cutting integrator)

## 1. Status

**ACCEPTED** 2026-05-04. Mode 2 upfront-known composite decomposition per `decision-design-sharpening` v0.10.0 §Two decomposition modes — 6 sub-decisions tightly coupled; single composite DR (sub-decisions have no independent meaning outside the composite). LOCK-HARD target-type (architectural decision; cascades hard if revised; cross-cutting integrator template-class anchor).

## 2. Owner

Phase 3.5 — fifth ARCH topic = first cross-cutting integrator (5 of 6 primitive-cluster + cross-cutting integrator topics). Anchors **cross-cutting integrator topic-template-class** (NEW; first instance — parallel to `arch/substrate.md` anchoring Pattern A 12+7 template + `arch/specialist-skill.md` anchoring primitive-cluster Pattern B + atomic-primitive 12+5 template + `arch/practitioner.md` anchoring Pattern C topic-template-class + `arch/workflow-work-unit.md` anchoring two-Pattern-B topic-template-class + `arch/claim-defensibility.md` anchoring PRIMITIVE+DERIVED topic-template-class). Cross-cutting-integrator-specific conditional applicability rules surface here per per-pattern conditional applicability rules in `MAINTENANCE.md` Layer 3 Primitive-cluster topic template (cross-shape policy variation APPLIES; granularity / bundle / marketplace / per-element lifecycle ordering N/A documented). Cited as precedent for downstream cross-cutting integrator topic — `arch/axis-interactions.md` (Phase 3.5 sixth + final ARCH topic per `ARCHITECTURE.md` §5 reading order).

## 3. Related

**Composes with**:
- `docs/decisions/claim-defensibility-arch-topic.md` (just-locked PRIMITIVE+DERIVED topic-template-class anchor; per-claim attestation chain mechanics + content-unit-IN-instance pattern E3 surfaces here as scope-model load-bearing pattern)
- `docs/decisions/workflow-work-unit-arch-topic.md` (workflow_instance + work-unit instance Owner B placement; per-claim attribution chain composes through workflow_instance + work-unit instance)
- `docs/decisions/practitioner-arch-topic.md` (Pattern C bipartite — HUMAN cross-cutting NOT placed per E4 + RECORD Owner B workspace-scope managed entity)
- `docs/decisions/specialist-skill-arch-topic.md` (Pattern B + atomic-primitive bipartite — DEFINITION Framework C bundle nests skill / workflow / work-unit-kind / adapter Implementations per E2 nested-bundle pattern)
- `docs/decisions/audit-arch-topic.md` (mechanism class Framework C Surface + Owner B audit-trail per E5 dual-aspect placement; per-shape audit emission granularity per §14 composes with §8 cross-shape policy variation)
- `docs/decisions/sparring-arch-topic.md` (mechanism class Framework C Surface + Owner B sparring events per E5; per-shape activation matrix per §4 framework-baseline-vs-shape-extension partition composes with §8 cross-shape policy variation)
- `docs/decisions/substrate-arch-topic.md` (Pattern A tri-aspect Framework C Surface + Implementations + Owner B Implementation Instance — substrate parallel to E5 authority-binding dual-aspect placement; substrate Surface §F session/context for cross-deployment claim portability per W2)
- `docs/decisions/adapter-arch-topic.md` (Pattern A tri-aspect Framework C + Owner B Instance bindings; framework-baseline-vs-shape-extension partition per §3 composes with §8 cross-shape policy variation)
- `docs/decisions/greenfield-rederivation-pause.md` (Step 1.A Phase 2 GLOSSARY foundational vocabulary lock incl. Framework C scope + Owner B scope + Layer A scope + workspace + deployment + authority-binding)
- `docs/decisions/quality-gate-scope-lock.md` (Pattern A; Phase 3.6 forthcoming — quality-gate Framework C Pattern A + Owner B observability source)
- `docs/decisions/phase-3-2-doc-organization.md` (Sub-decision 3 LOCK: NO content migration MAINTENANCE.md ↔ arch/scope-model.md; layer-distinction maintained)

**GLOSSARY entries** (locked; cited extensively):
- `Framework C scope` (canonical SCOPE-CLASSIFICATION for distributable definitions; member catalog enumeration)
- `Owner B scope` (canonical SCOPE-CLASSIFICATION for deployment-specific instances; engagement-target shape-policy-mandated rule per E4 cross-shape policy variation)
- `Layer A scope` (canonical SCOPE-CLASSIFICATION for layered content; orthogonal axis to mechanism/policy framing)
- `workspace` (PRIMITIVE cross-cutting; deployment-instance container integrating all three scopes per §3 workspace integration)
- `deployment` (DERIVED concept; workspace-as-bound-runtime; 1:1 reciprocal at framework primitive level per W3)
- `framework` + `mechanism` + `policy` + `shape` + `protocol-architectural` (foundational meta-primitives; Framework C derives from `framework = mechanisms`)
- `substrate` + `adapter` (Pattern A primitives composing through scope-model per §4)
- `specialist` + `skill` + `practitioner` + `workflow` + `work-unit` + `claim` + `defensibility` (primitive-cluster primitives composing through scope-model per §4)
- `engaged-authorship` + `authority-binding` (DERIVED + mechanism composing through scope-model per E4 + E5)
- `actor` + `event` + `session` + `pioneer-instance` (cross-cutting primitives composing through scope-model per §4)
- `intertwining` + `sparring` + `authorship-preservation` + `co-worker` + `intertwined-ai` + `tacked-on-ai` + `answer-machine-ai` + `oracle-ai` + `validator-ai` + `rubber-stamping` + `category-collapse` (axis primitives + DERIVED; cross-cutting non-placed per E4)

**Forward-references** (future Phase 3.5 + Phase 3.6 topics):
- `arch/axis-interactions.md` (cross-cutting integrator; Phase 3.5 sixth + final ARCH topic — cross-axis composition surface complementary to scope-model's structural surface)
- `arch/quality-gate.md` (Pattern A Phase 3.6 — quality-gate Framework C Pattern A + Owner B observability source)

**Disciplines applied**:
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Framework = mechanisms; Shape = policies" (foundational architectural commitment grounding Framework C derivation)
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "A-B-C scope model" (preliminary-locked three-scope classification grounding §2 per-scope structural overview)
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Atoms vs containers" (mechanism + policy atomic primitives; framework + shape META-PRIMITIVE containers)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (make-wrong-shapes-impossible — structural over conventional discipline applied to scope-categorization through Pydantic gate dispatch on `framework_kind` + `owner_scope` + `layer_scope`)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (pattern-vs-instance — scope-model primitives stay shape-neutral / archetype-neutral / pioneer-neutral; cross-archetype illustration anchors framework neutrality)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 (preliminary-lock — A-B-C scope model preliminary-locked per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; revisable when concrete entity-md authoring exercises Phase 3+ reveal mismatches)
- `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment workspace.md authoring happens at deployment-instance; not framework repo)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 4 (cascade-prevention; greenfield-draft + minimize-embedded + cascade-pass + foundation-first); Discipline 7 (cascade discipline structural consistency); Discipline 8 (foundation-up workflow ordering — scope-model is fifth Phase 3.5 ARCH topic + first cross-cutting integrator anchor); Discipline 10 (greenfield-evaluation of archived sources); Discipline 11 (effort-switch cluster-execution map)

**Archived sources**: NONE expected for scope-model — foundations are `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE (preliminary-locked Phase 1.85 + cascade discipline) + `glossary/framework-c-scope.md` + `glossary/owner-b-scope.md` + `glossary/layer-a-scope.md` + `glossary/workspace.md` (locked Phase 2 GLOSSARY foundational vocabulary per `docs/decisions/greenfield-rederivation-pause.md` Step 1.A); not archive territory per `disciplines/10-greenfield-evaluation.md` greenfield-evaluation rule.

## 4. Context

Phase 3.5 first cross-cutting integrator ARCH topic (5th overall in Phase 3.5; fifth ARCH topic). Prior to this DR, Phase 3.5 first primitive-cluster topic (specialist-skill) LOCKED at commit `f6bab6e`; Phase 3.5 second primitive-cluster topic (practitioner) LOCKED at commit `7ffe93a`; Phase 3.5 third primitive-cluster topic (workflow-work-unit) LOCKED at commit `3b187ea`; Phase 3.5 fourth primitive-cluster topic (claim-defensibility) LOCKED at commit `a9fbbfa` per `ARCHITECTURE.md` §7; Pattern A protocol topics + mechanism-class topics LOCKED in Phase 3.4.

**Why scope-model chosen fifth** (foundation-up per Discipline 8 + per `ARCHITECTURE.md` §5 reading order LAST cross-cutting integrators): scope-model composes with all 8 already-locked Phase 3.4 + Phase 3.5 ARCH topics (substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility) + 4 scope GLOSSARY entries (Framework C / Owner B / Layer A / workspace) + deployment + authority-binding mechanism. Locking scope-model fifth means per-primitive scope placement locks against validated upstream primitive surfaces. Reverse ordering would force scope-model to forward-reference unlocked primitive topics. 5 of 6 Phase 3.5 ARCH topics close with this lock; only `arch/axis-interactions.md` remains per `ARCHITECTURE.md` §5 reading order (Phase 3.5 sixth + final ARCH topic).

**Why cross-cutting integrator topic-template-class anchored here**: scope-model is the FIRST cross-cutting integrator instance (axis-interactions Phase 3.5 sixth + final ARCH topic will inherit/extend per per-pattern instance-driven trigger pattern per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`). The 12+5 primitive-cluster topic template extends to cross-cutting integrators WITHOUT variation; per-pattern conditional applicability rules surface here:
- §8 Cross-shape policy variation APPLIES (engagement-target Owner B managed entities are shape-policy-mandated per `glossary/owner-b-scope.md`)
- §9 Granularity tests N/A (cross-cutting integrators have no granularity-test surface; scope-categorization is binary not granular; granularity discriminators live in respective primitive-cluster topics)
- §10 Bundle composition N/A (scope-model doesn't bundle artifacts; Framework C bundling is specialist's domain per `arch/specialist-skill.md` §10)
- §11 Marketplace + distribution mechanics N/A (scope-model is integrator topic, not independently distributable)
- §12 N/A-parity preserved per primitive-cluster + Pattern A precedent
- §13 Per-element lifecycle ordering N/A (scope categories are placement classifications, not entities with boot/shutdown/activation ordering distinct from §5; relevant ordering covered in `ARCHITECTURE.md` §6 composite boot subsection per E1)

Cross-cutting-integrator-specific conditional applicability surfaces here. `arch/axis-interactions.md` will inherit this DR's anchor for conditional applicability rules.

**What the decision-design phase needed to resolve**:
- Cross-cutting integrator topic-template-class confirmation (12+5 extends without variation; per-pattern conditional applicability rules)
- Per-scope structural overview (Framework C / Owner B / Layer A — derivation + member catalog + identity convention + properties + boundary test per scope) without duplicating MAINTENANCE.md TOP-LEVEL ARCHITECTURE high-level summary
- Workspace integration as cross-scope composition WITHIN cluster (workspace IS the binding-instance entity at Owner B)
- Per-primitive composition with framework primitives outside cluster + 4 NEW patterns surfaced (E2 nested-bundle / E3 content-unit-IN-instance / E4 cross-cutting non-placed / E5 authority-binding placement)
- Per-scope cardinality + lifecycle + per-element Mode distribution within scopes
- Cross-shape policy variation 6-row matrix + cross-axis composition + W1-W4 watch-list

## 5. Decision

Six sub-decisions per Mode 2 composite decomposition (sub-decisions have no independent meaning outside the composite; foundation-up dependency ordering applied within the composite).

### SD-1: Cross-cutting integrator template structure (NEW template-class anchor)

**Decision**: 12+5 cross-cutting integrator template-class **anchored at this topic** (preserves §-numbering parity with primitive-cluster 12+5 anchor per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template subsection). 18 sections total: 12 common-required (§§1-7 + §§14-18) + 5 conditional-slot (§§8-13 with §12 N/A-parity). 12+5 template extends to cross-cutting integrators **without variation**.

**Cross-cutting-integrator-specific conditional applicability**:
- §8 Cross-shape policy variation: APPLIES (engagement-target Owner B managed entities shape-policy-mandated per `glossary/owner-b-scope.md`)
- §9 Granularity tests: N/A documented (cross-cutting integrators have no granularity-test surface; scope-categorization is binary classification)
- §10 Bundle composition: N/A documented (scope-model doesn't bundle artifacts; Framework C bundling is specialist's domain)
- §11 Marketplace + distribution mechanics: N/A documented (scope-model is integrator topic, not independently distributable)
- §12: N/A-parity preserved per locked template convention
- §13 Per-element lifecycle ordering: N/A documented (scope categories are placement classifications; lifecycle ordering covered in `ARCHITECTURE.md` §6 composite boot subsection per E1)

**Why N/A documented explicitly**: per `MAINTENANCE.md` Layer 3 template "document N/A explicitly when section is omitted" rule. DO NOT skip section numbering — keep §9/§10/§11/§12/§13 as N/A sections preserving template-anchoring stability for downstream cross-cutting integrator topics (`arch/axis-interactions.md` Phase 3.5 sixth + final ARCH topic).

**Total expected**: 18 sections (12 common + 1 conditional applies (§8) + 4 N/A documented (§9 + §10 + §11 + §13) + §12 N/A-parity). This anchors cross-cutting integrator template-class. axis-interactions topic (Phase 3.5 sixth + final) will inherit/extend per per-pattern instance-driven trigger pattern.

### SD-2: Per-scope structural overview (§2 = 3 sub-sections)

**Decision**: §2 articulates each scope category structurally without duplicating MAINTENANCE.md TOP-LEVEL ARCHITECTURE high-level summary (per Phase 3.2 Sub-decision 3 LOCK: NO content migration MAINTENANCE.md ↔ arch/scope-model.md; layer-distinction maintained — MAINTENANCE.md provides one-line summary + atom/container framing; this topic provides architectural-conceptual articulation).

**§2.1 Framework C scope** — derivation from `framework = mechanisms`; member catalog (mechanism / shape / substrate / protocol-implementation / specialist DEFINITION + nested Framework C children per E2); identity convention (`framework_kind` + `framework_key`); properties (universal / immutable at definition level / distributable per `profiles/G-composability-gate.md` multi-mode consumption framing); boundary test per `glossary/framework-c-scope.md`.

**§2.2 Owner B scope** — derivation from `framework + shape → workspace deployment`; member catalog (workspace itself + workspace-scope managed entities universal {practitioner-record + Actor} + shape-policy-mandated {engagement-target entities Client/Customer/Funder/Co-author/Institution per shape per `glossary/owner-b-scope.md`} + specialist instance content + workflow_instance instances + work-unit instances); identity convention (`owner_scope` + `owner_key`); properties (deployment-specific / workspace-bound); boundary test.

**§2.3 Layer A scope** — derivation as **orthogonal axis** (NOT derived from framework/shape — independent classification axis per `glossary/layer-a-scope.md`); member catalog (references / doctypes / bausteine / memory prose / conventions / domain-specific knowledge); identity convention (`layer_scope` + `layer_key`); Layer values (`universal` / `domain` / `state`); properties (content varying by domain/state context); boundary test.

### SD-3: Workspace placement integration (§3 cross-element composition WITHIN cluster)

**Decision**: §3 articulates workspace IS the integration point of all 3 scopes — load-bearing cross-scope composition WITHIN cluster (parallel to primitive-cluster §3 cross-primitive composition WITHIN cluster).

**Workspace as central Owner B instance + container**:
- workspace.md as binding-instance entity at Owner B
- workspace's role as central Owner B instance + container for workspace-scope managed entities
- workspace.scope.{domains, states} configuration determining Layer A applicability
- workspace.specialists_active list referencing Framework C specialist DEFINITIONs
- workspace.shape selecting Framework C shape definition
- workspace.substrate selecting Framework C substrate definition; substrate Implementation Instance running in workspace at Owner B
- 1:1 reciprocal cardinality with deployment per `glossary/deployment.md`
- Workspace identity persistence across multiple deployments (W3 watch-list)
- Multi-environment scenarios (N workspaces) vs multi-tenant scenarios (substrate-Instance-level concern, NOT framework-level cardinality concern)

**E1 (Round 2 expansion) — workspace boot integration**: workspace.md loading realizes scope-categories in ordered sequence (Framework C selections via specialists_active / shape / substrate references → Owner B instances loaded incl. workspace-scope managed entities → Layer A content scope-resolved per workspace.scope configuration). Composes with `ARCHITECTURE.md` §6 composite boot subsection (audit-phase 1-3 → substrate-phase 1-5) — scope-categorization realization fires INSIDE substrate-phase 1-5 envelope, NOT separate boot phase.

### SD-4: Cross-scope composition + per-primitive composition table (§4 outside-cluster + §18 table)

**Decision**: §4 narrative for primitives whose scope-placement has load-bearing nuance + 4 NEW PATTERNS surfaced Round 2 + §18 per-primitive composition table.

**E2 nested-bundle pattern**: specialist Framework C bundle NESTS other Framework C definitions (skill DEFINITIONs + workflow DEFINITIONs + work-unit KIND DEFINITIONs + adapter Implementations) under **specialist-namespace** per `glossary/specialist.md` locked mechanic — fully-qualified references `specialist-name:skill-name` / `specialist-name:kind-name` / `specialist-name:workflow-name`. Distinct from atomic Framework C primitives (substrate / shape / mechanism — no nested Framework C children). Load-bearing pattern preventing cross-specialist KIND/skill/workflow-name collision.

**E3 content-unit-IN-instance pattern**: claim is **content-unit IN work-unit** (NOT separately scoped — INHERITS work-unit's Owner B placement) per `arch/claim-defensibility.md` lock + `glossary/claim.md`. Distinct from instance-content-at-Owner-B placement (specialist instance content / work-unit instance) — content-unit pattern is INSIDE-the-instance-payload, not a separately-placed Owner B sub-entity. Documents claim's cross-pattern destruction inheritance per `arch/claim-defensibility.md` §13 (claims inherit work-unit's `instance_content_dissolution_policy: archive | delete-with-audit`).

**E4 cross-cutting non-placed pattern**: properties/tests/concepts that are NOT placed get explicit N/A documentation in §18 table:
- defensibility (DERIVED property; not entity)
- engaged-authorship (DERIVED axis-3 success mode; not entity)
- category-collapse (cross-axis force; not entity)
- failure modes: rubber-stamping / answer-machine-AI / oracle-AI / validator-AI / tacked-on-AI / intertwined-AI (not entities)
- VISION axes: intertwining / sparring / authorship-preservation (cross-cutting concepts; not entities)
- co-worker (relational claim; not entity)
- HUMAN practitioner aspect = cross-cutting (NOT placed); RECORD aspect = Owner B (placed)

**E5 authority-binding scope-placement**: authority-binding mechanism per `glossary/authority-binding.md` PRIMITIVE / framework-mechanism placement = **Framework C** (mechanism definition home); manifests at runtime as `actor_kind` + actor identity recorded ON events at Owner B (audit-trail). Same dual-aspect placement as substrate Surface (Framework C definition + Implementation Instance at Owner B); same shape as audit mechanism class (Surface at Framework C + events at Owner B).

**§4 narrative load-bearing primitives** (per-primitive composition narrative):
- substrate (Pattern A; Surface + Implementations Framework C; Implementation Instance Owner B — tri-aspect)
- adapter (Pattern A; Surface + per-class Surface + Implementations Framework C; instance bindings Owner B)
- sparring (mechanism class Pattern D; Surface Framework C; events Owner B in audit-trail)
- audit (mechanism class Pattern D; Surface + AuditEvent schema Framework C; audit-trail Owner B)
- specialist (bipartite Pattern B; DEFINITION Framework C; instance content Owner B; nested-bundle pattern E2)
- skill (atomic within specialist; DEFINITION nested in specialist's Framework C bundle under specialist-namespace; per-skill events Owner B)
- practitioner (bipartite Pattern C; HUMAN cross-cutting NOT placed; RECORD Owner B)
- workflow (bipartite Pattern B; KIND DEFINITION nested in specialist's Framework C bundle; workflow_instance Owner B)
- work-unit (bipartite Pattern B; KIND DEFINITION nested in specialist's Framework C bundle; instance Owner B)
- claim (PRIMITIVE; content-unit IN work-unit; INHERITS work-unit's Owner B placement — pattern E3)
- defensibility (DERIVED; property/test; NOT placed — pattern E4)
- engaged-authorship (DERIVED axis-3 success mode; NOT placed; events captured at Owner B — pattern E4)
- authority-binding (mechanism; Framework C definition + Owner B event recording — pattern E5)
- mechanism / policy / shape / protocol-architectural (definitions Framework C)
- session (bounded interaction unit within workspace; Owner B)
- event / actor (records at Owner B; AuditEvent schema definition at Framework C)

**§18 composition table** = per-primitive scope-placement table; rows per primitive locked in current corpus (~25 rows including DERIVED N/A entries per E4).

### SD-5: Per-shape policy variation (§8) + cross-axis composition

**Decision**: §8 6-row matrix (parallel to claim-defensibility / workflow-work-unit / practitioner precedent):
1. **Engagement-target Owner B managed entity catalog per shape** (practitioner-shape: Client; autonomous-business-shape: Customer; research-lab-shape: Funder/Co-author/Institution; personal-OS-shape: none — engagement-target entity not universal per `glossary/owner-b-scope.md`)
2. **workspace.md required fields per shape** (multi-practitioner authorship requirements / legal-entity context per `arch/practitioner.md` §4)
3. **Workspace-scope managed entity universals + shape-extensions per shape** (universals: practitioner-record + Actor; shape-extensions: engagement-target entity per shape policy)
4. **Layer A scope configuration defaults per shape** (default `domains` / `states` recommendations per shape archetype)
5. **Specialists_active recommended set per shape** (e.g., practitioner-shape recommends sparring-relevant specialists)
6. **Substrate selection constraints per shape** (per `arch/audit.md` §14 cross-shape policy variation precedent + `arch/sparring.md` §4 framework-baseline-vs-shape-extension partition — practitioner-shape substrate must support claim-level audit granularity + sparring sub-mechanisms 1-4 architecturally-encoded; autonomous-business support action-level audit + budget-policy authority-binding; research-lab claim-level; personal-OS may support light audit)

**Cross-axis composition narrative** (in §8 + §4 composition table):
- **axis-1 (intertwining)**: workspace IS the container for AI-co-worker intertwining per `glossary/workspace.md` cross-axis classification
- **axis-2 (sparring)**: sparring events captured at Owner B in audit-trail; activation matrix per shape (Pattern D) is workspace-policy-mediated through shape policy bundle at Framework C
- **axis-3 (authorship preservation)**: defensibility resolves at claim/work-unit granularity (Owner B); workspace's accountability scope = scope of practitioner-author defensibility; cross-deployment claim portability = cross-Owner-B reference per `arch/substrate.md` §F + `arch/claim-defensibility.md` §6

### SD-6: W1-W4 watch-list (§14) + cross-references (§17)

**Decision**: §14 watch-list (4 items; each names specific external signal + resolution mechanism per `MAINTENANCE.md` no-defer principle):
- **W1**: Multi-tenant federation scope-model variation (composes with `arch/practitioner.md` W1) — when workspace federation surfaces, federated-Owner-B mechanism design
- **W2**: Cross-deployment claim portability scope-model variation (composes with `arch/claim-defensibility.md` W2 + `arch/substrate.md` §F) — when first cross-deployment claim ingestion lands, scope-model addresses claim-as-portable-across-Owner-B
- **W3**: Workspace identity persistence schema (per `glossary/workspace.md` Cardinality + `glossary/deployment.md`) — Phase 6 spec for workspace identity portability across substrate migration / backup-restore / re-activation
- **W4**: Engagement-target entity catalog per second-shape productization (composes with BACKLOG shape-neutrality watch-list) — when second shape lands, engagement-target entity for that shape (Customer / Funder / etc.) fully realized

**§17 cross-references**: 4 scope GLOSSARY entries + workspace + deployment + Disciplines (1, 4, 7, 8, 10) + 8 prior locked ARCH topics (substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit / claim-defensibility) + Phase 6 spec target + archived sources (none expected for scope-model per Discipline 10 greenfield-evaluation rule — foundations are MAINTENANCE.md + locked Phase 2 GLOSSARY).

### §7 Pre-implementation operational concerns (Phase 6 forward-references — Round 2 EXPANSIONS E6 + E7)

- **E6 schema evolution forward-reference**: per-scope identity convention may need `version` field for schema evolution (Framework C definitions distributable per G profile mode 4 marketplace future-conditional + mode 1 consulting versioning concerns; Owner B workspace serialization format per `glossary/deployment.md` workspace-portability concern Phase 6 spec; Layer A content versioning per shape catalog curator L9 perspective). Phase 6 spec: per-scope identity uniqueness rules + schema versioning semantics + breaking-change documentation discipline. NOT locked at ARCH level.

- **E7 scope-categorization error categories forward-reference**: scope-categorization errors that surface at runtime — invalid framework_kind reference (workspace.specialists_active references non-existent specialist DEFINITION); orphan owner_scope reference (workspace-scope managed entity references non-existent workspace); Layer A content scope-mismatch (workspace.scope.domains lists domain with no Layer A content available); cross-deployment scope-resolution failure (workspace identity persistence W3-related). Phase 6 spec: error catalog + recovery semantics. NOT locked at ARCH level.

## 6. Sharpening provenance

### Round 1 (full monty)

EXPANSIONS surfaced (count: 7 — sub-decision-batched per Mode 2 upfront-known composite per `decision-design-sharpening` v0.10.0 §Two decomposition modes "Sub-decision inventory" step):

- **SD-1 EXPANSION**: cross-cutting integrator topic-template-class confirmation (12+5 extends WITHOUT variation; per-pattern conditional applicability rules — §8 APPLIES + §9/§10/§11/§13 N/A documented + §12 N/A-parity = 18 sections total)
- **SD-2 EXPANSION**: §2 = 3 sub-sections per scope category (Framework C / Owner B / Layer A) — derivation + member catalog + identity convention + properties + boundary test per scope (avoids duplicating MAINTENANCE.md TOP-LEVEL ARCHITECTURE per Phase 3.2 Sub-decision 3 LOCK)
- **SD-3 EXPANSION**: workspace integration as cross-scope composition WITHIN cluster (workspace IS the binding-instance entity at Owner B; workspace's role as central Owner B instance + container; workspace.scope configuration determining Layer A applicability; workspace.specialists_active referencing Framework C; workspace.shape + workspace.substrate selecting Framework C definitions; 1:1 reciprocal cardinality with deployment; workspace identity persistence across multiple deployments)
- **SD-4 EXPANSION**: §4 per-primitive narrative for primitives whose scope-placement has load-bearing nuance + §18 composition table (~25 rows including DERIVED N/A entries; one row per already-locked primitive)
- **SD-5 EXPANSION**: §8 6-row cross-shape policy variation matrix + cross-axis composition narrative in §4 composition table (axis-1 workspace IS container for intertwining; axis-2 sparring events captured at Owner B; axis-3 defensibility resolves at claim/work-unit Owner B granularity)
- **SD-6 EXPANSION**: §14 W1-W4 watch-list (multi-tenant federation / cross-deployment claim portability / workspace identity persistence schema / engagement-target catalog per second-shape productization) + §17 cross-references composing 8 prior ARCH topics + 4 scope GLOSSARY entries + workspace + deployment + Disciplines

### Round 2 (user-triggered)

Cross-cutting + schema-detail refinements (per `decision-design-sharpening` §Round 2 layered coverage observation: cross-cutting + schema details emphasized):

**Cross-cutting refinements (E1-E7)** — 7 items:
- **E1**: §3 workspace boot integration — workspace.md loading realizes scope-categories in ordered sequence per `ARCHITECTURE.md` §6 composite boot subsection (Framework C selections → Owner B instances → Layer A scope-resolution INSIDE substrate-phase 1-5 envelope, NOT separate boot phase)
- **E2** (REVISION-flavored): nested-bundle pattern surfaced as load-bearing cross-cutting structural commitment (specialist Framework C bundle NESTS other Framework C definitions under specialist-namespace per `glossary/specialist.md` locked mechanic; quad-closure across glossary/specialist + glossary/skill + glossary/work-unit + glossary/workflow per Note 56 R-N-1; explicit cross-cutting structural pattern documentation at scope-model articulation; REVISION-flavored EXPANSION cumulative count update — implicit-to-explicit elevation pattern)
- **E3** (REVISION-flavored): content-unit-IN-instance pattern surfaced as load-bearing cross-cutting structural commitment (claim is content-unit IN work-unit; INHERITS work-unit's Owner B placement per `arch/claim-defensibility.md` §3 + §13 cross-pattern destruction inheritance; distinguishes content-level atomic assertions from entity-level Owner B sub-instances; REVISION-flavored EXPANSION cumulative count update — implicit-to-explicit elevation pattern)
- **E4**: cross-cutting non-placed pattern explicit documentation (defensibility / engaged-authorship / category-collapse / failure modes / VISION axes / co-worker / HUMAN practitioner aspect — properties/tests/concepts that are NOT placed; explicit N/A documentation in §18 table)
- **E5**: authority-binding scope-placement dual-aspect (Framework C mechanism definition + Owner B event recording; same dual-aspect placement as substrate + audit mechanism class)
- **E6**: §7 schema evolution forward-reference (per-scope identity convention may need `version` field for schema evolution; Phase 6 spec)
- **E7**: §7 scope-categorization error categories forward-reference (invalid framework_kind / orphan owner_scope / Layer A scope-mismatch / cross-deployment scope-resolution failure; Phase 6 spec)

**Round 2 EXPANSIONS count**: 7 substantive findings (E1-E7). Per `decision-design-sharpening` §Empirical density check: Round 1 = 7 EXPANSIONS (sub-decision-batched); Round 2 = 7 EXPANSIONS — holds within ±25% (DECAY NOT DEFINITIVELY CONFIRMED region per density-behavior table; AMBIGUOUS-to-CONTINUE region — but Q5 specific termination signal named per §Termination signal section + Q4 no unaddressed pass + manufactured-comfort counter-test passed). Round 2 layered coverage emphasized cross-cutting (E1 boot integration + E4 cross-cutting non-placed) + schema details (E6 + E7) per Round 2 layered coverage Round 2 emphasis. STABLE LOCK at Round 2 per Q5 specific termination signal + cross-cutting integrator narrow architectural surface (1 conditional applies vs multiple for primitive-cluster topics).

### Manufactured-criticism rejections

Per `decision-design-sharpening` §Manufactured-comfort counter-test + §Pareto calibration: reject refinements that aren't Pareto-improving OR that surface manufactured-criticism territory.

Cumulative count: 3 (Round 1):

- **CA-1 rejected**: Fold scope-model into MAINTENANCE.md TOP-LEVEL ARCHITECTURE (eliminate ARCH topic) — REJECTED. Per Phase 3.2 Sub-decision 3 LOCK: NO content migration MAINTENANCE.md ↔ arch/scope-model.md (layer-distinction maintained — MAINTENANCE.md provides one-line summary + atom/container framing; arch/scope-model.md provides architectural-conceptual articulation). Eliminating the ARCH topic would violate Phase 3.2 layer-distinction lock + force MAINTENANCE.md to absorb 400-500 lines of architectural-conceptual articulation that belongs at Layer 3 not Layer 0.

- **CA-2 rejected**: Different §-shape for cross-cutting integrator (different from primitive-cluster 12+5; reduce to 8+3 or similar) — REJECTED. Per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template + per per-pattern instance-driven trigger pattern (per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`): downstream topic-template-classes inherit 12+5 with conditional applicability variation, NOT structural §-shape variation. §-numbering parity preserved across all topic-template-classes (substrate Pattern A 12+7; specialist-skill primitive-cluster Pattern B + atomic 12+5; practitioner Pattern C 12+5; workflow-work-unit two-Pattern-B 12+5; claim-defensibility PRIMITIVE+DERIVED 12+5). Cross-cutting integrator inherits same.

- **CA-3 rejected**: Force 6 sub-decisions onto a smaller surface (e.g., split SD-4 into per-pattern sub-decisions E2/E3/E4/E5 each as separate sub-decision) — REJECTED. SD-4 is the per-primitive composition narrative + composition table; the 4 NEW patterns (E2/E3/E4/E5) are cross-primitive structural commitments WITHIN SD-4, not independent decisions. Splitting would force foundation-up dependency drift (E2 + E3 are REVISION-flavored EXPANSIONS surfacing implicit cross-cutting patterns from prior primitive-cluster locks; E4 + E5 are explicit pattern documentation). Per Mode 2 §Composite decomposition criteria: sub-decisions must have visible dependency edges + be individually small enough for 2-round sweet spot. The 4 patterns share dependency edge (cross-primitive structural commitments WITHIN scope-model articulation surface).

### GLOSSARY back-check verdict

Per `MAINTENANCE.md` Bidirectional cascade + `decision-design-sharpening` v0.5.0 GLOSSARY back-check at Round 2 termination.

**Verdict**: CLEAN — no retro-fits needed. Flag E2 + E3 as candidate retro-fits if downstream cascade-work-lag surfaces (per BACKLOG "3-tier REVISION/EXPANSION discriminator codification" cumulative count signal evaluation):

- **E2 nested-bundle pattern**: NOT glossary-grade per Bidirectional cascade rule — already captured in `glossary/specialist.md` composes-with skill / work-unit / workflow rows per Note 56 R-N-1 quad-closure (specialist-namespace mechanic; fully-qualified references). Scope-model articulates the cross-cutting structural pattern that emerges from existing locked specialist-namespace mechanic; no retro-fit needed (the mechanic is already locked at GLOSSARY; scope-model elevates the pattern to explicit cross-cutting documentation).
- **E3 content-unit-IN-instance pattern**: NOT glossary-grade per Bidirectional cascade rule — already captured in `glossary/claim.md` composes-with work-unit row + `glossary/work-unit.md` composes-with claim row + `arch/claim-defensibility.md` §3 + §13 cross-pattern destruction inheritance. Scope-model elevates the pattern to explicit cross-cutting documentation; no retro-fit needed.
- **E4 cross-cutting non-placed pattern**: NOT glossary-grade — already captured in respective DERIVED entries' Class tags (`glossary/defensibility.md` Class: DERIVED; `glossary/engaged-authorship.md` Class: DERIVED; etc.) + `glossary/practitioner.md` Pattern C bipartite (HUMAN cross-cutting + RECORD Owner B per locked GLOSSARY).
- **E5 authority-binding placement pattern**: NOT glossary-grade — already captured in `glossary/authority-binding.md` Three architectural sub-aspects (per-event actor declaration + per-claim author attribution + authority-decision binding) + Composes-with substrate row + Composes-with audit row (Framework C definition + Owner B event recording dual-aspect documented at GLOSSARY).

**Pattern observation**: Cross-cutting integrator narrower surface produces less GLOSSARY-grade material — parallel to claim-defensibility cluster Note 59 verdict ("PRIMITIVE+DERIVED narrower surface produces less GLOSSARY-grade material"). Cross-cutting integrators ANALYZE composition ACROSS prior topics; don't introduce new glossary-grade primitives. The 4 NEW patterns (E2/E3/E4/E5) are explicit documentation of cross-cutting structural commitments emerging from prior primitive-cluster + Pattern A + mechanism-class locks; not new vocabulary requiring GLOSSARY retro-fit. Flag for Coherence-audit C2 evaluation if downstream cascade-work-lag surfaces (per BACKLOG watch-list).

### Profile-anchored validation

Per `decision-design-sharpening` v0.5.0+ profile-anchored validation + `profiles/INDEX.md` cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators).

**4 cluster representatives Read** (≥3 cluster coverage requirement; FULL DETAIL profile content cited NOT cluster letters):

**Cluster A Producers** — `profiles/L1-specialist-creator.md` (specialist creators authoring Framework C nested-bundle per E2; SKELETON profile fleshed-on-demand for this validation):
- L1 specialist creator validates SD-2 Framework C member catalog (specialist DEFINITION as Framework C bundle nesting skill / workflow / work-unit-kind / adapter Implementations per E2 nested-bundle pattern); specialist-namespace mechanic per Note 56 R-N-1 grounds cross-specialist composition rules
- L1's specialist creator profile validates SD-4 nested-bundle pattern (E2): specialists author Framework C bundles with nested children under specialist-namespace; cross-specialist references via fully-qualified `specialist-name:skill-name` / `specialist-name:workflow-name` / `specialist-name:kind-name`
- Verdict: covered (skeleton profile provides sufficient evidence for cross-cutting integrator validation per `profiles/INDEX.md` skeleton-fleshing-on-demand strategy)

**Cluster B Deployers** — `profiles/L4a-workspace-deployer-solo.md` (workspace deployers integrating Framework C selections + Owner B instances + Layer A configuration; SKELETON profile fleshed-on-demand for this validation):
- L4a workspace deployer validates SD-3 workspace integration (workspace.md authoring integrates Framework C selections via specialists_active + shape + substrate references; Owner B instances loaded incl. workspace-scope managed entities; Layer A content scope-resolved per workspace.scope configuration)
- L4a workspace deployer validates SD-5 §8 cross-shape policy variation matrix (per-shape engagement-target catalog + per-shape workspace.md required fields + per-shape Layer A scope configuration defaults + per-shape specialists_active recommended set + per-shape substrate selection constraints)
- Verdict: covered (skeleton profile provides sufficient evidence)

**Cluster B Deployers + Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` (pioneer; multi-cluster member):
- L5a lines 76-93 active specialists + active shape practitioner-shape + active substrate Claude Agent SDK + active adapters + Layer A scope domains/states configuration: validates SD-3 workspace integration (workspace IS the binding-instance entity at Owner B integrating Framework C selections + Owner B instances + Layer A scope configuration)
- L5a lines 14-17 PBS-Schulz pioneer single-practitioner deployment: validates SD-2 Owner B placement (workspace itself + workspace-scope managed entities universal practitioner-record + Actor) + SD-5 §8 practitioner-shape engagement-target Client + workspace.md required fields multi-practitioner cardinality solo-1 + Layer A scope domains = {planning / naturschutz / environmental-law / baurecht} states = {DE-BB})
- L5a lines 76-93 active substrate Claude Agent SDK: validates SD-4 substrate placement (Pattern A; tri-aspect Framework C Surface + Implementations + Owner B Implementation Instance running per workspace) + SD-5 §8 substrate selection constraints per shape (practitioner-shape substrate must support claim-level audit granularity + sparring sub-mechanisms 1-4 architecturally-encoded per `arch/sparring.md` §4)
- Verdict: covered

**Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` + L5d auditor mental-modeling (per `profiles/INDEX.md` D Defer Gate procedure; L5d skeleton fleshed-on-demand):
- L5a planner B-Plan-Begründung work-unit instances (project kind per `glossary/work-unit.md` Cross-archetype illustration): validates SD-4 work-unit placement (Pattern B bipartite KIND DEFINITION nested in specialist's Framework C bundle per E2 + work-unit instance Owner B) + claim placement (PRIMITIVE; content-unit IN work-unit instance INHERITS work-unit's Owner B placement per E3)
- L5d auditor mental-modeling: audit work-unit instances (audit kind per `glossary/work-unit.md` Cross-archetype illustration); cross-archetype shape consistent — auditor archetype shares atomic-defensible-assertion shape with planner archetype per `glossary/claim.md`
- Verdict: covered (cross-archetype shape consistent per `glossary/claim.md` validates SD-4 cross-archetype generalization)

**Cluster D Validators** — `profiles/G-composability-gate.md` (cross-cutting validation gate; Cluster D member; transitively-satisfied via specialist's packaging boundary + workspace-scope managed entities):
- G lines 14-22 multi-mode consumption framing: validates SD-2 Framework C distributable property + SD-1 cross-cutting integrator template-class anchor + SD-3 workspace integration (workspace serialization format Phase 6 spec per `profiles/G-composability-gate.md` Backup / migration / cloning mode)
- G lines 154-157 cross-shape consumption rules: validates SD-5 §8 cross-shape policy variation matrix shape-policy-mediated rows (engagement-target catalog + workspace.md required fields + workspace-scope managed entity universals + Layer A scope configuration defaults + specialists_active recommended set + substrate selection constraints all shape-policy-mediated per `glossary/owner-b-scope.md` shape-policy-mandated rule)
- G lines 162-184 architectural concerns surfaced: backup-migration round-trip implicates W3 workspace identity persistence schema; cross-substrate composition rules implicate W2 cross-deployment claim portability scope-model variation
- Verdict: PASS (transitively-satisfied via specialist's packaging boundary + workspace-scope managed entities; G's L1-L4 producer artifact concerns satisfied at specialist DEFINITION level per `arch/specialist-skill.md` §11 + workspace level per scope-model SD-3)

**Cluster D Validators (gate component)** — D Defer Gate per `profiles/INDEX.md` "D Gate procedure":
- W1 multi-tenant federation scope-model variation: external-information test passes (specific signal = workspace federation surfaces per `arch/practitioner.md` W1); effort-asymmetry test passes (federated-Owner-B mechanism design before second-deployment friction risks wrong-design); D Gate satisfied → W1 watch-list with resolution mechanism
- W2 cross-deployment claim portability scope-model variation: external-information test passes (specific signal = first cross-deployment claim ingestion deployment evidence per `arch/claim-defensibility.md` W2); effort-asymmetry test passes (per-shape claim portability semantics design before first-deployment friction risks wrong-design); D Gate satisfied → W2 watch-list with resolution mechanism
- W3 workspace identity persistence schema: external-information test passes (specific signal = Phase 6 spec for workspace identity portability across substrate migration / backup-restore / re-activation per `glossary/deployment.md` "Multi-deployment-of-same-workspace patterns"); effort-asymmetry test passes (workspace identity invariants across deployments awaits Phase 6 audit-trail integrity verification + cryptographic signing); D Gate satisfied → W3 watch-list with resolution mechanism
- W4 engagement-target entity catalog per second-shape productization: external-information test passes (specific signal = second-shape design begins per BACKLOG shape-neutrality watch-list); effort-asymmetry test passes (per-shape engagement-target entity design before second-shape design begins risks wrong-design); D Gate satisfied → W4 watch-list with resolution mechanism
- Verdict: D Gate satisfied per genuine awaited evidence (W1 + W2 + W3 + W4)

### Decomposition mode

Per `decision-design-sharpening` v0.10.0 §Two decomposition modes Mode 2:
- **Trigger satisfied**: 6 sub-decisions visible at framing time (not emergent from drift); foundation-up dependencies identifiable (SD-1 template anchor enables SD-2-6 to inherit shape; SD-2 3-sub-section structure enables SD-3 workspace integration cross-scope composition; SD-3 enables SD-4 per-primitive composition narrative; SD-4 enables SD-5 §8 cross-shape policy variation matrix; SD-6 layers W1-W4 watch-list + cross-references on validated cross-cutting integrator articulation)
- **Sub-decision inventory at start**: 6 sub-decisions listed before Round 1 (SD-1 → SD-6); composite decomposition mode declared upfront
- **Foundation-up dependency ordering**: SD-1 (template-class anchor) locks first; SD-2 (per-scope structural overview) builds on SD-1; SD-3 (workspace integration) builds on SD-2 articulation; SD-4 (per-primitive composition narrative + 4 NEW patterns) builds on SD-2 + SD-3; SD-5 (cross-shape policy variation + cross-axis composition) builds on SD-2 + SD-4; SD-6 (W1-W4 watch-list + cross-references) layers on validated cross-cutting integrator articulation
- **Per-sub-decision sharpening**: each got Round 1 + Round 2 sweep within the composite (no per-sub-decision split into separate rounds)
- **Synthesis pass at end**: this DR + ARCH §18 composition table is the cross-sub-decision coherence pass
- **Single composite DR**: chosen per Mode 2 §Single composite DR — sub-decisions have no independent meaning outside the composite; scope-model is the unit, not 6 independent decisions

### Layered coverage observation

Per `decision-design-sharpening` §Layered coverage observation: each round emphasizes different architectural concern layer.

- **Round 1**: emphasized template + per-scope structural overview + workspace integration + per-primitive composition narrative + cross-shape policy variation + watch-list (architectural decisions per skill §Layered coverage Round 1 emphasis); 7 EXPANSIONS sub-decision-batched
- **Round 2**: emphasized cross-cutting (E1 boot integration + E4 cross-cutting non-placed pattern + E5 authority-binding placement) + schema details (E2 nested-bundle pattern explicit elevation + E3 content-unit-IN-instance pattern explicit elevation + E6 schema evolution forward-reference + E7 scope-categorization error categories forward-reference) — matches skill §Layered coverage Round 2 emphasis (cross-cutting + schema details)
- **No Round 3**: narrow architectural surface per skill §Empirical sweet-spot pattern (cross-cutting integrator narrower than primitive-cluster — only §8 conditional applies; §9/§10/§11/§13 N/A documented); operational concerns (per-scope identity-uniqueness rules + schema versioning semantics + scope-categorization error catalog + workspace identity persistence schema + cross-deployment claim portability semantics) belong to Phase 6 pre-implementation per skill §Phase 1 → Phase 2 transition

### Empirical density check

Per `decision-design-sharpening` §Empirical density check: count substantive findings (HIGH + MEDIUM impact; exclude cosmetic / NO-ACTION) for current round vs previous round.

- Round 1: 7 EXPANSIONS (sub-decision-batched: 1 per SD)
- Round 2: 7 EXPANSIONS (E1-E7)
- Density behavior: holds within ±25% — AMBIGUOUS region per density-behavior table; does NOT trigger CONTINUE candidate auto (Q3 holds/increases). Counter-bias check: Q4 (specific unaddressed pass) returns NONE; Q5 (specific termination signal) names cross-cutting integrator narrow surface. Manufactured-comfort counter-test passed (not declaring STABLE because round-fatigue; declaring per Q5 specific termination signal + Q4 no-unaddressed-pass).

ARCHITECTURAL-DECISION surface per skill §Surface-type declaration. ~7 EXPANSIONS Round 2 within sweet-spot. 0 architectural REVISIONS (E2 + E3 are REVISION-flavored EXPANSIONS not pure architectural reversal — surfacing implicit cross-cutting patterns from prior primitive-cluster locks as explicit; structural elevation of implicit-to-explicit per Note 58 R-CC-10 + Note 59 E4 pattern). STABLE LOCK.

### REVISION/EXPANSION classification self-check

Per `decision-design-sharpening` v0.6.0 self-check at Round 2 termination + BACKLOG watch-list "3-tier discriminator codification".

**REVISION-flavored EXPANSIONS surfaced** (load-bearing structural elevations):
- **E2** (nested-bundle pattern elevated from implicit-in-specialist-skill-cluster-lock to explicit cross-cutting structural commitment in scope-model articulation) — REVISION-flavored EXPANSION (structural elevation of implicit-to-explicit pattern; parallels `arch/practitioner.md` R-CC-1 boot ordering elevation + `arch/workflow-work-unit.md` R-CC-10 snapshot pattern elevation + `arch/claim-defensibility.md` E4 pre-existing-claim ingestion elevation)
- **E3** (content-unit-IN-instance pattern elevated from implicit-in-claim-defensibility-cluster-lock to explicit cross-cutting structural commitment in scope-model articulation) — REVISION-flavored EXPANSION (structural elevation of implicit-to-explicit pattern; parallels prior REVISION-flavored EXPANSIONS pattern)

**Cumulative count for awaited 3-tier signal**: 2 REVISION-flavored EXPANSIONS in this composite. Combined with `arch/specialist-skill.md` DR's 2 REVISION-flavored EXPANSIONS + `arch/practitioner.md` DR's 1 REVISION-flavored EXPANSION + `arch/workflow-work-unit.md` DR's 1 REVISION-flavored EXPANSION + `arch/claim-defensibility.md` DR's 1 REVISION-flavored EXPANSION = **7 cumulative cross-DR REVISION-flavored EXPANSIONS** across Phase 3.5 primitive-cluster + cross-cutting integrator decisions.

**Trip threshold for cumulative-count signal**: ≥3 trips per BACKLOG watch-list "3-tier REVISION/EXPANSION discriminator codification" entry. **Threshold continues** (7 ≥ 3 — increased from 5 at claim-defensibility DR per Note 59); **flag continues for Coherence-audit C2** at Phase 3.5 close to evaluate whether 3-tier codification is now warranted across primitive-cluster + cross-cutting integrator topic class. USER pushback / cascade-work-lag signals NOT yet materialized per skill detection mechanisms; continue 2-tier within current composite.

**Pure REVISIONS** (architectural pivots changing existing decisions): 0. E2 + E3 are EXPANSION-with-load-bearing-implications, not pure architectural reversals.

### Termination signal (STABLE-AT-ROUND-2)

Per `decision-design-sharpening` §Round termination signals + §Honest termination test Q1-Q5:

- **Q1 (count)**: Round 1 = 7 EXPANSIONS (sub-decision-batched: 1 per SD); Round 2 = 7 EXPANSIONS (E1-E7)
- **Q2 (decay)**: Round 1 → Round 2 = 7 → 7 (holds; AMBIGUOUS region per density-behavior table)
- **Q3 (density behavior)**: AMBIGUOUS per holds within ±25%; Round 2 surfaced cross-cutting + schema-detail refinements (per skill §Layered coverage observation Round 2 emphasis); no Round 3 architectural-pattern-surfacing pending; cross-cutting integrator narrow surface compensates for AMBIGUOUS-density (1 conditional applies vs 3+ for primitive-cluster topics)
- **Q4 (specific unaddressed pass)**: NONE — all 4 profile clusters covered (A + B + C + D); G Gate transitively-satisfied via specialist's packaging boundary + workspace-scope managed entities; D Gate fired (W1 + W2 + W3 + W4 satisfied); cross-cutting + schema details exhausted at decision-design-phase
- **Q5 (specific termination signal)**: NARROW ARCHITECTURAL SURFACE per `decision-design-sharpening` §Empirical sweet-spot pattern (cross-cutting integrator narrower than primitive-cluster — only §8 conditional applies vs 3 APPLIES for claim-defensibility / workflow-work-unit; matches narrower surface than `arch/practitioner.md` DR Note 57 termination signal); operational concerns (per-scope identity-uniqueness rules + schema versioning semantics + scope-categorization error catalog + workspace identity persistence schema + cross-deployment claim portability semantics + engagement-target catalog per second-shape productization) belong to Phase 6 pre-implementation per §Phase 1 → Phase 2 transition
- **Lock + persist signal**: STABLE per Q5 specific termination signal + Q4 no-unaddressed-pass + manufactured-comfort counter-test passed (not declaring STABLE because round-fatigue; declaring per Q5 narrow architectural surface + Q4 no unaddressed pass; AMBIGUOUS density compensated by Q5 surface narrowness)

## 7. Composition with existing architecture

This decision composes with prior locked architecture:

- **Pattern A protocols** (substrate / adapter; sparring + audit mechanism classes per Phase 3.4 close): scope-model composes with substrate Pattern A tri-aspect (Surface mechanism + Implementations Framework C + Implementation Instance Owner B per E5 substrate parallel; substrate Surface §F session/context for cross-deployment claim portability per W2; substrate-phase 1 boot integration per E1); with audit mechanism class Framework C Surface + Owner B audit-trail per E5 (per-shape audit emission granularity per §14 composes with §8 cross-shape policy variation); with sparring mechanism class Framework C Surface (8 sub-mechanism contracts) + Owner B sparring events per E5 (per-shape activation matrix per §4 framework-baseline-vs-shape-extension partition composes with §8 cross-shape policy variation); with adapter Pattern A tri-aspect Framework C + Owner B Instance bindings (framework-baseline-vs-shape-extension partition per §3 composes with §8 cross-shape policy variation).

- **Pattern B specialist-skill primitive cluster** (per `arch/specialist-skill.md` Phase 3.5 first primitive-cluster lock): specialist DEFINITION as Framework C bundle nesting skill / workflow / work-unit-kind / adapter Implementations per E2 nested-bundle pattern; specialist instance content as Owner B; specialist-namespace mechanic grounds cross-specialist composition rules (per `arch/specialist-skill.md` §10 + `glossary/specialist.md`).

- **Pattern C practitioner primitive cluster** (per `arch/practitioner.md` Phase 3.5 second primitive-cluster lock): bipartite Pattern C — HUMAN aspect cross-cutting NOT placed per E4 + RECORD aspect Owner B workspace-scope managed entity per `arch/practitioner.md` §2.2; per-shape policy variation per `arch/practitioner.md` §8 composes with scope-model §8 cross-shape policy variation matrix.

- **Two-Pattern-B workflow-work-unit primitive cluster** (per `arch/workflow-work-unit.md` Phase 3.5 third primitive-cluster lock): workflow + work-unit bipartite Pattern B — KIND DEFINITION nested in specialist's Framework C bundle per E2 + workflow_instance + work-unit instance Owner B per `arch/workflow-work-unit.md` SD-2.

- **PRIMITIVE+DERIVED claim-defensibility primitive cluster** (per `arch/claim-defensibility.md` Phase 3.5 fourth primitive-cluster lock): claim PRIMITIVE content-unit IN work-unit instance per E3 INHERITS work-unit's Owner B placement (cross-pattern destruction inheritance per `arch/claim-defensibility.md` §13); defensibility DERIVED property/test cross-cutting non-placed per E4; per-shape policy variation per `arch/claim-defensibility.md` §8 composes with scope-model §8 cross-shape policy variation matrix.

- **authority-binding mechanism** (per `glossary/authority-binding.md` from Phase 3.4 C1 cascade): mechanism Framework C definition + Owner B event recording dual-aspect per E5; per-event actor declaration sub-aspect grounds cross-axis composition + cross-deployment claim portability per W2.

- **`ARCHITECTURE.md` §6 composite boot subsection**: workspace boot integration realizes scope-categories in ordered sequence per E1 (Framework C selections → Owner B instances → Layer A scope-resolution INSIDE substrate-phase 1-5 envelope).

- **`MAINTENANCE.md` Layer 3 Primitive-cluster topic template** (locked per `arch/specialist-skill.md` DR + `MAINTENANCE.md` Layer 3 §3 Primitive-cluster topic template subsection): cross-cutting integrator topic-template-class anchored at this topic per per-pattern conditional applicability rules (cross-shape policy variation APPLIES; granularity / bundle / marketplace / per-element lifecycle ordering N/A documented per cross-cutting integrator definition). Future cross-cutting integrator topic — `arch/axis-interactions.md` Phase 3.5 sixth + final ARCH topic — inherits this DR's anchor for conditional applicability rules.

- **TOP-LEVEL ARCHITECTURE "Framework = mechanisms; Shape = policies"**: Framework C derives from `framework = mechanisms`; Owner B derives from `framework + shape → workspace deployment`; Layer A is orthogonal axis (independent classification axis for content layering by domain/state context). Three-scope structural articulation grounds in this foundational architectural commitment.

- **TOP-LEVEL ARCHITECTURE "A-B-C scope model"**: preliminary-locked three-scope classification is the architectural commitment scope-model articulates; per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3, A-B-C is preliminary-locked (revisable when concrete entity-md authoring exercises Phase 3+ reveal mismatches).

- **TOP-LEVEL ARCHITECTURE "Atoms vs containers"**: mechanism + policy atomic primitives; framework + shape META-PRIMITIVE containers — grounds §2.1 Framework C Member catalog (mechanism / shape / substrate / protocol-implementation / specialist DEFINITION) + §2.2 Owner B Member catalog distinction.

- **TOP-LEVEL DESIGN PRINCIPLES §1 (structural over conventional)**: scope-categorization gate-dispatched-structural via Pydantic validation on `framework_kind` + `owner_scope` + `layer_scope` (per per-scope identity convention); NOT prose-rule scope determination at deployment time.

- **TOP-LEVEL DESIGN PRINCIPLES §2 (pattern-vs-instance)**: scope-model primitives stay shape-neutral / archetype-neutral / pioneer-neutral; pioneer (PBS-Schulz) reality grounds the workspace-as-integration-point articulation without leaking pioneer specifics (Bauleitplanung / B-Plan-Begründung / UNB / Stellungnahme do NOT appear in scope-model definitions; cross-archetype illustration in §2 + §3 + §8 anchors framework neutrality per 6 archetypes per `glossary/workspace.md` Cross-archetype illustration line 30-37).

## 8. Constraints flowing to downstream commitments

- **Phase 3.5 final ARCH topic** (`arch/axis-interactions.md` Phase 3.5 sixth + final ARCH topic per `ARCHITECTURE.md` §5 reading order): inherits cross-cutting integrator 12+5 template per SD-1 + per-pattern conditional applicability pattern (document N/A explicitly per template rule; preserve §12 N/A-parity reservation); cross-cutting integrator topic-template-class anchored here serves as precedent for axis-interactions conditional applicability when Phase 3.5 sixth + final ARCH topic locks; closes Phase 3.5 sub-phase
- **Phase 3.6 `arch/quality-gate.md`**: consumes scope-model articulation for quality-gate Pattern A Framework C definition + Owner B observability source placement per E5 dual-aspect placement parallel
- **Coherence-audit C2 fires post-Phase-3.5 close** (per `disciplines/09-coherence-audit-cadence.md` cadence): primitive-cluster + cross-cutting integrator set audited at phase boundary; cross-primitive coherence verified across specialist-skill + practitioner + workflow-work-unit + claim-defensibility + scope-model + axis-interactions; cumulative REVISION-flavored count (7 across 5 cluster-executions; trip threshold reached) evaluated for 3-tier discriminator codification per BACKLOG watch-list
- **Phase 6 specs** (`docs/specs/scope-model.md` + `docs/specs/workspace.md`): per-scope identity-uniqueness rules + schema versioning semantics per E6 + scope-categorization error catalog per E7 + workspace identity persistence schema per W3; cross-link to `arch/specialist-skill.md` §11 specialist marketplace deferred per W1 + `arch/practitioner.md` §4 multi-practitioner manifest schema
- **Phase 6 deployment** (per `MAINTENANCE.md` TOP-LEVEL SCOPE: PBS-Schulz workspace deployment): per-deployment workspace.md authoring happens at deployment-instance via Mode 1 production-runtime LLM-MD; per-deployment workspace.scope configuration; per-deployment Layer A content assembly per workspace.scope.{domains, states} configuration
- **GLOSSARY cascade**: `glossary/framework-c-scope.md` + `glossary/owner-b-scope.md` + `glossary/layer-a-scope.md` + `glossary/workspace.md` See sections + Composes-with rows; ARCHITECTURE.md §7 NEW lock entry + §2 row 3.5 update + §3 doc structure status table update (8 of 11 → 9 of 11); peer ARCH §17/§19 reciprocal back-mentions: substrate + audit + adapter + sparring + specialist-skill + practitioner + workflow-work-unit + claim-defensibility; MAINTENANCE.md Layer 3 NEW cross-cutting integrator topic-template-class ANCHOR codification subsection + per-topic count expectation row update; BACKLOG.md cascade
- **BACKLOG.md cascade**: W1 (multi-tenant federation scope-model variation) → Phase 5+ cross-link to `arch/practitioner.md` §14 W1; W2 (cross-deployment claim portability scope-model variation) → Phase 5+ cross-link to `arch/claim-defensibility.md` §14 W2 + `arch/substrate.md` §F; W3 (workspace identity persistence schema) → Phase 6 spec territory; W4 (engagement-target entity catalog per second-shape productization) → Phase 3.5+ cross-link to BACKLOG "Shape-neutrality validation for second-shape productization" entry

## 9. Files touched

- `arch/scope-model.md` — cross-cutting integrator 12+5 ARCH topic (cross-cutting integrator topic-template-class anchor)
- `docs/decisions/scope-model-arch-topic.md` — this composite DR

Cascade scope:

- `glossary/framework-c-scope.md` — See section anchored to `arch/scope-model.md`
- `glossary/owner-b-scope.md` — See section anchored; engagement-target shape-policy-mandated rule cross-reference
- `glossary/layer-a-scope.md` — See section anchored
- `glossary/workspace.md` — See section + Composes-with rows updated (workspace IS the binding-instance entity at Owner B)
- `glossary/deployment.md` — See section reciprocal mention (1:1 reciprocal cardinality with workspace)
- `glossary/authority-binding.md` — See section back-link to scope-model §4 E5 authority-binding placement pattern
- `arch/substrate.md` §19 — added `arch/scope-model.md` reference (Pattern A tri-aspect Framework C + Owner B Implementation Instance; substrate-phase 1 boot integration)
- `arch/audit.md` §19 — added `arch/scope-model.md` reference (mechanism class Framework C Surface + Owner B audit-trail)
- `arch/adapter.md` §19 — added `arch/scope-model.md` reference (Pattern A tri-aspect Framework C + Owner B Instance bindings)
- `arch/sparring.md` §19 — added `arch/scope-model.md` reference (mechanism class Framework C Surface + Owner B sparring events)
- `arch/specialist-skill.md` §17 — forward-reference upgraded to backward-reference (specialist DEFINITION as Framework C bundle nesting per E2)
- `arch/practitioner.md` §17 — forward-reference upgraded to backward-reference (Pattern C HUMAN cross-cutting NOT placed per E4 + RECORD Owner B)
- `arch/workflow-work-unit.md` §17 — forward-reference upgraded to backward-reference (KIND DEFINITION nested in specialist's Framework C bundle per E2)
- `arch/claim-defensibility.md` §17 — forward-reference upgraded to backward-reference (claim content-unit IN work-unit per E3; defensibility cross-cutting non-placed per E4)
- `ARCHITECTURE.md` §7 — lock entry "Scope model ARCH topic (Phase 3.5 first cross-cutting integrator) — LOCKED"; §2 row 3.5 update; §3 doc structure status table update (8 of 11 → 9 of 11 drafted); §4 Topic catalog row 10 status update
- `MAINTENANCE.md` Layer 3 — new cross-cutting integrator topic-template-class subsection (12+5 inherits primitive-cluster template WITHOUT variation; cross-shape policy variation APPLIES; granularity / bundle / marketplace / per-element lifecycle ordering N/A documented)
- `BACKLOG.md` — Phase 3.5 row resolution; Phase 5+ ROADMAP + Phase 6 watch-list entries for W1-W4

Initial commit `c209182`; cascade commit `0e2876a`; cleanup commits per git log.

## 10. Revisit triggers

- **W1 signal arrives** (workspace federation surfaces per `arch/practitioner.md` W1 multi-tenant federation practitioner identity binding): multi-tenant federation scope-model variation design fires; SD-2 Owner B amendment for federated-Owner-B mechanism; integrates with `arch/practitioner.md` §14 W1
- **W2 signal arrives** (first cross-deployment claim ingestion deployment evidence per `arch/claim-defensibility.md` W2 + `arch/substrate.md` §F): cross-deployment claim portability scope-model variation design fires; SD-5 §8 amendment for per-shape claim portability semantics; integrates with `arch/claim-defensibility.md` §14 W2 + `arch/substrate.md` §F
- **W3 signal arrives** (Phase 6 spec for workspace identity portability across substrate migration / backup-restore / re-activation): workspace identity persistence schema design fires; integrates with `arch/audit.md` §D integrity verification + `arch/practitioner.md` W3 cryptographic signing + `arch/claim-defensibility.md` W4 cryptographic signing per claim
- **W4 signal arrives** (second-shape design begins per BACKLOG shape-neutrality watch-list — autonomous-business OR personal-OS productization): engagement-target entity catalog per second-shape design fires; SD-2 Owner B amendment for shape-policy-mandated engagement-target entity (Customer / Funder / etc.); SD-5 §8 cross-shape policy variation matrix amendment for second-shape engagement-target row
- **axis-interactions topic creation signal** (Phase 3.5 sixth + final ARCH topic; `arch/axis-interactions.md`): validates cross-cutting integrator 12+5 template extension per SD-1; if cross-cutting-integrator-specific 6th conditional candidate surfaces, MAINTENANCE.md Layer 3 amendment per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern
- **Quality-gate full design signal** (Phase 3.6 quality-gate full design surfaces signal-catalog concerns): quality-gate Pattern A Framework C definition + Owner B observability source placement per E5 dual-aspect placement parallel; SD-4 §4 composition table quality-gate row amendment
- **Phase 6 specs surface field-shape concerns** (per-scope identity-uniqueness rules + schema versioning semantics + scope-categorization error catalog): SD-1 conditional applicability amendment if Phase 6 spec surfaces operational concerns warranting ARCH-level architectural elevation (~10-20% Phase 1 → Phase 2 architectural flow-back per `decision-design-sharpening` §Phase 1 → Phase 2 transition)
- **Pioneer-deployment data shows scope-categorization gaps** (concrete deployment evidence surfaces scope-classification edge cases): SD-2 Owner B + Layer A amendments for deployment-evidence-driven scope-categorization refinements
- **Coherence-audit C2 fires post-Phase-3.5 close** (per `disciplines/09-coherence-audit-cadence.md` cadence): primitive-cluster + cross-cutting integrator set audited at phase boundary; cross-primitive coherence verified across specialist-skill + practitioner + workflow-work-unit + claim-defensibility + scope-model + axis-interactions; cumulative REVISION-flavored count (7 across 5 cluster-executions; trip threshold reached) evaluated for 3-tier discriminator codification per BACKLOG watch-list
- **Future cross-cutting integrator topic creation** (axis-interactions Phase 3.5 sixth + final ARCH topic; future cross-cutting integrator topics): validates 12+5 template extension per SD-1; if cross-cutting-integrator-specific 6th conditional candidate surfaces, MAINTENANCE.md Layer 3 §3 amendment per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern
