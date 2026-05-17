# D55 — 2026-05-17 — Extends D19 — specialist.activation-scope interpretation layer + minimal grammar

**Decision (substantive; extends-D19 operationalization)**: The `activation-scope` slot on the specialist kind (D19) is operationalized with a minimal grammar (literal `"always"` OR a single-field structured predicate `{"when": {"payload-subtype": <value>}}`) interpreted by the substrate at pre-dispatch time in the subscriber loop — a coarser specialist-level gate evaluated BEFORE the existing per-subscription `payload-subtype` + `qualifier` filter. Honest 1-path scope per D52 + D50 precedent. Full DSL design (multi-field predicates, scope-state predicates, expression operators) deferred to Phase D PractitionerShape per D42. Pre-lock probe FIRED per probing.md Procedure 3 refined-skip rule + D48 §E + D50 §E + D52 §E precedent: NEW contract content (new grammar surface + new substrate sub-step in subscriber-dispatch + new FAILURE_CATEGORIES entry).

## A. Scope of cluster

D19 §Contract slots defines `activation-scope` as: *"optional; when present, declares scope conditions under which the specialist is active … Detail = layer-3 formal schema."* The layer-3 detail was deferred at D19-lock; this entry closes it minimally — only enough grammar to (a) operationalize the slot at runtime and (b) not paint into a corner that a fuller Phase D DSL would have to undo.

**Honest cluster cardinality: 1 path** — operationalization of one D19 slot. Aligns with D50 + D52 single-path scope. Not inflated to D46/D47/D48's 3-path shape; activation-scope is a single contract surface.

The path covered:

- **A.1 Activation-scope evaluation at pre-dispatch time**: when an event is being dispatched in `Substrate._dispatch_event_to_subscribers` (substrate.py — currently iterates `self.specialist_subscribers`, filters per-subscription by `payload-subtype` + `qualifier`, calls `sub.on_event(event)`), a new specialist-level gate is evaluated FIRST. If the specialist's `activation_scope` evaluates false for this event, the specialist is skipped entirely (no per-subscription iteration, no `on_event` fire). If true OR if `activation_scope` is absent / equal to `"always"`, dispatch proceeds as today.

**Out of scope** (deferred per §D):

- Multi-field predicates, expression operators (AND / OR / NOT), nested predicates.
- Scope-state predicates (predicates that read workspace state beyond the in-flight event).
- Cross-specialist scope coordination.
- Scope mutation between event arrivals.
- Layer-3 `activation-scope` extension semantics beyond the minimal grammar — full DSL design lives in Phase D PractitionerShape per D42.

## B. Triad applied per path

### B.1 — Activation-scope evaluation (pre-dispatch specialist-level gate)

| Triad element | Lock |
|---|---|
| **Detection** | Two failure shapes. **Boot-time (grammar)**: when `specialist.attach_workspace` runs, a new `_parse_activation_scope` step validates the spec's `activation-scope` value against the minimal grammar (string `"always"` OR object `{"when": {"payload-subtype": <non-empty-string>}}`). Unparseable values raise. **Runtime (evaluation)**: when `_dispatch_event_to_subscribers` evaluates the parsed predicate against an in-flight event, any unexpected raise is captured rather than silently swallowed. |
| **Surface** | Boot-time: `WorkspaceBootError(category="activation-scope-grammar")` raised at attach time with structured `ValidationFailure(path="composition.specialist-bindings[binding-id=...].activation-scope", value=<offending>, reason=...)`. Reuses existing `WorkspaceBootError` typed exception (parallel to D48 §B.3 `adapter-binding-resolution` reuse pattern). New `FAILURE_CATEGORIES` entry `"activation-scope-grammar"` added to `validator/types.py` per D46/D48/D52 pattern. Runtime: evaluation raise routes through the existing D47 §B.1 `SubscriberDispatchError` aggregation — appended to `self._subscriber_failures` as the existing `(specialist_id, event_id, exception)` tuple shape; surfaces at the outer drain boundary like any other subscriber-dispatch failure. No new typed exception. |
| **Recovery** | Boot-time: workspace boot fails all-or-nothing per `WorkspaceBootError` semantics; operator fixes the manifest's `activation-scope` and re-boots. State is not partially constructed (D46-established discipline). Runtime: cascade is NOT terminated by individual evaluation failures (per D47 §B.1 semantics); the aggregate surfaces all failures at drain end via `SubscriberDispatchError`. Caller catches and handles per D47 recovery contract. |

**Composition rationale**: routing the runtime evaluation failure through D47 §B.1 `SubscriberDispatchError` rather than introducing a new typed exception is the lighter pattern (parallel to D52 reusing `EventRejected`). Evaluation is part of subscriber dispatch (it gates whether `on_event` fires for this specialist); the D47 aggregation infrastructure already exists at substrate.py. The boot-time grammar check, however, IS a new check class (parseability of a layer-3 grammar at attach time) and warrants its own category in FAILURE_CATEGORIES — symmetric with D48 §B.3 introducing `adapter-binding-resolution` for an attach-time resolution check.

### Grammar (minimal)

The locked grammar:

```
activation-scope ::= "always"                                        ; string literal
                   | { "when": { "payload-subtype": <string> } }     ; single-field predicate
```

Semantics:
- `"always"` (or absent) → predicate always returns true; specialist activates for every event reaching dispatch.
- `{"when": {"payload-subtype": "claim"}}` → predicate returns true iff `event["payload-subtype"] == "claim"`.

Evaluation occurs before the existing per-subscription `payload-subtype` + `qualifier` filter. Both layers compose: activation-scope gates the specialist as a whole; per-subscription filtering selects which of the specialist's declared subscriptions match the event.

The schema (`specialist.schema.json` — currently `activation-scope: { type: string }`) gets a `oneOf` amendment to admit either the string literal or the structured single-field object form. Amendment is additive.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

- **New `FAILURE_CATEGORIES` entry** in `impl/src/fresh_plan/validator/types.py`: add `"activation-scope-grammar"` with inline comment naming D55 §B.1 origin.

- **Schema amendment** in `fresh-plan/schemas/specialist.schema.json`: replace the bare `string` form with a `oneOf` admitting either the existing string OR the structured `{"type": "object", "required": ["when"], ...}` form. Additive.

- **New `_parse_activation_scope` helper** in `impl/src/fresh_plan/runtime/specialist.py` (~10 LOC). Called from `attach_workspace` before the adapter-binding-resolution loop. Returns parsed predicate callable stored as `self._activation_predicate`. On grammar violation: raises `WorkspaceBootError(category="activation-scope-grammar")`.

- **`Substrate._dispatch_event_to_subscribers` modification** (~15 LOC). Insert specialist-level gate BEFORE the per-subscription loop: if `sub._activation_predicate is not None and not sub._activation_predicate(event)`, `continue` to next specialist. Evaluation-raise path: wrap predicate call in `try/except Exception`; on raise, append to `self._subscriber_failures` with existing 3-tuple shape `(spec_id, event.get("id"), exc)` and `continue`.

- **3 new tests** in `impl/tests/test_activation_scope.py` (NEW file):
  - Test 1 — literal `"always"`: specialist subscribed to payload-subtype X; emit event of subtype X; assert `on_event` fired.
  - Test 2 — structured predicate match + non-match: specialist with `{"when": {"payload-subtype": "claim"}}` + two declared subscriptions; emit one claim + one action; assert `on_event` fired once for claim only.
  - Test 3 — boot-time grammar violation: manifest with malformed `activation-scope` (e.g., `{"unknown-op": "x"}`); assert `WorkspaceBootError(category="activation-scope-grammar")` at boot.

Estimated impl size: **~30 LOC + 3 tests**. Baseline (post-D54 [impl] when it lands) → +3 tests post-D55.

## D. What is NOT in this decision

- **D-1 — Multi-field predicates + expression operators**: minimal grammar admits only single-field `{"when": {"payload-subtype": <value>}}`. AND/OR/NOT, multi-field, nested expressions deferred to Phase D PractitionerShape per D42.
- **D-2 — Scope-state predicates**: predicates reading workspace state beyond the in-flight event are NOT admitted. Cross-cutting concerns warrant a dedicated D-entry.
- **D-3 — Cross-specialist scope coordination**: one specialist's `activation-scope` depending on another specialist's state / emission history. Deferred without named target.
- **D-4 — Scope mutation between event arrivals**: dynamic re-evaluation triggered by composition-change events. Current locked semantics: parse-once at attach time; predicate static post-boot.
- **D-5 — Activation-scope vs per-subscription `qualifier` overlap**: per-subscription `qualifier` filter covers some payload-subtype gating. Activation-scope is coarser (whole specialist); per-subscription is finer (which subscription). The two compose at different granularities; this entry does not collapse them.
- **D-6 — Layer-3 extension semantics for activation-scope grammar**: future shapes may want to register new top-level predicate keys (beyond `"when"`). D29 namespacing applies; registration mechanism is Phase D PractitionerShape concern.
- **D-7 — Phase D end-to-end exercise**: current Phase B fixtures use no `activation-scope` value (all specialists implicitly `"always"`). Canonical "untested forward-bar" pattern per D52 §D D-7.

## Decision-shape template self-application

- **WHAT**: lock minimal grammar + interpretation layer for D19's deferred `activation-scope` slot.
- **WHO**: enforced by *substrate (runtime)* — pre-dispatch evaluation. *specialist (impl)* — `attach_workspace` parses + stores predicate. *framework-validator (B1)* — schema-level check.
- **FAILS**: per §B.1 triad — boot-time grammar parse-failure surfaces as WorkspaceBootError; runtime evaluation raise aggregated via D47 §B.1.
- **CROSS**: D19 §"Contract slots" (operationalizes deferred slot); D29 (namespacing — D-6); D30 §4 (per-event runtime checks — activation-scope is per-specialist pre-dispatch gate); D37 (event-driven coordination — D-3 deferral); D42 (PractitionerShape — full DSL design target); D44 (queued dispatch preserved); D45 (standing requirement); D47 §B.1 (canonical reuse — runtime evaluation failures route through SubscriberDispatchError aggregation); D48 §B.3 (precedent — WorkspaceBootError + new FAILURE_CATEGORIES for attach-time check); D50 §B.1 + §E (single-path cluster precedent); D52 §B.1 + §E (single-path + new FAILURE_CATEGORIES + FIRED probe).
- **DEFERS**: per §D — D-1 through D-7.

## E. Pre-lock probe disposition

D55 **FIRED** the pre-lock probe per refined-skip rule + D48 §E + D50 §E + D52 §E precedent. NEW contract content:

1. **New grammar surface** — minimal grammar for D19's deferred slot.
2. **New substrate sub-step** — pre-dispatch specialist-level gate BEFORE the per-subscription loop.
3. **New `FAILURE_CATEGORIES` entry** `"activation-scope-grammar"`.

**Probe outcome** (this drafting session): Load-bearing code claims VERIFIED against direct source reads — `_dispatch_event_to_subscribers` iterates `specialist_subscribers` with per-subscription `payload-subtype` + `qualifier` filtering (substrate.py, Read); `_subscriber_failures` 3-tuple shape `(spec_id, event_id, exc)` (substrate.py, Read); `SubscriberDispatchError` surfaces at outer drain boundary (substrate.py, Read); `Specialist.attach_workspace` is canonical attach-time hook with WorkspaceBootError raise pattern (specialist.py, Read); `FAILURE_CATEGORIES` is closed frozenset extended per cluster supersedes (validator/types.py, Read); `activation-scope` schema currently `{type: string, minLength: 1}` (specialist.schema.json, Read); `activation_scope` accessor returns `self.spec.get("activation-scope")` with no consumers (specialist.py, Read; grep verifies). Quiet assumptions surfaced + named as explicit §D DEFERS.

**One composition point**: runtime evaluation failures route through D47 §B.1 `SubscriberDispatchError` rather than a new typed exception. Honest decision — activation-scope evaluation IS part of subscriber dispatch (it gates `on_event`); the existing aggregation infrastructure absorbs evaluation-raise without contract bloat.

## Rationale

D19 deferred the `activation-scope` slot's layer-3 detail explicitly. D55 closes the minimal version of that deferral — enough grammar to operationalize the slot without painting into a corner that Phase D PractitionerShape's fuller DSL would have to undo. The grammar admits exactly two forms: literal `"always"` and a single-field structured predicate `{"when": {"payload-subtype": <string>}}`. Both are forward-compatible with a fuller DSL.

Honest 1-path scope per D50 + D52 precedent. Pattern-completion at sketch-time (per probing.md + D49 lesson + Clippy upstream D1 sub-check) is actively guarded against here.

D55 is positioned as an **Extends-D19 operationalization** rather than a cluster supersedes (the cluster-supersedes phase per D45 §C completed at D52). Returns to normal per-entry pre-lock probe discipline.

**Cross-references**: D5 §I3 (accountability — specialist activation observable via dispatch path); D7 §3 (workspace state — activation predicate per-instance, static post-boot); D12 + D17 + D43 (substrate runtime — canonical subscriber-dispatch path); D19 §"Contract slots" + §"Cross-specialist coordination" (extends — operationalizes deferred slot); D29 (namespacing); D30 §4 (per-event runtime checks); D37 (event-driven coordination); D42 (PractitionerShape — full DSL design target); D44 (queued dispatch); D45 (standing requirement); D47 §B.1 (canonical reuse for runtime evaluation failures); D48 §B.3 (boot-time check precedent); D50 §B.1 + §E (single-path cluster precedent); D52 §B.1 + §E (single-path + new FAILURE_CATEGORIES + FIRED probe); probing.md §"Pattern-completion over pattern-questioning"; probing.md Procedure 3 refined-skip rule.

## Honest basis caveats

- **Read directly**: README + CLIPPY-COMPANION + probing.md + D19 + D45 + D52 + specialist.schema.json + specialist.py + substrate.py (relevant sections + grep) + validator/types.py + boot.py (relevant section).
- **Claimed but not Read directly (Flag pending verification)**: D47 §B.1 + §B.2 entry text was NOT Read this session — relied on substrate.py docstrings + `SubscriberDispatchError` + `HookExecutionError` class definitions + D52 cross-references for D47 contract shape. The claim "D47 §B.1 aggregates `on_event` exceptions and surfaces `SubscriberDispatchError` at outer drain" is grounded in substrate.py code reads, not D47 entry text directly. Should D47 §B.1 carry restrictions on what failures may use `_subscriber_failures`, §B.1 Surface + §C `_dispatch_event_to_subscribers` modification need adjustment. Conversion-to-Read deferred to §C impl follow-through; alternatively a Phase B operational adjustment lands as separate clarification entry.
- **Inferred**: category-per-cluster precedent (new FAILURE_CATEGORIES entry vs reusing `schema`/`vocabulary`) follows D46/D48/D52; design judgment. Grammar shape (`{"when": {...}}` rather than `{"payload-subtype": ...}` flat) selected for forward-compatibility with sibling keys (`"and"`, `"or"`, `"unless"`); design judgment.
