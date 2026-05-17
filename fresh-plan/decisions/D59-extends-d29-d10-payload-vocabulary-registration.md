# D59 — 2026-05-17 — Extends D29 + D10 — payload-vocabulary registration mechanism + per-event validation

**Decision (substantive; new contract content extending D29 vocabulary registrations + D10 payload schemas)**: The four open-vocabulary string slots inside core payload schemas — `payload-claim.confidence`, `payload-action.action-name`, `payload-state-change.what`, `payload-lifecycle-transition.trigger` — are operationalized as extension-registerable vocabulary. D29 §"Vocabulary registrations" enumerated six top-level open-vocab slots (`event.payload-subtype`, `work-unit.kind`, `substrate.capabilities[]`, `substrate.runtime-shapes[]`, `adapter.protocol-or-transport`, `actor.subtype`) but did NOT cover open-vocab values *inside* core payload bodies; the payload schemas describe these slots as "open vocabulary; shape / specialist / adapter / extension concern" (verified at `schemas/payload-claim.schema.json:19`, `payload-action.schema.json:14`, `payload-state-change.schema.json:11-13`, `payload-lifecycle-transition.schema.json:16-19`) but framework has no mechanism to register a value or fail-closed on unregistered values. D59 closes that gap by binding payload-slot values to D29's registration mechanism via a single new manifest slot — `payload-vocabulary-registrations` — loaded into substrate's runtime tables at boot and consulted by a new per-event check at substrate step 1. Pre-lock probe FIRED per probing.md Procedure 3 refined-skip rule + D48 §E + D50 §E + D52 §E precedent.

## A. Scope

**Honest cluster cardinality: 1 path**, not 4. The four payload slots are covered by a SINGLE mechanism — one new manifest-slot shape, one boot-time loader extension, one per-event check site, one `vocabulary` failure category (reused). Slots differ only in `payload-slot` identifier; validation logic is uniform. Aligns with D50 + D52 honest 1-path scope.

The path:

- **A.1 Payload-vocabulary registration + per-event validation**: extension manifests may declare `payload-vocabulary-registrations: [{payload-slot, value, spec-ref}]` parallel to D29's existing top-level `vocabulary-registrations`. Framework loads these into a new substrate runtime table `registered_payload_vocabulary: dict[payload-slot, set[qualified-value]]` at boot (parallel to existing `registered_payload_subtypes` / `registered_work_unit_kinds` per `runtime/boot.py:153-159`). `runtime/per_event_checks.check_event_references` consults the table at runtime: for each of the four payload slots, when payload carries a value AND value is non-empty AND value is not in registered set for that slot, append `ValidationFailure(category="vocabulary")`. Substrate raises `EventRejected` per existing pattern.

**Distinction from D29 §"Vocabulary registrations"**: D29 registers values for *core kind contract* slots. D59 registers values for *core payload body* slots — structurally parallel concept D29 left implicit. Identifier namespacing per D29 applies unchanged (qualified form `<ext-id>:<value>`).

**Out of scope** (per §D):
- `payload-claim.evidence-references[]` items — these are opaque references per schema description ("framework does not validate semantics"); NOT a vocabulary surface.
- `payload-action.parameters` object structure validation — schema names "action-name-specific (extension-declared)"; full payload-parameter-schema validation per action-name is separate surface.
- Versioning of registered entries (D33/D54 territory).
- Required-vs-optional semantics — D59 locks FAIL per no-silent-substitution; D-3.
- Cross-extension vocabulary composition — D29 namespacing handles disambiguation; semantic equivalence out of scope.

## B. Triad applied per path

### B.1 — Payload-vocabulary registration + per-event check

| Triad element | Lock |
|---|---|
| **Detection** | `runtime/per_event_checks.check_event_references` extended: after existing payload-subtype check (per_event_checks.py:134-151), iterate the four payload slots. For each `(slot_name, payload_path)`: read value from event payload (`event["payload"][slot_name]`); if value is non-None AND event's `payload-subtype` matches owning subtype (`confidence` → claim; `action-name` → action; `what` → state-change; `trigger` → lifecycle-transition) AND value is non-empty string AND value is not in `substrate.registered_payload_vocabulary[slot_qualified_name]`, append `ValidationFailure(category="vocabulary", path=f"event.payload.{slot_name}", value=<value>, reason="payload value not registered by any loaded extension")`. The `slot_qualified_name` is `<payload-subtype>.<slot-name>` (e.g., `"action.action-name"`). |
| **Surface** | Reuses existing `EventRejected(failures=[ValidationFailure(category="vocabulary", ...)])` raised by `substrate.append_event` step 1. NO new exception type. NO new FAILURE_CATEGORIES entry — `"vocabulary"` already in `validator/types.py:27` per D30 §3. |
| **Recovery** | Event rejected at substrate step 1. State NOT mutated. Chain integrity preserved. Caller fixes either (a) extension manifest to register the missing value with spec-ref, or (b) event payload to use registered value, then re-emits. |

**Rationale for fail-closed**: D59 locks unregistered values as FAIL not WARN. Per global CLAUDE.md "No silent substitution" + D45 standing requirement. Silently accepting unregistered would allow events into chain whose semantic content is undefined at framework level. Empty-or-absent values remain OK (slots are optional). Check fires only when value is present AND non-empty AND unregistered.

**Distinction from existing per-event checks**:
- `check_event_references` already checks `event.payload-subtype` against `registered_payload_subtypes` — D29-style top-level subtype registration. D59 adds *nested* check for open-vocab string slot *within* the (already-registered) subtype's payload.
- Identity-resolution checks out of scope; D59 is purely vocabulary-surface.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

- **Extension-manifest schema** (`schemas/extension-manifest.schema.json`): add optional array property `payload-vocabulary-registrations` parallel to existing `vocabulary-registrations`. Item shape: `{payload-slot: string (enum of four qualified names: "claim.confidence", "action.action-name", "state-change.what", "lifecycle-transition.trigger"), value: string, spec-ref: string}`. Required: `payload-slot` + `value`; `spec-ref` optional per D29 §2 pattern.
- **`validator/workspace.py` step 7 (vocabulary-table merge)**: extend existing merge loop (workspace.py:264-268) with parallel loop populating new return-field `payload_vocabulary_tables: dict[payload-slot, set[qualified-value]]`. Loaded in dependency-topological order.
- **`validator/types.py` `ValidationResult`**: add `payload_vocabulary_tables: Optional[dict[str, list[str]]]` parallel to existing `vocabulary_tables`.
- **`runtime/substrate.py`**: add `registered_payload_vocabulary: dict[str, set[str]] = field(default_factory=lambda: {"claim.confidence": set(), "action.action-name": set(), "state-change.what": set(), "lifecycle-transition.trigger": set()})` parallel to existing fields at lines 121-122. Pass to `check_event_references` at line 194-201.
- **`runtime/boot.py`**: extend existing loop (boot.py:153-159) to populate `substrate.registered_payload_vocabulary` from `result.payload_vocabulary_tables`.
- **`runtime/per_event_checks.py::check_event_references`**: add new parameter `registered_payload_vocabulary: Optional[dict[str, Iterable[str]]] = None`. After existing payload-subtype check (line 151), add four-slot validation loop per §B.1 Detection.
- **2 new tests** in `impl/tests/test_payload_vocabulary.py` (NEW file):
  - Test 1 — registered value accepted: extension manifest registers `payload-vocabulary-registrations: [{payload-slot: "action.action-name", value: "tool-invoked", spec-ref: ...}]`. Emit action event with `action-name: "ext-id:tool-invoked"`. Assert no rejection.
  - Test 2 — unregistered value rejected: emit claim event with `confidence: "unknown-grade"` (not registered). Assert `EventRejected(category="vocabulary")`; state unchanged; chain length unchanged.

Estimated impl size: **~40 LOC + 2 tests**. 195 baseline → 197 tests post-D59 [impl].

## D. What is NOT in this decision

- **D-1 — Payload-vocabulary versioning + deprecation lifecycle**: D33/D54 territory. When entries get amended across extension versions, migration-safety applies.
- **D-2 — `payload-claim.evidence-references[]` items**: opaque references (URIs/paths/qualified-ids), not vocabulary tokens. Future D-entry may bind them to reference-resolution discipline.
- **D-3 — Required-vs-optional registration semantics extension**: D59 locks FAIL on unregistered. Shape policy permissive mode (dev-time WARN-only) is shape-policy hook concern (D13 hooks), not framework-core.
- **D-4 — Registration scope (per-workspace vs per-extension)**: D59 follows D29 namespacing — registered values are extension-qualified. Workspace-scoped overrides out of scope.
- **D-5 — Cross-extension semantic equivalence**: two extensions registering same value with semantically equivalent intent; D29 keeps them distinct. Cross-ext alias declaration out of scope.
- **D-6 — `payload-action.parameters` object structure validation per action-name**: parameters schema is action-name-specific. Full per-action-name parameter-schema-fetch + validation surface separate.
- **D-7 — Phase D end-to-end exercise**: D59 locks contract + impl + tests with synthetic extension manifests. PractitionerShape-bearing extensions in Phase D will exercise end-to-end (e.g., `defensibility-grade` confidence values).

Other items NOT in this decision:

- **No retroactive rewrite of D29 / D10** — append-only ledger.
- **No change to the four payload schemas**.
- **No new typed exception** — reuses `EventRejected`.
- **No new FAILURE_CATEGORIES entry** — reuses existing `"vocabulary"` per D30 §3.
- **No change to canonical substrate step ordering** — D59 extends existing step 1's per-event check.

## Decision-shape template self-application

- **WHAT**: lock detection + surface + recovery for open-vocab payload-body slots — bind D29's vocabulary-registration mechanism to the four open-vocab payload slots inside core payload schemas.
- **WHO**: enforced by *framework-validator (B1)* — workspace.py step 7 merges `payload-vocabulary-registrations` into `payload_vocabulary_tables`. *substrate (runtime)* — substrate field `registered_payload_vocabulary` populated at boot; per_event_checks consults at runtime. *extension (registered)* — extension manifests declare per new slot.
- **FAILS**: *Detection*: audit at next checkpoint catches missing per-event check. *Surface*: audit findings + failing tests. *Recovery*: impl-follow-through closes; or supersedes sharpens.
- **CROSS**: D10 (payload-subtype schemas — D59 extends per-event runtime semantics on four core subtypes' open-vocab body slots); D13 (shape kind — payload-vocabulary may compose with shape authority-bindings; shape-compatible but not bound here); D17 (extensions add to open vocab — D59 extends to payload-body slots); D29 §"Vocabulary registrations" (parallel mechanism for payload-body slots; namespacing applies unchanged); D29 §"Validation flow" step 4 (extended to include payload-vocabulary merge); D30 §3 (vocabulary failure category reused); D30 §4 (per-event runtime checks — D59 adds new vocabulary sub-check); D33/D54 (versioning out of scope per D-1); D45 (standing requirement); D48 §E + D50 §E + D52 §E (FIRED precedent).
- **DEFERS**: per §D — D-1 through D-7.

## E. Pre-lock probe disposition

D59 **FIRED** per refined-skip rule + D48 §E + D50 §E + D52 §E precedent. NEW contract content:

1. **New extension-manifest slot** `payload-vocabulary-registrations`.
2. **New boot-time loader extension** populating new `payload_vocabulary_tables` field on ValidationResult.
3. **New per-event check site** — new vocabulary sub-check.

**Probe outcome**: D59 reuses existing `EventRejected` + existing `"vocabulary"` category (no new exception type, no new FAILURE_CATEGORIES entry) but adds new manifest slot + new boot loader + new per-event check site. Per V1 evidence: per_event_checks.py:134-151 payload-subtype check verified; substrate.py:121-122 vocabulary-table fields verified; workspace.py:264-268 merge loop verified; types.py:27 `"vocabulary"` present per D30 §3 verified. Quiet assumptions surfaced as §D D-1 through D-7.

## Rationale

D29 enumerated six top-level open-vocab slots but did NOT include payload-body open-vocab slots. The four payload schemas describe their open-vocab string slots as "shape-policy or extension-defined" — but no D-entry locked the registration mechanism. D59 closes that gap with minimum-viable mechanism: one new manifest slot, one boot-time merge, one per-event check, reusing existing `EventRejected` + `"vocabulary"` category.

Per the durability bet: D59 is **specification** — manifest slot shape + runtime table contract + check semantics. Phase D PractitionerShape-bearing extensions will populate tables with real values; D59 makes the framework capable of enforcing whatever vocabulary extensions declare.

Honest cluster sizing: 1 path with 4 surface slots (not 4 paths). Structural uniformity of validation logic — same merge loop, same per-event check shape, same failure category — argues for single-path scope.

**Cross-references**: D5 §I3 (accountability — payload-body values subject to vocabulary registration); D7 §3 (workspace state — D59 extends boot-time vocabulary-table population); D10 (event kind — four core payload-subtypes carry registered open-vocab slots); D13 (shape kind — payload-vocabulary composable with authority-bindings); D17 (extensions add to open vocab); D29 §"Vocabulary registrations" (parallel mechanism); D29 §"Validation flow" step 4 (extended); D30 §3 (vocabulary failure category reused); D30 §4 (per-event runtime checks); D33/D54 (versioning out of scope); D44 (queued dispatch preserved); D45 (standing requirement); D46 (precedent for reuse-existing-typed-exception); D48 §E + D50 §E + D52 §E (FIRED pre-lock-probe precedent); probing.md §"Pattern-completion over pattern-questioning"; probing.md Procedure 3 refined-skip rule.

## Honest basis caveats

- **Read directly**: README + CLIPPY-COMPANION + probing.md + D29 + D30 + D45 + D52 + 4 payload schemas + per_event_checks.py (full) + validator/extensions.py + validator/workspace.py + substrate.py vocabulary wiring + types.py.
- **Claimed but not Read this session**: `schemas/extension-manifest.schema.json` exact current shape (claim "add optional array property" inferred from D29 §2 + existing vocabulary-registrations parallel; impl-follow-through must Read before adding slot).
- **Flagged-pending-Read for next turn**: extension-manifest schema exact current properties list (load-bearing for §C; Read at impl-start).
- **Inferred**: test count "197 post-D59 [impl]" arithmetic only; LOC estimate "~40" projection.
