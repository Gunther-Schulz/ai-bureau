# D15 — 2026-05-08 — Standards-compatibility criterion for refinement pass (clarifies D14)

**Decision**: The refinement pass per D14 includes an explicit **standards-compatibility criterion**: each layer-2 kind is checked for clean mappability to relevant external standards, without distortion. The check operationalizes the principle that the framework integrates *with* the standards ecosystem rather than *baking standards into* core kinds (per D2).

### Criterion phrasing

> *Is each kind cleanly mappable to the primitives of relevant external standards? If yes, framework integrates with the ecosystem without protocol-locking core. If mapping requires forced translation or distortion, either the kind needs sharpening OR the standard isn't relevant for this kind — surface as a finding either way.*

### Standards explicitly in scope (non-exhaustive)

The pass at minimum considers:
- **MCP** (Model Context Protocol) — already integrated as substrate capability + adapter protocol; check that adapter declared-emissions / consumptions map to MCP tool-call / resource semantics.
- **A2A** (Agent-to-Agent) — already integrated as substrate capability + adapter protocol; check that `agent-actor` identity, work-unit task model, and event-message exchange map cleanly to A2A's data model.

### Standards to investigate / research during the pass (non-exhaustive)

The pass also includes a **research step** to identify additional standards worth mapping to. Candidates that may be relevant (to be evaluated, not assumed in scope):

- **W3C PROV-O / PROV** — provenance ontology; potentially highly relevant for claim attribution + audit-trail semantics (per I3).
- **W3C Verifiable Credentials** — for attestation / authority-binding signaling across systems.
- **DID (Decentralized Identifiers)** — for actor identity across systems / federation.
- **CloudEvents** — standard event format; potentially relevant to event-kind mapping for cross-system event interchange.
- **OpenTelemetry** — observability / audit / tracing; potentially relevant for cross-substrate observability (Microsoft Agent Framework uses it natively).
- **OpenAPI** — for adapters that wrap REST/HTTP APIs (especially MCP-server-fronted ones).
- **AsyncAPI** — for event-driven adapters.
- **JSON Schema** — for the layer-3 formal schema notation itself.
- **Activity Streams** — standardized activity/event vocabulary.
- **EU AI Act compliance schemas** — emerging; relevant for accountability-bearing deployments per I3.

This list is **a starting point for research**, not a list of confirmed-in-scope standards. The pass produces findings: for each candidate standard, decide *in scope (kinds should map cleanly) / out of scope (not relevant for our kinds) / open (needs deeper investigation)*.

### Outputs of the standards-compatibility check

- For each kind: **mapping notes** to in-scope standards (e.g., "agent-actor.id maps to A2A agent-identity; agent-actor.substrate-binding doesn't map directly — surfaces only at A2A adapter layer").
- For each candidate standard: **scope decision** (in / out / open with research follow-up).
- **Supersedes / clarification entries** for any kind that requires sharpening to enable clean mapping to in-scope standards.

**Rationale**: standards-compatibility is what lets the framework be substantively useful in a heterogeneous ecosystem without sacrificing core's protocol-neutrality. Naming this as an explicit pass criterion (vs. ad-hoc consideration) ensures the check actually happens. Extending beyond MCP and A2A acknowledges that the standards landscape is broader than the two standards we've already engaged — and may shift over time.
