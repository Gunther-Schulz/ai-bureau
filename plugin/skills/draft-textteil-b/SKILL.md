---
name: draft-textteil-b
description: This skill should be used when the user asks to draft a B-Plan Begründung (Textteil B) from project source materials. Triggered by phrases like "Entwurf Begründung", "Begründung schreiben", "draft Begründung for Friedrichshof", "Textteil B aufsetzen", "neue Begründung", "Vorentwurf Begründung". Phase A entry skill — orchestrator routes here when a project requires fresh Begründung drafting.
version: 0.1.0
license: MIT
---

# draft-textteil-b

Specialist skill for drafting a B-Plan Begründung from project source
materials. Phase A entry per the orchestrator's three-phase model
(draft → review → finalize). Produces a compileable LaTeX document
that goes through Phase B review next.

## Load this now

Read `PROCEDURE.md` from this skill's directory for the detailed
section-by-section workflow.

While operating, hold these references loaded:

- `<repo>/memory/domain/style/style-spec.md` — Doctype A spec
  (scrreprt + pdflatex, German conventions).
- `<repo>/memory/domain/conventions/korrektur-rules.md` — office
  writing conventions (German quotes, non-breaking spaces, number
  formatting).
- `<repo>/memory/domain/verfahren/bauleitplanung-phasen.md` — phase
  context for Stand-des-Aufstellungsverfahrens-section.
- `<repo>/plugin/skills/validate-checklist/references/checklists/
  b-plan-begruendung.md` — required-sections list.

## When invoked

By orchestrator (Phase A entry) or direct user request. Inputs:

- **Project** — bound or proposed; loads state.md if bound.
- **Source materials** — `inputs/` content (briefing, surveys,
  drone scans, regulatory inputs, prior Stellungnahmen).
- **Doctype focus** — confirmed `b-plan-begruendung` (not c, not
  Umweltbericht).
- **Verfahren type** — Regelverfahren / vereinfachtes (§13) /
  beschleunigtes (§13a) / vorhabensbezogen (§12). Affects sections
  + content.

## Behavior

1. **Bind project** if not already bound (delegate to orchestrator's
   binding flow + survey-project).

2. **Index project inputs** if not indexed (call ingest_project_inputs
   or fall back to per-input direct read). Document this in
   `_ai/decisions.md`.

3. **Search corpus for similar context**:
   - search_corpus(filter={doctype: b-plan-begruendung}) for similar
     past projects (same client, same Standort-typ, same Verfahren).
   - List candidates to user as reference material — user picks 1-3
     for active reference during drafting.

4. **Load applicable bausteine**:
   - list_bausteine(scope=domain, domain=b-plan) for reusable
     argumentation patterns.
   - For solar/PV: include artenschutz-domain bausteine where
     §44/§45 BNatSchG come into play.

5. **Scaffold the LaTeX project structure** if not present:
   - Copy template tree from `~/dev/Planungsbüro-Schulz/22-16-Maxsolar---Friedrichshof---B-Plan---Begruendung/`
     to `<project>/B-Plan/Begründung/`.
   - Instantiate `Projektdaten.tex` with project metadata from
     state.md (Gemeinde, Ortsteil, Landkreis, BPlanNr, BPlanName,
     BPlanTyp, GeltungsbereichHa, etc.).
   - `git init` the LaTeX subfolder if user wants Overleaf sync.

6. **Draft section-by-section** per PROCEDURE.md. Each section:
   - Identify required content from canonical-section list.
   - Pull source inputs relevant to section.
   - Search corpus for similar section in past projects.
   - Apply applicable bausteine (cite via History).
   - Draft prose adhering to korrektur-rules.
   - Surface to user for feedback before moving to next section.

7. **Module decisions** — when including/excluding optional sections
   (Brandschutz, Denkmalschutz, etc.), log to
   `_ai/module-decisions.md` per orchestrator Checkpoint 6.3.

8. **Compile via latexmk** after each meaningful checkpoint. Address
   build errors before moving forward (orchestrator Compile Gate
   4.1).

9. **Hand off to review-draft** when full draft is compileable —
   orchestrator transitions Phase A → Phase B.

## Output

Per section:
- Drafted .tex content written to `<project>/B-Plan/Begründung/Textbausteine/<section>.tex`.
- One-line summary of what's drafted + sources used (inputs cited,
  bausteine applied, corpus refs).
- Compile status after section integration.

End-of-draft:
- Full Begründung compiled to PDF.
- `_ai/decisions.md` entries for major argumentation choices.
- `_ai/module-decisions.md` entries for optional-section choices.
- Orchestrator-handoff to Phase B review.

## Edge cases

- **Source material insufficient for a required section**: surface
  gap; ask user for missing input or authorize "minimal default"
  language.
- **Verfahren-type uncertain**: refuse to draft phase-dependent
  sections (Stand des Aufstellungsverfahrens) until decided.
- **Existing draft conflicts**: if Textbausteine/<section>.tex
  exists with content, ask whether to replace, append, or skip.
  Don't silently overwrite.
- **Corpus search yields no similar past project**: surface; let
  user authorize "from scratch" or postpone until first comparable
  project exists.

## Tools used (when MCP backend lands)

- `search_corpus`, `read_corpus_file`, `search_inputs` — research.
- `list_bausteine`, `get_baustein` — pattern retrieval.
- `scaffold_project` — initial structure.
- `compile_latex` — build cycles.

Until backend lands: `Read`/`Glob`/`Grep` for direct file ops + Bash
for `latexmk`.
