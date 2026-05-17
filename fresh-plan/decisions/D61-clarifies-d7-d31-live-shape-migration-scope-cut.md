# D61 — 2026-05-17 — Clarifies D7 + D31 — live in-place shape migration is a deliberate scope-cut; shape changes require workspace reboot

**Decision (clarifies D7 §2 + D31; reads off `payload-composition-change.schema.json:22-24`)**: The `binding-kind` enum in `schemas/payload-composition-change.schema.json` deliberately **EXCLUDES** `shape`. The enum admits `["substrate-binding", "adapter-binding", "specialist-binding", "actor", "extension"]` (lines 22-24); `shape` is not a valid `binding-kind` value. Live in-place shape migration mid-workspace-lifetime is **NOT** supported via composition-change events. Shape changes require **workspace reboot** under a new shape version. The exclusion is a scope-cut, not an oversight; D61 makes the implicit explicit at ledger layer.

### Substantive grounding

The scope-cut is anchored in three locked decisions:

- **D7 §2** (workspace composition cardinality): `shape: exactly 1 (the workspace is shape-typed; hybrid-shape mechanics deferred)`. A workspace is shape-*typed* — the shape is part of identity, not part of mutable composition. Other binding-kinds (substrate-binding `1+`; adapter `0+`; specialist `0+`; actor `1+`) carry cardinality semantics that admit mutation during lifecycle (D7 §4 "Composition is mutable"); shape's `exactly 1` reflects identity-tied cardinality.
- **D4** (framework-core has no substantive identity commitments) + **D31** (`extends` removed from shape): shape carries the workspace's substantive identity — the durable frame within which the event chain accumulates. Mid-life shape mutation would conflate the durable substantive frame with the event-history that frame interprets.
- **`payload-composition-change.schema.json:22-24`** binding-kind enum: the schema-level constraint enforces the scope-cut. Composition-change events that name `binding-kind=shape` fail schema validation; framework rejects them at the validation surface (per D29 / D51).

The workspace boundary is the migration surface. Across reboots, the event chain is preserved per D39 (state-is-fully-derived-from-event-chain); the new shape applies **prospectively** from boot — it interprets the prior event chain under its own policies (authority-bindings; hooks; actor-requirements per D52). This composes cleanly with D54 migration-safety: D54 formalizes shape-version transition discipline at boot; D61 makes explicit that boot is the **only** transition surface — there is no live-migration alternative.

### What is NOT in this clarification

- **Live in-place shape migration discipline** — explicitly rejected here with principled grounding (identity-tied cardinality per D7 §2 + substantive-identity-carrier per D4 + D31). If Phase D pioneer surfaces a concrete use-case requiring it, that requires a supersedes entry, not a clarification.
- **Cross-shape composition** — D7 §2 hybrid-shape mechanics deferred; D31 removed `extends` for the analogous reason. Neither composition nor mixin nor overlay enters via D61.
- **Multi-shape workspaces** — D7 §2 mandates exactly 1.
- **D54 migration-safety details** — D54 owns boot-time shape-version transition; D61 anchors the boundary (boot, not live), not the transition mechanics.
- **`change-type=update` for other binding-kinds** — D52 §D D-4 names this gap; D61 does not extend or close it.

## Decision-shape template self-application

- **WHAT**: lock the deliberate scope-cut of `shape` from `payload-composition-change.binding-kind` enum at ledger layer. Retroactive clarification of an existing schema constraint. Workspace reboot is the sole shape-transition surface.
- **WHO**: enforced by **framework-validator (B1)** at composition-change schema validation — schema enum rejects `binding-kind=shape` at validation step (D29 + D51 coverage). Enforced by **substrate (runtime)** at append_event — schema validation runs before substrate step 1. Enforced by **deferred (Phase D / future supersedes)** for any future live-migration mechanism if pioneer evidence forces one.
- **FAILS** (recursive — what happens if a workspace impl tries to bypass this?): a composition-change event with `binding-kind=shape` fails schema validation before substrate step 1; never reaches the event chain; never mutates state. Workspace impls cannot silently substitute live shape mutation — schema enum is the structural backstop.
- **CROSS**: D4 (substantive identity = shape policy; D61 reads off this); D7 §2 (shape exactly-1 cardinality — identity-tied constraint); D7 §4 (composition is mutable but shape is excluded); D10 (event kind — composition-change is core payload-subtype; D61 narrows its scope at binding-kind enum); D13 (shape kind contract); D29 §validation flow (validation surface enforcing schema enum); D31 (`extends` removed; analogous "no live mutation mechanism" rationale); D39 (event chain preserved across reboots — composes with boot-as-migration-surface); D51 (validation cluster — enforces schema constraints including binding-kind enum); D52 §D D-4 (composition-change:update unimplemented; D61 doesn't close this related gap); D54 (migration-safety at boot — composes with D61's boot-as-migration-surface anchor).
- **DEFERS**: live-migration discipline (rejected with grounding); cross-shape composition (D7 + D13 deferred); multi-shape workspaces (D7 mandates 1); D54 migration-safety mechanics (separate entry).

## E. Pre-lock probe disposition

**SKIPPED** per probing.md Procedure 3 refined skip rule + D45 §E + D46 / D47 / D51 §E precedent: D61 is pure clarification — locks an existing schema constraint at ledger layer. No new contract content; no new typed exception; no new category vocabulary; no new sub-procedure. The binding-kind enum is already locked in schema; this entry makes the scope-cut's rationale explicit and names the principled grounding (D4 + D7 §2 + D31) for why `shape` was excluded.

## Rationale

The schema-level exclusion of `shape` from `binding-kind` has stood since composition-change schema landed, but the rationale lives implicit across D4 (substantive-identity-as-shape-policy) + D7 §2 (shape exactly-1) + D31 (no live mechanism for shape variation). A future reader asking "why can't I emit a composition-change to swap shape?" today must reconstruct rationale from three entries + a schema; D61 closes that trace: D7 §2 (cardinality) → D31 (no mechanism precedent) → schema enum (structural enforcement) → D61 (explicit ledger anchor).

This pre-empts the post-hoc fault-mode where Phase D pioneer impl notices the gap, lacks principled framing, and either (a) lobbies for live-migration without confronting substantive-identity cost, or (b) hacks around the constraint by emitting events with semantically-shape-changing-but-binding-kind-misdeclared payloads. D61 names the constraint **and** its principled grounding so future debate starts from the locked rejection.

Composes with D54 migration-safety: D54 owns boot-time shape-version transition discipline (manifest version change → reboot → new shape applies prospectively → event chain preserved per D39). D61 anchors the migration surface (boot, not live); D54 fills in boot-time mechanics. The two compose without overlap.

**Cross-references**: D4 (substantive identity = shape policy — principled grounding for shape's identity-tied cardinality); D7 §2 (shape exactly-1; identity-tied constraint); D7 §4 (composition is mutable but shape is exception); D10 (composition-change is core payload-subtype; D61 narrows scope); D13 (shape kind contract); D29 §validation flow (surface enforcing schema enum); D31 (`extends` precedent — no live mutation mechanism); D38 (precedent for "no new kind; existing primitives carry the load" — analogous "no new mechanism; boot is the surface"); D39 (event chain preservation across reboots); D45 §E + D46/D47/D51 §E (SKIP precedent for pure clarification); D51 (validation cluster — enforces schema constraints); D52 §D D-4 (composition-change:update gap — related but not closed here); D54 (companion entry — migration-safety at boot); payload-composition-change.schema.json:22-24 (schema-locked enum that D61 anchors at ledger layer).

## Honest basis caveats

- **Read directly**: D7 (full); D31 (full); D38 (full); D49 + D52 (style); payload-composition-change.schema.json (full; lines 22-24 confirm enum excludes `shape`).
- **Claimed but inferred from session context**: D4 named as "substantive identity = shape policy" — D31's cross-references line cites this; D4 itself not re-read this session.
- **Claimed but inferred from session context**: D54 being "boot-time shape-version transition discipline" — locked earlier this session (commit ba64478); not re-read for this entry but content fresh in session memory.
- **Claimed but inferred from session context**: D29 §validation flow + D51 enforcing binding-kind enum at validation surface — grounded in D52's cross-references; D29 + D51 not re-read this session.
- **Claimed but inferred from session context**: D39 event-chain preservation across reboots — grounded in D52's body; D39 itself not re-read this session.
- **Not verified this session**: actual schema validation runtime path (where in substrate pipeline the binding-kind enum check runs) — surfaced by D52's body but specific code path not traced.
