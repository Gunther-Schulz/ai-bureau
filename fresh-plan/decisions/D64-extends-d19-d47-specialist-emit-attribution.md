# D64 — 2026-05-17 — Extends D19 + D47 — specialist emit-attribution mechanism; runtime enforcement of declared-event-emissions[]

**Decision (substantive; closes D62 §B §B-6 — Bref-followon "specialist.declared-event-emissions[] runtime enforcement")**: Events emitted via the specialist runtime path now carry an optional `emitting-specialist` slot (instance-identifier reference to the bound specialist binding-id), and the substrate's per-event check at step 1 (D30 §4 runtime portion) validates that the event's `payload-subtype` is in the emitting specialist's `declared-event-emissions[]` vocabulary (D19). Mechanism: `specialist.attach_workspace` wraps `workspace._emit_event` as a closure pre-filling `emitting_specialist=<self-binding-id>`; `workspace._emit_event` accepts the kwarg and threads it to the event dict; `per_event_checks.check_event_references` adds a new check block that rejects via `EventRejected(category="vocabulary"; path="event.emitting-specialist")` per D30 §3 + D59 pattern. Reuses existing `EventRejected` + `"vocabulary"` category (no new FAILURE_CATEGORIES entry per C3). Non-specialist emit paths (`ActorHandle.emit_claim/emit_action/emit_state_change`; boot.py system events; future adapter emits) do NOT set the slot; the check is skipped when the slot is absent. Per A2 STRICT lock: empty `declared-event-emissions[]` = zero allowed (per D19 required-with-explicit-empty + no-silent-substitution discipline). Pre-lock probe FIRED per probing.md Procedure 3 refined-skip rule + D48 §E + D50 §E + D52 §E precedent: D64 introduces new contract content (new event slot + new per-event check site) beyond pure pattern application (see §E).

## A. Scope of cluster

**Honest cluster cardinality: 1 path**. D62 §B §B-6 ("specialist.declared-event-emissions[] runtime enforcement") names exactly one bounded cheap-impl follow-through. D64 operationalizes it as one mechanism with a single point of attribution-stamp (closure-wrap at attach time) and a single point of vocabulary-check (per_event_checks step 1).

The path:

- **A.1 Specialist emit-attribution + vocabulary check**: `specialist.attach_workspace` wraps `workspace._emit_event` as a closure that pre-fills `emitting_specialist=<self-binding-id>` (using the binding-id already looked up at specialist.py:223-226 for activation-scope error-path naming per D55 §B.1). `workspace._emit_event` accepts an optional `emitting_specialist: Optional[str] = None` kwarg and threads it to the event dict (parallel to `work_unit_id` at workspace.py:441-442). Substrate's `append_event` step 1 builds a `specialist_emissions_map: dict[str, set[str]]` from `specialist_instances` and passes it to `check_event_references`; the new check block fires when the event has `emitting-specialist` set, looks up the allowed set, and emits `ValidationFailure(category="vocabulary", path="event.emitting-specialist")` on miss.

Out of scope (per §D):

- Adapter emit-attribution (adapters emit via `workspace._emit_event` same as specialists; deferred per §D D-1).
- Replay-validation of emit-attribution under D40 query interface (deferred per §D D-2; Phase C+ persistence layer).
- Cross-specialist emission delegation (deferred per §D D-3; Phase D PractitionerShape territory).
- `adapter.call` outcome events (deferred per §D D-4; Phase C real-wire surfaces concrete need).
- Subclass override semantics (`setdefault` admits override; documented but not exercised — deferred per §D D-5).

## B. Triad applied per path

### B.1 — Specialist emit-attribution + vocabulary check

| Triad element | Lock |
|---|---|
| **Detection** | NEW optional event slot `emitting-specialist` (oneOf: null OR instance-identifier per event.schema.json, mirroring `work-unit-id` slot at lines 52-58). NEW closure-wrap at `specialist.attach_workspace` (specialist.py:218-228 — replaces direct `self._emit_event = workspace._emit_event`): the closure pre-fills `emitting_specialist=<self-binding-id>` via `setdefault` (subclass may override at emit-call-site if needed). NEW check block in `per_event_checks.check_event_references` after the payload-subtype check (before D59 §B.1 block): when `event.get("emitting-specialist") is not None`, validate that `event.payload-subtype` is in `specialist_emissions_map[emitter]` — the per-bound-specialist emissions vocabulary set built from `sp.declared_event_emissions`. Per A2 STRICT lock: empty `declared-event-emissions[]` is the explicit-empty case (per D19 wording + no-silent-substitution global rule) — zero allowed. |
| **Surface** | `EventRejected(failures=[ValidationFailure(category="vocabulary", path="event.emitting-specialist", value=<binding-id>, reason="specialist <bid> emitted payload-subtype <subtype> which is not declared in its declared-event-emissions[] vocabulary")])`. Reuses existing `EventRejected` typed exception + `"vocabulary"` category per D30 §3 + D59 pattern; no new exception type, no new `FAILURE_CATEGORIES` entry (per C3). Identity gap (event names a specialist binding-id not bound in workspace) surfaces via `category="identity"` parallel to D51 §B.1 / D34 §A.5 identity surfaces — defensive, expected unreachable in practice since the closure-wrap stamps a known binding-id. |
| **Recovery** | Event rejected at substrate step 1 (existing per-event check site; no new step inserted). State NOT mutated; chain NOT appended (D30 §4 timing-modes: per-event failures REJECT). Composes with D47 §B.1 SubscriberDispatchError aggregation: when a subscribed specialist's `on_event` delegates to a `handle_skill` that emits off-vocabulary, the `EventRejected` raised inside the on_event call is captured per D47 §B.1 into `_subscriber_failures` and aggregated as `SubscriberDispatchError` after the outer drain. Direct-emit callers (e.g., the specialist's own `handle_skill` called directly) see the raw `EventRejected`. Caller fixes the specialist spec's `declared-event-emissions[]` to include the offending subtype OR removes the offending emit. |

**Rationale for closure-wrap-at-attach-time (per pre-lock probe Q1)**: alternatives considered:
- (a) **Closure-wrap-at-attach-time** [chosen]: closure captures binding-id at attach-time (immutable; specialist subclasses calling `self._emit_event` automatically inject attribution); `setdefault` semantics admit subclass override at emit-site if needed.
- (b) **Specialist subclass injects attribution at every emit-site**: rejected — forgetting at any subclass call site is silent-substitution (silent miss of the check).
- (c) **workspace._emit_event looks up the calling specialist via stack inspection / context-variable**: rejected — too magical; brittle to async/thread changes; framework-internal coupling beyond what D17 specialist boundary admits.

The closure-wrap pattern is parallel to how `_adapters` dict-injection works (specialist.py:275) — wire-time configuration cached on the specialist instance.

### B.2 — Composition with D47 §B.1 + D50 §B.1

When a subscribed specialist's `on_event` (D37 event-driven coordination) delegates to a `handle_skill` body that emits off-vocabulary, the `EventRejected` (raised by the substrate's per-event check at step 1 of the nested `append_event` call) propagates up through `handle_skill` → `on_event`. Per D47 §B.1 + substrate.py:310-320 aggregation, the exception is captured into `_subscriber_failures` and aggregated as `SubscriberDispatchError` after the outer drain completes. This composes with D50 §B.1 `SkillExecutionError` semantics: a specialist may choose to catch `EventRejected` inside its `handle_skill` body and re-raise as `SkillExecutionError(category="domain-error", original=EventRejected)` for uniform skill-failure surface; or propagate raw `EventRejected` if the off-vocabulary emit is a hard spec violation rather than a recoverable domain error.

### B.3 — Composition with existing per-event checks

The new check block sits in `per_event_checks.check_event_references` between the existing payload-subtype core/extension-registered check and the D59 §B.1 open-vocab payload-body validation. Order rationale: the payload-subtype core/extension-registered check is a prerequisite (an unregistered subtype is rejected before the emit-attribution check matters); the D59 open-vocab check validates payload-body slots within registered subtypes (independent dimension). The three checks compose without overlap: subtype-registration (D30 §3), specialist-emission-vocabulary (D64 §B.1), payload-body-vocabulary (D59 §B.1).

## C. Impl follow-through (same commit per C7 [design+impl])

Specific changes landed in this commit:

- **`schemas/event.schema.json`** — adds `emitting-specialist` to the properties block (after `work-unit-id`, mirroring its `oneOf: [null, instance-identifier]` shape). Existing events without the slot still validate (`unevaluatedProperties=false` admits the slot because it's now in the properties enumeration). ~8 LOC.

- **`impl/src/fresh_plan/runtime/specialist.py`** — replaces the direct `self._emit_event = workspace._emit_event` (was specialist.py:219) with a closure `_wrapped_emit(**kwargs)` that does `kwargs.setdefault("emitting_specialist", _binding_id_for_emit)` before forwarding. Reuses the binding-id already computed at specialist.py:223-226 for activation-scope error-path naming per D55 §B.1 (no duplicate lookup). ~12 LOC.

- **`impl/src/fresh_plan/runtime/workspace.py`** — adds `emitting_specialist: Optional[str] = None` to `_emit_event` signature; threads to event dict conditionally (`if emitting_specialist is not None: event["emitting-specialist"] = emitting_specialist`), parallel to `work_unit_id` at lines 441-442. ~4 LOC. Docstring updated to name the D64 §B.1 stamping behavior + the ActorHandle non-attribution path.

- **`impl/src/fresh_plan/runtime/per_event_checks.py`** — adds `specialist_emissions_map: Optional[dict[str, set[str]]] = None` kwarg to `check_event_references`; new check block after the payload-subtype core/extension-registered check + before the D59 §B.1 open-vocab block. Pattern matches existing D51 §B.1 / §B-3 / §B-4 / §B-7 check blocks (conditional fire on slot presence + map availability). ~28 LOC.

- **`impl/src/fresh_plan/runtime/substrate.py`** — `append_event` step 1 builds `specialist_emissions_map` via dict-comp from `specialist_instances` + passes to `check_event_references`. ~10 LOC.

- **NEW test file `impl/tests/test_emit_attribution.py`** — 3 tests:
  - Test 1 — **emit-within-vocabulary admitted**: workspace-generic-specialist fixture; `GenericSpecialist` declares-emits `action`; invoke `do-task` skill → action event accepted; assert event in chain carries `emitting-specialist="primary-specialist"`.
  - Test 2 — **emit-off-vocabulary rejected**: subclass `_OffVocabSpecialist` whose `emit_offvocab` method emits a `claim` event via `self._emit_event` despite spec declaring only `action`; assert `EventRejected` raised with `category="vocabulary"; path="event.emitting-specialist"`; assert reason names `"claim"` + `"declared-event-emissions"`.
  - Test 3 — **non-specialist emit no attribution**: `ActorHandle.emit_claim` on the workspace's `agent-primary` actor → event admitted; assert `"emitting-specialist"` key NOT present in returned event dict NOR in the chain event.

Estimated impl size: **~62 LOC + 3 tests**. Baseline (post-D65) 226 → 229 post-D64 [impl]. **Verified pass**: all 229 tests pass per `pytest -q` run.

No new module, no new exception type, no new `FAILURE_CATEGORIES` entry. Reuse-only per C3.

## D. What is NOT in this decision

The five explicit DEFERS (per probing.md Procedure 3 + Q1-Q9 pattern):

- **D-1 — Adapter emit-attribution**: adapters also emit via `workspace._emit_event` (D16 + D48 §B.2 specifies adapter call-outcome events). D64 scopes to specialist emit path only — adapters do not currently stamp `emitting-specialist` (semantically wrong slot name anyway). A future Bref-followon could lock `emitting-adapter` slot + `declared-event-emissions[]` parallel for adapters; D64 doesn't pre-commit shape. Reuses identical mechanism (closure-wrap at `Adapter.attach_workspace`; analogous map at substrate); follows-on naturally if Phase C real-wire surfaces use-case.

- **D-2 — Replay-validation under D40 query interface**: per D40 §A, workspace state derives from events 0..n. When the chain is replayed (e.g., for `state_at(seq_n)`), the per-event checks at step 1 are NOT re-run — the chain is treated as already-validated (events that landed passed their checks at append time). D64's emit-attribution check inherits this discipline: replay does not re-validate `emitting-specialist` against the (possibly different) specialist set at replay-time. Phase C+ persistence layer surfaces whether replay-validation is needed (e.g., loading an old chain whose `emitting-specialist` references a now-unbound specialist binding-id).

- **D-3 — Cross-specialist emission delegation**: a specialist may want to emit events ATTRIBUTED TO ANOTHER specialist (e.g., a coordinator specialist emitting on behalf of a worker specialist). The `setdefault` semantics admit subclass override at emit-call-site (subclass passes `emitting_specialist=<other-bid>` explicitly), but the framework does NOT validate the delegation authority. Phase D PractitionerShape territory: a PractitionerShape may declare which specialists may delegate to which; D64 leaves this open. Mechanism is forward-compatible (setdefault admits the override) — no DR amendment needed when delegation lock lands.

- **D-4 — `adapter.call` outcome events (Phase C)**: when a specialist invokes a bound adapter via `adapter.call(...)`, the adapter may emit an outcome event reporting the call result. Whether that outcome event is attributed to the calling specialist OR to the adapter (D-1) is an open framing question. D64 doesn't lock; Phase C real-wire (RAGSpecialist + rag-via-mcp adapter) surfaces the concrete need. Current Phase B stub `RAGSpecialist.handle_skill` emits its own action event THEN calls adapter (specialist.py:355-376) — adapter result returned but no adapter-side emit.

- **D-5 — Subclass override behavior**: the closure's `setdefault` lets a subclass call `self._emit_event(emitting_specialist=<other-bid>, ...)` or `self._emit_event(emitting_specialist=None, ...)` to override / suppress the default attribution. D64 documents the affordance but does not lock semantics for override (per D-3) or suppression. A subclass that passes `emitting_specialist=None` explicitly skips the check (semantically: "emit as the framework, not as me"); not currently exercised. Future use-case (e.g., specialist re-emitting a system-shaped event on behalf of boot procedure) surfaces a need to lock; D64 leaves open.

Other items NOT in this decision:

- **No new event step in substrate.append_event ordering** — emit-attribution check rides inside the existing step 1 (per-event check) call site; no insertion into the D47 §C / D49 §A / D52 step ordering. Canonical step count remains 10 (per D52's insertion of step 2.5).
- **No retroactive rewrite of D19** — D19 declared `declared-event-emissions[]` as required-with-explicit-empty; D64 operationalizes per A2 STRICT reading without amending D19. Append-only ledger preserved.
- **No new `FAILURE_CATEGORIES` entry** — reuses `"vocabulary"` per C3 + D30 §3 + D59 pattern.

## Decision-shape template self-application

- **WHAT**: lock the mechanism by which specialist-emitted events carry attribution to their emitting specialist binding-id AND lock runtime enforcement of `declared-event-emissions[]` vocabulary against that attribution. Closes D62 §B §B-6.
- **WHO**: enforced by *substrate (runtime)* — `append_event` step 1 builds `specialist_emissions_map` and passes it to the check. *specialist (runtime)* — `attach_workspace` wraps `_emit_event` with the closure. *workspace (runtime)* — `_emit_event` threads the kwarg. *framework-validator (B1)* — unaffected (slot is optional in schema). *shape (policy)* — unaffected (vocabulary is specialist-declared, not shape-declared).
- **FAILS**: *Detection*: per_event_checks new check block fires when event has `emitting-specialist` set AND the subtype is not in the emitter's declared set. *Surface*: `EventRejected(category="vocabulary"; path="event.emitting-specialist")`. *Recovery*: event NOT appended; chain integrity preserved; caller fixes spec OR removes offending emit.
- **CROSS**: D10 (event kind — D64 adds optional slot per D23 pattern); D13 (shape kind — independent dimension; shape policy is role-vocabulary, D64 is specialist-vocabulary); D17 (capability vocabulary — specialist runtime owns); D19 (specialist kind — `declared-event-emissions[]` becomes runtime-enforced); D29 (extension manifest — unchanged; specialist spec was already loadable); D30 §3 (`vocabulary` category — reuse); D30 §4 (per-event runtime check — D64 extends step 1 with new check block); D37 (cross-specialist coordination via events — D64 makes event provenance explicit); D45 §C (cluster supersedes precedent for FIRED probe on new contract content); D47 §B.1 (`SubscriberDispatchError` aggregation composes when off-vocab emit happens inside `on_event`); D52 §E (FIRED probe precedent for new contract content); D62 §B §B-6 (closes the named follow-through); D65 §E (SKIP precedent — D64 distinguishes by introducing new event slot + new check site).
- **DEFERS**: per §D — D-1 through D-5.

## E. Pre-lock probe disposition (per probing.md Procedure 3 refined-skip rule)

D64 **FIRED** the pre-lock probe per refined-skip rule + D48 §E + D50 §E + D52 §E precedent: D64 introduces NEW contract content (not pure pattern application). The two new-contract elements (per probing.md Procedure 3 refined skip criteria):

1. **New event slot** `emitting-specialist` on the event envelope schema — NEW contract surface on the event kind (parallel to D23's `work-unit-id` addition, but adding an attribution dimension beyond the existing identity dimensions of `actors[]` + `work-unit-id`).
2. **New per-event check site** in `per_event_checks.check_event_references` — NEW check block (the 4th vocabulary/identity discriminant on event content after subtype-registration + role-vocabulary + payload-body-vocabulary).

This distinguishes from D65 §E SKIP precedent (pure pathway operationalization of D56 + D57 locked content). D64 stays inside D45 §C item 4 cluster framing (specialist) but adds new contract content beyond what D50's typed-exception forward-bar covered.

**Probe brief shape (executed at design time per CLIPPY-COMPANION investigation-bias variant)**:

- **Code-claim verification**: A1 (specialist emit funnel) verified by grep impl/src/ for `substrate.append_event` call sites: workspace.py:443 (canonical specialist emit path) + boot.py:511 (boot-time actor seeding system event) + boot.py:549 (boot lifecycle-transition system event); boot.py paths are framework-emitted and correctly omit emitting-specialist. F2-F8 verified per tracker. **9/9 load-bearing code claims VERIFIED against direct source reads** (specialist.py:223-226 binding-id lookup; event.schema.json:7-58 properties block + unevaluatedProperties=false admission shape; substrate.py:158 specialist_instances field; specialist.json fixture declared-event-emissions structure; per_event_checks.py:35-44 signature pattern; workspace.py:408-422 _emit_event signature; D47 §B.1 + substrate.py aggregation; existing 'vocabulary' category in FAILURE_CATEGORIES).

- **Quiet-assumption surfacing**: 5 explicit DEFERS surfaced + named in §D (D-1 adapter emit-attribution; D-2 replay-validation; D-3 cross-specialist delegation; D-4 adapter.call outcomes Phase C; D-5 subclass override behavior). A2 STRICT lock (empty list = zero allowed) called out explicitly in §B.1 + decision bold per no-silent-substitution discipline.

- **Mechanism alternatives considered** (per §B.1 Q1): closure-wrap-at-attach-time (chosen) vs subclass-injects-at-every-emit-site (rejected — silent-substitution risk) vs workspace-stack-inspection (rejected — magical / brittle). Choice rationale captured in §B.1 rationale block.

**Precedent for future Bref-followon D-entries**: D64 §E continues the FIRED pattern (D48 §E + D50 §E + D52 §E). Future bounded Bref-followon entries that introduce new event slots OR new per-event check sites SHALL run pre-lock probe per the refined-skip rule. Pure pathway lock with no new contract content (e.g., D65) continues to SKIP per D65 §E.

## Rationale

D62 §B §B-6 named "specialist.declared-event-emissions[] runtime enforcement" as one of 5 cheap-impl follow-throughs deferred from Phase B closure. D19 locked the slot as required-with-explicit-empty, but the runtime never consulted it — specialists could emit any payload-subtype without consequence, leaving the spec's emission vocabulary as documentary rather than load-bearing. D64 closes the gap with the minimal mechanism: an optional event slot for attribution + a per-event check that fires when the slot is set.

The closure-wrap-at-attach-time pattern preserves specialist-author ergonomics — subclasses continue to call `self._emit_event(actor_id=..., payload_subtype=..., payload=...)` with no awareness of the attribution layer. The framework stamps automatically; subclasses opting into override (Phase D delegation use-cases) do so via explicit kwarg override per the `setdefault` semantics.

The A2 STRICT lock (empty list = zero allowed) follows no-silent-substitution discipline: D19 required-with-explicit-empty means an empty list is a deliberate "this specialist declares zero emissions" statement, not a "we forgot to declare" gap. A specialist with empty `declared-event-emissions[]` that nevertheless emits is a spec-violation; framework rejection at emit-time is the correct fail-closed response.

Per the durability bet: D64 is **specification** — typed exception (reused) + category (reused) + check-block contract + closure-wrap convention. The implementation is ~62 LOC + 3 tests. The decision's value is in operationalizing D19's deferred slot and closing the D62 §B-6 named follow-through, making specialist emission vocabulary load-bearing rather than documentary.

Honest 1-path scope per D50 + D52 precedent. Scope-cardinality-honesty discipline applied (per probing.md Pattern-completion failure mode + D49 first-pass lesson + Clippy upstream D1 sub-check). D62 §B §B-6 is exactly one path; D64 does not inflate to bundle adapter emit-attribution (D-1 explicit deferral) or replay-validation (D-2 explicit deferral).

**Cross-references**: D10 (event kind — D64 adds optional slot per D23 pattern; payload subtype core enumeration unchanged); D13 (shape kind — orthogonal; shape policy is role-vocabulary; specialist-vocabulary is specialist-declared); D17 (capability vocabulary — specialist runtime owns); D19 (specialist kind — required-with-explicit-empty `declared-event-emissions[]` becomes runtime-enforced; A2 STRICT lock per §B.1); D23 (event-gains-work-unit-id-slot — precedent pattern for optional slot addition); D29 (extension manifest validation — unchanged); D30 §3 (`vocabulary` category — reuse per C3); D30 §4 (per-event runtime check — D64 extends step 1 with new check block); D34 §A.5 (current-state resolution — D64 inherits; emit-attribution check is vocabulary-class, not identity-class except for unbound-emitter defensive surface); D37 (cross-specialist coordination via events — D64 makes provenance explicit); D45 §C (cluster supersedes precedent for FIRED probe on new contract content per D48 §E + D50 §E + D52 §E); D47 §B.1 (SubscriberDispatchError aggregation composes when off-vocab emit happens inside on_event; see §B.2); D50 (specialist cluster supersedes — D64 follows D50's 1-path honest scope precedent); D52 §E (FIRED precedent for new contract content); D59 §B.1 (open-vocab payload-body validation — D64's check block sits adjacent; composition per §B.3); D62 §B §B-6 (closes the named follow-through); D65 §E (SKIP precedent — D64 distinguishes by introducing new event slot + new check site); probing.md §"Pattern-completion over pattern-questioning" (scope-cardinality-honesty applied to D64's 1-path scope); probing.md Procedure 3 refined-skip rule (D64 §E FIRED disposition).

## Honest basis caveats

- **Read directly this session**: event.schema.json (full body); specialist.py (full body); workspace.py:22-145 (ActorHandle + WorkUnitHandle) + 380-460 (_emit_event); per_event_checks.py (full body); substrate.py:130-260 (state declarations + append_event entry); test_per_event_checks.py (head); test_specialist.py:1-260 (existing tests including SkillExecutionError + subscriber dispatch); fixtures/workspace-generic-specialist/workspace.json + specialist.json; decisions/D65 (full body — most recent SKIP precedent); decisions/D52 head + §B.1 + §E (FIRED precedent); D62 (§B §B-6 close); `.ai/constraints.yaml` (C1-C7); `.ai/investigation/tracker-unit-002.yaml` (full tracker); CLAUDE.md fresh-plan section.
- **Cited via tracker-unit-002.yaml + cross-references (not freshly Read in full this session)**: D10, D13, D17, D19, D23, D29, D30 §3 + §4, D34 §A.5, D37, D45 §C, D47 §B.1, D50, D59, probing.md §"Pattern-completion" + Procedure 3 — used as cross-references per tracker findings F1-F8.
- **Inferred**: LOC estimates (~8 schemas + ~12 specialist + ~4 workspace + ~28 per_event_checks + ~10 substrate = ~62) verified against the actual edits. Test count arithmetic (226 → 229) verified by running pytest before AND after.
- **Open / Flagged**: none load-bearing — the §D defers list (D-1 through D-5) names known deferrals; all are explicitly out-of-scope rather than open questions hanging on D64's lock. The `setdefault`-admits-subclass-override affordance is documented but unexercised; future delegation lock per D-3 surfaces semantics without amending D64.
