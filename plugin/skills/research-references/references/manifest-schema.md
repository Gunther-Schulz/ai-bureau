# references-manifest.yaml schema

The manifest is the single source of truth for which external
reference documents the assistant tracks. Lives at the repo root
(`<repo>/references-manifest.yaml`). Mirror copy at
`<hidrive>/_ai-references/manifest.json` for offline reference
(auto-generated from the YAML).

## Top-level structure

```yaml
version: 1
last_updated: 2026-04-28
maintainer: pbs-bureau

categories:
  gesetze:
    bund: [...]                            # federal laws
    eu: [...]                              # EU directives
    mv: [...]                              # Mecklenburg-Vorpommern
    other-laender: [...]                  # other Bundesländer (rare)

  leitfaeden: [...]                        # flat list across publishers

  urteile: [...]                           # flat list

  beispiele: [...]                         # exemplary documents

  methodik: [...]                          # methodology standards
```

## Entry schemas

### gesetze entry

```yaml
- id: BauGB
  title: Baugesetzbuch
  short_title: BauGB
  jurisdiction: bund                        # bund | eu | mv | other-laender:<land-code>
  source_url: https://www.gesetze-im-internet.de/baugb/
  source_type: gesetze-im-internet
  canonical_path: gesetze/bund/BauGB.txt   # relative to _ai-references/
  fetch_method: web-text                    # web-text | web-html | manual | git-mirror

  last_fetched: 2026-04-28
  last_modified_at_source: 2024-10-23
  current_amendment_form: |
    "BauGB i.d.F. der Bekanntmachung vom 03.11.2017 (BGBl. I S. 3634),
    zuletzt geändert durch Artikel 48 des Gesetzes vom 23.10.2024
    (BGBl. 2024 I Nr. 323)"
  checksum_sha256: "abc123..."

  archive_versions: true
  retention_versions: 5

  ingest: true
  chunking_strategy: per-paragraph
  chunk_metadata_extractor: gesetze-im-internet

  status: active                            # active | superseded | obsolete
  superseded_by: null
  notes: ""
  tags: [bauleitplanung, federal-baugb]
```

Fields:
- `id` — stable identifier, never changes once set. Referenced from
  bausteine, citations, validations.
- `canonical_path` — relative to `<hidrive>/_ai-references/`.
- `fetch_method` — `web-text` (HTML scrape, plain text), `web-html`
  (preserve structure), `manual` (user uploads), `git-mirror` (clone
  from a known mirror).
- `current_amendment_form` — literal string used by citation-freshness
  validation. Comparison is exact.
- `chunk_metadata_extractor` — name of a Python function in
  `pbs_mcp/extractors/` that parses § structure for ingestion.
- `status: superseded` — law entirely replaced. `obsolete` — once
  tracked but no longer needed.

### leitfaeden entry

```yaml
- id: KNE-PV-Naturschutz
  title: KNE-Auswahlbibliografie PV-FFA Naturschutz
  publisher: KNE — Kompetenzzentrum Naturschutz und Energiewende
  publication_date: 2020-11
  version: "1.0"
  source_url: https://www.naturschutz-energiewende.de/...
  canonical_path: leitfaeden/KNE-PV-Naturschutz.pdf
  fetch_method: web-pdf
  last_fetched: 2026-04-28
  checksum_sha256: "..."
  ingest: true
  chunking_strategy: per-section
  chunk_metadata_extractor: pdf-headings
  status: active
  notes: ""
  tags: [pv-freiflache, naturschutz, leitfaden]
```

Adds `publisher`, `publication_date`, `version`. Often PDFs.

### urteile entry

```yaml
- id: BVerwG-9-A-22-11
  title: "BVerwG — Urteil vom 23.08.2012 — 9 A 22.11"
  short_title: "Freiberg-Entscheidung"
  court: BVerwG
  docket: "9 A 22.11"
  decision_date: 2012-08-23
  jurisdiction: bund
  source_url: https://www.bverwg.de/...
  canonical_path: urteile/BVerwG-9-A-22-11.txt
  fetch_method: web-html
  last_fetched: 2026-04-28
  checksum_sha256: "..."
  ingest: true
  chunking_strategy: per-randnummer
  chunk_metadata_extractor: bverwg-randnummer
  status: active
  notes: |
    Wichtigste Entscheidung zur Begründungstiefe für §45 Abs.7 Nr.5
    bei privaten Vorhaben. Häufig zitiert in UNB-Stellungnahmen.
  tags: [§45-bnatschg, ausnahmegrund, bverwg]
```

### beispiele entry

```yaml
- id: Begruendung-Bad-Suelze-2023
  title: B-Plan Begründung Bad Sülze (Solarpark) 2023-09
  source_artifact: <project>/Externe Gutachten/Begründung_Bad-Sülze_September-2023.pdf
  source_origin: external                    # external | pbs-archive
  canonical_path: beispiele/Begruendung-Bad-Suelze-2023.pdf
  fetch_method: manual
  last_fetched: 2024-08-12
  checksum_sha256: "..."
  ingest: true
  chunking_strategy: per-section
  chunk_metadata_extractor: pdf-headings
  status: active
  notes: ""
  tags: [b-plan-begruendung, solar, mv, exemplary]
```

### methodik entry

```yaml
- id: Suedbeck-2005-Brutvoegel
  title: "Methodenstandards zur Erfassung der Brutvögel Deutschlands"
  authors: ["Südbeck", "Andretzke", "Fischer", "Gedeon", "Schikore", "Schröder", "Sudfeldt"]
  publication_year: 2005
  publisher: Radolfzell
  citation: "Südbeck, P. et al. (2005): Methodenstandards zur Erfassung der Brutvögel Deutschlands. Radolfzell."
  available: false                           # whether digital copy exists locally
  canonical_path: null                       # null when not available
  ingest: false                              # methodology references typically cited, not embedded
  notes: |
    Buch; nicht frei verfügbar. Wird zitiert, nicht ingestiert.
  tags: [methodik, avifauna]
```

`ingest: false` skips from RAG pipeline (used for citation-only entries).

## Tier 1 reference list (initial v1 manifest)

The starter manifest. Author into `references-manifest.yaml` as the
first concrete instantiation.

### Federal laws (bund)
- BauGB
- BauNVO
- BNatSchG
- EEG
- BImSchG
- UVPG
- PlanZV
- ROG

### EU
- FFH-RL (92/43/EWG)
- Vogelschutz-RL (2009/147/EG)

### Mecklenburg-Vorpommern
- LPlG-MV
- LBauO-MV
- NatSchAG-MV
- KV-MV

### Leitfäden
- KNE-PV-Naturschutz (have)
- KNE-Kriterienkatalog-Naturvertraegliche-Anlagengestaltung (have)
- KNE-Kriterienkatalog-Standortsteuerung (have)
- KNE-Auswirkungen-Landschaftsbild (have)
- KNE-Folgenutzung-Acker-Gruenland (have)
- LUNG-MV-Artenschutzleitfaden (need)
- Verfahrenserlass-Bauleitplanung-MV (need)
- Brandschutzkonzept-Leitfaden-PV-Freiflaechen-MV (need; verify exists)

### Urteile
- BVerwG-9-A-3-06 (Bestandsaufnahme nach bestem wiss. Erkenntnisstand)
- BVerwG-9-A-14-07 (FFH-Habitate, Eingriffsfolgen)
- BVerwG-9-A-39-07 (CEF-Wirksamkeit, Freiberg)
- BVerwG-9-A-22-11 (§45 Nr.5 Begründungstiefe)
- EuGH-C-127-02 (Waddenzee — Erheblichkeitsbewertung)
- EuGH-C-258-11 (Sweetman — Verschlechterungsverbot)

### Methodik (cite-only)
- Suedbeck-2005-Brutvoegel
- Dietz-Kiefer-2014-Fledermaeuse

Total: ~22 ingestable + 2 cite-only.

## Update workflow

```
research-references run
  │
  ├─ For each entry:
  │    fetch → checksum → if changed:
  │       archive old (if archive_versions)
  │       write new content
  │       update last_fetched, checksum, current_amendment_form
  │       surface diff to user
  │       on approval: re-ingest into LanceDB
  │
  └─ Append to _ai-references/changelog.md with run summary
```

## changelog.md format

Lives at `<hidrive>/_ai-references/changelog.md`.

```markdown
# References changelog

## 2026-04-28 — research-references run

- BauGB: amendment date 23.10.2024 newly captured. Old version archived.
- KNE-PV-Naturschutz: unchanged.
- LUNG-MV-Artenschutzleitfaden: 404 at source URL. Investigating.
- BVerwG-9-A-22-11: unchanged.

7 entries checked, 1 changed, 1 error.

## 2026-04-15 — manual update

- Added entry: Brandschutzkonzept-Leitfaden-PV-Freiflaechen-MV.
- Initial fetch from MUGV portal.
```

Append-only. Used by validate-bausteine to know which references
just changed (and therefore which bausteine may need re-validation).
