---
entry: workflow
class: PRIMITIVE
layer: multi-aspect
axis: axis-1
vision_usage: directly-used
---

# workflow

- **Class**: PRIMITIVE (atomic; the work-pattern unit) — **bipartite multi-aspect Pattern B** (DEFINITION in specialist's distributable bundle; INSTANCE-CONTENT at Owner B as workflow_instance entity). Optional structural overlay: workflow_instance engages only when work follows a codified pattern; ad-hoc work outside workflow primitive scope.
- **Layer**: multi-aspect — DEFINITION aspect inherits Framework C placement via specialist's bundle (specialists DEFINE workflow patterns; not standalone Framework C entries); INSTANCE aspect at Owner B (workflow_instance per workspace per work-unit when codified pattern applies)
- **Axis**: axis-1 (primary anchor — workflow is what intertwined AI intertwines WITH); cross-axis (workflows span all axes during execution)
- **VISION usage**: directly used (`VISION.md` thesis line 7: "interactive practitioner workflows"; line 27 axis 1: "AI is a co-worker in the workflow itself"; "Workflow as precondition" implication retained in current VISION)

**Vocabulary disambiguation**:
- **`workflow`** — the primitive (the abstraction; bipartite Pattern B)
- **`workflow definition`** — the DEFINITION aspect (reusable pattern in a specialist's bundle)
- **`workflow_instance`** — the INSTANCE aspect (specific run-through; entity-md per Owner B convention)

When unambiguous from context, just "workflow" works. When ambiguous, qualify.

**Canonical**: A pattern of work in a domain — sequence of activities, artifacts, decisions, and handoffs that defines how a practitioner produces accountability-bearing output. Per VISION axis 1: workflow is what intertwined AI intertwines WITH. The primitive is bipartite: a `workflow definition` is the reusable pattern (specialist-bundled); a `workflow_instance` is a specific execution against a work-unit (Owner B). The primitive engages OPTIONALLY — only when work follows a codified pattern; ad-hoc work without codified pattern engages session + work-unit + skill + claim + event WITHOUT workflow.

**What it is**: A domain-specific structure of work. Workflow definitions are pattern-level concepts: "how does B-Plan-Begründung drafting actually proceed?" or "how does a legal brief get from intake to filing?" They include activities (drafting, reviewing, sending), artifacts (Begründung, Stellungnahme, signed brief), decisions (which argumentation type, which authorities to address), and handoffs (between sessions, between humans, between AI and human). When a practitioner begins work that maps to a codified definition, a `workflow_instance` is created — it carries state, phase, work-unit attribution, audit-trail context across the run-through. Workflow_instance can span multiple sessions; specialists provide the skills that progress phases; the architecture's intertwining requirements (persistent state, orchestration, audit, etc.) are what allow AI to participate as co-worker rather than as discrete-feature-tool.

**Optional applicability**: Not all work engages the workflow primitive. Practitioner-driven ad-hoc work (start with task in mind; use deployment capabilities; produce artifact) is a legitimate first-class case. Ad-hoc work-units have NO workflow_instance — they're carried by session(s) + work-unit + skill firings + claim emissions + events alone. Workflow primitive engagement is opt-in via codified pattern existence.

Reciprocal to `work-unit`'s always-present anchor: work-unit is the always-present container (every accountability-bearing piece of work IS a work-unit); workflow_instance is the optional structural overlay attached to it when codified pattern applies. The asymmetry is load-bearing — ad-hoc work is first-class supported via the always-present work-unit primitive without forcing workflow primitive engagement.

**Evolution path (ad-hoc → codified)**: A practitioner doing ad-hoc work repeatedly may notice patterns. When pattern crystallizes, it can be abstracted into a workflow definition + added to a specialist's bundle. Future similar work then follows the codified pattern (workflow_instance engages). This evolution is part of the framework's value proposition — capacity-building manifests partly through practitioner expertise crystallizing into reusable codified patterns.

**Cardinality + lifecycle**:

**workflow definition** cardinality: N per specialist (each specialist DEFINITION declares the workflow patterns it supports). Per workspace = sum across active specialists.
**workflow definition** lifecycle: immutable per specialist version (specialist version bump may include workflow definition changes); distributed via specialist's Framework C placement.

**workflow_instance** cardinality: N per workspace per active specialist (instances created per work-unit when codified pattern applies; absent for ad-hoc work-units).
**workflow_instance** lifecycle: created at workflow-start with snapshot of definition (preserves defensibility — execution reproducible per original definition); transitions through phases via state machine (per ARCH Layer 3 schema); terminal states completed / abandoned / failed; non-terminal pause state suspended; mutable-with-audit (state transitions, phase changes, artifact accumulation all audited); persists across sessions via persistent-state mechanism; retains for audit per workspace's audit-retention policy.

**What it is NOT**:
- Not a `session` — session is one bounded interaction; workflow_instance can span many sessions
- Not a `skill` — skill is atomic work logic that fires on a trigger; workflow_instance is the broader execution context within which skills fire
- Not a `specialist` — specialist bundles skills + entities + workflow definitions; workflow is one of several primitives composed into specialist's bundle
- Not a `workspace` — workspace is the deployment container; workflow_instance is at Owner B within the workspace
- Not required for all work — ad-hoc work engages session + work-unit + skill + claim + event WITHOUT workflow_instance; workflow primitive is OPTIONAL structural overlay
- Not constraint on capability addition — practitioner adding adapters / activating new specialists / configuring new skills mid-flight is workspace-scope (orthogonal to workflow_instance state); workflow_instance doesn't gate capability changes

**Cross-archetype illustration**: workflows differ per archetype (the discriminator is what kind of accountability-bearing output gets produced and how):
- Planning bureau: B-Plan-Begründung drafting workflow (intake → research → draft → review → send → response handling)
- Legal practice: matter workflow (intake → research → drafting → filing → response cycle)
- Research lab: manuscript workflow (research → drafting → peer review → revision → submission)
- Auditor: audit engagement workflow (planning → fieldwork → finding → report)

In each archetype, the practitioner ALSO does ad-hoc work outside these codified workflows (research notes, exploratory analysis, one-off communications) — those run as session + work-unit + skill + claim without workflow_instance.

Per VISION's "Workflow as precondition" implication: domains with rich, structured workflows are natural fits for axis-1 intertwining. Generic "knowledge work" without explicit workflow is much harder — but ad-hoc work is still framework-supported via the optional-overlay design.

**Boundary test**: Three questions:
1. Is this a domain-specific pattern of work (sequence + artifacts + decisions + handoffs)? → it's a `workflow definition`
2. Is this a specific run-through of a codified pattern? → it's a `workflow_instance`
3. Is this work without a codified pattern? → ad-hoc; engages session + work-unit + skill without workflow_instance

**Composes with**:
- [intertwining (axis 1)](intertwining.md) — workflow is what axis-1 AI intertwines WITH; "Workflow as precondition" implication
- [specialist](specialist.md) — specialists' DEFINITIONS contain workflow definitions (workflow inherits Framework C placement via specialist's bundle). Workflow definition names scoped under specialist-namespace = specialist-name (per `glossary/specialist.md` composes-with workflow row); fully-qualified workflow reference is `specialist-name:workflow-name`.
- [session](session.md) — sessions execute parts of workflow_instance executions (one workflow_instance may span many sessions); persistent-state mechanism carries workflow_instance state across session boundaries
- [skill](skill.md) — skills are consumed BY workflow definitions (workflow definition references skills by name; skills fire within workflow phases when triggers match); composition direction: workflow → skill
- [workspace](workspace.md) — workspaces SUPPORT workflow_instances at Owner B (workspace's deployed specialists provide workflow definitions; workspace state enables workflow_instance persistence)
- [work-unit](work-unit.md) — workflow_instance attaches to work-unit instance when codified pattern applies. Cardinality asymmetry: workflow_instance has 1 work-unit attribution; work-unit has N workflow_instances attached (potentially across specialists). Work-unit is always-present anchor (Pattern B primitive); workflow_instance is optional overlay (Pattern B primitive with optional applicability). Two Pattern B primitives composing cleanly.
- [claim](claim.md) — claims emitted during workflow_instance execution attribute to that workflow_instance; per-claim audit composes into workflow audit context
- [event](event.md) — workflow_instance emits lifecycle events (workflow_started, phase_transitioned, workflow_completed, suspended, abandoned, failed); audit-emission mechanism captures these
- [authority-binding](authority-binding.md) — workflow_instance phase transitions may require specific authority (workflow definition declares per-phase authority requirements); per-shape policy declares trust model parameterizing authority-binding satisfaction
- [mechanism](mechanism.md) — composes with multiple framework-level mechanisms: persistent state (workflow_instance state across sessions); audit emission (lifecycle events); authority binding (phase transitions may require specific authority; workflow definition declares per-phase authority requirements)
- [category collapse](category-collapse.md) / [quality-gate](quality-gate.md) — quality-gate ARCH topic LOCKED Phase 3.6 per [arch/quality-gate.md](../arch/quality-gate.md); workflow_instance execution is observability source for quality-gate's drift detection (e.g., practitioner approving phase transitions without engaging review content → axis-3 rubber-stamping signal); checkpoint_kind `workflow_phase_transition` event-triggered per `arch/quality-gate.md` §2 capability category A
- [engaged authorship](engaged-authorship.md) — engagement events fire at workflow phases when codified workflow exists (drafting → review → signing); workflow's optional-overlay applicability is orthogonal to engaged-authorship's mandatory always-present status (engagement events fire per claim regardless of workflow_instance)

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "interactive practitioner workflows"
  - Line 27 (axis 1): "AI is a co-worker in the workflow itself, not a feature bolted onto an unchanged human workflow"
  - "Workflow as precondition" implication subsection retained in tightened VISION
- [intertwining (axis 1)](intertwining.md) GLOSSARY entry: "workflow — what intertwining intertwines WITH (axis 1 needs a workflow to intertwine with)"
- [session](session.md) GLOSSARY entry: "sessions execute parts of broader workflows"
- [specialist](specialist.md) GLOSSARY entry: specialist's DEFINITION includes workflow definitions
- Synthesis: bipartite Pattern B classification with optional-overlay applicability resolves the single-aspect-vs-bipartite hedge; ad-hoc work is first-class (carried by session + work-unit + skill + claim + event without workflow primitive engagement)

**See**:
- [intertwining (axis 1)](intertwining.md) (which intertwines with workflow)
- [specialist](specialist.md) (which contains workflow definitions in its bundle)
- [session](session.md) (which executes parts of workflow_instance)
- [work-unit](work-unit.md) (the deployment-bound artifact workflow_instance attaches to)
- [claim](claim.md) (claims attribute to workflow_instance during execution)
- `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster ARCH topic; two-Pattern-B topic-template-class anchor; bipartite Pattern B with optional applicability — workflow DEFINITION at Framework C via specialist's bundle + workflow_instance at Owner B; workflow_instance 5-state lifecycle (`running` | `suspended` | `completed` | `abandoned` | `failed`); definition-snapshot pattern preserving defensibility; cardinality asymmetry vs work-unit (1 work-unit per workflow_instance; N workflow_instances per work-unit); per-shape policy variation matrix; authority-binding composition for phase transitions; cross-axis composition with axis-1 PRIMARY anchor; W1-W4 watch-list)
- Cross-specialist shared workflow patterns: resolved via mental modeling (D gate) — shared patterns live as Layer A reusable templates / specialist-bundled bausteine (content, not framework primitive). If specialists develop genuinely-cross-archetype pattern not yet in Layer A, extend Layer A content. Watch-list signal: if Layer A growth proves insufficient for a pattern that's structurally cross-cutting (not just content-shaped), examine then; not a framework primitive by default.
- [quality-gate](quality-gate.md) (Pattern A runtime protocol that composes with workflow_instance observability; per GLOSSARY entry)
