# Decision record: Shape-extension framework + Option B architectural floor (session 14)

**Status**: ACCEPTED (session 14, 2026-04-30)
**Owner**: ARCHITECTURE.md (Workspace shapes catalog + Option B section); ROADMAP commitment #25 (Shape extension framework + Protocol pluggability)
**Sharpening metadata**: Multi-round iterative — emerged from competitive deep-read (Paperclip "could framework do this?" question) + EU AI Act regulatory analysis (anti-Art-25-trap structural enforcement) + layered approach formalization (framework shape-neutral + practitioner positioning).
**Related**:
- `terminology-and-specialist-primitive.md` (session 13 Sub-DR A — workspace/specialist primitives this decision builds on)
- `positioning-three-tier-framework.md` (session 13 Sub-DR B — three-tier framing where shape-extension lives)
- `closest-neighbors-deep-read.md` (session 14 sibling DR — Paperclip analysis triggered "could framework host autonomous-business?" question)
- `vision-realignment-session14.md` (session 14 sibling DR — VISION scope clarification + architectural inheritance subsection consumes Option B)
- Session 13 Sub-DR A "Make-wrong-shapes-impossible" reference (v0.21 ARCH discipline) — Option B applies this discipline to shape neutrality

## Context

Three converging threads forced this decision:

1. **Layered approach formalization** (session 14 user direction): "framework is option b shape neutral. that's the open source product. we market option a." Made explicit the architectural truth that framework primitives don't structurally privilege practitioner shape.

2. **Paperclip deep-read question** (session 14 user direction): "option b could do what Paperclip does right? with the correct instantiation? would possibly extend the backend and substrate of course." Forced sharpening of "what does shape-neutral framework actually mean."

3. **EU AI Act regulatory analysis** (session 14 deep-look): anti-Art-25-trap (preventing specialist authorship from autonomously shifting intended purpose) needs to be **structurally enforced**, NOT solvable by convention. Per Make-wrong-shapes-impossible discipline.

Together these surfaced a load-bearing architectural decision: **what does the framework structurally enforce regardless of workspace shape, vs what does the framework leave to per-shape configuration?**

## Decision

Two locked decisions, deeply coupled:

| # | Decision |
|---|---|
| 1 | **Shape-extension framework** — workspace shapes are pluggable extensions; framework provides shape-neutral primitives; concrete shapes (practitioner / autonomous-business / personal-OS / KG / federation / hybrid) live as `extensions/shapes/<shape-id>/` with default configs + shape-specific primitives |
| 2 | **Option B architectural floor** — even shape-neutral framework primitives structurally enforce certain accountability axioms regardless of shape configuration; shapes can configure axis intensities but cannot disable structural floor without explicit framework override (which produces non-PBS-conformant deployment) |

## 1. Shape-extension framework

### Architectural model

```
Framework primitives (shape-NEUTRAL core)
├── Workspace, Specialist, Skill (always)
├── Substrate Protocol (always)
├── Audit Protocol (claim-level OR action-level granularity — config)
├── Coordination Protocol (event-shaped OR call-shaped — config)
├── Sparring Protocol (always-on OR optional — config)
└── Trust/Governance Protocol (practitioner-judgment OR budget-policy — config)

Shape extensions (per-shape additions)
├── extensions/shapes/practitioner/     (PBS pioneer reference)
├── extensions/shapes/autonomous-business/  (Paperclip-style — community could build)
├── extensions/shapes/personal/         (PAI-style — community could build)
├── extensions/shapes/knowledge-graph/  (corpus-only)
├── extensions/shapes/federation/       (cross-node specialist sharing)
└── extensions/shapes/hybrid/           (combinations)
```

### Workspace shape = bundle of configuration defaults + supporting primitives

A "workspace shape" is more than "who's inside." It's a bundled set of:

| Configuration axis | Practitioner-shape default | Autonomous-business-shape default |
|---|---|---|
| Coordination | event-shaped | call-shaped (ticket + atomic checkout) |
| Sparring intensity | always-on runtime pillar | optional skill (when operator requests) |
| Audit granularity | claim-level (sources[] + causes[]) | action-level (who/what/when/cost) |
| Author primitive | practitioner-as-author | operator-as-supervisor |
| Trust model | practitioner-judgment + sparring | budget-caps + approval-gates |
| Coordination primitive | events + event_subscriptions | tickets + assignments + locks |
| Time model | turn-based (CASDK substrate) | long-running heartbeats (substrate adapter) |

Plus shape-specific primitives the framework needs to provide:
- **Practitioner shape needs**: sparring runtime, claim-level audit, source-grounding contract
- **Autonomous-business shape needs**: ticket primitive, budget primitive, long-running runtime, cost events
- **Personal shape needs**: light audit, individual author binding
- **KG shape needs**: corpus + entity + reference primitives only; no workflow loop
- **Federation shape needs**: cross-node specialist sharing protocol + identity federation

### Per-shape extension contract

Each shape extension declares:

```yaml
# extensions/shapes/<shape-id>/shape.md (Layer 1+2 hybrid-shape)
shape_id: practitioner | autonomous-business | personal | knowledge-graph | federation | hybrid
display_name: "Practitioner Workspace" | "Autonomous Business" | etc.
default_configs:
  coordination_protocol: event | call
  sparring_intensity: always-on | optional | none
  audit_granularity: claim-level | action-level | citation-only
  author_primitive: practitioner | operator | individual | curator
  trust_model: practitioner-judgment | budget-policy | none
  time_model: turn-based | long-running
shape_specific_primitives:
  - <pydantic-class-or-protocol-impl>
substrate_compat: [claude_agent_sdk, ms_agent_framework, ...]
required_extensions: []  # other shape extensions this depends on
```

Specialists can declare shape compatibility:
```yaml
specialist:
  shapes_supported: [practitioner, autonomous-business]  # cross-shape
  OR
  shapes_supported: [practitioner]  # shape-specific
```

### PBS pioneer = practitioner-shape extension reference implementation

PBS-Schulz (planning bureau) is one workspace using the practitioner-shape extension. The practitioner-shape extension is what PBS-the-product MARKETS. Other shape extensions are framework-supported but not PBS-marketed.

### Tom Sawyer dynamic

Open-source framework + shape-extension contract = community can build shape extensions for shapes PBS doesn't market. Examples:
- Community member wanting Paperclip-style autonomous-business → builds `extensions/shapes/autonomous-business/` with ticket primitive + budget primitive + long-running runtime adapter
- Community member wanting PAI-style personal → builds `extensions/shapes/personal/` with light audit + individual author binding
- Community member wanting Helsing-style sovereign-AI for defense → builds `extensions/shapes/sovereign/` with extra encryption + audit retention + actor verification

PBS doesn't gatekeep; framework hosts. **Framework is workspace-shape-neutral within Option B floor.**

## 2. Option B architectural floor

### The structural enforcement (cannot be disabled regardless of shape)

Three axioms framework structurally enforces:

| # | Structural axiom | Why load-bearing |
|---|---|---|
| 1 | **Anti-Art-25-trap gate** (specialist conformity manifest as Pydantic gate) | EU AI Act Art. 25(1)(b): specialist authorship that materially shifts intended purpose makes practitioner a PROVIDER (not deployer) — full Art. 16 obligations (CE marking, conformity assessment, EU database registration). Make this impossible by structural design. Specialist conformity manifest declares non-modification; gate enforces |
| 2 | **Claim-level audit emission** (decision provenance + sources[] + causes[]) | Defensibility cannot be reconstructed if claims aren't bound to evidence at write-time. Action-level audit (who did what when) is necessary but insufficient. Claim-level always emitted; shapes can ADD action-level overlay |
| 3 | **Human authority somewhere in accountability-bearing output chain** | EU AI Act Art. 14 human oversight + DACH Berufsrecht (planner remains liable regardless of AI assistance). Shape-configurable granularity (per-output / per-decision-class / per-policy / per-budget-cycle / per-specialist-installation) but NOT zero-human for accountability-bearing output |

### What CAN be configured per shape

Other axes are configurable (per shape needs):

- **Sparring intensity**: always-on (practitioner default) / optional (autonomous-business) / none (KG)
- **Audit overlay**: action-level can be added on top of claim-level baseline
- **Coordination**: event-shaped (PBS default) / call-shaped (Paperclip-style alternative)
- **Trust model**: practitioner-judgment / budget-policy / none
- **Time model**: turn-based / long-running
- **Author granularity**: per-output / per-decision-class / per-policy / etc.

### Real-world parallel — autonomous trading systems

**The Option B model mirrors how autonomous trading systems work in finance:**
- Algos can execute thousands of trades per second autonomously
- BUT human risk officer / compliance officer authorized the strategy + position limits
- BUT audit trail captures every decision
- BUT compliance gate prevents algo from changing strategy autonomously

PBS Option B = same shape applied to AI workspaces. **Autonomous execution + human authority chain at configurable granularity.**

### Worked example — autonomous-business shape under Option B

**Allowed**:
- Operator approves "PBS-AI-Org may invoice clients up to €X per month autonomously" (per-decision-class authority)
- AI-org generates and sends invoices within class, no per-output approval needed
- Sparring configured to optional (operator can request review per-task)
- Action-level audit added on top of claim-level baseline (operator wants to track every action)
- AI-org runs invoicing + customer support + scheduling autonomously between approval cycles

**Blocked by structural floor**:
- AI installs new specialists without operator approval (anti-Art-25 gate fires)
- AI shifts intended purpose (e.g., support-specialist starts giving legal advice → conformity manifest violated)
- Output going to regulators/courts/clients without ANY traceable human authorization in chain
- Pure unsupervised AI-org running indefinitely without ANY human-in-the-chain

### What it looks like for practitioner-shape (PBS-Schulz)

**Structural floor**: human signer per B-Plan output; claim-level audit per § citation; specialist conformity manifest per planning-document-work specialist.

**Configured (practitioner-shape defaults)**: sparring always-on (per VISION axis 2); event-shaped coordination; per-output authority; turn-based time.

### Why Option B over Option A (full freedom)

Considered Option A (framework hosts visions PBS doesn't endorse — full freedom). Rejected because:

| Reason | Detail |
|---|---|
| **Make-wrong-shapes-impossible discipline** (ARCH v0.21) | Structural enforcement > convention. Anti-Art-25-trap as Pydantic gate (impossible-by-construction) > anti-Art-25-trap as documented best-practice (solvable-at-deployment-time) |
| **EU AI Act protection** | Practitioner-author primitive cleanest under Art. 25 — but only if specialist authorship STRUCTURALLY can't shift intended purpose. Convention-level enforcement = Art. 25 trap risk per deployment |
| **PBS brand integrity** | OS license = community can fork. If accountability-violating fork claims "built on PBS" + ships into EU regulated context → PBS-the-brand exposed. Structural floor = "if it shipped on PBS, it has accountability binding" |
| **Practitioner protection** | EU practitioner using community shape extension shouldn't accidentally violate professional accountability. Structural floor protects them |
| **Tom Sawyer dynamic preserved** | Option B doesn't prevent shape extensions; it requires shape extensions to respect accountability floor. Pure-autonomy use cases (research simulation, internal R&D, no external output) can declare "non-accountability-bearing" workspace OR explicit framework override flag |

The freedom Option B gives up (some pure-autonomy use cases need explicit override) is small relative to the protection gained (every PBS deployment has structural accountability floor).

## Composition with disciplines

| Discipline | Connection |
|---|---|
| **Make-wrong-shapes-impossible (v0.21)** | Direct application — structural enforcement of accountability floor; specialist conformity manifest as Pydantic gate (impossible-by-construction); anti-Art-25-trap structurally prevented |
| **Pattern-vs-instance (v0.20)** | Workspace shapes themselves are properly pattern-vs-instance: framework primitives = pattern; shape extensions = instance-level configurations of pattern |
| **AI-as-runtime hybrid-shape (v0.16)** | Shape extension is canonical hybrid-shape application — `extensions/shapes/<id>/shape.md` Layer 1+2 frontmatter + body conventions; AI fuses at runtime per shape config |
| **Substrate-pluggability (v0.30)** | Shape extension's `substrate_compat` field declares which substrates support; substrate Protocol abstracts |
| **Glue-not-replacement (v0.15)** | Framework GLUES shape extensions; doesn't replace any shape's specific primitives. Adapter Protocol applies to shape-specific external integrations |
| **Entity-elevation 3-test** | Shape extension's primitives go through entity 3-test; e.g., "ticket" in autonomous-business shape passes entity-elevation test |
| **Specialist-granularity 3-test** | Specialists within shape extension still subject to specialist 3-test |
| **Sharp defer rule (v0.20)** | Defers below all chronological-valid (no manufactured restraint) |

## Pre-implementation surfacing (per Round 3 decision-design-sharpening)

Operational concerns surfaced for #25 implementation phase head-start:

| Concern | Position |
|---|---|
| **Boot order** | Workspace bootstraps shape extension first (loads default configs + shape primitives), then specialists per shape's compatibility check |
| **Shape conflict** | Workspace can use exactly ONE shape extension (no shape composition at workspace level); specialists declare shape compatibility; mismatch = error at install time |
| **Hybrid shape** | "Hybrid" shape extension is a NAMED shape that combines multiple shape primitives (not "use shapes A+B simultaneously"); explicit hybrid extension required |
| **Shape extension lifecycle** | Can shape be hot-swapped on running workspace? DEFER to first concrete need; default = shape locked at workspace creation |
| **Multi-shape deployment** | Can ONE PBS instance host MULTIPLE workspaces with DIFFERENT shapes? YES — each workspace independent; substrate shared |
| **Shape extension versioning** | Per-shape semver; framework-shape compatibility matrix in shape.md |

## Defers (chronological-valid)

| Defer | Home | Cost being avoided |
|---|---|---|
| **D1: Shape extension marketplace** (publishable shapes + community shape contributions) | ROADMAP v3 marketplace | Marketplace shape locked Sub-DR B; v3 mechanics deferred |
| **D2: Hot-swap shape on running workspace** | First concrete need | Implementation simplifies if shape locked at workspace creation |
| **D3: Cross-shape specialist portability** (specialist authored for practitioner shape used in autonomous-business shape) | First concrete cross-shape user | No concrete user today |
| **D4: Long-running runtime substrate adapter** (needed for autonomous-business shape) | First autonomous-business shape implementation | Substrate adapter is shape-extension-driven; build when shape needed |
| **D5: Pure-autonomy override flag** (declares non-PBS-conformant deployment) | First concrete pure-autonomy use case | No concrete user; theoretical override path |

All chronological-valid: each names specific information that doesn't exist yet.

## Cascade

| Layer | Change |
|---|---|
| `docs/decisions/shape-extension-and-architectural-floor.md` | NEW — this file |
| `ARCHITECTURE.md` | NEW section: "Workspace shapes — framework-supported catalog" (lists shapes + shape extension contract); NEW section: "Option B structural floor" (3 axioms + anti-Art-25-trap + claim-level audit + human authority chain); reference card row added; v0.31 → v0.32 version log entry |
| `ROADMAP.md` | NEW commitment #25: Shape extension framework + Protocol pluggability (foundational; Tom Sawyer dynamic enablement; AFTER #11 + #9; BEFORE marketplace v3) |
| `VISION.md` | Already updated session 14 — VISION scope section + architectural inheritance subsection reference Option B |
| `docs/strategic-positioning.md` | Will reference: layered approach + framework breadth as Tom Sawyer / community-shape-contribution upside |
| `entity-md-spec.md` | Add shape-as-type to namespacing examples |
| `plugin-conventions.md` | Add shape extension authoring guidance (when #25 implementation starts) |
| `HANDOFF.md` | Session 14 entry covers shape-extension model + Option B as major architectural decision |

## Files touched

- `docs/decisions/shape-extension-and-architectural-floor.md` (NEW — this file)

## Pattern-vs-instance check

| Domain | Pattern-vs-instance verdict |
|---|---|
| Framework primitives shape-neutral | ✅ Pattern-level |
| Shape extension contract | ✅ Pattern-level (any shape can be authored) |
| Concrete shape extensions (practitioner / autonomous-business / etc.) | ⚠ Instance-level (deployment chooses which shapes to install/build) |
| Option B structural floor (3 axioms) | ✅ Pattern-level (applies to ALL shapes by structural enforcement) |
| Configurable axis intensities | ⚠ Instance-level (per-shape default; per-deployment adjustable within shape) |

All architectural decisions properly leveled. Concrete shape choices stay instance-level; framework breadth + structural floor stay pattern-level.

## Revisit triggers

- Concrete autonomous-business shape extension is built (validates ticket primitive + budget primitive + long-running runtime adapter design)
- Concrete personal-shape extension is built (validates light-audit + individual-author primitives)
- Concrete KG-shape extension is built (validates corpus-only primitives)
- Specialist marketplace launches (per ROADMAP v3) — validates shape extension + specialist composition story
- Real first-bind deployment using non-practitioner shape (would be community-driven; PBS-marketed stays practitioner)
- EU AI Act Commission Art. 6 guidelines (Feb 2026) — may force tightening of anti-Art-25-trap structural enforcement
- Pure-autonomy use case demand (would activate D5 override flag work)
