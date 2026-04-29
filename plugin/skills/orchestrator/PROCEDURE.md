# Bureau orchestrator procedure

Mandatory checkpoints that interrupt default behavior. Continuous
flow throughout every session. Self-imposed — the user does not need
to invoke any of this; recognition and surfacing is the
orchestrator's job.

## Three-phase workflow model

Document workflow runs in three phases. Each phase has a canonical
entry skill (see `phase_role` in skill frontmatter):

- **Phase A — Drafting**: produce the document from project sources.
  Entry skills: `draft-textteil-b` (Begründung), `draft-textteil-c`
  (Festsetzungen). Future doctypes (Umweltbericht, Gutachten) gain
  their own Phase A entry when they land.
- **Phase B — Review**: layered review of the produced draft.
  Entry skill: `review-draft` (delegates to `validate-checklist`
  Layer 1, `verify-citations` Layer 2, `validate-latex-style`
  Layer 3).
- **Phase C — Finalize / Send**: send-gate, snapshot, lifecycle
  transition. Owned by orchestrator (Checkpoint 4.3, 4.4) +
  `draft-cover-mail` for transmittal.

Per-project `_ai/state.md.lifecycle` tracks where the project is
in this model: `draft` (Phase A) → `internal-review` (Phase B) →
`sent-to-authority` / `finalized` (Phase C).

Specialists self-identify their phase via `phase_role:` in
frontmatter (`phase_a_entry`, `phase_b_entry`, `layer_1` /
`layer_2` / `layer_3`). The orchestrator's routing tables can be
machine-derived from `list_skills()` responses.

---

## 1. Session open — before responding to first domain-context message

FIRST, when any planning-bureau-context trigger fires, identify the
operating scope from observable signals:

- **Office scope:** no project named, no project root path mentioned.
  Default for queries like "what's on my plate", "any UNB responses",
  "which projects are open".
- **Project scope:** a project name, project root path, or
  configured-naming-pattern identifier appears in the user message
  OR was bound in a prior turn of this session.
- **Product scope:** the user references the assistant itself —
  skills, MCP tools, the framework, the backlog, "fix this skill".

THEN load context for the detected scope:

| Scope | Read at open |
|---|---|
| Office | `<state_root>/projects-index.md`, `<state_root>/pending-actions.md` (path via `office_config.roots.state`); call `list_projects()` and `list_skills()` MCP tools |
| Project | Call `get_project_state(project)` (returns validated state + body — never Read state.md directly per ARCHITECTURE meta-rule 4); `<project-root>/_ai/file-map.md`, `<project-root>/_ai/decisions.md`. For doctype context: call `list_doctypes_manifests()` (no longer at `<repo>/memory/universal/doctypes.yaml` — registries are Configuration entity in `extensions/`). |
| Product | `<repo>/memory/product-backlog.md`, `<repo>/ROADMAP.md`, `<repo>/VISION.md`, `<repo>/ARCHITECTURE.md` |

Load `<repo>/memory/universal/style/style-spec.md` and `<repo>/memory/universal/conventions/korrektur-rules.md` whenever LaTeX work is in scope. Note: `memory/global/` no longer exists — content moved to `memory/universal/` (cross-cutting knowledge) and `memory/bausteine/` (instance records) per the orthogonality refactor.

THEN announce loaded context in one terse line: "Mode: project (\<name\>). Loaded: state, file-map, \<doctype\> domain, style-spec." or equivalent. Do not narrate at length.

If a referenced project has no `_ai/` or `.ai/` folder, treat the next user request as a binding event and run **Checkpoint 11 (project binding)** before proceeding.

---

## 2. Continuous watch list — runs throughout work

Six triggers (T1 reusable-pattern / T2 citation-drift / T3 promotion / T4 style-deviation / T5 standing-rule / T6 capability-gap) fire whenever they match in conversation or in produced output.

**Detection happens here in orchestrator** as part of normal workflow parsing. **Queue management, dedup, decay, surfacing, and four-way decision dispatch live in the `watch-list` skill** (extracted in v0.5 per design-review S3 — see `plugin/skills/watch-list/PROCEDURE.md` for the full data model + decay rules + per-trigger TTL/caps).

When the orchestrator detects a candidate, hand off to `watch-list`. T6 is special-cased — auto-backlog with no menu (see `watch-list/PROCEDURE.md` §6).

The watch list does not block. It surfaces decisions; the user decides. Per-session caps + per-trigger TTL prevent spam-the-user mode.

For the trigger taxonomy + detection criteria + per-trigger side-effects, see `plugin/skills/watch-list/references/triggers.md`.

---

## 3. The four-way decision menu (delegated to watch-list)

The decision menu protocol (`Noticed: <thing>. → capture-now / handle-now / backlog / drop?`) and reply parsing live in `plugin/skills/watch-list/PROCEDURE.md` §5. Orchestrator delegates surfacing + dispatch to the watch-list skill.

Dispatched actions hand off to specialist skills:
- **capture-now** → `save-baustein` (T1, T5) or `promote-to-skill` (T3)
- **handle-now** → `verify-citations` (T2), `validate-latex-style` (T4)
- **backlog** → append to `<repo>/memory/product-backlog.md`
- **drop** → no-op acknowledgment

Never silent capture. Every memory-write or backlog-append corresponds to an explicit four-way decision the user authorized (T6 exempted — internal observation, auto-backlogged).

---

## 4. Hard gates — blocking checkpoints

These cannot be bypassed. Each is enumerated with required evidence
the orchestrator must produce before proceeding.

### 4.1 Compile gate

Before claiming any draft is ready, complete, or sendable:

- [ ] Compile succeeded?
  - NO → CANNOT claim ready. Run `compile_latex` (or `latexmk -pdf` in the project dir if MCP not available). Surface the build log error to the user.
  - YES → Evidence: PDF path + zero LaTeX errors in log + page count from `pdfinfo`.

A "draft ready" claim without a compile-success evidence triple is a protocol violation. Treat warnings (overfull boxes, unresolved references, missing citations) as findings to surface — not as gate failures, but visible alongside the success.

### 4.2 Layered review gate

When the user requests review (explicit "review", "prüfe", "schau drüber") or when the orchestrator runs a pre-send review, run three layers strictly in order:

1. **Structural** — required sections present per doctype? Section order matches `style-spec.md`? Required Verfahrensvermerke / Quellenverzeichnis / Unterschriftenblock present?
2. **Fachlich** — content correctness: legal citations cite real provisions, claims have source grounding (Checkpoint 5), arguments are internally consistent.
3. **Formal** — LaTeX style spec compliance, `korrektur-rules.md` compliance (German quotes, non-breaking spaces, number formatting), no compile warnings.

Between layers, pause for user confirmation: "Strukturell sauber. Weiter mit Fachlich, oder zuerst die Strukturpunkte adressieren?" Each layer's findings are surfaced before the next layer starts. Do not bundle all findings across layers.

CANNOT skip a layer. Skipping is a protocol violation. The user can decline to fix findings from a layer, but each layer must run.

### 4.3 Send gate

Before drafting a transmittal mail, copying artifacts to a deliverables location, or marking a project state as `sent-to-authority`:

- [ ] Compile gate passed for the artifact in question?
  - Required.
- [ ] Final artifact set staged?
  - Required. List the exact files: PDF, source .tex, cover mail, recipient.
- [ ] Snapshot folder created?
  - Required. Path: `<project-root>/_ai/snapshots/<YYYY-MM-DD>-<recipient-tag>/`. Copy artifacts in.
- [ ] User confirmed?
  - Required. Output: "Senden an: \<recipient\>. Anhang: \<file list\>. Mail-Vorschau: \<inline preview or path\>. Bestätigen?" Wait for explicit confirmation.

Only then call `update_project_state(project, updates={"lifecycle": "sent-to-authority"}, body_append="- <date> — Sent to <recipient>.")`. Never write state.md directly.

### 4.4 State transition gate

Project state transitions require explicit acknowledgment, not implicit inference from activity. Lifecycle:

```
draft → internal-review → sent-to-authority → awaiting-response →
revision-requested → finalized → archived
```

To advance a state:
- Output current state and proposed next state.
- Wait for user confirmation.
- Call `update_project_state(project, updates={"lifecycle": "<new>"}, body_append="- <YYYY-MM-DD> — <triggering action>.")`. The MCP gate validates the merged state before writing; never edit state.md directly.

Never advance state silently. Particularly: never mark `finalized` until the user explicitly confirms the project is closed (the bausteine-promotion guard depends on this — see Checkpoint 6.4).

---

## 5. Source-grounding guard — invariant

BEFORE outputting any legal citation in a draft, review finding, or argument:

- A `§ X <Gesetz>` reference, an `Art. Y` reference, a court ruling (e.g. BVerwG 9 A 14.07), or a paragraph from a Verordnung MUST be backed by a tool result.

Evidence requirement, before each citation:
- A `search_corpus(...)` or `read_corpus_file(...)` call from this session that returned text containing the exact citation. State which call.

If no tool result backs the citation:
1. Run `search_corpus` over `source_type=reference` with the citation as query.
2. If found → use the citation.
3. If not found → output: "Keine Quelle in references gefunden. WebFetch von gesetze-im-internet.de oder ähnlich, oder Hinweis ohne Zitat?" — do not invent the citation.

Training memory is not a source. The model's recall of "BNatSchG zuletzt geändert durch Artikel 1 vom 08.12.2022" is not evidence; the citation must come from a tool result, period. This guard exists because legal citations rot — laws are amended and the model's recall lags.

---

## 6. Hard guards — invariants beyond source-grounding

Each of these cannot be violated. State the violation if it would occur and ask the user to authorize an exception, rather than silently bypassing.

### 6.1 German artifacts

Project deliverables (.tex, .pdf, mails, captions, file names inside the project) are written in German. The conversation between user and orchestrator may be German, English, or mixed. When producing artifact content, German is required regardless of the conversation language.

### 6.2 Memory write scopes (post-orthogonality)

`save-baustein` writes to one of four scopes per ARCHITECTURE.md scope orthogonality (universal × domain × state) plus per-project: `universal`, `domain`, `state`, `project`. Each requires `scope_key` (except universal). Routing rules:

| Content kind | Scope | scope_key |
|---|---|---|
| Cross-bureau pattern (signature conventions, language rules, universal frameworks like BauGB process) | `universal` | none |
| Reusable in a planning domain (e.g. PV-FFA, Wind, Naturschutz argumentation patterns) | `domain` | domain key (`Naturschutz`, `PV-FFA`, etc.) |
| State-specific knowledge (LUNG-MV interpretation, OVG-MV ruling application, MV Landesgesetze) | `state` | state code (`MV`, etc.) |
| Single-project fact (specific UNB contact, project-specific decision) | `project` | project name OR project_root |

Writes to `universal` scope require explicit user confirmation. Domain/state/project scopes follow standard four-way menu authorization. The orchestrator proposes the scope+scope_key as part of the menu line.

**Path resolution** (handled by `save_baustein` MCP tool per meta-rule 4):

- `universal` → `<repo>/memory/bausteine/universal/<name>.md`
- `domain` → `<repo>/memory/bausteine/domain/<scope_key>/<name>.md`
- `state` → `<repo>/memory/bausteine/state/<scope_key>/<name>.md`
- `project` → `<project_root>/_ai/bausteine/<name>.md`

Project-scope bausteine may set `cross_project_visible: true` to surface in `list_bausteine` queries from other projects in the same office without yet promoting to broader scope (resolves promote-or-keep-locked binary). See save-baustein/references/format.md for the field semantics.

### 6.3 Module-decision logging

When `draft-textteil-b`, `draft-textteil-c`, or any other doctype-drafting work decides which optional modules to include or exclude (e.g. for an Umweltbericht: include `Schutzgut_TierePflanzen_UB.tex` because survey shows Funde; exclude `MethodikGutachten_UB.tex` because no field methodology applies), append a row to `<project-root>/_ai/module-decisions.md`. Format:

```
- 2026-04-28 — included Schutzgut_TierePflanzen_UB.tex — reason: 
  Funde from Vermessung 2026-03 (Stellungnahme attached)
- 2026-04-28 — excluded MethodikGutachten_UB.tex — reason: 
  no separate field methodology section per client decision
```

Module decisions made conversationally without logging are a protocol violation — six months later when the UNB asks why a section is missing, the audit trail must exist.

### 6.4 Baustein promotion guard

A baustein in `<project_root>/_ai/bausteine/...` (project scope) may only be promoted to broader scope (`universal`, `domain`, or `state` under `<repo>/memory/bausteine/<layer>/<key>/`) after the source project's lifecycle is `finalized` — read via `get_project_state(source_project).state.lifecycle`, never via direct state.md Read. Reasoning: until a project is signed off, the argumentation may still change, and propagating an unvalidated pattern across the bureau (or worse, across deployments via universal/domain) is wrong.

Promotion before finalization → BLOCK. Output: "Quellprojekt ist noch \<state\>. Promotion erst nach finalized erlaubt." If the user insists, require an explicit "ich autorisiere die frühe Promotion" — log the override in `<repo>/memory/product-backlog.md` for later audit.

Note: setting `cross_project_visible: true` on a project-scope baustein is NOT promotion — it just extends search visibility within the same office. No guard required for that flag. See save-baustein/references/format.md.

---

## 7. Validation — automated, non-blocking

Run on every compile (Checkpoint 4.1) and surface as findings alongside the build success. Do not block the build for validation findings unless the build itself failed.

### 7.1 Citation freshness

For each legal citation in the document, compare against the reference index. If the cited form ("zuletzt geändert durch Artikel X vom DD.MM.YYYY") differs from the current reference text, surface: "Citation drift in §X BNatSchG: doc says \<A\>, references say \<B\>. update?" Send to four-way menu.

### 7.2 Style-spec diff

Compare the document's preamble + structure against `style-spec.md`. Surface deviations as findings: "Deviation: doc uses `\\usepackage[ngerman]{babel}` — spec matches. Deviation: doc uses `geometry` with custom margins — spec says left=25mm, doc has left=20mm." Each deviation is a finding for the four-way menu.

### 7.3 Section-level edits

When applying review findings or any multi-section change, prefer `Edit` over `Write` for source files. Produce an explicit diff summary after a review pass: "Changed: §3 Ergebnisse, §5.1 Ausnahmegrund-Formulierung, Quellenverzeichnis. Unchanged: everything else."

A whole-document `Write` for a multi-section change is a protocol violation. Section-level edits are observable: the orchestrator must enumerate the sections changed.

### 7.4 Required sections

Per doctype, the layered `doctypes.yaml` manifests (call `list_doctypes_manifests()` — Tier 1 MCP tool) list `sections_canonical`. Compare the document's section list against the canonical superset. Surface missing-required as findings; surface extras as informational (project-specific extensions are allowed, but flagged).

---

## 8. Project lifecycle and ownership modes

### 8.1 Lifecycle states

```
draft               — work in progress, no external review yet
internal-review     — internal pass before sending
sent-to-authority   — transmitted to UNB / Behörde / client
awaiting-response   — sent, no reply yet
revision-requested  — reply received with changes requested
finalized           — signed off, no further changes expected
archived            — formally closed, read-only
```

State lives in `<project-root>/_ai/state.md`. Transitions follow Checkpoint 4.4.

### 8.2 Ownership modes (existing projects only)

When binding to an existing project for the first time (Checkpoint 11), detect state and propose a mode. Record via `update_project_state(project, updates={"ownership_mode": "<mode>"})` (or via the `bind_project` MCP tool on initial creation). Modes:

| Mode | What the orchestrator may write | What it must not touch |
|---|---|---|
| **migrate** | Canonical doctype folders (Textteil B/, Textteil C/, Umweltbericht/), `_ai/` | Pre-existing .doc/.docx files (legacy); user-organized resource folders |
| **new-work-only** (default) | New files in canonical folders, `_ai/` | All existing files anywhere |
| **quarantine** | `_ai/` only | Everything else |

Proposing the mode is part of binding — see Checkpoint 11. Default is `new-work-only` because it has the smallest blast radius. The user explicitly upgrades to `migrate` per project.

### 8.3 New projects

For new projects (Checkpoint 12), the AI owns the entire project root. No quarantine. State lives in `<project-root>/.ai/` (hidden, since the whole folder is AI-managed and meta-state should not visually clutter).

### 8.4 Multi-practice projects

`_ai/state.md` carries `practices: [<id>, ...]` where the ids come
from `office_config.actors` (filtered to kind=internal). When more than one practice id appears
in the array, the project is multi-practice (e.g. text-document
practice + GIS practice working on the same job).

- Each practice's working files are preserved as-is. The orchestrator
  does not touch files outside its declared practice's role unless
  the user explicitly authorizes a cross-practice edit.
- The orchestrator's `_ai/` lives alongside the other practice's
  workspace. Neither touches the other.
- When another practice publishes outputs (e.g. GIS exports to
  `<project-root>/Ausgabe/`), those become inputs the orchestrator
  may read but not modify.
- Bausteine in `memory/universal/` apply to the orchestrator's
  practice's work only. Other practices may have their own per-project
  CLAUDE.md or assistant configurations; not consulted here.

---

## 9. MCP tool surface (delegated to specialist skills' frontmatter)

Every specialist skill declares its own MCP-tool dependencies +
fallback behavior in its `SKILL.md` frontmatter (per meta-rule 4 +
`docs/plugin-conventions.md` §1). The orchestrator reads these via
`list_skills()` MCP tool; tables enumerating per-tool fallbacks
have been removed from this PROCEDURE (single source of truth =
specialist's own frontmatter).

To inspect available tools + their fallback semantics: call
`list_skills()` (returns each skill's `mcp_tools_required[]`,
`mcp_tools_optional[]`, and `fallback_when_mcp_absent`). This
replaces the v0.4 inline tool-tables.

When the orchestrator itself needs an MCP tool not yet listed in
its frontmatter, fall back as appropriate and log a T6 capability-
gap trigger via the watch-list skill.

---

## 10. Specialist routing

The orchestrator does not draft, review, or finalize directly. Each operation routes to a specialist skill. When a routing target is missing, perform the work inline AND log a T6 (capability gap) trigger to `<repo>/memory/product-backlog.md`.

For canonical, queryable inventory call `list_skills()` (MCP tool) — returns every skill's name, description, version, and `mcp_tools_required[]`. Table below is at-glance reference; MCP tool is authoritative.

| Operation | Specialist | Trigger phrases |
|---|---|---|
| First-time office setup | `setup-office` | "deploy", "set up office", "first run", absent office-config |
| Draft Begründung from sources | `draft-textteil-b` | "Entwurf Textteil B", "Begründung schreiben", "draft Begründung for ..." |
| Draft Festsetzungen | `draft-textteil-c` | "Entwurf Festsetzungen", "Textteil C schreiben", "Satzungstext" |
| Layered review | `review-draft` | "review", "prüfe", "schau drüber", "korrigieren" |
| Capture baustein | `save-baustein` | (always: triggered by capture-now decision) |
| Baustein freshness sweep | `validate-bausteine` | "freshness check", "stale bausteine", session-open auto |
| Record external feedback | `record-feedback` | UNB Stellungnahme arrives, "Behörden-Reaktion", "approval kam von..." |
| Promote baustein → skill | `promote-to-skill` | (always: triggered by T3 → handle-now; guard 6.4) |
| Style validation | `validate-latex-style` | "style check", "spec-Abweichung", part of formal review |
| Doctype checklist | `validate-checklist` | part of structural review |
| Citation verification | `verify-citations` | "Zitate prüfen", part of formal review, T2 surfacing |
| Cover mail draft | `draft-cover-mail` | "Mail an UNB", "Anschreiben aufsetzen", part of send gate |
| First-bind project survey | `survey-project` | (always: triggered when binding to existing project) |
| Refresh references corpus | `research-references` | "update references", "neue Fassung", "refresh corpus" |
| Author new manifest | `author-manifest` | "new domain", "scaffold <Domain>", "add manifest for <STATE>" |

When performing inline what would be a specialist's job, hold the same checkpoints active: source-grounding, style-spec compliance, korrektur-rules, layered review structure.

---

## 11. Project binding — delegated to survey-project skill

When a user references a project that has no `_ai/` or `.ai/`
folder, run the **`survey-project`** skill before any other
operation. That skill owns binding logic (file clustering, ownership
mode proposal, state.md scaffolding) — see
`plugin/skills/survey-project/SKILL.md`.

Orchestrator's role here: detect the unbound condition (project
referenced but no `_ai/` or `.ai/` exists), invoke survey-project,
optionally append the resulting binding to `<roots.state>/projects-index.md`
afterwards.

Binding is a one-time per project event. Subsequent invocations
load the existing artifacts and re-survey only if file-map mtimes
are stale.

---

## 12. New-project creation — delegated to setup_project MCP tool

When the user requests a new project ("neues Projekt", "new
project", "scaffold ..."):

1. **Solicit core metadata**: project number (auto-suggested from
   `office_config.conventions.project_numbering`), client, location,
   doctype focus, practice (defaults to
   `office_config.default_internal_actor()`).
2. **Call `setup_project` MCP tool** with the gathered metadata.
   The tool's contract owns: path resolution (`office_config.roots.projects`),
   three-mode detection (absent → create+scaffold; empty → scaffold-in-place;
   populated → route to survey+bind), `.ai/` vs `_ai/` selection per
   ownership mode, scaffolding of canonical layout +
   per-doctype skeletons + `Projektdaten.tex` instantiation,
   `projects-index.md` append.
3. **Output a one-paragraph orientation** with name + folder layout
   + doctypes scaffolded + suggested next step.

For new projects, never propose an ownership mode — full AI
ownership is the only mode.

(Detail of `setup_project`'s three-mode behavior + scaffolding
contract lives in the tool's Pydantic schema +
`backend/.../tools/projects.py`. Per meta-rule 4, the tool is the
single source of truth for the lifecycle work; orchestrator
collects metadata + dispatches.)

---

## 13. Conversational style

(Cross-skill conventions live in `docs/plugin-conventions.md` §12.
This section retained as a thin pointer + orchestrator-specific
emphasis.)

Match the user's language per turn (mixed is fine). Be terse;
surface findings inline as one-liners (Checkpoint 3 menu format).
When uncertain about a decision the user must make, state the
orchestrator's recommendation alongside the question — do not
present open-ended choices.

For details (no-emoji, no bureaucratic-acknowledgments,
language-matching, body-language conventions), see
`docs/plugin-conventions.md` §12.

---

## 14. Session close

When the user signals end-of-session ("danke das wars", "stop for now", "we're done", or natural pause after artifact delivery):

Output a recap, four lines maximum:

1. **Project changes:** what artifacts moved or were modified.
2. **Memory changes:** what bausteine were captured / promoted.
3. **Backlog:** what was added to product-backlog.
4. **Next:** suggested resumption point.

Do not narrate. Do not editorialize. End with the orchestrator's recommendation for what to do next session, in one phrase.
