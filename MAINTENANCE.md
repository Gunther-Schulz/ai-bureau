# Doc system maintenance

This is the meta-doc that defines how the pbs-bureau corpus is organized and how it stays consistent. **Read at session start alongside `VISION.md` and `HANDOFF.md`.**

The doc system was designed in session 16 (2026-05-01) at start of the foundational rebuild. Two motivating concerns:

1. **Cognitive-load reduction** — the prior v0.35 corpus grew beyond easy handling (~10k+ lines of architectural docs); cursory reads produced pattern-matching failures in AI-assisted work. The layered structure makes the right depth for any question obvious; reading scope is bounded per question.
2. **Consistency across docs** — v0.35 contained internal contradictions (e.g., shape-neutrality + Option B floor; v0.34 location restructure not cascaded to shape-extension DR). These arose because cascade discipline was implicit. Making it explicit prevents recurrence.

---

## TOP-LEVEL RULE — Cascade discipline

**The doc system must stay in a consistent state. When you change any concept, decision, primitive, or term in any doc, identify every other place it appears and update each in the same commit (or a tightly-coupled sequence of commits explicitly marked as completing the cascade).**

### Direction of cascade

Changes propagate **down, up, and sideways** as needed:

- **DOWN** — changing a foundation propagates to dependent layers. Examples:
  - Glossary term redefined → every Layer 3 topic + Layer 4 DR + Layer 5 spec mentioning it must update
  - VISION axis refined → ARCH must update + Layer 3 topics referencing the axis must update
  - ARCH adds new primitive → Layer 3 topic file is created + Layer 5 spec defines schema + Layer 4 DR captures the decision

- **UP** — adding detail at a deeper layer can require overview update. Examples:
  - Layer 4 DR makes new decision touching architectural placement → Layer 3 topic updates + ARCH reference card updates if the decision shifts a placement rule
  - Layer 5 spec adds new schema field that's load-bearing → Layer 3 topic updates if the field affects the primitive's structural shape

- **SIDEWAYS** — peer docs at the same layer that share a concept boundary co-update. Examples:
  - Layer 3 `framework.md` and Layer 3 `shape.md` both describe the framework-vs-shape boundary; moving the boundary in one requires updating the other
  - Two DRs that compose architecturally (e.g., one adopts a Protocol pattern, another defines a specific Protocol implementation) update together when the pattern shifts

### Bidirectional cascade with GLOSSARY (UPSTREAM + DOWNSTREAM)

The UP / DOWN / SIDEWAYS direction above covers most cases, but the GLOSSARY layer (Layer 1 foundational vocabulary) has a special bidirectional relationship that warrants explicit attention:

- **UPSTREAM** (already covered above): GLOSSARY change → propagates to ARCH (Layer 2-3) + DRs (Layer 4) + specs (Layer 5)
- **DOWNSTREAM** (often missed): ARCH / DR / spec work surfaces a **glossary-grade** structural fact, named distinction, or vocabulary refinement → must retro-fit GLOSSARY before locking the ARCH/DR/spec commit

**What "glossary-grade" means** (decision rule for the back-check):
- Structural fact about a primitive's nature (always-present / optional / bipartite / cross-cutting / etc.)
- Reciprocal symmetry between two primitives (Lens 6 territory)
- Vocabulary distinction load-bearing across multiple entries
- Cross-axis interaction not currently captured

**What's NOT glossary-grade** (stays in ARCH/DR/spec):
- Schema details (field types, enum values)
- Per-implementation mechanics
- Operational procedures
- Per-shape-policy variations

**Trigger points for the back-check**:
- End of Round 2 sharpening (per `decision-design-sharpening` v0.5.0+ procedure)
- At ARCH topic completion before commit
- At DR drafting before lock
- During coherence-audit corpus-set passes (already covered by Lens 1 + Lens 8 + Lens 9)

**Canonical exemplar**: session 16 work-unit bipartite-classification surfaced "always-present container" (reciprocal to workflow's optional applicability) during Round 2 — glossary-grade structural fact that retro-fitted into work-unit + workflow GLOSSARY entries before lock. Without the back-check, it would have lived only in ARCH/DR and the GLOSSARY entries would silently have been incomplete.

### How to find cascades

Before committing any non-trivial doc change:

1. **Grep the affected concept name** across all docs (`git grep <term>`). Every hit is a candidate cascade target.
2. **Review each hit** — does the change shift this hit's meaning? If yes, update. If no, explicitly verify in commit message ("verified consistent: <hit>")
3. **Cross-check the layer above and below** — does the change require ARCH overview update (up) or Layer 3 topic update (down)?
4. **GLOSSARY back-check** (per Bidirectional cascade section above): does this work surface a glossary-grade structural fact / reciprocal symmetry / vocabulary distinction that should retro-fit into GLOSSARY?
5. **When uncertain**, surface the cascade question explicitly to the user during the change rather than committing partial cascade

### Anti-patterns (what cascade prevents)

- **Contradictory claims across docs** — e.g., DR-A says "framework is shape-neutral"; DR-B (added later, same author) says "framework enforces practitioner-shape axis 3 on all shapes." Cascade would have caught the contradiction at write-time.
- **Stale references** — e.g., a DR references `extensions/shapes/<id>/` (its original framing); a later restructure moves to `extensions/framework/shapes/<id>/`; the original DR is not updated. Cascade catches this.
- **Vocabulary drift** — e.g., one doc uses "office" while another uses "workspace"; sessions pass before the drift is noticed. Cascade catches at term-rename time.
- **Decisions without overview reflection** — Layer 4 DR captures decision, but Layer 2 ARCH overview's reference card or primitive list isn't updated. Reader of ARCH doesn't see the decision exists.

---

## TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies

The framework provides **MECHANISMS** — universal interface contracts that any workspace shape can use; no shape-specific values. Shapes provide **POLICIES** over mechanisms — each shape configures which mechanisms are active, which are mandatory, which defaults apply.

This means:

- **Framework-level**: what's POSSIBLE (interface contracts; capabilities; primitives)
- **Shape-level**: what's MANDATED for a workspace archetype (policies; defaults; required-vs-optional)
- **Cross-cutting**: workspace, practitioner, session, workflow (orthogonal to mechanism/policy split)

### Atoms vs containers

- **mechanism** is the atom — a single interface contract; capability with defined input/output surface
- **policy** is the atom — a single configured value; requirement/default/constraint
- **framework** is the container — the shape-neutral universal layer; collection of mechanisms + protocols + architectural disciplines
- **shape** is the container — the policy-bundle archetype for a workspace archetype

### A-B-C scope model

Three placement categories. Framework C + Owner B are **derived** from framework/shape; Layer A is **orthogonal** (an independent axis for content layering by deployment context, not derived from the mechanism/policy split).

- **Framework C scope** (derived from `framework = mechanisms`) — home for DEFINITIONS (mechanism / shape / substrate / protocol-implementation / specialist DEFINITIONS); universal, immutable, distributable
- **Owner B scope** (derived from `framework + shape → workspace deployment`) — home for INSTANCES (workspace, workspace-scope managed entities including practitioner-record + Actor + Client, specialist instance content, work-unit-kind instances); deployment-specific
- **Layer A scope** (orthogonal — independent classification by content scoping) — home for LAYERED CONTENT (universal / domain-keyed / state-keyed content: references, doctypes, bausteine, prose conventions); varies by deployment context

A-B-C is **preliminary-locked** — revisable when concrete entity-md authoring exercises (Phase 3+) reveal mismatches.

Reading any entity-md instance, two questions are answerable independently:
1. Is this a DEFINITION (Framework C) / INSTANCE (Owner B) / LAYERED CONTENT (Layer A)?
2. What scope-key applies (universal / domain / state / specialist-id / workspace / etc.)?

The two questions are orthogonal: a reference can be universal-Layer-A; an entity-instance can be workspace-scope-Owner-B; a definition can be Framework C regardless of layer.

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

Some framework primitives recur with a structural shape: **Surface + Implementations + Instance/binding** — the **Protocol pattern**. When this pattern manifests, the primitive has three aspects:

1. **Surface** (mechanism; framework-level): an abstract Protocol contract defining the interface
2. **Implementations** (Framework C definitions; distributable): concrete realizations of the surface
3. **Instance/binding** (Owner B; workspace-level): the running implementation a workspace selected/bound

Known instances (preliminary-locked; more may surface):

- **substrate** (locked) — Substrate Protocol surface + concrete substrates (Claude Agent SDK, MS Agent Framework) + workspace's running substrate per `workspace.md`
- **adapter** — Adapter Protocol surfaces per integration class + concrete adapters (e.g., gmail-adapter, lexware-adapter, MCP-protocol-based adapters) + workspace's active adapters; Pattern A primitive distinct from substrate along internal-vs-external axis (per locked GLOSSARY entry)
- **protocol** (architectural; canonical entry forthcoming) — the meta-concept: Coordination/Audit/Sparring/Trust/Time Protocol surfaces + their concrete implementations + per-shape-policy or per-workspace selection

**Naming**: "Protocol pattern" with explicit disambiguation from **Pydantic Protocol** (the Python typing concept; `typing.Protocol`). The architectural Protocol pattern is broader — it describes pluggable-subsystem structure regardless of implementation technique.

### Other multi-aspect primitives (NOT Protocol pattern)

Some primitives are **multi-aspect** (manifest at multiple scopes) but do NOT follow the Protocol pattern. The COUNT of aspects varies:

- **Pattern A primitives** (Protocol pattern; tri-aspect): substrate, adapter, protocol — Surface + Implementations + Instance/binding (3 aspects across mechanism / Framework C / Owner B)
- **specialist** (Pattern B; bipartite): DEFINITION (Framework C; distributable bundle) + INSTANCE-CONTENT (Owner B; entities owned within the deployed specialist) — 2 aspects. NO multiple implementations: a specialist IS its definition.
- **practitioner** (Pattern C; bipartite of different shape): HUMAN (cross-cutting; the actual person; not "placed") + RECORD (Owner B; system representation) — 2 aspects.

The Layer tag value `multi-aspect` covers all multi-scope primitives regardless of count. Each entry's body specifies the count + which aspects + which scopes.

Each has its own multi-aspect description in its GLOSSARY entry; only Pattern A is generalized as a recurring named pattern. Don't conflate B / C with A.

### Glossary entry classification

Each GLOSSARY entry tags itself with:

- **Class**: PRIMITIVE (atomic) / META-PRIMITIVE (container) / DERIVED (composition) / SCOPE-CLASSIFICATION
- **Layer**: framework-mechanism / shape-policy / cross-cutting / multi-aspect
- **Axis**: axis-1 / axis-2 / axis-3 / cross-axis (where applicable)
- **VISION usage**: directly used in VISION / implicit / derived-from-VISION-terms / framework-meta

Reading any GLOSSARY entry, the layered approach is structurally visible: foundational atom or derived? framework-territory or shape-territory? which axis does it serve? does VISION use the term?

(Tags are a means, not an end. If an entry is clearer with fewer tags, drop the extras.)

---

## TOP-LEVEL DESIGN PRINCIPLES — META-design rules applied universally to all primitive design

Three universal META-design principles fire at every architectural decision moment. They apply to ALL primitives and decisions; not specific to current architecture. Codified at TOP-LEVEL because they govern HOW we design rather than WHAT specific architecture lives in the framework.

### 1. Make wrong shapes impossible, not solvable

Prefer **structural constraints** (Pydantic, type system, gate enforcement, namespace separation) that make wrong shapes impossible by construction over **conventional solutions** that make wrong shapes solvable at deployment time.

**Why**: every "we'll document the convention; deployments handle correctness" answer is the framework offloading work to deployment time. Each consulting client hits the same problem; some solve inconsistently. Convention-driven solutions for framework correctness produce inconsistent shapes and deferred conflicts. Structural constraints solve it once for everyone.

**The discriminator**:

| Concern touched by | Layer | Mechanism |
|---|---|---|
| Gate / Pydantic / dispatch code on every read/write | **Structural** — impossible by construction | Type system, Pydantic validators, gate enforcement, namespace separation |
| AI at mint-time / decision-time / reasoning-time (governance check, naming, archival policy) | **Prose convention** with audit trail | Prose rule in `office-config.md` / `department.md` / conventions.md; AI applies; AuditEvent records `convention_applied: {file, section, git_sha}` |

If the gate dispatches on it every read/write → structural. If AI applies at mint-time / judgment-time → prose convention is correct (impossibility-by-construction would be SQL-DB-trap rigidity per AI-as-runtime principle in `ARCHITECTURE.md` cross-cutting principles).

**How to apply**: when proposing solution for framework-level correctness concern, force the question:
1. "Does the gate / Pydantic / dispatch code touch this concern on every read/write?" If yes → MUST be structural.
2. If yes to (1) and the proposed solution is "deployment documents the rule and AI/audit validates" → that's the offloading anti-pattern; design a structural constraint instead.
3. If the answer is no (AI applies at mint-time / judgment-time) → prose convention with audit is correct.

**Canonical exemplar**: session 11 Option C (convention-driven uniqueness for type names) rejected; Option B (department-namespaced types: `<scope-id>.<short-name>`) locked. Type names gate-dispatched on every read/write → structural required.

### 2. Pattern-vs-instance — never defer; mental-modeling resolves now

**Never defer.** PBS is the framework foundation for the consulting business, validated by the planning bureau — NOT a planning-bureau product. At every architectural step, do the full scalable foundational work; designed for any expert-practitioner deployment, not minimum-viable-PBS.

**The no-defer rule**: if a decision cannot be made today because external information genuinely doesn't exist, surface as a **watch-list entry** naming the specific external signal awaited. Watch-list entries have resolution mechanisms (signal arrives → decision made by mechanism Y). "Defer" is removed from architectural vocabulary because it lacks a resolution mechanism and accumulates passively.

**Two tests for "literally cannot decide today"** (both must pass):

1. **External-information test**: Is there a SPECIFIC external signal whose absence prevents the decision? Name it precisely (Phase 1 corpus deployment data; first-bind real workflow performance; regulatory ruling X; second-domain deployment feedback; community-built shape extension). Generic "we don't know yet" / "haven't done it yet" / "downstream isn't locked when we could lock it now" — fail the test.
2. **Effort-asymmetry test**: Could we do the design work today if we chose to? If yes — even if the design might be wrong — NOT a chronological gap. Wrong design today is cheaper to revise (per Preliminary-lock principle below) than missing design accumulating downstream cost.

**Watch-list entry format**: `**W<N>: <Concrete decision currently un-makeable>** — awaiting **<specific external signal>**. Resolution: when signal arrives, decision X made by mechanism Y.`

**Invalid defer reasons** (look like chronological-defer; aren't): "We haven't done the design work yet" / "It would take more sessions" / "Premature abstraction" / "YAGNI" / "PBS doesn't need it yet" / "Downstream consumer's shape isn't locked" / "Already-implemented parts work as-is" / "Speculation about future X" — all rejected.

**Defer-instinct disguises** (recurring across sessions): every session surfaces a new mask. Session 5 = "won't matter for months / YAGNI / trivial cost so we can add later"; Session 11 = "PBS doesn't need it yet / only planning exists today"; Session 15 = "speculation about future framework primitives is up-front-cost defer territory" (chronological-defer-as-YAGNI mask). The signal: defense feels abstract or principled rather than naming a specific external signal. Honest watch-list framing names a SPECIFIC EXTERNAL EVENT; defer-instinct cites a CATEGORY of caution.

**D Gate** (procedural enforcement at decision moment; per `profiles/INDEX.md`): fires whenever AI considers deferring; blocks until mental modeling within profile grounding attempted.

D Gate procedure:
1. Identify the item being considered for defer
2. Attempt mental modeling within profile grounding (multi-axis validation across L1-L9 profiles + G consumer gate)
3. Construct hypothetical scenarios within profile constraints
4. Check whether primitive's classification holds across mental scenarios
5. Defer ONLY IF mental modeling genuinely cannot resolve
6. If mental modeling resolves → evolve answer NOW (Round 1+2 sharpening)

**Pattern-vs-instance discipline (broader)**: framework primitives stay shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer-instance specifics (Bauleitplanung; B-Plan-Begründung; UNB; DACH-EU regulatory specifics; German Begründung naming) live at workspace level (per practitioner-shape policy mandates), NOT in framework primitive definitions. Per `profiles/L5a-planner-pbs-schulz.md` line 129: "PBS-Schulz specifics like Begründung / Stellungnahme / UNB / DACH-EU need to NOT leak into framework primitives."

### 3. Preliminary-lock — every decision revisable except VISION axes

Every architectural decision in pbs-bureau is **PRELIMINARY-LOCKED**. The "locked" vocabulary in HANDOFF / DRs / ARCH means current best position derived from available reasoning — NOT permanent. Decisions are revisable when VISION ideal design demands it.

**Why**: false stability anchors against re-examination. When a session reads "locked" and treats decision as non-revisable, defer-instinct uses it as polite excuse to compound around wrong locks ("we already decided X, so we work around it"). PBS is in deep design + exploratory phase; specs / DRs / ARCH / code are all living drafts.

**How to apply**:
- Treat every "Status: ACCEPTED" DR, every ARCH version, every meta-rule, every spec rule, every ROADMAP commitment, every backend code module as preliminary-locked.
- When prior decision is treated as constraint on current work, run the **preliminary-lock test**:
  1. Is the decision the IDEAL design per VISION lens, or past compromise / up-front-cost defer / scope limitation?
  2. Has subsequent reasoning surfaced reasons to revise?
  3. Would treating as fixed produce a worse outcome than re-examining?
  - If any answer suggests revision → re-examine. The cost of revising a preliminary-lock now is much smaller than the cost of compounding around a wrong lock.

**Vocabulary discipline**:
- "Locked" = preliminary-locked (current best position)
- "Anchored" = VISION axes only (high-bar revision via real-world falsification)
- "Settled" = avoid; suggests false permanence
- "Decided" = preliminary-decided (revisable)

**What's anchored, NOT preliminary**:
- VISION axes (revise only on real-world falsification per VISION's own criteria — load-bearing real-world signal required; extremely high bar)
- Memory feedback principles + user-stated working-style preferences (user-codified explicitly; user revises directly)

**Composition with no-defer**: the two compose. Never defer NEW decisions, AND prior locks aren't excuses to defer revision. A "permanently-locked" decision used to block re-examination is just a defer of revision.

---

## TOP-LEVEL SCOPE — Repo identity: framework source, not deployment instance

This repo is **the framework + dev tooling source — the starting point for deployments**, NOT a deployment instance itself.

**What lives here**:
- Framework architecture + foundational vocabulary (VISION, GLOSSARY, MAINTENANCE, DISCIPLINES, ARCHITECTURE per Phase 3, DRs, specs)
- **Dev skills only** in `plugin/skills/` — development-process tooling for working ON the framework (sharpening, framing, etc.); pattern-level; not domain-specific
- Plugin manifest scaffolding (`.claude-plugin/`, `plugin/.claude-plugin/`) — for distribution, not for self-instantiation
- Memory feedback files (cross-session AI behavior)

**What does NOT live here**:
- **App skills** — domain-specific workflow logic (drafting, review, validation, domain orchestration). These belong in **deployment instances** built from this framework, not in the framework source. Archive history (v0.35) bundled 19 PBS app skills directly in `plugin/skills/` — that conflated framework with pioneer instance. The rebuild reverses that: framework stays clean; deployments contain their own app skills.
- Workspace instances (`workspace.md`, practitioner records, project state)
- Layer A content for any specific domain/state (PBS extensions, doctype manifests, baustein YAML)
- Per-deployment configuration

**Why this matters**:
- **Distribution clarity**: anyone can clone this repo as a clean starting point for their own deployment without inheriting another deployment's instance state
- **Pattern-vs-instance discipline applied to repo structure**: per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2, framework = pattern-level; PBS-Schulz = pioneer instance. The repo embodying both was a session-12-era conflation that the rebuild corrects.
- **Rebuild-bias prevention**: app skills encode v0.35 vocabulary; restoring them mid-rebuild contaminates locked-architecture work. Phase 6 doesn't rebuild app skills INTO this repo — it rebuilds them as part of deploying the pioneer instance separately.

**Cascade implications**:
- Archived app skills (`archive/plugin/skills/<19 bundles>`) stay archived **permanently** in this repo's history; they don't return to active `plugin/skills/`. Phase 6 builds them into a separate deployment workspace (PBS-Schulz instance), not back here.
- Plugin manifest description (`plugin/.claude-plugin/plugin.json`) currently still describes PBS-domain workflow — staleness; needs rewrite to describe the framework-source-distribution role when Phase 3+ surfaces concrete framework distribution mechanics.
- Future tooling decisions test against: "is this dev tooling for working ON the framework, OR app/domain logic for a deployment?" — only the former lives here.

**See**:
- `MAINTENANCE.md` TOP-LEVEL SCOPE (memory) — archive/restore criteria for plugin skills under this distinction
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (memory) — pattern-vs-instance discipline (broader)
- `archive/INDEX.md` — archived app skills + rationale (don't restore)

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

- **README.md** — one-screen project description; what PBS is; how to enter; pointers to Layer 1
- **HANDOFF.md** — lean session log; ~30-100 lines per session; rotate older sessions to `archive/handoffs/HANDOFF-sessions-N-M.md` when active HANDOFF crosses ~500 lines (keep current session + last 2 entries active)
- **MAINTENANCE.md** — this file; doc system rules
- **DISCIPLINES.md** — cross-session working discipline; how we operate
- **BACKLOG.md** — Phase-tagged work-item tracker; pending items across phases (Phase 2 / 3 / 4 / 5 / 6 / cross-cutting); items added when surfaced + resolved when locked + archived at phase boundaries

### Layer 1 — Foundations (anchored; rarely change)

- **VISION.md** — three-axis thesis + framework's structural primitives + foundations + falsification criteria. **Anchored** per preliminary-lock principle (`memory/feedback_preliminary_lock.md`); revise only on real-world falsification per VISION's own criteria. Pure stance about the product — no tooling/methodology (those live in DISCIPLINES + plugin/skills + memory), no positioning (STRATEGY territory), no architectural detail (ARCH territory), no provenance (HANDOFF + git log).
- **GLOSSARY.md** — canonical vocabulary. **ONE home for every term definition.** Each entry: one-sentence canonical definition + non-examples + cross-archetype examples + boundary tests + cross-references to Layer 3 topic where the term has structural detail. Layer 3+ docs cite GLOSSARY rather than redefining terms.

**Cross-doc territory rule**: framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory. Positioning narrowness (target users + competitive landscape + funding fit + per-shape market positioning) is STRATEGY territory. Pure stance (what the framework IS + the axes it protects) is VISION territory. Foundational vocabulary is GLOSSARY territory. When content surfaces, route by territory rule before lock.

### Layer 2 — Overview

- **ARCHITECTURE.md** — structural primitives (1-line each) + design disciplines (1-line each) + reference card (where things go) + pointers to Layer 3 topics. **Cannot describe mechanisms in detail**; that's Layer 3 territory.
- **ROADMAP.md** — commitments + horizons; lean
- **STRATEGY.md** — market positioning + competitive landscape + funding + ICP. Architectural-adjacent, not architecture itself

### Layer 3 — Architecture detail (topical)

`arch/<topic>.md` — one file per major architectural concern (per Phase 3.2 doc-organization decisions: kebab-case slug; flat directory; no prefixes).

**Single abstraction level per file**: structural mechanisms for primitives; decisional reasoning for disciplines.

#### Pattern A protocol topic template (LOCKED)

For ARCH topics describing Pattern A protocols (Surface + Implementations + Selection per `protocol (architectural)` GLOSSARY entry), use this 18-section template (established by `arch/substrate.md` + validated by `arch/adapter.md`):

| § | Section | Purpose |
|---|---|---|
| 1 | Topic scope + frontmatter | Topic identity; Pattern classification; cardinality; cross-axis claim; composition with framework primitives |
| 2 | Surface contract (architectural-level) | Capability categories; per-class Surfaces if multi-class (two-layer Surface variant); explicit "NOT in Surface" exclusions; logic placement mode (Mode 4 here + Mode 3 spec at Phase 6) |
| 3 | Common-surface boundary criteria | Decision rule for Surface vs per-impl extension |
| 4 | Per-implementation aspect | Pattern level + current Implementation set + per-impl extension Protocols pattern |
| 5 | Selection mechanics | workspace.md selection field; cardinality; validation at boot; re-binding semantics |
| 6 | Tri-aspect reconciliation | Surface + Implementations + Running Instance; coupling-impossible-by-construction |
| 7 | Composition with framework primitives | Cross-references to all primitives this topic composes with |
| 8 | Substrate-internal vs skill-side audit emission | Architectural-event kinds enumeration; dual emission path resolution if applicable |
| 9 | Cardinality + lifecycle | Creator / owner / destroyer; mutability; cross-session persistence |
| 10 | Boot + shutdown phase ordering (architectural-level) | Per-instance lifecycle ordering; flush-before-release invariants |
| 11 | Substrate error categories (architectural-level) | Cross-class architectural categories + per-class refinements; per-shape error semantics |
| 12 | Transport variation + per-tier mapping (where applicable) | Multi-transport mapping; per-tier deployment behavior |
| 13 | Deployment-tier awareness | Tier 1/2/3; per-tier behavior in impl, not Surface |
| 14 | Pre-implementation operational concerns (Phase 6 forward reference) | Explicitly NOT-locked-at-ARCH-level operational details |
| 15 | Watch-list | Items awaiting external evidence; resolution mechanisms |
| 16 | Decision-design provenance | Archived sources; pattern-vs-instance discipline application |
| 17 | Phase routing | Architectural shape (locked here) vs Pydantic spec vs concrete impls (Phase 6) |
| 18 | Cross-references | GLOSSARY entries / disciplines / profiles validated / ARCH topics composing / Phase 6 spec target |

Future Pattern B / C / cross-cutting integrator topic templates locked when first instance lands (foundation-up; substrate established Pattern-A template via first-Pattern-A topic).

#### Provenance hygiene (per coherence-audit Lens 5 v0.2.1)

ARCH topics hold **pure architectural content** — provenance lives in HANDOFF + git log + commit messages + DRs (Layer 4 Sharpening provenance section). No "Pattern note (meta)" / sharpening trajectory / procedural narrative in ARCH topics.

Each topic file: minimal frontmatter (title; topic-cluster; status: drafted/locked/forthcoming); H1 = de-kebab-cased slug.

### Layer 4 — Decision records

`docs/decisions/<decision>.md` — ONE narrow decision per DR (or composite DR for upfront-known decomposition per `decision-design-sharpening` v0.6.0 Mode-2 composite decomposition pattern).

#### DR template (LOCKED)

Sections in order:

1. **Status** — ACCEPTED / SUPERSEDED-BY-X; sharpening rounds metadata (e.g., "2-round sharpening per `decision-design-sharpening` v0.6.0")
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

**Sharpening provenance section IS the meta-home** (resolves where process narrative belongs per coherence-audit Lens 5 v0.2.1: provenance in HANDOFF + git log + commit messages + DRs; NOT in ARCH topics or canonical content).

### Layer 5 — Specs

`docs/specs/<spec>.md` — implementation contracts.

Schema definitions, file format specs, code conventions, plugin authoring conventions, MCP tool conventions.

Versioned: semver if breaking; date if non-breaking.

---

## Cross-reference discipline (the navigability rule)

**Read references go DOWN the layers, not laterally:**

- Layer 0 → Layer 1 + 2 (entry pointers)
- Layer 2 → Layer 3 (overview points at topic detail)
- Layer 3 → Layer 4 + 5 (topic points at decisions + specs)
- Layer 4 → Layer 5 (decisions reference specs they implement)

**No lateral peer-references except within the same layer.** If two Layer 3 topics share a concept, that concept either:
- Belongs in GLOSSARY (Layer 1 — vocabulary)
- Belongs in ARCHITECTURE (Layer 2 — overview/reference card)
- Belongs in a third Layer 3 topic that both reference

**No upward read-references.** Layer 4 doesn't reference Layer 3 (Layer 3 references Layer 4). Forces hierarchy clarity.

**Note distinction**: cross-references are about READ direction (navigability). Cascade discipline is about WRITE direction (consistency when changing). When you change Layer 1 GLOSSARY, the change cascades DOWN to Layers 2-5 even though no Layer 1 doc references downward.

---

## Other maintenance disciplines

1. **Single abstraction level per doc.** If a Layer 2 doc starts describing mechanism details, split the detail to Layer 3. If a Layer 3 doc starts describing schemas, split the schema to Layer 5.
2. **Line budget as forcing function.** When a doc exceeds budget, decompose to next layer.
3. **One decision per DR** (Layer 4). If a decision splits, write multiple DRs.
4. **GLOSSARY is the single source for term definitions.** Layer 3+ docs may discuss structural detail about a primitive but cite GLOSSARY for canonical definition. If two docs define the same term, that's a cascade violation.
5. **Versioning per layer**:
   - VISION + ARCHITECTURE versioned (semver-ish on architectural significance)
   - DRs dated (no version; supersession via header note)
   - Specs semver
   - Topics + GLOSSARY versioned only on breaking changes (date for non-breaking)
6. **Periodic prune.** At major version boundaries: which docs no longer earn their keep? Collapse to broader topic / archive. Don't let dead docs accumulate.

---

## When this doc itself changes

This doc is Layer 0 — it governs the doc system itself. Changes to MAINTENANCE.md require especially careful cascade because they affect everything. When changing MAINTENANCE.md:

1. Identify what existing structure or discipline is being changed
2. Verify all docs currently following the prior rule still hold OR list which docs need updating to follow the new rule
3. Update HANDOFF.md to flag the rule change for future-session readers

---

## Composition

This doc holds TOP-LEVEL META-design principles (cascade / architecture / scope / design-principles / 5-layer model + templates). Operational disciplines (HOW we operate) live in `DISCIPLINES.md`. Memory feedback files in `memory/` hold cross-session AI behavioral preferences only:

- `feedback_propose_before_commit.md` — at decision phases propose first (decisions+reasons in chat); at content phases write directly without verbatim chat preview
- `feedback_judgment_and_automate.md` — commit positions instead of menus; routine work without asking
- `feedback_push_after_commit.md` — push immediately after each commit
- `feedback_blocked_actions.md` — surface hook/permission/sandbox blocks immediately; never workaround
- `feedback_plugin_marketplace_clone_sync.md` — operational tool note (marketplace clone sync mechanics)

Disciplines previously in memory (source-grounded / apply-principle-uniformly / pre-decision-sharpening / foundation-up-ordering / multi-axis-validation / vision-arch-grounding / skill-files-are-sources / llm-instruction-tightness) are absorbed into `DISCIPLINES.md` per session-16 doc-organization composite DR.

Architectural commitments previously in memory (wrong-shapes-impossible / pattern-not-instance / preliminary-lock / dev-vs-app-skills) are absorbed into MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES + TOP-LEVEL SCOPE sections. The `feedback_ai_as_runtime` content is absorbed into `ARCHITECTURE.md` cross-cutting principles.
