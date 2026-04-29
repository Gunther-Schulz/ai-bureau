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
    GetProjectStateInput,
    IngestPathsInput,
    IngestProjectInputsInput,
    ListBausteineInput,
    ListDoctypesManifestsInput,
    ListProjectsInput,
    ListReferenceManifestsInput,
    ListSkeletonsInput,
    ListSkillsInput,
    QueryAuditTrailInput,
    ReadCorpusFileInput,
    RecordAuditEventInput,
    SaveBausteinInput,
    ScaffoldProjectInput,
    SearchCorpusInput,
    SearchInputsInput,
    SetupProjectInput,
    SurveyProjectInput,
    UnbindProjectInput,
    UpdateProjectStateInput,
    ValidateSkillOutputInput,
)
from pbs_mcp.tools import audit, build, corpus, discovery, ingest, memory, projects, sparring

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
    "setup_project": (SetupProjectInput, projects.setup_project),
    "get_project_state": (GetProjectStateInput, projects.get_project_state),
    "update_project_state": (UpdateProjectStateInput, projects.update_project_state),
    # Audit trail (per docs/decisions/audit-trail-v1.md)
    "record_audit_event": (RecordAuditEventInput, audit.record_audit_event),
    "query_audit_trail": (QueryAuditTrailInput, audit.query_audit_trail),
    # Sparring-output validation (per docs/decisions/sparring-output-v1.md)
    "validate_skill_output": (ValidateSkillOutputInput, sparring.validate_skill_output),
    # Build
    "compile_latex": (CompileLatexInput, build.compile_latex),
    "scaffold_project": (ScaffoldProjectInput, build.scaffold_project),
    # Discovery (Tier 1, pre-RAG; per ROADMAP "Backend MCP discovery layer")
    "list_reference_manifests": (ListReferenceManifestsInput, discovery.list_reference_manifests),
    "list_doctypes_manifests": (ListDoctypesManifestsInput, discovery.list_doctypes_manifests),
    "list_skills": (ListSkillsInput, discovery.list_skills),
    "list_skeletons": (ListSkeletonsInput, discovery.list_skeletons),
}


# === Tool descriptions for list_tools ===

TOOL_DESCRIPTIONS: dict[str, str] = {
    "search_corpus": "Hybrid search (vector + BM25 + reranker) across the indexed corpus. Returns top-k chunks with metadata. Filter by source_type, project, doctype, etc.",
    "read_corpus_file": "Read full content of a file. Supports PDF extraction. Optional offset/limit slicing.",
    "ingest_paths": "Index file paths into LanceDB with embeddings. Selects chunker per source type. force=true re-indexes existing.",
    "ingest_project_inputs": "Project-namespaced ingestion of source materials. Wraps ingest_paths with project + artifact_kind=input metadata.",
    "search_inputs": "Search a single project's namespaced input documents only.",
    "list_bausteine": "List bausteine matching scope (universal/domain/state/project) + scope_key + project_root + status filters.",
    "get_baustein": "Fetch a baustein by name. Increments use_count and updates last_used.",
    "save_baustein": "Write a new baustein with full frontmatter (defaults applied). Uses the canonical format spec.",
    "flag_baustein": "Mark a baustein as flagged with a reason (e.g. citation drift, rejection feedback).",
    "archive_baustein": "Archive a baustein, optionally pointing at a successor.",
    "find_bausteine_by_reference": "Find bausteine whose references[] mention a given law/paragraph/ruling/leitfaden.",
    "list_projects": "List bound projects from the office projects-index.",
    "bind_project": "Register a project; creates _ai/state.md if absent. Adds to projects-index.",
    "unbind_project": "Delete a project's namespaced chunks; optionally remove from index.",
    "survey_project": "Lightweight clustering of files in a project root by likely role.",
    "setup_project": "Create / initialize / bind a project — single entry point for new project work. Mode auto-detected from target_root state. Generates folder name from conventions.project_naming, scaffolds layout per conventions.project_folder_layout, copies skeletons for chosen doctypes, seeds .ai/state.md, adds to projects-index.",
    "get_project_state": "Read + validate a project's state.md. Returns the typed frontmatter dict + raw markdown body. Raises ValidationError on contract violation; never returns partial data. State.md is schema-bearing per ARCHITECTURE.md meta-rule 4 — skills must use this gate, not direct Read.",
    "update_project_state": "Apply a partial update to a project's state.md frontmatter (merged over current values), optionally append text to History body. Re-validates the merged state; raises if the update would violate the contract (lifecycle/phase consistency, date order, required fields). Never writes a partially-invalid state.",
    "record_audit_event": "Append a single audit event to a project's audit-trail.jsonl. Server-fills id (UUID) + timestamp (UTC) when caller supplies empties. Validates AuditEvent contract; required: kind, summary, sources[]. Used by every event-producing skill (orchestrator, save-baustein, record-feedback, draft skills) per dual-write discipline. See docs/decisions/audit-trail-v1.md.",
    "query_audit_trail": "Filter the unified audit trail across one or all bound projects. AND-combined filters: project, kind, since/until, actor, references_paragraph, references_baustein. Returns events sorted by timestamp descending. Used to answer 'what happened with §X between dates Y and Z' queries; the canonical defensibility-test entry point per VISION axis 3.",
    "validate_skill_output": "Validate a sparring-mode skill output (text) against the skill's declared output_schema (per pbs_mcp/skill_outputs/SCHEMA_REGISTRY). Returns valid + extracted fields, or missing_fields + weak_fields + suggestions. Used by orchestrator after Phase B review and Checkpoint-13 recommendation outputs to enforce structural sparring-output shape (counter-argument, confidence, reasoning, etc.). See docs/decisions/sparring-output-v1.md.",
    "compile_latex": "Run latexmk (or pdflatex) on a LaTeX project. Returns PDF path, log excerpt, warnings, errors, page count.",
    "scaffold_project": "Copy a template tree to a new project root. Patches Projektdaten.tex with provided values. git inits for Overleaf.",
    "list_reference_manifests": "List references-manifests in scope (default: only those active per office's scope.{domains,states}; pass scope_filter=false for full union). Returns layer/scope_key/path/entry_count/last_updated per manifest.",
    "list_doctypes_manifests": "List doctypes-manifests in scope (same shape as list_reference_manifests). Default scope-filtered.",
    "list_skills": "Enumerate plugin/skills/*/SKILL.md, returning name/version/description/path + frontmatter dependency declarations (mcp_tools_required, mcp_tools_optional, fallback_when_mcp_absent).",
    "list_skeletons": "For a given doctype, return the layered skeleton dir set: universal layer + per-active-domain overlays. Used by setup_project for layered scaffold composition.",
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
