# `decisions.md` format

Chronological per-project decision log. Append-only. Lives at
`<project_root>/_ai/decisions.md`.

## Shape

Plain markdown, newest at top. Each entry:

```markdown
## 2026-04-28 — Phase transition 5a → 5b

**What**: closed frühzeitige Beteiligung, opening formelle Beteiligung.

**Why**: 6-week deadline reached; one substantive Stellungnahme
remained (UNB) and has been integrated into draft.

**By**: orchestrator (auto-logged on phase update).

**Consequences**:
- Begründung now versioned `v_5a_final` in snapshots/
- Next: send formelle Beteiligung notices, see send-gate checklist

---

## 2026-04-15 — Switched from §13a to §13b verfahren

**What**: switched from §13a Innenentwicklung to §13b Wohnnutzung.

**Why**: Geltungsbereich ≤ 10 000 m² confirmed; legal review
indicated §13b path is open and reduces UVP-Pflicht risk.

**By**: orchestrator + user (decision-checkpoint).

**Consequences**:
- §13b clauses propagated through Begründung Sec. 1
- Festsetzungen template adjusted
- See baustein `domain/Naturschutz/§13b-anwendung-vereinfacht.md`
```

## Append rules

- Orchestrator appends on every state transition (phase, scope,
  partner change).
- User-initiated decisions captured via the four-way menu's
  "decision-checkpoint" option also append here.
- NEVER edit past entries. Errors get a new entry referencing the
  previous one ("supersedes 2026-04-15 entry").
