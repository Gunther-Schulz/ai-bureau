# pbs-bureau roadmap

Deferred feature backlog. Each item is "designed enough to know it
matters but not yet specified in detail." Pick up in priority order
when the system is ready or when a real project needs the feature.

For session-state (what's done vs in-progress), see `HANDOFF.md`.
For taxonomy + decision rules, see `ARCHITECTURE.md`.

---

## v1.x — likely soon

### Modular integrations declared at office setup

**Why**: external systems (mail, calendar, scanner OCR, phone-system
call logs, accounting, GIS data feeds) vary per deployment. Some
offices use Thunderbird, others Outlook or web-IMAP-only; some
self-host email, some use Microsoft 365. Hard-coding any one
mechanism would break portability — the same architectural lesson
as paths/identity/practices.

**Sketch**: each integration class becomes a pluggable adapter:

```yaml
# in office-config.yaml
integrations:
  email:
    adapter: thunderbird-maildir       # | imap | outlook-pst | mbox-file | none
    config: { profile_path: ~/.thunderbird/<p>/Mail/ }
  calendar:
    adapter: caldav                     # | exchange-ews | ical-file | none
    config: { url: ..., credentials_ref: ... }
  scanner:
    adapter: hot-folder                 # | escli | tesseract | none
    config: { hot_folder: ~/Documents/Scans/ }
```

`setup-office` skill: at first-bootstrap, walks the user through
which integrations they want enabled and which adapter to pick per
class, writes config, validates each adapter loads. Adapters
themselves live as Python modules under
`backend/mcp-server/src/pbs_mcp/integrations/<class>/<adapter>.py`
implementing a small protocol (probe/list/fetch/normalize). MCP tools
expose the unified interface (`fetch_emails(project, since=...)`)
regardless of adapter.

**Note**: not implementing in v1. The architectural rule is clear —
no hardcoded mechanism. Initial v1 implementations may inline a
single adapter (e.g. Thunderbird maildir for email) but the adapter
boundary is in place from day one.

### Email integration (Thunderbird mbox reader)

**Why**: v1 has manual `.eml` drop into `<project>/Schriftverkehr/eml/`.
For complete project context, the assistant needs full inbox access
because the manually-saved `.eml` files are a curated subset.

**Sketch**: First adapter for the email-integration class above.
Small Python service that polls Thunderbird's local maildir/mbox at
`~/.thunderbird/<profile>/Mail/`, filters by domain whitelist +
project-keyword matching, drops matched messages into the right
project's `correspondence/eml/`. Could be an MCP tool or a
standalone daemon. Behind the integration adapter interface so an
office on IMAP can swap implementations without touching skills.

### Phone call note format

**Why**: `Schriftverkehr/telefonnotizen/` is a planned folder but no
spec exists for what a call note file should contain.

**Sketch**: small markdown spec — frontmatter (date, party,
contact, project, type=call, duration), body sections (Kontext,
Zusammenfassung, Entscheidungen, Folgeaktionen). Could be authored
into `<repo>/memory/domain/` as a reference content file.

### Office identity config

**Why**: `memory/global/identity.md` referenced by draft-cover-mail
and other skills. Holds PBS-specific signature, address, language
convention, default Quellen.

**Sketch**: single file with PBS-specific data. Format is reference
content (no frontmatter, just markdown). Drafted from existing PBS
templates.

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
but not detailed in `memory/domain/verfahren/bauleitplanung-phasen.md`.

**Spec**: full reference doc at
`memory/domain/verfahren/umweltpruefung.md`. Covers Scoping (§4
Abs.1), Umweltbericht structure cross-ref to umweltbericht checklist,
Wechselwirkungen, Monitoring (§4c) integration.

### FFH-Vorprüfung verfahren reference

**Why**: §34 BNatSchG Erheblichkeitsabschätzung is required for
projects near FFH-Gebiete. Was rhetorically handled in the Vorbeck
transcript; deserves its own reference doc for projects where
formal Vorprüfung is required.

**Spec**: full reference doc at
`memory/domain/verfahren/ffh-vorpruefung.md`. Covers
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

**Spec**: `memory/domain/verfahren/artenschutz.md`. Covers
Bestandsaufnahme-Standards (Südbeck, Dietz/Kiefer), Signifikanz-
prüfung, CEF-Wirksamkeit-Nachweis, FCS-Auslegung.

### Other verfahren / doctypes as projects raise them

- Bauantrag / V&E-Plan-spezifisches
- Zielabweichungsverfahren
- Innenbereichssatzung-Aufstellung (different from B-Plan)

---

## Working-style improvements (lessons collected)

These aren't features but discipline improvements observed during
v1 design. Apply by next session and onward.

### ARCHITECTURE.md as first reference

When in doubt about where new content belongs, walk Rules 1-5 in
`ARCHITECTURE.md`. Don't guess; classify deliberately.

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
