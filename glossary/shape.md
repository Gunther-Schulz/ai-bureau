---
entry: shape
class: META-PRIMITIVE
layer: framework-meta
axis: cross-axis
vision_usage: directly-used
---

# shape

- **Class**: META-PRIMITIVE (container; the category of policy bundles, not a single policy itself)
- **Layer**: framework-meta (this entry describes the shape layer concept itself)
- **Axis**: cross-axis (shapes can have policies serving any axis)
- **VISION usage**: directly used (`VISION.md` lines 11, 17, 19, 21, 72)

**Canonical**: A workspace archetype — a bundle of policies layered over framework mechanisms, configuring what's MANDATED for that archetype. Shape definitions are themselves framework primitives (live in Framework C scope); a workspace selects exactly one shape via its `workspace.md`.

**What it is**: A shape provides the "what's MANDATED" layer for a workspace archetype, per the framework/shape architectural relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE. Each shape declares its policies + may add shape-specific primitives needed for its archetype. PBS as marketed product positions on practitioner-shape; the framework underneath is shape-neutral and supports multiple shapes.

**What it is NOT**:
- Not a workspace (a workspace IS DEPLOYED as a specific shape's archetype; the shape is the configuration definition)
- Not the framework (shape sits OVER framework per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; framework is the universal mechanism layer)
- Not a deployment instance (shape DEFINITIONS are universal/distributable; live in Framework C scope; per-deployment selection happens via `workspace.md`)
- Not a single policy (shape is a BUNDLE)
- Not always practitioner-shape (PBS markets practitioner-shape; framework supports multiple shapes — see named-shapes catalog below)

**Cross-archetype catalog (named shapes — canonical per-shape detail forthcoming)**:
- **practitioner-shape** — workspace shape for accountability-bearing expert work; PBS marketed positioning + pioneer reference
- **autonomous-business-shape** — operator-supervised multi-agent shop
- **personal-OS-shape** — individual life-OS
- **knowledge-graph-shape** — corpus + curation; no workflow loop
- **federation-shape** — cross-node specialist sharing
- **hybrid-shape** — combinations of above

**Boundary test**: Three questions:
1. Is this an atomic unit contained within a shape (one element of its bundle)? → it's a `policy`
2. Is this an interface contract any shape could use? → it's a `mechanism` (lives in framework, not shape)
3. Is this a bundle of policies for a workspace archetype? → it's a shape

**Composes with**:
- [framework](framework.md) — counterpart in the framework/shape architectural relationship (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [policy](policy.md) — atomic unit contained within a shape's bundle
- [workspace](workspace.md) — deploys exactly one shape via `workspace.md`
- [Framework C scope](framework-c-scope.md) — where shape DEFINITIONS live as distributable framework primitives
- [mechanism](mechanism.md) — what shape policies configure (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)

**Source**:
- VISION (`VISION.md`):
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Line 17: "Framework primitives support multiple workspace shapes via shape-extension pattern"
  - Line 19: "this document remains the practitioner-shape articulation"
  - Line 21: "framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory"
  - Line 72: "framework is restricted to practitioner shape — framework is shape-neutral"
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" for framework/shape relationship + concept-by-concept worked examples
- `MAINTENANCE.md` Layer 3 description Pattern A protocol topic template §14 cross-shape policy variation conditional (per `docs/decisions/pattern-a-template-7th-conditional-cross-shape-variation.md`) — shape policy bundles mediate per-shape variation in shape-policy-mediated Pattern A protocols (adapter audit emission / permission flow / error escalation per shape; quality-gate enforcement per shape)
- [Framework C scope](framework-c-scope.md) (where shape definitions live)
- ARCH Layer 3 shape topic + per-shape detail (placeholder until Phase 3)
- Other foundational meta-primitives: [framework](framework.md), [mechanism](mechanism.md), [policy](policy.md)
