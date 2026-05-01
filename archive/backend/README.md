# pbs-bureau backend

Local services that the plugin's MCP tools rely on. Runs independently
of Claude Code; the plugin connects via stdio MCP.

## Components

- **MCP server** (Python, stdio) — single in-process backend. Holds
  the LanceDB connection, the embedder, and the LaTeX compile wrapper.
  No separate services. 22 MCP tools registered; full inventory at
  `backend/mcp-server/src/pbs_mcp/server.py` `TOOL_HANDLERS`. Highlights:
  - **Corpus**: `search_corpus`, `read_corpus_file`, `ingest_paths`
  - **Project-namespaced RAG**: `ingest_project_inputs`, `search_inputs`
  - **Memory**: `list_bausteine(scope?, scope_key?, project_root?, status?)`,
    `get_baustein`, `save_baustein`, `flag_baustein`, `archive_baustein`,
    `find_bausteine_by_reference`
  - **Project lifecycle**: `list_projects`, `bind_project`,
    `setup_project`, `survey_project`, `scaffold_project`
  - **Discovery (Tier 1, post-orthogonality)**: `list_skills`,
    `list_reference_manifests`, `list_doctypes_manifests`,
    `list_skeletons`
  - **Build**: `compile_latex` — latexmk wrapper
- **LanceDB** — embedded vector store; lives in `data/lancedb/`
  (gitignored).
- **SQLite legal-graph** — separate file alongside LanceDB
  (`legal-graph.sqlite`), populated at ingest with §-graph nodes +
  typed edges. Phase 3 work (deferred per
  `docs/rag-pipeline-decisions.md` B).
- **Embedder** — `fastembed` running in-process inside the MCP server
  with `BAAI/bge-m3` (568M params, 8k context, strong multilingual
  recall — important for German legal/planning text). Same model files
  Ollama would serve, but loaded directly via ONNX runtime, no
  separate service. Models cached in `~/.cache/fastembed/`.
- **Reranker** — `BAAI/bge-reranker-v2-m3` (cross-encoder); pinned in
  pyproject. Decision recorded in `docs/rag-pipeline-decisions.md` § 3.

## Why no Ollama / no Docker

Earlier drafts targeted Ollama+nomic-embed in Docker. Reconsidered:
quality comes from the model choice (bge-m3 vs nomic-embed-v1.5),
not from the runtime. fastembed runs the same models in-process with
near-zero latency, no Docker dependency, and no separate service to
manage. Ollama remains a viable swap if a future need arises (e.g.
GPU acceleration, runtime model swapping, or running a local LLM in
the same stack — none of which apply now).

## Status

22 MCP tools registered + handlers wired. Pre-RAG state: corpus
search/ingest/embedding works for text; multimodal (OCR, ColPali,
image retrieval) is Phase 3 per `docs/rag-pipeline-decisions.md`.
Conventions for backend Python (test layout, logging, MCP error
format) at `docs/backend-conventions.md`.

Run from `backend/mcp-server/` with `uv sync && uv run pbs-mcp`.

See `backend/mcp-server/README.md` for setup and configuration.
