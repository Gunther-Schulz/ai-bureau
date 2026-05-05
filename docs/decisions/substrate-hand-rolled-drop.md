# Decision record: Substrate hand-rolled Implementation drop

## 1. Status

ACCEPTED 2026-05-05. First v1.x ARCH amendment to fire post-Phase-3.7 v1.x re-tag (per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE v1.x amendment cadence + `BACKLOG.md` Phase 3.7 v1.x amendment candidates section). Mechanical scope-narrowing within stable Pattern A topic; no architectural REVISION; preliminary-lock revision per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3.

## 2. Owner

Phase 3.7 v1.x ARCH amendment cadence; `HANDOFF.md` Note 65 captures execution detail.

## 3. Related

- Composes with `arch/substrate.md` (the LOCK being amended; §4 Per-implementation aspect Current instance set + §9 Cardinality + §17 Decision-design provenance archived-source amendment-note)
- Composes with `docs/decisions/substrate-arch-topic.md` (original Phase 3.4 LOCK preserved; this DR amends Implementation cardinality + set without superseding the topic)
- Composes with `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE thin-slice rationale (Phase 6.1 in-scope artifact "Mode 2 reference substrate impl: Claude Agent SDK only"; Phase 6.2 adds MS Agent Framework)
- Composes with `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3 (preliminary-lock revision discipline)
- Composes with `BACKLOG.md` Phase 3.7 v1.x amendment candidates + Phase 6.1 thin-slice scope + Phase 6.2 production scope
- Composes with `arch/specialist-skill.md` §2.2 per-substrate materialization examples + §14 W2 cross-substrate skill-portability watch-list
- Composes with `arch/scope-model.md` §2.1 Framework C member catalog substrate definitions list

## 4. Context

`HANDOFF.md` Note 64 chat-locked the thin-slice v1.0-runtime milestone approach + Phase 6.1/6.2 split + Phase 3.7 v1.x re-tag + base framework boundary discriminator (per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE persistence cascade). Hand-rolled production-grade Implementation is out of scope for the thin-slice (Phase 6.1 = Claude Agent SDK only) AND out of scope for v1.0-production (Phase 6.2 adds MS Agent Framework; hand-rolled deprecated entirely from the current Implementation set). Carrying a speculative third Implementation in `arch/substrate.md` §4 + §9 cardinality table while the milestone scope explicitly excludes it produces an inconsistency between locked architecture surface and locked milestone scope.

Preliminary-lock revision discipline applies (per `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §3): the Pattern A Implementation set is preliminary-locked + revisable when VISION-grounded thin-slice scope demands it; revising 3 → 2 cleaner than carrying speculative third Implementation. Pattern A ≥2 implementations discriminator (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE Pattern A row) preserved post-amendment (2 ≥ 2).

## 5. Decision

Drop the hand-rolled (Python + MCP + Pydantic) Implementation entry from the substrate Pattern A Implementation set. Current set narrows from {Claude Agent SDK, MS Agent Framework, hand-rolled} → {Claude Agent SDK, MS Agent Framework}. Cardinality narrows from 3 → 2 concrete Implementations. Pattern A ≥2 implementations discriminator preserved (2 ≥ 2).

Cascade applied:
- `arch/substrate.md` §4 Current instance set narrative (3 → 2 Implementations; Pattern A ≥2 discriminator preservation noted) + §4 substrate identity example list (drop `hand_rolled_tier1`) + §9 Cardinality + lifecycle table row "Implementations per Framework C catalog" (N → ≥2 with explicit Pattern A discriminator note) + §17 Decision-design provenance amendment-note (historical archived-source citation kept INTACT; follow-up paragraph added pointing to this DR + noting future re-introduction fires as separate v1.x amendment)
- `arch/specialist-skill.md` §2.2 skill-loading-via-substrate Surface §G integration paragraph (per-substrate materialization examples — drop `hand-rolled = per-impl-decision`) + §14 W2 watch-list (drop "or hand-rolled" from second substrate deployment options)
- `arch/scope-model.md` §2.1 Framework C member catalog substrate definitions list (drop "/ hand-rolled" from runtime contract Implementations list)

Future re-introduction of hand-rolled Implementation OR addition of any other Implementation distinct from Claude Agent SDK + MS AF fires as a separate v1.x amendment per evidence trigger (per `arch/substrate.md` §16 W2 "New substrate candidate emergence" generic resolution mechanism + composition with PydanticAI W5 candidate per `HANDOFF.md` Note 64 #8 if PydanticAI maturity reaches ≥5 of 7 Surface categories).

## 6. Sharpening provenance

Chat-locked at `HANDOFF.md` Note 64 #4 (substantive decisions persisted): "Hand-rolled substrate Implementation drop (corollary of thin-slice) — Implementation set 3 → 2 (Claude Agent SDK + MS Agent Framework only). Pattern A ≥2 implementations discriminator already satisfied. NOTE: cascade dispatch SEPARATE upcoming dispatch (not in scope of THIS persistence cascade); persistence cascade FOREWARNS the substrate amendment but doesn't apply it."

No Round 1 / Round 2 sharpening triggered for this amendment because:
- Decision is a mechanical scope-narrowing within already-validated Pattern A surface (substrate Phase 3.4 LOCK + greenfield-rederivation v2 cascade amendments already validated the Pattern A topic; this amendment narrows the Implementation set without architectural revision)
- Decision is a corollary of the thin-slice v1.0-runtime milestone approach which was itself the substantive decision (locked at chat Note 64; persisted in `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE)
- No architectural REVISIONS surfaced; no manufactured-criticism rejections applied
- Profile-cluster validation N/A — mechanical drop within already-validated Pattern A surface; substrate Phase 3.4 LOCK already validated 4/4 profile clusters PASS with cited content per `docs/decisions/substrate-arch-topic.md` Sharpening provenance section
- GLOSSARY back-check verdict CLEAN — `glossary/substrate.md` body cross-archetype illustration mentions hand-rolled but as one of three named exemplars where future substrates may emerge; the drop does not surface a glossary-grade structural fact (Pattern A cardinality + cross-archetype illustration are different surfaces; cross-archetype illustration intentionally lists past + present + speculative-future exemplars per `MAINTENANCE.md` cascade discipline GLOSSARY back-check Trigger points)
- Cross-corpus sweep verifies clean residual state post-amendment (per `MAINTENANCE.md` cascade discipline cross-corpus sweep mandate at lock-time)

`decision-design-sharpening` skill NOT triggered per skill scope: skill scope is decisions needing disciplined sharpening BEFORE commit to file at decision-formation moment (per `plugin/skills/decision-design-sharpening/SKILL.md` "When this skill fires"); this amendment is a pre-locked corollary of the thin-slice approach with cardinality preservation, not a new architectural decision requiring sparring-mode challenge.

## 7. Composition with existing architecture

- **Pattern A 12+7 template-class FORMAL STABILITY UNAFFECTED** — template structure is per `MAINTENANCE.md` Layer 3 Pattern A / mechanism-class topic template; Implementation cardinality is independent of structural shape. 3 of 3 Pattern A instances complete with Phase 3.6 close (substrate anchor + adapter + quality-gate) survives this amendment without revision.
- **`arch/substrate.md` §4 Per-implementation aspect** — Current instance set narrative narrows; Pattern level (any agentic-runtime that can satisfy the Surface qualifies) unaffected; per-impl extension Protocols pattern unaffected (typed `ClaudeAgentSDKExtensions` + `MSAgentFrameworkExtensions` were the only two extension Protocols already; hand-rolled had no canonical extension Protocol surface).
- **`arch/substrate.md` §9 Cardinality + lifecycle** — table row narrows from N to ≥2 with explicit Pattern A ≥2 discriminator preservation note; §9 lifecycle ownership / mutability / cross-session persistence subsections unaffected.
- **`arch/substrate.md` §17 Decision-design provenance** — historical archived-source citation kept INTACT (faithful provenance to archived material per `MAINTENANCE.md` cascade discipline + Lens 5 v0.2.2 KEEP-class for load-bearing forward-references); follow-up amendment-note paragraph added pointing to this DR.
- **`arch/specialist-skill.md` §2.2 + §14 W2** — per-substrate materialization examples + cross-substrate skill-portability watch-list narrowed; cross-specialist composition rules + skill atomic structure + Pattern B nesting partner relationships unaffected.
- **`arch/scope-model.md` §2.1 Framework C member catalog** — substrate definitions list narrowed; Framework C scope-classification + workspace integration + Owner B + Layer A surfaces unaffected.
- **Phase 6.1 reference impl scope** — Mode 2 reference substrate impl narrowed to Claude Agent SDK only per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE Phase 6.1 in-scope artifacts; this DR makes the architectural surface consistent with that milestone scope.
- **Phase 6.2 production scope** — adds MS Agent Framework substrate impl per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE Phase 6.2 in-scope artifacts; hand-rolled remains out of scope for both 6.1 and 6.2.
- **W5 watch-list candidate composition** — PydanticAI Round 1 verdict per `HANDOFF.md` Note 64 #8 ("NOT a substrate per locked Surface; W5 watch-list candidate") parked as separate future v1.x amendment; if W5 fires, may add Implementation back per evidence trigger; orthogonal axis to this amendment.

## 8. Constraints flowing to downstream commitments

- **Phase 6.1 reference impl** = Claude Agent SDK only (Mode 2 reference impl per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE; this DR confirms the substrate Implementation surface narrows to match)
- **Phase 6.2 production impls** = adds MS Agent Framework substrate impl (matches the post-amendment Implementation set {Claude Agent SDK, MS AF})
- **Future v1.x Implementation additions** per evidence trigger only — PydanticAI W5 (per `HANDOFF.md` Note 64 #8) OR any other surfaced-need fires as separate v1.x amendment per `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE v1.x amendment cadence + `arch/substrate.md` §16 W2 generic resolution mechanism
- **`arch/substrate.md` §16 watch-list** unchanged at this amendment (W2 "New substrate candidate emergence" generic entry already covers the cardinality re-introduction signal class; W5 PydanticAI parked as separate future v1.x amendment per `HANDOFF.md` Note 64 #8)
- **No Pydantic schema impact at Phase 6** — substrate id enum may narrow at Phase 6 spec from 3 candidate values to 2 concrete values; `SubstrateConfig` Pydantic shape per `arch/substrate.md` §18 phase routing unaffected
- **No `glossary/substrate.md` content change** — cross-archetype illustration lists past + present + speculative-future exemplars; intentionally retains hand-rolled as one named exemplar where future substrates may emerge alongside other future substrates (no glossary-grade structural fact surfaced; per Lens 1 GLOSSARY back-check verdict CLEAN)

## 9. Files touched

- `arch/substrate.md` — §4 Per-implementation aspect (narrative + identity example list) + §9 Cardinality + lifecycle table + §12 Per-impl transport support varies (hand-rolled bullet drop) + §17 Decision-design provenance amendment-note + §18 Phase routing concrete-impls row (HandRolledSubstrate strike)
- `arch/specialist-skill.md` — §2.2 skill-loading-via-substrate Surface §G integration paragraph + §14 W2 watch-list
- `arch/scope-model.md` — §2.1 Framework C member catalog substrate definitions list
- `docs/decisions/substrate-hand-rolled-drop.md` (this file; NEW)

## 10. Revisit triggers

This DR should be revisited if:
- **PydanticAI maturity** reaches ≥5 of 7 Surface categories per `arch/substrate.md` §16 W5 candidate per `HANDOFF.md` Note 64 #8 — fires as separate v1.x amendment to add PydanticAI as third Implementation (orthogonal to this amendment; this DR's Implementation set is bounded by `{Claude Agent SDK, MS AF}` until W5 OR another evidence trigger fires)
- **Future deployment-instance evidence** of typed-agent substrate need distinct from Claude Agent SDK + MS AF surface — fires as separate v1.x amendment per `arch/substrate.md` §16 W2 generic resolution mechanism
- **Hand-rolled re-introduction evidence** — if concrete deployment-instance evidence surfaces a need for the minimal Tier 1 fallback baseline, fires as separate v1.x amendment per `arch/substrate.md` §16 W2 (W2's resolution mechanism explicitly covers re-evaluating boundary criteria + adding as new Implementation OR documenting why not)
- **Phase 6.1 thin-slice surfaces architectural friction** with the 2-Implementation cardinality (e.g., Pattern A discriminator stress at structural validation OR cross-substrate skill-portability friction per `arch/specialist-skill.md` W2) — fires as v1.x amendment to revise Implementation set semantics
- **Pattern A 12+7 topic-template-class FORMAL STABILITY** test under post-amendment substrate `arch/substrate.md` should remain stable (template structure is independent of Implementation cardinality); if template stability fails post-amendment, fires as architectural REVISION at C3 phase-boundary audit per `disciplines/09-coherence-audit-cadence.md` cadence
