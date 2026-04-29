# Scope + targets

Which subsystems get reviewed, and what files belong to each.

---

## Load-bearing first-run targets

For full first-principles review, default scope is the **6
foundations** below. These are the subsystems from which
everything else inherits shape. Wrong-shape there ripples through
the system; wrong-shape in a leaf is local.

Reviewing these covers the maximum-leverage anti-bias review with
bounded scope. Other subsystems get focused-mode reviews when
reached in workflow phases.

### Target 1 — Architecture meta-rules

**Files**: `ARCHITECTURE.md` (whole file), specifically the 5
meta-rule sections.

**Greenfield questions for the agent's reasoning**:

- If we were starting today, what placement rules would we want
  for "where does new content belong"?
- Are 5 meta-rules the right count? Could it be 3? 7?
- Are these the right 5 axes (app vs office; scope orthogonality;
  integration adapters; memory vs RAG; execution locality)?
  Greenfield might cut a different decomposition.
- Each meta-rule: is this a fundamental axis, or a derived
  consequence of another rule?

### Target 2 — Entity types + decision rules

**Files**: `ARCHITECTURE.md` § "The nine entity types" + § "The
decision rules".

**Greenfield questions**:

- If decomposing the system into entity types from scratch, would
  we still get 9?
- Are the boundaries between A/B/C/D/E/F/G/H/I clean, or do they
  blur at the edges?
- Are 6 decision rules the right scaffolding? Could placement
  decisions be made simpler / clearer?
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
- Is meta-rule 5's `mcp_tools_required[]` declaration the right
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

- The 6 decision rules form a placement scaffold. Are they the
  right 6? Could placement be simpler / more deterministic?
- Are the conventions docs (plugin-conventions, backend-
  conventions) at the right level of abstraction? Greenfield
  might fold them into ARCHITECTURE or split further.
- The audit + design-review pair — is the boundary between them
  clean? Greenfield might propose a unified review framework or
  push them further apart.

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
