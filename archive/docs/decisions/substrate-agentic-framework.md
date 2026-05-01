# Decision record: Agentic framework substrate evaluation (#18)

**Status**: ACCEPTED — session 12 (2026-04-30) framing + disqualifying screen + verification pass + deep-eval + recommendation. Final lock + downstream constraint authoring scheduled session 13 (was 14 — compressed by max-effort session 12).
**Owner**: ROADMAP commitment #18; ARCHITECTURE.md "Pattern-vs-instance discipline" + "Make wrong shapes impossible" + "AI-as-runtime hybrid-shape principle"
**Related**: `greenfield-architecture-review.md` (§3 — disqualifying criteria CONSUMED by this DR; produced session 11), `ai-as-runtime-hybrid-shape.md` (#16 — hybrid-shape contract that substrate must support), `office-vs-department.md` (#12 — Gap A scheduler + Gap B adapter callbacks future-event capabilities), `mcp-fallback-policy.md` (fail-closed corollary — substrate must compose with MCP gate as primary contract surface), `a2a-and-gemini-pattern-emulation.md` (#10 — A2A interop concerns; substrate-pluggability informs Tier 3 reframing — see "Counter-consideration: Tier 3 implications" below)

**Sibling evaluations (parallel BLOCKING)**: #19 (LlamaIndex pluggable RAG eval), #20 (PydanticAI eval — demoted from BLOCKING tier per session-11 ultrathink-review). This DR addresses the broadest-surface evaluation; results constrain implementation phases of #9 (entity gate), #11 (Cowork plugin agents), #13 (deployment flexibility / transport / observability).

## Context

Session 11 surfaced the substrate question — "why don't we build on agentic frameworks?" — combined with the corrected counterfactual "we started 2 days ago, full refactor when it's a win is the explicit tenet" (session-7 #11 directive, applied at architecture scope). This forced honest re-evaluation of whether to build the #9 entity gate + #11 plugin agents + #13 transport on hand-rolled Python + MCP + Pydantic, or on top of a substrate framework.

Substrate choice influences the Python implementation of every downstream pre-RAG commitment. Doing the eval after locking implementation choices means retrofitting under sunk-cost pressure. Doing it now, at 2-days-in scale, is the cheap window. Pre-launch deprecation discipline is essentially free (per ARCHITECTURE.md "Maintenance discipline" deprecation procedure).

Session 11 also produced `greenfield-architecture-review.md` §3 — a tightened disqualifying-criteria set derived from VISION + the named architectural disciplines. The eval transforms from "comprehensive comparison of 8 frameworks" (initial scope) to "reject obvious mismatches first; deep-eval the 2-4 survivors." That tightening is what this DR consumes as input.

This DR was structured to fit the time-boxed 2-3 session scope (per ROADMAP #18 + scope-creep guard from session-11 ultrathink-review): session 12 = framing + disqualifying screen + verification pass + deep-eval + recommendation (compressed from initial 3-session plan into max-effort session 12); session 13 = final lock + downstream constraint authoring.

**Session 12 web-verification surfaced two candidates that didn't exist when session-11 set the eval scope**: Claude Agent SDK (Anthropic's renamed Claude Code SDK) and Strands Agents (AWS, with Anthropic explicit contributor). Per scope-creep guard's allowed trigger ("framework X just shipped major release that changes the gap analysis qualifies"), both added to the screen. Total candidates evaluated: 10 (original 8 + 2 new). Survivor count after deep-eval narrows to **4** (Claude Agent SDK + MS AF + Strands + hand-rolled baseline; LangGraph downgraded to disqualified post-deep-eval on criterion 2). Skipping Anthropic's-own SDK in particular would have been a glaring blind spot for an Anthropic-ecosystem-aligned project.

## The 9 disqualifying criteria (from `greenfield-architecture-review.md` §3)

A candidate must pass ALL of these. Failing any → automatic disqualification, NO deep-eval.

| # | Criterion | Source discipline | Failure mode if violated |
|---|---|---|---|
| **1** | **Composes with MCP natively** (MCP server as primary contract surface, not awkwardly wrapped) | Anthropic ecosystem (Claude Code dev runtime + Cowork end-user runtime) + meta-rule 4 (gate boundary) | Framework wraps MCP awkwardly → ecosystem alignment lost; tool-use stops being primary; Cowork integration breaks |
| **2** | **Supports hybrid-shape** (markdown bodies as runtime fuel; not prompt-templating that flattens prose) | AI-as-runtime hybrid-shape (v0.16) | Framework treats prose as text-input only → SQL-DB-trap by default; entity-md spec can't compose |
| **3** | **Pydantic-native or Pydantic-compatible** (not a competing type system) | Strict-validation discipline + meta-rule 4 + #16 | Framework's type model competes with ours → dual maintenance, validation discipline weakens |
| **4** | **Doesn't force SQL-DB shapes** (no relational entity model assumed) | AI-as-runtime + entity-elevation 3-test | Framework assumes entity-per-noun + foreign keys → catastrophic for LLM-mediated systems; entity-elevation discipline broken |
| **5** | **Composable with sparring patterns** (counter-argument validation hooks, anti-sycophancy hooks, asymmetric knowledge respect, output-schema validation) | VISION axis 2 + sparring-output-v1 | Framework optimizes for autonomy/oracle-mode → can't backstop axis 2 without fighting framework |
| **6** | **Audit-trail-as-canonical-source compatible OR extensible** | VISION axis 3 + audit-trail-v2 | Framework imposes its own logging/state model → audit chain breaks; reasoning reconstruction lost |
| **7** | **Pluggable transport** (stdio + HTTP) OR transport-agnostic | Per #13 deployment flexibility | Framework hardcodes one transport → Tier 1 ↔ Tier 2 portability lost |
| **8** | **Heaviness scales appropriately** across 1-person shop / small company / enterprise (operational AND cognitive sub-axes) | Consulting framework target spectrum | Framework forces enterprise complexity at all tiers OR forces minimal complexity at all tiers → wrong for ≥2 of 3 deployment tiers |
| **9** | **Anthropic ecosystem aligned OR vendor-neutral** (not Microsoft / Google / OpenAI lock-in via SDK) | Glue-not-replacement + ROADMAP v2 multi-archetype consulting positioning | Framework couples to vendor → multi-archetype consulting story breaks |

Plus two future-roadmap items the substrate must compose with (per HANDOFF Section "BLOCKING SUBSTRATE EVALUATIONS" + ROADMAP #18):

- **Gap A — Time-driven triggers** (per #12 infrastructure-primitive review): server-side scheduler firing "tick" events. Substrate must compose, not impose competing scheduler abstraction.
- **Gap B — Event-driven adapter callbacks**: adapter Protocol's `subscribe_to_changes(callback)` (push) OR `poll_for_changes() -> list[Event]` (pull) per #9 Bundle E. Substrate must compose with adapter callback pattern.

These are evaluated as part of criterion 1 + 5 + 6 (composability).

## Heaviness sub-axes × deployment scales

Per ROADMAP #18 + session-11 user direction: heaviness has TWO sub-axes that must be evaluated separately because frameworks vary differently along each:

- **Operational heaviness**: boot time, memory footprint, runtime deps, observability cost when nobody's watching, deployment complexity. Easily measured.
- **Cognitive heaviness**: framework-specific abstractions a developer must learn before being productive. Harder to measure but real (especially for 1-person shops where the user IS the developer + the operator).

× Three deployment scales:

- **1-person shop** (Gunther's PBS today; future single-skill-utility shapes like brand-voice)
- **Small company** (5-20 person consulting client on Tier 2 cloud)
- **Enterprise** (100+ users, Tier 3 / enterprise multi-agent A2A platform)

**Critical question**: does the heaviness scale automatically? Some frameworks have configuration-driven scaling (lightweight defaults, opt-in to enterprise primitives). Others require enterprise-grade deps regardless of deployment size.

## Disqualifying screen — per-candidate verdict

Knowledge cutoff: January 2026. Eval date: 2026-04-30. Web-verification pass complete session 12.

### Bucket: Anthropic ecosystem (added session 12 — surfaced via verification pass)

#### Claude Agent SDK (Anthropic) — **SURVIVES (deep-eval, strongest fit)**

Renamed from Claude Code SDK; powers Claude Code itself + most of Anthropic's internal agent loops. Python + TypeScript. Released as production framework in 2026.

| Criterion | Verdict | Reasoning |
|---|---|---|
| 1. MCP-native | ✅ DEEPEST | "Attach MCP servers directly to an agent definition; framework handles connection lifecycle and capability negotiation automatically" — first-class by construction (Anthropic invented MCP) |
| 2. Hybrid-shape | ✅ STRONG | Skills are markdown injected into system prompt at runtime; Claude reads SKILL.md from filesystem on demand; same SKILL.md format we'd write anyway |
| 3. Pydantic-compatible | ✅ STRONG | `.model_json_schema()` for structured outputs; SDK forces Claude to return matching schema; auto-retries on validation fail |
| 4. No SQL-DB shapes | ✅ | Stateful sandboxed runtime per agent; not entity tables |
| 5. Sparring composable | ✅ STRONG | `RunHooks` lifecycle: `on_agent_start`, `on_tool_start`, `on_tool_end`, `on_agent_end` + PRE/POST tool hooks (PRE_TOOL_USE / POST_TOOL_USE) |
| 6. Audit-trail compatible | ✅ | Sessions are JSON files (composable with our AuditEvent); ephemeral by default = good fit (we control persistence via entity-md + audit-trail-as-canonical-source) |
| 7. Pluggable transport | ✅ | Via MCP (multiple transports) |
| 8. Heaviness scales | ⚠ MEDIUM | 1 GiB RAM / 5 GiB disk / 1 CPU recommended; Python 3.10+ + Node.js 18+ + Claude Code CLI via npm; cognitively familiar (powers Claude Code we already use) |
| 9. Vendor-neutral | ✅ by ecosystem alignment | Anthropic ecosystem alignment IS the goal of Tier 1-2 architecture |

**Gap A + Gap B native**: Claude Code Routines (cloud-hosted scheduler, runs even when laptop off) for Gap A; Channels (Telegram/Discord/webhook push) for Gap B. Both compose natively.

**Verdict**: SURVIVES, strongest candidate. Anthropic ecosystem alignment by construction. Powers Cowork (planned end-user runtime). SKILL.md format = already-our-format.

### Bucket: Enterprise-grade

#### MS Agent Framework (Microsoft) — **SURVIVES (deep-eval, strong-fit)**

1.0 GA April 3, 2026 as Microsoft's consolidated successor to Semantic Kernel + AutoGen. Python + .NET both at 1.0 GA.

| Criterion | Verdict | Reasoning |
|---|---|---|
| 1. MCP-native | ✅ NATIVE at 1.0 | Not bolt-on; `Agent.as_mcp_server()`; improved connection-loss + pagination at 1.0 |
| 2. Hybrid-shape | ✅ STRONG | Agent Skills uses SKILL.md format = "Agent Skills open standard" working with Claude Code, GitHub Copilot, Cursor, Gemini CLI, Codex CLI. **Industry convergence on the SAME hybrid-shape pattern Anthropic plugins use** |
| 3. Pydantic-compatible | ✅ STRONG | Pydantic schemas via `ResponseFormat` |
| 4. No SQL-DB shapes | ✅ | Agents + workflows + messages, not entity tables |
| 5. Sparring composable | ✅ STRONG | Three-layer middleware (agent / function / chat) + HITL approval via `ApprovalRequiredAIFunction` |
| 6. Audit-trail compatible | ✅ | OpenTelemetry-first observability composes with AuditEvent |
| 7. Pluggable transport | ✅ | Multiple transports for agent communication |
| 8. Heaviness scales | ⚠ MEDIUM-HEAVY | `agent-framework-core` "intentionally minimal"; selective install possible; "5 lines to first agent" but workflow + checkpointing concepts add cognitive load |
| 9. Vendor-neutral | ✅ CONFIRMED | Multi-provider connectors (Foundry / Azure OpenAI / OpenAI / Anthropic Claude / Bedrock / Gemini / Ollama); selective install avoids Azure deps |

**Gap A + Gap B native**: "Event-driven workflows monitor triggers such as file uploads, database changes, and scheduled jobs and invoke agents." Both natively supported.

**Verdict**: SURVIVES — strong-fit. Most criteria PASS confirmed in verification.

### Bucket: Lightweight

#### Strands Agents (AWS, Anthropic contributor) — **SURVIVES (deep-eval)**

Open-sourced by AWS specifically to address vendor-lock concerns. Anthropic explicit contributor. Multi-provider.

| Criterion | Verdict | Reasoning |
|---|---|---|
| 1. MCP-native | ✅ | "Choose from thousands of published MCP servers" |
| 2. Hybrid-shape | ✅ STRONG | **Agent SOPs** — `.sop.md` markdown workflow files with RFC 2119 keywords (MUST/SHOULD/MAY); plus Skills. SAME hybrid-shape pattern as Anthropic plugins / MS AF Agent Skills. "Determin-ish-tic" framing = between code-defined workflows and open-ended model-driven |
| 3. Pydantic-compatible | ⚠ verify | Python SDK; type model not deeply verified |
| 4. No SQL-DB shapes | ✅ | Lightweight model-driven design |
| 5. Sparring composable | ⚠ verify | Lightweight = thin abstractions; verify hook surface in deep-eval |
| 6. Audit-trail compatible | ⚠ verify | AWS observability natural for AgentCore deployments; opt-out for non-AWS deployment unclear |
| 7. Pluggable transport | ✅ | MCP-native + model-agnostic |
| 8. Heaviness scales | ⚠ verify | Lightweight at solo tier ✅; scale-up question |
| 9. Vendor-neutral | ✅ (with caveat) | AWS open-sourced specifically to address vendor-lock; Bedrock = default config not hard dep; runs on-prem + other clouds |

**Verdict**: SURVIVES. Lightweight bucket fill (Smolagents couldn't fill). Anthropic-contributor weakens AWS-coupling concern.

### Bucket: Mid-weight (DISQUALIFIED post-deep-eval)

#### LangGraph (LangChain) — **DISQUALIFIED on criterion 2** (downgraded session 12 deep-eval)

Initial screen marked SURVIVES with criterion 2 VERIFY tag. Deep-eval verification: LangGraph's prompt model is **PromptTemplate-based with placeholders** ({user_input}, {history}, {context}). System message is "default system prompt provided in prompts.py, updated via context." Markdown is OUTPUT format, not input runtime fuel.

| Criterion | Verdict | Reasoning |
|---|---|---|
| 2. Hybrid-shape | ❌ FAIL | PromptTemplate model with placeholders, NOT runtime-fueled markdown bodies. **Same architectural problem as CrewAI** — prose treated as template-input, not as `Claude reads SKILL.md from filesystem at runtime`. State-machine layer handles graph flow; prompt model underneath is still LangChain's templating |
| 1. MCP-native | ⚠ adapter-shaped | Via `langchain-mcp-adapters` package; production-ready wrapper but not first-class. Less native than Claude Agent SDK / MS AF |
| 6. Audit-trail compatible | ✅ | LangSmith opt-in via `LANGSMITH_OTEL_ENABLED`; custom callback handler; `LANGCHAIN_TRACING_V2` opt-out |

**Verdict**: DISQUALIFIED. Criterion 2 fail confirmed. Sparring counter-argument from initial screen ("LangGraph more state-machine-centric than LangChain heritage") doesn't hold; the state machine doesn't change the prompt-template fundament.

#### CrewAI — **DISQUALIFIED**

Three independent criteria fail (hybrid-shape + sparring + heaviness). See initial screen for detail.

### Bucket: Lightweight (DISQUALIFIED)

#### Smolagents (HuggingFace) — **DISQUALIFIED**

Doesn't scale UP without reimplementing primitives. Strands fills the lightweight bucket gap with better scale-up posture.

#### OpenAI Swarm / Agents SDK — **DISQUALIFIED**

Vendor-locked (OpenAI = both framework + model vendor through SDK idioms); MCP secondary.

### Bucket: Subsumed (DISQUALIFIED)

#### Semantic Kernel (Microsoft) — **DISQUALIFIED**

MS AF supersedes for new builds. SK going forward is legacy.

#### AutoGen (Microsoft) — **DISQUALIFIED**

Subsumed by MS AF. AutoGen's `selector` patterns + group chat shape preserved IN MS AF.

### Bucket: Hand-rolled (baseline)

#### Hand-rolled (Python + MCP + Pydantic) — **SURVIVES (baseline)**

| Criterion | Verdict | Reasoning |
|---|---|---|
| 1-9 | ✅ All pass by construction | We built it to satisfy our disciplines |

**Verdict**: SURVIVES as comparison baseline. Win-margin question — do substrates give substantial enough primitives to justify lock-in cost?

## Screen verdict — survivors after deep-eval

| Candidate | Verdict | Strength |
|---|---|---|
| **Claude Agent SDK** | ✅ STRONGEST FIT | Ecosystem alignment by construction; deepest MCP; SKILL.md format; RunHooks |
| **MS Agent Framework** | ✅ STRONG FIT | SKILL.md convergence; multi-provider; middleware sparring; Gap A + B native |
| **Strands Agents** | ✅ SURVIVES | Lightweight bucket fill; SOPs + Skills hybrid-shape; multi-provider; Anthropic-contributor |
| **Hand-rolled** | ✅ SURVIVES (baseline) | Win-margin reference for substrate adoption |
| ~~LangGraph~~ | ❌ DISQUALIFIED | Criterion 2 fail (PromptTemplate-centric, not runtime-fueled markdown) |
| Semantic Kernel / AutoGen / CrewAI / Smolagents / OpenAI Swarm | ❌ DISQUALIFIED | (per individual screens above) |

## Verification pass — RESOLVED session 12 (web-research)

Knowledge cutoff Jan 2026 vs eval date April 2026 = ~3-month gap.

**Sources (initial verification + deep-eval pass)**:
- [microsoft/agent-framework GitHub](https://github.com/microsoft/agent-framework)
- [MS Agent Framework 1.0 release blog](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [MS AF Using MCP Tools](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-tools)
- [MS AF Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills)
- [MS AF Workflows + Checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/)
- [MS AF Structured Outputs](https://learn.microsoft.com/en-us/agent-framework/agents/structured-outputs)
- [MS AF Agent Middleware](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-middleware)
- [MS AF Human-in-the-Loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)
- [In Agentic AI, It's All About the Markdown — VS Magazine 2026-02-24](https://visualstudiomagazine.com/articles/2026/02/24/in-agentic-ai-its-all-about-the-markdown.aspx)
- [LangGraph + MCP composition](https://changelog.langchain.com/announcements/mcp-adapters-for-langchain-and-langgraph)
- [LangSmith OpenTelemetry support](https://docs.langchain.com/langsmith/trace-with-opentelemetry)
- [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)
- [Claude Agent SDK Python reference](https://platform.claude.com/docs/en/agent-sdk/python)
- [Claude Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Run prompts on a schedule (Claude Code)](https://code.claude.com/docs/en/scheduled-tasks)
- [Building agents with Claude Agent SDK — Anthropic](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Strands Agents — strandsagents.com](https://strandsagents.com/)
- [Strands Agents — AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/)
- [Strands Agent SOPs](https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/)
- [Strands Skills](https://strandsagents.com/docs/user-guide/concepts/plugins/skills/)
- [Strands SDK technical deep dive — AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/)
- [2026 AI Agent Framework Showdown — QubitTool](https://qubittool.com/blog/ai-agent-framework-comparison-2026)

## Counter-consideration: runtime shape, model-swap-ability, and Tier 3 implications

**Surfaced session 12** by user question: "using these frameworks can we still do claude (or if the need arises another model) as the runtime as is planned right now? or would we have to do api calls for agents?"

This is load-bearing analysis the initial screen missed.

### Two architectural shapes

**Shape A — Claude IS the runtime (current PBS)**:
- Claude Code (or Cowork) loads plugin
- User converses with Claude
- Claude executes orchestrator skill, calls MCP tools, runs the workflow
- The Claude conversation IS the agent loop

**Shape B — Python program IS the runtime**:
- Python program imports framework, configures agent (model + tools + prompts)
- Program runs the agent loop in code
- Calls model API for LLM reasoning
- User interacts with the program (CLI, web UI, etc.)

### Per-framework runtime shape + model-swap-ability

| Framework | Shape A possible? | Model swap (Claude → GPT/Gemini) |
|---|---|---|
| **Hand-rolled** | ✅ Yes (current) | ❌ Hard — locked to Claude Code (Anthropic-only). Switching = rewrite |
| **Claude Agent SDK** | ✅ Yes (it IS Claude Code programmatically) | ❌ Hard — SDK is Anthropic-only by construction |
| **MS Agent Framework** | ❌ No (Shape B) | ✅ Trivial — multi-provider native |
| **Strands** | ❌ No (Shape B) | ✅ Trivial — multi-provider |
| **LangGraph** (DQ) | ❌ No (Shape B) | (n/a — disqualified) |

**Adopting MS AF / Strands as substrate = ARCHITECTURAL SHAPE PIVOT** from Shape A to Shape B. Implications:
- **Cowork integration (#11) becomes awkward** — Cowork is Claude's runtime (Shape A); Python program would be SEPARATE user surface
- **New user surface required** — CLI / web UI / something
- **Gain model-swap-ability** at the cost of architectural simplicity

**Adopting Claude Agent SDK = STAYS IN Shape A** + adds programmatic capability. Locked to Claude at model layer — but per existing architecture, **Tier 1-2 is already model-locked to Anthropic**. Tier 3 = different archetype = different substrate is the documented escape valve.

### Honest framing of the trade-off

| | Path A (Claude Agent SDK) | Path B (MS AF) |
|---|---|---|
| Integration depth | ✅ Anthropic ecosystem (Claude + Claude Code + Cowork + MCP) | API-only to model provider; **but coupled to Microsoft's infrastructure layer** (Azure AI Foundry deployment) |
| Runtime setup | ✅ Open Claude Code, plugin loads | New user surface needed (web UI? CLI?) — design + build cost |
| Infrastructure cost | Backend Python + MCP + persistence (we have this) — **no agent-loop infrastructure** | Backend + Python program runtime + framework deps + observability + user surface — substantially heavier |
| Model flexibility | ❌ Locked to Claude (matches existing arch) | ✅ Pluggable: Claude / Gemini / GPT / Bedrock / Ollama |
| Tier 3 path | Separate Tier 3 substrate effort (multi-archetype credibility move per existing roadmap) | MS AF natively supports multi-agent A2A archetype; Tier 3 partly subsumed |
| Vendor lock | Anthropic at model layer | **Microsoft at infrastructure layer** (you're trading lock targets, not eliminating lock) |

The "API only" framing for Path B is precise — but the trade-off isn't "Anthropic-locked vs vendor-neutral." It's "Anthropic-locked at MODEL layer (Path A)" vs "Microsoft-coupled at INFRASTRUCTURE layer (Path B)."

### Tier 3 implications — pattern-vs-instance reframing

MS AF natively supports the Tier 3 archetype (multi-agent A2A protocol native at 1.0; multi-agent orchestration patterns built-in). **This forces a pattern-vs-instance reframing of the existing Tier 3 plan.**

Current ROADMAP framing: "Tier 3 = Gemini Enterprise port" (specific instance).

Pattern-corrected framing: "Tier 3 = enterprise multi-agent A2A platform" (Gemini Enterprise / Azure AI Foundry / AWS Bedrock AgentCore as instances). Gemini Enterprise was the canonical exemplar — credibility-flow target since Anthropic Claude is in Gemini's Model Garden — but not the only valid instance.

This reframing applies **regardless of substrate choice** — even with Claude Agent SDK at Tier 1-2, the Tier 3 destination is platform-pluggable. With MS AF at all tiers, Tier 3 becomes "MS AF on whichever enterprise platform fits the consulting client" — partly subsumed by substrate choice.

ROADMAP "Gemini Enterprise port + parallel development — Tier 3 of deployment ladder" + `a2a-and-gemini-pattern-emulation.md` need pattern-corrected reframing per this analysis. See "Constraints flowing" → ROADMAP + Tier-3 section below.

## Hybrid analysis: dual-substrate architecture (key enabler)

**Substrate-pluggability is achievable with modest additional cost** because most of PBS architecture is already substrate-agnostic.

### Architectural layers

| Layer | Substrate-specific? | Same code across substrates? |
|---|---|---|
| Pydantic models (entity-md, AuditEvent, schemas) | No | ✅ Same |
| MCP gate layer (read_entity / write_entity / record_audit_event etc.) | No (MCP is a protocol) | ✅ Same |
| Skill content (SKILL.md markdown bodies) | No (industry convergence on SKILL.md format — Anthropic plugins + MS AF Agent Skills + Strands Skills all use this format) | ✅ Same |
| Persistence (entity-md files, audit-trail-as-canonical-source) | No (we control) | ✅ Same |
| Audit-trail (jsonl + render_audit_trail) | No | ✅ Same |
| Process-as-md, conventions, governance | No (markdown bodies AI reads at runtime) | ✅ Same |
| **Agent loop / orchestrator** | **YES** | ❌ Per-substrate implementation |
| **Sparring hooks** | **YES** | ❌ Per-substrate implementation (RunHooks vs middleware) |
| **User runtime / surface** | **YES** | ❌ Per-substrate (Cowork plugin vs Python program + UI) |

**~70-80% of the work transfers between substrates.** Substrate-specific work concentrated in 3 layers: agent loop + hooks + user runtime.

### Substrate Protocol pattern (NEW)

To make substrate-pluggability structural (per "Make wrong shapes impossible" v0.21), define explicit `Substrate` Protocol (Pydantic Protocol):

- Substrate-coupled methods: agent loop primitives, sparring hook interface, user-runtime adapter
- Concrete implementations swap at composition root
- Substrate Protocol satisfaction = structural; substrate-coupling in core code = impossible-by-construction

This is the pattern-level framework move (per "Pattern-vs-instance discipline" v0.20): substrate IS a pattern; specific frameworks are instances. Architecture should name the pattern explicitly via Protocol, not implicitly via "we happen to use only Pydantic + MCP which happens to be substrate-agnostic."

## Recommendation — Dual-substrate full-backend, single-frontend ship

> **Adopt Claude Agent SDK as primary substrate (full backend + frontend = Cowork plugin via #11). Build full backend implementation for MS AF as second substrate (orchestrator on middleware + sparring hooks via 3-layer middleware translation + Gap A/B via event-driven workflows). Substrate-pluggability via explicit `Substrate` Protocol (NEW architectural pattern). Defer Path B frontend (web UI / CLI / Cowork-equivalent for Shape B clients) to consulting signal.**

### What ships at session 12 + downstream pre-RAG work

**Substrate Protocol** (NEW pattern): Pydantic Protocol defining substrate-specific surface. Lands in #9 implementation as architectural foundation.

**Claude Agent SDK substrate** — FULL implementation:
- Orchestrator agent loop on Claude Agent SDK primitives
- Sparring hooks via RunHooks (PRE/POST tool + lifecycle callbacks)
- Schedule via Claude Code Routines (Gap A; cloud-hosted)
- Event-driven via Channels (Gap B; webhook + push)
- User runtime = Claude Code (dev) + Cowork plugin (end-user) per #11

**MS Agent Framework substrate** — FULL backend implementation:
- Orchestrator on MS AF agent middleware
- Sparring hooks via 3-layer middleware (agent / function / chat) translation from RunHooks pattern
- Schedule + event-driven via MS AF event-driven workflows
- Substrate Protocol satisfied with WORKING code (not stubs)
- Integration tests parity-validated across both substrates

**Path B frontend** — DEFERRED (chronological-valid):
- New user runtime design (web UI / CLI / something for Shape B deployment)
- Cowork-equivalent for Shape B clients OR explicit decision Shape B = different surface
- Triggered by: consulting client signal for non-Anthropic deployment

### Why this shape

1. **Pattern-vs-instance discipline fully satisfied** — Substrate Protocol is the pattern; Claude Agent SDK + MS AF are first-class instances
2. **Make wrong shapes impossible (v0.21)** — explicit Substrate Protocol structurally enforces substrate-pluggability vs implicit accidental swappability
3. **Substrate Protocol genuinely validated** — designed against TWO concrete implementations catches abstraction bugs the stub-version would mask
4. **Honest defer per sharp defer rule (v0.20)** — Path B frontend defers to consulting-client signal (info that doesn't exist yet); MS AF backend = current-scope framework infrastructure (would-be-needed-at-first-bind for Microsoft-shop consulting client)
5. **Multi-archetype consulting pitch becomes verifiable claim NOW** — "we built our framework substrate-pluggable; full backend on Claude + MS AF; ship on Anthropic at Tier 1-2 today; deliver Tier 3 or non-Anthropic Tier 1-2 on your preferred enterprise platform when needed"
6. **Tier 3 implications clean** — substrate-pluggability + Tier 3 reframing compose: Tier 3 = enterprise multi-agent A2A platform (Gemini / Azure / AWS); substrate (Claude Agent SDK or MS AF) determines deployment shape
7. **Future Path B deployment = "build a frontend" only** (~1-2 weeks engineering when consulting signal arrives), not "implement substrate" (~3-5 sessions saved by current backend work)

### Cost estimate

Additional work over Claude-Agent-SDK-only:
- ~2-3 sessions: MS AF orchestrator on agent middleware
- ~1 session: sparring hooks via 3-layer middleware translation (patterns map cleanly)
- ~1-2 sessions: integration tests + parity validation
- **Total: ~4-6 sessions added to current scope**

In return:
- Substrate Protocol tested with two real implementations
- Architecture genuinely substrate-pluggable (not just claimed)
- Future Path B deployment = "build a frontend" only
- Multi-archetype consulting pitch becomes verifiable claim NOW

### Counter-arguments engaged

**"Why not just do MS AF now, get model-pluggability, avoid future migration cost?"** Counter: future migration cost isn't free — it's ~5-10 sessions IF needed. Doing MS AF NOW costs: pivot Cowork integration (#11 redesign); build new user surface design + implementation NOW (1-2 weeks); slower path to validating PBS in real planning bureau use; consulting clients who DO want Anthropic ecosystem (likely majority given Cowork's marketing reach) get a less-natural product. Expected value of paying flexibility cost upfront only pays off IF most consulting clients demand non-Claude — not likely distribution given Anthropic's ecosystem position.

**"What if Claude Agent SDK turns out heavier than expected at scale?"** Counter: if real friction emerges at small-co or enterprise scale post-#11, primitives-only fallback is available; substrate decision is reversible at #13 (deployment flexibility lands anyway). And: Anthropic's Cowork = our end-user runtime = same SDK underneath.

**"Lock-in to Anthropic at model layer"** Counter: Anthropic IS our model + ecosystem at Tiers 1-2 (already locked architecturally). Adopting Claude Agent SDK doesn't change vendor posture; it strengthens already-chosen alignment. Tier 3 = different archetype = different substrate regardless.

**"MS AF has more enterprise primitives"** Counter: yes (workflow engine, checkpointing, hydration), but at the cost of cognitive heaviness for solo + small-co tiers. Win-margin of MS AF over Claude Agent SDK is mostly enterprise-tier. By having BOTH backends, enterprise-tier deployment can use MS AF substrate when warranted; solo + small-co stays on Claude Agent SDK.

**"5 survivors instead of predicted 2-4"** Counter: chronological-valid scope expansion. Claude Agent SDK + Strands didn't exist when scope was set in session 11. Per scope-creep guard's allowed trigger ("framework X just shipped major release"), both qualify. After deep-eval, narrows to 4 (LangGraph downgraded to disqualified on criterion 2).

## Pattern-vs-instance check on the eval itself

Is this eval pattern-level or PBS-instance? The METHOD (greenfield-criteria → screen → verification → deep-eval → recommendation → decision-record) is pattern-level — any AI-office deployment could run the same eval at substrate-choice moments. The CONTENT (which 10 frameworks evaluated, which screens passed, which substrates recommended) is framework-instance + circa-Apr-2026 industry-instance.

The Substrate Protocol pattern itself is pattern-level — applies to any AI-office substrate-choice scenario. Generalizes to other deployments: a legal-practice or research-lab AI office in the v2 builder era could run the same eval against then-current frameworks; the criteria stay valid (rooted in VISION axes + named disciplines), the candidates change, the Substrate Protocol pattern stays.

## Status archive + watch-list + process commitments (re-examined session 15 under v0.33 no-defer principle)

> **Session 15 amendment**: previously this section was titled "Defers (per defer-instinct discipline + sharp defer rule v0.20)". Under v0.33 no-defer principle, re-examined: D1+D2 are completed (not defers anymore); D4 is process commitment (not a defer); D3+D5 are valid watch-list entries.

### Completed (status archive)

| Item | Completion |
|---|---|
| Deep-eval of survivors (was D1) | ✅ COMPLETED session 12 (compressed from session 13 schedule into max-effort session 12) |
| Final substrate decision (was D2) | ✅ COMPLETED session 12 — recommendation locked (compressed from session 14 schedule) |

### Watch-list entries

| W# | Concrete decision currently un-makeable | Awaiting external signal | Resolution mechanism |
|---|---|---|---|
| **W3 (was D3)**: Re-verification of disqualified candidates | User request OR survivor deep-eval surfaces disqualifying-criterion blind spot | When signal arrives, re-evaluate the disqualified candidate(s) against current criteria. Re-verification without specific signal = manufactured rigor (own framing); valid watch-list. |
| **W5 (was D5)**: Path B frontend (web UI / CLI / Cowork-equivalent for Shape B) | Consulting-client signal for non-Anthropic deployment | Architecture is ready (MS AF backend in scope); only user-facing surface waits for concrete consulting client constraints. When signal arrives, ~1-2 weeks engineering per cost estimate. |

### Process commitments (not defers; recurring)

| Item | Process |
|---|---|
| Periodic substrate re-eval (was D4) | Per ARCH "Maintenance discipline" rule 6 (periodic greenfield review at major version boundaries). Substrate fit drifts over time; recurring evaluation per discipline rule. |

### Re-examination methodology

D1+D2 had ✅ completion markers and weren't really defers anymore — moved to status archive.
D3+D5 PASS external-information test (specific external signals: user request / disqualified-candidate blind spot; consulting-client signal) and PASS effort-asymmetry test (the design WORK depends on the external signal arriving with concrete constraints). Reframed as watch-list entries.
D4 is a process commitment — periodic review per ARCH discipline; not a chronological gap.

## Constraints flowing to downstream commitments

### → #9 (Department contract + entity gate Python implementation)

- Substrate Protocol (NEW pattern) lands in #9 implementation as architectural foundation
- Entity gate built against Substrate Protocol; concrete implementations: `ClaudeAgentSDKSubstrate` (full) + `MSAgentFrameworkSubstrate` (full backend)
- Bundles B/C/D/E DESIGN can proceed in parallel (substrate-agnostic per session-11 framing — confirmed: Pydantic + MCP + entity-md + audit-trail all transfer cleanly across substrates)
- Bundle A managed-entity registration shape: Substrate Protocol responsible for instantiating per-entity Pydantic from registration declarations

### → #11 (Cowork integration plugin agents)

- Plugin agent shape adopts Claude Agent SDK substrate's agent primitives
- Cowork integration deepens with Claude Agent SDK (powers Cowork natively)
- Path B frontend = NEW future ROADMAP item (deferred per D5)

### → #13 (Deployment flexibility / transport / observability)

- Substrate Protocol composes with deployment-mode flexibility
- Tier 1: stdio MCP + Claude Code (Shape A via Claude Agent SDK)
- Tier 2: HTTP MCP + Cowork plugin (Shape A via Claude Agent SDK)
- Tier 2 alternative path (consulting client with non-Anthropic stack): MS AF substrate + Path B frontend (when consulting signal arrives + frontend designed)
- Tier 3: enterprise multi-agent A2A platform — substrate determines deployment platform (Claude Agent SDK = separate Tier 3 effort; MS AF = MS AF on Azure AI Foundry / Gemini Enterprise / AWS AgentCore as instances)

### → #10 (A2A interop)

- Tier 3 reframing per pattern-vs-instance discipline (Gemini Enterprise → enterprise multi-agent A2A platform with Gemini / Azure / AWS as instances)
- A2A schema patterns from #10 stay valid; platform-specific deployment is substrate-determined

### → ROADMAP + Tier 3 section

- "Gemini Enterprise port + parallel development — Tier 3 of deployment ladder" reframes to "Tier 3 enterprise platform port — multi-archetype credibility through parallel development on a non-Anthropic enterprise platform"
- Three-tier table Tier 3 row reframes: "Enterprise multi-agent A2A platform (Gemini Enterprise / Azure AI Foundry / AWS Bedrock AgentCore)"
- NEW future-tagged ROADMAP item: **Path B frontend** (web UI / CLI for Shape B deployment) — triggered by consulting client signal for non-Anthropic deployment

### → `docs/decisions/a2a-and-gemini-pattern-emulation.md`

- Reframing note (header) added: pattern is enterprise-multi-agent-A2A-platform-agnostic; Gemini Enterprise = canonical exemplar; Azure AI Foundry + AWS AgentCore are alternatives. Schema patterns themselves don't change.

### → `docs/strategic-positioning.md`

- "Multi-archetype credibility" section sharpens: "we built our framework substrate-pluggable with TWO complete backends — Claude Agent SDK + MS AF; ship on Anthropic stack at Tier 1-2 today; deliver Tier 3 or non-Anthropic Tier 1-2 on your preferred enterprise platform when needed"

### → `ARCHITECTURE.md`

- Version log entry: substrate-pluggability discipline (Substrate Protocol pattern) NEW; Tier 3 reframing per pattern-vs-instance discipline applied to Gemini-Enterprise-instance-coupling

## Revisit triggers

- **Claude Agent SDK ships major release** affecting MCP integration / hybrid-shape / sparring hook surface — re-run screen on affected criteria; potentially substantial re-impact since this is primary substrate
- **MS AF ships major release** affecting backend implementation — re-eval middleware translation + Gap A + B composability
- **Strands deepens MCP integration / sparring hook surface** — could become viable third backend (currently DQ'd-from-current-scope by recommendation, not by criteria)
- **First consulting client demand for non-Anthropic deployment** — triggers D5 (Path B frontend) work; activates MS AF backend (which is already-built per current scope)
- **First consulting client at small-company or enterprise scale** — re-validate heaviness scaling assumptions against real deployment
- **New framework category emerges** (e.g., new lightweight or enterprise entrant meaningfully differing from current bucket representatives) — add to screen
- **VISION axis or discipline updates** affecting a criterion (new sparring mechanism added to axis 2; new validation layer added) — re-evaluate criteria coverage
- **Claude Agent SDK adds enterprise primitives** (multi-user / federated identity / formal observability) — strengthens its scale-up case; potentially reduces enterprise-tier reliance on MS AF substrate

## Files touched (session 12 — framing + screen + verification + deep-eval + recommendation)

- `docs/decisions/substrate-agentic-framework.md` — this file (NEW; status ACCEPTED — recommendation locked session 12)
- `ROADMAP.md` — Tier 3 reframing (three-tier table + "Gemini Enterprise port" section retitled + reframed); NEW future-tagged item for Path B frontend
- `docs/decisions/a2a-and-gemini-pattern-emulation.md` — reframing note added per pattern-vs-instance discipline
- `docs/strategic-positioning.md` — "Multi-archetype credibility" section sharpened with substrate-pluggability framing
- `ARCHITECTURE.md` — version log entry: substrate-pluggability discipline + Tier 3 reframing
- `HANDOFF.md` — session-12 progress note (after this session closes)
- `memory/feedback_propose_before_commit.md` — process feedback captured session 12

No code changes this session. Implementation work proceeds per #9 / #11 / #13 with Substrate Protocol as load-bearing pattern; both backends built in parallel with Claude Agent SDK as primary deployment path.
