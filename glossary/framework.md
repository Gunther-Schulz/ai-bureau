---
entry: framework
class: META-PRIMITIVE
layer: framework-meta
axis: cross-axis
vision_usage: directly-used
---

# framework

- **Class**: META-PRIMITIVE (container; the bounded category that contains mechanisms, protocols, and architectural disciplines)
- **Layer**: framework-meta (this entry describes the framework layer itself)
- **Axis**: cross-axis (the framework supports all three VISION axes; specific support per axis lives in mechanisms)
- **VISION usage**: directly used (`VISION.md` lines 17, 21, 72)

**Canonical**: The shape-neutral universal layer of the pbs-bureau architecture — the bounded set of mechanisms (atomic interface contracts), architectural protocols (pluggable subsystems), and architectural disciplines that any workspace shape can compose with.

**What it is**: The "what's POSSIBLE" boundary. The framework defines the universe of capabilities, contracts, and rules available to any workspace. The framework/shape architectural relationship — what's POSSIBLE (framework) vs what's MANDATED (shape) — is locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE. The framework is the open-source, marketed product's foundation; PBS-Schulz is one practitioner-shape deployment built from the framework.

The framework includes:
- **mechanisms** (audit emission, source-grounding, sparring Protocol surface, etc.)
- **architectural protocols** (Pattern A pluggable subsystems with multiple implementations): Substrate, Adapter, Quality-gate. Each is a PRIMITIVE primitive per its canonical GLOSSARY entry; all share Pattern A shape per `protocol (architectural)` entry. (Per `docs/decisions/greenfield-rederivation-pause.md` Step 3 greenfield re-derivation: prior catalog included Sparring + Audit + Coordination + Trust + Time as Pattern A protocols; greenfield re-derivation reclassified Sparring + Audit as mechanism classes with per-shape policy variation, and subsumed Coordination → substrate hook system + event-bus, Trust → authority-binding mechanism with per-shape policy, Time → substrate-impl temporal semantics + adapter time-driven operations.)
- **architectural disciplines** (cascade discipline, no-defer principle, preliminary-lock principle, make-wrong-shapes-impossible, AI-as-runtime hybrid-shape, pattern-vs-instance, glue-not-replacement)

**What it is NOT**:
- Not a specific shape's configuration (shape is the policy layer OVER the framework)
- Not the substrate (substrate is one mechanism within the framework's scope; framework is the layer that contains substrates among other mechanisms)
- Not the codebase per se (framework is the architectural layer; the codebase is one realization of the framework's mechanisms)
- Not a workspace or deployment instance (workspaces are BUILT FROM framework + shape policies + practitioners + state)
- Not market positioning or strategic claims (framework is shape-neutral; positioning lives in `STRATEGY.md`)

**Cross-archetype illustration**: All workspace archetypes share the SAME framework; they differ in which shape's policies they apply over framework mechanisms. Example shapes: practitioner-shape (PBS marketed positioning), autonomous-business-shape, personal-OS-shape, knowledge-graph-shape, federation-shape, hybrid-shape. Per-shape policy specifics live in canonical shape entries forthcoming (see [shape](shape.md) entry for the meta-primitive). Same framework underwrites all archetypes; shape policies determine what each one mandates.

**Boundary test**: Two questions:
1. "Is this thing shape-specific (only valid for one shape)?" If yes → not framework; it's shape-policy or shape-specific primitive.
2. "Is this thing an interface contract any shape could use?" If yes → framework-mechanism (lives within the framework).

If a candidate concept fails test 1 (it IS shape-specific), it doesn't belong in the framework. Move to shape-extension.

**Composes with**:
- [mechanism](mechanism.md) — atomic units of the framework (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [protocol (architectural)](protocol-architectural.md) — pluggable subsystems within the framework
- [shape](shape.md) — counterpart in the framework/shape architectural relationship (relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [workspace](workspace.md) — deployment-instance container that integrates framework + shape + specialists + practitioners

**Source**: VISION (`VISION.md`):
- Line 17: "The framework underneath is workspace-shape-neutral. Framework primitives support multiple workspace shapes via shape-extension pattern"
- Line 21: "The framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory"
- Line 72: "PBS does NOT claim the framework is restricted to practitioner shape — framework is shape-neutral; positioning is practitioner-focused"

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section (the foundational architectural commitment)
- `ARCHITECTURE.md` (Layer 2 overview; framework-mechanisms enumeration via topic catalog §4) + `arch/scope-model.md` (Phase 3.5 forthcoming — entity placement across Framework C / Owner B / Layer A)
- Other foundational meta-primitives: [shape](shape.md), [mechanism](mechanism.md), [policy](policy.md)
