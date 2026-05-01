"""Strict Pydantic base for contract-bearing models.

Per ARCHITECTURE.md meta-rule 4 strict-validation discipline:
contract-bearing models reject unknown fields rather than silently
ignoring them. Pydantic v2's default `extra="ignore"` is too lax for
this purpose — typos and schema drift would slip through silently.

Use `StrictModel` as the base for any model that owns a typed
contract enforced at a system boundary (file load, tool I/O across
trust boundary, schema-bearing entity persistence).

Do NOT use for purely-internal models or MCP I/O wrappers where the
MCP protocol already validates shape at the JSON level — that would
be redundant ceremony.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """Pydantic base with `extra="forbid"`. Unknown fields raise
    ValidationError at parse time rather than being silently dropped."""
    model_config = ConfigDict(extra="forbid")
