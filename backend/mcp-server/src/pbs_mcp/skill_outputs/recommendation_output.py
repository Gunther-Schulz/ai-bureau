"""Output schema for orchestrator's commit-to-recommendation pattern.

Per PROCEDURE.md Checkpoint 13 + docs/decisions/sparring-output-v1.md.
This is a phase-specific output (not whole-orchestrator), used when
the orchestrator surfaces a decision as recommendation + tradeoff.
"""
from __future__ import annotations

from typing import Literal

from pydantic import Field

from pbs_mcp._strict import StrictModel


class RecommendationOutput(StrictModel):
    """Structured output for the orchestrator's commit-to-recommendation
    pattern (PROCEDURE.md Checkpoint 13).

    Required fields force the recommendation to be a *position* (not a
    question), with named tradeoff and at least one alternative —
    preventing menu-presentation drift back into oracle-mode.
    """
    recommendation: str = Field(..., min_length=20)
    tradeoff: str = Field(..., min_length=20)
    alternative: str = Field(..., min_length=20)
    confidence: Literal["high", "medium", "low"]
    confidence_basis: str = Field(..., min_length=20)
    reasoning: str = Field(..., min_length=100)
