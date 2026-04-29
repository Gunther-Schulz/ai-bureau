# Session handoff — pbs-bureau

End of session 2026-04-29 (fifth major session). Earlier in this
session: pre-RAG architectural audit (3 parallel slice agents → 12
findings → conditional pass) + F1–F9 fix-now drift batch + U1
decision-recording backfill + U2 backend conventions doc + first
HANDOFF rewrite.

**Then the gate-closed claim turned out premature.** Three
follow-up audit rounds (meta-audit + rounds 3 + 4) surfaced 3
**BLOCKERS** in backend docs + live ingest code, plus 18
documentation drift items. All resolved in commit `488cfc7`.
Plus `docs/plugin-conventions.md` landed (commit `c67c73a`).

**Audit work is now genuinely complete.** Round 4's verdict was
explicit: "no new unaudited territory left." RAG-kickoff
preparation moves forward.

**Phase 0 (pre-RAG plumbing) is partially done**: items 1
(meta-audit) and 2 (plugin-conventions) per the restructured
plan are closed. Items 3 (integration registry design+impl)
and 4 (testing-methodology decisions + harness) are the
**next-session task** — discussion-first per user directive.

**Read order for next session**:

1. **This file (HANDOFF.md)** — current state
2. **`docs/rag-pipeline-decisions.md`** — ACCEPTED post-audit;
   Phase 0/1/2a/2b/3a/3b/4 phasing at the bottom
3. **`docs/plugin-conventions.md`** — NEW (Type A/B idioms;
   sibling to backend-conventions.md)
4. **`docs/backend-conventions.md`** — Type E idioms
5. **`docs/audit-pre-rag.md`** — frozen session-5 snapshot
   (closure banner at top; HANDOFF carries current state)
6. **`VISION.md`** — three-axis thesis
7. **`ARCHITECTURE.md`** — 5 meta-rules + 9 entity types + 6
   decision rules; Maintenance discipline back-refs to plugin/
   backend conventions docs
8. **`ROADMAP.md`** — Tier 1 + backend-conventions-doc removed
   (landed); Tier 2 split (find_bausteine_by_reference landed)

---

## Status snapshot — what landed this session

### ✅ Audit work — 4 rounds, 12 + 12 + 6 + 14 findings, all closed

| Round | Slices | Findings | Closed in |
|---|---|---|---|
| 1 — pre-RAG audit | A cross-doc / B 16-skill / C backend | 12 (9 fix-now drift, 3 user-decision, 5 deferred) | `ad01b18` (F-batch) + `d0f3f91` (U1) + `501eaa1` (U2) |
| 2 — meta-audit | E plugin-side / F memory+manifests / G self-audit+adapters | 12 (5 fix-now drift, 5 user-decision, defer-rest) | `488cfc7` |
| 3 — backend deep + cross-refs + READMEs | H backend / I PROCEDURE+handoffs / J READMEs+per-project-memory | 6 fix-now drift (incl 2 BLOCKERS in backend docs) | `488cfc7` |
| 4 — final pass | unified | 14 (incl 1 LIVE CODE BLOCKER in ingest.py + 6 drift + version-rebump confirmation) | `488cfc7` |

**Three BLOCKERS** (specifically dangerous):
- `backend/mcp-server/docs/vector-metadata-schema.md`: legacy `global | domain | project` baustein scope vocab → would have written wrong metadata to LanceDB on first ingest. Fixed.
- `backend/mcp-server/docs/chunking-strategy.md`: same legacy vocab in baustein chunker spec. Fixed.
- `backend/mcp-server/src/pbs_mcp/tools/ingest.py:217`: LIVE CODE — baustein source_subtype dispatcher returned `"global"` / `"domain"` for legacy paths; rewritten to detect orthogonal `/bausteine/{universal,domain,state}/` + project `_ai/` paths.

Audit-pattern confirmed valuable: 4 rounds caught progressively different drift surfaces (top-level docs → plugin-side → backend code → cross-cutting doc consistency). Each round needed a different scope frame.

### ✅ Skill version semver retroactively corrected (audit verdict applied)

Six skills bumped from patch-where-it-should-have-been-minor to minor (rule was already in plugin/CLAUDE.md but F-batch initially missed it; audit caught + user authorized retroactive correction):

| Skill | Was | Now |
|---|---|---|
| research-references | 0.2.1 | 0.3.0 |
| author-manifest | 0.1.1 | 0.2.0 |
| setup-office | 0.2.1 | 0.3.0 |
| validate-latex-style | 0.2.1 | 0.3.0 |
| draft-cover-mail | 0.2.1 | 0.3.0 |
| orchestrator | 0.2.0 | 0.3.0 |
| validate-checklist | 0.2.0 | 0.3.0 |

Discipline now codified in `docs/plugin-conventions.md` §3 — "if the orchestrator or any other tool/skill reads the field for planning, changing it = behavior change = minor bump."

### ✅ docs/plugin-conventions.md (commit `c67c73a`)

Sibling to `docs/backend-conventions.md`. Codifies Type A/B idioms:
frontmatter contract + version semver + body structure + references
organization + PROCEDURE.md gating + routing handoffs + path
conventions + domain+state capitalization + MCP tool naming +
trigger-phrase discipline (top-level vs. delegated) + anti-patterns.
Both conventions docs carry the same scope-boundary header pointing
back at ARCHITECTURE.md.

### ✅ Restructured RAG phasing in `docs/rag-pipeline-decisions.md`

Previous flat "Backend pipeline additions" lumped 7 distinct
concerns into one PR (too coarse). New phasing splits text vs
image side and downloads the corpus early so chunker design
iterates against real data:

- **Phase 0** (pre-RAG plumbing) — meta-audit, plugin-conventions,
  registry design+impl, testing-methodology design (~70%
  complete; items 3+4 outstanding)
- **Phase 1** — corpus download only (no embeddings)
- **Phase 2a** — text-side smoke (5 entries)
- **Phase 2b** — full text ingestion
- **Phase 3a** — image-side smoke (3 image-heavy + 1 scanned + 1 DRM)
- **Phase 3b** — full image ingestion + verified hybrid
- **Phase 4** — first project bind + real workflow

Each phase has explicit gates. Coverage-gap tracking + ground-truth
set + determinism harness will land as part of Phase 0 item 4.

### ⏸️ U3 — fresh-eyes review of VISION + ARCHITECTURE wording

Still deferred to post-RAG by user decision. Surface again after
Phase 1 (corpus download) lands.

---

## ⏳ Pending — next-session tasks

### Phase 0 item 3 — Integration registry design + implementation

**Discussion-first**: don't write code until decisions land.

Open design questions to resolve:

- **Capability vocabulary**: controlled enum, free-form tags, or hybrid (small enum + open tags)?
- **Manifest structure**: 4th layered type (`integrations-manifest.yaml` per universal/domain/state), or single registry file at repo root?
- **Discovery flow**: does orchestrator query `find_callables(capability=X)` or `list_registry_entries(filter=...)` — or both?
- **Layering vs replacement**: does the registry **replace** `list_skills` / `list_reference_manifests` / `list_doctypes_manifests`, or **layer above** them as a unified front?
- **MCP query API shape**: signature + return shape for the registry query tool(s).
- **Cross-deployment propagation**: how does a registry entry from PBS deployment flow to a hypothetical second office's registry without coupling?

Implementation cost estimate: ~half a day after design. Bundle with U2 conventions migration (tests/, ToolError, ruff `G` rule sweep) in the same PR.

### Phase 0 item 4 — Testing methodology + harness

**Discussion-first**.

Per user's specific concern: "if we have a limited RAG at first with no vision how do we track what we need to ingest at a later time (the pieces we will be missing)?"

Three layered concerns to design:

- **Coverage-gap tracking**: per-manifest-entry `coverage:` field schema (text/images/tables/graph + last_indexed + coverage_score). Chunkers self-report at ingest time. Rolls up to `<references_root>/coverage-report.md`.
- **Ground-truth set**: `tests/ground_truth/legal-queries.yaml` with 15-25 hand-curated query/expected-doc pairs. **User curates** these (Claude can scaffold candidates from existing memory references). Pytest test asserts top-5 reranked hits include expected doc.
- **Determinism + regression detection**: embedding seed pinned; reranker tie-break by ID. Baseline retrieval-quality scores stored; diff on chunker/model changes.

Output: `docs/rag-testing-strategy.md` documenting the three layers + acceptance criteria for each phase gate (e.g. "Phase 2b passes when ground-truth set top-5 ≥ 70% relevance").

### Then — Phase 1 corpus download

After items 3+4 close. Fetch all 57 entries via `research-references` full refresh. **No embeddings yet** — raw fetch + checksum + manifest population only. Surfaces real corpus shape (DRM/scanned/manual-discovery) before chunker code commits.

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis + pioneer instance |
| `ARCHITECTURE.md` | v0.4: 5 meta-rules + 9 entity types + 6 decision rules; Maintenance-discipline back-refs to plugin/backend conventions |
| `ROADMAP.md` | Tier 1 + backend-conventions-doc + integration-registry callable count refreshed/removed (landed) |
| `docs/rag-pipeline-decisions.md` | **ACCEPTED**; restructured Phase 0/1/2a/2b/3a/3b/4 phasing |
| `docs/plugin-conventions.md` | **NEW** — Type A/B idioms |
| `docs/backend-conventions.md` | Type E idioms (sibling to plugin-conventions) |
| `docs/audit-pre-rag.md` | Frozen session-5 audit snapshot (closure banner at top) |
| `docs/office-config.schema.yaml` | schema v2 |
| `plugin/skills/` | 16 skills, all aligned + retroactively rebumped to minor where appropriate |
| `plugin/templates/office-style/` | default + PV-FFA + Wind + **Naturschutz** (NEW stub) |
| `extensions/{universal,domain/<X>,state/<X>}/` | 5 populated + 1 skeleton (Innenentwicklung) ref manifests; 2 doctype manifests; 57 ref entries total |
| `memory/universal/per-project-memory/*.md` | Now carries `references_used: []` frontmatter per Type C |
| `memory/bausteine/{universal,domain/<X>,state/<X>}/` | Bausteine landing site (still empty until Phase 4) |
| `backend/mcp-server/src/pbs_mcp/tools/{discovery,memory,ingest}.py` | All three updated this session for orthogonality + ingest BLOCKER fix |
| `backend/mcp-server/docs/{vector-metadata-schema,chunking-strategy}.md` | Both fixed for orthogonal scope vocab |
| `~/.config/pbs-bureau/office.yaml` | PBS office config |
| `/mnt/data2t/hidrive/.../_ai-references/` | RAG corpus root (still empty; Phase 1 fills it) |
| `/mnt/data2t/hidrive/.../Projekte/` | All client projects |

---

## Working-style notes (carried + new)

1. **Audit pattern (3 parallel slice agents per round)** — proven valuable across 4 rounds. Each round caught a different drift surface; the cost (~5–10 min wall-clock per round) is small relative to the cost of mistagged data hitting LanceDB.
2. **Decision-recording convention** — every decision doc preserves alternatives + revisit triggers (ROADMAP "Working-style improvements"). Applied throughout this session.
3. **Commit between batches** — 4 + 4 commits this session (audit + F-batch / U1 / U2 / mid-session HANDOFF / meta-audit-fix-batch / plugin-conventions / final HANDOFF).
4. **Frontmatter changes are behavior changes** — minor bump per `docs/plugin-conventions.md` §3. Don't repeat the F-batch's patch-bump miss.
5. **Scope-boundary headers** on conventions docs to mitigate overlap with ARCHITECTURE.md placement rules.
6. **`pbs_core` / `pbs_mcp` discipline** — handlers stay thin-Python (Pydantic in/out); MCP framework types only in `server.py`. Physical split deferred to first non-MCP frontend.
7. **MCP tool naming**: snake_case matching `pbs_core` Python function name. Codified in plugin-conventions §10.
8. **Apply ARCHITECTURE.md rules rigorously** — when in doubt about where new content belongs, walk Rules 1–6.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Plugin cache symlink**: re-run `bash dev-link.sh` if
  `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` is a regular dir.
  This session bumped 7 skill versions; plugin version still 0.1.0.
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
| 4 | `ec143fd` | HANDOFF: session 5 → 6 boundary (premature — superseded below) |
| 5 | `488cfc7` | audit: meta-audit + rounds 3/4 fix-now batch (3 BLOCKERS + 18 drift) |
| 6 | `c67c73a` | docs/plugin-conventions: codify Type A/B idioms (skills + skill references) |
| 7 | (this commit) | HANDOFF: session 5 final boundary |

All pushed to origin/main once the user authorizes a push.
