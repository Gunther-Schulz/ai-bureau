# D65 — 2026-05-17 — Extends D56 + D7 — state.shape_config population pathway; immutable post-boot

**Decision (substantive; closes D56 §D D-7 deferral; composes D57 §B.1 + D56 §B.1.1)**: The `composition.shape.configuration` slot (admitted at the manifest layer per D57 §B.1 opaque pass-through; threaded to the Shape CONSTRUCTOR per boot.py:222) ALSO populates `substrate.state.shape_config` at boot, providing the runtime backing for the `state.shape-config.<key>` path-lookup grammar locked by D56 §B.1.1. One assignment in boot.py after substrate construction (between the registered_payload_vocabulary loop and the `# 6. Shape policies` block); same source dict, two distinct consumers (Shape constructor + state). Immutable post-boot per D4 (shape-as-substantive-identity carried as policy) + D13 (shape kind); no event mutates shape_config. Future shape-version transition per D54 carries new configuration via reboot. Pre-lock probe SKIPPED per pure-pattern-application precedent (D46 / D47 / D51 / D53 / D60 / D61 SKIP).

## A. Scope of cluster

**Honest cluster cardinality: 1 path**. Pure pathway operationalization of D56 §D D-7 deferral. No new contract framing — uses D57's locked `composition.shape.configuration` manifest slot + D56's locked `state.shape-config.<key>` path-lookup grammar; D65 routes the one to the other.

The path:

- **A.1 Manifest → state pathway**: at boot, after substrate construction completes (after registered_payload_vocabulary population at boot.py:207; before shape loading at boot.py:209), set `substrate.state.shape_config = composition.get("shape", {}).get("configuration") or {}`. Defensive on the `composition.shape` key presence (composition.shape is optional per workspace schema); trailing `or {}` defends against null/falsy configuration values per no-silent-substitution discipline (explicit empty dict; no implicit type coercion).

Out of scope (per §D):

- Per-event mutation of shape_config (rejected with grounding — see §D D-1).
- shape_config schema validation per kind (deferred per §D D-2; D57 §D D-1 pattern applies).
- Inheritance from extension defaults (deferred per §D D-3; D57 §D D-5 precedent).

## B. Pathway applied

### B.1 — Manifest → state pathway

| Triad element | Lock |
|---|---|
| **Detection** | At boot, in `boot_workspace` (boot.py), after the substrate construction + state-population block (registered_payload_subtypes / registered_work_unit_kinds / work_unit_kind_payload_schemas / registered_payload_vocabulary) and before shape policies loading. One statement: `substrate.state.shape_config = composition.get("shape", {}).get("configuration") or {}`. Subsequent `Shape.check_authority` invocations consulting the D56 `state.shape-config.<key>` path-lookup grammar now resolve against this populated dict. |
| **Surface** | None new. `composition.shape.configuration` is opaque per D57 §B.1 — kind-specific schema validation happens INSIDE the Shape constructor (D57 §D D-1). The state-side population is a pure assignment; no parse, no validation, no failure path at the pathway itself. Per-event constraint evaluation failures continue to surface via existing `EventRejected(category="authority")` per D56 §B.1. Boot-time grammar parse failures continue to surface via existing `WorkspaceBootError(category="authority-constraint-grammar")` per D56. |
| **Recovery** | None new. The pathway has no failure mode of its own — it either copies the dict (configuration present) or initializes to empty (configuration absent / null). The downstream surfaces (Shape constructor for kind-specific config validation; per-event check_authority for constraint evaluation) retain their existing recovery shape. |

### B.2 — Composition with D57 + D56

D57 §B.1 threads `composition.shape.configuration` to the Shape CONSTRUCTOR (boot.py:222 — `configuration=composition.get("shape", {}).get("configuration")`). D65 threads the SAME source dict to `substrate.state.shape_config`. Two distinct consumers; no overlap; one source. D56 §B.1.1 path-lookup grammar's `state.shape-config.<key>` lookup now resolves against the populated state slot rather than against the default empty dict.

### B.3 — Immutability post-boot

No event subtype mutates `state.shape_config`. Per D4 (shape-as-substantive-identity carried as shape policy) + D13 (shape kind), a workspace's shape configuration is part of its substantive identity, not a runtime-evolving state slot. A future shape-version transition per D54 carries new configuration via reboot (the workspace is rebooted with an updated manifest); live in-place mutation is rejected per D61 (live-shape-migration is a deliberate scope-cut).

Phase D pioneer-instance practitioner-shape may surface a use-case for per-event mutation (e.g., constraint-tightening over time as accountability scope grows). If so, that use-case warrants a NEW D-entry that explicitly supersedes the immutability lock — not a back-door via per-event projection. See §D D-1.

## C. Impl follow-through (same commit)

- **boot.py** — one statement inserted between `# 6.`-preceding state-population block and `# 6. Shape policies` loading. ~3 LOC including comment.
- **NEW test file** `impl/tests/test_shape_config_pathway.py` — 2 tests:
  - Test 1 — manifest config populates state: manifest carrying `composition.shape.configuration: {"required-attester": "actor-1"}` → `workspace.substrate.state.shape_config == {"required-attester": "actor-1"}` after boot.
  - Test 2 — absent config → empty dict: manifest omits `configuration` on `composition.shape` → `workspace.substrate.state.shape_config == {}` after boot.

Estimated impl size: **~3 LOC + 2 tests**. Baseline (post-D64) 224 → 226 post-D65 [impl].

No new module, no new exception type, no new `FAILURE_CATEGORIES` entry. Pure pathway lock.

## D. What is NOT in this decision

- **D-1 — Per-event shape_config mutation**: rejected with grounding (per §B.3). Shape configuration is substantive identity per D4 + D13, not runtime-evolving state. Phase D pioneer-instance practitioner-shape may surface a use-case warranting a NEW supersedes-D65 entry; no back-door via per-event projection.
- **D-2 — shape_config schema validation**: kind-specific per D57 §D D-1 (Shape constructor owns its configuration schema). D65 is pathway-only; the Shape constructor's existing D57 receipt of the same dict carries kind-specific validation.
- **D-3 — Inheritance from extension defaults**: per D57 §D D-5 precedent (extension-default merge deferred). D65 does NOT merge extension-declared defaults; manifest's `composition.shape.configuration` (or its absence) is the sole source.
- **D-4 — Multi-source merge**: e.g., per-actor overrides of shape_config. Not in scope; rejected by single-source manifest-only pathway.
- **D-5 — Persistence**: state slot lives in WorkspaceState which is in-memory per D7 §3 + B2 design lock. Persistence pathway for state.shape_config inherits whatever persistence pathway lands for WorkspaceState as a whole (separate work-unit).

Other items NOT in this decision:

- **No retroactive rewrite of D56** — D56 §D D-7 (open question on pathway) is closed by D65 via EXTENDS, not via D56 amendment. Append-only ledger preserved.
- **No new substrate step** — pathway runs inside existing boot procedure; no step renumbering. Step count remains as locked by D49 §A.
- **No new typed exception** — pathway is pure assignment; no failure mode at the pathway itself.

## Decision-shape template self-application

- **WHAT**: lock the pathway from `composition.shape.configuration` (D57 §B.1 opaque admission) to `substrate.state.shape_config` (D56 §B.1.1 path-lookup target). Closes D56 §D D-7 deferral.
- **WHO**: enforced by *substrate (runtime)* — boot procedure carries the assignment. *shape (policy)* — unaffected at construction (D57 §B.1 thread to constructor preserved); now sees its `additional-constraints` constraints resolve `state.shape-config.<key>` against populated state. *framework-validator (B1)* — unaffected.
- **FAILS**: *Detection*: none new — pathway has no failure mode. Downstream consumers (Shape constructor, check_authority) retain their existing detection surfaces. *Surface*: existing surfaces unchanged. *Recovery*: existing recoveries unchanged.
- **CROSS**: D4 (shape-as-substantive-identity carried as policy — motivates immutability lock); D7 (workspace identity — composition.shape part thereof); D13 (shape kind); D54 (shape-version transition carries new configuration via reboot); D56 §D D-7 (closes deferral); D57 §B.1 (composes — same source dict, distinct consumer); D61 (live-shape-migration scope-cut — composes with immutability lock).
- **DEFERS**: per §D — D-1 through D-5.

## E. Pre-lock probe disposition

D65 **SKIPPED** the pre-lock probe per pure-pattern-application precedent (D46 / D47 / D51 / D53 / D60 / D61 SKIP).

**Rationale**: D65 introduces no new contract content. D57 §B.1 already locked the manifest-layer slot (`composition.shape.configuration`) with opaque pass-through semantics. D56 §B.1.1 already locked the path-lookup grammar (`state.shape-config.<key>`) consuming a `state.shape_config` dict (default `{}`). D65 routes the one to the other in a single statement at boot. No new grammar, no new check site, no new exception, no new `FAILURE_CATEGORIES` entry, no new substrate step.

**Quiet-assumption surfacing**: the §D defers list (D-1 through D-5) names what the pathway lock DOES NOT close (per-event mutation; schema validation per kind; extension-default inheritance; multi-source merge; persistence). These compose with existing deferrals on D57 + D56 and do not extend D65's scope.

## Rationale

D56 §D D-7 explicitly flagged the state-slot population pathway as the one open question on D56's scope. The natural place for that pathway is boot (substrate construction); the natural source is `composition.shape.configuration` (D57 already routes it to the Shape constructor for kind-specific validation); the natural target is `substrate.state.shape_config` (D56's path-lookup target). The pathway is mechanical: one assignment statement after substrate construction, same source dict, two distinct consumers.

The immutability lock (per D4 + D13) makes the pathway one-shot — populated at boot, never mutated by events. This aligns with D61 (live-shape-migration is a deliberate scope-cut) and D54 (shape-version transitions carry new configuration via reboot). Phase D pioneer-instance practitioner-shape may surface a use-case for per-event mutation; if so, that warrants a NEW supersedes-D65 entry rather than retrofitting a back-door.

Per durability bet: D65 is specification — no new typed exception, no new category, no new grammar; pure pathway lock. The implementation is ~3 LOC + 2 tests. The decision's value is in closing the D56 §D D-7 open question with explicit immutability framing — preventing future drift toward per-event mutation as a "we never decided" gap.

Honest 1-path scope per D56 + D57 precedent. Scope-cardinality-honesty discipline applied.

**Cross-references**: D4 (shape-as-substantive-identity carried as policy); D7 (workspace identity); D13 (shape kind); D54 (shape-version transition via reboot); D56 §B.1.1 (path-lookup grammar — pathway target) + §D D-7 (deferral now closed); D57 §B.1 (manifest-layer slot — pathway source; D57 threads to Shape constructor; D65 threads same dict to state); D61 (live-shape-migration scope-cut — composes with immutability lock); D46 / D47 / D51 / D53 / D60 / D61 §E (SKIP precedents for pure-pattern-application); probing.md Procedure 3 refined-skip rule.

## Honest basis caveats

- **Read directly this session**: D56 (full body); D56 design artifact `.ai/design/unit-2-shape-config-pathway.md`; D56 investigation tracker `.ai/investigation/tracker-unit-001.yaml`; boot.py (full body); workspace_state.py:50-79 (shape_config field declaration); test_configuration_passthrough.py (pattern reference); workspace-generic-shape/workspace.json (fixture); decisions.md index tail; `.ai/constraints.yaml` (C1-C7).
- **Cited via D56's cross-references (not freshly Read)**: D4, D7, D13, D54, D57, D61, D46, D47, D51, D53, D60 — D56 already cross-cites these; D65 inherits their framings rather than re-deriving.
- **Inferred**: LOC estimate (~3) verified against the actual edit. Test count arithmetic (224 → 226) verified by running pytest before and after.
- **Open / Flagged**: none load-bearing — the §D defers list (D-1 through D-5) names known deferrals; all are explicitly out-of-scope rather than open questions hanging on D65's lock.
