# Scope + targets

Which subsystems get reviewed, and what files belong to each.

---

## Load-bearing first-run targets

For full first-principles review, default scope is the **7
foundations** below. These are the subsystems from which
everything else inherits shape. Wrong-shape there ripples through
the system; wrong-shape in a leaf is local.

Reviewing these covers the maximum-leverage anti-bias review with
bounded scope. Other subsystems get focused-mode reviews when
reached in workflow phases.

### Target 1 — Architecture meta-rules

**Files**: `ARCHITECTURE.md` (whole file), specifically the 4
meta-rule sections + the named layering convention.

**Greenfield questions for the agent's reasoning**:

- If we were starting today, what placement rules would we want
  for "where does new content belong"?
- Are 4 meta-rules + 1 named convention the right count? Could it
  be 3? 6?
- Are these the right axes (app vs office; memory vs RAG; source-
  of-truth & invalidation; execution determinism; scope-orthogonality
  layering convention)? Greenfield might cut a different decomposition.
- Each meta-rule: is this a fundamental axis, or a derived
  consequence of another rule?

### Target 2 — Entity types + decision rules

**Files**: `ARCHITECTURE.md` § "The 5 entity types" + § "The
decision rules".

**Greenfield questions**:

- If decomposing the system into entity types from scratch, would
  we still get 5 (Skill Bundle, Memory, Backend, Configuration,
  External Data)?
- Are the boundaries between the 5 types clean, or do they blur
  at the edges?
- Are 3 audience-first decision rules the right scaffolding? Could
  placement decisions be made simpler / clearer?
- Are any entity types accumulating "miscellaneous" content — a
  smell that the decomposition is wrong?

### Target 3 — Orchestrator skill

**Files**: `plugin/skills/orchestrator/SKILL.md` +
`plugin/skills/orchestrator/PROCEDURE.md`. Sample 2-3 specialist
skills' bodies for how they interact with orchestrator.

**Greenfield questions**:

- If designing the routing layer from scratch, what would it look
  like? (Single skill orchestrating? Multiple coordinators?
  Capability-based routing?)
- Does the orchestrator do too much (routing + watch lists +
  binding + setup-gate + send-gate)? Should some of this split?
- Are checkpoints (4.2, 4.3, 6.2, 6.4, 11, 12) the right
  granularity? Too few? Too many?
- The "loaded means active, never bypass" rule — is it the right
  framing, or could orchestrator be more flexibly invoked?

### Target 4 — Skill frontmatter contract

**Files**: `docs/plugin-conventions.md` § 1-3 + sample 5 SKILL.md
files (orchestrator + a drafter + a validator + a baustein-related
+ a meta-skill).

**Greenfield questions**:

- If designing the skill spec from scratch, what frontmatter
  would we require? (Currently: name, description, version,
  license, mcp_tools_required, _optional, fallback)
- Is meta-rule 4's `mcp_tools_required[]` declaration the right
  abstraction, or could deps be expressed differently?
- Should skills declare their *capabilities* (per the
  integration-registry design) directly in frontmatter? Or
  separately?
- Description-as-trigger-routing (Claude Code reads the
  description for auto-routing) — is this the right mechanism, or
  a workaround for the lack of explicit triggers?

### Target 5 — Office-config schema

**Files**: `docs/office-config.schema.yaml` + `setup-office`
SKILL.md + `setup-office/references/wizard-flow.md`.

**Greenfield questions**:

- Schema v2 emerged from a v1→v2 migration. If designing fresh
  today, would we still arrive at the same shape?
- Are the 5 integration classes (email/calendar/scanner/phone/
  accounting) the right set? Why these 5 and not fewer/more?
- Is "scope = (domains, states)" the right axis decomposition for
  per-deployment configuration? Greenfield might propose
  capability-based scope or different axes.
- The `extensions.{references,doctypes}_manifests` map shape —
  too verbose? Could it be derived from scope automatically?

### Target 6 — Decision rules + maintenance discipline

**Files**: `ARCHITECTURE.md` § "The decision rules" + §
"Maintenance discipline" + the conventions-doc back-refs.

**Greenfield questions**:

- The 3 decision rules form a placement scaffold. Are they the
  right 3? Could placement be simpler / more deterministic?
- Are the conventions docs (plugin-conventions, backend-
  conventions) at the right level of abstraction? Greenfield
  might fold them into ARCHITECTURE or split further.
- The audit + design-review pair — is the boundary between them
  clean? Greenfield might propose a unified review framework or
  push them further apart.

### Target 7 — LLM/Python boundary (placement-soundness)

**Files**: `ARCHITECTURE.md` meta-rule 4 (whole subsection
including refinements A + B) + 4-5 representative artifacts on
each side of the boundary:

- skill side: orchestrator/PROCEDURE.md, save-baustein/SKILL.md,
  validate-checklist/SKILL.md, draft-textteil-b/SKILL.md
- Python side: `pbs_mcp/tools/discovery.py`,
  `pbs_mcp/office_config.py`,
  `pbs_mcp/chunkers/__init__.py` (when populated),
  `pbs_mcp/integrations/__init__.py`

**Greenfield questions**:

- If designing the LLM/Python placement from scratch, would each
  current operation land where it currently does? Walk 5-8
  concrete operations (validate frontmatter, dedup bausteine,
  pick a baustein for a draft, route a trigger to a skill,
  forward-migrate office-config) and ask the byte-for-byte test
  freshly for each.
- Is meta-rule 4 the right *primary* axis (deterministic vs
  interpretive)? Or is the deeper axis something else —
  *contract-bearing vs free-form*? *Repeatable vs one-shot*?
  Greenfield might propose a different cut.
- The persistence-layer refinement (A) draws the line at *typed
  contract*. Is that the right operationalization, or could it
  be sharper (e.g., "Pydantic-validated" vs "loader-owned")?
- The reuse-direction rule (B) puts shared interpretive logic in
  Skill Bundle references. Is the Skill Bundle the right
  abstraction, or should there be a top-level shared-references
  tier (cross-skill, not skill-internal)?
- The pbs_core / pbs_mcp split is described as "consequence of
  meta-rule 4." Is that consequence load-bearing now, or
  premature? Should it be deferred until the second consumer
  emerges?
- The "static path-based access control belongs in settings.json"
  line — is this on the LLM/Python boundary, or is it a
  *different* axis (harness vs application code) that's been
  smuggled into meta-rule 4? Greenfield might split it out.

This target is **placement-soundness**, not declaration-correctness.
Audit slice 14 catches mechanical violations of the rule as it
stands; this target asks whether the rule itself is the right
shape.

---

## Focused-mode targets

For "design review the chunkers" / "is X sound" / etc., review one
subsystem at a time. Below are the documented file scopes for the
most likely focused requests.

### Chunkers

**Files**: `backend/mcp-server/src/pbs_mcp/chunkers/*.py` +
`backend/mcp-server/docs/chunking-strategy.md`.

### Backend tools

**Files**: `backend/mcp-server/src/pbs_mcp/server.py` +
`backend/mcp-server/src/pbs_mcp/tools/*.py` +
`backend/mcp-server/src/pbs_mcp/schemas.py`.

### Memory layout

**Files**: `memory/universal/**/*.md` + `memory/bausteine/README.md`
+ `plugin/skills/save-baustein/references/format.md` +
`plugin/skills/record-feedback/references/format.md`.

### Layered manifests

**Files**: `extensions/{universal,domain,state}/**/*.yaml` +
`plugin/skills/research-references/references/manifest-schema.md`
+ `plugin/skills/author-manifest/SKILL.md`.

### Integration adapters

**Files**: `backend/mcp-server/src/pbs_mcp/integrations/**/*.py` +
ARCHITECTURE.md § meta-rule 3 (integration adapter pattern).

### Layered template stack

**Files**: `plugin/templates/office-style/*.sty` +
`plugin/skills/validate-latex-style/SKILL.md` +
`memory/universal/style/style-spec.md`.

### Scope orthogonality

**Files**: ARCHITECTURE.md § meta-rule 3 + sample
`extensions/{domain,state}/...` content + `office-config.yaml`
schema + `plugin/skills/save-baustein/references/format.md` (where
scope_key surfaces).

---

## Out-of-scope finding handling

If a subagent's review on subsystem X surfaces a reshape that
*requires* reviewing subsystem Y to assess properly:

- **Don't expand current scope** — that's how reviews drift into
  fatigue
- **Log as follow-up review** in the artifact: "Reviewing X
  surfaced a reshape candidate that ripples to Y; recommend a
  follow-up focused-mode design-review on Y."
- The user decides whether to dispatch the follow-up

Same anti-fatigue pattern as audit's targeted-slice rule.

---

## What's NOT included by default

The full first-run does **NOT** include:

- Individual specialist skills (drafters, validators, baustein-related)
- Plugin scaffolding (CLAUDE.md, plugin.json)
- READMEs at any level
- Memory reference content (style-spec, korrektur-rules, etc.)

These get focused-mode reviews when they become load-bearing for
the next phase. E.g., before Phase 2a (text-side ingestion),
design-review the chunkers + memory layout. Before Phase 4 (first
project bind), design-review the project-state schema + survey-
project skill.

This is the **A-but-scoped** policy: load-bearing first; leaves
when reached. Preserves the unique pre-launch radical-rewrite
freedom for foundations while not consuming session budget on
leaf-level review until those leaves matter.
