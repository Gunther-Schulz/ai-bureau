---
name: promote-to-skill
description: This skill should be used when a baustein has been used frequently enough (≥3 references) that codifying it as its own skill is justified. Triggered by orchestrator's watch list T3 (promotion) when the user accepts via the four-way menu, or by direct user phrases like "promote this baustein", "make this a skill", "skill draus machen".
version: 0.5.0
license: MIT
mcp_tools_required: [get_baustein, archive_baustein, get_project_state]
mcp_tools_optional: [list_bausteine, find_bausteine_by_reference]
fallback_when_mcp_absent: "without get_baustein / archive_baustein / get_project_state the skill cannot operate — bausteine + state.md are contract-bearing (frontmatter contracts, invariants) per ARCHITECTURE meta-rule 4 fail-closed corollary. Surface 'MCP unreachable; restart backend' and stop. The new-skill scaffold (Write of plugin/skills/<name>/SKILL.md) is filesystem-direct because skill files are contract-free at create-time."
summary: Promotes a frequently-used baustein (≥3 references) to its own skill.
routing_mode: direct
triggers:
  - promote baustein to skill
  - make this a skill
handoffs: []
phase_role: utility
---

# promote-to-skill

Specialist skill for memory→skill graduation. Takes an existing
baustein with high use_count and proven track record, scaffolds a
new skill that codifies the pattern as procedural behavior.

## Load this now

Read `<repo>/plugin/skills/save-baustein/references/format.md` for
the baustein format spec — needed because the source baustein's
frontmatter (especially `references[]`,
`verified_against_version`, `successful_uses[]`,
`cross_project_visible`) drives the promoted skill's frontmatter
declarations and trigger derivation.

Read the source baustein the user wants to promote — full
content, all frontmatter fields. Use `get_baustein(name,
scope?, scope_key?)` (MCP tool) — increments use_count; that's
intentional (the promotion is itself a usage).

## When invoked

By orchestrator's watch list T3 (≥3 uses across recent sessions)
when user picks "handle-now" in the four-way menu, or by direct
user request "promote this baustein to a skill".

Inputs:

- **Source baustein name** — must exist in memory.
- **Target skill name** (optional; suggested) — kebab-slug.
- **Trigger phrases** (optional; suggested) — when should the
  new skill auto-load?

## Behavior

1. **Read source baustein** via
   `get_baustein(name, scope?, scope_key?)`:

   - Verify `use_count ≥ 3` AND at least 2 entries in
     `successful_uses[]` (hard guard — don't promote unproven
     bausteine).
   - Verify per orchestrator PROCEDURE.md Checkpoint 6.4
     baustein promotion guard: read source project's lifecycle
     via `get_project_state(source_project).state.lifecycle` (gate-
     only — never Read state.md directly per meta-rule 4). Must be
     `finalized` (when source is project-scope). If not finalized →
     BLOCK; require explicit "ich autorisiere die frühe Promotion"
     override + log to product-backlog.
   - Read When-to-use, Content, Notes, History sections.

2. **Determine target skill scope**: promoted skill INHERITS the
   source baustein's scope semantics. Per ARCHITECTURE.md scope
   orthogonality:

   - Source baustein scope = `universal` → skill is universal
     (always available)
   - Source baustein scope = `domain` (e.g. `Naturschutz`) →
     skill is domain-scoped; should declare in trigger
     description that it applies only when that domain is in
     `office_config.scope.domains`. Future: a registered-skill
     scope mechanism could enforce this; today it's a
     description convention.
   - Source baustein scope = `state` → skill is state-scoped
     (rare; usually state-specific patterns aren't generalizable
     enough for skill graduation)
   - Source baustein scope = `project` → CANNOT promote
     directly. Path forward: first save it to broader scope
     (universal/domain/state) with user confirmation that it
     generalizes, then promote. Or use `cross_project_visible:
     true` flag if it's reusable across projects without yet
     being skill-worthy.

3. **Propose target skill structure**:

   - **Frontmatter** — derived from baustein:
     - `name`: target skill name (user-provided or suggested
       slug)
     - `version`: `0.1.0`
     - `description`: from baustein's "When to use" + trigger
       phrases extracted from successful_uses contexts
     - `mcp_tools_required[]` — derived from what the baustein
       content actually requires when applied (often
       `search_corpus` for source-grounding, possibly
       `list_reference_manifests`). Per meta-rule 5.
     - `mcp_tools_optional[]` and `fallback_when_mcp_absent` —
       declare graceful-degradation contract.
   - **Body** with: Load this now (point at the source baustein
     copy under `references/baustein.md` as canonical content),
     When invoked (extracted from When-to-use), Behavior
     (procedural steps for applying the pattern), Output, Edge
     cases, Tools used.
   - **References folder** with the original baustein content
     copied (decision: copy for stability — promote-to-skill is
     a one-time event; later edits to the baustein are tracked
     separately via the archive's `superseded_by` pointer).

4. **Surface proposal to user** — full draft of the new SKILL.md
   + description + trigger phrases + scope inheritance noted.
   User confirms or edits.

5. **On confirmation, write**:

   - `<repo>/plugin/skills/<target-name>/SKILL.md`
   - `<repo>/plugin/skills/<target-name>/references/baustein.md`
     (copy of source baustein content)
   - Update source baustein via `archive_baustein(name,
     superseded_by=<target-skill-name>)`:
     - Sets `status=archived`
     - Sets `superseded_by = <target-skill-name>`
   - Append entry to source baustein History via direct Edit:
     "promoted to skill <date>"

6. **Inform user** — paths written, suggest re-linking via
   `dev-link.sh` for the cache to pick up new skill.

## Output

```
Promoting §45-nr5-innenbereich-privat (domain/Naturschutz) to skill.
  Source scope: domain/Naturschutz → promoted skill scope: domain
  (description notes "applies when scope.domains contains
  Naturschutz"; future: registered-skill scope mechanism)

Proposed skill: §45-nr5-argumentation
  Trigger: "ausnahmegrund §45 nr5", "innenbereich privat",
           "reine planungsrechtliche verankerung reicht nicht"
  mcp_tools_required: [search_corpus]
  mcp_tools_optional: [list_reference_manifests, read_corpus_file]
  fallback_when_mcp_absent: "degrade to manual citation lookup;
                             warn user about source-grounding gap"

  Behavior:
    1. Read source baustein content
    2. Apply combined Nr.5 + §1a Abs.2 BauGB argumentation
    3. Reference BVerwG 9 A 22.11 (verify-citations validates
       freshness)
    4. Adapt to project context (Innenbereichssatzung-Datum, ...)

Files to write:
  - plugin/skills/§45-nr5-argumentation/SKILL.md
  - plugin/skills/§45-nr5-argumentation/references/baustein.md

Source baustein will be:
  - status: archived
  - superseded_by: §45-nr5-argumentation

Confirm? [y/n/edit-draft]
```

## Edge cases

- **Source baustein has rejected_uses entries**: surface them
  — promotion may not be appropriate if the pattern has mixed
  track record. Ask user before proceeding.
- **Target skill name collides** with existing skill: ask for
  alternative name or merge strategy.
- **Source baustein references[] are stale** (any
  `verified_against_version` lags manifest current): refuse to
  promote until citations are refreshed via `verify-citations`.
  Promoting a stale-referenced baustein bakes drift into the
  skill.
- **Source baustein scope is project**: refuse direct promotion
  per behavior step 2. Offer: (a) first save to broader scope
  (universal/domain/state), then promote; (b) set
  `cross_project_visible: true` instead if cross-project reuse
  is the actual goal (no scope change needed).
- **Source project not finalized** (project-scope baustein):
  BLOCK per orchestrator guard 6.4. Override requires explicit
  "ich autorisiere die frühe Promotion" and logs to
  product-backlog.

## Tools used

- `get_baustein(name, scope?, scope_key?)` (MCP, required) —
  read source baustein with use_count++.
- `archive_baustein(name, superseded_by)` (MCP, required) —
  archive source after skill scaffolded.
- `list_bausteine(scope?, scope_key?)` (MCP, optional) — for
  collision check (does similar promoted skill exist already?).
- `find_bausteine_by_reference(law?, paragraph?, ruling?,
  leitfaden?)` (MCP, optional) — find related bausteine that
  might also benefit from promotion in the same pass.
- `Read` — format docs, neighboring skills for naming
  consistency.
- `Write` — new SKILL.md, references/baustein.md.
- `Edit` — append to source baustein History section.

When MCP backend unreachable: fall back to filesystem `Read` of
the source baustein + `Edit` on its frontmatter for archive.
Skill scaffold (`Write`) is filesystem-direct regardless. Warn
user about degraded mode.
