# Baustein format

A baustein is a single markdown file with YAML frontmatter (machine-
readable metadata) and a body (human-readable content). One file per
baustein. Layered along the `(universal × domain × state)` orthogonal
scopes per ARCHITECTURE.md, plus per-project scope.

## File location and naming

Path determined by scope (post-orthogonality refactor; new layout
under `memory/bausteine/`):

| Scope | Location |
|---|---|
| `universal` | `<repo>/memory/bausteine/universal/<name>.md` |
| `domain` | `<repo>/memory/bausteine/domain/<scope_key>/<name>.md` (e.g. `memory/bausteine/domain/Naturschutz/§45-nr5-innenbereich-privat.md`) |
| `state` | `<repo>/memory/bausteine/state/<scope_key>/<name>.md` (e.g. `memory/bausteine/state/MV/lung-mv-helgolaender-anwendung.md`) |
| `project` | `<project_root>/_ai/bausteine/<name>.md` |

Filename rules:

- ASCII-safe slug (kebab-case where possible).
- German legal symbols (`§`) acceptable; spaces are not.
- No `.tex` or other source extensions; bausteine are markdown.
- Stem unique within scope.

`scope_key` values match the directory names under
`extensions/{domain,state}/`:

- Domain: `Naturschutz`, `PV-FFA`, `Wind`, `Innenentwicklung`
- State: `MV`, `BB`, `BW`, `BE`, `HB`, `HH`, `HE`, `NI`, `NW`, `RP`,
  `SH`, `SL`, `SN`, `ST`, `TH` (ISO Bundesland codes)

## Frontmatter schema

```yaml
---
# Identity
name: §45-nr5-innenbereich-privat        # matches filename stem
scope: domain                             # universal | domain | state | project
scope_key: Naturschutz                    # required for domain/state; project name for project scope
type: argumentation                       # argumentation | technical-spec | citation | checklist | textbaustein | template

title: §45 Abs.7 Nr.5 BNatSchG — Innenbereichsentwicklung als Ausnahmegrund
language: de                              # de | en | mixed

# Provenance
source_project: <YY-NN>-<location-slug>   # null for universal bausteine
source_date: YYYY-MM-DD
captured_via: save-baustein-tool          # save-baustein-tool | promote-from-skill | seed | research-references | manual
captured_session: YYYY-MM-DD-<project>

# Lifecycle
status: active                            # active | flagged | archived | superseded
last_validated: YYYY-MM-DD
review_due: YYYY-MM-DD                    # default +1y
flagged_reason: null
superseded_by: null

# Use tracking
use_count: 0
last_used: null
successful_uses:
  - {project: <YY-NN>-<other-project>, date: YYYY-MM-DD, feedback_path: memory/bausteine/domain/Naturschutz/feedback/YYYY-MM-DD-UNB-rostock-§45-nr5.md}
rejected_uses: []

# Cross-project visibility (project scope only) — optional
cross_project_visible: false              # if true: surfaces in list_bausteine queries from OTHER projects in same office, even though scope=project. Resolves promote-or-keep-locked binary for mid-stage cross-project bausteine.

# Dependencies — surgical hook for research-references + verify-citations
references:
  - {law: BNatSchG, paragraph: §45 Abs.7 Nr.5, cited_form: "zwingende Gründe des überwiegenden öffentlichen Interesses", verified_against_version: "i.d.F. 23.10.2024"}
  - {law: BauGB, paragraph: §1a Abs.2, verified_against_version: null}
  - {ruling: BVerwG-9-A-22-11, verified_against_version: "as decided 2013-04-14"}
  - {leitfaden: LUNG-MV-Artenschutzleitfaden, version: 2024-08, verified_against_version: 2024-08}

tags: [solar, photovoltaik, innenbereich, privat]
---
```

Field semantics:

- `scope` + `scope_key` together resolve the canonical path. Per
  ARCHITECTURE.md scope orthogonality, a baustein has exactly one
  scope. If a candidate baustein applies to multiple, either
  promote it up the layer (`universal` if truly cross-domain) or
  split it.
- `status` transitions: `active` → `flagged` (citation drift,
  rejection feedback, source project regressed) → `active` (after
  re-validation) OR → `superseded`/`archived`.
- `flagged_reason` must be set when `status=flagged`. Short
  sentence with link to trigger (feedback file path or
  research-references diff log).
- `superseded_by` points at the name of the replacement, not a path.
- `cross_project_visible` (project scope only) — when `true`, the
  baustein appears in `list_bausteine` queries from other projects
  in the same office. Does NOT promote the baustein to broader
  scope; it just extends search visibility for cross-project
  reuse before the baustein is generalizable enough to promote
  via `promote-to-skill`. Resolves the otherwise-binary choice
  between project-locked and bureau-shareable.
- `references` entries:
  - `law` for federal/state laws (use ISO-style abbreviation:
    `BNatSchG`, `BauGB`, `BImSchG`, `LNatSchG-MV`, etc.)
  - `ruling` for court decisions (`BVerwG-<sigle>`, `EuGH-C-...`,
    `OVG-MV-<sigle>`)
  - `leitfaden` for guidance docs (`KNE-Anlagengestaltung`,
    `LUNG-MV-Artenschutzleitfaden`, etc.)
  - `methodology` for standards (Südbeck, Dietz/Kiefer, etc.)
  - `convention` for office practice
  - `verified_against_version` (recommended) — the amendment-form
    or version the baustein was last validated against. Allows
    `verify-citations` to detect drift when the law amends without
    re-validation. Set to `null` if not verified; that's a flag
    to verify-citations to surface for review.

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

- YYYY-MM-DD — Captured from <project> §45 argumentation.
- YYYY-MM-DD — Reused in <other-project>; UNB approved.
```

`When to use` and `Content` are mandatory. `Notes` and `History` recommended.

## Example: domain-scope argumentation baustein

```markdown
---
name: §45-nr5-innenbereich-privat
scope: domain
scope_key: Naturschutz
type: argumentation
title: §45 Abs.7 Nr.5 BNatSchG — Innenbereichsentwicklung als Ausnahmegrund
language: de
source_project: <YY-NN>-<location-slug>
source_date: YYYY-MM-DD
captured_via: save-baustein-tool
status: active
last_validated: YYYY-MM-DD
review_due: YYYY-MM-DD
use_count: 1
last_used: YYYY-MM-DD
successful_uses:
  - {project: <YY-NN>-<other-project>, date: YYYY-MM-DD, feedback_path: memory/bausteine/domain/Naturschutz/feedback/YYYY-MM-DD-UNB-rostock-§45-nr5.md}
rejected_uses: []
references:
  - {law: BNatSchG, paragraph: §45 Abs.7 Nr.5, verified_against_version: "i.d.F. 23.10.2024"}
  - {law: BauGB, paragraph: §1a Abs.2, verified_against_version: null}
  - {ruling: BVerwG-9-A-22-11, verified_against_version: "as decided 2013-04-14"}
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

- YYYY-MM-DD — Captured from <project> §45 argumentation. Approved by
  UNB <Landkreis> (<Sachbearbeiter>).
- YYYY-MM-DD — Reused in <other-project>. UNB <Landkreis> approved with
  minor §1a-Bezug-Anpassung.
```

## Example: project-scope baustein with cross_project_visible

```markdown
---
name: <project>-vorhabenträger-mit-eigenbeteiligung-argumentation
scope: project
scope_key: <YY-NN>-<location-slug>
type: argumentation
title: Vorhabenträger mit Eigenbeteiligung — Begründung der Tragfähigkeit
cross_project_visible: true            # surface for similar projects
references:
  - {law: BauGB, paragraph: §12, verified_against_version: "i.d.F. 23.10.2024"}
tags: [vorhabenbezogener-bplan, eigenbeteiligung, finanzierung]
---

# Vorhabenträger mit Eigenbeteiligung — Begründung der Tragfähigkeit

## When to use

Wenn der Vorhabenträger im vorhabenbezogenen B-Plan (§12 BauGB) eine
substantielle Eigenbeteiligung leistet und die Tragfähigkeit gegen
Zweifel der UNB / höhere Verwaltungsbehörde verteidigt werden muss.

## Content

[project-specific argumentation that may apply to similar future
project structures; user marked cross_project_visible to expose it
to other vorhabenbezogen projects without yet promoting to domain]
```

The `cross_project_visible: true` flag means: another project's
session calling `list_bausteine(scope=project, scope_key=<other>)`
gets this baustein surfaced as well, with a note that it's
cross-project-visible from `<source>`. Promotion to broader scope
remains a separate decision (orchestrator guard 6.4: source project
must be `finalized` before promoting).

## Lifecycle: when fields update

| Trigger | Field updates |
|---|---|
| Create new | All identity, provenance, lifecycle initialized; `references[]` populated by capture conversation |
| Retrieved (`get_baustein`) | `use_count++`; `last_used = today` (handled by MCP tool) |
| Approval feedback (`record-feedback`) | `successful_uses.append()`; `last_validated = feedback.date` |
| Rejection feedback | `rejected_uses.append()`; `status = flagged`; `flagged_reason = "rejection by <authority> <date>"` |
| Law change in `references[]` (research-references diff) | `status = flagged`; `flagged_reason` describes the change; `verified_against_version` retains old value until re-validation |
| `verify-citations` re-validates | `verified_against_version` updated to current; `last_validated = today` |
| `review_due` passed | Surfaced for review; no auto-update |
| Authorize archive | `status = archived`; `superseded_by` set if replacement exists |
| Promote to skill (`promote-to-skill`) | `superseded_by = <skill-name>`; `status = archived` after orchestrator guard 6.4 check |

Archived bausteine remain readable but excluded from default
`list_bausteine` queries.
