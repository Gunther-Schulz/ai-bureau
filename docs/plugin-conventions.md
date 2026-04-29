# Plugin conventions

> **Scope boundary.** This doc covers idioms within Type A (skills)
> and Type B (skill references) — and prospectively Type-A-adjacent
> scaffolding for agents/hooks when those land. For "where does X
> belong?" questions, see `ARCHITECTURE.md`. Specifically, meta-rule
> 5 (execution locality) decides what is a tool vs. skill behavior;
> this doc decides *how* a skill is written once that's settled.
> Backend Python idioms live in `docs/backend-conventions.md`.

Conventions for `plugin/skills/` and related plugin entities. Skills
are auto-discovered from `plugin/skills/*/SKILL.md`; the conventions
below are followed by precedent across the 16 current skills and
codified here so the next skill author doesn't have to reverse-
engineer them.

---

## 1. Frontmatter contract

Every `SKILL.md` carries YAML frontmatter at the very top:

```yaml
---
name: <kebab-case-skill-name>
description: This skill should be used when... <trigger criteria> + concrete trigger phrases (German + English).
version: 0.X.Y
license: MIT
mcp_tools_required: [tool_a, tool_b]
mcp_tools_optional: [tool_c]
fallback_when_mcp_absent: "<one-sentence describing degraded mode>"
---
```

### Required fields

- **name** — kebab-case; matches the directory name (`plugin/skills/<name>/SKILL.md`).
- **description** — opens with `"This skill should be used when…"` (or close variant: `"to draft…"`, `"during the structural review layer…"`). Names concrete trigger phrases in **both German and English**. Trigger phrases should be specific enough not to overlap with other skills' triggers (see §10 for trigger-phrase discipline).
- **version** — semver per §3 below.
- **license** — `MIT` (matches plugin license).

### Meta-rule-5 fields (required, per ARCHITECTURE.md §Meta-rule 5)

- **mcp_tools_required** — list of MCP tool names the skill *cannot operate without*. Empty array `[]` is valid (positive declaration of "no MCP tools needed").
- **mcp_tools_optional** — list of MCP tool names the skill *uses when available* but degrades gracefully without.
- **fallback_when_mcp_absent** — one sentence describing what degraded behavior looks like when MCP is unreachable. For pure-filesystem skills, say so explicitly.

The orchestrator + the `list_skills` MCP tool consume these fields for planning. Empty arrays are positive declarations and **must** be present even when no tools are needed.

### Anti-patterns

- ❌ Omitting any of the three meta-rule-5 fields (silent absence ≠ positive declaration).
- ❌ Listing tools in `mcp_tools_required` that the body never calls.
- ❌ Calling MCP tools in the body that aren't declared.
- ❌ Trigger phrases that overlap with another skill's (e.g. bare "review" routing to both `review-draft` and `validate-checklist`).
- ❌ Description that just restates the name (`"This skill drafts cover mails"` — instead, say *when* it's used and what triggers it).

---

## 2. Skill reference (Type B) frontmatter

Files under `plugin/skills/<name>/references/<file>.md` are Type B per ARCHITECTURE.md. **No frontmatter required.** Add frontmatter only when a reference file declares data the platform should query (rare); a plain `# heading` start is standard.

---

## 3. Version semver — two decoupled tracks

### Per-skill version (in `SKILL.md` frontmatter `version:` field)

| Bump | When |
|---|---|
| **major** | Breaking change to the skill's external contract: skill renamed, trigger-phrase semantics changed, expected inputs/outputs reshaped. |
| **minor** | Skill behavior changes — including changes to load-bearing frontmatter that orchestrator/list_skills consume (e.g. adding `mcp_tools_required[]`, expanding/narrowing trigger phrases, reorganizing the body's behavior steps). |
| **patch** | Wording / typo / formatting fixes; clarifications that don't change behavior. |

**Frontmatter changes are usually minor**: orchestrator's planning depends on them. The session-5 F-batch initially treated frontmatter additions as patch bumps (`0.2.0 → 0.2.1`); that was retroactively corrected to minor (`0.2.0 → 0.3.0`) when the discipline was codified. **The discipline going forward**: if the orchestrator or any other tool/skill reads the field for planning, changing it = behavior change = minor bump.

### Plugin-wide version (in `plugin.json`)

| Bump | When |
|---|---|
| **major** | Breaking changes to plugin manifest format, plugin name change. |
| **minor** | New skill added, skill removed, MCP wiring changed, manifest layout change. |
| **patch** | Documentation / README polish that doesn't affect plugin shape. |

The two tracks are decoupled: a single skill can rev to `0.4.0` without touching `plugin.json`'s `0.1.0`.

---

## 4. SKILL.md body structure

By convention, a skill body has this section order:

```markdown
# <skill-name>

<2-4 sentences: what this skill does, what it composes against>

## Load this now

<optional — references the skill loads on activation. Names files
under references/ + cross-cutting memory docs under <repo>/memory/.>

## When invoked

<concrete trigger contexts: orchestrator gates, user phrases.
Lists the modes/inputs the skill expects.>

## Behavior

<the procedure the skill follows. Numbered steps. Each step is
self-contained; the orchestrator/skill-author can reorder or skip
based on context.>

## Output

<what the user sees: format, key items, the verdict statement.>

## Edge cases

<bullet list: known weird inputs and the skill's response.>

## Tools used (optional — frontmatter is authoritative)

<commentary on which tools matter when. Frontmatter
mcp_tools_required[] is the source of truth; this section is
optional context for the reader.>
```

Variations: orchestrator + review-draft have a separate `PROCEDURE.md` for multi-checkpoint state. Most skills don't need one.

---

## 5. References organization (Type B)

`plugin/skills/<name>/references/*.md` holds detailed protocols, format specs, checklists, or worked examples that the parent SKILL.md loads on demand. Keep these files focused: one file per topic.

Examples in current skills:

- `save-baustein/references/format.md` — canonical baustein frontmatter spec
- `setup-office/references/wizard-flow.md` — step-by-step interactive script
- `research-references/references/manifest-schema.md` — manifest YAML schema

References are loaded by the parent SKILL.md's "Load this now" section. The skill itself is the entry point; references are detail.

---

## 6. PROCEDURE.md (multi-checkpoint state)

Add a `PROCEDURE.md` only when the skill carries state across multiple checkpoints (e.g. orchestrator: phase gates; review-draft: layered review). Most skills don't need one. PROCEDURE.md uses the same layered-section convention as SKILL.md but with explicit checkpoint numbering (`### 4.2 Layered review`, `### 6.4 Promote-to-skill guard`).

---

## 7. Routing handoff conventions

When skill A needs skill B's behavior:

- **Inline reference**: `"Hands off to <skill-B>"` followed by the trigger context. Example: `"Hands off to author-manifest if the target manifest doesn't yet exist."`
- **Don't duplicate B's behavior** in A — defer to B and let the orchestrator route.
- **Verify B exists**: when adding a handoff, confirm the target skill name is current (rename drift breaks handoffs silently).
- **Bidirectional handoffs are valid**: `research-references` ↔ `author-manifest` is a clean example.

The orchestrator's PROCEDURE.md §10 specialist routing list is the **at-a-glance** reference; the `list_skills` MCP tool is **authoritative** (auto-discovered from frontmatter, never stale).

---

## 8. Filesystem path conventions

| Token | Resolution |
|---|---|
| `<repo>/` | Plugin/repo root. Two directories up from any `plugin/skills/<name>/SKILL.md`. |
| `<project>/_ai/` or `<project>/.ai/` | Per-project AI memory. Both forms are supported (legacy `_ai/` for adopted projects, `.ai/` for new bindings — see `memory/universal/project-structure.md`). Skills should accept either. |
| `<state-root>/` | Office state root, resolved via `office_config.roots.state`. |
| `<references-root>/` | RAG corpus root, resolved via `office_config.roots.references`. |
| `<projects-root>/` | Client projects root, resolved via `office_config.roots.projects`. |

Never hardcode absolute paths in skill bodies. Always derive from `office-config.yaml` (loaded by orchestrator into in-memory `office_config`).

---

## 9. Domain + state capitalization

Canonical values are case-sensitive — match the directory names under `extensions/{domain,state}/`:

- **Domains**: `Naturschutz`, `PV-FFA`, `Wind`, `Innenentwicklung` (skeleton)
- **States** (ISO Bundesland codes): `MV`, `BB`, `BW`, `BE`, `HB`, `HH`, `HE`, `NI`, `NW`, `RP`, `SH`, `SL`, `SN`, `ST`, `TH`

Lowercase or alternate forms in code/docs/frontmatter are **drift**. The `save-baustein` MCP tool enforces case match against the manifest set; `office-style.<DOMAIN>.sty` files use the same casing.

---

## 10. MCP tool naming

Every MCP tool name is **snake_case** matching the corresponding `pbs_core` Python function name (or, if no `pbs_core` split yet, the handler function in `pbs_mcp/tools/`). This is forward-compatible with the future integration registry.

Current Tier 1 + Tier 2 tool names — don't drift to alternate forms:

```
search_corpus, read_corpus_file, ingest_paths
ingest_project_inputs, search_inputs
list_bausteine, get_baustein, save_baustein, flag_baustein, archive_baustein
find_bausteine_by_reference
list_projects, bind_project, setup_project, scaffold_project, survey_project
list_skills, list_reference_manifests, list_doctypes_manifests
list_skeletons
compile_latex
```

Skills calling these tools use the exact snake_case form in body text.

---

## 11. Trigger-phrase discipline

Skill `description:` fields drive Claude Code's auto-routing. Two skills routing on the same phrase = ambiguous routing.

- **Be specific**: `"structural check"`, `"strukturell prüfen"`, `"Strukturprüfung"` — not bare `"review"` / `"prüfen"`.
- **Cover both languages**: every domain-relevant phrase should appear in German + English (English first on default).
- **Top-level vs. delegated routing**: skills that the user *invokes directly* (e.g. `review-draft`) own broad trigger phrases. Skills that the orchestrator *delegates to* (e.g. `validate-checklist` for Layer 1 of layered review) should narrow their trigger phrases to delegation-specific phrases — and explicitly note in the description that broad phrases route to the delegating skill instead.

The session-5 audit caught `validate-checklist` claiming bare `"review"` / `"prüfen"` triggers; those were tightened to `"structural check"` / `"strukturell prüfen"` etc. Pattern to repeat for any future delegated skill.

---

## 12. Body language

- **Match the user's language**: skill bodies that interact with the user ask in the user's language (German default for this plugin given the German planning-bureau target). Code/path/identifier bits stay in English.
- **Use citations consistently**: `§ 44 Abs.1 BNatSchG` (with `~` non-breaking space in LaTeX context — see `memory/universal/conventions/korrektur-rules.md`).
- **Use canonical scope vocabulary**: `universal | domain | state | project` (NOT `global | domain | project`).

---

## 13. Anti-patterns to avoid

- ❌ Hardcoding office-specific values (identity, paths, signatures) in skill body. Pull from `office_config` instead.
- ❌ Hardcoding domain lists (`["Naturschutz", "PV-FFA", "Wind"]`) in skill body. Read from `office_config.scope.domains` or `list_doctypes_manifests()`.
- ❌ Inventing MCP tool names that don't exist (e.g. `query_skills`, `enumerate_manifests`). Always use the canonical names from §10.
- ❌ Frontmatter dependency declarations that don't match body usage (drift in either direction).
- ❌ Skill bodies with placeholder `TODO` / `FIXME`. If something is genuinely deferred, log a T6 trigger via orchestrator's watch list, don't ship a half-skill.
- ❌ Bypassing the orchestrator framework ("never bypass — loaded means active" per orchestrator/SKILL.md).

---

## 14. Agents (deferred to v1+)

When the first agent lands at `plugin/agents/<name>.md`, conventions will be added here. Expected shape (per skill-craft):

- Frontmatter: `name`, `description` (when-to-use trigger), `tools` (which tools the agent can call), `model` (optional override).
- Distinct from skills: agents are spawned for focused passes (deep code review, exhaustive citation verification) and run autonomously to a structured return.

---

## 15. Hooks (deferred until concrete need)

Hooks land at `plugin/hooks/hooks.json`. Per ARCHITECTURE meta-rule 5: "static path-blocks go through `settings.json` permissions instead." Hooks should be reserved for genuinely event-driven automation (e.g. detect external file change → re-ingest), not for replicating tool-permission logic.
