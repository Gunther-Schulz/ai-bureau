# pbs-bureau backend

Local services that the plugin's MCP tools rely on. Runs independently
of Claude Code; the plugin connects via stdio MCP.

## Components (planned)

- **Ollama** (Docker) — embedding model `nomic-embed-text-v1.5` for
  corpus indexing.
- **MCP server** (Python, stdio) — tool surface exposed to Claude Code:
  - `search_corpus(query, k, filter)` — vector search over corpus +
    references
  - `read_corpus_file(path)` — direct file read
  - `list_projects()`, `bind_project(name, root_path)` — project state
  - `ingest_project_inputs(project, paths)`, `search_inputs(...)` — per-
    project namespaced RAG
  - `list_bausteine(scope, domain?)`, `get_baustein(name)`,
    `save_baustein(scope, name, content, source)` — memory ops
  - `compile_latex(project_path)` — latexmk wrapper, returns PDF path
    + log
  - `survey_project(root_path)` — first-bind clustering of files for
    `_ai/file-map.md`
- **LanceDB** — embedded; lives in `data/lancedb/` (gitignored).

## Status

Skeleton only. Implementation pending in v0.2.x. See `<repo>/ROADMAP.md`
for sequencing.
