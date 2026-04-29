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

- **Section-addressable bodies** (D2 in `ai-as-runtime-hybrid-shape.md`):
  if entity bodies grow large enough, formalize section-anchor
  conventions so AI can selectively read sub-sections without
  loading the whole body. Defer until pain felt.
- **Body-spec per-deployment override**: a specific deployment may
  want additional recommended sections per entity type. Resolve
  via Layer 3 extension mechanism once decided.
- **Multi-language support**: today bodies are written in user's
  active language (PBS = German + English mixed). If multiple
  bureaus deploy with different languages, formalize convention.

---

**Last meaningful edit**: 2026-04-30 (session 10 followup —
scaffold authored alongside #16 decision record + ARCHITECTURE
v0.16 bump).
