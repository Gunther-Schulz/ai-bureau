---
title: Sparring
topic-cluster: mechanism-class topics (sparring + audit; per-shape policy variation; not Pattern A)
status: locked
---

# Sparring

> **Layer 3 ARCH topic**. Architectural-conceptual articulation of the Sparring **mechanism class** with per-shape policy variation. Mode 4 development-time documentation per `ARCHITECTURE.md` §6 Logic placement modes — NOT production-runtime; Phase 6 spec lands the Pydantic schemas for the architecturally-encoded sub-mechanisms (Mode 3).

## 1. Topic scope

The **Sparring mechanism class** is the runtime mechanism set realizing axis-2 (sparring) as a load-bearing pillar in practitioner-shape workspaces. Per locked GLOSSARY `sparring (axis 2)` entry: sparring is DERIVED axis-2 success mode; this mechanism class collects the 8 sparring sub-mechanisms (each a `mechanism` primitive — atomic interface contract) under a single architectural-conceptual home, parameterized by per-shape policy.

**Single Surface** (each sub-mechanism is its own atomic mechanism contract; the 8 sub-mechanisms together constitute the class). The class does NOT have multiple alternative implementations realizing one whole-class Surface differently — that's the discriminator distinguishing it from Pattern A protocols (substrate / adapter / quality-gate).

**Cardinality**: 8 sub-mechanism contracts; shape policy declares which sub-mechanisms active + how enforced + threshold values. Per-shape variation is POLICY-level (when sub-mechanisms fire / which active / how-enforced), NOT IMPL-level (no alternative whole-class architectures swap in/out per workspace).

**Cross-axis dependency**: sparring fires AT claim granularity; sparring events ARE the production-phase substrate for `engaged authorship` two-phase composite (per locked GLOSSARY engaged-authorship entry); axis-2 → axis-3 dependency.

**Composition with framework**:
- Each sub-mechanism is a `mechanism` (framework-level atomic interface contract); the Sparring class is the architectural-conceptual aggregation of the 8
- Per-shape policy bundle declares per-sub-mechanism activation + thresholds + retry budget
- Sub-mechanism execution lives within skill execution (skill-side); not a separately-bound runtime instance
- Architecturally-encoded sub-mechanisms (1-4) leverage substrate Surface §D (structured output validation) for schema enforcement
- Sparring events emitted via MCP audit gate (skill-side; per audit mechanism class emission discipline)

**Phase routing**: Pydantic schemas for architecturally-encoded sub-mechanisms 1-4 → Phase 6 spec (Mode 3). Per-sub-mechanism Implementation work (orchestrator wiring; heuristic-detection thresholds; bypass-with-reason UX) → Phase 6.

## 2. Sparring sub-mechanism Surfaces (architectural-level capability categories)

Each sub-mechanism declares its own atomic Surface (the mechanism's interface contract). **Articulated here at architectural-conceptual level** — Pydantic schemas for architecturally-encoded sub-mechanisms 1-4 land at Phase 6 spec.

Eight sub-mechanism capability categories constitute the Sparring mechanism class, split into architecturally-encoded (4) + behaviorally-enforced (4) per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator.

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

Per-sub-mechanism Surface contract articulated here (Mode 4 conceptual) + Phase 6 spec (Mode 3 Pydantic schemas for architecturally-encoded sub-mechanisms 1-4 + companion docs). Mode 1 production-runtime AI (skills + specialists) reads sparring-policy mandates from active shape policy bundle at workspace boot.

## 3. Sub-mechanism boundary criteria

Per Pattern A / mechanism-class template `MAINTENANCE.md:267`: §3 common-surface boundary criteria is conventionally N/A for mechanism-class topics (single-layer Surface convention — sub-mechanisms ARE the Surface; no multi-class boundary criteria). However, sparring as mechanism class still warrants a sub-mechanism-vs-non-sub-mechanism boundary rule (decision-criterion table below) plus a layer-of-introduction discriminator (framework-baseline-vs-shape-extension partition — co-located here for adapter-uniformity per `disciplines/02-apply-principle-uniformly.md`; full per-realization detail at §4).

Decision rule for "in Sparring mechanism class" vs "out":

| Decision criterion | Verdict | Examples |
|---|---|---|
| Axis-2 sparring sub-mechanism applying across all sparring-mode skill outputs | In class (per-sub-mechanism category) | counter-argument; confidence calibration; visible reasoning; selective friction; anti-sycophancy; asymmetric knowledge respect; commit-to-recommendations; what's-missing |
| Per-claim attestation (axis-3 success mode) | Out (composes with `engaged authorship` per axis-3 → `arch/claim-defensibility.md` Phase 3.5) |
| Cross-claim coordination (multiple claims in same workflow_instance) | Out (subsumed into substrate hooks + event-bus per `arch/substrate.md`; per-shape policy configures coordination shape — call-shaped vs event-shaped) |
| Authority decisions (who can sign / approve) | Out (authority-binding mechanism is its own framework primitive per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table; per-shape policy declares trust model — practitioner-judgment / budget-policy / individual) |
| Per-shape policy declaration mechanics (which sub-mechanisms active) | Out (composes with `shape` GLOSSARY entry; declared in shape policy bundles) |

Architectural-encoded vs behaviorally-enforced classification per sub-mechanism uses `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 discriminator: gate-dispatched-on-every-write → structural; AI-applies-at-judgment-time → prose convention with audit.

**Layer-of-introduction note**: sub-mechanisms further partition into framework-baseline vs shape-extension along a layer-of-introduction discriminator (parallel to adapter §3 framework-baseline-vs-shape-extension class partition — uniformly applied per `disciplines/02-apply-principle-uniformly.md`). Full discriminator + CONFIRMS-LOCKED 8 current sub-mechanisms as framework-baseline + shape-extension forward-pointer at §4 below.

## 4. Per-sub-mechanism realization aspect

Each sub-mechanism contract is realized at the framework-mechanism layer + parameterized by per-shape policy. Unlike Pattern A protocols (substrate / adapter / quality-gate), there is **no whole-class implementation that admits alternative architectures**; sub-mechanism realization is per-sub-mechanism, not per-class.

### Per-sub-mechanism realization

Architecturally-encoded sub-mechanisms 1-4 are realized via substrate Surface §D (structured output validation; Pydantic schemas land at Phase 6). Behaviorally-enforced sub-mechanisms 5-8 are realized via prose-convention skill body language + AI-applies-at-judgment-time + heuristic-detection emission events.

Per-sub-mechanism realization variation (e.g., LLM-prompted vs rule-based vs retrieval-based for a given sub-mechanism) is per-sub-mechanism implementation detail, not class-level pluggability — that's the discriminator distinguishing this class from Pattern A protocols.

### Current default realizations (CIRCA 2026)

- **Architecturally-encoded sub-mechanisms 1-4**: leverage substrate Surface §D (structured output validation) for schema enforcement; orchestrator wiring per archived sparring-output-v1.md pattern (validate → retry-on-fail → escalate-after-N-retries → bypass-with-reason).
- **Behaviorally-enforced sub-mechanisms 5-8**: AI applies at judgment time via skill body prose conventions + heuristic-detection emits events when sub-mechanism violations cluster.

### Framework-baseline sub-mechanism vs shape-extension sub-mechanism

Sub-mechanisms partition into two categories along a layer-of-introduction discriminator (uniformly applied with adapter §3 framework-baseline-vs-shape-extension class partition per `disciplines/02-apply-principle-uniformly.md`). The discriminator determines WHERE the sub-mechanism lives + WHEN it activates + WHO defines it; per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 pattern-vs-instance (framework primitives stay shape-neutral; shape policy bundle handles per-shape variation).

| Category | Defined by | Applicability | Activation | Lifecycle |
|---|---|---|---|---|
| **Framework-baseline sub-mechanism** | Framework-mechanism layer (this ARCH topic + Phase 6 per-sub-mechanism Pydantic schemas for architecturally-encoded sub-mechanisms 1-4) | ALL framework-supported shape archetypes (practitioner / autonomous-business / personal-OS / federation / hybrid) — universal applicability per Ming research foundation (sparring is the productive mode regardless of shape; only the activation matrix + thresholds vary per shape) | Available in any workspace regardless of selected shape; per-shape activation matrix (per §5) modulates which sub-mechanisms active + threshold values + retry budget but does NOT redefine the sub-mechanism semantically | Lives in framework distribution; new framework-baseline sub-mechanisms added via framework-mechanism-layer DR amendment per cascade discipline |
| **Shape-extension sub-mechanism** | Shape policy bundle (additive layer per shape; lives in shape's distributable artifacts) | Specific shape's archetype only (per shape that introduces it; NOT framework-mechanism modification — additive layer per shape) | Activated only in workspaces using the introducing shape (or shapes inheriting from it); per-shape policy declares activation + thresholds for the shape-extension sub-mechanism alongside framework-baseline sub-mechanisms | Lives in shape policy bundle distribution; new shape-extension sub-mechanisms added via shape-policy-bundle DR per shape definer (L2 profile) |

**Discriminator test** (when first instance of a candidate sub-mechanism surfaces):

1. **Universal-applicability test**: Would this sub-mechanism apply across ALL framework-supported shape archetypes — testable via hypothetical legal-practice / research-paper / engineering-doc workspaces (per `glossary/authority-binding.md` boundary-test pattern)? Per Ming research foundation: does the axis-2 productive-mode role apply regardless of shape? If yes → framework-baseline candidate.
2. **Shape-specific test**: Does this sub-mechanism only make sense within a specific shape's archetype scope (introduced by that shape's policy bundle as additional sub-mechanism beyond framework-baseline)? If yes → shape-extension candidate.
3. **Semantic-redefinition test**: Does the sub-mechanism require redefining a framework-baseline sub-mechanism's semantics for a specific shape (vs additive new sub-mechanism)? If yes → NOT shape-extension; that's framework-mechanism-layer revision per cascade discipline.

**Current 8 sub-mechanisms — CONFIRMED FRAMEWORK-BASELINE**:

| Sub-mechanism | Framework-baseline confirmation |
|---|---|
| **A. Counter-argument as first-class output** | Universal-applicability: hypothetical legal-practice (counter-argument on opposing-counsel-position), research-paper (counter-argument on methodology critique), engineering-doc (counter-argument on alternative-design-tradeoff) workspaces all need explicit counter-argument production. Per Ming research foundation: counter-argument is the productive-mode discriminator regardless of domain. |
| **B. Confidence calibration** | Universal-applicability: hypothetical legal-practice (precedent-strength confidence), research-paper (effect-size confidence), engineering-doc (specification-correctness confidence) workspaces all need typed confidence + basis-of-confidence declaration. |
| **C. Visible reasoning** | Universal-applicability: chain-of-inference disclosure is shape-neutral — every accountability-bearing claim across all hypothetical workspaces needs reasoning visibility for axis-3 defensibility composition. |
| **D. Selective friction** | Universal-applicability: per-claim-ambiguity threshold-triggered friction applies across all hypothetical workspaces; threshold value is shape-policy-mandated parameter (per §5 activation matrix), but the sub-mechanism semantics are framework-baseline. |
| **E. Anti-sycophancy guard** | Universal-applicability: soften-without-evidence pattern detection applies across all hypothetical workspaces — Ming research's validator-mode failure mode is shape-neutral. |
| **F. Asymmetric knowledge respect** | Universal-applicability: declarative "I'm drawing on X; local context Y might change this" applies across all hypothetical workspaces — practitioner local-context awareness is shape-neutral. |
| **G. Commit-to-recommendations** | Universal-applicability: context-dependent commit-vs-question discrimination applies across all hypothetical workspaces — per-claim recommendation production is shape-neutral. |
| **H. What's-missing checkpoint** | Universal-applicability: layered review checkpoint applies across all hypothetical workspaces — coverage-gap surfacing is shape-neutral. |

Per-shape activation matrix (per §5 + §14 cross-shape policy variation) modulates WHICH framework-baseline sub-mechanisms active in a given workspace + threshold values + retry budget; the activation matrix does NOT redefine sub-mechanism semantics — only the policy parameters per shape.

**Shape-extension sub-mechanism candidates** (forward-pointer):
- Future shape extensions may add per-domain sub-mechanisms — those land as **shape-extension sub-mechanisms** living in the introducing shape's distributable policy bundle, NOT in framework-mechanism-layer sparring distribution; framework-baseline 8-sub-mechanism enumeration unchanged by shape-extension additions
- Examples (illustrative; not yet locked): `precedent-citation-required` introduced by legal-practice shape policy bundle (per-claim precedent-citation requirement); `dataset-provenance-required` introduced by research-paper shape policy bundle (per-claim dataset-provenance requirement); `safety-case-traceability-required` introduced by engineering-doc shape policy bundle (per-claim safety-case-traceability requirement)
- Lifecycle: additive layer per shape; new shape-extension sub-mechanisms added via shape-policy-bundle DR per shape definer (L2 profile); per-shape activation matrix extends to cover framework-baseline + shape-extension sub-mechanisms uniformly
- Resolution: when first candidate sub-mechanism surfaces, apply discriminator test above to classify as framework-baseline (universal applicability per Ming research foundation → framework-mechanism-layer DR amendment) OR shape-extension (specific shape's policy bundle additive extension → shape-policy-bundle DR)

### Per-shape policy declares

Each per-shape policy bundle declares:
- **Sub-mechanism activation matrix** (which 8 sub-mechanisms enforced; per-shape variation)
- **Per-sub-mechanism schema enforcement** (architecturally-encoded sub-mechanisms; mandatory vs optional)
- **Threshold values** (selective-friction claim-ambiguity threshold; anti-sycophancy heuristic-detection threshold)
- **Retry-count + escalation** (orchestrator wiring; per-shape retry budget before bypass-with-reason path)
- **Failure mode** (fail-closed for practitioner-shape; fail-open with alert for autonomous-business; fail-open for personal-OS)
- **Error mapping** (validation failures → SparringValidationError categories per §11)

## 5. Per-shape policy mechanics

The Sparring mechanism class is parameterized by `shape` policy bundle (NOT workspace.md directly — practitioner-shape policy bundle declares which sparring sub-mechanisms active + which schema fields required + per-shape threshold values). Workspace inherits shape's sparring policy at boot.

### Cardinality

| Concern | Value | Mechanism |
|---|---|---|
| Sparring sub-mechanisms in the class | 8 | Fixed at framework-mechanism layer (4 architecturally-encoded + 4 behaviorally-enforced) |
| Sub-mechanisms active per workspace | 0-8 (per shape) | Shape policy declares activation matrix |
| Whole-class alternative implementations | N/A (not Pattern A) | Per-sub-mechanism realization variation only; no whole-class swap |

### Per-shape activation matrices

| Shape | Sub-mechanisms active | Architecturally-encoded enforcement | Failure escalation |
|---|---|---|---|
| **practitioner-shape** | All 8 (axis-2 critical for defensibility) | All 4 architectural categories MANDATORY | Fail-closed; ≥1 sparring-event per claim mandatory |
| **autonomous-business-shape** | Subset per business policy (typically 4-6) | Architectural sub-mechanisms per business risk | Fail-open with alert |
| **personal-OS-shape** | Subset per user preference (typically 1-3) | Architectural sub-mechanisms typically only counter-argument | Fail-open |

Validated at workspace boot:
- Active shape's sparring policy declares activation matrix
- Each active sub-mechanism has its framework-mechanism realization available
- Architecturally-encoded sub-mechanisms have schema declarations Pydantic-validated via substrate Surface §D

## 6. Mechanism-class structural reconciliation

Sparring as mechanism class with per-shape policy variation:

| Aspect | Layer | What it is |
|---|---|---|
| **Sub-mechanism Surfaces** (8) | mechanism (framework-level) | 8 atomic interface contracts; 4 architecturally-encoded + 4 behaviorally-enforced |
| **Per-sub-mechanism realizations** | mechanism realization | 1-4 via substrate Surface §D structured output validation; 5-8 via skill body prose convention + heuristic-detection emission |
| **Per-shape policy bundle** | shape (policy layer) | Activation matrix + thresholds + retry budget + failure mode declared in shape policy |
| **Skill-side execution** | runtime | Sub-mechanisms run within skill execution; not a separately-bound runtime instance |

### Sparring-coupling: skill-portability

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1: skill code targeting sub-mechanism Surface contracts is portable across realizations within shape; skill code reaching realization-internal heuristic-thresholds is realization-pinned. Per-sub-mechanism Pydantic schemas (architecturally-encoded sub-mechanisms 1-4) enforce contract-vs-realization boundary.

### Distinct from Pattern A protocols (substrate / adapter / quality-gate)

- substrate (Pattern A) = singular per workspace (1 impl; tier-aware; alternative architectural designs realize Surface differently — Claude Agent SDK / MS AF)
- adapter (Pattern A) = multi-instance per workspace (N adapters; per-class Surface variation; alternative impls per integration class — gmail / outlook / fastbill realize email-Surface differently)
- quality-gate (Pattern A) = singular per workspace (1 impl per shape; alternative architectural designs realize Surface differently — practitioner-shape-gate stateful procedure / autonomous-business-shape-gate programmatic threshold / personal-OS-shape-gate light reporting)
- **sparring = mechanism class** (8 sub-mechanism Surfaces; per-shape policy declares activation matrix + thresholds; NO whole-class alternative architectures — sub-mechanism realization variation only)
- **audit = mechanism class** (AuditEvent schema + audit-trail composition; per-shape granularity policy + substrate-mediated storage; NO whole-class alternative architectures — see `arch/audit.md`)

## 7. Composition with framework primitives

| Primitive | Composition |
|---|---|
| `framework` | Sparring is a mechanism class within the framework's mechanism layer |
| `mechanism` | Each sub-mechanism is its own `mechanism` (atomic interface contract); the Sparring class aggregates the 8 |
| `shape` | Shape policy declares per-sub-mechanism activation + thresholds + retry budget; load-bearing — sparring without shape policy has no policy direction |
| `workspace` | Workspace inherits shape's sparring policy at boot |
| `protocol (architectural)` | Sparring is **NOT** a Pattern A protocol — sub-mechanisms ARE the Surface; per-shape variation is POLICY-level, not IMPL-level. Distinct from substrate / adapter / quality-gate. |
| **`substrate`** | **Substrate Surface §B (hook registration) hosts sparring sub-mechanism execution hooks. Substrate Surface §D (structured output validation) load-bearing for architecturally-encoded sub-mechanisms 1-4 (Pydantic schema enforcement; auto-retry inherited). Substrate Surface §C (permission flow) NOT used by sparring (no authority decision; sparring is pre-output validation). Coordination concerns (cross-claim sparring consistency across same work-unit) subsumed into substrate hooks + event-bus per `docs/decisions/greenfield-rederivation-pause.md` Step 3.** |
| `claim` | Sparring fires AT claim granularity (per-claim counter-argument; per-claim confidence; per-claim selective friction) |
| `engaged authorship` | Sparring events ARE the production-phase substrate for engaged-authorship's two-phase composite (per-claim sparring participation observed via sparring-event emissions = production-phase engagement signal) |
| `defensibility` | Axis-2 → axis-3 dependency: sparring's production-phase engagement is one of three structural conditions defensibility tests |
| `quality-gate` (Phase 3.6) | Quality-gate (Pattern A protocol) consumes sparring-event emissions for axis-2 enforcement; per-shape policy declares quality-gate enforcement of sparring requirements |
| `event` | Sparring-event kinds first-class in audit-trail (per-sub-mechanism event-kind catalog; see §8) |
| `audit` (mechanism class) | Sparring sub-mechanisms emit sparring events via MCP audit gate (skill-side per audit mechanism class emission discipline; not substrate-internal direct emission — sparring runs within skill execution, not at substrate-architectural moments) |
| `answer-machine AI` / `oracle AI` / `validator AI` | Axis-2 failure modes (Ming research); sparring is the success mode these degrade FROM. Sparring may emit failure-mode-detected events when sub-mechanism violations cluster |
| `category collapse` | Cross-axis force; axis-2 manifestations are answer-machine / oracle / validator AI |
| `workflow` (Pattern B; optional overlay) | Sparring fires within workflow_instance phases AND ad-hoc work — workflow-orthogonal at framework level |
| Authority binding mechanism | Authority-binding mechanism is its own framework primitive (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table); per-shape policy declares trust model (practitioner-judgment / budget-policy / individual). Sparring is pre-output validation; no authority-binding decision involved. |

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
| Sub-mechanisms in the class | 8 (fixed at framework-mechanism layer) | 4 architecturally-encoded + 4 behaviorally-enforced |
| Sub-mechanisms active per workspace | 0-8 | Shape policy activation matrix |
| Sparring rounds per claim | ≥1 (practitioner-shape mandates ≥1) | Per-claim sparring fires at claim production moment |

### Lifecycle ownership

- **Per-sub-mechanism schema registration**: framework-runtime registers sub-mechanism Pydantic schemas via substrate Surface §D at workspace boot (architecturally-encoded sub-mechanisms 1-4)
- **Per-sub-mechanism execution**: skill runtime executes sub-mechanism contracts at skill output moments (skill-side; not separately-bound runtime instance)
- **Per-sub-mechanism state**: per-claim sparring history; heuristic-detection state for anti-sycophancy persists in skill execution context + audit-trail

### Mutability

- **Configuration immutable** across single workspace boot (per-shape policy activation matrix + thresholds + retry-count loaded at boot)
- **Runtime state** evolves during sparring rounds (per-claim sparring history; heuristic-detection state for anti-sycophancy)
- **Cross-session persistence**: confidence calibration state persists per claim across session pauses (per-claim sparring not session-bounded; same claim resumed in later session preserves prior confidence). Visible reasoning event-trail persists in audit-trail. Selective-friction history per session may be substrate-impl-specific.

## 10. Boot + shutdown phase ordering

Boot + shutdown phase ordering — **N/A**: sparring sub-mechanisms run within skill execution lifecycle (no separate sparring-impl boot/shutdown phases). Sub-mechanism schema registration happens within substrate boot per substrate topic §10. Lifecycle inheres in §9 cardinality + lifecycle.

## 11. Sparring error categories (architectural-level)

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

## 12. Transport variation

Transport variation — **N/A**: sparring does not have a multi-transport surface. Sub-mechanism execution is skill-side; no transport-tier mapping at architectural level.

## 13. Deployment-tier awareness

Deployment-tier awareness — **N/A**: sparring sub-mechanisms are tier-uniform; no per-tier behavior at architectural level. Tier-driven variation lives at substrate-impl + per-shape policy level (per `arch/substrate.md` §13).

## 14. Cross-shape policy variation

Sparring's behavior is shape-policy-mediated. Activation matrix table in §5 documents per-shape variation; this section enumerates per-shape policy detail.

**Practitioner-shape sparring profile**:
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

## 15. Pre-implementation operational concerns (Phase 6 forward reference)

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

## 16. Watch-list

| W# | Item | Awaited signal | Resolution mechanism |
|---|---|---|---|
| W1 | Behavioral → structural promotion of sub-mechanisms 5-8 | Operational evidence (drift patterns; user-frustration signals) accumulating across deployments | Re-evaluate per-sub-mechanism architectural-encoded vs behaviorally-enforced classification; promote to Surface category if structural enforcement becomes viable |
| W2 | Anti-sycophancy false-positive friction-budget | First production deployment surfaces friction patterns | Tune heuristic threshold per impl; potential per-shape override mechanism |
| W3 | Cross-shape sub-mechanism activation matrix expansion | Second-shape productization (autonomous-business / personal-OS deployments) | Validate activation matrix against second-shape reality; potential refinement of architecturally-encoded vs behaviorally-enforced classification per shape |
| W4 | Candidate **shape-extension sub-mechanism** (additive per shape policy bundle; NOT framework-baseline modification) — e.g., `precedent-citation-required` (legal-practice shape), `dataset-provenance-required` (research-paper shape), `safety-case-traceability-required` (engineering-doc shape) | Specific shape's policy bundle introduces domain-specific axis-2 sub-mechanism with concrete pattern | Apply §3 layer-of-introduction note + §4 framework-baseline-vs-shape-extension discriminator test (universal-applicability across hypothetical legal-practice / research-paper / engineering-doc workspaces per Ming research foundation? → framework-baseline via framework-mechanism-layer DR amendment; introduced by specific shape's policy bundle as additive layer? → shape-extension via shape-policy-bundle DR per L2 shape-definer profile). Lock as shape-extension sub-mechanism per §3/§4 discriminator; preserve framework-baseline 8-sub-mechanism enumeration unchanged (extension lives in shape policy bundle distribution; per-shape activation matrix extends uniformly to cover framework-baseline + shape-extension sub-mechanisms) |

## 17. Decision-design provenance

This topic articulates the Sparring mechanism class per locked GLOSSARY `sparring (axis 2)` entry. Source materials:

- `archive/docs/decisions/sparring-output-v1.md` — structural promotion of 3-of-7 axis-2 mechanisms to schema-validated output (counter-argument / confidence / visible reasoning); 4 stayed behavioral
- VISION.md axis 2 framing (sparring partner, not answer machine; load-bearing runtime mechanism in practitioner-shape)
- VISION.md "Vivienne Ming — sparring as the productive mode" foundation (only sparring outperforms human-alone or AI-alone; oracle/validator-mode collapse)

Mechanism-class classification (vs Pattern A protocol) is anchored at `docs/decisions/greenfield-rederivation-pause.md` Step 3. Cross-validated by GLOSSARY `sparring (axis 2)` entry tags (Class **DERIVED** + Layer **cross-cutting** — NOT multi-aspect Pattern A primitive).

Per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2: per-sub-mechanism architectural classification stays shape-neutral / archetype-neutral / pioneer-neutral. PBS-Schulz pioneer reality (per L5a line 128 sparring as load-bearing runtime mechanism) grounds the practitioner-shape activation matrix without leaking pioneer specifics into sub-mechanism Surfaces.

## 18. Phase routing

| Concern | Phase | Notes |
|---|---|---|
| Architectural shape (this topic) | 3.4 | LOCKED |
| Pydantic Protocol contract per Surface | 6 | Mode 3 spec; per-sub-mechanism schemas (architecturally-encoded sub-mechanisms 1-4) |
| Concrete Sparring Protocol Implementation | 6 | Default impl wiring with substrate Surface §D + §B |
| Pre-implementation operational concerns | 6 | Pre-implementation sharpening at Phase 6 implementation-start |
| Per-shape activation matrix concrete declarations | 6 | Per-shape policy bundle declarations (practitioner-shape primary; second-shape per W3 watch-list) |
| Quality-gate consumption of sparring events | 3.6 | Quality-gate ARCH topic; consumes sparring-event emissions for axis-2 enforcement |
| Behavioral → structural promotion (W1) | TBD per signal | Operational evidence triggers re-evaluation |

## 19. Cross-references

- **GLOSSARY**: `sparring (axis 2)` (canonical entry); `mechanism`, `Framework C scope`, `Owner B scope`, `protocol (architectural)`, `substrate`, `claim`, `engaged authorship`, `defensibility`, `quality-gate`, `event`, `audit`, `answer-machine AI`, `oracle AI`, `validator AI`, `category collapse`, `workflow`, `work-unit`, `shape`
- **Disciplines**: `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §1 (architecturally-encoded vs behaviorally-enforced discriminator); `DISCIPLINES.md` Discipline 3 (pre-decision-sharpening; Round 1 + Round 2 layered coverage)
- **Profiles validated**: `G-composability-gate.md` (line 157 cross-shape consumption); `L5a-planner-pbs-schulz.md` (line 128 sparring as load-bearing runtime mechanism; line 67 hybrid moments — sparring during drafting + rubber-stamp risk during send); `L1-specialist-creator.md` (specialist DEFINITION can bundle skill outputs satisfying sparring schemas); `L8-auditor-reviewer-posthoc.md` (line 29 audit-trail integrity for sparring events surviving deployment migrations)
- **ARCH topics composing with sparring**: `arch/substrate.md` (Surface §B hook registration + §D structured output validation; load-bearing for architecturally-encoded sub-mechanisms; subsumes prior coordination Pattern A topic per `docs/decisions/greenfield-rederivation-pause.md` Step 3); `arch/audit.md` (sparring-event emission; mechanism class peer to sparring); `arch/quality-gate.md` (Phase 3.6; Pattern A protocol consuming sparring events for axis-2 enforcement); `arch/claim-defensibility.md` (Phase 3.5; sparring-event-trail as axis-2 → axis-3 dependency); `arch/specialist-skill.md` (Phase 3.5 primitive-cluster; sparring sub-mechanisms invoked from skills within specialists — skills with declared output schemas compose with substrate Surface §D structured output validation per `arch/specialist-skill.md` §2.2 skill atomic structure; per-shape activation matrix per §5 declares which sparring sub-mechanisms apply per skill firing); `arch/practitioner.md` (Phase 3.5 second primitive-cluster; practitioner is engagement subject of sparring per axis-2 cross-axis composition per `arch/practitioner.md` §4; sparring engagement events `actor_kind: ai_runtime` AI sparring-partner compose with practitioner-record per per-shape activation matrix per §14; production-phase substrate for engaged-authorship per `glossary/engaged-authorship.md`); `arch/workflow-work-unit.md` (Phase 3.5 third primitive-cluster; sparring sub-mechanisms accessed by skills DURING workflow_instance phase progression AND ad-hoc work-unit progression; orthogonal to workflow primitive engagement per per-shape activation matrix — sparring fires regardless of workflow_instance presence per `arch/workflow-work-unit.md` §4 composition with sparring). Cancelled: `arch/coordination.md` + `arch/trust.md` + `arch/time.md` (subsumed per `docs/decisions/greenfield-rederivation-pause.md` Step 3).
- **Phase 6 spec target**: `docs/specs/sparring.md` (Pydantic Protocol + per-sub-mechanism schemas + per-impl spec + per-shape activation matrices)
- **Archived sources**: `archive/docs/decisions/sparring-output-v1.md`
