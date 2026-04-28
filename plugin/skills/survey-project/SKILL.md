---
name: survey-project
description: This skill should be used when first binding to an existing project that has no _ai/ folder yet. It walks the project root, clusters files by likely role (artifacts, inputs, sent versions, correspondence, cruft), and proposes a file-map.md interpretation for user confirmation. Triggered by orchestrator's binding flow (Checkpoint 11) or by direct user phrases like "survey this project", "scan the folder", "binde dieses Projekt".
version: 0.1.0
license: MIT
---

# survey-project

Specialist skill for first-bind clustering of project files. Reads a
project's filesystem, identifies likely roles per file/cluster, and
proposes a `_ai/file-map.md` for user confirmation.

## Load this now

Read `<repo>/memory/domain/project-structure.md` for the canonical
new-project folder structure. Existing projects often diverge from
it; the divergence is exactly what file-map.md captures.

Read `<repo>/memory/domain/doctypes.yaml` for doctype identification
heuristics.

## When invoked

By orchestrator's binding flow when a referenced project has no
`_ai/` or `.ai/` folder. Inputs:

- **Project root path** — absolute path on hidrive (or local).
- **Project name** — for state.md construction.
- **Practices guess** — orchestrator's guess of `[schulz]`,
  `[hendrik]`, or `[joint]` from path heuristic.

## Behavior

1. **Recursive glob to depth 4** of the project root, with
   exclusions:
   - Build artifacts: `*.aux`, `*.fdb_latexmk`, `*.fls`, `*.log`,
     `*.lot`, `*.toc`, `*.synctex.gz`
   - Office lockfiles: `~$*`
   - macOS detritus: `.DS_Store`, `._.*`
   - Backup files: `*.bak`, `*.old`

2. **Cluster by mtime windows**: files modified within ~1 week of
   each other often belong to the same work session. Group accordingly
   for context.

3. **Classify each file/folder by heuristic**:
   - **Doctype-relevant artifacts**: `.tex` files, `.pdf` outputs,
     `Textbausteine/`, `B-Plan/` substructures, `Umweltbericht/`
     subfolders, `Externe Gutachten/` (third-party reports).
   - **Inputs**: `Grundlagen/`, `Inputs/`, briefings, surveys,
     drone scans, GIS data files.
   - **Correspondence**: `Schriftverkehr/`, `*.eml`, `telefon-
     notizen/`, `besprechungsprotokolle/`.
   - **Resources to leave alone**: `Fotos/`, `Bilder/`, `GIS/`
     (Hendrik), `Karten/`, `ProjektBeispiel*` (templates).
   - **Sent / archived versions**: pattern `*_v[N].tex`, `*_final*`,
     `*_UNB-*`, files in subfolders named `alt/`, `archive/`,
     `sent/`.
   - **Cruft / unclassifiable**: surface for user to decide.

4. **Detect stale inputs**: if multiple files match the same kind
   pattern (e.g. multiple `briefing-*.pdf` with different dates),
   propose newest as active and others as superseded.

5. **Detect doctype-progress**: which doctype folders exist? Which
   contain `.tex` (LaTeX active) vs only `.doc` (legacy in
   transition)? Inform `state.md.doctype_status` proposal.

6. **Compose draft `file-map.md`** per `state-format.md` per
   `<repo>/plugin/skills/orchestrator/references/state-format.md`
   structure:
   - Frontmatter: project, last_survey, last_modified_at_survey,
     survey_method.
   - Sections: Current artifacts / Sent versions / Inputs (active) /
     Inputs (superseded) / Stellungnahmen / Resources / Cruft / Notes.

7. **Propose `state.md`** with detected fields:
   - `lifecycle` — guess from latest mtime + sent-version presence:
     - No sent versions → `draft`
     - Sent version + no response yet → `awaiting-response`
     - Recent activity post-send → `revision-requested`
   - `practices` — confirm or correct from path heuristic.
   - `doctype_status` — `active` for doctypes with current .tex,
     `applicable` for doctypes with only .doc, `tbd` for doctypes
     with no content yet.
   - `phase` — best guess from correspondence dates + sent-version
     metadata.

8. **Surface clusters and proposals to user**, walk through each
   cluster, get confirmation/correction before writing.

9. **On user confirmation**, write:
   - `_ai/state.md` with confirmed/corrected fields.
   - `_ai/file-map.md` with confirmed cluster assignments.
   - `_ai/decisions.md` empty (no decisions yet).
   - `_ai/correspondence-log.md` with one row per detected `.eml` /
     call note found in `Schriftverkehr/`.
   - `_ai/module-decisions.md` empty.
   - `_ai/snapshots/` empty directory.

10. **Append project to** `<hidrive>/_ai-office-state/projects-
    index.md`.

## Output

Step-by-step interactive walk:

```
Surveying 23-12 Maxsolar - Vorbeck (Schwaan)...

Found 142 files, 8 folders. Clustering...

Cluster 1 — Doctype artifacts:
  - B-Plan/Textteil B/B-Plan Begründung.tex (working draft, mtime 2026-04-22)
  - B-Plan/Testteil C/Textteil-B-B-Plan.tex (working draft, mtime 2026-04-22)
  Confirm as "Current artifacts"? [y/n/modify]

Cluster 2 — Sent versions:
  - alt/Begründung_v2_UNB-2024-03.tex (sent 2024-03-15)
  Confirm as "Sent / archived versions"? [y/n/modify]

...

Proposed state.md:
  lifecycle: revision-requested
  practices: [schulz, hendrik]   (joint — found GIS/ + scripts/)
  phase: 6-abwaegung
  doctype_status:
    b-plan-begruendung: active
    b-plan-festsetzungen: active
    umweltbericht: applicable

Confirm? [y/n/modify]
```

## Edge cases

- **Project root contains nested project** (rare; e.g. `Projekt-
  beispiel-B-Plan/` inside another project): surface as anomaly,
  ask user for guidance.
- **Project has Hendrik's `CLAUDE.md` already**: GIS workflow exists.
  Mark `practices: [joint]`. Don't write to GIS/ — that's Hendrik's
  workspace.
- **Project size huge (thousands of files)**: cap glob; surface
  warning that survey is partial; let user prioritize sub-folders.
- **mtime cluster spans years**: project has long history; expect
  many "sent versions". Propose most recent N as candidates for
  active; user decides.

## Tools used

- `Glob` — recursive file enumeration.
- `Read` — sample file content for doctype/role identification.
- `Bash` — file metadata via stat (when needed for mtime).
- No MCP backend dependency.
