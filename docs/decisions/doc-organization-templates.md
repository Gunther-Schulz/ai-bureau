# Decision record: Doc-organization templates + memory consolidation (composite)

**Status**: ACCEPTED — session 16 (2026-05-02); 2-round generic sharpen (per `plugin/skills/sharpen/SKILL.md` v0.9.0) on the proposal itself; user-authorized execution.

**Owner**: Doc-system maintenance (Layer 0 governance work; per MAINTENANCE.md "When this doc itself changes" discipline).

**Related**:
- `MAINTENANCE.md` (5-layer doc model + TOP-LEVEL DESIGN PRINCIPLES + TOP-LEVEL SCOPE absorbs absorbed memory content)
- `DISCIPLINES.md` (absorbs 7 discipline files)
- `ARCHITECTURE.md` (cross-cutting principles absorb ai-as-runtime + llm-instruction-tightness)
- `phase-3-2-doc-organization.md` (composite DR pattern; this DR follows same Mode-2 composite decomposition shape)
- coherence-audit Lens 5 v0.2.1 provenance hygiene (DR Sharpening provenance section IS the meta-home; absorbs provenance from ARCH topics)

## Context

Mid-session 16, after substrate + adapter ARCH topics locked, two gaps surfaced:

1. **Formatting rules incomplete**: `arch/<topic>.md` content structure NOT formally locked (de facto 18-section template from substrate → adapter; never codified). DR template NOT formally locked (convention from archive; "Pattern note (meta)" sections crept in violating Lens 5 v0.2.1).
2. **Memory stuffing**: 19 memory feedback files; ~14 are disciplines or architectural commitments that absorbed-content homes already exist for, but weren't moved.

User direction: "we need to vcreate clear interconnected docs or expand clarify exiting ones... move as much out of memories as is sensible... if you well like meta infomrtaion is relevant that shuold probably (lets deciede) go into decsion records."

## Decision

Three locks comprise this composite:

### Lock 1: arch/<topic>.md template (Pattern A protocol topic)

Lock 18-section template established by `arch/substrate.md` + validated by `arch/adapter.md`. Persisted in `MAINTENANCE.md` 5-layer model Layer 3 description.

Pattern A protocol topic template:
1. Topic scope + frontmatter
2. Surface contract (architectural-level)
3. Common-surface boundary criteria
4. Per-implementation aspect
5. Selection mechanics
6. Tri-aspect reconciliation
7. Composition with framework primitives
8. Substrate-internal vs skill-side audit emission
9. Cardinality + lifecycle
10. Boot + shutdown phase ordering
11. Substrate error categories
12. Transport variation + per-tier mapping (where applicable)
13. Deployment-tier awareness
14. Pre-implementation operational concerns (Phase 6 forward reference)
15. Watch-list
16. Decision-design provenance (archived sources only; meta-provenance moves to DR)
17. Phase routing
18. Cross-references

Future Pattern B / C / cross-cutting integrator topic templates locked when first instance lands (foundation-up; substrate established Pattern-A template via first-Pattern-A topic).

**Provenance hygiene** (per coherence-audit Lens 5 v0.2.1): ARCH topics hold pure architectural content. Provenance lives in HANDOFF + git log + commit messages + DRs (Sharpening provenance section per Lock 2).

### Lock 2: DR template

Lock DR template in `MAINTENANCE.md` 5-layer model Layer 4 description.

Sections:
1. Status
2. Owner
3. Related
4. Context
5. Decision
6. **Sharpening provenance** (the meta-home — absorbs Round-by-Round trajectory + counts + manufactured-criticism rejections + GLOSSARY back-check verdict + profile-anchored validation citations + decomposition mode)
7. Composition with existing architecture
8. Constraints flowing to downstream commitments
9. Files touched
10. Revisit triggers

Resolves where process narrative belongs per coherence-audit Lens 5 v0.2.1: provenance in HANDOFF + git log + commit messages + DRs; NOT in ARCH topics or canonical content.

### Lock 3: Memory consolidation

19 memory feedback files → 5 retained + 14 migrated to absorbed homes:

| File | Absorbed home |
|---|---|
| `feedback_source_grounded.md` | DISCIPLINES.md Discipline 1 |
| `feedback_vision_arch_grounding.md` | DISCIPLINES.md Discipline 1 (re-grounding sub-section) |
| `feedback_skill_files_are_sources.md` | DISCIPLINES.md Discipline 1 (skill+profile sub-section) |
| `feedback_apply_principle_uniformly.md` | DISCIPLINES.md Discipline 2 |
| `feedback_pre_decision_sharpening.md` | DISCIPLINES.md Discipline 3 |
| `feedback_multi_axis_validation.md` | DISCIPLINES.md Discipline 3 (multi-axis sub-section) |
| `feedback_foundation_up_ordering.md` | DISCIPLINES.md Discipline 8 |
| `feedback_pattern_not_instance_defers.md` | MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §2 (no-defer + pattern-vs-instance + D Gate consolidated) |
| `feedback_wrong_shapes_impossible.md` | MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §1 |
| `feedback_preliminary_lock.md` | MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES §3 |
| `feedback_dev_vs_app_skills.md` | MAINTENANCE.md TOP-LEVEL SCOPE |
| `feedback_ai_as_runtime.md` | ARCHITECTURE.md cross-cutting principles "AI as runtime, not AI as consumer" |
| `feedback_llm_instruction_tightness.md` | ARCHITECTURE.md cross-cutting principles "LLM-instruction tightness" |
| `feedback_full_monty_upfront.md` | DISCIPLINES.md Discipline 3 (already retired session 16; consolidated into pre-decision-sharpening) |

Memory dir retains 5 files (genuine cross-session AI behavioral preferences):
- `feedback_propose_before_commit.md`
- `feedback_judgment_and_automate.md`
- `feedback_push_after_commit.md`
- `feedback_blocked_actions.md`
- `feedback_plugin_marketplace_clone_sync.md`

**Discriminator** for "absorb vs retain in memory": tied to specific tool / decision-procedure / sharpening-cycle / cascade-action → DISCIPLINE (DISCIPLINES.md home); tied to general AI-behavior preference irrespective of specific procedure → BEHAVIORAL (memory home); architectural commitment about HOW the framework is designed → MAINTENANCE.md / ARCHITECTURE.md home.

## Sharpening provenance

### Round 1 (sharpen v0.9.0; user-triggered after framing question)

User raised the gap: "do we not have clear formating rules for arch/* and architecture md and glossary? if not lets discuss how to mitigate. and i dont wnat to keep stufing memories."

AI surfaced 3 open questions for discussion (cut from initial 5 per first round of refinement):
- A. MAINTENANCE.md vs ARCHITECTURE.md for architectural-commitment files
- B. Memory pattern: directive-content vs directive-pointer (hybrid)
- C. arch/<topic>.md template home: MAINTENANCE.md vs new docs/templates/

### Round 2 (sharpen v0.9.0; user-triggered)

Round 2 sharpened own Round 1 proposal. Key findings:

**A. Per-file home decision (NOT one-size-fits-all)**: The 6 "architectural-commitment" files are 4 different kinds:
- META-DESIGN-PRINCIPLES (universal): wrong-shapes / pattern-not-instance / preliminary-lock → MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES
- SCOPE RULE: dev-vs-app-skills → MAINTENANCE.md TOP-LEVEL SCOPE
- ARCHITECTURAL COMMITMENT (PBS-specific): ai-as-runtime → ARCHITECTURE.md cross-cutting principles
- DISCIPLINE (about HOW we author Mode 1 content): llm-instruction-tightness → ARCHITECTURE.md cross-cutting principles (alongside Logic placement modes)

**B. NOT hybrid — plain consolidation**: Round 1's "auto-load tradeoff" was overclaim. Re-checking auto-memory mechanism: only MEMORY.md INDEX one-liner auto-loads; individual feedback file CONTENT does NOT auto-load. Therefore migration of content from memory file → DISCIPLINES.md has NO loading-behavior loss. Memory dir retains only files with genuinely-loose-behavioral-preference content; absorbed files deleted outright.

**C. MAINTENANCE.md (both templates)**: arch/<topic>.md template + DR template both go in MAINTENANCE.md as expanded Layer 3 + Layer 4 descriptions of the 5-layer doc model. Reject docs/templates/ indirection (only 2 templates; doesn't justify directory).

**Cognitive-mode catch (mechanism-simulation pass)**: Cascade-scan procedural step missing from earlier proposal. Each migration requires `git grep "feedback_<name>.md"` before each migration commit; update all hits in same commit.

### Manufactured-criticism rejections

- "Should adapter be 'multi-instance Pattern A' as new META-classification?" → REJECT (inflates primitive count; Pattern A admits cardinality variation per locked GLOSSARY)
- "Hybrid pattern preserves auto-load while content consolidates?" → REJECT (Round 2 self-correction; auto-load tradeoff was overclaim — only MEMORY.md INDEX auto-loads, not feedback file content; hybrid pattern doesn't add value)

### GLOSSARY back-check (per Round 2 termination)

No glossary-grade structural facts surfaced. Migration is doc-organization mechanics, not vocabulary refinement. Clean.

### Profile-anchored validation

NOT applicable — this is doc-system meta-work, not architectural primitive design. Profile-anchored validation reserved for high-impact decisions (primitive classifications; per-protocol design).

### Decomposition mode

Mode-2 composite (upfront-known): 3 sub-decisions visible at framing time with foundation-up dependencies (Lock 1 + Lock 2 templates land independently; Lock 3 memory consolidation depends on Locks 1-2 having absorbed-content homes ready). Single composite DR captures all 3.

## Composition with existing architecture

- **MAINTENANCE.md TOP-LEVEL DESIGN PRINCIPLES** (NEW section): META-design rules previously scattered across memory feedback files now consolidated. Three principles: wrong-shapes-impossible / pattern-vs-instance + no-defer + D Gate / preliminary-lock.
- **MAINTENANCE.md Layer 3 + Layer 4** (expanded): templates for arch/<topic>.md + DR persistence.
- **DISCIPLINES.md Discipline 1** (sharpened): absorbs source-grounded + vision-arch-grounding + skill-files-are-sources as sub-sections.
- **DISCIPLINES.md Discipline 3** (sharpened): absorbs pre-decision-sharpening full content + multi-axis validation sub-section + profile-anchored validation sub-section.
- **DISCIPLINES.md Discipline 8** (NEW): foundation-up workflow ordering.
- **ARCHITECTURE.md cross-cutting principles** (expanded): "AI as runtime, not AI as consumer" + "LLM-instruction tightness for Mode 1 markdown layer" sections.
- **MEMORY.md** (slimmed): 5 retained behavioral-preference entries + migration record.
- **All cross-refs in DRs / ARCH topics / drafts / learnings / HANDOFF / CLAUDE.md / profiles** updated via cascade-scan from `feedback_<name>.md` references → absorbed location references.

## Constraints flowing to downstream commitments

- **Future ARCH topic content**: must follow Pattern A protocol topic 18-section template per MAINTENANCE.md Layer 3 description. Sparring / audit / coordination / trust / time topics next; reuse template directly.
- **Future DRs**: must follow DR template per MAINTENANCE.md Layer 4 description. Sharpening provenance section IS the meta-home — no "Pattern note (meta)" / sharpening trajectory in ARCH topics.
- **Future memory feedback proposals**: discriminator (behavioral preference vs discipline vs architectural commitment) determines home BEFORE writing memory file. Default to absorbed-content home; memory only when behavioral-preference shape applies.
- **Cascade discipline**: each future DR / ARCH topic / discipline change cascades cross-refs across affected files via `git grep` + per-file update in same commit.

## Files touched

- `MAINTENANCE.md` — NEW TOP-LEVEL DESIGN PRINCIPLES section (3 principles: wrong-shapes / pattern-not-instance + no-defer + D Gate / preliminary-lock); expanded Layer 3 (Pattern A protocol topic template); expanded Layer 4 (DR template); updated Memory composition section
- `DISCIPLINES.md` — sharpened Discipline 1 (absorbed source-grounded + vision-arch-grounding + skill-files-are-sources); sharpened Discipline 2 (apply-principle-uniformly); sharpened Discipline 3 (pre-decision-sharpening + multi-axis-validation + profile-anchored-validation); NEW Discipline 8 (foundation-up workflow ordering); slimmed Memory composition section
- `ARCHITECTURE.md` — added cross-cutting principles "AI as runtime, not AI as consumer" + "LLM-instruction tightness for Mode 1 markdown layer" sections
- `MEMORY.md` (auto-memory) — slimmed to 5 retained entries + migration record
- 14 memory files deleted from `~/.claude/projects/.../memory/` (auto-memory dir)
- 25+ files cross-ref-updated via batch sed: HANDOFF.md / BACKLOG.md / GLOSSARY.md / CLAUDE.md / profiles/INDEX.md / arch/substrate.md / arch/adapter.md / docs/decisions/*.md / drafts/execution-fidelity.md / drafts/composability-tooling.md / learnings/ai-app-development.md / plugin/skills/*/SKILL.md
- `docs/decisions/doc-organization-templates.md` (this file; NEW; status ACCEPTED)
- `HANDOFF.md` Note 37

## Revisit triggers

- New doc class added to corpus (new template needed)
- Pattern B / C / cross-cutting integrator topic first instance lands → that template gets locked alongside (per Lock 1 future-templates clause)
- A retained memory file's content sharpens to where it fits absorbed-content shape → migrate per discriminator
- Coherence-audit Lens 5 provenance hygiene catches any new "Pattern note (meta)" creep in ARCH topics → cascade-fix to DR Sharpening provenance section
- New skill written → its description gets the READ-FIRST directive prepended per Note 34 procedural-fidelity discipline
