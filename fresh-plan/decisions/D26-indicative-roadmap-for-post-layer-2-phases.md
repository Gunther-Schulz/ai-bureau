# D26 — 2026-05-08 — Indicative roadmap for post-layer-2 phases

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
