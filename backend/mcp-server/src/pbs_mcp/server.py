"""MCP stdio server — entry point for the pbs-bureau backend.

Spawned by Claude Code via the .mcp.json registration. Communicates
over stdio with the MCP protocol. All tool surface registered here;
implementations live in pbs_mcp.tools.*.
"""
from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from pbs_mcp.schemas import (
    ArchiveBausteinInput,
    BindProjectInput,
    CompileLatexInput,
    FindBausteineByReferenceInput,
    FlagBausteinInput,
    GetBausteinInput,
    IngestPathsInput,
    IngestProjectInputsInput,
    ListBausteineInput,
    ListProjectsInput,
    ReadCorpusFileInput,
    SaveBausteinInput,
    ScaffoldProjectInput,
    SearchCorpusInput,
    SearchInputsInput,
    SurveyProjectInput,
    UnbindProjectInput,
)
from pbs_mcp.tools import build, corpus, ingest, memory, projects

logger = logging.getLogger("pbs_mcp")

server: Server = Server("pbs-mcp")


# === Tool registry ===

TOOL_HANDLERS: dict[str, tuple[type, Any]] = {
    # Corpus
    "search_corpus": (SearchCorpusInput, corpus.search_corpus),
    "read_corpus_file": (ReadCorpusFileInput, corpus.read_corpus_file),
    # Ingest
    "ingest_paths": (IngestPathsInput, ingest.ingest_paths),
    "ingest_project_inputs": (IngestProjectInputsInput, ingest.ingest_project_inputs),
    "search_inputs": (SearchInputsInput, ingest.search_inputs),
    # Memory
    "list_bausteine": (ListBausteineInput, memory.list_bausteine),
    "get_baustein": (GetBausteinInput, memory.get_baustein),
    "save_baustein": (SaveBausteinInput, memory.save_baustein),
    "flag_baustein": (FlagBausteinInput, memory.flag_baustein),
    "archive_baustein": (ArchiveBausteinInput, memory.archive_baustein),
    "find_bausteine_by_reference": (FindBausteineByReferenceInput, memory.find_bausteine_by_reference),
    # Projects
    "list_projects": (ListProjectsInput, projects.list_projects),
    "bind_project": (BindProjectInput, projects.bind_project),
    "unbind_project": (UnbindProjectInput, projects.unbind_project),
    "survey_project": (SurveyProjectInput, projects.survey_project),
    # Build
    "compile_latex": (CompileLatexInput, build.compile_latex),
    "scaffold_project": (ScaffoldProjectInput, build.scaffold_project),
}


# === Tool descriptions for list_tools ===

TOOL_DESCRIPTIONS: dict[str, str] = {
    "search_corpus": "Hybrid search (vector + BM25 + reranker) across the indexed corpus. Returns top-k chunks with metadata. Filter by source_type, project, doctype, etc.",
    "read_corpus_file": "Read full content of a file. Supports PDF extraction. Optional offset/limit slicing.",
    "ingest_paths": "Index file paths into LanceDB with embeddings. Selects chunker per source type. force=true re-indexes existing.",
    "ingest_project_inputs": "Project-namespaced ingestion of source materials. Wraps ingest_paths with project + artifact_kind=input metadata.",
    "search_inputs": "Search a single project's namespaced input documents only.",
    "list_bausteine": "List bausteine matching scope/domain/project/status filters.",
    "get_baustein": "Fetch a baustein by name. Increments use_count and updates last_used.",
    "save_baustein": "Write a new baustein with full frontmatter (defaults applied). Uses the canonical format spec.",
    "flag_baustein": "Mark a baustein as flagged with a reason (e.g. citation drift, rejection feedback).",
    "archive_baustein": "Archive a baustein, optionally pointing at a successor.",
    "find_bausteine_by_reference": "Find bausteine whose references[] mention a given law/paragraph/ruling/leitfaden.",
    "list_projects": "List bound projects from the office projects-index.",
    "bind_project": "Register a project; creates _ai/state.md if absent. Adds to projects-index.",
    "unbind_project": "Delete a project's namespaced chunks; optionally remove from index.",
    "survey_project": "Lightweight clustering of files in a project root by likely role.",
    "compile_latex": "Run latexmk (or pdflatex) on a LaTeX project. Returns PDF path, log excerpt, warnings, errors, page count.",
    "scaffold_project": "Copy a template tree to a new project root. Patches Projektdaten.tex with provided values. git inits for Overleaf.",
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    for name, (input_cls, _) in TOOL_HANDLERS.items():
        schema = input_cls.model_json_schema()
        tools.append(Tool(
            name=name,
            description=TOOL_DESCRIPTIONS.get(name, ""),
            inputSchema=schema,
        ))
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name not in TOOL_HANDLERS:
        raise ValueError(f"unknown tool: {name}")
    input_cls, handler = TOOL_HANDLERS[name]
    try:
        validated = input_cls(**arguments)
    except Exception as e:
        return [TextContent(type="text", text=f"Input validation failed: {e}")]

    try:
        result = await asyncio.to_thread(handler, validated)
    except Exception as e:
        logger.exception(f"tool {name} raised")
        return [TextContent(type="text", text=f"Tool error: {type(e).__name__}: {e}")]

    if hasattr(result, "model_dump"):
        payload = result.model_dump(mode="json")
    else:
        payload = result
    return [TextContent(type="text", text=json.dumps(payload, default=str, ensure_ascii=False, indent=2))]


# === Entry point ===

async def _run() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    logger.info("pbs-mcp starting")
    asyncio.run(_run())


if __name__ == "__main__":
    main()
