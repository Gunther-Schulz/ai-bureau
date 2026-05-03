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

#### Resolved

- ~~**Engaged-authorship operational definition**~~ [resolved this commit] — locked as DERIVED axis-3 success mode with two-phase composite definition: (1) production-phase engagement (axis-2-anchored sparring events) + (2) attestation-phase engagement (axis-3-anchored per-claim attestation event). Both phases independent; both must structurally complete. Per-claim per-version granularity. Two layers of operationalization: framework-PRESENCE (Y/N event-existence test) + shape-policy-QUALITY (depth-of-engagement signals; quality-gate enforces). Framework-level enforcement via events + quality-gate (Pattern A) per shape policy. Round 1 + Round 2: 0 architectural REVISIONS surfaced (R1 PRIMITIVE / R2 merge-into-defensibility / R3 single-phase / R4 per-attestation-granularity all rejected) + 10 EXPANSIONS applied (vocabulary disambiguation; Lens 6 reciprocal asymmetry with rubber-stamping; claim revision per-version semantics; quality-vs-presence two-layer model; workflow_instance composition; multi-claim batch attestation; authority-binding orthogonal composition; pre-existing-claim ingestion; TOC §8 placement; AI-runtime-vs-practitioner engagement subject distinction). Cascade applied: new engaged-authorship GLOSSARY DERIVED entry + TOC + defensibility Condition #1 reference + authorship preservation Composes-with + rubber-stamping Composes-with + quality-gate Composes-with + claim Composes-with. DR created. **Phase 3.1 CLOSED**.
- ~~**"deployment" definition sharpening**~~ [resolved this commit] — locked as DERIVED concept = workspace-as-bound-runtime (binding-act-aspect of workspace); 1:1 with workspace at framework level. Vocabulary distinction: workspace = entity (configuration view); deployment = binding-relation (runtime view). Multi-environment / multi-tenant scenarios resolve at workspace-count or substrate-Instance level (not at deployment-cardinality level). Workspace identity may persist across multiple deployments over time. Round 1 + Round 2: 0 architectural REVISIONS (R1 retire-vocabulary / R2 scope-classification / R3 Pattern A all rejected) + 8 EXPANSIONS applied (industry-vocabulary disambiguation; snapshot/restore + substrate migration semantics; orthogonality with pioneer instance; reciprocal cross-ref; multi-environment taxonomy; quality-gate observability flow; entity-vs-relation framing). Cascade applied to GLOSSARY (new deployment entry + workspace Cardinality + pioneer instance Composes-with + TOC). DR created.
- ~~**work-unit bipartite-classification**~~ [resolved this commit] — re-classified to bipartite Pattern B parallel to workflow + specialist: KIND DEFINITION aspect in specialist's distributable bundle (specialists declare `work-unit kind`s + per-kind structural conventions); INSTANCE aspect = `work-unit instance` entity at Owner B. Critical asymmetry vs workflow (load-bearing): work-unit is **always-present container** (every accountability-bearing piece of work IS a work-unit); workflow_instance is OPTIONAL overlay attached to it. Round 2 surfaced 8 EXPANSIONS (kind-namespace disambiguation; multi-workflow_instance composition; kind snapshot semantics; quality-gate observability source; multi-practitioner authorship; authority-binding on lifecycle transitions; orphan-instance handling on specialist deactivation; always-present subsection added per Lens 6 reciprocal symmetry) + 0 architectural REVISIONS (R1 split / R2 always-present-shape-variation / R3 kind-decoupling all rejected). Cascade applied to specialist / workflow / Owner B scope / TOC entries. DR created.
- ~~**workflow bipartite-classification**~~ [resolved this commit] — re-classified to bipartite Pattern B with optional applicability: DEFINITION in specialist's distributable bundle (specialist-bundled, not standalone Framework C); INSTANCE = workflow_instance entity at Owner B. Critical refinement (Round 2 + user push): workflow_instance is OPTIONAL structural overlay — engages only when work follows codified pattern; ad-hoc work-units have no workflow_instance and run via session + work-unit + skill + claim + event without workflow primitive. Round 2 surfaced 9 EXPANSIONS (vocabulary disambiguation; versioning snapshot semantics; claim/skill/authority-binding composition; observability for quality-gate; mutability semantics DEFINITION-vs-INSTANCE; failure modes; multi-practitioner ownership) + 1 REVISION (scope clarification per user push: ad-hoc work outside primitive scope, not "degenerate Pattern B case" as Round 1 ST4 had it). Cascade applied to specialist / workspace / session / claim / event / intertwining / work-unit entries.

### 3.2 Topic taxonomy (lock topic identities before content)

Doc-structure-shape resolved at 3.0 (hybrid). Remaining decisions:

- ~~**Topic taxonomy**~~ [Sub-decision 1 of 4 RESOLVED this commit] — locked at 14 ARCH topics in protocol-centric aggregation with primitive-cluster topics: 8 Pattern A protocol topics (substrate / adapter / sparring / audit / coordination / trust / time / quality-gate) + 4 primitive-cluster topics (specialist+skill / practitioner / workflow+work-unit / claim+defensibility) + 2 cross-cutting topics (scope-model / axis-interactions). Foundation-up ordered. Under MAINTENANCE budget (15-20 cap) with 6-topic headroom. Aggregation discipline: tightly-coupled OR individually <100 lines. Phase 3.7 cross-cutting investigations excluded (research/strategic, not ARCH-topic-shaped). Round 2: 10 EXPANSIONS / 0 REVISIONS / 6 manufactured-criticism revisions rejected. Detail: `ARCHITECTURE.md` Topic taxonomy section.
- ~~**File naming convention**~~ [Sub-decision 2 of 4 RESOLVED this commit] — locked: `arch/<slug>.md` flat directory; lowercase kebab-case slug = topic name; aggregation join via hyphen (e.g., `specialist-skill.md`, `workflow-work-unit.md`, `claim-defensibility.md`); no numeric/bucket/category prefixes; no sub-directories; no arch/README.md (ARCHITECTURE.md is canonical entry); plain .md extension; minimal frontmatter (title/topic-cluster/status); H1 = de-kebab slug. Round 2: 9 EXPANSIONS / 0 REVISIONS / 5 manufactured-criticism revisions rejected (bucket sub-dirs / numbered prefix / `+` aggregation char / multi-aspect sub-files / generic-word ambiguity). Detail: `ARCHITECTURE.md` File naming convention section.
- ~~**Cross-cutting topics placement**~~ [Sub-decision 3 of 4 RESOLVED this commit] — locked: cross-cutting TOPICS (axis-interactions / scope-model / quality-gate) get dedicated `arch/<topic>.md` files (per Sub-decision 1); cross-cutting CONCERNS (Pattern-A/B/C semantics / cascade direction / scope framing / foundation-up ordering / gate disciplines) live in ARCHITECTURE.md sections. Distinction (TOPIC = architectural content; CONCERN = meta-principle) is load-bearing. Reading order: cross-cutting topics LAST in foundation-up sequence. No content migration MAINTENANCE.md ↔ arch/scope-model.md (layer-distinction maintained). Catalog uniformity (one-liner same depth as other topics). Round 2: 8 EXPANSIONS / 0 REVISIONS / 4 REVISIONs rejected. Detail: `ARCHITECTURE.md` Cross-cutting topics placement section.
- ~~**ARCHITECTURE.md overview structure**~~ [Sub-decision 4 of 4 RESOLVED this commit] — locked: 9-section structure (Audience+scope / Phase status / Doc structure / Topic catalog / Reading order / Cross-cutting principles / Locked decisions / Disciplines / Watch-list). Audience+scope explicit (framework-developer documentation; Mode 4; not production-runtime). Logic placement modes 4-mode distribution (Mode 1 production-runtime LLM-MD / Mode 2 production-runtime Python / Mode 3 hybrid Phase 6 specs / Mode 4 development-time documentation) added to cross-cutting principles. Catalog uniformity (cross-cutting topics same one-liner depth as other topics). Locked decisions section growth mitigation via short summaries + cross-refs. Round 2: 8 EXPANSIONS / 0 REVISIONS / 3 REVISIONs rejected. Detail: `ARCHITECTURE.md` (this commit fully restructures to 9-section form). Foundational consumer-model question (raised mid-sharpening) drove explicit Audience+scope section + Logic placement modes codification.
- **Phase 3.2 composite DR** [final synthesis pass — NEXT] — after all 4 sub-decisions lock (✅ all locked this commit), single composite DR captures Phase 3.2 doc-organization decisions per Mode-2 composite decomposition (decision-design-sharpening v0.6.0).

### 3.3 Per-mechanism detail (subsumed under Pattern A protocol topics per Phase 3.2 Sub-decision 1; mechanism content lives in respective protocol topics)

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

- ~~**Substrate Protocol** Surface specification + per-impl detail (Claude Agent SDK / MS AF / hand-rolled) + deployment-tier framing~~ [resolved this commit] — `arch/substrate.md` LOCKED as first canonical Pattern A protocol topic. Anchors the 12+7 Pattern A / mechanism-class topic template per `MAINTENANCE.md` Layer 3; 7 capability categories Surface contract (A-G); per-impl extension Protocols pattern; tri-aspect Pattern A reconciliation; boot/shutdown ordering + error categories + transport variation + tier-awareness as cross-cutting + schema-detail layer; substrate-internal vs skill-side dual audit emission. Phase 6 spec lands Pydantic Protocol contract (Mode 3) + concrete impls. 13 EXPANSIONS / 0 REVISIONS / 3 manufactured criticisms rejected. DR `substrate-arch-topic.md` created. Profile-anchored validation properly executed (4/4 clusters PASS with cited content). Procedural-fidelity case for `DISCIPLINES.md` Discipline 1 (skill+profile sub-section) discipline.
- ~~**Adapter Protocol** per-integration-class Surface specs + adapter lifecycle / auth-refresh / error-handling / permission-flow integration~~ [resolved this commit] — `arch/adapter.md` LOCKED as second Pattern A protocol topic. Validates 12+7 Pattern A template; two-layer Surface (META + 5 per-integration-class: Email / Accounting / MCP-Server / A2A-Peer / File-Sync); multi-instance cardinality; auth + lifecycle architectural-level; per-class error categories; circuit-breaker semantics; cross-shape policy variation; hot-swap re-binding; per-action audit emission via MCP gate (skill-side); permission flow composition with substrate Surface §C. 20 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected. DR `adapter-arch-topic.md` created. GLOSSARY back-check clean. Profile-cluster validation 4/4 PASS with cited content.
- ~~**Sparring Protocol** Surface + 8 sub-mechanisms + impl variations~~ [resolved this commit] — `arch/sparring.md` LOCKED as third Pattern A protocol topic. Single-layer Surface with 8 sub-mechanism categories (4 architecturally-encoded + 4 behaviorally-enforced per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator); per-shape activation matrix (NEW Pattern A cardinality pattern); composition with substrate Surface §D for architecturally-encoded sub-mechanisms; sparring events = production-phase substrate for engaged-authorship; per-shape escalation behavior + per-sub-mechanism event-kind catalog + axis-2 failure-mode detection. 20 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected. DR `sparring-arch-topic.md` created. GLOSSARY back-check clean. Profile-cluster validation 4/4 PASS with cited content.
- ~~**Audit Protocol** Surface + granularity-policy variation~~ [resolved this commit] — `arch/audit.md` LOCKED as fourth Pattern A protocol topic. 18 sections; single-layer Surface with 6 capability categories (emission/persistence/query/integrity/catalog/state-rendering); audit-trail-as-canonical-source architectural commitment; append-only enforcement gate-dispatched-structural; per-shape event-kind catalog (claim-level / action-level / light); boot-before-substrate + shutdown-after-substrate ordering; hash-chain integrity verification; cross-deployment evidence + external-format export. NEW deployment-tier-driven cardinality variation (4th Pattern A cardinality pattern). 21 EXPANSIONS / 0 REVISIONS / 5 manufactured criticisms rejected. DR `audit-arch-topic.md` created. GLOSSARY back-check clean. Profile-cluster validation 4/4 PASS with cited content.
- **Coordination Protocol** Surface + impl variations (event-shaped vs call-shaped)
- **Trust Protocol** Surface + trust-model variations (practitioner-judgment / budget-policy / individual)
- **Time Protocol** Surface + temporal-semantics variations (turn-based / long-running / heartbeat-based)
- ~~**Phase 3.4 sparring+audit reclassified-mechanism-class sub-cluster v2-audit**~~ [resolved cluster: commits `7dfdfa5` (DR stub PROPOSED) → `69f944e` (ACCEPTED-WITH-FINDINGS) → `0d53e1e` (cascade applied) → `f327e6f` (cleanup follow-up)] — Phase 3.4 v2-audit campaign CLOSED. Per `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-4-sparring-audit.md` ACCEPTED-WITH-FINDINGS. 0 T1 + 3 T2 (audit Trust-framing reframe + §14 addition + §14-§18 renumber) + 8 T3 + 21 T4 at Wave-1; +4 T3 at cleanup pass. All 3 bundled deferred items (a)+(b)+(c) reconciled in cascade. Cross-execution pattern signal continues (4 cluster-executions; 0 T1 across all; substantive architecture survives). Substantive REVISION surfaced: audit class scope shrinks from "subsumes Trust" → "composes with authority-binding mechanism (independent framework primitive)"; per-shape trust policy lives at shape-policy declaring trust model. Authority-binding-mechanism standalone status confirmed (mechanism-level treatment in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table; no full ARCH-topic surface warranted). HANDOFF Note 54 captures full execution detail.

### 3.5 Primitive-detail topics + axis-interaction analysis

Per-primitive deeper detail; cross-cutting axis-interactions.

- ~~**specialist + skill primitive-cluster ARCH topic**~~ [resolved cluster: commits `f6bab6e` (Wave-1 Writer LOCKED) → `8ef0448` (Wave-2 Cascade applied; 11 file edits) → `c4b4992` (Wave-2.5 Cleanup; Lens 6 quad-symmetry closure)] — `arch/specialist-skill.md` LOCKED as **first canonical primitive-cluster ARCH topic**; anchors **12+5 primitive-cluster topic template** in `MAINTENANCE.md` Layer 3 NEW subsection (parallel to Pattern A 12+7; §12-as-Transport-variation-N/A-parity convention codified explicitly to prevent template drift across downstream primitive-cluster topics). Mode 2 upfront-known composite decomposition (6 sub-decisions: SD-1 template / SD-2 specialist DEFINITION 8-field manifest schema / SD-3 skill atomic + substrate Surface §G hot-activation re-binding / SD-4 Pattern B nesting + specialist-namespace + cross-specialist composition / SD-5 granularity 3-tests + two-tier classification / SD-6 marketplace deferred + destruction archival-as-default + watch-list W1-W4). Specialist-namespace mechanic Lens 6 quad-closure across 4 GLOSSARY entries (specialist + skill + work-unit + workflow composes-with rows). Cross-execution pattern continues: 0 T1 + 1 T2 + 2 T3 + 13 T4 across Wave-1 + Wave-2 audits; 5-cluster-execution methodology composability validated (INITIAL-CREATION pattern beyond v2 audit-family; Writer + Reviewer + Cascade-Writer + Cascade-Reviewer + Cleanup-Writer orchestration). DR `specialist-skill-arch-topic.md` created. Profile-cluster validation 3/3 PASS with cited content (G + L5a + L1; Clusters A + B + C + D covered). HANDOFF Note 56 captures full execution detail.
- ~~**practitioner**~~ [resolved cluster: commits 7ffe93a (Wave-1 Writer LOCKED) → e86a92f (Wave-2 cascade applied; ~10 file edits)] — arch/practitioner.md LOCKED as second canonical primitive-cluster ARCH topic; anchors Pattern C topic-template-class (12+5 extends WITHOUT variation; §8 + §13 APPLIES + §9/§10/§11 N/A documented + §12 N/A-parity = 18 sections / 375 lines). Mode 2 upfront-known composite decomposition (5 sub-decisions: SD-1 template / SD-2 bipartite + 11-field manifest schema / SD-3 multi-practitioner + legal-entity workspace context / SD-4 lifecycle + archival-as-default destruction per cross-pattern coherence with specialist-skill §13 / SD-5 authority-binding cross-axis + W1-W4). Cross-execution pattern continues: 0 T1 + 0 T2 + 3 T3 + 8 T4. DR docs/decisions/practitioner-arch-topic.md created. Profile-cluster validation 3 clusters cited (L5a + G + L1) + 1 cluster N/A documented (Cluster A practitioner-not-producer). HANDOFF Note 57 will capture full execution detail (next session start).
- ~~**workflow + work-unit primitive-cluster ARCH topic**~~ [resolved cluster: commits `3b187ea` (Wave-1 Writer LOCKED) → `b6b4ff2` (Wave-2 cascade applied; ~12 file edits)] — `arch/workflow-work-unit.md` LOCKED as **third canonical primitive-cluster ARCH topic**; anchors **two-Pattern-B topic-template-class** (12+5 primitive-cluster template extends WITHOUT variation; §8 cross-shape policy variation + §9 granularity tests + §13 per-primitive lifecycle ordering APPLY; §10 bundle / §11 marketplace N/A documented explicitly per workflow + work-unit are bundled IN specialist not bundlers themselves; §12 N/A-parity preserved = 18 sections / 482 lines). Mode 2 upfront-known composite decomposition (6 sub-decisions: SD-1 template / SD-2 4-sub-section structural overview + 4 manifest schemas (workflow DEFINITION + workflow_instance + work-unit KIND DEFINITION + work-unit instance) / SD-3 within-cluster composition + always-present asymmetry + cardinality asymmetry + ad-hoc work first-class + snapshot pattern + cross-specialist composition rules / SD-4 lifecycle ordering + 2 state machines + 8-category error catalog + cross-pattern destruction archival-as-default + orphan handling + boot integration step 9 / SD-5 two granularity 3-tests subordinate to specialist 3-test / SD-6 cross-shape policy variation 6-row matrix + cross-axis composition + W1-W4 watch-list). Cross-execution pattern continues across 7 cluster-executions: 0 T1 + 0 T2 + 1 T3 acceptable + 18 T4 CONFIRMS-LOCKED at Wave-1 audit per HANDOFF Note 57 positive pattern. DR `docs/decisions/workflow-work-unit-arch-topic.md` created. Profile-cluster validation 3 clusters cited (L1 + L5a + G; Cluster A producer + Cluster B deployer + Cluster D validator covered) + 1 cluster on-demand for Cluster C consumer per L8 future fleshing. HANDOFF Note 58 captures full execution detail.
- **workflow** representation schema + handoff semantics + multi-session continuity | archived: workflow descriptions in plugin/skills/
- **session** boundary semantics + context-handoff rules + persistent-state migration | archived: substrate-protocol-design.md
- **event** AuditEvent Pydantic shape + event_kind catalog + append-only discipline | archived: audit-trail-v2.md
- **actor** full `actor_kind` enum + A2A actor support + identity sourcing | archived: a2a-and-gemini-pattern-emulation.md, governance-and-identity-sourcing.md
- **claim** claim-event schema + claim-revision semantics + finalization mechanics + source-grounding requirements per claim + sparring-target mechanics + audit-trail attribution per work-unit | archived: audit-trail-v2.md
- **defensibility** conditions formalization + six-months-later test mechanics + regulatory-challenge schema + structural enforcement mechanisms + defensibility-on-claim-revision semantics
- **Axis-interactions explicit articulation** [origin: VISION sanity check, Lens 3] — VISION sketches axis interactions through examples (sparring within intertwining; tacked-on sparring is axis-1 failure; defensibility resolves at claim-granularity in axis-1 work-products) but doesn't articulate them systematically. Dedicated axis-interactions analysis as architectural pattern.

### 3.6 Quality-gate ARCH topic (runtime mechanism)

- **Quality-gate ARCH topic** [scope-lock complete session 16; full design Phase 3.6] — Pattern A protocol with mechanism-shaped Surface; structural variation per shape (practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-shape-gate / extensible). Scope-lock resolved: type classification (Pattern A hybrid); composition direction (composes with axes + category collapse + sparring + audit + claim + workflow_instance + session + event); per-shape variation approach (structural via Pattern A pluggability); approximate intervention shape (per-implementation combinations: friction / nudge / block / audit). **Phase 3.6 produces**: full Surface specification + per-implementation detail + per-axis-failure-mode signal catalog + intervention mechanics + error semantics + tier-awareness configuration. Prerequisites met: ✅ category collapse locked; ✅ axis-2 trio + rubber-stamping locked; ✅ scope-lock complete (Round 1 + Round 2 sharpening). Detail: `GLOSSARY.md` quality-gate entry + `docs/decisions/quality-gate-scope-lock.md` DR (original exploratory draft removed on graduation per drafts discipline).

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

This is **Checkpoint C3** in the locked audit cadence (per `DISCIPLINES.md` Discipline 9). C1 + C2 fire earlier in Phase 3 (post-3.4 + post-3.5) per below.

### Coherence-audit checkpoints in Phase 3 (per `DISCIPLINES.md` Discipline 9)

- ~~**C1: Post-Phase-3.4 close**~~ [resolved cluster: commits `5e0ae4f` (Wave 1 foundation codification) → `f571a4c` (Wave 2 framework-baseline-vs-shape-extension partition) → `4ee2ea7` (Waves 3-6 mechanical bulk cascade) → `2566eca` (Cleanup-cascade Round 2 findings)] — STABLE per HANDOFF Note 55. Density 27 → 8 → 0 across 3 audit rounds. 6 substantive architectural commitments locked: Pattern D codification + Pattern A/mechanism-class topic template rename + NEW `authority-binding` GLOSSARY entry + `arch/substrate.md` §E event-bus extension + `ARCHITECTURE.md` §6 composite boot subsection + framework-baseline-vs-shape-extension partition. 30+ mechanical cleanups across 4 cascade commits. Phase 3.5 + 3.6 unblocked; C2 fires post-Phase-3.5 close per Discipline 9 cadence.
- **C2: Post-Phase-3.5 close** [scheduled this commit] — full corpus-set audit after 4 primitive cluster + 2 cross-cutting integrator topics locked. Validates primitive clusters compose cleanly with Pattern A protocols + cross-cutting integrators surface no gaps. 10 universal lenses; early indicators of Lens 11-12.
- **C3: Phase 3.8 phase-boundary** (above) — ARCH-specific Lenses 11-15 activate; comprehensive corpus-set audit before Phase 4 starts.

---

## Phase 4 — Decision Records (selective)

### Open

- **DR coverage gap** items — surface from Lens 14 audit; capture decisions that need standalone DR (vs ARCH-embedded)

### Coherence-audit checkpoint in Phase 4 (per `DISCIPLINES.md` Discipline 9)

Phase 4 close audit subsumed into C4 (Phase 6 pre-implementation) per cadence rationale: ROADMAP + spec planning audit together at Phase 6 pre-implementation; separate Phase 4 close audit not warranted unless 5+ DR trigger fires mid-Phase-4 (per Discipline 9 trigger conditions). Lens 16 (decision-linkage / constraint-flow tracking) activates within C4.

---

## Phase 5 — ROADMAP rebuild

### Open

- **AI-app-development-facilitation skill** [HIGH priority per user direction session 16] — captures cross-project discipline for building AI-centric apps; transferable to other AI-app projects. Consumes accumulated observations from `learnings/` folder. Per user: "should be our first ROADMAP item even though we will have many items that come before it."
- **`learnings/` distillation** — when per-session entries accumulate stable patterns (typically 3-5 sessions of evidence), distill into structured topic-specific docs in `learnings/`; promote held observations to memory feedback rules / DRs / ARCH disciplines as appropriate. Feeds into the AI-app-development skill above.
- **Testing harness for the framework** — eventual harness for systematic testing of framework primitives (mechanisms, protocols, shape conformance, sparring-output validation, audit-emission correctness). Composes with PydanticAI eval framework if adopted (per Phase 3 #7). Distinct from per-skill testing; this is harness for the framework layer itself.
- **Markdown structure validation (investigation + adoption)** — investigate (a) existing libraries for markdown structural validation (frontmatter conformance, required-sections-present, cross-ref existence, schema-of-allowed-tag-values); (b) what we already had in archived code (`backend/mcp-server/` + `plugin/skills/{audit,design-review}/`). Composes with Phase 3 #8.
- **Multi-tenant federation practitioner identity** [origin: arch/practitioner.md W1] — when workspace federation surfaces (Tier 3 cross-org per archived `governance-and-identity-sourcing.md` decision 1 OR `arch/audit.md` §15 federated audit-trail watch fires), cross-org practitioner-identity binding mechanism design (federated authority chain across workspaces); awaits second-deployment cross-org evidence | refs: `arch/practitioner.md` §14 W1
- **Cross-practitioner workflow handoff mechanics + per-shape policy variation** [origin: arch/practitioner.md W4] — second multi-practitioner deployment surfacing per-shape friction (single-practitioner pioneer doesn't surface handoff); per-shape policy declares handoff mechanics (explicit-named vs auto-route vs queued) | refs: `arch/practitioner.md` §14 W4
- **Workflow_pattern primitive vs Layer A reusable templates** [origin: arch/workflow-work-unit.md W1] — when ≥2 specialists develop genuinely-cross-archetype workflow pattern that Layer A growth proves insufficient for, examine workflow_pattern framework primitive elevation; cross-link to existing Phase 3.7 "Cross-specialist shared workflow patterns insufficient via Layer A" entry if applicable | refs: `arch/workflow-work-unit.md` W1
- **Cross-practitioner workflow handoff mechanics** [origin: arch/workflow-work-unit.md W2 + arch/practitioner.md W4 composition] — when second multi-practitioner deployment surface emerges, design `workflow_handoff` event-kind shape + attribution chain preservation rules + per-shape required-handoff-recipient enforcement; cross-link to `arch/practitioner.md` W4 (same awaited-signal) | refs: `arch/workflow-work-unit.md` W2 + `arch/practitioner.md` W4
- **Multi-workflow_instance phase choreography mechanics** [origin: arch/workflow-work-unit.md W4] — when second workspace deploys multi-workflow_instance against single work-unit pattern, design per-workflow phase coordination semantics + cross-specialist phase ordering; cross-link to `arch/specialist-skill.md` §10 cross-specialist composition rules | refs: `arch/workflow-work-unit.md` W4

### Open — Shape-neutrality validation for second-shape productization

- **Shape-neutrality stress-test for non-practitioner shapes** [origin: session 16 retrospective audit, GAP 1] — current GLOSSARY primitives have practitioner-shape-anchored framing (practitioner; intertwining/sparring/authorship axes; defensibility; failure modes including rubber-stamping). Profile L5e autonomous-business-operator + L5f personal-OS-knowledge-worker stress-test shape-neutrality: framings need shape-policy variants when second shape gets productized (axis-3 N/A or redefined for autonomous-business; defensibility shape varies; failure modes anchored differently). D-gate-validated: this is GENUINE awaited-evidence gap (mental modeling resolves SHAPE-POLICY-VARIATION pattern but specific shape-policy details await second-shape design). Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 no-defer principle: not a primitive-level revision needed today; framework primitives stay shape-neutral; shape primitive's policy bundle handles per-shape variation; **awaited signal**: second-shape design begins (autonomous-business OR personal-OS productization). Resolution at signal: validate primitive framings + new shape's policies handle the variations cleanly. Watch-list mechanism: track which primitives need shape-policy variants when second shape lands.

### Open — Composability tooling

- **Composability tooling — CLI / validators / linters enforcing packaging boundaries** [origin: session 16, profiles + composability discipline work] — tooling that makes packaging boundaries STRUCTURAL (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1): specialist self-containment validator; shape composition validator; deployment template composition validator; workspace serializer / deserializer; audit-trail integrity verifier across migration; license + provenance verification; cross-substrate / cross-shape compatibility checkers. Not blocking framework lock; emerges as framework matures + first non-pioneer deployments surface integration friction. Anchored to L1-L4 producer profiles + G composability gate per `profiles/`. Detail in `drafts/composability-tooling.md`. Trigger for graduation: Phase 5 ROADMAP identifies as ship-target OR first non-pioneer deployment surfaces packaging friction OR Phase 6 specs need concrete tooling to enforce contracts.

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
- **Adapter-mode practitioner-RECORD + Identity-class adapter Surface candidate** [origin: arch/practitioner.md W2 + adapter §3 framework-baseline-vs-shape-extension partition pattern] — concrete adapter implementation per Personio / Microsoft Entra / Coolify SSO will surface 6th-class candidate for `arch/adapter.md` §3 partition (currently 5 classes: Email / Accounting / MCP-Server / A2A-Peer / File-Sync); per archived `governance-and-identity-sourcing.md` decision 2 native-vs-adapter mode pattern | refs: `arch/practitioner.md` §14 W2 + `arch/adapter.md` §3
- **Practitioner-record signing mechanism for historic-claim defensibility** [origin: arch/practitioner.md W3] — Phase 6 audit `arch/audit.md` §D integrity verification + cryptographic-signature implementation; cryptographic chain mechanism (parallel to archived `audit-trail-v2.md` `convention_applied` field with `git_sha` precedent extended to per-claim signature) | refs: `arch/practitioner.md` §14 W3 + `arch/audit.md` §D
- **Per-kind structural conventions schema standardization** [origin: arch/workflow-work-unit.md W3] — when ≥3 kinds across specialists develop divergent artifact-attachment shapes warranting standardization, design per-kind structural conventions schema (work-unit kind manifest extension via `artifact_attachment_shape` field standardization) | refs: `arch/workflow-work-unit.md` W3
- **Workflow_instance suspension state implementation** [origin: arch/workflow-work-unit.md §13 state machine] — Phase 6 implementation of `suspended` state semantics + `suspended` → `running` resume transition + `suspended` → `abandoned` cancel transition; persistence mechanics per `arch/substrate.md` §F session/context management | refs: `arch/workflow-work-unit.md` §13 + `arch/substrate.md` §F
- **Work-unit instance pivot mechanics implementation** [origin: arch/workflow-work-unit.md §13 + R-CC-4 work_unit_pivoted event-kind] — Phase 6 implementation of `work_unit_pivoted` event emission + `predecessor_work_unit_id` linking (per `details:` payload pattern); integrates with `arch/audit.md` §A emission API + audit-trail attribution chain preservation per axis-3 defensibility | refs: `arch/workflow-work-unit.md` §13 + `arch/audit.md` §A

### Coherence-audit checkpoints in Phase 6 (per `DISCIPLINES.md` Discipline 9)

- **C4: Phase 6 pre-implementation** [scheduled this commit] — architectural-validation pass before implementation work begins. Per `pre-implementation-sharpening` skill timing. Catches architectural drift accumulated across Phase 4-5 specs/code planning. 10 universal lenses + Lens 17 (schema completeness) for Phase 6 spec-set.
- **C5: Post-Phase-6 close** [scheduled this commit] — final audit before stability lock + promotion to higher-classification. Full corpus including specs + code. 10 universal lenses + Lens 18 (spec/impl divergence) activates.

---

## Cross-cutting (any phase)

### Open

- **Plugin manifest description rewrite** [origin: session 16 dev-skill restoration] — `plugin/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` descriptions are neutral placeholder; full positioning rewrite when framework-distribution mechanics surface (Phase 3+)
- **Sharpening skills global plugin elevation** (#23 from archived ROADMAP) — promote `decision-design-sharpening` + `pre-implementation-sharpening` + `coherence-audit` to a global plugin so other AI-app projects can use them
- **3-tier REVISION/EXPANSION discriminator codification** [origin: session 16 toolkit-review pre-Phase-3.2] — current 2-tier (REVISION ~30% / EXPANSION ~70%) works empirically through Phase 3.1 with 0 architectural drift attributable to ambiguity. ~3 borderline cases this session (vocabulary disambiguation; Lens-6 reciprocal additions; always-present container elevation) suggest a possible Tier 2 (Structural EXPANSION) between REVISION + Coverage EXPANSION, distinguished by cascade-workflow (Tier 1 = decision-reopen + full cascade; Tier 2 = local cascade required for cross-entry reciprocals/elevations; Tier 3 = no cascade in-entry). **Awaited signal**: ≥3 borderline classifications across consecutive decisions/audits OR user pushback that classifications feel under-precise OR cascade-work-lag (Lens-6-style reciprocal gaps caught at audit-time that should have been caught at sharpening-time). **Detection mechanisms in place** (per `decision-design-sharpening` v0.6.0 + `coherence-audit` v0.3.1): self-check question at Round 2 termination + audit Step 7 asks "Any EXPANSION reclassifiable as REVISION on second look?" **At signal**: codify 3-tier (or alternative shape — accumulated cases may suggest different cuts than 3) with cascade-workflow-per-tier mapping. **Until then**: 2-tier + Pareto + LOAD-BEARING-lens discrimination sufficient. Per D-gate-logic-transposed-to-toolkit-level: real cases shape eventual codification better than anticipatory analysis. **Cumulative count update post-workflow-work-unit cluster (commit `3b187ea`)**: 4 REVISION-flavored EXPANSIONS across 3 cluster-executions (specialist-skill = 2 + practitioner = 1 + workflow-work-unit = 1). **Trip threshold for cumulative-count signal REACHED (4 ≥ 3)** but USER pushback / cascade-work-lag signals NOT yet materialized per skill detection mechanisms. Continue 2-tier within current composite; flag for Coherence-audit C2 evaluation post-Phase-3.5 close per `disciplines/09-coherence-audit-cadence.md`.

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
