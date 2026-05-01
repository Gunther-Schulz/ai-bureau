# Entity-md spec — formatting + terminology reference

> **v0.34 RESTRUCTURE session 15** per `docs/decisions/entity-md-scope-model-restructure.md`:
> flat 6-axis `scope` + `scope_key` enum REPLACED with three-category structure
> (Layer A: universal/domain/state; Owner B: workspace/specialist/project;
> Framework C: shape/substrate/protocol/specialist-DEFINITION). Each entity
> has exactly ONE category populated; Pydantic at-least-one-of validator
> enforces. Plus NEW Definition-vs-instance binding pattern: framework-primitive
> DEFINITIONS in Framework C; INSTANCE-SELECTION via workspace.md fields
> (Owner B) referencing definitions. Layer 2 schemas added for shape/substrate/
> protocol/specialist Framework C entity types (§4); body conventions added
> (§6); type namespacing per category (§3.2). Migration to three-category
> structure: pre-launch zero migration cost today; full cascade scheduled with
> #11 single-touch refactor.
>
> **Earlier supersession** (session 13 per #22 Sub-DR A): `department` → `specialist`;
> `office` → `workspace`. Both renames absorbed by v0.34 restructure where applicable.

**Status**: scaffold authored session 10; v0.34 restructure session 15 (three-category structure + Definition-vs-instance binding pattern). Layer 1 + Layer 2 schemas + body section conventions complete for all categories; specific Layer 2 fields per Framework C entity type grow in during #9 + #25 implementation phases.
**Owner**: ARCHITECTURE.md "Three-category scope model" section (was "Layering convention: scope orthogonality") + `docs/decisions/entity-md-scope-model-restructure.md` (v0.34) + `docs/decisions/ai-as-runtime-hybrid-shape.md` (Layer 1+2+3 contract) + `docs/decisions/terminology-and-specialist-primitive.md` (#22 Sub-DR A).
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

> **v0.34 restructure (session 15)** per `docs/decisions/entity-md-scope-model-restructure.md`: replaces flat 6-axis `scope` + `scope_key` with three-category structure (Layer A / Owner B / Framework C). Each entity has exactly ONE category populated; Pydantic at-least-one-of validator enforces. The previous `scope` + `scope_key` fields are SUPERSEDED. Old fields ↔ new fields mapping in §12 migration.

### Common Layer 1 fields (every entity, regardless of category)

| Field | Type | Required | Allowed values / Format | Notes |
|---|---|---|---|---|
| `id` | str | ✅ | kebab-case (`[a-z0-9-]+`); unique within (scope-category, scope-key, type) | The stable identifier. Matches file basename. |
| `label` | str | ✅ | non-empty | Human-readable display name. |
| `type` | str | ✅ | per-category rules (see §3.2) | Routes to Layer-2 Pydantic subclass at gate. |
| `status` | enum | ✅ | `active` / `deferred` / `stub` / `archived` | Canonical lifecycle marker. |
| `last_updated` | date | ✅ | ISO 8601 (`YYYY-MM-DD`) | Freshness. Updated on every meaningful edit. |
| `description` | str \| null | ⚠ optional | one-line | Used in listings (e.g., `list_entities` MCP output). Keep short — full description goes in body. |
| `tags` | list[str] | ⚠ optional | each tag kebab-case | Free-form categorization. |

### Scope category fields (exactly ONE category populated; Pydantic at-least-one-of validator)

#### Category A — Layer scope (layered content; merge by specificity)

| Field | Type | Required | Notes |
|---|---|---|---|
| `layer_scope` | enum \| null | when category active | `universal` / `domain` / `state` |
| `layer_key` | str \| null | when domain/state | null for universal; e.g., `"Naturschutz"` / `"PV-FFA"` for domain; `"MV"` / `"BB"` for state |

Used for: doctypes, references, manifests, bausteine, conventions content. Effective content = universal + active-domains + active-states (per workspace.md `scope.{domains,states}`); most-specific wins on conflicts. Gate dispatch: layered loader merges across active scope_keys.

#### Category B — Owner scope (deployment-instance ownership)

| Field | Type | Required | Notes |
|---|---|---|---|
| `owner_scope` | enum \| null | when category active | `workspace` / `specialist` / `project` |
| `owner_key` | str \| null | when specialist/project | null for `workspace` (workspace.md is the workspace itself); e.g., `"planning-document-work"` for specialist; `"<project-id>"` for project |

Used for: workspace.md (the workspace itself; owner_scope=workspace, owner_key=null); entities owned within a specialist instance (skills, processes, internal references — owner_scope=specialist, owner_key=<specialist-id>); project entity instances (per-project state.md, decisions, snapshots — owner_scope=project, owner_key=<project-id>). Gate dispatch: owner-lookup by (owner_scope, owner_key).

#### Category C — Framework primitive (definitions; immutable; distributable)

| Field | Type | Required | Notes |
|---|---|---|---|
| `framework_kind` | enum \| null | when category active | `shape` / `substrate` / `protocol` / `specialist` |
| `framework_key` | str | required when framework_kind active | e.g., `"practitioner"` for shape; `"claude-agent-sdk"` for substrate; `"event-coordination"` for protocol; `"planning-document-work"` for specialist DEFINITION |

Used for: framework-supplied primitive DEFINITIONS — distributable, immutable, composable. Gate dispatch: framework registry lookup; compat matrix validation; Option B floor enforcement (anti-Art-25-trap, claim-level audit, human authority chain — non-overridable per `shape-extension-and-architectural-floor.md`).

**Specialist dual-nature** (the only category-spanning primitive): specialist DEFINITION lives in Framework C (`framework_kind: specialist`; entity is the distributable bundle); specialist as SCOPE is Owner B (entities WITHIN a specialist's instance use `owner_scope: specialist, owner_key: <specialist-id>`). See `docs/decisions/entity-md-scope-model-restructure.md` §1 "Specialist dual-nature" for full reasoning.

Shape / substrate / protocol do NOT have dual-nature — their internal pieces ship as part of the definition's package, not as Owner B sub-entities.

### Definition vs instance binding pattern (per restructure DR §2)

Framework C definitions are bound by Owner B workspace.md reference fields:

```yaml
# workspace.md (Owner B; type=workspace.workspace; owner_scope=workspace, owner_key=null)
shape: <shape-id>                          # Framework C reference; exactly one
substrate: <substrate-id>                  # Framework C reference; exactly one
specialists_employed: [<specialist-id>+]   # Framework C references; multi-valued
protocol_overrides:                        # optional per-axis Framework C references; defaults from shape
  coordination: <protocol-id>
  sparring: <protocol-id>
  audit: <protocol-id>
  trust: <protocol-id>
  time: <protocol-id>
groupings: dict[str, list[<specialist-id>+]] | null   # per #22 Sub-DR A
```

Validation gate enforces compat: `substrate` in shape's `substrate_compat`; specialists' `shapes_supported` includes selected shape; `protocol_overrides` in shape's `protocols_allowed` per kind; **Option B floor axioms NOT overridable**.

**Format conventions for Layer 1**:

- Field naming: **snake_case** (no camelCase, no kebab-case)
- Booleans: lowercase `true` / `false`
- Lists: YAML block style (`- item`) preferred over flow (`[item, item]`) for readability
- Quoting: prefer unquoted scalars; quote only when YAML would mis-parse (colons, brackets, leading hyphens)
- Dates: ISO 8601 (`2026-04-30`) — NO `Date(...)`, NO `2026/04/30`

### 3.2 Type namespacing per scope category (v0.34 restructure; locked session 15)

The `type:` field follows category-specific namespacing rules. Three rule shapes; each makes wrong shapes impossible by construction within its category.

#### Category A — Layer scope: `<layer_scope>.<entity-type>`

| Entity | Type field | Layer 1 scope-category fields |
|---|---|---|
| Universal doctype b-plan-begruendung | `universal.doctype` | layer_scope=universal, layer_key=null |
| Universal reference (BauGB) | `universal.reference` | layer_scope=universal, layer_key=null |
| Domain reference saP | `domain.reference` | layer_scope=domain, layer_key=Naturschutz |
| State legal supplement | `state.legal-supplement` | layer_scope=state, layer_key=MV |

#### Category B — Owner scope: `<owner_scope-or-specialist-id>.<entity-type>`

- **workspace**: `type: workspace.<entity-type>` (e.g., `workspace.workspace` for workspace.md itself; `workspace.actor`; `workspace.client`)
- **specialist**: `type: <specialist-id>.<entity-type>` (e.g., `planning-document-work.process`, `planning-document-work.project-deadline`, `litigation.matter`)
- **project**: `type: project.<entity-type>` or just `type: project` (most projects use Layer 1+2 directly without entity-type sub-discrimination; e.g., `project` for state.md; `project.snapshot`; `project.module-decision`)

| Entity | Type field | Layer 1 scope-category fields |
|---|---|---|
| Workspace.md (PBS-Schulz) | `workspace.workspace` | owner_scope=workspace, owner_key=null |
| Workspace actor | `workspace.actor` | owner_scope=workspace, owner_key=null |
| Workspace client | `workspace.client` | owner_scope=workspace, owner_key=null |
| Specialist process (regelverfahren) | `planning-document-work.process` | owner_scope=specialist, owner_key=planning-document-work |
| Specialist doctype | `planning-document-work.doctype` | owner_scope=specialist, owner_key=planning-document-work |
| Project state.md | `project` | owner_scope=project, owner_key=<project-id> |
| Project snapshot | `project.snapshot` | owner_scope=project, owner_key=<project-id> |
| Hypothetical legal matter | `litigation.matter` | owner_scope=specialist, owner_key=litigation |

#### Category C — Framework primitive: unprefixed type matching the kind

Framework primitives use unprefixed type matching the kind (consistent with §4 registration-file-type exception for department/office/universal types; reduces redundancy with framework_key field).

| Entity | Type field | Layer 1 scope-category fields |
|---|---|---|
| Shape definition (practitioner) | `shape` | framework_kind=shape, framework_key=practitioner |
| Substrate definition (claude-agent-sdk) | `substrate` | framework_kind=substrate, framework_key=claude-agent-sdk |
| Substrate definition (ms-agent-framework) | `substrate` | framework_kind=substrate, framework_key=ms-agent-framework |
| Protocol definition (event-coordination) | `protocol` | framework_kind=protocol, framework_key=event-coordination |
| Protocol definition (always-on-sparring) | `protocol` | framework_kind=protocol, framework_key=always-on-sparring |
| Specialist DEFINITION (planning-document-work) | `specialist` | framework_kind=specialist, framework_key=planning-document-work |

**Note specialist dual-nature**: specialist DEFINITION uses `type: specialist` + `framework_kind: specialist` (Framework C); entities OWNED within a specialist instance use `type: <specialist-id>.<entity-type>` + `owner_scope: specialist` (Owner B). Two different uses of "specialist" in the type system.

**Why per-category namespacing** (instead of uniform `<category>.<entity-type>`):

- **Layer A + Owner B**: namespacing prevents type-name collisions across scope-keys (multiple specialists naturally reuse common type names like `process`, `doctype`, `project-deadline`); makes blueprint sharing collision-safe; aligns with Python modules / SQL schemas / Kubernetes namespaces.
- **Framework C**: no sub-types within a framework primitive (a shape isn't a category of "shape entity types"; the shape itself IS the entity); identity comes from framework_key. Same pattern as registration-file types per §4.
- **Audit-trail filtering**: type-prefix queries work naturally per category (e.g., `query_audit_trail(type_prefix="litigation.")` returns all entities owned by litigation specialist; `query_audit_trail(framework_kind="shape")` returns all shape-related events).

### Pre-restructure registration files (transitioning out per #11 single-touch refactor)

The pre-v0.34 registration-file pattern (`extensions/department/<dept>/department.md` + `extensions/office/office.md` + `extensions/universal/universal.md` with `managed_entities` maps; locked session 11 Bundle A) is SUPERSEDED by the three-category structure. Specialist DEFINITIONS now use Framework C entity-md form directly; entities owned within specialist instances use Owner B scope.

Migration to three-category structure: scheduled with #11 single-touch refactor (file path migrations + Pydantic class migrations). Pre-launch / no production entity-md instances persisted = essentially zero migration cost today.

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

### `department` / `office` / `universal` (pre-restructure registration-file types — SUPERSEDED v0.34)

> **SUPERSEDED v0.34**: pre-restructure used `managed_entities` registration map at `department.md` / `office.md` / `universal.md` to declare which entity types each scope hosted. Three-category structure replaces this: Owner B specialist scope hosts entities WITHIN a specialist instance (no registration map needed; entity type derived from `<specialist-id>.<entity-type>` namespacing); Framework C primitives are self-registering via filesystem location (`extensions/framework/<kind>/<id>/`). Pre-restructure registration files (department.md / office.md / universal.md) migrate to Framework C specialist-DEFINITION entities OR Owner B workspace.md per #11 single-touch refactor.

The pre-restructure shape, kept here for migration reference:

- `DepartmentEntity` (was for `type: department`) → SUPERSEDED. Specialist DEFINITIONS now use Framework C entity-md form (see `specialist` Framework C entry below).
- `OfficeEntity` (was for `type: office`) → SUPERSEDED. Workspace.md is now Owner B `type: workspace.workspace`.
- `UniversalEntity` (was for `type: universal`) → SUPERSEDED. Universal-scope entities self-classify via Layer A `layer_scope: universal`; no central registration entity needed.

### `shape` (Framework C; v0.34 NEW per #25 Shape extension framework)

Framework C entity type for workspace shape definitions. Lives at `extensions/framework/shapes/<shape-id>/shape.md`.

| Field | Type | Required | Notes |
|---|---|---|---|
| `display_name` | str | ✅ | e.g., "Practitioner Workspace" |
| `default_configs` | object | ✅ | Per-axis defaults: `coordination_protocol` / `sparring_intensity` / `audit_granularity` / `author_primitive` / `trust_model` / `time_model` |
| `protocols_allowed` | dict[str, list[str]] | ✅ | Per Protocol kind (coordination/sparring/audit/trust/time): list of allowed protocol-ids that this shape composes with. Workspace's `protocol_overrides` must select from these. |
| `shape_specific_primitives` | list[str] | ⚠ | Pydantic schemas + MCP gates needed per shape (e.g., `Ticket` + `Budget` for autonomous-business shape) |
| `substrate_compat` | list[str] | ✅ | Substrate ids supported (e.g., `[claude_agent_sdk, ms_agent_framework]`) |
| `required_extensions` | list[str] | ⚠ | Other shape extensions this depends on (e.g., hybrid shape might compose two shapes) |
| `semver` | str | ✅ | Per-shape version |
| `option_b_floor` | object | ✅ | Anti-Art-25-trap + claim-level audit + human authority chain enforcement (always-on per shape; `shape-extension-and-architectural-floor.md` Option B floor) |

### `substrate` (Framework C; v0.34 NEW per #25 + relocated from backend code)

Framework C entity type for substrate implementation definitions. Lives at `extensions/framework/substrates/<substrate-id>/substrate.md`. Selected by workspace.md `substrate: <substrate-id>` field.

| Field | Type | Required | Notes |
|---|---|---|---|
| `display_name` | str | ✅ | e.g., "Claude Agent SDK" |
| `substrate_protocol_compat` | list[str] | ✅ | Substrate Protocol surfaces implemented (per `substrate-protocol-design.md` common surface) |
| `agent_loop_implementation` | str | ✅ | Module reference (e.g., `extensions.framework.substrates.claude_agent_sdk.agent_loop`) |
| `mcp_attach_mechanism` | str | ✅ | How MCP servers attach (e.g., `in-process` / `stdio` / `http`) |
| `runhooks_lifecycle` | list[str] | ✅ | Lifecycle hooks supported (e.g., `[pre_tool, post_tool, on_error]`) |
| `shape_compat` | list[str] | ✅ | Shapes this substrate works with (e.g., `[practitioner, autonomous-business]` or `["all"]`) |
| `boot_characteristics` | object | ⚠ | Operational profile: `boot_time` / `memory_footprint` / `runtime_deps` |
| `semver` | str | ✅ | Per-substrate version |

### `protocol` (Framework C; v0.34 NEW per #25 Protocol pluggability)

Framework C entity type for Protocol implementation definitions. Lives at `extensions/framework/protocols/<protocol-id>/protocol.md`. Selected per shape's `default_configs` AND optionally overridden via workspace.md `protocol_overrides`.

| Field | Type | Required | Notes |
|---|---|---|---|
| `display_name` | str | ✅ | e.g., "Event-Shaped Coordination" |
| `protocol_kind` | enum | ✅ | `coordination` / `sparring` / `audit` / `trust` / `time` |
| `pydantic_class` | str | ✅ | Module reference for the Pydantic Protocol implementation |
| `shape_compat` | list[str] | ✅ | Shapes this protocol implementation works with (e.g., `[practitioner]` for sparring=always-on; `[autonomous-business]` for sparring=optional) |
| `substrate_compat` | list[str] | ⚠ | Substrate constraints (most protocols are substrate-agnostic; some require specific substrate primitives) |
| `failure_modes` | list[object] | ⚠ | Documented failure modes + recovery paths |
| `option_b_axiom` | enum \| null | ⚠ | If this protocol implements one of the 3 non-overridable axioms: `anti_art_25_trap` / `claim_level_audit` / `human_authority_chain` / null |
| `semver` | str | ✅ | Per-protocol version |

### `specialist` (Framework C DEFINITION; v0.34 NEW per #22 Sub-DR A)

Framework C entity type for specialist DEFINITIONS (the distributable composable bundle). Lives at `extensions/framework/specialists/<specialist-id>/specialist.md`. Distinct from Owner B specialist scope (entities within a specialist's instance).

| Field | Type | Required | Notes |
|---|---|---|---|
| `display_name` | str | ✅ | e.g., "Planning Document Work" |
| `composability_axes` | list[enum] | ✅ | Per #22 Sub-DR A: subset of `[FROM, IN, WITH, ACROSS, OVER]` |
| `classification` | enum | ✅ | `cross_archetype` (e.g., citation-verification) / `domain_anchored` (e.g., planning-document-work) |
| `skills_bundled` | list[str] | ✅ | Skill ids included in this specialist (skills live within `extensions/framework/specialists/<id>/skills/`) |
| `entity_types_owned` | list[str] | ✅ | Entity types owned by an instance of this specialist (e.g., `[planning-document-work.process, planning-document-work.project-deadline]`) — defines the Owner B sub-types this specialist hosts |
| `references_required` | list[str] | ⚠ | Reference content this specialist needs (cross-refs into Layer A universal/domain references) |
| `memory_required` | list[str] | ⚠ | Memory entries this specialist needs |
| `adapters_consumed` | list[str] | ⚠ | Integration adapters this specialist uses (per glue-not-replacement) |
| `shapes_supported` | list[str] | ✅ | Shapes this specialist works under (e.g., `[practitioner, autonomous-business]` for cross-shape; `[practitioner]` for shape-specific) |
| `semver` | str | ✅ | Per-specialist-definition version |

Pydantic class definitions for shape / substrate / protocol / specialist Framework C entities land with **#25 + #9 implementation phases**.

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

#### `shape` (Framework C; v0.34)

```markdown
## What this shape is for
## When to use this shape (vs alternatives)
## Default configs explained
## Shape-specific primitives
## Substrate compat reasoning
## Migration from other shapes (if applicable)
## Option B floor enforcement (the 3 axioms in this shape's context)
```

#### `substrate` (Framework C; v0.34)

```markdown
## What this substrate provides
## Substrate Protocol surfaces implemented
## Operational characteristics    (boot time, memory, MCP attach pattern, RunHooks)
## Compat constraints    (which shapes work, which don't, why)
## Migration / version evolution
## Known limitations
```

#### `protocol` (Framework C; v0.34)

```markdown
## What this implementation does    (per axis: coordination/sparring/audit/trust/time)
## Configuration knobs
## Compat constraints    (which shapes + substrates)
## Failure modes + recovery
## Option B axiom binding    (if this protocol implements an axiom; null otherwise)
## Migration / version evolution
```

#### `specialist` (Framework C DEFINITION; v0.34)

```markdown
## What this specialist is for
## Composability axes    (FROM/IN/WITH/ACROSS/OVER per #22 Sub-DR A)
## Skills bundled    (high-level overview; details in skills/<name>/SKILL.md)
## Entity types owned    (the Owner B sub-types this specialist hosts)
## Required references    (cross-refs into Layer A universal/domain references)
## Memory dependencies
## Cross-archetype vs domain-anchored classification reasoning
## Adapter dependencies    (per glue-not-replacement)
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
