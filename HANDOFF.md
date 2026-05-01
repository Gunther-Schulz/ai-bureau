# Session handoff — pbs-bureau (rebuild)

This is the running session log for the **foundational rebuild** launched session 16 (2026-05-01). The previous multi-session running handoff (sessions 1-15) is at `archive/HANDOFF.md` for reference.

## Anchors (carry forward, never rebuilt)

- `VISION.md` — three-axis thesis (intertwining + sparring + authorship preservation); preliminary-lock anchor; the ground truth the rebuild serves
- `MAINTENANCE.md` — doc system rules (5-layer model + cascade discipline + cross-reference discipline + maintenance rules); read at session start
- `memory/` — feedback files (lessons learned across sessions) + bausteine + universal prose; the actual user knowledge
- `archive/INDEX.md` — index of v0.35 corpus + code + content archived at rebuild launch; consult during Phase 3+

**Session-start reading**: `VISION.md` + `MAINTENANCE.md` + `HANDOFF.md` ≈ 1.7k lines.

## Rebuild phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Archive v0.35 corpus | ✅ Done session 16 |
| 1.5 | Design layered doc structure | ✅ Done session 16 (locked in `MAINTENANCE.md`) |
| 1.75 | VISION tightening pass (structure) | ✅ Done session 16 (1069 → 255 lines; content moved out lives in `archive/VISION.md`) |
| 1.8 | VISION terminology audit (term-level) | ✅ Done session 16 (15 candidates across 6 families; 2 inline tightenings; rest deferred to Phase 2 GLOSSARY) |
| 2 | Lock foundational vocabulary (`GLOSSARY.md`) | Next — proposal pending |
| 3 | Rebuild ARCH against locked vocabulary | Pending |
| 4 | Rebuild DRs selectively (collapse where possible) | Pending |
| 5 | Rebuild ROADMAP lean | Pending |
| 6 | Rebuild specs + code refactor (per existing #11 single-touch refactor) | Pending |

**Working procedure**: AI proposes next step → user adjusts/challenges/confirms → AI persists on sign-off. Per `feedback_propose_before_commit.md`.

## Session 16 — Rebuild launched (2026-05-01)

**What happened this session**:
1. Calibration clarifications surfaced 7 findings, all converging on one root: foundational vocabulary not crisply defined → layered approach named (session 14) but not permeated → instance-anchoring leakage in 5 different primitives (Art-25 naming, EU/DACH substrate-level additions, `project` enum, `groupings` primitive, practitioner = solo-human, vocabulary itself).
2. Strategy decision: archive everything (radical rebuild) rather than incremental patching. Rationale: pre-launch deprecation is essentially free per Maintenance discipline; `feedback_full_monty_upfront.md` says do comprehensive refinement upfront; preliminary-lock principle (v0.33) explicitly authorizes wholesale revision.
3. Archive complete: ARCH + ROADMAP + HANDOFF + docs/ (30 DRs + conventions + audits + design-reviews + strategic-positioning + rag-pipeline + plugin-conventions + backend-conventions + what-this-is + audit-pre-rag + office-config.schema) + extensions/framework/ (session-15 prototype) + backend/ (MCP server code) + plugin/ (19 skill bundles + templates) + .claude-plugin/ (plugin manifest) + extensions/{universal,domain,state}/ (PBS content; structure embodies scope-model decisions) + README.md. Code + content archived to remove rebuild bias per user direction; Phase 6 rebuilds against locked architecture. Memory/ + VISION + .claude/ + dev-link.sh + .gitignore stay as anchors / operational infrastructure.
4. `archive/INDEX.md` written with one-line purpose summary per piece + status note documenting known issues.
5. New HANDOFF.md (this file) written as rebuild log skeleton.

**Phase 1.5 outcome (locked session 16)**:

Layered doc structure designed and persisted in `MAINTENANCE.md` (Layer 0; read at session start). 5-layer model: Entry → Foundations → Overview → Architecture detail → DRs → Specs, plus Memory orthogonal. Cascade discipline elevated to top-level rule (per user direction): all docs stay in consistent state; changes propagate up/down/sideways in same commit.

**Phase 1.75 outcome (locked session 16)**:

VISION tightened from 1069 → 255 lines. Three axes preserved exactly; Ming foundation + IEP + adjacent thinkers preserved inline; falsification + robustness + defensibility test preserved (generalized). Removed: ARCH-territory mechanism lists; pioneer-instance + framework-foundation framing (design disciplines, not value claims); deployment possibilities + transition path + frontend + counter-VISION engagement + Cherry/EU fundability framing; Practitioner vs Specialist vocabulary; multi-practitioner implications. Resolved Option B floor inheritance contradiction. Reframed instance-anchored language to kind-neutral. All removed content lives in `archive/VISION.md` (v0.35 snapshot); new phases consult archive selectively when relevant rather than via promised lift-lists.

**Phase 2 starting state (locked session 16, multi-round sharpening complete)**:

**Foundational architecture locked** (now in MAINTENANCE.md "TOP-LEVEL ARCHITECTURE" section):
- Framework = MECHANISMS (universal interface contracts; no shape-specific values)
- Shape = POLICIES over mechanisms (each shape configures which active, mandatory, defaults)
- Atoms (mechanism, policy) vs containers (framework, shape) distinction
- A-B-C scope model derived from framework/shape framing (preliminary-locked)
- 4-axis classification scheme for GLOSSARY entries

**Term set locked** (~40 entries; multi-round sharpening output):
- 14 atomic primitives: workspace, practitioner, specialist, skill, AI runtime, actor, event, substrate, shape (meta), protocol, session, workflow, mechanism, policy
- 3 scope classifications: Layer A, Owner B, Framework C
- ~25 derived/compositions: workspace shape, practitioner-shape, named shapes catalog, multi-practitioner workspace, legal-entity workspace context, audit trail, sparring sub-mechanisms (8), cross-axis mechanisms (4), the 3 axes, defensibility, co-worker, intertwined-AI/tacked-on AI, pioneer instance, category collapse, framework
- Drops: trust/sparring/authorship mechanisms as separate classes (replaced by axis-tag metadata); shape-extension pattern (merged into shape); practitioner-author/expert practitioner (usage emphasis); practitioner-kind (variation lives at workspace level)

**Lock GLOSSARY entry-by-entry (per user direction "step by step")**. Order: foundational meta-primitives first (framework, shape, mechanism, policy), then atoms (workspace, practitioner, specialist, skill, AI runtime), then scope classifications (Layer A, Owner B, Framework C), then derived (axes, sparring sub-mechanisms, cross-axis mechanisms), then cross-cutting (actor, event, session, workflow, substrate, protocol).

AI proposes entry text → user adjusts/challenges/confirms → AI persists in `GLOSSARY.md`.

## Inputs to consider for the rebuild (from session-16 findings)

Persisted in `archive/INDEX.md` "Status note" section. Six findings flagged as inputs the rebuild should address at root:

1. Foundational vocabulary lock (framework / shape / mechanism / policy / practitioner / authority chain / Protocol disambiguation)
2. Shape-neutrality vs Option B floor contradiction
3. VISION-scope vs framework-scope contradiction
4. Instance-anchoring leakage (5 sites)
5. "Mechanism vs policy" vocabulary not in corpus (introduced in session-16 conversation; needs to land as named architecture if accepted)
6. Filesystem location drift (shape-extension DR vs v0.34 restructure)
