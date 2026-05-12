# D50 — 2026-05-12 — Extends D19 — specialist cluster honors detection-surface-recovery triad (per D45 §C)

**Decision (substantive; fourth cluster supersedes per D45 §C; SkillExecutionError forward-bar)**: The specialist runtime path — specifically `handle_skill` failure shape (the remaining D45 §C item 4 SUSPECT after D47 §B.1 closed the on_event exception path) — is locked under D45's detection-surface-recovery triad. New typed exception `SkillExecutionError` introduced for Phase C+ real-wire specialist body failures. Phase B specialist stubs (GenericSpecialist + RAGSpecialist) do NOT trigger the contract — their failure modes are Python idioms (pre-condition guards; dispatch-miss `NotImplementedError`) per second-pass scope correction; refactoring them would inflate ledger scope per D49 first-pass-pattern-completion lesson. Cluster is honestly smaller than D46/D47/D48 (1 SUSPECT vs 3 each); pre-lock probe FIRED per D48 §E precedent (D50 introduces new contract content: SkillExecutionError type + category vocabulary); 5 quiet assumptions surfaced + named as §D explicit deferrals.

## A. Scope of cluster

D45 §C item 4 named TWO specialist SUSPECTs: (a) `handle_skill` failure shape unspecified; (b) `on_event` exception path. D47 §B.1 explicitly closed (b) via subscriber-dispatch capture into `_subscriber_failures` + aggregation as `SubscriberDispatchError` after outer drain. **D50 addresses (a).**

Honest cluster cardinality: D50 covers 1 SUSPECT. The Phase B pre-condition guards in `specialist.py` (GenericSpecialist not-attached at `specialist.py:169-172`; RAGSpecialist not-attached at `:197-200`; RAGSpecialist dispatch-miss `NotImplementedError` at `:201-204`; RAGSpecialist required-adapter-not-bound at `:209-213`) are Python idioms for programming-time invariant violations, not runtime failure modes that callers programmatically handle — D50 does NOT refactor them (per D49 first-pass scope-inflation lesson; § "What is NOT" below names this explicitly).

The path covered here:

- **A.1 `handle_skill` failure shape (Phase C+ real-wire forward-bar)**: Phase B specialists (`specialist.py:144-160` GenericSpecialist + `specialist.py:176-235` RAGSpecialist) `handle_skill` bodies emit stub action events + return canned responses — no meaningful failure modes at Phase B. Phase C+ real-wire specialists (practitioner-specialist in Phase D; specialists wrapping real domain logic) WILL fail meaningfully: domain-validation rejection, external-dependency unavailable, runtime invariant violation. D50 locks the forward-bar: real-wire impls SHALL raise `SkillExecutionError` (NEW typed exception) on skill-body failures.

Out of scope (different clusters / Python idioms):

- Subscriber `on_event` exception path (closed by D47 §B.1; D50 §B.2 documents composition).
- Phase B pre-condition guards in `specialist.py` (Python idioms; not runtime failure modes; see §D D-1).
- Adapter `call()` failure (D48 §B.1) — composes naturally per §B.2 + §D D-5.
- D30 §4 per-work-unit identity checks; B1 collect-all skipping (D51 validation cluster).
- Composition-change post-projection state validity (D52 composition-change cluster).

## B. Triad applied per path

### B.1 — `handle_skill` failure shape (Phase C+ real-wire forward-bar)

| Triad element | Lock |
|---|---|
| **Detection** | Real-wire specialist impls (subclasses of `Specialist` overriding `handle_skill`) SHALL raise `SkillExecutionError` (NEW typed exception) on skill-body failures. Starting category vocabulary: `domain-error` / `external-dependency-error` / `skill-execution` / `unknown`. Per-shape extensions MAY register additional categories per D29 namespacing (e.g., practitioner-shape's `citation-missing`; autonomous-business-shape's `policy-violation`; see §D D-2). |
| **Surface** | `SkillExecutionError` carries structured fields: `specialist_id` (the specialist spec's id), `skill_id` (the skill_id parameter), `category` (string; starter vocabulary above; extension-registrable per shape), `detail` (dict carrying domain-specific structured context), original exception chained via Python `from`. **Two invocation paths surface differently**: (a) **direct `handle_skill` calls** (caller invokes `specialist.handle_skill(skill_id, params)` or via `substrate.skills.invoke(skill_id, params)` per `skills.py:59-62`) — `SkillExecutionError` propagates raw; caller catches directly. (b) **on_event-triggered `handle_skill` calls** (specialist's `on_event` delegates to its own `handle_skill`; `on_event` raises through subscriber-dispatch per D44 + D47) — `SkillExecutionError` is captured per D47 §B.1 into substrate's `_subscriber_failures` (`substrate.py:310-320`) and aggregated as `SubscriberDispatchError(failures)` after outer drain (raised at `substrate.py:274-286`). Caller of outermost `append_event` sees the wrapper; per-specialist failure detail accessible via `SubscriberDispatchError.failures[i][2]` (the captured `SkillExecutionError`). |
| **Recovery** | Caller catches `SkillExecutionError` (direct path) or `SubscriberDispatchError` containing `SkillExecutionError` (on_event-triggered path). Per-category recovery strategies (retry / fail-fast / escalate / abort) are caller-policy concern — Phase C+ shape policy or specialist-internal policy decides. Framework does NOT mandate retry semantics or per-category response. |

### B.2 — Composition with D47 §B.1 + D48 §B.1 (no new mechanism)

The on_event-triggered `handle_skill` path is already covered by D47 §B.1 substrate-level capture mechanism. D50 §B.2 documents the composition; no new mechanism is locked. When a specialist's `on_event` raises `SkillExecutionError` (via delegation to `handle_skill` that raises), the substrate's `_dispatch_event_to_subscribers` catches into `_subscriber_failures` per D47 §B.1; aggregated `SubscriberDispatchError` raised after outer drain per `substrate.py:274-286`.

Adapter-error composition: when `handle_skill` body invokes `adapter.call(...)` (per D48 §B.1) which raises `AdapterCallError`, the composition is specialist-impl choice — wrap as `SkillExecutionError(category="external-dependency-error", original=AdapterCallError)` for uniform skill-failure surface, OR propagate raw `AdapterCallError` for transparent layer-error surface. Caller MUST be prepared for either. See §D D-5 for explicit defer; first concrete real-wire impl establishes precedent.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

The contract is locked here; the impl follows. Specific changes:

- **New `SkillExecutionError` exception type** in `impl/src/fresh_plan/runtime/specialist.py` (parallel to D48's `AdapterCallError` in `adapter.py`). Fields per §B.1: `specialist_id`, `skill_id`, `category`, `detail` (dict), and standard exception-chaining via `from`. Constructor accepts these; `__str__` produces structured diagnostic with `[category] specialist={specialist_id!r} skill={skill_id!r}: {detail}`.
- **No Phase B refactor of pre-condition guards** at `specialist.py:169-172` / `:197-200` / `:201-204` / `:209-213`. These stay as Python idioms (bare `RuntimeError` / `NotImplementedError`); see §D D-1.
- **No `FAILURE_CATEGORIES` extension** — `SkillExecutionError` is a distinct exception type with its own `category` field; doesn't share `ValidationFailure`'s vocabulary (which D46/D48 extended).
- **New tests in `test_specialist.py`** (or new `test_specialist_failure_paths.py`): (i) MonkeyPatched-subclass specialist raises `SkillExecutionError` from `handle_skill`; assert propagation with all structured fields populated (direct invocation path). (ii) `SkillExecutionError` propagation through subscriber-dispatch composition (D47 §B.1 path; same pattern as D48's `test_adapter_call_error_aggregated_via_subscriber_dispatch`); raised inside specialist's `on_event` → captured + aggregated as `SubscriberDispatchError`.

Estimated impl size: ~15-25 lines of code change + 2 new test cases.

## D. What is NOT in this decision

- **No change to D19 specialist contract slots** — D19's slot definitions stand. D50 extends D19's runtime semantics around skill-body failure handling without altering the kind contract. `specialist.schema.json:19` has `additionalProperties: false`; no new slots can be added without schema amendment, which D50 explicitly does NOT do.

- **No retry / backoff / fall-through / escalation / circuit-breaker semantics** — caller policy (Phase C+ shape or specialist concern).

- **No retroactive rewrite of D19, D29, D37, D44, D47, D48 entries** — append-only ledger discipline.

The six explicit DEFERS:

- **D-1 — Phase B pre-condition guards stay as Python idioms; Phase C+ MAY upgrade**: `specialist.py:169-172` (GenericSpecialist not-attached), `:197-200` (RAGSpecialist not-attached), `:201-204` (RAGSpecialist dispatch-miss `NotImplementedError`), `:209-213` (RAGSpecialist required-adapter-not-bound) are bare `RuntimeError` / `NotImplementedError` for programming-time invariant violations. Phase B reaches these branches only via test/bootstrap bugs (attach succeeded → not-attached guards unreachable; D48 §B.3 boot-time check → adapter-not-bound at invoke unreachable in production). Future Phase C+ work may need to upgrade if dynamic attach/detach lifecycle becomes legitimate (hot-reload; runtime composition-change reconfiguration). D50 does NOT prematurely upgrade. **Lesson source**: D49 first-pass scope-inflation pattern (mirroring D48's 3-path structure with refactor sites that turned out to be Python idioms not failure modes).

- **D-2 — Category vocabulary extension for non-practitioner shapes**: starter set (`domain-error` / `external-dependency-error` / `skill-execution` / `unknown`) is practitioner-shape-flavored. Other shapes (Phase E multi-shape work; autonomous-business-shape, financial-trading-shape per D37 §"Rejected alternative") will register additional categories per D29 namespacing (`policy-violation`, `quorum-failure`, `market-rejection`, etc.). D50 starter vocabulary is HTTP/practitioner-flavored; non-practitioner shapes defer category vocabulary to their integration-pattern extensions.

- **D-3 — `handle_skill`-lifecycle raise-point**: WHEN within `handle_skill` the exception raises — before-side-effect (parameter validation), mid-execution (after partial work), after-emit (post-event-emit) — is per-real-wire-impl choice. D50 specifies the typed exception + structured fields; the raise-point is operational detail Phase C+ real-wire impls fix per their conventions.

- **D-4 — Async / streaming / generator `handle_skill`**: `SkillExecutionError` contract presumes synchronous return. Phase C+ async substrates / streaming skills (LLM token streams; long-running task generators) need different shape (mid-stream failure vs pre-stream failure; cancellation semantics; partial-result preservation). Deferred to Phase C+ async substrate work.

- **D-5 — AdapterCallError-inside-handle_skill composition contract**: when `handle_skill` body invokes `adapter.call(...)` which raises `AdapterCallError` (per D48 §B.1), specialist-impl choice — wrap as `SkillExecutionError(category="external-dependency-error", original=AdapterCallError)` for uniform skill-failure surface, OR propagate raw `AdapterCallError` for transparent layer-error surface. Both reasonable; caller catches either. First concrete real-wire impl (likely practitioner-specialist in Phase D) establishes precedent; future D-entry may lock per real-wire learning.

- **D-6 — Batch / multi-skill invocation contract**: contract presumes one-skill-per-call. D19's `skills[]` slot doesn't reject batch semantics but D50 doesn't lock them. Deferred to Phase C+ if batch use-case surfaces.

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: lock detection + surface + recovery for `handle_skill` body failures (Phase C+ real-wire forward-bar); fourth cluster supersedes per D45 §C.
- **WHO**: enforced by *specialist (impl)* — real-wire subclasses raise `SkillExecutionError` per §B.1. *substrate (runtime)* — D47 §B.1 composition handles on_event-triggered path; no new substrate code for D50.
- **FAILS** (recursive — what happens if impl doesn't honor the contract): *Detection*: detection-surface-recovery audit at next workstream-completion + phase-boundary checkpoints (per probing.md Procedure 2 + Checkpoint cadence). *Surface*: audit findings list. *Recovery*: impl-follow-through commit closes the gap OR supersedes entry sharpens.
- **CROSS**: D19 (specialist kind — D50 extends runtime semantics; slot list stands); D29 (extension manifest — per-shape category vocabulary extensions per D-2); D37 (event-driven coordination — D50 §B.1 indirect path composes with D47 §B.1); D44 (queued dispatch — preserved); D47 §B.1 (SubscriberDispatchError aggregation — D50 §B.2 composes); D48 §B.1 (AdapterCallError — D50 §B.2 + §D D-5 composition); D45 (standing requirement).
- **DEFERS**: per §D — Phase B pre-condition guards (D-1); category vocabulary extensions (D-2); raise-point within `handle_skill` (D-3); async / streaming (D-4); AdapterCallError-inside-handle_skill composition (D-5); batch invocation (D-6).

## E. Pre-lock probe disposition (per probing.md Procedure 3 refined-skip rule + D48 §E precedent)

D50 FIRED the pre-lock probe per probing.md refined-skip rule + D48 §E precedent: D50 introduces new contract content (`SkillExecutionError` type + category vocabulary + composition framing with D47 §B.1 + D48 §B.1) beyond pure pattern application of existing typed-exception templates. Probe brief: investigation-bias variant — code-claim verification + quiet Phase C / D / E assumptions.

Probe outcome (2026-05-12 session): **10/10 load-bearing code claims VERIFIED** against direct source reads (file:line citations match impl; D47 §B.1 capture + aggregation mechanism preserved; D19 contract slots unchanged; `skills.py:59-62` SkillRegistry.invoke path matches description). **5 quiet assumptions surfaced**, now named as explicit DEFERS in §D (D-2 through D-6). **D-1 (Phase B pre-condition guards stay as Python idioms)** is the second-pass-corrected scope decision, not a probe finding — surfaced by the D49-first-pass-scope-inflation lesson (mirroring D48's 3-path structure with refactor sites that turned out to be Python idioms).

D50 honors **two cross-session disciplines** that landed during this session:
- The just-amended global CLAUDE.md secondary-source-synthesis rule: pre-lock probe direct citations trusted as Cite-equivalent; probe interpretations (5 quiet assumptions) evaluated using session-context (Phase B forward-bar fitting; Phase E multi-shape consideration) before naming as §D defers.
- The D49 first-pass pattern-completion lesson: cluster cardinality honestly counted (1 SUSPECT vs D46/D47/D48's 3); didn't inflate scope to match precedent shape.

**Precedent extends from D48 §E**: future cluster supersedes that introduce new contract content (D51 validation cluster if it adds per-work-unit identity check semantics; D52 composition-change cluster if it adds post-projection validity contract) SHALL run pre-lock probe per the refined-skip rule, citing D48 §E + D50 §E precedent.

## Rationale

The 2026-05-12 audit identified `handle_skill` failure shape as one of D45 §C item 4's two SUSPECTs. D47 §B.1 closed (b) on_event exception path; D50 closes (a) `handle_skill` failure shape.

D50 is intentionally FOURTH in the D45 §C sequence (boot → subscriber-dispatch → adapter → specialist). Specialist runtime is where Phase D's practitioner-specialist will introduce rich domain skill semantics (draft-section / cite-regulation / etc.); locking the `SkillExecutionError` contract here sets the forward-bar that Phase D + Phase C+ real-wire specialists conform to. The composition framing with D47 §B.1 (subscriber-dispatch) + D48 §B.1 (adapter call) makes the cross-layer error propagation explicit — practitioner-specialist authoring will reference D50 §B.2 for composition expectations.

Honest cluster sizing: D50 addresses 1 SUSPECT vs D46/D47/D48's 3 each. Smaller is correct — the actually-named SUSPECTs are smaller; inflating to match precedent cardinality is exactly the pattern-completion failure-mode tracked in JOURNAL.md (D49 first-pass instance) and probing.md (Pattern-completion-over-pattern-questioning failure mode). The first-pass D50 sketch had 3 paths + 4 refactor sites mirroring D48 + recognized Python-idiom guards as failure-modes — corrected via second-pass to honest 1-path scope.

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): D50 is specification — typed exception + category surface + structured field shape — not Phase C+ real-wire implementation. Locking what's specification today + naming what's Phase C+ real-wire choice keeps the framework durable across eventual real-wire integrations. The 6 explicit DEFERS (D-1 through D-6) honor the spec-vs-impl boundary.

D50 follows D46 + D47 + D48 structural template with §E probe disposition (FIRED, per D48 precedent + the just-amended global CLAUDE.md secondary-source-synthesis rule applied to probe outcome evaluation).

**Cross-references**: D5 §I3 (accountability anchor — operationalized by skill-body failure being observable in event chain context); D10 (event chain — preserved; `SkillExecutionError` doesn't alter chain semantics); D19 (specialist kind contract — D50 extends runtime semantics; slot list stands); D29 (extension manifest — per-shape category vocabulary extensions register per §D D-2); D30 §4 + D34 §A.5 (per-event identity check — unaffected); D37 (event-driven coordination — D50 §B.1 indirect path composes with D47 §B.1); D44 (queued dispatch — D50 preserves; SkillExecutionError raised from `on_event` respects queued semantics); D45 (standing requirement; canonical citation); D46 (first cluster supersedes precedent — structural template); D47 §B.1 (SubscriberDispatchError aggregation — D50 §B.2 composes; canonical composition citation); D48 §B.1 (AdapterCallError — D50 §B.2 adapter-error composition + §D D-5 specialist-impl-choice defer); D48 §E (refined skip rule precedent for D50's probe disposition); D49 §A (sharpen-surfaced step-count correction — D50 §C honors corrected `substrate.py:165-179` 9-step ordering implicitly via D47 reference); D49 first-pass scope-inflation incident (lesson applied to D50's honest 1-path sizing per §D D-1 framing); probing.md §"Pattern-completion over pattern-questioning" failure mode (D49 first-pass + D50 second-pass correction is canonical example of the discipline working); probing.md Procedure 3 refined-skip rule (D50 §E disposition); 2026-05-12 D50 pre-lock probe (cited in §E; surfaced D-2 through D-6).
