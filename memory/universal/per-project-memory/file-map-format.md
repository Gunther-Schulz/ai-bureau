# `file-map.md` format

Per-project AI's interpretation of project folder contents. Lives at
`<project_root>/_ai/file-map.md`. Authored by `survey-project` skill
when binding an existing project (folder pre-existed `_ai/`).

## Purpose

A bound project's folder typically contains a mix of:
- AI-managed artifacts (current Begründung, Festsetzungen, current Umweltbericht)
- Inputs (client-supplied source materials, base data, plot plans)
- Sent versions (Auslieferung/ — frozen snapshots of delivered artifacts)
- Correspondence (Schriftverkehr/ — emails, call notes, letters)
- TöB folders (per-Behörde Stellungnahmen)
- Cruft (legacy folders, duplicate copies, abandoned drafts)

`file-map.md` is the AI's interpretation: what each top-level path
IS, what it's used for, what its current relevance is. Skills consult
this to know where to read inputs from, where to write artifacts,
where to find historical context.

## Shape

```markdown
# File map — 26-04 Maxsolar - Friedrichshof

Generated 2026-04-28 by `survey-project`. User-confirmed via
orchestrator binding flow.

## Active artifacts (AI-managed)

| Path | Doctype | Status |
|---|---|---|
| `B-Plan/Begründung/B-Plan Begruendung.tex` | b-plan-begruendung | phase 5a draft |
| `B-Plan/Festsetzungen/Textteil-B-B-Plan.tex` | b-plan-festsetzungen | not started |

## Inputs

| Path | Source | Notes |
|---|---|---|
| `inputs/Lageplan_2025-11.dwg` | Vermessungsbüro Müller | base survey |
| `inputs/Bestandsbäume.shp` | Hendrik (deroekologe) | tree inventory |

## Sent versions

| Path | What | When |
|---|---|---|
| `Auslieferung/2026-02-12_Vorentwurf/` | Vorentwurf complete | 2026-02-12 |

## Correspondence

| Path | What | Indexed |
|---|---|---|
| `Schriftverkehr/eml/` | Saved client/Behörden mail | yes (RAG) |
| `Schriftverkehr/telefonnotizen/` | Call notes | partial |

## TöB

| Path | Behörde | Status |
|---|---|---|
| `TöB/UNB-Nordwestmecklenburg/` | UNB NWM | Stellungnahme erhalten 2026-03-15 |

## Cruft (ignore)

- `_alt_2024-11/` — pre-bind draft, superseded
- `Brendan-Test/` — test folder, never meant for delivery
```

## Maintenance

- Re-run `survey-project` when project folder is reorganized.
- Manual edits OK for adding categorizations of new files (orchestrator
  prompts when it sees an unrecognized path).
- The map is descriptive, not prescriptive — it captures what IS,
  not what MUST be.
