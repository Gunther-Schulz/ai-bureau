# Framework Inventory (this repo)

> Inventory pass per pivot decision (`5-PIVOT-DECISION.md`). Classifies framework artifacts by forward role for the Cowork-based PBS-Schulz deployment.

## Summary

- **~110 artifacts inventoried** across 7 categories: 4 anchor docs (VISION/ARCHITECTURE/MAINTENANCE/DISCIPLINES) + GLOSSARY (37 entry index + 36 per-entry files) + 11 ARCH topic files + 17 profile files + 5 dev skill bundles + 19 archived deployment skills + 7 Mode 2 reference Python impls + 25 formal decision records (`docs/decisions/*.md`)
- **Load-bearing for Cowork build**: VISION (three axes anchor), GLOSSARY (vocabulary), `arch/sparring.md` + `arch/audit.md` + `arch/claim-defensibility.md` + `arch/specialist-skill.md` (the 4 ARCH topics directly informing what custom SKILL.md files + MCPs must do), 5 dev skills (transferable as-is), the 19 archived 0.1.0 deployment skills (rewrite-target).
- **Top-3 most reusable conceptual frames**:
  1. VISION three-axis thesis (intertwining/sparring/authorship-preservation) + Vivienne Ming sparring grounding + defensibility test (the why)
  2. Sparring 8 sub-mechanisms + audit-trail-as-canonical-source + per-claim attestation chain (the load-bearing mechanism designs the empirical investigation must replicate or refute via Cowork)
  3. GLOSSARY vocabulary (workspace / practitioner / specialist / claim / work-unit / engaged-authorship / etc.) — already-precise terms reusable as conceptual frame for designing custom skills
- **Top-3 most salvageable code/skill artifacts**:
  1. The 19 archived `archive/plugin/skills/pbs:*` deployment skills (orchestrator / draft-textteil-b / draft-textteil-c / review-draft / validate-checklist / verify-citations / etc.) — these are the **frozen 0.1.0 versions still active per system reminder showing pbs:* skills loaded from `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0/`**. These are the closest-to-Cowork-authoring artifacts in the repo.
  2. The 5 dev skills (`plugin/skills/sharpen/`, `decision-design-sharpening/`, `pre-implementation-sharpening/`, `coherence-audit/`, `greenfield-rederivation/`) — domain-neutral; transfer to deployment repo as-is for design discipline on the Cowork work itself.
  3. `pbs/impls/practitioner_shape_sparring.py` (1182 lines) + `practitioner_shape_authority_binding.py` (408 lines) + `practitioner_shape_gate.py` (1196 lines) — concrete Python realizations of sparring + authority-binding + quality-gate; useful as REFERENCE for what equivalent SKILL.md authoring + custom MCP-tool logic must achieve, and potentially salvageable as helper modules.
- **Notable gaps**: no `STRATEGY.md` despite VISION cross-ref; no `arch/source-grounding.md` though source-grounding is named as Cond #3 of defensibility (it's referenced as forthcoming Phase 3.3 detail); no Cowork-specific deployment template — the framework anticipates substrate as Pattern A pluggability but never wrote a Claude-Cowork substrate-impl beyond the Mode 2 thin-slice.

## By artifact category

### Vision + thesis

| File | Lines | Carries | Forward role |
|---|---|---|---|
| `VISION.md` | 257 | Three-axis thesis + Vivienne Ming sparring foundation + defensibility test + falsification criteria + category-collapse warning + axis-1/2/3 robustness-to-AI-capability claim + foundations (Schön/Kahneman/Dreyfus + EU AI Act + professional liability frameworks) | **PRESERVE as conceptual frame** — the WHY remains intact regardless of pivot. Ming's three-mode finding + the defensibility test (six-months-later) are the load-bearing intellectual contribution. Reference at every Cowork design moment for "does this serve all three axes". |
| `ARCHITECTURE.md` | ~1100 | Layer 2 overview: Phase 3 status table (3.0-3.7) + 11 ARCH topic catalog + reading order + cross-cutting principles (Pattern A/B/C/D semantics, AI-as-runtime, LLM-instruction tightness, 4-mode logic placement, composite boot+shutdown sequence) + 14 locked architectural decisions | **PRESERVE as reference frame** — Layer 2 detail (substrate composite boot ordering / quality-gate fail-closed semantics / Mode 1-4 distinction) informs Cowork design but is not directly portable. The 4-mode logic placement (Mode 1 SKILL.md / Mode 2 substrate Python / Mode 3 specs / Mode 4 docs) is reusable framing for organizing Cowork artifacts. |
| `MAINTENANCE.md` | ~3500+ | TOP-LEVEL RULE (cascade discipline) + TOP-LEVEL ARCHITECTURE (framework=mechanisms, shape=policies, A-B-C scope model, Pattern A/B/C/D pluggability) + TOP-LEVEL DESIGN PRINCIPLES (wrong-shapes-impossible / pattern-vs-instance / preliminary-lock) + procedure-rigor discipline + 5-layer doc model | **MOSTLY DROP-FROM-SCOPE for deployment, PRESERVE the META-design principles**: §1 wrong-shapes-impossible / §2 pattern-vs-instance / §3 preliminary-lock are reusable for any rigorous design work. Cascade discipline + 5-layer doc model are framework-source-repo specific. |
| `DISCIPLINES.md` | 211 (index) + 11 per-discipline files in `disciplines/` | 11 cross-session disciplines: source-grounded / apply-uniformly / pre-decision-sharpening / cascade-prevention / no-defer / anchored-vs-preliminary / cascade-discipline / foundation-up / coherence-audit cadence / greenfield-evaluation / effort-switch | **TRANSFER as deployment-repo working procedure** — most disciplines (source-grounded with cite-or-read-or-flag, no-defer with D-gate, foundation-up ordering) are domain-neutral working hygiene that should govern the Cowork-deployment work too. Cascade-discipline + coherence-audit-cadence are framework-source-repo specific (drop). |

### Vocabulary

`GLOSSARY.md` (~166 lines index) + `glossary/` (36 per-entry files; load-on-demand; ~30-150 lines each).

**36 entries clustered**:

- **Foundational** (mechanism / policy / framework / shape / Framework-C-scope / Owner-B-scope / Layer-A-scope) — framework-source-specific A-B-C model; **drop-from-deployment** but preserve as design vocabulary
- **Compositional primitives** (workspace / substrate / specialist / skill / practitioner / session / workflow / work-unit / claim) — **HIGH REUSE for Cowork** — these are the entities the Cowork deployment manipulates; precise definitions transfer directly
- **VISION axes** (intertwining / sparring / authorship-preservation) — **PRESERVE** anchor concepts
- **Audit + event primitives** (actor / event / authority-binding) — **HIGH REUSE** — defines what custom MCP audit-tool emissions must look like
- **Pattern A primitives** (substrate / protocol-architectural / adapter / quality-gate) — framework-source pluggability; Cowork pivot collapses substrate question (always Anthropic), but adapter abstraction informs custom-MCP design
- **Modes & relations** (co-worker / intertwined-AI / tacked-on-AI / answer-machine-AI / oracle-AI / validator-AI / rubber-stamping) — **HIGH REUSE** — the failure-mode vocabulary names what the Cowork attempt must architecturally avoid
- **Meta concepts** (deployment / pioneer-instance / category-collapse / defensibility / engaged-authorship) — **PRESERVE** — defensibility + engaged-authorship are the load-bearing tests for the Cowork attempt's success

**Net**: ~25 of 36 entries directly load-bearing as conceptual frame for Cowork design; ~11 are framework-source-specific scope/governance vocabulary that drop with the framework pause.

### Architectural reasoning

**11 ARCH topic files** in `arch/`, all LOCKED:

| File | Lines | Role |
|---|---|---|
| `arch/substrate.md` | 408 | Pattern A protocol; Claude Agent SDK + MS AF substrate-impl pluggability |
| `arch/adapter.md` | 516 | Pattern A; META-Surface + 5 per-class Adapter Surfaces (Email/Accounting/MCP-Server/A2A-Peer/File-Sync) |
| `arch/sparring.md` | 395 | **LOAD-BEARING** — 8 sub-mechanism contracts (4 architecturally-encoded + 4 behaviorally-enforced); axis-2→axis-3 dependency |
| `arch/audit.md` | 380 | **LOAD-BEARING** — AuditEvent schema + audit-trail-as-canonical-source + 7 capability categories |
| `arch/quality-gate.md` | 410 | Pattern A; checkpoint firing + per-axis signal ingestion + intervention dispatch |
| `arch/specialist-skill.md` | 470 | **LOAD-BEARING** — bipartite specialist DEFINITION/INSTANCE; manifest schema; substrate Surface §G integration |
| `arch/practitioner.md` | 375 | Pattern C bipartite (HUMAN + RECORD); multi-practitioner cardinality; legal-entity placement |
| `arch/workflow-work-unit.md` | 480 | Two-Pattern-B; workflow_instance state machine + work-unit-kind; ad-hoc work first-class |
| `arch/claim-defensibility.md` | 422 | **LOAD-BEARING** — 4-property claim + 3-condition defensibility test + per-claim attestation chain |
| `arch/scope-model.md` | 442 | Cross-cutting integrator; Framework-C/Owner-B/Layer-A placement |
| `arch/axis-interactions.md` | 372 | Cross-cutting integrator; 3 pairwise compositions + CC-1 cross-axis failure cascade |

**4 read in detail**: substrate (Pattern A first canonical), sparring (mechanism-class with 8 sub-mechanisms; closest to actual SKILL.md authoring concern), audit (AuditEvent schema + dual-emission paths; closest to custom-MCP audit-tool design), claim-defensibility (defensibility test mechanics; the empirical-investigation success criterion).

**Classification**: PRESERVE all 11 as reference frame. The 4 LOAD-BEARING ones (sparring / audit / claim-defensibility / specialist-skill) directly inform the substantive Cowork SKILL.md authoring work — what the sparring SKILL.md must enforce, what audit-MCP-tool emissions must capture, what defensibility-test the deployment passes. The Pattern A pluggability topics (substrate, adapter, quality-gate) become reference-only since Cowork collapses substrate selection (always Anthropic).

### Practitioner profiles

`profiles/INDEX.md` (245 lines) + 17 profile files clustered:

- **Cluster A — Producers**: L1 specialist-creator / L2 shape-definer / L3 deployment-template-creator / L9 shape-catalog-curator (skeleton; full content TBD)
- **Cluster B — Deployers**: L4a workspace-deployer-solo / L4b firm-IT / L5a planner-pbs-schulz (deployer-of-self; **anchor profile, FULL DETAIL**)
- **Cluster C — Consumers**: L5a-L5j practitioner archetypes (planner/lawyer/researcher/auditor/medical/architect/junior/multi-jurisdictional) + L5e autonomous-business + L5f personal-OS — most are skeleton
- **Cluster D — Validators**: L8 auditor/reviewer-posthoc + G composability-gate (**FULL DETAIL**) + D defer-gate

**Classification**: 
- L5a (PBS-Schulz pioneer) is the only deeply-fleshed profile; **transfer as the canonical user model** for Cowork deployment design — defines the day-in-the-life the deployment must serve
- G composability-gate (consumption modes: consulting / internal-firm-reuse / OSS / marketplace / backup-migration) is **partial reuse** — most modes are framework-source concerns; backup-migration matters for a deployment
- L8 auditor-reviewer-posthoc — **HIGH REUSE** — defines the post-hoc defensibility-challenger viewpoint the deployment's audit-trail must serve
- L1-L4 producer profiles — drop-from-deployment-scope (those exist when framework distribution exists; Cowork pivot kills that scope)

### Dev skills (sharpening / audit)

`plugin/skills/` — 5 skill bundles, all domain-neutral:

| Skill | Lines | Purpose | Forward role |
|---|---|---|---|
| `sharpen/SKILL.md` | 239 | Generic critical-pass discipline; KEEP/REVISE/CUT verdicts; counters self-validation bias; Pareto discipline | **TRANSFER as-is** — works on any content needing critical pass |
| `decision-design-sharpening/SKILL.md` | 381 | Phase 1 (pre-decision); challenge → surface → refine → solidify cycle; Round 1 full monty + Round 2+ user-triggered | **TRANSFER as-is** — applies to Cowork architectural decisions |
| `pre-implementation-sharpening/SKILL.md` | 297 | Phase 2 (implementation-start); operational/runtime/deployment-detail surfacing; ~10-20% architectural flow-back | **TRANSFER as-is** — applies before each Cowork build step |
| `coherence-audit/SKILL.md` | 433 | 10 universal lenses + ARCH 11-15 / DR-set 16 / spec-set 17-18 corpus-specific lenses; cross-decision SET-level audit | **TRANSFER, but lenses 11-18 are framework-source-specific** — universal lenses 1-10 are reusable; ARCH/DR/spec lenses drop |
| `greenfield-rederivation/SKILL.md` | 352 | Foundation-up re-derivation audit per cluster; per-artifact sub-agent dispatch + Writer-Reviewer pattern + tiered findings | **TRANSFER as-is** — methodology applies to any audit-pattern needing fresh-context re-derivation |

**Net**: All 5 dev skills transfer to deployment repo as-is for governing the Cowork-build work itself. They are not framework-runtime; they are dev-process tooling.

### Archived deployment skills (frozen pbs:*)

`archive/plugin/skills/` — **19 skills** (NOT to be deleted; the `pbs:*` skills shown active in this session's available-skills list are loaded from `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0/`, frozen at version 0.1.0):

`audit/`, `author-manifest/`, `design-review/`, `draft-cover-mail/`, `draft-textteil-b/`, `draft-textteil-c/`, `orchestrator/`, `promote-to-skill/`, `record-feedback/`, `research-references/`, `review-draft/`, `save-baustein/`, `setup-office/`, `survey-project/`, `validate-bausteine/`, `validate-checklist/`, `validate-latex-style/`, `verify-citations/`, `watch-list/`.

All have SKILL.md + most have PROCEDURE.md (orchestrator + draft-textteil-b + review-draft sampled).

**Notable structure** (per orchestrator SKILL.md sample):
- Frontmatter declares `mcp_tools_required` + `mcp_tools_optional` + `fallback_when_mcp_absent`
- `routing_mode: always_active` for orchestrator (auto-loaded on planning-bureau context detection)
- `handoffs:` list cross-skill routing
- `phase_role:` (routing / phase_a_entry / phase_b_entry) for workflow phases
- References to `style-spec.md`, `korrektur-rules.md`, gate-only state.md contract
- **state.md is gate-only** ("no direct skill Read/Write per ARCHITECTURE meta-rule 4 fail-closed corollary")

**Classification**: **PRIMARY STARTING POINT for Cowork SKILL.md authoring**. These 19 skills already encode the actual Bauleitplanung workflow (B-Plan / Festsetzungen / Begründung / Stellungnahme) at a depth no fresh authoring can reach. The pivot is from "rebuild these against PBS framework v2" to "adapt these against Cowork + custom MCPs".

**Recommended posture**: ADAPT (rewrite frontmatter for Cowork conventions; rewire MCP tool references; re-test PROCEDURE.md content) rather than REWRITE FROM SCRATCH or EXTRACT-PATTERNS-ONLY. The substantive German-planning-domain content + the orchestrator routing logic + the phase-A/B layered review framework are load-bearing and irreplaceable.

### Mode 2 reference impls

`pbs/impls/` — 7 Python files (read all per pivot doc §5):

| File | Lines | What it implements | Forward role |
|---|---|---|---|
| `__init__.py` | 84 | Package docstring enumerating Phase 6.1 thin-slice scope + Phase 6.2 deferred items + foundation-up dependency notes | DROP (purely framework-phase orientation) |
| `claude_agent_sdk_substrate.py` | 722 | Claude Agent SDK substrate Implementation; SubstrateProtocol §A-§G satisfaction; in-memory MCP registry / hooks / specialists / sessions; substrate-internal direct audit emission | **PARTIAL SALVAGE** — Cowork collapses substrate selection (always Anthropic), but the SubstrateProtocol §C (request_permission HITL flow) + §G (specialist registration) + §F (session+context store) shapes can guide Cowork-equivalent wiring |
| `claude_agent_sdk_audit.py` | 929 | jsonl file-backed audit-trail; SHA-256 hash-chain integrity; query API per-claim/per-actor/per-time-window/per-event-kind/per-work-unit; render_state for workflow_instance/claim_status/actor_activity; export jsonl | **HIGH SALVAGE as helper** — directly applicable for custom audit-MCP-tool implementation; jsonl + hash-chain pattern is substrate-neutral |
| `mcp_server_adapter.py` | 840 | Generic MCP-Server adapter; META + per-class Surface; in_process/subprocess/HTTP transports; auth_model + refresh_auth + lifecycle | **PARTIAL SALVAGE** — adapter abstraction informs custom-MCP design; concrete transport handling is reusable |
| `practitioner_shape_authority_binding.py` | 408 | PRACTITIONER_JUDGMENT trust model; HUMAN actor required for signature_applied/send_authorized/claim_attested/work_unit_archived/workflow_phase_transition events; check() + bind_decision() | **HIGH SALVAGE as helper** — encodes the per-event-kind authority binding rules; directly translatable to custom MCP audit-gate logic |
| `practitioner_shape_gate.py` | 1196 | Practitioner-shape quality-gate Implementation; full engagement procedure (friction/nudge/block/practitioner-attestation/re-engagement); fail-closed; stateful via audit-trail-as-state-store; rubber-stamping detection mandatory | **HIGH SALVAGE as helper** — the engagement-quality enforcement logic is precisely what custom Cowork SKILL.md + custom MCP gate-tool must replicate; concrete intervention mechanics are reusable |
| `practitioner_shape_sparring.py` | 1182 | 8 sub-mechanism impl classes (counter-argument / confidence-calibration / visible-reasoning / selective-friction / anti-sycophancy / asymmetric-knowledge-respect / commit-to-recommendations / whats-missing-checkpoint); aggregating PractitionerShapeSparring; failure-mode emission feeding gate axis-2 ingestion | **HIGHEST SALVAGE as helper** — this IS the sparring discipline as runtime mechanism; either re-shape into Cowork SKILL.md content + custom MCP validation tools, OR keep as Python helper called from Cowork agents |
| `stub_mcp_server_backend.py` | 883 | Filesystem-backed MCP server backend; 3 tools (read_entity / write_entity / record_audit_event); single-workspace scope | **MEDIUM SALVAGE** — pattern for custom-MCP-server wiring; production replacement (LanceDB + fastembed) is anyway scoped; the audit-event-forwarding pattern is reusable |

**Net**: 7 files / ~5260 lines of locked-against-arch reference code. 4 files (`claude_agent_sdk_audit` / `practitioner_shape_authority_binding` / `practitioner_shape_gate` / `practitioner_shape_sparring`) carry HIGH salvage value as either Python helpers callable from Cowork agents OR as reference for what equivalent custom SKILL.md + custom MCP-tool logic must achieve.

## Cowork build implications

### Conceptual frame (preserve, reference at design moments)
- **VISION.md** three axes + Vivienne Ming sparring grounding + defensibility test — anchor for every Cowork design moment
- **GLOSSARY** ~25 vocabulary entries (workspace / practitioner / specialist / claim / work-unit / engaged-authorship / sparring / defensibility / etc.) — reusable as conceptual frame
- **arch/sparring.md + arch/audit.md + arch/claim-defensibility.md + arch/specialist-skill.md** — the load-bearing 4 ARCH topics articulating what the empirical investigation must replicate or refute
- **VISION-derived design-principles** from MAINTENANCE §1/§2/§3 (wrong-shapes-impossible / pattern-vs-instance / preliminary-lock) — meta-design discipline
- **DISCIPLINES.md** — domain-neutral cross-session working procedures (source-grounded / no-defer / foundation-up)
- **L5a profile + L8 profile + G consumption-modes** — user model + post-hoc-defensibility lens + multi-mode consumption framing

### Custom SKILL.md candidates (rewrite vs adapt vs extract-from)

- **ADAPT (primary path)**: All 19 archived `pbs:*` deployment skills — frontmatter rewrite for Cowork conventions, MCP tool references rewired, PROCEDURE.md content kept substantively
- **AUTHORED FRESH (informed by sparring 8 sub-mechanisms)**: sparring-discipline SKILL.md + claim-attestation SKILL.md + defensibility-test SKILL.md (per pivot doc §3 test items)
- **AUTHORED FRESH (informed by L8 profile)**: defensibility-audit SKILL.md for post-hoc challenge scenarios

### Custom MCP candidates
- **Audit MCP** (record_audit_event tool + query API for per-claim/per-actor/per-time-window/per-event-kind/per-work-unit): high-confidence design from `claude_agent_sdk_audit.py` + `arch/audit.md` §C/§D/§F
- **Quality-gate MCP** (engagement-signal ingestion + intervention dispatch): design from `practitioner_shape_gate.py`
- **Authority-binding MCP** (per-event-kind required-actor enforcement): design from `practitioner_shape_authority_binding.py`
- **Bauleitplanung-corpus MCP** (BauGB / BNatSchG / DE-BB regional): per pivot §3, no existing reference impl
- **LaTeX compile MCP**: per pivot §3, no existing reference impl
- **Email + accounting MCPs**: design from `mcp_server_adapter.py` per-class Adapter Surface pattern

### Python helper code (potentially callable from Cowork agents)
- `pbs/impls/claude_agent_sdk_audit.py` (jsonl + SHA-256 hash-chain audit-trail) — directly importable
- `pbs/impls/practitioner_shape_authority_binding.py` (PRACTITIONER_JUDGMENT trust model logic) — directly importable
- `pbs/impls/practitioner_shape_sparring.py` (8 sub-mechanism validation logic) — directly importable
- `pbs/impls/practitioner_shape_gate.py` (engagement-quality verdict + intervention selection) — directly importable

These have ARCH-cross-references in docstrings tying them to substrate / audit / sparring / quality-gate / authority-binding ARCH topics — useful self-documenting; the same docstrings can stay as the audit trail of "what concept this implements".

### Drop-from-scope
- Framework distribution mechanics (specialist DEFINITION marketplace; shape catalog curator; cross-shape policy mediation) — pivot eliminates this scope
- Pattern A pluggability infrastructure for substrate (Cowork = always Anthropic) — drop substrate selection mechanism
- Phase 6 spec discipline (~11 Mode 3 Pydantic specs) — Cowork build doesn't need cross-substrate-portable typed contracts
- Cascade discipline + 5-layer doc model + topic-template-class formal-stability tracking — framework-source-repo specific
- BACKLOG.md Phase 3.7+ items — framework-only forward work
- ~25 formal architectural decisions in `docs/decisions/` (not inventoried per scope) — these are framework-design-trail, preserved with the framework but not load-bearing for the deployment

## Honest basis caveats

**Files read directly in this session**:
- `5-PIVOT-DECISION.md` (full)
- `VISION.md` (full)
- `MAINTENANCE.md` (first 200 lines — TOP-LEVEL RULE + TOP-LEVEL ARCHITECTURE + TOP-LEVEL DESIGN PRINCIPLES)
- `DISCIPLINES.md` (full)
- `ARCHITECTURE.md` (first 300 lines — Phase 3 status + topic catalog + cross-cutting principles + locked decisions)
- `GLOSSARY.md` (full index)
- `arch/sparring.md` (first 120 lines — load-bearing topic)
- `arch/audit.md` (first 120 lines — load-bearing topic)
- `arch/claim-defensibility.md` (first 100 lines — load-bearing topic)
- `arch/specialist-skill.md` (first 100 lines — load-bearing topic)
- `profiles/INDEX.md` (full)
- `profiles/L5a-planner-pbs-schulz.md` (first 80 lines)
- `profiles/G-composability-gate.md` (first 60 lines)
- All 5 dev skills' SKILL.md (first 80 lines each)
- `archive/plugin/skills/orchestrator/SKILL.md` (first 40 lines)
- `archive/plugin/skills/draft-textteil-b/SKILL.md` (first 20 lines)
- `archive/plugin/skills/review-draft/SKILL.md` (first 20 lines)
- All 7 Mode 2 impls in `pbs/impls/` — `__init__.py` full + first 60-120 lines of each impl
- `findings-from-pbs.md` (full)

**Files only listed (not read)**:
- 36 `glossary/<entry>.md` files (clustered by topic per GLOSSARY index, not individually read)
- 31 of 36 individual `glossary/*.md` per-entry bodies — content inferred from GLOSSARY.md index + cluster index + tag scheme
- 7 of 11 `arch/<topic>.md` files (substrate / adapter / quality-gate / practitioner / workflow-work-unit / scope-model / axis-interactions) — only known via ARCHITECTURE.md §4 + §7 locked-decisions summaries
- 14 of 17 profile files (only L5a + G read; INDEX summarized rest)
- 11 per-discipline files in `disciplines/<NN-slug>.md` — only known via DISCIPLINES.md index summaries
- All 19 archived `pbs:*` skills' PROCEDURE.md — only 3 SKILL.md files sampled; PROCEDURE.md content inferred from frontmatter + system-reminder skill descriptions
- Bodies of all 7 Mode 2 impls beyond first 60-120 lines — full Surface satisfaction logic + concrete intervention mechanics not directly verified

**Inferred from session context vs verified**:
- "19 archived skills are loaded as `pbs:*` from cache" — VERIFIED via system-reminder skill list showing pbs: prefix entries matching archive/ folder names
- Salvage-classification of Mode 2 impls as "HIGH SALVAGE" — INFERRED from docstrings + line counts + ARCH cross-refs; concrete reusability in Cowork context is INFERRED, not verified by porting
- Claim that 25 of 36 glossary entries are "directly load-bearing for Cowork" — INFERRED from category clustering + topic alignment with pivot doc §3 test items; not verified entry-by-entry
- Claim that GLOSSARY entries L1-L4 producer profiles "drop-from-deployment-scope" — INFERRED from pivot doc framing that framework distribution is paused; deployment may still need authoring discipline
- "Notable gaps" (no STRATEGY.md / no arch/source-grounding.md / no Cowork substrate-impl) — VERIFIED via top-level `ls` + ARCHITECTURE.md §4 topic catalog showing 11 topics (no source-grounding) + Mode 2 substrate impl is Claude-Agent-SDK not Cowork

---

**Net**: This repo holds substantial reusable conceptual frame (VISION + ~25 GLOSSARY entries + 4 LOAD-BEARING ARCH topics + dev skills + Mode 2 helpers) and the 19 archived `pbs:*` deployment skills are the closest-to-Cowork-authoring artifacts and primary adaptation target. The framework-source machinery (cascade discipline / Pattern A pluggability / Phase 6 spec layer / BACKLOG forward work) drops with the pivot but its outputs (reasoned ARCH topics + locked GLOSSARY) carry forward as design-reference.
