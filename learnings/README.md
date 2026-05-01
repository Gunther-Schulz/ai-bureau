# Learnings — observations from building pbs-bureau

**Scope**: this folder captures **preliminary methodological observations** about how building AI-centric apps differs from traditional software development. Distinct from:

- `DISCIPLINES.md` — locked cross-session working rules
- `memory/` — locked behavioral feedback rules (in user's per-project memory dir)
- `MAINTENANCE.md` / `VISION.md` / `GLOSSARY.md` — architectural foundation
- `HANDOFF.md` — current-session live state

**This folder holds observations, not locked rules.** Each observation is preliminary — mostly true probably, not fully proven yet. Observations earn promotion to discipline status (memory feedback rule, ARCH discipline, or DR) when they hold across multiple sessions and surface stable patterns.

## Scope: procedure/methodology only

This folder is for **procedural and methodological observations** about how to develop AI-centric apps — patterns of work, collaboration disciplines, design-process discoveries, things we learn about WORKING on AI apps.

**Not in scope** (these go elsewhere):

- **Implementation-level technical observations** — what specific tools (PydanticAI, LangChain, Pydantic, etc.) do or don't do; what kinds of validation are possible; technical capabilities and constraints. These belong in ARCH / DRs (Phase 3+) or HANDOFF "Phase 3 considerations" if surfaced before ARCH rebuild.
- **Architectural decisions** — go to DR / GLOSSARY / MAINTENANCE.md (locked structural shape)
- **Behavioral rules for AI-user interaction** — go to `memory/` feedback files (immediately codifiable cross-session rules)

The boundary: HOW WE WORK (procedural) belongs here. WHAT WE BUILD WITH (implementation) belongs in architecture territory.

## How to use

When a new pattern surfaces during a session:

| Where it goes | Pattern type |
|---|---|
| Memory feedback file (in `memory/`) | Behavioral rule for AI-user interaction (immediately codifiable) |
| DR / GLOSSARY entry / MAINTENANCE.md | Architectural decision (locks structural shape) |
| HANDOFF.md "Phase X considerations" | Implementation-level observation surfaced before its target phase |
| **Here (`learnings/<topic>.md`)** | Procedural/methodological observation about HOW WE WORK on AI app dev (preliminary; not yet discipline) |

When `learnings/` observations accumulate enough to suggest stable patterns (typically 3-5 sessions of evidence), distill into structured topic-specific docs (e.g., split `ai-app-development.md` into `cascade-discipline-observations.md`, `vocabulary-lock-observations.md`, etc.). Eventually feed into the AI-app-development-facilitation skill (per HANDOFF "Future ROADMAP items").

## Files

- `ai-app-development.md` — first batch of observations (session 16 launch); expected to grow + split as patterns differentiate

## Status discipline

When citing observations from this folder elsewhere in the corpus, mark them as preliminary:
- "Per `learnings/X.md` (preliminary observation), Y" — flags status
- Don't treat learnings as locked discipline; that elevation requires explicit review
