# Decision record: Greenfield architecture review under VISION lens (max-effort session 11)

**Status**: ACCEPTED (session 11, 2026-04-30)
**Owner**: ARCHITECTURE.md "Pattern-vs-instance discipline"; ROADMAP commitments #18 (substrate eval) + #19 (RAG eval); VISION.md three-axis thesis
**Related**: `ai-as-runtime-hybrid-shape.md` (#16 — hybrid-shape principle), `sparring-output-v1.md` (sparring axis-2 mechanisms 1-7), `office-vs-department.md` (#12 — office abstraction), `a2a-and-gemini-pattern-emulation.md` (#10 — archetype boundary), all session-5-7 backend + sparring + audit decision records (verified survive greenfield)

## Context

Session 11 closed with a max-effort retroactive review across 9 decision records (sessions 5-11). User then raised a deeper question:

> "So it all holds even if we considered throwing it all away and starting fresh? Should align with VISION.md and be radical. Like greenfield lens in context of VISION. Makes sense and is valuable? This will help us prepare for the next item where we research frameworks (like the MS one)."

The retroactive review checked: "do current decisions hold under current discipline?" Answer: yes, with framing refinements. But the greenfield question is sharper: **if we threw it all away and started fresh with VISION as the anchor, would we make the same decisions, or would we make different/radical ones?**

The user's framing connects this directly to upcoming substrate research (#18 agentic framework eval): without greenfield clarity on what we're TRYING to build, #18 risks evaluating frameworks against status-quo PBS (anchoring bias) rather than aspirational PBS. The greenfield exercise establishes the **aspirational target + disqualifying criteria** that #18 (and #19 RAG eval) consume as their evaluation scope.

This is also the design-review skill's anti-status-quo bias mechanism applied at the architecture's largest scope.

## The exercise — greenfield with VISION as anchor

**Imagined clean slate**: no PBS code, no decisions made, no inertia. The only fixed inputs are:

1. VISION.md three-axis thesis (intertwining-AI-workflow + sparring partnership + authorship preservation)
2. Vivienne Ming's research foundation (oracle / validator / sparring modes)
3. Pioneer-instance positioning (PBS validates the framework; framework is the IP)
4. Single-big-model archetype (not multi-agent A2A; that's Tier 3 separate archetype)
5. Anthropic ecosystem (Claude Code dev runtime, Cowork end-user runtime, MCP protocol)

**Question per architectural commitment**: "Would we build this from scratch?"

## Radical alternatives considered

Genuinely tried 15+ alternatives. Most failed on VISION grounds, not inertia.

### Alternatives that fail VISION

| Alternative | Why it fails |
|---|---|
| **AI-only architecture** (no Python backend) | No contract enforcement / audit / persistence → fails axis 3 (defensibility). No source-grounded retrieval without storage. |
| **Backend-only** (no skills) | AI as tool, not co-worker → fails axis 1 (intertwining). |
| **Single agent** (no orchestrator + skills split) | No composability / audit / single-responsibility → fails axis 1. Monolithic orchestration. |
| **Structured-everywhere** (no markdown bodies) | SQL-DB-trap; brittle for LLM-mediated systems → directly contradicts AI-as-runtime hybrid-shape (v0.16). LLMs reason poorly over highly-normalized schemas. |
| **Multi-agent A2A from day 1** | Wrong archetype for our scale tier. Per `a2a-and-gemini-pattern-emulation.md`: Tier 3 = N agents via A2A; we explicitly chose Tier 1-2 = single-Opus orchestration. Imposes federated-system overhead without federated-system requirement. |
| **LLM-as-database** (no persistent files) | No audit trail → fails axis 3. No reproducibility of "why was this decided?" |
| **Drop sparring-output schemas entirely; trust LLM with good prompts** | Vivienne Ming's research: only 5-10% of human-AI hybrid teams achieve sparring without structural enforcement. Default is oracle-mode (zero human contribution) or validator-mode (worse than AI alone). Without structural backstop, drift to oracle mode session by session → fails axis 2. |
| **Sparring validation across ALL skill outputs** (not just 3-of-7 mechanisms) | False-positive risk for non-sparring contexts. Setup wizards SHOULD give clear answers; counter-argument every step would be pointless friction → violates axis 1 selective-friction calibration. |
| **Drop pattern/instance separation** (per-bureau monorepo, no abstract pattern) | Breaks AI-office-builder (v2 vision) + consulting business model. Forks would mean every bureau diverges; consulting IP becomes worthless. |
| **Component-based ECS** (entity-component-system) | Wrong abstraction level for our entity count. ECS makes sense for game engines with hundreds of entities; we have a few dozen. Ceremony without benefit. |
| **Imperative orchestration** (Python orchestrator code, not LLM-mediated skill) | Loses semantic routing intelligence. The orchestrator's value IS its LLM-mediated reasoning. Hard-coded routing breaks intertwining axis. |
| **Different framing entirely** (not "AI office") | VISION's three axes anchor on this framing + pioneer-instance positioning. Reframing discards foundational thesis. The "office" abstraction IS the IP. |
| **Conflate memory + references + bausteine into one storage layer** | Different invalidation contracts per kind (memory: personal/team-scoped; references: legal-text-amendments; bausteine: project-rejection-rate). Conflating loses meta-rule 3 invalidation discipline. |
| **No plugin separation** (PBS-bureau monolithic; no plugin shape) | Misses ecosystem opportunity. Cowork is the deployment runtime; plugin shape is required. v2 builder generates plugins. |
| **AI as oracle from API responses only** (no persistent reasoning) | Fails axis 1 (intertwining requires continuous awareness, persistent state) + axis 3 (no audit trail of reasoning). |

### Alternatives that converge with current direction

Some "radical alternatives" turned out to already match the architecture's evolution:

- **All knowledge as entities** — initially a radical alternative ("conflate memory/references/bausteine"). Per #16 hybrid-shape (v0.16), references ARE entities now (BauGB.md, BauNVO.md). Per entity-elevation 3-test, bausteine elevate when they pass; most don't. The categorical distinction is dissolving into "entity with type=X" — already aligned with current direction.

- **Hybrid Python+LLM orchestration** — initially considered as alternative. Current architecture already has this: orchestrator skill (LLM-mediated routing) + MCP gates (Python deterministic). The split is meta-rule 4. ✓

## Where greenfield CONVERGES with current direction

These commitments survive clean-slate review and would be re-derived from VISION:

### Architectural patterns

- **Hybrid-shape (Pydantic frontmatter + markdown body, AI-as-runtime fuses them)** = exactly what serves intertwining (axis 1: continuous AI awareness of prose) + authorship (axis 3: defensible reasoning chain) + sparring (axis 2: prose for context, structure for contracts).
- **Multi-layer validation gating (L1 structural / L2 conventional / L3 retrospective scan / L4 prospective design / L5 external-boundary)** = each addresses distinct concerns; collapsing loses failure-mode coverage.
- **Pattern-vs-instance discipline + sharp defer rule (v0.20) + framework-foundation framing** = correct per pioneer-instance positioning + consulting business target.
- **Make wrong shapes impossible (v0.21)** = correct discriminator (gate-dispatched → structural; AI-applied → prose convention with audit).
- **Single-big-model archetype** (not multi-agent A2A) = correct for our deployment range; Tier 3 is separate archetype with documented migration path.
- **Pluggable transport (stdio + HTTP MCP)** = correct per #13 deployment flexibility.

### Domain abstractions

- **Office → departments → managed entities + skills + processes + references + memory + adapters** = clean abstraction that survives cross-domain test (legal-practice / research-lab / brand-voice / etc.).
- **Skills as singleton-department; office-level skills for cross-cutting concerns** = correct per #12 office-vs-department.
- **Process-as-md (per #16)** = correct (workflow-as-data is named failure mode in failure-mode-catalog).
- **Cross-department coordination event-shaped (not call-shaped)** = correct per #10 a2a-and-gemini constraint (preserves Tier 3 migration path).

### Audit + defensibility

- **Audit-trail v2 single-write architecture (gate atomically mirrors event → decisions.md)** = greenfield would re-derive this exactly. The v1 → v2 reversal is the canonical real-time-discipline-application example of make-wrong-shapes-impossible.
- **`actor_kind` + `actor_card` + `origin_agent_card` + `convention_applied` fields on AuditEvent** = correct (additive A2A-shape compatibility per #10; provenance per #6 + governance-and-identity-sourcing).

### Scope orthogonality

- **6-axis scope (universal × domain × state × department × office × project)** = greenfield would re-derive these axes. Each is orthogonal; no axis subsumes another.

### Discipline framework

- All eight architectural disciplines (pattern-vs-instance + sharp defer rule, make-wrong-shapes-impossible, AI-as-runtime hybrid-shape, entity-elevation 3-test, glue-not-replacement, validation-layering, evolution-patterns, informed-defaults) survive greenfield review.
- All four meta-rules (app-vs-office, memory-vs-RAG, source-of-truth + invalidation, execution-determinism + fail-closed corollary) survive.

## Genuine open questions — where greenfield WOULD diverge

Three areas where greenfield would not necessarily land on current implementation. These are the **genuine evaluation surfaces for #18 + #19 + future sparring work**.

### 1. Substrate choice (#18 territory)

Hand-rolled Python + MCP + Pydantic vs. an agentic framework substrate (MS Agent Framework / LangGraph / AutoGen / CrewAI / Semantic Kernel / Smolagents / OpenAI Swarm).

Greenfield doesn't pre-commit either way. The choice depends on whether a framework substrate composes with our load-bearing disciplines without forcing us to bend them. This is exactly what #18 evaluates.

#### Disqualifying criteria for #18 (derived from greenfield review)

A substrate candidate must pass ALL of these to be a real candidate. Failing any structural criterion is automatic disqualification — don't deep-eval.

| Criterion | Source discipline | Failure mode if violated |
|---|---|---|
| **Composes with MCP natively** | Anthropic ecosystem (Claude Code + Cowork runtimes); meta-rule 4 (gate boundary) | Framework wraps MCP awkwardly → ecosystem alignment lost; tool-use stops being primary |
| **Supports hybrid-shape** (markdown bodies as runtime fuel; not prompt-templating that flattens prose) | AI-as-runtime hybrid-shape (v0.16) | Framework treats prose as text-input only → SQL-DB-trap by default |
| **Pydantic-native or Pydantic-compatible** (not its own competing type system) | Strict-validation discipline + meta-rule 4 + #16 | Framework's type model competes with ours → dual maintenance, potential drift, validation discipline weakens |
| **Doesn't force SQL-DB shapes** (no relational entity model assumed) | AI-as-runtime + entity-elevation 3-test | Framework assumes entity-per-noun + foreign keys → catastrophic for LLM-mediated systems |
| **Composable with sparring patterns** (counter-argument validation hooks, anti-sycophancy hooks, asymmetric knowledge respect, output-schema validation) | VISION axis 2 + sparring-output-v1 | Framework optimizes for autonomy/oracle-mode → can't backstop axis 2 without fighting framework |
| **Audit-trail-as-canonical-source compatible OR extensible** | VISION axis 3 + audit-trail-v2 | Framework imposes its own logging/state model → audit chain breaks; reasoning reconstruction lost |
| **Pluggable transport** (stdio + HTTP) OR **transport-agnostic** | Per #13 deployment flexibility | Framework hardcodes one transport → Tier 1 ↔ Tier 2 portability lost |
| **Heaviness scales appropriately** across 1-person shop / small company / enterprise (operational AND cognitive heaviness sub-axes) | Consulting framework target spectrum | Framework forces enterprise-grade complexity at all tiers OR forces minimal-complexity at all tiers → wrong for at least 2 of 3 deployment tiers |
| **Anthropic ecosystem aligned OR vendor-neutral** (not Microsoft/Google/OpenAI lock-in via SDK) | Glue-not-replacement + ROADMAP v2 multi-archetype consulting positioning | Framework couples to vendor → multi-archetype consulting story breaks |

Probable disqualifications (verify in #18):
- **CrewAI** — likely fails hybrid-shape (its prompt-as-template model + role-playing abstractions probably treat prose differently). VERIFY.
- **OpenAI Swarm/Agents SDK** — fails Anthropic-ecosystem alignment + vendor neutrality. Likely automatic disqualification.
- **Smolagents** — possibly disqualified by being TOO minimal (no sparring hook surface, no observability primitives). VERIFY.

Probable serious candidates:
- **LangGraph** — graph-based state machines; verify hybrid-shape compatibility + LangChain churn risk.
- **MS Agent Framework** — production-ready, vendor-neutral-ish, MCP-supportive, A2A-native; verify hybrid-shape + sparring composability + heaviness profile.
- **Semantic Kernel** — production-ready, .NET-native (Python supported); verify hybrid-shape + Microsoft lock-in.
- **AutoGen** — multi-agent conversation framework, mature; verify hybrid-shape + heaviness profile.
- **Hand-rolled** (current default) — comparison baseline.

#### What this means for #18

The eval transforms from "comprehensive comparison of 8 frameworks" to "reject obvious mismatches first; deep-eval the survivors." Probably 2-4 frameworks survive disqualification. Comparison among survivors uses the heaviness sub-axes + concrete read criteria already in #18's scope.

### 2. RAG implementation (#19 territory)

Hand-rolled (LanceDB + bge-m3 + per-#13 ingestion-vs-serving split) vs. LlamaIndex pluggable.

Greenfield doesn't pre-commit. The CONTRACT (query → ranked passages with metadata) is correct per VISION axis 1 (source-grounded outputs). The IMPLEMENTATION can plug in.

#### Disqualifying criteria for #19

A RAG primitive (parser / chunker / retriever / etc.) is pluggable IF:

| Criterion | Failure mode if violated |
|---|---|
| **Per-reference Pydantic metadata model preserved** (entity-md-compatible per #16) | LlamaIndex's metadata model competes with ours → dual maintenance |
| **Citation traceability tied to OUR entity model** (not framework-specific source IDs) | Citations break entity-md cross-ref graph |
| **Per-#13 ingestion-vs-serving split honored** (heavy compute local, indices to cloud) | Framework forces single-deployment-shape → Tier 1 ↔ Tier 2 split lost |
| **Performance comparable to hand-rolled** (German legal text, multilingual, per-paragraph chunking) | Performance regression negates leverage |
| **Composable with our search_corpus MCP tool contract** (not requiring framework-specific consumer code in skills) | Skills couple to LlamaIndex → backend swap becomes multi-skill refactor |

Pluggable candidates (where adoption likely): document parsers (PDF, web-text), standard chunkers (extensible for our per-paragraph strategy), hybrid retrieval primitives (BM25 + vector + reranker), citation/source-tracking primitives.

KEEP CUSTOM (don't pluggable-replace): per-reference Pydantic metadata model, citation traceability tied to entity model, per-#13 ingestion split.

#### What this means for #19

Eval is primitives-by-primitive (per #19's pluggable framing) rather than all-or-nothing. Performance comparison on our specific use case (German legal text, multilingual, per-paragraph chunking).

### 3. Sparring infrastructure granularity — genuine info-gap, not manufactured restraint

This is the most subtle open question and the user explicitly asked it be captured.

**Current state**: 3 of 7 axis-2 sparring mechanisms are structurally enforced via Pydantic schemas (counter-argument, confidence calibration, visible reasoning). 2 are partially structural (what's missing, commit-to-recommendations — via specific schema fields in specific contexts per session-11 retroactive review). 2-3 stay primarily-behavioral (anti-sycophancy guard, asymmetric knowledge respect, recommendation-commit-in-other-contexts).

**Greenfield observation**: VISION axis 2 names sparring as the most-likely category-collapse path because it's gradual + undetectable without structural enforcement. Vivienne Ming's research is explicit: only 5-10% of human-AI hybrid teams achieve sparring; default mode is oracle/validator. **More structural enforcement would be greenfield-aligned.**

**But the info-gap is real, not manufactured restraint**:

| Mechanism | Why behavioral (info-gap reason — not up-front-cost) |
|---|---|
| **Anti-sycophancy guard** | Detection requires comparing skill output to PRIOR turn — did the skill soften without new evidence? Heuristic detection has false-positive risk: legitimate softening (user provided new context that changes the answer) looks like sycophancy. We don't yet know the heuristic shape that distinguishes legitimate-update from sycophantic-capitulation. **Info-gap**: empirical pattern of when LLM softens legitimately vs sycophantically isn't characterized. |
| **Asymmetric knowledge respect** | Tentatively naming "here's what I'm drawing on; this might be a case where local context I don't have should change the conclusion — does it?" requires the AI to identify when its codified-knowledge advantage might be overruled by user's tacit-current-causal advantage. The signal that the AI SHOULD invite user input is contextual, not formulaic. **Info-gap**: when does asymmetric-respect-naming help vs annoy? Probably context-dependent (high stakes → invite; routine → just say). Empirical pattern not yet characterized. |
| **Recommendation-commit (in non-orchestrator-Checkpoint-13 contexts)** | Within orchestrator's recommendation pattern, the schema enforces commit. But other skills' outputs (drafting, review) have moments where commit-vs-question is contextually right. Sometimes a question IS the right move (e.g., "I've drafted this section per §13a; do you want to verify the §13a applicability before I continue?"). **Info-gap**: when is commit-required vs question-allowed? Probably workflow-stage-dependent. Empirical pattern not yet characterized. |

**Per sharp defer rule (v0.20)**: these defers are CHRONOLOGICAL-VALID. The information needed to design structural enforcement (false-positive heuristics; context-dependency rules) doesn't yet exist. We need empirical data from real sparring sessions to see WHERE structural enforcement helps vs WHERE it produces false positives.

**Per sharp defer rule, what would be INVALID**: deferring because "more sessions" / "premature" / "we'll add it later when needed." The honest defer reason is "we lack the empirical pattern data to design the heuristic without false-positive rate."

### Greenfield recommendation on sparring (incremental, not radical)

**Plan when chronological info-gap closes**: after first 5-10 real sparring sessions accumulate, evaluate the empirical patterns. Specifically:

1. **Anti-sycophancy heuristic**: collect cases where LLM softened. Manually classify legitimate-update vs sycophantic-capitulation. If pattern emerges (e.g., "softening without new tool-result evidence = sycophantic"), structurally enforce.
2. **Asymmetric-respect contexts**: collect cases where user's local-context overruled AI's codified-knowledge. Identify the signal that triggers naming. If signal is contextual (high-stakes / first-of-kind / etc.), structurally prompt for naming in those contexts.
3. **Recommendation-commit context-dependency**: collect cases where question vs commit was the right move. Identify the workflow stages. If stages cluster (e.g., "verification-checkpoint stages allow questions; production-output stages require commit"), structurally enforce per stage.

**Until then**: behavioral enforcement via skill body language; audit + design-review monitoring for drift.

**Watch position in failure-mode catalog**: under "discipline-bloat / over-naming" entry — premature elevation of behavioral mechanisms to structural BEFORE the info-gap closes would be its own anti-pattern. Genuine empirical signal first, then structural enforcement.

This is an **honest defer** under sharp defer rule, distinct from manufactured restraint. The mechanism is in scope; the implementation timing depends on info that genuinely doesn't exist yet.

## Connection to existing disciplines

| Discipline | Connection |
|---|---|
| **Pattern-vs-instance + sharp defer rule (v0.20)** | Greenfield exercise IS the discipline applied at architecture's largest scope — verifying that current commitments are pattern-level, not instance-locked. |
| **Make wrong shapes impossible (v0.21)** | Greenfield review surfaces multiple worked examples (mcp-fallback structural; trigger-convention conventional; audit-trail v1→v2 reversal real-time application). Reinforces discipline. |
| **AI-as-runtime hybrid-shape (v0.16)** | Greenfield disqualifying criteria for #18 derive directly: substrate must support hybrid-shape, not flatten prose to prompt-templating. |
| **Validation-layering (v0.18)** | Greenfield review's "where would we diverge" surfaces the deterministic-vs-LLM judgment line for sparring mechanisms 4-7 (currently behavioral, candidate for structural-after-empirical-data). |
| **Pioneer-instance positioning** | Greenfield exercise validates that PBS-current-state and PBS-aspirational-state are aligned; the framework IS what we'd build greenfield. |

## Defers (per defer-instinct discipline)

| Defer | Home | Specific cost being avoided |
|---|---|---|
| **D1**: Sparring mechanisms 4-7 elevation to structural | Behavioral until empirical pattern data accumulates (5-10 real sparring sessions); then evaluate per mechanism | Designing structural heuristics WITHOUT empirical pattern data = false-positive rate unknown; would lock the wrong heuristic |
| **D2**: Concrete substrate adoption decision | #18 substrate eval (BLOCKING for #9 implementation phase) | Pre-empting #18 with greenfield-only conclusions; #18 needs concrete framework reads + heaviness measurements |
| **D3**: Concrete RAG primitives adoption decision | #19 LlamaIndex pluggable eval (BLOCKING for Phase 1 corpus) | Same shape as D2 |
| **D4**: Periodic discipline-pruning check (per failure-mode catalog "discipline-bloat" entry) | Future audit/design-review work; runs at major version boundaries | Premature pruning loses architectural memory; defer until pattern of over-naming surfaces |

Each defer names a specific home + specific cost. Per `feedback_defer_instinct.md` + `feedback_pattern_not_instance_defers.md`: chronological-valid (info-gap), not up-front-cost.

## Constraints flowing to downstream commitments

### → #18 (Agentic framework substrate eval)

- **Disqualifying criteria** above ARE the eval scope. Substrates failing any structural criterion are rejected without deep-eval. Eval transforms from "comprehensive comparison of 8 frameworks" to "reject obvious mismatches first; deep-eval the 2-4 survivors."
- **Heaviness sub-axes** (operational + cognitive) per session-11 ultrathink-review remain critical evaluation dimensions for the survivors.
- **Output**: `docs/decisions/substrate-agentic-framework.md` — references this DR's disqualifying criteria; deep-eval section evaluates only survivors.

### → #19 (LlamaIndex pluggable RAG eval)

- **Pluggable boundary** per disqualifying criteria above. Pluggable: parsers, chunkers, hybrid retrieval, citation primitives. Keep custom: per-reference Pydantic metadata, citation traceability tied to entity model, per-#13 ingestion split.
- **Performance comparison** on our specific use case (German legal text, multilingual, per-paragraph chunking) — not generic benchmarks.

### → Future sparring mechanisms 4-7 evaluation

- **Trigger**: 5-10 real sparring sessions accumulate empirical pattern data.
- **Process**: collect cases per mechanism; manually classify; identify heuristic signals; if pattern emerges, structurally enforce.
- **Anti-pattern guard**: don't elevate to structural BEFORE empirical signal — that's premature-discipline-elevation, named in failure-mode catalog as candidate watch position.

### → ARCH version log

This DR becomes load-bearing reference for #18 + #19. ARCH section disciplines reference it as "greenfield-validated."

## Pattern-vs-instance check on the exercise itself

Is this greenfield review exercise pattern-level or PBS-instance? The METHOD (greenfield-with-VISION-as-anchor) is pattern-level — any AI-office deployment could use the same exercise. The CONTENT (which alternatives we considered, which mechanisms are open questions) is PBS-instance + framework-instance.

Generalizes to other deployments: a legal-practice or research-lab AI office in the v2 builder era could run greenfield-with-its-own-VISION review at architecture milestones.

## Revisit triggers

- **#18 substrate eval completes** — confirm the disqualifying criteria above proved load-bearing in practice. Adjust if any criterion was wrong-shaped.
- **#19 RAG eval completes** — same.
- **First empirical sparring data accumulates** (5-10 sessions) — evaluate mechanisms 4-7 for structural elevation per the plan above.
- **Major architectural commitment lands** (e.g., #11 Cowork integration completes; #13 deployment flexibility ships) — re-run greenfield review to verify commitment didn't drift architecture from VISION.
- **VISION updates** (axis added, foundational research evolves) — re-run greenfield with new anchor.

## Files touched

- `docs/decisions/greenfield-architecture-review.md` — this file (NEW)
- `ARCHITECTURE.md` — v0.24 → v0.25 with version log entry referencing this DR as load-bearing for #18 + #19
- `HANDOFF.md` — essential framing references this DR as required reading before #18 substrate eval starts
- `ROADMAP.md` #18 + #19 — constraints sections updated to reference this DR's disqualifying criteria

No code changes this commitment. Implementation lives across #18 (substrate eval consuming disqualifying criteria) + #19 (RAG eval consuming pluggable boundary) + future sparring evaluation when empirical data accumulates.
