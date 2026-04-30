# Decision record: Three-tier framework + marketplace shape + strategic positioning

**Status**: ACCEPTED (session 13, 2026-04-30)
**Owner**: VISION.md "Three deployment possibilities" section + ROADMAP commitment #22 + `docs/strategic-positioning.md`
**Sharpening metadata**: Round 3 C-section content of decomposed terminology-and-level-boundaries decision-design-sharpening (3-round full surface coverage; per-sub-DR rounds skipped per Pareto analysis). ~10 strategic refinements surfaced as expansions/revisions.
**Related**:
- `terminology-and-specialist-primitive.md` (Sub-DR A — required precondition; defines Workspace + Specialist primitives this DR builds on)
- `office-vs-department.md` (#12 — predecessor for office-vs-department reasoning, now superseded by Sub-DR A on naming)
- `a2a-and-gemini-pattern-emulation.md` (#10 — A2A schema patterns; Tier 3 reframing surfaced session 12)
- `substrate-agentic-framework.md` (#18 — substrate decision; three-tier framing builds on substrate layer)

## Context

Sub-DR A established Workspace + Specialist as pattern primitives, demoted Department to optional grouping. The naming shift surfaces a deeper strategic implication: PBS positioning today ("AI office for expert practitioners") undersells what the framework actually IS (composable infrastructure for many workspace shapes).

Round 3 C-section sharpening (decomposed into this DR per skill's >3-round-decomposition trigger) surfaced:
- Three-tier framing locked
- ICP refinement (PBS narrow vs. framework broader)
- Three deployment possibilities → four (specialist authoring tier added)
- Marketplace shape locked (specialists, not workspaces)
- Strategic positioning rewrite

These are downstream of Sub-DR A's primitive decisions but separate enough in audience + cascade to warrant their own DR.

## Decision

Lock the three-tier framework + marketplace shape + four deployment possibilities + strategic positioning sharpening.

## Three-tier framing

Composable AI work infrastructure organizes across three tiers:

| Tier | Layer | What it is | Strategic claim |
|---|---|---|---|
| **Infrastructure** | The framework | Composable AI work runtime: persistence + governance + sparring + audit + substrate abstraction | "We build the infrastructure that powers practitioner workspaces" |
| **Workspace** | Deployment shape | A configured deployment: identity + employed specialists + state + groupings | "Office is one workspace shape; practice/lab/studio/personal-base are equally valid" |
| **Specialist** | Composable expertise | A bundle of codified expertise; cross-archetype OR domain-anchored | "Marketplace of specialists; install what your workspace needs" |

Each tier has distinct distribution + audience + economics:

| Tier | Distribution path | Audience | Economics |
|---|---|---|---|
| Infrastructure | Open-source framework | Framework adopters + consulting clients | Free framework + consulting revenue |
| Workspace | Pre-configured templates per archetype (v2 generator) | Specific archetypes (planning bureaus, legal practices, research labs) | Workspace generator product (v2) |
| Specialist | Specialist marketplace (v3) | Workspace operators selecting capabilities | Per-specialist subscription / open + premium tiers (TBD per D2) |

## ICP refinement

Today's ICP: "solo professionals + small companies in expert-practitioner domains."

Sharpened ICP across three tiers:

| Tier | What sells | ICP |
|---|---|---|
| Infrastructure | Framework adoption + consulting | Practitioner-archetype firms ready to deploy AI workspaces; consulting engagements |
| Workspace | Pre-configured workspace templates per archetype | Specific archetype niches (planning bureaus, legal practices, research labs, accounting firms) — narrower than infrastructure ICP |
| Specialist | Marketplace browse + install | Wider — any workspace operator (including non-practitioner archetypes: solo creatives, knowledge-graph deployments) |

**ICP discipline preserved**: PBS sells narrow (consulting + workspace templates); framework architecture serves broader (marketplace expands ecosystem). PBS-Schulz validates the planning-bureau workspace shape; other workspace shapes pioneered by other deployments.

## Four deployment possibilities (was three)

VISION.md "Three deployment possibilities" section updates to four:

| # | Possibility | Today's framing | Sharpened |
|---|---|---|---|
| 1 | **Infrastructure adoption + consulting** (primary) | "Real production + consulting" | Firms deploy workspaces using PBS infrastructure; PBS-Schulz reference workspace + Gunther as consultant. Pattern transfer is the natural realization of pioneer IP |
| 2 | **Specialist authoring** (NEW tier) | (didn't exist) | PBS-Schulz develops specialists (planning-document-work, citation-verification, layered-review-framework); marketplace distribution for cross-archetype specialists; revenue from specialist subscriptions or premium tier |
| 3 | **Workspace shape distribution** | "Sell to other Planungsbüros" | Pre-configured workspace templates per archetype (planning bureaus, legal practices, research labs); productized workspace shapes via v2 generator |
| 4 | **SaaS / multi-frontend** (distant) | Same | Hosted infrastructure tier; years out, not months |

The marketplace adds Tier 2 as a NEW intermediate revenue path between consulting (Tier 1) and productized workspaces (Tier 3).

## Marketplace shape (architectural lock)

**Marketplace is OF SPECIALISTS, not of workspaces or offices.**

This wasn't crisp pre-Sub-DR A. Now locked architecturally:

- Workspace generator (v2) scaffolds workspace shape per archetype
- Specialist marketplace (v3) populates workspaces with capabilities
- Two distinct distribution surfaces; complementary

### Architectural constraints locked (v3 mechanics deferred per D1)

Marketplace listing = one specialist version. Listing must include:

| Field | Required | Source |
|---|---|---|
| Specialist Pydantic shape (Layer 1 + Layer 2) | Yes | specialist.md frontmatter |
| Skill definitions | Yes | bundled SKILL.md files |
| Entity Pydantic schemas (Layer 2 subclasses) | Yes | entities/ directory |
| Process entities + references manifest | Yes | bundled |
| Event subscriptions | Yes | for compatibility check at install |
| Substrate compatibility list | Yes | substrate_compat field |
| Dependencies (other specialists) | Optional | for composite specialists per D5 |
| Version + changelog | Yes | semver track |

### Marketplace-level concerns deferred (per D1)

- Authentication
- Pricing model
- Quality governance
- Deprecation lifecycle
- Specialist signing / provenance verification

These are ROADMAP v3 work; constraints locked here so v3 design doesn't require redesign of v1 specialist contract.

## Strategic positioning rewrite

| Today (`docs/strategic-positioning.md`) | Sharpened |
|---|---|
| "AI office for expert practitioners (planners, lawyers, researchers, accountants)" | "Composable AI work infrastructure for practitioner workspaces (planning bureaus, legal practices, research labs, creative studios, knowledge bases, federation networks)" |
| Competitor: vertical SaaS replacements + Microsoft Copilot for orgs | Competitor: Notion + Slack + Anthropic plugin tooling; differentiated on intertwining + sparring + authorship |
| ROADMAP v2: "AI-office builder" | ROADMAP v2: "AI-workspace generator" (or "framework deployment generator") |
| ROADMAP v3: "Marketplace of department modules" | ROADMAP v3: "Marketplace of specialists" — matches Anthropic plugin shape |
| Consulting pitch: "deploy an AI office for your firm" | Consulting pitch: "deploy an AI workspace using PBS infrastructure; assemble specialists your practice needs" |
| Open-source-as-edge | Same — framework openness preserved; specialists can be open OR proprietary |

## Framework-foundation framing sharpening

Per ARCH "Pattern-vs-instance discipline" + framework-foundation framing (v0.20):

PBS framework foundation = the **infrastructure layer**. PBS-Schulz validates the workspace shape "office for planning bureau." Future deployments validate other shapes.

| Pioneer | Validates |
|---|---|
| PBS-Schulz | Office workspace shape; planning-document-work + project-management + invoicing specialists |
| Hypothetical legal-practice deployment | Practice workspace shape; legal-research + matter-management specialists |
| Hypothetical research lab | Lab workspace shape; methodology + manuscript-prep + grant-writing specialists |
| Hypothetical solo creative | Personal workspace shape; voice + drafting + editing specialists |
| Hypothetical knowledge graph | KB workspace shape; knowledge-only specialists (skills=[]) |
| Hypothetical federation | Federation workspace shape; assembled from shared specialist registry |

Each new validation extends the framework's proven envelope. PBS pioneers the office shape; later deployments pioneer other shapes.

## Composition with VISION

VISION's three axes (intertwined-AI-workflow + sparring partner + authorship preservation) **unchanged**. They apply to ANY workspace shape, not just office.

VISION cascade (specific edits):

| VISION section | Today | Sharpened |
|---|---|---|
| "What this is, in one line" | "An AI office pools and leverages domain and company knowledge to automate and support interactive workflows in a coherent manner" | "An AI workspace pools and leverages codified expertise (bundled as specialists) to automate and support interactive practitioner workflows in a coherent manner" |
| "Target users" | "expert-practitioner domains (planners, lawyers, researchers, accountants, consultants, boutique firms)" | Unchanged — expert-practitioner survives as human archetype per Sub-DR A's "Specialist" choice |
| "Office vs department" section heading | "Office vs department (open architectural question, session 7)" | "Workspace shapes (resolved session 13 per Sub-DR A; Department demoted to optional grouping)" |
| "Three deployment possibilities" | 3 possibilities | 4 possibilities (specialist authoring tier added; see above) |
| "AI-office builder" references | "AI-office builder" | "AI-workspace generator" |
| Architectural requirements section | "Office: a container for multiple departments" | "Workspace: deployment scope; assembles specialists" |

## Defers (chronological-valid)

| Defer | Home | Cost being avoided |
|---|---|---|
| D1: Marketplace mechanics (auth, pricing, governance, deprecation) | ROADMAP v3 | Substrate distribution mechanics not settled; substrate-coupling risk |
| D2: Specialist economic model (subscription / open + premium / one-time) | ROADMAP v3 | Marketplace shape locked; pricing requires user research + market data |
| D3: Workspace template productization details (which archetypes ship templates first; pricing) | Tier 3 productization (post-pioneer-instance phase) | Pioneer phase still in progress; productization premature |
| D4: Specialist signing / provenance | ROADMAP v3 marketplace launch | Trust infrastructure for marketplace not concrete pre-launch |

All chronological-valid: each names specific information that doesn't exist yet.

## Cascade

| Layer | Change |
|---|---|
| `docs/strategic-positioning.md` | Substantial rewrite per "Strategic positioning rewrite" section above |
| `VISION.md` | Per "Composition with VISION" section above; thesis line, deployment possibilities (3→4), AI-office references, architectural requirements section |
| `ROADMAP.md` v2 | "AI-office builder" → "AI-workspace generator" |
| `ROADMAP.md` v3 | "Marketplace of department modules" → "Marketplace of specialists"; architectural constraints locked here |
| `docs/decisions/a2a-and-gemini-pattern-emulation.md` | Tier 3 reframing already applied session 12; verify consistency with three-tier framing |
| `HANDOFF.md` | Session 13 entry; strategic positioning + four-tier framing summary |

## Files touched

- `docs/decisions/positioning-three-tier-framework.md` (NEW — this file)
- `docs/strategic-positioning.md` (substantial rewrite)
- `VISION.md` (per cascade above)
- `ROADMAP.md` (v2 + v3 entries)
- `HANDOFF.md` (session 13 entry)

## Revisit triggers

- First real second-deployment workspace shape lands → validates four deployment possibilities framing
- First marketplace listing → validates marketplace constraint locking
- First specialist authoring revenue → validates specialist authoring tier (possibility 2)
- First non-practitioner ICP customer (creative / KG / federation) → validates broader-ICP framing
- Workspace generator (v2) launches → validates workspace shape distribution (possibility 3)

## Pattern-vs-instance check

| Domain | Decisions hold? |
|---|---|
| Planning bureau (PBS) | ✅ Workspace shape: office; specialists: planning-document-work, PM, invoicing |
| Legal practice | ✅ Workspace shape: practice; specialists: legal-research, matter-management |
| Research lab | ✅ Workspace shape: lab; specialists: methodology, manuscript-prep |
| Solo creative | ✅ Workspace shape: personal; specialists: voice, drafting |
| Knowledge graph | ✅ Workspace shape: KB; specialists: knowledge-only |

Three-tier framing + marketplace shape generalize. Pattern-level. ✓
