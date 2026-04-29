# Bausteine — saved reusable text/argumentation patterns

Bausteine are Type-D records (instance records produced by skill
behavior over time) — captured by the `save-baustein` skill, queried
by `find_bausteine_by_reference` and `verify-citations`, surfaced
during drafting.

## Layout — mirrors the `(universal × domain × state)` scope

```
memory/bausteine/
├── universal/<name>.md        # applies regardless of domain or state (rare)
├── domain/<X>/<name>.md       # X ∈ {Naturschutz, PV-FFA, Wind, Innenentwicklung, ...}
└── state/<X>/<name>.md        # X ∈ ISO Bundesland code: MV, BB, SH, ...

# Project-scope bausteine live with the project, not here:
<project_root>/_ai/bausteine/<name>.md
```

Domain + state keys are case-sensitive and match the directory names
under `extensions/{domain,state}/`.

## Frontmatter schema

The canonical schema lives in
`plugin/skills/save-baustein/references/format.md` — read that file
for the authoritative spec. At a glance:

```yaml
---
name: <stem-matching-filename>
scope: universal | domain | state | project    # flat string discriminator
scope_key: Naturschutz                          # required for domain/state; project name for project scope; null/omitted for universal
type: argumentation | technical-spec | citation | checklist | textbaustein | template
title: <human-readable>
language: de | en | mixed
# ... plus provenance, lifecycle (status: active | flagged | archived | superseded),
# use tracking, cross_project_visible flag, references[] with verified_against_version
---
```

The `scope` + `scope_key` orthogonality is the post-v0.4 schema —
older nested-object shapes (`scope: {layer: ..., key: ...}`) are not
valid. `save-baustein` enforces path-matches-frontmatter.

## Single-scope rule

A baustein has exactly one scope. If a candidate baustein appears
to fit multiple scopes (e.g. both `domain/PV-FFA` and `domain/Wind`),
either:

- Promote it up the layer (`universal` if truly cross-domain), or
- Split it into two specialized bausteine.

Cross-scope leaks are an early signal that the content isn't really
a single reusable unit.

## Loader behavior

The Tier 1 MCP tool `list_bausteine(scope?, scope_key?, project_root?)`
and the Tier 2 `find_bausteine_by_reference(law=, paragraph=, ...)`
walk this tree (plus per-project `_ai/bausteine/`), filter by the
office's active `scope.{domains,states}` from `office-config.yaml`.
Universal bausteine always match.
