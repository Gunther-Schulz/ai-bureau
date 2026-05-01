# Decision record: AI-as-runtime hybrid-shape contract for managed entities + manifests

**Status**: ACCEPTED (session 10, 2026-04-29)
**Owner**: per-session HANDOFF; ARCHITECTURE.md "AI-as-runtime hybrid-shape" section; ROADMAP commitment #16
**Related**: ROADMAP commitment #11 (Cowork integration — `department.yaml` format decision depends on this), #15 (Client + Actor entity shapes), #9 (managed-entity concept design — uses this as central design lens; gate generalization lands here), #6 (audit-trail v2 retrofit — gate-side conformance check); `office-vs-department.md` (entity-elevation discipline + managed-entity concept this builds on)

## Context

Session-10 conversation resurfaced an architectural question that earlier framings had only gestured at: how do managed entities + manifests carry domain semantics (process flow, sub-entity required/optional rules, conditional logic) **portably across domains** without becoming a relational SQL schema?

The first-pass answer was a three-layer "structured + markdown + skill-prose-as-encoded-process" framing. That framing was **wrong** — it still treated process flow + conditional rules as something that gets *encoded* (just in prose instead of code), reproducing the SQL-DB trap in disguise.

The corrective: **AI processing is not a bridging layer between structured/freeform; it REPLACES the encoded-rules layer entirely.** The model already in use elsewhere — memories (frontmatter + markdown body, AI does the understanding) — is the canonical pattern. There is no memory engine parsing rules; the memory describes the thing in prose, AI applies it at runtime. Applied to managed entities: minimal structured skeleton (identity, persistence, machine contracts) + markdown body (semantics, rules, domain process) + AI as runtime that fuses them.

This isn't a feature. It's the architectural mechanism that makes cross-domain portability possible *without* becoming SQL — and it's the explicit implementation of ARCHITECTURE.md v0.13's gesture: *"closer to knowledge graph + document store with stable references, not Oracle."*

### Evidence: the problem isn't speculative

`extensions/universal/doctypes.yaml` and `references-manifest.yaml` already contain **prose squeezed into YAML block scalars**:

```yaml
# doctypes.yaml — prose stuffed into block scalar
b-plan-begruendung:
  description: >
    Multi-page narrative explanatory document for a Bebauungsplan.
    Document class: scrreprt (KOMA). Engine: pdflatex.

# references-manifest.yaml — expert reasoning in block scalar
- id: BauGB
  notes: |
    Bauleitplanung-Hauptgesetz. §3, §4 Beteiligungen, §10 Beschluss,
    §13 vereinfachtes Verfahren, §13a Innenentwicklung, §13b
    (Wohnnutzung), §214/215 Heilung. Verify §13b is included...
```

The `notes:` field on BauGB **is the rule** — exactly the AI-runtime knowledge ("when does §13a apply", "what to verify in fetched text"). Constrained by block-scalar form: no headings, no structured lists, no links, no examples.

`backend/mcp-server/src/pbs_mcp/project_state.py` (line 1-3 docstring): *"State.md is YAML frontmatter (validated here) + free-form markdown body... append-only by convention; no schema enforcement on it."* The hybrid pattern is **already explicitly articulated for ProjectState** — it just hasn't been generalized.

This decision record generalizes it.

## Decisions

### The principle (named + locked)

> **AI-as-runtime hybrid-shape principle**: Domain semantics, process flow, conditional rules, and contextual knowledge live in **markdown bodies attached to entity files**, not in encoded schemas or hardcoded skill procedures. Cross-domain portability is achieved by AI reading prose, not by abstracting over schema variants. Structured layers are reserved for **interfaces, identity, persistence, and machine contracts**; everything else is prose; AI is the runtime that fuses them at use-time.

The principle is parallel to (not subordinate to) entity-elevation, glue-not-replacement, and pattern-vs-instance. Each catches a different architectural failure mode.

### The three-layer frontmatter contract

Every managed entity, every manifest entry, every doctype declaration follows this shape:

#### Layer 1 — Universal frontmatter (every entity, strict-locked, Pydantic base)

| Field | Type | Purpose |
|---|---|---|
| `id` | str (kebab-case, unique-in-scope) | Stable identity |
| `label` | str | Human-readable name |
| `type` | Literal[doctype, reference, project, client, actor, baustein, process, ...] | Routes to correct Layer-2 Pydantic subclass at gate |
| `scope` | Literal[universal, domain, state, department, office, project] | 4-axis position (per #12 office-vs-department) |
| `scope_key` | str \| None | "Naturschutz" / "MV" / "planning" / null for universal |
| `status` | Literal[active, deferred, stub, archived] | Canonical lifecycle marker |
| `last_updated` | date | Freshness |
| `description` | str \| None | One-liner for listings (optional) |
| `tags` | list[str] | Optional |

#### Layer 2 — Type frontmatter (per-entity-type, strict-locked, Pydantic subclass)

Each entity type extends the universal base with its own type-specific fields. Examples:

```python
class DoctypeEntity(EntityBase):           # type: doctype
    style_ref: str | None = None
    master_file_pattern: str | None = None
    project_subfolder_default: str | None = None
    document_class: str | None = None
    latex_engine: str | None = None
    paired_with: str | None = None

class ReferenceEntity(EntityBase):         # type: reference
    source_url: str
    canonical_path: str
    fetch_method: Literal["web-text", "pdf-fetch", ...]
    last_fetched: date | None = None
    checksum_sha256: str | None = None
    jurisdiction: str
    archive_versions: bool
    chunking_strategy: str
    # ...

class ProjectEntity(EntityBase):           # type: project
    bundesland: StateCode
    verfahren_type: VerfahrenType
    lifecycle: Lifecycle
    phase: str
    departments_active: list[str]
    doctype_status: dict[str, DoctypeStatusValue]
    deadlines: list[Deadline]
    # ... (today's ProjectState fields, relocated)

class ClientEntity(EntityBase):            # type: client
    legal_name: str
    primary_contact: str
    address: Address
    billing_contact: str | None
    default_payment_terms: int
    # ...
```

Doctypes can have their own unique fields. References can have their own unique fields. Each type's frontmatter is locked against its Pydantic subclass; gate validates at read/write.

#### Layer 3 — Per-deployment extension (deferred to #9)

For per-bureau customization (e.g., a specific office wants a custom field on Project for internal review tracking). Three options remain on #9's table — Pydantic subclass per deployment / declared `extra_fields` / `metadata: dict` escape hatch. **This decision record does not pre-empt #9's per-deployment design**; only locks Layers 1 + 2.

### Body conventions (recommended sections, NOT gate-enforced)

Body content is markdown, free-form prose. AI reads it at runtime. Per-entity-type **body specs** document recommended sections; audit + design-review skills check presence and warn on absence — but the gate never rejects a body for missing sections.

Why recommended-not-enforced: hard requirement creates rigidity; entities that don't fit the template get filler text. Same pattern memories already use — feedback memories conventionally have **Why:** + **How to apply:** lines (documented in CLAUDE.md), but no validator enforces it; review/practice does.

| Entity type | Conventional sections |
|---|---|
| `doctype` | `## When this doctype applies` / `## Section conventions` / `## Pairing semantics` (if `paired_with`) / `## Domain-specific deviations` |
| `reference` | `## Why this matters` / `## Key sections for our work` / `## Recent amendments to watch` / `## Common citations` / `## Cross-refs` |
| `project` | `## Context` / `## History` (append-only) / `## Open questions` / `## Decisions` |
| `client` | `## Communication preferences` / `## Billing conventions` / `## Project history summary` / `## Watch-outs` |
| `process` | `## Phase sequence` / `## Required doctypes per phase` / `## Mandatory triggers` / `## Exceptions and shortcuts` |
| `actor` | `## Role + responsibilities` / `## Working preferences` / `## Capabilities + limits` |
| `baustein` | (per existing memory body conventions; out of scope) |

Body specs live at `docs/conventions/entity-md-spec.md` (one section per entity type). Created during #9 implementation alongside the Pydantic schemas.

### Where conditional rules live (the "Umweltbericht required when §13a doesn't apply" question)

Resolved: **rules about *when* something applies belong with the *process*, not with the entity itself.**

- The doctype's md describes what the doctype IS (its sections, its pairing semantics, its style conventions).
- The process md (per verfahren type) describes the **flow** + **which doctypes the flow produces**.
- The project entity's body is per-instance narrative, not rules.

Worked example: `extensions/department/planning/processes/regelverfahren.md` declares its phase sequence + the doctypes required per phase including Umweltbericht. `beschleunigtes.md` (§13a) declares its phase sequence WITHOUT Umweltbericht. Project state references `verfahren_type: beschleunigtes`; orchestrator loads the matching process md to know what doctypes are required.

This is **process-as-md, not state-machine-as-data**. AI reads the process md to reason about "what's next", "what's missing", "what's required given the current state."

### MCP gate semantics (generalization to #9)

Today: per-entity tools (`read_project_state`, `write_project_state`; AuditEvent has its own write path).

Tomorrow (per this decision, implementation in #9): **generic entity gate** with type-dispatch.

```python
def read_entity(path: Path) -> EntityFile:
    """Parse + validate any entity file. Type field routes to subclass."""
    # 1. Parse frontmatter; require `type:` field
    # 2. Dispatch to Layer-2 Pydantic subclass per `type:`
    # 3. Validate Layer-1 + Layer-2 fields strictly (fail-loud)
    # 4. Body returned as raw markdown; no schema check
    ...

def write_entity(path: Path, entity: EntityFile) -> None:
    """Write validated entity. Round-trip parse before write."""
    ...
```

Single tool, type-dispatch, replaces the per-entity-tool sprawl. Body preserved as-is across read/write cycles (same shape state.md uses today). Reuses the `parse_state_file` / `serialize_state_file` pattern at `project_state.py`, generalized.

This is the **gate generalization** the side-note flagged. Lives in #9's scope.

### Strictness summary

| Layer | Lock-down | Enforced by |
|---|---|---|
| Universal frontmatter (Layer 1) | STRICT (fail-loud) | MCP gate (Pydantic base) |
| Type frontmatter (Layer 2) | STRICT (fail-loud) | MCP gate (Pydantic subclass per type) |
| Per-deployment extension (Layer 3) | TBD per #9 | TBD per #9 |
| Body conventions (recommended sections) | RECOMMENDED (warn) | Audit skill + design-review skill (NOT gate) |
| Body free prose | UNCONSTRAINED | — |

## Worked examples — per-entity decomposition

### Example 1 — Doctype: `b-plan-begruendung`

**Today** (`extensions/universal/doctypes.yaml`, prose-in-block-scalar):

```yaml
b-plan-begruendung:
  label: "B-Plan Begründung"
  description: >
    Multi-page narrative explanatory document for a Bebauungsplan.
    Document class: scrreprt (KOMA). Engine: pdflatex.
  style_ref: memory/universal/style/style-spec.md#doctype-a-begruendung
  master_file_pattern: "B-Plan Begründung.tex"
  project_subfolder_default: B-Plan/Begründung
  paired_with: b-plan-festsetzungen
```

**After migration** (`extensions/universal/doctypes/b-plan-begruendung.md`):

```markdown
---
id: b-plan-begruendung
label: "B-Plan Begründung"
type: doctype
scope: universal
scope_key: null
status: active
last_updated: 2026-04-29
style_ref: memory/universal/style/style-spec.md#doctype-a-begruendung
master_file_pattern: "B-Plan Begründung.tex"
project_subfolder_default: B-Plan/Begründung
paired_with: b-plan-festsetzungen
document_class: scrreprt
latex_engine: pdflatex
---

# B-Plan Begründung

Narrative explanatory document for a Bebauungsplan. Pairs structurally
with Festsetzungen — Begründung explains the *why*, Festsetzungen state
the *what*.

## When this doctype applies

Required for every Bebauungsplan regardless of Verfahren type. Even
§13a beschleunigtes Verfahren produces a Begründung — only the
Umweltbericht is dropped.

## Section conventions

Standard order:
1. Anlass und Erforderlichkeit
2. Geltungsbereich und Bestand
3. Planungsziele
4. Planungsrechtliche Festsetzungen (mirrors Textteil B; cross-refs each)
5. Umweltprüfung / Umweltbericht (omitted in §13a)
6. Auswirkungen auf private Belange
7. Kosten / Bodenordnung
8. Verfahrensablauf

## Pairing semantics

`paired_with: b-plan-festsetzungen` is enforced at draft time: every
project drafting one must produce the other. `review-draft` cross-checks
section 4 of Begründung against Festsetzungen sections.

## Verfahren-specific deviations

- §13a (beschleunigtes): Umweltbericht section dropped entirely
- §12 (vorhabensbezogen): section 4 expands with Durchführungsvertrag references
- §13 (vereinfachtes): structurally identical to Regelverfahren
```

### Example 2 — Reference: `BauGB`

**After migration** (`extensions/universal/references/BauGB.md`):

```markdown
---
id: BauGB
label: Baugesetzbuch
type: reference
scope: universal
scope_key: null
status: active
last_updated: 2026-04-29
source_url: https://www.gesetze-im-internet.de/baugb/
canonical_path: gesetze/bund/BauGB.txt
fetch_method: web-text
last_fetched: null
checksum_sha256: null
archive_versions: true
retention_versions: 5
ingest: true
chunking_strategy: per-paragraph
chunk_metadata_extractor: gesetze-im-internet
jurisdiction: bund
tags: [bauleitplanung, federal-baugb, kernel]
---

# Baugesetzbuch (BauGB)

Bauleitplanungs-Hauptgesetz. The federal foundation for every B-Plan
in Germany.

## Why this matters

The BauGB is the primary legal basis we cite in Begründung,
Festsetzungen, and procedural correspondence. Every B-Plan project
references at least §1 + §3 + §4 + §10; §13a-Verfahren projects add §13a.

## Key sections for our work

- **§1 Aufgabe der Bauleitplanung**: foundational — opens most Begründungen
- **§3 Beteiligung der Öffentlichkeit**: triggers + frist conventions
- **§4 Beteiligung der Behörden**: TöB process; pairs with our send-skill
- **§10 Beschluss des Bebauungsplans**: closing rite of Verfahren
- **§13 vereinfachtes Verfahren**: skips Umweltbericht; tighter scope
- **§13a Innenentwicklung**: beschleunigtes Verfahren; Umweltbericht dropped
- **§13b Wohnnutzung**: 2024 reintroduction — verify present in fetched text
- **§214/215 Heilung**: error-correction provisions; relevant for late-stage review

## Recent amendments to watch

- 2024 §13b reintroduction (post-Wohnungsneubau-Beschleunigung). Older
  fetched text may be missing this — verify on every refresh.

## Common citations

In Begründung section 1: "Gemäß §1 Abs. 3 BauGB sind Bauleitpläne
aufzustellen, sobald und soweit es für die städtebauliche Entwicklung
und Ordnung erforderlich ist."

In §13a-Begründung: "Das Verfahren wird gemäß §13a BauGB im
beschleunigten Verfahren durchgeführt; eine Umweltprüfung nach §2 Abs.
4 BauGB entfällt..."

## Cross-refs

- BauNVO.md — implementing regulations; §11 SO-Gebiete + §19 Grundfläche
- ROG.md — übergeordnete Raumordnung
- UVPG.md — UVP-Pflicht; relevant for §13a-Ausschluss
```

### Example 3 — Adapter-mode entity: `Invoice` via Lexware

**After #11 + #15 implementation** (`extensions/department/invoicing/entities/invoice.md`):

```markdown
---
id: invoice
label: Invoice (Lexware-managed)
type: entity_definition
scope: department
scope_key: invoicing
status: active
last_updated: 2026-XX-XX
mode: adapter
adapter: lexware
adapter_config_ref: office-config.departments.invoicing.entities.invoice.config
capabilities: [read, create, update]
---

# Invoice (this office's Lexware setup)

Invoices for this bureau live in Lexware. PBS interacts via the
Lexware adapter; PBS itself doesn't store invoice content.

## How this office uses Lexware

- One Lexware "project" per PBS project_id (mapped via adapter config)
- Invoice line items follow Vorgang-by-Vorgang structure
- Default payment terms 30 days net; client overrides honored

## Edge cases

- Retainer invoices are NOT in Lexware; tracked in Excel and reconciled
  monthly. Adapter does NOT see them — out-of-system on purpose.
- Foreign-client invoicing (rare) goes via separate manual process; do
  not auto-issue via adapter.

## Mapping to PBS concepts

| PBS concept | Lexware field | Notes |
|---|---|---|
| `project_id` | `project.code` | 1:1 |
| `client_id` | `customer.id` | resolved via Client entity lookup |
| `Vorgang` | `line_item.description` prefix | convention, not enforced |

## Communication conventions

- Maxsolar prefers PDF email attachment
- Solarfaktor uses portal upload (not yet automated)
```

The body becomes the natural home for **per-deployment customization of how an office uses an external system** — the texture humans currently keep in their heads, now explicit and AI-readable.

## Pattern-vs-instance check

Per ARCHITECTURE.md "Pattern-vs-instance discipline" — the principle must work at pattern level, not just for PBS.

| Domain | Does the principle work? |
|---|---|
| **Legal practice** | Yes. Cases get state.md-shape; precedents become reference entities (md per case); doctypes become brief/motion/exhibit types; processes describe filing flow. Same shape, different prose. |
| **Research-paper review** | Yes. Manuscripts get state.md-shape; citations become reference entities (md per cited work); doctypes become review-letter/decision-letter types; processes describe submission/revision flow. |
| **Engineering-doc workflows** | Yes. Specs get state.md-shape; standards/RFCs become reference entities; doctypes become design-doc/ADR/runbook types; processes describe lifecycle from draft → review → ratified. |

The principle generalizes cleanly. Cross-domain portability is achieved through prose, not schema abstraction.

## Defers — re-examined session 15 under v0.33 no-defer principle

> **Session 15 amendment**: re-examined the 6 entries below. Result: D2 (gate-level selective section read) is a valid watch-list entry — names specific external signals (median entity body > 1500 tokens OR any single entity body > 4000 tokens routinely; audit slice 21 telemetry fires the trigger). D1, D3, D4, D5, D6 are phase routing (work scheduled to #9 / Phase 1 corpus / audit ripple / design-review ripple per ROADMAP queue), not chronological gaps. Per v0.33 preliminary-lock: this DR remains preliminary-locked. Original entries kept below as historical record.

| Defer | Home | Specific cost being avoided |
|---|---|---|
| **D1**: Per-deployment extension fields (Layer 3 design) | #9 (Pattern-vs-instance + managed-entity concept) | This DR doesn't pre-empt #9's per-bureau customization design; over-deciding now would lock the wrong customization mechanism without #9's full schema work |
| **D2**: Gate-level selective section read (e.g., `read_entity(path, sections=["When this applies"])` returns only that section's bytes) | Folds into #9 gate work when triggered. **Sharper trigger**: revisit when median entity body > 1500 tokens OR any single entity body > 4000 tokens routinely. Whichever fires first. | Today bodies don't exist on disk yet (no migrations done); even after migrations, bodies start small. Optimization without measurement = wrong design. Capability already exists today via section-anchor convention + AI reading whole body and focusing on named section. **D2 is a context-cost optimization, NOT a capability gap.** Audit slice 21 adds body-size telemetry sub-check; trigger fires when telemetry says it's needed. Mitigations (section-size + body-size guidance, pruning norm, anchor-and-grep technique) documented in entity-md-spec.md §16 to keep bodies small enough that trigger ideally never fires. |
| **D3**: Migration of `extensions/universal/doctypes.yaml` → per-entity md files | #9 (doctypes-manifest generalization) | #9 already addresses doctypes manifest as part of department-module contract; bundling avoids two passes over same files |
| **D4**: Migration of `extensions/{universal,domain,state}/references-manifest.yaml` → per-reference md files | Phase 1 corpus work | research-references skill already touches references-manifest; migration is cleaner bundled with the corpus full-refresh that exercises every entry |
| **D5**: Audit slice 21 (entity-md frontmatter + body-section conformance scan) implementation | Audit skill update; bundled with #9's audit ripple | Implementation needs entity gate to exist; gate lands in #9; slice can run dry pre-#9 but has nothing to scan |
| **D6**: Design-review target 12 (entity authoring conformance check) implementation | Design-review skill update; bundled with #9's design-review ripple | Same dependency on entity gate existence |

Each defer names a specific home + a specific cost being avoided. Per `feedback_defer_instinct.md`: not generic YAGNI; honest defers.

## Downstream constraints

### → #11 (Cowork integration deep refactor)

- `extensions/department/<dept>/department.yaml` file format **adopts hybrid-shape**: md+frontmatter, NOT pure YAML. Frontmatter declares `event_subscriptions:`, `managed_entities:` registry, department-level config; body describes department character + conventions in prose.
- Skill frontmatter sweep (per #12): when sweep adds `department:` field, also adopts hybrid-shape principle for any new declarative fields.
- Slash command namespacing unaffected.

### → #15 (Client + Actor as office-level managed entities)

- Client + Actor entity definitions land **as md files** at `extensions/office/entities/client/<client-id>.md` and `extensions/office/entities/actor/<actor-id>.md`.
- Frontmatter follows Layer-1 + Layer-2 contract (Layer-2 schema spec'd here for both types).
- Body conventions per the table above (`## Communication preferences` / `## Billing conventions` / etc. for Client; `## Role + responsibilities` / etc. for Actor).
- Cross-department reference convention (`<entity>_id: str` fields in Layer-2 frontmatter) unchanged.

### → #9 (Department module contract + managed-entity concept)

- The hybrid-shape principle is **central design lens** for #9's managed-entity concept work.
- **Generic entity gate** (`read_entity` / `write_entity` with type-dispatch) lands here. Replaces sprawl of per-entity tools.
- **Body specs document** (`docs/conventions/entity-md-spec.md`) authored alongside Pydantic Layer-2 subclasses.
- ProjectState refactor: when relocated to `extensions/department/planning/entities/project.py`, also publish corresponding body-spec section.
- **Migration of doctypes.yaml** (D3) executes here.
- **Per-deployment customization mechanism** (D1) decided here.

### → #6 (Audit-trail v2 retrofit)

- Audit events remain Pydantic-shaped (interface contract — rightly structured). Hybrid-shape principle does NOT touch AuditEvent format.
- Gate-side conformance: when retrofit adds `actor_kind` + `department:` filtering, also verify entity-write events route through the new generic gate (post-#9).
- `details` payload may surface markdown for free-form fields (e.g., `reasoning_full_text`); minor, not load-bearing.

### → Audit skill (new slice 21)

- Scan `extensions/**/*.md` entity files for Layer-1 + Layer-2 frontmatter conformance.
- Scan body for presence of recommended sections per the body-spec for the entity's `type:`.
- Warn on missing sections; don't fail (recommended-not-required).
- Implementation bundled with #9 (D5).

### → Design-review skill (new target 12)

- When authoring or modifying an entity md, validate Layer-1 + Layer-2 frontmatter against the appropriate Pydantic subclass.
- Suggest missing recommended body sections.
- Catch over-elevation (entity without stable-identity + state + lifecycle should be a memory entry, not an entity — coordinates with entity-elevation discipline target 11).
- Implementation bundled with #9 (D6).

### → Phase 1 corpus work (D4 migration)

- `research-references` full refresh migrates references-manifest entries to per-reference md files.
- Bundled with the corpus fetch + checksum + manifest-population pass that already touches every entry.

## Connection to existing architectural disciplines

| Discipline | Connection |
|---|---|
| **Entity-elevation** | Hybrid-shape applies AFTER 3-test verdict. Entity-elevation says "don't over-elevate"; hybrid-shape says "for things that DO elevate, here's their shape." |
| **Pattern-vs-instance** | Hybrid-shape IS how cross-domain portability is achieved. Same shape (frontmatter + body), different prose per domain. |
| **Glue-not-replacement** | Adapter-mode entities use the same hybrid-shape contract; per-deployment markdown body is the natural home for "how does THIS office use the external system." |
| **Strict-validation (meta-rule 4 corollary)** | Layer 1 + Layer 2 frontmatter respect strict-validation: required fields fail-loud, no silent defaults. Body is unconstrained by design — that's the principle. |
| **Source-of-truth (meta-rule 3)** | Hybrid-shape doesn't change source-of-truth placement; it changes **how** source-of-truth content is shaped (when content is semantic/process rather than identity/config). |

## Connection to VISION

The principle is the architectural expression of VISION axis 1 (intertwining-AI-workflow). AI is not a feature of the system; it is the runtime that fuses the layers. Without AI as runtime, the markdown bodies are inert prose; with AI as runtime, they ARE the rules + process + domain knowledge.

This is also why memory drift toward oracle-mode framings shows up as architectural drift toward over-structuring: when AI is treated as a passive answerer (oracle), the architecture compensates by encoding rules in schemas. When AI is treated as a workflow participant (intertwining axis), the architecture relies on AI to read prose. The hybrid-shape principle locks in the latter.

## Open questions (not blocking)

1. **Section-addressable bodies** (D2): if entity bodies grow large, do we adopt explicit section conventions (h2 = top-level, h3 = sub-sections) so AI can selectively read sections? Defer until pain. Likely yes when entity bodies > ~2000 tokens regularly.
2. **Body-spec versioning**: when body-spec for an entity type changes, how do existing entities migrate? Probably "next-edit migrates"; defer to first time body-spec actually changes.
3. **Stale-content detection in bodies**: prose can drift (notes about laws become outdated). Audit skill should scan; specifics deferred to first audit ripple.

## Revisit triggers

Re-open this decision record if:

- A real second-domain implementation reveals the principle creates rigidity for that domain (signal that hybrid-shape is itself too PBS-coupled).
- Section-addressable bodies become urgent before #9 lands (forces D2 forward).
- A managed entity type emerges that genuinely doesn't fit hybrid-shape (interface contract requiring all-structured; or content-heavy enough to warrant a different storage shape).

None expected pre-RAG.
