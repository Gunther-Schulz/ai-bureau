# D25 — 2026-05-08 — Layer 2 closure (final kind set; layer 2 complete)

**Decision**: Layer 2 (kinds) is **complete**. The framework-core's kinds are now fully enumerated; cross-kind consistency has been reviewed; standards-compatibility scope decisions have been made. Layer 2 is closed; layer 3 (extension protocol + formal schemas) is the next phase.

### Final kind set (8 kinds)

| Kind | Decision entry | One-line summary |
|---|---|---|
| **workspace** | D7 (closure) | Bounded coordination context where one composition runs. Manifest + state. |
| **actor** | D9, refined by D22 | Attribution-bearing participant; subtypes `human-actor`, `agent-actor`. |
| **event** | D10, refined by D23 | Single ordered chain per workspace; payload-subtypes (claim, action, state-change, composition-change, lifecycle-transition + extension-registered). |
| **substrate** | D12, capability section by D17 | Hosts the agent loop; declares capabilities (abstract core: `hooks`, `skills`, `event-streaming`) + extension-registered protocol-named capabilities. |
| **shape** | D13 | Substantive identity carrier (per D4); policy bundle of authority-bindings + roles + hooks + actor-requirements + capability requirements. |
| **adapter** | D16 | Interface to external surfaces; protocol-or-transport open vocabulary (no specific protocols at core per D2 strict reading). |
| **specialist** | D19 | Internal capability bundle; declares skills + supported work-unit-kinds + adapter dependencies + event subscriptions. |
| **work-unit** | D20 | Instance of organized work; kind-discriminated (extension-registered); fixed core lifecycle enum (created/in-progress/paused/completed/abandoned). |

### What is at framework-core after D5 + D7-D24

- **Layer 1 (identity, D5)**: I1 composition system + I2 machine-checkable contracts on kinds + I3 accountability-bearing AI-human work. Workspace as organizing primitive.
- **Layer 2 (kinds)**: 8 kinds above with semantic contracts. Cross-references resolved. Standards-compatibility scope decided. Refinement-pass complete.

### What is NOT yet defined (next phases)

- **Layer 3 (extension protocol + formal schemas)** — non-optional for any impl work. Per D11, this layer produces:
  - Formal schemas for each kind (concrete enough to validate, format-neutral).
  - Extension declaration mechanism (how an extension registers itself; how core validates conformance).
  - Composition rules (how extensions of different kinds compose; conflict resolution; precedence).
  - Promotion / demotion rules.
- **Implementation level (below layer 3)** — format/serialization choices (JSON, YAML, Pydantic, Protobuf), storage / wire / protocol mechanisms, specific extension impls (Claude Agent SDK substrate, practitioner-shape impl, MCP protocol extension, A2A protocol extension, specific specialists / adapters / work-unit-kinds).

### Verification targets carried forward to layer 3 + impl

These were named at layer 2 but their verification operates at layer 3 + impl:

1. **D21 workspace-as-A2A-peer deployability** — verify that specialist skill declarations carry enough metadata for clean agent-card mapping; that workspace lifecycle correctly binds/unbinds A2A peer adapter; that A2A peer auth integrates with shape authority-bindings; that per-skill exposure control mechanism is well-defined.
2. **MCP-server-exposure parallel** (per D21 generalization) — same rigor as A2A.
3. **Layer-3 formal schemas** for each of the 8 kinds + extension declaration mechanism + composition rules + promotion / demotion.
4. **Standards-compatibility mapping work** for in-scope standards (PROV-O, VC, DID, CloudEvents, OpenTelemetry, AsyncAPI, JSON Schema, Activity Streams, EU AI Act compliance) — depth varies by standard; some are layer-3-toolchain (JSON Schema), some are vocabulary-mapping (Activity Streams), some are extension-impl-level (OpenTelemetry).

### Recap of layer 2 ledger journey

- **D6** — enumeration approach (incremental + closure check).
- **D7, D9, D10, D12, D13, D16, D19, D20** — eight kind decisions.
- **D8** — no `discipline` kind (mechanisms-formerly-called-disciplines decompose into state property / shape policy / specialist-or-shape concern).
- **D11** — layering clarification (semantic contract = layer 2; formal schema = layer 3; format = implementation).
- **D14** — refinement-pass discipline.
- **D15** — standards-compatibility criterion.
- **D17** — supersedes D12's capability list (strict protocol-neutrality applied).
- **D18** — clarifies D15 phrasing.
- **D21** — workspace-as-A2A-peer deployability requirement.
- **D22** — clarifies D9 substrate-binding resolution.
- **D23** — supersedes D10 slot list (adds work-unit-id).
- **D24** — refinement-pass output (consistency + 4a flags + standards-compatibility findings).
- **D25 (this)** — closure.

**Layer 2 status: closed.** Next phase decision: when to begin layer 3 + how to structure that work.
