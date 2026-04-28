"""Office configuration loader.

Resolves and validates the per-deployment `office-config.yaml`. Every
office-specific value (paths, identity, practices, scope, LaTeX styling,
manifest extensions, integrations) is read through this module — never
hardcoded elsewhere.

Resolution order:
1. $PBS_OFFICE_CONFIG (explicit path)
2. ${XDG_CONFIG_HOME:-$HOME/.config}/pbs-bureau/office.yaml

Schema reference: docs/office-config.schema.yaml at the repo root.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator


CURRENT_SCHEMA_VERSION = 2


class Practice(BaseModel):
    """An internal sub-practice of THIS office."""
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    signer: str | None = None
    email: str | None = None
    email_match_patterns: list[str] = Field(default_factory=list)


class Partner(BaseModel):
    """An external collaborator the office regularly works with."""
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    signer: str | None = None
    specialization: str | None = None
    email: str | None = None
    email_match_patterns: list[str] = Field(default_factory=list)
    phone: str | None = None
    web: str | None = None


class Identity(BaseModel):
    address_lines: list[str] = Field(..., min_length=1)
    signature_block: str = Field(..., min_length=1)
    title: str | None = None
    phone: str | None = None
    mobile: str | None = None
    fax: str | None = None
    email: str | None = None
    web: str | None = None
    specializations: list[str] = Field(default_factory=list)
    logo_path: Path | None = None
    signature_image_path: Path | None = None

    @field_validator("logo_path", "signature_image_path", mode="before")
    @classmethod
    def _expand(cls, v):
        if v is None:
            return v
        return Path(os.path.expandvars(str(v))).expanduser()


StateCode = Literal[
    "BB", "BW", "BY", "BE", "HB", "HH", "HE", "MV",
    "NI", "NW", "RP", "SH", "SL", "SN", "ST", "TH",
]


class Office(BaseModel):
    name: str = Field(..., min_length=1)
    short: str = Field(..., min_length=1)
    language: Literal["de_DE"] = "de_DE"


class Paths(BaseModel):
    state_root: Path
    references_root: Path
    projects_root: Path
    local_repos_root: Path | None = None

    @field_validator("state_root", "references_root", "projects_root", "local_repos_root", mode="before")
    @classmethod
    def _expand(cls, v):
        if v is None:
            return v
        return Path(os.path.expandvars(str(v))).expanduser()


class Scope(BaseModel):
    """Which planning domains and Bundesländer this office operates in.

    Drives layered manifest resolution: the loader walks the universal
    manifest plus the domain[X] manifest for each X in scope.domains plus
    the state[X] manifest for each X in scope.states.

    Empty domains/states is legal — an office may run on universal-only
    content (rare, used during initial setup).
    """
    domains: list[str] = Field(default_factory=list)
    states: list[StateCode] = Field(default_factory=list)


def _expand_path_dict(v: Any) -> dict:
    if not isinstance(v, dict):
        return v
    return {
        k: Path(os.path.expandvars(str(p))).expanduser() if p is not None else None
        for k, p in v.items()
    }


class ManifestMap(BaseModel):
    """A layered manifest map: universal + domain[X] + state[X].

    Used for both references-manifest and doctypes-manifest. Domain and
    state keys are expected to match the office's scope.{domains,states}
    selection but extras don't error (they just won't be loaded).
    """
    universal: Path | None = None
    domain: dict[str, Path] = Field(default_factory=dict)
    state: dict[str, Path] = Field(default_factory=dict)

    @field_validator("universal", mode="before")
    @classmethod
    def _expand_universal(cls, v):
        if v is None:
            return v
        return Path(os.path.expandvars(str(v))).expanduser()

    @field_validator("domain", "state", mode="before")
    @classmethod
    def _expand_paths(cls, v):
        return _expand_path_dict(v)


class Extensions(BaseModel):
    """Layered manifest extensions: references + doctypes per scope axis.

    The universal layer ships with the app and applies to every deployment.
    Domain layers ship with the app under extensions/domain/<X>/ and are
    selected via scope.domains. State layers ship with the app under
    extensions/state/<X>/ for canonical state-law content; offices may
    register additional state overrides under their own state_root.
    """
    references_manifests: ManifestMap = Field(default_factory=ManifestMap)
    doctypes_manifests: ManifestMap = Field(default_factory=ManifestMap)


class IntegrationConfig(BaseModel):
    """A single integration adapter declaration.

    `adapter` selects which Python module under
    backend/.../integrations/<class>/<adapter>.py implements this
    integration class. `none` is the default no-op adapter.
    """
    adapter: str = "none"
    config: dict[str, Any] = Field(default_factory=dict)


class Integrations(BaseModel):
    """Pluggable integration adapters declared at office setup.

    Each integration class is independently swappable: an office on
    Thunderbird picks `email.adapter: thunderbird-maildir`; an office on
    IMAP picks `email.adapter: imap`. Adapters live as Python modules
    under backend/.../integrations/<class>/<adapter>.py implementing a
    small protocol.

    All defaults to `none` (no-op). Real adapters land in v1.x+.
    """
    email: IntegrationConfig = Field(default_factory=IntegrationConfig)
    calendar: IntegrationConfig = Field(default_factory=IntegrationConfig)
    scanner: IntegrationConfig = Field(default_factory=IntegrationConfig)
    phone: IntegrationConfig = Field(default_factory=IntegrationConfig)
    accounting: IntegrationConfig = Field(default_factory=IntegrationConfig)


class Templates(BaseModel):
    skeleton_source: str = "app"
    office_style_dir: Path | None = None
    identity_macros: str = "auto"
    doctype_overrides: dict[str, Path] = Field(default_factory=dict)

    @field_validator("office_style_dir", mode="before")
    @classmethod
    def _expand(cls, v):
        if v is None:
            return v
        return Path(os.path.expandvars(str(v))).expanduser()


class FolderLayout(BaseModel):
    inputs: str = "inputs/"
    sent_versions: str = "Auslieferung/"
    correspondence: str = "Schriftverkehr/"
    toeb: str = "TöB/"


class ProjectNumbering(BaseModel):
    pattern: Literal["YY-NN", "YYYY-NN", "NN", "YY/NN"] = "YY-NN"
    auto_increment: bool = True


class Conventions(BaseModel):
    project_naming: str = "{year_2}-{nr} {client} - {location}"
    project_numbering: ProjectNumbering = Field(default_factory=ProjectNumbering)
    project_folder_layout: FolderLayout = Field(default_factory=FolderLayout)


class OfficeConfig(BaseModel):
    schema_version: int
    office: Office
    identity: Identity
    practices: list[Practice] = Field(..., min_length=1)
    partners: list[Partner] = Field(default_factory=list)
    paths: Paths
    scope: Scope = Field(default_factory=Scope)
    extensions: Extensions = Field(default_factory=Extensions)
    integrations: Integrations = Field(default_factory=Integrations)
    templates: Templates = Field(default_factory=Templates)
    conventions: Conventions = Field(default_factory=Conventions)

    def find_partner_by_email(self, email: str) -> Partner | None:
        """Match an incoming email address against partner patterns."""
        import fnmatch
        for p in self.partners:
            if p.email and p.email.lower() == email.lower():
                return p
            for pattern in p.email_match_patterns:
                if fnmatch.fnmatch(email.lower(), pattern.lower()):
                    return p
        return None

    @model_validator(mode="after")
    def _resolve_template_defaults(self) -> "OfficeConfig":
        if self.templates.office_style_dir is None:
            self.templates.office_style_dir = self.paths.state_root / "templates"
        return self

    def all_references_manifests(self) -> list[Path]:
        """All reference manifests this office has selected, in load order.

        Universal first, then per-domain (in scope.domains order), then
        per-state (in scope.states order). Files that don't exist are
        silently skipped — the loader logs which were found.
        """
        return self._collect_manifests(self.extensions.references_manifests)

    def all_doctypes_manifests(self) -> list[Path]:
        """All doctype manifests this office has selected, in load order."""
        return self._collect_manifests(self.extensions.doctypes_manifests)

    def _collect_manifests(self, mmap: ManifestMap) -> list[Path]:
        out: list[Path] = []
        if mmap.universal is not None and mmap.universal.is_file():
            out.append(mmap.universal)
        for domain_key in self.scope.domains:
            p = mmap.domain.get(domain_key)
            if p is not None and p.is_file():
                out.append(p)
        for state_key in self.scope.states:
            p = mmap.state.get(state_key)
            if p is not None and p.is_file():
                out.append(p)
        return out

    @model_validator(mode="after")
    def _check_schema_version(self) -> "OfficeConfig":
        if self.schema_version > CURRENT_SCHEMA_VERSION:
            raise ValueError(
                f"office-config schema_version {self.schema_version} is newer than "
                f"this binary supports ({CURRENT_SCHEMA_VERSION}). Upgrade the app."
            )
        return self

    def default_practice(self) -> Practice:
        return self.practices[0]


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
