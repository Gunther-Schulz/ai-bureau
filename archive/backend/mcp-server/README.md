# pbs-mcp

Local MCP backend for the pbs-bureau Claude Code plugin. Single Python
process holding LanceDB (vector store), fastembed (embedder, bge-m3),
and a LaTeX compile wrapper. Spawned by Claude Code via stdio.

## Setup

```bash
cd backend/mcp-server
uv sync                          # creates .venv and installs deps
uv run pbs-mcp                   # starts the stdio MCP server (for testing)
```

Requires Python 3.13 (pinned via `.python-version`). `uv` will install
that automatically if it's not present.

## Configuration

Paths are auto-detected from the repo root. Override via environment
variables (mainly for tests):

| Var | Default |
|---|---|
| `PBS_REPO_ROOT` | auto-detected by walking up from `pbs_mcp/config.py` |
| `PBS_HIDRIVE_PROJEKTE` | `/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte` |
| `PBS_LOCAL_REPOS` | `~/dev/Planungsbüro-Schulz/` |
| `PBS_LANCEDB_PATH` | `<repo>/backend/data/lancedb` |

## Layout

```
src/pbs_mcp/
├── __init__.py
├── server.py                        stdio entry point + 22-tool registration
├── config.py                        path resolution + layered manifest API
├── office_config.py                 office.yaml loader + Pydantic schema
├── office_config_migrations/        v1→v2 forward migrations (in-memory at load)
├── schemas.py                       Pydantic input/output models for all tools
├── embedder.py                      fastembed bge-m3 + bge-reranker-v2-m3
├── db.py                            LanceDB wrapper + filter language
├── chunkers/                        per-strategy chunker modules (text-window,
│                                    gesetz-paragraph, urteil-randnr, leitfaden-
│                                    section, latex-enumerate, latex-textbaustein,
│                                    pdf-heading, eml, baustein-body)
├── integrations/                    Integration adapters (Backend sub-pattern;
│                                    phone/accounting; protocol.py + none.py
│                                    each — concrete adapters land per demand)
└── tools/
    ├── corpus.py                    search_corpus, read_corpus_file, ingest_paths
    ├── ingest.py                    ingest_project_inputs, search_inputs
    ├── memory.py                    list/get/save/flag/archive_baustein,
    │                                find_bausteine_by_reference
    ├── projects.py                  list/bind/setup_project, scaffold_project
    ├── build.py                     compile_latex
    ├── survey.py                    survey_project (file clustering)
    └── discovery.py                 Tier 1: list_skills, list_*_manifests,
                                     list_skeletons, list_bausteine
```

## Status

22 MCP tools registered + handlers wired. Pre-RAG state: corpus
search/ingest/embedding works for text. Multimodal (OCR, ColPali,
image retrieval) + legal-§-graph + new chunking strategy
(`per-section-with-paragraph-subchunks`) are Phase 2a/3a per
`docs/rag-pipeline-decisions.md`. Conventions for backend Python
(test layout, logging, MCP error format) at
`docs/backend-conventions.md`.
