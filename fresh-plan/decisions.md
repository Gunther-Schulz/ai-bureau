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
