# Profiles — usage profiles for framework validation

**Status: PRELIMINARY** — baseline, not rigid. If practice surfaces gaps not covered, surface as candidate profile addition. Profiles evolve.

## What this is

Persistent grounding for who-and-what the framework serves. Profiles span lifecycle stages × shape variations × archetypes. Used pre-validation (proposing primitive classifications) + post-validation (auditing locked corpus for gaps).

Without persisted profiles, the framework risks drift toward whoever AI implicitly imagines the user is at moment-of-decision — and that imagination is single-axis and idealized. Profiles ground the AI's validation in concrete, varied, persisted use cases.

## Why "profiles" not "user profiles"

The framework has multiple **usage layers** with different concerns:
- People who BUILD the framework (us)
- People who BUILD ON the framework (specialist creators, shape definers, template composers)
- People who DEPLOY framework outputs (workspace deployers; multi-tenant administrators)
- People who USE deployed workspaces (practitioners; multi-user collaborators)
- People who EVALUATE framework outputs (auditors; regulators; reviewers)
- People who CURATE framework ecosystem (shape catalog maintainers)
- People who CONSUME packaged framework artifacts (consulting clients; marketplace participants if marketplace materializes; internal-firm-reuse beneficiaries)

Single "user" framing collapses these into one. Multiple "usage profiles" preserves the distinction.

## How to use profiles

**Pre-validation (proposing primitive classifications)**:
- Run multi-axis validation against profiles: archetype × work-type × role
- For each relevant profile, ask: does this primitive serve this profile's reality?
- Force non-coverage question: what use cases does primitive NOT cover, and is that intentional or a gap?

**Post-validation (auditing locked corpus)**:
- Periodically validate already-locked corpus against profiles
- Surface gaps where locked primitives don't serve specific profiles cleanly
- Composability check: can artifacts produced at this profile's level be cleanly packaged for downstream consumption?

**As taxonomic framing**: profiles surface the participants vs context distinction; surface the multi-shape support requirement; surface the composability concern across packaging levels.

## Taxonomy

### Validation gate (fires FIRST)

| Role | Description | Profile |
|---|---|---|
| **G** | **Composability Gate (package consumer perspective)** — cross-cutting validation gate; fires FIRST when designing any L1-L4 producer artifact. Validates against multi-mode consumption (consulting / internal-firm-reuse / OSS / marketplace-future / backup-migration). If G fails, reshape design. If G passes, proceed to multi-axis validation across producer profiles. | [G-composability-gate.md](G-composability-gate.md) |

**Why a gate, not a stage**: G is not a sequential lifecycle stage (L1-L9 cover those). It's the initial composability check that fires before any producer-side design proceeds. Lifecycle order is L1-L4-produce → consumers-consume; validation order puts G first — design with the end (consumption) in mind.

### Lifecycle stages — framework participants (L0-L10)

People/roles who actively engage with framework artifacts:

| Stage | Description | Profile coverage |
|---|---|---|
| L0 | Framework developer (us, building the framework) | Not profiled (we don't validate framework against ourselves writing it) |
| L1 | Specialist creator | [L1-specialist-creator.md](L1-specialist-creator.md) |
| L2 | Shape definer | [L2-shape-definer.md](L2-shape-definer.md) |
| L3 | Deployment template creator (composes specialists + shape into ready-to-deploy templates; "AI Planungsbüro ready-to-deploy" example) | [L3-deployment-template-creator.md](L3-deployment-template-creator.md) |
| L4 | Workspace deployer (deploys specific instance from template; customizes for practitioner / team) | [L4a-workspace-deployer-solo.md](L4a-workspace-deployer-solo.md), [L4b-workspace-deployer-firm-it.md](L4b-workspace-deployer-firm-it.md) |
| L5 | Practitioner-user (day-to-day workspace use; codified workflow + ad-hoc + capability extensions) | 10 profiles (see below) |
| L6 | Multi-user collaborator (within shared workspace; governance + visibility + authority) | Folded into L4b + L5 profiles where applicable |
| L7 | Workflow designer (crystallizes ad-hoc patterns into codified workflow definitions) | Wearing-a-hat scenario; covered as moments within L1 + L5 profiles |
| L8 | Auditor / reviewer (post-hoc engagement; defensibility tests; regulatory challenge) | [L8-auditor-reviewer-posthoc.md](L8-auditor-reviewer-posthoc.md) |
| L9 | Shape catalog curator (maintains shape variants — DACH-planning vs UK-planning, etc.) | [L9-shape-catalog-curator.md](L9-shape-catalog-curator.md) |
| L10 | Cross-deployment learner (studies multiple deployments to derive new patterns) | Skipped — too speculative; requires multiple deployments existing first |

### Lifecycle stages — framework context (L11-L12)

External entities / forces shaping framework requirements without direct artifact engagement:

| Stage | Description | Profile coverage |
|---|---|---|
| L11 | Sponsor / steward (funds framework; shapes priorities) | Framing only in this INDEX; no separate profile |
| L12 | Regulatory / external (regulators, peer reviewers, opposing counsel — shape defensibility requirements) | Framing only in this INDEX; defensibility primitive captures their effect on framework decisions |

### Cross-cutting validation: G grounds the consumer side

G (above; validation gate; fires first) grounds the consumer side. L1-L4 each have a "Packaging boundary" section validating from producer side. Two-sided coverage of composability concerns.

### Shape variations — orthogonal to lifecycle

| Shape | Description | Coverage in L5 profiles |
|---|---|---|
| **practitioner-shape** | Workspace serves practitioner-author producing accountability-bearing output (PBS marketed positioning) | L5a planner, L5b lawyer, L5c researcher, L5d auditor, L5g medical, L5h architect/engineer, L5i junior, L5j multi-jurisdictional |
| **autonomous-business-shape** | Workspace operates as autonomous business / business-running-itself | L5e autonomous-business-operator |
| **personal-OS-shape** | Workspace as personal knowledge / information / task manager (lighter framework usage) | L5f personal-OS-knowledge-worker |

Other shapes (federation, hybrid, etc.) per VISION shape catalog — covered as needed.

### Archetypes — within practitioner-shape

| Archetype | Profile |
|---|---|
| Planner (B-Plan-Begründung; PBS-Schulz pioneer) | L5a |
| Lawyer (small practice; legal briefs) | L5b |
| Researcher (manuscripts; lab) | L5c |
| Auditor (engagement; regulatory) | L5d |
| Medical practitioner (clinical case; private practice) | L5g |
| Architect / engineer (technical specification; multi-disciplinary firm) | L5h |
| Junior practitioner under senior review (hierarchical authority) | L5i |
| Multi-jurisdictional consultant (cross-jurisdiction regulatory) | L5j |

## Profile catalog

| ID | Profile | Shape | Status |
|---|---|---|---|
| **G** | **Composability Gate — package consumer perspective** (initial gate; fires first) | n/a (cross-cutting validation) | **FULL DETAIL** |
| L1 | Specialist creator | n/a (creator stage) | Skeleton (full content TBD) |
| L2 | Shape definer | n/a (creator stage) | Skeleton (full content TBD) |
| L3 | Deployment template creator | n/a (creator stage) | Skeleton (full content TBD) |
| L4a | Workspace deployer — solo self-deploy | varies | Skeleton (full content TBD) |
| L4b | Workspace deployer — IT admin at firm | varies | Skeleton (full content TBD) |
| **L5a** | **Solo planner — PBS-Schulz pioneer** | practitioner-shape | **FULL DETAIL** (anchor profile) |
| L5b | Solo lawyer — small practice | practitioner-shape | Skeleton (full content TBD) |
| L5c | Researcher in lab | practitioner-shape | Skeleton (full content TBD) |
| L5d | Auditor at firm | practitioner-shape | Skeleton (full content TBD) |
| L5e | Autonomous-business operator | autonomous-business-shape | Skeleton (full content TBD) |
| L5f | Personal-OS knowledge worker | personal-OS-shape | Skeleton (full content TBD) |
| L5g | Medical practitioner — solo private practice | practitioner-shape | Skeleton (full content TBD) |
| L5h | Architect / engineer — small multi-disciplinary firm | practitioner-shape | Skeleton (full content TBD) |
| L5i | Junior practitioner under senior review | practitioner-shape | Skeleton (full content TBD) |
| L5j | Multi-jurisdictional consultant | practitioner-shape | Skeleton (full content TBD) |
| L8 | Auditor / reviewer — post-hoc defensibility test | n/a (evaluator stage) | Skeleton (full content TBD) |
| L9 | Shape catalog curator | n/a (ecosystem stage) | Skeleton (full content TBD) |

## Validation discipline (two-step order)

Profiles ground a two-step validation discipline that fires for any architectural decision affecting L1-L4 producer artifacts:

### Step 1: G — Composability Gate (fires FIRST)

Before producer-side design proceeds, validate against G consumer profile:
- Does this design support consulting deliverable distribution?
- Does it support internal firm reuse?
- Does it support OSS / community distribution?
- Does it support marketplace distribution (future-conditional)?
- Does it support backup / migration / cloning?

If G fails for any consumption mode, reshape the design. Don't proceed to multi-axis validation until G is satisfied. Wrong shapes can't pass — composability is structural, not advisory.

### Step 2: Multi-axis validation across producer profiles (per `feedback_multi_axis_validation.md`)

After G passes, validate primitive classifications across three orthogonal dimensions:
- **Archetype**: planner / lawyer / researcher / auditor / etc.
- **Work-type within archetype**: codified workflow / ad-hoc exploratory / one-off communication / research-mode / maintenance / learning
- **Role**: practitioner / workflow-designer / specialist-author / instance-deployer / AI-runtime / multi-user-collaborator

Plus explicit non-coverage question: what use cases does primitive NOT cover; intentional or gap?

### Two-sided coverage

- **G profile** grounds consumer side (single cross-cutting profile)
- **L1-L4 profiles** each have "Packaging boundary" section grounding producer side
- Both must pass for design to proceed

### Why G first

"Design with the end in mind." If consumption-side concerns aren't gated at the start, producer-side design can produce non-composable artifacts that require expensive rework. G-first makes composability structural rather than advisory. Per `feedback_wrong_shapes_impossible.md`: prefer structural constraints that make wrong shapes impossible.

## Persistence + evolution

**Status discipline**: profiles are PRELIMINARY (parallel to `learnings/` status discipline). Concrete grounding but not architectural lock — profiles evolve as practice surfaces gaps.

**When to add new profile**: practice reveals use case not covered by existing profiles + gap is load-bearing for architectural validation. Surface as candidate; discuss; add.

**When to update existing profile**: practice contradicts profile claims + contradiction is load-bearing. Update with evidence; preserve "what changed" via git history (not in-profile breadcrumbs per provenance hygiene).

**When to retire profile**: profile no longer reflects framework scope OR profile redundant with combined coverage from other profiles. Move to `archive/profiles/` with retirement note.

## Reading order at session start

Profiles are not all loaded at session start. Reading order:
1. INDEX.md (this file) — taxonomy + catalog (lightweight; orient AI to available profiles)
2. Specific profile loaded on-demand when relevant decision / audit / composability check requires it

For substantive PBS work involving primitive classification or composability concerns: load relevant profiles before sharpening / coherence-audit invocations.

## Cross-references

- `feedback_multi_axis_validation.md` (the discipline profiles ground)
- `feedback_foundation_up_ordering.md` (ordering principle complementary to profile validation)
- `MAINTENANCE.md` (profiles added to Layer-0 anchors)
- `HANDOFF.md` (session log captures profile creation + evolution)
- `BACKLOG.md` (composability tooling Phase 5+ entry; references profiles for grounding)
- `drafts/composability-tooling.md` (early draft of tooling that would enforce packaging boundaries)
