# Claude session-start procedure (pbs-bureau framework source repo)

This file auto-loads at every session start (including fresh sessions with no prior context). READ before substantive work.

This repo is a **framework source repository** (not a deployment instance). Currently in foundational rebuild — Phase 3 ARCH topical work (post-Phase-2 GLOSSARY lock; 35 entries locked). Per `MAINTENANCE.md` TOP-LEVEL SCOPE: dev skills + framework infrastructure live here permanently; app skills + per-deployment instance content NEVER live here.

## Mandatory session-start reads (substantive work)

Read in this order before substantive work. Skip only for trivial questions (e.g., "what's in this folder").

1. **`VISION.md`** — three-axis thesis (intertwining + sparring + authorship preservation); the ground truth the rebuild serves
2. **`MAINTENANCE.md`** — TOP-LEVEL ARCHITECTURE (framework=mechanisms; shape=policies; A-B-C scope model) + cascade discipline + 5-layer doc model
3. **`DISCIPLINES.md`** — cross-session working discipline; how we operate
4. **`HANDOFF.md`** — current session log; recent notes; what was just done; what's next
5. **`BACKLOG.md`** — Phase-tagged forward-work tracker
6. **`ARCHITECTURE.md`** — Layer 2 overview when working on architectural topics
7. **`GLOSSARY.md`** — Layer 1 vocabulary (35 locked entries) — consult for current term definitions

Specific `arch/<topic>.md` files + specific `profiles/L*.md` profile files load on-demand.

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

When validation requires profile-cluster check (per `decision-design-sharpening` v0.6.0 Round 2 + `coherence-audit` v0.3.1):

1. **READ `profiles/INDEX.md`** for cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators)
2. **READ ≥3 representative profile files** from affected clusters (e.g., L5a + L4a + L8 + L1 for substrate decisions)
3. **Cite profile content** (not just cluster letters A/B/C/D) in chat output

## Why these procedures (not optional conventions)

Pattern-matching from synthesized memory of skill / profile usage **is NOT direct evidence** per global honesty-about-sources rule (`~/.claude/CLAUDE.md`).

**Two failure modes covered**:
- **Compacted session**: pattern-memory of prior usage is directionally correct but misses load-bearing discipline elements. Compaction collapses prior Read content into synthesis-summary.
- **Fresh session (worse)**: no breadcrumbs at all. AI default in absence of pointer-evidence is to do ad-hoc work without recognizing specialized procedures exist.

**Canonical failure (session 16)**: substrate Round 1 post-compact applied `decision-design-sharpening` from synthesized memory; missed layered coverage observation; phase-routed cross-cutting concerns to Phase 6 too aggressively. User had to force re-Read; Round 2 surfaced 11 EXPANSIONS that should have been visible at Round 2 design.

Per `DISCIPLINES.md` Discipline 1 (source-grounded; re-grounding sub-section + skill+profile sub-section).

Per learnings: `learnings/ai-app-development.md` Observation 28.

Per drafts: `drafts/execution-fidelity.md` (META-framework concern; AI faithful execution as load-bearing precondition for every per-axis mechanism).

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

Per memory: `feedback_propose_before_commit.md`, `feedback_judgment_and_automate.md`, `feedback_push_after_commit.md`.

---

This file is **anchor-grade** like VISION/DISCIPLINES/MAINTENANCE — changes should be deliberate. Edits cascade per `MAINTENANCE.md` cascade discipline.
