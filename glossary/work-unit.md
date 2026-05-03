---
entry: work-unit
class: PRIMITIVE
layer: multi-aspect
axis: cross-axis
vision_usage: implicit
---

# work-unit

- **Class**: PRIMITIVE (atomic; the deployment-bound work-artifact unit) — **bipartite multi-aspect Pattern B** (KIND DEFINITION in specialist's distributable bundle; INSTANCE-CONTENT at Owner B as work-unit instance entity). Always-present container: every piece of accountability-bearing work IS a work-unit (no optional-overlay discount; cf. workflow's optional applicability).
- **Layer**: multi-aspect — KIND DEFINITION aspect inherits Framework C placement via specialist's bundle (specialists DEFINE work-unit kinds; not standalone Framework C entries); INSTANCE aspect at Owner B (work-unit instance entity per workspace per active kind)
- **Axis**: cross-axis (work-units are the artifact-containers all axes operate against — axis-1 intertwined work happens IN work-units; axis-2 sparring fires DURING work-unit progression; axis-3 authorship attaches TO work-units)
- **VISION usage**: implicit (VISION's "interactive practitioner workflows" line 7 produces work-products; work-unit is the deployment-bound container for those products; not directly named in VISION)

**Vocabulary disambiguation**:
- **`work-unit`** — the primitive (the abstraction; bipartite Pattern B)
- **`work-unit kind`** — the DEFINITION aspect (specialist-defined kind discriminator + per-kind structural conventions in specialist's bundle)
- **`work-unit instance`** — the INSTANCE aspect (specific deployment-bound artifact-container; entity-md per Owner B convention)

When unambiguous from context, just "work-unit" works. When ambiguous, qualify.

**Canonical**: The deployment-bound work-artifact container — a single bounded unit of accountability-bearing work that one or more workflows progress against. The primitive is bipartite: a `work-unit kind` is the specialist-defined discriminator + structural conventions (e.g., `project` for planning bureau, `matter` for legal practice, `case` for medical practice, `engagement` for consulting, `manuscript` for research lab, `audit` for accounting); a `work-unit instance` is a specific deployment-bound artifact-container at Owner B. Always-present: every piece of accountability-bearing work IS a work-unit (regardless of workflow primitive engagement).

**What it is**: The artifact-shaped container for "one piece of accountability-bearing work the practitioner will sign and defend." Work-unit kinds are pattern-level concepts in specialist DEFINITIONs: a planning-document-work specialist declares `project` kind with its lifecycle states, artifact attachment shape, and audit-trail attribution semantics; a legal-litigation specialist declares `matter` kind with different conventions. When a practitioner begins accountability-bearing work, a work-unit instance is created against an active kind — it carries lifecycle state (initiated → in-progress → completed / sent / archived), associated artifacts (drafts, references, sent versions), decisions made, sources cited, sparring outcomes, and audit-trail attribution (events emitted scoped to this instance). Workflow_instances execute AGAINST work-unit instances when codified pattern applies (one workflow_instance progresses one work-unit through stages; or multiple workflow_instances in sequence or parallel against one work-unit).

**Always-present container** (reciprocal to workflow's optional applicability): work-unit is always present when accountability-bearing work happens. Workflow_instance is the OPTIONAL structural overlay that ATTACHES to a work-unit when a codified pattern applies; ad-hoc work-units have no workflow_instance but still exist as work-unit instances (carried by session + skill firings + claim emissions + events). The work-unit is the always-present anchor; workflow_instance is opt-in via codified pattern existence. This asymmetry is load-bearing: ad-hoc work is first-class supported via the always-present work-unit primitive without forcing workflow primitive engagement.

**Cardinality + lifecycle**:

**work-unit kind** cardinality: N kinds per specialist (each specialist DEFINITION declares the kinds it supports). Per workspace = sum across active specialists.
**work-unit kind** lifecycle: immutable per specialist version (specialist version bump may include kind amendments); distributed via specialist's Framework C placement.

**work-unit instance** cardinality: N per workspace per active kind (instances created per piece of accountability-bearing work; multiple concurrent typical for practitioner-shape).
**work-unit instance** lifecycle: created with snapshot of kind's structural conventions at creation (preserves audit-trail integrity if specialist version bumps mid-instance-lifetime; mirrors workflow_instance definition-snapshot pattern); transitions through lifecycle states (initiated → in-progress → completed / sent / archived); kind is FIXED at creation (no kind-switching mid-lifecycle; pivot creates new work-unit); mutable-with-audit (state transitions, artifact accumulation, claim revisions all audited); persists across sessions; retains for audit per workspace's audit-retention policy.

**Multi-practitioner authorship**: practitioner-shape pioneer = 1 practitioner per work-unit; multi-practitioner work-units (federation-shape, multi-user practitioner-shape variants) are shape-policy variation per ARCH 3.5 work-unit-mechanics; signing/attribution semantics per shape policy.

**Orphan instances**: when owning specialist deactivated (workspace `specialists_active` change), existing work-unit instances of that kind become orphan-state — preserved per specialist persistence rule (deactivating specialist preserves accumulated content); reactivation restores progression capability; no auto-archive.

**What it is NOT**:
- Not a `workflow` — workflow is the PATTERN (sequence of activities + artifacts + decisions); work-unit is the artifact-container the work produces against. Workflow_instance is optional overlay; work-unit is always-present anchor.
- Not a `session` — sessions are bounded interactions; work-units span many sessions over time
- Not a `specialist` — specialists DEFINE work-unit kinds (DEFINITION aspect in specialist's bundle); work-unit is one of several primitives composed into specialist's DEFINITION
- Not a `workspace` — workspace contains many work-unit instances; workspace is the deployment container, work-unit is one bounded artifact-instance within it
- Not the produced output — produced output (Begründung PDF, signed brief, submitted manuscript) is an artifact OF a work-unit instance; the work-unit is the bounded-work-container that holds the artifact + its history + decisions
- Not optional — every accountability-bearing piece of work IS a work-unit (always-present; no opt-out path)

**Cross-archetype illustration** (kind names per archived corpus + cross-archetype examples):
- **Practitioner-shape (PBS-Schulz pioneer)**: `project` kind (e.g., "25-03 Maxsolar - Friedrichshof" tracking one B-Plan project from intake through approval)
- **Legal practice**: `matter` kind (one engagement: client + opposing party + filings + case state)
- **Medical practice**: `case` kind (one patient encounter or treatment trajectory)
- **Consulting**: `engagement` kind (one project: scope + deliverables + billing)
- **Research lab**: `manuscript` kind (one paper from drafting through submission and revision)
- **Accounting / auditor**: `audit` kind (one audit engagement: scope + fieldwork + findings + report)
- **Autonomous-business-shape**: `task` or `order` kind (operator-supervised AI work batch; ephemeral but always-present per work-unit)
- **Personal-OS-shape**: `task` or `goal` kind
- **Federation-shape**: cross-node `peering` work-units possible

The KIND is specialist-defined; the kind enum lives in specialist DEFINITION at Framework C. Workspace's active specialists determine which kinds are available in that deployment. Specialist-namespace disambiguation: when multiple specialists offer same-named kind (e.g., `legal-litigation:matter` vs `legal-advisory:matter`), workspace resolves at work-unit creation via active-specialist set + creator's specialist context (ARCH 3.5 schema-detail).

**Boundary test**: Three questions:
1. Is this the DEPLOYMENT-BOUND artifact-instance one piece of work tracks? → it's a `work-unit instance`
2. Is this the PATTERN of how work proceeds? → it's a `workflow definition`
3. Is this the DEFINITION of which work-unit kinds exist for a competence area? → it's a `work-unit kind` inside a `specialist` DEFINITION (at Framework C)

**Composes with**:
- [specialist](specialist.md) — specialists DEFINE work-unit kinds at the DEFINITION aspect (kind discriminator + per-kind structural conventions in specialist's bundle); workspace's active specialists determine which kinds are available. Work-unit kind names scoped under specialist-namespace = specialist-name (per `glossary/specialist.md` composes-with work-unit row); fully-qualified kind reference is `specialist-name:kind-name` (e.g., `legal-research:matter` distinct from `planning-document-work:project`).
- [workflow](workflow.md) — workflow_instance executes AGAINST work-unit instance when codified pattern applies. Cardinality asymmetry: workflow_instance has 1 work-unit attribution; work-unit has N workflow_instances attached (potentially across specialists — e.g., legal `matter` progressed by litigation-specialist's filing workflow + accounting-specialist's billing workflow). Ad-hoc work-units have no workflow_instance attribution — produced by session + skill + claim + event without workflow primitive. Work-unit is always-present anchor; workflow_instance is optional overlay.
- [workspace](workspace.md) — workspace CONTAINS work-unit instances as workspace-scope managed instances at Owner B; cardinality multiple per workspace per active kind
- [Owner B scope](owner-b-scope.md) — work-unit instances live there as workspace-scope managed entities (per `Owner B scope` members list)
- [event](event.md) — work-unit instance lifecycle emits events (work_unit_created, state_transitioned, work_unit_completed, work_unit_sent, work_unit_archived); audit-emission mechanism captures these; events scoped to work-unit per archived audit-trail-v2 schema
- [actor](actor.md) — actors emit events against work-unit instances (practitioner authorizing send; AI runtime drafting; external client responding)
- [practitioner](practitioner.md) — practitioners are the human authors signing work-unit instance outputs; defensibility test asks "will the practitioner be able to defend THIS work-unit's outputs?"; multi-practitioner authorship = shape-policy variation
- [claim](claim.md) — claims compose into work-unit instance output content; one work-unit instance contains N claims; work-unit is the artifact-container, claim is the atomic content-unit within
- [authority-binding](authority-binding.md) — work-unit lifecycle transitions emit events bound to authority-decision actor (practitioner-shape send/archive = practitioner-only per defensibility-critical; autonomous-business-shape transitions = operator-attestation programmatic); per-shape policy declares which transitions require which authority via authority-binding mechanism
- [mechanism](mechanism.md) — composes with persistent-state (work-unit instance state across sessions); audit-emission (lifecycle events); authority-binding (lifecycle transitions may require specific authority — practitioner-shape send/archive = practitioner-only per defensibility-critical; autonomous-business-shape transitions = operator-attestation programmatic)
- [quality-gate](quality-gate.md) — work-unit instance lifecycle events + per-claim emissions feed quality-gate's drift detection (e.g., rapid sign-off cadence without sparring → axis-3 rubber-stamping signal at attestation moment); work-unit is observability source

**Source**:
- Locked GLOSSARY entries: [Owner B scope](owner-b-scope.md) ("work-unit instances (kind specialist-defined: `project` for planning bureau; `matter` for legal practice; `case` for medical practice; `engagement` for consulting; `manuscript` for research; `audit` for accounting)"); [workspace](workspace.md) (cross-archetype examples reference per-archetype work patterns); [specialist](specialist.md) (DEFINITION includes work-unit kinds); [workflow](workflow.md) (workflow_instance attaches to work-unit instance)
- Synthesis: bipartite Pattern B classification parallel to workflow + specialist; always-present anchor (no optional-overlay discount); reciprocal to workflow's optional applicability
- Archived corpus for kind discriminator detail (Phase 3.5 ARCH territory): `entity-md-scope-model-restructure.md` (Owner B placement); per-specialist DEFINITION files in archived `plugin/skills/` (e.g., planning-document-work specialist's `project` kind)

**See**:
- [Owner B scope](owner-b-scope.md) (where work-unit instances live)
- [workflow](workflow.md) (optional overlay attaching to work-unit instance)
- [specialist](specialist.md) (which defines kinds at DEFINITION aspect)
- [workspace](workspace.md) (which contains work-unit instances)
- [claim](claim.md) (atomic content-unit within work-unit instance output)
- [quality-gate](quality-gate.md) (Pattern A runtime protocol consuming work-unit observability)
- `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster ARCH topic; two-Pattern-B topic-template-class anchor; bipartite Pattern B always-present container — work-unit KIND DEFINITION at Framework C via specialist's bundle + work-unit instance at Owner B; work-unit instance 5-state default lifecycle per kind (`initiated` → `in-progress` → `completed` | `sent` | `archived`) with per-kind extensible state machine; kind FIXED at creation gate-enforced; kind-snapshot pattern at creation; cross-specialist work-unit attachment PERMITTED + ownership mutation PROHIBITED per cross-specialist composition rules; orphan-instance handling on specialist deactivation; per-shape policy variation matrix; authority-binding composition for lifecycle transitions; W1-W4 watch-list including per-kind structural conventions schema standardization + work-unit instance pivot mechanics implementation)
