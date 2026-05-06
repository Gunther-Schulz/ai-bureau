# 3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING

> **Status**: Preliminary discovery document. Captures session 35 turn (post-2026-05-06) where the "thin-layer concern" surfaced and resolved into a substantive positioning correction: PBS framework is structurally a **context-graph + cross-domain-knowledge-composition framework for accountability-bearing work**, NOT a thin layer over platform infrastructure. This reframes 1-NEXT.md §3.5 framework positioning and surfaces an open architectural question (unified primitive vs distributed) for F1+ to address.
>
> **Companion documents**:
> - `1-NEXT.md` — working session handoff (currently frames §3.5 as thin-layer; pending reframe per this discovery)
> - `2-PRELEMINARY-ENTRERPRISE.md` — enterprise platform landscape research
> - This file — substantive PBS positioning surfaced from cross-domain knowledge gap analysis

---

## 1. The trigger

User observation late in session 35: *"if we refactor towards fully leveraging each abilities and standards and protocols [from Claude SDK / MS AF / Google ADK], we are rather thin layer on top."*

Honest concern: thin layer = trivially replicable by any large company with engineering capacity → no substantive value justifying framework adoption over rolling-your-own.

Counter-question that drove this discovery: **how do enterprises actually solve cross-domain knowledge sharing across scattered agents/tools/MCPs in practice today?**

## 2. Verified state of the cross-domain knowledge problem (2026)

From web search + verified sources this session:

**Tribal knowledge fragmentation** — knowledge "accumulates in people's heads, out of reach of the digital realm, existing in the white space between traditional applications filled by phenomena such as swivel-chair integration, ad-hoc apps, spreadsheets, email chains, and team communications apps. When humans are in the loop, agents don't know what's in those people's heads, and the tribal knowledge that informs decisions may leak out in messages or conversations, but there's no reliable way of fully capturing it" (per [diginomica context graphs](https://diginomica.com/context-graphs-unlock-new-seam-enterprise-knowledge-ai-agents)).

**Cross-domain coordination failure** — "agentic systems fail when context is fragmented across dashboards, ticket notes, topology tools, CRM views, and tribal knowledge... without a shared operational understanding, each agent may optimize locally while the system behaves inconsistently globally" (per [thefastmode autonomous networks](https://www.thefastmode.com/expert-opinion/47580-autonomous-networks-need-shared-understanding-why-telco-knowledge-graphs-will-matter-in-2026)).

**Knowledge foundation before automation** — "you can't automate chaos. Without a structured knowledge foundation, even the most advanced agents become brittle, inconsistent, and ungovernable. Organizations have been investing in sophisticated agent frameworks before establishing robust single-agent GraphRAG systems" (per [graphwise enterprise AI horizon](https://graphwise.ai/thought-leadership/the-2026-enterprise-ai-horizon-from-models-to-meaning-and-the-shift-from-power-to-purpose/)).

**Governance + explainability beyond access control** — "Traditional governance frameworks focusing on access control and data lineage aren't enough when autonomous agents make decisions on behalf of organizations. In 2026, enterprises will implement governance ensuring explainability, fairness, and auditability at every layer, including maintaining versioned knowledge graphs, enforcing reasoning constraints, and logging agent interactions."

**Decision traces vs outcome logs** — context graphs distinct from generic knowledge: "institutional memory for how an organization makes decisions: not how the process doc says it should, but how it actually works in practice... decision threads still live in Slack threads, side conversations, and people's heads rather than being treated as queryable data." Standard knowledge bases and RAG systems capture static information; context graphs dynamically track "what inputs were gathered across systems, what policy was evaluated, what exception route was invoked, who approved, and what state was written" (per [diginomica](https://diginomica.com/context-graphs-unlock-new-seam-enterprise-knowledge-ai-agents)).

## 3. What platforms address vs don't

Verified from §10 of 1-NEXT.md + this turn's research:

### Platforms address generically

- **Agent identity** — Microsoft Entra Agent ID; Gemini Agent Identity (cryptographic IDs per agent)
- **Audit logs** — security/compliance focused (Microsoft Foundry, Gemini Agent Observability)
- **OWASP Top 10 risks** — Microsoft Agent Governance Toolkit (sub-millisecond policy enforcement)
- **User-scoped persistent memory** — Gemini Memory Bank, explicitly NOT agent-to-agent per Google docs: "scopes memories to specific user identities... designed for user-centric rather than agent-to-agent knowledge transfer" (per [Memory Bank docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank))
- **Tool/data integration protocol** — MCP (universal cross-vendor)
- **Agent-to-agent protocol** — A2A (universal cross-vendor)
- **Knowledge Catalog** — Gemini Enterprise's data-asset-level cataloging, but NOT decision-trace level

### Platforms do NOT address

- **Cross-domain knowledge composition between agents** — each agent has its own MCPs; cross-MCP knowledge composition unaddressed
- **Decision traces with reasoning** — outcome logs vs how-and-why
- **Tribal knowledge capture in structured form** — institutional decision-making patterns
- **Cross-specialist accountability chains** — claim attribution spanning specialists/domains
- **Domain-specific accountability discipline** — practitioner-accountability for accountability-bearing professional work

## 4. What PBS already commits to (verified architectural primitives)

From session 35 reads of arch/* + glossary/*:

- **Claim-attribution chain** (per `arch/audit.md` + `arch/claim-defensibility.md`) — every claim has actor + reasoning + evidence path; defensibility test reconstructs the WHY of each output
- **Cross-specialist composition rules** (per `arch/specialist-skill.md` §10) — specialists CAN reference each other's work; cross-specialist entity reads permitted; audit-trail records cross-specialist composition
- **Layer A scope-resolution** (per `arch/scope-model.md` §2.3) — content scoped by domain + state; multiple domains active simultaneously per workspace; structurally domain-keyed knowledge layering
- **Engaged-authorship operational definition** (verified glossary/engaged-authorship.md) — practitioner-author engaged with reasoning chain not just outcomes; production-phase substrate captured for axis-3 defensibility
- **Defensibility test reconstruction** (per VISION.md) — "will the practitioner-author be able to defend this output six months from now under regulatory or professional challenge, having forgotten the details?"
- **Sparring engagement events as production-phase substrate** (per `arch/sparring.md` §1 + axis-2-to-axis-3 cross-axis composition)
- **Audit-trail with hash-chain integrity** (per `pbs/impls/claude_agent_sdk_audit.py` SHA-256 hash chain)
- **Cross-cutting non-placed primitives** (per `arch/scope-model.md` §4 E4) — defensibility / engaged-authorship / category-collapse manifest through behavior of placed entities

These compose into a **context-graph for accountability-bearing work**.

## 5. The corrected positioning

The earlier thin-layer framing was correct about LOWER layers (which should be thin) but minimized the SUBSTANTIVE layer. Revised:

| Layer | PBS approach | Why |
|---|---|---|
| **Open standards** (MCP, A2A) | THIN — leverage entirely | Universal cross-vendor; no point reimplementing |
| **Platform primitives shared across targets** (MCP server creation, permission flow, session, hook matchers) | THIN — leverage where parity exists | Reduces framework code; composes with platform infra |
| **Cross-platform abstraction layer** (Pattern A's ≥2-impl discriminator) | MODERATE — framework provides translation | Where Claude SDK / MS AF / Gemini ADK conventions diverge |
| **Context-graph + cross-domain-knowledge composition + practitioner-accountability discipline** | **NOT THIN — substantive PBS contribution** | Captures decision traces + claim attribution + sparring engagement + reasoning chains across specialists / domains / sessions; enterprises need this; no platform addresses it generically; the unique value justifying framework adoption |

Substantively PBS is **a decision-trace + cross-domain-knowledge-composition framework specifically tuned for accountability-bearing work**. That's the bull's eye of the verified gap. Not thin.

## 6. The open architectural question

Does PBS need a **unified primitive** (e.g., `context-graph` or `decision-graph`) for the substantive layer, or are the existing distributed primitives (audit + claim + specialist + scope-model + engaged-authorship + sparring + cross-cutting non-placed) sufficient?

### Arguments FOR unified primitive

- **Articulates substantive contribution clearly** — one concept to position the PBS contribution vs context-graph platforms (Galaxy, GraphWise, Stardog) and vs platform Memory Bank / Knowledge Catalog
- **Easier for new audiences to grasp** — "PBS is a practitioner-accountability context-graph" vs "PBS is a framework with audit + claim + specialist + scope-model + engaged-authorship + sparring composing into..."
- **Composes more cleanly for cross-deployment portability** — claims-as-portable across Owner B per W2 watch-list becomes claims-as-context-graph-nodes-portable
- **Aligns with industry vocabulary** — "context graph" is verified emerging term ([diginomica](https://diginomica.com/context-graphs-unlock-new-seam-enterprise-knowledge-ai-agents))

### Arguments AGAINST unified primitive

- **Existing distributed architecture is locked + works architecturally** — adding a new top-level primitive creates cascade work
- **Risk of conflating distinct primitives that should stay separate** — audit (mechanism class), claim (PRIMITIVE content unit), specialist (Pattern B), scope-model (cross-cutting integrator) have different scope-categorization semantics; a unified primitive might paper over load-bearing distinctions
- **Pattern-vs-instance discipline** — "context-graph" as named primitive could lock in instance-specific framing if it bakes in PBS-Schulz-shaped reasoning patterns

### Mental-modeling scenarios to resolve at F1+

Each scenario tests whether unified primitive is needed for the architecture to compose cleanly:

- **Scenario A — Legal firm with 50 matter specialists**: cross-matter citation lineage; precedent reasoning across matters; cross-attorney consultation traces. Test: do distributed primitives (claim attribution + cross-specialist composition + scope-model domain-keyed Layer A) compose cleanly for query "all matters where attorney X cited regulation Y under exception Z"?
- **Scenario B — Research lab with cross-paper citation graph**: claim provenance across papers; co-author attribution; methodology sharing across labs. Test: does the distributed architecture support "show me the reasoning chain for claim K across these 5 papers" without needing a unified primitive?
- **Scenario C — Planning firm cross-project compliance lineage** (PBS-Schulz extension): which BauGB §35 interpretations were applied across which projects; cross-project bauleitplanung pattern reuse. Test: does Layer A + cross-specialist composition + cross-claim portability compose cleanly?

If distributed primitives compose cleanly across all three scenarios → distributed sufficient; no unified primitive needed.
If composition feels strained / requires significant cross-primitive coordination logic in deployment code → unified primitive worth introducing.

Resolution: mental-model at F1 + F2 milestones; surface decision before F4 enterprise track activates.

## 7. Implications for F1+ (reframes pending in 1-NEXT.md)

### §3.5 framework positioning — reframe

Replace "thin-layer" framing with the §5 corrected 4-layer table. Bottom layer (substantive) is NOT thin; that's the PBS contribution.

### §3.6 (potential NEW section) — cross-domain knowledge composition

Add explicit architectural framing: PBS commits to context-graph + cross-domain-knowledge composition for accountability-bearing work. Open question (§6 above) named with mental-modeling resolution path.

### §6.6 thin-layer working discipline — refine scope

Still applies but ONLY to runtime infrastructure layer (top three rows of §5 table). Does NOT apply to substantive layer (bottom row); that's where framework code is justified.

### F1.0-F1.4 — implementation choices preserve composability

- **F1.0 (SUBPROCESS MCP transport)**: still leverage platform primitives where possible; but ensure the MCP server organization preserves cross-domain composability (e.g., audit MCP server exposes cross-specialist query API, not just per-specialist isolated logs)
- **F1.1 (audit MCP tool)**: design `pbs_audit_emit` + companion query tools to support context-graph traversal queries (claim attribution chain reconstruction; cross-specialist composition queries) — not just append-only logging
- **F1.2 (engagement-detection hook)**: hook flag drives engagement; but engagement-trail captured contributes to context-graph reasoning chain
- **F1.3 (practitioner-shape policy bundle externalized)**: per-shape policy bundle pattern generalizes — context-graph composition is shape-neutral; per-shape policy parameterizes accountability discipline
- **F1.4 (full F1 wiring)**: end-to-end exercises context-graph traversal at minimum (e.g., one PBS-Schulz scenario where claim attribution chain crosses ≥2 specialists or ≥2 domains)

### F2 — context-graph composition surfaces in real work

- F2.0+: specialist authoring discipline includes cross-specialist composition explicit (per `arch/specialist-skill.md` §10 cross-specialist composition rules)
- F2.3: Layer A content authoring exercises domain-keyed knowledge composition

### F4 — enterprise positioning leans on substantive layer

Track B (enterprise integration) positioning: PBS as context-graph + practitioner-accountability layer ON TOP of platform agent runtime infrastructure. Not "thin layer"; "context-graph layer specialized for accountability-bearing professional work."

## 8. What this changes about positioning vs enterprises

The right enterprise positioning isn't:

> "thin layer big firms could roll themselves"

It's:

> "PBS provides the context-graph infrastructure that captures decision traces, claim attribution chains, sparring engagement, and cross-domain knowledge composition — specifically structured for accountability-bearing professional work where the practitioner must defend outputs months later. Generic agent platforms (Gemini Enterprise, MS Foundry) address agent runtime + identity + governance; PBS sits ON TOP of them adding the decision-trace + cross-knowledge layer. Enterprises building this themselves face: tribal-knowledge fragmentation, GraphRAG foundation problem, governance-explainability problem, knowledge-foundation-before-automation challenge. PBS solves these for the specific accountability-bearing-work case — universal across legal / planning / engineering / healthcare / accounting / consulting verticals."

Substantive enough that big firms wouldn't trivially roll their own — they'd evaluate PBS the way they evaluate context-graph platforms (Galaxy, GraphWise, Stardog, etc.) but with practitioner-accountability discipline baked in.

## 9. What still needs verification

- **Does PBS's audit-trail design actually support context-graph traversal queries?** Not verified — would need to read `arch/audit.md` §C query API in detail + verify against Scenario A/B/C above. Mental-model at F1.1.
- **Does cross-specialist composition with Layer A scope-resolution support cross-domain queries cleanly?** Not verified — depends on specialist-namespace mechanic + Layer A active-domains/states semantics composing correctly under multi-specialist scenarios. Mental-model at F2.0.
- **Is there a load-bearing primitive missing** (e.g., explicit "decision-thread" or "reasoning-chain" entity at Owner B) that the current distributed architecture lacks? Mental-model at F1+ when context-graph traversal queries are concretely exercised.
- **Are the existing W1-W4 watch-lists already pointing toward context-graph composition** (e.g., cross-deployment claim portability per `arch/scope-model.md` W2)? Worth re-reading watch-list entries with this framing in mind.

## 10. Sources

Verified web sources cited above:
- https://diginomica.com/context-graphs-unlock-new-seam-enterprise-knowledge-ai-agents (context graphs as decision-trace primitive)
- https://graphwise.ai/thought-leadership/the-2026-enterprise-ai-horizon-from-models-to-meaning-and-the-shift-from-power-to-purpose/ (knowledge foundation before automation)
- https://www.thefastmode.com/expert-opinion/47580-autonomous-networks-need-shared-understanding-why-telco-knowledge-graphs-will-matter-in-2026 (cross-domain coordination failure)
- https://www.atomicwork.com/blog/why-enterprise-knowledge-graphs (enterprise knowledge graph context)
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank (Gemini Memory Bank user-scoped, NOT agent-to-agent)
- https://www.bain.com/insights/google_cloud_next_2026_the_agentic_enterprise_control_plane_comes_into_view/ (Google Cloud Next 2026 enterprise control plane)
- https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/ (Meta tribal knowledge mapping)

Verified PBS framework files (read in session 35):
- `VISION.md` (defensibility test, three axes, axis-3 authorship preservation)
- `glossary/engaged-authorship.md`, `glossary/defensibility.md`, `glossary/practitioner.md`, `glossary/claim.md`, `glossary/specialist.md`
- `arch/scope-model.md` §4 E4 cross-cutting non-placed primitives + §3 workspace integration
- `arch/specialist-skill.md` §10 cross-specialist composition rules
- `arch/sparring.md` §1 cross-axis dependency (axis-2 → axis-3 production-phase substrate)
- `pbs/impls/claude_agent_sdk_audit.py` SHA-256 hash chain integrity

## 11. Honest basis caveats

- **Verified directly via web sources cited in §10**: enterprise context-graph problem; tribal knowledge fragmentation; cross-domain coordination failure; Gemini Memory Bank scope (user-centric NOT agent-to-agent); platform offerings address generic AI safety/identity/governance only.
- **Verified earlier this session (1-NEXT.md §10)**: MCP universal adoption + Linux Foundation governance; A2A universal adoption; Microsoft Agent Governance Toolkit framework-agnostic via PolicyProviderInterface; Gemini Enterprise component set; EU AI Act regulatory pressure.
- **Verified earlier this session via PBS framework reads**: claim-attribution + cross-specialist composition + Layer A scope + engaged-authorship + defensibility test + sparring axis-2-to-axis-3 + audit hash-chain — all architectural primitives PBS commits to.
- **Inferred but high-confidence**: that PBS's distributed architectural primitives ARE structurally a context-graph framework for accountability-bearing work — derived from recognizing the pattern across the verified primitives + matching against the verified context-graph definition; not a positioning the existing arch docs use explicitly.
- **Inferred and uncertain**: that PBS would benefit from a unified `context-graph` or `decision-graph` primitive — based on positioning clarity argument; could be wrong if distributed primitives are architecturally cleaner; resolution requires F1+ mental-modeling against §6 scenarios.
- **Inferred and uncertain**: that practitioner-accountability is the SPECIFIC differentiator vs generic context-graph platforms (Galaxy, GraphWise, Stardog) — based on reading their feature lists at the level of search-result summaries; didn't deep-read their offerings; could be substantial overlap I haven't verified.
- **Not verified**: actual enterprise willingness to adopt PBS over rolling their own — speculation; depends on practitioner-accountability discipline being substantive enough to justify adoption; market evidence not collected.
- **Not verified**: that PBS's audit-trail design actually supports context-graph traversal queries — see §9; mental-modeling required at F1.1.
- **Not verified**: that the unified primitive question can be resolved via the three §6 scenarios alone — could surface load-bearing concerns the scenarios don't probe.

## 12. Net

The thin-layer concern was legitimate: at the runtime infrastructure layer, PBS should be thin and leverage platforms. But the SUBSTANTIVE layer — context-graph + cross-domain-knowledge composition + practitioner-accountability discipline — is NOT thin and is precisely the gap enterprises face that platform vendors don't fill.

PBS positioned as **context-graph framework specialized for accountability-bearing professional work** is substantive enough to justify adoption over rolling-your-own. The verified industry need (tribal knowledge fragmentation; cross-domain coordination failure; knowledge foundation before automation; governance/explainability beyond access control) maps directly to PBS's architectural commitments (claim attribution + cross-specialist composition + Layer A scope-resolution + engaged-authorship + defensibility test + sparring engagement substrate + audit-trail integrity).

Open architectural question: does the substantive layer want a unified primitive name (`context-graph` / `decision-graph`) or are distributed primitives sufficient? Mental-model at F1+ via three concrete scenarios; surface decision before F4 enterprise track.

Implications for 1-NEXT.md §3.5/§3.6/§6.6 + F1.0-F1.4 implementation choices captured in §7 above. Apply when reframing 1-NEXT.md.
