# D46 — 2026-05-12 — Extends D7 + D32 — boot procedure honors detection-surface-recovery triad (boot-procedure cluster per D45)

**Decision (substantive; first cluster supersedes per D45 §C)**: The workspace boot procedure (D7 §boot lifecycle + D32 §boot-time resolution + D29 §validation flow) is locked under D45's detection-surface-recovery triad. Three SUSPECT findings from the 2026-05-12 failure-mode + abandonment-path audit are unified here as the **boot-procedure cluster**: (1) silent ValueError swallowing in boot steps 6/7/8 (manifest-declared shape / adapter / specialist with unknown provision-id); (2) manifest-actor seeding mid-cascade rejection has no rollback (introduced in D39 closure work); (3) capability-only substrate-binding error path post-B1 is detected but recovery semantics are implicit. Each path now has detection + surface + recovery explicitly named per D45 §B. First Bref deliverable applying D45 to a runtime path; sets the structural template for cluster supersedes D47-D51.

## A. Scope of cluster

This entry applies the D45 triad to the workspace boot procedure as a unified runtime path. The boot procedure is owned at the contract layer by D7 §3 (state contents) + D7 §4 (composition mutability) + D32 (boot-time resolution: multi-binding satisfiability + circular deps + load order) + D29 §validation flow (B1 conformance gating). Concrete impl in `fresh-plan/impl/src/fresh_plan/runtime/boot.py`.

The three SUSPECT paths from the 2026-05-12 audit unified here:

- **A.1 Steps 6/7/8 silent ValueError swallowing**: when the manifest declares a `provision-id` that has no registered runtime class in the `_SHAPE_CLASSES` / `_ADAPTER_CLASSES` / `_SPECIALIST_CLASSES` registries, `load_*_from_provision` raises `ValueError`. Current impl: `try: ... except ValueError: continue` (boot.py:163-166 shape; boot.py:182-185 adapter; boot.py:202-217 specialist). Symptom: workspace boots successfully; the declared piece is silently absent; downstream code surfaces a misattributed error (e.g., specialist's `attach_workspace` raises "required-adapter-binding has no matching adapter-binding" when the *root cause* is the adapter's unknown provision-id earlier in boot).
- **A.2 Manifest-actor seeding mid-cascade rejection without rollback**: introduced in D39 closure work (boot.py:245-271). For each manifest-declared actor, boot emits a synthetic `composition-change:add` event. If actor #2's seed event is rejected (`EventRejected` from per-event check, schema validation, or shape authority check), the loop's exception propagates. State at failure: actor #1 in state; actors #3..N never seeded; lifecycle:boot event never fires. Workspace half-booted with indeterminate state; caller cannot observe whether this happened.
- **A.3 Capability-only substrate-binding error path post-B1**: when a substrate-binding declares `required-capabilities` only (no explicit `provision`), boot.py:107-119 raises `WorkspaceBootError(category="resolution")`. Detection + surface are CLEAR per the audit; recovery semantics are implicit (caller must add explicit provision; capability-only resolution mechanism is Phase C+ work).

Out of scope (different clusters):

- Authority-binding failures during boot synthetic events (covered by D47 subscriber-dispatch cluster, since they involve shape policy at append-time)
- B1 conformance validator failures pre-substrate-instantiation (already CLEAR per the audit; covered by D29 + D30 timing-modes contract; explicit `WorkspaceBootError(failures[])` already raised)
- Adapter `attach_workspace` runtime failures post-boot-completion (covered by D48 adapter cluster)

## B. Triad applied per path

### B.1 — Steps 6/7/8 unknown provision-id

| Triad element | Lock |
|---|---|
| **Detection** | `ValueError` raised by `load_shape_from_provision` / `load_adapter_from_provision` / `load_specialist_from_provision` when `_<KIND>_CLASSES` registry has no entry for the spec's `id`. |
| **Surface** | Re-raise as `WorkspaceBootError(failures=[ValidationFailure(category="resolution", path="composition.<binding-kind>-bindings[<idx>].provision", value=<provision-ref>, reason="provision <id> has no registered runtime class — manifest declares this binding but the framework cannot instantiate it")])`. Caller sees structured failure naming the offending binding + provision-id. No silent degradation. |
| **Recovery** | Caller fixes the manifest (correct provision-id matching a registered runtime class) and re-boots. Substrate is **not instantiated** (all-or-nothing per D30 boot-time semantics). The framework supplies the diagnostic; the caller supplies the fix. |

### B.2 — Manifest-actor seeding mid-cascade rejection

| Triad element | Lock |
|---|---|
| **Detection** | `EventRejected` (or `MalformedEventError`) raised mid `for actor in manifest_actors: substrate.append_event(seed_event)` loop. |
| **Surface** | Wrap the raised exception → re-raise as `WorkspaceBootError(failures=[ValidationFailure(category="actor-seeding", path=f"composition.actors[{idx}]", value=actor.get("id"), reason=f"actor seeding rejected at index {idx}: {original_msg}")])`. Caller sees which manifest-actor failed + the underlying reason. |
| **Recovery** | Boot is aborted. Substrate object exists (partially populated state: actors 0..idx-1 are in state; actors idx..N are not; no lifecycle:boot event was emitted). The substrate object is **considered partial-and-discardable**: the caller's reference becomes garbage; workspace handle is NOT returned to the caller (the WorkspaceBootError raises before `return workspace`). For the in-process substrate (where there is no separate process to clean up), garbage collection handles the discard. For Phase C+ real-wire substrates, "discard" may require explicit teardown; substrate impls SHALL define teardown semantics on partial-boot failure. |

### B.3 — Capability-only substrate-binding (recovery semantics formalized)

| Triad element | Lock |
|---|---|
| **Detection** | `boot.py:104-116` already detects: `prov_ref = primary_binding.get("provision")` is None when binding declares only `required-capabilities`. |
| **Surface** | Already raises `WorkspaceBootError(failures=[ValidationFailure(category="resolution", path="composition.substrate-bindings[0].provision", reason="substrate-binding lacks an explicit provision; capability-only binding is not bootable in Phase B")])`. |
| **Recovery** | Caller adds an explicit `provision` field to the substrate-binding. Capability-only-resolution mechanism (where the framework picks a substrate impl that satisfies declared capabilities) is **deferred to Phase C+** as an extension to the boot procedure; this entry locks "explicit-provision-required" as the Phase B contract. |

## C. Impl follow-through (separate commit; tracked in roadmap.md)

The contract is locked here; the impl follows in a follow-on commit. Specific changes:

- **boot.py steps 6/7/8**: replace `try: ... except ValueError: continue` patterns with `try: ... except ValueError as e: raise WorkspaceBootError([...]) from e`. Each path constructs a `ValidationFailure` per B.1 above.
- **boot.py manifest-actor seeding loop** (lines 245-271): wrap the loop in `try / except (EventRejected, MalformedEventError) as e:` re-raising as `WorkspaceBootError` per B.2 above. Document partial-state-discardable semantics in the loop's docstring.
- **boot.py capability-only error** (lines 104-116): already conforms; add docstring reference to D46 §B.3 + cross-reference Phase C+ deferral for the capability-only-resolution mechanism.
- **New tests in `tests/test_substrate_boot.py`**: one test per failure path. Each constructs a manifest exercising the failure (unknown shape provision; unknown adapter provision; unknown specialist provision; malformed actor record causing seed rejection; capability-only substrate-binding without provision). Each asserts `WorkspaceBootError` with the expected `failures[].category` + `path` + `reason` shape.
- **Cleanup**: the `actor.get("id") is None: continue` silent drop at boot.py:250 (audit finding) becomes `if aid is None: raise WorkspaceBootError([ValidationFailure(category="actor-seeding", ..., reason="manifest actor lacks id")])`. This is a fourth failure-path covered by the same impl follow-through commit.

Estimated impl size: ~30-50 lines of code change in boot.py + 4-5 new test cases + minor docstring updates.

## D. What is NOT in this decision

- **No change to D7 §3 / §4 contracts** — D7's slot definitions stand. D46 extends D7's runtime semantics around boot-time failure handling without altering the kind contract.
- **No change to D32 contract** — D32's boot-time resolution rules stand. D46 extends D32's failure-mode framing without altering the multi-binding satisfiability or circular-deps or load-order semantics.
- **No new failure-mode categories at framework level** — `WorkspaceBootError` + `ValidationFailure` shape (already locked by D29 + D30) carries everything needed. D46 just standardizes which categories apply per path.
- **No capability-only-resolution mechanism** — explicitly deferred to Phase C+. The substrate runtime registry is currently `_SUBSTRATE_CLASSES` keyed by spec.id; capability-driven instantiation needs framework-level resolution machinery that doesn't exist yet.
- **No change to silent-skip semantics in B1 validator collect-all path** — that's a separate audit finding (validation cluster, D50 candidate). Excluded from this entry's scope despite touching boot adjacency.
- **No automatic rollback of synthetic actor-seed events at the chain level** — partial chain state (actors 0..idx-1 successfully appended; actor idx rejected) is preserved as-emitted per the append-only chain discipline (D10 + D44 chain integrity). The event chain holds what was appended; the workspace handle is what's NOT returned. The chain reflects the failure attempt; it doesn't get retroactively cleaned. Audit-replay of a partial-boot chain shows exactly what happened.
- **No retroactive rewriting of D7 / D32 entries** — append-only ledger discipline. D46 EXTENDS those entries; their original wording stands.

## Decision-shape template self-application (per probing.md Procedure 1)

Eating own dog food, per D45's discipline:

- **WHAT**: lock detection + surface + recovery for the three boot-procedure failure paths identified by the 2026-05-12 audit; first cluster supersedes per D45 §C.
- **WHO**: enforced by *substrate (runtime)* — the boot procedure in `boot.py` raises typed exceptions; the in-process substrate's append path enforces actor-seeding integrity; the Phase B impl owns the implementation. *framework-validator (B1)* gates pre-substrate-instantiation failures via D29 + D30; D46 governs *post-B1* failures (steps 5-9 of the boot procedure per boot.py docstring).
- **FAILS** (recursive — what happens if the boot procedure fails to honor this triad after D46 lands?): *Detection*: failure-mode coverage audit at next workstream-completion or phase-boundary checkpoint catches missing triad implementation; pre-lock probe (Procedure 3) on the impl-follow-through commit's tests catches drift. *Surface*: audit findings list + test failures. *Recovery*: impl-follow-through commit closes the gap; or supersedes entry sharpens the contract if the audit finds the contract itself is wrong.
- **CROSS**: D7 §3 + §4 (workspace state + composition mutability — runtime-affecting; D46 extends boot-time enforcement); D29 §validation flow (B1 timing-mode contract — D46 governs post-B1 failures); D30 §boot-time enforcement (timing-modes table — D46 instantiates boot-time category on resolution path); D32 (boot-time resolution rules — D46 extends with detection-surface-recovery on resolution failures); D34 §A.5 (current-state resolution — D46's actor-seeding cluster preserves this); D39 (state-from-events — D46's actor-seeding rollback semantics preserve replay equivalence); D44 (queued dispatch precedent — D46 mirrors the typed-exception + structured-diagnostic + clean-state pattern); D45 (standing requirement that motivated this entry).
- **DEFERS**: capability-only-resolution mechanism (Phase C+); per-substrate teardown semantics for partial-boot failures in real-wire substrates (Phase C+); retroactive cleanup of partial-chain state from boot rollback (out of scope; chain stays as-emitted per append-only).

## E. Pre-lock probe self-referentiality (skip with documented reason per D45 §E precedent)

Per D45 §E established precedent: pre-lock probe SKIPPED for D46. Reason: this entry is grounded in the 2026-05-12 failure-mode + abandonment-path audit findings (specifically the boot-procedure cluster identified there). Re-probing would be circular — the audit motivated the entry; the entry codifies the audit's recommendation for this cluster; a pre-lock probe would re-derive what we already have. Future audit-driven cluster supersedes (D47-D51) follow the same precedent unless they materially diverge from the audit's framing.

## Rationale

The 2026-05-12 failure-mode audit found D44 was the only runtime decision honoring the failure-mode-as-first-class discipline. The boot procedure was identified as one of the worst offenders — three distinct silent-degradation paths in `boot.py` — partly because the boot procedure has been incrementally extended across multiple D-entries (D7 + D32 + D34 §A.5 + D39 + others) without a single "what's the failure model" lock. D45 established the standing requirement; D46 applies it to boot.

The boot-procedure cluster is intentionally the FIRST cluster supersedes (per D45 §C ordering). Reasons: (a) boot is the most concentrated runtime path in the framework — three distinct SUSPECTs in ~270 lines of `boot.py`; (b) boot-time failures are the most user-visible class — a workspace that boots silently-broken is the worst possible state; (c) boot-procedure cluster is bounded enough to set a clear template for D47-D51 (subscriber-dispatch / adapter / specialist / validation / composition-change clusters); (d) the actor-seeding gap was introduced in our own D39 closure work — it would be intellectually dishonest to leave a gap we just introduced un-addressed while processing pre-existing gaps.

The cluster shape ("apply the D45 triad to this runtime path's failure modes") is the structural template for D47-D51. Each future cluster supersedes will follow this entry's section structure: §A scope of cluster + §B triad applied per path + §C impl follow-through + §D What is NOT + decision-shape template self-application + §E pre-lock probe skip + Rationale + Cross-references.

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): the framework's boot procedure is what every downstream impl + every future substrate must eventually conform to. Locking failure-mode contracts here means Phase C real-wire substrates have a clear bar to meet, not a happy-path-only example to reverse-engineer from.

**Cross-references**: D7 §3 (workspace state — boot establishes initial state); D7 §4 (composition mutability — actor-seeding loop is composition-time); D29 §validation flow (B1 timing-mode contract — D46 governs post-B1 failures); D30 §timing-modes (boot-time enforcement category — D46 instantiates resolution-path); D32 (boot-time resolution — D46 extends with detection-surface-recovery for resolution failures); D34 §A.5 (current-state identity resolution — preserved by D46's all-or-nothing actor-seeding semantics); D39 (state-from-events + actor-seeding loop introduced; D46 closes the abandonment-path gap that closure work introduced); D44 (queued dispatch precedent — D46 mirrors typed-exception + structured-diagnostic + clean-state pattern); D45 (standing requirement that motivated this cluster supersedes; canonical citation); 2026-05-12 failure-mode + abandonment-path audit (motivating evidence; boot-procedure cluster identified there).
