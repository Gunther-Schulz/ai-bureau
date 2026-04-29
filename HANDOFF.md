# Session handoff — pbs-bureau

End of session 2026-04-29 (fifth major session, **extended scope**
after design-review on load-bearing foundations recommended a
substantial pre-launch refactor — user authorized "do the whole
refactor in the right sequence now").

This session is the largest pre-RAG cleanup the system has had.
It executed the full Path-2 / Path-3 / Path-1 / orchestrator-split
/ meta-infra-cleanup sequence per the design-review artifact at
`docs/design-reviews/foundations-20260429.md`.

**The system is now structurally simpler at every level**:

- **4 meta-rules + 1 named layering convention** (was 5)
- **5 entity types** (was 9; A-I letter scheme dropped)
- **3 decision rules** (was 6)
- **office-config v3** schema (was v2; consolidates office+identity,
  paths→roots, practices+partners→actors, drops derived extensions
  block, free-form integrations list)
- **18 skills migrated** to extended frontmatter (summary, routing_mode,
  triggers, handoffs, phase_role)
- **Watch-list logic extracted** from orchestrator into its own skill
  with explicit data model + decay rules
- **Decision records extracted** from backend-conventions to per-decision
  files under `docs/decisions/`

After Phase 0 items 1+2 in the previous HANDOFF (meta-audit +
plugin-conventions) and the design-review skill itself, this
session executed Phase 0 item 3 (architectural simplification —
the design-review's CC1) plus several other cross-cutting Reshapes.

**Phase 0 item 4 (testing methodology + harness) is the next-session
task** — discussion-first per user's earlier directive.

---

## Read order for next session

1. **This file (HANDOFF.md)** — current state
2. **`ARCHITECTURE.md`** — **v0.5** post-design-review simplification.
   4 meta-rules + scope-orthogonality layering convention. 5 entity
   types (Skill Bundle, Memory, Backend, Configuration, External Data).
   3 decision rules (audience-first). Deprecation procedure. **Read
   this fully if anything looks unfamiliar.**
3. **`VISION.md`** — three-axis thesis (unchanged)
4. **`docs/rag-pipeline-decisions.md`** — ACCEPTED post-audit;
   Phase 0/1/2a/2b/3a/3b/4 phasing
5. **`docs/design-reviews/foundations-20260429.md`** — design-review
   first-run artifact (frozen snapshot); the source of this session's
   refactor recommendations
6. **`docs/plugin-conventions.md`** — Skill Bundle idioms (frontmatter
   contract now extended with summary/triggers/handoffs/phase_role)
7. **`docs/backend-conventions.md`** — Backend idioms (alternatives +
   revisit triggers extracted to docs/decisions/)
8. **`docs/decisions/`** — per-decision records (3 backend decisions
   extracted from backend-conventions; mirrors rag-pipeline-decisions
   pattern)
9. **`docs/audits/`** + **`docs/audit-pre-rag.md`** — frozen audit
   artifacts
10. **`ROADMAP.md`** — deferred work
11. **`plugin/skills/orchestrator/{SKILL,PROCEDURE}.md`** — 0.9.0;
    watch-list delegated; §11/§12 delegated to specialists; "loaded
    means active" softened; 3-phase model declared
12. **`plugin/skills/watch-list/`** — NEW; T1-T6 watch-list with
    explicit data model + decay rules
13. **`plugin/skills/{audit,design-review}/`** — meta-infrastructure
    skills

---

## Status snapshot — what landed this session (extended)

### ✅ Audit work (4 rounds)

3 parallel slice agents per round. 12 + 12 + 6 + 14 findings; 3
BLOCKERS caught (legacy `global | domain | project` scope vocab
in backend docs + live ingest code).

Permanent record: `docs/audit-pre-rag.md`. All findings closed in
commits `ad01b18` (F-batch) + `488cfc7` (meta-audit + rounds 3/4
batch).

### ✅ U1 + U2 + plugin-conventions

- `docs/rag-pipeline-decisions.md`: alternatives + revisit triggers
  backfilled across all decision sections (commit `d0f3f91`)
- `docs/backend-conventions.md`: test layout + logging + MCP error
  format (commit `501eaa1`)
- `docs/plugin-conventions.md`: Type A/B idioms (commit `c67c73a`)

### ✅ audit skill (commit `ce82713`)

`plugin/skills/audit/` codifies the 4-round drift-sweep procedure
proven across the audit work. SKILL.md + PROCEDURE.md + 3 reference
files (drift surfaces + slice library, triggers + stopping criterion,
output conventions). Future audit artifacts land at
`docs/audits/<scope>-<YYYYMMDD>.md`.

### ✅ design-review skill (commit `12d8286`)

`plugin/skills/design-review/` codifies first-principles soundness
review with anti-status-quo bias mechanism (greenfield reframe).
SKILL.md + PROCEDURE.md + 3 reference files (anti-bias mechanism +
5-category framework, scope + load-bearing first-run targets, output
conventions). Sibling to audit (compliance vs. soundness — distinct
cognitive tasks; preserve split position).

### ✅ design-review first run on foundations (commit `973bccf`)

`docs/design-reviews/foundations-20260429.md` — first real run of
the design-review skill on the load-bearing foundations. 6 parallel
subagents; 3 "Rough and worth refining" verdicts, 1 "Refactor with
conviction", 1 "Refactor with 2 Reshapes", 1 "Rough but adequate
with 2 Reshapes". 5 cross-cutting recommendations identified
(CC1-CC5).

This artifact is the source of all Path-1/2/3/orchestrator-split/
meta-infra recommendations.

### ✅ Path 2 — Office-config v2 → v3 (commit `efc4a1a`)

Per Subsystem 5 Reshapes:

- **Merged `office` + `identity`**: all identity fields now live
  under `office:` block
- **Merged `practices` + `partners` → `actors[]`** with
  `kind: internal|external` discriminator
- **`paths` → `roots`** with shorter field names (state, references,
  projects, local_repos); added `office_style_dir` + `office_extensions`
- **Dropped `extensions:` block entirely** — manifests now discovered
  by walking `<repo>/extensions/` (and `roots.office_extensions/` if
  set) filtered by scope
- **Free-form `integrations` list** (was fixed-key map of
  email/calendar/scanner/phone/accounting); class set is open

Schema migration v2 → v3 (`office_config_migrations/v2_to_v3.py`)
forward-migrates existing offices transparently. Backend Pydantic
models, helper methods (`find_actor_by_email`, `default_internal_actor`,
`find_integration`), config.py manifest discovery, integrations loader,
discovery.py MCP tool, projects.py + build.py callsites — all updated.

Skill body updates: setup-office (full v3 wizard rewrite + skill
body), draft-cover-mail, survey-project, verify-citations,
orchestrator/{SKILL,PROCEDURE}.md, memory/universal/* docs,
plugin/CLAUDE.md, README.md, docs/plugin-conventions.md, ROADMAP.md.

5 skill version bumps.

### ✅ Path 3 — Frontmatter migration to all 18 skills (commit `d2571ee`)

Per Subsystem 4. Added 5 new supplementary frontmatter fields to
every skill (description stays canonical Claude-Code-readable):

- `summary` — 1-2 sentence what-and-when
- `routing_mode` — direct | delegated | always_active
- `triggers[]` — structured list of `{phrase, lang}` pairs
- `delegated_from[]` — when routing_mode=delegated
- `handoffs[]` — explicit declaration of which skills this hands off to
- `phase_role` — controlled enum (routing/phase_a_entry/phase_b_entry/
  layer_1/2/3/bureau_setup/manifest_authoring/lifecycle/meta/utility)

Backend `SkillInfo` Pydantic + `tools/discovery.py:list_skills` updated
to parse + return new fields. Future audit slice can detect
description/triggers drift + handoff rename drift.

18 skill version bumps + plugin-conventions §1 rewrite documenting
the new fields.

### ✅ Path 1 — ARCHITECTURE.md v0.5 simplification (commit `dbcc84b`)

The big one. Per CC1 (architectural simplification pass).

**Meta-rules: 5 → 4 + 1 named convention**:
1. App vs office (deployment portability) — absorbs integration
   adapter pattern as Mechanism subsection
2. Memory vs RAG (citation freshness) — unchanged
3. **Source-of-truth & invalidation** (NEW) — every entity declares
   its invalidation contract
4. Execution determinism (renamed from execution locality) —
   absorbs Backend organization subsection

Plus named layering convention: **Scope orthogonality
(universal × domain × state)** — demoted from meta-rule status; it's
a layering pattern within layered content, not a placement axis.

**Entity types: 9 → 5** (A-I letter scheme dropped):
- Skill Bundle (was A + B; references are chapters of the bundle)
- Memory (was C + D; sub-kinds: prose + records)
- Backend (was E + I; integration adapters are an internal pattern)
- Configuration (was G + H; sub-kinds: office-config + scope-keyed
  manifests)
- External data (was F)

**Decision rules: 6 → 3 audience-first**:
- Rule 1: Is this consumed by Claude at runtime as behavior?
- Rule 2: Is this Python?
- Rule 3: Then by mutability (prose / record / config / external)

Plus deprecation procedure added to Maintenance discipline.

Cross-doc updates: README, plugin/CLAUDE.md, plugin-conventions,
backend-conventions, rag-pipeline-decisions, ROADMAP, backend
README, schemas.py, orchestrator SKILL+PROCEDURE, audit + design-review
references — all updated to new entity-type names + meta-rule
numbers.

### ✅ Watch-list extraction (commit `7754bf4`)

Per Subsystem 3 — orchestrator split, starting with watch-list.

New skill `plugin/skills/watch-list/` with:
- SKILL.md (routing_mode delegated; admin-phrase routing for
  inspection)
- PROCEDURE.md (7 checkpoints — explicit data model, queue +
  TTL + dedup + per-session caps, four-way decision menu, T6
  auto-backlog special case, session-end decay)
- references/triggers.md (T1-T6 catalog)

Orchestrator's PROCEDURE.md §2-§3 condensed to delegate (saves ~70
lines). T6 capability-gap auto-creates backlog entry instead of
surfacing menu.

### ✅ Other orchestrator changes (commit `2582759`)

Subsystem 3 finish:

- **Dropped §9 MCP fallback tables** — duplicate of frontmatter;
  `list_skills()` is authoritative (~70 lines saved)
- **Condensed §11 (binding) + §12 (new-project)** — full logic
  delegated to survey-project + setup_project MCP tool
  contracts (~60 lines saved)
- **Softened §13 conversational style** — extracted cross-skill
  conventions to `docs/plugin-conventions.md` §12
- **Softened "loaded means active, never bypass"** → "auto-loads
  when in scope; specialists own their own invariants"
- **Declared 3-phase workflow model explicitly** at top of PROCEDURE.md
  (Phase A drafting → Phase B review → Phase C finalize)

### ✅ Meta-infra cleanup (commit `790178f`)

Subsystem 6 R5: extracted alternatives + revisit triggers from
`backend-conventions.md` to per-decision records under
`docs/decisions/`:
- `backend-test-layout.md`
- `backend-logging.md`
- `backend-mcp-error-format.md`

backend-conventions.md sections now contain only "how to write" +
one-line pointer to the decision record. Conventions stay scannable
as the system grows.

plugin-conventions.md had no Alternatives/Revisit blocks (clean
already).

(Maintenance discipline → checklist + deprecation procedure already
landed in v0.5 ARCHITECTURE.md rewrite.)

### ⏸️ Subsystem 3 deferred work — full orchestrator split

Watch-list extraction landed (smallest piece per my committed
position). Full orchestrator split (router + watch-list + gates +
project-lifecycle skills) — remaining gates extraction (compile
gate, send gate, state-transition gate as separate skills) is a
larger reshape. Defer to next major architectural session OR
when a gate's logic surface grows beyond what fits in
orchestrator/PROCEDURE.md.

### ✅ Audit slices 11-13 — implementation-quality (commit-pending)

Added to `plugin/skills/audit/references/drift-surfaces-and-slices.md`
in audit v0.3.0:

- **Slice 11 — test-coverage**: tests covering load-bearing
  handlers / chunkers / migrations
- **Slice 12 — security / data-handling**: SQL escape, input
  validation, secret handling, path traversal
- **Slice 13 — performance / efficiency**: hot-path complexity,
  embedder loading, LanceDB query patterns, caching

These are **not part of the default round sequence** (slices 1-10
remain default). Run 11-13 before phase boundaries that increase
exposure on those axes — e.g., before Phase 1 corpus download =
slice 11.

Audit skill version 0.2.0 → 0.3.0.

### ⏸️ U3 — fresh-eyes review of VISION + ARCHITECTURE wording

Still deferred per earlier user decision. ARCHITECTURE.md was
substantially rewritten this session (v0.5 simplification); the
VISION fresh-eyes review still pending.

---

## ⏳ Pending — next-session tasks

### First action: trigger v2 → v3 office-config migration

The user's existing `~/.config/pbs-bureau/office.yaml` is at v2.
Backend forward-migrates transparently in memory on every load,
but the file on disk is permanently v2 (and now drifts from the
in-memory shape — `practices: []` + `paths.X_root` etc. on disk
vs. `actors: []` + `roots.X` in code).

**Action**: run `setup-office` in **reconcile mode** to persist
v3 to disk. Cleaner state + tests the v2_to_v3 migration we just
shipped (which has only been exercised by the loader's in-memory
forward-migration so far; reconcile mode is the persistence path).

This is a **good test opportunity**: the migration is bounded,
the user has a real v2 file, and reconcile mode exercises both
the migration framework AND setup-office's "reshape detected;
walk newly-required fields" flow. Catches any v2_to_v3 bugs
before they're encountered post-launch.

### Phase 0 item 4 — Feature-survey skill design (NEW)

Per the design-review skill scope question raised at session-5
close: design-review covers **structural design quality**, not
**feature gaps** ("what's missing from the system that should
exist?") or **implementation quality** (test coverage, security,
performance).

Implementation-quality is now covered by audit slices 11-13
(test-coverage / security / performance — added in audit v0.3.0
this session). Feature-survey is still missing.

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

**Discussion-first** per user directive.

Per the user's specific concern: "if we have a limited RAG at first
with no vision how do we track what we need to ingest at a later
time (the pieces we will be missing)?"

Three layered concerns to design:

- **Coverage-gap tracking**: per-manifest-entry `coverage:` field
  schema (text/images/tables/graph + last_indexed + coverage_score).
  Chunkers self-report at ingest time. Rolls up to
  `<roots.references>/coverage-report.md`.
- **Ground-truth set**: `tests/ground_truth/legal-queries.yaml` with
  15-25 hand-curated query/expected-doc pairs. **User curates** these
  (Claude can scaffold candidates from existing memory references).
  Pytest test asserts top-5 reranked hits include expected doc.
- **Determinism + regression detection**: embedding seed pinned;
  reranker tie-break by ID. Baseline retrieval-quality scores stored;
  diff on chunker/model changes.

Output: `docs/rag-testing-strategy.md` documenting the three layers
+ acceptance criteria for each phase gate (e.g. "Phase 2b passes
when ground-truth set top-5 ≥ 70% relevance").

### Then — Phase 1 corpus download

After Phase 0 items 4 + 5 close. Fetch all 57 entries via
`research-references` full refresh. **No embeddings yet** — raw
fetch + checksum + manifest population only. Surfaces real corpus
shape (DRM/scanned/manual-discovery) before chunker code commits.

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis + pioneer instance |
| `ARCHITECTURE.md` | **v0.5**: 4 meta-rules + scope-orthogonality layering convention; 5 entity types; 3 decision rules; deprecation procedure |
| `ROADMAP.md` | Deferred work; pull-forward triggers; decision-recording convention |
| `docs/rag-pipeline-decisions.md` | ACCEPTED; Phase 0/1/2a/2b/3a/3b/4 phasing |
| `docs/plugin-conventions.md` | Skill Bundle idioms (frontmatter contract extended) |
| `docs/backend-conventions.md` | Backend idioms (decision records extracted) |
| `docs/decisions/` | NEW — per-decision records (3 backend) |
| `docs/audits/` | Audit artifacts |
| `docs/design-reviews/foundations-20260429.md` | Design-review first-run artifact |
| `docs/audit-pre-rag.md` | Frozen session-5 audit snapshot |
| `docs/office-config.schema.yaml` | **v3** schema |
| `plugin/.claude-plugin/plugin.json` | Plugin **v0.3.0** (will likely bump to 0.4.0 next session — orchestrator + watch-list reshape changes wiring) |
| `plugin/skills/` | 19 skills (was 18; watch-list added) |
| `plugin/skills/watch-list/` | **NEW** — T1-T6 with data model + decay rules |
| `plugin/skills/orchestrator/` | **0.9.0** — substantially simplified; watch-list delegated; §11/§12 delegated; 3-phase model declared |
| `plugin/skills/{audit,design-review}/` | Meta-infrastructure skills |
| `plugin/templates/office-style/` | default + PV-FFA + Wind + Naturschutz overlays |
| `extensions/{universal,domain/<X>,state/<X>}/` | 5 populated + 1 skeleton ref manifests; 2 doctype manifests |
| `memory/universal/per-project-memory/*.md` | Type C frontmatter (`references_used: []`) |
| `memory/bausteine/{universal,domain/<X>,state/<X>}/` | Bausteine landing site (still empty until Phase 4) |
| `backend/mcp-server/src/pbs_mcp/office_config.py` | **v3** Pydantic models |
| `backend/mcp-server/src/pbs_mcp/office_config_migrations/v2_to_v3.py` | NEW |
| `backend/mcp-server/src/pbs_mcp/{config,integrations}/...` | v3 manifest discovery + free-form integrations |
| `backend/mcp-server/src/pbs_mcp/tools/{discovery,projects,build,memory,ingest}.py` | All v3-aware |
| `~/.config/pbs-bureau/office.yaml` | PBS office config (will forward-migrate to v3 on next load) |
| `/mnt/data2t/hidrive/.../_ai-references/` | RAG corpus root (still empty; Phase 1 fills it) |
| `/mnt/data2t/hidrive/.../Projekte/` | All client projects |

---

## Skill versions snapshot (post-session)

| Skill | Version |
|---|---|
| orchestrator | 0.9.0 |
| setup-office | 0.5.0 |
| draft-cover-mail | 0.5.0 |
| validate-checklist | 0.4.0 |
| verify-citations | 0.4.0 |
| validate-latex-style | 0.4.0 |
| research-references | 0.4.0 |
| survey-project | 0.4.0 |
| save-baustein | 0.3.0 |
| validate-bausteine | 0.3.0 |
| record-feedback | 0.3.0 |
| promote-to-skill | 0.3.0 |
| draft-textteil-b | 0.3.0 |
| draft-textteil-c | 0.3.0 |
| review-draft | 0.3.0 |
| author-manifest | 0.3.0 |
| audit | 0.2.0 |
| design-review | 0.2.0 |
| watch-list | **0.1.0** (new) |
| plugin.json | 0.3.0 (likely 0.4.0 next session) |

---

## Working-style notes (carried + new)

1. **Audit + design-review pattern proven** — both skills' first
   real runs found substantive issues. Audit caught drift; design-
   review caught structural simplification opportunities. Use
   them at phase boundaries.
2. **The refinement loop matters** — for every plan/proposal,
   apply 5-category framing (drop bloat / add missing / reshape
   wrong-shape / surface anchoring / reverse manufactured criticism|
   restraint). Memory captures: `feedback_refine_pareto.md`,
   `feedback_defer_instinct.md`.
3. **Greenfield reframe is the only mechanism** that catches
   deep design issues — wrong-shape abstractions, missing concepts,
   anchoring escape. Without it, review collapses to incremental
   critique under incumbent advantage.
4. **The user is the cross-check** in interactive mode — pushback
   ("why?") is the corrective force. Don't add agent layers to
   substitute for it.
5. **Pre-launch is the unique window** for radical reshapes.
   Stage-awareness baked into design-review skill (revisit at
   first user-facing release).
6. **Commit between batches** — many commits this session, one
   per coherent change. Lets sanity-check progressively and
   rollback selectively. Push after every commit per memory.
7. **Frontmatter changes are behavior changes** — minor bump per
   plugin-conventions §3.
8. **MCP tool naming**: snake_case matching `pbs_core` Python
   function name.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Plugin cache symlink**: re-run `bash dev-link.sh` after this
  session — many skills bumped + plugin version may bump next
  session.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Office-config**: existing PBS office.yaml is at v2; will
  forward-migrate to v3 transparently on next backend load.
  setup-office reconcile mode prompts for any newly-required
  fields (none in v3 — it's all reshape, no required additions).
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md`
  - `feedback_judgment_and_automate.md`
  - `feedback_push_after_commit.md`
  - `feedback_refine_pareto.md`
  - `feedback_defer_instinct.md`

---

## What this session looked like (commits, in order)

| # | Commit | Theme |
|---|---|---|
| 1 | `ad01b18` | audit: pre-RAG architectural audit + F1–F9 fix-now drift batch |
| 2 | `d0f3f91` | docs/rag-pipeline-decisions: backfill alternatives + revisit triggers (U1) |
| 3 | `501eaa1` | docs/backend-conventions: test layout + logging + MCP error format (U2) |
| 4 | `ec143fd` | HANDOFF (premature) |
| 5 | `488cfc7` | audit: meta-audit + rounds 3/4 fix-now batch (3 BLOCKERS + 18 drift) |
| 6 | `c67c73a` | docs/plugin-conventions |
| 7 | `b50c211` | HANDOFF (also premature) |
| 8 | `ce82713` | audit skill |
| 9 | `12d8286` | design-review skill |
| 10 | `973bccf` | design-review first run on foundations |
| 11 | `efc4a1a` | Path 2: office-config v2 → v3 |
| 12 | `d2571ee` | Path 3: frontmatter migration (all 18 skills) |
| 13 | `dbcc84b` | Path 1a+1b+1c: ARCHITECTURE.md v0.5 simplification |
| 14 | `7754bf4` | Watch-list extraction |
| 15 | `2582759` | Other orchestrator changes (Subsystem 3 finish) |
| 16 | `790178f` | Meta-infra cleanup (decision records extracted) |
| 17 | (this commit) | HANDOFF: session 5 final close |

All pushed to origin/main.
