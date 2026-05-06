# NEXT — pbs-bureau session handoff (post-2026-05-06)

> **Status**: Working handoff document for the next session. Captures session 35's outcome: lock-and-park reopened (lock served its purpose); concrete deployment goals clarified; phased path forward established; engagement-detection design surfaced.
>
> **What to do at next session start**:
> 1. Read this file in full
> 2. Read `LOCKED-STATE.md` (will be reframed during F1; currently still in lock framing)
> 3. Read `findings-from-pbs.md` (one finding logged: M1 API friction)
> 4. Begin Phase F1 work per "Path forward" section below
>
> **Branch state**: `step-back-evaluation` is current; `lock-and-park` branch was merged into it. F1 work continues on `step-back-evaluation` OR a new `phase-f1` branch (decide at session start).
>
> **Companion artifact**: `~/dev/Gunther-Schulz/pbs-dep-1/` — keep as historical artifact; it's the deployment attempt that surfaced the gap between architectural intent and implementation reality. Its `findings/2026-05-06-m1-api-friction.md` stays valuable. New deployment work begins as `pbs-dep-2` per F1 step 5.

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
   - Tier 3 / SaaS: non-coder Cowork users (vendor-operated multi-tenant) — long-term

4. **Two substrate paths preserved**: Claude Agent SDK (primary; Anthropic-native ergonomics) + MS Agent Framework (secondary; Microsoft ecosystem path).

5. **Schedulers as part of deployment infrastructure**: cron-style for Tier 1, in-container for Tier 2 Docker, vendor-side for Tier 3 SaaS — running SDK orchestrator scripts. SDK has no native scheduling.

## 3. How these map to current architectural reality

### What survives intact (verified strong)

- **VISION** — three axes, shape-neutrality, pioneer-instance framing. Anchored.
- **Glossary vocabulary** — workspace, practitioner, specialist, skill, claim, work-unit, audit, sparring, gate, authority-binding, adapter, substrate. Architecturally sound.
- **Mechanism Surfaces** (Pattern A/B/C/D protocol contracts) — audit, sparring, quality-gate, authority-binding, adapter, substrate. Reusable across all tiers + both substrate impls + both modes.
- **Manifest schemas** (workspace.py, practitioner.py, specialist.py, workflow.py, work_unit.py, claim.py) — Pydantic schemas describe the deployment data shapes; reusable across packaging.
- **Three-tier semantics** — Tier 1/2/3 enum already in substrate (`pbs/substrate.py:78-80`); `arch/substrate.md` describes per-tier behavior expectations.
- **Transport modes** — IN_PROCESS / SUBPROCESS / HTTP defined in substrate Pattern A; supports Mode A (Claude Code → SUBPROCESS MCP) + hosted (HTTP MCP for Cowork-shipped SaaS) from day one architecturally.
- **Specialist + skill primitive cluster** — bipartite Pattern B with namespace mechanic; works for the "deployment ships specialists" model.
- **Existing Claude Code dev plugin** — proves plugin format works.

### What has gaps (load-bearing for the goals)

- **SUBPROCESS + HTTP transport implementation** — currently only IN_PROCESS implemented. Both Mode A interactive and Tier 2/3 hosted require these. Architecturally supported, implementationally NOT built.
- **PBS framework runtime as MCP server(s)** — mechanism Surfaces (audit, sparring, gate, authority, workspace state) need MCP-tool exposure so external interactive clients (Claude Code / Cowork) can invoke them. Not built.
- **Framework-level plugin content** — hooks (authority/audit/gate enforcement), cross-cutting agents (sparring-partner), framework slash commands (`/pbs-status`, `/pbs-attest`, etc.), framework-level skills (sparring discipline, claim-attestation). Documented in concept; not authored as Claude Code plugin content.
- **Specialist plugins for actual planning work** — planning-document-work, project-management, invoicing specialists not built. Per `LOCKED-STATE.md` TOP-LEVEL SCOPE these belong in deployment-instance repo (pbs-dep-2 etc.), not framework.
- **Tier-aware packaging** — no DR locks how PBS distributes per tier. Recommendations (pip+daemon for Tier 1, Docker for Tier 2, SaaS for Tier 3) are unspecified architecturally.
- **Scheduler integration** — SDK has no native scheduling; framework has no architectural commitment about how scheduled tasks compose with framework runtime. Recommendation (external scheduler launches SDK orchestrator scripts) is sound but unspecified.
- **Engagement detection** (NEW from session 35) — no architectural commitment about how PBS engagement gets detected per prompt; needs explicit design (see §6).

### What needs reframing

Of the 9 questionable points in `LOCKED-STATE.md`, session 35 validated only TWO as load-bearing:

- **#10 (NEW) — Substrate Pattern A model needs clarification**: assumes "framework owns the agent loop." Reality: Mode A means Claude Code owns the loop; Mode B means SDK orchestrator drives it. Pattern A primitive may need clarifying that Mode A bypasses substrate as agent-loop-owner and treats it as framework-services-provider via MCP. NOT a tear-down; a clarification.
- **#8 — `practitioner_shape_*.py` impls placement**: these encode policy values that PBS-Schulz happens to want. Per `LOCKED-STATE.md` reading they belong as deployment content (in `pbs-dep-2` or equivalent), not in framework. Refactor needed.

The other 7 questionable points (multi-shape composability, engagement-target conflation, hybrid-shape mechanics, etc.) — session 35 surfaced no evidence they're real blockers. They might be theoretical concerns PBS-as-pioneer doesn't actually hit. Defer to first-deployment-evidence-driven amendments rather than treat as blockers.

## 4. What "breaking the lock" means concretely

The lock served its purpose by forcing a deployment attempt (pbs-dep-1). The attempt revealed:
- The architecture's INTENT supports the goals (transport modes, tier semantics, both substrates, plugin-shaped distribution, MCP-server-backed runtime)
- The IMPLEMENTATION chose the wrong order: built IN_PROCESS substrate-as-orchestrator first; should have built SUBPROCESS MCP server transport first to enable Claude Code connection
- Some "questionable points" are theoretical; some are blockers. The ones that matter to the goals are #8 (practitioner_shape policy placement) + #10 (substrate model clarification for Mode A)

So reopening the lock isn't "we got it wrong, restart." It's "implementation order needs correcting based on validated deployment intent." Most architectural reasoning preserves; specific Phase 6 implementation work refactors.

## 5. Path forward — proposed in four phases

### Phase F1 — Foundation correction (weeks)

**Goal**: framework runtime in a state where Claude Code CLI can connect to it and use PBS services. Tier 1 on Gunther's machine.

Concrete steps:
1. **Implement SUBPROCESS MCP server transport** for the framework runtime (currently only IN_PROCESS). Unblocks Mode A.
2. **Decompose framework runtime into MCP servers** — choose between single-server-multi-tools vs server-per-Surface (audit / sparring / gate / authority / workspace-state). Recommend server-per-Surface per architectural Surface decomposition. Each ships a standalone MCP server callable via SUBPROCESS.
3. **Author framework-level Claude Code plugin content** — hooks (PreToolUse calling authority MCP; PostToolUse calling audit MCP; UserPromptSubmit driving engagement-detection per §6), cross-cutting sparring-partner agent, framework slash commands (`/pbs-status`, `/pbs-attest`, `/pbs-audit-query`, `/pbs-spar`), framework-level skills (sparring discipline, claim-attestation, defensibility-test).
4. **Refactor `practitioner_shape_*.py` policy values out of `pbs/impls/`** — move to deployment-side policy bundle. Framework keeps mechanism class shells (SparringProtocol, QualityGateProtocol, AuthorityBindingProtocol); deployment supplies per-shape values.
5. **Wire pbs-dep-2 to use Phase F1 framework** — workspace.md + practitioner-shape policy bundle + simple specialist + Claude Code config that loads PBS plugin + connects to PBS MCP servers. End state: open Claude Code, PBS available, basic work via the framework runs.

**Verifies**: Mode A on Tier 1 with Config 3 enforcement actually works for one practitioner.

### Phase F2 — Specialist content + first real work (months)

**Goal**: PBS-Schulz produces real planning work daily.

Concrete steps:
1. Author planning-document-work specialist as Claude Code plugin (separate from framework, or bundled — design choice).
2. Author project-management + invoicing specialists.
3. Author Layer A content (DACH-EU + Bauleitplanung + B-Plan-Begründung references; bausteine).
4. Wire MCP-corpus adapter (corpus backend choice — could be local LanceDB stub from Phase 6.2 architectural intent, or simpler initially).
5. Use it daily. Capture findings continuously in pbs-dep-2's `findings/` directory. Some deferred "questionable points" may surface as real; some won't.
6. **Engagement boundary discipline applied at every specialist** (per §6) — narrow honest `when_to_use` triggers, companion slash commands for explicit invocation, workflow phase declarations explicit.

**Verifies**: PBS does its actual work via the framework with the engagement experience matching the goal of "supportive not constraining."

### Phase F3 — Tier 2 packaging + Mode B scheduler (months)

**Goal**: PBS runnable as Docker image (Tier 2) + scheduled work via Mode B SDK orchestrator scripts.

Concrete steps:
1. Docker image bundling framework runtime + MCP servers + scheduler (cron or systemd timer in container).
2. SDK orchestrator script template (Hello PBS evolved into useful pattern).
3. First scheduled task: monthly invoicing for PBS-Schulz (or similar).
4. Test container deployment on a small VPS.

**Verifies**: Tier 2 works; Mode B + scheduler compose with the same framework runtime.

### Phase F4 — Tier 3 SaaS (much longer; only if/when audience demands)

**Goal**: hosted multi-tenant PBS for non-coder Cowork users.

This is a SaaS business, not just packaging. Defer until: (a) Tier 1 + Tier 2 are solid; (b) actual audience demand exists; (c) Gunther has appetite for SaaS operations. Not a near-term concern.

### Throughout: MS Agent Framework path stays viable

Phases F1-F3 stay substrate-impl-agnostic at framework runtime + MCP server layer. MS AF substrate impl can land later (Phase F2 or F3) without disturbing the rest. Pattern A's ≥2-impl discriminator stays satisfied.

## 6. Engagement detection design (NEW — session 35)

**The question**: in daily Claude Code use, how is it decided what gets routed through PBS framework enforcement vs flows as plain Claude work? How do users get "supportive not constraining" experience?

**Verified architectural answer**: PBS enforcement is **event-anchored, not session-blanket**. Skills auto-trigger via `when_to_use` matching; quality-gate fires at specific checkpoints (`pre_send` / `pre_claim_finalization` / `pre_decision_lock` / `per_edit` / `workflow_phase_transition` / `session_end` / `drift_audit`); sparring fires per-claim; authority-binding gates only catalog event_kinds.

So the framework already supports selective engagement architecturally. The deployment-side discipline determines how SELECTIVE the engagement is.

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

Result: framework enforcement happens only when PBS is actually engaged. No background overhead on plain Claude work. Addresses "supports but doesn't feel constrained" goal directly.

### Implementation status

**Verified architecturally supported**: UserPromptSubmit hook with `prompt: str` field exists in Claude Agent SDK (`types.py:295-299`); HookMatcher mechanism exists; slash commands work via plugin format.

**Not verified**: that "context flag" passing between hooks works as described — Claude Code hooks may not have built-in shared-state primitive. Possible workarounds: external state file, MCP server side state, environment variable. Solvable but not free; resolve in F1 step 3.

### What this adds to F1 + F2

- **F1 step 3**: framework hooks support BOTH implicit (skill-trigger-state) and explicit (prompt-prefix / slash-command) PBS engagement detection. UserPromptSubmit hook drives engagement-flag for downstream hooks. Resolve the context-flag-passing question.
- **F2 specialist authoring discipline**: includes BOTH `when_to_use` triggers AND companion `/pbs-<command>` slash commands for the same skills. Test both paths.
- **Engagement boundary** is a load-bearing F2 concern: skill trigger discipline + hook matcher specificity + workflow phase explicitness.

### Why this strengthens defensibility (axis 3)

If skill triggers are flaky, "did sparring actually fire on this claim?" becomes uncertain. Adding explicit invocation as fallback gives users a way to GUARANTEE engagement when defensibility matters most. That's not a concession — it's strengthening the defensibility-grade properties.

## 7. What to do about LOCKED-STATE.md

Reframe at start of F1. Not delete; not "we were wrong."

- **Status**: `Locked` → `Active development (per NEXT.md)`
- **Move questionable points #8 + #10** from "parked" to "Phase F1 leverage points" (active work)
- **Move questionable points #1-#7 + #9** from "parked" to "deferred — will surface during Phase F2 if real" (still parked, but reframed as "wait for evidence" not "wait for reopening trigger")
- **Update reopen criteria** — they were structured for "lock hold" mindset; replace with milestone-completion checkpoints (F1 close / F2 close / etc.)

Lock-and-park's PURPOSE — preventing premature speculative refactoring without ground truth — was right. Session 35's conversation IS the ground truth that justifies unparking specific things while continuing to defer others.

## 8. Honest framing on what session 35 changed

Session 35's failure mode (AI pattern-matching, user absorbing cognitive load) was real. It cost hours and produced fake roadblocks. But it ALSO produced:

- Clear articulation of Config 3 + Mode A + Mode B
- Tier 1/2/3 deployment shape clarity
- Recognition that SUBPROCESS MCP transport is the actual blocker for deployment goals
- Recognition that practitioner_shape policy values belong as deployment content
- Validation that VISION + most architectural reasoning + mechanism Surfaces survive intact
- Engagement detection design surfaced (combining 3 paths; hook scoping pattern)

Net: session 35 wasn't wasted. The cost was high; the clarification was real. The path forward is concrete and grounded.

**Discipline change for forward sessions**: Cite-or-Read-or-Flag for every architectural claim BEFORE stating it. Mark verified vs inferred status on every "finding" or "gap." Don't pattern-match from session memory.

## 9. Honest basis caveats

- **Verified directly** (read in session 35): VISION axes; glossary entries for shape/practitioner/workspace/framework-c-scope/owner-b-scope; MAINTENANCE.md TOP-LEVEL ARCHITECTURE + DESIGN PRINCIPLES + MILESTONE STRUCTURE + SCOPE; arch/scope-model.md; arch/specialist-skill.md sections 8-12; arch/practitioner.md sections 1-5; arch/adapter.md sections 1-3; pbs/manifests/workspace.py + specialist.py; SDK types.py + README + plugin example; SDK has no native scheduling (verified by grep); Cowork plugin model (verified via web search); UserPromptSubmit hook + prompt field; HookMatcher mechanism
- **Inferred but high-confidence**: Phase F1-F4 sequencing (based on dependency analysis); engagement-flag pattern (composes from verified hook primitives but not a documented PBS pattern); three-tier packaging recommendations (standard infrastructure practice)
- **Not verified**: actual time/effort for each phase (weeks/months are inferred from scope; could be substantially off); that practitioner_shape_*.py refactor is feasible without breaking other framework code (haven't traced all dependencies); how mid-session specialist deactivation works; that hook context-flag passing has a clean primitive in Claude Code (may need workaround)
- **Not verified**: whether Cowork has scheduling capability (web search returned no evidence; doesn't matter for Tier 1+2; matters for Tier 3 SaaS design)

## 10. Net

Goals are realizable with the framework's current architectural commitments. The locked architecture wasn't wrong; the implementation order was. Phase F1 is the focused correction work that unblocks Mode A on Tier 1 — Gunther's daily PBS use. Phase F2 builds the specialist content for real PBS work + engagement boundary discipline. Phase F3 packages for Tier 2 + Mode B scheduler. Phase F4 is much later if/when SaaS audience emerges.

Locked architectural reasoning preserves; specific premature implementation choices get corrected. MS Agent Framework path stays open throughout. Engagement detection design (3 paths combined; hooks scoped to engagement context) directly addresses the "supportive not constraining" experience goal.

Session 35 established what's actually needed. Move into Phase F1 when ready.

---

## Pickup checklist for next session

- [ ] Read this file in full
- [ ] Read `LOCKED-STATE.md` (will be reframed early in F1)
- [ ] Read `findings-from-pbs.md` (currently 1 finding logged)
- [ ] Decide branch strategy: continue on `step-back-evaluation` OR new `phase-f1` branch
- [ ] Begin F1 step 1: scope SUBPROCESS MCP server transport implementation
- [ ] Maintain Cite-or-Read-or-Flag discipline throughout

Sleep well between sessions. Pick up here.
