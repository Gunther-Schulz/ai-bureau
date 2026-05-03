# Greenfield-rederivation execution — Phase 3.2 doc-organization composite DRs cluster

## Status

ACCEPTED-WITH-FINDINGS — user-reconciliation complete; cascade applied per P1-P10 in single tightly-coupled commit per `MAINTENANCE.md` cascade discipline + `CLAUDE.md` M3 (sub-agent-first cascade).

Audit-pattern: greenfield-rederivation v0.1.0 (`plugin/skills/greenfield-rederivation/SKILL.md`). Per-cluster scope; per-artifact Writer + Reviewer sub-agent dispatch; tiered-divergence verdict scheme; user-decision per divergence.

## Owner

Phase 3 audit family (greenfield-rederivation skill execution; cluster scope). Doc-organization cluster (META work — composite DRs deciding HOW the corpus is organized; not architectural-content primitives).

## Related

- Audit-pattern source: `plugin/skills/greenfield-rederivation/SKILL.md` v0.1.0
- Prior cluster execution (HISTORICAL INPUT only; not authoritative for this execution): `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-1-drs.md` (Phase 3.1 4 DRs cluster; ACCEPTED-WITH-FINDINGS)
- v1 procedure DR (HISTORICAL INPUT only; not authoritative): `docs/decisions/greenfield-rederivation-pause.md` (SUPERSEDED)
- Cluster artifacts under audit:
  - `docs/decisions/phase-3-2-doc-organization.md` (composite — 4 sub-decisions: taxonomy / naming / cross-cutting placement / ARCHITECTURE.md structure)
  - `docs/decisions/doc-organization-templates.md` (composite — arch/<topic>.md template + DR template + memory consolidation rules)
- Composes-with disciplines (`DISCIPLINES.md`):
  - Discipline 1 (source-grounded; skill+profile sub-section)
  - Discipline 6 (foundation-up ordering; complementary to doc-organization decisions)
  - Discipline 9 (coherence-audit cadence; greenfield-rederivation runs at same checkpoint windows)
  - Discipline 10 (greenfield evaluation of archived material; this skill is the per-cluster orchestrated procedure)
- Anchor sources for greenfield derivation (META work — derivation traces through first-principles disciplines, not directly through VISION axes):
  - `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE (framework=mechanisms / shape=policies; A-B-C scope model)
  - `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §§1/2/3
  - `MAINTENANCE.md` 5-layer doc model (Layer 0 anchors / Layer 1 GLOSSARY / Layer 2 ARCHITECTURE / Layer 3 arch topics / Layer 4 DRs / Layer 5 specs)
  - `MAINTENANCE.md` cascade discipline + provenance-hygiene meta-home rule
  - `coherence-audit` Lens 5 v0.2.1 (provenance hygiene) + Lens 8 (pattern-vs-instance) + Lens 9 (VISION-grounding through first-principles transitive chain)
  - `VISION.md` (anchor for axes; doc-organization decisions trace transitively through MAINTENANCE first-principles which themselves serve VISION)
- Profile-cluster coverage planned per artifact: see Sharpening provenance §Wave-1 dispatch table

## Context

The 2 Phase 3.2 doc-organization composite DRs were locked under the same cascade-load conditions identified as a META-failure surface (single-AI execution; oversized mandatory load; cascade-mode adherence collapse). They were both produced before Lens 5 v0.2.1 codification (provenance hygiene) was lifted to first-class discipline status; phase-3-2-doc-organization predates Lens 5 v0.2.1 entirely; doc-organization-templates explicitly references Lens 5 v0.2.1 in its Decision body but was itself produced under cascade-load conditions.

Doc-organization is META work: these DRs decide HOW the corpus is organized (topic taxonomy / naming / placement / templates / memory consolidation), not WHAT primitives exist. Greenfield derivation traces through `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE + 5-layer doc model + first-principles design principles + DISCIPLINES, not directly through VISION axes (the linkage is transitive: VISION serves practitioner outcomes; MAINTENANCE first-principles preserve practitioner outcomes via doc-system shape; doc-organization decisions instantiate MAINTENANCE first-principles).

Cluster choice rationale (per skill §When-to-use cluster examples):
- **Foundation-second**: Phase 3.1 closure was foundational architectural questions; Phase 3.2 closure was foundational doc-system organization. Phase 3.2 sits one layer above Phase 3.1 in foundation-up ordering; auditing it after Phase 3.1 is consistent with Discipline 6 (foundation-up).
- **Smallest-eligible cluster**: 2 composite DRs fits 1 Wave parallel-dispatch comfortably.
- **High-load-bearing-error risk**: doc-organization decisions cascade across the entire corpus. Topic taxonomy decides what arch/* files exist; DR template decides what shape every DR takes; arch template decides what shape every Pattern A protocol topic takes; memory consolidation rules decide what stays in memory vs absorbed-into-DR. Drift in any of these cascades multiplicatively.

What this audit aims to surface (per skill §Reviewer brief — 4 lenses, applied in META context):
- **Pattern-vs-instance leakage**: do these DRs embed PBS-Schulz / DACH-EU / regulatory-instance assumptions in framework-level doc-organization claims?
- **VISION-grounding (transitive)**: does each doc-organization claim trace through MAINTENANCE first-principles disciplines back to VISION axes? META work doesn't trace directly to VISION; intermediate first-principles must be cited explicitly.
- **Provenance hygiene**: do canonical sections (Decision / sub-decisions / templates) contain narrative breadcrumbs ("session N", "AMENDED session N", "as of <date>") that should live in HANDOFF + git log + §Sharpening provenance?
- **Cascade-miss**: are cross-references between the 2 DRs symmetric (each cites the other where dependency exists)? Does doc-organization-templates correctly cascade from phase-3-2-doc-organization (which it depends on for taxonomy + naming)?

## Decision

Wave-1 findings persisted; user-reconciliation phase pending (status remains PROPOSED until reconciliation completes).

### Headline result

**0 T1 (framework-shape-changing) findings. 2 T2 (topic-rewriting) findings — both on doc-organization-templates.md Lock 1 (Pattern A topic template cascade-miss between locked DR and MAINTENANCE.md). ~13 T3 (mechanical edit) findings — concentrated in Lens 5 v0.2.1 self-application gaps + cascade-miss to disciplines/09 + Pareto-improving expansions.**

Core architectural commitments survive greenfield re-derivation under sub-agent + Writer-Reviewer orchestration. The load-bearing finding is **cascade-miss**: MAINTENANCE.md was revised to current 12-required + 6-conditional Pattern A topic template (post-greenfield-rederivation-pause Step 4 cascade), but the source-of-truth DR (`doc-organization-templates.md` Lock 1) was never amended to match. This is exactly the fault mode greenfield-rederivation is designed to catch — drift accumulated under prior cascade-load conditions before M1-M8 + Lens 5 v0.2.1 codification.

### Per-artifact verdict table

| DR | Per-artifact verdict | Tier | Reviewer summary |
|---|---|---|---|
| phase-3-2-doc-organization | GREENFIELD-VALID on substance (4 sub-decisions confirm-locked); NEEDS-REVISION on Lens 5 v0.2.1 provenance breadcrumbs in Status header + Sub-decision 1 body + strikethrough markup in canonical content; NEEDS-REVISION on disciplines/09 cascade-miss (stale 7-Pattern-A claim post-Step-3 amendment) + amendment-list completeness | T3 (×5) | Substance survives; mechanical Lens-5 cleanup + 1 cascade-fix to disciplines/09 |
| doc-organization-templates | GREENFIELD-VALID on Lock 2 (DR template) + Lock 3 (memory consolidation rules); NEEDS-REVISION on Lock 1 (Pattern A topic template cascade-miss vs MAINTENANCE.md current 12+6 structure); NEEDS-REVISION on multiple Lens 5 self-application gaps (Status field + §16 migration breadcrumb) + Pareto-improving expansions (per-protocol section counts; Discipline 10 cross-ref; section-ordering rationale) | T2 (×2 — Lock 1 cascade-miss); T3 (×8) | Lock 1 needs amendment to match MAINTENANCE.md current template; Lock 2/3 substance confirms-locked; ~10 mechanical edits |

### Position commits per divergence (main-session AI commits per `feedback_judgment_and_automate.md`)

#### On phase-3-2-doc-organization.md (Reviewer-1 findings)

**P1 — Lens 5 v0.2.1 provenance breadcrumbs (Status header + Sub-decision 1 body + strikethrough markup)**: REVISE-LOCKED (T3 mechanical). Strip "AMENDED session 17" / "session 16 (2026-05-02); amended session 17 (2026-05-02)" / "(as locked session 16; amended session 17 per greenfield-rederivation cascade)" / strikethrough `~~8 Pattern A protocol topics~~ → **3 Pattern A**` patterns from Status header + Sub-decision 1 body + Constraints flowing section. Replace strikethrough with clean current shape. Keep load-bearing forward-reference "Amended per greenfield-rederivation-pause.md Step 3" without session-N tag. Full amendment narrative stays in §Amendments (the meta-home). Per Lens 5 v0.2.1 strip-vs-keep test: removing breadcrumbs does not confuse a fresh reader's understanding of WHAT THE DECISION IS.

**P2 — disciplines/09 cascade-miss (stale 7-Pattern-A topic catalog)**: REVISE-LOCKED (T3 mechanical; cascade-fix). `disciplines/09-coherence-audit-cadence.md:16` C1 row reads "After 7 Pattern A protocol topics locked (substrate / adapter / sparring / audit / coordination / trust / time)" — stale post-session-17 amendment which reduced Pattern A catalog to 3 (substrate / adapter / quality-gate) + reclassified sparring/audit as mechanism-class + cancelled coordination/trust/time. Update C1 row to reflect current 3 Pattern A + 2 reclassified mechanism-class topics + cancellations.

**P3 — DR amendment cascade-list completeness**: AMEND-LOCKED (T3 mechanical). Add `disciplines/09-coherence-audit-cadence.md` to §Amendments cascade-list in phase-3-2-doc-organization.md (currently missing per CM-B finding).

#### On doc-organization-templates.md (Reviewer-2 findings)

**P4 — Lock 1 Pattern A topic template cascade-miss (LOAD-BEARING T2)**: AMEND-LOCKED (T2 topic-rewriting). Lock 1 currently shows ORIGINAL 18-section flat list; MAINTENANCE.md `:226-267` has REVISED 12-required + 6-conditional template (post-greenfield-rederivation-pause Step 4). Amend Lock 1 to match MAINTENANCE.md current structure: 12 required sections (in foundation-up order: topic scope+frontmatter / Surface contract / per-implementation aspect / Selection mechanics / tri-aspect reconciliation / Composition with framework primitives / Cardinality+lifecycle / Pre-implementation operational concerns forward-ref / Watch-list / Decision-design provenance INPUT-only / Phase routing / Cross-references) + 6 protocol-specific-conditional sections (common-surface boundary / substrate-internal-vs-skill-side mechanics / Boot+shutdown phase ordering / per-protocol error categories / transport variation+per-tier mapping / deployment-tier awareness). Add §Amendments entry tracking the cascade-miss closure. Source-DR-as-canonical-decision-record discipline: DR reflects current locked template, not original-then-stale 18-section list.

**P5 — Section naming generalization (cascades from P4)**: AMEND-LOCKED (T3 mechanical). Rename Lock 1 §8 from "Substrate-internal vs skill-side audit emission" (substrate-specific) to general Pattern-A wording per MAINTENANCE.md `:256` ("Substrate-internal vs skill-side mechanics"). Rename §11 from "Substrate error categories" to "Per-protocol error categories" per MAINTENANCE.md `:258`. Generalization required for Pattern-A-pluralism (multiple protocols beyond substrate use the template).

**P6 — Lens 5 v0.2.1 self-application failure in Status field**: REVISE-LOCKED (T3 self-application). Strip "session 16 (2026-05-02); 2-round generic sharpen (per `plugin/skills/sharpen/SKILL.md` v0.9.0) on the proposal itself; user-authorized execution" from Status `:3`. Move sharpening-tool reference (`sharpen v0.9.0` + 2-round) to §Sharpening provenance (the canonical meta-home). Strip date+session+narrative breadcrumbs entirely (live in HANDOFF + git log). Self-application: this DR codifies provenance hygiene; its own Status must satisfy the rule it codifies.

**P7 — §16 migration-trajectory breadcrumb strip**: REVISE-LOCKED (T3 mechanical). Strip "(archived sources only; **meta-provenance moves to DR**)" parenthetical from Lock 1 §16 Decision-design provenance section name. "Meta-provenance moves to DR" is migration-trajectory (where it WAS vs WHERE IT IS); fresh reader doesn't need this to understand WHAT THE SECTION IS. Keep clean "Decision-design provenance (INPUT-citation only)".

**P8 — Per-protocol section count expectations sync**: AMEND-LOCKED (T3 Pareto-improving expansion). Lock 1 currently silent on per-protocol section count expectations; MAINTENANCE.md `:262-265` provides per-protocol counts (substrate = 18 = 12 required + 6 conditional; adapter = 15-16 = 12 required + 3-4 conditional; quality-gate = 13-14 = 12 required + 1-2 conditional). Sync into Lock 1.

**P9 — Add Discipline 10 cross-reference**: AMEND-LOCKED (T3 mechanical; cascade-symmetry). Add `disciplines/10-greenfield-evaluation.md` to Lock 2 §16 Related list. Discipline 10 (`disciplines/10-greenfield-evaluation.md:33`) explicitly extends Lens 5 v0.2.1 to ARCH topics + DR §16 — load-bearing for this DR's own §16 wording rule. Currently missing.

**P10 — Section ordering rationale (Pareto-improving expansion)**: AMEND-LOCKED (T3 Pareto-improving expansion). Lock 1 currently provides flat numbered list with no rationale; Writer derivation surfaces design rationale (foundation-up + reader-cognitive-flow + provenance-meta-home compose). Add rationale prose. Strengthens template-design defensibility without changing content.

**P11 — Memory consolidation 5-target vs 4-target target inventory**: KEEP-LOCKED. Writer derivation includes GLOSSARY as 5th absorption target; locked DR enumerates 4 (DISCIPLINES + MAINTENANCE TOP-LEVEL DESIGN PRINCIPLES + MAINTENANCE TOP-LEVEL SCOPE + ARCHITECTURE cross-cutting). Locked DR captures what actually fired in the session-16 consolidation event; GLOSSARY route is theoretically valid (per primitive-vocabulary absorption) but didn't fire in THIS consolidation. Both legitimate; locked is concrete event-record (HISTORICAL-fact), Writer is broader-rule. Locked stands.

**P12 — Discriminator under-specification**: KEEP-LOCKED. Reviewer flagged Writer derivation as gap-in-Writer (under-specified runtime discriminator); locked DR `:101` provides 3-category discriminator (DISCIPLINE / BEHAVIORAL / architectural-commitment). Writer's derivation gap, not locked drift. Locked stands.

### v1 vs v2 audit comparison + cluster-execution-pair signal

This is the second cluster-execution of v2 greenfield-rederivation skill v0.1.0 (after Phase 3.1 4-DR cluster). Cross-execution signal:

- **Phase 3.1 (4 DRs)**: 0 T1 + 0-2 T2 (borderline) + ~10 T3. Concentrated in Lens 5 + Lens 8 (pioneer-instance leakage).
- **Phase 3.2 (2 DRs)**: 0 T1 + 2 T2 + ~13 T3. T2 finding is cascade-miss (locked DR not amended after MAINTENANCE.md was revised); T3 concentrated in Lens 5 v0.2.1 self-application gaps + cascade-miss to disciplines/09 + Pareto-improving expansions.

**Pattern emerging across both executions**: corpus survives greenfield-derivation chain on substantive architecture (0 T1 in either cluster); drift concentrates in provenance hygiene (Lens 5 v0.2.1 codification post-dates locked artifacts) + cascade gaps (downstream files not updated when upstream amends). M1-M8 mitigations from session 18 close the cascade-load fault surface going forward; the v2 audit campaign closes the legacy fault surface artifact-by-artifact.

**v2 skill empirical-evidence accumulation**: with this execution complete, v0.1.0 has TWO cluster-execution evidence base — meeting the ≥2-execution amendment threshold per skill §Status. v0.1.1 amendments can be considered post-this-execution. Reviewer-1's minor non-blocking observation from Phase 3.1 (section-name "Sharpening rounds metadata" → canonical "Sharpening provenance" normalization) accumulates with this cluster's similar Lens 5 self-application findings — pattern is "Lens 5 v0.2.1 retro-application across pre-codification artifacts."

### User-reconciliation phase (pending)

Per skill §Post-cluster step 2 (decision phase = user approval per `DISCIPLINES.md` working procedure). User decides per P1-P12. Status will transition PROPOSED → ACCEPTED-WITH-FINDINGS post-decision. Cascade execution (P1-P10 if approved) delegated to fresh-context sub-agent per `CLAUDE.md` M3 + skill §Cascade execution.

Verdict scheme reference (per skill §Verdict scheme):

| Per-artifact verdict | Meaning |
|---|---|
| GREENFIELD-VALID | Locked content passes greenfield-derivation chain |
| INPUT-ONLY-VALID | Archive/prior is INPUT not TEMPLATE; greenfield-chain holds |
| NEEDS-REVISION | Specific revision identified |
| NEEDS-REWORK | Substantial redo required |

Tier:
- T1 framework-shape-changing (cascades) | T2 topic-rewriting | T3 mechanical edit | T4 confirms-locked

User-decision verdict per divergence: REVISE-LOCKED / KEEP-LOCKED / AMEND-LOCKED / SUPERSEDE-LOCKED.

## Sharpening provenance

### Wave decomposition

| Wave | Artifacts | Parallelism | Foundation-up dependency |
|---|---|---|---|
| 1 | phase-3-2-doc-organization.md / doc-organization-templates.md | 2 Writers in parallel + 2 Reviewers in parallel | None within cluster — each Writer derives from MAINTENANCE first-principles + 5-layer model + DISCIPLINES + GLOSSARY substrate independently. Cross-DR dependency (templates DR depends on taxonomy DR) lives in MAINTENANCE Layer-3 description + DR-template convention; each derivation runs from primitives. |

Cluster within skill's stated 2-6 artifact / 3-4 parallel sweet spot per `plugin/skills/greenfield-rederivation/SKILL.md` §When-to-use + §Per-Wave step 1.

### Wave-1 Writer dispatch table (planned)

| Artifact | Writer brief profile-cluster coverage | Required reads (skill §Writer brief — adapted for META work) |
|---|---|---|
| phase-3-2-doc-organization.md | A Producers (L1 specialist creator + L2 shape definer + L3 deployment template creator) + D Validators (G + L8) — doc-organization decisions cascade into producer-side artifact structure (Pattern A protocol topics; primitive-cluster topics) + validator-side audit-trail meta-home (DR provenance) | VISION + MAINTENANCE TOP-LEVEL ARCHITECTURE + 5-layer doc model + TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 + cascade discipline + GLOSSARY index + DISCIPLINES Discipline 1 + Discipline 6 + Discipline 9 + Discipline 10 + profiles/INDEX.md + L1 + G + L8 + L4a |
| doc-organization-templates.md | A Producers (L1 + L2 + L3) + D Validators (G + L8) — template decisions cascade into every produced ARCH topic + every DR + memory-vs-DR placement | VISION + MAINTENANCE TOP-LEVEL ARCHITECTURE + 5-layer doc model + TOP-LEVEL DESIGN PRINCIPLES §§1/2/3 + cascade discipline + Lens 5 v0.2.1 provenance hygiene + GLOSSARY index + DISCIPLINES Discipline 1 + Discipline 6 + Discipline 9 + Discipline 10 + profiles/INDEX.md + L1 + G + L8 + L4a |

Each Writer brief explicitly excludes reading the artifact under audit during derivation + excludes reading the peer cluster artifact + excludes reading v1 findings (greenfield-rederivation-pause.md) + excludes reading prior v2 cluster findings (greenfield-rederivation-2026-05-03-phase-3-1-drs.md). Per skill §Sub-agent brief template — greenfield-Writer "DO NOT READ during derivation".

### Wave-1 Reviewer dispatch table (planned)

| Artifact | Reviewer brief inputs | 4 lenses applied |
|---|---|---|
| phase-3-2-doc-organization.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Pattern-vs-instance leakage / VISION-grounding (transitive through first-principles) / provenance hygiene / cascade-miss |
| doc-organization-templates.md | Writer derivation + locked DR + VISION + MAINTENANCE + Discipline 10 + coherence-audit Lens 5 + 8 + 9 | Same 4 lenses (Lens 5 self-application — does this DR's own canonical content satisfy the provenance-hygiene rule it codifies?) |

### Wave-1 dispatch summary (executed)

**Writer wave**: 2 sub-agents dispatched in parallel (single message; 2 Agent tool invocations). Each Writer in fresh context with focused brief (artifact path; required reads list; explicit DO-NOT-READ list including artifact-under-audit + peer cluster artifact + v1 findings + prior v2 cluster findings + ARCHITECTURE.md §4 + arch/* + memory/*). Each Writer derived greenfield content for the artifact's stated scope (4 sub-decisions for phase-3-2; 3 locks for doc-organization-templates) from MAINTENANCE first-principles + 5-layer doc model + DISCIPLINES + GLOSSARY substrate + ≥3 cluster-relevant profile files. Both Writers returned greenfield-derivation summaries with file:line citations + Ralph self-check confirmation + explicit synthesis-vs-citation flagging.

**Reviewer wave**: 2 sub-agents dispatched in parallel against respective Writer outputs (sequenced after Writer wave; Reviewer needs Writer derivation as input). Each Reviewer in fresh context with brief (locked-artifact path + inline Writer derivation + 4-lens framework: Lens 5 v0.2.1 provenance hygiene + Lens 8 pattern-vs-instance + Lens 9 VISION-grounding transitive + cascade-miss). Each Reviewer produced per-element verdict table + tier per finding + recommendation per finding + Ralph self-check confirmation. Reviewer-2 (doc-organization-templates) surfaced the load-bearing T2 cascade-miss between locked DR and MAINTENANCE.md current template.

### Per-sub-agent Ralph self-check verification (per skill §Termination criteria)

| Sub-agent | Required-reads complete | Discipline 10 applied | Avoided locked-artifact / peer-cluster / v1-findings / downstream reads | Cited specific MAINTENANCE/GLOSSARY/VISION refs |
|---|---|---|---|---|
| Writer-1 (phase-3-2-doc-organization) | ✅ | ✅ | ✅ | ✅ (50+ citations; transitive grounding for META work explicit) |
| Writer-2 (doc-organization-templates) | ✅ | ✅ | ✅ | ✅ (50+ citations; Lens 5 self-application discipline applied to derivation output) |
| Reviewer-1 (phase-3-2-doc-organization) | ✅ (locked + Writer + lenses) | n/a (Reviewer applies lenses) | n/a (Reviewer reads locked) | ✅ |
| Reviewer-2 (doc-organization-templates) | ✅ (locked + Writer + lenses + MAINTENANCE current template) | n/a | n/a | ✅ |

**Main-session Ralph self-check** (per skill §Ralph self-check at apparent completion + `CLAUDE.md` M7):
- Read SKILL.md fresh at invocation: ✅
- Each Writer + Reviewer Ralph self-check confirmed at completion: ✅ (4/4)
- Avoided executing greenfield-derivation in main session: ✅ (orchestrator role only)
- Dispatched Reviewer separate from Writer per artifact: ✅ (2+2 in fresh contexts)
- Persisted Wave-1 findings to per-execution DR before next Wave: ✅ (this commit; single Wave for this 2-artifact cluster)
- Cascade-execution discipline preserved: pending user-reconciliation; cascade delegated to fresh-context sub-agent per M3 + skill §Cascade execution
- Provenance-hygiene check on this DR: ✅ (Decision section holds shape-only verdict claims; trajectory + Wave dispatch summary in Sharpening provenance per `MAINTENANCE.md:288`; no session-N breadcrumbs in canonical content)

### Decomposition mode

Mode 2 upfront-known composite (per `decision-design-sharpening` v0.6.0): 2 tightly-coupled doc-organization composite DRs identified at cluster definition time (not emergent from drift). Both Phase 3.2-era; both composite Mode-2 sub-decision DRs themselves; both subject to same META-failure-surface conditions.

## Composition with existing architecture

- **Coherence-audit composition**: this audit catches per-artifact derivation drift / cargo-cult / instance-leakage / cascade-miss in doc-organization decisions; coherence-audit catches set-level + vocabulary-level + cascade-level drift via 10 universal lenses. Both compose at phase boundaries (per skill §Composition with other PBS dev skills). This execution is per-cluster (greenfield-rederivation territory); set-level lens scan over the whole doc-system would compose as separate coherence-audit invocation.
- **Cascade discipline**: any user-approved REVISE-LOCKED divergence triggers cascade per `MAINTENANCE.md` TOP-LEVEL RULE (UPSTREAM + DOWNSTREAM + SIDEWAYS); cascade execution itself delegated to fresh-context sub-agent per `CLAUDE.md` M3.
- **Phase 3 sub-phase status**: Phase 3.2 marked CLOSED in `ARCHITECTURE.md` §2 with composite DR amended per v1 procedure cascade (Pattern A catalog 14→11; Pattern A protocol catalog 8→3; sparring + audit reclassified as mechanism classes; coordination + trust + time cancelled). This v2 audit re-tests that closure under sub-agent + Writer-Reviewer orchestration to surface any drift the original closure + amendment cascade missed under cascade-load conditions.
- **v2 skill empirical-evidence accumulation**: this is the second cluster-execution of v2 greenfield-rederivation skill v0.1.0. Per skill §Status (preliminary-locked at v0.1.0; ≥2 cluster-executions threshold for amendment), completion of this execution moves the skill from single-execution-evidence to two-execution-evidence — the empirical threshold for skill v0.1.1 amendment review.

## Constraints flowing to downstream commitments

User-reconciliation complete. Cascade applied per position commits P1-P10 in single tightly-coupled commit:

- **P1** (REVISE-LOCKED, T3 Lens 5 v0.2.1 cleanup) → `docs/decisions/phase-3-2-doc-organization.md` Status header / Locked-line / Sub-decision 1 body / Constraints flowing section: stripped session-N + AMENDED-session-N + amendment-narrative breadcrumbs + strikethrough markup; replaced with clean current-shape claims; load-bearing forward-reference to greenfield-rederivation-pause Step 3 retained per Lens 5 v0.2.1 strip-vs-keep test
- **P2** (REVISE-LOCKED, T3 cascade-fix) → `disciplines/09-coherence-audit-cadence.md:16` C1 row: 7-Pattern-A-topic claim → 3 Pattern A + 2 reclassified mechanism-class ARCH topics + cancellation note; "Why this cadence" 5-of-7 reference also updated
- **P3** (AMEND-LOCKED, T3 cascade-list completion) → `docs/decisions/phase-3-2-doc-organization.md` §Amendments: added `disciplines/09-coherence-audit-cadence.md` to cascade-related file changes list
- **P4** (AMEND-LOCKED, T2 LOAD-BEARING cascade-miss) → `docs/decisions/doc-organization-templates.md` Lock 1: rewrote 18-section flat list to canonical 12 common-required + 6 protocol-specific-conditional structure per `MAINTENANCE.md:226-267`; included anchor + greenfield-tested provenance note; future Pattern B/C clause preserved
- **P5** (AMEND-LOCKED, T3 generalization; folded into P4) → Lock 1 §8 "Substrate-internal vs skill-side audit emission" → "Substrate-internal vs skill-side mechanics"; §11 "Substrate error categories" → "Per-protocol error categories"
- **P6** (REVISE-LOCKED, T3 Lens 5 self-application) → `docs/decisions/doc-organization-templates.md` Status field: stripped session-N + sharpen-tool-reference narrative; replaced with clean "ACCEPTED."; sharpen v0.9.0 + 2-round reference preserved in pre-existing §Sharpening provenance (canonical meta-home)
- **P7** (REVISE-LOCKED, T3 migration-trajectory strip; folded into P4) → Lock 1 §16 "Decision-design provenance" header parenthetical changed from "(archived sources only; meta-provenance moves to DR)" → "(INPUT-citation only)"
- **P8** (AMEND-LOCKED, T3 Pareto-improving expansion; folded into P4) → Lock 1 per-protocol section count expectations added: substrate=18 (12+6) / adapter=15-16 (12+3-4) / quality-gate=13-14 (12+1-2)
- **P9** (AMEND-LOCKED, T3 cross-ref completion) → `docs/decisions/doc-organization-templates.md` top-level Related list: added `disciplines/10-greenfield-evaluation.md` cross-reference
- **P10** (AMEND-LOCKED, T3 Pareto-improving expansion; folded into P4) → Lock 1 added section-ordering rationale paragraph (foundation-up + reader-cognitive-flow + provenance-meta-home composition)
- **Cascade-flowing edit** (cascades from P4) → Lock 1's "Future ARCH topic content" constraint also updated from "18-section template" reference → "two-tier template (12 common-required + 6 protocol-specific-conditional)"

Cascade discipline preserved: single tightly-coupled commit; all cascaded files + per-execution DR status transition + this Constraints flowing summary in same commit; no main-session bypass of `CLAUDE.md` M3 sub-agent-first routing.

## Files touched

- `docs/decisions/greenfield-rederivation-2026-05-03-phase-3-2-doc-organization.md` (this DR — Status: PROPOSED → ACCEPTED-WITH-FINDINGS; Constraints flowing populated with concrete cascade-applied summary; Files touched populated)
- `docs/decisions/phase-3-2-doc-organization.md` (P1 + P3 cascade — Status header + Sub-decision 1 body + Constraints flowing + §Amendments cleanup)
- `disciplines/09-coherence-audit-cadence.md` (P2 cascade — C1 checkpoint row + "Why this cadence" updated for current Pattern A topic catalog)
- `docs/decisions/doc-organization-templates.md` (P4 + P5 + P6 + P7 + P8 + P9 + P10 cascade — Status field cleanup + Related list expansion + Lock 1 rewrite to two-tier template + Constraints flowing template-shape correction)

## Revisit triggers

- New artifact added to Phase 3.2 cluster (none expected; Phase 3.2 closed)
- Stable-corpus signal: if 0 NEEDS-REVISION + 0 NEEDS-REWORK across all 2 artifacts (only T4-confirms-locked findings) → cluster greenfield-stable; cadence shifts to delta-audits per `coherence-audit` audit-scaling
- User-flagged drift on cluster artifact post-execution (e.g., new evidence surfaces during Phase 3.5 or 3.6 work that contradicts Phase 3.2 lock)
- Phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` (e.g., Phase 3.4 close C1 audit may compose with this re-audit)
- Lens 5 v0.2.1 amendment OR new provenance-hygiene rules emerge — re-audit doc-organization-templates against amended discipline (the DR's own canonical content must self-satisfy)
