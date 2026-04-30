# Decision record: SDK deep-read findings (#21)

**Status**: ACCEPTED — session 12 (2026-04-30)
**Owner**: ROADMAP commitment #21; `substrate-agentic-framework.md` (#18 — recommendation refined by this DR's findings)
**Related**: `substrate-agentic-framework.md` (substrate decision; this DR verifies + refines its claims with code-level evidence), `ai-as-runtime-hybrid-shape.md` (#16 — hybrid-shape contract substrate must support), `office-vs-department.md` (#12 — managed-entity concept that interacts with substrate primitives), `governance-and-identity-sourcing.md` (governance gate primitives that map to substrate hook surfaces)

## Context

ROADMAP commitment #18 (substrate eval, shipped session 12 commit `2a8dfb5`) made the substrate decision (Claude Agent SDK + MS Agent Framework dual-substrate; Substrate Protocol NEW pattern) based on documentation, blog posts, and web searches. ROADMAP commitment #21 (this DR) verifies those claims with code-level evidence by cloning both SDKs locally and structured code-reading.

Goals:
1. **Verify** #18's deep-eval claims (does the actual code match what the docs said?)
2. **Surface primitives** we could leverage that we missed (un-anticipated capabilities)
3. **Identify refactor opportunities** for current/planned PBS code (where SDK primitives subsume our hand-rolled work)
4. **Inform Substrate Protocol shape** with actual SDK API patterns rather than documented surface
5. **Anti-cargo-cult anchor**: explicit decisions about what we adopt vs what stays custom

## Method

Cloned both repos via `ref` skill convention to:
- `~/dev/reference/claude-agent-sdk-python/` (2.1 MB, shallow clone)
- `~/dev/reference/agent-framework/` (56 MB — includes both .NET + Python; Python tree at `python/packages/`)

Structured code-read with focus areas per substrate (per ROADMAP #21 spec):

- **Claude Agent SDK**: agent loop internals; MCP attach-to-agent mechanism; RunHooks lifecycle; Pydantic structured output flow; Channels event-driven; session JSON shape; plugin SKILL.md loader
- **MS Agent Framework**: agent middleware pipeline; 3-layer middleware; workflow engine + checkpointing; event-driven workflow trigger types; multi-provider connector patterns; Agent Skills loader; A2A integration

Read scope this session: public API surfaces (`__init__.py` files), README, key file structures + sizes (file sizes act as complexity-proxy signals). Detailed implementation reads of specific files (`_middleware.py`, `_skills.py`, `client.py`, etc.) deferred to implementation-time when specific primitives are adopted.

## Findings — Claude Agent SDK Python

### Verifications of #18 claims

| Claim | Verdict | Evidence |
|---|---|---|
| MCP integration deepest (attach to agent definition; framework handles lifecycle + capability negotiation) | ✅ CONFIRMED + STRONGER than documented | Uses **real `mcp.types` directly** (`from mcp.types import ToolAnnotations`); not wrapped. `@tool` decorator + `create_sdk_mcp_server` = **in-process Python tools as MCP server** (no subprocess; no IPC overhead). Mixed mode (in-process + external subprocess MCP) supported uniformly |
| Hybrid-shape via SKILL.md format (markdown bodies as runtime fuel) | ✅ CONFIRMED | Skills are markdown injected directly into system prompt at runtime; runtime reads SKILL.md from filesystem on demand; same SKILL.md format we'd write anyway |
| Pydantic structured output + auto-retry on validation fail | ✅ CONFIRMED | `.model_json_schema()` for structured outputs; SDK forces Claude to return matching schema; auto-retries with corrective instructions if validation fails |
| Bundled Claude Code CLI (no separate install needed) | ✅ CONFIRMED | "The Claude Code CLI is automatically bundled with the package - no separate installation required! The SDK will use the bundled CLI by default. If you prefer to use a system-wide installation or a specific version, you can use `cli_path=`" |
| Hooks for sparring composability (RunHooks lifecycle) | ✅ CONFIRMED + RICHER than documented (see "NEW capabilities" below) |
| Vendor-neutral by ecosystem alignment (Anthropic ecosystem IS the goal) | ✅ CONFIRMED | SDK is Anthropic's; alignment by construction |

### NEW capabilities discovered (not in #18 deep-eval)

**Hooks system is RICHER than initially characterized**:
- 11+ hook event types: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `PreCompact`, `Stop`, `Notification`, `SubagentStart`, `SubagentStop`, `PermissionRequest`
- Each event has typed input + structured output classes (e.g., `PreToolUseHookInput`, `PreToolUseHookSpecificOutput`)
- `HookMatcher` pattern for matching hooks to specific tools/conditions
- Hooks return `HookJSONOutput` (structured) — can deny tool use, modify inputs, provide reasoning
- **Significance for sparring**: rich enough hook surface to backstop counter-argument validation, anti-sycophancy heuristics, output schema validation, asymmetric knowledge respect — without fighting the framework

**Subagent + session forking primitives** (NEW in 0.1.0):
- `SubagentStartHookInput`, `SubagentStopHookInput`
- `get_subagent_messages`, `list_subagents`, `get_subagent_messages_from_store`
- `fork_session`, `ForkSessionResult` — branch a session into multiple
- `SessionStore` Protocol + `InMemorySessionStore` built-in implementation
- Session mutations: `delete_session`, `rename_session`, `tag_session`, `import_session_to_store`
- `SessionSummaryEntry`, `fold_session_summary` — session compaction primitives
- **Significance for PBS**: skills could become genuinely subagent-shaped; session forking enables exploring alternative drafts/argumentation paths; SessionStore could be persistence primitive

**Permission model primitives**:
- `CanUseTool` callback for runtime permission decisions
- `PermissionMode` enum, `PermissionRequestHookInput`, `PermissionRequestHookSpecificOutput`
- `PermissionResult` Allow/Deny variants, `PermissionUpdate`
- `ToolPermissionContext`
- **Significance**: maps directly to our four-way decision menu / governance gates / send-gate pattern — primitives we'd otherwise build

**Sandbox primitives**:
- `SandboxIgnoreViolations`, `SandboxNetworkConfig`, `SandboxSettings`
- **Significance**: relevant for adapter-mode entities + Tier 2 deployments where sandboxing matters

**Thinking mode** explicit:
- `ThinkingBlock`, `ThinkingConfig`, `ThinkingConfigAdaptive`, `ThinkingConfigDisabled`, `ThinkingConfigEnabled`
- **Significance**: per-skill or per-task thinking mode configuration

**Rate limit handling** built-in:
- `RateLimitEvent`, `RateLimitInfo`, `RateLimitStatus`, `RateLimitType`

**Context usage tracking**:
- `ContextUsageCategory`, `ContextUsageResponse`

**Plugin support**:
- `SdkPluginConfig`

**Two API levels** (already known but worth restating):
- `query()` — simple async iterator; no custom tools or hooks
- `ClaudeSDKClient` — bidirectional; supports custom tools + hooks (this is what PBS would use)

### Public API breadth

Public exports from `claude_agent_sdk` package: ~80+ types/classes/functions covering: 11+ hook input/output type pairs; permission primitives; sandbox; thinking; rate limit; context usage; sessions/forking/store/mutations; subagents; MCP types (real `mcp.types`); message types; content blocks; tool annotations; SDK MCP server creation.

## Findings — MS Agent Framework Python (core package)

### Verifications + nuances of #18 claims

| Claim | Verdict | Evidence + nuance |
|---|---|---|
| MCP-native at 1.0 (not bolt-on) | ⚠ NUANCED PASS | MS AF treats MCP as **one tool type among many**: `MCPStdioTool`, `MCPStreamableHTTPTool`, `MCPWebsocketTool`. Has full MCP support — but **NOT MCP-as-primary-contract-surface** the way Claude Agent SDK is. Criterion 1 verdict from #18 still passes; the nuance is that MS AF's MCP integration shape is "MCP as one tool transport"; Claude Agent SDK's is "MCP as the contract surface itself" |
| Agent Skills uses SKILL.md format = Anthropic plugins format (industry convergence) | ✅ CONFIRMED | `_skills.py` (58K) implements `Skill`, `SkillResource`, `SkillScript`, `SkillScriptRunner`, `SkillsProvider` — Agent Skills SDK pattern matches Anthropic conventions |
| Multi-provider connectors (Foundry / Azure OpenAI / OpenAI / Anthropic Claude / Bedrock / Gemini / Ollama) | ✅ CONFIRMED via separate packages | Subdirs in `python/packages/`: `anthropic`, `azure-ai-search`, `bedrock`, `claude` (separate from anthropic!), `foundry`, `foundry_hosting`, `foundry_local`, `gemini`, `github_copilot`, `mem0`, `ollama`, `openai`. `agent_framework_core` selective install genuinely minimal |
| 3-layer middleware (agent / function / chat) | ✅ CONFIRMED | `_middleware.py` (59K) implements `AgentMiddleware`, `ChatMiddleware`, `FunctionMiddleware` + corresponding contexts (`AgentContext`, `ChatContext`, `FunctionInvocationContext`) + decorators (`agent_middleware`, `chat_middleware`, `function_middleware`) + `MiddlewareTermination` |
| Pydantic structured outputs | ✅ CONFIRMED | `_types.py` (144K — substantial type system) provides comprehensive Pydantic models |
| Event-driven workflows for Gap A + Gap B | ✅ CONFIRMED | Workflow engine with `WorkflowAgent`, `AgentExecutor`, edge primitives (FanIn / FanOut / SwitchCase) + checkpointing |

### NEW capabilities discovered (not in #18 deep-eval)

**Evaluation framework FIRST-CLASS** (substantial — could subsume our planned testing methodology):
- `_evaluation.py` (72K) implements: `Evaluator` Protocol, `LocalEvaluator`, `EvalResults`, `EvalItemResult`, `EvalScoreResult`
- High-level functions: `evaluate_agent`, `evaluate_workflow`
- Pre-built checks: `keyword_check`, `tool_call_args_match`, `tool_called_check`, `tool_calls_present`
- `ConversationSplit`, `ConversationSplitter` for multi-turn eval
- `ExpectedToolCall`, `CheckResult`, `EvalItem`, `AgentEvalConverter`
- `EvalNotPassedError` for assertion-style testing
- `evaluator` decorator for custom evaluators
- **Significance**: PBS Phase 0 item 5 (testing methodology + harness — discussion-first per ROADMAP) could **substantially leverage MS AF eval primitives** rather than building from scratch. Adopt as primitives-only even though Claude Agent SDK is primary substrate

**Compaction strategies** (substantial — much more advanced than Claude Agent SDK's single PreCompact hook):
- `_compaction.py` (49K) implements: `CompactionProvider`, `CompactionStrategy`, `TokenizerProtocol`
- Multiple strategies: `SelectiveToolCallCompactionStrategy`, `SlidingWindowStrategy`, `SummarizationStrategy`, `TokenBudgetComposedStrategy`, `ToolResultCompactionStrategy`, `TruncationStrategy`
- `CharacterEstimatorTokenizer` default tokenizer
- `apply_compaction`, `included_messages`, `included_token_count`, `annotate_message_groups`
- Group/state metadata keys: `COMPACTION_STATE_KEY`, `EXCLUDE_REASON_KEY`, `EXCLUDED_KEY`, `GROUP_*` keys, `SUMMARIZED_BY_*` keys
- **Significance**: long-running planning bureau sessions (months-spanning B-Plan projects with hundreds of decisions) need sophisticated compaction. Could adopt MS AF compaction primitives even with Claude Agent SDK as primary substrate

**Sessions + History Providers**:
- `AgentSession`, `ContextProvider`, `FileHistoryProvider`, `InMemoryHistoryProvider`, `SessionContext`
- `register_state_type` — state-shape registration for sessions
- **Significance**: parallels Claude Agent SDK's SessionStore but with Provider pattern (more pluggable). PBS could use FileHistoryProvider for state persistence

**Workflow primitives** (richer than initially documented):
- `WorkflowAgent`, `AgentExecutor`, `AgentExecutorRequest`, `AgentExecutorResponse`
- Edge primitives: `Case`, `Default`, `Edge`, `EdgeCondition`, `FanInEdgeGroup`, `FanOutEdgeGroup`, `SingleEdgeGroup`, `SwitchCaseEdgeGroup`, `SwitchCaseEdgeGroupCase`
- `CheckpointStorage` Protocol + `FileCheckpointStorage` + `InMemoryCheckpointStorage` + `WorkflowCheckpoint`
- `DEFAULT_MAX_ITERATIONS`
- **Significance**: orchestrator could leverage workflow + checkpoint primitives if we adopt MS AF substrate; less applicable for Claude Agent SDK substrate (which uses session-based pattern)

**Observability** (`observability.py` is 99K — substantial):
- OpenTelemetry-first per #18 verification
- Detailed implementation TBD — file size suggests rich primitives

**Tools system**:
- `FunctionTool`, `tool` decorator, `FunctionInvocationConfiguration`, `FunctionInvocationLayer`, `ToolTypes`, `SKIP_PARSING`, `normalize_function_invocation_configuration`
- Three MCP tool variants (Stdio / StreamableHTTP / Websocket)

**Settings**:
- `SecretString` for secret-typed configs
- `load_settings`

### Public API breadth

Public exports from `agent_framework` core package: ~150+ types/classes/functions covering: comprehensive type system; agents (Agent, BaseAgent, RawAgent); chat clients (with capability protocols `Supports*Tool`); compaction (6 strategies + tokenizer); evaluation (8+ primitives); 3-layer middleware; sessions + history providers; skills; tools; workflows + edges + checkpointing; multi-provider lazy-loaded connectors.

## Big architectural insights

### Insight 1: The two substrates pull architecture in DIFFERENT directions

| Direction | Claude Agent SDK | MS Agent Framework |
|---|---|---|
| Primary metaphor | Plugin-runtime (Claude Code as host; agents are plugin-shaped) | Workflow-engine + agent runtime (Python program orchestrates agents through graph state) |
| MCP role | Primary contract surface | One tool type among many |
| State model | Session-based + forking + subagent | History providers + workflow checkpoints + register_state_type |
| Compaction | Single PreCompact hook | 6+ strategies + tokenizer protocol |
| Evaluation | (none built-in) | First-class framework (evaluate_agent, evaluate_workflow, Evaluator) |
| Permission/sparring surface | 11+ hook event types + permission primitives | 3-layer middleware (agent/function/chat) + HITL approval |

This confirms #18 framing — but the SHAPE divergence is more pronounced than initially documented. **Substrate Protocol abstraction will need to be narrower than initially hoped** to find common surface.

### Insight 2: Substrate Protocol common surface (refined)

Per #9 implementation work, the `Substrate` Protocol must define a surface that BOTH Claude Agent SDK and MS AF satisfy. After this code-read:

**Common surface (what both substrates support cleanly)**:
- Agent loop entry point (start an agent run with prompt + tools + system_prompt)
- Pydantic structured output validation (both have it; auto-retry semantics differ but conceptually align)
- Tool invocation lifecycle (both have hooks at PreTool / PostTool moments)
- Session/context management (both have persistent state primitives, different shapes)
- Multi-step workflow expression (both can express; Claude Agent SDK via subagents + ClaudeSDKClient turn-loop, MS AF via workflow engine)

**Substrate-SPECIFIC value-adds (NOT in common surface; per-substrate extension points)**:
- **Claude Agent SDK only**: subagent primitives + session forking + SessionStore + permission model + sandbox + thinking mode + Channels event-driven push
- **MS AF only**: 3-layer middleware (agent/function/chat) + workflow engine + checkpointing + evaluation framework + 6+ compaction strategies + history provider Protocol

**Implication for #9 entity gate design**: Substrate Protocol = ~5-6 method abstraction (agent run + tools + hooks + structured output + session). Per-substrate adapter wraps native primitives to satisfy Protocol. PBS skills work against the Protocol. Substrate-specific extensions accessed via substrate-name-typed extension methods (e.g., `sdk.subagent_for(skill)` only valid on Claude Agent SDK substrate; `sdk.evaluate_agent(...)` only on MS AF substrate).

### Insight 3: Refactor opportunities for current/planned PBS code (substantial)

The SDK code-read surfaces three concrete refactor opportunities:

**3a. PBS-mcp → in-process MCP server** (Claude Agent SDK pattern):
- Current: PBS-mcp is a separate Python process invoked by Claude Code via stdio MCP
- Opportunity: register PBS MCP tools via `create_sdk_mcp_server` as in-process Python server when running on Claude Agent SDK substrate
- Benefits: no subprocess management; no IPC overhead; simpler deployment; single-process Python; better debugging
- Cost: substrate-specific (only applies when on Claude Agent SDK substrate; MS AF substrate would still use external MCP)
- Lands: bundled with #11 (Cowork integration) when Claude Agent SDK becomes the runtime

**3b. MS AF eval primitives → adopt for testing methodology #5**:
- Current: testing methodology + harness scoped at Phase 0 item 5 as discussion-first ("design eval-result schema as Pydantic contracts: EvalRun / Scenario / EvalResult / RegressionSuite")
- Opportunity: MS AF's evaluation framework provides exactly these primitives + more (Evaluator Protocol, EvalResults, evaluate_agent, evaluate_workflow, pre-built checks, custom evaluator decorator, conversation splitter)
- Benefits: don't reinvent; mature framework; built-in checks; works regardless of which substrate is primary
- Adopt as: primitives-only (we don't switch substrate to MS AF for this; we use MS AF's `agent_framework.evaluation` primitives within our hand-rolled testing harness OR alongside Claude Agent SDK substrate)
- Lands: bundled with Phase 0 item 5 design

**3c. Permission model primitives → governance gate / sparring backstop**:
- Current: planned governance + sparring backstop is hand-rolled per `governance-and-identity-sourcing.md` decision 1 + sparring-output-v1
- Opportunity: Claude Agent SDK's permission primitives (`CanUseTool`, `PermissionMode`, `PermissionResult`, `ToolPermissionContext`) provide exactly the surface we'd build
- Benefits: built-in primitives; integrates with Claude Code's natural permission flow
- Lands: bundled with #9 implementation phase (entity gate uses permission primitives for write-authorization checks; sparring backstop hooks use permission primitives for counter-argument-validation deny path)

**3d. Skills as Claude Agent SDK subagents** (worth evaluating):
- Current: PBS skills are Anthropic plugin-shaped markdown files; orchestrator routes to them via skill descriptions
- Opportunity: Claude Agent SDK has rich subagent primitives (`SubagentStartHookInput`, `get_subagent_messages`, `list_subagents`)
- Question: do PBS skills naturally map to Claude Agent SDK subagents? Or are they a different abstraction (skills = capability declarations; subagents = forked execution contexts)?
- Verdict: subagent primitives are about EXECUTION context branching, not capability composition. Skills stay skills; subagent primitives might be useful for specific scenarios (e.g., "explore alternative draft path" = fork session + run skill in subagent)
- Lands: evaluated on case-by-case basis as PBS workflows surface scenarios where subagent-pattern fits

## Substrate Protocol design implications (refined from #18)

#18's Substrate Protocol was specified at high level: "agent loop primitives, sparring hook interface, user-runtime adapter." This DR refines:

**Substrate Protocol method surface (proposed for #9)**:

```python
class Substrate(Protocol):
    """Substrate-coupled primitives. Concrete implementations: 
    ClaudeAgentSDKSubstrate, MSAgentFrameworkSubstrate."""
    
    async def run_agent(
        self,
        prompt: str,
        system_prompt: str | None,
        tools: list[ToolType],
        output_schema: type[BaseModel] | None,
        max_turns: int | None,
    ) -> AgentRunResult: ...
    
    async def run_agent_with_hooks(
        self,
        ...,
        hooks: dict[HookEvent, list[HookCallback]],
    ) -> AgentRunResult: ...
    
    def get_session_store(self) -> SessionStore: ...
    
    def create_in_process_mcp_server(
        self,
        name: str,
        tools: list[Callable],
    ) -> MCPServerHandle: ...  # Substrate-specific impl; Claude Agent SDK = create_sdk_mcp_server; MS AF = different shape
```

Plus per-substrate extension points (NOT in common Protocol):

```python
class ClaudeAgentSDKExtensions(Protocol):
    def fork_session(self, ...) -> ForkSessionResult: ...
    def list_subagents(self, ...) -> list[SubagentInfo]: ...
    # subagent + permission + sandbox + thinking primitives

class MSAgentFrameworkExtensions(Protocol):
    def evaluate_agent(self, ...) -> EvalResults: ...
    def workflow_with_checkpoint(self, ...) -> WorkflowAgent: ...
    # eval + workflow + compaction primitives
```

Skills/orchestrator code uses Protocol-typed Substrate; substrate-specific primitives accessed via substrate's extensions interface (cast/type-narrow at use site).

## Recommendations

### R1: Adopt PRIMITIVES-ONLY from BOTH substrates regardless of primary choice

Per the SDK deep-read, BOTH substrates have value-adds worth adopting selectively:

- From **Claude Agent SDK** (primary substrate): in-process MCP server pattern (R3a); permission primitives (R3c); subagent primitives where workflow naturally fits (R3d); session forking for explore-alternatives scenarios
- From **MS AF** (secondary substrate but also adopt-as-primitives): evaluation framework (R3b — Phase 0 item 5); compaction strategies (long-running session viability)

This is the "primitives-only adoption from one or more" outcome named in #18's "Constraints flowing if all rejected" clause — but applied to ADOPTED substrates, not rejected ones. Rationale: each substrate has primitives the other lacks; adopting both as substrates AND as primitives-source doubles the leverage.

### R2: Substrate Protocol shape — NARROWER common surface + per-substrate extension Protocols

Per "Insight 2" above. Common surface = ~5-6 methods. Per-substrate extensions accessed via typed extension interfaces. Lands in #9 implementation as architectural foundation.

### R3: Specific refactor recommendations (with bundled commitments)

| Refactor | What | Lands with |
|---|---|---|
| 3a | PBS-mcp → in-process MCP server (Claude Agent SDK pattern) | #11 (Cowork integration / Claude Agent SDK substrate runtime) |
| 3b | MS AF eval primitives → testing methodology | Phase 0 item 5 (testing methodology + harness) |
| 3c | Permission primitives → governance gate / sparring backstop | #9 (entity gate) + #6 (audit-trail v2 retrofit — sparring schema integration) |
| 3d | Subagent pattern for explore-alternatives scenarios | Case-by-case as workflows surface need (no specific bundling) |

### R4: Criterion 1 verdict for MS AF refined

#18's screen verdict: MS AF passes criterion 1 ("MCP-native at 1.0; not bolt-on"). This DR refines to: **PASS WITH NUANCE** — MS AF treats MCP as one tool type among many (`MCPStdioTool`, `MCPStreamableHTTPTool`, `MCPWebsocketTool`), not as primary contract surface like Claude Agent SDK. Doesn't flip the recommendation (Claude Agent SDK already chosen as primary for ecosystem alignment); does refine the architectural understanding.

### R5: NO criterion-2 (hybrid-shape) re-evaluation needed

Both substrates use SKILL.md format for Agent Skills — this DR confirmed. Hybrid-shape compatibility holds for both.

## Defers

| Defer | Home | Specific cost being avoided (chronological) |
|---|---|---|
| **D1**: Detailed PBS-mcp → in-process refactor implementation | #11 implementation phase (Cowork integration) | Refactor needs Substrate Protocol implementation in place + Claude Agent SDK substrate runtime active; both land later in queue |
| **D2**: MS AF eval primitives integration | Phase 0 item 5 (testing methodology design) | Design needs to settle eval-result schema + scenario format BEFORE primitive adoption; can't pre-bind |
| **D3**: Detailed code-reads of `_middleware.py`, `_skills.py`, `client.py`, `_workflows/`, etc. | Per-implementation-phase as substrate primitives are adopted | Detailed reads benefit most from concrete-use-context; blanket reads now = potential YAGNI |
| **D4**: Substrate-specific extension Protocol shapes | #9 implementation (Substrate Protocol design) | Extension shapes designed alongside Substrate Protocol; can't pre-design without context |

Each defer names specific home + specific chronological cost. Per `feedback_pattern_not_instance_defers.md`: chronological-valid (info-gap), not up-front-cost.

## Constraints flowing to downstream commitments

### → #9 (Substrate Protocol design + entity gate)

- Substrate Protocol shape per Insight 2 (narrower common surface + per-substrate extension Protocols)
- Permission primitives adopted (R3c) — entity gate write-authorization checks use Claude Agent SDK permission primitives when on that substrate
- In-process MCP server pattern available for Claude Agent SDK substrate (R3a)
- Pydantic structured output + auto-retry available across both substrates (R5 confirmed)

### → #11 (Cowork integration plugin agents)

- PBS-mcp refactor to in-process pattern (R3a) lands here
- Skills consume Substrate Protocol abstraction; Claude Agent SDK substrate is primary deployment

### → #6 (audit-trail v2 retrofit)

- Permission primitives integration (R3c) for sparring backstop hooks
- AuditEvent emission could compose with Claude Agent SDK hooks (PreToolUse/PostToolUse return values become AuditEvent details)

### → Phase 0 item 5 (testing methodology + harness)

- MS AF eval primitives adoption (R3b) — substantial leverage; saves rebuilding from scratch
- EvalRun / Scenario / EvalResult / RegressionSuite Pydantic contracts can be MS AF's `EvalItem` / `EvalScoreResult` / `EvalResults` / `Evaluator` Protocol — adopt directly OR wrap as our schemas

### → #22 (terminology + level-boundary re-evaluation)

- SDK terminology (subagents / sessions / skills / workflows / agents) might inform terminology re-eval analysis
- E.g., "subagent" as concept could surface a parallel to our "skill" or "department" — pattern-vs-instance question becomes "is our terminology PBS-instance OR could it borrow from SDK conventions for broader fit?"

## Files touched (session 12 — #21 SDK deep-read)

- `docs/decisions/sdk-deep-read.md` — this file (NEW; status ACCEPTED)
- `~/dev/reference/claude-agent-sdk-python/` (cloned)
- `~/dev/reference/agent-framework/` (cloned)
- `HANDOFF.md` — session-12 progress note (after this session closes)

No code changes this session. Findings inform future implementation work per the constraints-flowing section above.

## Revisit triggers

- **Detailed code-read** of specific files (`_middleware.py`, `_skills.py`, `_workflows/`, `client.py`, `query.py`, etc.) when adoption of specific primitives proceeds
- **SDK major-version updates** (Claude Agent SDK 0.2.x; MS AF 1.x.x) — re-verify findings; check for new primitives
- **First implementation surfaces friction** — primitives that looked good on paper might not fit in practice; revisit recommendations
- **MS AF eval primitives evaluation** at Phase 0 item 5 design — confirm or revise R3b adoption recommendation
- **Substrate Protocol common-surface design** at #9 implementation — refine Insight 2's proposed shape with implementation reality
