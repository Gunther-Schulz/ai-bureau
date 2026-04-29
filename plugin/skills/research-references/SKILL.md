---
name: research-references
description: This skill should be used to fetch, update, or check freshness of legal references (gesetze, leitfäden, urteile) tracked across the office's layered references manifests. Triggered by user phrases like "update references", "neue Fassung holen", "BauGB current?", "research new law", "are our laws current?", "refresh references", "gesetze aktualisieren", "fetch BVerwG ruling", or scheduled refresh checks.
version: 0.3.0
license: MIT
mcp_tools_required: [list_reference_manifests, ingest_paths]
mcp_tools_optional: [find_bausteine_by_reference]
fallback_when_mcp_absent: "without list_reference_manifests + ingest_paths the skill cannot run a refresh — fail loud and route the user to restart the backend. find_bausteine_by_reference is optional; without it, dependent-baustein cross-reference falls back to a filesystem scan of memory/bausteine/**."
---

# research-references

Specialist skill for maintaining the reference corpus — fetching,
diffing, and updating legal texts and guidance documents across the
office's layered manifests (universal + per-domain + per-state).

## Load this now

Read `references/manifest-schema.md` for the
`references-manifest.yaml` schema, entry types, and the update
workflow.

## Source-of-truth principle

The reference corpus at the office's `_ai-references/` directory is
the **single, authoritative source of truth** for every entry across
every selected manifest layer. One canonical file per manifest ID,
written by this skill, fetched fresh from the publisher.

Implications:

- Every entry goes through a fresh fetch on first run and on every
  refresh — no "use existing copy if present" branch.
- The skill does not read references from anywhere other than its own
  output directory. If a reference is needed but the corpus doesn't
  have it, the answer is to fetch it, never to look elsewhere.
- All downstream consumers (`search_corpus`, `read_corpus_file`,
  citations in drafts) resolve references through this corpus only.

## Manifest sources (layered)

The skill walks the union of manifests selected by the office's
`scope` configuration — obtained from
`list_reference_manifests(scope_filter=true)` (Tier 1 MCP tool). The
list returns in load order:

1. `extensions/universal/references-manifest.yaml` (every bureau)
2. For each domain in `scope.domains`:
   `extensions/domain/<X>/references-manifest.yaml`
3. For each state in `scope.states`:
   `extensions/state/<X>/references-manifest.yaml`

Files not present on disk (placeholder dirs, unselected scope) are
silently skipped. The skill never reaches outside this set.

## When invoked

Three modes:

- **Full refresh** — "update references", "refresh all": walks the
  full union manifest set.
- **Targeted refresh** — "is BauGB current?", "fetch the new BVerwG
  ruling": single-entry or filtered subset across all manifests.
- **New-entry registration** — "add this leitfaden", "register a new
  ruling": user provides URL + metadata + target layer
  (universal/domain/state). Skill appends to the matching manifest
  and fetches.

## Behavior (full refresh)

1. **Resolve manifest set** via
   `list_reference_manifests(scope_filter=true)`. Report which
   manifests are in scope.

2. **For each entry in each manifest, fetch + diff**:
   - Fetch from `source_url` via `fetch_method`:
     - `web-text` — HTML scrape, plain text via readability extraction
     - `web-html` — preserve structure (for laws with §-anchors)
     - `web-pdf` — download PDF, extract text via pymupdf4llm
     - `git-mirror` — clone/pull from a known mirror repo
     - `manual` — Claude browses the publisher site to discover the
       canonical PDF URL, then downloads (used for KNE/LUNG/etc.
       leitfäden where direct PDF URLs aren't stable)
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
     `last_modified_at_source`, `current_amendment_form` (parsed
     from content).
   - **Surface diff to user**: meaningful summary.
   - **Wait for user approval** before re-ingesting.

5. **On user approval, re-ingest into LanceDB**:
   - Call `ingest_paths(paths=[changed_path], force=true)` —
     deletes old chunks for this path, re-chunks + re-embeds.

6. **Cross-reference dependents** (cross-cutting concern handler):
   for each changed entry, find both bausteine and memory docs
   that depend on the reference:
   - **Bausteine**: scan `<repo>/memory/bausteine/**/<name>.md`
     frontmatter for `references[]` matching `law` / `paragraph` /
     `ruling` / `leitfaden`. Each match → set `status: flagged`,
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
   checked per manifest, count changed, count errored.

## Behavior (targeted refresh)

Same as full refresh but scoped to filtered entries (single ID across
manifests, matching tag, matching category, or matching layer/scope-
key like "all entries from domain/Wind").

## Behavior (new-entry registration)

1. Solicit metadata from user: ID, title, category, source_url,
   fetch_method.
2. Determine target manifest layer:
   - State-specific law → `state/<X>/references-manifest.yaml`
   - Domain-specific Leitfaden → `domain/<X>/references-manifest.yaml`
   - Universal federal law → `universal/references-manifest.yaml`
3. Determine `canonical_path` per category convention.
4. Append entry to the chosen manifest. If the target manifest
   doesn't yet exist (e.g. user wants to add the first entry to
   `extensions/state/SH/`), hand off to `author-manifest` to scaffold
   it first.
5. Run targeted refresh on the new entry to do initial fetch.

## Output

User sees:

- Per manifest: "X entries checked; Y changed; Z errored."
- Across union: total counts.
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
  form): detect via heuristics. Treat as fetch error.
- **Same entry ID in multiple manifest layers**: not allowed.
  Universal-core and state-extension should never have the same ID.
  Surface as a config error.

## Tools used

- `WebFetch` (built-in) for source URLs.
- `list_reference_manifests(scope_filter=true)` (MCP) to enumerate.
- `ingest_paths(paths, force?)` (MCP tool) — re-ingestion.
- `find_bausteine_by_reference(law, paragraph)` — cross-reference
  dependents.
- Filesystem `Read` / `Edit` on each manifest YAML.
- Hands off to `author-manifest` if an entry needs to be added to a
  manifest that doesn't yet exist.
