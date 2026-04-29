"""MCP tool for sparring-output validation (axis-2 structural promotion).

Per docs/decisions/sparring-output-v1.md. Validates a skill's output
against its declared `output_schema` (looked up via SCHEMA_REGISTRY
in pbs_mcp/skill_outputs/).

V1 minimum: heuristic markdown-section parser extracts schema-declared
fields, then strict Pydantic validation. Skills that produce non-parsing
output get `valid: false` + missing_fields[] + suggestions[]. The full
markdown parser is next-session iteration; this stub returns
`valid: false, schema_name: None` with a clear message when no schema
is registered for the skill.

Strict-validation discipline: parser failures are reported via
weak_fields[]/suggestions[], NOT swallowed; Pydantic validation
errors propagate as parsed-but-invalid (filled missing/weak fields,
not a generic exception).
"""
from __future__ import annotations

import logging
import re
from typing import Any

from pbs_mcp.schemas import ValidateSkillOutputInput, ValidateSkillOutputOutput
from pbs_mcp.skill_outputs import SCHEMA_REGISTRY

logger = logging.getLogger(__name__)


# Common header patterns the heuristic parser recognizes. Skills are
# encouraged (per plugin-conventions.md) to produce output with these
# headers for parse-friendliness.
_FIELD_HEADER_PATTERNS = {
    "counter_argument": [r"##\s+counter[-_ ]?argument", r"\*\*counter[-_ ]?argument\*\*"],
    "confidence": [r"##\s+confidence", r"\*\*confidence\*\*\s*[:=]"],
    "confidence_basis": [r"##\s+confidence[-_ ]?basis", r"\*\*confidence[-_ ]?basis\*\*"],
    "reasoning": [r"##\s+reasoning", r"\*\*reasoning\*\*"],
    "recommendation": [r"##\s+recommendation", r"\*\*recommendation\*\*"],
    "tradeoff": [r"##\s+tradeoff", r"\*\*tradeoff\*\*"],
    "alternative": [r"##\s+alternative", r"\*\*alternative\*\*"],
    "whats_missing": [
        r"##\s+what['ʼ]?s[-_ ]?missing",
        r"\*\*what['ʼ]?s[-_ ]?missing\*\*",
    ],
}


def _extract_field(text: str, field_name: str) -> str | None:
    """Heuristic: find a markdown header matching `field_name` and return
    the text up to the next `## ` header or end-of-text. Returns None if
    no header matches."""
    patterns = _FIELD_HEADER_PATTERNS.get(field_name, [])
    if not patterns:
        return None
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            start = match.end()
            # Find next ## header or **bold**: at start of line; take everything before it
            next_match = re.search(r"\n##\s|\n\*\*\w+\*\*\s*[:=]", text[start:])
            end = start + next_match.start() if next_match else len(text)
            extracted = text[start:end].strip()
            # Strip leading colon (for inline `**Confidence**: high` style)
            extracted = re.sub(r"^[:=]\s*", "", extracted).strip()
            return extracted if extracted else None
    return None


def _parse_output_to_dict(text: str, fields: list[str]) -> dict[str, Any]:
    """Extract each declared field from text via heuristic header match."""
    parsed: dict[str, Any] = {}
    for field in fields:
        value = _extract_field(text, field)
        if value is not None:
            parsed[field] = value
    return parsed


def validate_skill_output(input: ValidateSkillOutputInput) -> ValidateSkillOutputOutput:
    """Validate a skill's output against its declared output_schema.

    V1 minimum: heuristic markdown parser + strict Pydantic validation.
    Returns either valid=true OR valid=false with explicit
    missing_fields/weak_fields/suggestions. Never raises (validation
    errors are converted to structured findings; the gate is a
    *gate*, not a crash point).
    """
    schema_name = input.schema_hint or input.skill_name
    schema_cls = SCHEMA_REGISTRY.get(schema_name)
    if schema_cls is None:
        # No schema registered for this skill — not a violation.
        return ValidateSkillOutputOutput(
            valid=True,
            schema_name=None,
            suggestions=[
                f"no output_schema registered for '{schema_name}'; "
                f"skill output not validated. Register in "
                f"pbs_mcp/skill_outputs/__init__.py SCHEMA_REGISTRY if "
                f"this skill should be sparring-mode-validated."
            ],
        )

    # Extract fields the schema declares.
    field_names = list(schema_cls.model_fields.keys())
    parsed = _parse_output_to_dict(input.output_text, field_names)

    # Detect missing fields (declared in schema, not extractable from text).
    required_fields = [
        name for name, info in schema_cls.model_fields.items()
        if info.is_required()
    ]
    missing = [f for f in required_fields if f not in parsed]

    if missing:
        return ValidateSkillOutputOutput(
            valid=False,
            schema_name=schema_cls.__name__,
            missing_fields=missing,
            suggestions=[
                f"add `## {f.replace('_', ' ').title()}` section to skill output"
                for f in missing
            ],
            parsed=parsed if parsed else None,
        )

    # Try strict Pydantic validation on the parsed dict.
    try:
        schema_cls.model_validate(parsed)
        return ValidateSkillOutputOutput(
            valid=True,
            schema_name=schema_cls.__name__,
            parsed=parsed,
        )
    except Exception as e:
        # Parse succeeded but Pydantic rejected (e.g., min_length).
        weak: list[str] = []
        msg = str(e)
        for field in field_names:
            if field in msg.lower():
                weak.append(field)
        if not weak:
            weak = ["<unknown>"]
        return ValidateSkillOutputOutput(
            valid=False,
            schema_name=schema_cls.__name__,
            weak_fields=weak,
            suggestions=[
                f"field(s) {weak} parsed but failed validation: {msg.splitlines()[0]}",
            ],
            parsed=parsed,
        )
