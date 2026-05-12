# D42 — 2026-05-11 — Clarifies D14 + D36 — formalize Bref as named Phase B refinement workstream

**Decision (clarifies D14 + D36)**: Phase B's end-of-phase refinement per D14 is formalized as a named workstream **Bref**, with currently-tracked deliverables surfaced as workstream scope + a closure output D-entry analogous to D34 (Phase A's refinement output). Reason: D36 §D's implicit phrasing ("refinement-pass discipline carries forward per D14 / D24 / D34. End-of-Phase-B refinement pass before closure entry") under-counts the work; the deliverables list grew enough through B1–B6 that surfacing it as a workstream with tracked scope serves the work better. Matches D34 precedent (Phase A's refinement was substantial enough to warrant its own D-entry output).

### Bref scope

Eight tracked deliverables at D42 lock-time (canonical tracking list maintained in `CONCEPTS.md` open-questions; will grow as B7 / B8 surface more): D39 out-of-band-state tensions; D17 capability-vocabulary sharpening if B2b surfaces Claude-flavored bias; D38 Sana-style worked-example validation; D19 activation-scope DSL design; `boot.py` step-3 duplication cleanup; D37 subscriber-dispatch reentrancy / loop semantics; D33 migration-safety discipline for shape versioning; `decisions.md` split into per-entry files. Plus standalone candidate clarification entries that may emerge during Bref: actor identity-binding spec slot, live in-place shape migration deliberate scope-cut, positioning lock (pending source-grounded Bucket A platform reads).

### Position in workstream order

Bref runs between **B8** (end-to-end scenario; closure trigger) and the **Phase B closure entry**. May overlap with late B8 work if findings surface during B8 authoring. Output is one substantive D-entry analogous to D34 — captures cross-cutting findings + supersedes / clarification entries that emerged + closes off with a list of validated-or-deferred items.

### Closure-criterion update for D36 §C (extends D41)

Phase B closes when: (a) B8 end-to-end fixture passes; (b) two-substrate parity per D41 is shipped; (c) **Bref output entry is locked** (cross-cutting refinement findings resolved or deferred with explicit homes).

**Cross-references**: D14 (refinement-pass discipline at phase boundaries); D26 (Phase B scope); D34 (Phase A refinement output — structural precedent); D36 (Phase B planning; §C closure criterion updated again here); D41 (two-substrate parity; another D36 amendment).
