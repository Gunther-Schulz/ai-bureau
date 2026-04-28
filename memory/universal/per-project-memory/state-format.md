# `state.md` format

Per-project AI state file. One per project, lives at
`<project_root>/_ai/state.md` (or `.ai/state.md` — both supported).
Created by `setup_project` / `bind_project`, updated by orchestrator
on phase transitions.

## Frontmatter (required, machine-queryable)

```yaml
---
schema_version: 1
project_id: "26-04 Maxsolar - Friedrichshof"   # canonical folder name
client: "Maxsolar GmbH"                          # client display name
location: "Friedrichshof"                        # project location
bundesland: MV                                   # state code (BB|BW|...|TH)
                                                 # — drives state-extension lookup
domains: [PV-FFA, Naturschutz]                   # subset of office's
                                                 # scope.domains active for
                                                 # this project (drives skeleton +
                                                 # baustein retrieval scope)
phase: "Phase 5a — frühzeitige Beteiligung"      # current Bauleitplanung phase
practices: [main]                                # internal practices on this project
partners: []                                     # external co-producers
                                                 # (empty if office solo)
last_updated: 2026-04-28
---
```

## Body sections (markdown)

```markdown
## Status
1-2 paragraphs: where we are, what's next.

## Decisions log pointer
→ see `decisions.md` for chronological record.

## Active artifacts
- Begründung: `B-Plan/Begründung/B-Plan Begruendung.tex` — phase 5a draft
- Festsetzungen: `B-Plan/Festsetzungen/Textteil-B-B-Plan.tex` — not started
- Umweltbericht: deferred to phase 6

## Open questions
- Bullet list of pending decisions, blocked items, awaiting input.
```

## Update rules

- Phase transitions: orchestrator updates `phase` + appends to
  `decisions.md`, never silently.
- Adding/removing a domain (project widens or narrows scope):
  update `domains[]` so baustein retrieval and skeleton composition
  reflect the change.
- `bundesland` should not change post-bind (a project doesn't
  change Bundesland); if it does, that's a structural mistake to
  surface.

## Schema version

`schema_version: 1` is the initial shape. Field additions bump this;
state.md migrations live in
`backend/.../tools/state_migrations/v<n>_to_v<n+1>.py`.
