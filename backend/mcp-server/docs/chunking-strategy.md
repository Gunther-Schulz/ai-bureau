# Chunking strategy

Each source type has an optimal chunk granularity. The wrong
granularity destroys recall (chunks too big = embedding washes out
specifics; too small = chunks lose context). This file specifies
per-type strategy, registered chunker functions, and the metadata
each chunker emits.

## Hard constraints (apply to all chunkers)

- **Max chunk size:** 1000 tokens (counted by bge-m3 tokenizer).
  Chunks above split at the nearest sentence boundary.
- **Min chunk size:** 50 tokens. Smaller chunks merged with their
  neighbor (forward preference, then backward).
- **Overlap:** 0 tokens by default. Per-section chunkers may set
  per-strategy overlap. Overlap is ONLY useful when cut points are
  arbitrary; for structured cuts (per § / per heading), overlap is
  harmful.

## Strategy table

| Source type | Strategy | Chunker function |
|---|---|---|
| Federal law (BauGB, BNatSchG, ...) | per-paragraph | `chunk_gesetz_paragraph` |
| EU directives (FFH-RL, ...) | per-article | `chunk_eu_article` |
| State laws (LPlG-MV, LBauO-MV, ...) | per-paragraph | `chunk_gesetz_paragraph` |
| Court rulings (BVerwG, EuGH) | per-randnummer | `chunk_urteil_randnr` |
| Leitfäden (PDF) | per-section (`##` after PDF→text) | `chunk_pdf_heading` |
| Past Begründungen (`Textbausteine/*.tex`) | per-Textbaustein file | `chunk_latex_textbaustein` |
| Past Festsetzungen (`Textteil-B-B-Plan.tex`) | per-numbered-rule | `chunk_latex_enumerate` |
| Umweltbericht (`Kapitel/Schutzgut_*_UB.tex`) | per-Schutzgut-section | `chunk_latex_kapitel` |
| Email (`*.eml`) | per-message | `chunk_eml` |
| Stellungnahmen (PDF) | per-numbered-comment, fallback page | `chunk_stellungnahme` |
| Drone scans, raw PDFs | sliding window 1024/128 | `chunk_pdf_window` |
| Generic text | sliding window | `chunk_text_window` |
| Bausteine (markdown) | whole-body | `chunk_baustein_body` |

## Per-strategy details

### `chunk_gesetz_paragraph` — federal/state laws

Cut points: at each `§ N` header. Chunk = one full §, including title
and all Absätze (1), (2), … If a single § exceeds 1000 tokens,
secondary cuts at Absatz boundaries.

Metadata per chunk:
- `paragraph`: full canonical form (e.g. `§45 Abs.7 BNatSchG`)
- `paragraph_label`: short slug (e.g. `BNatSchG-§45-7`)
- `section`: § title text
- `chunk_index`: ordinal within document
- `tags`: parsed from § title where useful

Notes:
- Cross-references like "Vorbehaltlich §47 Abs.2 …" stay in chunk;
  the linked §47 is a different chunk.
- Heading-only chunks ("Erster Abschnitt — Allgemeines") are NOT
  emitted (no embeddable content).
- Repealed paragraphs (`§N — weggefallen`) emit a stub chunk so that
  references like "vgl. §20" resolve cleanly.

### `chunk_eu_article` — EU directives

Same as gesetz-paragraph but cut points are `Artikel N` headers and
chunks are per-Article. Recital sections get their own per-recital
chunks.

### `chunk_urteil_randnr` — court rulings

Cut points: each Randnummer (`Rn. N`). Chunk = one Rn block. Leitsatz
and Tenor sections at the start each become their own chunk.

Metadata:
- `paragraph`: e.g. `Rn. 47`, `Leitsatz 1`, `Tenor`
- `paragraph_label`: e.g. `BVerwG-9-A-22-11-Rn-47`
- `section`: parent section name (Tatbestand, Entscheidungsgründe)
- `tags`: derived from manifest tags + content

EuGH judgments use Rn. similarly. National rulings without Randnummer
fall back to per-section.

### `chunk_pdf_heading` — leitfäden (PDF)

Pre-pipeline: PDF → markdown via `pymupdf4llm` or `marker-pdf`.

Cut points: each `##` heading. Multi-paragraph sections become one
chunk; chunks above 1000 tokens split at next `###` or paragraph break.

Metadata:
- `section`: `##` heading text
- `section_number`: PDF section number if present
- `chunk_index`, `chunk_total`

### `chunk_latex_textbaustein` — past Begründungen

Per-file chunking: each `Textbausteine/<Section>.tex` becomes one
chunk. The file IS the section.

Pre-processing: strip LaTeX commands that aren't semantic content
(`\input{...}` etc.), keep `\textbf`, `\glqq...\grqq`, `\cite{...}`.

Metadata:
- `doctype`: `b-plan-begruendung`
- `section`: derived from filename
- `project`: from path
- `artifact_kind`: `tex-source`

If a Textbaustein exceeds 1000 tokens (rare), split at `\section{...}`
or paragraph break.

### `chunk_latex_enumerate` — past Festsetzungen

The Festsetzungen-master is one big `enumerate` of rules: 1., 2., …
nested with 1.1., 1.2.

Cut points: each top-level `\item` of the outer `enumerate`. Chunk
includes the item's own text + all nested sub-items.

Metadata:
- `doctype`: `b-plan-festsetzungen`
- `section`: rule number + first-line summary
- `section_number`: e.g. `1`, `2`, `3`
- `tags`: derived from rule type (e.g. `[bauliche-nutzung, §9-baugb]`)

The Verfahrensvermerke section is chunked separately per-Vermerk.

### `chunk_latex_kapitel` — Umweltbericht modules

Per-file: each `Schutzgut_<Name>_UB.tex` and
`Schutzgut_<Name>_Mas_UB.tex` becomes one chunk.

Metadata:
- `doctype`: `umweltbericht`
- `section`: e.g. `Schutzgut Boden — Bestandsaufnahme` or `… —
  Maßnahmen`
- `tags`: derived

### `chunk_eml` — email correspondence

One chunk per message. Pre-process: parse RFC822, extract `From`,
`To`, `Date`, `Subject`, body. Drop attachments (referenced via
metadata `tags: [has-attachment]`); MIME-decode body.

Metadata:
- `source_subtype`: `correspondence`
- `section`: subject line
- `project`: from path (Schriftverkehr is per-project)
- `tags`: `[mail-in]` or `[mail-out]`; `[has-attachment]` if applicable

Chunk = `Subject\nFrom\nTo\nDate\n\nBody`. Headers included so search
on "what did Ratschker say" returns chunks where his name appears.

### `chunk_stellungnahme` — incoming Stellungnahmen (PDF)

Stellungnahmen often have numbered points (1., 1.1, 1.2 …) or section
headings. Chunker tries:

1. Detect numbered structure → cut at top-level numbers.
2. If no clear numbering → fall back to per-page `chunk_pdf_window`.

Metadata:
- `source_subtype`: `correspondence`
- `artifact_kind`: `input`
- `paragraph`: numbered point if present
- `tags`: parsed authority from filename (e.g. `[UNB,
  behoerde-stellungnahme]`)

### `chunk_pdf_window` — generic PDF (drone scans, raw inputs)

Sliding window after PDF→text:
- Window: 1024 tokens.
- Overlap: 128 tokens (helpful here because cut points arbitrary).

Metadata:
- `section`: null (no semantic section)
- `chunk_index`, `chunk_total`

### `chunk_text_window` — generic text fallback

Same as `chunk_pdf_window` but no PDF-extraction step. Last-resort
fallback when no specific chunker matches.

### `chunk_baustein_body` — bausteine (markdown)

Whole-body chunking: each baustein = one chunk = body (post-frontmatter).
If body >1000 tokens (rare), split at `##` headings.

Metadata:
- `source_type`: `baustein`
- `source_subtype`: scope (`universal` | `domain` | `state` | `project`)
- `baustein_name`, `baustein_scope`, `baustein_scope_key`, `baustein_status`: from frontmatter
- `tags`: from frontmatter

Frontmatter NOT embedded (metadata only). Body content is what the
embedder sees.

## Chunker selection (dispatch logic)

```python
def select_chunker(path: str, manifest_entry: dict | None) -> Chunker:
    # Manifest-driven: explicit chunking_strategy override
    if manifest_entry and "chunking_strategy" in manifest_entry:
        return CHUNKERS[manifest_entry["chunking_strategy"]]

    # Path-based heuristics:
    if "_ai-references/gesetze/" in path:
        return chunk_gesetz_paragraph
    if "_ai-references/urteile/" in path:
        return chunk_urteil_randnr
    if "_ai-references/leitfaeden/" in path:
        return chunk_pdf_heading
    if "Textbausteine/" in path and path.endswith(".tex"):
        return chunk_latex_textbaustein
    if path.endswith("Textteil-B-B-Plan.tex"):
        return chunk_latex_enumerate
    if "Kapitel_UB/" in path or "Umweltbericht/Kapitel/" in path:
        return chunk_latex_kapitel
    if "Schriftverkehr/eml/" in path or path.endswith(".eml"):
        return chunk_eml
    if "stellungnahmen/" in path and path.endswith(".pdf"):
        return chunk_stellungnahme
    if "memory/" in path and "bausteine" in path:
        return chunk_baustein_body
    if path.endswith(".pdf"):
        return chunk_pdf_window
    return chunk_text_window
```

## Quality variation

- Per-paragraph (laws): excellent. Cut aligns with how questions are
  asked.
- Per-randnummer (urteile): excellent. Each Rn is a complete legal
  argument.
- Per-section (leitfäden): good. PDF-heading detection is the weakest
  link; section boundaries can be missed.
- Per-Textbaustein (Begründungen): excellent. Each file is one
  semantic section.
- Per-rule (Festsetzungen): good. Some rules with deep nesting may
  need a 2nd-level cut.
- Per-message (email): excellent. One coherent thought per chunk.
- Sliding-window fallbacks: mediocre but bounded. Reranker recovers
  most of the loss.

When recall is bad on a specific source type, the fix is usually
**switching chunker**, not tuning embedding.
