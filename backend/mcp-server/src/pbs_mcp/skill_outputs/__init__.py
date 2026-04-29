"""Skill output schemas — structural enforcement of sparring-mode shape.

Per docs/decisions/sparring-output-v1.md and ARCHITECTURE.md
meta-rule 4. Each module here declares one Pydantic model per
sparring-mode skill output kind. Skills declare `output_schema:
<name>` in their YAML frontmatter; the orchestrator validates
their output against the schema via `validate_skill_output` MCP
tool.

This is the structural promotion of axis-2 (sparring) mechanisms:
counter-argument, confidence, and reasoning move from behavioral-
only enforcement (skill body says "do X") to structural enforcement
(output validation gate refuses incomplete shapes).

Initial v1 schemas: ReviewOutput (review-draft), RecommendationOutput
(orchestrator commit-to-recommendation pattern). Other skills stay
output-schema-free in v1 and may be promoted later.
"""
from pbs_mcp.skill_outputs.review_output import ReviewOutput, ReviewFinding
from pbs_mcp.skill_outputs.recommendation_output import RecommendationOutput

__all__ = ["ReviewOutput", "ReviewFinding", "RecommendationOutput"]


# Registry: skill_name → output_schema class. Keep in sync with each
# skill's `output_schema:` frontmatter declaration. Orchestrator + the
# validate_skill_output MCP tool use this registry to look up the
# expected schema for a given skill.
SCHEMA_REGISTRY: dict[str, type] = {
    "review-draft": ReviewOutput,
    # "orchestrator": RecommendationOutput,  # phase-specific; not skill-wide
    # Add entries as skills declare output_schema in their frontmatter.
}
