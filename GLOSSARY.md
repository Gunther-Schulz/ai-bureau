# pbs-bureau GLOSSARY

Canonical source for term definitions across the pbs-bureau corpus. Per `MAINTENANCE.md` cascade discipline, all docs cite GLOSSARY for term meaning rather than redefining.

**Per-entry split (load-on-demand)**: Each entry's canonical body lives in `glossary/<slug>.md`. This INDEX provides metadata + cross-refs only; entry content loads on demand. Pattern serves Anthropic's <500-line context-budget recommendation for mandatory session-start reads (per AgentIF benchmark + Chroma context-rot study + Claude Code best-practices guidance: oversized mandatory load directly causes adherence collapse).

To consult a term's full canonical definition, read `glossary/<slug>.md`. Anchor links in this index (`#term`) resolve within this file; per-entry file paths (`glossary/term.md`) resolve to canonical body.

## Tag legend

Each entry is tagged on 4 axes (per `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section):

- **Class**: `PRIMITIVE` (atomic) / `META-PRIMITIVE` (container) / `DERIVED` (composition / failure mode / property) / `SCOPE-CLASSIFICATION` (entity-md placement category)
- **Layer**: `framework-mechanism` / `shape-policy` / `cross-cutting` / `multi-aspect` (multi-scope) / `framework-meta` (operates on framework primitives)
- **Axis**: `axis-1` (intertwining) / `axis-2` (sparring) / `axis-3` (authorship preservation) / `cross-axis`
- **VISION usage**: `directly-used` / `implicit` / `derived` / `framework-meta`

Tags are a means, not an end. If an entry is clearer with fewer tags, drop the extras.

## Entry-locking discipline (cascade prevention of inherited-framing bias)

GLOSSARY is built foundation-up. Earlier entries may forward-reference terms not yet locked; later entries reference earlier ones. Discipline:

1. **Greenfield-draft** new entries from VISION + `MAINTENANCE.md` (locked architectural commitments) + first principles — NOT from prior entries' cross-references to this term as anchors
2. **Minimize embedded descriptions** of not-yet-locked terms — use brief role tags + cross-ref to authoritative source (`MAINTENANCE.md` or forthcoming entry); don't carry the not-yet-locked term's "definition" inline in current entry
3. **Cascade-pass after locking** per `MAINTENANCE.md` cascade discipline — review all prior cross-references to the new term; reconcile inconsistencies in the same commit

This prevents earlier-drafted cross-refs from biasing later canonical definitions.

**Three axes** referenced in tags map to VISION axes:
- **axis-1** = intertwining (workflow embedding)
- **axis-2** = sparring (interaction mode)
- **axis-3** = authorship preservation (outcome orientation)

Each axis has its own glossary entry; full claims live in `VISION.md`.

## Index (alphabetical)

| # | Entry | Class | Layer | Axis | File |
|---|-------|-------|-------|------|------|
| 1 | <a id="actor"></a>actor | PRIMITIVE | cross-cutting | cross-axis | [actor.md](glossary/actor.md) |
| 2 | <a id="adapter"></a>adapter | PRIMITIVE | multi-aspect | cross-axis | [adapter.md](glossary/adapter.md) |
| 3 | <a id="answer-machine-ai"></a>answer-machine AI | DERIVED | framework-meta | axis-2 | [answer-machine-ai.md](glossary/answer-machine-ai.md) |
| 4 | <a id="authorship-preservation-axis-3"></a><a id="authorship-preservation"></a>authorship preservation (axis 3) | DERIVED | cross-cutting | axis-3 | [authorship-preservation.md](glossary/authorship-preservation.md) |
| 5 | <a id="category-collapse"></a>category collapse | DERIVED | framework-meta | cross-axis | [category-collapse.md](glossary/category-collapse.md) |
| 6 | <a id="claim"></a>claim | PRIMITIVE | cross-cutting | axis-3 | [claim.md](glossary/claim.md) |
| 7 | <a id="co-worker"></a>co-worker | DERIVED | cross-cutting | axis-1 | [co-worker.md](glossary/co-worker.md) |
| 8 | <a id="defensibility"></a>defensibility | DERIVED | cross-cutting | axis-3 | [defensibility.md](glossary/defensibility.md) |
| 9 | <a id="deployment"></a>deployment | DERIVED | framework-meta | cross-axis | [deployment.md](glossary/deployment.md) |
| 10 | <a id="engaged-authorship"></a>engaged authorship | DERIVED | cross-cutting | axis-3 | [engaged-authorship.md](glossary/engaged-authorship.md) |
| 11 | <a id="event"></a>event | PRIMITIVE | framework-mechanism | cross-axis | [event.md](glossary/event.md) |
| 12 | <a id="framework"></a>framework | META-PRIMITIVE | framework-meta | cross-axis | [framework.md](glossary/framework.md) |
| 13 | <a id="framework-c-scope"></a>Framework C scope | SCOPE-CLASSIFICATION | framework-meta | cross-axis | [framework-c-scope.md](glossary/framework-c-scope.md) |
| 14 | <a id="intertwined-ai"></a>intertwined AI | DERIVED | cross-cutting | axis-1 | [intertwined-ai.md](glossary/intertwined-ai.md) |
| 15 | <a id="intertwining-axis-1"></a><a id="intertwining"></a>intertwining (axis 1) | DERIVED | cross-cutting | axis-1 | [intertwining.md](glossary/intertwining.md) |
| 16 | <a id="layer-a-scope"></a>Layer A scope | SCOPE-CLASSIFICATION | cross-cutting | cross-axis | [layer-a-scope.md](glossary/layer-a-scope.md) |
| 17 | <a id="mechanism"></a>mechanism | PRIMITIVE | framework-mechanism | cross-axis | [mechanism.md](glossary/mechanism.md) |
| 18 | <a id="oracle-ai"></a>oracle AI | DERIVED | framework-meta | axis-2 | [oracle-ai.md](glossary/oracle-ai.md) |
| 19 | <a id="owner-b-scope"></a>Owner B scope | SCOPE-CLASSIFICATION | cross-cutting | cross-axis | [owner-b-scope.md](glossary/owner-b-scope.md) |
| 20 | <a id="pioneer-instance"></a>pioneer instance | DERIVED | framework-meta | cross-axis | [pioneer-instance.md](glossary/pioneer-instance.md) |
| 21 | <a id="policy"></a>policy | PRIMITIVE | shape-policy | cross-axis | [policy.md](glossary/policy.md) |
| 22 | <a id="practitioner"></a>practitioner | PRIMITIVE | multi-aspect | axis-3 | [practitioner.md](glossary/practitioner.md) |
| 23 | <a id="protocol-architectural"></a>protocol (architectural) | META-PRIMITIVE | multi-aspect | cross-axis | [protocol-architectural.md](glossary/protocol-architectural.md) |
| 24 | <a id="quality-gate"></a>quality-gate | PRIMITIVE | framework-mechanism | cross-axis | [quality-gate.md](glossary/quality-gate.md) |
| 25 | <a id="rubber-stamping"></a>rubber-stamping | DERIVED | framework-meta | axis-3 | [rubber-stamping.md](glossary/rubber-stamping.md) |
| 26 | <a id="session"></a>session | PRIMITIVE | cross-cutting | cross-axis | [session.md](glossary/session.md) |
| 27 | <a id="shape"></a>shape | META-PRIMITIVE | framework-meta | cross-axis | [shape.md](glossary/shape.md) |
| 28 | <a id="skill"></a>skill | PRIMITIVE | cross-cutting | cross-axis | [skill.md](glossary/skill.md) |
| 29 | <a id="sparring-axis-2"></a><a id="sparring"></a>sparring (axis 2) | DERIVED | cross-cutting | axis-2 | [sparring.md](glossary/sparring.md) |
| 30 | <a id="specialist"></a>specialist | PRIMITIVE | multi-aspect | cross-axis | [specialist.md](glossary/specialist.md) |
| 31 | <a id="substrate"></a>substrate | PRIMITIVE | multi-aspect | cross-axis | [substrate.md](glossary/substrate.md) |
| 32 | <a id="tacked-on-ai"></a>tacked-on AI | DERIVED | cross-cutting | axis-1 | [tacked-on-ai.md](glossary/tacked-on-ai.md) |
| 33 | <a id="validator-ai"></a>validator AI | DERIVED | framework-meta | axis-2 | [validator-ai.md](glossary/validator-ai.md) |
| 34 | <a id="workflow"></a>workflow | PRIMITIVE | multi-aspect | axis-1 | [workflow.md](glossary/workflow.md) |
| 35 | <a id="work-unit"></a>work-unit | PRIMITIVE | multi-aspect | cross-axis | [work-unit.md](glossary/work-unit.md) |
| 36 | <a id="workspace"></a>workspace | PRIMITIVE | cross-cutting | cross-axis | [workspace.md](glossary/workspace.md) |

## Cluster index (concept-cluster navigation)

Reading map by concept-cluster. Same entries as the alphabetical index above; this is navigational only. Some primitives appear in multiple clusters (cross-listed); canonical body is single-located in `glossary/<slug>.md`.

### 1. Foundational (read first)

Atoms + containers + scope classifications. The architecture's load-bearing primitives.

- [mechanism](glossary/mechanism.md) — atomic interface contract within the framework
- [policy](glossary/policy.md) — atomic configured value within a shape
- [framework](glossary/framework.md) — universal mechanism layer (META-PRIMITIVE container)
- [shape](glossary/shape.md) — policy bundle archetype (META-PRIMITIVE container)
- [Framework C scope](glossary/framework-c-scope.md) — placement category for definitions
- [Owner B scope](glossary/owner-b-scope.md) — placement category for instances
- [Layer A scope](glossary/layer-a-scope.md) — placement category for layered content

### 2. Compositional primitives (deployment chain)

The primitives that compose into a workspace deployment.

- [workspace](glossary/workspace.md) — deployment-instance container
- [substrate](glossary/substrate.md) — runtime contract (Pattern A; tri-aspect)
- [specialist](glossary/specialist.md) — composable expertise bundle (Pattern B; bipartite)
- [skill](glossary/skill.md) — atomic work-logic unit within specialist
- [practitioner](glossary/practitioner.md) — human author who bears accountability (Pattern C; bipartite)
- [session](glossary/session.md) — bounded interaction unit
- [workflow](glossary/workflow.md) — bipartite Pattern B; optional structural overlay; pattern of work in a domain
- [work-unit](glossary/work-unit.md) — bipartite Pattern B; always-present container; specialist-defines kind
- [claim](glossary/claim.md) — atomic accountability-bearing assertion within work-unit output (the unit-of-defense per defensibility test)

### 3. VISION axes

- [intertwining (axis 1)](glossary/intertwining.md) — workflow embedding
- [sparring (axis 2)](glossary/sparring.md) — interaction mode
- [authorship preservation (axis 3)](glossary/authorship-preservation.md) — outcome orientation

### 4. Audit + event primitives (cross-axis structural substrate)

- [actor](glossary/actor.md) — event emitter
- [event](glossary/event.md) — audit emission unit

**Note**: specific mechanism instances (audit trail = sequence of events; source-grounding = traceability claim; persistent state = cross-session state; orchestration = continuous decision layer) are NOT separate GLOSSARY entries — they're specific instances of the abstract `mechanism` primitive (already locked). Their canonical detail lives in **ARCH Layer 3** (placeholder until Phase 3). Same applies to the 8 sparring sub-mechanisms (see §6 below). GLOSSARY locks SHAPE primitives (mechanism, policy, framework, shape, etc.); specific mechanism instances are ARCH territory.

### 5. Pattern A primitives (Protocol pluggability)

Surface + Implementations + Instance/binding. See `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" for the pattern.

- [substrate](glossary/substrate.md) (cross-listed; primary location §2)
- [protocol (architectural)](glossary/protocol-architectural.md) — architectural pluggable subsystem
- [adapter](glossary/adapter.md) — external integration boundary
- [quality-gate](glossary/quality-gate.md) — runtime checkpoint validation Protocol; cross-axis category-collapse-resistance enforcement

### 6. Sparring sub-mechanisms (axis 2 detail)

Eight named mechanisms supporting sparring mode: counter-argument, confidence calibration, visible reasoning, selective friction, asymmetric knowledge respect, anti-sycophancy, commit-to-recommendations, what's-missing.

**Note**: these are NOT separate GLOSSARY entries — they're specific instances of the abstract `mechanism` primitive (already locked). Their canonical detail lives in **ARCH Layer 3** (placeholder until Phase 3).

### 7. Modes & relations (conversational vocabulary)

- [co-worker](glossary/co-worker.md) — relational claim about AI's mode of participation
- [intertwined AI](glossary/intertwined-ai.md) — positive axis-1 mode
- [tacked-on AI](glossary/tacked-on-ai.md) — failure mode of axis 1
- [answer-machine AI](glossary/answer-machine-ai.md) — axis-2 failure mode (extraction direction)
- [oracle AI](glossary/oracle-ai.md) — axis-2 failure mode (declarative direction)
- [validator AI](glossary/validator-ai.md) — axis-2 failure mode (affirmation direction)
- [rubber-stamping](glossary/rubber-stamping.md) — axis-3 failure mode (sign-off without engagement)

**Note**: "AI runtime" is informal shorthand for substrate's tri-aspect Instance (per Pattern A) — used colloquially in docs but not a separate GLOSSARY primitive. Architectural primitive is `substrate`.

### 8. Meta concepts

- [deployment](glossary/deployment.md) — DERIVED concept; workspace-as-bound-runtime (binding-act-aspect of workspace; 1:1 with workspace at framework level)
- [pioneer instance](glossary/pioneer-instance.md) — originating deployment (production-tool + research-lab + IP-proving-ground)
- [category collapse](glossary/category-collapse.md) — cross-axis force that degrades engagement regardless of architectural intent
- [defensibility](glossary/defensibility.md) — operational test for axis 3
- [engaged authorship](glossary/engaged-authorship.md) — DERIVED axis-3 success mode (two-phase composite: production-phase sparring + attestation-phase per-claim attestation; success contrast to rubber-stamping)

## Cross-references

- `VISION.md` — three-axis thesis; the ground truth GLOSSARY serves
- `MAINTENANCE.md` — TOP-LEVEL ARCHITECTURE (framework=mechanisms; shape=policies; A-B-C scope model); cascade discipline; 5-layer doc model
- `ARCHITECTURE.md` — Layer 2 overview when working on architectural topics
- `arch/<topic>.md` — Layer 3 per-topic ARCH detail (loads on-demand)

Entries are alphabetical (case-insensitive). Cross-references are explicit; reading any entry should make the term's place in the architecture immediately clear.
