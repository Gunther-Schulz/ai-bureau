# pbs-bureau backend

Local services that the plugin's MCP tools rely on. Runs independently
of Claude Code; the plugin connects via stdio MCP.

## Components (planned)

- **MCP server** (Python, stdio) — single in-process backend. Holds
  the LanceDB connection, the embedder, and the LaTeX compile wrapper.
  No separate services. Tool surface exposed to Claude Code:
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
- **LanceDB** — embedded vector store; lives in `data/lancedb/`
  (gitignored).
- **Embedder** — `fastembed` running in-process inside the MCP server
  with `BAAI/bge-m3` (568M params, 8k context, strong multilingual
  recall — important for German legal/planning text). Same model files
  Ollama would serve, but loaded directly via ONNX runtime, no
  separate service. Models cached in `~/.cache/fastembed/`.

## Why no Ollama / no Docker

Earlier drafts targeted Ollama+nomic-embed in Docker. Reconsidered:
quality comes from the model choice (bge-m3 vs nomic-embed-v1.5),
not from the runtime. fastembed runs the same models in-process with
near-zero latency, no Docker dependency, and no separate service to
manage. Ollama remains a viable swap if a future need arises (e.g.
GPU acceleration, runtime model swapping, or running a local LLM in
the same stack — none of which apply now).

## Status

Skeleton only. Implementation pending in v0.2.x. See `<repo>/ROADMAP.md`
for sequencing.
