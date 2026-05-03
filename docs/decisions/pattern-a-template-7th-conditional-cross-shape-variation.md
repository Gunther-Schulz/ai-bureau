# Decision record: Pattern A protocol topic template — 7th protocol-specific-conditional section "Cross-shape policy variation"

**Status**: ACCEPTED. 1-round sharpening (full monty + user-locked en bloc).

**Owner**: Doc-system maintenance (Layer 0 governance work; per `MAINTENANCE.md` "When this doc itself changes" discipline).

**Related**:
- `docs/decisions/doc-organization-templates.md` Lock 1 (Pattern A protocol topic template — this DR adds a 7th conditional; preserves Lock 1 composite-historical-integrity rather than amending in place)
- `docs/decisions/doc-organization-templates.md` Lock 2 (DR template applied to this DR)
- `MAINTENANCE.md` Layer 3 description (canonical template surface; amended in this cascade)
- `arch/substrate.md` (anchor Pattern A topic; documents §14 N/A explicitly per shape-uniform substrate Surface)
- `arch/adapter.md` (second Pattern A topic; §13a appendix-slot precedent question relocated to canonical §14 in this cascade)
- `glossary/shape.md` (cross-reference added)
- `disciplines/10-greenfield-evaluation.md` Lens 5 v0.2.1 (provenance hygiene constraint applied throughout)
- `profiles/G-composability-gate.md` line 157 (cross-shape consumption framing — basis for new §14)
- `profiles/L5a-planner-pbs-schulz.md` line 90 (active adapters under practitioner-shape mandates)
- `profiles/L8-auditor-reviewer-posthoc.md` line 29 (audit-trail integrity / coherence-audit perspective)
- `HANDOFF.md` Note 52 (trigger context: Cascade-Reviewer flagged §13a appendix-slot precedent)
- `plugin/skills/decision-design-sharpening/SKILL.md` v0.10.0 (sharpening discipline applied)
- `plugin/skills/coherence-audit/SKILL.md` Lens 5 v0.2.1 (provenance-hygiene constraint extends to 7th conditional template-conformance check)

## Context

Note 52 in `HANDOFF.md` documents a precedent question that surfaced during Phase 3.4 substrate+adapter sub-cluster cascade-execution. Cascade-Writer added a `§13a` appendix-slot to `arch/adapter.md` capturing cross-shape policy variation (4-shape table: practitioner / autonomous-business / personal-OS / federation × audit emission / permission flow / error escalation). The appendix was needed because the content didn't fit Lock 1's 12-required-+-6-conditional template — none of the 6 existing conditional sections describe per-shape policy variation as their applicability axis.

Cascade-Reviewer flagged this ACCEPTABLE-AS-IS for the §13a as already-written, but RECOMMENDED template amendment BEFORE Phase 3.6 quality-gate ARCH topic begins. Three reasons drove the BEFORE-Phase-3.6 timing:

1. **Quality-gate is shape-policy-mediated** — quality-gate Pattern A topic (Phase 3.6) will face the same per-shape variation question as adapter; deferring template amendment forces a second appendix-slot that compounds the precedent problem
2. **Substrate-as-template-anchor work** means precedent matters NOW — substrate is the canonical template anchor; adapter is the second instance; the first surfacing of a 7th conditional should trigger the lock-when-first-instance pattern Lock 1 explicitly anticipated ("future Pattern B / C / cross-cutting integrator topic templates locked when first instance lands")
3. **Sparring + audit reclassified-mechanism-class topics** (Phase 3.4 sub-cluster) approach creation — locking the 7th conditional now means those topics can apply-or-document-N/A at creation rather than retrofitting

Lock 1 itself anticipated this via its closing "future templates lock when first instance lands" clause. The decision is: lock the 7th conditional under that explicit pattern.

## Decision

Add a 7th protocol-specific-conditional section to Lock 1's Pattern A protocol topic template:

**§14 Cross-shape policy variation** — applies when protocol behavior is shape-policy-mediated (audit emission per shape; permission flow per shape; error escalation per shape; or other axes where shape policy bundle declares per-shape variation). Document N/A explicitly when behavior is shape-uniform.

**Canonical numbered slot**: §14 (foundation-up — after §13 deployment-tier-awareness; before pre-implementation operational concerns + watch-list + provenance + phase routing + cross-references which renumber §15-§19).

**Persistence target**: NEW follow-up DR (this file) rather than in-place amendment of Lock 1. Rationale: Lock 1 is a composite ACCEPTED historical record of session-16 sharpening; in-place amendment would erode composite-historical-integrity. New DR preserves Lock 1's history + names this Pattern A template extension as its own decision unit + emits cleanly into MAINTENANCE.md Layer 3 description as canonical surface (the template's authoritative home is MAINTENANCE.md per Lock 1; DRs name decisions, MAINTENANCE.md hosts the template).

**Per-protocol section count expectation update**:
- substrate: 12 common-required + 7 protocol-specific-conditional (anchor; 6 of 7 apply; §14 N/A per shape-uniform substrate Surface) = 18 total content sections + 1 N/A documentation
- adapter: 12 common-required + ~5 conditional (§3 boundary criteria, §10 lifecycle/auth-refresh, §11 per-impl error categories, §14 cross-shape variation; §8 + §12 + §13 N/A) = ~17 total content sections + N/A documentations
- quality-gate (Phase 3.6 forthcoming): 12 common-required + ~3-4 conditional (TBD per topic creation; §14 expected to apply per shape-policy-mediated nature)

**Renumbering cascade**: existing §14-§18 in already-written Pattern A topics (substrate.md + adapter.md) renumber to §15-§19. All internal cross-references within those topics update accordingly in the same cascade commit.

## Sharpening provenance

### Round 1 (full monty + user-locked en bloc)

User raised the precedent question via Note 52 review during main-session decision-design-sharpening invocation. AI surfaced the full sharpening as Round 1:

**Adoption options surfaced + evaluated**:
- Option A (rejected): Leave §13a as appendix-slot in adapter.md only; future per-shape-policy-mediated topics each add their own appendix. Rejected — proliferates appendix-slot pattern; each ARCH topic accumulates ad-hoc structure deviations; defeats template purpose
- Option B (rejected): Amend Lock 1 in place to add §14 conditional. Rejected — Lock 1 is composite ACCEPTED historical record; in-place amendment erodes composite-historical-integrity; Lock 1 explicitly anticipated future-templates locking via separate decisions
- Option C (chosen): New follow-up DR adds 7th conditional + cascades across MAINTENANCE.md Layer 3 description + already-written Pattern A topics + cross-references. Preserves Lock 1; honors Lock 1's "future templates lock when first instance lands" clause

**13 substantive findings surfaced** (Round 1 full monty):

12 EXPANSIONS:
1. Conditional applicability framing names "shape-policy-mediated" as the specific axis (not generic "shape variation" which would be too broad)
2. Document N/A explicitly when shape-uniform — same discipline as 6 existing conditionals
3. Canonical numbered slot §14 (foundation-up: tier-awareness §13 → cross-shape §14 → operational concerns §15)
4. Renumbering cascade applies to substrate.md + adapter.md in same commit
5. Quality-gate (Phase 3.6) inherits slot at creation — no Phase-3.6 retrofit needed
6. Sparring + audit reclassified-mechanism-class topics (Phase 3.4 sub-cluster) apply-or-N/A at creation
7. Per-protocol section count expectation block in MAINTENANCE.md Layer 3 description updates to reflect 12+7
8. Substrate's §14 documents N/A — substrate Surface is shape-uniform per locked GLOSSARY (substrate-emitted events + Surface contracts are shape-neutral; shape policy interprets at shape primitive's domain, not at substrate's)
9. Adapter's §14 promotes §13a appendix to canonical position; drops appendix-slot meta-language per Lens 5 v0.2.1
10. Glossary/shape.md adds cross-reference to template §14 (NOT a new entry per finding 12)
11. Coherence-audit Lens 5 v0.2.1 template-conformance check extends to 7th conditional automatically (Lens 5 references MAINTENANCE.md Layer 3 description as the source-of-truth template)
12. Profile-anchored validation: ≥3 cluster representatives (G + L5a + L8 = Clusters A + C + D) confirms cross-shape policy variation is load-bearing across producer-side artifact design (G), per-archetype operational use (L5a), and audit-trail evaluator side (L8)

1 REVISION-flavored finding:
13. Persistence target chose NEW follow-up DR over Lock 1 in-place amendment — REVISION because it changes the persistence shape that initial framing assumed (initial framing assumed amendment); preserves Lock 1 composite-historical-integrity. ~8% revision rate (1 of 13) within calibration band per skill v0.10.0 (10-20% expected).

### Manufactured-criticism counter-test

Attempted: "Should §14 split into separate conditionals per axis (audit-emission-per-shape / permission-flow-per-shape / error-escalation-per-shape)?" → REJECT (inflates conditional count from 7 to 9; per-axis splitting fragments what is structurally one conditional applicability — shape-policy-mediated; the per-axis enumeration belongs WITHIN §14 content not as separate template sections).

Attempted: "Should 'shape-policy-mediated' become a glossary entry?" → REJECT (per finding 12 — not glossary-grade; it's a derived structural property of certain Pattern A protocols + a per-shape policy-bundle interpretation discipline; fully describable via existing `shape` + `policy` + `mechanism` + `protocol (architectural)` GLOSSARY entries).

### Manufactured-comfort counter-test (per skill v0.10.0)

Position is gate-anchored (G Gate fired for L1-L4 producer artifact = template is producer-side; D Gate fired = defer-instinct rejected because mental modeling resolved cleanly to new-DR persistence target without awaited evidence), not rounds-fatigue. Empirical density check: Round 1 surfaced 13 findings (12 EXPANSIONS + 1 REVISION); no Round 2 needed because (a) all 12 EXPANSIONS are mechanical template-mechanics with no remaining open questions, (b) the 1 REVISION resolved at Round 1 itself via persistence-target sharpening, (c) profile-anchored validation cited specific profile content cleanly, (d) STABLE per Q5 = "all findings are template-mechanics not architectural pivots; new conditional follows established 6-conditional pattern; quality-gate slot ready for Phase 3.6 without re-litigation."

### GLOSSARY back-check (per Round 2 termination — applied at Round 1 termination since no Round 2)

No glossary-grade structural facts surfaced. "Shape-policy-mediated" considered + REJECTED as glossary-grade (per finding 12 + manufactured-criticism counter-test). Migration is template-mechanics, not vocabulary refinement. Clean.

### Profile-anchored validation

Per `decision-design-sharpening` v0.6.0+ Round 2 + `coherence-audit` v0.3.1+ profile-anchored validation discipline. ≥3 cluster representatives read fresh in main session:

| Cluster | Profile | Verdict |
|---|---|---|
| **A — Producers** | `G-composability-gate.md` line 157 ("Cross-shape consumption: practitioner-shape specialist used in personal-OS-shape workspace; shape's policy bundle determines if specialist activates fully or partially") | PASS — cross-shape variation is load-bearing for L1-L4 producer artifact design; template §14 surfaces this at the right architectural moment (producer-side ARCH topic) |
| **C — Consumers** | `L5a-planner-pbs-schulz.md` line 90 ("Active adapters: email (Outlook); LaTeX compile; document signing (qualified electronic signature)" + practitioner-shape mandates throughout) | PASS — pioneer reality grounds per-shape variation as observable concern (practitioner-shape mandates audit emission per claim, fail-closed, HITL on send); §14 surfaces this without leaking pioneer specifics |
| **D — Validators** | `L8-auditor-reviewer-posthoc.md` line 29 ("Audit-trail integrity: workspace audit-trail must survive intact across deployments / migrations" + per-claim defensibility resolution) | PASS — auditor reads unified event stream per shape's policy interpretation; §14 surfaces audit-emission-per-shape as architectural enumeration so coherence-audit can validate template-conformance |

G Gate fired (producer-side artifact for L1-L4 template authors); D Gate fired (defer-instinct rejected — mental modeling resolved cleanly to new-DR persistence target without awaited evidence). Pattern-vs-instance stress-test applied: §14 framing names shape-policy-mediated as the structural property; pioneer-instance specifics (Bauleitplanung/UNB/B-Plan) do NOT leak into §14 content shape.

### Decomposition mode

NOT applicable. Single decision (template-amendment); no sub-decisions. Mode-1 emergent + Mode-2 upfront-known both fire on multi-decision compositions. This decision is atomic at template-mechanics level.

## Composition with existing architecture

- **Lock 1** (`docs/decisions/doc-organization-templates.md`): referenced not amended. Lock 1's "future templates lock when first instance lands" clause is the explicit hook for this DR. Lock 1's Pattern A template definition (12 + 6) is now superseded-by-extension to (12 + 7) via this DR + MAINTENANCE.md cascade
- **MAINTENANCE.md Layer 3 description**: canonical template surface; amended in this cascade to (12 + 7) with new §14 conditional definition + per-protocol section count expectation update
- **arch/substrate.md**: anchor Pattern A topic; documents §14 N/A explicitly per shape-uniform substrate Surface (substrate-emitted events + Surface contracts are shape-neutral per locked GLOSSARY); renumbering §14→§15, §15→§16, §16→§17, §17→§18, §18→§19
- **arch/adapter.md**: §13a appendix-slot relocated to canonical §14 with cleaned framing per Lens 5 v0.2.1 (drops appendix-slot meta-language; pure architectural content); renumbering §14→§15, §15→§16, §16→§17, §17→§18, §18→§19
- **arch/quality-gate.md** (Phase 3.6 forthcoming): slot ready at template creation; no re-litigation needed
- **arch/sparring.md** + **arch/audit.md** (Phase 3.4 sub-cluster reclassified-mechanism-class topics per `ARCHITECTURE.md` §6 Pattern-A/B/C semantics): both topics are already in-corpus (DRAFTED per `ARCHITECTURE.md` §4 catalog rows 3-4); §14 application + §14-§18 → §15-§19 renumbering DEFERRED to the scheduled Phase 3.4 sparring+audit reclassified-mechanism-class sub-cluster v2-audit (per `BACKLOG.md` Phase 3.4); v2-audit re-derives both topics from primitives + bundles §14 application as part of that re-derivation
- **glossary/shape.md**: cross-reference added pointing to MAINTENANCE.md Layer 3 §14 conditional + this DR
- **coherence-audit Lens 5 v0.2.1**: template-conformance check extends to 7th conditional automatically (Lens 5 references MAINTENANCE.md Layer 3 description as source-of-truth)
- **decision-design-sharpening Round-N pattern**: this Round 1 demonstrates skill firing on template-amendment moment (proves skill applicability extends beyond primitive design to template extension)

## Constraints flowing to downstream commitments

- **Future Pattern A topic authors** (Phase 3.4-3.6 + beyond): MUST apply 7th conditional §14 OR document N/A explicitly. Same discipline as 6 existing conditionals
- **Quality-gate ARCH topic** (Phase 3.6): inherits §14 slot at template-creation moment; expected to apply (per shape-policy-mediated nature of quality-gate enforcement — practitioner-shape fail-closed; autonomous-business fail-open with alert; personal-OS fail-open)
- **Sparring + audit reclassified-mechanism-class topics** (Phase 3.4 sub-cluster): apply-or-document-N/A at creation moment
- **8th-conditional candidates** (future Pattern A topic surfaces a NEW recurring conditional axis not in current 7): trigger lock-when-first-instance-surfaces pattern per Lock 1 + this DR (instance-driven trigger)
- **MAINTENANCE.md Layer 3 description** is the single canonical home for Pattern A protocol topic template; cascade-fix any future template-conformance check against this single surface

## Files touched

- `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md` (this file; NEW; status ACCEPTED)
- `MAINTENANCE.md` — Pattern A protocol topic template description amended: 12+6 → 12+7; new §14 conditional definition + applicability framing; per-protocol section count expectation block updated
- `arch/substrate.md` — new §14 documenting N/A explicitly + renumbering §14→§15 through §18→§19 + internal cross-reference updates
- `arch/adapter.md` — §13a appendix-slot promoted to canonical §14 with cleaned Lens-5 framing + renumbering §14→§15 through §18→§19 + internal cross-reference updates (including §7 composition table row referencing §14)
- `glossary/shape.md` — cross-reference addition to MAINTENANCE.md Layer 3 §14 conditional + this DR

## Revisit triggers

- **New Pattern A topic surfaces 8th conditional candidate**: cross-tier-cross-shape interactions; cross-protocol coordination semantics; or some other recurring axis not in current 7. Trigger: same lock-when-first-instance pattern per Lock 1 (new follow-up DR + MAINTENANCE.md cascade + retrofit applicable already-written topics)
- **Phase 3.6 quality-gate work invalidates §14 applicability framing**: if quality-gate's per-shape variation reveals that "shape-policy-mediated" framing under-specifies (e.g., needs explicit per-axis-axis sub-conditionals), trigger DR amendment to sharpen framing
- **Future GLOSSARY refinement to "shape-policy-mediated" as standalone vocabulary**: currently NOT glossary-grade per Round 1 finding 12; revisit if practice surfaces it as load-bearing distinction across multiple Pattern A protocols + 2+ DRs cite it as load-bearing structural fact
- **Pattern B / C / cross-cutting integrator topic templates lock**: per Lock 1 anticipation; cross-shape-variation analog may apply at those template moments; locks per their own first-instance pattern
