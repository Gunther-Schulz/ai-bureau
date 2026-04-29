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

## Cognitive-load-reduction framing

The honest positioning of what AI offices add (vs overselling):

**Pre-AI**: knowledge workers held cross-concern context in their heads. **Cognitive load was the bottleneck.**

**BPMN/RPA era**: deterministic coordination automatable; judgment work wasn't.

**AI chatbot era**: single-task help automatable; cross-concern context still wasn't.

**AI office era** (us): cross-concern coordination + judgment-mediated reasoning + audit defensibility, **together**. Worker keeps authorship; system carries coordination.

**The line to walk**: automation that **increases human capacity** vs automation that **displaces humans**. The first is a good thing for clients (their team gets better); the second is a layoffs pitch (riskier sale). **Lead with the first.**

**What the discipline catches**:
- "AI offices replace junior staff" — wrong (lead-to-disappointment messaging). Real outcome: junior staff are more effective; senior staff have more capacity.
- "AI offices automate decision-making" — wrong. Real: automate coordination so humans can decide better.
- "AI offices eliminate cognitive load" — wrong. Real: shift cognitive load FROM coordination TO judgment, where it should be.

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
