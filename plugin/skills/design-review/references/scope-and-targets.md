# Scope + targets

Which subsystems get reviewed, and what files belong to each.

---

## Load-bearing first-run targets

For full first-principles review, default scope is the **14
foundations** below (targets 1-11 from sessions 5-9; target 12
added session 10 for entity-md authoring conformance; targets
13-14 added session-10 followup as discipline-discovery and
discipline-gap-detection lenses). These are the subsystems from
which everything else inherits shape. Wrong-shape there ripples
through the system; wrong-shape in a leaf is local.

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

### Target 12 — Entity-md authoring conformance (hybrid-shape contract)

**Files**: any new or modified entity-md file under
`extensions/**/*.md` (doctype, reference, project, client, actor,
process, baustein-elevated-to-entity, etc.). Also any decision
record or refactor proposing a new managed-entity type.

**Why this matters**: per `ARCHITECTURE.md` "AI-as-runtime
hybrid-shape principle" (v0.16+) and
`docs/decisions/ai-as-runtime-hybrid-shape.md`, every managed
entity follows a three-layer frontmatter contract (Layer 1
universal Pydantic base + Layer 2 per-entity-type subclass +
Layer 3 per-deployment extension) plus recommended body
conventions per type. This target enforces conformance at
authoring time before drift accumulates across `extensions/`.

This target is the prospective-check companion to audit slice 21
(retrospective sweep). Same prep-vs-review pairing as target 11 +
slice 20.

**The conformance checks**:

For each entity-md being authored or modified:

1. **Layer 1 frontmatter** — required fields present (`id`,
   `label`, `type`, `scope`, `scope_key`, `status`,
   `last_updated`); values match expected enums; `id` is
   kebab-case + unique-in-scope.
2. **Layer 2 frontmatter** — fields match the Pydantic subclass
   for the declared `type:`; required fields present; types
   match.
3. **Body section conformance** — recommended sections per the
   entity type's body-spec (per
   `docs/conventions/entity-md-spec.md`) are present. Empty
   sections warned, not failed. Missing sections suggested with
   a draft prompt.
4. **Cross-references** — `<entity>_id:` fields point to existing
   entities (gate validates at write time; this target catches
   typos before write).
5. **Hybrid-shape principle adherence** — body contains prose-
   shaped content (process flow, conditional rules, domain
   knowledge); structured-only content stays in frontmatter.
   Catches "writing a YAML file with a markdown body that's just
   filler" — both halves should carry real content per their
   layer.

**Anti-patterns the target catches**:

- ❌ Frontmatter-only entity-md (empty body) when the type's
  body conventions call for ≥1 substantive section.
- ❌ Body-only entity-md (no frontmatter) — gate would fail
  read; catch at authoring.
- ❌ Prose stuffed into Layer 2 fields (`description: > ...`
  with multi-paragraph content). Move to body.
- ❌ Structured data in body (tables that should be Layer 2
  fields, e.g., `paired_with` declared in body prose instead of
  frontmatter).
- ❌ Section names that drift from the body-spec (e.g.,
  `## Application Notes` instead of `## When this applies`).
- ❌ Missing entity-elevation 3-test verdict (when the entity is
  newly proposed) — coordinates with target 11.

**Output expectation**:

For each entity-md reviewed:

1. **Layer 1 conformance**: ✅ pass / ❌ list missing fields /
   ⚠ enum values to fix
2. **Layer 2 conformance**: ✅ pass / ❌ list missing or wrong-
   typed fields
3. **Body sections**: list of present + missing recommended
   sections; quality assessment per present section (substantive
   vs filler)
4. **Cross-refs**: any unresolved `<entity>_id:` references
5. **Recommendations**: specific edits to bring conformance

**When to invoke**:

- At authoring time for any new entity-md
- Before promoting a baustein/memory entry to entity status
- During refactor that touches multiple entity-mds at once
- Periodically as `extensions/**/*.md` grows large

**Relationship to other targets + slices**:

- **Target 11** (entity-elevation): runs FIRST — confirms the
  thing should be an entity at all. Target 12 then validates the
  entity-md shape. Target 11 = "is this entity-shaped?"; target
  12 = "is this entity-md correctly written?"
- **Audit slice 21** (retrospective entity-md scan): catches
  drift across `extensions/**/*.md` over time. Target 12 is
  prospective; slice 21 is retrospective.
- **Implementation note**: this target is **scheduled for
  first-run alongside #9** (when the generic entity gate +
  Layer-2 Pydantic subclasses land). Body-spec reference at
  `docs/conventions/entity-md-spec.md` carries the per-type
  conventions this target validates against.

### Target 13 — Pattern emergence / unnamed convergence

**Files**: cross-cutting scan across the whole repo. Specifically:

- `ARCHITECTURE.md` — named disciplines (the index of what's
  *known*)
- `plugin/skills/**/SKILL.md` — implementation surfaces
- `backend/mcp-server/src/pbs_mcp/**/*.py` — implementation
  surfaces
- `extensions/**/*.{yaml,md}` — content surfaces
- `memory/**/*.md` — content surfaces
- `docs/decisions/*.md` — historical decisions (sometimes
  contain unnamed pattern observations)

**Why this matters**: existing audit + design-review modes catch
**deviations from named disciplines**. Neither catches **missing
disciplines themselves** — patterns that have emerged across ≥2
surfaces independently without being named, then drift apart
because the convergence isn't enforced. Session-10 case:
hybrid-shape (frontmatter + md body) was independently present in
memory + skills + state.md for 6+ months without being named as
discipline. Department.yaml was on track to drift into pure-YAML,
breaking the unnamed convergence.

This target adds the **discovery-mode** lens: scan structurally
similar implementations across surfaces; flag those that *should*
be a named discipline but aren't.

**Methodology** (the agent's reasoning steps):

1. **Identify candidate convergent patterns** — scan structurally
   across surfaces. Look for:
   - Repeated frontmatter shapes (same fields appearing in 3+
     unrelated files)
   - Repeated workflow shapes (skills with similar phase
     structure)
   - Repeated error-handling patterns
   - Repeated cross-cutting metadata (e.g., `last_updated:` in
     multiple manifest types)
   - Repeated body/section conventions used informally
2. **Filter for unnamed-but-convergent**: cross-reference against
   `ARCHITECTURE.md` named disciplines + `docs/decisions/*.md`
   committed records. If the convergent pattern doesn't appear
   in either, it's a candidate for elevation.
3. **Rank by surface count + impact**:
   - Surface count: ≥3 surfaces strong; 2 surfaces weak
   - Impact: would naming it influence ≥1 pre-RAG commitment?
     (cross-cutting impact)
4. **Recommend elevation** for high-rank candidates: propose
   discipline name + scope + decision-record draft outline +
   ARCHITECTURE bump shape.

**Anti-patterns the target catches**:

- ❌ Three skills implementing the same retry pattern without it
  being a named discipline; future skills will reinvent.
- ❌ Two manifest types using the same scope-axis layering
  without it being named; third manifest type drifts into a
  different shape.
- ❌ Hybrid-shape (the session-10 case): three surfaces using
  frontmatter + md body without it being principled; new
  surface (department.yaml) was on track to break it.
- ❌ Repeated cross-reference syntaxes (some skills use
  `[[wikilink]]`, some `[md](link)`, some `<id>` plain) — should
  be unified as convention.

**What this target does NOT catch** (acknowledged limitations):

- Patterns present in only ONE surface (no convergence yet —
  pattern emergence requires ≥2)
- Patterns convergent but **correctly named** (target 13 is for
  *unnamed* convergence — named convergent disciplines are out
  of scope; that's audit's job)
- Failure modes uncovered by any pattern at all (that's target
  14's job — discipline gap detection)

**Output expectation**:

For each candidate convergent pattern:

1. **Pattern description**: the structural shape that's recurring
2. **Surfaces where present**: list of files/modules + how each
   instantiates it
3. **Drift risk**: which planned surfaces (commitments not yet
   shipped) might drift away from the pattern if it stays unnamed
4. **Recommendation**: elevate (with draft discipline name +
   scope + DR outline) / dismiss (with reasoning, e.g., "two
   surfaces is coincidence, not convergence") / monitor (≥3
   surfaces but cross-cutting impact uncertain — re-scan in 1
   session)

**When to invoke**:

- Annually as a planned discipline-discovery cadence
- Before major architectural shifts (pre-#11 would have caught
  hybrid-shape)
- After session-postmortem of any architectural surprise (when
  the user catches a gap spontaneously, run this target to scan
  for related gaps)
- After session 10's hybrid-shape codification — first-run
  recommended

**Relationship to other targets + slices**:

- **Target 14 (discipline gap)**: complementary. Target 13 starts
  from existing surfaces and asks "is there a name for this?"
  Target 14 starts from a failure-mode catalog and asks "is
  there a discipline preventing this?" Both can catch the same
  thing (session 10's hybrid-shape was both); having both is
  robustness.
- **No specific audit slice pairing**: target 13 is fundamentally
  prospective + discovery-mode; the corresponding "retrospective"
  is hard to define (you can't audit what you haven't named).
  Re-running target 13 itself plays both roles.

### Target 14 — Discipline-gap detection

**Files**: `ARCHITECTURE.md` (named disciplines + meta-rules) +
`plugin/skills/design-review/references/failure-mode-catalog.md`
(the catalog itself) + cross-reference against
`plugin/skills/audit/references/drift-surfaces-and-slices.md` (to
identify which failure modes have audit coverage already).

**Why this matters**: target 13 starts from existing-surfaces
convergence and asks "is there a name for this?" Target 14 starts
from **architectural failure modes** and asks "is there a named
discipline that prevents this failure?" Different evidence base,
different coverage. Some failure modes are not visible as
convergence yet (no surface has implemented them poorly enough
for the pattern to emerge) but could still bite — proactive
catalog scan catches these.

This target's **load-bearing reference** is
`plugin/skills/design-review/references/failure-mode-catalog.md`
— a living catalog of architectural failure modes with their
named protections (or "uncovered" status). Target 14 maintains
this catalog (adds new modes from postmortems; updates coverage
status as new disciplines land).

**Methodology** (the agent's reasoning steps):

1. **Read `failure-mode-catalog.md`** — the canonical list of
   architectural failure modes seen in this and adjacent
   architectures.
2. **For each failure mode**: identify which named discipline (in
   ARCHITECTURE.md) protects against it, OR mark as "uncovered."
3. **For uncovered modes**:
   - Assess applicability to PBS today (does this failure mode
     have any plausible vector here?)
   - Assess severity (catastrophic / serious / minor)
   - Assess proximity (immediate-risk / theoretical)
4. **Recommend**: codify-now (high applicability + serious +
   immediate) / codify-on-trigger (theoretical-but-plausible) /
   acknowledge-and-skip (not applicable to PBS shape, e.g.,
   distributed-systems failures don't apply to single-process
   PBS today).

**Catalog seeding** (initial entries from session 10
postmortem):

- **Silent convergence** — multiple surfaces implementing same
  pattern unnamed → drift over time. **Now covered**: target 13
  (pattern emergence). ✅
- **Prose-in-block-scalars** — prose-shaped content squeezed
  into structured fields (YAML `description: >`, `notes: |`)
  that suppress its natural form. **Now covered**: AI-as-runtime
  hybrid-shape principle. ✅
- **Encoded-rules-when-AI-as-runtime-was-available** — rules
  expressed in code or prose-as-encoded-procedure when AI-read-
  prose would have served. **Now covered**: AI-as-runtime
  hybrid-shape principle. ✅

Additional catalog entries (literature-derived, status =
"covered" / "uncovered" / "n/a"):

- **SQL-DB trap** (Oracle-shape architecture for LLM-mediated
  systems) → covered by entity-elevation discipline + AI-as-
  runtime hybrid-shape. ✅
- **Source-of-truth ambiguity** (data exists in 2+ places, no
  invalidation contract) → covered by meta-rule 3 (source-of-
  truth & invalidation). ✅
- **Configuration-vs-code drift** (config and code expressing
  same rule, drifting over time) → partially covered by meta-
  rule 4 (execution determinism); evaluate after #9.
- **Hidden-global-state** (state read/mutated outside
  declared dependencies) → partially covered by strict-validation
  + fail-closed corollary; full coverage TBD.
- **Cargo-cult patterns** (pattern adopted from another codebase
  without understanding why) → uncovered. Low-priority; hard to
  catch structurally.
- **Hardcoded-instance-content-in-pattern-layer** → covered by
  pattern-vs-instance discipline. ✅
- **Vendor-lock at architecture layer** → covered by glue-not-
  replacement principle. ✅
- **Monolithic-skill-bundle** (one skill doing too much) →
  uncovered as named discipline; partially handled by
  skill-conventions §X. Evaluate.
- **Implicit-contract-between-skills** (skills coordinate via
  conventions not declared in frontmatter) → partially covered
  by `mcp_tools_required[]` + handoffs. Evaluate.

The catalog is a **living document**: every postmortem, every
new architectural discipline, every novel failure mode discovered
in production updates it.

**Output expectation**:

1. **Catalog status table**: each failure mode with current
   coverage status
2. **Newly uncovered modes** (high applicability + serious +
   immediate): recommended discipline name + scope + DR outline
3. **Newly added modes** (from session postmortems since last
   target-14 run): catalog entry text
4. **Coverage transitions** (modes whose status changed since
   last run, e.g., "covered" after a new discipline shipped)

**When to invoke**:

- Annually as planned cadence
- After every architectural surprise (postmortem feeds catalog)
- Before major architectural shifts (catch uncovered modes
  before commitments lock)
- After ARCHITECTURE.md major version bumps (re-evaluate
  coverage)

**Relationship to other targets**:

- **Target 13 (pattern emergence)**: complementary. 13 looks
  bottom-up from code; 14 looks top-down from failure-mode
  catalog. Some failures show up in both lenses (hybrid-shape);
  some only in one.
- **Target 9 (subsumption)**: orthogonal. Target 9 asks "what
  does this new thing replace?"; target 14 asks "what failure
  mode does this new thing prevent?"
- **Implementation note**: catalog seeded with session-10
  postmortem + literature-derived modes; first-run scheduled
  immediately (no dependencies — operates on existing
  ARCHITECTURE + catalog).

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
