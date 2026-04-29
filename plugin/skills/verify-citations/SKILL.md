---
name: verify-citations
description: This skill should be used to cross-check legal citations (laws, paragraphs, court rulings, leitfäden) in a document or baustein against the current reference index. Triggered by phrases like "verify citations", "Zitate prüfen", "are citations current", "check §-references", as part of layered review (Layer 2 fachlich + Layer 3 formal), at compile-time validation, or after a reference update by research-references.
version: 0.3.0
license: MIT
mcp_tools_required: [search_corpus, list_reference_manifests]
mcp_tools_optional: [read_corpus_file, find_bausteine_by_reference]
fallback_when_mcp_absent: "warn user; degrade to Grep over <office>/_ai-references/ corpus + filesystem Read of manifest YAMLs. Iterative resolution still possible but slower; recall worse without semantic search."
---

# verify-citations

Specialist skill for citation freshness — detects when cited legal
forms in a document or baustein no longer match current reference
text. Source-grounding guard against citation rot. Per priority
touchpoint refactor (HANDOFF), uses **iterative per-citation
resolution** instead of flat batch lookup: ambiguous cite → fetch
the defining chapter → narrow → fetch interpreting ruling → decide.
Strengthens source-grounding by ensuring each verdict is backed by
an explicit retrieval chain.

## Load this now

Resolve the references in scope via `list_reference_manifests()`
(MCP tool). Returns the layered manifest set per office's active
scope.{domains,states} — universal + per-domain + per-state. Each
manifest entry has `id`, `current_amendment_form`, and pointers
into the references corpus at `office_config.roots.references`.

If the manifest set is empty (newly-deployed office; no manifests
yet) or the references corpus is missing, the skill cannot validate
against authoritative sources — fall back to "no current reference
index; cannot verify; recommend running research-references first."
Don't fabricate verdicts (source-grounding guard, orchestrator
PROCEDURE.md Checkpoint 5).

## When invoked

Three modes:

- **Document review** — scan a document for citations, verify
  each iteratively. Triggered at Layer 2 (fachlich) and Layer 3
  (formal) of layered review.
- **Baustein freshness check** — verify a single baustein's
  `references[]` field against `verified_against_version` slots.
  Triggered by `validate-bausteine` skill.
- **Targeted verify** — user asks "is BauGB §44 still current?"
  Single-citation lookup with iterative resolution.

Inputs:

- **Target** — document path OR baustein name OR explicit citation.

## Behavior — iterative per-citation resolution (priority refactor)

Old pattern: bulk-extract all citations, lookup each once, return
flat finding list. Replaced with per-citation iteration. For each
citation:

1. **Extract + classify**:
   - For documents: regex-extract `§ X <Gesetz>`, `§N Abs.M`,
     `Art. Y`, `BVerwG <docket>`, `EuGH C-...` patterns. Build
     list with file:line.
   - For bausteine: read `references[]` from frontmatter directly
     (each entry is already classified; `verified_against_version`
     gives the prior validation point).

2. **Per citation, iterate**:

   a. **Initial lookup** — `search_corpus(query=<citation>,
      filter={source_type: reference, reference_id: <law_id>})`
      to find matching reference text. Inspect top 1-3 results.

   b. **Disambiguation step** (if results ambiguous): the §
      number may be defined in the law plus interpreted in
      multiple rulings; the cited form may match a paragraph
      from a Verordnung distinct from the cited Gesetz. Don't
      stop at first hit. Fetch the defining chapter (the law's
      enumeration of the §) AND the most-recent interpreting
      ruling (search_corpus filter for ruling type referencing
      the same §). Verify the cited content against the defining
      paragraph; verify the cited interpretation against the
      ruling.

   c. **Narrow + decide**: with definition + interpretation in
      hand, decide:
      - **current** — cited form matches both definition and
        latest interpretation
      - **drift** — cited form lags the manifest's
        `current_amendment_form`; show both forms
      - **paraphrased** — cited verbatim quote no longer
        appears in source (law was reworded); surface for
        review
      - **removed** — referenced paragraph was repealed; critical
      - **not-found** — no manifest entry; suggest adding via
        research-references

   d. **For bausteine specifically**: also compare
      `verified_against_version` (per the baustein's
      `references[]` entry) against the manifest's current
      `current_amendment_form`. If different → flag drift even
      when the cited content still matches; the baustein hasn't
      been re-validated since the law amended.

3. **Build finding list** with the iterative chain explicit:
   each finding names what was searched, what was retrieved,
   what was compared. Source-grounded by construction.

4. **For document targets**, return findings inline with line
   numbers. For baustein targets, surface as candidate flag
   (set `status: flagged`, `flagged_reason: "citation drift
   detected; verified_against_version <X> vs manifest current
   <Y>"`) only after user confirms.

## Output

```
Citations in B-Plan Begründung.tex:

  L143: § 44 BNatSchG — current ✓
        Verified: defining chapter @ corpus/bund/BNatSchG/§44
                  + BVerwG-9-A-22-13 interpretation
  L201: BVerwG 9 A 22.11 — current ✓
        Verified: corpus/urteile/bverwg-9-a-22-11/full-text
  L267: BNatSchG i.d.F. ... 08.12.2022 — DRIFT
        Cited form: i.d.F. ... 08.12.2022
        Manifest current: i.d.F. ... 23.10.2024
        Defining chapter unchanged at §; only amendment-form drift.
        Update suggested: lines 267-268.
  L412: BauGB § 13b — NOT FOUND in references-manifest
        Searched: list_reference_manifests + search_corpus
                  filter={law: BauGB, paragraph: §13b}
        No hits. (BauGB §13b was re-introduced 2024; not yet
        ingested into corpus.) Run research-references to fetch.
```

End with one-line verdict: `BLOCK / WARN / PASS`.

## Edge cases

- **Citation in baustein contradicts citation in current document**:
  surface as inter-source drift. Both may need updating; iterate
  through each source independently.
- **Citation references something not in our manifest** (e.g. obscure
  Bundesländer law not in any selected state manifest): surface as
  "out-of-scope reference; cannot verify". Suggest user add to
  manifest via author-manifest + research-references if relevant.
- **Cited form is paraphrase, not verbatim**: harder to detect.
  Iterative step: fetch the defining chapter, compare cited form
  to paragraph text via fuzzy match. If text is far from any
  current paragraph but cites that paragraph, surface as
  "cited-text-paraphrased — please verify the cited content
  still matches the current law."
- **Manifest entry's `last_fetched > 6 months ago`**: surface a
  warning that verification may itself be stale (the cached
  reference is old; check upstream via research-references).
- **Iteration would explode (document with 100+ citations)**:
  cap iteration depth per citation to 2 (initial + one
  disambiguation); for the rest fall back to flat lookup with a
  note. Surface volume warning.

## Tools used

- `search_corpus(query, filter)` (MCP, required) — find current
  cited_form in references; per-iteration retrieval.
- `list_reference_manifests(scope_filter=true)` (MCP, required) —
  enumerate the manifest set in scope; access
  `current_amendment_form` per entry.
- `read_corpus_file(path)` (MCP, optional) — read full reference
  text for verbatim comparison when fuzzy-match flagged.
- `find_bausteine_by_reference(law?, paragraph?, ruling?, leitfaden?)`
  (MCP, optional) — for inter-source drift detection: find other
  bausteine that cite the same reference and check whether their
  `verified_against_version` agrees with the doc under review.

When MCP backend unreachable: fall back to `Grep` over the office's
references corpus at `office_config.roots.references` and
`Read` of manifest YAMLs. Iterative resolution still possible but
slower; recall worse without semantic search. Warn user about
degraded mode.
