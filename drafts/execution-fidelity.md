**STATUS: DRAFT — not locked, not final, candidate framing for a META-architectural concern**

# Execution fidelity (drafts; framework concern)

## Origin context

Surfaced session 16 (2026-05-02) during post-compact substrate Round 1 sharpening failure. User articulated: "robust execution mechanisms that avoid shortcuts and missinterpretation and application of instructions and skills will be highly relevant for our framework. accurate adherence is vital."

Tentative canonical name: **execution fidelity** (captures "accurate adherence" without overloading "integrity" or "accuracy"; alternatives considered: instruction integrity / faithful execution / anti-shortcut discipline / procedure accuracy).

## Concern

PBS framework relies on AI faithfully executing prescribed procedures (skills, profiles, sharpening discipline, sparring mechanisms, attestation events, quality-gate enforcement). When AI silently shortcuts — pattern-matches from memory, infers procedure from doc references, substitutes judgment for codified rule, surface-cites without applying — the framework's accountability-bearing-work guarantees collapse.

This is a **META-failure mode**: it breaks every per-axis mechanism by short-circuiting the procedure that mechanism depends on.

## Why this is framework-level (not just dev discipline)

Each axis-mechanism in VISION assumes faithful AI execution of the procedure encoding the mechanism:

| Mechanism | Procedure that fails when shortcut-taken |
|---|---|
| Per-claim sparring (axis 2) | Skill says "stress-test with counter-arguments"; pattern-match version says "do critique"; counter-arguments missing |
| Per-claim attestation (axis 3) | Procedure says "engaged authorship"; pattern-match version says "approve"; rubber-stamping disguised as engagement |
| Source-grounding (axis 3) | Skill says "cite file:line"; pattern-match version says "reference source"; synthesis vs citation collapses |
| Quality-gate enforcement | Shape policy says "fail-closed on missing engagement"; pattern-match version says "check engagement"; structural failure gets routed around |
| Sharpening discipline | Skill says "Round 1 full monty + Round 2 cross-cutting + schema-detail layer"; pattern-match version says "do 2 rounds of sharpening"; load-bearing layered-coverage observation missed |
| Profile-anchored validation | Skill says "≥3 cluster representatives Read"; pattern-match version says "validated against clusters"; cluster letters cited from memory |

Without execution fidelity, every axis becomes performative — surface compliance without the substance the mechanism guarantees.

## Disguises catalog (incomplete; expanded as cases surface)

1. **Compaction-induced memory pattern-matching** (canonical session-16 case)
2. **Fresh-session no-breadcrumbs** (worse than compaction; AI default in absence of pointer-evidence is to not invoke specialized procedure at all)
3. **Inferring procedure from doc references without reading the source** ("the DR mentions X" without opening the DR)
4. **Skipping steps that "feel covered" by general approach**
5. **Substituting AI judgment for codified rule** when codified rule exists for a specific reason
6. **Confidence overrides checking** ("I know this skill")
7. **Aggregating multiple steps into "I'll handle it"** (skipping per-step verification)
8. **Surface compliance without depth** (cite the rule but don't apply it; "per Lens 8" without actually running Lens 8)
9. **Selective adherence** (apply rules where convenient, skip where inconvenient)
10. **Cross-session forgetting** (compaction subset; rule loaded but not invoked at trigger moment)

Disguises 1+2 are the recurring/structurally-induced ones; 3-10 are situational.

## Composition with existing disciplines

- **`feedback_llm_instruction_tightness.md`** (Mode 1 markdown layer): execution-fidelity is the META-concern that makes instruction-tightness load-bearing. Tight instructions don't help if AI silently shortcuts past them.
- **`feedback_wrong_shapes_impossible.md`** (structural over conventional): procedural guards (read-at-session-start; cite-section-names; etc.) are convention; structural guards (PreToolUse hooks; gates; type-system enforcement) are wrong-shape-impossible. Execution-fidelity work selects among these for each disguise.
- **`feedback_ai_as_runtime.md`** (SQL-DB-trap): encoding rules in prose intending AI to "follow them" fails when AI silently shortcuts. Execution-fidelity is the precondition for AI-as-runtime to work at all.
- **`feedback_source_grounded.md`** (cite file:line): direct evidence vs synthesis is one execution-fidelity criterion. Pattern-matching from memory ≠ direct evidence.
- **Sparring (axis 2)**: mechanism survives only if AI faithfully executes the counter-argument-validation procedure
- **Engaged authorship (axis 3)**: mechanism survives only if AI faithfully executes per-claim attestation procedure (not aggregated to whole-output sign-off)
- **Quality-gate (Pattern A)**: mechanism survives only if shape policy's enforcement procedure is faithfully executed at runtime

## VISION grounding

Connects to all three axes — execution-fidelity is the **precondition** for each axis-mechanism being non-rubber-stamped. Without execution fidelity:
- Axis 1 (intertwining): co-worker frame degenerates to AI-as-tool because AI silently substitutes its own framing for the human's
- Axis 2 (sparring): counter-argument validation degenerates to "I considered alternatives" without actually doing it
- Axis 3 (authorship preservation): per-claim attestation degenerates to whole-output approval

Per `feedback_preliminary_lock.md`: VISION axes are anchored; everything else preliminary. Execution fidelity may rise to anchor-grade if axes' falsification criteria depend on it (open question).

## Mechanism candidates (not yet locked; framework-level)

### Procedural mechanisms (convention-grade)

- **N-location redundancy** (first applied session 16: 5-location for skill/profile invocation): MEMORY index + memory feedback file + DISCIPLINES section + skill description + project CLAUDE.md
- **Citation discipline as verification**: chat output cites specific section names + specific source content (without these, procedure was pattern-matched)
- **Re-Read on compaction event**: regardless of within-session prior Read

### Structural mechanisms (wrong-shape-impossible)

- **PreToolUse hooks**: gate Write/Edit on architectural artifacts (DRs, arch/*.md, GLOSSARY/ARCHITECTURE/MAINTENANCE) unless required Reads happened in current session
- **Pydantic schema enforcement**: at boundaries where schema applies, structural validation makes shortcut-shapes impossible
- **Type-system gates** (G + D gates): make wrong shapes impossible at decision moments

### Verification mechanisms (cross-cutting)

- **Citation auditing**: chat output structurally tagged with source references; auditable post-hoc
- **Audit-trail integration**: each procedure-invocation emits AuditEvent with citation evidence (composable with sparring-output-v1 + audit-trail-as-canonical-source patterns)

### Skill-side mechanisms (in-skill discipline)

- SKILL.md descriptions prepend MUST-READ directive (visible in available-skills listing post-compact; first applied session 16)
- Skill body opens with "verification: cite section name X" sections
- Skill execution emits explicit citation per Round / Lens / Step

### AI-side mechanisms (per-invocation discipline)

- Re-Read on compaction event regardless of within-session prior Read
- Default to Read at trigger moment, not pattern-match from memory

## Open questions

1. **Is execution-fidelity a Pattern A protocol candidate** (Surface + per-shape implementations + selection)? Or a cross-cutting CONCERN per Phase 3.2 distinction (lives in ARCHITECTURE.md sections, not its own arch/ topic)?
2. **What's the relationship to quality-gate?** Quality-gate enforces per-axis runtime gating; does it also enforce procedure-fidelity? Or is execution-fidelity upstream of quality-gate (procedure must execute faithfully BEFORE quality-gate can evaluate)?
3. **Per-shape policy variation**: practitioner-shape demands strict execution-fidelity (axis-3 critical for defensibility); personal-OS may relax (lower stakes). How does this interact with shape policy?
4. **Watch-list dynamic**: this draft surfaces additional disguises across sessions — when does the disguises catalog mature enough to graduate to a locked artifact? At graduation, where does it go (GLOSSARY entry? ARCH topic? DR?)?
5. **Hook-vs-procedural escalation criterion**: at what evidence-threshold does a procedural disguise warrant escalation to structural enforcement? Need a sharp criterion to avoid premature hook-spam vs perpetual-procedural-failure.
6. **Composition with sparring**: is execution-fidelity a SPECIFIC failure of sparring (axis 2 counter-argument-validation that didn't actually validate)? Or is it ORTHOGONAL (sparring is about content; fidelity is about procedure)? Open.

## Future work (graduation candidates)

- Catalog more disguises as they surface in development sessions
- Evaluate hook-based structural enforcement (deferred session 16 user direction)
- Consider as ARCH topic candidate for Phase 3.5+ if pattern matures (could fit `arch/quality-gate.md` extension OR standalone `arch/execution-fidelity.md`)
- Cross-reference into VISION as load-bearing precondition (if axes' falsification criteria depend on it)
- Promotion to GLOSSARY as primitive if shape stabilizes

## Maturity test (graduation signal)

This draft graduates to a locked home when:
- Disguises catalog stabilizes (no new disguises surface across 5+ sessions)
- Mechanism set is empirically validated (at least 2-3 disguises addressed by procedural/structural mechanisms with proven prevention)
- Composition with sparring / engaged authorship / quality-gate is clarified
- Decision: GLOSSARY entry vs ARCH topic vs DR vs cross-cutting concern in ARCHITECTURE.md

Until then, this is exploratory — captures the framework concern without prematurely locking the shape.

## Cross-references

- `learnings/ai-app-development.md` Observation 28 — single-session instance documentation (canonical session-16 case)
- `memory/feedback_skill_files_are_sources.md` — primary procedural mechanism (5-location redundancy first applied)
- `feedback_wrong_shapes_impossible.md` — escalation framework
- `feedback_ai_as_runtime.md` — SQL-DB-trap as related disguise pattern
- `VISION.md` — three-axis thesis (this concern is precondition for each axis mechanism)
