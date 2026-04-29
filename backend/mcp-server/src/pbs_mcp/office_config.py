"""Office configuration loader.

Resolves and validates the per-deployment `office-config.yaml`. Every
office-specific value (paths, identity, actors, scope, LaTeX styling,
integrations) is read through this module — never hardcoded elsewhere.

Resolution order:
1. $PBS_OFFICE_CONFIG (explicit path)
2. ${XDG_CONFIG_HOME:-$HOME/.config}/pbs-bureau/office.yaml

Schema reference: docs/office-config.schema.yaml at the repo root.

Schema v3 (post-design-review session 5) consolidates the v2 split
between `office`/`identity`/`paths`/`practices`/`partners` into a
flatter shape: `office` (all identity fields), `actors[]` (with
`kind: internal|external` discriminator), `roots:` (one block for
all filesystem paths). Manifests are no longer stored in the config
— they're discovered by walking the repo `extensions/` tree filtered
by scope (see config.all_*_manifests).
"""
from __future__ import annotations

import fnmatch
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


CURRENT_SCHEMA_VERSION = 3


# === Office identity (merged from v2's office + identity) ================

class Office(BaseModel):
    """Office identity. v3 merges v2's `office` + `identity` into one block."""
    name: str = Field(..., min_length=1)
    short: str = Field(..., min_length=1)
    language: Literal["de_DE"] = "de_DE"
    title: str | None = None
    address_lines: list[str] = Field(..., min_length=1)
    phone: str | None = None
    mobile: str | None = None
    fax: str | None = None
    email: str | None = None
    web: str | None = None
    specializations: list[str] = Field(default_factory=list)
    logo_path: Path | None = None
    signature_image_path: Path | None = None
    signature_block: str = Field(..., min_length=1)

    @field_validator("logo_path", "signature_image_path", mode="before")
    @classmethod
    def _expand(cls, v):
        if v is None:
            return v
        return Path(os.path.expandvars(str(v))).expanduser()


# === Actors (merged from v2's practices + partners) ======================

class Actor(BaseModel):
    """A signing entity — internal practice or external partner.

    v3 merges v2's `practices[]` and `partners[]` into a single
    `actors[]` list discriminated by `kind`. Email-routing logic is
    now uniform across kinds.
    """
    id: str = Field(..., min_length=1)
    kind: Literal["internal", "external"]
    label: str = Field(..., min_length=1)
    signer: str | None = None
    specialization: str | None = None
    email: str | None = None
    email_match_patterns: list[str] = Field(default_factory=list)
    phone: str | None = None
    web: str | None = None


# === Roots (merged from v2's paths + templates.office_style_dir) =========

class Roots(BaseModel):
    """All filesystem roots in one block. v3 consolidates v2's `paths` +
    `templates.office_style_dir` into a single section.
    """
    state: Path
    references: Path
    projects: Path
    local_repos: Path | None = None
    office_style_dir: Path | None = None  # default: state/templates/
    office_extensions: Path | None = None  # office-local extensions tree (mirrors <repo>/extensions/<scope>/)

    @field_validator(
        "state", "references", "projects",
        "local_repos", "office_style_dir", "office_extensions",
        mode="before",
    )
    @classmethod
    def _expand(cls, v):
        if v is None:
            return v
        return Path(os.path.expandvars(str(v))).expanduser()


# === Scope ===============================================================

StateCode = Literal[
    "BB", "BW", "BY", "BE", "HB", "HH", "HE", "MV",
    "NI", "NW", "RP", "SH", "SL", "SN", "ST", "TH",
]


class Scope(BaseModel):
    """Which planning domains and Bundesländer this office operates in.

    Drives layered manifest resolution (see config.all_references_manifests
    + config.all_doctypes_manifests, which walk <repo>/extensions/
    filtered by this scope).
    """
    domains: list[str] = Field(default_factory=list)
    states: list[StateCode] = Field(default_factory=list)


# === Integrations (free-form list, v3) ===================================

class Integration(BaseModel):
    """One integration declaration in the integrations list.

    v3 removes the fixed-key map (email/calendar/scanner/phone/accounting)
    in favor of a free-form list. Any class string is valid; the adapter
    is resolved dynamically from `pbs_mcp.integrations.<class>.<adapter>`.
    """
    model_config = ConfigDict(populate_by_name=True)

    cls: str = Field(..., alias="class", min_length=1)  # `class` is reserved in Python
    adapter: str = "none"
    config: dict[str, Any] = Field(default_factory=dict)


# === Templates ===========================================================

class Templates(BaseModel):
    """LaTeX template configuration. v3 removes office_style_dir
    (consolidated into Roots).
    """
    skeleton_source: str = "app"
    identity_macros: str = "auto"
    doctype_overrides: dict[str, Path] = Field(default_factory=dict)


# === Conventions =========================================================

class FolderLayout(BaseModel):
    inputs: str = "inputs/"
    sent_versions: str = "Auslieferung/"
    correspondence: str = "Schriftverkehr/"
    toeb: str = "TöB/"


class ProjectNumbering(BaseModel):
    pattern: Literal["YY-NN", "YYYY-NN", "NN", "YY/NN"] = "YY-NN"
    auto_increment: bool = True


class PathClassification(BaseModel):
    """Optional per-source-type substring patterns that classify a path
    into a subtype.

    Schema: `{<source_type>: {<subtype>: [<substring-pattern>, ...]}}`.
    Source-types: `corpus`, `reference`, `baustein`. Subtype keys are
    free-form (consumers in `tools/ingest.py:_infer_source_subtype`
    expect known values per source-type, but the classifier accepts any
    declared subtype). Patterns are checked case-insensitively as
    substrings of the lowercased path.

    When absent (default), `_infer_source_subtype` falls back to
    hardcoded patterns for the canonical folder layout
    (`_ai/snapshots/`, `gesetze/bund/`, `bausteine/universal/`, etc.).
    Override here for offices whose folder names differ — partial
    override is supported (config rules tried first, hardcoded
    fallback applies for unmatched paths).

    Within each source-type, subtypes are tried in YAML-declared
    order (Python dicts preserve insertion order); first matching
    pattern wins. Order matters when one subtype's pattern is a
    superset of another's (e.g., `gesetz-state: [/gesetze/]` would
    swallow `gesetz-bund: [/gesetze/bund/]` if listed first).
    """
    corpus: dict[str, list[str]] = Field(default_factory=dict)
    reference: dict[str, list[str]] = Field(default_factory=dict)
    baustein: dict[str, list[str]] = Field(default_factory=dict)


class Conventions(BaseModel):
    project_naming: str = "{year_2}-{nr} {client} - {location}"
    project_numbering: ProjectNumbering = Field(default_factory=ProjectNumbering)
    project_folder_layout: FolderLayout = Field(default_factory=FolderLayout)
    path_classification: PathClassification = Field(default_factory=PathClassification)


# === Top-level OfficeConfig ==============================================

class OfficeConfig(BaseModel):
    schema_version: int
    office: Office
    actors: list[Actor] = Field(..., min_length=1)
    roots: Roots
    scope: Scope = Field(default_factory=Scope)
    integrations: list[Integration] = Field(default_factory=list)
    templates: Templates = Field(default_factory=Templates)
    conventions: Conventions = Field(default_factory=Conventions)

    def find_actor_by_email(self, email: str) -> Actor | None:
        """Match an incoming email address against actor patterns. Returns
        first match across all kinds (internal + external)."""
        e = email.lower()
        for a in self.actors:
            if a.email and a.email.lower() == e:
                return a
            for pattern in a.email_match_patterns:
                if fnmatch.fnmatch(e, pattern.lower()):
                    return a
        return None

    def default_internal_actor(self) -> Actor:
        """Return the first internal actor (canonical signer / practice)."""
        for a in self.actors:
            if a.kind == "internal":
                return a
        raise ValueError("office-config has no internal actor declared")

    def find_integration(self, class_name: str) -> Integration | None:
        """Find the configured integration for a class, or None if absent."""
        for i in self.integrations:
            if i.cls == class_name:
                return i
        return None

    @model_validator(mode="after")
    def _resolve_template_defaults(self) -> "OfficeConfig":
        """Default office_style_dir to <state>/templates/ when not set."""
        if self.roots.office_style_dir is None:
            self.roots.office_style_dir = self.roots.state / "templates"
        return self

    @model_validator(mode="after")
    def _check_at_least_one_internal_actor(self) -> "OfficeConfig":
        if not any(a.kind == "internal" for a in self.actors):
            raise ValueError(
                "office-config must declare at least one actor with kind='internal'"
            )
        return self

    @model_validator(mode="after")
    def _check_schema_version(self) -> "OfficeConfig":
        if self.schema_version > CURRENT_SCHEMA_VERSION:
            raise ValueError(
                f"office-config schema_version {self.schema_version} is newer than "
                f"this binary supports ({CURRENT_SCHEMA_VERSION}). Upgrade the app."
            )
        return self


# === Loader ==============================================================

class OfficeConfigNotFoundError(RuntimeError):
    """Raised when no office-config.yaml can be located."""


def _candidate_paths() -> list[Path]:
    paths: list[Path] = []
    if env := os.getenv("PBS_OFFICE_CONFIG"):
        paths.append(Path(env).expanduser())

    xdg = os.getenv("XDG_CONFIG_HOME")
    if xdg:
        paths.append(Path(xdg).expanduser() / "pbs-bureau" / "office.yaml")
    paths.append(Path.home() / ".config" / "pbs-bureau" / "office.yaml")
    return paths


def discover_path() -> Path | None:
    """Return the resolved office-config path, or None if absent."""
    for p in _candidate_paths():
        if p.is_file():
            return p
    return None


@lru_cache(maxsize=1)
def load() -> OfficeConfig:
    """Load + validate the office config. Cached for the process lifetime.

    Applies any pending schema migrations (in-memory only) before validation.
    The on-disk file is migrated by the `setup-office` skill, not silently
    here — the loader rejects on-disk versions newer than CURRENT but does
    forward-migrate older versions in memory so the tools keep working
    until the user re-runs setup-office.
    """
    path = discover_path()
    if path is None:
        searched = "\n  ".join(str(p) for p in _candidate_paths())
        raise OfficeConfigNotFoundError(
            "No office-config.yaml found. Run the `setup-office` skill, or set "
            "$PBS_OFFICE_CONFIG. Searched:\n  " + searched
        )

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    data = _migrate(data)
    return OfficeConfig.model_validate(data)


def _migrate(data: dict) -> dict:
    """Apply schema migrations sequentially up to CURRENT_SCHEMA_VERSION."""
    from pbs_mcp.office_config_migrations import apply_migrations
    return apply_migrations(data, target=CURRENT_SCHEMA_VERSION)


def reset_cache() -> None:
    """Forget cached config; next load() re-reads from disk."""
    load.cache_clear()
