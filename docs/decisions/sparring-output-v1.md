# Decision record: sparring-output structural promotion (v1 commitment)

**Status**: ACCEPTED (pulled forward from ROADMAP defer per
target 8 first-run finding F1, 2026-04-29 session 6)
**Owner**: per-session HANDOFF; full build spans 2-3 sessions

## Context

Design-review target 8's first run found that all 7 VISION axis-2
(sparring) mechanisms are **behavioral-only** — relying on
skill-body instruction language for enforcement, with no
architectural backstop:

| Mechanism | Today's enforcement |
|---|---|
| Counter-argument as first-class output | PROCEDURE.md Checkpoint 13 (text) |
| Confidence calibration | layered-review references (text) |
| "What's missing?" checkpoint | PROCEDURE.md Checkpoint 11+12 (text) |
| Anti-sycophancy guard | Checkpoint 13 (text) |
| Asymmetric knowledge respect | Checkpoint 13 (text) |
| Commit to recommendations | Checkpoint 13 (text) |
| Visible reasoning | module-decisions.md is optional (text) |

Only meta-rule 4's selective-friction calibration (placement
boundary) is structural. The behavioral-only enforcement means
the LLM re-derives sparring requirements from skill body text
each session — exactly the brittleness pattern named in
`feedback_llm_instruction_tightness.md`. Drifts silently if
skill bodies evolve; high overhead each invocation; no detector
fires when a skill's output ships in oracle-mode.

VISION names "answer machine" (axis-2 collapse) as one of three
category-collapse risks; meta-rule 1 (app/office) defends axis 1,
meta-rule 3 (invalidation) defends axis 3, **axis 2 has no
structural defense**. This is the highest-leverage architectural
gap surfaced by target 8.

## Decision

Promote 2-3 of the axis-2 mechanisms from behavioral to
structural via a Skill Bundle output-validation convention:

**Convention (Skill Bundle frontmatter)**: skills that produce
sparring-mode output declare `output_schema: <SchemaName>` in
their YAML frontmatter. The schema is a Pydantic model in
`pbs_mcp/skill_outputs/<SchemaName>.py` declaring the required
output shape (counter-argument, confidence, reasoning,
recommendation, etc.).

**MCP tool**: `validate_skill_output(skill_name, output_text)`
parses the output (heuristic field-extraction from markdown +
strict Pydantic validation) and returns either a `valid: true`
result OR a `missing_fields[]` + `suggestions[]` payload. Skills
loop on retry until valid OR explicit-bypass-with-reason.

**Orchestrator wiring**: after a skill produces output during a
sparring-mode phase, orchestrator calls `validate_skill_output`.
If invalid, kicks back to the skill with the missing-fields
list. If invalid 3x in a row, surfaces to user as "skill
couldn't produce sparring-compliant output — accept anyway, or
retry?"

This moves the validation surface from "skill body says do X" to
"orchestrator + MCP enforces output shape" — same lift in
brittleness reduction as the persistence-layer work in meta-rule
4 refinement A.

## Mechanisms structurally promoted (initial scope)

The minimum-viable v1 promotes **3 of the 7 axis-2 mechanisms**
to structural; the other 4 stay behavioral with sharper skill-
body language:

### Promoted (structural)

1. **Counter-argument as first-class output** — output schema
   has a required `counter_argument: str` field with `min_length=50`.
   Skill body must produce one; missing field fails validation.
2. **Confidence calibration** — output schema has a required
   `confidence: Literal["high", "medium", "low"]` field with
   accompanying `confidence_basis: str` (one-line rationale).
3. **Visible reasoning** — output schema has a required
   `reasoning: str` field with `min_length=100`. Skill body must
   produce its chain of reasoning, not just verdicts.

### Stays behavioral (sharpened skill-body language)

4. **"What's missing?" checkpoint** — Phase B layered review
   already structures this; sharpening skill-body wording is the
   refinement.
5. **Anti-sycophancy guard** — heuristic detection (did the skill
   soften vs. prior turn without new evidence?) is too fuzzy to
   structurally enforce; stays behavioral.
6. **Asymmetric knowledge respect** — declarative ("I'm drawing
   on X; local context Y might change this") is too discretionary
   to schema-enforce; stays behavioral.
7. **Commit to recommendations** — could be structural (require
   `recommendation: str` field with no question marks), but
   commit-vs-question is contextually dependent (sometimes a
   question IS the right move). Stays behavioral.

The promotion is incremental: 3 of 7 in v1, others surface as
refinement candidates after first real project work proves
which behavioral ones drift in practice.

## Initial output schemas (v1 minimum)

```python
# pbs_mcp/skill_outputs/review_output.py
class ReviewOutput(StrictModel):
    """Output shape for review-draft skill (Phase B layered review)."""
    findings: list[ReviewFinding] = Field(..., min_length=0)
    confidence: Literal["high", "medium", "low"]
    confidence_basis: str = Field(..., min_length=20)
    counter_argument: str = Field(..., min_length=50)
    reasoning: str = Field(..., min_length=100)
    whats_missing: str = Field(..., min_length=20)  # axis-2 mechanism 4

# pbs_mcp/skill_outputs/recommendation_output.py
class RecommendationOutput(StrictModel):
    """Output shape for orchestrator's commit-to-recommendation
    pattern (PROCEDURE.md Checkpoint 13)."""
    recommendation: str = Field(..., min_length=20)
    tradeoff: str = Field(..., min_length=20)
    alternative: str = Field(..., min_length=20)
    confidence: Literal["high", "medium", "low"]
    confidence_basis: str = Field(..., min_length=20)
    reasoning: str = Field(..., min_length=100)
```

Other skills (drafting, validation, search) stay output-schema-
free for v1; promotion candidates added incrementally as their
sparring-relevance becomes clear.

## MCP tool design

```python
class ValidateSkillOutputInput(StrictModel):
    skill_name: str  # must match a known skill with declared output_schema
    output_text: str  # raw skill output (markdown OK; parser extracts fields)

class ValidateSkillOutputOutput(StrictModel):
    valid: bool
    schema_name: str  # which Pydantic model was applied
    missing_fields: list[str] = []  # required fields the parser couldn't find
    weak_fields: list[str] = []     # fields that parsed but failed min_length etc.
    suggestions: list[str] = []     # what the skill should add
    parsed: dict[str, Any] | None = None  # the extracted fields, if parse succeeded
```

The parser is heuristic: walks markdown sections, extracts fields
by header (`## Counter-argument`, `## Confidence`, etc.) or by
declared markers (`Confidence: high`, `**Reasoning:** ...`).
Skills are responsible for producing parse-friendly output;
documentation in plugin-conventions.md spells out the format.

## Implementation plan

**Pre-RAG minimum (what ships before Phase 1 corpus download):**

- [x] Decision record (this file) — DONE this session
- [ ] `pbs_mcp/skill_outputs/__init__.py` + `_strict`-based base
- [ ] `pbs_mcp/skill_outputs/review_output.py` — ReviewOutput
- [ ] `pbs_mcp/skill_outputs/recommendation_output.py` — RecommendationOutput
- [ ] `validate_skill_output` MCP tool stub
- [ ] Plugin-conventions.md addition — `output_schema:` frontmatter
      field documented
- [ ] ARCHITECTURE.md addition — meta-rule 4 corollary noting
      sparring-mode structural enforcement

**Next-immediate-session-before-RAG:**

- [ ] Heuristic markdown-field parser (extracts schema-declared
      fields from skill output text)
- [ ] Output-validation invocation pattern in orchestrator
      PROCEDURE.md (after Phase B review skill output, validate
      via tool; loop on missing fields up to 3x)
- [ ] Retrofit `review-draft` skill — declare `output_schema:
      ReviewOutput` in frontmatter; add output-format section to
      skill body
- [ ] Retrofit `orchestrator` skill — recommendation output
      pattern at Checkpoint 13 declares `output_schema:
      RecommendationOutput` for that phase
- [ ] First test: run review-draft on a sample document; verify
      validation gate fires + skill iterates correctly when output
      is missing required fields

## Why pre-RAG (timing)

Per VISION's category-collapse risk: axis-2 is the most-likely
collapse path because it's gradual (each interaction "just a
little more oracle-mode") and undetectable without structural
enforcement. Once RAG ships, every drafting/review session is a
sparring-mode interaction; without the gate, the LLM's habits
calcify session-by-session.

Pre-launch is the unique window because:
- Skill bodies haven't yet been retrofitted with sparring-format
  expectations; cheap to add
- Output schemas can be designed for the gate's first real use
  (drafting + review) rather than retrofitted to existing patterns
- Orchestrator's PROCEDURE.md hasn't yet wired the validation
  loop; clean addition

If we ship RAG first, every drafting session generates output
that doesn't pass the gate (because the skills haven't been
retrofitted yet). Each is a habit-calcification step that we'd
have to undo session-by-session.

## Why these 3 mechanisms (not all 7)

- 3 promoted are *production-output* mechanisms (counter-arg,
  confidence, reasoning) — they're what the user reads and
  defends downstream. Brittleness here is highest-impact.
- 4 staying behavioral are *interaction-pattern* mechanisms
  (what's missing, anti-sycophancy, asymmetric respect,
  recommendation-commit) — harder to schema-validate without
  false-positive fail rates.

This is the Pareto pick: 80% of the structural-enforcement
benefit at 30% of the build cost. The other 4 can be promoted
later if behavioral drift surfaces in real project use.

## Revisit triggers

- After first 5 real review-draft + orchestrator-recommendation
  sessions: did the validation gate catch anything? Did skills
  retry effectively? Were the schemas the right shape?
- If audit slice 18 (future, sparring-output coverage) finds skill
  bodies bypassing the gate
- If user disagrees with structural-vs-behavioral split for any
  of the 4 not promoted in v1
