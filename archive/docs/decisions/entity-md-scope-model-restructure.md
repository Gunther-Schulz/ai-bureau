# Decision record: Entity-md scope model restructure (three-category) + Definition vs instance binding pattern (session 15)

**Status**: ACCEPTED (session 15, 2026-05-01) — 3-round sharpening (full monty + 2 user-triggered).

**Owner**: ARCHITECTURE.md "Layering convention: scope orthogonality" rewrite + `docs/conventions/entity-md-spec.md` §3 rewrite + this file.

**Sharpening metadata**: Phase 1 of decision-design-sharpening skill (`plugin/skills/decision-design-sharpening/SKILL.md`). 3 rounds: round 1 (full monty AI-proactive), round 2 (user-triggered; 11 refinements: 2 revisions + 9 expansions), round 3 (user-triggered; 8 refinements: 2 revisions + 6 expansions). Total 19 refinements; all Pareto-improving. Architectural-pattern-surfacing in round 3 (Definition vs instance binding pattern named).

**Related**:
- `ai-as-runtime-hybrid-shape.md` (Layer 1+2 frontmatter contract; entity-md form)
- `terminology-and-specialist-primitive.md` (#22 Sub-DR A; specialist primitive; workspace+specialist+project scope axes — these become Owner B category here)
- `positioning-three-tier-framework.md` (#22 Sub-DR B; marketplace of specialists — extends to marketplace of all Framework C primitives per E3-7)
- `shape-extension-and-architectural-floor.md` (shapes as framework primitives; Option B floor — non-overridable axioms anchored in Framework C category)
- `substrate-protocol-design.md` (substrate Protocol surface — substrates become Framework C primitives with definitions in entity-md form)
- `governance-and-identity-sourcing.md` (decision 4: prose-rules-as-conventions; per-category governance per E2 round 2)
- `ARCHITECTURE.md` "No-defer principle" + "Preliminary-lock principle" (v0.33) — both rules unblocked this restructure

## Context

Three converging threads forced this decision (session 15):

1. **No-defer principle (v0.33)** + **Preliminary-lock principle (v0.33)** were codified earlier session 15 in response to user direction. Combined effect: existing 6-axis entity-md scope enum (universal / domain / state / specialist / workspace / project) is preliminary-locked, not "given". Cannot defer restructure with chronological-defer-as-YAGNI rationalizations.

2. **Framework-axis question** surfaced session 15 during ROADMAP #25 entry-point design (where do shape/substrate/protocol entity-md fit?). Adding 3 new flat-enum values would deepen an existing semantic-category violation: the 6 existing axes already conflate two distinct gate-dispatch behaviors (Layer A merges; Owner B looks up by ownership).

3. **Make-wrong-shapes-impossible discipline (v0.21)** applied to scope dispatch: gate-dispatched scope enum should structurally reflect dispatch semantics, not require deployment-time disambiguation logic. The flat 6-axis enum was a partial violation already; extending it to 9 flat values would compound the violation.

The sharp question forced by the new no-defer + preliminary-lock rules: **what is the IDEAL design of the entity-md scope model per VISION lens, not "minimum extension of existing"?**

## Decision

Two coupled architectural decisions:

| # | Decision |
|---|---|
| 1 | **Three-category scope structure** — replace flat 6-axis enum with three explicit scope categories: **Layer A** (universal / domain / state), **Owner B** (workspace / specialist / project), **Framework C** (shape / substrate / protocol). Each entity has exactly one category populated; Pydantic at-least-one-of validator enforces. |
| 2 | **Definition vs instance binding pattern** (NEW architectural pattern) — framework-primitive DEFINITIONS live in Framework C (immutable, distributable, framework-supplied); INSTANCE-SELECTION lives in Owner B as workspace.md reference fields binding to definitions; per-instance Layer 3 customization (deferred to #9 per existing entity-md-spec) handles workspace-specific overrides without modifying Framework C definitions. |

## 1. Three-category scope structure

### Architectural model

```
Layer A — Layered content (merge by specificity)
├── universal: applies to every deployment
├── domain: applies to deployments in active domains (PV-FFA, Wind, Naturschutz, ...)
└── state: applies to deployments in active states (MV, BB, BY, ...)
   ↓ Effective content = universal + active-domains + active-states (per workspace.md scope.{domains,states}); most-specific wins on conflicts. Used for: doctypes, references, manifests, bausteine, conventions content.

Owner B — Deployment-instance ownership
├── workspace: workspace.md itself (the deployment scope)
├── specialist: entities owned within a specialist's instance (skills, processes, internal references — distinct from specialist DEFINITION which is Framework C)
└── project: project entity instances (per-project state.md, decisions, snapshots)
   ↓ Gate dispatch on owner_scope + owner_key for entity lookup. Entities owned by named scope.

Framework C — Framework primitives (definitions; immutable; distributable)
├── shape: workspace shapes (practitioner / autonomous-business / personal-OS / KG / federation / hybrid)
├── substrate: substrate implementations (claude-agent-sdk / ms-agent-framework / future)
└── protocol: Protocol implementations per axis (event-coordination / call-coordination / always-on-sparring / optional-sparring / claim-level-audit / action-level-audit / ...)
   ↓ Framework registry lookup; compat matrix validation; Option B floor enforcement (anti-Art-25-trap, claim-level audit, human authority chain — non-overridable).
```

### Layer 1 frontmatter (every entity, strict-locked Pydantic)

```yaml
id: <kebab-case>             # unique within scope category
label: <display>
type: <category-rules>       # see "Type namespacing per category" below
status: active|deferred|stub|archived
last_updated: <ISO-8601>

# Exactly ONE of these three categories non-null (Pydantic at-least-one-of validator)
layer_scope: null | universal | domain | state
layer_key: null | <key>      # null when layer_scope=null OR universal; required when domain/state (e.g., "Naturschutz", "MV")

owner_scope: null | workspace | specialist | project
owner_key: null | <key>      # null when owner_scope=workspace; required when specialist (e.g., "planning-document-work") or project (e.g., "<project-id>")

framework_kind: null | shape | substrate | protocol
framework_key: null | <key>  # required when framework_kind non-null (e.g., "practitioner", "claude-agent-sdk", "event-coordination")
```

### Type namespacing per category (per R2 round 2)

- **Layer A**: `<scope>.<entity-type>` (e.g., `universal.doctype`, `domain.reference`, `state.legal-supplement`)
- **Owner B specialist**: `<specialist-id>.<entity-type>` (e.g., `planning-document-work.project-deadline`, `planning-document-work.process`)
- **Owner B workspace**: `workspace.<entity-type>` (e.g., `workspace.actor`, `workspace.client`)
- **Owner B project**: `project.<entity-type>` or just `project` (most projects use Layer 1+2 directly without entity-type sub-discrimination)
- **Framework C** (consistent with existing entity-md-spec §4 registration-file-type exception): unprefixed type matching the kind: `type: shape`, `type: substrate`, `type: protocol`. Identity comes from `id` + `framework_key`.

### Specialist dual-nature (per R3-2 round 3)

Specialist is the only category-spanning primitive. Two facets, not contradictory:

- **Specialist DEFINITION** = Framework C entity. The distributable composable bundle (skills + entities + processes + references + memory + adapters). Lives at `extensions/framework/specialists/<specialist-id>/specialist.md`. Framework-supplied or community-built.
- **Specialist as SCOPE** = Owner B value. Entities WITHIN a specialist's instance (the skills + processes + internal references that ARE the specialist's content) have `owner_scope: specialist, owner_key: <specialist-id>`.

Shape/substrate/protocol do NOT have this dual-nature. Their internal pieces (shape-specific Pydantic schemas, substrate Protocol surface implementations, protocol implementation code) ship as part of the definition's `extensions/framework/<kind>/<id>/` package — they're not Owner B sub-entities.

## 2. Definition vs instance binding pattern (NEW architectural pattern)

Framework-primitive DEFINITIONS live in Framework C category — immutable, distributable, framework-supplied. INSTANCE-SELECTION lives in Owner B as workspace.md reference fields binding to definitions.

### Concrete bindings on workspace.md

```yaml
# workspace.md (Owner B; type=workspace; owner_scope=workspace; owner_key=null)
shape: <shape-id>                          # exactly one (Framework C reference)
substrate: <substrate-id>                  # exactly one (Framework C reference); relocated from backend composition-root code per AI-as-runtime hybrid-shape (E3-3)
specialists_employed: [<specialist-id>+]   # multi-valued (Framework C references)
protocol_overrides:                        # optional; per-axis (Framework C references); defaults inherit from shape
  coordination: <protocol-id>
  sparring: <protocol-id>
  audit: <protocol-id>
  trust: <protocol-id>
  time: <protocol-id>
groupings: dict[str, list[<specialist-id>+]] | null   # deployment-instance optional per #22 Sub-DR A
```

### Validation gate enforces:

- `shape` value is registered in `extensions/framework/shapes/<shape-id>/shape.md`
- `substrate` value is in selected shape's `substrate_compat` list
- `specialists_employed` values are registered AND each specialist's `shapes_supported` includes selected shape
- `protocol_overrides` values are in selected shape's `protocols_allowed: {<protocol-kind>: [<protocol-id>+]}` map per kind
- **Option B floor axioms are NOT overridable** — workspace.md cannot override anti-Art-25-trap gate, claim-level audit emission, or human authority chain (per `shape-extension-and-architectural-floor.md` Part 2). Gate validation rejects override attempts on these axes regardless of workspace request.

### Per-instance Layer 3 customization

Per `ai-as-runtime-hybrid-shape.md` Layer 3 (deferred to #9 implementation): per-deployment extension fields enable specialist-instance / workspace customization without modifying Framework C definitions. Layer 3 mechanism choice (Option A: Pydantic subclass / Option B: declared extra_fields / Option C: metadata dict) lands with #9 Bundle B implementation — independent of this DR.

### Why this pattern matters

The pattern resolves a real architectural ambiguity that existed pre-restructure: where do shape/substrate/protocol/specialist primitives "live"?

- Pre-restructure: ambiguous; primitives partially in backend code (substrate impls), partially in extensions/ (shape extensions per #25), partially as scope axes (specialist per #22).
- Post-restructure: definitions uniformly in Framework C (`extensions/framework/<kind>/<id>/`); instance-selection uniformly in Owner B (workspace.md fields). One pattern; structural enforcement.

This makes marketplace v3 (per #22 Sub-DR B) cleanly extensible — marketplace lists Framework C primitives (specialists, shapes, substrates, protocols all uniformly distributable). Tom Sawyer dynamic per #25 applies uniformly: community can author any Framework C primitive kind.

## Refinements applied (per round)

### Round 1 (full monty AI-proactive): three-category structure proposed

Initial proposal: 6-axis flat enum → three-category structure with Layer A / Owner B / Framework C. Migration scope outlined; per-category type namespacing proposed; cascade items flagged.

### Round 2 (user-triggered): 11 refinements (2 revisions + 9 expansions)

- **R1**: Specialist dual-nature surfaced (definition vs instance) — extended in Round 3 R3-2.
- **R2**: Type namespacing exception for Framework C (consistent with §4 registration-file exception); `type: shape / substrate / protocol` unprefixed.
- **E1**: Per-category lifecycle expectations specified (Layer A: layered-merge; Owner B: per-entity-type lifecycle; Framework C: semver + compat + deprecation).
- **E2**: Per-category governance specified (Layer A: framework-maintainer + experts; Owner B: workspace deployer + specialist authors; Framework C: framework-maintainer + community).
- **E3**: AuditEvent schema — add 6 category fields replacing single scope/scope_key (backward-compat additive per evolution patterns v0.19).
- **E4**: Gate dispatch — single `read_entity` / `write_entity` API with internal category discriminator (rejected per-category split APIs as caller complexity).
- **E5**: Migration script per evolution patterns (structured + mutable; pre-launch zero migration cost).
- **E6**: Boot order specified (workspace → shape → substrate → protocol selections → specialists → Layer A discovery → projects on-demand).
- **E7**: Per-category error model with category-appropriate recovery paths.
- **E8**: Versioning fields per Framework C entity (semver + compat matrices).
- **E9**: Filesystem layout — `extensions/framework/{shapes,substrates,protocols}/<id>/` (nested under `extensions/framework/`).

### Round 3 (user-triggered): 8 refinements (2 revisions + 6 expansions)

- **R3-1**: "Definition vs instance binding" pattern fully spelled out (extends R1) — workspace.md fields concretely defined; per-axis protocol overrides specified.
- **R3-2**: Specialist dual-nature resolution (Framework C definition + Owner B scope facets); shape/substrate/protocol do NOT have dual-nature.
- **E3-3**: Substrate selection relocates to workspace.md (`workspace.md.substrate: <id>`) — replaces backend composition-root-code selection per AI-as-runtime hybrid-shape principle.
- **E3-4**: Per-axis Protocol selection — defaults in shape.md `default_configs.<axis>_protocol`; per-workspace overrides via `workspace.md.protocol_overrides`; Option B floor axioms NOT overridable.
- **E3-5**: Body conventions per Framework C entity type (shape.md / substrate.md / protocol.md / specialist.md sections specified).
- **E3-6**: Per-category gate validation specifics (Layer A: scope_key membership; Owner B: ownership chain integrity; Framework C: registry + compat matrix + Option B floor enforcement).
- **E3-7**: Marketplace v3 implications — extends marketplace from specialists-only to all Framework C primitive kinds (per #25 Tom Sawyer dynamic).
- **E3-8**: Vocabulary lock — "scope category" at meta-level (3 categories); "scope axes" within each category for sub-values.

### Pareto verdict

All 19 refinements Pareto-improving. No manufactured criticism. Round 3 surfaced strong revisions (R3-1, R3-2 — load-bearing pattern naming) plus 6 expansions covering operational + cross-cutting concerns layered on round 2's foundation.

## Composition with existing architecture

| Existing decision / discipline | Connection |
|---|---|
| **#22 Sub-DR A (terminology-and-specialist-primitive.md)** | Workspace + specialist + project primitives are properly Owner B category here. Specialist's dual-nature (Framework C definition + Owner B scope) extends the Sub-DR A primitives without contradicting them. |
| **#22 Sub-DR B (positioning-three-tier-framework.md)** | Marketplace of specialists extends to marketplace of all Framework C primitives (per E3-7). Three-tier framing (Infrastructure / Workspace / Specialist) maps cleanly to substrate (Framework C) / workspace (Owner B) / specialist (Framework C definition). |
| **shape-extension-and-architectural-floor.md** | Shapes are Framework C primitives. Option B floor is structurally enforced via Framework C category gate validation (per E3-6). Filesystem layout shifts from `extensions/shapes/<id>/` to `extensions/framework/shapes/<id>/` (per E9 round 2). |
| **substrate-protocol-design.md** | Substrates become Framework C primitives with entity-md DEFINITION at `extensions/framework/substrates/<id>/substrate.md` (per E3-3). Substrate Protocol surface stays valid; selection mechanism relocates to workspace.md. |
| **ai-as-runtime-hybrid-shape.md (#16)** | Three-category structure preserves Layer 1 + Layer 2 + Layer 3 contract; Layer 1 frontmatter expands with three category fields. Process-as-md pattern unchanged. |
| **Make-wrong-shapes-impossible (v0.21)** | Direct application — three-category structure replaces flat-enum-with-implicit-categories; gate dispatch is structurally distinguished per category. Reduces deployment-time disambiguation logic. |
| **Pattern-vs-instance + No-defer (v0.33)** | This restructure is pattern-level work; happens now under no-defer principle. |
| **Preliminary-lock principle (v0.33)** | Existing 6-axis enum was preliminary-locked; this restructure exercises the principle. |
| **Three evolution patterns (v0.19)** | Entity-md frontmatter is structured + mutable; migration script handles transition (pre-launch = essentially zero cost). |

## Constraints flowing

### To existing artifacts

- **`docs/conventions/entity-md-spec.md`**: §3 Layer 1 frontmatter rewrite (three-category fields replace single scope/scope_key); §3.1 identifier uniqueness within scope-category; §3.2 type namespacing per category; §4 Layer 2 schemas for Framework C entity types (shape/substrate/protocol/specialist) added; §6 body conventions per Framework C entity type added.
- **`ARCHITECTURE.md`** "Layering convention: scope orthogonality" section: rewritten as "Three-category scope model" with Layer A / Owner B / Framework C structure. Reference card row updated (scope dispatch). Version log v0.33 → v0.34 entry.
- **`ROADMAP.md`** commitment #25 scope: rewrite to reflect three-category foundation + actual schema designs (shape.md / substrate.md / protocol.md / specialist.md schemas per Framework C category).
- **AuditEvent schema** (`audit-trail-v2.md` amendment): add 6 category fields (layer_scope / layer_key / owner_scope / owner_key / framework_kind / framework_key) replacing single scope / scope_key (backward-compat additive per evolution patterns).
- **Pydantic gate** (`pbs_core` post-#9 lift): three-category Layer 1 base + per-category dispatch logic + Pydantic at-least-one-of validator + per-category validation rules.

### To future work

- **#9 Bundle B (entity gate + Layer 3)**: implements three-category gate dispatch; Layer 3 mechanism per the existing entity-md-spec defer.
- **#9 Bundle A (specialist module + location/registration)**: registration files (specialist.md / shape.md / substrate.md / protocol.md) follow this DR's framework C category structure.
- **#9 Bundle C (ProjectEntity migration)**: ProjectEntity has owner_scope=project; per-instance phase/lifecycle dict.
- **#9 Bundle D (workspace.md schema)**: workspace.md fields match Definition vs instance binding pattern (shape/substrate/specialists_employed/protocol_overrides/groupings).
- **#11 Cowork integration**: filesystem path migrations (`extensions/specialists/<id>/` → `extensions/framework/specialists/<id>/`; `extensions/workspace/` stays Owner B layout).
- **#6 Audit-trail v2 retrofit**: AuditEvent schema additions; per-category audit filtering.
- **Marketplace v3** (post-launch): listing schema includes all Framework C primitive kinds.

## Watch-list entries (per no-defer principle v0.33; not "defers")

| W# | Concrete decision currently un-makeable | Awaiting external signal | Resolution mechanism |
|---|---|---|---|
| W1 | Layer 3 mechanism choice (Pydantic subclass / declared extra_fields / metadata dict) | First-bind real workflow performance + per-deployment customization needs from real consulting deployment | When signal arrives, evaluate mechanism trade-offs against real deployment patterns; lock in #9 Bundle B implementation phase. (Already a valid watch-list per existing entity-md-spec defer.) |
| W2 | Cross-shape specialist portability semantics (specialist authored for practitioner shape used in autonomous-business shape) | First concrete cross-shape user (community member or consulting client) | When signal arrives, evaluate per-shape contract gaps; revise specialist Pydantic if needed. |
| W3 | Hot-swap shape on running workspace | First concrete need (real deployment requesting shape change without rebuild) | When signal arrives, evaluate migration mechanism cost vs frequency. |
| W4 | Concrete long-running runtime substrate adapter implementation | First autonomous-business shape extension built (community-driven) | When signal arrives, implement adapter; Time Protocol abstraction (in #25 scope) provides Protocol surface to fill. |
| W5 | Marketplace mechanics (auth / pricing / governance / deprecation) | Marketplace v3 launch milestone | Lock at v3 design phase; constraints already locked Sub-DR B. |

All chronological-valid per no-defer principle (each names specific external signal awaited, not generic "we haven't done it yet" or "premature"). All have resolution mechanisms.

## Files touched (this DR persistence + cascade)

- `docs/decisions/entity-md-scope-model-restructure.md` (NEW — this file)
- `docs/conventions/entity-md-spec.md` (rewrite of §3 + §3.1 + §3.2 + §4 + §6)
- `ARCHITECTURE.md` (rewrite of "Layering convention: scope orthogonality" → "Three-category scope model"; reference card row update; version log v0.33 → v0.34 entry)
- `ROADMAP.md` (#25 scope rewrite to incorporate three-category foundation + actual schema designs)
- (Future cascade in subsequent commits): AuditEvent schema fields; Pydantic implementation #9; filesystem migrations #11.

## Pattern-vs-instance check

| Concern | Verdict |
|---|---|
| Three-category scope structure | ✅ Pattern-level — applies to any deployment using entity-md |
| Layer A / Owner B / Framework C category names | ✅ Pattern-level — semantic categories |
| Specific scope values within categories (universal/domain/state etc.) | ✅ Pattern-level — universal architectural axes |
| Definition vs instance binding pattern | ✅ Pattern-level — applies to any framework primitive |
| Specialist dual-nature | ✅ Pattern-level — applies to any deployment with specialists |
| Specific framework primitive kinds (shape/substrate/protocol) | ✅ Pattern-level — framework architecture defines the kinds |
| Specific shape values (practitioner/autonomous-business/...) | ⚠ Instance-level — concrete shape choices per deployment / community contribution |
| Specific specialist instances (planning-document-work) | ⚠ Instance-level — PBS-Schulz pioneer content |

All architectural decisions properly leveled. Concrete content stays instance-level; pattern-level shape + structure stays at architecture level.

## Revisit triggers (preliminary-lock principle applies; this DR is preliminary-locked)

Per Preliminary-lock principle (v0.33): this DR is preliminary-locked; revisable when VISION ideal design demands. Specific revision triggers:

- **First-bind real deployment** surfaces ergonomic issues with three-category Layer 1 frontmatter (e.g., users find the 6 category fields cumbersome) — revisit field structure
- **Layer 3 mechanism locked in #9** changes how per-instance customization composes with three-category structure — revisit binding semantics
- **Cross-shape specialist portability becomes real concern** (W2 signal arrives) — revisit specialist Pydantic
- **New framework primitive kind emerges** beyond shape/substrate/protocol (e.g., a substrate-orthogonal "Capability" primitive) — extend Framework C kind enum
- **Real cross-org / federation deployment** surfaces multi-tenant scope issues — revisit Owner B semantics for federation
- **AI capability shift** changes what "framework primitive" means architecturally — revisit category model
- **VISION axis falsification signal** — anchor revision per VISION's own falsification criteria
