# Plugin conventions

> **Scope boundary.** This doc covers idioms within Skill Bundles
> (SKILL.md + skill references) — and prospectively Skill-adjacent
> scaffolding for agents/hooks when those land. For "where does X
> belong?" questions, see `ARCHITECTURE.md`. Specifically, meta-rule
> 4 (execution-determinism) decides what is a tool vs. skill behavior;
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
description: This skill should be used when... <trigger criteria> + concrete trigger phrases.
version: 0.X.Y
license: MIT
mcp_tools_required: [tool_a, tool_b]
mcp_tools_optional: [tool_c]
fallback_when_mcp_absent: "<see §11 fallback-policy>"
summary: <1-2 sentence what-and-when, language-agnostic>
routing_mode: direct        # | delegated | always_active
triggers:
  - <concept-label>          # one entry per concept; LLM matches semantically
  - <German technical term>  # only when domain-anchor (UNB, Stellungnahme, …)
delegated_from: [<skill>]   # only when routing_mode=delegated
handoffs: [<skill1>, <skill2>]
phase_role: utility         # | phase_a_entry | phase_b_entry | layer_1 | layer_2 | layer_3 | routing | bureau_setup | manifest_authoring | lifecycle | meta
---
```

### Required identity fields

- **name** — kebab-case; matches the directory name (`plugin/skills/<name>/SKILL.md`).
- **description** — opens with `"This skill should be used when…"` (or close variant: `"to draft…"`, `"during the structural review layer…"`). Names concrete trigger phrases in whatever language is natural; LLM auto-router matches semantically across languages (per `docs/decisions/trigger-convention.md`). German technical terms (UNB, Stellungnahme, Bauleitplanung, Festsetzungen) belong here when they're domain-anchors, not as bilingual translation pairs. **Canonical Claude-Code-readable trigger surface** — Claude Code's auto-router reads this field directly. The `triggers[]` list below is the scannable concept-label index.
- **version** — semver per §3 below.
- **license** — `MIT` (matches plugin license).

### Meta-rule-5 fields (required, per ARCHITECTURE.md §Meta-rule 5)

- **mcp_tools_required** — list of MCP tool names the skill *cannot operate without*. Empty array `[]` is valid (positive declaration of "no MCP tools needed").
- **mcp_tools_optional** — list of MCP tool names the skill *uses when available* but degrades gracefully without.
- **fallback_when_mcp_absent** — one sentence describing skill behavior when MCP is unreachable. **Per ARCHITECTURE meta-rule 4 fail-closed corollary** (`docs/decisions/mcp-fallback-policy.md`): contract-bearing reads have no fallback path; the skill must surface to user and stop. Fallback strings declare what is *still possible* (contract-free reads, optional-tool degradations) and what causes a hard stop (any contract-bearing dependency). For pure-filesystem skills with no contract-bearing reads, say so explicitly.

The orchestrator + the `list_skills` MCP tool consume these fields for planning. Empty arrays are positive declarations and **must** be present even when no tools are needed.

### Routing + handoff contract (post-design-review session 5, Subsystem 4)

Five additional fields make routing semantics machine-checkable:

- **summary** — 1-2 sentence what-and-when, language-agnostic. Distilled essence of the description for human + machine readers.
- **routing_mode** — one of:
  - `direct`: user-typed phrases auto-route here (the common case)
  - `delegated`: this skill is invoked by another skill; user phrases that match its triggers go to the *delegating* skill first (which may then delegate)
  - `always_active`: skill auto-loads whenever the plugin is in scope (orchestrator only)
- **triggers** — flat list of concept labels that auto-route to this skill. Each entry is one concept; the LLM matches semantically across languages without explicit translation pairs (per `docs/decisions/trigger-convention.md`, session 7). Prefer English concept labels; include German technical terms only when they're domain-anchors (UNB, Stellungnahme, Bauleitplanung, Festsetzungen, Anschreiben), not when they're translations of an English label already present. The old `{phrase, lang}` structured form was retired session 7 — see `docs/decisions/trigger-convention.md` for the rationale (the structure suggested deterministic routing logic that no consumer actually implements; the LLM is the consumer and matches semantically). If a future consumer needs the structure, restore it.
- **delegated_from** — list of skill names that delegate to this one. Required when `routing_mode: delegated`. Reverse direction of `handoffs`.
- **handoffs** — list of skill names this skill explicitly hands off to (e.g. `review-draft → [validate-checklist, verify-citations, validate-latex-style]`). Closes the rename-drift loop: an audit slice can verify every name in `handoffs` resolves to an existing skill.
- **phase_role** — controlled enum locating this skill in the workflow:
  - `routing` — orchestrator (always_active, routes to specialists)
  - `phase_a_entry` — drafting entry skill (e.g. `draft-textteil-b`)
  - `phase_b_entry` — review entry skill (e.g. `review-draft`)
  - `layer_1` / `layer_2` / `layer_3` — layered review delegations
  - `bureau_setup` — first-time office setup
  - `manifest_authoring` — content scaffolding
  - `lifecycle` — project lifecycle (bind, survey)
  - `meta` — system-introspection skills (audit, design-review)
  - `utility` — everything else (research, baustein management, etc.)
- **output_schema** (optional) — name of a Pydantic model in `pbs_mcp/skill_outputs/` that the skill's output must validate against. Per `docs/decisions/sparring-output-v1.md`: skills producing sparring-mode output (counter-argument, confidence, reasoning) declare an `output_schema`; the orchestrator calls `validate_skill_output` after the skill's output and kicks back to the skill with missing-fields if validation fails. Initial v1 schemas: `ReviewOutput` (declared by `review-draft`), `RecommendationOutput` (used by orchestrator's Checkpoint-13 commit-to-recommendation pattern). Skills without this field are not output-validated. Adding the field is a behavior change → minor version bump per §3.

### Anti-patterns

- ❌ Omitting any of the three meta-rule-5 fields (silent absence ≠ positive declaration).
- ❌ Listing tools in `mcp_tools_required` that the body never calls.
- ❌ Calling MCP tools in the body that aren't declared.
- ❌ Trigger phrases that overlap with another skill's (e.g. bare "review" routing to both `review-draft` and `validate-checklist`).
- ❌ Description that just restates the name (`"This skill drafts cover mails"` — instead, say *when* it's used and what triggers it).
- ❌ `triggers[]` and `description` drift: every phrase in `triggers[]` should appear in `description` and vice versa. Audit slice can detect this.
- ❌ `handoffs[]` referencing a skill that doesn't exist (rename drift). Audit slice can detect this.

---

## 2. Skill reference frontmatter

Files under `plugin/skills/<name>/references/<file>.md` are part of the Skill Bundle per ARCHITECTURE.md (post-v0.5: A+B merged). **No frontmatter required.** Add frontmatter only when a reference file declares data the platform should query (rare); a plain `# heading` start is standard.

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

## 5. References organization

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

Skill `description:` fields drive Claude Code's auto-routing. Two skills routing on the same concept = ambiguous routing.

**Triggers are concept labels, not exact-string match targets.** The orchestrator's skill-routing is LLM-mediated — a user typing "schreib mal die Begleitmail an die UNB" routes to the skill listing `draft cover mail` without that exact phrase appearing in triggers. Add an entry only when the concept itself is new or when a German technical term is a domain-anchor (UNB, Stellungnahme, Bauleitplan, Festsetzungen) rather than a translation of a label already present.

- **Be specific**: `structural check`, `validate doctype structure` — not bare `review`. Specificity prevents cross-skill ambiguity, not language coverage.
- **Concept labels in English by default.** German technical terms join only when domain-anchors. Avoid one-to-one translation pairs (`draft cover mail` + `Anschreiben` of the same concept = redundant, drop one).
- **Top-level vs. delegated routing**: skills that the user *invokes directly* (e.g. `review-draft`) own broad concept labels. Skills that the orchestrator *delegates to* (e.g. `validate-checklist` for Layer 1) narrow their concept labels — and explicitly note in the description that broad phrases route to the delegating skill instead.

History: session 5 audit caught `validate-checklist` claiming bare `review` / `prüfen` triggers; those were tightened. Session 7 retired the old `{phrase, lang}` structured form for flat concept labels (`docs/decisions/trigger-convention.md`).

---

## 11b. Fail-closed fallback policy

**The rule** (per ARCHITECTURE.md meta-rule 4 fail-closed corollary + `docs/decisions/mcp-fallback-policy.md`): when MCP is unreachable, contract-bearing reads MUST surface to user and stop. No silent contract bypass via direct `Read`.

**The test for "contract-bearing":** does the file have any of —
- A Pydantic model that validates its shape
- A `schema_version` field with migrations applied on read
- Cross-reference invariants (validity depends on other files' state)
- A loader function in `pbs_mcp/` that constructs a typed object
- A `last_updated` / `last_fetched` / `checksum_sha256` field
  declaring an invalidation contract

If yes → contract-bearing → fail closed. If no → contract-free prose → direct `Read` fine.

**Two file classes, two policies:**

| Class | Examples | If MCP unreachable |
|---|---|---|
| Contract-bearing | state.md, office-config.yaml, doctype manifests (`extensions/.../doctypes.yaml`), reference manifests (`extensions/.../references-manifest.yaml`), baustein YAML (`memory/bausteine/.../*.md`), projects-index.md | **Fail closed.** Surface "MCP unreachable; restart backend." Skill stops. |
| Contract-free prose | HANDOFF.md, decisions.md, file-map.md, correspondence-log.md, module-decisions.md, README, prose memory under `memory/universal/{style,conventions,verfahren,...}/`, top-level docs | Direct Read fine. No gate exists; nothing to bypass. |

**`fallback_when_mcp_absent:` writing rules:**
- For contract-bearing dependencies: explicit fail-closed phrasing — "without \<tool\> the skill cannot operate (\<file class\> is gate-only per fail-closed corollary). Surface 'MCP unreachable; restart backend' and stop."
- For contract-free dependencies: degradation paths are valid — "direct Read of \<contract-free-file\>" is fine.
- For mixed (some contract-bearing tools, some optional): name the gate-required ones first (hard stop), then describe how the skill degrades when *only* optional tools are unavailable (gate is up).

**Anti-patterns:**
- ❌ "fall back to filesystem Read of state.md / office-config.yaml / doctype manifests / baustein frontmatter" — this is the silent contract bypass the corollary forbids. Audit slice 14 catches it.
- ❌ "warn user; degrade to direct Read of \<contract-bearing\>" — same bypass, polite phrasing.
- ❌ "skill operates entirely on filesystem reads" when the skill *does* have contract-bearing deps — under-specified and misleading.

**Counter-example (NOT a violation):** "Glob over memory/bausteine/** to *enumerate candidates*" — listing files is not reading content; no contract bypassed. Reading content via the gate is required for validation.

History: session 7 introduced the corollary + plugin-wide sweep. Audit slice 14 brief extended to scan fallback strings. See `docs/decisions/mcp-fallback-policy.md` for full rationale.

---

## 12. Body language + conversational style

(Cross-skill conventions extracted from orchestrator/PROCEDURE.md
§13 in v0.5 — they apply to all skills, not just orchestrator.)

### Language matching

- Match the user's language per turn. If the user writes German,
  respond German. If English, respond English. Mixed is fine.
- Artifact content (LaTeX bodies, mail drafts, baustein bodies) is
  always German regardless of conversation language — German is
  the canonical work language.
- Code/path/identifier bits stay in English.

### Terseness

- The framework is dense; the conversational surface is light.
- Surface findings inline as one-liners. Save longer prose for
  actual document content or the rare moment where complex
  reasoning needs to be explained.
- Avoid:
  - Bureaucratic acknowledgments ("Verstanden, ich werde nun...")
  - Restatements of what the user just said
  - Emoji unless the user uses them first
  - Multi-paragraph confirmations when one sentence suffices

### Decision-handling

- When uncertain about a decision the user must make, state the
  recommendation alongside the question. Do not present open-ended
  choices; commit to a position the user can react to (per memory
  feedback: "give judgment + recommendations, automate the rest").

### Format conventions

- **Citations**: `§ 44 Abs.1 BNatSchG` (with `~` non-breaking space
  in LaTeX context — see
  `memory/universal/conventions/korrektur-rules.md`).
- **Canonical scope vocabulary**: `universal | domain | state | project`
  (NOT `global | domain | project`).
- **Domain capitalization**: `Naturschutz`, `PV-FFA`, `Wind`,
  `Innenentwicklung` (case-sensitive — see §9).

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

Hooks land at `plugin/hooks/hooks.json`. Per ARCHITECTURE meta-rule 4 (execution-determinism): "static path-blocks go through `settings.json` permissions instead." Hooks should be reserved for genuinely event-driven automation (e.g. detect external file change → re-ingest), not for replicating tool-permission logic.
