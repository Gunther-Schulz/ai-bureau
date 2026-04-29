# Session handoff — pbs-bureau

End of session 2026-04-29 (fourth major session). Previous session
(2026-04-28) executed the `(universal × domain × state)`
**orthogonality refactor** (3rd meta-rule). This session executed
the **execution-locality meta-rule (5th)** + the entire **pre-RAG
work order** that the prior session queued: Tier 1 MCP discovery
tools, full skill-alignment sweep (13 skills), and the pre-RAG
architectural decisions doc with verdicts on multimodal storage,
legal §-graph at ingest, chunking strategy, and reference
versioning.

Plus this session created **VISION.md** as the deepest anchor —
the three-axis thesis (intertwined-AI-workflow + sparring partner
+ authorship preservation), foundations citing Vivienne Ming,
pioneer-instance positioning, and the operational checklists.

**Pre-RAG architectural work is now ~95% complete**. Only the
**audit gate** (task #21) remains before RAG kickoff.

**Read order for next session**:

1. **This file (HANDOFF.md)** — current state
2. **`VISION.md`** — three-axis thesis; pioneer-instance framing;
   sparring/trust/authorship infrastructure; checklists
3. **`ARCHITECTURE.md`** — vision anchor + 5 meta-rules + 9 entity
   types + 6 decision rules + Backend organization + worked
   examples
4. **`docs/rag-pipeline-decisions.md`** — pre-RAG decisions A–D +
   pipeline choices 1–3 (PROPOSED, awaiting audit confirmation)
5. **`ROADMAP.md`** — Tier 1/2/3 MCP work, knowledge-layer items,
   pioneer-instance validation strategy, decision-recording
   convention, etc.
6. **`docs/office-config.schema.yaml`** — schema v2 reference
7. **`plugin/skills/orchestrator/SKILL.md` + `PROCEDURE.md`** —
   updated this session for scope orthogonality + meta-rule 5
8. Whichever skill the user invokes

---

## Status snapshot — what landed this session

### ✅ Foundation: VISION.md (this session created)

Three-axis thesis (commit history: `519ed63` → `93668c0` →
`6ae58d1` → `294a314` → progressive refinement):

| Axis | Failure mode | PBS aim |
|---|---|---|
| Surface (workflow embedding) | Tacked-on AI features | Intertwined-AI-workflow |
| Process (interaction mode) | Answer machine / sycophant | Sparring partner |
| Purpose (outcome orientation) | Rubber-stamping | Authorship preservation |

Plus: **Foundations** section citing Vivienne Ming
(neuroscientist; *Robot-Proof*; AI-as-sparring-partner research)
as the alignment-check anchor for axis 2 + the underlying
capacity-atrophy concern motivating axis 3.

Plus: **PBS as pioneer instance** strategic framing — triple
purpose (working tool + proving ground + research lab); explicit
hierarchy among deployment possibilities (production+consulting
primary; sell-as-product secondary; SaaS distant); honest risks
of one-user pioneering; milestones (not terminal state).

Plus: three-axis checklists for "How to use this document" —
new-feature audit, frontend integration check, drift audit.

### ✅ Foundation: ARCHITECTURE.md v0.4 (commit `dbf5f74`)

- **Meta-rule 5 — execution locality** added (now 5 meta-rules
  total). Persistence-layer boundary; deterministic-vs-interpretive
  verdicts; enumeration-vs-selection corollary; static-path-blocks
  via settings.json permissions; **frontmatter dependency
  declarations** (`mcp_tools_required[]`, `mcp_tools_optional[]`,
  `fallback_when_mcp_absent`); MCP tool naming convention
  (snake_case = Python function name); hooks deferred until
  concrete need.
- **Backend organization** subsection (Type E internals):
  `pbs_core` (plain Python) + `pbs_mcp/tools/` (thin wrappers)
  discipline starts now; physical split deferred until first
  non-MCP frontend (web UI is the load-bearing trigger).
- **Vision anchor** at top of doc, pointing at VISION.md; every
  meta-rule + decision rule traces back.
- New worked example added (save-baustein declares
  `mcp_tools_required` in frontmatter per meta-rule 5).

### ✅ Backend: Tier 1 MCP discovery tools (commit `6865a93`)

5 new MCP tools (per ROADMAP "Backend MCP discovery layer"):

- `list_reference_manifests(scope_filter=true)` — wraps
  `cfg.all_references_manifests()`; returns
  `[{path, layer, scope_key, exists, entry_count, last_updated}]`
- `list_doctypes_manifests(scope_filter=true)` — same shape for
  doctype manifests
- `list_skills()` — reads `plugin/skills/*/SKILL.md` frontmatter;
  returns name/version/description/path + dependency declarations
- `list_skeletons(doctype)` — layered skeleton dirs (universal +
  per-active-domain overlays)
- Refactored `list_bausteine(scope, scope_key?, project_root?)`
  — scope-aware enumeration with new orthogonality semantics
  (universal/domain/state/project + scope_key); replaces legacy
  global/domain/project shape

Plus: **memory.py orthogonality refactor** — `baustein_path()`
+ `_enumerate_paths()` rewritten for new layered tree
(`memory/bausteine/{universal,domain/<X>,state/<X>}/<name>.md`).
SaveBausteinInput / GetBausteinInput / BausteinSummary all
updated for scope_key.

Smoke test green: 22 tools registered (was 17), 5 reference
manifests in scope (57 entries total: universal=10, PV-FFA=7,
Wind=6, Naturschutz=19, MV=15), 2 doctype manifests in scope,
16 skills enumerated, layered skeleton resolution works.

### ✅ Skills: full alignment sweep (commits `502f339` → `b90fa32` → `bd8a1e7` → `e495b55`)

All 16 PBS skills now aligned to post-orthogonality + meta-rule
5 architecture (3 already-aligned from prior session: setup-office
v0.2, research-references v0.2, author-manifest v0.1.0; 13 in
this session's 4-batch sweep).

**All 5 priority touchpoints** (HANDOFF "Five concrete refactor
touchpoints") refactored:

- **save-baustein** — dedupe guard via `list_bausteine` collision
  check; layered baustein paths + scope_key. Plus baustein-format
  extensions D + E (verified_against_version field;
  cross_project_visible flag).
- **verify-citations** — iterative per-citation resolution
  (replaces flat batch lookup); each verdict source-grounded by
  construction. Uses `verified_against_version` for baustein
  freshness.
- **validate-checklist** — reference-fetch enrichment (each
  checklist hit fetches the actual reference defining the
  requirement, not just matches section names). New finding
  types: reference_drift, requirement_obsolete.
- **survey-project** — per-ambiguous-file iteration (filename →
  content sniff → mtime → related files), iteration trail shown
  to user.
- **record-feedback** — per-concern Stellungnahme iteration (per
  concern: identify addressed argument → fetch baseline reference
  → fetch interpreting ruling → find similar past Abwägung →
  find affected bausteine). Plus layered feedback path
  (`memory/bausteine/<layer>/<scope_key>/feedback/...`).

**All 16 skills** declare `mcp_tools_required[]` /
`mcp_tools_optional[]` / `fallback_when_mcp_absent` per meta-rule
5. Doctype paths use `list_doctypes_manifests()` (Tier 1 tool),
not legacy `memory/universal/doctypes.yaml`. Bausteine retrieval
is scope-aware via `list_bausteine`. Domain capitalization
corrected throughout (Naturschutz / PV-FFA / Wind, not legacy
lowercase tags).

**Orchestrator** specifically: PROCEDURE.md sections 1, 2 (T3),
6.2, 6.4, 9.3, 10 all updated; specialist routing list expanded
with 5 previously missing skills (validate-bausteine,
record-feedback, research-references, author-manifest,
setup-office).

### ✅ docs/rag-pipeline-decisions.md (commits `c15bec4` + `d6d75f9`)

Pre-RAG architectural decisions A–D + pipeline choices 1–3, all
PROPOSED awaiting audit confirmation:

| ID | Topic | Verdict |
|---|---|---|
| A | Multimodal storage | YES first ingest: OCR + DRM + ColPali. Defer table extraction. Filesystem ref + LanceDB metadata. New tool `read_corpus_page_image`. Cap 5 imgs/response. Hybrid retrieval. |
| B | Legal §-graph at ingest | YES; SQLite alongside LanceDB; nodes + typed edges; regex extraction at chunk-time. New tool `query_legal_graph`. |
| C | Chunking strategies | 4 existing sufficient; add `per-section-with-paragraph-subchunks` hybrid. Multimodal: page-level for image-RAG (independent). |
| D | Baustein reference versioning | DONE in alignment sweep (`verified_against_version` slot). |
| 1 | Text-retrieval baseline | bge-m3 + bge-reranker-v2-m3. ColBERT conditional. |
| 2 | Query rewriting | Defer; HyDE for save-baustein dedupe is first consumer. |
| 3 | Reranker model | bge-reranker-v2-m3 baseline. |

All sections preserve alternatives + revisit triggers per the new
**decision-recording convention** (ROADMAP "Working-style
improvements").

### ✅ ROADMAP additions this session

New items captured:

- **Tier 1 MCP discovery tools** (now landed; remove from ROADMAP
  if cleaning up)
- **Tier 2 MCP cross-reference tools** (deferred; pull-forward at
  first project work)
- **Tier 3 MCP introspection tools** (deferred indefinitely)
- **SKILL.md version-bump reminder hook** (deferred)
- **Hooks item revised** per meta-rule 5: most former candidates
  belong in MCP tools as atomic side-effects; out-of-band file
  change detection is the surviving niche
- **Schema migration framework for memory data records** (deferred
  until first baustein saved)
- **Backend conventions doc** (testing/logging/error-handling)
- **Plugin/deployment shipping bundle doc** (deferred until second
  deployment)
- **Generalized knowledge ingestion via MCP connectors**
  (SharePoint/Confluence/Notion/etc.; deferred until first
  external-source need)
- **Cross-deployment community knowledge content** (distinct from
  integration registry; deferred until second deployment)
- **Cross-practice knowledge integration** (deferred)
- **Pioneer-instance validation strategy** — four evidence types
  for one-user prototype: architectural validation / failure-mode
  probing / historical project replay / mock project + peer
  review. Pull-forward when PBS becomes operational.
- **Anthropic-native-app / GUI-frontend integrations** (with
  category-collapse guard: integration must serve intertwined
  workflow, not reduce PBS to tacked-on)
- **Decision-recording convention** — preserve alternatives +
  revisit triggers; applies to all decision docs going forward
- **Integration registry pull-forward triggers** — capability-
  vocabulary friction OR callable count >50 OR second deployment

### ✅ Memory: feedback memory captured

Saved at `~/.claude/projects/.../memory/feedback_judgment_and_automate.md`:
"Give judgment + recommendations, automate the rest" — user wants
Claude to commit to positions (not present open-ended menus),
automate routine work without asking, let discussion emerge from
substance. Connects to PROCEDURE.md "commit to a position" rule
+ sparring-partner principle in VISION.md.

---

## ⏳ Pending — first task next session

### Task #21 — Full pre-RAG architectural audit (the only remaining gate)

**This is THE next session task.** Everything upstream is done;
RAG kickoff is gated on this audit. Per the audit task
description:

1. **Cross-doc consistency audit** across ARCHITECTURE.md /
   ROADMAP.md / HANDOFF.md / VISION.md / all 16 skills + the
   new docs/rag-pipeline-decisions.md.
2. **Schema gap audit**:
   - Memory data records have no migration framework yet
     (deferred per ROADMAP; flag if this becomes blocking
     before first baustein save)
3. **Backend convention audit**:
   - Test layout, logging strategy, MCP error format spec —
     all undefined; flag for backend conventions doc creation
     (ROADMAP item)
4. **Deployment shipping bundle audit**:
   - For second-office; deferred per ROADMAP unless concrete
     prospect
5. **Drift audit**:
   - Did the alignment sweep introduce any inconsistencies
     between skills?
   - Are all 16 skills' frontmatter declarations actually used
     in their bodies?
   - Do all skills correctly reference Tier 1 MCP tool names?

6. **Fresh-eyes review of VISION.md + ARCHITECTURE.md wording
   for finalization** (NEW — added per user flag at landing
   time: "tired, not full focus" when the vision work landed;
   wanted to revisit later with fresh attention). Re-read both
   docs after living with them through the sweep — is the
   framing still right? Wording sharp enough? Any axis or
   subsection that reads off?

   This part specifically benefits from USER fresh eyes (not
   Claude's) — Claude authored most of it, so its "fresh eyes"
   are limited.

**Output**: surface findings in audit report; resolve or
explicitly defer-with-reasoning before RAG kickoff.

### Then — RAG kickoff (gated on audit)

Per `docs/rag-pipeline-decisions.md` implementation order:

1. **Backend pipeline additions** (per A + B + C verdicts):
   - OCR + DRM-removal modules in ingest
   - ColPali embedder + image-render pipeline
   - LanceDB schema migration: `modality`, `image_path`,
     `page_number` columns
   - SQLite `legal-graph.sqlite` initialization + extraction
     hooks in chunkers
   - Hybrid retrieval in `search_corpus`
   - New MCP tools: `read_corpus_page_image`, `query_legal_graph`
   - New chunking strategy: `per-section-with-paragraph-subchunks`

2. **Smoke-test on 3–5 entries** (text-only, diagram-heavy,
   scanned, DRM-encumbered).

3. **Full first ingest** (all 57 entries via `research-references`
   refresh-all).

4. **Sample search** to verify retrieval quality. If poor →
   revisit assessment choices (e.g. swap to ColBERT-v2; add HyDE).

After that:

- Bind first project (any existing hidrive project — orchestrator
  routes through survey-project → bind_project).
- Optional: wire `\OfficeLogoPath`, `\OfficeSpecializations` into
  `office-style.sty` letterhead.

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/VISION.md` | **NEW** — deepest anchor (three-axis thesis + pioneer instance) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/ARCHITECTURE.md` | v0.4: 5 meta-rules + 9 entity types + 6 decision rules + Backend organization |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/ROADMAP.md` | Deferred work; pull-forward triggers; decision-recording convention |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/docs/rag-pipeline-decisions.md` | **NEW** — pre-RAG architectural decisions A–D + pipeline choices 1–3 |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/skills/` | 16 skills, all aligned (16/16) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/extensions/{universal,domain/<X>,state/<X>}/` | Layered references + doctypes manifests (57 entries total) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/universal/` | Universal cross-bureau knowledge |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/bausteine/{universal,domain/<X>,state/<X>}/` | Bausteine landing site (currently empty; populated post-RAG) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/backend/mcp-server/src/pbs_mcp/tools/discovery.py` | **NEW** — Tier 1 MCP discovery tool handlers |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/backend/mcp-server/src/pbs_mcp/tools/memory.py` | Refactored for orthogonality (scope_key + new layered paths) |
| `~/.config/pbs-bureau/office.yaml` | PBS office config (schema v2; 5 ref manifests + 2 doctype manifests in scope) |
| `/mnt/data2t/hidrive/.../_ai-references/` | PBS legal references RAG corpus (still empty — first ingest fills it) |
| `/mnt/data2t/hidrive/.../Projekte/` | All client projects |

---

## Working-style notes (carried + new)

1. **Commit between batches** — 12 commits this session, one per
   coherent design pass or implementation chunk. Lets sanity-check
   progressively and rollback selectively.
2. **Decision-recording convention** (NEW per this session) —
   preserve alternatives + revisit triggers in every decision doc.
   Captured in ROADMAP "Working-style improvements".
3. **`pbs_core` / `pbs_mcp` discipline** (NEW per meta-rule 5
   Backend organization) — logic in plain Python; MCP tools as
   thin wrappers. Apply starting now even though physical split
   is deferred.
4. **Frontmatter dependency declarations on every new skill**
   (`mcp_tools_required[]`, etc.) — meta-rule 5 enforced going
   forward.
5. **MCP tool naming**: snake_case matching `pbs_core` Python
   function name (forward-compatible with future integration
   registry).
6. **Apply ARCHITECTURE.md rules rigorously** — when in doubt
   about where new content belongs, walk Rules 1–6.
7. **Cite-only entries are bibliographic-only** — they validate
   citation form, not claim accuracy.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Plugin cache symlink**: re-run `bash dev-link.sh` if
  `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` is a regular dir.
  Note: this session bumped many skill versions to 0.2.0; plugin
  version itself unchanged at 0.1.0.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Dotfiles**: global CLAUDE.md and settings.json tracked in
  `~/dev/Gunther-Schulz/dotfiles/claude/`. After editing either,
  commit + push the dotfiles repo.
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md` — stop on block, don't work
    around
  - `feedback_judgment_and_automate.md` (NEW this session) —
    commit to positions; automate routine; let discussion
    emerge from substance

---

## What this session looked like (commits, in order)

| # | Commit | Theme |
|---|---|---|
| 1 | `dbf5f74` | meta-rule 5 (execution locality) + backend organization |
| 2 | `519ed63` | VISION.md initial: thesis + intertwining + sparring partner |
| 3 | `93668c0` | three-axis (added authorship preservation) |
| 4 | `6ae58d1` | Foundations (Ming) + Extension 1 refined |
| 5 | `157b48c` | knowledge-layer ROADMAP additions |
| 6 | `294a314` | pioneer instance framing |
| 7 | `34e2ee8` | pioneer-instance validation strategy + audit covers vision |
| 8 | `6865a93` | Tier 1 MCP discovery tools + memory orthogonality refactor |
| 9 | `502f339` | align save-baustein + orchestrator |
| 10 | `b90fa32` | align verify-citations + validate-checklist + survey-project |
| 11 | `bd8a1e7` | align record-feedback + validate-bausteine + promote-to-skill |
| 12 | `e495b55` | align drafts + review + validate-latex-style (sweep complete) |
| 13 | `c15bec4` | docs/rag-pipeline-decisions.md (A–D + pipeline 1–3) |
| 14 | `d6d75f9` | decision-recording convention + decisions doc strengthened |
| 15 | (this commit) | HANDOFF.md updated for fresh-session pickup |

All pushed to origin/main.
