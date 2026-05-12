# D19 — 2026-05-08 — Specialist kind

**Decision**: The specialist kind specifies a packaged role/skill bundle loaded into a workspace. Specialists declare what they do (skills) and where they fit (supported work-unit-kinds); their content is loaded into the substrate's `skills` capability per D17.

### Contract slots

- **`id`** — stable identifier (e.g., `planning-document-work`).
- **`version`** — version designator (range-comparable; semver-shaped at layer-3 formal schema).
- **`roles[]`** — required-with-explicit-empty: shape-role-tags this specialist operates in (per D13's role vocabulary).
- **`skills[]`** — required-with-explicit-empty: operations the specialist provides. Semantic declarations only; formal interface and content (SKILL.md or equivalent) = layer 3 / specialist-impl.
- **`supported-work-unit-kinds[]`** — required-with-explicit-empty: which work-unit-kinds this specialist is appropriate for.
- **`required-adapter-bindings[]`** — required-with-explicit-empty: adapter kinds the specialist needs bound in the workspace.
- **`required-substrate-capabilities[]`** — required-with-explicit-empty: typically just `skills`; possibly more (e.g., `event-streaming` if specialist subscribes to events).
- **`declared-event-emissions[]`** — required-with-explicit-empty: events the specialist produces (parallel to adapter D16).
- **`declared-event-subscriptions[]`** — required-with-explicit-empty: events the specialist reacts to (parallel to adapter's `consumptions`, but specialist-flavored — specialists react via skill invocation; adapters react via external interaction).
- **`activation-scope`** *(optional)* — when present, declares scope conditions under which the specialist is active (e.g., "scope.domain matches X"). When absent, specialist is always-active when bound. Detail = layer-3 formal schema.

### Skills vs supported-work-unit-kinds (clarification)

These are **orthogonal** declarations:
- `skills[]` = what the specialist does (verbs / operations).
- `supported-work-unit-kinds[]` = where the specialist fits (work-types / nouns).

Many-to-many at the domain level: one skill may serve multiple work-unit-kinds; one work-unit-kind may use multiple skills from a specialist. Framework does **not** cross-validate the two — that's a domain concern. Framework uses `skills` for substrate-level loading; uses `supported-work-unit-kinds` for routing + validation (workspace expecting work of kind X must have at least one specialist supporting X).

### Cross-specialist coordination

**Event-driven** (preferred at framework level): specialists subscribe to other specialists' / adapters' / shape's emissions and react via their skills. RPC-style direct invocation between specialists is implementation-shape — specialists CAN reference each other, but the framework doesn't validate or guarantee the semantics.

### Sub-agent relationship

Sub-agents are not a separate kind. A sub-agent spawned by a specialist's skill is an `agent-actor` (per D9) registered via a `composition-change` event (per D10). The specialist provides the skill that triggers spawn; the framework tracks the sub-agent as an actor; cross-process / cross-vendor sub-agents flow via A2A peer adapters (per D16).

### Concrete example (illustrative; not part of core)

`planning-document-work` specialist with roles `[drafter, reviewer]`, skills `[draft-section, review-section, cite-regulation]`, supported-work-unit-kinds `[b-plan-section, b-plan-festsetzung, umweltbericht-section]`, required-adapter-bindings `[bauleitplanung-corpus, latex-compile]`, required-substrate-capabilities `[skills]`. Worked through in discussion that produced this decision.

### What is NOT in the specialist kind contract

- **Specific skill semantics / content** (SKILL.md bodies; what `draft-section` actually does) — extension-content / specialist-impl.
- **Per-skill adapter mapping** (which skill uses which adapter) — specialist-internal documentation.
- **RPC-style cross-specialist invocation semantics** — implementation; not framework-validated.
- **Specialist runtime lifecycle internals** (initialization, hot-reload, etc.) — implementation.
- **Sub-agent spawn mechanics** — substrate concern; framework only sees the resulting actor + events.

**Rationale**: per I1, specialist is a composable internal capability bundle (paralleling adapter as composable external interface); per I2, declared slots give framework structural basis to validate workspace composition (does any specialist support work-unit-kind X? are required adapters bound? are required substrate capabilities provided?); per I3, declared event emissions / subscriptions let specialist's contributions integrate into the workspace event chain with proper attribution.
