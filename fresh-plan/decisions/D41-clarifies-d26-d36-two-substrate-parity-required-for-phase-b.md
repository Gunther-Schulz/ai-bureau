# D41 — 2026-05-11 — Clarifies D26 + D36 — two-substrate parity required for Phase B closure

**Decision (clarifies D26 + D36)**: Phase B closure requires **two diverse substrate stubs** passing the B1 conformance validator, not just one. The existing `inprocess-substrate-ext` (B2) is a substrate-shaped Python harness; it does not on its own prove that D17's abstract capability vocabulary (`hooks`, `skills`, `event-streaming`) is genuinely substrate-neutral rather than Claude-SDK-flavored. A second stub modelled on a structurally distinct framework — currently proposed: Microsoft Agent Framework — exercises D17 against a real second cognitive frame. Substitute is admissible if a more divergent second substrate surfaces (e.g., LangGraph, Semantic Kernel) — the load-bearing requirement is *diversity*, not the specific framework.

### Workstream addition

- **B2b — MS Agent Framework substrate stub.** Mirrors B2's structural shape (no real wire; stubbed loop), but mapped to MS Agent Framework's concepts (workflow / orchestration / agent composition primitives). Advertises the same three core abstract capabilities (`hooks`, `skills`, `event-streaming`) per D17. Boots cleanly through the B1 validator's capability satisfaction checks. Lives at `impl/extensions/ms-agent-framework-substrate-ext/0.1.0/`.
- B2b runs in parallel with B6 / B7 / B8; not blocking. Required before Phase B closure entry.

### Closure-criterion update for D36 §C

D36 §C "Workspace manifest declares 1 shape, ≥1 substrate-binding, ≥1 adapter-binding ..." now reads: **≥1 substrate-binding in B8 end-to-end fixture, AND ≥2 distinct substrate stubs (`inprocess-substrate-ext` + `ms-agent-framework-substrate-ext` or equivalent) shipped at `impl/extensions/` and passing B1 conformance independently**. The end-to-end B8 scenario does not need to swap substrates mid-run; the parity requirement is at the artifact level.

### Cross-tension as the test

If writing B2b reveals that `hooks` / `skills` / `event-streaming` map awkwardly onto MS Agent Framework's primitives, D17 is leaning Claude-flavored and needs sharpening — either by renaming the capabilities or by demoting any that don't translate to extension-registered status (same pattern as D17's original supersedes of D12's `mcp-client` / `a2a`). The sharpening is end-of-Phase-B refinement work (per D14 / D34 pattern); the surfacing happens during B2b authoring.

If B2b maps cleanly, D17 is substantiated as substrate-neutral; the parity test passes; Phase B can close without D17 changes.

**Rationale**: per the "Generic vs pioneer-instance discipline" (Working pattern), generic exemplars must be *demonstrably* generic, not just structurally promised to be. One stub is structural promise; two diverse stubs is demonstrated property. Same logic underlies Phase E's multi-deployment-validation premise (D26): shape-neutrality is proven by a second shape impl, not by the first. D41 applies that logic one phase earlier to substrate-neutrality, where the cost of a stub-pair is low and the alternative (discovering D17 is Claude-flavored only at Phase C real-wire impl) is high.

**Cross-references**: D12 (substrate kind); D17 (capability vocabulary; the contract being tested); D26 (Phase B scope; clarified here); D36 (Phase B planning; §C closure criterion updated here); D14 + D34 (refinement-pass discipline; sharpening is end-of-Phase-B work); generic-vs-pioneer-instance Working pattern (the same logic applied at substrate layer).
