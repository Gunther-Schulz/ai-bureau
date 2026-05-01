# Decision record: MS AF eval framework adoption (R3b from #21 SDK deep-read)

**Status**: ACCEPTED — session 12 (2026-04-30); 2-round sharpening (full monty + S1-S4 schema field refinements + minor cross-ref note from R3a round 2 — discovery API usage)
**Owner**: ROADMAP commitment #21 (SDK deep-read R3b); replaces Phase 0 item 5 design-from-scratch plan
**Related**: `substrate-agentic-framework.md` (#18); `sdk-deep-read.md` (#21 — origin findings); `ai-as-runtime-hybrid-shape.md` (#16 — entity-md spec used for scenarios); `office-vs-department.md` (#12 — entity convention); `audit-trail-v2.md` (eval emits AuditEvents); `sparring-output-v1.md` (composes with sparring schema validation); `in-process-mcp-server.md` (R3a — `mcp_gate_parity` scenario type); `permission-abstraction.md` (R3c — permission flows generate AuditEvents R3b validates)

## Context

Phase 0 item 5 originally scoped as "design eval-result schema as Pydantic contracts (EvalRun / Scenario / EvalResult / RegressionSuite)." MS AF provides exactly these primitives + more (Evaluator Protocol, EvalResults, evaluate_agent, pre-built checks).

The R3b question: adopt directly / wrap in own types / hybrid / hand-roll separate?

## Decision

**Hybrid (Option C) — adopt MS AF eval primitives as primary; extend with PBS-specific evaluators for VISION-axis-aligned scoring; minimal wrapping where extension lives.**

### Direct adoption from MS AF

- `Evaluator` Protocol, `EvalResults`, `EvalItem`, `EvalScoreResult`, `LocalEvaluator`, `CheckResult`, `ConversationSplit`, `ConversationSplitter`, `EvalNotPassedError`
- Pre-built checks: `keyword_check`, `tool_call_args_match`, `tool_called_check`, `tool_calls_present`
- Runner functions: `evaluate_agent`, `evaluate_workflow`

### PBS-specific extensions (implementing MS AF `Evaluator` Protocol)

- `SparringQualityEvaluator` — counter-argument presence + confidence calibration adequacy + visible reasoning depth + anti-sycophancy heuristic (per VISION axis 2)
- `DefensibilityEvaluator` — six-months-later-can-defend test (per VISION axis 3)
- `IntertwiningEvaluator` — workflow-embedding depth check (per VISION axis 1)

### PBS-specific check primitives

In `backend/eval/pbs_checks/`:
- `audit_event_emitted_check`
- `entity_state_check`
- `sparring_schema_check`
- `convention_applied_check`
- `decision_reconstructibility_check` (building block for DefensibilityEvaluator)
- `mcp_gate_parity_check` (for R3a CI parity testing)

**Tool/server discovery for scenarios** (per R3a M2): scenarios use `Substrate.list_mcp_servers()` + `Substrate.list_available_tools()` to discover gates being tested. Scenario authors can declaratively reference tools via these discovery methods rather than hardcoding tool names.

## Scenarios as entities (per entity-md spec)

```
extensions/{department}/eval-scenarios/{scenario-id}/
  ├── scenario.md (entity-md, type: <dept>.eval-scenario)
  ├── setup.py (optional Python module)
  └── assertions.py (optional Python module)
```

Loaded via #9 generic entity gate. Composes with AI-as-runtime hybrid-shape, entity-elevation discipline, pattern-vs-instance discipline, make-wrong-shapes-impossible, scope orthogonality.

### `EvalScenarioEntity` Layer 2 schema (with S1-S4 refinements)

```python
class EvalScenarioEntity(EntityBase):
    # Layer 1 inherited from EntityBase
    
    # Layer 2 specific fields
    applicable_evaluators: list[str]  # which evaluators run against this scenario
    severity: Literal["info", "warn", "error"]
    tags: list[str]
    setup_module: str  # dotted Python path
    assertions_module: str  # dotted Python path
    expected_check_results: list[CheckResult]
    
    # S1: scope dimension (NEW round 2)
    scope_dimension: Literal[
        "system_level",       # orchestrator routing, cross-skill flow
        "skill_level",        # single skill input/output
        "cross_skill",        # workflow spanning multiple skills
        "architectural",      # discipline enforcement
    ]
    
    # S2: substrate-conditional applicability (NEW round 2)
    applicable_substrates: list[Literal[
        "claude_agent_sdk",
        "ms_agent_framework",
        "hand_rolled",
        "any",
    ]]
    
    # S3: tier-conditional applicability (NEW round 2)
    applicable_tiers: list[Literal[
        "tier_1",
        "tier_2",
        "tier_3",
        "all",
    ]]
```

### Body conventions for `type: <dept>.eval-scenario`

Recommended sections (per entity-md-spec body conventions):
- `## What this scenario tests`
- `## Expected behavior`
- `## Edge cases`
- `## Domain reasoning`
- `## VISION axis alignment` (NEW per round 1 R5)
- `## Cross-references`

## Result reporting (S4 — explicit shape)

| Output | Shape | When |
|---|---|---|
| Console output | Structured stdout (PASS/FAIL counts, failed scenario list, EvalScoreResult details) | CI logs; local runs |
| Eval-run-summary entity | `extensions/{department}/eval-runs/{run_id}.md` (auto-generated entity-md per run; queryable via #9 entity gate) | After every full eval run |
| AuditEvent emission | `event_kind=eval_run_completed` with EvalResults summary in details | Per R11; composes with #6 audit-trail v2 |
| Future: web dashboard | (deferred to consulting client deployment with multi-user UX needs) | Tier 2+ |
| Future: notifications | (deferred to integration with alerting infrastructure) | Tier 2+ |

## Module layout

```
backend/eval/                                              # Framework code
  ├── __init__.py
  ├── pbs_evaluators/
  │   ├── sparring_quality.py
  │   ├── defensibility.py
  │   └── intertwining.py
  ├── pbs_checks/
  │   ├── audit_event_emitted.py
  │   ├── entity_state.py
  │   ├── sparring_schema.py
  │   ├── convention_applied.py
  │   ├── decision_reconstructibility.py
  │   └── mcp_gate_parity.py
  ├── harness.py
  └── scenario_loader.py
```

## Sparring eval methodology — three layers

| Layer | Mechanism | Status |
|---|---|---|
| **Layer 1** | Structural presence: Pydantic field validation + length checks; uses MS AF pre-built checks where applicable | Ships now (Phase 0 item 5) |
| **Layer 2** | LLM-as-judge: another Claude scores counter-argument quality (sparring-mode-prompted; anti-sycophancy applied to judge itself) | Deferred per chronological defer (`greenfield-architecture-review.md` §3) |
| **Layer 3** | Anti-sycophancy heuristic: compare current turn output to prior turn — did skill soften without new tool-result evidence? | Deferred per chronological defer |

Layer 2 + 3 ship when 5-10 real sparring sessions accumulate empirical pattern data.

## CI integration

| Gate | Mechanism | When |
|---|---|---|
| Pre-commit hook | Structural-presence checks (Layer 1 sparring; Pydantic validation); runs in <5s | Every commit |
| CI workflow | Full eval suite via `pytest backend/eval/` | Every PR |
| PR gate | CI eval must pass for merge to main | After eval framework lands |
| Phase boundary check | Full eval run before phase transitions | Manual; orchestrator-prompted |

## LLM-as-judge methodology (R13 from round 1)

For Layer 2 sparring quality + DefensibilityEvaluator scoring:

| Concern | Mitigation |
|---|---|
| Non-determinism | Run judge multiple times; use median/mode; document confidence interval |
| API cost | Budget per CI run; cap LLM-judge calls; use smaller model when possible (Sonnet vs Opus) |
| Judge bias | Document judge model in EvalResults metadata; report results-by-judge-model |
| Sparring discipline of judge | Judge LLM is sparring-mode-prompted: "score this counter-argument; argue against your own scoring" |

## Composition with existing architecture

| Concern | R3b interaction |
|---|---|
| `validate_skill_output` MCP tool | Composes — `validate_skill_output` = SCHEMA validation (runtime gate); `SparringQualityEvaluator` = QUALITY scoring (eval-time); non-overlapping |
| `audit-trail-v2.md` | Eval emits `eval_run_started`, `eval_run_completed`, `eval_scenario_failed` event kinds |
| `sparring-output-v1.md` | `SparringQualityEvaluator` scores against sparring schemas |
| #9 entity gate | Scenarios loaded via gate (`type=<dept>.eval-scenario`); eval-run-summaries written via gate |
| #16 entity-md spec | Scenarios are entity-md per spec; new body section "VISION axis alignment" added |
| R3a TransportMode | `mcp_gate_parity` scenario type validates both transport modes via this framework |
| R3c permission flow | Permission flows generate AuditEvents that R3b's `audit_event_emitted_check` validates |
| #6 audit-trail retrofit | Eval event kinds added to audit-trail-v2 schema |
| #15 office-level entities | DefensibilityEvaluator scores against actor-attributed audit trails |
| Substrate decision (#18) | Substrate-agnostic — eval primitives are pure Python types; runs on Claude Agent SDK / MS AF / hand-rolled |

## Phase 0 item 5 NEW scope (8 deliverables)

1. Adopt MS AF eval primitives via `pip install agent-framework-core`
2. Define Layer 2 `EvalScenarioEntity` Pydantic schema (per entity-md spec)
3. Implement `backend/eval/scenario_loader.py` (loads scenarios via #9 generic entity gate; resolves Python module paths)
4. Implement `backend/eval/harness.py` (runs scenarios via MS AF `evaluate_agent`; aggregates EvalResults; emits report)
5. Implement `backend/eval/pbs_evaluators/sparring_quality.py` (Layer 1 structural presence checks)
6. Implement PBS-specific check primitives in `backend/eval/pbs_checks/` (`audit_event_emitted`, `entity_state`, `sparring_schema`, `convention_applied`, `decision_reconstructibility`, `mcp_gate_parity`)
7. Author 5-10 initial scenarios in `extensions/{department}/eval-scenarios/` covering core MCP gates + sparring schemas + state.md round-trip + R3a parity
8. Wire CI: `pytest backend/eval/` runs harness + fails on eval failure

## Defers — re-examined session 15 under v0.33 no-defer principle

> **Session 15 amendment**: re-examined the 7 entries below. Result: 6 entries are valid watch-list entries (each names a specific external signal: D1 5-10 real sparring sessions; D2 first project artifact OR synthetic project artifact authored; D3 stable orchestrator workflow + persistent state samples; D4 Phase-1-corpus completion; D5 first consulting engagement; D7 performance-eval need surfacing). D6 (web dashboard + notifications) is phase routing to Tier 2+ deployment (#13). Per v0.33 preliminary-lock: this DR remains preliminary-locked. This DR is one of the cleaner defer-tables — most entries already had specific external signals named at write-time. Original entries kept below as historical record.

### Original entries (chronological-valid)

| Defer | Home | Reason |
|---|---|---|
| **D1**: Sparring eval Layer 2 + 3 | Post-empirical-data (5-10 real sparring sessions) per `greenfield-architecture-review.md` §3 | False-positive heuristic shapes need empirical pattern data |
| **D2**: `DefensibilityEvaluator` (wraps `decision_reconstructibility_check`) | First project artifact OR synthetic project artifact authored | Needs real artifact to score against |
| **D3**: `IntertwiningEvaluator` | Stable orchestrator workflow + persistent state samples | Needs stable runtime to score against |
| **D4**: Detailed scenario library | Post-Phase-1-corpus (real project workflows accumulate) | Pre-RAG = synthetic only |
| **D5**: Consulting-deployment-specific evaluators | First consulting engagement | Custom evaluators per client domain |
| **D6**: Web dashboard + notifications for results | Tier 2+ deployment with multi-user UX | Single-user (Tier 1) doesn't need; defer to Tier 2 |
| **D7**: `eval_dimension` field (correctness/performance/regression) | When performance-eval need surfaces | Phase 0 covers correctness only |

## Constraints flowing to downstream commitments

- **→ Phase 0 item 5**: scope shifted from "design from scratch" to this hybrid adoption (8 deliverables above)
- **→ #9 (entity gate)**: `EvalScenarioEntity` loaded via entity gate; `type=<dept>.eval-scenario` registered
- **→ #6 (audit-trail v2 retrofit)**: event kinds added: `eval_run_started`, `eval_run_completed`, `eval_scenario_failed`
- **→ entity-md-spec.md**: recommended body section "VISION axis alignment" added for `eval-scenario` type
- **→ R3a (in-process MCP)**: `mcp_gate_parity` scenario type validates both transport modes
- **→ R3c (permission flow)**: eval validates permission flow AuditEvents via `audit_event_emitted_check`
- **→ Substrate decision (#18)**: Substrate-agnostic adoption; pure dependency add (`pip install agent-framework-core`); no substrate switch

## Revisit triggers

- **MS AF eval primitives major release** (1.x → 2.x) — re-validate adoption + version pin update
- **Empirical pattern data accumulates** (5-10 real sparring sessions) — Layer 2 + 3 sparring eval design proceeds
- **First project artifact in place** — DefensibilityEvaluator implementation proceeds
- **First consulting client domain-specific eval needs surface** — custom evaluator design proceeds
- **Performance-eval need surfaces** — `eval_dimension` field added; performance scenarios designed

## Files touched

- `docs/decisions/eval-framework-adoption.md` — this file (NEW; status ACCEPTED)
- `sdk-deep-read.md` — updated to reference this DR as detailed implementation
- `entity-md-spec.md` — body section "VISION axis alignment" addition (deferred to implementation)
- `audit-trail-v2.md` — event kinds addition (with #6 retrofit)
