# pbs-bureau roadmap

Deferred feature backlog. Each item is "designed enough to know it
matters but not yet specified in detail." Pick up in priority order
when the system is ready or when a real project needs the feature.

For session-state (what's done vs in-progress), see `HANDOFF.md`.
For taxonomy + decision rules, see `ARCHITECTURE.md`.

---

## v1.x — likely soon

### Tier 2 MCP cross-reference tools (during first project work) — partial

**Status**: `find_bausteine_by_reference` landed in session 4 (see
`backend/mcp-server/src/pbs_mcp/tools/memory.py`). The remaining
two tools below are deferred until the first reference refresh
fires and the manual fallback proves friction.

**Why**: When `research-references` updates a law and needs to
find every dependent baustein and memory doc, the cross-reference
graph is partial — bausteine lookup landed but memory-docs and
manifest-entry single-lookup are still planned.

**Sketch (remaining)**:

- `find_memory_docs_by_reference(...)` — cross-cutting memory docs
  declaring `references_used[]` frontmatter.
- `find_manifest_entry(id)` — single-entry lookup across the
  union of in-scope manifests.

Build when the first reference refresh fires and the manual
fallback proves friction.

> **Tier 1 MCP discovery layer** (`list_reference_manifests`,
> `list_doctypes_manifests`, `list_skills`, `list_skeletons`,
> `list_bausteine`) landed in session 4 — see
> `backend/mcp-server/src/pbs_mcp/tools/discovery.py` and
> `tools/memory.py`. Removed from this ROADMAP per "Tracking
> conventions" rule.

### Tier 3 MCP introspection tools (deferred)

**Why**: Skills currently know office-config schema field paths
(`office_config.office.signature_block` etc.); changes to schema
ripple through every skill. Same for per-project state queries
that today are file-grep.

**Sketch**:

- `get_active_practices()`, `get_signature_block(practice?)`,
  `get_office_identity()` — schema introspection helpers.
- `get_project_state(project)`, `list_snapshots(project)`,
  `list_correspondence(project, since?)`, `list_decisions(project)`
  — per-project state queries.
- `list_office_style_overlays()` — returns the active `.sty`
  stack per active domains.

Don't pre-build. Add when first redundant string-matching is
observed in real skill code.

### Schema migration framework for memory data records

**Why**: Office-config has migrations
(`office_config_migrations/v<N>_to_v<N+1>.py`) that forward-migrate
on load. Memory (record) entities (bausteine, manifests'
entries, state.md, feedback entries) have no equivalent. Today
that's fine because PBS has zero saved bausteine — but the moment
first ingest writes any, the next schema change becomes painful
(touch every file by hand). The new `verified_against_version`
field added to `references[]` during the alignment sweep is a
schema reservation precisely to avoid this pain; the next
addition still needs migration support.

**Sketch**:
- Mirror the office-config pattern: `pbs_core/memory_migrations/`
  per-record-kind (bausteine, manifests, state, feedback) with
  `migrate_v<N>_to_v<N+1>(data: dict) -> dict` exporters.
- Each record type carries `schema_version: <N>` in frontmatter.
- The MCP tool that writes (e.g., `save_baustein`,
  `update_project_state`) checks the schema version on read and
  applies migrations in-memory; writes back with updated version.
- `setup-office` reconcile mode triggers a sweep migration of
  all in-scope records.
- Decision-rule update in ARCHITECTURE.md: Memory (record) edits
  go through MCP tools that handle migration, never direct Edit.

**Pull-forward trigger**: first user-visible session that saves
a baustein. Until then, no baustein exists to migrate.

### Boundary placement refinements (from slice 14, 2026-04-29)

**Why**: Audit slice 14's first run flagged 3 placement findings —
deterministic logic that should move from skills into MCP tools,
or from hardcoded Python into office-config. None are BLOCKERS;
all are honestly defer-worthy (each requires schema + handler +
tests for a new tool, or a config schema bump). Captured here
rather than batched into a same-session fix to keep diff scope
sane. See full audit at
`docs/audits/boundary-adherence-20260429.md`.

**Sketch — three independent items**:

- **`dedupe_bausteine` MCP tool**: dedupe procedure currently
  described in `save-baustein/SKILL.md` lines 65-75 (title + tag
  overlap matching). Move algorithm into MCP tool with reproducible
  scoring rule + Pydantic candidate output schema. Pull-forward
  trigger: when matching grows beyond title+tag (HyDE paraphrase
  search via search_corpus over indexed bausteine is already
  flagged as the next iteration).

- **`office-config.conventions.path_classification`**: ingest.py
  `_infer_source_subtype` (lines 182-226) hardcodes substring
  patterns like `/_ai/snapshots/`, `/gesetze/bund/`,
  `/bausteine/universal/`. Convention-correct per default layout
  but not invariant across deployments (`.ai/` instead of `_ai/`,
  flat `Gesetze-Bund/` instead of nested, etc.). Move classification
  rules into office-config schema as a tunable block; bump v3 → v4.
  Pull-forward trigger: before first multi-deployment install OR
  before any deployment with non-default folder names. **Highest
  priority of the three** because misclassification lands as silent
  metadata in LanceDB (re-indexing cost post-ingest).

- **`record_baustein_use` MCP tool**: `record-feedback/SKILL.md`
  lines 117-120 directs direct `Edit` of baustein frontmatter
  fields `rejected_uses[]` / `successful_uses[]`. Skill itself
  flags this as known debt ("future MCP tool record_baustein_use
  could atomicize"). Build the tool: takes baustein name +
  scope/key + kind ∈ {rejected, successful} + project/date/feedback_path,
  owns frontmatter mutation with validation. Pull-forward trigger:
  when frontmatter gains cross-reference structure (e.g., feedback_id
  linking).

### Pioneer-instance validation strategy

**Why**: Per VISION.md "PBS as pioneer instance" — a one-user
prototype generates thin validation. Risks (survivorship bias,
architectural over-fitting, sparse evidence sample, confirmation
bias) are real. Without explicit validation strategy, the
pioneer claim relies on "Gunther uses it and it seems to work"
— too thin to support proving-ground or research-lab purposes.
Compounded by current market reality: project density may be
sparse for a while; validation can't wait for projects to pile
up.

The question to answer: **what counts as valid evidence for an
early-mover prototype with sparse real-world tests?**

**Sketch — four complementary evidence types** (directly
addresses risks named in VISION.md):

- **Architectural validation** (cheap, immediate). Tests
  whether the architecture works mechanically — skills
  compose, layered manifest scope filtering operates,
  source-grounding fires, audit trail records what's expected,
  frontmatter dependency declarations resolve correctly.
  Doesn't require real projects; build as backend test suite
  with per-meta-rule invariants. Closest evidence type to
  unit-test discipline applied at the architecture level.

- **Failure-mode probing** (cheap, immediate). Stress-test
  the trust + sparring infrastructure under deliberate
  adversarial conditions — ambiguous citations, conflicting
  Stellungnahmen, intentionally weak argumentations,
  sycophancy bait ("don't you agree this looks fine?"),
  source-grounding evasion attempts. Verify guardrails
  actually fire under stress. Build as validation harness
  with reusable adversarial scenarios; runnable on demand.

- **Historical project replay** (medium effort, own data).
  Run PBS on past projects (without the AI seeing the actual
  sent versions); compare AI's drafts + reasoning chains
  against what was historically shipped. Catches over-fitting
  to user style; tests whether patterns reproduce expert
  judgment over PBS's own track record. Confirmation-bias
  risk: same person designed both architecture and originals,
  so agreement isn't independent verification.

- **Mock project + peer review** (medium effort, external
  input — user's original suggestion). Construct realistic
  synthetic project; another planning professional (Hendrik
  first, possibly others later) reviews PBS outputs. Their
  verdict: would they sign this? Would they have caught what
  AI missed? What's wrong, structurally or fachlich?
  Strongest external-validation path that doesn't depend on
  real client work.

Four distinct evidence types: **architecture / stress / own-
baseline / external-professional**. None requires waiting for
the next real project. Together they generate substantive
evidence even during low-project-density periods.

**Deferred (more ambitious, higher setup cost)**:

- Compare against published professional standards
  (Bauleitplanung leitfäden, BMI guidance, BBSR examples).
- Hypothetical model cases (publicly discussed regional
  planning challenges; PBS as if commissioned).
- Replay published BVerwG case law (simulate PBS at the time
  of a real dispute; compare against actual court outcome).
- External presentation as IP-transferability test (paper,
  conference, demo with feedback collection).

**Pull-forward triggers**:

- PBS becomes operational (Tier 1 MCP + alignment sweep + RAG
  kickoff complete). Validation should start at first
  operational use, not at first crisis.
- Project density stays low for >1 month — evidence
  accumulation via real work too slow to be sole strategy.
- First consulting / second-deployment conversation surfaces —
  need transferable evidence to share.

**Open questions** (refine and prioritize at task #21
pre-RAG audit; by then operational reality will inform
trade-offs):

- Effort budget per session: validation vs. real work split?
- Where does evidence land — per-type log files? new
  `evidence/` tree alongside `memory/`? Within the audit-trail
  ROADMAP item?
- Decision criteria: when does accumulated evidence justify
  productization, scope expansion, or external publishing?

### SKILL.md version-bump reminder hook

**Why**: Per meta-rule 4 (execution-determinism), hooks earn their keep on out-of-band
detection. Pure-advisory exception worth a 5-line
PostToolUse hook: when `plugin/skills/**/SKILL.md` is edited,
remind to bump `version:` and run `dev-link.sh`. No data
integrity at stake — just discipline.

**Order**: defer until a real version-bump miss causes friction.
Cheap to add later.

### Email adapter implementations

**Why**: integration adapter scaffolding is in place
(`backend/.../integrations/email/{protocol,none}.py`) — but no real
adapter yet. v1 has manual `.eml` drop into
`<project>/Schriftverkehr/eml/`. For complete project context the
assistant needs full inbox access; manually-saved `.eml` files are a
curated subset.

**Sketch**: first concrete adapter is `thunderbird-maildir.py` —
polls Thunderbird's local maildir/mbox at
`~/.thunderbird/<profile>/Mail/`, filters by domain whitelist +
project-keyword matching, drops matched messages into the right
project's `Schriftverkehr/eml/`. Implements
`pbs_mcp.integrations.email.protocol.EmailAdapter`. After that:
`imap.py` for self-hosted offices.

### Phone call note format

**Why**: `Schriftverkehr/telefonnotizen/` is a planned folder but no
spec exists for what a call note file should contain.

**Sketch**: small markdown spec — frontmatter (date, party,
contact, project, type=call, duration), body sections (Kontext,
Zusammenfassung, Entscheidungen, Folgeaktionen). Could be authored
into `<repo>/memory/universal/` as a reference content file. Future
integration: `phone.adapter: call-log-csv` reads a phone-system CSV
export and proposes call-note creations.

### Domain manifest population — Innenentwicklung

**Why**: `extensions/domain/Innenentwicklung/references-manifest.yaml`
is currently a skeleton. Will need population when first office with
this domain (urban planning, no renewables) deploys, OR when PBS
takes on an Innenentwicklung-only project.

**Sketch**: candidates — Difu-Leitfäden, BBSR-Veröffentlichungen,
BVerwG-Rechtsprechung zu §13a/§13b BauGB. Use `author-manifest`
already-existing skill to seed; `research-references` populates.

### Agentic retrieval — iterate searches per claim, not per section

**Why**: Current RAG pattern (planned for first-run) is bulk: skill
issues one or a few `search_corpus` calls per drafting section,
stuffs results into prompt, drafts. State-of-the-art is *agentic*:
the orchestrator iterates one search per claim during drafting —
fetches §44 BNatSchG when about to write the §44 sentence, fetches
the BVerwG-Freiberg ruling when about to cite CEF-Wirksamkeit.
Better citation grounding (each claim has its own retrieval), less
context bloat (no over-fetching upfront), more natural for Claude.

**Sketch (post-first-run)**:
- Mostly a skill-protocol question, not infrastructure. Update
  `draft-textteil-b` / `draft-textteil-c` / `draft-cover-mail`
  protocols: instead of "fetch all sources at start", say "before
  each citation-bearing claim, search for the supporting reference,
  cite from the result."
- The MCP backend (`search_corpus`, `read_corpus_file`) already
  supports per-call retrieval — no backend change needed.
- Source-grounding rule strengthens naturally: every cited §-ref
  is backed by a tool call in the same drafting turn.

**Open questions**:
- Latency: many small searches per draft vs few large ones. With
  bge-m3 + CUDA the per-search cost is low; the question is total
  drafting wall time.
- Hybrid: bulk-fetch the obvious universal references (BauGB-
  framework) once at start, agentic-fetch the specific cites?
- When to evaluate: after first-run sample-searches show whether
  the bulk pattern produces grounded enough citations.

### Late-interaction retrieval (ColBERT-v2)

**Why**: Current stack uses bge-m3 (single-vector dense embedding)
+ a cross-encoder reranker. State-of-the-art for long technical /
legal text is often *late-interaction* models like ColBERT-v2 —
token-level retrieval that scores fine-grained matches without the
bottleneck of compressing the whole document into one vector.
Particularly strong on German legal text where exact-phrase
matching matters.

**Sketch (conditional)**:
- **Trigger**: only if first-run sample-searches show quality
  issues — bge-m3 + reranker is the right baseline; don't preempt.
- **Drop-in**: ColBERT-v2 has Python implementations (PLAID,
  RAGatouille) that slot under the same `search_corpus` interface.
- **Trade-off**: late-interaction stores more per chunk (token-
  level vectors), so disk/memory footprint grows. RTX 5090 + 32GB
  VRAM handles it but the LanceDB schema needs adjusting.

**Open questions**:
- Evaluation set: need a small benchmark of "for query X, the right
  reference is Y" pairs to objectively compare bge-m3 vs ColBERT
  on PBS's actual corpus.
- Coexistence with multimodal page-image retrieval (ColPali — see
  next item): probably both, used for different content kinds.

### Query rewriting (HyDE + decomposition + expansion)

**Why**: We have ZERO query rewriting today. User/skill issues a
literal-keyword query → gets dense-retrieval matches. State of the
art rewrites the query before retrieval to bridge vocabulary gaps:
- **HyDE** (Hypothetical Document Embeddings): the model first
  drafts a hypothetical answer, embeds *that*, retrieves against
  the corpus. Catches paraphrase mismatches.
- **Decomposition**: split a multi-part query into sub-queries,
  retrieve each, union.
- **Expansion**: add synonyms / variants ("§44 BNatSchG Tötungs-
  verbot" → also search "Tötung Verbot §44", "signifikant Tötungs-
  risiko §44").

**Sketch**:
- HyDE for **baustein retrieval** (find similar bausteine when
  user is about to write a similar argument): the most natural fit.
- Decomposition for **multi-§-claim drafting**: a sentence that
  cites BauGB §13a and BNatSchG §44 issues two retrievals.
- Expansion for **legal lookup**: deterministic, can be a
  preprocessor on top of search_corpus.
- **save-baustein dedupe** — paraphrase the candidate in 3 variants,
  search each, union, decide if duplicate. Currently no dedupe
  guard in place at all.

**Open questions**:
- Where to apply: query-rewrite as preprocessor in the MCP backend
  (transparent to skills), or as an explicit skill responsibility?
  Likely backend for cheap variants (expansion), skill for HyDE
  (needs the model in the loop).
- Rewriting cost: HyDE adds one model call per search. Acceptable
  for high-stakes (drafting), maybe too much for bulk operations.

### Multimodal RAG (page images, tables, scanned PDFs, copy-protected PDFs)

**Why**: Current ingest pipeline is text-only. We lose:
- **Diagrams** in KNE-Anlagengestaltung (Modulreihen-schematics,
  row-spacing), KNE-Standortsteuerung (decision flowcharts).
- **Charts** in BfN-Schriften 705 (Agri-PV adoption, land-use).
- **Tables** in Helgoländer Papier (species × distance recommen-
  dations) — text-extracted tables often arrive mangled.
- **Maps** in LUNG-MV-Artenschutzleitfaden (Bestandskarten,
  Schutzgebiete).
- **Future Kartierberichte** from Hendrik — fundamentally visual
  (maps, distribution plots, habitat photos). Pure-text RAG would
  be useless for these.

**Sketch (4 sub-pieces)**:

1. **Page-image retrieval (ColPali / Nomic Vision)** — embed each
   PDF page as an image; query → page images; Claude (vision-
   capable) reads them. Lowest pipeline complexity; decent quality.
   Coexists with text-RAG (text for keyword-precise, images for
   "I need to see the diagram").

2. **Targeted table extraction** — Camelot / Tabula / Unstructured
   detects tabular blocks at ingest, extracts as structured records.
   Helgoländer-style species×distance tables become symbolic
   queries ("min distance for Schreiadler"). High value where it
   applies; not every PDF has tables worth this treatment.

3. **Scanned PDFs (OCR)** — many older Verfahrenserlasse, archived
   Stellungnahmen, scanned Behörden-correspondence are image-only
   PDFs with no embedded text. Need OCR at ingest. Tools:
   `ocrmypdf` (wraps tesseract; preserves PDF structure +
   adds searchable text layer), `tesseract` direct + custom
   reconstruction. German-language model essential.

4. **Copy-protected PDFs** — KNE/BfN/Verlag-published leitfäden
   sometimes ship with DRM (printing/copying disabled, sometimes
   password-protected). For internal RAG ingest of legitimately-
   acquired material we need a removal path:
   - `qpdf --decrypt` for owner-password DRM (most common,
     trivial to strip)
   - `pikepdf` (Python; same backend) for programmatic ingest
   - `mutool clean -d` (MuPDF) as fallback
   - Investigation: which DRM kinds appear in PBS's actual
     publisher mix; which tool handles each cleanly.
   - Legal: DE Privatkopie / wissenschaftliche Eigennutzung law
     covers internal-use ingest of legitimately-acquired material;
     redistribution is separate. Document the policy.

**Recommended architecture** (decided):

| Step | Who | Why |
|---|---|---|
| Pre-process PDFs at ingest (page render, OCR, table extract, DRM removal) | Local Python tools | Deterministic, one-shot |
| Embed page images for retrieval | Local ColPali on RTX 5090 | Bounded corpus, consistency with bge-m3 text-RAG |
| Match query → page images | Local LanceDB | Same store as text-RAG |
| **Read and reason about returned images** | **The Claude session itself** | Already in the loop, vision-capable, has project context |

The orchestrator runs IN a Claude session — Claude is already
vision-capable. MCP backend returns image bytes (new tool
`read_corpus_page_image` or extension to `read_corpus_file`); the
session passes them as image content blocks; Claude reads + reasons
directly. No separate vision-LLM deployment needed for interactive
work.

A separate local vision model (Llama 3.2 Vision, Qwen2-VL, Pixtral)
or API vision call is only needed for **batch/headless** processing
that runs outside a live Claude session — e.g. a future
"weekly auto-scan new Stellungnahmen for action items" cron. Defer
that until such a use case lands.

**Open questions**:
- Coexistence: page-image retrieval + text-RAG returning different
  hit kinds — how does the orchestrator decide which to send to the
  model? Probably hybrid retrieval that includes both kinds in
  candidate pool, reranker decides.
- Storage cost: page images are large; LanceDB blob storage or
  filesystem references?
- Token-budget control: every multimodal hit means image bytes in
  the context. Cap on images-per-turn?
- Table extraction precision: structured tables are queryable but
  the extractor mis-identifies blocks. Need fallback to text+image.

### Structural retrieval (legal §-graph + project graph + verfahren state-machine)

**Why**: PBS corpus and project state are full of latent structure
that text-only retrieval ignores. Recurring pattern observed in
this session: we keep designing things text-first and finding
ourselves needing a graph or registry later (integration registry,
audit trail are exactly this — formalizing what's currently
implicit).

**Meta-principle**: when something is queried by attribute /
capability / relationship, design it as data, not prose.

**Three concrete graphs**:

1. **Legal §-graph** — §44 BNatSchG cites §15, §1; BVerwG-9-A-22-13
   interprets §45 Abs.7 Nr.5; KNE-Anlagengestaltung references
   §44 Abs.1; LUNG-MV-Artenschutzleitfaden tracks BNatSchG §44
   Anwendungspraxis. Today: nothing — keyword search only. Graph
   would let symbolic traversal: "find all rulings interpreting
   §45 Abs.7", "what cites this baustein's underlying §s".
   Built at ingest (extract §-references from law/ruling/leitfaden
   text), updated by research-references on each refresh.

2. **Project-cross-project graph** — projects × doctypes × phases
   × decisions × partners × clients. Today: state.md per project,
   no aggregation. Graph would answer "all PV-FFA projects in
   phase 5b with Hendrik as partner", "which projects share this
   client", "decision X across projects".

3. **Verfahren state-machine** — bauleitplanung-phasen.md is *prose*
   describing the 13 phases + transitions. Could be a state machine
   the orchestrator queries: "given current phase X, valid next
   transitions"; "what's required to fire transition Y". Used by
   orchestrator for phase-transition validation, by validate-
   checklist for "is this artifact ready for phase X" gates.

**Open questions**:
- Storage: LanceDB has no graph queries; SQLite + manual graph
  schema, or a real graph DB (Kùzu / Neo4j)?
- Maintenance: §-graph and project-graph need to update on every
  research-references run / state.md write. Build derived-data
  pipeline?
- Integration with audit trail (separate ROADMAP item): an audit
  event is naturally a graph-edge ("decision X was logged in
  project Y by partner Z at time T").

_(Skill-protocol refactor for iterate/rewrite patterns —
verify-citations, validate-checklist, survey-project,
Stellungnahme/Abwägung handling, save-baustein dedupe — promoted
out of ROADMAP into immediate next-session work. See HANDOFF.md
"Pending — first task next session.")_

---

## v1.x-v2 — when first project needs it

### Plugin / deployment shipping bundle

**Why**: PBS is designed deployable to other German Planungsbüros
(per ARCHITECTURE.md meta-rule 1: app vs office). What gets
shipped to a second office is currently undocumented. Without
a coherent bundle definition, second-deployment friction is
unknown and the deployment story stays implicit.

**Sketch (small doc, ~1 page)**: at `docs/deployment.md`:
- Plugin payload: `plugin/skills/`, `plugin/templates/`,
  `plugin.json`, `dev-link.sh`. Versioned via plugin.json.
- Backend payload: `backend/mcp-server/` with pinned deps.
- Memory payload: `memory/universal/` (knowledge content),
  `memory/bausteine/` skeleton (empty subdirs for layered
  scope), `memory/product-backlog.md` template.
- Extensions payload: `extensions/universal/` (manifests),
  `extensions/{domain,state}/` skeletons (placeholder dirs for
  unselected scope keys).
- Office-config: not shipped — generated by `setup-office` per
  deployment.
- Docs: README → setup-office, ARCHITECTURE.md, ROADMAP.md.
- What is NOT shipped: `_ai-references/` corpus, per-project
  data, office-config.yaml.

**Pull-forward trigger**: first concrete second-deployment
conversation (another Planungsbüro evaluates the app, or PBS
themselves wants to test fresh-install on a clean machine).

### Maps/GIS integration

**Why**: Joint Schulz+Hendrik projects use both PBS text-document
work AND Hendrik's GIS/QGIS workflow. Need clean coexistence of two
MCP servers + shared context.

**Components**:
- gis-utils MCP server (already exists as a separate plugin —
  `gis-utils@gis-utils`)
- pbs-bureau MCP server (this repo's backend)
- Communication / shared state at `<project>/_ai/state.md` with
  `practices: [schulz, hendrik]` flag

**Open questions**:
- Should Hendrik's per-project `CLAUDE.md` (workflow.yaml + scripts/)
  be readable by pbs-bureau orchestrator? Or strict separation?
- How do Karten/ outputs from GIS workflow get referenced in
  Begründung's cartographic citations?
- File-map.md interpretation for GIS folders.

### Python-ACAD-Tools app integration

**Why**: User maintains a separate Python tools app at
`~/dev/Gunther-Schulz/Python-ACAD-Tools/` for AutoCAD-style drawing
manipulation. Used for technical Zeichnungen (Planzeichnungen, V&E-
Plan layouts, Bestandspläne). Like gis-utils, this is a sibling tool
that the pbs-bureau orchestrator should be aware of.

**Components**:
- Python-ACAD-Tools as a standalone tool (likely with its own MCP
  server or CLI; verify current state at session start)
- Per-project `Zeichnungen/` folder is the natural integration point
  (similar to GIS/Karten/ in joint-practice projects)
- pbs-bureau may produce textual references to Zeichnungen
  (Begründung Section 14: "Kataster- und Vermessungswesen") and
  needs to know where the CAD outputs live

**Open questions**:
- Does Python-ACAD-Tools have an MCP interface, or CLI-only?
- Per-project workflow shape (workflow.yaml-style like gis-utils, or
  ad-hoc scripts?)
- Symmetry with gis-utils: same coexistence pattern, or different?

### Overleaf sync workflow detail

**Why**: Decided that LaTeX subfolders are git-init'd per project for
Overleaf sync. The detailed mechanics (GitHub-remote-creation,
branch protection, push triggers, conflict resolution) need
spec'ing.

**Open questions**:
- Auto-create GitHub repos on scaffold-project? Or manual?
- Branch protection: should pbs-bureau push to `main` or to a `draft`
  branch?
- Conflict resolution when Overleaf and local both edit?

### Audit trail — unified change/decision/version tracking

**Why**: Currently audit-trail-like things are scattered across the
system without a coherent design:
- per-project `decisions.md` captures user-facing decisions
- per-project `snapshots/` captures frozen artifact versions
- references corpus `changelog.md` captures reference fetches
- git history captures code/skill changes
- references-manifest entries carry `last_fetched`, archived versions

There's no unified picture of "what happened to this piece, when,
why, by whom" across all the moving parts (project artifacts,
references, manifests, configs, integrations, bausteine, plans,
correspondence). When a UNB later asks "show me what changed
between Vorentwurf and Entwurf for §X", we should be able to
answer cleanly. When citation drift breaks a baustein months later,
we should be able to trace the chain.

**Sketch (topic-level only — design TBD)**:
- A unified event log with stable schema (timestamp, actor, kind,
  scope, target, before/after pointers, rationale).
- Per-domain handlers (project artifacts → snapshot manifest;
  references → changelog; bausteine → status flips; configs →
  schema migrations; etc.) emit into the same log.
- Query path: "what changed in scope X between dates A and B" or
  "what was the state of artifact Y at date Z".
- Privacy / retention boundaries: per-project audit lives with the
  project; cross-cutting (references, configs) at office level.

**Open questions** (deliberately unresolved):
- Single append-only event log file vs distributed per-domain logs
  with a query layer over them?
- Schema across domains: how rigid? per-kind subschemas?
- How does this interact with snapshots/, decisions.md, changelog.md
  — do those become projections of the unified log, or stay
  authoritative with the log as a thin index?
- External-actor attribution (UNB sends a Stellungnahme — that's
  also an event, but the actor is outside the system).

### Human-readable artifact generation at checkpoints

**Why**: Many workflow pieces are machine-readable (LaTeX source,
billing.md ledger, Stellungnahme YAML, baustein markdown) — but
humans review and discuss in their natural form (PDF, formatted
preview). Today only LaTeX has clean human-output via `compile_latex`.
Other kinds either have no checkpoint render or rely on ad-hoc
generation. We need a principle: at every meaningful checkpoint
(send-gate, phase transition, draft-invoice, baustein-promotion,
config-change), produce the human-readable artifact alongside the
machine state, so the human review step has something to look at.

**Examples**:
- LaTeX docs: PDF on every snapshot (already done)
- Invoices: PDF draft when `draft-invoice` runs (planned with PM item above)
- Stellungnahmen drafts: PDF for review before send-gate
- Cover mails: PDF/RTF for review before send
- Bausteine: when promoted to skill, show diff PDF or formatted view
- Config changes: human-readable summary of what changed (not raw YAML diff)
- Audit trail queries: rendered timeline view, not raw log
- Baustein freshness sweep: human-readable report PDF

**Sketch (topic-level)**:
- Convention: every checkpoint event has an associated render that
  produces a PDF (or HTML for interactive) at a predictable path.
- Backend tool family for renders (compile_latex already exists;
  add `render_invoice`, `render_stellungnahme`, `render_audit_timeline`,
  etc. as needed).
- Skills register their checkpoints + the render they produce.
- Renders are themselves versioned through the audit trail above —
  so we can show the user what the rendered checkpoint looked like
  at the time, not as it would render today.

**Open questions**:
- Render templates: per-office or universal? (Likely follows same
  3-layer LaTeX stack pattern: app shipping universal templates,
  office overlays for branding.)
- HTML vs PDF: when does interactive review (HTML) beat archival
  (PDF)? Probably both, with PDF as the canonical archival form.
- Storage: renders alongside source in snapshots/, or a separate
  renders/ tree?

### Integration registry — unified discovery of MCPs + adapters + skills

**Why**: PBS will accumulate many "things the orchestrator can call":
- Internal adapters (email, calendar, scanner, phone, accounting —
  Phase 5 scaffolded)
- External MCP servers (gis-utils, Python-ACAD-Tools, future
  review-platform MCP, future legal-search MCP, etc.)
- PBS-owned skills (16 currently — auto-discovered from
  plugin/skills/ but their utility/scope isn't queryable as data)

The orchestrator currently knows about these through tribal
knowledge (it knows `gis-utils` exists because the user has it
installed; it knows about `survey-project` because the SKILL.md
trigger fires). There's no unified registry where the orchestrator
can ask "what tools do I have for working with GIS data?" or "what's
available in the Wind domain that I could leverage?"

When a new MCP becomes useful (or new internal adapter, or new skill),
making it *known* to the orchestrator + queryable by capability is
itself a gap.

**Pull-forward triggers** (don't build until at least one fires):

- **Capability-vocabulary friction** — orchestrator string-
  matching tool descriptions becomes unwieldy; routing decisions
  are repeatedly wrong because the orchestrator can't query
  callables by capability.
- **Total callable count exceeds ~50** — current count is ~44
  (16 skills + 5 integration adapters + 22 MCP tools + 1 external
  MCP `gis-utils`). At this scale the orchestrator holds the
  inventory in context fine; at 50+ a registry pays off.
- **Second deployment** — PBS-only doesn't justify cross-office
  knowledge propagation; a second Planungsbüro adopting the app
  forces it (registry entries become reusable across offices).

Until at least one trigger fires, the Tier 1 `list_skills()` MCP
tool + frontmatter `mcp_tools_required[]` declarations + snake_case
tool naming convention (per ARCHITECTURE.md meta-rule 4) cover the
immediate need with forward-compatible string IDs.

**Sketch (topic-level)**:
- A 4th layered manifest type alongside references + doctypes:
  `integrations-manifest.yaml` per scope (universal / domain / state).
- Each entry catalogs ONE callable thing (MCP, internal adapter, or
  skill) with metadata:
  ```yaml
  - id: gis-utils
    kind: mcp                       # mcp | adapter | skill
    name: gis-utils
    description: GIS/CAD utility library — geometry conversion, recipes, templates
    scope_relevance: [PV-FFA, Wind, Naturschutz]   # which domains benefit
    state_relevance: []                              # any
    when_to_use: |
      Geometry conversion, lines→polygon, buffer/dissolve operations,
      checking recipe-layer compatibility, GIS-workflow authoring.
    capabilities: [geometry-conversion, workflow-authoring, recipe-discovery]
    docs_url: <plugin-docs>
    config_path: ~/.config/claude/mcp.json#gis-utils
    activation: explicit-skill-tool   # how the orchestrator invokes it
  ```
- Layered loader walks the union per office's scope (same pattern as
  references / doctypes). PBS sees universal + domain manifests for
  PV-FFA / Wind / Naturschutz + state for MV.
- A new PBS skill `register-integration` (or
  `integrate-tool`) walks the user through adding a new MCP /
  adapter / skill to the relevant scope manifest. Hands off to
  `author-manifest` if the target manifest doesn't exist yet.
- Orchestrator queries via new MCP backend tool
  `find_integrations(capability=?, scope=?)` — returns relevant
  entries, lets the AI surface "for this task, you have these
  options" to the user.

**Why a registry vs just letting the orchestrator discover by trial**:
- Discoverability: the AI knows what's available without trying
  random tool names.
- Cross-office reusability: once "review-platform / Hypothesis is a
  good fit for collaborative review" is captured, every office that
  selects that scope inherits the knowledge.
- Onboarding: a new deployment knows what's plug-and-play vs what
  needs configuration.

**Open questions**:
- Do MCP entries carry their own MCP server config (host, port,
  command), or just point at where it's configured externally
  (~/.claude/.mcp.json)?
- Skill entries — are they redundant with auto-discovery via
  SKILL.md frontmatter? Maybe yes for skills, registry is mostly
  for MCPs + adapters; skills get auto-registered.
- Capability vocabulary: free-text or controlled list? Free-text
  starts faster, controlled list helps queries.
- Integration with the "review-platform integration adapter class"
  proposed in the Web-UI item: that's a specific case of this more
  general pattern.

### Web UI for collaborative review (annotations + comments)

**Why**: Renders from the previous item produce review-ready PDFs,
but distribution + collaborative review still happens out-of-band
(email attachments, file shares). For colleagues, partners (Hendrik),
and clients to comment / annotate / discuss in-place — and for those
annotations to come back into the workflow — we need a web UI.
Self-hosted in Coolify (PBS's existing PaaS).

**Architectural trigger**: implementing this is the load-bearing
event for the `pbs_core` / `pbs_mcp` physical split (see
ARCHITECTURE.md → Backend organization). Until the web UI lands,
the conceptual split inside the monolithic MCP module is
sufficient; the web UI is the first concrete non-MCP consumer
that forces promoting `pbs_core` to its own package + wrapping it
as a persistent service.

**Sketch (topic-level)**:
- Web app receives uploads from the backend (PDFs + metadata
  context: project, doctype, version, what we want feedback on).
- Recipients get a share link (auth via password / signed link /
  account, TBD).
- Reviewers annotate (highlight, draw, comment per page/region),
  thread comments, mark sections as approved/rejected.
- Annotations + comments are queryable back via MCP (new tool
  `fetch_review_feedback(project, doctype, version)`) so they feed
  the orchestrator's record-feedback / Abwägung-drafting flows.
- Probably a "review-platform" integration adapter class (parallel
  to email/calendar/scanner/etc.) so the platform itself can be
  swapped per office preference.

**Research candidates** (open-source to evaluate before building):
- **Hypothesis** (web annotation, open source, well-established) —
  paragraph + range annotations on web pages / PDFs; has API for
  read-back. Mostly aimed at academic web annotation.
- **Cryptpad** (encrypted collaboration suite, French gov-funded) —
  has document review capabilities; self-hostable.
- **Nextcloud + Collabora Online** — generic collaborative office
  suite; Collabora supports PDF review; widely deployed.
- **Stirling-PDF** — open-source PDF tools; has annotation support;
  self-hostable.
- **HedgeDoc / Outline** — collaborative markdown; not PDF-focused
  but useful if review shifts upstream from PDF.
- **PDF.js + custom annotation backend** — Mozilla's PDF.js with
  annotation layer + a small server (FastAPI?) storing annotations.
  Custom-built; most flexible but most work.
- **Onlyoffice Document Server** — full collaborative office suite;
  PDF review; Coolify-friendly Docker deployment.
- **PaperHive / Annotator.js** — older annotation-focused projects;
  check current state.

Goal: prefer a deployable existing tool with a usable API over
custom build. Custom annotation server is last resort.

**Open questions**:
- Auth model for external reviewers (UNB officials, client
  contacts): passwords, signed links, federation?
- Annotation portability: if we leave the chosen tool later, can
  annotations export to a standard format (W3C Web Annotations)?
- Privacy: annotations on Begründung drafts contain pre-decisional
  content; storage location + retention need legal-review.
- Notification flow: how do reviewers learn there's something to
  review? Email integration (already on roadmap) is the natural
  hook — invite mail with review link.
- Round-trip: when reviewers comment, does the orchestrator surface
  it on next session-open, or wait for explicit `fetch-review-
  feedback` call?

### Anthropic-native-app / third-party GUI-frontend integrations

**Why**: As the AI-augmented workforce grows, users uncomfortable
with CLI need GUI on-ramps. Anthropic itself is building native
GUI apps with workspace features and integrations; similar
trajectories elsewhere (Cursor, Zed, etc.). PBS-style intertwined
workflow could be exposed through these GUIs as another frontend
over the same `pbs_core` engine — same intertwining model, more
accessible surface.

**The crucial guard (per VISION.md → category-collapse risk)**:
integrating with native GUIs is fine ONLY when the integration
exposes intertwined workflow. The risk is category collapse —
PBS reduced to a "summarize this email" plugin in someone else's
tool. That's tacked-on, not intertwined; it betrays the thesis.
Any integration must preserve continuous orchestration, persistent
state, source-grounding, and the human-authority gates. If the
host environment can't accommodate those, the integration should
be deferred or rejected outright.

**Sketch (topic-level, speculative)**:

- `pbs_core` exposed via HTTP / WebSocket / similar transport so
  GUI clients can call it (post-physical-split per ARCHITECTURE.md
  → Backend organization).
- Integration registry's `kind` field grows `frontend` or `client`
  alongside `mcp` / `adapter` / `skill`.
- Each GUI integration registered with metadata about which
  workflow surfaces it exposes (orchestrator chat? specific
  specialist skills? read-only state browser?) — surface mapping
  becomes auditable against the intertwining requirements.
- Authentication / multi-user concerns surface here (also tied
  to "Office as multi-human + AI" open question in VISION.md).

**Pull-forward triggers**:

- A specific GUI host emerges that can carry intertwined workflow
  faithfully (not just discrete features).
- A non-CLI colleague needs PBS-Office access and CLI is the
  bottleneck (Hendrik becomes a full participant, or PBS hires).
- SaaS pivot becomes concrete (possibility 3 in VISION.md).

Until then: defer. CLI (Claude Code) + planned web UI cover the
immediate frontend needs.

### Generalized knowledge ingestion via MCP connectors

**Why**: Today the architecture has two ingestion paths — legal
references via `research-references` (publishers' websites,
KNE/LUNG/BfN portals) and per-project inputs via
`ingest_project_inputs` (briefings, surveys, Stellungnahmen
dropped in `inputs/`). Companies have many more knowledge
sources: SharePoint, Confluence, Notion, internal wikis, custom
DMS, CRM systems, project management tools, billing systems,
internal email archives, recorded meeting notes. PBS doesn't
yet address how to bring these in. Generalizing the ingestion
layer is what makes intertwined workflow viable in real
companies — they have knowledge in many places.

**Sketch**: MCP connectors as the inbound knowledge layer
(parallel to integration adapters as the outbound layer; both are Backend sub-patterns).
Each company picks connectors that match their stack:

- SharePoint connector reads a configured folder; ingests at
  the appropriate scope per the layered manifest pattern.
- Notion connector exposes a configured workspace.
- Confluence connector reads a configured space.
- Custom DMS connectors via simple HTTP / file-system adapters.

The pattern mirrors `research-references`: each manifest entry
declares its `fetch_method` and source URL/connector.
Generalize the fetch_method enum to include MCP-connector kinds
(`mcp-sharepoint`, `mcp-notion`, `mcp-confluence`, etc.).
Ingested content lands in LanceDB at the appropriate scope,
searchable via `search_corpus` with source_type filtering.

**Pull-forward triggers**:

- First office that needs to ingest from an external source
  beyond legal references.
- First prospect (consulting / sales) with a structured DMS
  that PBS-style intertwined workflow needs to draw on.
- A non-legal corpus becomes valuable enough to PBS itself
  (e.g., archived correspondence + meeting notes corpus for
  cross-project pattern recognition).

**Open questions**:

- Schema: how do non-legal references differ from legal in
  manifest entry shape? Probably a unified schema with optional
  fields per source kind.
- Authentication: many corporate sources require OAuth /
  service accounts. Connector responsibility, but auth state
  needs persistence (office-config? per-connector credentials
  store?).
- Refresh policy: legal references refresh monthly-ish; live
  Notion / Confluence might want continuous sync. Per-connector
  configurable.
- New scope dimension? "Office-private" knowledge (this office's
  own SharePoint, internal docs) doesn't fit any of the
  shareable scopes (universal/domain/state). Either treat as
  per-deployment override of universal, or introduce a fifth
  scope kind. Resolve when first office-private connector lands.

### Cross-deployment community knowledge content

**Why**: The integration registry (above) covers cross-deployment
*callable* integrations — once "Hypothesis is good for collaborative
review" is captured, every office that adopts that scope inherits
the recommendation. But knowledge *content* (bausteine, refined
argumentations, captured patterns) currently has no cross-deployment
story. Each office is siloed. If PBS captures a valuable Naturschutz
baustein that proved itself in real Stellungnahme exchanges, no
mechanism exists for other Naturschutz-domain offices to benefit.

**Distinct from integration registry**: registry catalogs
*callables*; this catalogs *knowledge artifacts*. Both are
cross-office, both scope-aware, but they carry different things.

**Sketch (topic-level, speculative)**:

- A "community" layer above the (universal × domain × state)
  scopes — content that's been proven in one office and made
  available to others.
- Bausteine + memory docs explicitly marked as community-
  shareable; opt-in pull from receiving offices.
- Provenance preserved: who originated, who validated, with
  what feedback record.
- Curation question: who decides what's community-quality?
  Likely human curation by domain shepherds (one or more
  recognized practitioners per domain).

**Pull-forward triggers**:

- Second deployment exists (PBS-only doesn't justify;
  multi-office does).
- Concrete value example surfaces ("we wish we had Office X's
  Naturschutz bausteine").
- Curation infrastructure question becomes real (who validates,
  how distribution works).

**Open questions**:

- Distribution: git-mirror? Custom registry server? Bundled
  with releases?
- Trust model: how does Office Y verify Office X's baustein is
  worth adopting?
- Conflict resolution: community baustein vs. local baustein
  with same name?
- Privacy: bausteine may contain client-specific or politically
  sensitive context; sanitization required before community
  publishing.

### Cross-practice knowledge integration

**Why**: PBS-Office today supports multi-practice projects
(`practices: [<id>, ...]` in state.md, sibling-practice with
read-only crossing). The model assumes light coexistence: PBS
reads Hendrik's GIS exports as static inputs; doesn't write to
his workspace, doesn't query his database directly.

But intertwined workflow benefits from richer integration.
Hendrik's GIS findings (FFH-Gebiet boundaries, species
distribution plots, habitat photographs from Begehungen,
Bestandskarten) contain knowledge PBS could draw on directly
for artenschutzrechtliche reasoning. Today that knowledge is in
his GIS database; PBS sees it only via static exported PDFs/PNGs.

**Sketch (topic-level, speculative)**:

- Practice-aware MCP boundaries: each practice's tooling exposes
  its knowledge via MCP; cross-practice queries authorized per
  project (multi-practice flag) or per scope (cross-cutting).
- Or simpler: cross-practice knowledge surfaces as a special
  source kind in `search_corpus` (filter by practice).
- Authorship preservation matters here: if PBS draws on
  Hendrik's GIS finding, who is the author of the resulting
  Begründung paragraph? Joint authorship? Citation? Provenance
  recorded in audit trail.

**Pull-forward triggers**:

- First multi-practice project with significant cross-practice
  reasoning required (Begründung Section citing GIS-derived
  spatial analysis with traceable provenance).
- Hendrik's tooling becomes MCP-accessible (currently CLI /
  file-based).

**Open questions**:

- Trust + authorship: cross-practice knowledge enters PBS's
  output; whose responsibility is the integrated reasoning?
- Granularity: full GIS database access, or curated findings
  the GIS practice explicitly exposes?
- Conflict: when GIS finding contradicts text-practice
  assumption, who reconciles?

### Project management + invoicing

**Why**: Project work today has no time/billable tracking, no
milestone-to-invoice mapping, no status reporting to client. The
orchestrator knows phase transitions and decision logs but doesn't
connect them to billing. Adding PM concerns covers: time tracking
per project / per practice / per partner, milestone definitions
that trigger invoicing, status reports auto-generated from state.md
+ decisions.md, draft invoices from accumulated time.

**Sketch**:
- Per-project `_ai/billing.md` — ledger of billable units (hours,
  fixed-price milestones, expenses) with state-transition tagging.
- New PBS skill `log-time` — capture time entries from session
  context (e.g. "I worked 2h on Maxsolar Begründung Section 4
  today"), append to billing.md.
- New skill `draft-invoice` — composes invoice from a project's
  billing ledger, applies office-config invoice template, hands off
  to the accounting integration adapter for actual delivery.
- Accounting adapter implementations (DATEV-export, lexoffice,
  sevDesk) — protocol stub already in place from Phase 5
  (`backend/.../integrations/accounting/`).
- Integration with Begründung-deliverable-snapshot pairs: a
  send-gate firing on a Vorentwurf is also a billable milestone.

**Open questions**:
- Time entries: structured (hours / category / billable yes-no) or
  free-text with extraction?
- Multi-practice billing: when Hendrik (partner) co-produces, does
  PBS bill the client and split, or does each party bill independently?
- Privacy: billing data is sensitive. Per-project storage in
  `<project>/_ai/billing.md` keeps it co-located with project
  context but means it ships wherever the project ships. Office-
  state-only ledger (`<state_root>/billing/<project>.md`) is more
  isolated.

---

## v2 — extensions

### Reference versioning

**Why**: Laws amend. Currently `archive_versions: true` in manifest
keeps `retention_versions: 5` per entry. But: how does
verify-citations know which version a baustein was verified against?
History tracking spec needed.

### Reference internal cross-refs

**Why**: BauGB §44 mentions §1, etc. When retrieval pulls §44 chunk,
should §1 be auto-fetched as context? Reranker may handle this; test
with real queries first.

### Subagent patterns

**Why**: Currently no subagents. For deep legal review, a
`legal-reviewer` subagent (separate Claude instance with focused
context) could do thorough §-by-§ checks without bloating the main
session.

**Components**:
- `plugin/agents/legal-reviewer.md` — agent definition
- Invoked by review-draft skill at Layer 2 (fachlich) for
  juristisch-critical sections
- Returns findings; main Claude integrates

Similar pattern for `style-auditor` (deep style+korrektur sweep).

### Hooks / event triggers (revised per meta-rule 4)

**Why (revised)**: Per meta-rule 4 (execution-determinism), most
operations formerly imagined as hooks belong inside MCP tools as
atomic side-effects, not as separate hook scripts:

- `state-transition` → logged inside the `update_project_state`
  MCP tool, not a hook on Edit.
- `snapshot-on-send` → atomic write inside the snapshot-creation
  MCP tool, not a hook on Bash send-mail.
- `pre-compile validate-latex-style` → step inside `compile_latex`
  MCP tool's pipeline, not a PreToolUse hook.
- `post-ingest baustein-flag` → atomic in the `ingest_paths` MCP
  tool's transaction (already planned per `research-references`
  SKILL.md cross-reference handling).

The genuinely hook-shaped niche that survives is **out-of-band
file change detection between sessions** — when state changes
outside Claude Code's view (user manually edits a manifest YAML
in a text editor; hidrive sync brings in changes from a sibling
practice; an external script touches `office-config.yaml`). A
SessionStart hook could detect mtime deltas against a
last-session marker and trigger validation / cross-ref re-eval
before the orchestrator does its first action.

**Defer**: until concrete out-of-band-change friction is observed
in real use. Pre-designing for hypothetical out-of-band edits
adds enforcement scaffolding nobody asked for.

---

## v2.x — additional verfahren references

These are domain knowledge documents to author when first project
raises them.

### Umweltprüfung verfahren reference

**Why**: §2 Abs.4 BauGB + Anlage 1 environmental assessment
integration with the 13-phase Bauleitplanung. Currently mentioned
but not detailed in `memory/universal/verfahren/bauleitplanung-phasen.md`.

**Spec**: full reference doc at
`memory/universal/verfahren/umweltpruefung.md`. Covers Scoping (§4
Abs.1), Umweltbericht structure cross-ref to umweltbericht checklist,
Wechselwirkungen, Monitoring (§4c) integration.

### FFH-Vorprüfung verfahren reference

**Why**: §34 BNatSchG Erheblichkeitsabschätzung is required for
projects near FFH-Gebiete. Was rhetorically handled in the Vorbeck
transcript; deserves its own reference doc for projects where
formal Vorprüfung is required.

**Spec**: full reference doc at
`memory/universal/verfahren/ffh-vorpruefung.md`. Covers
Erheblichkeitsabschätzung, Kumulative Betrachtung,
Verschlechterungsverbot, Ausnahme nach §34 Abs.3-5.

### Abwägung mechanism + doctype

**Why**: Per-Stellungnahme structured response document. Distinct
shape from Begründung/Festsetzungen. Not yet in doctypes.yaml as
active.

**Components**:
- New doctype entry in `doctypes.yaml`
- Checklist at `plugin/skills/validate-checklist/references/checklists/
  abwaegung.md`
- Possibly `draft-abwaegung` specialist skill (Phase A entry for
  Abwägung doctype)

### Artenschutz / SPA verfahren reference

**Why**: §44 BNatSchG-Tatbestände + §45 Abs.7 Ausnahme; SPA-Vorprüfung
+ SPA-Hauptprüfung structure. Hendrik's domain primarily but joint
projects need it.

**Spec**: `memory/universal/verfahren/artenschutz.md`. Covers
Bestandsaufnahme-Standards (Südbeck, Dietz/Kiefer), Signifikanz-
prüfung, CEF-Wirksamkeit-Nachweis, FCS-Auslegung. Note: with the
domain split, this content is Naturschutz-domain-scoped — should
land at `memory/domain/Naturschutz/verfahren/artenschutz.md` once
domain-scoped memory directories exist (currently universal-only).
The decision to introduce per-domain memory directories awaits the
first domain-specific reference content (this would be the trigger).

### Other verfahren / doctypes as projects raise them

- Bauantrag / V&E-Plan-spezifisches
- Zielabweichungsverfahren
- Innenbereichssatzung-Aufstellung (different from B-Plan)

---

## Working-style improvements (lessons collected)

These aren't features but discipline improvements observed during
v1 design. Apply by next session and onward.

### ARCHITECTURE.md as first reference, kept fresh

When in doubt about where new content belongs, walk Rules 1-6 in
`ARCHITECTURE.md`. Don't guess; classify deliberately. For layered
manifest entries pick the scope (universal/domain/state) BEFORE the
path.

**Keep ARCHITECTURE.md current with every architectural change.**
Meta-rule changes, new entity types, schema bumps, integration
classes — all land in ARCHITECTURE.md *in the same commit* that
introduces them. ROADMAP-tracked items get a one-line pointer in
the "Designed extensions" section so future sessions don't
re-discover them. After any meta-rule addition or significant
refactor, sweep all skills against current meta-rules to catch
drift.

### Source-grounding for legal claims

`verify-citations` skill's invariant: any `§ X <Gesetz>` reference
must come from a `search_corpus` or `read_corpus_file` result, not
from training memory. Never invent citations.

### Section-level edits, not whole-document writes

Per orchestrator Validation 7.3: `Edit` tool with surrounding context,
not `Write` of the entire file. Especially during Phase B review.

### Decision recording preserves alternatives

When recording an architectural / design / verdict decision in
docs (ARCHITECTURE.md, ROADMAP.md, VISION.md, decision docs like
`docs/rag-pipeline-decisions.md`, project `_ai/decisions.md`,
etc.), always preserve the alternatives that were considered and
rejected — not just the chosen path. Capture per item:

- **The verdict** (chosen path)
- **Alternatives considered** (named explicitly with their
  reasoning + why-rejected)
- **Revisit trigger** (when would we revisit this decision? what
  signal would force re-evaluation?)

Why: decisions made today look obviously correct in their context
but reveal as defensible-or-not when the context shifts. A
verdict-only record reads as "this is how it is" — making the
revisit conversation harder than necessary because the original
alternatives have to be re-derived. A verdict + alternatives +
trigger record reads as "here was the option space and our
choice within it" — making revisit a refinement rather than a
re-investigation.

Applies to: architectural decisions, model/library choices,
schema choices, naming conventions, scope boundaries, deferred-
vs-urgent prioritization, anything where the next session might
reasonably ask "why this and not the other thing?"

### "Used by skill X" cross-refs are noise

In memory content (C type), don't include "loaded by skill Y at
checkpoint Z" lines. They don't change behavior. Skill files
themselves declare what they consume.

---

## Tracking conventions

When picking up an item from this roadmap:

1. Move it from "deferred" to "in-progress" by editing this file.
2. Once complete, remove from this file (it's now in the codebase
   per ARCHITECTURE.md placement rules).
3. Don't leave completed items here — that's clutter.

When a new deferred item emerges:

1. Add to the appropriate v-tier section.
2. Include "Why" + "Sketch" + "Open questions" subsections.
3. Don't elaborate beyond that — full design happens when picked up.
