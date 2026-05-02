# Glossary

Canonical source for term definitions across the pbs-bureau corpus. Per `MAINTENANCE.md` cascade discipline, all docs cite GLOSSARY for term meaning rather than redefining.

## How entries are structured

Each entry is tagged on 4 axes (per `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section):

- **Class**: PRIMITIVE (atomic) / META-PRIMITIVE (container) / DERIVED (composition) / SCOPE-CLASSIFICATION
- **Layer**: framework-mechanism / shape-policy / cross-cutting / multi-aspect / framework-meta
- **Axis**: axis-1 / axis-2 / axis-3 / cross-axis (where applicable)
- **VISION usage**: directly used / implicit / derived-from-VISION-terms / framework-meta

Tags are a means, not an end. If an entry is clearer with fewer tags, drop the extras.

**On entry-by-entry locking (cascade prevention of inherited-framing bias)**: GLOSSARY is built foundation-up. Earlier entries may forward-reference terms not yet locked; later entries reference earlier ones. Discipline:

1. **Greenfield-draft** new entries from VISION + `MAINTENANCE.md` (locked architectural commitments) + first principles — NOT from prior entries' cross-references to this term as anchors
2. **Minimize embedded descriptions** of not-yet-locked terms — use brief role tags + cross-ref to authoritative source (`MAINTENANCE.md` or forthcoming entry); don't carry the not-yet-locked term's "definition" inline in current entry
3. **Cascade-pass after locking** per `MAINTENANCE.md` cascade discipline — review all prior cross-references to the new term; reconcile inconsistencies in the same commit

This prevents earlier-drafted cross-refs from biasing later canonical definitions.

**The three axes** referenced in tags map to VISION axes:
- **axis-1** = intertwining (workflow embedding)
- **axis-2** = sparring (interaction mode)
- **axis-3** = authorship preservation (outcome orientation)

Each axis has its own glossary entry below; full claims live in `VISION.md`.

Entries are alphabetical (case-insensitive). Cross-references are explicit; reading any entry should make the term's place in the architecture immediately clear.

---

## Categories (navigation)

Reading map by concept-cluster. Each entry's canonical body lives in alphabetical order below; categories here are navigational only. Some primitives appear in multiple categories (cross-listed) — canonical body is single-located.

### 1. Foundational (read first)

Atoms + containers + scope classifications. The architecture's load-bearing primitives.

- [mechanism](#mechanism) — atomic interface contract within the framework
- [policy](#policy) — atomic configured value within a shape
- [framework](#framework) — universal mechanism layer (META-PRIMITIVE container)
- [shape](#shape) — policy bundle archetype (META-PRIMITIVE container)
- [Framework C scope](#framework-c-scope) — placement category for definitions
- [Owner B scope](#owner-b-scope) — placement category for instances
- [Layer A scope](#layer-a-scope) — placement category for layered content

### 2. Compositional primitives (deployment chain)

The primitives that compose into a workspace deployment.

- [workspace](#workspace) — deployment-instance container
- [substrate](#substrate) — runtime contract (Pattern A; tri-aspect)
- [specialist](#specialist) — composable expertise bundle (Pattern B; bipartite)
- [skill](#skill) — atomic work-logic unit within specialist
- [practitioner](#practitioner) — human author who bears accountability (Pattern C; bipartite)
- [session](#session) — bounded interaction unit
- [workflow](#workflow) — pattern of work in a domain
- [work-unit](#work-unit) — deployment-bound work-artifact (specialist-defines kind: project / matter / case / engagement / manuscript / audit)
- [claim](#claim) — atomic accountability-bearing assertion within work-unit output (the unit-of-defense per defensibility test)

### 3. VISION axes

- [intertwining (axis 1)](#intertwining-axis-1) — workflow embedding
- [sparring (axis 2)](#sparring-axis-2) — interaction mode
- [authorship preservation (axis 3)](#authorship-preservation-axis-3) — outcome orientation

### 4. Audit + event primitives (cross-axis structural substrate)

- [actor](#actor) — event emitter
- [event](#event) — audit emission unit

**Note**: specific mechanism instances (audit trail = sequence of events; source-grounding = traceability claim; persistent state = cross-session state; orchestration = continuous decision layer) are NOT separate GLOSSARY entries — they're specific instances of the abstract `mechanism` primitive (already locked). Their canonical detail lives in **ARCH Layer 3** (placeholder until Phase 3). Same applies to the 8 sparring sub-mechanisms (see §6 below). GLOSSARY locks SHAPE primitives (mechanism, policy, framework, shape, etc.); specific mechanism instances are ARCH territory.

### 5. Pattern A primitives (Protocol pluggability)

Surface + Implementations + Instance/binding. See `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" for the pattern.

- [substrate](#substrate) (cross-listed; primary location §2)
- [protocol (architectural)](#protocol-architectural) — architectural pluggable subsystem
- [adapter](#adapter) — external integration boundary

### 6. Sparring sub-mechanisms (axis 2 detail)

Eight named mechanisms supporting sparring mode: counter-argument, confidence calibration, visible reasoning, selective friction, asymmetric knowledge respect, anti-sycophancy, commit-to-recommendations, what's-missing.

**Note**: these are NOT separate GLOSSARY entries — they're specific instances of the abstract `mechanism` primitive (already locked). Their canonical detail lives in **ARCH Layer 3** (placeholder until Phase 3). See §4 note for the rationale.

### 7. Modes & relations (conversational vocabulary)

- [co-worker](#co-worker) — relational claim about AI's mode of participation
- [intertwined AI](#intertwined-ai) — positive axis-1 mode
- [tacked-on AI](#tacked-on-ai) — failure mode of axis 1

**Note**: "AI runtime" is informal shorthand for substrate's tri-aspect Instance (per Pattern A) — used colloquially in docs but not a separate GLOSSARY primitive. Architectural primitive is `substrate`.

### 8. Meta concepts

- pioneer instance (forthcoming) — workspace as production-tool + research-lab + IP-proving-ground
- [category collapse](#category-collapse) — cross-axis force that degrades engagement regardless of architectural intent
- [defensibility](#defensibility) — operational test for axis 3

---

## actor

- **Class**: PRIMITIVE (atomic; the event-emitter unit)
- **Layer**: cross-cutting (actor spans human + AI runtime + external systems; orthogonal to framework/shape split)
- **Axis**: cross-axis (actors emit events serving any axis; axis-3 lean — actors are the named-emitter primitive enabling axis-3 defensibility through audit attribution)
- **VISION usage**: implicit (VISION's "the user" + "the AI" map to actor kinds; not directly defined)

**Canonical**: An entity that emits events within the architecture — a human, an AI runtime, or an external system. Every AuditEvent declares its emitting actor (`actor_kind` enum; framework-level guarantee per locked `mechanism` entry). Actors are workspace-scope managed entities at Owner B (per `Owner B scope` members list).

**What it is**: The primitive that gives the architecture answer-to-the-question "who/what did this?" Every audit-emitted event has an actor; every action attributable in the audit trail traces to an actor. Actors are typed (`actor_kind`): typically `human`, `ai_runtime` (for substrate-running-instance-fired actions; named to disambiguate from the `skill` primitive — work-logic unit), or `external` (for events arriving from outside the workspace, e.g., A2A peers per archived corpus). The `actor_kind` enum lives at framework-mechanism level; specific actor records live as workspace-scope managed entities at Owner B.

**Naming note**: the `actor_kind: ai_runtime` enum value is deliberately NOT named `skill` — `skill` is locked vocabulary for the atomic work-logic unit within a specialist; using it as actor_kind would create naming collision. `ai_runtime` aligns with substrate's tri-aspect Instance nomenclature.

**Cardinality + lifecycle**: Actor cardinality per workspace = 1 ai_runtime (substrate's Instance is singular per workspace) + 1+ humans (practitioner-record(s); per shape — practitioner-shape mandates ≥1, multi-practitioner-shape allows N) + N external actors (peers, clients, external systems contacting the workspace; bounded by which adapters are activated). Lifecycle = practitioner-record created at workspace setup OR per-practitioner-addition; ai_runtime exists for duration of substrate activation; external actor records emerge when external entities first interact (lazy-creation per archived governance-and-identity-sourcing.md).

**What it is NOT**:
- Not a `practitioner` — practitioner is one specific actor kind (a human-practitioner-author); actor is the broader category that also includes AI runtimes and external systems
- Not the AI runtime — AI runtime is one actor kind (typically `actor_kind: ai_runtime` for substrate-running-instance-fired actions); actor is the abstraction
- Not an `event` — events are emitted BY actors; actor is the emitter, event is what gets emitted
- Not a workspace-config field — actors are managed entities (records); workspace.md may reference actors, not contain them inline

**Cross-archetype illustration**: actors recur across all workspace shapes:
- Practitioner-shape: human-practitioner-author actor + AI runtime actor + occasional external actors (clients sending email)
- Autonomous-business-shape: operator/board actor (humans) + AI runtime actors + customer-system actors (external)
- Personal-OS-shape: individual actor (human) + AI runtime actor
- Federation-shape: cross-node-peer actors (external A2A)

**Boundary test**: Three questions:
1. Does this entity emit audit events? → it's an actor
2. Is this the typed-kind of who emitted? → that's `actor_kind` (a property of actor + a framework mechanism)
3. Is this the structured emission unit? → that's an `event`, not an actor

**Composes with**:
- `event` — events are emitted by actors
- `mechanism` — `actor_kind` enum is a framework-level mechanism (interface contract requiring every event to declare its actor)
- `Owner B scope` — actor records live as workspace-scope managed entities
- `practitioner` — practitioner-record is one specific actor kind (human-practitioner-author)
- `audit trail` — actors' events compose into audit trail (specific mechanism instance; canonical detail in ARCH Layer 3, not a separate GLOSSARY entry)
- `skill` — skills emit events via the AI runtime that fires them (`actor_kind: ai_runtime`)
- `work-unit` — actors emit events scoped to work-units; actor attribution is per-work-unit in audit trail

**Source**:
- Locked GLOSSARY entries: `mechanism` ("`actor_kind` enum (declared on every audit event; framework-level guarantee)"); `Owner B scope` ("Actor (event emitter — could be human-practitioner or AI runtime)"); `skill` (composes-with: "skills emit AuditEvents via the AI runtime that fires them — `actor_kind: ai_runtime`")
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Authority binding" row in concept-by-concept table: "`actor_kind` enum includes `human`; AuditEvent records emitting actor"

**See**:
- `event` — what actors emit
- `practitioner` — one actor kind (human)
- `mechanism` — `actor_kind` is a framework-mechanism
- ARCH Layer 3 actor-detail topics (placeholder until Phase 3 — full actor_kind enum, A2A actor support per archived `a2a-and-gemini-pattern-emulation.md`, actor identity sourcing per archived `governance-and-identity-sourcing.md`)

---

## adapter

- **Class**: PRIMITIVE (atomic; the external-integration-boundary unit) — **tri-aspect Pattern A** (Adapter Protocol surface = mechanism; implementations = Framework C definitions; running instance = workspace-bound at Owner B per workspace.md adapter bindings)
- **Layer**: multi-aspect (framework-mechanism for the Protocol surface; Framework C for implementations; Owner B at workspace runtime — typically MULTIPLE adapter instances active per workspace, distinct from substrate's structural-singularity)
- **Axis**: cross-axis (different adapters serve different axes — email-adapter primarily axis-3 sending semantics; accounting-adapter cross-cutting business operations; MCP-adapter cross-axis tooling)
- **VISION usage**: implicit (architectural primitive supporting practitioner workflows that interact with external systems; not directly named in current VISION)

**Canonical**: An external-integration-boundary primitive — defines how a workspace interacts with EXTERNAL-WORLD systems via an Adapter Protocol surface; concrete implementations (gmail, outlook, fastbill, lexware, MCP-server, A2A-peer, etc.) live as Framework C definitions; a workspace activates one or more adapter instances via `workspace.md` adapter bindings. Architecturally distinct from `substrate` along the **internal-vs-external axis**: substrate = INTERNAL runtime contract for agent execution within the workspace; adapter = EXTERNAL-WORLD integration boundary connecting workspace to outside systems. Both are Pattern A primitives; cardinality (substrate singular, adapter multiple) follows from this distinction.

**What it is**: The Pattern A primitive for external-system integration. Each adapter has:
1. **Surface** (mechanism; framework-level): an Adapter Protocol contract per integration-class (e.g., the email-adapter Protocol surface defines send / fetch / threading semantics applicable to ANY email backend; the accounting-adapter Protocol surface defines invoice / payment / ledger semantics applicable to ANY accounting system)
2. **Implementations** (Framework C; distributable): concrete realizations (gmail-adapter, outlook-adapter, generic-SMTP-adapter for email; fastbill-adapter, lexware-adapter for accounting; MCP-server-adapter for MCP-protocol backends; A2A-peer-adapter for federation peers per archived `a2a-and-gemini-pattern-emulation.md`)
3. **Instance/binding** (Owner B; workspace-bound): the active implementation in a deployment, typically MULTIPLE simultaneously (a practitioner-shape workspace might run gmail-adapter + fastbill-adapter + MCP-corpus-adapter concurrently)

Skills invoke adapters at runtime (e.g., draft-cover-mail skill invokes email-adapter to send Begründung); specialists may bundle adapter implementations as part of their package (per locked `specialist` entry composes-with: "specialists may bundle adapter implementations as part of their package").

**What it is NOT**:
- Not the `substrate` — substrate is the INTERNAL runtime contract for agent execution (agent loop, tool surface, permission flow, lifecycle events) WITHIN the workspace; adapter is the EXTERNAL-WORLD integration boundary connecting workspace to outside systems. Both are Pattern A primitives but serve different architectural scopes (internal vs external).
- Not a `specialist` — specialists may USE adapters (and may bundle implementations); the adapter is the integration boundary itself, not codified expertise
- Not a `single mechanism` — Pattern A: Surface + Impls + Instance; mechanism is atomic without multiple impls
- Not a `workflow` — adapters serve workflow steps that involve external-system interaction; adapter is the integration primitive, workflow is the work-pattern
- Not an MCP tool per se — MCP-server-adapter is one specific adapter implementation; adapter as a primitive is broader (covers email, accounting, A2A, file-sync, etc.)

**Cross-archetype illustration** (named, archived examples; bidirectional vs unidirectional shape varies per impl-class):
- **Practitioner-shape (PBS-Schulz pioneer)**: email-adapter (mostly outbound send + threading on inbound; per archived `draft-cover-mail` skill); accounting-adapter (request/response invoicing per archived `invoicing` specialist); MCP-corpus-adapter (request/response sync; LanceDB backend per archived `backend-conventions.md`)
- **Autonomous-business-shape**: CRM-adapter, payment-processor-adapter, customer-system-adapter
- **Personal-OS-shape**: calendar-adapter, task-system-adapter, note-app-adapter
- **Federation-shape**: A2A-peer-adapter (bidirectional async; cross-node specialist sharing per archived `a2a-and-gemini-pattern-emulation.md`)
- **Hybrid-shape**: combinations across all of the above

**Boundary test**: Five questions:
1. Is this primarily about INTERNAL agent execution (runtime contract for the workspace's agent loop)? → it's the `substrate`, not adapter
2. Is this primarily about EXTERNAL-WORLD integration (workspace ↔ outside system)? → it's an adapter
3. Is this codified expertise bundled for a competence area? → it's a `specialist` (which may USE adapters)
4. Is this an atomic interface contract without multiple implementations? → it's a `mechanism`
5. Is this the meta-pattern shape itself (Surface + Impls + Instance)? → it's `protocol (architectural)` — the META-PRIMITIVE

**Composes with**:
- `mechanism` — Adapter Protocol surface IS a mechanism (atomic interface contract)
- `Framework C scope` — adapter implementations live there as distributable definitions
- `Owner B scope` — running adapter instances bound to workspace deployment
- `protocol (architectural)` — adapter is a Pattern A instance; META-PRIMITIVE protocol describes the pattern shape
- `substrate` — counterpart Pattern A primitive (substrate = INTERNAL runtime contract; adapter = EXTERNAL integration); adapters run WITHIN the substrate's execution
- `skill` — skills invoke adapters at runtime to interact with external systems (e.g., draft-cover-mail → email-adapter; verify-citations → MCP-corpus-adapter)
- `specialist` — specialists may bundle adapter implementations as part of their package
- `workspace` — workspace activates one-or-more adapter instances via `workspace.md` adapter bindings
- `shape` — shape policies may mandate certain adapters or constrain permitted ones (e.g., practitioner-shape may mandate audit-emitting adapter behavior per axis-3 defensibility)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" — adapter listed as Pattern A primitive instance (alongside substrate)
- Locked GLOSSARY entries: `protocol (architectural)` ("adapter — specific Pattern A instance (workspace-activated; multiple per workspace possible)"); `substrate` (Composes-with: "adapter — specific Pattern A instance (workspace-activated; multiple per workspace possible)"); `specialist` ("specialists may bundle adapter implementations as part of their package")
- Archived corpus for full per-adapter detail (Phase 3 ARCH territory): `a2a-and-gemini-pattern-emulation.md` (A2A peer adapter), `plugin-conventions.md` (MCP-tool integration), `backend-conventions.md` (MCP-corpus adapter)

**See**:
- `protocol (architectural)` (META-PRIMITIVE describing Pattern A shape)
- `substrate` (parallel Pattern A primitive; structurally singular vs adapter's multiplicity; INTERNAL runtime vs EXTERNAL integration)
- `specialist` (which may bundle adapter implementations)
- `skill` (which invokes adapters at runtime)
- ARCH Layer 3 adapter-detail topics (placeholder until Phase 3 — per-integration-class Adapter Protocol Surface specifications, per-implementation detail, audit-emission + permission-flow integration, lifecycle / auth-refresh / error-handling semantics; archived material to consult: `a2a-and-gemini-pattern-emulation.md`, `plugin-conventions.md`, `backend-conventions.md`)

---

## authorship preservation (axis 3)

- **Class**: DERIVED (claim/mode defined in VISION)
- **Layer**: cross-cutting
- **Axis**: axis-3
- **VISION usage**: directly used (`VISION.md` axis 3 — third interlocking principle)

**Canonical**: The architectural commitment that the practitioner remains the defensible expert author of everything PBS produces on their behalf — capable of defending, signing, and standing behind the produced work; per VISION axis 3.

**What it is**: The third VISION axis. PBS is an output-producing tool for an expert practitioner; the produced work goes out under the practitioner's name; the practitioner is legally and professionally accountable. Authorship preservation protects this professional/legal standing — no rubber-stamping, no signature without engagement, no work the practitioner can't defend. The operational test for this axis is `defensibility`.

**What it is NOT**:
- Not "user understanding" in the abstract (it's about *defending under regulatory or professional challenge*)
- Not capacity-building (capacity-building is a side effect when it happens; authorship preservation is the actual purpose)
- Not generic "human-in-the-loop" (humans-in-loop without engagement still rubber-stamp)
- Not output quality (quality is necessary but insufficient — the practitioner must be able to DEFEND it)

**Cross-archetype illustration**: legal practice signing briefs; medical practice signing case notes; planning bureau signing Begründungen; auditor signing audit reports — same axis applies wherever the practitioner-author bears regulatory/professional accountability.

**Boundary test**: ask "will the practitioner be able to defend this output six months from now under regulatory or professional challenge, having forgotten the details?" If no, axis 3 fails.

**Composes with**:
- `defensibility` — operational test for this axis
- `authorship mechanisms` — class of axis-3 mechanisms (collective term; per-mechanism detail in ARCH Layer 3)
- `practitioner` — the role this axis protects
- `practitioner-shape` — workspace shape where this axis is mandated (canonical entry forthcoming; see `shape` named-shapes catalog)
- `claim` — the atomic unit-of-defense; defensibility test resolves at claim granularity, not at whole-work-unit granularity

**Source**: `VISION.md` line 154 ("## Authorship preservation, not rubber-stamping (axis 3)"); line 164 (the practitioner-author claim); line 191 (authorship mechanisms framing); line 82 (axis-3 robustness claim); line 191 (practitioner's "professional/legal standing" framing).

**See**:
- VISION's "Authorship preservation, not rubber-stamping (axis 3)" section for full claim
- ARCH Layer 3 axis-3-mechanism topic (placeholder until Phase 3)

---

## category collapse

- **Class**: DERIVED (force/dynamic; not a primitive with instances; describes how high-engagement modes degrade to lower-engagement modes regardless of architectural intent)
- **Layer**: framework-meta (operates ON framework primitives without being one; manifestation depends on practitioner cognitive state, not architectural shape)
- **Axis**: cross-axis (primary anchor: axis 1) — the force pattern manifests on all three axes (intertwining → tacked-on; sparring → answer-machine/oracle/validator; engaged authorship → rubber-stamping); axis-1 manifestation is most-recognized and historically primary in PBS framing
- **VISION usage**: derived (composes with intertwining + axis-2 + axis-3 framings; not directly named in VISION but structurally implied by per-axis failure-mode framings)

**Canonical**: The force that degrades the practitioner's mode of engaging with the AI from a higher-engagement state to a lower-engagement state, regardless of architectural intent. The collapse occurs in the practitioner's mental category — the AI is re-categorized from co-worker-engaged-with to tool-to-deploy (axis 1), or from sparring-partner to oracle/validator/answer-machine (axis 2), or from authoring-partner to output-rubber-stamper (axis 3). At which point even an architecture deliberately designed for the higher-engagement state produces lower-engagement outcomes.

**What it is**: The general failure-force pattern across all three VISION axes. Each axis has a positive engagement state (intertwining / sparring / engaged authorship) and a degradation state (tacked-on / sycophantic-AI-modes / rubber-stamping). Category collapse names the force that produces degradation regardless of architectural intent.

The failure shape: architecture stays unchanged; the practitioner's mental category of the AI shifts; outcomes drift to match the new mental category, not the original architectural intent. This makes category collapse architecturally-resistant — pure architectural fixes can enable but not enforce the higher-engagement state.

Three structural drivers of category collapse:
1. **Workload pressure** — when cognitive overhead is high, the practitioner reverts to simpler categories ("use AI as tool" is simpler than "engage AI as co-worker"); the higher-engagement category requires sustained mental effort
2. **ROI-perception drift** — without feedback that the higher-engagement state is producing value, drift to "easier" lower-engagement state; the higher-engagement state's value is delayed (capacity-building, defensibility) while costs are immediate (engagement effort)
3. **Habituation** — repetitive use without deliberate engagement erodes the higher-engagement category; routines drift toward "what's easiest" rather than "what's deliberate"

**What it is NOT**:
- Not a single moment of failure — gradual drift, not discrete event
- Not a binary state change — erodes over time across uses
- Not prevented purely by architecture — architecture enables but doesn't enforce the mental category; practitioner-bound force
- Not specific to AI partnerships — applies to any partnership pattern requiring sustained mental category (e.g., novice trades-person treating master craftsman as task-executor rather than mentor; client treating advisor as service-provider rather than counsel)
- Not recoverable by architectural change alone — re-elevation requires deliberate practitioner re-engagement (separate concept; not yet a locked primitive)
- Not strictly unidirectional within a session — practitioner can re-engage mid-session if drift is noticed; the force is statistical, not deterministic

**Cross-archetype illustration**:

*Category collapse manifestations per archetype + axis*:
- **Practitioner-shape (planner / lawyer / researcher)**:
  - Axis 1: planner architected workspace for intertwined AI presence, but treats AI as draft-generator-tool under deadline pressure → tacked-on outcomes despite intertwined architecture
  - Axis 2: lawyer set up sparring-AI to challenge legal arguments, but accepts AI's first answer when fatigued → answer-machine outcomes despite sparring architecture
  - Axis 3: researcher engages AI for paper drafting, but signs off on AI text without engaging the reasoning → rubber-stamping despite engaged-authorship architecture
- **Auditor**:
  - Axis 1: audit workspace designed for continuous AI engagement, but auditor reverts to "run-this-check, get-result" tool-use under workload → tacked-on outcomes despite continuous-AI architecture

In all archetypes: the collapse is in the practitioner's mental category, not in the architecture. Architecture enables; the practitioner's cognitive state determines whether enablement converts to actual engagement.

**Boundary test**: Three questions — category collapse is occurring when ANY resolves favorably:
1. Has the practitioner mentally re-categorized the AI from its architectural-intent role (co-worker / sparring-partner / authoring-partner) to a lower-engagement role (tool / oracle / output-source)?
2. Are outcomes shifting from architectural-intent-aligned to lower-engagement-shape, despite no architectural change?
3. Is engagement frequency, depth, or quality declining across uses without architectural cause?

Negative-marker test (collapse NOT occurring):
- Architecture-intent-aligned outcomes are sustained across uses; OR
- When drift is detected, the practitioner re-engages deliberately and recovers higher-engagement state

**Composes with**:
- `intertwining (axis 1)` — primary state being degraded (intertwined → tacked-on collapse)
- `intertwined AI` — specific axis-1 mode that collapses
- `tacked-on AI` — axis-1 collapse outcome
- `co-worker` — relational frame that collapses (re-categorized to tool)
- `sparring (axis 2)` — axis-2 collapse target (sparring → answer-machine / oracle / validator)
- `authorship preservation (axis 3)` — axis-3 engaged-authorship state being degraded
- `defensibility` — collapsed authorship state (rubber-stamping) fails defensibility test
- `practitioner` — the cognitive-state-bound agent in whom the force operates
- `mechanism` — counter-mechanisms (sparring sub-mechanisms; engagement-feedback mechanisms; deliberate-re-engagement signals) work to RESIST collapse but don't prevent it; architectural intent enables, doesn't enforce

**Cardinality + lifecycle**: Cardinality N/A — category collapse is a force, not an instance-having entity. The force can manifest per practitioner per workspace per axis. **Lifecycle**: always-latent (any high-engagement mode is susceptible); manifestation is gradual (drift over time across uses); reversible via deliberate re-engagement or architectural re-design that adds friction against collapse (e.g., sparring sub-mechanisms that force engagement). Detectability requires engagement-quality signals, not just architectural-conformance signals (architecture stays unchanged during collapse; behavior shifts).

**Source**:
- VISION (`VISION.md`): structurally implied by axis-failure-mode framings (axis-1 tacked-on; axis-2 sycophantic modes; axis-3 rubber-stamping)
- Locked GLOSSARY entries: `intertwining (axis 1)` (composes with category collapse); `tacked-on AI` (axis-1 failure outcome); `co-worker` (relational frame)
- Lakoff (cognitive linguistics): analogical anchor — "category collapse" terminology imported from category-structure literature where higher-detail categories collapse into adjacent simpler categories under cognitive load
- Synthesis: cross-axis generalization from session-16 axis-1 trio Round 2 parallel-structure observation — each axis has a positive operational state + failure-mode anti-pattern; category collapse is the GENERAL force; per-axis failure modes are MANIFESTATIONS

**See**:
- `intertwining (axis 1)` (state being degraded, axis-1 primary)
- `tacked-on AI` (axis-1 failure outcome)
- `co-worker` (relational frame collapsing)
- `answer-machine AI / oracle AI / validator AI` (forthcoming — axis-2 failure outcomes)
- `rubber-stamping` (forthcoming — axis-3 failure outcome)
- ARCH Layer 3 category-collapse-detail topics (placeholder until Phase 3 — counter-mechanisms catalog; engagement-quality signals; per-archetype collapse signatures; collapse-detection observability; architectural friction patterns that resist collapse)

---

## claim

- **Class**: PRIMITIVE (atomic; the accountability-bearing-assertion unit within work-unit output)
- **Layer**: cross-cutting (claims sit within work-unit output content; not framework-mechanism, not shape-policy, not Framework C definition)
- **Axis**: axis-3 (primary anchor — claim is the unit-of-defense per defensibility test); axis-2 (claims are the targets sparring fires against — counter-arguments target individual claims; confidence calibration applies per claim); cross-axis (claims also serve axis-1 intertwined production as the unit AI co-authors with the practitioner)
- **VISION usage**: implicit (VISION's axis 3 framing — "the practitioner remains the defensible expert author of everything PBS produces" — claims are the atomic units of "what gets produced and defended"; not directly named in current VISION)

**Canonical**: An atomic accountability-bearing assertion within a work-unit's produced output — the smallest unit of content that the practitioner-author can be challenged on, must defend, and bears regulatory/professional accountability for. A B-Plan-Begründung paragraph asserting that a particular legal interpretation applies = one claim. A legal brief paragraph asserting case-law applicability = one claim. A research paper assertion about methodology or finding = one claim. An audit finding statement = one claim.

**What it is**: The unit of defensibility. The defensibility test (per `authorship preservation`) asks: "will the practitioner be able to defend this output six months from now under regulatory or professional challenge?" — the test resolves at claim granularity. A practitioner doesn't defend an entire 50-page Begründung as a single defensible blob; they defend the individual claims within: the legal-interpretation claim, the proportionality claim, the natural-protection claim, the mitigation-adequacy claim. Claims compose into work-unit output; work-unit is the artifact-container, claim is the atomic content-unit within. Every claim must trace to source (per source-grounding mechanism — framework-level guarantee that no claim is unsourced).

**What it is NOT**:
- Not a `work-unit` — work-unit is the bounded artifact (one project, one matter, one case); claim is an atomic assertion within work-unit output (many claims per work-unit)
- Not an `event` — events are STRUCTURED EMISSIONS to the audit trail; claim is the CONTENT-UNIT of the assertion. A claim emits a `claim_made` event (the event records the claim's emission; the claim itself is the asserted content)
- Not a `mechanism` — mechanisms are framework-level interface contracts; claim is content-level
- Not a paragraph or sentence per se — claim is the SEMANTIC unit (one assertion); typographical units (paragraph, sentence) may contain 0/1/N claims depending on content
- Not an "assertion" or "statement" generically — claim has THREE distinguishing properties:
  1. **Accountability-bearing**: practitioner can be professionally/regulatorily challenged on it
  2. **Judgment-bearing**: not a lookup-shaped fact ("BauGB §35 was amended in 2024" = fact-statement, not a claim) but a judgment the practitioner is responsible for
  3. **Source-grounded**: every claim traces to source (per source-grounding mechanism); generic "statements" / "assertions" need not have this property

**Cross-archetype illustration**:
- **Practitioner-shape (PBS-Schulz pioneer)**: B-Plan-Begründung claims (legal-interpretation; proportionality; nature-protection; mitigation adequacy)
- **Legal practice**: brief claims (case-law applicability; statutory-interpretation; remedy appropriateness)
- **Medical practice**: case-note claims (diagnosis attribution; treatment justification; prognosis)
- **Research lab**: manuscript claims (methodology validity; finding interpretation; limitation acknowledgment)
- **Auditor**: audit-finding claims (control deficiency; materiality assessment; recommendation)

In all archetypes: claim = atomic-defensible-assertion. Cross-archetype shape consistent.

**Boundary test**: Four questions:
1. Is this an atomic assertion that's accountability-bearing AND judgment-bearing AND source-grounded? → it's a claim
2. Is this a fact-statement (lookup-shaped; not judgment-bearing)? → it's a fact-statement, not a claim (though a claim may compose with fact-statements as supporting evidence)
3. Is this the bounded artifact-container (project / matter / case / etc.) holding many claims? → it's a `work-unit`
4. Is this the structured emission unit recording that a claim was made? → it's an `event` (specifically `claim_made` event-kind in archived `audit-trail-v2.md` event_kind catalog)

**Composes with**:
- `work-unit` — claims compose into work-unit output; work-unit contains N claims
- `practitioner` — practitioner is the author who must defend claims (axis-3 anchor)
- `authorship preservation (axis 3)` — defensibility test resolves at claim granularity
- `defensibility` — claim is the unit-of-defense per the defensibility test; one indefensible claim taints the work-unit's output
- `sparring (axis 2)` — sparring fires AT claim granularity: counter-arguments target individual claims; confidence calibration applies per claim; selective friction triggers per claim ambiguity
- `event` — claims emit `claim_made` events (specific event-kind; ARCH Layer 3 detail); the audit trail records claim emission per shape's audit-granularity policy
- `mechanism` — composes with TWO framework-level mechanisms: (1) audit-emission mechanism captures claim emission via `claim_made` event-kind; (2) source-grounding mechanism requires every claim trace to source (no unsourced claims at framework level)
- `policy` — audit granularity policy (per shape) determines emission frequency: **claim-level** = one event per claim (practitioner-shape standard; finest granularity; mandates by axis-3 defensibility); **action-level** = one event per workflow action (drafting_started, review_completed, send_authorized — not per claim; autonomous-business-shape default; coarser); **light** = minimal events for memory/replay only (personal-OS-shape default; no external accountability requirement)

**Cardinality + lifecycle**: Cardinality = N claims per work-unit (typically dozens-to-hundreds for substantive accountability-bearing outputs). Lifecycle = claims are CREATED during workflow execution (drafting fires `claim_made` events as claims are produced); claims may be REVISED during review (revision emits new event preserving prior claim state per append-only audit); claims are FINALIZED at send/sign moment (signed-claim_made event; practitioner authorship binding). Mutability = append-only at audit level (claim revision = new event, not rewriting previous); content mutability lives at draft level until finalization.

**Source**:
- VISION (`VISION.md`) line 154+ axis 3 framing — "the practitioner remains the defensible expert author of everything PBS produces"; the defensibility test resolves at claim granularity (axis-3 anchor)
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Concept-by-concept (worked examples)" — practitioner-shape policy "Audit granularity = claim-level" (claim is the unit-of-emission for that policy)
- Locked GLOSSARY entries: `policy` ("Audit granularity = claim-level (configures the framework's audit-emission mechanism)"); `event` (events compose audit trail; `claim_made` is one event-kind); `authorship preservation` (defensibility test)
- Archived corpus for full claim-event schema (Phase 3 ARCH territory): `audit-trail-v2.md` (claim_made event-kind in event_kind catalog; source-grounding fields; revision-event semantics)

**See**:
- `work-unit` (which contains claims)
- `authorship preservation (axis 3)` (which claim is the unit-of-defense for)
- `sparring (axis 2)` (which fires at claim granularity)
- `practitioner` (who defends claims)
- `event` (claims emit `claim_made` events)
- ARCH Layer 3 claim-detail topics (placeholder until Phase 3 — claim-event schema, claim-revision semantics, finalization mechanics, source-grounding requirements per claim, sparring-target mechanics; archived material to consult: `audit-trail-v2.md`)

---

## co-worker

- **Class**: DERIVED (relational claim/mode defined in VISION axis 1; characterizes AI's role in the workflow)
- **Layer**: cross-cutting
- **Axis**: axis-1 (defines AI's participation mode under intertwining; not a separate axis but axis-1's relational claim)
- **VISION usage**: directly used (`VISION.md` line 27 axis 1: "AI is a co-worker in the workflow itself, not a feature bolted onto an unchanged human workflow"; line 53 contrast table: "AI is a co-worker in the workflow itself"; line 60: "the AI is a participating colleague in the actual production of accountability-bearing work-products"; line 71: "AI-as-co-worker means AI does the bulk of the work" negative claim)

**Canonical**: The relational claim that the AI runtime participates in workflow as a CO-WORKER — a colleague in the actual production of accountability-bearing work — distinct from "AI as tool" / "AI as assistant" / "AI as oracle". The co-worker frame is what axis-1 architectural support enables; without it, AI defaults to tacked-on convenience-feature mode.

**What it is**: The categorical role-claim about AI's participation. When AI is a co-worker:
- AI participates in real work output (drafts, retrieves, decides, acts) — not just suggesting / summarizing on the side
- AI shares awareness of workflow state across sessions (axis-1 mechanisms enabling persistent state across sessions)
- AI orchestrates work alongside the practitioner
- AI is held to source-grounding / audit / authorship discipline like any colleague producing accountability-bearing work

The co-worker frame is operational, not metaphysical: it's about architectural commitments that PERMIT AI to act co-worker-shaped (vs tool-shaped). Whether the AI "feels" like a colleague is irrelevant; whether the architecture treats AI's outputs as colleague-grade work-products is what counts.

**What it is NOT**:
- Not "AI as tool" — tools don't share workflow state; co-worker does
- Not "AI as assistant" — assistant frames are subordinate; co-worker frame implies equal-grade-of-work participation
- Not "AI as oracle" — oracle delivers answers and the human submits them; co-worker produces work alongside the human under shared accountability discipline
- Not anthropomorphism — co-worker is the architectural-stance label, not a claim about AI sentience or agency
- Not full-autonomous-agent — co-worker still operates under practitioner-authority gates per axis 3 (authority binding mechanism); colleague-grade autonomy, not unrestricted

**Cross-archetype illustration**: co-worker frame applies wherever axis-1 architectures deploy:
- Practitioner-shape (PBS-Schulz): planner + AI-co-worker drafting Begründung together
- Legal practice: lawyer + AI-co-worker drafting brief together
- Research lab: researcher + AI-co-worker drafting/reviewing manuscript together
- Auditor: auditor + AI-co-worker working through findings together

Same role-shape across archetypes; differs by what work is produced.

**Boundary test**: Three questions:
1. Does AI participate in the work-PRODUCTION (drafting, deciding, acting) or stay on the side (suggesting, summarizing, formatting)? → if production, co-worker; if side, tool/assistant
2. Does AI share workflow state across sessions, or restart fresh each time? → if shared, co-worker; if fresh, tool
3. Is AI's output held to the same discipline (source-grounding / audit / defensibility) as the practitioner's? → if yes, co-worker; if relaxed, tool/assistant

**Cardinality + lifecycle**: N/A — co-worker is a relational claim/mode, not an instance-having entity. The frame applies whenever axis-1 architectures are deployed and the AI runtime operates within them. Mode state can SHIFT over deployment lifetime (architectural deepening realizes co-worker frame more fully; category collapse degrades it).

**Composes with**:
- `intertwining (axis 1)` — co-worker IS the relational frame intertwining establishes
- `intertwined AI` — positive mode where co-worker frame is realized
- `tacked-on AI` — failure mode where co-worker frame collapses to tool-frame
- `category collapse` — the force that breaks the co-worker frame regardless of architectural intent (host environment can collapse co-worker to tool-shape)
- `practitioner` — the human side of the co-worker pairing
- `substrate` (Instance aspect) — the runtime that occupies the co-worker role
- `mechanism` — co-worker frame requires axis-1 mechanisms (persistent state, orchestration, source-grounding, audit emission, authority binding)

**Source**:
- VISION (`VISION.md`) lines 27, 53, 60, 71 (axis 1 framing + contrast table + negative-claim qualifier)
- Locked GLOSSARY entries: `intertwining (axis 1)`; `practitioner`; `intertwined AI`

**See**:
- `intertwining (axis 1)` (which establishes co-worker frame)
- `intertwined AI` (positive realization)
- `tacked-on AI` (failure mode contrast)
- `practitioner` (human side of the pairing)
- ARCH Layer 3 axis-1-mechanism topic (placeholder until Phase 3 — the mechanisms enabling co-worker frame)

---

## defensibility

- **Class**: DERIVED (property/test defined in VISION axis 3; not a primitive with instances but the operational criterion that axis-3 architectures must satisfy)
- **Layer**: cross-cutting (defensibility is a property tested AGAINST claims + work-units; doesn't itself live at framework-mechanism, shape-policy, or instance level)
- **Axis**: axis-3 (defensibility IS the axis-3 success criterion; the test by which axis-3 is operationalized)
- **VISION usage**: directly used (`VISION.md` line 92 falsification axis 3: "if defensibility ISN'T enhanced by structural authorship"; line 82 axis-3 robustness: "accountability cannot be delegated regardless of AI capability"; implied throughout axis-3 framing as the operational discriminator)

**Canonical**: The operational test for `authorship preservation (axis 3)` — the property that the practitioner-author can defend the produced output under regulatory or professional challenge, having engaged with the judgment calls and being able to reconstruct the reasoning chain. The defensibility test asks: "will the practitioner be able to defend this six months from now under regulatory or professional challenge, having forgotten the details?" If yes, axis 3 succeeds; if no, axis 3 fails.

**What it is**: The discriminator that distinguishes axis-3-passing architectures from axis-3-failing architectures. Axis 3 itself is a CLAIM ("PBS produces output the practitioner remains the defensible expert author of"); defensibility is what makes that claim TESTABLE. Three structural conditions enable defensibility (each composing with specific framework mechanisms):

1. **Engaged authorship** — practitioner participated in producing the output (not rubber-stamped); structurally enabled by **authority binding** mechanism (human authority required somewhere in accountability-bearing output chain) + **sparring** mechanisms (axis-2 keeps practitioner critically engaged rather than passively accepting AI output)
2. **Reconstructible reasoning chain** — every claim traces to source; events compose audit trail; reasoning is recoverable post-hoc — structurally enabled by **audit emission** mechanism (events) + audit trail composition (ARCH Layer 3 detail)
3. **Source-grounded content** — no unsourced claims at framework level — structurally enabled by **source-grounding** mechanism (ARCH Layer 3 detail; every claim traces to source)

The test resolves at **claim granularity** (per `claim`): practitioner doesn't defend a 50-page document as a single defensible blob; they defend each individual claim within. Composability: if every claim passes the defensibility test, the work-unit's output passes. Conversely, ONE indefensible claim taints the output.

**What it is NOT**:
- Not output quality — quality is necessary but insufficient for defensibility (a high-quality output the practitioner can't defend still fails axis 3)
- Not capacity-building — capacity-building is a side effect when defensibility is structurally protected; not the test itself
- Not generic "human-in-the-loop" — HITL without engagement still rubber-stamps (and rubber-stamped output fails defensibility)
- Not "user understanding" in the abstract — defensibility is specifically about defending under regulatory/professional challenge (a higher bar than understanding)
- Not a primitive with instances — defensibility is a PROPERTY/TEST applied to claims + work-units; doesn't have its own deployment-bound instances

**Cross-archetype illustration**:

*Defensibility-passing per archetype*:
- **Practitioner-shape (PBS-Schulz pioneer)**: planner's Begründung defensible six months later under UNB Stellungnahme challenge — each legal-interpretation claim, proportionality claim, nature-protection claim passes
- **Legal practice**: lawyer's brief defensible under opposing counsel + court scrutiny — case-law applicability, statutory-interpretation, remedy-appropriateness claims pass
- **Medical practice**: clinician's case notes defensible under medical-board review — diagnosis, treatment-justification, prognosis claims pass
- **Research lab**: researcher's manuscript defensible under peer review + post-publication scrutiny — methodology, finding-interpretation claims pass
- **Auditor**: audit findings defensible under regulatory examination — control-deficiency, materiality-assessment claims pass

*Defensibility-failure modes per archetype* (showing the failure-shape):
- Practitioner-shape: planner who signs Begründung without engaging argumentation = rubber-stamping → fails engaged-authorship condition
- Legal practice: lawyer who can't reconstruct case-law citation chain under cross-examination → fails reasoning-chain condition
- Medical: clinician case-notes lacking source citations for treatment justification → fails source-grounding condition
- Research: researcher who can't defend methodology under peer review (rubber-stamped or unsourced) → fails on whichever condition is missing
- Auditor: audit findings without supporting evidence trail → fails reasoning-chain condition

In all archetypes: defensibility is the test that distinguishes accountability-bearing-output workspaces from output-producing-tool deployments.

**Boundary test**: Four questions — defensibility passes only when ALL four resolve favorably:
1. Will the practitioner be able to DEFEND this output six months from now under regulatory or professional challenge, having forgotten details? → if yes, defensibility passes
2. Is this output something the practitioner GENUINELY engaged with (not rubber-stamped)? → if no, defensibility fails regardless of quality
3. Can the reasoning chain (sources, decisions, sparring outcomes) be RECONSTRUCTED from audit trail? → if no, defensibility fails (post-hoc reconstruction impossible)
4. **Positive structural marker**: does the output have an audit trail showing per-claim sources, engagement events, and reasoning chain? → if yes, defensibility-conditions structurally hold; if no, defensibility is at risk regardless of practitioner intention

Questions 1-3 are practitioner/experiential tests; question 4 is the structural-observable test for architects.

**Composes with**:
- `authorship preservation (axis 3)` — defensibility IS the operational test for this axis; axis 3 expresses the architectural commitment, defensibility expresses how to test whether the commitment is met
- `practitioner` — defensibility tests apply TO practitioner-authored output; the test asks "will THIS practitioner defend THIS output?"
- `claim` — the defensibility test resolves at claim granularity; one indefensible claim taints the output
- `work-unit` — defensibility composes from per-claim tests across the work-unit's outputs
- `event` — events compose the audit trail that makes reasoning chains reconstructible (defensibility's third condition)
- `mechanism` — defensibility composes with three framework-level mechanisms collectively: source-grounding (every claim traces to source), audit emission (reasoning chain captured), authority binding (practitioner authorship structurally bound)
- `sparring (axis 2)` — sparring mechanisms structurally enable defensibility's engaged-authorship condition (sparring forces practitioner engagement; rubber-stamping fails sparring discipline → fails defensibility)
- `policy` — practitioner-shape policies mandate the conditions defensibility requires (claim-level audit granularity; source-grounding required for every claim; human authority required somewhere in chain)

**Cardinality + lifecycle**: Cardinality N/A — defensibility is a property/test, not an instance-having entity. **Lifecycle**: the test applies whenever the practitioner is challenged on produced output, but the structural conditions (engaged authorship + reconstructible reasoning + source-grounding) must be in place AT PRODUCTION TIME, not retrofitted. Architectures must STRUCTURALLY ENSURE the conditions hold (per make-wrong-shapes-impossible discipline) rather than relying on practitioner discipline alone. The test is **re-run-able**: six months / years later, when challenged, the reasoning chain is reconstructed via audit trail. Defensibility doesn't expire; the structural conditions, captured at production time, persist as audit records and remain testable indefinitely (subject to audit-trail retention policy).

**Source**:
- VISION (`VISION.md`):
  - Line 92 (axis-3 falsification): "if defensibility ISN'T enhanced by structural authorship (regulators don't care about audit trails)"
  - Line 82 (axis-3 robustness): "accountability cannot be delegated regardless of AI capability. As AI improves, regulatory frameworks tighten; practitioner-as-author becomes MORE load-bearing, not less"
  - Line 154+ (authorship preservation axis 3 section): the practitioner-author claim grounds the defensibility test
- Locked GLOSSARY entries: `authorship preservation` ("the operational test for this axis is `defensibility`"); `claim` ("the defensibility test resolves at claim granularity"); `event` ("events are the structural substrate enabling axis-3 defensibility"); `practitioner` ("defensibility test asks 'will the practitioner be able to defend this six months from now?'")

**See**:
- `authorship preservation (axis 3)` (which defensibility is the operational test for)
- `practitioner` (whose defensibility is at stake)
- `claim` (the granularity at which defensibility resolves)
- `event` (audit trail enables reconstructible reasoning chain)
- `sparring (axis 2)` (which structurally enables engaged-authorship condition)
- ARCH Layer 3 defensibility-detail topics (placeholder until Phase 3 — defensibility-conditions formalization, six-months-later test mechanics, regulatory-challenge schema, structural enforcement mechanisms, defensibility-on-claim-revision semantics; archived material to consult: `audit-trail-v2.md` for reasoning-chain reconstruction; `governance-and-identity-sourcing.md` for authority binding)

---

## event

- **Class**: PRIMITIVE (atomic; the audit-emission unit)
- **Layer**: framework-mechanism (the AuditEvent schema is a framework-level interface contract; events are the structured units of audit emission)
- **Axis**: cross-axis (events serve all three axes — they're the substrate enabling axis-3 defensibility primarily, plus axis-1 trust + axis-2 sparring records)
- **VISION usage**: implicit (VISION mentions "audit trail" line 92, 172, 183; events are the structured units of that trail; not directly defined as glossary term)

**Canonical**: A structured unit emitted to the audit trail by an actor — captures decision provenance, actor kind, timestamp, and per-event-kind details. The AuditEvent schema is a framework-level mechanism (atomic interface contract per locked `mechanism` entry).

**What it is**: The smallest unit of audit-trail content. Each event records: which actor emitted it (per `actor_kind` enum), when, what kind of event (event_kind), and event-specific details (sources, causes, decision rationale, etc. per archived audit-trail-v2 schema). Events compose into the audit trail (specific mechanism instance, ARCH Layer 3 detail); the audit trail composes from events emitted over time. Per archived corpus, events are append-only — never rewritten — which is what makes them load-bearing for axis-3 defensibility.

**What it is NOT**:
- Not the audit trail (ARCH Layer 3 detail) — audit trail is the COMPOSITION (sequence) of events; event is the atomic unit
- Not an `actor` — actors EMIT events; event is what gets emitted
- Not a workspace-state mutation — events are append-only audit records; workspace state is mutable; per archived `audit-trail-v2.md` these were unified into single-write architecture (state rendered FROM events)
- Not a session log — sessions may contain events but the event is the architectural primitive

**Cross-archetype illustration**: events emitted across all workspace shapes share the same AuditEvent schema; differ in event_kind catalog per shape:
- Practitioner-shape: claim-level events (decision_made, source_grounded, sparring_fired, send_authorized, signature_applied)
- Autonomous-business-shape: action-level events (task_started, task_completed, budget_consumed, approval_requested)
- All shapes: framework-level events (workspace_booted, specialist_activated, substrate_initialized)

The framework provides the AuditEvent schema (mechanism); shapes determine which event kinds are MANDATORY emission per their policies.

**Boundary test**: Three questions:
1. Is this an atomic structured emission unit with declared actor + timestamp + kind? → it's an event
2. Is this the sequence/composition of events over time? → it's the audit trail (ARCH Layer 3)
3. Is this the entity emitting? → it's an `actor`

**Composes with**:
- `actor` — every event declares its emitting actor (`actor_kind` field; framework-level guarantee)
- `audit trail` — events compose into the audit trail; audit trail = sequence of events (specific mechanism instance; canonical detail in ARCH Layer 3)
- `mechanism` — the AuditEvent schema IS a framework-mechanism (atomic interface contract)
- `skill` — skills emit events via the AI runtime that fires them (`actor_kind: ai_runtime`)
- `defensibility` — events are the structural substrate enabling axis-3 defensibility (reconstructible reasoning chain)
- `work-unit` — events are emitted scoped to work-units; each event records its work-unit attribution per archived audit-trail-v2 schema (every event traceable to the work-unit it concerns)
- `claim` — claims emit `claim_made` events (the structured emission recording that an accountability-bearing assertion was made; claim is the content, event is the audit-trail emission)

**Source**:
- Locked GLOSSARY entries: `mechanism` (lists "AuditEvent schema (Pydantic model contract for audit emission)" as canonical mechanism example); `actor` (events are emitted by actors)
- `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table "Audit emission" row
- VISION `VISION.md` line 92 (falsification axis 3): "if defensibility ISN'T enhanced by structural authorship (regulators don't care about audit trails)"
- Archived `audit-trail-v2.md` for full schema detail (Phase 3 ARCH territory)

**See**:
- `actor` — events are emitted by actors
- `audit trail` (ARCH Layer 3) — composition of events
- `mechanism` — AuditEvent schema as framework-mechanism
- ARCH Layer 3 event-schema topics (placeholder until Phase 3 — full AuditEvent Pydantic shape, event_kind catalog, append-only discipline; archived material to consult: `audit-trail-v2.md`)

---

## framework

- **Class**: META-PRIMITIVE (container; the bounded category that contains mechanisms, protocols, and architectural disciplines)
- **Layer**: framework-meta (this entry describes the framework layer itself)
- **Axis**: cross-axis (the framework supports all three VISION axes; specific support per axis lives in mechanisms)
- **VISION usage**: directly used (`VISION.md` lines 17, 21, 72)

**Canonical**: The shape-neutral universal layer of the pbs-bureau architecture — the bounded set of mechanisms (atomic interface contracts), architectural protocols (pluggable subsystems), and architectural disciplines that any workspace shape can compose with.

**What it is**: The "what's POSSIBLE" boundary. The framework defines the universe of capabilities, contracts, and rules available to any workspace. The framework/shape architectural relationship — what's POSSIBLE (framework) vs what's MANDATED (shape) — is locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE. The framework is the open-source, marketed product's foundation; PBS-Schulz is one practitioner-shape deployment built from the framework.

The framework includes:
- **mechanisms** (audit emission, source-grounding, sparring Protocol surface, etc.)
- **architectural protocols** (Pattern A pluggable subsystems with multiple implementations): Substrate, Adapter, Coordination, Audit, Sparring, Trust, Time. Substrate + Adapter additionally classified as PRIMITIVE primitives (per their canonical entries); the rest are named architectural Protocols (forthcoming entries). All share Pattern A shape per `protocol (architectural)` entry.
- **architectural disciplines** (cascade discipline, no-defer principle, preliminary-lock principle, make-wrong-shapes-impossible, AI-as-runtime hybrid-shape, pattern-vs-instance, glue-not-replacement)

**What it is NOT**:
- Not a specific shape's configuration (shape is the policy layer OVER the framework)
- Not the substrate (substrate is one mechanism within the framework's scope; framework is the layer that contains substrates among other mechanisms)
- Not the codebase per se (framework is the architectural layer; the codebase is one realization of the framework's mechanisms)
- Not a workspace or deployment instance (workspaces are BUILT FROM framework + shape policies + practitioners + state)
- Not market positioning or strategic claims (framework is shape-neutral; positioning lives in `STRATEGY.md`)

**Cross-archetype illustration**: All workspace archetypes share the SAME framework; they differ in which shape's policies they apply over framework mechanisms. Example shapes: practitioner-shape (PBS marketed positioning), autonomous-business-shape, personal-OS-shape, knowledge-graph-shape, federation-shape, hybrid-shape. Per-shape policy specifics live in canonical shape entries forthcoming (see `shape` entry for the meta-primitive). Same framework underwrites all archetypes; shape policies determine what each one mandates.

**Boundary test**: Two questions:
1. "Is this thing shape-specific (only valid for one shape)?" If yes → not framework; it's shape-policy or shape-specific primitive.
2. "Is this thing an interface contract any shape could use?" If yes → framework-mechanism (lives within the framework).

If a candidate concept fails test 1 (it IS shape-specific), it doesn't belong in the framework. Move to shape-extension.

**Composes with**:
- `mechanism` — atomic units of the framework (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `protocol` (architectural) — pluggable subsystems within the framework
- `shape` — counterpart in the framework/shape architectural relationship (relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `workspace` — deployment-instance container that integrates framework + shape + specialists + practitioners

**Source**: VISION (`VISION.md`):
- Line 17: "The framework underneath is workspace-shape-neutral. Framework primitives support multiple workspace shapes via shape-extension pattern"
- Line 21: "The framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory"
- Line 72: "PBS does NOT claim the framework is restricted to practitioner shape — framework is shape-neutral; positioning is practitioner-focused"

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section (the foundational architectural commitment)
- ARCH Layer 2 overview + Layer 3 framework-detail topics (placeholder until Phase 3)
- Other foundational meta-primitives: `shape`, `mechanism`, `policy`

---

## Framework C scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: framework-meta (placement category for framework primitive definitions)
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory; VISION doesn't directly use this term)

**Canonical**: The scope category for framework primitive DEFINITIONS — universal, immutable, distributable; the placement home for entity-md instances that define mechanisms, shapes, substrates, protocol-implementations, and specialist DEFINITIONS. Derived from `framework = mechanisms` (mechanism definitions live here) plus the framework's other distributable elements.

**What it is**: One of three scope classifications (Framework C / Owner B / Layer A) governing where entity-md instances live. Framework C is the "definitions" home — distributable, marketplace-listable (per ROADMAP v3), immutable at definition level. Identity is by `framework_kind` + `framework_key` in entity-md frontmatter.

**Members**:
- mechanism definitions (atomic interface contracts authored at framework level)
- shape definitions (policy bundles for an archetype)
- substrate definitions (runtime contracts: Claude Agent SDK, MS AF, future)
- protocol-implementation definitions (concrete impls: always-on-sparring, claim-level-audit, etc.)
- specialist DEFINITIONS (bipartite multi-aspect primitive: DEFINITION here, INSTANCE-CONTENT in Owner B)

**What it is NOT**:
- Not for instances (those go to Owner B)
- Not for layered content varying by domain/state (that's Layer A)
- Not for runtime state

**Boundary test**: ask "is this a distributable definition that any workspace shape could potentially use?" If yes → Framework C. "Is this an instance bound to a deployment?" → Owner B. "Is this content varying by domain/state?" → Layer A.

**Composes with**:
- `framework` — Framework C IS where framework primitive definitions live
- `shape` — shape definitions live in Framework C
- `mechanism`, `substrate`, `protocol`, `specialist` (DEFINITION) — all live in Framework C
- `Owner B scope` — where INSTANCES of Framework C definitions get deployed

**Source**: derived from session-15 entity-md scope model restructure; refined session 16 under `framework = mechanisms` / `shape = policies` framing.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)

---

## intertwined AI

- **Class**: DERIVED (positive axis-1 mode; the success state)
- **Layer**: cross-cutting
- **Axis**: axis-1 (the success state of axis-1)
- **VISION usage**: directly used (`VISION.md` line 37 axis-1 contrast table; line 53 contrast table; line 60: "real intertwining where the AI is a participating colleague")

**Canonical**: The positive realization of axis 1 — AI deeply embedded in workflow as co-worker; participates in real work production; cross-session state awareness; orchestration-aware; held to colleague-grade discipline. Per VISION axis 1: the success state architectures should target.

**What it is**: The architectural success state for axis 1. Concrete markers:
- AI shows up at workflow handoff points (review, send, response handling) without being explicitly invoked
- AI's output composes into work artifacts (Begründung paragraphs, brief sections) rather than living in side-channel chats
- Cross-session work continues seamlessly; AI knows what was decided last week
- Sparring (axis 2) fires within work-production, not as a separate "review" step (axis-2 activates within axis-1 intertwining; per VISION line 43 axis-interaction: tacked-on sparring is still axis-1 failure)

Intertwined AI is the operational success state for which axis-1 architectural support exists.

**What it is NOT**:
- Not "more AI" or "better AI" — intertwined is about INTEGRATION DEPTH, not capability
- Not full-autonomous-agent — intertwined still operates under practitioner-authority gates (axis 3)
- Not the same as "AI agent" generically — most "AI agent" demos are still tacked-on (per VISION line 60); intertwined is the deep-end version
- Not a UX claim — intertwined is architectural-shape claim, not a feeling or interaction-quality claim

**Cross-archetype illustration**:
- Practitioner-shape (PBS-Schulz): planner + AI work the B-Plan project across many sessions; AI knows project state, runs review at relevant moments, drafts Begründung paragraphs that compose into the artifact
- Legal practice: lawyer + AI work the matter; AI tracks case state across sessions, drafts brief sections, runs citation verification at appropriate workflow stages
- Research lab: researcher + AI work the manuscript; AI knows methodology decisions, drafts results sections, runs literature checks during writing
- Auditor: auditor + AI work the audit; AI tracks finding state, drafts audit-report sections, runs source verification

**Mixed-state common in transition deployments**: workspaces commonly have PARTIAL intertwining — some workflow stages intertwined (drafting + review where AI co-works), other stages tacked-on (send + response where AI is on the side). Mode state can shift per workflow stage; full intertwining is the target architecture, transition deployments evolve toward it.

**Boundary test**: Three questions (intertwined-success markers):
1. Does AI participate at workflow handoff points without explicit invocation? → if yes, intertwined
2. Does AI output compose into work artifacts (vs side-channel chat)? → if yes, intertwined
3. Does AI track work state across sessions? → if yes, intertwined

All three resolving "intertwined-side" = axis 1 succeeding.

**Cardinality + lifecycle**: N/A — operational mode, not instance. The mode is realized whenever axis-1 mechanisms are in place AND practitioner uses them as designed. Mode state shifts in BOTH directions over deployment lifetime: tacked-on → intertwined as architecture deepens (mechanism additions, workflow integration); intertwined → tacked-on as category collapse degrades (host-UX changes, workflow-bypass patterns).

**Composes with**:
- `intertwining (axis 1)` — intertwined AI IS the success state of this axis
- `tacked-on AI` — failure mode contrasted; same axis, opposite shape
- `co-worker` — the relational frame intertwined AI realizes
- `category collapse` — the force that degrades intertwined → tacked-on regardless of architectural intent
- `sparring (axis 2)` — axis-2 activates WITHIN axis-1 intertwining; sparring fires within work-production, not as separate review step (VISION line 43 axis-interaction)
- `workflow` — what intertwined AI intertwines WITH (intertwining requires workflow to embed in)
- `practitioner` — the human side of the co-worker pairing
- `substrate` (Instance aspect) — the runtime that operates intertwined
- `mechanism` — intertwined AI requires axis-1 mechanisms (persistent state, orchestration, source-grounding, audit emission, authority binding)

**Source**:
- VISION (`VISION.md`) lines 37, 53 (axis-1 contrast tables); line 60 (deep-end intertwining claim); line 43 (axis-interaction: axis-2 within axis-1)
- Locked GLOSSARY entries: `intertwining (axis 1)`; `co-worker`

**See**:
- `intertwining (axis 1)` (the architectural commitment intertwined AI realizes)
- `tacked-on AI` (failure-mode contrast)
- `co-worker` (relational frame)
- `workflow` (what gets intertwined with)
- ARCH Layer 3 axis-1-mechanism topic (placeholder until Phase 3)

---

## intertwining (axis 1)

- **Class**: DERIVED (claim/mode defined in VISION)
- **Layer**: cross-cutting
- **Axis**: axis-1
- **VISION usage**: directly used (`VISION.md` axis 1 — first interlocking principle)

**Canonical**: The integration depth where AI is a continuous co-worker IN the workflow itself, not a discrete feature bolted onto an unchanged workflow; per VISION axis 1.

**What it is**: The first VISION axis. AI participates in real work output — drafts, retrieves, decides, acts as orchestrating colleague — rather than offering convenience features (summarize this; format that) on the side. Requires architectural support: persistent state, orchestration, source-grounding, audit trail, continuous awareness, and explicit human-authority gates.

**What it is NOT**:
- Not "more AI" or "better AI" (it's a different SHAPE of integration, not a different magnitude)
- Not "AI agents" generically (most "AI agent" demos are still tacked-on)
- Not requiring AI to do the bulk of the work (could be 20% mechanical labor; the integration depth matters, not the labor share)
- Not generic "automation" (automation can be tacked-on too)

**Cross-archetype illustration**: planning bureau co-drafting Begründungen with AI in real workflow; legal practice with AI as co-worker on briefs; research lab with AI as co-author on manuscripts; auditor with AI as co-worker on audit findings — all instances of axis 1's deep integration.

**Boundary test**: ask "is the AI a participating colleague in actual work production, or a discrete convenience feature on the side?" If feature-on-the-side → tacked-on AI (failure mode for axis 1).

**Composes with**:
- `tacked-on AI` — the failure mode contrasted
- `intertwined AI` — positive mode (the success state of this axis)
- `co-worker` — relational claim about AI's mode of participation
- `trust mechanisms` — class of axis-1 mechanisms (collective term; per-mechanism detail in ARCH Layer 3)
- `workflow` — what intertwining intertwines WITH
- `category collapse` — risk to axis 1

**Source**: `VISION.md` line 23 ("## The thesis"); line 49 (axis-1 contrast table); line 60 (deep-end intertwining claim); line 199 ("Workflow as precondition (axis 1)" implication); line 203 ("Category-collapse risk (axis 1 protection)").

**See**:
- VISION "The thesis" axis 1 + tacked-on/intertwined contrast table
- VISION "Implications" → "Workflow as precondition" + "Category-collapse risk"
- ARCH Layer 3 axis-1-mechanism topic (placeholder until Phase 3)

---

## Layer A scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: cross-cutting (orthogonal to mechanism/policy split)
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory)

**Canonical**: The scope category for LAYERED CONTENT — content varying by deployment context (universal / domain-keyed / state-keyed). **Orthogonal axis** to framework/shape framing (about content scoping, not mechanism vs policy).

**What it is**: One of three scope classifications. Layer A is **independent** of the framework=mechanisms / shape=policies framing — it's an axis for content layering by domain/state context. Identity is by `layer_scope` + `layer_key` in entity-md frontmatter. Effective content for a workspace = universal + active-domains + active-states (workspace declares which apply via its scope configuration).

**Members**:
- references (e.g., legal texts; vary by jurisdiction)
- doctypes (e.g., B-Plan-Begründung is domain-specific)
- bausteine (saved text patterns; can be domain or state specific)
- memory prose (style-spec, korrektur-rules, verfahren docs; could be domain-specific)
- conventions (writing conventions per language / jurisdiction)
- domain-specific knowledge artifacts

**Layer values**:
- `universal` — applies to every deployment regardless of domain or jurisdiction
- `domain` — applies to deployments in specific domains (e.g., PV-FFA, Wind, Naturschutz, Innenentwicklung); multiple domains can be active simultaneously
- `state` — applies to deployments in specific jurisdictions (e.g., DE-BB, DE-BY, DE-BW, ...); multiple states can be active simultaneously

**What it is NOT**:
- Not derived from framework/shape (it's an INDEPENDENT classification axis)
- Not the same as framework's universal-vs-shape-specific distinction (Layer A is about CONTENT applicability by deployment context, not about mechanism vs policy)
- Not for definitions (those are Framework C)
- Not for instances (those are Owner B)

**Boundary test**: ask "does this content vary by deployment context (domain / state / universal)?" If yes → Layer A. "Is this a definition?" → Framework C. "Is this an instance bound to deployment?" → Owner B.

**Composes with**:
- `workspace` — workspace's scope configuration (active domains, active states) determines which Layer A content applies
- references / doctypes / bausteine / prose conventions — content kinds that live at Layer A

**Source**: predates session-16 rebuild (3-axis scope orthogonality from earlier ARCH); refined session 16 to clarify orthogonal-to-framework/shape status.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)

---

## mechanism

- **Class**: PRIMITIVE (atomic; irreducible unit of the framework)
- **Layer**: framework-mechanism (this entry describes the atomic unit at the framework layer)
- **Axis**: cross-axis (mechanisms can serve any of the three VISION axes)
- **VISION usage**: implicit (VISION uses "mechanisms" in plural for trust/sparring/authorship mechanism classes; doesn't define "mechanism" as singular term — that's `MAINTENANCE.md` territory)

**Canonical**: An atomic interface contract within the framework — a single capability with defined input/output surface, available to any workspace shape; the smallest unit of "what's POSSIBLE" the framework provides.

**What it is**: The atomic unit of the framework. Mechanisms are universal — usable by any shape, no shape-specific values embedded. They define WHAT'S POSSIBLE; shape policies determine WHAT'S MANDATED out of those possibilities. Multiple mechanisms compose into the framework alongside protocols (pluggable subsystems) and architectural disciplines (rules), per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE.

**Examples** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table):
- `AuditEvent` schema (Pydantic model contract for audit emission)
- `actor_kind` enum (declared on every audit event; framework-level guarantee)
- Pydantic gate (validator function dispatched on every contract-bearing write)
- Specialist conformity manifest schema (declaring a specialist's conformity surface as a Pydantic schema)
- Sparring Protocol surface (the architectural-protocol's interface contract, before any specific implementation)
- Source-grounding capability (every claim traceable to source; framework-level enforcement)
- Visible reasoning capability (Pydantic field on outputs requiring reasoning chain)

**What it is NOT**:
- Not a `policy` — policies are atomic CONFIGURED VALUES (defaults, requirements, constraints) within a shape's bundle; mechanisms are atomic INTERFACE CONTRACTS in the framework
- Not a `protocol` (architectural) — a protocol's surface IS a mechanism, but the protocol-with-multiple-implementations structure adds composition beyond a single mechanism
- Not the `framework` itself — the framework is the CONTAINER of mechanisms (+ protocols + disciplines); a single mechanism is one element of the container
- Not a workspace-level or instance-level construct — mechanisms live at framework level with no shape-specific values
- Not an architectural discipline — disciplines are RULES about how to design (canonical homes: `MAINTENANCE.md` + `DISCIPLINES.md`); mechanisms are CAPABILITIES the framework provides

**Cross-archetype illustration**: All workspace shapes use the SAME mechanisms (e.g., the `AuditEvent` schema is the same Pydantic contract in practitioner-shape, autonomous-business-shape, etc.). What differs across shapes is which mechanisms are MANDATORY, the granularity at which they're invoked, and what defaults apply — these are policies (shape-level), not mechanism variations.

**Boundary test**: Three questions:
1. Is this an atomic capability with a defined input/output surface? → likely a mechanism
2. Is this shape-neutral (any shape could use it)? → likely a mechanism (lives in framework)
3. Is this a configured value (default, requirement, mandatory)? → it's a `policy`, not a mechanism

If a candidate fails test 2 (it IS shape-specific), it doesn't belong as a framework mechanism. Move to shape-extension.

**Composes with**:
- `framework` — contains mechanisms as its atomic interface contracts (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `policy` — counterpart atom in the framework=mechanisms / shape=policies framing
- `shape` — applies policies OVER mechanisms (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `protocol` (architectural) — pluggable subsystem within the framework (relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section: "mechanism is the atom — a single interface contract; capability with defined input/output surface"
- `MAINTENANCE.md` "Concept-by-concept (worked examples)" table: examples per axis (audit emission, specialist modification, authority binding, sparring)

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section (atom-vs-container relationship + concept-by-concept worked examples)
- Other foundational meta-primitives + atoms: `framework`, `shape`, `policy`
- ARCH Layer 3 mechanism-detail topics (placeholder until Phase 3 — per-mechanism canonical detail)

---

## Owner B scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: cross-cutting
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory)

**Canonical**: The scope category for INSTANCES — deployment-specific entities owned at the workspace, specialist-instance, or work-unit-instance level; the placement home for entity-md instances that materialize in a particular deployment. Derived from `framework + shape → workspace deployment`.

**What it is**: One of three scope classifications. Owner B is the "instances" home — where definitions (Framework C) get DEPLOYED and bound to workspace context. Identity is by `owner_scope` + `owner_key` in entity-md frontmatter.

**Members**:
- workspace itself (workspace.md selecting shape + substrate + active specialists)
- workspace-scope managed entities (universal across shapes):
  - practitioner-record (system representation; per `practitioner` entry — bipartite: human cross-cutting, record at Owner B)
  - Actor (event emitter; one of `actor_kind: human / ai_runtime / external`)
  - additional managed entities per shape-policy mandate (NOT framework-level): each shape may mandate its own engagement-target managed entity — e.g., practitioner-shape mandates `Client` (engagement target for accountability-bearing service); autonomous-business-shape mandates `Customer`; research-lab-shape mandates `Funder` / `Co-author` / `Institution`; etc. Engagement-target entities are deliberately shape-policy-mandated rather than framework-level because they're not universal across archetypes (personal-OS-shape has no engagement-target).
- specialist instance content (entities owned within an active specialist instance — distinct from specialist DEFINITION which is Framework C)
- work-unit instances (kind specialist-defined: `project` for planning bureau; `matter` for legal practice; `case` for medical practice; `engagement` for consulting; `manuscript` for research; `audit` for accounting)

**What it is NOT**:
- Not for definitions (those are Framework C)
- Not for layered content (that's Layer A)
- Not where the practitioner-as-human "lives" (the human is cross-cutting; only the practitioner-record is placed)

**Boundary test**: ask "is this a deployment-specific instance bound to a workspace, specialist instance, or work-unit?" If yes → Owner B. "Is this a distributable definition?" → Framework C. "Is this content varying by deployment context (domain/state)?" → Layer A.

**Composes with**:
- `workspace` — the central Owner B instance + container for workspace-scope managed entities
- `specialist` — instance content sits at Owner B (distinct from specialist DEFINITION at Framework C)
- `work-unit` (kind specialist-defined) — instances at Owner B
- `practitioner` — record at Owner B; human itself cross-cutting
- `Framework C scope` — where the DEFINITIONS that get instantiated live

**Source**: derived from session-15 entity-md scope model restructure; refined session 16 (practitioner-record added per practitioner dual-aspect; orthogonal-Layer-A clarified).

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)

---

## policy

- **Class**: PRIMITIVE (atomic; irreducible unit of a shape's bundle)
- **Layer**: shape-policy (this entry describes the atomic unit at the shape layer)
- **Axis**: cross-axis (policies can configure any axis-related mechanism)
- **VISION usage**: implicit (VISION doesn't use "policy" as a defined term; the framework=mechanisms / shape=policies framing is locked in `MAINTENANCE.md`, not VISION)

**Canonical**: An atomic configured value within a shape — a single requirement, default, or constraint configuring how a framework mechanism is used for that shape's archetype; the smallest unit of "what's MANDATED" a shape declares.

**What it is**: The atomic unit of a shape's policy bundle. Policies are shape-level — they configure framework mechanisms for a specific archetype, with shape-specific values. They define WHAT'S MANDATED (out of what the framework's mechanisms make POSSIBLE). Multiple policies compose into a shape's bundle; the shape is the container.

**Examples** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table; practitioner-shape policies):
- Audit granularity = claim-level (configures the framework's audit-emission mechanism)
- Sparring always-on as runtime pillar (configures the sparring mechanism)
- Human authority required somewhere in accountability-bearing output chain (configures authority-binding mechanism)
- Modifications require explicit re-conformance event (configures specialist-modification mechanism)
(Per other shapes, different policies configure the same mechanisms differently — see cross-archetype illustration below.)

**What it is NOT**:
- Not a `mechanism` — mechanisms are atomic INTERFACE CONTRACTS in the framework; policies are atomic CONFIGURED VALUES in a shape
- Not a `shape` — shape is the BUNDLE of policies (container); a single policy is one element
- Not a workspace-instance configuration — policies live at SHAPE level (in a shape definition's bundle); workspace deployments inherit them from the selected shape
- Not the framework — framework provides the mechanisms; policies live in shapes that layer over the framework

**Cross-archetype illustration** (same mechanism, different policies per shape): the framework provides the audit-emission MECHANISM (AuditEvent schema + `actor_kind` enum). Different shapes declare different POLICIES configuring it:
- Practitioner-shape policy: audit granularity = claim-level; emission required for every output
- Autonomous-business-shape policy: audit granularity = action-level; emission per task
- Personal-OS-shape policy: audit granularity = light; emission optional

Same mechanism (the framework's audit-emission contract); different policies (each shape's archetype-specific values).

**Boundary test**: Three questions:
1. Is this a configured value (a default, requirement, or constraint)? → likely a policy
2. Is this shape-specific (varies by archetype)? → likely a policy (lives in a shape's bundle)
3. Is this an interface contract any shape could use? → it's a `mechanism`, not a policy

If a candidate fails test 2 (it's universal across shapes; no archetype variation), it's not a policy — it's mechanism territory.

**Composes with**:
- `shape` — contains policies as its atomic bundle elements (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `mechanism` — counterpart atom in the framework=mechanisms / shape=policies framing (mechanism = framework atom; policy = shape atom)
- `framework` — contains mechanisms over which policies are LAYERED (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `workspace` — selects a shape and inherits its policies

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section: "policy is the atom — a single configured value; requirement/default/constraint"
- `MAINTENANCE.md` "Concept-by-concept (worked examples)" table: practitioner-shape column = examples of policies per axis

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section (atom-vs-container relationship + concept-by-concept worked examples)
- Other foundational meta-primitives + atoms: `mechanism`, `framework`, `shape`
- `Framework C scope` — where shape definitions (containing policy bundles) live
- ARCH Layer 3 per-shape policy-detail topics (placeholder until Phase 3)

---

## practitioner

- **Class**: PRIMITIVE (atomic; the human-expert-author unit) — **bipartite** multi-aspect (Pattern C)
- **Layer**: multi-aspect (HUMAN aspect is cross-cutting; RECORD aspect is at Owner B as workspace-scope managed entity)
- **Axis**: axis-3 (primary anchor — practitioner is the axis-3 archetype, the role authorship preservation protects); cross-axis
- **VISION usage**: directly used (`VISION.md` lines 11, 15, 19 + axis 3 framing throughout)

**Canonical**: The human expert author who bears accountability for produced work — the natural person under whose name accountability-bearing output is signed and defended. Bipartite multi-aspect primitive (Pattern C; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Other multi-aspect primitives"): HUMAN (cross-cutting; the actual person, not "placed") + RECORD (Owner B; system representation including identity, credentials, signing authority, role bindings). Legal-entity context (firm-level contracting party) lives at WORKSPACE level (legal-entity workspace context), not at practitioner level — practitioner is always a natural person.

**What it is**: The role around which axis 3 (authorship preservation) is built. The practitioner is the human who signs the Begründung, the brief, the manuscript, the audit report — and who must be able to defend it later (the defensibility test). Architecturally this manifests in two aspects: the HUMAN itself (a person in the world; not a system entity; cross-cutting) AND a system RECORD (a managed entity at Owner B representing the practitioner — name, credentials, signing authority, role bindings). The HUMAN bears accountability legally + professionally; the RECORD is the system's stand-in that makes events traceable to a named person.

**Cardinality + lifecycle**: Practitioner-record cardinality per workspace = 1+ depending on shape (practitioner-shape solo workspace = 1; multi-practitioner-shape partnership workspace = N; legal-entity-shape workspace = N named practitioners under firm context). Lifecycle: practitioner-record created at workspace setup (initial practitioner) OR per-practitioner-addition (subsequent practitioners joining a multi-practitioner workspace). Mutability = mutable-with-audit (changes to credentials, signing authority, role bindings emit audit events; never silently rewritten). Records persist through workspace lifetime; deactivation semantics (practitioner leaving the firm) settled at ARCH Layer 3 — preliminary lock: deactivation marks record dormant, not deleted (preserves audit-trail attribution to historic outputs).

**What it is NOT**:
- Not an `actor` — actor is the broader event-emitter category; practitioner is one specific actor kind (`actor_kind: human` for practitioner-emitted events)
- Not a `specialist` — specialist is composable codified expertise (a tool the workspace activates); practitioner is the human author who employs the workspace's specialists
- Not a `workspace` — practitioners work IN workspaces; workspace serves the practitioner
- Not the `substrate`'s Instance aspect (informally "the AI runtime") — substrate's running instance is the AI side of the workspace; practitioner is human (the AI is co-worker, not the author)
- Not multiple-kinds-of-practitioner — practitioner is singular always; kind variation (solo / partnership / legal-entity-firm) lives at WORKSPACE LEVEL (multi-practitioner workspace; legal-entity workspace context), NOT at practitioner level

**Cross-archetype illustration**: practitioners across archetypes share the same role-shape (human author bearing accountability) but differ in workspace configuration:
- **Solo practitioner workspace** (PBS-Schulz pioneer): Gunther Schulz — one practitioner per workspace
- **Multi-practitioner partnership** (e.g., Müller Schmidt Weber Law): three individual practitioners sharing a workspace; each bears accountability for their own work
- **Legal-entity firm** (e.g., architecture firm): firm is the legal-entity contracting party; named architect signs each project as practitioner
- **Research lab**: principal investigator + collaborators as practitioners
- **Solo creative**: single practitioner workspace

In all cases: practitioner is one human (or natural-or-legal-person bearing accountability); workspace contains 1+ practitioners as workspace-scope managed entities.

**Boundary test**: Three questions:
1. Is this the human who signs + bears accountability for produced work? → it's a practitioner (the HUMAN aspect)
2. Is this the system's representation of that human (identity, credentials, signing authority)? → it's the practitioner-RECORD (the Owner-B aspect)
3. Is this the broader event-emitter category? → it's an `actor` (practitioner is one specific actor kind)

**Composes with**:
- `workspace` — workspace serves practitioner(s); multi-practitioner workspaces host N practitioners as workspace-scope managed entities; legal-entity workspace context binds firm + named practitioners
- `actor` — practitioner is one actor kind (`actor_kind: human` per `event` schema)
- `authorship preservation (axis 3)` — practitioner is the role axis 3 protects
- `Owner B scope` — practitioner-RECORD lives here as workspace-scope managed entity (the HUMAN aspect doesn't "live" anywhere in the system; cross-cutting)
- `defensibility` — operational test of axis 3; the test asks "will the practitioner be able to defend this six months from now?"
- `work-unit` — practitioners are the human authors signing work-unit outputs; defensibility test asks "will the practitioner defend THIS work-unit's outputs?" (the work-unit is the bounded artifact per which defensibility is judged)
- `claim` — practitioners are accountable for individual claims they author; the defensibility test resolves at claim granularity (practitioner defends each claim under regulatory/professional challenge)

**Source**:
- VISION (`VISION.md`):
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Line 15: "expert practitioners (planners, lawyers, researchers, accountants, creatives, consultants, advisors)"
  - Line 19: "this document remains the practitioner-shape articulation"
  - Multiple references throughout axis 3 framing
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Other multi-aspect primitives": "practitioner — bipartite of different shape: HUMAN (cross-cutting; the actual person; not 'placed') + RECORD (Owner B; system representation)"
- Locked GLOSSARY entries: `authorship preservation` ("practitioner — the role this axis protects"); `actor` ("practitioner is one specific actor kind"); `Owner B scope` ("practitioner-record (system representation...)"); `workspace` ("workspace serves practitioner(s); records at Owner B")

**See**:
- `authorship preservation (axis 3)` (the axis practitioner anchors)
- `workspace` (which serves practitioner; multi-practitioner workspace handles kind variation)
- `actor` (broader category; practitioner is one kind)
- `Owner B scope` (where practitioner-record lives)
- ARCH Layer 3 practitioner-detail topics (placeholder until Phase 3 — multi-practitioner workspace mechanics; legal-entity workspace context; signing-practitioner-per-work-product configuration; archived material to consult: `office-level-managed-entities.md` for practitioner-record schema)

---

## protocol (architectural)

- **Class**: META-PRIMITIVE (the Pattern A architectural shape itself; named architectural Protocols + `substrate` + `adapter` are specific PRIMITIVE instances of this pattern)
- **Layer**: multi-aspect (Surface = framework-mechanism; Implementations = Framework C; Instance/binding = workspace-bound or shape-policy-selected)
- **Axis**: cross-axis (different protocols serve different axes — Sparring Protocol = axis 2; Audit Protocol = cross-axis; etc.)
- **VISION usage**: implicit (architectural concept underlying mechanisms across all axes; not directly named in current VISION)

**Canonical**: The Pattern A architectural shape — pluggable subsystem with Surface (interface-contract mechanism) + multiple Implementations (Framework C definitions) + Instance/binding (the active implementation, selected per workspace or shape-policy). META-PRIMITIVE (the pattern itself); specific instances of this pattern are PRIMITIVEs: `substrate` (locked), `adapter` (locked), plus named architectural Protocols (Sparring, Audit, Coordination, Trust, Time — per-protocol detail in ARCH Layer 3, NOT separate GLOSSARY entries). Disambiguated from **Pydantic Protocol** (the Python typing concept; PEP 544 structural typing) — though architectural Protocols often USE Pydantic Protocol as their Surface implementation technique, the architectural concept is broader.

**What it is**: The Pattern A architectural shape made concrete. Each protocol-instance has:
1. **Surface** (mechanism; framework-level): an abstract Protocol contract defining what the subsystem provides
2. **Implementations** (Framework C; distributable): concrete realizations of the surface
3. **Instance/binding** (Owner B; workspace-bound, OR shape-policy-selected): the active implementation in a deployment

Different selection levels exist across instances:
- **Substrate Protocol**: workspace selects (one running instance per workspace via `workspace.md substrate:` field)
- **Adapter Protocol**: workspace activates instances (multiple may run; per workspace.md adapter bindings)
- **Sparring Protocol**: shape selects (practitioner-shape mandates `always-on-sparring` impl; personal-OS-shape may use `sparring-as-skill` impl) — selection lives in shape-policy
- **Audit Protocol**: shape policy + workspace overrides (granularity, retention)

**What it is NOT**:
- Not **Pydantic Protocol** — Pydantic Protocol is the Python typing concept (`typing.Protocol`); architectural Protocol is the broader pluggable-subsystem pattern. Architectural Protocols may USE Pydantic Protocol for their Surface implementation, but the pattern is independent of Python.
- Not a single `mechanism` — a mechanism is atomic; protocol-instances have multiple impls + selection beyond the surface alone
- Not itself a primitive — protocol is the META-PRIMITIVE pattern; specific Pattern A instances (`substrate`, `adapter`, named architectural Protocols) are the PRIMITIVEs
- Not a workflow or session — protocols are framework-level architectural primitives; workflows + sessions are runtime/work-pattern concepts

**Cross-archetype catalog (named architectural protocols; archived corpus + locked Pattern A members)**:
- **Substrate Protocol** (locked) — runtime contract; workspace selects one
- **Adapter Protocol** (forthcoming entry; pattern instance per integration class — email adapter, accounting adapter, MCP adapter, etc.)
- **Sparring Protocol** — axis-2 support; shape selects implementation (always-on / optional / sparring-as-skill / none)
- **Audit Protocol** — cross-axis emission; shape policy determines granularity (claim-level / action-level / light)
- **Coordination Protocol** — cross-specialist / cross-actor coordination shape (event-shaped vs call-shaped per shape policy)
- **Trust Protocol** — trust model (practitioner-judgment vs budget-policy vs individual)
- **Time Protocol** — temporal semantics (turn-based vs long-running vs heartbeat-based)

Per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE: framework provides protocols + their surfaces; shapes provide policies selecting implementations + parameterizing them.

**Boundary test**: Three questions:
1. Is this an architectural pluggable subsystem with Surface + Impls + Instance/binding? → it's a Pattern A instance (a PRIMITIVE — `substrate` / `adapter` / one of the named architectural Protocols)
2. Is this the Python typing structural concept (`typing.Protocol`)? → that's Pydantic Protocol — different concept; architectural Protocol may use it as implementation technique
3. Is this a single atomic interface contract without multiple impls? → it's a `mechanism`, not a Protocol

**Composes with**:
- `mechanism` — Protocol Surface IS a mechanism (atomic interface contract)
- `Framework C scope` — Protocol implementations live there as distributable definitions
- `shape` — shape policies select among Protocol implementations for shape-policy-selected protocols (like Sparring)
- `workspace` — workspace activates specific Protocol instances per workspace.md (for workspace-selected protocols like substrate) or inherits shape's selections
- `substrate` — specific Pattern A instance (workspace-selected)
- `adapter` — specific Pattern A instance (workspace-activated; multiple per workspace possible; EXTERNAL-integration counterpart to substrate's INTERNAL runtime contract)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" — defines Pattern A; lists known instances (substrate, adapter, protocol meta)
- Locked GLOSSARY entries: `substrate` (Pattern A instance; tri-aspect explicitly described); `mechanism` (Protocol Surface listed as mechanism example: "Sparring Protocol surface")
- Archived corpus for full per-protocol detail (Phase 3 ARCH territory): `substrate-protocol-design.md`, `shape-extension-and-architectural-floor.md`

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Recurring patterns: Protocol pluggability" (canonical pattern description)
- `substrate` (canonical Pattern A instance; locked)
- `adapter` (canonical Pattern A instance — workspace-activated multiple; EXTERNAL-integration counterpart)
- `mechanism` (Protocol Surface IS a mechanism)
- ARCH Layer 3 protocol-detail topics (placeholder until Phase 3 — per-protocol Surface specifications, per-implementation detail, selection mechanics; archived material to consult: `substrate-protocol-design.md`, `shape-extension-and-architectural-floor.md`)

---

## session

- **Class**: PRIMITIVE (atomic; the bounded-interaction unit)
- **Layer**: cross-cutting (sessions exist within workspaces; managed by substrate; not framework-mechanism, not shape-policy)
- **Axis**: cross-axis (sessions span all three axes — interactions can be sparring + audit-emitting + authorship-bearing)
- **VISION usage**: implicit (VISION's "persistent state across sessions" — the cross-session-persistence claim is part of axis-1 architectural support)

**Canonical**: A bounded interaction unit within a workspace — typically one human-AI exchange or work-session. Substrate manages session lifecycle (start/end, context boundaries); state persists ACROSS sessions (per axis-1 architectural mechanism); events fire WITHIN sessions (per `event` entry). A workspace contains many sessions over its lifetime.

**What it is**: The unit at which interactions happen. When you sit down to work with PBS, that work happens within a session: substrate manages the session boundary (when it starts, when it ends, what context is active); within the session, skills fire, events emit, decisions get made. The next session inherits persistent state from prior sessions (e.g., project state, decisions, baustein memory). Sessions are bounded; persistence is cross-session.

**What it is NOT**:
- Not a `workspace` — workspace contains many sessions over time; workspace is the deployment-instance, session is one bounded interaction within it
- Not a `workflow` — workflow is the pattern of work in a domain (sequence of activities); session is one execution-unit during which workflow steps may be progressed
- Not a single `event` — events fire WITHIN sessions; session is the bounded container, event is the atomic emission unit
- Not the `substrate` — substrate manages sessions (session lifecycle is a substrate primitive); session is one runtime artifact

**Cross-archetype illustration**:
- Practitioner-shape: a planning bureau session = drafting Begründung interaction (1+ hours of human-AI co-work); legal practice session = brief-drafting + research interaction
- Autonomous-business-shape: a session may be an operator approval review or an AI-org task-batch
- All shapes: substrate manages the bounded interaction; persistence happens across boundaries

**Boundary test**: Three questions:
1. Is this a bounded interaction with start/end + context boundaries? → it's a session
2. Is this the deployment-instance container that holds many sessions? → it's a `workspace`
3. Is this the pattern of work that sessions execute parts of? → it's a `workflow`

**Composes with**:
- `workspace` — workspaces contain many sessions over their lifetime
- `substrate` — substrate manages session lifecycle (start/end, context, persistence handoff)
- `event` — events fire within sessions; session bounds emission timing
- `actor` — actors operate within sessions
- `workflow` — sessions execute parts of broader workflows

**Source**:
- VISION (`VISION.md`) implicit reference: persistent-state-across-sessions is part of axis-1 architectural support
- `substrate` GLOSSARY entry: substrate's Protocol surface includes session/context primitives
- `workspace` GLOSSARY entry: "interaction units occur within a workspace"
- `event` GLOSSARY entry: events fire within sessions (implicit; events have timestamps tying them to session timeline)

**See**:
- `workspace` (which contains sessions)
- `substrate` (which manages session lifecycle)
- `event` (which fires within sessions)
- ARCH Layer 3 session-detail topics (placeholder until Phase 3 — session boundary semantics, context-handoff rules, persistent-state migration across sessions; archived material to consult: `substrate-protocol-design.md` for session/context API)

---

## shape

- **Class**: META-PRIMITIVE (container; the category of policy bundles, not a single policy itself)
- **Layer**: framework-meta (this entry describes the shape layer concept itself)
- **Axis**: cross-axis (shapes can have policies serving any axis)
- **VISION usage**: directly used (`VISION.md` lines 11, 17, 19, 21, 72)

**Canonical**: A workspace archetype — a bundle of policies layered over framework mechanisms, configuring what's MANDATED for that archetype. Shape definitions are themselves framework primitives (live in Framework C scope); a workspace selects exactly one shape via its `workspace.md`.

**What it is**: A shape provides the "what's MANDATED" layer for a workspace archetype, per the framework/shape architectural relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE. Each shape declares its policies + may add shape-specific primitives needed for its archetype. PBS as marketed product positions on practitioner-shape; the framework underneath is shape-neutral and supports multiple shapes.

**What it is NOT**:
- Not a workspace (a workspace IS DEPLOYED as a specific shape's archetype; the shape is the configuration definition)
- Not the framework (shape sits OVER framework per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; framework is the universal mechanism layer)
- Not a deployment instance (shape DEFINITIONS are universal/distributable; live in Framework C scope; per-deployment selection happens via `workspace.md`)
- Not a single policy (shape is a BUNDLE)
- Not always practitioner-shape (PBS markets practitioner-shape; framework supports multiple shapes — see named-shapes catalog below)

**Cross-archetype catalog (named shapes — canonical per-shape detail forthcoming)**:
- **practitioner-shape** — workspace shape for accountability-bearing expert work; PBS marketed positioning + pioneer reference
- **autonomous-business-shape** — operator-supervised multi-agent shop
- **personal-OS-shape** — individual life-OS
- **knowledge-graph-shape** — corpus + curation; no workflow loop
- **federation-shape** — cross-node specialist sharing
- **hybrid-shape** — combinations of above

**Boundary test**: Three questions:
1. Is this an atomic unit contained within a shape (one element of its bundle)? → it's a `policy`
2. Is this an interface contract any shape could use? → it's a `mechanism` (lives in framework, not shape)
3. Is this a bundle of policies for a workspace archetype? → it's a shape

**Composes with**:
- `framework` — counterpart in the framework/shape architectural relationship (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `policy` — atomic unit contained within a shape's bundle
- `workspace` — deploys exactly one shape via `workspace.md`
- `Framework C scope` — where shape DEFINITIONS live as distributable framework primitives
- `mechanism` — what shape policies configure (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)

**Source**:
- VISION (`VISION.md`):
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Line 17: "Framework primitives support multiple workspace shapes via shape-extension pattern"
  - Line 19: "this document remains the practitioner-shape articulation"
  - Line 21: "framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory"
  - Line 72: "framework is restricted to practitioner shape — framework is shape-neutral"
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" for framework/shape relationship + concept-by-concept worked examples
- `Framework C scope` (where shape definitions live)
- ARCH Layer 3 shape topic + per-shape detail (placeholder until Phase 3)
- Other foundational meta-primitives: `framework`, `mechanism`, `policy`

---

## skill

- **Class**: PRIMITIVE (atomic; the work-logic unit) — single-aspect (no multi-scope manifestation)
- **Layer**: cross-cutting (skill is an application-level work-logic unit that lives within specialists; manifests at whatever scope the containing specialist manifests at)
- **Axis**: cross-axis (skills serve any axis depending on what work they encode)
- **VISION usage**: implicit (VISION line 7 says "codified expertise bundled as specialists"; skills are the atomic units of that expertise; not directly defined as glossary term in VISION)

**Canonical**: An atomic unit of work logic within a specialist — a behavioral procedure invoked when its trigger conditions match (loading semantics — auto-load, explicit-load, lazy-load — are substrate-defined per Pattern A; `auto-loaded` is the convention in Anthropic-plugin-substrate but not architecturally mandated). Skills are the smallest composable unit of codified expertise; specialists bundle multiple skills (+ entities + memory + adapters) into a distributable expertise package. (Note: deliberately NOT "behavioral protocol" — `protocol` is locked architectural vocabulary for Pattern A pluggable subsystems.)

**What it is**: A skill is what you'd reach for when you want to express "do this specific kind of work when this condition is met." Skills have triggers (when they fire), body content (what they instruct), and may declare output schemas (Pydantic models for structured output). Multiple skills compose into a specialist; the specialist is the cohesion abstraction; the skill is the atomic unit.

**What it is NOT**:
- Not a `specialist` — specialist is the bundle; skills are units within it
- Not a `workspace` — workspace activates specialists (which contain skills); workspace doesn't activate skills directly
- Not a `mechanism` — skills are application-level work logic, not framework-level interface contracts
- Not a sparring sub-mechanism — those are specific axis-2 capabilities (counter-argument, confidence calibration, etc.); skills are general-purpose work units that may USE sparring mechanisms
- Not a `workflow` — workflow is the broader pattern of work; skills are atomic actions within workflows

**Cross-archetype illustration** (named examples; archived plugin/skills/ catalog):
- **orchestrator** — coordinates session-open + decision routing + state management (PBS-Schulz)
- **save-baustein** — saves reusable text patterns to memory (PBS-Schulz; cross-archetype)
- **draft-textteil-b** — drafts B-Plan-Begründung text (planning-domain; PBS-Schulz)
- **validate-checklist** — validates work against doctype checklists (cross-archetype)
- **citation-verification** — checks legal/scholarly citations (cross-archetype)
- **review-draft** — runs layered review with sparring mechanisms (cross-archetype)

A specialist activates a coherent set of skills; e.g., `planning-document-work` specialist bundles `orchestrator + save-baustein + draft-textteil-b + review-draft + validate-checklist + research-references + verify-citations + ...`.

**Boundary test**: Three questions:
1. Is this an atomic unit of work logic that fires on a trigger? → it's a skill
2. Is this codified expertise BUNDLED as a distributable unit? → it's a `specialist` (containing skills)
3. Is this a framework-level interface contract? → it's a `mechanism`, not a skill

**Composes with**:
- `specialist` — specialist contains skills as its atomic work-logic units; skill cannot be used outside specialist context — a specialist provides the skill's runtime context, dependencies, references. **Note**: this specialist-as-skill-bundle constraint is a PBS architectural commitment (per archived `terminology-and-specialist-primitive.md`); differs from Anthropic's bare-skill plugin convention where skills can exist standalone in `plugin/skills/`. Phase 6 reconciles which convention applies to PBS app-skill rebuild.
- `mechanism` — skills use framework mechanisms (audit emission, source-grounding, sparring) at runtime via the substrate
- `workflow` — skills participate in broader workflows (sequence of skill firings + decisions)
- `actor` — skills emit AuditEvents via the AI runtime that fires them (`actor_kind: ai_runtime`); the enum value is deliberately NOT `skill` to avoid naming collision with this primitive
- `adapter` — skills invoke adapters at runtime to interact with external systems (e.g., draft-cover-mail invokes email-adapter; verify-citations invokes MCP-corpus-adapter); the adapter is the integration boundary, the skill is the work-logic unit firing it

**Source**:
- VISION (`VISION.md`) line 7 (thesis): "codified expertise bundled as specialists" — skills implicit as the atomic units of expertise
- Locked GLOSSARY entry `specialist`: "skills are atomic work logic units within a specialist; specialist is the bundle that contains skills"
- Inherited from Anthropic plugin convention: skills as auto-loaded behavioral protocols with trigger frontmatter

**See**:
- `specialist` (which contains skills)
- ARCH Layer 3 skill-detail topics (placeholder until Phase 3 — skill granularity 3-test, frontmatter schema, output validation; archived material to consult: `skill-expert-agent-and-domain-knowledge.md`, `terminology-and-specialist-primitive.md` for `specialist:` frontmatter requirement)

---

## sparring (axis 2)

- **Class**: DERIVED (claim/mode defined in VISION)
- **Layer**: cross-cutting
- **Axis**: axis-2
- **VISION usage**: directly used (`VISION.md` axis 2 — second interlocking principle)

**Canonical**: An interaction mode (axis 2) where AI challenges, generates counter-arguments, names uncertainty, and resists giving easy answers. VISION axis 2 frames sparring as "load-bearing runtime mechanism" (using "mechanism" colloquially — meaning load-bearing AT RUNTIME, distinct from the locked architectural primitive `mechanism` = atomic interface contract). Architecturally, the framework supports the axis via the Sparring Protocol (Pattern A primitive; surface + impls + selection) + 8 sparring sub-mechanisms (each a framework-level interface contract per locked `mechanism` vocabulary).

**What it is**: The second VISION axis. AI participates in sparring-mode interaction, distinct from oracle-mode (humans submit AI's answer as their own; performance same as AI alone) or validator-mode (humans ask AI to support preconceptions; sycophancy loop; performance worse than AI alone). Per Vivienne Ming's research, only sparring-mode produces value rivaling or beating prediction markets. Sparring keeps the practitioner critically engaged.

**What it is NOT**:
- Not optional skill called per-task (it's a load-bearing runtime PILLAR in practitioner-shape)
- Not antagonistic-AI for its own sake (sparring is in service of the practitioner-author's growing capacity, not for confrontation)
- Not sparring-always (oracle mode is right for fact lookup; sparring overhead misplaced for trivial questions)
- Not the same as "sparring mechanisms" (the mechanisms — counter-argument, confidence calibration, etc. — are framework-level capabilities; sparring is the MODE characterized by these mechanisms)

**Cross-archetype illustration**: legal practice sparring on legal arguments; research lab sparring on methodology + manuscript claims; planning bureau sparring on Begründung argumentation choices; auditor sparring on audit-finding interpretations — same axis applies wherever practitioner faces nontrivial judgment calls.

**Boundary test**: ask "does the AI challenge / generate counter-arguments / surface uncertainty, or deliver easy answers?" If easy-answers → answer-machine failure mode (axis 2 failure).

**Composes with**:
- 8 sparring sub-mechanisms (specific instances of the abstract `mechanism` primitive; ARCH Layer 3 detail, NOT separate GLOSSARY entries): `counter-argument`, `confidence calibration`, `visible reasoning`, `selective friction`, `asymmetric knowledge respect`, `anti-sycophancy`, `commit-to-recommendations`, `what's-missing`
- `sparring mechanisms` — class of axis-2 mechanisms (collective term; per-mechanism detail in ARCH Layer 3)
- `claim` — sparring fires AT claim granularity (counter-arguments target individual claims; confidence calibration applies per claim; selective friction triggers per claim ambiguity)

**Source**: `VISION.md` line 142 ("## Sparring partner, not answer machine (axis 2)"); line 100 ("### Vivienne Ming — sparring as the productive mode (axis 2 anchor)"); line 81 (axis-2 robustness claim — sparring becomes MORE valuable as AI accuracy increases); line 190 (sparring-mechanisms framing).

**See**:
- VISION "Sparring partner, not answer machine (axis 2)" section + Foundations Vivienne Ming subsection
- ARCH Layer 3 axis-2-mechanism topic (placeholder until Phase 3)

---

## specialist

- **Class**: PRIMITIVE (atomic; the bundled-expertise unit) — **bipartite multi-aspect Pattern B** (DEFINITION in Framework C; INSTANCE-CONTENT in Owner B)
- **Layer**: multi-aspect (Framework C for the distributable definition; Owner B for entities owned by the deployed specialist instance)
- **Axis**: cross-axis (specialists support any axis through their bundled skills + entities + adapters)
- **VISION usage**: directly used (`VISION.md` thesis line 7: "codified expertise bundled as specialists")

**Canonical**: A composable bundle of codified expertise — skills + entities + memory + adapters — distributable as a unit. Bipartite multi-aspect primitive: a specialist's DEFINITION lives at Framework C scope (the distributable bundle); when a workspace activates a specialist, the entities owned by the specialist's instance live at Owner B scope. NOT a Pattern A primitive — a specialist has no multiple interchangeable implementations; it IS its definition.

**What it is**: The cohesion abstraction for codified expertise. A specialist packages everything needed to address a defined competence area into a single distributable unit. Workspaces activate specialists via `workspace.md`'s `specialists_active` field; an activated specialist runs within the workspace's substrate, contributing its skills + entities + memory to the workspace's work output. Specialists are designed to be reusable across workspaces (e.g., `citation-verification` works in legal, research, and planning workspaces); marketplace distribution (per archived ROADMAP v3) treats specialists as the canonical distributable unit.

**Cardinality + lifecycle**: Specialist DEFINITIONS are immutable Framework C distributables. Specialist INSTANCES are activated/deactivated by `workspace.md` `specialists_active` changes; multiple specialists active per workspace simultaneously. Specialist instance content (entities owned by the deployed specialist instance — e.g., bausteine, work-units of the specialist's kind) lives at Owner B as workspace-scope managed entities; **persists across activation/deactivation cycles** (deactivating a specialist doesn't delete its accumulated content; preserves practitioner work). ARCH Layer 3 settles instance-content destruction semantics (deletion-with-audit vs archival; on workspace dissolution).

**What it is NOT**:
- Not a Pattern A primitive — specialist has NO multiple interchangeable implementations (the `planning-document-work` specialist is one specific bundle, not interchangeable with another impl)
- Not a `workspace` — workspaces activate specialists; specialist is one of many elements a workspace activates
- Not a `skill` — skill is the atomic unit of work logic WITHIN a specialist; specialist is the bundle that contains skills
- Not a `practitioner` — practitioner is the human author; specialist is the codified expertise that the practitioner-led workspace deploys
- Not the `framework` — framework provides universal mechanisms; specialist is one Framework C definition among many primitive kinds

**Cross-archetype illustration** (named, archived examples):
- **planning-document-work** — domain-anchored specialist; PBS pioneer reference; bundles skills for B-Plan-Begründung drafting + review
- **citation-verification** — cross-archetype specialist; usable in legal practice (case-law citations), research lab (paper citations), planning bureau (legal-text citations)
- **project-management** — cross-archetype business specialist
- **invoicing** — cross-archetype business specialist (with adapter for accounting integration)
- **brand-voice** — cross-archetype creative specialist
- **legal-research** — legal-practice-anchored specialist

A workspace activates a domain-relevant set: PBS-Schulz might activate `planning-document-work + project-management + invoicing`; Müller Law workspace might activate `legal-research + citation-verification + project-management + invoicing`.

**Boundary test**: Three questions:
1. Is this a unit of work logic that fires on a trigger? → it's a `skill` — within a specialist
2. Is this a deployment scope? → it's a `workspace`
3. Is this codified expertise bundled as a distributable unit? → it's a specialist
4. Disambiguator: is this multiple interchangeable implementations of one Protocol surface? → it's a Pattern A primitive (substrate / adapter / protocol), NOT specialist

**Composes with**:
- `workspace` — workspace activates specialists per `specialists_active` field in `workspace.md`
- `Framework C scope` — specialist DEFINITIONS live here as distributable bundles
- `Owner B scope` — specialist INSTANCE-CONTENT (entities owned by the deployed specialist instance) lives here
- `skill` — skills are atomic work logic units within a specialist
- `mechanism` — specialists use framework mechanisms (audit emission, source-grounding, sparring) via the substrate at runtime
- `shape` — shape policies may mandate certain specialists or constrain what's permitted (e.g., practitioner-shape may mandate sparring-relevant specialists)
- `adapter` — specialists may bundle adapter implementations as part of their package (per locked `adapter` entry)
- `work-unit` — specialists DEFINE work-unit kinds (the kind discriminator lives in specialist DEFINITION at Framework C); workspace's active specialists determine which work-unit kinds are available in that deployment

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "A workspace pools and leverages codified expertise (bundled as specialists)"
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)" — implies specialists deploy to multiple shapes
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Other multi-aspect primitives": specialist named as Pattern B (bipartite definition+instance-content)
- Locked GLOSSARY entries: `Framework C scope` (members include specialist DEFINITIONS); `Owner B scope` (members include specialist instance content)

**See**:
- `Framework C scope` (where specialist definitions live)
- `Owner B scope` (where specialist instance content lives)
- `workspace` (which activates specialists)
- ARCH Layer 3 specialist-detail topics (placeholder until Phase 3 — specialist granularity 3-test, composability axes, two-tier classification, marketplace mechanics; archived material to consult: `terminology-and-specialist-primitive.md`, `entity-md-scope-model-restructure.md`)

---

## substrate

- **Class**: PRIMITIVE (atomic; the deployment-runtime unit) — **tri-aspect Pattern A** (Protocol surface = mechanism; implementations = Framework C definitions; running instance = workspace-bound at Owner B)
- **Layer**: multi-aspect (framework-mechanism for the Protocol surface; Framework C for implementations; Owner B at workspace runtime)
- **Axis**: cross-axis (substrate hosts all axes' runtime behavior)
- **VISION usage**: implicit (VISION doesn't directly use "substrate"; concept lives in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE + Framework C scope members)

**Canonical**: A deployment runtime that workspaces run on — defines the execution model (agent loop, dataflow, event-driven, etc. — substrate-impl-defined), tool surface, capability/permission flow, lifecycle events, and session/context primitives via a Protocol surface; concrete implementations (Claude Agent SDK, MS Agent Framework, future) live as Framework C definitions; a workspace selects exactly one substrate via its `workspace.md`.

**What it is**: One of the framework's mechanism categories (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE). The substrate provides the runtime contract any workspace operates on. The Protocol surface (interface contract) is universal/shape-neutral; specific implementations differ in how they realize that surface (e.g., Claude Agent SDK = Anthropic plugin runtime; MS Agent Framework = Microsoft agentic framework). **Substrate is an instance of the Protocol pattern** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Recurring patterns: Protocol pluggability"): Substrate Protocol Surface (mechanism; framework-level) + concrete Implementations (Framework C definitions: Claude Agent SDK, MS AF, future) + a running Instance bound to each workspace deployment (Owner B; via `workspace.md` `substrate:` field). NOT the same as specialist's bipartite manifestation (specialist is definition+instance-content; no multiple implementations like substrate has).

**What it is NOT**:
- Not the `framework` itself — framework is the universal mechanism layer; substrate is one mechanism category within the framework
- Not a `shape` — shape is the policy bundle archetype; substrate is a runtime-contract mechanism that shapes specify compatibility with (not equivalent)
- Not a `workspace` — workspaces select a substrate via `workspace.md`; substrate is what they run ON
- Not the `codebase` — substrate is the architectural runtime contract + its implementations; the codebase realizes one substrate impl

**Cross-archetype illustration**: All shapes use SOME substrate; not all shapes are compatible with all substrates. Examples (named, factually existing):
- **Claude Agent SDK** — Anthropic's plugin/agent runtime; archived as primary substrate per session-12 substrate eval
- **MS Agent Framework** — Microsoft's agentic framework; archived as second backend
- (Future substrates may emerge — e.g., specialized runtimes for Tier-3 / federation / autonomous-business shapes)

A practitioner-shape PBS-Schulz workspace might run on Claude Agent SDK; a knowledge-graph-shape workspace might run on a different substrate optimized for retrieval; the SAME framework mechanisms (audit emission, source-grounding, etc.) compose with each.

**Boundary test**: ask "what's the runtime contract this workspace operates on?" → it's the substrate. Three disambiguators:
1. Is this a runtime-contract Protocol surface or implementation? → substrate (mechanism + Framework C definition)
2. Is this a configured value in a shape's bundle? → it's a `policy`, not substrate
3. Is this a workspace-instance-level binding? → it's workspace configuration (workspace selects which substrate)

**Composes with**:
- `framework` — substrate is one mechanism category within the framework
- `mechanism` — the substrate's Protocol surface IS a mechanism (framework-level interface contract)
- `Framework C scope` — substrate IMPLEMENTATIONS live here as distributable definitions
- `shape` — shapes declare compatibility with substrates (not all shapes work on all substrates)
- `workspace` — workspace selects exactly one substrate via `workspace.md`
- `Owner B scope` — running substrate instance is bound to workspace deployment (Owner B)
- `protocol` (architectural) — substrate Protocol surface is one of the framework's architectural Protocols

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" — substrate listed as Framework C definition member + framework-mechanism category
- `Framework C scope` GLOSSARY entry: "substrate definitions (runtime contracts: Claude Agent SDK, MS AF, future)"
- `workspace` GLOSSARY entry: "workspace runs on exactly one substrate"

**See**:
- `Framework C scope` (where substrate definitions live)
- `workspace` (which selects exactly one substrate)
- ARCH Layer 3 substrate-detail topics (placeholder until Phase 3 — Substrate Protocol method set; per-substrate implementation detail; deployment-tier framing; eval-framework integration; archived material to consult: `substrate-protocol-design.md`, `substrate-agentic-framework.md`, `sdk-deep-read.md`)

---

## tacked-on AI

- **Class**: DERIVED (failure mode of axis 1; the contrast / anti-pattern)
- **Layer**: cross-cutting
- **Axis**: axis-1 (failure mode of axis-1)
- **VISION usage**: directly used (`VISION.md` line 37 + 53 axis-1 contrast tables; line 43 axis-interaction: "Tacked-on but well-designed sparring is still tacked-on (axis 1 failure)"; line 60: "Most 'AI agent' demos are tacked-on"; line 90 axis-1 falsification: "falsified if practitioner deployments show better outcomes from tacked-on features"; line 150 + 205 + 225: category collapse explicitly produces tacked-on shape)

**Canonical**: The architectural failure mode for axis 1 — AI as discrete convenience-feature bolted onto an unchanged human workflow; no cross-session state; no orchestration awareness; no colleague-grade discipline. Per VISION: the contrast that makes axis 1 concrete; what intertwining is NOT.

**What it is**: The architectural anti-pattern. Concrete markers of tacked-on:
- AI provides convenience features (summarize this; format that; suggest synonyms) on the side of unchanged workflow
- Workflow itself is unchanged — practitioner drafts, reviews, sends as before; AI is a side-tool not a co-worker
- No cross-session memory: each interaction starts fresh
- AI output isn't held to source-grounding / audit / defensibility discipline (because it doesn't compose into accountability-bearing work-products)
- Most "AI agent" demos and most current AI-product integrations are tacked-on by default — adding "AI to existing tool" usually preserves the tool-shape and adds AI-as-feature

Tacked-on AI is the LANDSCAPE DEFAULT against which axis 1 deliberately positions; recognizing it requires understanding what intertwining looks like in contrast.

**What it is NOT**:
- Not "bad AI" or "low-capability AI" — tacked-on can be technically excellent and still be tacked-on (a brilliant AI summarizer that doesn't change workflow shape is still tacked-on)
- Not "AI assistant" specifically — AI assistants CAN be intertwined or tacked-on depending on architectural integration depth; the failure mode is structural, not naming
- Not the same as "tool use" — AI using tools is a substrate capability; tacked-on is about whether AI participation reshapes workflow
- Not a moral failing — tacked-on is the SAFE DEFAULT; intertwining requires deliberate architectural choice + workflow as precondition

**Cross-archetype illustration** (tacked-on failure modes per archetype):
- Practitioner-shape: planner uses AI to summarize sources but drafts Begründung manually with no AI participation in argumentation = tacked-on
- Legal practice: lawyer uses AI for legal research lookup but writes brief without AI co-drafting = tacked-on
- Research lab: researcher uses AI to format citations but writes manuscript without AI methodology engagement = tacked-on
- Auditor: auditor uses AI to spell-check report but writes findings without AI evidence-traversal = tacked-on
- Generic-knowledge-work: any AI-in-text-editor where AI suggests improvements on already-drafted text = tacked-on by default

Same anti-pattern shape across archetypes: AI on the side, not in the workflow. Mixed-state common in transition deployments — partial intertwining at some workflow stages with tacked-on at others; recovery starts by deepening architecture at the tacked-on stages.

**Boundary test**: Three questions (mirror of intertwined AI; tacked-on markers):
1. Does AI only participate when explicitly invoked? → if yes, tacked-on
2. Does AI output live in side-channel chat (doesn't compose into artifacts)? → if yes, tacked-on
3. Does AI restart fresh each session with no work-state awareness? → if yes, tacked-on

Any "tacked-on-side" answer = axis 1 at risk; all three = full tacked-on failure.

**Cardinality + lifecycle**: N/A — failure-mode shape, not instance. The mode manifests whenever axis-1 mechanisms are absent OR the workflow precondition is missing OR category collapse forces tacked-on shape regardless of intent. Mode state can shift in BOTH directions: tacked-on → intertwined via architecture deepening; intertwined → tacked-on via category collapse / host-UX changes / workflow-bypass.

**Composes with**:
- `intertwining (axis 1)` — tacked-on AI is the failure mode for this axis
- `intertwined AI` — positive mode contrasted
- `co-worker` — the relational frame tacked-on AI fails to realize
- `category collapse` — the risk that produces tacked-on regardless of architectural intent (host environment forces tacked-on shape per VISION line 150)
- `workflow` — tacked-on AI exists outside the workflow (workflow continues unchanged); intertwined exists within
- `practitioner` — the human side that operates without AI co-worker participation in the tacked-on mode
- `substrate` (Instance aspect) — the runtime, in tacked-on mode, doesn't share workflow state architecturally

**Source**:
- VISION (`VISION.md`) lines 37, 43, 53, 60, 90 (falsification), 150 (category-collapse connection), 205, 225 (axis-1 check)
- Locked GLOSSARY entries: `intertwining (axis 1)`; `intertwined AI`

**See**:
- `intertwining (axis 1)` (the axis tacked-on fails)
- `intertwined AI` (positive contrast)
- `co-worker` (relational frame failed)
- `category collapse` (the force that produces tacked-on regardless of intent)
- ARCH Layer 3 axis-1-mechanism topic (placeholder until Phase 3)

---

## workflow

- **Class**: PRIMITIVE (atomic; the work-pattern unit)
- **Layer**: cross-cutting — bipartite-candidacy under examination. The DEFINITION aspect (the pattern itself: "how does B-Plan-Begründung drafting actually proceed?") could be Framework C OR Layer A (domain-keyed); the INSTANCE aspect (workflow execution in a specific workspace) is realized through sessions over time. Phase 3 ARCH resolves whether workflow is single-aspect cross-cutting (current) or bipartite Pattern B (DEFINITION + INSTANCE-CONTENT, parallel to specialist).
- **Axis**: axis-1 (primary anchor — workflow is what intertwined AI intertwines WITH); cross-axis (workflows span all axes during execution)
- **VISION usage**: directly used (`VISION.md` thesis line 7: "interactive practitioner workflows"; line 27 axis 1: "AI is a co-worker in the workflow itself"; "Workflow as precondition" implication retained in current VISION)

**Canonical**: A pattern of work in a domain — sequence of activities, artifacts, decisions, and handoffs that defines how a practitioner produces accountability-bearing output. Per VISION axis 1: workflow is what intertwined AI intertwines WITH; without a workflow, axis 1 has nothing to embed in.

**What it is**: A domain-specific structure of work. Workflows are pattern-level concepts: "how does B-Plan-Begründung drafting actually proceed?" or "how does a legal brief get from intake to filing?" Workflows include activities (drafting, reviewing, sending), artifacts (Begründung, Stellungnahme, signed brief), decisions (which argumentation type, which authorities to address), and handoffs (between sessions, between humans, between AI and human). Sessions execute parts of workflows; specialists provide the skills that progress workflow steps; the architecture's intertwining requirements (persistent state, orchestration, audit, etc.) are what allow AI to participate in workflows as co-worker rather than as discrete-feature-tool.

**Cardinality + lifecycle**: Workflows are SPECIALIST-DEFINED — each specialist DEFINITION declares the workflow patterns it supports for its competence area (e.g., `planning-document-work` specialist defines the B-Plan-Begründung drafting workflow). Cardinality per workspace = sum of workflows defined across active specialists. Lifecycle = workflow patterns are immutable (defined in specialist DEFINITION at Framework C); workflow EXECUTIONS run against work-units over time and span many sessions. ARCH Layer 3 settles workflow representation schema + handoff semantics + multi-session continuity.

**What it is NOT**:
- Not a `session` — session is one execution unit; workflow is the broader pattern that sessions execute parts of
- Not a `skill` — skill is atomic work logic that fires on a trigger; workflow is the broader pattern of work in which many skills fire
- Not a `specialist` — specialist bundles skills + entities for a competence area; workflow is domain-pattern that may span multiple specialists' contributions
- Not a `workspace` — workspace is the deployment container; workflow is the work-pattern the workspace supports

**Cross-archetype illustration**: workflows differ per archetype (the discriminator is what kind of accountability-bearing output gets produced and how):
- Planning bureau: B-Plan-Begründung drafting workflow (intake → research → draft → review → send → response handling)
- Legal practice: matter workflow (intake → research → drafting → filing → response cycle)
- Research lab: manuscript workflow (research → drafting → peer review → revision → submission)
- Auditor: audit engagement workflow (planning → fieldwork → finding → report)

Per VISION's "Workflow as precondition" implication: domains with rich, structured workflows are natural fits for axis-1 intertwining. Generic "knowledge work" without explicit workflow is much harder.

**Boundary test**: Three questions:
1. Is this a domain-specific pattern of work (sequence + artifacts + decisions + handoffs)? → it's a workflow
2. Is this one bounded execution unit? → it's a `session`
3. Is this an atomic work-logic unit? → it's a `skill`

**Composes with**:
- `intertwining (axis 1)` — workflow is what axis-1 AI intertwines WITH; "Workflow as precondition" implication
- `session` — sessions execute parts of workflows (one workflow may span many sessions)
- `skill` — skills are atomic work-logic units that progress workflow steps
- `specialist` — specialists provide bundles of skills relevant to specific workflow stages
- `workspace` — workspaces SUPPORT workflows (workspace's deployed specialists + state enable workflow progression)
- `work-unit` — workflows EXECUTE AGAINST work-units; one workflow may progress one work-unit through stages, or multiple workflows in sequence may progress the same work-unit (drafting workflow → review workflow → send workflow against same project)

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "interactive practitioner workflows"
  - Line 27 (axis 1): "AI is a co-worker in the workflow itself, not a feature bolted onto an unchanged human workflow"
  - "Workflow as precondition" implication subsection retained in tightened VISION
- `intertwining (axis 1)` GLOSSARY entry: "workflow — what intertwining intertwines WITH (axis 1 needs a workflow to intertwine with)"
- `session` GLOSSARY entry: "sessions execute parts of broader workflows"

**See**:
- `intertwining (axis 1)` (which intertwines with workflow)
- `session` (which executes parts of workflow)
- `work-unit` (the deployment-bound artifact one workflow execution produces / progresses)
- ARCH Layer 3 workflow-detail topics (placeholder until Phase 3 — workflow representation, handoff semantics, multi-session workflow continuity; archived material to consult: workflow descriptions in archived plugin/skills/)

---

## work-unit

- **Class**: PRIMITIVE (atomic; the deployment-bound work-artifact unit; specialist-defines kind)
- **Layer**: cross-cutting — bipartite-candidacy under examination (similar shape to workflow): the KIND DISCRIMINATOR lives in specialist DEFINITION (Framework C); the INSTANCE lives at Owner B as workspace-scope managed entity. Could be reclassified bipartite Pattern B (parallel to specialist) if Phase 3 ARCH determines kind-discriminator deserves multi-aspect treatment. Currently single-aspect cross-cutting.
- **Axis**: cross-axis (work-units are the artifact-containers all axes operate against — axis-1 intertwined work happens IN work-units; axis-2 sparring fires DURING work-unit progression; axis-3 authorship attaches TO work-units)
- **VISION usage**: implicit (VISION's "interactive practitioner workflows" line 7 produces work-products; work-unit is the deployment-bound container for those products; not directly named in VISION)

**Canonical**: The deployment-bound work-artifact container — a single bounded unit of accountability-bearing work that one or more workflows progress against. The KIND is specialist-defined (e.g., `project` for planning bureau, `matter` for legal practice, `case` for medical practice, `engagement` for consulting, `manuscript` for research lab, `audit` for accounting). Lives at Owner B as workspace-scope managed instance; cardinality is multiple per workspace (a practitioner-shape workspace typically tracks N concurrent work-units across active workflows).

**What it is**: The artifact-shaped container for "one piece of accountability-bearing work the practitioner will sign and defend." A work-unit has lifecycle (initiated → in-progress → completed / sent / archived), associated artifacts (drafts, references, sent versions), state (decisions made, sources cited, sparring outcomes), and audit-trail attribution (events emitted scoped to this unit). Workflows execute AGAINST work-units (one workflow may progress one work-unit through stages; or one work-unit may be progressed by multiple workflows in sequence).

**What it is NOT**:
- Not a `workflow` — workflow is the PATTERN (sequence of activities + artifacts + decisions); work-unit is one deployment-bound INSTANCE of work the workflow progresses
- Not a `session` — sessions are bounded interactions; work-units span many sessions over time
- Not a `specialist` — specialists DEFINE work-unit kinds (per the kind discriminator in specialist's DEFINITION); work-unit is the deployment-bound instance, specialist is the codified-expertise bundle that knows how to handle that kind
- Not a `workspace` — workspace contains many work-units; workspace is the deployment container, work-unit is one bounded artifact-instance within it
- Not the produced output — produced output (Begründung PDF, signed brief, submitted manuscript) is an artifact OF a work-unit; the work-unit is the bounded-work-container that holds the artifact + its history + decisions

**Cross-archetype illustration** (kind names per archived corpus + cross-archetype examples):
- **Practitioner-shape (PBS-Schulz pioneer)**: `project` kind (e.g., "25-03 Maxsolar - Friedrichshof" tracking one B-Plan project from intake through approval)
- **Legal practice**: `matter` kind (one engagement: client + opposing party + filings + case state)
- **Medical practice**: `case` kind (one patient encounter or treatment trajectory)
- **Consulting**: `engagement` kind (one project: scope + deliverables + billing)
- **Research lab**: `manuscript` kind (one paper from drafting through submission and revision)
- **Accounting / auditor**: `audit` kind (one audit engagement: scope + fieldwork + findings + report)
- **Autonomous-business-shape**: `task` or `order` kind (operator-supervised AI work batch)
- **Personal-OS-shape**: `task` or `goal` kind
- **Federation-shape**: cross-node `peering` work-units possible

The KIND is specialist-defined; the kind enum lives in specialist DEFINITION at Framework C. Workspace's active specialists determine which kinds are available in that deployment.

**Boundary test**: Three questions:
1. Is this the DEPLOYMENT-BOUND artifact-instance one piece of work tracks? → it's a work-unit
2. Is this the PATTERN of how that work proceeds? → it's a `workflow`
3. Is this the DEFINITION of which work-unit kinds exist for this competence area? → it's the kind discriminator inside a `specialist` DEFINITION (at Framework C)

**Composes with**:
- `specialist` — specialists DEFINE work-unit kinds; the kind discriminator lives in specialist DEFINITION (Framework C); workspace's active specialists determine which kinds are available
- `workflow` — workflows EXECUTE AGAINST work-units (one workflow progresses one work-unit through stages; or multiple workflows in sequence)
- `workspace` — workspace CONTAINS work-units as workspace-scope managed instances at Owner B; cardinality multiple per workspace
- `Owner B scope` — work-unit instances live there as workspace-scope managed entities (per `Owner B scope` members list — already cross-referenced)
- `event` — events are emitted scoped to work-units (each event records its work-unit attribution per archived audit-trail-v2 schema)
- `actor` — actors emit events against work-units (practitioner authorizing send; AI runtime drafting; external client responding)
- `practitioner` — practitioners are the human authors signing work-unit outputs; defensibility test asks "will the practitioner be able to defend THIS work-unit's outputs?"
- `claim` — claims compose into work-unit output content; one work-unit contains N claims; work-unit is the artifact-container, claim is the atomic content-unit within

**Source**:
- Locked GLOSSARY entries: `Owner B scope` ("work-unit instances (kind specialist-defined: `project` for planning bureau; `matter` for legal practice; `case` for medical practice; `engagement` for consulting; `manuscript` for research; `audit` for accounting)"); `workspace` (cross-archetype examples reference per-archetype work patterns); `specialist` (Composes-with implies specialists define kinds)
- Archived corpus for kind discriminator detail (Phase 3 ARCH territory): `entity-md-scope-model-restructure.md` (Owner B placement); per-specialist DEFINITION files in archived `plugin/skills/` (e.g., planning-document-work specialist's `project` kind)

**See**:
- `Owner B scope` (where work-unit instances live)
- `workflow` (which executes against work-units)
- `specialist` (which defines kinds)
- `workspace` (which contains work-units)
- ARCH Layer 3 work-unit-detail topics (placeholder until Phase 3 — kind discriminator schema, lifecycle states, artifact attachment semantics, audit-trail attribution; archived material to consult: `entity-md-scope-model-restructure.md`, archived per-specialist DEFINITIONs)

---

## workspace

- **Class**: PRIMITIVE (atomic; the deployment-instance unit)
- **Layer**: cross-cutting (workspace integrates framework mechanisms + shape policies + practitioners; orthogonal to mechanism/policy split per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- **Axis**: cross-axis (workspace is the container in which all three VISION axes manifest)
- **VISION usage**: directly used (`VISION.md` thesis line 7 + cross-archetype examples throughout)

**Canonical**: The deployment-instance container that integrates framework mechanisms + shape policies + active specialists + practitioners + state into a coherent unit for accountability-bearing work; selects exactly one shape via its `workspace.md`; lives at Owner B scope.

**What it is**: The top-level deployment primitive — what gets bound when a practitioner deploys PBS for their work. A workspace is the central Owner B instance: its `workspace.md` selects shape + substrate + active specialists; its workspace-scope managed entities (practitioner-record, Actor, plus shape-policy-mandated engagement-target entities like `Client` in practitioner-shape, `Customer` in autonomous-business-shape, etc. — engagement-target entities are deliberately shape-policy-mandated rather than framework-level) live at Owner B; its layered content (references, doctypes, bausteine per Layer A) varies by domain/state context (configured via workspace's `scope.{domains, states}`).

**Cardinality**: exactly 1 workspace per "deployment" (where deployment = one bound runtime: a single git-clone-instance + active substrate + workspace.md configuration; multi-deployment scenarios = multiple workspaces). "Deployment" definition flagged for Phase 3 ARCH sharpening — current preliminary lock is "one git-cloned + activated workspace.md per deployment."

**What it is NOT**:
- Not the `framework` — framework is the universal mechanism layer (what's POSSIBLE); workspace is one deployment instance built from framework + shape policies
- Not a `shape` — shape is the policy-bundle archetype (definition; lives in Framework C); workspace is an instance that SELECTS exactly one shape
- Not a `specialist` — specialist is composable expertise; workspace ACTIVATES specialists from the list in `workspace.md`
- Not a `session` — sessions are bounded interaction units WITHIN a workspace
- Not a single application running on a server — deployment-shape-agnostic (could be local, cloud, hybrid); not synonymous with "office" (prior naming, demoted session 13; workspace is broader)

**Cross-archetype illustration**:
- Planning bureau: "PBS-Schulz workspace"
- Legal practice: "Müller Law workspace"
- Research lab: "Smith Lab workspace"
- Solo creative: "Anna's Writing workspace"
- Knowledge graph: "BNatSchG knowledge workspace"
- Federation node: "Federation X workspace"

All workspaces are built from the same framework; they differ in selected shape (which configures policies), active specialists, and Layer A content per their domain/state scope.

**Boundary test**: ask "what's the deployment scope of this work?" The answer names a workspace.
- If answer is "a single feature" → it's a skill or specialist, not a workspace
- If answer is "the open-source product" → it's the framework, not a workspace
- If answer is "a configuration archetype" → it's a shape, not a workspace
- If answer is "a particular bounded interaction" → it's a session, not a workspace

**Composes with**:
- `shape` — workspace selects exactly one shape via `workspace.md` (the shape's policy bundle configures workspace's behavior over framework mechanisms)
- `framework` — workspace inherits framework's mechanisms; the selected shape's policies determine which are active/mandatory and what defaults apply
- `Owner B scope` — workspace lives as the central instance + container for workspace-scope managed entities (practitioner-record, Actor, Client)
- `specialist` — workspace activates a list of specialists per `specialists_active` field in `workspace.md`
- `practitioner` — workspace serves practitioner(s); records at Owner B (bipartite primitive: human cross-cutting, record at Owner B)
- `substrate` — workspace runs on exactly one substrate (selected via `workspace.md` `substrate` field)
- `session` — interaction units occur within a workspace
- `workflow` — workspaces SUPPORT workflows; workspace's deployed specialists + state + active substrate enable workflow progression (axis-1 intertwining requires workflow to embed in)
- `work-unit` — workspaces CONTAIN work-units as workspace-scope managed instances (cardinality multiple per workspace); kinds defined by active specialists
- `Layer A scope` — workspace's `scope.{domains, states}` configuration determines which Layer A content (references, doctypes, bausteine) applies

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "A workspace pools and leverages codified expertise (bundled as specialists) to automate and support interactive practitioner workflows in a coherent manner"
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Multiple cross-archetype examples throughout
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Cross-cutting" classification (workspace listed as cross-cutting alongside practitioner, session, workflow)

**See**:
- `Owner B scope` (where workspace itself + workspace-scope managed entities live)
- `shape` (what workspace selects)
- `Layer A scope` (content scoping per workspace's domain/state configuration)
- ARCH Layer 3 workspace-detail topics (placeholder until Phase 3 — `workspace.md` schema; multi-practitioner workspace; legal-entity workspace context; deployment configurations)
