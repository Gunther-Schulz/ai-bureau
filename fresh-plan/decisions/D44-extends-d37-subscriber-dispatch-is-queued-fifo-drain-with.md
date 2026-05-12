# D44 — 2026-05-11 — Extends D37 — subscriber-dispatch is queued (FIFO drain) with loop backstop

**Decision (extends D37 with a runtime-semantics contract)**: When events are appended to the workspace event chain, **subscriber dispatch (specialists' `on_event` per D19 + D37) is queued and drained FIFO by the outermost append call**. Per-event identity / authority / schema / chain-integrity / state-projection remain synchronous (preserves D10 chain order + D39 state-from-events + D40 §A replay equivalence) — only the subscriber-dispatch step is queued. Nested append calls (events emitted from inside `on_event`) enqueue without re-entering the drain. A loop backstop (`max_events_per_drain`, default 1000; per-substrate overridable) raises a `RuntimeError` with a diagnostic naming the offending event in flight when a single drain exceeds the limit, so genuine infinite loops surface fast. Bref deliverable per D42.

### Dispatch model

For every `append_event(E)` call:

1. Run per-event identity check (D30 §4 / D34 §A.5).
2. Run shape authority-binding check (D13 + D34 §A.5 if applicable).
3. Append `E` to the chain (`event.schema.json` validation + chain integrity per D10).
4. Apply state projection (`apply_event_to_state` per D39 + D40 §A).
5. Enqueue `E` for subscriber dispatch.
6. If this call is the outermost (no drain in progress): take the drain. While the queue is non-empty, pop the next event and call subscribers' `on_event`. Subscribers may emit further events during their reaction; those go through steps 1–5 synchronously and land on the drain queue (step 5) without re-entering the drain.
7. Return the assigned sequence number.

Steps 1–4 are unchanged from the pre-D44 baseline. Step 5–6 is the queued dispatch.

### Loop backstop

Per drain, the substrate counts dispatched events. Exceeding `max_events_per_drain` (default 1000) raises:

```
RuntimeError: subscriber-dispatch drain exceeded N events; likely infinite loop.
Last event in flight: id=<eid> payload-subtype=<subtype>
```

The remaining queue is cleared so the substrate is left in a clean post-drain state for the caller to handle (or for a containing harness to terminate the workspace). Per D44, the limit is a runtime-tunable backstop, not a contract: substrates with unusually-cascading shapes can raise it; tests can lower it to exercise the path. The default is high enough that legitimate cascades never hit it; low enough that a true loop terminates fast.

### Alternatives considered + rejected

- **Re-entry guard** (specialist's emissions don't re-trigger its own `on_event`). Catches direct A→A loops but misses indirect A→B→A. And it changes behavior in a quiet way ("you don't get to see your own emissions's reactions") that surprises authors more than queued dispatch does — synchronous-with-skip is the worst of both worlds: order is unpredictable AND cascades are partially invisible.
- **Recursion depth N**. Catches all loops including indirect, but N is a magic constant (5? 100?) that smells arbitrary. Half-completed cascades raise the question "what's the semantics — drop, raise, log?" — three sub-decisions where queued dispatch has a single clean answer.
- **Synchronous + no guard** (today's behavior). Works as long as no specialist actually loops. Phase D shape (practitioner-shape) is expected to introduce reactive policies (citation-checker reacting to claims, draft-reviewer reacting to actions); the loop risk crystallizes there. Defending the contract before it breaks is cheaper than after.

### Trade-off vs synchronous (today)

A specialist's `on_event(E)` no longer sees subscriber reactions to events IT emits — those reactions fire after `on_event` returns, in queue order. This is a one-time learning. In practice reactive policies are "observe, emit, done" rather than "observe, emit, await reactions, continue." If a Phase D specialist genuinely needs synchronous-with-cascades semantics (rare), that's an opt-in skill-invocation pattern on top of the queue, not a framework default.

### Cascade applied in same commit

- `runtime/substrate.py` — append_event refactored; `_dispatch_queue` (deque) + `_dispatching` flag + `max_events_per_drain` field added to the `Substrate` dataclass.
- New `tests/test_subscriber_dispatch.py` — 4 tests exercising FIFO ordering (intra-specialist + cross-specialist), the loop backstop with a custom limit, and that chain integrity + projection remain synchronous.
- 168 tests pass (164 baseline + 4 new for D44).
- No schema changes. No ledger amendments to D10 / D19 / D37 / D40 (all still hold; D44 extends rather than supersedes).

### What is NOT in this decision

- **No async substrate model** — the queued drain is synchronous (the drain loop runs to completion before `append_event` returns to the caller). A future async substrate could implement the same FIFO contract with an asyncio event loop; that's a Phase C+ concern.
- **No per-event-priority queue** — events drain in append order, full stop. If a future shape requires priority semantics, that's a shape-level concern (e.g., shape policy could pre-process the queue), not a framework-level scheduling primitive.
- **No specialist-level opt-out from queueing** — every subscribing specialist is dispatched through the same drain. A "synchronous-with-cascades" mode for individual specialists would be a separate proposal (and likely not warranted given the framework primitives — see "Trade-off" above).
- **No persistent queue across workspace restarts** — the queue is in-memory per running substrate. Events are durable in the chain (D10); the dispatch queue holds only events being processed in the current drain.
- **No per-event observability hook** in this entry — a "drain trace" or "max-depth-reached" hook for telemetry could be useful for Phase D shapes; deferred until a concrete need surfaces.

**Rationale**: per Failure-modes-are-first-class discipline, every framework runtime primitive that can fail (and an unbounded subscriber loop CAN fail catastrophically — call-stack exhaustion, OOM) needs an explicit detection + surface + recovery path. The queued-dispatch model gives all three: detection (drain counter), surface (`RuntimeError` with diagnostic naming the event in flight), recovery (queue cleared; caller handles or terminates). The recursive synchronous baseline gave none of the three; it relied on no-specialist-ever-looping as an unstated invariant. Phase D is when reactive policies arrive in earnest; defending the contract before then is cheaper than after.

The pattern matches mature event systems (Redux store, JavaScript event loop, Erlang messages, Elixir GenServer cast queue): synchronous side-effects (append + projection) + queued reactions + bounded depth. Fresh-plan adopting the well-trodden path is per the durability-framing — frameworks survive by aligning with patterns the field has converged on, not by inventing novel reactor semantics.

**Cross-references**: D10 (event chain — append + integrity remain synchronous); D13 (shape authority check — runs synchronously before append); D17 (the `event-chain` capability hosts this dispatch model; renamed by D43); D19 (specialist `on_event` + `declared-event-subscriptions`); D30 §4 + D34 §A.5 (per-event identity check — synchronous); D37 (event-driven cross-specialist coordination — D44 is the runtime-semantics contract that makes this safe at scale); D39 + D40 §A (state-from-events, replay equivalence — preserved by keeping projection synchronous); D42 (Bref — this is a Bref deliverable).
