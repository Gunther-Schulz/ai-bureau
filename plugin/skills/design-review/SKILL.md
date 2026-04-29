---
name: design-review
description: This skill should be used when the user requests a first-principles review of the system's architecture / plugin / backend / docs to surface design soundness issues — phrases like "design review", "is this design right", "first-principles review", "would we build this from scratch", "rough cut review", "review the architecture for soundness", "Designprüfung", "Grundüberprüfung". Distinct from `audit` (which checks compliance with the system's own claims) — this skill challenges the claims themselves with explicit anti-status-quo bias mechanism. Triggered before building atop existing infrastructure, when foundations look soft, or as a periodic deep-review during pre-launch / pre-distribution windows where radical rewrites are still cheap.
version: 0.4.0
license: MIT
mcp_tools_required: []
mcp_tools_optional: [list_skills]
fallback_when_mcp_absent: "skill is filesystem-only; dispatches general-purpose subagents that read files directly. list_skills is convenience for skill enumeration but agents glob plugin/skills/*/SKILL.md if absent."
summary: First-principles soundness review with anti-status-quo bias (greenfield reframe). Challenges the design itself, not its compliance.
routing_mode: direct
triggers:
  - {phrase: "design review", lang: en}
  - {phrase: "is this design right", lang: en}
  - {phrase: "first-principles review", lang: en}
  - {phrase: "would we build this from scratch", lang: en}
  - {phrase: "rough cut review", lang: en}
  - {phrase: "Designprüfung", lang: de}
  - {phrase: "Grundüberprüfung", lang: de}
handoffs: []
phase_role: meta
---

# design-review

First-principles review of system soundness. Where `audit` checks
compliance ("does X match what X claims to be?"), `design-review`
challenges the claim itself ("is X's claim about itself the right
shape?").

The anti-bias mechanism is **greenfield reframe** — every subsystem
under review is examined with the prompt "if we were starting
today, what would we build?" Findings are grounded against that
hypothetical, not against the existing form's incumbent advantage.

> **Stage assumption.** This skill's anti-status-quo bias mechanism
> assumes a pre-launch / pre-distribution context where radical
> rewrites are cost-cheap (no users to break, no production data
> to migrate). When the system ships to first user-facing release,
> this assumption shifts and the bias-explicit briefs should be
> updated to weight cost-of-change higher. **Revisit at first
> production deployment.**

## Load this now

Read the three reference files (in this order):

1. `references/anti-bias-mechanism.md` — the greenfield reframe,
   bias-explicit briefs to subagents, the 5-category refinement
   framing, the manufactured-restraint pattern to watch for.
2. `references/scope-and-targets.md` — load-bearing first-run
   targets (meta-rules, entity types, decision rules, orchestrator,
   skill contract, office-config schema), focused-mode scoping,
   out-of-scope-finding handling.
3. `references/output-conventions.md` — subsystem verdict types,
   recommendation buckets, greenfield-grounding requirement,
   cross-cutting recommendations section, artifact lifecycle.

PROCEDURE.md walks the multi-checkpoint logic.

## When invoked

Two modes:

- **Full first-principles review** (default for "design review",
  "is this design right", "would we build this from scratch") —
  reviews load-bearing foundations. Dispatches one subagent per
  subsystem in parallel.
- **Focused subsystem review** (for "design review the chunkers",
  "is the orthogonality refactor sound", etc.) — single-subsystem
  dispatch; no foundation-set fan-out.

There's **no verification mode** like audit has. Design-review
output is recommendations (claims about what should change),
not findings to fix; verification doesn't apply the same way.
After recommendations are acted on, a follow-up design-review run
on the same subsystem assesses the new shape.

Trigger detection:

| Phrase | Mode |
|---|---|
| "design review", "first-principles review", "would we build this from scratch", "rough cut review" | full |
| "design review X" / "is X the right shape" / "soundness of X" | focused on X |
| "review the architecture" | full (architecture is one of the load-bearing foundations) |

If unclear, ask the user: "full first-principles review (load-bearing foundations) or focused on a specific subsystem?"

## Behavior

Follow `PROCEDURE.md`. At a glance:

1. **Scope decision** — pick subsystem(s) per
   `references/scope-and-targets.md`.
2. **Dispatch subagents in parallel** — one per subsystem. Each
   brief includes the bias-explicit prompts from
   `references/anti-bias-mechanism.md` and requires greenfield
   reframe as a private reasoning step before findings.
3. **Synthesize** — consolidate per-subsystem verdicts +
   recommendations + cross-cutting reshape candidates.
4. **Self-refinement pass** — apply 5-category framework (drop
   bloat / add missing / reshape wrong-shape / surface anchoring /
   reverse manufactured criticism) on the recommendations
   themselves. One pass mandatory; stop if pass found no Pareto
   improvements.
5. **Commit positions** on user-decision items (per memory:
   commit to positions, don't present menus).
6. **Present to user** — frozen artifact at
   `docs/design-reviews/<scope>-<YYYYMMDD>.md`. User decides which
   recommendations to act on.

## Output

Frozen artifact at `docs/design-reviews/<scope>-<YYYYMMDD>.md` per
`references/output-conventions.md`:

- Title + date + trigger reason + scope (which subsystems
  reviewed)
- Per-subsystem section with **verdict** (Refined /
  Rough-but-adequate / Rough-and-worth-refining / Wrong-shape) +
  recommendations grouped by **bucket** (Keep / Refactor /
  Reshape) with greenfield grounding + what-it-unlocks +
  what-breaks + cost (S/M/L)
- **Cross-cutting recommendations** section for systemic reshapes
  spanning multiple subsystems
- Closure tracking via HANDOFF + commit history (artifact stays
  frozen)

The user is the cross-check in interactive mode; their pushback
catches manufactured criticism + manufactured restraint that
self-refinement misses. The skill's recommendations should be
sturdy enough to survive that pushback. Manufactured restraint
(unjustified deferrals) and manufactured criticism (over-cautious
flagging) are both anti-patterns; PROCEDURE Checkpoint 4 (self-
refinement) explicitly addresses both.

## Edge cases

- **Subsystem looks identical to greenfield**: verdict is
  "Refined." No recommendations. This is a positive outcome,
  not a failure.
- **Subsystem requires a Reshape that ripples across other
  subsystems**: the reshape lives in the **Cross-cutting**
  section, not in any one subsystem's section.
- **Subagent's greenfield reframe is shallow / doesn't engage with
  the existing system**: discard, re-dispatch with a tightened
  brief (specifically: cite specific files + ask "name 3 ways a
  from-scratch design would look different and why").
- **Recommendations conflict with each other**: surface the
  conflict to user; don't try to resolve in synthesis.
- **User pushback on a specific recommendation**: revise / revert
  per `references/anti-bias-mechanism.md` 5-category framework.
  Both directions valid (drop or keep based on cost-specific
  reasoning, not generic principles).

## Tools used

- `Agent` (built-in) — dispatch per-subsystem subagents in
  parallel.
- `Glob`, `Grep`, `Read` — direct filesystem reads when synthesis
  needs to verify a subagent's claim.
- `Edit`, `Write` — produce the frozen artifact.
- `list_skills` (MCP, optional) — quick skill inventory; agents
  fall back to filesystem glob if MCP absent.
