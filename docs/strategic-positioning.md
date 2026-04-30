# Strategic positioning — pbs-bureau as consulting IP

**Status**: working document (session 9 initial; substantial rewrite session 13 per #22 Sub-DR B; further substantial rewrite session 14 per `docs/decisions/closest-neighbors-deep-read.md` + `docs/decisions/shape-extension-and-architectural-floor.md` + `docs/decisions/vision-realignment-session14.md`). Strategic discussion captured for durability across sessions. Distinct from `ARCHITECTURE.md` (technical architecture) and `ROADMAP.md` (commitment queue) — this doc covers **how the work positions in the consulting market** and **what consulting offerings flow from it**.

**Operating geography**: EU, mainly Germany (DACH primary).

This is a living document. Update when strategy refines; review periodically for drift.

---

## Layered approach — framework breadth + positioning narrowness (locked session 14)

**Critical distinction** that shapes everything below:

| Layer | Property | Truth |
|---|---|---|
| **Open source framework** | Workspace-shape-NEUTRAL | Architectural reality — primitives support any shape (practitioner / autonomous-business / personal-OS / knowledge-graph / federation / hybrid); community can build for any audience via shape-extension contract |
| **Marketed product** | Practitioner-FOCUSED | Strategic positioning choice — Cherry Ventures fit + EU AI Act tailwind + empty OS market for practitioner shape |

**Within Option B floor** (per `shape-extension-and-architectural-floor.md`): even shape-neutral framework primitives structurally enforce 3 accountability axioms regardless of shape (anti-Art-25-trap gate + claim-level audit + human authority chain). Other shapes can configure axis intensities but cannot disable structural floor.

**Tom Sawyer dynamic**: framework is OS; community can author shape extensions for shapes PBS doesn't market (autonomous-business per Paperclip-style; personal-OS per PAI-style; sovereign for defense; etc.). Framework breadth grows organically without PBS effort. PBS-marketed energy stays focused on practitioner shape.

---

## Core positioning (sharpened session 13 per #22 Sub-DR B)

PBS-bureau is the **proof-of-concept for composable AI work infrastructure** — a methodology + pattern set + framework for building practitioner AI workspaces with audit defensibility, applicable across knowledge-work domains and workspace shapes (planning bureaus today; legal practice / research lab / creative studio / knowledge graph deployment / federation node tomorrow).

**Three-tier framing** (locked Sub-DR B):

| Tier | Layer | Strategic claim |
|---|---|---|
| **Infrastructure** | Composable AI work runtime | "We build the infrastructure that powers practitioner workspaces" |
| **Workspace** | Deployment shape | "Office is one workspace shape; practice / lab / studio / personal-base are equally valid" |
| **Specialist** | Composable codified expertise | "Marketplace of specialists; install what your workspace needs" |

**The IP that matters**:
- ✅ **Architectural discipline** (patterns visible openly; expertise applying them is yours)
- ✅ **Track record / proof points** (PBS-bureau + future generator-produced workspaces)
- ✅ **Domain mapping ability** (taking patterns into a new domain or workspace shape)
- ✅ **Refined practice content** (years of accumulated bausteine / korrektur-rules / decision records — the closed IP)
- ✅ **Specialist authoring** (cross-archetype specialists like citation-verification, layered-review-framework, brand-voice — distributable via marketplace per ROADMAP v3)
- ✅ **Delivery quality** (the actual work product holds up under scrutiny)
- ❌ NOT proprietary tooling (commodity in 6-12 months in this space)
- ❌ NOT exclusive access to AI/LLM techniques (commodity)
- ❌ NOT methodology-as-secret (the methodology IS the marketing)

**The honest summary** (calibrated for sophisticated buyers):

> "I architect AI workspaces — composable practitioner infrastructure with shared state + audit defensibility + architectural discipline — for knowledge-work domains. The methodology + patterns + framework are vendor-neutral and scale-independent. PBS-bureau is the open-source proof-of-concept I built for German planning bureaus (one workspace shape); the same infrastructure powers legal practices, research labs, creative studios, and knowledge graph deployments. **What this delivers**: 20-40% productivity uplift on document-heavy workflows + qualitative audit-defensibility that most AI consulting can't match. **What this isn't**: magic. The AI is genuinely useful where judgment + drafting matter; deterministic code does the work where accuracy matters; together they produce defensible work product. **What the IP is**: architectural methodology + practice-refined specialist content, NOT proprietary tools. When you outgrow our archetype, the patterns port to whatever runtime fits your scale."

---

## Open-source-as-edge

In a **commoditizing space** (LLM apps moving fast; new tooling shipping monthly from Anthropic / Google / Microsoft / OSS), proprietary tooling has a **6-12 month half-life**. Trying to monetize tools is a losing game. Open source flips this.

**Why openness IS the edge** (concrete):

1. **Credibility multiplier**. "Here's the architecture, audit it yourself" beats "trust us, our AI office is well-designed" with sophisticated buyers (regulated industries, biglaw, government). Open repo = "I eat my own dog food publicly" — strongest possible discipline signal.

2. **Trust-without-lockin**. Enterprise consulting prospects are scarred by vendor lock-in. "Methodology + patterns are open; only my expertise is proprietary" wins against vertical-SaaS competitors (Harvey, Filevine, Spellbook).

3. **Citation gravity**. When others independently arrive at "AI office abstraction" patterns, they cite the public reference implementation. **First-mover credibility, not first-mover invention.**

4. **Discipline-forcing function**. Public-facing work is sharper than private. The session work behind PBS exists at this quality BECAUSE it's headed for a public repo.

5. **Tom Sawyer / community effect**. Others contribute, refine, find bugs, adopt for their domains. Each adoption = proof point + lead.

6. **Force-multiplied lead generation**. Open repo + blog posts + conference talks + GitHub stars = inbound consulting interest. Different cost structure than proprietary tools (no sales team, no marketing budget required at solo / small-team scale).

---

## Three-tier content strategy

The cut between open and closed IP:

| Tier | Content | License | Purpose |
|---|---|---|---|
| **Tier 1: Open framework** | Architecture (ARCHITECTURE.md, decision records), skills (SKILL.md + references/), MCP tools, meta-skills (audit + design-review), conventions, Pydantic schemas, integration adapter Protocols | MIT (with attribution) | Credibility + lead generation |
| **Tier 2: Open demonstration** | ~20 generic bausteine, ~50 generic korrektur-rule entries, generic verfahren prose, public-domain references | MIT | "Working example" proof; framework wouldn't be credible without it |
| **Tier 3: Closed practice IP** | Refined bausteine library (hundreds), refined korrektur-rules library, custom domain skills built for paid clients, project artifacts, custom department modules | Private; consulting deliverable | Years of accumulated practice — the actual moat |

**Always private** (per existing architecture, app-vs-office split):
- Per-deployment `office-config.yaml`
- Per-project `<project>/_ai/state.md` + `audit-trail.jsonl` + `decisions.md` + `snapshots/`
- Per-deployment custom adapter configs (API keys, tenant IDs)
- Per-engagement client data, correspondence, working drafts

**Practical discipline**:
- **Be intentional about `memory/bausteine/` curation** in the open repo. ~20 entries showing the pattern, range, format conventions. NOT your refined library.
- **Maintain a private bausteine repository** (separate repo, private GitHub or self-hosted). Synced via tooling but not pushed to public.
- **License clarity**: open repo MIT; explicit "instance content under [closed]" for private library.
- **Talk publicly about the framework** (blog posts, talks) — that's lead generation.
- **Don't talk publicly about specific bausteine** — that's giving away the actual IP.

---

## Glue-not-replacement principle

PBS is **the glue layer**, not a replacement for existing infrastructure. Most enterprises have decades of investment in workflow / accounting / case-management systems. The addressable market for **"AI office that augments your existing stack"** is substantially larger than **"AI office that replaces your existing stack"**.

See `ARCHITECTURE.md` "Glue-not-replacement principle" for the architectural treatment. Consulting implications:

**Sales positioning**:

> "Your BPMN engine handles the workflow. Your accounting tool handles invoicing. Your CRM handles clients. Your calendar handles scheduling. We add the cross-concern judgment + drafting + audit-defensibility layer that sits on top — without replacing any of your existing investment. The cognitive-load reduction comes from the glue, not from rip-and-replace."

**Different addressable market** than competing AI verticals:
- Harvey / Filevine / Spellbook = vertical replacement plays. Limited to customers willing to switch FROM existing tools.
- PBS-bureau = augmentation play. Sellable to customers who refuse to switch.

**BPMN-empowerment as concrete example** (see `ROADMAP.md` v1.x-v2 "BPMN/workflow engine integration adapter class"):
- Service-task delegation: BPMN calls PBS for drafting/judgment
- Decision automation with sparring: BPMN's "approve" task gains audit-grade reasoning chain
- Cross-process intelligence layer: PBS sits ABOVE multiple BPMN processes, applying cross-process reasoning

This is **a fundamentally different sale** than vertical-SaaS replacement. Activation trigger: first prospect with substantial BPMN/workflow-engine investment.

---

## Cognitive-load + sparring-mode framing

The honest positioning, grounded in `VISION.md` axes 1-3 + Vivienne Ming's research on AI-human hybrid teams (oracle / validator / sparring partner modes — see VISION §200-235).

### The era progression

**Pre-AI**: knowledge workers held cross-concern context in their heads. **Cognitive load was the bottleneck.**

**BPMN/RPA era**: deterministic coordination automatable; judgment work wasn't.

**AI chatbot era**: single-task help automatable; cross-concern context still wasn't.

**AI office era** (us): cross-concern coordination + judgment-mediated reasoning + audit defensibility, **together**. Worker keeps authorship; system carries coordination.

### Two modes, not one boundary

The naïve framing "AI does operation, human does judgment" is **wrong** — and dangerously so. It's the **oracle-mode failure** Ming's research identifies as the trap that destroys the human's contribution. Per Ming: hybrid teams in oracle mode (humans submit AI's answer as their own) perform **same as AI alone**; in validator mode (humans ask AI to confirm preconceptions) perform **worse**. Only sparring mode (humans push back, demand evidence, interrogate; AI generates counter-arguments + names doubt + resists easy answers) outperforms — by margins neither alone could reach.

The architecture handles two modes differently:

**Mechanical mode** (full automation):
- Operating specialized tools (drawing geometry, formatting, computing fields)
- Cross-tool integration (data flowing between tools)
- Cross-department coordination (handoffs)
- Routine drafting (boilerplate, references, lookups)
- Compile / format / structural validation

→ AI takes over completely. Cognitive load → 0.

**Substantive mode** (sparring):
- Decision-making (which argumentation? which legal interpretation? which scope?)
- Research synthesis (what's relevant? what's missing? what conflicts?)
- Substantive authoring (judgment-bearing argumentation choices)
- Review (does this reflect my judgment? where would adversary push back?)

→ AI generates options + counter-arguments + alternatives. Human pushes back, interrogates, commits. Cognitive ENGAGEMENT preserved (per VISION axis 3 — defensibility test demands it). Per VISION axis 2 sparring requirements: counter-argument as first-class output, anti-sycophancy guard, commit-to-recommendations, asymmetric knowledge respect.

### What actually changes in substantive mode

Cognitive engagement is preserved (you still think hard). **But time + friction are substantially down.** Why?

- Options are presented (you don't scavenge for them)
- Counter-arguments are surfaced (you don't have to remember to consider)
- Reference content is at hand (no separate lookup phase)
- Cross-cutting context is loaded (don't have to hold mentally)
- Mechanical layer is gone (time freed to spend on substance)

Net result: **less time + less friction + better accuracy + preserved engagement.** All four, simultaneously.

The substantive work transforms — same depth of engagement, dramatically lower time + friction, dramatically higher accuracy. **The thinking remains yours; the supporting infrastructure carries the weight that used to cost you time + friction without adding value.**

### The line to walk

Automation that **increases human capacity** vs automation that **displaces humans + atrophies their judgment**. The first is a good thing for clients (their team gets better at the substantive work); the second is Ming's Information-Exploration Paradox (humans optimize themselves out of the loop; capacity collapses; work gets shallower while feeling faster).

**Lead with the first.** Ming's research is the load-bearing reference for why the architecture insists on sparring infrastructure (visible reasoning, counter-argument-as-first-class, anti-sycophancy guard, selective friction). These aren't process overhead — they're the protection against capacity-atrophy.

### What the discipline catches (consulting framing)

- **"AI offices replace junior staff"** — wrong. Lead-to-disappointment messaging. Real: junior staff are more effective; senior staff have more capacity. Both gain.
- **"AI offices automate decision-making"** — wrong (oracle-mode pitch — Ming's research warns specifically against this). Real: AI generates options + counter-arguments; humans decide. Both engaged.
- **"AI offices give you faster answers"** — wrong (validator-mode pitch — sycophancy loop). Real: AI gives you better-explored questions + tested challenges; humans commit to answers.
- **"AI offices eliminate cognitive load"** — incomplete. Real: mechanical load → 0; substantive load preserved but redirected (less time scavenging for options; more time evaluating them critically).

### The sharper consulting positioning

> **"Mechanical work disappears (full automation; cognitive load → 0). Substantive work transforms (same depth of engagement; dramatically lower time + friction; dramatically higher accuracy). The thinking remains yours; the supporting infrastructure carries what used to cost you time + friction without adding value. AI is the colleague that pushes back — not the oracle that gives easy answers, not the validator that confirms what you already think. The friction is the feature."**

This positions explicitly against the two failure-mode pitches competitors make (oracle / validator) — both of which produce, per Ming's research, dependency + capacity decline + worse outcomes than the human + AI alone. **PBS pitch is the third mode: AI as sparring partner.** Vendor-neutral framing; cited research foundation; demonstrably true under prospect scrutiny.

---

## Lived experience as credibility signal

**The architect personally lives the experience he architects for.** This is the strongest credibility evidence — stronger than the open-source repo itself.

### The pattern, demonstrated in the architect's own work

- **GIS work**: 18+ months ago, drove QGIS by hand for geometry creation + modification. Now: AI + `gis_utils` Python tools handle the mechanical authoring; QGIS is reduced to a presentation/review surface. Substantive decisions (which buffer, which classification, which boundary) shifted to sparring mode rather than disappearing. **Result: faster, more accurate, more defensible.**
- **AutoCAD work**: same pattern. AI orchestrates via specialized Python tools; AutoCAD is the rendering surface. Authoring shifted from manual operation to AI-orchestrated specialized APIs.
- **PBS-bureau itself**: the architecture was built in this mode. Multi-month conversations with AI as sparring partner. Architect caught AI's drift toward easy answers (oracle-mode); AI surfaced blind spots + alternatives the architect wouldn't have considered alone. Decision records capture the back-and-forth. The output (12+ commits per session of architectural sharpening) is **strictly better than the union of what either could have produced alone** — exactly Ming's productive-sparring marker.

### The architect's lived testimony

> **"My personal accuracy + client service level have increased manifold while time + friction have decreased. I've been working in sparring mode for 18+ months across GIS, CAD, and document drafting. The architecture I sell isn't theoretical — it's the formalization of how I've actually been working. I can demonstrate this in real time on demand."**

### Why this is unique credibility moat

- **Theory-only consultants** can be challenged ("how do you know it works?") — they can't answer with lived experience
- **Patterns** can be independently arrived at by other consultants (entity-elevation discipline, glue-not-replacement principle, etc. are good ideas, not unique inventions)
- **Lived 18+ months of working in this mode** is harder to manufacture. Other consultants in the AI-office space have NOT been doing this for that long; can't credibly claim the personal proof point
- **The session itself is a proof point**: any prospect can watch a real architectural conversation happen and see sparring-mode-in-action

### The consulting demonstration

For sophisticated prospects, a **live sparring demonstration** beats any pitch deck:
- Pose a real architectural question from the prospect's domain
- Walk through it in sparring mode in real time
- Prospect sees: AI generating options + counter-arguments; architect interrogating + committing; back-and-forth producing a result neither would have alone
- ~30-60 minutes; produces actual deliverable for the prospect's question
- **The demonstration IS the deliverable** of the early-engagement phase

This converts skeptics far more effectively than open-source-repo-citation alone. Combine: the open-source repo establishes the architectural baseline + demonstrated discipline; the live sparring session shows the methodology in action.

### Risks to manage

- **Selling the architect's personal time at scale doesn't work** — the methodology has to transfer. The framework + open-source proof + decision records + audit trail discipline are the transferable IP. Lived experience proves it works; the methodology lets clients work this way themselves.
- **Living the methodology is a precondition for selling it credibly** — if the architect ever slips back into oracle-mode AI usage (taking AI answers without sparring), the personal proof point dissolves. Maintenance discipline.
- **Avoid bragging-tone**. Lived testimony works only when delivered with calibrated confidence + concrete demonstration. "I've been doing this for 18 months and here's what I've produced" works; "I'm uniquely qualified" doesn't.

---

## Revenue model — three streams + future fourth

| Stream | What it sells | When it activates | Status |
|---|---|---|---|
| **1. Architecture-design engagements** | Pure expertise — "I architect an AI office for your domain using these patterns. Working multi-department office delivered." | First consulting prospect with concrete need + budget | Pursued actively post-v1 launch |
| **2. Domain-instance licensing** | Refined practice content — "Bausteine library for German planning bureaus / legal practice / etc." Annual subscription. | When refined library is mature for a domain (PBS planning today; built-up via consulting work for other domains) | Per-domain as practice accumulates |
| **3. Custom-build engagements** | Architecture + instance + delivery — "I architect your office AND populate refined instance content for YOUR practice." Premium pricing. | Mature consulting practice + complex prospects | Activates after stream 1 establishes |
| **4. Marketplace operations (v3+ horizon)** | Marketplace cut OR curation premium on Layer-2 niche marketplace | Post-v2 builder + ecosystem dynamics + open marketplace decision | Concept only; deferred |

**The mistake to avoid**: drifting toward tooling monetization (proprietary tier, hosted SaaS, paid plugins). That dilutes the open-as-edge positioning. **Tools open + free; consulting paid + scoped.**

---

## Three risks to manage

### Risk 1: Drifting toward tooling monetization

**Signals to watch for** (catch early):
- "We could charge for the audit skill / a hosted version of pbs_mcp / premium plugin agents"
- "Pro tier" features held back from open release
- "SaaS-managed pbs-bureau-as-a-service"
- Hiding the AI-office-builder behind a paywall when v2 ships
- Building proprietary extensions that compete with community contributions

**Why each damages the strategy**:
- Open framework + paid tier signals "the open isn't enough"
- Puts you in competition with actual SaaS vendors who have infrastructure + scale
- Creates maintenance burden distinct from consulting
- Misalignment: tempted to keep open framework imperfect so paid tier looks better. **The open thing should be the BEST thing.**

**The discipline test**: every time you feel "we could monetize this piece," ask: *does monetization come from making the open framework better, or from holding parts back?* Latter = drift. Catch it early.

### Risk 2: Failing to invest in complementary activities

**The brutal truth**: open source alone gets ~5 stars and zero consulting leads. **The repo is necessary but not sufficient.**

**Concrete activities** (~5-10 hrs/week of consistent effort):

- **Blog posts** synthesizing each major decision record as a public essay
- **Conference talks** — software architecture, AI/LLM, knowledge-work conferences
- **Public design-review sessions** — record + publish the meta-skill running on real artifacts
- **Comparative writing** — "AI offices vs BPMN engines", "AI offices aren't agentic iPaaS"
- **Case studies** when PBS-bureau actually deploys at Schulz — measurable outcomes
- **Newsletter** — weekly synthesis; forces clarity, builds audience
- **Twitter / LinkedIn / Mastodon** — substantive technical posts

**The good news**: decision records + ARCHITECTURE prose + the entity-elevation discipline write-up are **already in publishable shape**. Each could become a blog post with ~30 minutes of editing. Low marginal cost; high marginal credibility.

**The mistake to avoid**: "I'll just open-source it and the consulting will come." It won't. **Open-source works only with deliberate complementary investment.**

### Risk 3: Brand attribution drift

**What it looks like over time**:
- Someone publishes "the Three-Test for AI Entity Modeling" without citing your decision record
- A consultant references "knowledge graph + document store with stable references" without crediting where it came from
- Anthropic ships an `office-modularization` plugin guide using your patterns + framing
- Patterns become widely-cited but YOU don't get the lead conversion

**Active management** (without being annoying):

- **First-mover publication**: PUBLISH patterns publicly BEFORE someone else does. The first dated public artifact is the citable original.
- **Permalink discipline**: when others use your concepts, respond with "Glad to see this getting traction — original framing here [link]." Friendly, not aggressive.
- **Authorship in repo**: README leads with attribution; LICENSE has attribution clause; decision records signed/dated.
- **Branded patterns** (use sparingly): name patterns that are genuinely yours (e.g., "the 3-test entity-elevation discipline"). Risky if it sounds vain; **so use names for genuinely novel contributions, not for assembled-from-known-pieces patterns**.
- **Watch + respond**: Google Alerts for distinctive phrasing. Engage when used uncited.
- **Catastrophic case** (major vendor publishes derivative without citation): documented timeline + open-source dates. Reputation defense via documented record, not Twitter battles.

**Honest tradeoff**: open-source means open to derivative work. **Perfect attribution control is impossible.** The goal: **enough attribution that prospects connect the concept to your name** when evaluating consulting options. ~70% coverage is enough.

---

## Marketplace strategic arc (sharpened session 13 per #22 Sub-DR B)

See `ROADMAP.md` v2 "AI-workspace generator" → v3 "Marketplace of specialists" + `docs/decisions/positioning-three-tier-framework.md` for full treatment. Summary:

**Marketplace shape locked (Sub-DR B)**: marketplace is **of specialists**, NOT of workspaces or offices. This wasn't crisp pre-Sub-DR A. Now locked:

- Workspace generator (v2) scaffolds workspace shape per archetype
- Specialist marketplace (v3) populates workspaces with capabilities
- Two distinct distribution surfaces; complementary

**Two-layer marketplace strategy**:
- **Layer 1 — main app distribution**: PBS-bureau lives in **Anthropic's marketplace** (knowledge-work-plugins / Cowork plugin distribution). We don't run our own marketplace for the main framework.
- **Layer 2 — specialist marketplace** (v3): refined specialists distributed via marketplace. Might be ours, might live on Anthropic's premium tier, might be third-party. Open question; decide post-v2. Architectural constraints locked Sub-DR B (specialist Pydantic shape + skill definitions + entity schemas + process entities + references manifest + event subscriptions + substrate compatibility + dependencies + version + changelog).

**Critical for v2 generator design TODAY**: v2's output format must be **marketplace-compatible from the start**. Specialists generated by v2 must conform to marketplace listing constraints from Sub-DR B (architectural shape locked; v3 mechanics like auth/pricing/governance deferred).

---

## Closest OS neighbors — verified architecturally distinct (session 14 deep-reads)

Per session 14 closest-neighbors deep-read research (4 OS deep-reads + commercial scan + DACH analysis), PBS uniquely holds **5 of 6 distinctness axes** (workspace-as-practitioner-identity / specialist-as-codified-expertise-bundle / sparring-as-runtime-pillar / audit-by-construction / practitioner-as-author / multi-actor configurable). Closest neighbors fit 1-3 axes each.

| OS Project | Axes-fit | Architectural shape | Closest by | PBS distinct on |
|---|---|---|---|---|
| **PAI (Personal AI Infrastructure)** | 3/5 | Customization layer on Claude Code (NOT framework) | Architectural overlap (workspace-as-identity + composable bundles + practitioner-as-author shape) | sparring runtime + audit-by-construction + multi-actor + substrate abstraction |
| **OpenSail (TesslateAI)** | 2.5/6 | AI app-builder / agentic IDE (Bolt/Cursor lineage) | Verbal positioning (workspace + bundles + audit-log + non-developer audience) | workspace-as-practitioner-identity (vs container env) + sparring + claim-level audit + practitioner-as-author + composable specialist (vs containerized App) |
| **Paperclip** | 1.5/6 | Autonomous multi-agent business orchestration (Postgres-backed) | Sophistication + market visibility ("zero-human company" framing — aspirational marketing, not structural) | claim-level audit (vs action-level) + sparring runtime + composable specialist + multi-actor regulators + practitioner-as-author + event-shaped coordination |
| **Letta v1 (formerly MemGPT)** | 1-2/5 | Single-tier agent runtime + DB-backed state | Surface vocabulary collision (skills + subagents + memory + deployment) | three-tier separation + sparring + audit + workspace primitive + practitioner shape |

**Cargo-cult risk LOW for all** — verbal collision is surface-only at code level. Architectural shapes diverge cleanly. **All four are ecosystem peers (interop targets, pattern sources, distribution surfaces) — not competitive runtimes for practitioner-shape positioning.**

**Adoption opportunities surfaced** (~7 adopt + 3 defer; full table in `closest-neighbors-deep-read.md`):
- A1 SKILL.md interop for Specialist (Letta-confirmed; Anthropic ecosystem standardized)
- A2 Connector Proxy pattern → Adapter Protocol security (OpenSail)
- A3 Contract-as-data → Specialist runtime contracts (OpenSail)
- A4 Manifest schema versioning discipline (OpenSail)
- A5 INSTALL.md wizard pattern (PAI)
- A6 Closed-list capabilities with phantom-detection audit (PAI)
- A7 USER/ vs system separation contract (PAI)
- A8 issue_execution_decisions shape (Paperclip → PBS layered review)
- A9 document_revisions rollback pattern (Paperclip → PBS send-gate snapshots)

## Closest commercial neighbors (DACH + EU)

| Company | Axes-fit | Geography | Notes |
|---|---|---|---|
| **Beck-Noxtua / Noxtua SE** (€80.7M Series B; backed by C.H.Beck + CMS + Dentons + Northern Data + Global Brain + KDDI) | 2/6 | DACH | "Legal AI Workspace"; ISO/IEC 42001 + BSI C5 + ISO/IEC 27018 certified; sovereign EU infrastructure on Northern Data; transparent reference disclosure + change tracking. **Closest commercial neighbor for German market BUT vertical SaaS shape + practitioner-as-USER not author**. **Sovereign-AI funding model precedent** (strategic capital, not classical VC) |
| **Anthropic Claude Cowork + vertical plugins** (Feb 2026; financial services + HR + engineering + legal) | 2/6 | Global | Desktop workspace + Anthropic-or-partner-authored plugins encoding institutional knowledge. **Most architecturally-similar commercial offering — direction-of-travel evidence**. Enterprise-only + no sparring + no multi-actor + no self-host = PBS distinct |
| **Stilta** (YC W26; IP/patent work) | 1/6 | US | "Every output source-backed, referenced, and auditable" — explicit audit-by-construction language. **Validates the axis** in single-vertical SaaS form |
| **Avoice** (YC W26; "AI workspace for architects" / "Harvey for Architecture") | 1/6 | US/UK | Vertical SaaS for architecture firms; English-only; no DSGVO posture. **Does NOT block PBS in DACH** (no EU localization) — but watch for EU expansion |
| **AutoSitu** (YC W26; "AI-native workspace for municipal development review") | 1/6 | US | **OPPORTUNITY not threat** — operates INVERSE side of PBS pioneer domain (cities reviewing applications). **Customer-of-PBS-output**: cities digitizing review = demand for audit-ready submissions = favors PBS audit-by-construction. **Single biggest finding** from commercial scan |

## DACH competitive landscape (operating geography focus)

| Company | Notes |
|---|---|
| **Phase0 (formerly Compa, Berlin; founded 2020)** | **Dominant DACH incumbent — 800+ firms / 1,500+ users.** "OS für moderne Architektur- und Ingenieurbüros." HOAI (LP 1-9) + AVA (DIN 276, GAEB) + AI-Bautagebuch + AI-LV-generation in beta. DSGVO-konform, EU-hosted. **Owns operational-software layer for DACH planner+architect mid-market.** **PBS positions ABOVE Phase0** — expertise codification + audit + multi-actor + sparring layer. Co-existence model: Phase0 = operational; PBS = expertise. **Do NOT compete on HOAI/AVA mechanics (5-year build)** |
| **Langdock (Berlin)** | "Die Plattform für KI-Adoption." Frankfurt-hosted; ISO 27001 + SOC 2; DPA upfront; 40+ models. Custom-GPT primitive = weak practitioner-author proxy. **MEDIUM-HIGH substrate competitor** — DACH firm shopping "DSGVO-AI" buys Langdock + builds custom-GPTs themselves. **PBS differentiates: codified specialists + sparring + audit (categorically different from custom-GPTs)** |
| **Beck-Noxtua / PRIME LEGAL AI / anwalts.ai** | DACH legal/tax commercial workspaces. Practitioner-as-USER not author. **Watch for archetype expansion** to Steuerberater / Architekturbüro / Planungsbüro |
| **BAK (Bundesarchitektenkammer)** | Advocacy-only; **NO chamber-vendor partnership; NO chamber-stamp accreditation.** Liability concern ("Wer haftet für KI-Fehler?") is **PBS marketing wedge** — audit + practitioner-as-author + sparring directly address professional-liability anxiety |

**No DACH commercial product targets the planning-bureau practitioner-author shape.** Beck-Noxtua adjacent (lawyers not planners). **Genuine OS-market gap PBS specifically architected for.**

## Sharpened differentiators — 5 of 6 distinctness axes unique to PBS

Per session 14 competitive research (4 deep-reads + commercial scan):

| # | Axis | PBS holds | Closest competitor stance | Marketing wedge |
|---|---|---|---|---|
| 1 | **Workspace as practitioner-identity primitive** | ✅ unique | PAI = single-human; OpenSail = container env; Paperclip = company; Letta = no workspace | "Your practice is the workspace; not a container, not a SaaS tenant" |
| 2 | **Specialist as composable codified expertise bundle** | ✅ unique | All competitors use skill-as-markdown-file; none codify the multi-component bundle (skills + entities + memory + references + adapters) | "Specialists distribute composable expertise; install what your practice needs" |
| 3 | **Sparring as runtime pillar** | ✅ uniquely unique | All surveyed competitors treat sparring as installable skill (PAI's RedTeam/Council; community devils-advocate plugins); never as always-on runtime | "Sparring runs by default on every decision-class output, not as opt-in skill" |
| 4 | **Audit by construction (claim-level)** | ✅ unique vs claim-level | OpenSail/Paperclip/PAI = action-level (who/what/when); Beck-Noxtua/Stilta = transparent references (partial); none bind every claim to evidence at write-time | "Defensibility for any per-deployment audience (regulator / court / peer / client / future-self)" |
| 5 | **Practitioner-as-author** | ✅ unique | Letta/OpenSail/Paperclip = developer-author; PAI = "everyone" but actually power-user; commercial = practitioner-as-USER | "Practitioner authors specialists for their domain; not buyer of pre-built apps" |
| 6 | **Multi-actor primitive (configurable per-deployment)** | ⚠ unique | PAI = single-human; Paperclip = user/agent/system but no external_agent; commercial = single-tenant | "Practitioner + clients + regulators + corpus references — all first-class actors; configurable per-deployment" |

Plus **substrate abstraction at framework layer**: Letta/OpenSail/PAI/Paperclip all tightly substrate-coupled; PBS is genuinely substrate-pluggable (Claude Agent SDK + MS Agent Framework dual substrate per #18).

## EU AI Act tailwind — asymmetric in PBS favor

Per `docs/decisions/closest-neighbors-deep-read.md` + EU AI Act + DACH regulatory deep-look (session 14):

- **Sparring uniquely operationalises Art. 14 human oversight** — "*understand the relevant capacities and limitations*" + "*remain aware of the possible tendency of automatically relying or over-relying*". Genuinely unique regulatory asset; no competitor holds this
- **Practitioner-as-deployer = cleanest AI Act posture** — vs SaaS provider/deployer muddiness (Beck-Noxtua/Stilta face Art. 25 substantial-modification trap risk per deployment)
- **Self-hostable + EU residency** = sovereign-AI alignment (BSI C5 sovereignty + DSGVO Art. 44-49 third-country transfer rules). Closed-source US-SaaS competitors face structural disadvantage
- **Audit-by-construction = direct mapping** to Art. 11 (technical doc) + Art. 13 (instructions for use) + Art. 26(6) (6-month log retention)
- **Hard requirement before Aug 2026 production**: Art. 50(4) AI-disclosure for B-Plan Begründung (public-interest output per BauGB §3 Öffentlichkeitsbeteiligung)
- **Critical architectural constraint**: anti-Art-25-trap structurally enforced (specialist conformity manifest as Pydantic gate per Option B; impossible-by-construction)
- **Major commercial asset**: ISO/IEC 42001 SoA scaffold publishable as marketplace asset (cuts cert cost for any EU practitioner workspace; €35-90k saved per deployment)

## a16z / Sequoia "service-as-software" thesis as positioning risk for fundraising

Per session 14 a16z research:

**Sequoia (not a16z) owns canonical thesis** — Julien Bek's "Services: The New Software" (March 2026). Replace-the-consultant via AI-native firms. Portfolio: Harvey, Rogo, Crosby, Anterior, Lawhive, Mercor.

**a16z reinforces but doesn't own**: Big Ideas in Tech 2025; outcome-based-pricing newsletter; Notes on AI Apps in 2026.

**Adjacent VCs amplifying**: General Catalyst ($1.5B "creation strategy"); Bessemer (vertical AI eclipses vertical SaaS); NEA ($11T US labor spend); Menlo; Emergence ("AI-Native Services Playbook").

**Critique** (TechCrunch Sep 2025): Stanford "workslop" research — 40% of employees deal with AI-generated work that creates remediation labor (~2hrs/instance, ~$9M/yr per 10K-person org). Thesis may be empirically harder than VC consensus assumes.

**For PBS**: this thesis is the **antithesis of PBS positioning** (replace vs amplify). Accepting US-thesis-aligned VC capital would force narrative drift toward replace-the-practitioner — destroying audit-by-construction value proposition. **Avoid US classical VC route.**

## Cherry Ventures (Berlin) — only published EU VC thesis match + recommended funding path

Per session 14 European VC comparison:

**Cherry's published thesis** — "Cherry's Investment Theses on AI" (July 2024) + "Bringing the AI Thesis to Life":
- *"AI supports and enhances human creativity… without replacing"* — chess-player-and-computer model
- European founders advantaged because they *"intimately understand the regulatory landscape"* — regulation as innovation surface
- Portfolio: Cortea (regulatory compliance), Riplo (consulting OS), Sphinx (compliance automation)

**PBS positioning lands cleanly in Cherry thesis. Only published EU VC thesis match.**

**Other EU VCs** (mixed alignment, not thesis-match):
- **Visionaries Club** (Berlin/London, €600M+ AUM) — applied AI for "Europe's oil economy" legacy sectors. Closer to vertical-application than amplify-practitioner. Acceptable second
- **HV Capital + Earlybird** — Earlybird €360M Fund VIII (Apr 2026) explicitly favours infrastructure/foundation-model layers; misalignment with PBS application-layer positioning
- **Index Ventures + Atomico** — leaning into AI but co-investing in **replace-the-professional plays** (Ankar AI patent firm Series A). Closer to Sequoia thesis. **Avoid**
- **Project A + Speedinvest + La Famiglia** — La Famiglia merged into General Catalyst 2023; **carries replace-thesis import**. **Avoid GC-channel firms**

### Recommended funding path (strategic sequencing)

1. **Ground-up consulting revenue (PBS-Schulz pioneer)** + **EXIST/ZIM/go-Inno non-dilutive DACH grants** (18-24 months)
   - go-Inno Innovation Vouchers — 50% consulting cost coverage up to €20K/yr
   - ZIM (Zentrales Innovationsprogramm Mittelstand) — R&D grants for SME tech
   - EXIST AI.STARTUP.HUB programmes (BMWK)
   - Horizon Europe + EFRE Bundesländer programs
   - **Preserves practitioner-amplification framing fully; EU AI Act tailwind compounds**

2. **Strategic capital from publishers + chambers + state banks** (Beck-Noxtua model: €80.7M from C.H.Beck + CMS + Dentons + Northern Data — no classical VCs)
   - Target German planning publishers (Beuth, Werner Verlag, vhw, BAK)
   - Engineering chambers
   - State-bank vehicles (IBB Berlin, BayStartUP Bayern, NRW.BANK)
   - **Carries practitioner alignment by default**

3. **Cherry Ventures as VC-of-last-resort** — only thesis-aligned EU VC

4. **AVOID**: GC-channel firms (La Famiglia legacy); Index/Atomico growth-stage; US-classical VC (Sequoia/a16z thesis import)

## ICP refinement (per three-tier framing)

| Tier | What sells | ICP |
|---|---|---|
| Infrastructure | Framework adoption + consulting | Practitioner-archetype firms ready to deploy AI workspaces; consulting engagements |
| Workspace | Pre-configured workspace templates per archetype | Specific archetype niches (planning bureaus, legal practices, research labs, accounting firms) — narrower than infrastructure ICP |
| Specialist | Marketplace browse + install (v3) | Wider — any workspace operator including non-practitioner archetypes (community-buildable shape extensions) |

**ICP discipline preserved**: PBS sells narrow (consulting + workspace templates per archetype); framework architecture serves broader (marketplace expands ecosystem). PBS-Schulz validates the planning-bureau workspace shape; other workspace shapes pioneered by other deployments OR community shape extensions.

## Compliance specialist as marketplace asset (NEW per session 14)

Per ROADMAP commitment #24 (`eu-ai-compliance` + `dach-regulatory-extension` specialists):

- **Cross-archetype specialist** = applies to ANY EU practitioner workspace (every EU practitioner needs this)
- **Distributable via marketplace v3** — major commercial asset
- **ISO 42001 SoA scaffold** = the showcase deliverable (cuts cert cost €35-90k → near-free per deployment)
- **Strategic narrative**: PBS is the only OS framework with a built-in EU AI Act compliance specialist + structural anti-Art-25 enforcement
- **Fundraising amplifier**: directly addresses Cherry Ventures thesis ("regulatory landscape as innovation surface") + Beck-Noxtua-style strategic capital interest (publishers + chambers + state banks all care about regulatory compliance)
- **Defensibility moat for PBS-Schulz pioneer**: bureau gets first-deployment advantage of fully-compliant production from day-1

## Competitive landscape

| Competitor type | Examples | Their shape | Our differentiation |
|---|---|---|---|
| Vertical SaaS replacement | Harvey, Filevine, Spellbook, EuclidHL | One workflow within one domain; rip-and-replace play | We complement existing tools (glue-not-replacement); broader addressable market |
| Product-wrapper agents | Salesforce CRM agent, Workday HR agent, ServiceNow agent | One SaaS API exposed as agent | We orchestrate ABOVE these via integration adapters; coherent multi-department layer |
| Capability-slice plugins | Anthropic's `legal`/`finance`/`hr`, brand-voice partner-built | Single-specialist plugins, ~3 skills, no orchestrator | We're multi-specialist workspace shape with cross-specialist coordination, audit, lifecycle |
| Enterprise platforms | Gemini Enterprise + Apigee, MS Agent Framework, Vertex AI Agent Builder | Cross-SaaS automation via A2A | Different layer entirely — they automate; we coordinate domain-coherent multi-specialist workspaces on top |
| Methodology-only consultants | Generic AI consultants | Slides + advisory, no proof | We have the open-source proof + delivery track record |

**Sharpest positioning** (per ROADMAP §2293+ analysis):

> "Your fleet of product-wrapper agents (Salesforce, Workday, ServiceNow) plus your A2A cross-SaaS automation gives you AI-mediated SaaS integration. That's agentic iPaaS — not an AI office. The actual office layer — domain-coherent multi-department coordination with shared state, lifecycle, audit trail, and architectural discipline — has to be deliberately designed. **That's what I do.** I architect the office abstraction that turns your fleet of agents into a coherent operation, on whatever runtime archetype fits your scale (single-big-model orchestration for solo/small; multi-agent A2A on Gemini Enterprise for enterprise federation). Methodology and architectural discipline are vendor-neutral and scale-independent; the office abstraction is the IP."

---

## Multi-archetype credibility (planned, post-Tiers-1-2-maturity)

Most AI-office consultants will run on ONE archetype — either single-big-model (open-source / Anthropic-shop) or multi-agent A2A (enterprise platform — Gemini Enterprise / Azure AI Foundry / AWS Bedrock AgentCore). Few will run on both.

**Substrate-pluggable framework foundation** (per `docs/decisions/substrate-agentic-framework.md`, session 12): the framework is built substrate-pluggable from day 1 with TWO complete backends — Claude Agent SDK (Anthropic ecosystem; primary deployment) + Microsoft Agent Framework (multi-provider; backend ready, Path B frontend deferred to consulting signal). This makes the multi-archetype consulting pitch a verifiable claim NOW rather than a post-Tier-3-port future state.

**The plan** (per ROADMAP v2 "Tier 3 enterprise multi-agent A2A platform port + parallel development"): once Tiers 1-2 are mature (PBS-bureau working in real Schulz Planungsbüro use; pre-RAG queue completed; Phase 1 corpus ingested; first project producing real work), the architect ports + parallel-develops on a Tier-3 enterprise multi-agent A2A platform (Gemini Enterprise as default exemplar; Azure AI Foundry or AWS Bedrock AgentCore depending on consulting context + substrate choice) — **regardless of specific client demand**. The motivation is multi-archetype credibility for the consulting offering: building IS the validation work that earns the verified track record other consultants can't easily match.

**The consulting positioning shift this enables** (vs single-archetype peers):

> **"I've actually built and run on both archetypes. Tiers 1-2 (single-big-model orchestration) for the work you'll see today — Schulz Planungsbüro running on Coolify with PBS-bureau. Tier 3 (multi-agent A2A on Gemini Enterprise) for the work you'll see when scale demands it — same domain content, same architectural discipline, different runtime archetype. The methodology + patterns port cleanly because they were designed to from the start (per A2A schema compatibility decisions made pre-RAG). Other AI-office consultants will tell you they have a 'migration path'; I have a verified port + active parallel deployment. You pick the archetype that fits your scale; I architect the office on whichever you choose."**

**Why this matters competitively**:

- **Vertical-SaaS replacement competitors** (Harvey, Filevine, Spellbook): single-archetype, single-domain, rip-and-replace. We're cross-archetype, multi-domain, glue-not-replacement.
- **Single-archetype open-source AI-office consultants** (whoever else builds in this space): theoretical migration paths; no verified Gemini track record.
- **Enterprise-platform-native consultants** (Gemini Enterprise / Apigee specialists): no open-source archetype credibility; locked into one platform.

**Verifiability is the moat**. Theory-only consultants can claim "we work on any archetype." We can demonstrate it on demand: live deployment on Tiers 1-2 + live deployment on Tier 3 + the open-source repo showing the port architecture + the decision records showing the schema-compatibility work that enabled it.

**Honest framing of the investment**:

- Building the Gemini port is **substantial work** (3-6 months realistic estimate per ROADMAP §2667). Not free. Not casual.
- It's a **strategic investment in consulting capability**, not an immediate revenue play. Pays back through credibility + lead conversion + premium pricing on multi-archetype engagements.
- It's **post-Tiers-1-2 maturity** — not a parallel pre-launch effort. Tiers 1-2 must be working production-grade first.

**The architectural pre-work that enables this** (already committed pre-RAG):
- **#10 (A2A schema compatibility)** — AuditEvent + ProjectState + adapter Protocols all designed to be A2A-shape-compatible. The port doesn't require a schema migration; it requires a runtime swap.
- **Pattern-vs-instance discipline** — domain content + architectural patterns are pattern-level; runtime-specific code is instance-level. Clean separation makes the port conceptually clean.
- **Glue-not-replacement principle** — integration-adapter pattern works the same on either archetype.

**The consulting promise is structurally sound, not aspirational.** When activated, this section gets concrete metrics from the actual port (timeline, observed differences between archetypes, quality comparison, etc.).

---

## Review triggers

Update this document when:
- New revenue stream activates (first paid consulting engagement; first domain-licensing customer; first custom-build engagement)
- Marketplace decision becomes timely (post-v2 builder; ecosystem dynamics observable)
- Major competitive shift (Anthropic / Google / MS ships something that absorbs a niche we've been targeting)
- Brand attribution case (major vendor publishes derivative; need to respond)
- Consulting positioning learning (after first 3-5 engagements; what actually closes deals vs what I theorize closes deals)
- Annual review at minimum

**Not in this document** (intentionally):
- Specific pricing for engagements (varies per prospect; live in proposal docs)
- Specific clients / engagements (live in private project notes)
- Specific marketing copy (varies per channel; live in marketing assets repo)
- Tactical decisions (which conference to submit to; which blog post next; etc.)

This doc is **strategy** — the slow-moving load-bearing positioning principles. Tactics live elsewhere.
