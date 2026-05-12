# D35 — 2026-05-09 — Phase A closure (final artifacts; Phase A complete)

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
