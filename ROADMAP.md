# pbs-bureau roadmap

Deferred feature backlog. Each item is "designed enough to know it
matters but not yet specified in detail." Pick up in priority order
when the system is ready or when a real project needs the feature.

For session-state (what's done vs in-progress), see `HANDOFF.md`.
For taxonomy + decision rules, see `ARCHITECTURE.md`.

---

## v1.x — likely soon

### Generalize + publish domain-agnostic skills as separate plugin(s)

**Confirmed scope (primary)**: `audit` + `design-review` skills.
These two are the most clearly domain-agnostic in the plugin —
they review architecture / code / docs / decision records, not
planning law or B-Plan content. Both are battle-tested as the
session-by-session quality framework here; they generalize
unchanged to any knowledge-work plugin domain (legal practice,
research-paper review, engineering-doc workflows, etc.).

- `audit` — drift detection framework with slice-based
  composition. Today's slices reference some PBS-specific
  surfaces (manifests, bausteine) but the frame is generic; the
  domain-specific slices can stay here while the generic ones
  extract.
- `design-review` — first-principles soundness review with
  anti-bias mechanism. Targets 1-9 are domain-flavored in
  examples but the method (greenfield reframe, anti-status-quo
  bias, subsumption check) is generic.

**Under consideration (secondary, not committed)**: several other
skills + infrastructure could plausibly extract too — but the
priority needs empirical battle-test before committing to the
split. Listed for future evaluation, not for the first
extraction:

- `watch-list` — six-trigger continuous-watch infrastructure
  + four-way decision menu. Pattern looks generic; needs
  validation across domains before claiming it.
- Memory-record pattern (`save-baustein` / `record-feedback` /
  `validate-bausteine`) — "baustein" maps to "snippet" / "pattern"
  / "case" in other domains, but the invalidation-contract shape
  may differ enough to make a generic core leak abstractions.
- `orchestrator` infrastructure (meta-rule-4 enforcement,
  list_skills introspection, phase-routing) — likely generic, but
  the orchestrator currently encodes PBS-specific phase model
  (Phase A drafting / Phase B review / Phase C send). The
  *framework* extracts; the *phase model* doesn't.
- `promote-to-skill` — graduation-from-memory pattern. Tightly
  coupled to the memory-record pattern; extract together or
  not at all.
- Backend infrastructure — `pbs_core/`-style plain-Python +
  `pbs_mcp/`-style thin MCP wrappers; StrictModel + fail-closed
  discipline. Likely PyPI-package material once the API stabilizes.

**Domain-coupled (stays here unconditionally)**: `draft-textteil-b/c`,
`draft-cover-mail`, `validate-checklist`, `validate-latex-style`,
`verify-citations`, `research-references`, `survey-project`,
`setup-office`, `author-manifest`. These encode planning-bureau
domain knowledge.

**Sketch of the primary extraction (audit + design-review only)**:

- A new repo (working name TBD — `claude-plugin-meta-review` or
  similar) hosting just these two skills + their references
  + minimal backend dependencies (StrictModel, list_skills tool).
- pbs-bureau becomes a *consumer* of that base plugin via plugin
  install/dependency, adding only PBS-specific slices/targets
  on top of the generic frame.
- Versioning: the generic plugin evolves on its own track; PBS
  declares a version dependency.

**Pull-forward trigger**: after first ~3-5 real PBS projects have
exercised audit + design-review on real review cycles enough to
empirically validate that the generic / PBS-specific split holds.
Don't extract prematurely — extracting before battle-test risks
splitting in the wrong place.

**Decision needed before extraction**:

- Whether the secondary candidates extract together with audit +
  design-review, or in a later separate pass, or not at all.
  Today's instinct: separate later pass once empirical evidence
  accumulates. But interesting enough to keep the option open.

**Open questions** (defer until extraction window opens):

- Naming + scope of the extracted plugin(s).
- Backend infrastructure split: PyPI package vs vendoring?
- Test surface: how does a meta-review plugin test itself without
  a domain to review? Likely with a stub reference domain.

### Tier 2 MCP cross-reference tools — pulled forward to v1 (session 11)

**Status**: `find_bausteine_by_reference` landed in session 4 (see
`backend/mcp-server/src/pbs_mcp/tools/memory.py`). Remaining two
tools below pulled forward from v1.x to v1 pre-launch under
sharp-defer audit (session 11) — framework cross-reference
infrastructure for any consulting deployment at first bind. Bundle
with **#7 (bootstrap-write MCP tools)** since both extend the
MCP tool surface for contract-bearing files.

**Why**: When `research-references` updates a law and needs to
find every dependent baustein and memory doc, the cross-reference
graph must be complete — partial coverage produces silent gaps.

**Sketch (remaining)**:

- `find_memory_docs_by_reference(...)` — cross-cutting memory docs
  declaring `references_used[]` frontmatter.
- `find_manifest_entry(id)` — single-entry lookup across the
  union of in-scope manifests.

> **Tier 1 MCP discovery layer** (`list_reference_manifests`,
> `list_doctypes_manifests`, `list_skills`, `list_skeletons`,
> `list_bausteine`) landed in session 4 — see
> `backend/mcp-server/src/pbs_mcp/tools/discovery.py` and
> `tools/memory.py`. Removed from this ROADMAP per "Tracking
> conventions" rule.

### Tier 3 MCP introspection tools — pulled forward to v1 (session 11)

**Why**: Skills currently know office-config schema field paths
(`office_config.office.signature_block` etc.); changes to schema
ripple through every skill. Same for per-project state queries
that today are file-grep. Schema introspection is framework
infrastructure for any deployment — pulled forward from v1.x to
v1 pre-launch under sharp-defer audit (session 11). Bundle with
**#7 (bootstrap-write MCP tools)** since both are MCP-tool-layer
work.

**Sketch**:

- `get_active_practices()`, `get_signature_block(practice?)`,
  `get_office_identity()` — schema introspection helpers.
- `get_project_state(project)`, `list_snapshots(project)`,
  `list_correspondence(project, since?)`, `list_decisions(project)`
  — per-project state queries.
- `list_office_style_overlays()` — returns the active `.sty`
  stack per active domains.

### Schema migration framework for memory data records — pulled forward to v1 (session 11)

**Why**: Office-config has migrations
(`office_config_migrations/v<N>_to_v<N+1>.py`) that forward-migrate
on load. Memory (record) entities (bausteine, manifests' entries,
state.md, feedback entries) have no equivalent. Consulting clients
save bausteine from day one; framework needs migration support
ready at first bind. Pulled forward from v1.x to v1 pre-launch
under sharp-defer audit (session 11). Bundle with **#9 (entity
gate)** — the entity gate IS the migration boundary (every
read/write through `read_entity`/`write_entity` is a natural
migration application point).

**Sketch**:
- Mirror the office-config pattern: `pbs_core/memory_migrations/`
  per-record-kind (bausteine, manifests, state, feedback) with
  `migrate_v<N>_to_v<N+1>(data: dict) -> dict` exporters.
- Each record type carries `schema_version: <N>` in frontmatter
  (Layer 1 universal field per #16 hybrid-shape contract).
- The generic entity gate from #9 (`read_entity`) checks
  `schema_version` on read and applies migrations in-memory;
  `write_entity` writes back with updated version.
- `setup-office` reconcile mode triggers a sweep migration of
  all in-scope records.
- Decision-rule update in ARCHITECTURE.md: Memory (record) edits
  go through the generic entity gate which handles migration;
  never direct Edit.

### Boundary placement refinements (from slice 14, 2026-04-29) — pulled forward to v1 (session 11)

**Why**: Audit slice 14's first run flagged 3 placement findings —
deterministic logic that should move from skills into MCP tools,
or from hardcoded Python into office-config. Pulled forward from
v1.x to v1 pre-launch under sharp-defer audit (session 11): each
gap is real framework infrastructure for any consulting deployment;
the prior "honestly defer-worthy (requires schema + handler +
tests)" rationale was up-front-cost framing, not a chronological
defer. Bundle with **#6 (audit-trail v2 retrofit)** — both items
touch baustein frontmatter, single retrofit pass over save-baustein
+ record-feedback skills. See full audit at
`docs/audits/boundary-adherence-20260429.md`.

The middle item (path_classification) was landed in-session as a
purely-additive v3 optional block (no schema bump). Two remaining
items below pulled forward.

**Sketch — two independent items**:

- **`dedupe_bausteine` MCP tool**: dedupe procedure currently
  described in `save-baustein/SKILL.md` lines 65-75 (title + tag
  overlap matching). Move algorithm into MCP tool with reproducible
  scoring rule + Pydantic candidate output schema. Phase-2 (HyDE
  paraphrase search via search_corpus over indexed bausteine)
  becomes its own iteration when corpus indexing lands.

- **`record_baustein_use` MCP tool**: `record-feedback/SKILL.md`
  lines 117-120 directs direct `Edit` of baustein frontmatter
  fields `rejected_uses[]` / `successful_uses[]`. Skill itself
  flags this as known debt. Build the tool: takes baustein name +
  scope/key + kind ∈ {rejected, successful} +
  project/date/feedback_path, owns frontmatter mutation with
  validation.

### Manifest Pydantic models (from slice 15, 2026-04-29) — pulled forward to v1 (session 11)

**Why**: Audit slice 15's first run found that manifest YAMLs
(references-manifest.yaml, doctypes.yaml) carry their meta-rule-3
invalidation contracts (top-level `last_updated`, per-entry
`last_fetched`, `checksum_sha256`) by author discipline only —
no Pydantic model validates the structure at parse time. Manifest
validation is framework infrastructure for any consulting
deployment; pulled forward from v1.x to v1 pre-launch under
sharp-defer audit (session 11). Bundle with **#9 (entity gate)** —
post-#16 hybrid-shape, manifests migrate to per-entity md files
and the generic entity gate IS the manifest validator (Layer 1 +
Layer 2 frontmatter Pydantic dispatch).

See full analysis at
`docs/audits/invalidation-contract-20260429.md` finding F1.

**Sketch**:

- Per #16 hybrid-shape contract, manifest entries become per-entity
  md files (e.g., `extensions/universal/references/<id>.md`) with
  Layer 2 type-specific Pydantic subclass (`ReferenceEntity`,
  `DoctypeEntity`). The entity gate from #9 validates at every
  read/write.
- Top-level manifest fields (`version`, `scope`, `scope_key`,
  `last_updated`, `maintainer`) become frontmatter fields on a
  per-scope `manifest.md` registration file (parallel to
  `department.md` from #9 Bundle A) OR fold into existing
  registration files.
- `validate_manifest(path) → list[Finding]` MCP tool layered on
  the entity gate for explicit validation calls.
- Discovery tool's `ManifestInfo` response schema stays Optional
  on contract fields — graceful failure reporting; validation is
  the gate's responsibility.

### 🚧 PRE-RAG QUEUE — current order (locked session 14)

**Locked order** (per session 14 reorder):

| # | Step | Commitment | Why this position |
|---|---|---|---|
| 1 | DESIGN | **#25** Shape extension framework + Option B floor | Architectural foundation; locks shape extension contract + Option B 3-axiom structural floor; downstream Bundle design + #11 + #24 inherit |
| 2 | EVAL | **#20** PydanticAI evaluation | Informs Bundle B Layer-3 mechanism choice (Option A: Pydantic subclass / Option B: declared extra_fields / Option C: metadata dict) — placed BEFORE Bundles to lock Layer-3 naturally without provisional annotation |
| 3 | DESIGN | **Bundles B/C/D/E** (#9 design) | Inherits #25 shape model; Layer-3 mechanism locked by #20 result |
| 4 | IMPLEMENT | **#11** Cowork integration | Implements #25 + #9 designs; specialist primitive operational in Cowork plugin shape; 19 skills frontmatter sweep; slash command namespacing |
| 5 | IMPLEMENT | **#24** EU AI Act + DACH compliance specialist | HARD REQUIREMENT before Aug 2026 production B-Plan; needs #11 (specialist operational) + #25 (Option B floor active) |
| 6 | EVAL | **#19** LlamaIndex pluggable RAG eval + memory adapters (Mem0/Zep/Graphiti/Cognee) | Last in pre-RAG queue; informs Phase 1 corpus + Memory Bank shape; can wait until corpus shape needs to lock |

**After pre-RAG queue**: #15 (Client + Actor) → #6 (audit-trail v2 retrofit) → #7 (bootstrap-write) → #17 (MCP gate coverage) → #13 (deployment flexibility / Coolify) → #8 (pre-action framing skill) → C (sparring-output integration) → D (plugin version bump) → Phase 0 + Phase 1.

### Historical context — BLOCKING SUBSTRATE EVALUATIONS (added session 11; reordered session 14)

Three substrate-framework evaluations originally BLOCKING for #9 implementation
phase + #11 + #13 + Phase 1 corpus + all downstream code work.
Surfaced session 11. **#18 + #21 SHIPPED session 12** (Claude Agent SDK + MS AF dual-substrate adopted). #19 + #20 reordered session 14 — see queue table above. Original ordering rationale below for historical reference.

**Why originally blocking**: substrate choice (orchestration runtime + RAG
primitives + typed agent abstraction) influences the Python
implementation of every downstream pre-RAG commitment. Doing the
evaluations after locking implementation choices means
retrofitting under sunk-cost pressure.

**What can proceed in parallel** (substrate-agnostic): Bundles
B + C + D + E design work (entity gate signatures, Pydantic
schema shapes, body-preservation contracts, Layer 3 mechanism
options, ProjectEntity migration plan). Pure design doesn't
depend on substrate. **Per session-14 reorder: #20 happens BEFORE Bundle design to lock Layer-3 naturally.**

**Original order** (session 11; superseded session 14): #18 (MS AF) first; #19 (LlamaIndex) second; #20 (PydanticAI) third. **Session 14 reorder above is current.**

**18. Agentic framework substrate evaluation (multi-framework)**
(BLOCKING) — session 11 commitment.

- **Mission**: full investigation of agentic framework substrate
  candidates for orchestration / agent runtime / transport /
  observability. NOT adapter-level wrapping; substrate-level
  evaluation. Determines whether we build #9 entity gate Python
  implementation + #11 plugin agents + #13 transport on top of
  an agentic framework substrate or hand-rolled. Multi-framework
  evaluation; not MS-AF-only.
- **Frameworks in scope** (bucketed by category for meaningful
  comparison; compare WITHIN buckets, then ACROSS buckets per
  deployment scale needs):

  | Bucket | Frameworks | Note |
  |---|---|---|
  | **Enterprise-grade** (production-ready, observability built-in, mature) | MS Agent Framework, Semantic Kernel, AutoGen | Best fit for Tier 3 / Gemini-Enterprise scale; may be overkill for 1-person shop |
  | **Mid-weight** (popular community, common-case primitives) | LangGraph, CrewAI | Tier 2 cloud + small/medium-company sweet spot |
  | **Lightweight** (intentionally minimal abstraction, low-overhead) | Smolagents (HuggingFace), OpenAI Swarm/Agents SDK | Best fit for 1-person shop / single-skill-utility deployment shapes |
  | **Hand-rolled** (current default) | Raw Python + MCP + Pydantic | Comparison baseline; lowest cognitive + operational overhead |
- **Heaviness as a key evaluation dimension** (per session-11 user
  direction). Heaviness has TWO sub-axes that must be evaluated
  separately because frameworks vary differently along each:

  - **Operational heaviness** — boot time, memory footprint,
    runtime deps, observability cost when nobody's watching,
    deployment complexity. Easily measured.
  - **Cognitive heaviness** — how much framework-specific
    abstractions a developer must learn before being productive.
    CrewAI's "agents+crews+tasks" mental model is one shape;
    LangGraph's "state machine" another; raw Python+MCP near zero.
    Harder to measure but real (especially for 1-person shops where
    the user IS the developer + the operator).

  The substrate must serve our consulting business spectrum from
  1-person shops → small companies → enterprise (Tier 3 / Gemini
  Enterprise). For each candidate, evaluate BOTH sub-axes at each
  scale:

  - **1-person shop deployment** (Gunther's PBS today; future
    single-skill-utility shapes like brand-voice): does the
    framework add substantial operational overhead? Substantial
    cognitive overhead the user would have to absorb?
  - **Small company deployment** (5-20 person consulting client
    on Tier 2 cloud): does the framework's overhead feel
    proportional? Does it expose primitives the small office
    will use (multi-user, audit, basic governance) without
    forcing enterprise-grade complexity?
  - **Enterprise deployment** (100+ users, Tier 3 / Gemini
    Enterprise): does the framework expose primitives that
    enterprise needs (federated identity, multi-agent A2A,
    formal observability, regulatory governance)?
  - **Does the heaviness scale automatically?** Some frameworks
    may have configuration-driven scaling (lightweight defaults,
    opt-in to enterprise primitives). Others may require
    enterprise-grade deps regardless of deployment size. Critical
    for the consulting product positioning ("from solo
    practitioner to enterprise on the same architecture").

- **Scope-creep guard** (added session 11 ultrathink-review): the
  evaluation is time-boxed (2-3 sessions). Decisions made with
  available evidence after time-box; further investigation deferred
  ONLY with chronological reason ("framework X just shipped a major
  release that changes the gap analysis" qualifies; "we should also
  consider framework Y in similar bucket" does not — pick the
  representative within bucket, not exhaustive enumeration).
- **What an agentic framework would substrate** (any candidate):
  - Plugin-agent execution model (per #11 — currently undefined;
    we'd build it)
  - Multi-agent coordination patterns
  - Observability
  - A2A interop (varies per framework — MS AF native; others
    adapter)
- **What survives substrate change** (architectural commitments,
  documentation — substrate-agnostic):
  - All ARCH disciplines (eight + meta-rules + reference card +
    validation-gating-overview)
  - VISION axes (sparring + authorship — implementable on any
    substrate)
  - entity-md spec, scope orthogonality, audit-trail v2 schemas
  - MCP integration (multiple frameworks support MCP servers;
    composes)
- **Concrete read needed per candidate**:
  - **Prompt model**: does it assume prompts-as-template, or is
    it agnostic about prompt provenance? Critical for
    AI-as-runtime hybrid-shape (markdown bodies as runtime fuel)
  - **State model**: composes with our scope-orthogonality?
  - **Pydantic / typing alignment**
  - **MCP integration shape**
  - **Anthropic ecosystem alignment** (Claude Code dev runtime +
    Cowork end-user runtime — does the framework compose or add
    friction?)
  - **Lock-in risk** (vendor neutrality)
  - **Heaviness profile** (per scale tier above)
  - **Observability integration cost**
  - **Community + churn risk** (LangGraph wider community but
    LangChain churn; MS AF Microsoft-maintained; CrewAI smaller;
    etc.)
- **Future-roadmap items the eval MUST consider** (added session 11):
  - **Time-driven triggers (Gap A from #12 infrastructure-primitive
    review)**: framework must compose with server-side scheduler
    firing "tick" events on schedule. Per #13 deployment flexibility:
    `register_scheduled_trigger(condition, event_kind, cadence)` MCP
    tool extends event sources from "skill-emitted only" to "skill-
    emitted + time-emitted." Load-bearing for proactive deadline
    warnings, scheduled report generation, automatic Fristverlängerung
    filing. Tier 2 cloud naturally hosts the scheduler. Substrate
    candidates that don't compose with scheduled-trigger pattern OR
    impose a competing scheduler abstraction → friction or rejection.
  - **Event-driven adapter callbacks (Gap B from #12 infrastructure-
    primitive review)**: framework must support adapter Protocol's
    `subscribe_to_changes(callback)` (push) OR `poll_for_changes() ->
    list[Event]` (pull) per #9 Bundle E (restored from #11 deferral
    per session-11 sharp-defer audit). External state changes
    (Lexware webhook on invoice paid; Harvest external timesheet
    edit; calendar adapter on new meeting) translate to native
    AuditEvents with `actor_kind=external_agent` +
    `origin_agent_card=<adapter URL>` per #10's existing design.
    Substrate candidates that can't compose with adapter callback
    pattern → friction or rejection.
  - **Both items together** define the framework's future-event-
    handling surface. Substrate evaluated for both today + future
    fits, not just current synchronous request-response patterns.
- **Output**: `docs/decisions/substrate-agentic-framework.md` —
  multi-framework comparative table + per-candidate gap
  analysis + heaviness scaling assessment + adoption cost
  estimate + decision (adopt one / reject all / partial /
  primitives-only adoption from one or more).
- **Scope**: 2-3 sessions (broader than initial 1-2 estimate
  given multi-framework scope).
- **Order**: position 1 in pre-RAG queue. Before Bundles B-D-E
  design can lock implementation-relevant decisions; before #9
  implementation phase.
- **Constraints flowing if a substrate is adopted**:
  - #9 entity gate Python implementation built on chosen
    framework's agent primitives
  - #11 plugin agents use framework's agent shape
  - #13 transport uses framework's observability + transport
    abstractions
  - #10 A2A interop partially obtained by adoption (varies per
    framework)
- **Constraints flowing if all rejected** (hand-rolled stays):
  - Confirms hand-rolled substrate; decision record documents
    why per-framework didn't fit (anti-cargo-cult anchor for
    future sessions)
  - May surface specific primitives worth adopting at adapter
    level (e.g., MS AF observability, LangGraph state-machine
    primitives) without substrate adoption

**19. LlamaIndex pluggable RAG evaluation** (BLOCKING for Phase 1
corpus) — session 11 commitment.

- **Mission**: investigate LlamaIndex's RAG primitives for pluggable
  adoption (NOT all-or-nothing substrate replacement). Specifically:
  which primitives plug in to replace handbuild stack, which we
  keep custom, performance comparison.
- **Pluggable framing per user direction**: the question is NOT
  "adopt LlamaIndex as substrate" but "which specific primitives
  plug in?" Primitives-by-primitive evaluation:
  - Document parsers (PDF, web-text, HTML) — pluggable candidate
  - Chunkers (per-paragraph for laws, per-section for narrative) —
    pluggable candidate; LlamaIndex supports custom chunking
  - Vector store wrappers (LanceDB has a LlamaIndex integration) —
    pluggable; we'd use LanceDB regardless
  - Hybrid retrieval (BM25 + vector + reranking) — pluggable
    candidate
  - Query engines (composable retrieval pipelines) — pluggable
    candidate
  - Citation / source-tracking primitives — pluggable candidate
  - Per-reference Pydantic metadata model — KEEP CUSTOM (entity-md
    based; tied to our entity model)
  - Citation traceability tied to entity model — KEEP CUSTOM
  - Per-#13 ingestion-vs-serving split — KEEP CUSTOM (deployment
    architecture, not RAG-pipeline concern)
- **Concrete read needed**:
  - Performance comparison: LlamaIndex retrieval pipeline vs
    handbuild for our use cases (German legal text, multilingual,
    per-paragraph chunking)
  - Stability + churn: LlamaIndex has had churn but more stable
    than LangChain — concrete read
  - Plugability: can we use LlamaIndex parsers + chunkers WITHOUT
    adopting LlamaIndex's metadata + entity model?
  - Specific primitives: which save real engineering vs duplicate
    what we already have
- **Output**: `docs/decisions/rag-stack-llamaindex.md` — per-primitive
  evaluation + pluggable boundary + adoption recommendations +
  performance read + decision.
- **Scope**: 1-2 sessions.
- **Order (updated session 14)**: **POSITION 6 (LAST) in pre-RAG queue**
  — after #25 design + #20 + Bundles + #11 + #24 implementation. Scope
  EXTENDED session 14 to also include memory adapter evaluation (Mem0 /
  Zep / Graphiti / Cognee) — same architectural question (build vs
  adopt vs pluggable). Before Phase 1 corpus download (corpus shape +
  memory shape get locked once entries are processed).
- **Constraints flowing if pluggable adoption**:
  - Phase 1 corpus pipeline uses LlamaIndex for parsers + chunkers +
    retrieval
  - Per-reference metadata + citation traceability remain custom
  - LanceDB integration via LlamaIndex's wrapper

**20. PydanticAI evaluation** (NOT BLOCKING for general
implementation; evaluate before Bundle B Layer-3 mechanism decision
specifically) — session 11 commitment, demoted from BLOCKING tier
under session-11 ultrathink-review.

**Why demoted from BLOCKING**: PydanticAI's win surface is
genuinely narrower than #18/#19 (typed agent calls + sparring-output
validation + Layer 3 mechanism). Not adopting it doesn't gate
implementation work in #9/#11/#13 broadly; only gates the Bundle B
Layer-3 mechanism decision (which #20 might inform). Listing as
BLOCKING alongside #18/#19 (substrate-altering at scale) was
over-weighted.

- **Mission**: investigate PydanticAI as substrate for typed agent
  surfaces (skill output validation, Layer 3 mechanism implementation,
  any future typed multi-step agent calls). Determine whether
  adoption now is future-ready leverage or premature substrate cost.
- **Concrete read needed**:
  - PydanticAI's typed agent call abstraction vs our skill +
    MCP tool model (skills orchestrate; MCP tools are typed Pydantic;
    is there a real gap PydanticAI fills?)
  - Sparring-output validation: could PydanticAI replace
    `validate_skill_output` MCP tool? What's the win?
  - Layer 3 mechanism: could PydanticAI's typed extra-fields shape
    inform Layer 3 Option A (Pydantic subclass per deployment)?
  - Future v2 builder: PydanticAI for typed multi-step reasoning in
    the office-builder?
- **Output**: `docs/decisions/substrate-pydantic-ai.md` — gap
  analysis + win surface + decision (adopt now / adopt at v2 /
  reject).
- **Scope**: 1 session.
- **Order (updated session 14)**: **POSITION 2 in pre-RAG queue** —
  after #25 design (architectural foundation), BEFORE Bundles B/C/D/E
  design. Promoted from session-11 "before Bundle B Layer-3 mechanism
  decision specifically" to "before all Bundle design" — preserves
  #20-informs-Bundle-B-Layer-3 dependency naturally without provisional
  annotation. Earlier than v2 because evaluating now lets us be
  future-ready if adopted.
- **Constraints flowing if adopted**:
  - Skill output validation rebuilt on PydanticAI
  - Layer 3 mechanism may shift toward Option A (Pydantic subclass)
    if PydanticAI makes that ergonomic
  - Future v2 builder uses PydanticAI for typed reasoning
- **Constraints flowing if rejected/deferred**:
  - Confirms current sparring-output pattern; existing
    `validate_skill_output` stays
  - Layer 3 mechanism decided on its own merits

**21. SDK deep-read — Claude Agent SDK + MS Agent Framework code analysis**
(NEAR-BLOCKING for #9 implementation phase) — session 12 commitment, scaffolded.

- **Mission**: clone both substrate SDKs locally and read actual code (not just
  docs/blogs/searches that informed #18 decision). Verify our deep-eval claims
  with code-level evidence; surface primitives we could leverage that we missed;
  identify refactor opportunities in current/planned PBS code; discover
  unanticipated capabilities; inform Substrate Protocol shape with actual SDK
  API patterns rather than documented surface.
- **Method**: clone both repos via `ref` skill convention to
  `~/dev/reference/claude-agent-sdk/` + `~/dev/reference/agent-framework/`;
  structured code-read with focus areas per substrate.
- **Focus areas**:
  - **Claude Agent SDK**: agent loop internals; MCP attach-to-agent mechanism;
    RunHooks lifecycle (PRE/POST tool + lifecycle callbacks); Pydantic
    structured output flow; Channels event-driven push internals; session JSON
    shape (for AuditEvent compatibility analysis); plugin SKILL.md loader
    behavior
  - **MS Agent Framework**: agent middleware pipeline; 3-layer middleware
    shape (agent / function / chat); workflow engine + checkpointing internals;
    event-driven workflow trigger types; multi-provider connector patterns;
    SKILL.md / Agent Skills loader; A2A integration shape
- **Output**: `docs/decisions/sdk-deep-read.md` — findings + leverage
  opportunities + refactor recommendations + Substrate Protocol design
  implications.
- **Scope**: 1 session (this session if context allows; otherwise next).
- **Order**: before #9 implementation phase (Substrate Protocol shape benefits
  from code-level read); could run parallel with #19 (LlamaIndex eval) + #20
  (PydanticAI eval).
- **Constraints flowing**: Substrate Protocol design (lands in #9) informed by
  actual SDK API patterns; potential refactor list for existing PBS code;
  potential primitives-only adoption recommendations from MS AF for use within
  Claude Agent SDK substrate.

**22. Terminology + level-boundary re-evaluation — meta-architectural review**
✅ **SHIPPED session 13** (2026-04-30; commit batch with cascade).

- **Outcome**: three coupled changes locked together, decomposed into two sub-DRs:
  1. **Sub-DR A** (`docs/decisions/terminology-and-specialist-primitive.md`):
     Office → Workspace at pattern primitive level; Specialist NEW pattern primitive
     between Skill and Workspace (composable codified expertise bundle; 5
     composability axes; granularity 3-test); Department demoted from pattern
     primitive to optional `groupings: dict[str, list[specialist_id]] | None` shape
     (deployment-instance optional grouping convention).
  2. **Sub-DR B** (`docs/decisions/positioning-three-tier-framework.md`):
     Three-tier framing locked (Infrastructure / Workspace / Specialist); ICP
     refinement (PBS narrow + framework broader); three deployment possibilities
     → four (specialist authoring tier added); marketplace shape locked (of
     specialists, not workspaces — architectural constraints locked, v3
     mechanics deferred).
- **Sharpening metadata**: 3-round decision-design-sharpening (full monty + 2
  user-triggered). ~26 refinements surfaced; ~85% expansions, ~15% revisions.
  Decomposed at Round 4 trigger per `decision-design-sharpening` skill rules.
- **Migration cascade**: pre-RAG, pre-launch — essentially free per ARCH
  "Maintenance discipline" deprecation rules. Cost: 2-3 sessions careful sed +
  manual logical re-read.
- **Files touched in this commitment**:
  - NEW: Sub-DR A + Sub-DR B
  - ARCHITECTURE.md (v0.30 → v0.31; reference card; office-vs-department
    section rewrite; meta-rule 1 rename "app vs office" → "app vs workspace";
    meta-rule 3 invalidation contract)
  - VISION.md (thesis line; deployment possibilities 3→4; AI-office → AI-workspace;
    office-vs-department section rewrite; architectural requirements section)
  - docs/strategic-positioning.md (substantial rewrite per Sub-DR B)
  - This file (#22 collapse + downstream constraints flowing)
  - HANDOFF.md (session 13 entry)
  - docs/decisions/office-vs-department.md (header note: superseded scope)
  - Other DR cascading edits (s/department/specialist + s/office/workspace +
    logical re-reads): bundled with #11 single-touch refactor for skills + remaining
    DR sweep

- **Constraints flowing to downstream commitments**:
  - **#9 implementation**: uses Workspace + Specialist + Skill primitives;
    `extensions/specialists/<id>/specialist.md` registration (was
    `extensions/department/<dept>/department.md`); SpecialistDescriptor
    Pydantic Protocol added to substrate-protocol-design.md common surface
  - **#11 (Cowork integration)**: slash commands `/<specialist-id>:<skill>`;
    `specialist:` frontmatter sweep across 19+ skills (REQUIRED, no silent
    default); `extensions/workspace/` rename; `office-config.yaml` →
    `workspace.md` migration (also adopts hybrid-shape per #16);
    `setup-office` skill → `setup-workspace`; `integrate-department` skill
    → `integrate-specialist`
  - **#6 (audit-trail v2 retrofit)**: `specialist:` filter on `query_audit_trail`;
    `specialist_id` field on AuditEvent; new event kinds
    (`specialist_installed` / `_uninstalled` / `_event_subscription_matched`)
  - **#14 (Memory Bank)**: `search_memory` accepts `specialist:` filter
    (defaults to calling-skill's specialist); memory taxonomy 4th axis
    `department` → `specialist`
  - **Phase 1 corpus**: `search_corpus` `specialist_filter:` arg
  - **v2 (was AI-office builder)**: AI-workspace generator; output format
    must be marketplace-compatible per Sub-DR B
  - **v3 (was Marketplace of department modules)**: Marketplace of specialists;
    architectural constraints locked Sub-DR B; v3 mechanics (auth, pricing,
    governance, deprecation) deferred

**23. Sharpening skills (decision-design + pre-implementation) — local now + future global plugin elevation**
(NOT BLOCKING; meta-architectural skills scaffolded session 12) — captures the
two-phase sharpening pattern discovered during session 12 #21 SDK deep-read
multi-round sharpening work.

- **Mission**: codify the two-phase sharpening pattern as TWO invocable skills
  (one per phase, sharing methodology). Local skills exist; future elevation
  to global plugin marketplace when PBS framework distribution shape settles.
- **Two skills (DONE session 12, replacing initial single-skill scaffold)**:
  - `plugin/skills/decision-design-sharpening/SKILL.md` (NEW v0.1.0) — Phase 1;
    fires AT DECISION-FORMATION MOMENT before commit to file. Triggers via
    "do another round" / "sharpen again" / "review/refine" / "challenge this"
    after AI proposes architectural decision. 2-3 round sweet spot;
    decomposition trigger if >3 rounds.
  - `plugin/skills/pre-implementation-sharpening/SKILL.md` (NEW v0.1.0) —
    Phase 2; fires AT IMPLEMENTATION-START MOMENT for major commitment after
    DRs locked. Triggers via "let's start implementing X" /
    "implementation-readiness check". Surfaces operational/runtime/deployment
    details; ~10-20% architectural finding flow-back to upstream DRs.
- **Why two skills (not one with mode parameter)**:
  - Different triggers (decision-formation vs implementation-start)
  - Different deliverables (refinements + DR persistence vs implementation-
    readiness checklist + DR amendments)
  - Different audiences (decision-maker vs implementer)
  - Per "Make wrong shapes impossible" — clear invocation surface per phase
    prevents calling decision-design skill at implementation moment
  - Shared methodology lives in `memory/feedback_pre_decision_sharpening.md`
    (single source; both skills reference)
- **Empirical validation**: pattern discovered + validated session 12 across
  R3a/R3b/R3c/R3d sharpening rounds + Substrate Protocol synthesis. Yielded
  18+ substantive architectural refinements across 12+ sharpening rounds;
  decomposition + 2-3 rounds per sub-decision pattern confirmed.
- **Composition**: composes with `audit` + `design-review` skills (which serve
  drift-detection role POST); these skills operate UPSTREAM at decision-
  formation OR implementation-start moments.
- **Local scope (DONE session 12)**:
  - Two SKILL.md files per plugin conventions
  - Shared theoretical grounding in `memory/feedback_pre_decision_sharpening.md`
- **Future global plugin elevation (DEFERRED)**:
  - Triggered by: PBS framework distribution shape settled (post-#22
    terminology re-eval; post-marketplace decision per ROADMAP v3)
  - Generalizes beyond PBS terminology to any architectural-discipline
    workflow
  - Marketplace-asset shape per ROADMAP v3 framing
  - When elevated: consider extracting shared methodology into `references/`
    pattern within the global plugin
- **Order**: skills exist now (local); elevation to global plugin = future
  work post-marketplace decision.
- **Constraints flowing**: NONE substantive; these are meta-architectural
  skills that support OTHER architectural decisions across all commitments.

**24. EU AI Act + DACH compliance specialist — HARD REQUIREMENT before Aug 2026 production**
(NEAR-BLOCKING for first PBS-Schulz production B-Plan deployment) — session 14 commitment.

- **Mission**: ship two-tier compliance specialist + substrate-level structural enforcement before production B-Plan output goes to UNB Stellungnahmen (Öffentlichkeitsbeteiligung publication = public-interest output triggering Art. 50(4) AI-disclosure).
- **Two-tier specialist** (per Sub-DR A specialist 3-test: cohesive competence + distributable + reusable across workspaces):
  - **`eu-ai-compliance` specialist** (cross-archetype — applies to ANY EU practitioner workspace):
    - Skills: `assess-ai-act-classification` (Art. 6 derogation analysis + Annex III check); `generate-ai-disclosure` (Art. 50(4) auto-emitted); `export-compliance-bundle` (Annex IV doc + Art. 26(6) 6-month log + FRIA + DSGVO RoPA fragment); `validate-specialist-conformity` (anti-Art-25-trap gate); `iso-42001-soa-scaffold` (Statement of Applicability template — major commercial asset); `dsk-oh-ki-attest` (selection-criteria checklist); `fria-scaffold` (Art. 27 FRIA template)
    - Entities: `ComplianceArtifact`, `RegulatoryReference`, `ConformityDeclaration`, `DisclosureReceipt`
    - References: EU AI Act text (Reg. 2024/1689); Commission Art. 6 guidelines (when published Feb 2026); DSK Orientierungshilfe KI (May 2024); Hambacher Erklärung principles; ISO/IEC 42001 spec
  - **`dach-regulatory-extension` specialist** (domain-anchored — extends with DACH-specific layer):
    - Skills: `berufshaftpflicht-disclose` (client contract AI-disclosure clause); `bsi-c5-attest` (deferred until first public-sector deployment); `it-grundschutz-baseline` (Behörden contracts); `bmds-tracker` (KI-Durchführungsgesetz evolution)
    - References: BAK / BRAK leitfaden; BSI publications; BMDS KI-Durchführungsgesetz; Bundesländer-specific landesrecht
    - `depends_on: [eu-ai-compliance]`
- **Substrate-level additions** (NOT specialist content; framework primitives — go through #25 Protocol pluggability):
  - AuditEvent gains `ai_act_article_mapping: list[str]` field
  - Default 6-month log retention (Art. 26(6))
  - Specialist conformity manifest = Pydantic gate at Substrate Protocol layer (anti-Art-25-trap STRUCTURAL enforcement per Option B from `shape-extension-and-architectural-floor.md`)
- **Hard requirements before any production B-Plan use (binding from Aug 2026)**:
  - Art. 50(4) AI-disclosure on public-interest outputs (B-Plan Begründung is public-interest per BauGB §3 Öffentlichkeitsbeteiligung)
  - DSGVO controller-posture clarity + RoPA
  - BRAK/BAK-aligned client disclosure clause
- **Critical architectural constraint**: Art. 25(1)(b) substantial-modification trap — practitioner-author categorization must STRUCTURALLY prevent specialist authorship from shifting intended purpose (or practitioner becomes provider with full Art. 16 obligations: CE marking, conformity assessment, EU database registration). Make impossible by structural design (specialist conformity manifest as Pydantic gate); NOT solvable by convention.
- **Order (locked session 14 reorder)**: **POSITION 5 in pre-RAG queue** — DESIGN can happen anytime; IMPLEMENTATION needs #11 (Cowork integration — specialist primitive operational) + #25 (shape extension + Option B floor implementation). Sequence: #25 design → #20 → Bundles → #11 → **#24** → #19. BEFORE first PBS-Schulz production B-Plan ships (Aug 2026 hard deadline for Art. 50(4) AI-disclosure).
- **Strategic asset**: ISO 42001 SoA scaffold publishable as marketplace asset — cuts cert cost dramatically for any EU practitioner workspace adopter; major commercial differentiator.
- **Constraints flowing**:
  - **#9 Bundle B (entity gate + Layer 3)**: specialist conformity manifest is Pydantic Layer-2 schema; gate enforcement at write-time
  - **#11 Cowork integration**: `setup-workspace` skill + `integrate-specialist` skill prompt for compliance-specialist installation as default for EU deployments
  - **#6 audit-trail v2 retrofit**: `ai_act_article_mapping` field; 6-month retention default; new event kinds (compliance_artifact_emitted, disclosure_receipt_recorded, conformity_validation_run)
  - **#25 Shape extension framework**: practitioner-shape extension's Option B floor implementation includes specialist conformity gate; other shapes inherit
  - **VISION axis 2 + 3 + Foundation expansion (session 14)**: EU AI Act Art. 14 (sparring as human oversight operationalisation) + Berufsrecht (practitioner-as-author cleanest posture) directly map to PBS distinctness
  - **`docs/strategic-positioning.md`**: compliance specialist as marketplace asset + Cherry Ventures thesis match (regulatory landscape as innovation surface)
- **Files touched at implementation**:
  - NEW: `extensions/specialists/eu-ai-compliance/` + `extensions/specialists/dach-regulatory-extension/`
  - Substrate Protocol amendments (AuditEvent schema + retention default + conformity gate)
  - `docs/strategic-positioning.md` updates (commercial asset + fundraising narrative)
  - First-bind deployment template (PBS-Schulz pioneer production-readiness checklist)

**25. Shape extension framework + Protocol pluggability**
(FOUNDATIONAL; enables Tom Sawyer dynamic for community shape contributions) — session 14 commitment.

- **Mission**: implement shape-extension contract per `docs/decisions/shape-extension-and-architectural-floor.md`. Workspace shapes are pluggable extensions; framework provides shape-neutral primitives + Protocol pluggability (Coordination/Sparring/Audit/Trust/Time); concrete shapes (practitioner / autonomous-business / personal-OS / KG / federation / hybrid) live as `extensions/shapes/<shape-id>/`.
- **Scope**:
  - Shape extension contract: `extensions/shapes/<shape-id>/shape.md` Layer 1+2 hybrid-shape (entity-md per #16) declaring `shape_id`, `display_name`, `default_configs` per axis, `shape_specific_primitives`, `substrate_compat`, `required_extensions`
  - Coordination Protocol pluggability (event-default + call-shape extension reference per Paperclip-style autonomous-business needs)
  - Audit Protocol granularity pluggability (claim-level baseline + action-level overlay + citation-only)
  - Sparring Protocol intensity pluggability (always-on + optional + none)
  - Trust/Governance Protocol pluggability (practitioner-judgment + budget-policy + none)
  - Time Protocol pluggability (turn-based default + long-running extension shape) — the *abstraction* lands in #25; concrete long-running runtime substrate adapter implementation is deferred per DR D4 to first autonomous-business shape implementation (substrate adapter is shape-extension-driven; build when shape needed). #25 locks the Protocol surface so D4 implementation slots cleanly later
  - Practitioner-shape extension reference implementation (PBS pioneer = practitioner-shape) — validates contract end-to-end
  - Option B structural floor implementation: anti-Art-25-trap gate (specialist conformity manifest Pydantic gate) + claim-level audit baseline (always emitted) + human authority chain enforcement (configurable granularity)
- **Order (locked session 14 reorder)**: **POSITION 1 in pre-RAG queue** — DESIGN first as architectural foundation (locks shape extension contract + Option B floor specs; downstream Bundle design + #11 + #24 inherit). IMPLEMENTATION can wait for #11 substrate (specialist primitive operational in Cowork plugin shape) + #9 entity gate. Sequence: **#25 design** → #20 → Bundles → #11 → #25 implementation lands within #11 → #24 → #19. BEFORE marketplace v3 (shape extension contract = marketplace listing schema for shape distribution).
- **Strategic asset**: enables Tom Sawyer dynamic — community can author shape extensions for shapes PBS doesn't market (autonomous-business / personal-OS / sovereign / federation / hybrid). Framework breadth grows organically without PBS effort. Marketplace v3 hosts shape extensions alongside specialists.
- **Constraints flowing**:
  - **#9 implementation**: Substrate Protocol common surface gains shape-extension hooks; SpecialistDescriptor includes `shapes_supported` field
  - **#11 Cowork integration**: `setup-workspace` skill prompts for shape selection; defaults to practitioner shape
  - **#24 EU AI Act compliance specialist**: Option B floor implementation lives here; practitioner-shape extension's accountability binding inherits structurally
  - **ROADMAP v3 marketplace**: marketplace listing schema includes shape extensions + substrate implementations alongside specialists
  - **VISION**: VISION scope clarification (practitioner-shape) + architectural inheritance (Option B) reference shape extension model
- **Files touched at implementation**:
  - NEW: `extensions/shapes/practitioner/shape.md` (PBS pioneer reference)
  - NEW: shape extension contract Pydantic schema + `register_shape` MCP tool
  - Substrate Protocol amendments: shape-extension hooks; Protocol pluggability for Coordination/Sparring/Audit/Trust/Time
  - `entity-md-spec.md` updates: shape-as-type added to namespacing examples
  - `plugin-conventions.md` updates: shape extension authoring guidance
  - Test scaffolds: at least one non-practitioner shape extension scaffolded as architectural validation (likely autonomous-business per Paperclip-style reference; community-buildable post-implementation)

---

### v1 commitments (pulled forward from ROADMAP, 2026-04-29 session 6)

Three architectural items were *pulled forward to v1* — they MUST
land before Phase 1 corpus download. Each has a decision record
and an initial scaffold; remaining work is skill retrofits +
integration. Tracked here for visibility; full plans in the
linked decision records.

**1. Unified audit trail** — see `docs/decisions/audit-trail-v1.md`.

- Schema + Pydantic + 2 MCP tools (record_audit_event,
  query_audit_trail) shipped session 6.
- Remaining: backfill_audit_trail tool; skill-side dual-write
  retrofits (orchestrator, save-baustein, record-feedback,
  draft-textteil-b/c, review-draft, research-references each
  declare record_audit_event in mcp_tools_required + invoke at
  appropriate checkpoints); **slice 17 cross-reference invariant
  audit implementation lands in #6 scope; first-run waits for
  events** (chronological-valid: slice scans event records;
  no events to scan pre-first-binding. Implementation deferred
  is invalid per sharp defer rule v0.20; first-run deferred is
  the honest framing).

**2. Sparring-output structural promotion** — see
`docs/decisions/sparring-output-v1.md`.

- ReviewOutput + RecommendationOutput schemas + validate_skill_output
  MCP tool + plugin-conventions output_schema field shipped
  session 6.
- Remaining: heuristic markdown-field parser refinement;
  orchestrator PROCEDURE.md validation-loop integration; skill
  retrofits (review-draft declares output_schema + reformats body
  output sections; orchestrator's Checkpoint 13 declares schema
  for recommendation outputs); first end-to-end test on a sample
  document.

**3. State.md MCP gate** — schema-bearing project state lives at
`<project>/_ai/state.md`; ProjectState Pydantic + get/update_project_state
MCP tools shipped session 6 (covered in the same bundle since
state.md was already YAML-frontmatter shape — gap was validation,
not format).

- ✅ **Done session 7**: all 8 skills (orchestrator, survey-project,
  draft-cover-mail, validate-checklist, review-draft, draft-textteil-b/c,
  promote-to-skill) declare get_project_state / update_project_state
  in mcp_tools_required and route reads/writes through the gate.
- Verification: audit slice 14 run after retrofit confirms no direct
  Read/Write of state.md remains.

**4. Fail-closed fallback corollary** (session 7) — see
`docs/decisions/mcp-fallback-policy.md`.

- Meta-rule 4 corollary added to ARCHITECTURE.md (v0.6 → v0.7):
  contract-bearing reads have no fallback path; MCP-unreachable
  surfaces to user and stops, never bypasses the contract.
- Plugin-wide sweep (session 7): all 19 skills' `fallback_when_mcp_absent`
  strings rewritten under the rule. Audit slice 14 brief extended
  with violation pattern 5 to scan fallback strings for declared
  future bypasses.
- ✅ **Done session 7**.

**5. Trigger-convention simplification** (session 7) — see
`docs/decisions/trigger-convention.md`.

- Old `{phrase, lang}` structured form retired for flat concept
  labels; LLM matches semantically across languages. German
  technical anchors (UNB, Stellungnahme, Festsetzungen) preserved
  when domain-bearing.
- ✅ **Done session 7**: all 19 skills updated; convention codified
  in `docs/plugin-conventions.md` §11.

**6. Audit-trail v1 → v2 reversal** (session 7) — see
`docs/decisions/audit-trail-v2.md`. Supersedes v1.

- Single-write architecture: skills call `record_audit_event` only;
  the `record_decision` gate atomically mirrors to `decisions.md`.
  No skill-side dual-write discipline.
- 5 prose sources retired (`module-decisions.md`,
  `correspondence-log.md`, references `changelog.md`,
  `state.md.phase_history`) — render-time prose synthesis via new
  `render_audit_trail` MCP tool.
- 2 prose sources stay: `decisions.md` (legal-defense provenance)
  and `snapshots/` (artifact bytes).
- Remaining: `record_decision` + `render_audit_trail` MCP tools;
  schema additions (`user_confirmation` event, full reasoning
  text); skill retrofits per v2 plan; ProjectState schema drop
  `phase_history` field.
- **Per #16 constraint (session 10)**: AuditEvent schema remains
  Pydantic-shaped (events are interface contracts — rightly
  structured); hybrid-shape principle does NOT touch event
  format. **Gate-side conformance**: when retrofit adds
  `actor_kind` + `department:` filtering, also verify entity-write
  events route through the new generic entity gate (post-#9).
  `details.reasoning_full_text` may surface markdown for free-form
  fields (minor, not load-bearing).
- **Per session-11 constraint (governance + identity sourcing
  decision record)**: entity-mint AuditEvents include
  `convention_applied: {file, section, git_sha}` field in the
  `details:` payload when AI applied a convention rule to mint a
  new entity. Pydantic validates required-when-applicable
  (entity-mint events MUST include it; other events don't need
  it). The `git_sha` ties the audit event to convention state at
  mint time, enabling defensible historical reconstruction even
  after conventions evolve. NOT a new event kind — structured
  field on existing entity-mint events. Required for the
  prose-rules-as-conventions pattern (per
  `governance-and-identity-sourcing.md` decision 4 + operational
  concern 3) to be auditable.

**7. Bootstrap-write MCP tools** (session 7) — close the meta-rule
4 fail-closed gap surfaced by audit slice 14.

- Two skills (`author-manifest`, `setup-office`) currently scaffold
  contract-bearing files via direct `Write` because no MCP gate
  exists for *first-write* of those file types. The v0.7 fail-
  closed corollary makes this a known architectural gap; the
  skills declare the bypass loudly rather than silently. Pre-RAG
  is the right window — fix architecture before deployment.
- Sketch:
  - `create_manifest(target_path, kind: 'domain'|'state', name: str,
    initial_entries?: list[dict]) -> CreateManifestOutput` —
    scaffold a valid empty manifest YAML through Pydantic, write
    file via loader. Replaces author-manifest's direct Write.
  - `create_office_config(values: dict) -> CreateOfficeConfigOutput`
    — Pydantic-validate the wizard's collected values, write
    office-config.yaml through the loader. Replaces setup-office's
    bootstrap-then-validate pattern with gate-only-write.
- Skill retrofits: author-manifest + setup-office update bodies +
  `mcp_tools_required` to use the new gates; fallback strings drop
  the "known bypass" caveat.

**8. Pre-action framing/preparation skill** (session 7) — close
the prep → implementation → review cycle. The current meta-skills
(audit, design-review) form the *review* layer. Implementation
skills (orchestrator + specialists) form the *implementation*
layer. There is no formal *preparation* layer; today we
informally discuss before acting, but no skill surfaces the right
preparation questions.

- Sketch: a new meta-skill (working name: `frame-task` or
  `scoping`) that fires before any non-trivial task, asking:
  - What's the actual problem we're solving (not just the user's
    surface request)?
  - What's in scope, what's out?
  - What approaches exist? Which one fits the constraints?
  - What constraints are non-negotiable (legal, architectural,
    deadlines)?
  - What does success look like — observable outcome, not "feels
    done"?
- Triggered on non-trivial task starts (orchestrator routes here
  before routing to implementation specialists). Outputs a brief
  framing artifact the implementation skills consume.
- The audit-trail v1→v2 reversal in session 7 is example: with a
  proper framing pass at v1 design time, target 9's "what does
  this subsume?" question would have been asked then, and v2
  wouldn't have been a reversal — it would have been v1.
- Pull-forward trigger: pre-RAG bundle (this commitment list).
  The skill is preventive of design errors that compound after
  launch — better in place before real project work begins.

**9. Department module contract + managed-entity concept**
(session 7 originally as "Pattern-vs-instance best-effort split";
**reframed session 9** post-#12 followup) — see
`ARCHITECTURE.md` "Pattern-vs-instance discipline" +
`docs/decisions/office-vs-department.md` (managed-entity concept) +
ROADMAP v2 "AI-office builder" entry.

- **Mission reframed (session-9 followup)**: the original
  "extract universal core from PBS-specific extension" framing
  was wrong. There is no universal entity-type core — each
  department defines its own entity types completely. Some are
  PBS-native (Project for planning, Asset for brand-voice); some
  are adapter-delegated (Invoice for invoicing → Lexware/etc.,
  Timesheet for PM → Harvest/etc.). The new mission: **design
  the department module contract + managed-entity concept with
  two delivery modes**. See `office-vs-department.md` "Department-
  managed entities + delivery modes" subsection for the full
  design.
- **Why this scope (reasoning + implementation, not just
  reasoning)**: per the single-domain-pioneer constraint, we
  can't validate the split via second-domain implementations we
  won't actually do. Two distinct validation signals: signal #1
  (refactor doesn't break PBS — implementable now via PBS regression
  tests) is the maximum validation extractable pre-RAG; signal
  #2 (right boundary across domains) waits for a real second-
  domain implementation that may never come. **Doing the
  refactor later is more painful** — post-data-accumulation work
  vs. clean refactor today. Pre-RAG is the unique cost-cheap
  window.
- **Targets** (post-session-9 reframe):
  - **Department module contract**: how a department contributes
    skills + managed entities + workflow phases + memory + manifests
    + audit subscriptions to an office. Pattern-level; domain-agnostic.
  - **Managed-entity concept** with two delivery modes (native +
    adapter), per-entity choice, mixed-mode within a department
    supported. Generalizes meta-rule 1's existing integration-
    adapter pattern (auxiliary integrations → primary department
    system-of-record).
  - **Adapter-emitted events** (per session-9 followup #4
    infrastructure-primitive review, Gap B): adapter Protocol
    gains `subscribe_to_changes(callback)` OR `poll_for_changes()
    -> list[Event]` method. External state changes (Lexware
    webhook on invoice paid; Harvest external timesheet edit;
    calendar adapter on new meeting) translate to native
    AuditEvents with `actor_kind=external_agent` and
    `origin_agent_card=<adapter URL>` per #10's existing design.
    Without this, adapter-mode managed entities have one-way
    visibility (PBS asks but never hears); with it, audit trail
    captures full bidirectional change history.
    **DEFERRED to #11 per session-11 decision** — Bundle E in
    the bundle structure below; first adapter-mode entity ships
    with #11 (Cowork integration's invoicing/PM scaffolding) so
    Protocol design has a concrete consumer at that point.
  - `ProjectState` refactor: move from
    `backend/mcp-server/src/pbs_mcp/project_state.py` to
    `extensions/department/planning/entities/project.py`. Reframe
    as planning department's primary native managed entity. NOT
    "extract a core" — entire schema is planning department's
    contribution.
  - Per-department phase tracking on Project (`phases: dict[str,
    str]` instead of single `phase`) + per-department lifecycle
    (`lifecycle: dict[str, Lifecycle]`). Today's single-valued
    fields are PBS-instance assumptions (per #12 D1 + D2).
  - **Per-company customization mechanism**: design how a specific
    deployment customizes a department-module's managed-entity
    schema. Three options on the table — Pydantic subclass per
    deployment (heavy, type-safe), office-config-declared
    `extra_fields: dict[str, type]` per entity (lighter), or
    free-form `metadata: dict` escape hatch. Choose with rationale.
  - Doctype-manifest generalization: each department contributes
    its own doctypes per its mode. Already partially supported
    via #12's 4th memory axis; #9 finalizes the contract.
  - `office-config` schema additions: `departments.<name>.entities.
    <entity>.{mode,adapter,config}` per-entity sub-sections (per
    #12 schema). Schema bump + migration.
  - MCP tool interfaces — verify none embed domain knowledge in
    names (`validate_doctype(slug)` is generic; would be wrong
    if hardcoded `validate_b_plan_begruendung` — already correct
    today).
  - Decision records — review each for PBS-specific assumptions
    leaking into pattern-level prose.
- **Output**: refactored backend + skill retrofits + passing
  PBS regression tests + `pattern-vs-instance-split-rationale.md`
  documenting per-decision reasoning (department module contract
  shape, managed-entity concept rationale, per-company
  customization choice + rationale, ProjectState refactor
  rationale).

- **Bundle structure (session 11 reorganization)**: #9's design
  was originally framed as a single 2-3 session pass. Session-11
  discussion surfaced that the seven open decisions are too coupled
  to rush AND too distinct to bundle without depth loss. Restructured
  as **5 design bundles** + implementation:

  - **Bundle A — Department module + location/registration**
    (1 session). Foundational shape: `extensions/department/<dept>/`
    package layout, `department.md` registration file shape (Layer-2
    `type: department` schema declaring `managed_entities` registry +
    `path_pattern` per entity + Pydantic class refs), gate's
    department-discovery mechanism at startup. **Why first**: every
    later bundle slots into this.
  - **Bundle B — Entity gate + Layer 3** (1 session). Gate signatures
    (`read_entity` / `write_entity` / `list_entities`), error model,
    body-preservation, cross-ref validation tightness; Layer 3
    customization mechanism (Option A/B/C — Option C `metadata: dict`
    is the leading position with explicit elevation triggers).
    **Why second**: highest blast radius (every later commitment
    writes through gate); needs A's department-registration shape
    settled.
  - **Bundle C — ProjectEntity migration + per-department phase/
    lifecycle** (1 session). Field-by-field plan for ProjectState →
    ProjectEntity (relocate to `extensions/department/planning/
    entities/project.py`); `phase: str` → `phases: dict[str, str]`
    (#12 D1); `lifecycle: Lifecycle` → `lifecycle: dict[str,
    Lifecycle]` (#12 D2). **Why third**: validates A + B by use; if
    foundation is wrong, friction surfaces here.
  - **Bundle D — Office-config schema additions** (~0.5 session).
    Concrete YAML shape of `departments.<name>.entities.<entity>.
    {mode, adapter, config}` + interaction with `department.md`
    declarations (override layer pattern). **Why fourth**: mostly
    mechanical once A is settled.
  - **Bundle E — Adapter Protocol shape (Gap B)** (~0.5 session,
    restored to #9 per session-11 sharp-defer audit). Pydantic
    Protocol interface: `subscribe_to_changes(callback)` (push) vs
    `poll_for_changes() -> list[Event]` (pull) vs both. Adapter-
    emitted events translate to AuditEvents with
    `actor_kind=external_agent` + `origin_agent_card=<adapter URL>`
    per #10's existing design. **Why in #9** (not deferred to #11):
    Protocol interface is framework infrastructure — the
    abstraction shape (subscribe vs poll, signature, error model,
    Pydantic interface) doesn't depend on a specific concrete
    adapter consumer. Concrete adapters (Lexware, Harvest, Personio)
    in #11 + #13 + #15 implement against the #9-produced Protocol.
    Original "no consumer until first adapter-mode entity ships"
    rationale was up-front-cost framing rejected under v0.20 sharp
    defer rule.

- **Scope (revised session 11, sharp-defer amended)**: ~4 design
  sessions (A + B + C + half of D + E) + 2 implementation sessions
  = **5-6 sessions total** (was 4.5-5.5; further expanded under
  sharp-defer audit to absorb Bundle E + activation skill + schema
  migration framework + manifest Pydantic models). Expansion
  warranted — per #16's failure-mode catalog, rushed architectural
  decisions produce silent-convergence + SQL-DB-trap failure modes;
  spending the time matches discipline. Items absorbed under
  sharp-defer audit: (1) **Bundle E adapter Protocol shape**
  (restored from #11 deferral); (2) **`activate-department` skill
  + session-open detection sub-skill** (framework infrastructure
  for any consulting deployment with multiple departments at
  first bind); (3) **Schema migration framework for memory data
  records** (entity gate IS the migration boundary); (4) **Manifest
  Pydantic models** (post-#16 hybrid-shape, manifests migrate to
  per-entity md files validated by the generic entity gate).
- **Connection to commitment #8 (framing skill)**: framing skill
  builds on this work — the reasoning produced here becomes the
  pattern-vs-instance reasoning the framing skill codifies for
  repeatable use. Order: #9 first (produces contract + reasoning),
  then #8 (codifies into repeatable skill).
- **Dependencies (revised session 11)**: no longer depends on #6
  audit-trail v2 retrofit. Original claim ("examine stable
  post-v2 schemas") was from the old framing where #9 extracted
  a universal core from existing schemas. Per session-9 reframe,
  #9 designs the contract from scratch — the schemas don't
  pre-exist for #9 to examine. AuditEvent schema is in
  known-stable shape post-#10 (additive fields landed); the
  retrofit (#6) is a downstream consumer of the entity gate, not
  an upstream dependency. **Order revised**: #9 is now position 1
  in remaining queue, #6 follows after #15.
- **Order note (revised session 11)**: position 1 in remaining
  pre-RAG queue. The generic entity gate produced here is
  load-bearing for #15 (Client/Actor), #11 (`department.yaml`),
  #6 (audit-retrofit references entities), #7 (bootstrap-write
  references entities), #17 (gate coverage review surveys real
  gates). Building any of those before #9 forces per-loader hacks
  or one-off gates that #9 has to refactor — exactly the
  silent-convergence failure mode #16 is meant to prevent.
- **Per #16 constraint (session 10)**: hybrid-shape principle is
  the **central design lens** for #9's managed-entity concept
  work. Concrete deliverables that originate in #16 land here:
  - **Generic entity gate** (`read_entity` / `write_entity` with
    `type:`-field dispatch to Layer-2 Pydantic subclass) replaces
    per-entity tools. Body preserved as-is across read/write.
  - **Per-deployment customization mechanism** (Layer 3) decision
    — three options on the table (Pydantic subclass / declared
    `extra_fields` / `metadata: dict` escape hatch). Pick with
    rationale.
  - **Body specs document** (`docs/conventions/entity-md-spec.md`)
    authored alongside Layer-2 Pydantic subclasses (one section
    per entity type).
  - **ProjectState refactor**: when relocated to
    `extensions/department/planning/entities/project.py`, also
    publish corresponding entity-body-spec section.
  - **Migration of `extensions/universal/doctypes.yaml`** + per-
    domain `doctypes.yaml` files → per-entity md files (per
    #16 D3 defer).
  - **Audit slice 21** (entity-md frontmatter + body conformance
    scan) implementation, parallel to slice 20.
  - **Design-review target 12** (entity authoring conformance)
    implementation, parallel to target 11.

- **Per session-11 sharp-defer audit (additional v1 absorptions)**:
  the following items, previously v1.x, are absorbed into #9
  scope as framework infrastructure for first-bind consulting
  deployments:
  - **`activate-department` skill + session-open detection
    sub-skill**: validates candidate `department.md` against
    `DepartmentEntity` Pydantic; conflict-checks managed-entity
    type names against active departments; appends to
    `departments_active`; emits `department_activated` AuditEvent
    with `convention_applied` field per governance-and-identity-
    sourcing decision 4. Session-open sub-skill globs
    `extensions/department/*/` vs `departments_active`, surfaces
    candidates.
  - **Schema migration framework for memory data records**:
    `pbs_core/memory_migrations/` per-record-kind exporters;
    Layer 1 `schema_version` field; entity gate applies migrations
    on read; `setup-office` reconcile mode triggers sweep
    migration. See "Schema migration framework" v1.x entry
    (pulled forward).
  - **Manifest Pydantic models**: post-#16 hybrid-shape, manifests
    migrate to per-entity md files; entity gate's Layer 2 Pydantic
    dispatch IS the manifest validator. `validate_manifest(path)`
    MCP tool layered on the gate. See "Manifest Pydantic models"
    v1.x entry (pulled forward).

**10. A2A schema compatibility + Gemini Enterprise pattern
emulation decision gate** — see
`docs/decisions/a2a-and-gemini-pattern-emulation.md`.

- ✅ **Done session 8**: per-row decisions across the v2 comparison
  table (orchestrator / backend transport / persistent state /
  cross-department workflow / audit trail / governance / model);
  three additive AuditEvent fields shipped (`actor_kind` required,
  `actor_card` optional, `origin_agent_card` optional) +
  cross-reference validator (`external_agent` requires
  `origin_agent_card`).
- ✅ **ARCHITECTURE.md** v0.9 → v0.10: meta-rule 3 invalidation
  table for AuditEvent updated; archetype-portability paragraph
  added to v0.10 changelog entry.
- **Constraints recorded for downstream commitments**:
  - #6 audit-trail v2 retrofit: every `record_audit_event` /
    `record_decision` call MUST set `actor_kind` explicitly.
    Skill retrofits pass `actor_kind="skill", actor_card=<name>`.
    `user_confirmation` events emit as `actor_kind="human"`.
  - #11 Cowork plugin agents: emit as
    `actor_kind="skill", actor_card=<agent-name>`.
  - #12 office-vs-department: cross-department coordination MUST
    be event-shaped (typed events on audit trail or sibling
    mechanism), not call-shaped. Preserves transport-swap-to-A2A
    path.
  - #13 deployment flexibility: HTTP MCP transport implementation
    + data classification annotations + AuditEvent.user_id
    (multi-user) land here. #10 decided HTTP MCP adoption; #13
    builds it.
- **Deferred items** (with documented revisit triggers in the
  decision record):
  - Cryptographic signing fields (Tier 3 migration when triggered)
  - Deterministic JSON canonicalization (Tier 3 migration)
  - Session-spanning "office-memory" concept
  - Model Armor analogue (input validation at MCP gate)
  - Agent Simulation analogue (v2)
- **Standards-conformance evaluations** (added session 11):
  - **CloudEvents** (CNCF): event format standard for cross-system
    interop. AuditEvent could optionally conform — additive
    (CloudEvents core fields like `id`, `source`, `type`,
    `specversion`, `time` map cleanly onto AuditEvent's existing
    fields; conformance is a small Pydantic adjustment + emit-side
    serialization). Low cost; future leverage if A2A federation or
    Gemini-Enterprise interop needs cross-system event consumption.
    **Action**: 0.5-session evaluation before #6 audit-trail v2
    retrofit lands — decide whether to bake CloudEvents-conformant
    serialization into v2 from inception (cheaper than retrofitting
    later) or defer until concrete federation need surfaces.
  - **JOSE / JWT / JWS / JWE** (token formats + signing for A2A
    agent cards): folds into the existing "cryptographic signing
    fields" deferral above. Tier 3 trigger.
  - **PROV-O** (W3C Provenance Ontology, cross-system audit
    provenance interop): low-priority watch position. Could fold
    into AuditEvent shape if a regulated cross-org consulting
    deployment surfaces the need. **Action**: revisit if a
    regulated-industry consulting client engages.
  - **OAuth 2.0 / OIDC / SAML / SCIM** (federated identity standards):
    fold into #13 auth-layer abstraction (Tier 2/3). Already in
    governance-and-identity-sourcing decision 2 scope.
  - **Dublin Core / DCAT** (institutional metadata + data catalog):
    situational only; relevant for enterprises with archive /
    catalog mandates. **Action**: skip until a deployment surfaces
    the requirement; per glue-not-replacement, we'd adapt to their
    catalog infrastructure rather than build our own.
  - **RDF / OWL** (semantic web / formal knowledge graph):
    situational; high-cost machinery. ARCH already gestures via
    entity-elevation ("closer to knowledge graph + document
    store"). Real RDF/OWL adoption only if cross-org formal
    knowledge federation is the genuine need — rare even at
    enterprise scale. **Action**: skip until a deployment surfaces
    the requirement; per glue-not-replacement, adapt to their
    RDF infrastructure rather than build our own.

**11. Cowork as primary end-user runtime** (session 7, market
context) — see ROADMAP v2 "AI-office builder" entry's "Market
context" section.

- **Why this matters**: Cowork (Anthropic's desktop agent for
  knowledge workers) supports MCP servers, Agent Skills, and
  Plugins natively. "Custom connectors work across every Claude
  client" — including Cowork. Anthropic ships an open-source
  plugin library (`github.com/anthropics/knowledge-work-plugins`)
  with domain plugins for legal / finance / HR / marketing /
  design / operations. PBS-bureau aligns architecturally with
  this pattern.
- **The runtime split**:
  - **Dev runtime**: Claude Code (developer-mode; Gunther uses
    this to *build* PBS via skills + MCP server in this repo)
  - **End-user runtime**: Cowork (knowledge-work mode; the
    actual planning bureau worker uses this to *operate* the
    office)
  - **Backend**: same MCP server in both; same skill conventions;
    same memory layout. The runtime difference is the
    front-end agent loop, not the office.
- **Scope directive (session 7)**: **Deep + complete integration,
  no consideration for sunk costs.** Adopt Anthropic's plugin
  shape wholesale where it differs from ours. We don't preserve
  current implementations just because we built them — we converge
  with the canonical Cowork-plugin pattern unless there's a
  specific load-bearing reason to diverge. Full integration with
  Anthropic's existing infrastructure is the goal; partial
  alignment isn't.
- **Concrete work items** (deep + complete scope):
  - **Plugin shape conformance**:
    - `.mcp.json` at plugin root with `pbs_mcp` declared as stdio
      MCP server
    - `marketplace.json` at `.claude-plugin/marketplace.json` for
      distribution metadata
    - `CONNECTORS.md` documenting external services (Hidrive,
      email, etc.) PBS would use
    - LICENSE file at plugin root (verify present)
    - **Polished README** as marketing front door — sells the
      value prop, quick-start, lists components
  - **Slash commands as primary user surface** (Cowork-native
    invocation):
    - `commands/<name>.md` for major user operations
    - **Department-namespaced** per commitment #12:
      `/planning:draft-begruendung`, `/planning:review-draft`,
      `/planning:send-to-authority`, `/pm:create-timesheet`,
      `/invoicing:generate-invoice`, etc.
    - Slash commands invoke skills behind the scenes
    - Map every user-facing operation in current trigger-routing
      to an explicit slash command
  - **Plugin agents formalized** (lift from "deferred to v1+"):
    - Concrete agents:
      - `research-references-fetcher` — autonomous corpus fetch
        + checksum + ingest (currently runs ad-hoc in
        research-references skill via subagent)
      - `audit-slice-runner` — per-slice autonomous execution
      - `design-review-target-runner` — per-target autonomous
        execution
      - Future: `legal-reviewer` (deep §-by-§ checks per ROADMAP
        v2 entry)
    - Each agent has `<example>` blocks per Anthropic's pattern
    - Re-evaluate ARCHITECTURE meta-rule 4 placement table —
      "agents deferred until concrete need" no longer applies
  - **Migrate `office-config.yaml` → `pbs.local.md`** (markdown
    + YAML frontmatter), the Cowork-native pattern. Old YAML
    file deprecated; one-time migration script. Decision: the
    Cowork pattern is the standard; we adopt it.
  - **Skill frontmatter alignment**:
    - Adopt their fields where applicable (`argument-hint`,
      `user-invocable: false`)
    - Add `<example>` blocks per skill description
    - Keep our extra fields (mcp_tools_required, etc.) as
      additive — they don't conflict
    - Add `department:` field per commitment #12
  - **Test in actual Cowork** (not just Claude Code):
    - Install PBS as a Cowork plugin via
      `claude plugins add github.com/Gunther-Schulz/pbs-bureau`
    - End-to-end test of a representative workflow
      (e.g., `/planning:draft-begruendung` from blank project)
    - Document any incompatibilities; resolve by changing PBS
      (per "no sunk costs" directive)
  - **Decision record**: `docs/decisions/cowork-deployment.md`
    documenting all the shape decisions + migration outcomes.
- **Scope**: **3-5 sessions** (was 1-2; revised under deep-
  integration directive). Substantial work touching every
  user-facing surface.
- **Order note (revised session 11, sharp-defer amended)**:
  execute SIXTH in pre-RAG queue (after #9 entity gate + #15
  Client/Actor + #6 audit-trail v2 + #7 bootstrap-write + #17 gate
  coverage review). Chronological reason: #11 touches every
  user-facing skill (namespacing, `<example>` blocks, plugin shape
  conformance). Running it before #6 + #7 retrofits = double-
  touching every skill (first for plugin shape, then for
  audit-trail v2 + bootstrap-write retrofits). Position 6 is
  single-touch — every skill gets one combined refactor pass on
  the already-final post-retrofit shape. `department.yaml` adopts
  hybrid-shape from inception per #16; the generic `read_entity`
  / `write_entity` gate from #9 is the canonical loader (no
  per-loader hack). Adapter Protocol shape (Gap B) lands in #9
  Bundle E (restored from #11 deferral); concrete adapters
  implement against the #9-produced Protocol here. A2A decisions
  inform whether agent-card identity matters for Cowork-deployed
  offices. Before D (plugin version bump). Before #13 (deployment
  flexibility — needs Cowork plugin shape settled).
- **Per #16 constraint (session 10)**: `extensions/department/
  <dept>/department.yaml` file format **adopts hybrid-shape
  (md+frontmatter), NOT pure YAML**. Frontmatter declares
  `event_subscriptions:` + `managed_entities:` registry +
  department-level config; body describes department character +
  conventions in prose. Skill frontmatter sweep (per #12) doesn't
  conflict with #16 — frontmatter pattern is the same in both.
  See `docs/decisions/ai-as-runtime-hybrid-shape.md` for full
  Layer-1 + Layer-2 + body-conventions spec.

- **Adapter Protocol consumers (restored to #9 per session-11
  sharp-defer audit)**: the Protocol interface itself is designed
  in #9 Bundle E. #11 implements concrete adapters against it as
  Cowork integration scaffolds first invoicing/PM adapter-mode
  entities. Concrete adapter implementations (Lexware, Harvest,
  etc.) follow per-deployment.
- **Studying anthropics/knowledge-work-plugins repo**: planned
  as a discovery activity that informs this commitment. Multiple
  plugins are relevant to our work — not just for "how to
  package a plugin" but as **leverage candidates** (parts we
  could adopt rather than reinvent):
  - **`legal`** — most architecturally analogous to our planning-
    bureau work (regulatory expert practice with document-heavy
    workflow). Best comparison target for skill conventions,
    memory taxonomy, document review patterns.
  - **`enterprise-search`** — directly relevant to our RAG /
    legal references retrieval work. Likely handles cross-tool
    search patterns we'd otherwise reinvent. Decision: adopt
    parts of it for our `research-references` / `verify-citations`
    workflows? Or stay with our own LanceDB-based approach?
  - **`cowork-plugin-management`** — Anthropic's meta-plugin for
    building/customizing plugins. Closest existing analog to our
    AI-office-builder vision. Worth deep study before designing
    our builder; may subsume parts of what we'd build.
  - **`productivity`** — generic knowledge-work patterns; useful
    for understanding their "common-case" baseline conventions
    so our PBS-specific patterns are clearly differentiated.
  - **Others** (sales, finance, marketing, customer-support,
    product-management, data, bio-research) — relevant for
    pattern-vs-instance discipline (commitment #9): seeing how
    Anthropic structures domain-specific vs domain-agnostic
    elements informs our split.

**12. Office-vs-department modularization** — see
`docs/decisions/office-vs-department.md`.

- ✅ **Done session 9**: per-question decisions across skill
  classification, memory 4th axis, cross-department coordination
  shape, office-config schema additions, setup integration,
  pattern-vs-instance check. ProjectState gains `departments_active:
  list[str]` field (additive Pydantic addition, smoke-tested).
  Skills are singleton-department; offices have 0..N departments;
  cross-department coordination via AuditEvent + extended
  watch-list with per-department `event_subscriptions:` (no new
  event mechanism — reuses existing audit infrastructure).
- ✅ **ARCHITECTURE.md** v0.10 → v0.11: office-vs-department
  open-question section converted to resolved; meta-rule 3
  invalidation table updated for ProjectState; scope-orthogonality
  layering convention extended to 4 axes (department added).
- **Constraints recorded for downstream commitments**:
  - **#11 (Cowork integration)**: skill frontmatter `department:`
    sweep across 19+ skills (REQUIRED, no default per strict-
    validation discipline); slash commands namespaced
    (`/<dept>:<skill>`); office-config `departments.<name>`
    schema bump + migration co-located with `pbs.local.md`
    migration; `extensions/department/<dept>/department.yaml`
    file format implementation; `integrate-department` skill
    creation.
  - **#6 (audit-trail v2 retrofit)**: `record_audit_event`
    gate-side `departments_active` update logic + skill→department
    cached registry; `query_audit_trail` `department:` filter.
    Skill retrofits set both `actor_kind` (per #10) AND pass
    `department:` arg to memory tooling (per #12).
  - **#9 (Pattern-vs-instance split)**: ProjectState core/extension
    split MUST handle per-department phase tracking
    (`phases: dict[str, str]`) and per-department lifecycle
    (`lifecycle: dict[str, Lifecycle]`) — today's single-valued
    `phase`/`lifecycle` are PBS-instance assumptions. Project-as-
    long-running-entity itself is PBS-instance; ProjectState core/
    extension split should make project entity an opt-in
    extension (some offices have no project entity, e.g.
    brand-voice).
  - **#14 (Memory Bank)**: `search_memory` interface accepts
    `department:` filter (defaults to calling-skill's department);
    LanceDB memory index includes department metadata for filter
    queries.
  - **Phase 1 corpus work**: `search_corpus` gains optional
    `department_filter:` (defaults to calling-skill's department;
    overrideable for cross-department search).
- **Deferred items** (with proper-home identification per
  decision record):
  - Per-department phase tracking on ProjectState → #9
  - Per-department lifecycle on ProjectState → #9
  - Migration of existing state.md to multi-dept-aware shape →
    first-bind moment (academic today; zero projects bound)
- **Scope**: ~1 session (as planned) — primarily design + decision
  record + 1-line ProjectState schema addition.

**13. Deployment-mode flexibility architecture** (session 7,
post-Cowork-research insight) — see ROADMAP v2 "Gemini Enterprise
migration path" + commitment #10's HTTP MCP decision.

- **Why pre-RAG**: the architectural commitment is **deployment-
  mode flexibility**, not "pick a mode." Per-deployment decisions
  (local vs cloud, which cloud, on-prem, hybrid) happen
  case-by-case based on client needs, compliance constraints,
  budget, scale. What matters pre-RAG: the architecture supports
  any of these without rewriting. Designing flexibility post-RAG
  (after data accumulates in one specific mode's shape) is
  expensive; designing it pre-RAG is cheap.

- **The flexibility commitment** (Tiers 1-2 of the deployment
  ladder; Tier 3 is archetype change, documented separately):

  This commitment prepares the architecture to support both
  **Tier 1 (Local)** and **Tier 2 (Cloud-hosted)** without
  refactoring — the two tiers that share the same archetype
  (single-big-model orchestration). Tier 3 (Gemini Enterprise,
  multi-agent A2A archetype) is a separate refactor documented
  in ROADMAP v2 "Gemini Enterprise migration path."

  Three deployment modes within Tiers 1-2:

  - **Tier 1 — Local** (baseline): stdio MCP, all persistence
    in local files, no auth, single user. Gunther's daily PBS
    use; consulting clients who want their data on their own
    machine.
  - **Tier 2 — Cloud-hosted**: HTTP MCP, all persistence in
    cloud storage, auth required, multi-user-per-office.
    Typical consulting deployment — managed service,
    cross-device, EU-region for German clients, cloud-managed
    backups. Cloud provider chosen per client (Cloud Run /
    Fly.io / Render / managed K8s / on-prem K8s — case-by-case).
  - **Tier 2.5 — Hybrid**: HTTP MCP with persistence split —
    some local (per-user cache, sensitive working state), some
    cloud (shared bausteine, audit trail, manifests). For
    compliance-strict clients where some data can't leave
    premises.

  All three modes run the **same backend code** — same single-
  big-model archetype. Only the transport, persistence, and
  auth layers differ. Pluggable interfaces:

  - Transport: stdio vs HTTP
  - Persistence: local files vs cloud storage vs per-entity
    hybrid routing
  - Auth: none vs API key vs OAuth vs A2A signed agent cards

  **Tier 3 (Gemini Enterprise) is intentionally NOT in this
  commitment's scope** — it requires orchestrator decomposition,
  A2A message-passing as PRIMARY (not internal-shape-only),
  Memory Bank as state service, Agent Identity infrastructure.
  Substantial refactor (3-6 months estimated). Triggered by
  enterprise-scale need (1000+ users, federated authority,
  regulatory governance) — see v2 entry for trigger conditions.

- **What "local Claude install + flexible backend" enables**:
  - Local backend: Gunther's offline-capable, free, fast
  - Cloud backend: multi-user per-client office, cross-device,
    cloud-managed backups, EU-region GDPR-friendly for German
    clients
  - Hybrid: compliance-strict clients (some on-prem, some cloud)
  - In all cases, **local install is just Claude Code** (or
    Cowork). The local install never carries the backend
    weight; it's always just the client.

- **Concrete decisions for the gate** (2-3 sessions; pre-RAG
  must be deployment-ready for Schulz Planungsbüro Tier-2 use
  with Gunther + colleague on shared backend):

  **Layer abstractions (must support all three deployment
  modes):**
  - **Transport layer abstraction**: backend exposes both stdio
    (in-process) and HTTP (long-running service). Same handlers,
    different transports. Already adopted via #10's HTTP MCP
    decision.
  - **Persistence layer abstraction**: pluggable storage backend
    interface. Implementations:
    - `LocalFsBackend` — current state.md / `_ai/` / LanceDB-on-
      disk pattern
    - `CloudObjectBackend` — S3/GCS/R2 for documents, managed
      vector service or self-hosted vector DB for embeddings
    - `HybridBackend` — declares per-entity routing rules
    - Pydantic models stay identical; backend interface is
      separate
  - **Auth layer abstraction**: pluggable auth modes. None
    (local), API key, OAuth, A2A signed agent cards.

  **Multi-user readiness (pre-RAG required for Tier 2)**:
  - **User identity + attribution scheme**: every audit event,
    baustein use, decision-record entry, lifecycle transition
    needs correct user attribution. Required:
    - Authentication mechanism that identifies the user per
      MCP request (likely API token per user via Coolify SSO,
      OAuth, or signed agent cards from A2A pattern in #10)
    - `User` Pydantic model with id + display name + role
      (member of which practice)
    - AuditEvent gains `user_id` field (additive; was generic
      `actor` string before — now first-class)
    - Bausteine `successful_uses[]` / `rejected_uses[]` entries
      gain `user_id` per record
    - decisions.md entries auto-attributed to invoking user
  - **Concurrent access patterns**: when two users hit the same
    backend simultaneously, schemas + handlers must avoid
    races. Required:
    - State.md updates: optimistic locking via `lock_version`
      field on ProjectState (incremented per write; read-modify-
      write checks expected version, retries on mismatch)
    - Audit trail: append-only with monotonic event IDs (already
      designed; just verify no race in `record_audit_event`)
    - Bausteine dedup: idempotent save_baustein with content-
      hash based identity (already partly designed; verify race
      handling)
    - `bind_project`: idempotent (already noted in code; verify)
    - `record_decision` (audit-trail-v2): write decisions.md +
      audit event in same transaction (atomic at backend; not
      partial)

  **Reference deployment platform**:
  - **Coolify as Tier-2 reference deployment**: Schulz
    Planungsbüro will run on Coolify (existing infrastructure;
    Docker-native; HTTPS via Let's Encrypt; user is already
    operator). Pre-RAG output includes:
    - Dockerfile for pbs_mcp HTTP MCP server
    - docker-compose / Coolify-deploy spec for the full stack
      (HTTP MCP + vector store container + object store
      container + embedding service container)
    - Reference `pbs.local.md` config showing OAuth /
      authentication setup against Coolify SSO
    - End-to-end deployment guide (deploy on Coolify, configure
      Cowork `.mcp.json`, smoke-test)
    - **Working two-user deployment** with Gunther + colleague
      both connected, both writing audit events, both using
      bausteine, with correct attribution + no concurrent-write
      drift.
    - **Notification adapter contract** (per session-9 followup #2
      broader review): introduce `notification-channel` adapter
      class (per meta-rule 1 pattern) + concrete adapters (email,
      Slack, push) + `notification_sent` audit event kind. Trigger
      conditions live in skill logic (extension of watch-list);
      delivery via adapter; delivery log via audit event. PBS does
      NOT track read/unread state — receiving channel (inbox) is
      state-of-record. Async cross-user notifications become load-
      bearing once Gunther + colleague work concurrently.
    - **Time-driven trigger infrastructure** (per session-9
      followup #4 infrastructure-primitive review, Gap A):
      server-side cron-like scheduler that fires "tick" audit
      events on a schedule; subscribers react via existing event-
      subscription primitive. MCP tool sketch:
      `register_scheduled_trigger(condition, event_kind, cadence)`.
      Extends event sources from "skill-emitted only" to "skill-
      emitted + time-emitted." Load-bearing for proactive deadline
      warnings (Frist-X-days-before), scheduled report generation,
      automatic Fristverlängerung filing on missed deadlines.
      Tier 2 cloud deployment naturally hosts the scheduler;
      Tier 1 local deployment can run it as a backend service or
      skip it (interactive-only mode).

  **In #13 pre-launch scope (sharp-defer amended session 11)**:
  - **Migration tools (between deployment modes / clouds)** —
    pulled forward from "deferred to post-RAG" per session-11
    sharp-defer audit. Cross-tier migration (Tier 1 ↔ Tier 2;
    cloud A → cloud B) is framework infrastructure for any
    consulting deployment that may change tier (most do over
    time). Bidirectional, well-tested. Implementation in #13's
    pre-RAG scope.

  **Stays per-deployment / per-engagement (NOT framework-level)**:
  - Compute infrastructure choice for OTHER consulting clients
    (per-deployment decision; Coolify is Schulz's reference;
    clients may use Cloud Run / Fly.io / their own K8s / etc.).
    Architecture supports any; specific selection is a per-engagement
    decision, not framework infrastructure.
  - Cost model for consulting deployments — per-engagement
    pricing, not framework code.
- **Output**:
  - Decision record `docs/decisions/deployment-mode-
    flexibility.md` — abstraction interfaces + per-mode
    trade-offs + decision tree for per-engagement choices
  - Decision record `docs/decisions/user-identity-and-multi-
    user.md` — user identity scheme + concurrent access
    patterns + auth mechanism choice
  - Working Coolify deployment: Dockerfile + docker-compose +
    Coolify-deploy spec
  - End-to-end test: Schulz Planungsbüro on Coolify, two users
    (Gunther + colleague), both connected, both writing audit
    events, correct attribution, no race conditions
- **Scope**:
  - Pre-RAG: 2-3 sessions (was 1-2; expanded for multi-user
    readiness + Coolify reference deployment + working
    end-to-end test)
  - Post-RAG: additional cloud backends (CloudObject for
    non-Coolify clients), additional auth modes, migration
    tools, hardening (3-5 sessions, post-launch as needed)
- **Order note (revised session 11, sharp-defer amended)**:
  execute SEVENTH in pre-RAG queue (after #9 + #15 + #6 + #7 +
  #17 + #11). Chronological dependencies: persistence-layer
  abstraction surfaces via the Pydantic model boundary which #9
  designs via the generic entity gate; transport abstraction
  already decided (#10's HTTP MCP commitment); #6 + #7 retrofits
  don't depend on persistence backend. **#13 needs #11's plugin
  shape settled** (pbs.local.md migration in #11 produces the
  config surface #13 deploys against). **Multi-user auth in #13
  binds to Actor entity from #15** (Actor.id + Actor.roles are
  the auth primitives). All upstream dependencies produced
  earlier in the queue. Original instance-anchored framing
  ("Gunther uses local stdio today, no consulting client engaged
  yet") removed under v0.20 sharp defer rule — #13 is framework
  infrastructure for every consulting deployment at first bind,
  regardless of PBS-Schulz's current local-only state.

- **Governance scaling architectural arc** (session-11 decision —
  see `docs/decisions/governance-and-identity-sourcing.md`):
  governance scales naturally without inventing a separate
  governance system; existing primitives compose along the
  org-size spectrum:

  | Org size | Primary mechanism |
  |---|---|
  | Solo → 5 people | File-system access; informal coordination |
  | 5-20 people | Git PRs + code-owners + audit trail |
  | 20-100 people | Git + gate-level role enforcement (Actor.roles from #15 + approval events from #6 + AuditEvent) |
  | 100-1000 people | Git + gate + department isolation (per #12) + cross-department approvals |
  | 1000+ / regulated | Tier 3 / Gemini Enterprise federated authority (separate archetype) |

  Implementation under #13's pre-RAG scope: tier-conditional
  enforcement at the gate (build once, activate at Tier 2). The
  enforcement code is dormant in Tier 1 (single-user); fires when
  Tier 2 (cloud HTTP, multi-user) deploys. Layered defense-in-depth:
  git (file changes) + gate (Python, deterministic) + skill
  workflow (LLM, surface UX). Critically, the LLM is NOT the
  enforcer — gate is. Defense-in-depth principle.

  Identity sourcing also lands here (per same decision record):
  two distinct adapters at play (auth provider + actor-data
  adapter); native vs adapter mode per deployment; same adapter
  pattern (meta-rule 1) as Lexware/Harvest/etc.

- **Office conventions as prose-rules** (session-11 decision —
  same record): deployment-specific rules (identifier conventions,
  naming, archival policies) live in markdown prose alongside the
  data, applied by AI at runtime. Strongest application of #16
  (AI-as-runtime) surfaced so far. NOT new infrastructure —
  natural use of the prose layer the hybrid-shape principle
  already provides. Documented for awareness; consumers across
  #9/#15/#13.

- **The constraint and the fix**: today's pbs_mcp is stdio-based,
  spawned per-session, runs on user's machine. For consulting
  deployments at other companies, cloud is better — clients
  don't want to manage Python installs, LanceDB disk growth,
  cross-device sync, multi-user backend sharing, or update
  coordination.
- **Concrete decisions for the gate** (1-2 sessions design):
  - **Transport**: HTTP MCP server (already decided in #10's
    proactive emulation) — long-running service, accepts
    authenticated requests. stdio mode preserved for local Gunther
    use; both share core domain logic.
  - **Persistence layer abstraction**: design pluggable backends
    so the same code runs on:
    - Local files (`state.md`, `_ai/`, LanceDB on disk) for
      Gunther's PBS instance
    - Cloud storage (S3/GCS/R2 for state + audit-trail; managed
      vector service or self-hosted vector DB for embeddings;
      document DB or object store for memory bausteine) for
      consulting deployments
    - Pydantic models stay identical; persistence interface is
      a separate concern
  - **Authentication**: API keys / OAuth / signed agent cards
    (A2A pattern). Per-office isolation. Multi-tenant or
    single-tenant-per-deployment (likely single-tenant for
    consulting — each client gets their own instance, simpler
    isolation).
  - **Compute infrastructure choice**: evaluate Cloud Run /
    Fly.io / Render / containerized self-hosted. **Initial
    recommendation**: containerized deploy on Cloud Run or
    Fly.io (cheapest, simplest, scales-to-zero, easy to package
    for consulting clients). Self-hosted Docker for clients who
    want their own infra.
  - **Embedding (bge-m3)**: GPU-friendly Cloud Run revision or
    fast CPU instance; benchmark required.
  - **LaTeX compile**: container with TeX Live; same
    container or sidecar.
  - **Memory + state migration tools**: from local PBS to cloud
    deployment (and back, if needed). Bidirectional path documented.
  - **Cost model for consulting deployments**: per-deployment
    cloud instance (client pays infra), per-user pricing
    (shared infra), or self-deploy (client owns ops). **Initial
    recommendation**: per-deployment (client pays their cloud)
    + self-deploy Docker — simplest model for a solo consultant
    selling to small offices.
- **Output**: decision record `docs/decisions/cloud-deployment-
  architecture.md` documenting transport + persistence + auth +
  infrastructure decisions. Plus a minimum-viable cloud deploy
  artifact (Dockerfile + minimal HTTP MCP server) as proof-of-
  shape.
- **Scope**:
  - Pre-RAG: design + decision record + Dockerfile/HTTP MCP
    skeleton (1-2 sessions)
  - Post-RAG: full implementation — auth system, persistence-
    layer abstractions, cloud deployment automation, tested
    end-to-end consulting deployment (3-5 sessions, post-launch
    when first consulting engagement is in sight)
- **Order note (revised session 11)**: see prior order note above
  — execute SEVENTH in pre-RAG queue (after #11). Persistence-
  layer abstraction influences nothing in #6/#7/#9 schema work
  under the runtime-fabric-first re-ordering — Pydantic boundary
  is decoupled from storage backend; #6/#7 retrofits don't touch
  storage layer; #9's generic entity gate is storage-agnostic.

- **Hardware-spec research note** (session 8 followup, persisted
  for use when #13 lands): Schulz Planungsbüro Coolify reference
  deployment hardware sizing, with **ingestion-vs-serving split**
  + scaling ladder. Verify all Hetzner pricing at order time.

  **Architectural pattern: ingestion node vs serving node**.
  Heavy compute (RAG corpus embedding via bge-m3) runs **locally
  on Gunther's RTX 5090** during corpus updates; LanceDB indices
  produced locally are **rsync'd to the cloud serving node**
  which only needs the embedding + reranker models loaded for
  query-time inference. Pattern works because LanceDB stores
  indices as plain Apache Arrow / Lance files — no service
  migration, just `rsync -av --delete <index-dir>
  coolify:/path/to/pbs/indices/`. Memory indices (#14) build
  on the serving node directly (continuous low-rate writes;
  small corpus; CPU embedding fine for the write rate). Net
  effect: serving node sized for query-time latency only, not
  ingestion throughput.

  **Tier ladder** (start cheap; trigger-driven upgrade):

  | Tier | Hardware | Approx €/month | Query latency | When to use |
  |---|---|---|---|---|
  | **Test (start here)** | CCX23 Hetzner Cloud (4 dedicated vCPU, 16 GB RAM, 160 GB SSD) | ~€30 | 500-750 ms (CPU int8-ONNX) | Initial deployment, 2 users, light testing — confirms workload fits + Coolify ops shape |
  | **Working bureau (CPU)** | CCX33 Hetzner Cloud (8 dedicated vCPU, 32 GB RAM, 240 GB SSD) | ~€50-60 | 500-750 ms | Steady 2-user production if CPU latency tolerable; comfortable RAM headroom |
  | **Speed-priority (GPU)** | GEX44 Hetzner dedicated (RTX 4000 Ada 20 GB, i5-13500, 64 GB RAM) | ~€184 | 100-150 ms | When CPU latency frustrates real drafting flow; ~5-7× speedup; forces dedicated (no Cloud snapshot/resize) |
  | **Heavy / multi-tenant** | GEX131 Hetzner dedicated (RTX 6000 Pro Blackwell 96 GB, Xeon 24-core, 256 GB RAM) | ~€1000+ | <100 ms | Consulting client offices, multi-tenant builder-generated offices, multimodal RAG ingest serving (ColPali page-image retrieval), or workloads that need fp16 / fp32 precision instead of int8 quantization |

  **Quantization choice**: int8-ONNX on CPU tiers (CCX23/CCX33);
  fp16 on GPU tiers. Int8 loses ~1-2 % retrieval quality vs fp16
  per published bge-m3 benchmarks — acceptable for our recall
  targets. Switch to fp16 only when GPU is available.

  **Upgrade triggers (trigger-driven, not preemptive)**:
  - **CCX23 → CCX33**: 16 GB RAM hits OOM or thrash under both
    models loaded + LanceDB cache + Python sessions. Resize is
    a power-cycle on Hetzner Cloud, no migration.
  - **CCX33 → GEX44**: real-use latency frustrates drafting
    flow (subjective; agentic-retrieval per-claim queries
    compound the perception). Migration: snapshot CCX33,
    redeploy backend on GEX44 dedicated (no in-place upgrade
    Cloud↔Dedicated; ~half-day of ops work).
  - **GEX44 → GEX131**: serving consulting clients alongside
    Schulz, OR multimodal RAG ingest serving from same node,
    OR concurrency >10 users.

  **Ingest re-sync workflow** (when corpus updates):
  1. Local RTX 5090: `pbs-mcp ingest --refresh` rebuilds
     affected index slice (research-references full refresh
     trigger).
  2. Local: `rsync -av --delete <index-dir>
     <coolify-host>:/path/to/pbs/indices/`.
  3. Serving node: `pbs-mcp` reads updated index automatically
     (LanceDB handles versioning).

  Memory indices (#14) build on serving node directly — not
  part of the rsync flow. Different write rate + size
  characteristics make local-build a wrong choice for memory.

**14. Memory Bank — selective retrieval over the memory layer**
(session 8, post-#10 followup) — see also Row 8 of
`docs/decisions/a2a-and-gemini-pattern-emulation.md` (RAG /
Grounding architecture pattern).

- **Why**: Inspired by Vertex AI's Memory Bank (managed
  persistent-context service for agents). The PBS-relevant
  insight isn't the managed-cloud transport — our `memory/`
  files are the equivalent local persistence — but the
  **selective retrieval** pattern.
- **The problem this solves**: today every session loads
  `memory/universal/...` + `memory/bausteine/...` + relevant
  project `_ai/` files in full. Fine when memory is small,
  but as bausteine accumulate (target: hundreds per domain
  across years of practice) and cross-project actor reputation
  / deadline / korrektur-history grows, full-load becomes
  wasteful and eventually context-limit-relevant. Selective
  retrieval over memory mirrors the RAG pattern over corpus —
  same architectural shape, different content.
- **Concrete deliverables**:
  - `search_memory(query, scopes, kinds)` MCP tool —
    deterministic embedding + filter + rerank; same retrieval
    discipline as `search_corpus`; scoped query (universal +
    domain + state + project + department, weighted).
  - `read_memory_entry(path)` MCP tool for full-text follow-up
    after retrieval surfaces a candidate.
  - Embedding job over `memory/` content; incremental on
    memory writes (record_baustein / record_feedback /
    record_audit_event hooks).
  - LanceDB index for memory (separate from corpus index).
  - Skill retrofits: skills that today full-load bausteine
    switch to `search_memory` calls. Validate via existing
    audit + design-review pre-bind.
  - Multi-user continuity behavior: shared memory pool
    queryable across Gunther + colleague (per #13 multi-user
    deployment); selective retrieval surfaces relevant
    entries regardless of authorship.
- **Pattern-vs-instance check**: the selective-retrieval
  contract (query → ranked memory entries with metadata) is
  pattern-level — applies to any AI office regardless of
  domain. The embedding backend (local bge-m3 / hosted Vertex
  Memory Bank / hybrid) is instance-level per Row 8 of #10's
  decision record. Per #10's Phase 1 constraint: design the
  `search_memory` interface to be retrieval-backend-agnostic,
  same as `search_corpus`.
- **Order note**: schedule **alongside Phase 1 corpus work**
  (right before or after RAG ingest, per session-8
  follow-up). Memory + corpus retrieval share embedding
  infrastructure (bge-m3, LanceDB, rerank pipeline); building
  them together is cheaper than separately. Lands BEFORE
  first project bind, so the first real PBS workflow runs on
  selective retrieval from day one rather than full-load.
- **Scope**: ~2 sessions design + impl, plus skill retrofits
  bundled with Phase 1 corpus work.
- **Forward-compat for #11/#12/#13**: skill bodies must NOT
  hard-assume "all bausteine in scope are loaded into context."
  They call `list_bausteine` (already gate-mediated) with
  filters and consume results. That discipline already lets us
  swap full-load for selective retrieval transparently when
  this commitment lands.

**15. Office-level managed entities (Client + Actor)** (session 9
followup #2, post-broader-review) — see
`docs/decisions/office-vs-department.md` "Department-managed
entities + delivery modes" + "When to elevate to managed entity"
discipline.

- **Why**: real businesses have entities that span departments —
  Client and Actor (person) are the canonical examples. Every
  department references them: Project.client (planning),
  Invoice.client (invoicing), Timesheet.actor (PM),
  AuditEvent.actor (office-level). Without first-class shared
  entities, cross-department workflows have client/actor data
  drift from day one. This is what enterprise systems call
  Master Data Management — but kept light per the entity-
  elevation discipline.
- **Justification per the 3-test discipline**:
  - **Client**: stable identity (yes — across years), state of
    record (yes — contact, billing terms, conflict flags),
    lifecycle (yes — active/dormant/terminated). ✅ entity.
  - **Actor (person)**: stable identity (yes — person persists
    across sessions/years), state of record (yes — role,
    contact, email), lifecycle (partial — joined/active/left).
    ✅ entity. Today's `office-config.actors[]` is semi-typed
    config; #15 promotes Actor to first-class native managed
    entity.
- **Concrete deliverables**:
  - **Office-level managed entities concept** introduced —
    `extensions/office/entities/<entity>.py` (parallel to
    `extensions/department/<dept>/entities/`); entities owned
    by the office substrate, not any single department.
  - **Client Pydantic schema** (native mode by default; adapter
    mode possible if a deployment uses external CRM).
    Fields: id (slug), display_name, billing_address,
    contact_persons (list of actor refs), billing_terms,
    conflicts_with (list of client refs), status, notes.
  - **Actor refactor**: migrate from `office-config.actors[]`
    semi-typed config to first-class Actor entity.
    `office-config` retains `actors_external_lookup_class:` for
    OAuth/SSO integration in #13's multi-user mode (adapter to
    BambooHR/Personio/Coolify SSO).
  - **MCP tools**: `list_clients`, `get_client`, `update_client`;
    same for Actor (or `list_actors`, etc.).
  - **Cross-department reference convention**: department
    entities (Project, Invoice, etc.) have `client_id: str`
    field referencing Client; gate validates the reference
    exists at write time. No FK enforcement at storage layer
    (per knowledge-graph-not-SQL principle); validation is at
    the gate.
  - **Migration**: existing `office-config.actors[]` migrated
    to Actor entities via schema bump (CURRENT_SCHEMA_VERSION
    bump + migration script).
- **Pattern-vs-instance check**: Office-level managed entities
  generalize. Every AI office has clients/customers and people.
  Pattern-level. ✅
- **Forward-compat with #13 (multi-user)**: Actor entity is the
  identity primitive for #13's multi-user auth. Gunther + colleague
  are two Actor entries; auth maps to Actor.id; AuditEvent.actor
  references Actor.id.
- **Role-based actors** (per session-9 followup #2 broader review):
  Actor entity gains `roles: list[str]` field (open-ended;
  deployment-configurable values like "principal", "practice-lead",
  "admin", "junior", "contractor", "regulator", "client-contact").
  Auth integration in #13 maps roles to permissions; cross-
  department workflow rules can reference roles ("Invoice >€10K
  needs role=principal approval").
- **Order note (revised session 11)**: schedule **AFTER #9**
  (generic entity gate available for Client + Actor implementation)
  **BEFORE #6** (audit-trail v2 retrofit references Actor;
  approval event kinds reference Actor for `approving_actor`).
  The original "AFTER #13" rationale was multi-user-auth-binding;
  under runtime-fabric-first re-ordering, the Actor data model
  (Pydantic + MCP tools) lands first, and #13's auth binds to it
  later. Net: #15 is now position 2 in remaining queue
  (was position 3).
- **Scope**: 1-2 sessions — Pydantic schemas + MCP tools +
  office-config migration + cross-department reference convention
  documentation.
- **Per #16 constraint (session 10)**: Client + Actor entity
  definitions land **as md files** at `extensions/office/entities/
  clients/<id>.md` and `extensions/office/entities/actors/<id>.md`,
  following the three-layer frontmatter contract. Layer-2 fields
  spec'd in `docs/decisions/ai-as-runtime-hybrid-shape.md`. Body
  conventions: Client uses `## Communication preferences` /
  `## Billing conventions` / `## Project history summary` /
  `## Watch-outs`; Actor uses `## Role + responsibilities` /
  `## Working preferences` / `## Capabilities + limits`.

**16. AI-as-runtime hybrid-shape contract — entity-md +
manifest decomposition + gate generalization** (session 10) —
see `docs/decisions/ai-as-runtime-hybrid-shape.md` +
ARCHITECTURE.md "AI-as-runtime hybrid-shape principle" section.

- **Why**: existing `extensions/universal/doctypes.yaml` +
  `references-manifest.yaml` files contain prose squeezed into
  YAML block scalars (`description: >`, `notes: |`). The notes
  fields ARE the rule (when does §13a apply, what to verify in
  fetched text) but block-scalar form suppresses the form prose
  wants to take — no headings, no structured lists, no links, no
  examples. ProjectState/state.md already uses the hybrid pattern
  (frontmatter + md body) but it hasn't been generalized.
  Generalizing now is upstream of #11 (locks `department.yaml`
  format), #15 (locks Client/Actor entity shape), and #9 (central
  design lens for managed-entity concept).
- **Scope (session 10)**: principle locked + ARCHITECTURE
  discipline added + ROADMAP slot inserted + downstream
  constraints flowed. **No migration this session** — bundled into
  #9 (doctypes) + Phase 1 corpus (references) + #11
  (department.yaml format, never persisted as pure YAML to begin
  with).
- **The principle, stated**: *Domain semantics, process flow,
  conditional rules, and contextual knowledge live in markdown
  bodies attached to entity files — not in encoded schemas or
  hardcoded skill procedures. Cross-domain portability is achieved
  by AI reading prose, not by abstracting over schema variants.
  Structured layers reserved for interfaces, identity, persistence,
  machine contracts; everything else is prose; AI is the runtime
  that fuses them at use-time.*
- **Three-layer frontmatter contract**:
  - **Layer 1 (universal, strict-locked, Pydantic base)**: `id`,
    `label`, `type`, `scope`, `scope_key`, `status`,
    `last_updated`, optional `description`, optional `tags`. The
    `type:` field routes to Layer-2 Pydantic subclass at gate.
  - **Layer 2 (per-entity-type, strict-locked, Pydantic
    subclass)**: doctypes have `style_ref` / `master_file_pattern`
    / `paired_with` / etc.; references have `source_url` /
    `canonical_path` / `fetch_method` / etc.; projects have
    today's ProjectState fields (relocated). Each type's
    frontmatter locked against its subclass.
  - **Layer 3 (per-deployment extension fields)**: deferred to #9.
- **Body conventions** (recommended-not-enforced; warned by audit
  + design-review skills, NEVER blocked by gate). Per-entity-type
  body specs at `docs/conventions/entity-md-spec.md`
  (authored alongside Layer-2 schemas in #9).
- **Where conditional rules live**: rules about *when* something
  applies belong with the *process*, NOT the entity. Process-as-md
  per verfahren (`extensions/department/planning/processes/
  beschleunigtes.md` etc.) declares which doctypes its flow
  produces; the doctype md describes what the doctype IS.
  Resolves the "Umweltbericht required when §13a doesn't apply"
  ambiguity.
- **MCP gate generalization**: generic `read_entity(path)` /
  `write_entity(path, file)` with `type:`-field dispatch to the
  appropriate Layer-2 Pydantic subclass. Replaces per-entity-tool
  sprawl. Body preserved as-is across read/write cycles. Lands
  in #9.
- **Audit slice 21** (added to audit skill): scans
  `extensions/**/*.md` entity files for Layer-1 + Layer-2
  frontmatter conformance + body recommended-section presence.
  Implementation bundled with #9.
- **Design-review target 12** (added to design-review skill):
  when authoring or modifying an entity md, validates frontmatter
  against the appropriate Pydantic subclass + suggests missing
  recommended sections. Coordinates with target 11
  (entity-elevation discipline). Implementation bundled with #9.
- **Design-review targets 13 + 14** (session 10 followup —
  review-mechanism gap addressed): user noted that prior audit +
  design-review passes never surfaced the hybrid-shape gap.
  Hypothesis (codified): existing modes catch deviations from
  *named* disciplines; neither catches *missing* disciplines
  themselves. Two new targets close the gap structurally:
  - **Target 13 (pattern emergence / unnamed convergence)**:
    bottom-up scan for ≥2 surfaces converging on an unnamed
    pattern; flag for elevation. Catches "silent convergence"
    failure mode.
  - **Target 14 (discipline-gap detection)**: top-down scan of
    failure-mode catalog vs named disciplines; flag uncovered
    modes. Catches failure modes not yet visible as code-level
    convergence.
  - Load-bearing reference:
    `plugin/skills/design-review/references/failure-mode-catalog.md`
    (new) — living catalog seeded with session-10 postmortem +
    literature-derived modes (silent convergence, prose-in-
    block-scalars, encoded-rules-when-AI-was-available,
    SQL-DB-trap, source-of-truth ambiguity, config-vs-code
    drift, hardcoded-instance-content, vendor-lock, cargo-cult,
    monolithic skill, implicit contracts, hidden global state,
    workflow-as-data, premature elevation, distributed-systems
    failures).
  - **First-runs scheduled sessions 11-12** (light cadence;
    independent of #11). Annual cadence thereafter, plus after
    every architectural surprise.
- **Entity-md spec doc**
  (`docs/conventions/entity-md-spec.md`): single source of truth
  for the hybrid-shape contract implementation — file layout +
  Layer 1 frontmatter (every entity, snake_case, ISO 8601 dates,
  kebab-case ids) + Layer 2 scaffold per entity type (grows in
  during #9) + body section conventions per type (h2 top-level,
  h3 sub, no h1) + cross-ref syntax (no wikilinks) + validation
  expectations. Audit slice 21 + target 12 validate against
  THIS doc, not against ARCHITECTURE prose.
- **Pattern-vs-instance check**: principle generalizes. Legal
  practice (cases get state.md-shape, precedents become reference
  entities), research-paper review (manuscripts get state.md-shape,
  citations become reference entities), engineering-doc workflows
  (specs get state.md-shape, RFCs become reference entities) —
  same shape, different prose per domain. Pattern-level. ✅
- **Connection to existing disciplines**: applies AFTER
  entity-elevation 3-test verdict; IS how pattern-vs-instance
  cross-domain portability is achieved; complements glue-not-
  replacement (adapter-mode entities use the same contract);
  respects strict-validation (Layer 1 + Layer 2 fail-loud); body
  unconstrained by design.
- **Order note**: **POSITION 1 in pre-RAG queue, BEFORE #11.**
  Same shape as session 9's #12 work — single-session
  decision-heavy slot, no implementation. #11's
  `department.yaml` format must adopt hybrid-shape from
  inception, NOT pure YAML.
- **Scope**: 1 session of dedicated framing-pass work (session 10
  produced the deliverables above). No further #16-only sessions
  needed; downstream migration work happens during the commitments
  it constrains.

**17. MCP gate coverage comprehensiveness review** (session 10
followup-3 — scoped from user-flagged concern post-hybrid-shape
work).

- **Why**: meta-rule 4 promises that contract-bearing reads +
  writes go through MCP gates. Slice 16 (validation-gate
  coverage) checks per-Pydantic-model **strictness** of
  EXISTING gates. **Comprehensiveness** — "which surfaces lack
  gates that should have them?" — is a different scan,
  currently uncovered as discipline-shaped check. User flagged
  during session 10 followup; codified as failure-mode-catalog
  entry (`incomplete-gate-coverage`).
- **What this commitment produces**:
  - Comprehensive sweep of all contract-bearing files / file
    types in the repo (today: `state.md`, `office-config.yaml`,
    `audit_trail/*.json`, manifests, bausteine, project-`_ai/`
    files; post-#9 + #11 + #15: new entity-md surfaces).
  - For each: gate present? Strict enough? If absent, propose
    gate name + sketch.
  - Decision: scaffold as **slice 23** (comprehensiveness scan,
    parallel + paired with slice 16's strictness scan and slice
    22's wrong-shapes-solvable scan) OR one-off review session
    output. Lean toward slice 23 — gives re-run cadence as new
    entities land.
  - Failure-mode-catalog entry `incomplete-gate-coverage`
    coverage status updated from `partial` to `covered` once
    delivered.
- **Order note (revised session 11)**: position 5 in remaining
  queue — execute AFTER #9 entity gate + #15 Client/Actor + #6
  audit-trail v2 + #7 bootstrap-write have landed, BEFORE #11
  Cowork integration. Reason: #17 surveys real gates produced by
  the runtime-fabric-first wave; running #11 (Cowork integration)
  on already-reviewed gates is the goal. The original "between
  #15 and #6" position predates the runtime-fabric-first
  re-ordering.
- **Dependencies**: requires #9 entity gate generalization
  having landed (post-#9 entity-mds are evaluated against the
  new generic gate, not the per-entity tools).
- **Scope**: 1 session for the survey + slice 23 scaffolding.
  Implementation of any new gates uncovered: per-gate
  sub-tasks, scoped per finding.
- **Per #16 constraint (session 10)**: surveys the new
  `read_entity` / `write_entity` generic gate (post-#9) AND any
  new manifest or office-level entity gates introduced by
  #11/#15. Confirms hybrid-shape entity files all flow through
  the generic gate, not direct filesystem Read.

**6 (expanded)**: per session-9 followup #2, commitment #6's
scope gains **approval event kinds** (`approval_requested`,
`approval_granted`, `approval_rejected`) on AuditEvent. Approval
flows are event-driven, NOT entity-shaped — the thing being
approved is an entity (Invoice, Project-submission); the approval
chain is in its event history. Authorization rules ("Invoice
>€10K needs partner approval") live in skill logic, not entity
schema. Folds into #6 because it's already adding event kinds
(`user_confirmation`); approval kinds add cleanly with no new
infrastructure.

**Recommended next-session order** (revised session 11 —
runtime-fabric-first re-ordering):

```
Session 8:    #10 (A2A + Gemini emulation gate)          1 session   ✅ DONE
Session 9:    #12 (department modularization design)     1 session   ✅ DONE
Session 10:   #16 (AI-as-runtime hybrid-shape contract)  1 session   ✅ DONE
Session 11-13: #9  (Department contract + managed-entity + generic entity gate)  2-3 sessions
Session 14-15: #15 (Client + Actor as office-level managed entities)              1-2 sessions
Session 16-18: #6  (audit-trail v2 retrofit)                                      2-3 sessions
Session 19:    #7  (bootstrap-write MCP tools)                                    1 session
Session 20:    #17 (MCP gate coverage comprehensiveness review)                   1 session
Session 21-25: #11 (Cowork integration refactor)                                  3-5 sessions
Session 26-28: #13 (deployment flex + Coolify reference deployment)               2-3 sessions
Session 29-30: #8  (pre-action framing skill)                                     1-2 sessions
Session 31+:   C → D
              + #14 (Memory Bank) bundled with Phase 1   2 sessions
```

The reasoning (revised session 11):
- **A2A first, department modularization second, hybrid-shape
  third** — already shipped sessions 8-10. Each was a single-
  session decision-heavy slot that informed everything downstream.
- **Runtime fabric next (#9 → #15 → #6 → #7)** — these unlock
  real project work. #9 produces the generic entity gate
  (`read_entity` / `write_entity` with type-field dispatch to
  Layer-2 Pydantic subclass) — load-bearing for every later
  consumer. #15 (Client + Actor) is the first downstream
  consumer; #6 retrofits audit-trail v2 against the gate +
  Actor refs; #7 closes the bootstrap-write meta-rule 4 gap.
  Without these, no project can be bound + operated.
- **#17 (gate coverage review) right after** — natural review
  checkpoint once entity gate + new entity types have landed.
  Surveys real gates, not yet-to-be-written ones.
- **#11 (Cowork integration) sixth** — when skills get reshaped
  to Cowork form (slash commands, `department:` frontmatter,
  `pbs.local.md`), every skill is **already in final
  backend-tools shape from #6/#7 retrofits**. Single skill-touch
  pass instead of double-touch.
- **#13 (deployment flex + Coolify) seventh** — needs Cowork
  plugin shape settled (original logic preserved). Multi-user
  auth binds to Actor entity (which #15 already produced).
- **#8 (framing skill) last** — codifies the pattern-vs-instance
  reasoning #9 produces into repeatable skill.

**What changed vs the prior session-10 order**: #11 + #13 moved
from positions 1-2 (preparation refactors for runtimes the user
isn't using yet — Cowork end-user mode + Tier-2 cloud) to
positions 6-7. #9 moved from position 7 to position 1 because
#16's hybrid-shape principle made the generic entity gate
load-bearing for every subsequent commitment — building #11/#15
without it forces either per-loader hacks (creating exactly the
silent-convergence failure mode #16 is meant to prevent) or
one-off gates that #9 has to refactor away. The "examine stable
schemas" rationale for #9-last predates the session-9 reframe;
#9 no longer extracts a universal core, it designs the contract
from scratch, and the downstream commitments are the consumers.

All thirteen items: pre-RAG architectural commitments. Phase 1
corpus download unblocks pending sections B (audit-trail
single-write integration per v2), C (sparring-output integration),
D (plugin version bump), and the Phase 0 items 4 (feature-survey
skill) + 5 (testing methodology) per HANDOFF.md.

### Marketing + branding strategy (pre-launch todo)

**Status**: not yet defined. Open question flagged here so it doesn't get lost in the architectural-work queue. NOT a pre-RAG commitment; lands before any public consulting launch.

**What needs to be decided** (slow-moving, durable choices — not tactics):

- **Brand identity** — what's the consulting practice called? Options: "Gunther Schulz" (personal brand), "pbs-bureau" (artifact name reused), or a third brand (e.g., "AI Office Architecture" or similar). Each has tradeoffs (personal-brand limits scale; artifact-reuse confuses framework-vs-consulting; new brand needs separate building). Resolve before public launch artifacts.
- **ICP (Ideal Customer Profile)** — formal definition: domain / size / budget / pain / decision-maker profile. Today implicit ("solo professionals + small companies in expert-practitioner domains"); needs formalization for sales discipline.
- **Channel priorities** — broad ordering only (not specific tactics). Where does lead generation start: open-source repo + blog + conference talks; or also Twitter/LinkedIn; or also podcasts; etc. Prioritize the high-leverage few.
- **Content pipeline themes** — categories that compound (decision records as essays; comparative architecture writing; public design-review sessions; case studies post-deployment); not specific posts.
- **Domain / website strategy** — does pbs-bureau.com or guntherschulz.de or a new domain anchor consulting? Connects to brand identity decision.

**What's intentionally NOT in scope here**:
- Specific conference submissions (depend on what's accepting when launch happens)
- Specific blog post drafts (write when ready to publish)
- Pitch deck (build per first concrete prospect; varies)
- Pricing / proposal templates (depend on first 1-3 engagements as calibration)
- Visual brand identity (logo, palette, etc. — defer until brand-name decision is made)

**Pull-forward trigger**: before any public launch / open-source-repo announcement / first consulting outreach. The brand identity decision in particular is a one-time choice; making it before launch is much cheaper than rebranding after.

**Output (when activated)**: marketing/branding section added to `docs/strategic-positioning.md` (or sibling `docs/marketing-strategy.md` if substantial enough); decisions captured; pre-launch checklist resolved.

**Connection to existing positioning**: `docs/strategic-positioning.md` already covers strategic positioning, competitive landscape, sharpest-pitch drafts, lived-experience credibility. The marketing/branding workstream operationalizes that strategic content — what brand voice carries it, which channels distribute it, who's the audience.

### Strategic milestone — Schulz Planungsbüro as exit / "AI-augmented business" sale (session 7, user-articulated)

**The framing**: Gunther's father (co-founder of Schulz
Planungsbüro) is approaching retirement. PBS-bureau's natural
strategic endpoint is positioning the bureau for sale as an
**AI-augmented planning business** — i.e., the buyer acquires
the bureau (clients, contracts, reputation) PLUS the AI office
that has captured institutional knowledge (bausteine = how the
bureau argues §45 cases, state.md per project = lifecycle
history, audit trail = decision provenance, manifests = current
legal references, korrektur-rules = style discipline). The
buyer gets faster ramp + lower headcount requirement than
traditional bureau acquisition.

**This is a strategic context note, not a commitment.** It
exists in the roadmap to make the **timeline pressure explicit**:
PBS's pre-RAG completion + first real-project track record need
to land before father's retirement window for the "AI-augmented
business" sale story to be credible. **Slipping pre-RAG closing
puts this strategic exit at risk.**

**What's strong about this exit story**:
- Captures expertise that traditional bureau sales lose
  (retiring planner's tacit knowledge)
- Audit trail + bausteine + decision records ARE transferable
  IP in a way "tribal knowledge" isn't
- Coolify deployment makes technical handover concrete (clone,
  change auth, done)
- Differentiated story for buyers: "you're acquiring decades of
  planning expertise, encoded"

**What's harder than it looks (honest read)**:
- Knowledge transfer is **partial, not total** — bausteine +
  audit capture explicit reasoning; relationships with UNB
  Sachbearbeiter, negotiating instincts, "feel" for context-fit
  do NOT fully transfer. Realistic buyer is **another planner +
  AI-augmentation**, not a non-planner running the AI alone.
- "AI business" framing might oversell — today's PBS is
  augmentation, not autonomous operation. Buyers may discount.
  "AI-augmented planning bureau" is more honest framing for
  pricing discussions.
- Valuation premium requires **case study evidence** (headcount
  reduction, ramp acceleration shown in real numbers); without
  it, premium argument is theoretical and won't land in
  negotiation. The next 1-2 years of real PBS operation
  generate this evidence.
- Buyer pool is narrow: another planning bureau consolidating;
  construction/dev company acquiring planning capacity in-house;
  PE-style "AI rollup" play. Niche resale.
- **Timeline pressure is real and asymmetric**: father's
  retirement timeline (assume 1-3 years) vs PBS maturation
  realistic timeline (12-24 months from session 7 close). Cuts
  it close.

**Implications for the rest of the roadmap**:
- Pre-RAG completion timeline becomes **load-bearing for the
  exit story**, not just for PBS itself
- First real project work needs to start as soon as Phase 1
  corpus + first project bind are possible (post-RAG)
- Generate explicit case-study evidence (project counts, error
  catches, time savings, decision-trail completeness) during
  real operation
- Documentation discipline (decisions.md, audit trail, etc.)
  pays back at sale time — they're the buyer-facing evidence
  of "the AI captured the knowledge"

**Connection to AI-office-builder vision (v2)** and the
consulting offering:
- Selling Schulz Planungsbüro as the **first proven AI-augmented
  business** is the single best validation event for the
  AI-office-builder v2 vision and for the consulting business
- Validates the "AI office captures transferable expertise" thesis
- Generates the case study that makes consulting credible
- Establishes "AI-augmented business" as a recognized category
  (precondition for marketplace platform — see v2 entry)

**Status**: strategic context, not a commitment. No work item
attached. Re-evaluate annually + before any major roadmap
re-prioritization. The most concrete consequence right now is
**urgency on pre-RAG completion** — every commitment slip
shortens the window for the exit story to be credible.

### Pioneer-instance validation strategy

**Why**: Per VISION.md "PBS as pioneer instance" — a one-user
prototype generates thin validation. Risks (survivorship bias,
architectural over-fitting, sparse evidence sample, confirmation
bias) are real. Without explicit validation strategy, the
pioneer claim relies on "Gunther uses it and it seems to work"
— too thin to support proving-ground or research-lab purposes.
Compounded by current market reality: project density may be
sparse for a while; validation can't wait for projects to pile
up.

The question to answer: **what counts as valid evidence for an
early-mover prototype with sparse real-world tests?**

**Sketch — four complementary evidence types** (directly
addresses risks named in VISION.md):

- **Architectural validation** (cheap, immediate). Tests
  whether the architecture works mechanically — skills
  compose, layered manifest scope filtering operates,
  source-grounding fires, audit trail records what's expected,
  frontmatter dependency declarations resolve correctly.
  Doesn't require real projects; build as backend test suite
  with per-meta-rule invariants. Closest evidence type to
  unit-test discipline applied at the architecture level.

- **Failure-mode probing** (cheap, immediate). Stress-test
  the trust + sparring infrastructure under deliberate
  adversarial conditions — ambiguous citations, conflicting
  Stellungnahmen, intentionally weak argumentations,
  sycophancy bait ("don't you agree this looks fine?"),
  source-grounding evasion attempts. Verify guardrails
  actually fire under stress. Build as validation harness
  with reusable adversarial scenarios; runnable on demand.

- **Historical project replay** (medium effort, own data).
  Run PBS on past projects (without the AI seeing the actual
  sent versions); compare AI's drafts + reasoning chains
  against what was historically shipped. Catches over-fitting
  to user style; tests whether patterns reproduce expert
  judgment over PBS's own track record. Confirmation-bias
  risk: same person designed both architecture and originals,
  so agreement isn't independent verification.

- **Mock project + peer review** (medium effort, external
  input — user's original suggestion). Construct realistic
  synthetic project; another planning professional (Hendrik
  first, possibly others later) reviews PBS outputs. Their
  verdict: would they sign this? Would they have caught what
  AI missed? What's wrong, structurally or fachlich?
  Strongest external-validation path that doesn't depend on
  real client work.

Four distinct evidence types: **architecture / stress / own-
baseline / external-professional**. None requires waiting for
the next real project. Together they generate substantive
evidence even during low-project-density periods.

**Deferred (more ambitious, higher setup cost)**:

- Compare against published professional standards
  (Bauleitplanung leitfäden, BMI guidance, BBSR examples).
- Hypothetical model cases (publicly discussed regional
  planning challenges; PBS as if commissioned).
- Replay published BVerwG case law (simulate PBS at the time
  of a real dispute; compare against actual court outcome).
- External presentation as IP-transferability test (paper,
  conference, demo with feedback collection).

**Pull-forward triggers**:

- PBS becomes operational (Tier 1 MCP + alignment sweep + RAG
  kickoff complete). Validation should start at first
  operational use, not at first crisis.
- Project density stays low for >1 month — evidence
  accumulation via real work too slow to be sole strategy.
- First consulting / second-deployment conversation surfaces —
  need transferable evidence to share.

**Open questions** (refine and prioritize at task #21
pre-RAG audit; by then operational reality will inform
trade-offs):

- Effort budget per session: validation vs. real work split?
- Where does evidence land — per-type log files? new
  `evidence/` tree alongside `memory/`? Within the audit-trail
  ROADMAP item?
- Decision criteria: when does accumulated evidence justify
  productization, scope expansion, or external publishing?

### SKILL.md version-bump reminder hook

**Why**: Per meta-rule 4 (execution-determinism), hooks earn their keep on out-of-band
detection. Pure-advisory exception worth a 5-line
PostToolUse hook: when `plugin/skills/**/SKILL.md` is edited,
remind to bump `version:` and run `dev-link.sh`. No data
integrity at stake — just discipline.

**Order**: defer until a real version-bump miss causes friction.
Cheap to add later.

### Email adapter implementations

**Why**: integration adapter scaffolding is in place
(`backend/.../integrations/email/{protocol,none}.py`) — but no real
adapter yet. v1 has manual `.eml` drop into
`<project>/Schriftverkehr/eml/`. For complete project context the
assistant needs full inbox access; manually-saved `.eml` files are a
curated subset.

**Sketch**: first concrete adapter is `thunderbird-maildir.py` —
polls Thunderbird's local maildir/mbox at
`~/.thunderbird/<profile>/Mail/`, filters by domain whitelist +
project-keyword matching, drops matched messages into the right
project's `Schriftverkehr/eml/`. Implements
`pbs_mcp.integrations.email.protocol.EmailAdapter`. After that:
`imap.py` for self-hosted offices.

### Phone call note format

**Why**: `Schriftverkehr/telefonnotizen/` is a planned folder but no
spec exists for what a call note file should contain.

**Sketch**: small markdown spec — frontmatter (date, party,
contact, project, type=call, duration), body sections (Kontext,
Zusammenfassung, Entscheidungen, Folgeaktionen). Could be authored
into `<repo>/memory/universal/` as a reference content file. Future
integration: `phone.adapter: call-log-csv` reads a phone-system CSV
export and proposes call-note creations.

### Domain manifest population — Innenentwicklung

**Why**: `extensions/domain/Innenentwicklung/references-manifest.yaml`
is currently a skeleton. Will need population when first office with
this domain (urban planning, no renewables) deploys, OR when PBS
takes on an Innenentwicklung-only project.

**Sketch**: candidates — Difu-Leitfäden, BBSR-Veröffentlichungen,
BVerwG-Rechtsprechung zu §13a/§13b BauGB. Use `author-manifest`
already-existing skill to seed; `research-references` populates.

### Agentic retrieval — iterate searches per claim, not per section

**Why**: Current RAG pattern (planned for first-run) is bulk: skill
issues one or a few `search_corpus` calls per drafting section,
stuffs results into prompt, drafts. State-of-the-art is *agentic*:
the orchestrator iterates one search per claim during drafting —
fetches §44 BNatSchG when about to write the §44 sentence, fetches
the BVerwG-Freiberg ruling when about to cite CEF-Wirksamkeit.
Better citation grounding (each claim has its own retrieval), less
context bloat (no over-fetching upfront), more natural for Claude.

**Sketch (post-first-run)**:
- Mostly a skill-protocol question, not infrastructure. Update
  `draft-textteil-b` / `draft-textteil-c` / `draft-cover-mail`
  protocols: instead of "fetch all sources at start", say "before
  each citation-bearing claim, search for the supporting reference,
  cite from the result."
- The MCP backend (`search_corpus`, `read_corpus_file`) already
  supports per-call retrieval — no backend change needed.
- Source-grounding rule strengthens naturally: every cited §-ref
  is backed by a tool call in the same drafting turn.

**Open questions**:
- Latency: many small searches per draft vs few large ones. With
  bge-m3 + CUDA the per-search cost is low; the question is total
  drafting wall time.
- Hybrid: bulk-fetch the obvious universal references (BauGB-
  framework) once at start, agentic-fetch the specific cites?
- When to evaluate: after first-run sample-searches show whether
  the bulk pattern produces grounded enough citations.

### Late-interaction retrieval (ColBERT-v2)

**Why**: Current stack uses bge-m3 (single-vector dense embedding)
+ a cross-encoder reranker. State-of-the-art for long technical /
legal text is often *late-interaction* models like ColBERT-v2 —
token-level retrieval that scores fine-grained matches without the
bottleneck of compressing the whole document into one vector.
Particularly strong on German legal text where exact-phrase
matching matters.

**Sketch (conditional)**:
- **Trigger**: only if first-run sample-searches show quality
  issues — bge-m3 + reranker is the right baseline; don't preempt.
- **Drop-in**: ColBERT-v2 has Python implementations (PLAID,
  RAGatouille) that slot under the same `search_corpus` interface.
- **Trade-off**: late-interaction stores more per chunk (token-
  level vectors), so disk/memory footprint grows. RTX 5090 + 32GB
  VRAM handles it but the LanceDB schema needs adjusting.

**Open questions**:
- Evaluation set: need a small benchmark of "for query X, the right
  reference is Y" pairs to objectively compare bge-m3 vs ColBERT
  on PBS's actual corpus.
- Coexistence with multimodal page-image retrieval (ColPali — see
  next item): probably both, used for different content kinds.

### Query rewriting (HyDE + decomposition + expansion)

**Why**: We have ZERO query rewriting today. User/skill issues a
literal-keyword query → gets dense-retrieval matches. State of the
art rewrites the query before retrieval to bridge vocabulary gaps:
- **HyDE** (Hypothetical Document Embeddings): the model first
  drafts a hypothetical answer, embeds *that*, retrieves against
  the corpus. Catches paraphrase mismatches.
- **Decomposition**: split a multi-part query into sub-queries,
  retrieve each, union.
- **Expansion**: add synonyms / variants ("§44 BNatSchG Tötungs-
  verbot" → also search "Tötung Verbot §44", "signifikant Tötungs-
  risiko §44").

**Sketch**:
- HyDE for **baustein retrieval** (find similar bausteine when
  user is about to write a similar argument): the most natural fit.
- Decomposition for **multi-§-claim drafting**: a sentence that
  cites BauGB §13a and BNatSchG §44 issues two retrievals.
- Expansion for **legal lookup**: deterministic, can be a
  preprocessor on top of search_corpus.
- **save-baustein dedupe** — paraphrase the candidate in 3 variants,
  search each, union, decide if duplicate. Currently no dedupe
  guard in place at all.

**Open questions**:
- Where to apply: query-rewrite as preprocessor in the MCP backend
  (transparent to skills), or as an explicit skill responsibility?
  Likely backend for cheap variants (expansion), skill for HyDE
  (needs the model in the loop).
- Rewriting cost: HyDE adds one model call per search. Acceptable
  for high-stakes (drafting), maybe too much for bulk operations.

### Multimodal RAG (page images, tables, scanned PDFs, copy-protected PDFs)

**Why**: Current ingest pipeline is text-only. We lose:
- **Diagrams** in KNE-Anlagengestaltung (Modulreihen-schematics,
  row-spacing), KNE-Standortsteuerung (decision flowcharts).
- **Charts** in BfN-Schriften 705 (Agri-PV adoption, land-use).
- **Tables** in Helgoländer Papier (species × distance recommen-
  dations) — text-extracted tables often arrive mangled.
- **Maps** in LUNG-MV-Artenschutzleitfaden (Bestandskarten,
  Schutzgebiete).
- **Future Kartierberichte** from Hendrik — fundamentally visual
  (maps, distribution plots, habitat photos). Pure-text RAG would
  be useless for these.

**Sketch (4 sub-pieces)**:

1. **Page-image retrieval (ColPali / Nomic Vision)** — embed each
   PDF page as an image; query → page images; Claude (vision-
   capable) reads them. Lowest pipeline complexity; decent quality.
   Coexists with text-RAG (text for keyword-precise, images for
   "I need to see the diagram").

2. **Targeted table extraction** — Camelot / Tabula / Unstructured
   detects tabular blocks at ingest, extracts as structured records.
   Helgoländer-style species×distance tables become symbolic
   queries ("min distance for Schreiadler"). High value where it
   applies; not every PDF has tables worth this treatment.

3. **Scanned PDFs (OCR)** — many older Verfahrenserlasse, archived
   Stellungnahmen, scanned Behörden-correspondence are image-only
   PDFs with no embedded text. Need OCR at ingest. Tools:
   `ocrmypdf` (wraps tesseract; preserves PDF structure +
   adds searchable text layer), `tesseract` direct + custom
   reconstruction. German-language model essential.

4. **Copy-protected PDFs** — KNE/BfN/Verlag-published leitfäden
   sometimes ship with DRM (printing/copying disabled, sometimes
   password-protected). For internal RAG ingest of legitimately-
   acquired material we need a removal path:
   - `qpdf --decrypt` for owner-password DRM (most common,
     trivial to strip)
   - `pikepdf` (Python; same backend) for programmatic ingest
   - `mutool clean -d` (MuPDF) as fallback
   - Investigation: which DRM kinds appear in PBS's actual
     publisher mix; which tool handles each cleanly.
   - Legal: DE Privatkopie / wissenschaftliche Eigennutzung law
     covers internal-use ingest of legitimately-acquired material;
     redistribution is separate. Document the policy.

**Recommended architecture** (decided):

| Step | Who | Why |
|---|---|---|
| Pre-process PDFs at ingest (page render, OCR, table extract, DRM removal) | Local Python tools | Deterministic, one-shot |
| Embed page images for retrieval | Local ColPali on RTX 5090 | Bounded corpus, consistency with bge-m3 text-RAG |
| Match query → page images | Local LanceDB | Same store as text-RAG |
| **Read and reason about returned images** | **The Claude session itself** | Already in the loop, vision-capable, has project context |

The orchestrator runs IN a Claude session — Claude is already
vision-capable. MCP backend returns image bytes (new tool
`read_corpus_page_image` or extension to `read_corpus_file`); the
session passes them as image content blocks; Claude reads + reasons
directly. No separate vision-LLM deployment needed for interactive
work.

A separate local vision model (Llama 3.2 Vision, Qwen2-VL, Pixtral)
or API vision call is only needed for **batch/headless** processing
that runs outside a live Claude session — e.g. a future
"weekly auto-scan new Stellungnahmen for action items" cron. Defer
that until such a use case lands.

**Open questions**:
- Coexistence: page-image retrieval + text-RAG returning different
  hit kinds — how does the orchestrator decide which to send to the
  model? Probably hybrid retrieval that includes both kinds in
  candidate pool, reranker decides.
- Storage cost: page images are large; LanceDB blob storage or
  filesystem references?
- Token-budget control: every multimodal hit means image bytes in
  the context. Cap on images-per-turn?
- Table extraction precision: structured tables are queryable but
  the extractor mis-identifies blocks. Need fallback to text+image.

### Structural retrieval (legal §-graph + project graph + verfahren state-machine)

**Why**: PBS corpus and project state are full of latent structure
that text-only retrieval ignores. Recurring pattern observed in
this session: we keep designing things text-first and finding
ourselves needing a graph or registry later (integration registry,
audit trail are exactly this — formalizing what's currently
implicit).

**Meta-principle**: when something is queried by attribute /
capability / relationship, design it as data, not prose.

**Three concrete graphs**:

1. **Legal §-graph** — §44 BNatSchG cites §15, §1; BVerwG-9-A-22-13
   interprets §45 Abs.7 Nr.5; KNE-Anlagengestaltung references
   §44 Abs.1; LUNG-MV-Artenschutzleitfaden tracks BNatSchG §44
   Anwendungspraxis. Today: nothing — keyword search only. Graph
   would let symbolic traversal: "find all rulings interpreting
   §45 Abs.7", "what cites this baustein's underlying §s".
   Built at ingest (extract §-references from law/ruling/leitfaden
   text), updated by research-references on each refresh.

2. **Project-cross-project graph** — projects × doctypes × phases
   × decisions × partners × clients. Today: state.md per project,
   no aggregation. Graph would answer "all PV-FFA projects in
   phase 5b with Hendrik as partner", "which projects share this
   client", "decision X across projects".

3. **Verfahren state-machine** — bauleitplanung-phasen.md is *prose*
   describing the 13 phases + transitions. Could be a state machine
   the orchestrator queries: "given current phase X, valid next
   transitions"; "what's required to fire transition Y". Used by
   orchestrator for phase-transition validation, by validate-
   checklist for "is this artifact ready for phase X" gates.

**Open questions**:
- Storage: LanceDB has no graph queries; SQLite + manual graph
  schema, or a real graph DB (Kùzu / Neo4j)?
- Maintenance: §-graph and project-graph need to update on every
  research-references run / state.md write. Build derived-data
  pipeline?
- Integration with audit trail (separate ROADMAP item): an audit
  event is naturally a graph-edge ("decision X was logged in
  project Y by partner Z at time T").

_(Skill-protocol refactor for iterate/rewrite patterns —
verify-citations, validate-checklist, survey-project,
Stellungnahme/Abwägung handling, save-baustein dedupe — promoted
out of ROADMAP into immediate next-session work. See HANDOFF.md
"Pending — first task next session.")_

---

## v1.x-v2 — when first project needs it

### Plugin / deployment shipping bundle

**Why**: PBS is designed deployable to other German Planungsbüros
(per ARCHITECTURE.md meta-rule 1: app vs office). What gets
shipped to a second office is currently undocumented. Without
a coherent bundle definition, second-deployment friction is
unknown and the deployment story stays implicit.

**Sketch (small doc, ~1 page)**: at `docs/deployment.md`:
- Plugin payload: `plugin/skills/`, `plugin/templates/`,
  `plugin.json`, `dev-link.sh`. Versioned via plugin.json.
- Backend payload: `backend/mcp-server/` with pinned deps.
- Memory payload: `memory/universal/` (knowledge content),
  `memory/bausteine/` skeleton (empty subdirs for layered
  scope), `memory/product-backlog.md` template.
- Extensions payload: `extensions/universal/` (manifests),
  `extensions/{domain,state}/` skeletons (placeholder dirs for
  unselected scope keys).
- Office-config: not shipped — generated by `setup-office` per
  deployment.
- Docs: README → setup-office, ARCHITECTURE.md, ROADMAP.md.
- What is NOT shipped: `_ai-references/` corpus, per-project
  data, office-config.yaml.

**Pull-forward trigger**: first concrete second-deployment
conversation (another Planungsbüro evaluates the app, or PBS
themselves wants to test fresh-install on a clean machine).

### Maps/GIS integration

**Why**: Joint Schulz+Hendrik projects use both PBS text-document
work AND Hendrik's GIS/QGIS workflow. Need clean coexistence of two
MCP servers + shared context.

**Components**:
- gis-utils MCP server (already exists as a separate plugin —
  `gis-utils@gis-utils`)
- pbs-bureau MCP server (this repo's backend)
- Communication / shared state at `<project>/_ai/state.md` with
  `practices: [schulz, hendrik]` flag

**Open questions**:
- Should Hendrik's per-project `CLAUDE.md` (workflow.yaml + scripts/)
  be readable by pbs-bureau orchestrator? Or strict separation?
- How do Karten/ outputs from GIS workflow get referenced in
  Begründung's cartographic citations?
- File-map.md interpretation for GIS folders.

### Python-ACAD-Tools app integration

**Why**: User maintains a separate Python tools app at
`~/dev/Gunther-Schulz/Python-ACAD-Tools/` for AutoCAD-style drawing
manipulation. Used for technical Zeichnungen (Planzeichnungen, V&E-
Plan layouts, Bestandspläne). Like gis-utils, this is a sibling tool
that the pbs-bureau orchestrator should be aware of.

**Components**:
- Python-ACAD-Tools as a standalone tool (likely with its own MCP
  server or CLI; verify current state at session start)
- Per-project `Zeichnungen/` folder is the natural integration point
  (similar to GIS/Karten/ in joint-practice projects)
- pbs-bureau may produce textual references to Zeichnungen
  (Begründung Section 14: "Kataster- und Vermessungswesen") and
  needs to know where the CAD outputs live

**Open questions**:
- Does Python-ACAD-Tools have an MCP interface, or CLI-only?
- Per-project workflow shape (workflow.yaml-style like gis-utils, or
  ad-hoc scripts?)
- Symmetry with gis-utils: same coexistence pattern, or different?

### Overleaf sync workflow detail

**Why**: Decided that LaTeX subfolders are git-init'd per project for
Overleaf sync. The detailed mechanics (GitHub-remote-creation,
branch protection, push triggers, conflict resolution) need
spec'ing.

**Open questions**:
- Auto-create GitHub repos on scaffold-project? Or manual?
- Branch protection: should pbs-bureau push to `main` or to a `draft`
  branch?
- Conflict resolution when Overleaf and local both edit?

### Audit trail — unified change/decision/version tracking

**Status**: PROMOTED to v1 commitment (session 6, 2026-04-29).
Initial design + Pydantic + MCP tools shipped. See decision record
at `docs/decisions/audit-trail-v1.md` and the v1 commitments
section near the top of this ROADMAP.

### Human-readable artifact generation at checkpoints

**Why**: Many workflow pieces are machine-readable (LaTeX source,
billing.md ledger, Stellungnahme YAML, baustein markdown) — but
humans review and discuss in their natural form (PDF, formatted
preview). Today only LaTeX has clean human-output via `compile_latex`.
Other kinds either have no checkpoint render or rely on ad-hoc
generation. We need a principle: at every meaningful checkpoint
(send-gate, phase transition, draft-invoice, baustein-promotion,
config-change), produce the human-readable artifact alongside the
machine state, so the human review step has something to look at.

**Examples**:
- LaTeX docs: PDF on every snapshot (already done)
- Invoices: PDF draft when `draft-invoice` runs (planned with PM item above)
- Stellungnahmen drafts: PDF for review before send-gate
- Cover mails: PDF/RTF for review before send
- Bausteine: when promoted to skill, show diff PDF or formatted view
- Config changes: human-readable summary of what changed (not raw YAML diff)
- Audit trail queries: rendered timeline view, not raw log
- Baustein freshness sweep: human-readable report PDF

**Sketch (topic-level)**:
- Convention: every checkpoint event has an associated render that
  produces a PDF (or HTML for interactive) at a predictable path.
- Backend tool family for renders (compile_latex already exists;
  add `render_invoice`, `render_stellungnahme`, `render_audit_timeline`,
  etc. as needed).
- Skills register their checkpoints + the render they produce.
- Renders are themselves versioned through the audit trail above —
  so we can show the user what the rendered checkpoint looked like
  at the time, not as it would render today.

**Open questions**:
- Render templates: per-office or universal? (Likely follows same
  3-layer LaTeX stack pattern: app shipping universal templates,
  office overlays for branding.)
- HTML vs PDF: when does interactive review (HTML) beat archival
  (PDF)? Probably both, with PDF as the canonical archival form.
- Storage: renders alongside source in snapshots/, or a separate
  renders/ tree?

### BPMN / workflow engine integration adapter class

**Why**: enterprises typically have **decades of investment** in BPMN engines (Camunda, Pega, jBPM, Bonita, Flowable) or workflow platforms (ServiceNow Workflow, SAP Workflow, Salesforce Lightning Flow). Selling rip-and-replace is a losing pitch. Per the **glue-not-replacement principle** (`ARCHITECTURE.md`), PBS positions as an **augmentation layer ON TOP** of these systems — adding judgment-mediated reasoning + drafting + audit-defensibility to existing automated processes without displacing the customer's investment.

This is a **position-of-strength entry** for enterprise consulting market. Activation trigger: first prospect with existing BPMN investment.

**Three integration patterns** (lightest to deepest):

1. **Service-task delegation** (lightest): BPMN service task ("draft cover letter", "summarize feedback", "check compliance") → calls PBS-bureau via HTTP MCP → relevant skill (`draft-cover-mail`, `review-draft`, `verify-citations`) produces output → returns to BPMN. BPMN tracks workflow state; PBS produces the unstructured artifact. AuditEvent in PBS includes `bpmn_process_id` + `bpmn_task_id` for cross-system traceability.

2. **Decision automation with sparring** (medium): BPMN has a "decide" task → PBS receives context → surfaces decision to user with sparring (per `sparring-output-v1.md` — challenge + alternatives + reasoning) → returns user-approved decision → BPMN records the outcome with AI-attributed reasoning chain. **The defensibility upgrade**: BPMN engines record "user X clicked approve" — PBS adds "user X approved with reasoning Y, after sparring on counter-arguments Z, considering alternatives W." That's auditor-grade.

3. **Cross-process intelligence layer** (deepest): PBS sits ABOVE multiple BPMN processes, watching their event streams via webhooks (per #9 Gap B adapter-emitted events), applying cross-process reasoning. "Process A (invoice approval) just completed → Process B (project archival) should evaluate readiness." Single-engine BPMN can't do this; cross-engine federation is exactly A2A territory (#10's defensive shape pays off here).

**Architectural fit (already supported)**:
- **BPMN-engine adapter class** per meta-rule 1: `bpmn-workflow-engine` adapter class with concrete adapters per vendor (`camunda-adapter.py`, `pega-adapter.py`, `servicenow-workflow-adapter.py`, `flowable-adapter.py`)
- **HTTP MCP transport** per #10 + #13: BPMN engine calls PBS via HTTP MCP; same transport as Cowork uses
- **Adapter-emitted events** per #9 Gap B: BPMN process state changes flow into PBS audit trail as `actor_kind=external_agent` events with `origin_agent_card=<bpmn-engine-url>`
- **Event subscriptions** per #12: departments subscribe to BPMN-emitted event kinds; cross-process intelligence emerges via the watch-list mechanism

**No new architectural primitives needed.** The infrastructure already supports BPMN integration as a special case of the integration-adapter pattern.

**Consulting positioning**:

> "Your BPMN engine handles the workflow. We handle the judgment, drafting, and audit-defensibility on top — without replacing your existing investment. Your process compliance documentation gets stronger; your tasks get smarter; your audit trail captures not just what happened but why."

This is **a much easier sell** to enterprise prospects than "replace your Pega" or "replace your Camunda." Positions PBS as enabling-existing-investment, opens partnership possibilities with BPMN vendors.

**Activation trigger**: first consulting prospect with substantial BPMN/workflow-engine investment (typically: enterprise legal practice, regulated industry, government). Not pre-RAG critical; activates when concrete demand materializes.

**Output (when activated)**:
- Decision record `docs/decisions/bpmn-integration.md` — adapter class design + concrete vendor adapter selection rationale
- BPMN-engine adapter Protocol at `extensions/department/<dept>/adapters/bpmn-workflow-engine/protocol.py`
- Concrete adapter for the prospect's specific engine (Camunda first, likely)
- Cross-system traceability convention (`bpmn_process_id` + `bpmn_task_id` in AuditEvent details)
- Reference deployment with the prospect's engine + PBS office; end-to-end test

### Integration registry — unified discovery of MCPs + adapters + skills

**Why**: PBS will accumulate many "things the orchestrator can call":
- Internal adapters (email, calendar, scanner, phone, accounting —
  Phase 5 scaffolded)
- External MCP servers (gis-utils, Python-ACAD-Tools, future
  review-platform MCP, future legal-search MCP, etc.)
- PBS-owned skills (16 currently — auto-discovered from
  plugin/skills/ but their utility/scope isn't queryable as data)

The orchestrator currently knows about these through tribal
knowledge (it knows `gis-utils` exists because the user has it
installed; it knows about `survey-project` because the SKILL.md
trigger fires). There's no unified registry where the orchestrator
can ask "what tools do I have for working with GIS data?" or "what's
available in the Wind domain that I could leverage?"

When a new MCP becomes useful (or new internal adapter, or new skill),
making it *known* to the orchestrator + queryable by capability is
itself a gap.

**Pull-forward triggers** (don't build until at least one fires):

- **Capability-vocabulary friction** — orchestrator string-
  matching tool descriptions becomes unwieldy; routing decisions
  are repeatedly wrong because the orchestrator can't query
  callables by capability.
- **Total callable count exceeds ~50** — current count is ~44
  (16 skills + 5 integration adapters + 22 MCP tools + 1 external
  MCP `gis-utils`). At this scale the orchestrator holds the
  inventory in context fine; at 50+ a registry pays off.
- **Second deployment** — PBS-only doesn't justify cross-office
  knowledge propagation; a second Planungsbüro adopting the app
  forces it (registry entries become reusable across offices).

Until at least one trigger fires, the Tier 1 `list_skills()` MCP
tool + frontmatter `mcp_tools_required[]` declarations + snake_case
tool naming convention (per ARCHITECTURE.md meta-rule 4) cover the
immediate need with forward-compatible string IDs.

**Sketch (topic-level)**:
- A 4th layered manifest type alongside references + doctypes:
  `integrations-manifest.yaml` per scope (universal / domain / state).
- Each entry catalogs ONE callable thing (MCP, internal adapter, or
  skill) with metadata:
  ```yaml
  - id: gis-utils
    kind: mcp                       # mcp | adapter | skill
    name: gis-utils
    description: GIS/CAD utility library — geometry conversion, recipes, templates
    scope_relevance: [PV-FFA, Wind, Naturschutz]   # which domains benefit
    state_relevance: []                              # any
    when_to_use: |
      Geometry conversion, lines→polygon, buffer/dissolve operations,
      checking recipe-layer compatibility, GIS-workflow authoring.
    capabilities: [geometry-conversion, workflow-authoring, recipe-discovery]
    docs_url: <plugin-docs>
    config_path: ~/.config/claude/mcp.json#gis-utils
    activation: explicit-skill-tool   # how the orchestrator invokes it
  ```
- Layered loader walks the union per office's scope (same pattern as
  references / doctypes). PBS sees universal + domain manifests for
  PV-FFA / Wind / Naturschutz + state for MV.
- A new PBS skill `register-integration` (or
  `integrate-tool`) walks the user through adding a new MCP /
  adapter / skill to the relevant scope manifest. Hands off to
  `author-manifest` if the target manifest doesn't exist yet.
- Orchestrator queries via new MCP backend tool
  `find_integrations(capability=?, scope=?)` — returns relevant
  entries, lets the AI surface "for this task, you have these
  options" to the user.

**Why a registry vs just letting the orchestrator discover by trial**:
- Discoverability: the AI knows what's available without trying
  random tool names.
- Cross-office reusability: once "review-platform / Hypothesis is a
  good fit for collaborative review" is captured, every office that
  selects that scope inherits the knowledge.
- Onboarding: a new deployment knows what's plug-and-play vs what
  needs configuration.

**Open questions**:
- Do MCP entries carry their own MCP server config (host, port,
  command), or just point at where it's configured externally
  (~/.claude/.mcp.json)?
- Skill entries — are they redundant with auto-discovery via
  SKILL.md frontmatter? Maybe yes for skills, registry is mostly
  for MCPs + adapters; skills get auto-registered.
- Capability vocabulary: free-text or controlled list? Free-text
  starts faster, controlled list helps queries.
- Integration with the "review-platform integration adapter class"
  proposed in the Web-UI item: that's a specific case of this more
  general pattern.

### Web UI for collaborative review (annotations + comments)

**Why**: Renders from the previous item produce review-ready PDFs,
but distribution + collaborative review still happens out-of-band
(email attachments, file shares). For colleagues, partners (Hendrik),
and clients to comment / annotate / discuss in-place — and for those
annotations to come back into the workflow — we need a web UI.
Self-hosted in Coolify (PBS's existing PaaS).

**Architectural trigger**: implementing this is the load-bearing
event for the `pbs_core` / `pbs_mcp` physical split (see
ARCHITECTURE.md → Backend organization). Until the web UI lands,
the conceptual split inside the monolithic MCP module is
sufficient; the web UI is the first concrete non-MCP consumer
that forces promoting `pbs_core` to its own package + wrapping it
as a persistent service.

**Sketch (topic-level)**:
- Web app receives uploads from the backend (PDFs + metadata
  context: project, doctype, version, what we want feedback on).
- Recipients get a share link (auth via password / signed link /
  account, TBD).
- Reviewers annotate (highlight, draw, comment per page/region),
  thread comments, mark sections as approved/rejected.
- Annotations + comments are queryable back via MCP (new tool
  `fetch_review_feedback(project, doctype, version)`) so they feed
  the orchestrator's record-feedback / Abwägung-drafting flows.
- Probably a "review-platform" integration adapter class (parallel
  to email/calendar/scanner/etc.) so the platform itself can be
  swapped per office preference.

**Research candidates** (open-source to evaluate before building):
- **Hypothesis** (web annotation, open source, well-established) —
  paragraph + range annotations on web pages / PDFs; has API for
  read-back. Mostly aimed at academic web annotation.
- **Cryptpad** (encrypted collaboration suite, French gov-funded) —
  has document review capabilities; self-hostable.
- **Nextcloud + Collabora Online** — generic collaborative office
  suite; Collabora supports PDF review; widely deployed.
- **Stirling-PDF** — open-source PDF tools; has annotation support;
  self-hostable.
- **HedgeDoc / Outline** — collaborative markdown; not PDF-focused
  but useful if review shifts upstream from PDF.
- **PDF.js + custom annotation backend** — Mozilla's PDF.js with
  annotation layer + a small server (FastAPI?) storing annotations.
  Custom-built; most flexible but most work.
- **Onlyoffice Document Server** — full collaborative office suite;
  PDF review; Coolify-friendly Docker deployment.
- **PaperHive / Annotator.js** — older annotation-focused projects;
  check current state.

Goal: prefer a deployable existing tool with a usable API over
custom build. Custom annotation server is last resort.

**Open questions**:
- Auth model for external reviewers (UNB officials, client
  contacts): passwords, signed links, federation?
- Annotation portability: if we leave the chosen tool later, can
  annotations export to a standard format (W3C Web Annotations)?
- Privacy: annotations on Begründung drafts contain pre-decisional
  content; storage location + retention need legal-review.
- Notification flow: how do reviewers learn there's something to
  review? Email integration (already on roadmap) is the natural
  hook — invite mail with review link.
- Round-trip: when reviewers comment, does the orchestrator surface
  it on next session-open, or wait for explicit `fetch-review-
  feedback` call?

### Anthropic-native-app / third-party GUI-frontend integrations

**Why**: As the AI-augmented workforce grows, users uncomfortable
with CLI need GUI on-ramps. Anthropic itself is building native
GUI apps with workspace features and integrations; similar
trajectories elsewhere (Cursor, Zed, etc.). PBS-style intertwined
workflow could be exposed through these GUIs as another frontend
over the same `pbs_core` engine — same intertwining model, more
accessible surface.

**The crucial guard (per VISION.md → category-collapse risk)**:
integrating with native GUIs is fine ONLY when the integration
exposes intertwined workflow. The risk is category collapse —
PBS reduced to a "summarize this email" plugin in someone else's
tool. That's tacked-on, not intertwined; it betrays the thesis.
Any integration must preserve continuous orchestration, persistent
state, source-grounding, and the human-authority gates. If the
host environment can't accommodate those, the integration should
be deferred or rejected outright.

**Sketch (topic-level, speculative)**:

- `pbs_core` exposed via HTTP / WebSocket / similar transport so
  GUI clients can call it (post-physical-split per ARCHITECTURE.md
  → Backend organization).
- Integration registry's `kind` field grows `frontend` or `client`
  alongside `mcp` / `adapter` / `skill`.
- Each GUI integration registered with metadata about which
  workflow surfaces it exposes (orchestrator chat? specific
  specialist skills? read-only state browser?) — surface mapping
  becomes auditable against the intertwining requirements.
- Authentication / multi-user concerns surface here (also tied
  to "Office as multi-human + AI" open question in VISION.md).

**Pull-forward triggers**:

- A specific GUI host emerges that can carry intertwined workflow
  faithfully (not just discrete features).
- A non-CLI colleague needs PBS-Office access and CLI is the
  bottleneck (Hendrik becomes a full participant, or PBS hires).
- SaaS pivot becomes concrete (possibility 3 in VISION.md).

Until then: defer. CLI (Claude Code) + planned web UI cover the
immediate frontend needs.

### Generalized knowledge ingestion via MCP connectors

**Why**: Today the architecture has two ingestion paths — legal
references via `research-references` (publishers' websites,
KNE/LUNG/BfN portals) and per-project inputs via
`ingest_project_inputs` (briefings, surveys, Stellungnahmen
dropped in `inputs/`). Companies have many more knowledge
sources: SharePoint, Confluence, Notion, internal wikis, custom
DMS, CRM systems, project management tools, billing systems,
internal email archives, recorded meeting notes. PBS doesn't
yet address how to bring these in. Generalizing the ingestion
layer is what makes intertwined workflow viable in real
companies — they have knowledge in many places.

**Sketch**: MCP connectors as the inbound knowledge layer
(parallel to integration adapters as the outbound layer; both are Backend sub-patterns).
Each company picks connectors that match their stack:

- SharePoint connector reads a configured folder; ingests at
  the appropriate scope per the layered manifest pattern.
- Notion connector exposes a configured workspace.
- Confluence connector reads a configured space.
- Custom DMS connectors via simple HTTP / file-system adapters.

The pattern mirrors `research-references`: each manifest entry
declares its `fetch_method` and source URL/connector.
Generalize the fetch_method enum to include MCP-connector kinds
(`mcp-sharepoint`, `mcp-notion`, `mcp-confluence`, etc.).
Ingested content lands in LanceDB at the appropriate scope,
searchable via `search_corpus` with source_type filtering.

**Pull-forward triggers**:

- First office that needs to ingest from an external source
  beyond legal references.
- First prospect (consulting / sales) with a structured DMS
  that PBS-style intertwined workflow needs to draw on.
- A non-legal corpus becomes valuable enough to PBS itself
  (e.g., archived correspondence + meeting notes corpus for
  cross-project pattern recognition).

**Open questions**:

- Schema: how do non-legal references differ from legal in
  manifest entry shape? Probably a unified schema with optional
  fields per source kind.
- Authentication: many corporate sources require OAuth /
  service accounts. Connector responsibility, but auth state
  needs persistence (office-config? per-connector credentials
  store?).
- Refresh policy: legal references refresh monthly-ish; live
  Notion / Confluence might want continuous sync. Per-connector
  configurable.
- New scope dimension? "Office-private" knowledge (this office's
  own SharePoint, internal docs) doesn't fit any of the
  shareable scopes (universal/domain/state). Either treat as
  per-deployment override of universal, or introduce a fifth
  scope kind. Resolve when first office-private connector lands.

### Cross-deployment community knowledge content

**Why**: The integration registry (above) covers cross-deployment
*callable* integrations — once "Hypothesis is good for collaborative
review" is captured, every office that adopts that scope inherits
the recommendation. But knowledge *content* (bausteine, refined
argumentations, captured patterns) currently has no cross-deployment
story. Each office is siloed. If PBS captures a valuable Naturschutz
baustein that proved itself in real Stellungnahme exchanges, no
mechanism exists for other Naturschutz-domain offices to benefit.

**Distinct from integration registry**: registry catalogs
*callables*; this catalogs *knowledge artifacts*. Both are
cross-office, both scope-aware, but they carry different things.

**Sketch (topic-level, speculative)**:

- A "community" layer above the (universal × domain × state)
  scopes — content that's been proven in one office and made
  available to others.
- Bausteine + memory docs explicitly marked as community-
  shareable; opt-in pull from receiving offices.
- Provenance preserved: who originated, who validated, with
  what feedback record.
- Curation question: who decides what's community-quality?
  Likely human curation by domain shepherds (one or more
  recognized practitioners per domain).

**Pull-forward triggers**:

- Second deployment exists (PBS-only doesn't justify;
  multi-office does).
- Concrete value example surfaces ("we wish we had Office X's
  Naturschutz bausteine").
- Curation infrastructure question becomes real (who validates,
  how distribution works).

**Open questions**:

- Distribution: git-mirror? Custom registry server? Bundled
  with releases?
- Trust model: how does Office Y verify Office X's baustein is
  worth adopting?
- Conflict resolution: community baustein vs. local baustein
  with same name?
- Privacy: bausteine may contain client-specific or politically
  sensitive context; sanitization required before community
  publishing.

### Cross-practice knowledge integration

**Why**: PBS-Office today supports multi-practice projects
(`practices: [<id>, ...]` in state.md, sibling-practice with
read-only crossing). The model assumes light coexistence: PBS
reads Hendrik's GIS exports as static inputs; doesn't write to
his workspace, doesn't query his database directly.

But intertwined workflow benefits from richer integration.
Hendrik's GIS findings (FFH-Gebiet boundaries, species
distribution plots, habitat photographs from Begehungen,
Bestandskarten) contain knowledge PBS could draw on directly
for artenschutzrechtliche reasoning. Today that knowledge is in
his GIS database; PBS sees it only via static exported PDFs/PNGs.

**Sketch (topic-level, speculative)**:

- Practice-aware MCP boundaries: each practice's tooling exposes
  its knowledge via MCP; cross-practice queries authorized per
  project (multi-practice flag) or per scope (cross-cutting).
- Or simpler: cross-practice knowledge surfaces as a special
  source kind in `search_corpus` (filter by practice).
- Authorship preservation matters here: if PBS draws on
  Hendrik's GIS finding, who is the author of the resulting
  Begründung paragraph? Joint authorship? Citation? Provenance
  recorded in audit trail.

**Pull-forward triggers**:

- First multi-practice project with significant cross-practice
  reasoning required (Begründung Section citing GIS-derived
  spatial analysis with traceable provenance).
- Hendrik's tooling becomes MCP-accessible (currently CLI /
  file-based).

**Open questions**:

- Trust + authorship: cross-practice knowledge enters PBS's
  output; whose responsibility is the integrated reasoning?
- Granularity: full GIS database access, or curated findings
  the GIS practice explicitly exposes?
- Conflict: when GIS finding contradicts text-practice
  assumption, who reconciles?

### Project management + invoicing

**Why**: Project work today has no time/billable tracking, no
milestone-to-invoice mapping, no status reporting to client. The
orchestrator knows phase transitions and decision logs but doesn't
connect them to billing. Adding PM concerns covers: time tracking
per project / per practice / per partner, milestone definitions
that trigger invoicing, status reports auto-generated from state.md
+ decisions.md, draft invoices from accumulated time.

**Sketch**:
- Per-project `_ai/billing.md` — ledger of billable units (hours,
  fixed-price milestones, expenses) with state-transition tagging.
- New PBS skill `log-time` — capture time entries from session
  context (e.g. "I worked 2h on Maxsolar Begründung Section 4
  today"), append to billing.md.
- New skill `draft-invoice` — composes invoice from a project's
  billing ledger, applies office-config invoice template, hands off
  to the accounting integration adapter for actual delivery.
- Accounting adapter implementations (DATEV-export, lexoffice,
  sevDesk) — protocol stub already in place from Phase 5
  (`backend/.../integrations/accounting/`).
- Integration with Begründung-deliverable-snapshot pairs: a
  send-gate firing on a Vorentwurf is also a billable milestone.

**Open questions**:
- Time entries: structured (hours / category / billable yes-no) or
  free-text with extraction?
- Multi-practice billing: when Hendrik (partner) co-produces, does
  PBS bill the client and split, or does each party bill independently?
- Privacy: billing data is sensitive. Per-project storage in
  `<project>/_ai/billing.md` keeps it co-located with project
  context but means it ships wherever the project ships. Office-
  state-only ledger (`<state_root>/billing/<project>.md`) is more
  isolated.

---

## v2 — extensions

### AI-workspace generator (meta-skill) — long-horizon vision (renamed session 13 per #22 Sub-DR B; was AI-office builder)

**Why**: PBS-bureau is one instance of a pattern: an AI workspace
that coordinates document work for a specific domain (German
planning law) using a specific workspace shape (office). The
architectural commitments being made through sessions 5-13 —
meta-rule 4 boundary discipline, fail-closed corollary,
strict-validation, Skill Bundle frontmatter convention,
five-entity-type taxonomy, prep → implementation → review cycle,
three-axis VISION (intertwining / sparring / authorship
preservation), Workspace + Specialist + Skill three-primitive model
— are *pattern-level*, not PBS-specific. They generalize to any
practitioner workspace: legal practice, research lab, creative
studio, knowledge graph deployment, federation node, etc.

The vision: a meta-skill (or meta-plugin) that **generates a new AI
workspace** from a domain spec + workspace shape + employed
specialists + the accumulated architectural patterns +
infrastructure templates. Generative reuse, not just
library reuse — the generator produces complete working plugin
scaffolds for new workspaces, instantiating the pattern with
domain-specific specialists + workspace-specific configuration.

**Distinct from "Generalize + publish domain-agnostic skills"**
(v1.x ROADMAP entry above): that's library reuse — pull `audit`
+ `design-review` into other projects as drop-in components. The
builder is generative reuse — given a description of a new
domain's offices/practices, scaffold an entire working plugin
including its orchestrator, drafting skills templated for the
domain's doctypes, review skills with domain-specific slices,
memory taxonomy, manifests, etc. Both directions are valuable
and complementary.

**What the builder produces (per generated office)**:
- Complete plugin scaffold (`plugin/skills/<name>/SKILL.md` for
  each domain skill, with frontmatter populated)
- Orchestrator skill instantiated with domain-specific phase
  model (PBS uses Phase A/B/C; a legal office might use
  intake/discovery/filing/argument phases)
- Domain-specific MCP tools (drafting helpers, validation gates)
  vs reused generic infrastructure
- Memory taxonomy for the domain (PBS has bausteine; legal might
  have precedents/citations/templates)
- Manifests + reference structure (PBS has gesetze/leitfäden/
  urteile in layered manifests; medical might have drug-protocols/
  treatment-guidelines/regulatory-mandates)
- office-config schema with domain-specific fields
- Doctype skeletons + style conventions
- Initial decision records seeding the architectural commitments
  (each generated office starts with ARCHITECTURE.md and the
  same meta-rules 1-4 in place, plus a domain-specific VISION
  capturing that domain's three-axis equivalents)

**Domain-spec inputs** (the builder's interface):
- Domain identity: name, scope, regulatory anchor
- Actor types (practices/roles within the office)
- Doctype list with templates / structural conventions
- Workflow phases + transition rules
- Memory taxonomy: what kinds of records the domain accumulates
- Review layers: what counts as structural / fachlich / formal
  for this domain
- External authority types (PBS has UNB / Behörde / höhere
  Verwaltungsbehörde; legal has courts / opposing-counsel /
  regulators; research has reviewers / journals / funding-bodies)

**The builder is itself an AI office** (the office-of-offices).
It runs Claude-Code-mediated; conversational with the user
describing the new domain; iterates on scaffold; emits a
complete plugin tree.

**Refactoring needed before this is buildable**:

- **Pattern vs instance separation in PBS**: today the orchestrator
  bakes "B-Plan" / "Begründung" / "Festsetzungen" into PROCEDURE.md
  routing examples, the office-config schema has
  planning-specific fields, manifest schemas embed German legal
  taxonomy. These need to factor cleanly into "pattern (stays in
  the builder)" vs "instance content (lives in PBS-the-domain)."
- **Domain-spec format**: needs design — a declarative format for
  describing a domain that's expressive enough to generate working
  scaffolds but not so detailed it duplicates writing the plugin
  by hand.
- **Generation pipeline**: the builder reads the spec + applies
  templates + emits files. Likely Pydantic-validated spec input;
  Jinja-templated skill bodies; conversational refinement loop.

The session-7 architectural hardening is exactly the right work
to enable this future. Each commitment (fail-closed corollary,
target 9 subsumption check, framing skill, audit-trail v2's
single-write architecture) bakes in *pattern* discipline that
the builder will scaffold-by-default into every generated office.
Without these commitments, the builder would scaffold weak
defaults; with them, it scaffolds correct-by-construction
offices.

**Pull-forward trigger** (multi-stage, revised under single-
domain-pioneer constraint):

The user is a planning-domain expert and won't authentically
hand-build offices in domains they don't practice. The textbook
"build 2-3 hand-instances and measure overlap" trigger is wrong
for this constraint — see `ARCHITECTURE.md` "Validation under
the single-domain-pioneer constraint" for the analysis. Two
distinct validation signals replace it:

1. **Best-effort split stage** (immediate, pre-RAG): per ROADMAP
   v1 commitment #9, implement a best-effort pattern-vs-instance
   split of all current schemas + commitments using the 3-5
   hypothetical-domain thought experiment. Validate **signal #1**
   (split doesn't break PBS) via PBS regression tests. This
   doesn't validate the split's *correctness across domains* —
   only that it's *implementable and PBS-functional*. Mandatory
   pre-RAG; the cost of doing it later is much higher.
2. **Spec format design stage** (post-launch, when first natural
   second-domain opportunity arises — consulting engagement,
   second deployment, or a researcher contact): propose domain-
   spec format. Test against PBS retroactively (could the spec
   regenerate approximately PBS?). If yes, the format captures
   the pattern; if no, what's missing reveals where the split
   was too PBS-shaped (signal #2 starts arriving).
3. **First-build stage** (when a real second-domain user is
   committed): build that user's office *via the builder*.
   Compare the generated scaffold against what would have been
   hand-written. Measure delta; refine. **Signal #2 fully
   arrives** with this stage — the right-boundary validation
   the single-domain pioneer cannot self-supply.

Each stage is a real gate. Stage 1 is mandatory pre-RAG (it's
ROADMAP commitment #9). Stages 2-3 wait for natural triggers;
they may never arrive — and that's acceptable, as long as
stage 1 produces a solid best-effort split that future work can
build on.

**Distance from current state**: stage 1 is 1-2 sessions away
(pre-RAG commitment #9). Stages 2-3 depend on second-domain
opportunity that's external to the user — could be 6 months
(if consulting interest emerges) or never. The architecture
should be ready *if* it happens, and useful *whether or not* it
does.

**Open questions** (defer until validation stage):
- Should the builder be a plugin itself (Claude-Code-mediated
  conversational tool that emits other plugins) or a CLI/library?
- How to update generated offices when the underlying patterns
  evolve (analogous to OpenAPI-generated client regeneration —
  but for architectural commitments).
- Multi-domain offices (e.g., a planning bureau that also does
  light legal advisory work) — composable patterns or separate
  offices that share state?
- Naming: "AI Office Builder" / "Office-of-Offices" /
  "knowledge-work-plugin-generator" / TBD.

#### Market context (April 2026)

Three relevant launches landed late April 2026 — Claude Connectors
for Creatives (9 MCP-based tool integrations), Microsoft Agent
Framework 1.0 (production-ready Python+.NET multi-agent runtime),
Gemini Enterprise Agent Platform (formerly Vertex AI; agent
runtime + Memory Bank + A2A protocol governance). Plus Claude
Cowork (Anthropic's desktop agent for knowledge workers), already
shipping domain-specific plugins for legal / finance / HR /
marketing / design / operations / data analysis.

**Honest reading of where this leaves us:**

We are a single-user, single-domain, pre-launch project with
thoughtful architecture and an unvalidated thesis. Anthropic /
Microsoft / Google are shipping adjacent runtime + agent products
to thousands or millions of users today. The "domain office"
abstraction layer the AI-office-builder vision targets is a
*structural distinction we drew*, not a defensible category we
occupy. It might prove a real differentiation (best case);
Anthropic could ship Cowork+templates that subsume it (likely);
or it might turn out to be a distinction without a difference
(worst case).

**What this changes — five concrete takeaways:**

1. **MCP investment validated.** Heavy MCP usage is forward-
   compatible with where the market is converging. Connectors
   prove the pattern at consumer scale; A2A complements (cross-
   agent) without replacing (in-agent). Empirical, not boasting —
   our architectural bet here is correct.

2. **MS Agent Framework is the strongest substrate candidate
   when v2 work starts.** Subsumes (likely): graph-based workflow
   runtime, multi-agent orchestration patterns (sequential /
   concurrent / handoff / group chat / Magentic-One),
   OpenTelemetry observability, A2A interop. Does NOT subsume:
   domain office structure, memory taxonomy, three-axis VISION
   discipline, audit-trail-as-canonical-source. **Target 9
   (Subsumption check) at v2 design time should explicitly
   evaluate: build vs adopt MS Agent Framework as the office-
   builder runtime?**

3. **Claude Cowork is the natural end-user deployment substrate
   (NOT v2 long-horizon — pre-RAG concrete).** Cowork supports
   MCP servers, Agent Skills, and Plugins natively. Custom
   connectors work across all Claude clients (claude.ai, Cowork,
   Desktop, mobile). Anthropic is already shipping domain plugins
   for common verticals. **PBS-bureau deploys as a Cowork plugin
   for end-users**; Claude Code remains the dev runtime. The
   AI-office-builder vision becomes concrete: "scaffold a Cowork
   plugin for any expert-practitioner niche domain." See pre-RAG
   commitment #11 for the immediate decision gate.

4. **A2A protocol awareness should enter the architecture now
   (lightly).** Future offices may communicate via A2A (e.g.,
   PBS-bureau ↔ legal-practice office for combined planning /
   legal consulting work). Schemas should stay A2A-shape-
   compatible at pattern layer — particularly audit events
   (already cryptographic-friendly) and project state (already
   has identity fields). See pre-RAG commitment #10 for the
   decision gate.

5. **Gemini's Memory Bank + Agent Identity + Model Armor are
   competitive infrastructure for primitives we currently build
   ourselves.** Long-running agent state, persistent memory,
   signed agent cards, prompt-injection defense. Build-vs-buy
   decisions per primitive when v2 work starts; don't assume we
   build everything from scratch.

**What stays useful regardless of how the vision plays out:**

- PBS-bureau as a working tool for the user's planning bureau
  (load-bearing claim — independent of v2 success)
- Architectural discipline as internal quality framework
  (load-bearing — pays back in PBS quality whether or not the
  vision validates)
- MCP as integration protocol (forward-compatible regardless)

**What could subsume the vision** (named honestly so future-you
can recognize it):

- Anthropic ships "Cowork plugin templates per vertical" with
  scaffold tooling — the AI-office-builder becomes their
  feature, not our differentiation
- MS Agent Framework adds "domain office templates" — same
  outcome from different vendor
- The "domain office" layer turns out to just be "well-structured
  Cowork plugins" — distinction without a difference

If any of these arrive before our v2 work, the vision pivots
(e.g., from "build a builder" to "ship the best Cowork plugin for
expert planning work, with optional patterns documented for
others to copy"). That pivot is acceptable — the underlying
discipline (meta-rules, fail-closed, three-axis VISION, etc.) was
worth doing for PBS-the-instance regardless.

#### Marketplace of specialists as v3 horizon (architectural lock + mechanics deferred per #22 Sub-DR B)

Long-horizon possibility, post-v2 generator. Architectural
constraints **locked session 13 per Sub-DR B**
(`docs/decisions/positioning-three-tier-framework.md`); v3
mechanics deferred until v2 generator ships and ecosystem
dynamics are visible.

**Marketplace shape locked**: marketplace is **of specialists**,
not of workspaces or offices. Workspace generator (v2) scaffolds
workspace shape per archetype; specialist marketplace (v3)
populates workspaces with capabilities. Two distinct distribution
surfaces, complementary.

**Two-layer marketplace strategy** (the user's framing,
session-9 followup; sharpened session 13):

- **Layer 1 — main app distribution**: PBS-bureau itself
  (the framework + open demonstration content) lives in
  **Anthropic's marketplace** (today: `knowledge-work-plugins`
  repo + Cowork plugin distribution; tomorrow: whatever Anthropic
  ships as the canonical Cowork-plugin marketplace). We don't
  run our own marketplace for the main framework — we participate in
  Anthropic's. Easier distribution, broader reach, no
  marketplace operations overhead for us.
- **Layer 2 — specialist marketplace** (open
  question; was "specialized blueprint marketplace"): a niche
  marketplace for **specialists** (planning-document-work,
  citation-verification, layered-review-framework, legal-research,
  brand-voice — cross-archetype + domain-anchored) MIGHT be ours
  to operate. OR might also live on Anthropic's marketplace as
  "premium tier plugins." OR a third party might run it.
  **Decision deferred**; too early to know.

**Architectural constraints locked Sub-DR B** (so v3 mechanics
don't redesign v1 specialist contract):

Marketplace listing = one specialist version. Listing must include:
specialist Pydantic shape (Layer 1 + Layer 2); skill definitions;
entity Pydantic schemas (Layer 2 subclasses); process entities +
references manifest; event subscriptions (compatibility check);
substrate compatibility list; dependencies (other specialists, for
composite specialists per Sub-DR A D5); version + changelog.

**Marketplace-level concerns deferred** (per Sub-DR B D1-D4):
authentication; pricing model; quality governance; deprecation
lifecycle; specialist signing / provenance verification.

**Three evolutionary models** (whichever marketplace strategy
emerges):

| Stage | Model | When |
|---|---|---|
| **Stage 1** (v1.x — today) | You-as-sole-seller | You publish refined blueprints; buyers buy directly. No marketplace tooling. Direct consulting + asset licensing. |
| **Stage 2** (post-v2) | Curated marketplace (yours OR Anthropic's premium tier) | Vetted contributors; quality control; marketplace tooling exists. Curation premium reflects quality signal. |
| **Stage 3** (mature) | Open marketplace | Anyone publishes; community moderates; operator takes a cut. Anthropic-plugin-marketplace shape. Highest scale; lowest control. |

**Critical constraint on v2 builder design (load-bearing today)**:
the v2 AI-office-builder's OUTPUT format must be **marketplace-
compatible from the start**, regardless of which marketplace
strategy ultimately wins. Concretely:

- **Standardized blueprint manifest format**: each generated
  office is a self-contained blueprint with manifest declaring
  what's contributed (skills, managed entities, adapters,
  doctype manifests, references manifests, memory bauseine,
  workflow phases, integration adapter requirements)
- **Dependency declaration**: blueprint manifest declares
  framework version dependency, integration adapter classes
  required, MCP tool dependencies
- **Version compatibility annotations**: which framework
  versions this blueprint is tested against
- **Quality / completeness metadata**: declared completeness
  (skills only / skills + bauseine seed / fully refined practice
  library / etc.)
- **License declaration per blueprint** (some open, some closed)

If v2 ships with proprietary or per-deployment-only blueprint
formats, retrofitting marketplace standards later is painful.
**Design v2's output format with marketplace standards in mind,
even though the marketplace itself is v3+ horizon and the
operator may not be us.** This is the load-bearing piece for
TODAY'S v2 design work.

**Strategic value of running a Layer-2 niche marketplace**
(if we do):
- **Specialization positioning**: Anthropic's marketplace is
  general-purpose; ours could be the canonical place for "deep
  domain-specialist multi-department-office blueprints" with
  audit-defensibility + practice-content depth. Different
  niche.
- **Network effects**: marketplace operator captures both
  supply + demand once established
- **Standards-setting**: defines what a "good blueprint" looks
  like at the deep-domain level
- **Data moat**: market intelligence on what's selling, what's
  missing, what's working
- **Compounding brand**: "blueprints from THE pbs-bureau
  marketplace" beats "blueprints from N independent sellers"

**Risks if we DO run a Layer-2 marketplace**:
- Distracts from consulting growth (running a two-sided market
  is a different business)
- Anthropic's marketplace might absorb the niche (positioning
  around specialization is the mitigation)
- Quality fragmentation damages framework reputation —
  curation discipline must be tight
- We'd compete with our own sellers (resolution: at stage 2/3,
  retire from selling within own marketplace; switch revenue
  to marketplace fees + framework consulting)

**Strategic value of NOT running a Layer-2 marketplace**:
- Less operational overhead
- More focus on consulting
- Anthropic's existing marketplace (or whoever wins) handles
  distribution; we focus on architecture + delivery

**When the marketplace decision becomes timely**:
- v2 AI-office-builder has shipped + multiple instance offices
  exist
- External developers ask "where do I publish my legal-practice
  blueprint?"
- Anthropic's marketplace either embraces deep-domain blueprints
  (we participate) or doesn't (gap exists for us to fill)

**Strategic arc for consulting** (defensible long-arc pitch):

> "Today: open-source framework + my consulting expertise.
> Year 2: AI-office-builder generates new offices from domain
> spec. Year 3+: marketplace where the ecosystem of AI-office-
> architects publishes refined blueprints — possibly Anthropic's
> general marketplace, possibly a specialized one. PBS-bureau is
> the proof-of-concept; the builder is the meta-skill; the
> marketplace is the ecosystem. By engaging me now, you're
> getting first-mover positioning on architecture that scales
> into a larger ecosystem."

Captured as concept; **no commitment to build a marketplace**.
The v2 builder design constraint (marketplace-compatible
blueprint format) is the only load-bearing implication for
current work.

### Tier 3 — Enterprise multi-agent A2A platform port + parallel development

**Reframing note (session 12 substrate eval, 2026-04-30)**: this section was previously titled "Gemini Enterprise port + parallel development" with Gemini Enterprise framed as the exclusive Tier 3 target. Per pattern-vs-instance discipline applied during #18 substrate eval, Tier 3 destination is platform-agnostic — pattern is "**enterprise multi-agent A2A platform**"; instances include **Gemini Enterprise** (canonical exemplar — Anthropic Claude in Gemini's Model Garden = natural credibility-flow target), **Azure AI Foundry** (Microsoft's parallel enterprise AI platform; natural fit if MS AF substrate adopted), **AWS Bedrock AgentCore** (AWS's parallel; natural fit if Strands substrate adopted). Specific platform-of-choice depends on consulting client's ecosystem. The motivation, structure, and substantive content of this section remain valid; framing reframes from Gemini-exclusive to platform-pluggable. See `docs/decisions/substrate-agentic-framework.md` "Counter-consideration: Tier 3 implications" for the analysis.

**Why this is in the roadmap (revised session 9 followup)**:
**planned post-validation, regardless of client demand**. Was
previously framed as "persistence of the option, probably never";
upgraded to **planned workstream** post-v1-validation, motivated
by **exposure + learning** (not specific business case). The user
will port + parallel-develop on a Tier-3 enterprise multi-agent A2A platform (Gemini Enterprise as default exemplar; Azure AI Foundry or AWS Bedrock AgentCore depending on substrate choice + consulting context) once PBS's
performance is validated through real Schulz Planungsbüro use,
even without a big client trigger. **This is Tier 3** of the
three-tier deployment ladder; Tiers 1-2 are covered by pre-RAG
commitment #13 (deployment-mode flexibility within our archetype).

**Motivation (sharpened)**: building the Gemini port is the
**necessary precondition for credible multi-archetype consulting**.
You can't sell "we run on both archetypes; clients pick what fits
their scale" without having actually built on both. The port IS
the validation work that enables the consulting offering; without
it, the multi-archetype pitch is theoretical, not verifiable.

In priority order:
1. **Validation-through-use → enables consulting offering**: the
   primary motivation. Building the port is what earns the
   "verified track record across archetypes" credibility signal
   `docs/strategic-positioning.md` "Multi-archetype credibility"
   relies on. No port = no verifiable claim.
2. **Capability building**: building on a different archetype
   (multi-agent A2A vs single-Opus orchestration) teaches things
   that staying on one archetype doesn't.
3. **Exposure**: being on Gemini Enterprise's platform / Model
   Garden / Agentspace gets visibility we wouldn't otherwise have.
   Anthropic Claude is in Gemini Enterprise's Model Garden —
   credibility flows from running there.

**The three-tier deployment ladder**:

| Tier | Archetype | Deployment shape | Triggered by |
|---|---|---|---|
| **1 — Local** | Single-big-model orchestration | stdio MCP, local files, no auth, single user | Default for solo / small clients wanting data on their machine |
| **2 — Cloud-hosted container** | **Same archetype** as Tier 1 | HTTP MCP, cloud storage, auth, multi-user per office | Most consulting clients — managed service, cross-device |
| **3 — Enterprise multi-agent A2A platform** (Gemini Enterprise / Azure AI Foundry / AWS Bedrock AgentCore) | **Different archetype** (multi-agent A2A) | N agents communicating via A2A, persistent memory service, agent identity, governance gateway | Enterprise scale (1000+ users, federated authority, regulatory governance, cross-org workflows) |

**Tier 1 ↔ Tier 2** = same archetype, different deployment.
Pluggable transport/persistence/auth layers. Same codebase.
Commitment #13 prepares this — pre-RAG.

**Tier 2 → Tier 3** = **archetype change**. Orchestrator
decomposes into N agents. A2A becomes PRIMARY (not
internal-shape-only). Memory Bank replaces state.md. Agent
Identity becomes governance layer. **Substantial refactor**
(3-6 months estimated). This entry is the documented option for
when that need arises.

PBS today is built on the single-big-model archetype (Tiers 1-2).
**Post-v1 validation, the user will port + parallel-develop on
Gemini Enterprise's multi-agent A2A archetype** — Tiers 1-2 stay
the primary archetype for solo / small clients; Tier 3 runs in
parallel as additional deployment + capability investment. The
load-bearing IP (domain content + architectural discipline)
ports over.

**Pull-forward triggers** (revised — was "probably never, possibly
someday"; now "build is the validation, post-Tier-1-2 maturity"):

**Primary (planned, definite)**:
- **Tiers 1-2 maturity**: PBS-bureau working in real Schulz
  Planungsbüro use; pre-RAG queue completed; Phase 1 corpus
  ingested; first project bound and producing real work. Once the
  primary archetype is mature enough to be a stable substrate, the
  parallel Gemini port begins. **Building IS the validation** —
  the port enables the consulting credibility, doesn't wait for it.

**Additional (would accelerate)**:
- Consulting engagement with enterprise scale (1000+ users,
  parallel tasks, federated authority)
- Cross-organization federation requirement (e.g., PBS-bureau ↔
  legal-practice office ↔ client-CRM agent across orgs)
- Multi-bureau deployment (one PBS-style office multiplied across
  100 planning bureaus, each with own data, governed centrally)
- Government / regulator deployment requiring formal Agent
  Identity / Agent Gateway / Model Armor governance

**Notably absent from the new triggers**: a specific big client.
The port is committed without that.

**What survives the migration unchanged** (the load-bearing IP):
- Domain knowledge: skill bodies, manifests, korrektur-rules,
  doctype templates, decision records
- Architectural discipline: meta-rules, fail-closed corollary,
  pattern-vs-instance discipline, three-axis VISION
- Validation contracts: Pydantic models port to per-agent
  contracts
- Memory taxonomy: layered scopes (universal × domain × state ×
  project × department) port to Memory Bank scopes
- Office vs department distinction: maps cleanly to
  agents-per-department in A2A archetype

**What gets refactored** (runtime mechanics, not content):

| Element | Today (our archetype) | Future on Gemini Enterprise |
|---|---|---|
| Orchestrator | Single Opus session with skill delegation | N agents (one per skill or per department) communicating via A2A |
| Backend | Local Python MCP server (stdio) | Apigee-bridged managed MCP servers (HTTP, distributed) |
| Persistent state | `state.md` per project (markdown + Pydantic) | Memory Bank (Google's persistent context service) |
| Cross-department workflow | In-session skill orchestration | A2A protocol message-passing |
| Audit trail | Custom `audit-trail.jsonl` + `record_audit_event` MCP tool | Agent Identity (cryptographic signed agent cards) + A2A trace |
| Governance | Pattern-vs-instance discipline + fail-closed corollary + meta-rules | Agent Gateway + Model Armor + Agent Simulation |
| Model | Anthropic Claude (one model, single session) | Anthropic Claude (Model Garden — same model, different runtime) |

**Migration cost estimate**: substantial (3-6 months realistic
work) but conceptually clean — content + discipline port; runtime
changes. **Anthropic Claude is in Gemini Enterprise's Model Garden
as Claude Opus 4.7 + Sonnet + Haiku**, so the model layer doesn't
change. Apigee provides MCP-to-agent bridging so our existing MCP
tools have a translation path. A2A protocol is Linux Foundation
governed (stable v1.0) and supported by Anthropic + Microsoft +
AWS + Salesforce + SAP + ServiceNow.

**Pre-existing groundwork** (already in pre-RAG queue):
- Commitment #10 (A2A schema gate) — designs schemas to be
  A2A-shape-compatible. **This commitment is directly load-bearing
  for this migration path**: AuditEvent + ProjectState shaped to
  be A2A-friendly today means migration-day work is reduced.

**Why this is consulting-marketing-relevant**:

The migration path is itself a **positioning advantage** vs both
commercial vertical AI (Harvey, Filevine, Spellbook) and
enterprise platform-first builds (Gemini Enterprise from day one):

> "Start with our archetype — single-Opus orchestration, MCP-
> based, deployable as Cowork plugin. Right for one bureau or
> small practice (low cost, fast deploy, no platform lock-in).
> When you scale to 100 offices or need cross-organization
> federation, there's a known migration path to Gemini Enterprise
> that preserves your domain content and architectural discipline.
> The IP isn't tied to our runtime — the methodology and patterns
> travel."

Compared to:
- **Harvey/Filevine/Spellbook**: "Buy our SaaS, give us your
  data, no portability."
- **Build directly on Gemini Enterprise from day one**: "Pay
  enterprise platform overhead before you have one client;
  vendor-locked from the start."

**The agent-typology gap that defines our consulting niche**

Three distinct agent types currently dominate the market — and
the one that matters most for "AI office" abstraction is the
LEAST commoditized:

| Agent type | Examples | Shape | Market state |
|---|---|---|---|
| **Product-wrapper** (vendor tool exposed as agent) | Salesforce CRM agent, Workday HR agent, ServiceNow agent, Box/Adobe/Oracle agents in Gemini Agent Gallery; Slack/Notion/DocuSign Cowork connectors | One SaaS product's API as agent capabilities | **Heavily commoditized** — every vendor ships theirs |
| **Capability-slice** (single workflow specialist) | Spellbook (contract redlines), Harvey-tools (contract analysis), EuclidHL (zoning Q&A), brand-voice slices | One workflow within a domain | Crowded commercial space |
| **Department-shaped** (functional-area plugin with multi-skill coverage) | Anthropic's `legal`, `finance`, `hr` plugins; PBS-bureau today | Functional area, may use multiple tools, multi-skill | Sparse — Anthropic ships ~11 shallow examples |
| **Multi-department office** (coordinated multi-functional with shared state + lifecycle + discipline) | (PBS-bureau eventually, after #12 lands) | Office abstraction with N departments coordinating | **Empty in open source; rare even commercially** |

**What big companies CAN buy off-the-shelf**: product-wrapper
agents for every SaaS they pay for + cross-SaaS automation via
A2A protocol. That's "agentic iPaaS" (integration platform with
LLM-mediated workflows replacing declarative pipes). Useful but
NOT an AI office — it's AI-mediated cross-SaaS access.

**Concrete user-facing example of what the off-the-shelf platform
gives you**:

> User: "Update the Salesforce opportunity, create a Workday entry
> for the new hire, and ping ServiceNow for IT setup."
> → Salesforce agent updates → A2A message to Workday → Workday
> creates HR record → A2A message to ServiceNow → IT request queued

That's product-wrapper-agents-talking-to-each-other. It's
useful. It is not a coherent AI office.

**What big companies CANNOT buy off-the-shelf**:
- **Department-shaped agents** for their actual departments —
  Anthropic's `legal`/`finance`/`hr` plugins are shallow
  (single-department, no orchestrator, no lifecycle, no audit
  discipline)
- **Multi-department office coordination** — domain-coherent
  shared state across departments, with architectural discipline
  ensuring coherence
- **The office layer** that turns the agent fleet into a coherent
  operation rather than a federated automation pipeline

**The consulting positioning sharpens to**:

> "Your fleet of product-wrapper agents (Salesforce, Workday,
> ServiceNow) plus your A2A cross-SaaS automation gives you
> AI-mediated SaaS integration. That's agentic iPaaS — not an AI
> office. The actual office layer — domain-coherent multi-
> department coordination with shared state, lifecycle, audit
> trail, and architectural discipline — has to be deliberately
> designed. **That's what I do.** I architect the office
> abstraction that turns your fleet of agents into a coherent
> operation, on whatever runtime archetype fits your scale (our
> single-big-model orchestration for solo/small; multi-agent A2A
> on Gemini Enterprise for enterprise federation). Methodology
> and architectural discipline are vendor-neutral and scale-
> independent; the office abstraction is the IP."

This is meaningfully different from competing consulting offers:
- **"I'll build you another product-wrapper agent"**: already
  commoditized; vendor agents are free.
- **"I'll connect your SaaS apps via A2A"**: Gemini Enterprise +
  Apigee already does this declaratively.
- **"I'll write you Python"**: any consultant.

**Methodology + office-abstraction-design is the consulting IP.**
Independent of runtime archetype, the office-design layer is what's
missing in the market. PBS-bureau (and the AI-office-builder vision)
is the open-source proof-of-concept that makes this offering
credible to consulting prospects.

**Open questions** (deferred until trigger arises):
- Does the v2 AI-office-builder generate Cowork-deployable
  offices AND Gemini-Enterprise-deployable offices from the same
  domain spec? Or are these two different builders (one per
  archetype)?
- How does state-bank persistence map cleanly between archetypes?
  Memory Bank's API + ours need a translation layer; design when
  needed.
- A2A endpoint design (when to expose an actual endpoint vs
  schema-only awareness) — informed by commitment #10.

**Status**: persistence of the option only. Not committed to
implement. Trigger conditions named explicitly so future-you
recognizes when the migration is justified.

### AI-business marketplace platform (long-horizon watch position) — speculative

**Why this is in the roadmap**: persistence of the option only,
explicitly **speculative** — the underlying market category may
or may not form. Building infrastructure for a category that
hasn't materialized is a bet, not a plan. This entry documents
the idea + trigger conditions so future-you can re-evaluate
when (if) market signals shift.

**The idea**: a web platform for buying, selling, and
provisioning **AI-augmented businesses** — where seller is a
retiring practitioner (planner, lawyer, accountant, consultant,
researcher) whose practice has been encoded into an AI office,
and buyer is another practitioner (or non-practitioner +
practitioner team) acquiring practice + AI office together.
Platform provides:
- Marketplace listings (akin to BizBuySell / MicroAcquire /
  Flippa, but AI-business-specific)
- Valuation models (tooling for pricing AI-encoded knowledge as
  transferable IP)
- Provisioning automation (cloning AI office between owners,
  re-attribution, migration tooling, escrow)
- Trust layer (verification of captured knowledge depth, buyer
  due diligence on the AI office's operational history)

**Connection to broader strategy**:
- Schulz Planungsbüro sale (strategic milestone above) is the
  proof event — selling the first AI-augmented business
  validates that the category exists and that buyers will pay
  for it
- AI-office-builder v2 vision feeds the marketplace by making
  AI offices more replicable + more numerous (more potential
  inventory)
- Consulting offering generates the operating-experience
  evidence that informs valuation models

**Honest critical assessment** (session 7, user-articulated):

**What's potentially strong**:
- First-mover in a category that *could* emerge
- Network effects + brand + tooling become moat over time IF
  category materializes
- Adjacent existing markets exist (BizBuySell, Flippa,
  MicroAcquire) — proof that small-business resale is a real
  market; "AI-augmented" is the differentiator
- The provisioning-automation piece is a credible technical
  service even if the marketplace piece doesn't reach scale

**What's hard / risky**:
- **The category doesn't exist yet.** Today: zero AI businesses
  to buy/sell. Schulz Planungsbüro might be among the first.
  Building marketplace before category forms = building for a
  market that may never materialize.
- **Marketplace dynamics are brutal.** Two-sided: need supply +
  demand simultaneously. Trust takes years (Flippa/BizBuySell
  decade+ to dominance). High-value low-frequency transactions
  = fewer trust-building data points per dollar than typical
  marketplaces.
- **First-mover advantage is real but unprotective.** Network
  effects develop slowly with low frequency. Reputation moat
  takes years.
- **Capital + team requirements are large.** Marketplace
  operator (GTM/community), full SaaS platform, legal/compliance
  for business sales (jurisdictional), trust/escrow
  infrastructure. **Solo-founder execution unrealistic.**
  Co-founders or substantial hires needed. Different skill set
  than building PBS or consulting.
- **Opportunity cost is enormous.** Every hour on marketplace
  = hour not on PBS / consulting / case studies. Marketplace
  pays off only if it dwarfs opportunity cost — far from
  guaranteed.
- **Risk of being too early.** If category takes 5-10 years to
  materialize, marketplace burns capital for years before
  liquidity. Many marketplaces die before reaching critical
  mass.

**Trigger conditions** (re-evaluate when these emerge):

1. **Multiple AI businesses transacted** (5+ visible cases of
   AI-augmented businesses sold, ideally with public valuations)
2. **Demand-side signals**: PE plays for "AI rollups" of small
   businesses; strategic acquirer interest in AI-augmented
   acquisitions; explicit buyer demand for AI-encoded
   businesses
3. **Supply-side signals**: practitioners explicitly asking to
   sell their AI-augmented businesses (waiting list of
   sellers); retirement-driven exits with "AI augmentation"
   framing common
4. **Category recognition**: "AI business" or "AI-augmented
   business" as a recognized term in business-broker / M&A
   discourse
5. **Capital + team availability**: co-founder with
   marketplace / GTM expertise; capital runway for 3-5 years
   pre-revenue marketplace building

**If triggers don't fire** (likely outcome): the marketplace
remains a documented option that doesn't get built. The
provisioning-automation piece can still exist as part of the
consulting offering (technical service, not platform).

**If triggers fire** (best case): the consulting business
becomes the springboard. PBS + consulting clients + AI-office-
builder v2 generate the supply side; marketplace emerges as a
natural extension after category-validation evidence
accumulates. **Schulz Planungsbüro's sale is the first
transaction the marketplace would have facilitated** — it's
the proof point that gives the marketplace credibility from
day one.

**Strategic stance** — do NOT optimize toward this prematurely.
Let it earn the right to exist via Part A's demonstrated
success + consulting traction + observed category emergence.
**Sequence not parallel**: Part A (Schulz sale) → consulting
business → AI-office-builder v2 → THEN evaluate marketplace.

**Status**: long-horizon speculative watch position. No
commitment to build. Re-evaluate annually against trigger
conditions.

### Acquire + AI-office-ify existing small practices (v3 horizon option)

**Why in the roadmap**: another long-horizon strategic option that
builds on the same infrastructure as the marketplace. Captured as
**option only** — no commitment to pursue. Documented so future-you
can recognize when (if) the trigger conditions materialize.

**The idea**: rather than waiting for retiring practitioners to
bring their practices to a marketplace, *acquire* small expert
practices (planning bureaus, legal practices, accounting firms,
niche consulting shops) and AI-office-ify them using the v2
builder + accumulated patterns. The AI-augmented practice can
then be operated, held as portfolio, or sold (feeding the
marketplace). Inverse direction of the marketplace's "retiring
practitioner sells" supply: same demographic, different
transaction direction.

**How it composes with what we're already building**:
- **AI-office-builder v2** is the precondition — without it, each
  acquisition requires hand-built office scaffolding (uneconomical
  at portfolio scale)
- **Consulting offering** generates the operational know-how of
  how to AI-augment a specific domain — that's the transformation
  playbook each acquisition applies
- **Marketplace (if it materializes)** provides exit liquidity
  for transformed practices
- **Schulz Planungsbüro is the inverse prototype** — validates
  "build a practice, AI-augment it." The acquisition direction
  validates the forward path (acquire a practice, AI-augment it).
  Same architectural infrastructure serves both.

**Sourcing candidates**: retiring practitioners with no succession;
distressed small practices; undermarketed niche specialty firms.

**Exit options per acquisition**:
- **Hold + operate** as AI-augmented practice (income generator)
- **Sell** as AI-augmented business (feeds the v3 marketplace)
- **Roll up** into a portfolio (PE-shaped rollup of AI-augmented
  small practices in adjacent or complementary domains)

**What's hard / risky**:
- Operating businesses ≠ building software — fundamentally
  different skill set; running portfolio of practices needs
  operations capability we don't currently have
- Capital intensity — multi-acquisition portfolio needs
  significant patient funding
- Practitioner-handoff is sensitive — existing clients'
  continuity, regulatory / fiduciary concerns per domain
- Each domain's regulatory specifics constrain transformation
  depth (legal practices have bar-association rules; accounting
  has CPA certification; medical has licensing); the AI office
  augments practice operations, doesn't replace the credentialed
  practitioner

**Trigger conditions** (re-evaluate when):
- AI-office-builder v2 ships and demonstrably scaffolds working
  offices in a small bounded timeframe
- First consulting client retention extends 12+ months
  (operational transformation playbook validated)
- First AI-augmented practice sale completes (Schulz or similar)
  — exit valuation evidence exists for "what an AI-augmented
  practice is worth"
- Capital partner with patient capital + practice-acquisition
  experience surfaces (different relationship than typical
  software-VC)

**Strategic stance** — do NOT optimize toward this prematurely.
Sequence: PBS pioneer → consulting traction → AI-office-builder v2
→ marketplace (when/if) → THEN evaluate acquisition arm. Each
prior stage produces evidence + capability for the next.
Acquisitions without the v2 builder = unscalable; without the
consulting playbook = unguided; without exit liquidity =
illiquid portfolio.

**Status**: v3-horizon option, parallel branch to the marketplace.
No commitment to build. Re-evaluate annually with the marketplace
section.

### Agent Simulation — runtime stress-test framework (long-horizon)

**Why**: Inspired by Vertex AI's Agent Simulation pattern (cross-
agent stress testing at scale, adversarial scenarios, structured
eval reports as regression suite). Distinct from `audit` +
`design-review` (static-analysis quality framework — review
artifacts and discipline) and from the planned testing harness
(Phase 0 item 5; runtime eval framework — runs scenarios and
scores outcomes). Agent Simulation is the **adversarial /
edge-case / cross-agent stress-test** layer on top of those:
once basic eval works (Phase 0 #5), Agent Simulation adds
adversarial mode + cross-agent interaction testing + scale.

**What it adds beyond Phase 0 #5 testing harness**:
- **Adversarial scenarios**: red-team inputs (prompt injection
  attempts, ambiguous instructions, context manipulation,
  jailbreak edges)
- **Cross-agent interaction tests**: when multiple plugin
  agents (per #11) or departments (per #12) coordinate on a
  workflow, simulate the full multi-agent run including failure
  modes at handoff boundaries
- **Scale**: hundreds-to-thousands of scenarios per release,
  not the dozens that a hand-curated regression suite carries
- **Failure-mode classification**: structured taxonomy of agent
  errors (hallucination / policy violation / missed citation /
  latency outlier / handoff failure) with per-mode reporting

**Pre-trigger commitment**: NONE. Phase 0 #5 lands first; its
eval-result schema (per Row 9 of `a2a-and-gemini-pattern-
emulation.md`) is designed to support Agent Simulation
extension later — same `EvalRun` / `Scenario` / `EvalResult`
types, just larger volume + adversarial scenario kinds.

**Pull-forward triggers**:
- **First enterprise consulting client** asking explicitly about
  adversarial / red-team eval (regulated industries, government,
  healthcare may demand this).
- **First multi-department office in production** (post-#12) —
  cross-department workflows have more failure surface; basic
  regression isn't sufficient.
- **AI-office-builder v2 ships** — scaling stress-test across
  generated offices means we need scenario suites that
  generalize per-domain, not just PBS-specific.
- **Anthropic ships an Agent Simulation analogue** as a managed
  service that we can integrate (much cheaper than building from
  scratch).

**Status**: deferred to v2. Agnostic of A2A — applies whether
we stay single-Opus or migrate to multi-agent A2A archetype.
Different "agents" in the simulation correspond to different
shapes of consumer (skills today; plugin agents post-#11; A2A
peers post-Tier-3-trigger).

### Reference versioning

**Why**: Laws amend. Currently `archive_versions: true` in manifest
keeps `retention_versions: 5` per entry. But: how does
verify-citations know which version a baustein was verified against?
History tracking spec needed.

### Reference internal cross-refs

**Why**: BauGB §44 mentions §1, etc. When retrieval pulls §44 chunk,
should §1 be auto-fetched as context? Reranker may handle this; test
with real queries first.

### Subagent patterns

**Why**: Currently no subagents. For deep legal review, a
`legal-reviewer` subagent (separate Claude instance with focused
context) could do thorough §-by-§ checks without bloating the main
session.

**Components**:
- `plugin/agents/legal-reviewer.md` — agent definition
- Invoked by review-draft skill at Layer 2 (fachlich) for
  juristisch-critical sections
- Returns findings; main Claude integrates

Similar pattern for `style-auditor` (deep style+korrektur sweep).

### Hooks / event triggers (revised per meta-rule 4)

**Why (revised)**: Per meta-rule 4 (execution-determinism), most
operations formerly imagined as hooks belong inside MCP tools as
atomic side-effects, not as separate hook scripts:

- `state-transition` → logged inside the `update_project_state`
  MCP tool, not a hook on Edit.
- `snapshot-on-send` → atomic write inside the snapshot-creation
  MCP tool, not a hook on Bash send-mail.
- `pre-compile validate-latex-style` → step inside `compile_latex`
  MCP tool's pipeline, not a PreToolUse hook.
- `post-ingest baustein-flag` → atomic in the `ingest_paths` MCP
  tool's transaction (already planned per `research-references`
  SKILL.md cross-reference handling).

The genuinely hook-shaped niche that survives is **out-of-band
file change detection between sessions** — when state changes
outside Claude Code's view (user manually edits a manifest YAML
in a text editor; hidrive sync brings in changes from a sibling
practice; an external script touches `office-config.yaml`). A
SessionStart hook could detect mtime deltas against a
last-session marker and trigger validation / cross-ref re-eval
before the orchestrator does its first action.

**Defer**: until concrete out-of-band-change friction is observed
in real use. Pre-designing for hypothetical out-of-band edits
adds enforcement scaffolding nobody asked for.

---

## v2.x — additional verfahren references

These are domain knowledge documents to author when first project
raises them.

### Umweltprüfung verfahren reference

**Why**: §2 Abs.4 BauGB + Anlage 1 environmental assessment
integration with the 13-phase Bauleitplanung. Currently mentioned
but not detailed in `memory/universal/verfahren/bauleitplanung-phasen.md`.

**Spec**: full reference doc at
`memory/universal/verfahren/umweltpruefung.md`. Covers Scoping (§4
Abs.1), Umweltbericht structure cross-ref to umweltbericht checklist,
Wechselwirkungen, Monitoring (§4c) integration.

### FFH-Vorprüfung verfahren reference

**Why**: §34 BNatSchG Erheblichkeitsabschätzung is required for
projects near FFH-Gebiete. Was rhetorically handled in the Vorbeck
transcript; deserves its own reference doc for projects where
formal Vorprüfung is required.

**Spec**: full reference doc at
`memory/universal/verfahren/ffh-vorpruefung.md`. Covers
Erheblichkeitsabschätzung, Kumulative Betrachtung,
Verschlechterungsverbot, Ausnahme nach §34 Abs.3-5.

### Abwägung mechanism + doctype

**Why**: Per-Stellungnahme structured response document. Distinct
shape from Begründung/Festsetzungen. Not yet in doctypes.yaml as
active.

**Components**:
- New doctype entry in `doctypes.yaml`
- Checklist at `plugin/skills/validate-checklist/references/checklists/
  abwaegung.md`
- Possibly `draft-abwaegung` specialist skill (Phase A entry for
  Abwägung doctype)

### Artenschutz / SPA verfahren reference

**Why**: §44 BNatSchG-Tatbestände + §45 Abs.7 Ausnahme; SPA-Vorprüfung
+ SPA-Hauptprüfung structure. Hendrik's domain primarily but joint
projects need it.

**Spec**: `memory/universal/verfahren/artenschutz.md`. Covers
Bestandsaufnahme-Standards (Südbeck, Dietz/Kiefer), Signifikanz-
prüfung, CEF-Wirksamkeit-Nachweis, FCS-Auslegung. Note: with the
domain split, this content is Naturschutz-domain-scoped — should
land at `memory/domain/Naturschutz/verfahren/artenschutz.md` once
domain-scoped memory directories exist (currently universal-only).
The decision to introduce per-domain memory directories awaits the
first domain-specific reference content (this would be the trigger).

### Other verfahren / doctypes as projects raise them

- Bauantrag / V&E-Plan-spezifisches
- Zielabweichungsverfahren
- Innenbereichssatzung-Aufstellung (different from B-Plan)

---

## Working-style improvements (lessons collected)

These aren't features but discipline improvements observed during
v1 design. Apply by next session and onward.

### ARCHITECTURE.md as first reference, kept fresh

When in doubt about where new content belongs, walk Rules 1-6 in
`ARCHITECTURE.md`. Don't guess; classify deliberately. For layered
manifest entries pick the scope (universal/domain/state) BEFORE the
path.

**Keep ARCHITECTURE.md current with every architectural change.**
Meta-rule changes, new entity types, schema bumps, integration
classes — all land in ARCHITECTURE.md *in the same commit* that
introduces them. ROADMAP-tracked items get a one-line pointer in
the "Designed extensions" section so future sessions don't
re-discover them. After any meta-rule addition or significant
refactor, sweep all skills against current meta-rules to catch
drift.

### Source-grounding for legal claims

`verify-citations` skill's invariant: any `§ X <Gesetz>` reference
must come from a `search_corpus` or `read_corpus_file` result, not
from training memory. Never invent citations.

### Section-level edits, not whole-document writes

Per orchestrator Validation 7.3: `Edit` tool with surrounding context,
not `Write` of the entire file. Especially during Phase B review.

### Decision recording preserves alternatives

When recording an architectural / design / verdict decision in
docs (ARCHITECTURE.md, ROADMAP.md, VISION.md, decision docs like
`docs/rag-pipeline-decisions.md`, project `_ai/decisions.md`,
etc.), always preserve the alternatives that were considered and
rejected — not just the chosen path. Capture per item:

- **The verdict** (chosen path)
- **Alternatives considered** (named explicitly with their
  reasoning + why-rejected)
- **Revisit trigger** (when would we revisit this decision? what
  signal would force re-evaluation?)

Why: decisions made today look obviously correct in their context
but reveal as defensible-or-not when the context shifts. A
verdict-only record reads as "this is how it is" — making the
revisit conversation harder than necessary because the original
alternatives have to be re-derived. A verdict + alternatives +
trigger record reads as "here was the option space and our
choice within it" — making revisit a refinement rather than a
re-investigation.

Applies to: architectural decisions, model/library choices,
schema choices, naming conventions, scope boundaries, deferred-
vs-urgent prioritization, anything where the next session might
reasonably ask "why this and not the other thing?"

### "Used by skill X" cross-refs are noise

In memory content (C type), don't include "loaded by skill Y at
checkpoint Z" lines. They don't change behavior. Skill files
themselves declare what they consume.

---

## Tracking conventions

When picking up an item from this roadmap:

1. Move it from "deferred" to "in-progress" by editing this file.
2. Once complete, remove from this file (it's now in the codebase
   per ARCHITECTURE.md placement rules).
3. Don't leave completed items here — that's clutter.

When a new deferred item emerges:

1. Add to the appropriate v-tier section.
2. Include "Why" + "Sketch" + "Open questions" subsections.
3. Don't elaborate beyond that — full design happens when picked up.
