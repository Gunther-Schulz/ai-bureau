# Feedback format

Feedback entries record externally-authored reactions (rejection,
approval, partial, suggestion) to PBS work. One entry per
authority + project + topic. YAML frontmatter holds machine-readable
metadata; body holds the full text or excerpt.

## File location

```
memory/domain/<domain>/feedback/<YYYY-MM-DD>-<authority-slug>-<topic-slug>.md
```

Examples:
- `memory/domain/artenschutz/feedback/2026-04-28-UNB-rostock-§45-nr5.md`
- `memory/domain/b-plan/feedback/2025-12-10-LUNG-mv-CEF-monitoring.md`

Filename rules:
- Date prefix `YYYY-MM-DD` for chronological sort.
- Slugs kebab-case ASCII-safe.
- `§` symbol acceptable in topic slug.

Per-domain `feedback/INDEX.md` is a rolling table summary, regenerated
on each feedback save.

## Frontmatter schema

```yaml
---
# Identity
date: 2026-04-28
authority: UNB Landkreis Rostock
authority_slug: UNB-rostock
contact: Hr. Ratschker
project: 23-12-Vorbeck

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
source_artifact: <project>/_ai/snapshots/2026-04-15-UNB-rostock/Stellungnahme.pdf
source_excerpt_pages: [3, 4]

# Lifecycle
status: open                               # open | resolved | wont-act
resolved_by: null
resolved_date: null
---
```

Field semantics:

- `addresses_bausteine` is the surgical hook. On rejection: each
  listed baustein gets `status=flagged`, `flagged_reason=<this entry>`.
  On approval: each gets `successful_uses.append()`.
- `addresses_arguments` captures arguments by description even when no
  baustein currently exists. Future captures may match against this.
- `source_artifact` must point at an immutable copy (snapshot) — not
  a live working file.
- `status` lifecycle: `open` (just received) → `resolved` (baustein
  updated, replacement saved, or argument retired) OR → `wont-act`
  (acknowledged but no change planned).

## Body structure

```markdown
# Title (date — authority — topic)

## Context

Brief: which project, which phase, what was sent that prompted this
feedback.

## Feedback excerpt

Full text or extended excerpt of the relevant section. Quoted verbatim
where possible.

## Analysis

Why this feedback matters: which assumption it contradicts, which
arguments need rework, what it implies for similar future projects.

## Action taken

What was done in response. Updated when status moves to resolved.
Append-only.
```

`Context` and `Feedback excerpt` required. `Analysis` required for
type=rejection or type=partial. `Action taken` empty initially.

## Example: rejection entry

```markdown
---
date: 2026-04-28
authority: UNB Landkreis Rostock
authority_slug: UNB-rostock
contact: Hr. Ratschker
project: 23-12-Vorbeck
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

# 2026-04-28 — UNB Landkreis Rostock — §45 Nr.5 Innenbereich

## Context

Stellungnahme der UNB im förmlichen Verfahren §4 Abs.2 zu B-Plan
Vorbeck. Begründung Abschnitt 5 hat reine Innenbereichssatzungs-
Argumentation für §45 Abs.7 Nr.5 BNatSchG vorgetragen.

## Feedback excerpt

> "Die alleinige Bezugnahme auf die Innenbereichssatzung der Gemeinde
> reicht nicht aus, um zwingende Gründe des überwiegenden
> öffentlichen Interesses i.S.d. §45 Abs.7 Satz 1 Nr.5 BNatSchG zu
> begründen. Vgl. BVerwG, Urteil vom 23.08.2012 — 9 A 22.11."

## Analysis

Bestätigt die im Baustein notierte caveat. Innenbereichssatzung
allein ist unzureichend. §1a Abs.2 BauGB-Bezug + soziale Gründe
müssen kombiniert werden.

Future projects: never use Innenbereichssatzung-Argumentation alone
für Nr.5; immer kombinieren.

## Action taken

[empty until resolved]
```

## Example: approval entry

```markdown
---
date: 2025-09-12
authority: UNB Landkreis Rostock
authority_slug: UNB-rostock
project: 22-16-Friedrichshof
type: approval
phase: 10-genehmigung
addresses_bausteine:
  - §45-nr5-innenbereich-privat
status: resolved
---

# 2025-09-12 — UNB Rostock — §45 Nr.5 angenommen (Friedrichshof)

## Context

Genehmigung höhere Verwaltungsbehörde nach Auflagen.

## Feedback excerpt

> "Die Ausnahme nach §45 Abs.7 Satz 1 Nr.5 BNatSchG kann unter den
> in der Begründung dargestellten Voraussetzungen erteilt werden."

## Analysis

§45 Nr.5 + §1a Abs.2-Kombination wurde übernommen und akzeptiert.
```

## Lifecycle effects

```
Save new feedback entry
  ├─ if type=rejection or partial:
  │    addresses_bausteine[] → each gets status=flagged
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

## INDEX.md (per domain)

```markdown
# Feedback INDEX — <domain>

| Date | Authority | Type | Project | Topic | Status | Path |
|---|---|---|---|---|---|---|
| 2026-04-28 | UNB-rostock | rejection | 23-12-Vorbeck | §45-nr5-innenbereich | open | feedback/2026-04-28-UNB-rostock-§45-nr5.md |
| 2025-09-12 | UNB-rostock | approval | 22-16-Friedrichshof | §45-nr5-innenbereich | resolved | feedback/2025-09-12-UNB-rostock-§45-nr5.md |
```

Sorted newest-first. Auto-maintained on every feedback save.
