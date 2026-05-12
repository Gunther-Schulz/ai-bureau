# D36 — 2026-05-09 — Phase B planning: workstream order + setup decisions + closure criterion

**Decision**: Phase B (reference impl of core, per D26) is planned with a workstream order, setup decisions (branch / language / repo layout), and an explicit closure criterion. Analog of D27 for Phase B. Decision is intentionally a single planning lock covering structure + setup (rather than three separate entries) for density management.

### A. Phase B workstream order

Eight workstreams, with dependencies. Order is indicative not rigid per D26 caveat — phase boundaries are trigger-based.

| # | Workstream | Depends on | One-line |
|---|---|---|---|
| **B1** | Conformance validator | — | Impl of D29 §validation flow + D30 + D32; validates extension manifests, workspace manifests, runtime references. Foundation; everything else depends on it. |
| **B2** | Substrate impl | B1 | Claude Agent SDK as the reference substrate per D12; advertises core abstract capabilities (`hooks`, `skills`, `event-streaming`). |
| **B3** | Generic minimal shape impl | B1 | Per D26: explicitly NOT practitioner-shape (pioneer-instance bias). Neutral shape exercising D13's slots. |
| **B4** | Minimal MCP-server-protocol adapter | B1, B2 | Validates the MCP adapter pattern + the registered protocol identifier (per D16). |
| **B5** | Minimal direct-api adapter | B1, B2 | Validates the non-MCP adapter path (per D16). |
| **B6** | Minimal specialist | B1, B2, B4 | Exercises D19 slots; binds to B4 adapter to demonstrate `required-adapter-bindings`. |
| **B7** | Minimal RAG-via-MCP impl | B4, B6 | Per D26: specific case of B4 pattern; validates retrieval-shaped extension. |
| **B8** | End-to-end scenario | all above | Workspace manifest exercising all 8 kinds boots + runs a scripted scenario. |

B3, B4, B5 can run in parallel after B1 + B2.

### B. Setup decisions

**B.1 — Branch strategy**: `fresh-plan` is the canonical development branch. The current session is constrained to push to `claude/identify-repo-S5zfO` by session policy; this is a session-specific quirk, not the canonical convention. Future sessions resume pushing to `fresh-plan` as the canonical record. (Closes D26's deferred "branch / commit strategy" item.)

**Commit policy**: each substantive lock = one commit, descriptive message; push after commit (no manual confirmation per the README working preferences). Branch protection / merge policy / PR review = TBD when the project has more contributors; not load-bearing for solo development.

**B.2 — Language / stack**: **Python primary** for the reference impl. Reasons:

- Claude Agent SDK is Python-native (per D12 "likely Claude Agent SDK" framing).
- JSON Schema toolchain is mature in Python (`jsonschema` library, used by the Phase A validation tests).
- Most agent-ecosystem tooling (MCP servers, A2A peer libraries) has good Python support.
- Dependency management: `pyproject.toml` + `uv` (current ecosystem standard; fast resolver).

Other languages are not ruled out — a TypeScript second-impl pass in Phase E (multi-deployment validation) is plausible if shape-neutrality evidence demands cross-language demonstration. Phase B itself is Python.

**B.3 — Repo layout**: monorepo. Code lives in `fresh-plan/impl/` alongside `fresh-plan/schemas/` and `fresh-plan/decisions.md`. Specifically:

```
fresh-plan/
  README.md
  decisions.md
  schemas/                <- Phase A formal schemas (locked at D35)
  impl/                   <- Phase B reference impl (this workstream)
    pyproject.toml
    src/                  <- Python package(s)
    tests/                <- pytest tests
    scenarios/            <- end-to-end scripted scenarios (B8)
```

Single repo, single history; cross-reference between ledger / schemas / code is straightforward. Splitting into separate repos is reversible if the project ever needs it.

### C. Closure criterion

Per D26's Phase B closure trigger ("reference impl boots and runs a minimal scenario end-to-end through all 8 kinds"), B8 must demonstrate:

- Workspace manifest declares 1 shape, ≥1 substrate-binding, ≥1 adapter-binding, ≥1 specialist-binding, ≥1 actor — exercising D7's composition cardinalities.
- Workspace boots via D29 validation flow; conformance validator (B1) passes all D30 + D32 checks.
- Scripted scenario emits ≥1 event of each core payload-subtype (claim, action, state-change, composition-change, lifecycle-transition) — exercising D10 + payload schemas.
- ≥1 work-unit of an extension-registered `kind` is created, transitions through ≥2 lifecycle states (e.g., `created` → `in-progress` → `completed`).
- Conformance validator (B1) accepts the events + work-unit references at runtime.
- All Phase A schemas (D35 inventory) are exercised at least once during the scripted run.

Scope is "smallest thing that exercises all 8 kinds end-to-end and doesn't crash." No PBS-Schulz domain content — pioneer-instance is Phase D.

### D. Discipline

- **Refinement-pass discipline carries forward** per D14 / D24 / D34. End-of-Phase-B refinement pass before closure entry.
- **Append-only ledger**, one substantive decision per entry, supersedes-pattern for changes (same as Phase A).
- **Tier model** (per session working agreement): tier 1 (direct execution) for mechanical / routine work; tier 2 (summary review at workstream boundaries) for batched implementation work; tier 3 (pre-lock review) for substantive new decisions.
- **Sub-agent dispatch** for substantive new design questions or large-artifact production where fresh-context judgment is genuinely valuable; main-session for mechanical encoding work and routine commits.

### E. What is NOT in this decision (deferred to per-workstream entries or implementation)

- Specific Python package layout (one package or multiple? namespace package? — `src/` choice noted but internals TBD).
- Specific test framework choice (probably pytest, but not load-bearing).
- CI / lint / formatter setup — implementation per D11.
- Documentation strategy for the impl (separate docs site? inline? — TBD).
- Reference-impl versioning policy specifics — follows D33 versioning.
- Forward compatibility between Phase B impl and future Phase C/D extensions — Phase C concern.

**Rationale**: Phase B is qualitatively different from Phase A — implementation, not architecture. Setup decisions (branch, language, layout) need to be in the ledger because they shape the impl trajectory; per-workstream content (specific class hierarchies, function signatures, test scaffolding) is implementation per D11 and doesn't need ledger entries beyond per-workstream completion summaries.

Single D36 covering workstream order + setup + closure (rather than three entries) reflects that Phase B planning is one coherent moment. Splitting would create artificial seams between decisions that depend on each other (e.g., "monorepo layout" assumes "Python primary" which assumes "Claude Agent SDK is the reference substrate").

**Cross-references**: D14 (refinement-pass discipline); D26 (Phase B scope + closure trigger + deferred branch-strategy item); D27 (analog of this entry for Phase A); D29 + D30 + D32 (validator B1 implements these); D35 (Phase A closure; B1 builds on the artifact inventory there).
