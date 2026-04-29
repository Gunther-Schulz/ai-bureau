# Pre-RAG architectural decisions

Resolves the four architectural decisions (A–D) and the three
pipeline choices (1–3) required before first ingest, per HANDOFF
"Pre-RAG architectural decisions" section. Each gets a verdict
(yes/no + reasoning).

**Status**: PROPOSED — final confirmation at task #21 (full pre-RAG
architectural audit). The verdicts here represent the design pass;
the audit gates them before code lands.

**Why this doc exists**: re-ingesting 57 entries through OCR +
DRM-removal + multimodal pipelines is expensive; deferring an
architectural choice means re-processing later. Three of the
items below (A, B, C) are architectural — their resolution shapes
the storage schema and pipeline. D is captured here for
completeness; the schema slot already landed during the alignment
sweep.

---

## A. Multimodal storage schema

**Verdict**: **YES — first ingest includes OCR + DRM removal +
page-image retrieval (ColPali). Defer table extraction.**

### A.1 What ships in first ingest

| Sub-piece | First ingest? | Reasoning |
|---|---|---|
| **OCR for scanned PDFs** (`ocrmypdf`) | YES | Older Verfahrenserlasse + archived Stellungnahmen are scanned-only. Without OCR, those entries are blank in the corpus — significant recall gap. German-language tesseract model essential. |
| **DRM removal** (`qpdf`/`pikepdf`) | YES (cheap, no-op if no DRM) | Some KNE/BfN PDFs carry owner-password DRM. `qpdf --decrypt` handles trivially. Cost of including: minimal. Cost of skipping: have to re-process when first DRM PDF surfaces. |
| **Page-image retrieval** (ColPali) | YES | KNE-Anlagengestaltung diagrams + LUNG-MV Karten + future Hendrik Kartierberichte have non-trivial visual content. Re-ingesting all 57 entries to add image embeddings later is the cost we're avoiding. ColPali is bounded effort; RTX 5090 + 32GB VRAM handles it. |
| **Table extraction** (Camelot/Tabula) | NO (defer) | Narrow value: Helgoländer species×distance is the highest-value table; isolated work. Can ingest tables as images via ColPali for now (Claude session reads them); precise structured extraction lands when first table-symbolic-query use case surfaces. |

### A.2 LanceDB storage schema

Page images stored as **filesystem references + LanceDB metadata**,
not blob fields:

```yaml
# LanceDB schema additions (multimodal):
modality: text | image            # discriminator
source_path: <path-to-pdf>
page_number: int                  # for image rows
image_path: <path-to-page-render> # filesystem reference
embedding: vector                 # text-embedding for text rows;
                                  # ColPali patch-embeddings for image rows
```

Page renders live alongside extracted text under
`<references_root>/<id>/page_images/page-<N>.png`. PNG over JPEG
for diagram clarity.

**Why filesystem reference + metadata** (over blob field):

- Faster queries (no blob deserialization in the hot path)
- Smaller LanceDB on-disk size
- Simpler backup / migration / inspection
- Path stability is acceptable: references corpus is immutable
  per `research-references` "single source of truth" principle;
  page images don't move

### A.3 New MCP tool surface

```
read_corpus_page_image(path: str, page: int) -> bytes
  Returns image bytes for the specified page of a corpus PDF.
  Used by skills + orchestrator when delivering image content
  to the Claude session for vision-LLM reading.

search_corpus(filter={modality: "image"})
  Existing search_corpus extended with modality filter. Default
  (no filter) returns hybrid (text + image candidates merged by
  reranker). Explicit filter for modality-specific search.
```

`read_corpus_file(path)` continues to return text only (existing
behavior). New `read_corpus_page_image` is dedicated to image
bytes for clarity.

### A.4 Token-budget protocol for image content blocks

Each image content block consumes context tokens proportional to
image dimensions. Need budget control.

**Verdict**: cap 5 images per response by default (configurable
per call); deduplicate images per turn; render at 2048-px max
dimension.

**Alternatives considered**:

- **Cap 3 images** (more conservative): chosen against because 3
  often forces premature truncation when an authority Stellungnahme
  spans multiple pages or a Karte requires multiple reference views;
  user friction outweighs token saving.
- **Cap 10 images** (more permissive): chosen against because
  context tokens balloon quickly (each 2048-px image ~1500 tokens);
  10 per response approaches 15K image tokens before any text.
- **Image dimension at 1024-px**: lower fidelity; insufficient
  for German Bestandskarten + diagram detail (tested mentally
  against KNE-Anlagengestaltung diagrams). 2048-px is the
  reasonable floor.
- **Image dimension at 4096-px**: better fidelity but doubles
  token cost; marginal value for most Karten.

Revisit triggers: real usage shows under-fetching (images needed
but cap hit) or over-fetching (token budget consistently strained).

### A.5 Hybrid retrieval (text + image)

**Verdict**: `search_corpus` default behavior returns hybrid
candidates:

1. Text-vector retrieval (bge-m3) returns top-K text chunks.
2. Image-vector retrieval (ColPali) returns top-K image pages.
3. Reranker (bge-reranker-v2-m3) scores both kinds against the
   query; final top-K mixed list returned.

Skills consuming `search_corpus` results check `hit.modality` to
dispatch (text → use as text; image → call
`read_corpus_page_image`).

**Alternatives considered**:

- **Modality-specific search only** (no hybrid; caller must
  request text or image separately): rejected because most
  queries don't know in advance which modality has the answer
  ("what does the KNE recommendation say about Modulreihen-
  spacing?" might be best answered by the diagram OR by the
  prose; let the reranker decide).
- **Text-first, image-fallback** (only fetch images if text
  recall is poor): rejected because the recall-poor signal is
  unreliable; better to score both kinds and let reranker
  choose.
- **Image-first, text-context** (always fetch the page image
  AND the page's text chunks): considered for diagram-heavy
  content but rejected as default — too token-expensive for
  text-answerable queries; can be added as an explicit
  `search_corpus(filter={include_page_context: true})` flag
  later if a use case surfaces.

Revisit trigger: hybrid reranking shows poor quality on real
queries (e.g. text consistently outranks an obviously-better
image hit, or vice versa).

### A.6 Implementation order

1. OCR + DRM-removal in ingest pipeline (no schema change beyond
   new chunker module)
2. ColPali embedder loaded alongside bge-m3 (lazy-load on first
   image-query)
3. LanceDB schema migration: add `modality`, `image_path`,
   `page_number` columns
4. `read_corpus_page_image` MCP tool
5. Hybrid retrieval in `search_corpus` (reranker scores both
   modalities)

---

## B. Legal §-graph extraction at ingest

**Verdict**: **YES — extract §-graph at first ingest into SQLite
alongside LanceDB.**

### B.1 Why yes

- **Avoids re-process pass**: extracting at ingest is one-time
  work; deferring means re-reading all 57 entries later
- **Available immediately**: `verify-citations`, `validate-checklist`,
  `draft-textteil-b/c` benefit from symbolic queries from day one
- **Bounded extraction risk**: laws + rulings + leitfäden have
  well-known citation patterns (regex catches 90%+); LLM
  extraction not required at ingest time
- **Simple storage**: SQLite single file alongside LanceDB

### B.2 Storage choice

**SQLite** (over Kùzu / Neo4j / dedicated graph DB):

- Single file alongside LanceDB; no extra service to run
- Fits the local-first architecture (no Docker, per ARCHITECTURE)
- Adequate for 57-entry corpus → likely <100K nodes + edges
- Standard library; no new dependency
- Trade-off: graph traversal is SQL-with-recursive-CTEs, not
  Cypher; expressivity is fine for our query patterns
- Path: `<references_root>/legal-graph.sqlite` (parallel to LanceDB)

### B.3 Schema sketch

```sql
-- Nodes: laws, paragraphs, rulings, leitfäden, methodologies
CREATE TABLE node (
    id           TEXT PRIMARY KEY,    -- e.g. "BNatSchG", "BNatSchG/§44", "BVerwG-9-A-22-11"
    type         TEXT NOT NULL,       -- law | paragraph | ruling | leitfaden | methodology
    parent_id    TEXT,                -- e.g. "BNatSchG/§44/Abs.1" -> "BNatSchG/§44"
    title        TEXT,
    current_version TEXT,             -- amendment-form for laws; decision-date for rulings
    source_path  TEXT,                -- where in corpus
    FOREIGN KEY (parent_id) REFERENCES node(id)
);

-- Edges: typed relationships between nodes
CREATE TABLE edge (
    src_id    TEXT NOT NULL,
    dst_id    TEXT NOT NULL,
    type      TEXT NOT NULL,          -- references | interprets | cites | amends | applies-to
    context   TEXT,                   -- chunk_id where the edge was extracted from
    PRIMARY KEY (src_id, dst_id, type),
    FOREIGN KEY (src_id) REFERENCES node(id),
    FOREIGN KEY (dst_id) REFERENCES node(id)
);

CREATE INDEX idx_edge_src ON edge(src_id, type);
CREATE INDEX idx_edge_dst ON edge(dst_id, type);
```

### B.4 Extraction logic (at ingest)

For each chunk being indexed into LanceDB:

1. Regex-extract citations:
   - `§\s*(\d+)\s*(Abs\.\s*\d+)?\s*(Nr\.\s*\d+)?\s*(<Gesetz>)?`
   - `Art\.\s*\d+\s*(<Gesetz>)?`
   - `<Court>-(\d+)-([A-Z]+)-(\d+)\.(\d+)` (BVerwG-9-A-22-11 etc.)
   - `EuGH\s+C-(\d+)/(\d+)`
2. Resolve to canonical node IDs (e.g. `§44 Abs.1 BNatSchG` →
   `BNatSchG/§44/Abs.1`).
3. Insert nodes (idempotent on PRIMARY KEY).
4. Insert edge from chunk's source-document node to cited node
   (type=`references` for prose mentions; `cites` for explicit
   bibliographic refs).
5. Special handling for ruling text: extract which §s the
   ruling interprets → insert edges of type `interprets`.

### B.5 New MCP tool

```
query_legal_graph(
    node_id?: str,          # e.g. "BNatSchG/§44"
    node_type?: str,        # e.g. "ruling"
    edge_type?: str,        # e.g. "interprets"
    direction?: "out"|"in", # default "out" (find what node_id points TO)
    depth?: int = 1,        # traversal depth
) -> list[GraphHit]
```

Returns matching nodes + the edges connecting them. Used by
`verify-citations` (per-iteration disambiguation step), by
`validate-checklist` (reference enrichment), and by future
agentic-retrieval skills.

### B.6 Open question (deferred)

- **§-graph maintenance on reference updates**: when
  `research-references` re-fetches an updated law, do we
  re-extract its citations? Yes — graph rows for that source
  get deleted + re-inserted on each fetch. Standard re-ingest
  pattern.

---

## C. Chunking strategy sanity-check

**Verdict**: **4 strategies sufficient for first ingest. Add one
hybrid (`per-section-with-paragraph-subchunks`) for long-section
documents. Multimodal: page-level chunking for image-RAG (independent
of text chunking — same source PDF chunked separately for text and
images).**

### C.1 Existing 4 strategies (sanity-checked, all retained)

| Strategy | Used for | Example |
|---|---|---|
| `per-paragraph` | Court rulings, prose-heavy laws | BNatSchG §44 paragraphs |
| `per-randnummer` | Court ruling text (Randnummer = decision paragraph number) | BVerwG-9-A-22-11 Rn.32 |
| `per-section` | Leitfäden chapters | KNE-Anlagengestaltung §3 |
| `per-article` | Federal/state laws (Artikel) | BauGB Artikel 1 |

### C.2 New addition

| Strategy | Used for | Why |
|---|---|---|
| `per-section-with-paragraph-subchunks` | Long Leitfaden sections (e.g. KNE-Anlagengestaltung's full ColPali-relevant chapter) | Avoids over-large single chunks; preserves section coherence as parent context while sub-chunks improve retrieval precision |

Implementation: parent chunk is the full section; child sub-chunks
are paragraphs within. Both indexed; both searchable. Reranker
handles preference between section-level + paragraph-level hits.

### C.3 Multimodal chunking

Same source PDF chunked **twice**, one pipeline per modality:

- **Text pipeline**: applies the chunking strategy declared in
  the manifest entry (`per-section`, `per-paragraph`, etc.).
- **Image pipeline**: chunked at **page level** — each page is
  one chunk for ColPali. Independent of text chunking.

Chunks from both pipelines land in LanceDB with `modality`
discriminator; query-time retrieval merges hits per A.5.

### C.4 What did NOT need adding

- Sentence-level chunking: too granular; leads to over-fragmented
  context. Skipped.
- Document-level (whole-doc) chunking: too coarse; defeats
  retrieval purpose. Skipped.
- Sliding-window: not needed given the four strategies cover
  natural document boundaries.

---

## D. Reference versioning fields in baustein frontmatter

**Verdict**: **DONE during alignment sweep.** Schema slot reserved
in `save-baustein/references/format.md` (commit `502f339`):

```yaml
references:
  - {law: BNatSchG, paragraph: §45 Abs.7 Nr.5, verified_against_version: "i.d.F. 23.10.2024"}
```

`verified_against_version` is optional but recommended. It allows
`verify-citations` (also aligned during the sweep) to detect when
the cited law has amended since last validation — even if the
cited paragraph text still matches.

Versioning lifecycle logic (re-validation flow, archive of old
verified-against versions, comparison against manifest's
`current_amendment_form`) lands as v2 ROADMAP work. The schema
slot now is forward-compatible.

---

## Pipeline choices (1–3)

These are not architectural — they're model / placement choices.
Verdicts captured for completeness; can be revised post-first-run
if benchmarks show issues.

### 1. Text-retrieval baseline

**Verdict**: **bge-m3 + cross-encoder reranker (bge-reranker-v2-m3)
for first ingest.** Already pinned in `pyproject.toml`.

ColBERT-v2 is a ROADMAP item conditional on first-run
sample-searches showing quality issues with bge-m3 on German legal
text. Don't preempt; the conditional adoption path is documented
in ROADMAP "Late-interaction retrieval (ColBERT-v2)".

### 2. Query rewriting placement

**Verdict**: **Defer query rewriting in initial pipeline.**

- No HyDE in first ingest.
- No query decomposition in first ingest.
- No query expansion in first ingest.

Add HyDE selectively when first concrete value surfaces:

- **save-baustein dedupe** is the natural first HyDE consumer
  (paraphrase-search to catch near-duplicate bausteine before
  they're written). Per ROADMAP "Query rewriting" item +
  save-baustein priority touchpoint.

Decomposition + expansion: add when concrete drafting need
surfaces (e.g. multi-§-claim drafting needs decomposed retrieval).

### 3. Reranker model choice

**Verdict**: **bge-reranker-v2-m3 for first ingest.** Already
pinned in `pyproject.toml`.

Switch to jina-reranker-multilingual if German legal text shows
poor reranking quality during first-run sample-searches.

---

## Implementation order (post-decisions; pre-RAG kickoff)

Once these verdicts are confirmed at task #21 audit, implementation
falls into three steps:

1. **Backend pipeline additions** (per A + B + C):
   - OCR + DRM-removal modules in ingest
   - ColPali embedder + image-render pipeline
   - LanceDB schema migration: `modality`, `image_path`,
     `page_number` columns
   - SQLite `legal-graph.sqlite` initialization + extraction
     hooks in chunkers
   - Hybrid retrieval in `search_corpus`
   - New MCP tools: `read_corpus_page_image`, `query_legal_graph`
   - New chunking strategy: `per-section-with-paragraph-subchunks`

2. **Smoke-test on a few entries** (3–5 entries spanning text-only,
   diagram-heavy, scanned, DRM-encumbered):
   - Verify OCR works on scanned PDF
   - Verify DRM-removal works on DRM-encumbered PDF
   - Verify ColPali image embeddings + filesystem refs
   - Verify §-graph extraction populates SQLite as expected
   - Verify hybrid retrieval returns mixed candidates

3. **Full first ingest** (all 57 entries via `research-references`
   refresh-all):
   - Tracked in changelog
   - Bausteine flagged downstream via `find_bausteine_by_reference`
     (none yet exist; this becomes relevant on second run)

---

## Open work captured for follow-up

These are NOT pre-RAG decisions but surfaced during this design
pass; tracked here for traceability.

- **§-graph maintenance on reference updates**: documented in
  B.6; standard re-ingest pattern.
- **Image render dimensions**: 2048-px max chosen for first
  ingest; revisit if Claude vision struggles on detail-heavy
  diagrams.
- **Token-budget cap**: 5 images per response default; revisit
  if real usage shows under- or over-shooting.
- **Hybrid retrieval ranking**: reranker scores text + image
  candidates against same query; quality assumption to be
  validated empirically.
- **Schema for query_legal_graph results**: GraphHit shape not
  yet defined; lands when the MCP tool is implemented.

---

## Connection to ROADMAP

These decisions resolve / shape several ROADMAP items:

- **Multimodal RAG** — A's verdict shapes which sub-pieces ship.
  Table extraction explicitly deferred per A.1.
- **Structural retrieval (§-graph + project graph + verfahren
  state-machine)** — B's verdict commits to the legal §-graph
  at first ingest. Project graph + verfahren state-machine
  remain ROADMAP items (not pre-RAG).
- **Late-interaction retrieval (ColBERT-v2)** — pipeline choice
  1 confirms baseline; ColBERT only if quality issues observed.
- **Query rewriting (HyDE etc.)** — pipeline choice 2 defers;
  HyDE for save-baustein dedupe is the named first consumer.

---

## Verdicts summary (single-pane)

| ID | Topic | Verdict |
|---|---|---|
| A | Multimodal storage | YES first ingest: OCR + DRM + ColPali; defer table extraction. Filesystem ref + LanceDB metadata. New tool `read_corpus_page_image`. Cap 5 imgs/response. Hybrid retrieval. |
| B | Legal §-graph at ingest | YES; SQLite alongside LanceDB; nodes + typed edges; regex extraction at chunk-time. New tool `query_legal_graph`. |
| C | Chunking strategies | 4 existing sufficient; add `per-section-with-paragraph-subchunks` hybrid. Multimodal: page-level for image-RAG (independent of text chunking). |
| D | Baustein reference versioning | Done in alignment sweep (`verified_against_version` slot). |
| 1 | Text-retrieval baseline | bge-m3 + bge-reranker-v2-m3. ColBERT conditional. |
| 2 | Query rewriting | Defer; HyDE for save-baustein dedupe is first consumer when added. |
| 3 | Reranker model | bge-reranker-v2-m3 baseline. |

**Final confirmation**: at task #21 audit gate.
