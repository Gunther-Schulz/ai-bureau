# D52 — 2026-05-17 — Extends D10 + D13 + D39 — composition-change cluster honors detection-surface-recovery triad (per D45 §C)

**Decision (substantive; sixth cluster supersedes per D45 §C — the last cluster supersedes in Bref bounded-fill plan)**: The composition-change runtime path — specifically post-projection state validity for events that mutate actor composition — is locked under D45's detection-surface-recovery triad. One SUSPECT from the 2026-05-12 audit unified here as the **composition-change cluster** (per D45 §C item 6): post-projection state validity unchecked; composition-change events can produce state that violates shape policy with no detection. D52 operationalizes `shape.actor_requirements` (currently an unused contract slot per Bref slot-interpretation audit) by introducing a new shape runtime method `check_post_event_state_validity` invoked at substrate step 2.5 (NEW; between authority check at step 2 and pre-event-emit hook at step 3). Sixth cluster supersedes per D45 §C; D52 introduces new contract content (new shape method + new FAILURE_CATEGORIES entry + new substrate step ordering) beyond pure pattern application, so pre-lock probe FIRED per probing.md Procedure 3 refined-skip rule + D48 §E + D50 §E precedent (see §E).

## A. Scope of cluster

D45 §C item 6 canonical wording: "Composition-change cluster — D10 + D13 + D39: post-projection state validity unchecked (e.g., adding actor whose subtype contradicts shape's authority-binding requirements; composition-change passes per-event check but resulting state violates shape policy with no detection)."

**Honest cluster cardinality: 1 SUSPECT**, not 2. Per D45 §C item 6 canonical naming + scope-cardinality-honesty discipline (per probing.md Pattern-completion failure mode + D49 first-pass lesson + Clippy upstream D1 sub-check). Roadmap deliverable #19 row wording included "+ composition-change shape authority interaction" — this was scope-inflation in prior session work, not anchored to D45 canonical. D52 aligns with D50's honest 1-path scope (1 SUSPECT vs D46/D47/D48's 3-path structure).

The path covered here:

- **A.1 Post-projection state validity for composition-change events affecting actors**: `shape.actor_requirements` (shape.py:77-78 — runtime accessor with zero consumers in src/ + tests/; all 17 fixture shapes use `"none"`) declares workspace-level cardinality constraints per actor-subtype (per D13 + shape.schema.json `oneOf` clause: string `"none"` OR object map `{subtype: {min, max?}}`). When a composition-change event with `binding-kind=actor` projects new actor state (event_chain.py:52-63 `apply_event_to_state` for `change-type=add` or `change-type=remove`), the resulting actor population may violate the shape's cardinality declarations — but the framework currently checks NOTHING about post-projection state vs shape policy. D52 closes this gap.

**Distinction from existing checks** (per pre-lock probe Q5):
- `per_event_checks.check_event_references` (step 1) owns **identity resolution** (does actor.id resolve? per D30 §4; includes self-attestation for the on-event-added actor per D34 §A.5)
- `shape.check_authority` (step 2) owns **per-event authority** (does the emitting actor satisfy the shape's authority-binding for this payload-subtype + qualifier?)
- D52's new step 2.5 owns **post-projection shape-policy-validity** (does the resulting state honor shape.actor_requirements cardinality?)

Three distinct surfaces; no overlap.

Out of scope (deferred per §D below):
- Non-actor binding-kinds (substrate-binding, adapter-binding, specialist-binding, extension) — `event_chain.apply_event_to_state` currently no-ops projection for these (only the actor branch is implemented; lines 56-63).
- `change-type=update` projection — schema admits the enum value but `apply_event_to_state` has no `update` branch for any binding-kind.
- Composition-change payload.record schema validation against the binding-kind's own schema (e.g., actor record conforms to actor.schema.json) — schema description (composition-change.schema.json:26-28) names this as aspirational; runtime impl doesn't enforce.
- State-change post-projection state validity (work-unit-related events) — D51 partial coverage for work-unit-created references; remaining gaps are out of D52 scope.

## B. Triad applied per path

### B.1 — Post-projection state validity (composition-change actor events)

| Triad element | Lock |
|---|---|
| **Detection** | New shape runtime method `check_post_event_state_validity(event, state_before)` (Shape base; concrete subclasses inherit or override). For `event.payload-subtype == "composition-change"` AND `event.payload.binding-kind == "actor"` AND `shape.actor_requirements != "none"`: simulate the projection on a copy of `state_before` (apply `event_chain.apply_event_to_state` to the copy), then count actors by `subtype` in the simulated state and verify each `(subtype, {min, max?})` constraint declared in `actor_requirements`. Returns a list of `ValidationFailure(category="composition-validity")` — one per unsatisfied cardinality constraint. Early returns: non-composition-change events; non-actor binding-kinds; `actor_requirements == "none"`. |
| **Surface** | `EventRejected(failures=[ValidationFailure(category="composition-validity", path="event.payload.binding-reference" or "event.payload.record", value=<offending-actor-id>, reason=f"resulting state violates shape policy: actor-requirements <subtype>:{min:N, max:M} would be unsatisfied — simulated count <count>")])`. Reuses existing `EventRejected` typed exception (no new exception type; parallel to D46/D48 pattern). NEW `FAILURE_CATEGORIES` entry `composition-validity` added to `validator/types.py` per pattern (D46 added `actor-seeding`; D48 added `adapter-attach` + `adapter-binding-resolution`). |
| **Recovery** | Event rejected at substrate step 2.5 (NEW step inserted between authority check at step 2 and pre-event-emit hook at step 3). State NOT mutated — the check operates on a copy; if the simulation reveals a violation, the real state stays untouched and the event is not appended to the chain. Chain integrity preserved per D10 + D39 (append-only; state fully derivable from events). Caller fixes the manifest declaration OR avoids the offending composition-change; re-emits when the resulting state would honor shape policy. |

**Timing rationale (per pre-lock probe Q1)**: pre-projection-simulate over post-projection-warn or hook-based. Post-projection-warn (accept event into chain + log warning) is silent-substitution failure per global CLAUDE.md "No silent substitution" rule — the event would be canonical but its resulting state would silently violate shape policy. Hook-based pre-projection-validation pushes the discipline to shape-author burden without framework enforcement — shapes that forget to register the hook silently bypass the check. Pre-projection-simulate at substrate step 2.5 is framework-enforced (substrate calls shape.check_post_event_state_validity unconditionally when shape is present) and state-preserving (operates on copy; real state mutates only after the check passes).

## B.2 — Composition-change for non-actor binding-kinds + change-type=update (deferred per §D)

Non-actor binding-kinds (substrate-binding, adapter-binding, specialist-binding, extension) and `change-type=update` are admitted by the composition-change schema but currently no-op in `event_chain.apply_event_to_state` (lines 56-63 handle only `binding-kind=actor` with `change-type=add` or `change-type=remove`). D52 does NOT lock post-projection validity for these — see §D D-3 + D-4. Phase B has no use-case requiring runtime composition-change for non-actor binding-kinds (those are boot-time only); Phase C+ runtime-reconfiguration scenarios surface concrete needs.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

The contract is locked here; the impl follows. Specific changes:

- **New `Shape.check_post_event_state_validity` method** in `impl/src/fresh_plan/runtime/shape.py`. Signature: `check_post_event_state_validity(event: dict, state_before: WorkspaceState) -> list[ValidationFailure]`. Default impl on `Shape` base class implements the actor-cardinality check per §B.1; `GenericShape` + `MinShape` inherit unchanged (both have `actor-requirements: "none"` so the method early-returns empty list).

- **Substrate.append_event new step 2.5** in `impl/src/fresh_plan/runtime/substrate.py`. Insert between step 2 (authority check) + step 3 (pre-event-emit hook):

  ```
  # Step 2.5: post-projection state validity check (D52 §B.1)
  if self.shape is not None:
      comp_failures = self.shape.check_post_event_state_validity(event, self.state)
      if comp_failures:
          raise EventRejected(comp_failures)
  ```

  Docstring at lines 161-185 updated to list 10 ordered steps (insert step 2.5 entry; preserve numbering of existing steps 3-9 per scheme below).

- **Step numbering scheme (per pre-lock probe Q9)**: insert "step 2.5" rather than renumber-shift. Renumber-shift would move D47-locked-references (pre-event-emit hook at "step 3"; post-event-emit hook at "step 7") to step 4 / step 8, breaking cross-D-entry semantic references to the named position. Step 2.5 preserves D47 + D49 §A canonical numbering at no semantic cost. The canonical step count is now **10 (with step 2.5)** — this supersedes D49 §A's 9-count correction by addition (D49 §A's underlying correction stands; D52 adds step 2.5).

- **`FAILURE_CATEGORIES` extension** in `impl/src/fresh_plan/validator/types.py`: add `"composition-validity"` to the frozenset. Inline comment naming D52 §B.1 origin (parallel to D46 actor-seeding / D47 hook-handler / D48 adapter-attach + adapter-binding-resolution annotations).

- **3 new tests** in `impl/tests/test_composition_validity.py` (NEW file; or extend `test_substrate_boot.py` if file-creation overhead is unwanted):
  - Test 1 — **min violation**: shape with `actor-requirements: {human-actor: {min: 1}}` + workspace with 1 human-actor at boot. Emit composition-change:remove for that human-actor. Assert `EventRejected(category="composition-validity")`; state still has the human-actor (not removed; check ran on copy).
  - Test 2 — **max violation**: shape with `actor-requirements: {agent-actor: {max: 2}}` + workspace with 2 agent-actors. Emit composition-change:add for 3rd agent-actor. Assert `EventRejected`; state still has only 2 agent-actors.
  - Test 3 — **regression / none-case**: shape with `actor-requirements: "none"` (all current fixtures). Emit any composition-change:add or :remove. Assert no rejection (early-return path exercised).

  Tests use monkeypatched shape spec (parallel to D48 `_FailingAdapter` + D50 `_FailingSpecialist` patterns) to exercise cardinality logic since no current fixture defines real cardinality constraints (per pre-lock probe Q6: Phase D PractitionerShape will exercise this end-to-end; Phase B coverage uses monkeypatch).

Estimated impl size: **~30-40 lines code + 3 tests**. 190 baseline → 193 tests pass post-D52.

## D. What is NOT in this decision

The seven explicit DEFERS surfaced by pre-lock probe (per probing.md Procedure 3 + Q1-Q9 + D48 §D + D50 §D pattern):

- **D-1 — Check timing alternatives (post-projection-warn / hook-based pre-projection)**: D52 locks pre-projection-simulate at substrate step 2.5. Post-projection-warn (silent-substitution per CLAUDE.md "No silent substitution") + hook-based (shape-author burden without framework enforcement) explicitly rejected in §B.1 rationale. Re-evaluate if Phase D PractitionerShape impl surfaces a use-case that the canonical timing doesn't cover.

- **D-2 — `shape.actor_requirements` semantics extension beyond cardinality**: D52 operationalizes the schema's `oneOf` clause — string `"none"` or `{subtype: {min, max?}}` cardinality. Future shape policies may want role-correlated constraints (e.g., "every claim event's role=author MUST be backed by a role=attester within N events") or dynamic computed minimums. These are Phase D PractitionerShape concerns; D52 doesn't lock semantics it doesn't operationalize.

- **D-3 — Non-actor binding-kinds post-projection validity**: composition-change schema admits `binding-kind ∈ {substrate-binding, adapter-binding, specialist-binding, actor, extension}` × `change-type ∈ {add, remove, update}` = 15 cells. `event_chain.apply_event_to_state` (lines 56-63) implements 2 cells (actor:add, actor:remove). The other 13 cells no-op at projection. Their post-projection validity contracts are deferred to Phase C+ when hot-reconfiguration use-cases surface (adapter hot-attach; specialist hot-bind; substrate hot-swap). Per pre-lock probe Q2 quiet-assumption surfacing.

- **D-4 — `composition-change:update` projection semantics**: `change-type="update"` is admitted by the schema but unimplemented in `apply_event_to_state` for any binding-kind. D52 does NOT lock `update` semantics (the post-projection check would have nothing to validate against — no projection occurs). Per pre-lock probe Q4: likely an oversight in D39 closure work rather than a deliberate scope-cut. Future D-entry locks `update` semantics together with its post-projection-validity contract once a real use-case emerges.

- **D-5 — State-change post-projection state validity**: composition-change ≠ state-change. D52 scopes to composition-change events. State-change events (work-unit-created, work-unit-status, scope) may have their own post-projection validity gaps (work-unit-kind payload-schema validation; shape-policy work-unit transition rules). D51 partial coverage for work-unit-created references (D51 §B.1); remaining gaps belong to a future cluster or D51 follow-on.

- **D-6 — `composition-change.payload.record` schema validation against binding-kind-specific schema**: schema description (payload-composition-change.schema.json:26-28) names this validation as aspirational ("validated against the relevant kind schema by the framework conformance validator, not by this envelope schema"); runtime impl does NOT enforce. D52 doesn't close this gap — it's a separate validation surface (D29 §validation flow territory) that could land via D51 follow-on or a new entry. Per pre-lock probe verification of Claim 6.

- **D-7 — Phase D end-to-end exercise of actor-requirements cardinality**: D52 locks the contract + impl + tests (monkeypatched shapes). All 17 current fixture shapes use `actor-requirements: "none"` (verified by grep), so the new step 2.5 is exercised only by Phase B monkeypatched tests until Phase D PractitionerShape ships with real cardinality constraints (e.g., `{human-actor: {min: 1, max: 1}}` per fresh-plan's accountability-anchor framing). Per pre-lock probe Q6: this is the canonical "untested forward-bar" pattern — contract locked at Phase B; real-fixture exercise at Phase D.

Other items NOT in this decision:

- **No retroactive rewrite of D10, D13, D39 entries** — append-only ledger discipline. D52 EXTENDS those entries; their original wording stands.
- **No change to D13's `actor_requirements` slot contract** — D52 operationalizes existing schema semantics; no schema amendment.
- **No new typed exception** — reuses `EventRejected` (parallel to D46/D48 pattern; distinct from D48/D50 which introduced new typed exceptions for distinct domains).
- **No change to canonical substrate step ordering at semantic level** — D52 inserts step 2.5 at the named position; existing steps 3-9 keep their canonical positions per D47 + D49 §A. Step count goes 9 → 10; cross-D-entry references at named positions remain stable.

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: lock detection + surface + recovery for post-projection state validity of composition-change events affecting actors. Sixth cluster supersedes per D45 §C (the last). Operationalizes `shape.actor_requirements` (currently unused contract slot).
- **WHO**: enforced by *shape (policy)* — Shape base method `check_post_event_state_validity` reads `actor_requirements` from the shape spec + simulates projection. *substrate (runtime)* — substrate.append_event step 2.5 invokes the shape method + raises `EventRejected` on failures. *framework-validator (B1)* — unaffected (B1 is composition-time; D52 is per-event-time).
- **FAILS** (recursive — what happens if impl doesn't honor this contract?): *Detection*: detection-surface-recovery audit at next workstream-completion or phase-boundary checkpoint (per probing.md Procedure 2 + Checkpoint cadence). *Surface*: audit findings list + failing tests if impl regresses. *Recovery*: impl-follow-through commit closes; or supersedes entry sharpens.
- **CROSS**: D10 (event kind — composition-change is a core payload-subtype; D52 extends per-event runtime semantics without altering kind contract); D13 (shape kind — `actor_requirements` slot is now consumed at runtime by D52's new method); D30 §4 (per-event runtime checks — D52 adds a NEW per-event check class distinct from identity-resolution per Q5); D39 (state-is-fully-derived-from-event-chain — D52 preserves this property; check runs pre-projection on copy, state mutates only after pass); D44 (queued dispatch — preserved; D52 runs before chain append at step 4); D45 (standing requirement; canonical citation); D46 (precedent for cluster supersedes structure + reuses-EventRejected + new-FAILURE_CATEGORIES-entry pattern); D47 §C (canonical step ordering preserved; D52 inserts step 2.5 at named position); D48 §E (FIRED precedent — refined skip rule for new-contract content); D49 §A (canonical step-count 9 from 7; D52 makes it 10 by insertion at 2.5); D50 §E (FIRED precedent — single-path scope + new contract content).
- **DEFERS**: per §D — D-1 timing alternatives; D-2 actor_requirements semantics extension; D-3 non-actor binding-kinds; D-4 composition-change:update; D-5 state-change post-projection; D-6 record schema validation; D-7 Phase D end-to-end exercise.

## E. Pre-lock probe disposition (per probing.md Procedure 3 refined-skip rule)

D52 **FIRED** the pre-lock probe per refined-skip rule + D48 §E + D50 §E precedent: D52 introduces NEW contract content (not pure pattern application). The three new-contract elements (per probing.md Procedure 3 refined skip criteria):

1. **New shape runtime method** `check_post_event_state_validity` — NEW contract surface on Shape base class (parallel to but distinct from existing `check_authority`).
2. **New FAILURE_CATEGORIES entry** `"composition-validity"` — NEW category vocabulary.
3. **New substrate step 2.5** in the canonical append_event sequence — NEW composition framing (changes locked 9-step ordering per D47 §C + D49 §A correction to 10 steps via insertion-at-named-position scheme).

This distinguishes from D46/D47/D51 SKIP precedent (pure pattern application of existing typed exceptions + categories + framings).

Probe brief shape: investigation-bias variant per probing.md Procedure 3 brief menu — code-claim verification + quiet Phase C/D assumption surfacing.

**Probe outcome (2026-05-17 session)**: 9/10 load-bearing code claims VERIFIED against direct source reads (substrate.py 9-step ordering; shape.py:77-78 unused accessor; event_chain.py:52-63 actor-only projection; workspace_state.py add_actor without validation; payload-composition-change schema record aspirational; shape.schema.json actor-requirements oneOf; all 17 fixtures `"none"`; reuse-EventRejected pattern; D48/D50 §E FIRED). Claim 9 had minor caveat: "D46/D48/D51 pattern" — verified that D51 did NOT extend FAILURE_CATEGORIES (its categories landed in D48 [impl]); sketch wording corrected to "D46/D48 pattern" in §B.1 + §D framing. **7 quiet assumptions surfaced + named as explicit DEFERS in §D** (D-1 through D-7).

**Precedent for future cluster supersedes with new contract content**: D52 §E continues the FIRED pattern (D48 §E + D50 §E). Future audit-driven cluster supersedes that introduce new contract content SHALL run pre-lock probe per the refined-skip rule, citing D48 §E + D50 §E + D52 §E as precedent. The cluster-supersedes phase per D45 §C is now COMPLETE with D52; future D-entries return to normal Sketch-then-lock + per-entry pre-lock probe discipline rather than the cluster-batch pattern.

## Rationale

The 2026-05-12 audit identified composition-change post-projection state validity as the sixth + final SUSPECT cluster per D45 §C. D46-D51 closed the prior five (boot-procedure / subscriber-dispatch / adapter / specialist / validation). D52 closes the composition-change cluster — completing the cluster-supersedes phase of the Bref bounded-fill plan.

Honest cluster sizing: D52 addresses 1 SUSPECT (per D45 §C item 6 canonical wording). Aligns with D50's honest 1-path scope. Smaller than D46/D47/D48 (3 each) + D51 (2). Per the structural-pattern-completion failure mode (D49 first-pass scope inflation lesson; Clippy upstream D1 scope-cardinality-honesty sub-check), do NOT inflate to match precedent cluster shapes. Roadmap row #19 wording "+ composition-change shape authority interaction" was scope-inflation in prior session work; D52 honors D45 §C item 6 canonical naming over derived-document inflation.

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): D52 is **specification** — typed exception (reused) + category vocabulary + check-method contract + step-ordering convention. The shape policy enforced is shape-author-declared (`actor_requirements` per shape impl). Phase D PractitionerShape will populate the cardinality declarations; D52 makes the framework capable of enforcing whatever cardinality shape impls declare.

D52 follows D46-D51 structural template with §E FIRED disposition (per D48 + D50 precedent for new contract content). The cluster-supersedes phase per D45 §C is now COMPLETE; remaining Bref deliverables (slot-pass; D33 migration-safety; D38 Sana worked-example; Bref output entry; Phase B closure entry) move to next phase of work.

**Cross-references**: D5 §I3 (accountability anchor — operationalized by composition-change events being subject to shape-policy validation, not just identity check); D7 §3 + §4 (workspace state contents + composition mutability — D52 enforces shape policy at composition mutation); D10 (event kind — composition-change is a core payload-subtype per D10; D52 extends per-event runtime semantics); D13 (shape kind — `actor_requirements` slot consumed at runtime by D52's new method); D29 §validation flow (D52 extends step 6 cross-kind portion with per-event composition-validity); D30 §4 (per-event runtime checks — D52 adds a NEW per-event check class); D34 §A.5 (current-state resolution — preserved; D52 simulates projection on copy of state); D39 (state-is-fully-derived-from-event-chain — preserved; D52 runs pre-projection on copy; real state mutates only after check passes; chain-replay equivalence maintained); D44 (queued dispatch — preserved); D45 (standing requirement; canonical citation); D45 §C item 6 (this cluster's named SUSPECT — composition-change cluster); D46 (precedent for cluster supersedes structure + reuse-EventRejected + new-FAILURE_CATEGORIES-entry pattern); D47 §C (canonical step ordering — D52 inserts step 2.5 at named position preserving D47-referenced positions); D48 §B.1 (precedent for new-step-insertion semantics); D48 §E (FIRED pre-lock probe precedent for new contract content); D49 §A (step-count correction from 7 to 9; D52 makes it 10 by insertion); D50 §B.1 (precedent for single-path cluster + new shape-method surface); D50 §E (FIRED precedent — single-path scope + new contract content); D51 §B.2 (precedent for fail-closed silent-skip removal vs D52's no-silent-substitution rationale per CLAUDE.md global rule); probing.md §"Pattern-completion over pattern-questioning" (scope-cardinality-honesty applied to D52's 1-path scope); probing.md Procedure 3 refined-skip rule (D52 §E disposition); 2026-05-17 D52 pre-lock probe (cited in §E; surfaced D-1 through D-7).
