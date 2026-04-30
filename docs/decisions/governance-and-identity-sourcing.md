# Decision record: Governance scaling, identity sourcing, and office conventions as prose-rules

**Status**: ACCEPTED (session 11, 2026-04-30)
**Owner**: ROADMAP commitment #13 governance arc; #15 Actor entity; #6 approval events; ARCHITECTURE.md "AI-as-runtime hybrid-shape principle" extension
**Related**: `ai-as-runtime-hybrid-shape.md` (#16 — central mechanism), `office-vs-department.md` (#12 — entity-elevation discipline), ROADMAP commitments #13 (deployment flexibility) + #15 (Client + Actor) + #6 (audit-trail v2 + approval events)

## Context

Session 11 surfaced three interconnected architectural questions during a product-vision conversation, each branching from "how does this scale across deployments and organization sizes":

1. **Governance scaling** — how does governance work as the organization grows from solo to multi-department to enterprise?
2. **Identity sourcing** — how does PBS know who's connecting and what their roles/permissions are?
3. **Office conventions** — how do bureaus express deployment-specific rules (identifier patterns, naming, archival policies) without writing code or inventing config DSL?

All three turned out to be applications of the same architectural mechanism: **AI-as-runtime hybrid-shape (#16)**. The answers compose, which is why this is a single decision record rather than three.

The three questions arose from a "what does adoption at scale look like" conversation about consulting-deployment scenarios. Captured now while the design discussion is fresh, before context fades.

## Decisions

### 1. Governance scaling — existing primitives compose; no separate "governance system" needed

The architecture's existing primitives compose into governance scaling without inventing new infrastructure. The spectrum:

| Org size | Governance need | Primary mechanism |
|---|---|---|
| Solo (Schulz today) | None — direct edit fine | File-system access |
| 2-5 people | Informal coordination | Git workflow + verbal sync |
| 5-20 people | Light formalization — who can change what | **Git PRs + code-owners** + audit trail |
| 20-100 people | Role-based approval for schema/prose changes | **Existing primitives extend**: Actor.roles (#15) + approval events (#6) + AuditEvent.actor — gate-side check on writes |
| 100-1000 people | Department-isolated governance + cross-department coordination | **#12's department isolation** + per-department approvers + cross-dept events |
| 1000+ people / regulated | Federated multi-tenant authority | **Tier 3 / Gemini Enterprise** (separate archetype) |

**Most of the spectrum is addressable WITHOUT Tier 3 / Gemini Enterprise.** Git is the unsung hero up to ~20 people; gate-level role enforcement extends to ~100; department isolation extends to ~1000. Gemini's federated complexity earns its keep only at very-large/regulated scale.

#### Layered enforcement: defense-in-depth

Three enforcement layers, complementary:

| Layer | Who/what enforces | What it catches |
|---|---|---|
| **Git** | Repository host (GitHub/GitLab) — branch protection, code-owners, signed commits | All file changes that flow through git (most of them) |
| **MCP gate (Python)** | Backend code in `pbs_mcp` — `write_entity` checks authenticated Actor's roles before writing | Runtime writes via the gate (Cowork sessions, automated workflows) |
| **Skill (LLM)** | Skill body prose: "before writing X, check role; if not authorized, surface approval workflow" | The user-facing UX of the approval workflow (NOT enforcement) |

**Critical: the LLM is NOT the enforcer.** LLMs can be jailbroken, prompted around constraints, hallucinate. Putting governance solely in skill bodies = vulnerable. The structured layer (Python gate, code, deterministic) does the rejection/approval check; the prose layer (skill bodies, AI reasoning) explains the situation, routes the approval workflow, communicates with humans. AI is the runtime that fuses them — but the *structured* part is what stops unauthorized writes.

This is the AI-as-runtime principle (#16) applied to governance specifically.

#### Concrete flow: junior tries to edit a Layer-2 schema

```
1. alice (junior) is in a Cowork session, asks AI to draft a schema change
2. AI (skill) drafts the change, calls write_entity(path, new_schema)
3. Gate (Python) checks: alice's roles vs entity-type write requirements
4. Layer-2 schema requires role=architect → alice doesn't have it
5. Gate returns: 403 unauthorized; reason: "junior role can't write Layer-2 schemas"
6. Skill (LLM) receives the error, surfaces to alice:
   "This change needs an architect's approval. Want to request it from Bob?"
7. alice confirms → skill emits approval_requested event (per #6)
8. Bob (architect) sees the request via watch-list at his next session-open
9. Bob reviews + approves → emits approval_granted event
10. Gate now allows the write under that approval context (records both events)
```

Step 4 is **Python**. Step 6-9 is **LLM-orchestrated workflow** running on top of the deterministic check. Step 4 cannot be bypassed by clever prompting because it's in the gate code, not in the LLM's instructions.

#### Tier-conditional enforcement

The gate-level role enforcement code can EXIST in the Python backend without being load-bearing today; it activates when Tier 2 (multi-user cloud) deploys.

| Tier | Gate enforcement | Governance layer used |
|---|---|---|
| **Tier 1 (local stdio)** | Trivial — single user, role-checking adds no value | **Git** is the only meaningful layer |
| **Tier 2 (cloud HTTP, multi-user)** | Real — multiple authenticated Actors, gate enforces per-request | **Git + gate** (the medium-scale answer) |
| **Tier 3 (federated/Gemini)** | Federated — A2A signed agent cards, multi-tenant authority | **Git + gate + federated approval** (enterprise/regulated) |

Build the enforcement once (in #13's pre-RAG scope), use it tier-conditionally.

### 2. Identity sourcing — native or adapter, with two distinct adapters at play

Two related-but-distinct things:

| Question | What sources it | Example providers |
|---|---|---|
| **Authentication** — who is this connecting session? | Auth provider (token + identity confirmation) | Google Workspace SSO, Coolify SSO, OAuth providers, A2A signed agent cards |
| **Authorization data** — what are alice's roles, departments, attributes? | Actor entity (sourced natively or via adapter from HR) | Native md file, Personio, BambooHR, Microsoft Entra, custom |

These can be the same system (Coolify SSO might do both) or different (Google for auth, Personio for HR data). PBS architecture handles either via the same adapter pattern (meta-rule 1, generalized in #9 to managed entities).

#### Three deployment patterns

**Pattern 1: Native mode — Actor entity is source of truth**

```yaml
# extensions/office/actors/alice-mueller.md
---
id: alice-mueller
type: actor
scope: office
email: alice@schulz-planung.de
roles: [planning, junior]
departments: [planning]
---
```

PBS owns the data. Auth provider just confirms identity (token validates → email matches Actor.email). Roles/permissions come from PBS.

- **Pros**: simple, works in Tier 1, no external dependency
- **Cons**: HR system + PBS drift; manually keep alice's roles in sync if she gets promoted

**Pattern 2: Adapter mode — external HR/identity system is source of truth**

```yaml
# extensions/office/actors/12345.md (Personio internal ID)
---
id: actor-12345
type: actor
scope: office
mode: adapter
adapter: personio
adapter_config_ref: office-config.actors.external_lookup
---

# Alice Müller

This actor's identity is sourced from Personio. Roles + departments
hydrated at session-open via personio adapter.
```

PBS reads from external system at session-open. Adapter implements the Pydantic Protocol (per #15 + #11), translates external data → ActorEntity shape.

- **Pros**: HR system stays source of truth; promotion in Personio → automatic role update in PBS
- **Cons**: requires adapter implementation; introduces a runtime dependency; auth-side coupled to HR

**Pattern 3: Hybrid — auth from one system, authorization from PBS native**

Most realistic for many bureaus. Auth via Coolify SSO (or Google Workspace). Roles + departments + permissions stored in PBS Actor entity. When alice logs in:

1. Coolify SSO authenticates alice → returns email + token
2. PBS gate maps email → Actor.id (lookup in office Actor store)
3. PBS uses Actor's stored roles for authorization

- **Pros**: SSO handles passwords/MFA/account lifecycle; PBS handles its own role model
- **Cons**: dual sources for actor data (auth side + PBS side) — need to keep email mapping in sync

#### Concrete worked flow — Schulz Planungsbüro at hypothetical 30-person scale

`office-config.yaml`:

```yaml
auth:
  provider: google-workspace
  oauth_client_ref: ${GOOGLE_OAUTH_CLIENT}
actors:
  mode: adapter
  adapter: personio
  adapter_config_ref: ${PERSONIO_API_KEY}
```

Session-open flow when alice connects via Cowork:

```
1. Cowork → Google Workspace OAuth → token confirmed; email = alice@schulz.de
2. PBS gate receives request with token
3. Gate validates token → extracts email
4. Gate hydrates Actor:
   - Calls personio adapter: get_actor_by_email("alice@schulz.de")
   - Personio returns: {id: "12345", email: ..., role: "junior",
                        department: "planning", hire_date: "2024-..."}
   - Adapter translates Personio shape → ActorEntity shape (Pydantic)
5. Gate caches ActorEntity for the session: actor=alice, roles=[junior, planning]
6. Subsequent gate calls (write_entity, etc.) use cached Actor for authz checks
```

When alice gets promoted in Personio (junior → senior), next session-open hydrates the new role automatically. No manual PBS update.

### 3. Identifier uniqueness conventions — per-deployment, documented in office-config or department.md

Per entity-md-spec §3, `id` is kebab-case + **unique within scope**, and file basename equals `id`. So `alice.md` only works if there's exactly one alice in scope. With multiple alices, name collisions break the contract.

**Conventions (deployment-dependent)**:

| Strategy | Form | Use case |
|---|---|---|
| Firstname-lastname | `alice-mueller.md` | Native mode, small bureau, low collision risk |
| Email-prefix derived | `alice-mueller-schulz-de.md` | Native mode with email patterns; ugly but always unique |
| HR-system internal ID | `actor-12345.md` | Adapter mode (Personio, BambooHR); humans rarely see filename |
| Hybrid | `actor-12345.md` (filename) + `Alice Müller` (label in body) | Adapter mode with human-readable display |

**The choice is per-deployment.** Office-config or department.md should document the convention explicitly:

```yaml
# office-config.yaml or department.md frontmatter
actors:
  id_convention: firstname-lastname-from-email
  collision_strategy: append-initial  # firstname-lastname-m for second collision
```

Or — the more powerful option — express the convention as **prose** (next decision below).

### 4. Office conventions as prose-rules — the unifying mechanism

The strongest application of #16 (AI-as-runtime hybrid-shape) we've surfaced: **office-specific conventions live in markdown prose, AI applies them at runtime**.

#### The pattern

A bureau writes a convention rule in prose, alongside the data it governs. When that convention applies (creating a new actor, archiving a project, naming a doctype instance), AI:

1. Reads the rule
2. Extracts relevant context (email, project state, etc.)
3. Applies the rule
4. Asks the user for missing input if the rule needs it
5. Persists the result in the right shape
6. Audit event records both the rule application and the produced artifact

If the rule changes (bureau decides to switch from `firstname-lastname` to `email-prefix-derived`), they edit the prose. AI from then on follows the new rule. Existing artifacts stay as-minted under the prior rule. Audit trail captures rule evolution. **No code change. No migration.**

#### Worked example — actor ID convention

```markdown
# office-config.md body, or extensions/office/conventions.md

## Actor identifier convention

Actor IDs follow `<firstname>-<lastname>`, derived from the
`<firstname>.<lastname>@schulz-planung.de` company email pattern.

When adding a new actor:
1. Prefer email-derived if email matches the pattern
2. If email doesn't match (external collaborator, contractor), ask
   the user for explicit ID (kebab-case)
3. If a collision arises (two `alice-mueller`s), append middle
   initial: `alice-m-mueller`. If still colliding, escalate to
   senior — likely use HR system ID instead.

This convention applies to native mode. Adapter mode uses the
HR system's internal ID; this convention does not apply.
```

Concrete flow when `alice.mueller@schulz-planung.de` joins:

```
1. AI reads conventions.md, finds the actor identifier rule
2. Extracts email prefix: "alice.mueller"
3. Converts to kebab-case: "alice-mueller"
4. Checks for collisions: extensions/office/actors/alice-mueller.md exists?
5. No collision → mints id="alice-mueller", creates the file
6. Audit event: actor_minted, details={rule: conventions.md#actor-identifier-convention,
   input: alice.mueller@schulz-planung.de, output_id: alice-mueller}
```

#### Why this is powerful

- **Conventions are deployment-instance data**, not pattern-level architecture. Per pattern-vs-instance discipline, they don't belong in code or in shared schemas.
- **Conventions evolve** — bureaus refine them as they accumulate experience. Markdown edit > code refactor.
- **AI handles ambiguity natively** — "if email doesn't match the pattern, ask for explicit ID" is naturally interpreted by an LLM; awkward to encode in deterministic config DSL.
- **Audit trail captures rule + application** — six months later, "why was this actor named this way?" reconstructs from the conventions.md state at the time of mint + the audit event.

#### Where conventions live (which file)

Option-by-option:

| Convention type | Lives in | Example |
|---|---|---|
| Office-wide (applies across all departments) | `office-config.md` body OR `extensions/office/conventions.md` | actor ID convention, file-naming for shared resources |
| Department-specific | `extensions/department/<dept>/department.md` body | doctype naming, project archival policy for that department |
| Process-specific | `extensions/department/<dept>/processes/<process>.md` body | within-process step naming |

Bundle A (department.md design) and #15 (office entities) together provide the homes; this decision says **what kind of content lives where**.

#### Generalizes broadly

The pattern applies to many surfaces beyond actor IDs:

- Doctype filename conventions (`B-Plan Begründung.tex` vs `<project-id>-begruendung.tex`)
- Archive policies (when to snapshot, where, retention rules)
- Notification preferences (which events surface to whom, in what mode)
- Cross-department coordination triggers ("when planning sends to UNB, notify invoicing")
- Default values for recurring fields (default Bundesland, default Verfahren type)

Anywhere there's a "rule that depends on context" — fits this pattern. The structured layer carries the contracts (Pydantic schemas, machine interfaces); the prose layer carries the conventions; AI fuses them at use-time.

### 5. Same registration shape, office-level and department-level

Bundle A consistency insight: managed entities at office level (Actor, Client) and department level (Project, Doctype, Reference) follow the **same registration shape** — declared in their respective `<scope>.md` registration file with the same frontmatter contract.

```yaml
# extensions/department/planning/department.md frontmatter
managed_entities:
  project:
    pydantic_class: extensions.department.planning.entities.project.ProjectEntity
    path_pattern: "<project-root>/state.md"
    instance_axis: project

# extensions/office/office.md frontmatter (or equivalent registration)
managed_entities:
  actor:
    pydantic_class: extensions.office.entities.actor.ActorEntity
    path_pattern: "extensions/office/actors/{id}.md"
    instance_axis: office
    mode: adapter        # adapter or native, per #15
    adapter_protocol: actor-system   # required when mode=adapter
  client:
    pydantic_class: extensions.office.entities.client.ClientEntity
    path_pattern: "extensions/office/clients/{id}.md"
    instance_axis: office
    mode: native
```

**Architectural consequence**: Bundle A's `department.md` design is the same shape as office-level entity registration. The gate's discovery mechanism reads BOTH (department.md files for department entities + office-level registration for office entities) at startup, builds a unified `type:` dispatch table.

This is why the **Bundle A test list expands** to include Actor-via-adapter consistency check alongside cross-industry domain tests:

- Cross-industry test: does the proposed shape work for legal-practice / research-lab / brand-voice?
- Office-level test: does the same shape accommodate Actor-via-adapter (Personio integration) and Client-as-native?
- Prose-rules-fit test: does the shape leave room for office conventions in body (per decision 4)?

If proposed shape fails any of these, redesign before locking.

## Operational concerns — proactive defaults + detection + how-to-fix

Three operational concerns surfaced during session-11 application
of the AI-as-runtime conformance check (smoke + deep test) to the
prose-rules pattern. None are blockers — design honors the
principle — but each has practical handling spread across three
modes:

- **Proactive defaults** (ship-time): start with best-assumption
  defaults derived from the pioneer instance, not from empty.
  Bureaus see well-shaped examples to adapt rather than facing a
  blank canvas.
- **Detection** (runtime): violations still surface despite
  defaults; audit + design-review + Pydantic catch them.
- **How-to-fix** (when flagged): guidance for resolving violations
  when they appear.

The pattern: **defaults reduce the violation rate; detection
catches what slips through; how-to-fix guides resolution.** All
three modes work together. Empty-start + violation-only-detection
is the failure mode this section guards against.

### Concern 1: LLM interpretability — vague conventions produce inconsistent applications

**Problem**: a vague convention rule produces inconsistent
applications across invocations. AI may interpret "use sensible
names" differently each time; same input → different output.
Drift is silent until inconsistency surfaces.

**Proactive default** (ship with): `extensions/office/conventions/`
ships pre-populated with **template convention files** drawn from
the PBS pioneer instance — well-shaped, imperative, with examples
and edge cases. Bureaus adopting PBS see what good conventions
look like and adapt; they don't start from empty. Templates cover
common surfaces: actor-id minting, archive policy, file naming,
notification triggers, audit-record conventions. Empty conventions
file is NOT the default; well-shaped example IS.

**Detection** (LLM audit territory — judgment-shaped check):
audit slice 21 (entity-md conformance, post-#9) extends to a
"rule precision" sub-check — LLM evaluates whether convention
prose is imperative + has examples + has edge-case handling.
Pure pattern judgment; LLM is the right tool. Telemetry first;
auto-enforcement later if the pattern proves valuable.

**How-to-fix when flagged — write conventions as imperative rules
with concrete examples**:

| Vague (avoid) | Precise (preferred) |
|---|---|
| "Use sensible IDs" | "Actor IDs follow `<firstname>-<lastname>` from email prefix; on collision, append middle initial: `alice-m-mueller`. Example: `alice.mueller@schulz-planung.de` → `alice-mueller`." |
| "Archive old projects appropriately" | "Projects move to `archived/` after 18 months of inactivity; subfolder named `<closure-year>-<original-id>`. Example: `2024-friedrichshof-pv-3/`." |
| "Name doctype files clearly" | "Doctype filenames: `<doctype-id>.md` for spec; per-project instances at `<project-root>/<doctype-id>/<filename>.tex`." |

The discipline: imperative + concrete examples + edge-case handling.
NOT principles or guidelines — those leave too much interpretive
space for the LLM.

### Concern 2: Body-size budget — convention bodies grow unbounded

**Problem**: conventions accumulate over time. A bureau with 50
conventions × 200 tokens each = 10K tokens of body in
`office-config.md`. Hits entity-md-spec §16 thresholds (≤1500
token bodies, ≤500 token sections). Loading the whole body becomes
expensive; AI may struggle to keep all conventions in mind.

**Proactive default** (ship with): the file structure is
**already split by topic from day one** — `extensions/office/
conventions/{actor,archive,naming,notification,audit}-conventions.md`.
Bureaus inherit the split structure; they don't migrate from a
single mega-file later. Avoids the "everything in office-config.md"
anti-pattern entirely by structuring the canvas correctly upfront.

**Detection** (deterministic-primary, LLM for clustering judgment):
- **Threshold check** (deterministic, cheap): token-count entity
  bodies, flag those exceeding §16 thresholds. Pure mechanical
  check; runs in audit slice 21's body-size telemetry sub-check.
- **Split judgment** (LLM): when a body is over budget, *should*
  it be split into separate files? That's a clustering question —
  do conventions group naturally by topic? LLM judges based on
  reading the content. Reserved for files actually flagged.

**How-to-fix when flagged — split convention files by topic**:

```
extensions/office/
├── office-config.md                  # core deployment config
└── conventions/
    ├── actor-conventions.md          # identifier rules, role mapping
    ├── archive-conventions.md        # retention, closure rules
    ├── naming-conventions.md         # file/folder naming
    ├── notification-conventions.md   # who-gets-pinged-when
    └── audit-conventions.md          # what-gets-recorded-where
```

Each file stays within §16 thresholds. AI loads only relevant files
per workflow (audit-conventions.md when audit retrofits run;
actor-conventions.md when minting actors).

**Pruning norm also applies** (per entity-md-spec §16.3): drop
superseded conventions from the body during edits. Don't
accumulate dead rules. Brief commit message captures what was
removed and why. Convention md files are NOT append-only.

### Concern 3: Audit trail of rule application

**Problem**: when AI applies a convention to mint an entity, the
audit event must record both the rule reference + the produced
result. Without this, "why was alice-mueller minted that way?"
reconstructs from *current* convention state — but the convention
might have changed since then. Reconstruction unreliable.

**Proactive default** (ship with): the `convention_applied` field
is **in #6's first schema version** — Pydantic enforces it from
day one of audit-trail v2 retrofit. NOT added retroactively after
violations surface. Bureaus get the field for free; AI fills it
when minting; auditability is structural, not optional.

**Detection** (deterministic-primary, LLM for accuracy spot-check):
- **Field-presence check** (deterministic, Pydantic): entity-mint
  AuditEvents must have `convention_applied` field set when AI
  applied a convention rule. Pydantic validates at write-time;
  fail-loud if missing. Pure schema enforcement.
- **Reference accuracy check** (LLM): does the cited convention
  section actually contain a rule that would have produced this
  result? Sample-based audit; LLM judgment. Reserved for
  spot-checks, not every event.

**How-to-fix when flagged — entity-mint AuditEvents include `convention_applied` field**:

```yaml
event_kind: entity_minted
actor: alice         # who triggered the mint
actor_kind: skill
details:
  entity_type: actor
  entity_id: alice-mueller
  convention_applied:
    file: extensions/office/conventions/actor-conventions.md
    section: "Actor identifier convention"
    git_sha: <commit-sha-at-mint-time>
  input: alice.mueller@schulz-planung.de
```

The `git_sha` ties the audit event to the convention state at mint
time — even if conventions evolve later, the historical
reconstruction is exact.

**Home**: schema addition lands in **#6 audit-trail v2 retrofit**
as part of the existing `details:` payload extension. Not a
separate event kind; just a structured field added to entity-mint
events. Pydantic validates required-when-applicable. Constraint
passed to #6 (added to constraints section below).

### Summary across all three modes

| Concern | Proactive default (ship-time) | Detection (runtime) | How-to-fix when flagged |
|---|---|---|---|
| #1 Vague conventions | Convention templates pre-populated from PBS pioneer instance | LLM (audit slice 21 sub-check on prose precision) | Rewrite as imperative + examples + edge cases |
| #2 Body-size budget | File structure pre-split by topic (`actor-conventions.md`, `archive-conventions.md`, etc.) | Deterministic token threshold + LLM clustering judgment | Split file; prune stale conventions |
| #3 Audit field | Pydantic-required from #6 v1; AI fills automatically | Schema validation (deterministic) + LLM reference-accuracy spot-check | Backfill missing field if surfaced (rare with default) |

**Pattern**:

1. **Proactive defaults** reduce the violation rate at ship time —
   bureaus inherit good shapes, not empty canvases.
2. **Detection** is defense-in-depth — deterministic where cheap
   and reliable, LLM where judgment is genuinely required. Same
   logic as governance enforcement (decision 1: gate enforces
   roles, not LLM).
3. **How-to-fix** is documented guidance for when violations
   surface despite defaults.

The three modes work together. Empty-start with violation-only
detection is the failure mode this section guards against —
bureaus shouldn't have to discover good convention shape through
trial-and-error when the pioneer instance has already done that
work.

## Connection to existing architectural disciplines

| Discipline | Connection |
|---|---|
| **AI-as-runtime hybrid-shape (#16)** | Office conventions live in prose, AI applies at runtime — the strongest application of the principle surfaced so far. Conventions are the natural prose-layer content for deployment-instance rules. |
| **Glue-not-replacement** | Identity adapters compose with existing HR/IDP infrastructure; PBS doesn't reinvent identity. Same pattern as Lexware-for-invoicing, Harvest-for-time-tracking — extends to Personio/BambooHR-for-actors. |
| **Pattern-vs-instance** | Conventions are deployment-instance data, NOT pattern-universal. Belong in markdown alongside data, never in shared Pydantic schemas. |
| **Strict-validation (meta-rule 4 corollary)** | Layer 1 + Layer 2 frontmatter still strictly validated at gate; conventions apply at MINT TIME (creating new entities), not at every read. Validation discipline preserved. |
| **Entity-elevation 3-test (#12)** | Conventions are NOT entities — they're prose that AI reads. Don't elevate. They live in body of the office-config or department.md or conventions.md. |
| **Office-vs-department (#12)** | Department.md and office-level registration share the same frontmatter shape (decision 5). 4-axis scope orthogonality preserved. |

## Connection to VISION

Application of axis 1 (intertwining-AI-workflow): conventions written by domain experts in prose, applied by AI in the production of work output, with audit trail capturing both rule and application. AI is genuinely a co-worker — it doesn't follow hardcoded rules, it READS the rules the bureau writes for itself.

Application of axis 3 (authorship preservation): rule application is auditable. Six months later, "why was this actor minted with this ID, what convention was in force at the time?" reconstructs from the convention state + audit event. User remains the explicit author of conventions; AI executes them; defensibility infrastructure intact.

## Pattern-vs-instance check

The decisions generalize cleanly:

| Domain | Identifier convention example | Governance scaling | Adapter integration |
|---|---|---|---|
| **Legal practice** | matter-id from court filing number | partners gate matter-creation; juniors do filings | adapters to Clio / Casemine / Westlaw |
| **Research lab** | manuscript-id from arXiv pattern | PI gates submissions; postdocs do drafts | adapters to ORCID / institutional auth |
| **Healthcare clinic** | patient-id from MRN system | senior clinicians gate plan-of-care changes; junior staff do intake | adapters to Epic / Cerner |
| **Boutique consulting** | engagement-id from Salesforce opportunity | partners gate proposals; associates do drafts | adapters to Salesforce / Hubspot / etc. |

Same architectural mechanism (adapter pattern + gate enforcement + prose conventions + git foundation), different domain prose. Pattern-level. ✓

## Defers (per defer-instinct discipline)

| Defer | Home | Specific cost being avoided |
|---|---|---|
| **D1**: Concrete approval event flow specification for governance changes (which event kinds, which fields, which UI surface) | #6 (audit-trail v2 retrofit) — already adds approval event kinds | Pre-empting #6's design without concrete consumer pressure; #6 has the right scope to do this when it fires |
| **D2**: Concrete Actor adapter Pydantic Protocol shape | #15 (Client + Actor) — Actor adapter mode is in scope | #15's adapter Protocol design lives there; this decision documents the principle, not the specific Pydantic interface |
| **D3**: Tier 2 multi-user enforcement implementation (auth-token validation, cached ActorEntity, role-check middleware) | #13 (deployment flexibility + Coolify reference) — already in scope | Implementation cost lives where #13's multi-user readiness lives; this decision documents the architectural shape, not the code |
| **D4**: Office-conventions.md authoring conventions and the gate-side mechanism for AI to fetch convention rules at use-time | Bundle A and bundle implementation (where conventions location is decided) | Bundle A is currently designing department.md shape; conventions location decision composes naturally there |
| **D5**: Audit slice / design-review check that scans for conventions used inconsistently (e.g., some actors created with one ID convention, others with a different one — drift) | Future audit work; bundled with audit slice 21 (entity-md conformance) | Telemetry sub-check; needs entity gate to exist (post-#9 implementation) |

Each defer names a specific home + a specific cost being avoided. Per `feedback_defer_instinct`: not generic YAGNI; honest defers.

## Constraints for downstream commitments

### → #9 Bundle A (department module + location/registration)

- Bundle A's `department.md` shape MUST accommodate the same registration pattern as office-level entity registration (decision 5).
- Bundle A's body conventions discussion MUST consider where office-conventions prose lives (`office-config.md` body vs separate `extensions/office/conventions.md` vs department-scoped `department.md` body).
- Bundle A test list now includes:
  - Cross-industry stress-test (legal, research, brand-voice)
  - Office-level entity consistency (Actor-via-adapter)
  - Prose-rules-fit (does proposed shape leave room for conventions in body?)

### → #15 (Client + Actor as office-level managed entities)

- Actor adapter Pydantic Protocol design lands here (D2).
- Actor entity supports `mode: native | adapter` per the office-vs-department decision record's "Department-managed entities + delivery modes" subsection (extended to office-level entities).
- Actor.roles list[str] field is the role primitive for governance enforcement (per decision 1).
- Identifier uniqueness convention (decision 3) applies; deployment chooses + documents.

### → #13 (deployment flexibility + Coolify reference)

- Tier-conditional gate enforcement is in #13's pre-RAG scope (decision 1, "Tier-conditional enforcement").
- Auth provider integration (Google Workspace SSO, Coolify SSO, OAuth) lands as part of #13's auth-layer abstraction.
- Two-adapter pattern (auth + actor data) is the canonical shape; #13's auth abstraction must support both.

### → #6 (audit-trail v2 retrofit)

- Approval events extend to governance-change approvals (D1).
- AuditEvent.actor references Actor.id (already in #6's scope per #15 constraint).
- Audit slice or design-review check for convention drift (D5) bundled with audit slice 21.
- **`convention_applied` field on entity-mint events** (per
  operational concern 3): when AI applies a convention rule to
  mint a new entity, AuditEvent's `details:` payload includes
  `convention_applied: {file, section, git_sha}`. Pydantic
  validates required-when-applicable (entity-mint events MUST
  include it; other events don't need it). Required for
  defensible historical reconstruction six months later. NOT a
  new event kind — just a structured field on existing
  entity-mint events.

### → #11 (Cowork integration)

- Skill bodies include the user-facing UX of the approval workflow (decision 1, layered enforcement).
- Skill frontmatter sweep should NOT add `requires_role:` field — enforcement is at the gate, not in the skill (defense-in-depth principle).

## Convention evolution + conflict resolution (session-11 per-DR gap detection)

Per-DR gap detection surfaced two decisions within scope that
weren't surfaced originally:

### Convention versioning

**Decision**: conventions evolve via in-place edit + git history.
No formal version-number convention on convention md files.

**Why**: conventions are prose; AI applies them at runtime + audit
records `convention_applied: {file, section, git_sha}` per decision
4 above. The `git_sha` IS the version anchor — six months later,
"why was this entity minted this way?" reconstructs exactly via
the git_sha-pinned convention text.

**Implementation**:
- Existing entities minted under prior convention versions stay
  as-minted (their `convention_applied.git_sha` points to the
  prior text). No retroactive remint required.
- New entities minted after a convention edit use the new text
  (their `convention_applied.git_sha` points to the new commit).
- Audit slice 21 / target 12 verify the audit trail's convention
  references resolve at their pinned shas.

When a convention CHANGE produces NEW behavior (e.g., switch from
`firstname-lastname` to `email-prefix-derived` actor IDs), there
are two valid responses:
- **Forward-only** (default): new entities use new convention; old
  entities keep their old IDs. No mass-rename.
- **Mass-rename** (rare; explicit operation): a separate skill
  invocation walks all existing entities under the old convention
  + renames per the new. Emits AuditEvent
  `entity_renamed_per_convention_change` per entity. Rare; opt-in.

### Convention conflict resolution

**Decision**: when conventions in different files apply to the
same concern, the more-specific scope wins. Priority order
(most-specific to least-specific):

1. **Department-specific** (`extensions/department/<dept>/conventions/<topic>.md`)
2. **Office-wide** (`extensions/office/conventions/<topic>.md`)
3. **Universal / framework default** (e.g., entity-md-spec §3.1)

If two conventions at the SAME priority level conflict (e.g.,
two department-specific conventions for the same concern in the
same department), it's a **convention bug** — flag via audit slice
21 + design-review target 12 (rule precision check). The bureau
must reconcile; AI raises the conflict for explicit resolution
rather than picking arbitrarily.

**Implementation**: when AI applies a convention at mint-time, it
walks priority order from most-specific. First applicable
convention wins. AuditEvent's `convention_applied.file` records
which file's convention fired (so resolution is reconstructible).

**Cross-department coordination**: if a cross-department workflow
needs a convention applied that differs per department, route the
mint to the department-of-record (the department owning the
entity being minted) and use ITS convention. Cross-department
events relay results, not invocation.

---

## Revisit triggers

Re-open this decision record if:

- A real second deployment surfaces governance needs that don't compose with the existing primitives (signal that the "primitives compose" claim is wrong).
- A specific deployment hits scale where the gate-level enforcement code becomes a bottleneck (signal that the architecture doesn't scale to its claimed range without optimization).
- A regulated domain (healthcare HIPAA, financial SOX) requires governance audit trails beyond what AuditEvent + decisions.md provide (signal that we need to extend audit infrastructure for regulated cases).
- The prose-conventions pattern (decision 4) proves brittle — AI consistently misapplies a convention or hallucinates conventions that aren't there (signal that some conventions need to be encoded structurally after all).
- An office at scale (>100 people) demands federated governance shapes that don't fit the architecture's department-isolation model (signal that Tier 3 / Gemini Enterprise migration path becomes more urgent for that deployment).

None expected pre-RAG.

## Files touched by this commitment

- `docs/decisions/governance-and-identity-sourcing.md` — this file
- `ROADMAP.md` — note added under #13 referencing this record
- `docs/conventions/entity-md-spec.md` — identifier uniqueness conventions added
- `HANDOFF.md` — Bundle A test list expanded; session-11 thread captured

No code changes this commitment. Implementation lands progressively across #9, #15, #6, #13.
