# D22 — 2026-05-08 — Refinement: D9 substrate-binding resolution clarified

**Decision (clarifies D9)**: An `agent-actor`'s `substrate-binding` slot resolves to a **binding-id within `workspace.composition.substrate-bindings[]`**, not to a bare `substrate-id`. This makes the reference precise when a workspace has multiple bindings of the same substrate-id (e.g., one binding in `interactive` runtime-shape for daily work + another in `programmatic` runtime-shape for cron tasks — concrete example from D12 discussion).

**Why this is a clarification, not a substantive supersede**: D9's intent was "agent-actor identifies which substrate runtime hosts its execution"; the wording "references a substrate declared in workspace.composition" was loose because workspace.composition can have multiple bindings to the same substrate. The refinement makes the reference precise. Semantics unchanged; phrasing sharpened.

**Cross-references**: D7 §4 substrate-binding cardinality (multiple bindings allowed); D12 binding-resolution discussion.
