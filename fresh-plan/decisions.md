# fresh-plan decisions

> Append-only decision ledger for the fresh dev plan started 2026-05-08 on branch `fresh-plan`.
>
> Format per entry: decision ID, date, decision (what), rationale (why), supersedes (which prior decision it overrides, if any).
>
> Discipline: entries are *locked* once added. Override = new entry that explicitly supersedes the prior. Never edit a locked entry's substance; clarifications go in a follow-up entry.
>
> Everything in the existing pbs-bureau corpus (VISION, ARCHITECTURE, MAINTENANCE, DISCIPLINES, GLOSSARY, arch/*, profiles/*, plugin/*, pbs/*, 1-NEXT through 5-PIVOT-DECISION) is treated as **input**, not as anchor. Each artifact's status (inherit-as-is / inherit-with-modification / re-derive / discard / defer) is itself a future ledger decision.

---

## D1 — 2026-05-08 — Build target + conflict rule

**Decision**: Primary target = reusable thing (framework / OSS / product). PBS-Schulz planning office = first deployment / proving ground (secondary). When the two pull in different directions, **generality wins**: defer PBS-Schulz-specific features that don't generalize.

**Rationale**: The prior corpus oscillated between "PBS-Schulz daily use is the goal" and "framework is the goal." Without explicit primary/secondary + conflict rule, framing drift kept reintroducing premature deployment-specific detail at framework level. Locking primary = reusable + conflict rule = generality first prevents the drift.

**Supersedes**: `5-PIVOT-DECISION.md` (which had PBS-Schulz as primary and framework paused).

**Open tension flagged**: PBS-Schulz is a real running planning office; daily work cannot pause while the reusable thing is built. A rule for keeping daily work running on whatever-already-works during the rebuild is needed; deferred to a later decision (likely under working procedure).

---

## D2 — 2026-05-08 — Framework-core = meta-layer; instances = extensions

**Decision**: Framework-core contains *kinds*, *contracts*, *vocabulary*, *identity / structural commitments*, and *extension protocol*. Core does NOT contain instances. "Build" = add conformant extensions to core; "build" never means modifying core.

Concretely:
- The *abstraction* "what a substrate is and how a substrate plugs in" → core.
- The Claude Agent SDK substrate impl → extension.
- The *abstraction* "what a shape is and what a shape must declare" → core.
- The practitioner-shape → extension.
- The *abstraction* "what an adapter is and what its contract is" → core.
- Email / Accounting / MCP-Server / A2A-Peer / File-Sync / desktop / etc. adapters → extensions.

**Rationale**: The prior corpus's `arch/adapter.md` mixed protocol-shape abstractions (MCP-Server, A2A-Peer) with domain-shape instances (Email, Accounting) at the same level. That category-collapse reproduces in any "framework body" that holds both abstractions and instances. Forcing core = meta-only and instances = extensions makes the boundary structurally enforceable rather than discipline-dependent.

**Supersedes**: any prior framing that treated specific Surface classes / specific shapes / specific substrates as part of framework-core.

---

## D3 — 2026-05-08 — Core is layered top-down

**Decision**: Within framework-core, the contents are layered top-down:
1. **Identity / structural commitments** (what makes the framework be itself).
2. **Kinds / contracts** (the schemas of what kinds of things plug in).
3. **Extension protocol** (the rules of conformance: how extensions declare themselves, how core validates conformance, how extensions compose, promotion / demotion rules).

Layer 1 constrains layer 2; layer 2 constrains layer 3. Enumeration proceeds top-down: identity locked first, then kinds, then extension protocol.

**Rationale**: Top-down respects dependency. A "kind" only makes sense in light of the framework's identity; an "extension protocol" only makes sense in light of which kinds exist. Bottom-up risks defining extension rules for kinds that turn out unnecessary, or kinds that don't actually serve identity.

---

## D4 — 2026-05-08 — Framework-core has no substantive identity commitments

**Decision**: Framework-core's *identity layer* contains only **structural** claims about what kind of system the framework is. It does NOT carry substantive disciplinary commitments (no axes, no required disciplines, no required outcome-shapes).

Substantive identity (e.g., intertwining, sparring, authorship preservation, defensibility, engaged-authorship) is carried by **shapes** as policy bundles. Each shape declares which substantive commitments it adopts.

PBS-as-a-product = framework + a default shape bundle (e.g., practitioner-shape) that embodies the substantive commitments commonly associated with "PBS" in the prior corpus.

**Rationale**: Each axis from the prior VISION (intertwining / sparring / authorship preservation / defensibility / engaged-authorship) failed the inclusion test — for each, a plausible shape (autonomous-business, personal-OS, etc.) could opt out and still legitimately use the framework. The prior corpus simultaneously asserted "shape-neutral" and "anchored on three axes," which contradicts itself. Pushing substantive identity to the shape layer resolves the contradiction and matches the user's meta-principle ("everything is defined on how to extend and build").

**Supersedes**: `VISION.md` three-axes-as-framework-anchor framing (axes preserved as practitioner-shape policy candidates, not framework identity).

**Open question (closed by D5)**: what *structural* commitments does the identity layer actually contain?

---

## D5 — 2026-05-08 — Framework-core identity layer (structural commitments)

**Decision**: The identity layer of framework-core (per D3 layer 1) contains three structural commitments. These are orthogonal facets — *what* the framework is, *how* it works, *what* it's for. Each fails the inclusion test if removed; together they distinguish the framework from (a) a vocabulary, (b) a generic SDK, (c) a generic meta-framework — without forcing substantive disciplinary content into core.

**I1 — WHAT: composition system.** The framework's job is composing extensions — shapes, substrates, adapters, specialists, disciplines — over a *workspace*. The framework is not an SDK, not a runtime, not a vocabulary; it is the meta-layer where these compose.

**Workspace** (organizing primitive at identity level): the bounded coordination context where one composition runs. Has an identity, a composition (which extensions are bound), a state (what accumulates within it), and a lifecycle. Two workspaces are independent compositions — they may share extensions but their compositions don't bleed. Workspace is NOT a folder, a manifest file, a session, or a deployment instance — those are implementations / runtime episodes / colloquial names. The workspace *kind* (contract, manifest schema, state shape, lifecycle) will be defined at layer 2.

**I2 — HOW: machine-checkable contracts on kinds.** Every kind defined in core carries a contract that the framework can validate. Conformance is structural, not prose-convention. An extension declaring itself as kind K is checkably K — the framework can verify the claim. This is what distinguishes framework-as-framework from framework-as-style-guide.

**I3 — FOR: accountability-bearing AI-human work.** The framework targets work where attribution, reasoning, and authorship matter. Its kinds (to be enumerated at layer 2) are designed around accountability semantics, not as afterthoughts. Use for non-accountability-bearing domains is possible but unprivileged.

**Note on consistency with D4**: I3 sounds substantive at first read but is *domain-structural*, not *disciplinary-substantive*. It says **which kinds the framework cares about** (accountability semantics), not **which disciplines a deployment must perform**. A deployment can use the framework for accountability-bearing work without committing to sparring, intertwining, or any particular axis. The kinds support accountability-bearing disciplines; they don't require any specific discipline.

**Rationale**: Three orthogonal facets emerged from running the inclusion test on the prior corpus's "axes." Each prior axis failed the test as identity (a plausible shape could opt out). What survived was thinner: structural claims about what the framework IS, HOW it works, WHAT it's for. I1/I2/I3 together carry just enough identity to make the framework a coherent thing while leaving substantive content to shapes per D4.

**Flagged for layer 2 (not identity)**:
- Cross-substrate portability (Pattern A's ≥2-impl prior discriminator) — likely a property of the substrate kind / contract.
- Workspace-as-kind (vs workspace-as-organizing-primitive in I1) — concrete contract belongs at layer 2.
- Human-in-the-loop — implied by I3 (accountability requires accountable actors), not its own identity claim.

---

## D6 — 2026-05-08 — Layer 2 enumeration approach (incremental + closure check)

**Decision**: Layer 2 (kinds) is enumerated kind-by-kind, with each kind locked as its own decision entry as it's accepted. After the top-down-from-identity derivation is exhausted, a closing entry sweeps the prior corpus's kind list to catch anything missed; the closure entry affirms "layer 2 enumeration complete" with the final kind set named.

**Rationale**: Incremental locking (each kind = one entry) avoids piled-up unlocked discussion between layer-2 start and end (drift-prone). The closure entry after the prior-list sweep makes "layer 2 done" explicit so we don't leak unfinished kinds into layer 3.

**Procedure**:
1. Derive each kind top-down from I1/I2/I3 — each kind earns inclusion by being load-bearing for at least one identity facet.
2. Lock each kind as its own decision entry (kind name + contract sketch + rationale).
3. After top-down exhaustion, sweep the prior corpus's kind candidates (substrate, shape, adapter, specialist, workspace, practitioner, claim, event, actor, discipline, workflow / work-unit, etc.) — for each, decide: already-covered / add-now / not-a-kind / defer.
4. Lock closure entry naming the final kind set.

---

## D7 — 2026-05-08 — Workspace kind

**Decision**: The workspace kind contract specifies four facets, derived from D5/I1's organizing-primitive role.

### 1. Identity

- Each workspace declares a stable, unique identifier.
- The identifier persists across the workspace's full lifecycle (boot → shutdown → resume across machines / sessions / years).
- Same identifier = same workspace (same composition lineage, same state lineage). Different identifier = independent composition.

### 2. Composition (declarative bindings)

The workspace declares which extensions it composes. Each binding references an extension that conforms to its respective kind contract. The framework validates conformance per I2.

**Cardinality:**
- **shape**: exactly 1 (the workspace is shape-typed; hybrid-shape mechanics deferred).
- **substrate-binding**: 1+ (binding can be specific, capability-based, or mixed — see §4 lifecycle).
- **adapter**: 0+.
- **specialist**: 0+.
- **actor**: 1+ (universal — workspaces require attributable actors per I3; actor = `human-actor` or `agent-actor` subtype). "Practitioner" is **not** a kind at this layer — it is a shape-level role-binding (e.g., practitioner-shape declares: "the human-actor who is the accountable principal of this workspace"). Other shapes may not use the term.

### 3. State (what accumulates)

A workspace accumulates state as composition runs. State survives between runtime sessions (workspace persists; sessions are runtime episodes within it).

**State contents:**
- **events**: timeline of attribution-bearing happenings. Single kind `event` with **payload subtypes** including `claim`, `action`, `state-change`, `composition-change`, `lifecycle-transition`, etc. Disciplines (later, in shapes) declare which payload subtypes they care about.
- **work-units**: active and historical units of work (work-unit kind defined separately).
- **scope**: current active domain / state within which composition is operating.

**Attribution closure (per I3)**: every state mutation is an event. Nothing escapes attribution. Even composition mutations (adding an adapter, retiring a specialist) flow through state as events.

### 4. Lifecycle

A workspace can boot, run, persist, and shut down.

- **boot**: read manifest → bind extensions → restore state → become operational.
- **run**: process events through composed extensions; accumulate state.
- **persist**: state survives between runtime episodes.
- **shut down**: clean exit; state persisted; bound substrate(s) released.

**Composition is mutable** during lifecycle (new bindings can be added; old bindings retired). Every composition mutation is itself an attribution-bearing event (per I3).

**Boot is triggered externally** (host process, user action, schedule, orchestrating agent, etc.); the workspace kind is agnostic to trigger mechanism. The **substrate hosts the agent loop**; the workspace is composed within the substrate's context. The workspace does not boot itself.

**Substrate-binding cardinality across lifecycle**:
- Manifest: 1+ substrate-binding declared (specific / capability-based / mixed).
- Runtime (running): 1+ substrate currently live and bound.
- Persisted, non-running: 0 substrates live; manifest declaration unchanged.

### Manifest vs runtime distinction

- **Manifest** = declarative — what this workspace IS (identity, bindings, intended composition). Persisted; survives between runs.
- **Runtime state** = accumulating — what's happening / has happened (events, claims, work-units, scope). Persisted between runs but grows during runs.
- **Together**: workspace = manifest + state. Both must conform to contract; framework validates manifest at boot and validates state-accumulation per event (per I2).

**Rationale**: each facet is load-bearing for at least one identity claim:
- Identity supports I1 (workspaces are distinguishable so compositions are independent).
- Composition supports I1 (it's what gets composed) + I2 (binding validation is structural conformance).
- State supports I3 (accumulation is attribution-bearing; event-recursive ensures nothing escapes attribution).
- Lifecycle supports I1 (boot/run/persist makes composition operationally real) + I3 (transitions are attribution-bearing).

**Open / deferred**:
- Concrete schema of the manifest (Pydantic, markdown, both, other) — implementation choice; layer-3 territory.
- Concrete persistence mechanism for state — implementation choice.
- Hybrid-shape mechanics (workspace with mixed shapes) — deferred; either becomes a separate kind or is handled as a shape-of-shapes.
- Multi-workspace federation (one actor across multiple workspaces) — deferred.

**Flagged for layer 2 follow-up kinds** (each becomes its own decision entry):
- `actor` (with subtypes `human-actor`, `agent-actor`).
- `event` (with payload-subtype machinery).
- `work-unit`.
- `substrate` (kind contract; capability declarations; binding semantics).
- `shape`, `adapter`, `specialist` — bound by workspace.

---

## D8 — 2026-05-08 — No "discipline" kind at framework-core layer 2

**Decision**: There is no unified `discipline` kind in framework-core. The mechanisms-formerly-called-disciplines from the prior corpus (audit, sparring, gate, authority-binding, etc.) decompose across the existing kinds and the shape layer:

- **Audit** → built into the workspace kind's state facet by construction (per D7 §3 + I3: every state mutation is an event; audit-trail is automatic). Not a kind.
- **Sparring** → shape policy bundle (per D4). The shape kind defines how policy is declared; specific sparring configurations live in specific shapes (e.g., practitioner-shape).
- **Gate / HITL checkpoints** → likely specialist capability and/or shape policy ("when does approval fire"). Not a kind.
- **Authority-binding** → shape policy ("which actor must attest which event-subtypes"). Not a kind.

**Rationale**: The prior corpus's "Mechanism Surface" pattern abstracted these mechanisms as if they shared a contract. They don't — audit is logging-by-construction, sparring is engagement, gate is a checkpoint, authority-binding is attestation. Each carries different semantics. A unified `discipline` kind would be over-abstraction (a shared base with no actually-shared contract). Per D2, kinds at framework-core are abstractions of distinct kinds-of-things; they should not be invented for symmetry.

**Supersedes**: prior corpus's "Mechanism Surface (Pattern A)" framing at framework-kind level. The Pattern A discriminator concept (≥2 conformant impls per kind) survives as a property of *each* kind that has it (likely substrate); it is not itself a unified meta-pattern at the kind layer.

**Note**: shape-level mechanisms (sparring, gate, authority-binding configurations carried by specific shapes) may share patterns *within a shape's policy bundle structure*. Whether shapes formalize that structurally is a shape-kind concern (defined when we get to the `shape` kind), not a discipline-kind concern.

---

## D9 — 2026-05-08 — Actor kind

**Decision**: The actor kind contract specifies an attribution-bearing participant in a workspace. Cardinality: 1+ per workspace (per D7); each actor has stable workspace-scoped identity and a subtype.

### Contract

- **`id`** — stable unique identifier within the workspace. Persists across substrate restarts, across runtime episodes, across the workspace's full lifecycle. Identity is workspace-scoped (not cross-workspace; cross-workspace coordination is out of scope for this kind).
- **`subtype`** — one of `human-actor`, `agent-actor`. Subtypes are open (other subtypes can be added as needed in future decisions).
- **Subtype-specific metadata** (kind-level structural slots; semantics not enforced by framework-core):
  - `agent-actor`: **`substrate-binding`** referencing a substrate declared in workspace.composition. The actor's runtime resolves through that substrate.
  - `human-actor`: **`declared-name`** (or equivalent free-form designation).

### Identity persistence (illustrative)

- Substrate restart → same actor (substrate session is not actor identity).
- Model version upgrade for an agent-actor → same actor (model version is metadata, captured in individual events; not actor identity).
- Same workspace running on a different substrate (per workspace.substrate-binding capability resolution) → same actors (actor identity is workspace-level, not substrate-level).
- Actor granularity is a workspace-level decision: one substrate may host multiple distinct agent-actors (e.g., interactive `claude-primary` vs cron-driven `claude-monthly-invoicing`); the workspace decides where actor boundaries fall, not the substrate.

### Linkage to events

Per D7 §3, every event has at least one actor. Per the actor kind: events reference actors by `id`, and the framework validates structurally (per I2) that referenced actor `id`s exist in the workspace manifest. Events may reference **multiple actors with role-tags** (e.g., `drafter`, `attester`, `reviewer`); role-tag vocabulary is **shape policy**, not part of the actor kind.

### Concrete example (PBS-Schulz workspace, illustrative only)

```
actors:
  - id: gunther-schulz
    subtype: human-actor
    declared-name: "Gunther Schulz"
  - id: claude-primary
    subtype: agent-actor
    substrate-binding: claude-agent-sdk
  - id: claude-monthly-invoicing
    subtype: agent-actor
    substrate-binding: claude-agent-sdk
```

A claim event might attribute to multiple actors with shape-declared roles (e.g., `claude-primary` as `drafter`, `gunther-schulz` as `attester`).

### What is NOT in the actor kind contract (deliberate omissions)

- **Authority** ("what events this actor may attest / authorize") → shape policy per D4. Framework-core's actor doesn't carry authority declarations.
- **Roles** (`drafter`, `attester`, `reviewer`, `practitioner`, etc.) → shape policy. Practitioner specifically is a shape role-binding on a `human-actor`, not a kind.
- **Cross-workspace identity** — out of scope. Whether two workspaces' `gunther-schulz` actors refer to the same human is a coordination-layer concern above the workspace kind.
- **Legal-personhood metadata** (Berufsrecht, professional licenses, etc.) → shape policy.
- **Capability declarations** (what tools an agent-actor can invoke) → substrate / specialist concern, not actor.

**Rationale**: actor is the minimal attribution-bearing participant kind. Per I3, every event needs an attributable subject; the actor kind provides exactly that, with subtype machinery to distinguish humans from agents (since their identity-resolution mechanics differ — humans persist via declared name + workspace-scope; agents persist via substrate-binding + workspace-scope). All substantive role/authority semantics push to shapes per D4.

---

## D10 — 2026-05-08 — Event kind

**Decision**: The event kind is the workspace's attribution-bearing record of happenings. Single kind; no separate `claim` kind (claim is a payload subtype). Every state mutation in the workspace flows through events (audit closure per I3).

### Contract slots

- **`id`** — unique within the workspace.
- **`prev-event`** — reference to the prior event in the workspace's chain. `null` only for the workspace's first event ever.
- **`timestamp`** — when the event happened.
- **`actors`** — at least one actor reference per D9. Each entry: `{ id, role? }`. The role-tag (e.g., `drafter`, `attester`, `authorizer`) is **shape policy** vocabulary, not part of the event kind.
- **`payload-subtype`** — one of the registered subtypes (core set below or extension-declared).
- **`payload`** — subtype-specific structure.

### Single chain per workspace

A workspace has one ordered event chain. `prev-event` forms the chain. The chain is **integrity-checkable** (the implementation provides a mechanism — hash-of-prev, append-only log, database with sequence constraint, etc.); the kind contract states the property, not the mechanism.

Filtered views (per-actor, per-work-unit, per-domain) are **derived by query**, not stored as separate chains. This keeps audit reconstruction linear and makes cross-cutting events (composition changes, lifecycle transitions) live naturally in the same chain as everything else.

### Core payload subtypes (framework-declared)

- **`claim`** — attributable assertion. Payload shape: free-form assertional content + (optional) confidence + (optional) evidence references. Practitioner-shape and similar shapes operate disciplines (sparring, attestation) on this subtype.
- **`action`** — something an actor did. Tool call, message sent, file read, external API invoke. Payload shape: action-name + parameters + outcome reference.
- **`state-change`** — workspace state mutation other than composition or lifecycle (e.g., scope set, work-unit transition). Payload shape: `what` + before/after references.
- **`composition-change`** — workspace composition binding/unbinding (per D7 §4 composition mutability). Payload shape: change-type + binding reference.
- **`lifecycle-transition`** — workspace lifecycle phase change (boot, shutdown, persist, resume, per D7 §4). Payload shape: transition-type + trigger.

### Subtype machinery: hybrid (open via registration)

Extensions (shapes, specialists, adapters) **may register additional payload subtypes** via the extension protocol (layer 3). Per-subtype payload-shape is validated by whoever declared it:
- Framework-core validates the five core subtypes' payload shapes.
- Extension-declared subtypes are validated by the extension that declared them.

This keeps framework-core small while permitting domain-specific event vocabularies (e.g., a hypothetical practitioner-shape might add `attestation-revoked`; an adapter might add `external-event-received`).

### Concrete example

Per the discussion that produced this decision: a Monday-in-PBS-Schulz worked example showed a single chain across `lifecycle-transition` (boot) → `state-change` (scope set) → `action` (file read) → `claim` (B-Plan citation) → `composition-change` (adapter added) → `action` (email sent) → `lifecycle-transition` (shutdown). All linked via `prev-event`; multi-actor events with role-tags appeared on `claim` and `action` (send-email).

### What is NOT in the event kind contract

- **Role-tag vocabulary** (`drafter`, `attester`, `reviewer`, etc.) — shape policy.
- **Specific payload shape for non-core subtypes** — extension-declared.
- **Integrity-mechanism specifics** (hash algorithm, signing scheme, storage backend) — implementation choice / layer 3.
- **Per-event-kind chains** (per-actor chain, per-work-unit chain) — derived by query, not stored.
- **Cross-workspace event linkage** — out of scope; workspace-scoped chain.

**Rationale**: events are the substrate I3 demands ("nothing escapes attribution"). Single-chain ordering supports linear audit reconstruction (per I3); machine-checkable contract slots support I2; hybrid subtype machinery supports I1 (extensions can compose new event vocabularies without modifying core).

---

## D11 — 2026-05-08 — Layering clarification: formal schema is layer 3, format is implementation

**Decision**: The mental model of framework levels is sharpened to distinguish three things that earlier entries (D7, D9, D10) referred to loosely as "schema":

| Level | Content |
|---|---|
| **Layer 1** (identity) | What the framework IS, structurally (D5). |
| **Layer 2** (kinds) | **Semantic contracts**: slot lists, cardinalities, relationships, invariants. What we're producing now (D7, D9, D10, ongoing kinds). |
| **Layer 3** (extension protocol) | **Formal schemas** for each kind (concrete enough to validate, format-neutral) + extension declaration mechanism + conformance validation + composition rules + promotion / demotion rules. |
| **(Below layer 3) Implementation** | **Format / serialization choices** (JSON / YAML / Pydantic / Protobuf / etc.), **storage / wire / protocol** (files, DB, streams, etc.), specific extension impls. |

**The bridging element**: an extension impl cannot be written from layer 2 alone. It needs **layer 3's formal schemas** to know what conformance looks like. Layer 2 says "events form an ordered chain"; layer 3 says "id is a non-empty UTF-8 string ≤ 256 chars; prev-event is a nullable string reference matching `^evt-[a-zA-Z0-9-]+$`; timestamp is ISO-8601 UTC"; implementation says "encoded as JSON in append-only file."

**Format and serialization choices remain implementation-level** (below layer 3); they are not framework-core decisions. Multiple impls may serialize differently and still conform, as long as each impl's serialization round-trips through the formal schema.

**Where prior entries used "schema" loosely**: D7 ("Concrete schema of the manifest (Pydantic, markdown, both, other) — implementation choice; layer-3 territory"), D9 (similar wording), D10 (similar wording). The intended meaning was **formal schema = layer 3**; **format / serialization = implementation**. The prior entries' "schema" referred to formal schemas (correctly placed at layer 3); examples like "Pydantic, markdown" are serialization choices (implementation).

**Rationale**: without this distinction, "implementation choice; layer-3 territory" was ambiguous. Locking the distinction prevents drift in subsequent kind definitions and makes clear what each layer must produce before impl work can begin.

**Procedural implication**: layer 2 enumeration can finish (per D6 closure) before layer 3 begins; but **layer 3 is non-optional** for any impl work to follow. It is a later phase of framework-core work, not an afterthought or implementation concern.

---

## D12 — 2026-05-08 — Substrate kind

**Decision**: The substrate kind contract specifies what hosts the agent loop and exposes interfaces (capabilities) for other extensions to hook into. A workspace's manifest declares substrate-bindings (per D7) that resolve to substrate impls conforming to this contract.

### Contract slots

- **`id`** — stable identifier for this substrate (e.g., `claude-agent-sdk`).
- **`version`** — version designator (range-comparable for binding resolution; semver-shaped at layer-3 formal schema).
- **`capabilities[]`** — what interfaces the substrate exposes for other extensions to hook into. Hybrid vocabulary: framework-core declares a core set; extensions may register additional capabilities.
- **`runtime-shapes[]`** — which interaction modes the substrate supports: `interactive`, `programmatic`, `hosted-interactive`, `hosted-programmatic`. Open vocabulary; extensions may register additional shapes. A substrate may declare multiple shapes; each binding selects exactly one.

### Core capability vocabulary (framework-declared)

Framework-core declares only capabilities that *core kinds* depend on:

- **`mcp-client`** — substrate can be an MCP client (required by adapter kind for adapters that speak MCP).
- **`hooks`** — substrate exposes hook points for shape policies / discipline enforcement (required by shape kind for shapes that need pre/post-event policy hooks).
- **`skills`** — substrate can load specialist bundles as skills (required by specialist kind).
- **`event-streaming`** — substrate emits events the workspace state can capture (required by event kind per D10).
- **`a2a`** — substrate can speak A2A protocol (required by adapter kind for agent-to-agent adapters).

Other capabilities (`computer-use`, `cross-app-workflows`, `audit-via-purview`, `opentelemetry`, `parallel-tool-calls`, etc.) are extension-registered, not framework-required. The principle: framework-core declares a capability iff a core kind depends on it.

### Single kind; no subtypes

Substrate is a single kind. Variations sometimes imagined as subtypes (interactive vs programmatic vs hosted) are captured in `runtime-shapes[]` rather than kind subtypes — this avoids forced parallel hierarchies for what are really declarative facets.

### Binding resolution

A workspace's substrate-binding (per D7 §4 cardinality) may reference a substrate by:
- **specific identity**: `id` + `version-range` (e.g., `claude-agent-sdk @ ">=2.0"`)
- **capability requirements**: a list of required capabilities; runtime resolves any conforming substrate
- **mixed**: capability requirements + preferred substrate

Each binding selects exactly one runtime-shape. Multiple bindings of the same substrate (different runtime-shapes) are allowed — e.g., a workspace with `bind-primary: claude-agent-sdk@interactive` for daily work and `bind-scheduled: claude-agent-sdk@programmatic` for cron tasks.

### Capabilities as interfaces (boot semantics)

A substrate's capabilities are **interfaces other extensions hook into**, not just feature flags. When a workspace boots:

1. Host process loads the substrate (per the binding's id + version + runtime-shape).
2. Substrate provides runtime + exposes its declared capabilities as interfaces.
3. Workspace registers adapters into the substrate's `mcp-client` capability; specialists into `skills`; shape policies into `hooks`; events flow through `event-streaming` into the workspace event chain (per D10).
4. Agent loop runs; everything operates via substrate's exposed interfaces.

A substrate that lacks a capability required by another bound extension cannot host that composition. The framework validates this structurally per I2 at boot.

### D9 refinement (implicit but worth noting)

Per D9, an `agent-actor` declares `substrate-binding`. With a workspace possibly having multiple bindings of the same or different substrates, that reference resolves to a **specific binding-id within workspace.composition**, not just a substrate-id. This refinement is consistent with D9's wording; it just makes the resolution target precise.

### Concrete example (illustrative only; not part of core)

Three substrates with different capabilities and runtime-shapes — Claude Agent SDK supporting `[interactive, programmatic]`, Claude Cowork supporting `[hosted-interactive]`, MS Agent Framework supporting `[programmatic, hosted]` — and a workspace binding the same SDK twice with different runtime-shapes (interactive for daily work; programmatic for scheduled tasks). Worked through in discussion that produced this decision.

### What is NOT in the substrate kind contract

- Specific tool implementations → adapter kind.
- Specific skills / specialists loaded → specialist kind.
- Authentication configuration → implementation.
- Deployment / hosting target → implementation.
- Singletonness → a substrate may have multiple bindings within one workspace.
- **Formal protocol semantics** for each capability (e.g., the precise interface shape of `hooks`) → layer 3 / formal schema. At layer 2, we declare *that* the capability exists; layer 3 specifies its formal interface.

**Rationale**: substrate is the kind that hosts the agent loop and provides the runtime interfaces other extensions hook into. Per I1 (composition), the framework needs a defined kind for "where compositions execute"; per I2 (machine-checkable contracts), capability declarations let core validate that a substrate can host a given workspace's other bindings; per I3 (accountability), `event-streaming` connects substrate-level happenings to the workspace's event chain.

---

## D13 — 2026-05-08 — Shape kind

**Decision**: The shape kind is the carrier of substantive identity (per D4) — policy bundles that give a workspace its disciplines, authority semantics, and role vocabulary. Per D7, exactly 1 shape per workspace.

### Contract slots

- **`id`** — stable identifier (e.g., `practitioner-shape`).
- **`version`** — version designator (range-comparable; semver-shaped at layer-3 formal schema).
- **`extends`** *(optional)* — reference to a parent shape with version range. When present, the parent's slots are inherited; the child shape adds / specializes. Inheritance conflict resolution rules → layer-3 formal schema.
- **`actor-requirements`** *(required slot, explicit `none` admissible)* — workspace-level cardinality constraints per actor-subtype that aren't expressible in authority-bindings (e.g., single-practitioner constraint; supervisor presence not appearing in any binding). When present as concrete requirements, framework validates eagerly at boot + at composition mutation. When `none`, no eager cardinality check; framework relies on per-event validation via authority-bindings.
- **`required-capabilities[]`** — substrate capabilities the shape needs (non-empty list; a shape that needs no capabilities cannot meaningfully impose policy).
- **`optional-capabilities[]`** — substrate capabilities the shape uses if present (may be empty list).
- **`authority-bindings[]`** — list of `(payload-subtype, qualifier?, required-role, required-actor-subtype, additional-constraints?)` tuples. Empty list (`[]`) is admissible (shape with no per-event authority requirements); the author still must declare the slot, signaling the question was considered.
- **`roles[]`** — role-tag vocabulary the shape introduces. Used by events (per D10) to tag actor participation. Empty list admissible.
- **`hooks[]`** — semantic declarations of policy hook points (`name`, `purpose`, optional `applies-to` qualifier). Formal hook interface = layer 3. Empty list admissible. Hook callable code = implementation.

### Required-with-explicit-none / required-with-empty-list pattern

Several slots above (`actor-requirements`, `authority-bindings`, `roles`, `hooks`) are **mandatory** even when their content is empty — to force shape authors to consider whether they need the slot rather than silently omit. `actor-requirements` admits an explicit `none` sentinel because it is not list-shaped; the others admit `[]` (empty list). In both cases, the explicit-empty form is a deliberate "considered and chose none" declaration, structurally distinct from omission.

### What this lets the shape kind do

- **Carry substantive identity** (per D4) without forcing axes / specific disciplines into framework-core.
- **Be machine-validatable** (per I2): authority-bindings + capability requirements + actor-requirements all let core check at boot whether a workspace + bound extensions satisfy the shape's contract.
- **Compose via extension** (`extends`): regulated-practitioner-shape extends practitioner-shape; autonomous-business-shape stands alone; hybrid-shape mechanics deferred per D7.

### Concrete example (illustrative; not part of core)

Per discussion that produced this decision: a `practitioner-shape` (human-actor required; sparring + attestation hooks; claim attestation requires human-actor in role=attester) and a contrasting `autonomous-business-shape` (no human required; budget gate on financial actions). Plus a `regulated-practitioner-shape` extending the practitioner-shape with defensibility-grade claim qualifier and a regulator role.

### What is NOT in the shape kind contract

- **The "three axes"** (intertwining / sparring / authorship-preservation / defensibility / engaged-authorship) — shape-internal organizing principles, not kind-level slots. Practitioner-shape adopts them; other shapes may not. Per D4.
- **Discipline implementations** (sparring algorithm, attestation flow, gate-firing logic) — shape-impl / extension territory. The kind declares hook *names* and *purposes*; impls supply behavior.
- **Specific role semantics** (what `attester` means in practice) — shape impl / prose.
- **Hook callable code** — implementation.
- **Inheritance conflict resolution rules** — layer 3 (formal schema for `extends`).
- **Hybrid / multi-shape composition mechanics** — deferred per D7.

**Rationale**: shape carries substantive identity per D4. Its slots are structural-declarative (what kinds of policies + roles + cardinality the shape imposes); the substantive semantics (what disciplines mean, what attester actually does) are pushed to shape impls and shape prose. Per I1, shape is the composable substantive layer; per I2, shape declarations are machine-validatable so the framework can check workspace conformance to its bound shape; per I3, shape's authority-bindings + hooks define how attribution-bearing events get policy treatment without baking specific disciplines into core.

---

## D14 — 2026-05-08 — Layer 2 refinement-pass discipline

**Decision**: After layer-2 enumeration completes (per D6 step 3), a **refinement pass** sweeps all locked kind decisions before layer 2 is declared closed. The pass produces supersedes / clarification entries for any kinds needing sharpening.

### Pass criteria

For each locked kind decision (D7, D9, D10, D12, D13, and remaining kinds), review against:

- **Cross-kind consistency** — slot-naming conventions, required / optional discipline, cross-reference resolution (e.g., does an actor's `substrate-binding` resolve to a substrate-id or a binding-id? D12 surfaced this; D9 should be sharpened to match).
- **Late-emerging patterns** — patterns articulated after a kind was locked, applied retroactively where applicable. Examples already surfaced:
  - D13's **required-with-explicit-empty / explicit-none** pattern (forces author to consider each slot rather than silently omit) — review earlier kinds' optional slots for retroactive fit.
  - D11's **semantic-contract vs formal-schema vs format** distinction — sharpen any prior wording that conflated them.
- **Downstream tensions** — issues surfaced when later kinds referenced earlier ones.

### Outputs

- **Supersedes entries** for substantive revisions (per ledger discipline; new entry that explicitly supersedes the prior).
- **Clarification entries** for non-semantic phrasing sharpenings.
- **Confirmed-as-locked notes** for entries that pass review unchanged.

### Procedure update to D6

D6 step 4 (closure) is split:
- **4a**: enumeration completion check (top-down + prior-list sweep done).
- **4b**: refinement pass per this discipline.
- **4c**: closure entry naming the final kind set, marking layer 2 done.

**Rationale**: each kind was decided in isolation but kinds cross-reference. Late-emerging patterns deserve uniform application. Cross-cutting consistency only becomes visible with the whole layer in view. Locking this discipline before remaining kinds prevents accumulating entries under the false assumption "we won't re-touch these"; explicitly named refinement-as-phase prevents the pass being skipped or treated as ad-hoc cleanup.

---

## D15 — 2026-05-08 — Standards-compatibility criterion for refinement pass (clarifies D14)

**Decision**: The refinement pass per D14 includes an explicit **standards-compatibility criterion**: each layer-2 kind is checked for clean mappability to relevant external standards, without distortion. The check operationalizes the principle that the framework integrates *with* the standards ecosystem rather than *baking standards into* core kinds (per D2).

### Criterion phrasing

> *Is each kind cleanly mappable to the primitives of relevant external standards? If yes, framework integrates with the ecosystem without protocol-locking core. If mapping requires forced translation or distortion, either the kind needs sharpening OR the standard isn't relevant for this kind — surface as a finding either way.*

### Standards explicitly in scope (non-exhaustive)

The pass at minimum considers:
- **MCP** (Model Context Protocol) — already integrated as substrate capability + adapter protocol; check that adapter declared-emissions / consumptions map to MCP tool-call / resource semantics.
- **A2A** (Agent-to-Agent) — already integrated as substrate capability + adapter protocol; check that `agent-actor` identity, work-unit task model, and event-message exchange map cleanly to A2A's data model.

### Standards to investigate / research during the pass (non-exhaustive)

The pass also includes a **research step** to identify additional standards worth mapping to. Candidates that may be relevant (to be evaluated, not assumed in scope):

- **W3C PROV-O / PROV** — provenance ontology; potentially highly relevant for claim attribution + audit-trail semantics (per I3).
- **W3C Verifiable Credentials** — for attestation / authority-binding signaling across systems.
- **DID (Decentralized Identifiers)** — for actor identity across systems / federation.
- **CloudEvents** — standard event format; potentially relevant to event-kind mapping for cross-system event interchange.
- **OpenTelemetry** — observability / audit / tracing; potentially relevant for cross-substrate observability (Microsoft Agent Framework uses it natively).
- **OpenAPI** — for adapters that wrap REST/HTTP APIs (especially MCP-server-fronted ones).
- **AsyncAPI** — for event-driven adapters.
- **JSON Schema** — for the layer-3 formal schema notation itself.
- **Activity Streams** — standardized activity/event vocabulary.
- **EU AI Act compliance schemas** — emerging; relevant for accountability-bearing deployments per I3.

This list is **a starting point for research**, not a list of confirmed-in-scope standards. The pass produces findings: for each candidate standard, decide *in scope (kinds should map cleanly) / out of scope (not relevant for our kinds) / open (needs deeper investigation)*.

### Outputs of the standards-compatibility check

- For each kind: **mapping notes** to in-scope standards (e.g., "agent-actor.id maps to A2A agent-identity; agent-actor.substrate-binding doesn't map directly — surfaces only at A2A adapter layer").
- For each candidate standard: **scope decision** (in / out / open with research follow-up).
- **Supersedes / clarification entries** for any kind that requires sharpening to enable clean mapping to in-scope standards.

**Rationale**: standards-compatibility is what lets the framework be substantively useful in a heterogeneous ecosystem without sacrificing core's protocol-neutrality. Naming this as an explicit pass criterion (vs. ad-hoc consideration) ensures the check actually happens. Extending beyond MCP and A2A acknowledges that the standards landscape is broader than the two standards we've already engaged — and may shift over time.

---

## D16 — 2026-05-08 — Adapter kind

**Decision**: The adapter kind specifies how a workspace integrates with external surfaces (services, peer agents, event sources, custom systems). One kind covers all integration patterns (request/response tool, delegation peer, passive event source); pattern variability is captured by `protocol-or-transport` + `declared-event-emissions[]` + `declared-event-consumptions[]`. **No specific protocol is listed at framework-core level**; all protocol identifiers are extension-registered (per the strict reading of D2 — see "Strict protocol-neutrality" below).

### Contract slots

- **`id`** — stable identifier (e.g., `email-adapter-imap`).
- **`version`** — version designator (range-comparable; semver-shaped at layer-3 formal schema).
- **`protocol-or-transport`** — single opaque identifier for the protocol the adapter speaks. Fully open vocabulary; the identifier must resolve to an extension-registered protocol (per the extension protocol at layer 3). Multi-protocol adapters express by registering multiple adapter instances (one per protocol).
- **`required-substrate-capabilities[]`** — list of substrate capability identifiers the adapter needs. Required slot; may be `[]` (e.g., direct in-process adapter that needs no substrate capability). Framework validates at boot that the workspace's bound substrate(s) collectively provide every listed capability.
- **`declared-event-emissions[]`** — list of `(payload-subtype, qualifier?)` pairs the adapter can emit into the workspace event chain. Required slot; may be `[]`. Lets shapes' authority-bindings (per D13) reason about adapter outputs at composition validation time.
- **`declared-event-consumptions[]`** — list of `(payload-subtype, qualifier?)` pairs the adapter consumes / surfaces as workspace events. Required slot; may be `[]`.

### Three integration patterns (illustrative, not part of contract)

A single kind covers radically different patterns:

- **Request/response tool** (e.g., MCP-wrapped email adapter): emits `action` events on agent-invoked operations; emits `action` events on inbound (e.g., `email-received`).
- **Delegation peer** (e.g., A2A-wrapped research-agent): emits `action` events on delegation; emits `action` events on peer responses.
- **Passive event source** (e.g., direct calendar-watcher): emits `state-change` events without agent invocation; declared-event-consumptions typically empty.

### Configuration is binding-time

Adapter configuration (URLs, credentials, polling intervals, etc.) is supplied at workspace.composition binding time and is **extension-defined per protocol** — not in the kind contract. Each protocol extension declares the config schema its adapters expect.

### Strict protocol-neutrality (per D2)

Framework-core lists **no specific protocols**. `protocol-or-transport` is open vocabulary. MCP, A2A, CloudEvents, AsyncAPI, direct-api, file-sync, webhook-handler — all are extension-registered protocol identifiers, all of equal standing at core. This solidifies D2 (kinds are abstractions; specific protocols are instances).

Solidified across multiple passes including: slippery-slope test (no principled line admits MCP/A2A while excluding HTTP, OAuth, OpenTelemetry, etc.), D15 internal-consistency analysis, abstraction-vs-instance test, future-proofing (post-MCP / post-A2A protocols get parity from day one).

### Refinement-pass findings flagged (consequences for prior entries)

This decision surfaces inconsistencies in earlier entries that the refinement pass per D14 must address:

- **D12 (substrate capabilities) — same category-collapse.** D12's core capability list mixed abstract patterns (`hooks`, `skills`, `event-streaming`) with specific-protocol-named capabilities (`mcp-client`, `a2a`). Refinement-pass action: keep abstract capabilities at core; move specific-protocol capabilities to extension-registered status. Possibly introduce abstract capabilities `external-tools` (over MCP and equivalents) and `agent-peering` (over A2A and equivalents) at core.
- **D15 internal phrasing.** D15 says "MCP is already integrated as substrate capability." Under the strict reading, this should become "MCP is registered as an extension-protocol that satisfies the abstract core capability." Refinement-pass action: sharpen wording.

### What is NOT in the adapter kind contract

- **Specific protocol semantics** (how MCP tool-calls work; how A2A handshakes; how CloudEvents emit; etc.) — extension protocol territory at layer 3.
- **Configuration schema** — extension-declared per-protocol.
- **Authentication** — implementation.
- **Specific tool / resource lists** — extension-declared per-adapter (or per-protocol).
- **Adapter lifecycle internals** (connection pooling, retry, etc.) — implementation.
- **Multi-protocol single adapters** — out of scope; register multiple adapter instances instead.

**Rationale**: per I1 (composition), adapters are how the workspace composes with external surfaces; per I2, declared emissions / consumptions / required-capabilities give framework a structural basis to validate composition at boot; per I3, declared event emissions let the workspace's event chain incorporate adapter outputs as attribution-bearing events. The strict protocol-neutrality (per D2) keeps the framework standards-friendly without standards-locked.

---

## D17 — 2026-05-08 — Supersedes D12 core capability vocabulary (strict protocol-neutrality applied)

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

---

## D18 — 2026-05-08 — Clarifies D15 wording (per strict protocol-neutrality)

**Decision**: D15's wording around how MCP and A2A "integrate" with framework-core is **clarified** to align with the strict reading articulated in D16 + D17.

### Wording clarification

D15's "Standards explicitly in scope" section should be read as:

- **MCP** — registered as an extension-protocol identifier. In substrate context, MCP-supporting impls advertise via extension-registered substrate-capability identifiers (e.g., `mcp-client`). In adapter context, adapters wrapping MCP servers declare `protocol-or-transport: mcp-server`. Refinement pass verifies clean mappability of core kinds (actor, event, work-unit, etc.) to MCP primitives.
- **A2A** — same shape: extension-protocol identifier; substrate-supporting impls advertise via extension-registered substrate capabilities; adapters wrapping A2A peers declare `protocol-or-transport: a2a-peer`. Refinement pass verifies clean mappability.

The original phrasing in D15 ("MCP is already integrated as substrate capability + adapter protocol") was loose. It should have said: *"MCP is registered as an extension-protocol whose substrate-side implementations advertise via extension-registered substrate-capability identifiers; adapter-side implementations declare it as their protocol-or-transport."*

### Why this is a clarification, not a substantive supersede

D15's substantive content is unchanged:
- The standards-compatibility criterion still applies.
- The "research candidates" list still applies (PROV-O, VC, DID, CloudEvents, OpenTelemetry, OpenAPI, AsyncAPI, JSON Schema, Activity Streams, EU AI Act schemas).
- The operational pass procedure (per-kind mapping notes; per-standard scope decisions; supersedes/clarification outputs) still applies.

Only the phrasing about *how* MCP and A2A relate to core is sharpened.

### Refinement-pass status update

The D15-finding flagged in D16 is now addressed by this entry. With D17 + D18 together, the D16-flagged refinement-pass items are all resolved (per option C — rolling refinement of clear-now findings; named pass at closure still handles cross-cutting and late-emerging findings).

**Rationale**: keeping the ledger internally consistent during ongoing work — D15 should not be referenced or built upon while it carries phrasing that contradicts the strict reading just locked.

---

## D19 — 2026-05-08 — Specialist kind

**Decision**: The specialist kind specifies a packaged role/skill bundle loaded into a workspace. Specialists declare what they do (skills) and where they fit (supported work-unit-kinds); their content is loaded into the substrate's `skills` capability per D17.

### Contract slots

- **`id`** — stable identifier (e.g., `planning-document-work`).
- **`version`** — version designator (range-comparable; semver-shaped at layer-3 formal schema).
- **`roles[]`** — required-with-explicit-empty: shape-role-tags this specialist operates in (per D13's role vocabulary).
- **`skills[]`** — required-with-explicit-empty: operations the specialist provides. Semantic declarations only; formal interface and content (SKILL.md or equivalent) = layer 3 / specialist-impl.
- **`supported-work-unit-kinds[]`** — required-with-explicit-empty: which work-unit-kinds this specialist is appropriate for.
- **`required-adapter-bindings[]`** — required-with-explicit-empty: adapter kinds the specialist needs bound in the workspace.
- **`required-substrate-capabilities[]`** — required-with-explicit-empty: typically just `skills`; possibly more (e.g., `event-streaming` if specialist subscribes to events).
- **`declared-event-emissions[]`** — required-with-explicit-empty: events the specialist produces (parallel to adapter D16).
- **`declared-event-subscriptions[]`** — required-with-explicit-empty: events the specialist reacts to (parallel to adapter's `consumptions`, but specialist-flavored — specialists react via skill invocation; adapters react via external interaction).
- **`activation-scope`** *(optional)* — when present, declares scope conditions under which the specialist is active (e.g., "scope.domain matches X"). When absent, specialist is always-active when bound. Detail = layer-3 formal schema.

### Skills vs supported-work-unit-kinds (clarification)

These are **orthogonal** declarations:
- `skills[]` = what the specialist does (verbs / operations).
- `supported-work-unit-kinds[]` = where the specialist fits (work-types / nouns).

Many-to-many at the domain level: one skill may serve multiple work-unit-kinds; one work-unit-kind may use multiple skills from a specialist. Framework does **not** cross-validate the two — that's a domain concern. Framework uses `skills` for substrate-level loading; uses `supported-work-unit-kinds` for routing + validation (workspace expecting work of kind X must have at least one specialist supporting X).

### Cross-specialist coordination

**Event-driven** (preferred at framework level): specialists subscribe to other specialists' / adapters' / shape's emissions and react via their skills. RPC-style direct invocation between specialists is implementation-shape — specialists CAN reference each other, but the framework doesn't validate or guarantee the semantics.

### Sub-agent relationship

Sub-agents are not a separate kind. A sub-agent spawned by a specialist's skill is an `agent-actor` (per D9) registered via a `composition-change` event (per D10). The specialist provides the skill that triggers spawn; the framework tracks the sub-agent as an actor; cross-process / cross-vendor sub-agents flow via A2A peer adapters (per D16).

### Concrete example (illustrative; not part of core)

`planning-document-work` specialist with roles `[drafter, reviewer]`, skills `[draft-section, review-section, cite-regulation]`, supported-work-unit-kinds `[b-plan-section, b-plan-festsetzung, umweltbericht-section]`, required-adapter-bindings `[bauleitplanung-corpus, latex-compile]`, required-substrate-capabilities `[skills]`. Worked through in discussion that produced this decision.

### What is NOT in the specialist kind contract

- **Specific skill semantics / content** (SKILL.md bodies; what `draft-section` actually does) — extension-content / specialist-impl.
- **Per-skill adapter mapping** (which skill uses which adapter) — specialist-internal documentation.
- **RPC-style cross-specialist invocation semantics** — implementation; not framework-validated.
- **Specialist runtime lifecycle internals** (initialization, hot-reload, etc.) — implementation.
- **Sub-agent spawn mechanics** — substrate concern; framework only sees the resulting actor + events.

**Rationale**: per I1, specialist is a composable internal capability bundle (paralleling adapter as composable external interface); per I2, declared slots give framework structural basis to validate workspace composition (does any specialist support work-unit-kind X? are required adapters bound? are required substrate capabilities provided?); per I3, declared event emissions / subscriptions let specialist's contributions integrate into the workspace event chain with proper attribution.

---

## D20 — 2026-05-08 — Work-unit kind

**Decision**: The work-unit kind specifies a unit of organized work tracked in workspace state per D7. Work-unit is an *instance* concept (specific work being / having been done), distinct from specialist (capability template). One kind covers all work-unit instances; the variation lives in `kind` (work-unit-kind discriminator, extension-registered like event payload-subtypes).

### Contract slots

- **`id`** — unique within workspace.
- **`kind`** — work-unit-kind identifier (extension-registered; open vocabulary; per the layer-3 extension protocol). Examples: `b-plan-section`, `invoicing-cycle`, `correspondence-thread`.
- **`status`** — lifecycle phase. Fixed core enum (see below).
- **`payload`** — kind-specific content (validated by the work-unit-kind extension declaration; framework doesn't validate payload shape at core).
- **`contributing-actors[]`** — required-with-explicit-empty: actors operating on this work-unit, with role-tags per D9 + D13.
- **`contributing-specialists[]`** — required-with-explicit-empty: specialists operating on this work-unit (each must have this work-unit's `kind` in its `supported-work-unit-kinds`).
- **`lifecycle`** — timestamp markers: `created-at`, `started-at`, `completed-at`. Richer lifecycle history derivable from events filtered by this work-unit's id.

### Core lifecycle status enum (fixed at framework-core)

- **`created`** — work-unit declared; not yet started.
- **`in-progress`** — actively being worked on.
- **`paused`** — work suspended; can resume.
- **`completed`** — work finished successfully.
- **`abandoned`** — work terminated without completion.

Five states. Fixed at core; extensions cannot add lifecycle states. Specific shape / specialist concerns (review flows, attestation, approval gates) are modeled as **events** within `in-progress`, not as separate states. Forces consistent lifecycle vocabulary across work-unit-kinds + makes status transitions structurally predictable.

### Work-unit-id and event chain

Per D10, the workspace has a single ordered event chain. Work-unit-events are a **derived view** by filtering events that reference the work-unit's id. This requires events to carry a work-unit-id reference where applicable.

**Refinement-pass finding for D10**: events should have a `work-unit-id` slot (optional; null when event is not associated with any work-unit; non-null otherwise). This makes per-work-unit views queryable without payload-rummaging. Queued for the named refinement pass per D14.

### Concrete example (illustrative; not part of core)

`wu-b-plan-3.2-hennigsdorf-2024` of kind `b-plan-section`, status `in-progress`, payload `{section-number: "3.2", project-id: "hennigsdorf-2024"}`, contributing-actors `[claude-primary as drafter, gunther-schulz as practitioner]`, contributing-specialists `[planning-document-work]`. Worked through in discussion that produced this decision.

### What is NOT in the work-unit kind contract

- **Work-unit-kind payload schemas** — extension-declared per kind (the `b-plan-section` extension declares what `payload` shape its instances have).
- **Lifecycle transition rules** (when can `in-progress` → `completed`?) — shape / specialist concern; framework checks allowed transitions but not the conditions for them.
- **Containment hierarchy** (work-units containing sub-work-units) — out of scope for now; would need its own decision if surfaced.
- **Work-unit-state mutation semantics** (atomic vs eventual) — implementation.
- **Cross-workspace work-unit federation** — out of scope.

**Rationale**: per I1, work-unit is the instance-shaped composable concept that the workspace tracks (paralleling specialist as the template-shaped composable concept); per I2, fixed core lifecycle states + structural slots give framework a basis to validate work-unit transitions and references; per I3, work-unit's events (via the work-unit-id slot on events, refinement pending) form the attribution-bearing record of how work proceeded.

---

## D21 — 2026-05-08 — Workspace-as-A2A-peer deployability requirement

**Decision**: A deployed workspace must be exposable as an A2A peer when the deployment chooses A2A exposure. This is a load-bearing requirement on the framework's extensibility — framework-core kinds must support this composition pattern, even though the A2A protocol itself is extension territory (per D2 + D17).

### What this requires from framework-core

- Specialist `skills[]` declarations (per D19) carry enough metadata to map to A2A agent-card skill entries (name, description, input / output modalities). Verified at refinement pass via D15's standards-compatibility check.
- Workspace lifecycle (per D7 §4) supports A2A-peer-endpoint serving: boot binds the A2A peer adapter; adapter publishes agent-card; shutdown unpublishes.
- Shape authority-bindings (per D13) compose coherently with A2A peer authentication / authorization.
- Cross-process attribution flows through `agent-actor` (peer agents registered as actors per D9) + event chain (per D10), with peer interactions captured as events.

### What this requires from extensions

- **A2A peer adapter** (an instance of the adapter kind per D16): aggregates skills from loaded specialists into an agent-card; serves the agent-card at the well-known URL (e.g., `/.well-known/agent.json`); routes incoming A2A task requests to appropriate specialist skill invocations; translates results into A2A task responses.
- **A2A protocol extension** (extension-registered protocol identifier `a2a-peer`): defines the formal mapping between framework-core primitives (specialist skills, work-units, events, actors) and A2A protocol primitives (agent-card skills, tasks, messages, agents).
- **Per-skill exposure control**: specialist skills may need a publicly-exposed flag (or an explicit publish-list at adapter binding time) so internal-only skills don't leak into the agent-card. Specific mechanism = layer-3 formal schema; named here as a requirement.

### Generalization beyond A2A (MCP-server exposure parallel)

The parallel pattern for MCP — *workspace-as-MCP-server* (specialist skills exposed as MCP tools to external AI clients) — is similarly supported by the framework's extension architecture but is separate from this entry's scope. The refinement pass per D15 should verify the MCP-server-exposure mapping with the same rigor as A2A-peer mapping.

Both expose-patterns share the underlying requirement: *the workspace's specialists' skills are externally addressable via standards-conformant protocols*. The framework must enable this without baking either standard into core.

### Verification target for refinement pass (per D14 + D15)

The pass verifies:
- Specialist's skill declaration metadata is sufficient for clean agent-card mapping (no information loss).
- Workspace boot / shutdown lifecycle correctly binds / unbinds the A2A peer adapter.
- A2A peer auth integrates coherently with shape authority-bindings.
- Per-skill exposure control mechanism is well-defined.
- Cross-process actor attribution (peer agents in this workspace's actor registry) flows correctly.

### Why this matters (load-bearing rationale)

- **Cross-vendor interop**: PBS workspaces accessible to peer agents on Cowork, MS Agent Framework, Google ADK, LangGraph, CrewAI, LlamaIndex, Semantic Kernel, AutoGen — the universal A2A-adopting ecosystem in 2026.
- **Federation pathway**: workspaces can collaborate as peers without bespoke protocols. Multi-workspace federation (deferred per D7 + D9) gets a standards-based foundation.
- **Regulatory alignment**: A2A is converging with EU AI Act / governance frameworks for cross-vendor agent identity + collaboration audit (per D15 candidates including PROV-O, DID, VC).

### Caveat

The requirement applies to deployments that *choose* A2A exposure. Not every workspace must be A2A-exposed; this is deployment policy. The requirement is that the framework's design **supports it cleanly when chosen** — the framework neither forces A2A on every deployment nor makes A2A exposure a second-class extension.

**Rationale**: per D15's standards-compatibility criterion, specific compatibility targets need to be load-bearing requirements (not just verified at refinement). A2A-peer exposure is the most directly load-bearing because it's how a workspace participates in the cross-vendor agent ecosystem. Naming it as a requirement makes it a design constraint that informs the refinement pass + the layer-3 formal-schema work for specialist + workspace + adapter kinds.

---

## D22 — 2026-05-08 — Refinement: D9 substrate-binding resolution clarified

**Decision (clarifies D9)**: An `agent-actor`'s `substrate-binding` slot resolves to a **binding-id within `workspace.composition.substrate-bindings[]`**, not to a bare `substrate-id`. This makes the reference precise when a workspace has multiple bindings of the same substrate-id (e.g., one binding in `interactive` runtime-shape for daily work + another in `programmatic` runtime-shape for cron tasks — concrete example from D12 discussion).

**Why this is a clarification, not a substantive supersede**: D9's intent was "agent-actor identifies which substrate runtime hosts its execution"; the wording "references a substrate declared in workspace.composition" was loose because workspace.composition can have multiple bindings to the same substrate. The refinement makes the reference precise. Semantics unchanged; phrasing sharpened.

**Cross-references**: D7 §4 substrate-binding cardinality (multiple bindings allowed); D12 binding-resolution discussion.

---

## D23 — 2026-05-08 — Refinement: D10 events gain `work-unit-id` slot (supersedes D10 slot list)

**Decision (supersedes D10's contract slots)**: The event kind contract (D10) gains an optional **`work-unit-id`** slot:

- **`work-unit-id`** *(optional)* — references the work-unit (per D20) the event is associated with, when applicable. `null` when the event is not work-unit-associated (e.g., workspace-level lifecycle events, composition-changes that don't belong to a specific work-unit).

**Revised D10 slot list** (full, with the addition):

- `id` — unique within workspace
- `prev-event` — reference to prior event in chain (`null` only for first ever)
- `timestamp` — when the event happened
- `actors[]` — at least one actor reference; each entry `{ id, role? }`
- `payload-subtype` — registered subtype identifier
- `payload` — subtype-specific structure
- **`work-unit-id`** *(optional)* — work-unit reference, when applicable

**Rationale**: per D10's single-chain principle, work-unit-events are a derived view by filtering. Filtering needs a structural slot, not payload-rummaging — payload-rummaging is brittle and breaks the kind contract's machine-checkability per I2. Making `work-unit-id` first-class enables clean per-work-unit views (per D20's lifecycle-history-derivable-from-events claim).

**Substantive impact**: this adds a slot to D10's contract, so it's a supersedes-class change. Implementations / formal schema / serialization adjust accordingly.

**Cross-references**: D20 work-unit kind; D7 §3 state contents.

---

## D24 — 2026-05-08 — Refinement-pass output: cross-kind consistency + 4a flags + standards-compatibility findings

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

---

## D25 — 2026-05-08 — Layer 2 closure (final kind set; layer 2 complete)

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

---

## D26 — 2026-05-08 — Indicative roadmap for post-layer-2 phases

**Decision**: An indicative roadmap is locked for phases beyond layer-2 closure (D25). Phases are named at high level **without committing to schedule, scope detail, or rigid sequencing**. The roadmap exists for session-continuity (so a fresh session knows the trajectory) and to give deferred items implicit homes. The roadmap can be superseded as work progresses; this entry is informational + structural, not a binding plan.

### Phases

**Phase A — Layer 3 (extension protocol + formal schemas)**
- Formal schemas per kind (concrete enough to validate, format-neutral; per D11).
- Extension declaration mechanism (how an extension registers itself; how core validates conformance).
- Composition rules (cross-kind composition, conflict resolution, precedence).
- Promotion / demotion rules.
- JSON Schema toolchain decision (per D24 — JSON Schema is in-scope as the canonical formal-schema notation candidate).
- *Closure trigger*: layer-3 closure entry analogous to D25, after layer-3 refinement pass.

**Phase B — Reference impl of core**
- Substrate impl (likely Claude Agent SDK).
- A **generic / minimal shape impl** — explicitly *not* the practitioner-shape, to avoid pioneer-instance bias. Goal is to validate the layered design works across shapes, not just for the one we want to use.
- Minimal adapters (one MCP-server-protocol adapter, one direct-api adapter).
- Minimal specialist.
- Minimal RAG-via-MCP impl to validate the adapter pattern works for retrieval-shaped extensions.
- *Closure trigger*: reference impl boots and runs a minimal scenario through all 8 kinds end-to-end.

**Phase C — Standards-compat impl**
- A2A peer adapter (validates D21).
- MCP server adapter (validates D21 generalization — workspace-as-MCP-server).
- Per-standard mapping notes from D24 resolved into impl conventions where applicable.
- *Closure trigger*: A2A peer + MCP server demonstrably work in the reference workspace; at least one external peer interaction succeeds.

**Phase D — Pioneer-instance impl (PBS-Schulz)**
- Practitioner-shape impl (the substantive shape carrying the prior VISION's axes per D4).
- PBS-Schulz domain-specific specialists (planning-document-work, invoicing, correspondence, etc.).
- PBS-Schulz-specific adapters (bauleitplanung-corpus / RAG with real BauGB / BNatSchG / regional / leitfäden / urteile / beispiele content; LaTeX compile; client-management; etc.).
- Workspace manifest for PBS-Schulz (per D5 + D7) — id, shape, substrate-bindings, adapter-bindings, specialists, actors.
- **Resolves D1's open tension**: rule for "what runs PBS-Schulz daily during the rebuild" (coexistence with the existing 0.1.0 plugin during cutover).
- *Closure trigger*: PBS-Schulz running on the framework end-to-end; Gunther's daily work substantively uses the framework rather than the prior 0.1.0 plugin.

**Phase E — Multi-deployment validation**
- Second shape impl (autonomous-business-shape, personal-OS-shape, or another) to validate genuine shape-neutrality (per VISION's claim, treated as input).
- Corresponding second workspace deployment.
- Federation work (multi-workspace) begins — the deferred federation question (D7 + D9) gets concrete.
- *Closure trigger*: two distinct deployments coexist; framework's shape-neutrality empirically validated.

**Phase F+ — Refinement, optimization, ecosystem extensions**
- Indefinite. Driven by accumulated findings, deployment evidence, ecosystem developments.

### Deferred items mapped to phases

| Deferred item | Expected phase |
|---|---|
| Optional `parent-actor` slot on actor (D9) | Phase A or B (when sub-agent patterns are concretely exercised) |
| Workflow as containment hierarchy on work-unit | Phase D (if pioneer-instance forces) or Phase E (if multi-deployment forces) |
| PBS-Schulz daily-during-rebuild rule (D1 open tension) | Phase D |
| Branch / commit strategy | After fresh-plan stabilizes — likely during Phase A |
| D21 verification targets (A2A peer + MCP server) | Phase C |
| Standards-compatibility per-kind mapping (D24) | Phase A for layer-3-affecting standards; Phase B/C for impl-level; Phase D for deployment-specific |

### Caveats

- **Order is indicative, not rigid.** Phase B could start before Phase A closes if specific layer-3 questions can only be resolved by impl exercise. Phase D could parallel Phase C if deployment-specific work is independent of standards-compat.
- **Each phase has its own internal sub-phases.** Layer 3 (Phase A) in particular will be its own multi-week sequence with its own internal structure (kinds-by-kinds formal schemas mirroring how layer 2 was done).
- **Phase boundaries are trigger-based, not schedule-based.** Phases close when their criteria are met, not on a calendar.
- **The roadmap is supersede-able.** As work progresses, this entry can be revised.

**Rationale**: D25 named layer 3 + impl as next-phase but provided no roadmap beyond. A fresh session opening the ledger after layer-2 closure had zero visibility into trajectory. Indicative roadmap with phase names + triggers + deferred-item placement + caveats gives session continuity without premature commitment to specifics.

---

## D27 — 2026-05-09 — Phase A enumeration approach

**Decision**: Phase A (layer 3) is enumerated in five workstreams, in this order:

1. **Notation** — formal-schema toolchain choice.
2. **Extension mechanism** — how extensions declare themselves; how core validates conformance.
3. **Per-kind formal schemas** — the 8 kinds (D25), locked one-by-one.
4. **Composition rules** — cross-kind composition, conflict resolution, precedence.
5. **Promotion / demotion rules** — how things move between layers / extension ↔ core.

Each substantive decision = one ledger entry locked at the time of agreement (per D6 incremental discipline). After the five workstreams complete, a refinement pass per D14 sweeps the locked entries; a closure entry analog of D25 marks Phase A done.

**Rationale**: outside-in ordering. Notation comes first because the rest is written in it. Extension mechanism comes before per-kind schemas because every kind has extension-registered open vocabulary (event payload-subtypes, work-unit-kinds, protocol identifiers, capability identifiers) — schemas can't be precise without it. Composition + promotion build on top of locked schemas.

**Order is indicative, not rigid** (per D26 caveat): if a per-kind schema forces revisiting the extension mechanism, we revisit; if composition rules surface a schema gap, we sharpen. Strict sequence enforcement is not the point — the ordering is the default path.

**Procedural**: same disciplines as layer 2 — append-only, one question at a time, concrete examples before locking, rolling refinement (option C) for clear-now findings, named refinement pass at the end for cross-cutting findings.

---

## D28 — 2026-05-09 — Formal-schema notation: JSON Schema (Draft 2020-12)

**Decision**: Layer-3 formal schemas for the 8 kinds (D25) are written in **JSON Schema, Draft 2020-12**. This confirms D24's "in scope (layer-3 toolchain)" finding for JSON Schema.

**Rationale**:

- **Format-neutral per D11**: JSON Schema constrains structure, not wire format. Implementations may serialize instances as JSON, YAML, TOML, msgpack, etc. — all round-trip through the same schema.
- **Tooling maturity**: validators exist in every major language (ajv, jsonschema, opis/json-schema, etc.). No bootstrap problem.
- **Reference + composition**: `$ref`, `allOf`/`oneOf`/`anyOf`, `if/then/else`, `discriminator` (via OpenAPI extension) cover everything the kind contracts need (e.g., conditional metadata by `actor.subtype` per D9; `payload-subtype`-discriminated payloads per D10).
- **Draft 2020-12** is the latest stable; supersedes earlier drafts; broad validator support.

### What JSON Schema covers (sufficient)

- Per-kind structural validation: slot lists, required/optional, types, enums, cardinalities, format constraints (regex, ISO-8601 timestamps, etc.).
- Open-vocabulary slots (e.g., `payload-subtype`, `protocol-or-transport`, `kind`) modeled as strings with extension-registered values; the registry mechanism is layer-3 workstream 2 territory, not the schema itself.

### What JSON Schema does NOT cover (deferred to other layer-3 work)

- **Cross-kind referential integrity** — e.g., event's `actors[].id` must exist in workspace.actors[]; specialist's `supported-work-unit-kinds[]` must match an extension-registered work-unit-kind. Out of scope for JSON Schema; handled by the framework conformance validator (a layer above the schemas that applies cross-kind invariants). The schemas specify what conformance is *within* each kind; the validator specifies what conformance is *between* kinds.
- **Runtime invariants** — e.g., event-chain `prev-event` ordering, work-unit lifecycle transition validity. Schema-validates the slot's *type*; the validator-or-runtime enforces the *invariant*.

### What is NOT in this decision

- **Schema file layout / location** — deferred to per-kind workstream (workstream 3).
- **Validator implementation choice** (ajv vs jsonschema vs opis) — implementation level (below layer 3 per D11).
- **Other notations considered** — SHACL/RDF (overkill for kind contracts; may resurface in standards-mapping for PROV-O / VC / DID per D24); CUE / TypeSpec (less mature ecosystem). Not adopted; not ruled out for niche use later (e.g., a SHACL representation for PROV-O integration).
- **Schema versioning** (how schemas evolve over time) — deferred; will surface in promotion / demotion workstream (workstream 5).

**Cross-references**: D11 (formal schema = layer 3; format = implementation); D24 (JSON Schema named as in-scope toolchain candidate); D27 (workstream order).

---
