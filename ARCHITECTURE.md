# pbs-bureau architecture — what goes where

This document is the canonical placement reference. When in doubt
about where new content belongs, walk the **three decision rules**
below. Meta-rules establish principles; the decision rules apply
them.

> **Vision anchor.** PBS is built on three interlocking principles:
> **intertwined-AI-workflow (not tacked-on features)**, **sparring
> partner (not answer machine)**, and **authorship preservation
> (the user remains defensible expert author of everything PBS
> produces on their behalf)**. The architecture serves continuous
> human-AI collaboration with built-in challenge in service of
> defensible output — persistent state, orchestrated behaviors,
> source-grounded outputs, surfaced decisions, explicit human-
> authority gates, counter-arguments, calibrated confidence,
> selective friction. See `VISION.md` for the full thesis.

Status: **v0.6 (post-session-6 boundary refinement)**.

- v0.1 → v0.2: nine entity types + 6 decision rules.
- v0.2 → v0.3: scope-orthogonality live, layered manifests in
  repo, integration adapter scaffolding deployed, schema migration
  framework in place.
- v0.3 → v0.4: execution-locality meta-rule (skills declare
  `mcp_tools_required[]`; `settings.json` permissions; hooks
  deferred).
- v0.4 → v0.5: design-review-driven simplification. **5 meta-rules
  → 4 + 1 named convention**: integration-adapter demoted to corollary
  of app-vs-office; scope-orthogonality demoted to layering convention;
  execution-locality renamed to execution-determinism; new
  source-of-truth & invalidation meta-rule added. **9 entity types
  → 5**: A+B merged into Skill Bundle; G+H merged into Configuration;
  I demoted (it's an internal pattern of E, not a peer). A-I letter
  scheme dropped — names speak for themselves. **6 decision rules
  → 3** audience-first.
- **v0.5 → v0.6**: meta-rule 4 sharpening. **(A) Persistence-layer
  boundary refined**: the rule applies to durable state with a *typed
  contract* (Pydantic model + loader + cross-reference invariants),
  not to all files indiscriminately; loose markdown is skill-direct.
  **(B) Reuse direction made explicit**: shared deterministic logic →
  MCP tool; shared interpretive logic → Skill Bundle reference. The
  audit's slice 14 + design-review's target 7 land on this sharpened
  boundary.

> **Scope boundary.** This doc covers placement (which entity type /
> where). For *within-tier idioms* (how to write the thing once
> you've decided where it goes) see:
>
> - `docs/plugin-conventions.md` — Skill Bundle idioms (frontmatter,
>   semver, body patterns, references organization, routing
>   handoffs).
> - `docs/backend-conventions.md` — Backend idioms (test layout,
>   logging, MCP error format).
>
> Conventions docs trace decisions back here but never re-litigate
> placement.

## Maintenance discipline

A 3-line checklist:

1. Every meta-rule change, schema bump, or significant refactor
   lands in the same commit as the ARCHITECTURE.md update.
2. After meta-rule additions / refactor sweeps, run `audit` (drift
   detection) and `design-review` (soundness review) — see
   `plugin/skills/{audit,design-review}/`.
3. Sunset deprecated concepts via the deprecation procedure (below).

### Deprecation procedure

When retiring a concept (entity type, meta-rule, MCP tool name,
skill, etc.):

| Concept | Procedure |
|---|---|
| **Skill** | Bump major + add `deprecated: true` to frontmatter; remove after 1 plugin release. Document successor in description. |
| **MCP tool** | Alias old name → new for one minor version of pbs-mcp; remove after that. |
| **Entity type** | Pre-launch (now): rewrite ARCHITECTURE.md + sed across repo in one commit. Post-launch: announce in HANDOFF, add to deprecated-concepts list, give 1 release deprecation window. |
| **Meta-rule** | Reformulate in-place with explicit replaces-X note. Audit + design-review on next refactor verifies the replacement holds. |
| **Office-config field** | Bump schema_version + write migration that drops the field; existing offices forward-migrate transparently. |

Pre-launch / pre-distribution: deprecation is essentially
free — change in place. After first user-facing release the
procedure tightens.

---

# Meta-rules

The architecture rests on **four meta-rules**. Plus one named
convention (scope-orthogonality) that applies *within* layered
content. New content goes through the relevant meta-rule before
placement.

## Meta-rule 1: app vs office (deployment portability)

The repository is **a generic German planning-bureau workflow app**
that any Planungsbüro can deploy. It is not a PBS-specific instance.
Per-deployment configuration — paths, identity, actors, styling,
state-law extensions — lives **outside the repo** in an
`office-config.yaml` resolved via:

1. `$PBS_OFFICE_CONFIG` (env var, takes precedence)
2. `${XDG_CONFIG_HOME}/pbs-bureau/office.yaml`
3. `~/.config/pbs-bureau/office.yaml`

Schema: `docs/office-config.schema.yaml`. Generated interactively by
the `setup-office` skill on first run.

**Hard rules for app code (skills, backend, hooks, memory):**

- Never hardcode hidrive/projects/state paths. Read them from
  `roots.*` in the loaded office-config.
- Never hardcode office identity (name, address, signature, phone,
  email). Read them from `office.*` (post-v3 merge of identity into
  office).
- Never hardcode actor names. Read `actors[]` from config (kind=internal
  for practices, kind=external for partners).
- Never hardcode client/project names. Use neutral examples in docs
  (`YY-NN <Client> - <Location>`); refer to live projects only via
  paths the user provides at runtime.
- State-specific and domain-specific references are discovered by
  walking `<repo>/extensions/{universal,domain/<X>,state/<X>}/`
  filtered by the office's `scope.{domains,states}` (loader walks
  the union; manifests are NOT enumerated in office-config).
  Bundesland is a per-PROJECT property (`state.md.bundesland`), not
  an office property.
- LaTeX styling lives in the office's `office-style.sty`, NOT in
  app skeletons or classes.
- Office identity macros (`\OfficeName`, `\OfficeAddressLines`,
  `\OfficeSigner`) are auto-generated by the backend from `office.*`
  before each compile, NOT hand-written.

### Mechanism: pluggable integration adapters

Where the app interfaces with external systems whose mechanism
varies per deployment (email service, calendar, scanner, phone,
accounting, DMS, GIS, etc.), the implementation lives behind a
small **protocol + adapter pattern**: a Python `Protocol` defines
the contract; each adapter (`thunderbird-maildir`, `imap`, `caldav`,
etc.) implements it; office-config selects which adapter is active
per class.

Same architectural lesson as paths/identity/actors/scope: no
hardcoded mechanism. The adapter boundary is in place from day one;
concrete adapters land per demand. Adapters live at
`backend/mcp-server/src/pbs_mcp/integrations/<class>/<adapter>.py`,
each exporting an `Adapter(config: dict)` class implementing the
protocol at `<class>/protocol.py`. `load_adapter(class_name)`
resolves via `cfg.find_integration(class_name)` (v3 free-form
list).

The class set is open — any string is valid as long as a matching
subpackage exists. (Per design-review: integration adapters are
*backend-internal organizing pattern*, not a top-level meta-rule
peer; they're a consequence of app-vs-office deployment portability.)

**Schema versioning + migrations.** Adding fields to office-config
schema requires bumping `CURRENT_SCHEMA_VERSION` in
`backend/.../office_config.py` and adding a migration at
`backend/.../office_config_migrations/v<N>_to_v<N+1>.py`. The
dispatcher applies migrations sequentially in-memory on every load.

## Meta-rule 2: memory vs RAG (citation freshness)

A hard line: **what lives in memory** vs **what lives in the RAG
corpus**. The split protects against legal-citation rot.

**Memory** (loaded into context every session) holds:
- Workflow logic — phase order, phase→state mapping, doctype structure.
- Conventions — German number formatting, quotation conventions,
  hyphenation rules, korrektur-rules.
- Reference content (project-structure.md, per-project-memory
  format docs).
- Saved bausteine.
- Universal reasoning patterns that don't depend on current law text.

(Note: doctype + reference registries are NOT memory — they're
layered manifests in `extensions/`. Memory holds prose conventions
and saved instance records.)

**RAG** (`<roots.references>/`, retrieved on demand via
`search_corpus` / `read_corpus_file`) holds:
- Verbatim legal text (BauGB §X, BNatSchG §Y, etc.).
- Verbatim Verfahrensvermerk wording.
- Court ruling text.
- Leitfaden content from publishing bodies (KNE, LUNG, etc.).
- Anything that can be amended at the source.

**§-references as labels are allowed in memory** ("Phase 5a —
§3 Abs.2 BauGB") for navigation. Verbatim legal text and paraphrased
law-text are NOT — those route through RAG.

**Source-grounding rule.** Any legal citation in produced output
(drafts, reviews, mails) must be backed by a tool result — even if
the same §-number appears in memory. Memory's role is naming and
navigation, never authoring. The §-label "§3 Abs.2 BauGB" appearing
in memory does NOT satisfy the citation-evidence requirement when
drafting.

## Meta-rule 3: source-of-truth & invalidation

Every entity declares its invalidation contract: how the system
detects that this thing is stale, superseded, or wrong, and what
needs to happen when it is.

**Per entity type** (see "The five entity types" below for full
list):

| Entity | Invalidation contract |
|---|---|
| Skill Bundle | semver `version:` field; bump on behavior change. Body changes invalidate skill behavior on `/reload-plugins`. |
| Memory (prose) | `references_used: []` frontmatter declares dependent law refs. `research-references` flags affected docs in `memory/product-backlog.md` when a referenced law is updated. |
| Memory (records) | `status: active|flagged|archived|superseded`, `last_validated`, `review_due`, `references[].verified_against_version`. `validate-bausteine` sweeps for stale records. |
| Backend | Python imports + Pydantic schemas; restart MCP server after changes. No declarative invalidation hook. |
| Configuration | `schema_version` + migration framework. Manifests carry `last_updated` + per-entry `last_fetched` + `checksum_sha256`; `research-references` re-fetches on schema/source change. |
| External data | Per-project `_ai/state.md.lifecycle` declares phase + status; `roots.references_root` corpus carries `changelog.md`. |

**Cross-cutting concern handler.** `research-references` is the
canonical refresh skill: after fetching an updated reference, it
scans both bausteine (`references[]`) and memory docs
(`references_used[]`) for matches. Bausteine matching → flagged.
Memory docs matching → logged to `memory/product-backlog.md` with
affected paths.

**Frontmatter declares invalidation hooks.** Cross-cutting docs
that name laws declare them in frontmatter:

```yaml
---
references_used:
  - {law: BauGB, paragraph: §3 Abs.2}
  - {ruling: BVerwG-9-A-22-11}
  - {leitfaden: KNE-Anlagengestaltung}
---
```

This rule was previously implicit (scattered across "What changes
invalidate what" prose + per-entity-type schemas). Promoting to a
meta-rule forces every new entity type to answer "how does the
system know you're stale?" before shipping.

## Meta-rule 4: execution determinism (where deterministic work lives)

About *where* operations execute, not where content lives.

**Core principle.** Operations with a single deterministic correct
execution — validation, schema enforcement, transactional writes,
side-effect coupling, cross-reference consistency, computed
properties (hashes, indexes), migrations — live in **MCP gates**
(backend code, exposed as MCP tools). Skills are for judgment,
conversation, and surfacing decisions; they orchestrate MCP tool
calls, never reimplement what those tools do.

(Renamed from "execution locality" in v0.4. Locality suggests
*physical location*; the actual axis is determinism — single-right-
answer vs. judgment.)

**The persistence-layer boundary.** Cleanest line: *anything that
touches durable state with a **typed contract** (Pydantic model +
loader + cross-reference invariants) goes through MCP; session-
ephemeral state and loose unstructured files stay skill-direct.*
Watch list, in-conversation findings, surfacings queued during a
turn — all skill (ephemeral). Writes to office-config, baustein
YAML, manifests, schema-bearing state files — all MCP (the loader
owns the shape; bypassing MCP bypasses forward-migration and
invariants).

**The line is contract enforcement, not file type.** A file is in
scope of MCP if a Pydantic model + loader owns its shape. If the
file is parsed only by the LLM at read time, direct
`Read`/`Write` is fine. HANDOFF.md, prose memory `.md` files
under `memory/universal/`, top-level docs, READMEs — all
skill-direct, no schema, no migration, no transactional risk. A
markdown file *can* become schema-bearing later (e.g., `state.md`
once typed parsing lands) — at which point its access path
moves to MCP. Audit slice 14 reads each access via this test,
not by extension.

**Deterministic vs interpretive verdicts.** Validation with a
single right answer (frontmatter shape, ISO state code, schema
conformance, citation drift on exact-string match) is deterministic
→ MCP. Validation requiring interpretation (does this baustein
content actually concern §44 BNatSchG? does this language read as
collegiate or formal?) is interpretive → skill, surfaces verdict
to user. When unclear, ask: would two implementations agree byte-
for-byte on the verdict? If yes, MCP. If no, skill.

**Enumeration-vs-selection corollary.** "List the candidates" is
deterministic, scope-aware → MCP (`list_bausteine`,
`list_reference_manifests`). "Pick the right one for this drafting
context" is judgment → skill.

**Reuse direction.** When two consumers share logic, where does the
shared code live? The rule has a positive form, not just the
negative "skills compose, never reimplement":

- **Shared deterministic logic → MCP tool.** Two skills that need
  to dedupe, validate frontmatter, or look up a manifest entry call
  the *same* MCP tool. Don't reimplement; don't copy-paste prompt
  text describing the deterministic procedure into each consumer.
- **Shared interpretive logic → Skill Bundle reference.** Two skills
  that need to reason about korrektur-rules, layered review
  mechanics, or doctype conventions load the *same*
  `references/<topic>.md` file. The Skill Bundle convention exists
  for exactly this — judgment scaffolding shared across skill-side
  consumers without each skill re-stating it.

The negative form ("don't reimplement") tells you what's wrong; the
reuse direction tells you where the right home is. Audit slice 14
flags both directions: re-implemented determinism in skills *and*
re-implemented interpretive scaffolding when a Skill Bundle
reference would have served.

**Skill frontmatter declares MCP-tool dependencies.** Every skill's
`SKILL.md` frontmatter declares which MCP tools it relies on
(`mcp_tools_required[]`, `mcp_tools_optional[]`,
`fallback_when_mcp_absent`). See `docs/plugin-conventions.md` §1
for the full contract. Tools are referenced by snake_case name —
matches the Python function name in `pbs_core/`. Frontmatter is
machine-checkable; future audit slices verify every declared tool
exists in the MCP server's registry.

**Static path-based access control belongs in `settings.json`,
not in code.** Where a path should never be written outside a
specific MCP tool's context, use a permission deny rule. Cheaper
than scaffolding code paths that re-enforce what the harness can
already block.

### Backend organization (consequence of meta-rule 4)

Backend code splits conceptually into two layers:

- **`pbs_core/`** (planned package; currently part of `pbs_mcp/`):
  plain Python — config schema, validation, layered manifest API,
  integration adapters, RAG pipeline, project lifecycle, audit
  trail. Takes Python args, returns Python objects, raises Python
  exceptions. Knows nothing about MCP.
- **`pbs_mcp/tools/`**: thin MCP tool definitions that wrap
  `pbs_core` functions — parse JSON args, call core, format
  response, translate exceptions to MCP errors. Contains no
  business logic.

This is the consumer-side of the meta-rule: meta-rule 4 says
"deterministic logic in MCP gates"; this organization adds "MCP
gates are themselves thin wrappers around plain Python core."

This discipline applies starting now even though the two layers
live in the same module today. When the first non-MCP frontend
emerges (web UI is the load-bearing trigger per ROADMAP), the
physical split — promoting `pbs_core` to its own package — is a
small refactor, not a re-architecture.

**Don't do the physical split until a real second consumer exists.**
The conceptual discipline gives most of the maintainability +
testability benefit at near-zero cost.

---

# Layering convention: scope orthogonality (universal × domain × state)

(Demoted from meta-rule in v0.5 per design-review. It's a
*layering pattern* applied to specific entity types, not a placement
axis itself — it doesn't answer "where does this go?", it answers
"once you know it's the kind of thing that layers, which subdirectory?".)

Reference content, doctype registries, skeletons, and bausteine all
decompose along the same three orthogonal axes:

- **universal** — applies to every German Planungsbüro deploying
  this app, regardless of planning domain or Bundesland.
- **domain** — applies to bureaus working in a specific planning
  domain (e.g. PV-FFA, Wind, Naturschutz, Innenentwicklung).
  Multiple domains can be active simultaneously.
- **state** — applies to bureaus working in a specific Bundesland
  (BB, BW, BY, ..., TH). Multiple states can be active simultaneously.

A bureau's effective content is its `(domains × states)` selection
(set in `office-config.yaml > scope.{domains,states}`). Layered
loaders merge the universal layer with each selected domain/state
layer at runtime.

**Where this applies:**

- **References manifests**: `extensions/{universal,domain/<X>,state/<X>}/references-manifest.yaml`
- **Doctype manifests**: `extensions/{universal,domain/<X>,state/<X>}/doctypes.yaml`
- **Skeletons**: `plugin/templates/skeletons/{universal,domain/<X>}/<doctype>/`
- **Bausteine**: `memory/bausteine/{universal,domain/<X>,state/<X>}/<name>.md`
- **Office-style overlays**: `plugin/templates/office-style/office-style.{default,<DOMAIN>}.sty`

**Hard rules for placing layered content:**

- Decide the scope BEFORE the path. Ask: does this apply to every
  German bureau (universal), every bureau in this domain (domain),
  every bureau in this state (state)?
- A baustein has exactly one scope. If a candidate baustein applies
  to multiple, either promote it up the layer (`universal` if truly
  cross-domain) or split it.
- An entry's home is independent of who created it.

**Out of scope (entity types this convention doesn't apply to):**
Skill Bundles, Backend, External Data — none of these layer along
(universal × domain × state). Configuration partially applies (its
manifest tree under `extensions/` does; the office-config file
itself doesn't).

**The `author-manifest` skill** scaffolds new domain or state
manifests for scopes that don't yet have content.

---

# The five entity types

| Type | Where | Invalidation | What it does |
|---|---|---|---|
| **Skill Bundle** | `plugin/skills/<name>/SKILL.md` + `references/*.md` | semver `version:`; reload via `/reload-plugins` | Behavioral protocol auto-loaded on trigger match. SKILL.md is the entry point; references hold detailed format specs / checklists / procedures. (Combines former Type A skill + Type B skill reference — they're chapters of one bundle, not peers.) |
| **Memory** | `memory/universal/...` (prose), `memory/bausteine/{universal,domain/<X>,state/<X>}/...` + `<project>/_ai/...` (records) | references_used/status/review_due/verified_against_version | Two sub-kinds: **authored prose** (universal domain knowledge consumed across skills — style-spec, korrektur-rules, verfahren docs) + **generated records** (bausteine, feedback entries, project state.md). Mutability differs sharply between them; both share Memory's invalidation hooks. |
| **Backend** | `backend/mcp-server/...` (code + protocols + adapters + technical docs) | none declarative; restart MCP server after changes | Python implementation. Splits conceptually into `pbs_core/` (plain Python) + `pbs_mcp/tools/` (MCP wrappers) per meta-rule 4. Integration adapters live as a sub-organization here (`pbs_mcp/integrations/<class>/<adapter>.py`); they're an internal pattern, not a peer entity type. |
| **Configuration** | `office-config.yaml` (single per deployment, outside repo) + `extensions/{universal,domain/<X>,state/<X>}/{references,doctypes}-manifest.yaml` (scope-keyed, in repo) | `schema_version` + migration framework | Deployment-controlled YAML. Two sub-kinds — single-file (office-config) and scope-keyed (layered manifests) — distinguished by where they live + how they're discovered, but both are configuration-shaped (versioned, schema-validated, deployment-scoped). |
| **External data** | Resolved via `roots.*` (projects, references, state) + per-project `<project>/_ai/...` | Varies; project state via `_ai/state.md.lifecycle`; references corpus via `<roots.references>/changelog.md` | Real user data: legal texts, project artifacts, runtime state, correspondence. NOT versioned with the app. |

**Why 5 not 9** (per design-review session 5):
- **Skill Bundle** = former A (Skill) + B (Skill reference). A skill reference has no meaning outside its parent skill — it's a chapter of the bundle, not a peer. Decision rules collapse from "is this a skill or a skill-reference?" to "is it part of a skill bundle?"
- **Configuration** = former G (Office config) + H (Layered manifests). Both are deployment-controlled YAML; the only difference is single-file vs scope-keyed, which is *where* they live, not *what kind of thing* they are.
- **Backend** = former E (Backend code) + I (Integration adapters). Adapters are a backend-internal organizing pattern (same language, same package, same restart semantics) — not a peer entity type.
- **Drop A-I letters**: false ordinality + false peerage. Names ("Skill Bundle", "Memory", "Backend") are self-documenting.

(For migration: any prior reference to "Type A" / "Type B" / "Type C" / etc. should be re-read as the corresponding new name. Most references to the old letters can be dropped without replacement; the new names speak for themselves in context.)

---

# The three decision rules

For any new piece of content, walk these in order. The first to
classify wins.

## Rule 1 — Is this consumed by Claude at runtime as behavior?

If it tells the AI HOW to act, what to load, how to converse, when
to delegate — it's part of a Skill Bundle.

→ **Skill Bundle**: `plugin/skills/<name>/SKILL.md` (entry point,
with frontmatter) + optional `references/*.md` (detailed protocols,
format specs, checklists — no frontmatter).

If multiple skills consume the same content (e.g. korrektur-rules,
style-spec, verfahren-phasen), it's *cross-cutting authored prose*
— route to Rule 3 (Memory: prose).

## Rule 2 — Is this Python code?

If it's `.py` — backend code, MCP tool wrappers, integration
adapters, technical schema docs.

→ **Backend**: `backend/mcp-server/...`. Adapters are a sub-pattern
(same package), not a separate type.

## Rule 3 — Then by mutability:

**3a. Authored prose** (humans/AI write; cross-cutting knowledge):

- Universal domain knowledge → `memory/universal/...` →
  **Memory (prose)**.
- Layered (universal × domain × state) reference manifests +
  doctype registries → `extensions/<scope>/<key>/*.yaml` →
  **Configuration (scope-keyed manifest)**.
- Per-deployment values (paths, identity, actors, scope) →
  `office-config.yaml` (outside repo) → **Configuration (office-config)**.

**3b. Generated records** (tools write; instance state):

- Bausteine, feedback entries, project state — `memory/bausteine/<scope>/<key>/<name>.md` or `<project>/_ai/...` → **Memory (record)**.

**3c. External data** (user files, not versioned with app):

- Legal text corpus, client project artifacts, runtime state →
  `<roots.*>` paths, per-project `_ai/...` → **External data**.

## How the rules compose

Rule 1 catches everything Claude reads as instruction. Rule 2
catches everything written in Python. Rule 3 splits the rest by
who-writes-it (authored vs generated vs external).

The 4-mutability breakdown in Rule 3 is *one rule with sub-cases*,
not 4 separate rules. The decision is "what kind of content is
this?" (prose / record / config / external), not a sequential walk.

(This collapses the v0.4 6-rule walk to 3 rules + sub-cases. The
former Rules 4 and 5 — "HOW vs WHAT" — were a false axis: every
cross-cutting memory doc has *both* HOW and WHAT properties; the
real distinction is consumer breadth, which Rule 1's "multiple
skills" branch handles directly.)

---

# Worked examples

| Content | Reasoning | Type |
|---|---|---|
| `style-spec.md` (universal B-Plan LaTeX domain) | Rule 1: cross-cutting (multiple skills); Rule 3a: authored universal prose. | Memory (prose) |
| `korrektur-rules.md` (German writing conventions) | Same — cross-cutting prose; Rule 3a. | Memory (prose) |
| `bauleitplanung-phasen.md` (BauGB process) | Rule 3a: authored universal prose, cross-cutting. | Memory (prose) |
| `extensions/universal/doctypes.yaml` | Rule 3a: scope-keyed manifest. | Configuration (manifest) |
| `extensions/domain/Naturschutz/doctypes.yaml` | Same; scope=domain/Naturschutz. | Configuration (manifest) |
| `office-config.yaml` (outside repo) | Rule 3a: per-deployment configuration. | Configuration (office-config) |
| `baustein-format.md` (how to write a baustein) | Rule 1: instruction; consumed by ONE skill (save-baustein). Part of skill bundle. | Skill Bundle (reference) |
| `state-format.md` | Rule 1: instruction; single-skill (orchestrator). | Skill Bundle (reference) |
| `manifest-schema.md` | Rule 1: single-skill (research-references). | Skill Bundle (reference) |
| Doctype checklists | Rule 1: single-skill (validate-checklist). | Skill Bundle (reference) |
| `vector-metadata-schema.md` | Rule 2: backend technical schema. | Backend |
| A future saved baustein | Rule 3b: generated record. Apply layering convention to pick scope. | Memory (record) |
| A future feedback entry | Rule 3b: generated record. | Memory (record) |
| A future `<project>/_ai/state.md` | Rule 3b: generated record. | Memory (record) |
| `orchestrator` SKILL.md | Rule 1: skill bundle entry point. | Skill Bundle |
| `save-baustein` SKILL.md declares `mcp_tools_required: [save_baustein, list_bausteine]` | Meta-rule 4: skill is the orchestrator; MCP tool is the validator. Frontmatter makes the dependency explicit. | Skill Bundle |
| Email integration adapter Python | Rule 2: backend Python. (Sub-pattern: integration adapter.) | Backend |
| Court ruling text from BVerwG website | External data; lives in RAG corpus at `<roots.references>/urteile/...`. | External data |
| `references_used: []` frontmatter | Meta-rule 3 invalidation hook. | (per containing entity type) |

---

# Designed extensions, not yet implemented

These ROADMAP items will extend or modify the architecture when
implemented. Recorded here so future sessions don't re-discover
them. Full design lives in `ROADMAP.md`.

> **RAG-related items** (multimodal ingest, structural retrieval,
> query rewriting, agentic retrieval, late-interaction text
> retrieval) are resolved (ACCEPTED in session 5 post-audit) in
> `docs/rag-pipeline-decisions.md`. The bullets below list the
> ROADMAP framings; that doc carries the verdicts + alternatives
> + revisit triggers.

- **Audit trail** — unified change/decision/version log across
  artifacts, references, manifests, configs, integrations,
  bausteine, plans, correspondence. Today scattered (`decisions.md`,
  `snapshots/`, `changelog.md`, manifest archives, git). Will
  formalize as a Memory (record) sub-kind or a new
  Configuration-style log. Per meta-rule 3, every entity already
  declares invalidation; this extension unifies the log.
- **Human-readable artifact generation at checkpoints** — every
  meaningful checkpoint (send-gate, phase transition, draft-invoice,
  baustein-promotion, config-change) produces a PDF/HTML alongside
  machine state.
- **Integration registry** — discovery API over callables (skills,
  MCP tools, adapters) with capability metadata. Skills already
  carry `capabilities[]`-equivalent in their `phase_role` +
  `handoffs[]` frontmatter (post-design-review session 5);
  registry will federate that with backend tool registration.
- **Web UI for collaborative review** — Coolify-hosted; review-
  platform integration adapter class. First non-MCP frontend —
  triggers the `pbs_core/pbs_mcp` physical split.
- **PM + invoicing** — per-project `_ai/billing.md` ledger;
  `log-time` + `draft-invoice` skills; uses accounting integration
  adapter.
- **Multimodal RAG ingest pipeline** — page-image retrieval
  (ColPali), table extraction, OCR, DRM removal. Architecture
  decided: local pre-processing + embedding + matching; reading +
  reasoning happens via the in-loop Claude session.
- **Structural retrieval** — legal §-graph + project-cross-project
  graph + verfahren state-machine. SQLite alongside LanceDB.
- **Query rewriting** (HyDE, decomposition, expansion) +
  **agentic retrieval** (per-claim search) + **late-interaction
  text retrieval** (ColBERT-v2, conditional) — all retrieval-
  pattern improvements.
- **Per-domain memory directories** (`memory/domain/<X>/`) —
  introduce when first domain-scoped reference content lands.
  Mirror of references / doctypes layering.
