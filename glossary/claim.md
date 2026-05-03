---
entry: claim
class: PRIMITIVE
layer: cross-cutting
axis: axis-3
vision_usage: implicit
---

# claim

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
- [work-unit](work-unit.md) — claims compose into work-unit output; work-unit contains N claims
- [authority-binding](authority-binding.md) — every `claim_made` event records the authoring actor (per-claim author attribution; chain-of-defense per axis-3); per-claim attribution chain is one of three architectural sub-aspects of authority-binding
- [practitioner](practitioner.md) — practitioner is the author who must defend claims (axis-3 anchor)
- [authorship preservation (axis 3)](authorship-preservation.md) — defensibility test resolves at claim granularity
- [defensibility](defensibility.md) — claim is the unit-of-defense per the defensibility test; one indefensible claim taints the work-unit's output
- [sparring (axis 2)](sparring.md) — sparring fires AT claim granularity: counter-arguments target individual claims; confidence calibration applies per claim; selective friction triggers per claim ambiguity
- [event](event.md) — claims emit `claim_made` events (specific event-kind; ARCH Layer 3 detail); the audit trail records claim emission per shape's audit-granularity policy
- [mechanism](mechanism.md) — composes with TWO framework-level mechanisms: (1) audit-emission mechanism captures claim emission via `claim_made` event-kind; (2) source-grounding mechanism requires every claim trace to source (no unsourced claims at framework level)
- [policy](policy.md) — audit granularity policy (per shape) determines emission frequency: **claim-level** = one event per claim (practitioner-shape standard; finest granularity; mandates by axis-3 defensibility); **action-level** = one event per workflow action (drafting_started, review_completed, send_authorized — not per claim; autonomous-business-shape default; coarser); **light** = minimal events for memory/replay only (personal-OS-shape default; no external accountability requirement)
- [rubber-stamping](rubber-stamping.md) — claims rubber-stamped at attestation lack engaged-authorship; per-claim defensibility fails when rubber-stamping occurred at finalization
- [engaged authorship](engaged-authorship.md) — per-claim engagement is the success-mode test; per-claim engagement events fire DURING claim production (production-phase) + AT claim finalization (attestation-phase per-claim attestation event); engaged-authorship test resolves at claim granularity
- [answer-machine AI](answer-machine-ai.md) / [oracle AI](oracle-ai.md) / [validator AI](validator-ai.md) — axis-2 failure modes degrade per-claim sparring rigor; claims produced under axis-2 collapse less defensible per claim
- [category collapse](category-collapse.md) — general force; manifestations on any axis cascade into per-claim defensibility failure
- [workflow](workflow.md) — claims emitted during workflow_instance execution attribute to that workflow_instance; per-claim audit composes into workflow_instance audit context. Ad-hoc work claims attribute to work-unit + session without workflow_instance attribution.

**Cardinality + lifecycle**: Cardinality = N claims per work-unit (typically dozens-to-hundreds for substantive accountability-bearing outputs). Lifecycle = claims are CREATED during workflow execution (drafting fires `claim_made` events as claims are produced); claims may be REVISED during review (revision emits new event preserving prior claim state per append-only audit); claims are FINALIZED at send/sign moment (signed-claim_made event; practitioner authorship binding). Mutability = append-only at audit level (claim revision = new event, not rewriting previous); content mutability lives at draft level until finalization.

**Source**:
- VISION (`VISION.md`) line 154+ axis 3 framing — "the practitioner remains the defensible expert author of everything PBS produces"; the defensibility test resolves at claim granularity (axis-3 anchor)
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Concept-by-concept (worked examples)" — practitioner-shape policy "Audit granularity = claim-level" (claim is the unit-of-emission for that policy)
- Locked GLOSSARY entries: [policy](policy.md) ("Audit granularity = claim-level (configures the framework's audit-emission mechanism)"); [event](event.md) (events compose audit trail; `claim_made` is one event-kind); [authorship preservation](authorship-preservation.md) (defensibility test)
- Archived corpus for full claim-event schema (Phase 3 ARCH territory): `audit-trail-v2.md` (claim_made event-kind in event_kind catalog; source-grounding fields; revision-event semantics)

**See**:
- [work-unit](work-unit.md) (which contains claims)
- [authorship preservation (axis 3)](authorship-preservation.md) (which claim is the unit-of-defense for)
- [sparring (axis 2)](sparring.md) (which fires at claim granularity)
- [practitioner](practitioner.md) (who defends claims)
- [event](event.md) (claims emit `claim_made` events)
- ARCH Layer 3 claim-detail topics (placeholder until Phase 3 — claim-event schema, claim-revision semantics, finalization mechanics, source-grounding requirements per claim, sparring-target mechanics; archived material to consult: `audit-trail-v2.md`)
