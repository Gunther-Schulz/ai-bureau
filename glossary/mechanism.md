---
entry: mechanism
class: PRIMITIVE
layer: framework-mechanism
axis: cross-axis
vision_usage: implicit
---

# mechanism

- **Class**: PRIMITIVE (atomic; irreducible unit of the framework)
- **Layer**: framework-mechanism (this entry describes the atomic unit at the framework layer)
- **Axis**: cross-axis (mechanisms can serve any of the three VISION axes)
- **VISION usage**: implicit (VISION uses "mechanisms" in plural for trust/sparring/authorship mechanism classes; doesn't define "mechanism" as singular term — that's `MAINTENANCE.md` territory)

**Canonical**: An atomic interface contract within the framework — a single capability with defined input/output surface, available to any workspace shape; the smallest unit of "what's POSSIBLE" the framework provides.

**What it is**: The atomic unit of the framework. Mechanisms are universal — usable by any shape, no shape-specific values embedded. They define WHAT'S POSSIBLE; shape policies determine WHAT'S MANDATED out of those possibilities. Multiple mechanisms compose into the framework alongside protocols (pluggable subsystems) and architectural disciplines (rules), per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE.

**Examples** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table):
- `AuditEvent` schema (Pydantic model contract for audit emission)
- `actor_kind` enum (declared on every audit event; framework-level guarantee)
- Pydantic gate (validator function dispatched on every contract-bearing write)
- Specialist conformity manifest schema (declaring a specialist's conformity surface as a Pydantic schema)
- Sparring Protocol surface (the architectural-protocol's interface contract, before any specific implementation)
- Source-grounding capability (every claim traceable to source; framework-level enforcement)
- Visible reasoning capability (Pydantic field on outputs requiring reasoning chain)

**What it is NOT**:
- Not a `policy` — policies are atomic CONFIGURED VALUES (defaults, requirements, constraints) within a shape's bundle; mechanisms are atomic INTERFACE CONTRACTS in the framework
- Not a `protocol` (architectural) — a protocol's surface IS a mechanism, but the protocol-with-multiple-implementations structure adds composition beyond a single mechanism
- Not the `framework` itself — the framework is the CONTAINER of mechanisms (+ protocols + disciplines); a single mechanism is one element of the container
- Not a workspace-level or instance-level construct — mechanisms live at framework level with no shape-specific values
- Not an architectural discipline — disciplines are RULES about how to design (canonical homes: `MAINTENANCE.md` + `DISCIPLINES.md`); mechanisms are CAPABILITIES the framework provides

**Cross-archetype illustration**: All workspace shapes use the SAME mechanisms (e.g., the `AuditEvent` schema is the same Pydantic contract in practitioner-shape, autonomous-business-shape, etc.). What differs across shapes is which mechanisms are MANDATORY, the granularity at which they're invoked, and what defaults apply — these are policies (shape-level), not mechanism variations.

**Boundary test**: Three questions:
1. Is this an atomic capability with a defined input/output surface? → likely a mechanism
2. Is this shape-neutral (any shape could use it)? → likely a mechanism (lives in framework)
3. Is this a configured value (default, requirement, mandatory)? → it's a `policy`, not a mechanism

If a candidate fails test 2 (it IS shape-specific), it doesn't belong as a framework mechanism. Move to shape-extension.

**Composes with**:
- [framework](framework.md) — contains mechanisms as its atomic interface contracts (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [policy](policy.md) — counterpart atom in the framework=mechanisms / shape=policies framing
- [shape](shape.md) — applies policies OVER mechanisms (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [protocol (architectural)](protocol-architectural.md) — pluggable subsystem within the framework (relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section: "mechanism is the atom — a single interface contract; capability with defined input/output surface"
- `MAINTENANCE.md` "Concept-by-concept (worked examples)" table: examples per axis (audit emission, specialist modification, authority binding, sparring)

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section (atom-vs-container relationship + concept-by-concept worked examples)
- Other foundational meta-primitives + atoms: [framework](framework.md), [shape](shape.md), [policy](policy.md)
- ARCH Layer 3 mechanism-detail topics (placeholder until Phase 3 — per-mechanism canonical detail)
