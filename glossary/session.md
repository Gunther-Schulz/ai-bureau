---
entry: session
class: PRIMITIVE
layer: cross-cutting
axis: cross-axis
vision_usage: implicit
---

# session

- **Class**: PRIMITIVE (atomic; the bounded-interaction unit)
- **Layer**: cross-cutting (sessions exist within workspaces; managed by substrate; not framework-mechanism, not shape-policy)
- **Axis**: cross-axis (sessions span all three axes — interactions can be sparring + audit-emitting + authorship-bearing)
- **VISION usage**: implicit (VISION's "persistent state across sessions" — the cross-session-persistence claim is part of axis-1 architectural support)

**Canonical**: A bounded interaction unit within a workspace — typically one human-AI exchange or work-session. Substrate manages session lifecycle (start/end, context boundaries); state persists ACROSS sessions (per axis-1 architectural mechanism); events fire WITHIN sessions (per `event` entry). A workspace contains many sessions over its lifetime.

**What it is**: The unit at which interactions happen. When you sit down to work with PBS, that work happens within a session: substrate manages the session boundary (when it starts, when it ends, what context is active); within the session, skills fire, events emit, decisions get made. The next session inherits persistent state from prior sessions (e.g., project state, decisions, baustein memory). Sessions are bounded; persistence is cross-session.

**What it is NOT**:
- Not a `workspace` — workspace contains many sessions over time; workspace is the deployment-instance, session is one bounded interaction within it
- Not a `workflow` — workflow is the pattern of work in a domain (sequence of activities); session is one execution-unit during which workflow steps may be progressed
- Not a single `event` — events fire WITHIN sessions; session is the bounded container, event is the atomic emission unit
- Not the `substrate` — substrate manages sessions (session lifecycle is a substrate primitive); session is one runtime artifact

**Cross-archetype illustration**:
- Practitioner-shape: a planning bureau session = drafting Begründung interaction (1+ hours of human-AI co-work); legal practice session = brief-drafting + research interaction
- Autonomous-business-shape: a session may be an operator approval review or an AI-org task-batch
- All shapes: substrate manages the bounded interaction; persistence happens across boundaries

**Boundary test**: Three questions:
1. Is this a bounded interaction with start/end + context boundaries? → it's a session
2. Is this the deployment-instance container that holds many sessions? → it's a `workspace`
3. Is this the pattern of work that sessions execute parts of? → it's a `workflow`

**Composes with**:
- [workspace](workspace.md) — workspaces contain many sessions over their lifetime
- [substrate](substrate.md) — substrate manages session lifecycle (start/end, context, persistence handoff)
- [event](event.md) — events fire within sessions; session bounds emission timing
- [actor](actor.md) — actors operate within sessions
- [workflow](workflow.md) — sessions execute parts of broader workflow_instance executions (one workflow_instance can span many sessions); workflow_instance state persists across session boundaries via persistent-state mechanism. Sessions outside workflow_instance context (ad-hoc work) carry session + work-unit + skill firings without workflow primitive engagement.

**Source**:
- VISION (`VISION.md`) implicit reference: persistent-state-across-sessions is part of axis-1 architectural support
- [substrate](substrate.md) GLOSSARY entry: substrate's Protocol surface includes session/context primitives
- [workspace](workspace.md) GLOSSARY entry: "interaction units occur within a workspace"
- [event](event.md) GLOSSARY entry: events fire within sessions (implicit; events have timestamps tying them to session timeline)

**See**:
- [workspace](workspace.md) (which contains sessions)
- [substrate](substrate.md) (which manages session lifecycle)
- [event](event.md) (which fires within sessions)
- ARCH Layer 3 session-detail topics (placeholder until Phase 3 — session boundary semantics, context-handoff rules, persistent-state migration across sessions; archived material to consult: `substrate-protocol-design.md` for session/context API)
