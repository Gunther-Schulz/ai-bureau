---
title: Sparring
topic-cluster: Pattern A protocol topics (#3 of 8)
status: drafted (Phase 3.4 Round 2; locked)
---

# Sparring

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the Sparring Protocol (Pattern A). Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the Pydantic Protocol contract + per-sub-mechanism schema (Mode 3).

## 1. Topic scope

The **Sparring Protocol** is the runtime mechanism realizing axis-2 (sparring) as a load-bearing pillar in practitioner-shape workspaces. Per locked GLOSSARY `sparring (axis 2)` entry: sparring is DERIVED axis-2 success mode; the Sparring Protocol (Pattern A) is the framework primitive supporting that mode + 8 sparring sub-mechanisms (each a `mechanism` primitive — atomic interface contract).

**Single-layer Surface** (substrate-style; NOT adapter-style two-layer). 8 sub-mechanisms compose within unified axis-2 concern, not heterogeneous integration classes.

**Cardinality**: 1 Sparring Protocol Implementation per workspace; shape policy declares which sub-mechanisms active + how enforced. Distinct from adapter (multi-instance) and substrate (singular forever) — per-shape variation IS the load-bearing variation.

**Cross-axis dependency**: sparring fires AT claim granularity; sparring events ARE the production-phase substrate for `engaged authorship` two-phase composite (per locked GLOSSARY engaged-authorship entry); axis-2 → axis-3 dependency.

**Composition with framework**:
- Pattern A protocol per `protocol (architectural)` GLOSSARY entry
- Sparring Protocol Surface IS a `mechanism` (framework-level interface contract)
- Implementations live at `Framework C scope` as distributable definitions
- Running instance bound to `Owner B scope` per workspace deployment
- Per-shape policy declares which sub-mechanisms active

**Phase routing**: Pydantic Protocol contract + per-sub-mechanism schema fields → Phase 6 spec (Mode 3). Per-sub-mechanism Implementation work → Phase 6.

## 2. Sparring Protocol Surface (architectural-level capability categories)

The Surface is the universal interface any Sparring Protocol Implementation must satisfy. **Articulated here at architectural-conceptual level** — not Pydantic Protocol typing (Phase 6 spec).

Eight sub-mechanism capability categories define the Surface, split into architecturally-encoded (4) + behaviorally-enforced (4) per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator.

### Architecturally-encoded sub-mechanisms (4; gate-dispatched at every output)

#### A. Counter-argument as first-class output

Skill outputs in sparring-mode declare a required counter-argument category. Substrate Surface §D (structured output validation) enforces presence + min-content. Missing counter-argument fails validation; orchestrator retries.

#### B. Confidence calibration

Skill outputs declare a required confidence category (typed enum: high / medium / low) + accompanying basis-of-confidence. Schema-validated; missing field fails validation.

#### C. Visible reasoning

Skill outputs declare required reasoning category (chain of inference, not just verdict); min-content enforced.

#### D. Selective friction

Selective-friction fires per claim-ambiguity threshold. Threshold is shape-policy-mandated (gate-dispatched parameter), NOT impl-internal. Architectural commitment: per-shape threshold declaration in policy bundle; impl applies threshold uniformly.

### Behaviorally-enforced sub-mechanisms (4; AI applies at judgment time)

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: heuristic / declarative / context-dependent enforcement → prose convention with audit, NOT structural.

#### E. Anti-sycophancy guard

Heuristic detection compares current skill output against prior turn for soften-without-evidence pattern. Threshold + detection mechanism is impl-specific. Architectural-level: heuristic fires; emits event when detected.

#### F. Asymmetric knowledge respect

Declarative ("I'm drawing on X; local context Y might change this"). Too discretionary to schema-enforce; AI applies at judgment time.

#### G. Commit-to-recommendations

Context-dependent enforcement (sometimes a question IS the right move; sometimes a commit is). AI applies per claim.

#### H. What's missing checkpoint

Phase B layered review checkpoint; structural in skill body but content is judgment-applied.

### Logic placement mode

Surface contract articulated here (Mode 4 conceptual) + Phase 6 spec (Mode 3 Pydantic Protocol + per-sub-mechanism schema for architecturally-encoded categories + companion docs). Mode 1 production-runtime AI (skills + specialists) reads sparring-policy mandates from active shape policy bundle at workspace boot.

## 3. Common-surface boundary criteria

Decision rule for "in Sparring Protocol Surface" vs "out":

| Decision criterion | Verdict | Examples |
|---|---|---|
| Axis-2 sparring sub-mechanism applying across all sparring-mode skill outputs | Surface (per-sub-mechanism category) | counter-argument; confidence calibration; visible reasoning; selective friction; anti-sycophancy; asymmetric knowledge respect; commit-to-recommendations; what's-missing |
| Per-claim attestation (axis-3 success mode) | Out (composes with `engaged authorship` per axis-3 → `arch/claim-defensibility.md` Phase 3.5) |
| Cross-claim coordination (multiple claims in same workflow_instance) | Out (composes with `coordination` Pattern A — `arch/coordination.md`) |
| Authority decisions (who can sign / approve) | Out (composes with `trust` Pattern A — `arch/trust.md`) |
| Per-shape policy declaration mechanics (which sub-mechanisms active) | Out (composes with `shape` GLOSSARY entry; declared in shape policy bundles) |

Architectural-encoded vs behaviorally-enforced classification per sub-mechanism uses `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator: gate-dispatched-on-every-write → structural; AI-applies-at-judgment-time → prose convention with audit.

## 4. Per-implementation aspect

Implementations live at `Framework C scope` as distributable definitions. Each impl wraps native primitives of an underlying axis-2-validation runtime to satisfy the Surface contract.

### Pattern level

Any implementation satisfying the 8-sub-mechanism Surface (4 architecturally-encoded + 4 behaviorally-enforced via prose-convention skill body language) qualifies.

### Current Implementation set (CIRCA 2026)

- **Default Sparring Protocol Implementation** (single canonical impl currently): leverages substrate Surface §D (structured output validation) for architecturally-encoded sub-mechanisms; orchestrator wiring per archived sparring-output-v1.md pattern (validate → retry-on-fail → escalate-after-N-retries → bypass-with-reason).

Future Implementations may emerge per shape-specific axis-2 mechanics (e.g., legal-practice may add `precedent-citation-required` sub-mechanism via shape extension; not yet locked).

### Per-implementation declares

Each Implementation declares:
- **Sub-mechanism activation matrix** (which 8 sub-mechanisms enforced; per-shape variation)
- **Per-sub-mechanism schema** (architecturally-encoded sub-mechanisms; per-field validation)
- **Threshold declarations** (selective-friction claim-ambiguity threshold; anti-sycophancy heuristic-detection threshold per impl)
- **Retry-count + escalation** (orchestrator wiring; per-shape retry budget before bypass-with-reason path)
- **Error mapping** (validation failures → SparringValidationError categories per §10)

## 5. Selection mechanics

Sparring Protocol selection bound to `shape` (NOT to workspace.md directly — practitioner-shape policy bundle declares which sparring sub-mechanisms active + which schema fields required + per-shape threshold values). Workspace inherits shape's sparring policy.

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Sparring Protocol Implementations active per workspace | 1 | Shape policy declares; workspace inherits |
| Sub-mechanisms active per workspace | 0-8 (per shape) | Shape policy declares activation matrix |
| Implementations per Framework C catalog | M | Currently 1 default; future per shape-specific axis-2 variations |

### Per-shape activation matrices

| Shape | Sub-mechanisms active | Architecturally-encoded enforcement | Failure escalation |
|---|---|---|---|
| **practitioner-shape** | All 8 (axis-2 critical for defensibility) | All 4 architectural categories MANDATORY | Fail-closed; ≥1 sparring-event per claim mandatory |
| **autonomous-business-shape** | Subset per business policy (typically 4-6) | Architectural sub-mechanisms per business risk | Fail-open with alert |
| **personal-OS-shape** | Subset per user preference (typically 1-3) | Architectural sub-mechanisms typically only counter-argument | Fail-open |

Validated at workspace boot:
- Active shape's sparring policy declares activation matrix
- Each active sub-mechanism has Implementation declaration
- Architecturally-encoded sub-mechanisms have schema declarations Pydantic-validated

## 6. Tri-aspect reconciliation

Sparring Protocol as tri-aspect Pattern A primitive:

| Aspect | Layer | What it is |
|---|---|---|
| **Surface** (8 sub-mechanism categories) | mechanism (framework-level) | Atomic interface contract; 4 architecturally-encoded + 4 behaviorally-enforced |
| **Implementations** | Framework C scope | Distributable definitions wrapping native axis-2-validation primitives |
| **Running Instance** | Owner B scope | Bound to workspace deployment via shape policy |

### Sparring-coupling impossible-by-construction

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code targeting Sparring Protocol Surface is portable across Implementations within shape; skill code reaching Implementation-internal heuristic-thresholds is impl-pinned by construction.

### Distinct from adapter / substrate Pattern A

- substrate = singular per workspace (1 impl; tier-aware)
- adapter = multi-instance per workspace (N adapters; per-class Surface variation)
- **sparring = singular per workspace (1 impl); per-sub-mechanism activation per shape policy** (cardinality variation IS shape-policy-mandated, not impl-multiplicity)

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Sparring Protocol is one mechanism category within the framework |
| `mechanism` | Sparring Protocol Surface IS a mechanism (atomic interface contract); each sub-mechanism is its own `mechanism` (atomic) |
| `Framework C scope` | Sparring Protocol Implementations live there as distributable definitions |
| `shape` | Shape policy declares per-sub-mechanism activation + thresholds + retry budget; load-bearing — sparring without shape policy has no policy direction |
| `workspace` | Workspace inherits shape's sparring policy at boot |
| `Owner B scope` | Running Sparring Protocol Instance bound to workspace deployment |
| `protocol (architectural)` | Sparring Protocol is Pattern A protocol instance |
| **`substrate`** | **Substrate Surface §B (hook registration) hosts sparring impl hooks. Substrate Surface §D (structured output validation) load-bearing for architecturally-encoded sub-mechanisms 1-4 (Pydantic schema enforcement; auto-retry inherited). Substrate Surface §C (permission flow) NOT used by sparring (no authority decision; sparring is pre-output validation).** |
| `claim` | Sparring fires AT claim granularity (per-claim counter-argument; per-claim confidence; per-claim selective friction) |
| `engaged authorship` | Sparring events ARE the production-phase substrate for engaged-authorship's two-phase composite (per-claim sparring participation observed via sparring-event emissions = production-phase engagement signal) |
| `defensibility` | Axis-2 → axis-3 dependency: sparring's production-phase engagement is one of three structural conditions defensibility tests |
| `quality-gate` (Phase 3.6) | Quality-gate consumes sparring-event emissions for axis-2 enforcement; per-shape policy declares quality-gate enforcement of sparring requirements |
| `event` | Sparring-event kinds first-class in audit-trail (per-sub-mechanism event-kind catalog; see §8) |
| `audit` | Sparring impl emits sparring events via MCP audit gate (skill-side per adapter-style §8 emission discipline; not substrate-internal direct emission — sparring runs within skill execution, not at substrate-architectural moments) |
| `answer-machine AI` / `oracle AI` / `validator AI` | Axis-2 failure modes (Ming research); sparring is the success mode these degrade FROM. Sparring impl may emit failure-mode-detected events when sub-mechanism violations cluster |
| `category collapse` | Cross-axis force; axis-2 manifestations are answer-machine / oracle / validator AI |
| `workflow` (Pattern B; optional overlay) | Sparring fires within workflow_instance phases AND ad-hoc work — workflow-orthogonal at framework level |
| `coordination` (Phase 3.4 separate topic) | Cross-claim sparring coordination (e.g., consistency across claims in same work-unit) via coordination protocol; not sparring-internal |

## 8. Per-action audit emission (skill-side via MCP gate)

### Architectural commitment

Sparring sub-mechanisms run within skill execution (skill emits at sub-mechanism completion); not substrate-internal architectural events. Same emission discipline as adapter §8: skill-side via MCP audit gate (NOT substrate-internal direct emission). No circularity issue (sparring doesn't register MCP gate; substrate does).

### Per-sub-mechanism event-kind catalog (architectural-level)

Per-architecturally-encoded sub-mechanism (1-4):
- `counter_argument_produced` / `counter_argument_missing`
- `confidence_calibrated` / `confidence_missing`
- `visible_reasoning_provided` / `visible_reasoning_missing`
- `selective_friction_applied` / `selective_friction_skipped`

Per-behaviorally-enforced sub-mechanism (5-8):
- `anti_sycophancy_flag_raised` (heuristic detection fires)
- `asymmetric_knowledge_respected` (declarative; AI emits at completion)
- `recommendation_committed`
- `whats_missing_checked`

Cross-cutting (sparring-round level):
- `sparring_round_completed`
- `sparring_bypass_with_reason`
- `sparring_validation_retry`

### Axis-2 failure-mode detection events

Sparring impl may emit failure-mode-detected events when sub-mechanism violations cluster (per locked answer-machine AI / oracle AI / validator AI GLOSSARY entries):
- `answer_machine_detected`
- `oracle_mode_detected`
- `validator_mode_detected`

These events feed quality-gate's axis-2 enforcement (Phase 3.6).

### Bypass-with-reason audit semantics

When user explicitly bypasses failed sparring validation (after orchestrator retry-count exhausted), bypass event emitted with `bypass_reason: str`; bypass events first-class in audit-trail for L8 auditor reasoning-chain reconstruction (per L8 audit-trail integrity discipline).

## 9. Cardinality + lifecycle

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Sparring Protocol Implementations per workspace | 1 | Shape-policy-declared; workspace inherits |
| Sub-mechanisms active per workspace | 0-8 | Shape policy activation matrix |
| Sparring rounds per claim | ≥1 (practitioner-shape mandates ≥1) | Per-claim sparring fires at claim production moment |

### Lifecycle ownership

- **Creator**: framework-runtime instantiates Sparring Protocol Implementation per workspace boot (selecting impl per shape policy)
- **Owner**: workspace deployment runtime (Owner B scope)
- **Destroyer**: framework-runtime at workspace shutdown

### Mutability

- **Configuration immutable** across single sparring-impl boot (activation matrix + thresholds + retry-count loaded at boot)
- **Runtime state** evolves during sparring rounds (per-claim sparring history; heuristic-detection state for anti-sycophancy)
- **Cross-session persistence**: confidence calibration state persists per claim across session pauses (per-claim sparring not session-bounded; same claim resumed in later session preserves prior confidence). Visible reasoning event-trail persists in audit-trail. Selective-friction history per session may be substrate-impl-specific.

## 10. Sparring error categories (architectural-level)

Sparring operations may fail in named architectural categories. Each Implementation maps native errors to common categories.

| Category | Architectural meaning |
|---|---|
| `SparringValidationError` | Architecturally-encoded sub-mechanism missing or invalid (counter-argument missing; confidence not provided; reasoning insufficient; etc.) |
| `SparringSchemaError` | Output schema mismatch (impl-level) — Pydantic validation failed |
| `SparringRetryExhaustedError` | Orchestrator retry-count exceeded; bypass-with-reason path activated OR shape-policy-mandated fail-closed escalation |
| `SparringHeuristicError` | Heuristic detection failure (anti-sycophancy threshold corrupted; impl-internal) |
| `SparringPolicyError` | Shape policy declaration invalid (activation matrix references unknown sub-mechanism; threshold value out of range) |

Per-shape error semantics:
- **practitioner-shape**: fail-closed (defensibility-critical; sparring failures must surface to practitioner; ≥1 sparring-event per claim mandatory)
- **autonomous-business-shape**: fail-open with alert (continuity prioritized; alert on failure)
- **personal-OS-shape**: fail-open (lightweight; degradation acceptable)

Per-class Pydantic shape → Phase 6 spec.

## 11. Boot + shutdown phase ordering

### Boot sequence

1. Substrate boot completes (per `arch/substrate.md` §10)
2. Active shape policy loaded; sparring activation matrix + thresholds + retry-count parsed
3. Sparring Protocol Implementation instantiated per shape policy
4. Per-sub-mechanism schemas registered (architecturally-encoded sub-mechanisms 1-4 register Pydantic schemas via substrate Surface §D)
5. Sparring impl registers hooks via substrate Surface §B (PRE/POST skill output hooks)
6. Sparring impl `is_ready` becomes True
7. Skill execution can now produce sparring-mode outputs

### Shutdown sequence

1. Stop accepting new sparring rounds
2. Drain in-flight sparring rounds (allow current claim's sparring to complete)
3. Flush per-claim sparring state to audit-trail
4. Sparring impl shutdown returns
5. Substrate shutdown can proceed (per `arch/substrate.md` §10)

Flush-before-substrate-shutdown ordering preserves audit-trail integrity for sparring events; in-flight sparring rounds complete cleanly rather than leaving orphan partial-sparring state.

## 12. Cross-shape policy variation

Per `profiles/G-composability-gate.md` line 157: "Cross-shape consumption ... Shape's policy bundle determines if specialist activates fully or partially."

Sparring Protocol behavior is shape-policy-mediated. Activation matrix table in §5 documents per-shape variation.

**Practitioner-shape sparring profile** (anchor; per L5a line 128 "Sparring as load-bearing runtime mechanism"):
- All 8 sub-mechanisms active
- All 4 architecturally-encoded sub-mechanisms MANDATORY (fail-closed on missing)
- Selective-friction threshold = "substantive" (medium-or-higher claim ambiguity triggers)
- Anti-sycophancy heuristic fires per skill output
- ≥1 sparring-event per claim mandatory (axis-2 → axis-3 dependency)
- Retry budget: 3 invalid retries before bypass-with-reason escalation

**Autonomous-business-shape sparring profile**:
- Subset per business policy (typically counter-argument + confidence + visible reasoning + selective friction; remaining 4 optional)
- Architecturally-encoded enforcement per business-risk profile
- Fail-open with alert on validation failures
- Retry budget: configurable per business policy

**Personal-OS-shape sparring profile**:
- Subset per user preference (typically counter-argument; possibly confidence)
- Light enforcement (validation may be skipped per skill output)
- Fail-open

## 13. Sparring + workflow_instance composition

Sparring fires within workflow_instance phases AND ad-hoc work — workflow-orthogonal at framework level.

Per `profiles/L5a-planner-pbs-schulz.md` line 67 hybrid moments: sparring fires during drafting (codified workflow phase) AND ad-hoc research detours. Same sparring sub-mechanisms apply regardless of workflow_instance presence.

This validates `workflow` GLOSSARY entry's optional-overlay design + `work-unit` GLOSSARY entry's always-present container claim — sparring composes with always-present work-unit, NOT with optional workflow_instance.

## 14. Pre-implementation operational concerns (Phase 6 forward reference)

Operational/runtime concerns NOT locked at ARCH level — surfaced for Phase 6 pre-implementation sharpening:

- **Per-sub-mechanism Pydantic schema** (exact field shapes; min-length values; enum values for confidence)
- **Orchestrator wiring** for retry-on-invalid (per-shape retry budget; escalation-after-N-retries; bypass-with-reason event format)
- **Heuristic-detection threshold** (anti-sycophancy false-positive friction-budget; threshold tuning per impl)
- **Per-shape activation matrix** (concrete per-shape policy bundle declarations)
- **Cross-session sparring state persistence** (confidence calibration state schema; per-impl persistence semantics)
- **Failure-mode detection thresholds** (when do clustered sub-mechanism violations trigger answer_machine_detected vs oracle_mode_detected?)
- **Bypass-with-reason mechanics** (UX surface; user-visible escalation; audit-trail integration)
- **Selective-friction threshold semantics** (claim-ambiguity scoring; per-shape threshold values)

These belong to Phase 6 pre-implementation sharpening; ARCH topic explicitly does NOT lock these.

## 15. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| W1 | Behavioral → structural promotion of sub-mechanisms 5-8 | Operational evidence (drift patterns; user-frustration signals) accumulating across deployments | Re-evaluate per-sub-mechanism architectural-encoded vs behaviorally-enforced classification; promote to Surface category if structural enforcement becomes viable |
| W2 | Anti-sycophancy false-positive friction-budget | First production deployment surfaces friction patterns | Tune heuristic threshold per impl; potential per-shape override mechanism |
| W3 | Cross-shape sub-mechanism activation matrix expansion | Second-shape productization (autonomous-business / personal-OS deployments) | Validate activation matrix against second-shape reality; potential refinement of architecturally-encoded vs behaviorally-enforced classification per shape |
| W4 | Per-domain sparring sub-mechanism extension | Specific archetype (legal-practice / research-lab) surfaces domain-specific axis-2 mechanism (e.g., precedent-citation-required) | Add as per-shape-extension sub-mechanism; preserve framework Surface neutrality (extension lives in shape policy bundle) |

## 16. Decision-design provenance

This topic articulates the Sparring Protocol per locked GLOSSARY `sparring (axis 2)` entry. Source materials:

- `archive/docs/decisions/sparring-output-v1.md` — structural promotion of 3-of-7 axis-2 mechanisms to schema-validated output (counter-argument / confidence / visible reasoning); 4 stayed behavioral
- VISION.md axis 2 framing (sparring partner, not answer machine; load-bearing runtime mechanism in practitioner-shape)
- VISION.md "Vivienne Ming — sparring as the productive mode" foundation (only sparring outperforms human-alone or AI-alone; oracle/validator-mode collapse)

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: per-sub-mechanism architectural classification stays shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer reality (per L5a line 128 sparring as load-bearing runtime mechanism) grounds the practitioner-shape activation matrix without leaking pioneer specifics into Sparring Protocol Surface.

## 17. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.4 | LOCKED |
| Pydantic Protocol contract per Surface | 6 | Mode 3 spec; per-sub-mechanism schemas (architecturally-encoded sub-mechanisms 1-4) |
| Concrete Sparring Protocol Implementation | 6 | Default impl wiring with substrate Surface §D + §B |
| Pre-implementation operational concerns | 6 | Pre-implementation sharpening at Phase 6 implementation-start |
| Per-shape activation matrix concrete declarations | 6 | Per-shape policy bundle declarations (practitioner-shape primary; second-shape per W3 watch-list) |
| Quality-gate consumption of sparring events | 3.6 | Quality-gate ARCH topic; consumes sparring-event emissions for axis-2 enforcement |
| Behavioral → structural promotion (W1) | TBD per signal | Operational evidence triggers re-evaluation |

## 18. Cross-references

- **GLOSSARY**: `sparring (axis 2)` (canonical entry); `mechanism`, `Framework C scope`, `Owner B scope`, `protocol (architectural)`, `substrate`, `claim`, `engaged authorship`, `defensibility`, `quality-gate`, `event`, `audit`, `answer-machine AI`, `oracle AI`, `validator AI`, `category collapse`, `workflow`, `work-unit`, `shape`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (architecturally-encoded vs behaviorally-enforced discriminator); `DISCIPLINES.md` Discipline 3 (pre-decision-sharpening; Round 1 + Round 2 layered coverage)
- **Profiles validated**: `G-composability-gate.md` (line 157 cross-shape consumption); `L5a-planner-pbs-schulz.md` (line 128 sparring as load-bearing runtime mechanism; line 67 hybrid moments — sparring during drafting + rubber-stamp risk during send); `L1-specialist-creator.md` (specialist DEFINITION can bundle skill outputs satisfying sparring schemas); `L8-auditor-reviewer-posthoc.md` (line 29 audit-trail integrity for sparring events surviving deployment migrations)
- **ARCH topics composing with sparring**: `arch/substrate.md` (Surface §B hook registration + §D structured output validation; load-bearing for architecturally-encoded sub-mechanisms); `arch/audit.md` (sparring-event emission); `arch/coordination.md` (cross-claim sparring coordination); `arch/quality-gate.md` (Phase 3.6; consumes sparring events for axis-2 enforcement); `arch/claim-defensibility.md` (Phase 3.5; sparring-event-trail as axis-2 → axis-3 dependency)
- **Phase 6 spec target**: `docs/specs/sparring.md` (Pydantic Protocol + per-sub-mechanism schemas + per-impl spec + per-shape activation matrices)
- **Archived sources**: `archive/docs/decisions/sparring-output-v1.md`
