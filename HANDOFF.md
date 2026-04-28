# Session handoff — pbs-bureau

End of session 2026-04-28 (third major session). Previous session
landed the architectural foundation (app/office split, memory↔RAG,
practices/partners, 3-layer LaTeX). This session executed the
**`(universal × domain × state)` orthogonality refactor** — the
third meta-rule. Now: every reference / doctype / skeleton / baustein
lives in one of three layered scopes, loaders walk the union per
office's selected `scope`. PBS picks `{PV-FFA, Wind, Naturschutz} ×
{MV}`; future deployments pick their own.

**Read order for next session**:
1. This file (HANDOFF.md)
2. `ARCHITECTURE.md` — meta-rules (3 now) + 9 entity types + 6 decision rules
3. `docs/office-config.schema.yaml` — schema v2 with scope + integrations
4. `extensions/README.md` — layered manifest layout
5. `plugin/skills/orchestrator/SKILL.md` + `PROCEDURE.md`
6. Whichever skill the user invokes

---

## Status snapshot

### ✅ Refactor — 7 phases, 7 commits

This entire session was one coherent refactor. Each phase committed
separately for review-ability:

| Phase | Commit | What |
|---|---|---|
| 1 | `9571692` | Filesystem reshape — `(universal × domain × state)` directory layering, all renames clean. memory/domain → memory/universal; references-manifest.yaml → extensions/universal/; skeletons → universal/<doctype>/; new extensions/{domain,state} tree; memory/bausteine/ + per-project-memory/; office-style.{PV-FFA,Wind}.sty |
| 2 | `694e7a6` | Schema v2 — `scope.{domains,states}`, layered `ManifestMap`, integrations block, migration framework (`office_config_migrations/`). Backend rewiring: new `all_references_manifests()` / `all_doctypes_manifests()` / skeleton-overlay composition. |
| 3 | `75657e5` | Skills — setup-office wizard extended for scope multi-select + integrations + per-domain office-style overlays; research-references walks union of selected manifests; NEW `author-manifest` skill. |
| 4 | `16133c2` | Manifest content moved + gap-filled. Universal-core sliced down to truly-universal frameworks; PV-FFA / Wind / Naturschutz domain manifests populated; MV state manifest extended. ~50 entries across 6 manifests (was 24 in flat federal-core). |
| 5 | `a27378a` | Integration adapter scaffolding — protocol + none-adapter for email, calendar, scanner, phone, accounting. `load_adapter("email")` works; real adapters slot into protocols later. |
| 6 | `35e90fb` (next commit) | Docs sync — ARCHITECTURE.md (orthogonality meta-rule + 9 entity types + 6 rules), ROADMAP.md (modular-integrations item resolved into Phase 5; deferred-domain-population added), README.md (architectural meta-rules + new layout), HANDOFF.md (this file). |
| 7 | `<next>` | PBS deployment update + smoke test (this is what's pending below). |

### ✅ The orthogonality (now hardcoded into the architecture)

Three meta-rules in ARCHITECTURE.md, all enforced:

1. **App vs office** — no PBS-specific values in repo (identity, paths,
   practices, styling come from `office-config.yaml`).
2. **Memory vs RAG** — verbatim legal text in RAG only; memory holds
   workflow logic + §-labels with `references_used[]` frontmatter.
3. **Scope orthogonality** — references / doctypes / skeletons /
   bausteine layered along `(universal × domain × state)`. Office
   declares `scope.domains[]` + `scope.states[]`; loaders walk the
   union.

### ✅ Backend (commits `694e7a6`, `a27378a`)

- `office_config.py` v2: scope, layered ManifestMap, integrations
  block, schema-version dispatcher with migration framework
  (`office_config_migrations/v1_to_v2.py`).
- `config.py`: new layered API — `all_references_manifests()`,
  `all_doctypes_manifests()`, `app_universal_skeleton_for(doctype)`,
  `app_domain_skeleton_for(domain, doctype)`.
- `tools/projects.py`: `setup_project` composes universal skeleton +
  domain overlays.
- `tools/build.py`: TEXINPUTS uses recursive `//` for layered
  skeletons subtree.
- `integrations/{email,calendar,scanner,phone,accounting}/`: each
  has `protocol.py` + `none.py`. `load_adapter(class_name)` resolves
  via office_config; smoke test green for all 5.

### ✅ Skills (commit `75657e5`)

- `setup-office` v0.2: discovers available domains+states by
  listing `extensions/{domain,state}/*` (skipping placeholder dirs);
  multi-select wizard; auto-derives `extensions.{references,
  doctypes}_manifests` map from scope; per-domain office-style
  overlay offer; integration adapter selection per class.
- `research-references` v0.2: scope-aware — walks
  `office_config.all_references_manifests()`, hands off to
  `author-manifest` for new-target-manifest registration; per-manifest
  + union counts in output.
- **NEW `author-manifest`**: parameterized scaffold for new
  domain/state manifests. Used when a scope key doesn't yet have
  content (e.g. first office with Hochwasserschutz domain → scaffold
  `extensions/domain/Hochwasserschutz/...`).

### ✅ Manifests populated (commit `16133c2`)

`extensions/` tree now contains:

- `universal/`: 10 federal frameworks (BauGB, BauNVO, BImSchG,
  UVPG, PlanZV, ROG, EEG, WHG, BBodSchG, BWaldG) + universal
  doctypes (Begründung, Festsetzungen, Umweltbericht, Abwägung).
- `domain/Naturschutz/`: 2 federal Naturschutz-Gesetze (BNatSchG,
  BArtSchV), 2 EU directives (FFH-RL, VRL), 2 BfN-Schriften, 10
  Urteile (BVerwG x6 incl. Marburg + Westumfahrung Halle, EuGH x4
  incl. Białowieża + Holohan), 3 Methodik (Südbeck, Dietz/Kiefer,
  Garniel/Mierwald) + 8 Naturschutz doctypes (Artenschutzgutachten,
  saP-VP/HP, FFH-VP/-VP, LBP, AFB, Kartierbericht).
- `domain/PV-FFA/`: 6 KNE leitfäden + BfN-Schriften 705 (Agri-PV).
- `domain/Wind/`: WindBG + 4 KNE-Wind/Helgoländer leitfäden +
  Albrecht 2014 Fledermaus methodik.
- `domain/Innenentwicklung/`: skeleton-only (populates when a
  bureau with this domain deploys).
- `state/MV/`: 5 Landesgesetze + 5 LUNG/StALU leitfäden + 5
  OVG-MV urteile (3 M 63/06, Körkwitz, Wind vs Denkmalschutz,
  Untätigkeit, Seeadler 2024-06).

### ✅ Phase 7 — PBS deployment + smoke test

`~/.config/pbs-bureau/office.yaml` rewritten to schema v2:
- `scope.domains: [PV-FFA, Wind, Naturschutz]`, `scope.states: [MV]`
- `extensions.references_manifests` — full layered map pointing
  at in-repo manifests (universal + 3 domains + MV state)
- `extensions.doctypes_manifests` — universal + Naturschutz
- `integrations.{email,calendar,scanner,phone,accounting}.adapter: none`
- `schema_version: 2`

Smoke test results (all green):
- Schema v2 loads cleanly
- 5 reference manifests in scope, 2 doctype manifests in scope
- Reference entry total: **57 entries** discoverable via
  `cfg.all_references_manifests()`
- Email routing: `hs@deroekologe.de` → `hendrik` partner ✓;
  unrelated addresses return None ✓
- All 5 integration adapters loadable; `probe()` returns ok ✓

### ⏳ Pending — first task next session

**Full skill-alignment sweep** — all 16 PBS skills reviewed for
consistency with this session's architectural realizations, BEFORE
first-run RAG ingestion. Reasoning: this session changed a lot
(scope orthogonality, layered manifests, new skills, iterate/rewrite
patterns, baustein landing layout, references_used[] frontmatter).
Existing skills were largely written before these emerged — they
likely don't yet leverage or respect them. Aligning them BEFORE
first user-visible sessions means the new architecture actually
flows through to user-facing behavior from day one. Touching skills
is reversible; discovering misalignment post-ingest with bausteine
already saved at wrong paths isn't.

**Alignment checklist per skill** (apply to every SKILL.md +
references/):

- **Scope orthogonality**: does it use
  `office_config.scope.{domains,states}` to filter bausteine /
  references / doctypes? Does it walk `all_references_manifests()`
  or assume the old flat federal-core?
- **Baustein landing site**: when it writes a baustein (save-
  baustein) or queries them, does it respect
  `memory/bausteine/{universal,domain/<X>,state/<X>}/` layout
  with `scope` frontmatter? (Old layout was implicit / flat.)
- **Iterate / rewrite / rerank lens**: where the skill currently
  does bulk retrieval, evaluate per-claim iteration. HyDE-style
  query rewriting where applicable (esp. baustein dedupe).
- **Decision rules + entity types** (ARCHITECTURE.md): are
  generated artifacts placed per Rules 1–6 with the right entity
  type (incl. new H = layered manifests, I = integration adapters)?
- **`references_used[]` frontmatter**: does the skill emit /
  maintain it on memory docs that name laws? Does it read it for
  staleness checks?
- **Layered loaders**: does it call `cfg.all_references_manifests()`,
  `cfg.all_doctypes_manifests()`, `app_universal_skeleton_for(...)`
  + `app_domain_skeleton_for(...)` instead of hardcoded paths?
- **Trigger description accuracy**: still matches what the skill
  actually does after this session's changes?

**Five concrete refactor touchpoints already identified** (most
urgent within the alignment sweep):

- **`verify-citations`** — flat per-cite lookup → iterative:
  ambiguous cite → fetch chapter → narrow → fetch interpreting
  ruling → decide. Strengthens source-grounding naturally.
- **`validate-checklist`** — checklist hits fetch the actual
  reference defining the requirement, not just match section names.
- **`survey-project`** — per-ambiguous-file iteration (filename →
  content sniff → last-modified → related files) instead of
  one-shot classification.
- **Stellungnahmen-/Abwägung handling** (record-feedback +
  future draft-abwaegung) — per-concern iteration: fetch baseline
  + relevant ruling + similar past Abwägung per concern.
- **`save-baustein`** — add dedupe guard with HyDE-style
  paraphrase-search; ensure scope frontmatter + correct
  `memory/bausteine/<layer>/<key>/` landing path.

**Skills also touched this session that need follow-up review**:
- `orchestrator` — does its decision-tree know about scope, the new
  setup-office wizard expansion, author-manifest hand-off?
- `validate-bausteine` — sweeps `memory/bausteine/` — must walk the
  new layered tree, not assume flat.
- `record-feedback`, `promote-to-skill` — likely need scope-frontmatter
  awareness for emitted records.
- `draft-textteil-b`, `draft-textteil-c`, `draft-cover-mail`,
  `review-draft`, `validate-latex-style` — review for layered-
  manifest + scope-aware retrieval.

Already aligned (don't re-touch unless something changes):
`setup-office` v0.2, `research-references` v0.2, `author-manifest`
v0.1.0 — all written/updated in Phase 3 of this session.

These are skill-protocol changes (markdown SKILL.md +
`references/<file>.md`), not backend changes. The MCP tools
(`search_corpus`, `read_corpus_file`, manifest accessors) already
support what the protocols need.

Then RAG-options assessment (BEFORE first ingest — re-ingesting 57
entries through OCR + DRM-removal + multimodal pipelines is
expensive, so decide pipeline shape first):

**Pre-ingest decisions to make** (ROADMAP items already drafted —
this is the "which to wire in for first ingest, which to defer"
pass):

1. **Text-retrieval baseline**: stick with bge-m3 + cross-encoder
   reranker, or swap straight to ColBERT-v2 (RAGatouille/PLAID)?
   Default: keep bge-m3 baseline; ColBERT only if benchmarks for
   German legal text show meaningful gain. Research: recent
   benchmarks on German legal corpora; ColBERT-v2 vs bge-m3 on
   long technical documents.
2. **Multimodal scope for first ingest**: which subset of the
   four multimodal sub-pieces (page-image retrieval, table
   extraction, OCR for scanned PDFs, DRM removal) ship in first
   pipeline vs follow-up?
   - **OCR**: likely yes — many older Verfahrenserlasse / archived
     Stellungnahmen are scanned. Block on testing the corpus mix.
   - **DRM removal** (qpdf/pikepdf): yes if any KNE/BfN PDF has DRM;
     test on actual fetches. Cheap to add, no-op if no DRM.
   - **Page-image retrieval (ColPali)**: optional first-cut. Decide
     based on diagram-heavy vs text-heavy content mix.
   - **Table extraction (Camelot/Tabula)**: optional. Helgoländer-
     species×distance is highest-value table; isolated work.
3. **Query rewriting placement**: backend preprocessor (transparent
   to skills, deterministic variants like synonym expansion) vs
   skill-level (HyDE — needs model in the loop)? Decide before
   ingest only because it might affect chunking strategy.
4. **Chunking strategy review**: each manifest entry specifies
   `chunking_strategy` (per-paragraph, per-randnummer, per-section,
   per-article). Worth a sanity-check against the layered
   architecture before they get baked into LanceDB.
5. **Reranker model choice**: confirm reranker (bge-reranker-v2-m3
   default? Or jina-reranker-multilingual?) — German support
   matters.

**Output of assessment**: a brief decision document (could be
`docs/rag-pipeline-decisions.md` — ~1 page) capturing what gets
wired in for first ingest and what's deferred.

**"RAG" here = the whole retrieval/lookup subsystem**, not just
text-vector retrieval. Four mechanisms in scope:
- Unstructured text RAG (verbatim cites, prose)
- Structured tool calls (graph traversal, registry queries — the
  ROADMAP "structural retrieval" item: legal §-graph, project-
  cross-project, verfahren state-machine become typed MCP tools
  rather than text-search guesses)
- Multimodal RAG (page-image, table extraction, OCR, DRM removal)
- Hybrid (text + structured + multimodal candidates merged,
  reranker chooses)

If assessment decides to wire any non-trivial change in (e.g. add
HyDE, swap to ColBERT-v2, build the legal §-graph as a typed tool,
add ColPali for page images), **implement that change BEFORE first
ingest**. Re-ingesting 57 entries through a wrong pipeline is the
cost we're avoiding; same logic for re-emitting bausteine if the
retrieval API changed shape after they were saved.

Implementation order within this phase:
1. Assessment — produce decisions doc
2. Backend changes (chunking, new tools for structured retrieval,
   new pipeline stages for multimodal)
3. Skill changes that assume the new mechanisms
4. THEN proceed to RAG kickoff below

Then RAG kickoff:

1. **`/reload-plugins`** so Claude Code picks up the updated SKILL.md
   files (incl. the protocol refactors above + setup-office v0.2,
   research-references v0.2, new `author-manifest`).

2. **Run `research-references` first-time fetch** — ~57 entries
   across universal + 3 domains + MV. RTX 5090 picks up CUDA
   automatically; bge-m3 + reranker download (~3GB) on first
   ingest call (or whatever the assessment decided).

3. **Sample search** to verify the chosen retrieval pipeline
   returns sensible hits. If quality is poor → revisit assessment
   choices (e.g. swap to ColBERT-v2, add HyDE).

After that:
- Bind first project (any existing hidrive project — orchestrator
  routes through survey-project → bind_project, no schema migration
  needed).
- Optional: wire `\OfficeLogoPath`, `\OfficeSpecializations` into
  `office-style.sty` letterhead.

### ❌ Deferred (not blocking)

See ROADMAP.md for the full list. Highlights, including 5 new
v1.x-v2 design items added late in the session:

**Carried from before:**
- Real email/calendar/scanner/phone/accounting adapters
  (`thunderbird-maildir.py` etc.) — protocols + none-adapters in
  place; concrete adapters land per demand.
- Innenentwicklung domain population — when a bureau needs it.
- Per-domain memory directories (`memory/domain/<X>/`) —
  introduce when first domain-scoped reference content lands
  (Artenschutz verfahren reference is the natural trigger).
- Reference versioning, internal cross-refs, subagents, hooks —
  v2 work.

**New design items added this session** (topic-only, design TBD):
- **Audit trail** — unified change/decision/version tracking across
  artifacts, references, manifests, configs, integrations, bausteine,
  plans, correspondence. Currently scattered (decisions.md,
  snapshots/, changelog.md, git history) without coherent design.
- **Human-readable artifact generation at checkpoints** — every
  meaningful checkpoint (send-gate, phase transition, draft-invoice,
  baustein-promotion, config-change) produces a PDF/HTML alongside
  machine state for human review. Today only LaTeX has clean output
  via compile_latex.
- **Web UI for collaborative review** (Coolify-hosted) — share
  PDFs with colleagues / partners / clients, annotate + comment,
  read annotations back via MCP. Research candidates: Hypothesis,
  Cryptpad, Nextcloud+Collabora, Stirling-PDF, HedgeDoc, PDF.js+
  custom, Onlyoffice, PaperHive. Prefer existing OSS over custom.
- **PM + invoicing** — per-project billing.md ledger, log-time +
  draft-invoice skills, accounting-adapter implementations. Tied
  to send-gate (Vorentwurf snapshot = billable milestone).
- **Integration registry** — 4th layered manifest type
  (integrations-manifest.yaml per scope) cataloging all callables
  (MCPs + internal adapters + skills) with metadata for capability-
  based queries. NEW skill `register-integration` to add entries;
  NEW backend tool `find_integrations(capability=, scope=)`.

These five items inter-connect: the integration registry is the
discovery layer; audit trail records what happens; checkpoint
renders produce the human-readable artifacts; the web UI distributes
them; PM+invoicing is one specific consumer of all the above.
Worth designing them as a coherent subsystem rather than piecemeal.

---

## Key architectural decisions made (with reasoning)

### From this session

| Decision | Reasoning |
|---|---|
| **`(universal × domain × state)` orthogonality** | Real planning bureaus decompose work along these axes. Forcing a single flat federal-core mixes "universal-to-every-bureau" with "domain-of-PBS-interest" content; future deployments would need to fork the manifest. Layered loaders + scope selection give clean composition. |
| **Domain manifests live in repo, not per office** | Domain content (KNE-PV leitfäden, Helgoländer Papier) is the same for every bureau working in that domain. Shipping in repo + offices selecting via scope avoids drift across deployments. |
| **State manifests live in repo too**, with per-office overlay path | State laws are uniform across MV; ship canonical content in repo. Office-local additions (regional Leitfäden specific to NW-MV) are an optional overlay, not the default. |
| **Bauchstein scope is single-valued** | A baustein with multi-scope candidates is a signal that the content isn't really one reusable unit — promote to universal or split. |
| **`memory/domain/` renamed → `memory/universal/`** | Old name was misleading: the content was universal (every German bureau), not domain-scoped. Layered manifests took over the domain word. |
| **NEW `author-manifest` skill** (single, parameterized) | Same wizard logic for domain vs state vs references-vs-doctypes; three skills would duplicate. |
| **Schema migration framework from day one** | No second deployment yet, but pattern in place avoids retrofit pain. v1_to_v2 migration is real and tested. |
| **Integration adapter scaffolding now** | ROADMAP said "adapter boundary in place from day one". Wire-thin protocol + none-adapter cost ~5 min per class; sets discipline. |
| **doctypes split universal vs Naturschutz domain** | Begründung/Festsetzungen are universal; Artenschutzgutachten/LBP/saP are Naturschutz-domain. The domain split surfaced this; existing doctypes registry was conflating layers. |
| **TEXINPUTS gets `//` for skeletons** | Layered tree (universal/<doctype>/Textbausteine + domain/<X>/<doctype>/Textbausteine) needs recursive kpathsea search. |

### Carrying forward (from previous sessions)

| Decision | Reasoning |
|---|---|
| **App vs office-config split** | Repo deployable to other German planning bureaus; PBS-specific values in `office-config.yaml` outside repo. ARCHITECTURE.md meta-rule + skill-author checklist enforce. |
| **Memory ↔ RAG split** | §-refs as labels OK; verbatim text only in RAG; cross-cutting docs declare `references_used[]`. |
| **practices vs partners** | Internal sub-practices ≠ external collaborators. Email match patterns route either way. |
| **3-layer LaTeX stack** | App `.cls` + `office-style.sty` + project `Projektdaten.tex`. Identity macros auto-generated. Now layered for skeletons too: universal + domain overlays. |
| **No PBS project migration this session** | PBS keeps current per-doctype-LaTeX-repo layout. Orchestrator binding flow uses survey-project for adoption. |

---

## Key paths reference (post-refactor)

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/` | Claude Code plugin (16 skills now incl. author-manifest) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/templates/skeletons/{universal,domain/<X>}/<doctype>/` | Layered skeletons composed at scaffold |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/plugin/templates/office-style/office-style.{default,PV-FFA,Wind}.sty` | Office-style + per-domain overlays |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/extensions/{universal,domain/<X>,state/<X>}/` | Layered references + doctypes manifests |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/universal/` | Universal domain knowledge (formerly memory/domain/) |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/bausteine/{universal,domain/<X>,state/<X>}/` | Saved baustein landing site |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/memory/universal/per-project-memory/` | Schema docs for per-project `_ai/` |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/backend/mcp-server/src/pbs_mcp/integrations/<class>/{protocol,<adapter>}.py` | Pluggable integration adapters |
| `/home/g/dev/Gunther-Schulz/pbs-bureau/backend/mcp-server/src/pbs_mcp/office_config_migrations/` | Schema migration framework |
| `~/.config/pbs-bureau/office.yaml` | **PBS office config — needs Phase 7 update to v2 schema** |
| `/mnt/data2t/hidrive/.../_ai-office-state/` | PBS office state |
| `/mnt/data2t/hidrive/.../_ai-references/` | PBS legal references RAG corpus (still empty — Phase 7 fetch fills it) |
| `/mnt/data2t/hidrive/.../Projekte/` | All client projects |
| `~/dev/Planungsbüro-Schulz/` | PBS local per-doctype LaTeX working copies |

---

## Working-style notes

1. **Commit between phases** — 7 commits in this session, one per
   refactor phase, each a stable testable milestone. Lets
   sanity-check progressively and rollback selectively.
2. **Backend smoke-test after every backend change**, even one-liner —
   `python -c "from pbs_mcp import office_config; cfg = office_config.load(); print(cfg.scope)"` caught a migration bug in Phase 2 quickly.
3. **Prefer git mv** for file moves so rename detection preserves
   history. The `extensions/universal/references-manifest.yaml`
   shows up in git log with full history of the old
   `references-manifest.yaml`.
4. **Apply ARCHITECTURE.md rules rigorously** — when Phase 4 split
   the doctypes into universal vs Naturschutz, the orthogonality
   meta-rule made the split obvious; without it I'd have hand-waved
   Naturschutz-only types into the universal registry.
5. **Cite-only entries are bibliographic-only** — they validate
   citation form, not claim accuracy. The user surfaced this clearly
   during the gap-fill discussion; documented in
   `manifest-schema.md`.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **User's plugins active**: bildhauer, clippy, skill-craft,
  experiment-lab, gis-utils, plugin-dev, pbs (this one).
- **Plugin cache symlink**: re-run `bash dev-link.sh` if
  `~/.claude/plugins/cache/pbs-bureau/pbs/0.1.0` is a regular dir.
  Note: setup-office and research-references skill versions bumped
  to 0.2.0; new author-manifest at 0.1.0. Plugin version itself
  unchanged.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Dotfiles**: global CLAUDE.md and settings.json tracked in
  `~/dev/Gunther-Schulz/dotfiles/claude/`. After editing either,
  commit + push the dotfiles repo.
