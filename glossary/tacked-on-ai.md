---
entry: tacked-on AI
class: DERIVED
layer: cross-cutting
axis: axis-1
vision_usage: directly-used
---

# tacked-on AI

- **Class**: DERIVED (failure mode of axis 1; the contrast / anti-pattern)
- **Layer**: cross-cutting
- **Axis**: axis-1 (failure mode of axis-1)
- **VISION usage**: directly used (`VISION.md` line 37 + 53 axis-1 contrast tables; line 43 axis-interaction: "Tacked-on but well-designed sparring is still tacked-on (axis 1 failure)"; line 60: "Most 'AI agent' demos are tacked-on"; line 90 axis-1 falsification: "falsified if practitioner deployments show better outcomes from tacked-on features"; line 150 + 205 + 225: category collapse explicitly produces tacked-on shape)

**Canonical**: The architectural failure mode for axis 1 — AI as discrete convenience-feature bolted onto an unchanged human workflow; no cross-session state; no orchestration awareness; no colleague-grade discipline. Per VISION: the contrast that makes axis 1 concrete; what intertwining is NOT.

**What it is**: The architectural anti-pattern. Concrete markers of tacked-on:
- AI provides convenience features (summarize this; format that; suggest synonyms) on the side of unchanged workflow
- Workflow itself is unchanged — practitioner drafts, reviews, sends as before; AI is a side-tool not a co-worker
- No cross-session memory: each interaction starts fresh
- AI output isn't held to source-grounding / audit / defensibility discipline (because it doesn't compose into accountability-bearing work-products)
- Most "AI agent" demos and most current AI-product integrations are tacked-on by default — adding "AI to existing tool" usually preserves the tool-shape and adds AI-as-feature

Tacked-on AI is the LANDSCAPE DEFAULT against which axis 1 deliberately positions; recognizing it requires understanding what intertwining looks like in contrast.

**What it is NOT**:
- Not "bad AI" or "low-capability AI" — tacked-on can be technically excellent and still be tacked-on (a brilliant AI summarizer that doesn't change workflow shape is still tacked-on)
- Not "AI assistant" specifically — AI assistants CAN be intertwined or tacked-on depending on architectural integration depth; the failure mode is structural, not naming
- Not the same as "tool use" — AI using tools is a substrate capability; tacked-on is about whether AI participation reshapes workflow
- Not a moral failing — tacked-on is the SAFE DEFAULT; intertwining requires deliberate architectural choice + workflow as precondition

**Cross-archetype illustration** (tacked-on failure modes per archetype):
- Practitioner-shape: planner uses AI to summarize sources but drafts Begründung manually with no AI participation in argumentation = tacked-on
- Legal practice: lawyer uses AI for legal research lookup but writes brief without AI co-drafting = tacked-on
- Research lab: researcher uses AI to format citations but writes manuscript without AI methodology engagement = tacked-on
- Auditor: auditor uses AI to spell-check report but writes findings without AI evidence-traversal = tacked-on
- Generic-knowledge-work: any AI-in-text-editor where AI suggests improvements on already-drafted text = tacked-on by default

Same anti-pattern shape across archetypes: AI on the side, not in the workflow. Mixed-state common in transition deployments — partial intertwining at some workflow stages with tacked-on at others; recovery starts by deepening architecture at the tacked-on stages.

**Boundary test**: Three questions (mirror of intertwined AI; tacked-on markers):
1. Does AI only participate when explicitly invoked? → if yes, tacked-on
2. Does AI output live in side-channel chat (doesn't compose into artifacts)? → if yes, tacked-on
3. Does AI restart fresh each session with no work-state awareness? → if yes, tacked-on

Any "tacked-on-side" answer = axis 1 at risk; all three = full tacked-on failure.

**Cardinality + lifecycle**: N/A — failure-mode shape, not instance. The mode manifests whenever axis-1 mechanisms are absent OR the workflow precondition is missing OR category collapse forces tacked-on shape regardless of intent. Mode state can shift in BOTH directions: tacked-on → intertwined via architecture deepening; intertwined → tacked-on via category collapse / host-UX changes / workflow-bypass.

**Composes with**:
- [intertwining (axis 1)](intertwining.md) — tacked-on AI is the failure mode for this axis
- [intertwined AI](intertwined-ai.md) — positive mode contrasted
- [co-worker](co-worker.md) — the relational frame tacked-on AI fails to realize
- [category collapse](category-collapse.md) — the risk that produces tacked-on regardless of architectural intent (host environment forces tacked-on shape per VISION line 150)
- [workflow](workflow.md) — tacked-on AI exists outside the workflow (workflow continues unchanged); intertwined exists within
- [practitioner](practitioner.md) — the human side that operates without AI co-worker participation in the tacked-on mode
- [substrate](substrate.md) (Instance aspect) — the runtime, in tacked-on mode, doesn't share workflow state architecturally

**Source**:
- VISION (`VISION.md`) lines 37, 43, 53, 60, 90 (falsification), 150 (category-collapse connection), 205, 225 (axis-1 check)
- Locked GLOSSARY entries: [intertwining (axis 1)](intertwining.md); [intertwined AI](intertwined-ai.md)

**See**:
- [intertwining (axis 1)](intertwining.md) (the axis tacked-on fails)
- [intertwined AI](intertwined-ai.md) (positive contrast)
- [co-worker](co-worker.md) (relational frame failed)
- [category collapse](category-collapse.md) (the force that produces tacked-on regardless of intent)
- ARCH Layer 3 axis-1-mechanism topic (placeholder until Phase 3)
