# D24 — 2026-05-08 — Refinement-pass output: cross-kind consistency + 4a flags + standards-compatibility findings

**Decision**: The named refinement pass per D14 + D15 produces the following findings in three categories:

### A. Cross-kind consistency

**Required-with-explicit-empty pattern (D13) — retroactive review:**

- **D7 (workspace)** — slots are mostly required-non-empty (substrate-binding ≥ 1; actor ≥ 1) or always-have-content (state, lifecycle). The D13 pattern (mandatory slot with explicit-empty admissible) doesn't directly apply. **No retroactive change needed.**
- **D9 (actor)** — slots are mandatory; no list slots that the pattern would apply to. **No change needed.**
- **D10 (event)** — `actors[]` is required ≥ 1 (not "may be empty"). Other slots are inherently populated. **No change needed.**
- **D12 (substrate)** — `capabilities[]` and `runtime-shapes[]` are required non-empty (a substrate without either is meaningless). **No change needed.**
- **D13 (shape)** — pattern originated here; applied throughout. ✓
- **D16 (adapter)** — pattern applied per design. ✓
- **D19 (specialist)** — pattern applied per design. ✓
- **D20 (work-unit)** — pattern applied per design. ✓

**Cross-reference resolution audit:**
- workspace ↔ shape (1) — D7 + D13 ✓
- workspace ↔ substrate-bindings — D7 + D12 ✓ (refined by D22)
- workspace ↔ actors — D7 + D9 ✓
- workspace ↔ adapters — D7 + D16 ✓
- workspace ↔ specialists — D7 + D19 ✓
- agent-actor ↔ substrate-binding — D9 + D12 ✓ (clarified by D22)
- event ↔ actors — D10 + D9 ✓
- event ↔ work-unit — D10 + D20 ✓ (refined by D23)
- specialist ↔ work-unit-kinds — D19 + D20 ✓
- specialist ↔ adapters (required-bindings) — D19 + D16 ✓
- adapter ↔ substrate (capabilities) — D16 + D12 ✓
- shape ↔ actor-subtypes — D13 + D9 ✓

All cross-references resolve; no orphan references.

**Slot naming consistency:** identifiers (`id`), versions (`version`), required-substrate-capabilities, declared-event-emissions / consumptions / subscriptions consistent across kinds. ✓

**Optional parent-actor slot for sub-agents (D9 candidate from sub-agent discussion):** *Decision: not added at this pass.* Reason: event-recorded parent-child relationships (via `composition-change` event payload) are sufficient for current sub-agent patterns; adding an optional slot to D9 without empirical justification (no concrete sub-agent flow we can't currently express) is premature. Revisit if downstream impl work surfaces concrete need.

### B. 4a prior-list-sweep flag resolutions

**Workflow vs work-unit:**
*Decision: workflow is **not** a separate kind at framework-core.* The prior corpus's `arch/workflow-work-unit.md` conflated two things: (i) the *unit of organized work being done* (= work-unit, D20) and (ii) the *coordination pattern across multiple work-units* (= deployment-template / shape concern). Workflow as "containment hierarchy on work-unit" was deferred per D20 and stays deferred — no current core kind requires it. If a deployment needs workflow-style coordination, it expresses that via shape policy + specialist orchestration + event subscriptions, not via a new kind.

**Engagement-target / Client / Customer / Funder:**
*Decision: not framework-core kinds.* These are domain-flavored entities ("the parties the workspace works on behalf of or with"). They live as:
- *Shape policy*: shape may declare an engagement-target role-type (e.g., practitioner-shape declares `client` as a shape-role) per D13 roles[] vocabulary.
- *Adapter content*: e.g., a CRM adapter exposes client records as resources.
- *Workspace state payload*: work-units' payloads may reference engagement-target identifiers domain-specifically.
- The framework treats them as *opaque entities* — addressable via id, attributable via actor (when they participate in events as actors), but not its own kind.

Confirmed not a missing core kind.

### C. Standards-compatibility findings (per D15 + D21)

For each candidate standard, the pass evaluates scope + per-kind mapping notes.

| Standard | Scope decision | Per-kind mapping notes |
|---|---|---|
| **MCP** | In scope (load-bearing) | Substrate-side: extension-registered capability satisfying D17 abstract capabilities. Adapter-side: `protocol-or-transport: mcp-server`. Specialist skills exposable as MCP tools (workspace-as-MCP-server pattern, parallel to A2A per D21). Events with `action` payload-subtype map to MCP tool-call results. |
| **A2A** | In scope (load-bearing per D21) | Workspace exposable as A2A peer; agent-actors map to A2A agent identities; specialist skills aggregate into agent-card skills; work-unit lifecycle maps to A2A task lifecycle (submitted/working/completed/failed → maps cleanly to D20's enum); events form A2A task event streams. |
| **PROV-O** | In scope (strong fit) | Actors ↔ `prov:Agent`; events ↔ `prov:Activity`; claim payloads ↔ `prov:Entity` (the asserted thing); attestation events ↔ `prov:wasAttributedTo`. Strong fit for accountability-bearing-work framing per I3. Specific mapping for cross-tool provenance interchange = future investigation. |
| **W3C Verifiable Credentials** | In scope (relevant for attestation) | Authority-binding attestation events (per D13 authority-bindings) could be expressed as signed VCs. Cross-system attestation interchange. Specific mapping = future work. |
| **DID** | In scope (relevant for federation) | Actor identity (especially agent-actor) could use DIDs for cross-workspace federation. Connects to deferred multi-workspace federation question (D7 + D9). Future work when federation is on the table. |
| **CloudEvents** | In scope (format-level) | Event payload structure could optionally serialize as CloudEvents for cross-system event interchange. Implementation-level concern; framework events conform regardless of wire format. |
| **OpenTelemetry** | In scope (substrate-level) | Substrate impls (especially MS Agent Framework) emit OpenTelemetry spans natively. Substrate impls can map workspace events ↔ OTel spans for observability. Implementation choice. |
| **OpenAPI** | Out of scope at core | Relevant to MCP-server-impl-level (some MCP servers describe their tools via OpenAPI), but not framework-core mapping concern. |
| **AsyncAPI** | In scope at extension-impl level | Event-driven adapters may describe their event interfaces via AsyncAPI. Adapter-extension concern. |
| **JSON Schema** | In scope (layer-3 toolchain) | Strong candidate for the layer-3 formal schema notation. To be confirmed when layer-3 work begins. |
| **Activity Streams** | In scope (vocabulary inspiration) | Activity Streams' vocabulary (verb/actor/object/target) parallels our event/payload-subtype/payload structure. Could inform payload-subtype naming + extension-registered subtype conventions. |
| **EU AI Act compliance** | In scope (accountability alignment) | Audit-trail requirements + practitioner-accountability semantics align with PBS purpose per I3. Specific compliance schemas may emerge; framework structure already supports the underlying requirements. |

**Standards considered but NOT named in D15 — none surfaced during this pass.**

### Outputs of this pass

- **D22** — clarification of D9 substrate-binding resolution.
- **D23** — supersedes D10 slot list (adds work-unit-id).
- **This entry (D24)** — cross-kind consistency notes (most kinds pass unchanged); 4a flags resolved (no missing kinds); standards-compatibility findings (mapping notes captured per standard).
- **No further substantive supersedes** for D7, D12, D13, D16, D19, D20 from this pass.

**Refinement pass per D14 + D15: complete.** Layer 2 ready for closure entry per D6 step 4c.
