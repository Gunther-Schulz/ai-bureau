# pbs-bureau roadmap

Deferred feature backlog. Each item is "designed enough to know it
matters but not yet specified in detail." Pick up in priority order
when the system is ready or when a real project needs the feature.

For session-state (what's done vs in-progress), see `HANDOFF.md`.
For taxonomy + decision rules, see `ARCHITECTURE.md`.

---

## v1.x — likely soon

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

---

## v1.x-v2 — when first project needs it

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

### Web UI for collaborative review (annotations + comments)

**Why**: Renders from the previous item produce review-ready PDFs,
but distribution + collaborative review still happens out-of-band
(email attachments, file shares). For colleagues, partners (Hendrik),
and clients to comment / annotate / discuss in-place — and for those
annotations to come back into the workflow — we need a web UI.
Self-hosted in Coolify (PBS's existing PaaS).

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

### Hooks / event triggers

**Why**: Currently no hooks. Possible future events:
- `state-transition` — log to `decisions.md` automatically
- `snapshot-on-send` — auto-create snapshot when send-gate fires
- `pre-compile` — auto-run validate-latex-style as gate
- `post-ingest` — auto-flag affected bausteine after research-references

Defer until specific friction emerges.

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

### ARCHITECTURE.md as first reference

When in doubt about where new content belongs, walk Rules 1-6 in
`ARCHITECTURE.md` (after the v0.2 nine-entity-types refactor). Don't
guess; classify deliberately. For layered manifest entries pick the
scope (universal/domain/state) BEFORE the path.

### Source-grounding for legal claims

`verify-citations` skill's invariant: any `§ X <Gesetz>` reference
must come from a `search_corpus` or `read_corpus_file` result, not
from training memory. Never invent citations.

### Section-level edits, not whole-document writes

Per orchestrator Validation 7.3: `Edit` tool with surrounding context,
not `Write` of the entire file. Especially during Phase B review.

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
