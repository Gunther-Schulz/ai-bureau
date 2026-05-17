# D54 — 2026-05-17 — Extends D33 + D13 — migration-safety discipline for shape versioning

**Decision (substantive; extends D33 §B + D13)**: When the bound shape of a workspace evolves through versions, framework + shape authors share a **migration-safety discipline** classifying shape-version bumps into three categories — **safe in-place** (apply without workspace boundary), **new era** (apply with recorded transition event; prior events stand under prior shape), **breaking** (workspace boundary required; live migration explicitly out of scope per D33 §B major-bump semantics + per D54-companion entry locking the `binding-kind` schema enum scope-cut). This entry locks the per-slot taxonomy + a NEW pure-function classifier (`classify_shape_change`) + a NEW `FAILURE_CATEGORIES` entry `"shape-migration-unsafe"` as **Phase B forward-bar contract** (parallel to D48 §B.1 AdapterCallError pattern — Phase B stubs can't drive the path meaningfully; classifier + category typed-bar lock the contract now; runtime activation deferred to Phase C+ once persistence-layer lands per §D D-1). Pre-lock probe FIRED-FULL per probing.md Procedure 3; probe surfaced a load-bearing persistence-gap (current `WorkspaceState` + `AppendOnlyEventChain` are in-memory-only per workspace_state.py:50-55 + event_chain.py:117-118) which motivated scope tightening from "boot integration now" → "forward-bar contract + boot integration deferred." Sixth-or-later post-cluster Bref deliverable per D45 §C cluster-supersedes phase completed at D52; D54 lands Bref deliverable #5.

## A. Scope of cluster

D33 §B locked the *mechanical* version bump rules (major / minor / patch) at framework-core layer. D52 operationalized `shape.actor_requirements` at runtime (per-event composition-validity check at substrate step 2.5; shape.py:151-226 + types.py:37). Neither names the per-slot taxonomy of what shape-version changes are *safe to apply to an in-flight workspace's existing event chain* vs *require a recorded transition* vs *require workspace boundary*.

**One path**: per-slot migration-safety taxonomy for the D13 shape contract slots that can change between versions. Honest cluster cardinality: **1 path** (taxonomy + forward-bar contract). Not a runtime path cluster (those completed at D52); this is a **discipline entry** operationalizing D33's existing semver framing for the specific case of shape evolution.

Out of scope (deferred per §D):
- Boot-time activation of the migration check (requires persistence-layer source-of-truth for prior version; deferred).
- Extension-manifest migration safety (D29; structurally parallel but extension-scoped).
- Multi-shape composition migration (deferred at D7; D7 mandates exactly-1-shape).
- Cross-version event-replay equivalence under shape change (Phase C+; depends on Phase D PractitionerShape concrete versions).

**Composes with companion clarification** (separate entry; same session): the `payload-composition-change.binding-kind` schema enum at schemas/payload-composition-change.schema.json:21-24 deliberately excludes `shape` — locked at ledger layer in the companion clarification. D54 picks up where that scope-cut ends: shape transitions cross workspace boundaries per the schema enum; this entry classifies WHICH transitions are safe even at that boundary vs require principled rejection.

## B. Substantive content — the three-category taxonomy + forward-bar contract

### B.1 Per-slot classification (D13 contract slots)

Per D33 §B semver — applied to D13 slots (shape.py:54-56 `version` accessor reads `spec["version"]`):

| Shape slot (D13) | Safe in-place (patch / minor) | New era (minor — recorded transition event) | Breaking (major — workspace boundary) |
|---|---|---|---|
| `id` | — | — | always (D7 mandates exactly-1-shape; id-change = new workspace) |
| `version` | metadata-only patch | semver bump on additive change | semver-major on removal/narrowing |
| `actor-requirements` | tightening `max` upward; loosening `min` downward | tightening `min` upward; tightening `max` downward (existing actors stand; new events must satisfy under D52 §B.1) | removing a required actor-subtype (would orphan existing actors under D52) |
| `required-capabilities[]` | — | additive (new capabilities required for new events; existing events stand) | removal (existing impl may no longer be valid) |
| `optional-capabilities[]` | additive; removal (loosens) | — | — |
| `authority-bindings[]` | loosening (admitting agent-actor where human-actor required; widening `required-role`) | tightening (narrowing actor-subtype; adding new binding for previously-unconstrained payload-subtype) | removing a binding that existing events relied on |
| `roles[]` | additive | role-semantics change (description shift) under stable id | removal (events reference orphan roles) |
| `hooks[]` | additive; description clarification | new hook firing on existing payload-subtypes (changes runtime surface) | removal of hook other code relies on |

**Pioneer-instance canonical case** (per CONCEPTS.md migration sketch): PBS-Schulz high-human-involvement v1 → mostly-automated v2 = `authority-bindings[]` LOOSENING (existing requirements widen to admit agent-actor). Safe in-place per row above.

**Composition with D52 §B.1**: `actor-requirements` row above is the slot D52 operationalized at per-event runtime. D54 classifies WHICH inter-version changes to that slot are safe; D52 enforces post-projection validity at per-event time under whatever version is currently bound. The two compose: D52 catches in-version violations (current state vs current shape policy); D54 catches between-version violations (prior state under prior shape vs new shape policy). Different time-dimensions; no overlap.

### B.2 Phase B forward-bar contract (per D45 triad)

| Triad element | Phase B contract | Activation timing |
|---|---|---|
| **Detection** | NEW pure function `classify_shape_change(prior_spec, new_spec) -> list[(slot, prior, new, category)]` in `validator/shape_migration.py` (NEW) — implements §B.1 table; returns ordered list of classified changes; `category in {"safe-in-place", "new-era", "breaking"}` | Locked Phase B (pure-function unit-testable); activated when persistence-layer lands (per §D D-1) |
| **Surface** | NEW `WorkspaceBootError(category="shape-migration-unsafe")` typed exception (per D46 pattern); carries `failures[]` listing each unsafe slot change with prior-value / new-value / classification | Class locked Phase B; raised at boot when activation lands |
| **Recovery** | Operator either reverts shape version, ships a manual transition event recording the era boundary, or starts a new workspace at major-bump boundary | Discipline locked now; mechanical recovery actions land with activation |

NEW `FAILURE_CATEGORIES` entry `"shape-migration-unsafe"` per D46/D48/D52 precedent. Phase B forward-bar: classifier + category exist; substrate/validator integration deferred — see §D D-1.

This is the **D48 forward-bar pattern applied to a different concern**. D48 §B.1 locked `AdapterCallError` typed-exception class even though Phase B stubs can't fail meaningfully (call lifecycle not real-wired). D54 locks classifier + category even though Phase B has no persistence for "prior shape version." Both: contract surface locked early so dependent decisions can cite stable surface; runtime activation lands with the dependency.

## C. Impl follow-through scope (Phase B forward-bar only)

- `impl/src/fresh_plan/validator/types.py` — add `"shape-migration-unsafe"` to `FAILURE_CATEGORIES` frozenset.
- `impl/src/fresh_plan/validator/shape_migration.py` (NEW ~40 lines) — pure function `classify_shape_change(prior_spec, new_spec) -> list[(slot, prior, new, category)]` implementing §B.1 table.
- 3 new pure-function tests in `impl/tests/test_shape_migration.py`: (i) safe-in-place loosening returns `[(..., "safe-in-place")]`; (ii) breaking removal returns `[(..., "breaking")]`; (iii) new-era tightening returns `[(..., "new-era")]`.
- **NO boot.py changes in this entry** — Phase B forward-bar; boot integration deferred per §D D-1 (waiting on persistence-layer).
- **Estimated**: ~30-40 LOC code + 3 pure-function tests. 195 baseline → 198 tests post-impl.

## D. Deferrals (Phase C+ concerns)

- **D-1 (load-bearing; surfaced by pre-lock probe)** — Boot-time migration check requires persistence-layer source-of-truth for "prior shape version." Current `WorkspaceState` + `AppendOnlyEventChain` are in-memory-only with persistence explicitly deferred (workspace_state.py:50-55 + event_chain.py:117-118 + D7 §3). Boot integration of the classifier waits on a future persistence entry that defines where prior version comes from (event-chain re-read across reboots OR new workspace-state persistence layer).
- **D-2** — Phase D version-trajectory fixture. All 17 current fixture shapes are static-version; no test exercises "boot, mutate spec version, reboot." When persistence + PractitionerShape v1→v2 land at Phase D, the end-to-end exercise drives the activated boot check. Phase B coverage = pure-function classifier tests only.
- **D-3** — Recorded-transition-event payload shape (which payload-subtype carries era-boundary; likely a new `shape-era-transition` payload-subtype — needs Phase D pioneer concrete grounding).
- **D-4** — Cross-version event-replay equivalence under shape change. Event projection per D39 currently has no version-conditional logic; D54 does not address whether replaying events emitted under prior shape against new shape policy preserves semantics.
- **D-5** — Extension-manifest migration safety (D29-side; parallel but distinct surface).
- **D-6** — Tooling for shape-author classification check at shape-impl publish time (CI-side; out of framework-core scope).
- **D-7** — Pioneer-instance v1→v2 worked example (Phase D PractitionerShape concrete migration).

## E. Pre-lock probe disposition

**FIRED-FULL** (escalated from FIRE-light by probe outcome). Per probing.md Procedure 3 + D48 §E + D50 §E + D52 §E precedent: D54 introduces NEW contract content beyond pure pattern application of D33 (new `FAILURE_CATEGORIES` entry + new pure-function classifier + new per-slot taxonomy table).

Probe outcome (verified code-claims + surfaced quiet assumptions):

- **PASS** — shape.py:54-56 carries spec["version"] per draft claim.
- **PASS** — `WorkspaceBootError(category=...)` pattern fits (multiple precedents in boot.py).
- **PASS** — payload-composition-change schema enum excludes `shape` per scope-cut framing.
- **PASS** — D33 §B semver rules apply.
- **FAIL (load-bearing)** — Initial draft assumed "recorded prior shape version" persists at boot. Probe revealed `WorkspaceState` + `AppendOnlyEventChain` are explicit-in-memory-only per docstring. Initial §C boot integration was unbuildable. **Resolution**: scope tightened to forward-bar pattern per D48 §B.1 precedent; boot integration moved to §D D-1.
- **STALE-FRAMING** — Initial draft called `actor_requirements` "unused contract slot." D52 [design+impl] DONE; slot is now consumed at runtime (shape.py:151-226). **Resolution**: D54 §B.1 + composition-with-D52 paragraph above clarify D52's per-event runtime vs D54's between-version classification.

Probe surfaced 4 quiet assumptions; 3 absorbed as §D D-1 (persistence), D-2 (Phase D fixture), D-3 (transition event payload). One absorbed inline as §B.1 composition-with-D52 paragraph.

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: per-slot migration-safety taxonomy for D13 shape slots; framework forward-bar contract (classifier + typed exception class + FAILURE_CATEGORIES entry); discipline guidance for shape authors picking version bumps.
- **WHO**: enforced by **framework-validator (B1)** at boot-time shape change detection (Phase C+ once persistence lands); observed by **shape (policy)** authors at shape-impl publish time (discipline guidance, Phase B and onward).
- **FAILS**: per §B.2 triad. *Detection*: classifier identifies breaking changes between prior + new spec. *Surface*: `WorkspaceBootError(category="shape-migration-unsafe")` carrying failures[]. *Recovery*: revert version OR ship transition event OR new workspace boundary.
- **CROSS**: D7 (exactly-1-shape; workspace boundary semantics; §3 persistence-deferred which §D D-1 reflects); D13 (slots being classified); D33 §B (semver semantics underpinning the taxonomy); D39 (event chain preserved across shape transitions; per-event projection version-agnostic per D-4 deferral); D45 (standing triad requirement honored at §B.2); D46 (`WorkspaceBootError` pattern reused); D48 §B.1 (forward-bar pattern this entry applies); D52 §B.1 (`actor_requirements` slot composition: D52 enforces in-version; D54 classifies between-version); D7 §3 (persistence-deferral motivates §D D-1).
- **DEFERS**: per §D D-1 through D-7.

## Rationale

D33 §B locked the *mechanical* semver rules but left per-slot interpretation to shape authors. The roadmap deliverable #5 tracked this gap because shape authors absent guidance default to either over-conservative (every change = major) or unsafe-in-place (silent application without recording transition). The forward-bar contract (§B.2) locks the framework's eventual fail-closed bar shape now so future entries (persistence-layer; Phase D pioneer) can compose against stable surface — even though the bar can't yet be activated.

Why FIRE-FULL probe + scope tightening rather than ship-as-drafted: the load-bearing assumption that "prior version" persists at boot turned out unsupported by current impl. Without scope tightening, the entry would have committed to a contract no test could exercise (the canonical "design lock without grounding" failure mode per probing.md). Probe caught this; scope tightening aligns with D48's already-established forward-bar pattern; net contract content preserved at smaller activation-scope.

D54 composes with D52 — D52 enforces shape policy at in-version composition mutation; D54 classifies shape policy compatibility across version transitions. Both prevent "state survives the change in violation of policy" failure mode, at different time-dimensions.

**Cross-references**: D4 (substantive identity; shape carries); D7 (exactly-1-shape; workspace boundary semantics; §3 persistence-deferred); D13 (shape kind contract; slots classified); D29 (extension manifest; parallel discipline deferred); D33 §B (semver foundation; this entry extends); D39 (event chain preserved; projection version-agnostic deferred); D40 (state replay precedent; D-4 deferral cites); D45 (standing triad — §B.2 honors); D46 (`WorkspaceBootError` pattern); D48 §B.1 (forward-bar pattern this entry applies); D52 §B.1 (`actor_requirements` slot — D52 in-version + D54 between-version composition); roadmap.md row #5 (Bref deliverable closed by this entry); companion clarification entry (`payload-composition-change.binding-kind` enum scope-cut at schemas/payload-composition-change.schema.json:21-24).
