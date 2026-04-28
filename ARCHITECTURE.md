# pbs-bureau architecture — what goes where

This document is the canonical placement reference. When in doubt
about where new content belongs, walk the decision rules below.

Status: v0.1 — confirmed working classification. May refine as edge
cases emerge.

## The six entity types

| # | Type | Where | Frontmatter | What it does |
|---|---|---|---|---|
| **A** | **Skill** | `plugin/skills/<name>/SKILL.md` | Required (Claude Code uses for trigger detection) | Behavioral protocol. Auto-loaded on trigger match. Tells AI HOW to act. |
| **B** | **Skill reference** | `plugin/skills/<name>/references/<file>.md` | Not required | Detailed protocol or specs the parent skill loads on demand. Format specs, checklists, procedures. |
| **C** | **Memory reference content** | `memory/domain/...`, `memory/global/...`, `memory/office/...` | Not required (just `# H1` + body) | Domain knowledge / factual reference / external-reality descriptions consumed by multiple skills. |
| **D** | **Memory data record** | `memory/<scope>/<domain>/<name>.md`, `<project>/_ai/...` | Required (machine-readable fields tools query) | Instance records produced by skill behavior over time. Bausteine, feedback entries, state.md. |
| **E** | **Backend code & docs** | `backend/mcp-server/...` | Code: none. Docs: markdown without frontmatter. | Python implementation + technical schema docs. |
| **F** | **External data** | hidrive (`<hidrive>/Projekte/...`, `<hidrive>/_ai-references/...`, `<hidrive>/_ai-office-state/...`), per-project `<project>/_ai/...` | Varies | Real user data: legal texts, project artifacts, runtime state, correspondence. |

## The decision rules (apply IN ORDER until classified)

For any new piece of content, ask in sequence:

**Rule 1 — Is this Python code or backend technical schema?**
→ `E` (`backend/...`)

**Rule 2 — Is this an instance record produced by a skill's behavior over time** (a saved baustein, a feedback entry written today, a project's `state.md`)?
→ `D` (with frontmatter for queryable fields)

**Rule 3 — Does this tell the AI HOW to do something** (instruction, format spec, checklist, procedure)?
→ Then ask: **is it consumed by ONE skill or MULTIPLE skills?**
- ONE → `B` (skill reference, lives with the skill)
- MULTIPLE (cross-cutting) → `C` (memory) — exception: cross-skill content shouldn't live in one skill's folder

**Rule 4 — Does this describe WHAT something IS** (domain knowledge, external reality, factual reference)?
→ `C` (memory reference content)

**Rule 5 — Should Claude Code auto-discover this and load it on trigger match?**
→ `A` (skill, with frontmatter)

## Worked examples

| Content | Reasoning | Type |
|---|---|---|
| `style-spec.md` (PBS LaTeX style) | Rule 4: describes WHAT the style IS. Cross-cutting (review-draft, draft-*, validate-*). | `C` |
| `korrektur-rules.md` (German writing conventions) | Rule 3: HOW to write — but cross-cutting (multiple skills). Per Rule 3 exception → `C` | `C` |
| `bauleitplanung-phasen.md` (BauGB process) | Rule 4: describes WHAT the process IS. Cross-cutting. | `C` |
| `doctypes.yaml` (registry) | Rule 4: knowledge of what doctypes exist. Cross-cutting. | `C` |
| `baustein-format.md` (how to write a baustein) | Rule 3: instruction. Single-skill (save-baustein). | `B` |
| `feedback-format.md` | Same as above. | `B` |
| `state-format.md` | Rule 3: HOW to write state.md. Currently single-skill (orchestrator does the writes). | `B` |
| `manifest-schema.md` | Rule 3: HOW manifest is structured. Single-skill (research-references). | `B` |
| Doctype checklists | Rule 3: HOW to validate. Single-skill (validate-checklist). | `B` |
| `vector-metadata-schema.md` | Rule 1: backend technical schema. | `E` |
| A future saved baustein | Rule 2: instance record. | `D` |
| A future feedback entry | Rule 2: instance record. | `D` |
| A future `<project>/_ai/state.md` | Rule 2: instance record. | `D` |
| `orchestrator` SKILL.md | Rule 5: auto-loaded on trigger match. | `A` |
| `save-baustein` SKILL.md | Rule 5: same. | `A` |

## What changes invalidate what

- **Update to a Skill (A)** → AI's behavior changes. Re-link cache via `dev-link.sh` if not symlinked; otherwise reinstall.
- **Update to a Skill reference (B)** → parent skill behavior precision changes on next session.
- **Update to Memory reference content (C)** → AI's domain knowledge changes; downstream skills may produce different output.
- **Update to Memory data record (D)** → that record's instance state changes; tools see new field values.
- **Update to Backend (E)** → backend behavior changes; restart MCP server.
- **Update to External data (F)** → runtime state changes; if ingested into RAG, re-ingest the changed paths.

## Borderline cases (resolved here for now)

### `korrektur-rules.md` — instruction or knowledge?

Borderline. It's HOW to write LaTeX. But it's consumed by multiple
skills (review-draft, draft-*, validate-latex-style). Per Rule 3
exception: cross-cutting wins → `C` (memory).

Alternative: a "shared-references" pattern where multiple skills
load by path. Works but less clean. We'd revisit if more cross-skill
references emerge.

### `state-format.md` — single skill or future-multi-skill?

Today the orchestrator does state.md writes (during binding). If a
binding-specialist or scope-change-handler skill is later extracted,
state-format.md may need to move (or become cross-cutting → `C`).
For now: single-skill, lives at
`plugin/skills/orchestrator/references/`.

### Office-specific vs domain-generic in `memory/`

Currently `memory/domain/style/style-spec.md` and
`memory/domain/conventions/korrektur-rules.md` are PBS-instance-
specific (another planning office would have different LaTeX style
and possibly different writing conventions). They live in `domain/`
because conceptually they're "this office's domain knowledge."

If we ever want to fork pbs-bureau cleanly for another office, these
should move to `memory/office-config/`. Not done in v0.1 — flagged
for future refactor.

## How to use this document

When adding new content:

1. Walk Rules 1-5 above. Pick the first one that classifies.
2. Place the content in the matching path.
3. If classification is unclear, surface the case to the user with
   reasoning before placing.
4. If a new pattern emerges that doesn't fit cleanly, propose an
   amendment to this document — don't silently break the taxonomy.

When reviewing existing content during refactors:

1. For each file, check: does its current location match Rules 1-5?
2. If not, propose move with reasoning.
3. Don't move silently.

This document evolves with the system. Refinements expected as
real-use surfaces edge cases.
