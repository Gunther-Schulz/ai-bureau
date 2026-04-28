---
name: research-references
description: This skill should be used to fetch, update, or check freshness of legal references (gesetze, leitfäden, urteile) tracked in references-manifest.yaml. Triggered by user phrases like "update references", "neue Fassung holen", "BauGB current?", "research new law", "are our laws current?", or scheduled refresh checks.
version: 0.1.0
license: MIT
---

# research-references

Specialist skill for maintaining the reference corpus — fetching,
diffing, and updating legal texts and guidance documents.

## Load this now

Read `references/manifest-schema.md` for the
`references-manifest.yaml` schema, entry types, and the update
workflow.

## When invoked

By user request or scheduled refresh:
- "update references" → full refresh of all entries
- "is BauGB current?" → check single entry
- After law amendment news → targeted re-fetch of affected entries

## Behavior

1. Read `<repo>/references-manifest.yaml`.
2. For each entry: fetch from `source_url` via `fetch_method`.
3. Compute checksum, compare to stored.
4. If changed:
   - archive old version (if `archive_versions: true`)
   - write new content to `canonical_path`
   - update `last_fetched`, `checksum_sha256`,
     `current_amendment_form`
   - surface diff to user
   - on user approval: re-ingest into LanceDB via
     `ingest_paths(force=true)`
5. Cross-reference: find bausteine whose `references[]` mention
   changed entries → flag them for re-validation.
6. Append run summary to `<hidrive>/_ai-references/changelog.md`.

## Status

v0.1: stub. Manifest schema reference is complete; behavior
implementation follows when MCP tool surface lands.
