# Decision record: Practitioner ARCH topic (Phase 3.5 second primitive-cluster)

## 1. Status

**ACCEPTED** (session 28, 2026-05-03). 2-round decision-design-sharpening (Round 1 full monty + Round 2 user-triggered). Mode 2 upfront-known composite decomposition per `decision-design-sharpening` v0.10.0 §Two decomposition modes — 5 sub-decisions tightly coupled; single composite DR (sub-decisions have no independent meaning outside the composite).

Sharpening rounds metadata:
- Round 1 (full monty): 5 sub-decisions inventoried + sharpened with foundation-up dependency ordering
- Round 2 (user-triggered): cross-cutting + schema-detail refinements (R-CC-1 through R-CC-10 + R-SD-1 + R-SD-2)
- STABLE-AT-ROUND-2 verdict per `decision-design-sharpening` §Lock + persist signals (DECAY CONFIRMED; specific termination signal named below)
- LOCK-HARD target-type per skill §Step 4 target-type modifier (architectural decision; cascades hard if revised)

## 2. Owner

Phase 3.5 — second primitive-cluster ARCH topic. Anchors **Pattern C topic-template-class** (parallel to `arch/substrate.md` anchoring Pattern A 12+7 template + `arch/specialist-skill.md` anchoring primitive-cluster 12+5 template). Pattern C-specific conditional applicability rules surface here per per-pattern conditional applicability rules in `MAINTENANCE.md` Layer 3 Primitive-cluster topic template (granularity / bundle / marketplace likely N/A; cross-shape policy variation + per-primitive lifecycle ordering likely apply). Cited as precedent for downstream Phase 3.5 primitive-cluster topics where Pattern C-class conditional applicability surfaces.

## 3. Related

**Composes with**:
- `arch/substrate.md` Surface §C (permission flow records practitioner identity at HITL approval moments per R-CC-4) + §G (specialist registration composes with practitioner-record activation ordering per R-CC-1) + §10 (boot ordering integration) + §8 (dual-emission paths apply when practitioner-attribution events flow through both substrate-internal AND skill-side emission)
- `arch/audit.md` Surface §A (emission API + actor declaration for practitioner-RECORD identity) + §C (query API for cross-practitioner audit-trail defensibility test per R-CC-7) + §14 (cross-shape policy variation per R-CC-2 audit emission granularity composes with practitioner attribution) + §15 W5 federated audit-trail watch (composes with W1 multi-tenant federation)
- `arch/sparring.md` §14 per-shape activation matrix + sparring engagement events `actor_kind: ai_runtime` per R-CC-3
- `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition (W2 Identity-class adapter Surface candidate per W2)
- `arch/specialist-skill.md` §5 mid-session re-binding (cross-specialist activation actor binding back-link per R-CC-9) + §13 archival-as-default destruction semantics (cross-pattern coherence per R-CC-8)
- `docs/decisions/specialist-skill-arch-topic.md` (primitive-cluster 12+5 template precedent + Mode 2 composite decomposition precedent)
- `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` (Pattern A / mechanism-class template; primitive-cluster 12+5 derived parallel)
- `docs/decisions/audit-arch-topic.md` (mechanism-class precedent; per-shape trust model parameterization)

**GLOSSARY entries** (locked; cited extensively):
- `practitioner` (canonical Pattern C bipartite entry; HUMAN cross-cutting + RECORD at Owner B)
- `actor` (`actor_kind: human` for practitioner-emitted events; practitioner is one specific actor kind)
- `authority-binding` (per-event actor declaration; practitioner-RECORD as human authority)
- `workspace` (workspace serves practitioner(s); records at Owner B; multi-practitioner mechanics + legal-entity context)
- `Owner B scope` (practitioner-RECORD placement)
- `defensibility` (axis-3 operational test resolves at practitioner-author granularity)
- `engaged-authorship` (production-phase + attestation-phase per-claim engagement composes through practitioner-RECORD identity)
- `co-worker` (practitioner is human side of axis-1 co-worker pairing)
- `claim` (practitioners accountable for individual claims; defensibility resolves at claim granularity through practitioner attribution)
- `session` (session binds to ONE practitioner-record at session-open per R-CC-10)

**Forward-references** (future Phase 3.5 topics):
- `arch/claim-defensibility.md` (per-claim attestation chain via authority-binding + practitioner-RECORD identity; defensibility resolves at claim granularity)
- `arch/workflow-work-unit.md` (cross-practitioner workflow handoff mechanics per W4 + workflow_handoff event-kind composition)
- `arch/scope-model.md` (Owner B scope category for practitioner-RECORD placement; multi-practitioner workspace mechanics)

**Disciplines applied**:
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (signing_authority gate-enforced structural; cross-practitioner write boundary structural per axis-3)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (practitioner is always natural person regardless of shape; pioneer-neutrality of cluster primitive)
- `MAINTENANCE.md` TOP-LEVEL SCOPE (per-deployment practitioner-record instance-content lives at deployment-instance, not framework repo)
- `DISCIPLINES.md` Discipline 1 (skill+profile sub-section); Discipline 8 (foundation-up ordering); Discipline 10 (greenfield-evaluation of archived sources)

**Archived sources** (INPUT only per Discipline 10 — greenfield-evaluated against current locked vocabulary; NOT transcribed as template):
- `archive/docs/decisions/office-level-managed-entities.md` (NAMING SUPERSEDED per archived header — "Office-level managed entities" → "Workspace-scope managed entities" per current locked vocabulary; ActorEntity schema lines 84-95 cited as INPUT for practitioner-RECORD field enumeration but NOT transcribed verbatim — archive conflates actor + practitioner; current locked vocabulary SEPARATES them per `glossary/actor.md`; greenfield-derived practitioner-RECORD schema per current Pattern C bipartite)
- `archive/docs/decisions/governance-and-identity-sourcing.md` (decision 1 = role primitive at shape-policy per current vocabulary — applied to `role_bindings` field per SD-2 / §8; decision 2 = native vs adapter mode for practitioner-RECORD source — applied to `mode` + `adapter_binding` fields per SD-2; decision 3 = per-deployment uniqueness convention preserved as deployment-side commitment per R-SD-1; decision 4 = prose-rules pattern for ID minting cited as deployment-level discipline)

## 4. Context

Phase 3.5 second primitive-cluster ARCH topic. Prior to this DR, Phase 3.5 first primitive-cluster topic (specialist-skill) LOCKED at commit `f6bab6e` per `ARCHITECTURE.md` §7 + `docs/decisions/specialist-skill-arch-topic.md`; Pattern A protocol topics + mechanism-class topics LOCKED in Phase 3.4 per `ARCHITECTURE.md` §7 (substrate + adapter + sparring + audit).

**Why practitioner chosen second** (foundation-up per Discipline 8): practitioner-RECORD is the human-actor anchor for authority-binding's per-event actor declaration (per `glossary/authority-binding.md` "every `signature_applied` event records `actor_kind: human` + practitioner identity"). Authority-binding is mechanism-level framework primitive composing with claim primitive. Locking practitioner second after specialist-skill means the future Phase 3.5 `arch/claim-defensibility.md` topic locks per-claim attestation chain against an already-validated human-actor primitive. Reverse ordering would force claim-defensibility to forward-reference an unlocked human-actor primitive.

**Why Pattern C topic-template-class anchored here**: Pattern C bipartite primitive structure (HUMAN cross-cutting + RECORD at Owner B per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern C row) is structurally distinct from Pattern A pluggability + Pattern B definition+instance + Pattern D mechanism-class variation. Pattern C-specific conditional applicability surfaces here (granularity / bundle / marketplace N/A per Pattern C bipartite single-primitive nature; cross-shape policy variation + per-primitive lifecycle ordering APPLY per shape-policy-mediated cardinality + multi-practitioner activation). Future Pattern C primitive-cluster topics inherit this DR's anchor for conditional applicability rules.

**What the decision-design phase needed to resolve**:
- Pattern C topic-template-class confirmation (12+5 extends without variation; per-pattern conditional applicability rules)
- Bipartite Pattern C structural articulation (HUMAN aspect + RECORD aspect; manifest schema enumeration)
- Multi-practitioner workspace mechanics + legal-entity workspace context (cardinality matrix; cross-practitioner composition rules; workspace-level legal-entity context placement)
- Practitioner lifecycle + deactivation semantics (lifecycle states; event-kind catalog; per-shape policy variation; archival-as-default destruction)
- Authority-binding integration + cross-axis composition + watch-list (axis-1/2/3 composition; per-shape trust model; W1-W4)

## 5. Decision

Five sub-decisions per Mode 2 composite decomposition (sub-decisions have no independent meaning outside the composite; foundation-up dependency ordering applied within the composite).

### SD-1: Pattern C topic-template-class confirmation

**Decision**: 12+5 primitive-cluster template extends to Pattern C **without variation**. **Pattern C topic-template-class anchored at this topic** (parallel to substrate Pattern A 12+7 anchor + specialist-skill primitive-cluster anchor).

**Pattern C-specific conditional applicability** (per `MAINTENANCE.md` Layer 3 Primitive-cluster topic template per-pattern conditional applicability rules):
- §8 Cross-shape policy variation: APPLIES (cardinality-per-shape + multi-practitioner + legal-entity context shape-policy-mediated)
- §9 Granularity tests: N/A (practitioner has no granularity discriminator; one human = one practitioner; bipartite-aspect partition is not granularity)
- §10 Bundle composition: N/A (practitioner-RECORD doesn't bundle artifacts)
- §11 Marketplace + distribution mechanics: N/A (practitioner-records aren't distributable; identity entities owned-by-workspace)
- §12: N/A-parity (preserved per locked template convention)
- §13 Per-primitive lifecycle ordering: APPLIES (practitioner addition + deactivation + multi-practitioner activation has load-bearing ordering)

**Why N/A documented explicitly**: per `MAINTENANCE.md` Layer 3 template "document N/A explicitly when section is omitted" rule. DO NOT skip section numbering — keep §9/§10/§11/§12 as N/A sections preserving template-anchoring stability for downstream Pattern C primitive-cluster topics.

**Total expected**: ~14-15 sections (12 common + 2 conditional applies (§8 + §13) + 3 N/A documented (§9/§10/§11) + §12 N/A-parity).

### SD-2: Bipartite Pattern C structural articulation

**Decision**: Bipartite HUMAN + RECORD partition with explicit aspect-asymmetry.

**§2.1 HUMAN aspect**: cross-cutting; framework records nothing about the human directly — only the RECORD; HUMAN is the legal/professional accountability bearer in the world; framework's job is to make that accountability defensible via the RECORD; HUMAN NOT placed in any scope (per `glossary/practitioner.md` line 16 + `glossary/owner-b-scope.md` line 32).

**§2.2 practitioner-RECORD aspect**: Owner B entity shape; architectural-level enumeration of frontmatter manifest schema (Phase 6 lands Pydantic):

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | str | required | Practitioner-record identifier; per-deployment uniqueness convention per archived governance §3 |
| `legal_name` | str | required | Full legal name (the natural person) |
| `actor_kind` | enum | required | `human` per `glossary/actor.md` |
| `email` | str | optional | Contact + identity-mapping anchor (auth/SSO integration per W2) |
| `signing_authority` | enum | required | `independent` \| `under-supervision` \| `firm-bound` (framework-level enum; per-shape policy declares which categories REQUIRED per shape per SD-3 / §8) |
| `role_bindings` | list | optional | Per-workspace role list (cross-references shape-policy role primitive per archived governance decision 1) |
| `credentials` | list | optional | Professional credentials (license number; bar admission; medical license) — per-shape-policy-mandated |
| `mode` | enum | optional | `native` \| `adapter` per archived governance decision 2 |
| `adapter_binding` | str | optional | Adapter ID when mode=adapter (composes with `arch/adapter.md` Identity-class candidate per W2) |
| `lifecycle_state` | enum | required | `active` \| `dormant` per SD-4 |
| `firm_binding` | str | optional | Reference to workspace.md `legal_entity_context` block (per SD-3; for legal-entity-shape workspaces only) |

**Schema explanation note** (per R-CC-5): `signing_authority` constrains WHO can sign claims at framework level (gate-enforced structural per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1); `role_bindings` constrains WHICH actions per shape policy (shape-policy-enforced). Different scopes; both load-bearing; not redundant.

### SD-3: Multi-practitioner workspace mechanics + legal-entity workspace context

**Decision**: Cardinality matrix (3 rows): practitioner-shape solo = 1; multi-practitioner-shape partnership = N; legal-entity-shape firm = N under firm context.

**Legal-entity context lives at WORKSPACE level** (NOT practitioner-level): workspace.md may declare `legal_entity_context: { entity_name, entity_type, jurisdiction }` for legal-entity-shape workspaces; practitioner-record references back via `firm_binding: workspace_id` field. Practitioner is always a natural person regardless of workspace context.

**Cross-practitioner composition rules** (4-row table):
- Practitioner-A READS practitioner-B's signed claim: YES (audit-trail attribution preserved)
- Practitioner-A WRITES (modifies) practitioner-B's signed claim: NO (per-claim ownership boundary structural per axis-3)
- Cross-practitioner workflow handoff: YES (mid-workflow handoff = phase transition with attribution chain preserving prior + new owner)
- Cross-practitioner SPARRING engagement: YES via AI runtime (sparring `actor_kind: ai_runtime`; cross-practitioner REVIEW separate workflow phase per archived `office-level-managed-entities.md` decision 1 layered enforcement greenfield-evaluated)

**Multi-practitioner concurrent-session handling** (per R-CC-10): each session binds to ONE practitioner-record at session-open (`session.bound_practitioner_id: str`); cross-session within workspace = multiple practitioner-records active concurrently in different sessions; never multiple practitioners in single session.

### SD-4: Practitioner lifecycle + deactivation semantics

**Decision**: Lifecycle states: `active` | `dormant`.

**Lifecycle event-kind catalog** (4 kinds):
- `practitioner_record_minted` — workspace setup OR per-practitioner-addition
- `practitioner_record_updated` — single event-kind with `details.changed_fields: list[str]` per R-CC-6 (NOT separate event-kinds per field; minimal event-kind catalog growth per archived `audit-trail-v2.md` `details:` payload precedent)
- `practitioner_record_deactivated` — practitioner leaves; record becomes dormant (NOT deleted)
- `practitioner_record_reactivated` — dormant practitioner returns

**Deactivation = dormant-not-deleted**: ARCH locks rationale (axis-3 defensibility-critical; six-months-later test preservation).

**Per-shape policy variation matrix** (3 rows): practitioner-shape STRICT preservation; autonomous-business-shape archival OR deletion-with-audit; personal-OS-shape minimal lifecycle.

**Cross-practitioner-handoff at deactivation**: per shape policy (practitioner-shape may require explicit handoff-to-named-practitioner; autonomous-business-shape may permit auto-routing).

**Workspace dissolution + practitioner-record archival** (per R-CC-8 cross-pattern coherence with `arch/specialist-skill.md` §13): archival-as-default per axis-3 defensibility (practitioner-records preserve historic-claim attribution); deletion-with-audit opt-in per shape policy (`workspace.md` `instance_content_dissolution_policy: archive | delete-with-audit`).

### SD-5: Authority-binding integration + cross-axis composition + watch-list

**Decision**: Practitioner-RECORD IS the human authority bound to claim_made / signature_applied / sparring-engagement events per `glossary/authority-binding.md` line 35.

**Cross-axis composition table** (3 rows):
- axis-1 (intertwining): practitioner is the human in workflow that AI intertwines with; co-worker primitive applies
- axis-2 (sparring): practitioner is engagement subject of sparring (per `glossary/engaged-authorship.md` production-phase engagement)
- axis-3 (authorship preservation): practitioner is the ROLE axis-3 protects; per-claim attestation events bind to practitioner-record per attribution chain

**Per-shape trust model parameterizes practitioner-record's accountability surface** (per `arch/audit.md` §14):
- practitioner-shape: practitioner-judgment trust (every claim defensibility-required)
- autonomous-business-shape: budget-policy trust (signature only for budget-threshold)
- personal-OS-shape: individual trust (minimal; no professional-accountability binding)

**Watch-list (4 items)**:
- W1: Multi-tenant federation practitioner identity (awaits Tier 3 cross-org per archived governance decision 1 OR `arch/audit.md` §15 federated audit-trail watch)
- W2: Adapter-mode practitioner-RECORD source mechanics + Identity-class adapter Surface candidate (awaits concrete adapter implementation per Personio/Microsoft Entra/Coolify SSO; surfaces 6th-class candidate for `arch/adapter.md` §3 partition)
- W3: Practitioner-record signing mechanism for historic-claim defensibility (awaits Phase 6 `arch/audit.md` §D integrity verification + cryptographic-signature implementation)
- W4: Cross-practitioner workflow handoff mechanics + per-shape policy variation (awaits second multi-practitioner deployment surface; pioneer is solo)

## 6. Sharpening provenance

### Round 1 (full monty)

EXPANSIONS surfaced (count: 21 = 4 + 4 + 4 + 4 + 5 — one EXPANSION-batch per sub-decision; Mode 2 upfront-known composite per `decision-design-sharpening` v0.10.0 §Two decomposition modes "Sub-decision inventory" step):

- **SD-1 EXPANSIONS** (4): Pattern C topic-template-class confirmation; per-pattern conditional applicability rules surfaced (§9/§10/§11 N/A; §8/§13 APPLY); §12 N/A-parity preserved; per-topic section count expectation ~14-15
- **SD-2 EXPANSIONS** (4): bipartite HUMAN-vs-RECORD aspect-asymmetry articulation; HUMAN cross-cutting NOT placed; practitioner-RECORD frontmatter manifest schema 11-field enumeration; native vs adapter mode source mechanics
- **SD-3 EXPANSIONS** (4): cardinality matrix per shape (solo / partnership / legal-entity-firm); legal-entity context at workspace level (NOT practitioner level); cross-practitioner composition rules 4-row table (read YES / write NO / handoff YES / sparring YES via AI); multi-practitioner concurrent-session handling
- **SD-4 EXPANSIONS** (4): lifecycle states (active / dormant); event-kind catalog (4 kinds); deactivation = dormant-not-deleted rationale; per-shape policy variation matrix
- **SD-5 EXPANSIONS** (5): authority-binding integration; cross-axis composition table (3 rows); per-shape trust model parameterization; watch-list 4-item enumeration (W1-W4)

### Round 2 (user-triggered)

Cross-cutting + schema-detail refinements (per `decision-design-sharpening` §Round 2 layered coverage observation: cross-cutting + schema details emphasized):

**Cross-cutting refinements (R-CC-*)** — 10 items:
- **R-CC-1** (REVISION-flavored): boot ordering integration per `ARCHITECTURE.md` §6 — practitioner-record activation = within substrate-phase 3 adapter bindings load step; before substrate-phase 4 specialist registration. Goes in §13 per-primitive lifecycle ordering (structural elevation of implicit boot ordering to explicit)
- **R-CC-2**: per-shape audit emission granularity composes with practitioner attribution per `arch/audit.md` §14 (claim-level / action-level / light); composition table row in §4
- **R-CC-3**: sparring engagement events composition row in §4 composition table
- **R-CC-4**: substrate Surface §C permission flow composition row in §4 composition table (HITL approval moments record practitioner identity)
- **R-CC-5**: signing_authority vs role_bindings interaction note in SD-2 / §2.2 schema explanation (different scopes; gate-enforced vs shape-policy-enforced)
- **R-CC-6**: practitioner_record_updated single event-kind with `details.changed_fields` (already in SD-4 catalog; minimal event-kind catalog growth)
- **R-CC-7**: cross-practitioner audit-trail query pattern (defensibility test mechanic) — composition table row in §4 (audit Surface §C query API)
- **R-CC-8**: workspace dissolution archival per cross-pattern coherence with `arch/specialist-skill.md` §13 (already in SD-4)
- **R-CC-9**: cross-specialist activation actor binding back-link to `arch/specialist-skill.md` §5 mid-session re-binding — composition table row in §4 + cross-reference in §17
- **R-CC-10**: multi-practitioner concurrent-session handling (already in SD-3)

**Schema-detail refinements (R-SD-*)** — 2 items:
- **R-SD-1**: practitioner-RECORD entity-md storage convention deferred to Phase 6 (per `MAINTENANCE.md` TOP-LEVEL SCOPE: instance-content storage is deployment-instance not framework); §16 Phase routing entry
- **R-SD-2**: signing_authority enum 4th value REJECTED via D Gate (mental-modeling-resolves; per-shape policy handles attesting-only edge); document in DR §6 manufactured-criticism rejections

**Round 2 EXPANSIONS count**: 12 substantive findings (R-CC-1 through R-CC-10 + R-SD-1 + R-SD-2). Per `decision-design-sharpening` §Empirical density check: Round 1 = 21 EXPANSIONS (sub-decision-batched); Round 2 = 12 EXPANSIONS — drops ~43%, AMBIGUOUS region per density-behavior table (25-50% drop), but Round 2 surface is cross-cutting + schema-detail layer per §Layered coverage observation (different concern layer; not direct comparison to Round 1 sub-decision foundational batch).

### Manufactured-criticism rejections

Per `decision-design-sharpening` §Manufactured-comfort counter-test + §Pareto calibration: reject refinements that aren't Pareto-improving OR that surface manufactured-criticism territory.

Cumulative count: 6 (SD-1 ST3 + SD-2 ST3 + SD-3 ST3 + SD-4 ST3 + SD-5 ST2 + R-SD-2):

- **SD-1 ST3 rejected**: "Should Pattern C topic-template-class introduce 6th conditional candidate for Pattern C-specific bipartite-aspect-articulation section?" — manufactured criticism; bipartite-aspect articulation lives in §2.1/§2.2 per common-required §2 Per-primitive structural overview; new conditional adds template-surface without Pareto improvement; Pattern C-specific articulation handled within §2 sub-sections per common-required template
- **SD-2 ST3 rejected**: "Should practitioner-RECORD frontmatter include `competence_area` field analogous to specialist `axis_claim`?" — manufactured criticism; practitioner is the human, not the codified expertise; competence-area is a workspace + specialist-activation concern, NOT practitioner-RECORD identity concern; field adds schema surface without genuine attribution improvement (already covered by `role_bindings` + per-claim attribution chain)
- **SD-3 ST3 rejected**: "Should multi-practitioner workspace introduce separate `partnership` primitive for partnership cardinality?" — manufactured criticism; partnership is workspace-shape variation (multi-practitioner-shape vs legal-entity-shape per cardinality matrix), NOT a separate primitive; new primitive adds vocabulary surface without Pareto improvement; workspace-shape variation handles partnership-specific concerns
- **SD-4 ST3 rejected**: "Should lifecycle introduce 3rd state `suspended` between active and dormant?" — manufactured criticism; suspended adds state-machine complexity without identified deployment friction; mental-modeling-resolves test (per D Gate procedure per `profiles/INDEX.md`): suspension semantics handled via `lifecycle_state: dormant` + per-shape reactivation policy; no profile evidence for genuine 3rd state need
- **SD-5 ST2 rejected**: "Should W5 add 'practitioner-attestation event quality grading' watch?" — manufactured criticism; attestation quality grading is per-shape policy concern (per `glossary/engaged-authorship.md` shape-policy-level QUALITY refinement layer + `arch/audit.md` §14 per-shape granularity), NOT practitioner-RECORD framework concern; quality grading lives in shape policy bundle
- **R-SD-2 rejected**: "Should signing_authority enum add 4th value `attesting-only`?" — manufactured criticism via D Gate (per `decision-design-sharpening` Round 2 D Gate procedure per `profiles/INDEX.md`); mental-modeling-resolves test: attesting-only edge case handled by per-shape policy declaring required `signing_authority` categories (per §8) + per-shape attestation rules (per `arch/audit.md` §14 trust model); 3-value enum (`independent` | `under-supervision` | `firm-bound`) + per-shape policy interpretation covers attesting-only scenario without enum surface growth

### GLOSSARY back-check verdict

Per `MAINTENANCE.md` Bidirectional cascade + `decision-design-sharpening` v0.5.0 GLOSSARY back-check at Round 2 termination.

**Verdict**: CLEAN — no retro-fits needed. Candidates evaluated:

- **Practitioner-RECORD frontmatter manifest schema fields** evaluated for glossary-grade structural fact: result NOT glossary-grade per `MAINTENANCE.md` Bidirectional cascade rule ("Schema details / per-impl mechanics / operational procedures / per-shape variations are NOT glossary-grade — they stay in ARCH/DR/spec"). Schema lives in ARCH topic + Phase 6 spec.
- **Bipartite HUMAN-vs-RECORD aspect-asymmetry articulation** evaluated for glossary-grade structural fact: result already-codified in `glossary/practitioner.md` line 16 + `glossary/owner-b-scope.md` line 32 (HUMAN cross-cutting NOT placed; RECORD at Owner B). Current locked GLOSSARY entry adequately captures the bipartite structural distinction; no retro-fit needed.
- **Legal-entity workspace context placement at WORKSPACE level** evaluated: already-codified in `glossary/practitioner.md` ("Legal-entity context (firm-level contracting party) lives at WORKSPACE level... not at practitioner level"). No retro-fit needed.
- **Multi-practitioner concurrent-session handling (`session.bound_practitioner_id`)** evaluated for glossary-grade structural fact: result NOT glossary-grade per Bidirectional cascade rule (schema detail + per-shape variation; framework-level cardinality `1 practitioner-record per session` is implicit in `glossary/session.md` "bounded interaction unit within a workspace" + `glossary/practitioner.md` cardinality + lifecycle line 20).
- **Cross-practitioner composition rules (4-row table)** evaluated: per-event composition mechanics live in ARCH topic + composition with `glossary/authority-binding.md` per-event actor declaration. Glossary entries adequately reference; no retro-fit needed.

### Profile-anchored validation

Per `decision-design-sharpening` v0.5.0+ profile-anchored validation + `profiles/INDEX.md` cluster structure (Cluster A Producers / B Deployers / C Consumers / D Validators).

**3 cluster representatives Read** (≥3 cluster coverage requirement; FULL DETAIL profile content cited NOT cluster letters):

**Cluster B Deployers** + **Cluster C Consumers** — `profiles/L5a-planner-pbs-schulz.md` (pioneer; multi-cluster member):
- L5a lines 12-17 single-practitioner reality: validates Pattern C bipartite primitive structure + practitioner-shape solo cardinality (per SD-3 cardinality matrix); pioneer evidence anchors solo workspace shape
- L5a lines 76-83 active specialists set + lines 85-92 active substrate + adapters: validates practitioner-RECORD as workspace-bound managed entity + adapter binding context (per SD-2 schema mode field; W2 adapter-mode source mechanics)
- L5a lines 95-101 multi-user moments evidence: validates solo workspace + external actors as engagement targets (NOT workspace users) — anchors W4 watch-list (cross-practitioner workflow handoff awaits second multi-practitioner deployment surface; pioneer is solo)
- L5a lines 119-129 stress-tests: solo defensibility scenario + capacity-building + per-claim attestation in practice — validates per-shape trust model parameterization per SD-5 (practitioner-shape: every claim defensibility-required)
- Verdict: covered

**Cluster D Validators** — `profiles/G-composability-gate.md` (cross-cutting validation gate; Cluster D member):
- G lines 14-22 multi-mode consumption framing: practitioner-record handling cross-shape consumption (per §8 cross-shape policy variation); validates SD-3 multi-practitioner workspace mechanics + per-shape cardinality enforcement
- G lines 154-157 cross-shape consumption rules: shape-policy-mediated practitioner cardinality + signing_authority requirements (per SD-3 + §8); validates shape policy declares per-shape practitioner mandates per `arch/audit.md` §14 trust model parameterization
- G lines 162-184 architectural concerns surfaced: backup-migration round-trip implicates practitioner-record portability (per W1 multi-tenant federation watch-list); cross-substrate consumption + cross-shape consumption rules covered in §8
- Verdict: covered

**Cluster A Producers** — `profiles/L1-specialist-creator.md` (Cluster A member; SKELETON profile fleshed-on-demand for this validation):
- L1 lines 18-29 specialist creator stress-tests (intended-stress-test enumeration): cross-shape compatibility + cross-substrate compatibility cited as L1 producer evidence — practitioner-RECORD shape-policy-mediated mandate per §8 + adapter-mode source mechanics per W2 validate against L1's cross-shape compatibility surface; specialist creator profile validates that practitioner-RECORD field schema (per SD-2) supports shape-mandate-fulfilment claims at per-deployment integration time
- L1 lines 30-32 packaging boundary: practitioner-RECORD is NOT packaged-distributable (per §11 N/A); L1's packaging boundary discipline applies to specialist DEFINITION (Framework C distributable), not to practitioner-RECORD (Owner B workspace-bound); discriminator confirms §11 N/A correct for Pattern C bipartite identity primitive
- Verdict: covered (skeleton profile provides sufficient evidence for Pattern C cluster validation; full L1 fleshing not required for this decision per `profiles/INDEX.md` skeleton-fleshing-on-demand strategy)

**Cluster D Validators (gate component)** — D Defer Gate per `profiles/INDEX.md` "D Gate procedure":
- W1 multi-tenant federation: external-information test passes (specific signal = Tier 3 cross-org federated deployment OR `arch/audit.md` §15 W5 federated audit-trail signal); effort-asymmetry test passes (per-tenant federation mechanics design before evidence accumulates risks wrong-design); D Gate satisfied → W1 watch-list with resolution mechanism
- W4 cross-practitioner workflow handoff: external-information test passes (specific signal = second multi-practitioner deployment surface; pioneer is solo per L5a); effort-asymmetry test passes (per-shape handoff mechanics design before second-deployment friction risks wrong-design); D Gate satisfied → W4 watch-list with resolution mechanism
- R-SD-2 signing_authority 4th value: D Gate FIRED — mental-modeling-resolves test passed (per-shape policy handles attesting-only edge per `arch/audit.md` §14 trust model + §8 per-shape required-categories); rejected per manufactured-criticism (mental modeling resolves; no enum surface growth)
- Verdict: D Gate satisfied per genuine awaited evidence (W1 + W4) + mental-modeling-resolves rejection (R-SD-2)

### Mode 2 composite decomposition rationale

Per `decision-design-sharpening` v0.10.0 §Two decomposition modes Mode 2:
- **Trigger satisfied**: 5 sub-decisions visible at framing time (not emergent from drift); foundation-up dependencies identifiable (SD-1 template enables SD-2-5 to inherit shape; SD-2 RECORD schema enables SD-3 multi-practitioner mechanics; SD-3 + SD-4 enable SD-5 authority-binding integration + cross-axis composition)
- **Sub-decision inventory at start**: 5 sub-decisions listed before Round 1 (SD-1 → SD-5); composite decomposition mode declared upfront
- **Foundation-up dependency ordering**: SD-1 (template confirmation) locks first; SD-2 (bipartite Pattern C structure + RECORD schema) builds on SD-1; SD-3 (multi-practitioner mechanics) builds on SD-2 RECORD; SD-4 (lifecycle) builds on SD-2 RECORD; SD-5 (authority-binding integration + cross-axis + watch-list) layers on top of validated cluster shape
- **Per-sub-decision sharpening**: each got Round 1 + Round 2 sweep within the composite (no per-sub-decision split into separate rounds)
- **Synthesis pass at end**: this DR + ARCH §18 composition table is the cross-sub-decision coherence pass
- **Single composite DR**: chosen per Mode 2 §Single composite DR — sub-decisions have no independent meaning outside the composite; practitioner cluster is the unit, not 5 independent decisions

### REVISION/EXPANSION classification self-check

Per `decision-design-sharpening` v0.6.0 self-check at Round 2 termination + BACKLOG watch-list "3-tier discriminator codification".

**REVISION-flavored EXPANSIONS surfaced** (load-bearing structural elevations):
- R-CC-1 (boot ordering integration; structural elevation of implicit boot ordering to explicit per `ARCHITECTURE.md` §6 composite boot subsection) — REVISION-flavored

**Cumulative count for awaited 3-tier signal**: 1 REVISION-flavored EXPANSION in this composite. Combined with `arch/specialist-skill.md` DR's 2 REVISION-flavored EXPANSIONS = 3 cumulative across consecutive Phase 3.5 primitive-cluster decisions. Below ≥3-tier-codification trigger threshold per BACKLOG watch-list (specifically: REVISION-flavored EXPANSIONS within current composite); **2-tier (REVISION/EXPANSION) holds**; signal hasn't materialized for this composite. Note: cross-DR cumulative count meets the 3-DR threshold per BACKLOG watch-list — flag for Coherence-audit C2 at Phase 3.5 close to evaluate whether 3-tier codification is now warranted across primitive-cluster topic class.

**Pure REVISIONS** (architectural pivots changing existing decisions): 0. R-CC-1 is EXPANSION-with-load-bearing-implications, not pure architectural reversal.

### Termination signal (STABLE-AT-ROUND-2)

Per `decision-design-sharpening` §Round termination signals + §Honest termination test Q1-Q5:

- **Q1 (count)**: Round 1 = 21 EXPANSIONS (sub-decision-batched); Round 2 = 12 EXPANSIONS
- **Q2 (decay)**: Round 1 → Round 2 = 21 → 12 (drops ~43%; AMBIGUOUS region per density-behavior table; but Round 2 surface is different concern layer per §Layered coverage observation)
- **Q3 (density behavior)**: Round 2 surfaced cross-cutting + schema-detail refinements (per skill §Layered coverage observation Round 2 emphasis); no Round 3 architectural-pattern-surfacing pending
- **Q4 (specific unaddressed pass)**: NONE — all 4 profile clusters covered (A + B + C + D); G Gate + D Gate fired; cross-cutting + schema details exhausted at decision-design-phase
- **Q5 (specific termination signal)**: NARROW ARCHITECTURAL SURFACE per `decision-design-sharpening` §Empirical sweet-spot pattern (Pattern C narrower than Pattern B + atomic-primitive per fewer applicable conditional sections — 2 APPLY vs specialist-skill's 5; matches `arch/specialist-skill.md` DR Note 56 specialist-skill termination signal); operational concerns (per-deployment storage convention; adapter hydration caching; cross-practitioner handoff implementation mechanics) belong to Phase 6 pre-implementation per §Phase 1 → Phase 2 transition
- **Lock + persist signal**: STABLE per Q5 specific termination signal + Q4 no-unaddressed-pass + manufactured-comfort counter-test passed (operational concerns explicitly deferred per §Layered coverage observation Round 4+ DEFER to Phase 2)

## 7. Composition with existing architecture

This decision composes with prior locked architecture:

- **Pattern A protocols** (substrate / adapter; sparring + audit mechanism classes per Phase 3.4 close): practitioner composes with substrate Surface §C (permission flow records practitioner identity at HITL approval moments per R-CC-4) + §F (session/context management; session binds to ONE practitioner-record per R-CC-10); with audit Surface §A skill-side emission + §C query API (per R-CC-7); with adapter §3 framework-baseline-vs-shape-extension partition (W2 Identity-class adapter Surface candidate). Practitioner is NOT Pattern A (no multiple interchangeable implementations of one Surface) — practitioner is Pattern C bipartite (HUMAN cross-cutting + RECORD at Owner B).

- **Pattern B specialist-skill primitive cluster** (per `arch/specialist-skill.md` Phase 3.5 first primitive-cluster lock): cross-specialist activation actor binding back-link per `arch/specialist-skill.md` §5 mid-session re-binding — when specialist activates mid-session, the activating actor is practitioner-RECORD bound to current session (R-CC-9 cross-cutting refinement); back-link preserves attribution chain across capability changes.

- **authority-binding mechanism** (per `glossary/authority-binding.md` from Phase 3.4 C1 cascade): practitioner-RECORD IS the human authority bound to claim_made / signature_applied / sparring-engagement events per per-event actor declaration sub-aspect; per-claim author attribution chain composes through practitioner-RECORD identity for `actor_kind: human` events.

- **`ARCHITECTURE.md` §6 composite boot subsection**: practitioner-record activation ordering integrates within substrate-phase 3 adapter bindings load step per ARCH §13 boot-time activation ordering (R-CC-1 REVISION-flavored EXPANSION; structural elevation of implicit boot ordering to explicit).

- **`MAINTENANCE.md` Layer 3 Primitive-cluster topic template** (locked per `arch/specialist-skill.md` DR + `MAINTENANCE.md` Layer 3 §3 Primitive-cluster topic template subsection): Pattern C topic-template-class anchored at this topic per per-pattern conditional applicability rules (granularity / bundle / marketplace likely N/A for Pattern C bipartite single-primitive clusters; cross-shape policy variation + per-primitive lifecycle ordering likely apply). Future Pattern C primitive-cluster topics inherit this DR's anchor for conditional applicability rules.

- **TOP-LEVEL DESIGN PRINCIPLES §1 (structural over conventional)**: signing_authority gate-enforced structural (the gate dispatches on it for every signed-claim emission); cross-practitioner write boundary structural per axis-3 (each practitioner accountable for own signed claims; cross-practitioner write would break attribution chain integrity) — both exemplify structural-over-conventional discipline.

- **TOP-LEVEL DESIGN PRINCIPLES §2 (pioneer-neutrality)**: practitioner cluster primitives stay shape-neutral / archetype-neutral / pioneer-neutral; pioneer (PBS-Schulz) reality grounds the cluster primitive without leaking pioneer specifics (Bauleitplanung / B-Plan-Begründung / UNB / Stellungnahme do NOT appear in primitive definition).

## 8. Constraints flowing to downstream commitments

- **Phase 3.5 future primitive-cluster topics** (`arch/workflow-work-unit.md` / `arch/claim-defensibility.md`): inherit primitive-cluster 12+5 template per SD-1 + Pattern C-specific conditional applicability pattern (document N/A explicitly per template rule; preserve §12 N/A-parity reservation); Pattern C topic-template-class anchored here serves as precedent for conditional applicability when future Pattern C primitive-cluster topics emerge
- **Phase 3.5 `arch/claim-defensibility.md`** (next primitive-cluster topic; foundation-up dependency on practitioner): specifically inherits SD-5 cross-axis composition table + per-shape trust model parameterization; locks per-claim attestation chain mechanics against validated practitioner-RECORD primitive
- **Phase 3.5 `arch/workflow-work-unit.md`**: cross-practitioner workflow handoff mechanics (W4) compose with workflow_handoff event-kind shape; per-shape required-handoff-recipient enforcement per shape policy
- **Phase 3.6 `arch/quality-gate.md`**: consumes practitioner-attestation events for axis-3 intervention per `glossary/engaged-authorship.md` quality-gate row; quality-gate Pattern A composes with practitioner-RECORD identity for per-claim attestation defensibility
- **Phase 6 specs** (`docs/specs/practitioner.md`): inherit practitioner-RECORD frontmatter manifest schema per SD-2; PractitionerError class hierarchy per ARCH §7
- **Phase 6 deployment** (per `MAINTENANCE.md` TOP-LEVEL SCOPE: PBS-Schulz workspace deployment): per-deployment practitioner-record entity-md authoring + per-deployment ID uniqueness convention prose + adapter-mode hydration caching mechanics (R-SD-1; per-deployment storage convention deferred to Phase 6)
- **Wave-2 Cascade-Writer commit** (this commit's tight coupling): GLOSSARY back-check applied (CLEAN per §6 verdict — no retro-fits needed); MAINTENANCE.md Layer 3 Primitive-cluster topic template Pattern C-specific conditional applicability codification (if Pattern C-specific applicability rules warrant explicit codification per Cascade-Writer scope determination); ARCHITECTURE.md §7 lock entry; Lens 6 reciprocal back-mentions in peer ARCH topics §17/§19 (substrate + audit + adapter + sparring + specialist-skill)
- **BACKLOG.md**: W1 (multi-tenant federation practitioner identity) → Phase 5+ ROADMAP entry per D Gate; W2 (adapter-mode practitioner-RECORD source mechanics + Identity-class adapter Surface candidate) → Phase 6 watch trigger composing with `arch/adapter.md` §3 partition; W3 (practitioner-record signing mechanism) → Phase 6 audit-trail integrity implementation trigger; W4 (cross-practitioner workflow handoff) → Phase 5+ second-multi-practitioner-deployment-surface signal; cross-DR cumulative REVISION-flavored count (1 here + 2 in `arch/specialist-skill.md` DR = 3) flagged for Coherence-audit C2 evaluation of 3-tier discriminator codification

## 9. Files touched

Wave 1 (this DR commit + ARCH topic; commit `7ffe93a`):
- `arch/practitioner.md` (NEW; primitive-cluster 12+5 ARCH topic; Pattern C topic-template-class anchor)
- `docs/decisions/practitioner-arch-topic.md` (THIS file; composite DR; Mode 2 sub-decisions)

Cascade Wave 2 (single tightly-coupled commit per `MAINTENANCE.md` cascade discipline; following `arch/specialist-skill.md` DR §9 Wave-2 cascade pattern precedent):

**A. GLOSSARY downstream cascade**:
- `glossary/practitioner.md` See section update (placeholder text replaced with anchored `arch/practitioner.md` reference per Phase 3.5 second primitive-cluster lock; parallel to glossary/specialist.md Wave-2 cascade per Note 56)
- `glossary/authority-binding.md` See section reciprocal mention (added `arch/practitioner.md` §4 + §14 — practitioner-record as human authority bound to claim_made / signature_applied events; per-shape trust model parameterizes practitioner-record's accountability surface per `arch/audit.md` §14)

**B. Peer ARCH §19/§17 reciprocal back-mentions** (Lens 6 reciprocal symmetry; per Note 56 specialist-skill Wave-2.5 quad-closure precedent):
- `arch/substrate.md` §19 (added `arch/practitioner.md` reference — substrate Surface §C permission flow records practitioner identity at HITL approval moments per R-CC-4; practitioner-record activation integrates within substrate-phase 3 adapter bindings load step per `ARCHITECTURE.md` §6 composite boot subsection per practitioner §13)
- `arch/audit.md` §19 (added `arch/practitioner.md` reference — per-event actor declaration via Surface §A records practitioner identity for human-actor events; per-shape audit emission granularity per §14 composes through practitioner-record per practitioner §4; cross-practitioner audit-trail query pattern via Surface §C query API per practitioner §4 R-CC-7)
- `arch/adapter.md` §19 (added `arch/practitioner.md` reference — W2 Identity-class adapter Surface candidate per practitioner §14 watch-list; per archived `governance-and-identity-sourcing.md` decision 2 native-vs-adapter mode pattern; framework-baseline-vs-shape-extension partition pattern per adapter §3 currently 5 classes; Identity = 6th-class candidate awaiting concrete adapter implementation surface)
- `arch/sparring.md` §19 (added `arch/practitioner.md` reference — practitioner is engagement subject of sparring per axis-2 cross-axis composition; sparring engagement events `actor_kind: ai_runtime` AI sparring-partner compose with practitioner-record per per-shape activation matrix per sparring §14; production-phase substrate for engaged-authorship per `glossary/engaged-authorship.md`)
- `arch/specialist-skill.md` §17 (forward-reference upgraded to backward-reference per Note 56 cleanup discipline — practitioner-reference recasts from "Forward-references to future Phase 3.5 topics" to "Phase 3.5 second primitive-cluster LOCKED"; cross-specialist activation actor binding back-link per R-CC-9 — when specialist activates mid-session per §5, the activating actor (workspace-runtime activator per §7 `specialist_activated` event-kind) is the practitioner-RECORD bound to current session per practitioner §4 composition table cross-specialist activation actor binding row)

**C. ARCHITECTURE.md updates**:
- `ARCHITECTURE.md` §7 NEW lock entry: "Practitioner ARCH topic (Phase 3.5 second primitive-cluster) — LOCKED" (positioned after specialist-skill entry, before Phase 3.1 closed entry; covers Pattern C topic-template-class anchor + bipartite HUMAN cross-cutting + RECORD Owner B + 11-field manifest schema + multi-practitioner cardinality matrix + legal-entity workspace context placement at WORKSPACE level + lifecycle 4-event-kind catalog + archival-as-default deactivation per cross-pattern coherence with specialist-skill §13 + W1-W4 watch-list + composes-with substrate §C + audit §A/§C + adapter (W2) + sparring + specialist-skill (R-CC-9 back-link) + authority-binding mechanism + cross-axis composition axis-1/2/3)
- `ARCHITECTURE.md` §2 Phase 3 sub-phase status table row 3.5 update (reflects second primitive-cluster LOCKED — practitioner; Pattern C topic-template-class anchor; 4 primitive-cluster + cross-cutting integrator topics remain)
- `ARCHITECTURE.md` §3 Doc structure status table update (4 of 11 → 6 of 11 drafted: substrate / adapter / sparring / audit / specialist-skill / practitioner)

**D. MAINTENANCE.md Layer 3 Primitive-cluster topic template subsection**:
- Per-topic section count expectation row updated for practitioner: marked as ANCHOR for Pattern C topic-template-class; "12 common + 2 conditional applies (§8 + §13) + 3 N/A documented (§9 + §10 + §11) + §12 N/A-parity = 18 total per `arch/practitioner.md` (375 lines)"
- Per-pattern conditional applicability bullet updated: Pattern C bipartite clusters marked as ANCHOR per `arch/practitioner.md`; "granularity / bundle / marketplace N/A documented explicitly; cross-shape policy variation + per-primitive lifecycle ordering APPLIES; 12+5 template extends WITHOUT variation"

**E. BACKLOG.md cascade**:
- Phase 3.5 row resolution: practitioner topic marked RESOLVED with cluster commits 7ffe93a (Wave-1) → Wave-2 cascade commit hash + execution-pattern signal + DR + profile-cluster validation citations + HANDOFF Note 57 forward-reference
- Phase 5 ROADMAP entries added: "Multi-tenant federation practitioner identity" (W1) + "Cross-practitioner workflow handoff mechanics + per-shape policy variation" (W4)
- Phase 6 watch-list entries added: "Adapter-mode practitioner-RECORD + Identity-class adapter Surface candidate" (W2 + adapter §3 6th-class) + "Practitioner-record signing mechanism for historic-claim defensibility" (W3 + audit §D)
- Cross-cutting "3-tier REVISION/EXPANSION discriminator codification" watch-list cumulative count update (3 REVISION-flavored EXPANSIONS across 2 cluster-executions: specialist-skill = 2 + practitioner = 1; trip threshold reached for cumulative-count signal but USER pushback / cascade-work-lag signals NOT yet materialized; flag for Coherence-audit C2 evaluation post-Phase-3.5 close)

**F. T3-1 cleanup**: DR §3 phrasing fix on substrate §8 reference (per Wave-1 Reviewer T3-1 — current "+ §8 (dual-emission for practitioner-attribution events)" sharpened to "+ §8 (dual-emission paths apply when practitioner-attribution events flow through both substrate-internal AND skill-side emission)")

**G. THIS amendment**: DR §9 Files touched section enumeration (this amendment per cascade discipline auditability; following Note 56 specialist-skill DR §9 Wave-2 cascade-scope pattern precedent)

## 10. Revisit triggers

- **W1 signal arrives** (Tier 3 cross-org federated deployment OR `arch/audit.md` §15 W5 federated audit-trail signal): cross-tenant practitioner identity isolation mechanics + cross-org attribution chain semantics design fires; SD-2 manifest schema amendment for federation fields; SD-5 cross-axis composition amendment for federated authority-binding
- **W2 signal arrives** (concrete adapter implementation surface — Personio / Microsoft Entra / Coolify SSO / BambooHR): per-class Identity Surface design fires per `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition; SD-2 manifest schema mode + adapter_binding fields validate against concrete adapter implementation; 6th-class adapter Surface candidate per `arch/adapter.md` §4 per-class enumeration (instance-driven trigger per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` pattern)
- **W3 signal arrives** (Phase 6 `arch/audit.md` §D integrity verification + cryptographic-signature implementation): practitioner-record signing format design fires; SD-2 manifest schema amendment to add signing field; integrates with `signing_authority` field per §2.2
- **W4 signal arrives** (second multi-practitioner deployment surface): per-shape cross-practitioner-handoff mechanics design fires; SD-3 cross-practitioner composition rules amendment for handoff implementation mechanics; SD-4 deactivation policy amendment for cross-practitioner-handoff at deactivation specifics
- **Future primitive-cluster topic creation** (Phase 3.5 `arch/workflow-work-unit.md` / `arch/claim-defensibility.md`): validates 12+5 template extension per SD-1; if Pattern C-specific 6th conditional candidate surfaces (e.g., Pattern C bipartite-aspect-articulation conditional), MAINTENANCE.md Layer 3 §3 amendment per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` instance-driven trigger pattern
- **Phase 6 spec creation**: PractitionerRecord Pydantic schema may surface architectural amendments (~10-20% Phase 1 → Phase 2 architectural flow-back per `decision-design-sharpening` §Phase 1 → Phase 2 transition)
- **Coherence-audit C2** (post-Phase-3.5 close): primitive-cluster set audited at phase boundary; cross-primitive coherence verified across specialist-skill + practitioner + workflow-work-unit + claim-defensibility + scope-model; cumulative REVISION-flavored count (1 in this composite + 2 in `arch/specialist-skill.md` DR = 3 cross-DR cumulative) evaluated for 3-tier discriminator codification per BACKLOG watch-list
