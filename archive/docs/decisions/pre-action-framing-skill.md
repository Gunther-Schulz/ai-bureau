# Decision record: Pre-action framing skill (commitment #8)

**Status**: ACCEPTED (session 11, 2026-04-30; backfill DR for ROADMAP commitment #8 originally scoped session 7)
**Owner**: ROADMAP commitment #8; ARCHITECTURE.md sparring-mode infrastructure; new skill bundle `plugin/skills/frame-task/`
**Related**: `audit-trail-v2.md` (the canonical example case for why framing matters), `sparring-output-v1.md` (framing skill produces a sparring-shaped output), VISION.md axis 2 (sparring partner) + axis 3 (authorship preservation)

## Context

Session 7's `audit-trail` v1 → v2 reversal was the canonical case for why a pre-action framing skill matters: v1 was designed without asking "what does this subsume?" Once design-review target 9 (Subsumption check) was added in session 7, the question became part of design-time discipline — but only at design-review time, not at design-START time.

The current skill ecosystem has three layers:

| Layer | Skills | When fires |
|---|---|---|
| **Implementation** | orchestrator + specialists (drafting, review, validation, etc.) | When work happens |
| **Review** | audit, design-review | After work (drift, soundness checks) |
| **MISSING — Preparation** | (no skill) | Before non-trivial work begins |

The gap: today we informally discuss before acting (in-conversation), but no skill structurally surfaces the right preparation questions. Result: design errors that compound after launch (the v1 audit-trail case generalizes).

This DR backfills the architectural rationale for commitment #8.

## Decisions

### 1. Skill identity + name

**Decision**: new skill bundle `plugin/skills/frame-task/` with skill name `frame-task`. Short, generic, deployment-portable.

Alternative considered: `scoping`, `pre-flight`, `task-framing`. Rejected: `frame-task` reads as imperative ("frame the task") which matches the discipline's intent.

### 2. Skill type — interactive-sparring body type

**Decision**: `frame-task` is **skill-only** (per `skill-expert-agent-and-domain-knowledge.md` decision 3). Body type = `interactive-sparring`. Not agent-mode-eligible.

**Why**: framing requires sparring (the user must ENGAGE with the framing questions; autonomous framing is meaningless — there's nothing to frame for if no human is initiating work). Per VISION axis 2, sparring requires human in the loop.

### 3. Trigger conditions

**Decision**: orchestrator routes to `frame-task` BEFORE routing to implementation specialists when:

- Task is non-trivial (multi-step; multi-decision; cross-skill coordination required)
- Task is a NEW commitment-shape (architectural decision; new entity type; scope reframe)
- User explicitly invokes (`/frame-task` slash command per #11)

Triggers NOT firing:
- Routine work (single-skill invocation; well-trodden path)
- Conversational continuation of in-flight work (don't re-frame mid-stream)
- Read-only queries (audit, search)

The orchestrator's PROCEDURE.md (post-#11) declares the routing logic. Conservative default: when in doubt, surface "should we frame this first?" rather than auto-routing.

### 4. Output artifact

**Decision**: `frame-task` produces a structured framing artifact per the `FramingOutput` Pydantic schema (per sparring-output structural promotion pattern in `sparring-output-v1.md`):

```python
class FramingOutput(StrictModel):
    """Output shape for frame-task skill (preparation phase)."""
    actual_problem: str = Field(..., min_length=50)
    # Not the user's surface request; the underlying problem.
    # Example: user says "extract these skills"; actual problem
    # is "evaluate which skills are domain-agnostic enough to
    # extract without per-domain refactor."

    in_scope: list[str] = Field(..., min_length=1)
    out_of_scope: list[str] = Field(..., min_length=1)

    approaches_considered: list[Approach] = Field(..., min_length=2)
    # >=2 approaches; the second forces consideration of alternatives.
    # Per anti-bias mechanism in design-review skill.

    chosen_approach: str = Field(..., min_length=20)
    chosen_approach_rationale: str = Field(..., min_length=50)

    constraints: list[Constraint]
    # Non-negotiables: legal / architectural / deadlines / governance.

    success_criteria: list[str] = Field(..., min_length=1)
    # Observable outcome, not "feels done."

    confidence: Literal["high", "medium", "low"]
    confidence_basis: str = Field(..., min_length=20)
    # Per VISION axis 2 confidence calibration.
```

Schema fields chosen to surface the questions session 7's
audit-trail v1 missed:
- **actual_problem** vs surface request — would have caught "we're adding event log" without asking "are existing prose sources subsumed?"
- **approaches_considered (>=2)** — would have surfaced single-write architecture as alternative to dual-write.
- **constraints** — would have surfaced "strict-validation discipline applies."
- **chosen_approach_rationale** — would have triggered explicit defense.

### 5. Composition with existing skills

**Decision**: framing artifact feeds DOWNSTREAM into:

- **Implementation skills** (orchestrator + specialists): consume the framing artifact to anchor work. The artifact's `chosen_approach` shapes the implementation; `constraints` shape what's not changed; `success_criteria` shape verification.
- **Audit skill**: reads framing artifact at audit time as part of context (was the work consistent with its declared scope?).
- **Design-review skill**: reads framing artifact + verifies `approaches_considered` was substantive (target 9 subsumption check fires here).

The framing artifact is a project-level memory entry (per memory taxonomy) — lives at `<project>/_ai/framings/<task-slug>.md` (post-#9 entity-md compatible — frontmatter + body).

### 6. Scope per session

**Decision**: `frame-task` is short-form by design. ~3-5 minutes of conversational framing, not a deep planning exercise. Output artifact is concise (~200-400 words for `actual_problem` + scope + approaches; reasoning chain compact).

If framing surfaces that the task needs deeper analysis (e.g., a major architectural decision warranting its own DR), `frame-task` recommends spawning that DR-write workflow rather than absorbing the depth itself.

### 7. AuditEvent integration

**Decision**: `frame-task` invocations emit AuditEvent
`event_kind=task_framed` with `details: {framing_artifact_path,
trigger_reason, downstream_skills}` per #6 audit-trail v2.

Captures: who framed what + why orchestrator routed to framing
+ what implementation followed. Defensibility — six months later,
"why did we approach this task this way?" reconstructs from
framing artifact + audit chain.

## Composition with existing disciplines

| Discipline | Connection |
|---|---|
| **Sparring axis 2** | Framing IS sparring at the meta level — about the task itself before doing it. `approaches_considered (>=2)` enforces counter-perspective at framing time. |
| **Authorship preservation axis 3** | Framing artifact is signed by user (explicit confirmation before downstream skills consume it). Defensibility chain extends back from output to framing. |
| **Make wrong shapes impossible (v0.21)** | `FramingOutput` schema fields are required (Pydantic-enforced); convention-driven framing is rejected. Skills can't ship without framing for non-trivial tasks if orchestrator routes correctly. |
| **Pattern-vs-instance + sharp defer rule (v0.20)** | `frame-task` is pattern-level (every domain has framing needs). The TRIGGER conditions are deployment-instance (which tasks are non-trivial varies per domain). |
| **Skill-granularity discipline (v0.27)** | `frame-task` passes the 3-test: distinct workflow (preparation interaction, not work itself); distinct output (FramingOutput artifact); reuse across projects (every non-trivial task). Elevation warranted. |

## Defers — re-examined session 15 under v0.33 no-defer principle

> **Session 15 amendment**: re-examined the 4 entries below. Result: D1 (FramingOutput schema field tuning) is a valid watch-list entry — names specific external signal (first 5-10 real framings; refine per empirical signal). D2, D3, D4 are phase routing (D2 → #11 orchestrator PROCEDURE.md reshape; D3 → #11 slash command pattern; D4 → #6 audit-trail v2 retrofit). Per v0.33 preliminary-lock: this DR remains preliminary-locked. Original entries kept below as historical record.

### Original entries (per defer-instinct discipline)

| Defer | Home | Specific cost being avoided |
|---|---|---|
| **D1**: Concrete `FramingOutput` schema field tuning (do `approaches_considered` actually need >=2? Is `confidence` needed?) | First 5-10 real framings; refine per empirical signal | Locking schema before empirical use locks the wrong shape |
| **D2**: Orchestrator's routing-to-frame-task logic refinement | #11 Cowork integration (orchestrator PROCEDURE.md gets reshaped there) | Pre-empting #11 |
| **D3**: Slash command `/frame-task` UX surface | #11 (slash command pattern lands there) | Same as D2 |
| **D4**: `task_framed` AuditEvent kind details schema (additional fields beyond the named ones) | #6 audit-trail v2 retrofit | Bundled with #6's event-kind retrofits |

Each defer names a specific home + chronological-valid cost being avoided.

## Constraints flowing to downstream commitments

### → #6 (audit-trail v2 retrofit)

- **`task_framed` event kind** added to AuditEvent enum.
- **`details: {framing_artifact_path, trigger_reason, downstream_skills}`** payload validation per-kind.

### → #11 (Cowork integration)

- **Orchestrator PROCEDURE.md** adds routing logic: when does orchestrator route to `frame-task` vs directly to implementation specialist?
- **Slash command `/frame-task`** for explicit user invocation.
- **`frame-task` SKILL.md frontmatter** declares `output_schema: FramingOutput` per `sparring-output-v1.md` pattern + `display_label: "Task Framer"` per session-11 skill-expert-agent decision 1.

### → audit + design-review skills

- **Audit slice update**: when scanning an in-flight project for drift, audit reads framing artifacts to compare declared scope vs actual delivery. Surfaces scope-creep + missing-from-scope.
- **Design-review target update** (target 9 subsumption + target 14 discipline-gap): consume framing artifacts as "what alternatives were considered?" + "what discipline applied?" data.

### → entity-md ecosystem (post-#9)

- **Framing artifacts as project-axis entities**: `<project>/_ai/framings/<task-slug>.md` with frontmatter (Layer 1 universal + Layer 2 type=`<dept>.framing`) + body containing the FramingOutput rendered as markdown.

## Pattern-vs-instance check

`frame-task` generalizes cleanly:

| Domain | Framing trigger | Framing artifact |
|---|---|---|
| **Legal practice** | Before drafting a brief; before filing a motion; before deposition strategy | brief-framing / motion-framing / depo-framing artifacts |
| **Research lab** | Before manuscript drafting; before grant submission; before experimental design | manuscript-framing / grant-framing / experimental-framing |
| **Brand voice** | Before campaign concept; before voice spec | campaign-framing / voice-framing |

Same skill shape; deployment-instance content per domain.

## Pioneer-instance check

PBS validates the skill's mechanism on real planning-bureau tasks (drafting Begründungen for new Verfahren types, designing extensions, framing client engagements). The skill SHAPE is pattern-level (FramingOutput schema, trigger conditions, orchestrator integration); the deployment-instance content is what counts as "non-trivial task" per domain.

## Revisit triggers

- **After first 5-10 real framings**: validate FramingOutput schema field shape; adjust if `approaches_considered (>=2)` produces low-quality alternatives, or if `confidence` is consistently uncalibrated.
- **At #11 Cowork integration**: confirm orchestrator routing logic + slash command UX + plugin shape.
- **First framing artifact at second-domain deployment**: validate the schema generalizes (probably yes — all fields are domain-agnostic).
- **Framing-bypass pattern emerges**: if users repeatedly bypass `frame-task` for "small tasks" that turn out to be non-trivial, refine trigger conditions.

## Files touched (when this commitment lands)

- `docs/decisions/pre-action-framing-skill.md` — this file (NEW, backfill)
- `plugin/skills/frame-task/SKILL.md` — new skill bundle
- `plugin/skills/frame-task/PROCEDURE.md` — multi-checkpoint state for the framing flow
- `plugin/skills/frame-task/references/framing-modules.md` — domain-flavored framing question modules
- `backend/mcp-server/src/pbs_mcp/skill_outputs/framing_output.py` — `FramingOutput` Pydantic + min_length validators
- `backend/mcp-server/src/pbs_mcp/audit_trail.py` — `task_framed` EventKind addition
- `plugin/skills/orchestrator/PROCEDURE.md` — routing logic for when to route to `frame-task`
- `docs/plugin-conventions.md` — note about pre-action framing pattern in skill orchestration
- `ROADMAP.md` — commitment #8 marked shipped + cross-ref this DR
