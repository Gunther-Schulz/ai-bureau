# Market context / adjacent products

Reference material — not a ledger decision. Captures the space the framework operates in. Positioning ("where we sit" relative to these) is **deliberately deferred** — the framework's identity per D5 (composition system + machine-checkable contracts + accountability-bearing AI-human work) is not yet positioned against these as a deliberate market stance.

## Adjacent / similar-space products (as of 2026-05)

**Commercial agent platforms:**

- **Microsoft Copilot Studio** — SMB-friendly custom-copilot builder; deep Microsoft 365 integration.
- **Google Gemini Enterprise / Agent Marketplace** — newly announced at Google Cloud Next '26; $750M partner fund; partner-built agents from Adobe / Atlassian / etc.
- **IBM watsonx Orchestrate / Advantage Marketplace** — enterprise consulting + marketplace combo; domain agents across legal / finance / HR / etc.
- **Salesforce Agentforce** — for Salesforce-shop customers.
- **Kore.ai** — 300+ pre-built agent templates; marketplace model. *Verticalization-via-shape evidence per D4: 300 templates all running the same engine validates the engine-vs-template split at scale. Cited as rejected-alternative on orchestrator-vs-worker question per D37.*
- **Sana AI** (acquired by Workday 2025) — knowledge platform + agents. *Knowledge-thesis alternative: agents as tools over a central knowledge artifact. Cited as rejected-alternative for "knowledge as core kind" per D38; fresh-plan's I3 makes accountability-bearing work the central organizing primitive, not knowledge.*

**Event-chain / accountability-focused work (closer to fresh-plan's I3 thesis):**

- **AEGIS protocol** (research, 2026) — formal protocol spec: event schema, hash-chain construction (SHA-256 + Ed25519 + JCS canonicalization). Positioned for **EU AI Act Article 12** (effective 2026-08-02). Structurally close to fresh-plan's D10 event chain. *Cited as canonical first integrity-protocol candidate per D40 §B; would land as `aegis-protocol-ext` in Phase C (standards-compat impl per D26).*
- **Axon Framework** (open source, commercial Axoniq) — event sourcing for AI specifically; immutable record of every command / decision / state-transition. Aligned with **EU AI Act, SR 11-7, GDPR Article 22, OCC/CFPB**. Structurally close to fresh-plan's D10. *Validates the event-chain-as-audit-trail thesis empirically; could similarly land as `axon-protocol-ext` if Axoniq-style semantics are demanded.*

## Candidate positioning angles (not committed)

Surfaced from session conversation; pending deliberate positioning work. Sharpened by AEGIS / Axon evidence per the side-quest batch (D37-D40 + this update).

- **Open source** — none of the commercial platforms are; AEGIS + Axon are.
- **Small / individual / craft-practice scale** — the named commercial products are SMB-to-enterprise oriented; AEGIS + Axon are enterprise-grade.
- **Accountability-bearing AI-human work with regulatory alignment** (per D5 I3 + D24 EU AI Act compliance + D40 integrity-mechanism extension point). The framework is structurally designed around attribution + authorship + event-chain audit. The commercial agent platforms treat this as compliance bolt-on; AEGIS + Axon focus on it but as protocols / event-sourcing frameworks (not full agent / work / shape stacks). **This intersection is the cleanest positioning angle**: regulatory-aligned event chain + agent-and-shape stack on top, open-source, small-scale-first.
- **Substantively-neutral framework with shape ecosystems** (per D4) — none of the named products separate framework from shape; each bakes its own substantive opinions in.
- **Cross-vendor interop via standards** (per D21 + D24 + D40) — A2A + MCP + PROV-O alignment as design constraint; integrity-protocol extension point welcomes AEGIS / Axon-style protocols.

## Forward notes (for when positioning is committed)

- **Event-chain-as-audit-trail is a validated pattern.** D10 + I3 + D40 form a coherent architectural answer to the regulatory-compliance landscape (EU AI Act Article 12, GDPR Article 22, SR 11-7, OCC/CFPB). AEGIS and Axon are converging on this independently.
- **Hash-chain + signing is an emerging standard** for accountability-bearing event streams. Fresh-plan's openness on integrity mechanism (D10 leaves it open; D40 names an extension point) is the right pattern — adopt AEGIS or equivalent without baking it into core.
- **Fork-from-state + replay** are derived operations under D39 + D40. Pre-deployment simulation, time-travel debugging, and analytics views are composable from framework primitives rather than reinvented per substrate. This is positioning-relevant.

## Research notes — landscape map for future positioning

Snapshot of who's actually doing workplace-AI-aware-transformation work today (as of 2026-05; not committed positioning, research input for when positioning is settled). The pattern: no open methodology, no shared playbook at practitioner / SMB scale. Each entry has different IP / scope / openness shape.

- **Big-consultancy bespoke engagements** (KPMG / PwC / Accenture / IBM Consulting / Deloitte). Fortune-1000 clients at €5-50M engagement size. Custom per engagement; playbooks proprietary; no shared methodology output between engagements.
- **In-house AI ops teams at large enterprises.** Embedded inside closed organizations. Network-of-agents patterns operating across thousands of documents; methodology stays internal, not published.
- **Vertical AI startups owning one workflow deeply** (Harvey for legal; Hebbia for finance; EvenUp for personal injury). Transform one specific high-value workflow per company; don't generalize across the workplace; closed-source product; single-vertical scope.
- **Solo AI strategy consultants / boutique implementers.** Many in 2026, especially LinkedIn-visible. Per-client bespoke; rarely have framework / IP; mostly billable-hours wrapping ChatGPT / Copilot / Claude / Cursor. No shared methodology.
- **Thought leaders writing about it** (Ethan Mollick *Co-Intelligence*; "The Intelligence Age" essays). Books / essays / frameworks-as-prose. Not implementable methodology.
- **The practitioners themselves, doing it manually.** Planners, lawyers, architects, accountants individually working out how to integrate AI into their authoring of accountability-bearing artifacts. Re-invented per practitioner; no shared structure.

### What this map suggests (research direction, not committed)

- **No open framework + methodology for workplace-AI-aware-transformation at practitioner / SMB scale.** The named buckets each have IP / scope / openness reasons not to publish.
- **Closest analogs from prior paradigms**: GoF design patterns book (1994) for OO transformation; Agile Manifesto + Scrum (2001+) for waterfall→agile; Domain-Driven Design (Evans, 2003) for complex business domains. Each took 5-15 years to become widely adopted; each created a generation of practitioners + small consultancies who could deliver the transformation; none vendor-tied.
- **pbs-bureau corpus** already gestures at methodology (DISCIPLINES.md, profiles/L*.md, arch/, process-kit/) alongside framework architecture. The fresh-plan ledger has been sharpening framework architecture; methodology layer is currently dormant input per the fresh-plan README's "preservation / input only" framing.
- **Aspiration vs current state**: methodology positioning is reasonable aspiration once practitioner evidence accumulates (Phase D PBS-Schulz as first case; Phase E multi-deployment validation as scale evidence). Not current state. Premature claiming would be unsupported.

Action: track this as research input. Revisit when positioning is deliberately settled (likely Phase D or later per D26).

## Notes

- This file is **reference / input only**, parallel to how `pbs-bureau/VISION.md` etc. are treated as input per the fresh-plan README.
- Updates: add new adjacent products / positioning candidates as they surface. No supersedes discipline; this is not a locked ledger.
- When positioning is deliberately settled, it'll land as a decision entry (likely during Phase B or Phase D when the framework has enough concrete identity to position against alternatives).
