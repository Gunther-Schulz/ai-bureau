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
├── server.py            stdio entry point, tool registration
├── config.py            path resolution
├── embedder.py          fastembed wrapper (TBD)
├── db.py                lancedb wrapper (TBD)
└── tools/
    ├── corpus.py        search_corpus, read_corpus_file (TBD)
    ├── ingest.py        ingest_paths, search_inputs (TBD)
    ├── memory.py        list/get/save_baustein (TBD)
    ├── projects.py      list/bind/survey_project (TBD)
    └── build.py         compile_latex, scaffold_project (TBD)
```

## Status

v0.1 — scaffolding only. Tool implementations to follow.
