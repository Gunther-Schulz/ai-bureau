# fresh-plan — concepts

Framework orientation for any reader (human or agent) approaching `fresh-plan` cold. Stable reference content distilled from `decisions.md`; cite by D-number rather than re-summarizing inline. For session-procedure conventions, working patterns, ledger conventions, and current state, see `README.md` instead.

## What this is (background)

A clean restart of framework architectural decisions. The existing `pbs-bureau` corpus (`VISION.md`, `ARCHITECTURE.md`, `MAINTENANCE.md`, `GLOSSARY.md`, `arch/*`, `profiles/*`, `plugin/*`, `pbs/*`, 1-5 numbered docs at repo root) is treated as **input, not as anchor**. Each prior artifact's status (inherit-as-is / inherit-with-modification / re-derive / discard / defer) is itself a future ledger decision.

The fresh-plan reverses the prior `5-PIVOT-DECISION.md` (which had paused the framework and made PBS-Schulz primary). Per D1: **reusable framework is primary; PBS-Schulz is the first deployment / proving ground; generality wins on conflict.**

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

## Roadmap (indicative; per D26)

Phases beyond layer-2 closure, named at high level — order indicative not rigid; phase boundaries trigger-based not scheduled. See **D26** in `decisions.md` for full content.

| Phase | Work | Status |
|---|---|---|
| **A — Layer 3** | Formal schemas per kind; extension declaration mechanism; composition / promotion rules; JSON Schema toolchain | **Closed at D35.** Refined by D34 (refinement pass) + D37-D40 (side-quest sharpening). |
| **B — Reference impl of core** | Generic substrate / shape / adapters / specialist; minimal RAG-via-MCP | **In progress.** Workstreams per D36 + D41: B1 conformance validator ✅, B2 substrate runtime ✅ (+ B2-followon-1 D39 record emission ✅ + B2-followon-2 D40 §A `state_at(n)` ✅), B3 generic shape ✅, B4 MCP-server adapter (stub) ✅, B5 direct-api adapter (stub) ✅, B6 specialist (next), B2b MS Agent Framework substrate stub (per D41; required before closure; parallel-eligible with B6/B7/B8), B7 RAG-via-MCP, B8 end-to-end. |
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
- **Standards-compat per-kind mapping** (PROV-O, VC, DID, CloudEvents, OpenTelemetry, AsyncAPI, JSON Schema, Activity Streams, EU AI Act) → split across Phase A (layer-3-affecting), B/C (impl-level), D (deployment-specific).
- ~~B2 follow-on tasks~~ → **completed**: B2-followon-1 (composition-change `record` per D39) + B2-followon-2 (`state_at(sequence_n)` per D40 §A) landed.
- **D39 out-of-band-state tensions surfaced for end-of-Phase-B refinement** (per D39 "(ii) surfaced as a tension to address"): (a) manifest-declared actors loaded into state at boot bypass the event chain — `state_at(n)` pure-replay does not reflect them; (b) work-units' full records are not carried in state-change events (only `id` and status) — replay reconstructs status but not the full record. Both need either synthetic-event emission at boot (closing the loop) or explicit ledger entries before Phase B closure.
- **Phase B end-of-phase refinement** (per D14 / D34 pattern) before Phase B closure entry (analog of D25 / D35). Codified deliverables for the refinement pass:
  - Resolve D39 out-of-band-state tensions (manifest-actor seeding + work-unit record carry).
  - D17 capability-vocabulary sharpening if B2b two-substrate parity (D41) surfaces Claude-flavored bias.
  - Sana-style knowledge-query worked-example validating D38 (no knowledge-kind needed; decomposes across adapters + state + shape policy).
  - **Split `decisions.md` into per-entry files at `decisions/D<NN>-<slug>.md`**, with `decisions.md` becoming a thin chronological index. Precedent: pbs-bureau's GLOSSARY split (36 per-entry files) + DISCIPLINES split (10 per-discipline files) for context-load efficiency. Trigger: file size + Phase-C-onward growth makes the monolith painful. Done as part of refinement so it composes with the closure-entry write rather than colliding with mainline workstream commits.
- **AEGIS / Axon integrity-protocol extensions** → Phase C (per D40 §B as canonical first examples).
- **Positioning** (open-source / craft-practice / accountability-bearing / methodology-layer) → deliberately deferred per `market-context.md`; revisit Phase D or later.
- **Two-substrate parity (D41)** → B2b (MS Agent Framework substrate stub or equivalently diverse second substrate) shipped before Phase B closure; D17 capability vocabulary sharpened at end-of-Phase-B refinement if cross-tension surfaces.

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
```
