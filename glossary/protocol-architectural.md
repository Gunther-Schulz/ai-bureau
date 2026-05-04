---
entry: protocol (architectural)
class: META-PRIMITIVE
layer: multi-aspect
axis: cross-axis
vision_usage: implicit
---

# protocol (architectural)

- **Class**: META-PRIMITIVE (the Pattern A architectural shape itself; named architectural Protocols + `substrate` + `adapter` are specific PRIMITIVE instances of this pattern)
- **Layer**: multi-aspect (Surface = framework-mechanism; Implementations = Framework C; Instance/binding = workspace-bound or shape-policy-selected)
- **Axis**: cross-axis (different Pattern A protocols serve different axes — Substrate Protocol = cross-axis; Adapter Protocol = cross-axis; Quality-gate Protocol = cross-axis. Sparring + audit are Pattern D mechanism classes — NOT Pattern A protocols — per Reclassifications subsection below; sparring still anchors VISION axis 2 at the mechanism-class layer)
- **VISION usage**: implicit (architectural concept underlying mechanisms across all axes; not directly named in current VISION)

**Canonical**: The Pattern A architectural shape — pluggable subsystem with Surface (interface-contract mechanism) + multiple Implementations (Framework C definitions) + Instance/binding (the active implementation, selected per workspace or shape-policy). META-PRIMITIVE (the pattern itself); specific instances of this pattern are PRIMITIVEs: `substrate` (locked), `adapter` (locked), `quality-gate` (locked). Disambiguated from **Pydantic Protocol** (the Python typing concept; PEP 544 structural typing) — though architectural Protocols often USE Pydantic Protocol as their Surface implementation technique, the architectural concept is broader.

**What it is**: The Pattern A architectural shape made concrete. Each protocol-instance has:
1. **Surface** (mechanism; framework-level): an abstract Protocol contract defining what the subsystem provides
2. **Implementations** (Framework C; distributable): concrete realizations of the surface
3. **Instance/binding** (Owner B; workspace-bound, OR shape-policy-selected): the active implementation in a deployment

Different selection levels exist across instances:
- **Substrate Protocol**: workspace selects (one running instance per workspace via `workspace.md substrate:` field)
- **Adapter Protocol**: workspace activates instances (multiple may run; per workspace.md adapter bindings)
- **Quality-gate Protocol**: shape selects (practitioner-shape selects `practitioner-shape-gate` impl; autonomous-business-shape selects `autonomous-business-shape-gate`; personal-OS-shape selects `personal-OS-shape-gate`) — selection lives in shape-policy

**What it is NOT**:
- Not **Pydantic Protocol** — Pydantic Protocol is the Python typing concept (`typing.Protocol`); architectural Protocol is the broader pluggable-subsystem pattern. Architectural Protocols may USE Pydantic Protocol for their Surface implementation, but the pattern is independent of Python.
- Not a single `mechanism` — a mechanism is atomic; protocol-instances have multiple impls + selection beyond the surface alone
- Not itself a primitive — protocol is the META-PRIMITIVE pattern; specific Pattern A instances (`substrate`, `adapter`, named architectural Protocols) are the PRIMITIVEs
- Not a workflow or session — protocols are framework-level architectural primitives; workflows + sessions are runtime/work-pattern concepts

**Cross-archetype catalog (named architectural protocols)**:
- **Substrate Protocol** (locked) — runtime contract; workspace selects one
- **Adapter Protocol** (locked; per `adapter` GLOSSARY entry) — pattern instance per integration class (email adapter, accounting adapter, MCP adapter, etc.)
- **Quality-gate Protocol** (locked; per `quality-gate` GLOSSARY entry) — runtime checkpoint mechanism for category-collapse resistance; shape selects implementation (practitioner-shape-gate / autonomous-business-shape-gate / personal-OS-shape-gate; extensible)

**Reclassifications + subsumptions** (per `docs/decisions/greenfield-rederivation-pause.md` Step 3 verdict): the prior 8-protocol catalog inherited from archive included Sparring + Audit + Coordination + Trust + Time as Pattern A protocols; greenfield re-derivation reduced the Pattern A catalog to the 3 protocols above. Specifically:
- **Sparring** + **Audit** are **mechanism classes** with per-shape policy variation, NOT Pattern A protocols. Sub-mechanisms ARE the Surface; per-shape variation is POLICY-level (which sub-mechanisms active / granularity / how-enforced), not IMPL-level alternative architectures. Sparring still anchors VISION axis 2; reclassification is at framework-mechanism layer only.
- **Coordination** is subsumed into substrate (hook system + event-bus mechanisms; per-shape policy configures call-shape vs event-shape).
- **Trust** is subsumed into the authority-binding mechanism (per-shape policy declares trust model: practitioner-judgment / budget-policy / individual).
- **Time** is subsumed into substrate-impl temporal semantics + adapter time-driven operations (no separate Time Protocol Surface with alternative implementations).

Per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE: framework provides protocols + their surfaces; shapes provide policies selecting implementations + parameterizing them.

**Boundary test**: Three questions:
1. Is this an architectural pluggable subsystem with Surface + Impls + Instance/binding? → it's a Pattern A instance (a PRIMITIVE — `substrate` / `adapter` / one of the named architectural Protocols)
2. Is this the Python typing structural concept (`typing.Protocol`)? → that's Pydantic Protocol — different concept; architectural Protocol may use it as implementation technique
3. Is this a single atomic interface contract without multiple impls? → it's a `mechanism`, not a Protocol

**Composes with**:
- [mechanism](mechanism.md) — Protocol Surface IS a mechanism (atomic interface contract)
- [Framework C scope](framework-c-scope.md) — Protocol implementations live there as distributable definitions
- [shape](shape.md) — shape policies select among Protocol implementations for shape-policy-selected protocols (like Sparring)
- [workspace](workspace.md) — workspace activates specific Protocol instances per workspace.md (for workspace-selected protocols like substrate) or inherits shape's selections
- [substrate](substrate.md) — specific Pattern A instance (workspace-selected)
- [adapter](adapter.md) — specific Pattern A instance (workspace-activated; multiple per workspace possible; EXTERNAL-integration counterpart to substrate's INTERNAL runtime contract)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" — defines Pattern A; lists known instances (substrate, adapter, protocol meta)
- Locked GLOSSARY entries: [substrate](substrate.md) (Pattern A instance; tri-aspect explicitly described); [mechanism](mechanism.md) (Protocol Surface listed as mechanism example: "Substrate Protocol Surface")
- Archived corpus for full per-protocol detail (Phase 3 ARCH territory): `substrate-protocol-design.md`, `shape-extension-and-architectural-floor.md`

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" (canonical pattern description)
- [substrate](substrate.md) (canonical Pattern A instance; locked)
- [adapter](adapter.md) (canonical Pattern A instance — workspace-activated multiple; EXTERNAL-integration counterpart)
- [mechanism](mechanism.md) (Protocol Surface IS a mechanism)
- ARCH Layer 3 per-protocol topics — per-protocol Surface specifications, per-implementation detail, selection mechanics per Pattern A topic-template (12 common-required + 7 conditional sections per `MAINTENANCE.md` Layer 3 Pattern A template; FORMAL STABILITY achieved 3 of 3 Pattern A instances): [arch/substrate.md](../arch/substrate.md) (Pattern A anchor; LOCKED), [arch/adapter.md](../arch/adapter.md) (Pattern A second instance; LOCKED), [arch/quality-gate.md](../arch/quality-gate.md) (Pattern A third instance; LOCKED Phase 3.6); mechanism-class topic-template extension via [arch/sparring.md](../arch/sparring.md) + [arch/audit.md](../arch/audit.md) (Pattern D mechanism-class; LOCKED)
