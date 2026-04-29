# Failure-mode catalog

The load-bearing reference for **target 14 — discipline-gap
detection**. A living catalog of architectural failure modes seen
in this and adjacent architectures, with their current coverage
status (named discipline that protects against, or "uncovered").

## How this catalog is used

- **Target 14 reads this catalog**, then for each entry checks
  whether a named discipline (in `ARCHITECTURE.md`) protects
  against it. Entries marked "uncovered" with high applicability
  + severity become recommendations to codify a new discipline.
- **This catalog is a living document.** Every postmortem feeds
  it. Every new architectural discipline updates the coverage
  status of relevant entries. Every novel failure mode discovered
  in production gets a new entry.
- **Entries are organized by category** for navigability, not by
  priority.

## Entry schema

Each entry has:

- **Name** — short identifier (kebab-case)
- **Description** — one-paragraph explanation of the failure
  mode + how it manifests
- **Applicability** — does this apply to PBS today / in this
  architecture shape? (yes / partial / no — distributed-systems
  failures often "no" for single-process apps)
- **Severity** — catastrophic / serious / minor (when it bites)
- **Coverage status** — covered (which named discipline) /
  partial (which discipline + what's still uncovered) /
  uncovered
- **Notes** — surfaces where seen, postmortem refs, related
  entries

---

## Category 1 — Persistence + data shape failures

### Silent convergence

**Description**: multiple independent surfaces implement the same
structural pattern over time without anyone naming it as
discipline. Once unnamed, the pattern can't be enforced or
inherited consistently — new surfaces drift away from it. The
unnamed convergence breaks silently when one of the surfaces gets
modified in a way that breaks compatibility, because there's no
named contract to flag the break.

**Applicability**: yes (any codebase ≥3 surfaces).
**Severity**: serious (creates compounding drift over time).
**Coverage status**: ✅ **covered** — design-review target 13
(pattern emergence / unnamed convergence).
**Notes**: session-10 case — hybrid-shape (frontmatter + md body)
present in memory + skills + state.md unnamed for 6+ months;
department.yaml was on track to drift into pure-YAML.

### Prose-in-block-scalars

**Description**: prose-shaped content squeezed into structured-
container fields (YAML `description: >`, `notes: |`, JSON string
fields with `\n`) that suppress the natural form prose wants to
take — no headings, no structured lists, no links, no examples.
The container "works" mechanically but the content is degraded;
both authoring and AI-reading are harder than they should be.

**Applicability**: yes (any codebase mixing structured config +
prose semantics).
**Severity**: serious (degrades authoring quality + AI runtime
behavior).
**Coverage status**: ✅ **covered** — AI-as-runtime hybrid-shape
principle (`docs/decisions/ai-as-runtime-hybrid-shape.md`).
**Notes**: session-10 case —
`extensions/universal/doctypes.yaml` `description: >` blocks +
`extensions/universal/references-manifest.yaml` `notes: |`
blocks. Migration scheduled with #9 + Phase 1.

### Encoded-rules-when-AI-as-runtime-was-available

**Description**: rules expressed in code or as encoded prose-as-
procedure when **AI-read-prose** would have served. Adds a layer
that needs maintenance + couples rule expression to code release
cycle. Manifests as state machines, hardcoded conditional logic
in skills, or schema validators trying to enforce semantic rules.

**Applicability**: yes (any AI-mediated architecture).
**Severity**: serious (locks in rigidity that cross-domain
portability needs to break).
**Coverage status**: ✅ **covered** — AI-as-runtime hybrid-shape
principle.
**Notes**: session-10 corrective. The original three-layer
proposal (Pydantic + markdown + skill-prose-as-encoded-process)
was an instance of this failure mode wearing different clothes.

### SQL-DB-trap (Oracle-shape architecture for LLM-mediated systems)

**Description**: architecture creeping toward relational-DB
shape — one entity per noun, foreign keys, joins, normalization.
Catastrophic for LLM-mediated systems: makes the architecture
brittle, slow to evolve, and re-implements enterprise software's
worst tendency. LLMs reason poorly over highly-normalized schemas;
prefer document-shape with stable references.

**Applicability**: yes (any system tempted to elevate every noun
to entity).
**Severity**: catastrophic (architecture rebuild).
**Coverage status**: ✅ **covered** — entity-elevation discipline
(3-test) + AI-as-runtime hybrid-shape principle (closer to
knowledge graph + document store).
**Notes**: ARCHITECTURE.md v0.13 entity-elevation discipline.

### Source-of-truth ambiguity

**Description**: same data exists in 2+ places without an
invalidation contract. Updates to one don't propagate; readers
get stale data; the bug surface is "which copy is the real one?"
Can manifest as cached values, denormalized projections without
refresh, or two skills writing to overlapping files.

**Applicability**: yes (any persistence layer).
**Severity**: serious (data corruption + debugging hell).
**Coverage status**: ✅ **covered** — meta-rule 3 (source-of-
truth & invalidation).
**Notes**: catches both within-session (caches) and cross-session
(file representations) cases.

---

## Category 2 — Coupling + drift failures

### Configuration-vs-code drift

**Description**: a rule expressed both in config (e.g., YAML
schema) and in code (e.g., skill prose) drifts over time as one
side changes without the other. Manifests as "the docs say X but
the code does Y" mysteries.

**Applicability**: yes (any codebase with significant config
layer).
**Severity**: serious (silent behavioral changes).
**Coverage status**: ⚠ **partial** — meta-rule 4 (execution
determinism) constrains *where rules live* (deterministic →
MCP gate; interpretive → skill); reduces drift surface but
doesn't fully prevent. **Evaluate** after #9 for residual gaps.
**Notes**: a residual case: `office-config.schema.yaml` vs
`office_config.py` Pydantic model — could drift if not
co-maintained. Today both are co-edited; convention not
enforced.

### Hardcoded-instance-content-in-pattern-layer

**Description**: meta-rules, decision records, or framework code
include domain-specific terminology (e.g., "B-Plan", "Begründung")
in a way that prevents portability to other instances. Subtle
because individual examples may be fine but cumulative
hardcoding makes the framework PBS-specific.

**Applicability**: yes (any framework with pioneer instance).
**Severity**: catastrophic for builder vision (v2 AI-office
builder needs domain-agnostic patterns).
**Coverage status**: ✅ **covered** — pattern-vs-instance
discipline + design-review target 10.
**Notes**: ARCHITECTURE.md "Anti-patterns the discipline catches"
subsection enumerates instances.

### Vendor-lock at architecture layer

**Description**: architecture commits to a specific vendor
(Lexware, Harvest, Salesforce) at framework level rather than at
adapter level. Customer-replacement-cost rises; cross-domain
portability suffers; "AI office that augments your stack"
positioning becomes "AI office that locks you into our stack."

**Applicability**: yes (any system integrating external tools).
**Severity**: serious (competitive + adoption impact).
**Coverage status**: ✅ **covered** — glue-not-replacement
principle + meta-rule 1 (integration-adapter pattern).
**Notes**: every external integration goes through
`Pydantic Protocol` + concrete adapter, not direct vendor SDK
calls.

### Cargo-cult patterns

**Description**: pattern adopted from another codebase or
authority (Anthropic plugin, partner framework, popular library)
without understanding *why* it's the right shape for THIS
context. Manifests as architectural debt that nobody can defend
when challenged.

**Applicability**: yes (especially when adopting external
patterns like Cowork plugin shape).
**Severity**: minor-to-serious depending on what's adopted.
**Coverage status**: ⚠ **partial** — design-review's greenfield
reframe asks "would we build this from scratch?" which catches
some cases. Subsumption check (target 9) catches "what does this
replace?" Combined coverage is good but not airtight.
**Notes**: low-priority; hard to catch structurally. Most caught
through user instinct + sparring conversation.

---

## Category 3 — Skill + composition failures

### Monolithic-skill-bundle

**Description**: one skill doing too much — multiple distinct
responsibilities, multiple unrelated trigger phrases,
multi-purpose body. Hard to maintain, hard to compose with other
skills, hard to test.

**Applicability**: yes.
**Severity**: serious (maintenance burden, composability loss).
**Coverage status**: ⚠ **partial** — skill-conventions discusses
single-responsibility informally but no named discipline. Several
PBS skills (orchestrator, design-review) are intentionally
broad-scope; the line between "appropriately-broad" and
"monolithic" isn't sharp. **Evaluate** for explicit discipline.
**Notes**: orchestrator at 0.10.0 has multiple trigger phrases +
broad scope; intentional but worth periodic check.

### Implicit-contract-between-skills

**Description**: skills coordinate via conventions not declared in
frontmatter — skill A writes a file at known location, skill B
reads from same location, no declared dependency. Refactor
breaks contract silently.

**Applicability**: yes.
**Severity**: serious (silent breakage on refactor).
**Coverage status**: ⚠ **partial** — `mcp_tools_required[]` +
`handoffs` declarations cover MCP-mediated + handoff-mediated
flows. File-location-based implicit contracts (e.g., "the
state.md format" before MCP gate) are NOT covered by frontmatter
declarations. **Evaluate** for explicit discipline.
**Notes**: state.md MCP gate (session 6) closed one such case;
others may exist.

### Hidden-global-state

**Description**: state read or mutated outside declared
dependencies. Examples: env vars read in skills without
declaration, ambient process state assumed, race conditions on
shared resources.

**Applicability**: yes (especially as multi-user mode arrives in
#13).
**Severity**: catastrophic for multi-user; serious for
single-user.
**Coverage status**: ⚠ **partial** — strict-validation +
fail-closed corollary catch most cases at MCP boundary.
Pre-#13 single-user mode masks issues that #13 will surface.
**Re-evaluate after #13.**
**Notes**: scheduled re-evaluation when #13 lands.

---

## Category 4 — Process + workflow failures

### Workflow-as-data-instead-of-prose

**Description**: process flow encoded as state machine or
configurable data structure, when prose-described process md
+ AI-as-runtime would serve. Reproduces BPMN-engine complexity
unnecessarily.

**Applicability**: yes (especially as #11 + cross-domain work
arrives).
**Severity**: serious (architectural complexity, cross-domain
portability loss).
**Coverage status**: ✅ **covered** — AI-as-runtime hybrid-shape
principle (process-as-md, not state-machine-as-data).
**Notes**: explicit resolution in
`docs/decisions/ai-as-runtime-hybrid-shape.md`.

### Premature-elevation-to-entity

**Description**: a noun gets promoted to managed entity (Pydantic
+ MCP CRUD + persistence) before it clearly satisfies the 3-test
(stable identity + state of record + lifecycle). Adds schema
sprawl + maintenance burden for what should have been an event,
nested field, or memory entry.

**Applicability**: yes.
**Severity**: serious (compounding schema sprawl).
**Coverage status**: ✅ **covered** — entity-elevation discipline
+ design-review target 11.
**Notes**: 3-test mandatory check at design time + retrospective
audit slice 20.

---

## Category 5 — Distributed-systems failures

### Network-partition-during-write

**Description**: write fails halfway through a multi-step
sequence; readers see partial state.

**Applicability**: ⚠ **partial** — single-process MCP today, no
distributed write. Becomes applicable post-#13 (Coolify cloud +
multi-user).
**Severity**: TBD per #13.
**Coverage status**: 🚫 **n/a today**; **uncovered for post-#13**.
**Notes**: re-evaluate at #13.

### Clock-skew-across-nodes

**Description**: timestamps from different nodes drift; ordering
becomes ambiguous.

**Applicability**: 🚫 **no** — single-process today, single
authoritative clock.
**Severity**: n/a today.
**Coverage status**: 🚫 **n/a**.
**Notes**: re-evaluate if/when multi-node ever applies (likely
not within v1.x scope).

### Cascading-failure-on-dependency-down

**Description**: one downstream service failing causes upstream
failures to cascade.

**Applicability**: ⚠ **partial** — MCP gate fail-closed
discipline applies; broader cascading failures (Lexware adapter
→ invoicing skill → Project workflow) become applicable as
adapters multiply.
**Severity**: serious post-multi-adapter.
**Coverage status**: ⚠ **partial** — fail-closed corollary
covers MCP layer; adapter-layer cascade not yet codified.
**Re-evaluate after #11 + adapter expansion.**
**Notes**: schedule for re-evaluation post-#11.

---

## Adding to this catalog

When a new failure mode is identified (postmortem, literature,
spontaneous insight), add an entry following the schema. Don't
remove entries — change `Coverage status` instead. The catalog
is *additive history*; entries marked "n/a" or "covered" are still
informative for understanding the design space.

When a new discipline ships, run target 14 to update coverage
statuses.

When applicability changes (e.g., #13 ships and distributed-
systems modes become applicable), update affected entries.
