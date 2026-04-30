# Strategic positioning — pbs-bureau as consulting IP

**Status**: working document (session 9 followups, 2026-04-29). Strategic discussion captured for durability across sessions. Distinct from `ARCHITECTURE.md` (technical architecture) and `ROADMAP.md` (commitment queue) — this doc covers **how the work positions in the consulting market** and **what consulting offerings flow from it**.

This is a living document. Update when strategy refines; review periodically for drift.

---

## Core positioning

PBS-bureau is the **proof-of-concept for AI-office architecture** — a methodology + pattern set for building multi-department AI offices with audit defensibility, applicable across knowledge-work domains (planning bureaus today; legal practice / research / medical / regulatory / consulting tomorrow).

**The IP that matters**:
- ✅ **Architectural discipline** (patterns visible openly; expertise applying them is yours)
- ✅ **Track record / proof points** (PBS-bureau + future builder-generated offices)
- ✅ **Domain mapping ability** (taking patterns into a new domain)
- ✅ **Refined practice content** (years of accumulated bausteine / korrektur-rules / decision records — the closed IP)
- ✅ **Delivery quality** (the actual work product holds up under scrutiny)
- ❌ NOT proprietary tooling (commodity in 6-12 months in this space)
- ❌ NOT exclusive access to AI/LLM techniques (commodity)
- ❌ NOT methodology-as-secret (the methodology IS the marketing)

**The honest summary** (calibrated for sophisticated buyers):

> "I architect AI offices — multi-department coordination with shared state + audit defensibility + architectural discipline — for knowledge-work domains. The methodology + patterns are vendor-neutral and scale-independent. PBS-bureau is the open-source proof-of-concept I built for German planning bureaus; the same patterns apply to your domain. **What this delivers**: 20-40% productivity uplift on document-heavy workflows + qualitative audit-defensibility that most AI consulting can't match. **What this isn't**: magic. The AI is genuinely useful where judgment + drafting matter; deterministic code does the work where accuracy matters; together they produce defensible work product. **What the IP is**: architectural methodology + practice-refined domain content, NOT proprietary tools. When you outgrow our archetype, the patterns port to whatever runtime fits your scale."

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

## Marketplace strategic arc (concept; deferred decision)

See `ROADMAP.md` v2 "AI-office builder" → "Marketplace as v3 horizon" for full treatment. Summary:

**Two-layer marketplace strategy**:
- **Layer 1 — main app distribution**: PBS-bureau lives in **Anthropic's marketplace** (knowledge-work-plugins / Cowork plugin distribution). We don't run our own marketplace for the main app.
- **Layer 2 — specialized blueprint marketplace**: niche marketplace for refined domain blueprints might be ours — OR might also live on Anthropic's premium tier — OR might be third-party. Open question; decide post-v2.

**Critical for v2 builder design TODAY**: v2's output format must be **marketplace-compatible from the start**. Standardized blueprint manifest, dependency declaration, version compatibility, quality metadata, license declaration — even though the marketplace is v3+ horizon.

---

## Competitive landscape

Different niches; positioning around specialization:

| Competitor type | Examples | Their shape | Our differentiation |
|---|---|---|---|
| Vertical SaaS replacement | Harvey, Filevine, Spellbook, EuclidHL | One workflow within one domain; rip-and-replace play | We complement existing tools (glue-not-replacement); broader addressable market |
| Product-wrapper agents | Salesforce CRM agent, Workday HR agent, ServiceNow agent | One SaaS API exposed as agent | We orchestrate ABOVE these via integration adapters; coherent multi-department layer |
| Capability-slice plugins | Anthropic's `legal`/`finance`/`hr`, brand-voice partner-built | Single-department, ~3 skills, no orchestrator | We're multi-department-office shape with cross-department coordination, audit, lifecycle |
| Enterprise platforms | Gemini Enterprise + Apigee, MS Agent Framework, Vertex AI Agent Builder | Cross-SaaS automation via A2A | Different layer entirely — they automate; we coordinate domain-coherent multi-department offices on top |
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
