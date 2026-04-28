---
name: research-references
description: This skill should be used to fetch, update, or check freshness of legal references (gesetze, leitfäden, urteile) tracked in references-manifest.yaml. Triggered by user phrases like "update references", "neue Fassung holen", "BauGB current?", "research new law", "are our laws current?", "refresh references", "gesetze aktualisieren", "fetch BVerwG ruling", or scheduled refresh checks.
version: 0.1.0
license: MIT
---

# research-references

Specialist skill for maintaining the reference corpus — fetching,
diffing, and updating legal texts and guidance documents in
the office's `paths.references_root`.

## Load this now

Read `references/manifest-schema.md` for the
`references-manifest.yaml` schema, entry types, and the update
workflow.

## Source-of-truth principle

The reference corpus at the office's `_ai-references/` directory is
the **single, authoritative source of truth** for every entry in the
manifest. One canonical file per manifest ID, written by this skill,
fetched fresh from the publisher.

Implications:

- Every entry in the manifest goes through a fresh fetch on first run
  and on every refresh — no "use existing copy if present" branch.
- The skill does not read references from anywhere other than its own
  output directory. If a reference is needed but the corpus doesn't
  have it, the answer is to fetch it, never to look elsewhere.
- All downstream consumers (`search_corpus`, `read_corpus_file`,
  citations in drafts) resolve references through this corpus only.

## When invoked

Three modes:

- **Full refresh** — "update references", "refresh all": walks the
  full manifest.
- **Targeted refresh** — "is BauGB current?", "fetch the new BVerwG
  ruling", "check LUNG leitfaden": single-entry or filtered subset.
- **New-entry registration** — "add this leitfaden", "register a new
  ruling": user provides URL + metadata, skill appends a manifest
  entry and fetches.

## Behavior (full refresh)

1. **Read manifest** at `<repo>/references-manifest.yaml`.

2. **For each entry, fetch + diff**:
   - Fetch from `source_url` via `fetch_method`:
     - `web-text` — HTML scrape, plain text via readability extraction
     - `web-html` — preserve structure (for laws with §-anchors)
     - `web-pdf` — download PDF, extract text via pymupdf4llm
     - `git-mirror` — clone/pull from a known mirror repo
     - `manual` — skip; user uploads directly
   - Compute SHA-256 of fetched content.
   - Compare against `checksum_sha256` in manifest.

3. **If unchanged**: update `last_fetched` timestamp; no further
   action.

4. **If changed**:
   - **Archive old version** (if `archive_versions: true`):
     copy current `canonical_path` to
     `<canonical_dir>/<id>/archive/<old-fetch-date>.<ext>`.
   - **Write new content** to `canonical_path`.
   - **Update manifest entry**: `last_fetched`, `checksum_sha256`,
     `last_modified_at_source` (parsed from content),
     `current_amendment_form` (parsed from content).
   - **Surface diff to user**: meaningful summary (e.g.
     "BauGB §13b: text changed; old version archived. Specific changes:
     <bullet diff>."). Use unified diff for short changes; summary for
     long.
   - **Wait for user approval** before re-ingesting.

5. **On user approval, re-ingest into LanceDB**:
   - Call `ingest_paths(paths=[changed_path], force=true)` —
     deletes old chunks for this path, re-chunks + re-embeds with
     fresh metadata.

6. **Cross-reference dependents** (cross-cutting concern handler):
   for each changed entry, find both bausteine and cross-cutting
   memory docs that depend on the reference:
   - **Bausteine**: scan `<repo>/memory/*/<name>.md` frontmatter for
     `references[]` matching `law` / `paragraph` / `ruling` /
     `leitfaden`. Each match → set `status: flagged`,
     `flagged_reason: "reference updated <date>"`.
   - **Memory docs**: scan `<repo>/memory/**/*.md` frontmatter for
     `references_used[]` matching the same keys. Each match → append
     a row to `<repo>/memory/product-backlog.md` with date, affected
     doc path, and which references changed. (Memory docs have no
     `status` field; the orchestrator surfaces flagged docs at session
     open.)
   - List both flagged bausteine and flagged memory docs to user.

7. **Append to changelog**: write summary entry to
   `<references_root>/changelog.md`. Include count of entries
   checked, count changed, count errored.

## Behavior (targeted refresh)

Same as full refresh but scoped to filtered entries (single ID, or
matching tag, or matching category).

## Behavior (new-entry registration)

1. Solicit metadata from user: ID, title, category, source_url,
   fetch_method.
2. Determine `canonical_path` per category convention.
3. Append entry to `references-manifest.yaml`.
4. Run targeted refresh on the new entry to do initial fetch.

## Output

User sees:

- Summary line: "X entries checked; Y changed; Z errored."
- Per change: 1-line description + path of new + path of archived old.
- Per error: 1-line description + suggested action ("URL dead — check
  source").
- List of flagged bausteine with paths.
- Path of changelog entry.

## Edge cases

- **Source URL dead (404)**: don't archive, don't overwrite. Set
  manifest entry note. Surface to user; suggest alternate source.
- **Source returned content unchanged but checksum differs** (e.g.
  whitespace, timestamp in HTML): heuristic detection — strip
  common variable elements (timestamps in headers, session IDs)
  before checksumming. If still mismatch but content semantically
  identical, log as "noise change" and don't archive.
- **Manifest entry missing required fields**: fail loud, ask user to
  fix manifest.
- **Fetched content suspicious** (e.g. captcha page returned, login
  form): detect via heuristics (very short content for laws,
  presence of "captcha"/"login" tokens). Treat as fetch error.

## Tools used (when MCP backend lands)

- `WebFetch` (built-in) for source URLs.
- `ingest_paths(paths, force?)` — re-ingestion.
- `find_bausteine_by_reference(law, paragraph)` — cross-reference
  dependents.

Until backend lands: filesystem `Write` for canonical_path updates +
`WebFetch` + `Edit` on manifest. Re-ingestion deferred (graceful fail
with note "skipped re-ingest; backend not online").
