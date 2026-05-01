# Vector metadata schema

Single LanceDB table `pbs_corpus` holds all embedded chunks. Source
distinction is via metadata columns, not separate tables. Filtering
across source types is one query.

## Columns

```python
class CorpusChunk:
    # Identity
    id: str                                # uuid4
    content: str                           # the chunk text (verbatim)

    # Vectors (bge-m3 produces both)
    embedding: vector[1024]                # dense
    sparse_indices: list[int]              # sparse — token IDs
    sparse_values: list[float]             # sparse — token weights

    # Source classification
    source_type: str                       # corpus | reference | baustein
    source_subtype: str                    # see "Source subtypes" below
    source_path: str                       # absolute path on disk
    source_url: str | None                 # external URL (for references)

    # Corpus-specific (source_type=corpus)
    project: str | None                    # project ID matching state.md (e.g. "23-12-Vorbeck")
    doctype: str | None                    # b-plan-begruendung | b-plan-festsetzungen | umweltbericht | ...
    section: str | None                    # section name within doc
    section_number: str | None             # numeric/structured (e.g. "5.1", "I.3.2")
    artifact_kind: str | None              # tex-source | compiled-pdf | input | snapshot | correspondence

    # References-specific (source_type=reference)
    reference_id: str | None               # manifest ID (e.g. "BauGB", "BVerwG-9-A-22-11")
    reference_category: str | None         # gesetze | leitfaeden | urteile | beispiele | methodik
    paragraph: str | None                  # § number for laws, Randnummer for urteile
    paragraph_label: str | None            # canonical short form (e.g. "BNatSchG-§45-7-5")
    jurisdiction: str | None               # bund | eu | mv | other-laender:<code>
    last_amendment: str | None             # mirrored from manifest

    # Bausteine-specific (source_type=baustein)
    baustein_name: str | None              # if this chunk is from a baustein body
    baustein_scope: str | None             # universal | domain | state | project
    baustein_scope_key: str | None         # null for universal/project; domain key (Naturschutz/PV-FFA/Wind) or state key (MV) otherwise
    baustein_status: str | None            # mirror of frontmatter status

    # Timing
    indexed_at: timestamp
    source_modified_at: timestamp

    # Free-form
    tags: list[str]                        # e.g. [solar, artenschutz, mv]
    chunk_index: int                       # position within source file (0-based)
    chunk_total: int                       # total chunks for this source file
```

## Source subtypes

| `source_type` | `source_subtype` values |
|---|---|
| `corpus` | `local-repo` (`~/dev/Planungsbüro-Schulz/`), `hidrive-project` (`<hidrive>/Projekte/<YY-NN>/`), `snapshot` (immutable snapshot inside `_ai/`), `correspondence` (`Schriftverkehr/eml/` etc.) |
| `reference` | `gesetz-bund`, `gesetz-eu`, `gesetz-mv`, `leitfaden`, `urteil`, `beispiel`, `methodik` |
| `baustein` | `universal`, `domain`, `state`, `project` |

## Filter patterns

| Goal | Filter |
|---|---|
| Search only law texts (current versions) | `source_type=="reference" AND source_subtype IN ("gesetz-bund","gesetz-eu","gesetz-mv")` |
| Search BauGB only | `source_type=="reference" AND reference_id=="BauGB"` |
| Search past Begründungen | `source_type=="corpus" AND doctype=="b-plan-begruendung"` |
| Search this project's inputs | `source_type=="corpus" AND project=="23-12-Vorbeck" AND artifact_kind=="input"` |
| Search bausteine globally | `source_type=="baustein" AND baustein_status=="active"` |
| Find rulings citing §44 BNatSchG | `source_type=="reference" AND source_subtype=="urteil" AND content CONTAINS "§ 44 BNatSchG"` |
| Recently indexed | `indexed_at > "2026-04-01"` |

LanceDB SQL-style filters on these columns; combinations work standard SQL.

## Per-project namespacing

`ingest_project_inputs(project, paths)` writes with
`source_subtype=hidrive-project` AND `project=<id>` to namespace
cleanly. `search_inputs(query, project)` injects
`filter={"project": project, "artifact_kind": "input"}` on top of
`search_corpus`.

`unbind_project` deletes chunks where `project==<id>` AND
`artifact_kind=="input"`. Bausteine and snapshots stay (audit trail).

## Hybrid search + reranker flow

```
1. user query → bge-m3 dense embedding + sparse indices/values
2. LanceDB hybrid query:
     - vector search on embedding column (top 30)
     - sparse search on sparse_indices/sparse_values (top 30)
     - merge with reciprocal rank fusion → top 30
3. apply metadata filters (source_type, project, etc.)
4. bge-reranker-v2-m3 rerank top 30 → top k (default k=10)
5. return CorpusHit objects with score + content + full metadata
```

Reranker step ~50ms on the 5090, ~500ms on CPU.

## Where each metadata field comes from at ingestion

| Field | Source |
|---|---|
| `id` | uuid4 generated |
| `content` | chunk text post chunking |
| `embedding`, `sparse_*` | bge-m3 forward pass |
| `source_type`, `source_subtype` | derived from path: regex match against known patterns (`_ai-references/...` → reference, `~/dev/Planungsbüro-Schulz/...` → corpus, `memory/.../bausteine/` → baustein) |
| `source_path` | absolute path |
| `project` | for hidrive-project: extracted from path (`Projekte/(\d\d-\d\d.*?)/...`); for local-repo: extracted from path |
| `doctype` | inferred from filename heuristic + parent folder + content sniff |
| `section` | by chunker (per-section / per-paragraph yields section name; fallback null) |
| `reference_id` | from manifest entry that mapped to this canonical_path |
| `paragraph` | by chunk_metadata_extractor (e.g. gesetze-im-internet parser pulls `§N Abs.M Nr.K`) |
| `last_amendment` | mirrored from manifest at ingestion time |
| `baustein_*` | parsed from baustein frontmatter |
| `indexed_at` | now() at ingestion |
| `source_modified_at` | os.stat(source_path).st_mtime |
| `tags` | propagated: bausteine frontmatter tags, manifest tags, project state.md tags |
| `chunk_index`, `chunk_total` | from chunker |

## Re-indexing

When a source changes (file mtime > `source_modified_at`):

1. Delete all chunks where `source_path == <changed-path>`.
2. Re-chunk + re-embed.
3. Insert new chunks with fresh `indexed_at`.

Atomic per-source: a failed re-index leaves old chunks in place. For
references, `research-references` triggers re-indexing post-fetch via
`ingest_paths(paths=[changed_paths], force=true)`.

## Deliberately NOT stored

- Full-text raw bytes (only chunk content). Source files stay on
  disk; `read_corpus_file(path)` reads from filesystem.
- ColBERT late-interaction vectors (memory cost ~5x dense; unclear
  quality gain — revisit if recall lacking).
- Per-baustein successful_uses / rejected_uses arrays (those live in
  baustein file). Baustein chunks search content, not metadata-arrays.
- Embeddings of feedback content. Feedback files searched via grep /
  direct read, not vector retrieval. (Reconsider if base grows
  beyond ~100 entries.)

## Schema versioning

Schema at `version: 1`. Field additions are backwards-compatible if
nullable. Renames or type changes require:

1. Bump schema version in `pbs_mcp/schemas.py`.
2. Migration script reads old chunks, writes to new schema.
3. Re-ingest only if change affects existing data semantically.

LanceDB allows column-add via `add_columns` for nullable fields
without re-ingesting.
