# D17 — 2026-05-08 — Supersedes D12 core capability vocabulary (strict protocol-neutrality applied)

**Decision**: Supersedes D12's "Core capability vocabulary (framework-declared)" section per the strict reading of D2 articulated in D16. The revised list contains **only abstract capabilities that core kinds reference**; specific-protocol-named capabilities are moved to extension-registered status.

### Revised core capability vocabulary

The framework-core declares these capabilities. The principle: *a capability is at core iff a core kind contract references it*.

- **`hooks`** — substrate exposes hook points for shape policies / discipline enforcement. Referenced by shape kind (D13).
- **`skills`** — substrate can load specialist bundles. Referenced by specialist kind (forthcoming).
- **`event-streaming`** — substrate emits events the workspace state can capture. Referenced by workspace kind (D7) for state accumulation; by event kind (D10) for chain construction.

### Removed from core (now extension-registered)

- **`mcp-client`** — specific protocol; substrate that supports MCP advertises this via the MCP protocol extension.
- **`a2a`** — specific protocol; substrate that supports A2A advertises this via the A2A protocol extension.

### Abstract-over-protocol capabilities considered but NOT introduced

Discussion considered introducing abstract capabilities like `external-tools` (over MCP and equivalents) and `agent-peering` (over A2A and equivalents). They are **not introduced at core in this entry**. Reasons:
- The "core declares what core kinds reference" principle rules them out — no current core kind contract directly references them.
- Adapters declare `required-substrate-capabilities[]` via opaque identifiers (per D16); extensions register whatever capability identifiers their adapters need.
- If adapter-portability concerns later make abstract-over-protocol capabilities valuable, they can be introduced via supersedes entry then — with stronger evidence.

### Substrate kind contract impact (D12)

D12's `capabilities[]` slot semantics are unchanged — substrate declares what it exposes. The vocabulary it draws from is now:
- Three core abstract capabilities (above), AND
- Extension-registered capability identifiers (per the layer-3 extension protocol).

A Claude Agent SDK substrate would advertise `hooks`, `skills`, `event-streaming` (core) AND `mcp-client`, `a2a`, `computer-use`, `parallel-tool-calls` (extension-registered).

### Refinement-pass status update

The D12-finding flagged in D16 is now addressed by this entry (per the rolling refinement approach: option C in the discussion that produced D17 + D18).

**Rationale**: D2 (kinds are abstractions; instances are extensions) applied strictly per D16's multi-pass analysis requires no specific-protocol identifiers in framework-core's vocabulary. Keeping the core minimal (3 capabilities) follows the principle that core declares only what core kinds reference.
