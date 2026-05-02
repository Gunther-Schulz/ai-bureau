# Claude session-start procedure (pbs-bureau framework source repo)

This file auto-loads at every session start (including fresh sessions with no prior context). READ before substantive work.

This repo is a **framework source repository** (not a deployment instance). Currently in foundational rebuild — Phase 3 ARCH topical work (post-Phase-2 GLOSSARY lock; 36 entries locked). Per `MAINTENANCE.md` TOP-LEVEL SCOPE: dev skills + framework infrastructure live here permanently; app skills + per-deployment instance content NEVER live here.

## Mandatory session-start reads (substantive work)

Read in this order before substantive work. Skip only for trivial questions (e.g., "what's in this folder").

1. **`VISION.md`** — three-axis thesis (intertwining + sparring + authorship preservation); the ground truth the rebuild serves
2. **`MAINTENANCE.md`** — TOP-LEVEL ARCHITECTURE (framework=mechanisms; shape=policies; A-B-C scope model) + cascade discipline + 5-layer doc model
3. **`DISCIPLINES.md`** — cross-session working discipline; how we operate (per-discipline detail in `disciplines/<id>.md`, loaded on demand)
4. **`HANDOFF.md`** — current session log; recent notes; what was just done; what's next
5. **`BACKLOG.md`** — Phase-tagged forward-work tracker
6. **`ARCHITECTURE.md`** — Layer 2 overview when working on architectural topics
7. **`GLOSSARY.md`** — Layer 1 vocabulary index (36 locked entries; full body in `glossary/<entry>.md`, loaded on demand)

Specific `arch/<topic>.md` + `disciplines/<id>.md` + `glossary/<entry>.md` + `profiles/L*.md` files load on-demand.

## Cascade discipline (sub-agent-first; mandatory for multi-file architectural work)

Per session-18 research into Claude/agent adherence + Anthropic engineering guidance: oversized context + cascade-mode load reliably degrade instruction adherence (per Chroma context-rot study + AgentIF benchmark + Anthropic's "Bloated CLAUDE.md files cause Claude to ignore your actual instructions"). Five mitigations now codified:

1. **Sub-agent-first for cascade work**. Any multi-file architectural cascade (≥3 files of Layer 0/1/2/3 edits, or any cascade involving GLOSSARY / ARCHITECTURE / MAINTENANCE / arch/* / docs/decisions/*) MUST be delegated to general-purpose sub-agent(s). Brief each with focused scope + the specific files + relevant disciplines (NOT full corpus). Sub-agent works in clean fresh context; returns summary; main agent reviews + commits + pushes. Per Anthropic: "subagents are one of the most powerful tools available... preserve context by keeping exploration and implementation out of your main conversation."

2. **Writer-Reviewer pattern**. For any architectural commit (Layer 0/1/2/3), spawn a separate Reviewer sub-agent against the diff before push. Reviewer reads relevant disciplines, scans for breadcrumbs / instance-leakage / cargo-cult / cascade-miss. Per Anthropic: "Separating the agent doing the work from the agent judging it proves to be a strong lever" (counters self-praise bias).

3. **`/clear` between cascade chunks**. Recommend `/clear` at natural cascade boundaries (between Steps; between major files). User discipline; AI surfaces "recommend /clear before next chunk" at boundaries. Per Anthropic: "A clean session with a better prompt almost always outperforms a long session with accumulated corrections."

4. **HARD STOP markers**. Each logical work unit ends with HANDOFF write + commit + push + STOP. AI surfaces "logical unit complete; recommend HARD STOP" at natural boundaries. Per agent-loop research: structural session boundaries, not verbal commitments to stop.

5. **Ralph Loop self-check at apparent completion**. Before declaring done, AI explicitly asks: "Did I read every file the procedure listed? Did I apply every discipline cited? Did I leave anything unfinished?" Catches "agentic laziness" (per Anthropic long-running Claude research). Composes with M2 Reviewer.

## Specialized skill invocation procedure (mandatory at every invocation)

When invoking a sharpening / audit / validation skill, do this — every time, regardless of prior usage in same session:

1. **READ the SKILL.md via Read tool** (full file)
2. **Apply the skill's procedure** with file content present in current context
3. **Cite specific skill section names** in chat output (e.g., "per layered coverage observation"; "per Lens 8"; "per Round 2 termination self-check") — proves Read happened, not pattern-matched

Skills in scope:
- `plugin/skills/decision-design-sharpening/SKILL.md` — architectural decision sharpening (pre-commit; one decision; 2-3 round sweet spot)
- `plugin/skills/pre-implementation-sharpening/SKILL.md` — implementation-start sharpening (operational/runtime detail surfacing)
- `plugin/skills/coherence-audit/SKILL.md` — cross-decision corpus audit (10 universal lenses + corpus-specific)
- `plugin/skills/sharpen/SKILL.md` — generic critical-pass discipline

## Profile-anchored validation procedure (mandatory when triggered)

When validation requires profile-cluster check (per `decision-design-sharpening` v0.6.0+ Round 2 + `coherence-audit` v0.3.1+):

1. **READ `profiles/INDEX.md`** for cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators)
2. **READ ≥3 representative profile files** from affected clusters (e.g., L5a + L4a + L8 + L1 for substrate decisions)
3. **Cite profile content** (not just cluster letters A/B/C/D) in chat output

## Structural enforcement (PreToolUse hook on architectural artifacts)

`plugin/hooks/architectural_commit_gate.py` is a PreToolUse hook (active when `/reload-plugins` has run after the latest plugin.json change). On Edit/Write/MultiEdit to architectural artifacts (arch/* / docs/decisions/* / ARCHITECTURE.md / GLOSSARY.md / MAINTENANCE.md / DISCIPLINES.md), it blocks the write unless required prep Reads happened in current session AND the write content passes provenance-hygiene regex (no narrative breadcrumbs in canonical content).

Hook is **structural enforcement** per Anthropic recommendation ("Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens"). NOT a bandaid. Disabling shifts back to prose-rule discipline which has empirically failed across multiple sessions.

## Why these procedures (not optional conventions)

Pattern-matching from synthesized memory of skill / profile usage **is NOT direct evidence** per global honesty-about-sources rule (`~/.claude/CLAUDE.md`).

**Failure modes covered**:
- **Compacted session**: pattern-memory of prior usage is directionally correct but misses load-bearing discipline elements
- **Fresh session**: no breadcrumbs at all; AI default in absence of pointer-evidence is to do ad-hoc work without recognizing specialized procedures exist
- **Cascade-mode load**: under multi-file cascade work, AI drops disciplines that were read at session-start; mitigated by sub-agent-first routing (M3 above)

Per `DISCIPLINES.md` Discipline 1 (source-grounded; re-grounding sub-section + skill+profile sub-section).

Per learnings: `learnings/ai-app-development.md` Observation 28 (canonical session-16 case) + Observation 30 (framework-recursion-trap discipline).

Per drafts: `drafts/execution-fidelity.md` (META-framework concern; AI faithful execution as load-bearing precondition for every per-axis mechanism; disguises catalog 1-10).

## Repository identity (load-bearing)

**This repo = framework source, not a deployment instance.** Per `MAINTENANCE.md` TOP-LEVEL SCOPE:

- Dev skills (sharpening / audit / validation) live here permanently in `plugin/skills/`
- App skills (per-deployment workspace skills; specialist DEFINITIONs; per-shape policy bundles) NEVER live here — they belong in deployed workspaces
- Framework distribution mechanics + app-skill packaging surface in Phase 3+ ARCH work

## Working procedure

Per `DISCIPLINES.md` "Working procedure":
- AI proposes positions → user adjusts/challenges/confirms → AI persists on sign-off
- **Decision phase** (positions, framings, choices): user approval needed before persistence
- **Content phase** (markdown content following locked decisions): write directly without per-content approval
- **Commit positions, don't menu**: AI commits to recommendations with rationale; user shapes via challenge or confirmation
- **Commit and push often**: no per-commit confirmation needed; treat push as part of commit

Per memory: `feedback_propose_before_commit.md`, `feedback_judgment_and_automate.md`, `feedback_push_after_commit.md`, `feedback_subagent_first_cascade.md`, `feedback_hooks_are_structural.md`.

---

This file is **anchor-grade** like VISION/DISCIPLINES/MAINTENANCE — changes should be deliberate. Edits cascade per `MAINTENANCE.md` cascade discipline.
