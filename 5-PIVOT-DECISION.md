# 5-PIVOT-DECISION

> **Status**: Decision captured. PBS framework development PAUSED indefinitely. Pivot to building PBS-Schulz planning office directly on Claude Agent SDK / Cowork (including Managed Agents research-preview features). Framework preserved as-is for potential revisit; not active development.
>
> **Decision date**: session 35 (post-2026-05-06)
>
> **Companion documents**:
> - `1-NEXT.md` — F1-F4 framework plan PAUSED per this doc
> - `2-PRELEMINARY-ENTRERPRISE.md`, `3-PRELIMINARY-CONTEXT-GRAPH-POSITIONING.md`, `4-PRELIMINARY-COMPOSITION-FRAMEWORK.md` — preserved as decision-trail
> - `LOCKED-STATE.md` — status updated to "preserved pending Cowork-empirical-test outcomes"

---

## 1. The decision

**Build PBS-Schulz planning office directly on Claude Agent SDK + Cowork** (including Managed Agents features in research preview where useful). Use the empirical attempt as the canonical mechanism to discover:

- How far plain Claude SDK + Cowork can be leveraged for a real planning-office workflow
- What's genuinely missing vs PBS framework's design
- What (if anything) of the framework warrants preservation: full framework / specific pieces / nothing

**Framework development PAUSED**. Not abandoned; preserved. Repository state at this commit is the preservation point.

## 2. What drove this decision

Session 35 across multiple turns of competitive verification kept narrowing PBS framework's claimed unique value:

- Initial framing (thin-layer, context-graph, composition-substrate) progressively verified-against landscape
- Microsoft Copilot Studio verified as covering: persistent agents + workflow flows + reusable agents + visual low-code + cross-agent delegation + audit trail
- Claude Cowork + Managed Agents verified as covering: persistent agents + skills + MCP + cross-app workflows + event history + HITL + cross-platform SKILL.md format push
- PBS's verified-unique features narrowed to a niche intersection (self-host + open-source + cross-vendor + sparring/defensibility-discipline + engagement-detection + free + markdown-preference + regulated-profession-with-data-sovereignty)
- The intersection is real but small + each individual differentiator is niche

User position (verified per session 35 messages): "the only thing that matters can my framework bring unique value. that's the only thing." After today's verification: insufficient confidence the unique value justifies framework-build effort vs the empirical-attempt-on-existing-platform alternative.

The honest test isn't theoretical comparison; it's empirical attempt. This pivot enables that test.

## 3. The empirical investigation goal

Build a working planning-office deployment using Claude Agent SDK + Cowork + custom MCPs + custom skills + Managed Agents (where research-preview helps). Track:

**What works out-of-the-box**:
- Persistent agent definitions (Cowork agents / Managed Agents)
- Skills via SKILL.md format
- MCP server integration for tools (email, PM, file-sync, custom corpus)
- Cross-app workflows within Cowork
- Audit logging (server-side event history)
- HITL approval flows
- Multi-step orchestration

**What requires custom work but is achievable**:
- Bauleitplanung-specific corpus MCP (BauGB / BNatSchG / DE-BB regional)
- LaTeX compile MCP
- Specialist authoring for planning domains (planning-document-work, project-management, invoicing, correspondence)
- Cross-tool entity resolution (mapping tables for project IDs, etc.)

**What may NOT be achievable on Cowork alone (the test items)**:
- Sparring discipline as load-bearing runtime mechanism (8 sub-mechanisms; counter-argument generation; anti-sycophancy; etc.) — can these be authored as SKILL.md files at PBS-discipline depth?
- Defensibility-grade audit reconstruction (claim-attribution chain across roles for 6-month-later defense) — can this be achieved via Cowork's event log + custom skill logic?
- Engagement detection (rigor-on-demand; framework enforcement scoped to engaged work only) — can custom skills + workflow triggers achieve equivalent behavior?
- Cross-vendor portability (working across Anthropic + Microsoft + Google substrates) — explicitly NOT possible on Cowork (Anthropic-locked)
- Self-hosting (data sovereignty for regulated work) — explicitly NOT possible on Cowork (Anthropic-managed only)

The empirical attempt surfaces what's REAL gap vs what's authorable-via-custom-skills.

## 4. What the empirical attempt produces

Three possible outcomes:

**(A) Cowork covers everything sufficiently** → no PBS framework needed. Scrap framework work. Continue using Cowork + custom skills + custom MCPs as the long-term deployment.

**(B) Cowork covers most; specific gaps real but small** → ship sparring + defensibility + engagement-detection as open-source SKILL.md set + companion tooling, NOT as full framework. Smaller-scope contribution to Cowork ecosystem than full PBS framework.

**(C) Cowork has substantive structural gaps** → PBS framework's specific architectural commitments justify framework work; resume parts of F1-F4 with empirically-grounded specificity (only build what Cowork can't).

Decision deferred until empirical evidence accumulates.

## 5. What's preserved + why

The framework body of work has substantive value REGARDLESS of pivot outcome:

- **VISION.md** — three-axes thesis + practitioner-accountability framing + Vivienne Ming sparring grounding remain load-bearing intellectual contribution; should not be lost
- **Glossary** — vocabulary precision (workspace / practitioner / specialist / claim / work-unit / defensibility / engaged-authorship / etc.) is reusable as conceptual frame for the Cowork-based work
- **Architectural reasoning** (`arch/*.md`) — even if not implemented as PBS framework, the ARCHITECTURAL THINKING about cross-domain composition, audit-trail attribution, sparring discipline, engagement detection is referenceable for designing custom skills + MCPs
- **Mechanism Surfaces** — Pattern A/B/C/D taxonomy may inform how we author specialists in Cowork
- **Mode 2 reference impls** (`pbs/impls/*.py`) — practitioner_shape_authority_binding + practitioner_shape_sparring + practitioner_shape_gate could inform what equivalent SKILL.md files would need to do, OR could be salvaged as Python helpers callable from Cowork agents

**Repository state at commit `<this commit hash>` is the preservation point**. Not edited going forward unless framework revisit is explicitly triggered (per §6).

## 6. Reopen criteria for framework work

Framework work resumes ONLY if the empirical investigation surfaces:

- **Trigger A — substantive structural gap**: Cowork architecturally cannot deliver sparring discipline OR defensibility-grade audit OR engagement-detection at PBS's claimed depth, AND the gap matters for actual planning-office work. Not a marginal limitation; a real architectural mismatch.
- **Trigger B — multi-deployment validation**: a second deployment (autonomous-business-shape OR personal-OS-shape) needs to ship that requires cross-substrate portability OR shape-policy-mediated mechanism variation. Concrete need, not speculation.
- **Trigger C — explicit user re-decision**: user reviews accumulated empirical evidence + decides framework work warrants resumption.

Without trigger firing: framework stays preserved indefinitely. Cowork-based deployment is the long-term path.

## 7. Pivot execution

**Tonight (this session)**:
- This document captures the decision
- `LOCKED-STATE.md` updated to reflect preserved-pending-empirical-test status
- `1-NEXT.md` header notes F1-F4 PAUSED per this decision
- HANDOFF.md note captures the pivot

**Next session(s)**:
- Set up Cowork / Claude Agent SDK working environment
- Configure first specialist (planning-document-work) as Cowork agent OR Managed Agent
- Wire first MCP integrations (email; some PM tool; placeholder corpus)
- Author first SKILL.md files for sparring discipline + claim-attestation + defensibility-test
- Iterate; capture findings in deployment repo's `findings/` directory
- Track which capabilities require custom work vs work natively

**Repository decisions for deployment work**:
- `pbs-dep-1` (existing private repo) — historical artifact; M1 Hello PBS proof-of-life
- `pbs-dep-2` (planned but not yet created) — was going to be PBS-framework-based deployment; instead, becomes Cowork-based deployment OR new repo created (decide at next session)
- New deployment repo could be named `pbs-schulz-planning` or similar (firm-anchored, not framework-anchored, since this isn't a "PBS framework deployment" anymore)

## 8. What this pivot does NOT do

- **Does NOT abandon VISION** — three axes + practitioner-accountability + defensibility test remain the goal of the deployment work; just achieved via Cowork rather than custom framework
- **Does NOT throw away architectural reasoning** — the body of architectural work stays as reference + is reusable as conceptual frame for designing custom skills + specialists in Cowork
- **Does NOT commit to Cowork forever** — this is empirical investigation; if Cowork hits substantive limits, options remain (per §6 reopen criteria)
- **Does NOT preclude open-source contribution** — if the empirical attempt produces useful sparring discipline / defensibility-grade audit / engagement-detection patterns as SKILL.md files + tooling, those can ship as open-source Cowork-ecosystem contributions independent of full framework

## 9. What this pivot DOES do

- **Pauses framework infrastructure work** — F1-F4 plan in `1-NEXT.md` is suspended; mechanism Surfaces stay as reference; no new architectural commitments
- **Empirically tests competitive claims** — instead of "PBS uniquely solves X" speculation, we get evidence
- **Saves time** — months of framework work redirected to actual planning-office utility
- **Reduces cognitive load** — single platform target (Cowork) instead of multi-substrate framework architecture
- **Preserves option value** — if the empirical attempt finds real gaps, framework work can resume informed by evidence

## 10. Honest framing on what session 35 produced

Today's progression: lock-and-park pivot → reopened with F1-F4 plan → vision-sharpening across multiple framings → competitive verification → honest narrowing → this pivot decision.

The framework work isn't wasted. It produced:
- Coherent vocabulary (glossary)
- Substantive architectural reasoning (arch/*)
- Vision articulation grounded in research (VISION.md, Vivienne Ming foundations)
- Verified competitive landscape understanding (sessions 35 web research)
- Honest assessment of where unique value lies vs doesn't

This is a body of work worth preserving. The pivot just acknowledges the empirical test should precede further framework architecture investment.

## 11. Honest basis caveats

- **Verified directly via session 35 web research**: Claude Cowork capabilities (Feb-Apr 2026); Claude Managed Agents architecture per Anthropic docs; Microsoft Copilot Studio capabilities (where mentioned for landscape only — user prefers not to use); Bauleitplanung tooling landscape (vertical-specific tools largely absent)
- **Verified via session 35 framework reads**: PBS architectural primitives + their substantive design quality
- **Inferred but high-confidence**: that empirical attempt is the right next step — derived from pattern of theoretical narrowing today; settling requires evidence
- **Inferred and uncertain**: that Cowork can deliver sparring + defensibility + engagement-detection at sufficient depth via custom skills — needs empirical attempt to verify
- **Not verified**: actual cost / friction of building planning office on Cowork — depends on Managed Agents API economics + Cowork connector coverage + custom MCP development effort
- **Not verified**: whether reopen criteria (§6) are calibrated correctly — could be too strict or too loose; revisit when empirical evidence accumulates

---

## Decision in one paragraph

PBS framework development is paused indefinitely. Repository state preserved as decision artifact. Next direction: build PBS-Schulz planning office directly on Claude Agent SDK + Cowork + Managed Agents (research-preview features OK) + custom MCPs + custom SKILL.md files. Empirical attempt settles whether Cowork covers planning-office needs sufficiently, whether specific PBS-unique discipline (sparring + defensibility + engagement-detection) needs to ship as open-source SKILL.md set, OR whether substantive structural gaps justify resuming framework work. Decision deferred until empirical evidence accumulates. Framework work reopens only if §6 reopen criteria fire. Otherwise: Cowork-based deployment is the long-term path.
