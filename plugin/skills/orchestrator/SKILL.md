---
name: orchestrator
description: This skill should be used when the user works on Planungsbüro Schulz documents — any path under "/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte/" or "~/dev/Planungsbüro-Schulz/", mentions of B-Plan, Bebauungsplan, Begründung, Festsetzungen, Umweltbericht, Artenschutz, FFH-Vorprüfung, Stellungnahme, Abwägung, Gutachten, TöB, ZAV, or related German planning terminology, project work for clients like Maxsolar, W&R WPower, Solarfaktor, or any reference to a "YY-NN Client - Location" project naming pattern. Auto-loads at session start when PBS context is detected. Coordinates the entire conversational flow for all PBS document work.
version: 0.1.0
license: MIT
---

# PBS Bureau — Orchestrator

Master skill for Planungsbüro Schulz document workflows. Coordinates
drafting, review, and finalization across all PBS doctypes. The
framework is operational, not advisory — every PBS session runs
through it.

## Load this now

Read `PROCEDURE.md` from this skill's directory. Follow it.

While operating, hold these references loaded as authoritative
ground truth:

- `<repo>/memory/domain/style/style-spec.md` — canonical LaTeX styles
  for both PBS doctypes (Begründung scrreprt + pdflatex; Festsetzungen
  article + pdflatex with infinite-page geometry).
- `<repo>/memory/domain/conventions/korrektur-rules.md` — office
  writing conventions (German quotes `\glqq…\grqq{}`, non-breaking
  spaces before §/units/dates, German number formatting,
  hyphenation hints, source line wrap).
- `<repo>/memory/domain/doctypes.yaml` — registry of supported
  doctypes, template paths, master file conventions, ownership rules.

Resolve `<repo>` to the pbs-bureau plugin's repo root. From inside the
plugin, that is two directories up from this SKILL.md.

## System map

The skill coordinates four layers:

| Layer | Where | Purpose |
|---|---|---|
| Plugin | `<repo>/plugin/` | Skills (this one + specialists), agents, hooks |
| Backend | `<repo>/backend/` | MCP server, Docker stack (LanceDB + Ollama) — not yet built |
| Cross-cutting memory | `<repo>/memory/` | global / domain / office bausteine, specs, registry |
| Per-project memory | `<project-root>/_ai/` or `.ai/` | state, file-map, decisions, snapshots |

Project artifacts live under user-owned roots:

- **Hidrive (active client work):** `/mnt/data2t/hidrive/Öffentlich Planungsbüro Schulz/Projekte/<YY-NN ...>/`
- **Local (canonical LaTeX templates, per-doctype git working copies):** `~/dev/Planungsbüro-Schulz/`

The hidrive `Vorlagen/Latex/` folder is **not** authoritative — it
contains older or abandoned material. The local working copies are
the source of truth for templates.

## Specialist skills

The orchestrator routes to specialist skills rather than drafting,
reviewing, or finalizing directly. Specialists do not exist yet in
v0.1.0 — the orchestrator currently performs their work inline.
Routing intent is documented so behavior remains consistent when
specialists are extracted:

- `draft-textteil-b` — draft a Begründung from project sources
- `draft-textteil-c` — draft Textliche Festsetzungen (Teil B Text)
- `review-draft` — layered review of an existing draft
- `save-baustein` — capture a reusable text or argument to memory
- `promote-to-skill` — promote a frequently-used baustein to a skill
- `validate-latex-style` — diff a doc against `style-spec.md`
- `validate-checklist` — run doctype-specific required-section checks
- `verify-citations` — cross-check legal references against the RAG
- `draft-cover-mail` — draft transmittal mails to authorities
- `survey-project` — first-bind clustering of project files into a
  `_ai/file-map.md`

When a routing target does not yet exist as its own skill, perform
the work inline but log to `<repo>/memory/product-backlog.md` that
the specialist is wanted.

## What this skill is and is not

- **Is:** the always-on operational framework for any PBS session.
- **Is:** workflow-and-judgment hybrid — phases with gates, plus
  watch-list classification that surfaces decisions for the user.
- **Is not:** a drafting skill. Delegate to a specialist or perform
  inline; never bypass the framework.
- **Is not:** project-specific. Every project goes through the same
  framework with project-specific details loaded from per-project
  state.

## When to bypass

Never. Loaded means active. If a request is plainly unrelated to PBS
work (e.g., user asks an unrelated coding question with no PBS
context), this skill does not apply and `PROCEDURE.md` need not be
consulted. Detect non-PBS context from the absence of trigger
phrases and project paths.
