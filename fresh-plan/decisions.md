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

## D29 — 2026-05-09 — Extension manifest contract + validation flow

**Decision**: An extension is declared by a structural manifest. The manifest contract has four parts; core validates extensions at workspace.composition resolution-time.

### Manifest contract

**1. Identity**

- **`id`** — stable extension identifier.
- **`version`** — version designator (semver-shaped at layer-3 formal schema; range-comparable).
- **`extends`** *(optional)* — reference to a parent extension with version range. Inheritance conflict resolution = workstream 4.

**2. Vocabulary registrations** — list of `(slot, identifier, spec-ref)` tuples adding values to a core open-vocabulary slot.

The open-vocabulary slots in framework-core (per D7-D20):

- `event.payload-subtype` (D10)
- `work-unit.kind` (D20)
- `substrate.capabilities[]` items (D17 — beyond the three abstract core capabilities)
- `substrate.runtime-shapes[]` items (D12)
- `adapter.protocol-or-transport` (D16)
- `actor.subtype` (D9)

`spec-ref` references the value's specification (typically a JSON Schema per D28; for some slots, additionally a behavioral contract document).

Required slot; may be `[]` (per D13 required-with-explicit-empty pattern).

**3. Provisions** — list of `(kind, id, spec-ref)` tuples; actual instances of kinds the extension provides. Kinds that admit provisions: **substrate, shape, adapter, specialist**. (workspace, event, actor, work-unit are not extension-provided — workspace is per-deployment manifest; event / actor / work-unit are runtime instances.)

Each provision conforms to its kind's layer-3 formal schema (workstream 3).

Required slot; may be `[]`.

**4. Dependencies**

- **`required-core-capabilities[]`** — abstract core capabilities (`hooks`, `skills`, `event-streaming` per D17) the provisions need. Required, may be `[]`.
- **`required-extensions[]`** — list of `(extension-id, version-range)`. Required, may be `[]`. Circular-dep detection + resolution = workstream 4.

### Identifier namespacing

Identifiers registered by an extension are **implicitly namespaced by extension id**. Canonical fully-qualified form: `<extension-id>:<identifier>` (e.g., `a2a-protocol-ext:a2a-peer`).

Within an extension's own manifest, references to its own identifiers may be bare; cross-extension references must be fully-qualified. Workspace.composition references vocabulary by fully-qualified form. Two extensions registering the same bare identifier do not collide — they're distinct under qualification.

### Validation flow

Core validates at **workspace.composition resolution-time** (workspace boot, per D7 §4). No separate "install" step. The workspace's composition is the unit of trust.

1. Workspace manifest declares `composition`, referencing extensions by `(id, version-range)`.
2. Core resolves each reference to a specific extension version available locally.
3. Each resolved extension's manifest is validated against the extension formal schema (produced in workstream 3).
4. Vocabulary registrations are merged into the workspace's open-vocabulary tables (with namespacing per above).
5. Each provision is validated against its kind's formal schema.
6. Cross-kind composition checks run (workstream 4).
7. Any failure prevents workspace boot.

### Worked example: A2A protocol extension

```yaml
# Format: YAML for readability; on-disk format is implementation choice per D11.
id: a2a-protocol-ext
version: 1.0.0
extends: null

vocabulary-registrations:
  - slot: adapter.protocol-or-transport
    identifier: a2a-peer
    spec-ref: ./specs/a2a-peer-protocol.schema.json
  - slot: substrate.capabilities
    identifier: a2a
    spec-ref: ./specs/a2a-capability.schema.json

provisions:
  - kind: adapter
    id: a2a-peer-adapter-default
    spec-ref: ./adapters/a2a-peer-default.adapter.json

dependencies:
  required-core-capabilities: []
  required-extensions: []
```

A workspace using it:

```yaml
composition:
  extensions:
    - id: a2a-protocol-ext
      version: '>=1.0.0'
  adapter-bindings:
    - id: my-a2a-adapter
      provision: a2a-protocol-ext:a2a-peer-adapter-default
      protocol-or-transport: a2a-protocol-ext:a2a-peer
```

### Tensions / open questions surfaced (deferred)

- **Spec-ref resolution semantics** — within-package paths vs. URLs vs. registry references. Implementation per D11; manifest contract treats `spec-ref` as opaque-string-resolvable-by-the-loader.
- **Inheritance conflict resolution** for `extends` — child + parent register same identifier or provide same kind-id. → workstream 4.
- **Circular extension dependencies** — detection + handling. → workstream 4.
- **Mid-runtime extension reload** — workspace.composition mutability per D7 §4 covers conceptually; concrete validation flow for hot-reload = layer-3 detail / impl.
- **Extension signing / authenticity** — out of scope; impl / security concern.

### What is NOT in this decision

- The formal schema for the extension manifest itself (workstream 3 will produce).
- Discovery mechanism (how core finds available extensions) — implementation.
- File-system / packaging conventions — implementation.
- Inheritance + circular-dep + conflict resolution semantics — workstream 4.

**Rationale**: extensions connect the 8 layer-2 kinds' open vocabularies + impl-bearing kinds to the rest of the framework. Per I1, extensions compose; per I2, the manifest is machine-checkable; per I3, vocabulary registration is itself attribution-bearing (a `composition-change` event per D10).

The four-part shape reflects two distinct things extensions contribute — *vocabulary entries* (identifiers + specs) and *conforming things* (impls of kinds) — plus dependencies for composition validation. Each part is load-bearing.

**Cross-references**: D7, D10, D12, D13, D16, D17, D19, D20; D28 (notation); workstreams 3, 4, 5.

---

## D30 — 2026-05-09 — Cross-kind referential integrity (composition rules part 1)

**Decision**: The framework provides a **conformance validator** above the per-kind formal schemas that enforces cross-kind referential integrity. Five categories of checks; two timing modes; fail-fast failure semantics.

### The five check categories

**1. Resolution checks** (boot-time)

Every workspace.composition reference resolves to a loaded artifact:

- workspace.composition.shape.provision → a shape provision in some loaded extension
- workspace.composition.substrate-bindings[].provision → a substrate provision
- workspace.composition.adapter-bindings[].provision → an adapter provision
- workspace.composition.specialist-bindings[].provision → a specialist provision
- workspace.composition.extensions[] entries → extension manifests available locally

**2. Capability satisfaction** (boot-time)

Every `required-capabilities` declaration is satisfied:

- shape.required-capabilities[] → advertised by at least one of the workspace's bound substrates
- adapter.required-substrate-capabilities[] → same
- specialist.required-substrate-capabilities[] → same

For mixed substrate-bindings (D12: capability-based, specific, mixed), the validator considers the union across all bound substrates.

**3. Vocabulary resolution** (boot-time)

Every fully-qualified `<ext-id>:<id>` value referenced by a kind impl is registered by some loaded extension:

- specialist.supported-work-unit-kinds[] → extension-registered work-unit.kind values
- adapter.protocol-or-transport → extension-registered protocol identifier
- adapter.declared-event-emissions / consumptions[].payload-subtype → core or extension-registered payload-subtype
- specialist.declared-event-emissions / subscriptions[].payload-subtype → same
- shape.authority-bindings[].payload-subtype → same
- shape.authority-bindings[].required-actor-subtype → core or extension-registered actor-subtype

**4. Workspace-internal identity** (boot-time + per-event)

References within the workspace resolve to existing workspace-scoped entries:

- *Boot-time*: agent-actor.substrate-binding → existing binding-id within workspace.composition.substrate-bindings[] (per D9 + D22).
- *Per-event*: event.actors[].id → existing actor in workspace.composition.actors[]; event.work-unit-id (when non-null) → existing work-unit in workspace state; event.payload-subtype → registered (core or extension).
- *Per-work-unit*: work-unit.contributing-actors[].id → existing actor; work-unit.contributing-specialists[] → bound specialist; work-unit.kind → registered.

**5. Binding availability** (boot-time)

Specialist-level cross-binding requirements are satisfied:

- specialist.required-adapter-bindings[] → each referenced adapter has a matching entry in workspace.composition.adapter-bindings[]

### Timing modes

| Mode | Categories | Failure semantics |
|---|---|---|
| **Boot-time** | 1, 2, 3, 5, parts of 4 | Workspace cannot boot. Validator returns the structured failure list. |
| **Per-event** | parts of 4 | Event is rejected (not appended to chain). The rejection is itself recordable as a failed-attempt event by shape policy if desired (shape concern, not validator concern). |

Boot-time failures are **all-or-nothing**: the validator does not partially boot a workspace with some bindings disabled. Either all checks pass and boot proceeds, or boot fails with a complete failure report.

### Validator extension point

Extensions may register additional referential checks via the `hooks` capability (per D17). The framework declares the five core check categories; extensions may layer additional ones (e.g., a regulated-practitioner-shape extension could add "every claim event must have a defensibility-grade qualifier"). The formal hook interface for validator extension is layer-3 follow-on; this entry admits the extension point conceptually.

### Worked example: a failing boot

Consider the PBS-Schulz workspace example (`schemas/examples/workspace-pbs-schulz.json`) with a small modification: the `practitioner-shape-ext` extension is removed from `composition.extensions[]` but `composition.shape.provision` still references `practitioner-shape-ext:practitioner-shape`.

Boot proceeds through D29's validation flow:

1. Extension references resolved — `practitioner-shape-ext` is not loadable (not declared in `extensions[]`).
2. **Category 1 (resolution check) fails**: `composition.shape.provision = practitioner-shape-ext:practitioner-shape` does not resolve to a loaded extension's provision.
3. Validator returns failure: `{category: "resolution", path: "composition.shape.provision", value: "practitioner-shape-ext:practitioner-shape", reason: "extension 'practitioner-shape-ext' not in composition.extensions[]"}`.
4. Boot does not proceed.

Adding `practitioner-shape-ext` back fixes the failure; boot retries, all five categories pass, workspace runs.

### What is NOT in this decision (deferred to subsequent workstream-4 entries)

- **Composition conflict resolution** — when child + parent shape both register same role; when multiple substrate bindings could satisfy a capability requirement (precedence rules). → D31.
- **Circular extension dependencies** — detection + handling. → D32.
- **Extension load order** — derived from dependencies; affects when registrations become available. → D33.
- **Validator hook formal interface** — layer-3 follow-on.
- **Failure recovery** — partial boot, hot-reload after fix, etc. → implementation.
- **Performance characteristics** — order of checks, short-circuiting, parallelization → implementation.

**Rationale**: per I2, conformance must be machine-checkable. The per-kind schemas (workstream 3) cover within-kind structural conformance; cross-kind referential integrity needs a layer above. Per I3, attribution requires that referenced actors actually exist (so events can't fabricate actor-ids) and that work-unit references resolve (so the event chain's per-work-unit views are reconstructible). Per D29 §validation flow, the validator runs at workspace.composition resolution-time; D30 names the specific checks the validator performs.

Five-category structure follows from the schema topology: composition-level references (1), capability-requirement satisfaction (2), open-vocabulary value resolution (3), within-workspace identity (4), and cross-binding requirements (5). Each category has a distinct semantic: resolution failures mean "thing not loadable"; capability failures mean "thing loadable but its requirements unmet"; vocabulary failures mean "value not registered"; identity failures mean "internal reference dangles"; binding failures mean "specialist needs an adapter that isn't bound."

**Cross-references**: D7 (workspace composition + boot); D9 + D22 (actor.substrate-binding); D10 + D23 (event slots); D12 + D17 (substrate capabilities); D13 (shape required-capabilities, authority-bindings); D16 (adapter declarations); D19 (specialist declarations); D20 (work-unit slots); D28 (notation); D29 (validation flow + namespacing).

---

## D31 — 2026-05-09 — Supersedes D13 + D29: `extends` removed from shape and extension manifest

**Decision (supersedes the `extends` slot in D13 and D29)**: The `extends` slot is removed from both the shape kind contract (D13) and the extension manifest contract (D29). No composition / inheritance / mixin / overlay mechanism is introduced as a replacement. Shape variation patterns are deferred until concrete evidence forces a specific mechanism.

### Why this supersede

D13 introduced `extends` based on a hypothetical (regulated-practitioner-shape extending practitioner-shape); D29 introduced `extends` for extensions on parallel intent. No concrete deployment forces the slot today — we have neither a concrete second shape sharing with a first, nor an ecosystem-style variation pattern.

The cost of keeping `extends` (surfaced as workstream 4 began): conflict-resolution machinery per slot — additive vs. override vs. error rules; cascade through versioning; cognitive load of resolving extends-chains. Pure overhead until a concrete use case exists.

### Why no replacement mechanism

The mechanism shape changes; the cost remains:

- **Composition** (`composes: [...]`) — N-way conflict resolution; worse than 2-way inheritance.
- **Mixins** — same problem at finer granularity.
- **Configuration overlay** — pushes the conflict question into "what overlay slots exist."
- **Parameterization** — works for parameterizable values; doesn't address structural extension.
- **Delegation via reference** — runtime resolution semantics; same conflict question.

The mechanism that genuinely escapes the cost is **no mechanism — copy + modify when a deployment needs a variation**. Pay duplication; pay zero conflict-resolution complexity. Reversible later.

### What this changes

- **D13 (shape kind)** — the `extends` slot is removed. Shape is now standalone; no inheritance.
- **D29 (extension manifest contract)** — the `extends` slot is removed from the four-part manifest contract. Extensions are now standalone; no inheritance.
- **Workstream-3 schemas** — `shape.schema.json` and `extension-manifest.schema.json` are updated in the same commit as this entry to drop the `extends` slot (and the unused `version-range` `$def` in shape.schema.json that `extends` referenced). Worked examples updated where `extends: null` appeared (line removed).

### When to revisit

Per D14 late-emerging-pattern discipline + D26 Phase E (multi-deployment validation as evidence-gathering): when a concrete deployment surfaces a real cross-deployment variation pattern, the variation observed will tell us which mechanism (inheritance, composition, parameterization, overlay) is the right fit. Until then: nothing.

### What is NOT changed

- **D29 namespacing** — extension identifier scoping unchanged.
- **D29 vocabulary registrations + provisions + dependencies** — unchanged.
- **D13 other slots** — actor-requirements, required-capabilities, optional-capabilities, authority-bindings, roles, hooks all unchanged.
- **Workstream 4 remaining work** — multi-binding ambiguity (next entry); circular dependencies; extension load order + precedence. Inheritance conflict resolution removed from workstream 4 scope.

**Cross-references**: D4 (substantive identity = shape policy); D13 (shape kind contract; superseded on `extends`); D14 (late-emerging-pattern discipline); D26 (Phase E multi-deployment validation); D29 (extension manifest contract; superseded on `extends`); D30 (composition rules part 1).

---

## D32 — 2026-05-09 — Boot-time resolution: multi-binding, circular deps, load order (composition rules part 2)

**Decision**: Three boot-time resolution concerns settled together. The validator's behavior at workspace.composition resolution-time (per D29 + D30) is fully specified by these three principles plus D30's referential integrity checks.

### 1. Multi-binding ambiguity

When more than one binding could satisfy a requirement, the framework verifies satisfiability at boot but does not pick a specific binding for runtime use.

- **Specialist's `required-adapter-bindings[]`** — satisfied at boot if at least one workspace `adapter-bindings[]` entry references the named provision. If multiple bindings of the same provision exist, runtime / shape policy picks which one a given operation uses; framework does not specify.
- **Multiple specialists supporting the same `work-unit-kind`** — framework does not pick. Routing is shape policy or explicit at work-unit creation (work-unit.contributing-specialists[] declared per work-unit). Framework only verifies that at least one bound specialist supports the kind.
- **Shape's `required-capabilities[]` against multiple bound substrates** — already settled in D30 as union-based satisfiability (any substrate providing the capability satisfies). Restated here for completeness.

**Principle**: framework's boot-time job is *can the workspace run* (every requirement met by at least one provider); runtime concern is *which provider for this operation* (shape / runtime / impl decides).

### 2. Circular extension dependencies

Detected at boot via topological sort of the extension dependency graph.

- **Graph construction**: nodes = extensions referenced in workspace.composition.extensions[] (transitively closed via each extension's `dependencies.required-extensions[]`); edges = `A depends on B` becomes `B → A`.
- **Sort**: any standard topological-sort algorithm (Tarjan, Kahn). If sort fails, a cycle exists.
- **Failure semantics**: workspace cannot boot. Validator returns the cycle path (e.g., `A → B → C → A`). Per D30 timing modes: boot-time failure is all-or-nothing.

Algorithm specifics are implementation. The framework specifies *that* cycles are detected and *that* cycle-detection causes boot failure.

### 3. Extension load order + precedence

Once cycles are excluded, the dependency graph is a DAG. Load order is its topological order.

- **Predecessors before dependents**: if extension B depends on A, A's vocabulary registrations + provisions are available before B loads.
- **Independent extensions** (no dependency relationship, direct or transitive): framework loads them in **alphabetical order by extension id** for determinism. Avoids non-deterministic boot behavior across runs.
- **Precedence is not a question**: per D29's namespacing, two extensions cannot register the same fully-qualified identifier (`<ext-id>:<id>`). No "which registration wins" decision arises. The only ordering concern is *availability* (predecessor registrations available to dependents), which the topological order guarantees.

### Worked example: cycle detection

Workspace.composition.extensions includes `ext-a` and `ext-b`:

- `ext-a.dependencies.required-extensions[] = [{ id: "ext-b", version-range: ">=1.0.0" }]`
- `ext-b.dependencies.required-extensions[] = [{ id: "ext-a", version-range: ">=1.0.0" }]`

Boot:

1. Per D29 validation flow, extensions are resolved.
2. Per this D32 §2, dependency graph is built: edges `ext-a → ext-b → ext-a`.
3. Topological sort fails.
4. Validator returns failure: `{category: "circular-dependency", cycle: ["ext-a", "ext-b", "ext-a"]}`.
5. Boot does not proceed (per D30 all-or-nothing).

### What is NOT in this decision

- **Algorithm implementation** for cycle detection / topological sort — implementation per D11.
- **Runtime routing rules** for multi-binding cases (which adapter, which specialist) — shape policy / runtime / impl.
- **Hot-reload / partial-reload semantics** for extensions — implementation; D7 §4 composition mutability covers conceptually.
- **Extension version conflict resolution** when multiple workspace extensions transitively pull in different versions of the same dependency — surfaced here as a known gap; left to workstream 5 (promotion / demotion) or end-of-Phase-A refinement, since version-conflict resolution is interlinked with versioning policy more broadly.

**Rationale**: per I2, conformance must be machine-checkable; cycle detection + load order are mechanical. Per D29, validation runs at composition resolution-time. Multi-binding resolution settles to *satisfiability-only* at framework level because runtime routing is properly a shape / runtime concern (per D8: routing-by-context is not a framework-core kind). Alphabetical tiebreaking for independent extensions is the simplest deterministic rule; no real choice value lives here.

**Cross-references**: D8 (routing concerns are not framework-core); D11 (implementation level); D29 (validation flow + namespacing); D30 (referential integrity + boot-time failure semantics); D31 (extends removed; simpler workstream-4 scope).

---

## D33 — 2026-05-09 — Identifier graduation + versioning policy (workstream 5)

**Decision**: Two related concerns — graduation of identifiers between core and extension status, and versioning policy for framework artifacts — settled together as workstream 5.

### A. Identifier graduation (extension ↔ core)

Vocabulary values that live in framework-core's enums (capabilities per D17; payload-subtypes per D10; runtime-shapes per D12; actor-subtypes per D9) can move between core and extension status.

**Promotion (extension-registered → core)**

A value proves universal enough that core should own the name.

- **Process**: a supersedes entry on the relevant kind contract adds the value to core's enum.
- **Compatibility (non-breaking)**: existing extensions that already register the value continue to work. Per D29 namespacing, the qualified form `some-ext:mcp-client` and the bare core form `mcp-client` are *structurally distinct identifiers*; they don't collide. Existing extensions don't need to unregister; future extensions and impls naturally adopt the bare core form.

**Demotion (core → extension-registered)**

Already exemplified by D17 (`mcp-client`, `a2a` moved out of D12's core capability list).

- **Process**: a supersedes entry on the relevant kind contract removes the value from core's enum and names a canonical extension that now hosts the registration.
- **Compatibility (potentially breaking)**: instances using the bare form must update to the canonical extension's qualified form. Framework MAY ship a one-version-cycle deprecation alias resolving the bare form to the qualified form during transition; aliasing is implementation policy, not framework-core mandate.

**Source of truth**: a value is "core" iff it appears in a kind contract's enum at framework-core layer 2. The kind contract is the canonical record; supersedes entries on the contract are how graduation happens.

### B. Versioning policy

**Kind contract versioning**

Each kind contract (D7-D20) evolves via the decision ledger. Version bump rules:

- **Major** — breaking slot change (slot removed; type narrowed; semantic-breaking change). Existing impls must update to remain conformant. Migration path declared in the supersedes entry.
- **Minor** — non-breaking slot addition (new optional slot; enum value added — i.e., promotion per §A). Existing impls remain valid.
- **Patch** — clarification only, no slot change.

D23's `work-unit-id` addition to event is a **minor** bump (optional slot added). D17's capability demotion is a **major** bump on D12 (D12's enum narrowed; existing impls advertising `mcp-client` as core need to update).

**Schema versioning** (workstream-3 artifacts) tracks kind contract versioning: schema `$id` URLs MAY include a version path segment; specific scheme is implementation per D11.

**Extension versioning**: per D29, each extension manifest carries a semver-shaped version. Semver semantics apply: major = breaking; minor = additive; patch = clarification.

**Cross-extension version-conflict resolution** (the D32 deferral)

When a workspace's `composition.extensions[]` transitively pulls multiple version-ranges for the same extension dependency:

1. Compute the intersection of all declared ranges for each transitively-required extension.
2. If intersection is empty → boot fails with version-conflict report listing the conflicting ranges + their declarers.
3. If intersection is non-empty → pick the highest version within the intersection that is locally available.
4. If no locally-available version satisfies the intersection → boot fails with version-not-found report.

Algorithm specifics (range-intersection semantics, version-comparison details) are implementation per D11.

### Worked example: a version conflict

Workspace.composition.extensions:

- `pbs-schulz-ext` requires `mcp-protocol-ext` `>=1.0.0 <2.0.0`
- `regulator-shape-ext` requires `mcp-protocol-ext` `>=2.0.0`

Boot:

1. Per D32 §3, dependency graph constructed.
2. Per this D33 §B, range intersection for `mcp-protocol-ext`: `[1.0.0, 2.0.0)` ∩ `[2.0.0, ∞)` = ∅.
3. Validator returns failure: `{category: "version-conflict", extension: "mcp-protocol-ext", conflicts: [{range: ">=1.0.0 <2.0.0", declared-by: "pbs-schulz-ext"}, {range: ">=2.0.0", declared-by: "regulator-shape-ext"}]}`.
4. Boot does not proceed.

### What is NOT in this decision

- **Specific deprecation-alias mechanics** for demotion — implementation per D11.
- **Schema URL version-path scheme** — implementation; could be `/v1/`, `/v2/`, `/2026-05-09/`, etc.
- **Migration-tooling specifics** when major contract bumps require impl updates — implementation.
- **Forward compatibility** (newer instances / impls in older runtimes) — out of scope at framework-core; impl policy.
- **Adding / removing layer-2 kinds** — would re-open D25; out of scope for layer-3 promotion rules.

**Rationale**: per D2 (kinds are abstractions; instances are extensions), graduation is the mechanism by which the boundary between abstraction and instance can shift over time as the ecosystem matures. Per I2, version-conflict resolution must be machine-checkable; intersection-based resolution is mechanical. Per D11, formal-schema and implementation are separate concerns; versioning policy operates at the kind-contract layer (semantic), with schemas tracking (formal), with implementations free to choose URL / file conventions.

Locking these together (rather than splitting) reflects that they're one workstream: graduation is essentially a versioning event (a kind contract bumps when an identifier promotes / demotes); cross-extension version-conflict resolution is the runtime consequence of versioned dependencies. One workstream, one lock.

**Cross-references**: D2 (abstractions vs. instances); D9 + D10 + D12 + D17 (open-vocabulary slots); D11 (formal schema vs. implementation); D14 (decision-ledger discipline; supersedes pattern); D25 (layer 2 closure — kinds fixed); D29 (extension manifest versions); D32 (deferred version-conflict resolution to here).

---

## D34 — 2026-05-09 — Phase A end-of-phase refinement pass output

**Decision**: The named refinement pass per D14 + D15 (analog of D24 for Phase A) produces the following findings + actions, in three categories: substantive clarifications/supersedes, schema-artifact updates, and standards-compatibility verification. Most findings are addressed in this entry's commit; one (D33's kind-contract version operationality) is left as a documented advisory; T4 hygiene items are applied to the schemas in the same commit. Pass conducted by sub-agent under fresh context (per process-kit invariant 4 — separate doer from judge).

### A. Substantive clarifications + supersedes

**A.1 — Identifier-pattern split (refines D29 + D33; was finding 1.1)**

Phase-A refinement pass surfaced that the `kebab-id` regex (`^[a-z][a-z0-9-]*$`) was inappropriately applied to *workspace-scoped runtime instance identifiers* (workspace.id, actor.id, event.id, work-unit.id, binding-ids). The regex was originally defined for *vocabulary identifiers* (extension-id, kind-impl ids, role-tags, hook names, capability values) per D29 namespacing. Instance ids carry domain-natural keys (e.g., `wu-b-plan-3.2-hennigsdorf-2024`, timestamp-shaped event ids) that the kebab-strict regex rejects.

**Refinement**: framework distinguishes:

- **`vocabulary-identifier`** (kebab-strict; `^[a-z][a-z0-9-]*$`): extension-id, substrate.id, shape.id, adapter.id, specialist.id, role-tag, hook name, capability values, runtime-shape values, payload-subtype values, work-unit-kind bare forms.
- **`instance-identifier`** (broader; `^[a-zA-Z0-9][a-zA-Z0-9._-]*$`): workspace.id, actor.id, event.id, prev-event, event.work-unit-id, work-unit.id, all binding-ids (substrate, adapter, specialist), agent-actor.substrate-binding (which references a binding-id), event.actors[].id (workspace-scoped actor reference), work-unit.contributing-actors[].id (same).

Schemas updated (workstream 3 artifacts) per finding. The kebab-strict pattern remains the canonical form for vocabulary identifiers; instance ids may include dots and uppercase to accommodate domain-natural keys.

**A.2 — `contributing-specialists[]` reference target (clarifies D30 §4; was finding 1.2)**

D19 + D20's text and D30 §4's referential-integrity rule for `work-unit.contributing-specialists[]` were ambiguous: items could plausibly be specialist-impl ids, binding-ids, or fully-qualified provision references. **Clarification**: `work-unit.contributing-specialists[]` items reference `workspace.composition.specialist-bindings[].binding-id` values (workspace-scoped instance-identifiers, not extension-namespaced). Schema slot description updated; D30 §4 reads consistently with this resolution.

**A.3 — D17 + D24 fully-qualified-form retroactive reading (clarifies; was finding 2.1)**

D17 and D24 referenced `mcp-client` and `a2a` in bare form when those values were demoted from core capabilities. Post-D29 (which locks `<extension-id>:<identifier>` namespacing), these references should read in canonical fully-qualified form (e.g., `mcp-protocol-ext:mcp-client`, `a2a-protocol-ext:a2a`). No semantic change; ledger entries pre-date D29's namespacing. Future references in derived artifacts (schemas, examples, impl) MUST use the fully-qualified form (the `substrate-claude-agent-sdk.json` example already does this correctly).

**A.4 — D17 demotion is operationally breaking (clarifies; was finding 3.3)**

D33 §A frames demotion as "potentially breaking." For D17's specific case (mcp-client, a2a moved out of D12's core capability enum), the current Phase-A schemas are *operationally* breaking: the substrate schema's `capability-identifier` `oneOf` admits only `["hooks", "skills", "event-streaming"]` in the bare-form branch + qualified-identifier in the other branch. No deprecation alias is shipped. Acceptable because Phase A precedes any reference impl per D26 (Phase B). The ledger explicitly notes this is the intended behavior, not an oversight.

**A.5 — D30 §4 actor resolution is against current state, not manifest snapshot (clarifies; was finding 6.2)**

D30 §4's wording said `event.actors[].id` resolves against `workspace.composition.actors[]`. Per D7 §4 (composition is mutable) and D19 (sub-agents spawned mid-session register as agent-actors via composition-change events), this is technically wrong for runtime-added actors. **Clarification**: actor / work-unit / specialist-binding references resolve against the workspace's *current* state (manifest + applied composition-change events), not the boot-time manifest snapshot. Same principle for work-unit identity references. Schemas describe this in slot descriptions where relevant.

**A.6 — Substrate-binding mutual exclusivity (refines D7 + workstream-3 artifacts; was finding 6.4)**

The original `workspace.schema.json` admitted a substrate-binding declaring neither `provision` nor `required-capabilities` — schema-valid but unbootable. Per D12 (specific / capability-based / mixed), at least one must be supplied. Schema updated with `anyOf: [{required: ["provision"]}, {required: ["required-capabilities"]}]` constraint at the substrate-binding item level.

**A.7 — `vocabulary-slot` enum is intentionally closed (formalizes; was finding 2.4)**

The `vocabulary-slot` enum in `extension-manifest.schema.json` is closed at the six core open-vocabulary slots listed in D29 §2 (`event.payload-subtype`, `work-unit.kind`, `substrate.capabilities`, `substrate.runtime-shapes`, `adapter.protocol-or-transport`, `actor.subtype`). Adding a new open-vocabulary slot requires (i) a supersedes entry on the relevant kind contract, (ii) a major bump to the extension-manifest contract per D33 §B, and (iii) a schema regeneration. The closed status is intentional, locked here as the policy.

**A.8 — Per-payload-subtype schemas now shipped (closes D10 + D27; was finding 5.2)**

D10 prose says framework-core validates the five core payload subtypes' shapes; the original workstream-3 event schema treated payload as `type: object` with no further structure — a contract-vs-artifact gap. **Closed in this commit**: five new schemas added — `payload-claim.schema.json`, `payload-action.schema.json`, `payload-state-change.schema.json`, `payload-composition-change.schema.json`, `payload-lifecycle-transition.schema.json`. Event schema (`event.schema.json`) discriminates payload by `payload-subtype` via `allOf` + `if/then` clauses, $ref-ing into the per-subtype schemas. The `event-claim.json` example exercises the claim payload schema and validates correctly.

**A.9 — Kind-contract versioning operationality is advisory (clarifies D33; was finding 2.2)**

D33 §B classifies D17 as a major bump on D12 and D23 as a minor bump on D10. **Clarification**: kind-contract versions are *advisory descriptors of supersede magnitude in the ledger narrative*, not operationally consumed by the boot validator. The boot validator consumes only (i) extension-manifest semver per D29 and (ii) per-kind formal schemas at their current `$id`. A future entry may make kind-contract versions operationally consumed (e.g., via a `kind-contract-version` slot on impls); current Phase A artifacts do not.

### B. Schema-artifact updates (workstream-3 hygiene; T4 findings applied)

The following schema-artifact changes are applied in the same commit:

- **`_common.schema.json` extracted** (was finding 5.1) — single source of truth for `vocabulary-identifier`, `instance-identifier`, `qualified-identifier`, `semver`, `version-range`, `capability-identifier`, `payload-subtype-identifier`, `actor-subtype-identifier`, `runtime-shape-identifier`. Each per-kind schema now `$ref`s into `_common.schema.json` rather than duplicating these patterns.
- **Stale `extends` references removed** (was findings 3.1, 3.2) — `shape.schema.json` and `extension-manifest.schema.json` description strings updated to remove residual mentions of `extends` (which D31 superseded).
- **Per-payload-subtype schemas added** — five new schemas for the core event subtypes (per A.8 above).
- **Substrate-binding `anyOf` constraint** added (per A.6 above).
- **Identifier-pattern split applied** across all schemas (per A.1 above): instance-id slots use `instance-identifier`; vocabulary-id slots use `vocabulary-identifier`.
- **Examples updated**: `work-unit-b-plan-section.json` now uses dotted form `wu-b-plan-3.2-hennigsdorf-2024` (demonstrates instance-id capability); `event-claim.json` work-unit-id reference matches.

All 10 worked examples validate against updated schemas (jsonschema 4.26.0, Draft 2020-12).

### C. Standards-compatibility verification (per D15 + D24)

| Standard | Phase A verdict | Notes |
|---|---|---|
| **MCP** | No newly-broken mapping. | Substrate example uses fully-qualified `mcp-protocol-ext:mcp-client` per D29 + D34 §A.3; consistent. |
| **A2A** | Newly-enabled (specialist `publicly-exposed` flag schema-supported). | D21's per-skill exposure-control verification target is now structurally satisfied. Agent-card mapping still Phase C. |
| **PROV-O** | No newly-broken mapping. | Qualified-identifier strings serialize fine into PROV-O URIs under reasonable mapping. |
| **CloudEvents** | Improved by A.1's instance-id widening. | Round-tripping CloudEvents `id` (no character restrictions) into workspace event chain is cleaner with `instance-identifier` than with kebab-strict. |
| **OpenTelemetry** | No delta. | Substrate.version is plain semver; OTel resource attributes consume any string. |
| **JSON Schema** | Self-mapping confirmed. | Cross-file `$ref` (e.g., `workspace.schema.json` → `actor.schema.json`) resolves canonically under Draft 2020-12 with `$id` base resolution. |
| **W3C VC, DID** | Federation-deferred per D24; no Phase A delta. | |
| **AsyncAPI, Activity Streams, EU AI Act** | Phase B/C/D mapping concerns per D24; no Phase A delta. | |
| **OpenAPI** | Out of scope at core per D24; no delta. | |

**Standards-compatibility status**: Phase A's work does not break any in-scope standards mapping; it slightly improves CloudEvents and structurally satisfies one D21 verification target (per-skill exposure control).

### D. Findings deferred (not addressed in this commit)

- **Example-coverage gaps** (was finding 5.4) — actor-human / actor-agent examples are minimal; could add `shape-none-actor-requirements.json`, `adapter-direct-in-process.json`, `extension-with-deps.json` to exercise broader surface. Hygiene only; low priority. Phase B/C may add as needed.
- **Validator-load convention `schemas/README.md`** (was finding 5.6) — Phase B prerequisite when reference impl is built.

### Outputs of the pass

- **D34 (this entry)** — clarifications A.1-A.9; schema-artifact updates B; standards-compat findings C; deferrals D.
- **No further substantive supersedes** for D27-D33 from this pass beyond what's listed above.
- **No T1 (architectural) findings** — Phase A's foundations hold up under fresh-eyes review.

**Phase A refinement pass per D14 + D15: complete.** Phase A ready for closure entry per D27 step 7-8.

**Cross-references**: D7-D20 (kind contracts; some refined in §A above); D14 (refinement-pass discipline); D15 (standards-compatibility criterion); D24 (analog of this entry for layer 2); D27 (Phase A enumeration approach); D28-D33 (Phase A entries audited).

---

## D35 — 2026-05-09 — Phase A closure (final artifacts; Phase A complete)

**Decision**: Phase A (layer 3) is **complete**. Per-kind formal schemas, extension declaration mechanism, composition rules, and promotion / demotion + versioning policy are all locked. The framework now has machine-checkable contracts at three layers (D5 identity → D7-D20 kinds → D27-D34 layer 3 formalization). Phase A is closed; per D26, Phase B (reference impl of core) is next, with the proviso that order is indicative not rigid.

### Phase A workstream summary

| Workstream | Decisions | Artifacts |
|---|---|---|
| 1. Notation | D28 | (notation-only) |
| 2. Extension mechanism | D29 | `extension-manifest.schema.json` |
| 3. Per-kind formal schemas | (no dedicated entry; produced as workstream-3 work + sharpened by D34) | `workspace.schema.json`, `actor.schema.json`, `event.schema.json`, `substrate.schema.json`, `shape.schema.json`, `adapter.schema.json`, `specialist.schema.json`, `work-unit.schema.json`, plus `_common.schema.json` and 5 per-payload-subtype schemas |
| 4. Composition rules | D30 (referential integrity), D31 (extends removed), D32 (boot-time resolution) | (rules; no dedicated artifact) |
| 5. Promotion / demotion + versioning | D33 | (rules; no dedicated artifact) |
| Refinement pass | D34 | (clarifications + schema updates) |

### Phase A artifact inventory

**Schemas in `fresh-plan/schemas/`** (15 total):

- `_common.schema.json` — shared `$defs` (extracted in D34)
- `extension-manifest.schema.json` — extension manifest contract (D29 + D31)
- `workspace.schema.json` — workspace manifest (D7)
- `actor.schema.json` — actor (D9, D22)
- `event.schema.json` — event envelope + payload discrimination (D10, D23)
- `substrate.schema.json` — substrate impl (D12, D17)
- `shape.schema.json` — shape impl (D13, D31)
- `adapter.schema.json` — adapter impl (D16)
- `specialist.schema.json` — specialist impl (D19)
- `work-unit.schema.json` — work-unit (D20)
- `payload-claim.schema.json` — claim payload (D10, D34)
- `payload-action.schema.json` — action payload (D10, D34)
- `payload-state-change.schema.json` — state-change payload (D10, D34)
- `payload-composition-change.schema.json` — composition-change payload (D10, D34)
- `payload-lifecycle-transition.schema.json` — lifecycle-transition payload (D10, D34)

**Worked examples in `fresh-plan/schemas/examples/`** (10 total):

- `a2a-protocol-ext.manifest.json`
- `workspace-pbs-schulz.json`
- `actor-agent.json`, `actor-human.json`
- `event-claim.json`
- `substrate-claude-agent-sdk.json`
- `shape-practitioner.json`
- `adapter-a2a-peer.json`
- `specialist-planning-document-work.json`
- `work-unit-b-plan-section.json`

All examples validate against their schemas (jsonschema 4.26.0, Draft 2020-12).

### What is at framework-core after Phase A

- **Layer 1 (identity, D5)** — I1 composition system + I2 machine-checkable contracts on kinds + I3 accountability-bearing AI-human work.
- **Layer 2 (kinds, D7-D20 + D22 + D23 + D31)** — 8 kinds with semantic contracts; `extends` removed from shape per D31.
- **Layer 3 (extension protocol + formal schemas, D27-D34)**:
  - Notation: JSON Schema Draft 2020-12 (D28).
  - Extension manifest contract: 4-part (identity, vocabulary registrations, provisions, dependencies) per D29 (refined by D31 removing `extends`).
  - Validation flow: workspace.composition resolution-time per D29; cross-kind referential integrity per D30; boot-time resolution per D32.
  - Promotion / demotion + versioning per D33.
  - 15 formal schemas at `fresh-plan/schemas/`; 10 worked examples.

### What is NOT yet defined (next phases per D26)

- **Phase B — reference impl of core** — substrate impl (likely Claude Agent SDK), generic shape impl, minimal adapters/specialists. Closure trigger: reference impl boots end-to-end through all 8 kinds.
- **Phase C — standards-compat impl** — A2A peer adapter; MCP server adapter (validates D21).
- **Phase D — pioneer-instance (PBS-Schulz)**.
- **Phase E — multi-deployment validation**.
- **Phase F+ — refinement, optimization, ecosystem extensions**.

### Verification targets carried forward beyond Phase A

- D21 workspace-as-A2A-peer + workspace-as-MCP-server deployability — Phase C.
- Standards-compatibility per-kind mapping at impl level (PROV-O / VC / DID / CloudEvents / OpenTelemetry / AsyncAPI / Activity Streams / EU AI Act) — Phase B/C/D as applicable.
- Per D34 §A.9: making kind-contract versioning operational (vs. advisory) — future entry.
- Per D34 §D: example-coverage gaps; validator-load convention `schemas/README.md` — Phase B as needed.

### Recap of Phase A ledger journey

- **D27** — Phase A enumeration approach (5 workstreams).
- **D28** — Notation: JSON Schema Draft 2020-12.
- **D29** — Extension manifest contract + validation flow.
- **D30** — Cross-kind referential integrity (composition rules part 1).
- **D31** — Removes `extends` from shape (D13) + extension manifest (D29); no replacement composition mechanism pending concrete need.
- **D32** — Boot-time resolution: multi-binding satisfiability + circular deps + load order (composition rules part 2).
- **D33** — Identifier graduation + versioning policy.
- **D34** — End-of-Phase-A refinement pass output.
- **D35 (this)** — Phase A closure.

**Phase A status: closed.** Next phase trigger per D26: Phase B begins when reference-impl work starts; phase boundaries are trigger-based, not schedule-based.

**Cross-references**: D5 (layer 1 identity); D14 (refinement-pass discipline); D24 + D25 (analog of D34 + D35 for layer 2); D26 (indicative roadmap); D27 (workstream order); D28-D34 (Phase A entries).

---

## D36 — 2026-05-09 — Phase B planning: workstream order + setup decisions + closure criterion

**Decision**: Phase B (reference impl of core, per D26) is planned with a workstream order, setup decisions (branch / language / repo layout), and an explicit closure criterion. Analog of D27 for Phase B. Decision is intentionally a single planning lock covering structure + setup (rather than three separate entries) for density management.

### A. Phase B workstream order

Eight workstreams, with dependencies. Order is indicative not rigid per D26 caveat — phase boundaries are trigger-based.

| # | Workstream | Depends on | One-line |
|---|---|---|---|
| **B1** | Conformance validator | — | Impl of D29 §validation flow + D30 + D32; validates extension manifests, workspace manifests, runtime references. Foundation; everything else depends on it. |
| **B2** | Substrate impl | B1 | Claude Agent SDK as the reference substrate per D12; advertises core abstract capabilities (`hooks`, `skills`, `event-streaming`). |
| **B3** | Generic minimal shape impl | B1 | Per D26: explicitly NOT practitioner-shape (pioneer-instance bias). Neutral shape exercising D13's slots. |
| **B4** | Minimal MCP-server-protocol adapter | B1, B2 | Validates the MCP adapter pattern + the registered protocol identifier (per D16). |
| **B5** | Minimal direct-api adapter | B1, B2 | Validates the non-MCP adapter path (per D16). |
| **B6** | Minimal specialist | B1, B2, B4 | Exercises D19 slots; binds to B4 adapter to demonstrate `required-adapter-bindings`. |
| **B7** | Minimal RAG-via-MCP impl | B4, B6 | Per D26: specific case of B4 pattern; validates retrieval-shaped extension. |
| **B8** | End-to-end scenario | all above | Workspace manifest exercising all 8 kinds boots + runs a scripted scenario. |

B3, B4, B5 can run in parallel after B1 + B2.

### B. Setup decisions

**B.1 — Branch strategy**: `fresh-plan` is the canonical development branch. The current session is constrained to push to `claude/identify-repo-S5zfO` by session policy; this is a session-specific quirk, not the canonical convention. Future sessions resume pushing to `fresh-plan` as the canonical record. (Closes D26's deferred "branch / commit strategy" item.)

**Commit policy**: each substantive lock = one commit, descriptive message; push after commit (no manual confirmation per the README working preferences). Branch protection / merge policy / PR review = TBD when the project has more contributors; not load-bearing for solo development.

**B.2 — Language / stack**: **Python primary** for the reference impl. Reasons:

- Claude Agent SDK is Python-native (per D12 "likely Claude Agent SDK" framing).
- JSON Schema toolchain is mature in Python (`jsonschema` library, used by the Phase A validation tests).
- Most agent-ecosystem tooling (MCP servers, A2A peer libraries) has good Python support.
- Dependency management: `pyproject.toml` + `uv` (current ecosystem standard; fast resolver).

Other languages are not ruled out — a TypeScript second-impl pass in Phase E (multi-deployment validation) is plausible if shape-neutrality evidence demands cross-language demonstration. Phase B itself is Python.

**B.3 — Repo layout**: monorepo. Code lives in `fresh-plan/impl/` alongside `fresh-plan/schemas/` and `fresh-plan/decisions.md`. Specifically:

```
fresh-plan/
  README.md
  decisions.md
  schemas/                <- Phase A formal schemas (locked at D35)
  impl/                   <- Phase B reference impl (this workstream)
    pyproject.toml
    src/                  <- Python package(s)
    tests/                <- pytest tests
    scenarios/            <- end-to-end scripted scenarios (B8)
```

Single repo, single history; cross-reference between ledger / schemas / code is straightforward. Splitting into separate repos is reversible if the project ever needs it.

### C. Closure criterion

Per D26's Phase B closure trigger ("reference impl boots and runs a minimal scenario end-to-end through all 8 kinds"), B8 must demonstrate:

- Workspace manifest declares 1 shape, ≥1 substrate-binding, ≥1 adapter-binding, ≥1 specialist-binding, ≥1 actor — exercising D7's composition cardinalities.
- Workspace boots via D29 validation flow; conformance validator (B1) passes all D30 + D32 checks.
- Scripted scenario emits ≥1 event of each core payload-subtype (claim, action, state-change, composition-change, lifecycle-transition) — exercising D10 + payload schemas.
- ≥1 work-unit of an extension-registered `kind` is created, transitions through ≥2 lifecycle states (e.g., `created` → `in-progress` → `completed`).
- Conformance validator (B1) accepts the events + work-unit references at runtime.
- All Phase A schemas (D35 inventory) are exercised at least once during the scripted run.

Scope is "smallest thing that exercises all 8 kinds end-to-end and doesn't crash." No PBS-Schulz domain content — pioneer-instance is Phase D.

### D. Discipline

- **Refinement-pass discipline carries forward** per D14 / D24 / D34. End-of-Phase-B refinement pass before closure entry.
- **Append-only ledger**, one substantive decision per entry, supersedes-pattern for changes (same as Phase A).
- **Tier model** (per session working agreement): tier 1 (direct execution) for mechanical / routine work; tier 2 (summary review at workstream boundaries) for batched implementation work; tier 3 (pre-lock review) for substantive new decisions.
- **Sub-agent dispatch** for substantive new design questions or large-artifact production where fresh-context judgment is genuinely valuable; main-session for mechanical encoding work and routine commits.

### E. What is NOT in this decision (deferred to per-workstream entries or implementation)

- Specific Python package layout (one package or multiple? namespace package? — `src/` choice noted but internals TBD).
- Specific test framework choice (probably pytest, but not load-bearing).
- CI / lint / formatter setup — implementation per D11.
- Documentation strategy for the impl (separate docs site? inline? — TBD).
- Reference-impl versioning policy specifics — follows D33 versioning.
- Forward compatibility between Phase B impl and future Phase C/D extensions — Phase C concern.

**Rationale**: Phase B is qualitatively different from Phase A — implementation, not architecture. Setup decisions (branch, language, layout) need to be in the ledger because they shape the impl trajectory; per-workstream content (specific class hierarchies, function signatures, test scaffolding) is implementation per D11 and doesn't need ledger entries beyond per-workstream completion summaries.

Single D36 covering workstream order + setup + closure (rather than three entries) reflects that Phase B planning is one coherent moment. Splitting would create artificial seams between decisions that depend on each other (e.g., "monorepo layout" assumes "Python primary" which assumes "Claude Agent SDK is the reference substrate").

**Cross-references**: D14 (refinement-pass discipline); D26 (Phase B scope + closure trigger + deferred branch-strategy item); D27 (analog of this entry for Phase A); D29 + D30 + D32 (validator B1 implements these); D35 (Phase A closure; B1 builds on the artifact inventory there).

---

## D37 — 2026-05-11 — Clarifies D19 — multi-agent orchestration is shape-policy, not framework-core

**Decision (clarifies D19 + D8)**: Multi-agent orchestration semantics — orchestrator-vs-worker distinctions, delegation patterns, coordination flow — are **shape policy**, not framework-core. Per D19's existing wording: "Event-driven (preferred at framework level): specialists subscribe to other specialists' / adapters' / shape's emissions and react via their skills. RPC-style direct invocation between specialists is implementation-shape." This entry formalizes that wording as the canonical framework-level answer.

### Rejected alternative (named)

**Kore.ai's orchestrator-vs-worker pattern**: explicit orchestrator-role designation on specialists; framework-level routing-by-role; 300+ pre-built industry templates assuming this distinction. The pattern has commercial traction and scale evidence.

Why fresh-plan rejects at framework-core: per D4 inclusion test, legitimate shapes opt out of an orchestrator-vs-worker distinction (e.g., autonomous-business-shape with parallel specialists; financial-trading-shape with broadcast-then-aggregate semantics). Forcing the distinction into core fails the inclusion test the same way the VISION axes did.

### How shapes express orchestration

Shapes that need orchestrator-worker patterns declare them via existing D13 slots:

- **`roles[]`** — shape declares `orchestrator` + `worker` as shape-level role-tags.
- **`hooks[]`** — shape declares `pre-delegate`, `post-aggregate`, etc.
- **`authority-bindings[]`** — shape requires delegation events to be attested by the orchestrator role.

No framework-core changes needed; D19's existing mechanisms accommodate the full Kore.ai pattern at shape level.

**Cross-references**: D4 (inclusion test); D8 (routing is not a framework-core kind); D13 (shape policy slots); D19 (specialist cross-specialist coordination); D26 Phase E (multi-deployment validation as evidence-gathering for shape-neutrality).

---

## D38 — 2026-05-11 — Clarifies D25 — knowledge / corpus is not a framework-core kind

**Decision (clarifies D25)**: "Knowledge" or "corpus" is **not** a framework-core kind. The 8 layer-2 kinds (D25) remain final. Knowledge as a deployment concern is supported via existing primitives:

- **Retrieval-shaped adapters** (per D16; canonical example: RAG-via-MCP per D26 Phase B B7).
- **Workspace state event projections** (claim payloads per D10 carry assertional content; per D40 events are queryable; per D39 state is fully derived from chain).
- **Shape policy** declaring knowledge-related hooks / roles / authority-bindings (e.g., a knowledge-centric shape declares roles like `curator` / `consumer` and hooks like `pre-citation`).

### Rejected alternative (named)

**Sana AI's "knowledge platform + agents" thesis**: knowledge is the central artifact; agents are tools over knowledge. Sana was acquired by Workday in 2025; the thesis has commercial traction.

Why fresh-plan rejects at framework-core: per D4 inclusion test, legitimate shapes have no knowledge corpus (e.g., financial-trading using real-time data feeds; process-automation orchestrating workflows; autonomous-business with proprietary internal state). Forcing knowledge as a core primitive fails the inclusion test the same way the VISION axes did.

Per fresh-plan's I3 (accountability-bearing AI-human work, per D5): *work* is the central organizing primitive; knowledge is supporting infrastructure. Different deployments have different relationships to knowledge — some are knowledge-centric (Sana-shape candidate); some treat knowledge as ambient context; some don't engage with knowledge at all.

### Precedent

Same shape as D8 ("no `discipline` kind at framework-core layer 2"): mechanisms-formerly-called-disciplines decompose across existing kinds. Same principle: knowledge-related mechanisms decompose across adapters, events, and shape policy. No new kind.

**Cross-references**: D4 (inclusion test); D5 I3 (accountability-bearing work as central primitive); D8 (precedent — "no discipline kind"); D10 (claim payload carries assertional content); D16 (retrieval-shaped adapters); D25 (layer 2 closure; this entry defends the kind set against the knowledge-thesis alternative); D26 Phase B B7 (RAG-via-MCP); D40 (projection / query contract enabling knowledge-related projections).

---

## D39 — 2026-05-11 — Clarifies D7 §3 + extends payload-composition-change schema — state is fully derived from the event chain

**Decision (clarifies D7 §3 + D10; extends payload-composition-change schema)**: Workspace state — actors registry, work-unit tracker, scope — is **fully derived from the event chain**. Any workspace state at any sequence point is reconstructible by replaying the event chain up to that point. This property is now named explicitly + load-bearing.

### Why this is load-bearing

- **Pre-deployment simulation** — fork from a known state, exercise an experiment, throw away the fork. Requires state-from-chain.
- **Replay debugging + time-travel** — reconstruct state at sequence N to investigate. Requires state-from-chain.
- **Analytics views** — projection of state at arbitrary points. Requires state-from-chain.
- **Audit reconstruction** — regulators (EU AI Act Article 12) or auditors (SR 11-7, OCC/CFPB) reconstruct the workspace's state evolution. Requires state-from-chain.
- **Standards-compatibility** — PROV-O genealogy, AEGIS protocol, Axon-style event sourcing all assume this property.

### Implications

Every state mutation MUST be representable as one or more events. Current core payload-subtypes (D10) cover:

- Actor changes: composition-change events with binding-kind=actor.
- Work-unit lifecycle: state-change events on work-unit status.
- Scope changes: state-change events with what=scope.
- Composition mutations: composition-change events with binding-kind ∈ {substrate-binding, adapter-binding, specialist-binding, extension}.

**Out-of-band state mutations** (changes that bypass the event chain) violate this property. Per refinement-pass discipline, any out-of-band path is either (i) covered by a synthetic event the substrate generates, or (ii) surfaced as a tension to address.

### Schema update applied in same commit

Per D34's discipline of landing schema updates with the supersedes entry, the `payload-composition-change.schema.json` is extended in the same commit:

- New optional **`record`** slot — binding-kind-specific record content carrying the full state of the added / removed / updated binding. For `change-type: add`, this slot SHOULD carry the full record so workspace state can be reconstructed from the chain alone.
- Shape of `record` is binding-kind-specific (validated against the relevant kind schema by the framework conformance validator, not by the envelope schema). For binding-kind=actor, record conforms to actor.schema.json; for binding-kind=adapter-binding, record conforms to the workspace-manifest's adapter-binding shape; etc.

### Connection to B2

B2 sub-agent flagged that the current `Workspace.register_agent_actor` registers sub-agent actor records out-of-band (per the previous composition-change schema's `additionalProperties: false`). D39 resolves this by extending the schema to admit the actor record. B2's runtime needs a minor follow-on refactor to emit composition-change events with the new `record` slot populated. Tracked as **B2-followon-1** (low-effort; not blocking B3).

### What is NOT in this decision

- **Fork-as-framework-API** — derived operation per D40 §C; substrate-impl concern.
- **Specific replay tooling** — implementation per D11.
- **Snapshot caching** for replay performance — implementation per D11; the property is "state IS derivable," not "state must be re-derived every time."

**Cross-references**: D7 §3 (state contents); D10 + D23 (event chain + work-unit-id); D29 (validation flow); D34 (refinement discipline); D40 (projection / query contract building on this property); B2 surfaced tensions.

---

## D40 — 2026-05-11 — Extends D10 — projection / query contract + integrity-mechanism extension point

**Decision (extends D10's contract)**: The event chain (D10) gains two additions: a **minimum projection / query interface** every substrate must provide, and an explicit **integrity-mechanism extension point** for protocols like AEGIS / Axon to plug in.

### A. Minimum projection / query interface

Every substrate (D12) advertising the `event-streaming` capability (per D17) must provide the following operations over the event chain it hosts:

| Operation | Description |
|---|---|
| `filter-by-actor(actor-id)` | Returns ordered subsequence of events where `actor-id` appears in `event.actors[].id`. |
| `filter-by-work-unit(work-unit-id)` | Returns ordered subsequence of events where `event.work-unit-id` matches. |
| `filter-by-payload-subtype(subtype)` | Returns ordered subsequence of events with matching `payload-subtype`. |
| `state-at(sequence-n)` | Returns workspace state derived from events 0..n (per D39 state-is-derivable property). |
| `full-chain()` | Returns the full ordered event sequence. |

These are **minimum**; substrates may provide additional operations (indexed lookups, time-range filters, payload-shape predicates, etc.). The minimum guarantees cross-substrate portability for analytics, replay, simulation, and audit-reconstruction workflows (per D12's cross-substrate-portability goal).

**Refinement of D17**: the `event-streaming` capability is defined to include the minimum projection / query interface above. No new core abstract capability is added; D17's three-capability core (`hooks`, `skills`, `event-streaming`) is unchanged. Substrates advertising `event-streaming` implicitly commit to the minimum query interface.

### B. Integrity-mechanism extension point

D10's wording "integrity-checkable; the implementation provides a mechanism" is **retained as the framework-core position** (per D2: no specific protocols at core), but **D40 names "event-chain integrity protocols" as a registered protocol-or-transport category**: extensions may register integrity protocols that substrates can adopt.

**Canonical first example (not provided in Phase A or B; named as future work)**:

**AEGIS protocol** as an extension (`aegis-protocol-ext`) registering:
- `protocol-or-transport: aegis-event-chain-integrity`
- Specifies: SHA-256 hash chain + Ed25519 signing + JCS canonicalization.
- Positioned for EU AI Act Article 12 (effective 2026-08-02), GDPR Article 22, SR 11-7, OCC/CFPB alignment.

Other integrity protocols can coexist per D29 namespacing:
- `axon-protocol-ext` for Axoniq-style event-sourcing semantics.
- `prov-o-protocol-ext` for W3C PROV-O alignment.
- Future post-quantum-signature protocols.

A workspace's substrate-binding may declare the integrity protocol it uses via binding configuration (per D7 substrate-binding.configuration). Substrates that don't support a required integrity protocol fail capability satisfaction (D30 §2) for any deployment requiring it.

**Why AEGIS is not at core**: per D2 strict reading + D17 principle ("core declares a capability iff a core kind contract references it") + D4 inclusion test (legitimate deployments may use Axon, PROV-O, internal hash chains, or post-quantum schemes instead of AEGIS specifically). Same shape as D17's demotion of `mcp-client` / `a2a` — specific protocols are extension-registered, not core. If AEGIS proves universal, D33 promotion to core is a small supersedes entry — but reversibility (demoting later if alternatives emerge) is painful, so the discipline is "stays minimal until proven universal."

### C. Connection to fork-from-state

Per D39 (state-is-fully-derived) + D40 §A (`state-at(sequence-n)` is in the minimum query interface), **fork-from-state is a derived operation**: any workspace can be reconstituted from any prefix of its event chain. Fork is not a separate framework primitive; it's a derived capability that substrates may or may not expose as an API.

Pre-deployment simulation, replay debugging, time-travel workflows, and multi-tenant isolation are all derived from these properties + the minimum query interface. No new kind needed.

### What is NOT in this decision

- **AEGIS protocol implementation** — out of scope here; named as future extension. Phase C (standards-compat impl per D26) is the natural home.
- **Specific algorithm bindings** for integrity protocols (hash function choice, signature scheme, canonicalization) — extension territory.
- **Fork-as-framework-API** — derived operation; substrate-impl concern.
- **Time-range filtering or advanced query operations beyond the minimum** — substrate may provide; not in minimum.
- **Query performance characteristics** — implementation per D11.
- **Snapshot caching for state-at(n)** — implementation per D11; the property is "state IS derivable," not "state must be re-derived from scratch on every query."

### Connection to B1 / B2

- **B1 (conformance validator)**: substrates advertising `event-streaming` are now implicitly committed to the minimum query interface. Validator does not need a new check (no schema change to substrate.schema.json); the interface contract is at runtime / impl level.
- **B2 (substrate runtime)**: `AppendOnlyEventChain` already provides four of the five minimum operations (by-id, by-actor, by-work-unit, by-payload-subtype, full-chain). Needs to add **`state-at(sequence-n)`** (replay events 0..n and reconstruct state). Tracked as **B2-followon-2** (low-to-medium effort; not blocking B3).
- Combined with D39's composition-change schema extension: B2 follow-on tasks are (i) emit `record` in composition-change events; (ii) implement `state-at(n)` replay. Both small; landed as a "Phase B internal refinement" before Phase B closure.

**Rationale**: per D2 (kinds are abstractions; instances are extensions), the integrity mechanism is an instance-level concern that extensions own. Per D12 (substrate hosts the agent loop; cross-substrate portability), the query interface needs to be uniform across substrates — so the minimum interface is core-locked. Per D5 I3 (accountability-bearing AI-human work) + D24 (EU AI Act compliance in-scope), the integrity-mechanism extension point is what lets fresh-plan plug into the regulatory landscape without forcing a specific protocol on every deployment.

The split is clean: framework specifies *what* (queries, integrity-checkability), extensions specify *how* (specific algorithms, specific canonicalization).

**Cross-references**: D2 (no specific protocols at core); D4 (inclusion test); D10 (event chain; this entry extends with minimum query + integrity extension point); D12 + D17 (substrate capabilities; `event-streaming` refined to include query interface); D24 (EU AI Act compliance in-scope; AEGIS / Axon target the same); D26 Phase C (standards-compat impl — natural home for `aegis-protocol-ext`); D29 (namespacing — integrity protocols are extension-registered); D33 (promotion / demotion — AEGIS can graduate later if proven universal); D39 (state-is-derivable; foundation of `state-at(n)`); B2 surfaced tensions (integrity mechanism + projection contract).

---
