# VISION ↔ ARCHITECTURE coupling review (target 8, first run)

**Date**: 2026-04-29
**Scope**: VISION.md + ARCHITECTURE.md (4 meta-rules + 1 layering
convention + 5 entity types + 3 decision rules + maintenance
discipline) + sampled ROADMAP items
**Trigger**: Target 8 added in this session as part of the
boundary-refinement bundle. Mirrors slice 14's relationship to
target 7 — but at the higher coupling tier (vision-architecture,
not architecture-implementation).
**Skill version**: design-review 0.4.0

---

## Map 1 — VISION → ARCH (mechanisms → enforcement)

For each VISION-named mechanism, the architectural enforcement it
relies on, classified as:

- `structural` — architecture constrains placement; the mechanism
  is forced into existence by entity type / meta-rule / decision rule
- `behavioral` — skill body asserts the requirement; LLM has to
  follow it but no structural backstop
- `unenforced` — no current mechanism, only aspirational

### Axis 1 — Intertwining (6 mechanisms)

| # | Mechanism | Enforcement | Class |
|---|---|---|---|
| 1.1 | Persistent state across sessions | Meta-rule 1 (app/office split + roots.state); Meta-rule 3 (invalidation contracts on Memory + Configuration) | **structural** |
| 1.2 | Orchestration as primary | Skill Bundle entity + orchestrator skill + PROCEDURE.md checkpoints; decision rule 1 | **structural** |
| 1.3 | Source-grounded outputs | Meta-rule 2 (memory/RAG line); PROCEDURE.md Checkpoint 5 | **behavioral with structural floor** |
| 1.4 | Audit trail | Scattered: decisions.md, snapshots/, changelog.md, git, manifests; unified version is ROADMAP | **behavioral + unenforced** |
| 1.5 | Continuous awareness of context | Orchestrator session-open load (watch list, projects-index, pending-actions) | **structural** (skill loads) + **behavioral** (content) |
| 1.6 | Explicit human-authority gates | Decision rule 1 places gate logic in skills; meta-rule 4 enforces deterministic-vs-judgment split | **structural** (decision rules) + **behavioral** (gate placement in PROCEDURE.md) |

### Axis 2 — Sparring (7 mechanisms)

| # | Mechanism | Enforcement | Class |
|---|---|---|---|
| 2.1 | Counter-argument as first-class output | PROCEDURE.md Checkpoint 13 names it; no output-schema enforcement | **behavioral** |
| 2.2 | Confidence calibration | Mentioned in layered review references; no confidence-metadata schema | **behavioral** |
| 2.3 | "What's missing?" checkpoint | PROCEDURE.md Checkpoint 11 + 12 | **behavioral** |
| 2.4 | Anti-sycophancy guard | Checkpoint 13 ("does not capitulate without reason") | **behavioral** |
| 2.5 | Selective friction calibration | Decision rule 1 (mechanical→auto, judgment→surface); meta-rule 4 (deterministic/interpretive line) | **structural** |
| 2.6 | Asymmetric knowledge respect | Checkpoint 13 framing + specialist references | **behavioral** |
| 2.7 | Commit to recommendations | Checkpoint 13 names it | **behavioral** |
| 2.8 | Visible reasoning | module-decisions.md is optional; no format schema | **behavioral** |

(VISION lists 7 sparring mechanisms; the agent enumerated 8 by
counting "counter-argument" + "commit to recommendations" + visible
reasoning separately. Either count yields the same conclusion.)

### Axis 3 — Authorship preservation (5 mechanisms)

| # | Mechanism | Enforcement | Class |
|---|---|---|---|
| 3.1 | User understands what they're signing | Layered review (Checkpoints 4.2, 4.3) + module-decisions.md | **behavioral** |
| 3.2 | User has engaged with judgment calls | Selective friction (meta-rule 4) + four-way menu | **structural + behavioral** |
| 3.3 | User is explicit decision-maker at gates | Four-way menu, send confirmations, lifecycle gates | **behavioral** |
| 3.4 | User can reconstruct *why* later | Meta-rule 3 (invalidation contracts), decisions.md, snapshots, verified_against_version on bausteine | **structural floor + behavioral content + unenforced unified-trail** |
| 3.5 | AI labor; user judgment + signature | Decision rules 1+2+3; send-gate enforces signature step | **structural** |

---

## Map 2 — ARCH → VISION (meta-rules → axes served)

For each meta-rule + named convention, which VISION axes it serves,
classified as:

- `load-bearing` — axis would be unenforced without this rule
- `supporting` — one of several enforcers
- `floating` — no clear coupling (overhead candidate)

| Rule | Axis 1 | Axis 2 | Axis 3 |
|---|---|---|---|
| **Meta-rule 1: App vs office** | **load-bearing** (intertwining requires deployment-specific state to intertwine with — without office split, PBS becomes generic tool = tacked-on failure mode) | floating | **load-bearing** (without office split, signature/identity/signer can't be office-authored — app vendor becomes implicit author = authorship collapse) |
| **Meta-rule 2: Memory vs RAG (citation freshness)** | load-bearing (source-grounding) | floating | **load-bearing** (defensibility requires fresh citations — "I didn't know the law changed" isn't a defense) |
| **Meta-rule 3: Source-of-truth & invalidation** | **load-bearing** (state coherence over time) | floating | **load-bearing** (audit trail + verification metadata enable reconstruction) |
| **Meta-rule 4: Execution determinism** | **load-bearing** (orchestration consistency across sessions) | **supporting** (selective friction via deterministic/interpretive split — the closest axis-2 has to structural enforcement) | supporting |
| **Layering convention: Scope orthogonality** | supporting (orchestrator loads scope-appropriate context, but works without it) | floating | supporting (user's authorship scoped to their domain/state) |

---

## Findings

### F1. Axis 2 (sparring) is structurally weak

**All 7 sparring mechanisms are behavioral or behavioral-leaning.**
Only meta-rule 4's selective-friction calibration provides any
structural enforcement, and it's specifically about *placement*
(which side of the boundary an operation lives on), not about
sparring-output shape.

This means:
- The anti-sycophancy guard depends on the orchestrator skill body
  containing assertion-language that future LLM versions read and
  follow. If procedure wording softens during a refactor, the guard
  silently weakens.
- Counter-argument output is a procedural expectation; no
  validator catches a skill output that ships without one.
- Confidence calibration has no metadata schema; the LLM signals
  confidence in prose, which is unparseable downstream.

**This is exactly the LLM-inference surface area that
[feedback memory `feedback_llm_instruction_tightness.md`] warns
about.** Brittle. Drifts silently. High overhead each session.

**Risk profile**: VISION names "answer machine" (axis 2 collapse)
as one of three category-collapse risks. Meta-rule 1 has structural
defense against axis 1 collapse ("tacked-on"); meta-rule 3 has
structural defense against axis 3 collapse ("rubber-stamping" —
the audit trail gives reconstruction). **Axis 2 has no structural
defense** — it relies entirely on periodic vigilance via the audit
+ design-review skills running on schedule.

### F2. Unified audit trail still scattered + deferred

VISION's defensibility test ("user defends six months later") is
an axis-3 load-bearer. Today the audit trail lives across:

- `_ai/decisions.md` (per-project decisions)
- `_ai/module-decisions.md` (per-module include/exclude reasoning)
- `_ai/snapshots/` (immutable artifact bundles per send)
- `_ai/changelog.md` (chronological project changes)
- Git history (code/doc changes)
- Manifest entries (`verified_against_version` on bausteine refs)

There is no single query layer that reconstructs "what was decided
about §X between Vorentwurf and Entwurf, with why-reasoning, six
months later." The user does manual detective work to assemble
this from 6 sources.

**ROADMAP names "audit trail — unified change/decision/version
tracking" as deferred** with no stated pull-forward trigger.

The defensibility test's load-bearing requirement and the
ROADMAP's defer status are in tension. **This is a v1-scope
decision the user should make explicitly.**

### F3. Meta-rule 1 IS load-bearing for axes 1 + 3 (push-back on agent)

The first-run agent classified meta-rule 1 as "supporting" for
axis 3 only and proposed reframing as "deployment decoupling"
rather than VISION-infrastructure. This artifact disagrees:

- **Axis 1 coupling**: "intertwined-AI-workflow" requires deployment-
  specific workflow to intertwine with. Without app/office split,
  the workflow becomes generic-AI-features-applied-uniformly —
  which is the tacked-on failure mode VISION explicitly names.
  Meta-rule 1 IS structural defense against axis 1 collapse.

- **Axis 3 coupling**: "user remains the author" requires the
  signature/identity/signer name to be office-authored, not
  app-hardcoded. Without app/office split, PBS produces work
  signed by-default-the-app-vendor-name, with the office having
  to manually override every output. That's not authorship
  preservation; that's authorship reclamation. Meta-rule 1 IS
  structural defense against axis 3 collapse via the implicit-
  author failure mode.

**Recommendation**: keep meta-rule 1 as structural-load-bearing
for axes 1 + 3. The agent's framing missed the deeper coupling.

### F4. Category-collapse defense is asymmetric

VISION names three category-collapse risks:

| Risk | Structural defense | Vigilance defense |
|---|---|---|
| Axis 1: tacked-on feature catalog | meta-rule 1 (app/office) + decision rule 1 (orchestrator-as-primary) | audit + design-review periodic |
| Axis 2: answer machine | **none** | audit + design-review periodic |
| Axis 3: rubber-stamping | meta-rule 3 (audit-trail scaffolding) — **partial; unified trail deferred** | layered review checkpoints |

The asymmetry mirrors F1 + F2 above. Axis 2 is the high-leverage
gap; axis 3's gap is bounded (defer-with-trigger).

### F5. Behavioral-only enforcement isn't always wrong

Counter-finding for refinement-Pareto: **not every VISION
mechanism needs structural promotion.** Some are appropriately
behavioral:

- Source-grounding (1.3): meta-rule 2 + Checkpoint 5 + verify-
  citations skill provide solid floor; the LLM-inference cost is
  small for a clearly-stated principle. Promoting to schema
  validation would add overhead without much added enforcement.
- Visible reasoning (3.1, 3.4 partial): module-decisions.md is
  intentionally optional — not every decision needs reasoning,
  only judgment-bearing ones. Mandating format schema would force
  ceremony where it doesn't add value.

**The structural-promotion candidates from this review are F1
(axis 2 enforcement) and F2 (unified audit trail). Other
behavioral mechanisms can stay.**

---

## Verdicts (5-category framing)

### REFACTOR-WITH-CONVICTION

**(none)** — no current mechanism warrants in-session refactor.
Both highest-leverage findings (F1, F2) require their own design
passes; doing them in-session would balloon scope past what's
been authorized.

### REFACTOR-WITH-RESHAPE (next-session-or-later, with design pass)

1. **Axis-2 structural promotion (F1)**. Design + build a sparring-
   output convention that moves at least 2-3 of the 7 axis-2
   mechanisms from behavioral to structural. Most defensible
   options to investigate:
   - `sparring-output` MCP tool that validates output schemas
     carry counter-argument + confidence + reasoning fields where
     declared.
   - Skill Bundle convention: `validates_via: <tool-name>`
     frontmatter declaration; `list_skills` returns it; orchestrator
     wires the validation.
   - Anti-sycophancy guard as a deterministic check (e.g.,
     "did this response soften vs. the prior response on the same
     question without new evidence?" — heuristic, but better than
     nothing).
   This is a real architecture addition. Half-day to design + day
   to build. ROADMAP entry recommended.

2. **Unified audit trail promotion decision (F2)**. User-judgment
   call: keep deferred, or pull forward to v1? If pulled forward:
   design + build the unified Memory (record) subkind with
   query layer. Multi-day work. Decision belongs to the user, not
   to this artifact.

### ROUGH-AND-WORTH-REFINING

3. **Document the structural/behavioral classification in
   ARCHITECTURE.md.** The current meta-rules don't explicitly
   distinguish which VISION mechanisms they enforce structurally
   vs. supportively. A small addition to maintenance-discipline:
   when adding a meta-rule, declare which VISION axis it serves
   and at what classification. Forces vision-coupling explicit
   and makes future drift detectable. ~30 min addition.

### ROUGH-BUT-ADEQUATE

4. **Meta-rules 1, 2, 3 axis-1 + axis-3 coverage is solid.** No
   structural changes needed. Maintenance is sufficient.

### OVERHEAD-CANDIDATE

**(none)**. The agent flagged meta-rule 1 as overhead; this
artifact pushed back (F3). Other rules are clearly load-bearing.

---

## Stopping decision

**Target 8 first run is complete.**

The exercise validated target 8 as a useful design-review tool —
it surfaced two concrete gaps (F1, F2) that prior reviews hadn't
named, plus one push-back-worthy agent-conclusion (F3) that
demonstrates the target serves anti-bias review (the agent's
greenfield reframe was wrong on meta-rule 1; the human cross-
check caught it).

**Re-run target 8 after**:
- Axis-2 structural promotion lands (F1's reshape) — verify the
  newly structural mechanisms reduce the behavioral surface area
  cleanly.
- Unified audit trail decision is made (F2) — re-classify axis 3
  enforcement.
- Any new meta-rule is added to ARCHITECTURE.md.

The architecture *does* deliver on the vision, with two named
gaps that have clear next-session paths. Pre-launch is the right
window for axis-2 promotion, before behavioral-enforcement
patterns calcify into "the way it's done."
