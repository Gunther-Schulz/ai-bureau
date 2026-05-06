# 4-PRELIMINARY-COMPOSITION-FRAMEWORK

> **Status**: Preliminary positioning document. Captures session 35 (post-2026-05-06) vision sharpening across multiple turns where the framework's positioning evolved from "thin layer over platforms" → "context-graph for accountability work" → (final) **"composition substrate for solo / small-business operators to integrate existing tools into AI-supported cross-domain workflows with on-demand professional discipline."** This is the strongest framing reached today and supersedes earlier framings in `1-NEXT.md` §3.5 and `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md`.
>
> **Companion documents**:
> - `1-NEXT.md` — working session handoff + F1-F4 plan; §3.5 positioning to be revised per this doc
> - `2-PRELEMINARY-ENTRERPRISE.md` — enterprise platform landscape research (informs F4 only)
> - `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md` — earlier "context-graph" framing; subsumed by composition-framework framing here (the context-graph is a CONSEQUENCE of composition applied to accountability-bearing work, not the fundamental framing)
> - This file — vision-level positioning + audience definition + concrete examples + honest concerns

---

## 1. The vision in one paragraph

PBS framework is a **composition substrate** that lets a solo professional or small business (1-10 people, no engineering capacity) build their own AI-supported workspace where one person plays multiple employee roles (secretary + accounting + planning + project manager + domain expert + ...). The framework integrates existing tools (vertical SaaS like Harvey, PM tools, email, corpus access, accounting software) via open standards (MCP + A2A) and adapter Pattern A, maintains cross-tool / cross-role context awareness within the deployment, and applies on-demand professional discipline (audit trail + sparring + authorship preservation) for the work that needs rigor — without burdening routine work. Setup is configuration-driven (LLM-assisted bootstrap skill generates markdown configuration); coding only when genuinely necessary and outsourceable. Open-source, self-hostable. Composes WITH vertical SaaS instead of competing.

## 2. The crisp anchor example

Single user request in PBS-integrated workspace (Claude Code / Cowork / SDK orchestrator):

> "Compose email — tell project lead of customer that Entwurf XYZ shipped today."

This triggers a coordinated multi-tool orchestration because the framework's workspace context already provides:

- Project entity (which project, current state)
- Customer entity (who; shape-mandated engagement-target — `Client` for practitioner-shape per `arch/scope-model.md:73`)
- Project lead identity (resolved from project entity or prior correspondence audit-trail)
- Entwurf XYZ work-unit (state "shipped today" per work-unit lifecycle in `arch/workflow-work-unit.md`)
- Communication history (audit-trail of prior client correspondence)
- Email tone/conventions (Layer A content per workspace.scope domain)

The chain that fires:

1. Drafting specialist + LLM compose draft using workspace context (no manual feeding)
2. Sparring engagement IF the message warrants rigor (engagement detection per `1-NEXT.md` §5; routine status update gets light engagement; contractually-binding statement gets full sparring)
3. Practitioner reviews; framework respects axis-3 (practitioner remains author)
4. Send: `claim_attested` requires HUMAN actor per practitioner-shape authority-binding catalog → practitioner approves; `send_authorized` event captures
5. Email-adapter dispatches; PM-tool-adapter receives workflow phase transition → updates PM tool's project entry
6. Audit-trail captures: claim_made + send_authorized + workflow_phase_transition events as one coherent chain

Months later under defensibility test: "did Gunther actually communicate this? when? what exactly? what state was project in?" — reconstructible from the audit-trail chain.

That's the substantive value vs the alternative reality of "open email plugin → ask AI to compose → paste from project file → send → manually update PM → hope you remember to log it for audit."

## 3. Audience

The discriminator is **engineering capacity to build custom integration infrastructure**, NOT company size:

| Audience | Engineering capacity | Buy / build | PBS fit |
|---|---|---|---|
| Solo / 1-10 person firms | None | Buys / configures only | **PBS audience** — needs configurable framework |
| 10-50 person firms | None (no dedicated AI eng team) | Buys / configures | **PBS audience** — same constraint |
| 50-500 person firms | Maybe (small AI-curious team) | Mixed | Maybe — depends on config-vs-code feel |
| 500+ enterprise | Yes | Builds custom | NOT PBS audience — they roll their own; PBS could be REFERENCE for their build but not direct-adoption target |

**Operational corollary**: if PBS targets organizations without engineering capacity to BUILD their own integration, then PBS itself must require minimal engineering to OPERATE:

- Self-hosting: one-command-install or docker-compose
- Updates: self-updating, no "pull and rebuild"
- Configuration: markdown text-edit, not code-edit
- Failures: user-readable errors, not stack traces
- Specialist installation: one-command (`pbs-cli install specialist@version` or equivalent)

## 4. Core mechanism — composition substrate

PBS is fundamentally an INTEGRATION substrate, not a build-from-scratch framework. The "real work" of deploying PBS is transferring existing procedures / processes / data into the deployment configuration; the framework provides the substrate that wires them together.

What PBS integrates:

- **Vertical SaaS** (Harvey for legal, equivalents for other domains) via MCP-Server adapter class — verified `arch/adapter.md:54-58`
- **PM tools** (Asana, Notion, Linear, custom) via MCP / A2A / file-sync adapter classes
- **Email** (SMTP / IMAP / Gmail / Outlook) via Email adapter class
- **Document tools** (Word, LaTeX, custom) via File-Sync adapter class
- **Corpus / knowledge bases** (legal corpus, domain reference material, RAG backends) via MCP-Server adapter class
- **Accounting software** via Accounting adapter class
- **Other agents** (peer agents on different platforms) via A2A-Peer adapter class
- **Specialists** authored locally OR downloaded from marketplace per `arch/specialist-skill.md` §11

What PBS adds on top:

- **Cross-tool context**: workspace state spans all tools; specialists/skills reference each other's work
- **Workflow orchestration**: workflow_instance state machine ties adapter calls into coherent phase progressions
- **Engagement detection** (`1-NEXT.md` §5): on-demand professional discipline for work that needs rigor
- **Audit trail** (per `arch/audit.md`): single hash-chain captures cross-tool / cross-specialist operations
- **Practitioner accountability semantics** per shape policy: HUMAN attestation required for legal-bind moments
- **Defensibility test reconstruction** (per VISION): six-month-later audit reconstructs reasoning chains

## 5. Multi-role single-person mapping

Solo professional juggles N employee roles. Each role maps to PBS architectural primitives:

| Multi-role need | PBS primitive |
|---|---|
| Different employee roles | Specialists (planning-specialist, invoicing-specialist, project-management-specialist, correspondence-specialist, etc.) |
| Each role's domain knowledge | Layer A scope (domain-keyed content) + adapter-bindings (per-role MCP corpus / external tool access) |
| Workflows for each role | Workflow definitions per specialist (per `arch/workflow-work-unit.md`) |
| Cross-role context | Cross-specialist composition rules + cross-specialist entity reads (per `arch/specialist-skill.md` §10) — "secretarial" specialist can read "accounting" specialist's state when needed |
| External role-specific tools | MCP-Server / A2A-Peer / Email / Accounting / File-Sync adapter classes (per workspace.md adapter_bindings) |
| Where work needs rigor | Authority-binding catalog + sparring activation matrix + quality-gate firing per shape policy |
| Where work doesn't need rigor | Engagement detection (per `1-NEXT.md` §5) — `pbs:` / skill triggers / slash commands fire ONLY for engaged work; routine work runs as plain Claude with zero overhead |
| Audit trail across roles | Single workspace audit-trail captures everything per Owner B placement; defensibility test reconstructs across roles |

So the framework's combination = **AI co-worker for one person playing multiple employee roles, with rigor-on-demand for the work that needs it**.

## 6. Composition + discipline composing via engagement detection

The composition substrate (§4) is the FOUNDATION. The disciplines (audit trail, sparring, authority-binding, quality-gate, defensibility) are LAYERS that activate based on engagement.

Concrete day:

- **Morning** — schedule client meeting (secretary role) → plain Claude work, zero discipline overhead
- **Mid-morning** — draft B-Plan-Begründung section (planning role + practitioner-shape) → full discipline (sparring per claim; audit captures reasoning; HUMAN attestation at claim_attested; defensibility reconstructible)
- **Afternoon** — generate monthly invoice (accounting role) → light discipline (audit captures; HUMAN attestation for send_authorized)
- **Evening** — project status update (PM role) → moderate discipline

Same workspace. Same practitioner-record. Same audit-trail. Different specialists active. Different engagement levels per the work's actual nature.

## 7. LLM-assisted bootstrap pattern

The audience constraint (§3) requires authoring without code. The framework's Mode 1 markdown authoring pattern (verified per `MAINTENANCE.md` Mode model + `arch/scope-model.md` Mode 1 placement) is necessary but not sufficient — markdown authoring still requires structured thinking that not all small-biz operators have time for.

**Bootstrap skill solution**: a `/pbs-setup` (or equivalent) skill that interviews the user in natural language, generates the markdown configuration, validates it, and commits it.

Concrete flow:

```
Skill prompts: "Tell me about your work. What roles do you play in your business?"
User: "I'm a solo planner. I draft B-Plan-Begründungen, manage projects,
       handle invoicing, coordinate with UNB and clients via email."

Skill: "What tools do you currently use for each role?"
User: "Outlook for email, custom Excel for project tracking,
       Word for documents, manual filing for archive."

Skill: "Which work needs professional defensibility (legal-bind, regulatory)?"
User: "B-Plan-Begründungen and Festsetzungen — I sign these and they go
       to authorities. Project status updates and invoicing are routine."

Skill GENERATES:
  - workspace.md with appropriate shape selection + adapter bindings + specialists_active
  - draft specialist DEFINITIONs for the named roles
  - draft Layer A scope (domains: planning, naturschutz, baurecht; states: DE-BB)
  - draft engagement-detection patterns (which work triggers full discipline vs light)

Skill VALIDATES + user REVIEWS + adjusts + commits.
```

This composes naturally with PBS's "AI-as-runtime" design principle (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1). The framework already commits to LLM applying configurations at runtime; bootstrap skill extends this to LLM GENERATING configurations from natural language.

**Critical observation**: bootstrap skill makes framework usable on day 1 without specialist marketplace bootstrapped. User provides natural language; LLM + framework primitives produce working deployment. Marketplace specialists become a multiplier ON TOP of usable-day-1 framework.

## 8. Three audience tiers

The audience constraint (§3) has three sub-tiers, each with different relationship to the framework:

| Tier | Role with PBS |
|---|---|
| **Solo / small-biz user** (no engineering capacity) | USES PBS via bootstrap skill + configuration; LLM generates their setup |
| **Small-biz with one technical person** (limited engineering capacity) | Above + may author custom specialists OR write specific configurations directly OR engage contractors for adapters |
| **Specialist / adapter authors** (engineering capacity OR domain expertise + markdown-writing) | Author specialists for marketplace; build adapters for niche tools; ship them for others to use |

The third tier is where the OSS contributor + paid-contractor ecosystem lives. Doesn't need to be huge — even 50-100 active specialist authors covering common verticals (planning + legal + accounting + research + healthcare + ...) makes the framework useful for thousands of solo/small-biz users.

PBS-Schulz pioneer (Gunther authoring planning specialists) IS the proof-of-concept for this pattern. One domain expert + markdown competence = first specialist set.

## 9. Configurable not codeable (with outsourcing path)

Hard architectural constraint: PBS authoring must default to configuration, not coding. Workspace.md + specialist DEFINITIONs + adapter bindings + Layer A content all authorable as structured markdown — verified `arch/scope-model.md` Mode 1 placement + `arch/specialist-skill.md:75-85` directory shape.

Coded modules — when genuinely necessary — get **outsourced**:

- **Custom adapter for niche tool**: developer follows `arch/adapter.md` per-class Surface contract; ships as Python package OR self-contained MCP server; user installs via package manager OR adds adapter binding URL
- **Custom specialist code (rare; most specialists are markdown-only)**: developer authors per `arch/specialist-skill.md` §2.3 directory shape; bundles any code as adapters; ships as specialist marketplace entry
- **Outsourced contributor doesn't need to learn the FRAMEWORK deeply** — they just need to follow the relevant Surface contract

This preserves the audience constraint (no engineering capacity required from the OPERATING organization) while keeping a path open for genuinely-coded modules to enter the ecosystem via outsourced contracts.

## 10. Event-driven coordination (architecturally preferred)

For cross-specialist coordination — e.g., "when Begründungs-specialist's work-unit ships, correspondence-specialist composes client email" — event-driven subscription is architecturally preferred over RPC-style cross-specialist invocation:

- **Event-driven** (preferred): Begründungs-specialist publishes work-unit state transition event; correspondence-specialist subscribes to relevant events independently. Producer doesn't need to know consumers exist.
- **RPC-style** (less clean): Begründungs-specialist explicitly calls correspondence-specialist's compose-email skill via fully-qualified reference. Couples producer to consumer.

Verified architectural support:
- Workflow_instance phase transitions are first-class events (per `arch/workflow-work-unit.md`)
- Audit-trail captures all events; subscription mechanisms exist for quality-gate + sparring observers
- Cross-specialist invocation via fully-qualified references is supported (per `arch/specialist-skill.md` §10) — but this is RPC-style; event-subscription pattern may be a load-bearing architectural surface that's currently underdeveloped

**Open architectural question for F2 specialist authoring**: which specialist OWNS the workflow that bridges multiple specialists' work? Per `arch/workflow-work-unit.md` SD-2 workflow_instances live at Owner B; workflow DEFINITIONs are nested in some specialist's bundle. Could be project-coordination specialist OR workspace-level workflow OR separate orchestrator-specialist. F2 specialist authoring will surface concretely.

## 11. Cross-tool entity resolution (depth-as-supported)

Verified via web research: cross-tool entity correlation ("when user says do Begründung for project X, how does specialist know which X you mean in PM tool") has a name (entity resolution / record linkage) and is a well-studied hard problem. Mature enterprise platforms use combinations of deterministic + probabilistic + ML-based matching + human-in-loop confirmation; no vendor claims to solve it perfectly.

PBS approach (architectural fit):

- **Workspace as Master Data anchor** — canonical entity IDs at Owner B per `arch/scope-model.md` identity convention (`owner_scope` + `owner_key`)
- **Adapter binding mapping tables** — per-tool ID mappings: "PBS project `hennigsdorf-2024` ↔ PM tool ID `ASA-1234` ↔ accounting tool ID `INV-customer-456`"
- **Bootstrap skill builds initial mappings** — LLM reads the user's existing tool state via adapter; suggests mappings; user confirms
- **LLM-assisted runtime resolution** — for ambiguous cases, LLM resolves via context (recent activity, name + state + temporal proximity); asks user to confirm if ambiguous; confirmation persists
- **Audit-trail of resolution events** — "system thought project X was Y; user corrected to Z" traceable for defensibility

Honest framing: **PBS provides the SUBSTRATE for cross-tool entity correlation; doesn't try to be a dedicated entity resolution engine**. Per-deployment user maintains mapping tables for their specific tool stack with framework + bootstrap-skill assistance. Sufficient for solo / small-biz scale; would lose to specialized entity resolution platforms (RecordLinker, Galaxy, Stardog) at enterprise scale.

## 12. Verified gap (composition-substrate niche)

Per session 35 web research, the verified landscape:

- **Generic AI tools** (ChatGPT, Claude, Notion AI): zero cross-domain context until manually fed; no workflow orchestration; no professional discipline
- **Microsoft Copilot**: Microsoft-ecosystem-locked; no help for hybrid setups
- **Notion AI**: Notion-ecosystem-locked
- **Vertical SaaS** (Harvey, Spellbook): vertical-locked; premium-priced; ready-made not composable; no cross-tool workflow integration with the user's other tools
- **Enterprise platforms** (Gemini Enterprise, MS Foundry): require engineering capacity to deploy; targeted at large orgs
- **Developer frameworks** (CrewAI, LangGraph): require coding to compose; not for end-user business owners
- **iPaaS for small business** (Zapier, Make): tool-to-tool automation; lack workflow orchestration discipline + professional-accountability layer + cross-domain context substrate

PBS's combination = **horizontal cross-vertical composition substrate, configuration-driven via LLM-bootstrap, self-hostable, open-source, with on-demand professional discipline + audit-trail spine + cross-tool context awareness for solo / small-biz organizations**.

Per multi-search this session: didn't find an existing project occupying this exact niche. (Not verified-exhaustive; could miss less-discoverable projects.)

## 13. What PBS is NOT

Explicit non-claims to prevent positioning drift:

- **NOT** competing with vertical SaaS (Harvey, Spellbook, etc.) — PBS composes WITH them via adapters
- **NOT** an enterprise context-graph platform (that was an earlier wrong framing)
- **NOT** a Harvey-for-planning OR vertical-specific ready-built tool
- **NOT** a developer framework requiring coding to compose (audience constraint forbids this)
- **NOT** a no-code / low-code GUI agent builder (different audience; different feature set)
- **NOT** trying to solve cross-tool entity resolution generically (provides substrate; depth is per-deployment)
- **NOT** betting on enterprise sales as primary go-to-market (architectural alignment exists for F4 enterprise track but speculative)
- **NOT** a self-contained AI runtime — leverages platform agent runtimes (Claude Agent SDK + MS Agent Framework + Gemini ADK) at the runtime infrastructure layer

## 14. Honest concerns

Compounded across today's articulations:

**1. Vertical SaaS API availability (critical)** — Harvey, Spellbook, etc. need to expose APIs (MCP / REST / A2A) for PBS to integrate them as adapters. Some do; some are platform-locked; some don't. Hard constraint.

**2. Adapter marketplace bootstrapping** — small-biz users need adapters for THEIR specific tool stack. Either PBS authors core adapters (limits initial audience to those tools), OR community builds them (chicken-and-egg), OR users build their own (breaks audience constraint). Mitigation: bootstrap skill makes framework useful day 1 without needing many adapters; marketplace grows as multiplier.

**3. Missing-tool friction** — if user uses tool X and no PBS adapter exists for X, they're stuck unless they pay someone to build one. Adapter coverage will always lag actual tool diversity. Honest expectation-setting.

**4. Bootstrap skill quality** — first specialist in PBS-Schulz pioneer; if poor quality, framework adoption fails at the front door. Authoring it well is high-stakes early work.

**5. LLM drift in generated configuration** — Claude is good at structured authoring but produces drift; bootstrap skill needs validation gates + user review. Trust-but-verify pattern.

**6. Coded-outsourcing market** — "outsourced developer for custom adapter" pattern requires discoverable contractors + pricing transparency. Nascent at best for small-biz users.

**7. Entity resolution depth** — perfect cross-tool entity correlation is unsolved at any scale. PBS supports up to a useful degree; users accept imperfection + manage via mapping tables + human confirmation.

**8. Authoring complexity threshold** — even with bootstrap skill, the configuration model has structural complexity (specialists × workflows × adapter bindings × Layer A scope × shape policies). Some users may find it too much. Risk: framework architecturally fits the audience but practically demands more discipline than the audience has time for.

**9. Cross-role context comes from AUTHORSHIP not magic** — for the AI to be cross-role aware, the user (or specialist authors) has to author specialists with composition declarations + adapter bindings + Layer A content. Framework provides the COMPOSITION SUBSTRATE; the user provides the actual cross-role wiring. Realistic expectation-setting.

These don't kill the positioning. They're real adoption challenges to face honestly.

## 15. F1+ implications (refines `1-NEXT.md`)

This positioning sharpens the F1+ plan in `1-NEXT.md`:

- **§3.5 framework positioning**: replace "thin-layer" framing with this composition-framework framing. Bottom-row substantive layer of the table is the whole framework value proposition.
- **F1.4 framework-level plugin content**: explicitly include bootstrap skill (or designate F1.5 candidate). User-onboarding gate; without it, audience constraint breaks.
- **F1.4 contract clarifications**: include "compose email about Entwurf XYZ shipping" as the load-bearing test case for whether F1 framework actually delivers the promised orchestration.
- **F2 specialist authoring discipline**: includes event-driven coordination preferred over RPC-style cross-specialist invocation; surfaces "which specialist owns the cross-bridging workflow" question concretely.
- **F2 specialist authoring**: bootstrap skill is itself the FIRST specialist authoring exercise — exercises specialist authoring patterns + tests architecture's authoring-via-skill discipline + produces load-bearing user-onboarding tool.
- **F3 packaging**: ship bootstrap skill in default plugin distribution. Tier 1 install includes it; first-run experience IS the bootstrap conversation.
- **F4 enterprise track**: repositioned — PBS could become REFERENCE for enterprise build (engineering teams adapt PBS architectural primitives), not direct-adoption target. Speculative; architectural alignment exists; not load-bearing for vision.
- **Cross-tool entity resolution**: F2 surfaces concretely how mapping-tables compose with adapter bindings + bootstrap skill assists initial mapping + audit-trail captures resolution events.

## 16. Sources

Verified web sources cited above:
- https://www.getgalaxy.io/articles/what-is-entity-resolution-techniques-tools-use-cases (entity resolution as enterprise term)
- https://en.wikipedia.org/wiki/Record_linkage (academic record linkage)
- https://recordlinker.com/what-is-entity-resolution/ (deterministic + probabilistic + ML approaches)
- https://www.rudderstack.com/blog/what-is-entity-resolution/ (best practices)
- https://composio.dev/content/ai-agent-integration-platforms-ipaas-zapier-agent-native (iPaaS landscape)
- https://zapier.com/blog/best-enterprise-integration-platforms/ (Zapier 2026 + Copilot)
- https://www.stacksync.com/blog/comparing-best-ipaas-solutions-for-small-to-mid-sized-business-integration (small-biz iPaaS)
- https://enigmatica.ai/compare/notion-ai-vs-microsoft-copilot (Notion-Copilot ecosystem-lock comparison)
- https://www.entrepreneur.com/growing-a-business/7-ai-tools-that-run-a-one-person-business-in-2026-no/501943 (solopreneur stack pattern)
- https://www.spellbook.legal/learn/ai-legal-compliance (defensibility as core legal AI requirement)
- https://aceds.org/agentic-ai-liability-managing-accountability-in-autonomous-legal-workflows-aceds-blog/ (AB 316 + agent accountability)
- https://diginomica.com/context-graphs-unlock-new-seam-enterprise-knowledge-ai-agents (context graphs — though enterprise scope; partial fit)
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank (Memory Bank user-scoped, NOT agent-to-agent)
- https://www.bain.com/insights/google_cloud_next_2026_the_agentic_enterprise_control_plane_comes_into_view/ (enterprise control plane)
- https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/ (Microsoft Agent Governance Toolkit framework-agnostic via PolicyProviderInterface)

Verified PBS framework files (read in session 35):
- `VISION.md`, `MAINTENANCE.md` (TOP-LEVEL ARCHITECTURE + DESIGN PRINCIPLES + MILESTONE STRUCTURE + SCOPE), `arch/scope-model.md`, `arch/specialist-skill.md`, `arch/practitioner.md`, `arch/adapter.md`, `arch/audit.md`, `arch/sparring.md`, `arch/quality-gate.md`, `arch/workflow-work-unit.md`, `pbs/manifests/workspace.py`, `pbs/manifests/specialist.py`, `pbs/impls/practitioner_shape_authority_binding.py`, SDK types.py + README + plugin example

## 17. Honest basis caveats

- **Verified directly** (web sources cited in §16 + session 35 framework reads): all architectural primitive citations; landscape competitor positioning; entity resolution patterns; enterprise platform offerings; legal-vertical AI players; AB 316 + EU AI Act regulatory context; defensibility as industry consensus
- **Inferred but high-confidence**: composition-framework positioning as the strongest framing reached today — derived from arc of vision sharpening + verified architectural fit + verified gap in competitive landscape
- **Inferred but high-confidence**: PBS architectural primitives support the integration-first positioning — explicit in adapter Pattern A + workspace.md adapter_bindings + cross-specialist composition + Layer A scope + audit-trail integration
- **Inferred reasonably**: bootstrap skill flow + LLM-assisted entity resolution + multi-role mapping table — derived from existing PBS primitives composing; not articulated as specific worked patterns in arch docs
- **Inferred and uncertain**: that the niche between solo-with-no-tooling and enterprise-with-engineering-team is sufficiently large to be community-viable — based on general SMB-tooling market patterns; not measured for PBS specifically; needs validation
- **Inferred and uncertain**: that LLM-bootstrap + LLM-runtime-entity-resolution actually deliver enough value with low enough friction — needs prototype validation at F1.5 / F2
- **Not verified**: actual API availability of common vertical SaaS (Harvey, Spellbook, etc.) — might be enterprise-only; could limit integration audience
- **Not verified**: that audience constraint (no engineering capacity, configuration-only) is achievable while preserving framework expressive power — ongoing tension; worth surfacing if F1+ implementation forces breaking it
- **Not verified**: that markdown-only authoring (option A from prior turn discussion) is acceptable for the audience even with bootstrap-skill assistance — Gunther's experience is one data point; broader validation needed
- **Not verified**: that adapter marketplace network effects can be bootstrapped without commercial incentives — speculation; OSS marketplace patterns vary widely

## 18. Net

PBS framework's positioning has converged through session 35 across multiple turns into a coherent vision: **composition substrate for solo / small-business operators (no engineering capacity) to integrate existing tools (vertical SaaS + PM tools + email + corpus + accounting + agents) into AI-supported workflows where one person plays multiple employee roles, with cross-tool / cross-role context awareness, on-demand professional discipline (audit trail + sparring + authorship preservation), LLM-assisted bootstrap, configuration-only authoring with outsourceable code modules, event-driven cross-specialist coordination, open standards (MCP + A2A) for tool integration, open-source self-hostable, composes WITH vertical SaaS rather than competing.**

The crisp anchor: "compose email about Entwurf XYZ shipping" as a single user request triggering coordinated cross-tool action because workspace context is the framework's spine.

Verified gap exists in the competitive landscape — no project occupying this exact niche per multi-search this session. Honest concerns named (§14). F1+ implications captured (§15) for next-session integration into 1-NEXT.md.

This document supersedes earlier framings (`1-NEXT.md` §3.5 thin-layer; `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md`) — both were stages in the vision-sharpening; this is the integration-first composition-substrate framing reached.
