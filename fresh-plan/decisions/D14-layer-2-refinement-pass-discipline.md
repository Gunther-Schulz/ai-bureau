# D14 — 2026-05-08 — Layer 2 refinement-pass discipline

**Decision**: After layer-2 enumeration completes (per D6 step 3), a **refinement pass** sweeps all locked kind decisions before layer 2 is declared closed. The pass produces supersedes / clarification entries for any kinds needing sharpening.

### Pass criteria

For each locked kind decision (D7, D9, D10, D12, D13, and remaining kinds), review against:

- **Cross-kind consistency** — slot-naming conventions, required / optional discipline, cross-reference resolution (e.g., does an actor's `substrate-binding` resolve to a substrate-id or a binding-id? D12 surfaced this; D9 should be sharpened to match).
- **Late-emerging patterns** — patterns articulated after a kind was locked, applied retroactively where applicable. Examples already surfaced:
  - D13's **required-with-explicit-empty / explicit-none** pattern (forces author to consider each slot rather than silently omit) — review earlier kinds' optional slots for retroactive fit.
  - D11's **semantic-contract vs formal-schema vs format** distinction — sharpen any prior wording that conflated them.
- **Downstream tensions** — issues surfaced when later kinds referenced earlier ones.

### Outputs

- **Supersedes entries** for substantive revisions (per ledger discipline; new entry that explicitly supersedes the prior).
- **Clarification entries** for non-semantic phrasing sharpenings.
- **Confirmed-as-locked notes** for entries that pass review unchanged.

### Procedure update to D6

D6 step 4 (closure) is split:
- **4a**: enumeration completion check (top-down + prior-list sweep done).
- **4b**: refinement pass per this discipline.
- **4c**: closure entry naming the final kind set, marking layer 2 done.

**Rationale**: each kind was decided in isolation but kinds cross-reference. Late-emerging patterns deserve uniform application. Cross-cutting consistency only becomes visible with the whole layer in view. Locking this discipline before remaining kinds prevents accumulating entries under the false assumption "we won't re-touch these"; explicitly named refinement-as-phase prevents the pass being skipped or treated as ad-hoc cleanup.
