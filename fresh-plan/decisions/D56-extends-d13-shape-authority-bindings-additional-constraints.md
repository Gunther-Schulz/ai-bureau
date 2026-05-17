# D56 — 2026-05-17 — Extends D13 — shape.authority-bindings[].additional-constraints interpretation layer + minimal grammar

**Decision (substantive; extends D13 contract — operationalizes a currently-decorative slot)**: The `additional-constraints` slot on each `shape.authority-bindings[]` tuple (D13 — currently a free-form string at the schema layer per `shape.schema.json:72` and never consumed by `Shape.check_authority` per `shape.py:108-145`) gains an interpretation layer + a minimal structured grammar. Evaluated INSIDE `Shape.check_authority` as an additional pass over each binding that already matched on `payload-subtype` + `qualifier` + `required-role` + `required-actor-subtype` — extending the existing per-event authority surface rather than introducing a new check class. Two failure modes per D45 triad: (1) boot-time grammar parse-failure → new `WorkspaceBootError(category="authority-constraint-grammar")` per D46 pattern; (2) per-event evaluation-failure → reuses existing `EventRejected(category="authority")` (extends the authority-failure surface; no new category for the per-event path). Composes with D52 (different failure-mode dimension: D52 is post-projection state validity; this is per-event binding-level constraint over event-fields + actor metadata). Pre-lock probe FIRED per probing.md Procedure 3 refined-skip rule + D48 §E + D50 §E + D52 §E precedent (new contract content: new grammar + new boot-time check + new FAILURE_CATEGORIES entry).

## A. Scope of cluster

**Honest cluster cardinality: 1 path**. Cluster supersedes phase per D45 §C completed at D52; this entry is an EXTENDS-D13 operationalization of a currently-decorative slot, motivated by the same audit pattern (decorative-contract-cited-as-rationale-not-applied-as-check) but distinct in shape from the six D45 §C clusters.

The path:

- **A.1 Per-event additional-constraints evaluation**: `shape.authority-bindings[i].additional-constraints` (defined at `shape.schema.json:72` as free-form `{"type": "string", "minLength": 1}`; one in-repo example at `schemas/examples/shape-practitioner.json:15` carrying English prose). Currently NEVER consumed: `Shape.check_authority` (shape.py:108-145) matches each binding on payload-subtype + qualifier + role + actor-subtype only; the constraint string — if present — is silently ignored. D56 closes this gap with a minimal structured grammar evaluated at shape.check_authority match-time.

**Distinction from existing checks**:
- `per_event_checks.check_event_references` owns identity resolution.
- `shape.check_authority` owns per-event authority-binding match (role + actor-subtype).
- D56's extension to `check_authority` owns per-event additional-constraints evaluation over event-fields + actor metadata.
- D52's `check_post_event_state_validity` owns post-projection state-level cardinality.

Four distinct surfaces; D56 sharpens the authority surface from "role+subtype only" to "role+subtype + structured per-binding predicate."

Out of scope (per §D):
- Full DSL design (operators, nesting, regex, cross-event-chain lookups) — Phase D PractitionerShape concern per D42.
- Cross-binding constraint composition.
- Constraint idempotence / referential transparency assumptions.
- Constraint evaluation cost budgeting.
- Pioneer-instance practitioner-shape canonical constraints (e.g., rewriting `shape-practitioner.json:15` English prose as structured form).

## B. Triad applied per path

### B.1 — Per-event additional-constraints evaluation

| Triad element | Lock |
|---|---|
| **Detection** | At Shape `__init__` / boot-time (parse-once): for each `authority-bindings[i]` with non-empty `additional-constraints`, parse the string against the minimal grammar (§B.1.1 below). Parse failures surface as `WorkspaceBootError(failures=[ValidationFailure(category="authority-constraint-grammar", path=f"shape.authority-bindings[{i}].additional-constraints", reason=…)])` per D46 boot-error pattern. Parsed constraint is cached on the binding (in-memory only). At per-event time inside `check_authority` (shape.py:108-145): after a binding matches on payload-subtype + qualifier + required-role + required-actor-subtype (the existing `if not matched:` branch at shape.py:129), if the binding carries a parsed constraint, evaluate it against `(event, matched-actor-record, state)`. False evaluation → constraint unsatisfied. |
| **Surface** | Boot-time parse-failure: `WorkspaceBootError(category="authority-constraint-grammar")` per existing pattern. NEW `FAILURE_CATEGORIES` entry. User sees the diagnostic without reading logs (per D45 surface bar). Per-event evaluation-failure: REUSES existing `EventRejected(category="authority")` — appends one `ValidationFailure(category="authority", path=f"event.actors[{matched-actor-index}]", reason=...)`. Extends the authority-failure surface; does NOT introduce a per-event-time `authority-constraint-grammar` category (grammar is boot-time only by construction). |
| **Recovery** | Boot-time: workspace boot aborts cleanly per D45 + D46. Caller fixes the shape spec's constraint string. State not partially constructed. Per-event: event rejected at substrate step 2 (existing authority-check step; no new step). State NOT mutated. Chain integrity preserved per D10 + D39. Caller fixes the emitting actor's payload OR adjusts which actor emits OR adjusts the shape's binding constraint declaration. |

#### B.1.1 — Minimal grammar

Form: a JSON object (parsed FROM the string slot for back-compat with the schema's `{"type": "string"}` declaration; future schema amendment may admit object directly per §D D-6). Top-level object MUST carry exactly one of:

- **`equals`**: `{ "lhs": "<path>", "rhs": "<path>" }` — passes when the value at `lhs` equals the value at `rhs`. Each path is one of:
  - `event.payload.<key>` — looks up `event["payload"][<key>]`
  - `event.actor.<key>` — looks up the matched-actor-record's field
  - `state.shape-config.<key>` — looks up `state.shape_config[<key>]` (NEW workspace-state slot; see §C + §D D-7)
  - `literal:<string>` — literal string value
- **`in`**: `{ "lhs": "<path>", "rhs": [<literal>, …] }` — passes when the value at `lhs` is in the literal list.

Top-level absent / empty-string slot value: NO constraint (pass; back-compat with current decorative use).

Unknown top-level keys, malformed path strings, unresolved path lookups at per-event time: all FAIL CLOSED (no silent substitution per global CLAUDE.md). Boot-time grammar parse covers structure; per-event path resolution covers data presence — both surface explicitly.

#### B.1.2 — Composition with D52

D52 §B.1 enforces post-projection state validity (cardinality over actor population). D56 §B.1 enforces per-event binding-level predicate over event-fields + matched-actor metadata + shape-config state. Different failure-mode dimensions; no overlap.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

- **Grammar parser** in NEW module `impl/src/fresh_plan/runtime/authority_constraint.py` (~15 LOC). Parses JSON-from-string per §B.1.1; returns a small dataclass holding parsed form. Raises `AuthorityConstraintGrammarError` (module-local); caller (`Shape.__init__`) wraps into `WorkspaceBootError(category="authority-constraint-grammar")`.

- **`Shape.__init__` boot-time parse** in `impl/src/fresh_plan/runtime/shape.py`. Override `__post_init__` to iterate `self.spec["authority-bindings"]`; for each binding with non-empty `additional-constraints`, parse + cache on sibling list `self._parsed_constraints`. On parse failure, raise `WorkspaceBootError`.

- **`Shape.check_authority` extension** at shape.py:108-145. After the `if not matched:` branch (currently at shape.py:129), if `matched is True` AND `self._parsed_constraints[binding_index]` is not `None`, evaluate the constraint against `(event, matched_actor_record, state)`. False evaluation → append `ValidationFailure(category="authority", …)` per existing pattern. ~10 LOC added.

- **`FAILURE_CATEGORIES` extension** in `impl/src/fresh_plan/validator/types.py`: add `"authority-constraint-grammar"`.

- **NEW workspace-state slot `state.shape_config`** (per §B.1.1 path `state.shape-config.<key>`). Default empty dict; populated by future D-entry from manifest shape-config block. For Phase B tests, monkeypatch `workspace.state.shape_config` directly. **OPEN QUESTION** (per §D D-7): whether state slot population pathway lands in D56 impl follow-through or in a companion entry. D56 locks only the path-lookup; population pathway deferred.

- **3 new tests** in `impl/tests/test_authority_constraint.py` (NEW file):
  - Test 1 — equals pass.
  - Test 2 — equals fail → `EventRejected(category="authority")` citing the constraint.
  - Test 3 — boot-time grammar parse-failure → `WorkspaceBootError(category="authority-constraint-grammar")`.

Estimated impl size: **~25 LOC + 3 tests**. Baseline (post-D52) 195 → +3 post-D56 [impl].

## D. What is NOT in this decision

- **D-1 — Full DSL design**: `equals` + `in` are minimum viable; richer operators (boolean composition, arithmetic, regex match, set ops, cross-event-chain lookups, temporal predicates) deferred to Phase D PractitionerShape per D42.
- **D-2 — Cross-binding constraint composition**: e.g., "binding A's matched actor must equal binding B's matched actor across event chain." Phase D concern.
- **D-3 — Idempotence / referential-transparency**: D56's grammar is referentially transparent (lookups deterministic over `(event, actor-record, state)`). Future operators that break this would need explicit lock.
- **D-4 — Constraint evaluation cost**: D56 assumes O(1)-per-binding. Cost budgeting deferred.
- **D-5 — Pioneer-instance practitioner-shape canonical constraints**: `shape-practitioner.json:15`'s English prose remains decorative under D56's impl (would FAIL parse if non-empty). Phase D PractitionerShape will rewrite as structured grammar OR remove.
- **D-6 — Schema amendment to admit object directly**: D56 keeps schema slot as `{"type": "string"}` (back-compat) + parses JSON FROM the string. Future schema amendment could admit object-typed constraint directly.
- **D-7 — `state.shape_config` slot population pathway**: §C declares the path lookup `state.shape-config.<key>` and the state slot's existence (default `{}`). The pathway from MANIFEST to `state.shape_config` is NOT locked here. Companion D-entry candidate; tracked as Bref-followon.

Other items NOT in this decision:

- **No retroactive rewrite of D13** — append-only ledger.
- **No new typed exception for per-event evaluation-failure** — reuses `EventRejected(category="authority")`. NEW typed exception only at boot-time (via WorkspaceBootError; existing class), with NEW category `authority-constraint-grammar`.
- **No new substrate step** — extends existing step 2 (authority check) per D47 §C + D52's step-ordering scheme. Step count remains 10.

## Decision-shape template self-application

- **WHAT**: lock interpretation layer + minimal grammar for `shape.authority-bindings[].additional-constraints`. Operationalizes a currently-decorative D13 slot.
- **WHO**: enforced by *shape (policy)* — `Shape.__init__` parses grammar at boot; `Shape.check_authority` evaluates parsed constraints at per-event time. *substrate (runtime)* — unaffected at step ordering. *framework-validator (B1)* — unaffected.
- **FAILS**: *Detection*: detection-surface-recovery audit at next checkpoint. *Surface*: audit findings list + failing tests if impl regresses. *Recovery*: impl-follow-through commit closes; or supersedes entry sharpens.
- **CROSS**: D10 (event kind); D13 (shape kind — slot now consumed); D45 (standing requirement); D46 (precedent for `WorkspaceBootError(category=…)`); D47 §C (canonical step ordering preserved — no new step); D48 §E + D50 §E + D52 §E (FIRED precedents); D52 §B.1 (composition — different failure-mode dimension).
- **DEFERS**: per §D — D-1 through D-7.

## E. Pre-lock probe disposition

D56 **FIRED** the pre-lock probe per refined-skip rule + D48 §E + D50 §E + D52 §E precedent. NEW contract content:

1. **New grammar + parser**: §B.1.1 grammar is new contract content.
2. **New boot-time check**: `Shape.__init__` grammar-parse failure as `WorkspaceBootError`.
3. **New FAILURE_CATEGORIES entry**: `"authority-constraint-grammar"`.

**Probe outcome**: load-bearing code claims verified — shape.schema.json:72 string-type free-form (Read); shape-practitioner.json:15 English-prose example (grep); shape.py:108-145 `check_authority` does NOT consume `additional-constraints` (Read; no `additional_constraints` symbol in the file). Quiet assumptions surfaced + named as §D D-1 through D-7. **Open question surfaced inline** (not swept): the `state.shape_config` population pathway (§D D-7).

## Rationale

The 2026-05-12 audit's underlying pattern — *decorative-contract-cited-as-rationale-not-applied-as-check* — surfaced six runtime-path clusters (D45 §C) closed by D46-D52. The `additional-constraints` slot is the SAME pattern at finer granularity: contract slot present at schema + ledger layer (D13), never consumed by impl. Closing this gap honors the standing D45 requirement on the per-event authority surface without inflating it into a fictional D45 §C item 7. The entry shape is EXTENDS-D13 rather than cluster-supersedes.

Per the durability bet: D56 is specification — typed exception (reused EventRejected + NEW category for boot-time grammar) + grammar contract + check-method extension. Phase D PractitionerShape will populate real constraints — most likely starting by replacing `shape-practitioner.json:15`'s English prose with a structured `equals` constraint citing `state.shape-config.required-attester` per D-5.

Honest 1-path scope per D50 + D52 precedent. Scope-cardinality-honesty discipline applied.

**Cross-references**: D5 §I3 (accountability — operationalized by additional-constraints sharpening per-event authority); D10 (event kind); D13 (shape kind — slot now consumed at runtime; schema string-type preserved); D29 §validation flow (D56 extends boot-time validation with grammar parse); D30 §4 (per-event runtime checks — D56 extends step 2 authority check); D34 §A.5 (current-state resolution preserved); D39 (state-fully-derived preserved; check runs before append at step 2); D42 (Phase D PractitionerShape — destination for full DSL design per D-1 + D-2 + D-5); D44 (queued dispatch preserved); D45 (standing requirement); D45 §C (clusters complete at D52); D46 (precedent for WorkspaceBootError); D47 §C (canonical step ordering preserved); D48 §E + D50 §E + D52 §E (FIRED precedents); D49 §A (step-count 10 preserved); D52 §B.1 (composition — different failure-mode dimension); probing.md §"Pattern-completion over pattern-questioning"; probing.md Procedure 3 refined-skip rule.

## Honest basis caveats

- **Read directly**: README + CLIPPY-COMPANION + probing.md + D13 + D31 + D45 + D52 + shape.schema.json + shape.py (full) + validator/types.py (full) + boot.py:30-150 + grep for `additional-constraints` (only schemas; no impl).
- **Cited via other entries' summaries (not freshly Read)**: D46 (precedent inferred from D52 cross-citations + FAILURE_CATEGORIES annotations); D47 §C (canonical step ordering — cited via D52's restatement); D48/D50 §E FIRED precedent wording (cited via D52).
- **Inferred**: §C line-pin at shape.py:129 verified against Read; LOC estimate (~25) scaled from D52 (~30-40); test count ("198 post-D56 [impl]") arithmetic only.
- **Open / Flagged**: §C `state.shape_config` slot — §D D-7 explicitly Flags whether this lands in D56 impl follow-through or companion entry.
