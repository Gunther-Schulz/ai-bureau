# Decision record: MCP-unreachable fallback policy

**Status**: ACCEPTED (session 7, 2026-04-29)
**Owner**: ARCHITECTURE meta-rule 4 corollary; per-skill `fallback_when_mcp_absent` field

## Context

Session 6 promoted state.md to a typed-contract durable artifact:
`ProjectState` Pydantic model + cross-reference invariants + forward
migrations enforced on read/write through `get_project_state` /
`update_project_state` MCP tools. The session also committed
"strict-validation discipline" — captured as ARCHITECTURE meta-rule 4
corollary and `feedback_llm_instruction_tightness.md`: **no bad
defaults or fallbacks, clean clear failures only**.

Across the 19 skills, however, `fallback_when_mcp_absent` strings
typically describe degradation paths like:

> "warn user; degrade to filesystem Read of extensions/.../doctypes.yaml"
> "fall back to direct Read of office-config.yaml"
> "skill still functions — most of its work is reading state.md"

These fallbacks **bypass the contract that justified putting the file
behind a gate in the first place**. A skill that "falls back to
filesystem Read of state.md" gets potentially:

- Stale (pre-migration) frontmatter the loader would have updated
- Partial-invalid state the Pydantic model would have rejected
- Cross-reference-broken state (lifecycle ↔ phase mismatch) the
  invariant check would have caught
- Whatever raw YAML the file happens to contain — including data
  written by a buggy prior session that wouldn't survive validation

The strict-validation principle says this is exactly the failure
mode we don't want. Silent contract bypass is worse than no fallback:
it produces work output the system claims is correct.

## Decision

**Contract-bearing reads have no fallback path. MCP-unreachable for
any contract-bearing artifact surfaces to user as a clean failure.**

Two file classes, two policies:

| Class | Examples | If MCP unreachable |
|---|---|---|
| **Contract-bearing** | state.md, office-config.yaml, doctype manifests (`extensions/.../doctypes.yaml`), reference manifests (`extensions/.../references-manifest.yaml`), baustein YAML (`memory/bausteine/.../*.md`), projects-index.md | **Fail closed.** Surface to user: "MCP unreachable; cannot operate on \<X\>. Restart backend." Skill stops. |
| **Contract-free prose** | HANDOFF.md, decisions.md, file-map.md, correspondence-log.md, module-decisions.md, README.md, prose memory under `memory/universal/{style,conventions,verfahren,...}/`, top-level docs (VISION/ARCHITECTURE/ROADMAP) | Direct Read fine. No gate exists for these; nothing to bypass. |

**The test for contract-bearing**: does the file have any of —
- A Pydantic model that validates its shape
- A `schema_version` field with migrations applied on read
- Cross-reference invariants (validity depends on other files'
  state)
- A loader function in `pbs_mcp/` that constructs a typed object
- A `last_updated` / `last_fetched` / `checksum_sha256` field
  declaring an invalidation contract

If yes → contract-bearing → fail closed. If no → prose → direct
Read fine.

## Rationale

1. **Strict-validation was the point.** Session 6 spent significant
   effort moving state.md behind Pydantic. Allowing direct-Read
   fallback to coexist makes the gate optional, not enforced —
   defeating the purpose.

2. **Failure mode honesty.** A loud "MCP unreachable; restart
   backend" is a fixable problem with a clear next action. A silent
   degradation that returns half-validated data is a hidden problem
   that surfaces as "why did the bureau just commit to a wrong
   lifecycle?" three sessions later.

3. **MCP availability is binary in practice.** The MCP server is
   spawned per-session by Claude Code via stdio. If it's down, the
   whole system has a deeper issue — the skill bypassing the
   contract isn't the right resolution path.

4. **Mirrors meta-rule 4's existing discipline.** The rule already
   says "skills compose deterministic gates, never re-implement."
   Falling back to direct Read *is* re-implementing the gate's
   read-side (poorly — without validation/migrations/invariants).
   Fail-closed is the consistent extension.

5. **Contract-free prose stays free.** The rule applies only where
   contracts exist. Skills can still Read HANDOFF, decisions.md, and
   memory prose without MCP — those have no contract to bypass. The
   policy doesn't make skills more brittle in the prose layer.

## Implementation plan

1. **Slice 14 brief extension**: scan every skill's
   `fallback_when_mcp_absent` string. Flag any pattern of
   "fall back to filesystem Read of \<contract-bearing file\>".
   Brief receives the contract-bearing file list above.

2. **Plugin-wide sweep** (session 7): rewrite all 19 skills'
   `fallback_when_mcp_absent` strings under the new rule. For
   contract-bearing dependencies, the field becomes "without
   \<tool\>: skill cannot operate on \<contract-bearing X\>;
   surface to user 'MCP unreachable; restart backend' and stop."
   For contract-free dependencies, "direct Read of \<file\>"
   remains valid.

3. **ARCHITECTURE.md meta-rule 4 corollary**: append the rule to
   meta-rule 4's body. New section:
   *"Fail-closed for contract-bearing reads: when MCP is
   unreachable, skills MUST surface and stop, not bypass the
   contract via direct filesystem Read. The gate is the only
   correctness path; bypass produces silent invalid output."*

4. **plugin/CLAUDE.md**: add a one-line summary of the rule under
   the meta-rule 4 summary.

5. **Audit slice 14**: now also catches *declared* future violations
   (in fallback strings), not only live violations (in skill body).

## Alternatives considered

**A. Allow direct-Read fallback as "best-effort degraded mode"** —
rejected. Conflicts with session-6 strict-validation commitment;
produces silent invalid output that's worse than loud failure.

**B. Cache last-known-valid state in skill memory** — rejected.
Adds caching layer with its own invalidation problem; doesn't
respect cross-reference invariants that depend on other files;
solves the wrong problem (MCP availability is the issue, not
cache locality).

**C. Per-skill opt-in to the fail-closed rule** — rejected.
Architecturally inconsistent — would create two classes of skills
with different correctness guarantees. The whole point of meta-rule
4 is uniform discipline.

## Revisit triggers

- A real production scenario where MCP unavailability blocks a
  user's urgent work AND there's a contract-bearing read involved.
  The user can still work around by manually editing the contract-
  bearing file (with care) — the policy doesn't lock the file, just
  removes the silent-bypass affordance from skills.
- Fail-closed surfacing produces user friction that wasn't
  anticipated (e.g. transient MCP hiccups become hard stops where
  graceful degrade would have completed the work).
- A new contract-bearing artifact emerges where the test-criteria
  list above doesn't cleanly classify it — revisit the test.

## Files touched

- `ARCHITECTURE.md` — meta-rule 4 corollary
- `plugin/CLAUDE.md` — meta-rule 4 summary update
- `plugin/skills/*/SKILL.md` — all 19 `fallback_when_mcp_absent`
  fields
- `plugin/skills/audit/references/drift-surfaces-and-slices.md` —
  slice 14 brief extension
- `docs/plugin-conventions.md` — fallback policy section
