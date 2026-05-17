# D51 — 2026-05-12 — Extends D29 + D30 §4 — validation cluster honors detection-surface-recovery triad (per D45 §C)

**Decision (substantive; fifth cluster supersedes per D45 §C; PURE pattern application — pre-lock probe SKIPPED per D45 §E precedent)**: The validation layer (B1 conformance validator per D29 §validation flow + D30 cross-kind referential integrity checks) is locked under D45's detection-surface-recovery triad. Two SUSPECTs from the 2026-05-12 audit unified here: (1) per-work-unit identity checks named in D30 §4 but never implemented in `per_event_checks.py`; (2) B1 collect-all silent-skip when extensions empty at `validator/workspace.py:275`. Different layer than D46-D50 (validation, not runtime behavior); honest cluster sizing 2 SUSPECTs (vs D46/D47/D48's 3); operationalizes existing D30 §4 contract + closes a silent-degradation bug — no new contract content, so pre-lock probe SKIPPED per D45 §E precedent.

## A. Scope of cluster

D45 §C item 5 named two validation-layer SUSPECTs:

- **A.1 Per-work-unit identity checks (D30 §4 implementation gap)**: D30 §4 explicitly names "Per-work-unit: `work-unit.contributing-actors[].id` → existing actor; `work-unit.contributing-specialists[]` → bound specialist; `work-unit.kind` → registered." `per_event_checks.py` implements event-level checks (`event.actors[].id`, `event.work-unit-id`, `event.payload-subtype`) but does NOT validate the work-unit-internal slots when a work-unit is created. Work-units are created via state-change events with `what="work-unit-created"` (per D39 closure); `payload.after` carries the full work-unit record. D51 extends `check_event_references` to validate the work-unit record at creation-event time.

- **A.2 B1 collect-all silent-skip when extensions empty**: at `validator/workspace.py:275`, an `if loaded:` guard silently skips three of five D30 check categories (capability satisfaction; vocabulary resolution; binding availability) when no extensions are loaded. Comment justifies as "would emit noise" — but a manifest declaring `required-capabilities` or `required-adapter-bindings` with no loaded extensions SHOULD fail at those checks. The silent skip hides real failures. D51 removes the guard; the three checks become no-ops when there's genuinely nothing to check, and correctly surface failures when there are declared requirements with no satisfying extensions.

Different layer than D46-D50 (which addressed runtime-behavior clusters: boot procedure / subscriber-dispatch / adapter / specialist). D51 is the validation-layer cluster.

Out of scope (different clusters):

- Composition-change post-projection state validity (D52 composition-change cluster).
- Workspace-internal identity at event level (already implemented in `per_event_checks.check_event_references`; D51 extends the work-unit-internal portion only).
- D29 §validation flow itself — D51 operationalizes existing D30 §4 contract within the flow; does not alter the flow's structure.
- Defensive silent-skips at `checks.py:166-170 / 271-279 / 295-305 / 605-615` — verified upstream-catches via `check_resolution` (lines 172-194 record resolution failures for both ext-not-declared and provision-not-found branches); these are NOT silent-degradation bugs. Adjacent cleanup in §C: inline comments naming the defensive rationale (do-now adjacent cleanup per the new global CLAUDE.md "No silent substitution" form-level discipline).

## B. Triad applied per path

### B.1 — Per-work-unit identity checks

| Triad element | Lock |
|---|---|
| **Detection** | When `event["payload-subtype"] == "state-change"` and `event["payload"]["what"] == "work-unit-created"`, extend `check_event_references` (per_event_checks.py) to validate the work-unit record carried in `payload.after`: (i) `contributing-actors[].id` → each resolves to existing actor in current state (with self-attestation per D34 §A.5 for the on-event-added case); (ii) `contributing-specialists[]` → each resolves to a bound specialist binding-id in `substrate.specialist_bindings`; (iii) `kind` → registered work-unit-kind (core or extension-registered per D29 §validation flow step 4 vocabulary tables). |
| **Surface** | `EventRejected(failures=[ValidationFailure(category="identity", path="event.payload.after.<slot>", value=<bad-value>, reason=<...>), ...])`. Reuses existing `category="identity"` (per `FAILURE_CATEGORIES`) since per-work-unit identity is semantically the same class as event-level identity (workspace-internal reference resolution per D30 §4). No new exception type, no new category. |
| **Recovery** | Event is rejected per D30 §4 per-event timing semantics + per_event_checks's existing `EventRejected` raise contract. Work-unit is NOT created; chain unchanged. Caller fixes the work-unit record's bad references and re-emits. |

### B.2 — B1 collect-all silent-skip removal

| Triad element | Lock |
|---|---|
| **Detection** | At `validator/workspace.py:275`, the `if loaded:` guard around `check_capability_satisfaction` + `check_vocabulary_resolution` + `check_binding_availability` is removed. Each check runs unconditionally. When `loaded` is genuinely empty AND the manifest has no declared requirements, the checks no-op (empty iteration; zero failures). When `loaded` is empty BUT the manifest declares requirements (e.g., `required-adapter-bindings`, `required-capabilities`), the checks correctly surface failures rather than silently passing. |
| **Surface** | Existing `WorkspaceBootError(failures=[...])` shape via the validator's collect-all path. No new exception type, no new category — existing `category="capability"` / `"vocabulary"` / `"binding"` cover the surfaces. Caller sees structured failures naming the unsatisfied requirements. |
| **Recovery** | Caller fixes the manifest (declare the missing extension(s); or remove the declared-but-unsatisfied requirements). Re-boot. |

## C. Impl follow-through (separate commit; tracked in roadmap.md)

The contract is locked here; the impl follows. Specific changes:

- **Extend `check_event_references` in `per_event_checks.py`**: add a branch when `payload-subtype == "state-change"` and `payload.what == "work-unit-created"` to validate `payload.after.contributing-actors[].id` (against `state.has_actor` with self-attestation for the on-event-added work-unit per existing D34 §A.5 mechanism); `payload.after.contributing-specialists[]` (against `substrate.specialist_bindings` keys — need to pass this in; currently the function receives `known_binding_ids` for substrate-binding context, similar plumbing); `payload.after.kind` (against substrate's `registered_work_unit_kinds` set — new state, populated from extension vocabulary-registrations at boot, parallel to `registered_payload_subtypes`). Reuse `category="identity"`.

- **Pass specialist binding-ids + work-unit-kind registry to `check_event_references`**: extend the function signature with `known_specialist_binding_ids: Iterable[str]` and `registered_work_unit_kinds: Iterable[str]`. Plumb from `substrate.specialist_bindings.keys()` + a new `substrate.registered_work_unit_kinds` (populated at boot from `result.vocabulary_tables.get("work-unit.kind", [])` parallel to existing `registered_payload_subtypes`).

- **Remove `if loaded:` guard at `validator/workspace.py:275`**: the three check calls run unconditionally. The guard removal is the entire fix for §B.2; no new code.

- **Adjacent cleanup — inline rationale comments for 4 defensive silent-skips** (per global CLAUDE.md "No silent substitution" form-level discipline): at `checks.py:166-170` (substrate-binding-anyOf legitimate skip — already commented; verify comment clarity), `checks.py:271-279` + `:295-305` (capability check when ext not loaded — upstream `check_resolution` records resolution failure), `checks.py:605-615` (binding-availability when ext not loaded — same upstream-catches rationale). Add one-line comments naming the defensive rationale so future maintainers distinguish defensive-skip from silent-bug.

- **New tests in `test_per_event_checks.py`** (or new `test_work_unit_identity.py`): (i) work-unit-created event with valid `contributing-actors` + `contributing-specialists` + `kind` → passes. (ii) work-unit-created event with `contributing-actors[].id` referencing non-existent actor → `EventRejected(category="identity")` with structured path. (iii) work-unit-created event with `contributing-specialists[]` referencing unbound binding-id → same. (iv) work-unit-created event with `kind` not registered → same.

- **New test in `test_validator_workspace.py`** (or extend existing): manifest with `required-capabilities` declared in shape + no extensions loaded → boot fails with capability failure (not silent pass). Verifies the §B.2 guard removal.

Estimated impl size: ~30-50 lines code change (per_event_checks.py extension is the bulk; workspace.py is 1-line removal; boot.py needs to populate `registered_work_unit_kinds`) + 5 new test cases + 4 inline rationale comments.

## D. What is NOT in this decision

- **No change to D29 §validation flow** — D51 operationalizes the existing flow's step 6 ("Cross-kind composition checks run") + D30 §4 per-event-runtime portion; doesn't alter step ordering or extension-discovery semantics.

- **No change to D30's five-category structure or timing-modes** — D51 implements what D30 §4 specifies (per-work-unit identity); doesn't add new categories or modify timing semantics.

- **No new exception type or `FAILURE_CATEGORIES` extension** — reuses existing `EventRejected` + `category="identity"` for §B.1; existing `WorkspaceBootError` for §B.2. PURE pattern application of existing types.

- **No fix for the 4 defensive silent-skip patterns at the behavior level** — verified upstream-catches via `check_resolution`; behavior is correct; only form (silent `continue` without inline rationale) is addressed via §C adjacent comment cleanup.

- **No work-unit lifecycle state-change validation** — D51 validates work-unit creation references; lifecycle transitions (status changes: created → in-progress → completed / paused / abandoned per D20) are different checks not in D30 §4 scope.

- **No retroactive rewrite of D29, D30, D34, D39 entries** — append-only ledger discipline.

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: lock detection + surface + recovery for per-work-unit identity check implementation + B1 collect-all silent-skip removal; fifth cluster supersedes per D45 §C.
- **WHO**: enforced by *framework-validator (B1)* — `validate_workspace_boot` runs the unconditional D30 §B.2-§B.5 checks; *substrate (runtime)* — `check_event_references` validates work-unit records on creation events.
- **FAILS** (recursive): *Detection*: detection-surface-recovery audit at next workstream-completion or phase-boundary checkpoint catches missing impl. *Surface*: audit findings list + failing tests if impl regresses. *Recovery*: impl-follow-through commit closes; or supersedes entry sharpens contract.
- **CROSS**: D29 §validation flow (D51 operationalizes step 6's cross-kind check portion); D30 §1 + §2 + §3 + §4 + §5 (D51 implements §4 per-work-unit + removes §B.2-§B.5 silent-skip); D34 §A.5 (self-attestation extends to on-event-added work-unit on creation events); D39 (work-unit-created state-change event payload.after structure); D45 (standing requirement); D46/D47/D48/D50 (cluster supersedes precedent for §A scope + §B triad framing).
- **DEFERS**: work-unit lifecycle state-change validation; the 4 defensive silent-skips' behavior-level treatment (only form-level inline rationale added); composition-change post-projection validity (D52).

## E. Pre-lock probe disposition (SKIPPED per D45 §E precedent)

Unlike D48 + D50 (which FIRED the probe because they introduced new contract content: AdapterCallError + SkillExecutionError typed exceptions + category vocabularies + composition framings), **D51 SKIPS the pre-lock probe per D45 §E precedent** + the refined skip rule's first condition: D51 is PURE pattern application — operationalizes existing D30 §4 contract; removes a known silent-degradation bug at `validator/workspace.py:275`. No new exception types; no new categories; no new composition framings; no novel design choices requiring quiet-assumption surfacing. Like D46 + D47 (which both SKIPPED per D45 §E precedent for the same reason), D51 fits the original skip rule.

Audit discipline applied this session (per new global CLAUDE.md "First-order findings are starts, not ends"): the systematic audit of `validator/checks.py` for additional silent-skip / silent-substitution patterns of the same class found 4 more candidates (lines 166-170, 271-279, 295-305, 605-615). Direct Read of `check_resolution` (lines 172-194) verified the upstream-catches rationale: all 4 are defensive, not silent-degradation. D51 §C adjacent-cleanup adds inline rationale comments to make the defensive intent explicit per the new "No silent substitution" form-level discipline. The systematic-audit step itself is not a probe in the probing.md sense; it's V1 source-over-symptom verification of the audit class.

## Rationale

The 2026-05-12 audit identified validation-layer SUSPECTs as part of D45 §C item 5. Both are operational gaps in the B1 validator: (1) D30 §4 specifies per-work-unit identity checks that were never implemented; (2) `validator/workspace.py:275` silently skips three check categories when extensions are empty, hiding real failures from manifests with declared requirements.

D51 is intentionally FIFTH in the D45 §C sequence (boot → subscriber-dispatch → adapter → specialist → validation). The validation cluster is the natural next layer after the four runtime-behavior clusters; closing validation gaps before Phase D's pioneer-instance (where practitioner-specialist + custom shapes will exercise the validator heavily) ensures the validator surfaces real failures rather than silently passing.

Honest cluster sizing: D51 addresses 2 SUSPECTs. Smaller than D46/D47/D48 (3 each), larger than D50 (1). Sized by what the audit actually named + verified upstream-catches for adjacent candidates — neither inflated to match precedent (D50 first-pass pattern-completion lesson applied) nor under-scoped (the work-unit-internal validation gap is real Phase D-load-bearing per practitioner-specialist's eventual work-unit creation flows).

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): D51 is specification-already-locked (D30 §4) + implementation closing the gap. Not new contract; existing contract finally honored.

D51 follows D46-D50 structural template with §E SKIP disposition (per D45 §E precedent + D46/D47 alignment) instead of FIRE disposition (D48/D50). Skip is correct: PURE pattern application without new contract content.

The systematic audit step (verifying that 4 additional silent-skip candidates were defensive vs degradation) honors the new global CLAUDE.md "First-order findings are starts, not ends" discipline + V1 source-over-symptom rigor — read `check_resolution` to verify the upstream-catches claim before locking D51's narrow scope (rather than expanding to all 6 candidates indiscriminately).

**Cross-references**: D5 §I3 (accountability — operationalized by validator catching identity-failure events); D7 §boot (validator runs at composition-resolution-time per D7 + D29); D9 + D22 (actor.id resolution — already implemented at event level; D51 extends to work-unit-internal); D10 + D23 (event.work-unit-id slot — already implemented; D51 adds work-unit-creation-event work-unit-internal checks); D19 (specialist bindings — D51 §B.1 (ii) checks specialist-bindings membership); D20 (work-unit slots — `contributing-actors[]`, `contributing-specialists[]`, `kind` are the slots D51 §B.1 validates); D29 §validation flow (D51 operationalizes step 6 cross-kind portion); D29 §vocabulary registration (D51 §B.1 (iii) checks `kind` against the `work-unit.kind` slot's registered values); D30 §4 (D51 §B.1 is the per-work-unit portion implementation); D30 §B.2 + §B.3 + §B.5 (D51 §B.2 removes the silent-skip guard); D34 §A.5 (self-attestation — extends naturally to on-event-added work-unit per existing per_event_checks logic); D39 (work-unit-created state-change event carries record on payload.after); D45 (standing requirement; canonical citation); D46 + D47 (skip-probe precedents — D51 aligns); D48 + D50 (fire-probe precedents — D51 distinguishes; pure-pattern-application not new-contract); 2026-05-12 systematic audit of validator/checks.py (4 additional defensive silent-skip candidates verified upstream-catches via `check_resolution`; inline rationale comments added in §C as adjacent cleanup per new global CLAUDE.md "No silent substitution" form-level discipline).
