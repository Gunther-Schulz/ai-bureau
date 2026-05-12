# D18 — 2026-05-08 — Clarifies D15 wording (per strict protocol-neutrality)

**Decision**: D15's wording around how MCP and A2A "integrate" with framework-core is **clarified** to align with the strict reading articulated in D16 + D17.

### Wording clarification

D15's "Standards explicitly in scope" section should be read as:

- **MCP** — registered as an extension-protocol identifier. In substrate context, MCP-supporting impls advertise via extension-registered substrate-capability identifiers (e.g., `mcp-client`). In adapter context, adapters wrapping MCP servers declare `protocol-or-transport: mcp-server`. Refinement pass verifies clean mappability of core kinds (actor, event, work-unit, etc.) to MCP primitives.
- **A2A** — same shape: extension-protocol identifier; substrate-supporting impls advertise via extension-registered substrate capabilities; adapters wrapping A2A peers declare `protocol-or-transport: a2a-peer`. Refinement pass verifies clean mappability.

The original phrasing in D15 ("MCP is already integrated as substrate capability + adapter protocol") was loose. It should have said: *"MCP is registered as an extension-protocol whose substrate-side implementations advertise via extension-registered substrate-capability identifiers; adapter-side implementations declare it as their protocol-or-transport."*

### Why this is a clarification, not a substantive supersede

D15's substantive content is unchanged:
- The standards-compatibility criterion still applies.
- The "research candidates" list still applies (PROV-O, VC, DID, CloudEvents, OpenTelemetry, OpenAPI, AsyncAPI, JSON Schema, Activity Streams, EU AI Act schemas).
- The operational pass procedure (per-kind mapping notes; per-standard scope decisions; supersedes/clarification outputs) still applies.

Only the phrasing about *how* MCP and A2A relate to core is sharpened.

### Refinement-pass status update

The D15-finding flagged in D16 is now addressed by this entry. With D17 + D18 together, the D16-flagged refinement-pass items are all resolved (per option C — rolling refinement of clear-now findings; named pass at closure still handles cross-cutting and late-emerging findings).

**Rationale**: keeping the ledger internally consistent during ongoing work — D15 should not be referenced or built upon while it carries phrasing that contradicts the strict reading just locked.
