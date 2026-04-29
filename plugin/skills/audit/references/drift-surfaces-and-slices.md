# Drift surfaces + slice library

## The 6 drift-surface categories

Every finding falls into one of these. Slices target one or more
categories; rounds combine slices to cover the surface space.

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

**Drift surfaces**: all 6, but specifically looking for what
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

## Combining slices for full audits

| Round | Default slices | Why |
|---|---|---|
| 1 | 1, 2, 3 | Highest-leverage surfaces (top-level docs, skills, backend tools) |
| 2 | 4, 5, 9 | Adjacent surfaces (plugin scaffolding, content, self-audit) |
| 3 | 6, 7, 8 | Deep cuts (code, cross-refs, READMEs) |
| 4 | 10 | Final-pass cross-cutting + stopping decision |

If a round catches BLOCKERS, immediately run a verification pass
(scope = changed files only) before declaring round complete.

If audit is **focused** rather than full: run only the named
slices; skip the round structure.
