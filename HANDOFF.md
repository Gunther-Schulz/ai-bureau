# Session handoff — pbs-bureau

## 🧭 CORE OPERATING FRAME (read first, every session)

**PBS is the framework foundation for the consulting business**,
validated by the Schulz planning bureau. PBS is the pioneer
instance, never the product. At every architectural step, do
the **full scalable foundational work** — designed for any
expert-practitioner deployment (legal-practice / research-lab /
brand-voice / consulting-client) at first bind, not
minimum-viable-PBS today with infrastructure added later.

**Defer rule (sharp)**: defer ONLY for chronological reason
(downstream shape unlocked, second-domain feedback needed,
upstream precedent unresolved). **Up-front costs are NEVER
valid defer reasons** — not "more sessions," not "premature,"
not "YAGNI," not "PBS doesn't need it yet." See
ARCHITECTURE.md "Pattern-vs-instance discipline" → "Defer rule"
subsection (v0.20) and `memory/feedback_pattern_not_instance_
defers.md`.

The two tests that must pass for any defer to be honest:

1. **Chronological**: is there specific information that would
   change the design, and that information will exist later but
   not now? Name it.
2. **Framework-cost**: would a hypothetical legal-practice /
   consulting-client deployment opening tomorrow need this? If
   yes, design now.

This frame supersedes any prior "we'll add it when PBS needs
it" reasoning in the queue.

---

## 🚧 BLOCKING SUBSTRATE EVALUATIONS (added session 11; #18 SHIPPED session 12; #21 NEW session 12 — read before implementation work)

**STATUS UPDATE (session 12)**: #18 SHIPPED — Claude Agent SDK + MS Agent
Framework adopted as dual-substrate; Substrate Protocol NEW architectural
pattern; Tier 3 reframed per pattern-vs-instance discipline (Gemini Enterprise
→ enterprise multi-agent A2A platform with Gemini / Azure AI Foundry / AWS
Bedrock AgentCore as instances). See `docs/decisions/substrate-agentic-framework.md`
for full eval + recommendation + counter-considerations. #21 NEW (SDK deep-read)
added session 12 — near-blocking for #9 implementation phase.

#19 (LlamaIndex pluggable RAG eval) + #20 (PydanticAI eval) still pending.
Implementation phase WAITS for #21 + #19 + #20 to complete (#18 lift complete).

Three substrate-framework evaluations BLOCKING for #9 implementation
phase + #11 + #13 + Phase 1 corpus. Surfaced session 11 when the
substrate question + corrected counterfactual ("we started 2 days
ago, full refactor when it's a win is the explicit tenet") forced
honest re-evaluation. **Substrate choice influences the Python
implementation of every downstream pre-RAG commitment**; doing the
evaluations after locking implementation choices means retrofitting
under sunk-cost pressure.

**REQUIRED READING before any pre-implementation work** (post-#18):
`docs/decisions/substrate-agentic-framework.md` — substrate decision
locked session 12. Captures: 9 disqualifying criteria; per-candidate
verdicts; recommendation (Claude Agent SDK + MS AF dual-substrate; Substrate
Protocol NEW pattern); counter-consideration (Shape A vs B + model-swap-ability
+ Tier 3 implications); hybrid analysis. **#21 (SDK deep-read) consumes this
DR's recommendation as input.** **#9 implementation consumes the Substrate
Protocol pattern as architectural foundation.** **#11 (Cowork integration)
consumes Claude Agent SDK as primary substrate.** **#13 deployment flexibility
consumes substrate × deployment matrix.**

**REQUIRED READING for understanding the substrate eval method**:
`docs/decisions/greenfield-architecture-review.md` §3 — establishes
the **disqualifying criteria** for #18 (composes with MCP / supports
hybrid-shape / Pydantic-compatible / no SQL-DB shapes / sparring
composable / audit-trail compatible / pluggable transport / heaviness
scales / vendor-neutral). Substrates failing any structural criterion
were rejected without deep-eval. Eval transformed from "comprehensive
comparison of 8 frameworks" to "reject obvious mismatches first;
deep-eval the 2-4 survivors" (final survivors: 4). Same DR also establishes
#19 RAG pluggable boundary (parsers/chunkers/retrieval pluggable; per-ref
Pydantic metadata + citation traceability + per-#13 ingestion split
stay custom).

**Future-roadmap items #18 MUST consider** (per ROADMAP #18 entry):
- **Time-driven triggers (Gap A)**: framework must compose with
  server-side scheduler firing "tick" events on schedule (per #13's
  `register_scheduled_trigger` MCP tool). Substrate candidates that
  impose competing scheduler abstraction → friction or rejection.
- **Event-driven adapter callbacks (Gap B)**: framework must support
  adapter Protocol's `subscribe_to_changes(callback)` (push) OR
  `poll_for_changes() -> list[Event]` (pull) per #9 Bundle E
  (restored from #11 deferral). External state changes translate to
  AuditEvents with `actor_kind=external_agent`. Substrate candidates
  that can't compose with adapter callback pattern → friction or
  rejection.

**What can proceed in parallel** (substrate-agnostic): Bundles B + C
+ D + E design work (entity gate signatures, Pydantic schema shapes,
body-preservation contracts, Layer 3 mechanism options,
ProjectEntity migration plan). Pure design doesn't depend on
substrate. Implementation phase WAITS for substrate decisions.

**Order** (front of pre-RAG queue):

| Eval | Scope | Tier | Why first |
|---|---|---|---|
| **#18 — Agentic framework substrate (multi-framework + heaviness × 2 sub-axes)** | 2-3 sessions | **BLOCKING** for #9 implementation + #11 + #13 + Phase 1 | Highest leverage; affects orchestration + transport + agent runtime. Frameworks BUCKETED: enterprise-grade (MS AF / Semantic Kernel / AutoGen) / mid-weight (LangGraph / CrewAI) / lightweight (Smolagents / OpenAI Swarm) / hand-rolled baseline. **Heaviness has TWO sub-axes**: operational (boot/memory/deps) + cognitive (abstractions to learn). Both must scale across 1-person shop → small company → enterprise. Does heaviness scale automatically? |
| **#19 — LlamaIndex pluggable RAG eval** | 1-2 sessions | **BLOCKING** for Phase 1 corpus | RAG-specific. **Pluggable framing**: NOT all-or-nothing substrate. Primitives-by-primitive evaluation (parsers / chunkers / hybrid retrieval / query engines pluggable; per-reference Pydantic metadata + citation traceability + per-#13 ingestion split stay custom). Performance comparison vs handbuild for German legal text. |
| **#20 — PydanticAI evaluation** | 1 session | **NOT BLOCKING for general implementation; before Bundle B Layer-3 mechanism decision specifically** (demoted from BLOCKING tier under session-11 ultrathink-review — narrower surface than #18/#19) | Typed agent calls + sparring-output validation + Layer 3 mechanism options A/B/C. Future-ready if adopted. Could inform Bundle B Layer-3 (Pydantic subclass option specifically). |

**Parallelization**: #18 + #19 + #20 are independent (agentic framework vs RAG vs typed agents) — could run in parallel sub-sessions or as concurrent investigations, compressing the BLOCKING window from 4-6 sessions to 2-3 if executed in parallel. Each produces a decision record.

**Scope-creep guard** (added session-11 ultrathink-review): each eval is time-boxed; decisions made with available evidence after time-box. Further investigation deferred ONLY with chronological reason ("framework X just shipped major release" qualifies; "we should also consider Y in similar bucket" doesn't — pick representative within bucket, not exhaustive enumeration).

**Each produces a decision record** (`docs/decisions/<name>.md`)
with adoption / rejection / partial / pluggable conclusion +
constraints flowing to downstream commitments.

**See ROADMAP.md commitments #18, #19, #20** for the full
investigation scopes.

---

## ⚡ For next session — essential framing

**Read these three before substantive work, in this order:**

1. **This file (`HANDOFF.md`)** — current session state, queue, recent decisions
2. **`VISION.md`** — three axes (intertwining-AI-workflow + sparring partnership + authorship preservation) + Vivienne Ming's research foundation (oracle / validator / sparring-partner modes; only sparring outperforms human-alone or AI-alone). **Without this, AI drifts toward oracle/validator-mode framings — gives easy answers instead of generating productive friction. Empirically confirmed session 9: VISION re-grounding caught a misframing mid-conversation, prompted the role-shift refinement.**
3. **`ARCHITECTURE.md`** — **v0.29** (cumulative session-11 review work: greenfield architecture review under VISION lens (v0.25); VISION sharpenings (v0.26); ARCH disciplines greenfield (v0.27 — skill-granularity elevated); architectural-gap detection sweep + maintenance rule 6 periodic greenfield review (v0.28); per-DR internal gap detection with 3 amendments + 2 backfill DRs (v0.29). Architecture survives clean-slate review under max-effort. See `docs/decisions/greenfield-architecture-review.md` — REQUIRED READING before #18 substrate eval starts. **Read the "Data + boundary reference card" near the top first** — it consolidates the "where does X go?" rules across all disciplines into one table. **Companion**: `docs/validation-gating-overview.md` (v0.22, L5 added v0.23) — systems-view consolidating the FIVE validation layers (L1 runtime structural / L2 runtime conventional / L3 retrospective scan / L4 prospective design / L5 external-boundary). Read both before designing a new gate or convention. The architectural surface, organized:
   - **5 design disciplines** (load-bearing rules that gate design decisions): pattern-vs-instance + sharp defer rule (v0.20), make-wrong-shapes-impossible (v0.21), AI-as-runtime hybrid-shape (v0.16), entity-elevation 3-test (v0.13), glue-not-replacement (v0.15)
   - **3 operational principles** (rules that guide implementation choices): validation-layering deterministic-primary (v0.18), three evolution patterns mutable/append-only/forward-only (v0.19), informed-defaults ship-best-shape (v0.18)
   - **4 meta-rules**: app-vs-office (#1), memory-vs-RAG (#2), source-of-truth + invalidation (#3), execution-determinism + fail-closed corollary (#4)
   - **Earlier resolved concepts** absorbed into disciplines: archetype-portability (paragraph in pattern-vs-instance v0.10), office-vs-department modularization (#12, resolved v0.11), managed-entity concept (#9, framed v0.12)
   - Plus 4-axis scope orthogonality (universal × domain × state × department × office × project = 6 axes)

   **Without this, architectural proposals re-suggest already-discarded patterns, violate established discipline, reproduce pioneer-instance-anchored defer rationales, or chase six sections to apply a placement rule that the reference card answers in one row.**

**Read conditionally** (when context calls for it):
- `docs/strategic-positioning.md` — consulting positioning, marketplace decisions, brand questions, sparring-mode pitch
- `docs/decisions/<specific>.md` — when working in that decision's area (audit-trail-v2 for retrofits + session-11 amendments; office-vs-department for department modules; a2a-and-gemini-pattern-emulation for schema work; **skill-expert-agent-and-domain-knowledge** (NEW session 11) for skill granularity / agent dual-mode / display_label / fine-grained expertise placement; ai-as-runtime-hybrid-shape for entity-md / process-as-md decisions; governance-and-identity-sourcing for prose-rule conventions)
- Specific ROADMAP commitment #N entry — when working on commitment #N
- Specific skill bundle (`plugin/skills/<name>/SKILL.md` + `references/`) — when modifying that skill
- `docs/plugin-conventions.md` (especially §11 + §11b) — writing or editing skills
- `docs/backend-conventions.md` — backend code work
- `~/dev/reference/knowledge-work-plugins/` — when working on #11 (Cowork integration)

**Read situationally** (rare; when explicitly relevant):
- `docs/audits/` + `docs/design-reviews/` — running follow-up reviews
- `docs/rag-pipeline-decisions.md` — Phase 0/1 RAG work
- All decision records together — when designing a new architectural discipline (rare)

The detailed "Read order for next session" section further down is the long-form version of this trio + conditional list. The trio above is the **minimum viable framing** for any session.

**Re-grounding mid-session is valid** when drift is detected — when AI's framings lean toward easy answers, when an architectural discipline isn't being applied, when the user pushes back on something that suggests oracle-mode drift. See `memory/feedback_vision_arch_grounding.md`.

---

## Session 14 — Competitive-landscape research + VISION re-alignment + Option B architectural floor + EU AI Act compliance specialist + Cherry Ventures funding path

End of session 14 (2026-04-30). Six major work products shipped in batch commit. Operating-geography clarification mid-session ("EU, mainly Germany") reshaped strategic + regulatory framing. Paperclip + PAI + Avoice + a16z + EU AI Act each got dedicated research depth.

**What shipped session 14** (commit batch with cascade):

- **7 research passes complete** (4 OS deep-reads — Letta + OpenSail + PAI + Paperclip + commercial scan + OS+hybrid scan + Avoice/DACH architects + a16z/EU VC + EU AI Act/DACH regulatory). Cloned Letta + OpenSail + PAI + Paperclip to `~/dev/reference/` for local code-read. Gap-claim CONFIRMED with HIGH confidence raised — zero projects match 4+ of 5/6 distinctness axes simultaneously.

- **3 NEW decision records persisted**:
  - `docs/decisions/closest-neighbors-deep-read.md` — comprehensive synthesis of 4 deep-reads + commercial landscape + DACH analysis + 5-of-6 axes distinctness verdict + ~10 adoption opportunities table + watch-list entries
  - `docs/decisions/shape-extension-and-architectural-floor.md` — shape-extension framework (workspace shapes as pluggable extensions; per-shape configuration defaults + shape-specific primitives) + Option B architectural floor (3 axioms structurally enforced regardless of shape: anti-Art-25-trap gate + claim-level audit + human authority chain) + Make-wrong-shapes-impossible application
  - `docs/decisions/vision-realignment-session14.md` — Round 1 axis refinements + Round 2 R1-R8 sharpening + scope clarification (practitioner-shape) + foundation expansion + lifecycle triggers; locked Option B architectural inheritance for VISION axis 3 cross-shape enforcement

- **VISION.md substantially updated** — axis 2 framing as runtime mechanism; axis 3 scope-clarified to practitioner shape; new sections: VISION scope (post-session-13+14) + Counter-VISION engagement (R1) + What VISION does NOT claim (R2) + Robustness to AI capability growth (R3) + Falsification criteria (R6) + VISION ≠ ARCHITECTURE boundary (R4) + Lifecycle triggers (R8); Foundations expansion (Schön + Dreyfus + Kahneman as adjacent body citations + EU AI Act Art. 14 / Berufsrecht / Cherry Ventures as empirical regulatory anchors).

- **ARCHITECTURE.md v0.31 → v0.32** — NEW section "Workspace shapes — framework-supported catalog" (6 shapes: practitioner / autonomous-business / personal-OS / KG / federation / hybrid; shape extension contract; Tom Sawyer dynamic) + NEW section "Option B architectural floor" (3 axioms + composition with disciplines) + reference card rows (which workspace shape; can violate accountability; PBS-product vs framework split).

- **ROADMAP commitments #24 + #25 added**:
  - **#24 EU AI Act + DACH compliance specialist** (HARD REQUIREMENT before Aug 2026 production B-Plan use). Two-tier specialist: `eu-ai-compliance` (cross-archetype) + `dach-regulatory-extension` (domain-anchored). Substrate-level additions (AuditEvent ai_act_article_mapping; 6-month retention default; specialist conformity Pydantic gate). Hard requirements: Art. 50(4) AI-disclosure for B-Plan Begründung (public-interest per BauGB §3); DSGVO RoPA + controller posture; BRAK/BAK-aligned client disclosure. Critical architectural constraint: Art. 25(1)(b) substantial-modification trap structurally prevented (specialist conformity manifest as Pydantic gate; impossible-by-construction). Major commercial asset: ISO 42001 SoA scaffold publishable.
  - **#25 Shape extension framework + Protocol pluggability** (FOUNDATIONAL; Tom Sawyer dynamic enablement). Shape extension contract; Protocol pluggability for Coordination/Sparring/Audit/Trust/Time; long-running runtime substrate adapter (referenced from R3a in-process MCP work; needed for autonomous-business shape); practitioner-shape extension reference implementation (PBS pioneer); Option B floor implementation (anti-Art-25-trap + claim-level audit + human authority chain enforcement).

- **`docs/strategic-positioning.md` substantial rewrite** — NEW sections: Layered approach (framework breadth + positioning narrowness) + Closest OS neighbors (axes-fit table + adoption opportunities) + Closest commercial neighbors (Beck-Noxtua + Anthropic Cowork + Stilta + Avoice + AutoSitu) + DACH competitive landscape (Phase0 / Langdock / Beck-Noxtua + BAK marketing wedge) + Sharpened differentiators (5/6 axes unique) + EU AI Act tailwind + a16z/Sequoia thesis as positioning risk + Cherry Ventures as only published EU VC thesis match + Recommended funding path (consulting + grants + strategic + Cherry-of-last-resort) + ICP refinement + Compliance specialist as marketplace asset.

- **3 failure-mode catalog entries added**:
  - `verbal-framing-collision` — verbal positioning collision vs architectural distinctness; mitigation via approach-level test
  - `approach-level test as repeatable diagnostic` — methodology for verbal-collision verification (simulate building pioneer instance on competitor's framework; if overlay > native, approach mismatch)
  - `competitive-positioning instance-leak` — pattern-vs-instance discipline applied to own competitive positioning (parallel to ARCH defer-rationale instance-leak)

- **Memory `feedback_propose_before_commit.md` REFINED** session 13 (from prior commit) — supersedes prior formulation. Decision-phase needs approval; markdown-content phase doesn't. Applied throughout session 14 cascade — single-batch persistence + commit + push.

**Major architectural decisions locked session 14**:

1. **Layered approach** (locked): OS framework workspace-shape-neutral + marketed product practitioner-focused. Framework breadth lives in ARCH; positioning narrowness lives in VISION + strategic-positioning.

2. **Shape extension model** (NEW pattern): workspace shapes are pluggable extensions; framework provides shape-neutral primitives + Protocol pluggability; concrete shapes (practitioner / autonomous-business / personal-OS / KG / federation / hybrid) live as `extensions/shapes/<shape-id>/`; PBS pioneer = practitioner-shape extension reference; community can build other-shape extensions (Tom Sawyer dynamic).

3. **Option B architectural floor** (locked): 3 accountability axioms structurally enforced regardless of shape (anti-Art-25-trap gate + claim-level audit emission + human authority somewhere in accountability-bearing output chain). Other shapes can configure axis intensities (sparring optional vs always-on; audit overlay; coordination event vs call) but cannot disable structural floor without explicit framework override (which produces non-PBS-conformant deployment).

4. **VISION re-alignment** (locked): three axes structurally same; refinements in axis-2 wording (runtime mechanism vs partner) + axis-3 scope (practitioner-shape-specific); 8 new subsections (R1-R8) added; lifecycle + falsification criteria + counter-VISION engagement + negative space + temporal robustness all explicit.

5. **EU AI Act compliance commitment** (#24): HARD REQUIREMENT before Aug 2026 production. Two-tier specialist + substrate-level enforcement. Practitioner-as-deployer cleanest posture; sparring uniquely operationalises Art. 14; audit-by-construction maps Art. 11/13/26(6); ISO 42001 SoA scaffold = major commercial asset.

6. **Funding path strategy locked**: ground-up consulting revenue + EXIST/ZIM/go-Inno DACH grants → strategic capital (Beck-Noxtua publishers + chambers + state banks model) → Cherry Ventures VC-of-last-resort. AVOID GC-channel firms + US-classical VC (Sequoia/a16z thesis import would force narrative drift).

**Competitive landscape findings**:

| Project | Axes-fit | Type | Verdict |
|---|---|---|---|
| PAI (Personal AI Infrastructure) | 3/5 | OS | Closest by architecture; single-human-bound + Claude-Code-coupled |
| OpenSail (TesslateAI) | 2.5/6 | OS | Different domain (agentic IDE/app-builder); adjacent not competitor |
| Beck-Noxtua | 2/6 | Commercial DACH | Closest commercial neighbor for German market; vertical SaaS shape |
| Anthropic Claude Cowork | 2/6 | Commercial | Architectural direction-of-travel; Enterprise-only |
| Paperclip | 1.5/6 | OS | Conceptually distinct (autonomous business vs practitioner); adoptable patterns |
| Letta v1 | 1-2/5 | OS | Surface vocabulary collision; cargo-cult risk LOW |
| Avoice (architects) | 1/6 | Commercial US/UK | Doesn't block PBS in DACH (no localization) |
| AutoSitu (municipal review) | 1/6 | Commercial US | OPPORTUNITY not threat — inverse side; cities digitizing review = demand for audit-ready submissions |
| Phase0 (DACH operational software) | NA (different layer) | Commercial DACH | Owns operational layer; PBS positions ABOVE on expertise + audit + multi-actor + sparring |
| Langdock (DACH DSGVO platform) | 1/6 | Commercial DACH | Substrate-level threat; PBS differentiates via codified specialists |

**What's deferred to next sessions**:

- **#19 + #20** still pending (substrate evals — LlamaIndex pluggable RAG eval; PydanticAI eval). Both NEAR-BLOCKING for Bundles B/C/D/E + Phase 1 corpus.
- **Memory adapter strategy** — extend #19 scope to include Mem0 / Zep / Graphiti / Cognee evaluation.
- **Bundles B/C/D/E design** can proceed in parallel with #19/#20 (substrate-agnostic).
- **#25 implementation** before #24 implementation (Option B floor needed for compliance specialist substrate-level enforcement).
- **#11 Cowork integration** before #24 + #25 implementation (specialist primitive needs to be operational).

**Watch-list entries** (per `closest-neighbors-deep-read.md`):

- OpenSail practitioner-identity primitive emergence
- PAI practitioner-archetype fork ("PAI for lawyers / consultants / planners")
- Paperclip 5 trigger conditions (claim-level audit / always-on sparring / composable specialist / memory + invalidation / explicit practitioner courting)
- Letta skills+subagents evolution toward composable expertise bundles
- Beck-Noxtua archetype expansion (Steuerberater / Architekturbüro / Planungsbüro)
- Avoice EU/German market entry with DSGVO posture
- Anthropic Claude Cowork plugin ecosystem evolution
- AutoSitu adoption growth (opportunity)
- Cherry Ventures portfolio evolution (thesis maturation signal)
- CUNY AI Journalism Lab cohort (24 practitioner-builders 2026)

**Strategic insights crystallized session 14**:

1. **AutoSitu finding**: cities digitizing review = demand for audit-ready submissions = favors PBS audit-by-construction. Frame PBS as enabling cross-side compatibility, not compliance overhead.
2. **Cherry Ventures fit**: PBS positioning lands cleanly in Cherry's published thesis (only published EU VC thesis-aligned with practitioner-amplification).
3. **Beck-Noxtua precedent**: validates strategic-capital path (€80.7M from publishers + law firms; no classical VCs) — sovereign-AI funding model for PBS.
4. **EU AI Act asymmetric tailwind**: sparring uniquely operationalises Art. 14; practitioner-as-deployer cleanest posture; audit-by-construction maps Art. 11/13/26(6); self-host + EU residency = sovereign-AI alignment.
5. **a16z/Sequoia thesis is antithesis**: accepting US-classical VC capital would force narrative drift; recommended fundraising path explicitly avoids GC-channel firms.
6. **Compliance specialist = strategic asset**: ISO 42001 SoA scaffold cuts cert cost dramatically (€35-90k saved per deployment); marketplace v3 commercial asset.
7. **Phase0 DACH dominance**: PBS does NOT compete with Phase0 on HOAI/AVA mechanics; positions ABOVE on expertise + audit + multi-actor + sparring.

### Session 14 follow-up commits (2026-04-30 + 2026-05-01)

After main session-14 batch (`c0a97e0`), 5 follow-up commits sharpened + relocated content:

- **`c8f4171`** — pre-RAG queue reorder: locked **#25 → #20 → Bundles → #11 → #24 → #19** order. Preserves #20-informs-Bundle-B-Layer-3 dependency naturally (no provisional annotation). ROADMAP "BLOCKING SUBSTRATE EVALUATIONS" section restructured with explicit pre-RAG queue table at top + historical context below.

- **`1f1095b`** — load-bearing visual references persisted: NEW `ARCHITECTURE.md` "Framework architecture overview" section (4-layer canonical mental model: Substrate / Framework primitives shape-neutral core / Workspace shapes extensions / Concrete instances) + NEW `VISION.md` "Practitioner vs Specialist — vocabulary clarification" subsection (full comparison table). Plus Maintenance discipline rule 3 EXTENDED to cover visual representations.

- **`23517ca`** — VISION scope refactor: VISION had grown to 1181 lines + drifted into ARCH/strategic-positioning territory. Refactored to restore "deepest WHY" focus. REMOVED counter-VISION engagement subsection (~30 lines); MOVED Practitioner vs Specialist comparison to ARCH (full preservation); COMPRESSED VISION ≠ ARCHITECTURE boundary section + VISION lifecycle. Net VISION 1181 → 1065 lines (-116). Tighter scope discipline.

- **`5c24d99`** — VISION-axis → ARCH-implementation mapping table relocation: per scope-refactor audit, the 6-row mapping table was REMOVED with full content (only brief paragraph cross-ref left in VISION). Audit identified as genuinely valuable concrete reference. RELOCATED to `ARCHITECTURE.md` "How ARCH serves VISION — axis-to-implementation mapping" section (immediately after Framework architecture overview).

- **`2431926`** — counter-vision-engagement DR: NEW `docs/decisions/counter-vision-engagement.md` (~3500 words). Substantive intellectual engagement with the dominant 2026 opposing thesis (service-as-software). Multi-disciplinary thinkers covered — Susskind father+son + Frey/Osborne + Harari + Schwab + Bek/a16z (charitable case for) vs Autor + Brynjolfsson (Turing Trap) + Mindell (myth of full autonomy) + Dreyfus + Schön + Suchman + Kahneman + Sunstein/Hastie + Pasquale + Russell + Toyama + O'Reilly + Ming (anti-replacement / amplify case). Empirical record per industry (medicine + law + finance + aviation + customer service + Stanford workslop). Three sharp positioning claims. The 4 argument bullets (relocated from removed VISION counter-VISION subsection) live here as PBS's spine. Reference list: 17 foundational works. VISION cross-ref added in Foundations section. Strategic-positioning.md keeps fundraising-risk angle separately (different concern; complementary).

**Net session 14 + follow-up output**:
- 4 NEW DRs: `closest-neighbors-deep-read.md`, `shape-extension-and-architectural-floor.md`, `vision-realignment-session14.md`, `counter-vision-engagement.md`
- VISION + ARCH + ROADMAP + strategic-positioning + failure-mode catalog + HANDOFF substantial updates
- 4 cloned reference repos at `~/dev/reference/` (letta, opensail, pai, paperclip) for future session use
- Pre-RAG queue order locked: #25 → #20 → Bundles → #11 → #24 → #19
- 6 commits total to origin/main (`c0a97e0`, `c8f4171`, `1f1095b`, `23517ca`, `5c24d99`, `2431926`)

**Memory feedbacks applied + tested session 14**:
- `feedback_propose_before_commit.md` (refined session 13) — decision-phase approval; markdown content phase no per-content approval. Held throughout 14 + follow-ups.
- `feedback_judgment_and_automate.md` — committed positions throughout; minimal menu-presenting.
- `feedback_pre_decision_sharpening.md` — Round 1 + Round 2 USER-TRIGGERED rounds applied to VISION re-alignment; decomposition trigger respected (no Round 4).
- `feedback_full_monty_upfront.md` — comprehensive proposals in initial chat; iterative refinements via user-triggered rounds.
- `feedback_refine_pareto.md` — applied to scope-refactor audit (force "why?" challenge).

---

## Session 13 — #22 terminology + level-boundary re-evaluation shipped (Office → Workspace; Specialist NEW pattern primitive; Department demoted to optional grouping; three-tier framing; marketplace = of specialists)

End of session 13 (2026-04-30). Decision-design phase: 3-round sharpening (full monty + 2 user-triggered) on a broad architectural surface (terminology + level boundaries + workspace + specialist + grouping + strategic positioning + cross-cutting integration). ~26 refinements surfaced; ~85% expansions, ~15% revisions. Decomposition triggered at Round 4 per `decision-design-sharpening` skill rules → split into Sub-DR A (terminology + Specialist primitive) + Sub-DR B (three-tier framework + marketplace + positioning). Per-sub-DR sharpening rounds skipped per Pareto analysis (Round 3 covered integration surface; per-sub-DR rounds = manufactured criticism risk).

**What shipped session 13** (commit batch with cascade):

- **Sub-DR A** (`docs/decisions/terminology-and-specialist-primitive.md` NEW; status ACCEPTED): three coupled changes locked together:
  1. **Office → Workspace** at pattern primitive level. Cross-archetype stress test ≥6/10 archetypes "office" metaphor fights (solo expert, research project, creative practice, knowledge graph, federation, etc.). Naming alternatives (Workspace / Practice / Studio / Hub / Deployment) evaluated; Workspace wins on cross-archetype fit + software-ecosystem alignment.
  2. **Specialist** introduced as NEW pattern primitive between Skill and Workspace. Composable codified expertise bundle (skills + entities + process entities + references + memory + adapters). 5 composability axes (FROM/IN/WITH/ACROSS/OVER). Granularity 3-test (cohesive competence + distributable as unit + reusable across workspaces). Two-tier classification (cross-archetype vs domain-anchored). Edge cases (empty specialist for KG deployments; workspace-instance content; hyper-niche topics; composite specialist deferred D5).
  3. **Department demoted** from pattern primitive to optional `groupings: dict[str, list[specialist_id]] | None` shape on workspace.md (deployment-instance optional grouping convention). Convention name documentation-only (PBS-Schulz uses "departments"; legal practice may use "practice-areas"; flat deployments use `{}`).
- **Sub-DR B** (`docs/decisions/positioning-three-tier-framework.md` NEW; status ACCEPTED): downstream strategic implications:
  1. **Three-tier framing locked** (Infrastructure / Workspace / Specialist).
  2. **ICP refinement**: PBS narrow (consulting + workspace templates per archetype); framework broader (marketplace serves all archetypes including non-practitioner).
  3. **Three deployment possibilities → four**: specialist authoring tier added between consulting (T1) and workspace template productization (T3).
  4. **Marketplace shape locked**: of SPECIALISTS, not workspaces. Architectural constraints locked Sub-DR B (specialist Pydantic shape, skill defs, entity schemas, process entities, references, event subscriptions, substrate compat, deps, version); v3 mechanics (auth, pricing, governance, deprecation) deferred.
  5. **Strategic positioning rewrite**: "AI office for expert practitioners" → "Composable AI work infrastructure for practitioner workspaces."

- **ARCHITECTURE.md v0.30 → v0.31**: version log entry; reference card rows updated (specialist scope axis, workspace.md schema, namespacing); "Office-vs-department distinction" section rewritten to "Workspace-vs-specialist distinction"; meta-rule 1 renamed "app vs office" → "app vs workspace" with body update; meta-rule 3 invalidation contract updated (`departments_active` → `specialists_active`); pattern-vs-instance test examples (legal-practice / research-paper-review / engineering-doc / medical-records / regulatory-filing) renamed office → workspace.

- **VISION.md substantial cascade**: thesis line ("AI office pools..." → "AI workspace pools and leverages codified expertise (bundled as specialists)..."); "Office vs department" section rewritten as "Workspace shapes" per Sub-DR A; "Three deployment possibilities" → "Four deployment possibilities" per Sub-DR B (specialist authoring tier added); "AI-office builder" references → "AI-workspace generator"; expert-practitioner survives unchanged (per Sub-DR A's Specialist naming choice; user clarified this is naming-only, not architectural).

- **ROADMAP.md**: #22 collapsed to shipped-summary with full migration cascade list + downstream constraint flowing to #11/#9/#6/#14/Phase 1/v2/v3; v2 "AI-office builder" → "AI-workspace generator" with body rewrite; v3 "Marketplace as v3 horizon" sharpened to "Marketplace of specialists" with architectural constraints locked Sub-DR B.

- **`docs/strategic-positioning.md` substantial rewrite**: core positioning section sharpened with three-tier framing + IP list expanded (Specialist authoring added); marketplace strategic arc section rewritten per Sub-DR B (marketplace = of specialists); competitive landscape multi-department-office references → multi-specialist workspace.

- **DR cascade (header notes; full content sweep deferred to #11 single-touch refactor)**:
  - `office-vs-department.md`: header note (NAMING SUPERSEDED) + per-primitive rename table; structural decisions remain valid.
  - `office-level-managed-entities.md`: header note (NAMING SUPERSEDED — "Office-level" → "Workspace-scope"); file rename deferred (cross-refs across multiple files).
  - `substrate-protocol-design.md`: SpecialistDescriptor Pydantic Protocol added to common Substrate Protocol surface (per Sub-DR A); session 13 amendment header note.

- **`docs/conventions/entity-md-spec.md`**: header note (NAMING SUPERSEDED); type namespacing examples + scope axis enum updated (`department` → `specialist`; `office` → `workspace`); full sweep across remaining sections deferred to #11.

- **Memory `feedback_propose_before_commit.md` REFINED** (session 13 user clarification): supersedes prior formulation. NEW rule: approval needed at DECISION phases (positions, framings, choices); markdown-content phase NOT requiring per-content approval. AI writes markdown directly post-decision-lock; user reviews diff in commit if desired.

**Decomposition trigger empirically validated**: skill says >3 rounds at decision-design phase signals decomposition. Round 3 surfaced ~26 refinements integrating; Round 4 was offered as decomposition trigger; user accepted; 2-way decomposition (NOT 3-way; terminology + primitive are tightly coupled) chosen for Pareto reasons. Per-sub-DR sharpening rounds skipped post-decomposition (Round 3 covered the surface; per-sub-DR rounds = diminishing returns).

**What's deferred to #11 single-touch refactor**:
- Full DR cascade s/department/specialist + s/office/workspace across remaining ~10 DRs (ai-as-runtime-hybrid-shape worked examples; governance-and-identity-sourcing; skill-expert-agent-and-domain-knowledge clarification note; substrate-agentic-framework references)
- All 19 skill `specialist:` frontmatter sweep
- File path migrations (`extensions/department/<dept>/` → `extensions/specialists/<id>/`; `extensions/office/` → `extensions/workspace/`)
- Backend Pydantic class renames (`DepartmentEntity` → `SpecialistEntity`; `OfficeEntity` → `WorkspaceEntity`)
- AuditEvent schema field add (`specialist_id`)
- `office-config.yaml` → `workspace.md` migration (also adopts hybrid-shape per #16)
- env var renames (`PBS_OFFICE_CONFIG` → `PBS_WORKSPACE_CONFIG`)
- skill renames (`setup-office` → `setup-workspace`; `integrate-department` → `integrate-specialist`)
- plugin-conventions.md specialist concept section (deferred to #11 plugin-shape rework)

**What's next (session 14+)**:
- **#19 + #20** still pending (substrate evals — LlamaIndex pluggable RAG eval; PydanticAI eval). Both NEAR-BLOCKING for Bundles B/C/D/E design + Phase 1 corpus.
- **Bundles B/C/D/E design** (substrate-agnostic per session-11 framing) can proceed in parallel with #19/#20.
- **#9 implementation** waits for #19/#20 + Bundle design + #11 deferred cascade items.

---

## Session 12 — #18 substrate eval shipped + Tier 3 reframing + #21 SDK deep-read scaffolded

End of session 12 (2026-04-30). Max-effort session compressed 3-session scope (12-14) into single session: framing + 9 disqualifying criteria + screen against 10 candidates (8 original + 2 chronologically-valid additions: Claude Agent SDK + Strands) + verification pass + deep-eval + recommendation locked.

**What shipped session 12** (commit `2a8dfb5`):

- **Substrate decision** (`docs/decisions/substrate-agentic-framework.md` NEW; status ACCEPTED): **Claude Agent SDK adopted as primary substrate (full backend + frontend = Cowork plugin via #11) + Microsoft Agent Framework adopted as second backend (full backend; Path B frontend deferred to consulting signal — D5)**. Substrate-pluggability via explicit `Substrate` Protocol — NEW architectural pattern (Pydantic Protocol; substrate-coupling in core code impossible-by-construction per Make-wrong-shapes-impossible v0.21). Pattern: "Dual-substrate full-backend, single-frontend ship".
- **5 frameworks DISQUALIFIED** with concrete reasoning + counter-arguments engaged: Semantic Kernel + AutoGen (subsumed by MS AF); CrewAI (3 criteria fail — hybrid-shape + sparring + heaviness); Smolagents (no scale-up — would force re-implementation at upper tiers); OpenAI Swarm (vendor-lock + MCP secondary); LangGraph (criterion 2 fail post-deep-eval — PromptTemplate-centric, not runtime-fueled markdown bodies; same architectural problem as CrewAI).
- **Tier 3 reframing per pattern-vs-instance discipline**: previously Gemini-Enterprise-specific; now "enterprise multi-agent A2A platform" with Gemini Enterprise (canonical exemplar) / Azure AI Foundry / AWS Bedrock AgentCore as instances. Applied to: ROADMAP three-tier table + "Tier 3 platform port" section; `docs/decisions/a2a-and-gemini-pattern-emulation.md` (reframing note added); `docs/strategic-positioning.md` "Multi-archetype credibility" section sharpened with substrate-pluggable framing.
- **ARCHITECTURE.md v0.29 → v0.30** version log entry: substrate-pluggability discipline + Substrate Protocol NEW pattern + Tier 3 reframing.
- **#21 SDK deep-read** scaffolded as new BLOCKING-or-near-blocking commitment (in ROADMAP BLOCKING SUBSTRATE EVALUATIONS section): clone Claude Agent SDK + MS AF locally; structured code-read; output `docs/decisions/sdk-deep-read.md`. Verifies deep-eval claims with code-level evidence; informs Substrate Protocol shape with actual SDK API patterns.
- **Memory `feedback_propose_before_commit.md`** added — process feedback captured: for substantive PBS architectural content (decision records, ARCH/VISION/ROADMAP edits), propose structure + key positions in chat first; commit to file only after user approval.

**Counter-consideration surfaced session 12** (load-bearing for the recommendation):
- **Runtime shape (Shape A vs Shape B)**: Claude Agent SDK + hand-rolled = Shape A (Claude IS the runtime via Claude Code); MS AF + Strands + LangGraph = Shape B (Python program IS the runtime). Adopting MS AF as primary = architectural shape pivot away from Cowork integration.
- **Model-swap-ability**: Shape A locked to Claude (matches existing Tier 1-2 architecture); Shape B trivial multi-provider swap. Tier 3 = different archetype = different substrate is the documented escape valve for non-Claude.
- **Tier 3 implications**: MS AF natively supports Tier 3 archetype → forces pattern-vs-instance reframing of Tier 3 from Gemini-specific to platform-agnostic.

**What also shipped session 12**: **#21 SDK deep-read** (commit `1c1be3d`) — `docs/decisions/sdk-deep-read.md` (NEW; status ACCEPTED). Cloned both substrate SDKs; code-read public API surfaces + structures; verified #18 deep-eval claims; surfaced 4 refactor opportunities (R3a-R3d) + Substrate Protocol design refinement (narrower common surface + per-substrate extension Protocols). Plus **#22 terminology + level-boundary re-evaluation** scaffolded as next dedicated session work.

**Session 12 IN-PROGRESS work** (may carry to next session if context overflows): SDK findings adoption-decision discussion. Plan: R3a (in-process MCP) → R3b (MS AF eval primitives) → R3c (permission primitives → governance/sparring) → R3d (subagents-as-skills) → Substrate Protocol common surface iteration. Key insight defusing initial Protocol-shape worry: business logic is ~80% substrate-portable (skills + Pydantic + MCP gates + audit-trail + persistence + hybrid-shape); substrate-specific value-adds are leverage opportunities not constraints. Substrate-pluggable claim holds for load-bearing core.

**R3a + R3b + R3c PERSISTED as separate DRs** (commits `c061c5e` + amendments): `in-process-mcp-server.md` (TransportMode + MCPServerHandle + discovery API + governance for registration + observability — M1-M11 round 2); `eval-framework-adoption.md` (hybrid MS AF + scenarios as entities + S1-S4 schema fields); `permission-abstraction.md` (unified request_permission + 7 PermissionDecisionKinds + Permission/Quality gates distinction + T1-T8). Each underwent 2-round sharpening (full monty + dedicated round 2 pass). Round 2 yielded 4-11 substantive refinements per decision — validates pre-decision sharpening pattern.

**META-INSIGHT (captured in `memory/feedback_pre_decision_sharpening.md`)**: pre-decision sharpening rounds consistently outperform post-mortem audits/reviews. 5 mechanisms documented (anchoring bias / sunk-cost protection / sparring vs validation mode / fresh-context advantage / greenfield-still-anchored problem). Per VISION axis 2: pre-decision sharpening IS the sparring mechanism applied to architectural decisions; audits are validator-mode by construction.

**REFINED session 12 R3d round 3**: USER-TRIGGERED rounds outperform AI-self-triggered rounds. AI-self-driven sharpening tends toward Pareto-comfort + self-validation bias; user-trigger introduces external-perspective friction that forces AI past comfort. Refined pattern: round 1 (AI full monty proactive) + round 2+ (USER-TRIGGERED only; no AI-volunteered). Validated empirically — R3d AI-self round 2 felt comprehensive but user-triggered round 3 surfaced 5 substantive + 4 smaller refinements including NEW architectural pattern (per-substrate extension Protocols) + 2 R3c amendments.

**FURTHER REFINED session 12 (two-phase pattern locked per user direction)**: rounds yield mostly EXPANSION (filling out coverage layer by layer) NOT REVISION (changing decisions). Genuine architectural revisions are rare (~10-20% of refinements). **Two-phase pattern**: (1) Decision-design phase = 2-3 rounds (1 initial + 1-2 user-triggered sharpening) → architecturally lock + persist DR; (2) Pre-implementation phase = additional user-triggered rounds at implementation-start moment → surface operational/runtime/deployment details + flow-back ~10-20% architectural findings as DR amendments. Validated empirically: R3a/R3b/R3c locked at 2 rounds; R3d at 3 rounds (broader architectural surface); Substrate Protocol synthesis at 3 rounds (broadest surface — round 3 mostly pre-implementation surfacing captured early). Memory updated.

**Substrate Protocol design DR PERSISTED** (session 12 final synthesis): `docs/decisions/substrate-protocol-design.md` — common Substrate Protocol surface (rounds 1+2 architectural lock) + per-substrate extension Protocols + common surface boundary criteria + boot/shutdown lifecycle + error hierarchy + tier-awareness + audit-trail integration circularity resolution; round 3 operational/runtime concerns clearly marked as PRE-IMPLEMENTATION SURFACING (early; head-start for #9 implementation phase). Architectural foundation for #9 implementation now locked.

**AI-as-runtime principle — target-ecosystem-aligned; empirical validation DEFERRED** (session 12 framing, refined via close-out meta-questions): within our target deployment ecosystems (Anthropic plugins / Claude Agent SDK / MS Agent Framework / Strands Skills — all 4 SKILL.md-converged), hybrid-shape IS the convergent industry pattern. Design choice is not at risk of friction within target ecosystems. Alternatives exist outside our target set (prompt-template-centric per CrewAI/LangGraph — both disqualified at #18 screen; pure-schema per Kubernetes/Airflow — pre-LLM pattern; pure-prose per RAG-only — loses contracts; encoded-rules-in-YAML — explicit SQL-DB-trap pattern we rejected via #16) but none are relevant to our deployment scope. **Empirical validation** (comparative measurement against alternatives) still deferred — convergent adoption ≠ validation per failure-mode-catalog cargo-cult risk. Validation triggers: Phase 1 corpus + first project bind (real workflow); first consulting deployment in different domain (cross-domain portability); Phase 0 item 5 testing methodology (measurement infrastructure). Watch-list item: AI-as-runtime principle empirical validation deferred to post-Phase-1-corpus + first cross-domain deployment.

**Sharpening skills PERSISTED — TWO skills per phase** (session 12 — meta-architectural deliverable):
- `plugin/skills/decision-design-sharpening/SKILL.md` v0.1.0 — Phase 1; fires at decision-formation moment before commit
- `plugin/skills/pre-implementation-sharpening/SKILL.md` v0.1.0 — Phase 2; fires at implementation-start moment after DRs locked; surfaces operational/runtime/deployment details; ~10-20% architectural flow-back to upstream DRs

Initially scaffolded as single skill `pre-decision-sharpening` then split into two (per session-12 user direction): different triggers + different deliverables + different audiences; per "Make wrong shapes impossible" — clear invocation surface per phase prevents wrong invocation. Shared methodology in `memory/feedback_pre_decision_sharpening.md` (single source; both skills reference). ROADMAP commitment #23 covers both skills + future elevation to global plugin marketplace. **Decomposition refinement locked**: >3 rounds at decision-design phase signals decomposition missing; 2-3 universal sweet spot per decomposed sub-decision (validated empirically across R3a-R3d + Substrate Protocol synthesis).

**Skill candidate to formalize**: `pre-decision-sharpening` meta-skill — proposed for dedicated post-substrate-eval-completion session (alongside #22 / #19 / #20). Composes with audit + design-review skills (which still serve drift-detection role) but operates UPSTREAM at decision-formation moment.

**R3d PERSISTED** (commit `692b88c` + this commit): `subagent-primitives-adoption.md` (case-by-case adoption + per-substrate extension Protocols pattern + common surface boundary criteria + subagent permission inheritance/identity/sparring chain affecting R3c). Round 1 + 2 + 3 incorporated.

**What's next** (session 13+):
- **#22 terminology + level-boundary re-evaluation**: NEXT dedicated session per ROADMAP queue. Cross-domain stress-test "office / department / expert-practitioner" terminology against multiple archetypes. Pre-RAG essential. **Session 12 user direction added candidate generalization to evaluate (captured in ROADMAP #22 entry)**: AI Office = blueprint pattern; Domain-defined Office = blueprint applied to domain (instance); Expert = first-class composable abstract capability employed by any office (composition relationship, not identity); experts can exist standalone, span multiple offices, be domain-anchored OR cross-domain. Stress-test list provided in ROADMAP.
- **Comprehensive doc review** (post-#22): Substrate Protocol pattern as ARCHITECTURE design discipline section (currently only in version log entry); reference card row for substrate-coupled vs substrate-agnostic; failure-mode-catalog updates if SDK exploration surfaces new modes; other DRs scan for any remaining Gemini-specific framings; Path B frontend + MS AF backend explicit ROADMAP placements informed by SDK deep-read findings.
- **#19 + #20** still pending (substrate evals).
- **Bundles B/C/D/E design** can proceed in parallel (substrate-agnostic per session-11 framing — confirmed by SDK deep-read: Pydantic + MCP + entity-md + audit-trail all transfer cleanly across substrates).

---

## Session 11 — pre-RAG queue re-ordering + sharp-defer audit

Session 11 re-ordered the pre-RAG queue and audited the v1.x
backlog under the sharp defer rule (see CORE OPERATING FRAME
above). Order is purely chronological now; instance-anchored
rationales removed.

**Chronological dependencies driving the queue:**

- **#9's generic entity gate is load-bearing for every later
  commitment** per #16's hybrid-shape principle. Building #11
  (`department.yaml`) or #15 (Client/Actor) before #9 forces
  per-loader hacks (the silent-convergence failure mode #16 is
  meant to prevent) or one-off gates that #9 has to refactor.
- **#15 (Client + Actor) needs #9's entity gate available** to
  land office-level entities through the canonical write path.
- **#6 (audit-trail v2 retrofit) references Actor.id** (per #15
  constraint); needs #15 first.
- **#11 (Cowork integration) is single-touch only after #6 + #7
  retrofits**: skills get touched once for retrofit + namespacing
  + plugin shape, not twice. Running #11 before retrofits = every
  skill touched twice.
- **#13 (deployment flexibility) needs #11's plugin shape settled**
  (pbs.local.md migration in #11) and **#15's Actor entity** for
  multi-user auth. Both produced earlier in the queue.
- **#8 (framing skill) codifies pattern-vs-instance reasoning
  produced by #9** — must follow #9.

The "examine stable schemas" rationale for #9-last predates the
session-9 reframe — #9 no longer extracts a universal core, it
designs the contract from scratch. See ROADMAP.md per-commitment
Order notes for full chronological rationale.

**Pre-RAG queue (revised session 12 — #18 SHIPPED; #21 + #22 added; queue compressed)**:
**~~#18~~ ✅ → #21 (SDK deep-read) → #22 (terminology + level boundaries re-eval) → #19 → #20 → Bundles B/C/D/E (substrate-informed design) →
#9 implementation → #15 → #6 → #7 → #17 → #11 → #13 → #8 → C →
D → Phase 0 → Phase 1+#14**.

**#18 ✅ SHIPPED session 12** (commit `2a8dfb5`): Claude Agent SDK + MS Agent
Framework dual-substrate adopted; Substrate Protocol NEW pattern; Tier 3
reframed per pattern-vs-instance discipline. See
`docs/decisions/substrate-agentic-framework.md` for full eval + recommendation.
**#21 NEW** (SDK deep-read) added session 12: clone both SDKs + code-read +
findings DR. Near-blocking for #9 implementation phase (Substrate Protocol
shape benefits from code-level evidence beyond docs).

#21 + #20 land before Bundle B's Layer-3 mechanism decision (PydanticAI may
inform that). #19 lands anytime before Phase 1 corpus (could run in parallel
with implementation work after #9). #21 + #19 + #20 are evaluation sessions
producing decision records; they don't displace existing commitments — they
decide HOW to implement them.

**Sharp-defer audit results (session 11)** — six v1.x backlog
items pulled forward to v1 pre-launch as framework infrastructure
required at first-bind for any consulting deployment:

- Tier 2 MCP cross-reference tools (`find_memory_docs_by_reference`,
  `find_manifest_entry`) → bundles with #7 scope
- Tier 3 MCP introspection tools (schema introspection helpers +
  per-project state queries) → bundles with #7 scope
- Schema migration framework for memory data records → bundles
  with #9 scope (entity gate IS the migration boundary)
- Boundary placement refinements from slice 14 (`dedupe_bausteine`,
  `record_baustein_use` MCP tools) → bundles with #6 scope
- Manifest Pydantic models from slice 15 → bundles with #9 scope
  (entity gate generalizes to manifests post-#16 hybrid-shape)
- #13 cross-tier migration tools (between deployment modes) →
  stays in #13, removed from "deferred to post-RAG"

**One scope reversal** — Bundle E (adapter Protocol shape) moves
back from "DEFERRED to #11" to **in #9 implementation**. The
Protocol interface is framework infrastructure; doesn't depend
on a concrete adapter consumer. Concrete adapters in #11
implement against the #9-produced Protocol.

**Activation skill** (`activate-department` + session-open
detection) lands in #9 implementation phase, not deferred to
#11. Framework infrastructure for any consulting deployment
with multiple departments at first bind.

---

End of session 10 (2026-04-29). This session executed pre-RAG
commitment **#16 (AI-as-runtime hybrid-shape contract)** —
single-session framing-pass work resolving the structured-vs-
markdown boundary for managed entities + manifests, before #11's
`department.yaml` format would lock the wrong choice. Same shape
as session 9's #12 work: decision record + ARCHITECTURE bump +
ROADMAP slot + downstream constraints.

**What shipped session 10**:

- **Decision record**: `docs/decisions/ai-as-runtime-hybrid-shape.md`
  — the principle ("AI is the runtime that fuses structured +
  markdown, not a bridging layer between them"), three-layer
  frontmatter contract (Layer 1 universal Pydantic base + Layer 2
  type Pydantic subclass + Layer 3 per-deployment deferred to #9),
  body conventions per entity type (recommended-not-enforced),
  resolution of "where do conditional rules live" (process-as-md,
  not entity-shaped), MCP gate generalization spec, worked
  examples (b-plan-begruendung, BauGB, adapter-mode Invoice), 6
  defers each with specific home + cost being avoided.
- **ARCHITECTURE.md v0.15 → v0.16**: new top-level discipline
  section "AI-as-runtime hybrid-shape principle" added (parallel
  to pattern-vs-instance + entity-elevation + glue-not-replacement).
  Version log entry. Boundary: structured for interfaces / identity
  / persistence / machine contracts; markdown for semantics / rules
  / domain knowledge / process descriptions.
- **ROADMAP.md commitment #16** inserted at position 1 of pre-RAG
  queue (BEFORE #11). Constraints flowed to #11 (department.yaml
  adopts hybrid-shape from inception, NOT pure YAML), #15 (Client
  + Actor entity definitions land as md files following the
  contract), #9 (gate generalization + body specs + doctypes
  migration + audit slice 21 + design-review target 12 all
  bundled), #6 (gate-side conformance check; AuditEvent format
  unchanged). Recommended next-session order updated.
- **Memory `feedback_ai_as_runtime.md`** added — captures the
  pattern correction: when AI processing is named as load-bearing
  pillar of an architecture, mirror the memory pattern (minimal
  skeleton + md body + AI as runtime); resist adding rule-encoding
  layers (even in prose) because that's the SQL-DB trap in
  disguise.

**What also shipped session 10 (followup — review-mechanism gap
addressed)**:

User question: "multiple audit + review passes have run — why
didn't this core gap surface?" Honest answer: existing audit +
design-review modes catch *deviations from named disciplines*;
neither catches *missing disciplines themselves*. Two new
design-review targets added to address this gap structurally.

- **Design-review target 12 (entity-md authoring conformance)** —
  named in #16 DR; full description added to
  `plugin/skills/design-review/references/scope-and-targets.md`.
  Validates Layer 1 + Layer 2 frontmatter + body-section presence
  per the entity-md spec. Implementation bundled with #9.
- **Design-review target 13 (pattern emergence / unnamed
  convergence)** — NEW. Discovery-mode lens: scan code for
  ≥2 surfaces converging on an unnamed pattern; flag for
  elevation to discipline. Catches "silent convergence" failure
  mode. First-run scheduled session 11+ (after #11 starts; light
  cadence).
- **Design-review target 14 (discipline-gap detection)** — NEW.
  Top-down lens: scan named disciplines vs failure-mode catalog;
  flag uncovered modes. Catches failure modes that haven't yet
  manifested as code-visible convergence. Reads
  `plugin/skills/design-review/references/failure-mode-catalog.md`
  (new — seeded with session-10 postmortem + literature-derived
  modes).
- **Failure-mode catalog**
  (`plugin/skills/design-review/references/failure-mode-catalog.md`):
  living document. Initial entries: silent convergence (covered),
  prose-in-block-scalars (covered), encoded-rules-when-AI-was-
  available (covered), SQL-DB-trap (covered), source-of-truth
  ambiguity (covered), config-vs-code drift (partial), hardcoded-
  instance-content (covered), vendor-lock (covered), cargo-cult
  (partial), monolithic skill (partial — evaluate), implicit
  contracts between skills (partial — evaluate), hidden global
  state (partial — re-evaluate post-#13), workflow-as-data
  (covered), premature entity elevation (covered), distributed-
  systems failures (n/a today; re-evaluate post-#13).
- **Entity-md spec doc** — `docs/conventions/entity-md-spec.md`
  authored as scaffold. Single source of truth for hybrid-shape
  contract implementation: file layout, Layer 1 frontmatter
  fields (every entity, snake_case + ISO 8601 dates +
  kebab-case ids), Layer 2 type frontmatter (scaffold per
  entity type, grows in during #9), body section conventions
  per type (h2 top-level, h3 sub, no h1), cross-ref syntax (no
  wikilinks), validation expectations. Replaces the placeholder
  `docs/conventions/entity-body-specs.md` referenced earlier
  in #16 DR.
- **Design-review skill version bump**: 0.8.0 → 0.9.0 (3 new
  targets named + new reference file added). SKILL.md description
  updated.

**Why this followup matters (review-mechanism gap analysis)**:

Hypothesis (now codified into target 13): three independent
surfaces (memory + skills + state.md) had been using
hybrid-shape for 6+ months without anyone naming it as
discipline. Audit checks against named disciplines; greenfield-
reframe asks "would we keep existing?"; neither asks "what
unnamed pattern is this codebase converging on?" The gap is
*architectural*, not a methodological mistake.

Target 13 (pattern emergence) + target 14 (discipline gap) are
the structural patch. First-runs scheduled in early sessions
post-#11 to validate the lenses on real codebase state.

**Migration timing per #16 (no urgent migration this session)**:

- `extensions/universal/doctypes.yaml` + per-domain `doctypes.yaml`
  → per-entity md files: bundled with #9.
- `extensions/{universal,domain,state}/references-manifest.yaml`
  → per-reference md files: bundled with Phase 1 corpus
  (`research-references` already touches every entry during a
  full refresh).
- `extensions/department/<dept>/department.yaml` (new file format,
  #11): adopts hybrid-shape from inception — never persisted as
  pure YAML to begin with.
- Audit slice 21 + design-review target 12 implementation:
  bundled with #9 (depends on entity gate existence).

**Carried forward — session 9 work** (not duplicated, see
prior history below for full detail). #12 office-vs-department
shipped session 9; #15 Client+Actor added session-9 followup #2;
ARCH v0.10 → v0.15 cumulative.

---

End of session 9 (2026-04-29). This session executed pre-RAG
commitment **#12 (Office-vs-department modularization)** —
primarily design work resolving the open architectural question
from session 7 about offices conflating with single departments.
Plus a session-8 followup that landed earlier in this window:
#14 Memory Bank added to the v1 commitment queue scheduled
alongside Phase 1 corpus.

**What shipped session 9**:

- **Decision record**: `docs/decisions/office-vs-department.md`
  — full per-question reasoning (skill classification, memory
  4th axis, cross-department coordination shape, office-config
  schema, setup integration, pattern-vs-instance check). 11
  refinements from second pass + 3 explicit defers with
  proper-home identification.
- **ProjectState schema addition**:
  `departments_active: list[str] = Field(default_factory=list)` —
  routing + audit-filter dimension. Smoke-tested: default empty,
  explicit list, YAML round-trip preserves.
- **ARCHITECTURE.md v0.10 → v0.11**: office-vs-department
  open-question section converted to resolved; meta-rule 3
  invalidation table updated for ProjectState; scope-orthogonality
  layering convention extended from 3 to 4 axes (department added).
- **ROADMAP.md commitment #12** collapsed to shipped-summary;
  downstream constraint notes propagated to #6, #9, #11, #14, and
  Phase 1 corpus work.

**What also shipped earlier in this window** (session-8 followup):
- **Decision record framing pass** on a2a-and-gemini-pattern-
  emulation.md — three multipliers (builder / consulting / mid-
  term cross-boundary scenarios) replace PBS-Tier-3-centric
  framing.
- **Decision record Rows 8 + 9** added — RAG/Grounding
  architecture (constraint for Phase 1) + Evaluation/Simulation
  Service (constraint for Phase 0 #5).
- **#14 Memory Bank** added to v1 commitment queue (selective
  retrieval over memory layer; Vertex Memory Bank-inspired).
- **v2 Agent Simulation** entry added.
- **#13 hardware-spec research note** persisted (Hetzner tier
  ladder CCX23 → CCX33 → GEX44 → GEX131 with ingestion-vs-serving
  split architectural pattern).

**Constraints recorded session 9 for downstream commitments**:

- **#6 (audit-trail v2 retrofit)**: skill retrofits MUST set
  `actor_kind` (per #10) AND pass `department:` arg to memory
  tooling (per #12). Gate-side `departments_active` update logic.
  `query_audit_trail` `department:` filter + cached
  skill→department registry.
- **#9 (Pattern-vs-instance split)**: ProjectState core/extension
  split MUST handle per-department phase tracking
  (`phases: dict[str, str]`) and per-department lifecycle. Project-
  as-long-running-entity itself is PBS-instance; project entity
  becomes an opt-in extension.
- **#11 (Cowork integration)**: skill `department:` frontmatter
  sweep (REQUIRED, no default); slash commands namespaced; office-
  config `departments.<name>` schema bump + migration; department
  yaml file format; `integrate-department` skill creation.
- **#14 (Memory Bank)**: `search_memory` accepts `department:`
  filter (defaults to calling-skill's department); LanceDB memory
  index includes department metadata.
- **Phase 1 corpus work**: `search_corpus` gains optional
  `department_filter:` arg (defaults to calling-skill's department).

**Defers from session 9** (per office-vs-department.md):
- D1: per-department phase tracking on ProjectState → #9 (still
  pre-RAG)
- D2: per-department lifecycle on ProjectState → #9 (still pre-RAG)
- D3: state.md migration to multi-dept shape → first-bind moment
  (academic; zero projects bound today)

Each defer has a specific home + a specific cost being avoided.
Per "Defer-instinct produces manufactured restraint" check: honest
defers, not YAGNI.

---

## Read order for next session

1. **This file (HANDOFF.md)** — current state
2. **`ARCHITECTURE.md`** — **v0.30 (session 12 — substrate-pluggability discipline + Substrate Protocol pattern + Tier 3 reframing)**. AI-as-runtime hybrid-shape discipline added (session 10, v0.16). Office-vs-department resolved (v0.11); scope-orthogonality 4 axes; meta-rule 3 invalidation includes ProjectState.departments_active. Sessions 11-12 also added: pattern-vs-instance sharp defer rule (v0.20); make-wrong-shapes-impossible discipline (v0.21); validation-gating systems-view doc (v0.22); ARCH disciplines greenfield review (v0.27); architectural-gap detection sweep + maintenance rule 6 (v0.28); per-DR internal gap detection + 2 backfill DRs (v0.29).
3. **`docs/decisions/substrate-agentic-framework.md`** — **session-12 LOAD-BEARING artifact (NEW)**. Substrate decision: Claude Agent SDK + MS Agent Framework dual-substrate; Substrate Protocol NEW architectural pattern; Tier 3 reframing per pattern-vs-instance discipline. **Read before tackling #21 (SDK deep-read), #9 (entity gate uses Substrate Protocol), #11 (Cowork integration uses Claude Agent SDK), #13 (substrate × deployment matrix).**
4. **`docs/decisions/ai-as-runtime-hybrid-shape.md`** — session-10
   load-bearing artifact. **Read before tackling #9** (which
   implements the generic entity gate + Layer-1/Layer-2 contract +
   entity-md spec). Three-layer frontmatter contract; body
   conventions per entity type; process-as-md.
4. **`docs/decisions/office-vs-department.md`** — session-9
   load-bearing artifact. Read before tackling #9 (managed-entity
   concept) and #11 (department modularization sweep).
5. **`docs/decisions/a2a-and-gemini-pattern-emulation.md`** —
   session-8 artifact. Per-row decisions + constraints. Rows 8-9
   added in session-8 followup.
6. **`docs/decisions/`** — other authoritative records:
   - `mcp-fallback-policy.md` (session 7, fail-closed corollary)
   - `trigger-convention.md` (session 7, concept labels)
   - `audit-trail-v2.md` (session 7, single-write supersedes v1)
   - `audit-trail-v1.md` (SUPERSEDED, header note)
   - `sparring-output-v1.md` (session 6)
   - `backend-{test-layout,logging,mcp-error-format}.md` (session 5)
7. **`docs/conventions/entity-md-spec.md`** — session-10 followup
   scaffold. Single source of truth for hybrid-shape contract
   implementation. **Read before tackling #9** (which fills in
   Layer-2 schemas + body specs per entity type).
8. **`ROADMAP.md`** — commitments #10 + #12 + #16 + **#18** shipped (session 12). #21 (SDK deep-read) NEW (session 12; near-blocking for #9 implementation phase).
   **Remaining pre-RAG queue (revised session 12)**: **#21 → #19 → #20 → Bundles B/C/D/E (substrate-informed) → #9 → #15 → #6 → #7 → #17 → #11 → #13 → #8 → C → D → Phase 0 → Phase 1+#14**. Generalize-and-publish in v1.x. AI-office builder + Agent Simulation in v2.
8. **`docs/plugin-conventions.md`** — §11 (triggers) + §11b
   (fail-closed fallback policy)
9. **`VISION.md`** — pioneer-instance milestones
10. **`docs/audits/`** + **`docs/design-reviews/`** — first runs
11. **`docs/rag-pipeline-decisions.md`** — Phase 0/1/2/3/4 phasing
12. **`docs/backend-conventions.md`** — backend idioms
13. **`plugin/CLAUDE.md`** — meta-rule 4 summary
14. **`plugin/skills/audit/`** — **0.9.0** (slice 20 added; slice
    21 entity-md conformance scheduled with #9)
15. **`plugin/skills/design-review/`** — **0.9.0** (targets
    12 + 13 + 14 added session 10 followup; target 12 first-run
    bundled with #9; targets 13 + 14 first-runs scheduled
    sessions 11-12 to validate lenses on current codebase)
16. **`plugin/skills/orchestrator/`** — **0.10.0**
17. **`backend/mcp-server/src/pbs_mcp/audit_trail.py`** —
    session 8 schema with ActorKind + new fields + cross-ref
    validator
18. **`backend/mcp-server/src/pbs_mcp/project_state.py`** —
    session 9 `departments_active` field; will refactor to
    `extensions/department/planning/entities/project.md` per
    #16 + #9
19. All other 16 skills — session-7 versions snapshot still
    current (no skill bodies touched sessions 8, 9, or 10)

---

## ⏳ Pre-RAG gating items (post-session-10 — #16 shipped)

**#10 ✅ shipped session 8.** **#12 ✅ shipped session 9.**
**#16 ✅ shipped session 10** (AI-as-runtime hybrid-shape contract).
**#14 (Memory Bank) added session-8 followup.** **#15 (Client +
Actor) added session-9 followup #2.**

**Recommended execution order (session 11, sharp-defer amended)** —
chronological dependency chain. #9 + #15 + #6 + #7 + #17 sequence
the queue ahead of #11 + #13 because (1) the generic entity gate
(#9) is load-bearing for every later commitment, (2) #11 touches
every user-facing skill once-only after #6/#7 retrofits land
(single-touch refactor — running #11 first means double-touching
every skill), and (3) #13 binds to #11's plugin shape and #15's
Actor entity for multi-user auth. See ROADMAP.md per-commitment
Order notes for full chronological rationale.

```
Session 12-14: #18 (agentic framework substrate eval — multi-framework + heaviness) 2-3 sessions
Session 15:    #20 (PydanticAI eval)                                                  1 session
                   ← #18 + #20 produce decision records;
                     Bundle B Layer-3 mechanism informed by #20
Session 16-17: #19 (LlamaIndex pluggable RAG eval)                                    1-2 sessions
                   ← can also run in parallel with #9 design;
                     must complete before Phase 1 corpus
Session 12-21: #9  (Department contract + managed-entity + generic entity gate
                   + Bundle E + activation skill + schema migration framework
                   + manifest Pydantic models) 5-6 sessions, BUT:
                   - Bundles B/C/D/E DESIGN can proceed in parallel
                     with #18/#19/#20 (substrate-agnostic)
                   - Bundle A: dept module + location/registration   (~1 session)
                   - Bundle B: entity gate + Layer 3 (Layer-3 informed by #20)  (~1 session)
                   - Bundle C: ProjectEntity migration + phase/lifecycle  (~1 session)
                   - Bundle D: office-config schema additions         (~0.5 session)
                   - Bundle E: adapter Protocol shape (restored)      (~0.5 session)
                   - Implementation (Pydantic + gate + migrations
                     + activation skill + schema-migration framework
                     + manifest Pydantic) 2 sessions — WAITS for #18 outcome
Session 22-23: #15 (Client + Actor as office-level managed entities)              1-2 sessions
Session 24-27: #6  (audit-trail v2 retrofit + dedupe_bausteine + record_baustein_use
                   + CloudEvents conformance evaluation per #10) 3-4 sessions
Session 28:    #7  (bootstrap-write MCP tools + Tier 2/3 cross-ref + introspection) 1-2 sessions
Session 29:    #17 (MCP gate coverage comprehensiveness review)                   1 session
Session 30-34: #11 (Cowork integration refactor + concrete adapter implementations) 3-5 sessions
Session 35-37: #13 (deployment flex + Coolify reference + cross-tier migration tools) 2-3 sessions
Session 38-39: #8  (pre-action framing skill)                                     1-2 sessions
Session 40+:   C (sparring-output integration) → D (plugin version bump)
Then:          Phase 0 items 4 + 5 → Phase 1 corpus + #14 (Memory Bank bundled)
```

### Already shipped (architectural backstops)

1. ✅ **Unified audit trail v1** — schema + Pydantic + 2 MCP
   tools shipped session 6.
2. ✅ **Sparring-output structural promotion** — schemas + MCP
   tool + plugin-conventions field shipped session 6.
3. ✅ **State.md MCP gate** — Pydantic + 2 MCP tools shipped
   session 6. **Skill retrofits done session 7.**
4. ✅ **Fail-closed corollary** — done session 7.
5. ✅ **Trigger-convention simplification** — done session 7.
6. ✅ **Audit-trail v2 decision** — record done session 7;
   implementation deferred to commitment #6 (in remaining queue).
7. ✅ **A2A schema compatibility + Gemini Enterprise pattern
   emulation** — **done session 8**. Decision record + AuditEvent
   schema additions + ARCHITECTURE bump.
8. ✅ **Office-vs-department modularization** — **done session 9**.
   Decision record + ProjectState schema addition + ARCHITECTURE
   bump.
9. ✅ **AI-as-runtime hybrid-shape contract** — **done session 10**.
   Decision record + ARCHITECTURE bump (v0.15→v0.16) + ROADMAP
   commitment #16 + downstream constraints to #11/#15/#9/#6.
   Three-layer frontmatter contract (universal Pydantic base +
   per-type Pydantic subclass + per-deployment deferred). Body
   conventions per entity type, recommended-not-enforced.
   Process-as-md, not state-machine-as-data.

### Remaining for next-immediate-session-before-RAG

**#9 — Department module contract + managed-entity concept +
generic entity gate** (ROADMAP commitment #9) — **POSITION 1 in
remaining queue (revised session 11)** — **CURRENT WORK**:

- **Mission**: design the department module contract +
  managed-entity concept with two delivery modes (native +
  adapter-delegated). Produces the generic
  `read_entity` / `write_entity` MCP gate with `type:`-field
  dispatch to Layer-2 Pydantic subclass — load-bearing for every
  later pre-RAG commitment.
- **Why position 1**: #16's hybrid-shape principle made the
  generic entity gate load-bearing. Building #11 (`department.yaml`)
  or #15 (Client/Actor) before #9 forces per-loader hacks
  (creating exactly the silent-convergence failure mode #16
  prevents) or one-off gates #9 has to refactor.

- **Bundle structure (session-11 reorganization, sharp-defer
  amendment)**: scope expanded from 2-3 sessions to **5-6
  sessions** to handle 7 coupled open decisions properly + Bundle
  E (adapter Protocol shape, restored) + activation skill +
  schema migration framework + manifest Pydantic models.
  Restructured as 5 design bundles + implementation.

  | Bundle | Decisions | Status |
  |---|---|---|
  | **A** — Department module + location/registration | `extensions/department/<dept>/` package layout; `department.md` registration file shape; `path_pattern` declarations; gate's department-discovery mechanism | **In progress (session 11)** |
  | **B** — Entity gate + Layer 3 | `read_entity`/`write_entity`/`list_entities` signatures, error model, body-preservation, cross-ref validation tightness; Layer 3 mechanism (Option C `metadata: dict` is leading position — but see "metadata rename gap" consideration below) | Pending |
  | **C** — ProjectEntity migration + phase/lifecycle | ProjectState → ProjectEntity field-by-field plan; `phase: str` → `phases: dict[str, str]`; `lifecycle: Lifecycle` → `lifecycle: dict[str, Lifecycle]` | Pending |
  | **D** — Office-config schema additions | `departments.<name>.entities.<entity>.{mode,adapter,config}` shape; override-layer pattern with department.md | Pending |
  | **E** — Adapter Protocol shape (Gap B) | subscribe vs poll vs both; Pydantic Protocol interface | **In #9** (Protocol design is framework infrastructure; concrete adapters in #11 implement against it) |

- **Per #12 constraints** (lands in Bundle C): per-department phase
  tracking (`phases: dict[str, str]`), per-department lifecycle
  (`lifecycle: dict[str, Lifecycle]`), Project-as-long-running-
  entity opt-in per department.
- **Per #16 constraints** (split across bundles): generic entity
  gate (Bundle B) + Layer-1/Layer-2 Pydantic contract finalized
  (Bundle C) + `docs/conventions/entity-md-spec.md` updates + audit
  slice 21 + design-review target 12 implementation + migration of
  `extensions/universal/doctypes.yaml` (implementation phase).
- **Bundle B — metadata rename gap consideration** (session-11
  sanity-check finding, persist for Bundle B's deliberation):
  Layer 3 Option C (`metadata: dict[str, Any]` escape hatch) has
  a real cost beyond "no type safety" — there's also **no
  rename/migration support for custom fields**. If a deployment
  uses `metadata` heavily and wants to rename a key (e.g.,
  `metadata.review_status` → `metadata.internal_review_status`),
  no automatic mechanism updates existing entities. Pydantic
  doesn't validate `metadata` contents, so cross-ref validation
  doesn't catch orphans. This is a real cost of Option C to weigh
  against Options A (Pydantic subclass — typed + migratable but
  requires Python) and B (declared `extra_fields` — typed +
  migratable + no Python, at the cost of a YAML type DSL).
  Audit slice 21 could detect orphaned-key telemetry post-#9, but
  no in-architecture migration mitigation. Bundle B should weigh
  this when locking Layer 3 mechanism. NOT an automatic
  disqualifier for Option C — the rename cost may be acceptable
  if `metadata` use stays light. Just flag explicitly so the
  decision is informed.

- **Bundle A — LOCKED (session 11)**: shape stress-tested against
  three-test verification (cross-industry / office-level entity
  consistency / prose-rules-fit) and locked. Decisions:

  | Question | Decision |
  |---|---|
  | `department.md` Layer 2 frontmatter | `managed_entities`: keyed map of `dict[str, ManagedEntityRegistration]`. Each registration carries `pydantic_class: str` (dotted path) + `instances_at: str \| None` (path pattern, native mode) + `adapter: str \| None` (adapter id, adapter mode). At-least-one-of `{instances_at, adapter}` validator. |
  | Discriminator native vs adapter | Presence of `adapter:` field. No separate `mode:` field (avoids redundancy + Pydantic discriminated-union by field-presence). |
  | Type-name namespacing | **`type: <scope-id>.<short-name>`** (e.g., `planning.project`, `office.actor`, `universal.reference`). Per "Make wrong shapes impossible" discipline (ARCH v0.21) — collision impossible by construction across departments. Registration files use SHORT form as key; gate composes full namespaced form. See entity-md-spec §3.2. |
  | Package layout | **Recommended convention** (NOT gate-enforced — gate dispatches on `instances_at` paths only): `extensions/department/<dept>/`: `department.md` (registration + prose body), `entities/<type>.py` (Python module per Pydantic class, singular), `<types>/<id>.md` (md instance dirs, plural per non-project-axis types). NO per-department `projects/` dir — project entities live at `<project-root>/state.md` (project axis). Layout-flexible deployments (e.g., co-located Pydantic + md) can deviate; audit slice may warn on convention drift but gate doesn't reject. Per ARCH v0.23 ultrathink-review clarification — package layout is convention, not structural. |
  | Discovery | Gate startup: read office-config `departments_active` → load each `extensions/department/<dept>/department.md` → load `extensions/office/office.md` (always) → load `extensions/universal/universal.md` (always) → unified `type:` dispatch table built. No glob auto-discovery; `departments_active` is source of truth. Activation flow is conversational (skill orchestrates load+validate+append+audit). |
  | Body sections (`type: department`) | Recommended: `## What this department does` / `## Conventions` / `## Cross-department coordination` (when applicable). Same shape for `type: office` / `type: universal` registration files. |
  | Office registration filename | `extensions/office/office.md` (symmetric with `department.md`). Distinct from deployment-specific `office-config.md` / `pbs.local.md` (per #11 migration). |
  | Universal registration filename | `extensions/universal/universal.md` (symmetric — surfaced explicitly per ARCH v0.23 ultrathink-review; was inferred-by-symmetry in original close-out). |
  | `type: department` Pydantic class | `DepartmentEntity` extending `EntityBase` (Layer 2). Fields: `managed_entities: dict[str, ManagedEntityRegistration]`. Pydantic class definition lands with #9 implementation. |
  | `type: office` Pydantic class | `OfficeEntity` extending `EntityBase` (Layer 2). Fields: `managed_entities: dict[str, ManagedEntityRegistration]`. Same shape. |
  | `type: universal` Pydantic class | `UniversalEntity` extending `EntityBase` (Layer 2). Fields: `managed_entities: dict[str, ManagedEntityRegistration]`. Same shape (added explicitly per ARCH v0.23 ultrathink-review). |
  | Activation skill (`activate-department`) | In #9 implementation phase. Validates candidate `department.md` against `DepartmentEntity` Pydantic; conflict-checks managed-entity type names against active departments (collision impossible per namespacing — but adapter id collision still a real check); appends to `departments_active`; emits `department_activated` AuditEvent with `convention_applied` field per governance-and-identity-sourcing decision 4. Session-open sub-skill globs `extensions/department/*/` vs `departments_active`, surfaces candidates. |

  **Worked example** — `extensions/department/planning/department.md` Layer 2 frontmatter:

  ```yaml
  managed_entities:
    project:
      pydantic_class: extensions.department.planning.entities.project.ProjectEntity
      instances_at: "<project-root>/state.md"
    doctype:
      pydantic_class: extensions.department.planning.entities.doctype.DoctypeEntity
      instances_at: "extensions/department/planning/doctypes/{id}.md"
    process:
      pydantic_class: extensions.department.planning.entities.process.ProcessEntity
      instances_at: "extensions/department/planning/processes/{id}.md"
  ```

  Adapter-mode example (e.g., `extensions/department/invoicing/department.md`):

  ```yaml
  managed_entities:
    invoice:
      pydantic_class: extensions.department.invoicing.entities.invoice.InvoiceEntity
      adapter: lexware
  ```

- **Bundle A → Bundle B handoff**: shape locked; package layout
  + discovery + body conventions all decided. Move directly into
  Bundle B (entity gate + Layer 3 mechanism). Bundle B test list:
  - Layer 3 mechanism options (A: Pydantic subclass / B: declared
    `extra_fields` / C: `metadata: dict`) — including the
    metadata-rename-gap consideration captured below.
  - Cross-ref validation tightness at `read_entity` / `write_entity`.
  - Body-preservation across read/write cycles.
  - Error model for gate failures.

- **Session-11 unresolved threads** (now resolved + persisted):
  - **Governance scaling + identity sourcing + prose-rules**: all
    three architectural directions captured in
    `docs/decisions/governance-and-identity-sourcing.md` (session
    11). ROADMAP commitment #13 references the record; entity-md-
    spec §3.1 added for identifier uniqueness conventions.
    Implementation lives across #9 (Bundle A consistency), #15
    (Actor adapter Protocol), #6 (approval events for governance),
    #13 (tier-conditional gate enforcement).
  - **`docs/what-this-is.md` shipped session 11** (commit
    `0bbd07f`): outsider-shareable framing doc for friend / potential
    consulting collaborator. Iterated through honest-framing pass.
    See file for content.

**#15 — Office-level managed entities (Client + Actor)** (ROADMAP
commitment #15) — **POSITION 2 in remaining queue (revised
session 11)**:
- Office-level managed entities concept introduced —
  `extensions/office/entities/<entity>.py` (parallel to
  `extensions/department/<dept>/entities/`).
- **Client** Pydantic schema (native default) — referenced by
  Project (planning), Invoice (invoicing), Timesheet (PM), etc.
- **Actor** refactor — migrate from `office-config.actors[]`
  semi-typed config to first-class native managed entity. Identity
  primitive for #13's multi-user auth (which lands later in queue).
- Cross-department reference convention: entities hold
  `<entity>_id: str` fields; gate validates references exist;
  no FK enforcement at storage layer.
- **Per #16 constraint**: Client + Actor land as md files at
  `extensions/office/entities/clients/<id>.md` and
  `extensions/office/entities/actors/<id>.md`, following the
  three-layer frontmatter contract (using #9's generic entity
  gate).
- 1-2 sessions; AFTER #9 (gate available); BEFORE #6 (audit
  retrofit references Actor).

**#6 — Audit-trail v2 retrofit** (ROADMAP commitment #6) —
**POSITION 3 in remaining queue (revised session 11)** — per
`audit-trail-v2.md`, **scope expanded session-9 followup #2**:
- Backend: `record_decision` + `render_audit_trail` tools;
  `user_confirmation` event kind; `reasoning_full_text` in
  decision/module_decision details; drop `phase_history` from
  ProjectState.
- **Per #10 constraint**: every retrofit explicitly sets
  `actor_kind` on every event.
- **Per #12 constraint**: every retrofit passes `department:` arg
  to memory tooling. Gate-side `departments_active` update logic
  + cached skill→department registry. `query_audit_trail`
  `department:` filter.
- **Per #15 constraint**: AuditEvent.actor references Actor.id
  (office-level managed entity); replaces today's free-form actor
  string with typed reference.
- **Per session-9 followup #2 (approval flows)**: add event kinds
  `approval_requested`, `approval_granted`, `approval_rejected`.
  Details payload: `approving_actor`, `policy_rule`, `subject_entity_id`.
- Skills: orchestrator + save-baustein + record-feedback +
  draft-textteil-b/c + review-draft + research-references retrofits.
- Migration: `backfill_audit_trail` walks legacy prose sources.
- 2-3 sessions.

**#7 — Bootstrap-write MCP tools** (ROADMAP commitment #7) —
**POSITION 4 in remaining queue (revised session 11)**:
- `create_manifest` + `create_office_config` (Pydantic-validated
  first-write through loader).
- `author-manifest` + `setup-office` skill retrofits.
- 1 session.

**#17 — MCP gate coverage comprehensiveness review** (ROADMAP
commitment #17) — **POSITION 5 in remaining queue (revised
session 11)**:
- Comprehensive sweep of all contract-bearing files / file types
  in the repo for gate presence + strictness. Slice 23 scaffolded
  if discoveries warrant (slice 22 is wrong-shapes-solvable scan
  per session 11; #17's slice number bumped accordingly).
- Surveys real gates produced by #9 + #15 + #6 + #7 (not
  yet-to-be-written ones).
- 1 session.

**#11 — Cowork as primary end-user runtime, DEEP integration**
(ROADMAP commitment #11) — **POSITION 6 in remaining queue
(revised session 11)**:
- Deep + complete integration directive: adopt Anthropic's plugin
  shape wholesale where it differs from ours.
- **Per #12 constraint**: all 19+ skills get `department:`
  frontmatter (REQUIRED, no default). Slash commands namespaced
  (`/<dept>:<skill>` — `/planning:draft-begruendung`,
  `/office:setup-office`, etc.). Office-config `departments.<name>`
  schema bump + migration co-located with `pbs.local.md`.
  `extensions/department/<dept>/department.yaml` file format
  implementation (using #9's generic entity gate). New
  `integrate-department` skill creation.
- **Per #10 constraint**: plugin agents emit events as
  `actor_kind="skill", actor_card=<agent-name>`.
- **Why position 6 (chronological)**: #11 touches every
  user-facing skill (namespacing, `<example>` blocks, plugin
  shape conformance). Running it before #6 + #7 retrofits =
  double-touching every skill (first for plugin shape, then for
  audit-trail v2 + bootstrap-write retrofits). Position 6 is
  single-touch — every skill gets one combined refactor pass
  using the already-final post-retrofit shape.
- 3-5 sessions; substantial refactor touching every user-facing
  surface.

**#13 — Deployment flexibility + Coolify reference deployment**
(ROADMAP commitment #13) — **POSITION 7 in remaining queue
(revised session 11)**:
- Pluggable persistence + auth + transport abstractions.
- **Per #10 constraint**: HTTP MCP transport implementation lands
  here. AuditEvent.user_id field for multi-user attribution. Data
  classification annotations.
- **Hardware spec persisted** (session-8 followup): start
  CCX23/CCX33 Hetzner Cloud, ingestion-vs-serving split (heavy
  compute on RTX 5090 local, rsync indices to cloud), upgrade-
  triggered to GEX44/GEX131 if needed.
- 2-3 sessions.

**#8 — Pre-action framing skill** (ROADMAP commitment #8) —
**POSITION 8 in remaining queue (revised session 11)**:
- Design + scaffold meta-skill (`frame-task` or `scoping`).
- Triggered on non-trivial task starts.
- **Order note**: AFTER #9 — codifies pattern-vs-instance reasoning
  produced by #9 into a repeatable check. Last in pre-RAG queue
  before C/D/Phase-0/Phase-1.
- 1-2 sessions.

**#14 — Memory Bank** (session-8 followup):
- `search_memory` + `read_memory_entry` MCP tools; LanceDB index
  over `memory/`; embedding job.
- **Per #12 constraint**: `search_memory` accepts `department:`
  filter (defaults to calling-skill's department).
- Bundled with Phase 1 corpus work — shares embedding
  infrastructure (bge-m3 + LanceDB + rerank).

### Sparring-output integration (still per v1 plan)

- `review-draft` declares `output_schema: ReviewOutput`; body adds
  Output Format section.
- `orchestrator` PROCEDURE Checkpoint 13 declares
  `RecommendationOutput` schema; calls `validate_skill_output`.

### Plugin version bump

- `plugin.json` 0.3.0 → 0.5.0 after #6/#7/#9 retrofits land.
  Run `bash dev-link.sh` after.

### Then — Phase 0 items 4 + 5

- **Phase 0 item 4 — Feature-survey skill**: greenfield-the-vision
  sibling to audit + design-review.
- **Phase 0 item 5 — Testing methodology + harness**: discussion-
  first. **Per #10 constraint**: design eval-result schema as
  Pydantic contracts (`EvalRun` / `Scenario` / `EvalResult` /
  `RegressionSuite`).

### Then — Phase 1 corpus download + #14 bundled

Fetch all 57 entries via `research-references` full refresh.
**No embeddings yet on corpus during fetch** — raw fetch +
checksum + manifest population. Embedding pass **runs locally on
RTX 5090** per #13's ingestion-vs-serving architectural pattern
(persisted in #13 hardware-spec note); LanceDB indices then rsync
to cloud serving node. Memory Bank index built on serving node
directly (continuous low-rate writes).

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis (canonical "why") |
| `ARCHITECTURE.md` | **v0.16** — AI-as-runtime hybrid-shape principle added (session 10); office-vs-department resolved (v0.11) + 4-axis scope-orthogonality |
| `ROADMAP.md` | 16 v1 commitments (#10 + #12 + #16 ✅ shipped); remaining queue + downstream constraints |
| `~/dev/reference/knowledge-work-plugins/` | Cloned Anthropic plugins repo for #11 study |
| `docs/decisions/ai-as-runtime-hybrid-shape.md` | **Session-10 deliverable** — three-layer frontmatter contract + body conventions per entity type + process-as-md + gate generalization spec + 6 defers |
| `docs/decisions/office-vs-department.md` | **Session-9 deliverable** — per-question decisions + downstream constraints + 3 defers |
| `docs/decisions/a2a-and-gemini-pattern-emulation.md` | Session-8 deliverable — 9 rows of decisions + multipliers framing |
| `docs/decisions/mcp-fallback-policy.md` | Session-7 fail-closed corollary |
| `docs/decisions/trigger-convention.md` | Session-7 concept labels |
| `docs/decisions/audit-trail-v2.md` | Session-7 reversal; supersedes v1 |
| `docs/decisions/audit-trail-v1.md` | SUPERSEDED |
| `docs/decisions/sparring-output-v1.md` | Session-6 v1 commitment |
| `docs/decisions/backend-{test-layout,logging,mcp-error-format}.md` | Session-5 backend records |
| `docs/audits/boundary-adherence-20260429.md` | Slice 14 first run (session 6) |
| `docs/audits/invalidation-contract-20260429.md` | Slice 15 first run (session 6) |
| `docs/audits/validation-gate-20260429.md` | Slice 16 first run (session 6) |
| `docs/design-reviews/vision-arch-coupling-20260429.md` | Target 8 first run (session 6) |
| `docs/design-reviews/foundations-20260429.md` | Session-5 design-review |
| `backend/mcp-server/src/pbs_mcp/audit_trail.py` | Session 8 — ActorKind + 3 new fields + cross-ref validator |
| `backend/mcp-server/src/pbs_mcp/project_state.py` | **Session 9** — `departments_active: list[str]` field |
| `plugin/skills/audit/` | **0.10.0** — slices 1-16 + 18 + 19 + 20 + 21 (slice 21 description scaffolded session 10 followup-3; first-run scheduled with #9 entity-md migrations) |
| `plugin/skills/design-review/` | **0.9.0** — targets 1-11 + 12 (entity-md authoring) + 13 (pattern emergence) + 14 (discipline gap); failure-mode-catalog.md added |
| `docs/conventions/entity-md-spec.md` | **Session 10 followup** — single source of truth for hybrid-shape contract: file layout + Layer 1 fields + Layer 2 scaffold + body conventions + cross-ref syntax |
| `plugin/skills/design-review/references/failure-mode-catalog.md` | **Session 10 followup** — living catalog of architectural failure modes + their named-discipline coverage status |
| `plugin/skills/orchestrator/` | **0.10.0** |
| `plugin/CLAUDE.md` | Updated meta-rule 4 summary |
| `docs/plugin-conventions.md` | §11 (triggers) + §11b (fallback policy) |
| `~/.config/pbs-bureau/office.yaml` | v3 (session 6 migration) |

---

## Skill versions snapshot (post-session 10 followup)

Session 10 followup bumped design-review 0.8.0 → 0.9.0 (targets
12 + 13 + 14 added; failure-mode-catalog.md added). All other
skills unchanged. Will change significantly in session 11+ when
#11 introduces `department:` frontmatter sweep + slash command
namespacing.

| Skill | Version |
|---|---|
| audit | **0.11.0** (slice 22 — wrong-shapes-solvable scan added session 11; first-run scheduled session 12+ for skill-body + ARCH sweep) |
| author-manifest | 0.4.0 |
| design-review | **0.10.0** (target 15 — prospective make-wrong-shapes-impossible check added session 11; first-run scheduled immediately on Bundle B Layer-3-mechanism decision) |
| draft-cover-mail | 0.6.0 |
| draft-textteil-b | 0.5.0 |
| draft-textteil-c | 0.5.0 |
| orchestrator | 0.10.0 |
| promote-to-skill | 0.5.0 |
| record-feedback | 0.4.0 |
| research-references | 0.5.0 |
| review-draft | 0.5.0 |
| save-baustein | 0.4.0 |
| setup-office | 0.6.0 |
| survey-project | 0.5.0 |
| validate-bausteine | 0.4.0 |
| validate-checklist | 0.6.0 |
| validate-latex-style | 0.5.0 |
| verify-citations | 0.5.0 |
| watch-list | 0.2.0 |
| plugin.json | 0.3.0 (will bump to 0.5.0 after #6/#7/#9) |

---

## MCP tools shipped session 9

None this session — schema-only addition to existing ProjectState.
The session-6 tools (5 new) + session-8 AuditEvent additions
remain the current backend surface. Backend tools planned for
next-immediate-session retrofit (per #11 + #6 queue):
- `record_decision` (audit-trail v2 — for #6)
- `render_audit_trail` (audit-trail v2 — for #6)
- `create_manifest` (bootstrap-write — for #7)
- `create_office_config` (bootstrap-write — for #7)

Schema-side, ProjectState gained `departments_active: list[str]`
defaulting to empty. Gate-side update logic (gate appends
department to list when event's `actor_card ∈ skills_in_dept`)
deferred to #6.

---

## Working-style notes (carried + new)

1. **Pre-action framing matters more than post-action review**
   (carried). Session 9 explicitly used the framing-pass pattern
   for #12: drafted in chat, reviewed once, refined once with
   explicit defer-instinct check, THEN persisted.

2. **Defensive pre-RAG schema additions are nearly free** —
   confirmed again session 9. ProjectState.departments_active
   was a 1-line Pydantic field + smoke-test, ~10 minutes of work.
   Migration cost post-data-accumulation would be a multi-skill
   retrofit.

3. **"No menus, commit to positions"** (carried). Session 9
   produced verdicts on each of 7 open questions; refinement
   pass added 11 more committed positions; defers explicitly
   named with proper homes.

4. **Defer-instinct check is now explicit discipline.** Session 9
   listed 3 defers, each named with specific home + specific cost
   being avoided. Per "feedback_defer_instinct" memory: not
   generic YAGNI — honest defers.

5. **Pattern-vs-instance discipline catches real coupling.**
   Surfaced in #12 refinement: project-as-long-running-entity is
   PBS-instance, not pattern-universal. Some offices (brand-voice,
   single-skill utilities) have no project entity. Constraint
   passed to #9 (Pattern-vs-instance split). Without the check
   we'd have shipped a pattern that doesn't actually generalize.

6. **Entity-elevation discipline (session-9 followup #2)**: prefer
   events + nested fields + memory entries over new managed entity
   types. Elevate to first-class managed entity only when stable-
   identity + state-of-record + lifecycle ALL apply. Avoids the
   architecture creeping toward an SQL schema (catastrophic for
   LLM-mediated AI offices). Right level: knowledge graph + document
   store with stable references, not Oracle. Demoted Approval from
   proposed managed entity to event-kinds on AuditEvent (folded
   into #6's scope). Future audit/design-review check (target 11)
   should scan for over-modeled entities. **Broader-review pass
   (session-9 followup #3)** confirmed zero major gaps in capturing
   common business workflows: 7 candidate concerns (document
   versioning, notifications, role-based actors, reports, conflicts,
   business calendar, knowledge depreciation) all resolved via
   existing infrastructure / scope expansion of existing commitments
   / defer-to-concrete-need / out-of-scope-per-pattern-vs-instance.
   No new commitment numbers added.
   **Infrastructure-primitive review pass (session-9 followup #4)**
   stress-tested core primitives (skills, managed entities, audit
   events, memory, integration adapters, cross-department
   coordination) against business-process expressibility. 9/9
   coverage after two genuine gaps fold into existing commitments:
   Gap A (proactive time-driven triggers → server-side scheduler
   in #13) and Gap B (adapter-emitted events for external state
   changes → adapter Protocol generalization in #9). No new
   commitment numbers.

7. **Memory captures**: existing 6 feedback memories carry
   forward. The "leave legacy behind" + "judgment-not-menus" +
   "defer-instinct" + "entity-elevation discipline" principles all
   paid off in this conversation cycle.

8. **Glue-not-replacement principle (session-9 followup #6)**: PBS
   is the glue/coordination layer that brings AI to existing
   infrastructure; not a replacement for BPMN engines / accounting
   tools / CRMs / calendars / etc. Generalizes meta-rule 1's
   integration-adapter pattern as the canonical mechanism. Different
   addressable market than vertical-SaaS-replacement plays. ARCH
   v0.14 → v0.15 codifies as top-level discipline. ROADMAP v1.x-v2
   gains BPMN-empowerment entry as concrete positioning. ROADMAP v2
   AI-office-builder gains marketplace-as-v3 subsection (concept
   only; decision deferred; v2 builder output format must be
   marketplace-compatible from start). New `docs/strategic-
   positioning.md` captures the full strategic framing for
   consulting positioning (open-source-as-edge / three-tier content
   strategy / glue-not-replacement / cognitive-load-reduction
   framing / three risks / revenue model / marketplace arc /
   competitive landscape).

---

## Session 9 commits (chronological)

| # | Commit | Theme |
|---|---|---|
| 1 | (this commit) | session 9: pre-RAG #12 shipped — office-vs-department modularization. Decision record + ProjectState.departments_active + ARCHITECTURE v0.10→v0.11 + ROADMAP collapse + downstream constraints for #6/#9/#11/#14/Phase-1. |

Plus session-8 followups landing earlier in this conversation
window:
- `b6faaa6` — A2A decision record framing pass (3 multipliers)
- `b8390d7` — Rows 8 + 9 (RAG/Grounding + Eval/Simulation gaps)
- `9aa6d8d` — #14 Memory Bank + v2 Agent Simulation
- `1c5837c` — #13 hardware-spec research note (Hetzner ladder)

All pushed to origin/main.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **Plugin cache symlink**: bump `plugin.json` AND re-run
  `bash dev-link.sh` after #6/#7/#9 retrofits.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Office-config**: v3 on disk; no `path_classification` block.
  v4 schema bump (departments) lands in #11.
- **No projects bound yet**: schema additions (AuditEvent fields,
  ProjectState.departments_active) are design-time-pending until
  first project bind.
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md`
  - `feedback_judgment_and_automate.md`
  - `feedback_push_after_commit.md`
  - `feedback_refine_pareto.md`
  - `feedback_defer_instinct.md`
  - `feedback_llm_instruction_tightness.md`
  - `feedback_vision_arch_grounding.md`
  - `feedback_ai_as_runtime.md` (session 10 — when AI processing is named as load-bearing pillar, mirror the memory pattern; resist rule-encoding layers even in prose)
