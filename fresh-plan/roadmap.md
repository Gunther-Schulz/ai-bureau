# fresh-plan roadmap

Canonical map of phases, workstreams, and current status. This is the execution tracker — what work exists, what's done, what's next.

For framework orientation, see `CONCEPTS.md`. For session procedure, see `README.md`. For architectural decisions, see `decisions.md`. For adversarial stress-testing discipline, see `probing.md`.

Source-of-truth for each workstream's *definition* is the cited D-entry. This file *mirrors* status; D-entries are canonical for content. New workstreams added here BEFORE work begins to avoid the "we did work that wasn't on the tracker" pattern.

## Phases at a glance

| Phase | Description | Status |
|---|---|---|
| A | Layer 3 (formal schemas + extension protocol + composition rules + versioning) | DONE (closed at D35) |
| B | Reference impl of core | IN PROGRESS (impl side complete; Bref refinement workstream active) |
| C | Standards-compat impl (real-wire A2A peer adapter + MCP server adapter + integrity-protocol extensions) | NOT STARTED |
| D | Pioneer-instance (PBS-Schulz practitioner-shape) | NOT STARTED |
| E | Multi-deployment validation (second shape impl + federation begins) | NOT STARTED |
| F+ | Refinement / optimization / ecosystem | INDEFINITE |

Phase boundaries are trigger-based, not schedule-based (per D26). Order is indicative, not rigid.

---

## Phase A — DONE

Closed at D35. Refined by D34. Sharpened by D37-D40 side-quest batch.

| # | Workstream | Status | Source |
|---|---|---|---|
| 1 | Notation (JSON Schema Draft 2020-12) | DONE | D28 |
| 2 | Extension manifest contract + validation flow | DONE | D29 |
| 3 | Per-kind formal schemas (15 schemas) | DONE | D27 + D34 §A.8 |
| 4 | Composition rules (referential integrity + boot-time resolution + `extends` removal) | DONE | D30 + D31 + D32 |
| 5 | Promotion / demotion + versioning | DONE | D33 |
| - | Refinement pass | DONE | D34 |
| - | Closure entry | DONE | D35 |

---

## Phase B — IN PROGRESS

Per D36 (Phase B planning) + D41 (B2b two-substrate parity) + D42 (Bref formalization).

### Implementation workstreams — DONE

| # | Workstream | Status | Source |
|---|---|---|---|
| B1 | Conformance validator | DONE | D36 |
| B2 | In-process substrate (+ followon-1 + followon-2) | DONE | D36 |
| B2b | MS Agent Framework substrate stub | DONE | D41 |
| B3 | Generic minimal shape | DONE | D36 |
| B4 | Stub MCP-server-protocol adapter | DONE | D36 |
| B5 | Stub direct-api adapter | DONE | D36 |
| B6 | Generic minimal specialist | DONE | D36 |
| B7 | RAG-via-MCP impl | DONE | D36 |
| B8 | End-to-end scenario (D36 §C closure-criterion items 1-6 satisfied) | DONE | D36 §C |

168 tests pass. Implementation discipline locked.

### Bref — IN PROGRESS (Phase B refinement workstream per D42)

Originally tracked 7 deliverables at D42 lock-time. **Scope expanded mid-Bref** by the slot-interpretation audit (run as part of Bref deliverable processing; surfaced 24 SUSPECT slots and the underlying discipline gap that motivated `probing.md`).

**Original 7 tracked deliverables:**

| # | Deliverable | Status | Output |
|---|---|---|---|
| 1 | D39 out-of-band-state tensions | DONE (impl-side closure) | Will record in Bref output §A |
| 2 | D17 capability-vocabulary sharpening | DONE | D43 (supersedes D17 — rename `event-streaming` → `event-chain`) |
| 3 | D37 subscriber-dispatch reentrancy / loop semantics | DONE | D44 (extends D37 — queued FIFO + loop backstop) |
| 4 | D19 activation-scope DSL design | NOW PART OF SLOT PASS | Deferral entry candidate (~D45 if standalone, OR folded into slot-pass output) |
| 5 | D33 migration-safety discipline for shape versioning | NOT STARTED | TBD |
| 6 | D38 Sana-style worked-example validation | NOT STARTED | TBD |
| 7 | `decisions.md` split into per-entry files | NOT STARTED (mechanical, last) | TBD |

**Added to Bref scope mid-pass via slot-interpretation audit (2026-05-12):**

| # | Deliverable | Status | Output |
|---|---|---|---|
| 8 | `probing.md` adversarial stress-testing discipline (foundation) | DONE | `probing.md` (5 procedures) |
| 9 | `roadmap.md` canonical execution tracker | DONE | `roadmap.md` (this file) |
| 10 | Slot interpretation-layer pass (process 24 SUSPECT slots) | NOT STARTED | Mix of cheap labels + ~4-6 substantive D-entries (see breakdown below) |
| 11 | One additional adversarial audit (combined failure-mode coverage + abandonment-path) | DONE (2026-05-12) | **33 SUSPECT findings** on ~38 audited surface (more findings per surface than slot-interpretation's 24-of-78). Cross-category overlap → systemic pattern, not isolated gaps. Forced **bounded-fill plan revision** (pending next session) + **probing.md amendments** (5 edits landed; audit findings count tracking added to discipline evolution). See "Bounded lock-and-fill plan — REVISION PENDING" below. |
| 12 | probing.md amendments (5 edits) based on audit (c) findings | DONE | FAILS field strengthened with D44 triad pattern; new detection-surface-recovery audit shape; standing checkpoint cadence (failure-mode + abandonment-path now standing, not rotating); empirical calibration data point added; audit findings count tracking in evolution rules |
| 13 | D45 meta-foundation entry — detection-surface-recovery triad as standing requirement for runtime decisions | DONE | D45 (substantive; meta-foundation). Locks the pattern; pre-lock probe SKIPPED with documented reason (audit-driven entries are circular to re-probe; precedent for future audit-driven entries). Casts net over ~25-28 of 33 SUSPECTs via the cluster supersedes entries below. |
| 14 | Boot-procedure cluster supersedes entry | NOT STARTED | Apply D45 triad to boot path: silent ValueError swallowing (steps 6/7/8) + manifest-actor seeding rollback (introduced in D39 closure) + capability-only substrate-binding error path. ~D46 candidate. |
| 15 | Subscriber-dispatch cluster supersedes entry | NOT STARTED | Apply D45 triad to dispatch path: on_event exception silently swallowed + HookRegistry.fire integration site (hooks never invoked; D13 hook contract is decorative until firing-sites land). ~D47 candidate. |
| 16 | Adapter cluster supersedes entry | NOT STARTED | Apply D45 triad to adapter path: adapter call() failure shape unspecified + adapter binding mid-boot failure (root cause lost). ~D48 candidate. |
| 17 | Specialist cluster supersedes entry | NOT STARTED | Apply D45 triad to specialist path: handle_skill failure shape + on_event exception (composes with deliverable 15). ~D49 candidate. |
| 18 | Validation cluster supersedes entry | NOT STARTED | Apply D45 triad to validation path: D30 §4 per-work-unit identity checks (named in spec, never implemented) + B1 collect-all skipping when extensions empty. ~D50 candidate. |
| 19 | Composition-change cluster supersedes entry | NOT STARTED | Apply D45 triad to composition-change path: post-projection state validity (e.g., adding actor whose subtype contradicts shape's authority-binding) + composition-change shape authority interaction. ~D51 candidate. |

**Slot pass (#10) breakdown** (24 SUSPECT slots from the 2026-05-12 audit):

- ~8 impl gaps (cheap labels — design + spec correct; impl just didn't follow through):
  - `shape.actor-requirements` validation, `shape.optional-capabilities` consumption, `specialist.roles[]` cross-kind check, `event.actors[].role` vocabulary check, `work-unit.payload` validation against work-unit-kind schema, `adapter.declared-event-emissions[]` shape-side consumption, `specialist.declared-event-emissions[]` enforcement, `work-unit.contributing-actors[].role` vocabulary check
- ~3 spec drifts (small ledger notes or schema cleanup — schema added slots without D-entries):
  - `specialist.skills[].input-modalities`/`output-modalities`/`publicly-exposed`, `specialist.skills[].description`, `shape.hooks[].purpose`/`applies-to`
- ~11 design gaps (require substantive D-entries — likely 4-6 entries):
  - `specialist.activation-scope` (interpretation layer + grammar), `shape.authority-bindings[].additional-constraints` (interpretation layer + grammar), `workspace.composition.*.configuration` (D7 silent on slot semantics — 4 instances), `adapter.protocol-or-transport` binding-vs-provision relationship, `workspace.composition.*.version-range` precedence semantics, `substrate.runtime-shapes[]` runtime semantics, `work-unit.lifecycle.started-at`/`completed-at` reconciliation with event-derivation, payload-vocabulary registration mechanism (open `what`/`action-name`/`trigger`/`confidence`/`evidence-references`)
- 1 hybrid (HookRegistry.fire integration site) — substantive D-entry; design + impl gap reinforce each other

**Three candidate standalone clarification entries** (opportunistic placement during Bref):

- Actor identity-binding spec slot (D9 + D22 amendment; composes with VC + DID standards-compat work)
- Live in-place shape migration deliberate scope-cut (clarifies `payload-composition-change.binding-kind` enum doesn't include shape)
- Positioning lock (needs source-grounded Bucket A platform reads first — likely deferred)

### Bounded lock-and-fill plan — REVISED 2026-05-12 (process-by-pattern)

**Original plan**: process 24 slot-interpretation suspects, run one additional audit (deliverable #11), re-evaluate. **Status of original plan**: superseded by the process-by-pattern revision below.

**Revised plan (process-by-pattern; locked 2026-05-12 per D45)**:

1. ✅ DONE: D45 meta-foundation entry locks detection-surface-recovery triad as standing requirement for runtime decisions
2. NOT STARTED: 6 cluster supersedes entries (deliverables 14-19) apply D45 triad to specific runtime paths — each casts net over multiple SUSPECT findings
3. NOT STARTED: each cluster supersedes entry pairs with impl follow-throughs (typed exceptions + diagnostic surfaces + recovery paths in the impl)
4. NOT STARTED: slot-pass for the 24 slot-interpretation suspects (deliverable #10) — process in batches; cheap labels for impl gaps + spec drifts; substantive D-entries for design gaps that don't fold into the cluster supersedes
5. NOT STARTED: remaining original Bref deliverables (#5 D33 migration-safety; #6 D38 Sana worked-example; #7 decisions.md split — mechanical, last)
6. NOT STARTED: Bref output entry (analog of D34) consolidating all of the above
7. NOT STARTED: Phase B closure entry (analog of D35)

**Why process-by-pattern (rejected: process-by-suspect)**: the local-over-global failure mode that produced the gaps in the first place would repeat at scale if 57 suspects were processed individually. Pattern-level entries (D45 + cluster supersedes) cast nets and codify the discipline structurally. Per D45's rationale + the discipline-cited-as-label-not-applied-as-check observation from the 2026-05-12 audit.

**Phase B closure pre-condition expanded**: audit (c) revealed structural items that can't responsibly defer to Phase C+:
- HookRegistry.fire() never called (D13 hooks are decorative until firing-sites land) → addressed by deliverable #15 (subscriber-dispatch cluster)
- Specialist on_event exceptions silently swallowed (substrate.py:193-197) → addressed by deliverable #15
- Boot procedure swallows ValueError in steps 6/7/8 (silent degradation) → addressed by deliverable #14 (boot-procedure cluster)
- D30 §4 per-work-unit identity checks named in spec, never implemented → addressed by deliverable #18 (validation cluster)
- Multi-event boot-time actor seeding has no rollback (we just introduced this in D39 closure) → addressed by deliverable #14
- Composition-change post-projection state validity unchecked → addressed by deliverable #19 (composition-change cluster)

Estimated revised scope: **3-5 more sessions** of substantive work (cluster supersedes + impl + remaining Bref deliverables + closure entries).

### Phase B closure entry

Pending Bref completion. Analog of D35 (Phase A closure). Per D42 §"Closure-criterion update for D36 §C": Phase B closes when:

- (a) B8 fixture passes — DONE
- (b) Two-substrate parity per D41 shipped — DONE
- (c) Bref output entry locked — PENDING (waits on Bref deliverables 4-11)

---

## Phase C — NOT STARTED

Per D26 description. Per-phase planning entry (analog of D27/D36) when entered.

**Indicative workstreams** (not yet locked; to be enumerated in Phase C planning entry):

- Real-wire A2A peer adapter (validates D21)
- Real-wire MCP server adapter
- Real-wire substrate impl (Claude Agent SDK or alternative replacing the in-process stub)
- AEGIS / Axon integrity-protocol extensions (per D40 §B; canonical first examples)
- Standards-compat per-kind mappings (PROV-O, CloudEvents, OpenTelemetry, EU AI Act Article 12 audit-record format) — D24 tracker

### Cross-session input pending — standards-compat engagement

Surfaced during Bref session 2026-05-12 (cross-session input from another session): CloudEvents envelope alignment + W3C PROV-DM citation/export. Both already on D24's standards-compat tracker (CONCEPTS line ~142). **Decision deferred** to next session: small standalone clarification entry citing PROV-DM + naming CloudEvents alignment as priority, OR formalize a parallel "standards-compat per-kind mapping" workstream, OR leave on tracker. Lean: small clarification entry + leave heavy work for Phase C planning.

CloudEvents envelope alignment is a D43-class-but-larger rename refactor. NOT a Bref item. Phase C natural home for the actual mapping work. PROV-JSON export adapter is unambiguously Phase C deliverable per D24.

---

## Phase D — NOT STARTED

Per D26 description. Per-phase planning entry when entered.

**Indicative workstreams** (not yet locked):

- Practitioner-shape impl (carries VISION three-axes per D4)
- Domain specialists (planning-document-work, etc.)
- Bauleitplanung corpus integration
- PBS-Schulz workspace manifest
- Cutover from 0.1.0 plugin

### Pre-Phase-D probe checkpoint (per probing.md)

All "deferred to Phase D" items inventoried + cross-coherence checked before Phase D starts. Currently-tracked Phase D dependencies:

- D19 activation-scope DSL design (Phase D pioneer activation expressions = design input)
- VC + DID for actor-identity binding (D24 standards-compat; composes with the identity-binding gap from D9 + D22)
- Methodology articulation (lives in shape-policy + specialist behavior at Phase D, per CONCEPTS "Methodology placement")
- D1 open tension (PBS-Schulz daily during rebuild) — resolved in Phase D
- Workflow as containment hierarchy on work-unit (revisit in Phase D / E if forced)

---

## Phase E — NOT STARTED

Per D26 description. Multi-deployment validation. Second shape impl. Federation begins.

---

## Phase F+ — INDEFINITE

Refinement / optimization / ecosystem extensions. Per D26.

---

## Cross-phase work-streams

Per CONCEPTS "Cross-phase work-streams" section — work that spans multiple phases rather than living in one:

| Workstream | Phases | Notes |
|---|---|---|
| Substrate-neutrality evidence | B (stub-pair via D41) + C (real-wire impls) | Phase B established structural promise via two stubs; Phase C reinforces with real-wire |
| Shape-neutrality evidence | D (practitioner-shape) + E (second shape) | Single-shape evidence is not sufficient per D26 |
| Methodology articulation | D | Lives in shape-policy + specialist behavior at Phase D, not as a separate phase |
| Positioning research | Cross-phase | `market-context.md`; commit-decision waits for Phase D pioneer evidence |
| Standards-compat per-kind mapping | A/B (layer-3-affecting + impl-affordable) + C (real-wire) + D (deployment-specific) | D24 tracker |
| Adversarial probing discipline | Cross-phase | `probing.md`; runs at named checkpoints (workstream completion / phase boundary / mid-cycle) |

---

## External-trigger checkpoints

Per CONCEPTS "External-trigger checkpoints" section. Re-evaluate roadmap priorities when these hit:

- **2026-08-02 — EU AI Act Article 12 effective date.** Audit-record reconstruction enforceable. AEGIS-shaped integrity protocol (per D40 §B) = canonical extension target. Phase C natural home.
- **Microsoft Agent Framework GA / version evolution.** D41 substrate stub may need re-mapping if API shifts substantially.
- **MCP spec evolution under Linux Foundation.** Phase C MCP-server-protocol adapter tracks the spec.
- **Anthropic API changes affecting Claude Agent SDK.** Substrate-binding contracts may shift; relevant for Phase C real-wire impl.

---

## How this file is maintained

- **Updated as work progresses** — status changes happen at workstream completion / lock moments, in the same commit as the work that triggers them.
- **Source-of-truth is D-entries.** Workstream definitions live in their cited D-entry (D27 for Phase A, D36 + D41 + D42 for Phase B). This file mirrors status; D-entries are canonical.
- **Bref scope drift gets logged here.** Originally 7 deliverables; expanded to 11 mid-Bref via the slot audit. Drift is normal; tracking it surfaces the pattern. Any future scope expansion documented inline.
- **New workstreams added here BEFORE work begins** — avoids the "we did work but it wasn't on the tracker" pattern.
- **Per-phase planning entries** (analog of D27/D36) get written when each phase is entered. Until then, this file's per-phase sections carry indicative-only workstream lists.

This file added 2026-05-12 in response to the session-recognition that workstream tracking was scattered across `CONCEPTS.md` / `README.md` / `decisions.md` without a canonical home.
