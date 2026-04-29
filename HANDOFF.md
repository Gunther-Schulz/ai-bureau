# Session handoff — pbs-bureau

End of session 2026-04-29 (fifth major session). Previous session
closed with the **pre-RAG audit gate** as the only blocker. This
session **executed the audit** (Slice A cross-doc / B 16-skill
drift / C backend), shipped the resulting **F1–F9 fix-now drift
batch**, the **U1 decision-recording backfill** in
`rag-pipeline-decisions.md`, and the **U2 backend conventions
doc** (resolves audit deferred items D1/D2/D3).

**The pre-RAG audit gate is now closed.** RAG kickoff is
unblocked and is the first task next session.

The audit deferred fresh-eyes review of VISION.md and
ARCHITECTURE.md wording (U3) to **post-RAG** per user decision —
not blocking, but on the watch list.

**Read order for next session**:

1. **This file (HANDOFF.md)** — current state
2. **`docs/rag-pipeline-decisions.md`** — now **ACCEPTED**
   (previously PROPOSED). Implementation order at bottom is the
   next-session work plan.
3. **`docs/backend-conventions.md`** — NEW. Test layout, logging,
   MCP error format. Apply when RAG-pipeline code starts landing.
4. **`docs/audit-pre-rag.md`** — audit findings as of session 5.
   Permanent record; useful template for future audits.
5. **`VISION.md`** — three-axis thesis (still load-bearing)
6. **`ARCHITECTURE.md`** — 5 meta-rules + 9 entity types + 6
   decision rules (verified clean by audit; small additions
   for baustein extensions D+E pointer + RAG-decisions cross-ref)
7. **`ROADMAP.md`** — Tier 1 entry removed (landed); Tier 2
   split (find_bausteine_by_reference landed); Backend
   conventions doc removed (landed via U2)
8. **`plugin/skills/orchestrator/SKILL.md` + `PROCEDURE.md`**
9. Whichever skill the user invokes

---

## Status snapshot — what landed this session

### ✅ Pre-RAG architectural audit (Task #21, closed)

Three parallel audit slices (A cross-doc, B 16-skill drift, C
backend). 12 findings total: 9 fix-now drift, 3 user-decision,
plus 5 expected-gap items deferred-with-reasoning.

**Verdict**: conditional pass. All three conditions closed
this session.

Permanent record at `docs/audit-pre-rag.md`.

### ✅ F1–F9 fix-now drift batch (commit `ad01b18`)

The HANDOFF claim "all 16 skills aligned" was partially false at
session-4 boundary — 12/16 fully aligned, 4 had meta-rule-5
frontmatter gaps. F-batch closed all 9 mechanical drift items:

- **F1 — research-references** (BLOCKER): added all three
  frontmatter fields; migrated body from
  `office_config.load().all_references_manifests()` to Tier 1
  `list_reference_manifests(scope_filter=true)`. Version 0.2.0 → 0.2.1.
- **F2 — author-manifest** (BLOCKER): empty positive-declaration
  frontmatter (`mcp_tools_required: []` + optional + fallback).
  Version 0.1.0 → 0.1.1.
- **F3 — setup-office, validate-latex-style, draft-cover-mail**:
  positive-declaration frontmatter completion. All bumped to
  0.2.1.
- **F4 — orchestrator**: added `bind_project` + `setup_project`
  to `mcp_tools_optional`.
- **F5 — server.py:92**: `list_bausteine` description string
  refreshed (was stale: "domain/project" → now
  "scope_key/project_root").
- **F6 — ROADMAP**: Tier 1 MCP discovery section removed
  (landed); Tier 2 split (`find_bausteine_by_reference` landed).
- **F7 — ARCHITECTURE.md**: entity-type-D notes the baustein
  extensions D+E (`verified_against_version`,
  `cross_project_visible`) reserved schema slots; pointer to
  `plugin/skills/save-baustein/references/format.md` for full spec.
- **F8 — ARCHITECTURE.md**: "Designed extensions" section
  cross-refs `docs/rag-pipeline-decisions.md` for RAG-related
  items.
- **F9 — ROADMAP**: integration-registry callable count refreshed
  (~30 → ~44; 16 skills + 5 adapters + 22 MCP tools + 1 external).

### ✅ U1 — decision-recording convention backfill (commit `d0f3f91`)

`docs/rag-pipeline-decisions.md` had only 2 of ~13 sections
conforming to the new convention (preserve alternatives + revisit
triggers). Backfilled across A.1, A.2, A.3, B.1, B.2, B.4, C
(unified at C.4), D, and pipeline choices 1/2/3. Sections A.4
+ A.5 were already conforming (authoring template).
Schema-spec subsections (B.3, B.5) and pure sequencing (A.6)
intentionally left as-is — not decision points.

Status field on the doc moved **PROPOSED → ACCEPTED** post-audit.

### ✅ U2 — backend conventions doc (commit `501eaa1`)

NEW: `docs/backend-conventions.md`. Resolves audit deferred items
D1/D2/D3.

- **Tests**: pytest, `tests/{unit,integration}/` at backend root,
  real in-memory DBs over mocks (LanceDB and SQLite are local;
  fixtures land in `conftest.py`).
- **Logging**: standard `logger = logging.getLogger(__name__)`
  per module; `basicConfig` once in `server.main`; INFO default
  with `PBS_LOG_LEVEL` override; %-format in log calls (not
  f-strings) via ruff `G` rule; structured logs deferred until
  multi-user.
- **Errors**: JSON envelope with `_error` sentinel in
  `TextContent`; named string error codes (`input_validation`,
  `config_missing`, `not_found`, `not_in_scope`,
  `corpus_unavailable`, `tool_runtime`, `external_api`,
  `not_implemented`); `ToolError` exception class wraps domain
  exceptions; rejected `mcp.McpError` because Claude-Code MCP
  client surfaces those as generic "tool failed."

Each section preserves alternatives + revisit triggers per
decision-recording convention.

**Migration order** (in U2 doc): create `tests/` + conftest.py,
add `G` to ruff selection + sweep log calls, add `ToolError`
class + update `server.call_tool` wrapper. Land in same PR as
RAG-pipeline ingest additions (first real consumers).

ROADMAP "Backend conventions doc" item removed per Tracking
conventions.

### ⏸️ U3 — fresh-eyes review of VISION + ARCHITECTURE wording

**Deferred to post-RAG by user decision.** Not blocking.

The audit flagged this from the previous-session HANDOFF: user
flagged at vision-doc landing time "tired, not full focus";
wanted to revisit later with fresh attention. Specifically wants
**user fresh eyes**, not Claude's, since Claude authored most of
both docs.

Re-pick-up trigger: after the first RAG kickoff lands and the
operating reality of using the system can inform a fresh
read-through. The framing risks at that point are visible only
after using it.

---

## ⏳ Pending — first task next session

### RAG kickoff (per `docs/rag-pipeline-decisions.md` § Implementation order)

The audit gate is closed; the implementation plan in the
RAG-decisions doc moves from "verdict" to "build."

**Phase 1 — Backend pipeline additions** (single PR; lands the
U2 conventions migration in the same PR):

a. Set up `tests/` + `conftest.py` per `backend-conventions.md`
   §1; add `G` to ruff selection; add pytest config to
   `pyproject.toml`. Mechanical.
b. Add `ToolError` exception class to `pbs_mcp/`; update
   `server.call_tool` wrapper to emit error envelopes; convert
   existing handlers to raise `ToolError`. Mechanical.
c. **OCR + DRM-removal modules** in ingest pipeline. Per A.1.
   Branches on text-availability heuristic — skip OCR for PDFs
   that already carry extractable text.
d. **ColPali embedder** alongside bge-m3 (lazy-load on first
   image-query). Page-render pipeline → PNGs at 2048-px max.
e. **LanceDB schema migration**: add `modality`, `image_path`,
   `page_number` columns. Per A.2.
f. **SQLite `legal-graph.sqlite`** initialization + extraction
   hooks in chunkers. Per B.4 — regex extraction at chunk-time.
g. **Hybrid retrieval** in `search_corpus` (reranker scores
   text + image candidates). Per A.5.
h. **New MCP tools**: `read_corpus_page_image`,
   `query_legal_graph`. Per A.3 + B.5.
i. **New chunking strategy**: `per-section-with-paragraph-subchunks`.
   Per C.2.

**Phase 2 — Smoke-test on 3–5 entries** (text-only,
diagram-heavy, scanned, DRM-encumbered).

**Phase 3 — Full first ingest** (all 57 entries via
`research-references` refresh-all). Tracked in
`<references_root>/changelog.md`.

**Phase 4 — Sample search** to verify retrieval quality. If
poor → revisit assessment choices per the revisit triggers in
`rag-pipeline-decisions.md` (e.g. swap to ColBERT-v2; add HyDE).

### Then — first project bind

After RAG works:

- Bind first project (any existing hidrive project — orchestrator
  routes through survey-project → bind_project).
- Optional: wire `\OfficeLogoPath`, `\OfficeSpecializations` into
  `office-style.sty` letterhead.

### Watch list (not blocking; surface at session open if relevant)

- **U3 — fresh-eyes review of VISION + ARCHITECTURE wording** —
  deferred to post-RAG. Surface again once Phase 1 lands.
- **D5 — legacy backward-compat shim in `_summarize`**
  (`memory.py:308`) — drop once first migration sweep confirms no
  v0.3-shape bausteine remain (none can exist today; revisit at
  first baustein save).
- **D7 — Plugin/deployment shipping bundle** — defer until second
  deployment.

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis + pioneer instance |
| `ARCHITECTURE.md` | v0.4: 5 meta-rules + 9 entity types + 6 decision rules; updated this session for entity-type-D extensions D+E pointer + designed-extensions cross-ref |
| `ROADMAP.md` | Tier 1 + Backend-conventions-doc items removed (landed); Tier 2 split |
| `docs/rag-pipeline-decisions.md` | **ACCEPTED** post-audit; status updated |
| `docs/backend-conventions.md` | **NEW** — test layout, logging, MCP error format |
| `docs/audit-pre-rag.md` | Audit findings (permanent record) |
| `docs/office-config.schema.yaml` | schema v2 reference |
| `plugin/skills/` | 16 skills, all aligned (16/16 — *now* truly) |
| `extensions/{universal,domain/<X>,state/<X>}/` | 5 ref + 2 doctype manifests in scope (57 entries) |
| `memory/universal/` | Universal cross-bureau knowledge |
| `memory/bausteine/{universal,domain/<X>,state/<X>}/` | Bausteine landing site (still empty; populated post-RAG) |
| `backend/mcp-server/src/pbs_mcp/tools/discovery.py` | Tier 1 MCP discovery tool handlers |
| `backend/mcp-server/src/pbs_mcp/tools/memory.py` | Layered orthogonality (scope_key + project_root) |
| `backend/mcp-server/tests/` | Will be created in Phase 1a |
| `~/.config/pbs-bureau/office.yaml` | PBS office config (schema v2) |
| `/mnt/data2t/hidrive/.../_ai-references/` | RAG corpus (still empty; first ingest fills it) |
| `/mnt/data2t/hidrive/.../Projekte/` | All client projects |

---

## Working-style notes (carried + new)

1. **Commit between batches** — 4 commits this session (audit doc
   + F-batch combined; then U1; then U2; then this HANDOFF). One
   per coherent change.
2. **Decision-recording convention** — preserve alternatives +
   revisit triggers in every decision doc. Backfilled in U1 across
   `rag-pipeline-decisions.md`; applied throughout
   `backend-conventions.md`. Now well-established.
3. **`pbs_core` / `pbs_mcp` discipline** — handlers stay
   thin-Python (Pydantic in / out); MCP framework types only in
   `server.py`. Physical split deferred to first non-MCP frontend.
4. **Frontmatter dependency declarations on every skill** —
   meta-rule 5; F-batch closed the last gaps.
5. **MCP tool naming**: snake_case matching `pbs_core` Python
   function name (forward-compat with future integration registry).
6. **Apply ARCHITECTURE.md rules rigorously** — when in doubt
   about where new content belongs, walk Rules 1–6.
7. **Audit pattern**: three parallel slice agents (cross-doc /
   skill-drift / backend) was efficient — total ~6 minutes
   wall-clock, surfaced 12 findings cleanly. Use again for the
   next major audit cycle.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Plugin cache symlink**: re-run `bash dev-link.sh` if
  `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` is a regular
  dir. This session bumped 5 skill versions (research-references,
  author-manifest, setup-office, validate-latex-style,
  draft-cover-mail to 0.2.1 / 0.1.1); plugin version itself
  unchanged at 0.1.0.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md` — stop on block, don't work
    around
  - `feedback_judgment_and_automate.md` — commit to positions;
    automate routine; let discussion emerge from substance

---

## What this session looked like (commits, in order)

| # | Commit | Theme |
|---|---|---|
| 1 | `ad01b18` | audit: pre-RAG architectural audit + F1–F9 fix-now drift batch |
| 2 | `d0f3f91` | docs/rag-pipeline-decisions: backfill alternatives + revisit triggers (U1) |
| 3 | `501eaa1` | docs/backend-conventions: test layout + logging + MCP error format (U2) |
| 4 | (this commit) | HANDOFF: rewrite for session-5 → session-6 boundary |

All pushed to origin/main.
