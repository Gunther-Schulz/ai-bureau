# pbs-bureau architecture — what goes where

This document is the canonical placement reference. When in doubt
about where new content belongs, walk the **three decision rules**
below. Meta-rules establish principles; the decision rules apply
them.

> **Vision anchor.** PBS is built on three interlocking principles:
> **intertwined-AI-workflow (not tacked-on features)**, **sparring
> partner (not answer machine)**, and **authorship preservation
> (the user remains defensible expert author of everything PBS
> produces on their behalf)**. The architecture serves continuous
> human-AI collaboration with built-in challenge in service of
> defensible output — persistent state, orchestrated behaviors,
> source-grounded outputs, surfaced decisions, explicit human-
> authority gates, counter-arguments, calibrated confidence,
> selective friction. See `VISION.md` for the full thesis.

Status: **v0.29 (session 11 — per-DR internal gap detection across 12 retroactively-reviewed DRs + backfill DRs for #8 (pre-action framing skill) + #15 (office-level managed entities Client + Actor). 3 internal-gap amendments applied: mcp-fallback-policy retry behavior + error-vs-unreachable distinction; sparring-output-v1 schema versioning + bypass audit-trail; governance-and-identity-sourcing convention versioning + conflict resolution. 8 gaps correctly deferred to instance/chronological. 2 new DRs backfilled for previously-DR-less commitments)**.

> **Framework-foundation framing (read first, every session).** PBS is **the framework foundation for the consulting business**, validated by the Schulz planning bureau. PBS is the pioneer instance, never the product. At every architectural step, do the **full scalable foundational work** — designed for any expert-practitioner deployment (legal-practice / research-lab / brand-voice / consulting-client) at first bind, not minimum-viable-PBS. The framework is the IP; PBS-instance content is incidental. See "Pattern-vs-instance discipline" below for the operational rule + the sharp defer rule.

- **v0.28 → v0.29**: **Per-DR internal gap detection + backfill
  DRs for #8 + #15 (max-effort session 11)**. User asked: "and
  feature gap analysis you just did covered all already processed
  retroactive review corpus from earlier, right?" Honest answer:
  prior gap detection (v0.28) covered ARCHITECTURE-level gaps;
  did NOT directly cover per-DR INTERNAL gaps (decisions WITHIN
  each DR's scope that should have been surfaced but weren't).
  Ran deliberate per-DR gap detection across all 12 retroactively-
  reviewed DRs (sessions 5-11).

  **3 real internal-gap amendments applied** (decisions within
  scope that needed surfacing):

  - **mcp-fallback-policy.md**: added retry behavior decision
    (fail-closed on FIRST unreachable; no skill-level retry-with-
    backoff; transport handles its own connection retries) +
    error-vs-unreachable distinction (fail-closed corollary
    applies to UNREACHABILITY only; MCP-returned errors are
    structured envelopes for skill-side handling per
    backend-mcp-error-format).
  - **sparring-output-v1.md**: added schema versioning behavior
    (additive optional fields = forward-compat; required-field
    additions are SCHEMA-BREAKING per v0.19 evolution patterns) +
    bypass audit-trail decision (when sparring validation 3x-fails,
    `explicit-bypass-with-reason` emits `sparring_bypass`
    AuditEvent — without this, bypasses are invisible to
    defensibility reconstruction).
  - **governance-and-identity-sourcing.md**: added convention
    versioning (in-place edit + git history; entities pin to
    `git_sha` at mint-time per decision 4; forward-only default,
    mass-rename rare opt-in) + convention conflict resolution
    (more-specific scope wins: department > office > universal/
    framework default; same-priority conflicts are bugs flagged by
    audit slice 21 + design-review target 12).

  **8 gaps correctly deferred to instance / chronological** (no
  amendment needed):
  - PII redaction in logs/audit events → deployment-instance per #13
  - Event retention policy → deployment-instance per #13
  - Cross-tenant data isolation → Tier 3 / #13
  - Department deactivation/renaming → first deployment that needs it
  - Body translation / multi-language → multi-language deployment
  - display_label localization → same
  - Trigger conflict resolution → first multi-skill conflict
  - Tier 3 cross-org A2A trust model → Tier 3 trigger

  **2 new backfill DRs written** (per session-11 user direction):

  - **`pre-action-framing-skill.md`** (commitment #8): captures
    meta-skill design — when triggers (non-trivial / new
    commitment-shape / explicit invocation), what produces
    (`FramingOutput` Pydantic schema with required `actual_problem`
    / `in_scope` / `out_of_scope` / `approaches_considered (>=2)` /
    `chosen_approach` / `chosen_approach_rationale` / `constraints`
    / `success_criteria` / `confidence` / `confidence_basis`
    fields), how integrates (project-level memory entry; downstream
    skills consume; audit/design-review reference at review-time),
    composes with skill-granularity v0.27 (passes 3-test). Worked
    example: session-7 audit-trail v1 → v2 reversal would have
    been caught at framing time if `frame-task` existed (the
    `approaches_considered (>=2)` requirement forces single-write
    architecture as alternative to dual-write).
  - **`office-level-managed-entities.md`** (commitment #15):
    consolidates Client + Actor schemas + cross-department
    reference convention previously scattered across ROADMAP +
    `office-vs-department.md` + `governance-and-identity-sourcing.md`
    decision 5. Distinct scope: governance-and-identity-sourcing
    is about governance + identity sourcing PRINCIPLES; this DR is
    about the ENTITY TIER (Client + Actor as office-level managed
    entities; cross-department reference convention via
    `<entity>_id: str` Layer 2 fields with gate-validation;
    adapter mode for both per glue-not-replacement; Layer 2 schemas
    + body conventions per entity-md-spec).

  No real-revise items beyond the three internal-gap amendments.
  Per-DR detection found refinements that were implicit; backfill
  DRs surface architectural decisions that were scattered.
- **v0.27 → v0.28**: **Architectural-gap detection sweep
  (max-effort session 11)**. User asked: "btw, has your review
  also checked for architectural gaps? You know like the stuff I
  have pointed out and we discussed earlier in this session."
  Honest answer: prior reviews focused on whether existing
  decisions hold; gap detection was peripheral. Ran deliberate
  gap-detection sweep across four lenses:

  **Lens A — failure-mode catalog**: walked all entries against
  current discipline coverage. Three updates:
  - `monolithic-skill-bundle`: PARTIAL → COVERED via v0.27
    skill-granularity discipline (same 3-test catches both
    over-elevation AND under-elevation/should-split).
  - `implicit-contract-between-skills`: PARTIAL → narrowing.
    Three sub-shapes named: file-location-based (covered by
    fail-closed); audit-event-driven (covered by #6+#12);
    skill-to-skill handoffs via orchestrator (REMAINING GAP —
    context format, side-effect ordering, post-conditions
    implicit in orchestrator routing). Candidate fix: extend
    `handoffs:` frontmatter field to declare SHAPE; audit slice
    24 candidate (defer until #11 completes).
  - `cargo-cult patterns`: PARTIAL → COVERED via three-layer
    protection (greenfield review at major version boundaries +
    target 9 subsumption + sharp defer rule + #18/#19 substrate-
    eval disqualifying criteria).

  **Lens B — VISION-axis coverage**: walked architectural
  requirements per axis. All 19+ requirements addressed by current
  commitments. No gaps.

  **Lens C — greenfield-derived**: walked through hypothetical
  fresh-designer questions. Trust calibration / confidence /
  trust-over-time / frontend / multi-user / transition path /
  category-collapse all covered. No greenfield-derived gaps that
  map to architectural commitments.

  **Lens D — user-surfaced-pattern reflection**: pattern is
  emergent (user-as-detector + AI-as-executor); has produced
  reference card + validation-gating-overview + several disciplines
  via this exact mechanism. Diminishing returns on proactive
  detection beyond what's already done.

  **Maintenance discipline rule 6 added**: periodic greenfield
  review at major version boundaries. Formalizes the cargo-cult-
  prevention mechanism that was emergent; structurally catches
  drift over time. Discipline-bloat watch position notes that
  this is a process-level rule, not a content-level discipline —
  doesn't add a new naming, just a maintenance rule.

  Real gap remaining: implicit-contract-between-skills sub-shape 2
  (orchestrator handoff shapes). Mitigation deferred per its own
  chronological timing (#11 reshapes handoffs).

  No real-revise items beyond these three catalog/discipline
  updates. The architecture is sound; gap detection found the
  refinements already implicit.
- **v0.26 → v0.27**: **ARCH disciplines greenfield review under
  max-effort (session 11)**. After VISION greenfield review (v0.26)
  showed VISION holds, applied max-effort + greenfield lens to
  ARCH disciplines themselves: would we name these starting fresh,
  or different ones?

  **Findings**: All 8 design disciplines / operational principles +
  4 meta-rules + reference card + validation-gating-overview +
  maintenance rules survive clean-slate. Each addresses a distinct
  failure mode the architecture must defend against; greenfield
  would re-derive each from VISION + foundational constraints.

  Mergers / retirements considered + rejected:
  - Pattern-vs-instance + sharp defer rule combined — already
    grouped; works.
  - Glue-not-replacement folded into meta-rule 1 — different
    concerns (deployment portability vs strategic boundary).
  - Sharp defer rule + framework-foundation framing combined —
    tightly composed but address different aspects (when to defer
    vs which scope to optimize for).
  - Validation-layering + make-wrong-shapes combined — different
    abstraction levels.
  - Meta-rules 2+3 combined — same hierarchy as pattern-vs-instance
    / meta-rule 1; keep both at respective levels.

  **One refinement applied**: skill-granularity discipline
  elevated to ARCH-level. Previously lived only in
  plugin-conventions §14 + skill-expert-agent decision record.
  Greenfield: parallel concepts deserve parallel placement. Entity-
  elevation discipline has its own ARCH section; skill-granularity
  is its parallel concept (when to elevate to its own skill,
  analogous to when to elevate to its own entity). Added as
  sub-section "Elevation analogue for skills" under entity-
  elevation discipline. Same restraint-in-elevation principle;
  distinct criteria (workflow + output + reuse vs identity +
  state + lifecycle).

  No real-revise items. Discipline framework is sound; one
  parallel-concept elevation applied for consistency.
- **v0.25 → v0.26**: **VISION.md greenfield review under max-
  effort (session 11)**. After greenfield architecture review
  (v0.25) showed architecture survives clean-slate, the user
  triggered: "lets continue retroactive review with full framing"
  — apply max-effort + greenfield lens to remaining surfaces
  starting with VISION.

  **Findings**: VISION holds. Three axes (intertwining + sparring
  + authorship preservation) survive clean-slate review. 6+
  alternative axis-frames considered + rejected:
  - Two-axis (collapse intertwining + sparring) — fails because
    they're orthogonal (intertwined-AI can be oracle-mode;
    tacked-on AI can be sparring-shaped)
  - Four-axis (add accountability) — fails because accountability
    is downstream of authorship preservation
  - Productivity vs craft — wrong abstraction layer
  - Single-axis (just human-in-the-loop) — loses precision (all
    three failure modes have humans-in-loop)
  - Add multi-user as foundational — composes with existing axes,
    not new axis
  - Add privacy/sovereignty as foundational — instance-level
    concern, not pattern-level

  Foundations check: Vivienne Ming's research holds; Information-
  Exploration Paradox holds; pioneer-instance positioning holds.

  Architectural requirements check: all 14+ requirements derived
  from axes survive clean-slate.

  **Sharpenings applied to VISION.md**:
  1. **Sparring mechanisms structural/behavioral split**: VISION's
     "Sparring requirements" section now annotates each of the 7
     mechanisms with current status (structural / partially
     structural / behavioral) + chronological-defer reasoning
     for the behavioral ones. Captures the genuine info-gap (per
     greenfield-architecture-review §3) so future-session readers
     don't propose premature structural elevation. Includes a
     summary table.
  2. **Framework-foundation framing foregrounded**: VISION's
     pioneer-instance commitment section now explicitly cites the
     framework-foundation framing + sharp defer rule (v0.20) +
     two tests (chronological + framework-cost). Cross-refs to
     ARCH and memory `feedback_pattern_not_instance_defers.md`.
     The connection was implicit before; now load-bearing for
     future-session readers.

  No real-revise items. VISION's core thesis is sound; sharpenings
  add precision without changing direction.
- **v0.24 → v0.25**: **Greenfield architecture review under VISION
  lens (max-effort session 11)**. User triggered with: "so it all
  holds even if we considered throwing it all away and starting
  fresh? Should align with VISION.md and be radical. Like greenfield
  lens in context of VISION." Different from retroactive review
  (which checks "do current decisions hold under current
  discipline?"). Greenfield asks: "would we make the same decisions
  starting from scratch with VISION as anchor?"

  **Findings**: 15+ radical alternatives considered. Most failed on
  VISION grounds (not inertia): AI-only, backend-only, single agent,
  structured-everywhere, multi-agent A2A from day 1, LLM-as-database,
  drop sparring schemas, sparring across all skills, drop pattern/
  instance separation, ECS, imperative orchestration, different
  framing entirely, conflate memory/references/bausteine, no plugin
  separation, AI-as-oracle-only. Each fails specific VISION axes.

  **Convergences**: hybrid-shape, multi-layer validation gating,
  pattern-vs-instance discipline, make-wrong-shapes-impossible,
  single-big-model archetype, pluggable transport, office→department
  abstraction, audit-trail v2 single-write, scope orthogonality,
  all eight disciplines + four meta-rules. Greenfield re-derives
  these from VISION + foundational constraints.

  **Genuine open questions** (where greenfield WOULD diverge):

  1. **Substrate choice (#18)** — hand-rolled vs agentic framework.
     Greenfield-derived disqualifying criteria for #18 eval:
     composes with MCP natively / supports hybrid-shape / Pydantic-
     compatible / no SQL-DB shapes / sparring composable / audit-
     trail compatible / pluggable transport / heaviness scales /
     vendor-neutral. Substrates failing any structural criterion
     are rejected without deep-eval. Eval transforms from
     "comprehensive comparison" to "reject obvious mismatches
     first; deep-eval the 2-4 survivors."

  2. **RAG implementation (#19)** — hand-rolled vs LlamaIndex
     pluggable. Greenfield-derived pluggable boundary: parsers,
     chunkers, hybrid retrieval, citation primitives = pluggable
     candidates; per-reference Pydantic metadata + citation
     traceability + per-#13 ingestion split = keep custom.
     Performance comparison on our use case (German legal text,
     multilingual, per-paragraph chunking).

  3. **Sparring mechanisms 4-7 elevation to structural** — genuine
     info-gap (NOT manufactured restraint). Anti-sycophancy
     detection requires false-positive heuristic; asymmetric-
     respect requires context-sensitivity rules; recommendation-
     commit requires workflow-stage-dependency rules. Empirical
     pattern data missing pre-real-sparring-sessions. Defer until
     5-10 real sparring sessions accumulate; evaluate per mechanism
     for structural elevation. Anti-pattern guard against premature
     elevation. Captured for future-session reminder per user
     direction.

  See `docs/decisions/greenfield-architecture-review.md` for
  exercise + disqualifying criteria + lifecycle.
- **v0.23 → v0.24**: **Max-effort retroactive review pass across 9
  decision records (sessions 5-11)**. User raised the question
  whether the prior ultrathink-review pass (xhigh effort) caught
  all drift; rerun under max effort across decision records that
  pre-dated current disciplines OR were authored under xhigh.
  Findings: NO real-revise items; all decisions hold structurally;
  refinements are framing + cross-ref tightening.

  Specific refinements applied:
  - **Instance-anchored defer rationales reframed as chronological**:
    backend-logging.md ("local single-user backend" → aggregation
    system not yet chosen per #13);
    a2a-and-gemini Row 6a + 6b ("Solo Tier 1 has one user / trusted
    input" → consumer/threat-model lands in #13);
    office-vs-department D3 ("academic today; zero projects bound"
    → target-schema-not-yet-locked).
  - **Worked-examples cross-refs added**: mcp-fallback-policy.md +
    trigger-convention.md + audit-trail-v1.md (v1→v2 reversal) all
    note their relationship to "make wrong shapes impossible"
    discipline (v0.21) which they exemplified avant la lettre.
    `mcp-fallback-policy` is the canonical structural-direction
    example; `trigger-convention` is the canonical
    convention-direction (opposite-direction discriminator)
    example; `audit-trail-v1→v2 reversal` is the canonical
    real-time-discipline-application example.
  - **sparring-output split refined**: acknowledged that
    mechanisms 4 ("what's missing") and 7 ("commit to
    recommendations") are PARTIALLY structural via specific schema
    fields (`whats_missing`, `recommendation`) for specific skills,
    not purely behavioral as original text claimed. "Pareto pick:
    30% of build cost" framing reframed as info-gap (genuine
    chronological reason: schema-validating those mechanisms
    without false-positive rates is unclear pre-empirically).
  - **`_error` sentinel structural enforcement candidate**: noted
    in backend-mcp-error-format.md — `_error` is gate-dispatched
    every MCP response, so per v0.21 discriminator the convention
    could be elevated to a Pydantic base-class model_validator.
    Currently catches violations via slice 16 retrospectively;
    worth elevating when next touching `pbs_mcp/schemas.py`.
  - **skill-expert-agent decision record self-review** (under max
    effort the same turn as it was written under xhigh):
    - Decision 2 (informed defaults for high-variance choices):
      tightened to acknowledge guided-questions are valid form
      of "informed default" for high-variance choices;
      see informed-defaults principle clarification below.
    - Decision 3 (skill vs agent): tighter framing — bodies are
      TYPED by interaction shape (`interactive-sparring` /
      `monitoring-or-batch` / `scheduled-only`); invocation
      patterns are wrappers COMPATIBLE with body type. Replaces
      looser "orthogonal axes" framing.
    - Decision 4 (fine-grained expertise): replaced misleading
      "entity-elevation 3-test analogue" with skill-specific
      criteria (distinct workflow + distinct output + reuse
      across projects). Skills aren't entities; the criteria
      differ.
  - **Informed-defaults principle clarification (v0.18 sub-rule)**:
    informed defaults can take TWO forms — (a) pre-chosen TEMPLATES
    derived from pioneer instance (low-variance choices, e.g.,
    skill body conventions, doctype-md scaffolds) OR (b) GUIDED
    QUESTIONS with concrete options (high-variance choices, e.g.,
    "PM tool: Asana / Jira / none / custom?"). Both deliver the
    principle's spirit (no empty canvas; user gets concrete
    starting points); pre-chosen vs guided picks per the choice's
    variance across deployments. Earlier framing leaned toward
    templates-only; this addition makes the guided-question form
    explicit. See the discipline section for the updated text.

  No real-revise items. All decisions hold; refinements are
  documentation hygiene + cross-ref tightening.
- **v0.22 → v0.23**: **Ultrathink-review pass refinements**.
  Session-11 cumulative commitments (6 ARCH bumps, Bundle A
  locked, sharp-defer audit pulling 9 items forward, reference
  card, validation-gating-overview, 2 memory files) reviewed under
  ultrathink for drift / inconsistencies / refinement opportunities.
  Refinements applied:
  - **Discipline categorization** — discipline list reorganized
    explicitly into "5 design disciplines (gate design decisions)"
    + "3 operational principles (guide implementation choices)" +
    "4 meta-rules" + "earlier resolved concepts absorbed into
    disciplines." HANDOFF essential framing list aligned with
    ARCH section structure (was inconsistent — listed 8 items
    that didn't match ARCH's 8 sections).
  - **Bundle A package layout reframed** as recommended convention
    (NOT gate-enforced). Gate dispatches on `instances_at` paths
    only, not on physical layout. Layout-flexible deployments can
    deviate; audit slice may warn. Per "Make wrong shapes
    impossible" discriminator: gate doesn't dispatch every
    read/write on layout, so it's a convention. Bundle A close-out
    reframed accordingly.
  - **L5 external-boundary validation added** to validation-gating-
    overview (was 4 layers; now 5). External-boundary validation
    (A2A signing, OAuth/OIDC tokens, CloudEvents shape, JOSE/JWT
    outbound signing) is a distinct layer from internal Pydantic
    gate (L1). Largely Tier-2/Tier-3 territory; minimal in Tier 1.
  - **Failure-mode catalog gains** `navigational-consolidation-drift`
    (covered by maintenance discipline rules 3 + 5) +
    `discipline-bloat / over-naming` (uncovered watch position;
    candidate mitigation = periodic discipline-pruning check at
    major version boundaries).
  - **#20 PydanticAI demoted from BLOCKING** to "before Bundle B
    Layer-3 mechanism specifically" (narrower surface; doesn't
    gate broader implementation). #18 + #19 stay BLOCKING.
  - **#18 agentic framework substrate eval** gains heaviness sub-
    axes (operational vs cognitive) + framework bucketing
    (enterprise-grade / mid-weight / lightweight / hand-rolled
    baseline) + scope-creep guard. Substrate evals can run in
    parallel — compresses BLOCKING window from 4-6 to 2-3 sessions.
  - **UniversalEntity Pydantic class + universal.md registration**
    surfaced explicitly in Bundle A close-out (was inferred-by-
    symmetry; now locked).
  - **audit-trail-v2 decision record** gains session-11 amendments
    section (accumulated constraints from sessions 9-11).
  - **Skill body sweep extended** with broader keyword set; one
    additional check; no new fixes (only "stop for now" in
    user-dialog-quote, not a defer rationale).
- **v0.21 → v0.22**: **`docs/validation-gating-overview.md` added**
  as a systems-view of validation gating across the architecture.
  Surfaced session 11 mid-Bundle-A — the question "do we have plans
  for validation gating per our rules?" caught that the pieces are
  spread across ARCH disciplines + meta-rules + entity-md-spec +
  decision records + audit slices + design-review targets + ROADMAP
  commitments, with no single place to scan "how is X validated
  over its lifecycle?". The new doc consolidates as a navigational
  + systems-view (no new content; every section cross-refs source-
  of-truth detailed doc). Four layers named: L1 runtime structural
  (Pydantic + gate, fail-loud) / L2 runtime conventional (AI-applied
  prose + audit-trailed) / L3 retrospective scan (audit slices) /
  L4 prospective design (design-review targets). Inventory enumerates
  every load-bearing gate / convention / slice / target with status
  + source-of-truth pointer. Companion to "Data + boundary reference
  card" (which answers "where does X go?"); this doc answers "how is
  X validated over its lifecycle?". HANDOFF essential framing
  references it. Maintenance discipline rule 5 added: when adding a
  new gate / slice / target / convention, inventory updates in same
  commit as source-of-truth artifact.
- **v0.20 → v0.21**: **"Make wrong shapes impossible, not
  solvable" discipline named** as a top-level architectural
  principle (parallel to pattern-vs-instance / glue-not-
  replacement / AI-as-runtime / entity-elevation). Surfaced
  session 11 during Bundle A type-name uniqueness discussion:
  "convention-driven uniqueness" was the leading position until
  the discriminator emerged — *every "we'll document the
  convention; deployments handle correctness" answer is the
  framework offloading work to deployment time*. Each consulting
  client hits the same problem; each must solve it independently;
  some solve inconsistently. The principle: prefer **structural
  constraints** (type system, Pydantic, gate enforcement) that
  make wrong shapes impossible by construction over
  **conventional solutions** that make them solvable at
  deployment time. Composes with AI-as-runtime hybrid-shape
  (which assigns the boundary: structured for machine contracts,
  prose for semantics) by clarifying WITHIN the structured layer
  that collision-prone or correctness-critical concerns get
  impossibility-by-construction, not validation-by-discipline.
  Concrete first application: type-name uniqueness across
  departments resolved via Bundle A namespacing
  (`<scope-id>.<short-name>`) — collision impossible by
  construction — rather than via deployment-documented
  uniqueness convention. Memory
  `feedback_wrong_shapes_impossible.md` captures for future
  sessions. **Plus**: "Data + boundary reference card" added
  near top of ARCHITECTURE (after "where does X go?" placement
  rules became scattered across 4-6 sections + 2 decision
  records over sessions 7-11). Single consolidated table — no
  new rules, just navigational aid that replaces the chase-six-
  sections pain when applying existing disciplines mid-session.
  HANDOFF essential framing points to it.
- **v0.19 → v0.20**: **Pattern-vs-instance discipline tightened**.
  Surfaced session 11 mid-Bundle-A design when a defer rationale
  reproduced PBS-instance-anchored framing ("today no department
  needs activating") despite pattern-vs-instance discipline being
  named since v0.8. The recurrence signaled the discipline wasn't
  loud enough or operationally sharp. Two changes: (1)
  framework-foundation framing elevated to a top-of-document
  anchor — PBS is the framework foundation for the consulting
  business, validated by the planning bureau, never the product.
  At every architectural step, do the full scalable foundational
  work. (2) **Sharp defer rule** added as a subsection of
  pattern-vs-instance discipline: defer ONLY for chronological
  reason (information genuinely doesn't exist yet — downstream
  shape unlocked, second-domain feedback needed, upstream
  precedent unresolved). Up-front costs (time, complexity,
  "premature", "YAGNI", "PBS doesn't need it yet") are NEVER
  valid defer reasons. The rule composes with `feedback_defer_
  instinct.md`'s specific-cost-naming requirement: the named cost
  must be a future-information cost, not an up-front cost. New
  anti-pattern bullet added to the section's catalog. Memory
  `feedback_pattern_not_instance_defers.md` captures the bias for
  future sessions.
- v0.1 → v0.2: nine entity types + 6 decision rules.
- v0.2 → v0.3: scope-orthogonality live, layered manifests in
  repo, integration adapter scaffolding deployed, schema migration
  framework in place.
- v0.3 → v0.4: execution-locality meta-rule (skills declare
  `mcp_tools_required[]`; `settings.json` permissions; hooks
  deferred).
- v0.4 → v0.5: design-review-driven simplification. **5 meta-rules
  → 4 + 1 named convention**: integration-adapter demoted to corollary
  of app-vs-office; scope-orthogonality demoted to layering convention;
  execution-locality renamed to execution-determinism; new
  source-of-truth & invalidation meta-rule added. **9 entity types
  → 5**: A+B merged into Skill Bundle; G+H merged into Configuration;
  I demoted (it's an internal pattern of E, not a peer). A-I letter
  scheme dropped — names speak for themselves. **6 decision rules
  → 3** audience-first.
- **v0.5 → v0.6**: meta-rule 4 sharpening. **(A) Persistence-layer
  boundary refined**: the rule applies to durable state with a *typed
  contract* (Pydantic model + loader + cross-reference invariants),
  not to all files indiscriminately; loose markdown is skill-direct.
  **(B) Reuse direction made explicit**: shared deterministic logic →
  MCP tool; shared interpretive logic → Skill Bundle reference. The
  audit's slice 14 + design-review's target 7 land on this sharpened
  boundary.
- **v0.6 → v0.7**: meta-rule 4 fail-closed corollary. The rule
  symmetrizes for reads: when MCP is unreachable, contract-bearing
  reads MUST surface and stop, never bypass via direct filesystem
  `Read`. The strict-validation principle (no bad defaults / fail
  loud) extends to availability: a contract that is enforced on
  successful read but bypassed when MCP is down is not a contract.
  See `docs/decisions/mcp-fallback-policy.md`. Audit slice 14 brief
  extended to scan `fallback_when_mcp_absent` strings for declared
  future violations.
- **v0.7 → v0.8**: **Pattern-vs-instance discipline** added as
  meta-discipline before the meta-rules. Every architectural
  commitment must work at pattern level (the test: would this work
  for a hypothetical legal-practice / research-paper-review /
  engineering-doc office?), not just for PBS. PBS is the pioneer
  instance per VISION.md; the architecture is the pattern. Long-arc
  end-state is the AI-office builder (ROADMAP v2). Connects the
  Skill Bundle convention, meta-rules 1-4, fail-closed corollary,
  target 9 subsumption check — all pattern-level by construction —
  into a coherent discipline that constrains future commitments.
- **v0.8 → v0.9**: **Office-vs-department distinction** captured
  as open architectural question (post-partner-built-comparison
  insight). PBS today conflates "office" with "single department"
  (planning-document-work). Real offices contain multiple
  departments (PM, invoicing, etc.) coordinated via shared state +
  natural abstractions + ad-hoc context sharing + integration/
  setup configuration. Scoped as pre-RAG commitment #12 for
  structural design discussion before Phase 1 corpus download.
- **v0.9 → v0.10**: **A2A-shape compatibility decided per row** of
  the v2 Gemini Enterprise comparison table. AuditEvent grows three
  additive fields (`actor_kind` required, `actor_card` optional,
  `origin_agent_card` optional) — distinguishes human vs skill vs
  external-A2A-peer as event emitter. Pattern-vs-instance discipline
  picks up an explicit archetype-portability paragraph: every
  schema decision is checked against "would this port cleanly to a
  multi-agent A2A archetype?" alongside the cross-domain test. HTTP
  MCP transport, data classification, and signing fields are
  deferred with documented paths to commitments #13 and Tier-3
  migration. Cross-department coordination (open question per v0.9)
  receives a load-bearing constraint: must be event-shaped, not
  call-shaped — preserves transport-swap-to-A2A path for #12. See
  `docs/decisions/a2a-and-gemini-pattern-emulation.md`.
- **v0.10 → v0.11**: **Office-vs-department modularization resolved**
  (open question from v0.9). Office is the container; departments
  are capability areas (PBS = office with one department today,
  planning-document-work; future Schulz adds PM + invoicing).
  Skills declare `department:` frontmatter (REQUIRED, no default —
  matches `actor_kind` strict-validation discipline); office-level
  skills declare `department: office`. Memory taxonomy gains a 4th
  orthogonal axis (department), opt-in per entry. Cross-department
  coordination via AuditEvent + extended watch-list with per-
  department `event_subscriptions:` (no new event mechanism —
  subsumes via existing audit infrastructure). ProjectState gains
  `departments_active: list[str]` field for routing + audit-filter
  purposes. Skills are singleton-department; multi-department
  coordination via office-level orchestrating skills. Offices have
  0..N departments (zero-department = single-skill-utility shape;
  PBS-today = single-department; future Schulz = multi-department).
  Per-department phase/lifecycle on ProjectState deferred to #9
  (Pattern-vs-instance split, still pre-RAG); office-config schema
  bump + skill frontmatter sweep deferred to #11. See
  `docs/decisions/office-vs-department.md`.
- **v0.18 → v0.19**: **Three evolution patterns named** as
  pattern recognition (not new disciplines — names the three
  mechanisms already in use): (1) structured + mutable
  (migration framework, e.g., office-config); (2) structured +
  append-only (additive backward-compat, e.g., AuditEvent —
  never rewrite historical records); (3) prose + forward-only
  (no migration; historical anchoring via structured fields like
  `convention_applied: {git_sha}`). Surfaced during session-11
  sanity-check of the migration distinction; the three-pattern
  framing replaces the simpler structured/prose dichotomy
  because append-only structured (AuditEvent) follows neither
  the migration mechanism nor the forward-only mechanism. Each
  pattern has a different code path and discipline check.
- **v0.17 → v0.18**: **Two recurring patterns elevated to named
  architectural principles** (session 11 — surfaced during
  prose-rules-as-conventions discussion under the AI-as-runtime
  conformance check):
  - **Validation layering: deterministic primary, LLM secondary**.
    For any check or enforcement point, use deterministic
    validation (Pydantic, type checks, threshold comparisons) where
    the question has a determinate answer; reserve LLM validation
    for genuine judgment (precision of prose, accuracy of
    cross-reference, fit-to-shape). The two compose:
    deterministic catches binary failures cheaply; LLM catches
    judgment failures expensively. Pattern was already implicit in
    governance enforcement, audit slices, AI-as-runtime conformance
    check — now named so it's invocable as a discipline at design
    time. Cheapest-first ordering: free → cheap → medium →
    expensive (LLM).
  - **Informed defaults: ship best-shape, not empty**. When
    providing architecture/templates/scaffolding to deployments,
    ship with informed defaults derived from the pioneer instance
    (PBS-Schulz), NOT empty canvases. Bureaus inherit working
    starting points; they refine from a base, not bootstrap.
    Already implicit in `research-references` corpus seed,
    `design-review` failure-mode-catalog, skill `<example>`
    blocks. Critical pattern-vs-instance constraint: defaults are
    *shapes* you can adapt, not *instance content* you inherit
    verbatim. PBS-Begründung-content as legal-practice default =
    wrong abstraction; doctype md *file shape* with PBS example
    content = right abstraction.

  Both principles were applied (implicitly) during this session's
  prose-rules-as-conventions design (`docs/decisions/governance-
  and-identity-sourcing.md` operational concerns section uses both
  modes — proactive defaults + detection + how-to-fix). Naming
  them in ARCHITECTURE makes them invocable for future design
  decisions rather than re-derived each time.
- **v0.16 → v0.17**: **AI-as-runtime conformance check (smoke + deep)**
  added under the AI-as-runtime hybrid-shape discipline. Two-level
  test: smoke test (3 yes/no questions, 30-60 seconds, applied per
  proposal) catches obvious violations cheaply; deep test (6 checks
  in three tiers — architectural / operational / disqualifier,
  5-10 minutes, applied when smoke escalates or stakes warrant)
  provides full evaluation. Documented as manual mental checklist
  with explicit promotion path: after 3-5 real applications,
  evaluate for formalization as design-review target 15 (extending
  the discipline-check pattern that targets 1-14 already cover for
  the other 6 architectural disciplines — NOT a separate skill).
  Manual phase first per design-review target-13 "pattern emergence"
  discipline. See "AI-as-runtime conformance check" subsection
  under the hybrid-shape principle section.
- **v0.15 → v0.16**: **AI-as-runtime hybrid-shape principle**
  added as top-level architectural discipline (parallel to
  pattern-vs-instance + entity-elevation + glue-not-replacement).
  The principle: domain semantics, process flow, conditional
  rules, and contextual knowledge live in **markdown bodies
  attached to entity files**, not in encoded schemas or hardcoded
  skill procedures. Cross-domain portability is achieved by AI
  reading prose, not by abstracting over schema variants.
  Structured layers reserved for **interfaces, identity,
  persistence, machine contracts**; everything else is prose;
  AI is the runtime that fuses them at use-time. Three-layer
  frontmatter contract introduced: Layer 1 universal (every
  entity, Pydantic base, strict-locked); Layer 2 type-specific
  (Pydantic subclass per entity type, strict-locked); Layer 3
  per-deployment extension (deferred to #9). Body conventions
  recommended-not-enforced (mirrors how memories conventionally
  use Why:/How-to-apply: lines without validator enforcement).
  Resolves the "where do conditional rules live?" question:
  rules about *when* something applies belong with the *process*
  (process-as-md), not with the entity itself. New v1 commitment
  **#16 (AI-as-runtime hybrid-shape contract — entity-md +
  manifest decomposition + gate generalization)** scheduled
  position 1 in pre-RAG queue, BEFORE #11. Migration of existing
  `doctypes.yaml` + `references-manifest.yaml` (prose squeezed
  into block scalars) bundled with #9 + Phase 1 corpus
  respectively. Audit slice 21 + design-review target 12 added
  for entity-md conformance scanning. See
  `docs/decisions/ai-as-runtime-hybrid-shape.md`.
- **v0.14 → v0.15**: **Glue-not-replacement principle** added as
  top-level architectural discipline (parallel to pattern-vs-
  instance + entity-elevation). PBS is the **glue / coordination
  layer** that brings cross-concern AI to existing infrastructure;
  it does NOT replace existing systems (BPMN engines, accounting
  tools, CRMs, time-tracking, calendars, etc.). The architecture
  is integration-first: the integration-adapter pattern (meta-rule
  1) + adapter-mode managed entities (#12) + adapter-emitted events
  (#9 Gap B) all serve this principle. Where customers have
  existing infrastructure, PBS connects to it; where they don't,
  PBS provides native-mode managed entities + bundled MCP tools as
  an alternative. Both modes work uniformly through the same
  framework. Connects to the BPMN-empowerment positioning (v1.x-v2
  ROADMAP entry) and the consulting-niche framing (`docs/strategic-
  positioning.md`). See "Glue-not-replacement principle" section
  below.
- **v0.13 → v0.14**: **Infrastructure-primitive review pass**
  (session-9 followup #4) — stress-tests core primitives (skills,
  managed entities, audit events, memory, integration adapters,
  cross-department coordination) against expressibility of
  arbitrary business processes. Result: **9/9 process-need
  coverage** (state, actions, rules, history, knowledge, people,
  time, external world, workflows/sequences) after two genuine
  gaps fold into existing commitments. **Gap A — proactive
  time-driven triggers**: today's event sources are reactive +
  interactive only; missing scheduler-fired "tick" events for
  proactive deadline warnings, scheduled reports, Fristverlängerung
  automation. Folds into #13 (Tier 2 cloud naturally hosts
  scheduler); extends event sources from "skill-emitted" to
  "skill-emitted + time-emitted." **Gap B — adapter-emitted
  events**: adapters today are request-response; missing
  surfacing of external state changes (Lexware webhook on payment;
  Harvest external timesheet edit). Folds into #9 (department
  module contract); adapter Protocol gains
  `subscribe_to_changes` / `poll_for_changes`; external changes
  translate to native AuditEvents with `actor_kind=external_agent`
  per #10. No new commitment numbers; both gaps fold into
  existing scope. Smaller deferred items: workflow-as-data,
  centralized RBAC, team hierarchy, resource modeling for limited
  resources. See `docs/decisions/office-vs-department.md`
  "Infrastructure-primitive review" subsection.
- **v0.12 → v0.13**: **Entity-elevation discipline introduced +
  office-level managed entities concept added** (session-9 followup
  #2, post-broader-review). The discipline: prefer events + nested
  fields + memory entries over new managed entity types. Elevate
  to first-class managed entity only when **stable-identity +
  state-of-record + lifecycle all apply**. Avoids the architecture
  creeping toward a relational SQL schema (one entity per noun,
  foreign keys, joins, normalization rules — catastrophic for
  LLM-mediated AI offices). Right level: closer to **knowledge
  graph + document store with stable references**, not Oracle.
  "Joins" are answered via audit-trail filters, per-entity
  ID-based queries, memory queries, or adapter APIs — no join
  planner needed. New concept: **office-level managed entities**
  (Client, Actor) — owned by the office substrate, referenced by
  multiple departments. Distinct from department-level managed
  entities (Project, Invoice, Timesheet) — owned by a single
  department. Cross-department reference convention: entities
  hold `<entity>_id: str` fields referencing other entities; gate
  validates references exist at write time; no FK enforcement at
  storage layer. Approval flows demoted from managed-entity
  proposal to event-kinds on AuditEvent (folds into #6) per the
  three-test discipline. New v1 commitment **#15 (Client + Actor
  as office-level managed entities)** scheduled between #13 and
  #6. See `docs/decisions/office-vs-department.md` "When to
  elevate to managed entity" + "Approval flows are event-driven"
  subsections.
- **v0.11 → v0.12**: **Managed-entity concept introduced + meta-rule
  1 integration-adapter pattern generalized** (session-9 followup).
  The post-#12 first-pass realization: each department defines its
  own entity types completely; **there is no universal entity-type
  core**. Departments contribute "managed entities" (Project for
  planning, Invoice for invoicing, Timesheet for PM, Asset for
  brand-voice, Matter for legal-work) in one of two delivery modes:
  **native** (PBS owns system-of-record; Pydantic schema +
  native MCP tools) or **adapter-delegated** (external system owns
  system-of-record; integration adapter contract). Mixed-mode is
  required and supported per-entity (a department can have some
  entities native + some adapter-delegated). The adapter mode
  **generalizes meta-rule 1's existing integration-adapter pattern**
  from auxiliary integrations (email, calendar, scanner) to primary
  department system-of-record (Invoicing/PM/HR external systems);
  same Pydantic Protocol + concrete adapter contract, expanded
  consumer set. Project (PBS bauleitplanung) reframed as planning
  department's primary native managed entity (not "extension of a
  universal Project core"). #9's mission reframed from "extract
  universal core from PBS-specific extension" to "design the
  department module contract + managed-entity concept + per-
  company customization mechanism." See
  `docs/decisions/office-vs-department.md` "Department-managed
  entities + delivery modes" subsection.

> **Scope boundary.** This doc covers placement (which entity type /
> where). For *within-tier idioms* (how to write the thing once
> you've decided where it goes) see:
>
> - `docs/plugin-conventions.md` — Skill Bundle idioms (frontmatter,
>   semver, body patterns, references organization, routing
>   handoffs).
> - `docs/backend-conventions.md` — Backend idioms (test layout,
>   logging, MCP error format).
>
> Conventions docs trace decisions back here but never re-litigate
> placement.

## Data + boundary reference card

**Use this first** when a "where does X go?" question arises
mid-design. Each row links to the detailed section that owns the
rule. Pure consolidation — no new rules; this card replaces the
chase-six-sections pain when applying existing disciplines.

| When you're asking… | Look here | One-line rule |
|---|---|---|
| Where does X live across scope axes (universal vs domain vs state vs department vs office vs project)? | Meta-rule 3 + scope-orthogonality layering convention | 6 axes, orthogonal; place at the **most-specific axis that doesn't lie** about the data |
| Should X be a Pydantic structured field or a markdown body section? | AI-as-runtime hybrid-shape principle | **Structured** for interfaces / identity / persistence / machine contracts; **prose** for semantics / rules / domain knowledge / process |
| Should X be enforced structurally or by deployment-time convention? | Make wrong shapes impossible, not solvable | If gate / Pydantic / dispatch touches X on every read/write → **structural**. If AI applies X at mint-time / decision-time → **prose convention with audit**. **Sub-rule**: if external system / scheduler / cron needs to dispatch on X (per Gap A proactive time-driven triggers from #12 infrastructure-primitive review) → structural, even if conceptually "feels like" a rule |
| Should X be elevated to a managed entity, or stay as memory entry / event / nested field? | Entity-elevation discipline (3-test) | Elevate ONLY when stable-identity AND state-of-record AND lifecycle all apply. **Reference-style entities** (citations, regulations, sources) pass via "active vs amended/overturned" lifecycle. **When 3-test passes, choose NEW type only if Layer-2 schema differs structurally from existing types**; otherwise reuse existing type with `category` field or scope distinction (e.g., funding sources reuse `reference` type with `category: funding-source`, not a new `funding_source` type) |
| Is X shared across multiple departments? | Office-vs-department (#12) + office-level managed entities (#15) | If shared (Client referenced by planning + invoicing; Actor referenced across departments) → **office-level managed entity** at `extensions/office/...`. Cross-department references via `<entity>_id: str` Layer-2 fields; gate validates references exist at write time. Department-only entities stay at department level |
| Should X be Pydantic-validated or LLM-judged? | Validation layering (v0.18) | Deterministic primary (Pydantic / type / threshold) where the answer is determinate; LLM secondary for genuine judgment (prose precision, fit-to-shape) |
| Should X be in v1 framework now, or deferred? | Pattern-vs-instance + sharp defer rule (v0.20) | Defer ONLY for chronological reason (info doesn't exist yet). Up-front costs ("more sessions", "premature", "PBS doesn't need it yet") are NEVER valid defer reasons |
| When does X mutate, append, or stay forward-only? | Three evolution patterns (v0.19) | **Mutable** (migration framework, e.g., office-config) / **append-only** (additive backward-compat, e.g., AuditEvent) / **forward-only prose** (no migration; historical anchoring via `git_sha` / `convention_applied`) |
| Does X go through MCP gate or direct file Read/Write? | Meta-rule 4 + fail-closed corollary | Contract-bearing files (typed Pydantic + cross-ref invariants) go through gate; loose markdown is skill-direct. Fail-closed on MCP unreachable — never bypass |
| Where does X get its source-of-truth + invalidation contract? | Meta-rule 3 | Each piece of state has exactly ONE canonical source; invalidation contract names what changes when source changes |
| When does X integrate via adapter vs native? | Meta-rule 1 + Glue-not-replacement | If external system already owns the data → **adapter** (Lexware, Personio, Harvest); if PBS owns it → **native** Pydantic + native MCP tool. Mixed-mode within a department supported |
| Where does deployment-specific knowledge for X live? | Governance-and-identity-sourcing decision 4 (prose conventions) | Bureau-specific rules (actor-id minting, archive policy, naming conventions) live in markdown prose alongside the data; AI applies at runtime; AuditEvent records `convention_applied: {file, section, git_sha}` |
| What's the entity-md frontmatter contract? | entity-md-spec §3-§5 | **Layer 1 universal** (every entity, Pydantic base, strict-locked) + **Layer 2 type-specific** (Pydantic subclass per type, strict-locked) + **Layer 3 per-deployment** (deferred to #9 implementation) |
| What's the type-name namespacing? | entity-md-spec §3.2 | `type: <scope-id>.<short-name>` always (e.g., `planning.project`, `office.actor`, `universal.reference`). Department namespacing makes collisions impossible by construction |
| Should X have informed defaults shipped or empty canvas? | Informed defaults (v0.18) | Ship best-shape templates derived from PBS pioneer instance, NOT empty canvases. Bureaus inherit working starting points; refine from a base, not bootstrap |
| Should X fail-loud or fail-soft? | Strict-validation discipline (meta-rule 4 corollary) | Required = fail-loud, no silent defaults; optional = explicit null. No silent fallback for contract-bearing concerns |

### How to use this card

When a design question surfaces mid-session, walk the table top
to bottom; the first row that fits is usually the answer. If two
rows seem to apply, the more-specific one wins (e.g.,
"namespacing the type field" is governed by §3.2 first, then by
"Make wrong shapes impossible" — they agree, but §3.2 is the
specific case).

If the question doesn't fit any row → it's a candidate for a new
discipline; flag for design-review target 14 (discipline-gap
detection).

---

## Maintenance discipline

A 6-step checklist:

1. Every meta-rule change, schema bump, or significant refactor
   lands in the same commit as the ARCHITECTURE.md update.
2. After meta-rule additions / refactor sweeps, run `audit` (drift
   detection) and `design-review` (soundness review) — see
   `plugin/skills/{audit,design-review}/`.
3. **Reference card + detailed section sync**: when changing a
   discipline (wording, scope, discriminator), update BOTH the
   "Data + boundary reference card" row AND the detailed
   discipline section in the same commit. The card is the
   navigation; detailed sections carry the authoritative wording
   + reasoning. Same-commit update prevents drift between the
   two.
4. Sunset deprecated concepts via the deprecation procedure (below).
5. **Validation-gating inventory sync**: when adding a new gate /
   audit slice / design-review target / runtime convention, update
   the corresponding inventory row in
   `docs/validation-gating-overview.md` §4 in the same commit as
   the source-of-truth artifact (Pydantic file / slice description /
   target description / convention md). Inventory rows point at
   source of truth; same-commit update prevents drift between the
   layered systems-view and the detailed authoring sites.
6. **Periodic greenfield review at major version boundaries**:
   at significant ARCH version increments (0.x → 0.x+5 or per
   major-commitment milestones — e.g., #9 ships, #11 ships, Phase
   1 ships, v1.0 ships), run a greenfield-with-VISION-as-anchor
   review per `docs/decisions/greenfield-architecture-review.md`
   methodology. Walk architecture asking "would we build this from
   scratch?" Verifies disciplines remain VISION-anchored;
   structurally catches cargo-cult drift (per failure-mode-catalog
   "cargo-cult patterns" entry — closes its PARTIAL → COVERED
   coverage status). Exercise produces fresh decision record
   capturing alternatives considered + verdict. Added v0.28 after
   session-11 architectural-gap detection sweep surfaced cargo-cult
   PARTIAL coverage.

### Deprecation procedure

When retiring a concept (entity type, meta-rule, MCP tool name,
skill, etc.):

| Concept | Procedure |
|---|---|
| **Skill** | Bump major + add `deprecated: true` to frontmatter; remove after 1 plugin release. Document successor in description. |
| **MCP tool** | Alias old name → new for one minor version of pbs-mcp; remove after that. |
| **Entity type** | Pre-launch (now): rewrite ARCHITECTURE.md + sed across repo in one commit. Post-launch: announce in HANDOFF, add to deprecated-concepts list, give 1 release deprecation window. |
| **Meta-rule** | Reformulate in-place with explicit replaces-X note. Audit + design-review on next refactor verifies the replacement holds. |
| **Office-config field** | Bump schema_version + write migration that drops the field; existing offices forward-migrate transparently. |

Pre-launch / pre-distribution: deprecation is essentially
free — change in place. After first user-facing release the
procedure tightens.

---

## Pattern-vs-instance discipline

**The framing**: PBS is **the framework foundation for the
consulting business**, validated by the Schulz planning bureau.
PBS is the pioneer instance, never the product. Every
architectural commitment, every defer rationale, every design
decision serves the framework. The framework must work at
**first bind** for any expert-practitioner deployment
(legal-practice, research-lab, brand-voice, consulting-client)
— not minimum-viable-PBS today with infrastructure added later
when consulting demand surfaces. "Adding it later" means clients
hit gaps at first bind; that's the failure mode this discipline
prevents.

Every architectural commitment in this repo must work at the
**pattern level**, not just for PBS. The architecture is the
pattern; PBS is the proving instance. The long-arc end-state is
an AI-office builder that scaffolds new domain offices from a
domain spec + the accumulated patterns (see ROADMAP v2
"AI-office builder"). Every commitment that doesn't generalize
is a future migration cost the builder will pay; every
commitment that does generalize *is* the builder's foundation.

**The test** when proposing any new meta-rule, entity type,
persistence structure, MCP tool, or decision-record-grade
commitment:

- Would this work for a hypothetical **legal-practice office**
  (intake / discovery / filing / argument phases; courts /
  opposing-counsel / regulators as authorities; precedents +
  citations + templates as memory taxonomy)?
- Would this work for a hypothetical **research-paper-review
  office** (manuscript / review / revision / publication phases;
  journals / co-authors / reviewers as authorities; citations +
  prior-work + templates as memory taxonomy)?
- Would this work for a hypothetical **engineering-doc office**,
  **medical-records-workflow office**, **regulatory-filing
  office**?

If yes for at least 2 of these 3-5 hypothetical domains: the
commitment is pattern-level. Lock it in.

If no for most: the commitment is too PBS-coupled. Push it to
the **instance layer** — skill bodies (drafting drafts plug in
domain-specific doctype templates), manifests (domain-specific
references + actors), office-config (domain-specific scope
fields), korrektur-rules and similar prose memory.

**Where the line typically falls:**

| Layer | Pattern (stays in architecture) | Instance (lives in PBS or its successors) |
|---|---|---|
| Meta-rules 1-4 | All four | (none — they're patterns by construction) |
| Entity types (Skill / Memory / Configuration / etc.) | The taxonomy itself | What entities exist (which skills, which memory records) |
| MCP tool *patterns* | strict-validation discipline; fail-closed corollary; CRUD-style memory tools | Tool *names + bodies* (which gates exist; what they do) |
| office-config *schema shape* | layered manifests, scope.domains, paths.* discipline | Specific fields (verfahren_type values, doctype list, korrektur-rules path) |
| VISION axes | Three-axis framing (intertwining / sparring / authorship preservation) | Per-axis *content* — what counts as authorship in the domain |
| Decision-record format | The structure itself (Context / Decision / Why / Alternatives / Revisit) | Specific decisions — which mechanisms are committed |

**Anti-patterns the discipline catches:**

- ❌ A meta-rule that names "B-Plan" / "Begründung" /
  "Festsetzungen" in its body. Those are PBS instance content;
  the rule should describe the *shape* (e.g., "doctypes have
  required + optional sections per their manifest entry") and
  let PBS provide instance content for that shape.
- ❌ A persistence structure assuming German legal taxonomy
  (gesetze / urteile / leitfäden) at architectural layer.
  Pattern is "layered references manifest with invalidation
  contract"; instance is the German-law taxonomy.
- ❌ An MCP tool whose *interface* embeds domain knowledge
  (e.g., `validate_b_plan_begruendung` as a tool name). Pattern
  is `validate_doctype(doctype: <slug>)`; instance is what
  doctypes exist.
- ❌ A skill body that hardcodes domain-specific values rather
  than reading from office-config or manifests. Already covered
  by plugin-conventions §13 anti-pattern; now also a
  pattern-vs-instance violation.
- ❌ A defer rationale anchored in PBS-instance state ("today no
  department needs activating," "only planning exists right now,"
  "no consumer in PBS until #11"). Pioneer-instance defenses
  silently optimize for PBS instead of the framework. The
  framework's consumers include hypothetical legal-practice /
  research-lab / consulting-client deployments opening tomorrow
  — and most of them will need the deferred infrastructure at
  first bind. See "Defer rule" subsection below.

### Defer rule: chronological reason only

The discipline's operational rule for deferring any
infrastructure-shaped commitment (a skill, a gate, a Pydantic
class, a registration mechanism, an audit slice, a body
convention, a Layer-2 schema field):

**Defer ONLY for chronological reason** — i.e., the design
genuinely depends on information that doesn't exist yet:

- Downstream consumer's shape isn't locked → designing now would
  lock the wrong abstraction
- Second-domain deployment is required to validate the
  abstraction → without it the design over-fits PBS
- Upstream decision is unresolved → depends-on chain is real
- Genuine ordering constraint that the design's correctness
  depends on

**Up-front costs are NEVER valid defer reasons:**

- ❌ "It would take more sessions" — irrelevant; do the full work
- ❌ "We might design it wrong" — only relevant if a NAMED future
  signal would change the design; otherwise design now
- ❌ "Premature abstraction" — without a specific information gap,
  this is manufactured restraint
- ❌ "YAGNI" — the canonical form of manufactured restraint;
  rejected
- ❌ "PBS doesn't need it yet" / "only planning exists today" /
  "no consumer in PBS until #11" — pioneer-instance bias; the
  consulting framework's consumers include hypothetical
  deployments opening tomorrow
- ❌ "We can add it later when needed" — adding later means
  consulting clients hit the gap at first bind

**Two tests in order, both must pass for a defer to be honest:**

1. **Chronological test**: "Is there a specific piece of
   information that would change this design, and that
   information will exist later but not now?" If yes, name it
   explicitly. If no, the defer is invalid — design now.
2. **Framework-cost test**: "Would a hypothetical legal-practice
   / research-lab / consulting-client deployment opening tomorrow
   need this?" If yes, it's framework infrastructure — design
   now regardless of PBS state.

The rule composes with the existing "honest defers name a
specific cost" guidance (see `feedback_defer_instinct.md`
memory): the named cost must be a **future-information cost**
(the chronological test passes), not an up-front cost.

This rule was added v0.20 after a session-11 design loop where
the AI repeatedly produced PBS-instance-anchored defer
rationales despite the discipline being named since v0.8.
Sharpening was required because the discipline as previously
written caught content-coupling at architectural-rule level but
not pioneer-instance bias at defer-rationale level. The bias is
particularly insidious because it *looks like* sober "wait for
pressure" reasoning.

**Coupling exceptions** (where domain-coupling at architecture
level is allowed):

- The *vocabulary* used in examples (decision records, ARCH
  body) can use PBS terminology for legibility, as long as the
  underlying rule generalizes. "PBS bausteine" in an example is
  fine; a rule that *only* makes sense for PBS bausteine is not.
- The instance directory itself (`extensions/`, `memory/`,
  `office-config.yaml` populated values) is unconditionally
  PBS-instance. The pattern is the *schema*; PBS is the
  *content*.

**Discipline check at audit/design-review time:**

- Audit slice 14 (boundary adherence) extends naturally to this:
  "is this commitment pattern-level or instance-level?" applies
  to placement of decisions across the architecture/instance
  boundary, same way it applies across the LLM/Python boundary.
- Design-review target 9 (Subsumption check) implicitly tests
  this: a new mechanism that subsumes a PBS-specific legacy
  mechanism *and* generalizes is correct; one that subsumes
  PBS-specific in a PBS-specific way perpetuates the coupling.

**Connection to current work**: every session-7 commitment
(meta-rule 4 fail-closed corollary, target 9 subsumption check,
audit slice 18 legacy retirement scan, framing skill, audit-trail
v2 single-write architecture, Skill Bundle frontmatter
convention) is pattern-level by construction. The discipline
makes that property explicit and load-bearing for future work.

### Validation under the single-domain-pioneer constraint

PBS is operated by a single planning-domain expert. Realistically
**we will not implement second-domain instances ourselves** —
legal practice, research, engineering, etc. are domains the user
doesn't work in. Hand-building a "second instance" in a domain
the user doesn't actually practice would produce evidence of
*the user's idea of that domain*, not of the actual domain —
worse than no evidence, because misleading.

This constraint shapes the validation strategy: we **cannot** use
"build 2-3 hand-instances and measure overlap" as the validation
path. Waiting for empirical evidence from a real second-domain
deployment that may never come (consulting engagement; second
office adoption) becomes manufactured restraint disguised as
rigor — a way to defer architectural decisions indefinitely.

**Working method instead — best-effort split + immediate PBS
validation:**

The split is implemented now (pre-RAG), against PBS, with two
distinct validation signals:

| Signal | What it tells us | Source |
|---|---|---|
| **#1 — split doesn't break PBS** | The proposed split is implementable; refactor is executable; tests pass; skills route correctly; project state round-trips. Catches mechanics-level issues that pure reasoning misses. | Implementing the split now against PBS — **immediate** feedback. |
| **#2 — split chose the *right* boundary** | The pattern/instance line generalizes to other domains. Catches the split being too PBS-shaped (overfit). | Only known when a real second-domain implementation lands — **deferred, possibly indefinite**. |

Signal #1 is necessary-but-not-sufficient: confirms no regression
but can't confirm correct boundary. Signal #2 confirms boundary
but requires implementation that may never happen here. **Doing
the split now is the maximum validation we can extract before
signal #2 arrives — and crucially, doing it later is more
painful** (post-data-accumulation refactor + skill retrofits +
migration scripts vs. clean refactor today). The 3-5 hypothetical-
domain thought experiment (legal-practice, research-paper,
engineering-doc, medical-records, regulatory-filing) is the
*reasoning input* to the split; signal #1 is the *immediate
empirical check*; signal #2 waits for real second-domain.

**The thought experiment as legitimate epistemic basis**: it
doesn't require working in those domains, just thinking carefully
about them as architectural-imagination targets. Signal #1
catches what the thought experiment missed at implementation
level; signal #2 (when/if it arrives) catches what both missed
at boundary level.

This explicitly is a **best-effort** discipline, not a proven
one. The split *will* be wrong somewhere; the question is
whether it's *less wrong than no split* and *less expensive to
correct than no-split-then-painful-migration*. Pre-RAG is the
unique window where the cost answer is "yes."

Pre-RAG commitment #9 (`ROADMAP.md`) is the concrete realization:
the reasoning pass + best-effort split implementation + PBS
regression validation are bundled as one work stream, scheduled
before Phase 1 corpus download.

### Office-vs-department distinction (resolved session 9 per #12)

**Problem surfaced session 7 (after partner-built plugin
comparison)**, **resolved session 9** per
`docs/decisions/office-vs-department.md`. This section captures the
architectural distinction; the decision record carries the full
per-question reasoning + downstream constraints + defers.

The term "office" in PBS-bureau was used for two distinct things
that needed separation:

- **Department**: a single capability area with its own
  workflow, doctypes, memory, and external authorities. Examples:
  planning-document-work (what PBS implements today), project-
  management, invoicing, HR, marketing, brand-voice, legal-work.
  Anthropic's `partner-built/brand-voice` is a department-shaped
  plugin (one capability, three skills, three commands).
- **Office**: a container for *multiple departments*, coordinated
  via shared office-level state (projects, clients, deadlines,
  actors), natural abstractions (a "project" entity flows between
  departments), ad-hoc context sharing (explicit data-passing for
  non-obvious flows), and integration/setup configuration.

PBS-bureau today **conflates the two**: we have one department
(planning-document-work) wrapped in office-level scaffolding
(setup-office, office-config.yaml, projects-index, references-
manifest, orchestrator). A real Schulz Planungsbüro has at least
three departments: planning-document-work + project-management +
invoicing. Other PBS-shaped offices would have similar shapes.

**Implications under pattern-vs-instance discipline:**

- Pattern: office structure containing N departments.
- Instance: PBS office contains {planning-document-work, PM,
  invoicing} (eventually); a hypothetical legal practice office
  contains {legal-work, matter-management, invoicing}; a
  research lab office contains {research, grant-management,
  lab-operations}.
- Office-config.yaml gains `departments.<name>` sections.
- Skills gain a `department:` frontmatter field (REQUIRED, no
  silent default per strict-validation discipline); office-level
  skills declare `department: office`.
- Memory taxonomy gains a 4th orthogonal axis: scope-orthogonality
  becomes (universal × domain × state × department), opt-in per
  entry. Most existing entries stay in the original 3 cells;
  department-specific entries declare the 4th.
- Cross-department workflows are **event-shaped, not call-shaped**
  (per Row 4 of `a2a-and-gemini-pattern-emulation.md`). Each
  department declares `event_subscriptions:` in
  `extensions/department/<dept>/department.yaml`; orchestrator's
  watch-list extends to filter by subscription + exclude self-
  emitted events. No new event mechanism — reuses AuditEvent
  infrastructure.
- ProjectState gains `departments_active: list[str]` field for
  routing + audit-filter purposes. Gate-mediated update via
  `record_audit_event` (logic deferred to #6 retrofit).
- Skills are **singleton-department**; multi-department coordination
  via office-level orchestrating skills.
- Offices have **0..N departments** — zero (single-skill utility),
  one (PBS today, brand-voice partner-built plugin), or many
  (Schulz future, hypothetical legal/research/medical offices).
- AI-office-builder (v2) generates offices with whatever department
  composition the domain spec declares. Per-domain spec input
  includes department list + per-department config + integration
  spec.

**Pattern-vs-instance limitation surfaced**: project-as-long-running-
entity is PBS-instance, not pattern-universal. Some offices
(brand-voice, single-skill utilities) have no project entity.
Architecture supports both project-having and project-less offices.
Constraint passed to #9 (Pattern-vs-instance split): ProjectState
core/extension split should make the project entity itself an
opt-in extension, not a pattern-level mandatory.

**What's deferred and where** (per `office-vs-department.md`):
- Per-department phase tracking (`phases: dict[str, str]`) and
  per-department lifecycle (`lifecycle: dict[str, Lifecycle]`) →
  #9 (Pattern-vs-instance split, still pre-RAG).
- Office-config `departments.<name>` schema bump + migration → #11
  (Cowork integration, co-located with `pbs.local.md` migration).
- Skill frontmatter `department:` sweep across all 19+ skills → #11.
- `extensions/department/<dept>/department.yaml` event_subscriptions
  file format implementation → #11.
- `integrate-department <slug>` skill creation → #11.
- `record_audit_event` gate-side `departments_active` update logic
  + `query_audit_trail` `department:` filter → #6 (audit-trail v2
  retrofit).
- `search_corpus` `department_filter:` arg → Phase 1 corpus work.

**Connection to brand-voice comparison**: brand-voice is a
single-department plugin (in our framing: one department, all
skills declare `department: brand-voice`, no cross-department
coordination needed since N=1). PBS today is also a single-
department office (planning-document-work). The pattern handles
N=0/1/many uniformly.

---

## Entity-elevation discipline

A load-bearing companion to pattern-vs-instance discipline. Where
pattern-vs-instance asks "is this commitment at the right *level*
(pattern or instance)?", entity-elevation asks "is this concept
*entity-shaped at all* (vs event / nested / memory / config)?"

**The principle**:

> **Prefer events + nested fields + memory entries over new
> managed entity types. Elevate to first-class managed entity
> only when stable-identity + state-of-record + lifecycle ALL
> apply.**

**Why this matters**: pre-emptively elevating concepts to
first-class managed entities (Pydantic schemas + MCP CRUD tools +
persistence) creates schema sprawl. Each new entity adds: storage
layer commitments, query surface, migration burden, schema
versioning overhead, and cognitive load on every consumer. The
risk if undisciplined is the architecture creeping toward a
**relational SQL schema** — one entity per noun, foreign keys,
joins, normalization. That's catastrophic for LLM-mediated AI
offices: it makes the architecture brittle, slow to evolve, and
re-implements enterprise software's worst tendency.

**Right level**: closer to **knowledge graph + document store
with stable references** than Oracle. Entities have identity
(referenced by ID); relationships ride in audit-event details +
ID fields on entities; "joins" are answered via filtered queries
over events / per-entity stores / memory / adapter APIs. **No
join planner needed.**

### The 3-test (all three required to elevate)

For each candidate, walk all three:

1. **Stable identity** — has an ID/slug that persists across
   sessions and is referenced by other things?
2. **State of record** — has fields whose authoritative current
   value matters (not just historical)?
3. **Lifecycle** — has phases or status that progress over time?

**If all three**: managed entity. Lock in.
**If any missing**: route to the appropriate alternative —
event-kinds (moments-when-things-happened), nested fields
(data only meaningful in context of a parent), memory entries
(prose-shaped knowledge), or reference data (static / config).

### Worked-example reasoning

| Concept | Identity | State | Lifecycle | Verdict |
|---|---|---|---|---|
| Project, Client, Actor, Invoice, Asset, Matter, Manuscript | ✅ | ✅ | ✅ | ✅ entity |
| Approval, Decision, Send, PhaseTransition | each is one moment | fixed at action | doesn't progress | ❌ event kinds on AuditEvent |
| LineItem, Deadline, ContactPerson | only as part of parent | not independent | none | ❌ nested fields |
| Notification | inbox is state-of-record | external system | external system | ❌ adapter + event |
| Report, Dashboard | generated on demand | projection | none | ❌ generated artifact (render_*) |
| BusinessCalendar | yes | yes | none | ❌ reference data (config) |
| DocumentVersion | snapshot ID | immutable | none | ❌ event + bytes |

### How "joins" are answered without foreign keys

| Question | SQL approach | PBS approach |
|---|---|---|
| "All invoices for client X" | `JOIN` | Adapter API: `lexware.invoices(client_id=X)`. Or audit-trail filter. |
| "All projects with overdue deadlines" | `WHERE deadline < NOW()` | Native query on Project store filtered by `deadlines[].date < today`. |
| "Audit history of decisions made by colleague Y" | Multi-table join | Audit-trail filter: `actor=Y AND kind=decision`. |
| "Which bausteine cite §44 BNatSchG?" | Full-text + reference table | Memory query (post-#14): `search_memory(query="§44 BNatSchG", kinds=["baustein"])`. |

Filtered queries over a small set of stores. No join planner.

### Where the discipline is enforced (multi-checkpoint)

Defense in depth — discipline applied at five points in the workflow:

1. **Conversational gate (in-chat)** — when proposing a new entity
   during design discussion, walk the 3-test out loud before
   anything is persisted.
2. **Design-review target 11 (PRIMARY GATE — prospective)** —
   when a decision record / refactor / new commitment proposes a
   managed entity, target 11 enforces the 3-test before persistence.
   Same role as target 9 (subsumption) and target 10 (pattern-vs-
   instance).
3. **Decision-record convention** — any decision record naming a
   new managed entity must include explicit 3-test verdict
   subsection (per-criterion yes/no with reasoning).
4. **`integrate-department` runtime gate (post-#11)** — when
   onboarding a new department to a deployment, the skill walks
   each `managed_entities:` declaration in `department.yaml` and
   runs the 3-test interactively. Catches department-module-
   author drift.
5. **Audit slice 20 (retrospective)** — scheduled / on-demand scan
   of `extensions/.../entities/` Pydantic schemas + decision
   records, scoring against the 3-test. Catches drift over time.

Each catches a different failure mode. Discipline in design AND
in code AND in audit — analogous to meta-rule 4's strict-validation
defense in depth.

### Connection to other disciplines

- **Pattern-vs-instance** (above): different question. Pattern-
  vs-instance asks "right *level*?" Entity-elevation asks
  "entity-shaped *at all*?" Both apply at design time.
- **Subsumption check (target 9 / slice 18)**: when entity-
  elevation passes (entity-shaped is right), subsumption check
  separately asks what existing mechanism it replaces.
- **Strict validation (meta-rule 4)**: once an entity is correctly
  elevated, meta-rule 4's discipline applies to its Pydantic
  contract (required fields strictly required, no silent defaults
  for missing data, fail-loud on contract violation).

See `docs/decisions/office-vs-department.md` "When to elevate to
managed entity (the three-test discipline)" subsection for the
full reasoning + examples.

### Elevation analogue for skills (added v0.27 — skill-granularity criteria)

The same restraint-in-elevation discipline applies to skills, but
with different criteria. Where entity-elevation asks "is this
concept entity-shaped (vs event / nested / memory / config)?",
**skill-elevation** asks "is this concept skill-shaped (vs
in-skill content distributed across body + references + memory +
process entities)?"

**The skill-granularity principle**:

> **Prefer distributed in-skill content (body prose + skill
> references + memory bausteine + process entities + RAG corpus)
> over new specialist skills. Elevate a topic to its own skill
> only when distinct workflow + distinct output + reuse across
> projects ALL apply.**

**The 3-test for skills** (parallel structure to entity-elevation
3-test, distinct criteria):

| Test | Question | Why it matters |
|---|---|---|
| **Distinct workflow** | Does the topic have its own multi-step interaction shape that doesn't fit inside a broader skill's workflow? | A topic that uses an existing skill's workflow with parameter modifications is in-skill content, not a new skill. |
| **Distinct output** | Does the topic produce a distinct artifact / output the user receives, not a section/variant of a broader skill's output? | A topic producing a section of an existing skill's output is in-skill content. |
| **Reuse across projects** | Does the topic's workflow + output recur across multiple projects? | Single-project niche topics stay as in-skill content (or per-project memory). |

**Worked example — §13a-Verfahren**:
- Distinct workflow? **No** — drafting under §13a uses the SAME
  Begründungs-writing workflow as Regelverfahren, with §13a-
  specific modifications (drop Umweltbericht section, add §13a-
  citation template). The workflow is the SAME skill, parameterized.
- Distinct output? **No** — output is still a Begründung.
- Reuse across projects? Yes (any project under §13a) — but
  doesn't satisfy 1+2.

→ **Fails skill-granularity criteria. Lives as distributed
content fueling the broader Begründungs-writer skill** (per
`docs/decisions/skill-expert-agent-and-domain-knowledge.md`
Decision 4).

**Why this matters** (parallel to entity-elevation reasoning):
pre-emptively elevating fine-grained topics to separate skills
creates skill sprawl, fragmented routing, harder maintenance, and
loses the AI-as-runtime-composes advantage. Per
AI-as-runtime hybrid-shape principle: AI composes per-context
behavior at runtime from distributed sources (process entity +
references + skill body + memory). Topic-shaped content fueling a
broader skill is the canonical AI-as-runtime application.

**Anti-patterns the skill-granularity discipline catches**:

- ❌ Creating `§13a-Verfahren-expert` skill that duplicates
  Begründungs-writer's workflow with §13a tweaks. Should be
  in-skill content (process entity + references + skill body
  knows-when-to-read).
- ❌ Creating per-doctype-section skills (`section-1-introduction-
  expert`). Each section is a sub-step within doctype-drafting,
  not a distinct workflow.
- ❌ Creating per-edge-case skills (`late-Stellungnahme-handler`).
  Edge cases are conditions within process entities + skill
  body branching, not distinct skills.

**When elevation IS warranted**: when a concept genuinely has
distinct workflow + output + reuse — like `verify-citations`
(distinct workflow: walk every citation, fetch source, verify
quote; distinct output: citation-verification report; reuse:
every drafting cycle). That passes all 3 tests.

**Composition with entity-elevation**: a topic might fail
skill-elevation but PASS entity-elevation (e.g., a Process entity
that's stateful with phases + lifecycle is an entity, not a
skill). The two analogues compose — every concept gets evaluated
against its appropriate elevation criteria.

**Source of truth**: `docs/decisions/skill-expert-agent-and-
domain-knowledge.md` Decision 4 + `docs/plugin-conventions.md`
§14 (skill granularity guidance).

---

## Glue-not-replacement principle

PBS is **the glue layer** that brings cross-concern AI-mediated
reasoning to existing infrastructure. It is **not** a replacement
for the systems customers already have (BPMN engines, accounting
tools, CRMs, time-tracking, calendars, ticketing systems, etc.).
The architecture is integration-first by design.

**Why this matters**: most enterprises have **decades of
investment** in workflow / accounting / case-management
infrastructure. Selling rip-and-replace is a losing pitch — both
practically (the migration is too expensive) and politically (the
internal champions of those systems block adoption). The
addressable market for "AI office that augments your existing
stack" is **substantially larger** than "AI office that replaces
your existing stack."

**The principle, stated**:

> **PBS connects to existing infrastructure where it exists;
> provides native alternatives where it doesn't. Both modes work
> uniformly through the same framework. We never ask the customer
> to choose between AI augmentation and their existing
> investment.**

**Concrete implications across the architecture**:

| Principle expression | Architectural mechanism |
|---|---|
| Existing accounting tool? Use it. | Adapter-mode managed entity (`Invoice` via Lexware/FastBill/sevDesk adapter) per #12 |
| Existing time-tracking? Use it. | Adapter-mode managed entity (`Timesheet` via Harvest/MOCO adapter) |
| Existing BPMN/workflow engine? Augment it. | BPMN-engine adapter class (v1.x-v2 ROADMAP); service-task delegation + decision-automation + cross-process intelligence layered ON TOP |
| Existing calendar? Connect to it. | Adapter-mode (CalDAV / Google / Microsoft) |
| Existing CRM? Connect to it. | Adapter-mode managed entity (`Client` via Salesforce/HubSpot adapter) |
| No existing tool? Use built-in. | Native-mode managed entity (`Project` for B-Plan workflows; PBS IS the SoR — no external alternative exists) |
| Existing audit / compliance system? Augment with AI-mediated reasoning. | Cross-process events flow as `actor_kind=external_agent`; PBS adds judgment-mediated layer to existing audit infrastructure |

**The architectural mechanism the principle relies on**:

- **Meta-rule 1's integration-adapter pattern** (`Pydantic Protocol` + concrete adapter implementations selected per office-config) — already established
- **Adapter-mode managed entities** (per #12, `office-vs-department.md`) — generalizes the pattern from auxiliary integrations to primary department system-of-record
- **Adapter-emitted events** (per #9 Gap B, `office-vs-department.md` infrastructure-primitive review) — bidirectional flow; external state changes emit `actor_kind=external_agent` audit events
- **Mixed-mode per-entity** (per #12) — a single department can have some entities in adapter mode, some in native mode. Real-world deployments mix.

### Role-shift framing — what changes for the worker (per VISION axes)

The principle has a sharper worker-facing implication, grounded in `VISION.md` axes 1-3 + Vivienne Ming's research on AI-human hybrid teams (oracle / validator / sparring partner modes).

Specialized tools historically did **two jobs in one bundle**:
1. **Authoring** — creating and modifying the underlying data
2. **Presentation / review / output** — rendering, exporting, reviewing the result

The role-shift: **specialized tools' authoring role moves; presentation/review role stays.** But the shift isn't uniform — it splits along VISION axis 2's mode distinction:

**Mechanical authoring** (drawing geometry, formatting LaTeX, computing fields, routine drafting, file-format conversions, cross-reference lookups):
- **Full automation** — AI takes over completely via specialized API layers (gis_utils for GIS, latex/PDF skills for documents, integration adapters for accounting/calendar)
- The worker's cognitive load on this layer → 0
- The specialized GUI tool (QGIS, AutoCAD, etc.) reduces to its **presentation/review surface**

**Substantive authoring** (judgment-bearing decisions: which argumentation type, which legal interpretation, which scope, which classification scheme):
- **Sparring mode** (NOT full automation; per VISION axis 2 — Ming's productive mode)
- AI generates options + counter-arguments + alternatives; human pushes back, interrogates, commits
- Cognitive ENGAGEMENT preserved (per VISION axis 3 defensibility test)
- Time + friction substantially down vs solo work (options presented; counter-arguments surfaced; references at hand; mechanical layer freed time returns to substantive engagement)

**Net result for the worker**: less time + less friction + better accuracy + preserved cognitive engagement. **All four, simultaneously.** The substantive thinking remains theirs; the supporting infrastructure carries weight that used to cost time + friction without adding value. The thinking gets *better-supported*, not *easier in the dishonest "AI did it" sense*.

**The trap to avoid** (per Ming's research warning):
- **Oracle mode** (humans submit AI's answer; performance same as AI alone) — destroys human contribution
- **Validator mode** (humans seek AI confirmation; sycophancy loop; performance worse than AI alone) — actively degrades

**The architecture's job is to keep the worker in sparring mode for substantive work.** VISION axis 2's sparring requirements (counter-argument-as-first-class, anti-sycophancy guard, commit-to-recommendations, asymmetric knowledge respect, visible reasoning, selective friction calibration) make this enforceable rather than aspirational. Per the **Information-Exploration Paradox** (VISION §229-247): without these protections, the AI consumes the worker's exploration capacity; with them, the AI augments it.

**For consulting positioning** (see `docs/strategic-positioning.md`
for full treatment + lived-experience credibility framing):

> **"Your BPMN engine handles the workflow. Your accounting tool
> handles invoicing. Your CRM handles clients. Your calendar
> handles scheduling. Your specialized GUI tools (QGIS, AutoCAD,
> domain-specific apps) become presentation/review surfaces. We
> add the cross-concern AI office layer on top — handling the
> mechanical authoring + cross-tool integration + cross-department
> coordination automatically, while keeping the worker in sparring
> mode (not oracle mode) for substantive decisions. Less time +
> less friction + better accuracy + preserved cognitive
> engagement. The friction in substantive work is the feature,
> not the bug."**

This is **a fundamentally different sale** than "buy our AI tool to
replace [vertical SaaS]." Different addressable market; different
political dynamics within enterprise prospects; different
implementation timelines; different risk profile. Also a
fundamentally different sale than the typical AI-tool pitch
("faster answers" — Ming's validator-mode trap; "AI handles
decisions" — Ming's oracle-mode trap).

**Connection to other disciplines**:

- **Pattern-vs-instance**: the glue principle is itself pattern-
  level (every AI office, regardless of domain, integrates with
  domain-relevant existing infrastructure). Instance content =
  which specific adapters exist for the deployment.
- **Entity-elevation discipline**: helps decide which managed
  entities should be native vs adapter-mode. Strong default toward
  adapter-mode when external system is the natural state-of-record.
- **Meta-rule 1 (app-vs-office)**: the integration-adapter pattern
  is the implementation mechanism; this principle states the
  WHY (connect, don't replace).
- **Meta-rule 4 (execution determinism)**: deterministic gates
  delegate to deterministic external systems where they exist;
  judgment lives in the AI layer.

**When this principle pulls against pure native-mode preference**:

If two viable paths exist (native or adapter), default toward
adapter when the customer has the external system. Only choose
native when:
- No external alternative exists (PBS-bureau planning Project)
- The customer is solo / small enough that running an external
  system is overhead (small deployments per #13's CCX23 tier)
- Native gives demonstrable value the adapter can't (e.g., custom
  domain-specific reasoning that pre-exists in PBS's skills)

The architecture supports both modes uniformly (#12); the
principle expresses the strong preference toward integration when
viable.

---

## Make wrong shapes impossible, not solvable

> **Prefer structural constraints (type system, Pydantic, gate
> enforcement) that make wrong shapes impossible by construction
> over conventional solutions that make wrong shapes solvable at
> deployment time. Convention-driven solutions for framework-
> level correctness offload work to every deployment — each
> consulting client hits the same problem, each must solve it
> independently, some solve inconsistently. Make it impossible
> once for everyone.**

This principle composes with AI-as-runtime hybrid-shape (which
assigns the boundary: structured for machine contracts, prose for
semantics) by sharpening the discriminator WITHIN the structured
layer.

### The discriminator

The boundary between "structural constraint" and "prose
convention" is sharp:

| Concern touched by | Layer | Mechanism |
|---|---|---|
| Gate / Pydantic / dispatch code on every read/write | **Structural** — impossible by construction | Type system, Pydantic validators, gate enforcement, namespace separation |
| AI at mint-time / decision-time / reasoning-time (governance check, naming, archival policy) | **Prose convention** with audit trail | Prose rule in `office-config.md` / `department.md` / `conventions.md`; AI applies; AuditEvent records `convention_applied: {file, section, git_sha}` |

If the gate dispatches on it every read/write, design a
structural constraint that makes wrong shapes impossible. If AI
applies it at mint-time or judgment-time, prose convention is
correct — the impossibility-by-construction approach would be
SQL-DB-trap rigidity (per AI-as-runtime hybrid-shape).

### Examples — applied across the codebase

| Concern | Wrong (solvable via convention) | Right (impossible by construction) |
|---|---|---|
| **Type-name uniqueness across departments** | "Bureau documents `type:` namespacing convention; AI validates at activation" | Department-namespaced `type: <scope-id>.<short-name>` (Bundle A lock, session 11). Gate dispatches on full namespaced form — collision impossible |
| **Required AuditEvent fields** | "Skill bodies remember to set `actor_kind` on every event" | Pydantic `actor_kind` field required, fail-loud on missing — impossible to omit |
| **State.md write through gate** | "Skills know to use `update_project_state` rather than direct Edit" | MCP gate is the only write path; direct file Edit lacks the validation contract — impossible to bypass without explicit `fallback_when_mcp_absent` declaration |
| **Manifest contract integrity** | "Author discipline keeps `last_updated` + `last_fetched` + `checksum_sha256` consistent" | Pydantic models validate at parse time (slice 15 → v1 pull-forward); gate rejects malformed manifests — impossible to write invalid shape |
| **Department / Office entity registration** | "Convention: each department lists managed entities somewhere" | `department.md` `managed_entities` Pydantic-validated keyed map; gate's startup discovery enforces shape — registration impossible to malform |

### Examples — where prose convention is the right answer

| Concern | Why prose (not structural) |
|---|---|
| **Actor-id minting convention** (`firstname-lastname` from email) | AI applies at mint-time; deployment-specific; varies per bureau (small bureau ≠ adapter-mode bureau). Gate dispatches on `id` (string), not on its derivation rule — gate never touches the convention |
| **Archive policy** (when projects move to `archived/`, retention windows) | AI applies at archive-decision-time; deployment-specific |
| **Cross-department coordination triggers** ("when planning sends to UNB, notify invoicing") | AI applies at workflow-event-time; deployment-specific; varies per office structure |
| **Doctype filename convention** (`B-Plan Begründung.tex` vs `<project-id>-begruendung.tex`) | AI applies at file-create-time; deployment-specific aesthetic |

### Anti-patterns the discipline catches

- ❌ "Deployment documents the rule; AI validates at activation"
  for a concern the gate dispatches on every operation. The
  gate's hot path can't depend on prose validation; structural
  constraint is required.
- ❌ "Pydantic class with optional field + comment 'should always
  be set when X'." If always-set is a contract, make it
  required. If conditionally-required, encode the condition
  with a discriminated union or `model_validator`.
- ❌ "Future audit slice catches drift." Audit catches drift
  retroactively; the framework should make drift impossible
  prospectively where the constraint is structural.
- ❌ Pure-prose "best practices" docs for things the gate / type
  system / dispatch could enforce. Best-practices docs are for
  AI-applied judgment; framework correctness gets structural
  enforcement.

### Composition with existing disciplines

| Discipline | Connection |
|---|---|
| **Strict-validation (meta-rule 4 corollary)** | Same impulse, narrower scope. Strict-validation says "no silent defaults, fail loud on required fields"; this principle generalizes from validation to all structural design choices, with the gate-dispatch discriminator. |
| **AI-as-runtime hybrid-shape** | Assigns the structured / prose boundary at the top level. This principle sharpens WITHIN the structured layer: don't let convention creep in where structural constraint is possible. |
| **Pattern-vs-instance + sharp defer rule (v0.20)** | "We'll add it later when needed" defers structural work to deployment time; same offloading anti-pattern this principle catches. The two together push toward: design framework-correct shapes now, structurally, for everyone. |
| **Glue-not-replacement** | Adapter Protocol shape is structural (Pydantic Protocol interface) — adapters can't fail by being shape-incompatible. Adapter behavior conventions live in adapter-md prose body. |

### Promotion path (manual now; design-review target if proven valuable)

Apply manually at design-time; track applications and
counter-examples for 3-5 sessions; if the discipline proves
load-bearing, evaluate for elevation to a design-review target
(retroactive scanning) — same staged-elevation pattern that
AI-as-runtime conformance check followed.

---

## AI-as-runtime hybrid-shape principle

> **Domain semantics, process flow, conditional rules, and
> contextual knowledge live in markdown bodies attached to entity
> files — not in encoded schemas or hardcoded skill procedures.
> Cross-domain portability is achieved by AI reading prose, not
> by abstracting over schema variants. Structured layers are
> reserved for interfaces, identity, persistence, and machine
> contracts; everything else is prose; AI is the runtime that
> fuses them at use-time.**

### Why this matters

Trying to capture domain richness (sub-entity required/optional
rules, process flow, conditional logic, expert reasoning) in
formal schemas leads to two failure modes:

1. **The SQL-DB trap**: schemas grow until they recreate
   relational-database complexity. Per the entity-elevation
   discipline this is *catastrophic for LLM-mediated AI offices*
   — brittle, slow to evolve, re-implements enterprise software's
   worst tendency.
2. **Prose squeezed into structured fields**: the existing strain
   visible in `extensions/universal/doctypes.yaml` and
   `references-manifest.yaml` — `description: >` and `notes: |`
   block scalars holding what is fundamentally prose
   (descriptions, expert reasoning, when-this-applies notes).
   Block scalars work mechanically but suppress the form prose
   wants to take: no headings, no structured lists, no links, no
   examples.

The corrective: **AI processing is not a bridging layer between
structured + freeform; it REPLACES the encoded-rules layer
entirely.** The model already in use elsewhere — memories
(frontmatter + markdown body, AI does the understanding) — is the
canonical pattern. There is no memory engine parsing rules; the
memory describes the thing in prose, AI applies it at runtime.

This is the explicit implementation of v0.13's gesture: *"closer
to knowledge graph + document store with stable references, not
Oracle."*

### The three-layer frontmatter contract

Every managed entity, every manifest entry, every doctype
declaration follows this shape:

| Layer | Lock-down | Enforced by |
|---|---|---|
| **Layer 1 — Universal frontmatter** (every entity) | STRICT (fail-loud) | MCP gate (Pydantic base) |
| **Layer 2 — Type frontmatter** (per-entity-type) | STRICT (fail-loud) | MCP gate (Pydantic subclass per type) |
| **Layer 3 — Per-deployment extension fields** | TBD per #9 | TBD per #9 |
| **Body conventions** (recommended sections per type) | RECOMMENDED (warn) | Audit skill + design-review skill (NOT gate) |
| **Body free prose** | UNCONSTRAINED | — |

**Layer 1 fields** (every entity): `id`, `label`, `type`, `scope`,
`scope_key`, `status`, `last_updated`, optional `description`,
optional `tags`. The `type:` field routes to the Layer-2 Pydantic
subclass at gate-read time.

**Layer 2 fields**: per-entity-type, locked. Doctypes have
`style_ref`, `master_file_pattern`, `paired_with`, `document_class`,
etc. References have `source_url`, `canonical_path`,
`fetch_method`, `last_fetched`, `checksum_sha256`, etc. Projects
have `bundesland`, `verfahren_type`, `lifecycle`, `phase`,
`departments_active`, etc. (today's ProjectState fields, relocated).

**Body conventions** (per entity type, documented at
`docs/conventions/entity-md-spec.md`, audit-enforced not
gate-enforced):

| Entity type | Conventional body sections |
|---|---|
| `doctype` | When this doctype applies / Section conventions / Pairing semantics / Domain-specific deviations |
| `reference` | Why this matters / Key sections for our work / Recent amendments / Common citations / Cross-refs |
| `project` | Context / History (append-only) / Open questions / Decisions |
| `client` | Communication preferences / Billing conventions / Project history summary / Watch-outs |
| `process` | Phase sequence / Required doctypes per phase / Mandatory triggers / Exceptions and shortcuts |
| `actor` | Role + responsibilities / Working preferences / Capabilities + limits |

Recommended-not-required avoids the rigidity that hard-enforced
templates produce (entities that don't fit the template get filler
text). Same pattern memories already use — feedback memories
conventionally have **Why:** + **How to apply:** lines (documented
in CLAUDE.md), but no validator enforces it; review/practice does.

### Where conditional rules live

Resolved: **rules about *when* something applies belong with the
*process*, not with the entity itself.** The doctype md describes
what the doctype IS; the **process md** (per verfahren type)
describes the flow + which doctypes the flow produces; the
project entity's body is per-instance narrative, not rules.

Worked example: `extensions/department/planning/processes/
beschleunigtes.md` (§13a) declares its phase sequence WITHOUT
Umweltbericht. `regelverfahren.md` declares Umweltbericht as
required. Project state references `verfahren_type:
beschleunigtes`; orchestrator loads the matching process md to
know what's expected. This is **process-as-md, not
state-machine-as-data**.

### MCP gate generalization (lands in #9)

Today: per-entity tools (`read_project_state`, `write_project_state`).

Tomorrow (per #9 implementation): generic `read_entity(path)` /
`write_entity(path, file)` with `type:`-field dispatch to the
appropriate Layer-2 Pydantic subclass. Body preserved as-is across
read/write cycles (same shape state.md uses today). Replaces
per-entity-tool sprawl.

### Connections to other disciplines

| Discipline | Connection |
|---|---|
| **Entity-elevation** | Hybrid-shape applies AFTER the 3-test verdict. Entity-elevation says "don't over-elevate"; hybrid-shape says "for things that DO elevate, here's their shape." |
| **Pattern-vs-instance** | Hybrid-shape IS how cross-domain portability is achieved. Same shape (frontmatter + body), different prose per domain. |
| **Glue-not-replacement** | Adapter-mode entities use the same hybrid-shape contract; per-deployment markdown body is the natural home for "how does THIS office use the external system." |
| **Strict-validation (meta-rule 4)** | Layer 1 + Layer 2 frontmatter respect strict-validation: required fields fail-loud, no silent defaults. Body is unconstrained by design — that's the principle. |
| **Source-of-truth (meta-rule 3)** | Hybrid-shape doesn't change source-of-truth placement; it changes **how** source-of-truth content is shaped (when content is semantic/process rather than identity/config). |

### What stays structured (counter-cases)

The principle does NOT push everything to markdown. Things that
remain rightly structured:

- **Office-config** (`~/.config/pbs-bureau/office.yaml`):
  deployment switches, paths, mode/adapter selection. Pure config.
- **AuditEvent / Pydantic schemas**: events are interface
  contracts between skills + tools. Structured by design.
- **Adapter Protocols**: Pydantic Protocols defining
  machine-readable contracts that adapter implementations satisfy.
- **plugin.json**: plugin manifest. Mechanical.
- **office-config.schema.yaml**: schema spec. Pure structural.

The boundary: **structured for interfaces, identity, persistence,
machine contracts; markdown for semantics, rules, domain knowledge,
process descriptions; AI as runtime fuses them.**

### AI-as-runtime conformance check (two-level: smoke + deep)

Architectural proposals get checked against this principle. Two
levels — fast default, deep escalation when concern surfaces.

#### Smoke test (30-60 seconds, applied per proposal)

Three yes/no questions. Goal: catch obvious violations cheaply.

**Q1. Does the proposal encode rules / semantics / conditional
logic in structured form (Pydantic, YAML frontmatter, config DSL)?**
- NO → green
- YES → follow-up: does the structured form serve a *concrete*
  machine consumer (gate startup, audit slice, persistence
  contract, machine-to-machine interface)?
  - YES → green (interface contract, legitimately structured)
  - NO or "not sure" → ⚠ escalate to deep test

**Q2. Is the same rule or fact represented in more than one place
(structured + prose, structured + code, prose + code)?**
- NO → green
- YES → ⚠ escalate (drift risk; source-of-truth violation)

**Q3. Would a senior domain expert need engineer help to change
this rule?**
- NO (they edit markdown, done) → green
- YES → ⚠ escalate (over-coupled to code)

**Verdict**: all three green → proceed. Any ⚠ → run deep test
before locking the design.

#### Deep test (5-10 minutes, applied when smoke escalates OR
stakes warrant)

Six checks in three tiers:

**Architectural — must pass (pattern-level conformance):**

1. **Lives in prose** — rule is in markdown body that AI reads
   at runtime, NOT encoded in structured frontmatter or config
   DSL (unless concrete machine consumer justifies it).
2. **Single source of truth** — rule is in exactly one place; not
   duplicated structured + prose, or prose + code.
3. **Cross-industry portable** — same architectural shape works
   for legal-practice / research-lab / brand-voice / etc. via
   prose-rewrite alone (no schema or code change for different
   domain).

**Operational — note + monitor (practical viability):**

4. **LLM-interpretable** — current-generation LLMs reliably apply
   the rule consistently across invocations; precise enough to
   avoid hallucination at edge cases.
5. **Body-size budget** — fits entity-md-spec §16 thresholds
   (≤1500 token bodies, ≤500 token sections, prune-able when
   stale).

**Disqualifier — any fail = redesign:**

6. **No SQL-DB-trap** — not building nested structured schemas to
   encode rule data when prose would carry it. If the proposal is
   even adjacent to this anti-pattern, redesign.

#### When each test fires

| Trigger | Action |
|---|---|
| Architectural proposal (Bundle decisions, new entity type, new mechanism) | Run smoke test |
| Smoke test all-green | Proceed |
| Smoke test any ⚠ | Run deep test |
| New architectural discipline being introduced | Run deep test directly (skip smoke) |
| Pattern-level decision with broad downstream consumers | Run deep test directly |
| Periodic during audit / design-review sweeps | Run deep test on representative sample |

#### Status

**Documented as manual mental checklist.** After 3-5 real
applications across upcoming Bundle work, evaluate for
formalization as **design-review target 15** (extending the
discipline-check pattern that targets 1-14 already cover for the
other 6 architectural disciplines — NOT a separate skill). Manual
phase first per design-review-target-13 "pattern emergence"
discipline: wait for the checklist to surface real drift in real
discussions before formalizing.

### Discipline check at audit + design-review time

- **Audit slice 21** (entity-md conformance): scans
  `extensions/**/*.md` entity files for Layer-1 + Layer-2
  frontmatter conformance + body recommended-section presence.
  Warns on missing sections; doesn't fail. Implementation bundled
  with #9.
- **Design-review target 12** (entity authoring conformance):
  when authoring or modifying an entity md, validates frontmatter
  against the appropriate Pydantic subclass + suggests missing
  recommended body sections. Coordinates with target 11
  (entity-elevation) so over-elevation gets caught alongside
  shape-misuse.
- **Decision-record convention**: any decision proposing a new
  managed entity type or new manifest type must include
  Layer-1 + Layer-2 frontmatter spec + body-spec sections.

### Connection to VISION

The principle is the architectural expression of VISION axis 1
(intertwining-AI-workflow). AI is not a feature of the system; it
is the runtime that fuses the layers. Without AI as runtime, the
markdown bodies are inert prose; with AI as runtime, they ARE the
rules + process + domain knowledge.

Memory drift toward oracle-mode framings shows up as architectural
drift toward over-structuring: when AI is treated as a passive
answerer (oracle), the architecture compensates by encoding rules
in schemas. When AI is treated as a workflow participant
(intertwining axis), the architecture relies on AI to read prose.
The hybrid-shape principle locks in the latter.

See `docs/decisions/ai-as-runtime-hybrid-shape.md` for the full
decision record (worked examples, downstream constraints, defers,
revisit triggers).

---

## Validation layering: deterministic primary, LLM secondary

> **For any check or enforcement point in the architecture, use
> deterministic validation (Pydantic, type checks, threshold
> comparisons, hash verification, token counts) where the question
> has a determinate answer. Reserve LLM validation for genuine
> judgment (is this prose imperative? is the cited reference
> accurate? does this match the convention shape?). The two layers
> compose: deterministic catches binary failures cheaply; LLM
> catches judgment failures expensively. Each plays to its
> strength.**

### Why this matters

Checks and enforcement points come up everywhere — gate writes,
audit slices, design-review targets, conformance tests, governance
gates. Without an explicit principle, two failure modes recur:

1. **Over-LLM-ifying**: using LLMs to check things that have a
   determinate answer (does this YAML parse, is this field
   required, does this token count exceed threshold). Slow,
   expensive, non-deterministic — and wrong tool: the answer is
   binary.
2. **Under-LLM-ifying**: trying to encode genuine judgment
   (precision of prose, accuracy of cross-reference, fit-to-shape)
   in deterministic checks. Either fails to catch real
   violations, or invents brittle pattern-matching that
   approximates LLM judgment poorly.

The principle catches both: deterministic for the deterministic;
LLM for the judgmental; both layers compose.

### Where this applies in the architecture

| Surface | Deterministic layer | LLM layer |
|---|---|---|
| **Gate enforcement** (read_entity / write_entity) | Pydantic strict validation, cross-ref existence check, role check | (none — pure structured contract) |
| **Authorization (role-gated writes)** | Actor.roles vs entity-type write requirements | Skill workflow surfaces approval UX |
| **Audit slice 14** (boundary adherence) | Path-pattern check, file-existence check | Body content judgment for ambiguous boundary cases |
| **Audit slice 16** (validation-gate coverage) | Pydantic `extra='forbid'` enumeration | (rarely needed — schema check is binary) |
| **Audit slice 21** (entity-md conformance) | Frontmatter Pydantic validation, token-count thresholds | Body section presence, prose precision, content quality |
| **AI-as-runtime conformance check** | Smoke test (3 binary questions) | Deep test (judgment-shaped checks 1-6) |
| **Convention application** | Pattern match, schema validation of result | Edge-case judgment, "is this convention applied correctly?" |
| **Identity sourcing** | Token validation, schema check on adapter response | Reference accuracy, content interpretation |
| **Cross-reference validation** | Existence of referenced entity (gate) | Accuracy of reference (does the cited section actually contain the rule?) |

### Pattern: cheapest-first ordering

When multiple validation layers exist, they run in cost order:

1. **Free** — type system / static analysis (compile time)
2. **Cheap** — Pydantic validation, threshold comparisons (gate write time)
3. **Medium** — git-state checks, cross-reference existence checks
4. **Expensive** — LLM judgment (audit slices, design-review targets)

A failure at any layer can short-circuit the rest. Run cheap
checks before invoking LLM judgment; reserve LLM for what
genuinely needs it.

### Connection to existing disciplines

- **Meta-rule 4 (strict-validation)** specifies the deterministic
  layer's discipline (fail-loud, no silent defaults).
  Validation-layering names what runs ON TOP of that layer for
  judgment-shaped checks.
- **AI-as-runtime hybrid-shape** specifies the boundary at runtime
  (structured for contracts, prose for semantics, AI fuses).
  Validation-layering specifies the same boundary at check time.
- **Defense-in-depth** (governance enforcement, decision 1 of
  `governance-and-identity-sourcing.md`) is one application of
  this principle — gate enforces deterministically, skill workflow
  adds LLM-orchestrated UX above.

### Discipline check at design time

When designing any new validation point or enforcement gate:

1. What's the deterministic layer? (Pydantic, threshold, hash —
   anything binary)
2. What's the LLM layer? (judgment, content-quality, semantic
   accuracy — anything requiring interpretation)
3. Do they compose correctly? (LLM doesn't run on what
   deterministic already caught; deterministic doesn't try to
   pattern-match what LLM should judge)
4. Is the cost-ordering right? (deterministic first, LLM after)

Skipping this analysis tends to produce wrong-tool-for-job choices
that surface as flaky audits or expensive simple checks.

---

## Evolution patterns: how data shapes change over time

Pattern recognition (not a new discipline — names the three
mechanisms already in use across the architecture). When data
shapes need to evolve, the right mechanism depends on **what
kind of data** is changing:

| Pattern | Used for | Evolution mechanism |
|---|---|---|
| **Structured + mutable** | `office-config.yaml`, `ProjectState` (post-#9 → ProjectEntity), entity Layer 1 + Layer 2 frontmatter, Pydantic schemas | Versioned migration framework (`office_config_migrations/` style); migration scripts run on load when `CURRENT_SCHEMA_VERSION` mismatches |
| **Structured + append-only** | `AuditEvent`, `decisions.md` entries, `snapshots/` artifact bytes | Additive backward-compat: new fields default to `None` for old records; readers handle missing fields gracefully; **NEVER rewrite historical records** (would erase audit truth) |
| **Prose + forward-only** | All entity body content, `conventions.md`, doctype/reference/process bodies, decision records | No migration. New rule applies forward; existing entities stay as-minted under the prior rule. Historical reconstruction via structured anchoring (e.g., `convention_applied: {git_sha}` on entity-mint AuditEvents) |

### Why three, not two

It would be tempting to say "structured = migrate, prose =
forward-only" and call it a day. The append-only structured case
breaks that simplification — AuditEvents are structured, but
**rewriting them is wrong**. Old events stay in their old shape;
new code reads them via additive backward-compat (optional
fields, defaults). The mechanism is structurally different from
office-config migration even though both are "structured."

Naming all three makes the design choice explicit per surface:
"is this surface mutable (migrate), append-only (backward-compat
at read), or prose (forward-only)?" Different answer = different
mechanism = different code paths.

### Discipline check

When designing a new persistence point or evolving an existing
schema:

1. **Mutable or append-only?** Mutable supports rewrites;
   append-only doesn't. AuditEvent is the canonical append-only
   example.
2. **If mutable: structured or prose?** Structured uses migration
   framework; prose uses forward-only with historical anchoring.
3. **What anchors history?** For mutable structures, version
   number + migration. For append-only, the original write itself.
   For prose, the structured anchor field on the related event
   (e.g., `convention_applied: {file, section, git_sha}`).

Skipping this analysis tends to produce surfaces that try to
migrate things that shouldn't be migrated (overwriting historical
audit events) or fail to migrate things that need it (bumping a
schema without a migration script).

---

## Informed defaults: ship best-shape, not empty

> **When providing architecture, templates, or scaffolding to
> deployments, ship with informed defaults derived from the
> pioneer instance — not empty canvases. Bureaus inherit working
> starting points; they refine from a base, not bootstrap from
> scratch. Defaults reduce the violation rate, accelerate
> time-to-useful, and propagate accumulated lessons from the
> pioneer instance forward.**

### Two forms of informed default (added v0.24 retroactive review)

Informed defaults take TWO forms; pick the form per the choice's
variance across deployments:

| Form | When to use | Example |
|---|---|---|
| **(a) Pre-chosen template** | Low-variance choice — the right answer is similar across deployments; pioneer instance's shape generalizes | Skill body conventions; doctype-md scaffolds; entity-md spec body section catalog; failure-mode-catalog seed entries; reference-corpus seed |
| **(b) Guided question with concrete options** | High-variance choice — the right answer differs sharply per deployment; pre-choosing locks the wrong shape for most | "Does this office use an external PM tool? — Asana / Jira / Linear / none / custom"; "Auth provider: Google Workspace / Coolify SSO / OAuth / other"; "Embeddings model: bge-m3 / OpenAI / cohere / custom" |

Both forms deliver the principle's spirit — bureaus get concrete
starting points, never an empty canvas. The pre-chosen-vs-guided
distinction is about whether the variance across deployments is
low enough to commit to a default OR high enough that a question
is the better default-shape.

The skill-expert-agent decision record's PM-default decision (no
pre-pick; setup-office prompts at scaffold) is form (b). The
research-references corpus seed is form (a).

### Why this matters

Empty-canvas defaults force every bureau to discover good shape
through trial-and-error. The pioneer instance has already done
that work — failing to propagate it forward is a wasted asset.

Two failure modes the principle guards against:

1. **Empty-start drift**: bureau populates conventions from
   scratch, doesn't know what good shape looks like, ends up with
   inconsistent or under-shaped content. AI applies inconsistently.
2. **Late-discovered defaults**: bureau finds out months in that
   "we should have had X from the start" — and now has to migrate
   accumulated content into the better shape. Cost asymmetry:
   shipping the right default is cheap; migrating a populated
   deployment is expensive.

The principle catches both: ship the lessons we've already
learned; bureaus refine from a working base.

### Where this applies in the architecture

| Surface | Default shipped |
|---|---|
| `research-references` corpus seed | BauGB / BNatSchG / BauNVO / etc. (jurisdiction-relevant references) — bureaus inherit; can prune or extend |
| `design-review` skill | Pre-seeded `failure-mode-catalog.md` with literature-derived + PBS-experienced failure patterns |
| Skill bundles | `<example>` blocks per skill (per Anthropic plugin pattern) showing intended invocation shape |
| `extensions/office/conventions/` (post-#11/#15) | Pre-populated convention templates (actor-id, archive policy, naming, notification, audit) |
| `extensions/department/<dept>/processes/` (post-#9) | Pre-populated process md files for common verfahren (regelverfahren, beschleunigtes for planning) |
| `extensions/universal/doctypes/` (post-#9 migration) | Common doctype shapes (B-Plan Begründung, Festsetzungen, Stellungnahme, etc.) |
| Audit slices | Each ships with known violation patterns to scan for, not just empty rule-set |
| `office-config.schema.yaml` | Defaults for non-required fields where pioneer-instance experience suggests the right value |
| `entity-md-spec.md` body section catalog | Conventional sections per entity type (the table at §6 of entity-md-spec) — bureaus inherit |

### Pattern-vs-instance constraint (critical)

**Defaults must be at pattern level, not instance content.**

Wrong: shipping PBS-Schulz's specific Begründung content as the
default for legal practices. Mismatched abstraction; legal-practice
prose isn't planning-prose.

Right: shipping the doctype md file *shape* (frontmatter + body
sections + conventions) with example PBS content; legal-practice
adopts the shape, replaces the content with their own.

Right: shipping the convention md file *form* (imperative rule +
examples + edge cases) with PBS-derived example rules;
legal-practice keeps the form, writes their own rules.

The discipline: **defaults are shapes you can adapt; defaults are
not instance content you inherit verbatim.**

### Connection to existing disciplines

- **Pattern-vs-instance** is the constraint that scopes what's
  default-able. Pattern-level shapes ship as defaults;
  instance-level content does not.
- **Pioneer-instance commitment** (per VISION) provides the
  source: defaults are derived from real PBS experience, then
  abstracted to pattern level for shipping.
- **AI-as-runtime hybrid-shape** is what makes informed defaults
  effective — defaults SHIP as prose templates that AI applies +
  bureaus refine; not as code that requires engineer modification.

### Discipline check at design time

When designing any template, scaffold, or initial-state ship:

1. What's the empty-canvas alternative? (What would shipping
   without this default require the bureau to do?)
2. What's the pioneer-derived default? (What does PBS-Schulz
   experience suggest is the right starting shape?)
3. Is the default at pattern level? (Or is PBS-instance content
   leaking into something other domains should write themselves?)
4. Is the default override-able? (Can a bureau replace it
   cleanly, or does the framework assume the default forever?)

Skipping this analysis tends to produce either over-empty
deployments (everything must be populated from scratch) or
over-opinionated defaults (PBS-specific content baked in where
it shouldn't be).

---

# Meta-rules

The architecture rests on **four meta-rules**. Plus one named
convention (scope-orthogonality) that applies *within* layered
content. New content goes through the relevant meta-rule before
placement.

## Meta-rule 1: app vs office (deployment portability)

The repository is **a generic German planning-bureau workflow app**
that any Planungsbüro can deploy. It is not a PBS-specific instance.
Per-deployment configuration — paths, identity, actors, styling,
state-law extensions — lives **outside the repo** in an
`office-config.yaml` resolved via:

1. `$PBS_OFFICE_CONFIG` (env var, takes precedence)
2. `${XDG_CONFIG_HOME}/pbs-bureau/office.yaml`
3. `~/.config/pbs-bureau/office.yaml`

Schema: `docs/office-config.schema.yaml`. Generated interactively by
the `setup-office` skill on first run.

**Hard rules for app code (skills, backend, hooks, memory):**

- Never hardcode hidrive/projects/state paths. Read them from
  `roots.*` in the loaded office-config.
- Never hardcode office identity (name, address, signature, phone,
  email). Read them from `office.*` (post-v3 merge of identity into
  office).
- Never hardcode actor names. Read `actors[]` from config (kind=internal
  for practices, kind=external for partners).
- Never hardcode client/project names. Use neutral examples in docs
  (`YY-NN <Client> - <Location>`); refer to live projects only via
  paths the user provides at runtime.
- State-specific and domain-specific references are discovered by
  walking `<repo>/extensions/{universal,domain/<X>,state/<X>}/`
  filtered by the office's `scope.{domains,states}` (loader walks
  the union; manifests are NOT enumerated in office-config).
  Bundesland is a per-PROJECT property (`state.md.bundesland`), not
  an office property.
- LaTeX styling lives in the office's `office-style.sty`, NOT in
  app skeletons or classes.
- Office identity macros (`\OfficeName`, `\OfficeAddressLines`,
  `\OfficeSigner`) are auto-generated by the backend from `office.*`
  before each compile, NOT hand-written.

### Mechanism: pluggable integration adapters

Where the app interfaces with external systems whose mechanism
varies per deployment (email service, calendar, scanner, phone,
accounting, DMS, GIS, etc.), the implementation lives behind a
small **protocol + adapter pattern**: a Python `Protocol` defines
the contract; each adapter (`thunderbird-maildir`, `imap`, `caldav`,
etc.) implements it; office-config selects which adapter is active
per class.

Same architectural lesson as paths/identity/actors/scope: no
hardcoded mechanism. The adapter boundary is in place from day one;
concrete adapters land per demand. Adapters live at
`backend/mcp-server/src/pbs_mcp/integrations/<class>/<adapter>.py`,
each exporting an `Adapter(config: dict)` class implementing the
protocol at `<class>/protocol.py`. `load_adapter(class_name)`
resolves via `cfg.find_integration(class_name)` (v3 free-form
list).

The class set is open — any string is valid as long as a matching
subpackage exists. (Per design-review: integration adapters are
*backend-internal organizing pattern*, not a top-level meta-rule
peer; they're a consequence of app-vs-office deployment portability.)

**Generalization to department-managed entities (v0.12 per session-9
followup)**: the same Pydantic Protocol + concrete adapter pattern
also serves as the **adapter delivery mode for department-managed
entities** (per `docs/decisions/office-vs-department.md`). Two
delivery modes per entity: **native** (PBS owns the Pydantic schema
+ MCP CRUD tools — used when no external alternative exists, e.g.,
planning's Project entity for B-Plan workflows; brand-voice's Asset
entity), or **adapter-delegated** (external system owns system-of-
record — used for departments where mature tools exist, e.g.,
Invoicing's Invoice → Lexware/FastBill/sevDesk; PM's Timesheet →
Harvest/MOCO; HR's Employee → BambooHR/Personio). Mixed-mode is
required and supported per-entity within a single department. The
adapter implementation pattern is identical to auxiliary integrations
above; the **consumer set expands** from email/calendar/scanner to
primary department system-of-record. Department-managed-entity
adapters live at `extensions/department/<dept>/adapters/<entity>/`
(per the office-vs-department decision record schema additions).
Office-config selects per-entity mode + adapter via the
`departments.<name>.entities.<entity>.{mode, adapter, config}`
section.

**Schema versioning + migrations.** Adding fields to office-config
schema requires bumping `CURRENT_SCHEMA_VERSION` in
`backend/.../office_config.py` and adding a migration at
`backend/.../office_config_migrations/v<N>_to_v<N+1>.py`. The
dispatcher applies migrations sequentially in-memory on every load.

## Meta-rule 2: memory vs RAG (citation freshness)

A hard line: **what lives in memory** vs **what lives in the RAG
corpus**. The split protects against legal-citation rot.

**Memory** (loaded into context every session) holds:
- Workflow logic — phase order, phase→state mapping, doctype structure.
- Conventions — German number formatting, quotation conventions,
  hyphenation rules, korrektur-rules.
- Reference content (project-structure.md, per-project-memory
  format docs).
- Saved bausteine.
- Universal reasoning patterns that don't depend on current law text.

(Note: doctype + reference registries are NOT memory — they're
layered manifests in `extensions/`. Memory holds prose conventions
and saved instance records.)

**RAG** (`<roots.references>/`, retrieved on demand via
`search_corpus` / `read_corpus_file`) holds:
- Verbatim legal text (BauGB §X, BNatSchG §Y, etc.).
- Verbatim Verfahrensvermerk wording.
- Court ruling text.
- Leitfaden content from publishing bodies (KNE, LUNG, etc.).
- Anything that can be amended at the source.

**§-references as labels are allowed in memory** ("Phase 5a —
§3 Abs.2 BauGB") for navigation. Verbatim legal text and paraphrased
law-text are NOT — those route through RAG.

**Source-grounding rule.** Any legal citation in produced output
(drafts, reviews, mails) must be backed by a tool result — even if
the same §-number appears in memory. Memory's role is naming and
navigation, never authoring. The §-label "§3 Abs.2 BauGB" appearing
in memory does NOT satisfy the citation-evidence requirement when
drafting.

## Meta-rule 3: source-of-truth & invalidation

Every entity declares its invalidation contract: how the system
detects that this thing is stale, superseded, or wrong, and what
needs to happen when it is.

**Per entity type** (see "The five entity types" below for full
list):

| Entity | Invalidation contract |
|---|---|
| Skill Bundle | semver `version:` field; bump on behavior change. Body changes invalidate skill behavior on `/reload-plugins`. |
| Memory (prose) | `references_used: []` frontmatter declares dependent law refs. `research-references` flags affected docs in `memory/product-backlog.md` when a referenced law is updated. |
| Memory (records) | `status: active|flagged|archived|superseded`, `last_validated`, `review_due`, `references[].verified_against_version`. `validate-bausteine` sweeps for stale records. |
| Memory (audit-log) | Append-only `<project>/_ai/audit-trail.jsonl` per docs/decisions/audit-trail-v2.md (single-write supersedes v1's dual-write). Each `AuditEvent` carries `id`, `timestamp`, `kind`, `actor`, `actor_kind` (human/skill/external_agent per a2a-and-gemini-pattern-emulation.md), `actor_card?`, `origin_agent_card?`, `sources[]`. Events never invalidate (immutable history); `causes[]` chain captures supersession. `query_audit_trail` is the canonical query layer; `render_audit_trail` produces prose views from queries. Skills call `record_audit_event` (or `record_decision` for legal-defense provenance via `decisions.md` mirror — gate-mediated). Per the strict-validation discipline, `actor_kind` is required; `external_agent` events MUST name `origin_agent_card`. |
| Backend | Python imports + Pydantic schemas; restart MCP server after changes. No declarative invalidation hook. |
| Configuration | `schema_version` + migration framework. Manifests carry `last_updated` + per-entry `last_fetched` + `checksum_sha256`; `research-references` re-fetches on schema/source change. |
| External data | Per-project `_ai/state.md.lifecycle` declares phase + status (today single-valued — per-department `phases: dict` + `lifecycle: dict` deferred to #9 per `office-vs-department.md` D1+D2). `_ai/state.md.departments_active: list[str]` (added v0.11 per #12) declares which departments have engaged with this project; gate-mediated update via `record_audit_event` (logic deferred to #6). `roots.references_root` corpus carries `changelog.md`. |

**Cross-cutting concern handler.** Contract reading is layered
across two skills:

- `research-references` is the *trigger*: after fetching an
  updated reference, it scans both bausteine (`references[]`) and
  memory docs (`references_used[]`) for matches. Bausteine
  matching → flagged. Memory docs matching → logged to
  `memory/product-backlog.md` with affected paths.
- `validate-bausteine` is the *comparator*: it reads the
  `references[].verified_against_version` field on flagged
  bausteine and compares it against the current
  `current_amendment_form` from the manifest, surfacing drift
  for the user.

The split is intentional — research-references detects *which*
entities cite updated laws; validate-bausteine determines
*whether each entity's cited form is still current*. Both flows
are required to close the invalidation loop; neither alone
suffices.

**Frontmatter declares invalidation hooks.** Cross-cutting docs
that name laws declare them in frontmatter:

```yaml
---
references_used:
  - {law: BauGB, paragraph: §3 Abs.2}
  - {ruling: BVerwG-9-A-22-11}
  - {leitfaden: KNE-Anlagengestaltung}
---
```

This rule was previously implicit (scattered across "What changes
invalidate what" prose + per-entity-type schemas). Promoting to a
meta-rule forces every new entity type to answer "how does the
system know you're stale?" before shipping.

## Meta-rule 4: execution determinism (where deterministic work lives)

About *where* operations execute, not where content lives.

**Core principle.** Operations with a single deterministic correct
execution — validation, schema enforcement, transactional writes,
side-effect coupling, cross-reference consistency, computed
properties (hashes, indexes), migrations — live in **MCP gates**
(backend code, exposed as MCP tools). Skills are for judgment,
conversation, and surfacing decisions; they orchestrate MCP tool
calls, never reimplement what those tools do.

(Renamed from "execution locality" in v0.4. Locality suggests
*physical location*; the actual axis is determinism — single-right-
answer vs. judgment.)

**The persistence-layer boundary.** Cleanest line: *anything that
touches durable state with a **typed contract** (Pydantic model +
loader + cross-reference invariants) goes through MCP; session-
ephemeral state and loose unstructured files stay skill-direct.*
Watch list, in-conversation findings, surfacings queued during a
turn — all skill (ephemeral). Writes to office-config, baustein
YAML, manifests, schema-bearing state files — all MCP (the loader
owns the shape; bypassing MCP bypasses forward-migration and
invariants).

**The line is contract enforcement, not file type.** A file is in
scope of MCP if a Pydantic model + loader owns its shape. If the
file is parsed only by the LLM at read time, direct
`Read`/`Write` is fine. HANDOFF.md, prose memory `.md` files
under `memory/universal/`, top-level docs, READMEs — all
skill-direct, no schema, no migration, no transactional risk. A
markdown file *can* become schema-bearing later (e.g., `state.md`
once typed parsing lands) — at which point its access path
moves to MCP. Audit slice 14 reads each access via this test,
not by extension.

**Deterministic vs interpretive verdicts.** Validation with a
single right answer (frontmatter shape, ISO state code, schema
conformance, citation drift on exact-string match) is deterministic
→ MCP. Validation requiring interpretation (does this baustein
content actually concern §44 BNatSchG? does this language read as
collegiate or formal?) is interpretive → skill, surfaces verdict
to user. When unclear, ask: would two implementations agree byte-
for-byte on the verdict? If yes, MCP. If no, skill.

**Enumeration-vs-selection corollary.** "List the candidates" is
deterministic, scope-aware → MCP (`list_bausteine`,
`list_reference_manifests`). "Pick the right one for this drafting
context" is judgment → skill.

**Reuse direction.** When two consumers share logic, where does the
shared code live? The rule has a positive form, not just the
negative "skills compose, never reimplement":

- **Shared deterministic logic → MCP tool.** Two skills that need
  to dedupe, validate frontmatter, or look up a manifest entry call
  the *same* MCP tool. Don't reimplement; don't copy-paste prompt
  text describing the deterministic procedure into each consumer.
- **Shared interpretive logic → Skill Bundle reference.** Two skills
  that need to reason about korrektur-rules, layered review
  mechanics, or doctype conventions load the *same*
  `references/<topic>.md` file. The Skill Bundle convention exists
  for exactly this — judgment scaffolding shared across skill-side
  consumers without each skill re-stating it.

The negative form ("don't reimplement") tells you what's wrong; the
reuse direction tells you where the right home is. Audit slice 14
flags both directions: re-implemented determinism in skills *and*
re-implemented interpretive scaffolding when a Skill Bundle
reference would have served.

**Skill frontmatter declares MCP-tool dependencies.** Every skill's
`SKILL.md` frontmatter declares which MCP tools it relies on
(`mcp_tools_required[]`, `mcp_tools_optional[]`,
`fallback_when_mcp_absent`). See `docs/plugin-conventions.md` §1
for the full contract. Tools are referenced by snake_case name —
matches the Python function name in `pbs_core/`. Frontmatter is
machine-checkable; future audit slices verify every declared tool
exists in the MCP server's registry.

**Static path-based access control belongs in `settings.json`,
not in code.** Where a path should never be written outside a
specific MCP tool's context, use a permission deny rule. Cheaper
than scaffolding code paths that re-enforce what the harness can
already block.

**Strict-validation discipline.** Every MCP gate that owns a
typed contract validates via Pydantic. Required fields are
strictly required (no `Optional` for required, no silent default
to `None`). On contract violation, raise loud with descriptive
errors naming the offending field; never return partial data,
never coerce a missing required field to a placeholder. Defaults
are reserved for fields where missing semantically means
"not-yet-known" (`None`) — not for required fields where missing
would mean "broken data."

This discipline is what makes the gate a gate. A Pydantic model
that liberally uses `Optional` to "be flexible" silently accepts
malformed data and breaks the contract-enforcement guarantee.

Audit slice 16 (validation-gate coverage) checks adherence: it
walks every MCP tool's input/output models + every entity
Pydantic model and flags `Optional` on fields the rule says are
required, silent defaults that mask missing data, and exception
swallowing that converts contract violations to soft failures.

**Fail-closed for contract-bearing reads.** When MCP is
unreachable, skills MUST surface to the user and stop, never
bypass the contract via direct filesystem `Read`. The gate is the
only correctness path; bypass produces silent invalid output that
violates the strict-validation principle just established.

The rule applies symmetrically to writes (already covered by
"persistence-layer boundary" above) and reads. A skill that
"falls back to direct Read of state.md when MCP is down" gets:

- pre-migration frontmatter the loader would have updated
- partial-invalid state the Pydantic model would have rejected
- cross-reference-broken state (lifecycle ↔ phase mismatch) the
  invariant check would have caught

The right MCP-unreachable behavior for a contract-bearing read is
a clean failure surfacing: "MCP unreachable; cannot operate on
\<X\>. Restart backend." Contract-free prose (HANDOFF.md, prose
memory, decisions.md, file-map.md, READMEs, top-level docs)
remains skill-direct — no contract exists to bypass.

The test for "contract-bearing": Pydantic model owns its shape, OR
`schema_version` with migrations applied on read, OR cross-
reference invariants, OR a loader function in `pbs_mcp/`
constructs a typed object, OR `last_updated` / `last_fetched` /
`checksum_sha256` declares an invalidation contract. If any
yes → fail closed. Otherwise → direct Read fine.

Per-skill: `fallback_when_mcp_absent` strings declare what is
still possible; for contract-bearing dependencies the answer is
"nothing — surface and stop." Audit slice 14 scans these strings
and flags any "fall back to filesystem Read of \<contract-bearing
file\>" pattern as a declared future violation.

See `docs/decisions/mcp-fallback-policy.md` for the full
rationale and rollout.

### Backend organization (consequence of meta-rule 4)

Backend code splits conceptually into two layers:

- **`pbs_core/`** (planned package; currently part of `pbs_mcp/`):
  plain Python — config schema, validation, layered manifest API,
  integration adapters, RAG pipeline, project lifecycle, audit
  trail. Takes Python args, returns Python objects, raises Python
  exceptions. Knows nothing about MCP.
- **`pbs_mcp/tools/`**: thin MCP tool definitions that wrap
  `pbs_core` functions — parse JSON args, call core, format
  response, translate exceptions to MCP errors. Contains no
  business logic.

This is the consumer-side of the meta-rule: meta-rule 4 says
"deterministic logic in MCP gates"; this organization adds "MCP
gates are themselves thin wrappers around plain Python core."

This discipline applies starting now even though the two layers
live in the same module today. When the first non-MCP frontend
emerges (web UI is the load-bearing trigger per ROADMAP), the
physical split — promoting `pbs_core` to its own package — is a
small refactor, not a re-architecture.

**Don't do the physical split until a real second consumer exists.**
The conceptual discipline gives most of the maintainability +
testability benefit at near-zero cost.

---

# Layering convention: scope orthogonality (universal × domain × state × department)

(Demoted from meta-rule in v0.5 per design-review. It's a
*layering pattern* applied to specific entity types, not a placement
axis itself — it doesn't answer "where does this go?", it answers
"once you know it's the kind of thing that layers, which subdirectory?". Extended in v0.11 with the department axis per #12.)

Reference content, doctype registries, skeletons, bausteine, and
department-specific configuration all decompose along **four**
orthogonal axes:

- **universal** — applies to every German Planungsbüro deploying
  this app, regardless of planning domain or Bundesland.
- **domain** — applies to bureaus working in a specific planning
  domain (e.g. PV-FFA, Wind, Naturschutz, Innenentwicklung).
  Multiple domains can be active simultaneously.
- **state** — applies to bureaus working in a specific Bundesland
  (BB, BW, BY, ..., TH). Multiple states can be active simultaneously.
- **department** *(added v0.11 per #12)* — applies to a specific
  capability area within an office (planning, project-management,
  invoicing, brand-voice, legal-work, etc.). Opt-in per entry —
  most existing entries stay in the original 3 axes; department-
  specific entries declare the 4th. Multiple departments can be
  active simultaneously per office.

A bureau's effective content is its `(domains × states × departments)`
selection (set in `office-config.yaml > scope.{domains,states}` and
`departments.<name>`). Layered loaders merge the universal layer
with each selected domain/state/department layer at runtime.

**Where this applies:**

- **References manifests**: `extensions/{universal,domain/<X>,state/<X>,department/<X>}/references-manifest.yaml`
- **Doctype manifests**: `extensions/{universal,domain/<X>,state/<X>,department/<X>}/doctypes.yaml`
- **Skeletons**: `plugin/templates/skeletons/{universal,domain/<X>}/<doctype>/`
- **Bausteine**: `memory/bausteine/{universal,domain/<X>,state/<X>,department/<X>}/<name>.md`
- **Office-style overlays**: `plugin/templates/office-style/office-style.{default,<DOMAIN>}.sty`
- **Department config** *(added v0.11)*: `extensions/department/<X>/department.yaml` (event_subscriptions + per-department metadata; spec'd in `office-vs-department.md`, implementation deferred to #11)

**Hard rules for placing layered content:**

- Decide the scope BEFORE the path. Ask: does this apply to every
  German bureau (universal), every bureau in this domain (domain),
  every bureau in this state (state), or only this department
  (department)?
- A baustein has exactly one scope. If a candidate baustein applies
  to multiple, either promote it up the layer (`universal` if truly
  cross-domain-cross-department) or split it.
- An entry's home is independent of who created it.
- Most universal/domain/state content is department-agnostic — it
  applies across departments. Only declare a `department/<X>` cell
  when content is genuinely department-specific (invoicing-billing-
  templates, PM-deadline-conventions).

**Out of scope (entity types this convention doesn't apply to):**
Skill Bundles, Backend, External Data — none of these layer along
the scope axes. Configuration partially applies (its manifest tree
under `extensions/` does; the office-config file itself doesn't).
Skills declare `department:` in frontmatter (per #12) but skill
*bundles* themselves don't layer along the 4 axes — they're
discovered by their bundle path, not via layered loader merge.

**The `author-manifest` skill** scaffolds new domain, state, or
department manifests for scopes that don't yet have content.

---

# The five entity types

| Type | Where | Invalidation | What it does |
|---|---|---|---|
| **Skill Bundle** | `plugin/skills/<name>/SKILL.md` + `references/*.md` | semver `version:`; reload via `/reload-plugins` | Behavioral protocol auto-loaded on trigger match. SKILL.md is the entry point; references hold detailed format specs / checklists / procedures. (Combines former Type A skill + Type B skill reference — they're chapters of one bundle, not peers.) |
| **Memory** | `memory/universal/...` (prose), `memory/bausteine/{universal,domain/<X>,state/<X>}/...` + `<project>/_ai/...` (records) | references_used/status/review_due/verified_against_version | Two sub-kinds: **authored prose** (universal domain knowledge consumed across skills — style-spec, korrektur-rules, verfahren docs) + **generated records** (bausteine, feedback entries, project state.md). Mutability differs sharply between them; both share Memory's invalidation hooks. |
| **Backend** | `backend/mcp-server/...` (code + protocols + adapters + technical docs) | none declarative; restart MCP server after changes | Python implementation. Splits conceptually into `pbs_core/` (plain Python) + `pbs_mcp/tools/` (MCP wrappers) per meta-rule 4. Integration adapters live as a sub-organization here (`pbs_mcp/integrations/<class>/<adapter>.py`); they're an internal pattern, not a peer entity type. |
| **Configuration** | `office-config.yaml` (single per deployment, outside repo) + `extensions/{universal,domain/<X>,state/<X>}/{references,doctypes}-manifest.yaml` (scope-keyed, in repo) | `schema_version` + migration framework | Deployment-controlled YAML. Two sub-kinds — single-file (office-config) and scope-keyed (layered manifests) — distinguished by where they live + how they're discovered, but both are configuration-shaped (versioned, schema-validated, deployment-scoped). |
| **External data** | Resolved via `roots.*` (projects, references, state) + per-project `<project>/_ai/...` | Varies; project state via `_ai/state.md.lifecycle`; references corpus via `<roots.references>/changelog.md` | Real user data: legal texts, project artifacts, runtime state, correspondence. NOT versioned with the app. |

**Why 5 not 9** (per design-review session 5):
- **Skill Bundle** = former A (Skill) + B (Skill reference). A skill reference has no meaning outside its parent skill — it's a chapter of the bundle, not a peer. Decision rules collapse from "is this a skill or a skill-reference?" to "is it part of a skill bundle?"
- **Configuration** = former G (Office config) + H (Layered manifests). Both are deployment-controlled YAML; the only difference is single-file vs scope-keyed, which is *where* they live, not *what kind of thing* they are.
- **Backend** = former E (Backend code) + I (Integration adapters). Adapters are a backend-internal organizing pattern (same language, same package, same restart semantics) — not a peer entity type.
- **Drop A-I letters**: false ordinality + false peerage. Names ("Skill Bundle", "Memory", "Backend") are self-documenting.

(For migration: any prior reference to "Type A" / "Type B" / "Type C" / etc. should be re-read as the corresponding new name. Most references to the old letters can be dropped without replacement; the new names speak for themselves in context.)

---

# The three decision rules

For any new piece of content, walk these in order. The first to
classify wins.

## Rule 1 — Is this consumed by Claude at runtime as behavior?

If it tells the AI HOW to act, what to load, how to converse, when
to delegate — it's part of a Skill Bundle.

→ **Skill Bundle**: `plugin/skills/<name>/SKILL.md` (entry point,
with frontmatter) + optional `references/*.md` (detailed protocols,
format specs, checklists — no frontmatter).

If multiple skills consume the same content (e.g. korrektur-rules,
style-spec, verfahren-phasen), it's *cross-cutting authored prose*
— route to Rule 3 (Memory: prose).

## Rule 2 — Is this Python code?

If it's `.py` — backend code, MCP tool wrappers, integration
adapters, technical schema docs.

→ **Backend**: `backend/mcp-server/...`. Adapters are a sub-pattern
(same package), not a separate type.

## Rule 3 — Then by mutability:

**3a. Authored prose** (humans/AI write; cross-cutting knowledge):

- Universal domain knowledge → `memory/universal/...` →
  **Memory (prose)**.
- Layered (universal × domain × state) reference manifests +
  doctype registries → `extensions/<scope>/<key>/*.yaml` →
  **Configuration (scope-keyed manifest)**.
- Per-deployment values (paths, identity, actors, scope) →
  `office-config.yaml` (outside repo) → **Configuration (office-config)**.

**3b. Generated records** (tools write; instance state):

- Bausteine, feedback entries, project state — `memory/bausteine/<scope>/<key>/<name>.md` or `<project>/_ai/...` → **Memory (record)**.

**3c. External data** (user files, not versioned with app):

- Legal text corpus, client project artifacts, runtime state →
  `<roots.*>` paths, per-project `_ai/...` → **External data**.

## How the rules compose

Rule 1 catches everything Claude reads as instruction. Rule 2
catches everything written in Python. Rule 3 splits the rest by
who-writes-it (authored vs generated vs external).

The 4-mutability breakdown in Rule 3 is *one rule with sub-cases*,
not 4 separate rules. The decision is "what kind of content is
this?" (prose / record / config / external), not a sequential walk.

(This collapses the v0.4 6-rule walk to 3 rules + sub-cases. The
former Rules 4 and 5 — "HOW vs WHAT" — were a false axis: every
cross-cutting memory doc has *both* HOW and WHAT properties; the
real distinction is consumer breadth, which Rule 1's "multiple
skills" branch handles directly.)

---

# Worked examples

| Content | Reasoning | Type |
|---|---|---|
| `style-spec.md` (universal B-Plan LaTeX domain) | Rule 1: cross-cutting (multiple skills); Rule 3a: authored universal prose. | Memory (prose) |
| `korrektur-rules.md` (German writing conventions) | Same — cross-cutting prose; Rule 3a. | Memory (prose) |
| `bauleitplanung-phasen.md` (BauGB process) | Rule 3a: authored universal prose, cross-cutting. | Memory (prose) |
| `extensions/universal/doctypes.yaml` | Rule 3a: scope-keyed manifest. | Configuration (manifest) |
| `extensions/domain/Naturschutz/doctypes.yaml` | Same; scope=domain/Naturschutz. | Configuration (manifest) |
| `office-config.yaml` (outside repo) | Rule 3a: per-deployment configuration. | Configuration (office-config) |
| `baustein-format.md` (how to write a baustein) | Rule 1: instruction; consumed by ONE skill (save-baustein). Part of skill bundle. | Skill Bundle (reference) |
| `state-format.md` | Rule 1: instruction; single-skill (orchestrator). | Skill Bundle (reference) |
| `manifest-schema.md` | Rule 1: single-skill (research-references). | Skill Bundle (reference) |
| Doctype checklists | Rule 1: single-skill (validate-checklist). | Skill Bundle (reference) |
| `vector-metadata-schema.md` | Rule 2: backend technical schema. | Backend |
| A future saved baustein | Rule 3b: generated record. Apply layering convention to pick scope. | Memory (record) |
| A future feedback entry | Rule 3b: generated record. | Memory (record) |
| A future `<project>/_ai/state.md` | Rule 3b: generated record. | Memory (record) |
| `orchestrator` SKILL.md | Rule 1: skill bundle entry point. | Skill Bundle |
| `save-baustein` SKILL.md declares `mcp_tools_required: [save_baustein, list_bausteine]` | Meta-rule 4: skill is the orchestrator; MCP tool is the validator. Frontmatter makes the dependency explicit. | Skill Bundle |
| Email integration adapter Python | Rule 2: backend Python. (Sub-pattern: integration adapter.) | Backend |
| Court ruling text from BVerwG website | External data; lives in RAG corpus at `<roots.references>/urteile/...`. | External data |
| `references_used: []` frontmatter | Meta-rule 3 invalidation hook. | (per containing entity type) |

---

# Designed extensions, not yet implemented

These ROADMAP items will extend or modify the architecture when
implemented. Recorded here so future sessions don't re-discover
them. Full design lives in `ROADMAP.md`.

> **RAG-related items** (multimodal ingest, structural retrieval,
> query rewriting, agentic retrieval, late-interaction text
> retrieval) are resolved (ACCEPTED in session 5 post-audit) in
> `docs/rag-pipeline-decisions.md`. The bullets below list the
> ROADMAP framings; that doc carries the verdicts + alternatives
> + revisit triggers.

- **Audit trail** — unified change/decision/version log across
  artifacts, references, manifests, configs, integrations,
  bausteine, plans, correspondence. Today scattered (`decisions.md`,
  `snapshots/`, `changelog.md`, manifest archives, git). Will
  formalize as a Memory (record) sub-kind or a new
  Configuration-style log. Per meta-rule 3, every entity already
  declares invalidation; this extension unifies the log.
- **Human-readable artifact generation at checkpoints** — every
  meaningful checkpoint (send-gate, phase transition, draft-invoice,
  baustein-promotion, config-change) produces a PDF/HTML alongside
  machine state.
- **Integration registry** — discovery API over callables (skills,
  MCP tools, adapters) with capability metadata. Skills already
  carry `capabilities[]`-equivalent in their `phase_role` +
  `handoffs[]` frontmatter (post-design-review session 5);
  registry will federate that with backend tool registration.
- **Web UI for collaborative review** — Coolify-hosted; review-
  platform integration adapter class. First non-MCP frontend —
  triggers the `pbs_core/pbs_mcp` physical split.
- **PM + invoicing** — per-project `_ai/billing.md` ledger;
  `log-time` + `draft-invoice` skills; uses accounting integration
  adapter.
- **Multimodal RAG ingest pipeline** — page-image retrieval
  (ColPali), table extraction, OCR, DRM removal. Architecture
  decided: local pre-processing + embedding + matching; reading +
  reasoning happens via the in-loop Claude session.
- **Structural retrieval** — legal §-graph + project-cross-project
  graph + verfahren state-machine. SQLite alongside LanceDB.
- **Query rewriting** (HyDE, decomposition, expansion) +
  **agentic retrieval** (per-claim search) + **late-interaction
  text retrieval** (ColBERT-v2, conditional) — all retrieval-
  pattern improvements.
- **Per-domain memory directories** (`memory/domain/<X>/`) —
  introduce when first domain-scoped reference content lands.
  Mirror of references / doctypes layering.
