# Scope + targets

Which subsystems get reviewed, and what files belong to each.

---

## Load-bearing first-run targets

For full first-principles review, default scope is the **8
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

### Target 8 — VISION ↔ ARCHITECTURE coupling (traceability)

**Files**: `VISION.md` (whole file) + `ARCHITECTURE.md` (meta-rules
+ decision rules + maintenance discipline) + sample 3-4 ROADMAP
items (test how vision principles translate to deferred work).

**Why this matters most for the markdown layer**: most architectural
enforcement happens through skill instructions (markdown), not
deterministic Python. LLMs are smart enough to paper over weak
instructions by inference — but that's brittle, expensive, and
drifts silently as instructions evolve. Tight VISION→ARCHITECTURE
→skill-body coupling is what turns the LLM layer from "guesses
at intent" into "follows enforced contract." Pre-launch is the
unique window to verify this coupling before behavioral debt
accumulates.

**Greenfield questions**:

- For each VISION axis (intertwining, sparring, authorship
  preservation), which architectural mechanisms in ARCHITECTURE.md
  enforce it? Is the enforcement *structural* (meta-rule + entity
  placement constrains it) or only *behavioral* (skill body says
  "do X")? Behavioral-only enforcement is brittle — LLM has to
  re-derive the constraint each session.
- For each meta-rule, which VISION axis does it serve? Is the
  service load-bearing and articulable, or does the meta-rule
  float free of the vision (overhead candidate)?
- Where VISION names a requirement (e.g., "anti-sycophancy guard,"
  "counter-argument as first-class output," "selective friction
  calibration"), is there an architectural mechanism that
  operationalizes it, or is it a behavioral aspiration without
  enforcement?
- Are there VISION principles with no architectural enforcement?
  Many axis-2 (sparring) requirements may be in this category —
  sparring is partly behavioral, partly architectural. Greenfield:
  which parts NEED architecture vs. which can stay as skill-body
  conventions?
- Are there meta-rules with no clear VISION coupling? If yes —
  either the vision is incomplete OR the meta-rule is overhead
  that snuck in for tidiness.
- The "category-collapse risk" VISION names — does the architecture
  have a structural defense against it, or only a vigilance-based
  one (audit/design-review running periodically)?
- The "trust + sparring + authorship" three-layer protection
  framing in VISION — does ARCHITECTURE explicitly partition
  mechanisms by which layer they protect, or is the partition
  invisible?

**Output expectation**:

A bidirectional map:

1. **VISION → ARCH**: each VISION-named mechanism (axis 1's six
   intertwining requirements, axis 2's seven sparring requirements,
   axis 3's five authorship requirements) listed with its
   architectural enforcement: meta-rule, entity type, MCP tool,
   or skill convention. Mark each as `structural` (architecture
   constrains) or `behavioral` (skill body asserts) or `unenforced`
   (no current backing).
2. **ARCH → VISION**: each meta-rule + named convention listed
   with the VISION axes it serves. Mark each as `load-bearing`
   (axis would be unenforced without it), `supporting` (one of
   several enforcers), or `floating` (no clear coupling — overhead
   candidate).

Findings are at the **placement-soundness** level: does the
architecture actually deliver on the vision? Soundness, not
compliance. Mirror of audit slice 14's relationship to design-
review target 7 — but at the higher coupling tier (vision-
architecture, not architecture-implementation).

---

### Target 9 — Subsumption check (legacy retirement at design time)

**Files**: the new mechanism's design proposal/decision-record AND
the existing landscape it lands in (ARCHITECTURE.md current entity
inventory, current decision records, current plugin entities,
current persistence structures the new thing might replace).

**Why this matters**: adding a new mechanism without explicitly
asking "what does this subsume?" leaves load-bearing legacy in
place by inertia. Each new commitment gets layered on top, but no
one walks back and asks "is the prior decision still necessary
now that this one exists?" The audit-trail v1→v2 reversal in
session 7 is canonical: v1 added a unified JSONL log alongside
6 prose sources with dual-write discipline, when in fact 5 of 6
prose sources were subsumable. The retirement question wasn't
asked at v1 design time. v2 corrected it, but only after a fresh
review surfaced the gap.

This target exists to make the question MANDATORY at design time,
not retrospective.

**Greenfield questions** (mandatory when proposing any structural
mechanism — meta-rule, entity type, MCP tool, persistence
structure, decision record-grade commitment):

- **What does this new thing replace?** Walk every existing
  mechanism in the same domain (audit, persistence, routing,
  validation, etc.). For each: does the new mechanism subsume it
  partially, fully, or not at all?
- **What stays for non-redundant reasons?** For each mechanism
  the new thing partially or fully subsumes: what UNIQUE value
  does the legacy still carry that the new thing doesn't replace?
  ("Legacy provenance," "human-readable form," "external-tool
  compatibility," "regulatory requirement," etc. — name the
  specific load-bearing reason, not "we might want it.")
- **What can be RETIRED?** Anything where the new thing fully
  subsumes the old AND the old has no unique non-redundant value.
  Retirement is the default; preservation needs explicit
  justification.
- **Migration path for retired mechanisms**: existing instances
  (data, files, references in skills/docs) need a migration
  story. If migration is too painful, that's a signal the new
  mechanism isn't actually a clean replacement — surface the
  pain, don't paper over it.
- **Decision record for the retirement**: each retired mechanism
  gets a "supersedes" note in the new mechanism's decision record,
  AND the legacy's decision record (if one exists) gets a
  "superseded by" header. The audit trail of architectural
  evolution stays legible.

**Anti-patterns** the target catches:

- ❌ "We're adding X alongside Y" without checking if Y becomes
  redundant. Default-additive thinking.
- ❌ "Y is too established to retire" — without naming the
  specific load-bearing reason. Inertia masquerading as
  load-bearing-ness.
- ❌ Decision record proposes new mechanism with no "what does
  this replace?" section. Mandatory section.
- ❌ Retirement deferred to "future cleanup" — that future never
  comes, and the legacy continues consuming maintenance attention.

**Output expectation**:

For each new structural mechanism reviewed:

1. **Subsumption table**: existing mechanism × {fully-subsumed |
   partially-subsumed | unaffected} × name unique-value-retained
   if not fully subsumed.
2. **Retirement list**: which existing mechanisms can/should be
   retired. Include migration sketch.
3. **Preservation justifications**: for each "preserved alongside"
   item, the specific load-bearing reason. Reject "might be
   useful," "established," "we're used to it."
4. **Required decision-record sections**: list of
   `supersedes` / `superseded by` notes the decision records need.

**When to invoke**: at design time for any new commitment grade
mechanism (decision record-worthy proposal, meta-rule addition,
new entity type, new persistence structure). NOT for incremental
patches or skill-level changes — those rarely subsume anything.

**Relationship to slice 18**: target 9 is the prospective check
(at design time, cheap to fix). Slice 18 is the retrospective
sweep (catches what target 9 missed across the whole stack).
Both, not either.

---

### Target 10 — Pattern-vs-instance check

**Files**: the new mechanism's design proposal/decision-record AND
the architectural placement question (does this go in pattern
layer or instance layer? is the proposed shape domain-agnostic
or PBS-coupled?).

**Why this matters**: per `ARCHITECTURE.md` "Pattern-vs-instance
discipline" (v0.8+), every architectural commitment in this repo
must work at pattern level, not just for PBS. PBS is the pioneer
instance; the architecture is the pattern. The long-arc end-state
is an AI-office builder (`ROADMAP.md` v2) that scaffolds new
domain offices from accumulated patterns. Every commitment that
doesn't generalize is a future migration cost; every commitment
that does generalize *is* the builder's foundation. Catching
PBS-coupling at design time is much cheaper than retrofitting
later.

This target is the prospective-check companion to audit slice 19
(retrospective sweep). Same prep-vs-review pairing as target 9 +
slice 18.

**Greenfield questions** (mandatory when proposing any new
meta-rule, entity type, persistence structure, MCP tool, or
decision-record-grade commitment):

- **Would this work for a hypothetical legal-practice office?**
  (Workflow: intake / discovery / filing / argument. Authorities:
  courts / opposing-counsel / regulators. Memory taxonomy:
  precedents / citations / templates.)
- **Would this work for a hypothetical research-paper-review
  office?** (Workflow: draft / review / revision / publication.
  Authorities: journals / co-authors / reviewers. Memory taxonomy:
  citations / prior-work / templates.)
- **Would this work for a hypothetical engineering-doc / medical-
  records / regulatory-filing office?** (At least one more
  structurally-distinct domain.)
- **If yes for at least 2 of 3**: pattern-level. Lock in.
- **If no for most**: too PBS-coupled. Push to instance layer
  (skill bodies, manifests, office-config values) instead of
  pattern layer (meta-rules, schema shapes, MCP interfaces).

**Per-element placement test**:

- Does the rule/schema/interface name PBS-specific terminology
  (B-Plan, Begründung, Festsetzungen, gesetze, UNB) in its
  *body* or *contract*? If yes → instance content leaking into
  pattern. If only in *examples*, that's allowed (legibility).
- Does it assume German legal taxonomy or planning workflow at
  the schema level? If yes → too coupled.
- Does the *shape* generalize even if the *vocabulary* is
  PBS-flavored? If yes → fine, just ensure the shape is what
  the architecture commits to, not the vocabulary.

**Anti-patterns** the target catches:

- ❌ A meta-rule whose body names "B-Plan" / "Begründung" /
  "Festsetzungen" as load-bearing concepts. Pattern is the *shape*
  (e.g., "doctypes have required + optional sections per their
  manifest entry"); instance is the doctype list.
- ❌ A persistence structure assuming German legal taxonomy
  (gesetze / urteile / leitfäden) at the architectural layer.
  Pattern is "layered references manifest with invalidation
  contract"; instance is the German-law taxonomy.
- ❌ An MCP tool whose interface embeds domain knowledge in the
  signature (e.g., `validate_b_plan_begruendung`). Pattern is
  `validate_doctype(slug)`; instance is the doctype list.
- ❌ A Pydantic model whose required fields are PBS-specific
  (e.g., `b_plan_nr: str`). Pattern is core-with-extension shape
  (`ProjectStateCore + PBSProjectStateExtension`); instance is the
  PBS-extension fields.
- ❌ A decision record whose "Decision" section frames the
  commitment in PBS-only terms even when the underlying rule
  generalizes. Reformulate the commitment at pattern level; cite
  PBS as the example.

**Exceptions** (where domain-coupling at architecture layer is
allowed):

- Vocabulary in *examples*: "PBS bausteine" in an example to
  illustrate a generic rule is fine. The rule itself must stay
  generic.
- The instance directory itself (`extensions/`, `memory/`,
  populated `office-config.yaml` values) is unconditionally
  PBS-instance content. Pattern is the *schema*; PBS is the
  *content*.

**Output expectation**:

For each new mechanism reviewed:

1. **Pattern-level claim**: would it work for 3-5 hypothetical
   domains? List which ones it fits and which it would need
   adaptation for.
2. **Coupling findings**: any PBS-specific terminology, taxonomy,
   or assumptions baked into the proposed pattern layer.
3. **Refactor proposal** for any coupling found: how to push the
   PBS-specific part to instance layer (skill bodies, manifests,
   config values) while keeping the pattern at architecture layer.
4. **Validation signal note**: under the single-domain-pioneer
   constraint (`ARCHITECTURE.md`), only signal #1 is checkable
   immediately (does it work for PBS post-refactor?). Signal #2
   (does it work for other domains?) waits for real implementation
   in those domains and may never arrive. The reviewer must
   acknowledge this — pattern-level claims are best-effort, not
   empirically validated, until/unless second-domain implementation
   happens.

**When to invoke**: at design time for any new commitment
(decision record-worthy proposal, meta-rule addition, new entity
type, new persistence structure, new Pydantic model, new MCP tool
interface). NOT for incremental skill-level changes — those rarely
add architectural commitments.

**Relationship to slice 19**: target 10 is the prospective check
(at design time, cheap to fix). Slice 19 is the retrospective
sweep (catches what target 10 missed across the whole stack —
e.g., decision records written before this discipline existed).
Both, not either.

**Relationship to target 9 (Subsumption check)**: different
question. Target 9 asks "what does this *replace*?" Target 10
asks "is this at the right *level* (pattern vs instance)?"
Both apply at design time; both belong.

---

### Target 11 — Entity-elevation check (managed entity over-modeling)

**Files**: any decision record, refactor proposal, or commitment
design that proposes a new managed entity (Pydantic schema +
MCP CRUD tools + persistence) at office-level or department-level.

**Why this matters**: per `ARCHITECTURE.md` "Entity-elevation
discipline" (v0.13+), the architecture must stay closer to
**knowledge graph + document store with stable references** than
relational SQL schema. Pre-emptively elevating concepts to
first-class managed entities creates schema sprawl that LLMs
don't think well in. Every concept proposed as "an entity" should
prove it actually is one — most fail and resolve to event-kinds
+ nested fields + memory entries.

This target is the prospective-check companion to audit slice 20
(retrospective sweep). Same prep-vs-review pairing as target 9 +
slice 18 and target 10 + slice 19.

**The 3-test (all three required to elevate to managed entity)**:

For each proposed entity, the reviewer walks all three:

1. **Stable identity** — has an ID/slug that persists across
   sessions and is referenced by other things?
2. **State of record** — has fields whose authoritative current
   value matters (not just historical record)?
3. **Lifecycle** — has phases or status that progress over time?

**If all three**: managed entity. Lock in.
**If any missing**: route to the appropriate alternative
primitive — event-kinds (for moments-when-things-happened),
nested fields (for data only meaningful in context of a parent),
memory entries (for prose-shaped knowledge), or reference data
(for static/configuration values).

**Worked-example reasoning patterns**:

| Concept | Verdict | Why |
|---|---|---|
| Project, Client, Actor, Invoice, Asset, Matter, Manuscript | ✅ entity | All three apply: persistent identity, evolving state, lifecycle |
| Approval, Decision, Send, PhaseTransition | ❌ event kinds | Each is a moment, not a thing with state evolving over time |
| LineItem, Deadline, ContactPerson | ❌ nested fields | Only meaningful as data on a parent entity |
| Notification | ❌ adapter + event | Receiving channel (inbox) is state-of-record; PBS handles trigger + delivery + log |
| Report | ❌ generated artifact | Projection on demand, not entity with persistent state |
| BusinessCalendar | ❌ reference data | No lifecycle (static); fits as office-config field |
| DocumentVersion | ❌ event + bytes | Snapshot is immutable; capture as send event with causes[] chain + snapshot bytes |
| Conflict-of-interest | depends | Pattern-level: not architecture; per-department per-domain (legal practice has its own Conflict managed entity if its 3-test passes there) |

**Anti-patterns** the target catches:

- ❌ Proposing a managed entity for a moment-when-something-
  happened (Approval, Decision, Action, StateTransition). These
  are events, not entities.
- ❌ Proposing a managed entity for data that only makes sense
  in context of a parent (LineItem, Deadline, ContactPerson,
  PhaseEntry). These are nested fields.
- ❌ Proposing a managed entity for generated artifacts (Report,
  Dashboard, RenderedTimeline). These are projections.
- ❌ Proposing a managed entity for static reference data
  (BusinessCalendar, HolidayCalendar, CountryList). These are
  configuration / reference content.
- ❌ Proposing a managed entity for state owned by an external
  system (Notification-after-delivery, Email-in-inbox,
  Calendar-event-after-sync). These are adapter-mode where the
  external system is system-of-record.
- ❌ Proposing a "container" entity to group related entities
  when ID-references + audit-trail filters suffice (no need
  for a CustomerProjects entity that lists Project IDs — just
  query Projects where client_id=X).

**Exceptions** (where elevation is justified despite the test
feeling marginal):

- **Borderline-on-lifecycle**: if identity + state are clearly
  yes but lifecycle is "evolves slowly over years" rather than
  through explicit phases (e.g., Actor: joined → active → left,
  but the transitions are implicit not workflow-driven), the
  elevation is still right — Actor IS an entity. Lifecycle
  question relaxes when the other two are strong.
- **Borderline-on-state**: rare; usually means it's actually
  reference data, not entity. Resist elevation.

**Output expectation**:

For each proposed managed entity:

1. **3-test verdict per criterion**: identity (yes/no + why),
   state (yes/no + why), lifecycle (yes/no + why). Explicit, not
   hand-waved.
2. **Verdict**: ✅ entity / ❌ alternative-primitive (specify which)
3. **If ❌**: the recommended alternative primitive shape — event
   kinds (with proposed `kind:` values), nested fields (with
   proposed parent entity), memory record kind, reference data
   shape, or adapter Protocol contract.
4. **If ✅**: confirm the entity belongs at office-level or
   department-level (which department); native or adapter
   delivery mode.

**When to invoke**: at design time for any decision record /
refactor / commitment that proposes one or more new managed
entities. NOT for incremental skill-level changes (skills don't
typically introduce entities). MUST be invoked when:

- A decision record names a new Pydantic-modeled entity type
- A refactor proposes splitting an existing entity into multiple
- A new commitment scope includes "we'll add a [Foo] entity"
- A department module's `department.yaml` declares
  `managed_entities:` (each declared entry runs the 3-test)

**Relationship to slice 20**: target 11 is the prospective check
(at design time, cheap to refuse the elevation). Slice 20 is the
retrospective sweep (catches what target 11 missed across the
whole stack — entities introduced before this discipline existed,
or that drifted from valid 3-test status). Both, not either.

**Relationship to targets 9 and 10**: complementary checks.
Target 9 asks "what does this *replace*?" Target 10 asks "is this
at the right *level* (pattern vs instance)?" Target 11 asks "is
this *entity-shaped at all* (vs event/nested/memory/config)?"
All three apply at design time; all three belong.

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
