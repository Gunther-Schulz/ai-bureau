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
| 7 | `decisions.md` split into per-entry files | DONE (2026-05-12) | 45 entries → 45 files at `decisions/D<NN>-<slug>.md`; `decisions.md` is now the chronological index. Done BEFORE D46+ cluster supersedes entries so they land as new files (no monolith collision). Session-start procedure updated to read index + iterate per-entry files. |

**Added to Bref scope mid-pass via slot-interpretation audit (2026-05-12):**

| # | Deliverable | Status | Output |
|---|---|---|---|
| 8 | `probing.md` adversarial stress-testing discipline (foundation) | DONE | `probing.md` (5 procedures) |
| 9 | `roadmap.md` canonical execution tracker | DONE | `roadmap.md` (this file) |
| 10 | Slot interpretation-layer pass (process 24 SUSPECT slots) | NOT STARTED | Mix of cheap labels + ~4-6 substantive D-entries (see breakdown below) |
| 11 | One additional adversarial audit (combined failure-mode coverage + abandonment-path) | DONE (2026-05-12) | **33 SUSPECT findings** on ~38 audited surface (more findings per surface than slot-interpretation's 24-of-78). Cross-category overlap → systemic pattern, not isolated gaps. Forced **bounded-fill plan revision** (pending next session) + **probing.md amendments** (5 edits landed; audit findings count tracking added to discipline evolution). See "Bounded lock-and-fill plan — REVISION PENDING" below. |
| 12 | probing.md amendments (5 edits) based on audit (c) findings | DONE | FAILS field strengthened with D44 triad pattern; new detection-surface-recovery audit shape; standing checkpoint cadence (failure-mode + abandonment-path now standing, not rotating); empirical calibration data point added; audit findings count tracking in evolution rules |
| 13 | D45 meta-foundation entry — detection-surface-recovery triad as standing requirement for runtime decisions | DONE | D45 (substantive; meta-foundation). Locks the pattern; pre-lock probe SKIPPED with documented reason (audit-driven entries are circular to re-probe; precedent for future audit-driven entries). Casts net over ~25-28 of 33 SUSPECTs via the cluster supersedes entries below. |
| 14 | Boot-procedure cluster supersedes entry + impl follow-through | DONE (entry D46 + impl + tests landed 2026-05-12) | D46 locks D45 triad applied to boot path: 3 SUSPECT paths unified (steps 6/7/8 silent ValueError swallowing; manifest-actor seeding mid-cascade rollback; capability-only substrate-binding recovery semantics). Impl: boot.py raises typed `WorkspaceBootError` with structured `failures[]` for each path; `MinShape` runtime class registered in `shape.py` (was vestigial unregistered fixture stub). 4 new D46 tests added; 172 tests pass (168 + 4). Sets the structural template for D47-D51. |
| 15 | Subscriber-dispatch cluster supersedes entry + impl follow-through | DONE (entry D47 + impl + tests landed 2026-05-12) | D47 locks D45 triad applied to dispatch + hook firing. Subscriber on_event exception → SubscriberDispatchError aggregate after drain. NEW contract: pre-event-emit fires synchronously between authority check + chain.append (handler raise → EventRejected); post-event-emit fires synchronously after enqueue (handler raise → HookExecutionError aggregated after drain). Both handler-exception and subscriber-exception paths use collect-then-aggregate pattern. Impl: substrate.py append_event reordered to honor 9-step sequence per D47; new exception types `SubscriberDispatchError` + `HookExecutionError`; `_subscriber_failures` + `_post_emit_failures` collection lists; `HookRegistry.clear()` added for test cleanup; `FAILURE_CATEGORIES` extended with `actor-seeding` (D46 latent gap closed) + `hook-handler` (D47). 8 new tests; 180 tests pass. Caught + corrected D47 §B.3 confabulated API claim + B.2 timing contradiction + line-number drift before commit; motivated probing.md investigation-before-claim discipline (commit 86ae2dc). |
| 16 | Adapter cluster supersedes entry + impl follow-through | **[design+impl] DONE (D48 entry + impl + tests landed 2026-05-12)** | D48 locks D45 triad applied to adapter path. THREE paths unified: (B.1) adapter `call()` failure shape — new `AdapterCallError` typed exception forward-bar for Phase C real-wire (Phase B stubs can't fail meaningfully); composes with D47 §B.1 SubscriberDispatchError aggregation when fired from specialist on_event. (B.2) adapter `attach_workspace` failure — boot.py:260-281 wrapping → `WorkspaceBootError(category="adapter-attach")`; Phase C real-wire forward-bar. (B.3) specialist required-adapter-binding resolution — replaces specialist.py:103-106 bare RuntimeError with `WorkspaceBootError(category="adapter-binding-resolution")` per D46 pattern. **D48 §E**: pre-lock probe FIRED (FIRST cluster supersedes to do so per probing.md refined-skip rule — D48 introduces new contract content beyond pure audit cleanup); 10/10 code claims verified + 5 quiet Phase C assumptions surfaced + made explicit as DEFERS §D D-1 through D-5 (call-lifecycle raise-point; attach failure cause-vocabulary; non-HTTP category vocabulary extension; delegation peer + passive event source patterns; action-event-timing relative to call()). Sets precedent for D49/D50/D51 if they introduce new contract content. **[impl]**: new `AdapterCallError` class in adapter.py; specialist.py:103-106 refactored to structured `WorkspaceBootError`; boot.py:260-281 wraps adapter-attach loop; `FAILURE_CATEGORIES` extended with `adapter-attach` + `adapter-binding-resolution`; 3 new tests in test_adapter.py + 1 modified test in test_specialist.py (replacing prior bare-RuntimeError assertion); 183 tests pass (180 + 3). |
| 17 | Specialist cluster supersedes entry + impl follow-through | **[design+impl] DONE (D50 entry + impl + tests landed 2026-05-12)** | D50 locks D45 triad applied to specialist path. ONE path (D45 §C item 4 SUSPECT (a): handle_skill failure shape; (b) on_event already closed by D47 §B.1). Honest cluster sizing: 1 SUSPECT vs D46/D47/D48's 3 each — second-pass corrected the first-pass scope-inflation (mirroring D48's 3-path structure with refactor sites that turned out to be Python idioms; D49 first-pass pattern-completion lesson applied). NEW typed exception `SkillExecutionError` (parallel to D48's AdapterCallError) for Phase C+ real-wire forward-bar; Phase B pre-condition guards stay as Python idioms (specialist.py:169-172/197-200/201-204/209-213) per §D D-1. Composition with D47 §B.1 SubscriberDispatchError aggregation (on_event-triggered path) + D48 §B.1 AdapterCallError (adapter-call-inside-handle_skill; specialist-impl choice per §D D-5). Pre-lock probe FIRED per D48 §E precedent (new contract content) — 10/10 code claims verified + 5 quiet assumptions surfaced as §D D-2 through D-6 (category vocabulary for non-practitioner shapes; handle_skill-lifecycle raise-point; async/streaming; AdapterCallError composition; batch invocation). **[impl]**: new `SkillExecutionError` class in specialist.py (parallel to D48's `AdapterCallError`); 2 new tests in test_specialist.py — (i) structured-field propagation via monkeypatched subclass (direct invocation path); (ii) SkillExecutionError aggregation via subscriber-dispatch composition (D47 §B.1 path; delegating specialist's on_event invokes handle_skill that raises). 185 tests pass (183 + 2). |
| 18 | Validation cluster supersedes entry + impl follow-through | **[design+impl] DONE (D51 entry + impl + tests landed 2026-05-12)** | D51 locks D45 triad applied to validation path. 2 SUSPECTs unified: (B.1) per-work-unit identity checks (D30 §4 named, never implemented in per_event_checks.py); (B.2) B1 collect-all silent-skip when extensions empty at validator/workspace.py:275. Different layer than D46-D50 (validation, not runtime behavior). Honest cluster sizing: 2 SUSPECTs (vs D46/D47/D48's 3; D50's 1). PURE pattern application — operationalizes existing D30 §4 contract + removes known silent-degradation bug; NO new exception types / categories / composition framings; reuses EventRejected(category="identity") for §B.1 + WorkspaceBootError for §B.2. **§E SKIP probe per D45 §E precedent** (aligns with D46/D47; distinguishes from D48/D50 which fired probe for new-contract content). Systematic audit per new CLAUDE.md "First-order findings are starts" discipline found 4 additional silent-skip candidates in checks.py (lines 166-170, 271-279, 295-305, 605-615); direct Read of check_resolution verified upstream-catches rationale — they're defensive (not silent-degradation); §C adjacent cleanup adds inline rationale comments per new "No silent substitution" form-level discipline. **[impl]**: extended `check_event_references` in per_event_checks.py with work-unit-creation-event branch (validates contributing-actors/contributing-specialists/kind); added `registered_work_unit_kinds` field to Substrate dataclass; boot.py populates it from vocabulary_tables; removed `if loaded:` guard at validator/workspace.py:275 (one-line fix); 4 inline rationale comments at checks.py:166-180 / 271-282 / 305-313 / 622-630; 5 new tests (4 §B.1 + 1 §B.2); fixture update: workspace-substrate-test/min-shape-ext now registers work-unit.kind:k + :dummy-kind so test_substrate_e2e tests pass with the now-strict kind check. 190 tests pass (185 baseline + 5 new). |
| 19 | Composition-change cluster supersedes entry | NOT STARTED | Apply D45 triad to composition-change path: post-projection state validity (e.g., adding actor whose subtype contradicts shape's authority-binding) + composition-change shape authority interaction. ~D52 candidate (shifted +1). |
| 21 | 2026-05-12 retrospective sharpen sweep on D47 + D48 + discipline-hardening artifacts | DONE | Sharpen sweep via sub-agent dispatch surfaced (a) 2 HIGH + 3 MEDIUM on D47 (LOCK-HARD); (b) 0 HIGH + 3 MEDIUM on D48 (LOCK-HARD); (c) 5 HIGH + 4 MEDIUM on discipline-hardening artifacts (AMENDABLE-IN-FLIGHT). Phase 3 (AMENDABLE) sharpenings landed in commit 9325a1f (probing.md Pattern-completion bullet + README step 5/6 + Sketch-then-lock + [design+impl] criterion). LOCK-HARD findings landed via D49 clarification entry (this row's main artifact) — 3 corrections: D47 §C bullet 6 step-count 7→9; D47 §D missing handler-index defer; D48 §B.2 Recovery row wording. 5 wording-polish findings logged-and-accepted per cost/benefit. Dotfiles JOURNAL.md observation (commit 13adbcf in dotfiles) captures "sub-agent-trust-as-fact" failure mode as discipline-effectiveness data point. |
| 20 | Structural enforcement of grounded-reads discipline (PreToolUse hook) | NOT STARTED | Build a `plugin/hooks/<name>.py` PreToolUse hook (analog of inherited pbs-bureau `architectural_commit_gate.py`) that blocks Edit/Write on substantive artifacts (`fresh-plan/decisions/D*.md`, `fresh-plan/impl/src/**/*.py`, `fresh-plan/schemas/*.json`) unless required prep Reads happened in current session. Discipline content lives at README Session-start step 5 (HARD RULE). Hook is the structural backstop — prose rules empirically drift, hooks are deterministic per Anthropic engineering guidance. Motivating evidence: 2026-05-12 sketch-without-grounding incident; canonical AI failure mode of insufficient context-reading. Design open: which file-write paths qualify as "substantive"; what counts as "required prep Read"; how the hook detects session-scope Reads. |

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
5. NOT STARTED: remaining original Bref deliverables (#5 D33 migration-safety; #6 D38 Sana worked-example) — note: #7 decisions.md split landed early on 2026-05-12 (deliverable status table)
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
