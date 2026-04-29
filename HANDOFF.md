# Session handoff — pbs-bureau

End of session 6 (2026-04-29, same-day continuation of session 5).
Session 5 closed with the largest pre-RAG cleanup the system had
seen (architectural simplification, schema v3, frontmatter
migration, orchestrator split — see prior commits `f3fe2d0` and
back). Session 6 ran a follow-up boundary-and-coupling refinement
pass:

- **Sharpened meta-rule 4** (LLM/Python boundary) with two
  refinements: typed-contract persistence test (loose markdown is
  skill-direct), explicit reuse direction (deterministic→MCP,
  interpretive→Skill Bundle reference). ARCHITECTURE v0.5 → v0.6.
- **Added audit slice 14** (boundary-adherence) + slice 15
  (invalidation-contract coverage). Audit skill 0.3.0 → 0.5.0.
  New drift surfaces 10 (placement) + 11 (invalidation-contract).
- **Added design-review target 7** (LLM/Python placement-soundness)
  + target 8 (VISION ↔ ARCHITECTURE coupling traceability).
  Design-review skill 0.2.0 → 0.4.0. Fixed pre-existing v0.5 drift
  in targets 1+2 (5/9 entity types + A-I scheme references).
- **Persisted v2 → v3 office-config migration** to disk via in-
  process `apply_migrations()` + Pydantic round-trip (zero defects;
  v2 backup at `~/.config/pbs-bureau/office.yaml.v2-backup`).
- **Landed 2a fix** (path_classification config block) as purely-
  additive optional in v3 — no schema bump. PathClassification
  Pydantic + classifier consults config first, falls back to
  hardcoded patterns. Kicked off after slice 14's first-run finding.
- **Ran first runs** of slice 14, slice 15, target 7, target 8.
  Surfaced 7 findings total across the 4; 1 in-session fix, 5
  ROADMAP entries, 1 pushed-back-on agent overreach.

The boundary work was driven by user observation: LLMs paper over
imprecise markdown instructions silently, so pre-launch is the
unique window to tighten the LLM-consumed layer. New feedback
memory captures this rationale
(`feedback_llm_instruction_tightness.md`).

---

## Read order for next session

1. **This file (HANDOFF.md)** — current state
2. **`ARCHITECTURE.md`** — **v0.6** post-session-6 boundary
   refinement. 4 meta-rules + scope-orthogonality layering
   convention. 5 entity types. 3 decision rules. Meta-rule 4
   sharpened (typed-contract test + reuse direction). Meta-rule 3
   prose sharpened (research-references vs validate-bausteine
   layered reading). **Read fully if anything looks unfamiliar.**
3. **`VISION.md`** — three-axis thesis (unchanged; explicitly
   verified in target 8 first run as the canonical "why" anchor)
4. **`docs/audits/`** — boundary-adherence-20260429.md (slice 14
   first run; 3 findings, 0 BLOCKERS, 1 in-session fix);
   invalidation-contract-20260429.md (slice 15 first run;
   2 findings, 0 BLOCKERS, agent's BLOCKER call rejected)
5. **`docs/design-reviews/`** — foundations-20260429.md (session 5
   artifact); vision-arch-coupling-20260429.md (target 8 first
   run; 5 findings including F2 "unified audit trail v1-scope
   decision pending user judgment")
6. **`docs/rag-pipeline-decisions.md`** — ACCEPTED; Phase 0/1/
   2a/2b/3a/3b/4 phasing
7. **`docs/plugin-conventions.md`** — Skill Bundle idioms
   (frontmatter contract extended)
8. **`docs/backend-conventions.md`** — Backend idioms (decision
   records extracted to docs/decisions/)
9. **`docs/decisions/`** — per-decision records
10. **`ROADMAP.md`** — deferred work; **5 new entries** added in
    session 6: dedupe_bausteine, record_baustein_use, manifest
    Pydantic models, axis-2 sparring structural promotion, unified
    audit trail v1-scope decision (boundary-placement 2a removed —
    landed in-session)
11. **`plugin/skills/orchestrator/`** — 0.9.0 (unchanged session 6)
12. **`plugin/skills/{audit,design-review}/`** — both bumped this
    session; new slices/targets in their references/
13. **`plugin/skills/watch-list/`** — 0.1.0 (unchanged session 6)

---

## What landed this session (session 6 detail)

### ✅ Boundary refinement (commit `986857d`)

ARCHITECTURE.md meta-rule 4 sharpened with two refinements
identified after the user's question "what does the LLM/Python
boundary actually look like, and is it audited?":

- **(A) Typed-contract persistence test**: durable state with a
  Pydantic + loader + cross-reference invariant goes through MCP;
  loose markdown (HANDOFF, prose memory, READMEs) is skill-direct.
  The test is contract enforcement, not file extension.
- **(B) Reuse direction (positive form)**: shared deterministic →
  MCP tool; shared interpretive → Skill Bundle reference. Was
  implicit in "skills compose, never reimplement"; now explicit.

Audit slice 14 (boundary-adherence) + design-review target 7
(LLM/Python placement-soundness) added to detect violations of
the sharpened rule. ARCHITECTURE v0.5 → v0.6. Audit 0.3.0 →
0.4.0. Design-review 0.2.0 → 0.3.0.

Slice 14 first run found 3 findings, 0 BLOCKERS — see
`docs/audits/boundary-adherence-20260429.md`. All 3 were
ROADMAPed; one (2a path_classification) later landed in-session
as additive v3 block.

### ✅ VISION ↔ ARCH coupling work (commit pending)

User question: "anything else in ARCHITECTURE.md or even VISION.md
we should cover similarly?" Two real gaps surfaced:

- **Gap A** — design-review target 8 (VISION/ARCH coupling
  traceability). First run produced bidirectional maps:
  - **Map 1 (VISION → ARCH)**: 6 axis-1 + 7 axis-2 + 5 axis-3
    mechanisms; classified `structural` / `behavioral` /
    `unenforced`.
  - **Map 2 (ARCH → VISION)**: each meta-rule's coupling to
    each axis; classified `load-bearing` / `supporting` /
    `floating`.
  - **5 findings** including F1 (axis-2 sparring structurally
    weak — all 7 mechanisms behavioral; highest-leverage gap),
    F2 (unified audit trail v1-scope decision pending user
    judgment), F3 (push-back on agent's "meta-rule 1 is
    overhead" claim — meta-rule 1 IS load-bearing for axes 1+3).
  - Artifact: `docs/design-reviews/vision-arch-coupling-20260429.md`.
  - Design-review 0.3.0 → 0.4.0. Fixed pre-existing v0.5 drift
    in targets 1+2 while in the file.

- **Gap B** — audit slice 15 (invalidation-contract coverage).
  First run found 2 findings, 0 BLOCKERS:
  - F1 reframed (rejected agent's BLOCKER call): no Pydantic
    model validates manifest YAML structure — contract is
    document-discipline only. All 8 current manifests honor
    contract; gap is forward-looking. ROADMAPed.
  - F2 informational: ARCHITECTURE.md prose obscured layered
    reading (research-references + validate-bausteine).
    Sharpened in-session.
  - Artifact: `docs/audits/invalidation-contract-20260429.md`.
  - Audit 0.4.0 → 0.5.0. New drift surface 11.

### ✅ 2a fix landed in-session

`path_classification` optional block added to office-config v3
schema (no version bump — purely additive). PathClassification
Pydantic model + extended `Conventions`. `_infer_source_subtype`
now consults config first, falls back to hardcoded patterns for
canonical layout. Verified existing v3 office.yaml loads cleanly
without the new block; classifier produces same results as before
when block is absent. Schema doc updated.

### ✅ v2 → v3 office-config migration persisted

PBS office-config persisted to v3 via in-process
`apply_migrations(v2, target=3)` + Pydantic round-trip
validation. v2 backup at `~/.config/pbs-bureau/office.yaml.v2-backup`.
1 internal + 1 external actor (was practices + partners), 0
integrations (all v2 had `adapter: none`, dropped per migration).

### ✅ Memory addition

New feedback memory `feedback_llm_instruction_tightness.md`
capturing the rationale for prioritizing markdown-layer
sharpening pre-launch. The asymmetric brittleness argument:
LLMs paper over imprecise markdown silently; deterministic
Python self-fails. Bias toward sharpening the LLM-consumed
layer when pre-launch.

---

## ⏳ Pending — next-session tasks

### F2 follow-up — unified audit trail v1-scope decision

Target 8 first run named this as a user-judgment call (axis 3's
defensibility test depends on unified audit-trail reconstruction;
today scattered across 6 sources with no query layer).

**Options**:
- (a) Keep deferred — defensibility relies on manual assembly
  until ROADMAP "Audit trail — unified change/decision/version
  tracking" lands. Acceptable pre-launch.
- (b) Pull forward to v1 — design + build unified Memory (record)
  subkind with query layer. Multi-day work. Closes axis-3
  structural gap.

Awaiting user judgment. Revisit before any axis-3-stress event
(first real Stellungnahme defense, first historical project
replay).

### Phase 0 item 4 — Feature-survey skill design

Per session-5 close: design-review covers structural design
quality, not feature gaps ("what's missing from the system that
should exist?"). Implementation-quality is now covered by audit
slices 11-13; placement is now covered by slice 14; invalidation
is now covered by slice 15. Feature-survey is still missing.

**Build a `feature-survey` skill** with:
- Mechanism: greenfield-the-vision (vs. design-review's
  greenfield-the-architecture). Asks "given the user's goals
  and the system's purpose, what features should exist that
  don't?"
- Slice library: feature gaps per axis (workflow gaps, UX gaps,
  data-model gaps, integration gaps, observability gaps,
  collaboration gaps, lifecycle gaps).
- Output format: per-gap recommendation with priority + cost
  + alignment-with-VISION.md.

Same pattern as audit + design-review (parallel slice agents +
synthesis + frozen artifact). Discussion-first; expect ~half-day
to design well.

### Phase 0 item 5 — Testing methodology + harness

**Discussion-first** per user directive. Three layered concerns:

- **Coverage-gap tracking**: per-manifest-entry `coverage:` field
  schema (text/images/tables/graph + last_indexed +
  coverage_score). Chunkers self-report at ingest time. Rolls up
  to `<roots.references>/coverage-report.md`.
- **Ground-truth set**: `tests/ground_truth/legal-queries.yaml`
  with 15-25 hand-curated query/expected-doc pairs. **User
  curates**; Claude can scaffold candidates from existing memory
  references. Pytest test asserts top-5 reranked hits include
  expected doc.
- **Determinism + regression detection**: embedding seed pinned;
  reranker tie-break by ID. Baseline retrieval-quality scores
  stored; diff on chunker/model changes.

Output: `docs/rag-testing-strategy.md` documenting the three
layers + acceptance criteria for each phase gate.

### Then — Phase 1 corpus download

After Phase 0 items 4+5 close. Fetch all 57 entries via
`research-references` full refresh. **No embeddings yet** — raw
fetch + checksum + manifest population only. Surfaces real
corpus shape (DRM/scanned/manual-discovery) before chunker code
commits.

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis (canonical "why") |
| `ARCHITECTURE.md` | **v0.6**: meta-rule 4 sharpened with typed-contract test + reuse direction; meta-rule 3 prose layered-reading sharpened |
| `ROADMAP.md` | Deferred work; pull-forward triggers; **5 new entries this session** |
| `docs/audits/boundary-adherence-20260429.md` | Slice 14 first-run; 3 findings, 1 in-session fix |
| `docs/audits/invalidation-contract-20260429.md` | Slice 15 first-run; 2 findings |
| `docs/design-reviews/vision-arch-coupling-20260429.md` | Target 8 first-run; 5 findings |
| `docs/design-reviews/foundations-20260429.md` | Session-5 design-review |
| `docs/audit-pre-rag.md` | Frozen session-5 audit snapshot |
| `docs/office-config.schema.yaml` | **v3** schema with new optional `conventions.path_classification` block |
| `plugin/skills/audit/` | **0.5.0** — slices 1-15; surfaces 1-11 |
| `plugin/skills/design-review/` | **0.4.0** — targets 1-8 + focused-mode targets |
| `plugin/skills/orchestrator/` | 0.9.0 (unchanged session 6) |
| `plugin/skills/watch-list/` | 0.1.0 (unchanged session 6) |
| `backend/mcp-server/src/pbs_mcp/office_config.py` | v3 Pydantic + new `PathClassification` model |
| `backend/mcp-server/src/pbs_mcp/tools/ingest.py` | `_infer_source_subtype` now config-aware with hardcoded fallback |
| `~/.config/pbs-bureau/office.yaml` | v3 (unchanged from session-6 open; path_classification optional, not declared) |
| `~/.config/pbs-bureau/office.yaml.v2-backup` | v2 backup from session-6 migration |

---

## Skill versions snapshot (post-session 6)

| Skill | Version | Change this session |
|---|---|---|
| audit | **0.5.0** | + slices 14, 15; + drift surfaces 10, 11 |
| design-review | **0.4.0** | + targets 7, 8; targets 1-2 drift fixed |
| orchestrator | 0.9.0 | (unchanged) |
| setup-office | 0.5.0 | (unchanged) |
| watch-list | 0.1.0 | (unchanged) |
| (others) | (unchanged) | |
| plugin.json | 0.3.0 | (will likely bump 0.4.0 next session — orchestrator + watch-list reshape from session 5; not bumped session 6) |

---

## Working-style notes (carried + new)

1. **Boundary work + coupling work were the right pre-launch
   detour.** Started as "let's just understand the LLM/Python
   boundary" (user observation), expanded to a coherent
   meta-infrastructure tightening pass: target 7 + slice 14 (the
   boundary itself), target 8 + slice 15 (the next layers up,
   surfaced because the boundary work surfaced them). User's
   "anything else?" question after slice 14 was the
   leverage-multiplier prompt.

2. **Agent push-back happened twice in this session** — target 8
   first run mis-classified meta-rule 1; slice 15 first run
   mis-classified the manifest schema as a BLOCKER. Both caught
   by human cross-check. The pattern: agents do solid evidence-
   gathering but can over-state verdicts. Always read the
   evidence before accepting the conclusion.

3. **Pareto-refinement caught a real schema-bump avoidance**.
   Original 2a plan was v3 → v4 migration; refinement found that
   `path_classification` could be purely additive optional in v3.
   Saved ~2h + removed migration risk. The challenge "why is
   this the most aggressive change?" did the work.

4. **Memory captures**: new feedback memory
   `feedback_llm_instruction_tightness.md` makes the
   markdown-vs-Python brittleness asymmetry reusable for future
   prioritization decisions.

5. **Carried**: refine-Pareto, defer-instinct-restraint,
   judgment-and-automate, push-after-commit, blocked-actions —
   all still apply.

---

## Session 6 commit list (chronological)

| # | Commit | Theme |
|---|---|---|
| 1 | `cefb5ab` | HANDOFF: swap Phase 0 items 4/5 — feature-survey before testing-methodology |
| 2 | `ea838cf` | HANDOFF: mark v2→v3 office-config migration done |
| 3 | `986857d` | boundary refinement v0.5→v0.6: meta-rule 4 sharpening + slice 14 + target 7 |
| 4 | (this commit) | VISION/ARCH coupling: target 8 + slice 15 + 2a fix + meta-rule 3 prose + memory + HANDOFF |

All pushed to origin/main.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **Plugin cache symlink**: re-run `bash dev-link.sh` after any
  plugin.json version bump. Session 6 didn't bump plugin.json.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Office-config v3** persisted; backup retained at
  `office.yaml.v2-backup`. New optional
  `conventions.path_classification` block defaults to empty;
  classifier falls through to hardcoded patterns for canonical
  layout.
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md`
  - `feedback_judgment_and_automate.md`
  - `feedback_push_after_commit.md`
  - `feedback_refine_pareto.md`
  - `feedback_defer_instinct.md`
  - `feedback_llm_instruction_tightness.md` **(new session 6)**
