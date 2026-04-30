# Entity-md spec — formatting + terminology reference

**Status**: scaffold authored session 10. Layer 1 + body section
names + formatting conventions complete; Layer 2 per-entity-type
schemas grow in during #9 alongside Pydantic implementation.
**Owner**: ARCHITECTURE.md "AI-as-runtime hybrid-shape principle"
section + `docs/decisions/ai-as-runtime-hybrid-shape.md`.
**Validated by**: design-review target 12 (prospective) + audit
slice 21 (retrospective).

This document is the **single source of truth** for the
implementation-level formatting + terminology of the hybrid-shape
contract. ARCHITECTURE.md holds the principle + discipline; this
doc holds the exact rules.

---

## 1. File layout

Every managed entity is **one md file**. File location:

| Scope | Path pattern |
|---|---|
| Universal | `extensions/universal/<entity-type>/<id>.md` (e.g., `extensions/universal/doctypes/b-plan-begruendung.md`) |
| Domain | `extensions/domain/<domain>/<entity-type>/<id>.md` (e.g., `extensions/domain/Naturschutz/doctypes/saP-hauptpruefung.md`) |
| State | `extensions/state/<state>/<entity-type>/<id>.md` |
| Department | `extensions/department/<dept>/<entity-type>/<id>.md` (e.g., `extensions/department/planning/entities/projects/<project-id>.md` post-#9) |
| Office | `extensions/office/<entity-type>/<id>.md` (e.g., `extensions/office/clients/maxsolar.md`) |
| Project (state.md) | `<project-root>/state.md` (the per-project entity stays at project root, not in `extensions/`) |

**Naming**: file basename = entity `id` field exactly (`<id>.md`,
not `<id>-something.md`). One file = one entity instance.

---

## 2. File structure

```markdown
---
<frontmatter — Layer 1 universal fields + Layer 2 type-specific fields>
---

# <label or title>

<body — free-form markdown with recommended sections per type>
```

**Three required separators**: file MUST begin with `---` on
line 1, frontmatter ends with `---` on its own line, body
follows. Same shape `state.md` already uses; reused via the
generic entity gate (post-#9 `read_entity` / `write_entity`).

---

## 3. Layer 1 — Universal frontmatter (every entity, strict-locked)

These fields appear in EVERY entity-md regardless of type. Pydantic
base `EntityBase`. Fail-loud validation at gate.

| Field | Type | Required | Allowed values / Format | Notes |
|---|---|---|---|---|
| `id` | str | ✅ | kebab-case (`[a-z0-9-]+`); unique within scope | The stable identifier. Matches file basename. |
| `label` | str | ✅ | non-empty | Human-readable display name. |
| `type` | enum | ✅ | `doctype` / `reference` / `project` / `client` / `actor` / `process` / `baustein` / `entity_definition` / ... | Routes to Layer-2 Pydantic subclass at gate. Living enum extended per #9. |
| `scope` | enum | ✅ | `universal` / `domain` / `state` / `department` / `office` / `project` | 4-axis position per ARCHITECTURE meta-rule 3 + #12. |
| `scope_key` | str \| null | ✅ | `null` for universal; `"Naturschutz"` / `"PV-FFA"` / `"Wind"` for domain; `"MV"` / `"BB"` for state; `"planning"` / `"invoicing"` for department; `null` for office | Identifies WHICH entry within the scope axis. |
| `status` | enum | ✅ | `active` / `deferred` / `stub` / `archived` | Canonical lifecycle marker. |
| `last_updated` | date | ✅ | ISO 8601 (`YYYY-MM-DD`) | Freshness. Updated on every meaningful edit. |
| `description` | str \| null | ⚠ optional | one-line | Used in listings (e.g., `list_entities` MCP output). Keep short — full description goes in body. |
| `tags` | list[str] | ⚠ optional | each tag kebab-case | Free-form categorization. |

**Format conventions for Layer 1**:

- Field naming: **snake_case** (no camelCase, no kebab-case)
- Booleans: lowercase `true` / `false`
- Lists: YAML block style (`- item`) preferred over flow (`[item, item]`) for readability
- Quoting: prefer unquoted scalars; quote only when YAML would mis-parse (colons, brackets, leading hyphens)
- Dates: ISO 8601 (`2026-04-30`) — NO `Date(...)`, NO `2026/04/30`

### 3.1 Identifier uniqueness conventions

`id` MUST be unique within scope. The strategy for ensuring
uniqueness is **per-deployment** and should be documented in
office-config or `department.md` body — typically as a prose
convention rule (see `governance-and-identity-sourcing.md`
"Office conventions as prose-rules").

Common strategies:

| Strategy | Form | Use case |
|---|---|---|
| Firstname-lastname | `alice-mueller.md` | Native mode; small bureau; low collision risk |
| Email-prefix derived | `alice-mueller-schulz-de.md` | Native mode; email-based namespacing; ugly but unique |
| HR-system internal ID | `actor-12345.md` (filename) + `Alice Müller` (label in body) | Adapter mode (Personio, BambooHR); humans rarely see filename |
| Domain-natural ID | `b-plan-begruendung.md` for doctypes; `BauGB.md` for references | Type has obvious natural identifier; collision-free by definition |
| Project-prefixed | `<project-slug>-<entity>` | Per-project sub-entities where collision across projects is possible |

**For high-collision-risk scopes** (actors, clients with common
names; sub-entities across projects), the deployment SHOULD
document the convention explicitly:

```markdown
# In office-config.md body or extensions/office/conventions.md

## Actor identifier convention

Actor IDs follow `<firstname>-<lastname>` derived from
`<firstname>.<lastname>@schulz-planung.de` company email.
On collision, append middle initial: `alice-m-mueller`.
Adapter-mode deployments use the HR system's internal ID;
this convention does not apply to those.
```

AI applies the convention at mint-time per the prose-rule pattern
(per `governance-and-identity-sourcing.md` decision 4). Audit
event records both the convention reference and the produced ID.

**For low-collision-risk scopes** (universal/domain doctypes,
references with natural names), the natural identifier IS the ID
and no convention is needed. The Layer-1 `id` constraint
(kebab-case, unique within scope) is sufficient.

---

## 4. Layer 2 — Type frontmatter (per-entity-type, strict-locked)

Each entity type extends `EntityBase` with type-specific fields.
Schemas grow in during #9 alongside Pydantic subclasses. This
section is a **scaffold** — fields listed here are the planned
contract; final shape lands with #9 implementation.

### `doctype`

| Field | Type | Required | Notes |
|---|---|---|---|
| `style_ref` | str \| null | ⚠ | Path to style spec section (e.g., `memory/universal/style/style-spec.md#doctype-a-begruendung`) |
| `master_file_pattern` | str \| null | ⚠ | LaTeX master file naming pattern |
| `project_subfolder_default` | str \| null | ⚠ | Default subfolder under `<project-root>/` |
| `paired_with` | str \| null | ⚠ | Another doctype id; enforces co-creation |
| `document_class` | str \| null | ⚠ | LaTeX document class (e.g., `scrreprt`, `article`) |
| `latex_engine` | str \| null | ⚠ | `pdflatex` / `lualatex` / `xelatex` |

### `reference`

| Field | Type | Required | Notes |
|---|---|---|---|
| `source_url` | str (URL) | ✅ | Where the canonical text lives |
| `canonical_path` | str | ✅ | Local fetch destination relative to corpus root |
| `fetch_method` | enum | ✅ | `web-text` / `pdf-fetch` / `manual` / ... |
| `last_fetched` | date \| null | ✅ | null until first fetch |
| `last_modified_at_source` | date \| null | ⚠ | tracked when fetch reports it |
| `current_amendment_form` | str \| null | ⚠ | e.g., "Stand 2024-XX" |
| `checksum_sha256` | str \| null | ✅ | null until first fetch |
| `archive_versions` | bool | ✅ | whether to keep prior versions |
| `retention_versions` | int | ⚠ | number of prior versions to retain |
| `ingest` | bool | ✅ | whether to embed into LanceDB |
| `chunking_strategy` | str \| null | ⚠ | e.g., `per-paragraph`, `per-section` |
| `chunk_metadata_extractor` | str \| null | ⚠ | extractor module reference |
| `jurisdiction` | enum | ✅ | `bund` / `eu` / `state-XX` / ... |

### `project` (the state.md schema, post-#9 relocated)

Inherits today's ProjectState fields. Spec'd in
`backend/mcp-server/src/pbs_mcp/project_state.py` until #9
relocates to `extensions/department/planning/entities/projects/<id>.md`.
Layer 2 fields include `bundesland`, `verfahren_type`,
`lifecycle`, `phase`, `departments_active`, `doctype_status`,
`deadlines`, `linked_projects`, `geltungsbereich_ha`,
`b_plan_nr`, etc.

### `client` (per #15)

| Field | Type | Required | Notes |
|---|---|---|---|
| `legal_name` | str | ✅ | Full legal entity name |
| `primary_contact` | str | ✅ | Actor id or name |
| `address` | object | ⚠ | Structured address block |
| `billing_contact` | str \| null | ⚠ | Actor id |
| `default_payment_terms` | int | ⚠ | days net |
| `default_currency` | enum | ⚠ | ISO currency code |
| `mode` | enum | ⚠ | `native` / `adapter` |
| `adapter` | str \| null | ⚠ | adapter id when `mode: adapter` |

### `actor` (per #15)

| Field | Type | Required | Notes |
|---|---|---|---|
| `kind` | enum | ✅ | `internal` / `external` / `system` |
| `roles` | list[str] | ⚠ | open-ended per deployment |
| `email` | str \| null | ⚠ | |
| `departments` | list[str] | ⚠ | for internal actors, which departments they work in |

### `process` (per #16, populated during #11/#9)

| Field | Type | Required | Notes |
|---|---|---|---|
| `applicable_when` | object | ✅ | conditions for the process to apply (e.g., `verfahren_type: beschleunigtes`) |
| `produces_doctypes` | list[str] | ✅ | doctype ids this process flow produces |

Process ENTITIES are markdown-heavy by design. Most of the
process logic lives in the body, not Layer 2 fields.

### `baustein` (memory entries elevated to entity status, rare)

Per the entity-elevation 3-test, most bausteine remain memory
entries and don't elevate. Layer 2 fields TBD case-by-case when
elevation occurs.

---

## 5. Layer 3 — Per-deployment extension fields

**DEFERRED to #9**. Three options on the table:

- Pydantic subclass per deployment (heavy, type-safe)
- Office-config-declared `extra_fields: dict[str, type]` per entity (lighter)
- Free-form `metadata: dict` escape hatch on EntityBase (loosest)

This section will fill in once #9 decides which mechanism wins.

---

## 6. Body conventions

Body is markdown, free-form prose, AI reads at runtime. Per-entity-
type **recommended** sections below. Audit slice 21 + design-review
target 12 check presence + emptiness; gate never rejects body for
missing sections.

### Heading-level conventions (apply to all entity bodies)

- **No h1 in body**. The frontmatter `label:` field carries the
  display name. Bodies start at h2 (`##`).
- **h2 for top-level sections** (the recommended sections per
  type below).
- **h3 for sub-sections** within an h2.
- **h4 rarely used**; bodies should not require deep nesting.
  If they do, consider whether the entity is too large.

### Body section catalog by entity type

#### `doctype`

```markdown
## When this doctype applies
## Section conventions
## Pairing semantics    (only if `paired_with` set in frontmatter)
## Domain-specific deviations    (only if domain-specific variations exist)
```

#### `reference`

```markdown
## Why this matters
## Key sections for our work
## Recent amendments to watch
## Common citations
## Cross-refs
```

#### `project` (state.md body)

```markdown
## Context
## History
## Open questions
## Decisions
```

(`History` is append-only by convention; never edit prior entries.)

#### `client`

```markdown
## Communication preferences
## Billing conventions
## Project history summary
## Watch-outs
```

#### `actor`

```markdown
## Role + responsibilities
## Working preferences
## Capabilities + limits
```

#### `process`

```markdown
## Phase sequence
## Required doctypes per phase
## Mandatory triggers
## Exceptions and shortcuts
```

#### `entity_definition` (adapter-mode entity definitions, e.g. Invoice via Lexware)

```markdown
## How this office uses <external system>
## Edge cases
## Mapping to PBS concepts
## Communication conventions
```

---

## 7. Cross-reference syntax

When entity bodies reference other entities or files:

| Reference target | Syntax | Example |
|---|---|---|
| Another entity (same scope) | `<entity-type>/<id>` | `doctypes/b-plan-festsetzungen` |
| Another entity (different scope) | `<scope>/<scope-key>/<entity-type>/<id>` | `domain/Naturschutz/doctypes/saP-hauptpruefung` |
| Memory entry | `memory/<path>` | `memory/universal/style/style-spec.md` |
| Reference (legal text) | `references/<id>` (when located in references dir) | `references/BauGB` |
| Specific section in another file | `<path>#<heading-anchor>` | `memory/universal/style/style-spec.md#doctype-a-begruendung` |
| Standard markdown link (external URL) | `[label](url)` | `[BauGB](https://www.gesetze-im-internet.de/baugb/)` |

**No wikilinks** (`[[id]]`). They render unevenly across
markdown processors and add a non-standard syntax that AI must
parse separately.

---

## 8. List + table conventions

- Bulleted lists: `-` (not `*`)
- Numbered lists: `1.` `2.` `3.` (don't auto-number with `1.`
  everywhere)
- Tables: GitHub-flavored markdown; align `|` characters for
  legibility when feasible

---

## 9. Code block conventions

- Use fenced code blocks with language tags: ` ```yaml ` /
  ` ```python ` / ` ```latex `
- For inline frontmatter examples, use ` ```yaml ` to make the
  YAML structure explicit
- Avoid `<code>` HTML tags; use backticks

---

## 10. Validation expectations

### Layer 1 + Layer 2 (gate-validated, fail-loud)

- All required fields present
- Field types match Pydantic subclass
- Enum values within allowed set
- `id` is kebab-case + unique within scope
- `last_updated` is ISO 8601 date
- Cross-referenced `<entity>_id:` fields point to existing
  entities (gate validates at write time; read-time validation
  flags but doesn't fail)

### Body (audit + design-review enforced, NEVER gate-rejected)

- Recommended sections per type are present (warning if
  missing)
- Sections have substantive content (warning if empty / placeholder)
- Heading levels follow conventions (no h1, h2 for top, h3 for sub)
- Cross-references resolve (no dead links)

---

## 11. Examples

See `docs/decisions/ai-as-runtime-hybrid-shape.md` "Worked
examples" section for three full-form examples:

1. **Doctype** — `b-plan-begruendung.md` (universal scope)
2. **Reference** — `BauGB.md` (universal scope, federal jurisdiction)
3. **Adapter-mode entity** — Invoice via Lexware (department
   scope, mode=adapter)

---

## 12. Migration of existing files

| Today | After migration | Timing |
|---|---|---|
| `extensions/universal/doctypes.yaml` (one file, all doctypes) | `extensions/universal/doctypes/<id>.md` (one file per doctype) | Bundled with #9 |
| `extensions/domain/<domain>/doctypes.yaml` | `extensions/domain/<domain>/doctypes/<id>.md` | Bundled with #9 |
| `extensions/{universal,domain,state}/references-manifest.yaml` | `extensions/{universal,domain,state}/references/<id>.md` | Bundled with Phase 1 corpus full-refresh |
| `<project-root>/state.md` (already hybrid-shape) | unchanged in shape; relocates to follow new schema location post-#9 | Bundled with #9 |
| `extensions/department/<dept>/department.yaml` (NEW per #11) | adopts hybrid-shape from inception (md + frontmatter), NOT pure YAML | #11 implementation |

---

## 13. Change-management of THIS document

This spec is load-bearing for design-review target 12 + audit
slice 21. Changes to it must:

- Bump the spec version (frontmatter `last_updated:` field of
  this doc) — date-only, treat any same-day change as one bump
- Note the change in HANDOFF for next-session awareness
- Run target 12 + slice 21 on existing entity-mds to identify
  any that drift from the new spec; flag for migration
- For breaking changes (Layer 1 field rename, body section
  rename): pre-launch, edit-in-place + sed across `extensions/`;
  post-launch, follow ARCHITECTURE.md deprecation procedure for
  schemas

---

## 14. Open items growing in during #9

- **Layer 2 schemas finalized** alongside Pydantic subclasses
  (this doc carries today's scaffold; #9 lands the canonical set)
- **`type:` enum extended** as new entity types arrive
- **Layer 3 mechanism decided** (subclass / extra_fields / metadata)
- **Body section conventions evolved** as real entities accumulate
  and section names prove too narrow / too vague
- **Cross-reference resolution** at gate (validation tightness
  decision)

---

## 15. Open items growing in beyond #9

- **Gate-level selective section read** (D2 in
  `ai-as-runtime-hybrid-shape.md`): if entity bodies grow large
  enough, extend `read_entity(path)` with a `sections:` parameter
  that returns only matching h2-anchored regions. **Sharper
  trigger**: revisit when median entity body > 1500 tokens OR
  any single entity body > 4000 tokens routinely. Whichever
  fires first. Folds into #9 gate work when triggered (parameter
  extension, no new task). The capability of "AI focuses on a
  named section" already exists today via §16 anchor-and-grep
  technique; D2 is a context-cost optimization, not a capability
  gap.
- **Body-spec per-deployment override**: a specific deployment may
  want additional recommended sections per entity type. Resolve
  via Layer 3 extension mechanism once decided.
- **Multi-language support**: today bodies are written in user's
  active language (PBS = German + English mixed). If multiple
  bureaus deploy with different languages, formalize convention.

---

## 16. Body-size discipline + selective-read techniques (D2 mitigations)

The D2 deferral (gate-level selective section read) assumes
bodies stay small enough that loading the whole body is cheap.
The mitigations below keep that assumption true — the trigger
ideally never fires.

### 16.1 Section-size guidance

| Section size | Status | Action |
|---|---|---|
| ≤500 tokens | ✅ healthy | none |
| 500-1000 tokens | ⚠ on watch | review at next edit; consider whether content can be tightened |
| >1000 tokens | ❌ over budget | split section into sub-sections (h3) OR factor content out (e.g., long examples → linked memory entry; long historical notes → separate `## History` section that's understood as append-only) |

### 16.2 Body-size guidance

| Body size | Status | Action |
|---|---|---|
| ≤1500 tokens | ✅ healthy | none |
| 1500-3000 tokens | ⚠ on watch | review whether sections are pulling weight; consider pruning stale content |
| >3000 tokens | ❌ over budget | split entity OR aggressively prune stale content. **Splitting is non-trivial** — consult design-review target 11 (entity-elevation 3-test) before splitting; pre-emptive splitting can create entity sprawl. |

### 16.3 Pruning norm

Bodies are NOT append-only (except `## History` sections on
project entities, which ARE append-only by convention). Older
content that's no longer load-bearing should be pruned during
edits — like normal documentation maintenance. Brief commit
message captures what was removed and why.

This applies especially to:

- **Reference entities** — `## Recent amendments to watch`
  accumulates; old amendments past their relevance window get
  pruned (e.g., post-2024 §13b reintroduction note can be
  shortened once verified consistently in fetched corpora)
- **Doctype entities** — `## Domain-specific deviations` may
  accumulate edge cases that turn out to be rare; consolidate or
  remove
- **Process entities** — `## Exceptions and shortcuts`
  accumulates; rare exceptions that haven't fired in N projects
  can be pruned (or moved to a "rare-cases" linked memory entry)

### 16.4 Anchor-and-grep technique (selective focus today, no infrastructure needed)

Today the gate returns full body. AI can still selectively focus:

1. Body sections have stable h2 anchors per §6 conventions
2. To focus on `## When this applies` in a doctype, AI:
   - Loads the body (full read)
   - Locates `## When this applies` heading
   - Reads from that heading until the next `## ` heading or end of body
   - Uses ONLY that section in its reasoning chain

This is a documented technique, not infrastructure. It works
today. Only when bodies get large enough that even the full-load
becomes expensive does D2's gate-level selective return become
needed.

### 16.5 Selective-include in skill orchestration

When orchestrator dispatches a sub-agent that needs to reason
about a specific entity aspect (e.g., "is this doctype applicable
for §13a?"), it can:

1. Read the entity's full body
2. Extract just the relevant section (per §16.4)
3. Pass the extracted section to the sub-agent via prompt

This pushes selective-read into skill-side composition rather
than gate-side parameter. Works today. Future audit slice
(post-#9) can flag skills that pass full bodies when a single
section would suffice.

### 16.6 Audit slice 21 telemetry sub-check

Audit slice 21 (entity-md frontmatter + body conformance scan)
gains a body-size telemetry sub-check:

- **Per-entity output**: section sizes (token counts), total body
  size, oldest section unedited (for pruning signal)
- **Aggregate output**: median body size across all entities;
  max body size; count of entities over §16.1/§16.2 thresholds
- **D2 trigger detection**: if median > 1500 OR max > 4000,
  flag in audit report — signal that D2 should be revisited and
  folded into #9-followup gate work

The telemetry runs on every audit slice 21 invocation; cheap to
compute, valuable for monitoring.

---

**Last meaningful edit**: 2026-04-30 (session 11 — §3.1
identifier uniqueness conventions added per
`governance-and-identity-sourcing.md` decisions; previous edit
session 10 followup — scaffold authored alongside #16 decision
record + ARCHITECTURE v0.16 bump; §16 D2 mitigations added in
same followup).
