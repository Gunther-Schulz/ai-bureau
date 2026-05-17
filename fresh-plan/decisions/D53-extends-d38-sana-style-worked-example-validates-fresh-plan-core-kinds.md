# D53 — 2026-05-17 — Extends D38 — Sana-style worked-example validates fresh-plan core kinds against knowledge-work use case

**Decision (substantive; worked-example validation per Bref deliverable #6)**: A concrete Sana-style worked example — corpus-grounded knowledge agent retrieving from + writing back into a curated corpus, with curator + consumer roles + citation/provenance hooks — is locked as the validation artifact for D38's rejection-of-knowledge-as-core-kind. The 8 fresh-plan kinds (D25) map cleanly to the Sana-style use case via existing primitives (D16 adapters + D10 events + D13 shape policy) per D38's claim; no new framework-core gap surfaces. Worked example extends the existing B7 RAG-via-MCP fixture (workspace-rag-via-mcp; verified at fresh-plan/impl/tests/fixtures/workspace-rag-via-mcp/workspace.json) into a more Sana-shaped composition (knowledge-shape with curator/consumer authority-bindings + citation hooks + write-back adapter) — exercising the full kind set rather than just specialist+adapter as B7 does. Pre-lock probe SKIPPED per probing.md Procedure 3 refined-skip rule + D45 §E / D46 / D47 / D51 precedent: D53 is pure pattern application — no new typed exception, no new FAILURE_CATEGORIES entry, no new composition framing. Cluster-supersedes phase per D45 §C completed at D52; D53 begins post-cluster Bref deliverable closure work (deliverables #5 D33 migration-safety [next entry] + #6 D38 Sana worked-example [this entry] + Bref output + Phase B closure).

## A. Scope of cluster

D53 locks one artifact: a `workspace-sana-style` fixture + accompanying `test_sana_style.py` that exercises the full 8-kind composition under a knowledge-platform-style use case, validating D38's claim that knowledge decomposes across existing kinds.

**Honest cardinality: 1 worked example**, not multiple use-case variations. Per Clippy upstream D1 scope-cardinality-honesty sub-check + D49 first-pass lesson — do NOT inflate to multi-fixture sweep mirroring B-workstream scope (B3 / B6 / B7 each landed one canonical fixture). Sana-style is one shape exemplar; future shapes (Kore.ai-style template-marketplace; AEGIS-style integrity-protocol) are separate worked examples if/when they land.

What this entry validates (positive claim — gap-free) AND what it deliberately does NOT (honest limit):

- **Validates**: D38's rejection of `knowledge` kind holds against a substantive Sana-style scenario — curator-curates / consumer-cites / agent-retrieves-and-writes-back all expressible via D13 shape policy + D16 adapters + D10 events + D19 specialists, with no contract gap surfacing.
- **Does NOT validate**: that fresh-plan is a *better* answer than Sana's knowledge-as-core thesis for knowledge-centric deployments. That's positioning work, explicitly deferred per market-context.md "positioning is deferred" discipline. D53 is a structural-coverage validation, not a competitive-positioning artifact.

## B. The Sana-style use case + 8-kind mapping

**Use case framing**. Sana AI (acquired by Workday 2025; market-context.md cited) positions knowledge as the central artifact — agents are tools operating over a curated corpus. The Sana-style fresh-plan scenario: a knowledge-shape workspace where two human-actors (curator + consumer roles) and one agent-actor compose around a corpus of documents. Curators ingest/annotate/curate documents; consumers query and cite; the agent retrieves on demand + writes back synthesized notes that re-enter the corpus. Citations attach provenance back to corpus documents. The corpus IS knowledge-as-supporting-infrastructure (per D38's I3 framing) but is NOT a framework-core kind — it lives behind a knowledge-store adapter, its events are workspace events, and its policy is shape policy.

**8-kind mapping**:

| Kind | Sana-style instantiation | Maps via |
|---|---|---|
| **workspace** (D7) | `sana-style-ws` — bounded scope around one corpus + one curator team + one knowledge-agent | Existing manifest schema; no extension |
| **actor** (D9 + D22) | `curator-1` (human-actor; role=curator); `consumer-1` (human-actor; role=consumer); `kb-agent` (agent-actor) | Existing actor.schema.json subtypes |
| **event** (D10 + D23) | claim events carry assertional content (per D10) — curator-attestations + agent-syntheses; action events for retrieve/cite/write-back; composition-change events for actor additions; lifecycle for boot/shutdown | D10 payload-subtypes; no new subtype |
| **substrate** (D12 + D17) | `inprocess-substrate-ext:inprocess-substrate` (same as B7) — Phase B mocked substrate | Existing; same as workspace-rag-via-mcp |
| **shape** (D13) | NEW `sana-knowledge-shape` — declares authority-bindings (only role=curator may emit claims into the corpus-write-back path; consumers may emit claims with citation requirement); roles (curator, consumer); hooks (`pre-citation` validates cited-evidence-references resolve to chain events; `post-corpus-write` projects synthesis claim into corpus adapter); actor-requirements (`{human-actor: {min: 1}}` for at-least-one-curator) | D13 policy bundle; per D38 §3 "knowledge-centric shape declares roles like curator/consumer and hooks like pre-citation" |
| **adapter** (D16) | TWO adapters reusing `mcp-server-ext:mcp-client` protocol per D38 §1 (retrieval-shaped adapters): (a) `knowledge-retriever-adapter` — read corpus chunks (extends B7 rag-retriever-adapter); (b) `knowledge-writer-adapter` — write back synthesis notes (NEW) | Existing adapter.schema.json protocol-or-transport openness |
| **specialist** (D19) | `knowledge-agent-specialist` — supports work-unit-kinds `[retrieval-task, synthesis-task]`; required-adapter-bindings `[knowledge-retriever-adapter, knowledge-writer-adapter]`; declared-event-emissions `[claim, action]` | Existing specialist.schema.json |
| **work-unit** (D20) | `synthesis-task` work-unit-kind (NEW; extension-registered) — payload carries query + draft-synthesis fields; lifecycle uses fixed core enum (created/in-progress/completed) | D20 fixed core lifecycle + extension-registered kind-discriminator |

**Citation/provenance** is the load-bearing Sana-style mechanism. In the worked example: when `kb-agent` emits a synthesis claim, the shape's `pre-citation` hook validates that the claim's `evidence-references` (verified slot at schemas/payload-claim.schema.json:21) resolve to events in the chain — corpus-fetch action events from the retriever adapter. This binds synthesis-claims to retrievable evidence via the event chain (D40 projection / query). No new framework primitive required.

**Closure verification**: every Sana-style mechanism named in D38's text (retrieval-shaped adapters § §1; claim payloads carry assertional content § §2; shape declares curator/consumer + pre-citation § §3) maps to a kind. No leftover Sana-style mechanism requires a NEW kind.

## C. Impl follow-through (separate commit; tracked in roadmap.md)

The validation is **a fixture + tests**, not framework runtime changes. Specific changes:

- **New fixture** `impl/tests/fixtures/workspace-sana-style/` mirroring B7 fixture structure:
  - `workspace.json` — composition manifest binding `inprocess-substrate-ext` + new `sana-knowledge-shape-ext` + `mcp-server-ext` + new `sana-style-ext` (knowledge-retriever + knowledge-writer adapters + knowledge-agent specialist + synthesis-task work-unit-kind)
  - `extensions/sana-knowledge-shape-ext/0.1.0/` — shape extension with authority-bindings + hooks + actor-requirements + roles
  - `extensions/sana-style-ext/0.1.0/` — adapter + specialist + work-unit-kind extension specs
  - Reuses `inprocess-substrate-ext` + `mcp-server-ext` unchanged

- **New test file** `impl/tests/test_sana_style.py` — 4-6 tests exercising:
  1. Boot succeeds; all 8 kinds present in workspace; shape attached + hooks registered
  2. Curator emits curate-claim (role=curator, payload carries corpus-document reference) → accepted; chain event present
  3. kb-agent invokes `retrieve` skill → action event emitted via retriever adapter; outcome-reference present
  4. kb-agent invokes `synthesize` skill → action event + synthesis-claim emitted; pre-citation hook resolves `evidence-references` against prior retrieve action events; passes
  5. Synthesis-claim missing `evidence-references` → pre-citation hook raises → EventRejected (validates D38 §3 hook-based knowledge discipline)
  6. State replay via D40 `state_at(n)` reconstructs corpus-write-back projections deterministically from chain (validates D38 §2: workspace state event projections carry assertional content)

- **No changes to framework src/** — D53 validates contracts already locked. If the fixture build surfaces a real gap, that lands as a separate D-entry (D54+) with its own §C scope. Per honest-claim discipline: if a gap surfaces during impl, do NOT silently extend D53's scope; surface explicitly + lock separately.

- **Estimated impl size**: ~150 lines fixture JSON + ~120 lines test code + ~80 lines stub specialist/adapter Python impl in `sana-style-ext`. Tests pass count: 195 baseline → 200-201 post-D53.

Phase D PractitionerShape will later instantiate a different shape (per D26 + D38 — PBS-Schulz is practitioner-shape, not knowledge-shape); D53's sana-knowledge-shape is a NEW generic-tier shape exemplar, not a Phase D shape. Per "Generic vs pioneer-instance discipline" (README Working patterns) — keep deliberately neutral.

## D. What is NOT in this decision

- **D-1 — Real Sana-AI-product compatibility**: D53 validates D38's structural claim. It does NOT claim fixture-fidelity-to-Sana-AI's actual API, schema, or operational semantics. Sana is a closed commercial product; the fixture is a fresh-plan-shaped abstraction of the public-knowledge thesis per market-context.md, not a Sana-product clone.
- **D-2 — Positioning competition vs Sana**: deferred per market-context.md "positioning is deferred" discipline. D53 is structural; positioning lands later (Phase D or later).
- **D-3 — Multi-shape worked-example coverage**: D53 locks one Sana-style fixture. Kore.ai-style and AEGIS-style worked examples are separate future entries if/when locked.
- **D-4 — Pre-citation hook semantics for non-claim payload-subtypes**: D53 scopes pre-citation to claim events. Action / state-change / composition-change events with embedded citation requirements are out of scope; future shape-policy-extension work.
- **D-5 — Phase C+ standards-compatibility (PROV-O / W3C citation vocab) alignment**: D38 already names knowledge-via-existing-primitives; standards-compat mapping is deferred per D24 + roadmap Phase C standards-engagement work.
- **D-6 — Knowledge-shape's interaction with integrity-protocol extension (D40 / AEGIS)**: deferred; cross-shape composition is Phase D+ work.

## E. Pre-lock probe disposition

D53 **SKIPS** the pre-lock probe per probing.md Procedure 3 refined-skip rule + D45 §E / D46 / D47 / D51 precedent: D53 is PURE pattern application (no new typed exception, no new FAILURE_CATEGORIES entry, no new composition framing, no new sub-procedure). It validates an existing locked decision (D38) via a worked-example artifact — the canonical fresh-plan "concrete examples before locking" discipline (README Operating disciplines) applied post-hoc to validate D38's structural claim.

This distinguishes from D48 / D50 / D52 §E FIRED precedent (those introduced new contract content).

**If the fixture build surfaces a real gap**, that is a NEW D-entry per §D D's "FAILS" recovery path — not a retroactive probe-fire on D53. Worked-example validations either confirm closure (D53 locks; impl follows clean) or surface gaps (D53 still locks at this scope; gap-finding becomes D54+).

## Decision-shape template self-application (per probing.md Procedure 1)

- **WHAT**: lock a worked-example fixture validating D38's rejection-of-knowledge-as-core-kind via the 8-kind mapping table in §B.
- **WHO**: enforced by *framework-validator (B1)* — boot must succeed (validates schema + composition); *substrate (runtime)* — events must dispatch + chain correctly; *shape (policy)* — pre-citation hook firing exercises the knowledge-shape contract; *specialist (impl)* — knowledge-agent stub satisfies D19 contract.
- **FAILS**: if the fixture build surfaces a real framework-core gap (e.g., no slot for citation references; no policy hook for pre-emit knowledge-validation), that's a finding requiring a SEPARATE D-entry (D54+), not silent extension of D53. *Detection*: fixture build + test run during §C impl follow-through. *Surface*: failing tests / impossible-to-express fixture. *Recovery*: lock new D-entry naming the gap; D53 stays as scoped.
- **CROSS**: D7 §workspace state (composition + actors); D10 + D23 (claim event slots; evidence-references at payload-claim.schema.json:21); D13 (shape policy bundle — knowledge-shape uses authority-bindings + hooks + actor-requirements + roles); D16 (retrieval-shaped + write-back-shaped adapters); D19 (knowledge-agent specialist); D20 (synthesis-task work-unit-kind); D25 (8-kind closure being validated); D26 Phase B (B7 RAG-via-MCP precedent); D38 (the claim being validated — knowledge decomposes across existing kinds); D40 (state replay used by test 6); D52 (post-projection state validity — sana-knowledge-shape's actor-requirements exercises D52's new step 2.5 with `{human-actor: {min: 1}}`).
- **DEFERS**: per §D — D-1 through D-6.

## Rationale

D38 rejected "knowledge" as a framework-core kind on first-principles grounds (D4 inclusion test + D5 I3 work-as-central-primitive). D53 validates the rejection holds against a substantive Sana-style scenario rather than a thin counter-example. Per the "Concrete examples before locking" operating discipline (README) + "Cross-decision artifact probe" (probing.md Procedure 5) — worked examples that exercise the contract across multiple decisions catch local-over-global gaps that per-decision review misses.

Honest framing: D53 is **specification-validation**, not framework extension. The risk it covers is "D38's structural claim turned out wrong when actually exercised"; the value it produces is "D38 holds at the worked-example scale; future knowledge-platform-style deployments have a fixture to start from." Per the durability bet: worked examples are scaffolding (per-Phase exemplars), not durable framework content — they live alongside locked decisions as proof-of-coherence artifacts.

D53 follows D46-D52 cluster-supersedes structural template at smaller scope (single-fixture validation; no new contract content; SKIP probe per pure-pattern-application). Sixth/last cluster-supersedes phase per D45 §C completed at D52; D53 begins post-cluster Bref closure work.

**Cross-references**: D4 (inclusion test — legitimate shapes have no knowledge corpus; D53's sana-knowledge-shape is one shape, not framework identity); D5 §I3 (work-as-central-primitive; knowledge as supporting infrastructure); D7 (workspace kind — sana-style-ws is one workspace); D8 (precedent — mechanisms decompose across kinds; D53 demonstrates D38 follows D8 shape); D10 + D23 (claim payload — Sana-style synthesis claims use existing slot); D13 (shape policy bundle — sana-knowledge-shape uses authority-bindings + hooks + actor-requirements + roles); D16 (retrieval + write-back adapters); D19 (knowledge-agent specialist); D20 (synthesis-task work-unit-kind); D25 (8-kind closure validated by D53 worked example); D26 Phase B B7 (RAG-via-MCP — structural precedent for the fixture shape); D38 (THE decision validated by D53; D53 extends D38 with worked-example evidence); D40 (state replay used in test 6); D45 §C (cluster-supersedes phase completed at D52; D53 is post-cluster closure work); D52 (sana-knowledge-shape's `{human-actor: {min: 1}}` exercises D52 step 2.5); probing.md Procedure 5 (cross-decision artifact probe — worked-example validation shape); market-context.md (Sana AI as Workday-acquired knowledge platform; rejected-alternative source).
