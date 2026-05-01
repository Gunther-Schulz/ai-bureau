---
id: planning-document-work
label: Planning Document Work
type: specialist
status: active
last_updated: 2026-05-01

framework_kind: specialist
framework_key: planning-document-work

display_name: Planning Document Work
semver: "0.1.0"

composability_axes:
  - FROM
  - IN
  - WITH
  - ACROSS
  - OVER

classification: domain_anchored

skills_bundled:
  - orchestrator
  - draft-textteil-b
  - draft-textteil-c
  - review-draft
  - save-baustein
  - validate-bausteine
  - validate-checklist
  - validate-latex-style
  - verify-citations
  - research-references
  - record-feedback
  - draft-cover-mail
  - survey-project
  - promote-to-skill
  - watch-list

entity_types_owned:
  - planning-document-work.process
  - planning-document-work.project-deadline
  - planning-document-work.module-decision

references_required:
  - universal.reference.BauGB
  - universal.reference.BNatSchG
  - universal.reference.BauNVO
  - universal.reference.UVPG
  - universal.reference.ROG

memory_required:
  - memory/universal/style/style-spec.md
  - memory/universal/conventions/korrektur-rules.md
  - memory/universal/verfahren/bauleitplanung-phasen.md
  - memory/universal/conventions/baustein-format.md
  - memory/universal/conventions/state-format.md

adapters_consumed: []

shapes_supported:
  - practitioner
---

# Planning Document Work

## What this specialist is for

The planning-document-work specialist is the **PBS pioneer specialist DEFINITION** — the codified expertise bundle for German planning bureau (Planungsbüro) document work. It is the canonical reference implementation of the Specialist primitive (per `terminology-and-specialist-primitive.md` #22 Sub-DR A), Framework C category (per `entity-md-scope-model-restructure.md` v0.34).

Domain scope: produces and reviews planning documents required under German Bauleitplanung (B-Plan) processes — Begründungen, Textliche Festsetzungen, Umweltberichte, various Gutachten. The specialist orchestrates the full document lifecycle: drafting, source-grounded citation, layered review, send to authorities (UNB / Behörden / höhere Verwaltungsbehörde), feedback capture, revision.

PBS-Schulz workspace employs this specialist as its primary specialist (per `workspace.md.specialists_employed: [planning-document-work, ...]`). Future Schulz workspace will also employ project-management + invoicing specialists per the eventual full-bureau composition. Other planning bureaus deploying PBS infrastructure will employ this same specialist DEFINITION (cross-workspace reuse per `composability_axes: ACROSS`).

## Composability axes

This specialist exhibits all 5 composability axes per #22 Sub-DR A:

- **FROM (downward)** — bundles 15 skills + 3 process entity types + 5 references + 5 memory entries. Each is a smaller primitive composed into the specialist.
- **IN (upward)** — workspaces EMPLOY this specialist via `workspace.md.specialists_employed: [planning-document-work]`. PBS-Schulz workspace is the pioneer.
- **WITH (lateral)** — coordinates with other specialists (project-management, invoicing) via AuditEvent + `event_subscriptions` per event-coordination Protocol. E.g., when planning-document-work emits `phase_advanced`, project-management subscribes for deadline-tracking propagation.
- **ACROSS (cross-workspace)** — deployable to any planning bureau workspace (Schulz Planungsbüro Berlin, hypothetical Müller Planungsbüro München, etc.). Each workspace has independent state instance; specialist DEFINITION shared.
- **OVER (optional grouping)** — workspace MAY group via `groupings: dict[str, list[<specialist-id>]]`. PBS-Schulz uses "departments" grouping convention; planning-document-work is grouped under `departments.planning-document-work`.

## Skills bundled

15 skills compose this specialist:

| Skill | Role |
|---|---|
| `orchestrator` | Workspace-level routing and decision surfacing; PROCEDURE.md checkpoints |
| `draft-textteil-b` | Drafts Begründung documents (Teil B) |
| `draft-textteil-c` | Drafts Textliche Festsetzungen (Teil C) |
| `review-draft` | Layered review (structural / fachlich / formal); produces ReviewOutput with counter-argument + confidence + reasoning |
| `save-baustein` | Captures reusable text fragments (bausteine) into memory |
| `validate-bausteine` | Sweeps bausteine for staleness against current reference state |
| `validate-checklist` | Doctype-specific structural validation |
| `validate-latex-style` | Style-spec compliance check |
| `verify-citations` | Source-grounding contract enforcement; verify legal citations against current reference text |
| `research-references` | Fetches/updates legal references; flags downstream entities affected |
| `record-feedback` | Captures external feedback (UNB rejections, approvals, suggestions) |
| `draft-cover-mail` | Transmittal cover mail (Anschreiben) for sending artifacts to authorities |
| `survey-project` | First-bind project structure interpretation when no `_ai/` folder yet |
| `promote-to-skill` | Promotes frequently-used bausteine to dedicated skills |
| `watch-list` | Periodic tracking of pending items + freshness sweeps |

Skills live at `extensions/framework/specialists/planning-document-work/skills/<skill-name>/SKILL.md` post-#11 single-touch refactor (filesystem migration from `plugin/skills/<name>/`).

## Entity types owned

This specialist owns 3 Owner B entity types (entities scoped to a specialist instance per v0.34 three-category model):

- **`planning-document-work.process`** — Verfahren-type process entities (regelverfahren / beschleunigtes / etc.); declares phase sequence + required doctypes per phase + mandatory triggers + exceptions
- **`planning-document-work.project-deadline`** — per-project deadline entities tracking Fristen for Stellungnahmen + Bekanntmachungen + send dates
- **`planning-document-work.module-decision`** — per-section AI inclusion/exclusion decision logs (capture reasoning when AI includes/excludes optional sections; reviewable later per VISION axis 3 defensibility test)

Entity TYPE namespacing per entity-md-spec §3.2: `<specialist-id>.<entity-type>` for Owner B specialist scope. Entity INSTANCES live within the specialist's deployed instance directory at workspace level.

## Required references

5 universal-scope legal references (Layer A category, scope=universal):

- **BauGB** — Baugesetzbuch (federal building code; primary reference for B-Plan procedures)
- **BNatSchG** — Bundesnaturschutzgesetz (nature protection law; relevant for Naturschutz-domain projects)
- **BauNVO** — Baunutzungsverordnung (land use ordinance)
- **UVPG** — Gesetz über die Umweltverträglichkeitsprüfung (environmental impact assessment)
- **ROG** — Raumordnungsgesetz (spatial planning act; Land-level interface)

Plus domain-specific references (Layer A scope=domain) when active scope domain matches: PV-FFA references, Wind references, Naturschutz references, Innenentwicklung references. Plus state-specific references (Layer A scope=state) when active scope state matches: per-Bundesland legal supplements.

References fetched + maintained via `research-references` skill; freshness tracked via `references_used:` frontmatter on memory bausteine; invalidation propagation per Meta-rule 3 (source-of-truth + invalidation contract).

## Memory dependencies

5 universal memory entries (cross-cutting authored prose consumed across specialist's skills):

- **`memory/universal/style/style-spec.md`** — LaTeX styling spec for B-Plan doctypes
- **`memory/universal/conventions/korrektur-rules.md`** — German writing conventions (Hyphenation, number formatting, quotation conventions)
- **`memory/universal/verfahren/bauleitplanung-phasen.md`** — BauGB process phase semantics + required artifacts
- **`memory/universal/conventions/baustein-format.md`** — Format spec for memory bausteine
- **`memory/universal/conventions/state-format.md`** — Format spec for per-project state.md (project entity Layer 2)

Specialist-scope memory bausteine (specialist-internal expertise patterns; not universal) live at `extensions/framework/specialists/planning-document-work/memory/<baustein>.md` per #22 Sub-DR A bundling principle (specialist owns its memory; distribution unit self-contained).

## Cross-archetype vs domain-anchored classification reasoning

`classification: domain_anchored` — this specialist is anchored to the German planning bureau archetype:

- Document doctypes (Begründung, Festsetzungen, Stellungnahme) are German-planning-specific
- Legal references are German federal + state law
- Verfahren process types reference BauGB-specific phases
- Style conventions are German (Hyphenation rules, number formatting like "1.234,56")
- Authority structure (UNB, Behörden, höhere Verwaltungsbehörde) is German administrative

A hypothetical legal-practice deployment would have a DIFFERENT specialist (`legal-research` or `litigation` per #22 Sub-DR A worked examples) with its own domain-anchored content. The skills shape (drafting + reviewing + verifying citations + capturing memory + scheduled triggers) is COMPOSITIONALLY SIMILAR but CONTENT-DIFFERENT.

Cross-archetype specialists in this framework (per #22 Sub-DR A two-tier classification): `citation-verification`, `layered-review-framework`, `brand-voice` — these reuse compositionally across multiple archetypes. The planning-document-work specialist could potentially decompose into a domain-anchored core + several cross-archetype sub-specialists, but per session-15 #22 Sub-DR A D5 reframe (composite specialist not supported in v1; flat employed-list only), this decomposition is a v2+ exercise.

## Adapter dependencies

`adapters_consumed: []` — no adapter dependencies in v1. Planning-document-work is fully native: PBS owns the system-of-record for Project entities, doctype manifests, references, decisions.

Future adapter dependencies may emerge:
- **Civil Engineering CAD adapter** (per ROADMAP v1.x-v2 — Python-ACAD-Tools integration): if planning bureau uses CAD tools for drawing, adapter could bridge geometry-state into B-Plan attachments
- **Behördenschnittstelle adapter** (hypothetical EU/Bund e-government portal): if German authorities deploy submission portals beyond email, adapter could automate transmission
- **Prüfingenieur portal adapter** (hypothetical): if technical-review portals emerge, adapter for delegation

When concrete adapter need surfaces (per glue-not-replacement principle v0.15), specialist's `adapters_consumed` list grows.

## Cross-references

- `docs/decisions/terminology-and-specialist-primitive.md` (#22 Sub-DR A) — Specialist primitive definition; 5 composability axes; granularity 3-test; classification two-tier
- `docs/decisions/entity-md-scope-model-restructure.md` (v0.34) — Framework C category for specialist DEFINITIONS; specialist's dual-nature (DEFINITION = Framework C; SCOPE = Owner B for entities owned within instance)
- `docs/decisions/positioning-three-tier-framework.md` (#22 Sub-DR B) — three-tier framing; specialist as Tier 3 marketplace primitive
- `VISION.md` — practitioner-shape thesis; this specialist serves practitioner workspaces
- `docs/decisions/ai-as-runtime-hybrid-shape.md` (#16) — hybrid-shape contract; this specialist's content is markdown-bodied at runtime
- `docs/conventions/entity-md-spec.md` §4 specialist entry — Layer 2 schema; §6 body conventions
