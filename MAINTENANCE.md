# Doc system maintenance

This is the meta-doc that defines how the pbs-bureau corpus is organized and how it stays consistent. **Read at session start alongside `VISION.md` and `HANDOFF.md`.**

Two motivating concerns drove the doc system design: **cognitive-load reduction** (layered structure makes the right depth for any question obvious; reading scope is bounded per question) + **consistency across docs** (explicit cascade discipline prevents internal contradictions: shape claims, vocabulary drift, restructure-not-cascaded).

---

## TOP-LEVEL RULE — Cascade discipline

**The doc system must stay in a consistent state. When you change any concept, decision, primitive, or term in any doc, identify every other place it appears and update each in the same commit (or a tightly-coupled sequence of commits explicitly marked as completing the cascade).**

### Direction of cascade

Changes propagate **DOWN** (foundation change → dependent layers: GLOSSARY term redefined → Layer 3-5 mentions; VISION axis refined → ARCH + Layer 3; ARCH adds primitive → Layer 3 topic + Layer 5 spec + Layer 4 DR), **UP** (load-bearing deeper-layer detail → overview update: Layer 4 DR shifts placement rule → Layer 3 topic + ARCH reference card), and **SIDEWAYS** (peer docs sharing a concept boundary co-update: e.g., `framework.md` + `shape.md` both describe the framework-vs-shape boundary).

### Bidirectional cascade with GLOSSARY

GLOSSARY (Layer 1) has a special bidirectional relationship beyond UP/DOWN/SIDEWAYS:

- **UPSTREAM**: GLOSSARY change propagates to ARCH / DRs / specs (covered above)
- **DOWNSTREAM** (often missed): ARCH/DR/spec work surfaces a **glossary-grade** structural fact (always-present / optional / bipartite / cross-cutting; reciprocal symmetry between primitives; vocabulary distinction load-bearing across entries; cross-axis interaction not currently captured) → must retro-fit GLOSSARY before locking the ARCH/DR/spec commit. (Schema details / per-impl mechanics / operational procedures / per-shape variations are NOT glossary-grade — they stay in ARCH/DR/spec.)

**Trigger points for back-check**: end of Round 2 sharpening; ARCH topic completion before commit; DR drafting before lock; coherence-audit corpus-set passes (Lens 1 + Lens 8 + Lens 9).

### How to find cascades

Before committing any non-trivial doc change: (1) **grep the affected concept name** across all docs (`git grep <term>`) — every hit is a candidate target; (2) **review each hit** — if the change shifts its meaning, update; otherwise verify-consistent in commit message; (3) **cross-check the layer above and below** for required overview / topic updates; (4) **GLOSSARY back-check** — does this work surface a glossary-grade structural fact / reciprocal symmetry / vocabulary distinction needing retro-fit?; (5) when uncertain, surface the cascade question rather than committing partial cascade.

### Anti-patterns cascade prevents

Contradictory claims across docs (DR-A "framework is shape-neutral" + DR-B "framework enforces axis 3 on all shapes"); stale references (DR references old path after restructure); vocabulary drift ("office" vs "workspace"); decisions without overview reflection (Layer 4 DR captures decision; Layer 2 ARCH reference card not updated).

---

## TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies

The framework provides **MECHANISMS** — universal interface contracts that any workspace shape can use; no shape-specific values. Shapes provide **POLICIES** over mechanisms — each shape configures which mechanisms are active, which are mandatory, which defaults apply.

This means:

- **Framework-level**: what's POSSIBLE (interface contracts; capabilities; primitives)
- **Shape-level**: what's MANDATED for a workspace archetype (policies; defaults; required-vs-optional)
- **Cross-cutting**: workspace, practitioner, session, workflow (orthogonal to mechanism/policy split)

### Atoms vs containers

- **mechanism** = atom (single interface contract; capability with defined input/output surface); **framework** = container (shape-neutral universal layer; collection of mechanisms + protocols + architectural disciplines)
- **policy** = atom (single configured value; requirement/default/constraint); **shape** = container (policy-bundle archetype for a workspace archetype)

### A-B-C scope model

Three placement categories. Framework C + Owner B are **derived** from framework/shape; Layer A is **orthogonal** (independent axis for content layering by deployment context).

- **Framework C** (derived from `framework = mechanisms`) — home for DEFINITIONS (mechanism / shape / substrate / protocol-implementation / specialist DEFINITIONS); universal, immutable, distributable
- **Owner B** (derived from `framework + shape → workspace deployment`) — home for INSTANCES (workspace, workspace-scope managed entities including practitioner-record + Actor + Client, specialist instance content, work-unit-kind instances); deployment-specific
- **Layer A** (orthogonal classification by content scoping) — home for LAYERED CONTENT (universal / domain-keyed / state-keyed content: references, doctypes, bausteine, prose conventions); varies by deployment context

A-B-C is **preliminary-locked** — revisable when concrete entity-md authoring exercises (Phase 3+) reveal mismatches.

Reading any entity-md instance, two orthogonal questions answer independently: (1) DEFINITION (Framework C) / INSTANCE (Owner B) / LAYERED CONTENT (Layer A)? (2) Which scope-key (universal / domain / state / specialist-id / workspace / etc.)? A reference can be universal-Layer-A; an entity-instance can be workspace-scope-Owner-B; a definition can be Framework C regardless of layer.

### Concept-by-concept (worked examples)

| Concept | Framework-level (mechanism) | Practitioner-shape (policy) |
|---|---|---|
| Audit emission | AuditEvent schema; `actor_kind` declared on every event; Pydantic gate dispatches every write | Audit granularity = claim-level; emission required for every output |
| Specialist modification | Specialist definition loaded; Pydantic schema declares conformity surface; modifications re-validate | Modifications require explicit re-conformance event |
| Authority binding | `actor_kind` enum includes `human`; AuditEvent records emitting actor | Human authority required in accountability-bearing output chain |
| Sparring | Sparring Protocol exists as runtime mechanism | Always-on; runtime pillar; output blocked until sparring fires |
| EU AI Act | (nothing) | (nothing — lives in eu-ai-compliance specialist) |
| Long-running work-units | (nothing — workspace + specialist suffice) | Practitioner-shape may activate a "project" specialist; legal-practice may activate "matter"; work-unit kind is specialist-defined |

### Recurring patterns: Protocol pluggability (the Protocol pattern)

Some framework primitives recur with a structural shape: **Surface + Implementations + Instance/binding** — the **Protocol pattern** (tri-aspect):

1. **Surface** (mechanism; framework-level): abstract Protocol contract defining the interface
2. **Implementations** (Framework C definitions; distributable): concrete realizations of the surface
3. **Instance/binding** (Owner B; workspace-level): the running implementation a workspace selected/bound

Known instances (preliminary-locked; more may surface): **substrate** (Substrate Protocol surface + Claude Agent SDK / MS Agent Framework + workspace's running substrate per `workspace.md`); **adapter** (Adapter Protocol surfaces per integration class + concrete adapters like gmail-adapter / lexware-adapter / MCP-based adapters + workspace's active adapters; distinct from substrate along internal-vs-external axis); **protocol** (architectural meta-concept: Coordination/Audit/Sparring/Trust/Time Protocol surfaces + their concrete implementations + per-shape-policy or per-workspace selection).

**Naming**: "Protocol pattern" with explicit disambiguation from **Pydantic Protocol** (Python typing concept; `typing.Protocol`). The architectural Protocol pattern is broader — describes pluggable-subsystem structure regardless of implementation technique.

### Other multi-aspect primitives (NOT Protocol pattern)

Some primitives are **multi-aspect** (manifest at multiple scopes) but do NOT follow the Protocol pattern. The COUNT of aspects varies:

| Pattern | Primitives | Aspects |
|---|---|---|
| **A** (Protocol pattern; tri-aspect) | substrate, adapter, protocol | Surface + Implementations + Instance/binding (3 across mechanism / Framework C / Owner B) |
| **B** (bipartite — definition + instance-content) | specialist | DEFINITION (Framework C; distributable bundle) + INSTANCE-CONTENT (Owner B; entities owned within deployed specialist). NO multiple implementations: a specialist IS its definition. |
| **C** (bipartite of different shape) | practitioner | HUMAN (cross-cutting; the actual person; not "placed") + RECORD (Owner B; system representation) |

The Layer tag value `multi-aspect` covers all multi-scope primitives regardless of count. Each entry's body specifies the count + which aspects + which scopes. Only Pattern A is generalized as a recurring named pattern; don't conflate B / C with A.

### Glossary entry classification

Each GLOSSARY entry tags itself with:

- **Class**: PRIMITIVE (atomic) / META-PRIMITIVE (container) / DERIVED (composition) / SCOPE-CLASSIFICATION
- **Layer**: framework-mechanism / shape-policy / cross-cutting / multi-aspect
- **Axis**: axis-1 / axis-2 / axis-3 / cross-axis (where applicable)
- **VISION usage**: directly used in VISION / implicit / derived-from-VISION-terms / framework-meta

(Tags are a means, not an end. If an entry is clearer with fewer tags, drop the extras.)

---

## TOP-LEVEL DESIGN PRINCIPLES — META-design rules applied universally to all primitive design

Three universal META-design principles fire at every architectural decision moment. They apply to ALL primitives and decisions; not specific to current architecture. Codified at TOP-LEVEL because they govern HOW we design rather than WHAT specific architecture lives in the framework.

### 1. Make wrong shapes impossible, not solvable

Prefer **structural constraints** (Pydantic, type system, gate enforcement, namespace separation) that make wrong shapes impossible by construction over **conventional solutions** that make wrong shapes solvable at deployment time. Convention-driven solutions for framework correctness offload work to deployment time, produce inconsistent shapes across clients, and accumulate deferred conflicts; structural constraints solve it once for everyone.

**The discriminator**:

| Concern touched by | Layer | Mechanism |
|---|---|---|
| Gate / Pydantic / dispatch code on every read/write | **Structural** — impossible by construction | Type system, Pydantic validators, gate enforcement, namespace separation |
| AI at mint-time / decision-time / reasoning-time (governance check, naming, archival policy) | **Prose convention** with audit trail | Prose rule in `office-config.md` / `department.md` / conventions.md; AI applies; AuditEvent records `convention_applied: {file, section, git_sha}` |

If the gate dispatches on it every read/write → structural. If AI applies at mint-time / judgment-time → prose convention is correct (impossibility-by-construction would be SQL-DB-trap rigidity per AI-as-runtime principle in `ARCHITECTURE.md` cross-cutting principles).

**How to apply**: force the question — "Does the gate / Pydantic / dispatch code touch this on every read/write?" If yes → MUST be structural; "deployment documents the rule and AI/audit validates" is the offloading anti-pattern. If no (AI applies at judgment-time) → prose convention with audit is correct.

### 2. Pattern-vs-instance — never defer; mental-modeling resolves now

**Never defer.** PBS is the framework foundation for the consulting business, validated by the planning bureau — NOT a planning-bureau product. At every architectural step, do the full scalable foundational work; designed for any expert-practitioner deployment, not minimum-viable-PBS.

**The no-defer rule**: if a decision cannot be made today because external information genuinely doesn't exist, surface as a **watch-list entry** naming the specific external signal awaited. Watch-list entries have resolution mechanisms (signal arrives → decision made by mechanism Y). "Defer" is removed from architectural vocabulary because it lacks a resolution mechanism and accumulates passively.

**Two tests for "literally cannot decide today"** (both must pass):

1. **External-information test**: Is there a SPECIFIC external signal whose absence prevents the decision? Name it precisely (Phase 1 corpus deployment data; first-bind real workflow performance; regulatory ruling X; community-built shape extension). Generic "we don't know yet" / "haven't done it yet" / "downstream isn't locked" — fail the test.
2. **Effort-asymmetry test**: Could we do the design work today if we chose to? If yes — even if the design might be wrong — NOT a chronological gap. Wrong design today is cheaper to revise (per Preliminary-lock §3) than missing design accumulating downstream cost.

**Watch-list entry format**: `**W<N>: <Concrete decision currently un-makeable>** — awaiting **<specific external signal>**. Resolution: when signal arrives, decision X made by mechanism Y.`

**Invalid defer reasons** (look like chronological-defer; aren't): "We haven't done the design work yet" / "Premature abstraction" / "YAGNI" / "PBS doesn't need it yet" / "Downstream isn't locked" / "Already-implemented parts work as-is" / "Speculation about future X" — all rejected. Honest watch-list framing names a SPECIFIC EXTERNAL EVENT; defer-instinct cites a CATEGORY of caution.

**D Gate** (procedural enforcement; per `profiles/INDEX.md`): fires whenever AI considers deferring; blocks until mental modeling within profile grounding attempted. Procedure: identify item considered for defer → attempt mental modeling within profile grounding (multi-axis validation across L1-L9 profiles + G consumer gate) → construct hypothetical scenarios within profile constraints → check whether primitive's classification holds → defer ONLY IF mental modeling genuinely cannot resolve. If it resolves → evolve answer NOW.

**Pattern-vs-instance discipline (broader)**: framework primitives stay shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer-instance specifics (Bauleitplanung; B-Plan-Begründung; UNB; DACH-EU regulatory specifics) live at workspace level (per practitioner-shape policy mandates), NOT in framework primitive definitions.

### 3. Preliminary-lock — every decision revisable except VISION axes

Every architectural decision in pbs-bureau is **PRELIMINARY-LOCKED**. "Locked" in HANDOFF / DRs / ARCH means current best position from available reasoning — NOT permanent. Decisions are revisable when VISION ideal design demands it. False stability anchors against re-examination; defer-instinct uses "locked" as polite excuse to compound around wrong locks ("we already decided X, so we work around it"). PBS is in deep design + exploratory phase; specs / DRs / ARCH / code are all living drafts.

**Preliminary-lock test** (run when prior decision is treated as constraint on current work):
1. Is the decision the IDEAL design per VISION lens, or past compromise / up-front-cost defer / scope limitation?
2. Has subsequent reasoning surfaced reasons to revise?
3. Would treating as fixed produce a worse outcome than re-examining?

If any answer suggests revision → re-examine. The cost of revising a preliminary-lock now is much smaller than the cost of compounding around a wrong lock.

**Vocabulary discipline**: "Locked" = preliminary-locked (current best position); "Anchored" = VISION axes only (high-bar revision via real-world falsification); "Settled" = avoid (suggests false permanence); "Decided" = preliminary-decided (revisable).

**What's anchored, NOT preliminary**: VISION axes (revise only on real-world falsification per VISION's own criteria; extremely high bar) + memory feedback principles + user-stated working-style preferences (user-codified explicitly; user revises directly).

**Composition with no-defer**: the two compose. Never defer NEW decisions, AND prior locks aren't excuses to defer revision. A "permanently-locked" decision used to block re-examination is just a defer of revision.

---

## TOP-LEVEL SCOPE — Repo identity: framework source, not deployment instance

This repo is **the framework + dev tooling source — the starting point for deployments**, NOT a deployment instance itself.

**What lives here**: framework architecture + foundational vocabulary (VISION, GLOSSARY, MAINTENANCE, DISCIPLINES, ARCHITECTURE, DRs, specs); **dev skills only** in `plugin/skills/` (sharpening / framing / audit — pattern-level dev-process tooling; NOT domain-specific); plugin manifest scaffolding for distribution; memory feedback files (cross-session AI behavior).

**What does NOT live here**: **app skills** (domain-specific workflow logic — drafting, review, validation, domain orchestration; these belong in deployment instances built from this framework); workspace instances (`workspace.md`, practitioner records, project state); Layer A content for any specific domain/state (PBS extensions, doctype manifests, baustein YAML); per-deployment configuration.

**Why this matters**: distribution clarity (anyone can clone as clean starting point without inheriting another deployment's instance state); pattern-vs-instance discipline applied to repo structure (framework = pattern; PBS-Schulz = pioneer instance — the repo embodying both was an earlier conflation the rebuild corrects); rebuild-bias prevention (app skills encode prior-vocabulary; restoring them mid-rebuild contaminates locked-architecture work).

**Cascade implication**: archived app skills (`archive/plugin/skills/`) stay archived **permanently** in this repo's history. Phase 6 builds them into a separate deployment workspace (PBS-Schulz instance), not back here. Future tooling decisions test against: "is this dev tooling for working ON the framework, OR app/domain logic for a deployment?" — only the former lives here.

---

## The 5-layer model

| Layer | What lives there | Where | Reading scope at session start | Line budget per doc |
|---|---|---|---|---|
| **0 — Entry** | README + HANDOFF + MAINTENANCE (this file) + DISCIPLINES + BACKLOG | Top-level | **Always read** | ~100 / lean log / ~150 / ~150 / ~300 |
| **1 — Foundations** | VISION + GLOSSARY | Top-level | **Always read** | ~1000 / ~500 |
| **2 — Overview** | ARCHITECTURE + ROADMAP + STRATEGY | Top-level | Read on substantive sessions | ~500 each |
| **3 — Architecture detail** (topical) | `docs/architecture/<topic>.md` | per primitive / discipline / cross-cutting concern | Read when working in that area | ~500 each, 15-20 topics total |
| **4 — Decision records** | `docs/decisions/<decision>.md` | narrow single-decision capture | Read when re-examining specific decision | ~150-300 each, ≤15-25 total |
| **5 — Specs** | `docs/specs/<spec>.md` | schemas, file formats, code conventions | Read when implementing against contract | ~500 each, ~5-8 specs |

**Memory** (orthogonal, not layered): `memory/` — feedback files + bausteine + universal prose. Persistent state, not architecture.

**Drafts** (orthogonal, not layered): `drafts/` — exploratory thinking / future-candidates / brainstorm output. **NOT locked, NOT load-bearing.** Drafts can graduate to locked docs (STRATEGY / VISION / GLOSSARY / ARCH) when matured + user-locked, OR be discarded. Don't cascade-pass against drafts. Discipline + format detail in `drafts/README.md`.

**Active reading at session start**: Layer 0 + Layer 1 ≈ ~2.2k lines. Constant per session, not proportional to corpus size.

### Layer 0 — Entry

- **README.md** — one-screen project description; what PBS is; pointers to Layer 1
- **HANDOFF.md** — lean session log; ~30-100 lines per session; rotate older sessions to `archive/handoffs/HANDOFF-sessions-N-M.md` when active HANDOFF crosses ~500 lines (keep current session + last 2 entries active)
- **MAINTENANCE.md** — this file; doc system rules
- **DISCIPLINES.md** — cross-session working discipline; how we operate
- **BACKLOG.md** — Phase-tagged work-item tracker

### Layer 1 — Foundations (anchored; rarely change)

- **VISION.md** — three-axis thesis + framework's structural primitives + foundations + falsification criteria. **Anchored**; revise only on real-world falsification. Pure stance — no tooling/methodology, no positioning, no architectural detail, no provenance.
- **GLOSSARY.md** — canonical vocabulary. **ONE home for every term definition.** Each entry: one-sentence canonical definition + non-examples + cross-archetype examples + boundary tests + cross-references to Layer 3 topic. Layer 3+ docs cite GLOSSARY rather than redefining terms.

**Cross-doc territory rule**: framework breadth (which shapes supported + how framework structurally encodes value claims) = ARCH; positioning narrowness (target users / competitive landscape / funding fit / per-shape market positioning) = STRATEGY; pure stance (what framework IS + axes it protects) = VISION; foundational vocabulary = GLOSSARY. Route by territory rule before lock.

### Layer 2 — Overview

- **ARCHITECTURE.md** — structural primitives (1-line each) + design disciplines (1-line each) + reference card + pointers to Layer 3 topics. **Cannot describe mechanisms in detail** — Layer 3 territory.
- **ROADMAP.md** — commitments + horizons; lean
- **STRATEGY.md** — market positioning + competitive landscape + funding + ICP. Architectural-adjacent.

### Layer 3 — Architecture detail (topical)

`arch/<topic>.md` — one file per major architectural concern (kebab-case slug; flat directory; no prefixes).

**Single abstraction level per file**: structural mechanisms for primitives; decisional reasoning for disciplines.

#### Pattern A protocol topic template (LOCKED; revised per `docs/decisions/greenfield-rederivation-pause.md` Step 4 + `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`)

For ARCH topics describing Pattern A protocols (Surface + Implementations + Selection per `protocol (architectural)` GLOSSARY entry), use this two-tier template:
- **12 common-required sections** apply to every Pattern A topic
- **7 protocol-specific-conditional sections** apply per protocol if applicable to its nature

Established by `arch/substrate.md` (anchor; 6 of 7 conditional sections apply, §14 N/A per shape-uniform Surface) + validated by `arch/adapter.md` (some conditional sections thin or N/A; §14 applies per shape-policy-mediated nature) + greenfield-tested against quality-gate at template-derivation time.

**12 common-required sections** (every Pattern A topic):

| § | Section | Purpose |
|---|---|---|
| 1 | Topic scope + frontmatter | Topic identity; Pattern classification; cardinality; cross-axis claim; composition with framework primitives |
| 2 | Surface contract (architectural-level) | Capability categories; per-class Surfaces if multi-class (two-layer Surface variant); explicit "NOT in Surface" exclusions; logic placement mode (Mode 4 here + Mode 3 spec at Phase 6) |
| 4 | Per-implementation aspect | Pattern level + current Implementation set + per-impl extension Protocols pattern |
| 5 | Selection mechanics | workspace.md selection field OR shape-policy selection; cardinality; validation at boot; re-binding semantics |
| 6 | Tri-aspect reconciliation | Surface + Implementations + Running Instance; coupling-impossible-by-construction |
| 7 | Composition with framework primitives | Cross-references to all primitives this topic composes with |
| 9 | Cardinality + lifecycle | Creator / owner / destroyer; mutability; cross-session persistence |
| 15 | Pre-implementation operational concerns (Phase 6 forward reference) | Explicitly NOT-locked-at-ARCH-level operational details |
| 16 | Watch-list | Items awaiting external evidence; resolution mechanisms |
| 17 | Decision-design provenance | Archived sources; pattern-vs-instance discipline application |
| 18 | Phase routing | Architectural shape (locked here) vs Pydantic spec vs concrete impls (Phase 6) |
| 19 | Cross-references | GLOSSARY entries / disciplines / profiles validated / ARCH topics composing / Phase 6 spec target |

**7 protocol-specific-conditional sections** (apply per protocol if applicable to its nature; document N/A explicitly when section is omitted):

| § | Section | Applicability |
|---|---|---|
| 3 | Common-surface boundary criteria | Applies when protocol has multi-class Surface (e.g., adapter's per-integration-class Surfaces); skip if single-layer Surface |
| 8 | Substrate-internal vs skill-side audit emission | Substrate-specific (substrate registers MCP gate; other protocols emit skill-side only) |
| 10 | Boot + shutdown phase ordering (architectural-level) | Substrate-specific lifecycle (per-instance ordering; flush-before-release invariants); other protocols document lifecycle in §9 cardinality + lifecycle without separate phase ordering |
| 11 | Substrate error categories (architectural-level) | Per-protocol error semantics differ; document per-protocol error categories when load-bearing distinct from §9 lifecycle treatment |
| 12 | Transport variation + per-tier mapping | Substrate-specific (MCP transport variation); skip when no multi-transport surface |
| 13 | Deployment-tier awareness | Substrate-specific (Tier 1/2/3 per-tier behavior in impl, not Surface); skip when protocol is tier-uniform |
| 14 | Cross-shape policy variation | Applies when protocol behavior is shape-policy-mediated (audit emission per shape; permission flow per shape; error escalation per shape; or other axes where shape policy bundle declares per-shape variation); document N/A explicitly when behavior is shape-uniform |

**Per-protocol section count expectation**:
- substrate: 12 common + 7 conditional (anchor; 6 of 7 apply; §14 N/A per shape-uniform substrate Surface) = ~18-19 total (depending on counting N/A documentation)
- adapter: 12 common + ~5 conditional (§3 per-integration-class boundaries, §10 lifecycle/auth-refresh, §11 per-impl errors, §14 cross-shape variation; §8 + §12 + §13 N/A) = ~17 total
- quality-gate: 12 common + ~3-4 conditional (§11 fail-closed / fail-open per shape, §14 cross-shape variation expected per shape-policy-mediated nature; others TBD per topic creation) = ~15-16 total

Future Pattern B / C / cross-cutting integrator topic templates locked when first instance lands (foundation-up; substrate established Pattern-A template via first-Pattern-A topic). Future Pattern A 8th-conditional candidates lock when first instance surfaces (per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern).

#### Provenance hygiene

ARCH topics hold **pure architectural content** — provenance lives in HANDOFF + git log + commit messages + DRs (Layer 4 Sharpening provenance section). No "Pattern note (meta)" / sharpening trajectory / procedural narrative in ARCH topics.

Each topic file: minimal frontmatter (title; topic-cluster; status: drafted/locked/forthcoming); H1 = de-kebab-cased slug.

### Layer 4 — Decision records

`docs/decisions/<decision>.md` — ONE narrow decision per DR (or composite DR for upfront-known decomposition per `decision-design-sharpening` v0.6.0 Mode-2 composite decomposition pattern).

#### DR template (LOCKED)

Sections in order:

1. **Status** — ACCEPTED / SUPERSEDED-BY-X; sharpening rounds metadata
2. **Owner** — Phase / commitment number / responsible work tracker
3. **Related** — Composes-with DRs / GLOSSARY entries / archived sources / disciplines applied
4. **Context** — what motivated the decision; what was missing; what the decision-design phase needed to resolve
5. **Decision** — what was locked; concrete shape (no prose narrative; structured per content's nature)
6. **Sharpening provenance** — **the meta-home for sharpening trajectory**:
   - Round-by-Round summary (Round 1 EXPANSIONS / Round 2 EXPANSIONS / Round 3 if applicable)
   - REVISIONS surfaced (if any)
   - Manufactured-criticism rejections (compact list)
   - GLOSSARY back-check verdict (what was considered; clean or retro-fit fired)
   - Profile-anchored validation (which clusters tested; which profile content cited; verdict per cluster)
   - Decomposition mode if applicable (Mode 1 emergent / Mode 2 upfront-known composite)
7. **Composition with existing architecture** — how this decision interacts with prior decisions
8. **Constraints flowing to downstream commitments** — per Phase / per file / per primitive impacts
9. **Files touched** (this DR's commit) — list of artifacts modified
10. **Revisit triggers** — specific external signals OR architectural events that warrant re-examination

If work decomposes into multiple decisions, write multiple DRs OR composite DR with explicit sub-decision sections — never Sub-DR A + Sub-DR B in same file unless Mode-2 composite decomposition applies.

Supersession via header notes when a DR is superseded by a later one.

**Sharpening provenance section IS the meta-home** (resolves where process narrative belongs per coherence-audit Lens 5: provenance in HANDOFF + git log + commit messages + DRs; NOT in ARCH topics or canonical content).

### Layer 5 — Specs

`docs/specs/<spec>.md` — implementation contracts.

Schema definitions, file format specs, code conventions, plugin authoring conventions, MCP tool conventions.

Versioned: semver if breaking; date if non-breaking.

---

## Cross-reference discipline (the navigability rule)

**Read references go DOWN the layers, not laterally**: Layer 0 → Layer 1 + 2 (entry pointers); Layer 2 → Layer 3 (overview points at topic detail); Layer 3 → Layer 4 + 5 (topic points at decisions + specs); Layer 4 → Layer 5 (decisions reference specs they implement).

**No lateral peer-references except within the same layer.** If two Layer 3 topics share a concept, it belongs in GLOSSARY (Layer 1 vocabulary) OR ARCHITECTURE (Layer 2 reference card) OR a third Layer 3 topic that both reference.

**No upward read-references.** Layer 4 doesn't reference Layer 3 (Layer 3 references Layer 4). Forces hierarchy clarity.

**Note distinction**: cross-references = READ direction (navigability); cascade discipline = WRITE direction (consistency when changing). When Layer 1 GLOSSARY changes, the change cascades DOWN to Layers 2-5 even though no Layer 1 doc references downward.

---

## Other maintenance disciplines

1. **Single abstraction level per doc.** If a Layer 2 doc starts describing mechanism details, split the detail to Layer 3. If a Layer 3 doc starts describing schemas, split the schema to Layer 5.
2. **Line budget as forcing function.** When a doc exceeds budget, decompose to next layer.
3. **One decision per DR** (Layer 4). If a decision splits, write multiple DRs.
4. **GLOSSARY is the single source for term definitions.** Layer 3+ docs may discuss structural detail about a primitive but cite GLOSSARY for canonical definition. If two docs define the same term, that's a cascade violation.
5. **Versioning per layer**: VISION + ARCHITECTURE versioned (semver-ish on architectural significance); DRs dated (no version; supersession via header note); Specs semver; Topics + GLOSSARY versioned only on breaking changes (date for non-breaking).
6. **Periodic prune.** At major version boundaries: which docs no longer earn their keep? Collapse to broader topic / archive. Don't let dead docs accumulate.

---

## When this doc itself changes

This doc is Layer 0 — it governs the doc system itself. Changes require especially careful cascade: (1) identify the structure/discipline being changed; (2) verify all docs currently following the prior rule still hold OR list which docs need updating; (3) update HANDOFF.md to flag the rule change.

---

## Composition

This doc holds TOP-LEVEL META-design principles (cascade / architecture / scope / design-principles / 5-layer model + templates). Operational disciplines (HOW we operate) live in `DISCIPLINES.md`. Memory feedback files in `memory/` hold cross-session AI behavioral preferences only (propose-before-commit / judgment-and-automate / push-after-commit / blocked-actions / plugin-marketplace-clone-sync).
