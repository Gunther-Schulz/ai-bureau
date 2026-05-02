# Quality gate — DRAFT

> **STATUS: DRAFT — not locked, not final, candidate among many.** Exploratory capture of "could the sharpening spirit also be a quality-gate mechanism in the framework's product?" surfaced session 16 (2026-05-02) while building the generic `sharpen` skill. Not load-bearing yet. Lifts to ARCH (Phase 3) when the framework architecture surfaces concrete deliverables that could embed quality-gate mechanisms; OR to ROADMAP (Phase 5) as a feature commitment.

## Origin

User mid-flow during `sharpen` skill creation: "this could be also transferred into some sort of 'quality' gate or something for our framework. where should that go?"

Captured here as exploratory idea — not yet committed to architecture.

## The idea

The sharpening spirit (challenge → surface → refine → commit position) currently lives as DEV TOOLING (the four sharpening skills used while BUILDING the framework). The thought: could the same spirit become a **product-side mechanism** — a quality gate that fires at runtime checkpoints in deployments?

If yes, deployments would have built-in critical-pass capability — not just AI generating content, but AI generating content + critical-pass-against-it before commit / send / publication.

## What it gates against (locked-concept-anchored, session 16)

After `category collapse` locked in GLOSSARY: quality-gate's purpose is now precisely articulable. The gate would monitor for **category collapse manifestations** — the cross-axis force degrading practitioner engagement from higher-engagement state to lower-engagement state regardless of architectural intent.

Per-axis manifestations (what the gate would watch for):

| Axis | Higher-engagement state | Failure mode (collapse outcome) |
|---|---|---|
| Axis 1 | intertwined AI | tacked-on AI |
| Axis 2 | sparring | answer-machine / oracle / validator AI (Ming-research distinction) |
| Axis 3 | engaged authorship | rubber-stamping |

Without quality-gate (current state): category-collapse-resistance is ENABLED architecturally but not ENFORCED. Sparring sub-mechanisms are available; whether they fire at meaningful moments is practitioner-cognitive-state-dependent.

With quality-gate: sparring becomes structurally checkpointed at specific moments (per "Possible mappings" below) — converting enablement to partial enforcement at gate-firing moments. Per category collapse entry: *"architecture enables but doesn't enforce mental category."* Quality-gate would change that — at least at gate-firing moments.

## Prerequisites for Phase 3 ARCH development

Quality-gate ARCH topic development depends on:
- ✅ `category collapse` (locked session 16 — the force the gate gates against)
- ⏳ `answer-machine AI` / `oracle AI` / `validator AI` (axis-2 failure mode taxonomy; locking next per foundation-up)
- ⏳ `rubber-stamping` (axis-3 failure mode; locking after axis-2 trio)
- Phase 3 architectural decisions: mechanism vs Pattern A protocol; per-shape variation; observability schema; intervention mechanics

Until prerequisites land: quality-gate stays as draft.

## Possible mappings

What runtime checkpoints could quality-gate fire at?

- **Pre-send gate**: before practitioner-authored work goes out (Begründung, brief, manuscript), AI applies sharpening pass against the work (load-bearing vs decorative; overclaim vs grounded; gaps; clarity)
- **Pre-claim-finalization gate**: when a claim is about to be marked finalized (signed-claim_made event), apply sharpening pass against the claim's evidence chain
- **Pre-decision-lock gate**: when a workspace-level decision is about to lock (workflow choice, specialist activation), apply sharpening pass
- **Per-edit gate**: lighter touch — every substantive content edit triggers brief sharpening check
- **Drift-audit gate**: periodic / scheduled — apply coherence-audit-style pass on workspace's accumulated work-units

## Architectural questions (Phase 3 ARCH territory if pursued)

- Is quality-gate a MECHANISM (atomic interface contract) or a PROTOCOL (Pattern A pluggable subsystem)?
- Surface (interface contract) — what does "apply sharpening pass" mean as framework-level operation?
- Implementations — could vary per shape (practitioner-shape may want strict gate; personal-OS-shape may want light gate)
- Selection — workspace-level activation? Shape policy?
- Composes with which existing primitives? mechanism (gate IS a mechanism); claim (gate fires per claim?); event (gate emits gate-fired events to audit trail); workflow (gate fires at workflow stages)

## Why this might be load-bearing

Quality-gate would operationalize axis-2 (sparring) as a STRUCTURAL FEATURE, not just a runtime-mode-AI-engages-in. Architecturally would tie in with:
- Audit emission (gate-fired events recorded)
- Authorship preservation (gate is part of "engaged authorship" condition for defensibility)
- Claim-level mechanics (gate fires per claim)
- Source-grounding mechanism (gate verifies claims trace to source)

Could be a load-bearing PRODUCT feature that distinguishes PBS from "AI assistant" tools — the AI doesn't just generate; it generates AND CRITIQUES under structured discipline before output goes out.

## Why this might NOT be load-bearing

- Already covered by sparring (axis 2): if sparring is "always-on runtime mechanism," gate is just a special case of sparring fired at checkpoints
- Could be over-architecting: maybe sparring at runtime is sufficient; doesn't need formal gate mechanism
- Risks bureaucratic overhead: every commit/send goes through gate = friction

Need: practitioner-deployment data to test whether quality-gate-as-formal-mechanism adds value beyond axis-2 sparring at runtime.

## Maturity test

This draft graduates to ARCH (Phase 3) or ROADMAP (Phase 5) when:

- Phase 3 ARCH surfaces work on axis-2 mechanism encoding (would clarify whether gate is sub-mechanism or distinct primitive)
- Pioneer deployment data shows whether axis-2 runtime sparring is sufficient or whether additional gate-mechanism adds value
- User locks specific intent (e.g., "yes, build gate as runtime feature" → ROADMAP Phase 5 work item)

Until then: stays as draft loose-thinking. Future-session reference for "could we build sharpening as runtime feature?" exploration.

## Cross-references

- `plugin/skills/sharpen/SKILL.md` — the dev-tooling generic-sharpening skill (would be the parent pattern if quality-gate productized)
- `plugin/skills/decision-design-sharpening/SKILL.md` — specialized sharpening (pre-decision)
- `plugin/skills/pre-implementation-sharpening/SKILL.md` — specialized sharpening (implementation-start)
- `plugin/skills/coherence-audit/SKILL.md` — specialized sharpening (corpus)
- `BACKLOG.md` Phase 3 ARCH — entry pointing to this draft for ARCH consideration
- `VISION.md` axis 2 — sparring as runtime mechanism (would extend to formal-gate if pursued)
