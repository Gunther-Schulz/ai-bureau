# D63 — 2026-05-17 — Phase B closure (analog of D35) — Phase B complete

**Decision (substantive; phase-closure entry; analog of D35 for Phase B)**: Phase B (reference impl of framework-core) is **complete**. The 8 implementation workstreams B1-B8 + B2b two-substrate parity (per D41) + the Bref refinement workstream (per D42; closed at D62) are all landed. The framework now has a working reference impl validated against the Phase A formal schemas + per-event runtime contracts + the D45 detection-surface-recovery triad applied across all six runtime-behavior clusters per D45 §C. Per D36 §C + D41 closure-criterion + D42 §"Closure-criterion update for D36 §C": (a) B8 end-to-end fixture passes ✓; (b) two-substrate parity per D41 shipped ✓ (inprocess-substrate-ext + ms-agent-framework-substrate-ext both pass B1 conformance independently); (c) Bref output entry locked ✓ (D62). Phase B closed; per D26, Phase C (standards-compat impl) is next, with the proviso that order is indicative not rigid.

## A. Phase B summary

Phase B started 2026-05-08 (per D26 + D36 planning) and closed 2026-05-17 at this entry's lock. Goal: reference impl of framework-core proving the Phase A specifications boot end-to-end. 8 implementation workstreams (B1-B8) + 1 parity workstream (B2b per D41) + 1 refinement workstream (Bref per D42; closed at D62). State at start (post-D35 Phase A close): 15 formal schemas + 10 worked examples; no runtime code. State at close (this entry's lock): **218 tests pass** across 32 test files; runtime code spans 15 modules in `impl/src/fresh_plan/runtime/` + 7 modules in `impl/src/fresh_plan/validator/`; **63 D-entries** locked (D1-D63; D63 is this entry). All D45 §C cluster supersedes landed; Sana-style worked-example validates D38 structurally (D53); migration-safety discipline locked as forward-bar (D54); 23 of 24 SUSPECT slots addressed (per D62 §D).

The phase's principal architectural contribution beyond Phase A: the **D45 detection-surface-recovery triad** as standing requirement for runtime decisions, applied across boot-procedure + subscriber-dispatch + adapter + specialist + validation + composition-change clusters (D46-D52). The phase's principal process contribution: the **`probing.md` adversarial-stress-testing discipline** (5 procedures + checkpoint cadence) + Sketch-then-lock pattern + Pre-lock probe FIRE / SKIP refined rule + investigation-before-claim discipline. Both contributions emerged FROM Phase B's empirical work (failure-mode + abandonment-path audit + slot-interpretation audit + D49 first-pass scope-inflation incident + D47 §B.3 confabulation incident) rather than being upfront design.

## B. Final artifacts inventory

**Schemas in `fresh-plan/schemas/`** (15 Phase A baseline + Bref refinements; verified at D62 §B):
- 15 per-kind formal schemas locked at D35 — `_common.schema.json`, `extension-manifest.schema.json`, `workspace.schema.json`, `actor.schema.json`, `event.schema.json`, `substrate.schema.json`, `shape.schema.json`, `adapter.schema.json`, `specialist.schema.json`, `work-unit.schema.json`, + 5 per-payload-subtype schemas (claim / action / state-change / composition-change / lifecycle-transition).
- Bref-era schema amendments: capability-identifier rename `event-streaming` → `event-chain` (D43); composition-change schema enum exclusion of `shape` formally documented (D61); extension-manifest `payload-vocabulary-registrations` slot per D59; `specialist.activation-scope` oneOf admitting structured predicate per D55.

**Runtime (`fresh-plan/impl/src/fresh_plan/runtime/`)** (15 modules):
- `workspace.py` (B7 + composition); `boot.py` (D7 + D32 + D46 boot procedure); `substrate.py` (D12 + D17 + D43 + D44 + D47 + D52 ordered append_event); `event_chain.py` (D10 + D39 + D40 + D58 lifecycle derivation); `shape.py` (D13 + D52 check_post_event_state_validity + D55 activation-scope parse-cache + D56 authority-constraint parse-cache); `adapter.py` (D16 + D48 AdapterCallError); `specialist.py` (D19 + D50 SkillExecutionError + D55 activation-predicate cache); `workspace_state.py` (D7 §3 in-memory state + D56 shape_config); `per_event_checks.py` (D30 §4 + D34 §A.5 + D51 work-unit identity + D59 payload-vocabulary); `hooks.py` (D13 + D17 + D47 firing integration); `skills.py` (D19 + D50); `provision.py` (D29 + D32 + D46 + D48 §B.3 resolution + D57 ProvisionResolutionError); `authority_constraint.py` (NEW Bref — D56 grammar parser).

**Validator (`fresh-plan/impl/src/fresh_plan/validator/`)** (7 modules):
- `workspace.py` (B1 entry + D58 lifecycle reconciliation + D59 payload-vocabulary loader); `checks.py` (D29 §validation flow + D30 cross-kind referential integrity + §B item 2 specialist roles vs shape check); `dependency.py` (D32); `extensions.py` (D29 §"Validation flow" step 1-3); `schemas.py` (D28); `types.py` (FAILURE_CATEGORIES + ValidationFailure + ValidationResult — 19 entries at Bref close, verified); `shape_migration.py` (NEW Bref — D54 §C classifier).

**Tests (`fresh-plan/impl/tests/`)** (32 test files; **218 tests** verified via `pytest -q`):
- B-workstream baseline: test_extension_loading, test_schema_loading, test_dependency_resolution, test_checks, test_substrate_boot, test_workspace_lifecycle, test_workspace_state, test_event_chain, test_per_event_checks, test_shape, test_skills, test_specialist, test_subscriber_dispatch, test_adapter, test_substrate_e2e, test_end_to_end, test_end_to_end_scenario, test_hooks, test_ms_agent_framework_substrate, test_rag_specialist.
- Bref-era additions: test_activation_scope (D55) + test_authority_constraint (D56) + test_composition_validity (D52) + test_configuration_passthrough (D57) + test_lifecycle_derivation (D58) + test_payload_vocabulary (D59) + test_sana_style (D53) + test_shape_migration (D54).

**Worked examples in `fresh-plan/schemas/examples/`** (10 Phase A baseline + Bref fixtures):
- 10 Phase A examples per D35 §B.
- Bref-era fixture additions in `impl/tests/fixtures/`: workspace-sana-style (D53) + workspace-substrate-test extensions + workspace-rag-via-mcp updates per D43 rename + D55 §B-2 specialist roles vocabulary fix.

**D-entries** (63 total; verified via decisions.md index):
- Phase 0 / D1-D6: framework identity + layered model + workspace boundary.
- Layer 2 / D7-D25: 8 kinds locked + clarifications + closure.
- Phase A / D26-D35: roadmap + 5 workstreams + refinement + closure.
- Phase B (B1-B8 + B2b) / D36-D41: planning + side-quest sharpening + two-substrate parity.
- Bref / D42-D62: 20 entries (per D62 §B table) + D62 workstream-output entry.
- Phase B closure / D63: this entry.

## C. Forward-bars to Phase C

Contract surfaces locked at Phase B that Phase C real-wire activates (per the durability bet — framework's primary deliverable is specification; Phase C concrete impls conform to locked surface):

- **D48 §B.1 AdapterCallError typed-exception** — adapter.call() failure shape locked; structured fields `adapter_id` + `call_target` + `category` + `detail` + exception-chained `from`; starter category vocabulary (`transport` / `auth` / `timeout` / `protocol-error` / `upstream-error` / `unknown`); per-protocol extensions register additional categories per D29. Phase B stubs cannot fail meaningfully; Phase C real-wire impls raise per the contract.

- **D50 §B.1 SkillExecutionError typed-exception** — specialist.handle_skill failure shape locked; structured fields parallel to AdapterCallError; starter vocabulary; per-shape extensions register additional categories. Phase B stubs cannot fail; Phase C real-wire specialists + Phase D PractitionerShape-bearing specialists raise per the contract.

- **D54 §B.2 shape-migration classifier + shape-migration-unsafe category** — `classify_shape_change` pure function + `WorkspaceBootError(category="shape-migration-unsafe")` locked; boot integration deferred pending persistence-layer landing per D54 §D D-1. Phase B has no persistence (workspace_state + AppendOnlyEventChain are in-memory-only); Phase C+ persistence-layer entry resolves D54 §D D-1 and activates boot-time reconciliation.

- **D55 §D D-7 activation-scope Phase D end-to-end exercise** — current Phase B fixtures use no `activation-scope` value (all specialists implicitly `"always"`). Phase D PractitionerShape-bearing specialists populate predicates and exercise the substrate-side pre-dispatch gate end-to-end.

- **D56 §D D-5 + D-7 practitioner-shape canonical constraints + state.shape_config pathway** — `shape-practitioner.json:15` English prose remains decorative under D56 impl. Phase D PractitionerShape rewrites as structured `equals` constraint citing `state.shape-config.required-attester`. The pathway from manifest to `state.shape_config` is itself a Bref-followon (D62 §E).

- **D57 §D D-3 in-place reconfiguration / hot-reload** — D57 scopes to boot-time threading. Mid-lifecycle reconfiguration is Phase C+ (composes with D52 §D D-4 composition-change:update deferred).

- **D58 §D D-5 idempotent re-derivation cost (snapshot caching per D11 + D40 §C)** — D58 reconciles ALL manifest-declared work-units against full chain replay at boot. O(chain) per work-unit. Snapshot caching is implementation answer; D58 does NOT lock strategy. Acceptable for Phase B reference-impl scale; Phase C+ scales when needed.

- **D59 §D D-7 Phase D end-to-end vocabulary exercise** — D59 locks contract + impl + tests with synthetic extension manifests. Phase D PractitionerShape-bearing extensions populate with real values (e.g., `defensibility-grade` confidence values).

## D. Standards-compatibility engagement deferred

Per D24 standards-compatibility tracker + roadmap.md Phase C §"Cross-session input pending" + D62 §D:

- **CloudEvents envelope alignment** + **W3C PROV-DM citation** — surfaced mid-Bref via cross-session input; both already on D24's tracker. **Decision deferred** to next session: small standalone clarification entry citing PROV-DM + naming CloudEvents alignment as priority, OR formalize a parallel "standards-compat per-kind mapping" workstream, OR leave on tracker. Lean: small clarification entry + leave heavy work for Phase C planning. CloudEvents envelope alignment is a D43-class-but-larger rename refactor; NOT a Bref item; Phase C natural home. PROV-JSON export adapter is unambiguously Phase C deliverable per D24.

- **D24 tracker carry-over**: PROV-O + VC + DID + OpenTelemetry + AsyncAPI + Activity Streams + EU AI Act mappings — Phase C / Phase D as applicable per D35 §"Verification targets carried forward beyond Phase A" + roadmap.md Phase C indicative workstreams.

Phase B does not break any in-scope standards mapping (verified at D35 §C; no Bref-era standards regressions surfaced).

## E. Phase C scope handoff

Per D26 indicative scope + roadmap.md Phase C indicative-workstream enumeration + the forward-bars locked at Phase B (per §C above):

- **Real-wire integration for substrate impls** — InProcessSubstrate stubs → real Claude Agent SDK substrate (or alternative); MSAgentFrameworkSubstrate Phase B stub → real wire. Validates D17 + D43 capability vocabulary against real cognitive frames per D41 parity-evidence framing.
- **Real-wire adapters** — real MCP client adapter; real direct-API adapter; A2A peer adapter (validates D21 deployability requirement); future Phase C protocol extensions per D29 namespacing. Each exercises D48 §B.1 AdapterCallError forward-bar.
- **Real-wire specialists** — RAG-via-MCP real wire; generic specialists; future skill-bearing specialists. Each exercises D48 §B.1 AdapterCallError forward-bar + D50 §B.1 SkillExecutionError forward-bar via the composition framing locked at D50 §B.2.
- **Persistence layer** — resolves D54 §D D-1 (boot integration for shape-migration classifier); resolves D58 §D D-5 (snapshot caching for idempotent re-derivation). Per-phase-planning entry (analog of D27 + D36) when Phase C begins.
- **Integrity-protocol extensions** — AEGIS-shaped + Axon-shaped per D40 §B canonical first examples; EU AI Act Article 12 audit-record format (effective 2026-08-02; external-trigger checkpoint per roadmap.md).
- **Standards-compatibility engagement** — deferred Phase A → Phase B → Phase C carry-over; engagement specifics per §D above.

Per-phase planning entry (analog of D27 for Phase A + D36 for Phase B) lands when Phase C begins; until then, roadmap.md Phase C section carries indicative-only workstream lists. Phase boundaries are trigger-based, not schedule-based (per D26).

## F. Pre-lock probe disposition

**SKIPPED** per probing.md Procedure 3 refined-skip rule + D35 + D62 + D34 SKIP precedent. D63 is pure synthesis / closure — no new contract content. Consolidates already-locked artifacts + already-locked forward-bars + already-deferred items. Re-probing would be circular.

## Decision-shape template self-application

- **WHAT**: phase-closure entry locking Phase B as complete. Inventories final artifacts; names forward-bars activating in Phase C; defers standards-compat engagement; hands off Phase C scope. Analog of D35 for Phase B.
- **WHO**: enforced by *opaque (documentary)* at framework-core; *deferred (Phase C)* for all forward-bar activations + real-wire integrations; *deferred (Phase D)* for end-to-end exercises naming Phase D as their landing target.
- **FAILS** (recursive): *Detection*: pre-Phase-C-transition probe catches deferral inventory gaps; mid-cycle exploratory dispatch surfaces post-closure drift. *Surface*: probe findings; failing tests when Phase C real-wire integrations violate Phase B locked contract. *Recovery*: supersedes / clarification entries per append-only; bias toward Phase C lock + post-hoc supersedes per the durability-bet.
- **CROSS**: D26 (indicative roadmap); D27 (Phase A enumeration approach); D34 (Phase A refinement output; analog precedent for D62); D35 (Phase A closure; THIS entry's analog precedent); D36 (Phase B planning); D41 (B2b two-substrate parity; satisfied); D42 (Bref formalization; satisfied via D62 lock); D45 + D46-D52 (cluster supersedes phase; all 6 landed); D62 (Bref output; immediate predecessor); D63 (this entry).
- **DEFERS**: per §C (forward-bars); §D (standards-compat); §E (Phase C scope + persistence layer + integrity-protocol extensions); Bref-followon list per D62 §E.

## Rationale

Phase B closes structurally **clean** in the same shape Phase A closed: no T1 architectural findings across the entire phase + refinement workstream; all closure-criteria satisfied per D36 §C + D41 + D42 §"Closure-criterion update"; all D45 §C cluster supersedes landed; foundation holds under cluster-supersedes + slot-pass + Sana-worked-example + migration-safety stress-tests.

The phase's character differs from Phase A in one structural respect: Phase A was pure-specification (15 schemas + composition rules + versioning) with no runtime code; Phase B was reference-impl-bearing (runtime + validator + tests) and produced its own **process-discipline corpus** as a side product. Per the CONCEPTS durability bet, the process-discipline corpus may prove more durable than the impl code (which Phase C will substantially rewire); the disciplines compose forward across Phase C + Phase D + Phase E.

The 8 forward-bars locked at Phase B (per §C) are the canonical instance of the durability-bet — contract surfaces locked early so Phase C real-wire integrations + persistence-layer landing + Phase D PractitionerShape population can compose against stable surface. AdapterCallError + SkillExecutionError + classify_shape_change are *specification* — typed exception class + category vocabulary + structured field shape + composition framing. Phase C concrete impls fill in operational mechanics per the locked specification.

Per the "Generic vs pioneer-instance discipline" working pattern (README): Phase B's generic impls stay deliberately neutral; Phase D PractitionerShape introduces pioneer-specific opinions. The bias-avoidance is load-bearing for Phase E shape-neutrality validation per D26. Phase B closes WITHOUT a Phase D-style pioneer-shape; D38 + D53 + D55-D57 deliberately defer pioneer-specific population to Phase D.

Phase B closes here; Phase C trigger per D26 + roadmap.md is when real-wire substrate / adapter / specialist work begins. Per-phase planning entry for Phase C lands when Phase C begins.

**Cross-references**: D14 (refinement-pass discipline); D24 (standards-compatibility tracker; carry-over); D26 (indicative roadmap; Phase B ↔ Phase C boundary trigger-based); D27 (Phase A enumeration approach; analog precedent); D34 (Phase A refinement output; D62 is the Phase B analog); D35 (Phase A closure; THIS entry's analog precedent); D36 (Phase B planning; §C closure criteria satisfied); D38 (knowledge-as-not-a-kind; validated by D53); D40 §C (snapshot caching precedent for D58 §D D-5 deferral); D41 (B2b two-substrate parity; satisfied at workstream level); D42 (Bref formalization; closed at D62); D45 (detection-surface-recovery standing requirement); D45 §C items 1-6 (all six cluster supersedes landed: D46-D48 + D50-D52); D46-D52 cluster supersedes (architectural-lock heart of Bref); D53-D61 post-cluster Bref entries; D62 (Bref output; immediate predecessor); roadmap.md Phase B → Phase C handoff section; `validator/types.py` FAILURE_CATEGORIES (19 entries at close); `pytest -q` (218 tests at close).

## Honest basis caveats

- **Read directly this session**: README + CLIPPY-COMPANION + probing.md + decisions.md (full index) + roadmap.md + D34 + D35 + D41 + D42 + D43 + D44 + D45 + D46 + D47 + D48 + D49 + D50 + D51 + D52 + D53 + D54 + D55 + D56 + D57 + D58 + D59 + D60 + D61 + D62; `validator/types.py` FAILURE_CATEGORIES list (verified 19 entries); `impl/src/fresh_plan/runtime/` directory listing (verified 15 modules); `impl/src/fresh_plan/validator/` directory listing (verified 7 modules); `impl/tests/` directory listing (verified 32 test files); `pytest -q` output (verified 218 tests collected).
- **Claimed but inferred from D35 §B-§E shape**: §B artifact inventory mirrors D35's structure; specific schema-list at this entry's lock is verified via D62 §B + D35 §B.
- **Cited via D62 §D not freshly Read**: "23 of 24 SUSPECT slots addressed" count + "10 new FAILURE_CATEGORIES" attribution map — established in D62 §D; D63 carries forward without re-verification.
- **Inferred (non-load-bearing)**: the categorical claim that no T1 architectural findings surfaced across Phase B — grounded in D62 §D + roadmap.md Bref status table; not exhaustively re-audited at this entry's lock.
- **Standards-compat engagement deferred**: §D defers without lock; D63 carries forward but does not resolve; first-class Phase C planning concern.
