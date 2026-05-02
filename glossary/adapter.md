---
entry: adapter
class: PRIMITIVE
layer: multi-aspect
axis: cross-axis
vision_usage: implicit
---

# adapter

- **Class**: PRIMITIVE (atomic; the external-integration-boundary unit) — **tri-aspect Pattern A** (Adapter Protocol surface = mechanism; implementations = Framework C definitions; running instance = workspace-bound at Owner B per workspace.md adapter bindings)
- **Layer**: multi-aspect (framework-mechanism for the Protocol surface; Framework C for implementations; Owner B at workspace runtime — typically MULTIPLE adapter instances active per workspace, distinct from substrate's structural-singularity)
- **Axis**: cross-axis (different adapters serve different axes — email-adapter primarily axis-3 sending semantics; accounting-adapter cross-cutting business operations; MCP-adapter cross-axis tooling)
- **VISION usage**: implicit (architectural primitive supporting practitioner workflows that interact with external systems; not directly named in current VISION)

**Canonical**: An external-integration-boundary primitive — defines how a workspace interacts with EXTERNAL-WORLD systems via an Adapter Protocol surface; concrete implementations (gmail, outlook, fastbill, lexware, MCP-server, A2A-peer, etc.) live as Framework C definitions; a workspace activates one or more adapter instances via `workspace.md` adapter bindings. Architecturally distinct from `substrate` along the **internal-vs-external axis**: substrate = INTERNAL runtime contract for agent execution within the workspace; adapter = EXTERNAL-WORLD integration boundary connecting workspace to outside systems. Both are Pattern A primitives; cardinality (substrate singular, adapter multiple) follows from this distinction.

**What it is**: The Pattern A primitive for external-system integration. Each adapter has:
1. **Surface** (mechanism; framework-level): an Adapter Protocol contract per integration-class (e.g., the email-adapter Protocol surface defines send / fetch / threading semantics applicable to ANY email backend; the accounting-adapter Protocol surface defines invoice / payment / ledger semantics applicable to ANY accounting system)
2. **Implementations** (Framework C; distributable): concrete realizations (gmail-adapter, outlook-adapter, generic-SMTP-adapter for email; fastbill-adapter, lexware-adapter for accounting; MCP-server-adapter for MCP-protocol backends; A2A-peer-adapter for federation peers per archived `a2a-and-gemini-pattern-emulation.md`)
3. **Instance/binding** (Owner B; workspace-bound): the active implementation in a deployment, typically MULTIPLE simultaneously (a practitioner-shape workspace might run gmail-adapter + fastbill-adapter + MCP-corpus-adapter concurrently)

Skills invoke adapters at runtime (e.g., draft-cover-mail skill invokes email-adapter to send Begründung); specialists may bundle adapter implementations as part of their package (per locked `specialist` entry composes-with: "specialists may bundle adapter implementations as part of their package").

**What it is NOT**:
- Not the `substrate` — substrate is the INTERNAL runtime contract for agent execution (agent loop, tool surface, permission flow, lifecycle events) WITHIN the workspace; adapter is the EXTERNAL-WORLD integration boundary connecting workspace to outside systems. Both are Pattern A primitives but serve different architectural scopes (internal vs external).
- Not a `specialist` — specialists may USE adapters (and may bundle implementations); the adapter is the integration boundary itself, not codified expertise
- Not a `single mechanism` — Pattern A: Surface + Impls + Instance; mechanism is atomic without multiple impls
- Not a `workflow` — adapters serve workflow steps that involve external-system interaction; adapter is the integration primitive, workflow is the work-pattern
- Not an MCP tool per se — MCP-server-adapter is one specific adapter implementation; adapter as a primitive is broader (covers email, accounting, A2A, file-sync, etc.)

**Cross-archetype illustration** (named, archived examples; bidirectional vs unidirectional shape varies per impl-class):
- **Practitioner-shape (PBS-Schulz pioneer)**: email-adapter (mostly outbound send + threading on inbound; per archived `draft-cover-mail` skill); accounting-adapter (request/response invoicing per archived `invoicing` specialist); MCP-corpus-adapter (request/response sync; LanceDB backend per archived `backend-conventions.md`)
- **Autonomous-business-shape**: CRM-adapter, payment-processor-adapter, customer-system-adapter
- **Personal-OS-shape**: calendar-adapter, task-system-adapter, note-app-adapter
- **Federation-shape**: A2A-peer-adapter (bidirectional async; cross-node specialist sharing per archived `a2a-and-gemini-pattern-emulation.md`)
- **Hybrid-shape**: combinations across all of the above

**Boundary test**: Five questions:
1. Is this primarily about INTERNAL agent execution (runtime contract for the workspace's agent loop)? → it's the `substrate`, not adapter
2. Is this primarily about EXTERNAL-WORLD integration (workspace ↔ outside system)? → it's an adapter
3. Is this codified expertise bundled for a competence area? → it's a `specialist` (which may USE adapters)
4. Is this an atomic interface contract without multiple implementations? → it's a `mechanism`
5. Is this the meta-pattern shape itself (Surface + Impls + Instance)? → it's `protocol (architectural)` — the META-PRIMITIVE

**Composes with**:
- [mechanism](mechanism.md) — Adapter Protocol surface IS a mechanism (atomic interface contract)
- [Framework C scope](framework-c-scope.md) — adapter implementations live there as distributable definitions
- [Owner B scope](owner-b-scope.md) — running adapter instances bound to workspace deployment
- [protocol (architectural)](protocol-architectural.md) — adapter is a Pattern A instance; META-PRIMITIVE protocol describes the pattern shape
- [substrate](substrate.md) — counterpart Pattern A primitive (substrate = INTERNAL runtime contract; adapter = EXTERNAL integration); adapters run WITHIN the substrate's execution
- [skill](skill.md) — skills invoke adapters at runtime to interact with external systems (e.g., draft-cover-mail → email-adapter; verify-citations → MCP-corpus-adapter)
- [specialist](specialist.md) — specialists may bundle adapter implementations as part of their package
- [workspace](workspace.md) — workspace activates one-or-more adapter instances via `workspace.md` adapter bindings
- [shape](shape.md) — shape policies may mandate certain adapters or constrain permitted ones (e.g., practitioner-shape may mandate audit-emitting adapter behavior per axis-3 defensibility)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" — adapter listed as Pattern A primitive instance (alongside substrate)
- Locked GLOSSARY entries: [protocol (architectural)](protocol-architectural.md) ("adapter — specific Pattern A instance (workspace-activated; multiple per workspace possible)"); [substrate](substrate.md) (Composes-with: "adapter — specific Pattern A instance (workspace-activated; multiple per workspace possible)"); [specialist](specialist.md) ("specialists may bundle adapter implementations as part of their package")
- Archived corpus for full per-adapter detail (Phase 3 ARCH territory): `a2a-and-gemini-pattern-emulation.md` (A2A peer adapter), `plugin-conventions.md` (MCP-tool integration), `backend-conventions.md` (MCP-corpus adapter)

**See**:
- [protocol (architectural)](protocol-architectural.md) (META-PRIMITIVE describing Pattern A shape)
- [substrate](substrate.md) (parallel Pattern A primitive; structurally singular vs adapter's multiplicity; INTERNAL runtime vs EXTERNAL integration)
- [specialist](specialist.md) (which may bundle adapter implementations)
- [skill](skill.md) (which invokes adapters at runtime)
- ARCH Layer 3 adapter-detail topics (placeholder until Phase 3 — per-integration-class Adapter Protocol Surface specifications, per-implementation detail, audit-emission + permission-flow integration, lifecycle / auth-refresh / error-handling semantics; archived material to consult: `a2a-and-gemini-pattern-emulation.md`, `plugin-conventions.md`, `backend-conventions.md`)
