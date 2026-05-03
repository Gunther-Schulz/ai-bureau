---
entry: skill
class: PRIMITIVE
layer: cross-cutting
axis: cross-axis
vision_usage: implicit
---

# skill

- **Class**: PRIMITIVE (atomic; the work-logic unit) — single-aspect (no multi-scope manifestation)
- **Layer**: cross-cutting (skill is an application-level work-logic unit that lives within specialists; manifests at whatever scope the containing specialist manifests at)
- **Axis**: cross-axis (skills serve any axis depending on what work they encode)
- **VISION usage**: implicit (VISION line 7 says "codified expertise bundled as specialists"; skills are the atomic units of that expertise; not directly defined as glossary term in VISION)

**Canonical**: An atomic unit of work logic within a specialist — a behavioral procedure invoked when its trigger conditions match (loading semantics — auto-load, explicit-load, lazy-load — are substrate-defined per Pattern A; `auto-loaded` is the convention in Anthropic-plugin-substrate but not architecturally mandated). Skills are the smallest composable unit of codified expertise; specialists bundle multiple skills (+ entities + memory + adapters) into a distributable expertise package. (Note: deliberately NOT "behavioral protocol" — `protocol` is locked architectural vocabulary for Pattern A pluggable subsystems.)

**What it is**: A skill is what you'd reach for when you want to express "do this specific kind of work when this condition is met." Skills have triggers (when they fire), body content (what they instruct), and may declare output schemas (Pydantic models for structured output). Multiple skills compose into a specialist; the specialist is the cohesion abstraction; the skill is the atomic unit.

**What it is NOT**:
- Not a `specialist` — specialist is the bundle; skills are units within it
- Not a `workspace` — workspace activates specialists (which contain skills); workspace doesn't activate skills directly
- Not a `mechanism` — skills are application-level work logic, not framework-level interface contracts
- Not a sparring sub-mechanism — those are specific axis-2 capabilities (counter-argument, confidence calibration, etc.); skills are general-purpose work units that may USE sparring mechanisms
- Not a `workflow` — workflow is the broader pattern of work; skills are atomic actions within workflows

**Cross-archetype illustration** (named examples; archived plugin/skills/ catalog):
- **orchestrator** — coordinates session-open + decision routing + state management (PBS-Schulz)
- **save-baustein** — saves reusable text patterns to memory (PBS-Schulz; cross-archetype)
- **draft-textteil-b** — drafts B-Plan-Begründung text (planning-domain; PBS-Schulz)
- **validate-checklist** — validates work against doctype checklists (cross-archetype)
- **citation-verification** — checks legal/scholarly citations (cross-archetype)
- **review-draft** — runs layered review with sparring mechanisms (cross-archetype)

A specialist activates a coherent set of skills; e.g., `planning-document-work` specialist bundles `orchestrator + save-baustein + draft-textteil-b + review-draft + validate-checklist + research-references + verify-citations + ...`.

**Boundary test**: Three questions:
1. Is this an atomic unit of work logic that fires on a trigger? → it's a skill
2. Is this codified expertise BUNDLED as a distributable unit? → it's a `specialist` (containing skills)
3. Is this a framework-level interface contract? → it's a `mechanism`, not a skill

**Composes with**:
- [specialist](specialist.md) — specialist contains skills as its atomic work-logic units; skill cannot be used outside specialist context — a specialist provides the skill's runtime context, dependencies, references. Skill names scoped under specialist-namespace = specialist-name (per `glossary/specialist.md` composes-with skill row); fully-qualified skill reference is `specialist-name:skill-name`; cross-specialist skill invocation uses fully-qualified reference (specialist-A's skill can invoke specialist-B's skill via `specialist-B:skill-name`). **Note**: the specialist-as-skill-bundle constraint is a PBS architectural commitment (per archived `terminology-and-specialist-primitive.md`); differs from Anthropic's bare-skill plugin convention where skills can exist standalone in `plugin/skills/`. Phase 6 reconciles which convention applies to PBS app-skill rebuild.
- [mechanism](mechanism.md) — skills use framework mechanisms (audit emission, source-grounding, sparring) at runtime via the substrate
- [workflow](workflow.md) — skills participate in broader workflows (sequence of skill firings + decisions)
- [actor](actor.md) — skills emit AuditEvents via the AI runtime that fires them (`actor_kind: ai_runtime`); the enum value is deliberately NOT `skill` to avoid naming collision with this primitive
- [adapter](adapter.md) — skills invoke adapters at runtime to interact with external systems (e.g., draft-cover-mail invokes email-adapter; verify-citations invokes MCP-corpus-adapter); the adapter is the integration boundary, the skill is the work-logic unit firing it
- [authority-binding](authority-binding.md) — skill emissions record `actor_kind: ai_runtime` + skill identifier per authority-binding mechanism Surface (per `glossary/authority-binding.md` per-event actor declaration); chain of attribution composes into per-claim defensibility (the enum value is `ai_runtime` not `skill` to avoid naming collision per [actor](actor.md))

**Source**:
- VISION (`VISION.md`) line 7 (thesis): "codified expertise bundled as specialists" — skills implicit as the atomic units of expertise
- Locked GLOSSARY entry [specialist](specialist.md): "skills are atomic work logic units within a specialist; specialist is the bundle that contains skills"
- Inherited from Anthropic plugin convention: skills as auto-loaded behavioral protocols with trigger frontmatter

**See**:
- [specialist](specialist.md) (which contains skills)
- ARCH Layer 3 skill-detail topics (placeholder until Phase 3 — skill granularity 3-test, frontmatter schema, output validation; archived material to consult: `skill-expert-agent-and-domain-knowledge.md`, `terminology-and-specialist-primitive.md` for `specialist:` frontmatter requirement)
