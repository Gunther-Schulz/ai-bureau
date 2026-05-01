# Extensions — layered manifests

Reference + doctype registries layered along the orthogonal axes
`(universal × domain × state)`. The backend loader walks the union
of all manifests selected by an office's `scope.domains[]` +
`scope.states[]` (set in `office-config.yaml`).

## Layout

```
extensions/
├── universal/                       # applies to every German bureau
│   ├── references-manifest.yaml    # universal-core: BauGB, BImSchG, ROG, EU directives, federal courts
│   └── doctypes.yaml                # universal doctypes: Begründung, Festsetzungen, Umweltbericht
├── domain/<X>/                      # per planning domain
│   ├── references-manifest.yaml    # domain-specific laws/leitfäden/urteile
│   ├── doctypes.yaml                # domain-specific doctypes (e.g. LBP for Naturschutz)
│   └── skeletons/                   # optional: domain-specific Textbausteine overlays
└── state/<X>/                       # per Bundesland (16 codes: BB, BW, BY, ..., TH)
    ├── references-manifest.yaml    # state laws (LPlG-X, LBauO-X, NatSchAG-X)
    └── doctypes.yaml                # state-specific doctype variants (rare)
```

## Domain catalogue (currently)

- `PV-FFA` — Photovoltaik-Freiflächenanlagen
- `Wind` — Windenergie-an-Land
- `Naturschutz` — Naturschutz / Artenschutz / FFH
- `Innenentwicklung` — Urban Innenentwicklung (skeleton — populate when first office needs it)

New domains: use the `author-manifest` skill.

## State catalogue

All 16 German Bundesländer have placeholder directories. Only `MV/`
is populated (PBS reference deployment). Other states populate when
first office working in that state deploys.

## How offices select scope

`office-config.yaml`:

```yaml
scope:
  domains: [PV-FFA, Wind, Naturschutz]
  states:  [MV]
```

The `setup-office` skill populates these from a multi-select wizard
based on what's available in `extensions/`.
