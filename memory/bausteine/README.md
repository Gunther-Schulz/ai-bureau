# Bausteine — saved reusable text/argumentation patterns

Bausteine are Type-D records (instance records produced by skill
behavior over time) — captured by the `save-baustein` skill, queried
by `find_bausteine_by_reference` and `verify-citations`, surfaced
during drafting.

## Layout — mirrors the `(universal × domain × state)` scope

```
memory/bausteine/
├── universal/<name>.md       # applies regardless of domain or state (rare)
├── domain/<X>/<name>.md      # naturschutz, pv-ffa, wind, ...
└── state/<X>/<name>.md       # state-specific (e.g. M-V Verfahrensvermerk variants)
```

A baustein declares its scope in frontmatter:

```yaml
---
name: <baustein-name>
scope:
  layer: universal | domain | state
  key: <Naturschutz | MV | ...>     # null when layer == universal
type: text-block | argumentation | spec | citation
references:
  - {law: BNatSchG, paragraph: §44 Abs.1}
  - {ruling: BVerwG-9-A-22-13}
  - {leitfaden: KNE-Anlagengestaltung}
status: active | flagged | retired
flagged_reason: ""
last_reviewed: 2026-04-28
review_due: 2027-04-28
use_count: 0
---
```

Path matches the scope: `domain/Naturschutz/...` for
`scope.layer: domain, scope.key: Naturschutz`. The
`save-baustein` skill enforces this.

## Single-scope rule

A baustein has exactly one scope. If a candidate baustein appears
to fit multiple scopes (e.g. both `domain/PV-FFA` and `domain/Wind`),
either:
- Promote it up the layer (`universal` if truly cross-domain), or
- Split it into two specialized bausteine.

Cross-scope leaks are an early signal that the content isn't really
a single reusable unit.

## Loader behavior

Tools (`find_bausteine_by_reference`) walk the tree, filter by the
office's active `scope.domains[]` + `scope.states[]` from
`office-config.yaml`. Universal bausteine always match.
