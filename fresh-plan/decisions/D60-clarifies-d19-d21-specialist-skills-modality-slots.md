# D60 — 2026-05-17 — Clarifies D19 + D21 — `specialist.skills[]` modality + publicly-exposed slots are A2A-peer agent-card vocabulary anticipation

**Decision (clarifies D19 + D21)**: The `specialist.skills[].input-modalities` / `output-modalities` / `publicly-exposed` slots in `schemas/specialist.schema.json` (lines 46-51) are **opaque (documentary) slots** that anticipate D21's workspace-as-A2A-peer deployability. They populate the A2A AgentCard at peer-export time (Phase D+). The framework does **not** validate their semantics today: no boot-time validation; no runtime consumption; no enum constraint on modality strings. Carries through to the agent-card surface when D21 deployability lands. No impl change required — slots already in schema; this entry makes the load-bearing-anticipation intent explicit at ledger layer.

### Substantive grounding

D21 §"What this requires from framework-core" names the requirement: "Specialist `skills[]` declarations (per D19) carry enough metadata to map to A2A agent-card skill entries (name, description, input / output modalities)." D21 §"What this requires from extensions" names per-skill `publicly-exposed` as exposure control so internal-only skills don't leak into the agent-card. The schema-locked slots (`input-modalities`: array of non-empty strings; `output-modalities`: array of non-empty strings; `publicly-exposed`: boolean) are the concrete carriers of that anticipation: framework-core admits the data; extensions (A2A peer adapter per D21) consume it at AgentCard generation time.

### What is NOT in this clarification

- **AgentCard generation contract** — deferred to Phase D when D21 deployability lands; A2A peer adapter (an extension per D16) owns the mapping from specialist.skills → agent-card.skills.
- **Modality vocabulary** — open-ended; framework imposes no enum. Standards-aligned vocabulary (MIME-types; A2A modality conventions) will land at Phase D per D15 standards-compatibility check.
- **Publicly-exposed gating policy** — per-deployment policy (which skills are public when workspace is A2A-exposed); not framework-core concern.
- **MCP-server-exposure parallel** — D21 §"Generalization beyond A2A" names the parallel pattern; D60 scopes to A2A-peer. The MCP parallel uses the same slots with analogous semantics.

## Decision-shape template self-application

- **WHAT**: lock the documentary status of three specialist.skills[] slots as A2A-peer agent-card anticipation. Retroactive clarification; no contract change.
- **WHO**: enforced by **opaque (documentary)** at framework-core — framework admits the slots; runtime ignores. Enforced by **extension (registered)** at Phase D — A2A peer adapter consumes the slots when AgentCard is generated. Enforced by **deferred (Phase D)** for the AgentCard contract itself.
- **FAILS** (recursive — what happens if extension impls misread the documentary intent?): Phase D AgentCard impl would either (a) re-add framework-core validation it should not — caught by D21 refinement-pass standards-compat check or by D60 cross-reference; or (b) leak internal skills via missing `publicly-exposed` honoring — caught by D21's per-skill exposure control requirement.
- **CROSS**: D19 §"Contract slots" (skills[] semantic declaration; D60 clarifies sub-slot intent); D21 §"What this requires from framework-core" + §"What this requires from extensions" (the anticipated consumer); specialist.schema.json:46-51 (schema-locked slots).
- **DEFERS**: AgentCard generation contract (Phase D); modality vocabulary (standards-aligned at Phase D); publicly-exposed gating (per-deployment policy); MCP-server-exposure parallel (D21 §generalization scope).

## E. Pre-lock probe disposition

**SKIPPED** per probing.md Procedure 3 refined skip rule + D45 §E + D46 / D47 / D51 §E precedent: D60 is pure clarification / retroactive lock — no new contract content, no new typed exception, no new category vocabulary, no new sub-procedure. Slots already locked in schema; this entry makes documentary-anticipation status explicit at ledger layer.

## Rationale

D21's framework-core requirements were verified at refinement pass per D15 but never anchored back into a clarification entry naming the specific specialist.skills[] slots as the carriers. The schema added them; readers cross-referencing D19 against the schema today see `input-modalities` / `output-modalities` / `publicly-exposed` without an explicit ledger pointer naming why those three exist (D21 anticipation). D60 closes the trace: D19 (slot contract) → schema (slot encoding) → D21 (anticipated consumer) → D60 (explicit linkage). Append-only ledger discipline preserved.

**Cross-references**: D16 (adapter kind — A2A peer adapter is the extension that consumes these slots at Phase D); D19 §"Contract slots" + skills[] entry (the slot contract this clarifies); D21 §"What this requires from framework-core" + §"What this requires from extensions" + §"Per-skill exposure control" (the load-bearing anticipation); D26 Phase D (lock-time landing phase for AgentCard generation); D45 §E + D46/D47/D51 §E (SKIP precedent for pure clarification); specialist.schema.json:46-51 (the schema-locked slots).

## Honest basis caveats

- **Read directly**: D19 (full); D21 (full); specialist.schema.json:46-51 (three slots verified); D49 + D52 (style references).
- **Inferred from session context**: D15's "standards-compatibility check" — surfaced via D21 referencing D15; D15 not re-read.
- **Inferred from prior-session context**: D16 named as adapter kind for A2A peer adapter — grounded in D21's body, not re-read.
- **Not verified this session**: Phase D landing of AgentCard generation — surfaced by D21 + D26 roadmap.
