# 4-PRELIMINARY-COMPOSITION-FRAMEWORK

> **Status**: Preliminary positioning document. Captures session 35 (post-2026-05-06) vision sharpening across multiple turns + competitive verification that progressively NARROWED the claimed positioning to its honestly-defensible core. Final framing: **"composition substrate for solo / small-business operators in regulated professions where self-host + open-source + cross-vendor + practitioner-discipline matters."** Supersedes earlier framings in `1-NEXT.md` §3.5 and `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md`.
>
> **Major correction from initial 4- draft**: today's competitive research verified that Microsoft Copilot Studio + Claude Cowork already provide cross-tool orchestration + persisted workflows + reusable agents + audit trails today. The "PBS uniquely solves cross-tool composition for small biz" framing was wrong. PBS's honestly-defensible value is narrower — see §12 + §12.5 + §13.
>
> **Companion documents**:
> - `1-NEXT.md` — working session handoff + F1-F4 plan; §3.5 positioning to be revised per this doc
> - `2-PRELEMINARY-ENTRERPRISE.md` — enterprise platform landscape research
> - `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md` — earlier "context-graph" framing; subsumed
> - This file — vision-level positioning + audience definition + competitive verification + empirical test plan + honest concerns

---

## 1. The vision in one paragraph (honestly narrowed)

PBS framework is a **composition substrate** that lets a solo professional or small business (1-10 people, no engineering capacity) build their own AI-supported workspace where one person plays multiple employee roles (secretary + accounting + planning + project manager + domain expert + ...). It composes existing tools via open standards (MCP + A2A) + adapter Pattern A; maintains cross-tool / cross-role context within the deployment; applies on-demand professional discipline (audit trail + sparring + authorship preservation) for work that needs rigor — without burdening routine work. **Distinct from Microsoft Copilot Studio + Claude Cowork primarily on**: self-hosting + open-source + cross-vendor + sparring/defensibility-grade discipline + engagement-detection + zero per-user cost. Setup is configuration-driven (LLM-assisted bootstrap skill generates markdown configuration); coding only when genuinely necessary and outsourceable. Composes WITH vertical SaaS (Harvey-equivalents) rather than competing.

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
2. Sparring engagement IF the message warrants rigor (engagement detection per `1-NEXT.md` §5)
3. Practitioner reviews; framework respects axis-3 (practitioner remains author)
4. Send: `claim_attested` requires HUMAN actor per practitioner-shape authority-binding catalog → practitioner approves; `send_authorized` event captures
5. Email-adapter dispatches; PM-tool-adapter receives workflow phase transition → updates PM tool's project entry
6. Audit-trail captures: claim_made + send_authorized + workflow_phase_transition events as one coherent chain

**Critical correction from earlier framing**: this scenario IS solvable today in Claude Cowork (Feb 2026 cross-app workflows) and Microsoft Copilot Studio (Wave 3 multi-step agent flows). The example illustrates PBS's intended workflow but does NOT prove unique-capability differentiation — see §12 + §12.5 for honest competitive comparison.

## 3. Audience

The discriminator is **engineering capacity to build custom integration infrastructure**, NOT company size:

| Audience | Engineering capacity | Buy / build | PBS fit |
|---|---|---|---|
| Solo / 1-10 person firms | None | Buys / configures only | **Possible PBS audience** — IF other differentiators (self-host, open-source, etc.) matter to them |
| 10-50 person firms | None (no dedicated AI eng team) | Buys / configures | Same as above |
| 50-500 person firms | Maybe (small AI-curious team) | Mixed | Maybe — depends on config-vs-code feel |
| 500+ enterprise | Yes | Builds custom | NOT PBS audience — they roll their own; PBS could be REFERENCE for their build, not direct-adoption target |

**Operational corollary**: if PBS targets organizations without engineering capacity to BUILD their own integration, then PBS itself must require minimal engineering to OPERATE:

- Self-hosting: one-command-install or docker-compose
- Updates: self-updating, no "pull and rebuild"
- Configuration: markdown text-edit, not code-edit
- Failures: user-readable errors, not stack traces
- Specialist installation: one-command (`pbs-cli install specialist@version` or equivalent)

**Honest narrowing**: the audience is further narrowed by the OTHER differentiators that distinguish PBS from Cowork/Copilot Studio. Audience = small biz WITHOUT engineering capacity AND who values self-hosting OR open-source OR cross-vendor OR specific practitioner-discipline. The intersection is real but smaller than "all small biz."

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
| Cross-role context | Cross-specialist composition rules + cross-specialist entity reads (per `arch/specialist-skill.md` §10) |
| External role-specific tools | MCP-Server / A2A-Peer / Email / Accounting / File-Sync adapter classes (per workspace.md adapter_bindings) |
| Where work needs rigor | Authority-binding catalog + sparring activation matrix + quality-gate firing per shape policy |
| Where work doesn't need rigor | Engagement detection (per `1-NEXT.md` §5) — fires ONLY for engaged work; routine work runs as plain Claude with zero overhead |
| Audit trail across roles | Single workspace audit-trail captures everything per Owner B placement |

So the framework's combination = **AI co-worker for one person playing multiple employee roles, with rigor-on-demand for work that needs it**.

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

**Bootstrap skill solution**: a `/pbs-setup` (or equivalent) skill that interviews the user in natural language, generates the markdown configuration, validates it, and commits it. Concrete flow: skill prompts about roles + tools + rigor needs; generates workspace.md + draft specialist DEFINITIONs + adapter bindings; user reviews + commits.

**Honest narrowing surfaced today**: Microsoft Copilot Studio offers **visual low-code workflow builder** (drag-drop + natural-language description; system generates the agent + workflow definition). Visual low-code is probably MORE accessible than markdown for non-coder audiences than my "bootstrap skill makes markdown approachable" framing implied. PBS's accessibility argument narrows: the audience that prefers markdown-based authoring (perhaps because they want the configuration to be diffable / version-controlled / portable / open-format) is a sub-audience of the no-engineering-capacity audience.

## 8. Three audience tiers

The audience constraint (§3) has three sub-tiers, each with different relationship to the framework:

| Tier | Role with PBS |
|---|---|
| **Solo / small-biz user** (no engineering capacity) | USES PBS via bootstrap skill + configuration; LLM generates their setup |
| **Small-biz with one technical person** (limited engineering capacity) | Above + may author custom specialists OR write specific configurations directly OR engage contractors for adapters |
| **Specialist / adapter authors** (engineering capacity OR domain expertise + markdown-writing) | Author specialists for marketplace; build adapters for niche tools; ship them for others to use |

PBS-Schulz pioneer (Gunther authoring planning specialists) IS the proof-of-concept for the third tier pattern.

## 9. Configurable not codeable (with outsourcing path)

Hard architectural constraint: PBS authoring defaults to configuration, not coding. Workspace.md + specialist DEFINITIONs + adapter bindings + Layer A content all authorable as structured markdown — verified `arch/scope-model.md` Mode 1 placement + `arch/specialist-skill.md:75-85` directory shape.

Coded modules — when genuinely necessary — get **outsourced**:

- **Custom adapter for niche tool**: developer follows `arch/adapter.md` per-class Surface contract; ships as Python package OR self-contained MCP server; user installs via package manager OR adds adapter binding URL
- **Custom specialist code (rare; most specialists are markdown-only)**: developer authors per `arch/specialist-skill.md` §2.3 directory shape; bundles any code as adapters; ships as specialist marketplace entry

This preserves the audience constraint (no engineering capacity required from the OPERATING organization) while keeping a path open for genuinely-coded modules to enter the ecosystem via outsourced contracts.

## 10. Event-driven coordination (architecturally preferred)

For cross-specialist coordination — e.g., "when Begründungs-specialist's work-unit ships, correspondence-specialist composes client email" — event-driven subscription is architecturally preferred over RPC-style cross-specialist invocation:

- **Event-driven** (preferred): producer publishes work-unit state transition event; consumers subscribe to relevant events independently
- **RPC-style** (less clean): producer explicitly calls consumer's skill via fully-qualified reference; couples producer to consumer

Verified architectural support: workflow_instance phase transitions are first-class events (per `arch/workflow-work-unit.md`); audit-trail captures all events; subscription mechanisms exist for quality-gate + sparring observers. Cross-specialist invocation via fully-qualified references is supported (per `arch/specialist-skill.md` §10) — but this is RPC-style; event-subscription pattern may be a load-bearing architectural surface that's currently underdeveloped — open question for F2.

## 11. Cross-tool entity resolution (depth-as-supported)

Verified via web research: cross-tool entity correlation has a name (entity resolution / record linkage) and is a well-studied hard problem. Mature enterprise platforms use combinations of deterministic + probabilistic + ML-based matching + human-in-loop confirmation; no vendor claims to solve it perfectly.

PBS approach (architectural fit):

- **Workspace as Master Data anchor** — canonical entity IDs at Owner B per `arch/scope-model.md` identity convention
- **Adapter binding mapping tables** — per-tool ID mappings: "PBS project `hennigsdorf-2024` ↔ PM tool ID `ASA-1234` ↔ accounting tool ID `INV-customer-456`"
- **Bootstrap skill builds initial mappings** — LLM reads existing tool state via adapter; suggests mappings; user confirms
- **LLM-assisted runtime resolution** — for ambiguous cases, LLM resolves via context; asks user to confirm if ambiguous; confirmation persists
- **Audit-trail of resolution events** — "system thought project X was Y; user corrected to Z" traceable for defensibility

Honest framing: PBS provides the SUBSTRATE for cross-tool entity correlation; doesn't try to be a dedicated entity resolution engine. Sufficient for solo / small-biz scale.

## 12. Verified competitive landscape (HONEST NARROWING from initial 4- draft)

Today's competitive verification narrowed the claimed positioning. Honest landscape:

### Verified — Claude Cowork (Feb-Apr 2026 release wave)

Per [Claude Cowork connectors](https://claude.com/connectors) + [Cowork guide](https://findskill.ai/blog/claude-cowork-guide/) + [coworkerai integrations](https://coworkerai.io/connectors):

- Cross-app workflows in single session ("analyze Excel → build PowerPoint → draft Outlook email all within a single Cowork session")
- 50+ connectors as of Feb 2026 (Outlook, SharePoint, OneDrive, Slack, DocuSign, Salesforce, HubSpot, Asana, Atlassian, etc.)
- Cross-app context maintained within session
- Audit logging via Microsoft Purview (when configured) + OpenTelemetry built-in
- General availability on macOS + Windows April 9, 2026 with role-based access controls
- Memory Bank user-scoped (NOT agent-to-agent) per Google docs and Anthropic positioning

### Verified — Microsoft Copilot Studio (2026 Wave)

Per [Microsoft Learn agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview) + [agent node](https://learn.microsoft.com/en-us/power-platform/release-plan/2026wave1/microsoft-copilot-studio/invoke-agents-as-workflow-steps-agent-node):

- **First-class persisted workflows** ("agent flows") — defined steps, branching logic, handoffs, audit trail
- **Reusable agents** callable as workflow steps; workflows callable as agent tools
- **Cross-agent delegation** via open protocol (universal access)
- **Multi-agent orchestration** — Cowork framework for asynchronous collaboration with shared context, task handoffs
- **Visual low-code builder** (drag-drop + natural-language description; system generates agent + workflow definition)
- **HITL approval mechanisms** for enterprise accountability
- **Audit dashboards** built into Microsoft 365 governance
- Microsoft 365 ecosystem-locked

### Verified — Bauleitplanung-specific tools landscape (2026)

Per [Phase0 architectural AI guide](https://www.phase0.com/blog/kuenstliche-intelligenz-fur-architektinnen) + [TGA Fachplaner](https://www.tga-fachplaner.de/planungsbuero/kuenstliche-intelligenz-smarte-planungshelfer-ki-der-bauplanung) + [Hendel + Partner](https://www.hendelundpartner.de/kuenstliche-intelligenz-in-der-bauleitplanung/):

- **Generic AI tools applied to planning** (ChatGPT, Claude, Microsoft Copilot used in Planungsbüros for routine work) — well-documented
- **Use cases**: protocol creation, contract analysis, administration, knowledge management, project work
- **Vertical-specific Bauleitplanung AI infrastructure**: NOT FOUND in search
  - No B-Plan-Begründung-specific drafting tool with BauGB-aware corpus
  - No Bauleitplanung workflow phase modeling (Vorentwurf → Entwurf → Satzungsbeschluss → Genehmigung) as first-class entity
  - No LaTeX-compile-aware planning document workflows
  - No German Berufsrecht-defensibility-grade audit primitives for planning work
  - No specialist marketplace with planning-domain specialists

The landscape is generic AI tools applied to planning, NOT planning-specific AI infrastructure. The vertical-specific layer for Bauleitplanung is largely empty.

## 12.5 Honest competitive comparison table

After verification, where PBS genuinely differs vs Cowork / Copilot Studio:

| Concern | Claude Cowork | Microsoft Copilot Studio | PBS |
|---|---|---|---|
| Cross-app workflow within session | ✓ | ✓ | ✓ |
| First-class persisted workflows | Partial (skills + plugins) | ✓ (agent flows) | ✓ (workflow DEFINITIONs in specialist bundle) |
| Reusable agents | ✓ | ✓ | ✓ (specialists) |
| Connector ecosystem | 50+ ecosystem | M365 + Copilot Studio agents | Open standards (MCP universal); per-deployment configurable |
| Cross-agent delegation | Within Cowork | Open protocol | A2A universal |
| Audit trail | OpenTelemetry + Purview when configured | ✓ Microsoft 365 governance | Hash-chain integrity + claim attribution chain (verified) |
| Visual low-code authoring | ✗ | **✓** | ✗ (markdown) |
| HITL approval at gates | ✓ | ✓ | ✓ (authority-binding catalog) |
| Hosting | SaaS only | Azure-required for full features | **Self-hostable Tier 1** |
| Vendor lock-in | Yes (Anthropic ecosystem) | Yes (Microsoft ecosystem) | **Cross-vendor via open standards** |
| Open-source | ✗ | ✗ | **✓** |
| Sparring discipline (8 sub-mechanisms; counter-argument; anti-sycophancy; etc.) | Generic governance | Generic governance + HITL | **✓ load-bearing runtime mechanism** |
| Defensibility test reconstruction (claim attribution chain for 6-month-later audit) | Partial via audit logging | Partial via Purview | **✓ first-class architectural commitment** |
| Engagement detection (rigor-on-demand vs always-on governance) | Always-on if configured | Always-on if configured | **✓ specific architectural commitment** |
| Domain-customized specialists for regulated profession-specific work | Custom Cowork agents | Custom Copilot Studio agents (visual) | **✓ Mode 1 markdown specialist authoring; full deployment-side customization** |
| Cost (solo / small biz) | Cowork Pro $15-200/mo | M365 Copilot $30/mo + Studio agent costs | Free framework + self-host costs |

**Honest reading**: Cowork and Copilot Studio cover MOST of the orchestration / persistence / audit / agent-reuse capabilities I claimed PBS uniquely offered. PBS's verified-unique features narrow to:

- **Self-hosted** (data stays with practitioner; data sovereignty; regulated industries that can't legally use SaaS)
- **Open-source** (no vendor lock-in; auditable code; forkable; community-extensible)
- **Cross-vendor** (works across Claude + MS Foundry + Gemini ecosystems via open standards; verified architectural commitment via Pattern A substrate plurality + MCP universal + A2A universal)
- **Sparring discipline as load-bearing runtime mechanism** (the 8 sub-mechanisms; verified `arch/sparring.md` + practitioner_shape_sparring.py)
- **Defensibility test reconstruction** (claim-attribution chain across roles for 6-month-later audit; specifically architecturally committed vs Cowork/Copilot's generic audit logging)
- **Engagement detection** (rigor-on-demand; framework enforcement scopes to engaged work only)
- **Mode 1 markdown specialist authoring with deployment-side customization depth** (more flexible than visual low-code for power users; less accessible for casual users)
- **Free** (vs commercial subscription)

These remain real differentiators. They're a NARROWER value proposition than "we solve cross-tool orchestration." Cowork and Copilot Studio already solve cross-tool orchestration.

## 12.7 Empirical test plan (the actual settling mechanism)

Theoretical comparison kept narrowing the value claim. The empirical attempt would settle whether even the narrow remaining differentiation is real.

**Test scenario**: build PBS-Schulz workflow equivalent for ONE concrete planning task — drafting + reviewing + sending one section of a B-Plan-Begründung — using either Claude Cowork OR Microsoft Copilot Studio.

**9 specific things to try + observe**:

| # | Test | Predicted outcome | What it settles |
|---|---|---|---|
| 1 | **Domain corpus access**: connect a BauGB / BNatSchG / DE-BB regional regulation corpus to the AI tool | Likely needs custom MCP; nobody ships planning-specific corpus connectors | If gap real: PBS's specialist + adapter pattern lets community/contractor build the corpus adapter; solo planner doesn't have to |
| 2 | **LaTeX compile workflow**: AI tool integrates with LaTeX pipeline for Begründung output | Probably no native support | If gap real: PBS's adapter framework supports custom LaTeX compile adapter |
| 3 | **B-Plan workflow phases**: model Vorentwurf → Entwurf → Satzungsbeschluss as persistent workflow with attestation gates | MS Copilot Studio agent-flows can probably model phases; HITL approval at gates probably works | If Cowork/Copilot succeed: PBS's workflow primitives don't differentiate here |
| 4 | **Cross-section consistency**: AI knows about Festsetzungen section while drafting Begründung section, automatically | Depends on what context AI has access to within session | Tests cross-document context maintenance depth |
| 5 | **Sparring discipline**: enforce "every claim in this section must have counter-arguments generated and rejected before lock" | Cowork/Copilot probably don't have this as primitive; would need custom workflow logic | If gap real: PBS's 8 sub-mechanisms + activation matrix is genuine differentiation |
| 6 | **HUMAN attestation at legal-bind moments**: require human approval before send_authorized | Both have HITL; works | Cowork/Copilot probably succeed; not differentiator |
| 7 | **Defensibility-grade audit**: audit reconstructs "what reasoning led to this specific paragraph six months later" | Audit captures actions; whether it captures REASONING chains depends on what's logged | Critical test of PBS's claim-attribution-chain architectural commitment vs generic action-logging |
| 8 | **Cost realistic for solo planner**: Cowork Pro $15-30/mo OR M365 Copilot $30/mo + Studio agent costs separately | Both substantial for solo | Tests cost-sensitivity argument for PBS |
| 9 | **Data residency**: deployment guarantees data stays in DE-EU jurisdiction for client confidentiality | Both vendors offer EU residency for enterprise tiers; small-biz tiers may not | Tests data-sovereignty argument |

**Predicted outcome**: items 1-2 (domain corpus + LaTeX) probably WON'T work without custom dev. Items 5-7 (sparring + defensibility-grade audit) probably won't work to PBS's discipline depth. Items 3-4-6-8-9 probably mostly WORK in either platform.

If that prediction holds, PBS's empirically-verified value isn't in items 3/4/6 (cross-tool composition + workflow persistence + HITL — Cowork/Copilot deliver these). It's in items 1/2/5/7/8/9 (domain-specific extensibility + practitioner-discipline + defensibility-grade audit + cost + data residency).

**Suggestion**: pick item 5 (sparring discipline) AND item 7 (defensibility-grade audit reconstruction) as the priority empirical tests since these are PBS's claimed unique-discipline differentiation. If Cowork/Copilot can deliver these via custom agent design, PBS's discipline-specific value claim collapses. If they genuinely can't, that's verified unique value for the regulated-profession audience.

## 13. What PBS is NOT (corrected per today's verification)

Explicit non-claims to prevent positioning drift:

- **NOT** uniquely solving cross-tool orchestration for small biz (verified — Cowork + Copilot Studio do this today)
- **NOT** uniquely solving workflow persistence + reusable agents (verified — Copilot Studio agent flows do this today)
- **NOT** competing with vertical SaaS (Harvey, Spellbook, etc.) — PBS composes WITH them via adapters
- **NOT** an enterprise context-graph platform (that was an earlier wrong framing)
- **NOT** a Harvey-for-planning OR vertical-specific ready-built tool
- **NOT** a developer framework requiring coding to compose
- **NOT** a no-code GUI agent builder (different audience; that's Copilot Studio's territory)
- **NOT** providing better visual authoring UX than Copilot Studio (Mode 1 markdown vs visual drag-drop — Copilot Studio wins on accessibility for casual users)
- **NOT** trying to solve cross-tool entity resolution generically (provides substrate; depth is per-deployment)
- **NOT** betting on enterprise sales as primary go-to-market (architectural alignment exists for F4 enterprise track but speculative)
- **NOT** a self-contained AI runtime — leverages platform agent runtimes (Claude Agent SDK + MS Agent Framework + Gemini ADK) at the runtime infrastructure layer

## 14. Honest concerns

Compounded across today's articulations + verifications:

**1. Vertical SaaS API availability (critical)** — Harvey, Spellbook, etc. need to expose APIs (MCP / REST / A2A) for PBS to integrate them as adapters. Hard constraint.

**2. Adapter marketplace bootstrapping** — chicken-and-egg problem. Mitigation: bootstrap skill makes framework useful day 1 without needing many adapters.

**3. Missing-tool friction** — adapter coverage will always lag actual tool diversity. Honest expectation-setting.

**4. Bootstrap skill quality** — first specialist authored; high-stakes early work.

**5. LLM drift in generated configuration** — needs validation gates + user review.

**6. Coded-outsourcing market** — requires discoverable contractor network for niche adapters; nascent.

**7. Entity resolution depth** — perfect cross-tool entity correlation is unsolved at any scale.

**8. Authoring complexity threshold** — even with bootstrap skill, configuration model has structural complexity that may exceed audience tolerance.

**9. Cross-role context comes from AUTHORSHIP not magic** — framework provides the substrate; user provides the actual cross-role wiring.

**10. (NEW today)** **Visual low-code authoring loss** — Microsoft Copilot Studio offers visual drag-drop workflow building. PBS's markdown approach loses to visual on accessibility for casual non-coder users. PBS's audience is the markdown-preferring sub-audience (version-control / portable / open-format preference).

**11. (NEW today)** **Workflow persistence is no longer a differentiator** — verified Copilot Studio has first-class persisted workflows. PBS's "we have first-class workflow persistence" claim collapses; remaining differentiation is in the SHAPE / DISCIPLINE of those workflows, not their existence.

**12. (NEW today)** **The audience-intersection niche may be too small** — combining all verified-unique differentiators (self-host + open-source + cross-vendor + sparring + engagement-detection + free + markdown-preference + regulated-profession + small-biz) yields a tight niche. Audience size unverified; could be too small for community / OSS sustainability.

**13. (NEW today)** **Empirical verification is required, not theoretical** — today's theoretical narrowing settled progressively; the EMPIRICAL test (build PBS-Schulz workflow in Cowork/Copilot Studio per §12.7) is what actually settles whether the narrowed differentiation is real or whether even those gaps close with sufficient custom agent design.

These don't kill the positioning. They're real adoption challenges + market-size constraints to face honestly.

## 15. F1+ implications (refines `1-NEXT.md`)

This positioning sharpens the F1+ plan in `1-NEXT.md` (with today's corrections):

- **§3.5 framework positioning**: replace "thin-layer" framing with the §12.5 honest competitive comparison. Framework value is in the bottom rows of that table (verified-unique features), not in claims of cross-tool orchestration uniqueness.
- **F1.4 framework-level plugin content**: explicitly include bootstrap skill (or designate F1.5 candidate). User-onboarding gate.
- **F1.4 contract clarifications**: items 5 (sparring discipline) + 7 (defensibility-grade audit) per §12.7 become the load-bearing test cases for whether F1 framework actually delivers PBS's verified-unique value.
- **F2 specialist authoring discipline**: includes event-driven coordination preferred over RPC-style cross-specialist invocation; surfaces "which specialist owns the cross-bridging workflow" question concretely.
- **F2 specialist authoring**: bootstrap skill IS the FIRST specialist authoring exercise.
- **F3 packaging**: ship bootstrap skill in default plugin distribution.
- **F4 enterprise track**: repositioned — PBS could become REFERENCE for enterprise build, not direct-adoption target. Speculative.
- **Cross-tool entity resolution**: F2 surfaces concretely how mapping-tables compose with adapter bindings.
- **(NEW today)** **Empirical test plan from §12.7**: F1.4 OR F2.0 includes empirical verification — actually try to build the planning workflow in Cowork OR Copilot Studio first; document where each falls short; THAT becomes the load-bearing differentiation evidence for PBS's value vs unverified claims.
- **(NEW today)** **Bauleitplanung-specific corpus + LaTeX adapter** (per §12.7 items 1+2) become candidate Phase 6.2-equivalent work — these are the per-deployment vertical-specific extensibility points where PBS has architectural advantage IF the corpus + LaTeX adapters are built.

## 16. Sources

Verified web sources cited above:

**Cowork capabilities + ecosystem**:
- https://claude.com/connectors
- https://findskill.ai/blog/claude-cowork-guide/
- https://coworkerai.io/connectors

**Microsoft Copilot Studio + Cowork**:
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- https://learn.microsoft.com/en-us/power-platform/release-plan/2026wave1/microsoft-copilot-studio/invoke-agents-as-workflow-steps-agent-node
- https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/automate-business-processes-with-agents-plus-workflows-in-microsoft-copilot-studio/
- https://spicyadvisory.com/blog/microsoft-copilot-cowork-guide-2026
- https://harness-engineering.ai/blog/microsofts-copilot-cowork-ai-agent-workflows/

**Bauleitplanung / German planning AI landscape**:
- https://www.phase0.com/blog/kuenstliche-intelligenz-fur-architektinnen
- https://www.tga-fachplaner.de/planungsbuero/kuenstliche-intelligenz-smarte-planungshelfer-ki-der-bauplanung
- https://www.hendelundpartner.de/kuenstliche-intelligenz-in-der-bauleitplanung/
- https://www.ai-heroes.co/de/blog/microsoft-copilot-cowork-vs-claude-cowork

**Earlier-session verified sources** (entity resolution, enterprise landscape, etc.):
- https://www.getgalaxy.io/articles/what-is-entity-resolution-techniques-tools-use-cases
- https://en.wikipedia.org/wiki/Record_linkage
- https://composio.dev/content/ai-agent-integration-platforms-ipaas-zapier-agent-native
- https://zapier.com/blog/best-enterprise-integration-platforms/
- https://enigmatica.ai/compare/notion-ai-vs-microsoft-copilot
- https://www.entrepreneur.com/growing-a-business/7-ai-tools-that-run-a-one-person-business-in-2026-no/501943
- https://www.spellbook.legal/learn/ai-legal-compliance
- https://aceds.org/agentic-ai-liability-managing-accountability-in-autonomous-legal-workflows-aceds-blog/
- https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank
- https://www.bain.com/insights/google_cloud_next_2026_the_agentic_enterprise_control_plane_comes_into_view/

Verified PBS framework files (read in session 35):
- `VISION.md`, `MAINTENANCE.md`, `arch/scope-model.md`, `arch/specialist-skill.md`, `arch/practitioner.md`, `arch/adapter.md`, `arch/audit.md`, `arch/sparring.md`, `arch/quality-gate.md`, `arch/workflow-work-unit.md`, `pbs/manifests/workspace.py`, `pbs/manifests/specialist.py`, `pbs/impls/practitioner_shape_authority_binding.py`, SDK types.py + README + plugin example

## 17. Honest basis caveats

- **Verified directly via web sources cited in §16**: all competitive landscape claims (Cowork capabilities, Copilot Studio agent flows, Bauleitplanung tool absence, entity resolution patterns); regulatory pressure (AB 316; EU AI Act); enterprise platform landscape
- **Verified directly via session 35 framework reads**: PBS architectural primitives + their substantive design work
- **Inferred but high-confidence**: that PBS's verified-unique features per §12.5 (self-host + open-source + cross-vendor + sparring + defensibility + engagement-detection + free + markdown-authoring + cost + data-residency) are real differentiators — derived from competitive comparison; would benefit from empirical verification per §12.7
- **Inferred and uncertain**: that Cowork/Copilot Studio CANNOT deliver PBS's sparring discipline + defensibility-grade audit reconstruction via custom agent design — based on reading their governance docs at search-result level; could be present but undermarketed; needs empirical verification
- **Inferred and uncertain**: market size for the verified-unique-feature intersection — speculation; based on general SMB-tooling market patterns + regulated-profession-with-self-host-need patterns
- **Not verified**: actual feasibility of building German Bauleitplanung workflow in Cowork OR Copilot Studio — needs empirical attempt per §12.7 test plan
- **Not verified**: GDPR / data-residency capabilities of Cowork + MS Copilot at small-biz subscription tiers (vs enterprise) — may partially close the data-sovereignty gap
- **Not verified**: that visual low-code accessibility in Copilot Studio actually translates to better small-biz adoption than markdown — depends on user comfort patterns; not measured
- **Not verified**: that Bauleitplanung corpus connectors + LaTeX integration would be commercially-developed for Cowork/Copilot if PBS doesn't exist — could be filled by general-purpose vertical SaaS or by user-built custom MCPs

## 18. Net (HONESTLY NARROWED)

PBS framework's vision converged through session 35 across multiple turns of progressive narrowing via competitive verification:

- Initial framing: thin-layer over platforms (wrong; underclaimed)
- Second framing: context-graph for accountability work (too narrow; enterprise-flavored)
- Third framing: composition substrate for solo / small-biz with cross-domain awareness (overclaimed; Cowork + Copilot Studio do this)
- **Final honest framing**: composition substrate for solo / small-business operators in regulated professions where the specific intersection of (self-host + open-source + cross-vendor + sparring/defensibility-discipline + engagement-detection + zero per-user cost + markdown-preference) matters

The crisp anchor example ("compose email about Entwurf XYZ shipping") IS solvable in Cowork + Copilot Studio today. PBS's value isn't that it solves this example; it's that it solves it under deployment constraints + with discipline specifics that Cowork/Copilot don't ship.

The verified competitive landscape: Cowork + Copilot Studio cover most of the cross-tool orchestration + workflow persistence + audit trail capabilities. PBS's verified-unique value narrows to: deployment model (self-hosted, open-source, cross-vendor, free) + specific disciplines (sparring 8 sub-mechanisms; defensibility test reconstruction; engagement-detection rigor-on-demand) + Bauleitplanung-style vertical-specific extensibility (where vertical-specific AI infrastructure is largely absent in 2026 landscape).

The empirical test plan (§12.7) is what actually settles whether these narrowed differentiations are real, by attempting to build the PBS-Schulz workflow in Cowork OR Copilot Studio and documenting where they fall short. F1.4 or F2.0 should include this empirical verification BEFORE claiming PBS unique value to anyone (including yourself).

Honest concerns (§14) include 4 NEW concerns surfaced today: visual low-code accessibility loss; workflow persistence no longer a differentiator; audience-intersection niche may be too small; empirical verification required not theoretical.

This document supersedes earlier framings (`1-NEXT.md` §3.5 thin-layer; `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md`) — those were stages in the vision-sharpening; this is the integration-first composition-substrate framing reached AND honestly competitive-verified.
