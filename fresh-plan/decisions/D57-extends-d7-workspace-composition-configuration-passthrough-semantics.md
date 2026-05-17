# D57 — 2026-05-17 — Extends D7 — workspace.composition.*.configuration pass-through semantics

**Decision (substantive; extends D7)**: The four `configuration` slot-instances declared on D7 §2 composition bindings (`composition.shape.configuration`, `composition.substrate-bindings[i].configuration`, `composition.adapter-bindings[i].configuration`, `composition.specialist-bindings[i].configuration`) are locked under a **single pass-through contract**: the framework treats each `configuration` dict as opaque, performs no shape validation beyond the JSON Schema `{"type": "object"}` constraint (workspace.schema.json:54 / :83 / :105 / :120 — verified), and threads the dict unchanged to the kind-specific runtime constructor at boot. The kind-runtime owns interpretation; framework owns conveyance. Failure shape per D45 detection-surface-recovery triad: kind-runtime constructor rejection raises a kind-specific exception → framework catches at the construction call-site → re-raises as `WorkspaceBootError(category="configuration-rejected", path=...)` carrying the kind-specific cause via `from`. One shared category (not four), per D45 minimality. Analog: HTTP headers — framework conveys, endpoint interprets.

## A. Scope

**Honest cardinality: 1 contract, 4 slot-instances.** The contract (pass-through semantics + rejection-surface) is uniform across all 4 instances; the instances differ only by *which kind-runtime constructor* receives the dict. Per probing.md "Pattern-completion failure mode" + D49 first-pass lesson + D50/D52 honest-1-path precedent: this is ONE entry with ONE triad applied uniformly.

The 4 slot-instances (workspace.schema.json lines V1-verified):

1. `composition.shape.configuration` — workspace.schema.json:54 — threaded to Shape runtime constructor at boot.py:170-187.
2. `composition.substrate-bindings[i].configuration` — workspace.schema.json:83 — threaded to Substrate runtime constructor at boot.py:133-140.
3. `composition.adapter-bindings[i].configuration` — workspace.schema.json:105 — threaded to Adapter runtime constructor at boot.py:203-219.
4. `composition.specialist-bindings[i].configuration` — workspace.schema.json:120 — threaded to Specialist runtime constructor at boot.py:239-256.

Out of scope (per §D):
- Schema-per-configuration (per-kind JSON Schemas) — D-1.
- Framework-level validation policy — D-2.
- In-place reconfiguration / hot-reload — D-3.
- Cross-kind shared configuration — D-4.
- Configuration inheritance / composition — D-5.
- Deferred-interpretation configurations — D-6.

## B. Triad applied per path (uniform across 4 instances)

### B.1 — `configuration` pass-through + rejection surface

| Triad element | Lock |
|---|---|
| **Detection** | Kind-runtime constructor receives the `configuration` dict (or `None` when slot omitted — schema does not mark required at any of the 4 instances). Constructor interprets per its own contract and raises a kind-specific exception when the dict shape does not satisfy expectations. Framework does NOT validate dict shape — only schema-level `{"type": "object"}` enforced by B1. |
| **Surface** | At each construction call-site, kind-construction wrapped in `try / except Exception as e: raise WorkspaceBootError([ValidationFailure(category="configuration-rejected", path=f"composition.<slot>.configuration", value=<kind-id>, reason=f"<kind> runtime rejected configuration: {e}")]) from e`. Kind-specific exception preserved via `from` chaining. NEW `FAILURE_CATEGORIES` entry `"configuration-rejected"`. No silent substitution per CLAUDE.md (no try/except: configuration={} fallback). |
| **Recovery** | Caller fixes the offending `composition.<slot>.configuration` and re-boots. Boot is all-or-nothing per D30 + D46 §B.1 precedent. |

**Category choice — ONE shared `configuration-rejected` (not four)**: per D45 minimality. Four slot-instances differ only in which kind-runtime interprets; the *failure shape* (kind-runtime rejected its configuration) is one category. `path` field discriminates which slot; `value` field discriminates which kind-id; chained exception carries kind-specific detail. Four separate categories would inflate `FAILURE_CATEGORIES` without adding caller-observable distinctions beyond `path`.

**Quiet assumption surfaced**: this lock assumes the kind-runtime's interpretation is purely constructor-time. Kind-runtimes that defer interpretation (lazy / first-use evaluation) fall outside this contract; surface deferred to D-6.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

- **boot.py shape construction** (170-187): pass `configuration=composition["shape"].get("configuration")` to `load_shape_from_provision`. Wrap kind-construction `try / except` with `category="configuration-rejected"` if cause is NOT a `ValueError` from registry-lookup (which already gets `category="resolution"` per D46 §B.1). Discrimination: registry-miss ValueError (shape.py:300-304 `cls is None` branch) stays "resolution"; configuration-rejection from `cls(spec=spec, configuration=...)` constructor call becomes "configuration-rejected". Same discrimination for adapter (203-219) + specialist (239-256).
- **boot.py substrate construction** (133-140): `load_substrate_from_provision` already takes explicit kwargs. Add `configuration=primary_binding.get("configuration")` kwarg + thread to `cls(...)` call.
- **Loader signature update** for `load_shape_from_provision` (shape.py:289-305) / `load_adapter_from_provision` (adapter.py:232-249) / `load_specialist_from_provision` (specialist.py:295-311) / `load_substrate_from_provision` (substrate.py:390-417): each gains `configuration: Optional[dict] = None` kwarg + threads to `cls(spec=spec, configuration=configuration)`.
- **Phase B existing runtimes — configuration kwarg acceptance**: Shape / Adapter / Specialist / Substrate base classes gain `configuration: Optional[dict] = None` as dataclass field. Phase B stubs hold but ignore; Phase C+ real-wire impls read. Honest naming — field IS present; Phase B impls choose not to use it.
- **New `FAILURE_CATEGORIES` entry**: `"configuration-rejected"` in `validator/types.py` with inline comment naming D57 §B.1 origin.
- **4 new tests** in `impl/tests/test_configuration_passthrough.py` (NEW file): MonkeyPatched `_FailingShape` / `_FailingAdapter` / `_FailingSpecialist` / `_FailingSubstrate` subclasses raising from constructor on sentinel `configuration` value. Each test boots manifest declaring that configuration + asserts `WorkspaceBootError(category="configuration-rejected", path=...)` with underlying exception chained.

Estimated impl size: **~25 LOC + 4 tests**. 195 baseline → 199 tests post-D57 [impl].

## D. What is NOT in this decision

- **D-1 — Schema-per-configuration (kind-specific JSON Schemas)**: per-kind JSON Schemas constraining dict shape (e.g., MCP adapter's `configuration` MUST have `endpoint: string`). D57 treats dict as opaque at framework level; per-kind schema layering is extension-defined per D29 namespacing + kind-runtime's own contract.
- **D-2 — Validation policy (when configuration is "malformed")**: D57 declines to constrain *what* the kind-runtime checks. Strict / lazy / never is per-kind-runtime choice; framework only requires the rejection-wrap if constructor raises.
- **D-3 — In-place reconfiguration / hot-reload**: D57 scopes to boot-time threading. Mid-lifecycle reconfiguration is Phase C+. Composes with D52 §D D-4 (composition-change `change-type=update` deferred).
- **D-4 — Cross-kind shared configuration**: one dict feeding multiple kind-runtimes. D57 locks per-slot ownership; cross-kind sharing would need a separate slot or named-reference mechanism.
- **D-5 — Configuration inheritance / composition**: extension declares defaults + manifest overrides per-instance + boot merges. D57 treats manifest's dict as authoritative; no merging from extension defaults.
- **D-6 — Deferred-interpretation configurations**: kind-runtimes deferring interpretation past constructor-time. D57's rejection surface fires only at construction-time. Deferred-interpretation failures surface through other paths (skill execution per D50; adapter call per D48; on_event per D47).

Other items NOT in this decision:

- **No retroactive rewrite of D7** — append-only ledger.
- **No constraint on per-kind exception types** — kind-runtimes choose per their own contract.
- **No new typed exception at framework level** — reuses `WorkspaceBootError` + adds category entry only.

## Decision-shape template self-application

- **WHAT**: lock pass-through semantics + rejection-surface contract for the 4 `composition.*.configuration` slot-instances.
- **WHO**: enforced by *substrate (runtime)* — boot procedure wraps each kind-construction call at the 4 named call-sites; *kind-runtime (per-kind impl)* — Shape / Adapter / Specialist / Substrate constructors interpret per their own contract; *framework-validator (B1)* — unaffected beyond existing `{"type": "object"}` check.
- **FAILS**: *Detection*: audit at next checkpoint catches missing wrap. *Surface*: audit findings + test failures. *Recovery*: impl-follow-through commit closes; or supersedes entry sharpens.
- **CROSS**: D7 §2 (extends — runtime semantics for `configuration` sub-slot; slot contract unchanged); D29 (validation flow — B1 enforces schema-level only); D30 (boot-time enforcement; all-or-nothing semantics); D45 (standing requirement; canonical citation); D46 §B.1 (precedent for WorkspaceBootError + ValidationFailure + from-chaining + per-call-site try/except wrap); D48 §B.1 (precedent for runtime-call failure category — distinct lifecycle from D57's construction-time); D48 §B.2 (`adapter-attach` precedent); D50 §B.1 + §E (Phase C+ forward-bar when Phase B stubs don't exercise); D52 §B.1 (FAILURE_CATEGORIES extension for uniform failure shape — `configuration-rejected` parallels `composition-validity`).
- **DEFERS**: per §D — D-1 through D-6.

## E. Pre-lock probe disposition

D57 **FIRED** per refined-skip rule + D48 §E + D50 §E + D52 §E precedent. NEW contract content:

1. **New contract surface** — pass-through semantics for the 4 instances (D7 silent; D57 establishes).
2. **New `FAILURE_CATEGORIES` entry** — `"configuration-rejected"`.
3. **New constructor signatures** — Shape / Adapter / Specialist / Substrate base classes gain `configuration` field.

**Probe outcome (V1-verified during drafting)**: 4 construction sites verified at boot.py:133-140 / 170-187 / 203-219 / 239-256. 4 constructor signatures verified — Shape (shape.py:39-48 dataclass `spec: dict` only); Adapter (adapter.py:67-79); Specialist (specialist.py:72-86); Substrate.load (substrate.py:390-417 explicit kwargs, no `configuration`). FAILURE_CATEGORIES at types.py:22-39. D7 silent on configuration semantics (Read full). Quiet assumptions surfaced + named as §D D-1 through D-6.

## Rationale

D7 §2 enumerates the 4 composition binding kinds + names a `configuration` slot at each, but is silent on what the framework does with the dict. workspace.schema.json admits `{"type": "object"}` — no further constraint. The current Phase B impl threads NOTHING: 4 kind-construction call-sites ignore the dict entirely. This is the canonical silent-substitution anti-pattern at structural layer — manifest declares config; framework accepts at B1 schema-level; dict goes nowhere; kind-runtime never sees it. D57 closes the gap.

Contract choice — opaque pass-through, framework conveys, kind-runtime interprets — matches HTTP-headers analogy. Per the durability bet: the contract (configuration is opaque pass-through; rejection as `WorkspaceBootError(category="configuration-rejected")`) is what every Phase C+ kind-runtime must conform to. Per-kind schemas + validation policies + inheritance mechanisms are scaffolding layered on top.

Honest cardinality: ONE entry covering 1 contract × 4 instances. Per probing.md scope-cardinality-honesty: do NOT split into 4 D-entries; do NOT mirror D46/D48's 3-path multi-path structure. The 4 instances share ONE triad.

## Honest basis caveats

- **Read directly**: README + CLIPPY-COMPANION + probing.md + D07 (note: zero-padded filename) + D45 + D46 + D52 + workspace.schema.json (4 configuration slots verified) + boot.py (4 construction sites verified) + shape.py / adapter.py / specialist.py / substrate.py (constructor signatures verified) + validator/types.py.
- **Cited but not freshly re-read**: D47/D48/D50 entries — load-bearing cross-references inferred from D52's cross-citations. D48 §B.1 vs D48 §B.2 distinction (runtime-call vs attach) carried over from D52 summary. Should be Read-verified before impl commit.
- **Inferred**: "add field to dataclass" recommendation for Phase B existing runtimes is impl-design choice not yet user-confirmed; test count "199 post-D57 [impl]" arithmetic only.
