---
name: verify-citations
description: This skill should be used to cross-check legal citations (laws, paragraphs, court rulings, leitfäden) in a document or baustein against the current reference index. Triggered by phrases like "verify citations", "Zitate prüfen", "are citations current", "check §-references", as part of layered review (Layer 2 fachlich + Layer 3 formal), at compile-time validation, or after a reference update by research-references.
version: 0.1.0
license: MIT
---

# verify-citations

Specialist skill for citation freshness — detects when cited legal
forms in a document or baustein no longer match current reference
text. Source-grounding guard against citation rot.

## Load this now

Resolve the references in scope:
- `<repo>/references-manifest.yaml` — for IDs and current amendment
  forms.
- `<hidrive>/_ai-references/` — for actual reference text (loaded
  on-demand via search_corpus).

If the manifest or `_ai-references/` is missing, the skill cannot
validate against authoritative sources — fall back to "no current
reference index; cannot verify; recommend running research-references
first." Don't fabricate verdicts.

## When invoked

Three modes:

- **Document review** — scan a document for citations, verify each.
  Triggered at Layer 2 (fachlich) and Layer 3 (formal) of layered
  review.
- **Baustein freshness check** — verify a single baustein's
  `references[]` field. Triggered by `validate-bausteine` skill.
- **Targeted verify** — user asks "is BauGB §44 still current".
  Single-citation lookup.

Inputs:
- **Target** — document path OR baustein name OR explicit citation.

## Behavior

1. **Extract citations** from target:
   - For documents: regex-extract all `§ X <Gesetz>`, `§N Abs.M`,
     `Art. Y`, `BVerwG <docket>`, `EuGH C-...` patterns. Build list
     with file:line.
   - For bausteine: read `references[]` from frontmatter directly.

2. **For each citation, query reference index**:
   - `search_corpus(query=<citation>, filter={source_type:reference,
     reference_id:<law_id>})` to find matching reference text.
   - Extract the current `cited_form` from the manifest or from the
     reference document's first lines.

3. **Compare cited form**:
   - Document/baustein cited_form (e.g. "BNatSchG zuletzt geändert
     durch Art. 1 vom 08.12.2022")
   - Current cited_form (from manifest: "Art. 48 vom 23.10.2024")
   - If different → flag drift.

4. **Build finding list**:
   - `citation-drift` — cited form differs from current. Provide
     both forms.
   - `citation-not-found` — referenced law/paragraph/ruling has no
     entry in references-manifest.yaml. Suggest adding to manifest.
   - `cited-text-paraphrased` — cited verbatim quote no longer
     appears in source (law was reworded). Surface for review.
   - `cited-paragraph-removed` — referenced paragraph was repealed.
     Critical finding.

5. **For document targets**, return findings inline with line
   numbers. For baustein targets, surface as candidate flag (set
   `status: flagged`, `flagged_reason: "citation drift detected"`)
   only after user confirms.

## Output

```
Citations in B-Plan Begründung.tex:

  L143: § 44 BNatSchG — current ✓
  L201: BVerwG 9 A 22.11 — current ✓
  L267: BNatSchG i.d.F. ... 08.12.2022 — DRIFT
        Current: i.d.F. ... 23.10.2024
        Update? Suggested edit: lines 267-268.
  L412: BauGB § 13b — NOT FOUND in references-manifest
        (was added in 2024 reintroduction; not yet ingested)
        Run research-references to fetch.
```

## Edge cases

- **Citation in baustein contradicts citation in current document**:
  surface as inter-source drift. Both may need updating.
- **Citation references something not in our manifest** (e.g. obscure
  Bundesländer law): surface as "out-of-scope reference; cannot
  verify". Suggest user add to manifest if relevant.
- **Cited form is a paraphrase, not verbatim**: harder to detect.
  Check anyway via fuzzy match. If text is far from any current
  paragraph but cites that paragraph: surface as "cited-text-
  paraphrased — please verify the cited content still matches the
  current law".
- **References-manifest.yaml itself is stale** (last_fetched > 6
  months ago): surface a warning that verification may itself be
  stale.

## Tools used (when MCP backend lands)

- `search_corpus(query, filter)` — find current cited_form in
  references.
- `read_corpus_file(path)` — read full reference text for verbatim
  comparison.

Until backend lands: fallback uses `Grep` over `<hidrive>/
_ai-references/` and `Read` of manifest.yaml.
