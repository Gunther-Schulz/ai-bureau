# D43 — 2026-05-11 — Supersedes D17 — rename core capability `event-streaming` → `event-chain`

**Decision (supersedes D17 — core capability vocabulary)**: The core abstract capability previously named `event-streaming` is renamed to `event-chain`. Semantic is unchanged from D17 + D40 §A: the substrate hosts an append-only ordered event chain (D10) with the minimum projection / query interface (D40 §A) and integrity-mechanism extension point (D40 §B). The rename eliminates a misleading framing — "streaming" in modern AI parlance suggests SSE-style live runtime delta streaming (LLM token streams, partial agent output deltas), whereas fresh-plan's actual usage is event-sourcing / checkpointing semantics. Surfaced concretely during B2b authoring: MS Agent Framework distinguishes `AgentRunResponseUpdate` (live runtime deltas) from `Checkpoint` (event sourcing); fresh-plan's capability maps to the second, not the first, and the prior name pulled readers toward the first. First Bref deliverable producing a standalone D-entry per D42.

### Revised core capability vocabulary (supersedes D17 §"Revised core capability vocabulary")

The framework-core declares these capabilities. The principle from D17 stands: *a capability is at core iff a core kind contract references it*.

- **`hooks`** — substrate exposes hook points for shape policies / discipline enforcement. Referenced by shape kind (D13). Unchanged.
- **`skills`** — substrate can load specialist bundles. Referenced by specialist kind (D19). Unchanged.
- **`event-chain`** — substrate hosts the workspace event chain (D10) with the minimum projection / query interface (D40 §A) and integrity-mechanism extension point (D40 §B). Renamed from `event-streaming`; semantic unchanged.

### Cascade applied in same commit

Per D34 §A.4 precedent (D17's own demotion was operationally breaking and accepted because no third-party impls existed yet): same reasoning applies — Phase B is post-Phase-A but still pre-Phase-C-real-wire, no third-party extensions exist that would break. All in-tree usages updated together. Append-only ledger entries (D12 + D16 refinement + D17 + D36 + D40 + D41 references) retain prior wording — `event-chain` is canonical going forward; prior references read as the same concept under prior naming.

- Schemas: `_common.schema.json` (capability-identifier enum), `substrate.schema.json` (description), `extension-manifest.schema.json` (description).
- Worked examples: `schemas/examples/` substrate / specialist / shape files.
- Impl extensions: substrate / shape / specialist `.json` files in `impl/extensions/` + 11 fixture copies in `impl/tests/fixtures/`.
- Impl source: `validator/checks.py` (CORE_CAPABILITIES frozenset + docstring), `runtime/substrate.py` (docstring).
- Tests: `test_specialist.py`, `test_substrate_boot.py`, `test_ms_agent_framework_substrate.py`, `test_rag_specialist.py`, `test_shape.py`.
- Narrative docs: `CONCEPTS.md`, `impl/README.md`.

164 tests pass under the renamed vocabulary.

### Alternatives considered + rejected

- **Split into two capabilities** (`event-chain` for event-sourcing/checkpointing + `event-streaming` for runtime-delta streaming). Rejected: per D17's principle, no core kind contract references runtime-delta streaming; live-delta streaming is a UX-layer concern (adapter / specialist surfacing deltas to humans), not a substrate property in the I3 / D10 sense. Substrates that genuinely surface runtime deltas can extension-register a capability under their own namespace per D29 (e.g., `claude-sdk-ext:runtime-deltas`).
- **Rename to `event-sourcing`**. Rejected: term carries Greg-Young / CQRS architectural baggage (projections-as-tables, snapshots-vs-replay, etc.) that invites readers to assume specific tooling. `event-chain` is more neutral and matches D10's existing vocabulary throughout.
- **Keep `event-streaming` and document the scope**. Rejected: rests on documentation discipline; misleading name remains a trap for every reader. Cleanup cost is bounded NOW (~46 in-tree locations); grows with every Phase C real-wire substrate adoption.

### Versioning impact (per D33)

Per D33 §A: this is a major bump on D17's contract (the core capability vocabulary changed). Per D33 §B: the substrate kind contract is similarly affected (`capability-identifier` enum lost a value, gained a value). Per D34 §A.9: kind-contract versions are advisory descriptors of supersede magnitude in the ledger narrative (not operationally consumed by the boot validator at present); D43 tracks as a major bump in that narrative sense.

### What is NOT in this decision

- **No new capability added**. The three-capability core (`hooks`, `skills`, `event-chain`) remains. No `event-streaming` (or runtime-delta-streaming) capability is added as a separate concept.
- **No change to D40 §A (minimum query interface)**. The interface contract attaches to `event-chain` unchanged from how it attached to `event-streaming`.
- **No change to D40 §B (integrity-mechanism extension point)**. Integrity protocols (AEGIS, Axon, etc.) still register against substrates advertising the renamed capability.
- **No deprecation alias** (`event-streaming` is not retained as a synonym). Per D34 §A.4 reasoning, no third-party extensions exist that would break; clean rename.
- **No retroactive edit of D12 / D16 / D17 / D36 / D40 / D41** (append-only ledger; references to `event-streaming` in prior entries stand under their original wording).

**Rationale**: per the durability-framing pattern (CONCEPTS "What is durable vs scaffolding"), the framework is primarily a *specification* — naming choices in the spec compound across every reader and every downstream impl. A misleading core-vocabulary name is an asymmetric cost: low-effort to fix now, increasingly expensive as the spec is adopted. B2b authoring's surfaced confusion (per D41 cross-tension) is exactly the signal D41 anticipated; the resolution is a rename rather than a documentation patch precisely because the spec is the durable contribution. Per D17's own precedent (renaming / demoting to align with strict D2 protocol-neutrality), the framework is not afraid to sharpen its vocabulary when concrete authoring surfaces a mismatch.

**Cross-references**: D10 (event chain — the artifact this capability hosts); D12 (substrate kind contract — capability vocabulary slot); D17 (core capability vocabulary — superseded for `event-streaming` slot); D33 §A + §B (versioning policy — major bump on D17 contract); D34 §A.4 + §A.9 (operationally-breaking demotion precedent + kind-contract-version advisory status); D40 §A + §B (minimum query interface + integrity-mechanism extension point — both attach to renamed capability unchanged); D41 (B2b two-substrate parity — what surfaced this); D42 (Bref — this is a Bref deliverable per the workstream).
