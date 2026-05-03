---
entry: policy
class: PRIMITIVE
layer: shape-policy
axis: cross-axis
vision_usage: implicit
---

# policy

- **Class**: PRIMITIVE (atomic; irreducible unit of a shape's bundle)
- **Layer**: shape-policy (this entry describes the atomic unit at the shape layer)
- **Axis**: cross-axis (policies can configure any axis-related mechanism)
- **VISION usage**: implicit (VISION doesn't use "policy" as a defined term; the framework=mechanisms / shape=policies framing is locked in `MAINTENANCE.md`, not VISION)

**Canonical**: An atomic configured value within a shape — a single requirement, default, or constraint configuring how a framework mechanism is used for that shape's archetype; the smallest unit of "what's MANDATED" a shape declares.

**What it is**: The atomic unit of a shape's policy bundle. Policies are shape-level — they configure framework mechanisms for a specific archetype, with shape-specific values. They define WHAT'S MANDATED (out of what the framework's mechanisms make POSSIBLE). Multiple policies compose into a shape's bundle; the shape is the container.

**Examples** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table; practitioner-shape policies):
- Audit granularity = claim-level (configures the framework's audit-emission mechanism)
- Sparring always-on as runtime pillar (configures the sparring mechanism)
- Human authority required somewhere in accountability-bearing output chain (configures authority-binding mechanism)
- Modifications require explicit re-conformance event (configures specialist-modification mechanism)
(Per other shapes, different policies configure the same mechanisms differently — see cross-archetype illustration below.)

**What it is NOT**:
- Not a `mechanism` — mechanisms are atomic INTERFACE CONTRACTS in the framework; policies are atomic CONFIGURED VALUES in a shape
- Not a `shape` — shape is the BUNDLE of policies (container); a single policy is one element
- Not a workspace-instance configuration — policies live at SHAPE level (in a shape definition's bundle); workspace deployments inherit them from the selected shape
- Not the framework — framework provides the mechanisms; policies live in shapes that layer over the framework

**Cross-archetype illustration** (same mechanism, different policies per shape): the framework provides the audit-emission MECHANISM (AuditEvent schema + `actor_kind` enum). Different shapes declare different POLICIES configuring it:
- Practitioner-shape policy: audit granularity = claim-level; emission required for every output
- Autonomous-business-shape policy: audit granularity = action-level; emission per task
- Personal-OS-shape policy: audit granularity = light; emission optional

Same mechanism (the framework's audit-emission contract); different policies (each shape's archetype-specific values).

**Boundary test**: Three questions:
1. Is this a configured value (a default, requirement, or constraint)? → likely a policy
2. Is this shape-specific (varies by archetype)? → likely a policy (lives in a shape's bundle)
3. Is this an interface contract any shape could use? → it's a `mechanism`, not a policy

If a candidate fails test 2 (it's universal across shapes; no archetype variation), it's not a policy — it's mechanism territory.

**Composes with**:
- [shape](shape.md) — contains policies as its atomic bundle elements (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [mechanism](mechanism.md) — counterpart atom in the framework=mechanisms / shape=policies framing (mechanism = framework atom; policy = shape atom)
- [framework](framework.md) — contains mechanisms over which policies are LAYERED (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- [workspace](workspace.md) — selects a shape and inherits its policies
- `adapter` (Pattern A protocol per `arch/adapter.md`) — shape-extension class concept lives at policy bundle layer (per `arch/adapter.md` §3 framework-baseline-vs-shape-extension partition); shape-extension classes are additive policy bundle elements beyond framework-baseline
- `sparring` (mechanism class per `arch/sparring.md`) — shape-extension sub-mechanism concept lives at policy bundle layer (per `arch/sparring.md` §4 framework-baseline-vs-shape-extension partition); shape-extension sub-mechanisms are additive policy bundle elements beyond framework-baseline
- [authority-binding](authority-binding.md) — per-shape trust policy lives at policy layer; authority-binding mechanism is shape-neutral framework primitive that policy declares trust-model variation over (practitioner-judgment / budget-policy / individual per `audit` class §14 cross-shape policy variation)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section: "policy is the atom — a single configured value; requirement/default/constraint"
- `MAINTENANCE.md` "Concept-by-concept (worked examples)" table: practitioner-shape column = examples of policies per axis

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section (atom-vs-container relationship + concept-by-concept worked examples)
- Other foundational meta-primitives + atoms: [mechanism](mechanism.md), [framework](framework.md), [shape](shape.md)
- [Framework C scope](framework-c-scope.md) — where shape definitions (containing policy bundles) live
- `arch/sparring.md` §4 + `arch/audit.md` §14 + `arch/adapter.md` §3+§14 (Phase 3.4 locked — framework-baseline-vs-shape-extension partition lives at policy bundle layer); `arch/scope-model.md` (Phase 3.5 forthcoming — entity placement composing with policy bundles)
