# Drift surfaces + slice library

## The 11 drift-surface categories

Every finding falls into one of these. Slices target one or more
categories; rounds combine slices to cover the surface space.

The first 6 are *correctness* drift (claims vs. reality, schemas
vs. usage, etc.). 7-9 are *implementation quality* drift (test
coverage, security, performance) — added in v0.2 of the audit
skill per design-review session-5 follow-up. **10 is *placement*
drift** — operations on the wrong side of the LLM/Python boundary,
added in v0.4 alongside meta-rule 4's session-6 sharpening.
**11 is *invalidation-contract* drift** — entities that don't
declare (or don't honor) their staleness contract per meta-rule 3,
added in v0.5 alongside design-review target 8's coupling review.

Audit's scope is broader than just structural-correctness;
implementation rigor, architectural placement, and contract-
enforcement are all part of compliance with the system's own
claims.

### 1. Documentation drift

Cross-doc consistency, stale claims, broken cross-references,
numerical claims that don't match reality.

**Examples**: HANDOFF says "16 skills" but the directory has 17;
ARCHITECTURE.md says "5 meta-rules" but the section count is 4;
README cross-refs to a doc that's been moved.

**Why dangerous**: stale doc claims compound — readers (including
future Claude sessions) trust the doc and propagate the wrong fact.

### 2. Schema drift

Type definitions vs. actual usage. Frontmatter declarations vs.
body usage. YAML schema vs. populated content.

**Examples**: skill declares `mcp_tools_required: [foo]` but the
body never calls `foo`; baustein README documents
`scope: { layer, key }` but canonical schema is flat
`scope: domain` + `scope_key: Naturschutz`.

**Why dangerous**: tools that read the schema (orchestrator's
planner, list_skills) make decisions based on the declaration.
Mismatch between declaration and usage = silent wrong behavior.

### 3. Code drift

Legacy patterns, dead code, half-migrated paths in live code.

**Examples**: a function returns `"global"` for legacy paths that
no longer exist; an unused regex constant has a buggy alternative
branch; commented-out code from a prior refactor.

**Why dangerous**: live code drift causes bad data on first run.
Session-5 round-4 caught `tools/ingest.py:217` returning
`"global"` for baustein source_subtype — would have written wrong
metadata to LanceDB on first ingest.

### 4. Convention drift

Naming, capitalization, vocabulary inconsistency.

**Examples**: `global | domain | project` survivors after the
orthogonality refactor renamed to
`universal | domain | state | project`; lowercase `naturschutz`
where canonical is `Naturschutz`; `query_skills` where canonical
is `list_skills`.

**Why dangerous**: convention drift is highly contagious — one
stale doc seeds further drift in skills that read it.

### 5. Reference drift

Cross-skill handoffs, tool name references, path references that
point at renamed/removed targets.

**Examples**: skill A says "hands off to skill B" but B has been
renamed; orchestrator routing list mentions a skill that no
longer exists; a path reference to `memory/global/...` that's
been migrated.

**Why dangerous**: silent failures at runtime when the handoff
target is missing.

### 6. Claim drift

"Verified clean" overclaims. Audit artifacts that say "X is fine"
without specifying which scope of X was checked.

**Examples**: session-5 round-1 said "Bausteine path orthogonality
— verified clean across all 16 SKILL.md bodies" but didn't audit
backend docs (which still had the legacy vocab). The claim was
correct for its scope but read as system-wide.

**Why dangerous**: a "verified clean" claim discourages future
auditors from re-checking. Without scope-bounding, the claim
implicitly covers more than it actually verified.

### 7. Test-coverage drift

Code paths without tests. Tests that exist but don't actually
exercise the load-bearing logic. Tests that mock what should be
real.

**Examples**: a chunker module with 200 lines of dispatch logic
and zero tests; a Pydantic schema with no round-trip tests;
integration tests marked but never run; mock-based unit tests
that don't exercise the SQL/embedding path the production code
uses.

**Why dangerous**: untested paths fail silently in production.
Pre-launch, this is theoretical; once data lands in LanceDB,
test gaps become invisible bugs.

### 8. Security / data-handling drift

Code paths that touch sensitive data without appropriate care.
Inputs not validated. Outputs that leak. Auth/permission
inconsistencies.

**Examples**: SQL string interpolation without escape (caught
session-5: `db.delete_by_path` was unescaped); user input flowing
unsanitized to filesystem operations; office-config secrets
logged at INFO; MCP tool inputs not validated against malicious
shapes; path traversal in file operations.

**Why dangerous**: pre-launch, attack surface is small (single
user). Post-launch / multi-deployment, security drift is the
high-impact risk.

### 9. Performance / efficiency drift

Hot paths with non-obvious complexity. Repeated work that
should be cached. Algorithms that scale badly with corpus
growth. Memory leaks or unbounded growth.

**Examples**: a chunker that re-loads the embedder per chunk;
filesystem walks that re-stat the same files; LanceDB queries
without indexes; in-process caches that grow unbounded; LLM
calls in tight loops without batching.

**Why dangerous**: corpus is small now (57 entries). Post-RAG,
hot-path inefficiencies become user-visible latency or cost
spikes.

### 10. Boundary placement drift

Operations on the wrong side of meta-rule 4 (the LLM/Python
boundary). Distinct from code drift: the code itself may be
correct, but it lives in the wrong tier — deterministic logic
re-implemented in skills, or interpretive logic hardcoded in
Python, or schema-bearing state accessed outside MCP, or shared
logic copy-pasted instead of factored to a single home.

**Examples**: skill PROCEDURE contains step-by-step dedup logic
that an MCP `dedupe_*` tool should own; backend code does
`if "collegiate" in text: ...` for what's an interpretive call;
skill writes baustein YAML directly via `Write` instead of through
`save_baustein`; two skills carry identical 30-line procedural
blocks that should live as one Skill Bundle reference.

**Why dangerous**: contract enforcement leaks. Skill-side
re-implementation of MCP logic drifts from the canonical version
(now two implementations to keep in sync). Python-side
hardcoded interpretation locks out future refinement. Both
accumulate silently — nothing fails until a real consumer hits
the gap. Pre-launch is the unique window to fix placement; post-
launch, every callsite is a migration cost.

**The contract-enforcement test**: a file is in scope of MCP if a
Pydantic model + loader owns its shape. Loose markdown (HANDOFF,
prose memory, READMEs) is skill-direct. See ARCHITECTURE.md
meta-rule 4 for the full rule including reuse direction.

### 11. Invalidation-contract drift

Entities that don't declare their staleness contract per
meta-rule 3 ("every entity declares its invalidation contract"),
declare it incorrectly, or whose declaration isn't actually read
by the cross-cutting refresh handler (`research-references`).

Distinct from schema drift: schema drift is "the type definition
disagrees with usage." Invalidation-contract drift is "the rule
says this entity must declare *when it goes stale*, and either
it doesn't, or nothing reads it when refresh fires."

**Examples**: a memory-prose `.md` file that cites BauGB §35 in
the body but has no `references_used:` frontmatter (so
`research-references` won't flag it when BauGB updates); a
manifest entry without `checksum_sha256` (so the loader can't
detect remote-content drift); a baustein with `status: active`
and `references[]` but no `verified_against_version` on the
entries (so it never gets re-validated when the cited law moves);
a Pydantic schema that allows the contract field as `Optional`
when the rule says it's required.

**Why dangerous**: invalidation contracts are the system's
defense against silent staleness. Without them, citations rot,
bausteine become orphaned from updated laws, manifests claim
fresh data they don't have. The defensibility test in VISION
("can the user defend this six months later?") fails when
invalidation gaps mean the user *can't know* what's stale.

**The cross-cutting handler test**: not enough that the contract
is declared — `research-references` (or its peer refresh tools)
must actually read the declaration. A declared-but-unread
invalidation hook is worse than none, because it gives false
assurance.

---

## The slice library

Each slice is a reusable subagent brief targeting one or more drift
surfaces. Combine slices to cover the surface space; first round
runs slices 1-3 by default, subsequent rounds add slices based on
where prior rounds found drift.

For each slice: ID, drift surfaces, scope (files), and brief
template (the agent prompt).

---

### Slice 1 — cross-doc consistency

**Drift surfaces**: 1 (documentation), 4 (convention), 6 (claim)

**Scope**:
- Top-level docs: VISION.md, ARCHITECTURE.md, ROADMAP.md,
  HANDOFF.md, README.md
- All `docs/*.md` (rag-pipeline-decisions, conventions, audits)

**Brief template**:

> You are running Slice 1 of an audit pass. Read the top-level
> docs and `docs/*.md`. Look for:
> - Contradictions between docs (claim X in doc A; claim NOT-X in
>   doc B)
> - Numerical claims that may not match reality (counts of skills,
>   tools, manifests, entries — verify against filesystem)
> - Stale cross-references (doc points at a section/file that's
>   been moved or removed)
> - "Verified clean" claims missing scope-bounding (per claim-scope
>   rule)
> - Convention drift (legacy `global | domain | project`,
>   lowercase domain names, deprecated tool names)
>
> Output structured findings. Cap at 1000 words.

---

### Slice 2 — skill-drift

**Drift surfaces**: 2 (schema), 4 (convention), 5 (reference)

**Scope**: `plugin/skills/*/SKILL.md` (all skills)

**Brief template**:

> Audit all `plugin/skills/*/SKILL.md` files. For each skill:
> - Frontmatter contract: name/description/version/license +
>   meta-rule-5 fields (mcp_tools_required, _optional, fallback)
>   present?
> - Frontmatter declarations match body usage (tools listed are
>   called; tools called are listed)?
> - Trigger phrases overlap with another skill's (would confuse
>   routing)?
> - Convention drift: legacy scope vocab, lowercase domains,
>   deprecated tool names?
> - Cross-skill handoffs: does "hands off to X" point at an
>   existing skill?
> - Spec compliance with `docs/plugin-conventions.md`?
>
> Output structured findings. Cap at 1200 words.

---

### Slice 3 — backend-tools

**Drift surfaces**: 2 (schema), 3 (code), 4 (convention)

**Scope**:
- `backend/mcp-server/src/pbs_mcp/server.py` (tool registration)
- `backend/mcp-server/src/pbs_mcp/tools/*.py` (handlers)
- `backend/mcp-server/src/pbs_mcp/schemas.py` (Pydantic models)

**Brief template**:

> Audit MCP tool registration + handlers. Specifically:
> - Tool count matches HANDOFF claim?
> - Pydantic input/output models match the documented signatures?
> - Handler bodies don't import MCP framework types
>   (pbs_core/pbs_mcp discipline per ARCHITECTURE meta-rule 4)?
> - Legacy patterns: `global/domain/project` scope vocab in
>   handlers, dead branches, commented-out code?
> - Tool description strings match the actual signature?
>
> Output structured findings. Cap at 800 words.

---

### Slice 4 — plugin-side-scaffolding

**Drift surfaces**: 1 (documentation), 4 (convention), 5 (reference)

**Scope**:
- `plugin/CLAUDE.md` (auto-loaded plugin preamble)
- `plugin/.claude-plugin/plugin.json`
- `plugin/templates/office-style/*.sty`
- `plugin/agents/*` (if exists)
- `plugin/hooks/*` (if exists)
- `plugin/skills/*/references/*.md` (Skill Bundle reference sample)

**Brief template**:

> Audit plugin scaffolding. Check:
> - plugin/CLAUDE.md reflects current architecture (orthogonality,
>   meta-rule 4, current entity types)?
> - plugin.json description + keywords current?
> - office-style/ overlay set complete (one .sty per canonical
>   domain in scope)?
> - agents/hooks dirs match what plugin/CLAUDE.md claims?
> - References in plugin/skills/*/references/ use current scope
>   vocab + don't reference removed paths?
>
> Output structured findings. Cap at 1000 words.

---

### Slice 5 — memory-and-manifests

**Drift surfaces**: 1 (documentation), 2 (schema), 4 (convention)

**Scope**:
- `memory/universal/**/*.md`
- `extensions/{universal,domain,state}/**/*.yaml`
- `docs/office-config.schema.yaml`

**Brief template**:

> Audit Memory (prose) + Configuration (manifest) entities. Check:
> - Memory-prose frontmatter convention (`references_used: []`) applied?
> - Manifest top-level shape (version, scope, scope_key,
>   last_updated, maintainer) correct?
> - Per-entry shape correct (id, title, source_url, fetch_method,
>   canonical_path)?
> - Numerical claim from HANDOFF (entry counts) verifiable
>   against actual files?
> - office-config schema reflects current orthogonality + scope
>   shape?
>
> Output structured findings. Cap at 1000 words.

---

### Slice 6 — backend-code-deep

**Drift surfaces**: 3 (code), 2 (schema), 4 (convention)

**Scope**:
- `backend/mcp-server/src/pbs_mcp/chunkers/*.py`
- `backend/mcp-server/src/pbs_mcp/db.py`
- `backend/mcp-server/src/pbs_mcp/embedder.py`
- `backend/mcp-server/src/pbs_mcp/office_config.py`
- `backend/mcp-server/src/pbs_mcp/office_config_migrations/*.py`
- `backend/mcp-server/src/pbs_mcp/integrations/__init__.py`
- `backend/mcp-server/src/pbs_mcp/config.py`

**Brief template**:

> Audit backend code beyond what slice 3 covered. Check:
> - Legacy scope vocab (`global | domain | project`) in code or
>   docstrings?
> - Dead code, unused imports, commented-out paths from prior
>   refactors?
> - pbs_core / pbs_mcp discipline (no MCP framework imports in
>   chunkers/db/embedder/office_config)?
> - Migration framework correctness (forward-migrate v1→v2 in
>   memory at load)?
> - Hygiene: SQL escape, regex bugs, dead variables?
>
> Output structured findings. Cap at 1000 words.

---

### Slice 7 — cross-references-and-procedures

**Drift surfaces**: 5 (reference), 1 (documentation)

**Scope**:
- `plugin/skills/*/PROCEDURE.md` (all that exist)
- All cross-skill handoff references in SKILL.md bodies
- Orchestrator routing list

**Brief template**:

> Audit cross-references. Check:
> - PROCEDURE.md drift (checkpoint numbering matches HANDOFF
>   references; no legacy paths)?
> - "Hands off to X" mentions: X exists + X's description matches
>   the handoff context?
> - Orchestrator routing list completeness vs. actual skill set?
> - Trigger-phrase overlap between skills (top-level vs. delegated
>   per plugin-conventions §11)?
>
> Output structured findings. Cap at 1000 words.

---

### Slice 8 — readmes-and-supporting

**Drift surfaces**: 1 (documentation), 4 (convention)

**Scope**:
- `README.md` (top-level)
- `dev-link.sh`
- `extensions/README.md`
- `backend/README.md`
- `backend/mcp-server/README.md`
- `backend/mcp-server/docs/*.md`
- `memory/bausteine/README.md`

**Brief template**:

> Audit README + supporting files for drift. Check:
> - Tool / module / file lists current?
> - Setup instructions current (no broken steps)?
> - Cross-refs to top-level docs current?
> - Convention drift in code samples (scope vocab, etc.)?
> - Backend mcp-server/docs/* — these were a BLOCKER source in
>   session-5 round-3; check carefully for vocab drift.
>
> Output structured findings. Cap at 1000 words.

---

### Slice 9 — self-audit-and-adapters

**Drift surfaces**: 6 (claim), 5 (reference), 2 (schema)

**Scope**:
- New / recently-edited docs in `docs/` (audit each one's
  internal consistency)
- `backend/mcp-server/src/pbs_mcp/integrations/**/*.py`
- Prior audit artifacts in `docs/audits/`

**Brief template**:

> Audit self-consistency of recently-written docs and integration
> adapter scaffolding. Check:
> - Docs that claim things about other parts of the system —
>   are those claims still true?
> - Integration adapters (Backend sub-pattern): protocol.py + adapter
>   implementations consistent?
> - Adapter classes match office_config.Integrations Pydantic
>   model (5 expected: email/calendar/scanner/phone/accounting)?
> - "Verified clean" claims in prior audit artifacts: still
>   true, scope still bounded?
>
> Output structured findings. Cap at 1000 words.

---

### Slice 10 — final-pass-cross-cutting

**Drift surfaces**: all 9, but specifically looking for what
prior slices missed because their scope didn't reach.

**Scope**: any file that's been *referenced* by other slices but
not *audited*. Plus a focused check on dependency / build files
(`pyproject.toml`, `uv.lock`) and MCP wiring (`.mcp.json`,
`marketplace.json`).

**Brief template**:

> Final-pass slice. Walk through what prior slices' verified-clean
> claims actually covered. Check:
> - Five canonical concepts (scope vocab, domain capitalization,
>   doctype manifest path, MCP tool names, version semver
>   discipline) — verify consistency across **all** files audited
>   so far. Any drift not caught by the targeted slices?
> - Dependency files: pyproject.toml + uv.lock for stale pins
>   (heuristic-level — flag dependencies pinned at versions known
>   buggy or 6+ months old).
> - MCP wiring: `.mcp.json` + `plugin.json` mcpServers field —
>   does the user-facing setup work end-to-end?
> - Top-level claim audit: is HANDOFF's headline claim about
>   "audit gate closed" or similar still TRUE given everything
>   the prior slices found?
>
> Output structured findings. Cap at 1500 words. End with: are
> we genuinely complete, or do we need another round?

---

### Slice 11 — test-coverage

**Drift surfaces**: 7 (test-coverage)

**Scope**:
- `backend/mcp-server/tests/` (when populated; expected gap until
  Phase 0 conventions migration)
- `backend/mcp-server/src/pbs_mcp/tools/*.py` — load-bearing
  handlers should have corresponding test files
- `backend/mcp-server/src/pbs_mcp/chunkers/*.py` — chunker
  dispatch + per-chunker logic
- `backend/mcp-server/src/pbs_mcp/office_config.py` +
  `office_config_migrations/*.py` — schema validation +
  migration round-trip

**Brief template**:

> Audit test coverage. Check:
> - Does every load-bearing handler / chunker / migration have a
>   corresponding test file?
> - Are tests actually exercising the load-bearing path, or are
>   they trivial smoke tests that pass without exercising
>   anything?
> - Are integration tests (LanceDB / SQLite touchers) marked +
>   runnable?
> - Are mocks used where real-instance tests would be cheap (per
>   `docs/decisions/backend-test-layout.md`)?
> - For each module without tests: is it deferred-by-design (per
>   ROADMAP) or a gap?
>
> Pre-launch state: most modules expected to have zero tests
> until Phase 0 conventions migration. Flag the ones that are
> already in production-equivalent code paths.
>
> Output structured findings. Cap at 1000 words.

---

### Slice 12 — security / data-handling

**Drift surfaces**: 8 (security)

**Scope**:
- `backend/mcp-server/src/pbs_mcp/tools/*.py` (all handlers)
- `backend/mcp-server/src/pbs_mcp/db.py` (SQL construction)
- `backend/mcp-server/src/pbs_mcp/office_config.py` (config
  loading + secret handling)
- `backend/mcp-server/src/pbs_mcp/integrations/**/*.py` (external
  data flow)

**Brief template**:

> Audit security + data-handling. Check:
> - Any SQL/path string interpolation without escape (caught
>   session-5: `db.delete_by_path` was unescaped)
> - User input sanitization at MCP tool boundaries
> - Output: anything logged at INFO that could contain
>   secrets/PII (config values, mail headers, etc.)
> - File path operations: any `..` traversal possibility?
> - MCP tool inputs: do Pydantic validators catch malicious
>   shapes (overly long strings, recursive structures)?
> - Office-config secrets (passwords, API tokens): how are they
>   stored? Plain YAML? `password_ref: <env-var>` indirection?
> - Integration adapters: do they sanitize external data before
>   it crosses the trust boundary into pbs_core?
>
> Pre-launch state: single-user attack surface is small. Flag
> issues by severity assuming future multi-user / hosted
> deployment.
>
> Output structured findings. Cap at 1000 words.

---

### Slice 13 — performance / efficiency

**Drift surfaces**: 9 (performance)

**Scope**:
- `backend/mcp-server/src/pbs_mcp/embedder.py` — model loading,
  inference loops
- `backend/mcp-server/src/pbs_mcp/db.py` — LanceDB queries
- `backend/mcp-server/src/pbs_mcp/chunkers/*.py` — per-chunk
  cost
- `backend/mcp-server/src/pbs_mcp/tools/*.py` — hot-path tool
  handlers
- Caching layers (lru_cache decorators, in-process state)

**Brief template**:

> Audit performance + efficiency. Check:
> - Embedder loaded once per process or per call? (Should be once.)
> - Filesystem walks: do they re-stat the same files across
>   repeated calls? Is there a cache?
> - LanceDB queries: do they have indexes on the filtered
>   columns? Are queries N+1 patterns?
> - Chunkers: any per-chunk LLM call or heavy computation that
>   could be batched?
> - In-process caches (lru_cache): unbounded growth risk?
> - Memory profile: any obvious leaks or unbounded structures?
> - Cold-start cost: how long does first MCP tool call take?
>
> Pre-launch state: corpus small (57 entries). Flag issues
> assuming corpus grows to 500+ entries (post-deployment scale)
> or session length grows to hours.
>
> Output structured findings. Cap at 1000 words.

---

### Slice 14 — boundary-adherence

**Drift surfaces**: 10 (boundary placement)

**Scope**:
- All `plugin/skills/*/SKILL.md` + `plugin/skills/*/PROCEDURE.md`
  — look for inverted-determinism (re-implemented MCP logic) +
  inverted-persistence (direct write of schema-bearing files)
- `backend/mcp-server/src/pbs_mcp/**/*.py` — look for
  inverted-judgment (hardcoded interpretive verdicts)
- Cross-skill: pairs of skills with near-identical procedural
  blocks that should be one Skill Bundle reference
- Cross-tool: pairs of MCP tools with duplicated determinism that
  should be one shared `pbs_core` function

**Brief template**:

> You are running Slice 14 — boundary-adherence per
> ARCHITECTURE.md meta-rule 4 (post-v0.6 sharpening). The
> boundary places deterministic operations on the MCP/Python side
> and judgment/conversation on the skill side, with two
> refinements:
>
> **(A) Persistence-layer rule applies to *typed-contract*
> durable state** (Pydantic + loader + cross-reference
> invariants), NOT to all files. Skill-direct `Read`/`Write` of
> HANDOFF.md, prose memory, READMEs, top-level docs — fine. MCP
> only enforces files with schema/migration/cross-ref contracts.
> The test is contract enforcement, not file extension.
>
> **(B) Reuse direction**: shared deterministic → one MCP tool
> (or one `pbs_core` function used by multiple tools). Shared
> interpretive → one Skill Bundle reference loaded by multiple
> skill consumers.
>
> Audit for FOUR violation patterns:
>
> 1. **Inverted-determinism in skills**: skill body or
>    PROCEDURE.md contains procedural text that two
>    implementations would agree byte-for-byte on (validation,
>    dedup, schema-checking, enumeration, exact-string match)
>    AND that procedure isn't already factored as an MCP tool
>    call. Detect: the skill is *describing how to do* something
>    deterministic instead of *calling a tool* that does it.
>
> 2. **Inverted-judgment in Python**: backend code makes an
>    "is X true of Y?" decision via hardcoded string-match,
>    pattern-check, or threshold where reasonable interpreters
>    could disagree. Detect: code attempts to embed a verdict
>    that the byte-for-byte test fails — should surface to
>    skill, not decide silently.
>
> 3. **Persistence-boundary leak**: skill writes (or non-trivially
>    reads-then-mutates) a schema-bearing file directly, bypassing
>    MCP. Detect: skill body shows `Write` or `Edit` of
>    office-config.yaml, baustein YAML, manifests, schema-bearing
>    state files. Counter-example (NOT a violation): skill
>    `Read`s HANDOFF.md, prose memory `.md`, READMEs — no
>    schema, no migration, fine.
>
> 4. **Reuse-direction violation**: two or more skills carry
>    near-identical procedural-text blocks that should live as
>    one Skill Bundle reference. OR: two or more MCP tools
>    duplicate determinism that should be one shared `pbs_core`
>    function. Detect: textual similarity ≥ ~70% across two
>    consumers on a non-trivial block (≥ ~10 lines).
>
> For each finding: classify which violation pattern (1-4),
> name the file paths + line ranges, propose the canonical home
> (which MCP tool / Skill Bundle reference / `pbs_core` function
> should own it). If the canonical home doesn't yet exist,
> propose its name.
>
> Pre-launch state: every violation is cheap to fix now. Post-
> launch, each callsite becomes a migration. Surface even
> small-blast-radius findings.
>
> Output structured findings. Cap at 1500 words.

---

### Slice 15 — invalidation-contract coverage

**Drift surfaces**: 11 (invalidation-contract)

**Scope**:
- All `plugin/skills/*/SKILL.md` (verify `version:` field present;
  tracked but already partly covered by slice 2)
- All `memory/universal/**/*.md` — prose memory; check
  `references_used: []` frontmatter on docs that cite laws
- All `memory/bausteine/**/*.md` — record memory; check
  `status`, `last_validated`, `review_due`, and per-entry
  `verified_against_version` in `references[]`
- All `extensions/{universal,domain,state}/**/*.yaml` — manifests;
  check top-level `last_updated` + per-entry `last_fetched` +
  `checksum_sha256`
- `office-config.yaml` — check `schema_version` present + matches
  loader's expected version
- `backend/mcp-server/src/pbs_mcp/schemas.py` +
  `office_config.py` + memory-related Pydantic models — verify
  contract fields are required (not silently `Optional`) where
  the rule says they're required
- `plugin/skills/research-references/` body + backend handler —
  verify the cross-cutting refresh actually reads each declared
  invalidation hook

**Brief template**:

> You are running Slice 15 — invalidation-contract coverage per
> ARCHITECTURE.md meta-rule 3. Every entity must declare its
> invalidation contract. This slice verifies that:
> (a) entities actually declare what the rule says they should,
> (b) the declarations have correct shape,
> (c) the cross-cutting handler (`research-references`) actually
> reads them, and (d) sources of truth for the contract agree
> across ARCHITECTURE.md, Pydantic schemas, and skill bodies.
>
> The contract per entity type (per ARCHITECTURE.md meta-rule 3
> table):
>
> - **Skill Bundle**: `version:` field in SKILL.md frontmatter
>   bumped on behavior change.
> - **Memory (prose)**: `references_used: []` frontmatter declares
>   dependent law refs. Required when the doc cites laws/rulings/
>   leitfäden.
> - **Memory (records, bausteine)**: `status: active|flagged|
>   archived|superseded`, `last_validated`, `review_due`,
>   `references[].verified_against_version`.
> - **Configuration (office-config)**: `schema_version` + sequential
>   migration framework.
> - **Configuration (manifests)**: `last_updated` at top-level +
>   per-entry `last_fetched` + `checksum_sha256`.
> - **External data**: per-project `_ai/state.md.lifecycle` +
>   corpus `roots.references/changelog.md`.
> - **Backend**: no declarative hook required (Pydantic schemas
>   + MCP server restart serve as invalidation).
>
> Audit for FOUR violation patterns:
>
> 1. **Missing-contract entities**: entity exists but doesn't
>    declare its invalidation contract. Detect: walk each entity
>    type per scope; flag instances lacking required fields per
>    the rule.
>
> 2. **Incorrect-contract shape**: contract declared but with
>    wrong shape (e.g., `references_used: "..."` as string instead
>    of list-of-dicts; `verified_against_version` missing on a
>    `references[]` entry; `status: "live"` instead of one of the
>    rule's enum values).
>
> 3. **Unread-contract**: contract declared but the refresh
>    handler doesn't read it. Specifically check that
>    `research-references` (skill body + any backend `find_*`
>    tools it calls) actually consults each declared field. A
>    declared-but-unread hook gives false assurance.
>
> 4. **Three-source-of-truth disagreement**: ARCHITECTURE.md's
>    table says X; Pydantic schema in `pbs_mcp/schemas.py` (or
>    `office_config.py` etc.) says Y; SKILL.md body or PROCEDURE.md
>    references Z. The three sources should agree on what's
>    required, what's optional, what enum values are allowed.
>
> For each finding: classify pattern (1-4), name file paths +
> line ranges, propose fix (add field / fix shape / wire handler /
> align schema-doc-skill).
>
> Pre-launch state: bausteine directory is currently empty per
> HANDOFF — pattern 2 for bausteine yields no findings until
> records exist. Manifests + memory-prose are populated; pattern
> 1 + 4 should be checked there carefully. Pattern 3 is the
> most subtle — verify the handler-reads-declaration flow even
> when no actual refresh has fired yet.
>
> Output structured findings. Cap at 1500 words.

---

## Combining slices for full audits

| Round | Default slices | Why |
|---|---|---|
| 1 | 1, 2, 3 | Highest-leverage correctness surfaces (top-level docs, skills, backend tools) |
| 2 | 4, 5, 9 | Adjacent correctness surfaces (plugin scaffolding, content, self-audit) |
| 3 | 6, 7, 8 | Deep cuts (code, cross-refs, READMEs) |
| 4 | 10 | Final-pass cross-cutting + stopping decision |
| **Optional** | **11, 12, 13** | **Implementation quality** (test coverage, security, performance) — run before phase boundaries that increase exposure (first ingest, deployment, multi-user) |
| **Optional** | **14** | **Boundary adherence** (LLM/Python placement) — run after major refactors that may have moved logic across the boundary, or when surfacing a coverage gap audit didn't catch |
| **Optional** | **15** | **Invalidation-contract coverage** (meta-rule 3 enforcement) — run after adding new entity instances (manifests, prose docs, bausteine), after schema changes, or before a refresh cycle to verify handlers will actually read what's declared |

Slices 11-15 are **not part of the default round sequence** —
they're correctness-orthogonal. Run them when a phase boundary
increases exposure on that axis (e.g., before Phase 1 corpus
download = run slice 11 to confirm test coverage; before any
multi-user deployment = run slice 12 for security; after a
boundary-affecting refactor or before locking placement = run
slice 14; after schema changes that touch invalidation contracts
or before a `research-references` refresh = run slice 15).

If a round catches BLOCKERS, immediately run a verification pass
(scope = changed files only) before declaring round complete.

If audit is **focused** rather than full: run only the named
slices; skip the round structure.
