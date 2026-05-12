# D47 — 2026-05-12 — Extends D13 + D17 + D37 + D44 — subscriber dispatch + hook firing honor detection-surface-recovery triad (subscriber-dispatch cluster per D45)

**Decision (substantive; second cluster supersedes per D45 §C)**: The substrate's subscriber-dispatch path (specialists' `on_event` per D19 + D37, queued per D44) and the shape's hook-firing path (D13 + D17 capability `hooks`) are locked under D45's detection-surface-recovery triad. Three SUSPECT findings from the 2026-05-12 audit unified here as the **subscriber-dispatch cluster**: (1) `on_event` exceptions silently swallowed (`substrate.py:193-197 except Exception: pass`); (2) `HookRegistry.fire` never called anywhere in `impl/src/` — D13's hook contract is decorative until firing-sites land; (3) hook handler exception semantics are undefined because (2) never happened. This entry establishes the hook-firing integration sites + handler-exception contract + subscriber-aggregate-error contract. Second cluster supersedes following D46's template; sets the substantive-design pattern for clusters that include genuine new contract work (not just typed-exception application).

## A. Scope of cluster

This entry applies the D45 triad to two related runtime paths owned by the substrate but driven by different kinds:

- **Subscriber dispatch** (specialist runtime per D19 + D37 + D44): each event's append triggers dispatch to subscribing specialists' `on_event`; D44 locked queued FIFO drain semantics; this entry locks failure-mode contract for handler exceptions.
- **Hook firing** (shape runtime per D13 + D17 capability `hooks`): shapes declare hook names; substrates register handlers; **the FIRING — when handlers are invoked + with what payload — was never specified, and the impl never invokes them**. This entry establishes the firing contract.

Three SUSPECT paths from the 2026-05-12 audit unified here:

- **A.1 Subscriber `on_event` exception silently swallowed**: `substrate.py:_dispatch_event_to_subscribers` line 193-197 has `try: sub.on_event(event) except Exception: pass`. Phase D reactive specialists (citation-checker reacting to claims; draft-reviewer reacting to actions) would have their policy failures **invisible** to the caller. Audit named this as canonical "should-never-happen-without-alerting" violation.
- **A.2 `HookRegistry.fire` never called**: `impl/src/fresh_plan/runtime/hooks.py` defines `HookRegistry.fire(name, context: dict)` (line 41-51); `boot.py:183` and `shape.py:149` (Shape base) + `shape.py:167-171` (GenericShape) + `shape.py:188` (MinShape) register handlers via `register_handlers(hook_registry)`; **no impl site invokes `fire()` anywhere in `impl/src/`** (`grep -rn '\\.fire(' impl/src/` returns empty). D13 declares hooks as shape-policy slots; D17 declares `hooks` as core capability; the firing surface — when hooks fire, with what payload — was never specified. Hooks are write-only.
- **A.3 Hook handler exception semantics undefined**: a downstream consequence of A.2 — no handler-exception contract exists because no handler is ever invoked.

Out of scope (different clusters):

- Adapter `call()` failure semantics (D48 adapter cluster)
- Specialist `handle_skill` failure semantics (D49 specialist cluster — composes with this entry's on_event contract but `handle_skill` is invoked through skill-registry, not subscriber-dispatch)
- Composition-change post-projection state validity (D51 composition-change cluster)

## B. Triad applied per path

### B.1 — Subscriber `on_event` exception (D44 amendment)

| Triad element | Lock |
|---|---|
| **Detection** | Exception caught in `_dispatch_event_to_subscribers` per-subscriber try block. |
| **Surface** | Substrate **collects** subscriber exceptions during the drain into a list `(specialist_id, event_id, exception)`. After the drain completes (queue empty per D44), if collection list is non-empty, raise `SubscriberDispatchError(failures=[(specialist_id, event_id, exception), ...])`. Each failure independently captured; subsequent subscribers continue firing (cascade not terminated by first failure). Caller sees aggregate diagnosis across the entire drain. |
| **Recovery** | Caller catches `SubscriberDispatchError`; can identify which specialist + event combinations failed; decide retry / log / shut down workspace. Per D44, the chain itself is fully consistent — events appended + projected; only subscriber-side reactions failed. State-from-events replay still works. |

Aggregate-after-drain (vs propagate-immediately): subscribers are designed as independent reactors per D37 + D44. They already cannot see each other's reactions during the same outer-emit (queued FIFO). One failing shouldn't terminate subsequent subscribers' independent reactions. Phase D scenario: citation-checker raises (programming error) → draft-reviewer should still react to the original event. Aggregate gives caller all-failures-in-this-drain rather than just-the-first.

### B.2 — `HookRegistry.fire` integration (NEW contract)

The substrate fires hooks at two named points in `append_event`:

| Hook | When | Payload | Handler exception |
|---|---|---|---|
| **`pre-event-emit`** | Synchronously between D13 authority check (step 2) and `event_chain.append` (step 3). After authority succeeds, before the event lands in the chain. | event dict (treat as read-only by convention; mutation is undefined behavior — pioneer-instance shape impls SHALL NOT mutate the event in the handler) | → `EventRejected(failures=[ValidationFailure(category="hook-handler", path=f"hook[pre-event-emit][handler={idx}]", reason=<original>)])`. Event NOT appended. Chain integrity preserved per D10. |
| **`post-event-emit`** | Synchronously **after** subscriber-dispatch enqueue, per nested-event call. For outer call: collected aggregate raised after drain completes (symmetric with subscriber-exception aggregation per B.1). For nested call: collected, returns normally; outer drain raises aggregate. | event dict + assigned sequence number (`{"event": event, "sequence": seq}`) | Each handler's exception captured into substrate's collection list as `(hook_name, handler_index, event_id, exception)`. After outer drain completes, if collection non-empty, raise `HookExecutionError(failures=[...])`. **Event IS in chain + state + dispatch happened** (D10 + D39 + D44 preserved); only post-emit observation failed. Caller catches aggregate; can identify which handlers failed for which events; decide workspace-level recovery. |

Why **after authority** for pre-event-emit (not before): D13 authority-bindings are the named rejection mechanism. Hooks are supplementary shape policy. Putting hooks before authority would invert the architectural roles — hooks would become first line of rejection, demoting authority. Cleaner: authority owns rejection, hooks observe what passed.

Why **synchronous at append + collected** for post-event-emit (not synchronous-and-propagate-immediately): the synchronous-at-append firing matches projection timing (each event's post-emit fires when that event is appended; cascade order respected). The collected-aggregate-after-drain handling matches subscriber-exception aggregation per B.1 — both are post-append observation paths; both let the caller see all failures across the cascade; both keep the chain + state + dispatch consistent. Propagate-immediately would prevent the dispatch drain from completing for the outer call, leaving the queue full of unprocessed events — inconsistent with D44's "drain to completion" semantics.

Why **synchronous, not queued** for hooks (vs subscriber dispatch which IS queued per D44): hooks are shape-policy enforcement; subscribers are specialist reaction. Policy enforcement runs at the moment of the event being processed (synchronous = decision-time); reactions can defer to drain-time (queued = react-time). Different layer; different semantics.

### B.3 — Hook handler payload + signature

`HookRegistry.fire(name, context: dict)` is the existing API per `hooks.py`. The substrate's calling convention:

- `substrate.hooks.fire("pre-event-emit", {"event": event})` — context dict carrying the event
- `substrate.hooks.fire("post-event-emit", {"event": event, "sequence": seq})` — context dict carrying event + assigned sequence number

Handlers SHALL declare signatures matching the existing `HookHandler` type alias: `def handler(context: dict) -> Any`. Handler reads `context["event"]` (and `context["sequence"]` for post-emit). `HookRegistry.fire` propagates handler exceptions per the convention above (substrate's `append_event` catches + re-raises as the typed exception per B.2).

This is the minimum viable contract; extension hooks (per future D-entries) may register additional context-dict keys per shape.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

The contract is locked here; the impl follows. Specific changes:

- **`substrate.py append_event`**: insert `self.hooks.fire("pre-event-emit", {"event": event})` between `shape.check_authority` (step 2) and `event_chain.append` (step 3); wrap in try/except → re-raise as `EventRejected(failures=[ValidationFailure(category="hook-handler", ...)])`. Insert `self.hooks.fire("post-event-emit", {"event": event, "sequence": seq})` AFTER subscriber-dispatch enqueue (step 5+: queue insertion done, dispatch deferred to outer drain). Wrap post-emit in try/except → append failure to substrate's collection list (NOT raise). After outer drain completes, raise aggregated errors if collection lists non-empty.
- **`substrate.py _dispatch_event_to_subscribers`**: replace bare `except Exception: pass` with collection — append `(sub.id, event["id"], e)` to substrate's `_subscriber_failures` list. Dispatch loop continues to subsequent subscribers; aggregation happens at outer drain end.
- **`substrate.py append_event` outer drain**: after `while self._dispatch_queue:` loop completes (queue empty OR backstop), drain the two collection lists. If both non-empty: raise `SubscriberDispatchError(failures=sub_failures) from HookExecutionError(failures=post_failures)` — both visible via Python's exception chaining (`__context__` / `__cause__`). If only one non-empty: raise that one alone. If neither: return seq normally. Both lists cleared at start of next outer call.
- **`per_event_checks.py`**: add `EventRejected(category="hook-handler", ...)` accommodation if it doesn't already accept arbitrary categories (it does — category is just a string field on `ValidationFailure`).
- **New exception types in `substrate.py`** (or a new `errors.py`): `HookExecutionError`, `SubscriberDispatchError`. Both carry structured diagnostic + reference to original exception via `from`.
- **New tests in `test_subscriber_dispatch.py`** (or new `test_hooks.py`): (i) hook handler raise on pre-event-emit → event rejected, chain unchanged; (ii) hook handler raise on post-event-emit → event in chain + state, raised after subscriber dispatch enqueue (one event subscriber to verify it still drained); (iii) subscriber raise → aggregate captured + raised after drain; (iv) multiple subscribers raise → all captured; (v) hook fires in correct order (pre before append; post after projection).
- **Documentation**: update `hooks.py` `HookRegistry.fire` docstring to describe pre/post calling conventions per B.2 + B.3; update `substrate.py append_event` docstring to enumerate the 7 ordered steps including hook-firing positions.

Estimated impl size: ~50-80 lines of code change in `substrate.py` + new exception types + 5-7 new test cases + docstring updates.

## D. What is NOT in this decision

- **No new hook names beyond `pre-event-emit` + `post-event-emit`**. These are the two integration sites the substrate offers; future D-entries may add (e.g., `pre-shutdown` / `post-boot`); not in scope here.
- **No async hook firing**. Hooks fire synchronously per B.2; future async-substrate work (Phase C+) may add async firing variant; not in scope.
- **No handler ordering guarantees beyond registration order**. Multiple handlers for the same hook fire in registration order (`HookRegistry`'s default behavior). Priority / weight semantics deferred to future D-entries if shapes need them.
- **No mutation contract on event payload**. Convention is read-only; mutation is undefined behavior. A future D-entry could lock immutable-event-dict semantics; not in scope.
- **No retroactive rewriting of D13 / D17 / D37 / D44 entries** (append-only ledger). D47 EXTENDS those entries; their original wording stands.
- **No change to D44's queued-dispatch model**. D47 amends D44's exception-handling (collection + aggregate) without changing the queued-FIFO-drain semantics or the loop backstop.
- **No formal IDL for hook handler signatures**. Convention is documented (B.3); enforcement is at handler-author time, not framework-validated. Future probing audit may surface this as a gap; deferred.

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: lock detection + surface + recovery for subscriber `on_event` exceptions; establish hook firing integration sites + handler exception contract; second cluster supersedes per D45 §C.
- **WHO**: enforced by *substrate (runtime)* — `Substrate.append_event` calls `hooks.fire(...)` at the named points + collects subscriber exceptions during dispatch; raises typed exceptions per B.1 + B.2. *shape (policy)* — shapes register handlers via `register_handlers(hook_registry)`; handlers are shape-author-owned. *specialist (impl)* — `on_event` is specialist-author-owned; exception handling is captured by substrate without specialist cooperation.
- **FAILS** (recursive — what happens if substrate doesn't honor the contracts?): *Detection*: failure-mode coverage audit + detection-surface-recovery audit at next checkpoint. *Surface*: audit findings list. *Recovery*: supersedes entry sharpens contract OR impl-follow-through commit closes the gap.
- **CROSS**: D10 (chain integrity — preserved by pre-event-emit raising before append; post-event-emit raises after append, chain stays consistent); D13 (shape policy — hooks ARE shape policy; this entry establishes their firing contract); D17 §`hooks` capability (operationalized by this entry); D19 + D37 (specialist on_event subscribed via `declared-event-subscriptions[]`); D34 §A.5 (current-state resolution — preserved by hook firing not adding new state); D39 (state-from-events — preserved; hooks are observation/policy, not state mutation); D40 §A (minimum query interface — chain projections work over events including any that triggered hook handler raises on post); D44 (queued FIFO drain — D47 amends exception handling without changing drain semantics); D45 (standing requirement that motivated this entry); D46 (precedent for cluster supersedes structure).
- **DEFERS**: additional hook names (pre-shutdown / post-boot etc.); async hook firing for Phase C+ async substrates; handler priority/weight semantics; immutable event-dict enforcement; formal IDL for handler signatures.

## E. Pre-lock probe self-referentiality (skip with documented reason per D45 §E precedent)

Per D45 §E established precedent (followed by D46 §E): pre-lock probe SKIPPED for D47. Reason: this entry is grounded in the 2026-05-12 failure-mode + abandonment-path audit findings (specifically the subscriber-dispatch cluster, including the hook-firing structural surprise that the audit named explicitly). Re-probing would be circular — the audit motivated the entry; the entry codifies the cluster's resolution; a pre-lock probe would re-derive what we already have.

Note: D47's design content (§B.2 hook integration sites) is more substantive than D46's — it establishes a NEW contract that didn't exist before (hooks were never fired). The pre-lock-probe-skip is justified because the *gap was identified by the audit* (HookRegistry.fire never called) AND the *resolution shape was discussed in this session before lock* (the four design choices flagged + recommended + signed-off). Future audit-driven entries with substantive new design content should similarly document the design-choice-discussion that supplements the audit-driven motivation.

## Rationale

The 2026-05-12 failure-mode + abandonment-path audit identified the subscriber-dispatch cluster as one of the worst — three distinct silent-degradation paths in the substrate's hot dispatch path. The on_event silent-swallow is canonical "should-never-happen-without-alerting" violation per global CLAUDE.md. The hook-firing-never-happens is structurally worse — D13's hook contract has a registration mechanism with no trigger, meaning shape policy hooks are decorative until trigger-sites land. D17 declares `hooks` as a core capability the substrate advertises, but the substrate doesn't actually integrate them.

Per D45's standing requirement: every runtime decision needs detection + surface + recovery. D44 locked subscriber-dispatch's runtime semantics (queued FIFO + loop backstop) but didn't address handler-exception semantics (covered the WHAT of dispatch, not the FAILS). D47 closes that gap on the dispatch side.

The hook-firing integration is genuinely new contract work — the audit identified the gap; D47 establishes the resolution. The four design choices (after-authority, synchronous-at-append, aggregate-after-drain, combined-cluster) are committed per pre-lock discussion in this session. Worth surfacing for future readers: pre-event-emit + post-event-emit are minimum viable hook integration sites; future D-entries may add named hooks if shapes need them. Pioneer-instance practitioner-shape (Phase D) is the natural test of whether this contract is sufficient.

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): hook-firing integration is what makes shape-policy genuinely operational. Without firing, shapes are passive declarations; with firing, shapes are runtime-active policy enforcement. This is what distinguishes fresh-plan from a pure event-spec — the framework specifies HOW shape policy intervenes in event processing, not just WHAT shape policy declares.

D47 follows D46's structural template: §A scope of cluster + §B triad applied per path + §C impl follow-through + §D What is NOT + decision-shape template + §E pre-lock probe skip + Rationale + Cross-references. Sets the pattern for D48-D51 cluster supersedes which similarly mix typed-exception application with cluster-specific design content.

**Cross-references**: D10 (event chain integrity — preserved across hook firing); D13 §hooks slot (shape policy hooks — D47 establishes their runtime firing contract); D17 §`hooks` capability (operationalized by D47); D19 §declared-event-subscriptions (specialist subscription mechanism — D47 amends subscriber exception handling); D34 §A.5 (current-state resolution — preserved); D37 (event-driven cross-specialist coordination — D47 makes the dispatch path observable on failure); D39 (state-from-events — hook firing doesn't mutate state, so D39 preserved); D40 §A (query interface — works over events including those that triggered post-emit handler exceptions); D44 (queued FIFO drain + loop backstop — D47 amends exception aggregation without changing drain semantics); D45 (standing requirement); D46 (precedent for cluster supersedes structure; D47 follows the §A/§B/§C/§D/§E template); 2026-05-12 failure-mode + abandonment-path audit (motivating evidence; subscriber-dispatch cluster identified there).
