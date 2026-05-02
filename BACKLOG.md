# Backlog

Central tracker for pending work items across phases. Read at session start alongside `DISCIPLINES.md`, `VISION.md`, `MAINTENANCE.md`, `HANDOFF.md`.

## How this works

- **Items added when surfaced** (during audits, sharpening rounds, GLOSSARY locking, etc.). Each item carries: title, origin, description, refs.
- **Items resolved when locked** in same commit (per cascade discipline). Move to "Resolved" subsection with commit-ref.
- **Periodic archival** at phase boundaries: resolved items move to `archive/BACKLOG-<phase>.md` to keep the active backlog scannable.
- **Phase-tagged sections** so future sessions starting a phase can scan their relevant block.

Format per item:

```
- **<title>** [origin: <where surfaced>] — <description> | refs: <doc#section>
```

When resolved:

```
- ~~**<title>**~~ [resolved <commit-ref>] — <one-line outcome>
```

---

## Phase 2 — GLOSSARY (COMPLETE — pending Phase 3 transition)

### Open

(none — all Phase 2 entries locked)

### Resolved (current phase; archival at Phase 3 start)

- ~~**pioneer instance**~~ [resolved this commit] — originating deployment role (production-tool + research-lab + IP-proving-ground); cross-references PIONEER.md as identity-anchor; final Phase 2 entry — vocabulary lock complete
- ~~**rubber-stamping**~~ [resolved 0f172a5] — axis-3 failure mode (sign-off without engagement); parallel to tacked-on AI (axis-1) + axis-2 trio; independent dimension from axis-2 failures (can co-occur)
- ~~**answer-machine AI / oracle AI / validator AI**~~ [resolved abc0153] — axis-2 failure modes per Ming research; locked as 3 distinct entries with parallel structure (extraction / declarative / affirmation directions); naming-collision disambiguation noted for validator AI vs validator-mode (skill-craft / sharpen vocabulary)
- ~~**category collapse**~~ [resolved ef35933] — cross-axis force that degrades engagement regardless of architectural intent (axis-1 primary anchor; manifests on all three axes per Round 1 stress-test)
- ~~**adapter**~~ [resolved 7d199e5] — final Pattern A primitive locked
- ~~**work-unit**~~ [resolved 6a5dc53] — added per Round 3 audit RA2 (was missing canonical home)
- ~~**claim**~~ [resolved 480bfaa] — added per Round 3 audit RA1 (atomic accountability-bearing-assertion)
- ~~**defensibility**~~ [resolved 8547337] — operational test for axis 3
- ~~**co-worker**~~ [resolved ec5840a] — relational claim about AI's mode of participation
- ~~**intertwined AI**~~ [resolved ec5840a] — positive axis-1 mode (success state)
- ~~**tacked-on AI**~~ [resolved ec5840a] — failure mode of axis 1 (contrast / anti-pattern)
- ~~**AI runtime**~~ [resolved 480bfaa REMOVED] — was STUB-only; redundant with substrate's Instance aspect
- ~~**RA4 Client instance-leakage fix**~~ [resolved 6a5dc53] — moved from framework-level to shape-policy-mandated

---

## Phase 3 — ARCHITECTURE rebuild (in progress)

Sub-phase ordering per HANDOFF Phase 3 launch entry (note 28). Foundation-up: structure shape first, then questions, then topic taxonomy, then content, then audit.

### 3.0 Doc structure ✅ LOCKED

- **Hybrid structure** — single `ARCHITECTURE.md` overview (~1-2K lines: topic catalog + cross-cutting principles + how topics compose) + `arch/<topic-slug>.md` per-topic files (~500 lines each; 15-20 topics). Pure-single (10K lines unwieldy + context-budget concern) and pure-multi (no entry point + cross-cutting orphaning) both rejected. Hybrid aligns with progressive-disclosure principle (skill-craft pattern: SKILL.md → PROCEDURE.md → references/) + sharpen's AI-executor test (cognitive iteration via structure, not gist-extraction across 10K lines).

### 3.1 Open architectural questions (foundational; resolve before topic content)

#### Open

- **work-unit bipartite-classification** [origin: work-unit entry hedge, RA3 Round 3] — same shape as workflow; KIND DISCRIMINATOR in specialist DEFINITION + INSTANCE at Owner B; cascades from workflow resolution | refs: GLOSSARY#work-unit | **NEXT** (workflow resolved per Round 1 + Round 2 sharpening; work-unit follows similar pattern)
- **"deployment" definition sharpening** [origin: EA5 Round 3 + workspace entry] — current preliminary lock: "one git-clone + activated workspace.md per deployment"; sharpen mechanically | refs: GLOSSARY#workspace
- **Engaged-authorship operational definition** [origin: defensibility entry] — what counts as "engaged" vs rubber-stamped at framework level | refs: GLOSSARY#defensibility

#### Resolved

- ~~**workflow bipartite-classification**~~ [resolved this commit] — re-classified to bipartite Pattern B with optional applicability: DEFINITION in specialist's distributable bundle (specialist-bundled, not standalone Framework C); INSTANCE = workflow_instance entity at Owner B. Critical refinement (Round 2 + user push): workflow_instance is OPTIONAL structural overlay — engages only when work follows codified pattern; ad-hoc work-units have no workflow_instance and run via session + work-unit + skill + claim + event without workflow primitive. Round 2 surfaced 9 EXPANSIONS (vocabulary disambiguation; versioning snapshot semantics; claim/skill/authority-binding composition; observability for quality-gate; mutability semantics DEFINITION-vs-INSTANCE; failure modes; multi-practitioner ownership) + 1 REVISION (scope clarification per user push: ad-hoc work outside primitive scope, not "degenerate Pattern B case" as Round 1 ST4 had it). Cascade applied to specialist / workspace / session / claim / event / intertwining / work-unit entries.

### 3.2 Topic taxonomy (lock topic identities before content)

Doc-structure-shape resolved at 3.0 (hybrid). Remaining decisions:

- **Topic taxonomy** — ~30 BACKLOG items across 6 buckets (mechanism / protocol / primitive / primitive-detail / quality-gate / cross-cutting). Decide: 1:1 mapping (28+ topics, over budget) vs aggregation (e.g., "audit + event mechanisms" combines audit-trail + audit-emission + event-related). Per MAINTENANCE budget: 15-20 topics × ~500 lines.
- **File naming convention** — `arch/<topic-slug>.md`? Slug rules (kebab-case; how to name aggregated topics; how to disambiguate Pattern A protocol topics vs primitive-detail topics for substrate / adapter)?
- **Cross-cutting topics placement** — where do axis-interactions, quality-gate, scope-model live? In `ARCHITECTURE.md` overview, in dedicated `arch/<topic>.md`, or hybrid (overview summary + dedicated detail file)?
- **ARCHITECTURE.md overview structure** — sections it should contain (topic catalog with one-line summaries; cross-cutting principles; how topics compose; reading order recommendation; etc.)

### 3.3 Per-mechanism detail (12 mechanism instances)

Foundation-up within bucket: defensibility-supporting mechanisms first.

- **source-grounding** detail — every claim traces to source; framework-level enforcement; cited-source schema | foundational for defensibility | archived: relevant per archived corpus
- **audit emission** mechanism detail — AuditEvent Pydantic schema; event_kind catalog | foundational for audit-trail | archived: audit-trail-v2.md
- **audit trail** detail — sequence-of-events composition; append-only discipline; retention policy | composes from audit-emission | archived: `audit-trail-v2.md`
- **8 sparring sub-mechanisms** detail — counter-argument; confidence calibration; visible reasoning; selective friction; asymmetric knowledge respect; anti-sycophancy; commit-to-recommendations; what's-missing — per-mechanism Surface + composition | archived: relevant
- **orchestration** detail — continuous decision layer; orchestrator skill mechanics | archived: orchestrator skill in archived plugin
- **persistent state** detail — state across sessions; cross-session-handoff schema | archived: relevant per substrate-protocol-design.md
- **authority binding** mechanism detail — `actor_kind` enum extension; authorization flow | archived: governance-and-identity-sourcing.md

### 3.4 Per-architectural-Protocol + Per-Pattern-A primitive detail

Foundation-up: substrate first (most foundational); then adapter; then 5 named protocols.

- **Substrate Protocol** Surface specification (method set; tier-awareness; lifecycle events) | archived: substrate-protocol-design.md, sdk-deep-read.md
- **substrate** per-impl detail (Claude Agent SDK, MS Agent Framework) + deployment-tier framing + eval-framework integration | archived: substrate-agentic-framework.md, sdk-deep-read.md
- **Adapter Protocol** per-integration-class Surface specs (email, accounting, MCP-server, A2A-peer) | archived: a2a-and-gemini-pattern-emulation.md, plugin-conventions.md, backend-conventions.md
- **adapter** lifecycle / auth-refresh / error-handling semantics; permission-flow integration
- **Sparring Protocol** Surface + impl variations (always-on / optional / sparring-as-skill / none)
- **Audit Protocol** Surface + granularity-policy variation (claim-level / action-level / light)
- **Coordination Protocol** Surface + impl variations (event-shaped vs call-shaped)
- **Trust Protocol** Surface + trust-model variations (practitioner-judgment / budget-policy / individual)
- **Time Protocol** Surface + temporal-semantics variations (turn-based / long-running / heartbeat-based)

### 3.5 Primitive-detail topics + axis-interaction analysis

Per-primitive deeper detail; cross-cutting axis-interactions.

- **specialist** granularity 3-test + composability axes + two-tier classification + marketplace mechanics + instance-content destruction semantics | archived: terminology-and-specialist-primitive.md, entity-md-scope-model-restructure.md
- **skill** granularity 3-test + frontmatter schema + output validation | archived: skill-expert-agent-and-domain-knowledge.md
- **practitioner** deactivation semantics + multi-practitioner workspace mechanics + legal-entity workspace context | archived: office-level-managed-entities.md
- **workflow** representation schema + handoff semantics + multi-session continuity | archived: workflow descriptions in plugin/skills/
- **session** boundary semantics + context-handoff rules + persistent-state migration | archived: substrate-protocol-design.md
- **event** AuditEvent Pydantic shape + event_kind catalog + append-only discipline | archived: audit-trail-v2.md
- **actor** full `actor_kind` enum + A2A actor support + identity sourcing | archived: a2a-and-gemini-pattern-emulation.md, governance-and-identity-sourcing.md
- **claim** claim-event schema + claim-revision semantics + finalization mechanics + source-grounding requirements per claim + sparring-target mechanics + audit-trail attribution per work-unit | archived: audit-trail-v2.md
- **defensibility** conditions formalization + six-months-later test mechanics + regulatory-challenge schema + structural enforcement mechanisms + defensibility-on-claim-revision semantics
- **Axis-interactions explicit articulation** [origin: VISION sanity check, Lens 3] — VISION sketches axis interactions through examples (sparring within intertwining; tacked-on sparring is axis-1 failure; defensibility resolves at claim-granularity in axis-1 work-products) but doesn't articulate them systematically. Dedicated axis-interactions analysis as architectural pattern.

### 3.6 Quality-gate ARCH topic (runtime mechanism)

- **Quality-gate mechanism for runtime** [origin: session 16, while building generic `sharpen` skill; refined session 16 after category-collapse lock] — runtime mechanism to monitor for category-collapse manifestations across all three axes (axis-1 tacked-on; axis-2 answer-machine/oracle/validator; axis-3 rubber-stamping), surface drift signals, intervene with friction or re-engagement nudges. Fires at checkpoints (pre-send, pre-claim-finalization, pre-decision-lock, per-edit, drift-audit). Converts category-collapse-resistance from ENABLED-architecturally to ENFORCED-at-gate-firing-moments. Prerequisites: ✅ category collapse locked; ✅ axis-2 failure mode trio + rubber-stamping locked; Phase 3 architectural decisions still pending: mechanism vs Pattern A protocol; per-shape variation; observability schema; intervention mechanics. Detail in `drafts/quality-gate.md`.

### 3.7 Cross-cutting investigations

Investigations that surface during ARCH work; not blocking core sub-phases.

- **PydanticAI substrate evaluation** (#7) — re-examine #18 substrate eval + #20 PydanticAI eval against locked vocabulary | archived: substrate-agentic-framework.md, permission-abstraction.md | composes with 3.4 Substrate Protocol detail
- **Markdown-validation feasibility analysis** (#8) — distinguish structural validation (frontmatter / required-sections — feasible; libraries exist) from semantic procedure validation (impossible-by-nature; LLM-judged eval territory). Inform what kind of structural enforcement ARCH builds.
- **Ming research deeper investigation** [origin: session 16 reframing — Ming is spirit-anchor for proper-AI-work, not framework identity] — Vivienne Ming's primary work beyond the WSJ article + Robot-Proof book reference. Investigate her IEP framing in detail; her cognitive-science background; other empirical work on hybrid human-AI teams. Goal: deeper understanding of WHAT Ming actually claims vs. what we've inferred. Inform whether VISION's axis-2 anchor is correctly stated.
- **Adjacent thinkers expansion** [origin: session 16 — currently Schön, Kahneman, Dreyfus listed as adjacent; user noted "maybe we should draw on other thinkers"] — investigate other thinkers whose work grounds proper-AI-work / collaborative-rigor / capacity-preservation: Hubert Dreyfus deeper (skill acquisition; embodied expertise); Etienne Wenger (communities of practice); maybe Christopher Alexander (pattern languages applied to AI architecture); maybe Stafford Beer (cybernetics of management systems). Determine which deserve promotion to anchor status alongside Ming.
- **Multi-VISION model question** [origin: VISION Phase 1.85 clean-stance restructure] — VISION used to claim "this document remains the practitioner-shape articulation; when second-shape productization happens, that shape gets its own per-shape VISION." Removed during Phase 1.85 (VISION is now shape-neutral). Open architectural decision: when second-shape productization happens, does (a) each shape get its own per-shape VISION; (b) VISION expand to multi-shape unified articulation; (c) VISION stays shape-neutral and per-shape positioning lives in STRATEGY only? Decision deferred to Phase 3 ARCH or Phase 5 STRATEGY (whichever surfaces it first).

### 3.8 Coherence-audit Lenses 11-15 activation (phase-boundary audit)

ARCH-corpus-specific lenses activate when ARCH approaches lockable state. Run before Phase 4 transition.

- **Lens 11 (Inter-layer consistency)** — formalize ARCH ↔ GLOSSARY ↔ DR ↔ spec citation health checks
- **Lens 12 (Specs traceability)** — every ARCH topic with implementation contract has corresponding spec OR explicit deferral
- **Lens 13 (Architectural protocol completeness)** — coverage check for all named Pattern A primitives
- **Lens 14 (DR coverage gap)** — every architectural commitment lives in ARCH OR has explanatory DR
- **Lens 15 (Granularity match)** — per ~500-line topic budget; decomposition / merge signals

---

## Phase 4 — Decision Records (selective)

### Open

- **DR coverage gap** items — surface from Lens 14 audit; capture decisions that need standalone DR (vs ARCH-embedded)

---

## Phase 5 — ROADMAP rebuild

### Open

- **AI-app-development-facilitation skill** [HIGH priority per user direction session 16] — captures cross-project discipline for building AI-centric apps; transferable to other AI-app projects. Consumes accumulated observations from `learnings/` folder. Per user: "should be our first ROADMAP item even though we will have many items that come before it."
- **`learnings/` distillation** — when per-session entries accumulate stable patterns (typically 3-5 sessions of evidence), distill into structured topic-specific docs in `learnings/`; promote held observations to memory feedback rules / DRs / ARCH disciplines as appropriate. Feeds into the AI-app-development skill above.
- **Testing harness for the framework** — eventual harness for systematic testing of framework primitives (mechanisms, protocols, shape conformance, sparring-output validation, audit-emission correctness). Composes with PydanticAI eval framework if adopted (per Phase 3 #7). Distinct from per-skill testing; this is harness for the framework layer itself.
- **Markdown structure validation (investigation + adoption)** — investigate (a) existing libraries for markdown structural validation (frontmatter conformance, required-sections-present, cross-ref existence, schema-of-allowed-tag-values); (b) what we already had in archived code (`backend/mcp-server/` + `plugin/skills/{audit,design-review}/`). Composes with Phase 3 #8.

### Open — Shape-neutrality validation for second-shape productization

- **Shape-neutrality stress-test for non-practitioner shapes** [origin: session 16 retrospective audit, GAP 1] — current GLOSSARY primitives have practitioner-shape-anchored framing (practitioner; intertwining/sparring/authorship axes; defensibility; failure modes including rubber-stamping). Profile L5e autonomous-business-operator + L5f personal-OS-knowledge-worker stress-test shape-neutrality: framings need shape-policy variants when second shape gets productized (axis-3 N/A or redefined for autonomous-business; defensibility shape varies; failure modes anchored differently). D-gate-validated: this is GENUINE awaited-evidence gap (mental modeling resolves SHAPE-POLICY-VARIATION pattern but specific shape-policy details await second-shape design). Per `feedback_pattern_not_instance_defers.md` no-defer principle: not a primitive-level revision needed today; framework primitives stay shape-neutral; shape primitive's policy bundle handles per-shape variation; **awaited signal**: second-shape design begins (autonomous-business OR personal-OS productization). Resolution at signal: validate primitive framings + new shape's policies handle the variations cleanly. Watch-list mechanism: track which primitives need shape-policy variants when second shape lands.

### Open — Composability tooling

- **Composability tooling — CLI / validators / linters enforcing packaging boundaries** [origin: session 16, profiles + composability discipline work] — tooling that makes packaging boundaries STRUCTURAL (per `feedback_wrong_shapes_impossible.md`): specialist self-containment validator; shape composition validator; deployment template composition validator; workspace serializer / deserializer; audit-trail integrity verifier across migration; license + provenance verification; cross-substrate / cross-shape compatibility checkers. Not blocking framework lock; emerges as framework matures + first non-pioneer deployments surface integration friction. Anchored to L1-L4 producer profiles + G composability gate per `profiles/`. Detail in `drafts/composability-tooling.md`. Trigger for graduation: Phase 5 ROADMAP identifies as ship-target OR first non-pioneer deployment surfaces packaging friction OR Phase 6 specs need concrete tooling to enforce contracts.

### Open — Tooling promotion to shippable status (lifted from VISION post-1.85 restructure)

- **Tooling unified narrative doc** [origin: VISION post-1.85 restructure removing tooling from VISION] — when the framework's tooling (dev-skill methodology + decision-making disciplines + sharpening skills + coherence-audit) matures from emerged-side-product to deliberate-ship-target, write unified narrative doc (TOOLING.md or similar) that articulates what the tooling is + why it's distributable + how contributors / similar-framework-builders use it. Until then: tooling content stays distributed across `plugin/skills/` + `DISCIPLINES.md` + `memory/` + `MAINTENANCE.md` in their natural homes. Trigger: when at least 2 framework deployments use the tooling externally OR when sharpening skills feel deliberately shippable (not just "we needed them"); whichever fires first.

### Open — STRATEGY content lifted from VISION Phase 1.85

When STRATEGY.md is created, fold these positioning claims (removed from VISION during clean-stance restructure):

- **Target users / ICP positioning**: solo professionals and small companies in expert-practitioner domains (planners, lawyers, researchers, accountants, consultants, boutique firms). NOT enterprise federated deployments — that's a different archetype with separate migration path.
- **Single-big-model orchestration competitive framing**: framework's strengths (domain coherence; low operational overhead; vendor-neutral; big-context cross-specialist reasoning) land precisely in the solo-to-small expert-practitioner segment. Useful for STRATEGY's competitive-landscape section.
- **Competitive positioning vs service-as-software market thesis** (mentioned in archived VISION; STRATEGY engages with opposing market thesis).
- **Per-shape positioning + funding fit + cross-archetype migration paths** — when productizing second shape, STRATEGY articulates per-shape positioning (existing VISION cross-doc reference says STRATEGY = positioning + competitive landscape + funding).

---

## Phase 6 — Specs + code refactor

### Open

- **App-skill rebuild against locked architecture** — 19 archived skills (orchestrator, draft-textteil-b/c, review-draft, validate-checklist, validate-bausteine, validate-latex-style, verify-citations, research-references, draft-cover-mail, save-baustein, record-feedback, survey-project, promote-to-skill, watch-list, audit, design-review, author-manifest, setup-office). REBUILD INTO **deployment instance** (e.g., PBS-Schulz), NOT into this repo (per TOP-LEVEL SCOPE commitment).
- **Backend / MCP server rebuild** — Python MCP server (LanceDB + fastembed + bge-m3 + LaTeX compile wrapper). Same: deployment instance, not framework source.
- **Single-touch refactor** (#11 from archived ROADMAP) — `department:` → `specialist:` frontmatter rename + slash-command namespacing rebuild

---

## Cross-cutting (any phase)

### Open

- **Plugin manifest description rewrite** [origin: session 16 dev-skill restoration] — `plugin/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` descriptions are neutral placeholder; full positioning rewrite when framework-distribution mechanics surface (Phase 3+)
- **Sharpening skills global plugin elevation** (#23 from archived ROADMAP) — promote `decision-design-sharpening` + `pre-implementation-sharpening` + `coherence-audit` to a global plugin so other AI-app projects can use them

---

## Discipline

### When to add items here

- During GLOSSARY locking: forward-references like "Phase 3 ARCH resolves..." → add Phase 3 entry here
- During coherence-audit / decision-design-sharpening: items not actionable in current scope → add to relevant phase
- During HANDOFF writing: deferred items mentioned → add here
- Per TOP-LEVEL CASCADE discipline: when an item resolves, mark resolved in same commit

### When NOT to add items here

- Trivial / ephemeral details that fit within current task
- Items already captured in HANDOFF as session-state (BACKLOG = forward-looking; HANDOFF = current session log)
- Items that should live in memory feedback files (cross-session AI behavior, not work to do)

### Auto-add expectations from skills

- **`coherence-audit`** Lenses 11-15: items deferred to ARCH should be added here automatically
- **`decision-design-sharpening`** chronological-defers: surface as BACKLOG entries naming the awaited signal
- **`pre-implementation-sharpening`** flow-back items: DR amendments + implementation-readiness checklist items

### Periodic archival

At phase boundary (e.g., when Phase 3 starts): resolved Phase-2 items move to `archive/BACKLOG-phase-2.md`; active backlog stays scannable.
