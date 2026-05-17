# D58 — 2026-05-17 — Extends D20 + D39 — work-unit.lifecycle.started-at + completed-at reconciliation with event-derivation

**Decision (substantive; extends D20 work-unit kind + D39 state-is-fully-derived-from-event-chain)**: The `work-unit.lifecycle.started-at` and `completed-at` slots (work-unit.schema.json:63-64) are formally reconciled with D39's state-is-fully-derivable property. **Event chain is source of truth**; manifest-declared timestamps in `lifecycle.started-at` / `lifecycle.completed-at` are treated as **initial-snapshot only**. When the event chain carries `state-change:work-unit-status` transition events, **runtime-derived values shadow manifest** — timestamps projected from transition events' `event.at` and written to live work-unit record by `event_chain.apply_event_to_state` at the work-unit-status projection branch (event_chain.py:75-83). Boot-time framework-validator reconciles manifest-declared against chain-derived and raises `WorkspaceBootError(category="lifecycle-derivation-mismatch")` per D46 pattern when they disagree. One path; ONE workspace runtime moment (boot-time reconciliation) + ONE per-event projection extension. Not a D45 §C cluster supersedes (those completed at D52). Pre-lock probe FIRED per probing.md Procedure 3 refined-skip rule + D48 §E + D50 §E + D52 §E precedent — D58 introduces new contract content.

## A. Scope

**Honest scope: 1 path, 1 SUSPECT.** Not a cluster supersedes. D58 reconciles two timestamp sources:

- **Source (a) — manifest-declared**: `work-unit.schema.json:56-65` defines `lifecycle.started-at` / `completed-at` as optional ISO-8601 timestamps. Manifest may declare a work-unit at boot with these populated (resumption from prior session; replay of externally-attested record). Schema admits without runtime-grounded provenance.
- **Source (b) — event-chain-derived**: per D20 ("Richer lifecycle history derivable from events") + D39 (state-is-fully-derived). Substantive timestamps SHOULD project from transition events' `event.at` (transition to `in-progress` populates `started-at`; transition to `completed` populates `completed-at`).

Currently impl populates neither (verified: grep returns zero hits for `started-at`/`completed-at` in src/; `workspace.py:330` sets only `lifecycle.created-at`; `event_chain.apply_event_to_state`'s work-unit-status branch at event_chain.py:75-83 calls `state.transition_work_unit` updating `status` but not lifecycle timestamps). Schema admits both, impl populates neither, no rule reconciles manifest-declared against chain evidence. D58 closes this gap.

**Out of scope** (per §D):
- Timezone normalization (D-3).
- Re-derivation cost (snapshot caching per D11 + D40 §C) — D-5.
- Out-of-order transition events vs wall-clock — D-6.
- Cross-version trajectory under D33 migration-safety — D-7.
- `paused` / `abandoned` derived markers — D58 scopes to `started-at` (in-progress transition) + `completed-at` (completed transition) per schema slot enumeration; D-4.

## B. Triad applied per path

### B.1 — Work-unit lifecycle.started-at + completed-at reconciliation

| Triad element | Lock |
|---|---|
| **Detection** | Two surfaces. **Runtime projection (event_chain.apply_event_to_state work-unit-status branch at event_chain.py:75-83)**: extend so when `new_status == "in-progress"` AND live work-unit record's `lifecycle.started-at` is unset, write `event.at` to `state.work_units[wu_id]["lifecycle"]["started-at"]`. Symmetric for `new_status == "completed"` → `lifecycle.completed-at`. Idempotent: only writes when target field unset (first-transition wins; replay produces identical state). **Boot-time reconciliation (validator/workspace.py `validate_workspace_boot`)**: for each manifest-declared work-unit with non-null `lifecycle.started-at` or `lifecycle.completed-at`, replay event chain via `chain.state_at(len(chain)-1)` (per event_chain.py:265) and compare manifest-declared to chain-derived. Mismatch (declared but no corresponding transition event in chain; OR declared value ≠ derived value) yields `ValidationFailure(category="lifecycle-derivation-mismatch", path="workspace.work-units[<id>].lifecycle.<field>", value=<manifest-declared>, reason="manifest declares <field>=<X> but chain-derived value is <Y> (or no <status>-transition event present)")`. |
| **Surface** | `WorkspaceBootError(failures=[ValidationFailure(category="lifecycle-derivation-mismatch", ...)])` raised by `validate_workspace_boot` per D46 pattern. NEW `FAILURE_CATEGORIES` entry `"lifecycle-derivation-mismatch"`. |
| **Recovery** | Boot aborts; substrate not constructed. Caller catches `WorkspaceBootError` and reports. User reconciles by either (a) removing the manifest-declared timestamp (let chain derive on next boot), or (b) supplying the missing transition event in the chain. Runtime projection has no failure mode — idempotent "only-write-if-unset" rule means no detection/surface/recovery needed there beyond boot-time reconciliation. |

**Sole authority rationale**: chain-is-source-of-truth over manifest-is-source-of-truth. D39 already locks state-is-fully-derived-from-event-chain; permitting manifest values to silently override chain-derived would violate D39's load-bearing pre-deployment-simulation + replay-debugging + audit-reconstruction use-cases. Manifest as initial-snapshot-only preserves D39 (chain-replay reconstructs same state); manifest-declared timestamps checked-not-trusted at boot.

**Timing rationale**: boot-time reconciliation over per-event-time check. Reconciliation only arises when both sources exist. At per-event-time chain is being built incrementally. At boot-time both sources fully present; comparison well-formed. Per-event projection (constructive write) runs continuously per existing projection contract.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

- **`event_chain.apply_event_to_state` extension** (event_chain.py:75-83 work-unit-status branch). After existing `state.transition_work_unit(wu_id, new_status)` call: read work-unit record from `state.work_units[wu_id]`; if `new_status == "in-progress"` AND `record["lifecycle"].get("started-at") is None`, set `record["lifecycle"]["started-at"] = event.get("at")`; symmetric for `completed`. Idempotent guard ensures replay-equivalence.
- **`workspace_state.transition_work_unit` docstring update** (workspace_state.py:110-124). Signature unchanged; docstring names that lifecycle timestamp writes happen at projection layer (event_chain.apply_event_to_state), preserving projection-is-the-only-mutator invariant per D39.
- **`validate_workspace_boot` extension** (validator/workspace.py:50). New reconciliation check after existing B1 portion. For each manifest-declared work-unit with non-null `lifecycle.started-at` or `lifecycle.completed-at`: derive chain-projection state via `chain.state_at(len(chain)-1)`; compare derived `state.work_units[wu_id]["lifecycle"]` to manifest-declared; append `ValidationFailure(category="lifecycle-derivation-mismatch", ...)` per mismatch.
- **`FAILURE_CATEGORIES` extension** in `validator/types.py`: add `"lifecycle-derivation-mismatch"`.
- **2 new tests** in `impl/tests/test_lifecycle_derivation.py` (NEW file):
  - Test 1 — chain-derives-started-at: create work-unit at boot (status=created); transition to in-progress via state-change event; verify `state.work_units[wu_id]["lifecycle"]["started-at"]` equals event's `at` value. Replay via `chain.state_at(-1)` produces identical timestamp.
  - Test 2 — mismatch-rejected-at-boot: manifest declares work-unit with `lifecycle.completed-at: "2026-05-17T10:00:00Z"` but chain contains no transition to `completed`. Assert `WorkspaceBootError(category="lifecycle-derivation-mismatch")`; substrate not constructed.

Estimated impl size: **~30 LOC + 2 tests**. 195 baseline → 197 tests post-D58 [impl].

## D. What is NOT in this decision

- **D-1 — Timestamp ambiguity when no chain transition exists**: D58 locks manifest-declared values without backing chain transition events as REJECTED at boot. Alternative (use manifest as fallback) rejected: would re-establish manifest-as-authority, violating D39. Re-evaluate only if Phase D pioneer surfaces a use-case where pre-boot manifest-only attestation must round-trip.
- **D-2 — `event.at` field semantics for projection**: D58 assumes per-event `at` field carries canonical timestamp. Exact field path (`event.at` vs `event.payload.at` vs both with precedence) is impl-detail per event schema + D34 conventions; D58 does NOT lock. Impl follow-through reads schema; if ambiguity surfaces, clarification entry follows D49 pattern.
- **D-3 — Timezone normalization**: events carrying timestamps in mixed timezones may produce derived values equal in absolute time but unequal in string representation. D58 does NOT lock normalization. Phase C standards-compatibility work is natural home.
- **D-4 — `paused` and `abandoned` derived markers**: schema defines only `created-at` + `started-at` + `completed-at`. D20's status enum admits `paused` + `abandoned`; their derived timestamps out of D58 scope. Future entry may extend schema with `paused-at` / `abandoned-at` and reapply D58 reconciliation pattern.
- **D-5 — Idempotent re-derivation cost**: each boot reconciles ALL manifest-declared work-units against full chain replay. O(chain) per work-unit. Snapshot caching per D11 + D40 §C is implementation answer; D58 does NOT lock caching strategy. Cost framing acceptable for Phase B reference-impl scale.
- **D-6 — Out-of-order transition events**: chain's `prev-event` integrity check ensures structural ordering but NOT wall-clock monotonicity of `event.at`. A work-unit could have `completed` transition with `at < in-progress` transition's `at`. D58 honors chain order (first-transition-wins per idempotent guard); wall-clock-ordering enforcement out of scope.
- **D-7 — Cross-version trajectory under D33 migration-safety**: when D33 migration-safety lands and version-bumps work-unit schema, lifecycle timestamp semantics may shift. D58 does NOT lock cross-version reconciliation. D33 closure (already locked as D54 in this session — supersedes original D33 framing) determines whether to cite D58 explicitly.

Other items NOT in this decision:

- **No retroactive rewrite of D20 or D39** — append-only ledger.
- **No change to work-unit.schema.json** — D58 operationalizes existing slot semantics.
- **No new typed exception** — reuses `WorkspaceBootError`.
- **No change to canonical substrate step ordering** — D58's runtime projection extension lives inside existing event_chain.apply_event_to_state; no new substrate step. Boot-time reconciliation extends existing `validate_workspace_boot` body; no new boot-procedure step.

## Decision-shape template self-application

- **WHAT**: lock chain-is-source-of-truth for `work-unit.lifecycle.started-at` + `completed-at`; manifest values become initial-snapshot only; boot-time reconciliation enforces consistency via `WorkspaceBootError(category="lifecycle-derivation-mismatch")`. Operationalizes D20's "richer lifecycle history derivable from events" + D39's state-is-fully-derived at the lifecycle-field level.
- **WHO**: enforced by *substrate (runtime)* — `event_chain.apply_event_to_state` writes derived timestamps at work-unit-status projection branch. *framework-validator (B1)* — `validate_workspace_boot` reconciles manifest-declared against chain-derived at boot. *shape (policy)* — unaffected. *specialist (impl)* — unaffected.
- **FAILS**: *Detection*: audit at next checkpoint catches unwritten derived fields or skipped reconciliation. *Surface*: audit findings + failing tests. *Recovery*: impl-follow-through commit closes; or supersedes sharpens.
- **CROSS**: D10 (event chain runtime — D58 extends apply_event_to_state's work-unit-status projection branch); D20 (work-unit kind — lifecycle slot semantics now have derivation rule + reconciliation rule); D23 (work-unit-id reference on events — D58 relies on `event.work-unit-id` for projection filter); D29 + D30 §4 + D32 + D33 (boot validation flow — D58 adds new boot-time check class); D34 §A.5 (current-state resolution preserved); D39 (state-is-fully-derived — D58 closes lifecycle-timestamp gap); D40 §A (`state_at(sequence-n)` query interface — D58's reconciliation uses); D45 (standing requirement); D46 §B (precedent for `WorkspaceBootError` reuse + new FAILURE_CATEGORIES entry); D48 §E + D50 §E + D52 §E (FIRED precedent); D54 (D33 migration-safety; companion entry — D-7 deferral cites).
- **DEFERS**: per §D — D-1 through D-7.

## E. Pre-lock probe disposition

D58 **FIRED** per refined-skip rule + D48 §E + D50 §E + D52 §E precedent. NEW contract content:

1. **New FAILURE_CATEGORIES entry** `"lifecycle-derivation-mismatch"`.
2. **New boot-time reconciliation check** — NEW per-boot validation class.
3. **New event-projection field-population logic** in `apply_event_to_state`'s work-unit-status branch.

**Probe outcome (V1-verified)**: event_chain.py:27-83 projection function (work-unit-status branch confirmed to NOT write lifecycle fields); workspace_state.py:110-124 transition_work_unit (status-only mutation); workspace.py:330 creation site (only `created-at` set); validator/workspace.py:50 validate_workspace_boot (boot-validation entry point); validator/types.py:22-37 FAILURE_CATEGORIES frozenset; work-unit.schema.json:56-65 lifecycle slot (optional started-at + completed-at). Quiet assumptions surfaced + named as §D D-1 through D-7.

## Rationale

D20 promises "richer lifecycle history derivable from events"; D39 promises state-is-fully-derived. Both hold at **status** level (transition events project to `state.work_units[wu_id]["status"]`) but FAIL at **timestamp** level — no code path writes `lifecycle.started-at`/`completed-at` from chain evidence; no boot-time check reconciles. D58 closes the gap by extending projection contract + adding boot-time reconciliation, both within patterns established by D46-D52 (reuse WorkspaceBootError; new FAILURE_CATEGORIES; per-event projection inside existing event_chain branch).

Honest scope: 1 path, 1 SUSPECT. Not a cluster supersedes (cluster phase complete at D52). D58 is normal Extends entry post-cluster-phase. Future Extends entries closing similar gaps follow same pattern.

**Cross-references**: D5 §I3 (accountability — operationalized by chain-derived + boot-reconciled lifecycle timestamps); D10 (event chain — projection contract extended); D20 (work-unit kind — lifecycle slot semantics now have derivation + reconciliation rule); D23 (work-unit-id reference); D29 + D30 §4 + D32 + D33 (boot validation flow — D58 adds new check class); D34 §A.5 (current-state resolution preserved); D39 (state-fully-derived — D58 closes lifecycle-timestamp gap); D40 §A (query interface — D58 uses `state_at`); D45 (standing requirement); D46 §B (WorkspaceBootError reuse precedent); D48 §E + D50 §E + D52 §E (FIRED precedent); D52 §Rationale (cluster phase closure; D58 is post-cluster Extends entry); D54 (D33 migration-safety companion — D-7); probing.md Procedure 3 refined-skip rule; probing.md "Pattern-completion over pattern-questioning" (1-path scope honest, not inflated).

## Honest basis caveats

- **Read directly**: README + CLIPPY-COMPANION + probing.md + D20 + D39 + D45 + D52 + work-unit.schema.json + event_chain.py + workspace_state.py + workspace.py:300-380 + grep-verified `started-at`/`completed-at` absent from impl/src/ + validator/types.py:19-37 + validator/workspace.py:50 docstring.
- **NOT Read directly but claimed about (Flag)**: validator/workspace.py FULL body — only docstring window 19-55 was read; substantive reconciliation extension described at contract level. Flag-to-Read at impl follow-through. event.schema.json — precise `event.at` field path named in §D D-2 as deferred impl-detail.
- **Inferred from pattern (non-load-bearing)**: test count "197 post-D58 [impl]" arithmetic only. Impl LOC estimate "~30" rough projection.
- **Pattern-completion guard**: D58's 1-path scope honest per cluster phase closure; §E FIRED matches D48/D50/D52 precedent (new contract content).
