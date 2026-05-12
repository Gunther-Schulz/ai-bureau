# D16 — 2026-05-08 — Adapter kind

**Decision**: The adapter kind specifies how a workspace integrates with external surfaces (services, peer agents, event sources, custom systems). One kind covers all integration patterns (request/response tool, delegation peer, passive event source); pattern variability is captured by `protocol-or-transport` + `declared-event-emissions[]` + `declared-event-consumptions[]`. **No specific protocol is listed at framework-core level**; all protocol identifiers are extension-registered (per the strict reading of D2 — see "Strict protocol-neutrality" below).

### Contract slots

- **`id`** — stable identifier (e.g., `email-adapter-imap`).
- **`version`** — version designator (range-comparable; semver-shaped at layer-3 formal schema).
- **`protocol-or-transport`** — single opaque identifier for the protocol the adapter speaks. Fully open vocabulary; the identifier must resolve to an extension-registered protocol (per the extension protocol at layer 3). Multi-protocol adapters express by registering multiple adapter instances (one per protocol).
- **`required-substrate-capabilities[]`** — list of substrate capability identifiers the adapter needs. Required slot; may be `[]` (e.g., direct in-process adapter that needs no substrate capability). Framework validates at boot that the workspace's bound substrate(s) collectively provide every listed capability.
- **`declared-event-emissions[]`** — list of `(payload-subtype, qualifier?)` pairs the adapter can emit into the workspace event chain. Required slot; may be `[]`. Lets shapes' authority-bindings (per D13) reason about adapter outputs at composition validation time.
- **`declared-event-consumptions[]`** — list of `(payload-subtype, qualifier?)` pairs the adapter consumes / surfaces as workspace events. Required slot; may be `[]`.

### Three integration patterns (illustrative, not part of contract)

A single kind covers radically different patterns:

- **Request/response tool** (e.g., MCP-wrapped email adapter): emits `action` events on agent-invoked operations; emits `action` events on inbound (e.g., `email-received`).
- **Delegation peer** (e.g., A2A-wrapped research-agent): emits `action` events on delegation; emits `action` events on peer responses.
- **Passive event source** (e.g., direct calendar-watcher): emits `state-change` events without agent invocation; declared-event-consumptions typically empty.

### Configuration is binding-time

Adapter configuration (URLs, credentials, polling intervals, etc.) is supplied at workspace.composition binding time and is **extension-defined per protocol** — not in the kind contract. Each protocol extension declares the config schema its adapters expect.

### Strict protocol-neutrality (per D2)

Framework-core lists **no specific protocols**. `protocol-or-transport` is open vocabulary. MCP, A2A, CloudEvents, AsyncAPI, direct-api, file-sync, webhook-handler — all are extension-registered protocol identifiers, all of equal standing at core. This solidifies D2 (kinds are abstractions; specific protocols are instances).

Solidified across multiple passes including: slippery-slope test (no principled line admits MCP/A2A while excluding HTTP, OAuth, OpenTelemetry, etc.), D15 internal-consistency analysis, abstraction-vs-instance test, future-proofing (post-MCP / post-A2A protocols get parity from day one).

### Refinement-pass findings flagged (consequences for prior entries)

This decision surfaces inconsistencies in earlier entries that the refinement pass per D14 must address:

- **D12 (substrate capabilities) — same category-collapse.** D12's core capability list mixed abstract patterns (`hooks`, `skills`, `event-streaming`) with specific-protocol-named capabilities (`mcp-client`, `a2a`). Refinement-pass action: keep abstract capabilities at core; move specific-protocol capabilities to extension-registered status. Possibly introduce abstract capabilities `external-tools` (over MCP and equivalents) and `agent-peering` (over A2A and equivalents) at core.
- **D15 internal phrasing.** D15 says "MCP is already integrated as substrate capability." Under the strict reading, this should become "MCP is registered as an extension-protocol that satisfies the abstract core capability." Refinement-pass action: sharpen wording.

### What is NOT in the adapter kind contract

- **Specific protocol semantics** (how MCP tool-calls work; how A2A handshakes; how CloudEvents emit; etc.) — extension protocol territory at layer 3.
- **Configuration schema** — extension-declared per-protocol.
- **Authentication** — implementation.
- **Specific tool / resource lists** — extension-declared per-adapter (or per-protocol).
- **Adapter lifecycle internals** (connection pooling, retry, etc.) — implementation.
- **Multi-protocol single adapters** — out of scope; register multiple adapter instances instead.

**Rationale**: per I1 (composition), adapters are how the workspace composes with external surfaces; per I2, declared emissions / consumptions / required-capabilities give framework a structural basis to validate composition at boot; per I3, declared event emissions let the workspace's event chain incorporate adapter outputs as attribution-bearing events. The strict protocol-neutrality (per D2) keeps the framework standards-friendly without standards-locked.
