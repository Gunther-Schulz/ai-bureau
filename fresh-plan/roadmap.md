# fresh-plan roadmap

Canonical map of phases, workstreams, and current status. This is the execution tracker — what work exists, what's done, what's next.

For framework orientation, see `CONCEPTS.md`. For session procedure, see `README.md`. For architectural decisions, see `decisions.md`. For adversarial stress-testing discipline, see `probing.md`.

Source-of-truth for each workstream's *definition* is the cited D-entry. This file *mirrors* status; D-entries are canonical for content. New workstreams added here BEFORE work begins to avoid the "we did work that wasn't on the tracker" pattern.

## Phases at a glance

| Phase | Description | Status |
|---|---|---|
| A | Layer 3 (formal schemas + extension protocol + composition rules + versioning) | DONE (closed at D35) |
| B | Reference impl of core | IN PROGRESS (impl side complete; Bref refinement workstream active) |
| C | Real-wire integration (substrate + adapters + specialists + persistence + integrity-protocol extensions + impl-level standards-compat) | ACTIVE per D68 |
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

## Phase B — COMPLETE (closed 2026-05-17 at D63)

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

### Bref — COMPLETE (Phase B refinement workstream per D42; closed 2026-05-17 at D62)

Originally tracked 7 deliverables at D42 lock-time. **Scope expanded mid-Bref** by the slot-interpretation audit (surfaced 24 SUSPECT slots) + the failure-mode/abandonment-path audit (surfaced 33 SUSPECT runtime decisions). Both absorbed via D45 meta-foundation + 6 cluster supersedes (D46-D48 + D50-D52) + 5 substantive post-cluster Extends entries (D54-D58 + D59) + 2 clarifications (D60-D61). **Workstream closed at D62 (Bref output) + D63 (Phase B closure). 218 tests pass; 63 D-entries locked.**

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
| 19 | Composition-change cluster supersedes entry + impl follow-through | **[design+impl] DONE (D52 entry landed 2026-05-17; impl follow-through landed same-day; 5 new tests; 195 tests pass)** | D52 locks D45 triad applied to composition-change path. HONEST 1-path scope per D45 §C item 6 canonical wording (corrects roadmap inflated 2-path framing from prior session — scope-cardinality-honesty per Clippy upstream D1 sub-check). Path: post-projection state validity for composition-change events affecting actors; operationalizes `shape.actor_requirements` (previously-unused slot from Bref slot-interpretation audit). NEW shape runtime method `check_post_event_state_validity`; NEW substrate step 2.5 (between authority check + pre-event-emit hook; canonical step count 9 → 10 via insertion-at-named-position preserving D47/D49 references); NEW FAILURE_CATEGORIES entry `composition-validity`; reuses existing `EventRejected` typed exception. **§E pre-lock probe FIRED** per D48/D50 §E refined skip rule (new contract content). Probe outcome: 9/10 code claims verified + 7 quiet assumptions surfaced as explicit DEFERS §D D-1 through D-7 (timing alternatives; actor_requirements semantics extension; non-actor binding-kinds; composition-change:update; state-change post-projection; record schema validation; Phase D end-to-end exercise). Sixth + LAST cluster supersedes per D45 §C — cluster-supersedes phase of Bref bounded-fill plan COMPLETE with D52. **[impl] landed**: shape.py new method `check_post_event_state_validity` (deepcopies state + projects event + counts actors by subtype + validates against `actor-requirements: {subtype: {min?, max?}}`); substrate.py step 2.5 insertion + 10-step docstring update; validator/types.py FAILURE_CATEGORIES entry `composition-validity`; 5 new tests in test_composition_validity.py (min violation + max violation + actor-requirements='none' regression + state-not-mutated + non-composition-change short-circuit); 195 tests pass (190 baseline + 5 new). |
| 21 | 2026-05-12 retrospective sharpen sweep on D47 + D48 + discipline-hardening artifacts | DONE | Sharpen sweep via sub-agent dispatch surfaced (a) 2 HIGH + 3 MEDIUM on D47 (LOCK-HARD); (b) 0 HIGH + 3 MEDIUM on D48 (LOCK-HARD); (c) 5 HIGH + 4 MEDIUM on discipline-hardening artifacts (AMENDABLE-IN-FLIGHT). Phase 3 (AMENDABLE) sharpenings landed in commit 9325a1f (probing.md Pattern-completion bullet + README step 5/6 + Sketch-then-lock + [design+impl] criterion). LOCK-HARD findings landed via D49 clarification entry (this row's main artifact) — 3 corrections: D47 §C bullet 6 step-count 7→9; D47 §D missing handler-index defer; D48 §B.2 Recovery row wording. 5 wording-polish findings logged-and-accepted per cost/benefit. Dotfiles JOURNAL.md observation (commit 13adbcf in dotfiles) captures "sub-agent-trust-as-fact" failure mode as discipline-effectiveness data point. |
| 20 | Structural enforcement of grounded-reads discipline (PreToolUse hook) | **[design+impl] DONE (D66 entry + plugin + 3 tests landed 2026-05-17)** | D66 locks the hook contract + lands `fresh-plan/plugin/.claude-plugin/plugin.json` + `fresh-plan/plugin/hooks/fresh_plan_grounding_gate.py` (~212 LOC; 1 check; adapted from pbs-bureau parent `plugin/hooks/architectural_commit_gate.py` — narrowed to required-Reads freshness via whole-session transcript scan) + `fresh-plan/plugin/tests/test_grounding_gate.py` (3 subprocess tests). Substantive artifact path patterns: `fresh-plan/decisions/D*.md` + `fresh-plan/impl/src/**/*.py` + `fresh-plan/schemas/*.json`. Required Reads: `fresh-plan/CLIPPY-COMPANION.md` + `fresh-plan/probing.md`. Pre-lock probe FIRED per D48/D50/D52 §E precedent (new plugin component + new hook semantics + new required-Reads contract). 6 quiet assumptions surfaced as §D D-1 through D-6 (content-pattern checks; per-write-type granularity; profile-cluster N/A; perf; cross-branch portability; activation discipline). Plugin tests are SEPARATE from impl pytest baseline (229 unchanged); plugin tests run via `python3 -m unittest fresh-plan.plugin.tests.test_grounding_gate`. Activation requires `/reload-plugins` on fresh-plan-clippy branch (C1 branch isolation). |

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

## Phase C — ACTIVE (planned at D68; trigger-based per D26)

Per D26 indicative scope + D63 §E Phase C scope handoff + D68 Phase C planning entry (workstream order + setup decisions + closure criterion).

### Workstreams

Source-of-truth: D68 §A. Order indicative not rigid per D26 caveat. C3-C6 can run in parallel after C1 + C2 land.

| # | Workstream | Depends on | Status | Source |
|---|---|---|---|---|
| C1 | Real-wire substrate (Claude Agent SDK; single-substrate per D68 §B.1 + A3) | — | **[design+impl] DONE (D69 entry + impl + 11 tests landed 2026-05-17)** | D68 §A + §B.1 + D69 §B.1 NEW `sdk-init` FAILURE_CATEGORIES entry + ClaudeAgentSDKSubstrate runtime class + claude-agent-sdk-substrate-ext extension; 240 tests pass (229 baseline + 11 new); pre-lock probe FIRED per refined-skip rule (NEW contract: sdk-init category + agent-loop framing + sync-wrapper-over-async-SDK pattern); 7 §D defers cover Phase C+ refinements (translation granularity / multi-turn / tool registration / connection-pool / SDK version-incompat / real-wire Anthropic / ClaudeAgentOptions configuration). |
| C2 | Persistence layer (JSONL append-only per D68 §B.2) | C1 | **[design+impl] DONE (D70 entry + impl + 13 tests landed 2026-05-17)** | D68 §A + §B.2 + D70 §B.1 NEW `persistence-corruption` FAILURE_CATEGORIES entry + PersistenceLayer module + boot step 4.5 (replay + D54 §B.2 + D58 §B.1 activations) + Substrate.append_event Step 4a write-through; 253 tests pass (240 baseline + 13 new); pre-lock probe FIRED per refined-skip rule (NEW contract: persistence-corruption category + persistence-layer framing + boot step 4.5 insertion); 7 §D defers cover Phase C+ refinements (snapshot caching / in-memory rollback / composition delta / schema evolution / cross-platform durability / configurable default / multi-substrate isolation). |
| C3 | Real-wire MCP client adapter | C1, C2 | **[design+impl] DONE (D71 entry + impl + 12 tests landed 2026-05-17)** | D68 §A + §B.3 + D71 §B.1 ACTIVATES D48 §B.1 AdapterCallError forward-bar under real-wire MCP transport + RealWireMCPClientAdapter runtime class + mcp-server-ext 0.2.0 (NEW `mcp-client-realwire` protocol-or-transport identifier alongside preserved 0.1.0 `mcp-client`); resolves D48 §D D-1 (call-lifecycle raise-point: emit-before-wire) + D-3 (per-protocol category vocabulary mapping for MCP) + D-5 (action-event timing: emit-before-call); 265 tests pass (253 baseline + 12 new); pre-lock probe FIRED per refined-skip rule (NEW contract: real-wire AdapterCallError ACTIVATION + new protocol identifier + pre-wire action emission convention); 5 §D defers cover Phase C+ refinements (production transport selection / per-server auth-code mapping / non-stdio transport refinements / connection-pool + multi-call sessions / real-wire end-to-end). |
| C4 | Real-wire direct-API adapter | C1, C2 | **[design+impl] DONE (D72 entry + impl + 21 collected tests landed 2026-05-17)** | D68 §A + §B.3 + D72 §B.1 ACTIVATES D48 §B.1 AdapterCallError forward-bar under real-wire HTTP transport + RealWireDirectAPIAdapter runtime class + direct-api-ext 0.2.0 (NEW `direct-api-realwire` protocol-or-transport identifier alongside preserved 0.1.0 `direct-api`); pure pattern application of D71 framework (SAME class shape + asyncio.run sync-wrap + _session_factory test-injection + AdapterCallError reuse); IMPROVEMENT over D71: NATIVE HTTP auth-category mapping (401/403/407 → auth) where D71 §D D-2 deferred MCP's auth subcase per server-specific code requirement; partially resolves D48 §D D-3 (per-protocol category vocabulary mapping for HTTP); 286 tests pass (265 baseline + 21 new collected from 13 def test_ functions, 2 of which parametrize over 3+7 status codes); pre-lock probe SKIPPED per refined-skip rule (pure pattern application; D46/D47/D51/D53/D60/D61/D65/D67 SKIP precedent cluster); 4 §D defers cover Phase C+ refinements (production base_url/headers/TLS / per-API auth-flow specifics / streaming HTTP / real-wire end-to-end with credentials). |
| C5 | Real-wire A2A peer adapter | C1, C2 | **[design+impl] DONE (D73 entry + impl + 15 tests landed 2026-05-17)** | D68 §A + §B.3 + §C closure item (a) + D73 §B.1 + §B.2 + §B.3 ACTIVATES D21 workspace-as-A2A-peer deployability + D60 publicly-exposed filter; A2APeerAdapter combined publisher (GET /.well-known/agent.json) + task-receiver (POST /tasks → specialist.handle_skill) + outbound peer-client (call() POST /tasks via httpx, parallel to D72); a2a-peer-ext 0.1.0 NEW protocol-or-transport identifier `a2a-peer` (no prior stub to coexist with); server-async lifecycle via stdlib http.server.ThreadingHTTPServer on a daemon threading.Thread per D44 framing (HTTP-transport-local, NOT substrate-level event loop); §B.1 server-bind failure REUSES D48 §B.2 adapter-attach category (no new FAILURE_CATEGORIES); §B.2 outbound REUSES D72 §B.1 starter category vocabulary including NATIVE HTTP auth-category mapping (401/403/407); §B.3 NEW inbound-handler triad with HTTP error response surface (NOT AdapterCallError — server-side, no caller in framework process); a2a-sdk 1.0.3 canonical protobuf AgentCard / AgentSkill types serialized via google.protobuf.json_format.MessageToJson; 301 tests pass (286 baseline + 15 new); pre-lock probe FIRED per refined-skip rule (5 NEW contract elements: server-async pattern + agent-card aggregator + A2A protocol integration + a2a-sdk dep + NEW B.3 inbound-handler triad); 5 §D defers cover Phase C+ refinements (TLS/HTTPS / per-API auth-flow / long-running connections + A2A subscribe / AgentCard security_schemes / real-wire end-to-end with credentials). |
| C6 | Real-wire MCP server adapter | C1, C2 | **[design+impl] DONE (D74 entry + impl + 11 tests landed 2026-05-17)** | D68 §A + §B.3 + §C closure item (b) + D74 §B.1 + §B.2 ACTIVATES D21 §generalization workspace-as-MCP-server + D60 publicly-exposed filter at the server-side surface; MCPServerAdapter async-native (no threading; unlike c5) with tool-aggregator (@list_tools → publicly-exposed=True specialist skills) + tool-router (@call_tool → specialist.handle_skill dispatch with reverse-map `<binding_id>.<skill_id>` per MCP SEP-986 character set) + outbound NotImplementedError per §D D-2 cross-impl deferral; mcp-server-side-ext 0.1.0 NEW protocol-or-transport identifier `mcp-server` DISTINCT from `mcp-server-ext` CLIENT-side family (D71 0.2.0 mcp-client-realwire + preserved 0.1.0 mcp-client); HYBRID pure pattern application — c3 D71 MCP SDK + memory bridge UNCHANGED + c5 D73 server-side aggregator pattern UNCHANGED + c5 D73 §B.3 inbound-handler triad SHAPE REUSED translated to McpError surface; §B.1 inbound tool-call McpError vocabulary (-32601 method-not-found for unknown/not-exposed; -32603 internal-error for handle_skill exceptions); §B.2 server-bind REUSES D48 §B.2 adapter-attach unchanged (no new FAILURE_CATEGORIES); zero pyproject.toml dep delta — reuses mcp>=1.0 installed at D71; 312 tests pass (301 baseline + 11 new); pre-lock probe SKIPPED per refined-skip rule (HYBRID pure pattern application of D71 + D73; D46/D47/D51/D53/D60/D61/D65/D67/D72 SKIP precedent cluster); 5 §D defers cover Phase C+ refinements (production transport binding stdio/sse/streamable_http / outbound peer-as-server cross-impl / streaming + resources + prompts surfaces / tool-name-collision policy / real-wire end-to-end with external MCP client + credentials); closes Phase C closure item (b). |
| C7 | Real-wire specialists | C3, C4 | **[design+impl] DONE (D75 entry + impl + 10 tests landed 2026-05-17)** | D68 §A + §C closure items (c) + (f) + D75 §B.1 ACTIVATES D50 §B.1 SkillExecutionError forward-bar under real-wire conditions + RESOLVES D50 §D D-5 composition contract as first concrete precedent (WRAP AdapterCallError as SkillExecutionError(category='external-dependency-error') with __cause__ chain); NEW RealWireRAGSpecialist class subclassing Specialist (replaces B7 RAGSpecialist stub; B7 stub preserved per D41 two-version parity) + rag-via-mcp-ext 0.2.0 NEW specialist provision `rag-realwire-specialist` (required-adapter-bindings → `mcp-server-ext:mcp-real-wire-adapter` c3 D71 real-wire adapter); 4-category dispatch ladder per D50 §B.1 starter vocabulary (domain-error params validation / external-dependency-error AdapterCallError WRAP / skill-execution result-parse / unknown catch-all); D64 §B.1 emit-attribution INHERITED via Specialist.attach_workspace closure-wrap unchanged; in-process MCP server harness via mcp.shared.memory per scope-cut C12; zero pyproject.toml dep delta — reuses mcp>=1.0 + c3 RealWireMCPClientAdapter UNCHANGED; 322 tests pass (312 baseline + 10 new); pre-lock probe FIRED per refined-skip rule (NEW contract: D50 §B.1 ACTIVATION + D50 §D D-5 RESOLUTION first concrete precedent + cross-typed-exception flow end-to-end); 5 §D defers cover Phase C+ refinements (real-corpus retrieval / per-shape category vocabulary / streaming + batch + federation / specialist-side caching / generic-specialist real-wire equivalent); closes Phase C closure items (c) + (f). |
| C8 | Integrity-protocol extensions (AEGIS canonical first per D40 §B) | C1, C2 | **[design+impl] DONE (D76 entry + impl + 10 tests landed 2026-05-17)** | D68 §A + §C closure item (g) + D76 §B.1 ACTIVATES D40 §B integrity-mechanism extension point as canonical first concrete example; NEW module `runtime/integrity.py` (~526 LOC) with `IntegrityProtocol` ABC (future Axon / PROV-O / post-quantum protocols register here per D29 namespacing) + `AEGISIntegrityProtocol` concrete (SHA-256 hash chain over JCS(event) || prev_hash via rfc8785 + Ed25519 per-event signing via cryptography; first-event prev_hash = SHA-256(workspace_id)) + `IntegrityRecord` dataclass + `IntegrityViolationError` typed exception + 6 keypair / PEM helpers; NEW `FAILURE_CATEGORIES` entry `integrity-violation` (21 → 22) covering hash-mismatch / signature-invalid / missing-record / canonicalization-error sub-cases; NEW extension `aegis-protocol-ext/0.1.0/` registers vocabulary entry `adapter.protocol-or-transport: aegis-event-chain-integrity` per D29 + D40 §B (NO provisions — integrity protocols are protocol-or-transport identifiers not adapter provisions); PersistenceLayer extension adds optional `integrity_protocol` field + `events.integrity.jsonl` parallel-line side-effect + `has_integrity_records()` + `load_integrity_records()` + `prime_integrity_state()` methods (+204 LOC net); boot.py step 4.5+ integration between persistence-replay and shape-migration check dispatches by `substrate-bindings[0].configuration.integrity-protocol` per D57 §B.1 opaque pass-through (+107 LOC net); per-workspace Ed25519 keypair persists as `integrity-private-key.pem` (mode 600) + `integrity-public-key.pem` next to events.jsonl; NEW pyproject deps `cryptography>=42` (was transitive via claude-agent-sdk; now declared direct) + `rfc8785>=0.1`; 332 tests pass (322 baseline + 10 new); pre-lock probe FIRED per refined-skip rule (NEW: abstract base + concrete impl + dataclass + typed exception + FAILURE_CATEGORIES entry + protocol-or-transport identifier + extension + persistence side-effect + boot-step integration + 2 deps); 6 §D defers cover Phase D+ refinements (other integrity protocols / production key management KMS-HSM / EU AI Act Article 12 audit-record-bundle format per D24 + D68 §D external-trigger 2026-08-02 / multi-protocol coexistence / rollback on integrity-record write failure / encrypted private keys); closes Phase C closure item (g) AEGIS integrity-chain round-trip + tampered-chain detection per scope-cut C12 in-process mockable. |
| C9 | Standards-compatibility engagement (impl-level per A5 split) | C1, C3-C7 | **[design+impl] DONE (D77 entry + impl + 17 tests landed 2026-05-17)** | D68 §A + §A5 split + D24 standards-compat tracker + D77 §A NON-BREAKING export-only contract (fresh-plan event envelope UNCHANGED) + D77 §B.1 CloudEvents 1.0 envelope alignment via `to_cloudevents` pure converter + D77 §B.2 W3C PROV-DM/PROV-JSON via `event_chain_to_prov_json` + `write_prov_json` pure converters + NEW `ProvJsonExportAdapter` introducing EXPORT-ONLY adapter sub-shape (no inbound; no outbound real-wire) as durable forward-bar for future OpenTelemetry / AsyncAPI / Activity Streams export adapters per D24 carry-overs; NEW module `runtime/standards_export.py` (300 LOC; 2 pure conversion functions + 1 IO wrapper + validation helper); NEW extension `prov-json-export-ext/0.1.0/` registers protocol-or-transport identifier `prov-json-export` per D29; D71 pre-wire convention REUSED for pre-export action event (export-side-effect IN chain, NOT IN export payload — avoids self-reference pollution); D48 §D D-3 starter category vocabulary REUSED — `transport` for file IO failure + `protocol-error` for malformed event envelope + `unknown` catch-all; ZERO `FAILURE_CATEGORIES` delta (22 stands); NEW pyproject dep `cloudevents>=1.10` (resolves to cloudevents 2.0.0 at C9 workstream-start lock); 349 tests pass (332 baseline + 17 new); pre-lock probe FIRED per refined-skip rule (NEW: standards_export module + ProvJsonExportAdapter + EXPORT-ONLY sub-shape + protocol-or-transport identifier + extension + W3C citation + CloudEvents mapping table + cloudevents dep); 7 §D defers cover Phase D+ refinements (PROV-DM library dep + round-trip / OpenTelemetry-AsyncAPI-ActivityStreams export mappings / per-payload-subtype prov:Entity + deployment-specific PROV-DM / EU AI Act Article 12 audit-record-bundle format per D24 + D68 §D external-trigger 2026-08-02 / CloudEvents inbound parser / breaking event-envelope rename / production export targets cloud-storage-regulator-endpoints per scope-cut C12). |
| Cref | Phase C refinement workstream (analog of Bref) | C1-C9 | **[design+impl] DONE (D78 entry + 5 inline fixes + 2 new tests landed 2026-05-17)** | D68 §A; analog of D62 + D78 §A scope summary + §B disposition inventory (18 `log_for_cref` items + 6 cross-cycle pattern observations + 9 retro-validation R1-R9 findings). NO T1 architectural findings — same shape as Bref close per D62 §D. Dispositions: 5 fix-now (F3 substrate.py docstring + F12 adapter.py:1608 `partition` → `rpartition` LATENT BUG FIX for dotted binding-ids per `_common.schema.json` instance-identifier admitting dots + 2 new tests + F13 adapter.py build_tools docstring `:` → `.` per SEP-986 + F16 adapter.py:1874 remove redundant `list(...)` wrap of `all_events()` + F17 standards_export.py narrower-than-canonical docstring); 8 log-and-accept (F1 D69 numerical drift + F2 D69 false-Cite + F5 D71 anyio string-match trade-off + F6 D71 auth folded into upstream-error + F8 D72 line range overshoot + F9 D72 off-by-1 pyproject + F11 D73 404 test gap + F14 D74 test name nit); 5 defer-to-Phase-D-pioneer (F4 D70 persistence-write rollback + F7 D71 NotImplementedError-as-unknown + F10 D73 workspace.shutdown adapter cleanup + F15 D74 long-running Server.run + F18 D77 runtime/__init__.py public surface). Cross-cycle observations affirmed: P1 NON-BREAKING across Phase C; P2 FAILURE_CATEGORIES REUSE-vs-NEW (3 NEW + 6 REUSE; 19 → 22); P3 adapter pattern uniformity across c3/c4/c5/c6/c9; P4 D45 triad coverage on every entry; P5 D50 §D D-5 WRAP composition resolved at C7 D75 first concrete precedent; P6 investigation-before-claim discipline empirically narrowed drift across c1→c9 (c1 D67-class drift → c2-c9 zero load-bearing drift). 349 → 351 tests (+2 F12 regression coverage). ZERO `FAILURE_CATEGORIES` delta (22 stands). ZERO new D-entries beyond D78. ZERO new modules. ZERO new pyproject deps. SKIPPED pre-lock probe per D62 §F + D63 §F precedent for pure-synthesis workstream-output entries. C11 mandatory retro-validation honored via fresh-context investigation sub-agent at investigate-design phase (DEVIATION from C11 literal "sub-agent dispatch" wording surfaced in D78 §F Honest-basis-caveats). |
| closure | Phase C closure entry (analog of D63) | Cref | NOT STARTED | D68 §A; closure-criterion per D68 §C |

### Closure criterion

Source-of-truth: D68 §C. Phase C closes when all seven items demonstrable:

- (a) A2A peer external interaction succeeds (C5 + D21)
- (b) MCP server external invocation succeeds (C6 + D21 generalization)
- (c) Real-wire RAG-via-MCP end-to-end (C7 replaces B7 stub)
- (d) Persistence survives restart with D54 + D58 active (C2 activates D54 §D D-1 + D58 §D D-5)
- (e) D48 §B.1 AdapterCallError raised under real-wire conditions (each starter category exercised)
- (f) D50 §B.1 SkillExecutionError raised under real-wire conditions (each starter category exercised)
- (g) AEGIS integrity-chain verification round-trip (C8 operationalizes D40 §B)

### Cross-session input pending — standards-compat engagement

**A5 split locked in D68 §E** (2026-05-17): Phase C handles impl-level (CloudEvents envelope + W3C PROV-DM citation / PROV-JSON export per C9); Phase D handles deployment-specific (practitioner-shape PROV-O attribution; bauleitplanung domain-extension PROV-DM mappings). Aligned with D26 indicative phase-mapping ("Phase B/C for impl-level; Phase D for deployment-specific") + D24 standards-compat tracker carry-over.

CloudEvents envelope alignment is a D43-class-but-larger rename refactor — landed as part of C9 per D68 §A. PROV-JSON export adapter is C9 deliverable per D24. D24 tracker carry-overs (OpenTelemetry, AsyncAPI, Activity Streams, EU AI Act mappings) — per D68 §D EU AI Act Article 12 external-trigger checkpoint (2026-08-02) drives C8 timing.

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
