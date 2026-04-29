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

Status: **v0.8 (post-session-7 + pattern-vs-instance discipline)**.

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
- **v0.6 → v0.7**: meta-rule 4 fail-closed corollary. The rule
  symmetrizes for reads: when MCP is unreachable, contract-bearing
  reads MUST surface and stop, never bypass via direct filesystem
  `Read`. The strict-validation principle (no bad defaults / fail
  loud) extends to availability: a contract that is enforced on
  successful read but bypassed when MCP is down is not a contract.
  See `docs/decisions/mcp-fallback-policy.md`. Audit slice 14 brief
  extended to scan `fallback_when_mcp_absent` strings for declared
  future violations.
- **v0.7 → v0.8**: **Pattern-vs-instance discipline** added as
  meta-discipline before the meta-rules. Every architectural
  commitment must work at pattern level (the test: would this work
  for a hypothetical legal-practice / research-paper-review /
  engineering-doc office?), not just for PBS. PBS is the pioneer
  instance per VISION.md; the architecture is the pattern. Long-arc
  end-state is the AI-office builder (ROADMAP v2). Connects the
  Skill Bundle convention, meta-rules 1-4, fail-closed corollary,
  target 9 subsumption check — all pattern-level by construction —
  into a coherent discipline that constrains future commitments.

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

## Pattern-vs-instance discipline

Every architectural commitment in this repo must work at the
**pattern level**, not just for PBS. PBS is the pioneer instance
(per VISION.md "PBS as pioneer instance"); the architecture is
the pattern. The long-arc end-state is an AI-office builder that
scaffolds new domain offices from a domain spec + the
accumulated patterns (see ROADMAP v2 "AI-office builder"). Every
commitment that doesn't generalize is a future migration cost
the builder will pay; every commitment that does generalize
*is* the builder's foundation.

**The test** when proposing any new meta-rule, entity type,
persistence structure, MCP tool, or decision-record-grade
commitment:

- Would this work for a hypothetical **legal-practice office**
  (intake / discovery / filing / argument phases; courts /
  opposing-counsel / regulators as authorities; precedents +
  citations + templates as memory taxonomy)?
- Would this work for a hypothetical **research-paper-review
  office** (manuscript / review / revision / publication phases;
  journals / co-authors / reviewers as authorities; citations +
  prior-work + templates as memory taxonomy)?
- Would this work for a hypothetical **engineering-doc office**,
  **medical-records-workflow office**, **regulatory-filing
  office**?

If yes for at least 2 of these 3-5 hypothetical domains: the
commitment is pattern-level. Lock it in.

If no for most: the commitment is too PBS-coupled. Push it to
the **instance layer** — skill bodies (drafting drafts plug in
domain-specific doctype templates), manifests (domain-specific
references + actors), office-config (domain-specific scope
fields), korrektur-rules and similar prose memory.

**Where the line typically falls:**

| Layer | Pattern (stays in architecture) | Instance (lives in PBS or its successors) |
|---|---|---|
| Meta-rules 1-4 | All four | (none — they're patterns by construction) |
| Entity types (Skill / Memory / Configuration / etc.) | The taxonomy itself | What entities exist (which skills, which memory records) |
| MCP tool *patterns* | strict-validation discipline; fail-closed corollary; CRUD-style memory tools | Tool *names + bodies* (which gates exist; what they do) |
| office-config *schema shape* | layered manifests, scope.domains, paths.* discipline | Specific fields (verfahren_type values, doctype list, korrektur-rules path) |
| VISION axes | Three-axis framing (intertwining / sparring / authorship preservation) | Per-axis *content* — what counts as authorship in the domain |
| Decision-record format | The structure itself (Context / Decision / Why / Alternatives / Revisit) | Specific decisions — which mechanisms are committed |

**Anti-patterns the discipline catches:**

- ❌ A meta-rule that names "B-Plan" / "Begründung" /
  "Festsetzungen" in its body. Those are PBS instance content;
  the rule should describe the *shape* (e.g., "doctypes have
  required + optional sections per their manifest entry") and
  let PBS provide instance content for that shape.
- ❌ A persistence structure assuming German legal taxonomy
  (gesetze / urteile / leitfäden) at architectural layer.
  Pattern is "layered references manifest with invalidation
  contract"; instance is the German-law taxonomy.
- ❌ An MCP tool whose *interface* embeds domain knowledge
  (e.g., `validate_b_plan_begruendung` as a tool name). Pattern
  is `validate_doctype(doctype: <slug>)`; instance is what
  doctypes exist.
- ❌ A skill body that hardcodes domain-specific values rather
  than reading from office-config or manifests. Already covered
  by plugin-conventions §13 anti-pattern; now also a
  pattern-vs-instance violation.

**Coupling exceptions** (where domain-coupling at architecture
level is allowed):

- The *vocabulary* used in examples (decision records, ARCH
  body) can use PBS terminology for legibility, as long as the
  underlying rule generalizes. "PBS bausteine" in an example is
  fine; a rule that *only* makes sense for PBS bausteine is not.
- The instance directory itself (`extensions/`, `memory/`,
  `office-config.yaml` populated values) is unconditionally
  PBS-instance. The pattern is the *schema*; PBS is the
  *content*.

**Discipline check at audit/design-review time:**

- Audit slice 14 (boundary adherence) extends naturally to this:
  "is this commitment pattern-level or instance-level?" applies
  to placement of decisions across the architecture/instance
  boundary, same way it applies across the LLM/Python boundary.
- Design-review target 9 (Subsumption check) implicitly tests
  this: a new mechanism that subsumes a PBS-specific legacy
  mechanism *and* generalizes is correct; one that subsumes
  PBS-specific in a PBS-specific way perpetuates the coupling.

**Connection to current work**: every session-7 commitment
(meta-rule 4 fail-closed corollary, target 9 subsumption check,
audit slice 18 legacy retirement scan, framing skill, audit-trail
v2 single-write architecture, Skill Bundle frontmatter
convention) is pattern-level by construction. The discipline
makes that property explicit and load-bearing for future work.

### Validation under the single-domain-pioneer constraint

PBS is operated by a single planning-domain expert. Realistically
**we will not implement second-domain instances ourselves** —
legal practice, research, engineering, etc. are domains the user
doesn't work in. Hand-building a "second instance" in a domain
the user doesn't actually practice would produce evidence of
*the user's idea of that domain*, not of the actual domain —
worse than no evidence, because misleading.

This constraint shapes the validation strategy: we **cannot** use
"build 2-3 hand-instances and measure overlap" as the validation
path. Waiting for empirical evidence from a real second-domain
deployment that may never come (consulting engagement; second
office adoption) becomes manufactured restraint disguised as
rigor — a way to defer architectural decisions indefinitely.

**Working method instead — best-effort split + immediate PBS
validation:**

The split is implemented now (pre-RAG), against PBS, with two
distinct validation signals:

| Signal | What it tells us | Source |
|---|---|---|
| **#1 — split doesn't break PBS** | The proposed split is implementable; refactor is executable; tests pass; skills route correctly; project state round-trips. Catches mechanics-level issues that pure reasoning misses. | Implementing the split now against PBS — **immediate** feedback. |
| **#2 — split chose the *right* boundary** | The pattern/instance line generalizes to other domains. Catches the split being too PBS-shaped (overfit). | Only known when a real second-domain implementation lands — **deferred, possibly indefinite**. |

Signal #1 is necessary-but-not-sufficient: confirms no regression
but can't confirm correct boundary. Signal #2 confirms boundary
but requires implementation that may never happen here. **Doing
the split now is the maximum validation we can extract before
signal #2 arrives — and crucially, doing it later is more
painful** (post-data-accumulation refactor + skill retrofits +
migration scripts vs. clean refactor today). The 3-5 hypothetical-
domain thought experiment (legal-practice, research-paper,
engineering-doc, medical-records, regulatory-filing) is the
*reasoning input* to the split; signal #1 is the *immediate
empirical check*; signal #2 waits for real second-domain.

**The thought experiment as legitimate epistemic basis**: it
doesn't require working in those domains, just thinking carefully
about them as architectural-imagination targets. Signal #1
catches what the thought experiment missed at implementation
level; signal #2 (when/if it arrives) catches what both missed
at boundary level.

This explicitly is a **best-effort** discipline, not a proven
one. The split *will* be wrong somewhere; the question is
whether it's *less wrong than no split* and *less expensive to
correct than no-split-then-painful-migration*. Pre-RAG is the
unique window where the cost answer is "yes."

Pre-RAG commitment #9 (`ROADMAP.md`) is the concrete realization:
the reasoning pass + best-effort split implementation + PBS
regression validation are bundled as one work stream, scheduled
before Phase 1 corpus download.

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
| Memory (audit-log) | Append-only `<project>/_ai/audit-trail.jsonl` per docs/decisions/audit-trail-v1.md. Each `AuditEvent` carries `id`, `timestamp`, `kind`, `sources[]`. Events never invalidate (immutable history); `causes[]` chain captures supersession. `query_audit_trail` MCP tool is the canonical query layer; existing prose sources (decisions.md, snapshots/, etc.) remain authoritative for human-readable context. Dual-write discipline: every event-producing skill calls `record_audit_event`. |
| Backend | Python imports + Pydantic schemas; restart MCP server after changes. No declarative invalidation hook. |
| Configuration | `schema_version` + migration framework. Manifests carry `last_updated` + per-entry `last_fetched` + `checksum_sha256`; `research-references` re-fetches on schema/source change. |
| External data | Per-project `_ai/state.md.lifecycle` declares phase + status; `roots.references_root` corpus carries `changelog.md`. |

**Cross-cutting concern handler.** Contract reading is layered
across two skills:

- `research-references` is the *trigger*: after fetching an
  updated reference, it scans both bausteine (`references[]`) and
  memory docs (`references_used[]`) for matches. Bausteine
  matching → flagged. Memory docs matching → logged to
  `memory/product-backlog.md` with affected paths.
- `validate-bausteine` is the *comparator*: it reads the
  `references[].verified_against_version` field on flagged
  bausteine and compares it against the current
  `current_amendment_form` from the manifest, surfacing drift
  for the user.

The split is intentional — research-references detects *which*
entities cite updated laws; validate-bausteine determines
*whether each entity's cited form is still current*. Both flows
are required to close the invalidation loop; neither alone
suffices.

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

**Strict-validation discipline.** Every MCP gate that owns a
typed contract validates via Pydantic. Required fields are
strictly required (no `Optional` for required, no silent default
to `None`). On contract violation, raise loud with descriptive
errors naming the offending field; never return partial data,
never coerce a missing required field to a placeholder. Defaults
are reserved for fields where missing semantically means
"not-yet-known" (`None`) — not for required fields where missing
would mean "broken data."

This discipline is what makes the gate a gate. A Pydantic model
that liberally uses `Optional` to "be flexible" silently accepts
malformed data and breaks the contract-enforcement guarantee.

Audit slice 16 (validation-gate coverage) checks adherence: it
walks every MCP tool's input/output models + every entity
Pydantic model and flags `Optional` on fields the rule says are
required, silent defaults that mask missing data, and exception
swallowing that converts contract violations to soft failures.

**Fail-closed for contract-bearing reads.** When MCP is
unreachable, skills MUST surface to the user and stop, never
bypass the contract via direct filesystem `Read`. The gate is the
only correctness path; bypass produces silent invalid output that
violates the strict-validation principle just established.

The rule applies symmetrically to writes (already covered by
"persistence-layer boundary" above) and reads. A skill that
"falls back to direct Read of state.md when MCP is down" gets:

- pre-migration frontmatter the loader would have updated
- partial-invalid state the Pydantic model would have rejected
- cross-reference-broken state (lifecycle ↔ phase mismatch) the
  invariant check would have caught

The right MCP-unreachable behavior for a contract-bearing read is
a clean failure surfacing: "MCP unreachable; cannot operate on
\<X\>. Restart backend." Contract-free prose (HANDOFF.md, prose
memory, decisions.md, file-map.md, READMEs, top-level docs)
remains skill-direct — no contract exists to bypass.

The test for "contract-bearing": Pydantic model owns its shape, OR
`schema_version` with migrations applied on read, OR cross-
reference invariants, OR a loader function in `pbs_mcp/`
constructs a typed object, OR `last_updated` / `last_fetched` /
`checksum_sha256` declares an invalidation contract. If any
yes → fail closed. Otherwise → direct Read fine.

Per-skill: `fallback_when_mcp_absent` strings declare what is
still possible; for contract-bearing dependencies the answer is
"nothing — surface and stop." Audit slice 14 scans these strings
and flags any "fall back to filesystem Read of \<contract-bearing
file\>" pattern as a declared future violation.

See `docs/decisions/mcp-fallback-policy.md` for the full
rationale and rollout.

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
