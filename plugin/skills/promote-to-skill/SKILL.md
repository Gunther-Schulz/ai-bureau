---
name: promote-to-skill
description: This skill should be used when a baustein has been used frequently enough (≥3 references) that codifying it as its own skill is justified. Triggered by orchestrator's watch list T3 (promotion) when the user accepts via the four-way menu, or by direct user phrases like "promote this baustein", "make this a skill", "skill draus machen".
version: 0.1.0
license: MIT
---

# promote-to-skill

Specialist skill for memory→skill graduation. Takes an existing
baustein with high use_count and proven track record, scaffolds a
new skill that codifies the pattern as procedural behavior.

## Load this now

Read `<repo>/memory/universal/baustein-format.md` (already in skill
references via save-baustein, but reference its location).

Read the source baustein the user wants to promote — full content,
all frontmatter fields including `successful_uses[]` and `references[]`.

## When invoked

By orchestrator's watch list T3 (≥3 uses across recent sessions) when
user picks "handle-now" in the four-way menu, or by direct user
request "promote this baustein to a skill".

Inputs:
- **Source baustein name** — must exist in memory.
- **Target skill name** (optional; suggested) — kebab-slug.
- **Trigger phrases** (optional; suggested) — when should the new
  skill auto-load?

## Behavior

1. **Read source baustein**:
   - Verify use_count ≥ 3 AND at least 2 entries in
     `successful_uses[]` (hard guard — don't promote unproven
     bausteine; per orchestrator PROCEDURE.md Checkpoint 6.4
     baustein promotion guard requires source-project finalized).
   - Read When-to-use, Content, Notes, History sections.

2. **Propose target skill structure**:
   - **Frontmatter** with description derived from baustein's
     "When to use" + concrete trigger phrases extracted from
     successful_uses contexts.
   - **Body** with: Load this now (point at memory/universal/<domain>/
     <baustein>.md as the canonical content), When invoked
     (extracted from When-to-use), Behavior (procedural steps for
     applying the pattern), Output, Edge cases, Tools used.
   - **References folder** with the original baustein content
     copied or symlinked (decision: copy for stability —
     promote-to-skill is a one-time event; later edits to the
     baustein are tracked separately).

3. **Surface proposal to user** — full draft of the new SKILL.md +
   description + trigger phrases. User confirms or edits.

4. **On confirmation, write**:
   - `<repo>/plugin/skills/<target-name>/SKILL.md`
   - `<repo>/plugin/skills/<target-name>/references/baustein.md`
     (copy of source baustein content)
   - Update source baustein frontmatter:
     - `superseded_by: <target-skill-name>` (skill takes priority)
     - `status: archived` (the baustein is now redundant)
   - Append entry to source baustein History: "promoted to skill <date>"

5. **Inform user** — paths written, suggest re-linking via
   `dev-link.sh` for the cache to pick up new skill.

## Output

```
Promoting §45-nr5-innenbereich-privat to skill: §45-nr5-argumentation

Proposed skill:
  Trigger: "ausnahmegrund §45 nr5", "innenbereich privat",
           "reine planungsrechtliche verankerung reicht nicht"
  Behavior:
    1. Read source baustein content
    2. Apply combined Nr.5 + §1a Abs.2 BauGB argumentation
    3. Reference BVerwG 9 A 22.11
    4. Adapt to project context (Innenbereichssatzung-Datum, ...)

Files to write:
  - plugin/skills/§45-nr5-argumentation/SKILL.md
  - plugin/skills/§45-nr5-argumentation/references/baustein.md

Source baustein will be marked archived (superseded_by:
§45-nr5-argumentation).

Confirm? [y/n/edit-draft]
```

## Edge cases

- **Source baustein has rejected_uses entries**: surface them —
  promotion may not be appropriate if the pattern has mixed track
  record. Ask user before proceeding.
- **Target skill name collides** with existing skill: ask for
  alternative name or merge strategy.
- **Source baustein references[] are stale** (research-references
  shows drift): refuse to promote until citations are refreshed.
- **Source baustein scope is project**: a project-scope baustein
  can't be promoted directly to a skill. Path forward: first save
  it to domain scope (with user confirmation that it generalizes),
  then promote.

## Tools used

- `Read` — source baustein, format docs.
- `Write` — new SKILL.md, references/baustein.md.
- `Edit` — source baustein frontmatter (mark superseded).
- No MCP backend dependency for the promotion itself.
