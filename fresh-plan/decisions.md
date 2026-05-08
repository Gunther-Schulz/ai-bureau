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
