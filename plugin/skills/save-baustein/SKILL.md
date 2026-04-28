---
name: save-baustein
description: This skill should be used when the user authorizes capturing a reusable text, argumentation pattern, technical specification, or citation as a baustein in memory. Triggered by the orchestrator's four-way decision menu when "capture-now" is chosen, or by direct user request like "save this as a baustein", "speichere das", "merken für später".
version: 0.1.0
license: MIT
---

# save-baustein

Specialist skill for writing bausteine (reusable knowledge modules)
to memory in the canonical format.

## Load this now

Read `references/format.md` for the full baustein format
specification — frontmatter schema, body structure, lifecycle field
rules, and concrete examples.

## When invoked

Triggered by the orchestrator after a "capture-now" decision in the
four-way menu, or by direct user request.

Inputs from invocation context:
- Content to save (text, argumentation, spec, citation)
- Proposed name (kebab-slug)
- Scope: global / domain / project
- Source project (if known)
- Initial `references[]` (legal/leitfaden/ruling deps)

## Behavior

1. Validate scope-appropriate filename per format.md location rules.
2. Compose frontmatter with all required fields populated; optional
   fields with defaults (`use_count: 0`, `last_used: null`,
   `review_due: today+1y`, etc.).
3. Compose body with When-to-use, Content, Notes, History sections.
4. Write to filesystem at `memory/<scope>/<domain>/<name>.md` (or
   `<project>/_ai/bausteine/<name>.md` for project scope).
5. Update scope's INDEX.md.
6. Confirm to user with the path written.

## Status

v0.1: stub. Format reference is complete; behavior implementation
follows when MCP tool surface lands.
