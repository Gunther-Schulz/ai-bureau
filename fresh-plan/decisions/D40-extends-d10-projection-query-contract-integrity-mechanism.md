# D40 — 2026-05-11 — Extends D10 — projection / query contract + integrity-mechanism extension point

**Decision (extends D10's contract)**: The event chain (D10) gains two additions: a **minimum projection / query interface** every substrate must provide, and an explicit **integrity-mechanism extension point** for protocols like AEGIS / Axon to plug in.

### A. Minimum projection / query interface

Every substrate (D12) advertising the `event-streaming` capability (per D17) must provide the following operations over the event chain it hosts:

| Operation | Description |
|---|---|
| `filter-by-actor(actor-id)` | Returns ordered subsequence of events where `actor-id` appears in `event.actors[].id`. |
| `filter-by-work-unit(work-unit-id)` | Returns ordered subsequence of events where `event.work-unit-id` matches. |
| `filter-by-payload-subtype(subtype)` | Returns ordered subsequence of events with matching `payload-subtype`. |
| `state-at(sequence-n)` | Returns workspace state derived from events 0..n (per D39 state-is-derivable property). |
| `full-chain()` | Returns the full ordered event sequence. |

These are **minimum**; substrates may provide additional operations (indexed lookups, time-range filters, payload-shape predicates, etc.). The minimum guarantees cross-substrate portability for analytics, replay, simulation, and audit-reconstruction workflows (per D12's cross-substrate-portability goal).

**Refinement of D17**: the `event-streaming` capability is defined to include the minimum projection / query interface above. No new core abstract capability is added; D17's three-capability core (`hooks`, `skills`, `event-streaming`) is unchanged. Substrates advertising `event-streaming` implicitly commit to the minimum query interface.

### B. Integrity-mechanism extension point

D10's wording "integrity-checkable; the implementation provides a mechanism" is **retained as the framework-core position** (per D2: no specific protocols at core), but **D40 names "event-chain integrity protocols" as a registered protocol-or-transport category**: extensions may register integrity protocols that substrates can adopt.

**Canonical first example (not provided in Phase A or B; named as future work)**:

**AEGIS protocol** as an extension (`aegis-protocol-ext`) registering:
- `protocol-or-transport: aegis-event-chain-integrity`
- Specifies: SHA-256 hash chain + Ed25519 signing + JCS canonicalization.
- Positioned for EU AI Act Article 12 (effective 2026-08-02), GDPR Article 22, SR 11-7, OCC/CFPB alignment.

Other integrity protocols can coexist per D29 namespacing:
- `axon-protocol-ext` for Axoniq-style event-sourcing semantics.
- `prov-o-protocol-ext` for W3C PROV-O alignment.
- Future post-quantum-signature protocols.

A workspace's substrate-binding may declare the integrity protocol it uses via binding configuration (per D7 substrate-binding.configuration). Substrates that don't support a required integrity protocol fail capability satisfaction (D30 §2) for any deployment requiring it.

**Why AEGIS is not at core**: per D2 strict reading + D17 principle ("core declares a capability iff a core kind contract references it") + D4 inclusion test (legitimate deployments may use Axon, PROV-O, internal hash chains, or post-quantum schemes instead of AEGIS specifically). Same shape as D17's demotion of `mcp-client` / `a2a` — specific protocols are extension-registered, not core. If AEGIS proves universal, D33 promotion to core is a small supersedes entry — but reversibility (demoting later if alternatives emerge) is painful, so the discipline is "stays minimal until proven universal."

### C. Connection to fork-from-state

Per D39 (state-is-fully-derived) + D40 §A (`state-at(sequence-n)` is in the minimum query interface), **fork-from-state is a derived operation**: any workspace can be reconstituted from any prefix of its event chain. Fork is not a separate framework primitive; it's a derived capability that substrates may or may not expose as an API.

Pre-deployment simulation, replay debugging, time-travel workflows, and multi-tenant isolation are all derived from these properties + the minimum query interface. No new kind needed.

### What is NOT in this decision

- **AEGIS protocol implementation** — out of scope here; named as future extension. Phase C (standards-compat impl per D26) is the natural home.
- **Specific algorithm bindings** for integrity protocols (hash function choice, signature scheme, canonicalization) — extension territory.
- **Fork-as-framework-API** — derived operation; substrate-impl concern.
- **Time-range filtering or advanced query operations beyond the minimum** — substrate may provide; not in minimum.
- **Query performance characteristics** — implementation per D11.
- **Snapshot caching for state-at(n)** — implementation per D11; the property is "state IS derivable," not "state must be re-derived from scratch on every query."

### Connection to B1 / B2

- **B1 (conformance validator)**: substrates advertising `event-streaming` are now implicitly committed to the minimum query interface. Validator does not need a new check (no schema change to substrate.schema.json); the interface contract is at runtime / impl level.
- **B2 (substrate runtime)**: `AppendOnlyEventChain` already provides four of the five minimum operations (by-id, by-actor, by-work-unit, by-payload-subtype, full-chain). Needs to add **`state-at(sequence-n)`** (replay events 0..n and reconstruct state). Tracked as **B2-followon-2** (low-to-medium effort; not blocking B3).
- Combined with D39's composition-change schema extension: B2 follow-on tasks are (i) emit `record` in composition-change events; (ii) implement `state-at(n)` replay. Both small; landed as a "Phase B internal refinement" before Phase B closure.

**Rationale**: per D2 (kinds are abstractions; instances are extensions), the integrity mechanism is an instance-level concern that extensions own. Per D12 (substrate hosts the agent loop; cross-substrate portability), the query interface needs to be uniform across substrates — so the minimum interface is core-locked. Per D5 I3 (accountability-bearing AI-human work) + D24 (EU AI Act compliance in-scope), the integrity-mechanism extension point is what lets fresh-plan plug into the regulatory landscape without forcing a specific protocol on every deployment.

The split is clean: framework specifies *what* (queries, integrity-checkability), extensions specify *how* (specific algorithms, specific canonicalization).

**Cross-references**: D2 (no specific protocols at core); D4 (inclusion test); D10 (event chain; this entry extends with minimum query + integrity extension point); D12 + D17 (substrate capabilities; `event-streaming` refined to include query interface); D24 (EU AI Act compliance in-scope; AEGIS / Axon target the same); D26 Phase C (standards-compat impl — natural home for `aegis-protocol-ext`); D29 (namespacing — integrity protocols are extension-registered); D33 (promotion / demotion — AEGIS can graduate later if proven universal); D39 (state-is-derivable; foundation of `state-at(n)`); B2 surfaced tensions (integrity mechanism + projection contract).
