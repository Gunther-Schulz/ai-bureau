# Feedback format

Feedback entries record externally-authored reactions (rejection,
approval, partial, suggestion) to office work. One entry per
authority + project + topic. YAML frontmatter holds machine-
readable metadata; body holds the full text or excerpt. Layered
along the same scope orthogonality as bausteine.

## File location (post-orthogonality)

Feedback entries live alongside the bausteine they address, under
the layered baustein tree:

```
memory/bausteine/<layer>/<scope_key>/feedback/<YYYY-MM-DD>-<authority-slug>-<topic-slug>.md
```

Examples:

- `memory/bausteine/domain/Naturschutz/feedback/2026-04-15-UNB-rostock-§45-nr5.md`
- `memory/bausteine/state/MV/feedback/2026-04-15-LUNG-MV-bestandserfassung.md`
- `memory/bausteine/universal/feedback/2026-04-15-XYZ-allgemein.md` (rare; only when
  feedback is genuinely cross-domain/state)
- `<project_root>/_ai/bausteine/feedback/2026-04-15-UNB-rostock-§45-nr5.md`
  (project-scope feedback)

The scope/scope_key on a feedback entry inherits from the
addressed baustein(s). Single-scope per entry; if a feedback
addresses bausteine in different scopes, split into multiple
feedback entries (one per scope), cross-referenced.

Filename rules:

- Date prefix `YYYY-MM-DD` for chronological sort.
- Slugs kebab-case ASCII-safe.
- `§` symbol acceptable in topic slug.

Per-scope feedback `INDEX.md` is a rolling table summary,
regenerated on each feedback save:

- `memory/bausteine/<layer>/<scope_key>/feedback/INDEX.md`

## Frontmatter schema

```yaml
---
# Identity
date: YYYY-MM-DD
authority: UNB Landkreis <Landkreis>
authority_slug: UNB-<landkreis-slug>
contact: <Sachbearbeiter>
project: <YY-NN>-<location-slug>

# Scope (inherited from addressed baustein; see format note above)
scope: domain                              # universal | domain | state | project
scope_key: Naturschutz                     # required for domain/state; project name for project

# Type
type: rejection                            # rejection | approval | partial | suggestion
phase: 5b-foerml-toeb                      # bauleitplanung-phase

# What it addresses
addresses_bausteine:
  - §45-nr5-innenbereich-privat
addresses_arguments:
  - "Innenbereichssatzung als zwingender Grund Nr.5"
addresses_artifacts:
  - <project>/B-Plan/Begründung/B-Plan Begründung.tex

# Substance
verdict_reasoning: |
  Innenbereichssatzung allein reicht nicht; Verweis auf BVerwG 9 A 22.11.
suggested_alternative: |
  Kombinierte Argumentation §1a Abs.2 BauGB + soziale Gründe.

# Source
source_artifact: <project>/_ai/snapshots/2026-04-15-UNB-<landkreis-slug>/Stellungnahme.pdf
source_excerpt_pages: [3, 4]

# Lifecycle
status: open                               # open | resolved | wont-act
resolved_by: null
resolved_date: null
---
```

Field semantics:

- `scope` + `scope_key` — inherited from addressed baustein(s).
  Mirror the layered baustein layout so feedback co-locates with
  the affected bausteine.
- `addresses_bausteine` is the surgical hook. On rejection: each
  listed baustein gets `status=flagged`, `flagged_reason=<this
  entry path>`. On approval: each gets `successful_uses.append()`.
- `addresses_arguments` captures arguments by description even
  when no baustein currently exists. Future captures may match
  against this.
- `source_artifact` must point at an immutable copy (snapshot) —
  not a live working file.
- `status` lifecycle: `open` (just received) → `resolved`
  (baustein updated, replacement saved, or argument retired) OR →
  `wont-act` (acknowledged but no change planned).

## Body structure

```markdown
# Title (date — authority — topic)

## Context

Brief: which project, which phase, what was sent that prompted
this feedback.

## Feedback excerpt

Full text or extended excerpt of the relevant section. Quoted
verbatim where possible.

## Per-concern analysis

Per `record-feedback` priority refactor: when the Stellungnahme
raises multiple concerns, document each separately. For each:

### Concern N: <topic>

- **Argument addressed**: which baustein / which argument
- **Baseline reference fetched**: §X <Gesetz>, current form
  matches / drifted
- **Interpreting ruling fetched**: <docket>, relevance
- **Similar past Abwägung found**: <path>, outcome
- **Verdict implication**: what this means for the addressed
  argument
- **Affected dependent bausteine**: list from
  find_bausteine_by_reference

## Analysis (overall)

Why this feedback matters: which assumption it contradicts, which
arguments need rework, what it implies for similar future
projects.

## Action taken

What was done in response. Updated when status moves to resolved.
Append-only.
```

`Context` and `Feedback excerpt` required. `Per-concern analysis`
required for type=rejection or type=partial with multiple
concerns. `Analysis (overall)` required for type=rejection or
type=partial. `Action taken` empty initially.

## Example: domain-scope rejection entry

```markdown
---
date: 2026-04-15
authority: UNB Landkreis Rostock
authority_slug: UNB-rostock
contact: <Sachbearbeiter>
project: <YY-NN>-<location-slug>
scope: domain
scope_key: Naturschutz
type: rejection
phase: 5b-foerml-toeb
addresses_bausteine:
  - §45-nr5-innenbereich-privat
addresses_arguments:
  - "Innenbereichssatzung als zwingender Grund Nr.5"
addresses_artifacts:
  - <project>/B-Plan/Begründung/B-Plan Begründung.tex
verdict_reasoning: |
  Innenbereichssatzung allein reicht nicht; Verweis auf BVerwG 9 A 22.11.
suggested_alternative: |
  Kombinierte Argumentation §1a Abs.2 BauGB + soziale Gründe.
source_artifact: <project>/_ai/snapshots/2026-04-15-UNB-rostock/Stellungnahme.pdf
source_excerpt_pages: [3, 4]
status: open
---

# 2026-04-15 — UNB Landkreis Rostock — §45 Nr.5 Innenbereich

## Context

Stellungnahme der UNB im förmlichen Verfahren §4 Abs.2 zu B-Plan
\<project\>. Begründung Abschnitt 5 hat reine Innenbereichs-
satzungs-Argumentation für §45 Abs.7 Nr.5 BNatSchG vorgetragen.

## Feedback excerpt

> <verbatim Stellungnahme excerpt — paste from source artifact;
> stay verbatim, do not paraphrase. Cites BVerwG ruling, §45 Abs.7
> Satz 1 Nr.5 BNatSchG.>

## Per-concern analysis

### Concern 1: Reine Innenbereichssatzungs-Argumentation für Nr.5

- **Argument addressed**: §45-nr5-innenbereich-privat baustein
- **Baseline reference fetched**: §45 Abs.7 Nr.5 BNatSchG, i.d.F.
  23.10.2024 — text matches cited form ✓
- **Interpreting ruling fetched**: BVerwG-9-A-22-11 — confirms
  reine Innenbereichssatzung-Argumentation ist tragfähigkeits-
  schwach
- **Similar past Abwägung found**: project YY-NN-other-location
  used kombinierte §1a + soziale-Gründe-Argumentation, accepted
- **Verdict**: baustein needs caveat tightened or split into
  pure-vs-combined variants
- **Affected dependent bausteine**: none additional via
  find_bausteine_by_reference (this is the canonical baustein for
  Nr.5)

## Analysis

Bestätigt die im Baustein notierte caveat. Innenbereichssatzung
allein ist unzureichend. §1a Abs.2 BauGB-Bezug + soziale Gründe
müssen kombiniert werden.

Future projects: never use Innenbereichssatzung-Argumentation
allein für Nr.5; immer kombinieren.

## Action taken

[empty until resolved]
```

## Example: state-scope approval entry

```markdown
---
date: 2026-04-15
authority: UNB Landkreis Rostock
authority_slug: UNB-rostock
project: <YY-NN>-<other-project>
scope: state
scope_key: MV
type: approval
phase: 10-genehmigung
addresses_bausteine:
  - lung-mv-helgolaender-anwendung
status: resolved
---

# 2026-04-15 — UNB Landkreis Rostock — LUNG-MV Helgoländer-Anwendung angenommen

## Context

Genehmigung höhere Verwaltungsbehörde nach Auflagen.

## Feedback excerpt

> <verbatim approval text from source artifact>

## Analysis

LUNG-MV-Helgoländer-Anwendung wurde übernommen und akzeptiert.
```

## Lifecycle effects

```
Save new feedback entry
  ├─ if type=rejection or partial:
  │    addresses_bausteine[] → each gets status=flagged
  │    via flag_baustein() MCP tool
  │
  ├─ if type=approval:
  │    addresses_bausteine[] → each gets successful_uses.append(),
  │                             last_validated=feedback.date
  │
  └─ if type=suggestion:
       no auto-flag; advisory finding next session

User authors response → mark feedback resolved:
  status: resolved
  resolved_by: <baustein path or new baustein name>
  resolved_date: today
  Append "Action taken" body section.
```

## INDEX.md (per scope/scope_key)

```markdown
# Feedback INDEX — <layer>/<scope_key>

| Date | Authority | Type | Project | Topic | Status | Path |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | UNB-<landkreis-slug> | rejection | <YY-NN>-<location-slug> | §45-nr5-innenbereich | open | feedback/YYYY-MM-DD-UNB-<landkreis-slug>-§45-nr5.md |
| YYYY-MM-DD | UNB-<landkreis-slug> | approval | <YY-NN>-<other-project> | §45-nr5-innenbereich | resolved | feedback/YYYY-MM-DD-UNB-<landkreis-slug>-§45-nr5.md |
```

Sorted newest-first. Auto-maintained on every feedback save.
