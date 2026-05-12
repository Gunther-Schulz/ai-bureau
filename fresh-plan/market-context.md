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

## Research notes — vision framing: "AI as workspace, not app"

Snapshot of a sharper positioning framing surfaced in research (cross-session input as of 2026-05; not committed positioning). Captured here so it's available for future ledger / positioning work.

### The framing

Dominant model today: AI is an app you switch into — open ChatGPT for a question, open Claude for a draft, open Copilot in Word, open Cursor for code. AI is one more tile on the dock alongside Email, Calendar, Files, Slack, CAD viewer, accounting.

Sharper framing for fresh-plan: **AI is not on the dock — AI is the dock.** The workspace itself is AI-native. All artifacts (Begründungen, Festsetzungen, Stellungnahmen, evaluations, the project's events, cross-document relationships) live inside it. External tools (email, CAD, file storage, accounting) are adapters into the workspace, not destinations the practitioner leaves to. The practitioner doesn't "use AI" — they work inside an AI-aware substrate where AI is woven into how artifacts evolve, how decisions get recorded, how cross-document coherence is checked.

### Architectural lineage (real, citable)

- **Engelbart's NLS / "Augmenting Human Intellect"** (1962-68) — the system is the workspace; everything composes inside it. "Mother of All Demos."
- **Smalltalk image** (1980s) — persistent world where everything lives; not apps you launch.
- **Plan 9 from Bell Labs** (1990s) — workspace as primary surface; everything is a file in a unified namespace.
- **Emacs as a way of life** — single environment people live in for decades.
- **Magic Cap / General Magic** (1990s) — early personal-agent workspace attempt.
- **AI-era gestures**: "AI OS" thinking (Altman); Copilot+PCs (Microsoft); Rabbit R1 / Humane AI Pin (hardware attempts). Each is a half-step — Microsoft's framing is "AI everywhere in your existing OS"; the workspace-as-substrate framing is "the workspace IS the AI substrate."

The lineage has perfect architectural coherence and a near-perfect record of non-adoption at scale. NLS, Smalltalk, Plan 9, Emacs — all coherent, none won the general desktop. Fresh-plan's bet uses different levers (open framework + shape ecosystems + standards alignment per D4/D24/D40 + accountability-bearing per I3) that *may* survive where prior attempts didn't. Honest: not guaranteed.

### How fresh-plan's primitives already serve this (no architecture change needed)

- **D5 I1** (composition system) — the workspace IS the composition; not an app you visit.
- **D7** workspace kind — first-class identity / composition / state / lifecycle; persists across machines / sessions / years. Same shape as Smalltalk-image + Engelbart-NLS persistence.
- **D10** event chain — everything that happens in the workspace gets captured; the workspace owns the timeline.
- **D13** shape — substantive identity / disciplines the workspace carries. Practitioner-shape, autonomous-business-shape, personal-OS-shape — each configures the workspace's character.
- **D16** adapter — external surfaces (email, file system, CAD, calendar) are adapters into the workspace, not destinations the practitioner leaves to.
- **D19** specialist — capabilities native to the workspace; always-on, not invoked-per-session.
- **D20** work-unit — units of work live in the workspace with lifecycle and accountability.

The spec doesn't have to change for this vision. Sharpens it.

### What it clarifies about positioning

**Necessary but not sufficient.** "AI as workspace" is rhetorical territory others claim — Microsoft (Copilot+PCs), Google (Workspace AI), even OpenAI (Operator). The phrase alone doesn't distinguish fresh-plan. What actually distinguishes is the **combination**:

1. Workspace as the medium (this framing)
2. Shape-neutrality (D4) — substantive identity is shape policy, not vendor-baked
3. Accountability-bearing (I3) — work, not just chat; attribution + audit are first-class
4. Standards-interop + extension protocols (D24 + D40) — adapters into vendor services, not lock-in *to* vendor substrate
5. Open framework + craft-practice scale — not enterprise-bespoke; not vendor-owned

**"Sovereign workspace" framing requires honest caveats.** The practitioner still depends on vendor APIs (email server, file storage, CAD, accounting). What fresh-plan offers is **composition-ownership** — the practitioner owns the *manifest* + *event chain* + *shape policy*, not the underlying services. Adapters wrap vendor APIs; vendors keep their lock-in within their own service. Honest framing: "framework-aware composition layer where the practitioner is sovereign over how things compose, not where the underlying services run."

### Tensions this surfaces

- **UX-boundary design**: workspace-as-primary-surface (high-commitment for practitioner; they must move into it) vs workspace-as-coherent-substrate-behind-existing-UIs (low-commitment; weaker delivery of the "AI is the medium" promise). Real design tension at Phase D when PBS-Schulz pioneer impl gets concrete.
- **Bucket-A philosophical conflict**: vendor-substrate platforms want practitioners living *in their substrate*. Fresh-plan's framing says the workspace is sovereign with adapters *out* to those systems. This is not neutral coexistence — it's a quiet alternative thesis to vendor-lock-in.
- **5-10 year build, not v0.1.** Integrating N existing tools (email + calendar + CAD + files + accounting + communications) with maintenance + vendor-API churn is the slow grinding work after the architecture is right. The historical lesson from Emacs / Plan 9: integrating-everything is what takes a decade. Worth being explicit that workspace-as-substrate is decade-scale infrastructure-shaping work, not a quick product.
- **Engelbart-scale ambition with one author** (currently). PBS-Schulz daily use is what makes the work intrinsically valuable to the author regardless of external adoption; the spec + methodology survive even if scale-adoption takes 5-10 years or never arrives.

### Future-ledger candidates (deferred per "positioning is deferred")

When positioning is committed (likely Phase D PBS-Schulz pioneer impl, or later):

1. **Positioning clarification under D5** — adds "AI as workspace, not app" as an explicit framing of I1 composition system. Not a new identity claim; a framing sharpening.
2. **Practitioner-shape axis-3 sharpening** — the VISION three-axes (intertwining / sparring / authorship-preservation) carried as practitioner-shape policy per D4: axis-3 "intertwining" may sharpen to "workspace-as-medium-not-tool" with this framing. Becomes architecturally specific in shape policy without affecting framework-core.

Both candidates explicitly deferred per the existing discipline — positioning is committed only when practitioner evidence accumulates.

Action: persist as research input; integrate into future positioning work when it's deliberately settled.

## Tagline (stake-in-the-ground; 2026-05-12)

**Locked tagline**: *An open specification for accountable agent-human work.*

What this commits to (and why this phrasing):
- **"open specification"** — primary deliverable framing per the durability bet (CONCEPTS "What is durable vs scaffolding"). Spec, not platform; the runtime is exemplar, not canonical. Open per the candidate-positioning "open source" angle above.
- **"accountable"** — load-bearing word; mirrors I3 (D5) directly. Distinguishes from agent platforms that treat accountability as compliance bolt-on (Bucket A platforms) vs frameworks that center it (AEGIS / Axon, but those are protocols-only, not the full agent / work / shape stack).
- **"agent-human work"** — captures composition (humans + agents in one workspace); deliberate ordering puts agent first (signals AI-augmented work as the assumed shape, not human-with-AI-tools); "work" not "workflow" / "tasks" / "operations" because work-unit (D20) is the framework's organizing primitive and the term carries the right weight (work in the craft / professional sense).

What's NOT in this lock:
- **No name yet.** Tagline reads cleanly without one; name decision deferred. Candidates explored in 2026-05-12 side-quest (Praxis / Accord / Werk / Atrium / Concord) all rejected. The tagline lives without a name until the name lock arrives.
- **Tagline lock ≠ positioning lock.** Tagline is a stake-in-the-ground — useful for sharpening design intent + giving the framework consistent self-description in conversations. Full positioning (against the named commercial platforms + AEGIS / Axon + the standards landscape) still deferred per the existing discipline; lands as a decision entry when Phase D pioneer evidence accumulates.

Use the tagline now in: README hero text (when ship-time arrives), conversational self-reference, design-intent sharpening. **Do NOT use** in committed ledger entries until positioning lock arrives — D-entries should describe substance, not branding.

## Notes

- This file is **reference / input only**, parallel to how `pbs-bureau/VISION.md` etc. are treated as input per the fresh-plan README.
- Updates: add new adjacent products / positioning candidates as they surface. No supersedes discipline; this is not a locked ledger.
- When positioning is deliberately settled, it'll land as a decision entry (likely during Phase B or Phase D when the framework has enough concrete identity to position against alternatives).
