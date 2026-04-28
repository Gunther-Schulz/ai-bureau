# Snapshot convention

Per-project AI snapshots live at `<project_root>/_ai/snapshots/`.
Frozen point-in-time copies of artifacts at significant transitions
(send-gate fired, phase boundary crossed, major decision logged).

## Purpose

- **Audit trail**: prove what we sent on date X to authority Y.
- **Diff target**: what changed between Vorentwurf and Entwurf.
- **Recovery**: revert if a later edit pass goes wrong.

Distinct from `Auslieferung/` (the office-visible folder of delivered
artifacts) — snapshots are AI-internal versioning, retained per
retention policy. `Auslieferung/` is curated by the office.

## Shape

```
<project_root>/_ai/snapshots/
├── 2026-02-12_vorentwurf-complete/
│   ├── manifest.yaml                       # what's snapshot'd, why, by which event
│   ├── B-Plan_Begruendung.tex.snapshot
│   ├── B-Plan_Begruendung.pdf.snapshot
│   └── Textteil-B-B-Plan.tex.snapshot
├── 2026-04-28_phase-5a-end/
│   └── ...
└── retention.yaml                           # snapshot retention policy for this project
```

## manifest.yaml

```yaml
snapshot_id: 2026-04-28_phase-5a-end
created: 2026-04-28T14:32:00Z
trigger:
  type: phase-transition           # | send-gate | manual | major-decision
  from_phase: "Phase 5a"
  to_phase: "Phase 5b"
artifacts:
  - path: B-Plan/Begründung/B-Plan Begruendung.tex
    sha256: <hash>
  - path: B-Plan/Begründung/B-Plan Begruendung.pdf
    sha256: <hash>
state_md_at_snapshot:
  phase: "Phase 5a — frühzeitige Beteiligung"
  domains: [PV-FFA, Naturschutz]
notes: |
  End of frühzeitige Beteiligung. UNB and 3 TöB-Stellungnahmen
  integrated. Ready to open formelle Beteiligung.
```

## Retention policy

```yaml
# retention.yaml — defaults; override per project if needed
keep_all_send_gate: true             # never auto-delete a send-gate snapshot
keep_phase_transitions_for_days: 365
keep_manual_for_days: 730
prune_strategy: keep-monthly         # within retention window: keep 1 per month
```

Pruning happens lazily — when project disk usage check exceeds
threshold, orchestrator surfaces snapshot list with prune suggestions
for user approval (never auto-deletes).

## Triggers

- **send-gate fired** (orchestrator Checkpoint 4.3 send): mandatory snapshot.
- **phase transition**: snapshot before transition.
- **major decision logged in decisions.md**: snapshot offered.
- **manual**: orchestrator menu option "freeze current state".
