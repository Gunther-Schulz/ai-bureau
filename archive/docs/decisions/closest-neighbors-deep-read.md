# Decision record: Closest neighbors deep-read + competitive landscape (session 14)

**Status**: ACCEPTED (session 14, 2026-04-30)
**Owner**: `docs/strategic-positioning.md` (consumes findings); ARCHITECTURE.md (adoption opportunities); ROADMAP (#24 + #25 commitments)
**Sharpening metadata**: Synthesis of 7 research passes — landscape + adversarial gap-verification + 4 deep-reads (Letta + OpenSail + PAI + Paperclip) + exhaustive commercial scan + deeper OS+hybrid scan + DACH/EU regulatory + a16z VC thesis.
**Related**:
- `terminology-and-specialist-primitive.md` (session 13 Sub-DR A — workspace/specialist primitives competitor analysis is built around)
- `positioning-three-tier-framework.md` (session 13 Sub-DR B — three-tier marketplace shape)
- `shape-extension-and-architectural-floor.md` (session 14 sibling DR — shape-extension model + Option B)
- `vision-realignment-session14.md` (session 14 sibling DR — counter-VISION engagement consumes commercial findings)

## Context

Session 14 user direction: "let's research open source competition to us since we reframed to AI Workspace"; expanded with "we need to be exhaustive about competition. include commercial offerings"; further with "I would prefer an additional full os check or OS+commercial hybrid"; further with "I will be mainly operating in EU, mainly Germany"; further with "workspace for architects, a16z, EU AI Act"; further with "Paperclip closer look"; further with "PAI deserves same scrutiny."

7 research passes executed. Findings synthesized here.

## Top-level verdict

**Gap claim CONFIRMED with HIGH confidence raised across all research passes.** Zero projects (OS or commercial) match 4+ of 5 distinctness axes + multi-actor primitive simultaneously. Closest neighbors:

| Project | Axes-fit | Type | Closest by |
|---|---|---|---|
| **PAI (Personal AI Infrastructure)** | 3/5 | OS | Architectural overlap (workspace-as-identity + composable bundles + practitioner-as-author shape) |
| **OpenSail (TesslateAI)** | 2.5/6 | OS | Verbal positioning (workspace + bundles + audit-log + non-developer audience) |
| **Beck-Noxtua (€80.7M Series B)** | 2/6 | Commercial (DACH) | Geographic + market overlap (DACH legal AI workspace; EU AI Act tailwind aligned) |
| **Anthropic Claude Cowork + vertical plugins** | 2/6 | Commercial | Architectural direction-of-travel (composable plugins encoding workflows) |
| **Paperclip** | 1.5/6 | OS | Sophistication + market visibility (real product; conceptually distinct shape — autonomous-business not practitioner) |
| **Letta v1 (formerly MemGPT)** | 1-2/5 | OS | Surface vocabulary collision (skills + subagents + memory + deployment) |

**Distinctness summary**: PBS load-bearing distinct on **5 of 6 axes** (workspace-identity / specialist-bundle / sparring-runtime-pillar / audit-by-construction / practitioner-as-author / multi-actor). Closest competitors cover 1-3 axes each.

## Deep-read findings — per-project synthesis

### Letta (formerly MemGPT) — deep-read findings

**Architectural shape**: Single-tier agent runtime + DB-backed state (Postgres + pgvector). Central primitive `AgentState` aggregates blocks + tools + sources + secrets + tags + identities + managed_group + tool_rules + model_settings. **No workspace/specialist three-tier separation.**

**Skills**: SKILL.md compatible folder bundle in MemFS git-backed memory; rendered into `<available_skills>` system prompt block. **Real interop opportunity** — Anthropic-style format.

**Memory**: Three tiers (Block in-context / Archive vector / Message recall). Plus **MemFS** — git-backed memory filesystem stored at `~/.letta/memfs/`, exposed over Git Smart HTTP (`git clone http://.../v1/git/{agent_id}/state.git`). **Genuinely innovative pattern.**

**Sparring**: ABSENT. HITL approval (`ApprovalRequestMessage` / `ApprovalResponseMessage`) is cooperative-with-veto, not adversarial.

**Audit**: Telemetry-grade. `Step` / `ProviderTrace` / `LLMTrace` (ClickHouse mirror) / OpenTelemetry. **No `AuditEvent`-shaped decision provenance.** MemFS git history is closest to canonical write log but covers memory mutations only.

**Substrate abstraction**: Strong. `LLMClientBase` + 18+ provider implementations.

**Audience**: **Developers building stateful apps.** README target, REST/SDK, PostgreSQL setup, alembic migrations. Not architected for non-developer practitioners.

**Hypothetical PBS-Schulz on Letta**: 8/13 components require overlay (sparring, audit-grade, cross-specialist events, project-as-multi-phase-entity, external authorities, source-grounding contract, workspace identity, practitioner-as-author).

**Verdict**: Cargo-cult risk LOW. Architectural shapes diverge cleanly. **Treat as ecosystem peer** (interop target, pattern source) — not competitive runtime.

### OpenSail (TesslateAI) — deep-read findings

**Architectural shape**: AI app-builder / agentic-coding IDE in v0/Bolt/Lovable/Cursor lineage. README explicit: *"open-source alternative to Codex App, Claude Desktop, Cursor, and Cowork for agentic software work."* Four-tier: React/Monaco frontend + FastAPI orchestrator + Postgres metadata + per-project Docker/K8s container environments.

**Bundle = "App"**: containerized deployment with `app.manifest.json` (versioned schema). Runtime contract is K8s-native. Apps are NOT SKILL.md-compatible.

**Workspace concept**: K8s namespace + btrfs subvolume + container set. **Workspace = where the agent works** (compute environment), NOT practitioner identity envelope.

**Substrate**: LLM-API-layer abstraction via LiteLLM. Agent runtime is their own framework `tesslate-agent`. **Tightly coupled** to tesslate-agent + LiteLLM; not pluggable at framework layer.

**Sparring**: ABSENT as runtime concept. Closest equivalent: `AdversarialSuite` in marketplace pre-publish safety eval. Single-loop tool-calling at runtime.

**Audit**: Async fire-and-forget compliance logging. `audit_service.py:1-5` explicit: *"Non-blocking audit trail service. Fires and forgets — audit logging NEVER blocks the primary operation."* AuditLog rows + 90-day retention + AgentCommandLog. Append-only logging for compliance, not provenance.

**Permissions / governance**: Real and load-bearing — Contracts + Approval gates + Budget gates + per-project permissions.json + Connector Proxy + K8s NetworkPolicy. **"Connector Proxy" pattern** worth adopting (credentials never reach app code).

**Audience**: Developer-skewing despite README claiming "operators, founders, legal teams, support."

**Hypothetical PBS-Schulz on OpenSail**: 9/13 components mismatch. Container-per-specialist heavy mismatch with PBS markdown-runtime-composed shape.

**Verdict**: Different domain (agentic IDE / app-builder). Adjacent, not competitor. **Adoptable patterns**: Connector Proxy + Contract-as-data + manifest schema versioning + surface enum.

### PAI (Personal AI Infrastructure) — deep-read findings

**Architectural shape**: **Customization layer on Claude Code, NOT a framework.** README explicit: *"PAI is Claude Code native… built natively on Claude Code and designed to stay that way."* Installable surface = `~/.claude/{settings.json, hooks/, skills/, PAI/, agents/, commands/}` config tree. ~37 TypeScript hooks (Bun runtime). No agent loop / tool dispatcher / message protocol — those are substrate.

**Workspace / identity**: Convention not structural primitive. `PAI/USER/PRINCIPAL_IDENTITY.md` + `DA_IDENTITY.md` are markdown @-imported at session-start via `CLAUDE.md`. **Single-user only** — SYSTEM_PROMPT.md explicit: *"This {{DA_NAME}} instance is configured for {{PRINCIPAL_NAME}}'s individual use only."*

**Specialist composition**: Pack pattern. Each Pack contains `INSTALL.md` (AI-readable wizard), `VERIFY.md`, `README.md`, `src/{SKILL.md, Workflows/, Templates/}`. Installation: "point your AI at any pack and say 'install this'." **Not versioned packages, no registry, no dependency graph.** 6 customization layers (Identity / Preferences / Workflows / Skills / Hooks / Memory) as USER/-tree directories.

**Sparring**: Confirmed OPT-IN SKILLS, not runtime pillar. RedTeam + Council are entries in closed enumeration of *eligible* thinking capabilities the Algorithm may select. Algorithm v6.3.0 capability floors are count-based (E2 needs ≥1, E4 needs ≥6) — RedTeam/Council eligible but not required. **No always-on adversarial pass.**

**Audit**: Confirmed telemetry-style, not provenance-by-construction. `MEMORY/OBSERVABILITY/*.jsonl` append-logs + classifier telemetry. "12 security gates" are privacy containment, not audit-grade.

**Audience**: README claims "everyone" — code-base says "developer + power-user comfortable with bash/TypeScript/CLI." Daniel-shaped framework offered as universal.

**Substrate dependence**: Tightly coupled to Claude Code (hooks, settings.json schema, Skill/Agent tools). README admits porting is fork-not-substrate-switch.

**Hypothetical PBS-Schulz on PAI**: 2 success / 5 warning / 3 fail. Lifecycle/state + memory bausteine map well; send gate + audit + external authorities require overlay.

**Verdict**: Closest architectural neighbor (3/5 axes overlap) but **single-human-bound + Claude-Code-coupled + sparring-opt-in + audit-telemetry-grade**. PBS distinct on: sparring-as-runtime + audit-by-construction + multi-actor reality + practitioner-archetype + substrate abstraction. **Adoptable patterns**: INSTALL.md wizard + closed-list capabilities with phantom-detection audit + USER/system separation contract.

### Paperclip — deep-read findings

**Architectural shape**: TypeScript/Node monorepo + Express REST API + React UI + Postgres-as-source-of-truth (~70 tables). Runtime: shells out to local CLIs (`claude`, `codex`, `hermes`) or hits OpenClaw HTTP. **NEVER makes LLM calls itself.**

**"Zero-human" framing**: Aspirational marketing, NOT structural. Schema has `actorType: 'user'|'agent'|'system'`, `decidedByUserId`, `requestedByUserId`, `requireBoardApprovalForNewAgents`. Humans first-class actors throughout.

**Org-chart**: Two columns on `agents` (`role` text + `title` text + `reportsTo` self-FK). Static config-driven. **Flatter and less typed than PBS specialist composition.**

**Tickets/Issues**: Central work primitive. Single-assignee + atomic checkout (POST `/api/issues/:id/checkout` with optimistic 409 conflict). **Coordination is call-shaped, not event-shaped** — different concurrency model from PBS.

**Audit**: REAL append-only history (not telemetry). `activity_log` with `actorType` / actorId / action / details + `runId` ties every mutation to heartbeat run. **However**: action-level not claim-level. No `sources[]` / tool-result-binding for individual claims inside generated content. PBS audit-trail v2 is finer-grained.

**Sparring**: ABSENT as runtime. `approvals` table + `issue_execution_decisions` are policy-and-approval governance, not adversarial counter-argument.

**Substrate**: Tightly coupled to `tesslate-agent` (similar to OpenSail).

**Audience**: **Operator/board of many-agent autonomous shop.** "User with 20 Claude Code terminals open." Load-goals-and-supervise shape.

**Hypothetical PBS-Schulz on Paperclip**: ~5/10 components map cleanly + ~5/10 require substantial overlay + ~3/10 absent. Could host ticket+approval+heartbeat orchestration; load-bearing PBS primitives (claim-level audit, source-grounding, memory bausteine, references corpus, sparring) all live above/beside.

**Verdict**: Conceptual distance is REAL — different problem (autonomous business with operator) + different primitives (call-shaped + atomic checkout) + different center of gravity (Companies vs Practitioner). **Adoptable patterns**: heartbeat + wake-coalescing; `issue_execution_decisions` shape (transposable to PBS layered review); `document_revisions` rollback; multi-tenancy by scoping. **Not a competitor unless 5 trigger conditions fire** (claim-level audit / always-on sparring / composable specialist primitive / memory + invalidation / explicit practitioner courting).

## Commercial competitive landscape

### Closest commercial neighbors

| Company | Axes-fit | Notes |
|---|---|---|
| **Beck-Noxtua / Noxtua SE** (DACH; €92M Series B; backed by C.H.Beck + CMS + Dentons + Northern Data) | 2/6 | "Legal AI Workspace"; ISO/IEC 42001 + BSI C5 + ISO/IEC 27018 certified; sovereign EU infra; transparent reference disclosure + change tracking. **Closest commercial neighbor for German market — but vertical SaaS shape + practitioner-as-USER not author** |
| **Anthropic Claude Cowork + vertical plugins** (Feb 2026; financial services + HR + engineering + legal) | 2/6 | Desktop workspace + Anthropic-or-partner-authored plugins encoding "institutional knowledge and workflows." **Most architecturally-similar commercial offering** — direction-of-travel evidence — but Enterprise-only + no sparring + no multi-actor + no self-host |
| **Stilta** (YC W26; IP/patent work; $0→$15K MRR Feb 2026) | 1/6 | "Every output source-backed, referenced, and auditable" — explicit audit-by-construction language. **Validates the axis** in single-vertical SaaS form |
| **Avoice** (YC W26; "AI workspace for architects" / "Harvey for Architecture") | 1/6 | Vertical SaaS for architecture firms; 5 countries; £100/spec-agent UK pricing; "$300M+ active project value." Vendor-authored agents only; **no DSGVO posture, English-only — does NOT block PBS in DACH** |
| **AutoSitu** (YC W26; "AI-native workspace for municipal development review") | 1/6 | **OPERATES INVERSE side of PBS pioneer domain** — cities reviewing applications + zoning + fire + engineering codes. *Customer-of-PBS-output, not competitor.* Cities digitizing review = demand for audit-ready submissions = favors PBS audit-by-construction. **Single biggest finding** from commercial scan. |

### DACH-specific landscape (PBS operates EU/Germany — load-bearing)

| Company | Notes |
|---|---|
| **Phase0 (formerly Compa, Berlin; founded 2020)** | **Dominant DACH incumbent — 800+ firms / 1,500+ users.** "OS für moderne Architektur- und Ingenieurbüros." HOAI (LP 1-9) + AVA (DIN 276, GAEB) + AI-Bautagebuch + AI-LV-generation in beta. DSGVO-konform, EU-hosted. **Owns operational-software layer for DACH planner+architect mid-market.** PBS positions ABOVE Phase0 (expertise codification + audit + multi-actor + sparring); does NOT compete on HOAI/AVA mechanics |
| **Langdock (Berlin)** | "Die Plattform für KI-Adoption." Frankfurt-hosted; ISO 27001 + SOC 2; DPA upfront; 40+ models behind one interface. Custom-GPT primitive = weak practitioner-author proxy. **MEDIUM-HIGH substrate competitor** — DACH firm shopping "DSGVO-AI" buys Langdock + builds custom-GPTs themselves. PBS differentiates: codified specialists + sparring + audit (categorically different from custom-GPTs) |
| **Allplan / Vectorworks / ArchiCAD** | CAD-incumbent AI-add-ons. Pure CAD-feature, not workspace. Threat: LOW |
| **Beck-Noxtua / PRIME LEGAL AI / anwalts.ai** | DACH legal/tax commercial workspaces. Practitioner-as-USER not author. Watch for archetype expansion (Steuerberater / Architekturbüro / Planungsbüro) |
| **BAK (Bundesarchitektenkammer)** | Advocacy-only; **NO chamber-vendor partnership; NO chamber-stamp accreditation.** Liability concern ("Wer haftet für KI-Fehler?") is **PBS-axis advantage** — audit + practitioner-as-author + sparring directly address professional-liability anxiety. Marketing wedge |

### Other commercial (vertical SaaS — not the shape)

Vertical SaaS replacement plays not architecturally competitive: Harvey (legal $11B), Spellbook + Legora (Word-embedded contract AI), Eudia (in-house legal $105M), Rogo (investment banking $300M+), Accrual / Basis (accounting), Ambience (clinical OS), Bravi / Avoca (HVAC), Hazel + Vise (wealth), Pin + Humanly (HR/recruiting), Mike (open law), OpenAccountants (accounting skills lib).

### Workday acquired Sana for $1.1B

Adjacent player pulled into HR/L&D enterprise stack — removed from PBS competitive set.

## Strategic positioning implications

### a16z / Sequoia "service-as-software" thesis (positioning risk for fundraising)

Dominant 2026 VC framing (per Bek's "Services: The New Software" — Sequoia owns canonical, a16z reinforces). Replace-the-consultant via AI-native firms. Portfolio: Harvey, Rogo, Crosby, Anterior, Lawhive, Mercor. **Antithesis of PBS positioning** — accepting a16z/Sequoia capital would force narrative drift toward replace-the-practitioner.

### Cherry Ventures (Berlin) — only published EU VC thesis match

**"Cherry's AI Theses"** + **"Bringing the AI Thesis to Life"**: *"AI supports and enhances human creativity… without replacing"*; chess-player-and-computer model; European founders advantaged by *"intimately understand the regulatory landscape."* Portfolio: Cortea (regulatory compliance), Riplo (consulting OS), Sphinx (compliance automation). **PBS positioning lands cleanly** in Cherry thesis.

### Recommended funding path (ground-up + grants + strategic + Cherry-of-last-resort)

1. **Ground-up consulting revenue (PBS-Schulz pioneer)** + **EXIST/ZIM/go-Inno non-dilutive DACH grants** (18-24 months) — preserves framing fully
2. **Strategic capital from publishers + chambers + state banks** (Beck-Noxtua model: €80.7M from C.H.Beck + CMS + Dentons + Northern Data — no classical VCs)
3. **Cherry Ventures as VC-of-last-resort** (only thesis-aligned EU VC)
4. **AVOID GC-channel firms** (La Famiglia merged into General Catalyst 2023; carries replace-thesis import) + Index/Atomico growth + Earlybird-growth (deep-tech infrastructure-focused; misalignment with PBS application-layer positioning)

### EU AI Act tailwind (asymmetric — favors PBS)

Per EU AI Act + DACH regulatory deep-look:
- **Sparring uniquely operationalises Art. 14 human oversight** — genuinely unique regulatory asset
- **Practitioner-as-deployer = cleanest AI Act posture** vs SaaS provider/deployer muddiness
- **Self-hostable + EU residency** aligns with sovereign-AI direction (BSI C5 sovereignty + DSGVO Art. 44-49)
- **Audit-by-construction = direct mapping** to Art. 11/13/26(6) — Beck-Noxtua/Stilta partial overlap; PBS structurally fuller
- **Hard requirement before Aug 2026 production**: Art. 50(4) AI-disclosure for B-Plan Begründung
- **Critical architectural constraint**: prevent Art. 25 substantial-modification trap (specialist conformity manifest as Pydantic gate, NOT solvable by convention)
- **Major commercial asset opportunity**: ISO/IEC 42001 deployment template / SoA scaffold (cuts cert cost for any EU practitioner workspace)

### Distinctness axes confirmed (load-bearing for positioning)

PBS uniquely holds **5 of 6 distinctness axes**:

1. ✅ **Workspace as practitioner-identity primitive** (PAI is single-human-bound; OpenSail = container env; Paperclip = company; Letta = no workspace)
2. ✅ **Specialist as composable codified expertise bundle** (skills + entities + memory + references + adapters bundled)
3. ✅ **Sparring as runtime pillar** (CONFIRMED by all 4 deep-reads + commercial scan: NO competitor treats sparring as always-on runtime)
4. ✅ **Audit by construction** (claim-level; CONFIRMED unique; competitors all action-level/telemetry)
5. ✅ **Practitioner-as-author** (vs developer-author / operator-supervisor / installer/buyer)
6. ⚠ **Multi-actor primitive** (configurable per-deployment) — PAI is single-human; Paperclip has user/agent/system but no external_agent for regulators

## Adoption opportunities table (~10 patterns; ~7 adopt + 3 defer)

| # | Pattern | Source | Verdict | Where to land |
|---|---|---|---|---|
| **A1** | SKILL.md interop for Specialist (publish AS SKILL.md core + PBS extension manifest) | Letta + Anthropic ecosystem standardized | ✅ adopt | Bundle with #11 Cowork integration |
| **A2** | Connector Proxy pattern → Adapter Protocol security (credentials never reach specialist code) | OpenSail | ✅ adopt | Add to #9 Bundle E (Adapter Protocol) |
| **A3** | Contract-as-data → Specialist runtime contracts (allowed tools/MCPs/scopes/budget per invocation) | OpenSail | ✅ adopt | Compose with `permission-abstraction.md` (R3c) |
| **A4** | Manifest schema versioning discipline (per-version JSON Schema files; co-existence) | OpenSail (+ Letta AgentFile reference) | ✅ adopt | Bundle with #9 entity-md spec |
| **A5** | INSTALL.md wizard pattern (AI-readable wizard for Pack/Specialist installation) | PAI | ✅ adopt | Bundle with #11 |
| **A6** | Closed-list capabilities with phantom-detection audit (any name not in list = CRITICAL FAILURE) | PAI | ✅ adopt | Add as ARCHITECTURE pattern note (composes with Make-wrong-shapes-impossible v0.21) |
| **A7** | USER/ vs system separation contract (USER never modified by upgrades) | PAI | ✅ adopt | Codify in plugin-conventions |
| **A8** | `issue_execution_decisions` shape (stageId + stageType + actorAgentId/userId + outcome + createdByRunId) | Paperclip | ✅ adopt | Fold into #9 Bundle B (entity gate + Layer 3) + Contract-as-data work |
| **A9** | `document_revisions` + `agent_config_revisions` rollback pattern (revision-table + baseRevisionId optimistic-concurrency) | Paperclip | ✅ adopt | Fold into send-gate snapshot work (#11 / #6) |
| **A10** | Asqav cryptographic audit chain composition target | Asqav (deeper OS scan) | ⚠ evaluate | Consider as composition target for audit infrastructure (vs re-implement); evaluate post-#6 |
| **D1** | MemFS git-backed memory pattern | Letta | ⏳ defer | Interesting but not load-bearing; defer to first concrete cross-tool sync need |
| **D2** | AgentFile export schema (Letta-style transport) | Letta | ⏳ defer | #11 Cowork + ROADMAP v3 marketplace will lock distribution shape |
| **D3** | Heartbeat + wake-coalescing pattern (long-running agents) | Paperclip | ⏳ defer | First long-running-agent need (chronological-valid) |
| **D4** | PBS as MCP tool consumed by OpenSail / Letta | Various | ⏳ defer | ROADMAP v3+ tactical move |

## Watch-list entries

Monitor for evolution:

| Project | Trigger that would re-classify |
|---|---|
| **OpenSail** | If practitioner-identity primitive emerges (currently container env) → re-evaluate |
| **PAI** | If "PAI for lawyers / consultants / planners" practitioner-archetype fork emerges → would intrude on practitioner shape |
| **Paperclip** | (a) ships claim-level audit with sources[]/causes[] inside drafts → audit-by-construction collision; (b) ships always-on sparring/critique → sparring pillar collision; (c) ships composable specialist as first-class entity → specialist abstraction collision; (d) Memory roadmap lands as cross-project + invalidation-aware → bausteine collision; (e) explicitly courts practitioner audience → direct competition |
| **Letta** | If skills + subagents evolve toward composable expertise bundles (vs current SKILL.md-folder) → specialist primitive collision |
| **Beck-Noxtua** | Archetype expansion to Steuerberater / Architekturbüro / Planungsbüro → DACH market overlap |
| **Avoice** | EU/German market entry with DSGVO posture + German UI → DACH practitioner competition |
| **Anthropic Claude Cowork** | Plugin ecosystem expansion to practitioner-author primitive (currently Anthropic-or-partner-authored) → architectural direction-of-travel becomes direct |
| **AutoSitu** | Adoption growth → opportunity (cities demanding audit-ready submissions favors PBS) |
| **Cherry Ventures portfolio** | New investments in practitioner-amplification space → confirmation of thesis maturation |
| **CUNY AI Journalism Lab cohort** (24 practitioner-builders 2026) | May produce archetype-specific OS projects worth tracking |

## Composition with disciplines

| Discipline | Connection |
|---|---|
| Pattern-vs-instance (v0.20) | Competitive comparison properly framed as practitioner-shape comparison (apples-to-apples), not framework-vs-framework. Documented in `vision-realignment-session14.md` |
| Make-wrong-shapes-impossible (v0.21) | Adoption A6 (closed-list with phantom-detection audit) directly applies. Adoption A2 (Connector Proxy) makes credentials-leakage impossible-by-construction |
| Sharp defer rule (v0.20) | All defers (D1-D4) chronological-valid; named specific information that doesn't exist yet |
| Substrate-pluggability (v0.30) | All 4 substrates (Letta + OpenSail + PAI + Paperclip) tightly substrate-coupled; PBS framework-layer abstraction is genuinely distinct |
| Glue-not-replacement (v0.15) | Counter-VISION engagement (in `vision-realignment-session14.md`) consumes service-as-software thesis as antithesis. PBS = glue/amplify; service-as-software = replace |

## Defers — re-examined session 15 under v0.33 no-defer principle

> **Session 15 amendment**: re-examined the 3 entries below. Result: D1 (memory adapter integration) is RESCOPING — already executed via #19 scope expansion to include memory adapter eval (Mem0 / Zep / Graphiti / Cognee) per HANDOFF session-14 follow-up (#19 scope locked). Not a defer. D2 (PBS published as MCP tool) is a valid watch-list entry awaiting marketplace v3 launch milestone. D3 (Asqav composition vs build evaluation) is phase routing to #6 audit-trail v2 retrofit. Per v0.33 preliminary-lock: this DR remains preliminary-locked. Original entries kept below as historical record.

### Original entries (chronological-valid)

| Defer | Home | Cost being avoided |
|---|---|---|
| D1: Memory adapter integration (Mem0 / Zep / Graphiti / Cognee evaluation) | Extend #19 (LlamaIndex pluggable RAG eval) scope to include memory layer — same architectural question (build vs adopt vs pluggable) | No primary memory-layer choice locked; #19 architectural decision will determine |
| D2: PBS published as MCP tool (consumed by Letta/OpenSail/Paperclip ecosystems) | ROADMAP v3+ marketplace tactical move | Premature; v3 marketplace shape not finalized |
| D3: Asqav composition vs build evaluation | Post-#6 audit-trail v2 retrofit | Audit infrastructure must be implemented before composition vs build decision |

## Cascade

| Layer | Change |
|---|---|
| `docs/decisions/closest-neighbors-deep-read.md` | NEW — this file |
| `docs/strategic-positioning.md` | Will reference: closest neighbors section + Cherry thesis match + DACH grant ecosystem + a16z thesis as positioning risk + Phase0/Langdock/Beck-Noxtua/Avoice/AutoSitu entries + sharpened differentiators (per session 14 sibling rewrite DR) |
| `ARCHITECTURE.md` | Will reference: A6 (closed-list discipline) + A2 (Connector Proxy) + A3 (Contract-as-data) potentially as discipline notes |
| `ROADMAP.md` | Will reference: A1-A9 adoption opportunities flow into #11 / #9 / #6 commitments. Plus #24 (compliance specialist) + #25 (shape extension framework) per session 14 |
| `vision-realignment-session14.md` | Counter-VISION engagement (R1) consumes service-as-software finding |
| `shape-extension-and-architectural-floor.md` | Architectural distinctness verdict (5/6 axes unique) confirms shape-extension model + Option B value |
| `HANDOFF.md` | Session 14 entry captures full competitive landscape work |

## Files touched

- `docs/decisions/closest-neighbors-deep-read.md` (NEW — this file)
- `~/dev/reference/letta/` (cloned for deep-read)
- `~/dev/reference/opensail/` (cloned for deep-read)
- `~/dev/reference/pai/` (cloned for deep-read)
- `~/dev/reference/paperclip/` (cloned for deep-read)

## Revisit triggers

- Any watch-list entry above fires
- New OS or commercial entrant achieves 4+ axes-fit (would reframe gap claim)
- Major Anthropic Cowork ecosystem evolution
- Major Cherry Ventures portfolio evolution (validates / contradicts practitioner-amplification thesis)
- Real PBS first-bind real-world deployment data
