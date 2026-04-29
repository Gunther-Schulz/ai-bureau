# references-manifest.yaml schema

Each `references-manifest.yaml` file uses the same schema regardless
of which layer (universal / domain / state) it lives in. Skills
enumerate the in-scope set via the Tier 1 MCP tool
`list_reference_manifests(scope_filter=true)`; the loader walks the
union in scope order; entries in any manifest can reference entries
in any other manifest by ID.

## Manifest layers (where each file lives)

| Layer | Path | Applies when |
|---|---|---|
| Universal | `<repo>/extensions/universal/references-manifest.yaml` | always |
| Domain | `<repo>/extensions/domain/<X>/references-manifest.yaml` | scope.domains contains X |
| State | `<repo>/extensions/state/<X>/references-manifest.yaml` | scope.states contains X |
| State-office overlay (optional) | `<state_root>/extensions/<X>/references-manifest.yaml` | when office wants regional additions on top of canonical state manifest |

## Top-level structure

```yaml
version: 1
scope: universal | domain | state
scope_key: null | <DomainName> | <StateCode>     # null when scope == universal
last_updated: 2026-04-28
maintainer: pbs-bureau

categories:
  gesetze:
    bund: [...]                              # federal laws
    eu: [...]                                # EU directives
    <state-code>: [...]                      # state laws (lowercase)
  leitfaeden: [...]                          # flat list across publishers
  urteile: [...]                             # flat list
  beispiele: [...]                           # exemplary documents
  methodik: [...]                            # methodology standards
```

The `scope` and `scope_key` top-level fields make each manifest
self-describing — the loader can warn if a state manifest is wrongly
placed at a domain path, etc.

## Entry schemas

### gesetze entry

```yaml
- id: BauGB
  title: Baugesetzbuch
  short_title: BauGB
  jurisdiction: bund                          # bund | eu | <state-code>
  source_url: https://www.gesetze-im-internet.de/baugb/
  source_type: gesetze-im-internet           # | landesrecht-mv | eur-lex | bverwg | ...
  canonical_path: gesetze/bund/BauGB.txt     # relative to <references_root>/
  fetch_method: web-text                      # web-text | web-html | web-pdf | manual | git-mirror

  last_fetched: 2026-04-28                    # null until first fetch
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

  status: active                              # active | superseded | obsolete
  superseded_by: null
  notes: ""
  tags: [bauleitplanung, federal-baugb]
```

Fields:
- `id` — stable identifier, never changes once set. Referenced from
  bausteine, citations, validations. Unique across all manifests.
- `canonical_path` — relative to `<references_root>/`.
- `fetch_method` — `web-text` (HTML scrape, plain text), `web-html`
  (preserve structure), `web-pdf` (download PDF), `manual` (Claude
  discovers canonical PDF URL on publisher site, then downloads),
  `git-mirror` (clone from a known mirror).
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
  source_url: https://www.naturschutz-energiewende.de/
  canonical_path: leitfaeden/KNE-PV-Naturschutz.pdf
  fetch_method: manual
  last_fetched: null
  checksum_sha256: null
  ingest: true
  chunking_strategy: per-section
  chunk_metadata_extractor: pdf-headings
  status: active
  notes: ""
  tags: [pv-freiflache, naturschutz, leitfaden, kne]
```

Adds `publisher`, `publication_date`, `version`. Often PDFs.

### urteile entry

```yaml
- id: BVerwG-9-A-22-13
  title: "BVerwG, Urteil vom 23.04.2014 — 9 A 22.13 (§45 Nr.5 Begründungstiefe)"
  short_title: "9 A 22.13"
  court: BVerwG                               # | OVG-MV | EuGH | ...
  docket: "9 A 22.13"
  decision_date: 2014-04-23
  jurisdiction: bund                          # bund | eu | <state-code>
  source_url: https://www.bverwg.de/...
  canonical_path: urteile/BVerwG-9-A-22-13.txt
  fetch_method: web-html
  last_fetched: null
  checksum_sha256: null
  ingest: true
  chunking_strategy: per-randnummer
  chunk_metadata_extractor: bverwg-randnummer
  status: active
  notes: |
    Wichtigste Entscheidung zur Begründungstiefe für §45 Abs.7 Nr.5
    bei privaten Vorhaben.
  tags: [§45-bnatschg, ausnahmegrund, bverwg]
```

### beispiele entry

```yaml
- id: Begruendung-Bad-Suelze-2023
  title: B-Plan Begründung <Location> (<BPlan-Type>) YYYY-MM
  source_artifact: <project>/Externe Gutachten/Begründung_Bad-Sülze_September-2023.pdf
  source_origin: external                     # external | pbs-archive
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
  available: false                            # whether digital copy exists locally
  canonical_path: null                        # null when not available
  ingest: false                               # cite-only entries skip RAG
  notes: |
    Buch; nicht frei verfügbar. Wird zitiert, nicht ingestiert.
    Cite-only entry — verify-citations validates citation FORM
    (correct author/year/title) but not claim accuracy.
  tags: [methodik, avifauna]
```

`ingest: false` marks the entry as cite-only — the manifest holds the
canonical citation form but no full text is in RAG. Used for:
- Books that aren't freely available (paywalled, unscanned).
- Methodology references that are correctly formatted but don't need
  full-text retrieval.

Cite-only is a weak guarantee: verify-citations confirms the
citation is well-formed, not that the cited text actually says what
the user claims.

## Update workflow

```
research-references run
  │
  ├─ Resolve manifest set via list_reference_manifests(scope_filter=true)
  ├─ For each manifest, for each entry:
  │    fetch → checksum → if changed:
  │       archive old (if archive_versions)
  │       write new content
  │       update last_fetched, checksum, current_amendment_form
  │       surface diff to user
  │       on approval: re-ingest into LanceDB
  │
  └─ Append to <references_root>/changelog.md with run summary
```

## changelog.md format

Lives at `<references_root>/changelog.md`.

```markdown
# References changelog

## 2026-04-28 — research-references run

Manifests in scope: universal, domain/PV-FFA, domain/Wind,
domain/Naturschutz, state/MV.

- BauGB (universal): amendment date 23.10.2024 newly captured.
  Old version archived.
- KNE-PV-Naturschutz (domain/PV-FFA): unchanged.
- LUNG-MV-Artenschutzleitfaden (state/MV): 404 at source URL.
  Investigating.
- BVerwG-9-A-22-13 (universal): unchanged.

27 entries checked across 5 manifests, 1 changed, 1 error.

## 2026-04-15 — manual update

- Added entry: Brandschutzkonzept-Leitfaden-PV-Freiflaechen-MV
  (state/MV).
- Initial fetch from MUGV portal.
```

Append-only. Used by validate-bausteine to know which references
just changed (and therefore which bausteine may need re-validation).
