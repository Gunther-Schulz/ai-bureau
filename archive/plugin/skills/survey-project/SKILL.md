---
name: survey-project
description: This skill should be used when first binding to an existing project that has no _ai/ folder yet. It walks the project root, clusters files by likely role (artifacts, inputs, sent versions, correspondence, cruft), and proposes a file-map.md interpretation for user confirmation. Triggered by orchestrator's binding flow (Checkpoint 11) or by direct user phrases like "survey this project", "scan the folder", "binde dieses Projekt".
version: 0.5.0
license: MIT
mcp_tools_required: [list_doctypes_manifests, bind_project, update_project_state]
mcp_tools_optional: [search_inputs, list_skeletons, get_project_state]
fallback_when_mcp_absent: "warn user; without bind_project the skill cannot create state.md (strict-validated contract per ARCHITECTURE meta-rule 4 — direct write forbidden). Doctype-manifest fallback to direct Read of extensions/{universal,domain/<X>}/doctypes.yaml works; per-ambiguous-file content sniffing still works without MCP."
summary: First-bind clustering of project files into a _ai/file-map.md interpretation. Walks ambiguous files iteratively.
routing_mode: direct
triggers:
  - survey project
  - bind project from existing folder
  - scan project folder
handoffs: []
phase_role: lifecycle
---

# survey-project

Specialist skill for first-bind clustering of project files. Reads
a project's filesystem, identifies likely roles per file/cluster,
and proposes a `_ai/file-map.md` for user confirmation. Per priority
touchpoint refactor (HANDOFF), uses **per-ambiguous-file iteration**
(filename → content sniff → mtime → related files) instead of
one-shot classification. Strengthens classification accuracy on
projects with non-canonical layouts.

## Load this now

Read `<repo>/memory/universal/project-structure.md` for the canonical
new-project folder structure. Existing projects often diverge from
it; the divergence is exactly what file-map.md captures.

Call `list_doctypes_manifests()` (MCP tool) for the layered doctype
registry — universal + per-active-domain. Each doctype entry
declares filename heuristics, master-file conventions, and
folder-name patterns used for classification.

## When invoked

By orchestrator's binding flow when a referenced project has no
`_ai/` or `.ai/` folder. Inputs:

- **Project root path** — absolute path under
  `office_config.roots.projects` (or anywhere the user
  provides).
- **Project name** — for `bind_project` invocation that constructs state.md through the ProjectState contract.
- **Practices guess** — orchestrator's guess of one or more
  practice ids from `office_config.actors` (kind=internal), derived from
  path/file heuristic (presence of doctype-relevant files vs.
  other practices' workspace markers).

## Behavior — per-ambiguous-file iteration (priority refactor)

Old pattern: glob recursively, classify each file by single
heuristic, surface clusters. Replaced with iterative classification:

1. **Recursive glob to depth 4** of the project root, with exclusions:
   - Build artifacts: `*.aux`, `*.fdb_latexmk`, `*.fls`, `*.log`,
     `*.lot`, `*.toc`, `*.synctex.gz`
   - Office lockfiles: `~$*`
   - macOS detritus: `.DS_Store`, `._.*`
   - Backup files: `*.bak`, `*.old`

2. **Confident first-pass classification** — files matching strong
   heuristics get classified immediately:
   - `Schriftverkehr/eml/*.eml` → correspondence
   - `inputs/auftraggeber/*.pdf` → inputs (active)
   - `B-Plan/Begründung/*.tex` → doctype-relevant artifact
   - `Fotos/`, `Bilder/`, `Karten/` directories → resources to
     leave alone

3. **Per ambiguous file, iterate** (the priority refactor):

   For each file that didn't match a strong heuristic, run the
   classification chain step-by-step:

   a. **Filename pattern** — does the name match a doctype
      registry pattern (from `list_doctypes_manifests()`)? a
      typical input pattern? a sent-version pattern (`_v[N]`,
      `_final`, dates in name)?

   b. **Content sniff** — read first 500 chars or so. LaTeX
      preamble? PDF magic bytes? markdown frontmatter? German
      Begründungs-style prose vs. Stellungnahme-style prose?
      Use this to narrow type.

   c. **mtime context** — when was this last modified? Recent
      activity → likely active. Old + others nearby older →
      possibly archived. Old + nothing else nearby → orphan
      (likely cruft).

   d. **Related files** — same directory, same mtime cluster?
      That gives context. A `.tex` next to a `.pdf` of the
      same date is likely the source + output pair. A loose
      `.docx` with no nearby siblings is likely legacy.

   e. **Decide**: confident classification, or surface to user
      with the iteration trail visible:
      ```
      <path/to/file.tex>:
        - filename: matches no canonical pattern
        - content: LaTeX article-class with German prose
        - mtime: 2025-08-15 (4 months ago)
        - nearby: alone in this directory
        - guess: orphan / superseded? Or undocumented active?
        → user-decide
      ```

4. **Cluster by mtime windows**: files modified within ~1 week of
   each other often belong to the same work session. Group
   accordingly for context display.

5. **Detect stale inputs**: if multiple files match the same kind
   pattern (e.g. multiple `briefing-*.pdf` with different dates),
   propose newest as active and others as superseded.

6. **Detect doctype-progress**: which doctype folders exist?
   Which contain `.tex` (LaTeX active) vs only `.doc` (legacy
   in transition)? Inform `state.md.doctype_status` proposal.
   Use `list_skeletons(doctype)` to know what a fully-scaffolded
   doctype subfolder should look like.

7. **Compose draft `file-map.md`** per
   `<repo>/plugin/skills/orchestrator/references/state-format.md`
   structure:
   - Frontmatter: project, last_survey, last_modified_at_survey,
     survey_method.
   - Sections: Current artifacts / Sent versions / Inputs (active)
     / Inputs (superseded) / Stellungnahmen / Resources / Cruft / Notes.
   - Surface the iteration trail for any file the user needs to
     decide on (don't hide the reasoning).

8. **Propose `state.md`** with detected fields:
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

9. **Surface clusters and proposals to user**, walk through each
   cluster, get confirmation/correction before writing. For
   ambiguous files, show the iteration trail so the user can
   verify the reasoning.

10. **On user confirmation**:
    - Call `bind_project(name, root_path, bundesland, verfahren_type, phase)` — creates `_ai/state.md` through the ProjectState Pydantic contract (strict-validated; never write state.md directly per ARCHITECTURE meta-rule 4).
    - For any survey-derived fields beyond bind_project's required inputs (e.g. `doctype_status`, `practices`, `lifecycle` corrections, `client`, `location`), call `update_project_state(project, updates={...})`.
    - Write directly (these files have no schema contract):
      - `_ai/file-map.md` with confirmed cluster assignments.
      - `_ai/decisions.md` empty (no decisions yet).
      - `_ai/correspondence-log.md` with one row per detected `.eml` / call note found in `Schriftverkehr/`.
      - `_ai/module-decisions.md` empty.
      - `_ai/snapshots/` empty directory.

11. **Append project to**
    `<state_root>/projects-index.md` (`state_root` resolved via
    `office_config.paths.state_root`).

## Output

Step-by-step interactive walk:

```
Surveying YY-NN <Client> - <Location>...

Found 142 files, 8 folders. Confident classification: 89 files.
Ambiguous: 53 — iterating per-file.

Ambiguous file 1: alt/B-Plan-v2.tex
  - filename: matches "_v<N>" sent-version pattern
  - content: LaTeX scrreprt; date 2024-03 in title
  - mtime: 2024-03-22 (over 1 year ago)
  - nearby: B-Plan-v2.pdf same date
  → guess: sent version (paired source + output)
  Confirm as "Sent / archived versions"? [y/n/modify]

Ambiguous file 2: working/old-bodenschutz.tex
  - filename: "old-" prefix
  - content: incomplete; partial Bodenschutz-section
  - mtime: 2024-08-04 (older than current Begründung)
  - nearby: none active
  → guess: orphan / unmerged drafts
  Surface for decision? [y/n/modify]

[... continues per ambiguous file ...]

Cluster 1 — Doctype artifacts (confident):
  - B-Plan/Begründung/<doctype-master>.tex (working draft, mtime YYYY-MM-DD)
  - …
  Confirm as "Current artifacts"? [y/n/modify]

[... clusters as before ...]

Proposed state.md:
  lifecycle: revision-requested
  practices: [<id-1>, <id-2>]   (multi-practice — markers found)
  phase: 6-abwaegung
  doctype_status:
    b-plan-begruendung: active
    b-plan-festsetzungen: active
    umweltbericht: applicable

Confirm? [y/n/modify]
```

## Edge cases

- **Project root contains nested project** (rare; e.g. an example
  template tree inside another project): surface as anomaly, ask
  user for guidance.
- **Project shows another practice's workspace markers** (e.g. a
  sibling GIS practice's `scripts/`, `workflow.yaml`, `*.qgz`):
  add the corresponding practice id to `practices`. Don't write to
  that practice's directories — they are read-only here.
- **Project size huge (thousands of files)**: cap glob; cap
  iteration to top-N ambiguous files by mtime. Surface warning
  that survey is partial; let user prioritize sub-folders for
  deeper iteration.
- **mtime cluster spans years**: project has long history; expect
  many "sent versions". Propose most recent N as candidates for
  active; user decides.
- **Doctype manifest empty** (newly-deployed office): fall back
  to filename-only heuristics for doctype identification. Surface
  as T6 capability gap (would benefit from manifest population).

## Tools used

- `list_doctypes_manifests(scope_filter=true)` (MCP, required) —
  layered doctype registry for filename / folder pattern matching.
- `bind_project(...)` (MCP, required) — creates state.md through
  the ProjectState contract on user confirmation. Direct write of
  state.md is forbidden (ARCHITECTURE meta-rule 4).
- `update_project_state(project, updates)` (MCP, required) — applies
  survey-derived fields to state.md after bind_project creates it.
- `search_inputs(project, query)` (MCP, optional) — only useful
  AFTER first ingest; not used during initial bind.
- `list_skeletons(doctype)` (MCP, optional) — knowing what a
  scaffolded doctype subfolder looks like helps detect partial
  scaffolds.
- `Glob` — recursive file enumeration.
- `Read` — sample file content for doctype/role identification
  + iteration content-sniff step. NOT used for state.md.
- `Bash` — file metadata via stat (when needed for mtime).

When MCP backend unreachable: fall back to direct filesystem reads
of `extensions/{universal,domain/<X>}/doctypes.yaml`. Per-
ambiguous-file iteration still works without MCP — content sniff
+ mtime + neighbor analysis are pure filesystem operations.
