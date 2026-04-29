# Pre-RAG architectural decisions

Resolves the four architectural decisions (A–D) and the three
pipeline choices (1–3) required before first ingest, per HANDOFF
"Pre-RAG architectural decisions" section. Each gets a verdict
(yes/no + reasoning).

**Status**: **ACCEPTED** (session 5, 2026-04-29). Pre-RAG architectural
audit (`docs/audit-pre-rag.md`) closed conditional-pass; F-batch
drift (commit `ad01b18`), U1 decision-recording backfill (`d0f3f91`),
U2 backend conventions (`501eaa1`) all landed. RAG kickoff per
implementation order below is unblocked.

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

**Alternatives considered**:

- **Defer all multimodal sub-pieces until first concrete need**:
  rejected — re-ingesting 57 entries to add OCR/DRM/ColPali later
  re-pays the OCR + ColPali compute cost, plus risk that early
  bausteine cite text only available post-OCR. RTX 5090 capacity
  is in surplus; cheaper now than retrofit.
- **OCR everything indiscriminately** (including text-PDFs):
  rejected — most KNE/BfN PDFs already carry extractable text;
  OCR'ing them adds noise (OCR errors degrade text retrieval).
  Ingest pipeline branches on PDF text-availability heuristic.
- **Include table extraction in first ingest**: rejected — narrow
  value, high per-PDF tuning cost (Camelot/Tabula), ColPali handles
  visual representation adequately for Claude-session reading.

**Revisit trigger**: first-run sample-search shows scanned PDFs
missing from results despite OCR (OCR-quality issue); OR a
table-symbolic-query use case surfaces (revisit table extraction);
OR re-ingest cost proves cheap enough to add deferred sub-pieces
in batch.

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

**Alternatives considered**:

- **Blob field in LanceDB**: rejected — slows hot-path queries,
  bloats on-disk size, complicates backup/inspection.
- **External object store** (S3/MinIO): rejected — fights
  local-first / no-Docker stance for a 57-entry corpus.
- **JPEG over PNG**: rejected — diagram clarity matters for
  Bestandskarten + Anlagengestaltung detail; PNG size cost
  negligible at this corpus scale.

**Revisit trigger**: corpus grows past ~1000 PDFs (filesystem-ref
scaling friction); OR backup/sync friction suggests blobs would
be easier to manage; OR JPEG fidelity proves sufficient on
real-usage patterns.

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

**Alternatives considered**:

- **Extend `read_corpus_file` to return image bytes** (single
  tool, modality discrimination by file-type): rejected — clarity
  matters more than tool-count parsimony; image return is a
  different return type.
- **Inline image bytes in `search_corpus` results**: rejected —
  bloats search payload, forces every caller to handle bytes.
  Two-step (search returns hit+path; caller fetches bytes) is the
  right pattern for token-budgeted image blocks.

**Revisit trigger**: a skill consistently needs both text and
image bytes from the same call (bundling would pay off); OR the
path-then-fetch pattern proves a friction point in real use.

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

Sequencing for verdict A's sub-pieces is now part of the unified
phased plan — see "Implementation order" section near the bottom
of this doc. Phase 3a covers all five A-sub-pieces (OCR, DRM,
ColPali, schema migration, hybrid). This section retained as a
back-pointer.

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

**Alternatives considered**:

- **§-graph at runtime** (extract on-demand from chunks at
  query-time): rejected — repeats extraction cost per query, adds
  runtime latency, loses ingest-time global view (transitive
  citation chains can't be precomputed).
- **Defer §-graph entirely** until first concrete need: rejected
  — citation-aware skills (`verify-citations`, `validate-checklist`,
  `draft-textteil-b/c`) are exactly the day-1 consumers; running
  without graph means falling back to grep-the-corpus.
- **LLM-extracted §-graph at ingest** (Claude session emits
  citation edges): rejected — bounded extraction risk is low;
  regex catches 90%+ of well-formed citations; LLM cost not
  justified for the 10% edge cases.

**Revisit trigger**: regex extraction shows <80% citation recall
on real corpus (LLM extraction needed for the long tail); OR
query patterns reveal symbolic-query use cases not anticipated
(drives schema additions).

### B.2 Storage choice

**SQLite** (over Kùzu / Neo4j / dedicated graph DB):

- Single file alongside LanceDB; no extra service to run
- Fits the local-first architecture (no Docker, per ARCHITECTURE)
- Adequate for 57-entry corpus → likely <100K nodes + edges
- Standard library; no new dependency
- Trade-off: graph traversal is SQL-with-recursive-CTEs, not
  Cypher; expressivity is fine for our query patterns
- Path: `<references_root>/legal-graph.sqlite` (parallel to LanceDB)

**Alternatives considered**:

- **Kùzu** (embedded graph DB): rejected — Cypher is genuinely
  better for some traversal queries, but the 57-entry corpus
  doesn't justify a new dependency; SQLite recursive-CTEs handle
  the queries we actually need.
- **Neo4j**: rejected — full server, fights local-first /
  no-Docker stance.
- **NetworkX-on-disk** (Python in-process graph): rejected — not
  durable across sessions, weaker query expressivity than SQL
  recursive-CTE.
- **Graph rows in LanceDB** (reuse existing vector store):
  rejected — LanceDB is optimized for vector queries, not graph
  traversals; mixing concerns degrades both.

**Revisit trigger**: corpus grows past ~10K nodes/edges and
recursive-CTE queries become slow (>100ms for typical traversals);
OR a query pattern emerges that needs Cypher-like path expressions
awkward to write in SQL.

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

**Alternatives considered**:

- **LLM extraction at ingest** (Claude reads each chunk and emits
  edges): rejected as default — see B.1. Reserved as fallback if
  regex recall proves inadequate.
- **Spacy-NLP + custom rules**: rejected — heavy dependency for
  marginal gain over regex on well-formed German legal citations.
- **No edge typing** (treat all citations as undifferentiated
  `references` edges): rejected — the `references` vs `interprets`
  vs `cites` distinction is what makes graph queries useful.

**Revisit trigger**: regex recall measurably bad (<80%) on real
corpus AND missing citations are the load-bearing kind for skill
behavior; OR a citation form not covered by current regex (BVerwG
vs OLG vs OVG patterns differ) appears repeatedly.

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

### C.4 What did NOT need adding (alternatives considered)

- **Sentence-level chunking**: too granular; over-fragmented
  context. Skipped.
- **Document-level (whole-doc) chunking**: too coarse; defeats
  retrieval purpose. Skipped.
- **Sliding-window**: not needed given the four existing strategies
  cover natural document boundaries.
- **Extend `per-section` to handle long sections in-place** (split
  internally without parent/child structure): rejected for C.2 —
  loses the section-level coherent context that reranker can prefer
  when the answer spans paragraphs.
- **Single shared text+image chunking** (one chunk per page,
  text+image together): rejected for C.3 — text retrieval benefits
  from finer-grained chunks (paragraph/section); image retrieval
  needs page-level. Forcing one shared granularity degrades both.

**Revisit trigger** (across C): retrieval quality on first-run
sample searches reveals a chunk-size mismatch (e.g. answers
consistently span chunk boundaries — split too small; OR retrieved
chunks consistently too noisy — split too large); OR a
ruling/Leitfaden form emerges that doesn't match the existing four
patterns (suggests a new strategy is warranted).

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

**Alternatives considered**:

- **No version field on bausteine** (rely on manifest
  `current_amendment_form` alone): rejected — bausteine outlive
  individual law amendments; without per-baustein version capture,
  every law update would require re-validating every dependent
  baustein from scratch instead of comparing-and-skipping.
- **Hash-based versioning** (SHA of cited text): rejected — too
  brittle (whitespace/format changes invalidate); the
  amendment-form string is the human-meaningful version identifier
  that the law publishes itself.
- **Required (not optional) field**: rejected — would block early
  baustein capture before `verify-citations` has run; optional
  with strong recommendation lets the field populate as bausteine
  pass through verification.

**Revisit trigger**: first reference refresh shows the field is
unpopulated on >50% of saved bausteine (suggests strong
recommendation isn't enough — needs save-time gate); OR cited-text
hash diffs prove more useful than amendment-form strings for
detecting drift.

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

**Alternatives considered**:

- **ColBERT-v2 from day 1**: rejected for now — late-interaction
  models are heavier (per-token storage, per-query compute) and
  bge-m3 is the proven multilingual baseline. Adopt conditionally.
- **OpenAI text-embedding-3-large**: rejected — fights local-first
  (external API dependency, ongoing per-query cost), and the
  multilingual quality gap vs bge-m3 doesn't justify the trade-off
  for German legal text.
- **No reranker** (single-stage retrieval): rejected — first-stage
  retrieval recall is reliable but precision benefits significantly
  from reranking on well-formed German legal text.

**Revisit trigger**: first-run sample searches show <70% relevance
on top-5 reranked hits for typical legal queries (suggests model
upgrade); OR ColBERT-v2 publishes a German-trained variant that
materially outperforms bge-m3 on planning-domain corpora.

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

**Alternatives considered**:

- **HyDE in first ingest as a default**: rejected — adds latency
  + cost to every query without proven recall gain on German legal
  text; defer until a use case (save-baustein dedupe) makes the
  cost justifiable.
- **Query decomposition by default**: rejected — most retrieval
  queries in current skills are well-formed single-claim queries;
  decomposition is overhead for the common case.
- **Query expansion via synonym lookup**: rejected — German legal
  vocabulary is precise (`Eingriff` ≠ `Beeinträchtigung` ≠
  `Auswirkung`); naive synonym expansion injects noise.

**Revisit trigger**: save-baustein dedupe shows poor near-duplicate
detection (HyDE's first concrete consumer); OR multi-§-claim
drafting workflow surfaces and decomposed retrieval is the natural
fit; OR observed retrieval failures cluster on
vocabulary-mismatch (suggests targeted expansion).

### 3. Reranker model choice

**Verdict**: **bge-reranker-v2-m3 for first ingest.** Already
pinned in `pyproject.toml`.

Switch to jina-reranker-multilingual if German legal text shows
poor reranking quality during first-run sample-searches.

**Alternatives considered**:

- **jina-reranker-multilingual**: viable alternative, kept on the
  shelf. Comparable quality on multilingual benchmarks; not
  preempted only because bge-reranker-v2-m3 pairs naturally with
  bge-m3 retriever (same model family, consistent training data).
- **Cohere Rerank** (API-based): rejected — fights local-first and
  adds per-query cost.
- **No reranker, rely on retrieval scores**: rejected — see
  pipeline choice 1; reranking is the precision lift.

**Revisit trigger**: first-run sample searches show poor reranking
on German planning-law queries (top-1 not the right answer when
it should be); OR jina publishes a German-tuned variant with
materially better benchmarks.

---

## Implementation order (post-decisions; pre-RAG kickoff)

**Phasing revised in session 5** based on the following reasoning:
the previous flat "Backend pipeline additions" lumped 7 distinct
concerns (OCR/DRM, ColPali, LanceDB schema, §-graph, hybrid
retrieval, 2 new tools, new chunking) into one PR — too coarse.
Real corpus shape (which entries are scanned/DRM/manual-discovery)
should inform chunker decisions rather than be discovered after
implementation. Phases below split text and image sides; download
the corpus early so design iterates against real data.

### Phase 0 — Pre-RAG plumbing (current)

Discussion + small implementation. No corpus contact.

- Meta-audit slice (close remaining drift not caught in
  audit-pre-rag.md)
- `docs/plugin-conventions.md` (Type A/B idioms — sibling to
  backend-conventions.md)
- Integration registry design + implementation (4th layered
  manifest type? capability vocabulary? query API shape?)
- Testing-methodology design (`docs/rag-testing-strategy.md`):
  coverage-gap schema, ground-truth set scope, determinism
  harness, regression detection
- U2 conventions migration (tests/, ToolError, ruff `G` rule) —
  bundled with registry impl

**Gate**: Phase 0 closes when registry is queryable + harness
shape is documented + ground-truth set scoped (curation deferred
to Phase 1).

### Phase 1 — Corpus download (no embeddings)

Fetch all 57 entries via `research-references` full refresh.
Raw fetch + checksum + manifest population only. No chunking,
no embedding, no LanceDB writes.

**Why early**: surfaces real data shape before design commits.
Discovers DRM/scanned/manual-discovery surprises now, not after
the chunker/embedder code already assumes a shape.

**Output**: `<references_root>/` populated with raw text/PDFs
+ `changelog.md` populated + per-entry coverage scaffold (see
Phase 0 testing-strategy doc).

**Gate**: all 57 manifest entries either fetched-successfully
or flagged-with-reason. Coverage scaffold reflects reality.

### Phase 2a — Text-side ingestion (smoke)

Implement: bge-m3 embedder + reranker (already pinned), new
chunking strategy `per-section-with-paragraph-subchunks`,
SQLite `legal-graph.sqlite` initialization + regex extraction
hooks, hybrid retrieval in `search_corpus` (text-only —
image-modality not yet present).

Smoke-test on **5 text-heavy entries** (e.g. BNatSchG,
BauGB, KNE-Anlagengestaltung-text-only-section, a Leitfaden,
a court ruling).

**Gate**: ground-truth set sample search ≥ threshold
(threshold defined in Phase 0 testing-strategy); coverage
report shows text+graph indexed for the 5 entries.

### Phase 2b — Full text ingestion of corpus

Run full text ingestion across all 57 entries.

**Gate**: coverage dashboard shows text+graph indexed for
all eligible entries; ground-truth-set queries pass against
the full text-only corpus.

### Phase 3a — Image-side ingestion (smoke)

Implement: OCR (`ocrmypdf`) + DRM-removal (`qpdf`/`pikepdf`)
modules in ingest, ColPali embedder + page-render pipeline,
LanceDB schema migration (`modality`, `image_path`,
`page_number`), `read_corpus_page_image` MCP tool, full
hybrid retrieval (text + image candidates merged by
reranker).

Smoke-test on **3 image-heavy + 1 scanned + 1 DRM-encumbered
entry**.

**Gate**: image retrieval verified; hybrid reranker correctly
mixes text + image candidates on test queries; coverage
dashboard shows images+text indexed for the 5 entries.

### Phase 3b — Full image ingestion + verified hybrid

Run full image ingestion (re-process the corpus to add image
modality). Coverage delta visible: which entries now have
images indexed vs. text-only.

**Gate**: full hybrid retrieval verified against ground-truth
set (now including image-required queries).

### Phase 4 — First project bind + real workflow

Bind first hidrive project. Run survey-project →
draft-textteil-b/c → review-draft → save-baustein →
verify-citations → record-feedback. End-to-end exercise.

**Gate**: workflow produces defensible output; bausteine begin
to populate; orchestrator's watch-list semantics tested.

---

## Open work captured for follow-up

Items not resolvable at design-time; surface in implementation
phases.

- **Schema for `query_legal_graph` results**: `GraphHit` Pydantic
  shape lands when the MCP tool is implemented in Phase 2a (text
  + §-graph). Until then, the tool surface in B.5 is a sketch.
- **§-graph maintenance on reference updates** is documented in
  B.6 (standard re-ingest pattern). Listed here to keep the
  traceability link visible — no separate work.

(Earlier per-decision items — image render dimensions, token-budget
cap, hybrid retrieval ranking — are now captured as **Revisit
trigger** entries in their respective sections per the
decision-recording convention.)

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

**Status**: ACCEPTED at task #21 audit gate (session 5).
