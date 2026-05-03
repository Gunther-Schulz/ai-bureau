# Decision record: Workflow + work-unit ARCH topic (Phase 3.5 third primitive-cluster)

## 1. Status

**ACCEPTED** (session 29, 2026-05-03). 2-round decision-design-sharpening (Round 1 full monty + Round 2 user-triggered). Mode 2 upfront-known composite decomposition per `decision-design-sharpening` v0.10.0 §Two decomposition modes — 6 sub-decisions tightly coupled; single composite DR (sub-decisions have no independent meaning outside the composite).

Sharpening rounds metadata:
- Round 1 (full monty): 6 sub-decisions inventoried + sharpened with foundation-up dependency ordering (sub-decision-batched: 4 + 5 + 3 + 4 + 3 + 6 = 25 EXPANSIONS)
- Round 2 (user-triggered): cross-cutting + schema-detail refinements (R-CC-1 through R-CC-11 = 11 EXPANSIONS)
- STABLE-AT-ROUND-2 verdict per `decision-design-sharpening` §Lock + persist signals (Q3 DECAY CONFIRMED ~56%; Q5 specific termination signal named below; Q4 no unaddressed pass)
- LOCK-HARD target-type per skill §Step 4 target-type modifier (architectural decision; cascades hard if revised)

## 2. Owner

Phase 3.5 — third primitive-cluster ARCH topic. Anchors **two-Pattern-B topic-template-class** (parallel to `arch/substrate.md` anchoring Pattern A 12+7 template + `arch/specialist-skill.md` anchoring primitive-cluster Pattern B + atomic-primitive 12+5 template + `arch/practitioner.md` anchoring Pattern C topic-template-class). Two-Pattern-B-specific conditional applicability rules surface here per per-pattern conditional applicability rules in `MAINTENANCE.md` Layer 3 Primitive-cluster topic template (granularity / per-primitive lifecycle ordering likely apply; bundle / marketplace likely N/A — workflow + work-unit are bundled IN specialist, not bundlers themselves). Cited as precedent for downstream Phase 3.5 primitive-cluster topics where two-Pattern-B class conditional applicability surfaces.

## 3. Related

**Composes with**:
- `arch/substrate.md` Surface §C (permission flow integrates with workflow_instance phase transitions + work-unit instance lifecycle transitions for authority-binding moments per R-CC-4) + §F (session/context management persists workflow_instance + work-unit instance state across sessions per R-CC-5) + §10 (boot/shutdown ordering integration per ARCHITECTURE.md §6 composite subsection per R-CC-1) + §8 (dual-emission paths apply when workflow_instance + work-unit instance lifecycle events flow through both substrate-internal AND skill-side emission)
- `arch/audit.md` Surface §A (emission API + actor declaration for §SD-4 event-kind catalog per R-CC-6) + §C (query API for cross-workflow_instance + cross-work-unit-instance audit-trail defensibility test per R-CC-7) + §14 (cross-shape policy variation per R-CC-2 audit emission granularity composes with work-unit attribution) + §15 W5 federated audit-trail watch (composes with W2 cross-practitioner workflow handoff)
- `arch/sparring.md` §4 (sparring sub-mechanisms accessed by skills DURING workflow_instance phase progression AND ad-hoc work-unit progression; per-shape activation matrix; per R-CC-3)
- `arch/adapter.md` §2 (per-class Surfaces consumed by skills firing within workflow_instance phases per R-CC-8)
- `arch/specialist-skill.md` §10 (cross-specialist composition rules + bundle composition; workflow + work-unit DEFINITIONs nest within specialist's bundle per cluster boundary; cross-specialist work-unit attachment PERMITTED + ownership mutation PROHIBITED per R-CC-9) + §11 (marketplace + distribution mechanics; workflow + work-unit kind DEFINITIONs distributed THROUGH specialist DEFINITION) + §13 boot step 9 (workflow + work-unit kind DEFINITIONs registered at substrate-phase 4 step 9; cross-pattern destruction archival-as-default coherence) + §3-4 composition tables
- `arch/practitioner.md` §4 R-CC-10 (multi-practitioner concurrent-session handling; workflow_instance.bound_practitioner_id references session-bound practitioner; per R-CC-9) + §8 (cross-shape policy variation matrix shape-policy-mediated multi-practitioner work-unit authorship + workflow_instance flexibility) + §13 (archival-as-default destruction; cross-pattern coherence) + §14 W4 (cross-practitioner workflow handoff mechanics; composes with W2 here)
- `docs/decisions/specialist-skill-arch-topic.md` (primitive-cluster 12+5 template precedent + Mode 2 composite decomposition precedent)
- `docs/decisions/practitioner-arch-topic.md` (Pattern C topic-template-class anchor precedent + Mode 2 composite decomposition precedent + per-shape policy variation matrix precedent + lifecycle event-kind catalog with `details:` payload precedent + cross-pattern destruction archival-as-default precedent)
- `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` (Pattern A / mechanism-class template; primitive-cluster 12+5 derived parallel)
- `docs/decisions/audit-arch-topic.md` (mechanism-class precedent; per-shape trust model parameterization)

**GLOSSARY entries** (locked; cited extensively):
- `workflow` (canonical bipartite Pattern B with optional applicability entry)
- `work-unit` (canonical bipartite Pattern B with always-present container entry)
- `specialist` (containing primitive; workflow + work-unit DEFINITIONs nest within specialist's bundle)
- `skill` (composes-with workflow → skill direction)
- `practitioner` (multi-practitioner authorship per shape; bound_practitioner_id reference)
- `authority-binding` (per-event actor declaration; phase transitions may bind)
- `session` (sessions execute parts of workflow_instance)
- `claim` (work-unit instance contains N claims; forward-reference to claim-defensibility)
- `Owner B scope` (workflow_instance + work-unit instance placement)
- `Framework C scope` (workflow definition + work-unit kind placement via specialist's bundle)

**Forward-references** (future Phase 3.5 + Phase 3.6 topics):
- `arch/claim-defensibility.md` (claims emitted during workflow_instance execution attribute to that workflow_instance per `glossary/workflow.md` composes-with claim row; work-unit instance contains N claims per `glossary/work-unit.md`; per-claim attestation chain composes through workflow_instance + work-unit instance attribution)
- `arch/scope-model.md` (Owner B scope category for workflow_instance + work-unit instance placement; Framework C scope category for workflow definition + work-unit kind placement via specialist's bundle)
- `arch/quality-gate.md` (Pattern A Phase 3.6 — workflow_instance execution + work-unit instance lifecycle events feed quality-gate's drift detection per composes-with quality-gate rows)

**Disciplines applied**:
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (work-unit kind FIXED at creation gate-enforced structural; cross-specialist work-unit WRITES prohibited structural per axis-3)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (workflow + work-unit cluster primitives stay shape-neutral; cross-archetype illustration anchors framework neutrality; pioneer-neutrality)
- `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment workflow_instance + work-unit instance instance-content lives at deployment-instance, not framework repo)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 8 (foundation-up ordering); Discipline 10 (greenfield-evaluation of archived sources)

**Archived sources** (INPUT only per Discipline 10 — greenfield-evaluated against current locked vocabulary; NOT transcribed as template):
- `archive/docs/decisions/entity-md-scope-model-restructure.md` (NAMING SUPERSEDED per archived header — "office-level entities" → "workspace-scope managed entities" per current locked vocabulary; Owner B placement of work-unit instances + per-kind structural conventions concept cited as INPUT for SD-2 work-unit kind manifest schema `artifact_attachment_shape` field but NOT transcribed verbatim — archive uses pre-rebuild scope model; current locked vocabulary uses A-B-C scope model per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; greenfield-derived schema per current Pattern B bipartite + locked GLOSSARY entries)
- `archive/docs/decisions/audit-trail-v2.md` (`details:` payload precedent for `details.changed_fields` + `details.predecessor_work_unit_id` + `details.from_phase`/`to_phase` event-kind shapes cited as INPUT for §SD-4 event-kind catalog but NOT transcribed verbatim — archive uses prior event_kind catalog; current locked vocabulary aligns event-kinds to current GLOSSARY primitives + minimal event-kind catalog growth per `details:` payload pattern; greenfield-derived event-kind catalog per current Pattern B + lifecycle states per locked GLOSSARY)
- `archive/plugin/skills/` (per-specialist DEFINITION files referencing workflow + work-unit kind patterns cited as INPUT for cross-archetype illustration but NOT transcribed verbatim — archive's per-specialist content is pre-rebuild; current locked GLOSSARY cross-archetype examples per `glossary/work-unit.md` adequately cover archetype illustration; greenfield-derived cluster boundary per current Pattern B nesting per `arch/specialist-skill.md` §10)
- `archive/docs/decisions/governance-and-identity-sourcing.md` (decision 3 = per-deployment uniqueness convention preserved as deployment-side commitment per §16; decision 4 = prose-rules pattern for ID minting cited as deployment-level discipline)

## 4. Context

Phase 3.5 third primitive-cluster ARCH topic. Prior to this DR, Phase 3.5 first primitive-cluster topic (specialist-skill) LOCKED at commit `f6bab6e` per `ARCHITECTURE.md` §7 + `docs/decisions/specialist-skill-arch-topic.md`; Phase 3.5 second primitive-cluster topic (practitioner) LOCKED at commit `7ffe93a` per `ARCHITECTURE.md` §7 + `docs/decisions/practitioner-arch-topic.md`; Pattern A protocol topics + mechanism-class topics LOCKED in Phase 3.4 per `ARCHITECTURE.md` §7 (substrate + adapter + sparring + audit).

**Why workflow-work-unit chosen third** (foundation-up per Discipline 8): workflow + work-unit DEFINITIONs nest within specialist's bundle per `arch/specialist-skill.md` §10 (cluster boundary); workflow_instance + work-unit instance attribution composes through practitioner-RECORD per `arch/practitioner.md` §4 R-CC-10 (multi-practitioner concurrent-session handling). Locking workflow-work-unit third after specialist-skill + practitioner means the future Phase 3.5 `arch/claim-defensibility.md` topic locks per-claim attestation chain against an already-validated workflow_instance + work-unit instance attribution surface. Reverse ordering would force claim-defensibility to forward-reference unlocked workflow_instance + work-unit instance primitives.

**Why two-Pattern-B topic-template-class anchored here**: workflow + work-unit are BOTH bipartite Pattern B (per locked GLOSSARY entries: workflow bipartite Pattern B with optional applicability; work-unit bipartite Pattern B with always-present container). The cluster pairs two Pattern B primitives — structurally distinct from Pattern B + atomic-primitive (specialist-skill cluster) + Pattern C bipartite (practitioner cluster) + future PRIMITIVE + DERIVED (claim-defensibility cluster). Two-Pattern-B-specific conditional applicability surfaces here (granularity tests + per-primitive lifecycle ordering APPLY per shape-policy-mediated multi-practitioner authorship + workflow_instance state-machine + work-unit kind state-machine; bundle / marketplace N/A per workflow + work-unit are bundled IN specialist, not bundlers themselves). Future two-Pattern-B primitive-cluster topics inherit this DR's anchor for conditional applicability rules.

**What the decision-design phase needed to resolve**:
- Two-Pattern-B topic-template-class confirmation (12+5 extends without variation; per-pattern conditional applicability rules)
- Per-primitive structural overview (4 sub-aspects: workflow DEFINITION + workflow_instance + work-unit KIND DEFINITION + work-unit instance; manifest schemas)
- Cross-primitive composition WITHIN cluster (always-present asymmetry + cardinality asymmetry + ad-hoc work first-class + snapshot pattern + cross-specialist composition)
- Per-primitive lifecycle ordering (workflow_instance state machine + work-unit instance state machine + cross-pattern destruction + orphan handling + boot integration)
- Granularity tests (workflow definition 3-test + work-unit kind 3-test + composition with specialist 3-test + two-tier classification N/A)
- Cross-shape policy variation + cross-axis composition + W1-W4 watch-list

## 5. Decision

Six sub-decisions per Mode 2 composite decomposition (sub-decisions have no independent meaning outside the composite; foundation-up dependency ordering applied within the composite).

### SD-1: Two-Pattern-B topic-template-class confirmation

**Decision**: 12+5 primitive-cluster template extends to two-Pattern-B clusters **without variation**. **Two-Pattern-B topic-template-class anchored at this topic** (parallel to substrate Pattern A 12+7 anchor + specialist-skill primitive-cluster Pattern B + atomic-primitive 12+5 anchor + practitioner Pattern C 12+5 anchor).

**Two-Pattern-B-specific conditional applicability** (per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template per-pattern conditional applicability rules):
- §8 Cross-shape policy variation: APPLIES (per-shape multi-practitioner work-unit authorship + workflow_instance flexibility + work-unit lifecycle policy shape-policy-mediated)
- §9 Granularity tests: APPLIES (workflow definition + work-unit kind have granularity discriminators per locked GLOSSARY boundary tests)
- §10 Bundle composition: N/A (workflow + work-unit are bundled IN specialist per `arch/specialist-skill.md` §10; they are NOT bundlers)
- §11 Marketplace + distribution mechanics: N/A (distributed THROUGH specialist DEFINITION per `arch/specialist-skill.md` §11; not independently distributable)
- §12: N/A-parity (preserved per locked template convention)
- §13 Per-primitive lifecycle ordering: APPLIES (2 state machines + cross-pattern destruction + orphan handling + boot integration)

**Why N/A documented explicitly**: per `MAINTENANCE.md` Layer 3 template "document N/A explicitly when section is omitted" rule. DO NOT skip section numbering — keep §10/§11/§12 as N/A sections preserving template-anchoring stability for downstream two-Pattern-B primitive-cluster topics.

**Total expected**: 18 sections (12 common + 3 conditional applies (§8 + §9 + §13) + 2 N/A documented (§10 + §11) + §12 N/A-parity).

### SD-2: Per-primitive structural overview (4 sub-sections + 4 manifest schemas)

**Decision**: §2 = 4 sub-sections covering bipartite-pair structural articulation:
- **§2.1 Workflow DEFINITION** (Framework C; in specialist's bundle): bipartite Pattern B with optional applicability per `glossary/workflow.md`
- **§2.2 workflow_instance** (Owner B; OPTIONAL overlay): engages only when codified pattern applies
- **§2.3 Work-unit KIND DEFINITION** (Framework C; in specialist's bundle): bipartite Pattern B always-present container per `glossary/work-unit.md`
- **§2.4 work-unit instance** (Owner B; ALWAYS-PRESENT container): every accountability-bearing work IS a work-unit

**Workflow DEFINITION manifest schema** (architectural-level enumeration; Phase 6 lands Pydantic shape):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | str | required | Workflow name local to specialist; specialist-namespace per Note 56 R-N-1 |
| `version` | semver | required | Inherits specialist version |
| `phases` | list (ordered) | required | Phase identifiers in sequence |
| `phase_authority_requirements` | object | optional | Per-phase authority binding |
| `triggered_skills` | object | optional | Per-phase skill triggers |
| `optional_overlay_marker` | bool | default true | Always-true at framework level; documented for clarity |

**workflow_instance schema**:

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | str | required | workflow_instance identifier |
| `definition_snapshot` | object | required | Snapshot of workflow definition at workflow-start (preserves defensibility) |
| `definition_ref` | str | required | Fully-qualified `specialist-name:workflow-name@version` |
| `current_phase` | enum | required | References definition `phases` list |
| `lifecycle_state` | enum | required | `running` \| `suspended` \| `completed` \| `abandoned` \| `failed` (per R-CC-1 naming alignment) |
| `attached_work_unit_id` | str | required | work-unit instance attribution (cardinality asymmetry: 1 work-unit per workflow_instance) |
| `bound_practitioner_id` | str | required | practitioner-RECORD attribution per `arch/practitioner.md` §4 R-CC-10 |
| `phase_history` | list | optional | Phase transitions with timestamps + actor + audit event references |

**Work-unit KIND DEFINITION manifest schema**:

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | str | required | Kind discriminator; specialist-namespace per Note 56 R-N-1 |
| `version` | semver | required | Inherits specialist version |
| `lifecycle_states` | list | required | Kind-specific state machine; default: `initiated → in-progress → completed | sent | archived` |
| `artifact_attachment_shape` | object | optional | Per-kind structural conventions (archived `entity-md-scope-model-restructure.md` greenfield-evaluated INPUT) |
| `audit_attribution_semantics` | object | optional | Per-kind event scoping rules |

**work-unit instance schema**:

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | str | required | Per-deployment uniqueness convention |
| `kind_snapshot` | object | required | CREATION snapshot per `glossary/work-unit.md` lifecycle |
| `kind_ref` | str | required | Fully-qualified `specialist-name:kind-name@version` |
| `lifecycle_state` | enum | required | References kind `lifecycle_states` enum; FIXED kind at creation |
| `attached_workflow_instances` | list | optional | N workflow_instances per cardinality asymmetry |
| `owning_specialist_id` | str | required | Per `glossary/work-unit.md` composes-with specialist row |
| `attribution` | object | required | practitioner-RECORD authorship per `glossary/work-unit.md` composes-with practitioner row |

### SD-3: Cross-primitive composition WITHIN cluster

**Decision**: §3 articulates THREE load-bearing structural commitments + snapshot pattern + cross-specialist composition mechanics.

1. **Always-present asymmetry** (load-bearing per `glossary/work-unit.md` always-present + `glossary/workflow.md` optional applicability): work-unit ALWAYS-PRESENT container vs workflow_instance OPTIONAL overlay; every accountability-bearing work IS a work-unit; workflow_instance = structural overlay attached when codified pattern applies. NOT cosmetic — load-bearing.

2. **Cardinality asymmetry**: 1 work-unit per workflow_instance / N workflow_instances per work-unit (potentially across specialists per `glossary/work-unit.md`). Reciprocal but asymmetric.

3. **Ad-hoc work first-class via session + skill + claim + event** (NOT via workflow primitive engagement): when work-unit has no workflow_instance attached, work proceeds via session(s) + skill firings + claim emissions + audit events alone. Anchored in `profiles/L5a-planner-pbs-schulz.md` lines 60-73 hybrid moments.

4. **Snapshot pattern as cross-primitive structural commitment** (per R-CC-10 REVISION-flavored EXPANSION): workflow_instance `definition_snapshot` + work-unit instance `kind_snapshot` both use snapshot-at-creation for defensibility-preservation across specialist version bumps. Cross-primitive pattern; structural elevation of implicit pattern to explicit (parallels `arch/practitioner.md` R-CC-1 boot ordering elevation).

**Cross-specialist composition** (within cluster but cross-specialist mechanics per `arch/specialist-skill.md` §10):
- Cross-specialist work-unit ATTACHMENT: PERMITTED (workflow_instance from specialist-A attaches to work-unit from specialist-B)
- Cross-specialist work-unit READS: PERMITTED (per `arch/specialist-skill.md` §10 cross-specialist entity reads permitted)
- Cross-specialist work-unit WRITES (ownership mutation): PROHIBITED per `arch/specialist-skill.md` §10 cross-specialist composition rules

### SD-4: Per-primitive lifecycle ordering (§13)

**Decision**: TWO state machines + cross-pattern destruction coherence + orphan handling + boot integration.

**workflow_instance state machine** (per `glossary/workflow.md` lifecycle):
- States: `running | suspended | completed | abandoned | failed`
- Transitions: `running ↔ suspended`; `running → completed | abandoned | failed`; **`suspended → completed | abandoned | failed`** (per R-CC-3; non-terminal states transition to terminal)
- Event-kind catalog (architectural enumeration; Phase 6 Pydantic):
  - `workflow_started` — workflow_instance created with definition snapshot
  - `workflow_phase_transitioned` — phase change with `details.from_phase/to_phase` per archived `audit-trail-v2.md` `details:` payload precedent
  - `workflow_suspended`
  - `workflow_resumed`
  - `workflow_completed`
  - `workflow_abandoned`
  - `workflow_failed`

**work-unit instance state machine** (per `glossary/work-unit.md` lifecycle):
- States (kind-default): `initiated | in-progress | completed | sent | archived`
- Per-kind extensible via `kind.lifecycle_states` field per SD-2 schema (e.g., `audit` kind may add `under-review` state)
- Transitions: kind-specific; default: `initiated → in-progress → (completed | sent) → archived`
- Event-kind catalog:
  - `work_unit_created`
  - `work_unit_state_transitioned` (with `details.from_state/to_state`)
  - `work_unit_completed`
  - `work_unit_sent`
  - `work_unit_archived`
  - `work_unit_pivoted` (per R-CC-4; `details.predecessor_work_unit_id`; kind-FIXED-at-creation enforcement; pivot creates new work-unit linked via predecessor_id)

**Cross-pattern destruction coherence** (per `arch/specialist-skill.md` §13 + `arch/practitioner.md` §13): archival-as-default on workspace dissolution per `workspace.md` `instance_content_dissolution_policy: archive | delete-with-audit` (same field per cross-pattern coherence convention).

**Orphan-instance handling** (per `glossary/work-unit.md` line 39): owning specialist deactivated → work-unit instances of that kind become orphan-state; PRESERVED per specialist persistence rule + cross-pattern coherence with `arch/specialist-skill.md` §5 INSTANCE-CONTENT preservation; reactivation restores progression; NO auto-archive. Same applies to attached workflow_instances of orphaned work-units — workflow_instance state preserved; resumes when specialist reactivated. (`WorkflowInstanceOrphanReactivationFailure` if version-incompatible per §7.)

**Boot integration** (per `ARCHITECTURE.md` §6 composite boot subsection + `arch/specialist-skill.md` §13 boot step 9): workflow + work-unit kind DEFINITIONs registered at substrate-phase 4 step 9 (already covered by specialist-skill); workflow_instance + work-unit instance entity hydration follows from Owner B INSTANCE-CONTENT load.

### SD-5: Granularity tests (§9)

**Decision**: §9 contains TWO 3-tests (per-primitive granularity discriminators differ).

**Workflow definition granularity 3-test** (when considering "should this be ONE workflow OR split / should ad-hoc be codified"):
1. **Phase-boundary clarity** — clearly separable phases? Phases blurry/blending → ad-hoc instead of codification.
2. **Reusability across work-units** — applies to ≥3 work-unit instances? Single-use → ad-hoc better.
3. **Specialist-coherence** — belongs to ONE specialist's competence area? Cross-specialist workflows = mis-bundled.

**Work-unit kind granularity 3-test** (when considering "should this be ONE kind OR split"):
1. **Boundedness** — bounded artifact-container with single accountability scope? (`general-work` = unbounded mis-shape.)
2. **Archetype-discriminator** — specialized for ONE archetype's domain OR cross-archetype generic? Both well-shaped at appropriate shape.
3. **Lifecycle-distinctiveness** — distinct lifecycle-states OR artifact-attachment shapes warrant separate kind vs reuse existing?

**Composition with specialist 3-test**: workflow + work-unit kind 3-tests are SUBORDINATE to `arch/specialist-skill.md` §9 specialist 3-test (specialist 3-test asks "should THIS specialist exist"; workflow + work-unit kind tests ask "should THIS workflow / kind exist within validated specialist"). Foundation-up: specialist granularity validates first.

**Two-tier classification N/A**: workflow + work-unit kinds INHERIT containing specialist's `tier: domain-anchored | cross-archetype` per `arch/specialist-skill.md` §9. Per-primitive tier classification for workflow + work-unit kinds adds vocabulary surface without genuine discrimination — REJECTED via Round 1 ST3.

### SD-6: Cross-shape policy variation + cross-axis composition + W1-W4 watch-list

**Decision**: §8 cross-shape policy variation + cross-axis composition table in §4 + §7 error categories + W1-W4 watch-list.

**§8 Shape-uniform** (NOT shape-policy-mediated):
- Bipartite Pattern B partition for both workflow + work-unit
- Workflow definition + work-unit kind manifest schemas
- Always-present asymmetry
- Cardinality asymmetry
- Snapshot pattern
- Specialist-namespace mechanics

**§8 Shape-policy-mediated**:

| Dimension | practitioner-shape | autonomous-business-shape | personal-OS-shape |
|---|---|---|---|
| Multi-practitioner authorship of work-unit | Solo=1; partnership/firm=N per `arch/practitioner.md` §3 | N/A (no human-practitioner) | 1 user typically |
| work-unit lifecycle policy | Defensibility-critical preservation | Archival OR delete-with-audit per business policy | Minimal lifecycle |
| workflow_instance state-machine flexibility | Strict (rollback prohibited per defensibility) | Tolerant (auto-rollback per business retry policy) | Tolerant |
| work-unit kind required | Per shape policy may mandate | Per business policy | Optional |
| Authority-binding on workflow phase transition | Per workflow definition `phase_authority_requirements` | Programmatic per business + budget policy | Optional |
| Audit emission granularity per work-unit (composes with `arch/audit.md` §14) | Claim-level mandatory | Action-level | Light |

**Cross-axis composition** (in §4 composition table):
- **axis-1 PRIMARY anchor**: workflow per `glossary/workflow.md` (axis-1 — workflow is what intertwined AI intertwines WITH)
- **axis-1 cross-axis**: work-unit container axis-1 work happens IN
- **axis-2**: sparring fires DURING workflow_instance phase progression AND ad-hoc work-unit progression; orthogonal to workflow primitive engagement
- **axis-3**: work-unit instance is artifact-container authorship attaches TO; defensibility test resolves at work-unit + claim granularity

**§14 Watch-list** (4 items):
- **W1**: Workflow_pattern primitive vs Layer A reusable templates — Awaited signal: ≥2 specialists develop genuinely-cross-archetype workflow pattern that Layer A growth proves insufficient for. Resolution: examine then; primitive remains unwarranted by default per `glossary/workflow.md` See section explicit decision.
- **W2**: Cross-practitioner workflow handoff mechanics — Awaited signal: second multi-practitioner deployment surface (pioneer is solo per L5a). Resolution: `workflow_handoff` event-kind shape + attribution chain preservation rules + per-shape required-handoff-recipient enforcement. Cross-link: `arch/practitioner.md` §14 W4.
- **W3**: Per-kind structural conventions schema standardization — Awaited signal: ≥3 kinds across specialists develop divergent artifact-attachment shapes warranting standardization. Resolution: per-kind structural conventions schema; Phase 6 spec territory.
- **W4**: Multi-workflow_instance phase choreography mechanics — Awaited signal: second workspace deploys multi-workflow_instance against single work-unit pattern. Resolution: per-workflow phase coordination semantics + cross-specialist phase ordering. Cross-link: `arch/specialist-skill.md` §10.

**§7 Pre-implementation operational concerns** (per R-CC-11 error categories enumeration):

| Category | Architectural meaning |
|---|---|
| `WorkflowDefinitionValidation` | Manifest frontmatter fails schema validation |
| `WorkflowInstancePhaseTransitionViolation` | Illegal state transition |
| `WorkflowInstanceAuthorityBindingFailure` | Phase transition requires authority not present per `phase_authority_requirements` |
| `WorkUnitKindValidation` | Manifest schema fail |
| `WorkUnitKindCollision` | Within-specialist kind name collision (cross-specialist disambiguated via specialist-namespace) |
| `WorkUnitInstanceLifecycleStateConflict` | State transition not in kind's `lifecycle_states` enum |
| `WorkUnitInstancePivotViolation` | Attempt to switch kind mid-lifecycle |
| `WorkflowInstanceOrphanReactivationFailure` | Specialist reactivated but workflow_instance state can't resume (version incompatibility) |

## 6. Sharpening provenance

### Round 1 (full monty)

EXPANSIONS surfaced (count: 25 = 4 + 5 + 3 + 4 + 3 + 6 — one EXPANSION-batch per sub-decision; Mode 2 upfront-known composite per `decision-design-sharpening` v0.10.0 §Two decomposition modes "Sub-decision inventory" step):

- **SD-1 EXPANSIONS** (4): two-Pattern-B topic-template-class confirmation; per-pattern conditional applicability rules (§8/§9/§13 APPLY; §10/§11 N/A; §12 N/A-parity); per-topic section count expectation 18; downstream two-Pattern-B precedent
- **SD-2 EXPANSIONS** (5): 4 sub-section structural articulation (workflow DEFINITION + workflow_instance + work-unit KIND DEFINITION + work-unit instance); workflow DEFINITION 6-field manifest schema; workflow_instance 8-field schema; work-unit KIND DEFINITION 5-field schema; work-unit instance 7-field schema
- **SD-3 EXPANSIONS** (3): always-present asymmetry load-bearing articulation; cardinality asymmetry (1:N reciprocal but asymmetric); ad-hoc work first-class via session + skill + claim + event (NOT via workflow primitive engagement)
- **SD-4 EXPANSIONS** (4): workflow_instance state machine (5 states + transitions + 7 event-kinds); work-unit instance state machine (5 default states + per-kind extensible + 6 event-kinds); cross-pattern destruction archival-as-default coherence; orphan-instance handling preserves attached workflow_instances
- **SD-5 EXPANSIONS** (3): workflow definition granularity 3-test; work-unit kind granularity 3-test; composition with specialist 3-test (subordinate hierarchy)
- **SD-6 EXPANSIONS** (6): §8 6-row shape-policy-mediated matrix; cross-axis composition (axis-1 PRIMARY anchor + axis-1 cross-axis + axis-2 + axis-3); §7 8-category error catalog enumeration; W1 workflow_pattern primitive vs Layer A; W2 cross-practitioner workflow handoff; W3 per-kind structural conventions standardization

### Round 2 (user-triggered)

Cross-cutting + schema-detail refinements (per `decision-design-sharpening` §Round 2 layered coverage observation: cross-cutting + schema details emphasized):

**Cross-cutting refinements (R-CC-*)** — 11 items:
- **R-CC-1**: workflow_instance `lifecycle_state` enum naming alignment with work-unit instance `lifecycle_state` + `arch/practitioner.md` §2.2 `lifecycle_state` (cross-primitive coherence)
- **R-CC-2**: per-shape audit emission granularity composes with work-unit attribution per `arch/audit.md` §14 (claim-level / action-level / light); composition table row in §4
- **R-CC-3**: workflow_instance state-machine `suspended → completed | abandoned | failed` transitions explicit (non-terminal state can transition to terminal)
- **R-CC-4**: substrate Surface §C permission flow composition row in §4 composition table (workflow_instance phase transitions + work-unit instance lifecycle transitions request permission)
- **R-CC-5**: substrate Surface §F session/context management composition row in §4 (workflow_instance + work-unit instance state persists across sessions)
- **R-CC-6**: audit Surface §A emission API composition row in §4 (lifecycle events flow through Surface §A per §SD-4 catalog)
- **R-CC-7**: cross-workflow_instance + cross-work-unit-instance audit-trail query pattern via audit Surface §C (defensibility test mechanic)
- **R-CC-8**: adapter invocation by skills firing within workflow_instance phases — composition table row in §4
- **R-CC-9**: cross-specialist activation actor binding back-link to `arch/specialist-skill.md` §5 mid-session re-binding + `arch/practitioner.md` §4 R-CC-10 (workflow_instance.bound_practitioner_id references session-bound practitioner)
- **R-CC-10** (REVISION-flavored): snapshot pattern as cross-primitive structural commitment (workflow_instance `definition_snapshot` + work-unit instance `kind_snapshot`; structural elevation of implicit pattern to explicit; parallels `arch/practitioner.md` R-CC-1 boot ordering elevation)
- **R-CC-11**: §7 error categories enumeration (8 categories: WorkflowDefinitionValidation / WorkflowInstancePhaseTransitionViolation / WorkflowInstanceAuthorityBindingFailure / WorkUnitKindValidation / WorkUnitKindCollision / WorkUnitInstanceLifecycleStateConflict / WorkUnitInstancePivotViolation / WorkflowInstanceOrphanReactivationFailure)

**Round 2 EXPANSIONS count**: 11 substantive findings (R-CC-1 through R-CC-11). Per `decision-design-sharpening` §Empirical density check: Round 1 = 25 EXPANSIONS (sub-decision-batched); Round 2 = 11 EXPANSIONS — drops ~56% (DECAY CONFIRMED region per density-behavior table; ≥50% drop signals STABLE candidate per Q3).

### Manufactured-criticism rejections

Per `decision-design-sharpening` §Manufactured-comfort counter-test + §Pareto calibration: reject refinements that aren't Pareto-improving OR that surface manufactured-criticism territory.

Cumulative count: 6 (3 Round 1 ST + 3 Round 2 ST):

**Round 1 ST rejections** (3):
- **ST1 rejected**: "Should §10 Bundle composition apply weakly because workflow definition's `triggered_skills` field references skills?" — manufactured criticism; `triggered_skills` is REFERENCE composition, not BUNDLE composition (skills are bundled within specialist's `skills/` subdirectory per `arch/specialist-skill.md` §2.3; workflow definition references them by local name); conflating reference with bundle adds template surface without Pareto improvement; §10 N/A per template applicability rule (workflow + work-unit are bundled IN specialist, not bundlers)
- **ST2 rejected**: "Should §11 Marketplace + distribution mechanics apply via transitive distribution (workflow + work-unit kind DEFINITIONs ride along with specialist distribution)?" — manufactured criticism; transitive distribution is NOT independent distribution mechanics (no manifest of own beyond specialist's `capability_declarations` lists per `arch/specialist-skill.md` §2.3); §11 N/A per template applicability rule (not independently distributable); cross-deployment portability is specialist-distribution mechanics per `arch/specialist-skill.md` §11
- **ST3 rejected**: "Should §9 introduce unified 3-test (one 3-test for both workflow + work-unit kind)?" — manufactured criticism; per-primitive granularity discriminators differ (workflow's phase-boundary-clarity + reusability + specialist-coherence vs work-unit kind's boundedness + archetype-discriminator + lifecycle-distinctiveness); unified 3-test loses per-primitive discriminator precision; per `arch/specialist-skill.md` §9 anchored 3-test pattern precedent (specialist + skill have separate 3-tests per primitive)

**Round 2 ST rejections** (3):
- **ST-R2-1 rejected**: "Should workflow_instance schema include `bound_session_ids: list[str]` field tracking sessions that participated?" — manufactured criticism via D Gate (per `decision-design-sharpening` Round 2 D Gate procedure per `profiles/INDEX.md`); mental-modeling-resolves test: session-to-workflow_instance attribution composes through audit-trail event scoping per `arch/audit.md` §C query API + `glossary/session.md` composes-with workflow row; per-instance bound_session_ids field adds schema surface without genuine attribution improvement (audit-trail reconstructs via `actor_kind: ai_runtime` + skill identifier + workflow_instance scoping per authority-binding chain)
- **ST-R2-2 rejected**: "Should work-unit instance schema include explicit `claims: list[claim_id]` field listing contained claims?" — manufactured criticism; claims compose via audit-trail event scoping per `glossary/claim.md` composes-with work-unit row + audit Surface §C query API; per-instance claims list field would duplicate audit-trail query results + create consistency-with-trail concern; full claim mechanics → Phase 3.5 `arch/claim-defensibility.md` topic
- **ST-R2-3 rejected**: "Should snapshot pattern be elevated to its own GLOSSARY entry as a cross-primitive structural fact?" — manufactured criticism evaluated via GLOSSARY back-check (per `MAINTENANCE.md` Bidirectional cascade rule "Schema details / per-impl mechanics / operational procedures / per-shape variations are NOT glossary-grade — they stay in ARCH/DR/spec"); snapshot pattern is schema-detail mechanism present in two primitives' lifecycle, NOT a glossary-grade structural fact deserving its own primitive; lives in ARCH topic §3 cross-primitive composition + per-primitive schemas per §2.2 + §2.4

### GLOSSARY back-check verdict

Per `MAINTENANCE.md` Bidirectional cascade + `decision-design-sharpening` v0.5.0 GLOSSARY back-check at Round 2 termination.

**Verdict**: CLEAN — no retro-fits needed. Five candidates evaluated:

- **Snapshot pattern as cross-primitive structural commitment** evaluated for glossary-grade structural fact: result NOT glossary-grade per Bidirectional cascade rule (schema-detail mechanism present in two primitives' lifecycle); lives in ARCH topic §3 + per-primitive schemas. Per ST-R2-3 above.
- **Always-present asymmetry** evaluated for glossary-grade structural fact: result already-codified in `glossary/work-unit.md` always-present container + `glossary/workflow.md` optional applicability + reciprocal cross-references between the two entries. Current locked GLOSSARY entries adequately capture the asymmetry; no retro-fit needed.
- **Cardinality asymmetry (1 work-unit per workflow_instance / N workflow_instances per work-unit)** evaluated: already-codified in `glossary/work-unit.md` composes-with workflow row ("Cardinality asymmetry: workflow_instance has 1 work-unit attribution; work-unit has N workflow_instances attached") + `glossary/workflow.md` composes-with work-unit row (reciprocal). No retro-fit needed.
- **Ad-hoc work first-class via session + skill + claim + event** evaluated for glossary-grade structural fact: already-codified in `glossary/workflow.md` optional applicability + `glossary/work-unit.md` always-present container + reciprocal asymmetry articulation. Current locked GLOSSARY entries adequately capture the structural commitment; no retro-fit needed.
- **`lifecycle_state` enum naming alignment** evaluated for glossary-grade structural fact: result NOT glossary-grade per Bidirectional cascade rule (schema detail; per-primitive enum naming); lives in ARCH topic §2.2 + §2.4 + §13. Naming alignment is cross-primitive coherence convention, not glossary-grade primitive distinction.

### Profile-anchored validation

Per `decision-design-sharpening` v0.5.0+ profile-anchored validation + `profiles/INDEX.md` cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators).

**3 cluster representatives Read** (≥3 cluster coverage requirement; FULL DETAIL profile content cited NOT cluster letters):

**Cluster A Producers** — `profiles/L1-specialist-creator.md` (workflow + work-unit DEFINITIONs live in specialist's bundle; SKELETON profile fleshed-on-demand for this validation):
- L1 lines 18-29 specialist creator stress-tests (intended-stress-test enumeration): "workflow definition packaging (workflows are specialist-bundled per Phase 3.1 workflow lock)" — validates SD-1 cluster boundary "workflow + work-unit DEFINITIONs nest within specialist's bundle"; specialist self-containment (line 19) + cross-substrate compatibility (line 28) + cross-shape compatibility (line 29) validate SD-2 manifest schema + SD-6 cross-shape policy variation
- L1's specialist creator profile validates that workflow definition + work-unit kind manifests (per SD-2) support shape-mandate-fulfilment claims at per-deployment integration time (cross-specialist composition rules per SD-3)
- Verdict: covered (skeleton profile provides sufficient evidence for two-Pattern-B cluster validation per `profiles/INDEX.md` skeleton-fleshing-on-demand strategy)

**Cluster B Deployers + Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` (pioneer; multi-cluster member):
- L5a lines 22-29 B-Plan workflow phases ("intake → research → draft → review → send → response_handling"): validates SD-2 workflow definition manifest schema `phases` field (ordered list); pioneer evidence anchors workflow definition phases concrete shape
- L5a lines 60-73 hybrid moments ("practitioner is mid-drafting (codified workflow_instance active) → notices unusual parcel feature → ad-hoc research detour (no workflow_instance for that exploration) → returns to drafting (workflow_instance resumes)"): validates SD-3 ad-hoc work first-class commitment + cardinality asymmetry + always-present asymmetry; pioneer evidence anchors workflow's optional-overlay design + work-unit's always-present container
- L5a lines 76-83 active specialists set ("planning-document-work + naturschutz-specialist + legal-interpretation-specialist"): validates SD-1 + SD-3 cross-specialist composition (multiple active specialists in same workspace; cross-specialist work-unit attachment scenarios per `glossary/work-unit.md` "legal `matter` progressed by litigation-specialist's filing workflow + accounting-specialist's billing workflow")
- L5a lines 95-101 multi-user moments evidence (solo workspace + external actors as engagement targets): validates W2 cross-practitioner workflow handoff awaiting second multi-practitioner deployment (pioneer is solo per L5a; W4 cross-link)
- L5a lines 119-129 stress-tests (hybrid work pattern; capacity-building through codification; evolution path ad-hoc → codified): validates per-shape trust model parameterization per SD-6 §8 + workflow's evolution path per `glossary/workflow.md`
- Verdict: covered

**Cluster D Validators** — `profiles/G-composability-gate.md` (cross-cutting validation gate; Cluster D member; transitively-satisfied via specialist's packaging boundary):
- G lines 14-22 multi-mode consumption framing: validates SD-1 12+5 template extension; workflow + work-unit kind DEFINITIONs ride along with specialist distribution channels per SD-1 §11 N/A per `arch/specialist-skill.md` §11 (transitive distribution discrimination)
- G lines 154-157 cross-shape consumption rules: validates SD-6 §8 cross-shape policy variation matrix shape-policy-mediated rows; shape policy declares per-shape multi-practitioner work-unit authorship + workflow_instance flexibility
- G lines 162-184 architectural concerns surfaced: backup-migration round-trip implicates work-unit instance + workflow_instance portability per W3 + W4; workspace serialization + cross-substrate restore preserves work-unit + workflow_instance semantics per §13 archival mechanics
- Verdict: transitively-satisfied via specialist's packaging boundary (G's L1-L4 producer artifact concerns satisfied at specialist DEFINITION level per `arch/specialist-skill.md` §11 + §10; workflow + work-unit kind DEFINITIONs inherit via specialist's packaging boundary)

**Cluster D Validators (gate component)** — D Defer Gate per `profiles/INDEX.md` "D Gate procedure":
- W1 workflow_pattern primitive vs Layer A: external-information test passes (specific signal = ≥2 specialists develop genuinely-cross-archetype workflow pattern that Layer A growth proves insufficient for); effort-asymmetry test passes (mental modeling resolves SHAPED-AS-LAYER-A per `glossary/workflow.md` See section explicit decision; primitive remains unwarranted by default); D Gate satisfied → W1 watch-list with resolution mechanism
- W2 cross-practitioner workflow handoff: external-information test passes (specific signal = second multi-practitioner deployment surface; pioneer is solo per L5a); effort-asymmetry test passes (per-shape handoff mechanics design before second-deployment friction risks wrong-design); D Gate satisfied → W2 watch-list with resolution mechanism
- W3 per-kind structural conventions schema standardization: external-information test passes (specific signal = ≥3 kinds across specialists develop divergent artifact-attachment shapes warranting standardization); effort-asymmetry test passes (per-kind schema standardization before divergence accumulates risks wrong-design); D Gate satisfied → W3 watch-list with resolution mechanism
- W4 multi-workflow_instance phase choreography: external-information test passes (specific signal = second workspace deploys multi-workflow_instance against single work-unit pattern; pioneer L5a documents single-workflow_instance + ad-hoc transitions); effort-asymmetry test passes (per-workflow phase coordination before second-workspace friction risks wrong-design); D Gate satisfied → W4 watch-list with resolution mechanism
- ST-R2-1 bound_session_ids: D Gate FIRED — mental-modeling-resolves test passed (audit-trail reconstructs via authority-binding chain); rejected per manufactured-criticism
- Verdict: D Gate satisfied per genuine awaited evidence (W1 + W2 + W3 + W4) + mental-modeling-resolves rejection (ST-R2-1)

### Mode 2 composite decomposition rationale

Per `decision-design-sharpening` v0.10.0 §Two decomposition modes Mode 2:
- **Trigger satisfied**: 6 sub-decisions visible at framing time (not emergent from drift); foundation-up dependencies identifiable (SD-1 template enables SD-2-6 to inherit shape; SD-2 4-sub-section structure enables SD-3 cross-primitive composition; SD-3 enables SD-4 lifecycle ordering composition; SD-5 granularity tests subordinate to specialist 3-test from `arch/specialist-skill.md` §9; SD-6 cross-shape policy variation + cross-axis composition + W1-W4 layers on top of validated cluster shape)
- **Sub-decision inventory at start**: 6 sub-decisions listed before Round 1 (SD-1 → SD-6); composite decomposition mode declared upfront
- **Foundation-up dependency ordering**: SD-1 (template confirmation) locks first; SD-2 (4-sub-section + 4 manifest schemas) builds on SD-1; SD-3 (cross-primitive composition) builds on SD-2 schemas; SD-4 (lifecycle ordering) builds on SD-2 + SD-3; SD-5 (granularity tests) subordinate to specialist 3-test; SD-6 (cross-shape + cross-axis + watch-list) layers on validated cluster shape
- **Per-sub-decision sharpening**: each got Round 1 + Round 2 sweep within the composite (no per-sub-decision split into separate rounds)
- **Synthesis pass at end**: this DR + ARCH §18 composition table is the cross-sub-decision coherence pass
- **Single composite DR**: chosen per Mode 2 §Single composite DR — sub-decisions have no independent meaning outside the composite; workflow + work-unit cluster is the unit, not 6 independent decisions

### REVISION/EXPANSION classification self-check

Per `decision-design-sharpening` v0.6.0 self-check at Round 2 termination + BACKLOG watch-list "3-tier discriminator codification".

**REVISION-flavored EXPANSIONS surfaced** (load-bearing structural elevations):
- R-CC-10 (snapshot pattern as cross-primitive structural commitment; structural elevation of implicit pattern to explicit per cross-primitive lifecycle pattern; parallels `arch/practitioner.md` R-CC-1 boot ordering elevation pattern) — REVISION-flavored

**Cumulative count for awaited 3-tier signal**: 1 REVISION-flavored EXPANSION in this composite. Combined with `arch/specialist-skill.md` DR's 2 REVISION-flavored EXPANSIONS + `arch/practitioner.md` DR's 1 REVISION-flavored EXPANSION = **4 cumulative cross-DR REVISION-flavored EXPANSIONS** across Phase 3.5 primitive-cluster decisions.

**Trip threshold for cumulative-count signal**: ≥3 trips per BACKLOG watch-list "3-tier REVISION/EXPANSION discriminator codification" entry. **Threshold reached** (4 ≥ 3); **flag for Coherence-audit C2** at Phase 3.5 close to evaluate whether 3-tier codification is now warranted across primitive-cluster topic class. USER pushback / cascade-work-lag signals NOT yet materialized per skill detection mechanisms; continue 2-tier within current composite.

**Pure REVISIONS** (architectural pivots changing existing decisions): 0. R-CC-10 is EXPANSION-with-load-bearing-implications, not pure architectural reversal.

### Termination signal (STABLE-AT-ROUND-2)

Per `decision-design-sharpening` §Round termination signals + §Honest termination test Q1-Q5:

- **Q1 (count)**: Round 1 = 25 EXPANSIONS (sub-decision-batched: 4+5+3+4+3+6); Round 2 = 11 EXPANSIONS (R-CC-1 through R-CC-11)
- **Q2 (decay)**: Round 1 → Round 2 = 25 → 11 (drops ~56%; DECAY CONFIRMED region per density-behavior table; ≥50% drop signals STABLE candidate per Q3)
- **Q3 (density behavior)**: DECAY CONFIRMED per ≥50% drop; Round 2 surfaced cross-cutting + schema-detail refinements (per skill §Layered coverage observation Round 2 emphasis); no Round 3 architectural-pattern-surfacing pending
- **Q4 (specific unaddressed pass)**: NONE — all 4 profile clusters covered (A + B + C + D); G Gate transitively-satisfied via specialist's packaging boundary; D Gate fired (W1 + W2 + W3 + W4 satisfied); cross-cutting + schema details exhausted at decision-design-phase
- **Q5 (specific termination signal)**: NARROW ARCHITECTURAL SURFACE per `decision-design-sharpening` §Empirical sweet-spot pattern (two-Pattern-B cluster narrower than Pattern B + atomic-primitive per fewer applicable conditional sections — 3 APPLY vs specialist-skill's 5; matches `arch/practitioner.md` DR Note 57 termination signal); operational concerns (per-deployment storage convention; cross-practitioner workflow handoff implementation mechanics; per-kind structural conventions schema; multi-workflow_instance phase choreography implementation) belong to Phase 6 pre-implementation per §Phase 1 → Phase 2 transition
- **Lock + persist signal**: STABLE per Q3 DECAY CONFIRMED + Q5 specific termination signal + Q4 no-unaddressed-pass + manufactured-comfort counter-test passed (operational concerns explicitly deferred per §Layered coverage observation Round 4+ DEFER to Phase 2)

## 7. Composition with existing architecture

This decision composes with prior locked architecture:

- **Pattern A protocols** (substrate / adapter; sparring + audit mechanism classes per Phase 3.4 close): workflow + work-unit composes with substrate Surface §C (permission flow integrates with workflow_instance phase transitions + work-unit instance lifecycle transitions for authority-binding moments per R-CC-4) + §F (session/context management persists workflow_instance + work-unit instance state across sessions per R-CC-5); with audit Surface §A skill-side emission (per R-CC-6) + §C query API (per R-CC-7); with adapter §2 per-class Surfaces consumed by skills firing within workflow_instance phases (per R-CC-8); with sparring §4 per-shape activation matrix (per R-CC-3). Workflow + work-unit are NOT Pattern A (no multiple interchangeable implementations of one Surface) — both are bipartite Pattern B per locked GLOSSARY entries.

- **Pattern B specialist-skill primitive cluster** (per `arch/specialist-skill.md` Phase 3.5 first primitive-cluster lock): workflow + work-unit DEFINITIONs nest within specialist's bundle per `arch/specialist-skill.md` §10 (cluster boundary); cross-specialist composition rules apply per `arch/specialist-skill.md` §10 + §3 (cross-specialist work-unit attachment PERMITTED + ownership mutation PROHIBITED per R-CC-9); marketplace + distribution mechanics per `arch/specialist-skill.md` §11 (workflow + work-unit kind DEFINITIONs distributed THROUGH specialist DEFINITION per SD-1 §11 N/A); boot integration per `arch/specialist-skill.md` §13 boot step 9 (workflow + work-unit kind DEFINITIONs registered at substrate-phase 4 step 9).

- **Pattern C practitioner primitive cluster** (per `arch/practitioner.md` Phase 3.5 second primitive-cluster lock): workflow_instance binds to ONE practitioner-record at session-open per `arch/practitioner.md` §4 R-CC-10 (multi-practitioner concurrent-session handling; workflow_instance.bound_practitioner_id references session-bound practitioner per R-CC-9); work-unit instance attribution composes through practitioner-RECORD per `glossary/work-unit.md` composes-with practitioner row + `arch/practitioner.md` §3 + §8 (multi-practitioner-shape variants = shape-policy); cross-practitioner workflow handoff mechanics per W2 composes with `arch/practitioner.md` §14 W4; archival-as-default destruction per cross-pattern coherence with `arch/practitioner.md` §13.

- **authority-binding mechanism** (per `glossary/authority-binding.md` from Phase 3.4 C1 cascade): workflow_instance phase transitions may require specific authority per workflow definition `phase_authority_requirements` (per `glossary/workflow.md` composes-with authority-binding row); work-unit instance lifecycle transitions emit events bound to authority-decision actor per `glossary/work-unit.md` composes-with authority-binding row.

- **`ARCHITECTURE.md` §6 composite boot subsection**: workflow + work-unit kind DEFINITIONs registration ordering integrates within substrate-phase 4 step 9 specialist registration step per `arch/specialist-skill.md` §13 (already covered by specialist-skill boot ordering; workflow + work-unit kind DEFINITIONs ride along with specialist registration).

- **`MAINTENANCE.md` Layer 3 Primitive-cluster topic template** (locked per `arch/specialist-skill.md` DR + `MAINTENANCE.md` Layer 3 §3 Primitive-cluster topic template subsection): two-Pattern-B topic-template-class anchored at this topic per per-pattern conditional applicability rules (granularity / per-primitive lifecycle ordering APPLY for two-Pattern-B clusters; bundle / marketplace N/A — workflow + work-unit are bundled IN specialist, not bundlers themselves; cross-shape policy variation APPLIES). Future two-Pattern-B primitive-cluster topics inherit this DR's anchor for conditional applicability rules.

- **TOP-LEVEL DESIGN PRINCIPLES §1 (structural over conventional)**: work-unit kind FIXED at creation gate-enforced structural (the gate dispatches on it for every state transition emission; pivot creates new work-unit linked via predecessor_id); cross-specialist work-unit WRITES prohibited structural per axis-3 (entity ownership boundary structural per Pattern B nesting per `arch/specialist-skill.md` §10) — both exemplify structural-over-conventional discipline.

- **TOP-LEVEL DESIGN PRINCIPLES §2 (pioneer-neutrality)**: workflow + work-unit cluster primitives stay shape-neutral / archetype-neutral / pioneer-neutral; pioneer (PBS-Schulz) reality grounds the cluster primitives without leaking pioneer specifics (Bauleitplanung / B-Plan-Begründung / UNB / Stellungnahme do NOT appear in primitive definitions; cross-archetype illustration in §2 + §5 + §9 anchors framework neutrality).

## 8. Constraints flowing to downstream commitments

- **Phase 3.5 future primitive-cluster topics** (`arch/claim-defensibility.md` next; cross-cutting integrators last): inherit primitive-cluster 12+5 template per SD-1 + per-pattern conditional applicability pattern (document N/A explicitly per template rule; preserve §12 N/A-parity reservation); two-Pattern-B topic-template-class anchored here serves as precedent for conditional applicability when future two-Pattern-B primitive-cluster topics emerge
- **Phase 3.5 `arch/claim-defensibility.md`** (next primitive-cluster topic; foundation-up dependency on workflow + work-unit): specifically inherits SD-2 workflow_instance + work-unit instance schemas (per-claim attribution chain composes through workflow_instance + work-unit instance attribution per `glossary/workflow.md` + `glossary/work-unit.md` composes-with claim rows); locks per-claim attestation chain mechanics against validated workflow + work-unit cluster
- **Phase 3.5 cross-cutting integrators** (`arch/scope-model.md` + `arch/axis-interactions.md`; LAST per `ARCHITECTURE.md` §5 reading order): scope-model topic locks Owner B scope category for workflow_instance + work-unit instance placement + Framework C scope category for workflow definition + work-unit kind placement via specialist's bundle; axis-interactions topic locks workflow as axis-1 PRIMARY anchor + cross-axis composition table per SD-6
- **Phase 3.6 `arch/quality-gate.md`**: consumes workflow_instance + work-unit instance lifecycle events for quality-gate's drift detection per `glossary/workflow.md` + `glossary/work-unit.md` composes-with quality-gate rows; quality-gate Pattern A composes with workflow_instance observability (axis-3 rubber-stamping signal at attestation moment) + work-unit instance observability (rapid sign-off cadence signal)
- **Phase 6 specs** (`docs/specs/workflow.md` + `docs/specs/work-unit.md`): inherit WorkflowDescriptor + WorkUnitKindDescriptor manifest schemas per SD-2; WorkflowError + WorkUnitError class hierarchies per ARCH §7
- **Phase 6 deployment** (per `MAINTENANCE.md` TOP-LEVEL SCOPE: PBS-Schulz workspace deployment): per-deployment workflow_instance + work-unit instance entity-md authoring + per-deployment ID uniqueness convention prose + cross-practitioner workflow handoff implementation mechanics + per-kind structural conventions schema standardization + multi-workflow_instance phase choreography implementation
- **Wave-2 Cascade-Writer commit** (anticipated tight coupling): GLOSSARY downstream — workflow + work-unit See sections; ARCHITECTURE.md §7 NEW lock entry + §2 row 3.5 update + §3 doc structure status table update; peer ARCH §17/§19 reciprocal back-mentions: substrate + audit + adapter + sparring + specialist-skill + practitioner; MAINTENANCE.md Layer 3 Primitive-cluster topic template per-pattern conditional applicability rule update for two-Pattern-B; BACKLOG.md cascade
- **BACKLOG.md cascade**: W1 (workflow_pattern primitive vs Layer A) → Phase 5+ ROADMAP entry per D Gate; W2 (cross-practitioner workflow handoff mechanics) → Phase 5+ second-multi-practitioner-deployment-surface signal (composes with `arch/practitioner.md` §14 W4); W3 (per-kind structural conventions schema standardization) → Phase 6 spec territory; W4 (multi-workflow_instance phase choreography mechanics) → Phase 5+ second-workspace-multi-workflow_instance-pattern signal; cross-DR cumulative REVISION-flavored count (1 here + 2 in `arch/specialist-skill.md` DR + 1 in `arch/practitioner.md` DR = 4) flagged for Coherence-audit C2 evaluation of 3-tier discriminator codification (trip threshold reached: 4 ≥ 3)

## 9. Files touched

Wave 1 (this DR commit + ARCH topic; commit `3b187ea`):
- `arch/workflow-work-unit.md` (NEW; primitive-cluster 12+5 ARCH topic; two-Pattern-B topic-template-class anchor)
- `docs/decisions/workflow-work-unit-arch-topic.md` (THIS file; composite DR; Mode 2 sub-decisions)

Cascade Wave 2 scope (deferred to Wave-2 Cascade-Writer per `arch/specialist-skill.md` DR §9 + `arch/practitioner.md` DR §9 Wave-2 cascade pattern precedent; anticipated):

**A. GLOSSARY downstream cascade**:
- `glossary/workflow.md` See section update (placeholder text replaced with anchored `arch/workflow-work-unit.md` reference per Phase 3.5 third primitive-cluster lock; parallel to glossary/specialist.md + glossary/practitioner.md Wave-2 cascade per Notes 56 + 57)
- `glossary/work-unit.md` See section update (parallel; placeholder text replaced with anchored `arch/workflow-work-unit.md` reference)
- `glossary/authority-binding.md` See section reciprocal mention (potentially — if workflow phase transitions + work-unit lifecycle transitions warrant explicit authority-binding back-link per Cascade-Writer scope determination)

**B. Peer ARCH §17/§19 reciprocal back-mentions** (Lens 6 reciprocal symmetry; per Note 56 + Note 57 specialist-skill + practitioner Wave-2 cascade precedent):
- `arch/substrate.md` §19 (added `arch/workflow-work-unit.md` reference — substrate Surface §C permission flow integrates with workflow_instance phase transitions + work-unit instance lifecycle transitions; Surface §F session/context management persists workflow_instance + work-unit instance state across sessions)
- `arch/audit.md` §19 (added `arch/workflow-work-unit.md` reference — Surface §A emission API for §SD-4 event-kind catalog; Surface §C query API for cross-workflow_instance + cross-work-unit-instance audit-trail defensibility; §14 cross-shape policy variation per-shape audit emission granularity composes with work-unit attribution)
- `arch/adapter.md` §19 (added `arch/workflow-work-unit.md` reference — adapters invoked by skills firing within workflow_instance phases per `glossary/skill.md` composes-with adapter row)
- `arch/sparring.md` §19 (added `arch/workflow-work-unit.md` reference — sparring sub-mechanisms accessed by skills DURING workflow_instance phase progression AND ad-hoc work-unit progression; orthogonal to workflow primitive engagement per per-shape activation matrix)
- `arch/specialist-skill.md` §17 (forward-reference upgraded to backward-reference per Note 56 + Note 57 cleanup discipline — workflow-work-unit-reference recasts from "Forward-references to future Phase 3.5 topics" to "Phase 3.5 third primitive-cluster LOCKED"; cross-specialist composition rules per §10 + §3 apply to cross-specialist work-unit attachment per workflow-work-unit §3)
- `arch/practitioner.md` §17 (forward-reference upgraded to backward-reference — workflow-work-unit-reference recasts from "Forward-references to future Phase 3.5 topics" to "Phase 3.5 third primitive-cluster LOCKED"; workflow_instance bound_practitioner_id + work-unit instance attribution compose through practitioner-RECORD per §4 R-CC-10; cross-practitioner workflow handoff mechanics per §14 W4 composes with W2 in workflow-work-unit)

**C. ARCHITECTURE.md updates**:
- `ARCHITECTURE.md` §7 NEW lock entry: "Workflow + work-unit ARCH topic (Phase 3.5 third primitive-cluster) — LOCKED" (positioned after practitioner entry, before Phase 3.1 closed entry; covers two-Pattern-B topic-template-class anchor + 4-sub-section structural overview + always-present asymmetry + cardinality asymmetry + ad-hoc work first-class + snapshot pattern + cross-specialist composition rules + 2 state machines + per-shape policy variation matrix + 8-category error catalog + W1-W4 watch-list + composes-with substrate §C/§F + audit §A/§C + adapter + sparring + specialist-skill + practitioner + authority-binding mechanism + cross-axis composition axis-1/2/3)
- `ARCHITECTURE.md` §2 Phase 3 sub-phase status table row 3.5 update (reflects third primitive-cluster LOCKED — workflow-work-unit; two-Pattern-B topic-template-class anchor; 3 primitive-cluster + cross-cutting integrator topics remain)
- `ARCHITECTURE.md` §3 Doc structure status table update (6 of 11 → 7 of 11 drafted: substrate / adapter / sparring / audit / specialist-skill / practitioner / workflow-work-unit)

**D. MAINTENANCE.md Layer 3 Primitive-cluster topic template subsection**:
- Per-topic section count expectation row updated for workflow-work-unit: marked as ANCHOR for two-Pattern-B topic-template-class; "12 common + 3 conditional applies (§8 + §9 + §13) + 2 N/A documented (§10 + §11) + §12 N/A-parity = 18 total"
- Per-pattern conditional applicability bullet updated: Two Pattern B clusters marked as ANCHOR per `arch/workflow-work-unit.md`; "granularity + per-primitive lifecycle ordering APPLIES; cross-shape policy variation APPLIES; bundle / marketplace N/A documented explicitly (workflow + work-unit are bundled IN specialist, not bundlers themselves); 12+5 template extends WITHOUT variation"

**E. BACKLOG.md cascade**:
- Phase 3.5 row resolution: workflow-work-unit topic marked RESOLVED with cluster commits `3b187ea` (Wave-1) → Wave-2 cascade commit hash (resolved at Wave-2 commit landing) + execution-pattern signal + DR + profile-cluster validation citations + HANDOFF Note 58 forward-reference
- Phase 5 ROADMAP entries added: "Workflow_pattern primitive vs Layer A reusable templates" (W1) + "Cross-practitioner workflow handoff mechanics" (W2) + "Multi-workflow_instance phase choreography mechanics" (W4)
- Phase 6 watch-list entries added: "Per-kind structural conventions schema standardization" (W3) + "Workflow_instance suspension state implementation" + "work-unit instance pivot mechanics implementation"
- Cross-cutting "3-tier REVISION/EXPANSION discriminator codification" watch-list cumulative count update (4 REVISION-flavored EXPANSIONS across 3 cluster-executions: specialist-skill = 2 + practitioner = 1 + workflow-work-unit = 1; **trip threshold reached: 4 ≥ 3**; flag for Coherence-audit C2 evaluation post-Phase-3.5 close per `disciplines/09-coherence-audit-cadence.md`)

**Wave-2 cascade applied** (commit hash recorded in HANDOFF Note 58 + git log; cascade-bundle pattern per Note 56 + Note 57): A1+A2 GLOSSARY downstream cascade (workflow.md + work-unit.md See sections anchored to `arch/workflow-work-unit.md`) + A3 reciprocal mention (glossary/authority-binding.md composes-with workflow + work-unit rows + See section reciprocal back-link APPLIED per cardinality-asymmetry composition); B1-B6 peer ARCH §17/§19 reciprocal back-mentions (substrate + audit + adapter + sparring §19; specialist-skill + practitioner §17 forward-references upgraded to backward-references); C1 `ARCHITECTURE.md` §7 NEW lock entry + C2 §2 row 3.5 update (2 of 6 → 3 of 6 phrasing per row content; remaining count `3 primitive-cluster + cross-cutting integrator topics remain`) + C3 §3 doc structure status table update (6 of 11 → 7 of 11); D1+D2 MAINTENANCE.md Layer 3 Primitive-cluster topic template ANCHOR codification for two-Pattern-B + per-topic count expectation row update; E1-E4 BACKLOG cascade (Phase 3.5 row resolution + Phase 5 W1+W2+W4 + Phase 6 W3 + suspension/pivot watch-list entries + 3-tier discriminator cumulative-count update reaching trip threshold).

**F. DR §9 Files-touched Wave-2 cascade hash resolution** (THIS amendment per cascade discipline auditability; following Note 57 specialist-skill + practitioner DR §9 Wave-2 cascade-scope pattern precedent): Wave-1 commit hash `3b187ea` substituted for placeholder `<this-commit>` in Wave-1 enumeration above; Wave-2 cascade scope sub-sections A-E supplemented with applied-status note above. This DR amendment is part of the SAME Wave-2 cascade commit (cascade-bundle pattern per Note 56 + Note 57).

## 10. Revisit triggers

- **W1 signal arrives** (≥2 specialists develop genuinely-cross-archetype workflow pattern that Layer A growth proves insufficient for): workflow_pattern framework primitive vs Layer A reusable templates examination fires; SD-1 cluster boundary amendment if primitive warranted; SD-2 manifest schema amendment for workflow_pattern fields
- **W2 signal arrives** (second multi-practitioner deployment surface): cross-practitioner workflow handoff mechanics design fires; SD-3 cross-primitive composition amendment for handoff implementation mechanics; `workflow_handoff` event-kind shape design + attribution chain preservation rules; integrates with `arch/practitioner.md` §14 W4 (composes with same awaited-signal)
- **W3 signal arrives** (≥3 kinds across specialists develop divergent artifact-attachment shapes warranting standardization): per-kind structural conventions schema design fires; SD-2 work-unit kind manifest schema amendment for `artifact_attachment_shape` field standardization; Phase 6 spec territory
- **W4 signal arrives** (second workspace deploys multi-workflow_instance against single work-unit pattern): multi-workflow_instance phase choreography mechanics design fires; SD-3 cross-primitive composition amendment for multi-workflow_instance coordination; SD-4 lifecycle ordering amendment for cross-workflow phase coordination; integrates with `arch/specialist-skill.md` §10 cross-specialist composition rules
- **Future primitive-cluster topic creation** (Phase 3.5 `arch/claim-defensibility.md` next + cross-cutting integrators last): validates 12+5 template extension per SD-1; if two-Pattern-B-specific 6th conditional candidate surfaces, MAINTENANCE.md Layer 3 §3 amendment per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern
- **Phase 6 spec creation**: WorkflowDescriptor + WorkUnitKindDescriptor Pydantic schemas may surface architectural amendments (~10-20% Phase 1 → Phase 2 architectural flow-back per `decision-design-sharpening` §Phase 1 → Phase 2 transition)
- **Coherence-audit C2** (post-Phase-3.5 close): primitive-cluster set audited at phase boundary; cross-primitive coherence verified across specialist-skill + practitioner + workflow-work-unit + claim-defensibility + cross-cutting integrators; cumulative REVISION-flavored count (4 across 3 cluster-executions; trip threshold reached) evaluated for 3-tier discriminator codification per BACKLOG watch-list
