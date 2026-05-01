---
id: practitioner
label: Practitioner Workspace
type: shape
status: active
last_updated: 2026-05-01

# Framework C — Framework primitive
framework_kind: shape
framework_key: practitioner

# Layer 2 — shape-specific
display_name: Practitioner Workspace
semver: "0.1.0"

default_configs:
  coordination_protocol: event-coordination
  sparring_intensity: always-on
  audit_granularity: claim-level
  author_primitive: practitioner-as-author
  trust_model: practitioner-judgment
  time_model: turn-based

protocols_allowed:
  coordination:
    - event-coordination
  sparring:
    - always-on-sparring
  audit:
    - claim-level-audit
    - claim-level-audit-with-action-overlay
  trust:
    - practitioner-judgment-trust
  time:
    - turn-based-time

shape_specific_primitives:
  - sparring_runtime_mechanism
  - source_grounding_contract
  - claim_level_audit_emission

substrate_compat:
  - claude-agent-sdk
  - ms-agent-framework

required_extensions: []

option_b_floor:
  anti_art_25_trap: enforced
  claim_level_audit: enforced
  human_authority_chain: enforced
---

# Practitioner Workspace

## What this shape is for

The practitioner shape is the workspace shape for **expert professionals** doing **accountability-bearing work** under their own name — planners, lawyers, researchers, accountants, consultants, advisors, and similar regulated practices. The practitioner is the human author who signs, defends, and bears legal/professional liability for everything the workspace produces on their behalf.

This shape is the canonical realization of `VISION.md`'s three axes:

1. **Intertwined-AI-workflow** (axis 1) — AI is a continuous co-worker in the practitioner's actual production of accountability-bearing artifacts (drafting B-Plan-Begründungen, contracts, manuscripts, audit reports). Not a discrete feature catalog bolted onto an unchanged workflow.
2. **Sparring as load-bearing runtime mechanism** (axis 2) — AI generates counter-arguments, names uncertainty, surfaces "what's missing", resists giving easy answers. Always-on runtime pillar (per `default_configs.sparring_intensity: always-on`); not opt-in skill called per-task. Per Vivienne Ming research: only sparring mode produces the value; oracle mode wastes the human partner; validator mode actively degrades.
3. **Authorship preservation** (axis 3) — practitioner remains the defensible expert author of everything the workspace produces. Defensibility test: "will the user be able to defend this output six months from now under challenge, having forgotten the details?" If yes, the architecture works.

PBS-bureau (the planning bureau Gunther operates) is the **pioneer reference deployment** of this shape. The shape generalizes to any practitioner archetype where these three axes apply.

## When to use this shape (vs alternatives)

Use **practitioner shape** when:

- The work produced has **external accountability** (signed by a named human; goes to authorities/regulators/clients/courts; bears professional liability)
- The practitioner has **codified expertise** that can be augmented by sparring + reference grounding (vs purely tacit work where AI augmentation provides little leverage)
- The deployment **single-practitioner-bound** or **small team of practitioners** (federation shape covers cross-org sharing; this shape's authorship model is per-practitioner)
- Workflow has **discrete artifacts** with identifiable judgment moments (where sparring + selective friction earn their cost)

Use a **different shape** when:

- **Autonomous-business shape** — operator/board supervises AI specialists as workforce; AI executes tasks autonomously between approval cycles (e.g., AI-org running customer support + invoicing + scheduling within budget caps; per Paperclip-style framing). Practitioner shape's always-on-sparring would impose cost without benefit.
- **Personal-OS shape** — single human + AI for life management; sparring optional; audit lighter; no external accountability concern. Practitioner shape's claim-level audit + Option B floor enforcement would over-engineer.
- **Knowledge-graph shape** — corpus + curator + AI for retrieval; no workflow loop; specialists empty; no external accountability concern. Practitioner shape's coordination Protocol would impose unused machinery.
- **Federation shape** — cross-node specialist sharing; multi-practitioner identity federation. Practitioner shape doesn't address cross-node sharing primitives.
- **Hybrid shape** — combinations (e.g., practitioner with autonomous sub-orchestration for routine work). Compose explicitly via hybrid extension.

## Default configs explained

Per `default_configs`, this shape configures the 6 pluggable Protocol axes with values appropriate for accountability-bearing practitioner work:

### `coordination_protocol: event-coordination`

Cross-specialist coordination is event-shaped, not call-shaped. Specialists emit AuditEvents; subscribed specialists react via `event_subscriptions`. Events carry decision provenance + sources + causes (per claim-level audit). Reasons:

- **Loose coupling** — specialists don't directly invoke each other; testable + replaceable
- **Auditability** — every cross-specialist interaction is recorded as event; defensible reconstruction at any later point
- **Practitioner workflow fit** — practitioner work is event-driven by nature (Stellungnahme arrives → triggers review; phase advances → triggers next-phase scaffolding; deadline approaches → triggers reminder)
- **Per Row 4 of `a2a-and-gemini-pattern-emulation.md`** — preserves transport-swap-to-A2A path for federation shape later

Alternative `call-coordination` (used by autonomous-business shape) is rejected for practitioner shape: tickets + atomic checkout + assignments suit operator-supervised AI workforce, not practitioner authoring.

### `sparring_intensity: always-on`

Sparring is the **load-bearing runtime mechanism**, not an optional skill called per-task. Per VISION axis 2 + Ming research: oracle mode and validator mode actively degrade the human partner; only sparring mode produces the value. Always-on means:

- Counter-argument is FIRST-CLASS output (`ReviewOutput.counter_argument` Pydantic field; per `sparring-output-v1.md`)
- Confidence calibration always required (`ReviewOutput.confidence` + `confidence_basis`)
- Visible reasoning always required (`min_length=100` per Pydantic schema)
- "What's missing?" checkpoint always present
- Anti-sycophancy + asymmetric knowledge respect + commit-to-recommendations are behavioral (chronological-defer for structural; sparring sessions accumulate empirical pattern data)

Alternative `optional` (autonomous-business shape) treats sparring as a skill operator can invoke; practitioner shape rejects this because sparring being optional means by-default oracle mode, which degrades practitioner capacity per Ming's Information-Exploration Paradox.

### `audit_granularity: claim-level`

Every claim made by the AI in produced output is bound to evidence at write-time. Audit emission carries `sources[]` (where the claim came from — tool result, reference, prior decision) + `causes[]` (what triggered this output — user request, prior event, scheduled trigger). Action-level audit (who/what/when/cost) is overlay on top of claim-level baseline (per `protocols_allowed.audit: [claim-level-audit, claim-level-audit-with-action-overlay]`).

Reasons:
- **Defensibility test** (per VISION axis 3) — "user can defend output six months from now" requires reconstructable claim-evidence chain
- **EU AI Act Art. 11 + Art. 13 + Art. 26(6)** — audit-by-construction maps to documentation + transparency + record-keeping requirements
- **Berufsrecht** (German professional law) — practitioner-as-deployer cleanest posture under Art. 25(1)(b) requires structural binding of claims to evidence

Alternative `action-level` only (autonomous-business shape default) is insufficient for practitioner shape — knowing WHO did WHAT WHEN doesn't reconstruct WHY a specific claim was made. Action-level adds tracking; claim-level adds defensibility.

### `author_primitive: practitioner-as-author`

The practitioner is the human author bearing legal/professional liability for output. AI assists; practitioner authors + signs + defends. This contrasts with `operator-as-supervisor` (autonomous-business shape) where operator authorizes AI workforce within bounds, or `individual` (personal-OS) where there's no external accountability concern.

Concrete consequences for this shape:
- Workspace has at least one Actor entity (the practitioner) marked as the accountability-bearer
- Send gates require explicit practitioner confirmation before any external transmission
- Module-decision logs capture practitioner's reasoning at judgment moments
- Rendered output bears practitioner's name + signature + identity macros (per LaTeX style spec)

### `trust_model: practitioner-judgment`

AI cooperation is bounded by practitioner judgment — not by budget caps (autonomous-business shape) or implicit trust (personal-OS). Concrete manifestations:

- Four-way decision menu at every memory-write or backlog-append (capture / handle / backlog / drop)
- Compile gate, send gate, layered review gate, state-transition gate — human-authority gates per VISION axis 1's intertwining-requirements list
- Selective friction calibration (per VISION axis 2's sparring-requirements) — friction reserved for accountability moments + judgment moments; mechanical work automated seamlessly

### `time_model: turn-based`

Practitioner workflow is turn-based — practitioner engages, AI responds, practitioner reviews, AI continues. Long-running heartbeats (autonomous-business shape) would conflict with practitioner-as-author primitive: between practitioner turns, AI shouldn't be making accountability-bearing decisions. Per Substrate Protocol design: turn-based time model maps to Claude Agent SDK's session model (CASDK is turn-based); MS Agent Framework also supports turn-based out of box.

Alternative `long-running` (autonomous-business shape) requires substrate adapter implementation (per `entity-md-scope-model-restructure.md` W4 watch-list — concrete implementation awaits first autonomous-business shape extension built).

## Shape-specific primitives

These primitives ship with the practitioner shape and are required for the shape's accountability-bearing posture:

### `sparring_runtime_mechanism`

Per `sparring-output-v1.md`: `ReviewOutput` + `RecommendationOutput` Pydantic schemas define the structural sparring contract (counter-argument + confidence + reasoning + whats_missing as required fields). The runtime mechanism wires these schemas into the sparring axis Protocol implementation (`always-on-sparring` per default_configs). Substrate-specific materialization (CASDK plugin output schema; MS AF module output spec) handled per substrate adapter.

### `source_grounding_contract`

Per VISION axis 1's intertwining-requirements: every legal citation backed by a tool result, never invented from training memory. The contract is enforced at claim-emission time by the audit Protocol (claim-level-audit). Practitioner-shape-specific aspect: the contract requires referenceable sources for every accountability-bearing claim (legal citations, regulatory references, prior project decisions). Other shapes may relax this (autonomous-business may emit budget-class claims without reference grounding for routine operations).

### `claim_level_audit_emission`

Per Option B floor's claim-level audit axiom: AuditEvent emission with `sources[]` + `causes[]` fields bound to every claim in produced output. Practitioner-shape-specific aspect: the emission Pydantic schema has stricter validation (sources required for legal/regulatory claims; causes required for module-decision-bearing claims). Materialization-side enforced by substrate (CASDK RunHooks emit on every tool result; MS AF lifecycle hooks emit on every step).

## Substrate compat reasoning

`substrate_compat: [claude-agent-sdk, ms-agent-framework]`

Both substrates support the practitioner shape's requirements:

- **Claude Agent SDK** (PRIMARY) — turn-based session model; in-process MCP; RunHooks for audit emission; output schema validation. PBS-marketed deployment uses CASDK as primary substrate per `substrate-agentic-framework.md` decision. Shape-specific primitives materialize as: sparring_runtime_mechanism → CASDK output_schema; source_grounding_contract → CASDK RunHooks PRE/POST tool callbacks; claim_level_audit_emission → CASDK RunHooks emit.
- **Microsoft Agent Framework** (SECONDARY backend) — turn-based execution; module manifest validation; lifecycle hooks for audit emission. Per `substrate-agentic-framework.md`: full backend; Path B frontend deferred to consulting signal. Shape-specific primitives materialize via MS AF module spec + lifecycle hooks.

Other substrates (future) need to be evaluated for practitioner-shape compat: must support turn-based time model + per-call output schema validation + lifecycle hooks for audit emission. Substrates failing any of these requirements cannot host practitioner shape.

## Migration from other shapes

Not applicable for v1. Practitioner shape is the PBS pioneer reference; PBS-Schulz workspace is built directly on this shape from initial bind. Migration tooling for shape changes (e.g., autonomous-business → practitioner if a deployment regulates) is part of W1 marketplace mechanics watch-list (awaiting marketplace v3 launch milestone).

Per `shape-extension-and-architectural-floor.md` D2 reframe (session-15 amendment): v1 does not support hot-swap shape on running workspace. Workaround: create new workspace + migrate content manually.

## Option B floor enforcement

Per `option_b_floor` Layer 2 frontmatter — all 3 axioms structurally enforced; cannot be disabled without explicit `option_b_floor_override: NonPBSConformant` workspace.md field (per shape-extension DR D5 reframe, session 15):

### `anti_art_25_trap: enforced`

Specialist conformity manifest is a Pydantic gate. Specialists declare their `intended_purpose` at registration; runtime gate validates that specialist's actual usage matches declared purpose. If a specialist tries to materially shift its intended purpose (e.g., a planning-document-work specialist starts producing legal advice), gate rejects + emits `art_25_trap_attempted` AuditEvent. Per EU AI Act Art. 25(1)(b): specialist authorship that materially shifts intended purpose makes practitioner a PROVIDER (full Art. 16 obligations). Make impossible by structural design.

### `claim_level_audit: enforced`

Every claim emission requires `sources[]` + `causes[]` fields populated. Gate validates at write-time. Empty `sources[]` rejected for accountability-bearing claims. Per `audit-trail-v2.md`: structured + append-only; immutable historical record.

### `human_authority_chain: enforced`

Every accountability-bearing output has at least one human-authority gate in the chain. Configurable granularity per `default_configs.author_primitive: practitioner-as-author`:

- Per-output (default for practitioner shape) — every external send requires explicit practitioner confirmation
- Per-decision-class — practitioner authorizes a class of decisions; AI executes within class
- Per-policy — practitioner authorizes a policy document; AI applies policy to instances
- Per-budget-cycle — practitioner reviews monthly; AI operates within budget bounds (more autonomous-business-like; not default for practitioner shape)
- Per-specialist-installation — practitioner installs specialist with conformity manifest; specialist operates within manifest

Practitioner-shape default = per-output (highest authority granularity). Other granularities available for specific deployment configurations within the shape.

## Cross-references

- `VISION.md` — three axes thesis; this shape's value claim
- `ARCHITECTURE.md` — "Three-category scope model" section + "Workspace shapes catalog" + "Option B architectural floor"
- `docs/decisions/shape-extension-and-architectural-floor.md` — DR establishing shape extension framework + Option B floor
- `docs/decisions/entity-md-scope-model-restructure.md` — DR establishing this entity-md form (Framework C category)
- `docs/decisions/substrate-agentic-framework.md` — substrate decision (CASDK + MS AF dual-substrate)
- `docs/decisions/sparring-output-v1.md` — sparring schemas + always-on enforcement
- `docs/decisions/audit-trail-v2.md` — claim-level audit emission contract
- `docs/conventions/entity-md-spec.md` — Layer 1+2 frontmatter contract; §6 body conventions for `shape` entity type
