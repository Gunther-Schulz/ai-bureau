"""Office configuration loader.

Resolves and validates the per-deployment `office-config.yaml`. Every
office-specific value (paths, identity, practices, LaTeX styling,
state-law extensions) is read through this module — never hardcoded
elsewhere.

Resolution order:
1. $PBS_OFFICE_CONFIG (explicit path)
2. ${XDG_CONFIG_HOME:-$HOME/.config}/pbs-bureau/office.yaml

Schema reference: docs/office-config.schema.yaml at the repo root.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator


CURRENT_SCHEMA_VERSION = 1


class Practice(BaseModel):
    """An internal sub-practice of THIS office.

    Most offices have a single practice (themselves). Multi-practice
    setups exist for offices internally divided into specialized
    sub-units (e.g. text/planning + GIS as separate departments
    within the same legal entity).
    """
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    signer: str | None = None
    email: str | None = None
    email_match_patterns: list[str] = Field(default_factory=list)


class Partner(BaseModel):
    """An external collaborator the office regularly works with.

    Different from Practice: a partner is its own legal entity with
    its own email/identity. May appear on projects either as a
    co-producer (`state.md.partners: [hendrik]`) or as the client
    (`state.md.client: Hendrik`).

    `email_match_patterns` accept fnmatch-style wildcards (`*@domain`)
    used by the email integration to associate incoming messages
    with this partner.
    """
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    signer: str | None = None
    specialization: str | None = None     # e.g. "Landschaftsökologie"
    email: str | None = None
    email_match_patterns: list[str] = Field(default_factory=list)
    phone: str | None = None
    web: str | None = None


class Identity(BaseModel):
    address_lines: list[str] = Field(..., min_length=1)
    signature_block: str = Field(..., min_length=1)
    title: str | None = None              # e.g. "Dipl.-Ing."
    phone: str | None = None
    mobile: str | None = None             # separate Funk/Mobile field
    fax: str | None = None
    email: str | None = None
    web: str | None = None
    specializations: list[str] = Field(default_factory=list)
                                          # disciplines listed on letterhead
    logo_path: Path | None = None         # path to office logo image
    signature_image_path: Path | None = None
                                          # scanned signature for signed PDFs

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


class Extensions(BaseModel):
    """Reference-manifest extensions, keyed by Bundesland code.

    State is purely per-project (in `state.md.bundesland`); the office
    has no state of its own. The map registers which state extensions
    have been provisioned in this deployment. When a project's
    bundesland is set, skills look up the matching key here. Missing
    keys → research-references is suggested.
    """
    references_manifests: dict[StateCode, Path] = Field(default_factory=dict)

    @field_validator("references_manifests", mode="before")
    @classmethod
    def _expand_paths(cls, v):
        if not isinstance(v, dict):
            return v
        return {
            k: Path(os.path.expandvars(str(p))).expanduser()
            for k, p in v.items()
        }


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
    extensions: Extensions = Field(default_factory=Extensions)
    templates: Templates = Field(default_factory=Templates)
    conventions: Conventions = Field(default_factory=Conventions)

    def find_partner_by_email(self, email: str) -> Partner | None:
        """Match an incoming email address against partner patterns.

        Uses fnmatch-style wildcards. Returns the first matching
        partner; partners are scanned in declaration order.
        """
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

    def references_manifest_for_state(self, bundesland: StateCode) -> Path | None:
        """Resolve the extension manifest for a project's Bundesland.

        Falls back to the conventional default location
        `<state_root>/extensions/<state>/references-manifest.yaml` if
        no explicit override is registered.
        """
        explicit = self.extensions.references_manifests.get(bundesland)
        if explicit is not None:
            return explicit if explicit.is_file() else None
        default = (
            self.paths.state_root / "extensions" / bundesland
            / "references-manifest.yaml"
        )
        return default if default.is_file() else None

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
    """Load + validate the office config. Cached for the process lifetime."""
    path = discover_path()
    if path is None:
        searched = "\n  ".join(str(p) for p in _candidate_paths())
        raise OfficeConfigNotFoundError(
            "No office-config.yaml found. Run the `setup-office` skill, or set "
            "$PBS_OFFICE_CONFIG. Searched:\n  " + searched
        )

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    return OfficeConfig.model_validate(data)


def reset_cache() -> None:
    """Forget cached config; next load() re-reads from disk."""
    load.cache_clear()
