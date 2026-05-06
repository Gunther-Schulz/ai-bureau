# NEXT — pbs-bureau session handoff (post-2026-05-06)

> **Status**: Working handoff document for the next session. Captures session 35's outcome: lock reopened (it served its purpose); concrete deployment goals clarified; framework/deployment boundary discipline established; phased path forward established with intermediate-milestone discipline; engagement-detection design surfaced; enterprise-landscape research integrated; working discipline corrected.
>
> **What to do at next session start**:
> 1. Read this file in full
> 2. Read `LOCKED-STATE.md` (to be reframed early in F1; currently still in lock framing)
> 3. Read `findings-from-pbs.md` (one finding logged: M1 API friction)
> 4. Decompose F1 into intermediate framework milestones (illustrative draft in §7) and pick the FIRST milestone (F1.0) to execute
>
> **Branch state**: `step-back-evaluation` is current; `lock-and-park` branch was merged into it. F1 work continues on `step-back-evaluation` OR a new `phase-f1` branch (decide at session start).
>
> **Companion artifact**: `~/dev/Gunther-Schulz/pbs-dep-1/` — keep as historical artifact; the deployment attempt that surfaced the gap between architectural intent and implementation reality. Its `findings/2026-05-06-m1-api-friction.md` stays valuable. New deployment validation work begins as `pbs-dep-2` per F1.

---

## 1. Foundational thesis (anchored, not under revision)

From `VISION.md`:
- AI partnership that cultivates expert craft via three axes — **intertwining, sparring, authorship preservation**
- Framework is **shape-neutral** — supports practitioner-shape (PBS-Schulz pioneer), autonomous-business-shape, personal-OS-shape, others
- Pioneer instance: PBS-Schulz planning office; Gunther is the test-deployment practitioner

These remain anchored. Nothing in session 35 challenges them.

## 2. Framework/deployment boundary (load-bearing — applies to all of §3-§12)

Two distinct things, currently easy to conflate:

1. **What we DESIGN and BUILD** = the abstract framework. Shape-neutral. Cross-substrate (Claude Agent SDK + MS Agent Framework). Tier-flexible (Tier 1 local + Tier 2 hosted + Tier 3 SaaS/enterprise). Mode-flexible (Mode A interactive + Mode B orchestrator). Lives in `pbs-bureau/`. Targets the hypothetical N deployments the framework should support.

2. **What we TEST IT AGAINST** = ONE concrete deployment we have available — PBS-Schulz planning office. Domain-specific. Lives in `pbs-dep-2`. Validates whether the abstract realization translates to one real case. Ideally we'd test against ≥10 deployments; we have one.

**The discipline**: framework choices are made for the abstract case (§1 thesis + §3 architectural reality). PBS-Schulz validates whether the abstract realization works for one shape × one substrate × one tier. PBS-Schulz validation passing does NOT mean the framework is correct — it means the framework works for ONE shape × ONE substrate × ONE tier. Mental-modeling against ≥2 hypothetical shapes + ≥2 substrates per architectural commitment is the only way to validate generalization with one available test deployment.

**Each milestone has TWO sides**:
- **Framework side**: architectural commitment realized in code; mental-modeled against ≥2 shapes + ≥2 substrates; contract clarification passes (§6.2); structurally honest, not accidentally fitting one deployment.
- **Deployment side**: PBS-Schulz scenario exercises the framework piece; finding logged in `pbs-dep-2/findings/`; concrete validation lens applied.

Milestone is "done" when BOTH sides land cleanly. PBS-Schulz works but framework is shape-pinned → milestone fails. Framework architecturally clean but PBS-Schulz can't exercise it → milestone fails. Both pass → milestone done.

**This boundary applies above F1-F4. Every phase, every milestone, every contract clarification operates under it.** The composability questions deferred in §3 (multi-shape composability / engagement-target conflation / hybrid-shape mechanics / cross-substrate skill portability / etc.) are addressed continuously per §6.5 mental-modeling discipline at the milestones where they're load-bearing — NOT deferred to "evidence from PBS deployment" because PBS-only evidence won't surface them.

## 3. Concrete framework targets (clarified across session 35)

What the framework must SUPPORT (not what PBS-Schulz happens to need):

1. **Config 3 = machine-enforced framework runtime**: audit-trail integrity, authority-binding enforcement, sparring validation, quality-gate decisions — programmatically, not just prompt-instructed. Required for any shape; PBS-Schulz uses it as one consumer.

2. **Mode A + Mode B both accessible**:
   - Mode A = interactive chat (Claude Code CLI / Claude Desktop / Claude Cowork)
   - Mode B = SDK orchestrator for autonomous/scheduled/batch work

3. **Three-tier deployment progression**:
   - Tier 1: local single-user (PBS-Schulz daily use validates this tier)
   - Tier 2: hosted small-firm (no current validation deployment)
   - Tier 3: dual-track — (a) SaaS for non-coder users; (b) enterprise integration as governance plug-in for Gemini Enterprise / MS Foundry / similar platforms

4. **Two substrate paths preserved**: Claude Agent SDK (primary; Anthropic-native ergonomics) + MS Agent Framework (secondary; Microsoft ecosystem path). Pattern A's ≥2-impl discriminator is real architectural commitment, not aspiration.

5. **Schedulers as part of deployment infrastructure**: cron-style for Tier 1, in-container for Tier 2 Docker, vendor-side for Tier 3 SaaS — running SDK orchestrator scripts. SDK has no native scheduling.

## 3.5. Framework positioning (thin-layer over open standards + platform primitives)

PBS framework is structurally a layered composition, not a self-contained runtime:

| Layer | PBS approach | Why |
|---|---|---|
| **Open standards** (MCP, A2A) | Leverage entirely; PBS just speaks them | Universal cross-vendor adoption per §10; Linux Foundation governance for MCP; verified universal A2A adoption across Claude SDK / MS AF / Google ADK / LangGraph / CrewAI / LlamaIndex / Semantic Kernel / AutoGen |
| **Platform primitives shared across targets** (MCP server creation, permission flow, session management, hook matchers, plugin loading) | Leverage where Claude Agent SDK + MS Agent Framework + Gemini ADK have parity | Reduces framework code; reduces maintenance burden; composes cleanly with platform infrastructure |
| **Cross-platform abstraction** (where Claude SDK / MS AF / Gemini ADK conventions diverge) | Framework provides translation surface; mechanism Surfaces decouple from platform-specific primitives | Pattern A's ≥2-impl discriminator IS this layer's load-bearing reason |
| **PBS-unique discipline** (practitioner-accountability semantics, sparring 8 sub-mechanisms, defensibility test, engaged-authorship operational definition, three-axes composition, workspace/practitioner/specialist/claim/work-unit vocabulary) | Framework owns this entirely; this IS the PBS contribution | Platform vendors address generic AI safety + identity + governance; PBS addresses domain-specific practitioner-accountability discipline that platforms don't |

The framework's substantive value is the bottom row. The top three rows should be as thin as platform parity permits. This positioning is what allows PBS to coexist cleanly with the enterprise landscape (§10) — PBS plugs in as practitioner-accountability layer ON TOP of platform-level governance, not as a competing runtime.

**Architectural test**: for any framework code, ask "does this implement PBS-unique discipline, OR could a platform primitive / open standard provide it?" If the latter, it's a candidate for leveraging rather than building. Composes with §6.6 working discipline.

## 4. Architectural reality mapping

### What survives intact (verified strong in session 35 reads)

- **VISION** — three axes, shape-neutrality, pioneer-instance framing. Anchored.
- **Glossary vocabulary** — workspace, practitioner, specialist, skill, claim, work-unit, audit, sparring, gate, authority-binding, adapter, substrate. Architecturally sound.
- **Mechanism Surfaces** (Pattern A/B/C/D protocol contracts) — audit, sparring, quality-gate, authority-binding, adapter, substrate. Reusable across all tiers + both substrate impls + both modes per §2 boundary.
- **Manifest schemas** (workspace.py, practitioner.py, specialist.py, workflow.py, work_unit.py, claim.py) — Pydantic schemas describe deployment data shapes; reusable across packaging.
- **Three-tier semantics** — Tier 1/2/3 enum already in substrate (`pbs/substrate.py:78-80`); `arch/substrate.md` describes per-tier behavior expectations.
- **Transport modes** — IN_PROCESS / SUBPROCESS / HTTP defined in substrate Pattern A. Supports Mode A (Claude Code → SUBPROCESS MCP) + hosted (HTTP MCP for Tier 3) from day one architecturally.
- **Specialist + skill primitive cluster** — bipartite Pattern B with namespace mechanic; works for the "deployment ships specialists" model.
- **Adapter Pattern A with MCP-Server + A2A-Peer per-class Surfaces** — directly aligns with the open-standards reality: MCP for tool/data integration; A2A for agent-to-agent. Both are universal cross-vendor standards in 2026.
- **Existing Claude Code dev plugin** (`plugin/.claude-plugin/plugin.json`) — proves plugin format works; framework's plugin.json explicitly forecast "Phase 3+ app-skill packaging surface."

### What has gaps (load-bearing for the framework targets, not just PBS-Schulz)

- **SUBPROCESS + HTTP transport implementation** — currently only IN_PROCESS implemented. Mode A (Tier 1 + 2 + 3) needs SUBPROCESS; Tier 3 hosted needs HTTP. Architecturally supported, implementationally NOT built.
- **PBS framework runtime as MCP server(s)** — mechanism Surfaces (audit, sparring, gate, authority, workspace state) need MCP-tool exposure so any external interactive client (Claude Code / Cowork / future) can invoke them. Not built.
- **Framework-level Claude Code plugin content** — hooks (authority/audit/gate enforcement), cross-cutting agents (sparring-partner), framework slash commands (`/pbs-status`, `/pbs-attest`, etc.), framework-level skills (sparring discipline, claim-attestation). Documented in concept; not authored. Same content reusable across MS AF (translated to its plugin/hook conventions) per substrate-agnostic intent.
- **Specialist plugins** — for any deployment, specialists are deployment-side content (per `LOCKED-STATE.md` TOP-LEVEL SCOPE). PBS-Schulz needs planning-document-work + project-management + invoicing; other deployments would need their own specialists.
- **Tier-aware packaging** — no DR locks how PBS distributes per tier. Recommendations (pip+daemon for Tier 1, Docker for Tier 2, SaaS or enterprise plug-in for Tier 3) unspecified architecturally.
- **Scheduler integration** — SDK has no native scheduling; framework has no architectural commitment about how scheduled tasks compose with framework runtime.
- **Engagement detection** — no architectural commitment about how PBS engagement gets detected per prompt; design proposed in §5. Same design applies regardless of which deployment uses it.
- **Enterprise platform integration interfaces** — Microsoft Agent Governance Toolkit's PolicyProviderInterface (and Gemini Enterprise's equivalent) are the right enterprise-tier integration shape. Not on framework's roadmap yet.

### What needs reframing (framework-level questions surfaced session 35)

Of the 9 questionable points in `LOCKED-STATE.md`, session 35 validated TWO as currently load-bearing AND surfaced that the OTHERS need continuous mental-modeling discipline (per §2 + §6.5), not "defer to evidence":

**Currently load-bearing for F1**:
- **#10 (NEW) — Substrate Pattern A model needs clarification**: assumes "framework owns the agent loop." Reality: Mode A means Claude Code (or any chat-host substrate) owns the loop; Mode B means SDK orchestrator drives it. Pattern A primitive may need clarifying that Mode A bypasses substrate as agent-loop-owner and treats it as framework-services-provider via MCP. Mental-model against MS AF: same clarification likely applies (MS AF as agent-loop-owner OR MS AF orchestrator driving substrate-as-services). Resolves at F1.4.
- **#8 — `practitioner_shape_*.py` impls placement**: encode policy values that practitioner-shape requires. Belong as deployment content (per-shape policy bundle), not in framework. Mental-model against autonomous-business-shape: a separate per-shape policy bundle would provide its values; framework keeps mechanism class shells reusable. Resolves at F1.3.

**Continuously addressed via §6.5 mental-modeling at relevant milestones (NOT deferred to PBS evidence)**:
- Multi-shape composability — single workspace.shape vs hypothetical multi-archetype organizations. Mental-model at F1.3 (when externalizing practitioner-shape policy bundle: would the mechanism shell accept multiple shapes' bundles concurrently in a hypothetical autonomous-business + practitioner workspace?).
- Engagement-target entity catalog conflicts — Client vs Customer vs Funder. Mental-model at F2.0 (when authoring first specialist: would the specialist's engagement-target references work for an autonomous-business deployment that uses Customer instead?).
- Specialist `shape_compatibility` runtime semantics — coarse boot-time check. Mental-model at F2.0+ (specialist authoring).
- Hybrid-shape mechanics — placeholder in glossary. Mental-model whenever shape composability surfaces; document deferred decision shape so framework doesn't accidentally close it off.
- Cross-substrate skill portability (W2 watch-list) — Mental-model at F1.4 + F2.0 (framework plugin content + specialist content): would the same skill load on MS AF unchanged?
- Practitioner-shape policy bundle externalization generalization — Mental-model at F1.3 (refactor moment): does the framework's interface accept any shape's policy bundle, not just practitioner-shape's?
- Substrate Pattern A clarification (#10 above) — Mental-model continuously across F1.

The deferred-to-PBS-evidence framing was wrong for shape-neutrality concerns: PBS-only evidence won't surface them. Mental-modeling per `MAINTENANCE.md` D Gate procedure is the existing discipline that addresses this; we've been violating it.

## 5. Why the lock breaks now (and what dep-1 taught us)

The lock served its purpose by forcing a deployment attempt (pbs-dep-1). The attempt revealed:

- The architecture's INTENT supports the framework targets (transport modes, tier semantics, both substrates, plugin-shaped distribution, MCP-server-backed runtime).
- The IMPLEMENTATION chose the wrong order: built IN_PROCESS substrate-as-orchestrator first; should have built SUBPROCESS MCP server transport first to enable any chat-host substrate to connect.
- Some "questionable points" are framework-level architectural clarifications needed (#8 + #10); some are deferred-to-mental-modeling concerns (the other 7 per §4); none turned out to be "wait for evidence" concerns.

So reopening the lock isn't "we got it wrong, restart." It's "implementation order needs correcting based on validated framework architectural intent." Most architectural reasoning preserves; specific Phase 6 implementation work refactors.

**The deeper lesson — load-bearing for §6 working discipline**: dep-1 wasn't deployable for real work, but it surfaced transport gaps + practitioner_shape placement question + substrate model clarification need + Mode A vs Mode B distinction + engagement detection gap. None visible from architectural reasoning alone. Intermediate deployments — even ones not ready to do real work — are the validation mechanism for the deployment side of §2 boundary. Framework-side validation (mental-modeling against ≥2 shapes + ≥2 substrates) is the OTHER half. Both required.

## 6. Working discipline (the corrective from session 35)

Session 35 broke under cognitive load. Diagnosis: load came from cross-module composition questions held simultaneously, not from missing module boundaries. The framework already IS modular (mechanism Surfaces, Pattern A/B/C/D taxonomy, per-class Surfaces, sub-mechanisms, manifest schemas). The corrective is in HOW we work, not in MORE modularity.

Five discipline elements apply across F1+. They compose; none is optional. All operate under §2 framework/deployment boundary.

### 6.1 Deployment-slice work organization

Work is organized by milestone (framework architectural commitment + PBS-Schulz validation), NOT by architectural module. Each session focuses on a vertical slice of what's needed for the current milestone — substrate AND audit AND adapter pieces if they're all needed to advance the milestone, but ONLY the pieces needed.

Modules NOT relevant to current milestone don't load into working memory — they're not in the work, by construction.

### 6.2 One-contract-at-a-time (with framework-side test discipline)

For every architectural commitment surfaced during F1+ work, produce ONE explicit contract clarification before locking it. Format:

- One sentence in plain language: "X promises Y to consumer Z."
- Test against ≥3 concrete scenarios spanning ≥2 hypothetical shapes (e.g., one practitioner-shape PBS-Schulz scenario + one autonomous-business-shape hypothetical + one personal-OS-shape hypothetical) AND mental-model against ≥2 substrates (Claude Agent SDK + MS Agent Framework). Survives all checks → lockable. Fails any → revise the contract before locking.
- Hold ONE contract in working memory at a time. Never juggle.

For F1 specifically: produce contract clarifications for authority-binding (promise to skill authors), audit (promise to defensibility test), quality-gate (promise to engagement-detection), sparring (promise to claim-makers), substrate (promise to specialist authors). Five contracts, one at a time, each tested across hypothetical shapes + substrates AND validated against PBS-Schulz scenario.

If writing a contract clarification surfaces that the current architectural shape doesn't permit a clean one-sentence promise spanning hypothetical shapes/substrates, that's evidence the shape needs revision. Surface to user; don't paper over with hedged contract.

This is where §4 "continuously addressed" composability concerns get resolved: per-contract mental-modeling is the discipline that catches shape-pinning at each architectural commitment.

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

### 6.4 Intermediate-milestone discipline (framework + deployment two-track)

Dep-1 evidence: intermediate deployments — even ones not ready to do real work — surface mismatches between architectural intent and implementation reality that abstract reasoning cannot. Intermediate deployment IS the validation mechanism for the deployment side of §2 boundary, not a celebration at phase end.

Framework side parallel: mental-modeling against ≥2 hypothetical shapes + ≥2 substrates per architectural commitment validates the framework side. Both required.

Each phase decomposes into intermediate milestones with TWO sides:

**Framework side criteria** (what makes a milestone framework-ready):
1. **Architectural commitment named** — what is the framework promising at this milestone? (one sentence)
2. **Mental-modeled against ≥2 shapes** — practitioner-shape + autonomous-business-shape + (optionally) personal-OS-shape; verify the commitment doesn't shape-pin
3. **Mental-modeled against ≥2 substrates** — Claude Agent SDK + MS Agent Framework; verify the commitment doesn't substrate-pin
4. **Contract clarification produced** per §6.2

**Deployment side criteria** (what makes a milestone deployable to dep-2):
1. **Concrete enough to deploy** — actual artifacts produced (not just designs); something runnable / connectable / observable
2. **Bounded enough to deploy now** — narrow scope that can land in one session OR a small cluster of sessions; not multi-week
3. **Surfaces specific assumption** — explicit hypothesis about what the deployment will validate or reveal
4. **Findings expected** — assume the deployment WILL surface mismatches; findings/ entry expected per intermediate milestone, not exception

**Per-phase decomposition**: at start of each phase, decompose into intermediate milestones with explicit framework-side commitments + deployment-side assumption-tests. Don't lock the milestone list rigidly — adjust as evidence accumulates — but always have a NEXT milestone with both sides named.

**Anti-pattern**: treating phase completion as the deployment moment. Wrong. Each intermediate is its own deployment + its own findings cycle.

**Anti-pattern**: PBS-Schulz validation passing OR mental-modeling passing alone. Both must pass for milestone done.

### 6.5 Session behavior derived from 6.1-6.4

Concrete behavioral rules per session:

- **Per-session scope**: pick ONE milestone (or one sub-step of an intermediate milestone). Don't carry over scope from prior sessions; never combine milestones in a single session unless they're truly atomic.
- **Per-claim discipline**: every architectural claim made during F1+ work is either (a) cited from a doc read in current session, (b) read now before stating, or (c) flagged as inferred. No pattern-matching from session memory.
- **Per-contract gate**: lock nothing without producing the §6.2 contract clarification first (with ≥2 shapes + ≥2 substrates mental-modeling). If contract can't be written in one sentence spanning hypothetical shapes/substrates, the shape isn't clear enough OR the framework is shape-pinning.
- **Per-mental-modeling check**: before deferring any §4 "continuously addressed" composability concern at this milestone's commitment, run `MAINTENANCE.md` D Gate procedure (mental modeling within profile grounding); only defer if mental-modeling genuinely cannot resolve.
- **Per-cognitive-load check**: at any session moment where ≥3 architectural modules are in working memory simultaneously, STOP. Surface to user. Decide: defer one module, or split the session.
- **Per-deployment expectation**: every milestone produces at least one finding entry — even if it's "expectation matched, no friction." Keeps the findings/ habit live.
- **Per-leverage check** (per §6.6): before authoring framework code, ask "could a platform primitive / open standard provide this?" If yes and parity exists across target platforms → leverage; framework code unjustified.

### 6.6 Thin-layer architectural posture

Per §3.5 framework positioning: framework code defaults to leveraging platform primitives + open standards; framework owns code only where (a) it implements PBS-unique discipline OR (b) cross-platform abstraction is genuinely required.

Per-milestone implementation question that gates code authoring: "can this be done by leveraging a platform primitive (Claude SDK / MS AF / Gemini ADK) or open standard (MCP / A2A), or does it require framework code?"

- **Leverageable AND parity exists across target platforms** → leverage; framework code unjustified.
- **Leverageable on ONE platform only** → consider whether parity is achievable; if not, framework code provides cross-platform abstraction (Pattern A's ≥2-impl discriminator).
- **Implements PBS-unique discipline** (practitioner-accountability / sparring / defensibility / engaged-authorship / three-axes composition / vocabulary) → framework code justified.

This composes with §6.2 contract clarification — when writing the contract, if the promise turns out to be "what platform primitive X already does," the framework code is unjustified; revise to either reference the platform primitive directly OR identify what PBS-unique discipline is being added on top.

**Anti-pattern**: building framework code that duplicates platform primitives because the framework was designed before platform primitives matured. F1 specifically: SUBPROCESS MCP transport, hook scaffolding, MCP server scaffolding, permission flow wiring may all be platform-leverageable rather than framework-owned. Verify per-milestone before authoring framework code. The 7 platform features verified in §10 enterprise landscape are direct candidates to evaluate for leverage at F1.0-F1.4.

## 7. Path forward — four phases with intermediate framework milestones

Each phase is **framework-architectural-commitment-flavored**, validated by PBS-Schulz deployment per §2 boundary. Same implementation work as a deployment-flavored phasing would produce; framing inverts so framework integrity is the success criterion.

### Phase F1 — Framework runtime architectural commitments (weeks)

**Framework goal**: substrate Pattern A SUBPROCESS realization + framework-as-MCP-services + engagement detection + practitioner-shape policy bundle externalization. All commitments mental-modeled against ≥2 shapes + ≥2 substrates per §6.2.

**Deployment validation lens**: PBS-Schulz Tier 1 daily use exercises the F1 framework realization end-to-end; Mode A through Claude Code CLI.

**Phase F1 verifies**: framework runtime architectural commitments realized + PBS-Schulz Tier 1 use validates the realization works for one concrete shape × substrate × tier.

**Intermediate milestones (illustrative; refine + lock at F1 start per §6.4)** — each has framework side (architectural commitment) + deployment side (PBS-Schulz validation):

- **F1.0 — SUBPROCESS MCP transport architectural commitment realized**
  - *Framework side*: substrate Pattern A SUBPROCESS transport implemented; mental-model against MS AF MCP client (would it connect unchanged?) + against autonomous-business-shape deployment (transport doesn't shape-pin); contract: "framework runtime exposes services as standalone subprocess MCP server; ANY MCP-protocol-speaking client can connect."
  - *Deployment side*: standalone subprocess MCP server starts; Claude Code MCP client (PBS-Schulz validation surface) connects; empty tool list returned.
  - *Tests*: does SUBPROCESS transport compose cleanly with MCP-protocol clients (PBS validates with Claude Code; mental-model validates with MS AF)?

- **F1.1 — Audit Surface MCP-tool exposure architectural commitment realized**
  - *Framework side*: ONE concrete framework service (e.g., `pbs_audit_emit`) exposed as MCP tool; mental-model against autonomous-business deployment using same audit Surface for action-level granularity; contract for audit Surface produced per §6.2.
  - *Deployment side*: PBS-Schulz Claude Code invokes `pbs_audit_emit`; audit-trail records the invocation with hash-chain integrity.
  - *Tests*: does the framework's audit Surface compose cleanly with MCP tool-call semantics across hypothetical deployments?

- **F1.2 — Engagement-detection hook architectural commitment realized**
  - *Framework side*: PreToolUse hook activates only when engagement-detection flag set; gates on authority-binding catalog. Mental-model against MS AF hook system equivalents (would the engagement-detection pattern translate?). Contract for authority-binding Surface produced per §6.2; resolves the context-flag-passing question from §5.
  - *Deployment side*: PBS-Schulz Claude Code session — `pbs:` prefix sets engagement; framework hook fires; non-engaged prompt skips hook; zero overhead on plain Claude work.
  - *Tests*: does the engagement-detection pattern (UserPromptSubmit → flag → downstream hooks) work in both substrate hook systems (PBS validates Claude Code; mental-model validates MS AF)?

- **F1.3 — Per-shape policy bundle externalization architectural commitment realized**
  - *Framework side*: refactor `practitioner_shape_*.py` policy values out of `pbs/impls/`; framework keeps mechanism class shells (SparringProtocol, QualityGateProtocol, AuthorityBindingProtocol); ANY shape's policy bundle plugs in. Mental-model: hypothetical autonomous-business-shape policy bundle would plug into the same mechanism shells — no framework changes needed.
  - *Deployment side*: pbs-dep-2 provides practitioner-shape policy bundle; framework loads it cleanly; PBS-Schulz session uses externalized values.
  - *Tests*: does the framework cleanly accept per-deployment policy values for ANY shape? Resolves LOCKED-STATE questionable point #8 + addresses §4 "continuously addressed" multi-shape composability concern at the externalization moment.

- **F1.4 — Framework plugin content + Hello PBS v2 (full F1 wiring)**
  - *Framework side*: framework-level Claude Code plugin content authored — hooks (authority/audit/gate enforcement), cross-cutting sparring-partner agent, framework slash commands (`/pbs-status`, `/pbs-attest`, `/pbs-audit-query`, `/pbs-spar`), framework-level skills (sparring discipline, claim-attestation, defensibility-test). Mental-model: same content translates to MS AF plugin/hook conventions (W2 cross-substrate skill portability). Contract clarifications per §6.2 produced for sparring + quality-gate + substrate Surfaces. Resolves LOCKED-STATE questionable point #10.
  - *Deployment side*: PBS-Schulz end-to-end interactive flow — open Claude Code, PBS framework plugin loaded, MCP servers connected, practitioner-shape policy bundle from dep-2, basic work runs through Config 3 enforcement.
  - *Tests*: does the full F1 stack produce the promised "supportive not constraining" experience? Does framework content translate to a hypothetical MS AF deployment without framework changes?

Each F1.k is its own framework commitment + dep-2 deployment. Findings expected at each.

### Phase F2 — Specialist primitive realization + Layer A scope-resolution + adapter MCP-corpus realization (months)

**Framework goal**: specialist primitive cluster fully exercised via real specialist authoring; Layer A scope-resolution exercised via real domain content; MCP-corpus adapter Surface exercised via real corpus backend. All commitments mental-modeled against hypothetical autonomous-business or personal-OS specialists.

**Deployment validation lens**: PBS-Schulz produces real planning work daily — B-Plan-Begründung sections, attestations, defensibility-grade audit trail.

**Phase F2 verifies**: specialist primitive + Layer A + adapter architectural commitments realized + PBS-Schulz daily-use validates the engagement experience matches "supportive not constraining."

**Intermediate milestones (decompose at F2 start per §6.4)** — illustrative shape:

- F2.0: One specialist (probably planning-document-work) authored per `arch/specialist-skill.md` §2.3 manifest schema + §10 namespace mechanic; mental-model: hypothetical autonomous-business invoicing specialist would follow same authoring pattern; deployable in dep-2.
- F2.1: First real B-Plan-Begründung section drafted via PBS; first real claim_attested event with HUMAN actor per practitioner-shape policy; first real claim-defensibility audit-trail entry.
- F2.2: Second + third specialists (project-management, invoicing) authored; cross-specialist composition tested per `arch/specialist-skill.md` §10 cross-specialist composition rules; mental-model: cross-specialist composition for hypothetical autonomous-business multi-specialist deployment.
- F2.3: Layer A content for one real domain + one real state added; corpus retrieval tested via MCP-corpus adapter; adapter Surface contract validated; mental-model: hypothetical research-lab Layer A scope-resolution.
- F2.4: Daily-use threshold — PBS replaces whatever Gunther currently uses for the work this milestone covers; F2 deployment-side validation complete.

**Engagement boundary discipline applied at every specialist** (per §5+§6): narrow honest `when_to_use` triggers, companion slash commands for explicit invocation, workflow phase declarations explicit. Mental-model engagement boundary against hypothetical autonomous-business specialist: would `pbs:` prefix mechanism work the same?

### Phase F3 — Tier 2 packaging architectural commitment + Mode B scheduler integration (months)

**Framework goal**: three-tier packaging architectural commitment realized for Tier 2 (Tier 1 + Tier 3 paths retained); Mode B SDK orchestrator pattern realized; scheduler integration architectural pattern locked. All mental-modeled against MS AF substrate impl swap-in.

**Deployment validation lens**: PBS-Schulz Tier 2 hosted deployment (could be small local server / VPS); first scheduled task runs autonomously.

**Phase F3 verifies**: Tier 2 packaging + Mode B + scheduler architectural commitments realized + PBS-Schulz Tier 2 deployment validates them.

**Intermediate milestones (decompose at F3 start per §6.4)** — illustrative shape:

- F3.0: Docker image bundling framework runtime + MCP servers boots cleanly in a container; mental-model: hypothetical MS AF substrate impl would swap in via image variant.
- F3.1: SDK orchestrator script template (Hello PBS evolved); runs once successfully driving Claude through PBS-loaded plugin via Mode B.
- F3.2: First scheduled task: monthly invoicing OR similar; runs autonomously via cron-in-container; audit-trail captures everything; mental-model: hypothetical autonomous-business deployment using same scheduler pattern for back-office operations.
- F3.3: Container deployment tested on a small VPS; persistence + scheduler + MCP servers all survive container restart.

### Phase F4 — Tier 3 dual-track (much longer; only when audience demands)

**Framework goal**: Tier 3 architectural commitments realized — either Track A (multi-tenant SaaS) OR Track B (enterprise platform integration as governance plug-in) OR both. Extends realized commitments rather than introducing new architecture.

**Deployment validation lens**: depends on which track activates — Track A validated by Cowork SaaS user; Track B validated by enterprise deployment using Gemini Enterprise / MS Foundry / similar.

**Track A — SaaS for Cowork users**: hosted multi-tenant PBS; user signs up; gets workspace provisioned; connects Cowork via OAuth. Vendor operates infrastructure (hosting, billing, GDPR, multi-tenancy, security, uptime). This is a SaaS business, not just packaging.

**Track B — Enterprise integration**: PBS framework's existing A2A-Peer adapter class + MCP transport + Pattern A substrate plurality is the right architectural position for the heterogeneous A2A-interop enterprise reality (verified: A2A is Google-originated open standard with universal adoption — Microsoft Agent Framework, Google ADK, LangGraph, CrewAI, LlamaIndex, Semantic Kernel, AutoGen). Microsoft Agent Governance Toolkit's PolicyProviderInterface (and equivalent extension points in other platforms) explicitly support framework-agnostic governance plug-ins. PBS could plug in as the practitioner-accountability layer ON TOP of platform-level governance.

The opportunity: practitioner-accountability + defensibility for expert-practitioner verticals is a specific gap the giant platforms address generically, not professionally. PBS could fill it. Doesn't require betting on Google OR Microsoft — works in environments using either or both via open standards (MCP universal; A2A universal).

**Defer F4 entirely** until: (a) Tier 1 + Tier 2 are solid; (b) actual audience demand exists; (c) Gunther has appetite for SaaS operations OR concrete enterprise inquiry surfaces.

### Throughout: MS Agent Framework path stays viable

Phases F1-F3 stay substrate-impl-agnostic at framework runtime + MCP server layer per §2 boundary + §6.2 contract discipline. MS AF substrate impl can land later (Phase F2 or F3) without disturbing the rest. Pattern A's ≥2-impl discriminator stays satisfied. The "stays viable" guarantee comes from per-milestone mental-modeling against MS AF, not from a one-time architectural review.

## 8. Engagement detection design

**The question**: in daily Claude Code use (or any chat-host substrate), how is it decided what gets routed through PBS framework enforcement vs flows as plain chat work? How does the user get the "supportive not constraining" experience?

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
    skip — plain chat work, zero overhead
```

Framework enforcement happens only when PBS is actually engaged. No background overhead on plain chat work. Addresses "supports but doesn't feel constrained" goal directly. Same pattern applies regardless of which substrate hosts the chat.

**Why this strengthens defensibility (axis 3)**: if skill triggers are flaky, "did sparring actually fire on this claim?" becomes uncertain. Adding explicit invocation as fallback gives users a way to GUARANTEE engagement when defensibility matters most. Strengthens defensibility-grade properties.

**Implementation status**: UserPromptSubmit hook with `prompt: str` field exists in Claude Agent SDK (verified `types.py:295-299`); HookMatcher mechanism exists; slash commands work via plugin format. Context-flag-passing between hooks may need workaround (external state file / MCP server side state / environment variable) — resolve in F1.2. Mental-model at F1.2: equivalent hook primitives in MS AF.

## 9. LOCKED-STATE.md reframing (early F1 task)

Reframe at start of F1. Not delete; not "we were wrong."

- **Status**: `Locked` → `Active development (per 1-NEXT.md)`
- **Move questionable points #8 + #10** from "parked" to "F1 leverage points" (active framework architectural commitments per §4)
- **Move questionable points #1-#7 + #9** from "parked" to "continuously addressed via §6.5 mental-modeling discipline at relevant milestones" (NOT "wait for evidence" — that framing was wrong because PBS-only evidence won't surface them)
- **Replace reopen criteria** with milestone-completion checkpoints (F1.0 / F1.1 / F1.2 / F1.3 / F1.4 close + F1 close + F2.x close + F3.x close); each milestone has framework-side + deployment-side criteria per §6.4

Lock-and-park's PURPOSE — preventing premature speculative refactoring without ground truth — was right. Session 35's conversation IS the ground truth that justifies unparking specific things while continuing to address others via mental-modeling rather than speculative implementation.

## 10. Enterprise landscape context (for F4 planning when activated)

Verified state of the agentic deployment landscape, 2025-2026:

- **MCP** (Model Context Protocol): donated to Linux Foundation December 2025; universal cross-vendor adoption (Anthropic, Microsoft, Google, OpenAI). THE standard at the tool/data integration layer. Got stronger in 2026, not weaker. PBS commits to MCP as primary integration protocol — well-positioned.

- **A2A** (Agent-to-Agent): Google-originated; native support across Google ADK + Microsoft Semantic Kernel/AutoGen + LangGraph + CrewAI + LlamaIndex + Microsoft Agent Framework; 150+ orgs production. Cross-vendor interop verified. PBS adapter Pattern A's A2A-Peer class commits to A2A — aligned with the standard.

- **Microsoft Agent Framework + Foundry + Agent Governance Toolkit**: framework-agnostic governance via PolicyProviderInterface; framework deploys to containers / on-premises / multi-cloud; full enterprise governance via Azure AI Foundry hosting. Open standards: MCP, A2A, OpenAPI, pluggable memory.

- **Google Gemini Enterprise Agent Platform** (April 2026, evolution of Vertex AI): Agent Identity (cryptographic IDs + audit), Agent Registry, Agent Gateway, Agent Anomaly Detection, Agent Sandbox. MCP supported. Multi-model (Anthropic Claude + Gemma + others).

- **Regulatory pressure**: EU AI Act enforced 2025; high-risk AI systems require detailed activity logs preserved for regulatory review; up to 3% global annual turnover penalty. Practitioner-accountability + defensibility-grade audit-trail (PBS axis-3) is regulatory-aligned.

- **Market governance maturity**: 80% of enterprises deploying agents lack mature governance; only 21% have it. Platform vendors (MS + Google) filling this generically; PBS could fill domain-specific (practitioner-shape) niche.

This context informs F4 positioning but does not affect F1-F3 work. Don't divert F1-F3 to chase enterprise integration. Capture as forward-reference for F4 activation.

## 11. Honest framing on what session 35 changed

Session 35's failure mode (AI pattern-matching, user absorbing cognitive load) was real. It cost hours and produced fake roadblocks. But it ALSO produced:

- Clear articulation of Config 3 + Mode A + Mode B
- Tier 1/2/3 deployment shape clarity
- Recognition that SUBPROCESS MCP transport is the actual blocker for the framework's transport architectural commitment
- Recognition that practitioner_shape policy values belong as deployment content (per-shape policy bundle pattern)
- Validation that VISION + most architectural reasoning + mechanism Surfaces survive intact
- Engagement detection design (combining 3 paths; hook scoping pattern)
- Enterprise landscape research integrated (open-standards layer cake; PBS positioned for it)
- Working discipline corrective (deployment-slice + one-contract + cognitive-entry-path + intermediate-milestone)
- **Framework/deployment boundary discipline (§2)** — explicit recognition that PBS-Schulz validation is one lens, not the framework's definition

Net: session 35 wasn't wasted. The cost was high; the clarification was real. The path forward is concrete and grounded.

**Discipline change for forward sessions** (codified in §6): Cite-or-Read-or-Flag for every architectural claim BEFORE stating it; one-contract-at-a-time discipline with ≥2 shapes + ≥2 substrates mental-modeling; deployment-slice scope per session; cognitive entry path docs; intermediate-milestone deployments as deployment-side validation paired with mental-modeling as framework-side validation.

## 12. Honest basis caveats

- **Verified directly** (read in session 35): VISION axes; glossary entries for shape/practitioner/workspace/framework-c-scope/owner-b-scope; MAINTENANCE.md TOP-LEVEL ARCHITECTURE + DESIGN PRINCIPLES + MILESTONE STRUCTURE + SCOPE; arch/scope-model.md; arch/specialist-skill.md sections 8-12; arch/practitioner.md sections 1-5; arch/adapter.md sections 1-3; pbs/manifests/workspace.py + specialist.py; SDK types.py + README + plugin example; SDK has no native scheduling (verified by grep); Cowork plugin model (verified via web search); UserPromptSubmit hook + prompt field; HookMatcher mechanism; A2A is Google-originated open standard (verified via web search); MCP donated to Linux Foundation (verified via web search); Microsoft Agent Governance Toolkit framework-agnostic via PolicyProviderInterface (verified via web search).

- **Inferred but high-confidence**: F1-F4 sequencing (based on dependency analysis); engagement-flag pattern (composes from verified hook primitives but not a documented PBS pattern); three-tier packaging recommendations (standard infrastructure practice); intermediate-milestone discipline as the right corrective for session 35's failure mode (extracted from dep-1 outcome); framework/deployment boundary as load-bearing structural framing (extracted from dep-1 + your articulated boundary intuition).

- **Inferred and uncertain**: that one-session-per-intermediate-milestone is achievable (could be too aggressive or too conservative; calibrate during F1); that the F1.0-F1.4 illustrative decomposition is right (these are MY guess at sensible intermediate points; needs reaction at F1 start; could be wrong about which boundaries matter most); that ≥2-shapes + ≥2-substrates mental-modeling at every contract is operationally sustainable (could feel heavy; calibrate during F1); that practitioner-accountability is genuinely a gap platforms don't address (based on reading their feature lists; didn't exhaustively search).

- **Not verified**: actual time/effort for each phase (weeks/months are inferred from scope; could be substantially off); that practitioner_shape_*.py refactor is feasible without breaking other framework code (haven't traced all dependencies); how mid-session specialist deactivation works; that hook context-flag passing has a clean primitive in Claude Code (may need workaround); that MS AF has equivalent hook primitives for engagement-detection pattern (mental-modeling deferred to F1.2 implementation moment); whether Cowork has scheduling capability (matters for Track A SaaS design, not for Tier 1+2); that PolicyProviderInterface specifically would accept PBS's mechanism Surface shape (would need to read interface spec for Track B).

## 13. Net

The framework's targets are realizable with the framework's current architectural commitments. The locked architecture wasn't wrong; the implementation order was; AND the framework/deployment boundary discipline (§2) was implicit, now explicit. F1 is the focused correction work that realizes the framework's runtime architectural commitments — validated by PBS-Schulz Tier 1 daily use. F2 realizes specialist + Layer A + adapter commitments — validated by PBS-Schulz daily real planning work. F3 realizes Tier 2 packaging + Mode B scheduler commitments — validated by PBS-Schulz Tier 2 deployment. F4 dual-track (SaaS + enterprise integration) waits for evidence.

Locked architectural reasoning preserves; specific premature implementation choices get corrected. MS Agent Framework path stays viable through per-milestone mental-modeling, not one-time review. Engagement detection design (3 paths combined; hooks scoped to engagement context) directly addresses the "supportive not constraining" experience goal. Enterprise landscape is favorable (open standards converge; PBS positioned for both standalone and platform-integration).

Move into F1 when ready, per §2 framework/deployment boundary + §6 working discipline (deployment-slice scope per session + one-contract-at-a-time with ≥2-shapes-+-≥2-substrates mental-modeling + cognitive entry path + intermediate-milestone deployments with framework + deployment two-track criteria) — not the previous open-ended cluster-execution methodology.

---

## Pickup checklist for next session

- [ ] Read this file in full
- [ ] Read `LOCKED-STATE.md` (will be reframed early in F1 per §9)
- [ ] Read `findings-from-pbs.md` (currently 1 finding logged)
- [ ] Decide branch strategy: continue on `step-back-evaluation` OR new `phase-f1` branch
- [ ] **Internalize §2 framework/deployment boundary** — every milestone has framework side + deployment side; both must pass
- [ ] **Author `READ-ME-FIRST.md` (cognitive entry paths) early in F1 per §6.3** — even before its first use, just to enable it
- [ ] **Decompose F1 into intermediate milestones with framework-side commitment + deployment-side assumption-test per §6.4** — react to illustrative F1.0-F1.4 in §7 or revise
- [ ] **Pick the FIRST milestone (F1.0) to execute** — one milestone per session
- [ ] **Apply session behavior rules from §6.5**: per-session scope discipline; Cite-or-Read-or-Flag on every claim; per-contract gate before locking (with ≥2 shapes + ≥2 substrates mental-modeling); per-mental-modeling check on §4 continuously-addressed concerns; per-cognitive-load check (halt if ≥3 modules in working memory); per-deployment expectation (findings entry per milestone); per-leverage check (§6.6) before authoring framework code
- [ ] **Apply §3.5 framework positioning + §6.6 thin-layer posture** at every F1 architectural choice — default to leveraging platform primitives + open standards; build framework code only for PBS-unique discipline OR cross-platform abstraction

Sleep well between sessions. Pick up here.
