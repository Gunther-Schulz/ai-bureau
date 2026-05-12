# D39 — 2026-05-11 — Clarifies D7 §3 + extends payload-composition-change schema — state is fully derived from the event chain

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
