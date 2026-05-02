---
entry: substrate
class: PRIMITIVE
layer: multi-aspect
axis: cross-axis
vision_usage: implicit
---

# substrate

- **Class**: PRIMITIVE (atomic; the deployment-runtime unit) — **tri-aspect Pattern A** (Protocol surface = mechanism; implementations = Framework C definitions; running instance = workspace-bound at Owner B)
- **Layer**: multi-aspect (framework-mechanism for the Protocol surface; Framework C for implementations; Owner B at workspace runtime)
- **Axis**: cross-axis (substrate hosts all axes' runtime behavior)
- **VISION usage**: implicit (VISION doesn't directly use "substrate"; concept lives in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE + Framework C scope members)

**Canonical**: A deployment runtime that workspaces run on — defines the execution model (agent loop, dataflow, event-driven, etc. — substrate-impl-defined), tool surface, capability/permission flow, lifecycle events, and session/context primitives via a Protocol surface; concrete implementations (Claude Agent SDK, MS Agent Framework, future) live as Framework C definitions; a workspace selects exactly one substrate via its `workspace.md`.

**What it is**: One of the framework's mechanism categories (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE). The substrate provides the runtime contract any workspace operates on. The Protocol surface (interface contract) is universal/shape-neutral; specific implementations differ in how they realize that surface (e.g., Claude Agent SDK = Anthropic plugin runtime; MS Agent Framework = Microsoft agentic framework). **Substrate is an instance of the Protocol pattern** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Recurring patterns: Protocol pluggability"): Substrate Protocol Surface (mechanism; framework-level) + concrete Implementations (Framework C definitions: Claude Agent SDK, MS AF, future) + a running Instance bound to each workspace deployment (Owner B; via `workspace.md` `substrate:` field). NOT the same as specialist's bipartite manifestation (specialist is definition+instance-content; no multiple implementations like substrate has).

**What it is NOT**:
- Not the `framework` itself — framework is the universal mechanism layer; substrate is one mechanism category within the framework
- Not a `shape` — shape is the policy bundle archetype; substrate is a runtime-contract mechanism that shapes specify compatibility with (not equivalent)
- Not a `workspace` — workspaces select a substrate via `workspace.md`; substrate is what they run ON
- Not the `codebase` — substrate is the architectural runtime contract + its implementations; the codebase realizes one substrate impl

**Cross-archetype illustration**: All shapes use SOME substrate; not all shapes are compatible with all substrates. Examples (named, factually existing):
- **Claude Agent SDK** — Anthropic's plugin/agent runtime; archived as primary substrate per substrate eval
- **MS Agent Framework** — Microsoft's agentic framework; archived as second backend
- (Future substrates may emerge — e.g., specialized runtimes for Tier-3 / federation / autonomous-business shapes)

A practitioner-shape PBS-Schulz workspace might run on Claude Agent SDK; a knowledge-graph-shape workspace might run on a different substrate optimized for retrieval; the SAME framework mechanisms (audit emission, source-grounding, etc.) compose with each.

**Boundary test**: ask "what's the runtime contract this workspace operates on?" → it's the substrate. Three disambiguators:
1. Is this a runtime-contract Protocol surface or implementation? → substrate (mechanism + Framework C definition)
2. Is this a configured value in a shape's bundle? → it's a `policy`, not substrate
3. Is this a workspace-instance-level binding? → it's workspace configuration (workspace selects which substrate)

**Composes with**:
- [framework](framework.md) — substrate is one mechanism category within the framework
- [mechanism](mechanism.md) — the substrate's Protocol surface IS a mechanism (framework-level interface contract)
- [Framework C scope](framework-c-scope.md) — substrate IMPLEMENTATIONS live here as distributable definitions
- [shape](shape.md) — shapes declare compatibility with substrates (not all shapes work on all substrates)
- [workspace](workspace.md) — workspace selects exactly one substrate via `workspace.md`
- [Owner B scope](owner-b-scope.md) — running substrate instance is bound to workspace deployment (Owner B)
- [protocol (architectural)](protocol-architectural.md) — substrate Protocol surface is one of the framework's architectural Protocols

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" — substrate listed as Framework C definition member + framework-mechanism category
- [Framework C scope](framework-c-scope.md) GLOSSARY entry: "substrate definitions (runtime contracts: Claude Agent SDK, MS AF, future)"
- [workspace](workspace.md) GLOSSARY entry: "workspace runs on exactly one substrate"

**See**:
- [Framework C scope](framework-c-scope.md) (where substrate definitions live)
- [workspace](workspace.md) (which selects exactly one substrate)
- ARCH Layer 3 substrate-detail topics (placeholder until Phase 3 — Substrate Protocol method set; per-substrate implementation detail; deployment-tier framing; eval-framework integration; archived material to consult: `substrate-protocol-design.md`, `substrate-agentic-framework.md`, `sdk-deep-read.md`)
