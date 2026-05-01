# pbs-bureau vision

This document anchors the deepest "why" behind the architecture. Every design decision and every commitment traces back to one thesis. When in doubt about whether a proposed feature belongs, check it against this thesis first.

## What this is, in one line

**A workspace pools and leverages codified expertise (bundled as specialists) to automate and support interactive practitioner workflows in a coherent manner.**

Target users: solo professionals and small companies in expert-practitioner domains (planners, lawyers, researchers, accountants, consultants, boutique firms). Not enterprise federated deployments — that's a different archetype with a documented migration path. Single-big-model orchestration's strengths (domain coherence, low operational overhead, vendor-neutral, big-context cross-specialist reasoning) land precisely in the solo-to-small expert-practitioner segment.

PBS-bureau is the pioneer instance of this workspace infrastructure — specifically a Planungsbüro (German planning bureau) workspace shape. The patterns generalize to any practitioner workspace shape (legal practice, research lab, creative studio, etc.).

## What this framework also is

PBS as marketed product is the workspace infrastructure for expert practitioners. PBS as framework contribution is broader: **a method-and-architecture for building accountability-bearing AI-co-worker systems for any expert-practitioner archetype.**

The framework comprises three load-bearing layers:

1. **Architectural patterns** reusable across AI-co-worker systems: framework=mechanisms / shape=policies; A-B-C scope model (Framework C definitions / Owner B instances / Layer A layered content); Pattern A protocol pluggability (Surface + Implementations + Instance/binding); bipartite multi-aspect primitives (Patterns B + C: definition+instance-content; human+record).

2. **Dev-skill methodology** for building such systems: pre-decision sharpening (decision-design + pre-implementation phases); coherence-audit (cross-decision corpus auditing); applying sparring as runtime mechanism to the development process itself (the architecture's own discipline applied recursively).

3. **Working disciplines** for sustaining architectural integrity: cascade discipline (changes propagate up/down/sideways); preliminary-lock principle (decisions revisable except VISION axes); pattern-vs-instance discipline (instance-anchoring leakage is the primary framework failure mode); make-wrong-shapes-impossible (structural constraints over conventions); no-defer (decisions made now; info-gaps as watch-list); source-grounded (every assertion has a basis).

The pioneer instance (PBS-Schulz, German Planungsbüro) is BOTH a real workspace deployment AND a research-lab for the framework. Framework discoveries surface through pioneer-instance work; pioneer-instance soundness depends on framework integrity. This co-evolution is intentional, not incidental.

## VISION scope — practitioner shape

This document articulates the **practitioner-shape thesis** — the value claims PBS makes for expert practitioners (planners, lawyers, researchers, accountants, creatives, consultants, advisors). It is the pioneer-instance + marketed-product VISION.

**The framework underneath is workspace-shape-neutral.** Framework primitives support multiple workspace shapes (each shape composing policies over framework mechanisms): practitioner (this VISION's domain), autonomous-business (operator-supervised), personal-OS (individual life-OS), knowledge-graph, federation, hybrid. Other shapes have their own potential per-shape visions if productized.

**Three VISION axes apply with full force to practitioner shape.** When second-shape productization happens, that shape gets its own per-shape VISION; this document remains the practitioner-shape articulation.

The framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory. Positioning narrowness (why practitioner-shape is what PBS markets; funding fit; competitive landscape) lives in STRATEGY.

## The thesis

PBS is built on three interlocking principles. None alone is sufficient; all three together define the design space:

1. **PBS is intertwined-AI-workflow, not tacked-on AI features.** The AI is a co-worker in the workflow itself, not a feature bolted onto an unchanged human workflow.

2. **Sparring as load-bearing runtime mechanism, not optional skill or answer machine.** AI challenges, generates counter-arguments, names uncertainty, resists giving easy answers — as always-on runtime pillar, not as opt-in skill called per-task. Keeps the practitioner critically engaged.

3. **PBS produces output the practitioner remains the author of.** Not teaching, not capacity-building in the abstract; preserving the practitioner-author's role as the expert who can defend, sign, and stand behind the produced work.

Three axes. Each must be served:

| Layer | Axis | Failure mode | PBS aim |
|---|---|---|---|
| Surface | Workflow embedding | Tacked-on: discrete AI features in unchanged workflow | Intertwined: AI as continuous co-worker |
| Process | Interaction mode | Answer machine: oracle / sycophant / easy answers | Sparring partner: challenger / interrogator / counter-argument |
| Purpose | Outcome orientation | Rubber-stamping: AI produces, practitioner-author signs without engagement | Authorship preservation: practitioner remains defensible expert author |

A system can fail on any axis independently:

- Tacked-on but well-designed sparring (a "find weaknesses" button) is still tacked-on (axis 1 failure).
- Intertwined but answer-machine (AI runs the workspace, practitioner-author rubber-stamps) breaks axes 2 and 3.
- Intertwined sparring that produces work the practitioner-author can't defend (no audit trail, opaque reasoning, no engagement with judgment calls) breaks axis 3.

PBS aims for all three: **intertwined sparring partnership in service of defensible authorship.**

The contrast that makes axis 1 concrete:

| Tacked-on AI | Intertwined AI |
|---|---|
| Discrete features bolted onto existing tools | AI is a co-worker in the workflow itself |
| Transactional ("summarize this email") | Continuous ("what's pending; what's next; draft this section") |
| Workflow stays human-driven; AI offers convenience | Workflow is fundamentally collaborative |
| Trust is low; user checks every output | Trust is high; AI participates in real work output |
| No persistent state; each invocation fresh | Persistent state across sessions; AI remembers context |
| AI is an assistant on the side | AI is in the loop |

Most "AI agent" demos are tacked-on. PBS aims for the deep end: real intertwining where the AI is a participating colleague in the actual production of accountability-bearing work-products — not a feature that helps you write them faster.

## What VISION does NOT claim

Drawing the negative space sharpens the positive:

- ❌ PBS does NOT claim practitioners become obsolete
- ❌ PBS does NOT claim AI replaces human judgment
- ❌ PBS does NOT claim it optimizes for speed at the cost of capacity
- ❌ PBS does NOT claim sparring is always the right interaction mode (oracle mode is right for fact lookup; sparring overhead misplaced for trivial questions)
- ❌ PBS does NOT claim audit-by-construction makes humans unnecessary — it makes their accountability defensible
- ❌ PBS does NOT claim AI-as-co-worker means AI does the bulk of the work — could be AI handles 20% of mechanical labor, augments practitioner on the 80% where judgment matters
- ❌ PBS does NOT claim the framework is restricted to practitioner shape — framework is shape-neutral; positioning is practitioner-focused

## Robustness to AI capability growth

Question: as frontier models become MUCH better (2027+ AGI-trajectory), does VISION still apply?

**All three axes are robust** because the load-bearing claims are **accuracy-independent**:

- **Axis 1 (intertwined-AI-workflow)**: workflow integration depth is independent of AI capability. Better AI just makes integration more valuable.
- **Axis 2 (sparring)**: per Ming's IEP — capacity-preservation concern is **accuracy-independent**. Even if AI is 99.9% correct, exploration capacity matters. Better AI RAISES the temptation to abandon exploration; doesn't eliminate the value of exploration. Sparring becomes MORE valuable as AI accuracy increases.
- **Axis 3 (authorship preservation)**: accountability cannot be delegated regardless of AI capability. As AI improves, regulatory frameworks tighten; practitioner-as-author becomes MORE load-bearing, not less.

The capacity-preservation thesis strengthens with better AI; it does not weaken.

## Falsification criteria

Pioneer-instance honesty: what would empirically falsify each axis?

- **Axis 1**: falsified if practitioner deployments show better outcomes from tacked-on features than continuous co-work. Watch for: feature-by-feature satisfaction higher than orchestrated workflow.
- **Axis 2**: falsified if real sparring sessions consistently degrade output quality vs oracle mode. Watch for: practitioner friction without quality improvement; sparring-bypass-rate trending up.
- **Axis 3**: falsified if defensibility ISN'T enhanced by structural authorship (regulators don't care about audit trails; insurers don't reward source-grounding; courts don't honor decision provenance). Watch for: real defensibility events where audit-trail provided no benefit.

**Update triggers**: real Phase 1+ corpus deployment data; first-bind real use; per-axis empirical signal; major regulatory interpretation shift.

## Foundations

VISION needs anchors. PBS draws on specific research and thinking that future alignment checks reference back to.

### Vivienne Ming — sparring as the productive mode (axis 2 anchor)

Theoretical neuroscientist and cognitive scientist Vivienne Ming ran an experiment (reported in Wall Street Journal; expanded in her book *Robot-Proof: When Machines Have All The Answers, Build Better People*) testing human teams, AI teams, and human-AI hybrid teams at predicting real-world events against prediction markets. Three modes of hybrid interaction emerged, with starkly different outcomes:

- **AI as oracle** (most hybrid teams): humans submitted AI's answer as their own. Human contribution: zero. Performance: same as AI alone.
- **AI as validator** (some hybrid teams): humans asked AI to support their preconceptions. Confirmation-bias loop; sycophancy. Performance: **worse than AI alone.**
- **AI as sparring partner** (5–10% of hybrid teams): humans pushed back, demanded evidence, interrogated assumptions. AI generated counter-arguments, surfaced doubts, resisted easy answers. Performance: rivaled or beat prediction markets — insights neither human nor AI alone could reach.

Only the third mode produces the value. The first two waste the human partner — and the second actively degrades it.

### Information-Exploration Paradox (axes 2 + 3 motivation)

Ming names the **Information-Exploration Paradox**: as the cost of information approaches zero, human exploration collapses. Students perform better on AI-assisted tasks, worse on everything afterward. Developers ship more code, understand it less. "We are slowly optimizing ourselves out of the loop."

The capacities AI is consuming are precisely the ones that matter:

- Capacity to be wrong in public and stay curious
- Sitting with a question your phone could answer in three seconds
- Reading a confident, fluent AI response and asking "what's missing?" instead of defaulting to "great, that's done"
- Disagreeing with something that sounds authoritative and trusting your instinct enough to follow it

Most AI products are designed to deliver the answer before the user feels the discomfort of not having one. PBS aims for the opposite: **deliver discomfort productively**, in service of the practitioner-author's growing capacity.

### Adjacent thinkers

Cited in axis bodies but not promoted to anchor status (avoid diluting Ming):

- **Donald Schön** (*The Reflective Practitioner*) — practitioner authoring via reflection-in-action; relevant to axis 3
- **Hubert Dreyfus** (skill acquisition; novice → expert progression) — practitioner-shape audience grounding
- **Daniel Kahneman** (System 1 / System 2) — sparring as System 2 forcing function; relevant to axis 2

### Empirical regulatory evidence (axes 2 + 3 universality)

Regulatory environments globally converge on practitioner-amplification rather than practitioner-replacement for accountability-bearing work. Examples:

- **EU AI Act Article 14 (human oversight)** — sparring operationalises this requirement
- **Professional liability frameworks** (DACH Berufsrecht / Berufshaftpflicht; ABA Model Rules in US; SRA conduct rules in UK; equivalent professional codes elsewhere) — practitioner-as-author is the cleanest professional-liability posture; authorship-preservation is regulatory-rewarded across jurisdictions

These are evidence of axis-2 and axis-3 universality, not jurisdictional anchoring of the axes themselves.

When auditing for drift, foundations are the reference point: are we still doing what Ming's research identified as the productive mode? Are we still serving the concerns she names about capacity atrophy? Foundations grow as we engage with more research; add new entries when external work becomes a reference for our own alignment checks.

## Sparring partner, not answer machine (axis 2)

The second axis. Even an intertwined AI can fail badly if it operates in answer-machine mode. The Ming research foundation makes the claim concrete: only sparring-mode produces the value; oracle wastes the human partner; validator actively degrades.

### Why text-first matters here

Sparring is a text-shaped interaction. You can argue with text — push back, demand evidence, ask follow-ups, sit with a counter-argument. You cannot argue with a "summarize" button or an autocomplete suggestion. The CLI's pure text I/O is the most sparring-shaped surface possible.

Speech-to-text counts (text-equivalent). GUIs that funnel through chat-shaped surfaces count. But GUIs that reduce interaction to button-presses and form-fills break sparring — they revert toward answer-machine mode by design. This is part of the category-collapse risk in frontend integrations: a host environment that doesn't support text-first discussion will collapse PBS into a tacked-on feature regardless of architectural intent.

How sparring is encoded structurally (counter-argument as first-class output, confidence calibration, visible reasoning, selective friction, etc.) is ARCH territory.

## Authorship preservation, not rubber-stamping (axis 3)

The third axis. Even an intertwined AI in sparring mode can fail if the produced output isn't something the practitioner-author can genuinely defend.

### What PBS is and isn't

PBS is **an output-producing tool for an expert practitioner.** Not a teaching tool. The practitioner is already an expert author with years of domain knowledge; PBS does not exist to make them a better author. It exists to help them produce more work-products, more consistently, with better citation hygiene, in less time.

But the produced work-products go out under the practitioner-author's name (or the firm's name with the practitioner-author signing). They get signed, sent to authorities or clients, defended in challenge contexts (correspondence exchanges, council meetings, court hearings, peer review, audit committees, etc. — the specific fora vary per practitioner archetype). The practitioner-author is legally and professionally accountable for everything PBS produces on their behalf.

This creates the third axis: **PBS produces output; the practitioner remains the author.** Authorship in the professional/legal sense — capable of defending the output, accountable for what's signed, having engaged with the judgment calls. Capacity-building in the abstract is a side effect when it happens; authorship preservation is the actual purpose.

### The defensibility test

A sharp, operational test for whether the architecture is doing its job:

> **Will the practitioner-author be able to defend this output six months from now under regulatory or professional challenge, having forgotten the details?**

If yes — the practitioner understood the judgment calls, the reasoning is reconstructable, the audit trail captures the why — the architecture works. If no — AI did the work, practitioner signed; no engagement, no defense — that's authorship collapse, regardless of how good the output looked when shipped.

This test cuts through edge cases:

- A perfectly automated drafting feature that removes the practitioner's engagement with key argumentation choices fails (practitioner can't defend the choice later).
- A "skip review" shortcut that bypasses layered review fails.
- A summarization feature that compresses reasoning into pithy bullet points (losing the chain) fails (defense requires the full chain).
- A fully automated send pipeline (no practitioner review of the cover communication — Anschreiben in PBS-Schulz pioneer; cover letter / transmittal note in other archetypes) fails (the practitioner owns the words sent under their name).

All might pass axes 1 and 2 (intertwined, sparring-friendly in some sense). They fail axis 3.

How authorship preservation is encoded structurally (visible reasoning, layered review, audit trail, lifecycle gates, etc.) is ARCH territory.

### Trust + sparring + authorship together

Three forms of protection composing into one architecture:

- **Trust mechanisms** (axis 1): protect the practitioner *from* the AI — no invented citations, no silent state changes, no unauthorized sends.
- **Sparring mechanisms** (axis 2): protect the practitioner *from comfortable but degrading interaction patterns* — no oracle worship, no sycophancy loop, no easy answers everywhere.
- **Authorship mechanisms** (axis 3): protect the practitioner's *professional/legal standing* in everything PBS produces on their behalf — no rubber-stamping, no signature without engagement, no work the practitioner can't defend.

A system with full trust + sparring but weak authorship preservation produces accurate, well-reasoned drafts the practitioner signs without understanding — works until challenged. A system with full authorship preservation but weak trust or sparring is engaged but unreliable — the practitioner defends bad output well. PBS aims for all three, in service of work that is **correct, defensible, and genuinely the practitioner's.**

## Implications

Four implications worth surfacing here (the rest live in ARCH or STRATEGY):

### Workflow as precondition (axis 1)

Intertwined AI needs a workflow to intertwine with. Domains with rich, structured workflows (planning, law, engineering, healthcare, accounting) are natural fits — there's a real pattern of work to embed in. Generic "knowledge work" without explicit workflow is much harder; nothing concrete to intertwine with.

### AI-as-runtime as precondition (all axes)

The three axes require AI participation in RUNTIME work — not as pre-computed-tooling consumer, but as the runtime executor of memory access, reasoning, claim production, sparring engagement, source verification. Axis 1 is impossible without runtime AI participation (no co-worker = no intertwining). Axis 2 is impossible without runtime engagement (no AI to spar with at the relevant moments). Axis 3 requires reasoning-chain-traceable claims that emerge from runtime AI work (post-hoc-defensible chains require capture-at-creation, not retrofit).

This commits the architecture to **AI-as-runtime hybrid-shape**: AI is load-bearing at runtime, not abstracted behind deterministic-only logic. The pre-RAG-database trap (build deterministic SQL-style tooling that AI consumes) is the failure mode this commitment guards against. Memory, reasoning, claim-state, and sparring engagement are markdown-skeleton-plus-AI-reads-at-runtime, not Pydantic-models-AI-consumes.

### Category-collapse risk (axis 1 protection)

The biggest risk to the thesis is **category collapse**: PBS gradually reduced to a "tacked-on" feature catalog because each discrete addition seemed reasonable in isolation. Especially at risk: GUI integrations into hosts where the host's UX paradigm is feature-driven. Each integration must be checked: does it expose intertwined workflow, or does it reduce PBS to a "summarize this" plugin in someone else's tool? The first is a frontend; the second is category collapse.

### Pattern-vs-instance discipline (framework integrity protection)

Framework primitives are PATTERN-LEVEL, not pioneer-instance-anchored. Instance-anchoring leakage — defining a primitive in terms of pioneer-specific assumptions (PBS-Schulz solo-human practitioner; German planning bureau workflow; DACH regulatory specifics; EU AI Act terminology) — is the primary framework failure mode. The session-16 rebuild was triggered by five such leakages accumulated across the corpus.

This discipline protects the framework's shape-neutrality (per "What this framework also is" + line 17 above) operationally: every primitive must work for hypothetical legal-practice / research-paper-review / engineering-doc / personal-OS workspaces. Pioneer-instance examples appear as illustrations, not load-bearing claims. Verifiable structurally — coherence-audit's instance-leakage lens explicitly tests "would this primitive work for hypothetical X workspace?" before locking.

Pattern-vs-instance discipline is what makes the framework distributable as method (per "What this framework also is" — distinct from pioneer-instance + workspace-deployment).

## How to use this document

Three checklists, one per axis:

**Axis 1 — Workflow embedding (intertwining):**

- Does the proposed feature serve persistent-state / orchestration / source-grounding / audit / continuous-awareness / human-authority? If discrete and disconnected, ask whether it belongs.

**Axis 2 — Interaction mode (sparring):**

- Does the proposed feature support counter-argument / confidence calibration / "what's missing?" checkpoints / selective friction / asymmetric knowledge respect / anti-sycophancy / commit-to-recommendations / visible reasoning? Or does it deliver easy answers, suppress uncertainty, automate engagement away?

**Axis 3 — Authorship preservation (defensibility):**

- Will the practitioner be able to defend the output six months from now under challenge, having forgotten the details? Does the feature preserve the practitioner's role as expert author, or edge them toward rubber-stamping?

**For frontend integrations:**

- Axis 1 check: does it expose intertwined workflow, or reduce PBS to a tacked-on feature in someone else's tool?
- Axis 2 check: does the frontend support text-first discussion, or funnel through buttons that break sparring?
- Axis 3 check: does the frontend preserve the practitioner's visible engagement with judgment calls, or hide them behind UX convenience?

**For drift audits:**

- Has any recent addition collapsed PBS toward "AI feature catalog" (axis 1 drift)?
- Has any recent addition collapsed PBS toward "answer machine" (axis 2 drift)?
- Has any recent addition collapsed PBS toward "rubber-stamp signing" (axis 3 drift)?

This is the deepest anchor. ARCH describes how the system is structured; this document describes why and against what failure modes.

## Where this fits

VISION = WHY (value claims). ARCHITECTURE = HOW (structural primitives + disciplines). STRATEGY = MARKET (positioning + competitive landscape + funding).

Cross-doc: VISION axes get IMPLEMENTED in ARCH; STRATEGY engages with opposing market thesis (service-as-software vs PBS practitioner-amplification).

**Update triggers + lifecycle**: VISION review fires periodically alongside major architectural rebuilds. Specific triggers: major AI capability shift; major regulatory shift; real Phase 1+ deployment data showing axis-falsification signal; cross-deployment second-domain validation; strategic positioning shift (would unscope VISION + trigger per-shape VISIONs).

## Document history

- v0.1 (initial): three-axis thesis articulated
- session 13: AI workspace framing (was AI office); shape-neutral framework + practitioner positioning layered approach
- session 14: Round 1 axis refinements + Round 2 sharpening; VISION scope section + falsification + robustness + counter-VISION engagement reference
- session 16 (rebuild Phase 1.75): tightening pass. Content moved out lives in `archive/VISION.md` (the v0.35 snapshot); new phases consult archive selectively rather than via promised lift-lists.
  - **Removed (content available in archive)**: ARCH-territory mechanism lists (intertwining requirements / trust infrastructure mechanisms / sparring mechanisms with Pydantic refs and structural-status table / authorship structural requirements / Workspace shapes section); Pioneer-instance commitment + framework-foundation framing (these are design disciplines, not value claims); Triple purpose / deployment hierarchy / four deployment possibilities / counter-VISION engagement / transition path / frontend determines accessibility / Cherry Ventures + EU AI Act fundability framing; Practitioner vs Specialist vocabulary; Multi-practitioner implications subsection.
  - **Resolved contradictions**: Architectural inheritance / Option B floor subsection (asserted framework-level structural enforcement of axis 3, contradicting practitioner-shape scope claim — removed; floor mechanism, if any, is ARCH territory). Axis-3 standalone (no longer claims framework-level enforcement). Three-vs-four deployment-possibilities count inconsistency (deployment count moved out entirely).
  - **Reframed instance-anchored language**: practitioner kind-neutral (singular-human assumption removed; kind variation per-deployment); defensibility test generalized (UNB → "regulatory or professional challenge"); regulatory anchors generalized (DACH as illustration of broader pattern; ABA / SRA / equivalents acknowledged).
  - **Vocabulary drift swept**: no "office" terms; no chronological-defer wording (superseded by v0.33 no-defer principle in `memory/`); no archived-doc cross-refs.
  - Net: 1069 → ~280 lines. Three axes preserved exactly; foundations preserved inline; falsification + robustness preserved; defensibility test preserved (generalized).
- session 16 (rebuild Phase 1.8): VISION terminology audit on its own. ~15 candidate terms walked through 6 families (workspace / practitioner / sparring / authorship / framework / meta). 2 inline tightenings applied: (1) dropped "AI" prefix from "AI workspace" (every PBS workspace is AI by design — redundant); (2) parallel wording in 3-layer protection summary ("trust mechanisms / sparring mechanisms / authorship mechanisms" — replaced inconsistent "infrastructure" suffix). All other terms deferred to GLOSSARY (Phase 2) for formal lock — VISION's usage was already consistent in context; what's missing is canonical definitions, which is GLOSSARY territory not VISION's. The audit's value: confirmed term list GLOSSARY must lock, derived from VISION's actual usage rather than abstract architectural concepts.
- session 16 (rebuild Phase 1.85): VISION sanity check (3-lens scan against 28 locked GLOSSARY entries) + expansion pass. **Sanity check** applied 4 small fixes: shape-extension-pattern outdated framing → "shape definitions composing policies over framework mechanisms"; anti-sycophancy added to axis-2 sub-mechanism checklist (was 7, now 8 matching GLOSSARY); two minor instance-anchoring generalizations (council meetings → challenge contexts; cover mail → cover communication). **Expansion pass** added: (1) new "What this framework also is" section articulating the framework as method-and-architecture (not just product), with three load-bearing layers (architectural patterns / dev-skill methodology / working disciplines); (2) "AI-as-runtime as precondition (all axes)" implication; (3) "Pattern-vs-instance discipline (framework integrity protection)" implication. Implications grew from 2 to 4. Driver: holistic view that VISION served Phase 2 GLOSSARY adequately but would under-serve Phase 3+ ARCH because it treated the framework's methodological contribution + architectural-integrity disciplines as implicit rather than explicit value-claims.
