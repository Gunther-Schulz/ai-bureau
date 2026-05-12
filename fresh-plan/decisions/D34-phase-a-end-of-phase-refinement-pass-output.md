# D34 — 2026-05-09 — Phase A end-of-phase refinement pass output

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
