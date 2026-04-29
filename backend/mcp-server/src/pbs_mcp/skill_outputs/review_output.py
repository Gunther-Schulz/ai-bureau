"""Output schema for the review-draft skill (Phase B layered review).

Per docs/decisions/sparring-output-v1.md axis-2 promotion:
counter-argument, confidence, reasoning, and "what's missing"
become structural fields rather than behavioral expectations.
"""
from __future__ import annotations

from typing import Literal

from pydantic import Field

from pbs_mcp._strict import StrictModel


class ReviewFinding(StrictModel):
    """One finding from a layered review."""
    layer: Literal["structural", "fachlich", "formal"]
    severity: Literal["blocker", "concern", "suggestion"]
    location: str = Field(..., min_length=1)  # section/page/line reference
    description: str = Field(..., min_length=20)
    proposed_fix: str | None = None


class ReviewOutput(StrictModel):
    """Structured output for review-draft skill.

    Required fields per axis-2 sparring promotion (3 of 7 mechanisms):
    - counter_argument: forces the skill to articulate the strongest
      case against its own findings
    - confidence + confidence_basis: forces calibration, not just
      verdict
    - reasoning: forces the chain to be visible, not just conclusions
    - whats_missing: forces the "what's absent that should be
      considered?" question (axis-2 mechanism 3)

    findings list can be empty (a review can find nothing wrong);
    other fields are required-non-empty.
    """
    findings: list[ReviewFinding] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
    confidence_basis: str = Field(..., min_length=20)
    counter_argument: str = Field(..., min_length=50)
    reasoning: str = Field(..., min_length=100)
    whats_missing: str = Field(..., min_length=20)
