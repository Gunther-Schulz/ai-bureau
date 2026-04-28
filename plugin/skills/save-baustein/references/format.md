# Baustein format

A baustein is a single markdown file with YAML frontmatter (machine-
readable metadata) and a body (human-readable content). One file per
baustein.

## File location and naming

Path determined by scope:

| Scope | Location |
|---|---|
| `global` | `<repo>/memory/global/<name>.md` |
| `domain` | `<repo>/memory/<domain>/<name>.md` (e.g. `memory/domain/artenschutz/§45-nr5-innenbereich-privat.md`) |
| `project` | `<project-root>/_ai/bausteine/<name>.md` |

Filename rules:
- ASCII-safe slug (kebab-case where possible).
- German legal symbols (`§`) acceptable; spaces are not.
- No `.tex` or other source extensions; bausteine are markdown.
- Stem unique within scope.

## Frontmatter schema

```yaml
---
# Identity
name: §45-nr5-innenbereich-privat        # matches filename stem
scope: domain                             # global | domain | project
domain: artenschutz                       # required if scope=domain
project: 23-12-Vorbeck                    # required if scope=project
type: argumentation                        # argumentation | technical-spec | citation | checklist | textbaustein | template

title: §45 Abs.7 Nr.5 BNatSchG — Innenbereichsentwicklung als Ausnahmegrund
language: de                               # de | en | mixed

# Provenance
source_project: 23-12-Vorbeck             # null for global bausteine
source_date: 2026-04-22
captured_via: orchestrator-menu            # orchestrator-menu | manual | promote-from-skill | seed | research-references
captured_session: 2026-04-22-vorbeck

# Lifecycle
status: active                             # active | flagged | archived | superseded
last_validated: 2026-04-22
review_due: 2027-04-22                     # default +1y
flagged_reason: null
superseded_by: null

# Use tracking
use_count: 0
last_used: null
successful_uses:
  - {project: 22-16-Friedrichshof, date: 2025-09-12, feedback_path: memory/domain/artenschutz/feedback/2025-09-12-UNB-rostock-§45-nr5.md}
rejected_uses: []

# Dependencies — surgical hook for research-references
references:
  - {law: BNatSchG, paragraph: §45 Abs.7 Nr.5, cited_form: "zwingende Gründe des überwiegenden öffentlichen Interesses"}
  - {law: BauGB, paragraph: §1a Abs.2}
  - {ruling: BVerwG-9-A-22-11}
  - {leitfaden: LUNG-MV-Artenschutzleitfaden, version: 2024-08}

tags: [solar, photovoltaik, innenbereich, privat]
---
```

Field semantics:

- `status` transitions: `active` → `flagged` (citation drift, rejection feedback, source project regressed) → `active` (after re-validation) OR → `superseded`/`archived`.
- `flagged_reason` must be set when status=flagged. Short sentence with link to trigger (feedback file path or research-references diff log).
- `superseded_by` points at the name of the replacement, not a path.
- `references` entries: `law` for federal/state laws, `ruling` for court decisions, `leitfaden` for guidance docs, `methodology` for standards (Südbeck etc.), `convention` for office practice.

## Body structure

```markdown
# Title

## When to use

Concrete trigger: when does this baustein apply? Be specific.

## Content

The reusable text/argument/spec ready to drop into a draft with light
project-specific substitution.

## Notes / caveats

Limitations, known weaknesses, when NOT to use, alternative approaches.

## History

Append-only narrative log. Each entry: date — event description.

- 2026-04-22 — Captured from Vorbeck §45 argumentation.
- 2026-09-12 — Reused in Friedrichshof; UNB approved.
```

`When to use` and `Content` are mandatory. `Notes` and `History` recommended.

## Example: argumentation baustein

```markdown
---
name: §45-nr5-innenbereich-privat
scope: domain
domain: artenschutz
type: argumentation
title: §45 Abs.7 Nr.5 BNatSchG — Innenbereichsentwicklung als Ausnahmegrund
language: de
source_project: 23-12-Vorbeck
source_date: 2026-04-22
captured_via: orchestrator-menu
status: active
last_validated: 2026-04-22
review_due: 2027-04-22
use_count: 1
last_used: 2025-09-12
successful_uses:
  - {project: 22-16-Friedrichshof, date: 2025-09-12, feedback_path: memory/domain/artenschutz/feedback/2025-09-12-UNB-rostock-§45-nr5.md}
rejected_uses: []
references:
  - {law: BNatSchG, paragraph: §45 Abs.7 Nr.5}
  - {law: BauGB, paragraph: §1a Abs.2}
  - {ruling: BVerwG-9-A-22-11}
tags: [solar, photovoltaik, innenbereich, privat]
---

# §45 Abs.7 Nr.5 BNatSchG — Innenbereichsentwicklung als Ausnahmegrund

## When to use

Privates Bauvorhaben im Innenbereich (§34 BauGB) wo eine
artenschutzrechtliche Ausnahme nach §45 Abs.7 BNatSchG erforderlich
wird und nur Nr.5 als Ausnahmegrund einschlägig sein kann.

Voraussetzungen:
- Innenbereichssatzung oder gleichwertige planungsrechtliche
  Verankerung der Wohnbebauung in der Gemeinde existiert.
- Vorhabenträger ist Privat.

## Content

Als einschlägiger Ausnahmegrund kommt Nr.5 (zwingende Gründe des
überwiegenden öffentlichen Interesses, einschließlich solcher
sozialer oder wirtschaftlicher Art) in Betracht. Das öffentliche
Interesse wird hier getragen durch:

- den planerischen Willen der Gemeinde zur Innenbereichsentwicklung,
  dokumentiert in der einschlägigen Innenbereichssatzung,
- den bundespolitisch verankerten Vorrang der Innenentwicklung vor
  Außenbereichsentwicklung (§1a Abs.2 BauGB),
- die Stärkung gewachsener ländlicher Ortslagen durch Ersatz
  baufälliger Substanz und Schaffung von zeitgemäßem Wohnraum,
- flankierend soziale/wirtschaftliche Gründe auf Seiten des Bauherrn
  (Eigenbedarf).

## Notes / caveats

- Reine Nr.5-Argumentation hat hohe Begründungstiefe-Schwelle (BVerwG
  9 A 22.11). Stand-alone selten tragfähig; immer mit §1a Abs.2-
  Verankerung kombinieren.
- Nicht für rein gewerbliche Vorhaben ohne Wohnnutzungsbezug.

## History

- 2026-04-22 — Captured from Vorbeck §45 argumentation. Approved by
  UNB Rostock (Hr. Ratschker).
- 2025-09-12 — Reused in Friedrichshof. UNB Rostock approved with
  minor §1a-Bezug-Anpassung.
```

## Lifecycle: when fields update

| Trigger | Field updates |
|---|---|
| Create new | All identity, provenance, lifecycle initialized; references[] populated by capture conversation |
| Retrieved | use_count++; last_used=today |
| Approval feedback | successful_uses.append(); last_validated=feedback.date |
| Rejection feedback | rejected_uses.append(); status=flagged; flagged_reason="rejection by <authority> <date>" |
| Law change in references[] | status=flagged; flagged_reason describes the change |
| review_due passed | Surfaced for review; no auto-update |
| Authorize archive | status=archived; superseded_by set if replacement exists |

Archived bausteine remain readable but excluded from default list queries.
