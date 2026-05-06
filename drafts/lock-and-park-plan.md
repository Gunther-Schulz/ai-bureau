# Lock-and-park plan — pivot to concrete-first PBS deployment

> **Status**: DRAFT proposal. Not locked. Reads as a memo for the user to review at their own pace and react to in chunks.
>
> **Why this exists**: Session 35 (2026-05-06) surfaced that the framework as currently designed has cognitive load and architectural-composition gaps that can't be resolved abstractly without ground truth from a real deployment. This plan pivots from "design abstract framework" to "build PBS concretely; let framework patterns emerge or be validated by real evidence."
>
> **What you're being asked to react to**: the plan as a whole, section by section. No large decisions in one go. Each section ends with explicit reaction prompts.

---

## 0. The pivot in one paragraph

The framework's been designed abstractly for months without a concrete deployment to test against. Today's session showed the cost: high cognitive load, multiple unresolved architectural questions, no clear leverage points to fix them. The way through is to STOP designing the framework abstractly and START building one concrete deployment (PBS-Schulz planning office) end-to-end. The framework SURFACES that already exist (substrate / audit / sparring / quality-gate / authority-binding / adapter / specialist) probably stay roughly right; the policy values, shape catalogs, and composition primitives that were locked prematurely will get tested by real PBS work and refactored later when concrete evidence demands. Existing architectural reasoning is preserved intact for future mining — nothing thrown away.

---

## 1. Lock declaration

### What gets locked

The current state of the framework — code (`pbs/`), architecture docs (`arch/`, `ARCHITECTURE.md`), DRs (`docs/decisions/`), glossary, MAINTENANCE.md, VISION.md — is FROZEN as a coherent body of work. Frozen means: not edited unless the edit falls under documented exceptions (see "What's allowed during lock" below).

### Why lock vs refactor

Refactoring requires us to know what to fix; today's session showed we don't, with confidence. Locking preserves the entire body of architectural reasoning intact for future mining once concrete evidence (PBS deployment findings) tells us what's actually load-bearing vs accidental. Cleaner separation, lower cognitive load, no risk of refactoring the wrong things.

### Lock date

The day this plan is approved by the user (TBD; estimated 2026-05-06+).

### What's allowed during lock

Edits to framework code/docs are allowed ONLY for:
- Bug fixes (typos in docs, broken imports in code, mypy/test failures)
- Doc clarifications that don't change architectural commitments
- Capturing new findings from PBS work in the questionable-points doc

NOT allowed during lock:
- New ARCH topic locks
- New Mode 2 reference impl additions
- New Mode 3 spec additions
- Refactoring shape impls
- Decisions about deferred questions (multi-shape composition, hybrid-shape, etc.)

If something feels like it crosses the line, surface it for explicit approval rather than acting.

### Known questionable points (from session 35)

These are surfaced gaps. They're parked, not solved. PBS deployment will tell us which are real vs theoretical.

1. **Single-shape-per-workspace forces wrong fit for multi-archetype organizations.** A planning firm doing client deliverables + business ops + maybe personal workflow currently has to pick one shape; any choice mis-fits the other two.

2. **Specialist `shape_compatibility` is a coarse boot-time check, not runtime policy resolution.** All activated specialists run under workspace.shape's policies regardless of which specialist they came from.

3. **Engagement-target entity catalog conflicts across shapes.** Same real entity (a municipality being Client AND Customer) needs two framework representations if a workspace hosts both shapes.

4. **Hybrid-shape escape hatch is named in glossary but undefined.** No arch topic locks structural mechanics.

5. **Per-shape policy variation matrix in scope-model §8 doesn't have a column for "what if multiple shapes apply".**

6. **Boot sequence assumes single shape.** substrate-phase 5 loads "engagement-target entity per shape policy" (singular).

7. **Specialist instance content boundary unclear when specialist's natural shape ≠ workspace's selected shape.**

8. **Pattern-vs-instance discipline strain on practitioner_shape_*.py impls.** Are they "framework primitive definitions" (must stay shape-neutral) or "shape policy bundles realized as code" (Framework C distributables)? Arguably the latter, but the discipline language doesn't carve this out cleanly.

9. **Non-session-initiated work has no articulated practitioner-binding mechanism.** Per `arch/practitioner.md`, binding is at session-open. Scheduled tasks, AI-proactive monitoring, autonomous workflows that emit events requiring HUMAN actor have no clear binding.

### Other expected shortcomings (surfaced earlier in session)

- CLAUDE.md TOP-LEVEL SCOPE vs MAINTENANCE.md vs glossary contradiction on whether specialist DEFINITIONs and per-shape policy bundles are framework-side or deployment-side. Resolved earlier in session: glossary is canonical (they ARE Framework C distributables); CLAUDE.md was over-restrictive in summary. Worth recording.

- "Shape" as currently locked conflates ~6 dimensions (governance policies + engagement-target catalog + Layer A defaults + specialists activation policy + workspace.md required fields + substrate selection constraints). Conflation may be the deepest leverage point; deferred until PBS evidence demands.

### Deferred questions (parked, not parked permanently)

- How shape composition works (if at all) for multi-archetype organizations
- Whether "shape" as currently defined is one cohesive thing or N orthogonal things glued together
- Whether engagement-target should be its own first-class primitive
- Cross-deployment claim portability mechanics
- Federation primitives
- "Framework-from-scratch builder" skill idea (user-deferred until PBS deployment scope locked; see §6 Forward references)

### Reopen criteria (when do we resume framework work?)

Framework work resumes when ANY of:

- **Trigger A — PBS first-useful-state**: PBS deployment is producing real B-Plan-Begründung successfully (or equivalent first useful work product), AND has been used for ≥4 weeks. Signals concrete patterns are starting to appear.
- **Trigger B — finding count**: ≥5 framework-blocking findings accumulated in PBS-side findings log (definition of "framework-blocking" in §4).
- **Trigger C — explicit user trigger**: user decides framework concerns warrant attention regardless of triggers A/B.
- **Trigger D — second deployment intent**: someone (you or other) starts authoring a second deployment that isn't planning-firm shape. Forces shape-neutrality validation.

Reopen doesn't mean restart. It means a structured review session with PBS evidence in hand, deciding which questionable points to address now and which to keep parked.

### Reaction prompt for §1

Read and react to:
- Is this lock scope right (everything in `pbs/`, `arch/`, `docs/decisions/`, glossary, MAINTENANCE, VISION), or too broad/narrow?
- Are the 9 questionable points the right ones, or am I missing something / overstating something?
- Are the 4 reopen triggers reasonable, or do you want different triggers / threshold values?

---

## 2. Two-track structure

### Track 1: Framework (this repo, `pbs-bureau`)

Stays as-is. Locked per §1. Branch protection optional but recommended (merge gate for any changes).

### Track 2: PBS-deployment (separate repo recommended)

PBS deployment work happens in a separate repo. Recommended name: `pbs-bureau-deployment` (or `pbs-schulz` if you prefer firm-anchored naming).

Why separate repo:
- Clean separation; no risk of accidentally editing framework
- Repo URL clarity for future reference (this is the deployment; that is the framework)
- Different versioning cadence (framework locked; deployment evolves)
- Aligns with `MAINTENANCE.md` TOP-LEVEL SCOPE intent (deployment-instance content lives elsewhere)

Why NOT a subdirectory:
- Subdirectory blurs the separation
- Risk of deployment work creeping into framework files

### Cross-track communication

- PBS-deployment side: per-finding entries logged as `findings/<date>-<short-name>.md`. Format in §4.
- Framework side: aggregator doc (probably extending `LOCKED-STATE.md` or new `findings-from-pbs.md`) lists known PBS findings linked to framework areas they touch. Updated weekly or per-finding.

### Reaction prompt for §2

- New separate repo for PBS deployment, or subdirectory in this repo? I lean separate repo. Confirm or redirect.
- Repo name preference: `pbs-bureau-deployment` (framework-anchored) vs `pbs-schulz` (firm-anchored) vs other?

---

## 3. PBS deployment plan (high level)

This is the actual concrete work. Sequenced in increments small enough that each delivers something runnable.

### Milestone 1 — "Hello PBS"

Minimum viable PBS deployment that exercises the framework Surfaces end-to-end. Goal: prove the framework's substrate / audit / specialist activation / session binding actually compose for a real deployment.

What this includes:
- `workspace.md` declaring: shape (practitioner-shape, with PBS-specific policy values authored locally), substrate (claude_agent_sdk), one specialist active, one practitioner (Gunther Schulz), legal_entity_context (Schulz Planning GmbH)
- ONE specialist DEFINITION authored locally — probably the simplest one PBS needs (e.g., `note-capture` or similar), not the full `planning-document-work` yet
- Practitioner-shape policy bundle authored as DEPLOYMENT content (extracted from `pbs/impls/practitioner_shape_*.py` reference impls; PBS owns the values, framework just provides the impl shells)
- One trivial workflow that exercises: substrate boots → specialist activates → skill fires → emits event → audit records → workflow_instance state transitions → cleanly shuts down
- Manually-tested end-to-end (not full test suite yet)

What this does NOT include:
- Real B-Plan-Begründung work (that's milestone 2+)
- Layer A content beyond minimal placeholder
- Multi-specialist composition
- Real adapter wirings (email/MCP/etc. — stubs are fine)

### Milestone 2 — "PBS does one real thing"

Minimal real-work capability. Goal: PBS produces a real B-Plan-Begründung section (one section, one client work-unit).

What this adds:
- `planning-document-work` specialist with ≥3 skills (e.g., `draft-section`, `verify-citations`, `attest-claim`)
- Sparring + quality-gate + authority-binding actually firing on real work
- Practitioner attestation flow (HUMAN actor required for claim_attested) tested with real Gunther interaction
- One real client engagement-target entity (Client A)
- Layer A content: one real baustein, one real reference (the actual law cited)

What this does NOT include:
- Multi-client management
- Invoice generation
- Personal workflow

### Milestone 3 — "PBS does its day"

Full daily-use PBS. Goal: PBS deployment is what Gunther actually uses for planning work, end of every day.

What this adds:
- Multiple specialists composed (planning-document-work + project-management + maybe invoicing)
- Real adapter wirings (email, MCP corpus)
- Multiple clients
- Layer A content built out for real domains/states (planning + naturschutz + DE-BB)
- Workflow_instance state persistence across sessions

### Milestone 4 — "PBS is the deployment of record"

PBS replaces whatever Gunther currently uses for planning work. Daily ground-truth signal generator.

### Beyond milestone 4

Not planned in detail. Likely surfaces "this needs framework changes" — at which point reopen criteria fire (§1) and we go back to framework work with concrete evidence.

### What stays NOT in scope for any milestone

- Autonomous-business shape work (deferred per session 35; no second shape until first deployment is solid)
- Personal-OS workflow (defer; possibly second workspace later)
- Federation / multi-tenant / multi-environment
- LanceDB / fastembed / RAG-stack production infrastructure (Phase 6.2 territory in old plan; defer)

### Reaction prompt for §3

- Does this milestone sequence match how you'd naturally build PBS, or does it sequence wrong?
- Is "Hello PBS" minimal enough, or still too ambitious for first step?
- Anything missing from milestones 2-4 that PBS actually needs early?

---

## 4. Findings log structure

Every PBS finding that touches framework gets logged. Even if we don't act on it (we won't, during lock). The log IS the evidence pool that reopen criteria fire against.

### Where findings live

- **Primary**: `findings/` directory in PBS-deployment repo, one file per finding
- **Aggregator**: `findings-from-pbs.md` in this repo (framework side), pointing to PBS-side files

### Per-finding format

```yaml
---
date: 2026-MM-DD
short_name: <kebab-case>
framework_area: <e.g., shape, specialist, workspace, adapter, audit>
severity: blocking | workaround-acceptable | annoyance | observation
related_questionable_point: <reference to §1 lock declaration questionable point #N if applicable>
---

## Finding

<plain-language description of what surfaced during PBS deployment>

## Why it touches framework

<which framework area + why current architecture doesn't handle this cleanly>

## Current workaround

<what we did in PBS-deployment to ship around it; or "no workaround possible — blocking">

## Reopen-trigger relevance

<does this contribute to a reopen trigger? which one?>
```

### Severity definitions

- **blocking**: PBS deployment cannot proceed without framework change. Auto-trigger reopen consideration.
- **workaround-acceptable**: PBS works around it; framework gap noted for later.
- **annoyance**: minor friction; framework gap noted; low priority.
- **observation**: pattern observed; not yet a gap; might become one.

### Reaction prompt for §4

- Format reasonable, or want different fields?
- Severity scale right, or merge/split categories?

---

## 5. Reopen criteria (detail of §1)

### Triggers (recap from §1)

- A: PBS first-useful-state + 4 weeks of use
- B: ≥5 framework-blocking findings accumulated
- C: explicit user trigger
- D: second deployment intent

### What "reopen" looks like

NOT: scrap PBS work and rebuild framework.

YES:
- Structured review session with PBS evidence in hand
- For each questionable point in §1 + each accumulated finding: ask "is there enough evidence to decide now?"
- Some get decided (with concrete patterns from PBS as ground truth)
- Some get re-parked (still not enough evidence)
- Whatever gets decided gets implemented as targeted framework amendments
- PBS keeps running; framework changes ripple to PBS in controlled cadence

### Cadence guess

If PBS development goes well, first reopen probably 3-6 months after lock. Could be sooner if blocking findings accumulate fast. Could be longer if PBS just works without framework friction.

### Reaction prompt for §5

- Trigger thresholds reasonable, or want them tighter/looser?
- Does the "reopen looks like" description match what you'd want, or is reopen actually more dramatic (e.g., scrap and redesign)?

---

## 6. Forward references (deferred ideas captured so they don't get lost)

### "Framework-from-scratch builder skill" (user idea, session 35)

User concept (paraphrased): a skill that builds a framework fully realized + abstract per the original VISION, from scratch. Possibly composable with the `clippy` skill set (don't look at clippy until ready).

Status: deferred until PBS deployment scope is locked down. Revisit after milestone 3-4.

Why this might matter: if PBS deployment surfaces that the current framework's primitive set is fundamentally mis-shaped, a from-scratch derivation might be a cleaner path forward than incremental refactoring. Or it might inform what the "right" framework looks like vs what we have.

Captured here to ensure it surfaces during the next planning conversation post-PBS-milestone-3.

### Other deferred items

- Bildhauer step 3-8 (catalog / classify / leverage / step-back / recommend) — deferred; the conditions assumed by those steps don't hold under lock-and-park
- Shape decomposition analysis — deferred until concrete PBS evidence
- Multi-archetype composition mechanics — deferred until second deployment shows actual need

### Reaction prompt for §6

- Forward-reference capture sufficient, or want each forward reference to have its own doc/issue?

---

## 7. Execution sequence (what I do once you confirm)

In order, on the `lock-and-park` branch (this branch). Each step ends with commit + push so progress is visible.

### Step 1 — Lock declaration

Write `LOCKED-STATE.md` at top level of this repo. Content:
- Lock declaration + date + scope (§1 of this plan)
- Known questionable points (§1)
- Deferred questions (§1)
- Reopen criteria (§1 + §5)
- Cross-link to this plan doc

### Step 2 — Findings log scaffolding

Create:
- `findings-from-pbs.md` at top level (aggregator stub)
- Template for per-finding files (instructions for PBS-deployment side to use)

### Step 3 — Update HANDOFF.md

Note 82-equivalent capturing: lock-and-park pivot decision, new branch, plan document, sequence forward.

### Step 4 — Update BACKLOG.md

Mark current Phase 6.1 in-scope items as parked. Add new item: "PBS-deployment work in separate repo per lock-and-park plan." Forward-reference the plan.

### Step 5 — Set up PBS-deployment repo

Create new repo (per §2 confirmation). Initial scaffold: README + workspace.md skeleton + findings/ directory + cross-link back to framework repo's locked state.

### Step 6 — Commit lock-and-park branch + open PR (or merge to step-back-evaluation, your call)

After steps 1-5 complete, push branch, open PR for review (or merge directly if you prefer). Lock takes effect on merge.

### Step 7 — First PBS deployment work session

Begin Milestone 1 ("Hello PBS"). Authored in the new deployment repo. First session likely scopes the workspace.md + minimal specialist DEFINITION + practitioner-shape policy values extracted from current `pbs/impls/practitioner_shape_*.py`.

### Reaction prompt for §7

- Sequence reasonable, or want different ordering?
- Step 6: PR for review or direct merge? (I lean PR for the audit trail; your call.)
- Step 7 should be a separate session after lock is merged, or right after step 6?

---

## 8. What success looks like 3 months from now

If this works: PBS is doing real planning work daily. Framework is unchanged from lock state. Findings log has 10-30 entries. Reopen review surfaces which framework changes have concrete evidence vs which questionable points are theoretical only. Targeted amendments land based on evidence.

If this doesn't work: PBS gets blocked too often by framework gaps. Findings log explodes. Either reopen comes earlier than planned (trigger B fires fast) or PBS deployment effort itself reveals the framework needs more fundamental rework (trigger to consider the "from-scratch builder" idea from §6).

Either outcome is useful. Both are better than continuing to design abstractly without ground truth.

---

## 9. Open questions for you to react to (consolidated)

Sections that need your reaction before execution:

1. (§1) Lock scope, questionable points, reopen triggers — all reasonable?
2. (§2) Separate repo for PBS deployment? Repo name preference?
3. (§3) Milestone sequence right?
4. (§4) Findings log format right?
5. (§5) Reopen trigger thresholds reasonable?
6. (§6) Forward-reference capture sufficient?
7. (§7) Execution sequence right?

You can react section by section over multiple turns. No need to answer all at once.

---

## End of plan

Once you've confirmed (or redirected) the sections that need confirmation, I execute steps 1-6 from §7. Step 7 (first PBS work session) is a separate engagement after lock is in effect.

If anything in this plan feels wrong, surface it. The plan itself is draft; revising it before execution is cheap.
