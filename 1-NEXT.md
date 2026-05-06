# NEXT — pbs-bureau session handoff (post-2026-05-06)

> **Status**: Working handoff document for the next session. Captures session 35's outcome: lock reopened (it served its purpose); concrete deployment goals clarified; phased path forward established with intermediate-milestone discipline; engagement-detection design surfaced; enterprise-landscape research integrated; working discipline corrected.
>
> **What to do at next session start**:
> 1. Read this file in full
> 2. Read `LOCKED-STATE.md` (to be reframed early in F1; currently still in lock framing)
> 3. Read `findings-from-pbs.md` (one finding logged: M1 API friction)
> 4. Decompose F1 into intermediate milestones (illustrative draft in §6.4) and pick the FIRST milestone (F1.0) to execute
>
> **Branch state**: `step-back-evaluation` is current; `lock-and-park` branch was merged into it. F1 work continues on `step-back-evaluation` OR a new `phase-f1` branch (decide at session start).
>
> **Companion artifact**: `~/dev/Gunther-Schulz/pbs-dep-1/` — keep as historical artifact; it's the deployment attempt that surfaced the gap between architectural intent and implementation reality. Its `findings/2026-05-06-m1-api-friction.md` stays valuable. New deployment work begins as `pbs-dep-2` per F1.

---

## 1. Foundational thesis (anchored, not under revision)

From `VISION.md`:
- AI partnership that cultivates expert craft via three axes — **intertwining, sparring, authorship preservation**
- Framework is **shape-neutral** — supports practitioner-shape (PBS-Schulz pioneer), autonomous-business-shape, personal-OS-shape, others
- Pioneer instance: PBS-Schulz planning office; Gunther is the test-deployment practitioner

These remain anchored. Nothing in session 35 challenges them.

## 2. Concrete deployment goals (clarified across session 35)

1. **Config 3 = machine-enforced framework runtime**: audit-trail integrity, authority-binding enforcement, sparring validation, quality-gate decisions — programmatically, not just prompt-instructed.

2. **Mode A + Mode B both accessible**:
   - Mode A = interactive chat (Claude Code CLI / Claude Desktop / Claude Cowork)
   - Mode B = SDK orchestrator for autonomous/scheduled/batch work

3. **Three-tier deployment progression**:
   - Tier 1: PBS-Schulz on Gunther's machine (daily use)
   - Tier 2: hosted small-firm deployments (Docker / cloud-app template)
   - Tier 3: dual-track — (a) SaaS for non-coder Cowork users; (b) enterprise integration as governance plug-in for Gemini Enterprise / MS Foundry / similar platforms

4. **Two substrate paths preserved**: Claude Agent SDK (primary; Anthropic-native ergonomics) + MS Agent Framework (secondary; Microsoft ecosystem path).

5. **Schedulers as part of deployment infrastructure**: cron-style for Tier 1, in-container for Tier 2 Docker, vendor-side for Tier 3 SaaS — running SDK orchestrator scripts. SDK has no native scheduling.

## 3. Architectural reality mapping

### What survives intact (verified strong in session 35 reads)

- **VISION** — three axes, shape-neutrality, pioneer-instance framing. Anchored.
- **Glossary vocabulary** — workspace, practitioner, specialist, skill, claim, work-unit, audit, sparring, gate, authority-binding, adapter, substrate. Architecturally sound.
- **Mechanism Surfaces** (Pattern A/B/C/D protocol contracts) — audit, sparring, quality-gate, authority-binding, adapter, substrate. Reusable across all tiers + both substrate impls + both modes.
- **Manifest schemas** (workspace.py, practitioner.py, specialist.py, workflow.py, work_unit.py, claim.py) — Pydantic schemas describe deployment data shapes; reusable across packaging.
- **Three-tier semantics** — Tier 1/2/3 enum already in substrate (`pbs/substrate.py:78-80`); `arch/substrate.md` describes per-tier behavior expectations.
- **Transport modes** — IN_PROCESS / SUBPROCESS / HTTP defined in substrate Pattern A. Supports Mode A (Claude Code → SUBPROCESS MCP) + hosted (HTTP MCP for Tier 3) from day one architecturally.
- **Specialist + skill primitive cluster** — bipartite Pattern B with namespace mechanic; works for the "deployment ships specialists" model.
- **Adapter Pattern A with MCP-Server + A2A-Peer per-class Surfaces** — directly aligns with the open-standards reality: MCP for tool/data integration; A2A for agent-to-agent. Both are universal cross-vendor standards in 2026.
- **Existing Claude Code dev plugin** (`plugin/.claude-plugin/plugin.json`) — proves plugin format works; framework's plugin.json explicitly forecast "Phase 3+ app-skill packaging surface."

### What has gaps (load-bearing for the goals)

- **SUBPROCESS + HTTP transport implementation** — currently only IN_PROCESS implemented. Both Mode A interactive and Tier 2/3 hosted require these. Architecturally supported, implementationally NOT built.
- **PBS framework runtime as MCP server(s)** — mechanism Surfaces (audit, sparring, gate, authority, workspace state) need MCP-tool exposure so external interactive clients (Claude Code / Cowork) can invoke them. Not built.
- **Framework-level Claude Code plugin content** — hooks (authority/audit/gate enforcement), cross-cutting agents (sparring-partner), framework slash commands (`/pbs-status`, `/pbs-attest`, etc.), framework-level skills (sparring discipline, claim-attestation). Documented in concept; not authored.
- **Specialist plugins for actual planning work** — planning-document-work, project-management, invoicing specialists not built. Per `LOCKED-STATE.md` TOP-LEVEL SCOPE these belong in deployment-instance repo (`pbs-dep-2` etc.), not framework.
- **Tier-aware packaging** — no DR locks how PBS distributes per tier. Recommendations (pip+daemon for Tier 1, Docker for Tier 2, SaaS or enterprise plug-in for Tier 3) unspecified architecturally.
- **Scheduler integration** — SDK has no native scheduling; framework has no architectural commitment about how scheduled tasks compose with framework runtime.
- **Engagement detection** — no architectural commitment about how PBS engagement gets detected per prompt; design proposed in §5.
- **Enterprise platform integration interfaces** — Microsoft Agent Governance Toolkit's PolicyProviderInterface (and Gemini Enterprise's equivalent) are the right enterprise-tier integration shape. Not on framework's roadmap yet.

### What needs reframing (load-bearing surfaced session 35)

Of the 9 questionable points in `LOCKED-STATE.md`, session 35 validated only TWO as load-bearing:

- **#10 (NEW) — Substrate Pattern A model needs clarification**: assumes "framework owns the agent loop." Reality: Mode A means Claude Code owns the loop; Mode B means SDK orchestrator drives it. Pattern A primitive may need clarifying that Mode A bypasses substrate as agent-loop-owner and treats it as framework-services-provider via MCP. NOT a tear-down; a clarification.
- **#8 — `practitioner_shape_*.py` impls placement**: these encode policy values that PBS-Schulz happens to want. They belong as deployment content (in `pbs-dep-2` or equivalent), not in framework. Refactor needed.

The other 7 questionable points (multi-shape composability, engagement-target conflation, hybrid-shape mechanics, etc.) — session 35 surfaced no evidence they're real blockers. They might be theoretical concerns PBS-as-pioneer doesn't actually hit. Defer to first-deployment-evidence-driven amendments rather than treat as blockers.

## 4. Why the lock breaks now (and what dep-1 taught us)

The lock served its purpose by forcing a deployment attempt (pbs-dep-1). The attempt revealed:

- The architecture's INTENT supports the goals (transport modes, tier semantics, both substrates, plugin-shaped distribution, MCP-server-backed runtime).
- The IMPLEMENTATION chose the wrong order: built IN_PROCESS substrate-as-orchestrator first; should have built SUBPROCESS MCP server transport first to enable Claude Code connection.
- Some "questionable points" are theoretical; some are blockers. The ones that matter to the goals are #8 (practitioner_shape policy placement) + #10 (substrate model clarification for Mode A).

So reopening the lock isn't "we got it wrong, restart." It's "implementation order needs correcting based on validated deployment intent." Most architectural reasoning preserves; specific Phase 6 implementation work refactors.

**The deeper lesson — load-bearing for §6 working discipline**: dep-1 wasn't deployable for real work, but it surfaced transport gaps + practitioner_shape placement question + substrate model clarification need + Mode A vs Mode B distinction + engagement detection gap. None visible from architectural reasoning alone. Intermediate deployments — even ones not ready to do real work — are the validation mechanism. Architecture-only reasoning is insufficient; deployment evidence is required.

## 5. Engagement detection design

**The question**: in daily Claude Code use, how is it decided what gets routed through PBS framework enforcement vs flows as plain Claude work? How does the user get the "supportive not constraining" experience?

**Verified architectural answer**: PBS enforcement is **event-anchored, not session-blanket**. Skills auto-trigger via `when_to_use` matching; quality-gate fires at specific checkpoints (`pre_send` / `pre_claim_finalization` / `pre_decision_lock` / `per_edit` / `workflow_phase_transition` / `session_end` / `drift_audit`); sparring fires per-claim; authority-binding gates only catalog event_kinds.

So the framework already supports selective engagement architecturally. Deployment-side discipline determines how SELECTIVE the engagement is.

### Three engagement paths — combine, don't choose

1. **Implicit (skill triggers)** — primary path. Skills declared with narrow honest `when_to_use`. PBS engages naturally when work matches. Best for axis-1 intertwined feel.
2. **Conventional (`pbs:` prompt prefix)** — UserPromptSubmit hook checks for prefix; if present, sets engagement-flag. Best for "I want PBS rigor on this freeform task" without specific command.
3. **Explicit (`/pbs-<command>` slash commands)** — guaranteed-fire deterministic invocation. Claude Code lists discoverable commands. Best for specific workflows + as RESCUE for skill-trigger fragility (known issue in agent runtimes generally).

A normal day uses all three. Most engagement implicit (natural co-work flow); `pbs:` prefix when user wants discipline applied to something the trigger missed; slash commands for ceremonies (`/pbs-attest`, `/pbs-spar`, `/pbs-audit-query`).

### Hook scoping pattern

Framework hooks scoped to fire ONLY in PBS-engaged context:

```
UserPromptSubmit hook:
  if prompt starts with "/pbs-" or "pbs:":
    set context flag "pbs-engaged: true"
  elif any active skill matched the prompt:
    set context flag "pbs-engaged: true"
  else:
    set context flag "pbs-engaged: false"

PreToolUse / PostToolUse hooks:
  if pbs-engaged:
    do PBS enforcement (audit / authority / gate)
  else:
    skip — plain Claude work, zero overhead
```

Framework enforcement happens only when PBS is actually engaged. No background overhead on plain Claude work. Addresses "supports but doesn't feel constrained" goal directly.

**Why this strengthens defensibility (axis 3)**: if skill triggers are flaky, "did sparring actually fire on this claim?" becomes uncertain. Adding explicit invocation as fallback gives users a way to GUARANTEE engagement when defensibility matters most. Strengthens defensibility-grade properties.

**Implementation status**: UserPromptSubmit hook with `prompt: str` field exists in Claude Agent SDK (verified `types.py:295-299`); HookMatcher mechanism exists; slash commands work via plugin format. Context-flag-passing between hooks may need workaround (external state file / MCP server side state / environment variable) — resolve in F1.

## 6. Working discipline (the corrective from session 35)

Session 35 broke under cognitive load. Diagnosis: load came from cross-module composition questions held simultaneously, not from missing module boundaries. The framework already IS modular (mechanism Surfaces, Pattern A/B/C/D taxonomy, per-class Surfaces, sub-mechanisms, manifest schemas). The corrective is in HOW we work, not in MORE modularity.

Four discipline elements apply across F1+. They compose; none is optional.

### 6.1 Deployment-slice work organization

Work is organized by deployment milestone, NOT by architectural module. Each session focuses on a vertical slice of what's needed for the current milestone — substrate AND audit AND adapter pieces if they're all needed to advance the milestone, but ONLY the pieces needed.

Modules NOT relevant to current milestone don't load into working memory — they're not in the work, by construction.

### 6.2 One-contract-at-a-time

For every architectural commitment surfaced during F1+ work, produce ONE explicit contract clarification before locking it. Format:

- One sentence in plain language: "X promises Y to consumer Z."
- Test against ≥3 concrete PBS-Schulz scenarios. Survives all 3 → lockable. Fails any 1 → revise the contract before locking.
- Hold ONE contract in working memory at a time. Never juggle.

For F1 specifically: produce contract clarifications for authority-binding (promise to skill authors), audit (promise to defensibility test), quality-gate (promise to engagement-detection), sparring (promise to claim-makers), substrate (promise to specialist authors). Five contracts, one at a time, each tested against PBS scenarios.

If writing a contract clarification surfaces that the current architectural shape doesn't permit a clean one-sentence promise, that's evidence the shape needs revision. Surface to user; don't paper over with hedged contract.

### 6.3 Cognitive entry path

Add `READ-ME-FIRST.md` at framework root early in F1. NOT a list of files; concern-driven paths.

Format:

> If you're working on [concern type X]:
> 1. Read [doc A] (skim — hold the 2-3 anchors)
> 2. Read [doc B] (the specific arch topic)
> 3. Read [doc C] only if implementing
>
> You don't need to hold [other docs D, E, F] for this concern.

Cover concerns: starting a new architectural decision; implementing a mechanism Surface impl; authoring a deployment-side specialist; investigating a cross-module composition question.

The current session-start procedure (read 7 anchor files in flat list) is a flat-list, not a path. Replace with concern-driven entry paths so working memory holds 2-3 docs maximum at any moment.

### 6.4 Intermediate-deployment milestone discipline

Dep-1 evidence: intermediate deployments — even ones not ready to do real work — surface mismatches between architectural intent and implementation reality that abstract reasoning cannot. Intermediate deployment IS the validation mechanism, not a celebration at phase end.

Each phase decomposes into intermediate deployable points where the partial-deployment IS the assumption-test.

**Milestone criteria** (what makes a deployable intermediate point):

1. **Concrete enough to deploy** — actual artifacts produced (not just designs); something runnable / connectable / observable
2. **Bounded enough to deploy now** — narrow scope that can land in one session OR a small cluster of sessions; not multi-week
3. **Surfaces specific assumption** — explicit hypothesis about what the deployment will validate or reveal: "deploying this will tell us whether X assumption holds"
4. **Findings expected** — assume the deployment WILL surface mismatches; findings/ entry expected per intermediate milestone, not exception

**Per-phase decomposition**: at start of each phase, decompose into intermediate milestones with explicit assumption-tests. Don't lock the milestone list rigidly — adjust as evidence accumulates — but always have a NEXT milestone with named hypothesis.

**Anti-pattern**: treating phase completion as the deployment moment. Wrong. Each intermediate is its own deployment + its own findings cycle.

### 6.5 Session behavior derived from 6.1-6.4

Concrete behavioral rules per session:

- **Per-session scope**: pick ONE milestone (or one sub-step of an intermediate milestone). Don't carry over scope from prior sessions; never combine milestones in a single session unless they're truly atomic.
- **Per-claim discipline**: every architectural claim made during F1+ work is either (a) cited from a doc read in current session, (b) read now before stating, or (c) flagged as inferred. No pattern-matching from session memory.
- **Per-contract gate**: lock nothing without producing the §6.2 contract clarification first. If contract can't be written in one sentence, the contract isn't clear enough to lock.
- **Per-cognitive-load check**: at any session moment where ≥3 architectural modules are in working memory simultaneously, STOP. Surface to user. Decide: defer one module, or split the session.
- **Per-deployment expectation**: every milestone produces at least one finding entry — even if it's "expectation matched, no friction." Keeps the findings/ habit live.

## 7. Path forward — four phases with intermediate milestones

### Phase F1 — Foundation correction (weeks)

**Goal**: framework runtime in a state where Claude Code CLI can connect to it and use PBS services. Tier 1 on Gunther's machine.

**Phase F1 verifies**: Mode A on Tier 1 with Config 3 enforcement actually works for one practitioner.

**Intermediate milestones (illustrative; refine + lock at F1 start per §6.4)**:

- **F1.0 — SUBPROCESS MCP boots cleanly**: standalone subprocess MCP server starts, exposes empty tool list, accepts connection from Claude Code. Tests: does the framework's substrate Pattern A SUBPROCESS transport actually compose with Claude Code's MCP client? Findings expected: transport-level surprises, packaging issues.

- **F1.1 — One framework MCP tool callable**: ONE concrete tool exposed (e.g., `pbs_audit_emit`); Claude Code can invoke it; audit-trail records the invocation. Tests: does the framework's audit Surface compose cleanly with MCP tool-call semantics? Contract clarification per §6.2 produced for audit Surface here.

- **F1.2 — Engagement-detection hook fires**: PreToolUse hook activates only when engagement-detection flag set; gates on authority-binding catalog. Tests: does the engagement-detection pattern (UserPromptSubmit → flag → downstream hooks) work in Claude Code's hook system? Resolves the context-flag-passing question from §5. Contract clarification per §6.2 produced for authority-binding Surface here.

- **F1.3 — Practitioner-shape policy bundle externalized**: refactor `practitioner_shape_*.py` values out of `pbs/impls/`; wire dep-2 to provide them. Tests: does the framework cleanly accept per-deployment policy values, OR does the refactor surface tighter coupling than expected? Resolves LOCKED-STATE questionable point #8.

- **F1.4 — Hello PBS v2 (full F1 wiring)**: end-to-end interactive flow in Claude Code through PBS framework MCP servers + practitioner-shape policy bundle from dep-2 + framework-level plugin content (hooks + sparring-partner agent + framework slash commands + framework-level skills). Tests: does the full F1 stack produce the promised "supportive not constraining" experience? Contract clarifications per §6.2 produced for sparring + quality-gate + substrate Surfaces here. Resolves LOCKED-STATE questionable point #10.

Each F1.k is its own deployment to dep-2. Findings expected at each. dep-2 grows with each milestone.

### Phase F2 — Specialist content + first real work (months)

**Goal**: PBS-Schulz produces real planning work daily.

**Phase F2 verifies**: PBS does its actual work via the framework with engagement experience matching the goal of "supportive not constraining."

**Intermediate milestones (decompose at F2 start per §6.4)** — illustrative shape:

- F2.0: One specialist (probably planning-document-work) with one minimal workflow; deployable in dep-2. Tests: does specialist + framework + Claude Code compose for actual domain work?
- F2.1: First real B-Plan-Begründung section drafted via PBS; first real attestation; first real claim-defensibility audit-trail entry.
- F2.2: Second + third specialists (project-management, invoicing) added; cross-specialist composition tested.
- F2.3: Layer A content for one real domain + one real state added; corpus retrieval tested via MCP-corpus adapter.
- F2.4: Daily-use threshold — PBS replaces whatever Gunther currently uses for the work this milestone covers.

**Engagement boundary discipline applied at every specialist** (per §5+§6): narrow honest `when_to_use` triggers, companion slash commands for explicit invocation, workflow phase declarations explicit.

### Phase F3 — Tier 2 packaging + Mode B scheduler (months)

**Goal**: PBS runnable as Docker image (Tier 2) + scheduled work via Mode B SDK orchestrator scripts.

**Phase F3 verifies**: Tier 2 works; Mode B + scheduler compose with the same framework runtime.

**Intermediate milestones (decompose at F3 start per §6.4)** — illustrative shape:

- F3.0: Docker image bundling framework runtime + MCP servers boots cleanly in a container.
- F3.1: SDK orchestrator script template (Hello PBS evolved); runs once successfully driving Claude through the PBS-loaded plugin.
- F3.2: First scheduled task: monthly invoicing OR similar; runs autonomously; audit-trail captures everything.
- F3.3: Container deployment tested on a small VPS; persistence + scheduler + MCP servers all survive container restart.

### Phase F4 — Tier 3 dual-track (much longer; only when audience demands)

**Goal**: hosted multi-tenant PBS for non-coder users (Track A: SaaS) AND/OR enterprise integration as governance plug-in (Track B: enterprise platform integration).

**Track A — SaaS for Cowork users**: hosted multi-tenant PBS; user signs up; gets workspace provisioned; connects Cowork via OAuth. Vendor operates infrastructure (hosting, billing, GDPR, multi-tenancy, security, uptime). This is a SaaS business, not just packaging.

**Track B — Enterprise integration**: PBS framework's existing A2A-Peer adapter class + MCP transport + Pattern A substrate plurality is the right architectural position for the heterogeneous A2A-interop enterprise reality (verified: A2A is Google-originated open standard with universal adoption — Microsoft Agent Framework, Google ADK, LangGraph, CrewAI, LlamaIndex, Semantic Kernel, AutoGen). Microsoft Agent Governance Toolkit's PolicyProviderInterface (and equivalent extension points in other platforms) explicitly support framework-agnostic governance plug-ins. PBS could plug in as the practitioner-accountability layer ON TOP of platform-level governance.

The opportunity: practitioner-accountability + defensibility for expert-practitioner verticals is a specific gap the giant platforms address generically, not professionally. PBS could fill it. Doesn't require betting on Google OR Microsoft — works in environments using either or both via open standards (MCP universal; A2A universal).

**Defer F4 entirely** until: (a) Tier 1 + Tier 2 are solid; (b) actual audience demand exists; (c) Gunther has appetite for SaaS operations OR concrete enterprise inquiry surfaces.

### Throughout: MS Agent Framework path stays viable

Phases F1-F3 stay substrate-impl-agnostic at framework runtime + MCP server layer. MS AF substrate impl can land later (Phase F2 or F3) without disturbing the rest. Pattern A's ≥2-impl discriminator stays satisfied.

## 8. Enterprise landscape context (for F4 planning when activated)

Verified state of the agentic deployment landscape, 2025-2026:

- **MCP** (Model Context Protocol): donated to Linux Foundation December 2025; universal cross-vendor adoption (Anthropic, Microsoft, Google, OpenAI). THE standard at the tool/data integration layer. Got stronger in 2026, not weaker. PBS commits to MCP as primary integration protocol — well-positioned.

- **A2A** (Agent-to-Agent): Google-originated; native support across Google ADK + Microsoft Semantic Kernel/AutoGen + LangGraph + CrewAI + LlamaIndex + Microsoft Agent Framework; 150+ orgs production. Cross-vendor interop verified. PBS adapter Pattern A's A2A-Peer class commits to A2A — aligned with the standard.

- **Microsoft Agent Framework + Foundry + Agent Governance Toolkit**: framework-agnostic governance via PolicyProviderInterface; framework deploys to containers / on-premises / multi-cloud; full enterprise governance via Azure AI Foundry hosting. Open standards: MCP, A2A, OpenAPI, pluggable memory.

- **Google Gemini Enterprise Agent Platform** (April 2026, evolution of Vertex AI): Agent Identity (cryptographic IDs + audit), Agent Registry, Agent Gateway, Agent Anomaly Detection, Agent Sandbox. MCP supported. Multi-model (Anthropic Claude + Gemma + others).

- **Regulatory pressure**: EU AI Act enforced 2025; high-risk AI systems require detailed activity logs preserved for regulatory review; up to 3% global annual turnover penalty. Practitioner-accountability + defensibility-grade audit-trail (PBS axis-3) is regulatory-aligned.

- **Market governance maturity**: 80% of enterprises deploying agents lack mature governance; only 21% have it. Platform vendors (MS + Google) filling this generically; PBS could fill domain-specific (practitioner-shape) niche.

This context informs F4 positioning but does not affect F1-F3 work. Don't divert F1-F3 to chase enterprise integration. Capture as forward-reference for F4 activation.

## 9. LOCKED-STATE.md reframing (early F1 task)

Reframe at start of F1. Not delete; not "we were wrong."

- **Status**: `Locked` → `Active development (per 1-NEXT.md)`
- **Move questionable points #8 + #10** from "parked" to "F1 leverage points" (active work)
- **Move questionable points #1-#7 + #9** from "parked" to "deferred — will surface during F2 if real" (still parked, but reframed as "wait for evidence" not "wait for reopening trigger")
- **Replace reopen criteria** with milestone-completion checkpoints (F1.0 / F1.1 / F1.2 / F1.3 / F1.4 close + F1 close + F2.x close + F3.x close)

Lock-and-park's PURPOSE — preventing premature speculative refactoring without ground truth — was right. Session 35's conversation IS the ground truth that justifies unparking specific things while continuing to defer others.

## 10. Honest framing on what session 35 changed

Session 35's failure mode (AI pattern-matching, user absorbing cognitive load) was real. It cost hours and produced fake roadblocks. But it ALSO produced:

- Clear articulation of Config 3 + Mode A + Mode B
- Tier 1/2/3 deployment shape clarity
- Recognition that SUBPROCESS MCP transport is the actual blocker for deployment goals
- Recognition that practitioner_shape policy values belong as deployment content
- Validation that VISION + most architectural reasoning + mechanism Surfaces survive intact
- Engagement detection design (combining 3 paths; hook scoping pattern)
- Enterprise landscape research integrated (open-standards layer cake; PBS positioned for it)
- Working discipline corrective (deployment-slice + one-contract + cognitive-entry-path + intermediate-milestone)

Net: session 35 wasn't wasted. The cost was high; the clarification was real. The path forward is concrete and grounded.

**Discipline change for forward sessions** (codified in §6): Cite-or-Read-or-Flag for every architectural claim BEFORE stating it; one-contract-at-a-time discipline; deployment-slice scope per session; cognitive entry path docs; intermediate-milestone deployments as validation mechanism.

## 11. Honest basis caveats

- **Verified directly** (read in session 35): VISION axes; glossary entries for shape/practitioner/workspace/framework-c-scope/owner-b-scope; MAINTENANCE.md TOP-LEVEL ARCHITECTURE + DESIGN PRINCIPLES + MILESTONE STRUCTURE + SCOPE; arch/scope-model.md; arch/specialist-skill.md sections 8-12; arch/practitioner.md sections 1-5; arch/adapter.md sections 1-3; pbs/manifests/workspace.py + specialist.py; SDK types.py + README + plugin example; SDK has no native scheduling (verified by grep); Cowork plugin model (verified via web search); UserPromptSubmit hook + prompt field; HookMatcher mechanism; A2A is Google-originated open standard (verified via web search); MCP donated to Linux Foundation (verified via web search); Microsoft Agent Governance Toolkit framework-agnostic via PolicyProviderInterface (verified via web search).

- **Inferred but high-confidence**: F1-F4 sequencing (based on dependency analysis); engagement-flag pattern (composes from verified hook primitives but not a documented PBS pattern); three-tier packaging recommendations (standard infrastructure practice); intermediate-milestone discipline as the right corrective for session 35's failure mode (extracted from dep-1 outcome).

- **Inferred and uncertain**: that one-session-per-intermediate-milestone is achievable (could be too aggressive or too conservative; calibrate during F1); that the F1.0-F1.4 illustrative decomposition is right (these are MY guess at sensible intermediate points; needs reaction at F1 start; could be wrong about which boundaries matter most); that practitioner-accountability is genuinely a gap platforms don't address (based on reading their feature lists; didn't exhaustively search).

- **Not verified**: actual time/effort for each phase (weeks/months are inferred from scope; could be substantially off); that practitioner_shape_*.py refactor is feasible without breaking other framework code (haven't traced all dependencies); how mid-session specialist deactivation works; that hook context-flag passing has a clean primitive in Claude Code (may need workaround); whether Cowork has scheduling capability (matters for Track A SaaS design, not for Tier 1+2); that PolicyProviderInterface specifically would accept PBS's mechanism Surface shape (would need to read interface spec for Track B).

## 12. Net

Goals are realizable with the framework's current architectural commitments. The locked architecture wasn't wrong; the implementation order was. F1 is the focused correction work that unblocks Mode A on Tier 1 — Gunther's daily PBS use. F2 builds the specialist content for real PBS work + engagement boundary discipline. F3 packages for Tier 2 + Mode B scheduler. F4 dual-track (SaaS + enterprise integration) waits for evidence.

Locked architectural reasoning preserves; specific premature implementation choices get corrected. MS Agent Framework path stays open throughout. Engagement detection design (3 paths combined; hooks scoped to engagement context) directly addresses the "supportive not constraining" experience goal. Enterprise landscape is favorable (open standards converge; PBS positioned for both standalone and platform-integration).

Move into F1 when ready, per §6 working discipline (deployment-slice scope per session + one-contract-at-a-time + cognitive entry path + intermediate-milestone deployments) — not the previous open-ended cluster-execution methodology.

---

## Pickup checklist for next session

- [ ] Read this file in full
- [ ] Read `LOCKED-STATE.md` (will be reframed early in F1 per §9)
- [ ] Read `findings-from-pbs.md` (currently 1 finding logged)
- [ ] Decide branch strategy: continue on `step-back-evaluation` OR new `phase-f1` branch
- [ ] **Author `READ-ME-FIRST.md` (cognitive entry paths) early in F1 per §6.3** — even before its first use, just to enable it
- [ ] **Decompose F1 into intermediate milestones with named assumption-tests per §6.4** — react to illustrative F1.0-F1.4 in §7 or revise
- [ ] **Pick the FIRST milestone (F1.0) to execute** — one milestone per session
- [ ] **Apply session behavior rules from §6.5**: per-session scope discipline; Cite-or-Read-or-Flag on every claim; per-contract gate before locking; per-cognitive-load check (halt if ≥3 modules in working memory); per-deployment expectation (findings entry per milestone)

Sleep well between sessions. Pick up here.
