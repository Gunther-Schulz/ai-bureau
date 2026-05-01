# Pre-RAG architectural audit

> **Closure status (post-session-5):** Conditional pass. F1–F9 + U1
> + U2 closed in commits `ad01b18` / `d0f3f91` / `501eaa1`. The
> meta-audit (slices E/F/G) and rounds 3+4 surfaced additional drift
> beyond the original 12 findings; those are tracked in `HANDOFF.md`
> and resolved in subsequent commits. This doc is a frozen
> session-5 snapshot — read alongside HANDOFF for current state.

**Date:** 2026-04-29 (session 5).
**Trigger:** HANDOFF Task #21 — gate before RAG kickoff.
**Method:** three parallel slice audits — cross-doc consistency (A), skill drift across the 16 plugin skills (B), backend & convention gaps (C). Each slice followed the brief in HANDOFF "audit covers".
**Scope NOT covered here:** fresh-eyes review of VISION.md + ARCHITECTURE.md wording (per HANDOFF, this benefits from *user* fresh eyes; Claude authored most of it).

## Verdict

**Conditional pass.** The architecture is sound, the alignment sweep is ~88% complete (12/16 skills fully aligned, not 16/16 as HANDOFF claimed), and all backend claims verified at the bit level. There are 7 fix-now drift items (small, mechanical), 5 defer-with-reasoning items (all expected per ROADMAP), and 3 items that need user input before RAG kickoff.

After the fix-now batch lands, RAG kickoff is unblocked.

---

## Findings — fix-now drift

These are small, mechanical, and should land before RAG kickoff so the codebase isn't carrying drift into the next phase of work.

### F1 — research-references missing meta-rule-5 frontmatter (BLOCKER)
**Where:** `plugin/skills/research-references/SKILL.md` lines 1–6.
**What:** No `mcp_tools_required[]`, `mcp_tools_optional[]`, or `fallback_when_mcp_absent` declared. Body uses `ingest_paths`, `find_bausteine_by_reference`, plus `office_config.load().all_references_manifests()`.
**Fix:** Add the three frontmatter fields. Replace `office_config.load().all_references_manifests()` with `list_reference_manifests(scope_filter=true)` so the skill is consistent with the rest of the plugin (verify-citations, validate-bausteine, draft-textteil-b/c, etc. all use the Tier 1 tool).

### F2 — author-manifest missing meta-rule-5 frontmatter (BLOCKER)
**Where:** `plugin/skills/author-manifest/SKILL.md` lines 1–6.
**What:** No `mcp_tools_required[]`, `mcp_tools_optional[]`, or `fallback_when_mcp_absent`. Body uses only Glob/Bash/Write/Read/Edit + `office_config.load()` (Python helper, not an MCP tool).
**Fix:** Add `mcp_tools_required: []`, `mcp_tools_optional: []`, and a fallback string. The empty arrays are the *positive* declaration that no MCP tools are needed — that's what meta-rule 5 expects, not silent absence.

### F3 — setup-office, validate-latex-style, draft-cover-mail partial frontmatter (drift)
**Where:** the three SKILL.md files.
**What:**
- `setup-office`: no MCP frontmatter declared at all (same pattern as author-manifest).
- `validate-latex-style`: only `fallback_when_mcp_absent` present; missing the two array fields.
- `draft-cover-mail`: only `mcp_tools_optional` + fallback; missing `mcp_tools_required: []`.

**Fix:** Add the missing fields as empty arrays where there are no MCP tools, so meta-rule 5's positive-declaration contract holds across all 16 skills.

### F4 — orchestrator missing `setup_project` in frontmatter (hygiene)
**Where:** `plugin/skills/orchestrator/SKILL.md` line 7 (frontmatter) vs. PROCEDURE.md Checkpoint 12 + body line 90.
**What:** Orchestrator invokes `setup_project` MCP tool from PROCEDURE Checkpoint 12 but doesn't declare it in `mcp_tools_optional[]`.
**Fix:** Add `setup_project` to orchestrator's `mcp_tools_optional[]` (or `_required` if mandatory).

### F5 — server.py `list_bausteine` description stale
**Where:** `backend/mcp-server/src/pbs_mcp/server.py:92`.
**What:** Description string still reads "List bausteine matching scope/**domain/project**/status filters." After the orthogonality refactor it's `scope/scope_key/project_root/status`. The Pydantic-generated JSON schema is correct; only the human-readable description string is stale.
**Fix:** One-line edit.

### F6 — ROADMAP stale: Tier 1 + Tier 2 partial-landed items still listed as pending
**Where:** `ROADMAP.md` lines 14–51 (Tier 1) and 53–72 (Tier 2).
**What:** Tier 1 MCP discovery layer still listed as a pending v1.x ROADMAP item — but all 5 tools landed in `server.py` lines 76–80. ROADMAP's own Tracking conventions say "Once complete, remove from this file." Separately, Tier 2 section claims "no graph query exists" but `find_bausteine_by_reference` is implemented (memory.py:270, server.py:66).
**Fix:** Remove Tier 1 section entirely. Split Tier 2: remove `find_bausteine_by_reference` (landed); keep `find_memory_docs_by_reference` and `find_manifest_entry` as remaining Tier 2 work.

### F7 — ARCHITECTURE.md silent on baustein extensions D + E
**Where:** `ARCHITECTURE.md` (no mention) vs. `plugin/skills/save-baustein/references/format.md` (where they live) + HANDOFF claim that they "landed."
**What:** `verified_against_version` and `cross_project_visible` are ARCHITECTURE-level extensions to entity-type D's schema. ARCHITECTURE.md's "maintenance discipline" rule (line 32) requires schema-level facts to be recorded there. Currently the spec lives only in a skill reference file.
**Fix:** Add a one-line pointer in ARCHITECTURE.md's entity-type-D notes: "Bausteine schema reserves `verified_against_version` (per RAG-decision D) and `cross_project_visible` (project-scope visibility flag); see `plugin/skills/save-baustein/references/format.md`."

### F8 — ARCHITECTURE.md "Designed extensions" section doesn't cite rag-pipeline-decisions.md
**Where:** `ARCHITECTURE.md` lines 554–599.
**What:** Lists "Multimodal RAG ingest pipeline", "Structural retrieval", "Query rewriting", "agentic retrieval", "late-interaction text retrieval" as designed-but-not-implemented and points only at ROADMAP. But `docs/rag-pipeline-decisions.md` has now resolved these to specific verdicts (PROPOSED).
**Fix:** Add at the top of the section: "RAG-related items are further resolved (PROPOSED) in `docs/rag-pipeline-decisions.md`; final confirmation pending pre-RAG audit (this audit)."

### F9 — ROADMAP integration-registry callable count stale
**Where:** `ROADMAP.md` lines 706–724.
**What:** "16 skills + 5 integration adapters + ~10 planned MCP tools = ~30 callables." Tier 1 landed → current count is 22 MCP tools. Total ~38 callables (16 skills + 5 adapters + 22 MCP tools + 1 external MCP gis-utils).
**Fix:** Refresh the count so the >50 trigger threshold remains meaningful.

---

## Findings — defer-with-reasoning (all expected per ROADMAP)

### D1 — Tests: no test directory, pytest unused (expected gap)
**Where:** `backend/`. `pytest>=8.3.0` in pyproject.toml dev-deps but no `tests/` dir.
**Reasoning:** ROADMAP "Backend conventions doc" item explicitly defers test layout. No bausteine saved yet, no first project bound, and the discovery tools are simple enough that smoke-testing via `list_*` calls in a session is sufficient pre-RAG.
**Revisit trigger:** Before merging the first non-trivial RAG-pipeline change (OCR / ColPali / hybrid retrieval) — those have integration-test surface area that ad-hoc testing can't cover.

### D2 — Logging: ad-hoc but consistent (expected gap)
**Where:** all backend modules use `logger = logging.getLogger(__name__)`; `basicConfig` happens once in `server.main`. Mix of f-strings and %-formatting.
**Reasoning:** Consistent pattern, no structured logging needed pre-RAG. The f-string vs %-format inconsistency will be caught by ruff `G` rule when conventions doc is written.
**Revisit trigger:** Same as D1 — when conventions doc is written.

### D3 — MCP error format: stringified, no error envelope (expected gap)
**Where:** `server.py:125–145`. Errors return `TextContent("Tool error: TypeName: msg")`. No JSON-shaped envelope, no error codes.
**Reasoning:** Skill-side branching on error type isn't needed yet; current error strings are debuggable. Decision between JSON-envelope `TextContent` vs `mcp.McpError` is a real choice that should land in the conventions doc.
**Revisit trigger:** First time a skill needs to branch on a tool's failure mode (e.g., distinguishing "config not found" from "ingest failed" to choose recovery path).

### D4 — pbs_core / pbs_mcp discipline: structurally clean, schemas coupled
**Where:** `tools/discovery.py`, `tools/memory.py`, `schemas.py`.
**Reasoning:** Handlers ARE thin Python functions taking Pydantic in / Pydantic out — no MCP types in handler bodies. `server.py` is the only file importing MCP framework types. *But* the Pydantic schemas live in `pbs_mcp/schemas.py`, which couples handler logic to the MCP-tier namespace. Physical split is deferred per HANDOFF until first non-MCP frontend.
**Revisit trigger:** First non-MCP frontend (web UI is the load-bearing trigger per ARCHITECTURE meta-rule 5 Backend organization). When that happens, move models to `pbs_core.schemas`.

**Minor side-note:** `save_baustein` (memory.py:198–239) has 32 lines of inline dict construction. Worth extracting to `_default_frontmatter(input)` when the split happens, so non-MCP callers can reuse it. Not a blocker.

### D5 — Legacy backward-compat shim in `_summarize`
**Where:** `memory.py:308` — `scope_key = fm.get("scope_key") or fm.get("domain") or fm.get("project")`.
**Reasoning:** Reads old `domain`/`project` frontmatter keys. Comment acknowledges "none yet at v0.4". Harmless and intentional.
**Revisit trigger:** First migration sweep that confirms no v0.3-shape bausteine remain (none can exist today — bausteine dir is empty).

### D6 — Schema migration framework for memory data records (expected gap)
**Reasoning:** ROADMAP defers until first baustein saved. None saved yet.
**Revisit trigger:** First baustein save, OR first schema change after first baustein save (whichever blocks first).

### D7 — Plugin/deployment shipping bundle (expected gap)
**Reasoning:** ROADMAP defers until second deployment. No concrete second-office prospect.
**Revisit trigger:** First serious conversation about deploying to a second office.

---

## Findings — needs user input

These are not Claude's call.

### U1 — Decision-recording convention applied inconsistently in rag-pipeline-decisions.md
**Where:** `docs/rag-pipeline-decisions.md`. Only sections A.4 and A.5 contain explicit "Alternatives considered" + "Revisit trigger" blocks. Sections A.1–A.3, B (all subsections), C, D, 1, 2, 3 give verdict + reasoning but lack the formal three-part record.
**Tension:** The convention was authored in commit `d6d75f9` *to strengthen this very doc*. Either the convention's bar is higher than current practice (backfill needed), or current practice is fine and the convention should be relaxed to "verdicts must, alternatives encouraged for non-obvious choices."
**Recommendation:** Backfill alternatives + revisit triggers across all sections. The doc is the audit-confirmation gate for RAG kickoff, so the rigor pays off. Should be one focused pass — ~30 min of writing.
**Decision needed:** Backfill or relax?

### U2 — ROADMAP "Backend conventions doc" trigger has fired
**Where:** `ROADMAP.md` lines 124–148.
**What:** Trigger reads "write the doc when Tier 1 MCP tools land — that's when the conventions get applied for the first time." Tier 1 has landed. Trigger fired but doc hasn't been written.
**Tension:** Defer items D1/D2/D3 above all point at this same doc; it's the single resolution for three deferred items. Writing it is justified now.
**Recommendation:** Write the conventions doc before RAG kickoff (it's small — test layout + logging style + error format = 3 short sections). RAG pipeline will need integration tests anyway, so resolving D1's revisit trigger now is cheap.
**Decision needed:** Write it now (preferred), or defer to "before first RAG-pipeline change merges"?

### U3 — Fresh-eyes review of VISION.md + ARCHITECTURE.md wording
**Where:** both top-level docs.
**What:** Per HANDOFF: "user flagged at landing time: 'tired, not full focus' when the vision work landed; wanted to revisit later with fresh attention." Specifically wants USER fresh eyes, not Claude's, since Claude authored most of it.
**Recommendation:** Read both docs through end-to-end with fresh attention. Open question: is the framing still right? Wording sharp enough? Any axis or subsection that reads off?
**Decision needed:** User pass.

---

## Verified clean

- **HANDOFF numerical claims** — 16 skills (count of `plugin/skills/*/SKILL.md` matches), 22 tools (TOOL_HANDLERS dict in server.py has 22 entries), 57 manifest entries (universal=10, PV-FFA=7, Wind=6, Naturschutz=19, MV=15 — sum verified), 5 ref + 2 doctype manifests in scope.
- **ARCHITECTURE structural counts** — 5 meta-rules (`## Meta-rule:` headers), 9 entity types A–I, 6 decision rules.
- **VISION three-axis naming** — Surface/Process/Purpose framing consistent across VISION, ARCHITECTURE, ROADMAP, HANDOFF.
- **Meta-rule names stable** — app-vs-office, scope-orthogonality, integration-adapter, memory-vs-RAG, execution-locality.
- **Domain capitalization** — Naturschutz, PV-FFA, Wind correct across all 16 skills.
- **Bausteine path orthogonality** — all skills use `memory/bausteine/{universal,domain/<X>,state/<X>}/...` shape; no legacy `memory/global/bausteine/`.
- **`list_bausteine` arg shape** — all callers (12 skills) use `(scope?, scope_key?, project_root?)`; no old `(global/domain/project)` shape.
- **Tier 1 MCP tools** — all 5 registered with correct names, signatures, and return shapes; `list_skills` parses `mcp_tools_required/optional/fallback_when_mcp_absent` from skill frontmatter.
- **Memory orthogonality refactor** — `baustein_path()` produces documented layered tree; `_enumerate_paths()` walks it; all Pydantic models carry `scope_key`.
- **Specific-skill spot checks** — save-baustein (extensions D + E), verify-citations (`verified_against_version`), validate-checklist (reference-fetch + new finding types), survey-project (per-file iteration), record-feedback (per-concern iteration + layered path) all confirmed.
- **Orchestrator routing list** — all 16 specialists listed; the 5 previously-missing entries (validate-bausteine, record-feedback, research-references, author-manifest, setup-office) are present.
- **No rag-pipeline-decisions.md verdict contradicts ARCHITECTURE meta-rule 5** — decisions A/B add MCP tools rather than pushing deterministic work into skills.

---

## Recommended fix-now batch (Claude can execute)

Group F1–F9 into one commit ("audit: fix-now drift batch"):

1. F1 — research-references frontmatter + Tier 1 tool migration
2. F2 — author-manifest frontmatter
3. F3 — setup-office / validate-latex-style / draft-cover-mail frontmatter completion
4. F4 — orchestrator `setup_project` in optional
5. F5 — server.py `list_bausteine` description string
6. F6 — ROADMAP cleanup (Tier 1 removal, Tier 2 split)
7. F7 — ARCHITECTURE.md baustein extensions D+E pointer
8. F8 — ARCHITECTURE.md "Designed extensions" → rag-pipeline-decisions.md cross-ref
9. F9 — ROADMAP integration-registry count refresh

After this lands, the audit gate is closed pending user resolution of U1, U2, U3.

## Then — RAG kickoff (gated on U1/U2/U3)

Per `docs/rag-pipeline-decisions.md` implementation order:
1. Backend pipeline additions (OCR/DRM, ColPali, LanceDB schema, SQLite legal-graph, hybrid retrieval, new tools `read_corpus_page_image` + `query_legal_graph`, new chunking strategy)
2. Smoke-test on 3–5 entries
3. Full first ingest (57 entries)
4. Sample search to verify retrieval quality
