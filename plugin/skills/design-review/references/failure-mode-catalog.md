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
- **Applicability** — does this apply to the framework today / in
  this architecture shape, including deployments the framework
  serves (consulting clients at first bind, not just PBS-pioneer
  state)? (yes / partial / no — distributed-systems failures
  often "no" for single-process apps; PBS-only-state limitations
  are NOT valid grounds for "no" since the framework targets
  multi-deployment first-bind)
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

### Convention-driven solution for gate-dispatched concern

**Description**: a concern that the gate / Pydantic / dispatch
code touches on every read/write is enforced via deployment-time
convention (skill body imperative, prose rule in office-config,
"deployment documents the X" claim) rather than via structural
constraint. Each consulting client hits the same problem; each
must solve it independently; some solve inconsistently. Drift
across deployments is guaranteed eventually. The convention "works"
because individual contributors are disciplined, but the framework
relies on per-deployment-discipline rather than impossibility-by-
construction. Manifests as: skill bodies saying "remember to set X
on every Y"; Pydantic Optional fields with comments like "should
always be set when Z"; two skills both having to "remember" the
same convention.

**Applicability**: yes (any framework with deployment instances).
**Severity**: serious (compounding cross-deployment drift +
inconsistent shapes + deferred conflicts when blueprints share).
**Coverage status**: ✅ **covered** — **"Make wrong shapes
impossible, not solvable" discipline (ARCH v0.21)**. Discriminator:
gate / Pydantic / dispatch touches concern on every read/write →
structural enforcement required. Retrospective scan: **slice 22
(wrong-shapes-solvable)**. Prospective check: **design-review
target 15**.
**Notes**: session-11 case — type-name uniqueness across
departments was leading toward Option C (convention-driven) until
the discriminator surfaced; locked Option B (department-namespaced)
as structural fix. Discipline named after the failure mode was
caught.

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
**Coverage status**: ⚠ **partial** — multi-discipline cover with
residual gaps. Meta-rule 3 (source-of-truth + invalidation) is
the primary cover for "data exists in 2+ places." Meta-rule 4
(execution determinism) constrains *where rules live*
(deterministic → MCP gate; interpretive → skill). **"Make wrong
shapes impossible, not solvable" (v0.21)** narrows further: when
a rule is gate-dispatched on every read/write, structural
enforcement (one-source-of-truth via Pydantic + gate) is required,
making drift impossible by construction. **Slice 22
(wrong-shapes-solvable scan)** retrospectively flags residual
cases. **Evaluate** after #9 for residual gaps.
**Notes**: a residual case: `office-config.schema.yaml` vs
`office_config.py` Pydantic model — could drift if not
co-maintained. Today both are co-edited; convention not
enforced. Slice 22's first run will flag this category of cases
retrospectively.

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

### Manufactured-restraint defer

**Description**: a defer rationale that masquerades as honest
restraint but is actually offloading framework work to deployment
time. Two flavors: **(a) pioneer-instance-anchored** — "today PBS
doesn't need it" / "only planning exists" / "no consumer in PBS
until #N" — silently optimizes for PBS instead of the framework
that PBS validates. **(b) up-front-cost shaped** — "more sessions"
/ "premature abstraction" / "YAGNI" / "we'll add it later when
needed" — treats present-time effort as a valid defer reason when
it isn't. Both produce manufactured restraint — the defer LOOKS
like sober "wait for pressure" reasoning but is actually
offloading. Each consulting client deploying tomorrow hits the gap
at first bind; the framework should have closed it.

**Applicability**: yes (any framework + pioneer-instance setup).
**Severity**: serious (cumulative — each manufactured defer
creates a first-bind gap for future deployments).
**Coverage status**: ✅ **covered** — **pattern-vs-instance +
sharp defer rule (ARCH v0.20)**. Two tests both must pass for an
honest defer: chronological (info doesn't exist yet that would
change the design) AND framework-cost (no hypothetical second-
domain deployment needs this at first bind). Up-front costs
(time, complexity, "premature") are NEVER valid defer reasons.
Memory `feedback_pattern_not_instance_defers.md` propagates to
future sessions.
**Notes**: session-11 cases — `activate-department` skill
defer-to-#11 ("today no department needs activating, only
planning exists") + Bundle E adapter Protocol defer-to-#11 ("no
consumer until first adapter-mode entity ships") were both
manufactured-restraint-defer instances caught and reversed.
Sharp-defer audit pulled six v1.x items forward to v1 under same
discipline.

### Cargo-cult patterns

**Description**: pattern adopted from another codebase or
authority (Anthropic plugin, partner framework, popular library)
without understanding *why* it's the right shape for THIS
context. Manifests as architectural debt that nobody can defend
when challenged.

**Applicability**: yes (especially when adopting external
patterns like Cowork plugin shape, agentic frameworks per #18).
**Severity**: minor-to-serious depending on what's adopted.
**Coverage status**: ✅ **covered** — three-layer protection:
1. **Greenfield review at major version boundaries** (per ARCH
   maintenance discipline rule 6, added v0.28). Periodic walk
   through architecture asking "would we build this from
   scratch?" catches accumulated cargo-cult drift.
2. **Design-review subsumption check (target 9)** catches "what
   does this replace?" — prevents new mechanism from coexisting
   with the legacy it should retire.
3. **Sharp defer rule (v0.20) + greenfield-disqualifying-criteria
   for substrate evaluations (#18, #19)** — substrate adoption
   evaluated against VISION + load-bearing disciplines, not
   adopted by ecosystem-fit alone.
**Notes**: session-11 ARCH disciplines greenfield review (v0.27)
+ greenfield-architecture-review.md (v0.25) demonstrate the
mechanism — 15+ radical alternatives considered + rejected on
VISION grounds rather than inertia.

---

## Category 3 — Skill + composition failures

### Monolithic-skill-bundle

**Description**: one skill doing too much — multiple distinct
responsibilities, multiple unrelated trigger phrases,
multi-purpose body. Hard to maintain, hard to compose with other
skills, hard to test.

**Applicability**: yes.
**Severity**: serious (maintenance burden, composability loss).
**Coverage status**: ✅ **covered** — skill-granularity discipline
(ARCH v0.27, elevated to ARCH-level under "Elevation analogue for
skills" sub-section of entity-elevation discipline). Same
restraint-in-elevation criteria apply in REVERSE direction: a
skill is too monolithic when it contains MULTIPLE concepts that
each pass the 3-test (distinct workflow + distinct output +
reuse across projects) — those should be SPLIT into separate
skills. The 3-test's same criteria catch both over-elevation
(don't create new skill for a topic that fails) AND under-
elevation (split a skill containing multiple topics that each
pass).
**Notes**: orchestrator + design-review intentionally broad-scope
because their workflow IS coordination/review across multiple
sub-concerns — single workflow per the 3-test. Different from
"monolithic": split would lose the coordination function.

### Incomplete-gate-coverage

**Description**: meta-rule 4's "contract-bearing reads + writes go
through MCP gate" applies in principle, but in practice not every
contract-bearing surface has a gate today. New entity types or new
contract-bearing files may go through direct filesystem `Read` /
`Write` for an extended period before someone notices the missing
gate. Slice 16 (validation-gate coverage) checks per-Pydantic-model
strictness of EXISTING gates; doesn't enumerate surfaces that
SHOULD be gated but aren't. Different scan.

**Applicability**: yes (immediate). Today: bausteine
(`memory/bausteine/`) have YAML frontmatter contracts but no
gate. Per-project memory (`<project>/_ai/file-map.md`,
`decisions.md`, `snapshots/`) — partial coverage. Post-#9 +
#11 + #15: many new entity-md surfaces will need gating; risk of
some being missed.

**Severity**: serious — a missing gate breaks fail-closed
discipline (skill bypasses contract via direct Read), makes
schema migrations harder, and silently degrades the "everything
contract-bearing goes through MCP" promise.

**Coverage status**: ⚠ **partial — narrowing.** Three layers
of cover now: (1) slice 16 covers strictness of existing gates;
(2) **"Make wrong shapes impossible, not solvable" (v0.21)**
makes "convention enforces what should be gated" structurally
identifiable as anti-pattern; (3) **slice 22 (wrong-shapes-
solvable scan)** + **design-review target 15** retrospectively
+ prospectively flag concerns enforced via skill-body discipline
that should have structural gates. The comprehensiveness scan
("which surfaces lack gates that should have them?") is also
**scheduled as pre-RAG task #17 (MCP gate coverage
comprehensiveness review)** — see ROADMAP. Status remains
"partial" until #17 runs and gaps close, but the gap is
narrower than before v0.21.

**Notes**: slice 22 + #17 + target 15 are the closing-loop
combination. Slice 22 catches "convention where gate should be";
#17 catches "no gate at all"; target 15 prevents new instances at
design time.

### Implicit-contract-between-skills

**Description**: skills coordinate via conventions not declared in
frontmatter — skill A writes a file at known location, skill B
reads from same location, no declared dependency. Refactor
breaks contract silently. Three sub-shapes:
1. **File-location-based** (e.g., "skill A writes
   `<project>/_ai/X.md`; skill B reads it") — addressed by MCP
   gate adoption per fail-closed corollary.
2. **Skill-to-skill handoffs via orchestrator** — context format,
   side-effect ordering, expected post-conditions implicit in
   orchestrator routing logic. NOT covered by frontmatter
   declarations beyond `handoffs:` field; the SHAPE of the
   handoff is implicit.
3. **Inter-skill state coordination** (e.g., skill A's audit event
   triggers skill B's behavior) — covered by AuditEvent shape
   per #6 audit-trail-v2.

**Applicability**: yes.
**Severity**: serious (silent breakage on refactor).
**Coverage status**: ⚠ **partial — narrowing**.
- Sub-shape 1 (file-location-based): ✅ covered by fail-closed
  corollary (mcp-fallback-policy.md) + #17 MCP gate coverage
  comprehensiveness review (slice 23 scaffolded).
- Sub-shape 3 (audit-event-driven coordination): ✅ covered by
  AuditEvent + watch-list + event_subscriptions per #6 + #12.
- Sub-shape 2 (skill-to-skill handoffs via orchestrator): ⚠
  **REMAINING GAP** — context format, side-effect ordering,
  post-conditions of handoffs are implicit in orchestrator
  routing logic + skill body discipline. Not structurally
  enforced. Candidate fix: extend `handoffs:` frontmatter field
  to declare SHAPE (expected context fields, post-conditions,
  side-effects); audit slice candidate that walks declared
  handoffs vs actual orchestrator routing.

**Notes**: gap surfaced in session-11 architectural-gap detection
sweep. Mitigation candidates:
- Tighten plugin-conventions §7 (Routing handoff conventions) with
  explicit handoff-shape declaration.
- New audit slice 24 candidate: scan orchestrator PROCEDURE.md +
  skill `handoffs:` declarations for shape consistency. Defer
  scaffolding until #11 Cowork integration completes (handoff
  shapes likely shift then).

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

### Navigational-consolidation drift

**Description**: as ARCH grows, navigational consolidation docs (reference card, validation-gating-overview, future similar) accumulate alongside detailed source-of-truth sections. Without explicit sync discipline, the navigational docs drift from the detailed sections — readers look at one, follow it, and act on stale guidance because the detailed source has changed.

**Applicability**: yes (active concern post-session-11 with reference card + validation-gating-overview).
**Severity**: minor-to-serious (depends on how stale the navigational doc gets before noticed).
**Coverage status**: ✅ **covered** — ARCH "Maintenance discipline" rules 3 (reference card sync) + 5 (validation-gating-overview inventory sync). When changing a discipline / gate / slice / target / convention, both navigational + detailed surfaces update in same commit.
**Notes**: enforced by author discipline + design-review target 14 sweep (will detect divergence between named disciplines and navigational doc inventories).

### Discipline-bloat / over-naming

**Description**: as architectural failure modes get caught, named disciplines accumulate. Each new discipline solves a real problem at the time of naming but adds cumulative cognitive load on future readers + rule-application overhead. Without periodic pruning, the discipline set grows monotonically; eventually new readers can't keep all named rules in mind, and discipline-driven design becomes its own friction.

**Applicability**: yes (latent — session-11 added 4 new ARCH sections in v0.20-v0.22; not over-bloated yet at 11 sessions in, but trajectory matters).
**Severity**: minor today; serious if unchecked at v50+ sessions.
**Coverage status**: 🚫 **uncovered as discipline-shaped check**. Target 9 (subsumption) catches NEW commitments that subsume old ones; doesn't catch already-named disciplines that have become subsumed by later additions. Target 14 (discipline-gap) catches MISSING; doesn't catch OVER-named.
**Notes**: candidate mitigation — periodic discipline-pruning check (analogous to legacy retirement scan; runs at major version boundaries, evaluates each named discipline against "is this still load-bearing or now subsumed by later discipline + meta-rules?"). Defer mitigation until pattern of over-naming surfaces; flag as watch position.

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
