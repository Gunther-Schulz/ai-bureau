# fresh-plan — concepts

Framework orientation for any reader (human or agent) approaching `fresh-plan` cold. Stable reference content distilled from `decisions.md`; cite by D-number rather than re-summarizing inline. For session-procedure conventions, working patterns, ledger conventions, and current state, see `README.md` instead.

## What this is (background)

A clean restart of framework architectural decisions. The existing `pbs-bureau` corpus (`VISION.md`, `ARCHITECTURE.md`, `MAINTENANCE.md`, `GLOSSARY.md`, `arch/*`, `profiles/*`, `plugin/*`, `pbs/*`, 1-5 numbered docs at repo root) is treated as **input, not as anchor**. Each prior artifact's status (inherit-as-is / inherit-with-modification / re-derive / discard / defer) is itself a future ledger decision.

The fresh-plan reverses the prior `5-PIVOT-DECISION.md` (which had paused the framework and made PBS-Schulz primary). Per D1: **reusable framework is primary; PBS-Schulz is the first deployment / proving ground; generality wins on conflict.**

### In concrete terms (vision)

Concrete picture of what fresh-plan enables: an office worker has a project they're working on. Through the day they receive emails, look up regulations and prior decisions, draft documents based on accumulated context, coordinate with colleagues (human + agent), get sign-off, and file work. The AI workspace knows their project (scope), holds relevant context (corpus + history), routes work intelligently (some agent-handled, some human-surfaced), captures every action attributably (audit), preserves continuity across sessions (state-from-events), and composes with existing tools (email / calendar / files / CAD / accounting).

| Concrete | Framework primitive |
|---|---|
| The project's coordination context | **workspace** (D7) |
| The office worker + their agents | **actors** (D9) — `human-actor` + `agent-actor` |
| What this workspace substantively *is* | **shape** (D13) — e.g., `practitioner-shape` at Phase D |
| Email / files / CAD / accounting integration | **adapters** (D16) |
| Domain skill bundles (draft-section, review-citation, etc.) | **specialists** (D19) |
| What's being worked on (a section, a Vorprüfung, etc.) | **work-units** (D20) |
| The audit trail of everything that happened | **event chain** (D10) |

**Automation level is a deployment configuration, not a framework constraint.** A workspace can run with high human involvement (every claim requires human attestation; specialists deferred to human review), low human involvement (most events agent-attributable; humans only for sign-off), or fully autonomous (no human-actors; agent-actors fulfill all roles). The framework expresses this fluidity via:

- **Shape choice** — `practitioner-shape` mandates ≥1 human-actor; `autonomous-business-shape` requires none. Different shape = different default posture.
- **Per-event authority-bindings (D13 with `qualifier` slot)** — same payload-subtype can have different requirements depending on event qualifier. Defensibility-grade claims may require human-actor attestation; routine-draft claims may admit agent-actor attribution. Same workspace, mixed posture per event class.
- **Composition mix** — which specialists / adapters are bound determines where work is routed. Same shape, different bindings = different automation posture.
- **Evolution over time** — composition-change events (D10) + shape versioning (D33) let a workspace's posture *change over its lifetime*. Start human-attested; swap in agent-attribution as trust + capability grow. The event chain records the transition; the new shape version represents the new snapshot.

Same framework, 1% automation, 50%, 99%. The spec doesn't prescribe a ratio; the deployment configures it; the workspace evolves it. PBS-Schulz pioneer-instance (Phase D) instantiates the high-human-involvement end; future deployments calibrate differently. The framework's job is to make all of them attributable, composable, audit-replayable — regardless of posture.

**How shapes evolve over the long term** (shapes are designed to be decades-stable):

- **Role vocabulary is the durable layer.** Roles like `drafter` / `attester` / `reviewer` / `supervisor` / `sign-off` name *functions* — what gets done — not *who does it*. The function vocabulary stays stable across versions of a shape because the work itself is stable; only the actors fulfilling each role change.
- **Authority-binding is the flexible layer.** Same role, different `required-actor-subtype` across shape versions. `practitioner-shape@1.0.0`'s `attester` role required human-actor; `@2.0.0`'s `attester` role admits agent-actor for routine, human-actor for defensibility-grade. Same function; different mechanism per version.
- **Substantive identity is preserved as long as the role vocabulary stays.** A shape with stable roles + evolving authority-bindings + evolving composition mix is *the same shape* (version bumps). A shape with fundamentally different role vocabulary is *a different shape* (workspace boundary; reboot with new shape).
- **The accountability anchor persists.** Even in the maximally-automated case, the workspace has an *accountable party* — the human / org legally on the hook if a regulator audits. That party is a human-actor (or possibly an extension-registered org-actor subtype) in the workspace, even when only fulfilling a `signee` / `accountable-party` role. EU AI Act + similar regulations mandate this regardless of automation level; `practitioner-shape`'s substantive identity holds *as long as practitioner accountability holds*. Drop the accountability anchor → workspace migrates to a different shape (autonomous-business-shape territory).

PBS-Schulz over decades concretely: same `practitioner-shape` throughout (with major version bumps as automation matures); same role vocabulary; evolving authority-bindings (progressively more agent-actor admission); evolving composition (more specialists; more adapters); accountable-party stays the practitioner. If that role itself goes away, it's a shape identity change — migration, not version bump.

### What is durable vs scaffolding

Working framing (stake-in-the-ground; candidate D42 at end-of-Phase-B refinement after source-grounded reads of Bucket A platform positioning):

**The durable contribution** is the **specification + methodology + protocol extensions** for accountability-bearing AI-human work:
- *Vocabulary* — workspace, actor, event, substrate, shape, adapter, specialist, work-unit (the 8 kinds; D7 / D9 / D10 / D12 / D13 / D16 / D19 / D20).
- *Structural commitments* — I1 composition / I2 machine-checkable contracts / I3 accountability-bearing AI-human work (D5).
- *Composition rules* — extension manifest contract, boot-time resolution, versioning policy (D29 / D30 / D31 / D32 / D33).
- *Protocol extensions* — workspace-as-A2A-peer (D21); adapter-as-MCP-server (D16); integrity-mechanism extension point with AEGIS / Axon as canonical examples (D40 §B); standards-alignment toward PROV-O / VC / DID / CloudEvents / OpenTelemetry / AsyncAPI / JSON Schema / Activity Streams / EU AI Act tooling (D24).
- *Methodology* — see "Methodology placement" section below.

**The scaffolding** is the **reference implementation** at `fresh-plan/impl/`:
- B1 conformance validator + B2-B6 runtime classes + shipped extensions. Necessary for two things: (a) proving the specification is implementable (the durability bet survives "spec without ref-impl never gets adopted"); (b) supporting PBS-Schulz daily use during Phase D pioneer-instance. Not the canonical runtime; one exemplar of the spec.

**Why this framing matters**: the historical survivor pattern (CORBA → REST, SOAP → JSON-over-HTTP, EJB → POJOs + microservices, etc.) suggests thick runtime middleware perishes when models + protocols mature; thin specs survive. Fresh-plan's ledger is mostly already specification-shaped; the framing makes the durability bet explicit and shapes how future entries frame themselves. JSON Schema for accountability-bearing AI-human workspaces; not CORBA for accountability-bearing AI-human workspaces.

**What this is NOT a bet on**: the radical "agents fully self-organize structural work; humans become signees" extrapolation. No Bucket A platform with shipping power (Gemini Enterprise, Microsoft Copilot Studio, Salesforce Agentforce, IBM watsonx, Kore.ai) publicly targets that scenario. Their actual stated direction — agents + orchestration + protocols + governance + persistent human-in-the-loop — is *more* friendly to fresh-plan's positioning, not less. The conservative direction has stronger demand-signal for accountability infrastructure than the radical scenario. Use the radical framing as a stress-test to avoid painting corners (composition rules should permit runtime discovery; event chain should be capability-card-compatible); do not position for it as roadmap.

**Why discovery + smart agents don't replace this**: A2A / MCP / agent cards / discoverability handle *how agents wire up + how work gets done*. They do not handle *attribution* (who said what, attributable to whom), *audit replay* (reconstructing state at sequence N), *authorization* (which roles can delegate which events), or *composition validation* (is this workspace's composition valid against its shape policy?). Smart agents producing more autonomous work create *more* records that need shared structure — the OpenTelemetry / OpenAPI / Prometheus pattern. EU AI Act Article 12 (Aug 2026) makes audit-grade records legally mandatory for certain AI systems. Fresh-plan sits in the demand side of that regulatory + governance arc; the wire-level protocols sit underneath.

### Relationship to governance frameworks / tooling

"Governance" is a broad term spanning several distinct concerns. Fresh-plan covers the **specification-side**; hooks into existing tools for the **runtime-side**:

| # | Concern | Fresh-plan covers? |
|---|---|---|
| 1 | Audit / accountability records (who did what when, attributable, replayable) | **YES — spec side**: I3 + D10 event chain + D39 state-from-events + D40 §A `state_at(n)` projection. |
| 2 | Authority / authorization semantics (role-bindings, signing, who can do what) | **YES — spec side**: D13 authority-bindings + shape role vocabulary. |
| 3 | Integrity / tamper-evidence (cryptographic guarantees over records) | **YES — extension point**: D40 §B integrity-mechanism slot; AEGIS / Axon / post-quantum schemes register here. |
| 4 | Compliance reporting (EU AI Act / NIST AI RMF / SR 11-7 / SOX) | **PARTIAL — spec aligns**: D24 standards-alignment list. Reporting *tools* are external. |
| 5 | Policy enforcement engines (runtime evaluators) | **NO — tooling**: Open Policy Agent / Cedar / etc. Fresh-plan declares policies; engine choice is external. |
| 6 | Risk dashboards / model risk / content risk | **NO — tooling**: Microsoft AGT / IBM OpenPages / AuditBoard / Drata. They consume event records. |
| 7 | Lifecycle approvals (deployment gates, change management) | **NO — tooling**: ServiceNow / ITIL / workflow products. Approval-as-event lives in fresh-plan; workflow engine doesn't. |
| 8 | Identity binding (workspace-actor ↔ real-world identity via SSO / JWT / DID) | **Mostly external** — mechanism is adapter-territory + external IdPs. **Binding-contract slot is currently a gap** (see open questions). |

The relationship is the durability-framing pattern: fresh-plan provides the *contract* that governance tooling reads against. A workspace's event chain is structured per fresh-plan's spec; compliance tooling (existing products, future Bucket A platform features, in-house) consumes it to produce reports / dashboards / approval flows. Fresh-plan does not re-implement what governance products already ship.

This matches what Bucket A platforms are publicly doing: adding governance features as agents become more autonomous (Microsoft AGT, Salesforce Agentforce governance, IBM watsonx Orchestrate governance). They need shared specs to consume. Fresh-plan competes by providing better specs, not by competing with their tooling. Follow established specs (PROV-O, JSON Schema, AEGIS-shape, EU AI Act audit-record requirements) as much as possible; introduce new vocabulary only where existing standards leave a gap fresh-plan's positioning fills (accountability-bearing workspace composition is the genuine gap).

## Layered structure (per D3)

| Layer | Content | Status |
|---|---|---|
| **Layer 1 — identity** | I1 composition system / I2 machine-checkable contracts / I3 accountability-bearing AI-human work. No substantive identity at core; substantive identity carried by shapes per D4. | Closed at D5. |
| **Layer 2 — kinds** | 8 kinds (workspace D7, actor D9, event D10, substrate D12, shape D13, adapter D16, specialist D19, work-unit D20). | Closed at D25. |
| **Layer 3 — extension protocol + formal schemas** | Per-kind formal schemas (workstream 3 artifacts in `schemas/`). Extension declaration mechanism (D29). Composition + boot-time resolution (D30, D31, D32). Promotion / demotion + versioning policy (D33). End-of-Phase-A refinement (D34). | Closed at D35 (Phase A). |
| **Implementation (below layer 3)** | Format / serialization choices; storage / wire / protocol mechanisms; specific extension impls (substrate impls, shape impls, adapter impls, specialist impls). | Out of scope for framework-core work. Begins at D26 Phase B. |

## The 8 kinds at a glance

| Kind | Decision | One-line |
|---|---|---|
| workspace | D7 | Bounded coordination context where one composition runs (manifest + state). |
| actor | D9 (refined by D22) | Attribution-bearing participant; subtypes `human-actor` / `agent-actor`. |
| event | D10 (refined by D23) | Single ordered chain per workspace; payload-subtypes (claim, action, state-change, composition-change, lifecycle-transition + extension-registered). |
| substrate | D12 (cap section by D17) | Hosts the agent loop; declares capabilities (core abstract: `hooks`, `skills`, `event-streaming`) + extension-registered protocol-named capabilities. |
| shape | D13 | Substantive identity carrier (per D4); policy bundle. |
| adapter | D16 | Interface to external surfaces; `protocol-or-transport` open vocabulary (no specific protocols at core per strict D2). |
| specialist | D19 | Internal capability bundle; declares skills + supported work-unit-kinds + adapter dependencies + event subscriptions. |
| work-unit | D20 | Instance of organized work; kind-discriminated (extension-registered); fixed core lifecycle enum (created / in-progress / paused / completed / abandoned). |

## Protocol extensions

First-class deliverable cluster per the durability framing: fresh-plan defines how accountability-bearing workspaces integrate with the maturing protocol ecosystem. These are *not* extensions to fresh-plan's core; they are fresh-plan's contributions *to* external specifications, expressed via the extension mechanism (D29).

| Target | Fresh-plan contribution | Source decisions |
|---|---|---|
| **A2A** (agent-to-agent peering) | Workspace-as-A2A-peer deployability — every workspace can expose its specialists + accept work as an A2A peer | D21 |
| **MCP** (Model Context Protocol, under Linux Foundation) | Adapter-as-MCP-server pattern — any MCP server is a candidate adapter via the protocol-or-transport extension-registered vocabulary | D16 + D29 |
| **PROV-O** (W3C provenance) | Event-chain alignment — workspace event chain is structurally compatible with PROV-O genealogy + Activity Streams | D10 + D24 |
| **Event-chain integrity** (AEGIS, Axon, post-quantum signatures, etc.) | Integrity-mechanism extension point — substrates declare which integrity protocol they implement; framework specifies what (queries, integrity-checkability); extensions specify how | D40 §B |
| **EU AI Act Article 12** (audit-record reconstruction, effective 2026-08-02) | Standards-compat workstream + D17 query-interface (`state_at(n)`) make audit replay an architectural property, not a bolted-on feature | D24 + D40 §A |
| **JSON Schema 2020-12** | Formal-schema notation; all kind contracts are machine-validatable | D28 + D34 §A.6 |
| **Standards under D24 watch** | PROV-O / VC / DID / CloudEvents / OpenTelemetry / AsyncAPI / Activity Streams — per-kind mapping work split across Phases A (layer-3-affecting), B/C (impl-level), D (deployment-specific) | D24 |

The pattern: framework-core stays protocol-neutral (per D2 strict reading); protocol identifiers are extension-registered (per D17 + D29); per-protocol behavior is extension-defined. This composes with the durability framing — fresh-plan adds *contracts* to the protocol ecosystem; it does not *re-implement* what protocols already standardize.

## Roadmap (indicative; per D26)

Phases beyond layer-2 closure, named at high level — order indicative not rigid; phase boundaries trigger-based not scheduled. See **D26** in `decisions.md` for full content.

| Phase | Work | Status |
|---|---|---|
| **A — Layer 3** | Formal schemas per kind; extension declaration mechanism; composition / promotion rules; JSON Schema toolchain | **Closed at D35.** Refined by D34 (refinement pass) + D37-D40 (side-quest sharpening). |
| **B — Reference impl of core** | Generic substrate / shape / adapters / specialist; minimal RAG-via-MCP | **In progress.** Workstreams per D36 + D41 + D42: B1 conformance validator ✅, B2 substrate runtime ✅ (+ B2-followon-1 D39 record emission ✅ + B2-followon-2 D40 §A `state_at(n)` ✅), B3 generic shape ✅, B4 MCP-server adapter (stub) ✅, B5 direct-api adapter (stub) ✅, B6 specialist ✅ (+ subscriber-dispatch infrastructure giving D17 event-streaming push semantics per D37), B2b MS Agent Framework substrate stub (per D41; required before closure; parallel-eligible with B7/B8), B7 RAG-via-MCP, B8 end-to-end, **Bref (per D42; refinement workstream between B8 and closure entry; output D-entry analogous to D34)**, Phase B closure entry (analog of D25 / D35). |
| **C — Standards-compat impl** | A2A peer adapter; MCP server adapter (validates D21) | Not started. Phase B prerequisite. |
| **D — Pioneer-instance (PBS-Schulz)** | Practitioner-shape; domain specialists; bauleitplanung corpus; PBS-Schulz workspace manifest; cutover from 0.1.0 plugin | Not started. Phase B + C prerequisite. |
| **E — Multi-deployment validation** | Second shape impl; second workspace; federation begins | Not started. |
| **F+** | Refinement / optimization / ecosystem | Indefinite. |

## Open questions / deferred items (with phase placement)

Per D26, deferred items have implicit phase homes:

- **D1 open tension** (PBS-Schulz daily during rebuild) → resolved in Phase D.
- **Optional `parent-actor` slot on actor** → revisit in Phase A or B if sub-agent patterns surface concrete need.
- **Workflow as containment hierarchy on work-unit** → Phase D (pioneer) or E (multi-deployment) if forced.
- ~~Branch / commit strategy~~ → **resolved in D36** (`fresh-plan` is canonical).
- **D21 verification targets** (A2A peer + MCP server) → Phase C.
- **Standards-compat per-kind mapping** (PROV-O, VC, DID, CloudEvents, OpenTelemetry, AsyncAPI, JSON Schema, Activity Streams, EU AI Act) → split across Phase A (layer-3-affecting), B/C (impl-level), D (deployment-specific). **Status: list is named in D24 as alignment targets but the actual mapping work is mostly unstarted.** Concrete sub-items for Phase B/C: (i) PROV-O event-chain mapping — workspace event chain ↔ PROV-O Activity / Agent / Entity; (ii) CloudEvents envelope alignment — do our event shapes round-trip through CloudEvents binding?; (iii) EU AI Act Article 12 audit-record bundle format — what's a regulator-consumable export?; (iv) OpenTelemetry trace alignment for cross-workspace operations; (v) VC + DID for actor-identity binding (composes with the identity-binding gap below). Some (i, ii) are Phase B-affordable; most are Phase C natural home.
- **Identity-binding spec slot for actor records (gap)** → D9 + D22 specify actor.id / subtype / declared-name / substrate-binding; no slot for *external-identity reference* (e.g., DID, SSO subject, JWT). The mechanism is external (adapter-territory + external IdPs); the *binding contract* is fresh-plan-shaped. Becomes load-bearing in Phase C (A2A peering = cross-workspace identity) and Phase D (PBS-Schulz humans need real-identity mapping). Candidate refinement entry; specifically a small actor-schema amendment adding an optional `external-identity: { scheme, identifier, verification? }` slot.
- **Live in-place shape migration deliberate scope-cut (implicit, should be explicit)** → `payload-composition-change.schema.json` binding-kind enum is `{substrate-binding, adapter-binding, specialist-binding, actor, extension}` — shape is NOT in the enum. Migration to a new shape version requires workspace reboot (event chain preserved per D39; new shape version applies to events appended after the transition; transition itself recorded as composition-change / lifecycle event). Probably correct (cleaner audit lineage; shape carries substantive identity per D4 + D7 mandates exactly-1-shape-per-workspace; live identity-mutation mid-life is conceptually fraught) but currently implicit. Candidate clarification entry naming the scope-cut + reasoning, so future readers (and future-us) don't assume it's an oversight.
- ~~B2 follow-on tasks~~ → **completed**: B2-followon-1 (composition-change `record` per D39) + B2-followon-2 (`state_at(sequence_n)` per D40 §A) landed.
- **D39 out-of-band-state tensions surfaced for end-of-Phase-B refinement** (per D39 "(ii) surfaced as a tension to address"): (a) manifest-declared actors loaded into state at boot bypass the event chain — `state_at(n)` pure-replay does not reflect them; (b) work-units' full records are not carried in state-change events (only `id` and status) — replay reconstructs status but not the full record. Both need either synthetic-event emission at boot (closing the loop) or explicit ledger entries before Phase B closure.
- **Phase B refinement workstream — Bref (per D42)** — formalized as a named workstream, running between B8 and Phase B closure entry; output is one substantive D-entry analogous to D34. Currently-tracked deliverables (canonical scope list, will grow as B7 / B8 surface more):
  - Resolve D39 out-of-band-state tensions (manifest-actor seeding + work-unit record carry).
  - D17 capability-vocabulary sharpening if B2b two-substrate parity (D41) surfaces Claude-flavored bias.
  - Sana-style knowledge-query worked-example validating D38 (no knowledge-kind needed; decomposes across adapters + state + shape policy).
  - **Activation-scope DSL** for specialists per D19 — currently the slot is opaque metadata (runtime treats any non-null value as always-active-when-bound). Phase D pioneer concrete activation expressions give the DSL design real input; locked here as a candidate refinement deliverable.
  - **boot.py step-3 duplication cleanup** — the substrate-provision capability resolution in step 3 still has an inline `discover_extensions / load_extension / provisions_loaded.get` block (same pattern step 8 shed in B6). Route through `load_provision_spec` for consistency. Small (~20-line cleanup); not blocking any workstream.
  - **Subscriber-dispatch reentrancy / loop semantics** — the substrate dispatches events to subscribing specialists' `on_event` after append (per B6 + D37). If a real (non-stub) `on_event` emits new events, those fire more subscribers — could loop. B6 stubs are no-op so no actual loop today, but real reactive specialists in Phase D will hit this. Design choice for refinement: re-entry guard (subscribers receive events only during their own bounded scope), explicit-loop semantics (recursion allowed up to N levels), or queued-dispatch (events accumulate, drain after the trigger event's append returns). Refinement-time decision.
  - **Migration-safety discipline for shape versioning per D33** — guidance for shape authors on what kinds of shape-version bumps are *safe in-place* vs *define a new era* vs *breaking*. Sketch: loosening authority-bindings (admitting agent-actor where human was required) is safe in-place; tightening authority-bindings defines a new era (old events stand under prior shape, new under tightened, transition is a recorded event); additive role / hook / payload-subtype additions are safe; removals are breaking and require major version bump or workspace boundary. PBS-Schulz pioneer-instance trajectory (high-human-involvement v1 → mixed → mostly-automated v2) is the canonical loosening case + concrete grounding for the discipline.
  - **Split `decisions.md` into per-entry files at `decisions/D<NN>-<slug>.md`**, with `decisions.md` becoming a thin chronological index. Precedent: pbs-bureau's GLOSSARY split (36 per-entry files) + DISCIPLINES split (10 per-discipline files) for context-load efficiency. Trigger: file size + Phase-C-onward growth makes the monolith painful. Done as part of refinement so it composes with the closure-entry write rather than colliding with mainline workstream commits.
- **AEGIS / Axon integrity-protocol extensions** → Phase C (per D40 §B as canonical first examples).
- **Positioning** (open-source / craft-practice / accountability-bearing / methodology-layer) → deliberately deferred per `market-context.md`; revisit Phase D or later.
- **Two-substrate parity (D41)** → B2b (MS Agent Framework substrate stub or equivalently diverse second substrate) shipped before Phase B closure; D17 capability vocabulary sharpened at end-of-Phase-B refinement if cross-tension surfaces.
- **Positioning lock (candidate Bref-output-adjacent entry)** → end-of-Phase-B refinement deliverable: a clarification of D1 making explicit that the durable contribution is the specification + methodology + protocol extensions; the reference impl is exemplar, not canonical runtime. Stake-in-the-ground framing currently in CONCEPTS "What is durable vs scaffolding" + "Protocol extensions" sections. Pre-lock: source-grounded reads of Gemini Enterprise / Microsoft Copilot Studio + AGT / Salesforce Agentforce / IBM watsonx Orchestrate / Kore.ai current product positioning pages, so the entry is grounded in *what they publicly target*, not synthesis.

## Cross-phase work-streams

Some threads of work span multiple phases rather than living in one. Sequential phasing can obscure this; surface explicitly:

- **Substrate-neutrality evidence** — proven by stub-pair in Phase B (per D41) + reinforced by real-wire substrate impls in Phase C. Single-substrate evidence is not sufficient.
- **Shape-neutrality evidence** — proven by second shape impl in Phase E (practitioner-shape in Phase D first, then a contrasting shape in E per D26). Single-shape evidence is not sufficient.
- **Methodology articulation** — see "Methodology placement" below; lives in shape-policy + specialist behavior at Phase D, not as a separate phase.
- **Positioning** — research lives in `market-context.md`; commit-decision waits for Phase D pioneer evidence; no dedicated phase.

## External-trigger checkpoints

Trigger-based phasing (per D26) is correct discipline for internal work but blind to calendar-bound externals. Known external events that should re-evaluate roadmap priorities when they hit:

- **EU AI Act Article 12 effective date — 2026-08-02.** Audit-record reconstruction requirements become enforceable. AEGIS-shaped integrity protocol (per D40 §B) is the canonical extension target; Phase C is the natural impl home. Re-evaluate Phase C scope when the date approaches.
- **Microsoft Agent Framework GA / version evolution.** D41 names MS Agent Framework as the candidate second substrate; if its API shifts substantially between B2b authoring and Phase C real-wire work, B2b stub may need re-mapping.
- **MCP spec evolution under Linux Foundation.** Phase C's MCP-server-protocol adapter (per D26) tracks the spec; major version changes require Phase C scope adjustment.
- **Anthropic API changes affecting Claude Agent SDK.** Substrate-binding contracts may shift; relevant for Phase C real-wire impl.

These are monitoring discipline, not architecture. Update list as new external dependencies surface.

## Status of the existing pbs-bureau corpus

Treated as **preservation / input only**. Specific findings so far:

- `VISION.md` three axes (intertwining / sparring / authorship-preservation / defensibility / engaged-authorship): **moved from framework identity to shape policy** per D4. Practitioner-shape carries them.
- `arch/adapter.md` 5 Surfaces (Email / Accounting / MCP-Server / A2A-Peer / File-Sync): **superseded** — no specific protocols at framework-core per D2 + D17. Protocol identifiers are extension-registered.
- `arch/*` discipline mechanisms (audit / sparring / gate / authority-binding): **decomposed** per D8 — audit is state property; sparring/authority-binding are shape policy; gate is specialist+shape concern. No `discipline` kind at framework-core.
- `1-NEXT.md` F1-F4 plan: **paused** per 5-PIVOT-DECISION; further reversed by D1 (reusable framework now primary, PBS-Schulz secondary).
- Existing `arch/practitioner.md`, `arch/workflow-work-unit.md`, etc. — not yet processed against fresh-plan; treat as input when relevant.

### Methodology placement

Methodology content from the inherited corpus — `DISCIPLINES.md`, `process-kit/`, `profiles/` — has no dedicated phase in the roadmap. The structural answer is locked in **D4** + **D8**: methodology mechanisms (disciplines, sparring, audit, authority-binding, etc.) **decompose** into shape policy + specialist behavior + adapter mechanics. There is no separate "methodology" kind at framework-core.

So methodology *content* (what does "be a practitioner" mean? what's the workflow of writing a Begründung? what's the discipline of sparring?) lives in **shape impls + specialist impls** at Phase D pioneer-instance. The older `DISCIPLINES.md` / `process-kit/` / `profiles/` artifacts are *input* to that re-derivation — preservation per the "Status of the existing pbs-bureau corpus" section above; not directly inherited. Practitioner-shape (Phase D) is where the methodology resurfaces with framework-aware policy structure.

## Repository layout

```
fresh-plan/
  README.md          <- session-procedure anchor: working disciplines + patterns + ledger conventions + current state
  CONCEPTS.md        <- this file: framework orientation (what fresh-plan is, the 8 kinds, layered structure, roadmap)
  decisions.md       <- the append-only ledger (D1 through current)
  market-context.md  <- adjacent products + positioning research notes (not committed positioning)
  schemas/           <- Phase A layer-3 formal schemas (D28 + workstream 3 + D34 + D39 + D40)
    README.md        <- multi-schema loading convention + identifier + authoring conventions
    _common.schema.json
    extension-manifest.schema.json
    workspace.schema.json
    actor.schema.json
    event.schema.json
    substrate.schema.json
    shape.schema.json
    adapter.schema.json
    specialist.schema.json
    work-unit.schema.json
    payload-claim.schema.json
    payload-action.schema.json
    payload-state-change.schema.json
    payload-composition-change.schema.json
    payload-lifecycle-transition.schema.json
    examples/        <- worked-example instances (validate against schemas)
  impl/              <- Phase B reference impl (per D36)
    README.md        <- install + CLI + library usage + naming conventions
    pyproject.toml   <- Python 3.11+; deps: jsonschema, referencing, pyyaml, click, node-semver
    src/fresh_plan/
      validator/     <- B1: conformance validator (D29 + D30 + D32 + D33)
      runtime/       <- B2-B4: substrate runtime + shape + adapter (D7 + D10 + D12 + D13 + D16 + D19 + D20)
      cli.py         <- fresh-plan-validate + fresh-plan-run
    tests/           <- pytest; 128 tests passing as of B4
    extensions/      <- shipped canonical extensions
      inprocess-substrate-ext/  <- B2 substrate
      generic-shape-ext/        <- B3 shape (GenericShape(Shape))
      mcp-server-ext/           <- B4 stub MCP-server-protocol adapter (MCPToolAdapter(Adapter))
      direct-api-ext/           <- B5 stub direct-api adapter (DirectAPIAdapter(Adapter))
      generic-specialist-ext/   <- B6 specialist (GenericSpecialist(Specialist); registers generic-task into work-unit.kind)
```
