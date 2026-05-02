# Profile L5a: Solo planner — PBS-Schulz pioneer

**Status: PRELIMINARY — anchor profile (most-grounded; pioneer reality)**

**Lifecycle stage**: L5 (practitioner-user)
**Shape variation**: practitioner-shape
**Archetype**: planner (Bauleitplanung; specifically B-Plan + Begründung)
**Scale**: solo (single practitioner; planning bureau as one-person practice)

## Identity + context

Gunther Schulz, planner running Planungsbüro Schulz in Brandenburg, Germany. Sole proprietor (single-practitioner planning bureau). Domain: Bauleitplanung (urban planning under German Baugesetzbuch). Specialty: Bebauungsplan + Begründung work for municipalities (mostly small municipalities; ~2-50K residents).

Regulatory environment: heavy. EU directives → German federal law (BauGB) → state law (Brandenburg LBauO) → municipal regulations. Defensibility under Stellungnahmen (formal objections from authorities); legal challenges; potential litigation. Six-months-later test is concrete: a Begründung's argumentation must hold up under UNB (Untere Naturschutzbehörde) review months after submission.

Tech-comfort: high. Uses git for document version control; uses LaTeX for formal documents; building PBS framework specifically for AI-co-worker integration. Comfort with tooling complexity is unusual for the planning archetype generally.

The pioneer instance: PBS-Schulz is the originating deployment. Framework was extracted FROM this work, then re-applied TO it; refinements flow bidirectionally between framework and pioneer.

## Day-in-the-life / usage flow

A typical project arc (B-Plan-Begründung for a municipality):

**Intake phase**:
- Municipality contacts; submits parcel + scope; signs contract
- Practitioner creates work-unit (kind: `project`) in workspace
- Initial codified workflow_instance starts: B-Plan-Begründung drafting workflow
- Phases: research → draft → review → send → response handling

**Research phase (often hybrid: codified + ad-hoc)**:
- Codified: load relevant references (BauGB Art-XX commentary; FFH-VP guidance; previous B-Plans for similar municipalities); legal-interpretation skill activations
- Ad-hoc: exploratory case-law browsing; cross-referencing recent court decisions; reading new BMVBS guidance documents that don't fit codified flow
- AI co-worker engagement: sparring on legal interpretations ("does Art-1a apply here despite ÖPNV exception?"); challenge sessions on Naturschutz-Belange weighing
- Multiple sessions over days/weeks

**Drafting phase (codified + ad-hoc)**:
- Codified: draft Festsetzungstext + Begründung sections per shape templates; apply bausteine (reusable text patterns) for standard sections
- Ad-hoc: novel argumentation for non-standard situations; one-off explanations for unusual parcel features
- Per-claim source-grounding: every legal-interpretation claim, proportionality claim, nature-protection claim sourced + audit-trailed
- Sparring with AI on weak claims; revision cycles
- claim_made events emitted per substantive claim

**Review phase (codified)**:
- review-draft skill activated; layered review with sparring mechanisms
- Self-review pass + AI counter-argument pass + simulated UNB-perspective pass
- claim revisions tracked; new events emitted
- Authority binding: practitioner-only authority for accepting/rejecting AI counter-arguments

**Send phase (codified, with rubber-stamping risk)**:
- Final review; signed-claim_made events for finalization
- HITL authority: practitioner attests to each claim's defensibility before sending
- High rubber-stamping risk under deadline pressure (axis 3 failure mode)
- Document compiled (LaTeX → PDF) and sent to municipality

**Response handling (mix of codified + ad-hoc)**:
- Codified: Stellungnahme review workflow; per-objection response drafting
- Ad-hoc: novel objections requiring fresh research + argumentation; coordinator phone calls; informal authority consultations

## Hybrid moments

**Within a single session**: practitioner is mid-drafting (codified workflow_instance active) → notices unusual parcel feature → ad-hoc research detour (no workflow_instance for that exploration) → returns to drafting (workflow_instance resumes) → drafts a Festsetzung citing newly-researched precedent. Same session, multiple workflow_instance ↔ ad-hoc transitions.

**Across same work-unit**: project starts with B-Plan-Begründung drafting workflow (workflow_instance_A); during drafting, practitioner realizes Naturschutz aspects need separate FFH-VP workflow (workflow_instance_B starts in parallel against same work-unit); FFH-VP completes; drafting resumes; review workflow_instance_C starts post-drafting. Multiple workflow_instances against single work-unit, with ad-hoc work between.

**Mode switching**:
- Drafting (codified workflow) ↔ research (ad-hoc) ↔ communication (one-off email to municipality coordinator) ↔ archive (filing past project for reuse) — all within same hour sometimes
- AI engagement state shifts: deep sparring during drafting (axis 2); transcription of regulatory guidance during research (axis-2 risk: oracle); intertwined co-work during difficult argumentation (axis 1 success); occasional rubber-stamp risk during deadline-pressure send (axis 3 risk)

**Capability extension mid-flight**:
- Mid-project, practitioner realizes need for new specialist (e.g., FFH-VP-specific specialist not yet activated) → activates specialist mid-project → new skills become available → resumes work
- Adds new bausteine to memory based on novel argumentation; bausteine become reusable for future projects
- Configures new adapter (e.g., LaTeX-to-Word converter for municipality coordinator who doesn't use LaTeX)

## Capability composition

**Active specialists (subset)**:
- planning-document-work specialist: orchestrator + draft-textteil-b + review-draft + validate-checklist + research-references + verify-citations + save-baustein + record-feedback + survey-project + draft-cover-mail
- naturschutz-specialist: FFH-VP-specific skills + Eingriffsbilanzierung + Vermeidungsmaßnahmen
- legal-interpretation-specialist: Art-XX commentary loading + court-decision tracking
- Could activate more for specific projects (BImSchG specialist for noise-relevant projects, etc.)

**Active shape**: practitioner-shape (PBS marketed positioning)
- Mandates claim-level audit granularity
- Mandates source-grounding per claim
- Mandates engaged-authorship attestation per claim
- Mandates sparring sub-mechanisms (anti-sycophancy, counter-argument, etc.)

**Active substrate**: Claude Agent SDK (current pioneer choice)

**Active adapters**: email (Outlook); LaTeX compile; document signing (qualified electronic signature for sent docs)

**Layer A scope**: domains = {planning, naturschutz, environmental-law, baurecht}; states = {DE-BB} (Brandenburg-specific Layer A content)

## Multi-user moments

Solo practitioner — but interacts with:
- **Municipality coordinator** (client-side): sends drafts; receives Stellungnahmen; coordinates timing. Not a workspace user; treated as engagement-target.
- **UNB / TÖB authorities** (regulatory-side): submit Stellungnahmen; framework's defensibility test resolves against their challenges. Not workspace users; framework context (L12).
- **Coordinator / sub-consultant** (occasional): when project requires specialist sub-consultation (e.g., FFH-VP expert not in-house), practitioner sends draft sections for review. Not full workspace co-user; transient external-actor.

So: solo workspace user + multiple external actors interacting with produced artifacts. Not multi-practitioner workspace.

## Edge cases

**Deadline pressure**: Stellungnahme deadlines are statutory (often 6 weeks); compressed work cycles. Risk: rubber-stamping (axis 3 failure); answer-machine extraction (axis 2 failure); skipping sparring engagement to meet deadline.

**Novel regulatory situations**: new BMVBS guidance + court decisions create gaps in codified workflow patterns. Ad-hoc work increases proportionally. Framework must support seamless ad-hoc engagement without forcing premature codification.

**Cross-project pattern recognition**: practitioner notices same Festsetzungstext pattern appearing in 3+ projects → pattern crystallizes into reusable baustein → new memory entry → future projects reference. Capacity-building through codification.

**Regulatory challenge reality**: receives Stellungnahme citing Begründung weakness; six-months-later test fires. Practitioner must defend specific claim under UNB challenge. Defensibility primitive's three structural conditions tested in practice.

**Single-practitioner liability**: practitioner bears legal responsibility for entire project; no firm-internal review chain. Defensibility requirement is sharpest because no fallback signature authority.

**Mid-project specialist gap**: project surfaces need for specialist not yet activated (e.g., immissionsschutz expertise for noise-relevant project). Capability extension mid-flight required. Framework must support this without disrupting active workflow_instances.

## What this profile EXEMPLIFIES

This profile stress-tests:
- **Hybrid work pattern** (codified + ad-hoc + mode-switching) — anchor for workflow primitive's optional-overlay design
- **Solo defensibility** (single practitioner; no firm review chain) — sharpest defensibility scenario
- **High-regulatory environment** (EU + federal + state + municipal) — defensibility primitive's three conditions tested in practice
- **Capacity-building through codification** (bausteine + workflow definitions emerging from ad-hoc patterns) — capacity-building manifestation
- **Capability extension mid-flight** (specialist activation; adapter configuration) — workspace-scope capability changes orthogonal to running workflow_instance
- **Pioneer instance triple-purpose** (production-tool + research-lab + IP-proving-ground) — framework evolution feedback flows from this profile
- **Single-substrate concrete reality** (Claude Agent SDK choice; substrate primitive validated in concrete deployment)
- **Per-claim attestation** (claim-level audit granularity in practice; rubber-stamping risk realistic under deadline pressure)
- **Sparring as load-bearing runtime mechanism** (axis 2 sub-mechanisms used per drafting session; not occasional)
- **Cross-archetype generalization risk** (PBS-Schulz specifics like Begründung / Stellungnahme / UNB / DACH-EU need to NOT leak into framework primitives — pioneer instance grounds this concern)

## Architectural concerns this profile surfaces

- workflow primitive's bipartite + optional-overlay design grounded in this profile's hybrid reality
- defensibility primitive's three structural conditions concrete (engaged-authorship at attestation; reconstructible reasoning chain via audit; source-grounding per claim)
- claim primitive's claim-level granularity required for this profile's defensibility scenario
- Pattern-vs-instance discipline: profile reality must NOT leak into framework primitives (every PBS-Schulz-specific term is candidate instance-leakage to vigilant about)
- Capability extension orthogonality: workspace-scope changes don't disrupt workflow_instance state
- Sparring sub-mechanisms required by practitioner-shape policy mandates

## Status

**PRELIMINARY** — anchor profile (most-grounded reality; pioneer deployment). Updates flow from actual PBS-Schulz deployment experience. As alternative deployments accumulate evidence, this profile's load-bearing weight transitions from primary validator to historical anchor.
