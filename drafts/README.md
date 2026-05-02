# Drafts

Exploratory thinking / ideas / future-candidates. **NOT locked, NOT final, NOT load-bearing.**

This directory holds drafts of things that might become real later — marketing themes, naming explorations, positioning candidates, brainstorm output, "thinking I had while working on something else."

## Discipline

- **Drafts are loose**. Status: DRAFT. Don't treat as authoritative. Don't cascade-pass against drafts.
- **Drafts can be discarded**. If a draft never matures, it's archived or deleted; not a failure.
- **Drafts can graduate**. When a draft matures (via additional sharpening rounds + user lock), it lifts to its proper home: STRATEGY.md (positioning) / VISION.md (stance) / GLOSSARY.md (vocabulary) / `arch/<topic>.md` (architectural detail) / DRs / etc.
- **At graduation, the draft is REMOVED entirely** (not marked GRADUATED-TO-X; not retained as historical record). Graduated content lives in its canonical home (GLOSSARY entry / DR / ARCH topic / etc.); draft becomes redundant. Per provenance hygiene (coherence-audit Lens 5 v0.2.1): provenance lives in HANDOFF + git log + commit messages, not in retained-but-superseded draft files. Draft retention after graduation = stale-content drift risk + maintenance overhead.
- **Drafts are session-snapshot, not running log**. Each draft captures thinking AT A MOMENT. New thinking on the same theme should update the draft (or supersede with new file) — not endlessly append.

## What goes here vs other places

| Belongs in `drafts/` | Belongs elsewhere |
|---|---|
| Tagline / positioning variants explored but not locked | VISION header tagline (current locked stance) |
| Marketing themes / messaging candidates | STRATEGY.md (when Phase 5 surfaces) |
| Naming explorations beyond the working title | HANDOFF.md (working-title status) |
| Conceptual brainstorm / "what if we framed it as..." | GLOSSARY (locked vocabulary) |
| Future-architecture sketches | BACKLOG (Phase-tagged work items) |

If a thought is **load-bearing pending work** → `BACKLOG.md`.
If a thought is **cross-session AI behavior rule** → `memory/`.
If a thought is **exploratory idea / future-candidate** → `drafts/`.

## Format per draft

Each `drafts/<topic>.md` carries:

1. **Status banner** at top: `STATUS: DRAFT — not locked, not final, candidate among many`
2. **Origin context**: when surfaced, why captured here
3. **Body**: bullets / thoughts / candidates / open questions — loose form
4. **Maturity test**: what would graduate this to a locked doc? What signal triggers re-evaluation?
