"""Pydantic models for MCP tool input/output.

One model class per tool, paired Input/Output. Used by server.py
when registering tools — Pydantic gives us validation + JSON schema
generation for the MCP protocol layer.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

# === Common types ===

SourceType = Literal["corpus", "reference", "baustein"]
SourceSubtype = Literal[
    # corpus
    "local-repo", "project-folder", "snapshot", "correspondence", "external",
    # reference
    "gesetz-bund", "gesetz-eu", "gesetz-state", "leitfaden",
    "urteil", "beispiel", "methodik",
    # baustein
    "global", "domain", "project",
]


class CorpusHit(BaseModel):
    """Single search result with metadata."""
    content: str
    score: float
    source_type: SourceType
    source_subtype: str | None = None
    source_path: str
    project: str | None = None
    doctype: str | None = None
    section: str | None = None
    paragraph: str | None = None
    reference_id: str | None = None
    tags: list[str] = Field(default_factory=list)
    indexed_at: datetime | None = None


# === Corpus tools ===

class SearchCorpusInput(BaseModel):
    query: str
    k: int = 10
    filter: dict[str, Any] | None = None
    rerank: bool = True


class SearchCorpusOutput(BaseModel):
    hits: list[CorpusHit]
    query: str
    k_returned: int
    used_reranker: bool


class ReadCorpusFileInput(BaseModel):
    path: str
    offset: int | None = None
    limit: int | None = None


class ReadCorpusFileOutput(BaseModel):
    path: str
    content: str
    truncated: bool


# === Ingest tools ===

class IngestPathsInput(BaseModel):
    paths: list[str]
    source_type: SourceType
    force: bool = False
    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class IngestPathsOutput(BaseModel):
    indexed: list[str]
    skipped_unchanged: list[str]
    errors: list[dict[str, str]]
    total_chunks: int


class IngestProjectInputsInput(BaseModel):
    project: str
    paths: list[str]
    project_root: str | None = None


class IngestProjectInputsOutput(BaseModel):
    project: str
    indexed: list[str]
    total_chunks: int
    errors: list[dict[str, str]]


class SearchInputsInput(BaseModel):
    query: str
    project: str
    k: int = 10
    rerank: bool = True


class SearchInputsOutput(BaseModel):
    hits: list[CorpusHit]
    project: str
    k_returned: int


# === Memory tools ===

class ListBausteineInput(BaseModel):
    scope: Literal["global", "domain", "project"] | None = None
    domain: str | None = None
    project: str | None = None
    status: Literal["active", "flagged", "archived", "superseded"] | None = "active"


class BausteinSummary(BaseModel):
    name: str
    scope: str
    domain: str | None
    project: str | None
    type: str
    title: str
    status: str
    use_count: int
    last_used: str | None
    last_validated: str | None
    review_due: str | None
    flagged_reason: str | None
    superseded_by: str | None
    tags: list[str]
    path: str


class ListBausteineOutput(BaseModel):
    bausteine: list[BausteinSummary]
    total: int


class GetBausteinInput(BaseModel):
    name: str
    scope: Literal["global", "domain", "project"] | None = None
    domain: str | None = None
    project: str | None = None


class GetBausteinOutput(BaseModel):
    name: str
    path: str
    frontmatter: dict[str, Any]
    body: str


class SaveBausteinInput(BaseModel):
    name: str
    scope: Literal["global", "domain", "project"]
    domain: str | None = None
    project: str | None = None
    type: str
    title: str
    body: str
    references: list[dict[str, Any]] = Field(default_factory=list)
    source_project: str | None = None
    source_date: str | None = None
    tags: list[str] = Field(default_factory=list)
    overwrite: bool = False


class SaveBausteinOutput(BaseModel):
    name: str
    path: str
    created: bool


class FlagBausteinInput(BaseModel):
    name: str
    reason: str


class FlagBausteinOutput(BaseModel):
    name: str
    path: str
    previous_status: str
    new_status: str = "flagged"


class ArchiveBausteinInput(BaseModel):
    name: str
    superseded_by: str | None = None


class ArchiveBausteinOutput(BaseModel):
    name: str
    path: str
    new_status: str = "archived"


class FindBausteineByReferenceInput(BaseModel):
    law: str | None = None
    paragraph: str | None = None
    ruling: str | None = None
    leitfaden: str | None = None


class FindBausteineByReferenceOutput(BaseModel):
    bausteine: list[BausteinSummary]
    matched_filter: dict[str, str | None]


# === Project tools ===

class ListProjectsInput(BaseModel):
    state: str | None = None
    practice: str | None = None


class ProjectSummary(BaseModel):
    name: str
    project_root: str
    client: str | None
    location: str | None
    lifecycle: str
    practices: list[str]
    last_session: str | None
    deadlines: list[dict[str, str]] = Field(default_factory=list)


class ListProjectsOutput(BaseModel):
    projects: list[ProjectSummary]
    total: int


class BindProjectInput(BaseModel):
    name: str
    root_path: str | None = None


class BindProjectOutput(BaseModel):
    name: str
    project_root: str
    state_path: str
    created: bool


class UnbindProjectInput(BaseModel):
    name: str
    keep_index_entry: bool = True


class UnbindProjectOutput(BaseModel):
    name: str
    chunks_deleted: int
    index_entry_kept: bool


class SurveyProjectInput(BaseModel):
    project: str
    project_root: str | None = None


class SurveyProjectOutput(BaseModel):
    project: str
    clusters: dict[str, list[str]]
    proposed_state: dict[str, Any]
    proposed_file_map: str


# === Build tools ===

class CompileLatexInput(BaseModel):
    project_path: str
    master_file: str | None = None  # auto-detected if None


class CompileLatexOutput(BaseModel):
    success: bool
    pdf_path: str | None
    log_excerpt: str
    warnings: list[str]
    errors: list[str]
    page_count: int | None


class ScaffoldProjectInput(BaseModel):
    name: str
    doctype: str
    target_root: str
    template_repo: str | None = None
    git_init_latex: bool = True
    project_data: dict[str, Any] = Field(default_factory=dict)


class ScaffoldProjectOutput(BaseModel):
    name: str
    project_root: str
    created_paths: list[str]
    git_repos_initialized: list[str]


class SetupProjectInput(BaseModel):
    """Input for the setup_project tool — single entry point for new
    project work.

    Mode is auto-detected from `target_root` (when set) or generated
    via `office_config.conventions.project_naming` from the metadata
    fields. Three modes:

      - absent      → folder doesn't exist → create + scaffold
      - empty       → folder exists, near-empty → scaffold inside
      - populated   → folder has content → fall back to survey + bind

    Required for create/initialize: client, location, doctypes,
    practice. Required for bind-fallback: target_root with project name.
    """
    name: str | None = None       # explicit project name; else generated
    client: str | None = None
    location: str | None = None
    project_number: str | None = None  # explicit; else auto-incremented
    doctypes: list[str] = Field(default_factory=list)
    practice: str | None = None   # practice id; else first from office config
    target_root: str | None = None  # explicit path; else under projects_root
    project_data: dict[str, Any] = Field(default_factory=dict)
    git_init_latex: bool = False  # initialize git repo per doctype subfolder


class SetupProjectOutput(BaseModel):
    name: str
    project_root: str
    mode: Literal["created", "initialized", "bound"]
    created_paths: list[str]
    doctypes_scaffolded: list[str]
    state_path: str
    index_entry_added: bool
    next_steps: list[str]
