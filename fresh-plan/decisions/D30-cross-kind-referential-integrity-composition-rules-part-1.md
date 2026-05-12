# D30 — 2026-05-09 — Cross-kind referential integrity (composition rules part 1)

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
